"""
Enhanced Gemini Helper with Context Awareness
Gemini sẽ tự động biết ngữ cảnh: cung nào, chủ đề gì, đang xem phần nào
"""

import google.generativeai as genai
import os
import requests
import json
import time

# Robust Fallback Import
try:
    from free_ai_helper import FreeAIHelper
except ImportError:
    # If fails (rare), define a dummy
    class FreeAIHelper:
        def __getattr__(self, name):
            return lambda *args, **kwargs: "⚠️ Chế độ Offline không khả dụng (Lỗi Import)."

class GeminiQMDGHelper:
    """Helper class for Gemini AI with QMDG specific knowledge and grounding"""
    
    _response_cache = {}
    _cache_max_size = 100
    
    def __init__(self, api_key_input):
        import hashlib
        import re
        
        # ROBUST KEY EXTRACTION (REGEX)
        # Finds anything looking liek a Google API Key: AIzaSy... (39 chars)
        self.api_keys = re.findall(r"AIza[0-9A-Za-z-_]{35}", str(api_key_input))
        
        # Fallback if regex fails (e.g. valid key but unusual format)
        if not self.api_keys and api_key_input:
             self.api_keys = [k.strip() for k in str(api_key_input).split(',') if k.strip()]

        self.current_key_index = 0
        self.api_key = self.api_keys[0] if self.api_keys else None
        
        self.version = "V1.9.1-SmartParser"
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self._failed_models = set()
        self._hashlib = hashlib
        self.current_context = {
            'topic': None, 
            'palace': None, 
            'chart_data': None, 
            'last_action': None, 
            'dung_than': []
        }
        self.max_retries = 3
        self.base_delay = 2
        self.n8n_url = None
        self.n8n_timeout = 90
        
        # Initialize Helpers
        self.model = self._get_best_model()
        self.fallback_helper = FreeAIHelper()

    def _rotate_key(self):
        """Switch to next available API Key"""
        if not self.api_keys or len(self.api_keys) <= 1:
            return False
            
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.api_key = self.api_keys[self.current_key_index]
        print(f"🔄 Rotating to API Key #{self.current_key_index + 1}")
        try:
            genai.configure(api_key=self.api_key)
            return True
        except:
            return False

    def _get_best_model(self):
        # 404 ERROR FIX: Use specific version codes first, then generics
        # Re-added gemini-1.0-pro as ultimate fallback if Flash fails
        models_to_try = [
            'gemini-1.5-flash-001',   # Specific stable version
            'gemini-1.5-flash-002',   # Newer specific version
            'gemini-1.5-flash',       # Generic alias
            'gemini-1.5-flash-8b',    # Specialized
            'gemini-pro',             # V1.0 Stable (Last Resort)
        ]
        
        # First pass: try with a simple ping
        for name in models_to_try:
            if name in self._failed_models: continue
            try:
                m = genai.GenerativeModel(name)
                # Quick check without tool configuration first
                m.generate_content("ping", generation_config={"max_output_tokens": 1})
                return m
            except Exception as e:
                # 404 or other errors -> mark as failed and try next
                # print(f"Model {name} check failed: {e}")
                self._failed_models.add(name)
                continue
        
        # Fallback to a guaranteed model (even if it might fail 429 later, better than 404 crash)
        return genai.GenerativeModel('gemini-1.5-flash')

    def test_connection(self):
        try:
            resp = self.model.generate_content("ping", generation_config={"max_output_tokens": 1})
            return True, "Kết nối thành công!"
        except Exception as e:
            return False, f"Lỗi kết nối: {str(e)}"


    # ... (cached response methods remain same) ...

    def safe_get_text(self, response):
        try:
            if not response.candidates: return "⚠️"
            candidate = response.candidates[0]
            try:
                if response.text: return response.text
            except: pass
            if candidate.content and candidate.content.parts:
                return "".join([p.text for p in candidate.content.parts if hasattr(p, 'text')])
            return "⚠️"
        except: return "⚠️"
    
    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        # ... (cache check remains) ...
        
        # dynamic tool selection
        tools = []
        if use_web_search:
            try:
                tools = [{"google_search": {}}]
            except:
                tools = [{"google_search_retrieval": {}}]

        for attempt in range(self.max_retries):
            try:
                if tools:
                    resp = self.model.generate_content(prompt, tools=tools)
                else:
                    resp = self.model.generate_content(prompt)
                text = self.safe_get_text(resp)
                if "⚠️" not in text:
                    self._cache_response(prompt, text)
                    return text
            except Exception as e:
                err_str = str(e).lower()
                if "quota" in err_str or "429" in err_str or "resource" in err_str:
                    print(f"⚠️ Quota hit on {self.model.model_name}")
                    
                    # STRATEGY 1: ROTATE KEY FIRST
                    if self._rotate_key():
                        time.sleep(1)
                        continue
                        
                    # STRATEGY 2: ROTATE MODEL
                    try:
                        models = [
                            'gemini-1.5-flash', 'gemini-1.5-flash-8b', 
                            'gemini-2.0-flash-lite-001'
                        ]
                        import random
                        next_model = random.choice(models)
                        self.model = genai.GenerativeModel(next_model)
                        time.sleep(1)
                        continue
                    except: pass

                time.sleep(self.base_delay * (2 ** attempt))
                continue
        
        return "🛑 Hết hạn mức"

    # --- WRAPPED METHODS FOR OFFLINE RESILIENCE ---

    def answer_question(self, question, chart_data=None, topic=None):
        res = self._call_ai(f"Câu hỏi: {question}", use_web_search=True)
        if "🛑" in res:
            return self.fallback_helper.answer_question(question, chart_data, topic) + "\n\n_(⚠️ Chế độ Offline do Quota)_"
        return res

    def analyze_palace(self, palace_data, topic):
        res = self._call_ai(f"Phân tích cung Kỳ Môn: {topic} - Data: {json.dumps(palace_data)}", use_web_search=True)
        if "🛑" in res:
            return self.fallback_helper.analyze_palace(palace_data, topic) + "\n\n_(⚠️ Chế độ Offline do Quota)_"
        return res

    def explain_element(self, element_type, element_name):
        res = self._call_ai(f"Giải thích chi tiết yếu tố {element_type} trong Kỳ Môn Độn Giáp: {element_name}", use_web_search=True)
        if "🛑" in res:
            return self.fallback_helper.explain_element(element_type, element_name) + "\n\n_(⚠️ Chế độ Offline do Quota)_"
        return res

    def analyze_mai_hao(self, res_data, topic="Chung"):
        res = self._call_ai(f"Luận giải quẻ Mai Hoa Dịch Số cho chủ đề '{topic}': {json.dumps(res_data)}", use_web_search=True)
        if "🛑" in res:
            return self.fallback_helper.analyze_mai_hao(res_data, topic) + "\n\n_(⚠️ Chế độ Offline do Quota)_"
        return res

    def analyze_luc_hao(self, res_data, topic="Chung"):
        res = self._call_ai(f"Luận giải quẻ Lục Hào cho chủ đề '{topic}': {json.dumps(res_data)}", use_web_search=True)
        if "🛑" in res:
            return self.fallback_helper.analyze_luc_hao(res_data, topic) + "\n\n_(⚠️ Chế độ Offline do Quota)_"
        return res

    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None):
        res = self._call_ai(f"Phân tích tổng quan bàn Kỳ Môn: {topic}. Dữ liệu: {json.dumps(chart_data)}", use_web_search=True)
        if "🛑" in res:
            return self.fallback_helper.comprehensive_analysis(chart_data, topic, dung_than_info) + "\n\n_(⚠️ Chế độ Offline do Quota)_"
        return res

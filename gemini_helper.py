"""
Enhanced Gemini Helper with Context Awareness
Gemini sẽ tự động biết ngữ cảnh: cung nào, chủ đề gì, đang xem phần nào
"""

import google.generativeai as genai
import os
import requests
import json
import time

class GeminiQMDGHelper:
    """Helper class for Gemini AI with QMDG specific knowledge and grounding"""
    
    _response_cache = {}
    _cache_max_size = 100
    
    def __init__(self, api_key):
        import hashlib
        self.api_key = api_key
        self.version = "V1.7.5"
        genai.configure(api_key=api_key)
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
        self.model = self._get_best_model()

    def _get_cached_response(self, prompt):
        try:
            prompt_hash = self._hashlib.md5(prompt.encode()).hexdigest()
            return self._response_cache.get(prompt_hash)
        except: return None

    def _cache_response(self, prompt, response):
        try:
            if len(self._response_cache) >= self._cache_max_size:
                del self._response_cache[next(iter(self._response_cache))]
            prompt_hash = self._hashlib.md5(prompt.encode()).hexdigest()
            self._response_cache[prompt_hash] = response
        except: pass

    def set_n8n_url(self, url):
        self.n8n_url = url

    def update_context(self, **kwargs):
        self.current_context.update(kwargs)

    def _get_best_model(self):
        models_to_try = [
            'gemini-1.5-flash', 'gemini-1.5-flash-latest', 
            'gemini-2.0-flash', 'gemini-2.0-flash-001', 'gemini-2.0-flash-lite-001',
            'gemini-1.5-pro-latest', 'gemini-1.5-pro'
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
                print(f"Model {name} check failed: {e}")
                continue
        
        # Fallback to a guaranteed model
        return genai.GenerativeModel('gemini-1.5-flash')

    def test_connection(self):
        try:
            resp = self.model.generate_content("ping", generation_config={"max_output_tokens": 1})
            return True, "Kết nối thành công!"
        except Exception as e:
            return False, f"Lỗi kết nối: {str(e)}"

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
        if not use_web_search:
            cached = self._get_cached_response(prompt)
            if cached: return cached
        
        # dynamic tool selection - Updated for SDK 0.8.3+
        tools = []
        if use_web_search:
            # Standard way to enable Google Search for 1.5 and 2.0 models in modern SDK
            try:
                tools = [{"google_search": {}}]
            except:
                # Fallback format if needed
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
                if "quota" in str(e).lower():
                    time.sleep(self.base_delay * (2 ** attempt))
                    continue
        return "🛑 Hết hạn mức."

    def answer_question(self, question, chart_data=None, topic=None):
        return self._call_ai(f"Câu hỏi: {question}", use_web_search=True)

    def analyze_palace(self, palace_data, topic):
        return self._call_ai(f"Phân tích cung Kỳ Môn: {topic} - Data: {json.dumps(palace_data)}", use_web_search=True)

    def explain_element(self, element_type, element_name):
        return self._call_ai(f"Giải thích chi tiết yếu tố {element_type} trong Kỳ Môn Độn Giáp: {element_name}", use_web_search=True)

    def analyze_mai_hao(self, res, topic="Chung"):
        return self._call_ai(f"Luận giải quẻ Mai Hoa Dịch Số cho chủ đề '{topic}': {json.dumps(res)}", use_web_search=True)

    def analyze_luc_hao(self, res, topic="Chung"):
        return self._call_ai(f"Luận giải quẻ Lục Hào cho chủ đề '{topic}': {json.dumps(res)}", use_web_search=True)

    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None):
        return self._call_ai(f"Phân tích tổng quan bàn Kỳ Môn: {topic}. Dữ liệu: {json.dumps(chart_data)}", use_web_search=True)

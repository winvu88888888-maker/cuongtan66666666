"""
Enhanced Gemini Helper with Context Awareness (V2.0 - Secretary Mode)
"""

import google.generativeai as genai
import os
import requests
import json
import time
import hashlib
import re

# Robust Fallback Import
try:
    from free_ai_helper import FreeAIHelper
except ImportError:
    class FreeAIHelper:
        def __getattr__(self, name):
            return lambda *args, **kwargs: "⚠️ Chế độ Offline không khả dụng (Lỗi Import)."

class GeminiQMDGHelper:
    """Helper class for Gemini AI with QMDG specific knowledge and grounding"""
    
    _response_cache = {}
    _cache_max_size = 100
    
    def __init__(self, api_key_input):
        # ROBUST KEY EXTRACTION
        self.api_keys = re.findall(r"AIza[0-9A-Za-z-_]{35}", str(api_key_input))
        if not self.api_keys and api_key_input:
             self.api_keys = [k.strip() for k in str(api_key_input).split(',') if k.strip()]

        self.current_key_index = 0
        self.api_key = self.api_keys[0] if self.api_keys else None
        
        self.version = "V2.0-Secretary" # Marked to verify update
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self._failed_models = set()
        self._hashlib = hashlib
        self.max_retries = 2
        self.base_delay = 1
        self.n8n_url = None
        self.n8n_timeout = 8
        
        self.model = self._get_best_model()
        self.fallback_helper = FreeAIHelper()

    def _get_best_model(self):
        models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        for m_name in models:
            try:
                m = genai.GenerativeModel(m_name)
                return m
            except: continue
        return genai.GenerativeModel('gemini-pro')

    def test_connection(self):
        try:
            self.model.generate_content("ping")
            return True, "Kết nối OK"
        except Exception as e:
            return False, str(e)
            
    def set_n8n_url(self, url):
        self.n8n_url = url

    # --- CORE INTELLIGENCE: INTENT CLASSIFIER ---
    def classify_intent(self, text):
        """Phân loại ý định: 'social' vs 'question'"""
        text = text.lower().strip()
        social_keywords = ["chào", "hello", "hi", "bạn ơi", "alo", "có đó không", "giỏi quá", "hay quá", "tạm biệt", "cảm ơn"]
        if len(text.split()) < 5 and any(k in text for k in social_keywords): return 'social'
        return 'question'

    def call_n8n_webhook(self, question, context_summary):
        """Gọi n8n để lấy dữ liệu thực tế"""
        if not self.n8n_url: return None
        try:
            # Standard Schema
            payload = {
                "question": question,
                "context": context_summary,
                "timestamp": str(self._hashlib.sha256(question.encode()).hexdigest())[:10]
            }
            resp = requests.post(self.n8n_url, json=payload, timeout=self.n8n_timeout)
            if resp.status_code == 200:
                data = resp.json()
                # Support multiple schema variations
                return data.get('output') or data.get('text') or data.get('result')
            return None
        except Exception as e:
            print(f"n8n Error: {e}")
            return None

    # --- MASTERMIND: PROMPT ENGINEERING ---
    def _create_expert_prompt(self, user_input):
        import streamlit as st
        
        # 1. Gather State
        try:
            current_topic = st.session_state.get('chu_de_hien_tai', 'Chung')
        except: current_topic = "Chung"

        is_def = any(k in user_input.lower() for k in ["là gì", "nghĩa là", "ý nghĩa"])
        
        # 2. Intent Classification
        intent = self.classify_intent(user_input)
        
        # 3. Knowledge Retrieval
        knowledge = ""
        
        # A. Social
        if intent == 'social':
            knowledge += "[CHẾ ĐỘ XÃ GIAO]: Người dùng chào hỏi. Hãy đáp lại ngắn gọn, thân thiện, không phân tích."
        
        # B. Definition (Dictionary)
        elif is_def:
            try:
                from skill_library import lookup_concept
                defin = lookup_concept(user_input)
                if defin:
                    knowledge += f"\n[TỪ ĐIỂN]: {defin['summary']}\n(YÊU CẦU: Trả lời đúng định nghĩa này.)"
            except: pass
            
        # C. Topic Binding (Only if not definition)
        if intent == 'question' and not is_def:
             knowledge += f"\n[CHỦ ĐỀ UI]: {current_topic}\n"
             
        # D. n8n
        if intent == 'question' and self.n8n_url:
             n8n_data = self.call_n8n_webhook(user_input, f"Topic: {current_topic}")
             if n8n_data:
                 knowledge += f"\n[DỮ LIỆU THỰC TẾ N8N]: {n8n_data}\n"

        # 4. System Prompt
        sys_prompt = (
            "VAI TRÒ: Trợ lý Huyền Học Thông Minh.\n"
            "NGUYÊN TẮC: \n"
            "1. 'social' -> Chào hỏi ngắn gọn.\n"
            "2. Hỏi định nghĩa -> Trả lời định nghĩa ngay.\n"
            "3. Hỏi vấn đề (Tài lộc, Tình duyên) -> Dùng kiến thức Huyền Học để giải quyết.\n"
            f"THÔNG TIN BỔ SUNG: {knowledge}\n"
        )
        return sys_prompt + f"\nUSER: {user_input}"

    def answer_question(self, question, chart_data=None, topic=None):
        final_prompt = self._create_expert_prompt(question)
        return self._call_ai_raw(final_prompt)

    # --- BASIC AI CALLER ---
    def _call_ai_raw(self, prompt):
        try:
            # Use 'google_search_retrieval' for grounding if possible
            tools = [{"google_search_retrieval": {}}]
            try:
                resp = self.model.generate_content(prompt, tools=tools)
            except:
                # Fallback no tools
                resp = self.model.generate_content(prompt)
                
            if resp.text: return resp.text
            return "⚠️ AI không phản hồi."
        except Exception as e:
            return f"🛑 Lỗi: {e}"

    # --- WRAPPERS FOR COMPATIBILITY ---
    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None):
        return self.answer_question(f"Phân tích bàn cờ chủ đề {topic}: {json.dumps(chart_data)}")
        
    def analyze_palace(self, data, topic):
        return self.answer_question(f"Phân tích cung {topic}: {json.dumps(data)}")

    def analyze_mai_hao(self, data, topic):
        return self.answer_question(f"Phân tích Mai Hoa {topic}: {json.dumps(data)}")

    def analyze_luc_hao(self, data, topic):
        return self.answer_question(f"Phân tích Lục Hào {topic}: {json.dumps(data)}")

    def explain_element(self, type, name):
         return self.answer_question(f"Giải thích {type} {name}")

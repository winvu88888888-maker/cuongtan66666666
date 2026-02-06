"""
Enhanced Gemini Helper with Context Awareness (V2.2 - Smart Router)
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
        
        self.version = "V2.2-SmartRouter" # Marked to verify update
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
        # Default placeholder, actual model is found in test_connection
        return genai.GenerativeModel('gemini-1.5-flash')

    def test_connection(self):
        candidate_models = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro',
            'gemini-1.5-pro-latest',
            'gemini-pro',
            'gemini-1.0-pro'
        ]
        
        last_error = ""
        for m_name in candidate_models:
            try:
                temp_model = genai.GenerativeModel(m_name)
                # Active Test
                resp = temp_model.generate_content("ping")
                if resp:
                    # Found a working one!
                    self.model = temp_model
                    self.active_model_name = m_name
                    return True, f"Kết nối OK (Model: {m_name})"
            except Exception as e:
                last_error = str(e)
                continue
                
        return False, f"Không tìm thấy model nào hoạt động. Lỗi cuối: {last_error}"


            
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

    def safe_get_text(self, response):
        try:
            if not response.candidates: return "⚠️"
            if response.text: return response.text
        except: pass
        return "⚠️"

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
    
    # --- WRAPPED METHODS FOR OFFLINE RESILIENCE ---
    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        return self._call_ai_raw(prompt)

    # --- PROCESS RESPONSE (Parsing logic) ---
    def _process_response(self, text):
        import re
        import streamlit as st
        
        thinking = ""
        answer = text
        
        # Regex search for the thinking block
        match_thinking = re.search(r'\[SUY_LUAN\](.*?)\[/SUY_LUAN\]', text, re.DOTALL)
        if match_thinking:
            thinking = match_thinking.group(1).strip()
            answer = text.replace(match_thinking.group(0), "").strip()
            
            # Display the thinking process visually (AntiGravity Style)
            st.markdown("""
            <style>
            .ag-thinking {
                background-color: #f0f9ff;
                border: 1px solid #7dd3fc;
                border-radius: 8px;
                padding: 10px;
                font-family: monospace;
                font-size: 0.9em;
                color: #0369a1;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)
            with st.expander("⚡ Antigravity Quy Trình Tư Duy (Click để xem)", expanded=False):
                st.markdown(f'<div class="ag-thinking">{thinking}</div>', unsafe_allow_html=True)

        # Regex search for the Conclusion block (New Standard)
        match_conclusion = re.search(r'\[KET_LUAN\](.*?)\[/KET_LUAN\]', answer, re.DOTALL)
        if match_conclusion:
            answer = match_conclusion.group(1).strip()
        
        # Fallback: If AI put everything in thinking block and answer is empty
        if not answer.strip() and thinking:
            answer = "ℹ️ **Kết quả từ quy trình suy luận:**\n\n" + thinking
            
        return answer


    def answer_question(self, question, chart_data=None, topic=None): 
        # 1. CLASSIFY INTENT
        import streamlit as st
        
        intent = self.classify_intent(question)
        
        # 2. FAST PATH: SOCIAL & GREETING
        if intent == 'social':
            # Bypass Orchestrator for simple greetings
            return self._call_ai_raw(f"User nói: '{question}'. Hãy đáp lại thật ngắn gọn, thân thiện (1 câu). Ví dụ: 'Chào bạn, tôi có thể giúp gì cho bạn?'")

        # 3. KNOWLEDGE PATH: DEFINITIONS
        is_def = any(k in question.lower() for k in ["là gì", "nghĩa là", "ý nghĩa", "giải thích"])
        if is_def:
             prompt = self._create_expert_prompt(question)
             return self._call_ai_raw(prompt)

        # 4. EXTERNAL PATH: N8N (News, Real-time Data)
        n8n_result = None
        # Only call n8n if url is set AND not a pure metaphysical term lookup
        # (This prevents calling n8n for "Sinh Môn là gì")
        if self.n8n_url and not any(k in question.lower() for k in ["bàn cờ", "dụng thần", "cung", "quẻ", "sao", "cửa"]):
             try:
                n8n_result = self.call_n8n_webhook(question, f"User Interest: {topic}")
             except: pass
        
        # If n8n gave a clear result, use it directly!
        if n8n_result:
             # Synthesize n8n result simply
             prompt = (
                 f"User hỏi: {question}\n"
                 f"Thông tin tìm được từ Internet (N8N): {n8n_result}\n"
                 f"Yêu cầu: Trả lời câu hỏi user dựa trên thông tin trên. Ngắn gọn, súc tích."
             )
             return self.safe_get_text(self.model.generate_content(prompt))

        # 5. DEEP PATH: CALCULATOR & ANALYST (Orchestrator)
        from qmdg_orchestrator import AIOrchestrator
        orc = AIOrchestrator(self)
        
        raw = orc.run_pipeline(
            question, 
            current_topic=topic or "Chung", 
            chart_data=chart_data or st.session_state.get('chart_data'),
            mai_hoa_data=st.session_state.get('mai_hoa_result'),
            luc_hao_data=st.session_state.get('luc_hao_result')
        )
        return self._process_response(raw)

    def analyze_palace(self, palace_data, topic): 
        prompt = self._create_expert_prompt(f"Phân tích Cung chi tiết ({topic})")
        # Reuse logic? No, specific analysis needs tools.
        # Ideally this should also use orchestrator for consistency, but for now raw is fine or Orchestrator.
        # Let's keep it using _create_expert which injects context.
        prompt = f"Phân tích Cung: {topic}. Data: {json.dumps(palace_data)}"
        return self._call_ai_raw(prompt)

    def explain_element(self, type, name):
         return self.answer_question(f"Giải thích {type} {name}")
    
    def analyze_mai_hao(self, res_data, topic="Chung"): 
        return self.answer_question(f"Luận quẻ Mai Hoa ({topic}): {json.dumps(res_data)}")

    def analyze_luc_hao(self, res_data, topic="Chung"): 
         return self.answer_question(f"Luận quẻ Lục Hào ({topic}): {json.dumps(res_data)}")

    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None): 
         return self.answer_question(f"Tổng quan bàn Kỳ Môn ({topic})")

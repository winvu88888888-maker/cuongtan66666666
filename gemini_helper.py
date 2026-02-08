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

# Import QMDG Complete Knowledge Base
try:
    from qmdg_knowledge_complete import (
        CUU_CUNG, CUU_TINH, BAT_MON, BAT_THAN, THAP_THIEN_CAN,
        tra_cuu_cung, tra_cuu_sao, tra_cuu_mon, tra_cuu_than, tra_cuu_can,
        xac_dinh_gioi_tinh_ke_lay, xac_dinh_huong_khoang_cach, kha_nang_tim_duoc
    )
    QMDG_KNOWLEDGE_LOADED = True
except ImportError:
    QMDG_KNOWLEDGE_LOADED = False

# Import Advanced Rules (64 Quẻ, Màu sắc, Quen/Lạ)
try:
    from qmdg_advanced_rules import (
        MAU_SAC_NGU_HANH, QUEN_LA_QUY_TAC, KHOANG_CACH_CHI_TIET,
        KHA_NANG_LAY_LAI, QUE_64, phan_tich_tim_do_chi_tiet
    )
    ADVANCED_RULES_LOADED = True
except ImportError:
    ADVANCED_RULES_LOADED = False

# Import Complete Inference Rules (Màu sắc, Giá trị, Kẻ trộm bị bắt, v.v.)
try:
    from qmdg_inference_rules import (
        phan_tich_toan_dien_tim_do, format_ket_qua_cho_ai,
        tinh_mau_sac_vat, tinh_gia_tri_vat, tinh_khoang_cach,
        tinh_kha_nang_bi_bat, xac_dinh_ke_lay
    )
    INFERENCE_RULES_LOADED = True
except ImportError:
    INFERENCE_RULES_LOADED = False

# Import Auto-Learning System
try:
    from auto_knowledge_updater import (
        auto_learn_from_question, get_learned_knowledge,
        LINH_VUC_CO_SAN, get_field_detail_level
    )
    AUTO_LEARN_LOADED = True
except ImportError:
    AUTO_LEARN_LOADED = False

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
        try:
            # 1. Ask Google: "What models do I have?"
            # This is the most robust way to avoid 404s on names.
            valid_models = []
            try:
                available = list(genai.list_models())
                for m in available:
                    if 'generateContent' in m.supported_generation_methods:
                        valid_models.append(m.name)
            except Exception as e:
                return False, f"Lỗi liệt kê model (API Key hỏng?): {str(e)}"

            if not valid_models:
                return False, "Key này không có quyền truy cập bất kỳ Model nào!"

            # 2. Prioritize modern models
            # We sort/filter to pick the best one.
            # Names come like 'models/gemini-1.5-flash-001'
            priority_order = ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-2.0-flash-001']
            
            chosen_model_name = None
            
            # Simple match logic
            for p in priority_order:
                for vm in valid_models:
                    if p in vm:
                        chosen_model_name = vm
                        break
                if chosen_model_name: break
            
            # Fallback to FIRST valid model if no priority match
            if not chosen_model_name:
                chosen_model_name = valid_models[0]

            # 3. Final Test
            self.model = genai.GenerativeModel(chosen_model_name)
            self.model.generate_content("ping")
            self.active_model_name = chosen_model_name
            
            return True, f"Kết nối OK! (Model: {chosen_model_name})"

        except Exception as e:
            return False, f"Lỗi kết nối cuối cùng: {str(e)}"


            
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

        # 4. System Prompt - KIẾN THỨC HOÀN CHỈNH (QMDG + MAI HOA + KINH DỊCH)
        sys_prompt = (
            "VAI TRÒ: Chuyên gia Huyền Học (Kỳ Môn + Mai Hoa + Kinh Dịch)\n"
            "NGUYÊN TẮC: KHÔNG nói 'không có thông tin' - LUÔN suy luận và đưa SỐ LIỆU CỤ THỂ\n\n"
            
            "=== 🔮 BẢNG 8 QUÁI (MAI HOA + KINH DỊCH) ===\n"
            "| Quái | Hành | Hướng | Giới tính | Tuổi | Màu sắc |\n"
            "| Càn | Kim | TÂY BẮC | NAM, cha, lãnh đạo | >50 | Trắng |\n"
            "| Khôn | Thổ | TÂY NAM | NỮ, mẹ, phụ nữ già | >45 | Vàng/Nâu |\n"
            "| Chấn | Mộc | ĐÔNG | NAM, con trai cả | 25-40 | Xanh lá |\n"
            "| Tốn | Mộc | ĐÔNG NAM | NỮ, con gái cả | 25-35 | Xanh lá |\n"
            "| Khảm | Thủy | BẮC | NAM, con trai giữa | 30-45 | Đen/Xanh dương |\n"
            "| Ly | Hỏa | NAM | NỮ, con gái giữa | 25-40 | Đỏ/Cam |\n"
            "| Cấn | Thổ | ĐÔNG BẮC | NAM, con trai út | 15-25 | Vàng/Nâu |\n"
            "| Đoài | Kim | TÂY | NỮ, con gái út | 15-25 | Trắng |\n\n"
            
            "=== 📍 BẢNG CUNG VỊ (KHOẢNG CÁCH + HƯỚNG) ===\n"
            "| Cung | Quái | Hướng | Khoảng cách | Địa điểm |\n"
            "| 1 | Khảm | BẮC | 100-1000m | Nơi có nước, WC |\n"
            "| 2 | Khôn | TÂY NAM | 50-500m | Đất trống, ruộng |\n"
            "| 3 | Chấn | ĐÔNG | 300-3000m | Chợ, nơi đông người |\n"
            "| 4 | Tốn | ĐÔNG NAM | 400-4000m | Văn phòng, nơi cao |\n"
            "| 5 | - | TẠI CHỖ | 0-200m | Trong nhà |\n"
            "| 6 | Càn | TÂY BẮC | 600-6000m | Cơ quan, nhà cao |\n"
            "| 7 | Đoài | TÂY | 70-700m | Quán xá, karaoke |\n"
            "| 8 | Cấn | ĐÔNG BẮC | 80-800m | Núi, kho, cửa hàng |\n"
            "| 9 | Ly | NAM | 900-9000m | Trường học, nhà bếp |\n\n"
            
            "=== 👤 GIỚI TÍNH NGƯỜI LẤY ===\n"
            "NAM: Canh, Mậu, Nhâm, Bính + Thiên Bồng, Huyền Vũ, Bạch Hổ + Càn, Chấn, Khảm, Cấn\n"
            "NỮ: Ất, Kỷ, Quý, Đinh + Thái Âm, Lục Hợp + Khôn, Tốn, Ly, Đoài\n\n"
            
            "=== 🎨 MÀU SẮC VẬT MẤT (THEO NGŨ HÀNH) ===\n"
            "Kim = TRẮNG/BẠC | Mộc = XANH LÁ | Thủy = ĐEN | Hỏa = ĐỎ | Thổ = VÀNG/NÂU\n\n"
            
            "=== 🔗 QUEN HAY LẠ ===\n"
            "Huyền Vũ/Bạch Hổ = 90% NGƯỜI LẠ | Thái Âm/Lục Hợp = 70% QUEN\n"
            "Cung 2/5/8 = 70% QUEN | Cung 1/6 = 70% LẠ\n\n"
            
            "=== 📊 KHẢ NĂNG TÌM ĐƯỢC (THEO MÔN) ===\n"
            "Sinh=85% | Hưu=80% | Khai=70% | Cảnh=50% | Đỗ=40% | Thương=25% | Kinh=15% | Tử=5%\n\n"
            
            "=== ✅ FORMAT TRẢ LỜI BẮT BUỘC ===\n"
            "👤 Ai lấy: [NAM/NỮ], [XX-XX] tuổi (Căn cứ: [Can/Thần/Quái])\n"
            "📍 Hướng: [HƯỚNG] (Căn cứ: Cung [X] = Quái [X])\n"
            "📏 Khoảng cách: [XXX-XXXm] (Căn cứ: Cung [X])\n"
            "🎨 Màu sắc: [MÀU] (Căn cứ: Hành [X])\n"
            "🔗 Quen/Lạ: [X%] (Căn cứ: [Thần])\n"
            "🔄 Lấy lại được: [X%] (Căn cứ: [Môn])\n\n"
            
            f"THÔNG TIN BỔ SUNG: {knowledge}\n"
        )
        return sys_prompt + f"\nUSER: {user_input}"

    def safe_get_text(self, response):
        try:
            if not response.candidates: return "⚠️"
            if response.text: return response.text
        except: pass
        return "⚠️"

    # --- BASIC AI CALLER WITH RETRY + FALLBACK + DEBUG LOGGING ---
    def _call_ai_raw(self, prompt):
        import random
        from datetime import datetime
        
        # DEBUG: Log start
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'='*50}")
        print(f"[STEP 1] 🚀 _call_ai_raw START @ {timestamp}")
        print(f"[STEP 1] 📝 Prompt length: {len(str(prompt))} chars")
        
        # CASCADE: CURRENT MODELS (Feb 2026) - FROM GOOGLE DOCS!
        # ⚠️ Gemini 1.5 is DEPRECATED - removed!
        cascade_models = [
            'gemini-2.0-flash',              # Free tier, fast
            'gemini-2.0-flash-001',          # Stable version
            'gemini-2.5-flash',              # Latest stable (may need paid)
            'gemini-2.5-flash-lite',         # Low cost alternative
        ]
        print(f"[STEP 2] 📋 Models to try: {cascade_models}")
        
        max_retries = 3
        base_delay = 1
        last_error = None
        error_log = []
        
        for model_idx, model_name in enumerate(cascade_models):
            print(f"\n[STEP 3.{model_idx+1}] 🔄 Trying model: {model_name}")
            
            for attempt in range(max_retries):
                try:
                    print(f"[STEP 4] ⏳ Attempt {attempt+1}/{max_retries} with {model_name}")
                    
                    import google.generativeai as genai
                    active_model = genai.GenerativeModel(model_name)
                    print(f"[STEP 5] ✅ Model instantiated: {model_name}")
                    
                    # Try with search tools first
                    try:
                        print(f"[STEP 6a] 🔍 Trying with google_search_retrieval...")
                        tools = [{"google_search_retrieval": {}}]
                        resp = active_model.generate_content(prompt, tools=tools)
                        print(f"[STEP 6a] ✅ Response with tools OK")
                    except Exception as tool_err:
                        print(f"[STEP 6b] ⚠️ Tools failed: {str(tool_err)[:30]}. Trying without...")
                        resp = active_model.generate_content(prompt)
                        print(f"[STEP 6b] ✅ Response without tools OK")
                    
                    if resp.text: 
                        print(f"[STEP 7] 🎉 SUCCESS! Response length: {len(resp.text)} chars")
                        print(f"{'='*50}\n")
                        return resp.text
                    else:
                        print(f"[STEP 7] ⚠️ Empty response from {model_name}")
                        
                except Exception as e:
                    err = str(e).lower()
                    err_short = err[:80]
                    error_log.append(f"{model_name}@attempt{attempt+1}: {err_short}")
                    print(f"[STEP ERROR] ❌ {model_name} failed: {err_short}")
                    
                    # LEAKED KEY - Stop immediately
                    if "leaked" in err or "403" in err or ("key" in err and "invalid" in err):
                        print(f"[STEP ERROR] 🛑 API KEY BLOCKED! Stopping all retries.")
                        return "🛑 LỖI API KEY: Key đã bị khóa. Vui lòng đổi Key mới!"
                    
                    # 404 - Model not found
                    if "404" in err or "not found" in err:
                        print(f"[STEP ERROR] 🔍 Model {model_name} NOT FOUND. Trying next...")
                        break  # Skip to next model
                    
                    # QUOTA - Retry with backoff
                    if "429" in err or "quota" in err:
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                            print(f"[STEP RETRY] ⏳ Rate limited. Waiting {delay:.1f}s...")
                            time.sleep(delay)
                            continue
                        else:
                            print(f"[STEP RETRY] ⚠️ {model_name} exhausted after {max_retries} retries")
                            last_error = e
                            break
                    
                    print(f"[STEP ERROR] ⚠️ Unknown error. Trying next model...")
                    last_error = e
                    break
        
        # FALLBACK TO FREE AI
        print(f"\n[STEP 8] 🆘 All Gemini models exhausted. Activating FREE AI backup...")
        try:
            if self.fallback_helper:
                print(f"[STEP 8a] 📞 Calling FreeAIHelper...")
                free_response = self.fallback_helper.answer_question(str(prompt)[:500])
                if free_response and len(str(free_response)) > 10:
                    print(f"[STEP 8a] ✅ Free AI responded: {len(str(free_response))} chars")
                    return f"[FREE AI BACKUP] {free_response}"
                else:
                    print(f"[STEP 8a] ⚠️ Free AI returned empty/short response")
            else:
                print(f"[STEP 8a] ❌ No fallback_helper available!")
        except Exception as fallback_err:
            print(f"[STEP 8b] ❌ Free AI failed: {fallback_err}")
        
        # LAST RESORT
        print(f"[STEP 9] 💀 ALL OPTIONS EXHAUSTED. Returning error message.")
        print(f"[STEP 9] 📋 Error log: {error_log}")
        print(f"{'='*50}\n")
        
        return (
            "⏳ **AI tạm thời quá tải**\n\n"
            "**Đã thử:**\n"
            f"✅ {len(cascade_models)} models Gemini\n"
            "✅ Free AI Backup\n\n"
            "**Giải pháp:**\n"
            "1. ⏰ Đợi 60 giây rồi thử lại\n"
            "2. 🔑 Dùng API key khác\n"
            f"\n_Debug Log: {'; '.join(error_log[-3:])}_"
        )
    
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
             return self._call_ai_raw(prompt)

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

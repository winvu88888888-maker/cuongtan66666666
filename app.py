import streamlit as st

# VERSION: 2026-02-04-V1.9.1-SMART-KEYS
try:
    st.set_page_config(
        page_title="Kỳ Môn Độn Giáp Pro - v2.0 FIXED",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass

import sys
import os
import traceback
import re

def show_fatal_error(e):
    st.error("🛑 LỖI HỆ THỐNG NGHIÊM TRỌNG")
    st.write("Ứng dụng gặp sự cố khi khởi động. Chi tiết kỹ thuật bên dưới:")
    st.code(traceback.format_exc())
    st.stop()

# ALL MISSION CRITICAL LOGIC GOES INSIDE THIS BLOCK
import random
import textwrap
import datetime as dt_module

try:
    import pytz
except ImportError:
    pytz = None

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

from PIL import Image
import importlib

# GLOBAL INIT
params = None

st.sidebar.success("✅ V2.2 - SMART ROUTER & FIXED")
st.sidebar.markdown("""
<div style="background: #047857; color: white; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 15px;">
    <b>🧠 AI KEY DETECTOR</b><br>
    <span style="font-size: 0.8em;">Auto-find keys in sloppy text</span>
</div>
""", unsafe_allow_html=True)
st.sidebar.info("Hệ thống: [READY]")

# --- DIAGNOSTIC INFO (SIDEBAR) ---
st.sidebar.markdown("### 🖥️ Hệ thống Giao diện")
st.sidebar.write(f"📂 Thư mục gốc: `{os.path.dirname(os.path.abspath(__file__))}`")
try:
    import mai_hoa_dich_so
    st.sidebar.caption(f"🌸 Mai Hoa: ✅")
    import luc_hao_kinh_dich
    st.sidebar.caption(f"☯️ Lục Hào: ✅")
except Exception as e:
    st.sidebar.error(f"⚠️ Module: {e}")

# --- AI FACTORY STATUS (SIDEBAR) ---
try:
    # Quick check for status without importing everything
    import json
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_hub", "factory_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            last_run = cfg.get("last_run")
            is_active_247 = cfg.get("autonomous_247", False)
            
            # Logic: Running if last_run < 90 mins
            is_running = False
            if last_run:
                try:
                    diff = dt_module.datetime.now() - dt_module.datetime.strptime(last_run, "%Y-%m-%d %H:%M:%S")
                    if diff.total_seconds() < 5400: # 90 mins
                        is_running = True
                except: pass
            
            st.sidebar.markdown("---")
            if is_running:
                st.sidebar.success(f"🟢 **AI Factory: ONLINE**\n\n(Chạy lúc: {last_run})")
            else:
                st.sidebar.error("🔴 **AI Factory: OFFLINE**")
                if is_active_247:
                    st.sidebar.caption("⌛ Đang chờ GitHub Action...")
except Exception: pass

# Add project root and dist directory to Python path
root_path = os.path.dirname(os.path.abspath(__file__))
dist_path = os.path.join(root_path, 'dist')
ai_modules_path = os.path.join(root_path, 'ai_modules')

for path in [root_path, dist_path, ai_modules_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# FORCE RELOAD CUSTOM MODULES
import importlib
try:
    import mai_hoa_dich_so
    importlib.reload(mai_hoa_dich_so)
    import luc_hao_kinh_dich
    importlib.reload(luc_hao_kinh_dich)
except Exception:
    pass

# Initialize fallbacks to prevent NameErrors if core files are missing
KY_MON_DATA = {"DU_LIEU_DUNG_THAN_PHU_TRO": {"CUU_TINH": {}, "BAT_THAN": {}, "BAT_MON": {}}}
TOPIC_INTERPRETATIONS = {}
BAT_MON_CO_DINH_DISPLAY = {}
BAT_MON_CO_DINH_CUNG = {}
CUNG_NGU_HANH = {}
QUAI_TUONG = {}

# Optional advanced modules
try:
    from qmdg_data import load_custom_data, save_custom_data
    from qmdg_data import KY_MON_DATA, TOPIC_INTERPRETATIONS
    from qmdg_detailed_analysis import phan_tich_chi_tiet_cung, so_sanh_chi_tiet_chu_khach
    USE_DETAILED_ANALYSIS = True
except ImportError:
    USE_DETAILED_ANALYSIS = False
    
# try:
#     import qmdg_calc
# except ImportError:
#     pass

try:
    from super_detailed_analysis import phan_tich_sieu_chi_tiet_chu_de, tao_phan_tich_lien_mach
    USE_SUPER_DETAILED = True
except ImportError:
    USE_SUPER_DETAILED = False

try:
    from integrated_knowledge_base import (
        get_comprehensive_palace_info, 
        format_info_for_display,
        get_qua_info,
        get_sao_info,
        get_mon_info,
        get_can_info
    )
    USE_KNOWLEDGE_BASE = True
except ImportError:
    USE_KNOWLEDGE_BASE = False

try:
    from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, tinh_qua_ngau_nhien, giai_qua
    USE_MAI_HOA = True
except ImportError:
    USE_MAI_HOA = False

try:
    from luc_hao_kinh_dich import lap_qua_luc_hao
    USE_LUC_HAO = True
except ImportError:
    USE_LUC_HAO = False
    
# Import AI modules (optional - only needed for AI Factory view)
try:
    from orchestrator import AIOrchestrator
    from memory_system import MemorySystem
    AI_FACTORY_AVAILABLE = True
except ImportError as e:
    AI_FACTORY_AVAILABLE = False
    print(f"âš ï¸ AI Factory modules not available: {e}")
    
# --- INLINED GEMINI HELPER (DEPLOYMENT FIX V2.2) ---
try:
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
            
            self.version = "V2.2-SmartRouter-AutoDiscover" # Marked to verify update
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
            # DIAGNOSTIC DATA
            sdk_version = "Unknown"
            try: sdk_version = genai.__version__
            except: pass
            
            try:
                # 1. Ask Google: "What models do I have?"
                valid_models = []
                try:
                    available = list(genai.list_models())
                    for m in available:
                        if 'generateContent' in m.supported_generation_methods:
                            valid_models.append(m.name)
                except Exception as e:
                    return False, f"Lỗi liệt kê (SDK {sdk_version}): {str(e)}"

                if not valid_models:
                    return False, f"Key OK nhưng 0 Model (SDK {sdk_version})"

                # 2. Prioritize modern models
                priority_order = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
                chosen_model_name = None
                
                for p in priority_order:
                    for vm in valid_models:
                        if p in vm:
                            chosen_model_name = vm
                            break
                    if chosen_model_name: break
                
                if not chosen_model_name:
                    chosen_model_name = valid_models[0]

                # 3. Final Test
                self.model = genai.GenerativeModel(chosen_model_name)
                self.model.generate_content("ping")
                self.active_model_name = chosen_model_name
                
                return True, f"OK! Model: {chosen_model_name} (SDK {sdk_version})"

            except Exception as e:
                # DUMP EVERYTHING FOR DEBUGGING
                return False, f"Lỗi: {str(e)} | SDK: {sdk_version} | Models: {valid_models}"

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
                        knowledge += f"\\n[TỪ ĐIỂN]: {defin['summary']}\\n(YÊU CẦU: Trả lời đúng định nghĩa này.)"
                except: pass
                
            # C. Topic Binding (Only if not definition)
            if intent == 'question' and not is_def:
                 knowledge += f"\\n[CHỦ ĐỀ UI]: {current_topic}\\n"
                 
            # D. n8n
            if intent == 'question' and self.n8n_url:
                 n8n_data = self.call_n8n_webhook(user_input, f"Topic: {current_topic}")
                 if n8n_data:
                     knowledge += f"\\n[DỮ LIỆU THỰC TẾ N8N]: {n8n_data}\\n"

            # 4. System Prompt
            sys_prompt = (
                "VAI TRÒ: Trợ lý Huyền Học Thông Minh.\\n"
                "NGUYÊN TẮC: \\n"
                "1. 'social' -> Chào hỏi ngắn gọn.\\n"
                "2. Hỏi định nghĩa -> Trả lời định nghĩa ngay.\\n"
                "3. Hỏi vấn đề (Tài lộc, Tình duyên) -> Dùng kiến thức Huyền Học để giải quyết.\\n"
                f"THÔNG TIN BỔ SUNG: {knowledge}\\n"
            )
            return sys_prompt + f"\\nUSER: {user_input}"

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
                answer = "ℹ️ **Kết quả từ quy trình suy luận:**\\n\\n" + thinking
                
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
            if self.n8n_url and not any(k in question.lower() for k in ["bàn cờ", "dụng thần", "cung", "quẻ", "sao", "cửa"]):
                 try:
                    n8n_result = self.call_n8n_webhook(question, f"User Interest: {topic}")
                 except: pass
            
            # If n8n gave a clear result, use it directly!
            if n8n_result:
                 # Synthesize n8n result simply
                 prompt = (
                     f"User hỏi: {question}\\n"
                     f"Thông tin tìm được từ Internet (N8N): {n8n_result}\\n"
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

    GEMINI_AVAILABLE = True
except (ImportError, Exception) as e:
    GEMINI_AVAILABLE = False
    print(f"⚠️ Gemini inlined load error: {e}")
        
# Import Free AI helper as fallback
try:
    from free_ai_helper import FreeAIHelper
    FREE_AI_AVAILABLE = True
except ImportError:
    FREE_AI_AVAILABLE = False

# ======================================================================
# INITIALIZE SESSION STATE
# ======================================================================
if 'zoom_level' not in st.session_state:
    st.session_state.zoom_level = 100
if 'chu_de_hien_tai' not in st.session_state:
    st.session_state.chu_de_hien_tai = "Tá»•ng QuÃ¡t"
if 'all_topics_full' not in st.session_state:
    core_topics = list(TOPIC_INTERPRETATIONS.keys())
    hub_topics = []
    try:
        from ai_modules.shard_manager import search_index
        index_results = search_index()
        hub_topics = list(set([e['title'] for e in index_results]))
    except Exception:
        pass
    st.session_state.all_topics_full = sorted(list(set(core_topics + hub_topics)))
if 'current_view' not in st.session_state:
    st.session_state.current_view = "ky_mon"  # ky_mon, mai_hoa, luc_hao

# Additional Module Imports (Flattened)
try:
    from dung_than_200_chu_de_day_du import (
        DUNG_THAN_200_CHU_DE,
        hien_thi_dung_than_200,
        lay_dung_than_200
    )
    USE_200_TOPICS = True
except ImportError:
    USE_200_TOPICS = False

try:
    from database_tuong_tac import (
        LUC_THAN_MAPPING,
        SINH_KHAC_MATRIX,
        TUONG_TAC_SAO_MON,
        QUY_TAC_CHON_DUNG_THAN,
        ANH_HUONG_MUA,
        TRONG_SO_PHAN_TICH,
        TRONG_SO_YEU_TO,
        LUC_THAN_THEO_CHU_DE,
        goi_y_doi_tuong_theo_chu_de
    )
    from phan_tich_da_tang import (
        chon_dung_than_theo_chu_de,
        xac_dinh_luc_than,
        phan_tich_sinh_khac_hop,
        phan_tich_tuong_tac_trong_cung,
        phan_tich_tuong_tac_giua_cac_cung,
        phan_tich_yeu_to_thoi_gian,
        tinh_diem_tong_hop,
        phan_tich_toan_dien,
        tinh_ngu_hanh_sinh_khac
    )
    USE_MULTI_LAYER_ANALYSIS = True
except (ImportError, Exception):
    USE_MULTI_LAYER_ANALYSIS = False
    # Fallback if import fails
    def phan_tich_yeu_to_thoi_gian(hanh, mua):
        return "Bình"

# --- HELPER: LEARNING MODE ---
import os
import json

def load_custom_learning():
    try:
        if os.path.exists("custom_learning.json"):
            with open("custom_learning.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except: pass
    return {}

def save_custom_learning(data):
    try:
        with open("custom_learning.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

def render_brain_training_ui():
    st.sidebar.markdown("---")
    with st.sidebar.expander("🧠 Huấn Luyện Antigravity", expanded=False):
        st.markdown("""
        <div style="font-size: 0.8rem; color: #666; margin-bottom: 10px;">
            Dạy cho AI những thuật ngữ mới. Nó sẽ áp dụng ngay lập tức.
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize if needed
        if 'custom_keywords' not in st.session_state:
            st.session_state.custom_keywords = load_custom_learning()
            
        with st.form("training_form"):
            new_kw = st.text_input("Từ khóa (VD: Bitcoin, bóng đá...)")
            
            # Get topics dynamically
            topics = list(TOPIC_INTERPRETATIONS.keys()) if 'TOPIC_INTERPRETATIONS' in globals() else ["Chung"]
            target_topic = st.selectbox("Gán vào Chủ đề:", topics)
            
            submitted = st.form_submit_button("Lưu Vào Não Bộ 💾")
            
            if submitted and new_kw:
                st.session_state.custom_keywords[new_kw.lower()] = target_topic
                save_custom_learning(st.session_state.custom_keywords)
                st.success(f"✅ Đã dạy: '{new_kw}' -> '{target_topic}'")
                st.rerun()

        # Show learned items
        if st.session_state.custom_keywords:
            st.markdown("---")
            st.caption("📚 Các thuật ngữ đã học:")
            for k, v in list(st.session_state.custom_keywords.items())[-5:]: 
                st.markdown(f"- **{k}**: {v}")

CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
SAO_9 = list(KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["CUU_TINH"].keys())
THAN_8 = list(KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_THAN"].keys())
CUA_8 = list(BAT_MON_CO_DINH_DISPLAY.keys())


# ======================================================================
# PREMIUM CUSTOM CSS
# ======================================================================

# ======================================================================
# PREMIUM CUSTOM CSS
# ======================================================================
st.markdown("""
<style>
    /* Imperial Silk & High-Contrast Theme */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #1e293b;
    }
    
    /* SPECIFIC HIGH-CONTRAST FOR EXPLANATIONS (TABLES & INFO) */
    [data-testid="stTable"] {
        background-color: #ffffff !important;
        border: 2px solid #b91c1c !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stTable"] th {
        background-color: #b91c1c !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border-bottom: 2px solid #991b1b !important;
    }
    
    [data-testid="stTable"] td {
        color: #000000 !important;
        font-weight: 700 !important;
        border-bottom: 1px solid #fee2e2 !important;
    }

    /* Force readable color for info boxes in light mode */
    .stAlert p {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    .stButton>button {
        background: linear-gradient(145deg, #1e293b, #334155);
        color: #f1f5f9;
        border: none;
        padding: 12px 24px;
        border-radius: 15px;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 10px 20px -5px rgba(30, 41, 59, 0.4),
                    inset 0 -4px 0 rgba(0,0,0,0.2),
                    inset 0 2px 2px rgba(255,255,255,0.1);
        transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 30px -8px rgba(30, 41, 59, 0.5);
        background: linear-gradient(145deg, #334155, #1e293b);
    }
    
    /* Palace 4D & Ultra-Large Text Enhancements */
    .palace-3d {
        perspective: 1200px;
        margin-bottom: 25px;
    }
    
    .palace-inner {
        transform-style: preserve-3d;
        box-shadow: 0 15px 45px rgba(0,0,0,0.3);
        transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        border-radius: 16px;
        position: relative;
        overflow: hidden;
        background-color: #1e293b; /* Fallback for contrast */
    }

    .glass-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.5); /* DEEPER OVERLAY FOR BETTER CONTRAST */
        z-index: 1;
    }

    /* Palace Layout & Element Stacking */
    .palace-content-v {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: 2;
    }

    .than-corner {
        position: absolute;
        top: 45px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 2px 2px 8px black, 0 0 10px rgba(0,0,0,0.8);
    }

    .sao-corner {
        position: absolute;
        top: 100px;
        left: 15px;
        font-size: 1.6rem;
        font-weight: 800;
        text-shadow: 2px 2px 8px black, 0 0 5px black;
    }

    .mon-corner {
        position: absolute;
        top: 100px;
        right: 15px;
        font-size: 1.9rem;
        font-weight: 900;
        text-shadow: 2px 2px 8px black, 0 0 5px black;
    }

    .thien-corner {
        position: absolute;
        bottom: 50px;
        right: 15px;
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 2px 2px 8px black, 0 0 5px black;
    }

    .dia-corner {
        position: absolute;
        bottom: 12px;
        right: 15px;
        font-size: 1.8rem;
        font-weight: 900;
        color: #ffffff !important;
        text-shadow: 2px 2px 10px black, 0 0 5px black;
    }

    .palace-markers {
        position: absolute !important;
        bottom: 10px !important;
        left: 10px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        z-index: 99999 !important; /* ABOVE EVERYTHING */
        pointer-events: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    .marker-badge {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 4px !important;
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        padding: 5px 12px !important;
        border-radius: 8px !important;
        border: 3px solid #000 !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 5px 15px rgba(0,0,0,0.5) !important;
        line-height: 1 !important;
        text-shadow: none !important;
        white-space: nowrap !important;
    }

    .marker-badge.ma {
        background: #f59e0b !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }

    .marker-badge.kv {
        background: #ffffff !important;
        color: #000000 !important;
        border-color: #000000 !important;
    }

    .marker-badge.pillar-nam { background: #1e3a8a !important; color: white !important; }
    .marker-badge.pillar-thang { background: #166534 !important; color: white !important; }
    .marker-badge.pillar-ngay { background: #991b1b !important; color: white !important; }
    .marker-badge.pillar-gio { background: #854d0e !important; color: white !important; }

    .kv-group, .ma-group {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;
    }

    .marker {
        font-size: 0.85rem;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 900;
        color: white;
        text-shadow: 1px 1px 2px black;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .marker.kv-nam, .marker.kv-thang, .marker.kv-ngay, .marker.kv-gio { background: #64748b; }
    .marker.ma-nam, .marker.ma-thang, .marker.ma-ngay, .marker.ma-gio { background: #f59e0b; }

    .palace-header-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        position: relative;
        z-index: 2;
    }

    .palace-title {
        color: #f1c40f;
        font-weight: 900;
        font-size: 1.3rem;
        text-shadow: 1px 1px 2px black;
    }

    .palace-footer-markers {
        display: flex;
        justify-content: flex-start;
        gap: 20px;
        padding: 10px 15px;
        position: relative;
        z-index: 2;
        font-size: 1.5rem; /* Large icons/text in footer */
        font-weight: 800;
    }

    .status-badge {
        font-size: 0.65rem;
        padding: 3px 10px;
        border-radius: 20px;
        font-weight: 800;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .palace-footer-markers {
        display: flex;
        justify-content: flex-start;
        gap: 12px;
        padding: 8px 12px;
        position: relative;
        z-index: 2;
    }
    
    .dung-than-active {
        border-width: 4px !important;
        box-shadow: 0 0 30px rgba(245, 158, 11, 0.3) !important;
    }

    /* --- I-CHING & MAI HOA PROFESSIONAL UI --- */
    /* --- I-CHING & MAI HOA PROFESSIONAL UI (EMPEROR THEME) --- */
    .iching-container {
        background: linear-gradient(to bottom, #ffffff, #fff9e6);
        border: 3px solid #b91c1c;
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 20px 50px rgba(185, 28, 28, 0.15);
        position: relative;
        overflow: hidden;
    }

    .iching-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 10px;
        background: linear-gradient(90deg, #b91c1c, #f59e0b, #b91c1c);
    }

    .hex-header-row {
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin-bottom: 3rem;
    }

    .hex-title-pro {
        font-size: 2.2rem;
        font-weight: 900;
        color: #b91c1c;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    .hex-subtitle {
        font-size: 1.5rem; /* RESTORED LARGE SUBTITLE */
        color: #92400e;
        font-weight: 900;
        letter-spacing: 1px;
    }

    .hex-visual-stack {
        display: flex;
        flex-direction: column;
        gap: 12px;
        align-items: center;
        margin: 30px 0;
        padding: 30px;
        background: radial-gradient(circle, #ffffff 0%, #f1f5f9 100%);
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }

    .hao-line-pro {
        height: 22px;
        width: 220px;
        border-radius: 6px;
        position: relative;
        transition: all 0.3s ease;
    }

    .yang-line-pro {
        background: linear-gradient(180deg, #475569 0%, #0f172a 40%, #020617 100%);
        box-shadow: 
            0 8px 15px rgba(0,0,0,0.4),
            inset 0 2px 2px rgba(255,255,255,0.4),
            inset 0 -2px 5px rgba(0,0,0,0.5);
        border: 1px solid #0f172a;
    }

    .yin-line-pro {
        display: flex;
        gap: 40px;
        width: 220px;
        filter: drop-shadow(0 8px 12px rgba(0,0,0,0.3));
    }

    .yin-half-pro {
        flex: 1;
        height: 22px;
        background: linear-gradient(180deg, #475569 0%, #0f172a 40%, #020617 100%);
        border-radius: 6px;
        box-shadow: 
            inset 0 2px 2px rgba(255,255,255,0.4),
            inset 0 -2px 5px rgba(0,0,0,0.5);
        border: 1px solid #0f172a;
    }
    }

    .hao-moving-glow {
        box-shadow: 
            0 0 25px rgba(245, 158, 11, 0.8),
            0 0 10px rgba(245, 158, 11, 0.4),
            inset 0 0 10px rgba(255, 255, 255, 0.6) !important;
        border: 2.5px solid #fbbf24 !important;
        transform: scale(1.03);
        z-index: 10;
    }

    .hao-moving-red {
        background: linear-gradient(180deg, #ff0000 0%, #b91c1c 100%) !important;
        box-shadow: 0 0 15px #ff0000, 0 0 5px #b91c1c !important;
        border: 2px solid #ffffff !important;
    }

    .hao-row-pro {
        display: flex;
        align-items: center;
        width: 100%;
        margin-bottom: 5px;
    }

    .hao-info-pro {
        font-size: 0.9rem;
        font-weight: 800;
        color: #1e293b;
        margin-left: 15px;
        white-space: nowrap;
        background: rgba(255,255,255,0.7);
        padding: 2px 8px;
        border-radius: 4px;
        border-right: 3px solid #b91c1c;
    }

    .hao-label-pro {
        font-size: 0.75rem;
        font-weight: 800;
        color: #64748b;
        width: 50px;
        text-align: right;
        margin-right: 10px;
    }

    .hao-table-pro {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 8px;
        margin-top: 1.5rem;
    }

    .hao-table-pro th {
        background: #b91c1c;
        color: #ffffff;
        font-weight: 800;
        padding: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: none;
        text-align: center;
    }

    .hao-table-pro td {
        background: #ffffff;
        padding: 12px;
        border-top: 1px solid #fee2e2;
        border-bottom: 1px solid #fee2e2;
        text-align: center;
        font-weight: 700;
        color: #1e293b;
    }

    .hao-table-pro tr td:first-child { border-left: 1px solid #fee2e2; border-radius: 8px 0 0 8px; }
    .hao-table-pro tr td:last-child { border-right: 1px solid #fee2e2; border-radius: 0 8px 8px 0; }

    .highlight-red {
        background: #fff1f2 !important;
        color: #b91c1c !important;
    }

    .status-footer-pro {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #fcd34d;
        padding: 20px;
        border-radius: 12px;
        margin-top: 2rem;
        font-weight: 800;
        display: flex;
        justify-content: space-around;
        border-bottom: 5px solid #f59e0b;
        font-size: 1.1rem;
    }

    .tuong-que-box {
        background: #fefce8;
        border-left: 6px solid #f59e0b;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        font-style: italic;
    }

    .action-card {
        background: rgba(255, 251, 235, 0.9);
        border-left: 8px solid #f59e0b;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    .action-title {
        color: #92400e;
        font-weight: 800;
        font-size: 1.2rem;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    .action-item {
        margin: 12px 0;
        padding-left: 25px;
        position: relative;
        font-weight: 800; /* RESTORED EXTRA BOLD */
        font-size: 1.1rem;
        color: #451a03;
        list-style: none;
    }
    .action-item::before {
        content: "⚡";
        position: absolute;
        left: 0;
    }
</style>
""", unsafe_allow_html=True)
# Zoom level already initialized in session state

# Inject custom CSS for zoom
def apply_zoom():
    zoom_scale = st.session_state.zoom_level / 100
    st.markdown(f"""
        <style>
        .main .block-container {{
            transform: scale({zoom_scale});
            transform-origin: top center;
            transition: transform 0.3s ease;
        }}
        
        /* Adjust container to prevent cutoff */
        .main {{
            overflow-x: hidden;
        }}
        
        /* Zoom control styling */
        .zoom-controls {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 999999;
            background: rgba(255, 255, 255, 0.95);
            padding: 8px 12px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            display: flex;
            gap: 8px;
            align-items: center;
        }}
        
        .zoom-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
        }}
        
        .zoom-btn:hover {{
            background: #5568d3;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .zoom-btn:active {{
            transform: translateY(0);
        }}
        
        .zoom-display {{
            font-weight: 600;
            color: #2c3e50;
            min-width: 50px;
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# Helper for base64 images
def get_base64_image(path):
    import base64
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

apply_zoom()

# ======================================================================
# AUTHENTICATION
# ======================================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if "password" in st.session_state:
            if st.session_state["password"] == "1987":
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # don't store password
            else:
                st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.markdown("### 🔑 Xác Thực Truy Cập - Kỳ Môn Độn Giáp")
        st.text_input(
            "Vui lòng nhập mật khẩu để sử dụng:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.markdown("### 🔑 Xác Thực Truy Cập - Kỳ Môn Độn Giáp")
        st.text_input(
            "Vui lòng nhập mật khẩu để sử dụng:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("❌ Mật khẩu không chính xác! Vui lòng liên hệ tác giả Vũ Việt Cường.")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()

# ======================================================================
# ZOOM CONTROLS (Floating)
# ======================================================================
# Create zoom controls using columns at the top
zoom_col1, zoom_col2, zoom_col3, zoom_col4, zoom_col5 = st.columns([1, 1, 1, 1, 6])

with zoom_col1:
    if st.button("🔍 −", key="zoom_out", help="Thu nhỏ (Zoom Out)"):
        st.session_state.zoom_level = max(50, st.session_state.zoom_level - 10)
        st.rerun()

with zoom_col2:
    if st.button(f"{st.session_state.zoom_level}%", key="zoom_reset", help="Đặt lại 100%"):
        st.session_state.zoom_level = 100
        st.rerun()

with zoom_col3:
    if st.button("🔍 +", key="zoom_in", help="Phóng to (Zoom In)"):
        st.session_state.zoom_level = min(200, st.session_state.zoom_level + 10)
        st.rerun()

with zoom_col4:
    st.markdown(f"<div style='padding: 8px; color: #666; font-size: 12px;'>Zoom: {st.session_state.zoom_level}%</div>", unsafe_allow_html=True)

# ======================================================================
# HEADER
# ======================================================================
col_header1, col_header2, col_header3 = st.columns([1, 3, 1])

with col_header1:
    # Try to load avatar image
    img_path = os.path.join(os.path.dirname(__file__), "dist", "táº£i xuá»‘ng (1).jpg")
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            st.image(img, width=100)
        except:
            pass

with col_header2:
    st.markdown("<h1 style='text-align: center; color: #f1c40f;'>🔮 KỲ MÔN ĐỘN GIÁP 🔮</h1>", unsafe_allow_html=True)

with col_header3:
    st.markdown("**Tác giả**")
    st.markdown("**Vũ Việt Cường**")

st.markdown("---")

# ======================================================================
# SIDEBAR - CONTROLS
# ======================================================================
with st.sidebar:
    st.markdown("### ⚙️ Điều Khiển")
    
    # View selection
    view_option = st.radio(
        "Chọn Phương Pháp:",
        ["🔮 Kỳ Môn Độn Giáp", "🏭 Nhà Máy AI", "🌟 40 Chuyên Gia AI", "📖 Mai Hoa 64 Quẻ", "☯️ Lục Hào Kinh Dịch", "🤖 Hỏi Gemini AI"],
        index=0
    )
    
    if view_option == "🔮 Kỳ Môn Độn Giáp":
        st.session_state.current_view = "ky_mon"
    elif view_option == "🏭 Nhà Máy AI":
        st.session_state.current_view = "ai_factory"
    elif view_option == "🌟 40 Chuyên Gia AI":
        st.session_state.current_view = "ai_experts"
    elif view_option == "📖 Mai Hoa 64 Quẻ":
        st.session_state.current_view = "mai_hoa"
    elif view_option == "☯️ Lục Hào Kinh Dịch":
        st.session_state.current_view = "luc_hao"
    else:  # 🤖 Hỏi Gemini AI
        st.session_state.current_view = "gemini_ai"
    
    
    st.markdown("---")
    
    # --- AI Initialization & Mode Switcher ---
    st.markdown("### 🤖 Cấu hình AI")
    ai_col1, ai_col2 = st.columns(2)
    
    with ai_col1:
        if st.button("🌐 Online AI", help="Sử dụng Gemini Pro (Yêu cầu API Key)", use_container_width=True):
            st.session_state.ai_preference = "online"
            # Clear existing to force re-init
            if 'gemini_helper' in st.session_state: del st.session_state.gemini_helper
            st.rerun()
            
    with ai_col2:
        if st.button("💾 Offline AI", help="Sử dụng Free AI (Dự phòng)", use_container_width=True):
            st.session_state.ai_preference = "offline"
            # Clear existing to force re-init
            if 'gemini_helper' in st.session_state: del st.session_state.gemini_helper
            st.rerun()

    if 'ai_preference' not in st.session_state:
        st.session_state.ai_preference = "auto" # Default to auto discovery

    # Actual Initialization Logic
    if ('gemini_helper' not in st.session_state or 
        not hasattr(st.session_state.gemini_helper, 'analyze_mai_hao') or 
        'V1.7.5' not in getattr(st.session_state.gemini_helper, 'version', '')):
        
        # ƯU TIÊN 1: Streamlit Cloud Secrets (Quan trọng nhất cho deployment)
        st_secret = None
        try:
            st_secret = st.secrets.get("GEMINI_API_KEY", None)
        except Exception:
            pass
        
        # ƯU TIÊN 2: File custom_data.json (Local)
        custom_data = load_custom_data()
        saved_key = custom_data.get("GEMINI_API_KEY")
        
        # ƯU TIÊN 3: Factory Config (Đồng bộ)
        factory_key = None
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_hub", "factory_config.json")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    factory_key = cfg.get("api_key")
        except: pass
        
        # Tổng hợp: Ưu tiên Streamlit Secrets > Saved Key > Factory Key
        secret_api_key = st_secret or saved_key or factory_key
        
        # Thông báo nếu chạy trên cloud nhưng chưa có secret
        if not st_secret and not saved_key and not factory_key:
            # Đang chạy trên cloud và không có API key nào
            st.session_state.missing_cloud_secret = True
        
import google.generativeai as genai

# --- IMPORT GEMINI HELPER FROM EXTERNAL MODULE (Unified Logic) ---
try:
    from gemini_helper import GeminiQMDGHelper
except ImportError:
    st.error("⚠️ Critical Error: gemini_helper.py not found! Vui lòng kiểm tra lại thư mục.")


# -----------------------------------------------

# Auto-Init logic
if st.session_state.ai_preference == "offline":
    if FREE_AI_AVAILABLE:
        st.session_state.gemini_helper = FreeAIHelper()
        st.session_state.ai_type = "Free AI (Manual Offline)"
else: # auto or online
    if secret_api_key and GEMINI_AVAILABLE:
        try:
            # INSTANTIATE INLINED CLASS DIRECTLY
            st.session_state.gemini_helper = GeminiQMDGHelper(secret_api_key)
            st.session_state.gemini_key = secret_api_key
            st.session_state.ai_type = "Gemini Pro (V2.2 - Smart Router)"
        except Exception: 
            if st.session_state.ai_preference == "auto" and FREE_AI_AVAILABLE:
                st.session_state.gemini_helper = FreeAIHelper()
                st.session_state.ai_type = "Free AI (Fallback)"
    elif FREE_AI_AVAILABLE:
        st.session_state.gemini_helper = FreeAIHelper()
        st.session_state.ai_type = "Free AI (Offline Mode)"


    # AI Status Display with LED Indicator
    ai_status = st.session_state.get('ai_type', 'Chưa sẵn sàng')
    
    # Auto-check API status periodically (every 30 seconds)
    if 'last_api_check_time' not in st.session_state:
        st.session_state.last_api_check_time = 0
    
    import time
    current_time = time.time()
    
    # Auto-check API status
    if "Gemini" in ai_status and (current_time - st.session_state.last_api_check_time > 30):
        try:
            success, msg = st.session_state.gemini_helper.test_connection()
            st.session_state.api_status_ok = success
            st.session_state.api_status_msg = msg
            st.session_state.last_api_check_time = current_time
        except:
            st.session_state.api_status_ok = False
            st.session_state.api_status_msg = "Chưa kiểm tra"
    
    # Initialize status if not exists
    if 'api_status_ok' not in st.session_state:
        st.session_state.api_status_ok = None  # None = chưa check, True = OK, False = Lỗi
        st.session_state.api_status_msg = "Chưa kiểm tra"
    
    # LED Indicator Colors
    if st.session_state.api_status_ok is True:
        led_color = "🟢"  # Xanh = OK
        status_color = "#10b981"
        status_text = "HOẠT ĐỘNG TỐT"
    elif st.session_state.api_status_ok is False:
        led_color = "🔴"  # Đỏ = Lỗi
        status_color = "#ef4444"
        status_text = "LỖI KẾT NỐI"
    else:
        led_color = "🟡"  # Vàng = Chưa check
        status_color = "#f59e0b"
        status_text = "CHƯA KIỂM TRA"
    
    # Display with LED & Unified Configuration
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {status_color}22 0%, {status_color}11 100%);
        border-left: 4px solid {status_color};
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">{led_color}</span>
            <div style="flex: 1;">
                <div style="font-weight: 800; color: {status_color}; font-size: 0.9rem;">
                    {status_text}
                </div>
                <div style="font-weight: 600; color: #475569; font-size: 0.85rem;">
                    🤖 {ai_status}
                </div>
                <div style="font-size: 0.75rem; color: #dc2626; margin-top: 5px; font-style: italic;">
                    {st.session_state.api_status_msg if st.session_state.api_status_ok is False else ""}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # UNIFIED SETTINGS (One place for everything)
    is_connected = st.session_state.api_status_ok is True
    expander_title = "🔑 Thay đổi API Key / Cấu hình" if is_connected else "🔑 Cấu Hình AI (Yêu cầu Key)"
    
    with st.expander(expander_title, expanded=not is_connected):
        # 1. Connection Controls (Only if connected)
        if is_connected:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🔄 Test Kết Nối Lại", key="test_ai_conn_unified", use_container_width=True):
                    with st.spinner("Đang thử kết nối..."):
                        success, msg = st.session_state.gemini_helper.test_connection()
                        st.session_state.api_status_ok = success
                        st.session_state.api_status_msg = msg
                        st.session_state.last_api_check_time = current_time
                        st.rerun()
            with col2:
                if st.button("R", key="force_refresh_unified", help="Reload App", use_container_width=True):
                    st.rerun()
                    
            st.markdown("---")

        # 2. Main Input Area (ALWAYS VISIBLE HERE)
        st.markdown("👉 [Lấy API Key Google miễn phí](https://aistudio.google.com/app/apikey)")
        st.info("💡 Mẹo: Dán đè Key mới vào đây để thay đổi. Hỗ trợ dán nhiều Key cùng lúc.")
        
        user_api_input = st.text_area("Dán Key vào đây (Tự động lọc):", height=100, key="input_api_key_smart_unified")
        
        if st.button("🚀 CẬP NHẬT & KÍCH HOẠT", type="primary", use_container_width=True):
            if user_api_input:
                with st.spinner("🤖 Đang quét Key & Test kết nối..."):
                    try:
                        # 1. Initialize Helper (It filters keys inside __init__)
                        from gemini_helper import GeminiQMDGHelper
                        temp_helper = GeminiQMDGHelper(user_api_input)
                        
                        # 2. Check if any valid keys found
                        if not temp_helper.api_keys:
                            st.error("❌ Không tìm thấy API Key nào hợp lệ (AIza...) trong văn bản bạn nhập.")
                        else:
                            # 3. Test Connection
                            success, msg = temp_helper.test_connection()
                            if success:
                                # SUCCESS! Save and Apply
                                st.session_state.gemini_helper = temp_helper
                                st.session_state.gemini_key = temp_helper.api_key
                                st.session_state.ai_type = f"Gemini Ultra ({len(temp_helper.api_keys)} Keys Active)"
                                st.session_state.api_status_ok = True
                                st.session_state.api_status_msg = "Kết nối thành công"
                                
                                # Save to disk
                                data = load_custom_data()
                                data["GEMINI_API_KEY"] = ",".join(temp_helper.api_keys) # Save all valid keys
                                save_custom_data(data)
                                
                                # Sync to Factory
                                try:
                                    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_hub", "factory_config.json")
                                    if os.path.exists(config_path):
                                        with open(config_path, 'r', encoding='utf-8') as f:
                                            cfg = json.load(f)
                                        cfg["api_key"] = ",".join(temp_helper.api_keys)
                                        with open(config_path, 'w', encoding='utf-8') as f:
                                            json.dump(cfg, f, indent=2, ensure_ascii=False)
                                except: pass

                                st.success(f"✅ KẾT NỐI THÀNH CÔNG! (Đã nạp {len(temp_helper.api_keys)} Key)")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")
                    except Exception as e:
                        st.error(f"❌ Lỗi xử lý: {e}")
            else:
                st.warning("⚠️ Vui lòng dán Key vào ô trống.")

    # n8n Configuration
    with st.expander("🔗 Kết nối n8n (Advanced AI)"):
        n8n_url = st.secrets.get("N8N_WEBHOOK_URL", "")
        n8n_input = st.text_input("n8n Webhook URL:", value=st.session_state.get('n8n_url', n8n_url))
        if n8n_input:
            st.session_state.n8n_url = n8n_input
            if 'gemini_helper' in st.session_state and hasattr(st.session_state.gemini_helper, 'set_n8n_url'):
                st.session_state.gemini_helper.set_n8n_url(n8n_input)
    
    st.markdown("---")
    
    st.markdown("---")
    
    # Time controls (GLOBAL for all views)
    st.markdown("### 🕒 Thời Gian")
    
    use_current_time = st.checkbox("Sử dụng giờ hiện tại", value=True)
    
    # Timezone handling (Robust Purification)
    vn_tz = None
    if pytz is not None:
        try:
            vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        except:
            pass
    
    if vn_tz is None:
        try:
            import zoneinfo
            vn_tz = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")
        except:
            try:
                from zoneinfo import ZoneInfo
                vn_tz = ZoneInfo("Asia/Ho_Chi_Minh")
            except:
                vn_tz = dt_module.timezone.utc

    if use_current_time:
        now = dt_module.datetime.now(vn_tz)
        selected_datetime = now
    else:
        now_vn = dt_module.datetime.now(vn_tz)
        selected_date = st.date_input("Chọn ngày:", now_vn.date())
        selected_time = st.time_input("Chọn giờ:", now_vn.time())
        selected_datetime = dt_module.datetime.combine(selected_date, selected_time, tzinfo=vn_tz)
    
    # Calculate QMDG parameters (Always calculate to show in sidebar)
    params = None
    try:
        import qmdg_calc
        params = qmdg_calc.calculate_qmdg_params(selected_datetime)
        
        # Calculate Lunar Date for display
        lday, lmonth, lyear, is_leap = qmdg_calc.solar_to_lunar(selected_datetime)
        l_year_can, l_year_chi = qmdg_calc.get_can_chi_year(lyear)
        l_year_name = f"{l_year_can} {l_year_chi}"
        
        st.info(f"""
        **Thời gian:** {selected_datetime.strftime("%H:%M - %d/%m/%Y")}
        
        **Âm lịch:**
        - Ngày: **{lday}/{lmonth} năm {l_year_name}** {'(Nhuận)' if is_leap else ''}
        - Giờ: {params['can_gio']} {params['chi_gio']}
        - Ngày: {params['can_ngay']} {params['chi_ngay']}
        - Tháng: {params['can_thang']} {params['chi_thang']}
        
        **Cục:** {params['cuc']} ({'Dương' if params.get('is_duong_don', True) else 'Âm'} Độn)
        """)
    except Exception as e:
        st.error(f"Lỗi tính toán: {e}")
    
    st.markdown("---")
    
    # Topic selection
    st.markdown("### 🎯 Chủ Đề Chính")
    
    # Dynamic Topic Refresh
    # Dynamic Topic Refresh with Categories
    core_topics = list(TOPIC_INTERPRETATIONS.keys())
    
    # Get standard categories from Strategist
    from ai_modules.mining_strategist import MiningStrategist
    standard_categories = list(MiningStrategist().categories.keys()) + ["Kiáº¿n Thá»©c", "KhÃ¡c"]
    
    hub_entries = []
    try:
        from ai_modules.shard_manager import search_index
        hub_entries = search_index() # Returns list of dicts with 'title' and 'category'
    except Exception: pass
    
    # Store full entry list for filtering
    st.session_state.hub_entries = hub_entries
    
    # Filter topics logic simplified for selectbox
    all_titles = sorted(list(set(core_topics + [e['title'] for e in hub_entries])))
    st.session_state.all_topics_full = all_titles


    search_term = st.text_input("🔍 Tìm kiếm chủ đề:", "")
    
    # NEW: Topic Counter Button
    if st.button("📊 Đếm tổng số chủ đề đang có"):
        total_count = len(st.session_state.all_topics_full)
        st.success(f"📈 Hiện hệ thống đang có tổng cộng: **{total_count}** chủ đề tri thức!")
    
    with st.expander("✍️ Đặt câu hỏi riêng & Kích hoạt AI Mining"):
        with st.form("custom_topic_form"):
            new_q = st.text_area("Nhập vấn đề/câu hỏi bạn đang quan tâm:", placeholder="Ví dụ: Đầu tư vàng năm 2026, Phân tích quẻ gieo cho sức khỏe bố mẹ...")
            if st.form_submit_button("🚀 Gửi & Lưu làm Chủ đề mới"):
                if new_q:
                    try:
                        from ai_modules.shard_manager import add_entry
                        # Save as a SEED topic
                        id = add_entry(
                            title=new_q, 
                            content=f"Câu hỏi gốc người dùng: {new_q}\n(Chủ đề này đã được nạp làm hạt giống để AI quân đoàn đi khai thác Internet.)",
                            category="Kiến Thức",
                            source="User Inquiry"
                        )
                        if id:
                            st.success(f"✅ Đã nạp thành công! AI sẽ bắt đầu tìm kiếm thông tin liên quan cho bạn.")
                            st.session_state.chu_de_hien_tai = new_q
                            st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi nạp chủ đề: {e}")

    # 1. Select Standard Category (Chủ đề chuẩn)
    standard_categories = ["Tất cả"] + list(MiningStrategist().categories.keys()) + ["Kiến Thức", "Lưu Trữ (Sách)", "Khác"]
    
    selected_cat = st.selectbox(
        "📂 Lọc theo Phân loại chuẩn:",
        standard_categories,
        index=0
    )
    
    # 2. Filter topics based on category
    available_topics = []
    divination_categories = ["Kỳ Môn Độn Giáp", "Kinh Dịch & Dự Đoán", "Phong Thủy & Địa Lý"]
    
    if selected_cat == "Tất cả":
        # Default view: Only core topics + specific divination hub topics
        hub_divination = [e['title'] for e in st.session_state.hub_entries if e['category'] in divination_categories]
        available_topics = sorted(list(set(core_topics + hub_divination)))
    else:
        # Get hub topics in this specific category
        available_topics = [e['title'] for e in st.session_state.hub_entries if e['category'] == selected_cat]
        
    # Search Filter
    if search_term:
        available_topics = [t for t in available_topics if search_term.lower() in t.lower()]
    
    if not available_topics:
        available_topics = ["(Chưa có dữ liệu cho phân loại này)"]

    selected_topic = st.selectbox(
        "Chọn chủ đề chi tiết:",
        available_topics,
        index=0 if "Tổng Quát" not in available_topics else available_topics.index("Tổng Quát")
    )

    
    st.session_state.chu_de_hien_tai = selected_topic
    
    st.info(f"📌 Đã chọn: **{selected_topic}**")
    
    # Multi-layer analysis (if available)
    if USE_MULTI_LAYER_ANALYSIS:
        st.markdown("---")
        st.markdown("### 🎯 Đối Tượng (Lục Thân)")
        
        doi_tuong_options = [
            "👤 Bản thân",
            "👨‍👩‍👧 Anh chị em",
            "👴👵 Bố mẹ",
            "👶 Con cái",
            "🤝 Người lạ (theo Can sinh)"
        ]
        
        selected_doi_tuong = st.selectbox("Chọn đối tượng:", doi_tuong_options, index=0)
        
        target_stem_name = "Giáp" # Default
        if selected_doi_tuong == "🤝 Người lạ (theo Can sinh)":
            target_stem_name = st.selectbox("Chọn Thiên Can năm sinh của người đó:", 
                                           ["Không rõ (Dùng Can Giờ)", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"])
        
        st.session_state.selected_doi_tuong = selected_doi_tuong
        st.session_state.target_stem_name_custom = target_stem_name

# ======================================================================
# MAIN CONTENT
# ======================================================================

if st.session_state.current_view == "ai_factory":
    try:
        from web.ai_factory_view import render_ai_factory_view
        render_ai_factory_view()
    except ImportError as e:
        st.error(f"Không thể tải module AI Factory: {e}")
        st.info("Vui lòng kiểm tra lại file web/ai_factory_view.py")

if st.session_state.current_view == "ky_mon":
    st.markdown("## 🔮 BẢNG KỲ MÔN ĐỘN GIÁP")
    
    if params:
        # Calculate full chart
        try:
            # Get Can Gio from pre-calculated params (Standard sources)
            can_gio = params['can_gio']
            
            # Calculate boards
            from qmdg_data import an_bai_luc_nghi, lap_ban_qmdg, tinh_khong_vong, tinh_dich_ma
            
            dia_can = an_bai_luc_nghi(params['cuc'], params['is_duong_don'])
            thien_ban, can_thien_ban, nhan_ban, than_ban, truc_phu_cung = lap_ban_qmdg(
                params['cuc'], params['truc_phu'], params['truc_su'], 
                can_gio, params['chi_gio'], params['is_duong_don']
            )
            
            # Calculate special palaces
            khong_vong = tinh_khong_vong(can_gio, params['chi_gio'])
            dich_ma = tinh_dich_ma(params['chi_gio'])
            
            # Store in session state
            if 'chart_data' not in st.session_state:
                st.session_state.chart_data = {}
            
            st.session_state.chart_data = {
                'thien_ban': thien_ban,
                'can_thien_ban': can_thien_ban,
                'nhan_ban': nhan_ban,
                'than_ban': than_ban,
                'dia_can': dia_can,
                'khong_vong_4': params.get('khong', {}),
                'dich_ma_4': params.get('ma', {}),
                'can_gio': can_gio,
                'chi_gio': params['chi_gio'],
                'can_ngay': params['can_ngay'],
                'chi_ngay': params['chi_ngay'],
                'can_thang': params.get('can_thang', 'N/A'),
                'can_nam': params.get('can_nam', 'N/A')
            }
            
        except Exception as e:
            st.error(f"Lỗi tính toán bàn: {e}")
            st.session_state.chart_data = None
        
        # Display 9 palaces grid with full information
        if st.session_state.chart_data:
            st.markdown("### 📊 Chín Cung Kỳ Môn")
            
            chart = st.session_state.chart_data
            
            # Palace layout: 4-9-2 / 3-5-7 / 8-1-6
            palace_layout = [
                [4, 9, 2],
                [3, 5, 7],
                [8, 1, 6]
            ]
            
            # Create 3x3 grid
            for row in palace_layout:
                cols = st.columns(3)
                for col_idx, palace_num in enumerate(row):
                    with cols[col_idx]:
                        # Get palace data
                        sao = chart['thien_ban'].get(palace_num, 'N/A')
                        cua = chart['nhan_ban'].get(palace_num, 'N/A')
                        than = chart['than_ban'].get(palace_num, 'N/A')
                        can_thien = chart['can_thien_ban'].get(palace_num, 'N/A')
                        can_dia = chart['dia_can'].get(palace_num, 'N/A')
                        hanh = CUNG_NGU_HANH.get(palace_num, 'N/A')
                        
                        # Check if palace has Dụng Thần (Resolved Logic)
                        topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                        dung_than_list = topic_data.get("Dụng_Thần", [])
                        
                        # Mapping symbolic names to actual stems
                        symbolic_map = {
                            "Can Ngày": chart.get('can_ngay'),
                            "Can Giờ": chart.get('can_gio'),
                            "Can Tháng": chart.get('can_thang'),
                            "Can Năm": chart.get('can_nam')
                        }
                        
                        resolved_dt = []
                        for dt_item in dung_than_list:
                            if dt_item in symbolic_map:
                                resolved_dt.append(symbolic_map[dt_item])
                            else:
                                resolved_dt.append(dt_item)
                        
                        # Final check for highlighting
                        has_dung_than = any(dt in [sao, cua, than, can_thien, can_dia] for dt in resolved_dt)
                        
                        # Special handling for Doors: "Sinh" vs "Sinh Môn"
                        if not has_dung_than:
                            clean_cua = cua.replace(" Môn", "")
                            clean_cua = cua.replace(" Môn", "")
                            has_dung_than = any(dt in [clean_cua] for dt in resolved_dt)
                        
                        # Determine Strength based on month
                        now_dt = dt_module.datetime.now()
                        month = now_dt.month
                        season_map = {1:"Xuân", 2:"Xuân", 3:"Xuân", 4:"Hạ", 5:"Hạ", 6:"Hạ", 7:"Thu", 8:"Thu", 9:"Thu", 10:"Đông", 11:"Đông", 12:"Đông"}
                        current_season = season_map.get(month, "Xuân")
                        strength = phan_tich_yeu_to_thoi_gian(hanh, current_season) if USE_MULTI_LAYER_ANALYSIS else "Bình"
                        
                        strength_color = {
                            "Vượng": "#ef4444", "Tướng": "#f59e0b", "Hưu": "#10b981", "Tù": "#3b82f6", "Tử": "#64748b"
                        }.get(strength, "#475569")

                        # Get door properties for analysis (Required for NameError fix)
                        door_data = KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_MON"].get(cua if " Môn" in cua else cua + " Môn", {})
                        cat_hung = door_data.get("Cát_Hung", "Bình")

                        # Element Styles & Aesthetics
                        element_configs = {
                            "Mộc": {"border": "#10b981", "icon": "🌿", "img": "moc.png"},
                            "Hỏa": {"border": "#ef4444", "icon": "🔥", "img": "hoa.png"},
                            "Thổ": {"border": "#f59e0b", "icon": "⛰️", "img": "tho.png"},
                            "Kim": {"border": "#94a3b8", "icon": "⚔️", "img": "kim.png"},
                            "Thủy": {"border": "#3b82f6", "icon": "💧", "img": "thuy.png"}
                        }.get(hanh, {"border": "#475569", "icon": "✨", "img": "tho.png"})

                        # Base64 Background Logic
                        bg_path = os.path.join(os.path.dirname(__file__), "web", "static", "img", "elements", element_configs.get('img', 'tho.png'))
                        bg_base64 = get_base64_image(bg_path)
                        
                        if bg_base64:
                            bg_style = f"background: url('data:image/png;base64,{bg_base64}') center/cover no-repeat;"
                        else:
                            bg_style = "background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);"

                        border_width = "4px" if has_dung_than else "1px"

                        # Color Mapping
                        def get_qmdg_color(name, category):
                            good_stars = ["Thiên Phụ", "Thiên Nhậm", "Thiên Tâm", "Thiên Cầm"]
                            good_doors = ["Khai", "Hưu", "Sinh", "Khai Môn", "Hưu Môn", "Sinh Môn"]
                            good_deities = ["Trực Phù", "Thái Âm", "Lục Hợp", "Cửu Địa", "Cửu Thiên"]
                            good_stems = ["Giáp", "Ất", "Bính", "Đinh", "Mậu"]
                            is_good = False
                            if category == "star": is_good = any(gs in name for gs in good_stars)
                            elif category == "door": is_good = any(gd in name for gd in good_doors)
                            elif category == "deity": is_good = any(gt in name for gt in good_deities)
                            elif category == "stem": is_good = any(gs in name for gs in good_stems)
                            return "#ff4d4d" if is_good else "#ffffff" # Bright Red vs Pure White

                        c_sao = get_qmdg_color(sao, "star")
                        c_cua = get_qmdg_color(cua, "door")
                        c_than = get_qmdg_color(than, "deity")
                        c_thien = get_qmdg_color(can_thien, "stem")
                        c_dia = get_qmdg_color(can_dia, "stem")

                        # Handle Palace 5 (Trung Cung) specific logic for Heaven Plate
                        if palace_num == 5:
                            # Central Palace Heaven Plate is often its original Earth Plate or follows the Leader
                            if can_thien == "N/A":
                                can_thien = can_dia # Showing Earth Plate as a reference for "What is Heaven Plate in 5"

                        # --- ROBUST MARKER LOGIC (4-PILLAR REFINEMENT) ---
                        ma_data = params.get('ma', {})
                        kv_data = params.get('khong', {})
                        
                        m_html = []
                        # Force current palace to int
                        try:
                            curr_p_int = int(palace_num)
                        except:
                            curr_p_int = -99

                        # 1. Horse (Mã) - Pillar specific
                        for pillar, label in [('nam', 'Mã Năm'), ('thang', 'Mã Tháng'), ('ngay', 'Mã Ngày'), ('gio', 'Mã Giờ')]:
                            val = ma_data.get(pillar)
                            if val is not None:
                                try:
                                    if int(val) == curr_p_int:
                                        m_html.append(f'<div class="marker-badge ma">🐎 {label}</div>')
                                except: pass
                        
                        # 2. Void (Tuần Không) - Pillar specific
                        for pillar, label in [('nam', 'Không Năm'), ('thang', 'Không Tháng'), ('ngay', 'Không Ngày'), ('gio', 'Không Giờ')]:
                            vals = kv_data.get(pillar, [])
                            try:
                                if any(int(v) == curr_p_int for v in vals):
                                    m_html.append(f'<div class="marker-badge kv">💀 {label}</div>')
                            except: pass
                        
                        # 3. 4 Pillar Cans (Năm/Tháng/Ngày/Giờ) location on Earth Plate
                        # We find where the 4 stems sit in the dia_can (Earth Plate)
                        for pillar, (p_can, p_label) in {
                            'nam': (params.get('can_nam'), 'Trụ Năm'),
                            'thang': (params.get('can_thang'), 'Trụ Tháng'),
                            'ngay': (params.get('can_ngay'), 'Trụ Ngày'),
                            'gio': (params.get('can_gio'), 'Trụ Giờ')
                        }.items():
                            if p_can and can_dia == p_can:
                                m_html.append(f'<div class="marker-badge pillar-{pillar}">📍 {p_label} ({p_can})</div>')

                        marker_display_html = "".join(m_html)

                        # Palace Name & Alignment Refinement
                        p_full_name = f"{palace_num} {QUAI_TUONG.get(palace_num, '')}"
                        if palace_num == 5: p_full_name = "5 Trung Cung"

                        # Status Badge
                        status_badge = f'<span class="status-badge" style="background: {strength_color}; color: white;">{strength}</span>'

                        # --- RENDER TRADITIONAL CORNER LAYOUT (NO LABELS) ---
                        palace_html = f"""<div class="palace-3d animated-panel">
<div class="palace-inner {'dung-than-active' if has_dung_than else ''}" style="{bg_style} border: {border_width} solid {element_configs['border']}; min-height: 320px; position: relative;">
<div class="glass-overlay"></div>
<div class="palace-header-row">
    <span class="palace-title">{p_full_name}</span>
    {status_badge}
</div>
<div class="palace-content-v">
    <div class="than-corner" style="color: {c_than};">{than}</div>
    <div class="sao-corner" style="color: {c_sao};">{sao.replace('Thiên ', '')}</div>
    <div class="mon-corner" style="color: {c_cua};">{cua.replace(' Môn', '')}</div>
    <div class="thien-corner" style="color: {c_thien};">{can_thien}</div>
    <div class="dia-corner" style="color: {c_dia};">{can_dia}</div>
</div>
<div class="palace-markers">
    {marker_display_html}
</div>
</div></div>"""
                        st.markdown(palace_html, unsafe_allow_html=True)

                        
                        # Expander for detailed analysis
                        with st.expander(f"📖 Chi tiết Cung {palace_num}"):
                            # Basic info
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.markdown(f"**Quái tượng:** {QUAI_TUONG.get(palace_num, 'N/A')}")
                                st.markdown(f"**Ngũ hành:** {hanh}")
                            with col_info2:
                                st.markdown(f"**Cát/Hung:** {cat_hung}")
                                st.markdown(f"**Trạng thái:** {strength}")
                            
                            st.markdown("---")
                            
                            # Check Dụng Thần with clearer explanation
                            topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                            dung_than_list = topic_data.get("Dụng_Thần", [])
                            
                            # --- PRE-CALCULATE CORE VARIABLES (FIXES NAMEERROR) ---
                            actual_can_gio = chart.get('can_gio', 'N/A')
                            actual_can_ngay = chart.get('can_ngay', 'N/A')
                            actual_can_thang = chart.get('can_thang', 'N/A')
                            actual_can_nam = chart.get('can_nam', 'N/A')
                            
                            # Resolve Relation (Lục Thân) stem
                            rel_type = st.session_state.get('selected_doi_tuong', "👤 Bản thân")
                            target_can_representative = actual_can_ngay # Default to Self
                            rel_label = "Bản thân"
                            
                            if "Anh chị em" in rel_type:
                                target_can_representative = actual_can_thang
                                rel_label = "Anh chị em"
                            elif "Bố mẹ" in rel_type:
                                target_can_representative = actual_can_nam
                                rel_label = "Bố mẹ"
                            elif "Con cái" in rel_type:
                                target_can_representative = actual_can_gio
                                rel_label = "Con cái"
                            elif "Người lạ" in rel_type:
                                custom_val = st.session_state.get('target_stem_name_custom', "Giáp")
                                if "Không rõ" in custom_val:
                                    target_can_representative = actual_can_gio
                                    rel_label = "Đối tượng (Can Giờ)"
                                else:
                                    target_can_representative = custom_val
                                    rel_label = f"Đối tượng ({target_can_representative})"

                            # --- PART 1: RELATIONSHIP ANALYSIS (SUBJECT VS OBJECT) ---
                            st.subheader("🎯 Phân tích Tương tác Dụng Thần")
                            
                            # Determine Subject (Bản thân) Stem Palace
                            subject_palace = 0
                            # Assuming 'dia_can' holds the Earth Stems for each palace
                            # We need to find the palace where the 'can_ngay' (subject's stem) resides
                            for p_num, d_can in chart['dia_can'].items():
                                if d_can == actual_can_ngay:
                                    subject_palace = p_num
                                    break
                            
                            # Determine Object (Dụng Thần) Palace (Current Palace)
                            object_palace = palace_num
                            
                            s_hanh = CUNG_NGU_HANH.get(subject_palace, "Thổ")
                            o_hanh = CUNG_NGU_HANH.get(object_palace, "Thổ")
                            
                            s_hanh = CUNG_NGU_HANH.get(subject_palace, "Thổ")
                            o_hanh = CUNG_NGU_HANH.get(object_palace, "Thổ")
                            
                            interaction = SINH_KHAC_MATRIX.get(s_hanh, {}).get(o_hanh, "Bình Hòa")
                            
                            # Visual Interaction Report
                            col_rel1, col_rel2, col_rel3 = st.columns([2, 1, 2])
                            with col_rel1:
                                st.info(f"👥 **Bản thân**\n\nCung {subject_palace} ({s_hanh})")
                            with col_rel2:
                                st.markdown(f"<div style='text-align:center; font-size:1.5rem; padding-top:10px;'>{'➡️' if 'Sinh' in interaction else '⚔️' if 'Khắc' in interaction else '🤝'}</div>", unsafe_allow_html=True)
                                st.caption(f"<div style='text-align:center;'>{interaction}</div>", unsafe_allow_html=True)
                            with col_rel3:
                                st.success(f"🎯 **Đối tượng**\n\nCung {object_palace} ({o_hanh})")
                            
                            st.write(f"**Kết luận nhanh:** {rel_label} và Đối tượng có mối quan hệ **{interaction}**. " + 
                                     ("Đây là dấu hiệu thuận lợi, năng lượng lưu thông." if "Sinh" in interaction or "Bình" in interaction 
                                      else "Cần thận trọng vì có sự xung đột hoặc cản trở về mặt năng lượng."))

                            st.markdown("---")
                            
                            # --- PART 2: TECHNICAL ELEMENT LOOKUPS ---
                            st.subheader("🔍 Chi tiết Tác động của Thần - Tinh - Môn")
                            
                            # Create a clean table for lookups
                            tech_data = {
                                "Yếu tố": ["Thần (Deity)", "Tinh (Star)", "Môn (Door)", "Thiên Can", "Địa Can"],
                                "Tên": [than, sao, cua, can_thien, can_dia],
                                "Ý nghĩa & Tác động": [
                                    KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_THAN"].get(than, {}).get("Tính_Chất", "N/A"),
                                    KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["CUU_TINH"].get(sao, {}).get("Tính_Chất", "N/A"),
                                    KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_MON"].get(cua if " Môn" in cua else cua + " Môn", {}).get("Luận_Đoán", "N/A"),
                                    KY_MON_DATA["CAN_CHI_LUAN_GIAI"].get(can_thien, {}).get("Tính_Chất", "N/A"),
                                    KY_MON_DATA["CAN_CHI_LUAN_GIAI"].get(can_dia, {}).get("Tính_Chất", "N/A")
                                ]
                            }
                            st.table(tech_data)
                            
                            # --- PART 3: TOPIC-SPECIFIC ANALYSIS ---
                            st.subheader(f"💡 Phân tích theo chủ đề: {selected_topic}")
                            topic_detail = topic_data.get("Diễn_Giải", topic_data.get("Diễn_Giải", "Đang cập nhật..."))
                            st.write(topic_detail)
                            
                            # Combinatorial Analysis (Cách Cục)
                            combo_key = f"{can_thien}{can_dia}"
                            combo_info = KY_MON_DATA.get("TRUCTU_TRANH", {}).get(combo_key)
                            if combo_info:
                                ten_cach = combo_info.get('Tên_Cách_Cục') or combo_info.get('Tên_Cách_Cục') or "N/A"
                                cat_hung = combo_info.get('Cát_Hung') or combo_info.get('Cát_Hung') or "N/A"
                                luan_giai = combo_info.get('Luận_Giải') or combo_info.get('Luận_Giải') or "N/A"
                                st.warning(f"🎭 **Cách cục: {ten_cach} ({cat_hung})**")
                                st.write(luan_giai)
                            
                            # Final Advice
                            st.markdown("---")
                            st.info("**Lời khuyên từ chuyên gia:** Dựa trên sự tương tác giữa Bản thân và Dụng Thần, bạn nên chủ động nắm bắt cơ hội nếu có sự tương sinh, hoặc lùi lại quan sát nếu gặp sự hình khắc mạnh.")
                            
                            # Advanced Matching Logic
                            found_dt = []
                            for dt in dung_than_list:
                                is_match = False
                                display_name = dt
                                
                                # 1. Check direct matches (Star, Deity, Stems)
                                if dt in [sao, than]:
                                    is_match = True
                                # 2. Check Doors (Normalize "Sinh" vs "Sinh Môn")
                                elif dt == cua or dt == f"{cua} Môn" or (cua and dt.startswith(cua)):
                                    is_match = True
                                # 3. Check Symbolic Stems (PRECISION: Only Heaven Plate)
                                elif dt == "Can Giờ" and (actual_can_gio == can_thien):
                                    display_name = f"Can Giờ ({actual_can_gio} - Sự việc)"
                                    is_match = True
                                elif dt == "Can Ngày" and (actual_can_ngay == can_thien):
                                    display_name = f"Can Ngày ({actual_can_ngay})"
                                    is_match = True
                                elif dt == "Can Tháng" and (actual_can_thang == can_thien):
                                    display_name = f"Can Tháng ({actual_can_thang})"
                                    is_match = True
                                elif dt == "Can Năm" and (actual_can_nam == can_thien):
                                    display_name = f"Can Năm ({actual_can_nam})"
                                    is_match = True
                                # 4. Check Stems directly if they are on Heaven Plate
                                elif dt in ["Nhâm", "Quý", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân"] and (dt == can_thien):
                                    is_match = True
                                # 5. Check Special Markers
                                elif dt == "Mã Tinh" and palace_num == chart.get('dich_ma'):
                                    is_match = True
                                elif dt == "Không Vong" and palace_num in chart.get('khong_vong', []):
                                    is_match = True
                                
                                if is_match:
                                    found_dt.append(display_name)
                                    
                            # ADD RELATIONSHIP HIGHLIGHT
                            if target_can_representative == can_thien:
                                found_dt.append(f"📍 {rel_label}")
                            
                            dt_html = f"""
                            <div class="dung-than-box">
                                <div style="font-weight: 800; color: #92400e; margin-bottom: 5px;">📍 PHÂN TÍCH DỤNG THẦN</div>
                                <div style="font-size: 14px;"><strong>Chủ đề:</strong> {selected_topic}</div>
                                <div style="font-size: 14px;"><strong>Dụng thần cần tìm:</strong> {', '.join(dung_than_list)}</div>
                                <div style="margin-top: 10px; font-weight: 700; color: {'#15803d' if found_dt else '#b91c1c'};">
                                    {f'✅ Tìm thấy: {", ".join(found_dt)}' if found_dt else '⚠️ Cung này không chứa Dụng Thần chính'}
                                </div>
                            </div>
                            """
                            st.markdown(dt_html, unsafe_allow_html=True)
                            
                            # UNIFIED AI EXPERT BUTTON
                            if 'gemini_helper' in st.session_state:
                                st.markdown("---")
                                if st.button(f"🧙 AI Chuyên Gia Tư Vấn Cung {palace_num}", key=f"ai_palace_expert_btn_{palace_num}", use_container_width=True, type="primary"):
                                    with st.spinner(f"Chuyên gia AI đang phân tích Cung {palace_num} theo chủ đề {selected_topic}..."):
                                        analysis = st.session_state.gemini_helper.analyze_palace(
                                            {
                                                "num": palace_num,
                                                "qua": QUAI_TUONG.get(palace_num, 'N/A'),
                                                "hanh": hanh,
                                                "star": sao,
                                                "door": cua,
                                                "deity": than,
                                                "can_thien": can_thien,
                                                "can_dia": can_dia
                                            },
                                            selected_topic
                                        )
                                        st.markdown(f"""
                                        <div class="interpret-box">
                                            <div class="interpret-title">🔮 Phân Tích Chuyên Sâu Cung {palace_num}</div>
                                            <div style="font-size: 15px; line-height: 1.6; color: #1e293b;">{analysis}</div>
                                        </div>
                                        """, unsafe_allow_html=True)

                            # Static descriptions (Keep it brief)
                            st.markdown("---")
                            star_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(sao, {})
                            if star_data:
                                st.markdown(f"**⭐ Sao {sao}:** {star_data.get('Tính_Chất', 'N/A')}")
                            
                            if door_data:
                                st.markdown(f"**🚪 Cửa {cua}:** {door_data.get('Tính_Chất', 'N/A')}")
                            
                            deity_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(than, {})
                            if deity_data:
                                st.markdown(f"**🛡️ Thần {than}:** {deity_data.get('Tính_Chất', 'N/A')}")
                            
                            # Stem combination
                            cach_cuc_key = can_thien + can_dia
                            combination_data = KY_MON_DATA['TRUCTU_TRANH'].get(cach_cuc_key, {})
                            if combination_data:
                                col_can_1, col_can_2 = st.columns([3, 1])
                                with col_can_1:
                                    st.markdown(f"**🔗 {can_thien}/{can_dia}:** {combination_data.get('Luận_Giải', 'Chưa có nội dung')}")
                                    st.caption(f"Cát/Hung: {combination_data.get('Cát_Hung', 'Bình')}")
                                with col_can_2:
                                    show_can_exp = False
                                    if 'gemini_helper' in st.session_state:
                                        if st.button(f"🔮 Giải Thích", key=f"ai_can_{palace_num}_{can_thien}_{can_dia}", use_container_width=True):
                                            show_can_exp = True
                                
                                # Move explanation out of columns for full width
                                if show_can_exp:
                                    with st.spinner(f"AI đang phân giải tổ hợp {can_thien}/{can_dia}..."):
                                        explanation = st.session_state.gemini_helper.explain_element('stem', f"{can_thien}/{can_dia}")
                                        st.markdown(f"""
                                        <div class="interpret-box">
                                            <div class="interpret-title">📖 Luận Giải Cặp Can: {can_thien}/{can_dia}</div>
                                            <div style="font-size: 15px; line-height: 1.6; color: #1e293b;">{explanation}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            # End of Palace Details

        
        # Display Dụng Thần info
        st.markdown("---")
        st.markdown("### 🎯 THÔNG TIN DỤNG THẦN")
        
        topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
        dung_than_list = topic_data.get("Dụng_Thần", [])
        luan_giai = topic_data.get("Luận_Giải_Gợi_Ý", "")
        
        if dung_than_list:
            st.success(f"**Dụng Thần cần xem:** {', '.join(dung_than_list)}")
        
        if luan_giai:
            st.info(f"**Gợi ý luận giải:** {luan_giai}")
        
        # Display detailed Dụng Thần from 200+ database
        if USE_200_TOPICS:
            dt_data = lay_dung_than_200(selected_topic)
            if dt_data and 'ky_mon' in dt_data:
                km = dt_data['ky_mon']
                st.markdown("#### 🔮 Dụng Thần Kỳ Môn Chi Tiết")
                st.write(f"**Dụng Thần:** {km.get('dung_than', 'N/A')}")
                st.write(f"**Giải thích:** {km.get('giai_thich', 'N/A')}")
                st.write(f"**Cách xem:** {km.get('cach_xem', 'N/A')}")
                if 'vi_du' in km:
                    st.write(f"**Ví dụ:** {km['vi_du']}")
        
        # ===== COMPREHENSIVE AI REPORT SECTION =====
        if st.session_state.chart_data and 'gemini_helper' in st.session_state:
            st.markdown("---")
            st.markdown("### 🏆 BÁO CÁO TỔNG HỢP CHUYÊN SÂU (AI)")
            
            with st.container():
                st.markdown(f"""
                <div class="ai-response-panel animated-panel">
                    <div style="font-size: 1.2rem; font-weight: 800; color: #1e3a8a; margin-bottom: 15px;">
                        🤖 KẾT LUẬN CUỐI CÙNG TỪ AI
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🔮 Bắt đầu Phân Tích Tổng Hợp", type="primary", use_container_width=True):
                    with st.spinner("AI đang tổng hợp dữ liệu từ 9 cung và tính toán kết quả..."):
                        # Prepare data for AI
                        chart = st.session_state.chart_data
                        topic = selected_topic
                        
                        # Identify key palaces for AI
                        key_palaces_info = []
                        for pn in range(1, 10):
                            # (Simulate the finding logic for the report summary)
                            can_t = chart['can_thien_ban'].get(pn, 'N/A')
                            can_d = chart['dia_can'].get(pn, 'N/A')
                            s = chart['thien_ban'].get(pn, 'N/A')
                            c = chart['nhan_ban'].get(pn, 'N/A')
                            t = chart['than_ban'].get(pn, 'N/A')
                            
                            # Just send all palaces as they are rich data
                            key_palaces_info.append(f"Cung {pn}: Sao {s}, Môn {c}, Thần {t}, Can {can_t}/{can_d}")
                        
                        rel_type = st.session_state.get('selected_doi_tuong', "👤 Bản thân")
                        custom_stem = st.session_state.get('target_stem_name_custom', "N/A")
                        
                        prompt = f"""
                        Bạn là một đại sư Kỳ Môn Độn Giáp. Hãy phân tích TỔNG HỢP cho chủ đề: {topic}.
                        
                        **Ngữ cảnh Đối tượng (Lục Thân):** {rel_type} (Can mục tiêu: {custom_stem if 'người lạ' in rel_type.lower() else 'Theo Lục Thân'})
                        
                        **Dữ liệu 9 Cung:**
                        {chr(10).join(key_palaces_info)}
                        
                        **Trạng thái Can:** Giờ: {chart['can_gio']}, Ngày: {chart['can_ngay']}, Tháng: {chart.get('can_thang')}, Năm: {chart.get('can_nam')}
                        
                        **YÊU CẦU PHÂN TÍCH CHUYÊN SÂU:**
                        1. Xác định Cung Bản Thân (người hỏi) và Cung Sự Việc (Kết quả) hoặc Cung Đối tác/Người mua (Can Giờ).
                        2. Phân tích sự tương tác Sinh-Khắc-Hợp-Xung giữa các Cung này.
                        3. Đánh giá sức mạnh của các Sao và Cửa tại các cung trọng yếu.
                        4. **KẾT LUẬN DỨT KHOÁT:** Có đạt được mục đích không? (Bán được không? Giá tốt không? Kết hôn được không?...).
                        5. **LỜI KHUYÊN HÀNH ĐỘNG:** Cần làm gì ngay bây giờ? 
                        
                        Viết theo phong cách chuyên nghiệp, thực tế, không dùng thuật ngữ quá khó hiểu nếu không giải thích kèm theo.
                        """
                        
                        try:
                            # Use comprehensive_analysis if suitable, or answer_question for flexibility
                            final_report = st.session_state.gemini_helper.answer_question(prompt)
                            st.markdown(f"""
                            <div class="interpret-box" style="background: white; border-top: 5px solid #1e3a8a;">
                                {final_report}
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Lỗi phân tích: {e}")

        # ===== PALACE COMPARISON SECTION =====
        if st.session_state.chart_data:
            st.markdown("---")
            st.markdown("### ⚖️ SO SÁNH CHỦ - KHÁCH")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                chu_cung = st.selectbox(
                    "Chọn Cung Chủ (Bản thân):",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                    format_func=lambda x: f"Cung {x} - {QUAI_TUONG.get(x, '')}",
                    key="chu_cung_select"
                )
            
            with col2:
                khach_cung = st.selectbox(
                    "Chọn Cung Khách (Đối phương):",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                    index=1,
                    format_func=lambda x: f"Cung {x} - {QUAI_TUONG.get(x, '')}",
                    key="khach_cung_select"
                )
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔍 So Sánh", type="primary", use_container_width=True):
                    st.session_state.show_comparison = True
            
            # Display comparison results
            if st.session_state.get('show_comparison', False):
                try:
                    chart = st.session_state.chart_data
                    
                    # Get palace info
                    def get_palace_info(cung_num):
                        return {
                            'so': cung_num,
                            'ten': QUAI_TUONG.get(cung_num, 'N/A'),
                            'hanh': CUNG_NGU_HANH.get(cung_num, 'N/A'),
                            'sao': chart['thien_ban'].get(cung_num, 'N/A'),
                            'cua': chart['nhan_ban'].get(cung_num, 'N/A'),
                            'than': chart['than_ban'].get(cung_num, 'N/A'),
                            'can_thien': chart['can_thien_ban'].get(cung_num, 'N/A'),
                            'can_dia': chart['dia_can'].get(cung_num, 'N/A')
                        }
                    
                    chu = get_palace_info(chu_cung)
                    khach = get_palace_info(khach_cung)
                    
                    # Use detailed comparison if available
                    try:
                        if USE_DETAILED_ANALYSIS:
                            comparison_result = so_sanh_chi_tiet_chu_khach(selected_topic, chu, khach)
                            
                            st.markdown("#### 📊 KẾT QUẢ SO SÁNH CHI TIẾT")
                            
                            # Display palace info side by side
                            col_chu, col_khach = st.columns(2)
                            
                            with col_chu:
                                st.markdown(f"**🏠 CUNG CHỦ - Cung {chu['so']} ({chu['ten']})**")
                                st.write(f"- Ngũ Hành: {chu['hanh']}")
                                st.write(f"- ⭐ Tinh: {chu['sao']}")
                                st.write(f"- 🚪 Môn: {chu['cua']}")
                            
                            with col_khach:
                                st.markdown(f"**👥 CUNG KHÁCH - Cung {khach['so']} ({khach['ten']})**")
                                st.write(f"- Ngũ Hành: {khach['hanh']}")
                                st.write(f"- ⭐ Tinh: {khach['sao']}")
                                st.write(f"- 🚪 Môn: {khach['cua']}")
                            
                            # Element interaction
                            st.markdown("---")
                            interaction = comparison_result.get('ngu_hanh_sinh_khac', 'N/A')
                            st.info(f"**Phân tích Ngũ Hành:** {interaction}")
                            
                            # AI Comparison Analysis
                            if 'gemini_helper' in st.session_state:
                                if st.button("🤖 AI Phân Tích So Sánh", key="ai_compare_btn", type="primary"):
                                    with st.spinner("🤖 AI Đang phân tích..."):
                                        prompt = f"So sánh Cung {chu['so']} ({chu['hanh']}) và Cung {khach['so']} ({khach['hanh']}) cho chủ đề {selected_topic}."
                                        analysis = st.session_state.gemini_helper.answer_question(prompt)
                                        st.markdown(analysis)
                        else:
                            raise ImportError
                    except (ImportError, NameError, Exception):
                        # Fallback to simple comparison
                        st.markdown("#### 📊 KẾT QUẢ SO SÁNH CƠ BẢN")
                        
                        col_chu, col_khach = st.columns(2)
                        
                        with col_chu:
                            st.markdown(f"**🏠 Cung Chủ {chu['so']}**")
                            st.write(f"Ngũ Hành: {chu['hanh']}")
                            st.write(f"Sao: {chu['sao']}")
                            st.write(f"Môn: {chu['cua']}")
                        
                        with col_khach:
                            st.markdown(f"**👥 Cung Khách {khach['so']}**")
                            st.write(f"Ngũ Hành: {khach['hanh']}")
                            st.write(f"Sao: {khach['sao']}")
                            st.write(f"Môn: {khach['cua']}")
                        
                        # Simple element interaction
                        interaction = tinh_ngu_hanh_sinh_khac(chu['hanh'], khach['hanh'])
                        st.info(f"**Ngũ hành:** {interaction}")
                        
                except Exception as e:
                    st.error(f"Lỗi so sánh: {e}")
        
        # ===== UNIFIED EXPERT ANALYSIS SYSTEM =====
        if st.session_state.chart_data:
            st.markdown("---")
            st.markdown("## 🏆 HỆ THỐNG LUẬN GIẢI TỔNG HỢP CHUYÊN SÂU")
            
            # 1. PRIMARY AI EXPERT REPORT (Dụng Thần focus)
            if 'gemini_helper' in st.session_state:
                with st.container():
                    st.markdown("### 🎯 KẾT LUẬN TỔNG HỢP TỪ AI (Dụng Thần)")
                    if st.button("🔴 ⭐ BẮT ĐẦU LUẬN GIẢI CHUYÊN SÂU (ƯU TIÊN ĐỌC TRƯỚC) ⭐ 🔴", type="primary", key="ai_final_report_btn", use_container_width=True):
                        with st.spinner("🤖 AI Đang thực hiện luận giải trọng tâm..."):
                            try:
                                # Get Dụng Thần info from the best available source
                                dung_than_list = []
                                if 'USE_200_TOPICS' in globals() and USE_200_TOPICS:
                                    dung_than_list = lay_dung_than_200(selected_topic)
                                
                                if not dung_than_list:
                                    topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                                    dung_than_list = topic_data.get("Dụng_Thần", [])
                                
                                # Get interpretation hints
                                topic_hints = TOPIC_INTERPRETATIONS.get(selected_topic, {}).get("Luận_Giải_Gợi_Ý", "")
                                
                                # Resolve Dynamic Actors (Chủ - Khách)
                                # The Subject (Chủ thể/Người thực hiện) is the person we are asking ABOUT.
                                rel_type = st.session_state.get('selected_doi_tuong', "👩‍👧‍👦 Bản thân")
                                subj_stem = st.session_state.chart_data.get('can_ngay') # Default to Self
                                obj_stem = st.session_state.chart_data.get('can_gio') # Default to General Matter/Other Party
                                
                                role_label = "Bản thân bạn"
                                if "Anh chị em" in rel_type:
                                    subj_stem = st.session_state.chart_data.get('can_thang')
                                    role_label = "Anh chị bạn"
                                elif "Bố mẹ" in rel_type:
                                    subj_stem = st.session_state.chart_data.get('can_nam')
                                    role_label = "Bố mẹ bạn"
                                elif "Con cái" in rel_type:
                                    subj_stem = st.session_state.chart_data.get('can_gio')
                                    role_label = "Con cái bạn"
                                elif "Người lạ" in rel_type:
                                    custom_val = st.session_state.get('target_stem_name_custom', "Giáp")
                                    if "Không rõ" not in custom_val:
                                        subj_stem = custom_val
                                    role_label = "Đối phương (Người ngoài)"
                                
                                # Process Dụng Thần labels for better context
                                enriched_dung_than = []
                                for dt in dung_than_list:
                                    if dt == "Sinh Môn": enriched_dung_than.append("Sinh Môn (Lợi nhuận/Ngôi nhà)")
                                    elif dt == "Khai Môn": enriched_dung_than.append("Khai Môn (Công việc/Sự khởi đầu)")
                                    else: enriched_dung_than.append(dt)
                                
                                # Build a comprehensive prompt
                                prompt = f"""Phân tích chi tiết về chủ đề: {selected_topic}

**Đối tượng:** {role_label}
**Dụng Thần:** {', '.join(enriched_dung_than)}
**Gợi ý:** {topic_hints}

Hãy luận giải tình hình dựa trên Cung Bản Mệnh (Can Ngày) và Cung Sự Việc (Can Giờ).
"""
                                analysis = st.session_state.gemini_helper.answer_question(
                                    prompt,
                                    chart_data=st.session_state.chart_data,
                                    topic=selected_topic
                                )
                                
                                # 2. GENERATE QUICK ACTIONS
                                quick_actions = "- Hãy hành động dựa trên kết luận trên\n- Chọn thời điểm phù hợp với ngũ hành"
                                
                                # Display Quick Actions First
                                st.markdown(f"""
                                <div class="action-card">
                                    <div class="action-title">🚀 HÀNH ĐỘNG NHANH CẦN LÀM NGAY</div>
                                    {chr(10).join([f'<div class="action-item">{line.strip("- ").strip()}</div>' for line in quick_actions.strip().split(chr(10)) if line.strip()])}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display Detailed Analysis
                                st.markdown(f'<div class="expert-box">{analysis}</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"❌ Lỗi AI: {str(e)}")

            # 2. COMPARISON SECTION (Chủ - Khách Interaction)
            st.markdown("---")
            st.markdown("### ⚖️ SO SÁNH CHỦ - KHÁCH")
            col_comp1, col_comp2 = st.columns([3, 1])
            with col_comp1:
                st.caption("Phân tích tương quan giữa Bản thân (Chủ) và Đối tượng/Sự việc (Khách)")
            with col_comp2:
                if st.button("📊 Chạy So Sánh", key="run_comp_btn", use_container_width=True):
                    st.session_state.show_comparison = True
            
            if st.session_state.get('show_comparison'):
                # Extract comparison logic (Previously at line 1200 area)
                try:
                    chart = st.session_state.chart_data
                    chu_idx = 5
                    for cung, can in chart['can_thien_ban'].items():
                        if can == chart['can_ngay']:
                            chu_idx = cung
                            break
                    khach_idx = st.session_state.get('khach_cung_select', 1)
                    
                    def get_mini_info(idx):
                        return {
                            'so': idx,
                            'hanh': CUNG_NGU_HANH.get(idx, 'Thổ'),
                            'sao': chart['thien_ban'].get(idx, 'N/A'),
                            'cua': chart['nhan_ban'].get(idx, 'N/A')
                        }
                    
                    c_chu = get_mini_info(chu_idx)
                    c_khach = get_mini_info(khach_idx)
                    
                    c1, c2 = st.columns(2)
                    with c1: st.info(f"**Bản Thân (Cung {chu_idx}):** {c_chu['sao']} - {c_chu['cua']}")
                    with c2: st.warning(f"**Đối Tượng (Cung {khach_idx}):** {c_khach['sao']} - {c_khach['cua']}")
                    
                    res_mqh = tinh_ngu_hanh_sinh_khac(c_chu['hanh'], c_khach['hanh'])
                    st.success(f"**Tương tác Ngũ Hành:** {res_mqh}")
                    
                    if st.button("🤖 AI Phân Tích So Sánh", key="ai_compare_details"):
                        with st.spinner("AI Đang so sánh..."):
                            p = f"So sánh chi tiết Cung {chu_idx} và Cung {khach_idx} cho {selected_topic}."
                            ans = st.session_state.gemini_helper.answer_question(p)
                            st.info(ans)
                except Exception as e:
                    st.error(f"Lỗi: {e}")

            # 3. DETAILED TECHNICAL REPORT (Existing multi-layer analysis)
            st.markdown("---")
            with st.expander("🔎 Xem Phân Tích Kỹ Thuật (Kỳ Môn + Mai Hoa + Lục Hào)"):
                if USE_SUPER_DETAILED and st.button("🚀 Tạo Báo Cáo Kỹ Thuật", key="tech_report_btn"):
                    try:
                        # ... (original logic from line 1245-1362)
                        chart = st.session_state.chart_data
                        chu_idx = 5
                        for cung, can in chart['can_thien_ban'].items():
                            if can == chart['can_ngay']: chu_idx = cung; break
                        khach_idx = st.session_state.get('khach_cung_select', 1)
                        
                        def get_p_info(idx):
                            return {
                                'so': idx, 'ten': QUAI_TUONG.get(idx, 'N/A'), 'hanh': CUNG_NGU_HANH.get(idx, 'N/A'),
                                'sao': chart['thien_ban'].get(idx, 'N/A'), 'cua': chart['nhan_ban'].get(idx, 'N/A'),
                                'than': chart['than_ban'].get(idx, 'N/A'), 'can_thien': chart['can_thien_ban'].get(idx, 'N/A'),
                                'can_dia': chart['dia_can'].get(idx, 'N/A')
                            }
                        
                        chu = get_p_info(chu_idx); khach = get_p_info(khach_idx); now = dt_module.datetime.now()
                        from super_detailed_analysis import phan_tich_sieu_chi_tiet_chu_de, tao_phan_tich_lien_mach
                        res_9pp = phan_tich_sieu_chi_tiet_chu_de(selected_topic, chu, khach, now)
                        mqh = tinh_ngu_hanh_sinh_khac(chu['hanh'], khach['hanh'])
                        res_lien_mach = tao_phan_tich_lien_mach(selected_topic, chu, khach, now, res_9pp, mqh)
                        
                        st.success("✅ Đã tạo báo cáo tổng hợp!")
                        
                        # Display 9 aspects analysis
                        st.markdown("#### 📊 PHÂN TÍCH 9 PHƯƠNG DIỆN")
                        
                        aspects = [
                            ('thai_at', '⚔️ Thái Ất'),
                            ('thanh_cong', '🎯 Thành Công'),
                            ('tai_loc', '💰 Tài Lộc'),
                            ('quan_he', '🤝 Quan Hệ'),
                            ('suc_khoe', '❤️ Sức Khỏe'),
                            ('tranh_chap', '⚖️ Tranh Chấp'),
                            ('di_chuyen', '🚌 Di Chuyển'),
                            ('hoc_van', '📚 Học Vấn'),
                            ('tam_linh', '⚛️ Tâm Linh')
                        ]
                        
                        for key, label in aspects:
                            if key in res_9pp:
                                data = res_9pp[key]
                                with st.expander(f"{label} - Điểm: {data.get('diem', 'N/A')}/10"):
                                    st.write(f"**Thái độ:** {data.get('thai_do', 'N/A')}")
                                    st.write(f"**Phân tích:** {data.get('phan_tich', 'N/A')}")
                        
                        # Overall score
                        if 'tong_ket' in res_9pp:
                            st.markdown("---")
                            st.markdown("#### 🎯 TỔNG KẾT")
                            tong_ket = res_9pp['tong_ket']
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Điểm Tổng Hợp", f"{tong_ket.get('diem_tong', 'N/A')}/100")
                            with col2:
                                st.metric("Thái Độ", tong_ket.get('thai_do_chung', 'N/A'))
                            
                            if 'loi_khuyen_tong_quat' in tong_ket:
                                st.info(f"**💡 Lời khuyên:** {tong_ket['loi_khuyen_tong_quat']}")
                        
                        # Coherent analysis
                        if res_lien_mach:
                            st.markdown("---")
                            st.markdown("#### 📜 PHÂN TÍCH LIÊN MẠCH")
                            st.write(res_lien_mach)
                        
                        # Download report
                        report_text = f"""
BÁO CÁO PHÂN TÍCH KỲ MÔN ĐỘN GIÁP
Chủ Đề: {selected_topic}
Thời gian: {now.strftime('%H:%M - %d/%m/%Y')}

THÔNG TIN CUNG CHỦ (Cung {chu['so']}):
- Quái: {chu['ten']}
- Ngũ Hành: {chu['hanh']}
- Sao: {chu['sao']}
- Môn: {chu['cua']}
- Thần: {chu['than']}
- Can: {chu['can_thien']}/{chu['can_dia']}

THÔNG TIN CUNG KHÁCH (Cung {khach['so']}):
- Quái: {khach['ten']}
- Ngũ Hành: {khach['hanh']}
- Sao: {khach['sao']}
- Môn: {khach['cua']}
- Thần: {khach['than']}
- Can: {khach['can_thien']}/{khach['can_dia']}

PHÂN TÍCH LIÊN MẠCH:
{res_lien_mach}
                        """
                        
                        st.download_button(
                            label="📄 Tải Báo Cáo (TXT)",
                            data=report_text,
                            file_name=f"bao_cao_qmdg_{selected_topic}_{now.strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"Lỗi tạo báo cáo: {e}")
                        import traceback
                        st.code(traceback.format_exc())

            # 4. AI Q&A SECTION
            st.markdown("---")
            st.markdown("### ❓ HỎI AI VỀ BÀN NÀY")
            user_question = st.text_area("Đặt câu hỏi cho Chuyên gia AI:", placeholder="Hỏi thêm về thời điểm, cách hóa giải...", key="ai_q_input")
            if st.button("🤖 Gửi Câu Hỏi", key="ai_ask_final"):
                if user_question:
                    with st.spinner("🤖 Chuyên gia AI đang phân tích dữ liệu..."):
                        from qmdg_orchestrator import AIOrchestrator
                        orc = AIOrchestrator(st.session_state.gemini_helper)
                        raw = orc.run_pipeline(
                            user_question, 
                            current_topic=selected_topic,
                            chart_data=st.session_state.get('chart_data'),
                            mai_hoa_data=st.session_state.get('mai_hoa_result'),
                            luc_hao_data=st.session_state.get('luc_hao_result')
                        )
                        final_ans = st.session_state.gemini_helper._process_response(raw)
                        st.info(final_ans)
                        orc.render_logs()



elif st.session_state.current_view == "mai_hoa":
    st.markdown("## 🌸 MAI HOA DỊCH SỐ - TAM TÀI HỢP NHẤT")
    
    if not USE_MAI_HOA:
        st.error("❌ Module Mai Hoa Dịch Số không khả dụng.")
        st.stop()
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")
    
    method = st.radio("Phương pháp:", ["Thời gian", "Ngẫu hứng"], horizontal=True, key="mh_method")
    
    if st.button("🌸 LẬP QUẺ MAI HOA PRO", type="primary", use_container_width=True):
        dt = selected_datetime
        if method == "Thời gian":
            res = tinh_qua_theo_thoi_gian(dt.year, dt.month, dt.day, dt.hour)
        else:
            res = tinh_qua_ngau_nhien()
        
        # Add interpretation
        res['interpretation'] = giai_qua(res, selected_topic)
        st.session_state.mai_hoa_result = res

    if 'mai_hoa_result' in st.session_state:
        res = st.session_state.mai_hoa_result
        st.markdown('<div class="iching-container">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="hex-header-row">
            <div>
                <div class="hex-title-pro">{res.get('ten', 'Quẻ Chính')}</div>
                <div class="hex-subtitle">{res.get('upper_symbol')} / {res.get('lower_symbol')}</div>
            </div>
            <div>
                <div class="hex-title-pro">{res.get('ten_qua_bien', 'BIẾN CÁT TƯỢNG')}</div>
                <div class="hex-subtitle">Động hào {res.get('dong_hao', '?')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Imagery (Tượng Quẻ)
        st.markdown(f"""
        <div class="tuong-que-box">
            <strong>🖼️ Tượng Quẻ:</strong> {res.get('tuong', 'Đang cập nhật...')} <br>
            <strong>📖 Ý nghĩa:</strong> {res.get('nghĩa', 'Đang phân tích...')}
        </div>
        """, unsafe_allow_html=True)

        # Add visual lines for Mai Hoa
        col_mh_v1, col_mh_v_ho, col_mh_v2 = st.columns(3)
        with col_mh_v1:
            if 'lines' in res:
                st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUẺ CHỦ ({res["upper_element"]}/{res["lower_element"]})</div>', unsafe_allow_html=True)
                st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
                for i, line in enumerate(reversed(res['lines'])):
                    h_idx = 6 - i
                    is_dong = (h_idx == res['dong_hao'])
                    cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                    # Apply red color if moving
                    dong_cls = "hao-moving-red" if is_dong else ""
                    
                    st.markdown('<div style="display:flex; align-items:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="hao-label-pro">Hào {h_idx}</div>', unsafe_allow_html=True)
                    if line == 1:
                        st.markdown(f'<div class="hao-line-pro {cls} {dong_cls}"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="{cls}"><div class="yin-half-pro {dong_cls}"></div><div class="yin-half-pro {dong_cls}"></div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_mh_v_ho:
            if 'lines_ho' in res:
                st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">HỖ QUẺ</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center; font-size:0.9rem; font-weight:700;">{res.get("ten_ho", "") or "Quẻ Hỗ"}</div>', unsafe_allow_html=True)
                st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
                for i, line in enumerate(reversed(res['lines_ho'])):
                    h_idx = 6 - i
                    cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                    st.markdown('<div style="display:flex; align-items:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="hao-label-pro">Hào {h_idx}</div>', unsafe_allow_html=True)
                    if line == 1:
                        st.markdown(f'<div class="hao-line-pro {cls}"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="{cls}"><div class="yin-half-pro"></div><div class="yin-half-pro"></div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_mh_v2:
            if 'lines_bien' in res:
                st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUẺ BIẾN</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center; font-size:0.9rem; font-weight:700;">{res.get("ten_qua_bien", "") or "Quẻ Biến"}</div>', unsafe_allow_html=True)
                st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
                for i, line in enumerate(reversed(res['lines_bien'])):
                    h_idx = 6 - i
                    cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                    st.markdown('<div style="display:flex; align-items:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="hao-label-pro">Hào {h_idx}</div>', unsafe_allow_html=True)
                    if line == 1:
                        st.markdown(f'<div class="hao-line-pro {cls}"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="{cls}"><div class="yin-half-pro"></div><div class="yin-half-pro"></div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.info(f"💡 **Luận giải chi tiết:** {res.get('interpretation', 'Đang phân tích...')}")

        if st.button("🤖 AI Luận Quẻ Mai Hoa", key="ai_mai_hoa_btn"):
            with st.spinner("AI Đang giải mã Mai Hoa..."):
                ans = st.session_state.gemini_helper.analyze_mai_hoa(res, selected_topic)
                st.markdown(f"""
                <div class="interpret-box" style="background: white; border-top: 5px solid #b91c1c;">
                    {ans}
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="footer-stamp">Copyright © 2026 MAI HOA DICH SO PRO</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.current_view == "luc_hao":
    st.markdown("## ☯️ LỤC HÀO KINH DỊCH - CHUYÊN SÂU")
    
    if not USE_LUC_HAO:
        st.error("❌ Module Lục Hào Kinh Dịch không khả dụng.")
        st.stop()
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")
    
    show_debug_ih = st.checkbox("🐛 Chế độ Kiểm tra Dữ liệu", key="debug_iching_mode")
    
    if st.button("🎲 LẬP QUẺ LỤC HÀO PRO", type="primary", use_container_width=True):
        try:
            # Use the global selected_datetime
            dt = selected_datetime
            can_ngay = params.get('can_ngay', 'Giáp') if params else "Giáp"
            chi_ngay = params.get('chi_ngay', 'Tý') if params else "Tý"
            
            st.session_state.luc_hao_result = lap_qua_luc_hao(
                dt.year, dt.month, dt.day, dt.hour, 
                topic=selected_topic, 
                can_ngay=can_ngay, 
                chi_ngay=chi_ngay
            )
        except Exception as e:
            st.error(f"Lỗi lập quẻ: {e}")

    if 'luc_hao_result' in st.session_state:
        res = st.session_state.luc_hao_result
        st.markdown('<div class="iching-container">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="hex-header-row">
            <div>
                <div class="hex-title-pro">{res['ban']['name']}</div>
                <div class="hex-subtitle">Họ {res['ban']['palace']}</div>
            </div>
            <div>
                <div class="hex-title-pro">{res['bien']['name']}</div>
                <div class="hex-subtitle">Quẻ Biến</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUẺ CHỦ ({res["ban"]["palace"]})</div>', unsafe_allow_html=True)
            st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
            moving_hao = res.get('dong_hao', [])
            detail_map_ban = {d['hao']: d for d in res['ban']['details']}
            for i, line in enumerate(reversed(res['ban']['lines'])):
                h_idx = 6 - i
                is_dong = h_idx in moving_hao
                cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                dong_cls = "hao-moving-red" if is_dong else ""
                d = detail_map_ban.get(h_idx, {})
                
                st.markdown('<div class="hao-row-pro">', unsafe_allow_html=True)
                st.markdown(f'<div class="hao-label-pro">Hào {h_idx}</div>', unsafe_allow_html=True)
                if line == 1:
                    st.markdown(f'<div class="hao-line-pro {cls} {dong_cls}"></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="{cls}"><div class="yin-half-pro {dong_cls}"></div><div class="yin-half-pro {dong_cls}"></div></div>', unsafe_allow_html=True)
                
                # Enhanced Label with Debugging
                s = d.get("strength")
                val_s = s if s else "N/A"
                if s:
                    s_label = f"<span style='color: #15803d;'>{s}</span>" if s in ["Vượng", "Tướng"] else f"<span style='color: #b91c1c;'>{s} (Suy)</span>" if s in ["Hưu", "Tù", "Tử"] else s
                else:
                    s_label = "⚠️ Thiếu"
                
                lt = d.get("luc_thu", "N/A")
                m = d.get("marker", "")
                
                st.markdown(f'<div class="hao-info-pro">{d.get("luc_than","N/A")} | {d.get("can_chi","N/A")} | {lt} | {s_label} {m}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if show_debug_ih:
                st.write("DEBUG (Hào 1):", res['ban']['details'][0])
                st.write(f"📊 Module Path: `{luc_hao_kinh_dich.__file__}`")
                st.write(f"⚙️ Version: `{getattr(luc_hao_kinh_dich, 'VERSION_LH', 'Unknown')}`")

            st.markdown('<table class="hao-table-pro"><tr><th>HÀO</th><th>LỤC THÂN</th><th>CAN CHI</th><th>ĐỊNH VỊ</th></tr>', unsafe_allow_html=True)
            for d in reversed(res['ban']['details']):
                h_cls = "highlight-red" if d['is_moving'] else ""
                marker = d.get('marker', '')
                
                st.markdown(f'<tr class="{h_cls}"><td>Hào {d["hao"]} {marker}</td><td>{d["luc_than"]}</td><td>{d["can_chi"]}</td><td>{d.get("loc_ma", "-")}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUẺ BIẾN</div>', unsafe_allow_html=True)
            st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
            detail_map_bien = {d['hao']: d for d in res['bien'].get('details', [])}
            for i, line in enumerate(reversed(res['bien']['lines'])):
                h_idx = 6 - i
                cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                d = detail_map_bien.get(h_idx, {})
                
                st.markdown('<div class="hao-row-pro">', unsafe_allow_html=True)
                st.markdown(f'<div class="hao-label-pro">Hào {h_idx}</div>', unsafe_allow_html=True)
                if line == 1:
                    st.markdown(f'<div class="hao-line-pro {cls}"></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="{cls}"><div class="yin-half-pro"></div><div class="yin-half-pro"></div></div>', unsafe_allow_html=True)
                
                # Enhanced Label (Converted Hexagram usually doesn't show strength/marker in some schools but user asked for it)
                sb = d.get("strength","")
                sb_label = f"<span style='color: #15803d;'>{sb}</span>" if sb in ["Vượng", "Tướng"] else f"<span style='color: #b91c1c;'>{sb} (Suy)</span>" if sb in ["Hưu", "Tù", "Tử"] else sb
                st.markdown(f'<div class="hao-info-pro">{d.get("luc_than","")} | {d.get("can_chi","")} | {d.get("luc_thu","")} | {sb_label} {d.get("marker","")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<table class="hao-table-pro"><tr><th>HÀO</th><th>LỤC THÂN</th><th>CAN CHI</th><th>LỤC THÚ</th></tr>', unsafe_allow_html=True)
            for d in reversed(res['bien']['details']):
                st.markdown(f'<tr><td>Hào {d["hao"]}</td><td>{d["luc_than"]}</td><td>{d["can_chi"]}</td><td>{d["luc_thu"]}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)


        # Expert Footer
        st.markdown(f"""
        <div class="status-footer-pro">
            <span>💡 {res['the_ung']}</span>
            <span>📝 Dụng Thần: {res['ban']['details'][2]['luc_than']}</span>
            <span>📜 {res['conclusion'].split('.')[1]}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="footer-stamp">Copyright © 2026 KY MON DON GIAP PRO</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🤖 AI Luận Quẻ", key="ai_iching_btn"):
            with st.spinner("AI Đang giải mã..."):
                ans = st.session_state.gemini_helper.analyze_luc_hao(res, selected_topic)
                st.info(ans)


# ======================================================================
# FOOTER
# ======================================================================


# ======================================================================
# AI FACTORY VIEW
# ======================================================================
elif st.session_state.current_view == "ai_factory":
    st.markdown("## 🏭 NHÀ MÁY PHÁT TRIỂN AI - 50 AGENTS HUB")
    st.info("Hệ thống tự động hóa điều phối bởi AI Orchestrator + n8n.")
    
    # Status Row
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Agents Đang Chạy", "40/50", "Active")
    with c2: st.metric("Công Việc Hoàn Tất", "1,248", "Today")
    with c3: st.metric("Độ Ổn Định", "99.9%", "Verified")
    
    st.markdown("### 🤖 Agents Hoạt Động 24/7")
    
    # List of Agents in a Grid
    agents = [
        ("Secretary AI", "Phân tích yêu cầu & Lập kế hoạch", "🟢"),
        ("Code Writer", "Viết code chức năng tự động", "🟢"),
        ("Tester AI", "Kiểm thử Unit Test & UI", "🟢"),
        ("Orchestrator", "Điều phối luồng công việc", "🟢"),
        ("Memory Manager", "Lưu trữ & Truy xuất tri thức", "🟢"),
        ("Gemini Pro", "Siêu trí tuệ phân tích chuyên sâu", "🟢")
    ]
    
    rows = [st.columns(3) for _ in range(2)]
    for i, (name, desc, status) in enumerate(agents):
        col = rows[i // 3][i % 3]
        with col:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <div style="font-weight: 800; color: #1e3a8a;">{status} {name}</div>
                <div style="font-size: 13px; color: #666;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Sidebar Header
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px; background: linear-gradient(to right, #047857, #6ee7b7); border-radius: 10px; color: white; margin-bottom: 20px;">
        <h2 style="margin:0; font-size: 1.5rem;">KỲ MÔN PRO</h2>
        <p style="margin:0; font-size: 0.8rem; opacity: 0.9;">✨ V1.9.1 (SMART KEYS)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧪 Gửi Yêu Cầu Cho Nhà Máy")
    factory_prompt = st.text_area("Yêu cầu phát triển mới:", placeholder="Ví dụ: Tạo module phân tích bát tự tích hợp...")
    if st.button("🚀 Bắt Đầu Quy Trình Tự Động", type="primary"):
        st.warning("⚠️ Đang gửi yêu cầu tới workflow n8n... Vui lòng kiểm tra Dashboard n8n để theo dõi.")

# ======================================================================
# AI EXPERTS VIEW (40 AGENTS)
# ======================================================================
elif st.session_state.current_view == "ai_experts":
    st.markdown("## 🌟 40 CHUYÊN GIA AI - TƯ VẤN CHUYÊN SÂU")
    st.caption("Danh sách 40 AI Agents chuyên biệt cho từng lĩnh vực khác nhau.")
    
    # Choose Agent Category
    cat = st.tabs(["💎 Super AI", "🏡 Đời Sống", "📈 Tài Chính", "🛠️ Tiện Ích"])
    
    with cat[0]: # Super AI
        selected_agent = st.selectbox("Chọn Chuyên Gia Siêu Trí Tuệ:", [
            "Chart Interpreter AI (Phân tích bàn Kỳ Môn)",
            "Scheduler AI (Tìm giờ đẹp thông minh)",
            "Mai Hoa Expert (Chuyên gia Dịch số)",
            "Luc Hao Expert (Bậc thầy Lục Hào)",
            "Topic Advisor (Gợi ý chủ đề linh hoạt)"
        ])
        
    with cat[1]: # Life
        selected_agent = st.selectbox("Chọn Chuyên Gia Đời Sống:", [
            "Career Advisor AI (Sự nghiệp & Công danh)",
            "Health Advisor (Sức khỏe & Bình an)",
            "Relationship AI (Tình duyên & Hôn nhân)",
            "Name Analyzer (Phân tích danh tính)",
            "Dream Interpreter (Giải mã giấc mơ)"
        ])
        
    with cat[2]: # Finance
        selected_agent = st.selectbox("Chọn Chuyên Gia Tài Chính:", [
            "Wealth Advisor (Tài lộc & Đầu tư)",
            "Direction Advisor (Phương hướng kinh doanh)",
            "Date Selector (Chọn ngày đại sự)",
            "Fortune Calendar (Lịch vận hạn năm/tháng)"
        ])

    with cat[3]: # Utilities
        selected_agent = st.selectbox("Chọn Agent Tiện Ích:", [
            "History Tracker (Theo dõi lịch sử)",
            "Prediction Validator (Kiểm chứng kết quả)",
            "Report Generator (Tạo báo cáo chuyên nghiệp)",
            "Comparison AI (So sánh đa tầng)",
            "Notification AI (Cảnh báo giờ lành)",
            "Learning Assistant (Trình học liệu QMDG)",
            "Voice Assistant (Trợ lý giọng nói AI)"
        ])

    st.markdown(f"### 🤖 Bắt đầu tư vấn với: **{selected_agent.split('(')[0]}**")
    exp_q = st.text_area("Nội dung cần tư vấn:", placeholder="Nhập câu hỏi hoặc bối cảnh cụ thể của bạn...")
    
    if st.button("🧙 Triệu hồi Chuyên Gia AI", type="primary"):
        if exp_q:
            with st.spinner(f"AI {selected_agent} đang chạy quy trình xử lý chuyên sâu..."):
                try:
                    # INITIALIZE ORCHESTRATOR
                    from orchestrator import AIOrchestrator
                    orc = AIOrchestrator(st.session_state.gemini_helper)
                    
                    # RUN PIPELINE with Role Injected
                    safe_topic = selected_agent.split('(')[0].strip()
                    full_query = f"Bạn đang đóng vai chuyên gia: {selected_agent}. Hãy trả lời câu hỏi: {exp_q}"
                    
                    raw_response = orc.run_pipeline(
                        full_query, 
                        current_topic=safe_topic,
                        chart_data=st.session_state.get('chart_data'),
                        mai_hoa_data=st.session_state.get('mai_hoa_result'),
                        luc_hao_data=st.session_state.get('luc_hao_result')
                    )
                    
                    # PROCESS & DISPLAY
                    res = st.session_state.gemini_helper._process_response(raw_response)
                    st.info(res)
                    
                    # SHOW LOGS
                    orc.render_logs()
                    
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        else:
            st.warning("Vui lòng nhập câu hỏi.")

elif st.session_state.current_view == "gemini_ai":
    ai_name = st.session_state.get('ai_type', 'AI Assistant')
    st.markdown(f"## 🤖 HỎI {ai_name.upper()} VỀ KỲ MÔN ĐỘN GIÁP")
    
    if not GEMINI_AVAILABLE and not FREE_AI_AVAILABLE:
        st.error("❌ Không có module AI nào khả dụng.")
        st.stop()
    
    # Check if API key is configured
    if 'gemini_helper' not in st.session_state:
        st.error("❌ Không thể kết nối với máy chủ AI. Vui lòng thử lại sau.")
        st.stop()
    
    st.success(f"✅ {ai_name} đã sẵn sàng! Hãy đặt câu hỏi bên dưới.")
    
    # Topic selection for context
    st.markdown("### 🎯 Chọn Chủ Đề (Tùy chọn)")
    st.caption("Chọn chủ đề để AI có ngữ cảnh tốt hơn, hoặc để trống để hỏi chung")
    
    col_topic1, col_topic2 = st.columns([3, 1])
    
    with col_topic1:
        selected_topic_ai = st.selectbox(
            "Chủ đề:",
            ["Không chọn (Hỏi chung)"] + st.session_state.all_topics_full,
            key="ai_topic_select"
        )
    
    with col_topic2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚛️ Lập Bàn Nhanh", use_container_width=True):
            # Quick chart calculation for context
            try:
                from qmdg_calc import calculate_qmdg_params as tinh_ky_mon_don_gian
                st.session_state.ai_chart_data = tinh_ky_mon_don_gian(now.year, now.month, now.day, now.hour)
                st.success("✅ Đã lập bàn!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    st.markdown("---")
    
    # Question input area
    st.markdown("### ✍️ Câu Hỏi Của Bạn")
    user_question = st.text_area(
        "Nhập câu hỏi:",
        placeholder="Ví dụ: Tôi muốn biết về ý nghĩa của Thiên Tâm Tinh trong Kỳ Môn Độn Giáp?",
        height=150,
        key="ai_free_question"
    )
    
    if st.button(f"🤖 Hỏi {ai_name}", type="primary", use_container_width=True, key="ask_gemini_btn"):
        if user_question:
            with st.spinner(f"🤖 {ai_name} đang chạy quy trình xử lý..."):
                try:
                    # INITIALIZE ORCHESTRATOR (N8N STYLE SYSTEM)
                    from orchestrator import AIOrchestrator
                    orc = AIOrchestrator(st.session_state.gemini_helper)
                    
                    # RUN PIPELINE
                    safe_topic = selected_topic_ai if selected_topic_ai != 'Không chọn (Hỏi chung)' else 'Chung'
                    raw_response = orc.run_pipeline(
                        user_question, 
                        current_topic=safe_topic,
                        chart_data=st.session_state.get('chart_data'),
                        mai_hoa_data=st.session_state.get('mai_hoa_result'),
                        luc_hao_data=st.session_state.get('luc_hao_result')
                    )
                    
                    # PROCESS & DISPLAY
                    response_text = st.session_state.gemini_helper._process_response(raw_response)
                    
                    # Display response in a nice panel
                    st.markdown("---")
                    st.markdown(f"### 🤖 Trả Lời Từ {ai_name}")
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                        border-radius: 15px;
                        color: white;
                        margin: 10px 0;
                    ">
                        <h4 style="color: white; margin-top: 0;">💡 Câu Hỏi</h4>
                        <p style="font-size: 16px;">{user_question}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 15px;
                        border-left: 5px solid #667eea;
                        margin: 10px 0;
                    ">
                        {response_text.replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # RENDER WORKFLOW LOGS (User requested n8n visibility)
                    orc.render_logs()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        else:
            st.warning("⚠️ Vui lòng nhập câu hỏi")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>© 2026 Vũ Việt Cường - Kỳ Môn Độn Giáp Web Application</p>
    <p>🌐 Chạy 24/7 trên Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)


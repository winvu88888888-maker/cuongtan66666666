import streamlit as st

# ═══ PHIÊN BẢN — CHỈ SỬA Ở ĐÂY, TỰ ĐỘNG CẬP NHẬT TOÀN BỘ APP ═══
APP_VERSION = "V114.0"
APP_VERSION_FULL = f"{APP_VERSION} — THIÊN CƠ ĐẠI SƯ (Pháp Độc Tượng Vạn Vật Loại Tượng 6 Tầng ⛰️ + Tích Hợp Kho Tử Vi Thiên Kỷ 56.6GB GitHub 🔯 + Hội Tụ 6 Tầng Số 🔢)"
# ═══════════════════════════════════════════════════════════════════════
try:
    st.set_page_config(
        page_title=f"🔮 Kỳ Môn AI {APP_VERSION}",
    page_icon="☯️",
    layout="wide",
    initial_sidebar_state="expanded"
)
except Exception:
    pass

import sys
import os
import traceback
import re

# V114.0: Tự động Hot-Reload toàn bộ module Python trên Streamlit Cloud ngay khi có bản cập nhật mới
_CODE_BUILD_VERSION = "V114.0"
import importlib as _imp_hot
if getattr(sys, "_qmdg_loaded_build_version", None) != _CODE_BUILD_VERSION:
    for _m_name in [
        "qmdg_calc",
        "qmdg_data",
        "mai_hoa_dich_so",
        "luc_hao_kinh_dich",
        "dai_luc_nham",
        "thai_at_than_so",
        "question_parser",
        "dual_ai_agents",
        "interaction_diagrams",
        "ung_ky_engine",
        "world_class_methods",
        "offline_brain",
        "omniscient_prophecy",
        "ai_modules.luc_hao_expert_ai", "luc_hao_expert_ai",
        "ai_modules.mai_hoa_expert_ai", "mai_hoa_expert_ai",
        "ai_modules.relationship_ai", "relationship_ai",
        "ai_modules.wealth_advisor_ai", "wealth_advisor_ai",
        "ai_modules.career_advisor_ai", "career_advisor_ai",
        "ai_modules.health_advisor_ai", "health_advisor_ai",
        "ai_modules.chart_interpreter_ai", "chart_interpreter_ai",
        "gemini_helper",
        "free_ai_helper",
    ]:
        if _m_name in sys.modules and sys.modules[_m_name] is not None:
            try:
                _imp_hot.reload(sys.modules[_m_name])
            except Exception:
                pass
    sys._qmdg_loaded_build_version = _CODE_BUILD_VERSION

try:
    import free_ai_helper as _fah_mod
except Exception:
    pass

try:
    if st.session_state.get("_session_build_version") != _CODE_BUILD_VERSION:
        for _stale_k in ["_cached_free_ai_helper", "gemini_helper", "ai_orchestrator", "_qa_fast_cache", "master_qa_last_result"]:
            st.session_state.pop(_stale_k, None)
        st.session_state["_session_build_version"] = _CODE_BUILD_VERSION
except Exception:
    pass

import extra_streamlit_components as stx
# REMOVED: st_autorefresh was causing full page rerun every 60s, wiping AI analysis data
# from streamlit_autorefresh import st_autorefresh

# Initialize CookieManager without cache to avoid CachedWidgetWarning
cookie_manager = stx.CookieManager(key="cookie_mgr")
# REMOVED: st_autorefresh(interval=60000, key="auto_time_refresh") — was deleting AI results every 60s

def show_fatal_error(e):
    st.error("🛑 LỖI HỆ THỐNG NGHIÊM TRỌNG")
    st.write("Ứng dụng gặp sự cố khi khởi động. Chi tiết kỹ thuật bên dưới:")
    st.code(traceback.format_exc())
    st.stop()

# ALL MISSION CRITICAL LOGIC GOES INSIDE THIS BLOCK
import random
import textwrap
import datetime as dt_module
import time
import json

try:
    import requests
except ImportError:
    requests = None

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

# Banner removed by user request

st.sidebar.info("Hệ thống: [READY]")

# --- DIAGNOSTIC INFO (SIDEBAR) ---
st.sidebar.markdown("### 🖥️ Hệ thống Giao diện")

# --- ZOOM CONTROL ---
if 'zoom_level' not in st.session_state: st.session_state.zoom_level = 100
zoom = st.sidebar.slider("🔍 Phóng to / Thu nhỏ (%)", 50, 150, st.session_state.zoom_level, 10, key="zoom_slider")
st.session_state.zoom_level = zoom

# Dynamic CSS for Zoom
st.markdown(f"""
<style>
    /* V40.9: EXACT FIX — ẩn text "keyboard_arrow_right" bên trong summary */
    /* Element nằm sâu: summary > span > span > span — cần catch ALL */
    [data-testid="stExpander"] summary span {{
        font-size: 0 !important;
        color: transparent !important;
        overflow: hidden !important;
    }}
    /* Giữ lại text label của expander — chỉ span chứa title */
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary p span {{
        font-size: inherit !important;
        color: inherit !important;
    }}
    /* Thay icon bằng Unicode arrow */
    [data-testid="stExpander"] summary > span:first-child {{
        width: 20px !important;
        height: 20px !important;
        display: inline-block !important;
        position: relative !important;
    }}
    [data-testid="stExpander"] summary > span:first-child::before {{
        content: "▸" !important;
        font-size: 16px !important;
        color: #94a3b8 !important;
    }}
    [data-testid="stExpander"] details[open] summary > span:first-child::before,
    details[open] > summary > span:first-child::before {{
        content: "▾" !important;
    }}
    
    /* Sidebar collapse/expand button */  
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] span {{
        font-size: 0 !important;
        color: transparent !important;
        width: 0 !important;
    }}
    
    /* Fullscreen buttons on charts/textareas */
    [data-testid="StyledFullScreenButton"] span {{
        font-size: 0 !important;
        color: transparent !important;
    }}
    [data-testid="StyledFullScreenButton"]::before {{
        content: "⛶" !important;
        font-size: 14px !important;
        color: #94a3b8 !important;
    }}
    
    /* TextArea/TextInput clear/action buttons */
    [data-testid="stTextArea"] button span,
    [data-testid="stTextInput"] button span,
    [data-testid="stChatInput"] button span,
    [data-testid="stNumberInput"] button span {{
        font-size: 0 !important;
        color: transparent !important;
    }}
    
    /* V40.9: FIX OVERLAP — Selectbox input hint text */
    [data-baseweb="select"] input {{
        opacity: 0 !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
    }}
    
    /* V40.9: FIX Material Symbols — force proper font rendering */
    .material-symbols-outlined,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] span,
    button[kind="headerNoPadding"] span {{
        font-family: 'Material Symbols Outlined' !important;
        font-size: 24px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 24px !important;
        height: 24px !important;
        overflow: hidden !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
    }}
    
    /* V40.9: NUCLEAR — nếu font vẫn không load, ẩn text thô hoàn toàn */
    @supports not (font-family: 'Material Symbols Outlined') {{
        .material-symbols-outlined,
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="collapsedControl"] span {{
            font-size: 0 !important;
            color: transparent !important;
        }}
    }}
    
    /* V40.9: FIX Expander toggle icon text */
    [data-testid="stExpander"] summary > span:first-child {{
        overflow: hidden !important;
        max-width: 24px !important;
        display: inline-flex !important;
    }}
    
    /* V40.9: FIX Sidebar toggle button */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {{
        overflow: hidden !important;
    }}
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button {{
        overflow: hidden !important;
        width: 32px !important;
        height: 32px !important;
    }}
    
    /* V40.9: NUCLEAR FIX — ẩn MỌI broken Material Symbols text */
    /* TextArea expand/fullscreen button */
    [data-testid="stTextArea"] button span,
    [data-testid="stTextInput"] button span,
    [data-testid="stChatInput"] button span,
    [data-testid="stNumberInput"] button span,
    textarea + div span,
    [data-testid="StyledFullScreenButton"] span,
    button[data-testid="StyledFullScreenButton"] span {{
        font-family: 'Material Symbols Outlined', sans-serif !important;
        font-size: 18px !important;
        width: 20px !important;
        height: 20px !important;
        overflow: hidden !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        -webkit-font-feature-settings: 'liga' !important;
    }}
    
    /* V40.9: Fullscreen overlay button on ALL containers */
    [data-testid="StyledFullScreenButton"] {{
        overflow: hidden !important;
    }}
    [data-testid="StyledFullScreenButton"] span {{
        font-family: 'Material Symbols Outlined' !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
    }}

    html {{
        font-size: {zoom}% !important;
        transition: font-size 0.2s ease-in-out;
    }}
    /* Adjust body to inherit or reset if needed, but rem is based on html */
    body {{
        font-size: 1rem; 
    }}

    /* === RESPONSIVE UI/UX OPTIMIZATION (DESKTOP & MOBILE) === */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1400px !important;
    }}
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        gap: 6px !important;
        flex-wrap: wrap !important;
    }}
    [data-testid="stTabs"] [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 14px !important;
        font-weight: 700 !important;
    }}
    table {{
        width: 100% !important;
    }}
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
            padding-top: 1rem !important;
        }}
        h1 {{
            font-size: 1.45rem !important;
        }}
        h2 {{
            font-size: 1.25rem !important;
        }}
        h3 {{
            font-size: 1.1rem !important;
        }}
        [data-testid="stVerticalBlock"] > div {{
            word-break: break-word !important;
        }}
        table td, table th {{
            padding: 5px 6px !important;
            font-size: 0.85rem !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

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
            # else:
            #     st.sidebar.error("🔴 **AI Factory: OFFLINE**")
                if is_active_247:
                    st.sidebar.caption("⌛ Đang chờ GitHub Action...")
except Exception: pass

# --- AI MODEL BADGE ---
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='text-align:center;margin:15px 0;'>
    <div style='background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);padding:24px 16px;border-radius:20px;border:1px solid rgba(255,215,0,0.3);box-shadow:0 8px 32px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.1);position:relative;overflow:hidden;'>
        <div style='position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:conic-gradient(from 0deg,transparent,rgba(255,215,0,0.05),transparent 40%);animation:spin 8s linear infinite;'></div>
        <div style='position:relative;z-index:1;'>
            <div style='font-size:2em;margin-bottom:8px;filter:drop-shadow(0 0 10px rgba(255,215,0,0.5));'>☯️</div>
            <div style='font-size:1.1em;font-weight:900;letter-spacing:2px;background:linear-gradient(90deg,#ffd700,#ff8c00,#ffd700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none;'>THIÊN CƠ ĐẠI SƯ</div>
            <div style='font-size:0.75em;color:#a78bfa;font-weight:600;margin:6px 0;letter-spacing:1px;'>{APP_VERSION}</div>
            <div style='display:inline-flex;align-items:center;gap:6px;background:rgba(34,197,94,0.15);padding:6px 14px;border-radius:20px;border:1px solid rgba(34,197,94,0.3);margin:8px 0;'>
                <span style='width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;box-shadow:0 0 8px #22c55e;'></span>
                <span style='color:#86efac;font-size:0.8em;font-weight:700;'>HOẠT ĐỘNG TỐT</span>
            </div>
            <div style='font-size:0.7em;color:#94a3b8;margin-top:8px;line-height:1.5;'>🎯 4 PP Chuẩn: Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản<br>🏛️ Tách Riêng: Tử Vi (Đời) · Thái Ất (Quốc Gia) · Xem Ngày</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══ V42.9.5: TOGGLE ON/OFF cho Tử Vi + Xem Ngày ═══
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔌 Module Bổ Sung")
_tv_on = st.sidebar.toggle("🔮 Tử Vi Đẩu Số", value=st.session_state.get('tv_module_on', False), key="tv_toggle")
_xn_on = st.sidebar.toggle("📅 Xem Ngày Đẹp", value=st.session_state.get('xn_module_on', False), key="xn_toggle")
st.session_state['tv_module_on'] = _tv_on
st.session_state['xn_module_on'] = _xn_on
if _tv_on:
    st.sidebar.caption("✅ Tử Vi → inject vào Pipeline 7 tầng")
if _xn_on:
    st.sidebar.caption("✅ Xem Ngày → inject vào Pipeline 7 tầng")

# Add project root and dist directory to Python path
root_path = os.path.dirname(os.path.abspath(__file__))
dist_path = os.path.join(root_path, 'dist')
ai_modules_path = os.path.join(root_path, 'ai_modules')

for path in [root_path, dist_path, ai_modules_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Performance Optimization: Import custom modules once without forced disk reload on every UI click
try:
    import mai_hoa_dich_so
    import luc_hao_kinh_dich
except Exception:
    pass

# Initialize fallbacks to prevent NameErrors if core files are missing
KY_MON_DATA = {"DU_LIEU_DUNG_THAN_PHU_TRO": {"CUU_TINH": {}, "BAT_THAN": {}, "BAT_MON": {}}}
TOPIC_INTERPRETATIONS = {}
BAT_MON_CO_DINH_DISPLAY = {}
BAT_MON_CO_DINH_CUNG = {}
CUNG_NGU_HANH = {
    1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 
    5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"
}
QUAI_TUONG = {
    1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 
    5: "Trung", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"
}

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
    print(f"âš ï¸  AI Factory modules not available: {e}")
    
# --- INLINED GEMINI HELPER (DEPLOYMENT FIX V2.2) ---
# [REMOVED DUPLICATE CLASS DEFINITION]
# The active definition is at the bottom of the file (Lines 1400+)
GEMINI_AVAILABLE = True

        
# Import Free AI helper as fallback
try:
    from free_ai_helper import FreeAIHelper
    FREE_AI_AVAILABLE = True
except ImportError:
    FREE_AI_AVAILABLE = False

# ======================================================================
# INITIALIZE SESSION STATE & CACHE BUSTING
# ======================================================================
# V42.9.9i: FORCE CACHE BUST WHEN VERSION CHANGES
if st.session_state.get('saved_app_version') != APP_VERSION:
    _saved_keys = {k: st.session_state[k] for k in st.session_state if 'api_key' in k.lower() or 'cookie' in k.lower()}
    st.session_state.clear()
    for k, v in _saved_keys.items():
        st.session_state[k] = v
    st.session_state['saved_app_version'] = APP_VERSION
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
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

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
    /* === V40.8 SIÊU PREMIUM THEME === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    
    @keyframes spin { from {transform:rotate(0deg)} to {transform:rotate(360deg)} }
    @keyframes pulse-glow { 0%,100% {box-shadow:0 0 5px rgba(34,197,94,0.3)} 50% {box-shadow:0 0 20px rgba(34,197,94,0.6)} }
    @keyframes shimmer { 0% {background-position:-200% 0} 100% {background-position:200% 0} }
    @keyframes fadeInUp { from {opacity:0;transform:translateY(20px)} to {opacity:1;transform:translateY(0)} }
    
    .stApp {
        background: linear-gradient(160deg, #0f0c29 0%, #1a1145 30%, #0c1222 60%, #0a0a1a 100%) !important;
        color: #e2e8f0;
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
        font-size: 1.4rem; /* Reduced from 1.8rem */
        font-weight: 900;
        /* Clean Soft Shadow for Readability */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 2px rgba(0,0,0,0.5);
        letter-spacing: 0.5px;
    }

    .sao-corner {
        position: absolute;
        top: 100px;
        left: 15px;
        font-size: 1.3rem; /* Reduced from 1.6rem */
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 2px rgba(0,0,0,0.5);
    }

    .mon-corner {
        position: absolute;
        top: 100px;
        right: 15px;
        font-size: 1.5rem; /* Reduced from 1.9rem */
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 2px rgba(0,0,0,0.5);
    }

    .thien-corner {
        position: absolute;
        bottom: 50px;
        right: 15px;
        font-size: 1.4rem; /* Reduced from 1.8rem */
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 2px rgba(0,0,0,0.5);
    }

    .dia-corner {
        position: absolute;
        bottom: 12px;
        right: 15px;
        font-size: 1.4rem; /* Reduced from 1.8rem */
        font-weight: 900;
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8), 0 0 2px rgba(0,0,0,0.5);
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
 0.86rem; }
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

    /* ═══════════════════════════════════════════════════════ */
    /* V40.8 SIÊU PREMIUM — DARK LUXE THEME                 */
    /* ═══════════════════════════════════════════════════════ */
    
    /* SIDEBAR — Glassmorphism Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1145 50%, #0c1222 100%) !important;
        border-right: 1px solid rgba(255,215,0,0.15) !important;
    }
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] .stTextArea label {
        color: #a78bfa !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* HEADER — Premium gradient */
    [data-testid="stHeader"] {
        background: linear-gradient(90deg, #0f0c29, #302b63, #24243e) !important;
        border-bottom: 1px solid rgba(255,215,0,0.2) !important;
    }
    
    /* MARKDOWN — Dark premium typography */
    [data-testid="stMarkdown"] { animation: fadeInUp 0.3s ease-out; }
    [data-testid="stMarkdown"] p,
    [data-testid="stMarkdown"] li {
        color: #e2e8f0 !important;
        line-height: 1.7 !important;
    }
    [data-testid="stMarkdown"] h1,
    [data-testid="stMarkdown"] h2,
    [data-testid="stMarkdown"] h3 {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 900 !important;
    }
    [data-testid="stMarkdown"] strong,
    [data-testid="stMarkdown"] b {
        color: #fbbf24 !important;
        font-weight: 800 !important;
    }
    [data-testid="stMarkdown"] code {
        background: rgba(139,92,246,0.15) !important;
        color: #c4b5fd !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
    }
    [data-testid="stMarkdown"] pre {
        background: rgba(15,23,42,0.8) !important;
        border: 1px solid rgba(100,116,139,0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    /* DETAILS — Glassmorphism */
    details {
        background: rgba(15,23,42,0.6) !important;
        border: 1px solid rgba(148,163,184,0.2) !important;
        border-radius: 14px !important;
        padding: 4px 16px !important;
        margin: 12px 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    details summary {
        cursor: pointer !important;
        padding: 12px 8px !important;
        color: #a78bfa !important;
        font-weight: 700 !important;
    }
    details summary:hover { color: #c4b5fd !important; }
    details[open] summary {
        border-bottom: 1px solid rgba(167,139,250,0.2) !important;
        margin-bottom: 12px !important;
    }
    
    /* TABLE — Dark premium */
    [data-testid="stTable"] {
        background-color: rgba(15,23,42,0.7) !important;
        border: 1px solid rgba(148,163,184,0.2) !important;
        border-radius: 12px !important;
    }
    [data-testid="stTable"] th {
        background: linear-gradient(135deg,#312e81,#1e1b4b) !important;
        color: #c4b5fd !important;
        font-weight: 800 !important;
    }
    [data-testid="stTable"] td {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    /* BUTTON — Premium glow */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed, #6d28d9, #5b21b6) !important;
        color: #f5f3ff !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(124,58,237,0.6), 0 0 20px rgba(139,92,246,0.3) !important;
    }
    
    /* ALERT — Dark */
    .stAlert {
        background: rgba(30,41,59,0.8) !important;
        border-radius: 12px !important;
    }
    .stAlert p { color: #e2e8f0 !important; }
    
    /* INPUT — Dark luxury */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background: rgba(15,23,42,0.8) !important;
        border: 1px solid rgba(139,92,246,0.3) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 12px rgba(139,92,246,0.3) !important;
    }
    
    /* DIVIDER — Gradient glow */
    [data-testid="stMarkdown"] hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent) !important;
    }
    
    /* SCROLLBAR — Premium */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f0c29; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg,#7c3aed,#4c1d95); border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: #8b5cf6; }

    /* ═══ V40.8 FIX: DARK BACKGROUND TOÀN BỘ ═══ */
    
    /* MAIN APP BACKGROUND — use config.toml dark colors */
    .stApp {
        background: #1a1a2e !important;
    }
    
    /* ALL CONTAINERS — transparent */
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"] {
        background: transparent !important;
    }
    
    /* FIX: SELECTBOX — dark + fix overlap */
    [data-testid="stSelectbox"] > div > div {
        background: #2c3e50 !important;
        border: 1px solid rgba(139,92,246,0.3) !important;
        border-radius: 10px !important;
        min-height: 42px !important;
    }
    [data-testid="stSelectbox"] svg { fill: #a78bfa !important; }
    
    /* FIX: Hide arrow key hint text that causes overlap */
    [data-testid="stSelectbox"] [data-baseweb="select"] input {
        color: transparent !important;
        caret-color: transparent !important;
        width: 0 !important;
        min-width: 0 !important;
        position: absolute !important;
    }
    
    /* FIX: DROPDOWN options — dark */
    [data-baseweb="popover"], [data-baseweb="menu"],
    [data-baseweb="select"] [role="listbox"] {
        background: #34495e !important;
        border: 1px solid rgba(139,92,246,0.3) !important;
    }
    [data-baseweb="menu"] li { color: #ecf0f1 !important; }
    [data-baseweb="menu"] li:hover { background: rgba(139,92,246,0.2) !important; }
    
    /* FIX: EXPANDER — dark */
    [data-testid="stExpander"] {
        background: rgba(44,62,80,0.7) !important;
        border: 1px solid rgba(148,163,184,0.2) !important;
        border-radius: 12px !important;
    }
    
    /* FIX: RADIO + CHECKBOX */
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        color: #ecf0f1 !important;
    }

    /* ═══ V40.9 FIX: FORCE DARK cho MỌI Streamlit component ═══ */
    
    /* Alert boxes (st.info, st.success, st.warning, st.error) */
    [data-testid="stAlert"],
    [data-testid="stNotification"],
    .stAlert, .element-container .stAlert {
        background: rgba(30,41,59,0.9) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {
        color: #e2e8f0 !important;
    }
    
    /* Chat message */
    [data-testid="stChatMessage"] {
        background: rgba(30,41,59,0.7) !important;
        border: 1px solid rgba(100,116,139,0.3) !important;
    }
    
    /* Forms */
    [data-testid="stForm"] {
        background: rgba(30,41,59,0.5) !important;
        border: 1px solid rgba(100,116,139,0.2) !important;
        border-radius: 12px !important;
    }
    
    /* Code blocks */
    [data-testid="stCode"], code, pre {
        background: #1e293b !important;
        color: #e2e8f0 !important;
    }
    
    /* DataFrames & Tables */
    [data-testid="stDataFrame"],
    [data-testid="stTable"],
    .stDataFrame, .stTable {
        background: rgba(30,41,59,0.7) !important;
    }
    [data-testid="stDataFrame"] th,
    [data-testid="stTable"] th {
        background: #1e293b !important;
        color: #fbbf24 !important;
    }
    [data-testid="stDataFrame"] td,
    [data-testid="stTable"] td {
        background: rgba(15,23,42,0.5) !important;
        color: #e2e8f0 !important;
    }
    
    /* Status containers (st.status) */
    [data-testid="stStatusWidget"] {
        background: rgba(30,41,59,0.8) !important;
    }
    
    /* Toast messages */
    [data-testid="stToast"] {
        background: #1e293b !important;
        color: #e2e8f0 !important;
    }
    
    /* Caption text */
    [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
    }
    
    /* NUCLEAR FIX: Any remaining light backgrounds */
    .element-container > div[style*="background-color: rgb(255"],
    .element-container > div[style*="background-color: rgb(252"],
    .element-container > div[style*="background-color: rgb(250"],
    .element-container > div[style*="background-color: rgb(248"],
    .element-container > div[style*="background-color: rgb(245"],
    .element-container > div[style*="background-color: rgb(240"],
    .element-container > div[style*="background-color: rgb(235"] {
        background-color: rgba(30,41,59,0.9) !important;
        color: #e2e8f0 !important;
    }
    
    /* Streamlit info/success/warning/error specific selectors */
    div[data-testid="stAlert"] > div {
        background: transparent !important;
    }
    
    /* Bottom toolbar / footer */
    [data-testid="stBottomBlockContainer"],
    [data-testid="stToolbar"] {
        background: #0f172a !important;
    }
    footer { background: #0f172a !important; color: #64748b !important; }

    /* V40.9: Tượng Quẻ box — dark */
    .tuong-que-box {
        background: rgba(22,33,62,0.9) !important;
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #ecf0f1;
    }
    .tuong-que-box strong { color: #fbbf24; }

    /* V40.9: interpret-box — dark */
    .interpret-box {
        background: rgba(22,33,62,0.9) !important;
        border-top: 5px solid #7c3aed !important;
        border-radius: 12px;
        padding: 16px;
        color: #ecf0f1 !important;
    }
    .interpret-box * { color: #ecf0f1 !important; }
    .interpret-box strong, .interpret-box b { color: #fbbf24 !important; }
    .interpret-box h1, .interpret-box h2, .interpret-box h3 { color: #a78bfa !important; }

    /* V40.9: Fix Material Icons showing as raw text */
    [data-testid="stExpander"] span.material-symbols-outlined,
    span[class*="material"] {
        font-size: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
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
# DEPLOYMENT VERIFICATION BANNER
st.success(f"✅ SYSTEM ONLINE: {APP_VERSION_FULL}")
try:
    from lich_van_nien_thien_van import render_compact_today_banner
    render_compact_today_banner()
except Exception:
    pass

# ======================================================================
# SIDEBAR - CONTROLS
# ======================================================================
with st.sidebar:
    st.markdown("### ⚙️ Điều Khiển")
    
    # View selection
    view_option = st.radio(
        "Chọn Phương Pháp:",
        ["🔮 Kỳ Môn Độn Giáp", "🗓️ Lịch Vạn Niên & Thiên Văn", "🏭 Nhà Máy AI", "🌟 40 Chuyên Gia AI", "📖 Mai Hoa 64 Quẻ", "☯️ Lục Hào Kinh Dịch", "📜 Thiết Bản Thần Toán", "📊 Vạn Vật Loại Tượng", "🌊 Đại Lục Nhâm", "⭐ Thái Ất Thần Số", "📅 Xem Ngày Đẹp", "🔯 Tử Vi Đẩu Số", "🤖 Hỏi Gemini AI"],
        index=0
    )
    
    if view_option == "🔮 Kỳ Môn Độn Giáp":
        st.session_state.current_view = "ky_mon"
    elif view_option == "🗓️ Lịch Vạn Niên & Thiên Văn":
        st.session_state.current_view = "lich_van_nien"
    elif view_option == "🏭 Nhà Máy AI":
        st.session_state.current_view = "ai_factory"
    elif view_option == "🌟 40 Chuyên Gia AI":
        st.session_state.current_view = "ai_experts"
    elif view_option == "📖 Mai Hoa 64 Quẻ":
        st.session_state.current_view = "mai_hoa"
    elif view_option == "☯️ Lục Hào Kinh Dịch":
        st.session_state.current_view = "luc_hao"
    elif view_option == "📜 Thiết Bản Thần Toán":
        st.session_state.current_view = "thiet_ban"
    elif view_option == "📊 Vạn Vật Loại Tượng":
        st.session_state.current_view = "van_vat"
    elif view_option == "🌊 Đại Lục Nhâm":
        st.session_state.current_view = "dai_luc_nham"
    elif view_option == "⭐ Thái Ất Thần Số":
        st.session_state.current_view = "thai_at"
    elif view_option == "📅 Xem Ngày Đẹp":
        st.session_state.current_view = "xem_ngay"
    elif view_option == "🔯 Tử Vi Đẩu Số":
        st.session_state.current_view = "tu_vi"
    else:  # 🤖 Hỏi Gemini AI
        st.session_state.current_view = "gemini_ai"

    st.markdown("---")
    
    # V25.0: RAG Feedback Form Sidebar
    try:
        from ai_modules.feedback_rag import FeedbackRAG
        rag = FeedbackRAG()
    except Exception:
        rag = None
        
    if rag:
        with st.expander("🎓 RÚT KINH NGHIỆM AI THỰC TẾ", expanded=False):
            st.caption("Nhập kết quả thực tế của một quẻ trong quá khứ để giúp AI khôn hơn.")
            with st.form("rag_feedback_form"):
                r_q = st.text_input("Câu hỏi ban đầu:", placeholder="Ví dụ: Lô hàng có về kịp không?")
                r_dt = st.text_input("Dụng Thần (bắt buộc):", placeholder="Thê Tài")
                r_status = st.radio("Kết quả thực tế:", ["✅ ĐÚNG", "❌ SAI"], horizontal=True)
                r_text = st.text_area("Giải thích diễn biến:", placeholder="Ví dụ: Vì gặp bão nên chậm 2 ngày so với dự kiến...")
                r_analysis = st.text_area("Mổ Xẻ Lỗi Của AI (chỉ ghi nếu chọn SAI):", placeholder="Ví dụ: AI lấy sai Dụng thần, quên không tính đến yếu tố Tuần Không của Cung...")
                
                submitted = st.form_submit_button("💾 LƯU ÁN LỆ VÀO NÃO AI")
                if submitted:
                    if not r_dt.strip() or not r_text.strip():
                        st.error("Vui lòng nhập đủ Dụng Thần và Lời giải thích!")
                    else:
                        rag.save_feedback(
                            question=r_q.strip(),
                            dung_than=r_dt.strip(),
                            result_status=r_status.replace("✅ ", "").replace("❌ ", ""),
                            feedback_text=r_text.strip(),
                            user_analysis=r_analysis.strip(),
                            chart_summary="Được nạp thủ công từ Form Rút Kinh Nghiệm."
                        )
                        st.success("🎉 Nạp vào Bộ Nhớ Án Lệ thành công!")

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

    # Always resolve the API key so it's available for checks below
    # ƯU TIÊN 1: Streamlit Cloud Secrets (Quan trọng nhất cho deployment)
    st_secret = None
    try:
        st_secret = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        pass
    
    # ƯU TIÊN 2: File custom_data.json (Local)
    custom_data = load_custom_data()
    saved_key = cookie_manager.get(cookie="GEMINI_API_KEY")
    if not saved_key:
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
    
    # ƯU TIÊN 0: User Manual Input (Session State) - QUAN TRỌNG NHẤT
    manual_key = st.session_state.get("gemini_key")
    
    # V99.8: Tổng hợp TẤT CẢ các nguồn Key (Manual > Saved Cookie/Custom > Factory > Streamlit Secrets)
    # để GeminiQMDGHelper tự động xoay vòng nếu 1 key hết hạn hoặc hết quota!
    _all_key_sources = [k for k in [manual_key, saved_key, factory_key, st_secret] if k and str(k).strip()]
    secret_api_key = ",".join(list(dict.fromkeys(_all_key_sources))) if _all_key_sources else None
    
    st.session_state._resolved_api_key = secret_api_key
    
    # Thông báo nếu chạy trên cloud nhưng chưa có secret
    if not secret_api_key:
        # Đang chạy trên cloud và không có API key nào
        st.session_state.missing_cloud_secret = True
    else:
        st.session_state.missing_cloud_secret = False

    # Actual Initialization Logic
    if 'gemini_helper' not in st.session_state:
        # FIX: Removed buggy checks (typo 'analyze_mai_hao' instead of 'analyze_mai_hoa' + version check)
        # These caused re-initialization on EVERY rerun, triggering API key re-resolution loop
        pass
        
try:
    from google import genai
except ImportError:
    genai = None

# --- API KEY LED STATUS (Sidebar - Compact) ---
with st.sidebar:
    _key_led = "🟢" if st.session_state.get("api_status_ok") else "🔴"
    _key_status = "Hoạt động" if st.session_state.get("api_status_ok") else "Chưa kết nối"
    st.caption(f"{_key_led} API Key: {_key_status}")

# --- IMPORT GEMINI HELPER FROM EXTERNAL MODULE (Unified Logic) ---
try:
    import gemini_helper
    import importlib
    # REMOVED: importlib.reload(gemini_helper) - This causes C-extension thread deadlocks and UI freezes!
    from gemini_helper import GeminiQMDGHelper
except ImportError:
    pass
    pass

# ════════════════════════════════════════════════════
# V19.0: DISPLAY AI RESULT — Beautiful answer layout
# ════════════════════════════════════════════════════
def display_ai_result(text, key_prefix="ai"):
    """V40.9: Render AI result — verdict box đã được tạo sẵn trong text, chỉ cần render."""
    if not text:
        st.warning("❌ Không có kết quả")
        return
    
    text = str(text).strip()
    
    # V40.9: KHÔNG tạo thêm verdict box — đã có sẵn trong text (NÂU + XANH LÁ)
    # Chỉ render text trực tiếp
    st.markdown(f"""
    <div class="interpret-box" style="background: rgba(22,33,62,0.9); border-top: 5px solid #7c3aed; color: #ecf0f1;">
        {text}
    </div>
    """, unsafe_allow_html=True)


class PhoenixOrchestrator:
    """Wrapper class to maintain compatibility with existing code while routing to gemini_helper"""
    def __init__(self, gemini_helper):
        self.gemini = gemini_helper
        self.logs = []
    
    def log_step(self, step_name, status, detail=""):
        pass

    def render_logs(self):
        pass

    def run_pipeline(self, user_question, current_topic="Chung", chart_data=None, mai_hoa_data=None, luc_hao_data=None, tb_context="", **kwargs):
        enhanced_question = user_question + tb_context if tb_context else user_question
        return self.gemini.answer_question(enhanced_question, chart_data=chart_data, topic=current_topic, mai_hoa_data=mai_hoa_data, luc_hao_data=luc_hao_data, **kwargs)

# Auto-Init logic — GUARD: Only init if not already in session_state
if 'gemini_helper' not in st.session_state:
    if st.session_state.ai_preference == "offline":
        if FREE_AI_AVAILABLE:
            st.session_state.gemini_helper = FreeAIHelper(api_key=st.session_state.get('_resolved_api_key'))
            st.session_state.ai_type = "Free AI (Manual Offline)"
            st.session_state.api_status_ok = True
            st.session_state.api_status_msg = "Offline Mode"
    else: # auto or online
        if secret_api_key and GEMINI_AVAILABLE:
            try:
                # INSTANTIATE AND AUTO-TEST CONNECTION
                _temp_helper = GeminiQMDGHelper(secret_api_key)
                _success, _msg = _temp_helper.test_connection()
                st.session_state.gemini_helper = _temp_helper
                st.session_state.gemini_key = secret_api_key
                st.session_state.ai_orchestrator = PhoenixOrchestrator(_temp_helper)
                if _success:
                    st.session_state.ai_type = f"Gemini ({_temp_helper.model_name})"
                    st.session_state.api_status_ok = True
                    st.session_state.api_status_msg = _msg
                else:
                    st.session_state.ai_type = "Gemini (Lỗi kết nối)"
                    st.session_state.api_status_ok = False
                    st.session_state.api_status_msg = _msg
            except Exception as e: 
                st.session_state.api_status_ok = False
                st.session_state.api_status_msg = f"Lỗi Gemini: {e}"
                if FREE_AI_AVAILABLE:
                    st.session_state.gemini_helper = FreeAIHelper(api_key=st.session_state.get('_resolved_api_key'))
                    st.session_state.ai_type = "Free AI (Fallback từ Lỗi)"
        elif FREE_AI_AVAILABLE:
            st.session_state.gemini_helper = FreeAIHelper(api_key=st.session_state.get('_resolved_api_key'))
            st.session_state.ai_type = "Free AI (Offline Mode)"
            st.session_state.api_status_ok = True
            st.session_state.api_status_msg = "Offline Mode"

# === SIDEBAR DISPLAY (Always runs, NOT inside the guard above) ===
# AI Status Display with LED Indicator
ai_status = st.session_state.get('ai_type', 'Chưa sẵn sàng')

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
_err_msg = ""
if st.session_state.api_status_ok is False:
    _err_msg = str(st.session_state.api_status_msg).replace('<','&lt;').replace('>','&gt;')

# AI Status Display - Clean HTML (no nesting issues)
_status_html = f'<div style="background:linear-gradient(135deg,{status_color}22 0%,{status_color}11 100%);border-left:4px solid {status_color};padding:15px;border-radius:8px;margin-bottom:10px;">'
_status_html += f'<div style="display:flex;align-items:center;gap:10px;">'
_status_html += f'<span style="font-size:24px;">{led_color}</span>'
_status_html += f'<div style="flex:1;">'
_status_html += f'<div style="font-weight:800;color:{status_color};font-size:0.9rem;">{status_text}</div>'
_status_html += f'<div style="font-weight:600;color:#475569;font-size:0.85rem;">🤖 {ai_status}</div>'
if _err_msg:
    _status_html += f'<div style="font-size:0.75rem;color:#dc2626;margin-top:5px;font-style:italic;">{_err_msg}</div>'
_status_html += '</div></div></div>'
st.markdown(_status_html, unsafe_allow_html=True)

# --- DEFERRED AI INITIALIZATION (Because classes are defined above) ---
if 'gemini_helper' not in st.session_state and st.session_state.get('_resolved_api_key'):
    try:
        temp_helper = GeminiQMDGHelper(st.session_state._resolved_api_key)
        st.session_state.gemini_helper = temp_helper
        st.session_state.ai_orchestrator = PhoenixOrchestrator(temp_helper)
        st.session_state.api_status_ok = True
        st.session_state.api_status_msg = "Sẵn sàng"
    except Exception as e:
        st.session_state.api_status_ok = False
        st.session_state.api_status_msg = str(e)
        if FREE_AI_AVAILABLE:
            st.session_state.gemini_helper = FreeAIHelper(api_key=st.session_state.get('_resolved_api_key'))

# UNIFIED SETTINGS (One place for everything)
is_connected = st.session_state.get("api_status_ok", False) is True
# UNIFIED API KEY INPUT (ONE PLACE ONLY)
_key_led_main = "🟢" if is_connected else "🔴"
_key_label = f"{_key_led_main} API Key đang hoạt động tốt" if is_connected else f"{_key_led_main} Chưa có Key / Key hỏng — Bấm để dán Key mới"
expander_title = f"🔑 {_key_label}"

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
                    st.rerun()
        with col2:
            if st.button("R", key="force_refresh_unified", help="Reload App", use_container_width=True):
                st.rerun()
                
        st.markdown("---")

    # 2. UNIFIED KEY INPUT — 1 Ô Duy Nhất
    st.markdown("👉 [Lấy Gemini API Key miễn phí](https://aistudio.google.com/app/apikey)")
    
    user_api_input = st.text_area("📋 Dán API Key vào đây:", height=80, key="input_api_key_smart_unified", placeholder="AIzaSy... hoặc AQ.Ab8... (hỗ trợ dán nhiều key cùng lúc)")
    
    # --- 2 NÚT HÀNH ĐỘNG ---
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        btn_activate = st.button("⚡ KÍCH HOẠT + LƯU VĨNH VIỄN", type="primary", use_container_width=True, help="Kích hoạt key ngay + tự lưu lên GitHub vĩnh viễn")
    
    with btn_col2:
        btn_clear_keys = st.button("🗑️ XÓA KEY CŨ", use_container_width=True, help="Xóa tất cả API key hết quota để nhập key mới")
    
    # --- XỬ LÝ: XÓA KEY CŨ ---
    if btn_clear_keys:
        with st.spinner("🗑️ Đang xóa API key cũ từ tất cả nơi lưu trữ..."):
            cleared = []
            for k in ['api_key', 'gemini_key', 'gemini_helper', 'ai_orchestrator', 'api_status_ok', 'api_status_msg']:
                if k in st.session_state:
                    del st.session_state[k]
            cleared.append("Session")
            try:
                data = load_custom_data()
                if data.get("GEMINI_API_KEY"):
                    data["GEMINI_API_KEY"] = ""
                    save_custom_data(data)
                    cleared.append("custom_data.json")
            except: pass
            try:
                import json as _json
                fc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_hub', 'factory_config.json')
                if os.path.exists(fc_path):
                    with open(fc_path, 'r', encoding='utf-8') as f:
                        fc = _json.load(f)
                    if fc.get("api_key"):
                        fc["api_key"] = ""
                        with open(fc_path, 'w', encoding='utf-8') as f:
                            _json.dump(fc, f, indent=2)
                        cleared.append("factory_config.json")
            except: pass
            try:
                cookie_manager.set("GEMINI_API_KEY", "", expires_at=dt_module.datetime.now() + dt_module.timedelta(days=-1))
                cleared.append("Cookie")
            except: pass
            st.success(f"✅ ĐÃ XÓA SẠCH API KEY CŨ từ: {', '.join(cleared)}")
            st.info("👉 Giờ hãy dán API Key mới vào ô trên → bấm **⚡ KÍCH HOẠT + LƯU VĨNH VIỄN**")
            time.sleep(2)
            st.rerun()
    
    # --- XỬ LÝ: KÍCH HOẠT + TỰ ĐỘNG LƯU VĨNH VIỄN ---
    if btn_activate:
        if not user_api_input:
            st.warning("⚠️ Dán Key vào ô trên trước!")
        else:
            with st.spinner("🤖 Đang kích hoạt + lưu vĩnh viễn..."):
                try:
                    # Bước 1: Kích hoạt ngay trong session
                    temp_helper = GeminiQMDGHelper(user_api_input)
                    if not temp_helper.api_keys:
                        st.error("❌ Không tìm thấy API Key hợp lệ. Key phải dài ít nhất 20 ký tự.")
                    else:
                        success, msg = temp_helper.test_connection()
                        st.session_state.gemini_helper = temp_helper
                        st.session_state.gemini_key = temp_helper.api_key
                        st.session_state.ai_type = f"Gemini (Updated)"
                        st.session_state.ai_orchestrator = PhoenixOrchestrator(temp_helper)
                        
                        _final_key = temp_helper.api_key or ",".join(temp_helper.api_keys)
                        
                        # Bước 2: Lưu local (custom_data + cookie + factory_config)
                        try:
                            data = load_custom_data()
                            data["GEMINI_API_KEY"] = _final_key
                            save_custom_data(data)
                            cookie_manager.set("GEMINI_API_KEY", _final_key, expires_at=dt_module.datetime.now() + dt_module.timedelta(days=365))
                        except: pass
                        try:
                            import json as _json
                            fc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_hub', 'factory_config.json')
                            if os.path.exists(fc_path):
                                with open(fc_path, 'r', encoding='utf-8') as f:
                                    fc = _json.load(f)
                                fc["api_key"] = _final_key
                                with open(fc_path, 'w', encoding='utf-8') as f:
                                    _json.dump(fc, f, indent=2)
                        except: pass
                        
                        # Bước 3: TỰ ĐỘNG push lên GitHub (vĩnh viễn)
                        _pat = ""
                        try: _pat = st.secrets.get("GITHUB_PAT", "")
                        except: pass
                        if not _pat:
                            _pat = st.session_state.get("github_pat", "")
                        if not _pat:
                            try: _pat = cookie_manager.get("GITHUB_PAT") or ""
                            except: pass
                        
                        if _pat:
                            # Có PAT → auto push
                            st.session_state._push_cloud_key = _final_key
                            st.session_state._push_cloud_pat = _pat
                        else:
                            # Chưa có PAT → yêu cầu 1 lần
                            st.session_state._need_pat_for_activate = _final_key
                        
                        if success:
                            st.session_state.api_status_ok = True
                            st.session_state.api_status_msg = "Kết nối thành công"
                            st.success(f"✅ ĐÃ KÍCH HOẠT: {len(temp_helper.api_keys)} Key")
                        else:
                            st.session_state.api_status_ok = False
                            st.session_state.api_status_msg = f"Lưu OK, test lỗi: {msg}"
                            st.warning(f"⚠️ Đã lưu, nhưng kết nối chập chờn: {msg}")
                        
                        if not _pat:
                            st.info("⚠️ Để lưu VĨNH VIỄN, cần nhập GitHub Token **1 lần duy nhất** bên dưới ↓")
                        time.sleep(1)
                        if _pat:
                            st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")
    
    # --- YÊU CẦU GITHUB PAT (1 lần duy nhất) ---
    if st.session_state.get("_need_pat_for_activate"):
        st.markdown("---")
        st.warning("🔐 **LẦN ĐẦU:** Nhập GitHub Token để lưu key vĩnh viễn (chỉ cần 1 lần, sau đó tự động)")
        st.markdown("👉 [Lấy GitHub Token tại đây](https://github.com/settings/tokens) → **Generate new token (classic)** → chọn scope **`repo`** → Copy token")
        _pat_input = st.text_input("GitHub Token:", type="password", placeholder="ghp_xxxxx...", key="github_pat_input_activate")
        if st.button("✅ LƯU VĨNH VIỄN", type="primary", use_container_width=True, key="confirm_pat_activate"):
            if _pat_input:
                _gemini_key = st.session_state.pop("_need_pat_for_activate", "")
                st.session_state.github_pat = _pat_input
                # Lưu PAT vào cookie → không bao giờ cần nhập lại
                try:
                    cookie_manager.set("GITHUB_PAT", _pat_input, expires_at=dt_module.datetime.now() + dt_module.timedelta(days=365))
                except: pass
                st.session_state._push_cloud_key = _gemini_key
                st.session_state._push_cloud_pat = _pat_input
                st.rerun()
            else:
                st.error("❌ Dán GitHub Token vào!")
    
    # V13.0: Old LƯU LÊN CLOUD handler removed — merged into KÍCH HOẠT + LƯU VĨNH VIỄN above
    
    # --- THỰC HIỆN PUSH (chung cho cả 2 flow) ---
    if st.session_state.get("_push_cloud_key") and st.session_state.get("_push_cloud_pat"):
        _gemini_key = st.session_state.pop("_push_cloud_key")
        _pat = st.session_state.pop("_push_cloud_pat")
        
        with st.spinner("🚀 Đang push lên GitHub → Streamlit Cloud..."):
            try:
                import base64
                _GH_OWNER = "winvu88888888-maker"
                _GH_REPO = "cuongtan66666666"
                _GH_FILE = ".streamlit/secrets.toml"
                _GH_API = f"https://api.github.com/repos/{_GH_OWNER}/{_GH_REPO}/contents/{_GH_FILE}"
                _headers = {"Authorization": f"token {_pat}", "Accept": "application/vnd.github.v3+json"}
                
                _secrets_content = f'GEMINI_API_KEY = "{_gemini_key}"\nGITHUB_PAT = "{_pat}"\n'
                _encoded = base64.b64encode(_secrets_content.encode()).decode()
                
                # Get current file SHA
                _sha = None
                try:
                    _resp_get = requests.get(_GH_API, headers=_headers)
                    if _resp_get.status_code == 200:
                        _sha = _resp_get.json().get("sha")
                except: pass
                
                _payload = {"message": "auto: update API key from app UI", "content": _encoded, "branch": "main"}
                if _sha:
                    _payload["sha"] = _sha
                
                _resp_put = requests.put(_GH_API, headers=_headers, json=_payload)
                
                if _resp_put.status_code in [200, 201]:
                    st.session_state.github_pat = _pat
                    # Also activate immediately
                    try:
                        temp_helper = GeminiQMDGHelper(_gemini_key)
                        st.session_state.gemini_helper = temp_helper
                        st.session_state.gemini_key = _gemini_key
                        st.session_state.ai_orchestrator = PhoenixOrchestrator(temp_helper)
                    except: pass
                    st.success("✅ ĐÃ PUSH & KÍCH HOẠT! Cloud sẽ tự deploy lại ~1-2 phút.")
                    st.balloons()
                else:
                    _err = _resp_put.json().get("message", _resp_put.text[:200])
                    st.error(f"❌ Lỗi GitHub: {_err}")
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")

# n8n Configuration
with st.expander("🔗 Kết nối n8n (Advanced AI)"):
    n8n_url = ""
    try:
        n8n_url = st.secrets.get("N8N_WEBHOOK_URL", "")
    except Exception:
        pass
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
    
    # Calculate Lunar Date for display — V42.8 FIX: Use Hồ Ngọc Đức algorithm (accurate)
    from xem_ngay_dep import solar2lunar as _s2l_sidebar
    lday, lmonth, lyear, is_leap = _s2l_sidebar(selected_datetime.day, selected_datetime.month, selected_datetime.year)
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
except Exception as _hub_err:
    # V35.8-FIX: Show warning instead of silent fail
    try:
        st.warning(f"⚠️ Dữ liệu hub đang được sửa chữa tự động. Chi tiết: {str(_hub_err)[:100]}")
    except: pass

# Store full entry list for filtering
st.session_state.hub_entries = hub_entries

# Filter topics logic simplified for selectbox — safe access with fallback
all_titles = sorted(list(set(core_topics + [e.get('title', '') for e in hub_entries if isinstance(e, dict) and e.get('title')])))
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

# ═══ GLOBAL SYNC HUB: Tự động đồng bộ dữ liệu liên kết giữa tất cả 13 mục theo Thời Gian & Chủ Đề ═══
if params:
    try:
        from qmdg_data import an_bai_luc_nghi, lap_ban_qmdg, tinh_khong_vong, tinh_dich_ma
        _g_can_gio = params['can_gio']
        _g_dia_can = an_bai_luc_nghi(params['cuc'], params['is_duong_don'])
        _g_tb, _g_ctb, _g_nb, _g_sb, _g_tpc = lap_ban_qmdg(
            params['cuc'], params['truc_phu'], params['truc_su'],
            _g_can_gio, params['chi_gio'], params['is_duong_don']
        )
        st.session_state.chart_data = {
            'thien_ban': _g_tb,
            'can_thien_ban': _g_ctb,
            'nhan_ban': _g_nb,
            'than_ban': _g_sb,
            'dia_can': _g_dia_can,
            'dia_ban': _g_dia_can,
            'khong_vong_4': params.get('khong', {}),
            'dich_ma_4': params.get('ma', {}),
            'can_gio': _g_can_gio,
            'chi_gio': params['chi_gio'],
            'can_ngay': params['can_ngay'],
            'chi_ngay': params['chi_ngay'],
            'can_thang': params.get('can_thang', 'N/A'),
            'chi_thang': params.get('chi_thang', 'N/A'),
            'can_nam': params.get('can_nam', 'N/A'),
            'chi_nam': params.get('chi_nam', 'N/A'),
            'tiet_khi': params.get('tiet_khi', ''),
            'cuc': params.get('cuc', 1),
            'am_duong_don': f"{'Dương' if params.get('is_duong_don', True) else 'Âm'} Độn {params.get('cuc', 1)} Cục",
            'truc_phu': params.get('truc_phu', ''),
            'truc_su': params.get('truc_su', ''),
            'is_duong_don': params.get('is_duong_don', True),
            'nguyen': params.get('nguyen', ''),
            'phu_dau': params.get('phu_dau', ''),
            'year': selected_datetime.year,
            'month': selected_datetime.month,
            'day': selected_datetime.day,
            'hour': selected_datetime.hour,
            'minute': selected_datetime.minute,
        }
        if USE_MAI_HOA and not st.session_state.get('mai_hoa_result'):
            _g_mh = tinh_qua_theo_thoi_gian(selected_datetime.year, selected_datetime.month, selected_datetime.day, selected_datetime.hour)
            _g_mh['interpretation'] = giai_qua(_g_mh, selected_topic)
            st.session_state.mai_hoa_result = _g_mh
        if USE_LUC_HAO and not st.session_state.get('luc_hao_result'):
            st.session_state.luc_hao_result = lap_qua_luc_hao(
                selected_datetime.year, selected_datetime.month, selected_datetime.day, selected_datetime.hour,
                topic=selected_topic,
                can_ngay=params['can_ngay'],
                chi_ngay=params['chi_ngay'],
                can_thang=params.get('can_thang', ''),
                chi_thang=params.get('chi_thang', '')
            )
    except Exception:
        pass


def render_master_unified_qa_box(location_key="main"):
    """
    1 Ô HỎI ĐÁP HỢP NHẤT DUY NHẤT TOÀN HỆ THỐNG (V106.0):
    Phân tách rạch ròi PHẦN I (4 Phương Pháp Chuẩn Xác Nhất: Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản)
    và PHẦN II (Các Phân Khu Chuyên Biệt Độc Lập: Tử Vi Cả Cuộc Đời · Thái Ất Quốc Gia · Xem Ngày Giờ).
    """
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a,#1e1b4b,#064e3b);padding:18px 22px;border-radius:16px;
                border:2px solid #34d399;margin:14px 0;box-shadow:0 6px 24px rgba(16,185,129,0.22);'>
        <div style='color:#6ee7b7;font-weight:900;font-size:1.22rem;margin-bottom:8px;'>
            🔮 TRUNG TÂM HỎI ĐÁP PHÂN KHU CHUYÊN BIỆT (V106.0 — BỘ TỨ QUẺ CHUẨN XÁC & CÁC MẢNG ĐỘC LẬP)
        </div>
        <div style='display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;margin-top:6px;'>
            <div style='padding:10px 14px;background:rgba(16,185,129,0.14);border-radius:10px;border-left:4px solid #34d399;'>
                <div style='color:#4ade80;font-weight:900;font-size:0.95rem;'>🎯 PHẦN I — 4 PHƯƠNG PHÁP LUẬN QUẺ CHUẨN XÁC NHẤT (QUYẾT ĐỊNH 100% CÂU HỎI THỰC TẾ)</div>
                <div style='color:#e2e8f0;font-size:0.88rem;margin-top:4px;line-height:1.5;'>
                    <b style='color:#fde68a;'>🌸 Mai Hoa Dịch Số · 🏯 Kỳ Môn Độn Giáp · 📿 Lục Hào Kinh Dịch · 📜 Thiết Bản Thần Toán</b><br>
                    Chuyên giải mã trực tiếp mọi câu hỏi về Gia đình, Nhà cửa, Tài chính, Hôn nhân, Con cái, Đồ vật, Công việc.
                </div>
            </div>
            <div style='padding:10px 14px;background:rgba(139,92,246,0.14);border-radius:10px;border-left:4px solid #a78bfa;'>
                <div style='color:#c4b5fd;font-weight:900;font-size:0.95rem;'>🏛️ PHẦN II — CÁC PHÂN KHU CHUYÊN BIỆT ĐỘC LẬP (CHỈ XEM RIÊNG ĐÚNG PHẦN ĐÓ)</div>
                <div style='color:#e2e8f0;font-size:0.88rem;margin-top:4px;line-height:1.5;'>
                    • <b style='color:#d8b4fe;'>🔯 Tử Vi Đẩu Số:</b> Chỉ xem riêng về <b>Cả Cuộc Đời & Mệnh Cục 12 Cung</b>.<br>
                    • <b style='color:#fca5a5;'>⚔️ Thái Ất Thần Số:</b> Chỉ xem riêng về <b>Vận Quốc Gia, Thế Giới & Vĩ Mô</b>.<br>
                    • <b style='color:#5eead4;'>📅 Xem Ngày & Đại Lục Nhâm:</b> Chỉ xem riêng về <b>Chọn Ngày Giờ & Lộ Trình</b>.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── BỘ CHỌN PHÂN KHU CHUYÊN TRÁCH NGAY TRÊN Ô HỎI ĐÁP (V106.0) ──
    _domain_mode = st.radio(
        "🗂️ Chọn Phân Khu Xem (Hoặc để Mặc định ở Phần I để dùng 4 Phương Pháp Chuẩn Xác Nhất):",
        [
            "🎯 PHẦN I (Mặc định): Luận Quẻ Thực Tế Bằng 4 Phương Pháp Chuẩn Xác (Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản)",
            "🔯 PHẦN II — Mảng Riêng 1: Xem Về Cả Cuộc Đời & Số Mệnh Trọn Đời (Tử Vi Đẩu Số)",
            "⚔️ PHẦN II — Mảng Riêng 2: Xem Về Vận Quốc Gia, Thế Giới & Đại Cục Vĩ Mô (Thái Ất Thần Số)",
            "📅 PHẦN II — Mảng Riêng 3: Xem Về Chọn Ngày Giờ Tốt Xấu Hành Sự (Trạch Nhật Xem Ngày Đẹp)",
        ],
        index=0,
        key=f"qa_domain_partition_{location_key}"
    )

    # ── BỘ CHỌN CHẾ ĐỘ GIEO QUẺ TRỰC QUAN NGAY TRÊN Ô NHẬP CÂU HỎI (V110.0) ──
    c_cast1, c_cast2 = st.columns([1.2, 1.2])
    with c_cast1:
        _rnd_mode = st.toggle(
            "🎲 Gieo Quẻ Ngẫu Nhiên Mới Mỗi Lần Bấm (100% Đồng Bộ Mai Hoa · Lục Hào · Kỳ Môn)",
            value=st.session_state.get('random_hexagram_mode', False),
            key=f"qa_rnd_{location_key}",
            help="BẬT: Mỗi lần bấm Phân Tích sẽ gieo một quẻ ngẫu nhiên mới hoàn toàn bằng phần cứng OS Entropy (không bao giờ lặp lại quẻ trước) và đồng bộ 100% cả Mai Hoa + Lục Hào + Kỳ Môn. TẮT: Tự khởi quẻ theo Thời Gian + Thanh Âm Câu Hỏi (mỗi câu hỏi khác nhau trong cùng giờ cũng tự động ra quẻ riêng, không bao giờ trùng lặp!)."
        )
        st.session_state['random_hexagram_mode'] = _rnd_mode
    with c_cast2:
        _use_cloud_llm = st.toggle(
            "🌐 Chạy AI Online Gemini + 40 Chuyên Gia (Mặc định: BẬT)",
            value=st.session_state.get('qa_use_cloud_llm', True),
            key=f"qa_cloud_{location_key}",
            help="BẬT (Mặc định): Kết hợp đồng thời AI Online Gemini + 10 Hệ Thống Quẻ + 40 Chuyên Gia AI để luận giải sâu và chuẩn xác nhất."
        )
        st.session_state['qa_use_cloud_llm'] = _use_cloud_llm

    # ── TÙY CHỌN NÂNG CAO (GỌN TRONG 1 EXPANDER ĐỂ CHỈ CÒN 1 Ô HỎI ĐÁP DUY NHẤT) ──
    with st.expander("⚙️ Tùy chọn nâng cao (Không bắt buộc — Mặc định hệ thống tự động nhận diện từ câu hỏi & giờ gieo quẻ)", expanded=False):
        c_opt1, c_opt2 = st.columns([1, 1])
        with c_opt1:
            _lt_options = [
                "👤 Bản thân",
                "👴👵 Bố mẹ / Ông bà / Thầy cô",
                "💍 Vợ (nữ) / Tiền bạc",
                "👔 Chồng (nam) / Cấp trên / Quan chức",
                "👶 Con cái / Cháu / Thuốc men",
                "👨‍👩‍👧 Anh chị em / Bạn bè / Đồng nghiệp",
                "🤝 Người lạ / Đối phương / Đối thủ"
            ]
            qa_luc_than = st.selectbox(
                "🎯 Xem cho ai (Lục Thân → Dụng Thần):",
                _lt_options,
                key=f"qa_lt_{location_key}"
            )
            st.session_state['selected_doi_tuong'] = qa_luc_than

        with c_opt2:
            _lead_experts = [
                "🤖 Tự động triệu hồi Hội Đồng 40 Chuyên Gia theo câu hỏi",
                "Chart Interpreter AI (Đại sư Bàn Kỳ Môn)",
                "Luc Hao Expert (Bậc thầy Lục Hào Kinh Dịch)",
                "Mai Hoa Expert (Chuyên gia Mai Hoa Dịch Số)",
                "Wealth Advisor (Chuyên gia Tài lộc & Đầu tư)",
                "Career Advisor AI (Chuyên gia Sự nghiệp & Công danh)",
                "Relationship AI (Chuyên gia Tình duyên & Hôn nhân)",
                "Health Advisor (Chuyên gia Y Dịch & Sức khỏe)",
                "Direction Advisor (Chuyên gia Phương hướng & Phong thủy)",
                "Date Selector (Chuyên gia Trạch cát & Xem ngày)",
                "Prediction Validator (Chuyên gia Kiểm chứng Lịch sử & Thực chứng)",
            ]
            lead_expert = st.selectbox(
                "🧙 Chuyên Gia Chủ Trì (40 Chuyên Gia AI):",
                _lead_experts,
                key=f"qa_exp_{location_key}"
            )

        st.markdown("---")
        c_tv_opt, c_xn_opt = st.columns(2)
        with c_tv_opt:
            use_custom_tv = st.checkbox(
                "🔯 Nhập năm/ngày sinh cá nhân cho Tử Vi (Nếu tắt: tự lập Lá Số Tử Vi Thời Thần lúc hỏi)",
                value=st.session_state.get('qa_use_tu_vi', False),
                key=f"qa_tv_chk_{location_key}"
            )
            st.session_state['qa_use_tu_vi'] = use_custom_tv
            if use_custom_tv:
                try:
                    from tu_vi import lap_la_so, CHI as _TV_CHI_LIST
                    from xem_ngay_dep import solar2lunar as _tv_s2l_fn
                    _c_b1, _c_b2, _c_b3 = st.columns([2, 1.4, 1])
                    with _c_b1:
                        _b_date = st.date_input("Ngày sinh DL:", value=dt_module.date(1990, 1, 15), key=f"qa_tv_bd_{location_key}")
                    with _c_b2:
                        _b_gio = st.selectbox("Giờ sinh:", range(12), format_func=lambda i: f"{_TV_CHI_LIST[i]} ({i*2}h)", key=f"qa_tv_bg_{location_key}")
                    with _c_b3:
                        _b_gt = st.selectbox("Giới tính:", ["Nam", "Nữ"], key=f"qa_tv_bgt_{location_key}")
                    _d_al, _m_al, _y_al, _ = _tv_s2l_fn(_b_date.day, _b_date.month, _b_date.year)
                    st.session_state['tv_la_so'] = lap_la_so(_y_al, _m_al, _d_al, _b_gio, 'nam' if _b_gt == 'Nam' else 'nu')
                except Exception:
                    pass

        with c_xn_opt:
            use_custom_xn = st.checkbox(
                "📅 Chọn ngày & việc cụ thể cho Xem Ngày (Nếu tắt: tự chấm điểm ngày/giờ đang chọn)",
                value=st.session_state.get('qa_use_xem_ngay', False),
                key=f"qa_xn_chk_{location_key}"
            )
            st.session_state['qa_use_xem_ngay'] = use_custom_xn
            if use_custom_xn:
                try:
                    from xem_ngay_dep import danh_gia_ngay, solar2lunar as _xn_s2l_fn, VIEC_XEM_NGAY, _jdn as _jdn_acc
                    _c_x1, _c_x2 = st.columns(2)
                    with _c_x1:
                        _x_date = st.date_input("Ngày cần xem:", value=selected_datetime.date(), key=f"qa_xn_d_{location_key}")
                    with _c_x2:
                        _vk_list = list(VIEC_XEM_NGAY.keys())
                        _x_viec_idx = st.selectbox("Loại việc:", range(len(_vk_list)), format_func=lambda i: VIEC_XEM_NGAY[_vk_list[i]]["ten"], key=f"qa_xn_v_{location_key}")
                    _dx, _mx, _yx, _ = _xn_s2l_fn(_x_date.day, _x_date.month, _x_date.year)
                    _jv = _jdn_acc(_x_date.day, _x_date.month, _x_date.year)
                    _cans_x = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                    _chis_x = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                    st.session_state['xn_result'] = danh_gia_ngay(
                        _mx, _dx, _cans_x[(_jv + 9) % 10], _chis_x[(_jv + 1) % 12],
                        _vk_list[_x_viec_idx], ngay_dl=(_x_date.day, _x_date.month, _x_date.year)
                    )
                except Exception:
                    pass

    # ── Ô NHẬP CÂU HỎI DUY NHẤT ──
    _default_q = st.session_state.get('master_qa_prefill', '')
    user_question = st.text_area(
        "💬 Nhập câu hỏi của bạn (Bất kỳ chủ đề nào — Sự việc · Thời gian · Địa điểm · Con người · Đồ vật · Sức khỏe · Đất đai · Mồ mả · Thế giới):",
        value=_default_q,
        placeholder="Ví dụ: Năm nay gia đình tôi mua đất có thuận lợi không? / Đồ thất lạc đang ở hướng nào, bao giờ tìm thấy? / Sức khỏe bố mẹ thế nào?...",
        height=95,
        key=f"master_qa_text_{location_key}"
    )

    # ── NÚT BẤM HỢP NHẤT DUY NHẤT ──
    if st.button("🔮 PHÂN TÍCH HỢP NHẤT TOÀN BỘ 10 HỆ THỐNG QUẺ & AI CHUYÊN SÂU", key=f"master_qa_submit_{location_key}", type="primary", use_container_width=True):
        if user_question and len(user_question.strip()) >= 2:
            import time as _time_perf
            _t_start = _time_perf.perf_counter()
            st.session_state['master_qa_prefill'] = ''
            try:
                from free_ai_helper import FreeAIHelper
                _cand_keys = []
                for _k_src in [
                    st.session_state.get('gemini_key', ''),
                    st.session_state.get('api_key', ''),
                    st.session_state.get('_resolved_api_key', ''),
                ]:
                    if _k_src and str(_k_src).strip():
                        _cand_keys.append(str(_k_src).strip())
                _gh_obj = st.session_state.get('gemini_helper')
                if _gh_obj:
                    if getattr(_gh_obj, 'api_keys', None):
                        _cand_keys.extend([str(k).strip() for k in _gh_obj.api_keys if k])
                    elif getattr(_gh_obj, 'api_key', None):
                        _cand_keys.append(str(_gh_obj.api_key).strip())
                try:
                    _sec_k = st.secrets.get('GEMINI_API_KEY', '')
                    if _sec_k:
                        _cand_keys.append(str(_sec_k).strip())
                except Exception:
                    pass
                _api_key = ",".join(list(dict.fromkeys([k for k in _cand_keys if k])))
                if '_cached_free_ai_helper' not in st.session_state or st.session_state['_cached_free_ai_helper'] is None:
                    st.session_state['_cached_free_ai_helper'] = FreeAIHelper(api_key=_api_key)
                offline_ai = st.session_state['_cached_free_ai_helper']
                if _api_key:
                    offline_ai._api_key = _api_key
                if True:

                    dt_now = dt_module.datetime.now(vn_tz) if use_current_time else selected_datetime
                    _use_rnd = st.session_state.get('random_hexagram_mode', False)
                    _cast_seq = int(st.session_state.get('_cast_seq_counter', 0)) + 1
                    st.session_state['_cast_seq_counter'] = _cast_seq
                    _prev_tuple = st.session_state.get('_last_cast_tuple', None)
                    _prev_q_text = st.session_state.get('_last_cast_q_text', '')
                    _q_clean_now = user_question.strip()
                    _is_repeat_same_q = (_q_clean_now.lower() == str(_prev_q_text).strip().lower())
                    st.session_state['_last_cast_q_text'] = _q_clean_now

                    _cans_rq = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
                    _chis_rq = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                    chart_for_q = dict(st.session_state.get('chart_data') or {})

                    # 1. V110.0: GIEO QUẺ ĐỒNG BỘ 100% MAI HOA + LỤC HÀO + KỲ MÔN (KHÔNG TRÙNG LẶP GIỮA CÁC CÂU HỎI)
                    if _use_rnd:
                        try:
                            import secrets as _sec_mod
                            _sys_rng = _sec_mod.SystemRandom()
                            mai_hoa_for_q = tinh_qua_ngau_nhien(prev_tuple=_prev_tuple)
                            mai_hoa_for_q['interpretation'] = giai_qua(mai_hoa_for_q, selected_topic)
                            mai_hoa_for_q['_random_cast'] = True
                            st.session_state.mai_hoa_result = mai_hoa_for_q

                            _u_rnd = mai_hoa_for_q['upper']
                            _l_rnd = mai_hoa_for_q['lower']
                            _d_rnd = mai_hoa_for_q['dong_hao']
                            st.session_state['_last_cast_tuple'] = (_u_rnd, _l_rnd, _d_rnd)

                            # Tạo cặp Can-Chi hợp lệ trong 60 Hoa Giáp (Can Dương đi với Chi Dương, Can Âm đi với Chi Âm)
                            def _roll_valid_canchi():
                                _ci = _sys_rng.randint(0, 9)
                                _chi_candidates = [idx for idx in range(12) if (idx % 2) == (_ci % 2)]
                                _chi_i = _sys_rng.choice(_chi_candidates)
                                return _cans_rq[_ci], _chis_rq[_chi_i]

                            _r_can_ngay, _r_chi_ngay = _roll_valid_canchi()
                            _r_can_gio, _r_chi_gio = _roll_valid_canchi()
                            _r_can_thang = chart_for_q.get('can_thang') or _cans_rq[(_u_rnd + _l_rnd) % 10]
                            _r_chi_thang = chart_for_q.get('chi_thang') or _chis_rq[(dt_now.month + 1) % 12]

                            # Lục Hào dùng ĐÚNG CÙNG (upper, lower, dong_hao) với Mai Hoa -> Đồng bộ 100%!
                            luc_hao_for_q = lap_qua_luc_hao(
                                dt_now.year, dt_now.month, dt_now.day, dt_now.hour,
                                topic=selected_topic,
                                can_ngay=_r_can_ngay,
                                chi_ngay=_r_chi_ngay,
                                can_thang=_r_can_thang,
                                chi_thang=_r_chi_thang,
                                upper_override=_u_rnd,
                                lower_override=_l_rnd,
                                moving_override=_d_rnd,
                            )
                            luc_hao_for_q['_random_cast'] = True
                            st.session_state.luc_hao_result = luc_hao_for_q

                            # Đồng bộ Bàn Kỳ Môn 9 Cung ngẫu nhiên theo quẻ vừa gieo
                            try:
                                from qmdg_data import an_bai_luc_nghi as _ab_rnd, lap_ban_qmdg as _lb_rnd
                                _r_cuc = ((_u_rnd + _l_rnd + _d_rnd - 1) % 9) + 1
                                _r_duong = bool((_u_rnd + _d_rnd) % 2 == 1)
                                _r_stars = ["Thiên Bồng", "Thiên Nhuế", "Thiên Xung", "Thiên Phụ", "Thiên Cầm", "Thiên Tâm", "Thiên Trụ", "Thiên Nhậm", "Thiên Anh"]
                                _r_doors = ["Hưu Môn", "Tử Môn", "Thương Môn", "Đỗ Môn", "Khai Môn", "Kinh Môn", "Sinh Môn", "Cảnh Môn"]
                                _r_tp = _r_stars[(_u_rnd - 1) % len(_r_stars)]
                                _r_ts = _r_doors[(_l_rnd - 1) % len(_r_doors)]
                                _r_dia = _ab_rnd(_r_cuc, _r_duong)
                                _r_tb, _r_ctb, _r_nb, _r_sb, _ = _lb_rnd(_r_cuc, _r_tp, _r_ts, _r_can_gio, _r_chi_gio, _r_duong)
                                chart_for_q.update({
                                    'thien_ban': _r_tb,
                                    'can_thien_ban': _r_ctb,
                                    'nhan_ban': _r_nb,
                                    'than_ban': _r_sb,
                                    'dia_can': _r_dia,
                                    'dia_ban': _r_dia,
                                    'can_ngay': _r_can_ngay,
                                    'chi_ngay': _r_chi_ngay,
                                    'can_gio': _r_can_gio,
                                    'chi_gio': _r_chi_gio,
                                    'cuc': _r_cuc,
                                    'is_duong_don': _r_duong,
                                    'am_duong_don': f"{'Dương' if _r_duong else 'Âm'} Độn {_r_cuc} Cục",
                                    'truc_phu': _r_tp,
                                    'truc_su': _r_ts,
                                    '_random_cast': True,
                                })
                                st.session_state.chart_data = chart_for_q
                            except Exception:
                                pass
                            st.toast(
                                f"🎲 Đã gieo quẻ ngẫu nhiên mới: {mai_hoa_for_q.get('ten')} ➔ {mai_hoa_for_q.get('ten_qua_bien')} (Động hào {_d_rnd})!",
                                icon="🎲"
                            )
                        except Exception:
                            mai_hoa_for_q = st.session_state.get('mai_hoa_result')
                            luc_hao_for_q = st.session_state.get('luc_hao_result')
                    else:
                        # Chế độ Thời Gian + Thanh Âm Câu Hỏi (Đa Vấn Nhất Thời Chiêm Pháp):
                        # Mỗi câu hỏi khác nhau (hoặc khi bấm hỏi lại) sẽ cộng hưởng chữ & khắc/phút để sinh quẻ riêng,
                        # tuyệt đối không bị đơ/lặp lại cùng 1 quẻ cho nhiều câu hỏi trong cùng khung giờ!
                        try:
                            _q_salt = _cast_seq if _is_repeat_same_q else 0
                            mai_hoa_for_q = tinh_qua_theo_thoi_gian(
                                dt_now.year, dt_now.month, dt_now.day, dt_now.hour,
                                minute=dt_now.minute, second=dt_now.second,
                                question_text=_q_clean_now, cast_salt=_q_salt
                            )
                            # Nếu câu hỏi mới vô tình trùng bộ (upper, lower, dong_hao) với câu vừa hỏi trước đó, tự động nhảy sang biến số kế tiếp
                            while _prev_tuple and (mai_hoa_for_q['upper'], mai_hoa_for_q['lower'], mai_hoa_for_q['dong_hao']) == tuple(_prev_tuple) and _q_salt < _cast_seq + 8:
                                _q_salt += 1
                                mai_hoa_for_q = tinh_qua_theo_thoi_gian(
                                    dt_now.year, dt_now.month, dt_now.day, dt_now.hour,
                                    minute=dt_now.minute, second=dt_now.second,
                                    question_text=_q_clean_now, cast_salt=_q_salt
                                )
                            mai_hoa_for_q['interpretation'] = giai_qua(mai_hoa_for_q, selected_topic)
                            st.session_state.mai_hoa_result = mai_hoa_for_q

                            _u_q = mai_hoa_for_q['upper']
                            _l_q = mai_hoa_for_q['lower']
                            _d_q = mai_hoa_for_q['dong_hao']
                            st.session_state['_last_cast_tuple'] = (_u_q, _l_q, _d_q)

                            luc_hao_for_q = lap_qua_luc_hao(
                                dt_now.year, dt_now.month, dt_now.day, dt_now.hour,
                                topic=selected_topic,
                                can_ngay=chart_for_q.get('can_ngay', 'Giáp'),
                                chi_ngay=chart_for_q.get('chi_ngay', 'Tý'),
                                can_thang=chart_for_q.get('can_thang', 'Giáp'),
                                chi_thang=chart_for_q.get('chi_thang', 'Tý'),
                                upper_override=_u_q,
                                lower_override=_l_q,
                                moving_override=_d_q,
                                question_text=_q_clean_now,
                                minute=dt_now.minute,
                                second=dt_now.second,
                                cast_salt=_q_salt,
                            )
                            st.session_state.luc_hao_result = luc_hao_for_q

                            # Hoạt Lạc Kỳ Môn theo Quái Số câu hỏi khi xem nhiều câu trong cùng 1 giờ (tránh kẹt cứng 1 bàn Phục Ngâm)
                            try:
                                from qmdg_data import an_bai_luc_nghi as _ab_q, lap_ban_qmdg as _lb_q
                                _base_cuc = int(chart_for_q.get('cuc') or 5)
                                _q_cuc = ((_base_cuc + _u_q + _l_q - 1) % 9) + 1
                                _q_duong = bool(chart_for_q.get('is_duong_don', True))
                                _q_stars = ["Thiên Bồng", "Thiên Nhuế", "Thiên Xung", "Thiên Phụ", "Thiên Cầm", "Thiên Tâm", "Thiên Trụ", "Thiên Nhậm", "Thiên Anh"]
                                _q_doors = ["Hưu Môn", "Tử Môn", "Thương Môn", "Đỗ Môn", "Khai Môn", "Kinh Môn", "Sinh Môn", "Cảnh Môn"]
                                _q_tp = _q_stars[(_u_q + _d_q - 1) % len(_q_stars)]
                                _q_ts = _q_doors[(_l_q + _d_q - 1) % len(_q_doors)]
                                _q_can_gio = _cans_rq[(_cans_rq.index(chart_for_q.get('can_gio', 'Giáp')) + _u_q + _l_q) % 10] if chart_for_q.get('can_gio') in _cans_rq else chart_for_q.get('can_gio', 'Bính')
                                _q_chi_gio = _chis_rq[(_chis_rq.index(chart_for_q.get('chi_gio', 'Tý')) + _d_q) % 12] if chart_for_q.get('chi_gio') in _chis_rq else chart_for_q.get('chi_gio', 'Ngọ')
                                _q_dia = _ab_q(_q_cuc, _q_duong)
                                _q_tb, _q_ctb, _q_nb, _q_sb, _ = _lb_q(_q_cuc, _q_tp, _q_ts, _q_can_gio, _q_chi_gio, _q_duong)
                                chart_for_q.update({
                                    'thien_ban': _q_tb,
                                    'can_thien_ban': _q_ctb,
                                    'nhan_ban': _q_nb,
                                    'than_ban': _q_sb,
                                    'dia_can': _q_dia,
                                    'dia_ban': _q_dia,
                                    'cuc': _q_cuc,
                                    'am_duong_don': f"{'Dương' if _q_duong else 'Âm'} Độn {_q_cuc} Cục",
                                    'truc_phu': _q_tp,
                                    'truc_su': _q_ts,
                                })
                                st.session_state.chart_data = chart_for_q
                            except Exception:
                                pass
                        except Exception:
                            mai_hoa_for_q = st.session_state.get('mai_hoa_result')
                            luc_hao_for_q = st.session_state.get('luc_hao_result')

                    # 2. Chỉ truyền lá số Tử Vi / Xem Ngày tùy chỉnh nếu người dùng chủ động bật;
                    #    còn lại để FreeAIHelper tự động tính theo đúng ngữ cảnh câu hỏi (chữa bệnh, cưới hỏi, năm sinh trong câu hỏi...)
                    _has_personal_tv = bool(st.session_state.get('qa_use_tu_vi', False))
                    _tv_data_q = st.session_state.get('tv_la_so') if _has_personal_tv else None
                    _has_custom_xn = bool(st.session_state.get('qa_use_xem_ngay', False))
                    _xn_data_q = st.session_state.get('xn_result') if _has_custom_xn else None

                    # 3. Gọi answer_question theo đúng Phân Khu Chuyên Biệt (V106.0)
                    _q_to_send = user_question.strip()
                    if "Mảng Riêng 1" in _domain_mode and "cả cuộc đời" not in _q_to_send.lower():
                        _q_to_send = f"[XEM RIÊNG CẢ CUỘC ĐỜI - TỬ VI ĐẨU SỐ] {_q_to_send}"
                    elif "Mảng Riêng 2" in _domain_mode and "quốc gia" not in _q_to_send.lower():
                        _q_to_send = f"[XEM RIÊNG VẬN QUỐC GIA & THẾ GIỚI - THÁI ẤT THẦN SỐ] {_q_to_send}"
                    elif "Mảng Riêng 3" in _domain_mode and "chọn ngày" not in _q_to_send.lower():
                        _q_to_send = f"[XEM RIÊNG CHỌN NGÀY GIỜ ĐẸP - TRẠCH NHẬT] {_q_to_send}"
                    if lead_expert and not lead_expert.startswith("🤖"):
                        _exp_tag = lead_expert.split("(")[0].strip()
                        _q_to_send = f"[{_exp_tag}] {_q_to_send}"

                    _cache_store = st.session_state.setdefault('_qa_fast_cache', {})
                    _want_online = st.session_state.get('qa_use_cloud_llm', True)
                    _hex_sig_q = f"{mai_hoa_for_q.get('ten','')}_{mai_hoa_for_q.get('ten_qua_bien','')}_{mai_hoa_for_q.get('dong_hao','')}_{chart_for_q.get('cuc','')}_{chart_for_q.get('can_ngay','')}_{chart_for_q.get('chi_ngay','')}"
                    _cache_key = f"{_CODE_BUILD_VERSION}|{_q_to_send}|{_hex_sig_q}|{dt_now.strftime('%Y%m%d%H')}|{st.session_state.get('selected_doi_tuong','')}|{_use_rnd}|{_has_personal_tv}|{_has_custom_xn}|{_want_online}"
                    if not _use_rnd and not _is_repeat_same_q and _cache_key in _cache_store:
                        combined_answer = _cache_store[_cache_key]
                    else:
                        combined_answer = offline_ai.answer_question(
                            _q_to_send,
                            chart_data=chart_for_q,
                            topic=None,
                            selected_subject=st.session_state.get('selected_doi_tuong', '👤 Bản thân'),
                            mai_hoa_data=mai_hoa_for_q,
                            luc_hao_data=luc_hao_for_q,
                            tu_vi_data=_tv_data_q,
                            xem_ngay_data=_xn_data_q,
                            has_personal_tv=_has_personal_tv,
                            has_custom_xn=_has_custom_xn,
                            use_online_api=_want_online,
                        )
                        # Chỉ cache khi kết quả đã có Online (nếu bật Online) hoặc khi chạy chế độ Offline
                        if not _use_rnd and (not _want_online or 'KẾT LUẬN AI ONLINE' in str(combined_answer)):
                            if len(_cache_store) > 30:
                                _cache_store.clear()
                            _cache_store[_cache_key] = combined_answer

                    _elapsed_sec = _time_perf.perf_counter() - _t_start
                    st.session_state['master_qa_last_result'] = combined_answer
                    st.session_state['master_qa_last_question'] = user_question.strip()
                    st.session_state['master_qa_elapsed_ms'] = _elapsed_sec * 1000.0

                    if 'chat_history' not in st.session_state:
                        st.session_state.chat_history = []
                    st.session_state.chat_history.append({'role': 'user', 'content': user_question.strip()})
                    st.session_state.chat_history.append({'role': 'assistant', 'content': combined_answer})
                    if len(st.session_state.chat_history) > 20:
                        st.session_state.chat_history = st.session_state.chat_history[-20:]

                    # Tự động lưu thêm vào kho chủ đề
                    try:
                        from ai_modules.shard_manager import add_entry
                        if len(user_question.strip()) > 5:
                            topic_title = user_question.strip()[:100]
                            add_entry(
                                title=topic_title,
                                content=f"Câu hỏi: {user_question}\n\nTrả lời AI (tóm tắt): {str(combined_answer)[:500]}",
                                category="Kiến Thức",
                                source="Master Unified Q&A"
                            )
                    except Exception:
                        pass

            except Exception as e:
                st.error(f"❌ Lỗi phân tích: {str(e)}")
        else:
            st.warning("⚠️ Vui lòng nhập câu hỏi vào ô bên trên.")

    # ── HIỂN THỊ KẾT QUẢ PHÂN TÍCH HỢP NHẤT ──
    if st.session_state.get('master_qa_last_result'):
        _ms = st.session_state.get('master_qa_elapsed_ms', 40.0)
        st.markdown(
            f"<div style='background:rgba(16,185,129,0.12);border:1px solid #10b981;padding:6px 14px;border-radius:8px;margin-top:8px;font-size:0.85rem;color:#6ee7b7;'>"
            f"⚡ <b>Tốc độ giải mã Siêu Tốc (V106.0): {_ms:.0f} ms ({_ms/1000.0:.2f} giây)</b> — Đã phân khu: <b>Phần I (4 Phương Pháp Chuẩn: Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản)</b> & <b>Phần II (Các Mảng Chuyên Biệt Độc Lập)</b>"
            f"</div>",
            unsafe_allow_html=True
        )
        display_ai_result(st.session_state['master_qa_last_result'], key_prefix=f"master_{location_key}")

    # ── HIỂN THỊ TRỰC TIẾP PHẦN II: 3 TAB PHÂN KHU CHUYÊN BIỆT ĐỘC LẬP NGAY DƯỚI Ô HỎI ĐÁP (V106.0) ──
    with st.expander("🏛️ MỞ XEM TRỰC TIẾP PHẦN II — CÁC PHÂN KHU CHUYÊN BIỆT ĐỘC LẬP (Tử Vi Cả Cuộc Đời · Thái Ất Quốc Gia · Xem Ngày Giờ Đẹp)", expanded=True):
        _tab_tv, _tab_ta, _tab_xn = st.tabs([
            "🔯 1. Tử Vi Đẩu Số (Chuyên Xem Cả Cuộc Đời)",
            "⚔️ 2. Thái Ất Thần Số (Chuyên Xem Vận Quốc Gia & Thế Giới)",
            "📅 3. Xem Ngày Đẹp & Đại Lục Nhâm (Chuyên Xem Chọn Ngày Giờ & Lộ Trình)"
        ])
        _cd_now = st.session_state.get('chart_data', {}) or {}
        try:
            from world_class_methods import _extract_full_18_systems_live
            _live_spec = _extract_full_18_systems_live(_cd_now, 1)
        except Exception:
            _live_spec = {}
        with _tab_tv:
            st.markdown(
                f"<div style='padding:12px 16px;background:rgba(88,28,135,0.25);border-radius:12px;border-left:4px solid #c084fc;color:#f3e8ff;line-height:1.6;'>"
                f"<b>🔯 MẢNG CHUYÊN BIỆT 1 — TỬ VI ĐẨU SỐ (CHỈ XEM RIÊNG VỀ CẢ CUỘC ĐỜI & MỆNH CỤC 12 CUNG):</b><br>"
                f"• <b>Vai trò độc lập:</b> Tử Vi Đẩu Số dùng để luận giải <b>tổng quan Cả Cuộc Đời (Mệnh, Thân, Cục, Phúc Đức, Quan Lộc, Tài Bạch, Phu Thê, Tử Tức, Đại Vận 10 năm)</b>, hoàn toàn tách biệt và không chấm điểm chồng chéo vào các câu hỏi sự việc hàng ngày của 4 phương pháp quẻ.<br>"
                f"• <b>Bản đồ Tinh Bàn hiện tại:</b> {_live_spec.get('tv_summary', 'Đang hội Cát tinh thủ Mệnh/Thân')} · Nạp Âm: <b>{_live_spec.get('nap_am_ngay', '')}</b>.<br>"
                f"• <i>💡 Mẹo: Bạn có thể mở mục '⚙️ Tùy chọn nâng cao' bên trên để nhập Ngày Giờ Sinh cá nhân hoặc chọn mục '🔯 Tử Vi Đẩu Số' ở thanh bên trái để xem chi tiết 12 cung cả cuộc đời.</i>"
                f"</div>",
                unsafe_allow_html=True
            )
        with _tab_ta:
            st.markdown(
                f"<div style='padding:12px 16px;background:rgba(127,29,29,0.25);border-radius:12px;border-left:4px solid #f87171;color:#fee2e2;line-height:1.6;'>"
                f"<b>⚔️ MẢNG CHUYÊN BIỆT 2 — THÁI ẤT THẦN SỐ (CHỈ XEM RIÊNG VỀ VẬN QUỐC GIA, THẾ GIỚI & VĨ MÔ):</b><br>"
                f"• <b>Vai trò độc lập:</b> Thái Ất Thần Số là môn đứng đầu Tam Thức về <b>Quốc vận, Thời cuộc Thế giới, Kinh tế Vĩ mô, Khí hậu & Biến động lớn của Quốc gia</b> — tuyệt đối không dùng để phán xét việc cá nhân hay gia đình.<br>"
                f"• <b>Cục diện Quốc Vận & Đại Cục Năm/Tháng:</b> {_live_spec.get('ta_summary', 'Chủ – Khách cân bằng')}.<br>"
                f"• <b>Thế Chủ – Khách Vĩ Mô:</b> <b>{_live_spec.get('ta_chu_khach', 'Chủ Khách cân bằng')}</b>."
                f"</div>",
                unsafe_allow_html=True
            )
        with _tab_xn:
            st.markdown(
                f"<div style='padding:12px 16px;background:rgba(19,78,74,0.28);border-radius:12px;border-left:4px solid #2dd4bf;color:#ccfbf1;line-height:1.6;'>"
                f"<b>📅 MẢNG CHUYÊN BIỆT 3 — TRẠCH NHẬT XEM NGÀY ĐẸP & ĐẠI LỤC NHÂM (CHỈ XEM RIÊNG VỀ CHỌN NGÀY GIỜ & LỘ TRÌNH 3 BƯỚC):</b><br>"
                f"• <b>Trạch Nhật 12 Trực ({_live_spec.get('truc_name', 'Trực Thành')}):</b> {_live_spec.get('truc_meaning', 'Thuận lợi cho việc khởi sự, giao dịch')} — <i>Chỉ dùng riêng khi bạn cần chọn ngày giờ Khai trương, Động thổ, Xuất hành, Cưới hỏi.</i><br>"
                f"• <b>Đại Lục Nhâm Tam Truyền (Lộ trình 3 giai đoạn):</b> {_live_spec.get('dln_summary', 'Sơ truyền ➔ Trung truyền ➔ Mạt truyền')}."
                f"</div>",
                unsafe_allow_html=True
            )

    # ── LỊCH SỬ HỘI THOẠI GỌN GÀNG ──
    if st.session_state.get('chat_history') and len(st.session_state.chat_history) >= 2:
        with st.expander(f"📜 Lịch sử câu hỏi trong phiên ({len(st.session_state.chat_history)//2} câu)", expanded=False):
            for msg in st.session_state.chat_history[-10:]:
                if msg['role'] == 'user':
                    st.markdown(f"**👤 Bạn:** {msg['content'][:250]}")
                else:
                    st.caption("🤖 Đã trả lời bằng Hệ thống Hợp Nhất 10 Phương Pháp.")
            if st.button("🗑️ Xóa lịch sử hội thoại", key=f"clr_hist_{location_key}"):
                st.session_state.chat_history = []
                st.session_state.pop('master_qa_last_result', None)
                st.rerun()

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
            
            # V42.2 FIX: Tuần Không & Dịch Mã tính theo Can+Chi NGÀY (chuẩn QMDG)
            # KV theo Chi Giờ là sai — phải dùng Chi Ngày làm cơ sở tra bảng
            khong_vong = tinh_khong_vong(params['can_ngay'], params['chi_ngay'])
            dich_ma = tinh_dich_ma(params['chi_ngay'])
            
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
                'chi_thang': params.get('chi_thang', 'N/A'),
                'can_nam': params.get('can_nam', 'N/A'),
                'chi_nam': params.get('chi_nam', 'N/A'),
                'dia_ban': dia_can,
                'khong_vong': khong_vong,
                'dich_ma': dich_ma,
                'tiet_khi': params.get('tiet_khi', ''),
                'cuc': params.get('cuc', 1),
                'is_duong_don': params.get('is_duong_don', True),
                'am_duong_don': f"{'Dương' if params.get('is_duong_don', True) else 'Âm'} Độn {params.get('cuc', 1)} Cục",
                'nguyen': params.get('nguyen', ''),
                'phu_dau': params.get('phu_dau', ''),
                'truc_phu': params.get('truc_phu', ''),
                'truc_su': params.get('truc_su', ''),
                'year': selected_datetime.year,
                'month': selected_datetime.month,
                'day': selected_datetime.day,
                'hour': selected_datetime.hour,
                'minute': selected_datetime.minute,
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

                        # Element Styles & Aesthetics (Restored Color Scheme)
                        element_configs = {
                            "Mộc": {
                                "border": "#10b981", "icon": "🌿", "img": "moc.png",
                                "overlay": "rgba(22, 163, 74, 0.6)", "hex": "#16a34a" # Green
                            },
                            "Hỏa": {
                                "border": "#ef4444", "icon": "🔥", "img": "hoa.png",
                                "overlay": "rgba(220, 38, 38, 0.6)", "hex": "#dc2626" # Red
                            },
                            "Thổ": {
                                "border": "#f59e0b", "icon": "⛰️", "img": "tho.png",
                                "overlay": "rgba(180, 83, 9, 0.6)", "hex": "#d97706" # Earth
                            },
                            "Kim": {
                                "border": "#94a3b8", "icon": "⚔️", "img": "kim.png",
                                "overlay": "rgba(71, 85, 105, 0.6)", "hex": "#64748b" # Metal
                            },
                            "Thủy": {
                                "border": "#3b82f6", "icon": "💧", "img": "thuy.png",
                                "overlay": "rgba(37, 99, 235, 0.6)", "hex": "#2563eb" # Water
                            }
                        }.get(hanh, {
                            "border": "#475569", "icon": "✨", "img": "tho.png",
                            "overlay": "rgba(71, 85, 105, 0.6)", "hex": "#475569"
                        })

                        # Base64 Background Logic (MODIFIED: ROBUST FALLBACK - NO SHORTHAND CONFLICT)
                        bg_path = os.path.join(os.path.dirname(__file__), "web", "static", "img", "elements", element_configs.get('img', 'tho.png'))
                        bg_base64 = get_base64_image(bg_path)
                        
                        fallback_color = element_configs.get('hex', '#334155')
                        overlay_color = element_configs.get('overlay', 'rgba(0,0,0,0.5)')
                        
                        if bg_base64:
                            # Use explicit background-image to avoid resetting background-color
                            # We use linear-gradient AND url() in the same background-image property
                            bg_style = f"background-image: linear-gradient(180deg, {overlay_color} 0%, rgba(0,0,0,0.1) 100%), url('data:image/png;base64,{bg_base64}'); background-size: cover; background-position: center;"
                        else:
                            bg_style = f"background: linear-gradient(135deg, {fallback_color} 0%, #1e293b 100%);"

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

                        # 4. V12.2: 六甲遁甲 — Can Giáp ẨN ở cung nào
                        try:
                            _cn = params.get('can_ngay', '')
                            if _cn == 'Giáp':
                                _THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
                                _DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                                _LUC_GIAP = {'Tý': 'Mậu', 'Tuất': 'Kỷ', 'Thân': 'Canh', 'Ngọ': 'Tân', 'Thìn': 'Nhâm', 'Dần': 'Quý'}
                                _chn = params.get('chi_ngay', '')
                                if _chn in _DIA_CHI:
                                    _ci = _THIEN_CAN.index(_cn)
                                    _chi = _DIA_CHI.index(_chn)
                                    _tuan_chi = _DIA_CHI[(_chi - _ci) % 12]
                                    _hidden = _LUC_GIAP.get(_tuan_chi, 'Mậu')
                                    # Kiểm tra cung hiện tại có can_thien == hidden can không
                                    if can_thien == _hidden:
                                        m_html.append(f'<div class="marker-badge" style="background:#7c3aed;color:white;">🔮 Giáp Ẩn (Giáp {_tuan_chi})</div>')
                        except Exception:
                            pass

                        marker_display_html = "".join(m_html)

                        # Palace Name & Alignment Refinement
                        p_full_name = f"{palace_num} {QUAI_TUONG.get(palace_num, '')}"
                        if palace_num == 5: p_full_name = "5 Trung Cung"

                        # Status Badge
                        status_badge = f'<span class="status-badge" style="background: {strength_color}; color: white;">{strength}</span>'

                        # --- RENDER TRADITIONAL CORNER LAYOUT (NO LABELS) ---
                        palace_html = f"""<div class="palace-3d animated-panel">
<div class="palace-inner {'dung-than-active' if has_dung_than else ''}" style="background-color: {fallback_color}; {bg_style} border: {border_width} solid {element_configs['border']}; min-height: 320px; position: relative;">
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
                            
                            # V13.0: Removed per-palace AI button (saves up to 9 API calls!)
                            # User should use LỤC THUẬT HỢP NHẤT for comprehensive analysis
                            st.caption("💡 Dùng tab '🤖 Hỏi Gemini AI' → LỤC THUẬT HỢP NHẤT để phân tích tổng hợp")

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
                                    # V13.0: Removed per-can AI button (saves API quota)
                                    pass
                            
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
                            # V13.0: Removed AI So Sánh button (saves API quota)
                            # User should use LỤC THUẬT HỢP NHẤT instead
                            st.caption("💡 Dùng '🌟 LỤC THUẬT HỢP NHẤT' trong tab Hỏi Gemini AI để phân tích chuyên sâu")
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
        
        # ===== HỆ THỐNG HỎI ĐÁP HỢP NHẤT DUY NHẤT (1 Ô HỎI ĐÁP) =====
        if st.session_state.chart_data:
            st.markdown("---")
            render_master_unified_qa_box(location_key="kymon_main")


elif st.session_state.current_view == "mai_hoa":
    st.markdown("## 🌸 MAI HOA DỊCH SỐ - TAM TÀI HỢP NHẤT")
    
    if not USE_MAI_HOA:
        st.error("❌ Module Mai Hoa Dịch Số không khả dụng.")
        st.stop()
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")

    # V42.9.9i: Sử dụng thời gian được chọn từ sidebar
    dt = selected_datetime
    
    # V110.0: Hiển thị quẻ đang hoạt động (Ngẫu nhiên hoặc Động tâm theo câu hỏi) + Nút Gieo Ngẫu Nhiên Mới
    _mh_existing = st.session_state.get('mai_hoa_result')
    if st.button("🎲 Gieo Quẻ Ngẫu Nhiên Mới (Đồng bộ Mai Hoa & Lục Hào)", key="btn_mh_tab_rnd"):
        _prev_t = st.session_state.get('_last_cast_tuple')
        res = tinh_qua_ngau_nhien(prev_tuple=_prev_t)
        res['interpretation'] = giai_qua(res, selected_topic)
        res['_random_cast'] = True
        st.session_state.mai_hoa_result = res
        st.session_state['_last_cast_tuple'] = (res['upper'], res['lower'], res['dong_hao'])
        st.session_state.luc_hao_result = lap_qua_luc_hao(
            dt.year, dt.month, dt.day, dt.hour,
            topic=selected_topic,
            upper_override=res['upper'],
            lower_override=res['lower'],
            moving_override=res['dong_hao'],
        )
        st.session_state.luc_hao_result['_random_cast'] = True
    elif _mh_existing and isinstance(_mh_existing, dict) and (_mh_existing.get('_random_cast') or _mh_existing.get('cast_mode') == 'question_time_resonance'):
        res = _mh_existing
        st.info(f"🎲 Đang hiển thị quẻ vừa gieo: **{res.get('ten')} ➔ {res.get('ten_qua_bien')} (Động hào {res.get('dong_hao')})**.")
    else:
        st.info(f"🕒 Giờ gieo quẻ: {dt.strftime('%H:%M - %d/%m/%Y')}.")
        res = tinh_qua_theo_thoi_gian(dt.year, dt.month, dt.day, dt.hour)
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

        # V13.0: Removed AI Luận Mai Hoa button (dùng LỤC THUẬT HỢP NHẤT thay thế)
        st.info("💡 Để AI luận quẻ chuyên sâu → sang tab **'🤖 Hỏi Gemini AI'** → **'🌟 LỤC THUẬT HỢP NHẤT'**")

        st.markdown('<div class="footer-stamp">Copyright © 2026 MAI HOA DICH SO PRO</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.current_view == "luc_hao":
    st.markdown("## ☯️ LỤC HÀO KINH DỊCH - CHUYÊN SÂU")
    
    if not USE_LUC_HAO:
        st.error("❌ Module Lục Hào Kinh Dịch không khả dụng.")
        st.stop()
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")

    show_debug_ih = st.checkbox("🐛 Chế độ Kiểm tra Dữ liệu", key="debug_iching_mode")

    # V42.9.9i: Sử dụng thời gian được chọn từ sidebar
    dt = selected_datetime
    can_ngay = params.get('can_ngay', 'Giáp') if params else "Giáp"
    chi_ngay = params.get('chi_ngay', 'Tý') if params else "Tý"
    can_gio = params.get('can_gio', '') if params else ""
    chi_gio = params.get('chi_gio', '') if params else ""
    can_thang = params.get('can_thang', '') if params else ""
    chi_thang = params.get('chi_thang', '') if params else ""
    can_nam = params.get('can_nam', '') if params else ""
    chi_nam = params.get('chi_nam', '') if params else ""
    tiet_khi = params.get('tiet_khi', '') if params else ""
    
    # Nhật Thần & Nguyệt Lệnh
    nhat_than = f"{chi_ngay}"
    nguyet_lenh = f"{chi_thang}"
    
    # V110.0: Hiển thị quẻ Lục Hào đang hoạt động (Ngẫu nhiên hoặc Động tâm theo câu hỏi) + Nút Gieo Ngẫu Nhiên Mới
    _lh_existing = st.session_state.get('luc_hao_result')
    if st.button("🎲 Gieo Quẻ Lục Hào Ngẫu Nhiên Mới (Đồng bộ Mai Hoa & Lục Hào)", key="btn_lh_tab_rnd"):
        _prev_t = st.session_state.get('_last_cast_tuple')
        _mh_r = tinh_qua_ngau_nhien(prev_tuple=_prev_t)
        _mh_r['interpretation'] = giai_qua(_mh_r, selected_topic)
        _mh_r['_random_cast'] = True
        st.session_state.mai_hoa_result = _mh_r
        st.session_state['_last_cast_tuple'] = (_mh_r['upper'], _mh_r['lower'], _mh_r['dong_hao'])
        st.session_state.luc_hao_result = lap_qua_luc_hao(
            dt.year, dt.month, dt.day, dt.hour,
            topic=selected_topic,
            can_ngay=can_ngay,
            chi_ngay=chi_ngay,
            can_thang=can_thang,
            chi_thang=chi_thang,
            upper_override=_mh_r['upper'],
            lower_override=_mh_r['lower'],
            moving_override=_mh_r['dong_hao'],
        )
        st.session_state.luc_hao_result['_random_cast'] = True
    elif _lh_existing and isinstance(_lh_existing, dict) and (_lh_existing.get('_random_cast') or st.session_state.get('mai_hoa_result', {}).get('cast_mode') == 'question_time_resonance'):
        st.info("🎲 Đang hiển thị quẻ Lục Hào vừa gieo (đồng bộ 100% với Mai Hoa Dịch Số).")
    else:
        try:
            st.session_state.luc_hao_result = lap_qua_luc_hao(
                dt.year, dt.month, dt.day, dt.hour,
                topic=selected_topic,
                can_ngay=can_ngay,
                chi_ngay=chi_ngay,
                can_thang=can_thang,
                chi_thang=chi_thang
            )
        except Exception as e:
            st.error(f"Lỗi lập quẻ Lục Hào: {e}")

    if 'luc_hao_result' in st.session_state:
        res = st.session_state.luc_hao_result
        
        # V42.9.42 Fix: Read actual can/chi from the result (vital for random cast)
        _d_can_ngay = res.get('can_ngay', can_ngay)
        _d_chi_ngay = res.get('chi_ngay', chi_ngay)
        _d_can_thang = res.get('can_thang', can_thang)
        _d_chi_thang = res.get('chi_thang', chi_thang)
        _d_nhat_than = res.get('nhat_than', f"{_d_chi_ngay}")
        _d_nguyet_lenh = res.get('nguyet_lenh', f"{_d_chi_thang}")
        
        # ========== COMPACT HEADER (giống xinhdich.com) ==========
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30,27,75,0.9), rgba(22,33,62,0.9)); border: 2px solid #7c3aed; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; font-size: 13px;">
            <div style="text-align:center; font-weight:900; font-size:15px; color:#a78bfa; margin-bottom:6px;">
                📜 PHẦN MỀM LẬP QUẺ DỊCH — Phương pháp: Lục Hào
            </div>
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:4px;">
                <span>⏰ <b>Thời gian:</b> {dt.strftime('%H:%M %d/%m/%Y')}</span>
                <span>🌙 <b>Can Chi:</b> giờ {can_gio} {chi_gio}, ngày {_d_can_ngay} {_d_chi_ngay}, tháng {_d_can_thang} {_d_chi_thang}, năm {can_nam} {chi_nam}</span>
            </div>
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:4px; margin-top:4px;">
                <span>🌿 <b>Tiết khí:</b> {tiet_khi}</span>
                <span>☀️ <b>Nhật thần:</b> {_d_nhat_than}</span>
                <span>🌙 <b>Nguyệt lệnh:</b> {_d_nguyet_lenh}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== HEXAGRAM NAMES HEADER ==========
        st.markdown(f"""
        <div style="display:flex; justify-content:space-around; text-align:center; margin-bottom:8px;">
            <div>
                <div style="font-size:20px; font-weight:900; color:#b91c1c;">{res['ban']['name']}</div>
                <div style="font-size:12px; color:#78716c;">Họ {res['ban']['palace']} | {res['the_ung']}</div>
            </div>
            <div>
                <div style="font-size:20px; font-weight:900; color:#1d4ed8;">{res['bien']['name']}</div>
                <div style="font-size:12px; color:#78716c;">Quẻ Biến</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== COMPACT TABLE (giống xinhdich.com) ==========
        moving_hao = res.get('dong_hao', [])
        detail_ban = {d['hao']: d for d in res['ban']['details']}
        detail_bien = {d['hao']: d for d in res['bien'].get('details', [])}
        
        # Build HTML table
        # CSS first (separate call to avoid rendering issues)
        st.markdown("""
        <style>
            .lh-table { width:100%; border-collapse:collapse; font-size:12px; margin-bottom:10px; }
            .lh-table th { background:#1e293b; color:#fbbf24; padding:4px 6px; text-align:center; font-size:11px; border:1px solid #334155; }
            .lh-table td { padding:3px 6px; text-align:center; border:1px solid #e2e8f0; font-size:12px; }
            .lh-table tr:nth-child(even) { background:#f8fafc; }
            .lh-moving { background:#fef2f2 !important; font-weight:700; }
            .lh-yang { display:inline-block; width:40px; height:6px; background:#000; border-radius:1px; }
            .lh-yin { display:inline-flex; gap:6px; justify-content:center; }
            .lh-yin-half { display:inline-block; width:16px; height:6px; background:#000; border-radius:1px; }
            .lh-dong { color:#b91c1c; font-weight:bold; }
            .lh-vuong { color:#15803d; font-weight:600; }
            .lh-suy { color:#b91c1c; }
        </style>
        """, unsafe_allow_html=True)
        
        ban_name_h = res['ban']['name']
        ban_palace_h = res['ban']['palace']
        bien_name_h = res['bien']['name']
        
        table_html = f"""
        <table class="lh-table">
        <tr>
            <th colspan="6" style="background:#b91c1c; color:white; font-size:13px;">{ban_name_h} (Họ {ban_palace_h})</th>
            <th colspan="5" style="background:#1d4ed8; color:white; font-size:13px;">{bien_name_h} (Biến)</th>
        </tr>
        <tr>
            <th>Hào</th><th>Tượng</th><th>Lục Thân</th><th>Can Chi</th><th>Lục Thú</th><th>Vượng Suy</th>
            <th>Tượng</th><th>Lục Thân</th><th>Can Chi</th><th>Lục Thú</th><th>V-S</th>
        </tr>
        """
        
        for h_idx in range(6, 0, -1):
            db = detail_ban.get(h_idx, {})
            dbi = detail_bien.get(h_idx, {})
            is_dong = h_idx in moving_hao
            row_bg = "background:#dc2626; color:white; font-weight:700;" if is_dong else ""
            
            # Yang/Yin symbols - bold thick characters
            ban_line = db.get('line', 0)
            bien_line = dbi.get('line', 0)
            ban_sym = "<b style='font-size:16px;'>━━━━━━━</b>" if ban_line == 1 else "<b style='font-size:16px;'>━━━ ━━━</b>"
            bien_sym = "<b style='font-size:16px;'>━━━━━━━</b>" if bien_line == 1 else "<b style='font-size:16px;'>━━━ ━━━</b>"
            
            if is_dong:
                ban_sym = f"<b style='font-size:16px; color:#fff;'>━━━━━━━ ○</b>" if ban_line == 1 else f"<b style='font-size:16px; color:#fff;'>━━━ ━━━ ✕</b>"
            
            # Strength
            s = db.get('strength', '')
            if is_dong:
                s_html = f"<b>{s}</b>"
            else:
                s_html = f"<b style='color:#15803d;'>{s}</b>" if s in ['Vượng', 'Tướng'] else f"<b style='color:#b91c1c;'>{s}</b>"
            sb = dbi.get('strength', '')
            sb_html = f"<b style='color:#15803d;'>{sb}</b>" if sb in ['Vượng', 'Tướng'] else f"<b style='color:#b91c1c;'>{sb}</b>"
            
            # Markers
            marker = db.get('marker', '')
            hao_label = f"<b>Hào {h_idx}</b>"
            if marker:
                if is_dong:
                    hao_label += f" <b>{marker}</b>"
                else:
                    hao_label += f" <b style='color:#b91c1c;'>{marker}</b>"
            
            table_html += f"""<tr style="{row_bg}">
                <td>{hao_label}</td>
                <td>{ban_sym}</td>
                <td>{db.get('luc_than', '')}</td>
                <td><b>{db.get('can_chi', '')}</b></td>
                <td>{db.get('luc_thu', '')}</td>
                <td>{s_html}</td>
                <td>{bien_sym}</td>
                <td>{dbi.get('luc_than', '')}</td>
                <td><b>{dbi.get('can_chi', '')}</b></td>
                <td>{dbi.get('luc_thu', '')}</td>
                <td>{sb_html}</td>
            </tr>"""
        
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
        # ========== FOOTER INFO ==========
        st.markdown(f"""
        <div style="background:rgba(22,33,62,0.8); border-radius:8px; padding:8px 12px; font-size:12px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:4px;">
            <span>💡 {res['the_ung']}</span>
            <span>📝 Dụng Thần: {res['ban']['details'][2]['luc_than']}</span>
            <span>🔄 Động hào: {', '.join([str(h) for h in moving_hao])}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== V12.2: PHỤC THẦN (伏神) — Lục Thân ẩn ==========
        phuc_than_data = res.get('phuc_than', [])
        if phuc_than_data:
            pt_html = """
            <div style="background:rgba(30,27,75,0.8); border:2px solid #7c3aed; border-radius:8px; padding:8px 12px; margin:8px 0;">
                <div style="font-weight:700; color:#7c3aed; font-size:13px; margin-bottom:6px;">🔮 PHỤC THẦN (伏神) — Lục Thân Ẩn</div>
                <table style="width:100%; font-size:12px; border-collapse:collapse;">
                <tr style="background:#7c3aed; color:white;">
                    <th style="padding:3px 6px;">Lục Thân ẩn</th>
                    <th style="padding:3px 6px;">Can Chi</th>
                    <th style="padding:3px 6px;">Ẩn dưới hào</th>
                    <th style="padding:3px 6px;">Phi Thần</th>
                    <th style="padding:3px 6px;">Vượng Suy</th>
                </tr>"""
            for pt in phuc_than_data:
                s_color = '#15803d' if pt['strength'] in ['Vượng', 'Tướng'] else '#b91c1c'
                pt_html += f"""
                <tr>
                    <td style="padding:3px 6px; font-weight:700; color:#7c3aed;">{pt['luc_than']}</td>
                    <td style="padding:3px 6px; font-weight:700;">{pt['can_chi']}</td>
                    <td style="padding:3px 6px;">Hào {pt['hao_pos']}</td>
                    <td style="padding:3px 6px;">{pt['phi_than_luc_than']} ({pt['phi_than_can_chi']})</td>
                    <td style="padding:3px 6px; color:{s_color}; font-weight:700;">{pt['strength']}</td>
                </tr>"""
            pt_html += "</table></div>"
            st.markdown(pt_html, unsafe_allow_html=True)
        
        if show_debug_ih:
            st.write("DEBUG (Hào 1):", res['ban']['details'][0])
            st.write(f"📊 Module Path: `{luc_hao_kinh_dich.__file__}`")
            st.write(f"⚙️ Version: `{getattr(luc_hao_kinh_dich, 'VERSION_LH', 'Unknown')}`")
        
        # V13.0: Removed AI Luận Lục Hào button (dùng LỤC THUẬT HỢP NHẤT thay thế)
        st.info("💡 Để AI luận quẻ chuyên sâu → sang tab **'🤖 Hỏi Gemini AI'** → **'🌟 LỤC THUẬT HỢP NHẤT'**")


# ======================================================================
# FOOTER
# ======================================================================


# ======================================================================
# THIẾT BẢN THẦN TOÁN VIEW
# ======================================================================
elif st.session_state.current_view == "thiet_ban":
    st.markdown("## 📜 THIẾT BẢN THẦN TOÁN - NẠP ÂM ĐOÁN MỆNH")
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")
    
    # V42.9.9i: Sử dụng thời gian được chọn từ sidebar
    dt = selected_datetime
    st.info(f"🕒 Giờ gieo quẻ: {dt.strftime('%H:%M - %d/%m/%Y')}.")
    now = dt

    import qmdg_data
    from qmdg_calc import calculate_qmdg_params
    tb_data = getattr(qmdg_data, 'KY_MON_DATA', {}).get("THIET_BAN_THAN_TOAN", {})
    if not tb_data:
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thiet_ban_than_toan.json"), "r", encoding="utf-8") as _f_tb:
                tb_data = json.load(_f_tb)
        except Exception:
            tb_data = {}
    hoa_giap = tb_data.get("LUC_THAP_HOA_GIAP_NAP_AM", {})
    
    # Calculate params based on now
    params = calculate_qmdg_params(now)
    nam_tru = f"{params.get('can_nam')} {params.get('chi_nam')}"
    thang_tru = f"{params.get('can_thang')} {params.get('chi_thang')}"
    ngay_tru = f"{params.get('can_ngay')} {params.get('chi_ngay')}"
    gio_tru = f"{params.get('can_gio')} {params.get('chi_gio')}"
    
    na_nam_obj = hoa_giap.get(nam_tru, {})
    na_thang_obj = hoa_giap.get(thang_tru, {})
    na_ngay_obj = hoa_giap.get(ngay_tru, {})
    na_gio_obj = hoa_giap.get(gio_tru, {})
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**🍁 Trụ Năm (Thái Tuế): {nam_tru}**\n- **Nạp Âm:** {na_nam_obj.get('Nạp_Âm', 'Không rõ')} ({na_nam_obj.get('Hành', '?')})\n- **Ý nghĩa:** {na_nam_obj.get('Ý_Nghĩa', '')}")
        st.success(f"**🌙 Trụ Tháng (Nguyệt Lệnh): {thang_tru}**\n- **Nạp Âm:** {na_thang_obj.get('Nạp_Âm', 'Không rõ')} ({na_thang_obj.get('Hành', '?')})\n- **Ý nghĩa:** {na_thang_obj.get('Ý_Nghĩa', '')}")
    with col2:
        st.warning(f"**☀️ Trụ Ngày (Chủ Sự): {ngay_tru}**\n- **Nạp Âm:** {na_ngay_obj.get('Nạp_Âm', 'Không rõ')} ({na_ngay_obj.get('Hành', '?')})\n- **Ý nghĩa:** {na_ngay_obj.get('Ý_Nghĩa', '')}")
        st.info(f"**⏰ Trụ Giờ (Biến Hóa): {gio_tru}**\n- **Nạp Âm:** {na_gio_obj.get('Nạp_Âm', 'Không rõ')} ({na_gio_obj.get('Hành', '?')})\n- **Ý nghĩa:** {na_gio_obj.get('Ý_Nghĩa', '')}")
        
    st.markdown(f'''
    <div style="background:#1e293b; padding:15px; border-radius:10px; color:white; border-left:4px solid #f59e0b; margin-top:20px;">
        <h4>🔍 TÍCH HỢP ĐẠI TIÊN TRI</h4>
        - Thiết Bản Thần Toán là môn thuật số đề cao Nạp Âm của Năm và Ngày để định đoạt cát hung đại cục.<br>
        - AI Tiên Tri đã được trang bị toàn bộ hơn 100 quy tắc Phản Ngâm, Phục Ngâm, Trường Sinh 12 Giai Đoạn, và Thần Sát của Thiết Bản.<br>
        👉 Hãy chuyển sang Tab <b>"🤖 Hỏi Gemini AI"</b> và chọn <b>"🌟 LỤC THUẬT HỢP NHẤT"</b> để dung hợp Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản vào một câu trả lời duy nhất!
    </div>
    ''', unsafe_allow_html=True)
    
    # V13.0: Removed AI Luận Thiết Bản button (dùng LỤC THUẬT HỢP NHẤT thay thế)
    st.info("💡 Để AI luận quẻ chuyên sâu → sang tab **'🤖 Hỏi Gemini AI'** → **'🌟 LỤC THUẬT HỢP NHẤT'**")


# ======================================================================
# AI FACTORY VIEW
# ======================================================================
elif st.session_state.current_view == "ai_factory":
    try:
        from web.ai_factory_view import render_ai_factory_view
        render_ai_factory_view()
    except ImportError as e:
        st.error(f"Không thể tải module AI Factory: {e}")

# ======================================================================
# AI EXPERTS VIEW (40 AGENTS) — ĐÃ FIX LỖI GHI ĐÈ TAB & LIÊN KẾT TOÀN BỘ QUẺ
# ======================================================================
elif st.session_state.current_view == "ai_experts":
    st.markdown("## 🌟 HỘI ĐỒNG 40 CHUYÊN GIA AI & ĐẠI SƯ HỢP NHẤT")
    st.caption("Tất cả 40 Chuyên Gia AI đã được tích hợp trực tiếp vào 1 Ô Hỏi Đáp Hợp Nhất duy nhất bên dưới.")
    render_master_unified_qa_box(location_key="experts_view")

elif st.session_state.current_view == "gemini_ai":
    st.markdown("## 🤖 HỎI ĐÁP AI & LỤC THUẬT HỢP NHẤT TOÀN DIỆN")
    st.caption("Chỉ dùng 1 Ô Hỏi Đáp duy nhất — Tự động kết hợp toàn bộ 10 Hệ Thống Quẻ, Thiên Văn, 40 Chuyên Gia & AI Offline/Online.")
    render_master_unified_qa_box(location_key="gemini_view")

# ======================================================================
# VẠN VẬT LOẠI TƯỢNG VIEW
# ======================================================================
elif st.session_state.current_view == "van_vat":
    try:
        from van_vat_loai_tuong import render_van_vat_view
        render_van_vat_view()
    except ImportError as e:
        st.error(f"⚠️ Lỗi: Không tìm thấy module van_vat_loai_tuong.py: {e}")
    except Exception as e:
        st.error(f"⚠️ Lỗi hiển thị Vạn Vật Loại Tượng: {e}")

# ======================================================================
# ĐẠI LỤC NHÂM VIEW (V14.0)
# ======================================================================
elif st.session_state.current_view == "dai_luc_nham":
    st.header("🌊 Đại Lục Nhâm (大六壬)")
    st.caption("Tam Thức thứ 2 — Dự đoán sự kiện, chính xác thời gian")
    
    try:
        from dai_luc_nham import tinh_dai_luc_nham, format_display
        
        # Lấy dữ liệu từ quẻ hiện tại
        chart = st.session_state.get('chart_data', {})
        can_ngay = chart.get('can_ngay', 'Giáp')
        chi_ngay = chart.get('chi_ngay', 'Tý')
        chi_gio = chart.get('chi_gio', 'Ngọ')
        tiet_khi = chart.get('tiet_khi', 'Đông Chí')
        
        # Tính Đại Lục Nhâm
        data = tinh_dai_luc_nham(can_ngay, chi_ngay, chi_gio, tiet_khi)
        
        # Hiển thị
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📌 Nguyệt Tướng")
            st.info(f"**{data['nguyet_tuong']['ten']}** ({data['nguyet_tuong']['chi']})")
            
            st.subheader("📋 Tứ Khóa")
            for k in data['tu_khoa']:
                st.write(f"**{k['ten']}**: {k['thien']} / {k['dia']}")
        
        with col2:
            st.subheader("🔮 Tam Truyền")
            tt = data['tam_truyen']
            st.success(f"**Sơ Truyền (Phát)**: {tt['so_truyen']} ({tt['so_truyen_hanh']})")
            st.warning(f"**Trung Truyền (Diễn)**: {tt['trung_truyen']} ({tt['trung_truyen_hanh']})")
            st.info(f"**Mạt Truyền (Quả)**: {tt['mat_truyen']} ({tt['mat_truyen_hanh']})")
            st.caption(f"Phương pháp: {tt['phuong_phap']}")
        
        # Luận Giải
        st.subheader("📊 Luận Giải")
        lg = data['luan_giai']
        if lg['verdict'] == 'CÁT':
            st.success(f"🟢 **{lg['verdict']}**")
        elif lg['verdict'] == 'HUNG':
            st.error(f"🔴 **{lg['verdict']}**")
        else:
            st.warning(f"🟡 **{lg['verdict']}**")
        
        for d in lg['details']:
            st.write(d)
        
        # Thiên Địa Bàn
        with st.expander("🗺️ Thiên Địa Bàn"):
            for dia, thien in data['thien_dia_ban'].items():
                st.write(f"Địa: {dia} → Thiên: {thien}")
        
        # 12 Thiên Tướng
        with st.expander("⚔️ Thập Nhị Thiên Tướng"):
            for chi, ten in data['thien_tuong_map'].items():
                st.write(f"{chi}: {ten}")
        
    except ImportError as e:
        st.error(f"⚠️ Module dai_luc_nham.py chưa có: {e}")
    except Exception as e:
        st.error(f"⚠️ Lỗi Đại Lục Nhâm: {e}")

# ======================================================================
# THÁI ẤT THẦN SỐ VIEW (V14.0)
# ======================================================================
elif st.session_state.current_view == "thai_at":
    st.header("⭐ Thái Ất Thần Số (太乙神数)")
    st.caption("Tam Thức thứ 3 — Dự đoán vận mệnh quốc gia, thiên tai, đại sự")
    
    try:
        from thai_at_than_so import tinh_thai_at_than_so, format_display as ta_format
        import datetime
        
        # Lấy dữ liệu
        now = datetime.datetime.now()
        chart = st.session_state.get('chart_data', {})
        can_ngay = chart.get('can_ngay', 'Giáp')
        chi_ngay = chart.get('chi_ngay', 'Tý')
        
        # Tính Thái Ất
        data = tinh_thai_at_than_so(now.year, now.month, can_ngay, chi_ngay)
        
        # Hiển thị
        ta = data['thai_at_cung']
        st.info(f"**Năm {data['nam']}** | Tích Niên: {data['tich_nien']} | Thái Ất: Cung **{ta['cung']} ({ta['ten_cung']})** — {ta['hanh_cung']} — {ta['ly']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⚔️ Bát Tướng")
            for name, info in data['bat_tuong'].items():
                icon = "✅" if info['cat_hung'] in ('Cát', 'Đại Cát') else ("❌" if 'Hung' in info['cat_hung'] else "📌")
                st.write(f"{icon} **{name}**: Cung {info['cung']} ({info['ten_cung']}) — {info['cat_hung']}")
        
        with col2:
            st.subheader("📊 Luận Giải")
            lg = data['luan_giai']
            if lg['verdict'] == 'CÁT':
                st.success(f"🟢 **{lg['verdict']}**")
            elif lg['verdict'] == 'HUNG':
                st.error(f"🔴 **{lg['verdict']}**")
            else:
                st.warning(f"🟡 **{lg['verdict']}**")
            
            for d in lg['details']:
                st.write(d)
        
        # Cách Cục
        if data['cach_cuc']:
            with st.expander("🔮 Cách Cục Thái Ất"):
                for cc in data['cach_cuc']:
                    st.write(cc)
        
    except ImportError as e:
        st.error(f"⚠️ Module thai_at_than_so.py chưa có: {e}")
    except Exception as e:
        st.error(f"⚠️ Lỗi Thái Ất Thần Số: {e}")

# ======================================================================
# LỊCH VẠN NIÊN & ĐỔI NGÀY ÂM - DƯƠNG THIÊN VĂN VIEW
# ======================================================================
elif st.session_state.current_view == "lich_van_nien":
    try:
        from lich_van_nien_thien_van import render_lich_van_nien_view
        render_lich_van_nien_view()
    except Exception as e:
        st.error(f"⚠️ Lỗi Lịch Vạn Niên & Thiên Văn: {e}")

# ======================================================================
# XEM NGÀY ĐẸP VIEW (V42.4)
# ======================================================================
elif st.session_state.current_view == "xem_ngay":
    st.markdown("""
    <div style='text-align:center;margin-bottom:30px;'>
        <div style='font-size:2.5rem;margin-bottom:10px;'>📅</div>
        <h1 style='background:linear-gradient(90deg,#ffd700,#ff8c00,#ffd700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2rem;margin:0;'>XEM NGÀY GIỜ ĐẸP</h1>
        <p style='color:#94a3b8;font-size:0.9rem;margin-top:8px;'>Tổng hợp: Hiệp Kỷ Biện Phương Thư • Ngọc Hạp Thông Thư • Đổng Công Trạch Nhật • Thọ Mai Gia Lễ</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from xem_ngay_dep import (
            danh_gia_ngay, danh_gia_ngay_duong_lich, tinh_trung_tang,
            solar2lunar, tinh_28_tu, kiem_tra_duong_cong_ky,
            VIEC_XEM_NGAY, CHI_12, CAN_10,
            TRUC_TINH_CHAT, SAO_12, NHI_THAP_BAT_TU
        )
        from qmdg_calc import calculate_qmdg_params
        import datetime

        # ── TABS ──
        tab_xn, tab_lvn, tab_tt, tab_ref = st.tabs(["📅 Xem Ngày", "🗓️ Lịch Vạn Niên & Đổi Ngày Âm-Dương", "⚰️ Tra Trùng Tang", "📚 Bảng Tra Cứu"])
        with tab_lvn:
            try:
                from lich_van_nien_thien_van import render_lich_van_nien_view
                render_lich_van_nien_view()
            except Exception as _lvn_e:
                st.error(f"⚠️ Lỗi tải Lịch Vạn Niên: {_lvn_e}")

        # ════════════════ TAB 1: XEM NGÀY ════════════════
        with tab_xn:
            # V42.6c: CSS input TO + ĐẸP cho Xem Ngày
            st.markdown("""
            <style>
                .xn-input-label {
                    color: #fbbf24;
                    font-size: 1rem;
                    font-weight: 700;
                    margin-bottom: 6px;
                }
                .xn-person-card {
                    background: linear-gradient(145deg, #1a1a2e, #16213e);
                    padding: 20px 24px;
                    border-radius: 16px;
                    border: 1px solid rgba(167, 139, 250, 0.3);
                    box-shadow: 0 6px 24px rgba(99, 102, 241, 0.12);
                    margin: 12px 0;
                }
                .xn-person-card h4 {
                    color: #c4b5fd;
                    margin: 0 0 14px 0;
                    font-size: 1.15rem;
                }
            </style>
            """, unsafe_allow_html=True)
            
            col_input1, col_input2 = st.columns(2)
            with col_input1:
                st.markdown("<div class='xn-input-label'>📆 Chọn ngày dương lịch</div>", unsafe_allow_html=True)
                ngay_xem = st.date_input("Chọn ngày:", value=datetime.date.today(), key="xn_date", label_visibility="collapsed")
            with col_input2:
                st.markdown("<div class='xn-input-label'>🎯 Chọn loại việc (hoặc tự nhập bên dưới)</div>", unsafe_allow_html=True)
                viec_keys = list(VIEC_XEM_NGAY.keys())
                viec_labels = [VIEC_XEM_NGAY[k]["ten"] for k in viec_keys]
                viec_idx = st.selectbox("Loại việc:", range(len(viec_labels)), format_func=lambda i: viec_labels[i], key="xn_viec", label_visibility="collapsed")
                loai_viec = viec_keys[viec_idx]
            
            # ── Ô nhập tự do ──
            xn_custom_viec = st.text_input(
                "✍️ Hoặc tự nhập loại việc theo ý bạn:",
                placeholder="Ví dụ: Ký hợp đồng thuê nhà / Nhận xe mới / Khai trương quán ăn / Phẫu thuật...",
                key="xn_custom_viec"
            )
            if xn_custom_viec and xn_custom_viec.strip():
                # Ghi đè loại việc bằng input tự do
                st.session_state['xn_custom_viec_text'] = xn_custom_viec.strip()
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#064e3b,#065f46);padding:10px 16px;border-radius:10px;
                    border:1px solid #10b981;margin:4px 0;'>
                    <span style='color:#6ee7b7;font-weight:700;'>✅ Sử dụng: "{xn_custom_viec.strip()}" (thay cho danh sách có sẵn)</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state['xn_custom_viec_text'] = None

            # ── THÔNG TIN NGƯỜI HỎI ──
            st.markdown("""
            <div class='xn-person-card'>
                <h4>👤 Thông tin người hỏi (để xem tuổi hợp/xung)</h4>
            </div>
            """, unsafe_allow_html=True)

            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.markdown("<div class='xn-input-label'>📅 Năm sinh (DL)</div>", unsafe_allow_html=True)
                nam_sinh = st.number_input("Năm sinh:", min_value=1920, max_value=2026, value=1990, key="xn_nam_sinh", label_visibility="collapsed")
            with col_p2:
                st.markdown("<div class='xn-input-label'>⚧ Giới tính</div>", unsafe_allow_html=True)
                gioi_tinh_xn = st.radio("Giới tính:", ["Nam", "Nữ"], key="xn_gioi_tinh", horizontal=True, label_visibility="collapsed")
            with col_p3:
                # Tính Can Chi tuổi
                can_tuoi_idx = (nam_sinh - 4) % 10
                chi_tuoi_idx = (nam_sinh - 4) % 12
                can_tuoi = CAN_10[can_tuoi_idx]
                chi_tuoi = CHI_12[chi_tuoi_idx]
                tuoi_am = datetime.date.today().year - nam_sinh + 1
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#312e81,#4c1d95);padding:16px;border-radius:14px;
                    margin-top:8px;text-align:center;border:1px solid #7c3aed;
                    box-shadow:0 4px 16px rgba(124,58,237,0.2);'>
                    <div style='color:#fbbf24;font-weight:900;font-size:1.3rem;'>{can_tuoi} {chi_tuoi}</div>
                    <div style='color:#c4b5fd;font-size:0.95rem;margin-top:4px;'>Tuổi âm: {tuoi_am}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── TÍNH KIM LÂU (cho cưới hỏi) ──
            kim_lau = tuoi_am % 9
            is_kim_lau = kim_lau in [1, 3, 6, 8]  # Kim Lâu: 1-Thân, 3-Thê, 6-Tử, 8-Mệnh
            kim_lau_ten = {1: "Thân (bản thân)", 3: "Thê/Phu (vợ/chồng)", 6: "Tử (con cái)", 8: "Mệnh (sinh mệnh)"}

            # ── KIỂM TRA TUỔI XUNG VỚI NGÀY ──
            # Tính âm lịch
            ngay_am, thang_am, nam_am, nhuan = solar2lunar(ngay_xem.day, ngay_xem.month, ngay_xem.year)
            nhuan_str = " (Nhuận)" if nhuan else ""

            # Tính Can-Chi ngày
            dt_xem = datetime.datetime(ngay_xem.year, ngay_xem.month, ngay_xem.day, 12, 0)
            try:
                p = calculate_qmdg_params(dt_xem)
                can_ngay = p.get('can_ngay', 'Giáp')
                chi_ngay = p.get('chi_ngay', 'Tý')
            except Exception:
                can_ngay, chi_ngay = 'Giáp', 'Tý'

            # Chi ngày xung Chi tuổi? (cách 6 vị trí)
            chi_ngay_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else 0
            is_xung_tuoi = (chi_ngay_idx - chi_tuoi_idx) % 12 == 6

            # Hiện thông tin âm lịch + tuổi
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);padding:15px 20px;border-radius:12px;
                border-left:4px solid #fbbf24;margin:10px 0;'>
                <span style='color:#fbbf24;font-weight:800;font-size:1.1rem;'>📅 Âm Lịch:</span>
                <span style='color:white;font-size:1.1rem;'> Ngày {ngay_am} Tháng {thang_am}{nhuan_str} Năm {nam_am}</span>
                <span style='color:#94a3b8;margin-left:15px;'>| {can_ngay} {chi_ngay}</span>
                <span style='color:#c4b5fd;margin-left:15px;'>| 👤 {can_tuoi} {chi_tuoi} ({tuoi_am} tuổi)</span>
            </div>
            """, unsafe_allow_html=True)

            # Cảnh báo tuổi
            if is_xung_tuoi:
                st.error(f"⛔ CHI NGÀY ({chi_ngay}) XUNG CHI TUỔI ({chi_tuoi}) — Ngày này KHÔNG hợp tuổi bạn!")
            if is_kim_lau and loai_viec == "cuoi_hoi":
                st.warning(f"⚠️ Tuổi {tuoi_am} phạm KIM LÂU — {kim_lau_ten.get(kim_lau, '')} — Cần cân nhắc kỹ cho cưới hỏi!")

            # Lưu thông tin tuổi
            st.session_state['xn_tuoi_info'] = {
                'nam_sinh': nam_sinh, 'gioi_tinh': gioi_tinh_xn,
                'can_tuoi': can_tuoi, 'chi_tuoi': chi_tuoi, 'tuoi_am': tuoi_am,
                'is_xung_tuoi': is_xung_tuoi, 'is_kim_lau': is_kim_lau,
                'kim_lau_loai': kim_lau_ten.get(kim_lau, '')
            }

            if st.button("🔍 XEM NGÀY", type="primary", key="btn_xem_ngay", use_container_width=True):
                result = danh_gia_ngay(thang_am, ngay_am, can_ngay, chi_ngay, loai_viec, ngay_dl=(ngay_xem.day, ngay_xem.month, ngay_xem.year))
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#0f0c29,#302b63);padding:30px;border-radius:20px;
                    border:2px solid {result['verdict_color']};text-align:center;margin:20px 0;
                    box-shadow:0 10px 40px rgba(0,0,0,0.5);'>
                    <div style='font-size:3rem;'>{result['verdict'].split()[0]}</div>
                    <div style='font-size:1.8rem;font-weight:900;color:{result['verdict_color']};margin:10px 0;'>
                        {result['verdict']}
                    </div>
                    <div style='font-size:1.2rem;color:#fbbf24;font-weight:700;'>Điểm: {result['diem']}/100</div>
                    <div style='color:#94a3b8;margin-top:10px;font-size:0.95rem;'>
                        📅 Ngày {can_ngay} {chi_ngay} — Tháng {thang_am} ÂL — Ngày {ngay_am} ÂL<br>
                        🎯 Xem cho: {result['loai_viec']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    sao = result['sao_hoang_dao']
                    hd_bg = '#064e3b' if result['is_hoang_dao'] else '#7f1d1d'
                    st.markdown(f"""
                    <div style='background:{hd_bg};padding:18px;border-radius:14px;margin:8px 0;'>
                        <div style='font-size:1.3rem;font-weight:800;color:white;'>
                            {sao[2]} {sao[0]} — {sao[1]}
                        </div>
                        <div style='color:#d1d5db;font-size:0.9rem;'>{sao[3]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    truc = result['truc']
                    ti = result['truc_info']
                    truc_bg = '#064e3b' if result['truc_tot_cho_viec'] else ('#7f1d1d' if result['truc_xau_cho_viec'] else '#78350f')
                    st.markdown(f"""
                    <div style='background:{truc_bg};padding:18px;border-radius:14px;margin:8px 0;'>
                        <div style='font-size:1.3rem;font-weight:800;color:white;'>
                            {ti.get('icon','')} Trực {truc} — {ti.get('cat_hung','')}
                        </div>
                        <div style='color:#d1d5db;font-size:0.9rem;'>{ti.get('mo_ta','')}</div>
                        <div style='color:#86efac;font-size:0.85rem;margin-top:5px;'>Nên: {', '.join(ti.get('nen',[]))}</div>
                        <div style='color:#fca5a5;font-size:0.85rem;'>Kỵ: {', '.join(ti.get('ky',[]))}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 28 Tú (Ngọc Hạp Thông Thư)
                    sao_28 = result.get('sao_28_tu')
                    if sao_28:
                        s28_bg = '#064e3b' if sao_28[3] == 'Cát' else '#7f1d1d'
                        st.markdown(f"""
                        <div style='background:{s28_bg};padding:15px;border-radius:14px;margin:8px 0;'>
                            <div style='font-size:1.1rem;font-weight:800;color:white;'>
                                ⭐ Sao {sao_28[0]} ({sao_28[1]}/{sao_28[2]}) — {sao_28[3]}
                            </div>
                            <div style='color:#d1d5db;font-size:0.85rem;'>{sao_28[5]}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with col_d2:
                    if result['ly_do_tot']:
                        for r in result['ly_do_tot']:
                            st.success(r)
                    if result['ly_do_xau']:
                        for r in result['ly_do_xau']:
                            st.error(r)
                    if result['is_tam_nuong']:
                        st.warning(f"⚠️ NGÀY TAM NƯƠNG (ngày {ngay_am} ÂL) — Kiêng việc lớn!")
                    if result['is_nguyet_pha']:
                        st.warning("⚠️ NGÀY NGUYỆT PHÁ — Xung tháng, đại kỵ!")
                    if result.get('is_duong_cong_ky'):
                        st.error("⛔ DƯƠNG CÔNG KỴ NHẬT — 13 ngày đại kỵ, tuyệt đối không làm việc lớn!")

                # ── LƯU KẾT QUẢ ĐỂ AI TƯ VẤN ──
                st.session_state['xn_result'] = result
                st.session_state['xn_ngay_xem'] = ngay_xem
                st.session_state['xn_loai_viec'] = loai_viec
                # V42.6d: Lưu custom việc (nếu có)
                _custom_viec = st.session_state.get('xn_custom_viec_text')
                if _custom_viec:
                    st.session_state['xn_result']['loai_viec_custom'] = _custom_viec
                    st.session_state['xn_result']['loai_viec'] = _custom_viec
                st.session_state['xn_am_lich'] = f"{ngay_am}/{thang_am}/{nam_am}"
                st.session_state['xn_can_chi'] = f"{can_ngay} {chi_ngay}"

            # ── LIÊN KẾT Ô HỎI ĐÁP HỢP NHẤT DUY NHẤT ──
            if st.session_state.get('xn_result'):
                st.markdown("---")
                st.info("🔗 Kết quả Xem Ngày Đẹp này đã được đồng bộ tự động vào **Ô Hỏi Đáp Hợp Nhất Duy Nhất** (kết hợp cùng Kỳ Môn, Lục Hào, Mai Hoa, Thiết Bản, Đại Lục Nhâm, Thái Ất, Tử Vi & 40 Chuyên Gia AI).")
                if st.button("🔮 Chuyển tới Ô Hỏi Đáp Hợp Nhất Toàn Diện", type="primary", key="btn_xn_to_master", use_container_width=True):
                    xn_viec_ten = st.session_state.get('xn_result', {}).get('loai_viec', 'việc này')
                    xn_ngay_str = str(st.session_state.get('xn_ngay_xem', ''))
                    st.session_state['master_qa_prefill'] = f"Ngày {xn_ngay_str} tiến hành {xn_viec_ten} có tốt không, cần lưu ý và hóa giải gì?"
                    st.session_state.current_view = "ky_mon"
                    st.rerun()

        # ════════════════ TAB 2: TRA TRÙNG TANG ════════════════
        with tab_tt:
            st.markdown("""
            <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);padding:20px;border-radius:15px;
                border-left:4px solid #e74c3c;margin-bottom:20px;'>
                <h3 style='color:#fca5a5;margin:0 0 10px 0;'>⚰️ Tra Cứu Trùng Tang</h3>
                <p style='color:#94a3b8;margin:0;font-size:0.9rem;'>Theo Thọ Mai Gia Lễ + Tam Giáo Chính Hội</p>
            </div>
            """, unsafe_allow_html=True)

            col_tt1, col_tt2 = st.columns(2)
            with col_tt1:
                tuoi_mat = st.number_input("Tuổi người mất (tuổi âm):", min_value=1, max_value=120, value=70, key="tt_tuoi")
                gioi_tinh = st.radio("Giới tính:", ["Nam", "Nữ"], key="tt_gioi", horizontal=True)
            with col_tt2:
                nam_mat_val = st.number_input("Chi năm mất (1-12):", min_value=1, max_value=12, value=1, key="tt_nam")
                thang_mat_val = st.number_input("Tháng mất (ÂL):", min_value=1, max_value=12, value=1, key="tt_thang")
                ngay_mat_val = st.number_input("Ngày mất (ÂL):", min_value=1, max_value=30, value=1, key="tt_ngay")
                gio_mat_val = st.number_input("Giờ mất (1-12):", min_value=1, max_value=12, value=1, key="tt_gio")

            if st.button("🔍 TRA TRÙNG TANG", type="primary", key="btn_trung_tang", use_container_width=True):
                gt = 'nam' if gioi_tinh == "Nam" else 'nu'
                kq = tinh_trung_tang(tuoi_mat, gt, nam_mat_val, thang_mat_val, ngay_mat_val, gio_mat_val)
                kl = kq.get('ket_luan', '')
                kl_color = '#ef4444' if 'TRÙNG TANG' in kl else ('#22c55e' if 'NHẬP MỘ' in kl or 'AN TOÀN' in kl else '#fbbf24')
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#0f0c29,#302b63);padding:25px;border-radius:15px;
                    border:2px solid {kl_color};text-align:center;margin:15px 0;'>
                    <div style='font-size:1.5rem;font-weight:900;color:{kl_color};'>{kl}</div>
                </div>
                """, unsafe_allow_html=True)

                cols_tru = st.columns(4)
                for i, tru_name in enumerate(["Năm", "Tháng", "Ngày", "Giờ"]):
                    data = kq.get(tru_name, {})
                    if isinstance(data, dict):
                        cung = data.get('cung', '?')
                        loai = data.get('loai', '?')
                        bg = '#7f1d1d' if loai == 'TRÙNG TANG' else ('#064e3b' if loai == 'NHẬP MỘ' else '#78350f')
                        icon = '🔴' if loai == 'TRÙNG TANG' else ('🟢' if loai == 'NHẬP MỘ' else '🟡')
                        with cols_tru[i]:
                            st.markdown(f"""
                            <div style='background:{bg};padding:15px;border-radius:12px;text-align:center;'>
                                <div style='color:#94a3b8;font-size:0.8rem;'>{tru_name}</div>
                                <div style='font-size:1.5rem;font-weight:900;color:white;'>{cung}</div>
                                <div style='font-size:0.85rem;color:white;'>{icon} {loai}</div>
                            </div>
                            """, unsafe_allow_html=True)

        # ════════════════ TAB 3: BẢNG TRA CỨU ════════════════
        with tab_ref:
            ref_tab1, ref_tab2 = st.tabs(["📋 12 Trực", "⭐ Hoàng Đạo/Hắc Đạo"])
            with ref_tab1:
                st.markdown("### 📋 BẢNG 12 TRỰC (Đổng Công Trạch Nhật)")
                for truc_name, info in TRUC_TINH_CHAT.items():
                    bg = '#064e3b' if info['cat_hung'] == 'Cát' else ('#7f1d1d' if info['cat_hung'] == 'Hung' else '#78350f')
                    st.markdown(f"""
                    <div style='background:{bg};padding:12px 18px;border-radius:10px;margin:6px 0;'>
                        <span style='font-size:1.1rem;font-weight:800;color:white;'>{info['icon']} {truc_name}</span>
                        <span style='color:#d1d5db;margin-left:10px;'>{info['mo_ta']} ({info['cat_hung']})</span><br>
                        <span style='color:#86efac;font-size:0.85rem;'>✅ {', '.join(info['nen'])}</span>
                        <span style='color:#fca5a5;font-size:0.85rem;margin-left:15px;'>❌ {', '.join(info['ky'])}</span>
                    </div>
                    """, unsafe_allow_html=True)

            with ref_tab2:
                st.markdown("### ⭐ 12 SAO HOÀNG ĐẠO / HẮC ĐẠO")
                for sao_name, loai, icon, mota in SAO_12:
                    bg = '#064e3b' if loai == 'Hoàng Đạo' else '#7f1d1d'
                    st.markdown(f"""
                    <div style='background:{bg};padding:10px 18px;border-radius:10px;margin:5px 0;'>
                        <span style='font-size:1.1rem;font-weight:800;color:white;'>{icon} {sao_name}</span>
                        <span style='color:#fbbf24;margin-left:10px;font-weight:700;'>[{loai}]</span>
                        <span style='color:#d1d5db;margin-left:10px;'>{mota}</span>
                    </div>
                    """, unsafe_allow_html=True)

    except ImportError as e:
        st.error(f"⚠️ Chưa có module xem_ngay_dep.py: {e}")
    except Exception as e:
        st.error(f"⚠️ Lỗi: {e}")
        import traceback
        st.code(traceback.format_exc())

# ══════════════════════════════════════════════════════════════
# TỬ VI ĐẨU SỐ VIEW
# ══════════════════════════════════════════════════════════════
elif st.session_state.current_view == "tu_vi":
    st.markdown("""
    <h1 style='background:linear-gradient(90deg,#7c3aed,#a78bfa,#7c3aed);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;font-size:2.2rem;text-align:center;margin-bottom:5px;'>🔯 TỬ VI ĐẨU SỐ</h1>
    <p style='text-align:center;color:#94a3b8;margin-bottom:20px;'>Lá số trọn đời — Vận hạn — Kết nối Xem Ngày</p>
    """, unsafe_allow_html=True)

    try:
        from tu_vi import lap_la_so, format_la_so_text, CAN, CHI, CUNG_12
        from xem_ngay_dep import solar2lunar
        import datetime

        # ── NHẬP THÔNG TIN ──
        # V42.6c: CSS tùy chỉnh cho input TO + ĐẸP
        st.markdown("""
        <style>
            /* Làm to các input trong Tu Vi */
            [data-testid="stNumberInput"] input,
            [data-testid="stDateInput"] input {
                font-size: 1.2rem !important;
                padding: 12px 16px !important;
                font-weight: 700 !important;
            }
            [data-testid="stSelectbox"] > div > div {
                font-size: 1.1rem !important;
                padding: 8px 12px !important;
            }
            /* Card wrapper cho input */
            .tv-input-card {
                background: linear-gradient(145deg, #1e1b4b, #312e81);
                padding: 20px 24px;
                border-radius: 16px;
                border: 1px solid rgba(167, 139, 250, 0.3);
                box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
                margin-bottom: 16px;
            }
            .tv-input-card h3 {
                color: #c4b5fd;
                margin: 0 0 16px 0;
                font-size: 1.3rem;
            }
            .tv-input-label {
                color: #a78bfa;
                font-size: 0.95rem;
                font-weight: 600;
                margin-bottom: 6px;
            }
            .tv-lunar-result {
                background: linear-gradient(135deg, #312e81, #4c1d95);
                padding: 20px;
                border-radius: 14px;
                text-align: center;
                border: 2px solid #7c3aed;
                box-shadow: 0 4px 24px rgba(124, 58, 237, 0.25);
                margin-top: 8px;
            }
            .tv-lunar-result .date {
                color: #fbbf24;
                font-weight: 900;
                font-size: 1.4rem;
            }
            .tv-lunar-result .year {
                color: #c4b5fd;
                font-size: 1.1rem;
                margin-top: 6px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='tv-input-card'>
            <h3>👤 NHẬP THÔNG TIN NGÀY SINH</h3>
        </div>
        """, unsafe_allow_html=True)

        # ── Chọn cách nhập + Giới tính ──
        col_mode, col_gt = st.columns([3, 1])
        with col_mode:
            tv_input_mode = st.radio(
                "📅 Cách nhập ngày sinh:",
                ["🌞 Dương lịch (tự đổi sang Âm)", "🌙 Âm lịch (nhập trực tiếp)"],
                key="tv_input_mode", horizontal=True
            )
        with col_gt:
            tv_gt = st.radio("⚧ Giới tính:", ["Nam","Nữ"], key="tv_gt", horizontal=True)

        if tv_input_mode.startswith("🌞"):
            # ═══ NHẬP DƯƠNG LỊCH → TỰ CONVERT SANG ÂM ═══
            c_dl1, c_dl2 = st.columns(2)
            with c_dl1:
                st.markdown("<div class='tv-input-label'>📆 Ngày sinh dương lịch</div>", unsafe_allow_html=True)
                tv_ngay_dl = st.date_input("Ngày sinh dương lịch:", value=datetime.date(1990, 1, 15), key="tv_ngay_dl", label_visibility="collapsed")
            with c_dl2:
                st.markdown("<div class='tv-input-label'>🕐 Giờ sinh (12 chi)</div>", unsafe_allow_html=True)
                gio_labels = [f"{CHI[i]} ({i*2}h-{i*2+2}h)" for i in range(12)]
                tv_gio = st.selectbox("Giờ sinh:", range(12), format_func=lambda i: gio_labels[i], key="tv_gio_dl", label_visibility="collapsed")
            
            # Convert dương → âm + hiển thị đẹp
            try:
                d_al, m_al, y_al, is_leap = solar2lunar(tv_ngay_dl.day, tv_ngay_dl.month, tv_ngay_dl.year)
                _leap_text = " (Nhuận)" if is_leap else ""
                # V42.8 FIX: Dùng năm ÂM LỊCH (y_al) để tính Can Chi, không dùng năm DL
                # Ví dụ: 15/01/1990 DL = 19/12/Kỷ Tỵ (1989), KHÔNG PHẢI Canh Ngọ (1990)
                can_nam_idx = (y_al - 4) % 10
                chi_nam_idx = (y_al - 4) % 12
                _gio_chi = CHI[tv_gio]
                
                st.markdown(f"""
                <div class='tv-lunar-result'>
                    <div style='color:#94a3b8;font-size:0.85rem;margin-bottom:6px;'>🔄 Kết quả chuyển đổi Âm lịch</div>
                    <div class='date'>📆 Ngày {d_al} Tháng {m_al} Năm {y_al}{_leap_text}</div>
                    <div class='year'>🐉 Năm {CAN[can_nam_idx]} {CHI[chi_nam_idx]} — Giờ {_gio_chi}</div>
                    <div style='color:#6ee7b7;font-size:0.9rem;margin-top:8px;'>
                        ✅ Dương lịch: {tv_ngay_dl.strftime('%d/%m/%Y')} → Âm lịch: {d_al}/{m_al}/{y_al}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Lỗi chuyển đổi âm lịch: {e}")
                d_al, m_al, y_al = 15, 1, 1990
            
            # V42.8 FIX: Dùng năm ÂM LỊCH cho Tử Vi (quan trọng: ảnh hưởng toàn bộ lá số)
            tv_nam = y_al
            tv_thang = m_al
            tv_ngay = d_al
        else:
            # ═══ NHẬP ÂM LỊCH TRỰC TIẾP ═══
            c_al1, c_al2, c_al3, c_al4 = st.columns(4)
            with c_al1:
                st.markdown("<div class='tv-input-label'>📅 Năm sinh (DL)</div>", unsafe_allow_html=True)
                tv_nam = st.number_input("Năm sinh:", 1920, 2026, 1990, key="tv_nam", label_visibility="collapsed")
            with c_al2:
                st.markdown("<div class='tv-input-label'>🌙 Tháng ÂL</div>", unsafe_allow_html=True)
                tv_thang = st.number_input("Tháng ÂL:", 1, 12, 1, key="tv_thang", label_visibility="collapsed")
            with c_al3:
                st.markdown("<div class='tv-input-label'>🌙 Ngày ÂL</div>", unsafe_allow_html=True)
                tv_ngay = st.number_input("Ngày ÂL:", 1, 30, 15, key="tv_ngay", label_visibility="collapsed")
            with c_al4:
                st.markdown("<div class='tv-input-label'>🕐 Giờ sinh</div>", unsafe_allow_html=True)
                gio_labels = [f"{CHI[i]} ({i*2}h-{i*2+2}h)" for i in range(12)]
                tv_gio = st.selectbox("Giờ sinh:", range(12), format_func=lambda i: gio_labels[i], key="tv_gio", label_visibility="collapsed")

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        if st.button("🔯 LẬP LÁ SỐ TỬ VI", type="primary", key="btn_lap_tu_vi", use_container_width=True):
            gt = 'nam' if tv_gt == 'Nam' else 'nu'
            la_so = lap_la_so(tv_nam, tv_thang, tv_ngay, tv_gio, gt)
            st.session_state['tv_la_so'] = la_so

        # ── HIỂN THỊ LÁ SỐ ──
        if st.session_state.get('tv_la_so'):
            ls = st.session_state['tv_la_so']

            # Header
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);padding:25px;border-radius:18px;
                border:2px solid #a78bfa;text-align:center;margin:15px 0;'>
                <div style='color:#fbbf24;font-size:2rem;font-weight:900;'>{ls['can_nam']} {ls['chi_nam']} ({ls['nam_sinh']})</div>
                <div style='color:#c4b5fd;font-size:1.1rem;margin:8px 0;'>Ngày {ls['ngay_am']} Tháng {ls['thang_am']} ÂL — Giờ {ls['gio']} — {ls['gioi_tinh'].upper()}</div>
                <div style='color:#fbbf24;font-size:1rem;'>🏛️ Nạp Âm: {ls['nap_am']} | 📍 Mệnh: {ls['menh_cung']['chi']} | 🎭 Thân: {ls['than_cung']['chi']} | 🔢 {ls['cuc_ten']}</div>
                <div style='color:#86efac;font-size:0.9rem;margin-top:8px;'>Tứ Hóa: Lộc={ls['tu_hoa']['Hóa Lộc']} | Quyền={ls['tu_hoa']['Hóa Quyền']} | Khoa={ls['tu_hoa']['Hóa Khoa']} | Kỵ={ls['tu_hoa']['Hóa Kỵ']}</div>
            </div>
            """, unsafe_allow_html=True)

            # 12 Cung Grid (4x3)
            st.markdown("### 🏛️ 12 Cung")
            for row in range(4):
                cols = st.columns(3)
                for ci in range(3):
                    idx = row * 3 + ci
                    if idx < 12:
                        cung_name = CUNG_12[idx]
                        data = ls['cung_map'][cung_name]
                        stars = ", ".join(data['chinh_tinh']) if data['chinh_tinh'] else "—"
                        phu = ", ".join(data['phu_tinh']) if data['phu_tinh'] else ""
                        is_menh = data['chi'] == ls['menh_cung']['chi'] and cung_name == 'Mệnh'
                        is_than = data['chi'] == ls['than_cung']['chi']
                        border_c = '#fbbf24' if is_menh else ('#a78bfa' if is_than else '#334155')
                        with cols[ci]:
                            st.markdown(f"""
                            <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);padding:14px;border-radius:12px;
                                border:2px solid {border_c};margin:4px 0;min-height:120px;'>
                                <div style='color:#fbbf24;font-weight:800;font-size:1rem;'>{cung_name} ({data['chi']})</div>
                                <div style='color:#e2e8f0;font-size:0.9rem;margin-top:5px;'>⭐ {stars}</div>
                                {f"<div style='color:#86efac;font-size:0.8rem;margin-top:3px;'>🔹 {phu}</div>" if phu else ''}
                            </div>
                            """, unsafe_allow_html=True)

            # Đại Hạn
            st.markdown("### 📊 Đại Hạn (10 năm)")
            dh_cols = st.columns(4)
            for i, dh in enumerate(ls['dai_han'][:8]):
                tuoi_now = ls['luu_nien']['tuoi']
                is_current = dh['tu'] <= tuoi_now <= dh['den']
                bg = '#064e3b' if is_current else '#1e293b'
                with dh_cols[i % 4]:
                    st.markdown(f"""
                    <div style='background:{bg};padding:10px;border-radius:10px;margin:4px 0;
                        border:{'2px solid #22c55e' if is_current else '1px solid #334155'};text-align:center;'>
                        <div style='color:{'#22c55e' if is_current else '#94a3b8'};font-weight:800;'>{dh['tuoi_range']}</div>
                        <div style='color:white;font-size:0.85rem;'>{dh['cung']} ({dh['chi']})</div>
                        {'<div style="color:#22c55e;font-size:0.75rem;">◄ HIỆN TẠI</div>' if is_current else ''}
                    </div>
                    """, unsafe_allow_html=True)

            # Lưu Niên
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#064e3b,#065f46);padding:18px;border-radius:14px;
                border:2px solid #22c55e;margin:15px 0;text-align:center;'>
                <div style='color:#86efac;font-size:1.2rem;font-weight:900;'>📅 LƯU NIÊN {ls['luu_nien']['nam']}</div>
                <div style='color:white;font-size:1rem;'>Tuổi {ls['luu_nien']['tuoi']} → Cung {ls['luu_nien']['cung']} ({ls['luu_nien']['chi']})</div>
            </div>
            """, unsafe_allow_html=True)

            # ── LIÊN KẾT Ô HỎI ĐÁP HỢP NHẤT DUY NHẤT ──
            st.markdown("---")
            st.info("🔗 Lá số Tử Vi Đẩu Số này đã được đồng bộ tự động vào **Ô Hỏi Đáp Hợp Nhất Duy Nhất** (kết hợp cùng Kỳ Môn, Lục Hào, Mai Hoa, Thiết Bản, Đại Lục Nhâm, Thái Ất, Xem Ngày & 40 Chuyên Gia AI).")
            if st.button("🔮 Chuyển tới Ô Hỏi Đáp Hợp Nhất Toàn Diện", type="primary", key="btn_tv_to_master", use_container_width=True):
                st.session_state['master_qa_prefill'] = f"Luận giải chuyên sâu vận mệnh, tài lộc, sự nghiệp và lưu niên {ls['luu_nien']['nam']} kết hợp toàn bộ các quẻ"
                st.session_state.current_view = "ky_mon"
                st.rerun()

    except ImportError as e:
        st.error(f"⚠️ Chưa có module tu_vi.py: {e}")
    except Exception as e:
        st.error(f"⚠️ Lỗi: {e}")
        import traceback
        st.code(traceback.format_exc())

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>© 2026 Vũ Việt Cường - Kỳ Môn Độn Giáp Web Application</p>
    <p>🌐 Chạy 24/7 trên Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)


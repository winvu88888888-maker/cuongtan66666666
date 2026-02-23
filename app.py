import streamlit as st

# VERSION: 2026-02-06-V2.5-TITAN-FORCE-REBUILD-01
try:
    st.set_page_config(
    page_title="🔴 SYSTEM DIAGNOSTIC MODE 🔴",
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

import extra_streamlit_components as stx
from streamlit_autorefresh import st_autorefresh

# Initialize CookieManager without cache to avoid CachedWidgetWarning
cookie_manager = stx.CookieManager(key="cookie_mgr")
st_autorefresh(interval=60000, key="auto_time_refresh") # Refresh every 60s

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
    html {{
        font-size: {zoom}% !important;
        transition: font-size 0.2s ease-in-out;
    }}
    /* Adjust body to inherit or reset if needed, but rem is based on html */
    body {{
        font-size: 1rem; 
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
st.sidebar.markdown("### 🧠 Trí Tuệ Nhân Tạo")
st.sidebar.success("🚀 **MODEL: GEMINI-1.5-PRO**")
st.sidebar.caption("Trạng thái: Đã kích hoạt Prophet Mode")

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
    print(f"âš ï¸ AI Factory modules not available: {e}")
    
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
# DEPLOYMENT VERIFICATION BANNER
st.success("✅ SYSTEM ONLINE: V4.0 - TỨ THUẬT HỢP NHẤT")

# ======================================================================
# SIDEBAR - CONTROLS
# ======================================================================
with st.sidebar:
    st.markdown("### ⚙️ Điều Khiển")
    
    # View selection
    view_option = st.radio(
        "Chọn Phương Pháp:",
        ["🔮 Kỳ Môn Độn Giáp", "🏭 Nhà Máy AI", "🌟 40 Chuyên Gia AI", "📖 Mai Hoa 64 Quẻ", "☯️ Lục Hào Kinh Dịch", "📜 Thiết Bản Thần Toán", "🤖 Hỏi Gemini AI"],
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
    elif view_option == "📜 Thiết Bản Thần Toán":
        st.session_state.current_view = "thiet_ban"
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
        'V2.7' not in getattr(st.session_state.gemini_helper, 'version', '')):
        
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
        
        # Tổng hợp: Ưu tiên Manual > Streamlit Secrets > Saved Key > Factory Key
        secret_api_key = manual_key or st_secret or saved_key or factory_key
        
        # Thông báo nếu chạy trên cloud nhưng chưa có secret
        if not st_secret and not saved_key and not factory_key:
            # Đang chạy trên cloud và không có API key nào
            st.session_state.missing_cloud_secret = True
        
import google.generativeai as genai

# --- MANUAL KEY OVERRIDE (CRITICAL FOR LEAKED KEYS) ---
with st.sidebar:
    with st.expander("🔑 Cấu hình API Key (Nâng cao)", expanded=st.session_state.get("missing_cloud_secret", False)):
        new_key = st.text_input("Nhập Gemini API Key mới:", type="password", key="manual_gemini_key_input", help="Nhập key mới nếu key cũ bị lỗi 403/Quota.")
        if new_key:
            st.session_state.gemini_key = new_key
            st.session_state.missing_cloud_secret = False
            # Clear helper to force reload
            if 'gemini_helper' in st.session_state: del st.session_state.gemini_helper
            st.success("Đã lưu Key! Vui lòng bấm 'Rerun' hoặc F5.")
            if st.button("🔄 Kích hoạt ngay"):
                st.rerun()

# --- IMPORT GEMINI HELPER FROM EXTERNAL MODULE (Unified Logic) ---
# try:
#     from gemini_helper import GeminiQMDGHelper
# except ImportError:
#     st.error("⚠️ Critical Error: gemini_helper.py not found! Vui lòng kiểm tra lại thư mục.")

# --- INLINED GEMINI HELPER TO BYPASS IMPORT CACHING (PHOENIX FIX) ---
class GeminiQMDGHelper:
    """Helper class for Gemini AI with QMDG specific knowledge and grounding"""
    
    def __init__(self, api_key_input):
        import re
        import hashlib
        import google.generativeai as genai
        
        # ROBUST KEY EXTRACTION (Combined Method)
        keys_from_regex = re.findall(r"AIza[0-9A-Za-z-_]{35}", str(api_key_input))
        
        # Fallback/Supplemental: Split by common delimiters
        raw_text = str(api_key_input).replace("\n", ",").replace(";", ",")
        keys_from_split = [k.strip() for k in raw_text.split(',') if len(k.strip()) > 30 and "AIza" in k]
        
        # Merge and Deduplicate (Preserve order)
        all_candidates = keys_from_regex + keys_from_split
        self.api_keys = list(dict.fromkeys(all_candidates)) # remove duplicates while keeping order
        
        # Final cleanup
        self.api_keys = [k for k in self.api_keys if len(k) > 30]

        self.current_key_index = 0
        self.api_key = self.api_keys[0] if self.api_keys else None
        
        # Feedback to User (Subtle)
        if hasattr(st, 'toast') and self.api_keys:
            st.toast(f"🔑 Đã nạp thành công {len(self.api_keys)} API Key!", icon="🛡️")

            # DEBUG DISPLAY - TEMPORARY
            if len(self.api_keys) > 1:
                st.info(f"📋 DEBUG: Đã nhận diện {len(self.api_keys)} Key. (Key 1: ...{self.api_keys[0][-6:]}, Key 2: ...{self.api_keys[1][-6:]})")
            else:
                raw_preview = str(api_key_input)[:20] + "..." if api_key_input else "None"
                # st.warning(f"⚠️ DEBUG: Chỉ tìm thấy 1 Key! (Input: {raw_preview})")
        
        self.version = "V4.0 - TỨ THUẬT HỢP NHẤT" 
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self.n8n_url = None
        self.n8n_timeout = 8
        
        # Default placeholder
        self.model = self._get_best_model()

    def _get_best_model(self):
        # Always default to Flash 2.0 for stability
        import google.generativeai as genai
        return genai.GenerativeModel('gemini-2.0-flash')

    def test_connection(self):
        try:
            import google.generativeai as genai
            list(genai.list_models())
            return True, "Kết nối thành công (Inlined)"
        except Exception as e:
            return False, f"Lỗi kết nối: {str(e)}"

    def classify_intent(self, text):
        text = text.lower()
        social_keywords = ['chào', 'hello', 'hi', 'bạn là ai', 'tên gì', 'khỏe không']
        if any(x in text for x in social_keywords) and len(text) < 20:
            return 'social'
        return 'question'

    def call_n8n_webhook(self, question, context_summary):
        if not self.n8n_url: return None
        try:
            import requests
            import hashlib
            payload = {
                "question": question,
                "context": context_summary,
                "timestamp": str(hashlib.sha256(question.encode()).hexdigest())[:10]
            }
            resp = requests.post(self.n8n_url, json=payload, timeout=self.n8n_timeout)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('output') or data.get('text') or data.get('result')
            return None
        except Exception: return None

    def _create_expert_prompt(self, user_input):
        return f"VAI TRÒ: Trợ lý Huyền Học.\\nUSER: {user_input}"

    def safe_get_text(self, response):
        try:
            if response.text: return response.text
        except: pass
        return "⚠️"

    # --- BASIC AI CALLER WITH CASCADE FALLBACK & KEY ROTATION ---
    def _call_ai_raw(self, prompt):
        import google.generativeai as genai
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        import time

        # RELAXED SAFETY SETTINGS (Prevent "Safety" Blocks on Fortune Telling topics)
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # DYNAMIC DISCOVERY V3 (The Last Stand)
        # Goal: Find ANY model that works and tell the user what we found.
        if not hasattr(self, 'cascade_models') or not self.cascade_models:
            self.cascade_models = []
            try:
                # 1. Get ALL valid models that support generation
                all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # 2. LOGGING FOR USER (Crucial for Debugging)
                if hasattr(st, 'toast'):
                    # Show first 3 models found to verify we see ANYTHING
                    try:
                         # Only toast if we haven't toasted recently to avoid spam (optional optimization)
                         pass
                    except: pass
                    # st.toast(f"🔎 Tìm thấy {len(all_models)} Models: {all_models[:3]}...", icon="🤖")
                    print(f"DEBUG: Capabilities Found: {all_models}")

                # 3. Intelligent Sorting: 1.5 Flash > 1.5 Pro > 2.0 Flash (Preview)
                # We prioritize 1.5 because 2.0 has low quota for free users.
                def model_score(m_name):
                    score = 0
                    if 'gemini-1.5-flash' in m_name: score += 100
                    if 'gemini-1.5-flash-8b' in m_name: score += 150 # Bias slightly higher for speed/quota
                    if 'gemini-1.5-pro' in m_name: score += 80
                    if 'gemini-2.0' in m_name: score += 50 # Lower priority due to limits
                    if 'latest' in m_name: score -= 10 # Avoid unstable
                    return score

                all_models.sort(key=model_score, reverse=True)
                self.cascade_models = all_models
                
                # 4. Fallback if empty
                if not self.cascade_models: raise Exception("No generateContent models found")
                
            except Exception as e:
                print(f"⚠️ Model Discovery Failed: {e}. Using Safe Fallback List.")
                self.cascade_models = [
                    'gemini-1.5-flash',
                    'gemini-1.5-flash-8b',
                    'gemini-1.5-pro',
                    'gemini-2.0-flash',
                    'gemini-pro'
                ]
                
        # Use the discovered list
        cascade_models = self.cascade_models
        
        last_error = None
        error_log = []
        
        # KEY ROTATION LOOP
        # We try every key in our list until one works or all fail
        for key_idx, current_api_key in enumerate(self.api_keys):
            
            # Configure with current key
            try:
                genai.configure(api_key=current_api_key)
            except: continue

            # MODEL CASCADE LOOP for Current Key
            for model_name in cascade_models:
                try:
                    active_model = genai.GenerativeModel(model_name)
                    # Try with tools first
                    try: 
                        tools = [{"google_search_retrieval": {}}]
                        resp = active_model.generate_content(prompt, tools=tools, safety_settings=safety_settings)
                    except:
                        resp = active_model.generate_content(prompt, safety_settings=safety_settings)
                    
                    # ROBUST TEXT EXTRACTION (Handle Safety Filters)
                    final_text = ""
                    try:
                        if resp.text: final_text = resp.text
                    except Exception:
                        # Fallback for "ValueError: The response was blocked."
                        try:
                            if resp.candidates and resp.candidates[0].content.parts:
                                final_text = resp.candidates[0].content.parts[0].text
                        except: pass
                    
                    if final_text and len(final_text.strip()) > 1:
                         return final_text
                    
                    # If empty, IT IS AN ERROR -> Force next model/key
                    block_reason = "Unknown"
                    try:
                        if resp.prompt_feedback and resp.prompt_feedback.block_reason:
                             block_reason = str(resp.prompt_feedback.block_reason)
                    except: pass
                    
                    raise Exception(f"Empty Response (Len: {len(final_text) if final_text else 0}, Block Reason: {block_reason})")

                except Exception as e:
                    # CATCH ALL ERRORS TO CONTINUE FALLBACK
                    err = str(e)
                    error_log.append(f"Key{key_idx+1}-{model_name}: {err}")
                    
                    # DEBUG: SHOW REAL ERROR TO USER
                    print(f"DEBUG ERROR: {model_name} with Key {key_idx+1}: {err}")

                    # CRITICAL ERRORS THAT REQUIRE KEY SWITCH (Only 403 or Invalid Key)
                    lower_err = err.lower()
                    if "403" in lower_err or "key" in lower_err and "invalid" in lower_err:
                         print(f"⚠️ Key {key_idx+1} Permission Denied/Invalid. Switching Key...")
                         last_error = e
                         break # BREAK MODEL LOOP -> Next Key
                    
                    # RETRY STRATEGY FOR 429 (RATE LIMIT)
                    if "429" in lower_err or "quota" in lower_err:
                         print(f"⏳ Rate Limit hit on {model_name}. Sleeping 2s...")
                         time.sleep(2) # Wait a bit before trying next model/key
                         # Don't break, just continue to next model/key
                    
                    # OTHER ERRORS (Likely model specific, not key specific) -> Try next model
                    print(f"⚠️ {model_name} failed: {err}. Switching Model...")
                    last_error = e
                    continue
        
        # ANALYZE FAILURE REASONS
        error_text = "\\n".join(error_log)
        if "429" in error_text or "quota" in error_text:
            return f"⏳ **Hết lượt (429)**<br>Đã thử {len(self.api_keys)} Key nhưng đều thất bại.<br>Chi tiết lỗi:<br>{error_text}"
            
        return f"🛑 AI Failed. Debug Log:<br>{error_text if error_text else 'No specific error log. Unknown failure.'}"


    # COMPATIBILITY WRAPPER FOR ORCHESTRATOR
    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        return self._call_ai_raw(prompt)

    def _process_response(self, text):
        import re
        import streamlit as st
        
        thinking = ""
        answer = text
        
        # Regex search for the thinking block
        if not text: return "" # Defensive coding
        text = str(text) # Force string conversion
        match_thinking = re.search(r'\[SUY_LUAN\](.*?)\[/SUY_LUAN\]', text, re.DOTALL)
        if match_thinking:
            thinking = match_thinking.group(1).strip()
            answer = text.replace(match_thinking.group(0), "").strip()
            
            # Display the thinking process visually
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
            with st.expander("⚡ Logic Suy Luận (Click để xem)", expanded=False):
                st.markdown(f'<div class="ag-thinking">{thinking}</div>', unsafe_allow_html=True)

        return answer

    def answer_question(self, question, chart_data=None, topic=None, mai_hoa_data=None, luc_hao_data=None): 

        
        # --- V3.6 VISIBLE INTELLECT: PROOF OF REASONING ---
        import streamlit as st
        t = st.session_state.get('chu_de_hien_tai', 'Chung')
        
        # REMOVED SOCIAL BYPASS -> ALL QUESTIONS GO TO MASTER BRAIN
        
        # A. KNOWLEDGE REPOSITORY
        element_definitions = (
             "TRA CỨU TỪ ĐIỂN KỲ MÔN (CƠ BẢN):\n"
             "- Cửa Sinh: Sự sống, lợi lộc. | Cửa Tử: Chấm dứt, săn bắn. | Cửa Thương: Tổn thương, xe cộ.\n"
             "- Cửa Đỗ: Bế tắc, ẩn nấp. | Cửa Cảnh: Tin tức, giấy tờ. | Cửa Hưu: Nghỉ ngơi, hôn nhân.\n"
             "- Cửa Kinh: Sợ hãi, kiện tụng. | Cửa Khai: Mở ra, công việc.\n"
             "- Sao Thiên Bồng: Trộm cướp, mạo hiểm. | Sao Thiên Nhu: Ôn hòa, bệnh tật.\n"
             "- Sao Thiên Xung: Nóng nảy, xung đột. | Sao Thiên Phụ: Văn chương, thi cử.\n"
             "- Sao Thiên Anh: Nóng nảy, văn thư. | Sao Thiên Nhậm: Cẩn trọng, giữ tiền.\n"
             "- Sao Thiên Trụ: Phá hoại, vững chắc. | Sao Thiên Tâm: Tâm tính, lãnh đạo.\n"
             "QUY TẮC DỊCH MÃ & TUẦN KHÔNG (TỰ TÍNH):\n"
             "- Dịch Mã (Biến động): Dần Ngọ Tuất -> Thân | Thân Tý Thìn -> Dần | Tỵ Dậu Sửu -> Hợi | Hợi Mão Mùi -> Tỵ.\n"
             "- Tuần Không (Hư ảo): Giáp Tý (Tuần Không Tuất Hợi)... (Tự suy từ Can Chi Ngày/Giờ).\n"
         )

        # B. BUILD CONTEXT
        extra_context = ""
        if chart_data:
            extra_context += "\\n[DỮ LIỆU KỲ MÔN ĐỘN GIÁP (THỜI KHẮC CHIẾN LƯỢC)]:\\n"
            extra_context += f"- Thời gian: {chart_data.get('can_gio')} {chart_data.get('chi_gio')} (Giờ), {chart_data.get('can_ngay')} {chart_data.get('chi_ngay')} (Ngày)\\n"
            extra_context += f"{element_definitions}\\n" 
            
            extra_context += "\\n[BÀN CỜ 9 CUNG KỲ MÔN (ĐỂ SUY KẾT QUẢ)]:\\n"
            for p in range(1, 10):
                p_star = chart_data.get('thien_ban', {}).get(p, '?')
                p_door = chart_data.get('nhan_ban', {}).get(p, '?')
                p_deity = chart_data.get('than_ban', {}).get(p, '?')
                p_can_t = chart_data.get('can_thien_ban', {}).get(p, '?')
                p_can_d = chart_data.get('can_dia_ban', {}).get(p, '?')
                if p_star != '?':
                    extra_context += f"- Cung {p}: Sao {p_star} | Cửa {p_door} | Thần {p_deity} | Can: {p_can_t}/{p_can_d}\\n"

        if mai_hoa_data:
            extra_context += f"\\n[DỮ LIỆU MAI HOA (HÌNH TƯỢNG & ĐIỀM BÁO)]:\\n"
            extra_context += f"- Quẻ: {mai_hoa_data.get('ten', '?')}. Tượng: {mai_hoa_data.get('tuong', '?')}\\n"
            extra_context += f"- Ý Nghĩa Sâu: {mai_hoa_data.get('nghĩa', '?')}\\n"

        if luc_hao_data:
            extra_context += f"\\n[DỮ LIỆU LỤC HÀO (CHI TIẾT SỰ VIỆC)]:\\n"
            extra_context += f"- Quẻ Chủ: {luc_hao_data.get('ban', {}).get('name')} -> Biến: {luc_hao_data.get('bien', {}).get('name')}\\n"
            extra_context += f"- Dụng Thần: {luc_hao_data.get('dung_than_label')}\\n"
            extra_context += f"- Kết Luận Sơ Bộ: {luc_hao_data.get('conclusion')}\\n"
            if luc_hao_data.get('dong_hao'):
                 extra_context += f"- Hào Động: {luc_hao_data.get('dong_hao')} (Động là nơi sự việc biến đổi).\\n"

        # C. VISIBLE REASONING PROMPT (V4.0 - TỨ THUẬT HỢP NHẤT)
        import datetime
        timestamp_str = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
        
        # 1. CALCULATE USER PALACE & STRENGTH (VƯỢNG SUY)
        user_palace_info = "KHÔNG XÁC ĐỊNH ĐƯỢC CUNG MỆNH"
        if chart_data and 'can_ngay' in chart_data and 'can_thien_ban' in chart_data:
            can_ngay = chart_data['can_ngay']
            # Find Palace containing Day Stem
            u_idx = None
            for idx, stem in chart_data['can_thien_ban'].items():
                if stem == can_ngay:
                    u_idx = idx
                    break
            
            if u_idx:
                # Get Attributes
                u_star = chart_data.get('thien_ban', {}).get(u_idx, '?')
                u_door = chart_data.get('nhan_ban', {}).get(u_idx, '?')
                u_deity = chart_data.get('than_ban', {}).get(u_idx, '?')
                
                # Determine Element Relationship (Simplified for AI Context)
                # This helps AI guess age: Vượng/Tướng -> Young/Strong; Hưu/Tù/Tử -> Old/Weak
                palace_element = CUNG_NGU_HANH.get(u_idx, 'Thổ')
                
                user_palace_info = (
                    f"USER LÀ CAN NGÀY '{can_ngay}', ĐANG NGỰ TẠI CUNG {u_idx} (Hành {palace_element}):\n"
                    f"- Sao (Tính Cách): {u_star}\n"
                    f"- Cửa (Hành Động): {u_door}\n"
                    f"- Thần (Tâm Linh): {u_deity}\n"
                    f"-> GỢI Ý XẠ PHÚC (ĐOÁN NGƯỜI):\n"
                    f"   + Nhìn vào tương tác giữa Can Ngày '{can_ngay}' và Cung {u_idx} ({palace_element}) để đoán độ tuổi (Vượng -> Trẻ, Suy -> Già).\n"
                    f"   + Nhìn vào tính chất Âm/Dương của Sao {u_star} và Cửa {u_door} để đoán Giới Tính."
                )

        # Fallback Context if no chart
        if not extra_context:
            extra_context = f"KHÔNG CÓ DỮ LIỆU BÀN CỜ. HÃY DÙNG THỜI GIAN HIỆN TẠI ĐỂ LUẬN: {timestamp_str}"

        prompt = (
            f"<system_instructions>\n"
            f"BẠN LÀ MỘT VỊ THIÊN CƠ LÃO TỔ - BẬC THẦY KỲ MÔN ĐỘN GIÁP VÀ TỨ THUẬT.\n"
            f"=== QUY TẮC BẮT BUỘC ===\n"
            f"1. LỆNH NGÔN NGỮ: BẮT BUỘC 100% TRẢ LỜI BẰNG TIẾNG VIỆT.\n"
            f"2. LỆNH THUYẾT TRÌNH: TRẢ LỜI TRỰC TIẾP VÀO TRỌNG TÂM THEO FORMAT CHỈ ĐỊNH. TUYỆT ĐỐI KHÔNG CHÀO HỎI, KHÔNG NÓI 'TÔI ĐÃ SẴN SÀNG', KHÔNG VÒNG VO! ❌\n"
            f"TUYỆT ĐỐI KHÔNG HIỂN THỊ CÁC BƯỚC SUY LUẬN BẰNG TIẾNG ANH (Như 'Okay, let's analyze...'). CHỈ ĐƯỢC PHÉP IN RA KẾT QUẢ CUỐI CÙNG.\n"
            f"3. CHỐNG SIÊU DÀI DÒNG: TUYỆT ĐỐI KHÔNG liệt kê hay đi phân tích vòng vo toàn bộ 9 cung. Hãy tập trung tổng hợp Tứ Thuật để đưa ra câu trả lời.\n"
            f"4. LUẬT TỐI CAO TUỔI TÁC: Năm {timestamp_str[-4:]} là NĂM XEM BÓI, KHÔNG PHẢI NĂM SINH.\n"
            f"5. ⛔ LUẬT TỬ HÌNH CHỐNG ÁO GIÁC (ANTI-HALLUCINATION): BẠN CHỈ ĐƯỢC PHÉP luận đoán dựa trên những Cung, Sao, Môn, Thần, Yếu Tố CÓ MẶT TRONG <context_data>. TUYỆT ĐỐI KHÔNG BỊA RA CÁC CUNG (NHƯ 'CUNG CÀN', 'CUNG VỊ') HAY KIẾN THỨC CHUNG CHUNG NẾU TỪ KHÓA ĐÓ KHÔNG CÓ TRONG KẾT QUẢ! ⛔\n"
            f"6. LỆNH BẮT BUỘC: Bạn phải đóng vai Thầy Bói thực thụ, không được tóm tắt chung chung. Hãy thực hiện quy trình sau:\n"
            f"  - Bước 1: Xác định Dụng Thần (chủ thể của câu hỏi là gì?).\n"
            f"  - Bước 2: Tìm trong Kỳ Môn xem Cung Mệnh của người hỏi (Cung của Can Ngày) và Cung Sự Việc (Cung của Dụng Thần/Can Giờ) tương sinh hay tương khắc.\n"
            f"  - Bước 3: Tìm trong Mai Hoa xem Thể và Dụng sinh khắc ra sao.\n"
            f"  - Bước 4: Khảo sát Lục Hào xem Hào Động báo hiệu điều gì, Dụng Thần vượng hay suy.\n"
            f"Lấy tất cả các dữ kiện có thật này chắp nối thành một câu trả lời chính xác, TUYỆT ĐỐI không chép lại dữ liệu MANG ĐOÁN nếu dữ liệu gốc chi tiết hơn.\n\n"
            f"BẮT BUỘC TRÌNH BÀY ĐÚNG 4 PHẦN THEO ĐÚNG THỨ TỰ SAU (Tuyệt đối không được bỏ sót Header nào, kể cả khi thiếu dữ liệu):\n"
            f"# 1. HỒ SƠ KHÁCH HÀNG\n"
            f"(TUYỆT ĐỐI KHÔNG TRẢ LỜI CÂU HỎI CHÍNH Ở PHẦN NÀY! Chỉ suy luận tuổi/giới tính nếu có dữ liệu. Nếu không, ghi 'Không đủ dữ liệu xác định')\n\n"
            f"# 2. CĂN CỨ TỨ THUẬT\n"
            f"(Bắt buộc phân tích logic tại đây dựa trên <context_data>. Nếu môn nào thiếu, ghi 'Chưa gieo quẻ')\n"
            f"- KỲ MÔN: ...\n"
            f"- MAI HOA: ...\n"
            f"- LỤC HÀO: ...\n"
            f"- THIẾT BẢN: ...\n\n"
            f"# 3. KẾT QUẢ DỰ BÁO\n"
            f"(CHỈ ĐƯỢC PHÉP TRẢ LỜI CÂU HỎI TRỰC TIẾP TẠI ĐÂY. Tổng hợp logic từ Phần 2 để chốt ĐÁP ÁN)\n\n"
            f"# 4. LỜI KHUYÊN\n"
            f"(1 câu hành động thiết thực)\n"
            f"</system_instructions>\n\n"
            f"<context_data>\n"
            f"{user_palace_info}\n"
            f"{extra_context}\n"
            f"</context_data>\n\n"
            f"<user_question>\n"
            f"{question}\n"
            f"</user_question>"
        )
        return self._call_ai_raw(prompt)

    # --- MISSING METHODS RESTORED & UPGRADED FOR "SMARTEST AI" ---
    
    def analyze_palace(self, palace_data, topic):
        """Analyzes a specific QMDG Palace with context (V3.5 Prophet Mode)."""
        p_num = palace_data.get('num', '?')
        prompt = (
            f"VAI TRÒ: Chuyên gia Kỳ Môn Độn Giáp (V3.5 Prophet Mode).\\n"
            f"NHIỆM VỤ: Phân tích CÁT HUNG của Cung {p_num} theo chủ đề '{topic}'.\\n"
            f"--------------------------------------------------\\n"
            f"DỮ LIỆU CUNG {p_num}:\\n"
            f"- Cửa: {palace_data.get('door')} | Sao: {palace_data.get('star')} | Thần: {palace_data.get('deity')}\\n"
            f"- Thiên Bàn: {palace_data.get('can_thien')} | Địa Bàn: {palace_data.get('can_dia')}\\n"
            f"--------------------------------------------------\\n"
            f"QUY TRÌNH LUẬN GIẢI (V3.5):\\n"
            f"1. **NGHĨA ĐỘNG (Contextual)**: Xét ý nghĩa Cửa/Sao dựa trên '{topic}'. (Ví dụ: Cửa Tử xấu cho Hôn nhân nhưng tốt cho Săn bắn/Tu luyện).\\n"
            f"2. **TƯƠNG TÁC NGŨ HÀNH**: Xét sự sinh khắc giữa Cửa - Cung - Sao - Thần.\\n"
            f"3. **YẾU TỐ ẨN**: Tự xét xem có phạm Tuần Không hay Dịch Mã không (dựa trên kiến thức của bạn về Kỳ Môn).\\n"
            f"\\n"
            f"KẾT LUẬN:\\n"
            f"🔮 **Đánh Giá**: [Tốt/Xấu/Trung Bình]\\n"
            f"💡 **Lý Do Chính**: [Giải thích ngắn gọn, súc tích]\\n"
        )
        return self._call_ai_raw(prompt)

    def explain_element(self, element_type, value):
        """Explains a specific QMDG element (Stem, Star, Door)."""
        prompt = (
            f"VAI TRÒ: Từ điển Sống về Kỳ Môn Độn Giáp (V3.5).\\n"
            f"YÊU CẦU: Giải thích ý nghĩa của {element_type}: {value}.\\n"
            f"1. **Ý Nghĩa Gốc**: Cát hay Hung?\\n"
            f"2. **Ý Nghĩa Mở Rộng**: Tốt cho việc gì, xấu cho việc gì?\\n"
            f"3. **Hình Tượng**: Nó đại diện cho người/vật gì?"
        )
        return self._call_ai_raw(prompt)

    def analyze_mai_hoa(self, hex_data, topic):
        """Analyzes Mai Hoa Hexagram (V3.5 Prophet Mode)."""
        ten = hex_data.get('ten', 'Quẻ')
        tuong = hex_data.get('tuong', 'Image')
        nghia = hex_data.get('nghĩa', 'Meaning')
        prompt = (
            f"VAI TRÒ: Nhà Tiên Tri Mai Hoa (V3.5).\\n"
            f"CHỦ ĐỀ: {topic}\\n"
            f"QUẺ: {ten}\\n"
            f"TƯỢNG: {tuong}\\n"
            f"Ý NGHĨA: {nghia}\\n"
            f"--------------------------------------------------\\n"
            f"PHÂN TÍCH TIÊN TRI:\\n"
            f"Hãy nhìn vào 'Tượng Quẻ' (Hình ảnh) để đưa ra dự báo cho '{topic}'.\\n"
            f"Đừng chỉ tra sách, hãy dùng Trực Giác Tiên Tri để kết nối hình ảnh với sự việc.\\n"
            f"KẾT QUẢ: Cát hay Hung? Tại sao?"
        )
        return self._call_ai_raw(prompt)
        
    def analyze_luc_hao(self, hex_data, topic):
        """Analyzes Luc Hao Hexagram (V3.5 Prophet Mode)."""
        ban = hex_data.get('ban', {}).get('name', '?')
        bien = hex_data.get('bien', {}).get('name', '?')
        conclusion = hex_data.get('conclusion', '...')
        prompt = (
            f"VAI TRÒ: Chuyên gia Lục Hào Thần Sát (V3.5).\\n"
            f"CHỦ ĐỀ: {topic}\\n"
            f"DIỄN BIẾN: Quẻ {ban} biến thành {bien}\\n"
            f"LUẬN SƠ BỘ: {conclusion}\\n"
            f"--------------------------------------------------\\n"
            f"LUẬN GIẢI CHI TIẾT:\\n"
            f"1. **Động Hào**: Hào động báo hiệu sự thay đổi gì?\\n"
            f"2. **Biến Hóa**: Sự việc sẽ kết thúc (Quẻ Biến) như thế nào?\\n"
            f"3. **Lời Khuyên**: Nên tiến hay lùi?"
        )
        return self._call_ai_raw(prompt)



# -----------------------------------------------

# --- PHOENIX ORCHESTRATOR (INLINED TO FIX IMPORT CACHING) ---
class PhoenixOrchestrator:
    """
    Simulates an n8n-style workflow orchestration.
    Coordinates specialized Agents (Nodes) to answer user queries accurately.
    Inlined to prevent 'Empty Response' due to old cached modules.
    """
    
    def __init__(self, gemini_helper):
        self.gemini = gemini_helper
        self.logs = [] # Execution logs to show in UI
        
    def log_step(self, step_name, status, detail=""):
        import datetime
        entry = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "step": step_name,
            "status": status,
            "detail": detail
        }
        self.logs.append(entry)
        
    def run_pipeline(self, user_question, current_topic="Chung", chart_data=None, mai_hoa_data=None, luc_hao_data=None, tb_context=""):
        self.logs = [] # Reset logs
        final_answer = ""
        knowledge_context = ""
        
        # --- NODE 0: LIVE DATA INGESTION ---
        # AUTO-CAPTURE from session_state if arguments are missing (Smart Context)
        import streamlit as st
        if not mai_hoa_data and 'mai_hoa_result' in st.session_state:
            mai_hoa_data = st.session_state.mai_hoa_result
        if not luc_hao_data and 'luc_hao_result' in st.session_state:
            luc_hao_data = st.session_state.luc_hao_result
        if not chart_data and 'chart_data' in st.session_state:
            chart_data = st.session_state.chart_data
            
        live_context = self._format_live_context(chart_data, mai_hoa_data, luc_hao_data, current_topic)
        if live_context:
            knowledge_context += f"\\n[DỮ LIỆU BÀN CỜ & QUẺ (LIVE INTELLIGENCE)]:\\n{live_context}\\n"
            self.log_step("Live Data Ingestion", "SUCCESS", "Captured & Decoded QMDG/MaiHoa/LucHao.")
        else:
            self.log_step("Live Data Ingestion", "SKIPPED", "No active chart/hexagram found.")
            
        if tb_context:
            knowledge_context += f"\\n{tb_context}\\n"
            self.log_step("Live Data Ingestion", "SUCCESS", "Captured Thiet Ban Than Toan context.")
        
        # --- NODE 1: INTENT ROUTER (Regex Enhanced) ---
        self.log_step("Intent Analysis", "RUNNING", "Analyzing user question...")
        import re
        q_lower = f" {user_question.lower()} " # Padding for boundary matching
        intent = "GENERAL"

        # Regex Helpers
        def match_any(keywords, text):
            return any(re.search(rf"\\b{kw}\\b", text) for kw in keywords)

        # 1. Calculation
        if match_any(["giờ tốt", "xuất hành", "khổng minh", "tính giờ", "giờ nào"], q_lower):
            intent = "CALCULATION"
        # 2. Timing
        elif match_any(["khi nào", "bao giờ", "bao lâu", "tháng mấy", "năm nào", "ngày nào", "mấy giờ", "đến lúc nào"], q_lower):
            intent = "TIMING"
        # 3. People / Profile
        elif match_any(["ai", "người", "trai", "gái", "nam", "nữ", "ghét", "thương", "tính cách", "bản tính"], q_lower):
            intent = "PROFILE"
        # 4. Remedy
        elif match_any(["hóa giải", "cách sửa", "làm gì", "đối phó"], q_lower):
            intent = "REMEDY"
        # 5. Definition
        elif match_any(["là gì", "ý nghĩa", "giải thích", "định nghĩa"], q_lower):
            intent = "DEFINITION"
        # 6. Analysis
        elif match_any(["luận giải", "phân tích", "đánh giá", "xem giúp", "như thế nào", "kết quả", "thành bại", "được không"], q_lower):
            intent = "ANALYSIS"
            
        self.log_step("Intent Analysis", "COMPLETED", f"Detected Intent: {intent}")
        
        # --- NODE 2: KNOWLEDGE RETRIEVAL ---
        self.log_step("Knowledge Retrieval", "RUNNING", f"Fetching data for {intent}...")
        
        # Sub-Node: Forced Topic Override
        people_time_keywords = ["ai", "người", "trai", "gái", "nam", "nữ", "khi nào", "bao giờ", "lúc nào", "mấy giờ", "ghét", "thương"]
        topic_override = any(kw in q_lower for kw in people_time_keywords) or intent in ["PROFILE", "TIMING"]
        
        # Sub-Node: Time Horizon Hint
        time_horizon = "FUTURE"
        if any(x in q_lower for x in ["đã", "vừa mới", "quá khứ", "trước đây"]):
            time_horizon = "PAST"
        knowledge_context += f"\\n[GỢI Ý THỜI ĐIỂM]: {time_horizon}\\n"

        # Sub-Node: Dictionary Skill
        try:
            from skill_library import lookup_concept
            dict_data = lookup_concept(user_question)
            if dict_data:
                self.log_step("Dictionary Skill", "SUCCESS", f"Found definition for input term.")
                knowledge_context += f"\\n[📖 TỪ ĐIỂN CHUYÊN NGÀNH]: {dict_data['summary']}\\nChi tiết: {dict_data['details']}\\n"
            
            # Sub-Node: Object Mapping
            dung_than_data = lookup_concept("dụng thần")
            if dung_than_data:
                 knowledge_context += f"\\n[🔍 BẢNG TRA CỨU ĐỐI TƯỢNG (DỤNG THẦN)]: {dung_than_data['summary']}\\nChi tiết: {dung_than_data['details']}\\n"
                 self.log_step("Object Mapping", "SUCCESS", "Loaded Reference Objects Table.")

            # Sub-Node: Timing/Remedy/Weather
            for skill_key, skill_intent in [("ứng kỳ", "TIMING"), ("hóa giải", "REMEDY"), ("thời tiết", "WEATHER")]:
                if intent == skill_intent:
                    skill_data = lookup_concept(skill_key)
                    if skill_data:
                         knowledge_context += f"\\n[🔍 QUY TẮC CHUẨN - {skill_key.upper()}]:\\n{skill_data['details']}\\n"
                         self.log_step(f"{skill_key.capitalize()} Skill", "SUCCESS", f"Loaded Rules for {skill_intent}")
            
            # Sub-Node: Personality & Gender
            if intent == "PROFILE" or any(kw in q_lower for kw in ["tính cách", "nam", "nữ", "trai", "gái", "ai"]):
                profile_data = lookup_concept("tính cách")
                gender_data = lookup_concept("nam nữ")
                if profile_data: knowledge_context += f"\\n[👤 TỪ ĐIỂN TÍNH CÁCH]:\\n{profile_data['details']}\\n"
                if gender_data: knowledge_context += f"\\n[⚧️ QUY TẮC XEM GIỚI TÍNH (Nam/Nữ)]:\\n{gender_data['details']}\\n"
                self.log_step("Profile Skill", "SUCCESS", "Loaded Profile & Gender Rules.")
        except:
            self.log_step("Skill Library", "WARNING", "Could not import skill_library. Skipping.")

        # Sub-Node: Topic Context
        if not topic_override and intent in ["ANALYSIS", "GENERAL", "DEFINITION"]:
            try:
                import qmdg_data
                topic_dict = getattr(qmdg_data, 'TOPIC_INTERPRETATIONS', {})
                if current_topic in topic_dict:
                     t_data = topic_dict[current_topic]
                     knowledge_context += f"\\n[CHỦ ĐỀ ĐANG XEM TRÊN UI]: {current_topic}\\n- Dụng thần chuẩn: {t_data.get('Dụng_Thần')}\\n- Gợi ý luận giải: {t_data.get('Luận_Giải_Gợi_Ý')}\\n"
                     self.log_step("Topic Context", "SUCCESS", f"Injected context for {current_topic}")
            except: pass
        else:
            self.log_step("Topic Context", "SKIPPED", "Ignored UI topic to focus on specific Person/Time query.")
        
        # Sub-Node: Time Calculation Skill
        if intent == "CALCULATION":
            try:
                import datetime
                import streamlit as st
                d_val = datetime.datetime.now()
                if hasattr(st, 'session_state') and 'selected_date' in st.session_state:
                     d_val = st.session_state.selected_date
                from ai_tools import get_lunar_date_offline, get_khong_minh_luc_dieu
                lm, ld = get_lunar_date_offline(d_val)
                summ, det = get_khong_minh_luc_dieu(lm, ld)
                knowledge_context += f"\\n[⏱️ TÍNH TOÁN THỜI GIAN]:\\n{summ}\\n{det}\\n"
                self.log_step("Time Calc Skill", "SUCCESS", f"Calculated for Lunar Date {ld}/{lm}")
            except Exception as e:
                self.log_step("Time Calc Skill", "ERROR", str(e))
                
        self.log_step("Knowledge Retrieval", "COMPLETED", "Data gathering finished.")
        
        # --- NODE 3: CONTEXT MEMORY ---
        self.log_step("Context Memory", "RUNNING", "Retrieving session history...")
        history_context = ""
        import streamlit as st
        if hasattr(st, 'session_state') and 'chat_history' in st.session_state:
            recent_history = st.session_state.chat_history[-6:] 
            history_context = "\\n[LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY]:\\n"
            for msg in recent_history:
                role = "Bạn" if msg["role"] == "user" else "AI"
                history_context += f"- {role}: {msg['content'][:100]}...\\n"
        self.log_step("Context Memory", "SUCCESS", "Internal memory updated.")

        # --- NODE 4: SYNTHESIS ---
        self.log_step("Gemini Synthesis", "RUNNING", "Generating final response...")
        
        import datetime as _dt_prompt
        _now_ts = _dt_prompt.datetime.now()
        
        # V5.0: MANG ĐOÁN - Pre-computed blind reading
        _blind_text = ""
        try:
            from blind_reading import blind_read, format_blind_reading
            _chart = st.session_state.get('chart_data', None)
            _mh = st.session_state.get('mai_hoa_result', None)
            _lh = st.session_state.get('luc_hao_result', None)
            _readings = blind_read(chart_data=_chart, mai_hoa_data=_mh, luc_hao_data=_lh)
            _blind_text = format_blind_reading(_readings)
        except Exception as _e:
            _blind_text = f"(Lỗi Mang Đoán: {_e})"
        system_prompt = (
            f"<system_instructions>\n"
            f"Bạn là Bậc Thầy Tứ Thuật (Kỳ Môn, Mai Hoa, Lục Hào, Thiết Bản). Năm {_now_ts.year} là năm xem bói.\n"
            f"LUẬT TOÁN MỆNH BẮT BUỘC:\n"
            f"- LỆNH NGÔN NGỮ: BẮT BUỘC 100% TRẢ LỜI BẰNG TIẾNG VIỆT.\n"
            f"- LỆNH THUYẾT TRÌNH: TRẢ LỜI NGAY VÀO FORMAT, TUYỆT ĐỐI KHÔNG HIỂN THỊ DÒNG SUY NGHĨ HAY CÁC BƯỚC PHÂN TÍCH BẰNG TIẾNG ANH (Như 'Okay, let's analyze...'). ❌ TUYỆT ĐỐI KHÔNG CHÀO HỎI, KHÔNG NÓI 'TÔI ĐÃ SẴN SÀNG'. ❌\n"
            f"- ⛔ LUẬT TỬ HÌNH CHỐNG ÁO GIÁC (ANTI-HALLUCINATION): BẠN CHỈ ĐƯỢC PHÉP LUẬN DỰA TRÊN DỮ LIỆU TRONG <context_data>! NẾU QUẺ KHÔNG NHẮC ĐẾN 'CUNG CÀN', THÌ TUYỆT ĐỐI KHÔNG ĐƯỢC CHÉM GIÓ VỀ 'CUNG CÀN'. CHỈ DÙNG DỮ LIỆU CÓ THẬT!!! ⛔\n"
            f"- KHÔNG được lười biếng tóm tắt chung chung. Bạn PHẢI đóng vai Thầy Bói thực thụ, thực hiện quy trình sau dựa trên <context_data>:\n"
            f"   + Bước 1: Xác định Dụng Thần (chủ thể của câu hỏi là gì?).\n"
            f"   + Bước 4: Khảo sát Lục Hào xem Hào Động báo hiệu điều gì, Dụng Thần vượng hay suy.\n"
            f"   + Bước 5: Tham chiếu Thiết Bản Thần Toán xem điềm báo thời cơ là gì.\n"
            f"   Lấy tất cả các dữ kiện có thật này chắp nối thành một câu trả lời chính xác, sắc bén và TUYỆT ĐỐI KHÔNG BỊA ĐẶT.\n\n"
            f"=========================================\n"
            f"📖 CẨM NANG DỤNG THẦN VẠN NĂNG (UNIVERSAL RULEBOOK)\n"
            f"Dùng cẩm nang này để tự suy luận Dụng Thần cho BẤT KỲ CÂU HỎI NÀO của người dùng:\n\n"
            f"1. LỤC THÂN (LỤC HÀO) - ĐẠI DIỆN CHO:\n"
            f"- HÀO QUAN QUỶ: Nghề nghiệp, chức vụ, sếp, bệnh tật, ma quỷ, tai họa, trộm cướp, chồng/bạn trai.\n"
            f"- HÀO THÊ TÀI: Tiền bạc, tài sản, lợi nhuận, đồ ăn, vợ/bạn gái, thuộc cấp, người làm thuê.\n"
            f"- HÀO TỬ TÔN: Con cái, cháu chắt, thú cưng, thuốc men chữa bệnh, sự bình an, đường gỡ rối.\n"
            f"- HÀO PHỤ MẪU: Cha mẹ, người lớn tuổi, nhà cửa, đất đai, xe cộ, trường học, quần áo, giấy tờ, hợp đồng, tin tức.\n"
            f"- HÀO HUYNH ĐỆ: Anh chị em, bạn bè, đối tác, đối thủ cạnh tranh, người chia tiền.\n\n"
            f"2. KỲ MÔN DỤNG THẦN - ĐẠI DIỆN CHO:\n"
            f"- Nhật Can (Can Ngày): Bản thân người hỏi.\n"
            f"- Thời Can (Can Giờ): Sự việc chung, kết quả, con cái, súc vật, cấp dưới.\n"
            f"- Nguyệt Can (Can Tháng): Anh em, bạn bè, đồng nghiệp.\n"
            f"- Niên Can (Can Năm): Cha mẹ, trưởng bối, sếp lớn, chính quyền.\n"
            f"- Khai Môn: Công việc, sự nghiệp, cửa hàng, mở mang.\n"
            f"- Sinh Môn: Lợi nhuận, tiền tài, nhà cửa, sự sống, nghề địa ốc.\n"
            f"- Tử Môn: Chết chóc, bệnh tật, đất đai, mồ mả, sự bế tắc.\n"
            f"- Cảnh Môn: Thư từ, giấy báo, thi cử, hình ảnh, hỏa hoạn.\n"
            f"- Thiên Tâm: Bác sĩ, thuốc men, quý nhân, người lãnh đạo.\n"
            f"- Trực Phù: VIP, sếp, chủ nợ, tài sản lớn.\n"
            f"- Huyền Vũ / Thiên Bồng: Trộm cướp, tiểu nhân, sự lừa dối, mất mát.\n\n"
            f"3. CÔNG THỨC TOÁN SỐ BÍ TRUYỀN (Tính Số Lượng/Tuổi Tác):\n"
            f"- Nếu hỏi số lượng (bao nhiêu người, mấy cái nhà, mấy tầng, mấy tỷ, mấy con thú...): Chọn Cung Kỳ Môn chứa Dụng Thần. Số lượng = Số Hà Đồ của Cung đó (Khảm=1/6, Khôn=2/7, Chấn=3/8, Tốn=4/9, Trung=5/10, Càn=1/6, Đoài=4/9, Cấn=5/10, Ly=2/7). Nếu Cung Vượng/Tướng dồi dào -> Lấy số LỚN. Nếu Suy/Tuyệt -> Lấy số NHỎ.\n"
            f"=========================================\n\n"
            f"BẮT BUỘC TRÌNH BÀY ĐÚNG 4 PHẦN THEO ĐÚNG THỨ TỰ SAU (Tuyệt đối không được bỏ sót Header nào, kể cả khi thiếu dữ liệu):\n"
            f"# 1. HỒ SƠ KHÁCH HÀNG\n"
            f"(TUYỆT ĐỐI KHÔNG TRẢ LỜI CÂU HỎI CHÍNH Ở PHẦN NÀY! Chỉ suy luận tuổi/giới tính nếu có dữ liệu. Nếu không, ghi 'Không đủ dữ liệu xác định')\n\n"
            f"# 2. CĂN CỨ TỨ THUẬT\n"
            f"(Bắt buộc phân tích logic tại đây dựa trên <context_data>. Nếu môn nào thiếu, ghi 'Chưa gieo quẻ')\n"
            f"- KỲ MÔN: ...\n"
            f"- MAI HOA: ...\n"
            f"- LỤC HÀO: ...\n"
            f"- THIẾT BẢN: ...\n\n"
            f"# 3. KẾT QUẢ DỰ BÁO\n"
            f"(CHỈ ĐƯỢC PHÉP TRẢ LỜI CÂU HỎI TRỰC TIẾP TẠI ĐÂY. Tổng hợp logic từ Phần 2 để chốt ĐÁP ÁN. Nếu Phần 2 hoàn toàn không có dữ liệu, hãy ghi 'Do hệ thống chưa nhận được dữ liệu bàn cờ nên không thể đưa ra đáp án chính xác')\n\n"
            f"# 4. LỜI KHUYÊN\n"
            f"(1 câu hành động thiết thực)\n"
            f"</system_instructions>\n\n"
            f"<context_data>\n"
            f"{history_context}\n{knowledge_context}\n{_blind_text}\n"
            f"</context_data>\n\n"
            f"<user_question>\n"
            f"{user_question}\n"
            f"</user_question>"
        )
        
        try:
            final_answer = self.gemini._call_ai(system_prompt)
        except Exception as e:
            self.log_step("Gemini Synthesis", "ERROR", str(e))
            final_answer = f"⚠️ Lỗi xử lý AI: {str(e)}"
            
        if not final_answer:
             final_answer = "⚠️ AI trả về dữ liệu rỗng (Phoenix Fix). Vui lòng thử lại."
             
        return final_answer

    def _format_live_context(self, qmdg, mai_hoa, luc_hao, current_topic="Chung"):
        context = ""
        import json
        import datetime
        
        # Helper string force
        def safe_str(val):
            return str(val) if val is not None else "Unknown"

        # Helper to safely get nested keys
        def get_safe(data, key):
            val = data.get(key, "N/A") if data else "N/A"
            return str(val)

        # --- LOAD TRUCTU_TRANH & CAN_CHI DATA FOR CÁCH CỤC LOOKUP ---
        TRUCTU_TRANH = {}
        CAN_CHI_LUAN_GIAI = {}
        CUU_TINH_DATA = {}
        BAT_MON_DATA = {}
        BAT_THAN_DATA = {}
        try:
            import qmdg_data
            KY_MON = getattr(qmdg_data, 'KY_MON_DATA', {})
            TRUCTU_TRANH = KY_MON.get('TRUCTU_TRANH', {})
            CAN_CHI_LUAN_GIAI = KY_MON.get('CAN_CHI_LUAN_GIAI', {})
            dung_than = KY_MON.get('DU_LIEU_DUNG_THAN_PHU_TRO', {})
            CUU_TINH_DATA = dung_than.get('CUU_TINH', {})
            BAT_MON_DATA = dung_than.get('BAT_MON', {})
            BAT_THAN_DATA = dung_than.get('BAT_THAN', {})
        except Exception:
            pass

        # --- Helper: Lookup Cách Cục for a palace ---
        def lookup_cach_cuc(can_thien, can_dia):
            if not can_thien or not can_dia or can_thien == 'N/A' or can_dia == 'N/A':
                return None
            key = f"{can_thien}{can_dia}"
            return TRUCTU_TRANH.get(key, None)

        # --- Helper: Ngũ Hành relationship ---
        NGU_HANH_MAP = {"Mộc": 0, "Hỏa": 1, "Thổ": 2, "Kim": 3, "Thủy": 4}
        def ngu_hanh_relation(hanh1, hanh2):
            if not hanh1 or not hanh2: return "Không rõ"
            idx1 = NGU_HANH_MAP.get(hanh1, -1)
            idx2 = NGU_HANH_MAP.get(hanh2, -1)
            if idx1 < 0 or idx2 < 0: return "Không rõ"
            diff = (idx2 - idx1) % 5
            return {0: "Tỷ Hòa (ngang nhau)", 1: "Sinh (tốt, hỗ trợ)", 2: "Khắc (xấu, bị chế ngự)", 3: "Bị Khắc (bị tổn thương)", 4: "Được Sinh (được hỗ trợ)"}[diff]

        def get_hanh_of_can(can_name):
            info = CAN_CHI_LUAN_GIAI.get(can_name, {})
            return info.get('Hành', 'Thổ')

        # --- CUNG NGŨ HÀNH (Palace elements) ---
        CUNG_NGU_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}

        # --- 0. IDENTITY AUTO-DETECT ---
        can_ngay_val = "Giáp"
        can_nam_val = "Bính"
        t_tru = "N/A"
        
        if qmdg:
            can_ngay_val = get_safe(qmdg, 'can_ngay')
            can_nam_val = get_safe(qmdg, 'can_nam')
            t_tru = f"{get_safe(qmdg, 'can_nam')} {get_safe(qmdg, 'chi_nam')} / {get_safe(qmdg, 'can_thang')} {get_safe(qmdg, 'chi_thang')} / {can_ngay_val} {get_safe(qmdg, 'chi_ngay')} / {get_safe(qmdg, 'can_gio')} {get_safe(qmdg, 'chi_gio')}"
        else:
            try:
                from qmdg_calc import calculate_qmdg_params
                now = datetime.datetime.now()
                params = calculate_qmdg_params(now) 
                can_ngay_val = safe_str(params.get('can_ngay', 'Giáp'))
                can_nam_val = safe_str(params.get('can_nam', 'Bính'))
                def p(k): return safe_str(params.get(k, '?'))
                t_tru = f"{p('can_nam')} {p('chi_nam')} / {p('can_thang')} {p('chi_thang')} / {can_ngay_val} {p('chi_ngay')} / {p('can_gio')} {p('chi_gio')}"
            except Exception as e:
                t_tru = "Dữ liệu tính toán bị lỗi"
                context += f"[LỖI TÍNH TOÁN ẨN]: {e}\n"

        # --- 1. LỊCH ÂM/DƯƠNG (Calendar) - Lấy từ session state (đã có timezone VN) ---
        try:
            import qmdg_calc
            import streamlit as st
            # Lấy thời gian từ session state (đã tính sẵn ở sidebar, timezone VN)
            if 'selected_datetime' in dir(st.session_state) or True:
                try:
                    # Try to get VN timezone
                    vn_tz = None
                    try:
                        import pytz
                        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
                    except:
                        try:
                            from zoneinfo import ZoneInfo
                            vn_tz = ZoneInfo("Asia/Ho_Chi_Minh")
                        except:
                            vn_tz = datetime.timezone(datetime.timedelta(hours=7))
                    now = datetime.datetime.now(vn_tz)
                except:
                    now = datetime.datetime.now() + datetime.timedelta(hours=7)  # Fallback: UTC+7
            
            tomorrow = now + datetime.timedelta(days=1)
            
            lday_today, lmonth_today, lyear_today, is_leap_today = qmdg_calc.solar_to_lunar(now)
            lday_tmr, lmonth_tmr, lyear_tmr, is_leap_tmr = qmdg_calc.solar_to_lunar(tomorrow)
            
            l_year_can_today, l_year_chi_today = qmdg_calc.get_can_chi_year(lyear_today)
            l_year_can_tmr, l_year_chi_tmr = qmdg_calc.get_can_chi_year(lyear_tmr)
            
            # Can Chi ngày hôm nay và ngày mai
            params_today = qmdg_calc.calculate_qmdg_params(now)
            params_tmr = qmdg_calc.calculate_qmdg_params(tomorrow)
            canchi_today = f"{params_today.get('can_ngay','?')} {params_today.get('chi_ngay','?')}"
            canchi_tmr = f"{params_tmr.get('can_ngay','?')} {params_tmr.get('chi_ngay','?')}"
            
            context += f"=== LỊCH NGÀY (CHÍNH XÁC - TIMEZONE VIỆT NAM) ===\n"
            context += f"HÔM NAY: Dương lịch {now.strftime('%d/%m/%Y')} | Âm lịch: {lday_today}/{lmonth_today} năm {l_year_can_today} {l_year_chi_today}{'(Nhuận)' if is_leap_today else ''} | Ngày {canchi_today}\n"
            context += f"NGÀY MAI: Dương lịch {tomorrow.strftime('%d/%m/%Y')} | Âm lịch: {lday_tmr}/{lmonth_tmr} năm {l_year_can_tmr} {l_year_chi_tmr}{'(Nhuận)' if is_leap_tmr else ''} | Ngày {canchi_tmr}\n"
        except Exception:
            pass

        # --- 2. IDENTITY HINTS ---
        can_yang = ["Giáp", "Bính", "Mậu", "Canh", "Nhâm"]
        is_yang = any(k in can_ngay_val for k in can_yang)
        gender_hint = "NAM (Can Ngày Dương)" if is_yang else "NỮ (Can Ngày Âm)"
        
        context += f"\n=== DỮ LIỆU LUẬN GIẢI CHUẨN ===\n"
        context += f"Tứ Trụ: {t_tru}\n"
        context += f"Giới Tính (Theo Can Ngày): {gender_hint}\n"

        # --- 3. QMDG FULL ANALYSIS WITH CÁCH CỤC ---
        if qmdg:
            context += f"\n=== KỲ MÔN ĐỘN GIÁP ===\n"
            context += f"Tiết Khí: {get_safe(qmdg, 'tiet_khi')} | Cục: {get_safe(qmdg, 'cuc')}\n"
            
            can_thien_ban = qmdg.get('can_thien_ban', {})
            can_dia_ban = qmdg.get('can_dia_ban', {})
            thien_ban = qmdg.get('thien_ban', {})
            nhan_ban = qmdg.get('nhan_ban', {})
            than_ban = qmdg.get('than_ban', {})
            
            # Find USER palace (Can Ngày) and TOPIC palace
            user_palace_idx = None
            for idx, stem in can_thien_ban.items():
                if stem == can_ngay_val:
                    user_palace_idx = idx
                    break
            
            # Build focused analysis for each palace
            key_palaces = {}
            for idx in [1,2,3,4,6,7,8,9]:
                ct = safe_str(can_thien_ban.get(idx, can_thien_ban.get(str(idx), '?')))
                cd = safe_str(can_dia_ban.get(idx, can_dia_ban.get(str(idx), '?')))
                star = safe_str(thien_ban.get(idx, thien_ban.get(str(idx), '?')))
                door = safe_str(nhan_ban.get(idx, nhan_ban.get(str(idx), '?')))
                deity = safe_str(than_ban.get(idx, than_ban.get(str(idx), '?')))
                
                cach_cuc = lookup_cach_cuc(ct, cd)
                cach_cuc_str = ""
                if cach_cuc:
                    cach_cuc_str = f" | CÁCH CỤC: {cach_cuc.get('Tên_Cách_Cục','?')} ({cach_cuc.get('Cát_Hung','?')}) - {cach_cuc.get('Luận_Giải','')}"
                
                # Get Cát/Hung from star & door data
                star_info = CUU_TINH_DATA.get(star, {})
                door_full = f"{door} Môn" if door and "Môn" not in door else door
                door_info = BAT_MON_DATA.get(door_full, BAT_MON_DATA.get(door, {}))
                deity_info = BAT_THAN_DATA.get(deity, {})
                
                hanh_cung = CUNG_NGU_HANH.get(int(idx) if isinstance(idx, str) else idx, 'Thổ')
                
                palace_line = (
                    f"  Cung {idx} ({hanh_cung}): Sao={star}({star_info.get('Hành','?')}) | "
                    f"Cửa={door}({door_info.get('Cát_Hung','?')}) | Thần={deity} | "
                    f"Can: {ct}/{cd}{cach_cuc_str}"
                )
                
                key_palaces[idx] = {
                    'line': palace_line, 'star': star, 'door': door, 'deity': deity,
                    'can_thien': ct, 'can_dia': cd, 'cach_cuc': cach_cuc,
                    'hanh_cung': hanh_cung, 'star_info': star_info, 'door_info': door_info
                }
            
            # USER PALACE ANALYSIS (FOCUSED)
            if user_palace_idx and user_palace_idx in key_palaces:
                up = key_palaces[user_palace_idx]
                context += f"\n★ CUNG CHỦ (User - Can Ngày '{can_ngay_val}' tại Cung {user_palace_idx}):\n"
                context += f"{up['line']}\n"
                hanh_can = get_hanh_of_can(can_ngay_val)
                rel = ngu_hanh_relation(hanh_can, up['hanh_cung'])
                context += f"  → Ngũ Hành: Can {can_ngay_val}({hanh_can}) vs Cung({up['hanh_cung']}) = {rel}\n"
            
            # 8 PALACES (compact) - DISABLED TO PREVENT WORD SALAD
            # context += f"\n📋 TOÀN BÀN (8 Cung + Cách Cục):\n"
            # for idx in [1,2,3,4,6,7,8,9]:
            #     if idx in key_palaces:
            #         context += f"{key_palaces[idx]['line']}\n"
            pass
            
        # --- 4. MAI HOA (DEEP) ---
        if mai_hoa:
            mh_ten = get_safe(mai_hoa, 'ten')
            mh_dong = get_safe(mai_hoa, 'dong_hao')
            mh_bien = get_safe(mai_hoa, 'ten_qua_bien')
            mh_upper_e = get_safe(mai_hoa, 'upper_element')
            mh_lower_e = get_safe(mai_hoa, 'lower_element')
            mh_upper_s = get_safe(mai_hoa, 'upper_symbol')
            mh_lower_s = get_safe(mai_hoa, 'lower_symbol')
            
            # Thể Dụng sinh khắc analysis
            the_dung_rel = ""
            NGU_HANH_ORD = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
            if mh_upper_e in NGU_HANH_ORD and mh_lower_e in NGU_HANH_ORD:
                i1 = NGU_HANH_ORD.index(mh_upper_e)
                i2 = NGU_HANH_ORD.index(mh_lower_e)
                diff = (i2 - i1) % 5
                rel_map = {0: "Tỷ Hòa", 1: "Sinh", 2: "Khắc", 3: "Bị Khắc", 4: "Được Sinh"}
                the_dung_rel = f"Ngoại ({mh_upper_e}) vs Nội ({mh_lower_e}) = {rel_map.get(diff, '?')}"
            
            context += f"\n=== MAI HOA DỊCH SỐ ===\n"
            context += f"Quẻ Chủ: {mh_ten} ({mh_upper_s} / {mh_lower_s})\n"
            context += f"Thể: {get_safe(mai_hoa, 'ten_the')} | Dụng: {get_safe(mai_hoa, 'ten_dung')}\n"
            context += f"Tượng: {get_safe(mai_hoa, 'tuong')}\n"
            context += f"Ý Nghĩa: {get_safe(mai_hoa, 'nghĩa')}\n"
            context += f"Động Hào: {mh_dong} | Quẻ Biến: {mh_bien}\n"
            context += f"Thể Dụng Ngũ Hành: {the_dung_rel}\n"
            context += f"→ Thể sinh Dụng = CÁT (tốt cho mình), Dụng khắc Thể = HUNG.\n"

        # --- 5. LỤC HÀO (DEEP) ---
        if luc_hao:
            context += f"\n=== LỤC HÀO KINH DỊCH ===\n"
            ban_info = luc_hao.get('ban', {})
            bien_info = luc_hao.get('bien', {})
            lh_ten = get_safe(ban_info, 'name')
            lh_bien = get_safe(bien_info, 'name')
            lh_palace = get_safe(ban_info, 'palace')
            context += f"Quẻ: {lh_ten} (Họ {lh_palace}) biến {lh_bien}\n"
            context += f"Dụng Thần: {get_safe(luc_hao, 'dung_than_label')}\n"
            context += f"Thế Ứng: {get_safe(luc_hao, 'the_ung')}\n"
            context += f"Hào Động: {get_safe(luc_hao, 'dong_hao')}\n"
            
            # Chi tiết 6 hào
            ban_details = ban_info.get('details', [])
            if ban_details:
                context += "Chi Tiết 6 Hào:\n"
                for d in ban_details:
                    h_num = d.get('hao', '?')
                    lt = d.get('luc_than', '?')
                    cc = d.get('can_chi', '?')
                    lthu = d.get('luc_thu', '?')
                    stren = d.get('strength', '?')
                    moving = "⚡ĐỘNG" if d.get('is_moving', False) else ""
                    mk = d.get('marker', '')
                    lm = d.get('loc_ma', '')
                    context += f"  Hào {h_num}: {lt} | {cc} | {lthu} | {stren} {moving} {mk} {lm}\n"
            
            context += f"Kết Luận Sơ Bộ: {get_safe(luc_hao, 'conclusion')}\n"
            context += f"→ Dụng Thần Vượng = CÁT, Dụng Thần Suy/Tuyệt = HUNG.\n"

        # --- 6. THIẾT BẢN THẦN TOÁN (DEEP) ---
        try:
            # Load from JSON file first, then fallback
            tb_data = None
            try:
                import os as _os
                json_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "thiet_ban_than_toan.json")
                if _os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        tb_data = json.load(f)
            except: pass
            
            if not tb_data:
                import qmdg_data
                tb_data = getattr(qmdg_data, 'KY_MON_DATA', {}).get("THIET_BAN_THAN_TOAN", {})
            
            hoa_giap = tb_data.get("LUC_THAP_HOA_GIAP_NAP_AM", {})
            
            nam_tru = f"{can_nam_val} {get_safe(qmdg, 'chi_nam')}" if qmdg else f"{can_nam_val} {params.get('chi_nam','?')}"
            ngay_tru = f"{can_ngay_val} {get_safe(qmdg, 'chi_ngay')}" if qmdg else f"{can_ngay_val} {params.get('chi_ngay','?')}"
            
            na_nam_info = hoa_giap.get(nam_tru.strip(), {})
            na_ngay_info = hoa_giap.get(ngay_tru.strip(), {})
            na_nam = na_nam_info.get("Nạp_Âm", "Không rõ")
            na_nam_hanh = na_nam_info.get("Hành", "?")
            na_nam_yn = na_nam_info.get("Ý_Nghĩa", "")
            na_ngay = na_ngay_info.get("Nạp_Âm", "Không rõ")
            na_ngay_hanh = na_ngay_info.get("Hành", "?")
            na_ngay_yn = na_ngay_info.get("Ý_Nghĩa", "")
            
            context += f"\n=== THIẾT BẢN THẦN TOÁN ===\n"
            context += f"Mệnh Năm ({nam_tru.strip()}): {na_nam} (Hành {na_nam_hanh}) - {na_nam_yn}\n"
            context += f"Mệnh Ngày ({ngay_tru.strip()}): {na_ngay} (Hành {na_ngay_hanh}) - {na_ngay_yn}\n"
            
            # Trường Sinh 12 Giai Đoạn
            truong_sinh = tb_data.get("TRUONG_SINH_12_GIAI_DOAN", {})
            nh_ts_tai = truong_sinh.get("Ngũ_Hành_Trường_Sinh_Tại", {})
            giai_doan_map = truong_sinh.get("Giai_Đoạn", {})
            chi_ngay_check = get_safe(qmdg, 'chi_ngay') if qmdg else params.get('chi_ngay', '?')
            
            if na_ngay_hanh != "?" and chi_ngay_check != "?":
                hanh_ts = nh_ts_tai.get(na_ngay_hanh, {})
                for stage_name, chi_val in hanh_ts.items():
                    if chi_val == chi_ngay_check:
                        clean_stage = stage_name.replace("_", " ")
                        gd_info = giai_doan_map.get(clean_stage, {})
                        context += f"Trường Sinh Ngày: {clean_stage} (Mức {gd_info.get('Mức', '?')}/10) - {gd_info.get('Luận', '?')}\n"
                        break
            
            # Thần Sát
            than_sat = tb_data.get("THAN_SAT_LOOKUP", {})
            relevant_sats = []
            for sat_name, sat_info in than_sat.items():
                cach_an = sat_info.get("Cách_An", "")
                if can_ngay_val in cach_an or chi_ngay_check in cach_an:
                    relevant_sats.append(f"{sat_name.replace('_', ' ')} ({sat_info.get('Loại', '?')}): {sat_info.get('Tác_Dụng', '')}")
            if relevant_sats:
                context += "Thần Sát liên quan:\n"
                for sat in relevant_sats[:3]:
                    context += f"  - {sat}\n"
            
            # Cung chi tiết cho User + Sự Việc
            cung_rules = tb_data.get("CUNG_LUAN_DOAN_CHI_TIET", {})
            def get_c_rule(idx):
                if not idx: return ""
                for k, v in cung_rules.items():
                    if f"Cung_{idx}_" in k: return f"{v.get('Quái','')} (Hành {v.get('Hành', '')}): {v.get('Luận_Đoán', '')}"
                return ""
                
            obj_stem = get_safe(qmdg, 'can_gio') if qmdg else "N/A"
            obj_idx = None
            if qmdg and 'can_thien_ban' in qmdg:
                for idx, stem in qmdg['can_thien_ban'].items():
                    if stem == obj_stem: obj_idx = idx
            
            if user_palace_idx: context += f"Gợi ý Cung Chủ: {get_c_rule(user_palace_idx)}\n"
            if obj_idx: context += f"Gợi ý Cung Sự Việc: {get_c_rule(obj_idx)}\n"
            
            # Ngũ Bất Ngộ Thời
            quy_tac = tb_data.get("QUY_TAC_LUAN_DOAN_NANG_CAO", {})
            ngu_bat = quy_tac.get("Ngũ_Bất_Ngộ_Thời", {})
            if ngu_bat:
                context += f"→ Ngũ Bất Ngộ Thời: {'; '.join(ngu_bat.get('Quy_Tắc', []))}\n"
            context += f"→ Chú ý Phục Ngâm/Phản Ngâm, Tam Kỳ Đắc Sử.\n"
        except Exception as e:
            context += f"\n(Lỗi load Thiết Bản Thần Toán: {e})\n"

        return context

    def render_logs(self):
        import streamlit as st
        st.markdown("### ⚙️ Quy Trình Xử Lý (Phoenix System Workflow)")
        for log in self.logs:
            icon = "✅" if log['status'] in ["SUCCESS", "COMPLETED"] else "🔄"
            if log['status'] == "ERROR": icon = "❌"
            
            with st.expander(f"{icon} {log['step']} - {log['status']}", expanded=False):
                st.write(f"**Time:** {log['time']}")
                st.write(f"**Detail:** {log['detail']}")

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
            st.session_state.ai_type = "Gemini Pro (V4.0 - Tứ Thuật Hợp Nhất)"
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
                        # from gemini_helper import GeminiQMDGHelper <--- REMOVED TO USE INLINED CLASS
                        temp_helper = GeminiQMDGHelper(user_api_input)
                        
                        # 2. Check if any valid keys found
                        # 2. Check if any valid keys found
                        if not temp_helper.api_keys:
                            st.error("❌ Không tìm thấy API Key nào hợp lệ (AIza...) trong văn bản bạn nhập.")
                        else:
                            # 3. FORCE SAVE FIRST (Trust the User)
                            # Update Session State immediately so next run uses this key
                            st.session_state.gemini_helper = temp_helper
                            st.session_state.gemini_key = temp_helper.api_key
                            st.session_state.ai_type = f"Gemini (Updated)"
                            
                            # Update Persistent Storage immediately
                            try:
                                data = load_custom_data()
                                data["GEMINI_API_KEY"] = ",".join(temp_helper.api_keys)
                                save_custom_data(data)
                                cookie_manager.set("GEMINI_API_KEY", ",".join(temp_helper.api_keys), expires_at=dt_module.datetime.now() + dt_module.timedelta(days=365))
                            except: pass

                            # 4. Test Connection (Just for info)
                            success, msg = temp_helper.test_connection()
                            
                            if success:
                                st.session_state.api_status_ok = True
                                st.session_state.api_status_msg = "Kết nối thành công"
                                st.success(f"✅ ĐÃ LƯU & KẾT NỐI: {len(temp_helper.api_keys)} Key")
                            else:
                                st.session_state.api_status_ok = False
                                st.session_state.api_status_msg = f"Lưu thành công, nhưng test lỗi: {msg}"
                                st.warning(f"⚠️ Đã lưu Key mới, nhưng kết nối chập chờn: {msg}. (Đừng lo, Web sẽ tự thử lại)")
                            
                            time.sleep(1)
                            st.rerun()
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

Hãy luận giải tình hình dựa trên Cung Bản Mệnh (Can Ngày) và Cung Sự Việc (Can Giờ/Dụng Thần).
"""
                                analysis = st.session_state.gemini_helper.answer_question(
                                    prompt,
                                    chart_data=st.session_state.chart_data,
                                    topic=selected_topic,
                                    selected_subject=st.session_state.get('selected_doi_tuong', 'Bản thân')
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
                        try:
                            # from qmdg_orchestrator import AIOrchestrator
                            # Use PHOENIX ORCHESTRATOR (Inlined)
                            orc = PhoenixOrchestrator(st.session_state.gemini_helper)
                            raw = orc.run_pipeline(
                                user_question, 
                                current_topic=selected_topic,
                                chart_data=st.session_state.get('chart_data'),
                                mai_hoa_data=st.session_state.get('mai_hoa_result'),
                                luc_hao_data=st.session_state.get('luc_hao_result')
                            )
                            # Check if raw is empty
                            if not raw:
                                st.error(f"❌ Lỗi: AI trả về rỗng (Empty Response) - [DEBUG_V3.0].\\nType: {type(raw)}\\nContent: {repr(raw)}")
                            else:
                                final_ans = st.session_state.gemini_helper._process_response(raw)
                                st.info(final_ans)
                            
                            orc.render_logs()
                        except Exception as e:
                            st.error(f"❌ Lỗi xử lý AI: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
                            # Try to render logs even if crashed
                            if 'orc' in locals(): orc.render_logs()



elif st.session_state.current_view == "mai_hoa":
    st.markdown("## 🌸 MAI HOA DỊCH SỐ - TAM TÀI HỢP NHẤT")
    
    if not USE_MAI_HOA:
        st.error("❌ Module Mai Hoa Dịch Số không khả dụng.")
        st.stop()
    
    st.markdown("### 🎯 Chủ đề: **{selected_topic}**")

    # AUTO CAST TIME
    dt = dt_module.datetime.now(vn_tz)
    st.info(f"🕒 Giờ hiện tại: {dt.strftime('%H:%M - %d/%m/%Y')}. Quẻ tự động cập nhật theo thời gian thực.")
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
    
    st.markdown("### 🎯 Chủ đề: **{selected_topic}**")

    show_debug_ih = st.checkbox("🐛 Chế độ Kiểm tra Dữ liệu", key="debug_iching_mode")

    # AUTO CAST TIME
    dt = dt_module.datetime.now(vn_tz)
    st.info(f"🕒 Giờ hiện tại: {dt.strftime('%H:%M - %d/%m/%Y')}. Quẻ tự động cập nhật theo thời gian thực.")
    can_ngay = params.get('can_ngay', 'Giáp') if params else "Giáp"
    chi_ngay = params.get('chi_ngay', 'Tý') if params else "Tý"
    try:
        st.session_state.luc_hao_result = lap_qua_luc_hao(
            dt.year, dt.month, dt.day, dt.hour,
            topic=selected_topic,
            can_ngay=can_ngay,
            chi_ngay=chi_ngay
        )
    except Exception as e:
        st.error(f"Lỗi lập quẻ Lục Hào: {e}")

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
# THIẾT BẢN THẦN TOÁN VIEW
# ======================================================================
elif st.session_state.current_view == "thiet_ban":
    st.markdown("## 📜 THIẾT BẢN THẦN TOÁN - NẠP ÂM ĐOÁN MỆNH")
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")
    
    if st.button("📜 TRA CỨU MỆNH CỤC CHI TIẾT", type="primary", use_container_width=True):
        import qmdg_data
        from qmdg_calc import calculate_qmdg_params
        tb_data = getattr(qmdg_data, 'KY_MON_DATA', {}).get("THIET_BAN_THAN_TOAN", {})
        hoa_giap = tb_data.get("LUC_THAP_HOA_GIAP_NAP_AM", {})
        
        # Calculate params based on now
        params = calculate_qmdg_params(now)
        nam_tru = f"{params.get('can_nam')} {params.get('chi_nam')}"
        ngay_tru = f"{params.get('can_ngay')} {params.get('chi_ngay')}"
        
        na_nam = hoa_giap.get(nam_tru, {}).get("Nạp_Âm", "Không rõ")
        na_ngay = hoa_giap.get(ngay_tru, {}).get("Nạp_Âm", "Không rõ")
        
        st.success("✅ Cập nhật Tứ Trụ Sinh Thần thành công!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**🍁 Mệnh Năm (Thái Tuế):**\n- {nam_tru}\n- Nạp Âm: {na_nam}")
        with col2:
            st.warning(f"**☀️ Mệnh Ngày (Chủ Sự):**\n- {ngay_tru}\n- Nạp Âm: {na_ngay}")
            
        st.markdown(f'''
        <div style="background:#1e293b; padding:15px; border-radius:10px; color:white; border-left:4px solid #f59e0b; margin-top:20px;">
            <h4>🔍 TÍCH HỢP ĐẠI TIÊN TRI</h4>
            - Thiết Bản Thần Toán là môn thuật số đề cao Nạp Âm của Năm và Ngày để định đoạt cát hung đại cục.<br>
            - AI Tiên Tri đã được trang bị toàn bộ hơn 100 quy tắc Phản Ngâm, Phục Ngâm, Trường Sinh 12 Giai Đoạn, và Thần Sát của Thiết Bản.<br>
            👉 Hãy chuyển sang Tab <b>"🤖 Hỏi Gemini AI"</b> và chọn <b>"🌟 TỨ THUẬT HỢP NHẤT"</b> để dung hợp Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản vào một câu trả lời duy nhất!
        </div>
        ''', unsafe_allow_html=True)


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
                    # INITIALIZE ORCHESTRATOR -> REDIRECT TO KNOWLEDGE BRAIN
                    # orc = PhoenixOrchestrator(st.session_state.gemini_helper)
                    orc = st.session_state.gemini_helper # Use the main brain
                    
                    # RUN PIPELINE with Role Injected
                    safe_topic = selected_agent.split('(')[0].strip()
                    full_query = f"Bạn đang đóng vai chuyên gia: {selected_agent}. Hãy trả lời câu hỏi: {exp_q}"
                    
                    raw_response = orc.answer_question(
                        full_query, 
                        topic=safe_topic,
                        chart_data=st.session_state.get('chart_data')
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
    
    col_ask1, col_ask2 = st.columns(2)
    with col_ask1:
        btn_ask_normal = st.button(f"🤖 Hỏi {ai_name} (Thường)", use_container_width=True, key="ask_gemini_btn")
    with col_ask2:
        btn_ask_supreme = st.button("🌟 TỨ THUẬT HỢP NHẤT", type="primary", help="Tự động gieo quẻ Kỳ Môn, Kinh Dịch, Mai Hoa và Thiết Bản để tổng hợp 1 kết quả chính xác nhất.", use_container_width=True, key="ask_supreme_btn")
        
    if btn_ask_normal or btn_ask_supreme:
        if user_question:
            with st.spinner(f"🌟 Khởi động Đại Tiên Tri Tứ Thuật..." if btn_ask_supreme else f"🤖 {ai_name} đang chạy quy trình..."):
                try:
                    safe_topic = selected_topic_ai if selected_topic_ai != 'Không chọn (Hỏi chung)' else 'Chung'
                    
                    # --- ENSURE QMDG CHART IS FULLY POPULATED BEFORE AI RUNS ---
                    try:
                        from qmdg_data import an_bai_luc_nghi, lap_ban_qmdg
                        dia_can = an_bai_luc_nghi(params['cuc'], params['is_duong_don'])
                        thien_ban, can_thien_ban, nhan_ban, than_ban, truc_phu_cung = lap_ban_qmdg(
                            params['cuc'], params['truc_phu'], params['truc_su'], 
                            params['can_gio'], params['chi_gio'], params['is_duong_don']
                        )
                        st.session_state.chart_data = {
                            'thien_ban': thien_ban,
                            'can_thien_ban': can_thien_ban,
                            'nhan_ban': nhan_ban,
                            'than_ban': than_ban,
                            'dia_can': dia_can,
                            'cuc': params['cuc'],
                            'tiet_khi': params.get('tiet_khi', ''),
                            'can_ngay': params['can_ngay'],
                            'chi_ngay': params['chi_ngay'],
                            'can_nam': params.get('can_nam', 'N/A'),
                            'chi_nam': params.get('chi_nam', 'N/A'),
                            'can_thang': params.get('can_thang', 'N/A'),
                            'chi_thang': params.get('chi_thang', 'N/A'),
                            'can_gio': params['can_gio'],
                            'chi_gio': params['chi_gio']
                        }
                    except Exception as e:
                        pass
                    
                    if btn_ask_supreme:
                        # 1. AUTO GENERATE ALL CHARTS BASED ON USER'S SELECTED TIME
                        import datetime
                        import random
                        import hashlib
                        
                        # Use the globally selected datetime
                        current_dt = selected_datetime
                        
                        try:
                            from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, giai_qua
                            st.session_state.mai_hoa_result = tinh_qua_theo_thoi_gian(current_dt.year, current_dt.month, current_dt.day, current_dt.hour)
                            st.session_state.mai_hoa_result['interpretation'] = giai_qua(st.session_state.mai_hoa_result, safe_topic)
                        except Exception as e:
                            pass
                            
                        try:
                            seed = int(hashlib.md5(f"{user_question}_{current_dt}".encode()).hexdigest(), 16) % 100000
                            random.seed(seed)
                            hao_list = [random.choice([6, 7, 8, 9]) for _ in range(6)]
                            from luc_hao_kinh_dich import lap_que
                            st.session_state.luc_hao_result = lap_que(hao_list, current_dt, safe_topic)
                        except Exception as e:
                            pass
                            
                        # THIẾT BẢN THẦN TOÁN (Context Injection)
                        tb_context = ""
                        try:
                            from qmdg_data import THIET_BAN_THAN_TOAN
                            from qmdg_calc import get_can_chi_year
                            tb_year_can, tb_year_chi = get_can_chi_year(lyear)
                            tb_year = f"{tb_year_can} {tb_year_chi}"
                            tb_day = f"{params['can_ngay']} {params['chi_ngay']}"
                            nap_am_nam = THIET_BAN_THAN_TOAN["nap_am_60_hoa_giap"].get(tb_year, {}).get("nap_am", "?")
                            nap_am_ngay = THIET_BAN_THAN_TOAN["nap_am_60_hoa_giap"].get(tb_day, {}).get("nap_am", "?")
                            tb_context = f"\n[DỮ LIỆU THIẾT BẢN THẦN TOÁN]:\n- Nạp Âm Trụ Năm Mở Quẻ: {nap_am_nam} ({tb_year})\n- Nạp Âm Trụ Ngày Mở Quẻ: {nap_am_ngay} ({tb_day})\nLƯU Ý THẦN TOÁN: ĐÂY LÀ KHÍ CHẤT CỦA THỜI GIAN HIỆN TẠI, TUYỆT ĐỐI KHÔNG LẤY NÓ LÀM MỆNH (NĂM SINH) CỦA NGƯỜI DÙNG.\n"
                        except Exception:
                            pass
                        
                        # 2. CALL PHOENIX MASTER
                        orc = PhoenixOrchestrator(st.session_state.gemini_helper)
                        
                        raw_response = orc.run_pipeline(
                            user_question, 
                            current_topic=safe_topic,
                            chart_data=st.session_state.get('chart_data'),
                            mai_hoa_data=st.session_state.get('mai_hoa_result'),
                            luc_hao_data=st.session_state.get('luc_hao_result'),
                            tb_context=tb_context
                        )
                    else:
                        # Call the upgraded answer_question method with ALL charts
                        raw_response = st.session_state.gemini_helper.answer_question(
                            user_question, 
                            topic=safe_topic,
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
                    if hasattr(st.session_state.gemini_helper, 'render_logs'):
                        st.session_state.gemini_helper.render_logs()
                    
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


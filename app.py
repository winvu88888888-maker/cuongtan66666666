import streamlit as st

# VERSION: 2026-04-15-V32.2-UNIFIED-INDEX-OFFLINE
try:
    st.set_page_config(
        page_title="🔮 Kỳ Môn AI V32.2",
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
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h3 style='color: #4CAF50; margin-bottom: 5px;'>Trí Tuệ Nhân Tạo</h3>
    <div style='background-color: #2E3B4E; padding: 5px 10px; border-radius: 15px; display: inline-block;'>
        <code style='color: #4CAF50; background: none;'>🚀 MODEL: GEMINI-2.5-PRO</code>
    </div>
    <div style='margin-top: 10px; font-size: 0.8em; color: #a0aec0;'>
        Trạng thái: <b>THIÊN CƠ ĐẠI SƯ V32.2</b> —<br>Unified Index + Offline Engine (6 Môn + Vạn Vật 2226+)
    </div>
</div>
""", unsafe_allow_html=True)

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
st.success("✅ SYSTEM ONLINE: V32.2 — THIÊN CƠ ĐẠI SƯ (Unified Index + Offline Engine + Vạn Vật 2226+ items)")

# ======================================================================
# SIDEBAR - CONTROLS
# ======================================================================
with st.sidebar:
    st.markdown("### ⚙️ Điều Khiển")
    
    # View selection
    view_option = st.radio(
        "Chọn Phương Pháp:",
        ["🔮 Kỳ Môn Độn Giáp", "🏭 Nhà Máy AI", "🌟 40 Chuyên Gia AI", "📖 Mai Hoa 64 Quẻ", "☯️ Lục Hào Kinh Dịch", "📜 Thiết Bản Thần Toán", "📊 Vạn Vật Loại Tượng", "🌊 Đại Lục Nhâm", "⭐ Thái Ất Thần Số", "🤖 Hỏi Gemini AI"],
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
    elif view_option == "📊 Vạn Vật Loại Tượng":
        st.session_state.current_view = "van_vat"
    elif view_option == "🌊 Đại Lục Nhâm":
        st.session_state.current_view = "dai_luc_nham"
    elif view_option == "⭐ Thái Ất Thần Số":
        st.session_state.current_view = "thai_at"
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
    
    # Tổng hợp: Ưu tiên Manual > Streamlit Secrets > Saved Key > Factory Key
    secret_api_key = manual_key or st_secret or saved_key or factory_key
    
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
    """V20.5: Trình bày kết quả AI giống hệt nút 'Bắt đầu Phân Tích Tổng Hợp' - dễ đọc, rõ ràng."""
    if not text:
        st.warning("❌ Không có kết quả")
        return
    
    import re
    text = str(text).strip()
    
    # ═══ PHÁT HIỆN KẾT LUẬN CHÍNH (CÁT/HUNG/BÌNH) ═══
    conclusion = ""
    verdict_badge = ""
    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        if re.search(r'(?:KẾT LUẬN|PHÁN QUYẾT|TỔNG KẾT|VERDICT)', stripped, re.IGNORECASE):
            conclusion = stripped
        elif re.search(r'^\*\*.*(?:CÁT|ĐẠI CÁT|HUNG|ĐẠI HUNG|THUẬN LỢI|KHÓ KHĂN).*\*\*', stripped, re.IGNORECASE):
            conclusion = stripped
        if conclusion:
            if re.search(r'CÁT|ĐẠI CÁT|THUẬN LỢI|TỐT|THÀNH CÔNG', conclusion, re.IGNORECASE):
                verdict_badge = "cat"
            elif re.search(r'HUNG|ĐẠI HUNG|KHÓ|XẤU|THẤT BẠI', conclusion, re.IGNORECASE):
                verdict_badge = "hung"
            else:
                verdict_badge = "binh"
            break
    
    # ═══ 1. VERDICT BOX (nổi bật) ═══
    if conclusion:
        if verdict_badge == "cat":
            gradient = "linear-gradient(135deg, #065f46, #047857)"
            border_color = "#10b981"
            v_icon = "✅"; label = "THUẬN LỢI"
        elif verdict_badge == "hung":
            gradient = "linear-gradient(135deg, #7f1d1d, #b91c1c)"
            border_color = "#ef4444"
            v_icon = "⚠️"; label = "KHÓ KHĂN"
        else:
            gradient = "linear-gradient(135deg, #78350f, #b45309)"
            border_color = "#f59e0b"
            v_icon = "⚖️"; label = "CÂN NHẮC"
        
        clean_conclusion = conclusion.replace('**', '').replace('##', '').replace('#', '').strip()
        st.markdown(f"""
        <div style="background:{gradient}; border-radius:16px; padding:24px 28px; margin:16px 0; box-shadow:0 8px 32px rgba(0,0,0,0.15); border-left:6px solid {border_color};">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                <span style="font-size:28px;">{v_icon}</span>
                <span style="background:{border_color}; color:white; padding:4px 16px; border-radius:20px; font-weight:800; font-size:13px; letter-spacing:1px;">{label}</span>
            </div>
            <div style="color:white; font-size:1.3rem; font-weight:700; line-height:1.6; text-shadow:0 1px 3px rgba(0,0,0,0.3);">{clean_conclusion}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ═══ 2. NỘI DUNG CHÍNH — RENDER GIỐNG HỆT "Bắt đầu Phân Tích Tổng Hợp" (dòng 2370) ═══
    # Y HỆT: st.markdown(f'<div class="interpret-box">{text}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="interpret-box" style="background: white; border-top: 5px solid #1e3a8a;">
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

    def run_pipeline(self, user_question, current_topic="Chung", chart_data=None, mai_hoa_data=None, luc_hao_data=None, tb_context=""):
        enhanced_question = user_question + tb_context if tb_context else user_question
        return self.gemini.answer_question(enhanced_question, chart_data=chart_data, topic=current_topic, mai_hoa_data=mai_hoa_data, luc_hao_data=luc_hao_data)

# Auto-Init logic — GUARD: Only init if not already in session_state
if 'gemini_helper' not in st.session_state:
    if st.session_state.ai_preference == "offline":
        if FREE_AI_AVAILABLE:
            st.session_state.gemini_helper = FreeAIHelper()
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
                    st.session_state.gemini_helper = FreeAIHelper()
                    st.session_state.ai_type = "Free AI (Fallback từ Lỗi)"
        elif FREE_AI_AVAILABLE:
            st.session_state.gemini_helper = FreeAIHelper()
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
            st.session_state.gemini_helper = FreeAIHelper()

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
    
    user_api_input = st.text_area("📋 Dán API Key vào đây:", height=80, key="input_api_key_smart_unified", placeholder="AIzaSy... (hỗ trợ dán nhiều key cùng lúc)")
    
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
                        st.error("❌ Không tìm thấy API Key hợp lệ (AIza...) trong văn bản.")
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
                'chi_thang': params.get('chi_thang', 'N/A'),
                'can_nam': params.get('can_nam', 'N/A'),
                'chi_nam': params.get('chi_nam', 'N/A')
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
                            st.session_state.final_ai_report = final_report
                        except Exception as e:
                            st.error(f"Lỗi phân tích: {e}")
                
                if st.session_state.get('final_ai_report'):
                    st.markdown(f"""
                    <div class="interpret-box" style="background: white; border-top: 5px solid #1e3a8a;">
                        {st.session_state.final_ai_report}
                    </div>
                    """, unsafe_allow_html=True)

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
        
        # ===== UNIFIED EXPERT ANALYSIS SYSTEM =====
        if st.session_state.chart_data:
            st.markdown("---")
            st.markdown("## 🏆 HỆ THỐNG LUẬN GIẢI TỔNG HỢP CHUYÊN SÂU")
            
            # 1. PRIMARY AI EXPERT REPORT (Dụng Thần focus) — DUAL MODE
            with st.container():
                st.markdown("### 🎯 KẾT LUẬN TỔNG HỢP TỪ AI (Dụng Thần)")
                
                # V8.2: MỘT NÚT DUY NHẤT — Kết hợp AI Offline + Online
                unified_clicked = st.button("🔮 PHÂN TÍCH TỔNG HỢP AI", type="primary", key="ai_unified_btn", use_container_width=True)
                
                if unified_clicked:
                    try:
                        selected_topic = st.session_state.get('selected_topic', 'Chung')
                        topic_data = st.session_state.get('topic_data', {})
                        params = st.session_state.get('params', {})
                        dung_than_list = topic_data.get('Dụng_Thần', []) if topic_data else []
                        topic_hints = topic_data.get('Gợi_Ý', '') if topic_data else ''
                        
                        # Xác định đối tượng
                        rel_type = st.session_state.get('selected_doi_tuong', 'Bản thân')
                        # V10.2: role_label phải phản ánh đúng đối tượng, KHÔNG hardcode
                        role_label = rel_type if rel_type and rel_type != 'Bản thân' else 'Bản thân'
                        
                        # V28.0: Fix Lỗi 1 — GỬI CÂU HỎI THỰC thay vì prompt template
                        # Prompt template cũ chứa "Bạn là đại sư..." khiến Smart Category phân loại SAI
                        actual_question = f"Phân tích về {selected_topic}"
                        if role_label and role_label != 'Bản thân':
                            actual_question += f" cho {role_label}"
                        
                        # ====== BƯỚC 1: AI OFFLINE phân tích quẻ trước ======
                        with st.spinner("⚙️ Bước 1/2: AI Offline đang phân tích quẻ..."):
                            from free_ai_helper import FreeAIHelper
                            _offline_api_key = st.session_state.get('api_key', '')
                            offline_ai = FreeAIHelper(api_key=_offline_api_key)
                            
                            # Auto-compute Mai Hoa & Lục Hào
                            mai_hoa_for_offline = st.session_state.get('mai_hoa_result')
                            luc_hao_for_offline = st.session_state.get('luc_hao_result')
                            
                            if not mai_hoa_for_offline:
                                try:
                                    dt_now = dt_module.datetime.now(vn_tz)
                                    mai_hoa_for_offline = tinh_qua_theo_thoi_gian(dt_now.year, dt_now.month, dt_now.day, dt_now.hour)
                                    mai_hoa_for_offline['interpretation'] = giai_qua(mai_hoa_for_offline, selected_topic)
                                    st.session_state.mai_hoa_result = mai_hoa_for_offline
                                except Exception:
                                    pass
                            
                            if not luc_hao_for_offline:
                                try:
                                    dt_now = dt_module.datetime.now(vn_tz)
                                    # V28.0: Fix Lỗi 6 — Lấy Can/Chi từ chart_data thay vì params rỗng
                                    _chart = st.session_state.get('chart_data', {})
                                    can_ngay_val = _chart.get('can_ngay', 'Giáp') if _chart else 'Giáp'
                                    chi_ngay_val = _chart.get('chi_ngay', 'Tý') if _chart else 'Tý'
                                    luc_hao_for_offline = lap_qua_luc_hao(
                                        dt_now.year, dt_now.month, dt_now.day, dt_now.hour,
                                        topic=selected_topic,
                                        can_ngay=can_ngay_val,
                                        chi_ngay=chi_ngay_val
                                    )
                                    st.session_state.luc_hao_result = luc_hao_for_offline
                                except Exception:
                                    pass
                            
                            offline_result = offline_ai.answer_question(
                                actual_question,
                                chart_data=st.session_state.chart_data,
                                topic=selected_topic,  # V28.0: PHẢI truyền topic để match đúng DT
                                selected_subject=rel_type,
                                mai_hoa_data=mai_hoa_for_offline,
                                luc_hao_data=luc_hao_for_offline
                            )
                        
                        # ====== V13.0: AI ONLINE đã tích hợp trong answer_question ======
                        # Loại bỏ refine_prompt riêng — tiết kiệm 50% API quota
                        # V12.0 gọi _call_ai_raw thêm 1 lần ở đây → TỐN GẤP ĐÔI
                        # V13.0: offline_result đã bao gồm online result bên trong rồi
                        st.session_state.primary_ai_analysis = offline_result
                    except Exception as e:
                        st.error(f"❌ Lỗi AI: {str(e)}")
            
            # Moved outside of 'gemini_helper' check to persist during API key reload
            if st.session_state.get('primary_ai_analysis'):
                # 2. GENERATE QUICK ACTIONS
                quick_actions = ["Hãy hành động dựa trên kết luận trên", "Chọn thời điểm phù hợp với ngũ hành"]
                actions_html = "".join([f'<div class="action-item">{act}</div>' for act in quick_actions])
                
                # Display Quick Actions First
                st.markdown(f"""
                <div class="action-card">
                    <div class="action-title">&#128640; HÀNH ĐỘNG NHANH CẦN LÀM NGAY</div>
                    {actions_html}
                </div>
                """, unsafe_allow_html=True)
                
                # V19.0: Display Detailed Analysis với bố cục đẹp
                display_ai_result(st.session_state.primary_ai_analysis, key_prefix="primary")

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
                    
                    # V13.0: Removed duplicate AI So Sánh button
                    st.caption("💡 Dùng '🌟 LỤC THUẬT HỢP NHẤT' trong tab Hỏi Gemini AI")
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

            # 4. AI Q&A SECTION — V8.2 UNIFIED (Offline + Online kết hợp)
            st.markdown("---")
            st.markdown("### ❓ HỎI AI — KHÔNG GIỚI HẠN CHỦ ĐỀ")
            user_question = st.text_area("💬 Đặt câu hỏi bất kỳ (tự do, không giới hạn chủ đề):", placeholder="Ví dụ: Năm nay có mua được nhà không? / Con mèo lạc tìm ở đâu? / Bao giờ tìm được việc?...", key="ai_q_input", height=80)
            if st.button("🔮 PHÂN TÍCH TỔNG HỢP AI", key="ai_ask_unified", type="primary", use_container_width=True):
                if user_question:
                    try:
                        # ====== BƯỚC 1: AI OFFLINE phân tích quẻ ======
                        with st.spinner("⚙️ Bước 1/2: AI Offline đang phân tích quẻ từ câu hỏi của bạn..."):
                            from free_ai_helper import FreeAIHelper
                            # V8.2: Lấy API key từ session_state HOẶC secrets
                            _api_key = st.session_state.get('api_key', '')
                            if not _api_key:
                                try:
                                    _api_key = st.secrets.get('GEMINI_API_KEY', '')
                                except Exception:
                                    _api_key = ''
                            offline_ai = FreeAIHelper(api_key=_api_key)
                            
                            # Auto-compute Mai Hoa & Lục Hào
                            mai_hoa_for_q = st.session_state.get('mai_hoa_result')
                            luc_hao_for_q = st.session_state.get('luc_hao_result')
                            
                            if not mai_hoa_for_q:
                                try:
                                    dt_now = dt_module.datetime.now(vn_tz)
                                    mai_hoa_for_q = tinh_qua_theo_thoi_gian(dt_now.year, dt_now.month, dt_now.day, dt_now.hour)
                                    mai_hoa_for_q['interpretation'] = giai_qua(mai_hoa_for_q, selected_topic)
                                    st.session_state.mai_hoa_result = mai_hoa_for_q
                                except Exception:
                                    pass
                            
                            if not luc_hao_for_q:
                                try:
                                    dt_now = dt_module.datetime.now(vn_tz)
                                    # V28.0: Fix Lỗi 6 — Lấy Can/Chi từ chart_data thay vì params rỗng
                                    _chart_q = st.session_state.get('chart_data', {})
                                    can_ngay_val = _chart_q.get('can_ngay', 'Giáp') if _chart_q else 'Giáp'
                                    chi_ngay_val = _chart_q.get('chi_ngay', 'Tý') if _chart_q else 'Tý'
                                    luc_hao_for_q = lap_qua_luc_hao(
                                        dt_now.year, dt_now.month, dt_now.day, dt_now.hour,
                                        topic=selected_topic, can_ngay=can_ngay_val, chi_ngay=chi_ngay_val
                                    )
                                    st.session_state.luc_hao_result = luc_hao_for_q
                                except Exception:
                                    pass
                            
                            # V8.2: topic=None → AI tự phân tích câu hỏi thay vì dùng dropdown
                            offline_result = offline_ai.answer_question(
                                user_question,
                                chart_data=st.session_state.get('chart_data'),
                                topic=None,
                                selected_subject=st.session_state.get('selected_doi_tuong', 'Bản thân'),
                                mai_hoa_data=mai_hoa_for_q,
                                luc_hao_data=luc_hao_for_q
                            )
                        
                        # ====== V13.0: AI ONLINE đã tích hợp trong answer_question ======
                        # Loại bỏ refine_prompt riêng — tiết kiệm 50% API quota
                        # V13.0: offline_result đã bao gồm online result bên trong rồi
                        combined_answer = offline_result or ""
                        
                        # V19.0: Display với bố cục đẹp
                        display_ai_result(combined_answer, key_prefix="qa")

                        # Lưu vào history
                        st.session_state.chat_history.append({'role': 'user', 'content': user_question})
                        st.session_state.chat_history.append({'role': 'assistant', 'content': combined_answer})
                        if len(st.session_state.chat_history) > 20:
                            st.session_state.chat_history = st.session_state.chat_history[-20:]
                    
                    except Exception as e:
                        st.error(f"❌ Lỗi AI: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())



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

        # V13.0: Removed AI Luận Mai Hoa button (dùng LỤC THUẬT HỢP NHẤT thay thế)
        st.info("💡 Để AI luận quẻ chuyên sâu → sang tab **'🤖 Hỏi Gemini AI'** → **'🌟 LỤC THUẬT HỢP NHẤT'**")

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
        
        # ========== COMPACT HEADER (giống xinhdich.com) ==========
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border: 2px solid #b45309; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; font-size: 13px;">
            <div style="text-align:center; font-weight:900; font-size:15px; color:#92400e; margin-bottom:6px;">
                📜 PHẦN MỀM LẬP QUẺ DỊCH — Phương pháp: Mai Hoa
            </div>
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:4px;">
                <span>⏰ <b>Thời gian:</b> {dt.strftime('%H:%M %d/%m/%Y')}</span>
                <span>🌙 <b>Can Chi:</b> giờ {can_gio} {chi_gio}, ngày {can_ngay} {chi_ngay}, tháng {can_thang} {chi_thang}, năm {can_nam} {chi_nam}</span>
            </div>
            <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:4px; margin-top:4px;">
                <span>🌿 <b>Tiết khí:</b> {tiet_khi}</span>
                <span>☀️ <b>Nhật thần:</b> {nhat_than}</span>
                <span>🌙 <b>Nguyệt lệnh:</b> {nguyet_lenh}</span>
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
        <div style="background:#f1f5f9; border-radius:8px; padding:8px 12px; font-size:12px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:4px;">
            <span>💡 {res['the_ung']}</span>
            <span>📝 Dụng Thần: {res['ban']['details'][2]['luc_than']}</span>
            <span>🔄 Động hào: {', '.join([str(h) for h in moving_hao])}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== V12.2: PHỤC THẦN (伏神) — Lục Thân ẩn ==========
        phuc_than_data = res.get('phuc_than', [])
        if phuc_than_data:
            pt_html = """
            <div style="background:#faf5ff; border:2px solid #7c3aed; border-radius:8px; padding:8px 12px; margin:8px 0;">
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
    
    # AUTO CAST TIME
    dt = dt_module.datetime.now(vn_tz)
    st.info(f"🕒 Giờ hiện tại: {dt.strftime('%H:%M - %d/%m/%Y')}. Kết quả tự động cập nhật theo thời gian thực.")
    now = dt

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
        👉 Hãy chuyển sang Tab <b>"🤖 Hỏi Gemini AI"</b> và chọn <b>"🌟 LỤC THUẬT HỢP NHẤT"</b> để dung hợp Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản vào một câu trả lời duy nhất!
    </div>
    ''', unsafe_allow_html=True)
    
    # V13.0: Removed AI Luận Thiết Bản button (dùng LỤC THUẬT HỢP NHẤT thay thế)
    st.info("💡 Để AI luận quẻ chuyên sâu → sang tab **'🤖 Hỏi Gemini AI'** → **'🌟 LỤC THUẬT HỢP NHẤT'**")


# ======================================================================
# AI FACTORY VIEW
# ======================================================================
elif st.session_state.current_view == "ai_factory":
    st.markdown("## 🏭 NHÀ MÁY PHÁT TRIỂN AI - 10 AGENTS HUB")
    st.info("Hệ thống tự động hóa điều phối bởi AI Orchestrator + n8n.")
    
    # Status Row
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Agents Đang Chạy", "10/10", "Active")
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
                    # === SAVE TO CHAT HISTORY ===
                    st.session_state.chat_history.append({'role': 'user', 'content': exp_q})
                    st.session_state.chat_history.append({'role': 'assistant', 'content': res})
                    if len(st.session_state.chat_history) > 20:
                        st.session_state.chat_history = st.session_state.chat_history[-20:]
                    
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
    
    st.markdown("### 🎯 Chọn Chủ Đề (Tùy chọn)")
    st.caption("Chọn chủ đề để AI có ngữ cảnh tốt hơn, hoặc để trống để hỏi chung")
    
    selected_topic_ai = st.selectbox(
        "Chủ đề:",
        ["Không chọn (Hỏi chung)"] + st.session_state.all_topics_full,
        key="ai_topic_select"
    )
    
    st.markdown("---")
    
    # === CONVERSATION HISTORY UI ===
    if st.session_state.chat_history:
        st.markdown("### 📜 Lịch Sử Hội Thoại")
        st.caption(f"AI sẽ nhớ {len(st.session_state.chat_history) // 2} câu hỏi trước đó để trả lời chính xác hơn.")
        
        # Display chat history
        for i, msg in enumerate(st.session_state.chat_history):
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 10px 15px; border-radius: 10px; color: white; margin: 5px 0; margin-left: 20%;">
                    <b>👤 Bạn:</b> {msg['content'][:200]}{'...' if len(msg['content']) > 200 else ''}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f0f2f6; padding: 10px 15px; border-radius: 10px; color: #1e293b; margin: 5px 0; margin-right: 20%; border-left: 4px solid #667eea;">
                    <b>🤖 AI:</b> {msg['content'][:300]}{'...' if len(msg['content']) > 300 else ''}
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🗑️ Xóa Lịch Sử Hội Thoại", key="clear_chat_history"):
            st.session_state.chat_history = []
            st.rerun()
        
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
        btn_ask_normal = st.button("💬 HỎI NHANH (Kiến Thức Chung)", use_container_width=True, key="ask_gemini_btn", help="Hỏi Gemini trực tiếp về kiến thức huyền học — KHÔNG gieo quẻ, KHÔNG dùng dữ liệu offline.")
    with col_ask2:
        btn_ask_supreme = st.button("🌟 LỤC THUẬT HỢP NHẤT", type="primary", help="Tự động gieo quẻ Kỳ Môn, Kinh Dịch, Mai Hoa và Thiết Bản để tổng hợp 1 kết quả chính xác nhất.", use_container_width=True, key="ask_supreme_btn")
        
    if btn_ask_normal or btn_ask_supreme:
        if user_question:
            with st.spinner(f"🌟 Khởi động Đại Tiên Tri Lục Thuật..." if btn_ask_supreme else f"💬 Đang hỏi Gemini trực tiếp..."):
                try:
                    safe_topic = selected_topic_ai if selected_topic_ai != 'Không chọn (Hỏi chung)' else 'Chung'
                    
                    if btn_ask_normal:
                        # ===============================================================
                        # V29.4: NÚT "HỎI NHANH" — Gọi Gemini TRỰC TIẾP (không gieo quẻ)
                        # Dùng cho kiến thức huyền học chung, KHÔNG chạy offline engine
                        # ===============================================================
                        quick_prompt = (
                            f"Bạn là THIÊN CƠ ĐẠI SƯ — chuyên gia huyền học Phương Đông.\n"
                            f"Trả lời câu hỏi dưới đây bằng kiến thức huyền học (Kỳ Môn, Lục Hào, Mai Hoa, Kinh Dịch, Phong Thủy, v.v.).\n"
                            f"Giọng văn: Tự tin, chuyên nghiệp, dễ hiểu.\n"
                            f"Nếu câu hỏi YÊU CẦU BÓI/GIEO QUẺ cụ thể, hãy khuyên user bấm nút '🌟 LỤC THUẬT HỢP NHẤT' để có kết quả chính xác.\n\n"
                            f"Chủ đề: {safe_topic}\n"
                            f"CÂU HỎI: {user_question}"
                        )
                        
                        # Thử gọi Gemini trực tiếp (không qua offline engine)
                        raw_response = None
                        try:
                            if hasattr(st.session_state.gemini_helper, '_call_ai_raw'):
                                raw_response = st.session_state.gemini_helper._call_ai_raw(quick_prompt)
                            elif hasattr(st.session_state.gemini_helper, '_call_ai'):
                                raw_response = st.session_state.gemini_helper._call_ai(quick_prompt)
                        except Exception:
                            pass
                        
                        # Fallback: nếu không có Gemini API → dùng offline engine
                        if not raw_response or len(str(raw_response)) < 50:
                            raw_response = (
                                "⚠️ **AI Online không khả dụng.** Không thể trả lời nhanh.\n\n"
                                "💡 **Gợi ý:** Bấm nút **'🌟 LỤC THUẬT HỢP NHẤT'** để AI Offline phân tích "
                                "dựa trên quẻ Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản."
                            )
                    
                    else:
                        # ===============================================================
                        # NÚT "LỤC THUẬT HỢP NHẤT" — Full Pipeline (Offline 5PP → Online)
                        # ===============================================================
                    
                        # --- AUTO GENERATE ALL 4 CHARTS (KỲ MÔN, MAI HOA, LỤC HÀO, THIẾT BẢN) FOR AI ---
                        import datetime
                        import random
                        import hashlib
                        import datetime as dt_module
                        vn_tz = dt_module.timezone(dt_module.timedelta(hours=7))
                        current_dt = dt_module.datetime.now(vn_tz) # Use the real-time auto-refresh datetime
                        
                        # 1. KỲ MÔN ĐỘN GIÁP
                        temp_chart_data = st.session_state.get('chart_data')
                        if not temp_chart_data:
                            try:
                                from qmdg_calc import calculate_qmdg_params
                                from qmdg_data import an_bai_luc_nghi, lap_ban_qmdg
                                q_params = calculate_qmdg_params(current_dt)
                                dia_can = an_bai_luc_nghi(q_params['cuc'], q_params['is_duong_don'])
                                thien_ban, can_thien_ban, nhan_ban, than_ban, truc_phu_cung = lap_ban_qmdg(
                                    q_params['cuc'], q_params['truc_phu'], q_params['truc_su'], 
                                    q_params['can_gio'], q_params['chi_gio'], q_params['is_duong_don']
                                )
                                temp_chart_data = {
                                    'thien_ban': thien_ban,
                                    'can_thien_ban': can_thien_ban,
                                    'nhan_ban': nhan_ban,
                                    'than_ban': than_ban,
                                    'dia_can': dia_can,
                                    'cuc': q_params['cuc'],
                                    'tiet_khi': q_params.get('tiet_khi', ''),
                                    'can_ngay': q_params['can_ngay'],
                                    'chi_ngay': q_params['chi_ngay'],
                                    'can_nam': q_params.get('can_nam', 'N/A'),
                                    'chi_nam': q_params.get('chi_nam', 'N/A'),
                                    'can_thang': q_params.get('can_thang', 'N/A'),
                                    'chi_thang': q_params.get('chi_thang', 'N/A'),
                                    'can_gio': q_params['can_gio'],
                                    'chi_gio': q_params['chi_gio']
                                }
                            except Exception as e:
                                pass
                                
                        # 2. MAI HOA DỊCH SỐ
                        temp_mai_hoa = st.session_state.get('mai_hoa_result')
                        if not temp_mai_hoa:
                            try:
                                from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, giai_qua
                                temp_mai_hoa = tinh_qua_theo_thoi_gian(current_dt.year, current_dt.month, current_dt.day, current_dt.hour)
                                temp_mai_hoa['interpretation'] = giai_qua(temp_mai_hoa, safe_topic)
                            except Exception as e:
                                pass
                                
                        # 3. LỤC HÀO KINH DỊCH
                        temp_luc_hao = st.session_state.get('luc_hao_result')
                        if not temp_luc_hao:
                            try:
                                seed = int(hashlib.md5(f"{user_question}_{current_dt}".encode()).hexdigest(), 16) % 100000
                                random.seed(seed)
                                hao_list = [random.choice([6, 7, 8, 9]) for _ in range(6)]
                                from luc_hao_kinh_dich import lap_que
                                temp_luc_hao = lap_que(hao_list, current_dt, safe_topic)
                            except Exception as e:
                                pass
                                
                        # 4. THIẾT BẢN THẦN TOÁN (Context Injection)
                        tb_context = ""
                        try:
                            from qmdg_data import KY_MON_DATA
                            from qmdg_calc import get_can_chi_year
                            hoa_giap = KY_MON_DATA.get("THIET_BAN_THAN_TOAN", {}).get("LUC_THAP_HOA_GIAP_NAP_AM", {})
                            tb_year_can, tb_year_chi = get_can_chi_year(current_dt.year)
                            tb_year_key = f"{tb_year_can} {tb_year_chi}"
                            # Try to use existing chart_data if any, otherwise default
                            tb_day_key = f"{temp_chart_data['can_ngay']} {temp_chart_data['chi_ngay']}" if temp_chart_data else "? ?"
                            nap_am_nam = hoa_giap.get(tb_year_key, {}).get("Nạp_Âm", "Không rõ")
                            nap_am_ngay = hoa_giap.get(tb_day_key, {}).get("Nạp_Âm", "Không rõ")
                            tb_context = f"\\n[DỮ LIỆU THIẾT BẢN THẦN TOÁN]:\\n- Nạp Âm Trụ Năm Mở Quẻ: {nap_am_nam} ({tb_year_key})\\n- Nạp Âm Trụ Ngày Mở Quẻ: {nap_am_ngay} ({tb_day_key})\\nLƯU Ý THẦN TOÁN: ĐÂY LÀ KHÍ CHẤT CỦA THỜI GIAN HIỆN TẠI, TUYỆT ĐỐI KHÔNG LẤY NÓ LÀM MỆNH (NĂM SINH) CỦA NGƯỜI DÙNG.\\n"
                        except Exception as e:
                            pass
                        
                        # CALL PHOENIX MASTER (FULL PIPELINE)
                        orc = PhoenixOrchestrator(st.session_state.gemini_helper)
                        
                        raw_response = orc.run_pipeline(
                            user_question, 
                            current_topic=safe_topic,
                            chart_data=temp_chart_data,
                            mai_hoa_data=temp_mai_hoa,
                            luc_hao_data=temp_luc_hao,
                            tb_context=tb_context
                        )
                    
                    # PROCESS & DISPLAY
                    response_text = st.session_state.gemini_helper._process_response(raw_response)
                    
                    # === SAVE TO CHAT HISTORY ===
                    st.session_state.chat_history.append({'role': 'user', 'content': user_question})
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})
                    # Giới hạn tối đa 10 cặp Q&A (20 messages)
                    if len(st.session_state.chat_history) > 20:
                        st.session_state.chat_history = st.session_state.chat_history[-20:]
                    
                    # === AUTO GROW TOPICS (CHỈ THÊM, KHÔNG BAO GIỜ XÓA) ===
                    try:
                        from ai_modules.shard_manager import add_entry
                        # Lưu câu hỏi thành chủ đề mới (nếu đủ dài)
                        if len(user_question.strip()) > 5:
                            topic_title = user_question.strip()[:100]  # Max 100 ký tự cho title
                            add_entry(
                                title=topic_title,
                                content=f"Câu hỏi: {user_question}\n\nChủ đề gốc: {safe_topic}\n\nTrả lời AI (tóm tắt): {response_text[:500]}",
                                category="Kiến Thức",
                                source="Auto-Generated from AI Q&A"
                            )
                            # Cập nhật danh sách chủ đề trong session (thêm vào, ko xóa)
                            if topic_title not in st.session_state.all_topics_full:
                                st.session_state.all_topics_full.append(topic_title)
                                st.session_state.all_topics_full = sorted(st.session_state.all_topics_full)
                    except Exception:
                        pass  # Không crash app nếu lưu topic lỗi
                    
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
                    
                    # RENDER
                    st.markdown("""
                    <div style='text-align: center; color: gray; padding: 20px 0;'>
                        --- <b>☯️ Kỳ Môn AI V32.2 — Unified Index + Offline Engine</b> ---<br>
                        <i>© 2024-2026 Cuongtan888888. All rights reserved.</i>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # RENDER WORKFLOW LOGS (User requested n8n visibility)
                    if hasattr(st.session_state.gemini_helper, 'render_logs'):
                        st.session_state.gemini_helper.render_logs()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        else:
            st.warning("⚠️ Vui lòng nhập câu hỏi")

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

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>© 2026 Vũ Việt Cường - Kỳ Môn Độn Giáp Web Application</p>
    <p>🌐 Chạy 24/7 trên Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)


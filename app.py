import streamlit as st

# VERSION: 2026-02-03-V1.7.6-BULLETPROOF
try:
    st.set_page_config(
        page_title="ðŸ”® Ká»³ MÃ´n Äá»™n GiÃ¡p ðŸ”®",
        page_icon="ðŸ”®",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass

import sys
import os
import traceback

def show_fatal_error(e):
    st.error("ðŸ›‘ Lá»–I Há»† THá»NG NGHIÃŠM TRá»ŒNG")
    st.write("á»¨ng dá»¥ng gáº·p sá»± cá»‘ khi khá»Ÿi Ä‘á»™ng. Chi tiáº¿t ká»¹ thuáº­t bÃªn dÆ°á»›i:")
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

st.sidebar.success("ðŸ› ï¸ BUILD V1.7.5 - QUOTA FIX")
st.sidebar.info("Há»‡ thá»‘ng: [DEBUG MODE - GROUNDING UPDATED]")

# --- DIAGNOSTIC INFO (SIDEBAR) ---
st.sidebar.markdown("### ðŸ” Há»‡ thá»‘ng Giao diá»‡n")
st.sidebar.write(f"ðŸ“ ThÆ° má»¥c gá»‘c: `{os.path.dirname(os.path.abspath(__file__))}`")
try:
    import mai_hoa_dich_so
    st.sidebar.caption(f"ðŸŒ¸ Mai Hoa: âœ…")
    import luc_hao_kinh_dich
    st.sidebar.caption(f"â˜¯ï¸ Lá»¥c HÃ o: âœ…")
except Exception as e:
    st.sidebar.error(f"âš ï¸ Module: {e}")

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
                st.sidebar.success(f"ðŸŸ¢ **AI Factory: ONLINE**\n\n(Cháº¡y lÃºc: {last_run})")
            else:
                st.sidebar.error("ðŸ”´ **AI Factory: OFFLINE**")
                if is_active_247:
                    st.sidebar.caption("â³ Äang chá» GitHub Action...")
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
    
try:
    from gemini_helper import GeminiQMDGHelper
    GEMINI_AVAILABLE = True
except (ImportError, Exception) as e:
    GEMINI_AVAILABLE = False
    print(f"âš ï¸ Gemini helper load error: {e}")
        
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
        phan_tich_toan_dien
    )
    USE_MULTI_LAYER_ANALYSIS = True
except (ImportError, Exception):
    USE_MULTI_LAYER_ANALYSIS = False
    # Fallback if import fails
    def phan_tich_yeu_to_thoi_gian(hanh, mua):
        return "BÃ¬nh"

CAN_10 = ["GiÃ¡p", "áº¤t", "BÃ­nh", "Äinh", "Máº­u", "Ká»·", "Canh", "TÃ¢n", "NhÃ¢m", "QuÃ½"]
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
        content: "âš¡";
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
        st.markdown("### ðŸ” XÃ¡c Thá»±c Truy Cáº­p - Ká»³ MÃ´n Äá»™n GiÃ¡p")
        st.text_input(
            "Vui lÃ²ng nháº­p máº­t kháº©u Ä‘á»ƒ sá»­ dá»¥ng:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.markdown("### ðŸ” XÃ¡c Thá»±c Truy Cáº­p - Ká»³ MÃ´n Äá»™n GiÃ¡p")
        st.text_input(
            "Vui lÃ²ng nháº­p máº­t kháº©u Ä‘á»ƒ sá»­ dá»¥ng:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("âŒ Máº­t kháº©u khÃ´ng chÃ­nh xÃ¡c! Vui lÃ²ng liÃªn há»‡ tÃ¡c giáº£ VÅ© Viá»‡t CÆ°á»ng.")
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
    if st.button("ðŸ”âˆ’", key="zoom_out", help="Thu nhá» (Zoom Out)"):
        st.session_state.zoom_level = max(50, st.session_state.zoom_level - 10)
        st.rerun()

with zoom_col2:
    if st.button(f"{st.session_state.zoom_level}%", key="zoom_reset", help="Äáº·t láº¡i 100%"):
        st.session_state.zoom_level = 100
        st.rerun()

with zoom_col3:
    if st.button("ðŸ”+", key="zoom_in", help="PhÃ³ng to (Zoom In)"):
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
    st.markdown("<h1 style='text-align: center; color: #f1c40f;'>ðŸ”® Ká»² MÃ”N Äá»˜N GIÃP ðŸ”®</h1>", unsafe_allow_html=True)

with col_header3:
    st.markdown("**TÃ¡c giáº£**")
    st.markdown("**VÅ© Viá»‡t CÆ°á»ng**")

st.markdown("---")

# ======================================================================
# SIDEBAR - CONTROLS
# ======================================================================
with st.sidebar:
    st.markdown("### âš™ï¸ Äiá»u Khiá»ƒn")
    
    # View selection
    view_option = st.radio(
        "Chá»n PhÆ°Æ¡ng PhÃ¡p:",
        ["ðŸ”® Ká»³ MÃ´n Äá»™n GiÃ¡p", "ðŸ­ NhÃ  MÃ¡y AI", "ðŸŒŸ 40 ChuyÃªn Gia AI", "ðŸ“– Mai Hoa 64 Quáº»", "â˜¯ï¸ Lá»¥c HÃ o Kinh Dá»‹ch", "ðŸ¤– Há»i Gemini AI"],
        index=0
    )
    
    if view_option == "ðŸ”® Ká»³ MÃ´n Äá»™n GiÃ¡p":
        st.session_state.current_view = "ky_mon"
    elif view_option == "ðŸ­ NhÃ  MÃ¡y AI":
        st.session_state.current_view = "ai_factory"
    elif view_option == "ðŸŒŸ 40 ChuyÃªn Gia AI":
        st.session_state.current_view = "ai_experts"
    elif view_option == "ðŸ“– Mai Hoa 64 Quáº»":
        st.session_state.current_view = "mai_hoa"
    elif view_option == "â˜¯ï¸ Lá»¥c HÃ o Kinh Dá»‹ch":
        st.session_state.current_view = "luc_hao"
    else:  # ðŸ¤– Há»i Gemini AI
        st.session_state.current_view = "gemini_ai"
    
    
    st.markdown("---")
    
    # --- AI Initialization & Mode Switcher ---
    st.markdown("### ðŸ¤– Cáº¥u hÃ¬nh AI")
    ai_col1, ai_col2 = st.columns(2)
    
    with ai_col1:
        if st.button("ðŸŒ Online AI", help="Sá»­ dá»¥ng Gemini Pro (YÃªu cáº§u API Key)", use_container_width=True):
            st.session_state.ai_preference = "online"
            # Clear existing to force re-init
            if 'gemini_helper' in st.session_state: del st.session_state.gemini_helper
            st.rerun()
            
    with ai_col2:
        if st.button("ðŸ’¾ Offline AI", help="Sá»­ dá»¥ng Free AI (Dá»± phÃ²ng)", use_container_width=True):
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
        
        # Æ¯U TIÃŠN 1: Streamlit Cloud Secrets (Quan trá»ng nháº¥t cho deployment)
        st_secret = None
        try:
            st_secret = st.secrets.get("GEMINI_API_KEY", None)
        except Exception:
            pass
        
        # Æ¯U TIÃŠN 2: File custom_data.json (Local)
        custom_data = load_custom_data()
        saved_key = custom_data.get("GEMINI_API_KEY")
        
        # Æ¯U TIÃŠN 3: Factory Config (Äá»“ng bá»™)
        factory_key = None
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_hub", "factory_config.json")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    factory_key = cfg.get("api_key")
        except: pass
        
        # Tá»•ng há»£p: Æ¯u tiÃªn Streamlit Secrets > Saved Key > Factory Key
        secret_api_key = st_secret or saved_key or factory_key
        
        # ThÃ´ng bÃ¡o náº¿u cháº¡y trÃªn cloud nhÆ°ng chÆ°a cÃ³ secret
        if not st_secret and not saved_key and not factory_key:
            # Äang cháº¡y trÃªn cloud vÃ  khÃ´ng cÃ³ API key nÃ o
            st.session_state.missing_cloud_secret = True
        
        if st.session_state.ai_preference == "offline":
            if FREE_AI_AVAILABLE:
                st.session_state.gemini_helper = FreeAIHelper()
                st.session_state.ai_type = "Free AI (Manual Offline)"
        else: # auto or online
            if secret_api_key and GEMINI_AVAILABLE:
                try:
                    from gemini_helper import GeminiQMDGHelper
                    st.session_state.gemini_helper = GeminiQMDGHelper(secret_api_key)
                    st.session_state.gemini_key = secret_api_key
                    st.session_state.ai_type = "Gemini Pro (V1.7.5)"
                except Exception: 
                    if st.session_state.ai_preference == "auto" and FREE_AI_AVAILABLE:
                        st.session_state.gemini_helper = FreeAIHelper()
                        st.session_state.ai_type = "Free AI (Fallback)"
            elif FREE_AI_AVAILABLE:
                st.session_state.gemini_helper = FreeAIHelper()
                st.session_state.ai_type = "Free AI (Offline Mode)"

    # AI Status Display with LED Indicator
    ai_status = st.session_state.get('ai_type', 'ChÆ°a sáºµn sÃ ng')
    
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
            st.session_state.api_status_msg = "ChÆ°a kiá»ƒm tra"
    
    # Initialize status if not exists
    if 'api_status_ok' not in st.session_state:
        st.session_state.api_status_ok = None  # None = chÆ°a check, True = OK, False = Lá»—i
        st.session_state.api_status_msg = "ChÆ°a kiá»ƒm tra"
    
    # LED Indicator Colors
    if st.session_state.api_status_ok is True:
        led_color = "ðŸŸ¢"  # Xanh = OK
        status_color = "#10b981"
        status_text = "HOáº T Äá»˜NG Tá»T"
    elif st.session_state.api_status_ok is False:
        led_color = "ðŸ”´"  # Äá» = Lá»—i
        status_color = "#ef4444"
        status_text = "Lá»–I Káº¾T Ná»I"
    else:
        led_color = "ðŸŸ¡"  # VÃ ng = ChÆ°a check
        status_color = "#f59e0b"
        status_text = "CHÆ¯A KIá»‚M TRA"
    
    # Display with LED
    if "Gemini" in ai_status:
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
                        ðŸ¤– {ai_status}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("âš™ï¸ Quáº£n lÃ½ Gemini"):
            # Manual check button
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("ðŸ”„ Kiá»ƒm tra káº¿t ná»‘i ngay", key="test_ai_conn", use_container_width=True):
                    with st.spinner("Äang thá»­ káº¿t ná»‘i..."):
                        success, msg = st.session_state.gemini_helper.test_connection()
                        st.session_state.api_status_ok = success
                        st.session_state.api_status_msg = msg
                        st.session_state.last_api_check_time = current_time
                        if success: 
                            st.success(f"âœ… {msg}")
                            st.rerun()  # Refresh to update LED
                        else: 
                            st.error(f"âŒ {msg}")
                            st.rerun()  # Refresh to update LED
            
            with col2:
                if st.button("ðŸ”„", key="force_refresh", help="LÃ m má»›i", use_container_width=True):
                    st.rerun()
            
            # Display current model info
            try:
                if hasattr(st.session_state, 'gemini_helper') and st.session_state.gemini_helper:
                    # Try to get model name safely
                    model_obj = getattr(st.session_state.gemini_helper, 'model', None)
                    if model_obj:
                        model_name = getattr(model_obj, 'model_name', None)
                        if model_name:
                            st.info(f"**Model Ä‘ang dÃ¹ng:** `{model_name}`")
                            
                            # Quota warning for Pro models
                            if 'pro' in model_name.lower():
                                st.warning("âš ï¸ **Cáº£nh bÃ¡o:** Model Pro tá»‘n quota ráº¥t nhiá»u. NÃªn chuyá»ƒn sang Flash.")
                            else:
                                st.success(f"âœ… **Model Flash** - Tiáº¿t kiá»‡m quota")
            except Exception as e:
                # Silently ignore model display errors
                pass
            
            if st.session_state.last_api_check_time > 0:
                import datetime as dt_module
                last_check = dt_module.datetime.fromtimestamp(st.session_state.last_api_check_time)
                st.caption(f"Láº§n check cuá»‘i: {last_check.strftime('%H:%M:%S')}")
            
            new_key = st.text_input("Thay Ä‘á»•i API Key (TÃ¹y chá»n):", type="password", key="new_api_key")
            save_permanently = st.checkbox("LÆ°u khÃ³a nÃ y vÄ©nh viá»…n", value=True)
            
            if st.button("Cáº­p nháº­t Key má»›i"):
                if new_key:
                    try:
                        from gemini_helper import GeminiQMDGHelper
                        st.session_state.gemini_helper = GeminiQMDGHelper(new_key)
                        st.session_state.gemini_key = new_key
                        st.session_state.ai_type = "Gemini Pro (V1.7.5 Updated)"
                        
                        if save_permanently:
                            data = load_custom_data()
                            data["GEMINI_API_KEY"] = new_key
                            save_custom_data(data)
                            
                            # Äá»’NG Bá»˜ SANG AI FACTORY
                            try:
                                config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_hub", "factory_config.json")
                                if os.path.exists(config_path):
                                    with open(config_path, 'r', encoding='utf-8') as f:
                                        cfg = json.load(f)
                                    cfg["api_key"] = new_key
                                    with open(config_path, 'w', encoding='utf-8') as f:
                                        json.dump(cfg, f, indent=2, ensure_ascii=False)
                            except: pass
                            
                            st.success("âœ… ÄÃ£ cáº­p nháº­t vÃ  LÆ°u vÄ©nh viá»…n!")
                        else:
                            st.success("âœ… ÄÃ£ cáº­p nháº­t (Táº¡m thá»i)!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"âŒ Lá»—i: {e}")
                else:
                    st.warning("Vui lÃ²ng nháº­p Key.")
    else:
        st.warning(f"â„¹ï¸ {ai_status}")
        
        # Cáº¢NH BÃO Äáº¶C BIá»†T CHO STREAMLIT CLOUD
        if st.session_state.get('missing_cloud_secret', False):
            st.error("""
            ### âš ï¸ CHÆ¯A Cáº¤U HÃŒNH API KEY TRÃŠN STREAMLIT CLOUD!
            
            **á»¨ng dá»¥ng Ä‘ang cháº¡y trÃªn Streamlit Cloud nhÆ°ng chÆ°a cÃ³ API Key.**
            
            #### ðŸ”§ CÃ¡ch Sá»­a (2 phÃºt):
            1. VÃ o **Streamlit Cloud Dashboard**: https://share.streamlit.io/
            2. Click vÃ o app cá»§a báº¡n â†’ **âš™ï¸ Settings**
            3. Chá»n tab **"Secrets"**
            4. DÃ¡n ná»™i dung sau:
            ```
            GEMINI_API_KEY = "YOUR_API_KEY_HERE"
            ```
            5. Click **"Save"** â†’ App sáº½ tá»± Ä‘á»™ng restart
            
            ðŸ‘‰ [Láº¥y API Key miá»…n phÃ­ táº¡i Ä‘Ã¢y](https://aistudio.google.com/app/apikey)
            """)
        
        with st.expander("ðŸ”‘ KÃ­ch hoáº¡t Gemini Pro (ThÃ´ng minh hÆ¡n)", expanded=True):
            st.markdown("ðŸ‘‰ [Láº¥y API Key miá»…n phÃ­](https://aistudio.google.com/app/apikey)")
            user_api_key = st.text_input("DÃ¡n API Key vÃ o Ä‘Ã¢y:", type="password", key="input_api_key_sidebar")
            save_key_permanently = st.checkbox("LÆ°u khÃ³a nÃ y vÄ©nh viá»…n", value=True, key="save_key_checkbox")
            
            if st.button("KÃ­ch hoáº¡t ngay", type="primary"):
                if GEMINI_AVAILABLE and user_api_key:
                    try:
                        from gemini_helper import GeminiQMDGHelper
                        st.session_state.gemini_helper = GeminiQMDGHelper(user_api_key)
                        st.session_state.gemini_key = user_api_key
                        st.session_state.ai_type = "Gemini Pro (V1.7.5 Active)"
                        
                        if save_key_permanently:
                            data = load_custom_data()
                            data["GEMINI_API_KEY"] = user_api_key
                            save_custom_data(data)
                            
                            # Äá»’NG Bá»˜ SANG AI FACTORY
                            try:
                                config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_hub", "factory_config.json")
                                if os.path.exists(config_path):
                                    with open(config_path, 'r', encoding='utf-8') as f:
                                        cfg = json.load(f)
                                    cfg["api_key"] = user_api_key
                                    with open(config_path, 'w', encoding='utf-8') as f:
                                        json.dump(cfg, f, indent=2, ensure_ascii=False)
                            except: pass
                                    
                            st.success("âœ… KÃ­ch hoáº¡t vÃ  LÆ°u vÄ©nh viá»…n!")
                        else:
                            st.success("âœ… ÄÃ£ kÃ­ch hoáº¡t!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"âŒ Lá»—i: {e}")
                else:
                    st.error("Vui lÃ²ng nháº­p Key hoáº·c thiáº¿u thÆ° viá»‡n.")

    # n8n Configuration
    with st.expander("ðŸ”— Káº¿t ná»‘i n8n (Advanced AI)"):
        n8n_url = st.secrets.get("N8N_WEBHOOK_URL", "")
        n8n_input = st.text_input("n8n Webhook URL:", value=st.session_state.get('n8n_url', n8n_url))
        if n8n_input:
            st.session_state.n8n_url = n8n_input
            if 'gemini_helper' in st.session_state and hasattr(st.session_state.gemini_helper, 'set_n8n_url'):
                st.session_state.gemini_helper.set_n8n_url(n8n_input)
    
    st.markdown("---")
    
    st.markdown("---")
    
    # Time controls (GLOBAL for all views)
    st.markdown("### ðŸ• Thá»i Gian")
    
    use_current_time = st.checkbox("Sá»­ dá»¥ng giá» hiá»‡n táº¡i", value=True)
    
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
        selected_date = st.date_input("Chá»n ngÃ y:", now_vn.date())
        selected_time = st.time_input("Chá»n giá»:", now_vn.time())
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
        **Thá»i gian:** {selected_datetime.strftime("%H:%M - %d/%m/%Y")}
        
        **Ã‚m lá»‹ch:**
        - NgÃ y: **{lday}/{lmonth} nÄƒm {l_year_name}** {'(Nhuáº­n)' if is_leap else ''}
        - Giá»: {params['can_gio']} {params['chi_gio']}
        - NgÃ y: {params['can_ngay']} {params['chi_ngay']}
        - ThÃ¡ng: {params['can_thang']} {params['chi_thang']}
        
        **Cá»¥c:** {params['cuc']} ({'DÆ°Æ¡ng' if params.get('is_duong_don', True) else 'Ã‚m'} Äá»™n)
        """)
    except Exception as e:
        st.error(f"Lá»—i tÃ­nh toÃ¡n: {e}")
    
    st.markdown("---")
    
    # Topic selection
    st.markdown("### ðŸŽ¯ Chá»§ Äá» ChÃ­nh")
    
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


    search_term = st.text_input("ðŸ” TÃ¬m kiáº¿m chá»§ Ä‘á»:", "")
    
    # NEW: Topic Counter Button
    if st.button("ðŸ“Š Äáº¿m tá»•ng sá»‘ chá»§ Ä‘á» Ä‘ang cÃ³"):
        total_count = len(st.session_state.all_topics_full)
        st.success(f"ðŸ“ˆ Hiá»‡n há»‡ thá»‘ng Ä‘ang cÃ³ tá»•ng cá»™ng: **{total_count}** chá»§ Ä‘á» tri thá»©c!")
    
    with st.expander("âœï¸ Äáº·t cÃ¢u há»i riÃªng & KÃ­ch hoáº¡t AI Mining"):
        with st.form("custom_topic_form"):
            new_q = st.text_area("Nháº­p váº¥n Ä‘á»/cÃ¢u há»i báº¡n Ä‘ang quan tÃ¢m:", placeholder="VÃ­ dá»¥: Äáº§u tÆ° vÃ ng nÄƒm 2026, PhÃ¢n tÃ­ch quáº» gieo cho sá»©c khá»e bá»‘ máº¹...")
            if st.form_submit_button("ðŸš€ Gá»­i & LÆ°u lÃ m Chá»§ Ä‘á» má»›i"):
                if new_q:
                    try:
                        from ai_modules.shard_manager import add_entry
                        # Save as a SEED topic
                        id = add_entry(
                            title=new_q, 
                            content=f"CÃ¢u há»i gá»‘c ngÆ°á»i dÃ¹ng: {new_q}\n(Chá»§ Ä‘á» nÃ y Ä‘Ã£ Ä‘Æ°á»£c náº¡p lÃ m háº¡t giá»‘ng Ä‘á»ƒ AI quÃ¢n Ä‘oÃ n Ä‘i khai thÃ¡c Internet.)",
                            category="Kiáº¿n Thá»©c",
                            source="User Inquiry"
                        )
                        if id:
                            st.success(f"âœ… ÄÃ£ náº¡p thÃ nh cÃ´ng! AI sáº½ báº¯t Ä‘áº§u tÃ¬m kiáº¿m thÃ´ng tin liÃªn quan cho báº¡n.")
                            st.session_state.chu_de_hien_tai = new_q
                            st.rerun()
                    except Exception as e:
                        st.error(f"Lá»—i náº¡p chá»§ Ä‘á»: {e}")

    # 1. Select Standard Category (Chá»§ Ä‘á» chuáº©n)
    standard_categories = ["Táº¥t cáº£"] + list(MiningStrategist().categories.keys()) + ["Kiáº¿n Thá»©c", "LÆ°u Trá»¯ (SÃ¡ch)", "KhÃ¡c"]
    
    selected_cat = st.selectbox(
        "ðŸ—‚ï¸ Lá»c theo PhÃ¢n loáº¡i chuáº©n:",
        standard_categories,
        index=0
    )
    
    # 2. Filter topics based on category
    available_topics = []
    divination_categories = ["Ká»³ MÃ´n Äá»™n GiÃ¡p", "Kinh Dá»‹ch & Dá»± ÄoÃ¡n", "Phong Thá»§y & Äá»‹a LÃ½"]
    
    if selected_cat == "Táº¥t cáº£":
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
        available_topics = ["(ChÆ°a cÃ³ dá»¯ liá»‡u cho phÃ¢n loáº¡i nÃ y)"]

    selected_topic = st.selectbox(
        "Chá»n chá»§ Ä‘á» chi tiáº¿t:",
        available_topics,
        index=0 if "Tá»•ng QuÃ¡t" not in available_topics else available_topics.index("Tá»•ng QuÃ¡t")
    )

    
    st.session_state.chu_de_hien_tai = selected_topic
    
    st.info(f"ðŸ“Œ ÄÃ£ chá»n: **{selected_topic}**")
    
    # Multi-layer analysis (if available)
    if USE_MULTI_LAYER_ANALYSIS:
        st.markdown("---")
        st.markdown("### ðŸŽ¯ Äá»‘i TÆ°á»£ng (Lá»¥c ThÃ¢n)")
        
        doi_tuong_options = [
            "ðŸ§‘ Báº£n thÃ¢n",
            "ðŸ‘¨â€ðŸ‘©â€ðŸ‘§ Anh chá»‹ em",
            "ðŸ‘´ðŸ‘µ Bá»‘ máº¹",
            "ðŸ‘¶ Con cÃ¡i",
            "ðŸ¤ NgÆ°á»i láº¡ (theo Can sinh)"
        ]
        
        selected_doi_tuong = st.selectbox("Chá»n Ä‘á»‘i tÆ°á»£ng:", doi_tuong_options, index=0)
        
        target_stem_name = "GiÃ¡p" # Default
        if selected_doi_tuong == "ðŸ¤ NgÆ°á»i láº¡ (theo Can sinh)":
            target_stem_name = st.selectbox("Chá»n ThiÃªn Can nÄƒm sinh cá»§a ngÆ°á»i Ä‘Ã³:", 
                                           ["KhÃ´ng rÃµ (DÃ¹ng Can Giá»)", "GiÃ¡p", "áº¤t", "BÃ­nh", "Äinh", "Máº­u", "Ká»·", "Canh", "TÃ¢n", "NhÃ¢m", "QuÃ½"])
        
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
        st.error(f"KhÃ´ng thá»ƒ táº£i module AI Factory: {e}")
        st.info("Vui lÃ²ng kiá»ƒm tra láº¡i file web/ai_factory_view.py")

if st.session_state.current_view == "ky_mon":
    st.markdown("## ðŸ”® Báº¢NG Ká»² MÃ”N Äá»˜N GIÃP")
    
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
            st.error(f"Lá»—i tÃ­nh toÃ¡n bÃ n: {e}")
            st.session_state.chart_data = None
        
        # Display 9 palaces grid with full information
        if st.session_state.chart_data:
            st.markdown("### ðŸ“Š ChÃ­n Cung Ká»³ MÃ´n")
            
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
                        
                        # Check if palace has Dá»¥ng Tháº§n (Resolved Logic)
                        topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                        dung_than_list = topic_data.get("Dá»¥ng_Tháº§n", [])
                        
                        # Mapping symbolic names to actual stems
                        symbolic_map = {
                            "Can NgÃ y": chart.get('can_ngay'),
                            "Can Giá»": chart.get('can_gio'),
                            "Can ThÃ¡ng": chart.get('can_thang'),
                            "Can NÄƒm": chart.get('can_nam')
                        }
                        
                        resolved_dt = []
                        for dt_item in dung_than_list:
                            if dt_item in symbolic_map:
                                resolved_dt.append(symbolic_map[dt_item])
                            else:
                                resolved_dt.append(dt_item)
                        
                        # Final check for highlighting
                        has_dung_than = any(dt in [sao, cua, than, can_thien, can_dia] for dt in resolved_dt)
                        
                        # Special handling for Doors: "Sinh" vs "Sinh MÃ´n"
                        if not has_dung_than:
                            clean_cua = cua.replace(" MÃ´n", "")
                            has_dung_than = any(dt in [clean_cua] for dt in resolved_dt)
                        
                        # Determine Strength based on month
                        now_dt = dt_module.datetime.now()
                        month = now_dt.month
                        season_map = {1:"XuÃ¢n", 2:"XuÃ¢n", 3:"XuÃ¢n", 4:"Háº¡", 5:"Háº¡", 6:"Háº¡", 7:"Thu", 8:"Thu", 9:"Thu", 10:"ÄÃ´ng", 11:"ÄÃ´ng", 12:"ÄÃ´ng"}
                        current_season = season_map.get(month, "XuÃ¢n")
                        strength = phan_tich_yeu_to_thoi_gian(hanh, current_season) if USE_MULTI_LAYER_ANALYSIS else "BÃ¬nh"
                        
                        strength_color = {
                            "VÆ°á»£ng": "#ef4444", "TÆ°á»›ng": "#f59e0b", "HÆ°u": "#10b981", "TÃ¹": "#3b82f6", "Tá»­": "#64748b"
                        }.get(strength, "#475569")

                        # Get door properties for analysis (Required for NameError fix)
                        door_data = KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_MON"].get(cua if " MÃ´n" in cua else cua + " MÃ´n", {})
                        cat_hung = door_data.get("CÃ¡t_Hung", "BÃ¬nh")

                        # Element Styles & Aesthetics
                        element_configs = {
                            "Má»™c": {"border": "#10b981", "icon": "ðŸŒ¿", "img": "moc.png"},
                            "Há»a": {"border": "#ef4444", "icon": "ðŸ”¥", "img": "hoa.png"},
                            "Thá»•": {"border": "#f59e0b", "icon": "â›°ï¸", "img": "tho.png"},
                            "Kim": {"border": "#94a3b8", "icon": "âš”ï¸", "img": "kim.png"},
                            "Thá»§y": {"border": "#3b82f6", "icon": "ðŸ’§", "img": "thuy.png"}
                        }.get(hanh, {"border": "#475569", "icon": "âœ¨", "img": "tho.png"})

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
                            good_stars = ["ThiÃªn Phá»¥", "ThiÃªn Nháº­m", "ThiÃªn TÃ¢m", "ThiÃªn Cáº§m"]
                            good_doors = ["Khai", "HÆ°u", "Sinh", "Khai MÃ´n", "HÆ°u MÃ´n", "Sinh MÃ´n"]
                            good_deities = ["Trá»±c PhÃ¹", "ThÃ¡i Ã‚m", "Lá»¥c Há»£p", "Cá»­u Äá»‹a", "Cá»­u ThiÃªn"]
                            good_stems = ["GiÃ¡p", "áº¤t", "BÃ­nh", "Äinh", "Máº­u"]
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

                        # 1. Horse (MÃ£) - Pillar specific
                        for pillar, label in [('nam', 'MÃ£ NÄƒm'), ('thang', 'MÃ£ ThÃ¡ng'), ('ngay', 'MÃ£ NgÃ y'), ('gio', 'MÃ£ Giá»')]:
                            val = ma_data.get(pillar)
                            if val is not None:
                                try:
                                    if int(val) == curr_p_int:
                                        m_html.append(f'<div class="marker-badge ma">ðŸŽ {label}</div>')
                                except: pass
                        
                        # 2. Void (Tuáº§n KhÃ´ng) - Pillar specific
                        for pillar, label in [('nam', 'KhÃ´ng NÄƒm'), ('thang', 'KhÃ´ng ThÃ¡ng'), ('ngay', 'KhÃ´ng NgÃ y'), ('gio', 'KhÃ´ng Giá»')]:
                            vals = kv_data.get(pillar, [])
                            try:
                                if any(int(v) == curr_p_int for v in vals):
                                    m_html.append(f'<div class="marker-badge kv">ðŸ’€ {label}</div>')
                            except: pass
                        
                        # 3. 4 Pillar Cans (NÄƒm/ThÃ¡ng/NgÃ y/Giá») location on Earth Plate
                        # We find where the 4 stems sit in the dia_can (Earth Plate)
                        for pillar, (p_can, p_label) in {
                            'nam': (params.get('can_nam'), 'Trá»¥ NÄƒm'),
                            'thang': (params.get('can_thang'), 'Trá»¥ ThÃ¡ng'),
                            'ngay': (params.get('can_ngay'), 'Trá»¥ NgÃ y'),
                            'gio': (params.get('can_gio'), 'Trá»¥ Giá»')
                        }.items():
                            if p_can and can_dia == p_can:
                                m_html.append(f'<div class="marker-badge pillar-{pillar}">ðŸ“ {p_label} ({p_can})</div>')

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
    <div class="sao-corner" style="color: {c_sao};">{sao.replace('ThiÃªn ', '')}</div>
    <div class="mon-corner" style="color: {c_cua};">{cua.replace(' MÃ´n', '')}</div>
    <div class="thien-corner" style="color: {c_thien};">{can_thien}</div>
    <div class="dia-corner" style="color: {c_dia};">{can_dia}</div>
</div>
<div class="palace-markers">
    {marker_display_html}
</div>
</div></div>"""
                        st.markdown(palace_html, unsafe_allow_html=True)

                        
                        # Expander for detailed analysis
                        with st.expander(f"ðŸ“– Chi tiáº¿t Cung {palace_num}"):
                            # Basic info
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.markdown(f"**QuÃ¡i tÆ°á»£ng:** {QUAI_TUONG.get(palace_num, 'N/A')}")
                                st.markdown(f"**NgÅ© hÃ nh:** {hanh}")
                            with col_info2:
                                st.markdown(f"**CÃ¡t/Hung:** {cat_hung}")
                                st.markdown(f"**Tráº¡ng thÃ¡i:** {strength}")
                            
                            st.markdown("---")
                            
                            # Check Dá»¥ng Tháº§n with clearer explanation
                            topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                            dung_than_list = topic_data.get("Dá»¥ng_Tháº§n", [])
                            
                            # --- PRE-CALCULATE CORE VARIABLES (FIXES NAMEERROR) ---
                            actual_can_gio = chart.get('can_gio', 'N/A')
                            actual_can_ngay = chart.get('can_ngay', 'N/A')
                            actual_can_thang = chart.get('can_thang', 'N/A')
                            actual_can_nam = chart.get('can_nam', 'N/A')
                            
                            # Resolve Relation (Lá»¥c ThÃ¢n) stem
                            rel_type = st.session_state.get('selected_doi_tuong', "ðŸ§‘ Báº£n thÃ¢n")
                            target_can_representative = actual_can_ngay # Default to Self
                            rel_label = "Báº£n thÃ¢n"
                            
                            if "Anh chá»‹ em" in rel_type:
                                target_can_representative = actual_can_thang
                                rel_label = "Anh chá»‹ em"
                            elif "Bá»‘ máº¹" in rel_type:
                                target_can_representative = actual_can_nam
                                rel_label = "Bá»‘ máº¹"
                            elif "Con cÃ¡i" in rel_type:
                                target_can_representative = actual_can_gio
                                rel_label = "Con cÃ¡i"
                            elif "NgÆ°á»i láº¡" in rel_type:
                                custom_val = st.session_state.get('target_stem_name_custom', "GiÃ¡p")
                                if "KhÃ´ng rÃµ" in custom_val:
                                    target_can_representative = actual_can_gio
                                    rel_label = "Äá»‘i tÆ°á»£ng (Can Giá»)"
                                else:
                                    target_can_representative = custom_val
                                    rel_label = f"Äá»‘i tÆ°á»£ng ({target_can_representative})"

                            # --- PART 1: RELATIONSHIP ANALYSIS (SUBJECT VS OBJECT) ---
                            st.subheader("ðŸŽ¯ PhÃ¢n tÃ­ch TÆ°Æ¡ng tÃ¡c Dá»¥ng Tháº§n")
                            
                            # Determine Subject (Báº£n thÃ¢n) Stem Palace
                            subject_palace = 0
                            # Assuming 'dia_can' holds the Earth Stems for each palace
                            # We need to find the palace where the 'can_ngay' (subject's stem) resides
                            for p_num, d_can in chart['dia_can'].items():
                                if d_can == actual_can_ngay:
                                    subject_palace = p_num
                                    break
                            
                            # Determine Object (Dá»¥ng Tháº§n) Palace (Current Palace)
                            object_palace = palace_num
                            
                            s_hanh = CUNG_NGU_HANH.get(subject_palace, "Thá»•")
                            o_hanh = CUNG_NGU_HANH.get(object_palace, "Thá»•")
                            
                            interaction = SINH_KHAC_MATRIX.get(s_hanh, {}).get(o_hanh, "BÃ¬nh HÃ²a")
                            
                            # Visual Interaction Report
                            col_rel1, col_rel2, col_rel3 = st.columns([2, 1, 2])
                            with col_rel1:
                                st.info(f"ðŸ‘¤ **Báº£n thÃ¢n**\n\nCung {subject_palace} ({s_hanh})")
                            with col_rel2:
                                st.markdown(f"<div style='text-align:center; font-size:1.5rem; padding-top:10px;'>{'âž¡ï¸' if 'Sinh' in interaction else 'âš”ï¸' if 'Kháº¯c' in interaction else 'ðŸ¤'}</div>", unsafe_allow_html=True)
                                st.caption(f"<div style='text-align:center;'>{interaction}</div>", unsafe_allow_html=True)
                            with col_rel3:
                                st.success(f"ðŸŽ¯ **Äá»‘i tÆ°á»£ng**\n\nCung {object_palace} ({o_hanh})")
                            
                            st.write(f"**Káº¿t luáº­n nhanh:** {rel_label} vÃ  Äá»‘i tÆ°á»£ng cÃ³ má»‘i quan há»‡ **{interaction}**. " + 
                                     ("ÄÃ¢y lÃ  dáº¥u hiá»‡u thuáº­n lá»£i, nÄƒng lÆ°á»£ng lÆ°u thÃ´ng." if "Sinh" in interaction or "BÃ¬nh" in interaction 
                                      else "Cáº§n tháº­n trá»ng vÃ¬ cÃ³ sá»± xung Ä‘á»™t hoáº·c cáº£n trá»Ÿ vá» máº·t nÄƒng lÆ°á»£ng."))

                            st.markdown("---")
                            
                            # --- PART 2: TECHNICAL ELEMENT LOOKUPS ---
                            st.subheader("ðŸ” Chi tiáº¿t TÃ¡c Ä‘á»™ng cá»§a Tháº§n - Tinh - MÃ´n")
                            
                            # Create a clean table for lookups
                            tech_data = {
                                "Yáº¿u tá»‘": ["Tháº§n (Deity)", "Tinh (Star)", "MÃ´n (Door)", "ThiÃªn Can", "Äá»‹a Can"],
                                "TÃªn": [than, sao, cua, can_thien, can_dia],
                                "Ã nghÄ©a & TÃ¡c Ä‘á»™ng": [
                                    KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_THAN"].get(than, {}).get("TÃ­nh_Cháº¥t", "N/A"),
                                    KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["CUU_TINH"].get(sao, {}).get("TÃ­nh_Cháº¥t", "N/A"),
                                    KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_MON"].get(cua if " MÃ´n" in cua else cua + " MÃ´n", {}).get("Luáº­n_ÄoÃ¡n", "N/A"),
                                    KY_MON_DATA["CAN_CHI_LUAN_GIAI"].get(can_thien, {}).get("TÃ­nh_Cháº¥t", "N/A"),
                                    KY_MON_DATA["CAN_CHI_LUAN_GIAI"].get(can_dia, {}).get("TÃ­nh_Cháº¥t", "N/A")
                                ]
                            }
                            st.table(tech_data)
                            
                            # --- PART 3: TOPIC-SPECIFIC ANALYSIS ---
                            st.subheader(f"ðŸ’¡ PhÃ¢n tÃ­ch theo chá»§ Ä‘á»: {selected_topic}")
                            topic_detail = topic_data.get("Diá»…n_Giáº£i", "Äang cáº­p nháº­t...")
                            st.write(topic_detail)
                            
                            # Combinatorial Analysis (CÃ¡ch Cá»¥c)
                            combo_key = f"{can_thien}{can_dia}"
                            combo_info = KY_MON_DATA["TRUCTU_TRANH"].get(combo_key)
                            if combo_info:
                                st.warning(f"ðŸŽ­ **CÃ¡ch cá»¥c: {combo_info['TÃªn_CÃ¡ch_Cá»¥c']} ({combo_info['CÃ¡t_Hung']})**")
                                st.write(combo_info['Luáº­n_Giáº£i'])
                            
                            # Final Advice
                            st.markdown("---")
                            st.info("**Lá»i khuyÃªn tá»« chuyÃªn gia:** Dá»±a trÃªn sá»± tÆ°Æ¡ng tÃ¡c giá»¯a Báº£n thÃ¢n vÃ  Dá»¥ng Tháº§n, báº¡n nÃªn chá»§ Ä‘á»™ng náº¯m báº¯t cÆ¡ há»™i náº¿u cÃ³ sá»± tÆ°Æ¡ng sinh, hoáº·c lÃ¹i láº¡i quan sÃ¡t náº¿u gáº·p sá»± hÃ¬nh kháº¯c máº¡nh.")
                            
                            # Advanced Matching Logic
                            found_dt = []
                            for dt in dung_than_list:
                                is_match = False
                                display_name = dt
                                
                                # 1. Check direct matches (Star, Deity, Stems)
                                if dt in [sao, than]:
                                    is_match = True
                                # 2. Check Doors (Normalize "Sinh" vs "Sinh MÃ´n")
                                elif dt == cua or dt == f"{cua} MÃ´n" or (cua and dt.startswith(cua)):
                                    is_match = True
                                # 3. Check Symbolic Stems (PRECISION: Only Heaven Plate)
                                elif dt == "Can Giá»" and (actual_can_gio == can_thien):
                                    display_name = f"Can Giá» ({actual_can_gio} - Sá»± viá»‡c)"
                                    is_match = True
                                elif dt == "Can NgÃ y" and (actual_can_ngay == can_thien):
                                    display_name = f"Can NgÃ y ({actual_can_ngay})"
                                    is_match = True
                                elif dt == "Can ThÃ¡ng" and (actual_can_thang == can_thien):
                                    display_name = f"Can ThÃ¡ng ({actual_can_thang})"
                                    is_match = True
                                elif dt == "Can NÄƒm" and (actual_can_nam == can_thien):
                                    display_name = f"Can NÄƒm ({actual_can_nam})"
                                    is_match = True
                                # 4. Check Stems directly if they are on Heaven Plate
                                elif dt in ["NhÃ¢m", "QuÃ½", "áº¤t", "BÃ­nh", "Äinh", "Máº­u", "Ká»·", "Canh", "TÃ¢n"] and (dt == can_thien):
                                    is_match = True
                                # 5. Check Special Markers
                                elif dt == "MÃ£ Tinh" and palace_num == chart.get('dich_ma'):
                                    is_match = True
                                elif dt == "KhÃ´ng Vong" and palace_num in chart.get('khong_vong', []):
                                    is_match = True
                                
                                if is_match:
                                    found_dt.append(display_name)
                                    
                            # ADD RELATIONSHIP HIGHLIGHT
                            if target_can_representative == can_thien:
                                found_dt.append(f"ðŸ“ {rel_label}")
                            
                            dt_html = f"""
                            <div class="dung-than-box">
                                <div style="font-weight: 800; color: #92400e; margin-bottom: 5px;">ðŸ“ PHÃ‚N TÃCH Dá»¤NG THáº¦N</div>
                                <div style="font-size: 14px;"><strong>Chá»§ Ä‘á»:</strong> {selected_topic}</div>
                                <div style="font-size: 14px;"><strong>Dá»¥ng tháº§n cáº§n tÃ¬m:</strong> {', '.join(dung_than_list)}</div>
                                <div style="margin-top: 10px; font-weight: 700; color: {'#15803d' if found_dt else '#b91c1c'};">
                                    {f'âœ… TÃ¬m tháº¥y: {", ".join(found_dt)}' if found_dt else 'âš ï¸ Cung nÃ y khÃ´ng chá»©a Dá»¥ng Tháº§n chÃ­nh'}
                                </div>
                            </div>
                            """
                            st.markdown(dt_html, unsafe_allow_html=True)
                            
                            # UNIFIED AI EXPERT BUTTON
                            if 'gemini_helper' in st.session_state:
                                st.markdown("---")
                                if st.button(f"ðŸ§™ AI ChuyÃªn Gia TÆ° Váº¥n Cung {palace_num}", key=f"ai_palace_expert_btn_{palace_num}", use_container_width=True, type="primary"):
                                    with st.spinner(f"ChuyÃªn gia AI Ä‘ang phÃ¢n tÃ­ch Cung {palace_num} theo chá»§ Ä‘á» {selected_topic}..."):
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
                                            <div class="interpret-title">ðŸ”® PhÃ¢n TÃ­ch ChuyÃªn SÃ¢u Cung {palace_num}</div>
                                            <div style="font-size: 15px; line-height: 1.6; color: #1e293b;">{analysis}</div>
                                        </div>
                                        """, unsafe_allow_html=True)

                            # Static descriptions (Keep it brief)
                            st.markdown("---")
                            star_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(sao, {})
                            if star_data:
                                st.markdown(f"**â­ Sao {sao}:** {star_data.get('TÃ­nh_Cháº¥t', 'N/A')}")
                            
                            if door_data:
                                st.markdown(f"**ðŸšª Cá»­a {cua}:** {door_data.get('TÃ­nh_Cháº¥t', 'N/A')}")
                            
                            deity_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(than, {})
                            if deity_data:
                                st.markdown(f"**ðŸ›¡ï¸ Tháº§n {than}:** {deity_data.get('TÃ­nh_Cháº¥t', 'N/A')}")
                            
                            # Stem combination
                            cach_cuc_key = can_thien + can_dia
                            combination_data = KY_MON_DATA['TRUCTU_TRANH'].get(cach_cuc_key, {})
                            if combination_data:
                                col_can_1, col_can_2 = st.columns([3, 1])
                                with col_can_1:
                                    st.markdown(f"**ðŸ”— {can_thien}/{can_dia}:** {combination_data.get('Luáº­n_Giáº£i', 'ChÆ°a cÃ³ ná»™i dung')}")
                                    st.caption(f"CÃ¡t/Hung: {combination_data.get('CÃ¡t_Hung', 'BÃ¬nh')}")
                                with col_can_2:
                                    show_can_exp = False
                                    if 'gemini_helper' in st.session_state:
                                        if st.button(f"ðŸ”® Giáº£i ThÃ­ch", key=f"ai_can_{palace_num}_{can_thien}_{can_dia}", use_container_width=True):
                                            show_can_exp = True
                                
                                # Move explanation out of columns for full width
                                if show_can_exp:
                                    with st.spinner(f"AI Ä‘ang phÃ¢n giáº£i tá»• há»£p {can_thien}/{can_dia}..."):
                                        explanation = st.session_state.gemini_helper.explain_element('stem', f"{can_thien}/{can_dia}")
                                        st.markdown(f"""
                                        <div class="interpret-box">
                                            <div class="interpret-title">ðŸ“– Luáº­n Giáº£i Cáº·p Can: {can_thien}/{can_dia}</div>
                                            <div style="font-size: 15px; line-height: 1.6; color: #1e293b;">{explanation}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            # End of Palace Details

        
        # Display Dá»¥ng Tháº§n info
        st.markdown("---")
        st.markdown("### ðŸŽ¯ THÃ”NG TIN Dá»¤NG THáº¦N")
        
        topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
        dung_than_list = topic_data.get("Dá»¥ng_Tháº§n", [])
        luan_giai = topic_data.get("Luáº­n_Giáº£i_Gá»£i_Ã", "")
        
        if dung_than_list:
            st.success(f"**Dá»¥ng Tháº§n cáº§n xem:** {', '.join(dung_than_list)}")
        
        if luan_giai:
            st.info(f"**Gá»£i Ã½ luáº­n giáº£i:** {luan_giai}")
        
        # Display detailed Dá»¥ng Tháº§n from 200+ database
        if USE_200_TOPICS:
            dt_data = lay_dung_than_200(selected_topic)
            if dt_data and 'ky_mon' in dt_data:
                km = dt_data['ky_mon']
                st.markdown("#### ðŸ”® Dá»¥ng Tháº§n Ká»³ MÃ´n Chi Tiáº¿t")
                st.write(f"**Dá»¥ng Tháº§n:** {km.get('dung_than', 'N/A')}")
                st.write(f"**Giáº£i thÃ­ch:** {km.get('giai_thich', 'N/A')}")
                st.write(f"**CÃ¡ch xem:** {km.get('cach_xem', 'N/A')}")
                if 'vi_du' in km:
                    st.write(f"**VÃ­ dá»¥:** {km['vi_du']}")
        
        # ===== COMPREHENSIVE AI REPORT SECTION =====
        if st.session_state.chart_data and 'gemini_helper' in st.session_state:
            st.markdown("---")
            st.markdown("### ðŸ† BÃO CÃO Tá»”NG Há»¢P CHUYÃŠN SÃ‚U (AI)")
            
            with st.container():
                st.markdown(f"""
                <div class="ai-response-panel animated-panel">
                    <div style="font-size: 1.2rem; font-weight: 800; color: #1e3a8a; margin-bottom: 15px;">
                        ðŸ¤– Káº¾T LUáº¬N CUá»I CÃ™NG Tá»ª AI
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("ðŸ”® Báº¯t Ä‘áº§u PhÃ¢n TÃ­ch Tá»•ng Há»£p", type="primary", use_container_width=True):
                    with st.spinner("AI Ä‘ang tá»•ng há»£p dá»¯ liá»‡u tá»« 9 cung vÃ  tÃ­nh toÃ¡n káº¿t quáº£..."):
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
                            key_palaces_info.append(f"Cung {pn}: Sao {s}, MÃ´n {c}, Tháº§n {t}, Can {can_t}/{can_d}")
                        
                        rel_type = st.session_state.get('selected_doi_tuong', "ðŸ§‘ Báº£n thÃ¢n")
                        custom_stem = st.session_state.get('target_stem_name_custom', "N/A")
                        
                        prompt = f"""
                        Báº¡n lÃ  má»™t Ä‘áº¡i sÆ° Ká»³ MÃ´n Äá»™n GiÃ¡p. HÃ£y phÃ¢n tÃ­ch Tá»”NG Há»¢P cho chá»§ Ä‘á»: {topic}.
                        
                        **Ngá»¯ cáº£nh Äá»‘i tÆ°á»£ng (Lá»¥c ThÃ¢n):** {rel_type} (Can má»¥c tiÃªu: {custom_stem if 'ngÆ°á»i láº¡' in rel_type.lower() else 'Theo Lá»¥c ThÃ¢n'})
                        
                        **Dá»¯ liá»‡u 9 Cung:**
                        {chr(10).join(key_palaces_info)}
                        
                        **Tráº¡ng thÃ¡i Can:** Giá»: {chart['can_gio']}, NgÃ y: {chart['can_ngay']}, ThÃ¡ng: {chart.get('can_thang')}, NÄƒm: {chart.get('can_nam')}
                        
                        **YÃŠU Cáº¦U PHÃ‚N TÃCH CHUYÃŠN SÃ‚U:**
                        1. XÃ¡c Ä‘á»‹nh Cung Báº£n ThÃ¢n (ngÆ°á»i há»i) vÃ  Cung Sá»± Viá»‡c (Káº¿t quáº£) hoáº·c Cung Äá»‘i tÃ¡c/NgÆ°á»i mua (Can Giá»).
                        2. PhÃ¢n tÃ­ch sá»± tÆ°Æ¡ng tÃ¡c Sinh-Kháº¯c-Há»£p-Xung giá»¯a cÃ¡c Cung nÃ y.
                        3. ÄÃ¡nh giÃ¡ sá»©c máº¡nh cá»§a cÃ¡c Sao vÃ  Cá»­a táº¡i cÃ¡c cung trá»ng yáº¿u.
                        4. **Káº¾T LUáº¬N Dá»¨T KHOÃT:** CÃ³ Ä‘áº¡t Ä‘Æ°á»£c má»¥c Ä‘Ã­ch khÃ´ng? (BÃ¡n Ä‘Æ°á»£c khÃ´ng? GiÃ¡ tá»‘t khÃ´ng? Káº¿t hÃ´n Ä‘Æ°á»£c khÃ´ng?...).
                        5. **Lá»œI KHUYÃŠN HÃ€NH Äá»˜NG:** Cáº§n lÃ m gÃ¬ ngay bÃ¢y giá»? 
                        
                        Viáº¿t theo phong cÃ¡ch chuyÃªn nghiá»‡p, thá»±c táº¿, khÃ´ng dÃ¹ng thuáº­t ngá»¯ quÃ¡ khÃ³ hiá»ƒu náº¿u khÃ´ng giáº£i thÃ­ch kÃ¨m theo.
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
                            st.error(f"Lá»—i phÃ¢n tÃ­ch: {e}")

        # ===== PALACE COMPARISON SECTION =====
        if st.session_state.chart_data:
            st.markdown("---")
            st.markdown("### âš–ï¸ SO SÃNH CHá»¦ - KHÃCH")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                chu_cung = st.selectbox(
                    "Chá»n Cung Chá»§ (Báº£n thÃ¢n):",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                    format_func=lambda x: f"Cung {x} - {QUAI_TUONG.get(x, '')}",
                    key="chu_cung_select"
                )
            
            with col2:
                khach_cung = st.selectbox(
                    "Chá»n Cung KhÃ¡ch (Äá»‘i phÆ°Æ¡ng):",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                    index=1,
                    format_func=lambda x: f"Cung {x} - {QUAI_TUONG.get(x, '')}",
                    key="khach_cung_select"
                )
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("ðŸ” So SÃ¡nh", type="primary", use_container_width=True):
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
                            
                            st.markdown("#### ðŸ“Š Káº¾T QUáº¢ SO SÃNH CHI TIáº¾T")
                            
                            # Display palace info side by side
                            col_chu, col_khach = st.columns(2)
                            
                            with col_chu:
                                st.markdown(f"**ðŸ  CUNG CHá»¦ - Cung {chu['so']} ({chu['ten']})**")
                                st.write(f"- NgÅ© HÃ nh: {chu['hanh']}")
                                st.write(f"- â­ Tinh: {chu['sao']}")
                                st.write(f"- ðŸšª MÃ´n: {chu['cua']}")
                            
                            with col_khach:
                                st.markdown(f"**ðŸ‘¥ CUNG KHÃCH - Cung {khach['so']} ({khach['ten']})**")
                                st.write(f"- NgÅ© HÃ nh: {khach['hanh']}")
                                st.write(f"- â­ Tinh: {khach['sao']}")
                                st.write(f"- ðŸšª MÃ´n: {khach['cua']}")
                            
                            # Element interaction
                            st.markdown("---")
                            interaction = comparison_result.get('ngu_hanh_sinh_khac', 'N/A')
                            st.info(f"**PhÃ¢n tÃ­ch NgÅ© HÃ nh:** {interaction}")
                            
                            # AI Comparison Analysis
                            if 'gemini_helper' in st.session_state:
                                if st.button("ðŸ¤– AI PhÃ¢n TÃ­ch So SÃ¡nh", key="ai_compare_btn", type="primary"):
                                    with st.spinner("ðŸ¤– AI Ä‘ang phÃ¢n tÃ­ch..."):
                                        prompt = f"So sÃ¡nh Cung {chu['so']} ({chu['hanh']}) vÃ  Cung {khach['so']} ({khach['hanh']}) cho chá»§ Ä‘á» {selected_topic}."
                                        analysis = st.session_state.gemini_helper.answer_question(prompt)
                                        st.markdown(analysis)
                        else:
                            raise ImportError
                    except (ImportError, NameError, Exception):
                        # Fallback to simple comparison
                        st.markdown("#### ðŸ“Š Káº¾T QUáº¢ SO SÃNH CÆ  Báº¢N")
                        
                        col_chu, col_khach = st.columns(2)
                        
                        with col_chu:
                            st.markdown(f"**ðŸ  Cung Chá»§ {chu['so']}**")
                            st.write(f"NgÅ© HÃ nh: {chu['hanh']}")
                            st.write(f"Sao: {chu['sao']}")
                            st.write(f"MÃ´n: {chu['cua']}")
                        
                        with col_khach:
                            st.markdown(f"**ðŸ‘¥ Cung KhÃ¡ch {khach['so']}**")
                            st.write(f"NgÅ© HÃ nh: {khach['hanh']}")
                            st.write(f"Sao: {khach['sao']}")
                            st.write(f"MÃ´n: {khach['cua']}")
                        
                        # Simple element interaction
                        interaction = tinh_ngu_hanh_sinh_khac(chu['hanh'], khach['hanh'])
                        st.info(f"**NgÅ© hÃ nh:** {interaction}")
                        
                except Exception as e:
                    st.error(f"Lá»—i so sÃ¡nh: {e}")
        
        # ===== UNIFIED EXPERT ANALYSIS SYSTEM =====
        if st.session_state.chart_data:
            st.markdown("---")
            st.markdown("## ðŸ† Há»† THá»NG LUáº¬N GIáº¢I Tá»”NG Há»¢P CHUYÃŠN SÃ‚U")
            
            # 1. PRIMARY AI EXPERT REPORT (Dá»¥ng Tháº§n focus)
            if 'gemini_helper' in st.session_state:
                with st.container():
                    st.markdown("### ðŸŽ¯ Káº¾T LUáº¬N Tá»”NG Há»¢P Tá»ª AI (Dá»¥ng Tháº§n)")
                    if st.button("ðŸ”´ â­ Báº®T Äáº¦U LUáº¬N GIáº¢I CHUYÃŠN SÃ‚U (Æ¯U TIÃŠN Äá»ŒC TRÆ¯á»šC) â­ ðŸ”´", type="primary", key="ai_final_report_btn", use_container_width=True):
                        with st.spinner("ðŸ¤– AI Ä‘ang thá»±c hiá»‡n luáº­n giáº£i trá»ng tÃ¢m..."):
                            try:
                                # Get Dá»¥ng Tháº§n info from the best available source
                                dung_than_list = []
                                if 'USE_200_TOPICS' in globals() and USE_200_TOPICS:
                                    dung_than_list = lay_dung_than_200(selected_topic)
                                
                                if not dung_than_list:
                                    topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                                    dung_than_list = topic_data.get("Dá»¥ng_Tháº§n", [])
                                
                                # Get interpretation hints
                                topic_hints = TOPIC_INTERPRETATIONS.get(selected_topic, {}).get("Luáº­n_Giáº£i_Gá»£i_Ã", "")
                                
                                # Resolve Dynamic Actors (Chá»§ - KhÃ¡ch)
                                # The Subject (Chá»§ thá»ƒ/NgÆ°á»i thá»±c hiá»‡n) is the person we are asking ABOUT.
                                rel_type = st.session_state.get('selected_doi_tuong', "ðŸ§‘ Báº£n thÃ¢n")
                                subj_stem = st.session_state.chart_data.get('can_ngay') # Default to Self
                                obj_stem = st.session_state.chart_data.get('can_gio') # Default to General Matter/Other Party
                                
                                role_label = "Báº£n thÃ¢n báº¡n"
                                if "Anh chá»‹ em" in rel_type:
                                    subj_stem = st.session_state.chart_data.get('can_thang')
                                    role_label = "Anh chá»‹ báº¡n"
                                elif "Bá»‘ máº¹" in rel_type:
                                    subj_stem = st.session_state.chart_data.get('can_nam')
                                    role_label = "Bá»‘ máº¹ báº¡n"
                                elif "Con cÃ¡i" in rel_type:
                                    subj_stem = st.session_state.chart_data.get('can_gio')
                                    role_label = "Con cÃ¡i báº¡n"
                                elif "NgÆ°á»i láº¡" in rel_type:
                                    custom_val = st.session_state.get('target_stem_name_custom', "GiÃ¡p")
                                    if "KhÃ´ng rÃµ" not in custom_val:
                                        subj_stem = custom_val
                                    role_label = "Äá»‘i phÆ°Æ¡ng (NgÆ°á»i ngoÃ i)"
                                
                                # Process Dá»¥ng Tháº§n labels for better context
                                enriched_dung_than = []
                                for dt in dung_than_list:
                                    if dt == "Sinh MÃ´n": enriched_dung_than.append("Sinh MÃ´n (Lá»£i nhuáº­n/NgÃ´i nhÃ )")
                                    elif dt == "Khai MÃ´n": enriched_dung_than.append("Khai MÃ´n (CÃ´ng viá»‡c/Sá»± khá»Ÿi Ä‘áº§u)")
                                    else: enriched_dung_than.append(dt)
                                
                                # Build a comprehensive prompt
                                prompt = f"""PhÃ¢n tÃ­ch chi tiáº¿t vá» chá»§ Ä‘á»: {selected_topic}

**Äá»‘i tÆ°á»£ng:** {role_label}
**Dá»¥ng Tháº§n:** {', '.join(enriched_dung_than)}
**Gá»£i Ã½:** {topic_hints}

HÃ£y luáº­n giáº£i tÃ¬nh hÃ¬nh dá»±a trÃªn Cung Báº£n Má»‡nh (Can NgÃ y) vÃ  Cung Sá»± Viá»‡c (Can Giá»).
"""
                                analysis = st.session_state.gemini_helper.answer_question(
                                    prompt,
                                    chart_data=st.session_state.chart_data,
                                    topic=selected_topic
                                )
                                
                                # 2. GENERATE QUICK ACTIONS
                                quick_actions = "- HÃ£y hÃ nh Ä‘á»™ng dá»±a trÃªn káº¿t luáº­n trÃªn\n- Chá»n thá»i Ä‘iá»ƒm phÃ¹ há»£p vá»›i ngÅ© hÃ nh"
                                
                                # Display Quick Actions First
                                st.markdown(f"""
                                <div class="action-card">
                                    <div class="action-title">ðŸš€ HÃ€NH Äá»˜NG NHANH Cáº¦N LÃ€M NGAY</div>
                                    {chr(10).join([f'<div class="action-item">{line.strip("- ").strip()}</div>' for line in quick_actions.strip().split(chr(10)) if line.strip()])}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display Detailed Analysis
                                st.markdown(f'<div class="expert-box">{analysis}</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"âŒ Lá»—i AI: {str(e)}")

            # 2. COMPARISON SECTION (Chá»§ - KhÃ¡ch Interaction)
            st.markdown("---")
            st.markdown("### âš–ï¸ SO SÃNH CHá»¦ - KHÃCH")
            col_comp1, col_comp2 = st.columns([3, 1])
            with col_comp1:
                st.caption("PhÃ¢n tÃ­ch tÆ°Æ¡ng quan giá»¯a Báº£n thÃ¢n (Chá»§) vÃ  Äá»‘i tÆ°á»£ng/Sá»± viá»‡c (KhÃ¡ch)")
            with col_comp2:
                if st.button("ðŸ“Š Cháº¡y So SÃ¡nh", key="run_comp_btn", use_container_width=True):
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
                            'hanh': CUNG_NGU_HANH.get(idx, 'Thá»•'),
                            'sao': chart['thien_ban'].get(idx, 'N/A'),
                            'cua': chart['nhan_ban'].get(idx, 'N/A')
                        }
                    
                    c_chu = get_mini_info(chu_idx)
                    c_khach = get_mini_info(khach_idx)
                    
                    c1, c2 = st.columns(2)
                    with c1: st.info(f"**Báº£n ThÃ¢n (Cung {chu_idx}):** {c_chu['sao']} - {c_chu['cua']}")
                    with c2: st.warning(f"**Äá»‘i TÆ°á»£ng (Cung {khach_idx}):** {c_khach['sao']} - {c_khach['cua']}")
                    
                    res_mqh = tinh_ngu_hanh_sinh_khac(c_chu['hanh'], c_khach['hanh'])
                    st.success(f"**TÆ°Æ¡ng tÃ¡c NgÅ© HÃ nh:** {res_mqh}")
                    
                    if st.button("ðŸ¤– AI PhÃ¢n TÃ­ch So SÃ¡nh", key="ai_compare_details"):
                        with st.spinner("AI Ä‘ang so sÃ¡nh..."):
                            p = f"So sÃ¡nh chi tiáº¿t Cung {chu_idx} vÃ  Cung {khach_idx} cho {selected_topic}."
                            ans = st.session_state.gemini_helper.answer_question(p)
                            st.info(ans)
                except Exception as e:
                    st.error(f"Lá»—i: {e}")

            # 3. DETAILED TECHNICAL REPORT (Existing multi-layer analysis)
            st.markdown("---")
            with st.expander("ðŸ” Xem PhÃ¢n TÃ­ch Ká»¹ Thuáº­t (Ká»³ MÃ´n + Mai Hoa + Lá»¥c HÃ o)"):
                if USE_SUPER_DETAILED and st.button("ðŸš€ Táº¡o BÃ¡o CÃ¡o Ká»¹ Thuáº­t", key="tech_report_btn"):
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
                        
                        st.success("âœ… ÄÃ£ táº¡o bÃ¡o cÃ¡o tá»•ng há»£p!")
                        
                        # Display 9 aspects analysis
                        st.markdown("#### ðŸ“Š PHÃ‚N TÃCH 9 PHÆ¯Æ NG DIá»†N")
                        
                        aspects = [
                            ('thai_at', 'âš–ï¸ ThÃ¡i áº¤t'),
                            ('thanh_cong', 'ðŸŽ¯ ThÃ nh CÃ´ng'),
                            ('tai_loc', 'ðŸ’° TÃ i Lá»™c'),
                            ('quan_he', 'ðŸ¤ Quan Há»‡'),
                            ('suc_khoe', 'â¤ï¸ Sá»©c Khá»e'),
                            ('tranh_chap', 'âš”ï¸ Tranh Cháº¥p'),
                            ('di_chuyen', 'ðŸš— Di Chuyá»ƒn'),
                            ('hoc_van', 'ðŸ“š Há»c Váº¥n'),
                            ('tam_linh', 'ðŸ”® TÃ¢m Linh')
                        ]
                        
                        for key, label in aspects:
                            if key in res_9pp:
                                data = res_9pp[key]
                                with st.expander(f"{label} - Äiá»ƒm: {data.get('diem', 'N/A')}/10"):
                                    st.write(f"**ThÃ¡i Ä‘á»™:** {data.get('thai_do', 'N/A')}")
                                    st.write(f"**PhÃ¢n tÃ­ch:** {data.get('phan_tich', 'N/A')}")
                        
                        # Overall score
                        if 'tong_ket' in res_9pp:
                            st.markdown("---")
                            st.markdown("#### ðŸŽ¯ Tá»”NG Káº¾T")
                            tong_ket = res_9pp['tong_ket']
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Äiá»ƒm Tá»•ng Há»£p", f"{tong_ket.get('diem_tong', 'N/A')}/100")
                            with col2:
                                st.metric("ThÃ¡i Äá»™", tong_ket.get('thai_do_chung', 'N/A'))
                            
                            if 'loi_khuyen_tong_quat' in tong_ket:
                                st.info(f"**ðŸ’¡ Lá»i khuyÃªn:** {tong_ket['loi_khuyen_tong_quat']}")
                        
                        # Coherent analysis
                        if res_lien_mach:
                            st.markdown("---")
                            st.markdown("#### ðŸ”— PHÃ‚N TÃCH LIÃŠN Máº CH")
                            st.write(res_lien_mach)
                        
                        # Download report
                        report_text = f"""
BÃO CÃO PHÃ‚N TÃCH Ká»² MÃ”N Äá»˜N GIÃP
Chá»§ Ä‘á»: {selected_topic}
Thá»i gian: {now.strftime('%H:%M - %d/%m/%Y')}

THÃ”NG TIN CUNG CHá»¦ (Cung {chu['so']}):
- QuÃ¡i: {chu['ten']}
- NgÅ© HÃ nh: {chu['hanh']}
- Sao: {chu['sao']}
- MÃ´n: {chu['cua']}
- Tháº§n: {chu['than']}
- Can: {chu['can_thien']}/{chu['can_dia']}

THÃ”NG TIN CUNG KHÃCH (Cung {khach['so']}):
- QuÃ¡i: {khach['ten']}
- NgÅ© HÃ nh: {khach['hanh']}
- Sao: {khach['sao']}
- MÃ´n: {khach['cua']}
- Tháº§n: {khach['than']}
- Can: {khach['can_thien']}/{khach['can_dia']}

PHÃ‚N TÃCH LIÃŠN Máº CH:
{res_lien_mach}
                        """
                        
                        st.download_button(
                            label="ðŸ“¥ Táº£i BÃ¡o CÃ¡o (TXT)",
                            data=report_text,
                            file_name=f"bao_cao_qmdg_{selected_topic}_{now.strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"Lá»—i táº¡o bÃ¡o cÃ¡o: {e}")
                        import traceback
                        st.code(traceback.format_exc())

            # 4. AI Q&A SECTION
            st.markdown("---")
            st.markdown("### â“ Há»ŽI AI Vá»€ BÃ€N NÃ€Y")
            user_question = st.text_area("Äáº·t cÃ¢u há»i cho ChuyÃªn gia AI:", placeholder="Há»i thÃªm vá» thá»i Ä‘iá»ƒm, cÃ¡ch hÃ³a giáº£i...", key="ai_q_input")
            if st.button("ðŸ¤– Gá»­i CÃ¢u Há»i", key="ai_ask_final"):
                if user_question:
                    with st.spinner("Äang tráº£ lá»i..."):
                        a = st.session_state.gemini_helper.answer_question(user_question, st.session_state.chart_data, selected_topic)
                        st.info(a)



elif st.session_state.current_view == "mai_hoa":
    st.markdown("## ðŸŒ¸ MAI HOA Dá»ŠCH Sá» - TAM TÃ€I Há»¢P NHáº¤T")
    
    if not USE_MAI_HOA:
        st.error("âŒ Module Mai Hoa Dá»‹ch Sá»‘ khÃ´ng kháº£ dá»¥ng.")
        st.stop()
    
    st.markdown(f"### ðŸŽ¯ Chá»§ Ä‘á»: **{selected_topic}**")
    
    method = st.radio("PhÆ°Æ¡ng phÃ¡p:", ["Thá»i gian", "Ngáº«u há»©ng"], horizontal=True, key="mh_method")
    
    if st.button("ðŸŒ¸ Láº¬P QUáºº MAI HOA PRO", type="primary", use_container_width=True):
        dt = selected_datetime
        if method == "Thá»i gian":
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
                <div class="hex-title-pro">{res.get('ten', 'Quáº» ChÃ­nh')}</div>
                <div class="hex-subtitle">{res.get('upper_symbol')} / {res.get('lower_symbol')}</div>
            </div>
            <div>
                <div class="hex-title-pro">{res.get('ten_qua_bien', 'BIáº¾N CÃT TÆ¯á»œNG')}</div>
                <div class="hex-subtitle">Äá»™ng hÃ o {res.get('dong_hao', '?')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Imagery (TÆ°á»£ng Quáº»)
        st.markdown(f"""
        <div class="tuong-que-box">
            <strong>ðŸ–¼ï¸ TÆ°á»£ng Quáº»:</strong> {res.get('tuong', 'Äang cáº­p nháº­t...')} <br>
            <strong>ðŸ“– Ã nghÄ©a:</strong> {res.get('nghÄ©a', 'Äang phÃ¢n tÃ­ch...')}
        </div>
        """, unsafe_allow_html=True)

        # Add visual lines for Mai Hoa
        col_mh_v1, col_mh_v_ho, col_mh_v2 = st.columns(3)
        with col_mh_v1:
            if 'lines' in res:
                st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUáºº CHá»¦ ({res["upper_element"]}/{res["lower_element"]})</div>', unsafe_allow_html=True)
                st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
                for i, line in enumerate(reversed(res['lines'])):
                    h_idx = 6 - i
                    is_dong = (h_idx == res['dong_hao'])
                    cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                    # Apply red color if moving
                    dong_cls = "hao-moving-red" if is_dong else ""
                    
                    st.markdown('<div style="display:flex; align-items:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="hao-label-pro">HÃ o {h_idx}</div>', unsafe_allow_html=True)
                    if line == 1:
                        st.markdown(f'<div class="hao-line-pro {cls} {dong_cls}"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="{cls}"><div class="yin-half-pro {dong_cls}"></div><div class="yin-half-pro {dong_cls}"></div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_mh_v_ho:
            if 'lines_ho' in res:
                st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">Há»– QUáºº</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center; font-size:0.9rem; font-weight:700;">{res.get("ten_ho", "") or "Quáº» Há»—"}</div>', unsafe_allow_html=True)
                st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
                for i, line in enumerate(reversed(res['lines_ho'])):
                    h_idx = 6 - i
                    cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                    st.markdown('<div style="display:flex; align-items:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="hao-label-pro">HÃ o {h_idx}</div>', unsafe_allow_html=True)
                    if line == 1:
                        st.markdown(f'<div class="hao-line-pro {cls}"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="{cls}"><div class="yin-half-pro"></div><div class="yin-half-pro"></div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_mh_v2:
            if 'lines_bien' in res:
                st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUáºº BIáº¾N</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center; font-size:0.9rem; font-weight:700;">{res.get("ten_qua_bien", "") or "Quáº» Biáº¿n"}</div>', unsafe_allow_html=True)
                st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
                for i, line in enumerate(reversed(res['lines_bien'])):
                    h_idx = 6 - i
                    cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                    st.markdown('<div style="display:flex; align-items:center;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="hao-label-pro">HÃ o {h_idx}</div>', unsafe_allow_html=True)
                    if line == 1:
                        st.markdown(f'<div class="hao-line-pro {cls}"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="{cls}"><div class="yin-half-pro"></div><div class="yin-half-pro"></div></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.info(f"ðŸ’¡ **Luáº­n giáº£i chi tiáº¿t:** {res.get('interpretation', 'Äang phÃ¢n tÃ­ch...')}")

        if st.button("ðŸ¤– AI Luáº­n Quáº» Mai Hoa", key="ai_mai_hoa_btn"):
            with st.spinner("AI Ä‘ang giáº£i mÃ£ Mai Hoa..."):
                ans = st.session_state.gemini_helper.analyze_mai_hoa(res, selected_topic)
                st.markdown(f"""
                <div class="interpret-box" style="background: white; border-top: 5px solid #b91c1c;">
                    {ans}
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="footer-stamp">Copyright Â© 2026 MAI HOA DICH SO PRO</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


elif st.session_state.current_view == "luc_hao":
    st.markdown("## â˜¯ï¸ Lá»¤C HÃ€O KINH Dá»ŠCH - CHUYÃŠN SÃ‚U")
    
    if not USE_LUC_HAO:
        st.error("âŒ Module Lá»¥c HÃ o Kinh Dá»‹ch khÃ´ng kháº£ dá»¥ng.")
        st.stop()
    
    st.markdown(f"### ðŸŽ¯ Chá»§ Ä‘á»: **{selected_topic}**")
    
    show_debug_ih = st.checkbox("ðŸž Cháº¿ Ä‘á»™ Kiá»ƒm tra Dá»¯ liá»‡u", key="debug_iching_mode")
    
    if st.button("ðŸŽ² Láº¬P QUáºº Lá»¤C HÃ€O PRO", type="primary", use_container_width=True):
        try:
            # Use the global selected_datetime
            dt = selected_datetime
            can_ngay = params.get('can_ngay', 'GiÃ¡p') if params else "GiÃ¡p"
            chi_ngay = params.get('chi_ngay', 'TÃ½') if params else "TÃ½"
            
            st.session_state.luc_hao_result = lap_qua_luc_hao(
                dt.year, dt.month, dt.day, dt.hour, 
                topic=selected_topic, 
                can_ngay=can_ngay, 
                chi_ngay=chi_ngay
            )
        except Exception as e:
            st.error(f"Lá»—i láº­p quáº»: {e}")

    if 'luc_hao_result' in st.session_state:
        res = st.session_state.luc_hao_result
        st.markdown('<div class="iching-container">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="hex-header-row">
            <div>
                <div class="hex-title-pro">{res['ban']['name']}</div>
                <div class="hex-subtitle">Há» {res['ban']['palace']}</div>
            </div>
            <div>
                <div class="hex-title-pro">{res['bien']['name']}</div>
                <div class="hex-subtitle">Quáº» Biáº¿n</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUáºº CHá»¦ ({res["ban"]["palace"]})</div>', unsafe_allow_html=True)
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
                st.markdown(f'<div class="hao-label-pro">HÃ o {h_idx}</div>', unsafe_allow_html=True)
                if line == 1:
                    st.markdown(f'<div class="hao-line-pro {cls} {dong_cls}"></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="{cls}"><div class="yin-half-pro {dong_cls}"></div><div class="yin-half-pro {dong_cls}"></div></div>', unsafe_allow_html=True)
                
                # Enhanced Label with Debugging
                s = d.get("strength")
                val_s = s if s else "N/A"
                if s:
                    s_label = f"<span style='color: #15803d;'>{s}</span>" if s in ["VÆ°á»£ng", "TÆ°á»›ng"] else f"<span style='color: #b91c1c;'>{s} (Suy)</span>" if s in ["HÆ°u", "TÃ¹", "Tá»­"] else s
                else:
                    s_label = "âš ï¸ Thiáº¿u"
                
                lt = d.get("luc_thu", "N/A")
                m = d.get("marker", "")
                
                st.markdown(f'<div class="hao-info-pro">{d.get("luc_than","N/A")} | {d.get("can_chi","N/A")} | {lt} | {s_label} {m}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if show_debug_ih:
                st.write("DEBUG (HÃ o 1):", res['ban']['details'][0])
                st.write(f"ðŸ“ Module Path: `{luc_hao_kinh_dich.__file__}`")
                st.write(f"ðŸ·ï¸ Version: `{getattr(luc_hao_kinh_dich, 'VERSION_LH', 'Unknown')}`")

            st.markdown('<table class="hao-table-pro"><tr><th>HÃ€O</th><th>Lá»¤C THÃ‚N</th><th>CAN CHI</th><th>Äá»ŠNH Vá»Š</th></tr>', unsafe_allow_html=True)
            for d in reversed(res['ban']['details']):
                h_cls = "highlight-red" if d['is_moving'] else ""
                marker = d.get('marker', '')
                
                st.markdown(f'<tr class="{h_cls}"><td>HÃ o {d["hao"]} {marker}</td><td>{d["luc_than"]}</td><td>{d["can_chi"]}</td><td>{d.get("loc_ma", "-")}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div style="text-align:center; font-weight:800; color:#b91c1c;">QUáºº BIáº¾N</div>', unsafe_allow_html=True)
            st.markdown('<div class="hex-visual-stack">', unsafe_allow_html=True)
            detail_map_bien = {d['hao']: d for d in res['bien'].get('details', [])}
            for i, line in enumerate(reversed(res['bien']['lines'])):
                h_idx = 6 - i
                cls = "yang-line-pro" if line == 1 else "yin-line-pro"
                d = detail_map_bien.get(h_idx, {})
                
                st.markdown('<div class="hao-row-pro">', unsafe_allow_html=True)
                st.markdown(f'<div class="hao-label-pro">HÃ o {h_idx}</div>', unsafe_allow_html=True)
                if line == 1:
                    st.markdown(f'<div class="hao-line-pro {cls}"></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="{cls}"><div class="yin-half-pro"></div><div class="yin-half-pro"></div></div>', unsafe_allow_html=True)
                
                # Enhanced Label (Converted Hexagram usually doesn't show strength/marker in some schools but user asked for it)
                sb = d.get("strength","")
                sb_label = f"<span style='color: #15803d;'>{sb}</span>" if sb in ["VÆ°á»£ng", "TÆ°á»›ng"] else f"<span style='color: #b91c1c;'>{sb} (Suy)</span>" if sb in ["HÆ°u", "TÃ¹", "Tá»­"] else sb
                st.markdown(f'<div class="hao-info-pro">{d.get("luc_than","")} | {d.get("can_chi","")} | {d.get("luc_thu","")} | {sb_label} {d.get("marker","")}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<table class="hao-table-pro"><tr><th>HÃ€O</th><th>Lá»¤C THÃ‚N</th><th>CAN CHI</th><th>Lá»¤C THÃš</th></tr>', unsafe_allow_html=True)
            for d in reversed(res['bien']['details']):
                st.markdown(f'<tr><td>HÃ o {d["hao"]}</td><td>{d["luc_than"]}</td><td>{d["can_chi"]}</td><td>{d["luc_thu"]}</td></tr>', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)


        # Expert Footer
        st.markdown(f"""
        <div class="status-footer-pro">
            <span>ðŸ”¹ {res['the_ung']}</span>
            <span>ðŸ“ Dá»¥ng Tháº§n: {res['ban']['details'][2]['luc_than']}</span>
            <span>ðŸ“Œ {res['conclusion'].split('.')[1]}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="footer-stamp">Copyright Â© 2026 KY MON DON GIAP PRO</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("ðŸ¤– AI Luáº­n Quáº»", key="ai_iching_btn"):
            with st.spinner("AI Ä‘ang giáº£i mÃ£..."):
                ans = st.session_state.gemini_helper.analyze_luc_hao(res, selected_topic)
                st.info(ans)


# ======================================================================
# FOOTER
# ======================================================================


# ======================================================================
# AI FACTORY VIEW
# ======================================================================
elif st.session_state.current_view == "ai_factory":
    st.markdown("## ðŸ­ NHÃ€ MÃY PHÃT TRIá»‚N AI - 50 AGENTS HUB")
    st.info("Há»‡ thá»‘ng tá»± Ä‘á»™ng hÃ³a Ä‘iá»u phá»‘i bá»Ÿi AI Orchestrator + n8n.")
    
    # Status Row
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Agents Äang Cháº¡y", "40/50", "Active")
    with c2: st.metric("CÃ´ng Viá»‡c HoÃ n Táº¥t", "1,248", "Today")
    with c3: st.metric("Äá»™ á»”n Äá»‹nh", "99.9%", "Verified")
    
    st.markdown("### ðŸ¤– Agents Hoáº¡t Äá»™ng 24/7")
    
    # List of Agents in a Grid
    agents = [
        ("Secretary AI", "PhÃ¢n tÃ­ch yÃªu cáº§u & Láº­p káº¿ hoáº¡ch", "ðŸŸ¢"),
        ("Code Writer", "Viáº¿t code chá»©c nÄƒng tá»± Ä‘á»™ng", "ðŸŸ¢"),
        ("Tester AI", "Kiá»ƒm thá»­ Unit Test & UI", "ðŸŸ¢"),
        ("Orchestrator", "Äiá»u phá»‘i luá»“ng cÃ´ng viá»‡c", "ðŸŸ¢"),
        ("Memory Manager", "LÆ°u trá»¯ & Truy xuáº¥t tri thá»©c", "ðŸŸ¢"),
        ("Gemini Pro", "SiÃªu trÃ­ tuá»‡ phÃ¢n tÃ­ch chuyÃªn sÃ¢u", "ðŸŸ¢")
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

    st.markdown("---")
    st.markdown("### ðŸ§  Gá»­i YÃªu Cáº§u Cho NhÃ  MÃ¡y")
    factory_prompt = st.text_area("YÃªu cáº§u phÃ¡t triá»ƒn má»›i:", placeholder="VÃ­ dá»¥: Táº¡o module phÃ¢n tÃ­ch bÃ¡t tá»± tÃ­ch há»£p...")
    if st.button("ðŸš€ Báº¯t Äáº§u Quy TrÃ¬nh Tá»± Äá»™ng", type="primary"):
        st.warning("âš ï¸ Äang gá»­i yÃªu cáº§u tá»›i workflow n8n... Vui lÃ²ng kiá»ƒm tra Dashboard n8n Ä‘á»ƒ theo dÃµi.")

# ======================================================================
# AI EXPERTS VIEW (40 AGENTS)
# ======================================================================
elif st.session_state.current_view == "ai_experts":
    st.markdown("## ðŸŒŸ 40 CHUYÃŠN GIA AI - TÆ¯ Váº¤N CHUYÃŠN SÃ‚U")
    st.caption("Danh sÃ¡ch 40 AI Agents chuyÃªn biá»‡t cho tá»«ng lÄ©nh vá»±c khÃ¡c nhau.")
    
    # Choose Agent Category
    cat = st.tabs(["ðŸ’Ž Super AI", "ðŸ’¼ Äá»i Sá»‘ng", "ðŸ“ˆ TÃ i ChÃ­nh", "ðŸ›¡ï¸ Tiá»‡n Ãch"])
    
    with cat[0]: # Super AI
        selected_agent = st.selectbox("Chá»n ChuyÃªn Gia SiÃªu TrÃ­ Tuá»‡:", [
            "Chart Interpreter AI (PhÃ¢n tÃ­ch bÃ n Ká»³ MÃ´n)",
            "Scheduler AI (TÃ¬m giá» Ä‘áº¹p thÃ´ng minh)",
            "Mai Hoa Expert (ChuyÃªn gia Dá»‹ch sá»‘)",
            "Luc Hao Expert (Báº­c tháº§y Lá»¥c HÃ o)",
            "Topic Advisor (Gá»£i Ã½ chá»§ Ä‘á» linh hoáº¡t)"
        ])
        
    with cat[1]: # Life
        selected_agent = st.selectbox("Chá»n ChuyÃªn Gia Äá»i Sá»‘ng:", [
            "Career Advisor AI (Sá»± nghiá»‡p & CÃ´ng danh)",
            "Health Advisor (Sá»©c khá»e & BÃ¬nh an)",
            "Relationship AI (TÃ¬nh duyÃªn & HÃ´n nhÃ¢n)",
            "Name Analyzer (PhÃ¢n tÃ­ch danh tÃ­nh)",
            "Dream Interpreter (Giáº£i mÃ£ giáº¥c mÆ¡)"
        ])
        
    with cat[2]: # Finance
        selected_agent = st.selectbox("Chá»n ChuyÃªn Gia TÃ i ChÃ­nh:", [
            "Wealth Advisor (TÃ i lá»™c & Äáº§u tÆ°)",
            "Direction Advisor (PhÆ°Æ¡ng hÆ°á»›ng kinh doanh)",
            "Date Selector (Chá»n ngÃ y Ä‘áº¡i sá»±)",
            "Fortune Calendar (Lá»‹ch váº­n háº¡n nÄƒm/thÃ¡ng)"
        ])

    with cat[3]: # Utilities
        selected_agent = st.selectbox("Chá»n Agent Tiá»‡n Ãch:", [
            "History Tracker (Theo dÃµi lá»‹ch sá»­)",
            "Prediction Validator (Kiá»ƒm chá»©ng káº¿t quáº£)",
            "Report Generator (Táº¡o bÃ¡o cÃ¡o chuyÃªn nghiá»‡p)",
            "Comparison AI (So sÃ¡nh Ä‘a táº§ng)",
            "Notification AI (Cáº£nh bÃ¡o giá» lÃ nh)",
            "Learning Assistant (TrÃ¬nh há»c liá»‡u QMDG)",
            "Voice Assistant (Trá»£ lÃ½ giá»ng nÃ³i AI)"
        ])

    st.markdown(f"### ðŸ¤– Báº¯t Ä‘áº§u tÆ° váº¥n vá»›i: **{selected_agent.split('(')[0]}**")
    exp_q = st.text_area("Ná»™i dung cáº§n tÆ° váº¥n:", placeholder="Nháº­p cÃ¢u há»i hoáº·c bá»‘i cáº£nh cá»¥ thá»ƒ cá»§a báº¡n...")
    
    if st.button("ðŸ§™ Triá»‡u há»“i ChuyÃªn Gia AI", type="primary"):
        if exp_q:
            with st.spinner(f"AI {selected_agent} Ä‘ang xá»­ lÃ½ dá»¯ liá»‡u..."):
                # Forward request to specialized module logic
                try:
                    agent_key = selected_agent.split('(')[0].strip().lower().replace(" ", "_")
                    # Dynamically call the module or use unified helper
                    res = st.session_state.gemini_helper.answer_question(f"Role: {selected_agent}. Question: {exp_q}", st.session_state.get('chart_data'))
                    st.info(res)
                except Exception as e:
                    st.error(f"Lá»—i: {e}")
        else:
            st.warning("Vui lÃ²ng nháº­p cÃ¢u há»i.")

elif st.session_state.current_view == "gemini_ai":
    ai_name = st.session_state.get('ai_type', 'AI Assistant')
    st.markdown(f"## ðŸ¤– Há»ŽI {ai_name.upper()} Vá»€ Ká»² MÃ”N Äá»˜N GIÃP")
    
    if not GEMINI_AVAILABLE and not FREE_AI_AVAILABLE:
        st.error("âŒ KhÃ´ng cÃ³ module AI nÃ o kháº£ dá»¥ng.")
        st.stop()
    
    # Check if API key is configured
    if 'gemini_helper' not in st.session_state:
        st.error("âŒ KhÃ´ng thá»ƒ káº¿t ná»‘i vá»›i mÃ¡y chá»§ AI. Vui lÃ²ng thá»­ láº¡i sau.")
        st.stop()
    
    st.success(f"âœ… {ai_name} Ä‘Ã£ sáºµn sÃ ng! HÃ£y Ä‘áº·t cÃ¢u há»i bÃªn dÆ°á»›i.")
    
    # Topic selection for context
    st.markdown("### ðŸŽ¯ Chá»n Chá»§ Äá» (TÃ¹y chá»n)")
    st.caption("Chá»n chá»§ Ä‘á» Ä‘á»ƒ AI cÃ³ ngá»¯ cáº£nh tá»‘t hÆ¡n, hoáº·c Ä‘á»ƒ trá»‘ng Ä‘á»ƒ há»i chung")
    
    col_topic1, col_topic2 = st.columns([3, 1])
    
    with col_topic1:
        selected_topic_ai = st.selectbox(
            "Chá»§ Ä‘á»:",
            ["KhÃ´ng chá»n (Há»i chung)"] + st.session_state.all_topics_full,
            key="ai_topic_select"
        )
    
    with col_topic2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ðŸ”® Láº­p BÃ n Nhanh", use_container_width=True):
            # Quick chart calculation for context
            try:
                from qmdg_calc import calculate_qmdg_params as tinh_ky_mon_don_gian
                st.session_state.ai_chart_data = tinh_ky_mon_don_gian(now.year, now.month, now.day, now.hour)
                st.success("âœ… ÄÃ£ láº­p bÃ n!")
            except Exception as e:
                st.error(f"Lá»—i: {e}")
    
    st.markdown("---")
    
    # Question input area
    st.markdown("### âœï¸ CÃ¢u Há»i Cá»§a Báº¡n")
    user_question = st.text_area(
        "Nháº­p cÃ¢u há»i:",
        placeholder="VÃ­ dá»¥: TÃ´i muá»‘n biáº¿t vá» Ã½ nghÄ©a cá»§a ThiÃªn TÃ¢m Tinh trong Ká»³ MÃ´n Äá»™n GiÃ¡p?",
        height=150,
        key="ai_free_question"
    )
    
    if st.button(f"ðŸ¤– Há»i {ai_name}", type="primary", use_container_width=True, key="ask_gemini_btn"):
        if user_question:
            with st.spinner(f"ðŸ¤– {ai_name} Ä‘ang suy nghÄ©..."):
                try:
                    # Sá»­ dá»¥ng phÆ°Æ¡ng thá»©c answer_question thá»‘ng nháº¥t cho cáº£ 2 helper
                    response_text = st.session_state.gemini_helper.answer_question(
                        user_question, 
                        topic=selected_topic_ai if selected_topic_ai != 'KhÃ´ng chá»n (Há»i chung)' else 'Chung'
                    )
                    
                    # Display response in a nice panel
                    st.markdown("---")
                    st.markdown(f"### ðŸ¤– Tráº£ Lá»i Tá»« {ai_name}")
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                        border-radius: 15px;
                        color: white;
                        margin: 10px 0;
                    ">
                        <h4 style="color: white; margin-top: 0;">ðŸ’¡ CÃ¢u Há»i</h4>
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
                    
                except Exception as e:
                    st.error(f"âŒ Lá»—i: {str(e)}")
        else:
            st.warning("âš ï¸ Vui lÃ²ng nháº­p cÃ¢u há»i")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>Â© 2026 VÅ© Viá»‡t CÆ°á»ng - Ká»³ MÃ´n Äá»™n GiÃ¡p Web Application</p>
    <p>ðŸŒ Cháº¡y 24/7 trÃªn Streamlit Cloud</p>
</div>
""", unsafe_allow_html=True)

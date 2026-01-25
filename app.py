import streamlit as st
import sys
import os
import random
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image

# Add dist directory to Python path
dist_path = os.path.join(os.path.dirname(__file__), 'dist')
ai_modules_path = os.path.join(os.path.dirname(__file__), 'ai_modules')
if dist_path not in sys.path:
    sys.path.insert(0, dist_path)
if ai_modules_path not in sys.path:
    sys.path.insert(0, ai_modules_path)

# Import modules from dist directory
try:
    # Các module phân tích nâng cao (Thiết lập là Optional để tránh crash app nếu thiếu file)
    try:
        from qmdg_data import *
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
        print(f"⚠️ AI Factory modules not available: {e}")
    
    try:
        from gemini_helper import GeminiQMDGHelper
        GEMINI_AVAILABLE = True
    except ImportError:
        GEMINI_AVAILABLE = False
        
    # Import Free AI helper as fallback
    try:
        from free_ai_helper import FreeAIHelper
        FREE_AI_AVAILABLE = True
    except ImportError:
        FREE_AI_AVAILABLE = False


    
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
            return "Bình"

    CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    SAO_9 = list(KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["CUU_TINH"].keys())
    THAN_8 = list(KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_THAN"].keys())
    CUA_8 = list(BAT_MON_CO_DINH_DISPLAY.keys())

except ImportError as e:
    st.error(f"❌ Lỗi: Thiếu file dữ liệu hoặc module: {e}")
    st.stop()

# ======================================================================
# STREAMLIT PAGE CONFIG
# ======================================================================
st.set_page_config(
    page_title="🔮 Kỳ Môn Độn Giáp 🔮",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    .ai-response-panel {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        color: #1e293b;
    }

    .palace-3d {
        perspective: 2000px;
        margin-bottom: 25px;
    }
    
    .palace-inner {
        transform-style: preserve-3d;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        border-radius: 20px;
        padding: 2px;
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        background-color: #ffffff;
    }
    
    .palace-inner:hover {
        transform: rotateX(10deg) rotateY(-10deg) translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.2);
        border: 1px solid rgba(0,0,0,0.2);
    }
    
    .palace-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
        padding: 15px;
        border-radius: 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .element-icon-3d {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 15px currentColor);
        margin-bottom: 10px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-10px) scale(1.1); }
    }

    .interpret-box {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.05);
        padding: 24px;
        color: #1e293b;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.02);
    }

    .interpret-title {
        color: #1e3a8a;
        font-weight: 800;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(0,0,0,0.1);
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated-panel {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    /* Dụng Thần info box */
    .dung-than-box {
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)
# Initialize zoom level in session state
if 'zoom_level' not in st.session_state:
    st.session_state.zoom_level = 100  # Default 100%

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
        st.markdown("### 🔐 Xác Thực Truy Cập - Kỳ Môn Độn Giáp")
        st.text_input(
            "Vui lòng nhập mật khẩu để sử dụng:",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.markdown("### 🔐 Xác Thực Truy Cập - Kỳ Môn Độn Giáp")
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
    if st.button("🔍−", key="zoom_out", help="Thu nhỏ (Zoom Out)"):
        st.session_state.zoom_level = max(50, st.session_state.zoom_level - 10)
        st.rerun()

with zoom_col2:
    if st.button(f"{st.session_state.zoom_level}%", key="zoom_reset", help="Đặt lại 100%"):
        st.session_state.zoom_level = 100
        st.rerun()

with zoom_col3:
    if st.button("🔍+", key="zoom_in", help="Phóng to (Zoom In)"):
        st.session_state.zoom_level = min(200, st.session_state.zoom_level + 10)
        st.rerun()

with zoom_col4:
    st.markdown(f"<div style='padding: 8px; color: #666; font-size: 12px;'>Zoom: {st.session_state.zoom_level}%</div>", unsafe_allow_html=True)

# ======================================================================
# INITIALIZE SESSION STATE
# ======================================================================
if 'chu_de_hien_tai' not in st.session_state:
    st.session_state.chu_de_hien_tai = "Tổng Quát"
if 'all_topics_full' not in st.session_state:
    st.session_state.all_topics_full = sorted(list(TOPIC_INTERPRETATIONS.keys()))
if 'current_view' not in st.session_state:
    st.session_state.current_view = "ky_mon"  # ky_mon, mai_hoa, luc_hao

# ======================================================================
# HEADER
# ======================================================================
col_header1, col_header2, col_header3 = st.columns([1, 3, 1])

with col_header1:
    # Try to load avatar image
    img_path = os.path.join(os.path.dirname(__file__), "dist", "tải xuống (1).jpg")
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
        ["🔮 Kỳ Môn Độn Giáp", "🏭 Nhà Máy AI", "📖 Mai Hoa 64 Quẻ", "☯️ Lục Hào Kinh Dịch", "🤖 Hỏi Gemini AI"],
        index=0
    )
    
    if view_option == "🔮 Kỳ Môn Độn Giáp":
        st.session_state.current_view = "ky_mon"
    elif view_option == "📖 Mai Hoa 64 Quẻ":
        st.session_state.current_view = "mai_hoa"
    elif view_option == "🏭 Nhà Máy AI":
        st.session_state.current_view = "ai_factory"
    elif view_option == "☯️ Lục Hào Kinh Dịch":
        st.session_state.current_view = "luc_hao"
    else:  # 🤖 Hỏi Gemini AI
        st.session_state.current_view = "gemini_ai"
    
    
    st.markdown("---")
    
    # Gemini AI Configuration - Auto-load if available
    if 'gemini_helper' not in st.session_state:
        # Load from custom_data.json first
        custom_data = load_custom_data()
        saved_key = custom_data.get("GEMINI_API_KEY")
        
        # Then try Streamlit Secrets
        secret_api_key = st.secrets.get("GEMINI_API_KEY", saved_key)
        
        if secret_api_key and GEMINI_AVAILABLE:
            try:
                st.session_state.gemini_helper = GeminiQMDGHelper(secret_api_key)
                st.session_state.gemini_key = secret_api_key
                st.session_state.ai_type = "Gemini Pro (Tự động)"
            except Exception: pass
        
        # 2. Fallback to Free/Offline if still nothing
        if 'gemini_helper' not in st.session_state and FREE_AI_AVAILABLE:
            st.session_state.gemini_helper = FreeAIHelper()
            st.session_state.ai_type = "Free AI (Offline)"

    # AI Status Display
    ai_status = st.session_state.get('ai_type', 'Chưa sẵn sàng')
    if "Gemini" in ai_status:
        st.success(f"🤖 **{ai_status}**")
        with st.expander("⚙️ Quản lý Gemini"):
            if st.button("🔄 Kiểm tra kết nối", key="test_ai_conn"):
                with st.spinner("Đang thử kết nối..."):
                    success, msg = st.session_state.gemini_helper.test_connection()
                    if success: st.success(msg)
                    else: st.error(msg)
            
            new_key = st.text_input("Thay đổi API Key (Tùy chọn):", type="password", key="new_api_key")
            save_permanently = st.checkbox("Lưu khóa này vĩnh viễn", value=True)
            
            if st.button("Cập nhật Key mới"):
                if new_key:
                    try:
                        st.session_state.gemini_helper = GeminiQMDGHelper(new_key)
                        st.session_state.gemini_key = new_key
                        st.session_state.ai_type = "Gemini Pro (Cá nhân)"
                        
                        if save_permanently:
                            data = load_custom_data()
                            data["GEMINI_API_KEY"] = new_key
                            save_custom_data(data)
                            st.success("✅ Đã cập nhật và Lưu vĩnh viễn!")
                        else:
                            st.success("✅ Đã cập nhật (Tạm thời)!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi: {e}")
                else:
                    st.warning("Vui lòng nhập Key.")
    else:
        st.warning(f"ℹ️ {ai_status}")
        with st.expander("🔑 Kích hoạt Gemini Pro (Thông minh hơn)", expanded=True):
            st.markdown("👉 [Lấy API Key miễn phí](https://aistudio.google.com/app/apikey)")
            user_api_key = st.text_input("Dán API Key vào đây:", type="password", key="input_api_key_sidebar")
            save_key_permanently = st.checkbox("Lưu khóa này vĩnh viễn", value=True, key="save_key_checkbox")
            
            if st.button("Kích hoạt ngay", type="primary"):
                if GEMINI_AVAILABLE and user_api_key:
                    try:
                        st.session_state.gemini_helper = GeminiQMDGHelper(user_api_key)
                        st.session_state.gemini_key = user_api_key
                        st.session_state.ai_type = "Gemini Pro (Active)"
                        
                        if save_key_permanently:
                            data = load_custom_data()
                            data["GEMINI_API_KEY"] = user_api_key
                            save_custom_data(data)
                            st.success("✅ Thành công và Đã Lưu!")
                        else:
                            st.success("✅ Thành công!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi: {e}")
                else:
                    st.error("Vui lòng nhập Key hoặc thiếu thư viện.")

    # n8n Configuration
    with st.expander("🔗 Kết nối n8n (Advanced AI)"):
        n8n_url = st.secrets.get("N8N_WEBHOOK_URL", "")
        n8n_input = st.text_input("n8n Webhook URL:", value=st.session_state.get('n8n_url', n8n_url))
        if n8n_input:
            st.session_state.n8n_url = n8n_input
            if 'gemini_helper' in st.session_state and hasattr(st.session_state.gemini_helper, 'set_n8n_url'):
                st.session_state.gemini_helper.set_n8n_url(n8n_input)
    
    st.markdown("---")
    
    # Time controls (for Ky Mon)
    if st.session_state.current_view == "ky_mon":
        st.markdown("### 🕐 Thời Gian")
        
        use_current_time = st.checkbox("Sử dụng giờ hiện tại", value=True)
        
        if use_current_time:
            # Use Vietnam timezone (UTC+7)
            vn_tz = ZoneInfo("Asia/Ho_Chi_Minh")
            now = datetime.now(vn_tz)
            selected_datetime = now
        else:
            vn_tz = ZoneInfo("Asia/Ho_Chi_Minh")
            now_vn = datetime.now(vn_tz)
            selected_date = st.date_input("Chọn ngày:", now_vn.date())
            selected_time = st.time_input("Chọn giờ:", now_vn.time())
            selected_datetime = datetime.combine(selected_date, selected_time, tzinfo=vn_tz)
        
        # Calculate QMDG parameters
        try:
            try:
                import qmdg_calc
                params = qmdg_calc.calculate_qmdg_params(selected_datetime)
            except ImportError:
                # Fallback calculation if module is missing
                st.warning("⚠️ Module tính toán chưa được tải lên. Sử dụng chế độ rút gọn.")
                params = {
                    'can_gio': 'Giáp', 'chi_gio': 'Tý',
                    'can_ngay': 'Giáp', 'chi_ngay': 'Tý',
                    'can_thang': 'Giáp', 'chi_thang': 'Tý',
                    'can_nam': 'Giáp', 'chi_nam': 'Tý',
                    'cuc': 1, 'is_duong_don': True,
                    'tiet_khi': 'Lập Xuân',
                    'truc_phu': 'Thiên Bồng',
                    'truc_su': 'Hưu Môn'
                }
            
            st.info(f"""
            **Thời gian:** {selected_datetime.strftime("%H:%M - %d/%m/%Y")}
            
            **Âm lịch:**
            - Giờ: {params['can_gio']} {params['chi_gio']}
            - Ngày: {params['can_ngay']} {params['chi_ngay']}
            - Tháng: {params['can_thang']} {params['chi_thang']}
            - Năm: {params['can_nam']} {params['chi_nam']}
            
            **Cục:** {params['cuc']} ({'Dương' if params.get('is_duong_don', True) else 'Âm'} Độn)
            
            **Tiết khí:** {params['tiet_khi']}
            
            **Trực Phù:** {params['truc_phu']}
            
            **Trực Sử:** {params['truc_su']}
            """)
            
        except Exception as e:
            st.error(f"Lỗi tính toán: {e}")
            params = None
    
    st.markdown("---")
    
    # Topic selection
    st.markdown("### 🎯 Chủ Đề Chính")
    
    # Search box
    search_term = st.text_input("🔍 Tìm kiếm chủ đề:", "")
    
    if search_term:
        filtered_topics = [t for t in st.session_state.all_topics_full if search_term.lower() in t.lower()]
    else:
        filtered_topics = st.session_state.all_topics_full
    
    selected_topic = st.selectbox(
        "Chọn chủ đề:",
        filtered_topics,
        index=0 if "Tổng Quát" not in filtered_topics else filtered_topics.index("Tổng Quát")
    )
    
    st.session_state.chu_de_hien_tai = selected_topic
    
    st.info(f"📌 Đã chọn: **{selected_topic}**")
    
    # Multi-layer analysis (if available)
    if USE_MULTI_LAYER_ANALYSIS:
        st.markdown("---")
        st.markdown("### 🎯 Đối Tượng (Lục Thân)")
        
        doi_tuong_options = [
            "🧑 Bản thân",
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
            # Get Can Gio
            map_can_ngay = {"Giáp": 0, "Kỷ": 0, "Ất": 1, "Canh": 1, "Bính": 2, "Tân": 2, 
                            "Đinh": 3, "Nhâm": 3, "Mậu": 4, "Quý": 4}
            idx_start = map_can_ngay.get(params['can_ngay'], 0)
            idx_chi = CAN_CHI_Gio.index(params['chi_gio'])
            can_gio_idx = (idx_start * 2 + idx_chi) % 10
            can_gio = CAN_10[can_gio_idx]
            
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
                'khong_vong': khong_vong,
                'dich_ma': dich_ma,
                'can_gio': can_gio,
                'can_ngay': params['can_ngay'],
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
                        
                        # Check if palace has Dụng Thần
                        topic_data = TOPIC_INTERPRETATIONS.get(selected_topic, {})
                        dung_than_list = topic_data.get("Dụng_Thần", [])
                        has_dung_than = any(dt in [sao, cua, than, can_thien, can_dia] for dt in dung_than_list)
                        
                        # Determine color based on auspiciousness
                        door_data = KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_MON"].get(cua + " Môn", {})
                        cat_hung = door_data.get("Cát_Hung", "Bình")
                        
                        if cat_hung in ["Đại Cát", "Cát"]:
                            bg_color = "#d4edda"  # Light green
                            border_color = "#28a745"
                        elif cat_hung in ["Hung", "Đại Hung"]:
                            bg_color = "#f8d7da"  # Light red
                            border_color = "#dc3545"
                        else:
                            bg_color = "#fff3cd"  # Light yellow
                            border_color = "#ffc107"
                        
                        # Highlight if has Dụng Thần
                        if has_dung_than:
                            border_color = "#007bff"
                            border_width = "3px"
                        else:
                            border_width = "2px"
                        
                        # Special markers
                        markers = []
                        if palace_num in chart['khong_vong']:
                            markers.append("🌑 Không Vong")
                        if palace_num == chart['dich_ma']:
                            markers.append("🐎 Dịch Mã")
                        marker_text = " ".join(markers) if markers else ""
                        
                        # Determine Strength based on month
                        # Simple mapping for display
                        month = selected_datetime.month
                        season_map = {1:"Xuân", 2:"Xuân", 3:"Xuân", 4:"Hạ", 5:"Hạ", 6:"Hạ", 7:"Thu", 8:"Thu", 9:"Thu", 10:"Đông", 11:"Đông", 12:"Đông"}
                        current_season = season_map.get(month, "Xuân")
                        strength = phan_tich_yeu_to_thoi_gian(hanh, current_season) if USE_MULTI_LAYER_ANALYSIS else "Bình"
                        
                        # Element Styles & Backgrounds
                        element_configs = {
                            "Mộc": {"img": "moc.png", "border": "#10b981", "glow": "rgba(16, 185, 129, 0.4)", "icon": "🌿"},
                            "Hỏa": {"img": "hoa.png", "border": "#ef4444", "glow": "rgba(239, 68, 68, 0.4)", "icon": "🔥"},
                            "Thổ": {"img": "tho.png", "border": "#f59e0b", "glow": "rgba(245, 158, 11, 0.4)", "icon": "⛰️"},
                            "Kim": {"img": "kim.png", "border": "#94a3b8", "glow": "rgba(148, 163, 184, 0.4)", "icon": "⚔️"},
                            "Thủy": {"img": "thuy.png", "border": "#3b82f6", "glow": "rgba(59, 130, 246, 0.4)", "icon": "💧"}
                        }.get(hanh, {"img": "tho.png", "border": "#475569", "glow": "rgba(71, 85, 105, 0.4)", "icon": "✨"})

                        # Load Background Image Base64 (Reliable Streamlit Method)
                        bg_path = os.path.join(os.path.dirname(__file__), "web", "static", "img", "elements", element_configs['img'])
                        bg_base64 = get_base64_image(bg_path)
                        
                        if bg_base64:
                            bg_style = f"url('data:image/png;base64,{bg_base64}') center/cover no-repeat"
                        else:
                            # Fallback Gradient
                            gradients = {
                                "Mộc": "linear-gradient(135deg, #064e3b 0%, #10b981 100%)",
                                "Hỏa": "linear-gradient(135deg, #7f1d1d 0%, #ef4444 100%)",
                                "Thổ": "linear-gradient(135deg, #78350f 0%, #f59e0b 100%)",
                                "Kim": "linear-gradient(135deg, #334155 0%, #94a3b8 100%)",
                                "Thủy": "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)"
                            }
                            bg_style = gradients.get(hanh, "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)")

                        strength_color = {
                            "Vượng": "#ef4444", "Tướng": "#f59e0b", "Hưu": "#10b981", "Tù": "#3b82f6", "Tử": "#64748b"
                        }.get(strength, "#475569")

                        # Hexagram Line Visualization
                        palace_lines = [random.randint(0,1) for _ in range(3)]
                        lines_html = "".join([f'<div style="color: {"#f87171" if l == 1 else "#60a5fa"}; font-size: 8px; line-height: 1.1;">{"━━━━━━" if l == 1 else "━━  ━━"}</div>' for l in palace_lines])

                        # Prepare markers HTML
                        marker_html = f'<div style="margin-top: 15px; font-size: 11px; color: #c084fc; font-weight: 900; text-align: center; text-transform: uppercase; letter-spacing: 2px; filter: drop-shadow(0 0 5px rgba(192, 132, 252, 0.5));">✨ {marker_text}</div>' if marker_text else ''

                        # PREMIUM PALACE CARD HTML - DEDENTED FOR STREAMLIT RENDER
                        palace_html = f"""<div class="palace-3d"><div class="palace-inner" style="background: {bg_style}; border: {border_width} solid {element_configs['border']}; min-height: 380px; position: relative; box-shadow: 0 20px 50px rgba(0,0,0,0.1);"><div style="position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.6)); z-index: 0;"></div><div style="position: relative; z-index: 1; padding: 22px; height: 100%; display: flex; flex-direction: column;"><div style="display: flex; justify-content: space-between; align-items: flex-start;"><div><div style="font-weight: 900; font-size: 32px; color: #1e293b; line-height: 1; text-shadow: 0 0 10px rgba(255,255,255,0.8);">{palace_num}</div><div style="font-size: 15px; font-weight: 800; color: {element_configs['border']}; margin-top: 4px; letter-spacing: 1px;">{QUAI_TUONG.get(palace_num, '')}</div></div><div style="text-align: right;"><div style="background: {strength_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 900; text-transform: uppercase;">{strength}</div><div class="element-icon-3d" style="margin-top: 10px;">{element_configs['icon']}</div></div></div><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px;"><div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(4px); padding: 10px; border-radius: 12px; text-align: center; border: 1px solid rgba(0,0,0,0.05);"><div style="font-size: 9px; color: #64748b; font-weight: 800; letter-spacing: 1px; margin-bottom: 4px;">TINH</div><div style="font-size: 18px; font-weight: 900; color: #1e293b;">{sao}</div></div><div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(4px); padding: 10px; border-radius: 12px; text-align: center; border: 1px solid rgba(0,0,0,0.05);"><div style="font-size: 9px; color: #64748b; font-weight: 800; letter-spacing: 1px; margin-bottom: 4px;">MÔN</div><div style="font-size: 18px; font-weight: 900; color: #1e293b;">{cua}</div></div><div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(4px); padding: 10px; border-radius: 12px; text-align: center; border: 1px solid rgba(0,0,0,0.05);"><div style="font-size: 9px; color: #64748b; font-weight: 800; letter-spacing: 1px; margin-bottom: 4px;">THẦN</div><div style="font-size: 18px; font-weight: 900; color: #1e293b;">{than}</div></div><div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(4px); padding: 10px; border-radius: 12px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 1px solid rgba(0,0,0,0.05);"><div style="font-size: 9px; color: #64748b; font-weight: 800; margin-bottom: 4px;">QUÁI</div><div style="margin-top: 2px;">{lines_html}</div></div></div><div style="margin-top: auto; padding-top: 15px;"><div style="background: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); display: flex; justify-content: space-between;"><div><div style="font-size: 9px; font-weight: 800; color: #64748b; margin-bottom: 2px;">THIÊN</div><div style="font-size: 22px; font-weight: 900; color: #b45309; line-height: 1;">{can_thien}</div></div><div style="text-align: right;"><div style="font-size: 9px; font-weight: 800; color: #64748b; margin-bottom: 2px;">ĐỊA</div><div style="font-size: 22px; font-weight: 900; color: #475569; line-height: 1;">{can_dia}</div></div></div>{marker_html}</div></div></div></div>"""
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
                            
                            # Advanced Matching Logic
                            found_dt = []
                            actual_can_gio = chart.get('can_gio', 'N/A')
                            actual_can_ngay = chart.get('can_ngay', 'N/A')
                            actual_can_thang = chart.get('can_thang', 'N/A')
                            actual_can_nam = chart.get('can_nam', 'N/A')
                            
                            # Resolve Relation (Lục Thân) stem
                            rel_type = st.session_state.get('selected_doi_tuong', "🧑 Bản thân")
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
                        
                        rel_type = st.session_state.get('selected_doi_tuong', "🧑 Bản thân")
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
                                    with st.spinner("🤖 AI đang phân tích..."):
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
                        with st.spinner("🤖 AI đang thực hiện luận giải trọng tâm..."):
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
                                rel_type = st.session_state.get('selected_doi_tuong', "🧑 Bản thân")
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
                                
                                analysis = st.session_state.gemini_helper.comprehensive_analysis(
                                    st.session_state.chart_data,
                                    selected_topic,
                                    enriched_dung_than,
                                    topic_hints,
                                    subj_stem=subj_stem,
                                    obj_stem=obj_stem,
                                    subj_label=role_label
                                )
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
                        with st.spinner("AI đang so sánh..."):
                            p = f"So sánh chi tiết Cung {chu_idx} và Cung {khach_idx} cho {selected_topic}."
                            ans = st.session_state.gemini_helper.answer_question(p)
                            st.info(ans)
                except Exception as e:
                    st.error(f"Lỗi: {e}")

            # 3. DETAILED TECHNICAL REPORT (Existing multi-layer analysis)
            st.markdown("---")
            with st.expander("🔍 Xem Phân Tích Kỹ Thuật (Kỳ Môn + Mai Hoa + Lục Hào)"):
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
                        
                        chu = get_p_info(chu_idx); khach = get_p_info(khach_idx); now = datetime.now()
                        from super_detailed_analysis import phan_tich_sieu_chi_tiet_chu_de, tao_phan_tich_lien_mach
                        res_9pp = phan_tich_sieu_chi_tiet_chu_de(selected_topic, chu, khach, now)
                        mqh = tinh_ngu_hanh_sinh_khac(chu['hanh'], khach['hanh'])
                        res_lien_mach = tao_phan_tich_lien_mach(selected_topic, chu, khach, now, res_9pp, mqh)
                        
                        st.success("✅ Đã tạo báo cáo tổng hợp!")
                        
                        # Display 9 aspects analysis
                        st.markdown("#### 📊 PHÂN TÍCH 9 PHƯƠNG DIỆN")
                        
                        aspects = [
                            ('thai_at', '⚖️ Thái Ất'),
                            ('thanh_cong', '🎯 Thành Công'),
                            ('tai_loc', '💰 Tài Lộc'),
                            ('quan_he', '🤝 Quan Hệ'),
                            ('suc_khoe', '❤️ Sức Khỏe'),
                            ('tranh_chap', '⚔️ Tranh Chấp'),
                            ('di_chuyen', '🚗 Di Chuyển'),
                            ('hoc_van', '📚 Học Vấn'),
                            ('tam_linh', '🔮 Tâm Linh')
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
                            st.markdown("#### 🔗 PHÂN TÍCH LIÊN MẠCH")
                            st.write(res_lien_mach)
                        
                        # Download report
                        report_text = f"""
BÁO CÁO PHÂN TÍCH KỲ MÔN ĐỘN GIÁP
Chủ đề: {selected_topic}
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
                            label="📥 Tải Báo Cáo (TXT)",
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
                    with st.spinner("Đang trả lời..."):
                        a = st.session_state.gemini_helper.answer_question(user_question, st.session_state.chart_data, selected_topic)
                        st.info(a)



elif st.session_state.current_view == "mai_hoa":
    st.markdown("## 📖 MAI HOA DỊCH SỐ - 64 QUẺ KINH DỊCH")
    
    if not USE_MAI_HOA:
        st.error("❌ Module Mai Hoa Dịch Số không khả dụng. Vui lòng kiểm tra file mai_hoa_dich_so.py trong thư mục dist.")
        st.stop()
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")
    st.caption("Mai Hoa Dịch Số sẽ phân tích theo chủ đề đã chọn")
    
    st.markdown("### Chọn phương pháp tính quẻ:")
    
    method = st.radio("", ["Theo thời gian", "Ngẫu nhiên"], key="mai_hoa_method")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        btn_time = st.button("🎲 Lập Quẻ Theo Thời Gian", use_container_width=True) if method == "Theo thời gian" else False
    
    with col_btn2:
        btn_random = st.button("🎲 Lập Quẻ Ngẫu Nhiên", use_container_width=True) if method == "Ngẫu nhiên" else False
    
    if btn_time or btn_random:
        try:
            now = datetime.now()
            
            if btn_time:
                qua_result = tinh_qua_theo_thoi_gian(now.year, now.month, now.day, now.hour)
            else:
                qua_result = tinh_qua_ngau_nhien()
            
            # Get interpretation for selected topic
            giai_qua_result = giai_qua(qua_result, selected_topic)
            qua_result['interpretation'] = giai_qua_result
            
            # Store in session state
            st.session_state.mai_hoa_result = qua_result
            
        except Exception as e:
            st.error(f"Lỗi lập quẻ: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    # Display results if available
    if 'mai_hoa_result' in st.session_state:
        qua_result = st.session_state.mai_hoa_result
        
        st.success("✅ Đã lập quẻ thành công!")
        
        # Display hexagrams visually
        st.markdown("### 📊 Quẻ Tượng")
        
        col_ban, col_ho, col_bien = st.columns(3)
        
        # Helper function to display hexagram
        def display_hexagram(qua_name, title, column):
            with column:
                st.markdown(f"**{title}**")
                st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: #2c3e50;'>{qua_name}</div>", unsafe_allow_html=True)
                
                # Display trigrams (simplified)
                st.markdown("<div style='text-align: center; font-size: 14px; color: #7f8c8d;'>☰☷☲☳☴☵☶☱</div>", unsafe_allow_html=True)
        
        if 'ban_qua' in qua_result:
            display_hexagram(qua_result['ban_qua'], "🎯 Bản Quẻ", col_ban)
        
        if 'ho_qua' in qua_result:
            display_hexagram(qua_result['ho_qua'], "🤝 Hỗ Quẻ", col_ho)
        
        if 'bien_qua' in qua_result:
            display_hexagram(qua_result['bien_qua'], "🔄 Biến Quẻ", col_bien)
        
        # Display detailed information
        st.markdown("---")
        st.markdown("### 📋 Thông Tin Chi Tiết")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            if 'thuong_qua' in qua_result:
                st.info(f"**Thượng Quái:** {qua_result['thuong_qua']}")
            if 'ha_qua' in qua_result:
                st.info(f"**Hạ Quái:** {qua_result['ha_qua']}")
        
        with info_col2:
            if 'dong_hao' in qua_result:
                st.warning(f"**Động Hào:** {qua_result['dong_hao']}")
            if 'ngu_hanh' in qua_result:
                st.success(f"**Ngũ Hành:** {qua_result['ngu_hanh']}")
        
        # Display interpretation
        st.markdown("---")
        st.markdown(f"### 📜 Giải Quẻ Theo Chủ Đề: **{selected_topic}**")
        
        if 'interpretation' in qua_result:
            st.markdown(qua_result['interpretation'])
        else:
            st.write("Chưa có giải quẻ chi tiết.")
        
        # Display raw data in expander
        with st.expander("🔍 Xem Dữ Liệu Thô"):
            st.json(qua_result)


elif st.session_state.current_view == "luc_hao":
    st.markdown("## ☯️ LỤC HÀO KINH DỊCH")
    
    if not USE_LUC_HAO:
        st.error("❌ Module Lục Hào Kinh Dịch không khả dụng. Vui lòng kiểm tra file luc_hao_kinh_dich.py trong thư mục dist.")
        st.stop()
    
    st.markdown(f"### 🎯 Chủ đề: **{selected_topic}**")
    st.caption("Lục Hào Kinh Dịch sẽ phân tích theo chủ đề đã chọn")
    
    if st.button("🎲 Lập Quẻ Lục Hào", type="primary", use_container_width=False):
        try:
            now = datetime.now()
            luc_hao_result = lap_qua_luc_hao(now.year, now.month, now.day, now.hour, selected_topic)
            
            # Store in session state
            st.session_state.luc_hao_result = luc_hao_result
            
        except Exception as e:
            st.error(f"Lỗi lập quẻ: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    # Display results if available
    if 'luc_hao_result' in st.session_state:
        luc_hao_result = st.session_state.luc_hao_result
        
        st.success("✅ Đã lập quẻ thành công!")
        
        # Display hexagram visually
        st.markdown("### 📊 Quẻ Tượng")
        
        col_ban, col_bien = st.columns(2)
        
        with col_ban:
            st.markdown("<div style='text-align: center; margin-bottom: 20px;'><strong>🎯 Bản Quẻ</strong></div>", unsafe_allow_html=True)
            if 'ban_qua_ten' in luc_hao_result:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 15px;'>{luc_hao_result['ban_qua_ten']}</div>", unsafe_allow_html=True)
            
            # Premium 6-line display
            if 'ban_qua_lines' in luc_hao_result:
                lines = luc_hao_result['ban_qua_lines']
                details = luc_hao_result.get('phan_tich_tung_hao', [])
                
                for i in range(6):
                    line = lines[i]
                    detail = details[i] if i < len(details) else {}
                    
                    line_html = "━━━━━━" if line == 1 else "━━  ━━"
                    line_color = "#ef4444" if line == 1 else "#3b82f6" # Red for Yang, Blue for Yin
                    
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 8px;">
                        <div style="font-size: 11px; font-weight: 700; color: #64748b; width: 60px; text-align: right;">{detail.get('luc_thu', '')}</div>
                        <div style="font-size: 18px; font-weight: 900; color: {line_color}; letter-spacing: -2px;">{line_html}</div>
                        <div style="font-size: 11px; font-weight: 700; color: #1e293b; width: 60px; text-align: left;">{detail.get('luc_than', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with col_bien:
            st.markdown("<div style='text-align: center; margin-bottom: 20px;'><strong>🔄 Biến Quẻ</strong></div>", unsafe_allow_html=True)
            if 'bien_qua_ten' in luc_hao_result:
                st.markdown(f"<div style='text-align: center; font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 15px;'>{luc_hao_result['bien_qua_ten']}</div>", unsafe_allow_html=True)
            
            if 'bien_qua_lines' in luc_hao_result:
                lines_bien = luc_hao_result['bien_qua_lines']
                for i, line in enumerate(lines_bien):
                    line_html = "━━━━━━" if line == 1 else "━━  ━━"
                    line_color = "#ef4444" if line == 1 else "#3b82f6"
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 8px;">
                        <div style="font-size: 18px; font-weight: 900; color: {line_color}; letter-spacing: -2px;">{line_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Display detailed information
        st.markdown("---")
        st.markdown("### 📋 Thông Tin Chi Tiết")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'the_ung' in luc_hao_result:
                st.info(f"**Thế Ứng:** {luc_hao_result['the_ung']}")
            if 'dong_hao' in luc_hao_result:
                st.warning(f"**Động Hào:** {luc_hao_result['dong_hao']}")
        
        with col2:
            if 'luc_than' in luc_hao_result:
                st.success(f"**Lục Thân:** {luc_hao_result['luc_than']}")
            if 'luc_thu' in luc_hao_result:
                st.info(f"**Lục Thú:** {luc_hao_result['luc_thu']}")
        
        with col3:
            if 'vuong_suy' in luc_hao_result:
                st.success(f"**Vượng Suy:** {luc_hao_result['vuong_suy']}")
            if 'dong_tinh' in luc_hao_result:
                st.warning(f"**Động Tĩnh:** {luc_hao_result['dong_tinh']}")
        
        # Display interpretation
        st.markdown("---")
        st.markdown(f"### 📜 Giải Quẻ Theo Chủ Đề: **{selected_topic}**")
        
        if 'giai_qua' in luc_hao_result:
            st.markdown(luc_hao_result['giai_qua'])
        elif 'interpretation' in luc_hao_result:
            st.markdown(luc_hao_result['interpretation'])
        else:
            st.write("Chưa có giải quẻ chi tiết.")
        
        # Detailed analysis by lines
        if 'phan_tich_tung_hao' in luc_hao_result:
            with st.expander("🔍 Phân Tích Từng Hào"):
                for hao_info in luc_hao_result['phan_tich_tung_hao']:
                    st.markdown(f"**{hao_info.get('ten', 'N/A')}:** {hao_info.get('y_nghia', 'N/A')}")
        
        # Display raw data in expander
        with st.expander("🔍 Xem Dữ Liệu Thô"):
            st.json(luc_hao_result)


# ======================================================================
# FOOTER
# ======================================================================

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
        if st.button("🔮 Lập Bàn Nhanh", use_container_width=True):
            # Quick chart calculation for context
            try:
                from datetime import datetime
                now = datetime.now()
                from qmdg_calculator import tinh_ky_mon_don_gian
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
            with st.spinner(f"🤖 {ai_name} đang suy nghĩ..."):
                try:
                    # Sử dụng phương thức answer_question thống nhất cho cả 2 helper
                    response_text = st.session_state.gemini_helper.answer_question(
                        user_question, 
                        topic=selected_topic_ai if selected_topic_ai != 'Không chọn (Hỏi chung)' else 'Chung'
                    )
                    
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

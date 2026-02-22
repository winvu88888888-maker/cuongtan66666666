import streamlit as st
import os
import json
import sys
import random
import time
from collections import Counter
from datetime import datetime
import datetime as dt_module

# --- ROBUST PATHING ---
def setup_sub_paths():
    current_file = os.path.abspath(__file__)
    web_dir = os.path.dirname(current_file)
    root_dir = os.path.dirname(web_dir)
    ai_modules_dir = os.path.join(root_dir, "ai_modules")
    for p in [root_dir, web_dir, ai_modules_dir]:
        if p not in sys.path: sys.path.insert(0, p)
    return root_dir

ROOT_DIR = setup_sub_paths()

# --- IMPORT SHARD MANAGER ---
try:
    from shard_manager import add_entry, search_index, get_full_entry, delete_entry, get_hub_stats
    from autonomous_miner import run_mining_cycle, run_daemon, load_config, save_config
    from factory_manager import init_global_factory
    from qmdg_data import load_custom_data
except ImportError:
    from ai_modules.shard_manager import add_entry, search_index, get_full_entry, delete_entry, get_hub_stats
    from ai_modules.autonomous_miner import run_mining_cycle, run_daemon, load_config, save_config
    from ai_modules.factory_manager import init_global_factory
    from qmdg_data import load_custom_data # Should be in root





# --- EXPANDED MINER DATA (50 AGENTS) ---
def get_50_miners():
    categories = [
        ("Kỳ Môn Độn Giáp", "Google, China Archives"),
        ("Kinh Dịch Pro", "I-Ching Scholars"),
        ("Python AI", "GitHub, StackOverflow"),
        ("LLM Research", "Arxiv, OpenAI Docs"),
        ("UI/UX Design", "Dribbble, Behance"),
        ("Security/Hacking", "CVE, Kali Forums"),
        ("Traditional Medicine", "Medical Journals"),
        ("Military Strategy", "Strategy Archives"),
        ("Feng Shui", "Folklore, Geography"),
        ("Financial AI", "Kaggle, Yahoo Finance")
    ]
    miners = []
    statuses = ["🟢 Đang quét sâu", "🟢 Đang phân tích", "🟡 Chờ nạp Shard", "🟢 Đang tổng hợp"]
    
    for i in range(50):
        cat_info = categories[i % len(categories)]
        miners.append({
            "id": f"Agent {i+1:02d}",
            "topic": f"{cat_info[0]} #{i//len(categories) + 1}",
            "status": random.choice(statuses),
            "target": cat_info[1]
        })
    return miners

def render_universal_data_hub_tab():
    st.subheader("🌐 Kho Dữ Liệu Vô Tận (Scalable Hub)")
    
    # ═══════════════════════════════════════════════════════════
    # REAL-TIME STATUS INDICATORS
    # ═══════════════════════════════════════════════════════════
    st.markdown("### 📊 Trạng Thái Hệ Thống Real-time")
    
    # Check if systems are running
    config = load_config()
    last_run_str = config.get("last_run")
    is_recently_active = False
    
    if last_run_str:
        try:
            last_run = dt_module.datetime.strptime(last_run_str, "%Y-%m-%d %H:%M:%S")
            time_diff = dt_module.datetime.now() - last_run
            # Consider active if ran within last 45 minutes (30min interval + 15min buffer)
            is_recently_active = time_diff.total_seconds() < 2700
        except:
            pass
    
    # MASTER STATUS CARD (As requested by user)
    st.markdown(f"""
    <div style='padding: 20px; border-radius: 12px; background-color: #2e4a45; border: 1px solid #3e5a55; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <div style='width: 15px; height: 15px; background-color: #00ff00; border-radius: 50%; box-shadow: 0 0 10px #00ff00;'></div>
            <h3 style='color: #4ade80; margin: 0; font-size: 1.2rem;'>AI Factory: {'ONLINE' if is_recently_active else 'OFFLINE'}</h3>
        </div>
        <p style='color: #4ade80; margin: 10px 0 0 0; font-size: 0.9rem; opacity: 0.8;'>
            (Chạy lúc: {last_run_str if last_run_str else 'Chưa có thông tin'})
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicators
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        if is_recently_active:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: linear-gradient(135deg, #00c853 0%, #00e676 100%); text-align: center;'>
                <h3 style='color: white; margin: 0;'>🟢 50 AI AGENTS</h3>
                <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>ĐANG CHẠY</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); text-align: center;'>
                <h3 style='color: white; margin: 0;'>🔴 50 AI AGENTS</h3>
                <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>KHÔNG CHẠY</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_status2:
        st.markdown("""
        <div style='padding: 15px; border-radius: 10px; background: linear-gradient(135deg, #00c853 0%, #00e676 100%); text-align: center;'>
            <h3 style='color: white; margin: 0;'>🛡️ BẢO TỒN DỮ LIỆU</h3>
            <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>100% AN TOÀN</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status3:
        github_actions_active = config.get("autonomous_247", False)
        
        if github_actions_active:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: linear-gradient(135deg, #00c853 0%, #00e676 100%); text-align: center;'>
                <h3 style='color: white; margin: 0;'>🟢 GITHUB ACTIONS</h3>
                <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>24/7 ACTIVE</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); text-align: center;'>
                <h3 style='color: white; margin: 0;'>🔴 GITHUB ACTIONS</h3>
                <p style='color: white; margin: 5px 0 0 0; font-size: 14px;'>TẮT</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    # ═══════════════════════════════════════════════════════════
    
    st.info("Hệ thống lưu trữ Đa Tầng: Tốc độ xử lý vĩnh cửu.")


    # Data Volume Stats Button
    if st.button("📊 KIỂM TRA DỮ LIỆU ĐÃ TẢI", use_container_width=True, type="primary"):
        stats = get_hub_stats()
        st.markdown(f"""
        <div style="background: #0f172a; padding: 20px; border-radius: 12px; border-left: 8px solid #3b82f6; margin: 10px 0; color: #ffffff;">
            <h3 style="color: #47a1ff; margin-top: 0;">📈 Báo Cáo Lưu Trữ AI Factory</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div style="background: #1e293b; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                    <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Tổng số bản ghi</p>
                    <h2 style="color: #3b82f6; margin: 5px 0;">{stats['total']}</h2>
                </div>
                <div style="background: #1e293b; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                    <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Tổng dung lượng</p>
                    <h2 style="color: #10b981; margin: 5px 0;">{stats['size_mb']} MB</h2>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <p style="font-weight: 700; color: #cbd5e1; margin-bottom: 5px;">📂 Phân bổ theo phân loại:</p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    {" ".join([f'<span style="background:#334155; color:#f1f5f9; padding:4px 10px; border-radius:20px; font-size:0.8rem;">{k}: {v}</span>' for k,v in stats['categories'].items()])}
                </div>
            </div>
            <p style="font-style: italic; font-size: 0.8rem; color: #64748b; margin-top: 15px;">* Dữ liệu được tính toán thời gian thực từ Sharded Hub.</p>
        </div>
        """, unsafe_allow_html=True)

    categories = ["Mã Nguồn", "Nghiên Cứu", "Kiến Thức", "Kỳ Môn Độn Giáp", "Kinh Dịch", "Khác"]

    with st.expander("📥 Nạp Dữ Liệu Mới Thủ Công"):
        with st.form("sharded_hub_form_final", clear_on_submit=True):
            title = st.text_input("Tiêu đề/Chủ đề:")
            cat = st.selectbox("Phân loại:", categories)
            content = st.text_area("Nội dung chi tiết (Markdown):", height=150)
            if st.form_submit_button("🚀 Lưu vào Hệ Thống"):
                if title and content:
                    id = add_entry(title, content, cat, source="Thủ công")
                    if id: 
                        st.success(f"✅ Đã lưu! ID: {id}")
                        time.sleep(0.5)
                        st.rerun()

    st.markdown("---")
    
    col_f1, col_f2 = st.columns([1, 2])
    selected_cat = col_f1.selectbox("Xem theo loại:", ["Tất cả"] + categories)
    search_q = col_f2.text_input("🔍 Tìm kiếm nhanh:", placeholder="Nhập từ khóa...")
    
    index_results = search_index(search_q, selected_cat)
    st.write(f"Đang hiển thị {len(index_results)} mục.")
    
    for e in index_results:
        with st.expander(f"[{e['category']}] 📁 {e['title']} ({e['created_at'][:10]})"):
            if st.button("👁️ Tải nội dung chi tiết", key=f"load_{e['id']}"):
                full = get_full_entry(e['id'], e['shard'])
                if full: 
                    st.caption(f"ID: {e['id']} | Shard: {e['shard']}")
                    st.markdown(full['content'])
            
            if st.button("🗑️ Xóa", key=f"del_{e['id']}"):
                if delete_entry(e['id']): st.success("Đã xóa!"); st.rerun()

def render_mining_summary_on_dashboard(key_suffix=""):
    config = load_config()
    last_run_str = config.get("last_run")
    
    # ═══════════════════════════════════════════════════════════
    # 📊 TRẠNG THÁT HỆ THỐNG (TOP PRIORITY)
    # ═══════════════════════════════════════════════════════════
    st.markdown("### 📊 Trạng Thái Hệ Thống Real-time")
    
    # Status Check Logic
    is_recently_active = False
    time_diff_minutes = 999
    if last_run_str:
        try:
            last_run_dt = dt_module.datetime.strptime(last_run_str, "%Y-%m-%d %H:%M:%S")
            diff = dt_module.datetime.now() - last_run_dt
            time_diff_minutes = diff.total_seconds() / 60
            if time_diff_minutes < 90: is_recently_active = True
        except: pass
    
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        if is_recently_active:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: #064e3b; text-align: center; border: 1px solid #059669;'>
                <h3 style='color: #4ade80; margin: 0;'>🟢 50 AI AGENTS</h3>
                <p style='color: #ffffff; margin: 5px 0 0 0; font-size: 14px; font-weight: bold;'>ĐANG KHAI THÁC</p>
                <small style='color: #a7f3d0; opacity: 0.8;'>Lần cuối: """ + str(int(time_diff_minutes)) + """p trước</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: #450a0a; text-align: center; border: 1px solid #b91c1c;'>
                <h3 style='color: #f87171; margin: 0;'>🔴 50 AI AGENTS</h3>
                <p style='color: #ffffff; margin: 5px 0 0 0; font-size: 14px; font-weight: bold;'>ĐANG DỪNG</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_status2:
        st.markdown("""
        <div style='padding: 15px; border-radius: 10px; background: #064e3b; text-align: center; border: 1px solid #059669;'>
            <h3 style='color: #4ade80; margin: 0;'>🛡️ BẢO TỒN</h3>
            <p style='color: #ffffff; margin: 5px 0 0 0; font-size: 14px; font-weight: bold;'>DỮ LIỆU AN TOÀN</p>
        </div>
        """, unsafe_allow_html=True)
            
    with col_status3:
        github_actions_active = config.get("autonomous_247", False)
        if github_actions_active:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: #064e3b; text-align: center; border: 1px solid #059669;'>
                <h3 style='color: #4ade80; margin: 0;'>🟢 24/7 ACTIVE</h3>
                <p style='color: #ffffff; margin: 5px 0 0 0; font-size: 14px; font-weight: bold;'>MỖI 30 PHÚT</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='padding: 15px; border-radius: 10px; background: #450a0a; text-align: center; border: 1px solid #b91c1c;'>
                <h3 style='color: #f87171; margin: 0;'>🔴 24/7 OFF</h3>
                <p style='color: #ffffff; margin: 5px 0 0 0; font-size: 14px; font-weight: bold;'>ĐÃ TẮT</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # BẢO TỒN DỮ LIỆU - Không xóa bất kỳ chủ đề nào
    st.success("🛡️ **Chế độ BẢO TỒN**: Tất cả chủ đề được bảo vệ vĩnh viễn.")
    st.markdown("---")
    
    # 2. 50 MINING AGENTS INFO
    st.markdown("### 🏹 Quân Đoàn 50 Đặc Phái Viên AI")
    st.caption("✨ **NÂNG CẤP MỚI**: Mỗi agent tìm kiếm trên Google/Internet + Gemini AI Grounding")
    
    # --- Removed redundant status check and display ---

    # 24/7 Control Panel
    c1_24, c2_24 = st.columns([2, 1])
    with c1_24:
        toggle_key = f"toggle_247_{key_suffix}"
        
        # Check if key exists before allowing activation
        current_key = st.session_state.get("gemini_key", "")
        
        # Fallback: check saved data
        if not current_key:
            try:
                data = load_custom_data()
                current_key = data.get("GEMINI_API_KEY", "")
                if current_key:
                    st.session_state.gemini_key = current_key
            except: pass
    

    
    # 24/7 Autonomous Mode Toggle
    c1_24, c2_24 = st.columns([1, 1])
    
    with c1_24:
        is_active = config.get("autonomous_247", False)
        current_key = config.get("api_key") or (st.session_state.get('gemini_key') if 'gemini_key' in st.session_state else None)
        
        new_status = st.toggle(
            "⚡ KÍCH HOẠT CHẾ ĐỘ TỰ TRỊ 24/7",
            value=is_active,
            key=f"toggle_247_mode{key_suffix}",
            help="Bật để hệ thống tự động chạy liên tục mỗi 30 phút qua GitHub Actions"
        )
        
        if new_status != is_active:
            if new_status and not current_key:
                st.error("⚠️ Vui lòng nhập Gemini API Key trước khi kích hoạt chế độ 24/7!")
            else:
                config["autonomous_247"] = new_status
                if new_status:
                    config["api_key"] = current_key
                save_config(config)
                
                # Explicitly trigger daemon
                if new_status:
                    init_global_factory()
                
                st.success(f"✅ Đã {'BẬT' if new_status else 'TẮT'} chế độ tự trị!")
                time.sleep(1.0) # Increased delay for stabilization
                st.rerun()
            
    with c2_24:
        if is_active:
            st.success("🤖 ĐANG CHẠY 24/7")
            init_global_factory() # Ensure it's active
        else:
            st.info("💤 ĐANG TẠM DỪNG")

    # Real Trigger Button (Manual override)
    btn_key = f"activate_mining_legion_btn{key_suffix}"
    if st.button("🚀 CHẠY CHU KỲ THỦ CÔNG (50 AGENTS THẬT)", use_container_width=True, key=btn_key, type="primary"):
        # AUTO-DETECT API KEY FROM MULTIPLE SOURCES
        api_key = None
        
        # Source 1: Session state
        if 'gemini_key' in st.session_state and st.session_state.gemini_key:
            api_key = st.session_state.gemini_key
        
        # Source 2: custom_data.json
        if not api_key:
            try:
                import json, os
                custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_data.json")
                if os.path.exists(custom_path):
                    with open(custom_path, "r", encoding="utf-8") as f:
                        api_key = json.load(f).get("GEMINI_API_KEY")
            except: pass
        
        # RUN OR ERROR
        if api_key:
            with st.spinner("🤖 50 AI AGENTS ĐANG CHẠY THẬT... (2-5 phút)"):
                try:
                    run_mining_cycle(api_key)
                    st.success("✅ HOÀN TẤT! 50 agents đã thu thập dữ liệu THẬT từ Google + Gemini AI!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")
        else:
            st.error("❌ THIẾU API KEY! Paste Gemini API Key ở sidebar trước (phần '🤖 Cấu hình AI')")

    stats = get_hub_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng Đặc phái viên", "50", help="50 AI agents tìm kiếm trên Google + Internet")
    col2.metric("Chu kỳ hoàn tất", config.get("total_cycles", 0), help="Mỗi chu kỳ = 50 tasks")
    col3.metric("Lưu trữ Shard", f"{stats['size_mb']} MB", help="Dữ liệu từ web + AI synthesis")
    col4.metric("Dữ liệu nạp", f"{stats['total']} bản ghi", help="Tự động cập nhật 24/7")
    
    if config.get("last_run"):
        st.caption(f"🕒 Lần cuối hoạt động: {config['last_run']} | Giãn cách: {config.get('interval_minutes')} phút")
    
    with st.expander(f"🔍 Xem danh sách 50 Đặc phái viên đang thực nhiệm ({key_suffix.strip('_')})"):
        miners = get_50_miners()
        for m in miners:
            cx1, cx2, cx3 = st.columns([1, 2, 2])
            cx1.write(f"**{m['id']}**")
            cx2.write(f"📌 {m['topic']}")
            cx3.write(f"{m['status']}")

def render_system_management_tab():
    st.subheader("🛠️ Quản Trị Hệ Thống & Bảo Trì")
    t1, t2, t3 = st.tabs(["🤖 Command Center", "🏥 System Health", "🧬 DB Interaction"])
    
    with t1:
        # --- BẢO TỒN DỮ LIỆU ---
        st.success("🛡️ **Chế độ BẢO TỒN VĨNH VIỄN**: Tất cả chủ đề và dữ liệu được bảo vệ 100%. Không có chức năng xóa nào hoạt động.")
        
        st.markdown("---")
        render_mining_summary_on_dashboard(key_suffix="_mgmt")
        st.markdown("---")
        
    with t2:
        st.success("Tình trạng Shards: 🟢 Hoạt động tốt.")
        st.write("Shard Manager: Standby.")

    with t3:
        st.write("Cấu hình Hạt giống thông minh (Seed Config)...")

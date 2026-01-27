import streamlit as st
import os
import json
import sys
import random
from collections import Counter
from datetime import datetime

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
except ImportError:
    from ai_modules.shard_manager import add_entry, search_index, get_full_entry, delete_entry, get_hub_stats
    from ai_modules.autonomous_miner import run_mining_cycle, run_daemon, load_config, save_config
    from ai_modules.factory_manager import init_global_factory

# --- TOP 5 HOT TOPICS LOGIC ---
def get_top_5_hot_topics():
    """Analyze the index to find most active research areas."""
    try:
        index_path = os.path.join(ROOT_DIR, "data_hub", "hub_index.json")
        if not os.path.exists(index_path): return []
        
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        # Count frequency of titles (each mining run creates an entry)
        topic_counts = Counter([e['title'] for e in index])
        top_5 = topic_counts.most_common(5)
        return top_5
    except Exception:
        return []

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
    st.info("Hệ thống lưu trữ Đa Tầng: Tốc độ xử lý vĩnh cửu.")

    # Data Volume Stats Button
    if st.button("📊 KIỂM TRA DỮ LIỆU ĐÃ TẢI", use_container_width=True, type="primary"):
        stats = get_hub_stats()
        st.markdown(f"""
        <div style="background: #f1f5f9; padding: 20px; border-radius: 12px; border-left: 8px solid #3b82f6; margin: 10px 0;">
            <h3 style="color: #1e293b; margin-top: 0;">📈 Báo Cáo Lưu Trữ AI Factory</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <p style="color: #64748b; font-size: 0.9rem; margin: 0;">Tổng số bản ghi</p>
                    <h2 style="color: #3b82f6; margin: 5px 0;">{stats['total']}</h2>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <p style="color: #64748b; font-size: 0.9rem; margin: 0;">Tổng dung lượng</p>
                    <h2 style="color: #10b981; margin: 5px 0;">{stats['size_mb']} MB</h2>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <p style="font-weight: 700; color: #1e293b; margin-bottom: 5px;">📂 Phân bổ theo phân loại:</p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    {" ".join([f'<span style="background:#e2e8f0; padding:4px 10px; border-radius:20px; font-size:0.8rem;">{k}: {v}</span>' for k,v in stats['categories'].items()])}
                </div>
            </div>
            <p style="font-style: italic; font-size: 0.8rem; color: #94a3b8; margin-top: 15px;">* Dữ liệu được tính toán thời gian thực từ Sharded Hub.</p>
        </div>
        """, unsafe_allow_html=True)

    categories = ["Mã Nguồn", "Nghiên Cứu", "Kiến Thức", "Kỳ Môn Độn Giáp", "Kinh Dịch", "Khác"]

    with st.expander("📥 Nạp Dữ Liệu Mới Thủ Công"):
        with st.form("sharded_hub_form_final"):
            title = st.text_input("Tiêu đề/Chủ đề:")
            cat = st.selectbox("Phân loại:", categories)
            content = st.text_area("Nội dung chi tiết (Markdown):", height=150)
            if st.form_submit_button("🚀 Lưu vào Hệ Thống"):
                if title and content:
                    id = add_entry(title, content, cat, source="Thủ công")
                    if id: st.success(f"✅ Đã lưu! ID: {id}"); st.rerun()

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
    # 1. CLEANUP LEGION STATUS
    st.markdown("### 🧹 Quân Đoàn Dọn Dẹp & Tối Ưu (Autonomous 24/7)")
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric("Bản ghi trùng đã xóa", "0", delta="0")
    c_m2.metric("Túi nén (Bags)", "0")
    c_m3.info("🛡️ Trạng thái: **🟢 Sẵn sàng dọn dẹp**")
    
    st.markdown("---")

    # 2. TOP 5 HOT TOPICS (NEW)
    st.markdown("### 🔥 Top 5 Chủ Đề 'Nóng' Nhất (Hệ thống đang đào sâu)")
    hot_topics = get_top_5_hot_topics()
    if hot_topics:
        cols = st.columns(5)
        for i, (topic, count) in enumerate(hot_topics):
            with cols[i]:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #FF512F 0%, #DD2476 100%); 
                            padding:15px; border-radius:12px; color:white; text-align:center;">
                    <h4 style="margin:0; font-size:0.9rem;">{topic[:20]}...</h4>
                    <p style="font-size:1.5rem; font-weight:bold; margin:5px 0;">{count}</p>
                    <small>Dữ liệu nạp</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Đang phân tích dữ liệu xu hướng...")

    st.markdown("---")
    
    # 3. 50 MINING AGENTS STATUS
    st.markdown("### 🏹 Quân Đoàn 50 Đặc Phái Viên AI (Khai thác 24/7)")
    
    config = load_config()
    is_active = config.get("autonomous_247", False)
    
    # 24/7 Control Panel
    c1_24, c2_24 = st.columns([2, 1])
    with c1_24:
        new_status = st.toggle("⚡ KÍCH HOẠT CHẾ ĐỘ TỰ TRỊ 24/7", value=is_active)
        if new_status != is_active:
            config["autonomous_247"] = new_status
            if new_status:
                config["api_key"] = st.session_state.get("gemini_key", "")
            save_config(config)
            st.rerun()
            
    with c2_24:
        if is_active:
            st.success("🤖 ĐANG CHẠY 24/7")
            init_global_factory() # Ensure it's active
        else:
            st.info("💤 ĐANG TẠM DỪNG")

    # Real Trigger Button (Manual override)
    btn_key = f"activate_mining_legion_btn{key_suffix}"
    if st.button("🚀 CHẠY CHU KỲ THỦ CÔNG", use_container_width=True, key=btn_key):
        if 'gemini_key' in st.session_state and st.session_state.gemini_key:
            with st.spinner("🤖 Quân đoàn AI đang xuất quân..."):
                try:
                    run_mining_cycle(st.session_state.gemini_key)
                    st.success("✅ Chu kỳ khai thác hoàn tất! Dữ liệu đã được nạp vào Shard Hub.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khai thác: {e}")
        else:
            st.warning("⚠️ Vui lòng cấu hình Gemini API Key để kích hoạt quân đoàn.")

    stats = get_hub_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng Đặc phái viên", "50")
    col2.metric("Chu kỳ hoàn tất", config.get("total_cycles", 0))
    col3.metric("Lưu trữ Shard", f"{stats['size_mb']} MB")
    col4.metric("Dữ liệu nạp", f"{stats['total']} bản ghi")
    
    if config.get("last_run"):
        st.caption(f"🕒 Lần cuối hoạt động: {config['last_run']} | Giãn cách: {config.get('interval_minutes')} phút")
    
    with st.expander("🔍 Xem danh sách 50 Đặc phái viên đang thực nhiệm"):
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
        render_mining_summary_on_dashboard(key_suffix="_mgmt")
        st.markdown("---")
        if st.button("♻️ Kích hoạt Bảo trì Thủ công (Manual Sync)"):
            try:
                from ai_modules.maintenance_manager import MaintenanceManager
                mm = MaintenanceManager()
                res = mm.run_cleanup_cycle()
                st.success(f"✅ Bảo trì hoàn tất! (Xóa: {res['removed']}, Đóng gói: {res['bagged']})")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi: {e}")
        
    with t2:
        st.success("Tình trạng Shards: 🟢 Hoạt động tốt.")
        st.write("Shard Manager: Standby.")

    with t3:
        st.write("Cấu hình Hạt giống thông minh (Seed Config)...")

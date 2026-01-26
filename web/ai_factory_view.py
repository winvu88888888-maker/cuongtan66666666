import streamlit as st
import sys
import os
import json
import importlib.util
from pathlib import Path
from datetime import datetime

# --- ROBUST PATH INITIALIZATION (STREAMLIT CLOUD COMPATIBLE) ---
def initialize_paths():
    try:
        # Get the absolute path of the current file (ai_factory_view.py)
        current_file = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file)
        root_dir = os.path.dirname(current_dir)
        
        # Add both to sys.path if not present
        for p in [root_dir, current_dir]:
            if p not in sys.path:
                sys.path.insert(0, p)
        
        return root_dir, current_dir
    except Exception as e:
        st.error(f"Path Init Error: {e}")
        return None, None

ROOT_PATH, WEB_PATH = initialize_paths()

# --- DEFINE FALLBACKS FOR TABS ---
def render_universal_data_hub_tab(): st.error("Tab Dữ Liệu lỗi")
def render_system_management_tab(): st.error("Tab Quản Trị lỗi")
def add_to_hub(*args, **kwargs): return False

# --- DYNAMIC IMPORT OF TABS ---
try:
    # Try multiple import styles to handle different server environments
    try:
        from web.ai_factory_tabs import render_universal_data_hub_tab, render_system_management_tab, add_to_hub
    except ImportError:
        try:
            from ai_factory_tabs import render_universal_data_hub_tab, render_system_management_tab, add_to_hub
        except ImportError:
            # Absolute fallback using file path if standard imports fail
            tabs_path = os.path.join(WEB_PATH, "ai_factory_tabs.py")
            if os.path.exists(tabs_path):
                spec = importlib.util.spec_from_file_location("ai_factory_tabs_dynamic", tabs_path)
                tabs_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(tabs_mod)
                render_universal_data_hub_tab = tabs_mod.render_universal_data_hub_tab
                render_system_management_tab = tabs_mod.render_system_management_tab
                add_to_hub = tabs_mod.add_to_hub
            else:
                st.error(f"⚠️ Không tìm thấy file tại: {tabs_path}")
except Exception as e:
    st.error(f"⚠️ Lỗi tải Tab bổ trợ: {e}")

# Import modules from ai_modules
try:
    from ai_modules.orchestrator import AIOrchestrator
    from ai_modules.memory_system import MemorySystem
except ImportError:
    st.error("⚠️ Không thể tải ai_modules")

try:
    try:
        from n8n_integration import N8nClient as N8NClient, setup_n8n_config
    except ImportError:
        import n8n_integration
        from n8n_integration import N8nClient as N8NClient, setup_n8n_config
except ImportError:
    # Fallback if module is named differently or not found
    st.info("ℹ️ Chế độ n8n: Sử dụng giả lập (Local Only)")
    class N8NClient:
        def __init__(self, base_url="http://localhost:5678", api_key=None):
            self.base_url = base_url
            self.api_key = api_key
        def test_connection(self): return False
        def get_workflow_statistics(self): return {'total_workflows': 0, 'active_workflows': 0}
        def get_execution_statistics(self): return {'total_executions': 0, 'successful': 0, 'executions': []}
        def get_workflows(self): return []
    def setup_n8n_config(*args, **kwargs): pass

def render_ai_factory_view():
    """Renders the AI Factory Dashboard within the main application."""
    
    st.markdown("## 🏭 NHÀ MÁY AI - PHÁT TRIỂN TỰ ĐỘNG")
    st.info("Hệ thống tích hợp n8n: Kỳ Môn Độn Giáp định hướng chiến lược & Gemini AI thực thi kỹ thuật.")
    
    # Initialize session state for this view
    if 'orchestrator' not in st.session_state:
        if 'gemini_key' in st.session_state and st.session_state.gemini_key:
            st.session_state.orchestrator = AIOrchestrator(st.session_state.gemini_key)
        else:
            st.session_state.orchestrator = None
            
    if 'memory' not in st.session_state:
        st.session_state.memory = MemorySystem()
        
    if 'n8n_client' not in st.session_state:
        n8n_url = st.secrets.get("N8N_BASE_URL", "http://localhost:5678")
        n8n_key = st.secrets.get("N8N_API_KEY", None)
        st.session_state.n8n_client = N8NClient(n8n_url, n8n_key)

    # Sub-navigation for AI Factory
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Dashboard", 
        "✍️ Tạo Code & Dự Án", 
        "📚 Knowledge Base", 
        "🌐 Kho Dữ Liệu Vô Tận",
        "⚙️ Workflows",
        "🛠️ Quản Trị Hệ Thống"
    ])

    with tab1: render_dashboard_tab()
    with tab2: render_create_code_tab()
    with tab3: render_knowledge_base_tab()
    with tab4: render_universal_data_hub_tab()
    with tab5: render_workflows_tab()
    with tab6: render_system_management_tab()

def render_dashboard_tab():
    st.subheader("Thống Kê Hoạt Động")
    stats = st.session_state.memory.get_statistics()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #667eea;"><h3 style="color: #667eea; margin: 0;">📁 {stats.get("total_code_files", 0)}</h3><p style="margin: 0; color: #666;">File Code</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #764ba2;"><h3 style="color: #764ba2; margin: 0;">📚 {stats.get("total_knowledge", 0)}</h3><p style="margin: 0; color: #666;">Kiến Thức</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71;"><h3 style="color: #2ecc71; margin: 0;">⚡ {stats.get("total_executions", 0)}</h3><p style="margin: 0; color: #666;">Lần Chạy</p></div>', unsafe_allow_html=True)
    with col4:
        success_rate = 0
        if stats.get('total_executions', 0) > 0:
            success = stats.get('executions_by_status', {}).get('success', 0)
            success_rate = int((success / stats['total_executions']) * 100)
        st.markdown(f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #e74c3c;"><h3 style="color: #e74c3c; margin: 0;">✅ {success_rate}%</h3><p style="margin: 0; color: #666;">Thành Công</p></div>', unsafe_allow_html=True)
        
    st.markdown("### 📜 Hoạt Động Gần Đây")
    recent = st.session_state.memory.get_execution_history(limit=5)
    if recent:
        for ex in recent:
            color = "green" if ex['status'] == 'success' else "red"
            st.markdown(f"- <span style='color:{color}'>●</span> **{ex['workflow_name']}** ({ex['created_at']})", unsafe_allow_html=True)
    else: st.info("Chưa có hoạt động.")

def render_create_code_tab():
    st.subheader("Tạo Code & Dự Án Mới")
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Vui lòng nhập Gemini API key ở Sidebar.")
        return

    if 'last_generation_result' not in st.session_state:
        st.session_state.last_generation_result = None

    with st.form("code_generation_form"):
        req = st.text_area("Mô tả phần mềm:", height=150)
        auto = st.checkbox("Tự động thực thi", value=True)
        if st.form_submit_button("🚀 Bắt Đầu"):
            with st.spinner("🤖 Đang vận hành..."):
                try:
                    res = st.session_state.orchestrator.process_request(req, auto_execute=auto)
                    # Auto Archive
                    nm = res.get('plan', {}).get('project_name', 'Untilted')
                    add_to_hub(f"Yêu cầu: {nm}", f"**Yêu cầu:** {req}\n\n**Plan:**\n{json.dumps(res.get('plan',{}), indent=2, ensure_ascii=False)}", "Nghiên Cứu")
                    for f_path in res.get('execution', {}).get('created_files', []):
                        if os.path.exists(f_path):
                            with open(f_path, 'r', encoding='utf-8') as f:
                                add_to_hub(f"Source: {os.path.basename(f_path)} ({nm})", f"```python\n{f.read()}\n```", "Mã Nguồn")
                    st.session_state.last_generation_result = res
                    st.rerun()
                except Exception as e: st.error(f"Lỗi: {e}")

    if st.session_state.last_generation_result:
        res = st.session_state.last_generation_result
        st.success("✅ Hoàn tất! Đã tự động lưu vào Kho Vô Tận.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Files", len(res.get('execution', {}).get('created_files', [])))
        c2.metric("Fixes", res.get('fixes', {}).get('total_fixes', 0))
        c3.metric("Time", f"{res.get('total_time', 0):.2f}s")
        
        if res.get('package') and os.path.exists(res['package']):
            with open(res['package'], "rb") as f:
                st.download_button("📥 Tải (.zip)", f, file_name=os.path.basename(res['package']))
                
        if res.get('execution', {}).get('created_files'):
            st.markdown("### 📁 Files Đã Tạo")
            for f in res['execution']['created_files']:
                if os.path.exists(f):
                    with st.expander(f"📄 {os.path.basename(f)}"):
                        with open(f, 'r', encoding='utf-8') as content: st.code(content.read())

def render_knowledge_base_tab():
    st.subheader("Cơ Sở Tri Thức AI")
    q = st.text_input("🔍 Tìm kiếm:")
    if q:
        items = st.session_state.memory.search_knowledge(q)
        for i in items:
            with st.expander(f"📖 {i['topic']}"): st.markdown(i['content'])
    
    with st.expander("➕ Thêm Kiến Thức Mới"):
        with st.form("add_k"):
            t = st.text_input("Chủ đề:")
            c = st.text_area("Nội dung:")
            if st.form_submit_button("💾 Lưu"):
                st.session_state.memory.store_knowledge(t, c)
                st.success("Đã lưu!")

def render_workflows_tab():
    st.subheader("Quản Lý n8n Workflows")
    client = st.session_state.n8n_client
    if client.test_connection():
        st.success(f"✅ Đã kết nối n8n tại `{client.base_url}`")
        stats = client.get_workflow_statistics()
        st.metric("Workflows", stats['total_workflows'])
        for wf in client.get_workflows():
            st.write(f"- {wf.get('name')}")
    else: st.warning("⚠️ Chưa kết nối n8n Server")

# Helper for dir listing
def show_workflows_in_dir(directory):
    if Path(directory).exists():
        for f in Path(directory).rglob("*.json"):
            with st.expander(f.name): st.json(json.load(open(f, 'r', encoding='utf-8')))

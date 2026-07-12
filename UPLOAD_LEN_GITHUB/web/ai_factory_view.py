import streamlit as st
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# --- SYSTEM PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path: sys.path.insert(0, root_dir)
if current_dir not in sys.path: sys.path.insert(0, current_dir)

# --- IMPORTS ---
try:
    try:
        from web.ai_factory_tabs import render_universal_data_hub_tab, render_system_management_tab, render_mining_summary_on_dashboard
        from ai_modules.shard_manager import add_entry, get_hub_stats
        from ai_modules.factory_manager import init_global_factory
    except ImportError:
        from ai_factory_tabs import render_universal_data_hub_tab, render_system_management_tab, render_mining_summary_on_dashboard
        from shard_manager import add_entry, get_hub_stats
        from factory_manager import init_global_factory
except Exception as e:
    st.error(f"🚨 Lỗi nạp Hệ thống: {e}")
    def render_universal_data_hub_tab(): st.error("Tab Dữ Liệu lỗi")
    def render_system_management_tab(): st.error("Tab Quản Trị lỗi")
    def render_mining_summary_on_dashboard(**kwargs): pass
    def add_entry(*args, **kwargs): return False
    def get_hub_stats(): return {'total': 0, 'size_mb': 0.0}
    def init_global_factory(): return {'status': 'offline'}

# Import modules from ai_modules
try:
    from ai_modules.orchestrator import AIOrchestrator
    from ai_modules.memory_system import MemorySystem
except ImportError:
    # V22.0: Fallback — tránh crash NameError khi module không tồn tại
    class AIOrchestrator:
        def __init__(self, api_key=None):
            self.api_key = api_key
        def process_request(self, req):
            return {'plan': {'project_name': 'N/A'}, 'execution': {'created_files': []}}
    class MemorySystem:
        def __init__(self):
            pass
        def get_statistics(self):
            return {'total_knowledge': 0, 'total_executions': 0, 'executions_by_status': {'success': 0}}
        def search_knowledge(self, q):
            return []

# n8n Integration
try:
    from n8n_integration import N8nClient as N8NClient, setup_n8n_config
except ImportError:
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
    st.markdown("## 🏭 NHÀ MÁY AI - PHÁT TRIỂN TỰ ĐỘNG")
    st.info("Hệ thống tích hợp n8n & Sharded Data Hub: Tự động hóa 24/7.")
    
    # Initialize Global Factory Manager (Persistent 24/7)
    from ai_modules.autonomous_miner import load_config, save_config
    config = load_config()
    
    # AUTO-SYNC: Luôn đồng bộ API key mới nhất vào factory
    _active_key = st.session_state.get("gemini_key", "")
    if not _active_key:
        try:
            _active_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
    if _active_key and _active_key != config.get("api_key", ""):
        config["api_key"] = _active_key
        config["autonomous_247"] = True
        save_config(config)
    
    is_active_247 = config.get("autonomous_247", False)

    if 'global_factory_status' not in st.session_state or st.session_state.get('last_247_state') != is_active_247:
        try:
            # Use cache_resource but pass is_active as argument to force refresh on toggle
            @st.cache_resource
            def start_daemon_resource(active_status):
                return init_global_factory()
            
            st.session_state.global_factory_status = start_daemon_resource(is_active_247)
            st.session_state.last_247_state = is_active_247
        except Exception as e:
            st.error(f"Lỗi khởi động 24/7: {e}")

    if 'orchestrator' not in st.session_state:
        if 'gemini_key' in st.session_state and st.session_state.gemini_key:
            st.session_state.orchestrator = AIOrchestrator(st.session_state.gemini_key)
        else:
            st.session_state.orchestrator = None
            
    if 'memory' not in st.session_state:
        st.session_state.memory = MemorySystem()
        
    if 'n8n_client' not in st.session_state:
        try:
            n8n_url = st.secrets.get("N8N_BASE_URL", "http://localhost:5678")
            n8n_key = st.secrets.get("N8N_API_KEY", None)
        except Exception:
            n8n_url = "http://localhost:5678"
            n8n_key = None
        st.session_state.n8n_client = N8NClient(n8n_url, n8n_key)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Dashboard", "✍️ Tạo Code & Dự Án", "📚 Knowledge Base", 
        "🌐 Kho Dữ Liệu Vô Tận", "⚙️ Workflows", "🛠️ Quản Trị Hệ Thống"
    ])

    with tab1: render_dashboard_tab()
    with tab2: render_create_code_tab()
    with tab3: render_knowledge_base_tab()
    with tab4: render_universal_data_hub_tab()
    with tab5: render_workflows_tab()
    with tab6: render_system_management_tab()

def render_dashboard_tab():
    st.subheader("Thống Kê Hoạt Động (Real-time)")
    stats = st.session_state.memory.get_statistics()
    
    # Merge with Shard Hub Stats
    hub_stats = get_hub_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    s = 'padding:15px;border-radius:10px;border-left:5px solid '
    bg_style = 'background: #1e293b; color: #ffffff;' # Premium dark background
    
    # Show real Shard Hub total
    col1.markdown(f'<div style="{s}#3b82f6;{bg_style}"><h3>📁 {hub_stats.get("total", 0)}</h3><p style="color: #94a3b8; margin:0;">Shards Hub</p></div>', unsafe_allow_html=True)
    col2.markdown(f'<div style="{s}#764ba2;{bg_style}"><h3>📚 {stats.get("total_knowledge", 0)}</h3><p style="color: #94a3b8; margin:0;">Memory DB</p></div>', unsafe_allow_html=True)
    col3.markdown(f'<div style="{s}#2ecc71;{bg_style}"><h3>💾 {hub_stats.get("size_mb", 0.0)} MB</h3><p style="color: #94a3b8; margin:0;">Dung lượng</p></div>', unsafe_allow_html=True)
    
    success = stats.get("executions_by_status", {}).get("success", 0)
    total = max(1, stats.get("total_executions", 0))
    col4.markdown(f'<div style="{s}#e74c3c;{bg_style}"><h3>✅ {int(success/total*100)}%</h3><p style="color: #94a3b8; margin:0;">Hệ thống</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("🛡️ **Chế độ BẢO TỒN**: Tất cả chủ đề được bảo vệ vĩnh viễn. Không có dữ liệu nào bị xóa.")
    st.markdown("---")
    render_mining_summary_on_dashboard(key_suffix="_dash")

def render_create_code_tab():
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Nhập Gemini API key để bắt đầu.")
        return
    if 'last_res' not in st.session_state: st.session_state.last_res = None

    with st.form("gen_form"):
        req = st.text_area("Mô tả phần mềm:", height=100)
        if st.form_submit_button("🚀 Kích Hoạt AI Factory"):
            with st.spinner("🤖 Đang phân tích và viết code..."):
                try:
                    res = st.session_state.orchestrator.process_request(req)
                    nm = res.get('plan',{}).get('project_name','Project')
                    
                    # Store in SCALABLE HUB
                    add_entry(f"Yêu cầu: {nm}", f"Mô tả: {req}\n\nPlan: {json.dumps(res.get('plan',{}), indent=2)}", "Nghiên Cứu", source="AI Architect")
                    for f_p in res.get('execution',{}).get('created_files',[]):
                        if os.path.exists(f_p):
                            with open(f_p,'r',encoding='utf-8') as content:
                                add_entry(f"Source: {os.path.basename(f_p)}", f"```python\n{content.read()}\n```", "Mã Nguồn", source="AI Coder")
                    
                    st.session_state.last_res = res
                    st.rerun()
                except Exception as e: st.error(f"Lỗi: {e}")

    if st.session_state.last_res:
        res = st.session_state.last_res
        st.success("✅ Dự án hoàn tất! Đã lưu trữ Shard và đồng bộ GitHub.")
        if res.get('package') and os.path.exists(res['package']):
            st.download_button("📥 Tải (.zip)", open(res['package'],"rb"), file_name=os.path.basename(res['package']))
        for f_p in res.get('execution',{}).get('created_files',[]):
            if os.path.exists(f_p):
                with st.expander(os.path.basename(f_p)): st.code(open(f_p, 'r', encoding='utf-8').read())

def render_knowledge_base_tab():
    q = st.text_input("🔍 Truy vấn tri thức nhanh:")
    if q:
        for i in st.session_state.memory.search_knowledge(q):
            with st.expander(i['topic']): st.markdown(i['content'])

def render_workflows_tab():
    c = st.session_state.n8n_client
    if c.test_connection(): st.success(f"✅ Đã kết nối n8n tại `{c.base_url}`")
    else: st.warning("⚠️ Chưa kết nối n8n server")

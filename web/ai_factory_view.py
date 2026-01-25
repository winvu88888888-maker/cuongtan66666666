import streamlit as st
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import modules from ai_modules
from ai_modules.orchestrator import AIOrchestrator
from ai_modules.memory_system import MemorySystem
from n8n_integration import N8NClient, setup_n8n_config

def render_ai_factory_view():
    """Renders the AI Factory Dashboard within the main application."""
    
    st.markdown("## 🏭 NHÀ MÁY AI - PHÁT TRIỂN TỰ ĐỘNG")
    st.info("Hệ thống tích hợp n8n: Kỳ Môn Độn Giáp định hướng chiến lược & Gemini AI thực thi kỹ thuật.")
    
    # Initialize session state for this view
    if 'orchestrator' not in st.session_state:
        # Check if we have a key from the main app's sidebar
        if 'gemini_key' in st.session_state and st.session_state.gemini_key:
            st.session_state.orchestrator = AIOrchestrator(st.session_state.gemini_key)
        else:
            st.session_state.orchestrator = None
            
    if 'memory' not in st.session_state:
        st.session_state.memory = MemorySystem()
        
    if 'n8n_client' not in st.session_state:
        st.session_state.n8n_client = N8NClient()

    # Sub-navigation for AI Factory
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "✍️ Tạo Code & Dự Án", "📚 Knowledge Base", "⚙️ Workflows"])

    with tab1:
        render_dashboard_tab()

    with tab2:
        render_create_code_tab()

    with tab3:
        render_knowledge_base_tab()
        
    with tab4:
        render_workflows_tab()

def render_dashboard_tab():
    st.subheader("Thống Kê Hoạt Động")
    
    stats = st.session_state.memory.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #667eea;">
            <h3 style="color: #667eea; margin: 0;">📁 {stats.get('total_code_files', 0)}</h3>
            <p style="margin: 0; color: #666;">File Code</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #764ba2;">
            <h3 style="color: #764ba2; margin: 0;">📚 {stats.get('total_knowledge', 0)}</h3>
            <p style="margin: 0; color: #666;">Kiến Thức</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71;">
            <h3 style="color: #2ecc71; margin: 0;">⚡ {stats.get('total_executions', 0)}</h3>
            <p style="margin: 0; color: #666;">Lần Chạy</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        success_rate = 0
        if stats.get('total_executions', 0) > 0:
            success = stats.get('executions_by_status', {}).get('success', 0)
            success_rate = int((success / stats['total_executions']) * 100)
            
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #e74c3c;">
            <h3 style="color: #e74c3c; margin: 0;">✅ {success_rate}%</h3>
            <p style="margin: 0; color: #666;">Thành Công</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 📜 Hoạt Động Gần Đây")
    recent_executions = st.session_state.memory.get_execution_history(limit=5)
    
    if recent_executions:
        for exec in recent_executions:
            status_color = "green" if exec['status'] == 'success' else "red"
            st.markdown(f"- <span style='color:{status_color}'>●</span> **{exec['workflow_name']}** ({exec['created_at']}) - {exec['execution_time']}ms", unsafe_allow_html=True)
    else:
        st.info("Chưa có hoạt động nào được ghi nhận.")

def render_create_code_tab():
    st.subheader("Tạo Code & Dự Án Mới")
    
    if st.session_state.orchestrator is None:
        st.warning("⚠️ Vui lòng nhập Gemini API key ở thanh bên trái (Sidebar) để sử dụng tính năng này.")
        return

    with st.form("code_generation_form"):
        st.markdown("### 📝 Mô Tả Yêu Cầu")
        
        user_request = st.text_area(
            "Mô tả chi tiết phần mềm bạn muốn tạo:",
            height=150,
            placeholder="Ví dụ: Tạo một ứng dụng quản lý chi tiêu cá nhân bằng Python với giao diện dòng lệnh, lưu dữ liệu vào SQLite..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            auto_execute = st.checkbox("Tự động thực thi quy trình", value=True)
        
        submit = st.form_submit_button("🚀 Bắt Đầu (n8n + AI)")
        
        if submit and user_request:
            with st.spinner("🤖 Nhà máy AI đang vận hành... Phân tích -> Lập kế hoạch -> Viết Code -> Kiểm thử"):
                try:
                    result = st.session_state.orchestrator.process_request(
                        user_request,
                        auto_execute=auto_execute
                    )
                    
                    st.success("✅ Quy trình hoàn tất!")
                    
                    # Display results summary
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Files Created", len(result.get('execution', {}).get('created_files', [])))
                    c2.metric("Errors Fixed", result.get('fixes', {}).get('total_fixes', 0))
                    c3.metric("Total Time", f"{result.get('total_time', 0):.2f}s")
                    
                    # Download button
                    if result.get('package') and os.path.exists(result['package']):
                        with open(result['package'], "rb") as f:
                            st.download_button(
                                "📥 Tải về Project (.zip)", 
                                f, 
                                file_name=os.path.basename(result['package']),
                                mime="application/zip"
                            )
                    
                    # Plan Details
                    with st.expander("📋 Xem Kế Hoạch Chi Tiết"):
                        st.json(result.get('plan', {}))
                        
                    # Files Created
                    if result.get('execution', {}).get('created_files'):
                        st.markdown("### 📁 Files Đã Tạo")
                        for file in result['execution']['created_files']:
                            with st.expander(f"📄 {os.path.basename(file)}"):
                                try:
                                    with open(file, "r", encoding="utf-8") as f:
                                        st.code(f.read())
                                except:
                                    st.warning(f"Không thể đọc file {file}")

                except Exception as e:
                    st.error(f"❌ Lỗi trong quá trình xử lý: {str(e)}")

def render_knowledge_base_tab():
    st.subheader("Cơ Sở Tri Thức AI")
    
    search_query = st.text_input("🔍 Tìm kiếm kiến thức đã lưu:")
    
    if search_query:
        results = st.session_state.memory.search_knowledge(search_query)
        st.markdown(f"**Tìm thấy {len(results)} kết quả:**")
        
        for item in results:
            with st.expander(f"📖 {item['topic']}"):
                st.markdown(item['content'])
                st.caption(f"Nguồn: {item['source']} | Danh mục: {item['category']}")
    
    st.markdown("---")
    with st.expander("➕ Thêm Kiến Thức Mới Thụ Động"):
        with st.form("add_knowledge"):
            topic = st.text_input("Chủ đề:")
            content = st.text_area("Nội dung chi tiết:")
            category = st.selectbox("Danh mục:", ["coding", "design", "testing", "deployment", "qmdg", "other"])
            
            if st.form_submit_button("💾 Lưu vào Bộ Nhớ"):
                if topic and content:
                    st.session_state.memory.store_knowledge(topic, content, category=category)
                    st.success("✅ Đã lưu kiến thức mới!")
                    st.experimental_rerun()

def render_workflows_tab():
    st.subheader("Quản Lý n8n Workflows")
    
    client = st.session_state.n8n_client
    
    # Connection Status Check
    is_connected = client.test_connection()
    
    col_status, col_config = st.columns([2, 1])
    with col_status:
        if is_connected:
            st.success(f"✅ **Đã kết nối n8n** tại `{client.base_url}`")
        else:
            st.warning("⚠️ **Chưa kết nối n8n Server** (Dùng Local Files)")
    
    with col_config:
        with st.popover("⚙️ Cấu Hình"):
            st.markdown("### Cấu hình n8n")
            with st.form("n8n_config_form"):
                base_url = st.text_input("Server URL:", value=client.base_url)
                api_key = st.text_input("API Key:", value=client.api_key or "", type="password")
                
                if st.form_submit_button("Lưu & Kết Nối"):
                    setup_n8n_config(api_key, base_url)
                    # Re-init client
                    st.session_state.n8n_client = N8NClient(base_url, api_key)
                    st.rerun()

    # If connected, show Dashboard
    if is_connected:
        st.markdown("---")
        
        # Stats Board
        s1, s2, s3, s4 = st.columns(4)
        stats = client.get_workflow_statistics()
        exec_stats = client.get_execution_statistics()
        
        s1.metric("Total Workflows", stats['total_workflows'])
        s2.metric("Active Running", stats['active_workflows'])
        s3.metric("Total Executions", exec_stats['total_executions'])
        s4.metric("Success Rate", f"{int(exec_stats['successful'] / max(1, exec_stats['total_executions']) * 100)}%")
        
        st.markdown("### 📋 Danh Sách Workflows (Server)")
        
        tab_list, tab_execs = st.tabs(["Workflows", "Recent Executions"])
        
        with tab_list:
            workflows = client.get_workflows()
            for wf in workflows:
                status_icon = "🟢" if wf.get('active') else "⚪"
                with st.expander(f"{status_icon} {wf.get('name', 'Unnamed')} (ID: {wf.get('id')})"):
                    col_info, col_act = st.columns([3, 1])
                    with col_info:
                        st.json(wf)
                    with col_act:
                        if wf.get('active'):
                            if st.button("⏹️ Deactivate", key=f"deac_{wf['id']}"):
                                client.deactivate_workflow(wf['id'])
                                st.rerun()
                        else:
                            if st.button("▶️ Activate", key=f"act_{wf['id']}"):
                                client.activate_workflow(wf['id'])
                                st.rerun()
                        
                        if st.button("🚀 Execute", key=f"exec_{wf['id']}"):
                            with st.spinner("Executing..."):
                                res = client.execute_workflow(wf['id'])
                                if res: st.success("Executed!")
                                else: st.error("Failed")
        
        with tab_execs:
            executions = exec_stats['executions']
            for exe in executions:
                status = "✅" if exe.get('finished') and not exe.get('stoppedAt') else "❌"
                st.write(f"{status} **ID:** {exe.get('id')} | **Time:** {exe.get('startedAt')}")

    
    st.markdown("---")
    st.info("📂 **Local Workflow Files (Backups/Templates):**")
    
    # List workflows in directory (Fallback/Reference)
    workflows_dir = Path("n8n_workflows")
    if workflows_dir.exists():
        tabs = st.tabs(["Secretary", "Code Writer", "Code Fixer", "Memory"])
        
        with tabs[0]:
            show_workflows_in_dir(workflows_dir / "secretary")
        with tabs[1]:
            show_workflows_in_dir(workflows_dir / "code_writer")
        with tabs[2]:
            show_workflows_in_dir(workflows_dir / "code_fixer")
        with tabs[3]:
            show_workflows_in_dir(workflows_dir / "memory")

def show_workflows_in_dir(directory):
    if directory.exists():
        for wf_file in directory.rglob("*.json"):
            with st.expander(f"📄 {wf_file.name}"):
                st.markdown(f"**Path:** `{wf_file}`")
                try:
                    with open(wf_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    st.json(data)
                except:
                    st.error("Invalid JSON")

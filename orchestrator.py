import streamlit as st
import json
import datetime
from skill_library import lookup_concept
from ai_tools import get_khong_minh_luc_dieu, get_lunar_date_offline

class AIOrchestrator:
    """
    Simulates an n8n-style workflow orchestration.
    Coordinates specialized Agents (Nodes) to answer user queries accurately.
    """
    
    def __init__(self, gemini_helper):
        self.gemini = gemini_helper
        self.logs = [] # Execution logs to show in UI
        
    def log_step(self, step_name, status, detail=""):
        entry = {
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "step": step_name,
            "status": status,
            "detail": detail
        }
        self.logs.append(entry)
        
    def run_pipeline(self, user_question, current_topic="Chung", chart_data=None, mai_hoa_data=None, luc_hao_data=None):
        """
        Main Workflow Entry Point.
        Flow:
        1. Intent Analysis Node (Router)
        2. Knowledge Retrieval Node (Worker) - Now includes [LIVE BOARD DATA]
        3. Context Memory Node
        4. Synthesis Node (Writer)
        """
        self.logs = [] # Reset logs
        final_answer = ""
        knowledge_context = ""
        
        # --- NODE 0: LIVE DATA INGESTION ---
        live_context = self._format_live_context(chart_data, mai_hoa_data, luc_hao_data)
        if live_context:
            knowledge_context += f"\n[DỮ LIỆU BÀN CỜ ĐANG HIỂN THỊ (LIVE DATA)]:\n{live_context}\n"
            self.log_step("Live Data Ingestion", "SUCCESS", "Captured current Board/Hexagram state.")
        else:
            self.log_step("Live Data Ingestion", "SKIPPED", "No active chart/hexagram found.")

        # --- NODE 1: INTENT ROUTER ---
        self.log_step("Intent Analysis", "RUNNING", "Analyzing user question...")
        intent = "GENERAL"
        
        q_lower = user_question.lower()
        
        # Priority 1: Time Calculation (Specific tool required)
        if any(x in q_lower for x in ["giờ tốt", "xuất hành", "khổng minh", "tính giờ"]):
            intent = "CALCULATION"
            
        # Priority 2: Timing / Forecast (When?)
        elif any(x in q_lower for x in ["khi nào", "bao lâu", "tháng mấy", "năm nào", "ứng kỳ", "thời gian", "lúc nào", "ngày nào"]):
            intent = "TIMING"
            
        # Priority 3: Personality / People / Profiles
        elif any(x in q_lower for x in ["tính cách", "con người", "ngoại hình", "tâm tính", "trai", "gái", "nam", "nữ", "là ai", "người nào", "của ai", "ghét", "thương", "ai", "đàn ông", "phụ nữ", "con trai", "con gái", "đối phương"]):
            intent = "PROFILE"
            
        # Priority 4: Remedy / Items
        elif any(x in q_lower for x in ["hóa giải", "vật phẩm", "làm gì để", "linh vật"]):
            intent = "REMEDY"
            
        # Priority 5: Weather
        elif any(x in q_lower for x in ["mưa", "nắng", "thời tiết", "bão"]):
            intent = "WEATHER"
            
        # Priority 6: Definitions / Terms
        elif any(x in q_lower for x in ["là gì", "ý nghĩa", "giải thích", "định nghĩa"]):
            intent = "DEFINITION"
            
        # Priority 7: Analysis / Review Table
        elif any(x in q_lower for x in ["luận giải", "phân tích", "đánh giá", "xem giúp", "như thế nào"]):
            intent = "ANALYSIS"
            
        self.log_step("Intent Analysis", "COMPLETED", f"Detected Intent: {intent}")
        
        # --- NODE 2: KNOWLEDGE RETRIEVAL ---
        self.log_step("Knowledge Retrieval", "RUNNING", f"Fetching data for {intent}...")
        
        # Sub-Node: Time Horizon Hint
        time_horizon = "FUTURE"
        if any(x in q_lower for x in ["đã", "vừa mới", "quá khứ", "trước đây"]):
            time_horizon = "PAST"
        knowledge_context += f"\n[GỢI Ý THỜI ĐIỂM]: {time_horizon}\n"

        # Sub-Node: Dictionary Skill
        dict_data = lookup_concept(user_question)
        if dict_data:
            self.log_step("Dictionary Skill", "SUCCESS", f"Found definition for input term.")
            knowledge_context += f"\n[📖 TỪ ĐIỂN CHUYÊN NGÀNH]: {dict_data['summary']}\nChi tiết: {dict_data['details']}\n"
        
        # Sub-Node: Object Mapping (ALWAYS INJECT FOR CONTEXT)
        dung_than_data = lookup_concept("dụng thần")
        if dung_than_data:
             knowledge_context += f"\n[🔍 BẢNG TRA CỨU ĐỐI TƯỢNG (DỤNG THẦN)]: {dung_than_data['summary']}\nChi tiết: {dung_than_data['details']}\n"
             self.log_step("Object Mapping", "SUCCESS", "Loaded Reference Objects Table.")

        # Sub-Node: Timing/Remedy/Weather Skill logic dispatch
        for skill_key, skill_intent in [("ứng kỳ", "TIMING"), ("hóa giải", "REMEDY"), ("thời tiết", "WEATHER")]:
            if intent == skill_intent:
                skill_data = lookup_concept(skill_key)
                if skill_data:
                     knowledge_context += f"\n[🔍 QUY TẮC CHUẨN - {skill_key.upper()}]:\n{skill_data['details']}\n"
                     self.log_step(f"{skill_key.capitalize()} Skill", "SUCCESS", f"Loaded Rules for {skill_intent}")
        
        # Sub-Node: Personality & Gender Profiling Skill
        if intent == "PROFILE":
            profile_data = lookup_concept("tính cách")
            gender_data = lookup_concept("nam nữ")
            
            if profile_data:
                 knowledge_context += f"\n[👤 TỪ ĐIỂN TÍNH CÁCH]:\n{profile_data['details']}\n"
            if gender_data:
                 knowledge_context += f"\n[⚧️ QUY TẮC XEM GIỚI TÍNH (Nam/Nữ)]:\n{gender_data['details']}\n"
            
            self.log_step("Profile Skill", "SUCCESS", "Loaded Profile & Gender Rules.")

        # Sub-Node: Time Calculation Skill
        if intent == "CALCULATION":
            try:
                d_val = datetime.datetime.now()
                if hasattr(st, 'session_state') and 'selected_date' in st.session_state:
                     d_val = st.session_state.selected_date
                lm, ld = get_lunar_date_offline(d_val)
                summ, det = get_khong_minh_luc_dieu(lm, ld)
                knowledge_context += f"\n[⏱️ TÍNH TOÁN THỜI GIAN]:\n{summ}\n{det}\n"
                self.log_step("Time Calc Skill", "SUCCESS", f"Calculated for Lunar Date {ld}/{lm}")
            except Exception as e:
                self.log_step("Time Calc Skill", "ERROR", str(e))
                
        # Sub-Node: Topic Context (ONLY if not a standalone definition/timing/profile question)
        import qmdg_data
        topic_dict = getattr(qmdg_data, 'TOPIC_INTERPRETATIONS', {})
        
        # If user asks a general definition or profile, the UI topic (e.g. Selling House) 
        # often distracts. We only inject it if intent is ANALYSIS or GENERAL.
        if intent in ["ANALYSIS", "GENERAL"] and current_topic in topic_dict:
             t_data = topic_dict[current_topic]
             knowledge_context += f"\n[CHỦ ĐỀ ĐANG XEM TRÊN UI]: {current_topic}\n- Dụng thần chuẩn: {t_data.get('Dụng_Thần')}\n- Gợi ý luận giải: {t_data.get('Luận_Giải_Gợi_Ý')}\n"
        
        self.log_step("Knowledge Retrieval", "COMPLETED", "Data gathering finished.")
        
        # --- NODE 3: CONTEXT MEMORY ---
        self.log_step("Context Memory", "RUNNING", "Retrieving session history...")
        history_context = ""
        if hasattr(st, 'session_state') and 'chat_history' in st.session_state:
            # Take last 3 exchanges for context
            recent_history = st.session_state.chat_history[-6:] 
            history_context = "\n[LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY]:\n"
            for msg in recent_history:
                role = "Bạn" if msg["role"] == "user" else "AI"
                history_context += f"- {role}: {msg['content'][:100]}...\n"
        self.log_step("Context Memory", "SUCCESS", "Internal memory updated.")

        # --- NODE 4: SYNTHESIS ---
        self.log_step("Gemini Synthesis", "RUNNING", "Generating final response...")
        
        # Construct Prompt
        system_prompt = (
            f"VAI TRÒ: Bạn là Hệ thống SIÊU TRÍ TUỆ KỲ MÔN (Orchestrated AI).\n"
            f"BẠN PHẢI TRẢ LỜI CHÍNH XÁC THEO CÁC NGUỒN DỮ LIỆU ĐƯỢC CUNG CẤP DƯỚI ĐÂY:\n"
            f"{history_context}\n"
            f"{knowledge_context}\n"
            f"--------------------------------------------------\n"
            f"CÂU HỎI NGƯỜI DÙNG: '{user_question}'\n\n"
            f"QUY TẮC BẮT BUỘC:\n"
            f"1. BẮT BUỘC căn cứ vào [DỮ LIỆU BÀN CỜ ĐANG HIỂN THỊ] (Kỳ Môn, Mai Hoa, Kinh Dịch) để đưa ra kết luận. KHÔNG TRẢ LỜI CHUNG CHUNG.\n"
            f"2. BẮT BUỘC xác định đúng đối tượng (Dụng Thần) cần xem từ [BẢNG TRA CỨU ĐỐI TƯỢNG].\n"
            f"3. Xác định đúng thời điểm (Quá khứ/Hiện tại/Tương lai) từ đề bài và [GỢI Ý THỜI ĐIỂM] để trả lời phù hợp.\n"
            f"4. Nếu có dữ liệu [📖 TỪ ĐIỂN] hoặc [⚧️ GIỚI TÍNH], bạn phải dùng đúng định nghĩa đó. KHÔNG ĐƯỢC TỰ Ý THAY ĐỔI.\n"
            f"5. Nếu hỏi về thời gian (Khi nào), hãy áp dụng đúng [⏳ QUY TẮC ỨNG KỲ]. Giải thích rõ tại sao.\n"
            f"6. TRÌNH BÀY: \n"
            f"   - Bắt đầu bằng khối [SUY_LUAN] giải thích logic tìm kiếm thông tin.\n"
            f"   - Kết thúc bằng [KET_LUAN] đưa ra câu trả lời cuối cùng súc tích, chuẩn xác sách vở.\n"
            f"   - QUY TẮC CÔ LẬP NHIỆM VỤ: Nếu người dùng hỏi về con người (trai/gái), thời tiết, hay thời gian, hãy BỎ QUA HOÀN TOÀN các chủ đề mặc định như 'Bán nhà đất', 'Kiện tụng' đang có trên UI. Chỉ tập trung vào việc tra cứu Dụng Thần tương ứng trong dữ liệu chuyên ngành.\n"
            f"7. TUYỆT ĐỐI ưu tiên dữ liệu trong [TỪ ĐIỂN] và [BẢNG TRA CỨU] hơn là kiến thức tổng quát của AI. Nếu sách quy định là Nam, bạn không được tự ý trả lời là Nữ."
        )
        
        final_answer = self.gemini._call_ai(system_prompt)
        return final_answer

    def _format_live_context(self, qmdg, mai_hoa, luc_hao):
        """Helper to turn complex state into readable text for AI"""
        context = ""
        
        # 1. QMDG Grid
        if qmdg:
            context += "--- KỲ MÔN ĐỘN GIÁP ---\n"
            # Extract basic 4 pillars if available
            context += f"Tứ trụ: {qmdg.get('can_nam')} {qmdg.get('chi_nam')} / {qmdg.get('can_thang')} {qmdg.get('chi_thang')} / {qmdg.get('can_ngay')} {qmdg.get('chi_ngay')} / {qmdg.get('can_gio')} {qmdg.get('chi_gio')}\n"
            context += f"Tiết khí: {qmdg.get('tiet_khi')} | Cục: {qmdg.get('cuc')} {'Dương' if qmdg.get('is_duong_don') else 'Âm'}\n"
            
            # Extract 9 palaces
            for i in range(1, 10):
                sao = qmdg.get('thien_ban', {}).get(i, "N/A")
                mon = qmdg.get('nhan_ban', {}).get(i, "N/A")
                than = qmdg.get('than_ban', {}).get(i, "N/A")
                c_thien = qmdg.get('can_thien_ban', {}).get(i, "N/A")
                c_dia = qmdg.get('dia_can', {}).get(i, "N/A")
                context += f"- Cung {i}: {sao}, {mon}, {than}, Thiên Can {c_thien} lâm {c_dia}\n"

        # 2. Mai Hoa
        if mai_hoa:
            context += "\n--- MAI HOA DỊCH SỐ ---\n"
            context += f"Quẻ Chính: {mai_hoa.get('ten')} (Thể: {mai_hoa.get('ten_the')}, Dụng: {mai_hoa.get('ten_dung')})\n"
            context += f"Quan hệ Ngũ hành: {mai_hoa.get('upper_element')} / {mai_hoa.get('lower_element')}\n"
            context += f"Tượng Quẻ: {mai_hoa.get('tuong')}\n"
            context += f"Quẻ Biến: {mai_hoa.get('ten_qua_bien')} (Động hào {mai_hoa.get('dong_hao')})\n"

        # 3. Lục Hào
        if luc_hao:
            context += "\n--- LỤC HÀO ---\n"
            context += f"Quẻ: {luc_hao.get('ten_que')}\n"
            context += f"Dụng Thần: {luc_hao.get('dung_than_label')}\n"
            context += f"Trạng thái Thế/Ứng: {luc_hao.get('the_ung_interaction')}\n"
            
        return context
        
    def render_logs(self):
        """Render the n8n-style execution steps in Streamlit"""
        st.markdown("### ⚙️ Quy Trình Xử Lý (System Workflow)")
        for log in self.logs:
            icon = "✅" if log['status'] in ["SUCCESS", "COMPLETED"] else "🔄"
            if log['status'] == "ERROR": icon = "❌"
            
            with st.expander(f"{icon} {log['step']} - {log['status']}", expanded=False):
                st.write(f"**Time:** {log['time']}")
                st.write(f"**Detail:** {log['detail']}")


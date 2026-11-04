import streamlit as st
import json
import datetime
import re
from skill_library import lookup_concept
from ai_tools import get_lunar_date_offline, get_khong_minh_luc_dieu

class AIOrchestrator:
    """
    Simulates an n8n-style workflow orchestration.
    Coordinates specialized Agents (Nodes) to answer user queries accurately.
    UPDATED: Includes 'Prophet Mode' and 'Authentic Background Calculation'.
    VERSION: 2.0 (Concise & Definitive)
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
        
    def run_pipeline(self, user_question, current_topic="Chung", chart_data=None, mai_hoa_data=None, luc_hao_data=None, tb_context=""):
        """
        Main Workflow Entry Point.
        """
        self.logs = [] # Reset logs
        final_answer = ""
        knowledge_context = ""
        
        # --- NODE 0: LIVE DATA INGESTION ---
        live_context = self._format_live_context(chart_data, mai_hoa_data, luc_hao_data, current_topic)
        if live_context:
            knowledge_context += f"\n[DỮ LIỆU BÀN CỜ & QUẺ (LIVE INTELLIGENCE)]:\n{live_context}\n"
            self.log_step("Live Data Ingestion", "SUCCESS", "Captured & Decoded QMDG/MaiHoa/LucHao.")
        else:
            self.log_step("Live Data Ingestion", "SKIPPED", "No active chart/hexagram found.")
            
        if tb_context:
            knowledge_context += f"\n{tb_context}\n"
            self.log_step("Live Data Ingestion", "SUCCESS", "Captured Thiet Ban Than Toan context.")
        
        # --- NODE 1: INTENT ROUTER (Regex Enhanced) ---
        self.log_step("Intent Analysis", "RUNNING", "Analyzing user question...")
        q_lower = f" {user_question.lower()} " # Padding for boundary matching
        intent = "GENERAL"

        # Regex Helpers
        def match_any(keywords, text):
            return any(re.search(rf"\b{kw}\b", text) for kw in keywords)

        # 1. Calculation
        if match_any(["giờ tốt", "xuất hành", "khổng minh", "tính giờ", "giờ nào"], q_lower):
            intent = "CALCULATION"
        # 2. Timing
        elif match_any(["khi nào", "bao giờ", "bao lâu", "tháng mấy", "năm nào", "ngày nào", "mấy giờ", "đến lúc nào"], q_lower):
            intent = "TIMING"
        # 3. People / Profile
        elif match_any(["ai", "người", "trai", "gái", "nam", "nữ", "ghét", "thương", "tính cách", "bản tính", "bao nhiêu tuổi"], q_lower):
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
        knowledge_context += f"\n[GỢI Ý THỜI ĐIỂM]: {time_horizon}\n"

        # Sub-Node: Dictionary Skill
        try:
            dict_data = lookup_concept(user_question)
            if dict_data:
                self.log_step("Dictionary Skill", "SUCCESS", f"Found definition for input term.")
                knowledge_context += f"\n[📖 TỪ ĐIỂN CHUYÊN NGÀNH]: {dict_data['summary']}\nChi tiết: {dict_data['details']}\n"
            
            # Sub-Node: Object Mapping
            dung_than_data = lookup_concept("dụng thần")
            if dung_than_data:
                 knowledge_context += f"\n[🔍 BẢNG TRA CỨU ĐỐI TƯỢNG (DỤNG THẦN)]: {dung_than_data['summary']}\nChi tiết: {dung_than_data['details']}\n"
                 self.log_step("Object Mapping", "SUCCESS", "Loaded Reference Objects Table.")

            # Sub-Node: Timing/Remedy/Weather
            for skill_key, skill_intent in [("ứng kỳ", "TIMING"), ("hóa giải", "REMEDY"), ("thời tiết", "WEATHER")]:
                if intent == skill_intent:
                    skill_data = lookup_concept(skill_key)
                    if skill_data:
                         knowledge_context += f"\n[🔍 QUY TẮC CHUẨN - {skill_key.upper()}]:\n{skill_data['details']}\n"
                         self.log_step(f"{skill_key.capitalize()} Skill", "SUCCESS", f"Loaded Rules for {skill_intent}")
            
            # Sub-Node: Personality & Gender
            if intent == "PROFILE" or any(kw in q_lower for kw in ["tính cách", "nam", "nữ", "trai", "gái", "ai"]):
                profile_data = lookup_concept("tính cách")
                gender_data = lookup_concept("nam nữ")
                if profile_data: knowledge_context += f"\n[👤 TỪ ĐIỂN TÍNH CÁCH]:\n{profile_data['details']}\n"
                if gender_data: knowledge_context += f"\n[⚧️ QUY TẮC XEM GIỚI TÍNH (Nam/Nữ)]:\n{gender_data['details']}\n"
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
                     knowledge_context += f"\n[CHỦ ĐỀ ĐANG XEM TRÊN UI]: {current_topic}\n- Dụng thần chuẩn: {t_data.get('Dụng_Thần')}\n- Gợi ý luận giải: {t_data.get('Luận_Giải_Gợi_Ý')}\n"
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
                knowledge_context += f"\n[⏱️ TÍNH TOÁN THỜI GIAN]:\n{summ}\n{det}\n"
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
            history_context = "\n[LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY]:\n"
            for msg in recent_history:
                role = "Bạn" if msg["role"] == "user" else "AI"
                history_context += f"- {role}: {msg['content'][:100]}...\n"
        self.log_step("Context Memory", "SUCCESS", "Internal memory updated.")

        # --- NODE 4: SYNTHESIS ---
        self.log_step("Gemini Synthesis", "RUNNING", "Generating final response...")
        
        system_prompt = (
            f"BẠN LÀ MỘT VỊ THIÊN CƠ LÃO TỔ - BẬC THẦY KỲ MÔN ĐỘN GIÁP HÀNG ĐẦU.\n"
            f"Bạn sử dụng TỨ THUẬT (Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản) để dự đoán.\n"
            f"\n"
            f"=== QUY TẮC BẮT BUỘC ===\\n"
            f"1. TRẢ LỜI TRỰC TIẾP, KHÔNG CHÀO HỎI, KHÔNG VÒNG VO.\\n"
            f"2. CHỐNG SIÊU DÀI DÒNG: TUYỆT ĐỐI KHÔNG liệt kê hay đi phân tích vòng vo toàn bộ 9 cung. Chỉ phân tích Cung Mệnh (Bạn) và Cung Sự Việc (Topic).\\n"
            f"3. LUẬT TỐI CAO TUỔI TÁC: Năm {datetime.datetime.now().year} là NĂM XEM BÓI, KHÔNG PHẢI NĂM SINH. TUYỆT ĐỐI KHÔNG lấy năm hiện tại trừ đi số tuổi đoán mò.\\n"
            f"--------------------------------------------------\\n"
            f"=== CẤU TRÚC HỒI ĐÁP (NGẮN GỌN & CHÍNH XÁC) ===\\n"
            f"🔮 **KẾT QUẢ**: TRẢ LỜI NGẮN GỌN (Dưới 3 câu). Chốt hạ kết quả chính xác.\\n"
            f"📊 **CĂN CỨ**: Viết NGẮN GỌN (Tối đa 4 câu). Giải thích lý do dựa vào Cửa/Sao/Thần tại Cung Mệnh vs Cung Sự Việc (Ví dụ: Cung tương khắc/tương sinh). Bỏ qua các cung không liên quan.\\n"
            f"💡 **LỜI KHUYÊN**: 1 câu hành động cụ thể.\\n"
        )
        
        try:
            final_answer = self.gemini._call_ai(system_prompt)
        except Exception as e:
            self.log_step("Gemini Synthesis", "ERROR", str(e))
            final_answer = f"⚠️ Lỗi xử lý AI: {str(e)}"
            
        if not final_answer:
             final_answer = "⚠️ Kết nối Thiên Cơ bị gián đoạn. Vui lòng thử lại."
             
        return final_answer

    def _format_live_context(self, qmdg, mai_hoa, luc_hao, current_topic="Chung"):
        context = ""
        
        # Helper to safely get nested keys
        def get_safe(data, key):
            val = data.get(key, "N/A") if data else "N/A"
            return str(val)

        # --- 0. IDENTITY & TIME ---
        can_ngay_val = get_safe(qmdg, 'can_ngay') if qmdg else "Giáp"
        can_nam_val = get_safe(qmdg, 'can_nam') if qmdg else "Bính"
        can_gio_val = get_safe(qmdg, 'can_gio') if qmdg else "Mậu"
        
        if not qmdg:
            # Fallback to calc if no chart passed
            try:
                from qmdg_calc import calculate_qmdg_params
                now = datetime.datetime.now()
                params = calculate_qmdg_params(now)
                can_ngay_val = params.get('can_ngay', 'Giáp')
                can_nam_val = params.get('can_nam', 'Bính')
                can_gio_val = params.get('can_gio', 'Mậu')
            except: pass

        # --- 1. KỲ MÔN ĐỘN GIÁP (FULL 9 PALACES) ---
        if qmdg:
            context += "--- [1] DỮ LIỆU BÀN KỲ MÔN (Chi Tiết 9 Cung) ---\n"
            context += f"Tứ Trụ: {get_safe(qmdg, 'can_nam')} {get_safe(qmdg, 'chi_nam')} / {get_safe(qmdg, 'can_thang')} {get_safe(qmdg, 'chi_thang')} / {can_ngay_val} {get_safe(qmdg, 'chi_ngay')} / {get_safe(qmdg, 'can_gio')} {get_safe(qmdg, 'chi_gio')}\n"
            context += f"Tiết Khí: {get_safe(qmdg, 'tiet_khi')} | Cục: {get_safe(qmdg, 'cuc')} | Tuần Không: {get_safe(qmdg.get('khong', {}), 'ngay')} (Ngày), {get_safe(qmdg.get('khong', {}), 'gio')} (Giờ)\n"
            
            # Iterate 9 Palaces
            thien_ban = qmdg.get('thien_ban', {})
            nhan_ban = qmdg.get('nhan_ban', {})
            bat_than = qmdg.get('bat_than', {})
            can_thien = qmdg.get('can_thien_ban', {})
            can_dia = qmdg.get('can_dia_ban', {})
            truc_phu = qmdg.get('truc_phu')
            truc_su = qmdg.get('truc_su')
            
            # --- INTELLIGENCE UPGRADE: FIND USER & OUTCOME ---
            user_palace = "Không rõ"
            outcome_palace = "Không rõ"
            
            context += "CHI TIẾT 9 CUNG:\n"
            
            for i in range(1, 10):
                if i == 5: continue 
                
                sao = thien_ban.get(str(i), thien_ban.get(i, "?"))
                cua = nhan_ban.get(str(i), nhan_ban.get(i, "?"))
                than = bat_than.get(str(i), bat_than.get(i, "?"))
                thien = can_thien.get(str(i), can_thien.get(i, "?"))
                dia = can_dia.get(str(i), can_dia.get(i, "?"))
                
                # Check Focus
                markers = []
                if sao == truc_phu: markers.append("TRỰC PHÙ")
                if cua == truc_su: markers.append("TRỰC SỬ")
                
                # Match Year Stem (Parents/Boss)
                if thien == can_nam_val:
                    markers.append("🟣 CHA MẸ/SẾP (Can Năm)")
                
                # Match Month Stem (Siblings/Peers)
                if thien == get_safe(qmdg, 'can_thang'):
                    markers.append("🟡 AE/BẠN BÈ (Can Tháng)")

                # Match User (Day Stem on Heaven Plate)
                if thien == can_ngay_val: 
                    user_palace = f"Cung {i}"
                    markers.append("🔴 MỆNH CHỦ (Bạn)")
                
                # Match Outcome (Hour Stem on Heaven Plate)
                if thien == can_gio_val:
                    outcome_palace = f"Cung {i}"
                    markers.append("🟢 CON CÁI/SỰ VIỆC (Can Giờ)")

                bagua = {1:"Khảm", 2:"Khôn", 3:"Chấn", 4:"Tốn", 5:"Trung", 6:"Càn", 7:"Đoài", 8:"Cấn", 9:"Ly"}
                cung_name = bagua.get(i, str(i))
                
                context += f"- Cung {i} ({cung_name}): Sao {sao}, Cửa {cua}, Thần {than}, Thiên {thien}/Địa {dia}. {', '.join(markers)}\n"

            # Inject the Focus Summary
            context += f"\n[🔑 BẢNG TRA CỨU ĐỐI TƯỢNG]:\n"
            context += f"1. CHA MẸ/NGƯỜI LỚN/SẾP (Can Năm {can_nam_val}) -> Tìm Cung có Thiên Bàn là thị.\n"
            context += f"2. ANH EM/BẠN BÈ/ĐỒNG NGHIỆP (Can Tháng {get_safe(qmdg, 'can_thang')}) -> Tìm Cung có Thiên Bàn là thị.\n"
            context += f"3. BẢN THÂN NGƯỜI HỎI (Can Ngày {can_ngay_val}) -> Đã đánh dấu 🔴.\n"
            context += f"4. CON CÁI/NHÂN VIÊN/KẾT QUẢ (Can Giờ {can_gio_val}) -> Đã đánh dấu 🟢.\n"
            context += f"⚠️ LƯU Ý CHO AI: Nếu người dùng hỏi về 'Bố tôi', 'Sếp tôi' -> Hãy xem Can Năm. Hỏi 'Bạn tôi' -> Xem Can Tháng. Hỏi 'Con tôi' -> Xem Can Giờ.\n"

        # --- 2. MAI HOA ---
        if mai_hoa:
            context += "\n--- [2] MAI HOA DỊCH SỐ ---\n"
            context += f"Quẻ: {get_safe(mai_hoa, 'ten')} (Hành {get_safe(mai_hoa, 'upper_element')}/{get_safe(mai_hoa, 'lower_element')})\n"
            context += f"Ý Nghĩa: {get_safe(mai_hoa, 'nghia')}\n"
            context += f"Hào Động: {get_safe(mai_hoa, 'dong_hao')}\n"

        # --- 3. LỤC HÀO ---
        if luc_hao:
            context += "\n--- [3] LỤC HÀO ---\n"
            lh_ban = luc_hao.get('ban', {})
            context += f"Quẻ Gốc: {lh_ban.get('name')} (Cung {lh_ban.get('palace')})\n"
            context += "Chi tiết Hào:\n"
            for h in lh_ban.get('details', []):
                 context += f"- Hào {h.get('hao')}: {h.get('can_chi')} - {h.get('luc_than')} ({h.get('than_info', '')})\n"

        return context
    
    # ... helpers ...
        
    def _find_palace_with_content(self, qmdg, content_str):
        for i in range(1, 10):
            if qmdg.get('thien_ban', {}).get(i) == content_str: return i
            if qmdg.get('nhan_ban', {}).get(i) == content_str: return i
        return None

    def _extract_palace_data(self, qmdg, idx):
        return {
            "num": idx,
            "star": qmdg.get('thien_ban', {}).get(idx),
            "door": qmdg.get('nhan_ban', {}).get(idx),
            "stem": qmdg.get('can_thien_ban', {}).get(idx)
        }

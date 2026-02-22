"""
Enhanced Gemini Helper - TỨ THUẬT HỢP NHẤT (V4.0 - Four Arts Unified)
Deeply integrates: Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản Thần Toán
Refactored for Maximum Accuracy & Anti-Hallucination
"""

import google.generativeai as genai
import os
import requests
import json
import time
import hashlib
import re
import datetime
import streamlit as st

# Robust Fallback Import
try:
    from free_ai_helper import FreeAIHelper
except ImportError:
    class FreeAIHelper:
        def __getattr__(self, name):
            return lambda *args, **kwargs: "⚠️ Chế độ Offline không khả dụng (Lỗi Import)."

class GeminiQMDGHelper:
    """Helper class for Gemini AI with QMDG specific knowledge and grounding"""
    
    def __init__(self, api_key_input):
        # --- 1. KEY PARSING (Robost) ---
        import re
        keys_from_regex = re.findall(r"AIza[0-9A-Za-z-_]{35}", str(api_key_input))
        raw_text = str(api_key_input).replace("\n", ",").replace(";", ",")
        keys_from_split = [k.strip() for k in raw_text.split(',') if len(k.strip()) > 30 and "AIza" in k]
        all_candidates = keys_from_regex + keys_from_split
        self.api_keys = list(dict.fromkeys(all_candidates)) 
        self.api_keys = [k for k in self.api_keys if len(k) > 30]

        self.current_key_index = 0
        self.api_key = self.api_keys[0] if self.api_keys else None
        
        self.version = "V4.0-TuThuat"
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self._failed_models = set()
        self._hashlib = hashlib
        self.max_retries = 2
        self.base_delay = 1
        self.n8n_url = None
        self.n8n_timeout = 8
        self.logs = [] 

        # Initial Model Setup
        self.model = self._get_best_model_placeholder()
        self.fallback_helper = FreeAIHelper()

    def _get_best_model_placeholder(self):
        return genai.GenerativeModel('gemini-1.5-flash')

    def log_step(self, step, status, detail):
        self.logs.append({
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "step": step,
            "status": status,
            "detail": detail
        })

    def test_connection(self):
        try:
            valid_models = []
            try:
                available = list(genai.list_models())
                for m in available:
                    if 'generateContent' in m.supported_generation_methods:
                        valid_models.append(m.name)
            except Exception as e:
                return False, f"Lỗi liệt kê model: {str(e)}"

            if not valid_models:
                return False, "Key không có quyền truy cập model nào!"

            # Priority: 1.5 Pro > 1.5 Flash
            priority_order = ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-pro']
            chosen_model_name = valid_models[0]
            
            for p in priority_order:
                for vm in valid_models:
                    if p in vm:
                        chosen_model_name = vm
                        break
                if chosen_model_name != valid_models[0]: break
            
            self.model = genai.GenerativeModel(chosen_model_name)
            self.model.generate_content("ping")
            return True, f"Kết nối OK! ({chosen_model_name})"

        except Exception as e:
            return False, f"Lỗi kết nối: {str(e)}"

    def set_n8n_url(self, url):
        self.n8n_url = url

    # --- CORE: CALL AI RAW ---
    def _call_ai_raw(self, prompt):
        # SAFETY SETTINGS: OFF
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Auto-Discovery of Models
        if not hasattr(self, 'cascade_models') or not self.cascade_models:
             self.cascade_models = [
                'gemini-1.5-pro-latest',
                'gemini-1.5-pro',
                'gemini-1.5-flash-latest',
                'gemini-1.5-flash',
                'gemini-pro'
             ]

        error_log = []
        
        # KEY ROTATION & MODEL CASCADE
        for key_idx, current_api_key in enumerate(self.api_keys):
            try:
                genai.configure(api_key=current_api_key)
            except: continue

            for model_name in self.cascade_models:
                try:
                    active_model = genai.GenerativeModel(model_name)
                    resp = active_model.generate_content(prompt, safety_settings=safety_settings)
                    
                    text = ""
                    try: text = resp.text
                    except: 
                        if resp.candidates: text = resp.candidates[0].content.parts[0].text
                    
                    if text and len(text.strip()) > 1:
                        return text
                    
                    error_log.append(f"{model_name}: Empty/Blocked")
                    
                except Exception as e:
                    error_log.append(f"{model_name}: {str(e)}")
                    if "429" in str(e): time.sleep(2)
                    continue
        
        return f"🛑 AI Failed. Errors: {'; '.join(error_log)}"

    def _call_ai(self, prompt, **kwargs):
        return self._call_ai_raw(prompt)

    # ================================================================
    # CORE: ANSWER QUESTION (THE BRAIN) - V4.0 TỨ THUẬT HỢP NHẤT
    # ================================================================
    def answer_question(self, question, chart_data=None, topic="Chung", selected_subject=None, mai_hoa_data=None, luc_hao_data=None): 
        self.logs = [] # Reset logs
        
        # 1. GREETING CHECK
        social_keywords = ["chào", "hello", "hi", "bạn ơi"]
        if len(question.split()) < 5 and any(k in question.lower() for k in social_keywords):
            return "Chào bạn, tôi là Trợ lý Huyền Học (AI Tiên Tri V4.0 Tứ Thuật). Tôi có thể giúp gì cho bạn về vận mệnh, thời thế?"

        # 2. PREPARE FULL CONTEXT DATA (ALL 4 METHODS)
        live_context = self._get_paranoid_context(chart_data, topic, question, selected_subject, mai_hoa_data, luc_hao_data)
        
        # 3. DATE ENFORCEMENT
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M")
        
        universal_rulebook = (
            "=========================================\n"
            "📖 CẨM NANG DỤNG THẦN VẠN NĂNG (UNIVERSAL RULEBOOK)\n"
            "Dùng cẩm nang này để tự suy luận Dụng Thần cho BẤT KỲ CÂU HỎI NÀO của người dùng:\n\n"
            "1. LỤC THÂN (LỤC HÀO) - ĐẠI DIỆN CHO:\n"
            "- HÀO QUAN QUỶ: Nghề nghiệp, chức vụ, sếp, bệnh tật, ma quỷ, tai họa, trộm cướp, chồng/bạn trai.\n"
            "- HÀO THÊ TÀI: Tiền bạc, tài sản, lợi nhuận, đồ ăn, vợ/bạn gái, thuộc cấp, người làm thuê.\n"
            "- HÀO TỬ TÔN: Con cái, cháu chắt, thú cưng, thuốc men chữa bệnh, sự bình an, đường gỡ rối.\n"
            "- HÀO PHỤ MẪU: Cha mẹ, người lớn tuổi, nhà cửa, đất đai, xe cộ, trường học, quần áo, giấy tờ, hợp đồng, tin tức.\n"
            "- HÀO HUYNH ĐỆ: Anh chị em, bạn bè, đối tác, đối thủ cạnh tranh, người chia tiền.\n\n"
            "2. KỲ MÔN DỤNG THẦN - ĐẠI DIỆN CHO:\n"
            "- Nhật Can (Can Ngày): Bản thân người hỏi.\n"
            "- Thời Can (Can Giờ): Sự việc chung, kết quả, con cái, súc vật, cấp dưới.\n"
            "- Nguyệt Can (Can Tháng): Anh em, bạn bè, đồng nghiệp.\n"
            "- Niên Can (Can Năm): Cha mẹ, trưởng bối, sếp lớn, chính quyền.\n"
            "- Khai Môn: Công việc, sự nghiệp, cửa hàng, mở mang.\n"
            "- Sinh Môn: Lợi nhuận, tiền tài, nhà cửa, sự sống, nghề địa ốc.\n"
            "- Tử Môn: Chết chóc, bệnh tật, đất đai, mồ mả, sự bế tắc.\n"
            "- Cảnh Môn: Thư từ, giấy báo, thi cử, hình ảnh, hỏa hoạn.\n"
            "- Thiên Tâm: Bác sĩ, thuốc men, quý nhân, người lãnh đạo.\n"
            "- Trực Phù: VIP, sếp, chủ nợ, tài sản lớn.\n"
            "- Huyền Vũ / Thiên Bồng: Trộm cướp, tiểu nhân, sự lừa dối, mất mát.\n\n"
            "3. CÔNG THỨC TOÁN SỐ BÍ TRUYỀN (Tính Số Lượng/Tuổi Tác):\n"
            "- Nếu hỏi số lượng (bao nhiêu người, mấy cái nhà, mấy tầng, mấy tỷ...): Chọn Cung Kỳ Môn chứa Dụng Thần. Số lượng = Số Hà Đồ của Cung đó (Khảm=1/6, Khôn=2/7, Chấn=3/8, Tốn=4/9, Trung=5/10, Càn=1/6, Đoài=4/9, Cấn=5/10, Ly=2/7). Nếu Cung Vượng/Tướng dồi dào -> Lấy số LỚN. Nếu Suy/Tuyệt -> Lấy số NHỎ.\n"
            "=========================================\n"
        )
        
        # 5. BUILD PROMPT V5.0 - MANG ĐOÁN
        system_prompt = (
            f"<system_instructions>\n"
            f"Bạn là Bậc Thầy Tứ Thuật (Kỳ Môn, Mai Hoa, Lục Hào, Thiết Bản). Năm {now.year} là năm xem bói.\n\n"
            f"LUẬT TOÁN MỆNH BẮT BUỘC:\n"
            f"- LỆNH NGÔN NGỮ: BẮT BUỘC 100% TRẢ LỜI BẰNG TIẾNG VIỆT.\n"
            f"- LỆNH THUYẾT TRÌNH: TRẢ LỜI NGAY VÀO FORMAT, TUYỆT ĐỐI KHÔNG HIỂN THỊ DÒNG SUY NGHĨ HAY CÁC BƯỚC PHÂN TÍCH BẰNG TIẾNG ANH (Như 'Okay, let's analyze...'). ❌ TUYỆT ĐỐI KHÔNG CHÀO HỎI, KHÔNG NÓI 'TÔI ĐÃ SẴN SÀNG'. ❌\n"
            f"- ⛔ LUẬT TỬ HÌNH CHỐNG ÁO GIÁC (ANTI-HALLUCINATION): BẠN CHỈ ĐƯỢC PHÉP LUẬN DỰA TRÊN DỮ LIỆU TRONG <context_data>! NẾU QUẺ KHÔNG NHẮC ĐẾN 'CUNG CÀN', THÌ TUYỆT ĐỐI KHÔNG ĐƯỢC CHÉM GIÓ VỀ 'CUNG CÀN'. CHỈ DÙNG DỮ LIỆU CÓ THẬT!!! ⛔\n"
            f"- KHÔNG được lười biếng tóm tắt chung chung. Bạn PHẢI đóng vai Thầy Bói thực thụ, thực hiện quy trình sau dựa trên <context_data>:\n"
            f"   + Bước 1: Xác định Dụng Thần (chủ thể của câu hỏi là gì?).\n"
            f"   + Bước 2: Tìm trong Kỳ Môn xem Cung của người hỏi (Can Ngày) và Cung Sự Việc (Dụng Thần/Can Giờ) tương sinh hay tương khắc.\n"
            f"   + Bước 3: Tìm trong Mai Hoa xem Thể và Dụng sinh khắc ra sao.\n"
            f"   + Bước 4: Khảo sát Lục Hào xem Hào Động báo hiệu điều gì, Dụng Thần vượng hay suy.\n"
            f"   + Bước 5: Tham chiếu Thiết Bản Thần Toán xem điềm báo thời cơ là gì.\n"
            f"   Lấy tất cả các dữ kiện có thật này chắp nối thành một câu trả lời chính xác, sắc bén và TUYỆT ĐỐI KHÔNG BỊA ĐẶT.\n\n"
            f"{universal_rulebook}\n"
            f"BẮT BUỘC TRÌNH BÀY ĐÚNG 4 PHẦN THEO ĐÚNG THỨ TỰ SAU (Tuyệt đối không được bỏ sót Header nào, kể cả khi thiếu dữ liệu):\n"
            f"# 1. HỒ SƠ KHÁCH HÀNG\n"
            f"(TUYỆT ĐỐI KHÔNG TRẢ LỜI CÂU HỎI CHÍNH Ở PHẦN NÀY! Chỉ suy luận tuổi/giới tính nếu có dữ liệu. Nếu không, ghi 'Không đủ dữ liệu xác định')\n\n"
            f"# 2. CĂN CỨ TỨ THUẬT\n"
            f"(Bắt buộc phân tích logic tại đây dựa trên <context_data>. Nếu môn nào thiếu, ghi 'Chưa gieo quẻ')\n"
            f"- KỲ MÔN: ...\n"
            f"- MAI HOA: ...\n"
            f"- LỤC HÀO: ...\n"
            f"- THIẾT BẢN: ...\n\n"
            f"# 3. KẾT QUẢ DỰ BÁO\n"
            f"(CHỈ ĐƯỢC PHÉP TRẢ LỜI CÂU HỎI TRỰC TIẾP TẠI ĐÂY. Tổng hợp logic từ Phần 2 để chốt ĐÁP ÁN)\n\n"
            f"# 4. LỜI KHUYÊN\n"
            f"(1 câu hành động thiết thực)\n"
            f"</system_instructions>\n\n"
            f"<context_data>\n"
            f"{live_context}\n"
            f"</context_data>\n\n"
            f"<user_question>\n"
            f"{question}\n"
            f"</user_question>"
        )
        
        # 5. CALL AI
        self.log_step("AI Generation", "RUNNING", "Sending Tứ Thuật prompt to Gemini...")
        raw_response = self._call_ai_raw(system_prompt)
        
        # 6. PROCESS RESPONSE
        return self._process_response(raw_response)

    # ================================================================
    # PARANOID CONTEXT BUILDER - V4.0 FULL 4 METHODS
    # ================================================================
    def _get_paranoid_context(self, qmdg_input, topic="Chung", question="", selected_subject=None, mai_hoa_data=None, luc_hao_data=None):
        """Builds comprehensive context from ALL 4 divination methods."""
        try:
            info = ""
            
            # ============================================
            # PART 1: KỲ MÔN ĐỘN GIÁP (Primary)
            # ============================================
            if qmdg_input and isinstance(qmdg_input, dict) and 'can_gio' in qmdg_input:
                can_ngay = qmdg_input.get('can_ngay', '?')
                can_gio = qmdg_input.get('can_gio', '?')
                can_thang = qmdg_input.get('can_thang', '?')
                can_nam = qmdg_input.get('can_nam', '?')
                
                t_tru = f"{can_nam} {qmdg_input.get('chi_nam','?')} / {can_thang} {qmdg_input.get('chi_thang','?')} / {can_ngay} {qmdg_input.get('chi_ngay','?')} / {can_gio} {qmdg_input.get('chi_gio','?')}"
                
                info += (
                    f"=== [1] KỲ MÔN ĐỘN GIÁP ===\n"
                    f"Tứ Trụ (THỜI ĐIỂM XEM BÓI, KHÔNG phải năm sinh): {t_tru}\n"
                    f"Tiết Khí: {qmdg_input.get('tiet_khi','?')} | Cục: {qmdg_input.get('cuc','?')}\n"
                    f"Tuần Không: {qmdg_input.get('khong_vong_4', {}).get('ngay', '?')} (Ngày), {qmdg_input.get('khong_vong_4', {}).get('gio', '?')} (Giờ)\n"
                )
                
                info += "\\n[BÀN CỜ 9 CUNG KỲ MÔN (ĐỂ SUY KẾT QUẢ)]:\\n"
                for p in range(1, 10):
                    p_star = qmdg_input.get('thien_ban', {}).get(p, '?')
                    p_door = qmdg_input.get('nhan_ban', {}).get(p, '?')
                    p_deity = qmdg_input.get('than_ban', {}).get(p, '?')
                    p_can_t = qmdg_input.get('can_thien_ban', {}).get(p, '?')
                    p_can_d = qmdg_input.get('can_dia_ban', {}).get(p, '?')
                    if p_star != '?':
                        info += f"- Cung {p}: Sao {p_star} | Cửa {p_door} | Thần {p_deity} | Can: {p_can_t}/{p_can_d}\\n"

                # --- DEEP PALACE ANALYSIS WITH NGŨ HÀNH ---
                try:
                    # Ngũ Hành mappings
                    CUNG_NGU_HANH = {'1': 'Thủy', '2': 'Thổ', '3': 'Mộc', '4': 'Mộc', '5': 'Thổ', '6': 'Kim', '7': 'Kim', '8': 'Thổ', '9': 'Hỏa'}
                    CAN_NGU_HANH = {'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa', 'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim', 'Nhâm': 'Thủy', 'Quý': 'Thủy'}
                    CAN_AM_DUONG = {'Giáp': 'Dương', 'Ất': 'Âm', 'Bính': 'Dương', 'Đinh': 'Âm', 'Mậu': 'Dương', 'Kỷ': 'Âm', 'Canh': 'Dương', 'Tân': 'Âm', 'Nhâm': 'Dương', 'Quý': 'Âm'}
                    
                    def ngu_hanh_relation(e1, e2):
                        """Return relationship: e1 đối với e2"""
                        SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
                        KHAC = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
                        if e1 == e2: return "Tỷ Hòa (ngang sức)"
                        if SINH.get(e1) == e2: return f"{e1} sinh {e2} → BẢN THÂN BỎ SỨC"
                        if SINH.get(e2) == e1: return f"{e2} sinh {e1} → BẢN THÂN ĐƯỢC HỖ TRỢ"
                        if KHAC.get(e1) == e2: return f"{e1} khắc {e2} → BẢN THÂN KHẮC CHẾ ĐỐI PHƯƠNG (CÁT)"
                        if KHAC.get(e2) == e1: return f"{e2} khắc {e1} → BẢN THÂN BỊ KHẮC (HUNG)"
                        return "?"
                    
                    def vuong_suy_state(can_hanh, cung_hanh):
                        """Tính trạng thái Vượng/Suy"""
                        SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
                        KHAC = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
                        if can_hanh == cung_hanh: return "VƯỢNG (đắc địa, mạnh nhất)"
                        if SINH.get(cung_hanh) == can_hanh: return "TƯỚNG (được sinh, khá mạnh)"
                        if SINH.get(can_hanh) == cung_hanh: return "HƯU (nghỉ ngơi, trung bình)"
                        if KHAC.get(can_hanh) == cung_hanh: return "TÙ (bị giam, yếu)"
                        if KHAC.get(cung_hanh) == can_hanh: return "TỬ (bị khắc, rất yếu)"
                        return "TRUNG BÌNH"
                    
                    subj_stem = can_ngay
                    obj_stem = can_gio
                    obj_label = "Sự Việc (Can Giờ)"
                    
                    if selected_subject:
                        s_sub = str(selected_subject).lower()
                        if "bố" in s_sub or "mẹ" in s_sub:
                            obj_stem = can_nam; obj_label = "Bố Mẹ (Can Năm)"
                        elif "anh" in s_sub or "chị" in s_sub or "em" in s_sub:
                            obj_stem = can_thang; obj_label = "Anh Chị Em (Can Tháng)"
                        elif "con" in s_sub:
                            obj_stem = can_gio; obj_label = "Con Cái (Can Giờ)"
                    
                    def find_palace_of_stem(stem_char):
                        ctb = qmdg_input.get('can_thien_ban', {})
                        for idx, s in ctb.items():
                            if s == stem_char: return idx
                        return None

                    subj_idx = find_palace_of_stem(subj_stem)
                    obj_idx = find_palace_of_stem(obj_stem)
                    
                    def get_details(idx):
                        if not idx: return "Không tìm thấy"
                        return (
                            f"Cung {idx} (Hành {CUNG_NGU_HANH.get(str(idx), '?')}) | "
                            f"Sao: {qmdg_input.get('thien_ban',{}).get(idx,'?')} | "
                            f"Cửa: {qmdg_input.get('nhan_ban',{}).get(idx,'?')} | "
                            f"Thần: {qmdg_input.get('than_ban',{}).get(idx,'?')}"
                        )
                    
                    # Compute Ngũ Hành analysis
                    subj_hanh = CAN_NGU_HANH.get(subj_stem, '?')
                    obj_hanh = CAN_NGU_HANH.get(obj_stem, '?')
                    subj_am_duong = CAN_AM_DUONG.get(subj_stem, '?')
                    subj_cung_hanh = CUNG_NGU_HANH.get(str(subj_idx), '?') if subj_idx else '?'
                    
                    # Vượng/Suy of Can Ngày in its palace
                    vuong_suy = vuong_suy_state(subj_hanh, subj_cung_hanh) if subj_hanh != '?' and subj_cung_hanh != '?' else '?'
                    
                    # Relationship between two palaces
                    relation = ngu_hanh_relation(subj_hanh, obj_hanh) if subj_hanh != '?' and obj_hanh != '?' else '?'
                    
                    info += (
                        f"\n[PHÂN TÍCH CUNG CHỦ vs CUNG SỰ VIỆC]\n"
                        f"★ BẢN THÂN (Can Ngày {subj_stem}, {subj_am_duong}, Hành {subj_hanh}): {get_details(subj_idx)}\n"
                        f"  → Trạng thái: {vuong_suy}\n"
                        f"★ ĐỐI TƯỢNG ({obj_label} {obj_stem}, Hành {obj_hanh}): {get_details(obj_idx)}\n"
                        f"★ QUAN HỆ NGŨ HÀNH: {relation}\n"
                    )
                except Exception as e:
                    info += f"\n(Lỗi phân tích cung: {str(e)})\n"

            else:
                # FALLBACK: Calculate fresh from current time
                try:
                    from qmdg_calc import calculate_qmdg_params
                    now = datetime.datetime.now()
                    params = calculate_qmdg_params(now)
                    def safe(k): return str(params.get(k, '?'))
                    t_tru = f"{safe('can_nam')} {safe('chi_nam')} / {safe('can_thang')} {safe('chi_thang')} / {safe('can_ngay')} {safe('chi_ngay')} / {safe('can_gio')} {safe('chi_gio')}"
                    
                    info += (
                        f"=== [1] KỲ MÔN ĐỘN GIÁP (Thời gian thực) ===\n"
                        f"Tứ Trụ: {t_tru}\n"
                        f"Tiết Khí: {safe('tiet_khi')} | Cục: {safe('cuc')}\n"
                        f"Trực Phù: {safe('truc_phu')} | Trực Sử: {safe('truc_su')}\n"
                    )
                    # Store for Thiết Bản later
                    qmdg_input = params
                except Exception as e:
                    info += f"=== [1] KỲ MÔN ĐỘN GIÁP ===\n⚠️ Lỗi tính: {e}\n"
            
            # ============================================
            # PART 2: MAI HOA DỊCH SỐ
            # ============================================
            if not mai_hoa_data:
                # Auto-generate from session or time
                try:
                    if hasattr(st, 'session_state') and 'mai_hoa_result' in st.session_state:
                        mai_hoa_data = st.session_state.mai_hoa_result
                except: pass
            
            if not mai_hoa_data:
                # Calculate fresh
                try:
                    from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, giai_qua
                    now = datetime.datetime.now()
                    mai_hoa_data = tinh_qua_theo_thoi_gian(now.year, now.month, now.day, now.hour)
                    mai_hoa_data['interpretation'] = giai_qua(mai_hoa_data, topic)
                except: pass
            
            if mai_hoa_data:
                mh_ten = mai_hoa_data.get('ten', '?')
                mh_tuong = mai_hoa_data.get('tuong', '?')
                mh_nghia = mai_hoa_data.get('nghĩa', mai_hoa_data.get('nghia', '?'))
                mh_dong = mai_hoa_data.get('dong_hao', '?')
                mh_upper_e = mai_hoa_data.get('upper_element', '?')
                mh_lower_e = mai_hoa_data.get('lower_element', '?')
                mh_upper_s = mai_hoa_data.get('upper_symbol', '?')
                mh_lower_s = mai_hoa_data.get('lower_symbol', '?')
                mh_bien = mai_hoa_data.get('ten_qua_bien', '?')
                
                # Thể Dụng analysis
                the_dung_note = ""
                if mh_upper_e != '?' and mh_lower_e != '?':
                    the_dung_note = f"Ngoại quái ({mh_upper_e}) vs Nội quái ({mh_lower_e})"
                    # Simple Ngũ Hành check
                    NGU_HANH_order = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"]
                    if mh_upper_e in NGU_HANH_order and mh_lower_e in NGU_HANH_order:
                        i1 = NGU_HANH_order.index(mh_upper_e)
                        i2 = NGU_HANH_order.index(mh_lower_e)
                        diff = (i2 - i1) % 5
                        rel_map = {0: "Tỷ Hòa → TRUNG BÌNH", 1: "Thể sinh Dụng → BỎ SỨC (bất lợi nhẹ)", 2: "Thể khắc Dụng → BẢN THÂN MẠNH (CÁT)", 3: "Dụng khắc Thể → BẢN THÂN BỊ KHẮC (HUNG)", 4: "Dụng sinh Thể → ĐƯỢC HỖ TRỢ (CÁT)"}
                        the_dung_note += f" → {rel_map.get(diff, '?')}"
                
                info += (
                    f"\n=== [2] MAI HOA DỊCH SỐ ===\n"
                    f"Quẻ Chủ: {mh_ten} ({mh_upper_s} / {mh_lower_s})\n"
                    f"Tượng Quẻ: {mh_tuong}\n"
                    f"Ý Nghĩa: {mh_nghia}\n"
                    f"Động Hào: {mh_dong} | Quẻ Biến: {mh_bien}\n"
                    f"Thể Dụng: {the_dung_note}\n"
                    f"→ Thể sinh Dụng = Cát (tốt cho mình), Dụng khắc Thể = Hung (bất lợi).\n"
                )
            else:
                info += f"\n=== [2] MAI HOA DỊCH SỐ ===\n(Chưa có dữ liệu)\n"
            
            # ============================================
            # PART 3: LỤC HÀO KINH DỊCH
            # ============================================
            if not luc_hao_data:
                try:
                    if hasattr(st, 'session_state') and 'luc_hao_result' in st.session_state:
                        luc_hao_data = st.session_state.luc_hao_result
                except: pass
            
            if not luc_hao_data:
                try:
                    from luc_hao_kinh_dich import lap_qua_luc_hao
                    now = datetime.datetime.now()
                    can_ngay_lh = qmdg_input.get('can_ngay', 'Giáp') if qmdg_input else 'Giáp'
                    chi_ngay_lh = qmdg_input.get('chi_ngay', 'Tý') if qmdg_input else 'Tý'
                    luc_hao_data = lap_qua_luc_hao(now.year, now.month, now.day, now.hour, topic=topic, can_ngay=can_ngay_lh, chi_ngay=chi_ngay_lh)
                except: pass
            
            if luc_hao_data:
                ban_info = luc_hao_data.get('ban', {})
                bien_info = luc_hao_data.get('bien', {})
                lh_ten = ban_info.get('name', '?')
                lh_bien = bien_info.get('name', '?')
                lh_palace = ban_info.get('palace', '?')
                lh_conclusion = luc_hao_data.get('conclusion', '?')
                lh_dung_than = luc_hao_data.get('dung_than_label', '?')
                lh_the_ung = luc_hao_data.get('the_ung', '?')
                lh_dong_hao = luc_hao_data.get('dong_hao', [])
                
                info += (
                    f"\n=== [3] LỤC HÀO KINH DỊCH ===\n"
                    f"Quẻ Chủ: {lh_ten} (Họ: {lh_palace}) → Biến: {lh_bien}\n"
                    f"Hào Động: {lh_dong_hao}\n"
                    f"Dụng Thần: {lh_dung_than}\n"
                    f"Thế Ứng: {lh_the_ung}\n"
                )
                
                # Chi tiết 6 hào
                ban_details = ban_info.get('details', [])
                if ban_details:
                    info += "Chi Tiết 6 Hào (Quẻ Chủ):\n"
                    for d in ban_details:
                        hao_num = d.get('hao', '?')
                        luc_than = d.get('luc_than', '?')
                        can_chi = d.get('can_chi', '?')
                        luc_thu = d.get('luc_thu', '?')
                        strength = d.get('strength', '?')
                        is_moving = d.get('is_moving', False)
                        loc_ma = d.get('loc_ma', '')
                        marker = d.get('marker', '')
                        
                        dong_mark = "⚡ĐỘNG" if is_moving else ""
                        info += f"  Hào {hao_num}: {luc_than} | {can_chi} | {luc_thu} | {strength} {dong_mark} {marker} {loc_ma}\n"
                
                info += (
                    f"Kết Luận Sơ Bộ: {lh_conclusion}\n"
                    f"→ Dụng Thần Vượng = CÁT, Dụng Thần Suy/Tuyệt = HUNG.\n"
                )
            else:
                info += f"\n=== [3] LỤC HÀO KINH DỊCH ===\n(Chưa có dữ liệu)\n"
            
            # ============================================
            # PART 4: THIẾT BẢN THẦN TOÁN
            # ============================================
            try:
                tb_data = self._load_thiet_ban_data()
                
                if tb_data and qmdg_input:
                    can_nam_tb = qmdg_input.get('can_nam', '?')
                    chi_nam_tb = qmdg_input.get('chi_nam', '?')
                    can_ngay_tb = qmdg_input.get('can_ngay', '?')
                    chi_ngay_tb = qmdg_input.get('chi_ngay', '?')
                    
                    nam_tru = f"{can_nam_tb} {chi_nam_tb}".strip()
                    ngay_tru = f"{can_ngay_tb} {chi_ngay_tb}".strip()
                    
                    hoa_giap = tb_data.get("LUC_THAP_HOA_GIAP_NAP_AM", {})
                    na_nam_info = hoa_giap.get(nam_tru, {})
                    na_ngay_info = hoa_giap.get(ngay_tru, {})
                    
                    na_nam = na_nam_info.get("Nạp_Âm", "Không rõ")
                    na_nam_hanh = na_nam_info.get("Hành", "?")
                    na_nam_ynhia = na_nam_info.get("Ý_Nghĩa", "")
                    na_ngay = na_ngay_info.get("Nạp_Âm", "Không rõ")
                    na_ngay_hanh = na_ngay_info.get("Hành", "?")
                    na_ngay_ynhia = na_ngay_info.get("Ý_Nghĩa", "")
                    
                    info += (
                        f"\n=== [4] THIẾT BẢN THẦN TOÁN ===\n"
                        f"Mệnh Năm ({nam_tru}): {na_nam} (Hành {na_nam_hanh}) - {na_nam_ynhia}\n"
                        f"Mệnh Ngày ({ngay_tru}): {na_ngay} (Hành {na_ngay_hanh}) - {na_ngay_ynhia}\n"
                    )
                    
                    # Trường Sinh 12 Giai Đoạn - tính cho Hành Ngày tại Chi Ngày
                    truong_sinh = tb_data.get("TRUONG_SINH_12_GIAI_DOAN", {})
                    nh_ts_tai = truong_sinh.get("Ngũ_Hành_Trường_Sinh_Tại", {})
                    giai_doan_map = truong_sinh.get("Giai_Đoạn", {})
                    
                    if na_ngay_hanh != "?" and chi_ngay_tb != "?":
                        hanh_ts = nh_ts_tai.get(na_ngay_hanh, {})
                        current_stage = None
                        for stage_name, chi_val in hanh_ts.items():
                            if chi_val == chi_ngay_tb:
                                current_stage = stage_name.replace("_", " ")
                                break
                        
                        if current_stage:
                            gd_info = giai_doan_map.get(current_stage, {})
                            info += f"Trường Sinh Ngày: {current_stage} (Mức {gd_info.get('Mức', '?')}/10) - {gd_info.get('Luận', '?')}\n"
                    
                    # Thần Sát lookup cho Can Ngày
                    than_sat = tb_data.get("THAN_SAT_LOOKUP", {})
                    relevant_sats = []
                    for sat_name, sat_info in than_sat.items():
                        cach_an = sat_info.get("Cách_An", "")
                        if can_ngay_tb in cach_an or chi_ngay_tb in cach_an:
                            relevant_sats.append(f"{sat_name.replace('_', ' ')} ({sat_info.get('Loại', '?')}): {sat_info.get('Tác_Dụng', '?')}")
                    
                    if relevant_sats:
                        info += "Thần Sát liên quan:\n"
                        for sat in relevant_sats[:3]:  # Max 3
                            info += f"  - {sat}\n"
                    
                    # Phục Ngâm / Phản Ngâm check
                    pn_data = tb_data.get("PHUC_NGAM_PHAN_NGAM", {})
                    info += f"→ LƯU Ý: Kiểm tra Phục Ngâm/Phản Ngâm (Sao/Môn lâm cung gốc/đối diện = trì trệ/phản bội).\n"
                    
                    # Quy tắc nâng cao
                    quy_tac = tb_data.get("QUY_TAC_LUAN_DOAN_NANG_CAO", {})
                    if quy_tac:
                        ngu_bat = quy_tac.get("Ngũ_Bất_Ngộ_Thời", {})
                        if ngu_bat:
                            info += f"→ Ngũ Bất Ngộ Thời (5 trường hợp xấu): {'; '.join(ngu_bat.get('Quy_Tắc', []))}\n"
                    
                else:
                    info += f"\n=== [4] THIẾT BẢN THẦN TOÁN ===\n(Không có dữ liệu Tứ Trụ để tra cứu)\n"
                    
            except Exception as e:
                info += f"\n=== [4] THIẾT BẢN THẦN TOÁN ===\n(Lỗi: {e})\n"
            # ============================================
            # PART 5: MANG ĐOÁN - PRE-COMPUTED READINGS
            # ============================================
            try:
                from blind_reading import blind_read, format_blind_reading
                readings = blind_read(
                    chart_data=qmdg_input, 
                    mai_hoa_data=mai_hoa_data, 
                    luc_hao_data=luc_hao_data
                )
                blind_text = format_blind_reading(readings)
                if blind_text:
                    info += f"\n{blind_text}\n"
            except Exception as e:
                info += f"\n(Lỗi Mang Đoán: {e})\n"
            
            return info
            
        except Exception as e:
            return f"⚠️ Lỗi tính toán dữ liệu nền: {str(e)}"

    def _load_thiet_ban_data(self):
        """Load Thiết Bản Thần Toán from JSON file or qmdg_data."""
        # Try JSON file first
        try:
            import os
            json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thiet_ban_than_toan.json")
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except: pass
        
        # Fallback to qmdg_data
        try:
            from qmdg_data import KY_MON_DATA
            return KY_MON_DATA.get("THIET_BAN_THAN_TOAN", {})
        except: pass
        
        return {}

    def _get_chat_history(self):
        try:
            if hasattr(st, 'session_state') and 'chat_history' in st.session_state:
                hist = st.session_state.chat_history[-4:]
                return "\\n".join([f"- {m['role']}: {m['content'][:50]}..." for m in hist])
        except: pass
        return "(Không có)"

    def _process_response(self, text):
        match_thinking = re.search(r'\[SUY_LUAN\](.*?)(\[/SUY_LUAN\]|$)', text, re.DOTALL | re.IGNORECASE)
        answer = text
        thinking = ""
        
        if match_thinking:
            thinking = match_thinking.group(1).strip()
            answer = text.replace(match_thinking.group(0), "").strip()
            
            # Display Thinking
            st.markdown("""
            <style>
            .ag-thinking-box {
                background: #f8f9fa; 
                border-left: 4px solid #4a90e2;
                padding: 10px;
                font-size: 0.9em;
                color: #555;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)
            with st.expander("⚡ Tư Duy Tiên Tri (Click để xem)", expanded=False):
                st.markdown(f'<div class="ag-thinking-box">{thinking}</div>', unsafe_allow_html=True)

        match_conclusion = re.search(r'\[KET_LUAN\](.*?)(\[/KET_LUAN\]|$)', answer, re.DOTALL | re.IGNORECASE)
        if match_conclusion:
            answer = match_conclusion.group(1).strip()

        if not answer.strip() and thinking:
             return thinking # Fallback if only thinking exists
             
        return answer

    def render_logs(self):
        """Displays execution logs in a clean UI format."""
        if not self.logs:
            st.caption("*(Chưa có nhật ký hoạt động)*")
            return

        st.markdown("### 📜 Nhật Ký Xử Lý AI")
        for log in self.logs:
            status_icon = "⚪"
            if log['status'] == "RUNNING": status_icon = "🔄"
            elif log['status'] == "SUCCESS" or log['status'] == "COMPLETED": status_icon = "✅"
            elif log['status'] == "ERROR": status_icon = "❌"
            elif log['status'] == "WARNING": status_icon = "⚠️"
            
            with st.expander(f"{status_icon} {log['step']} ({log['time']})"):
                st.write(f"**Chi tiết:** {log['detail']}")
                if log['status'] == "ERROR":
                    st.error(log['detail']) 

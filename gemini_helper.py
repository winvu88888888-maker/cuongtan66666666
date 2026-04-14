"""
Enhanced Gemini Helper - THIÊN CƠ ĐẠI SƯ (V20.0 - Siêu Trí Tuệ Thông Minh Nhất)
Python Pre-Analysis Engine + 12-Step CoT + Deep Reasoning + Tam Tài + Contradiction Resolution
Lục Thuật Hợp Nhất: Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản + Đại Lục Nhâm + Thái Ất + Mang Đoán + Vạn Vật
"""

from google import genai
from google.genai import types as genai_types
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
        keys_from_regex = re.findall(r"AIza[0-9A-Za-z-_]{35,}", str(api_key_input))
        raw_text = str(api_key_input).replace("\n", ",").replace(";", ",")
        keys_from_split = [k.strip() for k in raw_text.split(',') if len(k.strip()) > 30 and "AIza" in k]
        all_candidates = keys_from_regex + keys_from_split
        self.api_keys = list(dict.fromkeys(all_candidates)) 
        self.api_keys = [k for k in self.api_keys if len(k) > 30]

        self.current_key_index = 0
        self.api_key = self.api_keys[0] if self.api_keys else None
        
        self.version = "V21.0-GenAI-SDK"
        # V21.0: Khởi tạo Client mới (google-genai SDK)
        self._client = None
        if self.api_key:
            self._client = genai.Client(api_key=self.api_key)
        
        self._failed_models = set()
        self._hashlib = hashlib
        self.max_retries = 2
        self.base_delay = 1
        self.n8n_url = None
        self.n8n_timeout = 8
        self.logs = [] 

        self.model_name = "gemini-2.5-pro"  # V31.2: Best available, fallback to 3.1/flash
        self.model = None  # V21.0: Không cần model object, dùng client.models
        self.fallback_helper = FreeAIHelper()

    def _get_best_model_placeholder(self):
        return None  # V21.0: Không cần placeholder, dùng client.models

    def log_step(self, step, status, detail):
        self.logs.append({
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "step": step,
            "status": status,
            "detail": detail
        })

    def test_connection(self):
        try:
            if not self._client:
                return False, "Chưa có API Key!"
            
            valid_models = []
            try:
                available = list(self._client.models.list())
                for m in available:
                    valid_models.append(m.name)
            except Exception as e:
                return False, f"Lỗi liệt kê model: {str(e)}"

            if not valid_models:
                return False, "Key không có quyền truy cập model nào!"

            # V31.4: SMART BILLING DETECT — Auto-detect paid models
            model_names_short = [m.split('/')[-1] if '/' in m else m for m in valid_models]
            
            # Check: có model PAID trong danh sách? → có billing
            has_billing = any('3.1-pro' in mn or '3.0-pro' in mn for mn in model_names_short)
            
            if has_billing:
                # CÓ BILLING → ưu tiên model mạnh nhất (PAID)
                priority_order = [
                    'gemini-3.1-pro-preview',      # 🏆 BEST — Thế hệ mới nhất, suy luận siêu sâu
                    'gemini-2.5-pro',              # Rất tốt — sâu, ổn định
                    'gemini-2.5-flash',            # Nhanh — fallback
                    'gemini-2.5-flash-lite',       # Nhẹ — fallback
                    'gemini-1.5-pro',              # Legacy Pro
                    'gemini-1.5-flash',            # Legacy
                ]
                tier_label = "💎 PREMIUM (Billing Active)"
            else:
                # KHÔNG BILLING → chỉ dùng FREE models
                priority_order = [
                    'gemini-2.5-pro',              # 🏆 FREE — Suy luận sâu nhất
                    'gemini-2.5-flash',            # FREE — Nhanh, quota cao
                    'gemini-2.5-flash-lite',       # FREE — Nhẹ nhất
                    'gemini-1.5-flash',            # FREE — Legacy
                ]
                tier_label = "🆓 FREE Tier"
            
            # Find best available model
            first_match = None
            for model_alias in priority_order:
                if any(model_alias in mn for mn in model_names_short):
                    first_match = model_alias
                    break
            
            if first_match:
                self.model_name = first_match
                # V31.4: Update cascade_models theo billing
                self.cascade_models = priority_order
                return True, f"Kết nối OK! ({first_match}) — {tier_label}"
            else:
                fallback = model_names_short[0] if model_names_short else 'gemini-2.0-flash'
                self.model_name = fallback
                return True, f"Kết nối OK! ({fallback})"

        except Exception as e:
            return False, f"Lỗi kết nối: {str(e)}"

    def set_n8n_url(self, url):
        self.n8n_url = url

    # --- CORE: CALL AI RAW ---
    def _call_ai_raw(self, prompt):
        # V21.0: google-genai SDK — safety settings via types
        safety_settings = [
            genai_types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_NONE'),
            genai_types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_NONE'),
            genai_types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_NONE'),
            genai_types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
        ]

        # V31.3: Model cascade — FREE first, PAID last
        if not hasattr(self, 'cascade_models') or not self.cascade_models:
            self.cascade_models = [
                'gemini-2.5-pro',                  # FREE tier — Suy luận sâu nhất
                'gemini-2.5-flash',                # FREE — Nhanh, quota cao
                'gemini-2.5-flash-lite',           # FREE — Nhẹ nhất
                'gemini-1.5-flash',                # FREE — Legacy
                'gemini-3.1-pro-preview',          # PAID — Chỉ khi có billing
                'gemini-1.5-pro',                  # PAID — Legacy Pro
            ]

        error_log = []

        # KEY ROTATION & MODEL CASCADE
        for current_api_key in self.api_keys:
            try:
                client = genai.Client(api_key=current_api_key)
            except Exception:
                continue

            for model_name in self.cascade_models:
                # V21.0: Thử TẤT CẢ model — mỗi model có quota RIÊNG!
                try:
                    gen_config = genai_types.GenerateContentConfig(
                        temperature=0.15,         # V29.2: Giảm mạnh — bám sát data 100%, CẤM sáng tạo/bịa
                        top_p=0.7,                # V29.2: Thu hẹp tối đa — chỉ chọn từ ngữ chính xác nhất
                        top_k=20,                 # V29.2: Giảm mạnh — bám sát data, không suy diễn
                        max_output_tokens=8192,   # V30.0: Giảm từ 65536 → buộc Gemini viết TẬP TRUNG, không lan man
                        safety_settings=safety_settings,
                    )
                    resp = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=gen_config,
                    )

                    # V14.0: Fix parsing cho thinking models (gemini-2.5-flash)
                    # Thinking model trả về nhiều parts: thought (suy nghĩ nội bộ) + text (câu trả lời)
                    text = ""
                    try:
                        text = resp.text
                    except Exception:
                        pass
                    
                    # Nếu resp.text rỗng → trích xuất từ tất cả parts (bỏ thought)
                    if not text and resp.candidates:
                        parts = resp.candidates[0].content.parts if resp.candidates[0].content else []
                        for p in parts:
                            # Bỏ thought parts — chỉ lấy text parts
                            is_thought = getattr(p, 'thought', False)
                            if not is_thought and hasattr(p, 'text') and p.text:
                                text += p.text

                    if text and len(text.strip()) > 1:
                        self.model_name = model_name
                        return text

                    error_log.append(f"{model_name}: Phản hồi rỗng/bị chặn")

                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str:
                        error_log.append(f"{model_name}: ⏳ Hết quota — thử model khác...")
                        time.sleep(0.5)  # V13.0: Giảm wait, thử model tiếp ngay
                    elif "404" in error_str or "not found" in error_str.lower():
                        error_log.append(f"{model_name}: ❌ Model không khả dụng.")
                    elif "API_KEY_INVALID" in error_str or "expired" in error_str.lower():
                        error_log.append(f"{model_name}: 🔑 Key không hợp lệ!")
                        break  # Key lỗi hoàn toàn → skip key này
                    else:
                        error_log.append(f"{model_name}: {error_str[:80]}...")
                    continue

        # === FALLBACK: Nếu tất cả Gemini model đều lỗi ===
        error_summary = " | ".join(error_log[:3]) if error_log else "Không có model khả dụng"
        self._last_error_log = error_summary  # V13.0: Lưu lỗi để hiện cho user
        
        # V10.0: Kiểm tra xem prompt có phải là refine_prompt (đã có offline result) hay không
        # Nếu là refine → KHÔNG chạy lại offline (tránh lặp đôi + prompt leak)
        is_refine_prompt = "KẾT QUẢ PHÂN TÍCH OFFLINE" in prompt or "THIÊN CƠ ĐẠI SƯ" in prompt[:200]
        
        if is_refine_prompt:
            # Refine mode: Chỉ trả lỗi, KHÔNG chạy offline lần 2
            return None  # app.py sẽ xử lý None = không có online
        
        # Chỉ fallback offline khi gọi từ answer_question() (không phải refine)
        try:
            short_question = ""
            import re
            match = re.search(r'<user_question>(.*?)</user_question>', prompt, re.DOTALL)
            if match:
                short_question = match.group(1).strip()
            else:
                # Lấy dòng đầu tiên sau "Câu hỏi:" nếu có
                match2 = re.search(r'Câu hỏi[:\s]+(.+?)[\n\r]', prompt)
                if match2:
                    short_question = match2.group(1).strip()
                else:
                    short_question = prompt[:200]  # Fallback an toàn

            _chart = None
            _mai_hoa = None
            _luc_hao = None
            try:
                import streamlit as st
                _chart = st.session_state.get('chart_data')
                _mai_hoa = st.session_state.get('mai_hoa_result')
                _luc_hao = st.session_state.get('luc_hao_result')
            except Exception:
                pass

            offline_response = self.fallback_helper.answer_question(
                short_question,
                chart_data=_chart,
                mai_hoa_data=_mai_hoa,
                luc_hao_data=_luc_hao
            )
            return (
                f"⚠️ **AI Online không khả dụng.** Lý do chính: {error_summary}\n\n"
                f"🤖 **Đây là phân tích từ AI Offline (rule-based):**\n\n{offline_response}\n\n"
                f"💡 *Để dùng AI thông minh (Gemini), hãy nhập một API Key mới tại [Google AI Studio](https://aistudio.google.com/app/apikey).*"
            )
        except Exception as fallback_err:
            return f"🛑 **AI lỗi:** {error_summary}"

    def _call_ai(self, prompt, **kwargs):
        return self._call_ai_raw(prompt)

    # ================================================================
    # V20.5: OFFLINE VERDICT SUMMARY BUILDER
    # ================================================================
    def _build_offline_verdict_summary(self, live_context):
        """V20.5: Extract pre-computed verdicts from context and build a summary
        that forces the AI to explain/follow these verdicts rather than re-compute."""
        if not live_context:
            return "(Không có dữ liệu offline)"
        
        verdicts = []
        import re
        
        # Extract VERDICT lines from context
        verdict_patterns = [
            r'VERDICT\s+(?:KỲ MÔN|LỤC HÀO|MAI HOA|LỤC NHÂM|THÁI ẤT)[:\s]*(.+)',
            r'KẾT LUẬN[:\s]*(CÁT|HUNG|ĐẠI CÁT|ĐẠI HUNG|BÌNH|TRUNG BÌNH)',
            r'CROSS-METHOD VERDICT[:\s]*(.+)',
        ]
        
        for pattern in verdict_patterns:
            matches = re.findall(pattern, str(live_context), re.IGNORECASE)
            for m in matches:
                verdicts.append(m.strip())
        
        # Extract specific analysis markers
        summary_parts = []
        
        # Kỳ Môn
        if 'BẢN THÂN BỊ KHẮC (HUNG)' in live_context:
            summary_parts.append("KỲ MÔN: HUNG — Bản thân bị khắc")
        elif 'BẢN THÂN KHẮC CHẾ ĐỐI PHƯƠNG (CÁT)' in live_context:
            summary_parts.append("KỲ MÔN: CÁT — Bản thân khắc chế đối phương")
        elif 'BẢN THÂN ĐƯỢC HỖ TRỢ' in live_context:
            summary_parts.append("KỲ MÔN: CÁT — Bản thân được hỗ trợ")
        elif 'VƯỢNG (đắc địa' in live_context:
            summary_parts.append("KỲ MÔN: CÁT — Can Ngày VƯỢNG đắc địa")
        elif 'TỬ (bị khắc' in live_context:
            summary_parts.append("KỲ MÔN: HUNG — Can Ngày TỬ bị khắc")
        
        # Lục Hào markers
        if 'ĐẠI CÁT' in live_context and 'Nguyên Thần VƯỢNG + ĐỘNG' in live_context:
            summary_parts.append("LỤC HÀO: ĐẠI CÁT — Nguyên Thần VƯỢNG ĐỘNG sinh DT")
        elif 'ĐẠI HUNG' in live_context and 'Kỵ Thần VƯỢNG + ĐỘNG' in live_context:
            summary_parts.append("LỤC HÀO: ĐẠI HUNG — Kỵ Thần VƯỢNG ĐỘNG khắc DT")
        elif 'NHẬT THẦN' in live_context and 'SINH DT' in live_context:
            summary_parts.append("LỤC HÀO: CÁT — Nhật Thần sinh DT")
        elif 'NHẬT THẦN' in live_context and 'KHẮC DT' in live_context:
            summary_parts.append("LỤC HÀO: HUNG — Nhật Thần khắc DT")
        
        # Mai Hoa
        if 'Thể khắc Dụng → BẢN THÂN MẠNH (CÁT)' in live_context:
            summary_parts.append("MAI HOA: CÁT — Thể khắc Dụng")
        elif 'Dụng khắc Thể → BẢN THÂN BỊ KHẮC (HUNG)' in live_context:
            summary_parts.append("MAI HOA: HUNG — Dụng khắc Thể")
        elif 'Dụng sinh Thể → ĐƯỢC HỖ TRỢ (CÁT)' in live_context:
            summary_parts.append("MAI HOA: CÁT — Dụng sinh Thể")
        
        # Build summary
        result = "╔══════════════════════════════════════════╗\n"
        result += "║  📊 OFFLINE VERDICT SUMMARY (Python)     ║\n"
        result += "║  ⛔ AI PHẢI tuân theo verdict này        ║\n"
        result += "╚══════════════════════════════════════════╝\n"
        
        if summary_parts:
            for sp in summary_parts:
                result += f"→ {sp}\n"
        
        if verdicts:
            result += "\n[VERDICT GỐC từ Pre-Analysis Engine]:\n"
            for v in verdicts[:6]:
                result += f"• {v}\n"
        
        if not summary_parts and not verdicts:
            result += "→ Không có verdict rõ ràng — AI phân tích dựa trên PRE-ANALYSIS data.\n"
        
        return result

    # ================================================================
    # CORE: ANSWER QUESTION (THE BRAIN) - V20.5 GROUNDED
    # ================================================================
    def answer_question(self, question, chart_data=None, topic="Chung", selected_subject=None, mai_hoa_data=None, luc_hao_data=None): 
        """
        V28.4: Route direct AI Online calls through FreeAIHelper 
        to ensure all deterministic Offline logic and weighted score 
        data are passed into Gemini's context.
        """
        self.logs = [] # Reset logs
        try:
            from free_ai_helper import FreeAIHelper
            offline_ai = FreeAIHelper(api_key=self.api_key)
            return offline_ai.answer_question(
                question=question,
                chart_data=chart_data,
                topic=topic,
                selected_subject=selected_subject,
                mai_hoa_data=mai_hoa_data,
                luc_hao_data=luc_hao_data
            )
        except Exception as e:
            return f"❌ Lỗi Tích Hợp AI: {str(e)}"

    # ================================================================
    # PARANOID CONTEXT BUILDER - V5.0 TIÊN TRI FULL 6 METHODS
    # ================================================================
    def _get_paranoid_context(self, qmdg_input, topic="Chung", question="", selected_subject=None, mai_hoa_data=None, luc_hao_data=None):
        """Builds comprehensive context from ALL 4 divination methods."""
        try:
            info = ""
            # VẠN VẬT LOẠI TƯỢNG DATA
            vv_info = ""
            
            try:
                from van_vat_loai_tuong import get_ngu_hanh_tuong, get_bat_quai_tuong
            except ImportError:
                def get_ngu_hanh_tuong(h): return ""
                def get_bat_quai_tuong(q): return ""

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
                
                # V14.0: TUẦN KHÔNG TỨ TRỤ + DỊCH MÃ + TỨ TRỤ Ý NGHĨA
                try:
                    _CAN = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                    _CHI = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                    _TK_MAP = {'Giáp Tý':['Tuất','Hợi'],'Giáp Tuất':['Thân','Dậu'],'Giáp Thân':['Ngọ','Mùi'],
                               'Giáp Ngọ':['Thìn','Tị'],'Giáp Thìn':['Dần','Mão'],'Giáp Dần':['Tý','Sửu']}
                    _DICH_MA = {'Thân':'Dần','Tý':'Dần','Thìn':'Dần','Dần':'Thân','Ngọ':'Thân','Tuất':'Thân',
                                'Tị':'Hợi','Dậu':'Hợi','Sửu':'Hợi','Hợi':'Tị','Mão':'Tị','Mùi':'Tị'}
                    _CAN_NGH = {'Giáp':'Mộc-Dương','Ất':'Mộc-Âm','Bính':'Hỏa-Dương','Đinh':'Hỏa-Âm',
                                'Mậu':'Thổ-Dương','Kỷ':'Thổ-Âm','Canh':'Kim-Dương','Tân':'Kim-Âm',
                                'Nhâm':'Thủy-Dương','Quý':'Thủy-Âm'}
                    _CHI_NGH = {'Tý':'Thủy-Dương','Sửu':'Thổ-Âm','Dần':'Mộc-Dương','Mão':'Mộc-Âm',
                                'Thìn':'Thổ-Dương','Tị':'Hỏa-Âm','Ngọ':'Hỏa-Dương','Mùi':'Thổ-Âm',
                                'Thân':'Kim-Dương','Dậu':'Kim-Âm','Tuất':'Thổ-Dương','Hợi':'Thủy-Âm'}
                    
                    def _calc_tk(can, chi):
                        if can not in _CAN or chi not in _CHI: return []
                        gi = (_CHI.index(chi) - _CAN.index(can)) % 12
                        return _TK_MAP.get(f'Giáp {_CHI[gi]}', [])
                    
                    chi_ngay = qmdg_input.get('chi_ngay', '?')
                    chi_gio = qmdg_input.get('chi_gio', '?')
                    chi_thang = qmdg_input.get('chi_thang', '?')
                    chi_nam = qmdg_input.get('chi_nam', '?')
                    
                    # --- TUẦN KHÔNG TỨ TRỤ ---
                    tk_ngay = _calc_tk(can_ngay, chi_ngay)
                    tk_gio = _calc_tk(can_gio, chi_gio) if can_gio in _CAN and chi_gio in _CHI else []
                    tk_thang = _calc_tk(can_thang, chi_thang) if can_thang in _CAN and chi_thang in _CHI else []
                    tk_nam = _calc_tk(can_nam, chi_nam) if can_nam in _CAN and chi_nam in _CHI else []
                    
                    tk_info = "\n[TUẦN KHÔNG TỨ TRỤ (空亡) — Chi lâm Tuần Không = HƯ ẢO, KHÔNG CÓ THẬT, sự việc TRỐNG RỖNG]\n"
                    tk_info += f"★ Không Ngày: {', '.join(tk_ngay) if tk_ngay else '?'} — (Tuần {can_ngay} {chi_ngay}) → Hào/Chi nào là {', '.join(tk_ngay)} thì KHÔNG CÓ THẬT\n"
                    tk_info += f"★ Không Giờ: {', '.join(tk_gio) if tk_gio else '?'} — (Tuần {can_gio} {chi_gio})\n"
                    tk_info += f"★ Không Tháng: {', '.join(tk_thang) if tk_thang else '?'} — (Tuần {can_thang} {chi_thang})\n"
                    tk_info += f"★ Không Năm: {', '.join(tk_nam) if tk_nam else '?'} — (Tuần {can_nam} {chi_nam})\n"
                    
                    # Check Chi Giờ / Chi Ngày lâm Tuần Không
                    if chi_gio in tk_ngay:
                        tk_info += f"⛔ Chi Giờ ({chi_gio}) LÂM TUẦN KHÔNG NGÀY → SỰ VIỆC HƯ ẢO, KHÔNG CÓ THẬT!\n"
                    if chi_ngay in tk_thang:
                        tk_info += f"⚠️ Chi Ngày ({chi_ngay}) LÂM TUẦN KHÔNG THÁNG → Bản thân bị ảnh hưởng!\n"
                    if chi_ngay in tk_nam:
                        tk_info += f"⚠️ Chi Ngày ({chi_ngay}) LÂM TUẦN KHÔNG NĂM → Nền tảng không vững!\n"
                    if chi_gio in tk_thang:
                        tk_info += f"⚠️ Chi Giờ ({chi_gio}) LÂM TUẦN KHÔNG THÁNG → Sự việc bị Lệnh Tháng phủ nhận!\n"
                    
                    # V14.0: Check Lục Hào Dụng Thần Chi vs Tuần Không
                    try:
                        if luc_hao_data:
                            ban_details = luc_hao_data.get('ban', {}).get('details', [])
                            for hao in ban_details:
                                hao_chi = str(hao.get('can_chi', '')).split('-')[0] if '-' in str(hao.get('can_chi', '')) else ''
                                # Extract Chi from format like "Mão-Mộc" or "Hợi-Thủy"
                                if not hao_chi:
                                    cc = str(hao.get('can_chi', ''))
                                    for c in _CHI:
                                        if c in cc:
                                            hao_chi = c
                                            break
                                if hao_chi and hao_chi in tk_ngay:
                                    luc_thu = hao.get('luc_thu', '?')
                                    marker = hao.get('marker', '')
                                    tk_info += f"⛔ HÀO {hao.get('hao','?')} ({luc_thu} {hao.get('can_chi','?')}) {marker} LÂM TUẦN KHÔNG NGÀY → HÀO NÀY KHÔNG CÓ LỰC!\n"
                                    if 'Thê Tài' in str(luc_thu):
                                        tk_info += f"   → THÊ TÀI (tài sản) LÂM TUẦN KHÔNG = TÀI SẢN KO MẤT / KO CÓ THẬT!\n"
                                    if 'Quan Quỷ' in str(luc_thu):
                                        tk_info += f"   → QUAN QUỶ (bệnh/việc) LÂM TUẦN KHÔNG = BỆNH KO NGUY / VIỆC KO CÓ!\n"
                                    if 'Tử Tôn' in str(luc_thu):
                                        tk_info += f"   → TỬ TÔN LÂM TUẦN KHÔNG = KO CÓ SỰ BẢO HỘ!\n"
                    except Exception:
                        pass
                    
                    info += tk_info
                    
                    # --- DỊCH MÃ TỨ TRỤ ---
                    _DM_CUC = {'Dần': 'Thân Tý Thìn (Thủy cục)', 'Thân': 'Dần Ngọ Tuất (Hỏa cục)',
                               'Hợi': 'Tị Dậu Sửu (Kim cục)', 'Tị': 'Hợi Mão Mùi (Mộc cục)'}
                    dm_ngay = _DICH_MA.get(chi_ngay, '?')
                    dm_gio = _DICH_MA.get(chi_gio, '?')
                    dm_thang = _DICH_MA.get(chi_thang, '?')
                    dm_nam = _DICH_MA.get(chi_nam, '?')
                    
                    dm_info = "\n[DỊCH MÃ TỨ TRỤ (驿马) — Dịch Mã = DI CHUYỂN, biến động, xuất hành, KHÔNG YÊN TẠI CHỖ]\n"
                    dm_info += f"★ Dịch Mã Ngày: {dm_ngay} (Chi Ngày {chi_ngay} thuộc {_DM_CUC.get(dm_ngay, '?')})\n"
                    dm_info += f"★ Dịch Mã Giờ: {dm_gio} (Chi Giờ {chi_gio} thuộc {_DM_CUC.get(dm_gio, '?')})\n"
                    dm_info += f"★ Dịch Mã Tháng: {dm_thang} (Chi Tháng {chi_thang})\n"
                    dm_info += f"★ Dịch Mã Năm: {dm_nam} (Chi Năm {chi_nam})\n"
                    dm_info += f"→ Ý nghĩa: Hào/Chi nào trùng Dịch Mã = có DI CHUYỂN, THAY ĐỔI. DM+Cát=đi xa tốt. DM+Hung=bỏ chạy.\n"
                    
                    # Check: Chi nào trong Tứ Trụ trùng Dịch Mã?
                    all_chi_tru = {'Ngày': chi_ngay, 'Giờ': chi_gio, 'Tháng': chi_thang, 'Năm': chi_nam}
                    all_dm = [dm_ngay, dm_gio, dm_thang, dm_nam]
                    for tru_name, tru_chi in all_chi_tru.items():
                        if tru_chi in all_dm and tru_chi != '?':
                            dm_info += f"⚡ Chi {tru_name} ({tru_chi}) TRÙNG DỊCH MÃ → {tru_name} có BIẾN ĐỘNG, di chuyển!\n"
                    
                    # Check Lục Hào DT vs Dịch Mã
                    try:
                        if luc_hao_data:
                            ban_details = luc_hao_data.get('ban', {}).get('details', [])
                            for hao in ban_details:
                                cc = str(hao.get('can_chi', ''))
                                hao_chi = ''
                                for c in _CHI:
                                    if c in cc:
                                        hao_chi = c
                                        break
                                if hao_chi and hao_chi == dm_ngay:
                                    luc_thu = hao.get('luc_thu', '?')
                                    dm_info += f"⚡ HÀO {hao.get('hao','?')} ({luc_thu} {cc}) TRÙNG DỊCH MÃ NGÀY → Hào này có tính DI CHUYỂN!\n"
                    except Exception:
                        pass
                    
                    info += dm_info
                    
                    # --- LỤC THẦN CHẨN ĐOÁN THẬT/GIẢ ---
                    try:
                        if luc_hao_data:
                            ban_details = luc_hao_data.get('ban', {}).get('details', [])
                            lt_info = ""
                            has_huyen_vu = False
                            has_dang_xa = False
                            
                            for hao in ban_details:
                                luc_than = str(hao.get('luc_than', ''))
                                luc_thu = str(hao.get('luc_thu', ''))
                                marker = str(hao.get('marker', ''))
                                is_moving = hao.get('is_moving', False)
                                hao_num = hao.get('hao', '?')
                                can_chi = hao.get('can_chi', '?')
                                
                                # Huyền Vũ detection
                                if 'Huyền Vũ' in luc_than or 'Huyền' in luc_than:
                                    has_huyen_vu = True
                                    lt_info += f"⛔ HÀO {hao_num} ({luc_thu} {can_chi}) LÂM HUYỀN VŨ (玄武) → DẤU HIỆU GIẢ DỐI/ÁM MUỘI\n"
                                    if 'Thế' in marker:
                                        lt_info += f"   → HUYỀN VŨ LÂM THẾ: Người hỏi KHÔNG THỰC LÒNG hoặc có ẩn ý!\n"
                                    if 'Ứng' in marker:
                                        lt_info += f"   → HUYỀN VŨ LÂM ỨNG: Đối phương GIẢ DỐI, LỪA ĐẢO!\n"
                                    if 'Quan Quỷ' in luc_thu and is_moving:
                                        lt_info += f"   → HUYỀN VŨ + QUAN QUỶ ĐỘNG: MẤT TRỘM THẬT, kẻ gian đã hành động!\n"
                                    if 'Huynh Đệ' in luc_thu and is_moving:
                                        lt_info += f"   → HUYỀN VŨ + HUYNH ĐỆ ĐỘNG: Bị NGƯỜI QUEN lừa gạt tiền!\n"
                                    if 'Thê Tài' in luc_thu:
                                        lt_info += f"   → HUYỀN VŨ + THÊ TÀI: Tiền bạc KHÔNG CHÍNH ĐÁNG!\n"
                                    if 'Phụ Mẫu' in luc_thu:
                                        lt_info += f"   → HUYỀN VŨ + PHỤ MẪU: Văn bản/hợp đồng CÓ GIẢ!\n"
                                
                                # Đằng Xà detection
                                if 'Đằng Xà' in luc_than or 'Đằng' in luc_than:
                                    has_dang_xa = True
                                    lt_info += f"⚠️ HÀO {hao_num} ({luc_thu} {can_chi}) LÂM ĐẰNG XÀ (螣蛇) → HƯ KINH, lo sợ vô căn cứ\n"
                                    if 'Thế' in marker:
                                        lt_info += f"   → ĐẰNG XÀ LÂM THẾ: Bản thân lo lắng VÔ CĂN CỨ, việc KHÔNG THẬT!\n"
                                    if 'Quan Quỷ' in luc_thu and is_moving:
                                        lt_info += f"   → ĐẰNG XÀ + QUAN QUỶ ĐỘNG: Có người GIĂNG BẪY, cần đề phòng!\n"
                                    if 'Phụ Mẫu' in luc_thu:
                                        lt_info += f"   → ĐẰNG XÀ + PHỤ MẪU: Thông tin HƯ GIẢ, tin đồn!\n"
                            
                            if lt_info:
                                info += f"\n[LỤC THẦN CHẨN ĐOÁN THẬT/GIẢ (Python-computed)]\n{lt_info}"
                            
                            if not has_huyen_vu and not has_dang_xa:
                                info += "\n[LỤC THẦN]: Không có Huyền Vũ/Đằng Xà trên DT → KHÔNG có dấu hiệu giả dối rõ ràng.\n"
                    except Exception:
                        pass
                    
                    # --- TỨ TRỤ GIẢI NGHĨA ---
                    tu_tru_info = "\n[TỨ TRỤ GIẢI NGHĨA — Ý nghĩa từng trụ trong Kỳ Môn + Mai Hoa + Kinh Dịch]\n"
                    tru_data = [
                        ('Trụ Năm', can_nam, chi_nam, 'GỐC RỄ — ông bà, xã hội, nền tảng, giai đoạn 1-15 tuổi'),
                        ('Trụ Tháng', can_thang, chi_thang, 'CỬA CHÍNH — cha mẹ, sự nghiệp, LỆNH THÁNG (quan trọng nhất cho vượng suy), 15-30 tuổi'),
                        ('Trụ Ngày', can_ngay, chi_ngay, 'BẢN THÂN — chính mình (Can=ta, Chi=phối ngẫu), tâm tính, 30-45 tuổi'),
                        ('Trụ Giờ', can_gio, chi_gio, 'TƯƠNG LAI — con cái, kết quả cuối cùng, hậu vận, 45+ tuổi'),
                    ]
                    for tru_name, can, chi, y_nghia in tru_data:
                        can_nh = _CAN_NGH.get(can, '?')
                        chi_nh = _CHI_NGH.get(chi, '?')
                        tu_tru_info += f"★ {tru_name}: {can} {chi} ({can_nh} | {chi_nh}) — {y_nghia}\n"
                    info += tu_tru_info
                    
                except Exception:
                    pass
                
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
                        # V12.2: Trong QMDG, Can Giáp ẩn dưới Lục Nghi (六甲遁甲)
                        # Xác định Giáp ẩn dưới can nào dựa trên Tuần
                        if stem_char == 'Giáp':
                            hidden_can = _get_giap_hidden_can(qmdg_input)
                            if hidden_can:
                                for idx, s in ctb.items():
                                    if s == hidden_can: return idx
                        return None
                    
                    def _get_giap_hidden_can(chart):
                        """六甲遁甲: Xác định Giáp ẩn dưới can nào dựa trên Tuần của ngày"""
                        THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
                        DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                        # Lục Giáp → Can ẩn
                        LUC_GIAP_MAP = {
                            'Tý': 'Mậu',    # Giáp Tý tuần → ẩn Mậu
                            'Tuất': 'Kỷ',   # Giáp Tuất tuần → ẩn Kỷ  
                            'Thân': 'Canh',  # Giáp Thân tuần → ẩn Canh
                            'Ngọ': 'Tân',   # Giáp Ngọ tuần → ẩn Tân
                            'Thìn': 'Nhâm', # Giáp Thìn tuần → ẩn Nhâm
                            'Dần': 'Quý',   # Giáp Dần tuần → ẩn Quý
                        }
                        cn = chart.get('can_ngay', '')
                        chn = chart.get('chi_ngay', '')
                        if cn not in THIEN_CAN or chn not in DIA_CHI:
                            return 'Mậu'  # fallback
                        # Tính lùi về Giáp (đầu tuần)
                        can_idx = THIEN_CAN.index(cn)
                        chi_idx = DIA_CHI.index(chn)
                        # Lùi can_idx bước để về Giáp
                        steps_back = can_idx  # vì Giáp ở index 0
                        chi_start = DIA_CHI[(chi_idx - steps_back) % 12]
                        return LUC_GIAP_MAP.get(chi_start, 'Mậu')

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
                    
                    # V12.2: 六甲遁甲 — Hiển thị Can Giáp ẩn ở cung nào
                    if subj_stem == 'Giáp':
                        hidden_can = _get_giap_hidden_can(qmdg_input)
                        ctb = qmdg_input.get('can_thien_ban', {})
                        hidden_palace = None
                        for idx_p, s_p in ctb.items():
                            if s_p == hidden_can:
                                hidden_palace = idx_p
                                break
                        if hidden_palace:
                            info += (
                                f"\n🔮 [六甲遁甲] Can Giáp ẨN dưới Can {hidden_can} → tại Cung {hidden_palace} ({CUNG_NGU_HANH.get(str(hidden_palace), '?')})\n"
                                f"  Sao: {qmdg_input.get('thien_ban',{}).get(hidden_palace,'?')} | "
                                f"Cửa: {qmdg_input.get('nhan_ban',{}).get(hidden_palace,'?')} | "
                                f"Thần: {qmdg_input.get('than_ban',{}).get(hidden_palace,'?')}\n"
                                f"  (Tuần: Giáp {_get_giap_tuan_chi(qmdg_input)} → ẩn {hidden_can})\n"
                            )
                    
                    def _get_giap_tuan_chi(chart):
                        """Trả về Chi đầu tuần (Tý/Tuất/Thân/Ngọ/Thìn/Dần)"""
                        THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
                        DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                        cn = chart.get('can_ngay', '')
                        chn = chart.get('chi_ngay', '')
                        if cn not in THIEN_CAN or chn not in DIA_CHI:
                            return 'Tý'
                        can_idx = THIEN_CAN.index(cn)
                        chi_idx = DIA_CHI.index(chn)
                        return DIA_CHI[(chi_idx - can_idx) % 12]
                    
                    # --- V5.0: CAN CHI NÂNG CAO ---
                    try:
                        chi_ngay = qmdg_input.get('chi_ngay', '')
                        chi_gio = qmdg_input.get('chi_gio', '')
                        chi_thang = qmdg_input.get('chi_thang', '')
                        
                        # Lục Hợp Chi
                        LUC_HOP_CHI = {'Tý': 'Sửu', 'Sửu': 'Tý', 'Dần': 'Hợi', 'Hợi': 'Dần', 'Mão': 'Tuất', 'Tuất': 'Mão', 'Thìn': 'Dậu', 'Dậu': 'Thìn', 'Tỵ': 'Thân', 'Thân': 'Tỵ', 'Ngọ': 'Mùi', 'Mùi': 'Ngọ'}
                        # Lục Xung Chi
                        LUC_XUNG_CHI = {'Tý': 'Ngọ', 'Ngọ': 'Tý', 'Sửu': 'Mùi', 'Mùi': 'Sửu', 'Dần': 'Thân', 'Thân': 'Dần', 'Mão': 'Dậu', 'Dậu': 'Mão', 'Thìn': 'Tuất', 'Tuất': 'Thìn', 'Tỵ': 'Hợi', 'Hợi': 'Tỵ'}
                        # Thiên Can Hợp
                        THIEN_CAN_HOP = {'Giáp': 'Kỷ', 'Kỷ': 'Giáp', 'Ất': 'Canh', 'Canh': 'Ất', 'Bính': 'Tân', 'Tân': 'Bính', 'Đinh': 'Nhâm', 'Nhâm': 'Đinh', 'Mậu': 'Quý', 'Quý': 'Mậu'}
                        # Tam Hợp
                        TAM_HOP = {'Thân': ('Tý', 'Thìn', 'Thủy'), 'Tý': ('Thân', 'Thìn', 'Thủy'), 'Thìn': ('Thân', 'Tý', 'Thủy'), 'Tỵ': ('Dậu', 'Sửu', 'Kim'), 'Dậu': ('Tỵ', 'Sửu', 'Kim'), 'Sửu': ('Tỵ', 'Dậu', 'Kim'), 'Dần': ('Ngọ', 'Tuất', 'Hỏa'), 'Ngọ': ('Dần', 'Tuất', 'Hỏa'), 'Tuất': ('Dần', 'Ngọ', 'Hỏa'), 'Hợi': ('Mão', 'Mùi', 'Mộc'), 'Mão': ('Hợi', 'Mùi', 'Mộc'), 'Mùi': ('Hợi', 'Mão', 'Mộc')}
                        
                        can_chi_analysis = ""
                        
                        # Thiên Can Hợp check
                        if subj_stem and obj_stem and THIEN_CAN_HOP.get(subj_stem) == obj_stem:
                            can_chi_analysis += f"★ THIÊN CAN HỢP: {subj_stem} hợp {obj_stem} → DUYÊN, hợp tác thuận lợi!\n"
                        
                        # Lục Hợp Chi check
                        if chi_ngay and chi_gio:
                            if LUC_HOP_CHI.get(chi_ngay) == chi_gio:
                                can_chi_analysis += f"★ LỤC HỢP CHI: {chi_ngay} hợp {chi_gio} → GẮN KẾT, thuận lợi\n"
                            if LUC_XUNG_CHI.get(chi_ngay) == chi_gio:
                                can_chi_analysis += f"★ LỤC XUNG CHI: {chi_ngay} xung {chi_gio} → XUNG ĐỘT, biến động!\n"
                        
                        # Ngũ Bất Ngộ Thời check
                        if subj_stem and obj_stem and subj_hanh != '?' and obj_hanh != '?':
                            subj_ad = CAN_AM_DUONG.get(subj_stem, '')
                            obj_ad = CAN_AM_DUONG.get(obj_stem, '')
                            KHAC_MAP = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
                            obj_hanh_check = CAN_NGU_HANH.get(obj_stem, '?')
                            if KHAC_MAP.get(obj_hanh_check) == subj_hanh and subj_ad == obj_ad:
                                can_chi_analysis += f"⚠️ NGŨ BẤT NGỘ THỜI: Can Giờ {obj_stem} khắc Can Ngày {subj_stem} (cùng {subj_ad}) → CỰC HUNG!\n"
                        
                        # Tam Hợp check
                        all_chi = [c for c in [chi_ngay, chi_gio, chi_thang] if c]
                        if len(all_chi) >= 2:
                            for c in all_chi:
                                if c in TAM_HOP:
                                    c1, c2, hanh_cuc = TAM_HOP[c]
                                    if c1 in all_chi or c2 in all_chi:
                                        can_chi_analysis += f"★ TAM HỢP: {c} + {c1 if c1 in all_chi else c2} (hướng tới {hanh_cuc} cục)\n"
                                        break
                        
                        if can_chi_analysis:
                            info += f"\n[PHÂN TÍCH CAN CHI NÂNG CAO V5.0]\n{can_chi_analysis}"
                    except:
                        pass
                    
                    # Thêm Vạn Vật Loại Tượng cho Kỳ Môn
                    if subj_idx: vv_info += get_bat_quai_tuong(f"CUNG {subj_idx}") + "\n"
                    if obj_idx and obj_idx != subj_idx: vv_info += get_bat_quai_tuong(f"CUNG {obj_idx}") + "\n"
                    if subj_hanh != '?': vv_info += get_ngu_hanh_tuong(subj_hanh) + "\n"
                    if obj_hanh != '?' and obj_hanh != subj_hanh: vv_info += get_ngu_hanh_tuong(obj_hanh) + "\n"
                    
                    # V20.3: HÌNH TƯỢNG CỬU CUNG KỲ MÔN (Unicode Art)
                    try:
                        thien_ban = qmdg_input.get('thien_ban', {})
                        nhan_ban = qmdg_input.get('nhan_ban', {})
                        than_ban = qmdg_input.get('than_ban', {})
                        
                        CUNG_TEN = {1:'Khảm',2:'Khôn',3:'Chấn',4:'Tốn',5:'Trung',6:'Càn',7:'Đoài',8:'Cấn',9:'Ly'}
                        # Thứ tự hiển thị Cửu Cung (Lạc Thư): 4-9-2 / 3-5-7 / 8-1-6
                        GRID = [[4,9,2],[3,5,7],[8,1,6]]
                        
                        km_visual = []
                        km_visual.append(f"\n【HÌNH TƯỢNG CỬU CUNG KỲ MÔN — AI HÃY NHÌN VÀ CẢM NHẬN】")
                        km_visual.append(f"┌──────────────┬──────────────┬──────────────┐")
                        
                        for row in GRID:
                            line1 = "│"
                            line2 = "│"
                            line3 = "│"
                            for c in row:
                                sao = str(thien_ban.get(c, thien_ban.get(str(c), '?')))[:6]
                                cua = str(nhan_ban.get(c, nhan_ban.get(str(c), '?')))[:6]
                                than = str(than_ban.get(c, than_ban.get(str(c), '?')))[:6]
                                
                                mark = ""
                                if subj_idx and c == subj_idx: mark = "◀CHỦ"
                                elif obj_idx and c == obj_idx: mark = "◀VIỆC"
                                
                                cung_n = CUNG_TEN.get(c, '?')
                                line1 += f" {c}.{cung_n:<5}{mark:>5}│"
                                line2 += f"  ★{sao:<11}│"
                                line3 += f"  ⛩{cua:<5} 🐲{than:<3}│"
                            
                            km_visual.append(line1)
                            km_visual.append(line2)
                            km_visual.append(line3)
                            km_visual.append(f"├──────────────┼──────────────┼──────────────┤")
                        
                        # Replace last separator with bottom border
                        km_visual[-1] = f"└──────────────┴──────────────┴──────────────┘"
                        
                        km_visual.append(f"→ ◀CHỦ = Cung Bản Thân (Can Ngày) | ◀VIỆC = Cung Sự Việc")
                        if subj_idx and obj_idx:
                            dist = abs(subj_idx - obj_idx) if subj_idx and obj_idx else 0
                            if subj_idx == obj_idx:
                                km_visual.append(f"→ CẢM NHẬN: CHỦ và VIỆC CÙNG CUNG — việc NẰM TRONG TẦM TAY")
                            elif dist <= 2:
                                km_visual.append(f"→ CẢM NHẬN: CHỦ và VIỆC GẦN NHAU — dễ tiếp cận, thuận lợi")
                            else:
                                km_visual.append(f"→ CẢM NHẬN: CHỦ và VIỆC XA NHAU — cần nỗ lực nhiều, khó đạt nhanh")
                        
                        info += "\n".join(km_visual) + "\n"
                    except:
                        pass
                        
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
                
                # V20.5 FIX GAP 3: HỖ QUÁI (互卦) — dùng đúng ho_upper/ho_lower đã tính sẵn
                try:
                    QUAI_NUM_HQ = {1:'Càn',2:'Đoài',3:'Ly',4:'Chấn',5:'Tốn',6:'Khảm',7:'Cấn',8:'Khôn'}
                    QUAI_HANH_HQ = {'Càn':'Kim','Đoài':'Kim','Ly':'Hỏa','Chấn':'Mộc','Tốn':'Mộc','Khảm':'Thủy','Cấn':'Thổ','Khôn':'Thổ'}
                    # V20.5: Dùng ho_upper/ho_lower đã tính sẵn thay vì dùng nhầm upper/lower
                    ho_up = mai_hoa_data.get('ho_upper', 0)
                    ho_lo = mai_hoa_data.get('ho_lower', 0)
                    ho_ten = mai_hoa_data.get('ten_ho', '?')
                    if ho_up and ho_lo:
                        ho_upper_n = QUAI_NUM_HQ.get(ho_up, '?')
                        ho_lower_n = QUAI_NUM_HQ.get(ho_lo, '?')
                        ho_upper_h = QUAI_HANH_HQ.get(ho_upper_n, '?')
                        ho_lower_h = QUAI_HANH_HQ.get(ho_lower_n, '?')
                        info += f"HỖ QUÁI (互卦 — diễn biến ẨN): {ho_ten} — Thượng {ho_upper_n}({ho_upper_h}) / Hạ {ho_lower_n}({ho_lower_h})\n"
                        info += f"→ Hỗ Quái cho biết DIỄN BIẾN GIỮA QUÁ TRÌNH, những điều chưa lộ rõ.\n"
                except:
                    pass
                
                # Thêm Vạn Vật Loại Tượng cho Mai Hoa
                if mh_upper_e != '?': vv_info += get_bat_quai_tuong(mh_upper_s.split(' ')[0]) + "\n"
                if mh_lower_e != '?' and mh_lower_s != mh_upper_s: vv_info += get_bat_quai_tuong(mh_lower_s.split(' ')[0]) + "\n"
                
                # V20.3: HÌNH TƯỢNG QUẺ MAI HOA (Unicode Art)
                try:
                    QUAI_LINE = {
                        'Càn': ['━━━','━━━','━━━'], 'Đoài': ['━ ━','━━━','━━━'],
                        'Ly':  ['━━━','━ ━','━━━'], 'Chấn': ['━ ━','━ ━','━━━'],
                        'Tốn': ['━━━','━━━','━ ━'], 'Khảm': ['━ ━','━━━','━ ━'],
                        'Cấn': ['━━━','━ ━','━ ━'], 'Khôn': ['━ ━','━ ━','━ ━']
                    }
                    upper_name = mh_upper_s.split(' ')[0] if mh_upper_s != '?' else ''
                    lower_name = mh_lower_s.split(' ')[0] if mh_lower_s != '?' else ''
                    up_lines = QUAI_LINE.get(upper_name, ['???','???','???'])
                    lo_lines = QUAI_LINE.get(lower_name, ['???','???','???'])
                    
                    is_dong_upper = mh_dong in [4, 5, 6] if isinstance(mh_dong, int) else False
                    the_label = "DỤNG" if is_dong_upper else "THỂ"
                    dung_label = "THỂ" if is_dong_upper else "DỤNG"
                    
                    mh_visual = []
                    mh_visual.append(f"\n【HÌNH TƯỢNG MAI HOA — AI HÃY NHÌN VÀ CẢM NHẬN】")
                    mh_visual.append(f"┌─── {mh_ten} ───┐")
                    mh_visual.append(f"│ ☰ Thượng: {upper_name} ({mh_upper_e}) = {the_label}")
                    for l in up_lines:
                        mh_visual.append(f"│     {l}     │")
                    mh_visual.append(f"│─── ĐỘNG HÀO: {mh_dong} ───│")
                    for l in lo_lines:
                        mh_visual.append(f"│     {l}     │")
                    mh_visual.append(f"│ ☷ Hạ:     {lower_name} ({mh_lower_e}) = {dung_label}")
                    mh_visual.append(f"└──────────────────┘")
                    mh_visual.append(f"→ {the_dung_note}")
                    mh_visual.append(f"→ Quẻ Biến: {mh_bien}")
                    
                    info += "\n".join(mh_visual) + "\n"
                except:
                    pass
                
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
                
                # V20.3: TƯỢNG QUẺ HÌNH ẢNH (Unicode Art) — để AI "nhìn" được quẻ
                try:
                    visual_lines = []
                    visual_lines.append("\n【HÌNH TƯỢNG QUẺ — AI HÃY NHÌN VÀ CẢM NHẬN】")
                    visual_lines.append(f"┌────── {lh_ten} ──────┐    ┌────── {lh_bien} ──────┐")
                    visual_lines.append(f"│    QUẺ CHỦ (BẢN)     │    │    QUẺ BIẾN         │")
                    
                    # Lấy chi tiết 6 hào (từ dưới lên trên)
                    ban_det = ban_info.get('details', [])
                    bien_det = bien_info.get('details', []) if bien_info else []
                    
                    # Vẽ từ hào 6 xuống hào 1
                    for h in range(6, 0, -1):
                        ban_d = ban_det[h-1] if h-1 < len(ban_det) else {}
                        bien_d = bien_det[h-1] if h-1 < len(bien_det) else {}
                        
                        # Quẻ chủ
                        is_moving = ban_d.get('is_moving', False)
                        luc_thu = str(ban_d.get('luc_thu', ''))[:4]
                        can_chi_b = str(ban_d.get('can_chi', ''))
                        marker = str(ban_d.get('marker', ''))
                        
                        # Xác định Âm/Dương
                        chi_part = can_chi_b.split('-')[-1].strip() if '-' in can_chi_b else can_chi_b
                        DUONG_CHI = ['Tý', 'Dần', 'Thìn', 'Ngọ', 'Thân', 'Tuất']
                        is_yang = chi_part in DUONG_CHI
                        
                        if is_yang:
                            ban_line = "━━━━━━━"
                        else:
                            ban_line = "━━━ ━━━"
                        
                        dong_mark = " ⚡" if is_moving else "   "
                        the_ung_m = " ◀THẾ" if "Thế" in marker else (" ◀ỨNG" if "Ứng" in marker else "      ")
                        
                        # Quẻ biến
                        if bien_d:
                            can_chi_v = str(bien_d.get('can_chi', ''))
                            chi_v = can_chi_v.split('-')[-1].strip() if '-' in can_chi_v else can_chi_v
                            is_yang_v = chi_v in DUONG_CHI
                            bien_line = "━━━━━━━" if is_yang_v else "━━━ ━━━"
                        else:
                            bien_line = "       "
                        
                        visual_lines.append(f"│ {h} {ban_line}{dong_mark}{the_ung_m}│    │ {h} {bien_line}       │")
                    
                    visual_lines.append(f"└───────────────────────┘    └──────────────────────┘")
                    
                    # Thêm gợi ý cho AI
                    dong_count = len(lh_dong_hao) if lh_dong_hao else 0
                    tinh_count = 6 - dong_count
                    visual_lines.append(f"→ Hào ĐỘNG: {dong_count} | Hào TĨNH: {tinh_count}")
                    
                    if dong_count == 0:
                        visual_lines.append("→ CẢM NHẬN: Quẻ hoàn toàn TĨNH — tình huống ỔN ĐỊNH, ít biến động")
                    elif dong_count == 1:
                        visual_lines.append(f"→ CẢM NHẬN: ĐỘC PHÁT — Hào {lh_dong_hao[0]} là TÂM ĐIỂM, mọi sự tập trung vào đó")
                    elif dong_count >= 4:
                        visual_lines.append("→ CẢM NHẬN: LOẠN ĐỘNG — tình huống BẤT ỔN, nhiều biến số")
                    else:
                        visual_lines.append(f"→ CẢM NHẬN: {dong_count} hào động — tình huống có thay đổi nhưng còn kiểm soát được")
                    
                    info += "\n".join(visual_lines) + "\n"
                except:
                    pass
                
                # V12.2: Phục Thần (伏神) — Lục Thân ẩn
                phuc_than_data = luc_hao_data.get('phuc_than', [])
                if phuc_than_data:
                    info += "\n[PHỤC THẦN — LỤC THÂN ẨN]:\n"
                    for pt in phuc_than_data:
                        info += (
                            f"  ★ {pt['luc_than']} ({pt['can_chi']}) — ẨN dưới Hào {pt['hao_pos']} "
                            f"({pt['phi_than_luc_than']} {pt['phi_than_can_chi']}) — {pt['strength']}\n"
                        )
                    info += "→ Phục Thần Vượng + Phi Thần yếu = CÓ THỂ LỘ. Phục Thần Suy + Phi Thần mạnh = KHÔNG LỘ.\n"
                
                # Thêm Vạn Vật Loại Tượng cho Lục Hào
                if ban_info and ban_info.get('palace'):
                    vv_info += get_bat_quai_tuong(ban_info.get('palace').replace('Cung ', '').strip()) + "\n"
                    
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
                    
                    # V20.1 FIX 5: Nạp Âm cross-check Ngày vs Năm
                    na_relation = ""
                    if na_nam_hanh != '?' and na_ngay_hanh != '?':
                        _SINH_NA = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
                        _KHAC_NA = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
                        if na_nam_hanh == na_ngay_hanh:
                            na_relation = f"Năm-Ngày TỶ HÒA ({na_nam_hanh}) → Ổn định"
                        elif _SINH_NA.get(na_nam_hanh) == na_ngay_hanh:
                            na_relation = f"Năm ({na_nam_hanh}) SINH Ngày ({na_ngay_hanh}) → CÁT, nền tảng hỗ trợ"
                        elif _SINH_NA.get(na_ngay_hanh) == na_nam_hanh:
                            na_relation = f"Ngày ({na_ngay_hanh}) SINH Năm ({na_nam_hanh}) → Bỏ sức cho nền tảng"
                        elif _KHAC_NA.get(na_nam_hanh) == na_ngay_hanh:
                            na_relation = f"Năm ({na_nam_hanh}) KHẮC Ngày ({na_ngay_hanh}) → HUNG, gốc rễ bất lợi"
                        elif _KHAC_NA.get(na_ngay_hanh) == na_nam_hanh:
                            na_relation = f"Ngày ({na_ngay_hanh}) KHẮC Năm ({na_nam_hanh}) → Bản thân mạnh hơn nền tảng"
                    
                    info += (
                        f"\n=== [4] THIẾT BẢN THẦN TOÁN ===\n"
                        f"Mệnh Năm ({nam_tru}): {na_nam} (Hành {na_nam_hanh}) - {na_nam_ynhia}\n"
                        f"Mệnh Ngày ({ngay_tru}): {na_ngay} (Hành {na_ngay_hanh}) - {na_ngay_ynhia}\n"
                        f"{f'Quan hệ Nạp Âm: {na_relation}' + chr(10) if na_relation else ''}"
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
                    
                    # V20.3: HÌNH TƯỢNG THIẾT BẢN (Unicode Art)
                    try:
                        tb_visual = []
                        tb_visual.append(f"\n【HÌNH TƯỢNG THIẾT BẢN — AI HÃY NHÌN VÀ CẢM NHẬN】")
                        tb_visual.append(f"┌──────────────────────────────────────────┐")
                        tb_visual.append(f"│ 📜 THIẾT BẢN THẦN TOÁN — NẠP ÂM MỆNH   │")
                        tb_visual.append(f"├──────────────────────────────────────────┤")
                        tb_visual.append(f"│ 🏔️ MỆNH NĂM: {na_nam:<10} ({na_nam_hanh:>4}) │")
                        tb_visual.append(f"│   → {na_nam_ynhia:<38}│")
                        tb_visual.append(f"│ 📅 MỆNH NGÀY: {na_ngay:<10} ({na_ngay_hanh:>4}) │")
                        tb_visual.append(f"│   → {na_ngay_ynhia:<38}│")
                        if na_relation:
                            tb_visual.append(f"│ ⚡ {na_relation[:40]:<40}│")
                        # Trường Sinh stage visual
                        if na_ngay_hanh != '?' and chi_ngay_tb != '?':
                            TS_STAGES = ['Trường Sinh','Mộc Dục','Quan Đới','Lâm Quan','Đế Vượng','Suy','Bệnh','Tử','Mộ','Tuyệt','Thai','Dưỡng']
                            cur_s = current_stage if 'current_stage' in dir() and current_stage else '?'
                            tb_visual.append(f"├──────────────────────────────────────────┤")
                            tb_visual.append(f"│ 🔄 TRƯỜNG SINH 12 GIAI ĐOẠN:            │")
                            bar = ""
                            for s in TS_STAGES:
                                if s == cur_s:
                                    bar += f"▶{s[:3]}◀"
                                else:
                                    bar += f" {s[:2]} "
                            tb_visual.append(f"│ {bar[:40]:<40}│")
                        tb_visual.append(f"└──────────────────────────────────────────┘")
                        info += "\n".join(tb_visual) + "\n"
                    except:
                        pass
                    
                else:
                    info += f"\n=== [4] THIẾT BẢN THẦN TOÁN ===\n(Không có dữ liệu Tứ Trụ để tra cứu)\n"
                    
            except Exception as e:
                info += f"\n=== [4] THIẾT BẢN THẦN TOÁN ===\n(Lỗi: {e})\n"
                
            # GỘP VẠN VẬT LOẠI TƯỢNG VÀO INFO
            if vv_info.strip():
                # Lọc trùng lặp để tránh prompt quá dài
                unique_vv = list(set([v for v in vv_info.split('\n\n') if v.strip()]))
                info += "\n=== [TỪ ĐIỂN VẠN VẬT LOẠI TƯỢNG CỦA QUẺ] ===\n"
                info += "(Chỉ dùng thông tin này làm CHẤT LIỆU TƯỢNG QUẺ để trả lời chi tiết hơn, DỰA VÀO ĐÚNG chủ đề người dùng hỏi)\n"
                info += "\n".join(unique_vv) + "\n"
                
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
            
            # ============================================
            # PART 6: V14.0 PRE-ANALYSIS ENGINE (Python-computed)
            # V20.5: Auto-detect Dụng Thần Label trước khi pre-analyze
            # ============================================
            luc_nham_pre = ""
            thai_at_pre = ""
            try:
                # V20.5 FIX GAP 1: Auto-detect dung_than_label từ câu hỏi
                if luc_hao_data and not luc_hao_data.get('dung_than_label'):
                    q_lower = question.lower() if question else ''
                    t_lower = topic.lower() if topic else ''
                    combined = q_lower + ' ' + t_lower
                    if any(k in combined for k in ['tiền', 'tài', 'lãi', 'lỗ', 'đầu tư', 'giá', 'bán', 'mua', 'lương', 'vốn', 'nợ']):
                        luc_hao_data['dung_than_label'] = 'Thê Tài'
                    elif any(k in combined for k in ['bệnh', 'ốm', 'khỏe', 'sức khỏe', 'viện', 'thuốc', 'đau', 'sốt']):
                        luc_hao_data['dung_than_label'] = 'Quan Quỷ'
                    elif any(k in combined for k in ['con', 'sinh', 'bình an', 'vui', 'sướng', 'phúc', 'bảo hộ', 'may mắn']):
                        luc_hao_data['dung_than_label'] = 'Tử Tôn'
                    elif any(k in combined for k in ['nhà', 'xe', 'học', 'thi', 'bằng', 'giấy tờ', 'hợp đồng', 'văn bản', 'sách', 'trường']):
                        luc_hao_data['dung_than_label'] = 'Phụ Mẫu'
                    elif any(k in combined for k in ['sếp', 'quan', 'việc', 'kiện', 'tòa', 'công việc', 'thăng', 'chức', 'cơ quan']):
                        luc_hao_data['dung_than_label'] = 'Quan Quỷ'
                    elif any(k in combined for k in ['yêu', 'vợ', 'chồng', 'tình', 'kết hôn', 'hôn nhân', 'người yêu', 'đám cưới']):
                        luc_hao_data['dung_than_label'] = 'Thê Tài'
                    elif any(k in combined for k in ['bạn', 'đối thủ', 'anh em', 'cạnh tranh']):
                        luc_hao_data['dung_than_label'] = 'Huynh Đệ'
                    else:
                        # Fallback: dùng Thế hào
                        luc_hao_data['dung_than_label'] = '__THE_HAO__'
                
                ky_mon_pre = self._pre_analyze_ky_mon(qmdg_input)
                luc_hao_pre = self._pre_analyze_luc_hao(luc_hao_data)
                mai_hoa_pre = self._pre_analyze_mai_hoa(mai_hoa_data)
                
                if ky_mon_pre: info += ky_mon_pre
                if luc_hao_pre: info += luc_hao_pre
                if mai_hoa_pre: info += mai_hoa_pre
            except Exception as e:
                info += f"\n(Lỗi Pre-Analysis KM/LH/MH: {e})\n"
                ky_mon_pre = ""
                luc_hao_pre = ""
                mai_hoa_pre = ""
            
            # V14.0: ĐẠI LỤC NHÂM PRE-ANALYSIS
            try:
                from dai_luc_nham import tinh_dai_luc_nham, phan_tich_chuyen_sau
                if qmdg_input and isinstance(qmdg_input, dict) and qmdg_input.get('can_ngay'):
                    ln_data = tinh_dai_luc_nham(
                        qmdg_input.get('can_ngay', 'Giáp'),
                        qmdg_input.get('chi_ngay', 'Tý'),
                        qmdg_input.get('chi_gio', 'Ngọ'),
                        qmdg_input.get('tiet_khi', 'Đông Chí')
                    )
                    ln_topic = 'chung'
                    q_lower = question.lower() if question else ''
                    if any(k in q_lower for k in ['tiền', 'tài', 'lãi', 'lỗ', 'đầu tư']): ln_topic = 'tai_chinh'
                    elif any(k in q_lower for k in ['bệnh', 'ốm', 'khỏe', 'sức khỏe']): ln_topic = 'suc_khoe'
                    elif any(k in q_lower for k in ['yêu', 'vợ', 'chồng', 'tình']): ln_topic = 'tinh_cam'
                    elif any(k in q_lower for k in ['tìm', 'mất', 'ở đâu']): ln_topic = 'tim_do'
                    ln_deep = phan_tich_chuyen_sau(ln_data, question, ln_topic)
                    luc_nham_pre = "\n[ĐẠI LỤC NHÂM PRE-ANALYSIS (Python-computed)]\n"
                    tam_truyen = ln_data.get('tam_truyen', {})
                    if tam_truyen:
                        luc_nham_pre += f"Sơ Truyền (QUÁ KHỨ): {tam_truyen.get('so_truyen', '?')} ({tam_truyen.get('so_truyen_hanh', '?')})\n"
                        luc_nham_pre += f"Trung Truyền (HIỆN TẠI): {tam_truyen.get('trung_truyen', '?')} ({tam_truyen.get('trung_truyen_hanh', '?')})\n"
                        luc_nham_pre += f"Mạt Truyền (TƯƠNG LAI): {tam_truyen.get('mat_truyen', '?')} ({tam_truyen.get('mat_truyen_hanh', '?')})\n"
                    for d in ln_deep.get('details', [])[:10]:
                        luc_nham_pre += f"{d}\n"
                    luc_nham_pre += f"VERDICT LỤC NHÂM: {ln_deep.get('verdict', 'BÌNH')}\n"
                    
                    # V20.3: HÌNH TƯỢNG LỤC NHÂM (Unicode Art)
                    try:
                        ln_visual = []
                        ln_visual.append(f"\n【HÌNH TƯỢNG ĐẠI LỤC NHÂM — AI HÃY NHÌN VÀ CẢM NHẬN】")
                        so_t = tam_truyen.get('so_truyen', '?')
                        trung_t = tam_truyen.get('trung_truyen', '?')
                        mat_t = tam_truyen.get('mat_truyen', '?')
                        so_h = tam_truyen.get('so_truyen_hanh', '?')
                        trung_h = tam_truyen.get('trung_truyen_hanh', '?')
                        mat_h = tam_truyen.get('mat_truyen_hanh', '?')
                        
                        ln_visual.append(f"┌─────────────┬─────────────┬─────────────┐")
                        ln_visual.append(f"│  QUÁ KHỨ    │  HIỆN TẠI   │  TƯƠNG LAI  │")
                        ln_visual.append(f"│  SƠ TRUYỀN  │ TRUNG TRUYỀN│ MẠT TRUYỀN  │")
                        ln_visual.append(f"├─────────────┼─────────────┼─────────────┤")
                        ln_visual.append(f"│  {so_t:<6}     │  {trung_t:<6}     │  {mat_t:<6}     │")
                        ln_visual.append(f"│  ({so_h:<4})     │  ({trung_h:<4})     │  ({mat_h:<4})     │")
                        ln_visual.append(f"│      ⬇       │      ⬇       │      ⬇       │")
                        ln_visual.append(f"│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │")
                        ln_visual.append(f"└─────────────┴─────────────┴─────────────┘")
                        
                        # Nhận xét flow
                        SINH_LN = {'Mộc':'Hỏa','Hỏa':'Thổ','Thổ':'Kim','Kim':'Thủy','Thủy':'Mộc'}
                        if SINH_LN.get(so_h) == trung_h:
                            ln_visual.append(f"→ CẢM NHẬN: Quá khứ SINH hiện tại — nền tảng tốt, xu hướng THUẬN")
                        elif SINH_LN.get(trung_h) == mat_h:
                            ln_visual.append(f"→ CẢM NHẬN: Hiện tại SINH tương lai — tương lai SÁNG SỦA")
                        elif so_h == trung_h == mat_h:
                            ln_visual.append(f"→ CẢM NHẬN: 3 truyền ĐỒNG HÀNH — tình huống ỔN ĐỊNH, ít biến")
                        else:
                            ln_visual.append(f"→ CẢM NHẬN: Tam Truyền KHÔNG liên tục — tình huống có BIẾN CHUYỂN")
                        
                        luc_nham_pre += "\n".join(ln_visual) + "\n"
                    except:
                        pass
                    
                    info += luc_nham_pre
            except Exception as e:
                luc_nham_pre = ""
            
            # V14.0: THÁI ẤT THẦN SỐ PRE-ANALYSIS
            try:
                from thai_at_than_so import tinh_thai_at_than_so
                import datetime as _dt_ta
                now_ta = _dt_ta.datetime.now()
                ta_can = qmdg_input.get('can_ngay', 'Giáp') if qmdg_input and isinstance(qmdg_input, dict) else 'Giáp'
                ta_chi = qmdg_input.get('chi_ngay', 'Tý') if qmdg_input and isinstance(qmdg_input, dict) else 'Tý'
                ta_data = tinh_thai_at_than_so(now_ta.year, now_ta.month, ta_can, ta_chi)
                thai_at_pre = "\n[THÁI ẤT PRE-ANALYSIS (Python-computed)]\n"
                ta_cung = ta_data.get('thai_at_cung', {})
                thai_at_pre += f"Thái Ất: Cung {ta_cung.get('cung', '?')} ({ta_cung.get('ten_cung', '?')}) — {ta_cung.get('hanh_cung', '?')} — {ta_cung.get('ly', '?')}\n"
                bat_tuong = ta_data.get('bat_tuong', {})
                for bt_name, bt_info in list(bat_tuong.items())[:4]:
                    thai_at_pre += f"{bt_name}: Cung {bt_info.get('cung', '?')} ({bt_info.get('ten_cung', '?')}) — {bt_info.get('cat_hung', '?')}\n"
                luan_giai = ta_data.get('luan_giai', {})
                for d in luan_giai.get('details', [])[:6]:
                    thai_at_pre += f"{d}\n"
                for cc in ta_data.get('cach_cuc', [])[:3]:
                    thai_at_pre += f"{cc}\n"
                thai_at_pre += f"VERDICT THÁI ẤT: {luan_giai.get('verdict', 'BÌNH')}\n"
                
                # V20.3: HÌNH TƯỢNG THÁI ẤT (Unicode Art)
                try:
                    ta_visual = []
                    ta_visual.append(f"\n【HÌNH TƯỢNG THÁI ẤT THẦN SỐ — AI HÃY NHÌN VÀ CẢM NHẬN】")
                    ta_visual.append(f"┌──────────────────────────────────────┐")
                    ta_cung_num = ta_cung.get('cung', '?')
                    ta_cung_ten = ta_cung.get('ten_cung', '?')
                    ta_cung_hanh = ta_cung.get('hanh_cung', '?')
                    ta_visual.append(f"│ 🌟 THÁI ẤT CƯ CUNG: {ta_cung_num} ({ta_cung_ten}) │")
                    ta_visual.append(f"│    Hành: {ta_cung_hanh:<10}                   │")
                    ta_visual.append(f"├──────────────────────────────────────┤")
                    ta_visual.append(f"│ 🎭 BÁT TƯỚNG:                       │")
                    for bt_name, bt_info in list(bat_tuong.items())[:4]:
                        bt_cung = bt_info.get('cung', '?')
                        bt_cat = bt_info.get('cat_hung', '?')
                        icon = '🟢' if 'CÁT' in str(bt_cat).upper() else ('🔴' if 'HUNG' in str(bt_cat).upper() else '🟡')
                        ta_visual.append(f"│  {icon} {bt_name[:8]:<8} → Cung {bt_cung} ({bt_cat}) │")
                    ta_visual.append(f"├──────────────────────────────────────┤")
                    ta_verdict = luan_giai.get('verdict', 'BÌNH')
                    v_icon = '🟢' if 'CÁT' in str(ta_verdict).upper() else ('🔴' if 'HUNG' in str(ta_verdict).upper() else '🟡')
                    ta_visual.append(f"│ {v_icon} VERDICT: {ta_verdict:<26} │")
                    ta_visual.append(f"└──────────────────────────────────────┘")
                    
                    thai_at_pre += "\n".join(ta_visual) + "\n"
                except:
                    pass
                
                info += thai_at_pre
            except Exception as e:
                thai_at_pre = ""
            
            # V14.0: CROSS-METHOD VERDICT (5 phương pháp)
            try:
                cross_verdict = self._compute_cross_verdict(ky_mon_pre, luc_hao_pre, mai_hoa_pre, luc_nham_pre, thai_at_pre)
                if cross_verdict: info += cross_verdict
            except Exception:
                pass
            
            # ============================================
            # PART 7.5: NUMBER ENGINE (V20.3) — SỐ HỌC QUẺ
            # Tính sẵn các con số để AI KHÔNG phải bịa
            # ============================================
            try:
                num_result = []
                
                # Bát Quái numbers (Tiên Thiên + Hậu Thiên)
                TIEN_THIEN = {'Càn':1,'Đoài':2,'Ly':3,'Chấn':4,'Tốn':5,'Khảm':6,'Cấn':7,'Khôn':8}
                HAU_THIEN = {'Khảm':1,'Khôn':2,'Chấn':3,'Tốn':4,'Càn':6,'Đoài':7,'Cấn':8,'Ly':9}
                # Ngũ Hành numbers (Hà Đồ)
                HA_DO = {'Thủy': [1,6], 'Hỏa': [2,7], 'Mộc': [3,8], 'Kim': [4,9], 'Thổ': [5,10]}
                
                # Lấy số từ Kỳ Môn
                km_nums = []
                if qmdg_input and isinstance(qmdg_input, dict):
                    cung_chu = qmdg_input.get('cung_ban_than', '')
                    cung_sv = qmdg_input.get('cung_su_viec', '')
                    if cung_chu: km_nums.append(int(cung_chu) if str(cung_chu).isdigit() else 0)
                    if cung_sv: km_nums.append(int(cung_sv) if str(cung_sv).isdigit() else 0)
                
                # Lấy số từ Mai Hoa
                mh_nums = []
                if mai_hoa_data:
                    mh_upper = mai_hoa_data.get('upper', 0)
                    mh_lower = mai_hoa_data.get('lower', 0)
                    mh_dong = mai_hoa_data.get('dong_hao', 0)
                    ten_thuong = mai_hoa_data.get('ten_thuong', '')
                    ten_ha = mai_hoa_data.get('ten_ha', '')
                    if ten_thuong: mh_nums.extend([TIEN_THIEN.get(ten_thuong, 0), HAU_THIEN.get(ten_thuong, 0)])
                    if ten_ha: mh_nums.extend([TIEN_THIEN.get(ten_ha, 0), HAU_THIEN.get(ten_ha, 0)])
                    if mh_upper: mh_nums.append(mh_upper)
                    if mh_lower: mh_nums.append(mh_lower)
                    if mh_dong: mh_nums.append(mh_dong)
                
                # Lấy số từ Lục Hào
                lh_nums = []
                if luc_hao_data:
                    lh_dong = luc_hao_data.get('dong_hao', [])
                    if lh_dong: lh_nums.extend(lh_dong)
                    # Palace number
                    palace_name = luc_hao_data.get('ban', {}).get('palace', '')
                    for qn, qv in HAU_THIEN.items():
                        if qn in str(palace_name):
                            lh_nums.append(qv)
                            break
                
                # Ngũ Hành numbers
                hanh_nums = []
                if qmdg_input and isinstance(qmdg_input, dict):
                    can_ngay_h = qmdg_input.get('can_ngay', '')
                    CAN_HANH_NUM = {'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa',
                                    'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim',
                                    'Nhâm': 'Thủy', 'Quý': 'Thủy'}
                    hanh_can = CAN_HANH_NUM.get(can_ngay_h, '')
                    if hanh_can and hanh_can in HA_DO:
                        hanh_nums = HA_DO[hanh_can]
                
                # Tổng hợp tất cả số
                all_nums = list(set([n for n in km_nums + mh_nums + lh_nums + hanh_nums if n and n > 0]))
                all_nums.sort()
                
                if all_nums:
                    num_result.append(f"SỐ GỐC TỪ QUẺ: {', '.join(map(str, all_nums))}")
                    num_result.append(f"SỐ MAY MẮN: {', '.join(map(str, all_nums[:3]))}")
                    
                    # Tính range cho các loại số
                    base = all_nums[0]
                    
                    # Tuổi: dùng Tiên Thiên × 10 ± Hậu Thiên
                    age_ranges = []
                    for n in all_nums[:3]:
                        if n <= 3: age_ranges.append(f"{n*10}-{n*10+9}")
                        elif n <= 6: age_ranges.append(f"{n*7}-{n*8}")
                        else: age_ranges.append(f"{n*8}-{n*9}")
                    num_result.append(f"TUỔI (range): {', '.join(age_ranges)} tuổi")
                    
                    # Chiều cao: dùng Quái × bội số
                    height_base = all_nums[0] if all_nums[0] >= 1 else 5
                    num_result.append(f"CHIỀU CAO (range): {140 + height_base*4}-{150 + height_base*4} cm")
                    
                    # Tiền: dùng Hà Đồ × đơn vị
                    money_nums = hanh_nums if hanh_nums else all_nums[:2]
                    num_result.append(f"SỐ TIỀN (cơ sở): {', '.join(map(str, money_nums))} → nhân đơn vị (triệu/trăm triệu/tỷ tùy context)")
                    
                    # Thời gian: dùng Động Hào + Cung
                    time_nums = lh_nums[:2] if lh_nums else km_nums[:2] if km_nums else all_nums[:2]
                    num_result.append(f"THỜI GIAN: {', '.join(map(str, time_nums))} ngày/tuần/tháng (tùy DT Vượng/Suy)")
                    
                    # Khoảng cách
                    num_result.append(f"KHOẢNG CÁCH: {', '.join(map(str, all_nums[:2]))} × đơn vị (km/m/dặm tùy context)")
                    
                    # Số lượng
                    num_result.append(f"SỐ LƯỢNG: {', '.join(map(str, all_nums[:3]))}")
                
                # ═══════════════════════════════════════════
                # MAI HOA SỐ HỌC CHÍNH XÁC (Thiệu Khang Tiết)
                # ═══════════════════════════════════════════
                if mai_hoa_data:
                    num_result.append("")
                    num_result.append("【MAI HOA SỐ HỌC — CHÍNH XÁC NHẤT】")
                    mh_u = mai_hoa_data.get('upper', 0)
                    mh_l = mai_hoa_data.get('lower', 0)
                    mh_d = mai_hoa_data.get('dong_hao', 0)
                    tong_so = mh_u + mh_l
                    
                    if tong_so > 0:
                        num_result.append(f"→ Thượng Quái số: {mh_u} | Hạ Quái số: {mh_l} | Tổng: {tong_so}")
                        num_result.append(f"→ Động Hào: {mh_d}")
                        
                        # Quy tắc Mai Hoa: SỐ = Quái số, × bội nếu cần
                        num_result.append(f"→ SỐ CHÍNH: {tong_so} (dùng cho tuổi/ngày/tháng/số lượng)")
                        num_result.append(f"→ SỐ PHỤ: {mh_u}, {mh_l}, {mh_d}")
                        
                        # Bội số Mai Hoa
                        boi_list = [tong_so, tong_so*2, tong_so*5, tong_so*10]
                        num_result.append(f"→ BỘI SỐ (×1,×2,×5,×10): {', '.join(map(str, boi_list))}")
                        
                        # Mai Hoa timing rule
                        num_result.append(f"→ NGÀY ỨNG (Mai Hoa): {tong_so} ngày hoặc {mh_d} ngày kể từ hôm nay")
                
                # ═══════════════════════════════════════════
                # LỤC HÀO ỨNG KỲ CHI — NGÀY CHÍNH XÁC
                # ═══════════════════════════════════════════
                if luc_hao_data:
                    CHI_LIST_NUM = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                    CHI_HANH_NUM = {'Tý':'Thủy','Sửu':'Thổ','Dần':'Mộc','Mão':'Mộc','Thìn':'Thổ','Tỵ':'Hỏa',
                                    'Ngọ':'Hỏa','Mùi':'Thổ','Thân':'Kim','Dậu':'Kim','Tuất':'Thổ','Hợi':'Thủy'}
                    SINH_MAP = {'Mộc':'Thủy','Hỏa':'Mộc','Thổ':'Hỏa','Kim':'Thổ','Thủy':'Kim'}
                    
                    dt_hanh_num = ''
                    dt_strength_num = ''
                    ban_det = luc_hao_data.get('ban', {}).get('details', [])
                    dt_lab = luc_hao_data.get('dung_than_label', '')
                    for d in ban_det:
                        if dt_lab and dt_lab in str(d.get('luc_thu', '')):
                            can_chi = str(d.get('can_chi', ''))
                            parts = can_chi.split('-')
                            if len(parts) > 1:
                                dt_hanh_num = parts[-1].strip()
                            dt_strength_num = str(d.get('strength', ''))
                            break
                    
                    if dt_hanh_num:
                        num_result.append("")
                        num_result.append("【LỤC HÀO ỨNG KỲ — NGÀY CHÍNH XÁC】")
                        
                        s_up = dt_strength_num.upper()
                        if 'VƯỢNG' in s_up or 'ĐẾ VƯỢNG' in s_up:
                            # DT Vượng → ứng ngày Sinh (Chi có hành sinh DT)
                            hanh_sinh_dt = SINH_MAP.get(dt_hanh_num, '')
                            ngay_ung = [c for c, h in CHI_HANH_NUM.items() if h == hanh_sinh_dt]
                            num_result.append(f"→ DT({dt_hanh_num}) VƯỢNG → ứng ngày {'/'.join(ngay_ung)} ({hanh_sinh_dt} sinh {dt_hanh_num})")
                            num_result.append(f"→ Đơn vị: NGÀY (vì DT Vượng = ứng nhanh)")
                        elif 'TƯỚNG' in s_up:
                            ngay_ung = [c for c, h in CHI_HANH_NUM.items() if h == dt_hanh_num]
                            num_result.append(f"→ DT({dt_hanh_num}) TƯỚNG → ứng ngày {'/'.join(ngay_ung)} ({dt_hanh_num} Tỷ Hòa)")
                            num_result.append(f"→ Đơn vị: NGÀY hoặc TUẦN")
                        elif 'HƯU' in s_up or 'TRUNG' in s_up:
                            ngay_ung = [c for c, h in CHI_HANH_NUM.items() if h == dt_hanh_num]
                            num_result.append(f"→ DT({dt_hanh_num}) HƯU → ứng tháng/ngày {'/'.join(ngay_ung)}")
                            num_result.append(f"→ Đơn vị: TUẦN hoặc THÁNG")
                        elif 'TÙ' in s_up:
                            hanh_sinh_dt = SINH_MAP.get(dt_hanh_num, '')
                            ngay_ung = [c for c, h in CHI_HANH_NUM.items() if h == hanh_sinh_dt]
                            num_result.append(f"→ DT({dt_hanh_num}) TÙ → chờ ngày {'/'.join(ngay_ung)} ({hanh_sinh_dt} sinh DT)")
                            num_result.append(f"→ Đơn vị: THÁNG (vì DT yếu = ứng chậm)")
                        elif 'TUYỆT' in s_up or 'TỬ' in s_up:
                            num_result.append(f"→ DT({dt_hanh_num}) TUYỆT/TỬ → rất lâu hoặc KHÔNG ỨNG")
                            num_result.append(f"→ Đơn vị: THÁNG/NĂM")
                        
                        # Tuần Không timing
                        try:
                            import streamlit as st
                            chart_tk = st.session_state.get('chart_data', {}) if hasattr(st, 'session_state') else {}
                            tuan_khong = chart_tk.get('tuan_khong', [])
                            if tuan_khong:
                                num_result.append(f"→ TUẦN KHÔNG: {', '.join(tuan_khong)} → Hào lâm Tuần Không sẽ ỨNG khi XUẤT KHÔNG (ra khỏi tuần)")
                        except:
                            pass
                
                # ═══════════════════════════════════════════
                # KỲ MÔN SỐ CUNG — SỐ LẠC THƯ
                # ═══════════════════════════════════════════
                if km_nums:
                    num_result.append("")
                    num_result.append("【KỲ MÔN SỐ CUNG — LẠC THƯ】")
                    for cn in km_nums:
                        if cn and cn > 0:
                            lac_thu_nums = {1:'Khảm/Thủy',2:'Khôn/Thổ',3:'Chấn/Mộc',4:'Tốn/Mộc',
                                           5:'Trung Cung',6:'Càn/Kim',7:'Đoài/Kim',8:'Cấn/Thổ',9:'Ly/Hỏa'}
                            num_result.append(f"→ Cung {cn} = {lac_thu_nums.get(cn, '?')} → Số liên quan: {cn}, {cn*10}")
                
                if num_result:
                    info += "\n=== [SỐ HỌC QUẺ — NUMBER ENGINE V20.3] ===\n"
                    info += "(⛔ AI PHẢI dùng các số này, KHÔNG ĐƯỢC tự bịa con số)\n"
                    info += "\n".join(num_result) + "\n"
                    
            except Exception:
                pass
            
            # ============================================
            # PART 7: KNOWLEDGE BASE RULES PRE-ANALYSIS
            # Phase 2-4 data modules for enriched Gemini context
            # ============================================
            try:
                from luc_hao_ky_mon_rules import (
                    LUC_HAO_RULES, HAO_BIEN_RULES, NHAT_NGUYET_RULES
                )
                from kinh_dich_64_que import MAI_HOA_THE_DUNG, MAI_HOA_UNG_KY
                
                kb_lines = []
                
                # --- Mai Hoa Thể Dụng ---
                if mai_hoa_data and MAI_HOA_THE_DUNG:
                    the_name = mai_hoa_data.get('ten_thuong', '')
                    dung_name = mai_hoa_data.get('ten_ha', '')
                    QUAI_HANH = {'Càn': 'Kim', 'Đoài': 'Kim', 'Ly': 'Hỏa', 'Chấn': 'Mộc',
                                 'Tốn': 'Mộc', 'Khảm': 'Thủy', 'Cấn': 'Thổ', 'Khôn': 'Thổ'}
                    the_h = QUAI_HANH.get(the_name, '')
                    dung_h = QUAI_HANH.get(dung_name, '')
                    if the_h and dung_h:
                        td_info = MAI_HOA_THE_DUNG.get((the_h, dung_h), {})
                        if td_info:
                            kb_lines.append(f"[Mai Hoa Thể Dụng] Thể={the_name}({the_h}) vs Dụng={dung_name}({dung_h})")
                            kb_lines.append(f"  Quan hệ: {td_info.get('quan_he','')} → Kết luận: {td_info.get('ket_luan','')}")
                            kb_lines.append(f"  Chi tiết: {td_info.get('chi_tiet','')}")
                            # Ứng Kỳ
                            if MAI_HOA_UNG_KY:
                                uk = MAI_HOA_UNG_KY.get(td_info.get('quan_he', ''), {})
                                if uk:
                                    kb_lines.append(f"  Ứng Kỳ: {uk.get('giai_thich','')} (tốc độ: {uk.get('toc_do','?')})")
                
                # --- Lục Hào Rules scan ---
                if luc_hao_data and LUC_HAO_RULES:
                    ban_data = luc_hao_data.get('ban', {})
                    haos = ban_data.get('haos', [])
                    dong_hao_g = luc_hao_data.get('dong_hao', [])
                    
                    # Xác định Dụng Thần hào
                    dt_hao = None
                    for h in haos:
                        if h.get('the_ung') == 'Thế':
                            dt_hao = h
                            break
                    
                    if dt_hao:
                        dt_vuong = str(dt_hao.get('vuong_suy', ''))
                        rule_hits = []
                        for rule in LUC_HAO_RULES:
                            rid = rule.get('id', '')
                            if rid == 'R01' and ('Vượng' in dt_vuong or 'Tướng' in dt_vuong):
                                rule_hits.append(rule)
                            elif rid == 'R02' and ('Suy' in dt_vuong or 'Tử' in dt_vuong or 'Tuyệt' in dt_vuong):
                                rule_hits.append(rule)
                        
                        if rule_hits:
                            kb_lines.append(f"\n[Lục Hào Rules Matched: {len(rule_hits)}]")
                            for rh in rule_hits[:3]:
                                kb_lines.append(f"  {rh['id']} {rh['ten']}: {rh['ket_luan']}")
                    
                    # Hào Biến Rules
                    if HAO_BIEN_RULES and dong_hao_g:
                        bien_data = luc_hao_data.get('bien', {})
                        bien_haos = bien_data.get('haos', []) if bien_data else []
                        if bien_haos:
                            hb_hits = []
                            for d in dong_hao_g:
                                if d <= len(haos) and d <= len(bien_haos):
                                    orig_h = haos[d-1].get('ngu_hanh', '')
                                    bien_h = bien_haos[d-1].get('ngu_hanh', '')
                                    SINH_G = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
                                    if bien_h and orig_h and SINH_G.get(bien_h) == orig_h:
                                        for hbr in HAO_BIEN_RULES:
                                            if hbr.get('id') == 'HB01':
                                                hb_hits.append(f"Hào {d}: {hbr['ten']} → {hbr['ket_luan']}")
                                                break
                            if hb_hits:
                                kb_lines.append(f"\n[Hào Biến Rules: {len(hb_hits)}]")
                                for hbh in hb_hits[:2]:
                                    kb_lines.append(f"  {hbh}")
                    
                    # Nhật Nguyệt Rules
                    if NHAT_NGUYET_RULES and dt_hao and qmdg_input:
                        CAN_HANH_G = {'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa',
                                      'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim',
                                      'Nhâm': 'Thủy', 'Quý': 'Thủy'}
                        CHI_HANH_G = {'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc',
                                      'Thìn': 'Thổ', 'Tị': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ',
                                      'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'}
                        SINH_G2 = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
                        KHAC_G = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
                        
                        dt_hanh_g = dt_hao.get('ngu_hanh', '')
                        can_ngay_g = qmdg_input.get('can_ngay', '')
                        chi_thang_g = qmdg_input.get('chi_thang', '')
                        hanh_ngay_g = CAN_HANH_G.get(can_ngay_g, '')
                        hanh_thang_g = CHI_HANH_G.get(chi_thang_g, '')
                        
                        nn_hits = []
                        if hanh_ngay_g and dt_hanh_g and SINH_G2.get(hanh_ngay_g) == dt_hanh_g:
                            nn_hits.append("NN01 Nhật Thần Sinh DT → CÁT")
                        if hanh_ngay_g and dt_hanh_g and KHAC_G.get(hanh_ngay_g) == dt_hanh_g:
                            nn_hits.append("NN02 Nhật Thần Khắc DT → HUNG")
                        if hanh_thang_g and dt_hanh_g and SINH_G2.get(hanh_thang_g) == dt_hanh_g:
                            nn_hits.append("NN03 Nguyệt Thần Sinh DT → ĐẠI CÁT")
                        if hanh_thang_g and dt_hanh_g and KHAC_G.get(hanh_thang_g) == dt_hanh_g:
                            nn_hits.append("NN04 Nguyệt Phá → ĐẠI HUNG")
                        
                        if nn_hits:
                            kb_lines.append(f"\n[Nhật Nguyệt Rules: {len(nn_hits)}]")
                            for nnh in nn_hits:
                                kb_lines.append(f"  {nnh}")
                
                if kb_lines:
                    info += "\n=== [7] KNOWLEDGE BASE RULES PRE-ANALYSIS ===\n"
                    info += "(Quy tắc cổ điển đã match với dữ liệu quẻ hiện tại — Dùng để kiểm chứng và bổ sung)\n"
                    info += "\n".join(kb_lines) + "\n"
                    
            except Exception as e:
                info += f"\n(Lỗi KB Rules: {e})\n"
            
            return info
            
        except Exception as e:
            return f"⚠️ Lỗi tính toán dữ liệu nền: {str(e)}"

    def _verify_analysis(self, raw_analysis, context_data, question):
        """V5.1: Kiểm chứng kết quả AI bằng cách đối chiếu với dữ liệu gốc."""
        try:
            self.log_step("Verification", "RUNNING", "Đối chiếu kết luận vs dữ liệu quẻ...")
            
            # Giới hạn context và analysis để prompt nhỏ gọn
            ctx_short = context_data[:3000] if len(context_data) > 3000 else context_data
            analysis_short = raw_analysis[:4000] if len(raw_analysis) > 4000 else raw_analysis
            
            verify_prompt = (
                f"Bạn là KIỂM CHỨNG VIÊN — chuyên gia kiểm tra phân tích quẻ.\n\n"
                f"DỮ LIỆU QUẺ GỐC:\n{ctx_short}\n\n"
                f"PHÂN TÍCH CỦA AI:\n{analysis_short}\n\n"
                f"NHIỆM VỤ: Kiểm tra từng kết luận:\n"
                f"1. Kết luận có ĐÚNG với dữ liệu quẻ gốc không?\n"
                f"2. Có chỗ nào BỊA ĐẶT (nói dữ kiện không có trong quẻ gốc) không?\n"
                f"3. Logic nhân quả có CHẶT CHẼ không?\n\n"
                f"NẾU CÓ SAI: Sửa lại chỗ sai, giữ nguyên phần đúng.\n"
                f"NẾU TẤT CẢ ĐÚNG: Trả lại nguyên văn bản phân tích.\n"
                f"100% TIẾNG VIỆT. Giữ nguyên format markdown."
            )
            
            # Gọi AI kiểm chứng với temperature cực thấp
            # V21.0: google-genai SDK verification
            safety_settings = [
                genai_types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_NONE'),
                genai_types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_NONE'),
                genai_types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_NONE'),
                genai_types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
            ]
            gen_config = genai_types.GenerateContentConfig(
                temperature=0.1,  # Cực thấp cho kiểm chứng
                top_p=0.7,
                max_output_tokens=32768,
                safety_settings=safety_settings,
            )
            
            # Dùng model hiện tại qua client
            if not self._client:
                return raw_analysis
            resp = self._client.models.generate_content(
                model=self.model_name,
                contents=verify_prompt,
                config=gen_config,
            )
            
            try:
                return resp.text
            except:
                if resp.candidates:
                    return resp.candidates[0].content.parts[0].text
                return None
                
        except Exception as e:
            self.log_step("Verification", "WARNING", f"Bỏ qua kiểm chứng: {str(e)[:80]}")
            return None  # Nếu lỗi, trả về None → dùng kết quả gốc

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

    # ================================================================
    # V6.0: PRE-ANALYSIS ENGINE — Python-computed divination rules
    # ================================================================
    
    def _pre_analyze_luc_hao(self, luc_hao_data):
        """V20.1: Auto-detect advanced Lục Hào rules + Nguyên/Kỵ/Cừu Thần + Nhật/Nguyệt + Ứng Kỳ."""
        if not luc_hao_data:
            return ""
        
        try:
            result = []
            ban = luc_hao_data.get('ban', {})
            bien = luc_hao_data.get('bien', {})
            dong_hao_list = luc_hao_data.get('dong_hao', [])
            ban_details = ban.get('details', [])
            bien_details = bien.get('details', [])
            
            # --- CHI mappings ---
            CHI_LIST = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
            LUC_XUNG = {0:6, 6:0, 1:7, 7:1, 2:8, 8:2, 3:9, 9:3, 4:10, 10:4, 5:11, 11:5}
            TAM_HOP = {
                'Thủy': ['Thân', 'Tý', 'Thìn'],
                'Kim': ['Tỵ', 'Dậu', 'Sửu'],
                'Hỏa': ['Dần', 'Ngọ', 'Tuất'],
                'Mộc': ['Hợi', 'Mão', 'Mùi']
            }
            SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
            KHAC = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
            CHI_HANH = {'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc', 'Thìn': 'Thổ', 'Tỵ': 'Hỏa',
                        'Ngọ': 'Hỏa', 'Mùi': 'Thổ', 'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'}
            # Lục Thân sinh khắc chain for Nguyên/Kỵ/Cừu Thần
            LUC_THAN_SINH = {'Quan Quỷ': 'Thê Tài', 'Thê Tài': 'Tử Tôn', 'Tử Tôn': 'Huynh Đệ',
                             'Huynh Đệ': 'Phụ Mẫu', 'Phụ Mẫu': 'Quan Quỷ'}
            LUC_THAN_KHAC = {'Quan Quỷ': 'Huynh Đệ', 'Thê Tài': 'Phụ Mẫu', 'Tử Tôn': 'Quan Quỷ',
                             'Huynh Đệ': 'Thê Tài', 'Phụ Mẫu': 'Tử Tôn'}
            
            def get_chi(can_chi_str):
                """Extract Chi from 'Can-Element' format like 'Tý-Thủy'"""
                if not can_chi_str: return None
                parts = str(can_chi_str).split('-')
                return parts[0].strip() if parts else None
            
            def get_hanh(can_chi_str):
                """Extract Hành from 'Chi-Hành' format like 'Tý-Thủy'"""
                if not can_chi_str: return None
                parts = str(can_chi_str).split('-')
                return parts[-1].strip() if len(parts) > 1 else None
            
            def chi_index(chi_name):
                try: return CHI_LIST.index(chi_name)
                except: return -1
            
            # ═══════════════════════════════════════════
            # V20.1 FIX 1: NGUYÊN THẦN / KỴ THẦN / CỪU THẦN
            # ═══════════════════════════════════════════
            dt_label = luc_hao_data.get('dung_than_label', '')
            dt_luc_than = ''
            dt_hanh = ''
            dt_strength = ''
            dt_hao_num = ''
            
            # V20.5 FIX GAP 1: Xác định DT trong 6 hào — dùng luc_than (KHÔNG phải luc_thu)
            for d in ban_details:
                luc_than = str(d.get('luc_than', ''))  # V20.5: Fix — dùng luc_than thay vì luc_thu
                marker = str(d.get('marker', ''))
                # DT match: by label hoặc by Thế hào (fallback)
                if dt_label == '__THE_HAO__':
                    # Fallback: dùng Thế hào làm DT
                    if 'Thế' in marker:
                        dt_luc_than = luc_than
                        dt_hanh = get_hanh(d.get('can_chi', ''))
                        dt_strength = str(d.get('strength', ''))
                        dt_hao_num = str(d.get('hao', ''))
                        break
                elif dt_label and dt_label in luc_than:
                    dt_luc_than = luc_than
                    dt_hanh = get_hanh(d.get('can_chi', ''))
                    dt_strength = str(d.get('strength', ''))
                    dt_hao_num = str(d.get('hao', ''))
                    break
            
            if dt_luc_than:
                result.append(f"📌 DỤNG THẦN: {dt_luc_than} tại Hào {dt_hao_num} ({dt_hanh}) — {dt_strength}")
                
                # Nguyên Thần = Lục Thân sinh DT
                nguyen_than_name = ''
                for lt_name, lt_sinh in LUC_THAN_SINH.items():
                    if lt_sinh == dt_luc_than:
                        nguyen_than_name = lt_name
                        break
                # Kỵ Thần = Lục Thân khắc DT
                ky_than_name = ''
                for lt_name, lt_khac in LUC_THAN_KHAC.items():
                    if lt_khac == dt_luc_than:
                        ky_than_name = lt_name
                        break
                # Cừu Thần = Lục Thân khắc Nguyên Thần
                cuu_than_name = ''
                if nguyen_than_name:
                    for lt_name, lt_khac in LUC_THAN_KHAC.items():
                        if lt_khac == nguyen_than_name:
                            cuu_than_name = lt_name
                            break
                
                # Tìm Nguyên Thần trong 6 hào
                if nguyen_than_name:
                    for d in ban_details:
                        if nguyen_than_name in str(d.get('luc_thu', '')):
                            nt_dong = '⚡ĐỘNG' if d.get('is_moving') else 'TĨNH'
                            result.append(f"  → NGUYÊN THẦN (sinh DT): {nguyen_than_name} tại Hào {d.get('hao','?')} — {d.get('strength','?')} {nt_dong}")
                            if d.get('is_moving') and 'Vượng' in str(d.get('strength', '')):
                                result.append(f"    ✅ Nguyên Thần VƯỢNG + ĐỘNG = SINH DT MẠNH → ĐẠI CÁT")
                            elif not d.get('is_moving'):
                                result.append(f"    ○ Nguyên Thần TĨNH = chưa phát huy hết sức")
                            break
                
                # Tìm Kỵ Thần trong 6 hào
                if ky_than_name:
                    for d in ban_details:
                        if ky_than_name in str(d.get('luc_thu', '')):
                            kt_dong = '⚡ĐỘNG' if d.get('is_moving') else 'TĨNH'
                            result.append(f"  → KỴ THẦN (khắc DT): {ky_than_name} tại Hào {d.get('hao','?')} — {d.get('strength','?')} {kt_dong}")
                            if d.get('is_moving') and 'Vượng' in str(d.get('strength', '')):
                                result.append(f"    ⛔ Kỵ Thần VƯỢNG + ĐỘNG = KHẮC DT MẠNH → ĐẠI HUNG")
                            break
                
                if cuu_than_name:
                    result.append(f"  → CỪU THẦN (khắc Nguyên Thần): {cuu_than_name}")
            
            # ═══════════════════════════════════════════
            # V20.1 FIX 2: NHẬT THẦN / NGUYỆT KIẾN sinh khắc DT
            # ═══════════════════════════════════════════
            if dt_hanh:
                try:
                    import streamlit as st
                    chart = st.session_state.get('chart_data', {}) if hasattr(st, 'session_state') else {}
                    chi_ngay_nh = chart.get('chi_ngay', '')
                    chi_thang_nh = chart.get('chi_thang', '')
                    
                    if chi_ngay_nh:
                        nh_hanh = CHI_HANH.get(chi_ngay_nh, '')
                        if nh_hanh and dt_hanh:
                            if SINH.get(nh_hanh) == dt_hanh:
                                result.append(f"🌞 NHẬT THẦN ({chi_ngay_nh}/{nh_hanh}) SINH DT ({dt_hanh}) → CÁT! DT được Nhật Thần hỗ trợ")
                            elif KHAC.get(nh_hanh) == dt_hanh:
                                result.append(f"🌞 NHẬT THẦN ({chi_ngay_nh}/{nh_hanh}) KHẮC DT ({dt_hanh}) → HUNG! DT bị Nhật Phá")
                            elif nh_hanh == dt_hanh:
                                result.append(f"🌞 NHẬT THẦN ({chi_ngay_nh}/{nh_hanh}) TỶ HÒA DT ({dt_hanh}) → Trung bình")
                    
                    if chi_thang_nh:
                        ng_hanh = CHI_HANH.get(chi_thang_nh, '')
                        if ng_hanh and dt_hanh:
                            if SINH.get(ng_hanh) == dt_hanh:
                                result.append(f"🌙 NGUYỆT KIẾN ({chi_thang_nh}/{ng_hanh}) SINH DT ({dt_hanh}) → ĐẠI CÁT! DT đắc Lệnh Tháng")
                            elif KHAC.get(ng_hanh) == dt_hanh:
                                result.append(f"🌙 NGUYỆT KIẾN ({chi_thang_nh}/{ng_hanh}) KHẮC DT ({dt_hanh}) → ĐẠI HUNG! DT thất Lệnh")
                            elif ng_hanh == dt_hanh:
                                result.append(f"🌙 NGUYỆT KIẾN ({chi_thang_nh}/{ng_hanh}) VƯỢNG DT ({dt_hanh}) → CÁT! DT đắc Lệnh")
                except Exception:
                    pass
            
            # 1. TẤN THẦN / THOÁI THẦN (advancing/retreating)
            for dh in dong_hao_list:
                ban_d = next((d for d in ban_details if d['hao'] == dh), None)
                bien_d = next((d for d in bien_details if d['hao'] == dh), None)
                if ban_d and bien_d:
                    ban_chi = get_chi(ban_d.get('can_chi'))
                    bien_chi = get_chi(bien_d.get('can_chi'))
                    if ban_chi and bien_chi:
                        bi = chi_index(ban_chi)
                        bii = chi_index(bien_chi)
                        if bi >= 0 and bii >= 0:
                            if bii == (bi + 1) % 12:
                                result.append(f"★ TẤN THẦN: Hào {dh} ({ban_chi}→{bien_chi}) — Sự việc TIẾN BỘ, phát triển")
                            elif bii == (bi - 1) % 12:
                                result.append(f"★ THOÁI THẦN: Hào {dh} ({ban_chi}→{bien_chi}) — Sự việc THOÁI LUI, suy giảm")
                            # V20.1 FIX 3: Hóa Hồi Đầu Khắc + Sinh for DỤNG THẦN specifically
                            ban_elem = get_hanh(ban_d.get('can_chi', ''))
                            bien_elem = get_hanh(bien_d.get('can_chi', ''))
                            if ban_elem and bien_elem:
                                if KHAC.get(bien_elem) == ban_elem:
                                    is_dt = dt_luc_than and dt_luc_than in str(ban_d.get('luc_thu', ''))
                                    severity = "CỰC HUNG — DT bị chính hào biến khắc!" if is_dt else "HUNG"
                                    result.append(f"⚠️ HÓA HỒI ĐẦU KHẮC: Hào {dh} ({ban_elem}→{bien_elem}) → {severity}")
                                elif SINH.get(bien_elem) == ban_elem:
                                    result.append(f"★ HÓA HỒI ĐẦU SINH: Hào {dh} ({ban_elem}←{bien_elem}) → CÁT, được hào biến trợ lực")
            
            # 2. PHỤC NGÂM / PHẢN NGÂM
            for dh in dong_hao_list:
                ban_d = next((d for d in ban_details if d['hao'] == dh), None)
                bien_d = next((d for d in bien_details if d['hao'] == dh), None)
                if ban_d and bien_d:
                    ban_chi = get_chi(ban_d.get('can_chi'))
                    bien_chi = get_chi(bien_d.get('can_chi'))
                    if ban_chi and bien_chi:
                        if ban_chi == bien_chi:
                            result.append(f"⚠️ PHỤC NGÂM: Hào {dh} biến thành CHÍNH NÓ ({ban_chi}→{bien_chi}) → Trì trệ, giằng co")
                        bi = chi_index(ban_chi)
                        bii = chi_index(bien_chi)
                        if bi >= 0 and bii >= 0 and LUC_XUNG.get(bi) == bii:
                            result.append(f"⚠️ PHẢN NGÂM: Hào {dh} biến đối xung ({ban_chi}→{bien_chi}) → Đảo ngược hoàn toàn")
            
            # 3. TAM HỢP CỤC — check if 3 branches present across 6 hào
            all_chi_in_hex = [get_chi(d.get('can_chi')) for d in ban_details if get_chi(d.get('can_chi'))]
            for hanh, trio in TAM_HOP.items():
                present = [c for c in trio if c in all_chi_in_hex]
                if len(present) >= 3:
                    result.append(f"★ TAM HỢP CỤC {hanh.upper()}: {'+'.join(trio)} → Sức mạnh {hanh} GẤP 3 LẦN")
                elif len(present) == 2:
                    missing = [c for c in trio if c not in present][0]
                    result.append(f"○ BÁN TAM HỢP {hanh}: {'+'.join(present)} (thiếu {missing})")
            
            # 4. LỤC XUNG / LỤC HỢP QUẺ (check 3 pairs: 1-4, 2-5, 3-6)
            xung_count = 0
            hop_count = 0
            LUC_HOP_MAP = {0:1, 1:0, 2:11, 11:2, 3:10, 10:3, 4:9, 9:4, 5:8, 8:5, 6:7, 7:6}
            for pair in [(0, 3), (1, 4), (2, 5)]:
                if pair[0] < len(ban_details) and pair[1] < len(ban_details):
                    chi_a = get_chi(ban_details[pair[0]].get('can_chi'))
                    chi_b = get_chi(ban_details[pair[1]].get('can_chi'))
                    if chi_a and chi_b:
                        ia, ib = chi_index(chi_a), chi_index(chi_b)
                        if ia >= 0 and ib >= 0:
                            if LUC_XUNG.get(ia) == ib: xung_count += 1
                            if LUC_HOP_MAP.get(ia) == ib: hop_count += 1
            if xung_count >= 3:
                result.append("⚠️ QUẺ LỤC XUNG: 3 cặp hào đều XUNG → Tan rã, BẤT THÀNH dù quẻ tốt")
            elif hop_count >= 3:
                result.append("★ QUẺ LỤC HỢP: 3 cặp hào đều HỢP → Gắn kết, THÀNH CÔNG")
            
            # ═══════════════════════════════════════════
            # V20.3 FIX 1: NHẬT PHÁ — Chi Ngày xung từng hào
            # ═══════════════════════════════════════════
            try:
                import streamlit as st
                chart_np = st.session_state.get('chart_data', {}) if hasattr(st, 'session_state') else {}
                chi_ngay_np = chart_np.get('chi_ngay', '')
                if chi_ngay_np:
                    ci_ngay = chi_index(chi_ngay_np)
                    if ci_ngay >= 0:
                        for d in ban_details:
                            hao_chi = get_chi(d.get('can_chi', ''))
                            if hao_chi:
                                ci_hao = chi_index(hao_chi)
                                if ci_hao >= 0 and LUC_XUNG.get(ci_ngay) == ci_hao:
                                    is_moving = d.get('is_moving', False)
                                    hao_num = d.get('hao', '?')
                                    luc_thu = d.get('luc_thu', '?')
                                    if is_moving:
                                        result.append(f"💥 NHẬT PHÁ: Hào {hao_num} ({hao_chi}) bị Chi Ngày ({chi_ngay_np}) XUNG + ĐỘNG → HÀO TÁN, VÔ LỰC")
                                    else:
                                        # Hào TĨNH bị Nhật xung = ÁM ĐỘNG
                                        result.append(f"👁️ ÁM ĐỘNG: Hào {hao_num} ({hao_chi}/{luc_thu}) bị Chi Ngày ({chi_ngay_np}) XUNG → Hoạt động NGẦM, sự việc Ẩn đang xảy ra")
            except Exception:
                pass
            
            # ═══════════════════════════════════════════
            # V20.3 FIX 3: ĐỘC PHÁT — chỉ 1 hào động
            # ═══════════════════════════════════════════
            if len(dong_hao_list) == 1:
                doc_hao = dong_hao_list[0]
                doc_d = next((d for d in ban_details if d['hao'] == doc_hao), None)
                if doc_d:
                    result.append(f"🎯 ĐỘC PHÁT: Chỉ có DUY NHẤT Hào {doc_hao} ({doc_d.get('luc_thu','?')}) ĐỘNG → Đây là TÂM ĐIỂM tuyệt đối, mọi phán đoán tập trung vào hào này")
            elif len(dong_hao_list) == 0:
                result.append(f"🔒 QUẺ TĨNH: KHÔNG có hào nào ĐỘNG → Sự việc ỔN ĐỊNH, ít biến chuyển, xem Thế/Ứng làm chính")
            elif len(dong_hao_list) >= 4:
                result.append(f"⚡ LOẠN ĐỘNG: {len(dong_hao_list)}/6 hào ĐỘNG → Sự việc LOẠN, nhiều biến số, khó kiểm soát")
            
            # ═══════════════════════════════════════════
            # V20.3 FIX 4: QUẺ BIẾN PHÂN LOẠI CÁT/HUNG
            # ═══════════════════════════════════════════
            bien_name = bien.get('name', '')
            if bien_name:
                QUE_HUNG = ['Bĩ', 'Bác', 'Khốn', 'Minh Di', 'Sơn Hỏa Bí', 'Đại Quá',
                            'Thiên Thủy Tụng', 'Địa Thủy Sư', 'Thủy Sơn Kiển', 'Sơn Trạch Tổn',
                            'Trạch Phong Đại Quá', 'Trạch Thủy Khốn', 'Địa Sơn Khiêm']
                QUE_DAI_CAT = ['Thái', 'Ký Tế', 'Càn Vi Thiên', 'Khôn Vi Địa',
                               'Thiên Hỏa Đồng Nhân', 'Phong Thủy Hoán', 'Hỏa Phong Đỉnh',
                               'Phong Lôi Ích', 'Lôi Hỏa Phong', 'Thủy Lôi Truân']
                QUE_CAT = ['Tấn', 'Thăng', 'Đại Hữu', 'Tiểu Súc', 'Đại Súc',
                           'Thiên Lôi Vô Vọng', 'Sơn Thiên Đại Súc', 'Lôi Địa Dự']
                
                is_hung = any(h in bien_name for h in QUE_HUNG)
                is_dai_cat = any(c in bien_name for c in QUE_DAI_CAT)
                is_cat = any(c in bien_name for c in QUE_CAT)
                
                if is_hung:
                    result.append(f"⛔ QUẺ BIẾN HUNG: {bien_name} → Xu hướng tương lai XẤU ĐI, cần đề phòng")
                elif is_dai_cat:
                    result.append(f"🌟 QUẺ BIẾN ĐẠI CÁT: {bien_name} → Xu hướng tương lai RẤT TỐT")
                elif is_cat:
                    result.append(f"✅ QUẺ BIẾN CÁT: {bien_name} → Xu hướng tương lai THUẬN LỢI")
                else:
                    result.append(f"○ QUẺ BIẾN: {bien_name} → Xu hướng TRUNG BÌNH, xem thêm chi tiết hào")
            
            # ═══════════════════════════════════════════
            # V20.1 FIX 6: ỨNG KỲ AUTO-COMPUTED
            # ═══════════════════════════════════════════
            if dt_strength:
                ung_ky = ""
                s = dt_strength.upper()
                if 'VƯỢNG' in s or 'ĐẾ VƯỢNG' in s:
                    ung_ky = "1-3 ngày (DT Vượng → ứng nhanh)"
                elif 'TƯỚNG' in s:
                    ung_ky = "~1 tuần (DT Tướng → ứng khá nhanh)"
                elif 'HƯU' in s or 'TRUNG BÌNH' in s:
                    ung_ky = "~1 tháng (DT Hưu → ứng chậm)"
                elif 'TÙ' in s:
                    ung_ky = "3+ tháng (DT Tù → ứng rất chậm, chờ Xuất Không)"
                elif 'TUYỆT' in s or 'TỬ' in s:
                    ung_ky = "Rất lâu hoặc KHÔNG ỨNG (DT Tuyệt/Tử)"
                
                if xung_count >= 3:
                    ung_ky = "3-7 ngày (Quẻ Lục Xung → ứng nhanh bất kể)"
                elif hop_count >= 3:
                    ung_ky = "1-3 tháng (Quẻ Lục Hợp → ứng chậm)"
                
                if ung_ky:
                    result.append(f"⏰ ỨNG KỲ (auto-computed): {ung_ky}")
            
            if result:
                return "\n[LỤC HÀO PRE-ANALYSIS V20.3 (Python-computed, chính xác 100%)]\n" + "\n".join(result)
            return ""
        except Exception as e:
            return f"\n(Lỗi pre-analysis Lục Hào: {e})"
    
    def _pre_analyze_ky_mon(self, qmdg_input):
        """V6.0: Auto-detect Kỳ Môn Cách Cục using Python logic."""
        if not qmdg_input or not isinstance(qmdg_input, dict):
            return ""
        
        try:
            result = []
            can_thien_ban = qmdg_input.get('can_thien_ban', {})
            can_dia_ban = qmdg_input.get('can_dia_ban', {})
            nhan_ban = qmdg_input.get('nhan_ban', {})
            than_ban = qmdg_input.get('than_ban', {})
            
            CUA_CAT = ['Hưu Môn', 'Sinh Môn', 'Khai Môn']
            TAM_KY = ['Ất', 'Bính', 'Đinh']
            
            # 1. TAM KỲ ĐẮC SỬ: Can Ất/Bính/Đinh + Cửa Cát
            for p in range(1, 10):
                can_t = can_thien_ban.get(p, '')
                cua = nhan_ban.get(p, '')
                if can_t in TAM_KY and cua in CUA_CAT:
                    result.append(f"★ TAM KỲ ĐẮC SỬ: Cung {p} có {can_t} (Tam Kỳ) + {cua} (Cửa Cát) → CỰC CÁT, thuận lợi lớn")
            
            # 2. NGỌC NỮ THỦ MÔN: Can Đinh + Trực Phù
            for p in range(1, 10):
                can_t = can_thien_ban.get(p, '')
                than = than_ban.get(p, '')
                if can_t == 'Đinh' and than == 'Trực Phù':
                    result.append(f"★ NGỌC NỮ THỦ MÔN: Cung {p} có Đinh (Ngọc Nữ) + Trực Phù → Quý nhân phù trợ, thành công bí mật")
            
            # 3. THANH LONG PHẢN THỦ: Mậu trên Bính (hoặc Giáp trên Bính)
            for p in range(1, 10):
                can_t = can_thien_ban.get(p, '')
                can_d = can_dia_ban.get(p, '')
                if can_t in ['Mậu', 'Giáp'] and can_d == 'Bính':
                    result.append(f"★ THANH LONG PHẢN THỦ: Cung {p} có {can_t}/{can_d} → 80-90% THÀNH CÔNG, đột phá mạnh")
            
            # 4. TAM HÌNH (Punishment configurations)
            chi_4tru = []
            for key in ['chi_nam', 'chi_thang', 'chi_ngay', 'chi_gio']:
                c = qmdg_input.get(key, '')
                if c: chi_4tru.append(c)
            
            HINH_SETS = [
                (['Dần', 'Tỵ', 'Thân'], 'Dần-Tỵ-Thân (VÔ ÂN CHI HÌNH)'),
                (['Sửu', 'Tuất', 'Mùi'], 'Sửu-Tuất-Mùi (TRÌ THẾ CHI HÌNH)'),
                (['Tý', 'Mão'], 'Tý-Mão (VÔ LỄ CHI HÌNH)'),
            ]
            for hinh_set, label in HINH_SETS:
                present = [c for c in hinh_set if c in chi_4tru]
                if len(present) >= 2:
                    result.append(f"⚠️ TAM HÌNH: {label} — CẢNH BÁO hình phạt, kiện tụng, tự hại")
            
            # 5. Check all 9 palaces for Phục Ngâm / Phản Ngâm of Stars/Doors
            # (Star/Door returns to its original palace = Phục Ngâm)
            SAO_GỐC = {1: 'Thiên Bồng', 2: 'Thiên Nhuế', 3: 'Thiên Xung', 4: 'Thiên Phụ',
                        5: 'Thiên Cầm', 6: 'Thiên Tâm', 7: 'Thiên Trụ', 8: 'Thiên Nhậm', 9: 'Thiên Anh'}
            CUA_GỐC = {1: 'Hưu Môn', 2: 'Tử Môn', 3: 'Thương Môn', 4: 'Đỗ Môn',
                        5: None, 6: 'Khai Môn', 7: 'Kinh Môn', 8: 'Sinh Môn', 9: 'Cảnh Môn'}
            
            thien_ban = qmdg_input.get('thien_ban', {})
            for p in range(1, 10):
                sao = thien_ban.get(p, '')
                cua = nhan_ban.get(p, '')
                if sao and sao == SAO_GỐC.get(p):
                    result.append(f"○ PHỤC NGÂM SAO: Cung {p} — {sao} về cung gốc → Trì trệ, không tiến")
                if cua and cua == CUA_GỐC.get(p):
                    result.append(f"○ PHỤC NGÂM CỬA: Cung {p} — {cua} về cung gốc → Sự việc bế tắc")
            
            # 6. V10.0: THẬP CAN KHẮC ỨNG — 81 tổ hợp (Sách Lưu Bá Ôn)
            try:
                from luc_hao_ky_mon_rules import THAP_CAN_KHAC_UNG, CAN_CHI_TUONG_Y
                for p in range(1, 10):
                    can_t = can_thien_ban.get(p, '')
                    can_d = can_dia_ban.get(p, '')
                    if can_t and can_d:
                        ku_key = f"{can_t}+{can_d}"
                        ku = THAP_CAN_KHAC_UNG.get(ku_key)
                        if ku:
                            result.append(f"📖 KHẮC ỨNG Cung {p}: {ku.get('ten','')} ({ku.get('cat_hung','')}) — {ku.get('luan','')}")
                
                # 7. V10.0: CAN CHI TƯỢNG Ý — cho Cung Bản Thân
                chu_cung_key = qmdg_input.get('cung_ban_than', '')
                if chu_cung_key:
                    can_bt = can_thien_ban.get(chu_cung_key, can_thien_ban.get(str(chu_cung_key), ''))
                    if can_bt and can_bt in CAN_CHI_TUONG_Y:
                        ty = CAN_CHI_TUONG_Y[can_bt]
                        result.append(f"📖 TƯỢNG Ý ({can_bt}): {ty.get('loai_tuong','')} | Nội tạng: {ty.get('an_tang','')} | Bệnh: {ty.get('benh','')}")
            except ImportError:
                pass
            
            if result:
                return "\n[KỲ MÔN CÁCH CỤC PRE-ANALYSIS (Python-computed)]\n" + "\n".join(result)
            return ""
        except Exception as e:
            return f"\n(Lỗi pre-analysis Kỳ Môn: {e})"
    
    def _pre_analyze_mai_hoa(self, mai_hoa_data):
        """V6.0: Compute Hỗ Quái, Thác Quái, and detailed Thể-Dụng for Mai Hoa."""
        if not mai_hoa_data:
            return ""
        
        try:
            result = []
            QUAI_NAMES = {1: 'Càn', 2: 'Đoài', 3: 'Ly', 4: 'Chấn', 5: 'Tốn', 6: 'Khảm', 7: 'Cấn', 8: 'Khôn'}
            QUAI_ELEMENTS = {1: 'Kim', 2: 'Kim', 3: 'Hỏa', 4: 'Mộc', 5: 'Mộc', 6: 'Thủy', 7: 'Thổ', 8: 'Thổ'}
            SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
            KHAC = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
            
            upper = mai_hoa_data.get('upper', 0)
            lower = mai_hoa_data.get('lower', 0)
            dong_hao = mai_hoa_data.get('dong_hao', 0)
            
            # 1. HỖ QUÁI (already computed in build_res but may not be in context)
            ho_upper = mai_hoa_data.get('ho_upper', 0)
            ho_lower = mai_hoa_data.get('ho_lower', 0)
            ten_ho = mai_hoa_data.get('ten_ho', '')
            
            if ho_upper and ho_lower:
                ho_up_e = QUAI_ELEMENTS.get(ho_upper, '?')
                ho_lo_e = QUAI_ELEMENTS.get(ho_lower, '?')
                result.append(f"★ HỖ QUÁI: {ten_ho} ({QUAI_NAMES.get(ho_upper,'?')}/{QUAI_NAMES.get(ho_lower,'?')}) — Hành: {ho_up_e}/{ho_lo_e}")
                result.append(f"  → Hỗ Quái là DIỄN BIẾN GIỮA CHỪNG: cho biết quá trình xảy ra trước khi đến kết quả cuối")
            
            # 2. THÁC QUÁI (invert all lines)
            lines = mai_hoa_data.get('lines', [])
            if lines and len(lines) == 6:
                thac_lines = [1-l for l in lines]
                quai_lines_map = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4, (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}
                thac_lower = quai_lines_map.get(tuple(thac_lines[:3]), 0)
                thac_upper = quai_lines_map.get(tuple(thac_lines[3:]), 0)
                if thac_lower and thac_upper:
                    thac_name = f"{QUAI_NAMES.get(thac_upper,'?')} {QUAI_NAMES.get(thac_lower,'?')}"
                    result.append(f"★ THÁC QUÁI: {thac_name} (đảo Âm↔Dương) — Mặt TRÁI của vấn đề, rủi ro ẩn giấu")
            
            # 3. THỂ-DỤNG CHI TIẾT
            if dong_hao and upper and lower:
                if dong_hao <= 3:
                    the_quai = upper  # Hạ quái động → Thượng = Thể
                    dung_quai = lower
                    the_label = "Thượng (Ngoại)"
                    dung_label = "Hạ (Nội)"
                else:
                    the_quai = lower  # Thượng quái động → Hạ = Thể
                    dung_quai = upper
                    the_label = "Hạ (Nội)"
                    dung_label = "Thượng (Ngoại)"
                
                the_e = QUAI_ELEMENTS.get(the_quai, '?')
                dung_e = QUAI_ELEMENTS.get(dung_quai, '?')
                
                # Sinh khắc analysis
                if the_e == dung_e:
                    rel = "THỂ-DỤNG TỶ HÒA → TRUNG BÌNH, ngang sức"
                elif SINH.get(dung_e) == the_e:
                    rel = "DỤNG SINH THỂ → ĐẠI CÁT! Được hỗ trợ, thuận lợi"
                elif SINH.get(the_e) == dung_e:
                    rel = "THỂ SINH DỤNG → Hao tốn, bỏ sức cho người khác"
                elif KHAC.get(the_e) == dung_e:
                    rel = "THỂ KHẮC DỤNG → CÁT! Bản thân mạnh, khắc chế sự việc"
                elif KHAC.get(dung_e) == the_e:
                    rel = "DỤNG KHẮC THỂ → HUNG! Bản thân bị khắc, bất lợi"
                else:
                    rel = "Không xác định"
                
                result.append(f"★ THỂ ({the_label}, {QUAI_NAMES.get(the_quai,'?')}, {the_e}) vs DỤNG ({dung_label}, {QUAI_NAMES.get(dung_quai,'?')}, {dung_e})")
                result.append(f"  → KẾT LUẬN: {rel}")
            
            if result:
                return "\n[MAI HOA PRE-ANALYSIS (Python-computed)]\n" + "\n".join(result)
            return ""
        except Exception as e:
            return f"\n(Lỗi pre-analysis Mai Hoa: {e})"
    
    def _compute_cross_verdict(self, ky_mon_pre, luc_hao_pre, mai_hoa_pre, luc_nham_pre='', thai_at_pre=''):
        """V20.0: Dynamic Confidence Scoring — weighted cross-method verdict with Tam Tài."""
        try:
            # --- 1. DETECT QUESTION CATEGORY FROM SESSION ---
            question_type = 'general'  # default
            try:
                import streamlit as st
                q = st.session_state.get('last_question', '').lower() if hasattr(st, 'session_state') else ''
                if any(k in q for k in ['tìm', 'mất', 'ở đâu', 'hướng']):
                    question_type = 'direction'
                elif any(k in q for k in ['yêu', 'vợ', 'chồng', 'tình', 'hôn', 'duyên']):
                    question_type = 'emotion'
                elif any(k in q for k in ['bệnh', 'ốm', 'khỏe', 'sức khỏe', 'thuốc']):
                    question_type = 'health'
                elif any(k in q for k in ['bao nhiêu', 'mấy', 'tuổi', 'số']):
                    question_type = 'quantity'
                elif any(k in q for k in ['khi nào', 'bao giờ', 'thời điểm', 'lúc nào']):
                    question_type = 'timing'
            except Exception:
                pass

            # --- 2. WEIGHT MATRIX (V20.0) ---
            # Weights: How much each method matters for this question type
            WEIGHT_MATRIX = {
                'general':   {'km': 3, 'lh': 2, 'mh': 1, 'ln': 1, 'ta': 1},
                'emotion':   {'km': 1, 'lh': 3, 'mh': 2, 'ln': 1, 'ta': 1},
                'direction': {'km': 3, 'lh': 1, 'mh': 2, 'ln': 1, 'ta': 1},
                'health':    {'km': 1, 'lh': 3, 'mh': 1, 'ln': 1, 'ta': 1},
                'quantity':  {'km': 1, 'lh': 2, 'mh': 3, 'ln': 1, 'ta': 1},
                'timing':    {'km': 2, 'lh': 3, 'mh': 1, 'ln': 1, 'ta': 1},
            }
            weights = WEIGHT_MATRIX.get(question_type, WEIGHT_MATRIX['general'])

            # --- 3. SCORE EACH METHOD ---
            methods = [
                ('km', ky_mon_pre, 'Kỳ Môn'),
                ('lh', luc_hao_pre, 'Lục Hào'),
                ('mh', mai_hoa_pre, 'Mai Hoa'),
                ('ln', luc_nham_pre, 'Lục Nhâm'),
                ('ta', thai_at_pre, 'Thái Ất'),
            ]

            total_weighted_score = 0
            total_weight = 0
            method_results = []

            for key, text, name in methods:
                if not text:
                    continue
                w = weights.get(key, 1)
                cat_words = text.count('CÁT') + text.count('THÀNH CÔNG') + text.count('THUẬN LỢI') + text.count('TIẾN BỘ') + text.count('ĐẠI CÁT')
                hung_words = text.count('HUNG') + text.count('BẤT THÀNH') + text.count('THOÁI LUI') + text.count('CỰC HUNG') + text.count('TRÌ TRỆ')

                if cat_words > hung_words:
                    score = 1  # CÁT
                    label = 'CÁT'
                elif hung_words > cat_words:
                    score = -1  # HUNG
                    label = 'HUNG'
                else:
                    score = 0  # BÌNH
                    label = 'BÌNH'

                total_weighted_score += score * w
                total_weight += w
                method_results.append(f"  {name}: {label} (trọng số {w}x)")

            if total_weight == 0:
                return ""

            # --- 4. COMPUTE CONFIDENCE ---
            # Normalized score: -1 (full HUNG) to +1 (full CÁT)
            normalized = total_weighted_score / total_weight
            # Map to percentage: -1 → 10%, 0 → 50%, +1 → 90%
            pct = int(50 + normalized * 40)
            pct = max(10, min(95, pct))

            # --- 5. DETERMINE VERDICT ---
            if pct >= 80:
                verdict = f"ĐẠI CÁT — Đa số PP đồng thuận tích cực"
                icon = "🟢"
            elif pct >= 65:
                verdict = f"CÁT — Xu hướng thuận lợi"
                icon = "🟢"
            elif pct >= 50:
                verdict = f"BÌNH — Cân bằng CÁT/HUNG"
                icon = "🟡"
            elif pct >= 35:
                verdict = f"HUNG — Xu hướng bất lợi"
                icon = "🟠"
            else:
                verdict = f"ĐẠI HUNG — Đa số PP đồng thuận tiêu cực"
                icon = "🔴"

            # --- 6. TAM TÀI SUMMARY ---
            # Auto-compute Tam Tài from available data
            thien = "CÁT" if any(t and ('CÁT' in t or 'THUẬN LỢI' in t) for t in [thai_at_pre]) else "HUNG" if thai_at_pre else "?"
            dia = "CÁT" if any(t and ('CÁT' in t) for t in [ky_mon_pre]) else "HUNG" if ky_mon_pre else "?"
            nhan = "CÁT" if any(t and ('CÁT' in t) for t in [luc_hao_pre, mai_hoa_pre]) else "HUNG" if (luc_hao_pre or mai_hoa_pre) else "?"

            # --- 7. BUILD OUTPUT ---
            result = (
                f"\n[CROSS-METHOD VERDICT V20.0 — Dynamic Confidence Scoring]\n"
                f"Loại câu hỏi phát hiện: {question_type.upper()}\n"
                f"Trọng số ưu tiên: KM={weights['km']}x | LH={weights['lh']}x | MH={weights['mh']}x | LN={weights['ln']}x | TA={weights['ta']}x\n"
                f"\nKết quả từng PP:\n"
            )
            result += "\n".join(method_results)
            result += (
                f"\n\n{icon} TỔNG KẾT: {verdict} — Tin cậy {pct}%\n"
                f"TAM TÀI: Thiên={thien} | Địa={dia} | Nhân={nhan}\n"
            )

            return result
        except Exception:
            return ""

    def _search_hub_knowledge(self, question, topic="Chung"):
        """Tìm kiếm tri thức liên quan từ Data Hub (Nhà Máy AI đã khai thác)."""
        try:
            from ai_modules.shard_manager import search_index
            
            # Tìm theo topic + question keywords
            all_entries = search_index()
            if not all_entries:
                return "(Kho dữ liệu trống - Nhà Máy AI chưa khai thác)"
            
            # Lọc entries liên quan (fuzzy match)
            relevant = []
            search_terms = [topic.lower()] + [w.lower() for w in question.split() if len(w) > 2]
            
            for entry in all_entries:
                title = entry.get('title', '').lower()
                category = entry.get('category', '').lower()
                score = 0
                for term in search_terms:
                    if term in title:
                        score += 3
                    if term in category:
                        score += 1
                if score > 0:
                    relevant.append((score, entry))
            
            # Sắp xếp theo score và lấy top 5
            relevant.sort(key=lambda x: x[0], reverse=True)
            top_entries = relevant[:5]
            
            if not top_entries:
                # V5.1: Không fallback random → tránh pha loãng prompt
                return "(Không tìm thấy tri thức liên quan trong Kho Dữ Liệu)"
            
            # Build context string
            hub_context = f"📚 Kho Tri Thức AI ({len(all_entries)} chủ đề, {len(relevant)} liên quan):\n"
            for score, entry in top_entries:
                title = entry.get('title', 'N/A')
                content = entry.get('content', '')[:500]  # Giới hạn 500 ký tự mỗi entry
                category = entry.get('category', 'N/A')
                hub_context += f"\n--- [{category}] {title} ---\n{content}\n"
            
            return hub_context
        except Exception as e:
            return f"(Lỗi truy vấn kho tri thức: {e})"

    def _search_internet(self, question, topic="Chung"):
        """Tìm kiếm thông tin từ Internet để bổ sung cho AI."""
        try:
            # Chỉ tìm kiếm nếu câu hỏi đủ dài (không phải chào hỏi)
            if len(question.split()) < 3:
                return "(Câu hỏi quá ngắn, không cần tìm internet)"
            
            from ai_modules.web_searcher import get_web_searcher
            searcher = get_web_searcher()
            
            # Tạo query tìm kiếm: kết hợp câu hỏi + chủ đề
            search_query = f"{question} {topic} phong thủy huyền học" if topic != "Chung" else question
            
            # Tìm kiếm nhanh (3 kết quả)
            self.log_step("Internet Search", "RUNNING", f"Tìm kiếm: {search_query[:50]}...")
            results = searcher.search_google(search_query, num_results=3)
            
            if not results:
                self.log_step("Internet Search", "DONE", "Không tìm thấy kết quả internet")
                return "(Không tìm thấy thông tin internet liên quan)"
            
            # Tổng hợp kết quả
            internet_info = "🌐 THÔNG TIN TỪ INTERNET (đã chắt lọc):\n"
            for idx, r in enumerate(results, 1):
                internet_info += f"\n{idx}. {r.get('title', 'N/A')}\n"
                snippet = r.get('snippet', '')
                if snippet:
                    internet_info += f"   Tóm tắt: {snippet[:300]}\n"
            
            # Giới hạn tổng dữ liệu internet (tránh prompt quá dài)
            if len(internet_info) > 2000:
                internet_info = internet_info[:2000] + "\n...(đã cắt bớt)"
            
            self.log_step("Internet Search", "DONE", f"Tìm thấy {len(results)} nguồn internet")
            return internet_info
            
        except Exception as e:
            self.log_step("Internet Search", "SKIP", f"Lỗi internet: {str(e)[:50]}")
            return f"(Không thể tìm kiếm internet: {str(e)[:80]})"

    def analyze_luc_hao(self, luc_hao_data, topic="Chung"):
        """Phân tích chuyên sâu quẻ Lục Hào bằng AI Gemini với luật luận đoán chi tiết."""
        try:
            # Build comprehensive hexagram data string for AI
            ban = luc_hao_data.get('ban', {})
            bien = luc_hao_data.get('bien', {})
            dong_hao = luc_hao_data.get('dong_hao', [])
            the_ung = luc_hao_data.get('the_ung', '')
            
            # Format all line details
            ban_details = ""
            for d in ban.get('details', []):
                markers = d.get('marker', '')
                dong_mark = " ★ĐỘNG★" if d.get('is_moving') else ""
                line_type = "Dương ━━━" if d.get('line') == 1 else "Âm ━ ━"
                ban_details += f"  Hào {d['hao']}: {line_type} | {d.get('luc_than','')} | {d.get('can_chi','')} | {d.get('luc_thu','')} | {d.get('strength','')}{dong_mark} {markers}\n"
            
            bien_details = ""
            for d in bien.get('details', []):
                line_type = "Dương ━━━" if d.get('line') == 1 else "Âm ━ ━"
                bien_details += f"  Hào {d['hao']}: {line_type} | {d.get('luc_than','')} | {d.get('can_chi','')} | {d.get('luc_thu','')} | {d.get('strength','')}\n"
            
            # V12.2: Phục Thần data
            phuc_than_info = ""
            for pt in luc_hao_data.get('phuc_than', []):
                phuc_than_info += f"  ★ {pt['luc_than']} ({pt['can_chi']}) AN duoi Hao {pt['hao_pos']} (Phi Than: {pt['phi_than_luc_than']} {pt['phi_than_can_chi']}) — {pt['strength']}\n"
            
            expert_prompt = f"""BAN LA CHUYEN GIA LUC HAO KINH DICH — 50 nam kinh nghiem.

⛔ QUY TAC SO 1: TRA LOI THANG CAU HOI TRUOC, ROI MOI GIAI THICH.
⛔ TOI DA 500 CHU. KHONG DAI DONG.

═══════════════════════════════════
📌 CAU HOI CUA NGUOI DUNG: {topic}
═══════════════════════════════════

📜 QUE CHU: {ban.get('name', '')} — Ho {ban.get('palace', '')}
{ban_details}
📜 {the_ung}

🔄 QUE BIEN: {bien.get('name', '')}
{bien_details}

⚡ HAO DONG: {', '.join([str(h) for h in dong_hao]) if dong_hao else 'Khong co'}

{f'🔮 PHUC THAN (Luc Than an):{chr(10)}{phuc_than_info}' if phuc_than_info else ''}

═══════════════════════════════════
📋 BANG TRA DUNG THAN:
Tien/Tai = The Tai | Viec/Sep/Benh = Quan Quy | Con/Suc khoe = Tu Ton
Nha/Xe/Hoc/Thi = Phu Mau | Ban/Anh em = Huynh De

📋 QUY TAC DAC BIET:
★ HOI SO LUONG/TUOI: 
  - Tim Dung Than o hao nao → Can Chi → Ngu Hanh → quai tuong ung
  - So Tien Thien: Can=1, Doai=2, Ly=3, Chan=4, Ton=5, Kham=6, Can2=7, Khon=8
  - So Ha Do: Kham=1/6, Khon=2/7, Chan=3/8, Ton=4/9, Trung=5/10, Can=1/6, Doai=4/9, Can2=5/10, Ly=2/7
  - Vuong/Tuong → chon so LON. Suy/Tu → chon so NHO

★ HOI MAU SAC:
  - Kim = trang/bac | Moc = xanh la | Thuy = den/xanh dam | Hoa = do | Tho = vang/nau
  - Mau = Ngu Hanh cua Dung Than hoac hao lien quan

★ HOI HUONG:
  - Kham=Bac | Ly=Nam | Chan=Dong | Doai=Tay | Can=TayBac | Khon=TayNam | Can2=DongBac | Ton=DongNam

═══════════════════════════════════
📝 FORMAT TRA LOI (BAT BUOC):
═══════════════════════════════════

## 🏆 TRA LOI
[2-3 cau tra loi THANG cau hoi. Neu hoi so luong → cho 1 CON SO cu the. Neu hoi mau → cho MAU cu the.]

## 🔍 Can cu
- **Dung Than:** [La gi, o hao nao, Vuong/Suy]
- **Luc Hao:** [Hao dong anh huong gi? Nguyen Than/Ky Than?]
- **Phi Phuc:** [DT an o dau? Phi Than khac/sinh?]

## 💡 Khuyen
[1-2 cau khuyen cu the]

CHU Y: Tra loi TIENG VIET. PHAI DUT KHOAT — khong noi "chua ro rang"."""
            
            # Call Gemini AI
            response = self._call_ai_raw(expert_prompt)
            if response and len(response) > 50:
                return response
            
        except Exception as e:
            self.log_step("analyze_luc_hao", "⚠️", f"Gemini error: {str(e)[:100]}")
        
        # Fallback to offline expert
        try:
            from ai_modules.luc_hao_expert_ai import get_luc_hao_expert
            expert = get_luc_hao_expert()
            return expert.get_detailed_interpretation(luc_hao_data, topic)
        except:
            return self.fallback_helper.analyze_luc_hao(luc_hao_data, topic)
    
    def analyze_mai_hoa(self, mai_hoa_data, topic="Chung"):
        """Phân tích chuyên sâu quẻ Mai Hoa Dịch Số bằng AI Gemini."""
        try:
            mh_ten = mai_hoa_data.get('ten', '?')
            mh_tuong = mai_hoa_data.get('tuong', '?')
            mh_nghia = mai_hoa_data.get('nghia', mai_hoa_data.get('nghĩa', '?'))
            mh_dong = mai_hoa_data.get('dong_hao', '?')
            mh_upper_e = mai_hoa_data.get('upper_element', '?')
            mh_lower_e = mai_hoa_data.get('lower_element', '?')
            mh_upper_s = mai_hoa_data.get('upper_symbol', '?')
            mh_lower_s = mai_hoa_data.get('lower_symbol', '?')
            mh_bien = mai_hoa_data.get('ten_qua_bien', '?')
            interp = mai_hoa_data.get('interpretation', '')
            
            expert_prompt = f"""BAN LA CHUYEN GIA MAI HOA DICH SO — 50 nam kinh nghiem.

⛔ QUY TAC SO 1: TRA LOI THANG CAU HOI TRUOC, ROI MOI GIAI THICH.
⛔ TOI DA 500 CHU. KHONG DAI DONG.

═══════════════════════════════════
📌 CAU HOI CUA NGUOI DUNG: {topic}
═══════════════════════════════════

Que Chu: {mh_ten} ({mh_upper_s} / {mh_lower_s})
Tuong: {mh_tuong} | Y Nghia: {mh_nghia}
Ngoai quai: {mh_upper_s} (Hanh {mh_upper_e}) | Noi quai: {mh_lower_s} (Hanh {mh_lower_e})
Dong Hao: {mh_dong} | Que Bien: {mh_bien}

📋 QUY TAC:
- THE = quai KHONG dong. DUNG = quai CO dong
- The sinh Dung = bat loi. Dung sinh The = CAT. The khac Dung = CAT. Dung khac The = HUNG
- Ho Quai = dien bien giua. Bien Quai = ket qua cuoi

★ HOI SO LUONG: So Tien Thien (Can=1,Doai=2,Ly=3,Chan=4,Ton=5,Kham=6,Can2=7,Khon=8). Vuong→so LON, Suy→so NHO
★ HOI MAU: Kim=trang/bac | Moc=xanh | Thuy=den | Hoa=do | Tho=vang/nau
★ HOI HUONG: Kham=Bac | Ly=Nam | Chan=Dong | Doai=Tay

📝 FORMAT (BAT BUOC):

## 🏆 TRA LOI
[2-3 cau tra loi THANG. Neu hoi so → cho CON SO. Neu hoi mau → cho MAU.]

## 🔍 Can cu
- **The-Dung:** [Quan he? Vuong/Suy?]
- **Ho+Bien Quai:** [Tac dong gi?]

## 💡 Khuyen
[1-2 cau]

Tra loi TIENG VIET. PHAI DUT KHOAT."""
            
            response = self._call_ai_raw(expert_prompt)
            if response and len(response) > 50:
                return response

        except Exception as e:
            self.log_step("analyze_mai_hoa", "ERR", f"Gemini error: {str(e)[:80]}")
        
        return f"⚠️ AI Online khong kha dung. Luan giai offline: {mai_hoa_data.get('interpretation', 'Khong co du lieu')}"
    
    def analyze_thiet_ban(self, chart_data, topic="Chung"):
        """Phân tích chuyên sâu Thiết Bản Thần Toán bằng AI Gemini."""
        try:
            # Lay du lieu tu chart
            can_nam = chart_data.get('can_nam', '?')
            chi_nam = chart_data.get('chi_nam', '?')
            can_ngay = chart_data.get('can_ngay', '?')
            chi_ngay = chart_data.get('chi_ngay', '?')
            
            # Load Thiet Ban data
            tb_data = self._load_thiet_ban_data()
            if not tb_data:
                return "Khong co du lieu Thiet Ban"
            
            hoa_giap = tb_data.get("LUC_THAP_HOA_GIAP_NAP_AM", {})
            nam_tru = f"{can_nam} {chi_nam}"
            ngay_tru = f"{can_ngay} {chi_ngay}"
            na_nam = hoa_giap.get(nam_tru, {})
            na_ngay = hoa_giap.get(ngay_tru, {})
            
            # Truong Sinh
            truong_sinh = tb_data.get("TRUONG_SINH_12_GIAI_DOAN", {})
            
            expert_prompt = f"""BAN LA CHUYEN GIA THIET BAN THAN TOAN.

⛔ QUY TAC SO 1: TRA LOI THANG CAU HOI TRUOC, ROI MOI GIAI THICH.
⛔ TOI DA 500 CHU. KHONG DAI DONG.

═══════════════════════════════════
📌 CAU HOI CUA NGUOI DUNG: {topic}
═══════════════════════════════════

Tu Tru: {can_nam} {chi_nam} / {chart_data.get('can_thang','?')} {chart_data.get('chi_thang','?')} / {can_ngay} {chi_ngay} / {chart_data.get('can_gio','?')} {chart_data.get('chi_gio','?')}
Menh Nam ({nam_tru}): {na_nam.get('Nap_Am', '?')} (Hanh {na_nam.get('Hanh', '?')}) — {na_nam.get('Y_Nghia', '')}
Menh Ngay ({ngay_tru}): {na_ngay.get('Nap_Am', '?')} (Hanh {na_ngay.get('Hanh', '?')}) — {na_ngay.get('Y_Nghia', '')}

📋 QUY TAC:
- Nap Am = tinh cach, van menh. Hanh Nap Am vs Hanh Menh = sinh/khac?
- Truong Sinh 12 giai doan: Thai→Duong→Truong Sinh→Lam Quan→De Vuong→Suy→Benh→Tu→Mo→Tuyet→Thai→Duong
- Than Sat: Quy Nhan=tot, Van Xuong=hoc, Kiem Sat=khac nghiet

★ HOI MAU: Kim=trang/bac | Moc=xanh | Thuy=den | Hoa=do | Tho=vang/nau
★ HOI SO: So theo Ngu Hanh (Thuy=1/6, Hoa=2/7, Moc=3/8, Kim=4/9, Tho=5/10)

📝 FORMAT (BAT BUOC):

## 🏆 TRA LOI
[2-3 cau tra loi THANG cau hoi.]

## 🔍 Can cu
- **Nap Am:** [Menh gi? Hanh gi? Tuong trung?]
- **Truong Sinh:** [Dang o giai doan nao?]

## 💡 Khuyen
[1-2 cau]

Tra loi TIENG VIET. PHAI DUT KHOAT."""
            
            response = self._call_ai_raw(expert_prompt)
            if response and len(response) > 50:
                return response

        except Exception as e:
            self.log_step("analyze_thiet_ban", "ERR", f"Gemini error: {str(e)[:80]}")
        
        return "⚠️ AI Online khong kha dung cho Thiet Ban."
    
    def _get_chat_history(self):
        """Lấy lịch sử hội thoại để AI nhớ ngữ cảnh các câu hỏi trước."""
        try:
            if hasattr(st, 'session_state') and 'chat_history' in st.session_state:
                hist = st.session_state.chat_history[-6:]  # V5.1: Max 3 cặp Q&A (6 messages) → giảm noise
                if not hist:
                    return "(Chưa có lịch sử hội thoại)"
                lines = []
                for m in hist:
                    role_label = "👤 NGƯỜI DÙNG" if m['role'] == 'user' else "🤖 AI"
                    content = m['content'][:200]  # V5.1: Giảm từ 500→200 → giảm prompt length
                    lines.append(f"{role_label}: {content}")
                return "\n".join(lines)
        except: pass
        return "(Chưa có lịch sử hội thoại)"


    def _process_response(self, text):
        if not text:
            return "⚠️ AI không trả lời được."
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

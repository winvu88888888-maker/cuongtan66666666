"""
Enhanced Gemini Helper with Context Awareness
Gemini sẽ tự động biết ngữ cảnh: cung nào, chủ đề gì, đang xem phần nào
"""

import google.generativeai as genai
import os
import requests
import json

CUNG_NGU_HANH = {
    1: "Thủy",
    2: "Thổ",
    3: "Mộc",
    4: "Mộc",
    5: "Thổ",
    6: "Kim",
    7: "Kim",
    8: "Thổ",
    9: "Hỏa"
}

CUNG_TEN = {
    1: "Khảm (Thủy)",
    2: "Khôn (Thổ)",
    3: "Chấn (Mộc)",
    4: "Tốn (Mộc)",
    5: "Trung Cung (Thổ)",
    6: "Càn (Kim)",
    7: "Đoài (Kim)",
    8: "Cấn (Thổ)",
    9: "Ly (Hỏa)"
}

class GeminiQMDGHelper:
    """Helper class with context awareness for QMDG analysis"""
    
    def __init__(self, api_key):
        """Initialize Gemini with API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self._failed_models = set() # Track exhausted models
        
        # Context tracking
        self.current_context = {
            'topic': None,
            'palace': None,
            'chart_data': None,
            'last_action': None,
            'dung_than': []
        }
        
        # Adaptive model selection
        self.model = self._get_best_model()

        # n8n endpoint (optional)
        self.n8n_url = None
    
    def set_n8n_url(self, url):
        """Set n8n webhook URL for processing"""
        self.n8n_url = url

    def _get_best_model(self):
        """Find the best available model for the current API key"""
        # Prioritize 1.5 Pro because "gemini tốt nhất"
        models_to_try = [
            'gemini-2.0-flash-exp', # Try latest 2.0 flash
            'gemini-1.5-pro-latest', 
            'gemini-1.5-pro',
            'gemini-1.5-flash-latest', 
            'gemini-1.5-flash',
            'gemini-pro', 
            'gemini-1.0-pro'
        ]
        
        last_error = "Unknown error"
        for model_name in models_to_try:
            if model_name in self._failed_models: continue # Skip known broken models
            try:
                model = genai.GenerativeModel(model_name)
                # Quick test with low tokens
                model.generate_content("ping", generation_config={"max_output_tokens": 1})
                return model
            except Exception as e:
                last_error = str(e)
                if "429" in last_error or "quota" in last_error.lower():
                    self._failed_models.add(model_name)
                continue
        
        # Fallback to list models if configured ones fail
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    name = m.name.split('/')[-1]
                    if name in self._failed_models: continue
                    try:
                        model = genai.GenerativeModel(name)
                        model.generate_content("ping", generation_config={"max_output_tokens": 1})
                        return model
                    except: continue
        except Exception: pass
        
        # Ultimate fallback but store error info
        self.last_startup_error = last_error
        return genai.GenerativeModel('gemini-1.5-flash') # Default to flash as it's more widely available

    def test_connection(self):
        """Quickly test if the API key and model are working"""
        try:
            response = self.model.generate_content("Xin chào?", generation_config={"max_output_tokens": 5})
            if response.text:
                return True, "Kết nối thành công!"
            return False, "Không nhận được phản hồi từ AI."
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                return False, "API Key không chính xác."
            elif "429" in error_msg or "quota" in error_msg.lower():
                return False, "Đã hết hạn mức sử dụng (Quota) cho model này."
            return False, f"Lỗi: {error_msg}"

    def _call_ai(self, prompt):
        """Call AI with auto-switch fallback on quota failure"""
        # Option 1: Use n8n if configured
        if self.n8n_url:
            try:
                payload = {
                    "prompt": prompt,
                    "api_key": self.api_key
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(self.n8n_url, json=payload, headers=headers, timeout=60)
                if response.status_code == 200:
                    text = response.json().get('text', '')
                    if text: return text
                    # If empty text, fallback might be needed or return empty
                else:
                    print(f"n8n Error: {response.text}")
            except Exception as e:
                print(f"n8n Exception: {e}")
                # Fallback to local
        
        # Option 2: Direct Gemini API with Swapping
        import time
        for attempt in range(3): # 3 attempts, potentially 3 different models
            try:
                response = self.model.generate_content(prompt)
                if not response.text:
                    return "⚠️ AI trả về kết quả trống."
                return response.text
            except Exception as e:
                error_msg = str(e)
                model_name = getattr(self.model, 'model_name', 'unknown').split('/')[-1]
                
                # Quota Failure (429) -> Switch Model
                if "429" in error_msg or "quota" in error_msg.lower():
                    self._failed_models.add(model_name)
                    print(f"Model {model_name} exhausted. Switching...")
                    self.model = self._get_best_model() # Try to get a NEW model
                    time.sleep(1)
                    continue
                
                # Safety Block
                if "SAFETY" in error_msg or "blocked" in error_msg.lower():
                    return "🛡️ Nội dung bị chặn do quy tắc an toàn. Thử đổi chủ đề."
                
                # If it's the last attempt or a different error, return or raise
                if attempt == 2:
                    return f"❌ Lỗi AI: {error_msg}\n\nVui lòng đợi hoặc đổi API Key."
                time.sleep(0.5)
        return "🛑 **Hết hạn mức AI trên tất cả các dòng model:** Bạn đã dùng hết quota MIỄN PHÍ hằng ngày. Vui lòng thử lại vào ngày mai hoặc dùng API Key khác."
    
    def update_context(self, **kwargs):
        """Update current context"""
        self.current_context.update(kwargs)
    
    def get_system_knowledge(self):
        """Returns string representation of key system rules for AI context"""
        knowledge = """
**QUY TẮC LUẬN GIẢI CHUYÊN SÂU:**
1. **Nguyên lý Sinh Khắc Cung:** 
   - Thủy (1) -> Mộc (3,4) -> Hỏa (9) -> Thổ (2,8,5) -> Kim (6,7) -> Thủy (1).
   - Khắc: Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy.
2. **Dụng Thần (Object):** Là yếu tố đại diện cho sự việc cần xem.
3. **Bản Thân (Subject):** Đại diện bởi Can Ngày (Thiên bàn) hoặc cung của người hỏi.
4. **Phân tích nội cung:** 
   - Sao (Thiên thời), Môn (Địa lợi - Nhân hòa), Thần (Thần trợ), Không Vong (Trạng thái rỗng, chưa tới lúc hoặc thất bại).
5. **KẾT LUẬN:** Dựa trên việc Cung Dụng Thần Sinh cho hay Khắc Cung Bản Thần (hoặc ngược lại).
"""
        return knowledge

    def get_context_prompt(self):
        """Build context prompt from current state"""
        context_parts = []
        
        # Add system-wide knowledge
        context_parts.append(self.get_system_knowledge())
        
        if self.current_context.get('topic'):
            context_parts.append(f"**Chủ đề hiện tại:** {self.current_context['topic']}")
        
        if self.current_context.get('palace'):
            palace = self.current_context['palace']
            context_parts.append(f"**Đang xem cung:** Cung {palace.get('num', 'N/A')} - {palace.get('qua', 'N/A')}")
            context_parts.append(f"  - Sao: {palace.get('star', 'N/A')}")
            context_parts.append(f"  - Môn: {palace.get('door', 'N/A')}")
            context_parts.append(f"  - Thần: {palace.get('deity', 'N/A')}")
        
        if self.current_context.get('dung_than'):
            context_parts.append(f"**Dụng Thần:** {', '.join(self.current_context['dung_than'])}")
        
        if self.current_context.get('last_action'):
            context_parts.append(f"**Hành động trước:** {self.current_context['last_action']}")
        
        if context_parts:
            return "\n".join(["**NGỮ CẢNH VÀ KIẾN THỨC HIỆN TẠI:**"] + context_parts) + "\n\n"
        return ""
    
    def analyze_palace(self, palace_data, topic):
        """
        Analyze a specific palace with AI - FOCUS ON ESSENTIALS
        """
        # Update context
        self.update_context(
            topic=topic,
            palace=palace_data,
            last_action=f"Phân tích Cung {palace_data.get('num')}"
        )
        
        context = self.get_context_prompt()
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giáp hàng đầu. Hãy phân tích Cung {palace_data.get('num', 'N/A')} cho chủ đề: **{topic}**.

**NGUYÊN TẮC: NGẮN GỌN - ĐỦ Ý - KHÔNG LAN MAN.**

**Yêu cầu:**
1. **Giá trị của cung**: Cung này là Thuận hay Nghịch cho việc "{topic}"?
2. **Điểm nhấn chính**: Tổ hợp Sao/Môn/Thần/Can tại đây báo hiệu điều gì cốt lõi nhất?
3. **Chiến thuật hành động**: Làm gì ngay tại cung này để đạt mục tiêu?

Trả lời súc tích, đi thẳng vào vấn đề, không chào hỏi, không dẫn nhập."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}\n\nVui lòng kiểm tra API key hoặc thử lại."
    
    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None, topic_hints="", subj_stem=None, obj_stem=None, subj_label="Bản thân"):
        """
        Expert Consultation: Human-Centric Narrative with Deep Elemental Detail.
        """
        # Update context
        self.update_context(
            topic=topic,
            chart_data=chart_data,
            dung_than=dung_than_info or [],
            last_action=f"Tư vấn chuyên sâu cho {subj_label}"
        )
        
        can_ngay = chart_data.get('can_ngay', 'N/A')
        can_gio = chart_data.get('can_gio', 'N/A')
        truc_phu = chart_data.get('truc_phu_ten', 'N/A')
        truc_su = chart_data.get('truc_su_ten', 'N/A')
        khong_vong_list = chart_data.get('khong_vong', [])
        dich_ma_cung = chart_data.get('dich_ma', None)
        
        # Determine actual actors for this session
        final_subj_stem = subj_stem if subj_stem else can_ngay
        final_obj_stem = obj_stem if obj_stem else can_gio
        
        # Mapping for human-centric roles
        role_map = {
            final_subj_stem: subj_label,
            # If the user is asking about someone else, Day Stem might still be "Bạn (Người hỏi)"
            can_ngay: "Bạn (Người hỏi)" if final_subj_stem != can_ngay else subj_label,
            final_obj_stem: "Đối tượng/Người mua/Đối phương" if final_obj_stem != can_gio else "Đối tượng (Can Giờ)"
        }
        
        # 1. GROUP DATA BY PALACE
        palaces_of_interest = {} # {palace_num: {info}}
        
        def add_to_poi(p_num, label):
            if p_num not in palaces_of_interest:
                palaces_of_interest[p_num] = {
                    'labels': [],
                    'star': chart_data.get('thien_ban', {}).get(p_num, 'N/A'),
                    'door': chart_data.get('nhan_ban', {}).get(p_num, 'N/A'),
                    'deity': chart_data.get('than_ban', {}).get(p_num, 'N/A'),
                    'can_thien': chart_data.get('can_thien_ban', {}).get(p_num, 'N/A'),
                    'can_dia': chart_data.get('dia_can', {}).get(p_num, 'N/A'),
                    'hanh': CUNG_NGU_HANH.get(p_num, 'N/A'),
                    'void': p_num in khong_vong_list,
                    'horse': p_num == dich_ma_cung
                }
            if label not in palaces_of_interest[p_num]['labels']:
                palaces_of_interest[p_num]['labels'].append(label)

        # Scan all palaces for actors and Useful Gods
        for i in range(1, 10):
            can_thien_p = chart_data.get('can_thien_ban', {}).get(i)
            # 1. Check for Roles (Bản thân, Anh chị...)
            if can_thien_p in role_map:
                add_to_poi(i, role_map[can_thien_p])
            
            # 2. Check for Dụng Thần Topic
            if dung_than_info:
                for dt in dung_than_info:
                    door_val = chart_data.get('nhan_ban', {}).get(i)
                    if (chart_data.get('thien_ban', {}).get(i) == dt or 
                        door_val == dt or 
                        chart_data.get('than_ban', {}).get(i) == dt or 
                        can_thien_p == dt or
                        (dt.split(' (')[0] if ' (' in dt else dt) in [door_val, f"{door_val} Môn"]):
                        add_to_poi(i, dt)
        
        # 2. CONTEXTUAL PROMPT
        poi_desc = []
        from qmdg_data import KY_MON_DATA
        
        for p_num, info in palaces_of_interest.items():
            labels_str = ", ".join(info['labels'])
            void_str = " [📍 KHÔNG VONG - Sự việc bế tắc/Trống rỗng]" if info['void'] else ""
            horse_str = " [🐎 DỊCH MÃ - Sự chuyển dịch/Nhanh chóng]" if info['horse'] else ""
            p_name = CUNG_TEN.get(p_num, f"Cung {p_num}")
            
            # Detailed Symbolism Lookup
            star_prop = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(info['star'], {}).get('Tính_Chất', 'Bình')
            door_prop = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(info['door'] if " Môn" in info['door'] else f"{info['door']} Môn", {}).get('Luận_Đoán', 'Bình')
            deity_prop = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(info['deity'], {}).get('Tính_Chất', 'Bình')
            can_prop = KY_MON_DATA['CAN_CHI_LUAN_GIAI'].get(info['can_thien'], {}).get('Tính_Chất', 'Bình')
            
            desc = (f"- **{p_name} (Cung {p_num})**: Đại diện cho **{labels_str}**.\n"
                    f"  + Thành phần: Sao {info['star']} ({star_prop}), Môn {info['door']} ({door_prop}), Thần {info['deity']} ({deity_prop}).\n"
                    f"  + Thiên Can: {info['can_thien']} ({can_prop}) lâm trên {info['can_dia']}.\n"
                    f"  + Đặc tính: {info['hanh']}{void_str}{horse_str}.")
            poi_desc.append(desc)

        prompt = f"""{self.get_context_prompt()}Bạn là bậc thầy Kỳ Môn Độn Giáp tư vấn riêng cho **{subj_label}**. Hãy thực hiện LUẬN GIẢI CHI TIẾT NHÂN QUẢ cho chủ đề: **{topic}**.

**NGUYÊN TẮC NGÔN NGỮ BẮT BUỘC:**
1. **Dùng tên gọi gần gũi**: Tuyệt đối không gọi là "Chủ thể", "Khách". Hãy gọi là **"{subj_label}"**, **"Người mua"**, **"Ngôi nhà"**, **"Công việc"**... tùy theo ngữ cảnh.
2. **Tư duy Ngũ Hành**: Khi phân tích một cung, hãy giải thích: "Vì Sao/Môn này thuộc hành X, tương tác với cung Y nên kết quả là Z". 
3. **Phân tích Động cơ (Lý do)**: Dựa vào các tính chất Sao/Môn/Thần, hãy chỉ rõ lý do tại sao sự việc diễn ra (Ví dụ: Vì có Bạch Hổ nên {subj_label} đang gặp áp lực rất lớn về nợ nần/sức khỏe).

**CẤU TRÚC BÁO CÁO:**

**1. ĐỊNH VỊ NHÂN VẬT & MỤC TIÊU** (Liệt kê rõ ai/cái gì ở cung nào, số mấy).
**2. PHÂN TÍCH CHI TIẾT NỘI TẠI** (Bóc tách Ngũ hành, Sao/Môn/Thần và các dấu hiệu Dịch Mã/Không Vong để nói rõ trạng thái tâm lý/năng lực của {subj_label} và đối tác).
**3. LUẬN GIẢI TƯƠNG TÁC (NHÂN - QUẢ)** (Sự kết nối giữa các cung vị đã nêu).
**4. LỜI KHUYÊN CHIẾN THUẬT & PHÁN QUYẾT** (Kết quả cuối cùng và bước đi thông minh nhất).

**DỮ LIỆU CUNG VỊ CHI TIẾT:**
{chr(10).join(poi_desc)}

**THẾ TRẬN TỔNG QUAN:**
- Xu thế (Trực Phù): {truc_phu}
- Chấp hành (Trực Sử): {truc_su}
- Gợi ý định hướng: "{topic_hints}"

Trả lời bằng phong thái chuyên gia tư vấn tận tâm, ngôn ngữ giàu hình ảnh và sắc bén."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}"
    
    def answer_question(self, question, chart_data=None, topic=None):
        """
        Answer with FULL CONTEXT AWARENESS
        """
        # Use stored context if not provided
        if chart_data is None:
            chart_data = self.current_context.get('chart_data')
        if topic is None:
            topic = self.current_context.get('topic', 'Chung')
        
        # Update context
        self.update_context(
            topic=topic,
            chart_data=chart_data,
            last_action=f"Hỏi: {question[:50]}..."
        )
        
        context = self.get_context_prompt()
        
        # Build chart context if available
        chart_context = ""
        if chart_data:
            palace_summary = []
            for i in range(1, 10):
                palace_summary.append(
                    f"Cung {i}: {chart_data.get('thien_ban', {}).get(i, 'N/A')} - "
                    f"{chart_data.get('nhan_ban', {}).get(i, 'N/A')} - "
                    f"{chart_data.get('than_ban', {}).get(i, 'N/A')}"
                )
            chart_context = "\n**Bàn Kỳ Môn hiện tại:**\n" + "\n".join(palace_summary)
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giáp.

**Bối cảnh:**
- Chủ đề: {topic}
{chart_context}

**Câu hỏi của người dùng:**
{question}

Hãy trả lời câu hỏi dựa trên:
1. Ngữ cảnh hiện tại (chủ đề, cung đang xem, hành động trước)
2. Thông tin từ bàn Kỳ Môn (nếu có)
3. Kiến thức về dịch học
4. Nguyên lý Ngũ hành, Bát quái

Trả lời CỰC KỲ NGẮN GỌN (tối đa 3-5 câu), tập trung vào thực tế, không lý thuyết suông."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi: {str(e)}"
    
    def explain_element(self, element_type, element_name):
        """
        Explain element with context
        """
        # Update context
        self.update_context(
            last_action=f"Giải thích {element_type}: {element_name}"
        )
        
        context = self.get_context_prompt()
        
        type_map = {
            'star': 'Tinh (Sao)',
            'door': 'Môn (Cửa)',
            'deity': 'Thần',
            'stem': 'Can (Thiên Can)'
        }
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giáp.

Hãy giải thích CỐT LÕI về {type_map.get(element_type, element_type)}: **{element_name}**

**Yêu cầu (Tối đa 3-4 dòng):**
1. Bản chất cốt lõi (Cát/Hung/Ngũ hành).
2. Tác động chính đến vận mệnh/công việc.
3. Lời khuyên nhanh khi gặp yếu tố này.

Bỏ qua nguồn gốc, ví dụ hay dẫn giải dài dòng. Trả lời sắc bén, súc tích."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi: {str(e)}"

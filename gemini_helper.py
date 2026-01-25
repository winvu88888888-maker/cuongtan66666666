"""
Enhanced Gemini Helper with Context Awareness
Gemini sẽ tự động biết ngữ cảnh: cung nào, chủ đề gì, đang xem phần nào
"""

import google.generativeai as genai
import os
import requests
import json

class GeminiQMDGHelper:
    """Helper class with context awareness for QMDG analysis"""
    
    def __init__(self, api_key):
        """Initialize Gemini with API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Context tracking - Initialize BEFORE model selection
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
            try:
                model = genai.GenerativeModel(model_name)
                # Quick test with low tokens
                model.generate_content("ping", generation_config={"max_output_tokens": 1})
                return model
            except Exception as e:
                last_error = str(e)
                continue
        
        # Fallback to list models if configured ones fail
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    name = m.name.split('/')[-1]
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
            response = self.model.generate_content("Xin chào, bạn có khỏe không?", generation_config={"max_output_tokens": 20})
            if response.text:
                return True, "Kết nối thành công!"
            return False, "Không nhận được phản hồi từ AI."
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                return False, "API Key không chính xác hoặc đã hết hạn."
            elif "quota" in error_msg.lower():
                return False, "Đã hết hạn mức sử dụng (Quota) cho Key này."
            return False, f"Lỗi kết nối: {error_msg}"

    def _call_ai(self, prompt):
        """Call AI via n8n or direct Gemini API"""
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
        
        # Option 2: Direct Gemini API
        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                return "⚠️ AI trả về kết quả trống. Thử lại sau hoặc kiểm tra API Key."
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "finish_reason: SAFETY" in error_msg:
                return "🛡️ Nội dung bị AI chặn do vi phạm quy tắc an toàn. Thử đặt câu hỏi khác."
            raise e # Let the helper handle more complex errors if needed
    
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
    
    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None, topic_hints=""):
        """
        Multi-Factor Relational Analysis: Comparing Buyer, Price, Seller, etc.
        """
        # Update context
        self.update_context(
            topic=topic,
            chart_data=chart_data,
            dung_than=dung_than_info or [],
            last_action="Luận giải trọng tâm Dụng Thần (Đa tầng)"
        )
        
        # 1. SCAN FOR CORE ACTORS
        can_ngay = chart_data.get('can_ngay', 'N/A')
        can_gio = chart_data.get('can_gio', 'N/A')
        truc_phu = chart_data.get('truc_phu_ten', 'N/A')
        truc_su = chart_data.get('truc_su_ten', 'N/A')
        
        self_palace = "?"
        dung_than_details = []
        process_palace = "?"
        
        for i in range(1, 10):
            # Locate Self (Seller/Subject)
            if chart_data.get('can_thien_ban', {}).get(i) == can_ngay:
                self_palace = str(i)
            # Locate Outcome (Outcome/Timing)
            if chart_data.get('can_thien_ban', {}).get(i) == can_gio:
                process_palace = str(i)
            # Locate Topic Factors (Dụng Thần)
            if dung_than_info:
                for dt in dung_than_info:
                    door_val = chart_data.get('nhan_ban', {}).get(i)
                    if (chart_data.get('thien_ban', {}).get(i) == dt or 
                        door_val == dt or 
                        chart_data.get('than_ban', {}).get(i) == dt or 
                        chart_data.get('can_thien_ban', {}).get(i) == dt or
                        (dt.endswith(" Môn") and door_val and door_val in dt)):
                        
                        detail = {
                            'dt': dt,
                            'palace': i,
                            'star': chart_data.get('thien_ban', {}).get(i),
                            'door': door_val,
                            'deity': chart_data.get('than_ban', {}).get(i),
                            'void': i in chart_data.get('khong_vong', [])
                        }
                        dung_than_details.append(detail)
        
        # 2. CONTEXTUAL PROMPT
        prompt = f"""{self.get_context_prompt()}Bạn là bậc thầy Kỳ Môn Độn Giáp. Hãy thực hiện LUẬN GIẢI ĐA TẦNG cho chủ đề: **{topic}**.

**NGUYÊN TẮC LUẬN GIẢI:**
- CHỈ phân tích các cung có Dụng Thần hoặc Bản Thân. KHÔNG liệt kê các cung khác.
- SO SÁNH các Dụng Thần với nhau (ví dụ: Người mua so với Giá bán, hoặc Công việc so với Tiền bạc).
- SỬ DỤNG gợi ý sau để định hướng: "{topic_hints}"

**THÔNG TIN BÀN CỜ:**
1. **Bản Thân (Can Ngày):** Cung {self_palace} (Sao {chart_data.get('thien_ban', {}).get(int(self_palace) if self_palace.isdigit() else 1)}, Môn {chart_data.get('nhan_ban', {}).get(int(self_palace) if self_palace.isdigit() else 1)}).
2. **Các Nhân Tố Dụng Thần ({topic}):** 
   {chr(10).join([f"- {d['dt']} tại Cung {d['palace']} (Môn {d['door']}, Thần {d['deity']}{', KHÔNG VONG' if d['void'] else ''})" for d in dung_than_details])}
3. **Diễn biến (Can Giờ):** Cung {process_palace}.
4. **Cơ cấu lãnh đạo:** {truc_phu} (Xu thế), {truc_su} (Chấp hành).

**YÊU CẦU NỘI DUNG (SÚC TÍCH):**

- **PHẦN 1: TƯƠNG QUAN DỤNG THẦN (Cốt lõi):** So sánh quan hệ giữa các nhân tố trên. Ví dụ: Dụng thần Người mua có phối hợp với Dụng thần Giá bán không? Cả hai có Sinh cho Bản thân không?
- **PHẦN 2: KẾT LUẬN & CHIẾN THUẬT:** Dựa trên gợi ý "{topic_hints}", hãy cho biết kết quả là thắng hay bại? Phải làm gì để chốt hạ vấn đề?
- **PHẦN 3: ỨNG KỲ:** Thời điểm chính xác (Dựa trên Cung Can Giờ {process_palace}).

Trả lời sắc bén, lạnh lùng, tập trung 100% vào việc ra quyết định."""

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

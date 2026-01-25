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
**KIẾN THỨC HỆ THỐNG KỲ MÔN:**
- Hệ thống sử dụng Ma trận Sinh Khắc: Mộc sinh Hỏa, Hỏa sinh Thổ, Thổ sinh Kim, Kim sinh Thủy, Thủy sinh Mộc.
- Các cung: 1 (Khảm - Thủy), 2 (Khôn - Thổ), 3 (Chấn - Mộc), 4 (Tốn - Mộc), 6 (Càn - Kim), 7 (Đoài - Kim), 8 (Cấn - Thổ), 9 (Ly - Hỏa).
- Trực Phù là yếu tố lãnh đạo, Trực Sử là việc thực thi.
- Dụng Thần quan trọng: 
  + Hôn nhân: Ất (Nữ), Canh (Nam), Lục Hợp (Hợp tác).
  + Kinh doanh: Sinh Môn (Lợi nhuận), Mậu (Vốn).
  + Bệnh tật: Thiên Nhuế (Bệnh), Thiên Tâm/Ất (Thầy thuốc/Thuốc).
- Các thần: Trực Phù (Cát), Đằng Xà (Quái dị), Thái Âm (Mưu mẹo), Lục Hợp (Hòa hợp), Bạch Hổ (Sát phạt), Huyền Vũ (Tối tăm), Cửu Địa (Bền vững), Cửu Thiên (Phát triển).
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
        Analyze a specific palace with AI - WITH CONTEXT
        """
        # Update context
        self.update_context(
            topic=topic,
            palace=palace_data,
            last_action=f"Phân tích Cung {palace_data.get('num')}"
        )
        
        context = self.get_context_prompt()
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giáp với kiến thức sâu rộng về dịch học Trung Hoa.

Hãy phân tích cung sau một cách chi tiết và dễ hiểu:

**Thông tin cung:**
- Cung số: {palace_data.get('num', 'N/A')}
- Quái tượng: {palace_data.get('qua', 'N/A')}
- Ngũ hành: {palace_data.get('hanh', 'N/A')}
- Tinh (Sao): {palace_data.get('star', 'N/A')}
- Môn (Cửa): {palace_data.get('door', 'N/A')}
- Thần: {palace_data.get('deity', 'N/A')}
- Can Thiên: {palace_data.get('can_thien', 'N/A')}
- Can Địa: {palace_data.get('can_dia', 'N/A')}

**Chủ đề đang xem:** {topic}

Hãy phân tích theo cấu trúc sau:

1. **Ý nghĩa tổng quan**: Cung này đại diện cho điều gì trong chủ đề "{topic}"?

2. **Phân tích các yếu tố**:
   - Tinh {palace_data.get('star', 'N/A')} mang ý nghĩa gì?
   - Môn {palace_data.get('door', 'N/A')} báo hiệu điều gì?
   - Thần {palace_data.get('deity', 'N/A')} ảnh hưởng như thế nào?
   - Tổ hợp Can {palace_data.get('can_thien', 'N/A')}/{palace_data.get('can_dia', 'N/A')} có ý nghĩa gì?

3. **Tương tác giữa các yếu tố**: Các yếu tố này kết hợp với nhau tạo ra thông điệp gì?

4. **Điềm báo**: Cát hay hung? Mức độ như thế nào?

5. **Lời khuyên cụ thể**: Nên làm gì? Tránh điều gì?

Trả lời bằng tiếng Việt, ngắn gọn nhưng đầy đủ ý nghĩa."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}\n\nVui lòng kiểm tra API key hoặc thử lại."
    
    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None):
        """
        Comprehensive analysis with FULL CONTEXT
        """
        # Update context
        self.update_context(
            topic=topic,
            chart_data=chart_data,
            dung_than=dung_than_info or [],
            last_action="Phân tích tổng hợp toàn bàn"
        )
        
        context = self.get_context_prompt()
        
        # Build palace summary
        palace_summary = []
        for i in range(1, 10):
            palace_summary.append(f"""
Cung {i}:
- Tinh: {chart_data.get('thien_ban', {}).get(i, 'N/A')}
- Môn: {chart_data.get('nhan_ban', {}).get(i, 'N/A')}
- Thần: {chart_data.get('than_ban', {}).get(i, 'N/A')}
- Can: {chart_data.get('can_thien_ban', {}).get(i, 'N/A')}/{chart_data.get('dia_can', {}).get(i, 'N/A')}
""")
        
        palaces_text = "\n".join(palace_summary)
        
        dung_than_text = ""
        if dung_than_info:
            dung_than_text = f"\n**Dụng Thần cần chú ý:** {', '.join(dung_than_info)}"
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giáp hàng đầu.

Hãy phân tích TỔNG QUAN toàn bộ bàn Kỳ Môn sau cho chủ đề: **{topic}**

**Thông tin bàn:**
{palaces_text}
{dung_than_text}

Hãy phân tích theo cấu trúc:

1. **Tổng quan tình hình** (2-3 câu): Nhìn chung tình hình như thế nào?

2. **Các điểm mạnh**: Những cung/yếu tố nào thuận lợi? Tại sao?

3. **Các điểm yếu**: Những cung/yếu tố nào bất lợi? Cần lưu ý gì?

4. **Tương tác quan trọng**: Có tương tác đặc biệt nào giữa các cung không?

5. **Thời điểm**: Khi nào là thời điểm tốt/xấu?

6. **Lời khuyên tổng hợp**: 
   - Nên làm gì?
   - Không nên làm gì?
   - Chiến lược tổng thể?

7. **Dự đoán kết quả**: Khả năng thành công? Cần chuẩn bị gì?

Trả lời bằng tiếng Việt, cụ thể và thực tế."""

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

Trả lời ngắn gọn, dễ hiểu, cụ thể và thực tế bằng tiếng Việt."""

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

Hãy giải thích chi tiết về {type_map.get(element_type, element_type)}: **{element_name}**

Bao gồm:
1. Nguồn gốc và ý nghĩa
2. Thuộc tính (Ngũ hành, âm dương, v.v.)
3. Tính chất (cát/hung, đặc điểm)
4. Ứng dụng trong luận đoán
5. Ví dụ cụ thể

Giải thích dễ hiểu, bằng tiếng Việt."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi: {str(e)}"

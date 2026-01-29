import json
import random

class MiningStrategist:
    """The Mega-Brain managing 50 specialized AI Mining Agents."""
    
    def __init__(self):
        # EXPANDED TO 100+ SPECIALIZED TOPICS FOR 50 AI AGENTS
        self.categories = {
            "Kỳ Môn Độn Giáp": [
                "Bản văn cổ Kỳ Môn Độn Giáp bí truyền", "Kỳ Môn Độn Giáp: Giải mã Bát Môn thần đoán", 
                "Cửu Tinh và Thần Sát trong Kỳ Môn: Nguyên lý gốc", "Kỳ Môn Độn Giáp: Các cách cục quý hiếm",
                "Ứng dụng Kỳ Môn trong dự đoán vận hạn cao cấp", "Bản dịch Kỳ Môn Độn Giáp chuẩn từ thư khố cổ",
                "Kỳ Môn Độn Giáp: Pháp thuật và tâm linh thực hành", "Trạch Cát Kỳ Môn: Tuyển tập bí yếu",
                "Kỳ Môn và các bản thảo quân sự mưu lược cổ", "Phân tích 1080 cục Kỳ Môn Độn Giáp: Cách luận chuẩn"
            ],
            "Kinh Dịch & Dự Đoán": [
                "Kinh Dịch: 64 Quẻ và lời hào gốc Chu Dịch", "Mai Hoa Dịch Số: Tuyển thảo Thần đoán", 
                "Lục Hào Dự Đoán: Nguyên lý gieo quẻ và ứng dụng chuẩn", "Giải mã 384 hào bản dịch cổ quý hiếm",
                "Dịch Học: Các bí bản về dự toán thiên văn và vận mệnh", "Tượng quẻ thực tế từ các đại sư Kinh Dịch xưa",
                "Huyền Không Đại Quái: Bản thảo gốc và ứng dụng", "Kinh Dịch: Sự biến hóa của âm dương bản văn quý"
            ],
            "Y Học & Dưỡng Sinh": [
                "Âm Dương Ngũ Hành và Y Đạo: Bí yếu trị liệu cổ", "Hoàng Đế Nội Kinh: Bản dịch và chú giải chuyên sâu",
                "Khí Công và Thiền Định: Các bí pháp dưỡng sinh từ cổ tịch", "Dược liệu quý trong y học cổ truyền: Bản thảo hiếm"
            ],
            "Phong Thủy & Địa Lý": [
                "Huyền Không Phi Tinh: Nguyên lý và thực hành chuẩn", "Loan Đầu Hình Thế: Địa lý bí yếu từ cổ tịch",
                "Bát Trạch Minh Cảnh: Bản thảo gốc và phân tích", "Trấn Trạch Hóa Giải: Tuyển tập kỹ thuật bí truyền"
            ]
        }

    def seed_from_user(self, user_question):
        """AI takes a user question and generates 5 high-quality global research branches."""
        return [
            f"{user_question}: Nguyên lý và ứng dụng cổ tịch",
            f"{user_question}: Ví dụ thực tế từ các bậc thầy xưa",
            f"{user_question}: Giải pháp bí truyền từ chuyên gia phương Đông",
            f"{user_question}: Phân tích bối cảnh 2026 dưới góc nhìn Huyền học",
            f"Mở rộng tri thức: {user_question[:20]}... và tầm ảnh hưởng sâu rộng"
        ]

    def generate_research_queue(self, category=None, count=10):
        """Generates a list of clean, professional topics for the 50 agents."""
        if category and category in self.categories:
            base_topics = self.categories[category]
        else:
            cat = random.choice(list(self.categories.keys()))
            base_topics = self.categories[cat]
            
        queue = []
        for _ in range(count):
            topic = random.choice(base_topics)
            # Add deep research markers to the search query if it's a general topic
            search_query = f"{topic} nguyên lý bí truyền giải mã"
            queue.append(search_query)
            
        return list(set(queue))

    def synthesize_mining_prompt(self, target_topic):
        """Mega-Prompt for the 50 Mining Agents - Re-focused on Practical Divination & Reality Checking."""
        category_list = ", ".join(self.categories.keys())
        
        # Pick a random research angle to inject into the logic
        angle = random.choice([
            "Nghiên cứu cổ tịch & Tài liệu hiếm", "Nguyên lý gốc và cách luận chính xác", 
            "Ứng dụng thực tế cao cấp", "Phòng tránh sai lầm và lệch lạc kiến thức", 
            "Bí kíp thực thi từ các bậc tiền bối", "Kết hợp tri thức cổ và logic hiện đại"
        ])

        return f"""
Bạn là 'Đại Pháp Sư Tri Thức' (Expert Diviner & Scholar).
Nhiệm vụ: Khai thác những tài liệu **QUÝ HIẾM**, **CHÍNH XÁC** và **NỘI DUNG GỐC** về chủ đề: **{target_topic}**.
Góc nhìn tập trung vào: **{angle}**.

Mục tiêu: Tạo ra nội dung mang tính **DI SẢN TRÍ TUỆ**, tập trung vào các bản thảo, bí kíp và nguyên lý chuẩn mực. 
TUYỆT ĐỐI không lấy thông tin hời hợt trên mạng. Nếu có dữ liệu từ Google Search, hãy lọc lấy những phần tinh túy nhất.

YÊU CẦU ĐỊNH DẠNG PHẢN HỒI JSON (BẮT BUỘC Ở ĐẦU):
```json
{{
  "clean_title": "Tên chủ đề CHUẨN (Ví dụ: 'Giải Mã Bát Môn Kỳ Môn'). KHÔNG chứa từ rác.",
  "standard_category": "Chọn 1 trong: {category_list}"
}}
```

NỘI DUNG YÊU CẦU:
1. **NGUYÊN LÝ GỐC (ROOT LOGIC)**: Trình bày chính xác cách thức vận hành, không nói chung chung.
2. **CHIẾT TỰ & Ý NGHĨA**: Nếu là thuật ngữ cổ, hãy giải thích sâu.
3. **CÁCH LUẬN ĐOÁN (DIVINATION METHOD)**: Từng bước áp dụng thực tế là gì?
4. **LỜI KHUYÊN BẬC THẦY**: Những lưu ý quan trọng để đạt được sự chính xác.

Giọng văn: Uy nghiêm, sâu sắc, mang tính cổ điển nhưng dễ hiểu.
"""

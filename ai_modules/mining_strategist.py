import json
import random

class MiningStrategist:
    """The Mega-Brain managing 50 specialized AI Mining Agents."""
    
    def __init__(self):
        # EXPANDED TO 100+ SPECIALIZED TOPICS FOR 50 AI AGENTS
        self.categories = {
            "Kỳ Môn Độn Giáp": [
                "Bát Môn Độn Giáp", "Cửu Tinh Phân Tích", "Bát Thần Trợ Lực", 
                "Thần Sát Ẩn Tàng", "Cấu Trúc Phản Phục", "Ứng Dụng Kinh Doanh",
                "Sức Khỏe & Trị Liệu", "Pháp Thuật Kỳ Môn", "Thiên Cáp Thần",
                "Kỳ Môn Tiên Thiên", "Kỳ Môn Hậu Thiên", "Khởi Lệ Bí Truyền",
                "Trạch Cát Thời Gian", "Dự Đoán Thiên Văn", "Quân Sự & Mưu Lược"
            ],
            "Kinh Dịch & Dự Đoán": [
                "64 Quẻ Dịch Học", "Lời Hào & Biến Hóa", "Mai Hoa Dịch Số", 
                "Lục Hào Dự Đoán", "Dịch Học & Thuật Toán", "Tế Lễ Cổ Truyền",
                "Huyền Không Đại Quái", "Trạch Cát Dịch Học", "Tượng Quẻ Thực Tế",
                "Dịch Học & Vật Lý", "Dịch Học & Tài Chính", "Tâm Lý Học Kinh Dịch"
            ],
            "Hệ Thống AI": [
                "Agentic Frameworks", "LLM Fine-tuning", "UI/UX Advanced", 
                "Performance Optimization", "AI Security", "RAG Systems",
                "LangChain & Autogen", "Microservices", "Vector Databases",
                "DevOps AI", "Cloud Solutions", "Kubernetes ML",
                "MLOps Excellence", "Model Compression", "Edge AI",
                "Prompt Mastery", "Multi-Agent Systems", "AI Orchestration"
            ],
            "Y Học & Dưỡng Sinh": [
                "Châm Cứu & Huyệt Đạo", "Dược Liệu Quý Hiếm", "Âm Dương Ngũ Hành",
                "Khí Công Dưỡng Sinh", "Y Đạo Trị Gốc", "Thiền Định & Sóng Não",
                "Dinh Dưỡng Tự Nhiên", "Giải Phẫu Tinh Vi", "Y Học Cổ Truyền",
                "Ayurveda & India", "Dinh Dưỡng Phân Tử", "Liệu Pháp Gen"
            ],
            "Phong Thủy & Địa Lý": [
                "Loan Đầu Hình Thế", "Lý Khí Tuyệt Kỹ", "Huyền Không Phi Tinh",
                "Bát Trạch Minh Cảnh", "Trấn Trạch Hóa Giải", "Long Mạch Toàn Cầu",
                "Phong Thủy Đô Thị", "Âm Trạch Chuyên Biệt", "Phong Thủy Văn Phòng",
                "Phong Thủy Startup", "Địa Lý Thiên Văn", "Kiến Trúc Xanh"
            ],
            "Chiến Lược & Tâm Lý": [
                "Thập Nhị Binh Thư", "Tôn Tử Binh Pháp", "Quỷ Cốc Tử Mưu Lược",
                "Đàm Phán Quốc Tế", "Chiến Tranh Tâm Lý", "Phòng Vệ Tâm Lý",
                "Quản Trị Phương Đông", "Chiến Lược Đại Dương Xanh", "Game Theory",
                "Behavioral Economics", "NLP Thực Chiến", "Strategic Foresight"
            ],
            "Khoa Học Tương Lai": [
                "Gemini AI Evolution", "Multimodal AI", "Robotics & Cybernetics",
                "Edge Computing", "AI Ethics", "Web 4.0 & Blockchain",
                "Quantum Computing", "Space Exploration", "Brain-Computer Interface",
                "Synthetic Biology", "Nanotechnology", "Fusion Energy", "6G Connectivity"
            ],
            "Kinh Tế & Tài Chính": [
                "Crypto Strategies", "DeFi Protocols", "Stock Analysis",
                "Macro Trends 2026", "Real Estate", "Venture Capital",
                "Financial Modeling", "Risk Management", "Algo Trading", "NFT Economy",
                "CBDC Systems", "Global Trade"
            ],
            "Nghiên Cứu Khoa Học": [
                "Climate Solutions", "Renewable Energy", "Materials Science",
                "Astrophysics", "Neuroscience", "Genomics",
                "Ocean Exploration", "Particle Physics", "Dark Matter", "Exoplanets"
            ],
            "Văn Hóa & Xã Hội": [
                "Ancient Civilizations", "Philosophy", "Art History",
                "Music Theory", "Literature", "Sociology",
                "Anthropology", "Religious Studies", "Cultural Psych", "Language Evolution"
            ]
        }

    def seed_from_user(self, user_question):
        """AI takes a user question and generates 5 high-quality global research branches."""
        return [
            f"{user_question}: Phân tích bối cảnh thực tế 2026",
            f"{user_question}: Ví dụ thực tế thành công",
            f"{user_question}: Giải pháp tối ưu từ chuyên gia phương Đông",
            f"{user_question}: Giải pháp từ công nghệ AI hiện đại",
            f"Mở rộng tri thức: {user_question[:20]}... và các hệ quả"
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
            # We no longer add suffixes here to keep the core topic clean
            queue.append(topic)
            
        return list(set(queue))

    def synthesize_mining_prompt(self, target_topic):
        """Mega-Prompt for the 50 Mining Agents - Re-focused on Practical Divination & Reality Checking."""
        category_list = ", ".join(self.categories.keys())
        
        # Pick a random research angle to inject into the logic
        angle = random.choice([
            "Ví dụ thực tế 2026", "Ứng dụng sâu sắc", "Nghiên cứu cổ tịch & Tài liệu hiếm", 
            "Phòng tránh rủi ro & Cạm bẫy", "Giải pháp tối ưu hóa cuộc sống",
            "Bí quyết thực thi thần tốc", "Kết hợp tri thức cổ và công nghệ"
        ])

        return f"""
Bạn là 'Bậc Thầy Tư Vấn Tri Thức' (Expert Strategy Consultant & Diviner).
Nhiệm vụ: Khai thác bí mật và **KIỂM CHỨNG THỰC TẾ** về chủ đề: **{target_topic}**.
Góc nhìn tập trung vào: **{angle}**.

Mục tiêu: Tạo ra nội dung **TRÍ TUỆ THỰC CHIẾN**, không phải lý thuyết suông.

YÊU CẦU ĐỊNH DẠNG PHẢN HỒI JSON (BẮT BUỘC Ở ĐẦU):
```json
{{
  "clean_title": "Tên chủ đề CHUẨN, NGẮN GỌN, CHUYÊN NGHIỆP. TUYỆT ĐỐI KHÔNG chứa các từ rác kỹ thuật như 'Ví dụ:', 'Nghiên cứu:', 'Case study:', 'Phần 1:', 'Sâu:', ... ",
  "standard_category": "Chọn 1 trong: {category_list}"
}}
```

NỘI DUNG YÊU CẦU:
1. **KIỂM CHỨNG THỰC TẾ (REALITY CHECK)**: Có hiệu quả thực sự không? Đừng chỉ tin vào sách, hãy dùng logic và dữ liệu 2026 để phản biện.
2. **ỨNG DỤNG BÁO CÁO**: Nếu một người đang gặp rắc rối liên quan đến việc này, giải pháp 'vàng' cụ thể là gì?
3. **TRÍ TUỆ CHUYÊN SÂU**: Trích xuất tinh hoa.
4. **HÀNH ĐỘNG**: Bước 1, 2, 3 rõ ràng.

Giọng văn: Sắc bén, uy quyền, mang tính chuyên gia.
"""

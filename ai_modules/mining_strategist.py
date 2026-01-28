import json
import random

class MiningStrategist:
    """The Mega-Brain managing 50 specialized AI Mining Agents."""
    
    def __init__(self):
        # EXPANDED TO 100+ SPECIALIZED TOPICS FOR 50 AI AGENTS
        self.categories = {
            "Kỳ Môn Độn Giáp (Sâu)": [
                "Bát Môn chuyên sâu", "Cửu Tinh biến hóa", "Bát Thần trợ lực", 
                "Thần sát ẩn tàng", "Cấu trúc phản phục", "Ứng dụng trong kinh doanh",
                "Kỳ Môn và sức khỏe", "Pháp thuật Kỳ Môn cổ", "Thiên Cáp Thần",
                "Kỳ Môn Tiên Thiên", "Kỳ Môn Hậu Thiên", "Độn Giáp khởi lệ bí truyền",
                "Kỳ Môn chọn ngày giờ", "Kỳ Môn dự đoán thời tiết", "Kỳ Môn quân sự"
            ],
            "Kinh Dịch & Dự Đoán": [
                "64 Quẻ và biến hóa", "Lời hào bí ẩn", "Mai Hoa Dịch Số nâng cao", 
                "Lục Hào chuyên sâu", "Dịch học và thuật toán AI", "Tế lễ và Kinh Dịch",
                "Huyền Không Đại Quái", "Trạch Cát theo Kinh Dịch", "Tượng quẻ thực tế",
                "Kinh Dịch và vật lý lượng tử", "Ứng dụng Kinh Dịch trong tài chính",
                "Kinh Dịch và tâm lý học hiện đại"
            ],
            "Lập Trình & Hệ Thống AI": [
                "Agentic Frameworks", "LLM Fine-tuning", "Streamlit Advanced UI/UX", 
                "Python Performance Optimization", "AI Security & Pentesting", "RAG Systems",
                "LangChain & Autogen", "Microservices Architecture", "Vector Databases",
                "DevOps cho AI", "Cloud Native AI Solutions", "Kubernetes for ML",
                "MLOps Best Practices", "AI Model Compression", "Edge AI Deployment",
                "Prompt Engineering Mastery", "Multi-Agent Systems", "AI Orchestration"
            ],
            "Y Học & Dưỡng Sinh": [
                "Châm cứu và hệ thống huyệt đạo", "Dược liệu quý hiếm toàn cầu", "Âm dương ngũ hành tạng phủ",
                "Khí công dưỡng sinh cổ truyền", "Trị bệnh từ gốc (Y đạo)", "Thiền định và sóng não",
                "Thực phẩm chức năng tự nhiên", "Giải phẫu học tinh vi", "Y học cổ truyền Trung Quốc",
                "Ayurveda và Y học Ấn Độ", "Dinh dưỡng phân tử", "Liệu pháp gen"
            ],
            "Phong Thủy & Địa Lý": [
                "Loan Đầu (Hình thế)", "Lý Khí (Tính toán)", "Huyền Không Phi Tinh",
                "Bát Trạch Minh Cảnh", "Trấn trạch và hóa giải", "Long mạch toàn cầu",
                "Phong thủy đô thị hiện đại", "Âm trạch chuyên sâu", "Phong thủy văn phòng",
                "Phong thủy cho startup", "Địa lý thiên văn", "Phong thủy và kiến trúc xanh"
            ],
            "Chiến Lược & Tâm Lý": [
                "Thập Nhị Binh Thư", "Tôn Tử Binh Pháp", "Quỷ Cốc Tử mưu lược",
                "Chiến lược đàm phán quốc tế", "Tâm lý học chiến tranh", "Thao túng và phòng vệ tâm lý",
                "Quản trị học phương Đông", "Chiến lược Blue Ocean", "Game Theory ứng dụng",
                "Behavioral Economics", "Neuro-Linguistic Programming", "Strategic Foresight"
            ],
            "Công Nghệ Mới & Tương Lai": [
                "Gemini 3.0/4.0 Speculations", "Multimodal AI breakthroughs", "Robotics & Cybernetics",
                "Edge Computing", "AI Ethics & Global Policy", "Web 4.0 & Blockchain",
                "Quantum Computing", "Space Tech & Colonization", "Brain-Computer Interfaces",
                "Synthetic Biology", "Nanotechnology", "Fusion Energy", "6G Networks"
            ],
            "Kinh Tế & Tài Chính": [
                "Cryptocurrency Trading Strategies", "DeFi Protocols", "Stock Market Analysis",
                "Macroeconomics Trends 2026", "Real Estate Investment", "Venture Capital",
                "Financial Modeling", "Risk Management", "Algorithmic Trading", "NFT Economics",
                "Central Bank Digital Currencies", "Global Trade Dynamics"
            ],
            "Khoa Học & Nghiên Cứu": [
                "Climate Change Solutions", "Renewable Energy Tech", "Materials Science",
                "Astrophysics Discoveries", "Neuroscience Breakthroughs", "Genomics Research",
                "Ocean Exploration", "Particle Physics", "Dark Matter Studies", "Exoplanet Research"
            ],
            "Văn Hóa & Xã Hội": [
                "Ancient Civilizations", "Philosophy Eastern vs Western", "Art History",
                "Music Theory Advanced", "Literature Analysis", "Sociology Trends",
                "Anthropology Studies", "Religious Studies", "Cultural Psychology", "Language Evolution"
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
        """Generates a list of deep-dive sub-topics for the 50 agents."""
        if category and category in self.categories:
            base_topics = self.categories[category]
        else:
            cat = random.choice(list(self.categories.keys()))
            base_topics = self.categories[cat]
            
        queue = []
        for _ in range(count):
            topic = random.choice(base_topics)
            angle = random.choice([
                "Ví dụ thực tế 2026", "Ứng dụng sâu", "Case study hiếm", 
                "Hướng dẫn chi thực", "Phân tích rủi ro", "Giải pháp tối ưu",
                "Bí quyết thực thi nhanh", "Dữ liệu gốc từ cổ tịch/papers"
            ])
            queue.append(f"{topic}: {angle}")
            
        return list(set(queue))

    def synthesize_mining_prompt(self, target_topic):
        """Mega-Prompt for the 50 Mining Agents - Now requesting Smart Filtering fields."""
        category_list = ", ".join(self.categories.keys())
        return f"""
Bạn nằm trong 'Quân đoàn 50 Đặc phái viên AI' cấp cao.
Nhiệm vụ: Khai thác tri thức TỐI THƯỢNG về **{target_topic}**.

YÊU CẦU ĐỊNH DẠNG PHẢN HỒI (RẤT QUAN TRỌNG):
Bắt đầu phản hồi bằng một khối JSON như sau (để hệ thống lọc thông minh):
```json
{{
  "clean_title": "Tên chủ đề ngắn gọn, dễ hiểu (ví dụ: 'Bệnh mãn tính' thay vì tên kỹ thuật dài)",
  "standard_category": "Chọn 1 trong danh sách này: {category_list}"
}}
```

SAU ĐÓ LÀ NỘI DUNG CHI TIẾT:
1. **TRANG BỊ 3 VÍ DỤ THỰC TẾ**: Cung cấp tình huống thực tế minh họa cực kỳ chi tiết.
2. **CHIẾN LƯỢC HÀNH ĐỘNG**: Đề xuất cụ thể bước 1, 2, 3 để ứng dụng kiến thức này ngay.
3. **DỮ LIỆU CHUYÊN SÂU**: Trích xuất thông số, mã nguồn hoặc cổ văn liên quan.
4. **LIÊN KẾT ĐA TẦNG**: Đề xuất 2 chủ đề ngách khác liên quan đến phát hiện này.

Hãy viết như một chuyên gia tư vấn chiến lược hàng đầu, bám sát thực tế và giàu tính thực thi.
"""

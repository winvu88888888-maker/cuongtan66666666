import json
import random

class MiningStrategist:
    """The brain that decides what the 10 AI Miners should search for next."""
    
    def __init__(self):
        self.categories = {
            "Kỳ Môn Độn Giáp": [
                "Bát Môn chuyên sâu", "Cửu Tinh biến hóa", "Bát Thần trợ lực", 
                "Thần sát ẩn tàng", "Cấu trúc phản phục", "Ứng dụng trong kinh doanh",
                "Kỳ Môn và sức khỏe", "Pháp thuật Kỳ Môn cổ", "Thiên Cáp Thần"
            ],
            "Kinh Dịch Chuyên Sâu": [
                "64 Quẻ và biến hóa", "Lời hào bí ẩn", "Mai Hoa Dịch Số nâng cao", 
                "Lục Hào tiên đoán", "Dịch học và thuật toán AI", "Tế lễ và Kinh Dịch"
            ],
            "Lập Trình Python/AI": [
                "Agentic Frameworks", "LLM Fine-tuning", "Streamlit UI/UX", 
                "Python Performance", "AI Security", "RAG Systems"
            ],
            "Y Học Cổ Truyền": [
                "Châm cứu và huyệt đạo", "Dược liệu quý hiếm", "Âm dương ngũ hành trong tạng phủ",
                "Khí công dưỡng sinh", "Trị bệnh từ gốc"
            ],
            "Phong Thủy Địa Lý": [
                "Loan Đầu và Lý Khí", "Huyền Không Phi Tinh", "Bát Trạch Minh Cảnh",
                "Trấn trạch và hóa giải", "Long mạch toàn cầu"
            ],
            "Chiến Lược": [
                "Thập Nhị Binh Thư", "Tôn Tử Binh Pháp", "Quỷ Cốc Tử",
                "Chiến lược đàm phán", "Tâm lý học chiến tranh"
            ],
            "Công Nghệ AI Mới": [
                "Gemini 1.5/2.0 updates", "Multimodal AI", "Robotics AI",
                "Edge Computing", "AI Ethics"
            ]
        }

    def seed_from_user(self, user_question):
        """AI takes a user question and generates 3-5 high-quality global research branches."""
        # This will be used in Phase 21 to expand topics based on user's personal interests
        return [
            f"{user_question}: Phân tích bối cảnh toàn cầu 2026",
            f"{user_question}: Ví dụ thực tế thành công",
            f"{user_question}: Giải pháp tối ưu từ chuyên gia",
            f"Chủ đề liên quan đến: {user_question[:30]}..."
        ]

    def evolve_categories(self, new_findings):
        """Allows the AI to add new categories based on what it discovers on the internet."""
        # Logic to be called by the miner when it finds something outside current scope
        for cat, topics in new_findings.items():
            if cat not in self.categories:
                self.categories[cat] = topics
            else:
                self.categories[cat] = list(set(self.categories[cat] + topics))

    def generate_research_queue(self, category=None, count=5):
        """Generates a list of deep-dive sub-topics with emphasis on NEW fields."""
        if category and category in self.categories:
            base_topics = self.categories[category]
        else:
            # Shift categories over time to explore new areas
            cat = random.choice(list(self.categories.keys()))
            base_topics = self.categories[cat]
            
        queue = []
        for _ in range(count):
            topic = random.choice(base_topics)
            # Add a recursive depth factor focused on PRACTICALITY
            angle = random.choice([
                "Ví dụ thực tế 2026", "Ứng dụng đời đời", "Case study thành công", 
                "Hướng dẫn chi tiết từng bước", "Phân tích sai lầm thực tế", "Giải pháp tối ưu"
            ])
            queue.append(f"{topic}: {angle}")
            
        return list(set(queue))

    def synthesize_mining_prompt(self, target_topic):
        """Creates a specialized system prompt for an AI agent to 'mine' this topic with EXAMPLE focus."""
        return f"""
Bạn là một Đặc phái viên AI 'Khai thác Đa tầng'. 
Nhiệm vụ: Khai thác tri thức về **{target_topic}**.

YÊU CẦU BẮT BUỘC:
1. **TRANG BỊ VÍ DỤ THỰC TẾ**: Cung cấp ít nhất 3 ví dụ hoặc tình huống thực tế minh họa cho kiến thức này.
2. **DỮ LIỆU GỐC**: Trích xuất các thông số, thuật toán hoặc văn bản gốc (cổ văn/mã nguồn).
3. **LIÊN KẾT CHỦ ĐỀ MỚI**: Đề xuất 2-3 chủ đề liên quan tiềm năng chưa có trong danh sách hiện tại.

Hãy trả về nội dung cực kỳ chi tiết, bám sát thực tế và sẵn sàng để 'nạp' vào hệ thống tri thức.
"""

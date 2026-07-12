import json
import random

class MiningStrategist:
    """The Mega-Brain managing 50 specialized AI Mining Agents.
    V2.0 - EXPANDED to 200+ seed topics across 10+ categories."""
    
    def __init__(self):
        # EXPANDED TO 200+ SPECIALIZED TOPICS FOR 50 AI AGENTS
        self.categories = {
            "Kỳ Môn Độn Giáp": [
                "Bản văn cổ Kỳ Môn Độn Giáp bí truyền", "Kỳ Môn Độn Giáp: Giải mã Bát Môn thần đoán", 
                "Cửu Tinh và Thần Sát trong Kỳ Môn: Nguyên lý gốc", "Kỳ Môn Độn Giáp: Các cách cục quý hiếm",
                "Ứng dụng Kỳ Môn trong dự đoán vận hạn cao cấp", "Bản dịch Kỳ Môn Độn Giáp chuẩn từ thư khố cổ",
                "Kỳ Môn Độn Giáp: Pháp thuật và tâm linh thực hành", "Trạch Cát Kỳ Môn: Tuyển tập bí yếu",
                "Phân tích 1080 cục Kỳ Môn Độn Giáp: Cách luận chuẩn", "Kỳ Môn Độn Giáp: Khói mây biến hóa Cửu Cung",
                "Thần sát Thiên Mã, Thiên Võng trong Kỳ Môn", "Kỳ Môn Độn Giáp: Lộc Mã Quý Nhân bí pháp",
                "Dụng Thần Kỳ Môn Độn Giáp: Ứng dụng bách biến", "Kỳ Môn Độn Giáp: Chế sát và Hóa giải bí truyền",
                # --- NEW V2.0 topics ---
                "Kỳ Môn Độn Giáp: Tam Kỳ Lục Nghi chuyên sâu", "Kỳ Môn: Phép đoán thất vật tìm đồ",
                "Kỳ Môn Độn Giáp: Luận đoán bệnh tật theo cung vị", "Kỳ Môn: Thuật dùng binh và mưu lược cổ đại",
                "Kỳ Môn Độn Giáp: Luận giải hôn nhân duyên phận", "Kỳ Môn: Kiện tụng tranh chấp cách luận",
                "Kỳ Môn Độn Giáp: Luận tài vận kinh doanh buôn bán", "Kỳ Môn: Đầu tư chứng khoán bất động sản",
                "Kỳ Môn Độn Giáp: Xuất hành di chuyển cát hung", "Kỳ Môn: Phép xem thời tiết thiên văn",
                "Kỳ Môn Độn Giáp: Thi cử học hành công danh", "Kỳ Môn: Bí pháp Kỳ Môn Phi Bàn",
                "Kỳ Môn Độn Giáp: Chuyển Bàn và Phi Cung bí yếu", "Kỳ Môn: Tam Giáp ẩn độn trong Cửu Cung",
                "Kỳ Môn Độn Giáp: Các sách cổ kinh điển giải nghĩa", "Kỳ Môn: Cách cục Phục Ngâm Phản Ngâm",
                "Kỳ Môn Độn Giáp: Long Độn Hổ Độn Phong Độn Vân Độn", "Kỳ Môn: Luận đoán thai sản sinh con",
                "Kỳ Môn Độn Giáp: Trạch Nhật chọn ngày tốt", "Kỳ Môn: Xem tướng mạo qua cung Kỳ Môn",
                "Kỳ Môn Độn Giáp: Bát Thần chi phối vận mệnh", "Kỳ Môn: Cửu Tinh sáng tối luận cát hung",
                "Kỳ Môn Độn Giáp: Năm trụ Kỳ Môn lập mệnh", "Kỳ Môn: Hợp tác làm ăn xem đối tác",
            ],
            "Kinh Dịch & Dự Đoán": [
                "Kinh Dịch: 64 Quẻ và lời hào gốc Chu Dịch", "Mai Hoa Dịch Số: Tuyển thảo Thần đoán", 
                "Lục Hào Dự Đoán: Nguyên lý gieo quẻ và ứng dụng chuẩn", "Giải mã 384 hào bản dịch cổ quý hiếm",
                "Dịch Học: Các bí bản về dự toán thiên văn và vận mệnh", "Tượng quẻ thực tế từ các đại sư Kinh Dịch xưa",
                "Huyền Không Đại Quái: Bản thảo gốc và ứng dụng", "Kinh Dịch: Sự biến hóa của âm dương bản văn quý",
                "Quẻ Dịch và Phong Thủy: Mối liên hệ mật thiết", "Dự đoán Lục Hào: Nạp Giáp và Phi Thần bí yếu",
                "Dịch Kinh: Đạo trị quốc và mưu lược quân sự", "Mai Hoa Dịch Số: Đoán sự qua âm thanh và hình ảnh",
                # --- NEW V2.0 topics ---
                "Kinh Dịch: Quẻ Càn giải nghĩa sâu từ nguyên bản", "Kinh Dịch: Quẻ Khôn và đức tính Đất Mẹ",
                "Kinh Dịch: Hào Biến và Hỗ Quái cách đoán", "Mai Hoa: Ngoại Ứng phương pháp lấy quẻ",
                "Lục Hào: Lục Thân sinh khắc luận giải", "Lục Hào: Nguyệt Phá Nhật Phá tác dụng",
                "Kinh Dịch: Thuyết Thái Cực và Lưỡng Nghi", "Dịch Học: Hà Đồ Lạc Thư nguồn gốc và ứng dụng",
                "Mai Hoa: Thể Dụng sinh khắc đoán sự việc", "Lục Hào: Dụng Thần và Nguyên Thần cách chọn",
                "Kinh Dịch: Hệ Từ Truyện giải nghĩa chuyên sâu", "Dịch Học: Tiên Thiên Bát Quái và Hậu Thiên Bát Quái",
                "Mai Hoa: Đoán bệnh tật sức khỏe theo quẻ", "Lục Hào: Đoán tài vận buôn bán kinh doanh",
                "Kinh Dịch: Ứng dụng trong quản trị doanh nghiệp", "Dịch Học: Nghiên cứu của Thiệu Ung về Mai Hoa",
                "Mai Hoa: Số đo chữ viết khởi quẻ", "Lục Hào: Tìm người mất tích theo quẻ",
                "Kinh Dịch: Quẻ Ký Tế và Vị Tế ý nghĩa kết thúc", "Dịch Học: Tam Tài Thiên Địa Nhân trong Dịch",
            ],
            "Tài Liệu Cổ Tịch (Tri Thức Vô Tận)": [
                "Bản thảo hiếm về Thuật Số phương Đông", "Tàng thư bí truyền của các danh gia Huyền học",
                "Phân tích các bản khắc gỗ Cổ Tịch quý hiếm", "Tri thức từ các thư viện cổ quốc tế về Dịch Lý",
                # --- NEW V2.0 topics ---
                "Hoàng Cực Kinh Thế: Tác phẩm kinh điển của Thiệu Ung", "Trạch Cát Thông Thư: Sách chọn ngày giờ cổ đại",
                "Thái Ất Thần Kinh: Bí thư dự đoán quốc vận", "Lục Nhâm Đại Toàn: Phương pháp dự đoán cổ xưa nhất",
                "Tăng San Bốc Dịch: Sách kinh điển về Lục Hào", "Thiên Cơ Tia Tỉnh: Bí kíp dự đoán thiên cơ",
                "Uyên Hải Tử Bình: Sách gốc về Tứ Trụ mệnh học", "Trích Thiên Tùy: Luận giải mệnh lý Tứ Trụ",
                "Tam Mệnh Thông Hội: Bách khoa toàn thư mệnh lý", "Tử Bình Chân Thuyên: Tinh hoa Tứ Trụ",
                "Đạo Đức Kinh: Triết lý Lão Tử và Huyền học", "Chu Dịch Tham Đồng Khế: Luyện đan và Dịch Lý",
                "Hoàng Đế Trạch Kinh: Phong thủy nhà ở cổ đại", "Thanh Nang Kinh: Bí thư phong thủy hàng đầu",
                "Cửu Thiên Huyền Nữ phương pháp xem hướng", "Kỳ Môn Độn Giáp Đại Toàn: Sách tổng hợp Kỳ Môn",
                "Mai Hoa Dịch Số toàn bản gốc Thiệu Khang Tiết", "Mã Y Tướng Pháp: Sách xem tướng kinh điển",
                "Liễu Phàm Tứ Huấn: Phương pháp thay đổi vận mệnh", "Tuyết Tâm Phú: Luận giải mệnh lý kinh điển",
            ],
            "Y Học & Dưỡng Sinh": [
                "Âm Dương Ngũ Hành và Y Đạo: Bí yếu trị liệu cổ", "Hoàng Đế Nội Kinh: Bản dịch và chú giải chuyên sâu",
                "Khí Công và Thiền Định: Các bí pháp dưỡng sinh từ cổ tịch", "Dược liệu quý trong y học cổ truyền: Bản thảo hiếm",
                # --- NEW V2.0 topics ---
                "Thần Nông Bản Thảo Kinh: Sách dược liệu đầu tiên", "Thương Hàn Luận: Y thuật Trương Trọng Cảnh",
                "Kim Quỹ Yếu Lược: Điều trị nội khoa cổ đại", "Châm Cứu Đại Thành: Bí pháp châm cứu toàn diện",
                "Tứ Chẩn: Vọng Văn Vấn Thiết phương pháp khám bệnh", "Bát Cương: Biện chứng luận trị Y học cổ truyền",
                "Ngũ Hành sinh khắc trong chẩn đoán bệnh tật", "Dưỡng sinh theo mùa: Xuân Hạ Thu Đông bí quyết",
                "Bát Đoạn Cẩm: Phương pháp khí công cổ xưa", "Thái Cực Quyền: Nội công dưỡng sinh hàng ngày",
                "Thực dưỡng Ngũ Hành: Ăn uống theo mệnh", "Tý Ngọ Lưu Chú: Châm cứu theo giờ sinh học",
                "Kinh Lạc học: Hệ thống đường kinh trong cơ thể", "Đông Y trị liệu ung thư: Nghiên cứu hiện đại",
                "Ngũ Cầm Hí: Bài tập dưỡng sinh của Hoa Đà", "Thiền định và não bộ: Khoa học hiện đại chứng minh",
            ],
            "Phong Thủy & Địa Lý": [
                "Huyền Không Phi Tinh: Nguyên lý và thực hành chuẩn", "Loan Đầu Hình Thế: Địa lý bí yếu từ cổ tịch",
                "Bát Trạch Minh Cảnh: Bản thảo gốc và phân tích", "Trấn Trạch Hóa Giải: Tuyển tập kỹ thuật bí truyền",
                # --- NEW V2.0 topics ---
                "Phong Thủy văn phòng: Bố trí bàn làm việc theo cung mệnh", "Long Mạch: Tìm hiểu huyệt đất và khí mạch",
                "Phong Thủy nhà ở: Cách cục cát hung từng phòng", "Thủy Pháp: Luận đoán nước đến nước đi",
                "Phong Thủy phòng ngủ: Hướng giường và sức khỏe", "Sa Pháp: Xem núi đồi hình thế xung quanh",
                "Phong Thủy nhà bếp: Vị trí bếp và tài vận", "Hướng nhà theo tuổi: Bát Trạch phối mệnh",
                "Phong Thủy cửa hàng kinh doanh buôn bán", "Trạch nhật động thổ xây dựng nhà cửa",
                "Phong Thủy mộ phần: Âm Trạch và phúc đức hậu thế", "Phong Thủy sân vườn cây cảnh hòn non bộ",
                "Phong Thủy xe hơi: Chọn xe theo mệnh tuổi", "Huyền Không Đại Quái phương pháp lập cục",
                "Phong Thủy nội thất: Màu sắc vật liệu theo Ngũ Hành", "Tam Nguyên Cửu Vận: Chu kỳ vận khí đất trời",
                "Phong Thủy cho người mệnh Kim Mộc Thủy Hỏa Thổ", "Long Hổ Sa Thủy trong địa lý phong thủy",
                "Phong Thủy chung cư căn hộ cao tầng", "Hình Sát trong phong thủy: Nhận diện và hóa giải",
            ],
            # ===================== NEW CATEGORIES V2.0 =====================
            "Tử Vi Đẩu Số": [
                "Tử Vi Đẩu Số: Nguyên lý lập lá số và an sao", "Tử Vi: 14 Chính Tinh và ý nghĩa từng sao",
                "Tử Vi: Cung Mệnh và Cung Thân phân tích sâu", "Tử Vi: Tam Hợp Tứ Hóa luận đoán vận mệnh",
                "Tử Vi: Luận đoán sự nghiệp công danh", "Tử Vi: Xem tài vận và cách cục giàu nghèo",
                "Tử Vi: Luận đoán hôn nhân tình duyên", "Tử Vi: Xem sức khỏe bệnh tật theo cung",
                "Tử Vi: Đại Hạn Tiểu Hạn Lưu Niên", "Tử Vi: Sao Tử Vi Thiên Cơ Thái Dương Vũ Khúc",
                "Tử Vi: Sao Tham Lang Cự Môn Liêm Trinh", "Tử Vi: Sao Thiên Đồng Thiên Lương Thiên Tướng",
                "Tử Vi: Phá Quân Thất Sát Tham Lang tam cách", "Tử Vi: Tả Phụ Hữu Bật Văn Xương Văn Khúc",
                "Tử Vi: Lộc Tồn Hóa Lộc Thiên Mã luận tài", "Tử Vi: Kình Dương Đà La Hỏa Tinh Linh Tinh",
                "Tử Vi: 12 Cung vị chi tiết luận giải", "Tử Vi: Tứ Hóa Phi Tinh phương pháp cao cấp",
                "Tử Vi: So sánh lá số nam nữ hợp hôn", "Tử Vi: Luận đoán con cái và Cung Tử Tức",
                "Tử Vi: Cung Điền Trạch nhà cửa bất động sản", "Tử Vi: Cung Nô Bộc xem bạn bè đồng nghiệp",
                "Tử Vi: Xem năm tháng ngày giờ vận hạn chi tiết", "Tử Vi: Các cách cục đặc biệt quý hiếm",
            ],
            "Tứ Trụ & Bát Tự": [
                "Tứ Trụ Bát Tự: Nguyên lý Can Chi và Ngũ Hành", "Bát Tự: Cách xác định Dụng Thần chính xác",
                "Tứ Trụ: Thập Thần luận giải tính cách và vận mệnh", "Bát Tự: Hợp Hình Xung Phá Hại Can Chi",
                "Tứ Trụ: Cách cục Chính Quan Thiên Quan luận sự nghiệp", "Bát Tự: Tài Tinh Chính Tài Thiên Tài luận tài vận",
                "Tứ Trụ: Ấn Tinh và Kiêu Ấn luận học vấn", "Bát Tự: Thực Thần Thương Quan luận tài năng",
                "Tứ Trụ: Tỷ Kiên Kiếp Tài luận bạn bè xã hội", "Bát Tự: Đại Vận Tiểu Vận Lưu Niên phân tích",
                "Tứ Trụ: Không Vong Đào Hoa Quý Nhân các thần sát", "Bát Tự: Luận đoán hôn nhân nam nữ hợp mệnh",
                "Tứ Trụ: 12 Trường Sinh và vòng đời Ngũ Hành", "Bát Tự: Ngũ Hành thiếu thừa cách bổ sung",
                "Tứ Trụ: Thiên Can Thấu Xuất và Địa Chi Tàng Can", "Bát Tự: Phương pháp Manh Phái hiện đại",
                "Tứ Trụ: Đặt tên theo mệnh Ngũ Hành", "Bát Tự: Chọn nghề nghiệp theo Dụng Thần",
                "Tứ Trụ: Kiện tụng pháp lý xem theo mệnh", "Bát Tự: Xem sức khỏe bệnh tật qua Tứ Trụ",
            ],
            "Nhân Tướng Học": [
                "Nhân Tướng: Ngũ Quan và cách xem tướng mặt", "Nhân Tướng: Tướng trán và vận mệnh sớm muộn",
                "Nhân Tướng: Tướng mắt và trí tuệ tình cảm", "Nhân Tướng: Tướng mũi và tài vận sự nghiệp",
                "Nhân Tướng: Tướng miệng và phúc đức ẩm thực", "Nhân Tướng: Tướng tai và thọ mệnh phú quý",
                "Nhân Tướng: Tướng tay và vận mệnh đường đời", "Nhân Tướng: Đường chỉ tay Sinh Mệnh Trí Tuệ Tình Cảm",
                "Nhân Tướng: Nốt ruồi trên cơ thể và ý nghĩa", "Nhân Tướng: Tướng đi tướng đứng luận tính cách",
                "Nhân Tướng: Tam Đình ngũ nhạc xem toàn diện", "Nhân Tướng: Tướng lông mày và vận hạn trung niên",
                "Nhân Tướng: Xem tướng người qua giọng nói", "Nhân Tướng: Mã Y Tướng Pháp ứng dụng thực tế",
                "Nhân Tướng: Tướng xương luận đoán quý tiện", "Nhân Tướng: Tướng học trong tuyển dụng nhân sự",
            ],
            "Số Học & Danh Số": [
                "Thần Số Học: Chỉ số Đường Đời và ý nghĩa", "Thần Số Học: Ma trận ngày sinh và tiềm năng",
                "Danh Số Học: Đặt tên theo Ngũ Hành bổ mệnh", "Số Học: Chọn số điện thoại may mắn theo mệnh",
                "Thần Số Học: Năm cá nhân và chu kỳ 9 năm", "Danh Số Học: Tên công ty doanh nghiệp hợp phong thủy",
                "Số Học: Biển số xe may mắn theo tuổi mệnh", "Thần Số Học: Chỉ số Linh Hồn và Nhân Cách",
                "Danh Số Học: Phương pháp Ngũ Cách của Nhật Bản", "Số Học: Ý nghĩa các con số trong đời sống",
                "Thần Số Học: Tương hợp bạn đời theo chỉ số", "Danh Số Học: Đổi tên để thay đổi vận mệnh",
                "Số Học: Ngày giờ sinh và mật mã vũ trụ", "Thần Số Học: Sứ mệnh cuộc đời và con số chủ đạo",
            ],
            "Thiên Văn & Lịch Pháp": [
                "Lịch Can Chi: Cách tính ngày giờ theo âm lịch", "Thiên Văn: 28 Tú và ảnh hưởng đến vận mệnh",
                "Lịch Vạn Niên: Phương pháp tra cứu chính xác", "Thiên Văn: Nhật thực Nguyệt thực và dự đoán",
                "Lịch Pháp: Tiết Khí 24 và ứng dụng trong dự đoán", "Thiên Văn: Cửu Tinh hành đạo và vận mệnh quốc gia",
                "Lịch Can Chi: Nạp Âm Ngũ Hành 60 Hoa Giáp", "Thiên Văn: Sao Bắc Đẩu và phương pháp tu luyện",
                "Lịch Pháp: Ngày Hoàng Đạo Hắc Đạo cách tính", "Thiên Văn: Hành tinh và ảnh hưởng chiêm tinh phương Đông",
                "Lịch Can Chi: Tam Hợp Lục Hợp Tứ Hành Xung", "Thiên Văn: Tử Vi viên chiếu và bầu trời cổ đại",
            ],
            "Tâm Linh & Tu Luyện": [
                "Đạo Giáo: Phù chú và bùa hộ mệnh cổ đại", "Phật Giáo: Kinh Phật và phương pháp tu tập",
                "Thiền Định: Các trường phái thiền trong lịch sử", "Mật Tông: Chân ngôn và Dharani bí mật",
                "Yoga: Nguồn gốc và mối liên hệ với khí công Đông phương", "Luân Hồi: Nghiên cứu khoa học về tiền kiếp",
                "Phong Thủy Tâm Linh: Cúng bái và lễ nghi cổ truyền", "Đạo Giáo: Thái Thượng Cảm Ứng Thiên chiêm nghiệm",
                "Thiền Định: Kỹ thuật quán tưởng và trực giác", "Tâm Linh: Giấc mơ và phương pháp giải mộng cổ đại",
                "Phật Giáo: Bát Nhã Tâm Kinh giải nghĩa chuyên sâu", "Đạo Giáo: Nội Đan và ngoại Đan thuật",
            ],
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
        """Generates a list of clean, professional topics for the 50 agents.
        V2.0: Selects from ALL categories for maximum diversity."""
        if category and category in self.categories:
            base_topics = self.categories[category]
        else:
            # V2.0: Pick from ALL categories for diversity
            base_topics = []
            for cat_topics in self.categories.values():
                base_topics.extend(cat_topics)
            
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
            "Bí kíp thực thi từ các bậc tiền bối", "Kết hợp tri thức cổ và logic hiện đại",
            "So sánh các trường phái và phương pháp", "Phân tích trường hợp thực tế và kinh nghiệm",
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

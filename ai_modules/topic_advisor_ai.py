"""
TOPIC ADVISOR AI - Gợi Ý Chủ Đề Thông Minh
Phân tích và gợi ý chủ đề phù hợp theo giờ, ngày, hoàn cảnh
"""

from datetime import datetime
from zoneinfo import ZoneInfo

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

# Chủ đề theo giờ
TOPICS_BY_HOUR = {
    # Giờ Tý (23-01): Thủy - Bí mật, suy nghĩ, tĩnh lặng
    (23, 1): ["Sức khỏe", "Giấc ngủ", "Suy nghĩ nội tâm", "Bí mật"],
    # Giờ Sửu (01-03): Thổ - Tích lũy, chuẩn bị
    (1, 3): ["Lập kế hoạch", "Chuẩn bị", "Tích lũy", "Học tập"],
    # Giờ Dần (03-05): Mộc - Khởi đầu mới
    (3, 5): ["Khởi nghiệp", "Bắt đầu mới", "Xuất hành", "Tập thể dục"],
    # Giờ Mão (05-07): Mộc - Giao tiếp, văn thư
    (5, 7): ["Giao tiếp", "Họp hành", "Ký hợp đồng", "Xin việc"],
    # Giờ Thìn (07-09): Thổ - Kinh doanh, đối ngoại
    (7, 9): ["Kinh doanh", "Giao dịch", "Gặp đối tác", "Thương lượng"],
    # Giờ Tỵ (09-11): Hỏa - Văn hóa, học thuật
    (9, 11): ["Học tập", "Thi cử", "Nghiên cứu", "Sáng tạo"],
    # Giờ Ngọ (11-13): Hỏa - Kết nối, liên kết
    (11, 13): ["Hợp tác", "Ký kết", "Tình cảm", "Kết hôn"],
    # Giờ Mùi (13-15): Thổ - Ăn uống, giao lưu
    (13, 15): ["Đầu tư", "Mua bán", "Bất động sản", "Ẩm thực"],
    # Giờ Thân (15-17): Kim - Quyền lực, quyết định
    (15, 17): ["Quyết định lớn", "Đàm phán", "Kiện tụng", "Thử thách"],
    # Giờ Dậu (17-19): Kim - Thu hoạch, hoàn tất
    (17, 19): ["Thu hoạch", "Hoàn tất", "Nhận lương", "Kết thúc"],
    # Giờ Tuất (19-21): Thổ - Gia đình, nghỉ ngơi
    (19, 21): ["Gia đình", "Con cái", "Nhà cửa", "Thư giãn"],
    # Giờ Hợi (21-23): Thủy - Tĩnh lặng, kết thúc
    (21, 23): ["Tổng kết", "Lập kế hoạch ngày mai", "Tình cảm", "Nghỉ ngơi"]
}

# Chủ đề theo ngày trong tuần
TOPICS_BY_WEEKDAY = {
    0: ["Khởi đầu tuần mới", "Lập kế hoạch", "Công việc quan trọng"],  # Thứ 2
    1: ["Giao tiếp", "Họp hành", "Thương lượng"],  # Thứ 3
    2: ["Học tập", "Nghiên cứu", "Sáng tạo", "Phát triển"],  # Thứ 4
    3: ["Mở rộng", "Đầu tư", "Gặp gỡ", "Hợp tác"],  # Thứ 5
    4: ["Hoàn tất", "Thu tiền", "Ký kết", "Quyết định"],  # Thứ 6
    5: ["Gia đình", "Mua sắm", "Giải trí", "Tình cảm"],  # Thứ 7
    6: ["Nghỉ ngơi", "Tâm linh", "Sức khỏe", "Dọn dẹp"]  # Chủ nhật
}

# 200 chủ đề phổ biến
CHU_DE_PHO_BIEN = [
    # Tài chính
    "Xin tăng lương", "Đầu tư chứng khoán", "Vay tiền", "Mua nhà", "Mua xe",
    "Kinh doanh online", "Mở cửa hàng", "Xổ số", "Cá cược", "Trả nợ",
    
    # Công việc
    "Xin việc", "Đổi việc", "Thăng tiến", "Khởi nghiệp", "Ký hợp đồng",
    "Nhảy việc", "Nghỉ việc", "Phỏng vấn", "Thi tuyển", "Đàm phán lương",
    
    # Tình cảm
    "Tỏ tình", "Hẹn hò", "Kết hôn", "Ly hôn", "Hòa giải",
    "Tìm người yêu", "Quay lại với người cũ", "Ngoại tình", "Chia tay",
    
    # Gia đình
    "Sinh con", "Đám cưới", "Xây nhà", "Chuyển nhà", "Cải tạo nhà",
    "Mua đất", "Thờ cúng", "Động thổ", "Nhập trạch", "An táng",
    
    # Sức khỏe
    "Khám bệnh", "Phẫu thuật", "Chữa bệnh", "Thọ mệnh", "Tai nạn",
    "Sinh nở", "Tuổi thọ", "Bệnh tật", "Hồi phục",
    
    # Di chuyển
    "Xuất hành", "Du lịch", "Đi xa", "Di dân", "Về quê",
    
    # Pháp lý
    "Kiện tụng", "Tranh chấp", "Thắng kiện", "Thua kiện", "Hòa giải",
    
    # Học tập
    "Thi đại học", "Du học", "Học nghề", "Bảo vệ luận văn", "Thi bằng lái"
]


class TopicAdvisorAI:
    """
    AI Gợi Ý Chủ Đề Thông Minh
    Đề xuất chủ đề phù hợp với thời gian và hoàn cảnh
    """
    
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper
    
    def get_current_chi(self):
        """Lấy Chi của giờ hiện tại"""
        now = datetime.now(VN_TZ)
        hour = now.hour
        
        chi_map = {
            (23, 1): "Tý", (1, 3): "Sửu", (3, 5): "Dần", (5, 7): "Mão",
            (7, 9): "Thìn", (9, 11): "Tỵ", (11, 13): "Ngọ", (13, 15): "Mùi",
            (15, 17): "Thân", (17, 19): "Dậu", (19, 21): "Tuất", (21, 23): "Hợi"
        }
        
        for (start, end), chi in chi_map.items():
            if start <= hour < end or (chi == "Tý" and (hour >= 23 or hour < 1)):
                return chi, (start, end)
        
        return "Tý", (23, 1)
    
    def get_recommended_topics(self):
        """Lấy chủ đề được khuyên dùng theo giờ và ngày"""
        now = datetime.now(VN_TZ)
        hour = now.hour
        weekday = now.weekday()
        
        chi, hour_range = self.get_current_chi()
        
        # Chủ đề theo giờ
        topics_hour = TOPICS_BY_HOUR.get(hour_range, [])
        
        # Chủ đề theo ngày
        topics_day = TOPICS_BY_WEEKDAY.get(weekday, [])
        
        return {
            "gio_hien_tai": f"{hour:02d}:00",
            "chi": chi,
            "thu": weekday + 2 if weekday < 6 else "Chủ nhật",
            "chu_de_theo_gio": topics_hour,
            "chu_de_theo_ngay": topics_day,
            "tong_hop": list(set(topics_hour + topics_day))
        }
    
    def analyze_topic_match(self, topic):
        """Phân tích mức độ phù hợp của chủ đề với thời điểm hiện tại"""
        now = datetime.now(VN_TZ)
        recommendations = self.get_recommended_topics()
        
        topic_lower = topic.lower()
        
        # Kiểm tra xem chủ đề có trong danh sách khuyên dùng không
        match_score = 0
        match_reasons = []
        
        for rec_topic in recommendations["tong_hop"]:
            if rec_topic.lower() in topic_lower or topic_lower in rec_topic.lower():
                match_score += 30
                match_reasons.append(f"✅ Phù hợp với khuyến nghị thời điểm: {rec_topic}")
        
        if match_score == 0:
            match_reasons.append("⚠️ Chủ đề không nằm trong khuyến nghị của thời điểm này")
        
        # Điểm cơ bản theo giờ
        hour = now.hour
        if 7 <= hour <= 17:  # Giờ làm việc
            if any(kw in topic_lower for kw in ["việc", "kinh doanh", "họp", "ký"]):
                match_score += 20
                match_reasons.append("✅ Giờ làm việc phù hợp cho công việc")
        elif 18 <= hour <= 22:  # Giờ tối
            if any(kw in topic_lower for kw in ["tình", "gia đình", "nghỉ"]):
                match_score += 20
                match_reasons.append("✅ Giờ tối phù hợp cho gia đình, tình cảm")
        
        # Đảm bảo tối thiểu 40 nếu không vi phạm gì
        if match_score < 40:
            match_score = 40
        
        match_score = min(100, match_score)
        
        if match_score >= 70:
            verdict = "RẤT PHÙ HỢP"
        elif match_score >= 50:
            verdict = "PHÙ HỢP"
        else:
            verdict = "KHÔNG LÝ TƯỞNG"
        
        return {
            "topic": topic,
            "score": match_score,
            "verdict": verdict,
            "reasons": match_reasons,
            "gio_tot_hon": self._suggest_better_time(topic)
        }
    
    def _suggest_better_time(self, topic):
        """Gợi ý thời gian tốt hơn cho chủ đề"""
        topic_lower = topic.lower()
        
        suggestions = []
        
        if any(kw in topic_lower for kw in ["việc", "phỏng vấn", "ký"]):
            suggestions.append("Giờ Mão (05-07), Thìn (07-09): Tốt cho việc giao tiếp, ký kết")
        
        if any(kw in topic_lower for kw in ["tiền", "tài", "đầu tư"]):
            suggestions.append("Giờ Thìn (07-09), Mùi (13-15): Tốt cho tài chính")
        
        if any(kw in topic_lower for kw in ["tình", "yêu", "hôn"]):
            suggestions.append("Giờ Ngọ (11-13), Hợi (21-23): Tốt cho tình cảm")
        
        if any(kw in topic_lower for kw in ["học", "thi"]):
            suggestions.append("Giờ Tỵ (09-11): Tốt cho học tập, thi cử")
        
        if any(kw in topic_lower for kw in ["xuất hành", "đi"]):
            suggestions.append("Giờ Dần (03-05), Mão (05-07): Tốt cho xuất hành")
        
        if not suggestions:
            suggestions.append("Xem giờ Hoàng Đạo trong ngày để chọn thời điểm tốt nhất")
        
        return suggestions
    
    def get_all_topics(self, category=None):
        """Lấy danh sách tất cả chủ đề"""
        categories = {
            "tai_chinh": [t for t in CHU_DE_PHO_BIEN if any(kw in t.lower() for kw in ["tiền", "lương", "tư", "vay", "nợ", "nhà", "xe"])],
            "cong_viec": [t for t in CHU_DE_PHO_BIEN if any(kw in t.lower() for kw in ["việc", "nghiệp", "tuyển", "phỏng", "hợp đồng"])],
            "tinh_cam": [t for t in CHU_DE_PHO_BIEN if any(kw in t.lower() for kw in ["tình", "yêu", "hôn", "hẹn"])],
            "gia_dinh": [t for t in CHU_DE_PHO_BIEN if any(kw in t.lower() for kw in ["con", "nhà", "đất", "thờ", "táng"])],
            "suc_khoe": [t for t in CHU_DE_PHO_BIEN if any(kw in t.lower() for kw in ["bệnh", "khám", "thuật", "thọ"])],
            "khac": [t for t in CHU_DE_PHO_BIEN if not any(kw in t.lower() for kw in ["tiền", "việc", "tình", "nhà", "bệnh"])]
        }
        
        if category and category in categories:
            return categories[category]
        
        return CHU_DE_PHO_BIEN
    
    def get_smart_suggestion(self):
        """Lấy gợi ý thông minh theo thời điểm"""
        now = datetime.now(VN_TZ)
        recommendations = self.get_recommended_topics()
        
        output = []
        output.append(f"## 💡 GỢI Ý CHỦ ĐỀ - {now.strftime('%H:%M %d/%m/%Y')}")
        output.append("")
        output.append(f"**Giờ hiện tại:** {recommendations['chi']} ({recommendations['gio_hien_tai']})")
        output.append("")
        
        output.append("### 🕐 CHỦ ĐỀ PHÙ HỢP GIỜ NÀY")
        for topic in recommendations["chu_de_theo_gio"]:
            output.append(f"- {topic}")
        output.append("")
        
        output.append("### 📅 CHỦ ĐỀ PHÙ HỢP NGÀY NÀY")
        for topic in recommendations["chu_de_theo_ngay"]:
            output.append(f"- {topic}")
        output.append("")
        
        output.append("### ⭐ TỔNG HỢP KHUYÊN DÙNG")
        for topic in recommendations["tong_hop"][:5]:
            output.append(f"- **{topic}**")
        
        return "\n".join(output)


# Singleton
_advisor = None

def get_topic_advisor(gemini_helper=None):
    global _advisor
    if _advisor is None:
        _advisor = TopicAdvisorAI(gemini_helper)
    return _advisor


if __name__ == "__main__":
    advisor = get_topic_advisor()
    
    print(advisor.get_smart_suggestion())
    print("\n" + "="*50 + "\n")
    print(advisor.analyze_topic_match("Xin việc"))

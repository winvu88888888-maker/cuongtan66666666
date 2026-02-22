"""
CAREER ADVISOR AI - Tư Vấn Sự Nghiệp
Phân tích và tư vấn về công việc, sự nghiệp, thăng tiến
"""


class CareerAdvisorAI:
    """
    AI Tư vấn sự nghiệp
    - Phân tích cơ hội nghề nghiệp
    - Đánh giá thời điểm thay đổi công việc
    - Tư vấn thăng tiến
    """
    
    def __init__(self):
        self.career_indicators = self._load_indicators()
    
    def _load_indicators(self):
        """Load các chỉ báo sự nghiệp"""
        return {
            "thang_tien": {
                "tot": ["Khai Môn cát", "Cửu Thiên hỗ trợ", "Thiên Phụ văn xương"],
                "xau": ["Tử Môn", "Huyền Vũ lọt vào", "Không Vong"]
            },
            "doi_viec": {
                "tot": ["Dịch Mã động", "Thiên Xung di chuyển", "Khai Môn ở cung di"],
                "xau": ["Sinh Môn bị khắc", "Bản thân nhược"]
            },
            "xin_viec": {
                "tot": ["Khai Môn sinh Bản Thân", "Có quý nhân", "Quan Tinh vượng"],
                "xau": ["Khai Môn khắc Bản Thân", "Tử Môn", "Không Vong"]
            },
            "kinh_doanh": {
                "tot": ["Sinh Môn vượng", "Thê Tài tinh tốt", "Thiên Nhậm hỗ trợ"],
                "xau": ["Huynh Đệ tinh động", "Sinh Môn nhược", "Cạnh tranh mạnh"]
            }
        }
    
    def analyze_career_question(self, chart_data, career_topic):
        """Phân tích câu hỏi về sự nghiệp"""
        topic_lower = career_topic.lower()
        
        # Xác định loại câu hỏi
        if any(kw in topic_lower for kw in ["thăng", "tiến", "lên chức"]):
            career_type = "thang_tien"
            dung_than = "Khai Môn + Quan Tinh"
        elif any(kw in topic_lower for kw in ["đổi", "nhảy", "chuyển"]):
            career_type = "doi_viec"
            dung_than = "Dịch Mã + Khai Môn"
        elif any(kw in topic_lower for kw in ["xin", "phỏng vấn", "ứng tuyển"]):
            career_type = "xin_viec"
            dung_than = "Khai Môn"
        elif any(kw in topic_lower for kw in ["kinh doanh", "mở", "buôn"]):
            career_type = "kinh_doanh"
            dung_than = "Sinh Môn"
        else:
            career_type = "xin_viec"
            dung_than = "Khai Môn"
        
        # Phân tích (simplified)
        indicators = self.career_indicators.get(career_type, {})
        
        # Tính điểm dựa trên chart_data
        score = self._calculate_career_score(chart_data, career_type)
        
        return {
            "loai": career_type,
            "dung_than": dung_than,
            "diem": score,
            "danh_gia": self._score_to_verdict(score),
            "chi_tiet": self._generate_career_details(career_type, score),
            "loi_khuyen": self._generate_career_advice(career_type, score)
        }
    
    def _calculate_career_score(self, chart_data, career_type):
        """Tính điểm sự nghiệp"""
        base_score = 50
        
        # Kiểm tra các yếu tố trong chart_data
        nhan_ban = chart_data.get('nhan_ban', {})
        thien_ban = chart_data.get('thien_ban', {})
        than_ban = chart_data.get('than_ban', {})
        
        # Kiểm tra Khai Môn
        for cung, mon in nhan_ban.items():
            if "Khai" in str(mon):
                base_score += 20
            elif "Tử" in str(mon):
                base_score -= 20
        
        # Kiểm tra Cửu Thiên
        for cung, than in than_ban.items():
            if "Cửu Thiên" in str(than):
                base_score += 10
        
        # Kiểm tra Không Vong
        khong_vong = chart_data.get('khong_vong', [])
        if khong_vong:
            base_score -= 15
        
        return max(0, min(100, base_score))
    
    def _score_to_verdict(self, score):
        """Chuyển điểm thành đánh giá"""
        if score >= 80:
            return "RẤT TỐT - Thời điểm lý tưởng"
        elif score >= 60:
            return "TỐT - Có thể tiến hành"
        elif score >= 40:
            return "TRUNG BÌNH - Cần cân nhắc"
        else:
            return "KHÔNG TỐT - Nên chờ thời cơ khác"
    
    def _generate_career_details(self, career_type, score):
        """Tạo chi tiết phân tích"""
        details = {
            "thang_tien": [
                "Vị trí hiện tại có tiềm năng thăng tiến" if score >= 60 else "Cần tích lũy thêm",
                "Có sự hỗ trợ từ cấp trên" if score >= 70 else "Cần tạo quan hệ tốt hơn",
                f"Khả năng thành công: {score}%"
            ],
            "doi_viec": [
                "Thời điểm thích hợp để thay đổi" if score >= 60 else "Chưa phải lúc",
                "Cơ hội mới sẽ tốt hơn" if score >= 70 else "Có rủi ro",
                f"Khả năng thành công: {score}%"
            ],
            "xin_viec": [
                "Hồ sơ sẽ được chú ý" if score >= 60 else "Cần cải thiện hồ sơ",
                "Phỏng vấn sẽ thuận lợi" if score >= 70 else "Cần chuẩn bị kỹ",
                f"Khả năng được nhận: {score}%"
            ],
            "kinh_doanh": [
                "Thời điểm tốt để khởi nghiệp" if score >= 60 else "Chưa thuận lợi",
                "Tiền vốn sẽ sinh lời" if score >= 70 else "Có rủi ro tài chính",
                f"Khả năng thành công: {score}%"
            ]
        }
        return details.get(career_type, [f"Điểm: {score}%"])
    
    def _generate_career_advice(self, career_type, score):
        """Tạo lời khuyên"""
        if score >= 70:
            return [
                "👉 Nên hành động ngay, thời cơ đang thuận lợi",
                "👉 Chuẩn bị kỹ lưỡng để tận dụng cơ hội",
                "👉 Tự tin thể hiện năng lực bản thân"
            ]
        elif score >= 50:
            return [
                "👉 Có thể tiến hành nhưng cẩn thận",
                "👉 Chuẩn bị phương án dự phòng",
                "👉 Nên tham khảo thêm ý kiến người có kinh nghiệm"
            ]
        else:
            return [
                "👉 Nên chờ thời điểm tốt hơn",
                "👉 Tập trung tích lũy kinh nghiệm và kỹ năng",
                "👉 Xem lại các giờ Hoàng Đạo để chọn ngày tốt"
            ]
    
    def get_career_report(self, chart_data, topic):
        """Tạo báo cáo tư vấn sự nghiệp"""
        analysis = self.analyze_career_question(chart_data, topic)
        
        output = []
        output.append(f"## 🏢 TƯ VẤN SỰ NGHIỆP: {topic.upper()}")
        output.append("")
        
        output.append(f"### Điểm đánh giá: **{analysis['diem']}/100**")
        output.append(f"**{analysis['danh_gia']}**")
        output.append("")
        
        output.append("### Chi tiết:")
        for detail in analysis["chi_tiet"]:
            output.append(f"- {detail}")
        output.append("")
        
        output.append("### Lời khuyên:")
        for advice in analysis["loi_khuyen"]:
            output.append(advice)
        
        return "\n".join(output)


# Singleton
_career = None

def get_career_advisor():
    global _career
    if _career is None:
        _career = CareerAdvisorAI()
    return _career


if __name__ == "__main__":
    advisor = get_career_advisor()
    
    chart = {
        "nhan_ban": {6: "Khai Môn"},
        "thien_ban": {6: "Thiên Tâm"},
        "than_ban": {6: "Cửu Thiên"},
        "khong_vong": []
    }
    
    print(advisor.get_career_report(chart, "Xin việc công ty IT"))

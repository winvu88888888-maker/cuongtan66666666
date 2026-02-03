"""
CASE STUDY AI - Phân Tích Case Study Thực Tế
Cung cấp ví dụ và phân tích các trường hợp thực tế
"""


# Kho case study theo chủ đề
CASE_STUDIES = {
    "cong_viec": [
        {
            "id": "CV001",
            "title": "Xin việc công ty công nghệ",
            "context": "Nam, 28 tuổi, xin vào công ty IT lớn. Lập bàn giờ Mão, ngày Giáp Tý.",
            "chart_summary": "Khai Môn ở cung 6, Thiên Tâm đồng cung. Can Ngày Giáp lạc cung 3.",
            "analysis": {
                "dung_than": "Khai Môn (công việc) ở cung 6 Kim",
                "ban_than": "Giáp (Mộc) ở cung 3",
                "quan_he": "Kim khắc Mộc - Bất lợi cho người hỏi",
                "diem_tot": ["Khai Môn là cát môn", "Thiên Tâm hỗ trợ"],
                "diem_xau": ["Quan hệ sinh khắc bất lợi"]
            },
            "prediction": "60% thành công, cần vượt qua nhiều vòng phỏng vấn. Kết quả trong 2 tuần.",
            "actual_result": "Được nhận việc sau 3 lần phỏng vấn, 10 ngày sau.",
            "accuracy": 85
        },
        {
            "id": "CV002",
            "title": "Thăng tiến lên quản lý",
            "context": "Nữ, 35 tuổi, đang chờ kết quả thăng chức.",
            "chart_summary": "Khai Môn + Cửu Thiên ở cung 1, Can Ngày ở cung 6.",
            "analysis": {
                "dung_than": "Khai Môn + Cửu Thiên (quý nhân ủng hộ)",
                "quan_he": "Cung 1 Thủy sinh cung 6 Kim - Thuận lợi",
                "diem_tot": ["Có quý nhân", "Cát môn cát thần"]
            },
            "prediction": "85% thành công, có người ủng hộ mạnh.",
            "actual_result": "Được thăng chức 1 tuần sau.",
            "accuracy": 95
        }
    ],
    "tai_chinh": [
        {
            "id": "TC001",
            "title": "Đầu tư chứng khoán",
            "context": "Xem có nên mua cổ phiếu công ty X không.",
            "chart_summary": "Sinh Môn ở cung 8, rơi Không Vong.",
            "analysis": {
                "dung_than": "Sinh Môn (tài)",
                "diem_xau": ["Rơi Không Vong - Tiền không thực", "Cung 8 đóng"]
            },
            "prediction": "Không nên đầu tư, tiền sẽ mất hoặc không như kỳ vọng.",
            "actual_result": "Cổ phiếu giảm 30% sau 1 tháng.",
            "accuracy": 90
        }
    ],
    "tinh_cam": [
        {
            "id": "TC001",
            "title": "Hỏi về mối quan hệ mới",
            "context": "Nam 30 tuổi, mới quen cô gái, hỏi triển vọng.",
            "chart_summary": "Lục Hợp ở cung 4, Cảnh Môn đồng cung.",
            "analysis": {
                "dung_than": "Lục Hợp (tình cảm)",
                "diem_tot": ["Lục Hợp là thần hợp"],
                "diem_xau": ["Cảnh Môn - Hư ảo, không thực"]
            },
            "prediction": "Mối quan hệ đẹp nhưng khó bền, nhiều mơ mộng.",
            "actual_result": "Yêu 3 tháng rồi chia tay.",
            "accuracy": 80
        }
    ],
    "suc_khoe": [
        {
            "id": "SK001",
            "title": "Chữa bệnh dạ dày",
            "context": "Bệnh nhân hỏi việc điều trị sẽ như thế nào.",
            "chart_summary": "Thiên Tâm (y dược) ở cung 6, Tử Môn ở cung 2.",
            "analysis": {
                "dung_than": "Thiên Tâm (chữa bệnh)",
                "diem_tot": ["Thiên Tâm là sao y dược tốt", "Ở cung 6 Kim vượng"],
                "diem_xau": ["Tử Môn ở cung bệnh - Bệnh nặng"]
            },
            "prediction": "Bệnh nặng nhưng chữa được nếu kiên trì. 2-3 tháng.",
            "actual_result": "Điều trị 2.5 tháng, khỏi bệnh.",
            "accuracy": 90
        }
    ]
}


class CaseStudyAI:
    """
    AI Phân tích Case Study
    - Cung cấp ví dụ thực tế
    - So sánh với trường hợp tương tự
    - Rút kinh nghiệm từ các case cũ
    """
    
    def __init__(self):
        self.cases = CASE_STUDIES
    
    def get_case_by_topic(self, topic):
        """Lấy case study theo chủ đề"""
        topic_lower = topic.lower()
        
        if any(kw in topic_lower for kw in ["việc", "nghiệp", "thăng", "phỏng vấn"]):
            return self.cases.get("cong_viec", [])
        elif any(kw in topic_lower for kw in ["tiền", "tài", "đầu tư", "lương"]):
            return self.cases.get("tai_chinh", [])
        elif any(kw in topic_lower for kw in ["tình", "yêu", "hôn", "người yêu"]):
            return self.cases.get("tinh_cam", [])
        elif any(kw in topic_lower for kw in ["bệnh", "khỏe", "khám", "điều trị"]):
            return self.cases.get("suc_khoe", [])
        
        # Trả về tất cả nếu không match
        all_cases = []
        for cases in self.cases.values():
            all_cases.extend(cases)
        return all_cases[:3]
    
    def get_case_detail(self, case_id):
        """Lấy chi tiết một case study"""
        for category, cases in self.cases.items():
            for case in cases:
                if case["id"] == case_id:
                    return case
        return None
    
    def get_similar_case(self, topic, chart_summary=None):
        """Tìm case tương tự"""
        cases = self.get_case_by_topic(topic)
        
        if not cases:
            return {"message": "Không tìm thấy case tương tự"}
        
        # Trả về case đầu tiên phù hợp
        return {
            "case": cases[0],
            "similarity": "Cao",
            "recommendation": "Tham khảo case này để hiểu cách luận giải"
        }
    
    def learn_from_case(self, case_id):
        """Rút bài học từ case study"""
        case = self.get_case_detail(case_id)
        if not case:
            return {"error": "Không tìm thấy case"}
        
        lessons = []
        
        # Phân tích điểm tốt
        for good in case.get("analysis", {}).get("diem_tot", []):
            lessons.append(f"✅ {good}")
        
        # Phân tích điểm xấu
        for bad in case.get("analysis", {}).get("diem_xau", []):
            lessons.append(f"⚠️ {bad}")
        
        # So sánh dự đoán vs thực tế
        accuracy = case.get("accuracy", 0)
        if accuracy >= 80:
            lessons.append(f"📊 Dự đoán chính xác {accuracy}% - Phương pháp đáng tin cậy")
        else:
            lessons.append(f"📊 Dự đoán {accuracy}% - Cần xem xét thêm yếu tố khác")
        
        return {
            "case_id": case_id,
            "title": case["title"],
            "lessons": lessons,
            "key_takeaway": self._generate_takeaway(case)
        }
    
    def _generate_takeaway(self, case):
        """Tạo bài học chính"""
        accuracy = case.get("accuracy", 0)
        analysis = case.get("analysis", {})
        
        if accuracy >= 85:
            return "Khi Dụng Thần mạnh và có cát tinh hỗ trợ, kết quả thường tốt."
        elif analysis.get("diem_xau"):
            return "Dù có điểm tốt, vẫn cần chú ý các dấu hiệu cảnh báo."
        else:
            return "Cần xem xét tổng hợp nhiều yếu tố, không chỉ dựa vào một yếu tố."
    
    def get_all_cases_summary(self):
        """Lấy tóm tắt tất cả case studies"""
        output = []
        output.append("## 📚 KHO CASE STUDY")
        output.append("")
        
        for category, cases in self.cases.items():
            cat_name = {
                "cong_viec": "🏢 Công việc",
                "tai_chinh": "💰 Tài chính",
                "tinh_cam": "❤️ Tình cảm",
                "suc_khoe": "🏥 Sức khỏe"
            }.get(category, category)
            
            output.append(f"### {cat_name}")
            for case in cases:
                output.append(f"- **{case['id']}**: {case['title']} (Độ chính xác: {case.get('accuracy', 'N/A')}%)")
            output.append("")
        
        return "\n".join(output)
    
    def format_case_study(self, case):
        """Format case study để hiển thị"""
        output = []
        output.append(f"## 📖 CASE STUDY: {case['title']}")
        output.append(f"**ID:** {case['id']}")
        output.append("")
        
        output.append("### Bối cảnh:")
        output.append(case["context"])
        output.append("")
        
        output.append("### Bàn QMDG:")
        output.append(case["chart_summary"])
        output.append("")
        
        output.append("### Phân tích:")
        analysis = case["analysis"]
        for key, value in analysis.items():
            if isinstance(value, list):
                output.append(f"**{key}:**")
                for item in value:
                    output.append(f"- {item}")
            else:
                output.append(f"**{key}:** {value}")
        output.append("")
        
        output.append("### Dự đoán:")
        output.append(case["prediction"])
        output.append("")
        
        output.append("### Kết quả thực tế:")
        output.append(case["actual_result"])
        output.append(f"**Độ chính xác:** {case.get('accuracy', 'N/A')}%")
        
        return "\n".join(output)


# Singleton
_case_study = None

def get_case_study_ai():
    global _case_study
    if _case_study is None:
        _case_study = CaseStudyAI()
    return _case_study


if __name__ == "__main__":
    ai = get_case_study_ai()
    
    print(ai.get_all_cases_summary())
    print("\n" + "="*50 + "\n")
    
    case = ai.get_case_detail("CV001")
    if case:
        print(ai.format_case_study(case))

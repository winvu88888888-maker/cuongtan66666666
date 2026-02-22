"""
WEALTH ADVISOR AI - Tư Vấn Tài Chính
Phân tích và tư vấn về tiền bạc, đầu tư, tài sản
"""


class WealthAdvisorAI:
    """
    AI Tư vấn tài chính
    - Phân tích cơ hội tài chính
    - Đánh giá đầu tư
    - Tư vấn cầu tài
    """
    
    def __init__(self):
        self.wealth_indicators = self._load_indicators()
    
    def _load_indicators(self):
        """Load các chỉ báo tài chính"""
        return {
            "tot": {
                "Sinh Môn": "Cửa sinh tài, tiền vào ổn định",
                "Thiên Nhậm": "Sao tài lộc, có thu nhập",
                "Thiên Phụ": "Có người giúp đỡ tiền bạc",
                "Thái Âm": "Tài ẩn, có tiền không lộ",
                "Lục Hợp": "Hợp tác có lợi nhuận"
            },
            "xau": {
                "Huynh Đệ": "Hao tài, bị cạnh tranh lấy mất",
                "Không Vong": "Tiền hư, không thực",
                "Tử Môn": "Mất tiền, lỗ vốn",
                "Thiên Nhuế": "Tiền đi chữa bệnh",
                "Đằng Xà": "Tiền có nguồn không rõ, rủi ro"
            },
            "dau_tu": {
                "tot": ["Sinh Môn vượng", "Thê Tài sinh Bản Thân", "Thiên Nhậm tốt"],
                "xau": ["Huynh Đệ động", "Sinh Môn Không Vong", "Thê Tài bị khắc"]
            }
        }
    
    def analyze_wealth(self, chart_data, wealth_topic):
        """Phân tích câu hỏi về tài chính"""
        topic_lower = wealth_topic.lower()
        
        # Xác định loại câu hỏi
        if any(kw in topic_lower for kw in ["đầu tư", "chứng khoán", "crypto"]):
            wealth_type = "dau_tu"
            risk_level = "cao"
        elif any(kw in topic_lower for kw in ["lương", "thu nhập"]):
            wealth_type = "thu_nhap"
            risk_level = "thấp"
        elif any(kw in topic_lower for kw in ["vay", "nợ"]):
            wealth_type = "vay_no"
            risk_level = "trung bình"
        elif any(kw in topic_lower for kw in ["mua", "nhà", "đất", "xe"]):
            wealth_type = "tai_san"
            risk_level = "trung bình"
        else:
            wealth_type = "cau_tai"
            risk_level = "trung bình"
        
        # Phân tích
        score = self._calculate_wealth_score(chart_data, wealth_type)
        
        return {
            "loai": wealth_type,
            "rui_ro": risk_level,
            "diem": score,
            "danh_gia": self._score_to_verdict(score),
            "chi_tiet": self._generate_wealth_details(chart_data),
            "so_luong": self._estimate_amount(chart_data, score),
            "thoi_gian": self._estimate_timing(chart_data),
            "loi_khuyen": self._generate_wealth_advice(score, wealth_type)
        }
    
    def _calculate_wealth_score(self, chart_data, wealth_type):
        """Tính điểm tài chính"""
        base_score = 50
        
        nhan_ban = chart_data.get('nhan_ban', {})
        thien_ban = chart_data.get('thien_ban', {})
        than_ban = chart_data.get('than_ban', {})
        
        # Kiểm tra Sinh Môn
        for cung, mon in nhan_ban.items():
            if "Sinh" in str(mon):
                base_score += 20
            elif "Tử" in str(mon):
                base_score -= 20
        
        # Kiểm tra Thiên Nhậm
        for cung, sao in thien_ban.items():
            if "Thiên Nhậm" in str(sao):
                base_score += 15
        
        # Kiểm tra Huyền Vũ (hao tài)
        for cung, than in than_ban.items():
            if "Huyền Vũ" in str(than):
                base_score -= 10
        
        # Không Vong
        if chart_data.get('khong_vong'):
            base_score -= 15
        
        return max(0, min(100, base_score))
    
    def _score_to_verdict(self, score):
        """Chuyển điểm thành đánh giá"""
        if score >= 80:
            return "RẤT TỐT - Tài vận hưng thịnh"
        elif score >= 60:
            return "TỐT - Có tiền, nhưng cần cẩn thận"
        elif score >= 40:
            return "TRUNG BÌNH - Khó kiếm, cần cố gắng"
        else:
            return "XẤU - Hao tài, không nên mạo hiểm"
    
    def _generate_wealth_details(self, chart_data):
        """Tạo chi tiết phân tích tài chính"""
        details = []
        
        nhan_ban = chart_data.get('nhan_ban', {})
        thien_ban = chart_data.get('thien_ban', {})
        
        # Phân tích các yếu tố
        for cung, mon in nhan_ban.items():
            mon_str = str(mon)
            if mon_str in self.wealth_indicators["tot"]:
                details.append(f"✅ {mon_str}: {self.wealth_indicators['tot'][mon_str]}")
        
        for cung, sao in thien_ban.items():
            sao_str = str(sao)
            if sao_str in self.wealth_indicators["tot"]:
                details.append(f"✅ {sao_str}: {self.wealth_indicators['tot'][sao_str]}")
        
        # Cảnh báo
        if chart_data.get('khong_vong'):
            details.append("⚠️ Không Vong: Tiền chưa chắc chắn")
        
        if not details:
            details.append("📊 Tài vận ổn định, không có biến động lớn")
        
        return details
    
    def _estimate_amount(self, chart_data, score):
        """Ước tính số lượng tiền"""
        # Dựa trên số cung Sinh Môn
        base = 0
        for cung, mon in chart_data.get('nhan_ban', {}).items():
            if "Sinh" in str(mon):
                base = cung
                break
        
        if base == 0:
            base = 5
        
        multiplier = score / 10
        amount = base * multiplier
        
        return {
            "con_so": int(amount),
            "y_nghia": f"Con số liên quan đến tài: {int(amount)} (đơn vị: triệu/trăm triệu tùy ngữ cảnh)"
        }
    
    def _estimate_timing(self, chart_data):
        """Ước tính thời gian có tiền"""
        # Dựa trên Dịch Mã và các yếu tố động
        if chart_data.get('dich_ma'):
            return "Nhanh - 1-2 tuần"
        elif chart_data.get('khong_vong'):
            return "Chậm - 2-3 tháng hoặc hơn"
        else:
            return "Trung bình - 1-2 tháng"
    
    def _generate_wealth_advice(self, score, wealth_type):
        """Tạo lời khuyên tài chính"""
        if score >= 70:
            advice = [
                "💰 Thời điểm tốt để cầu tài",
                "📈 Có thể đầu tư vừa phải",
                "🤝 Hợp tác kinh doanh sẽ có lợi"
            ]
        elif score >= 50:
            advice = [
                "💰 Có tiền nhưng không nhiều",
                "⚠️ Đầu tư cẩn thận, không all-in",
                "📊 Nên giữ ổn định, tránh mạo hiểm"
            ]
        else:
            advice = [
                "🛑 Không nên đầu tư lúc này",
                "💼 Tập trung công việc ổn định",
                "🔒 Tiết kiệm, tránh chi tiêu lớn"
            ]
        
        # Thêm advice theo loại
        if wealth_type == "dau_tu" and score < 60:
            advice.append("📉 Rủi ro đầu tư cao, có thể lỗ")
        elif wealth_type == "vay_no":
            if score >= 50:
                advice.append("✅ Có thể vay, khả năng trả được")
            else:
                advice.append("❌ Không nên vay, khó trả")
        
        return advice
    
    def get_wealth_report(self, chart_data, topic):
        """Tạo báo cáo tư vấn tài chính"""
        analysis = self.analyze_wealth(chart_data, topic)
        
        output = []
        output.append(f"## 💰 TƯ VẤN TÀI CHÍNH: {topic.upper()}")
        output.append("")
        
        output.append(f"### Điểm: **{analysis['diem']}/100**")
        output.append(f"**{analysis['danh_gia']}**")
        output.append(f"**Mức rủi ro:** {analysis['rui_ro']}")
        output.append("")
        
        output.append("### Chi tiết:")
        for detail in analysis["chi_tiet"]:
            output.append(f"- {detail}")
        output.append("")
        
        output.append("### Số lượng:")
        output.append(f"- {analysis['so_luong']['y_nghia']}")
        output.append("")
        
        output.append("### Thời gian:")
        output.append(f"- {analysis['thoi_gian']}")
        output.append("")
        
        output.append("### Lời khuyên:")
        for advice in analysis["loi_khuyen"]:
            output.append(advice)
        
        return "\n".join(output)


# Singleton
_wealth = None

def get_wealth_advisor():
    global _wealth
    if _wealth is None:
        _wealth = WealthAdvisorAI()
    return _wealth


if __name__ == "__main__":
    advisor = get_wealth_advisor()
    
    chart = {
        "nhan_ban": {2: "Sinh Môn", 6: "Khai Môn"},
        "thien_ban": {2: "Thiên Nhậm", 6: "Thiên Tâm"},
        "than_ban": {2: "Thái Âm"},
        "khong_vong": [],
        "dich_ma": None
    }
    
    print(advisor.get_wealth_report(chart, "Đầu tư chứng khoán"))

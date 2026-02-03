"""
HEALTH ADVISOR AI - Tư Vấn Sức Khỏe
Phân tích và tư vấn về sức khỏe, bệnh tật từ góc nhìn QMDG
"""


class HealthAdvisorAI:
    """
    AI Tư vấn sức khỏe
    - Phân tích triển vọng sức khỏe
    - Đánh giá tình trạng bệnh
    - Tư vấn thời điểm điều trị
    """
    
    def __init__(self):
        self.health_indicators = self._load_indicators()
    
    def _load_indicators(self):
        """Load các chỉ báo sức khỏe"""
        return {
            "sao_tot": {
                "Thiên Tâm": "Sao y dược, có thầy giỏi chữa được",
                "Thiên Nhậm": "Sao tài lộc, bệnh nhẹ, mau khỏi",
                "Thiên Phụ": "Có người giúp đỡ chăm sóc"
            },
            "sao_xau": {
                "Thiên Nhuế": "Sao bệnh tật, bệnh nặng, kéo dài",
                "Thiên Bồng": "Bệnh ngầm, khó phát hiện",
                "Thiên Anh": "Sốt, viêm, nóng trong người"
            },
            "mon_benh": {
                "Tử Môn": "Bệnh nặng, nguy kịch",
                "Kinh Môn": "Bệnh gây lo lắng, stress",
                "Thương Môn": "Bệnh do chấn thương, tai nạn"
            },
            "mon_khoi": {
                "Khai Môn": "Bệnh nhẹ, dễ chữa",
                "Sinh Môn": "Có cơ hội hồi phục",
                "Hưu Môn": "Cần nghỉ ngơi, bệnh từ từ khỏi"
            }
        }
    
    def analyze_health(self, chart_data, health_topic):
        """Phân tích câu hỏi về sức khỏe"""
        topic_lower = health_topic.lower()
        
        # Xác định Dụng Thần
        if any(kw in topic_lower for kw in ["khám", "chữa", "điều trị"]):
            dung_than = "Thiên Tâm (Y dược)"
            dung_than_type = "dieu_tri"
        elif any(kw in topic_lower for kw in ["bệnh gì", "nguyên nhân"]):
            dung_than = "Thiên Nhuế (Bệnh)"
            dung_than_type = "chan_doan"
        else:
            dung_than = "Thiên Tâm + Tử Tôn"
            dung_than_type = "suc_khoe_chung"
        
        # Phân tích
        score = self._calculate_health_score(chart_data, dung_than_type)
        prognosis = self._determine_prognosis(chart_data, score)
        
        return {
            "dung_than": dung_than,
            "loai": dung_than_type,
            "diem": score,
            "tien_luong": prognosis,
            "chi_tiet": self._generate_health_details(chart_data, dung_than_type),
            "loi_khuyen": self._generate_health_advice(score, dung_than_type)
        }
    
    def _calculate_health_score(self, chart_data, dung_than_type):
        """Tính điểm sức khỏe"""
        base_score = 50
        
        nhan_ban = chart_data.get('nhan_ban', {})
        thien_ban = chart_data.get('thien_ban', {})
        
        # Kiểm tra sao
        for cung, sao in thien_ban.items():
            sao_str = str(sao)
            if "Thiên Tâm" in sao_str:
                base_score += 20
            elif "Thiên Nhuế" in sao_str:
                base_score -= 15
        
        # Kiểm tra Môn
        for cung, mon in nhan_ban.items():
            mon_str = str(mon)
            if "Tử" in mon_str:
                base_score -= 25
            elif "Sinh" in mon_str:
                base_score += 15
        
        # Không Vong
        if chart_data.get('khong_vong'):
            base_score -= 10
        
        return max(0, min(100, base_score))
    
    def _determine_prognosis(self, chart_data, score):
        """Xác định tiên lượng"""
        if score >= 75:
            return "TỐT - Bệnh nhẹ hoặc mau khỏi"
        elif score >= 50:
            return "TRUNG BÌNH - Cần điều trị kiên trì"
        elif score >= 30:
            return "CẦN LƯU Ý - Bệnh có thể kéo dài"
        else:
            return "NGHIÊM TRỌNG - Cần chú ý đặc biệt"
    
    def _generate_health_details(self, chart_data, dung_than_type):
        """Tạo chi tiết phân tích sức khỏe"""
        thien_ban = chart_data.get('thien_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        
        details = []
        
        # Phân tích theo sao
        for cung, sao in thien_ban.items():
            sao_str = str(sao)
            if sao_str in self.health_indicators["sao_tot"]:
                details.append(f"✅ {sao_str}: {self.health_indicators['sao_tot'][sao_str]}")
            elif sao_str in self.health_indicators["sao_xau"]:
                details.append(f"⚠️ {sao_str}: {self.health_indicators['sao_xau'][sao_str]}")
        
        # Phân tích theo Môn
        for cung, mon in nhan_ban.items():
            for mon_key, meaning in self.health_indicators["mon_benh"].items():
                if mon_key in str(mon):
                    details.append(f"⚠️ {mon_key}: {meaning}")
            for mon_key, meaning in self.health_indicators["mon_khoi"].items():
                if mon_key in str(mon):
                    details.append(f"✅ {mon_key}: {meaning}")
        
        if not details:
            details.append("📊 Không có yếu tố đặc biệt, sức khỏe ổn định")
        
        return details
    
    def _generate_health_advice(self, score, dung_than_type):
        """Tạo lời khuyên sức khỏe"""
        if score >= 70:
            return [
                "🏥 Điều trị sẽ hiệu quả, đúng phác đồ",
                "💊 Uống thuốc đầy đủ, bệnh sẽ thuyên giảm",
                "🧘 Nghỉ ngơi hợp lý, giữ tinh thần lạc quan"
            ]
        elif score >= 50:
            return [
                "🏥 Cần kiên trì điều trị",
                "💊 Có thể cần thay đổi phác đồ nếu không thuyên giảm",
                "🍎 Chú ý chế độ dinh dưỡng và sinh hoạt"
            ]
        else:
            return [
                "🏥 Nên khám chuyên khoa, xin ý kiến nhiều bác sĩ",
                "⚠️ Cần theo dõi sát sao",
                "🙏 Giữ tinh thần, tránh lo lắng quá mức"
            ]
    
    def get_health_report(self, chart_data, topic):
        """Tạo báo cáo tư vấn sức khỏe"""
        analysis = self.analyze_health(chart_data, topic)
        
        output = []
        output.append(f"## 🏥 TƯ VẤN SỨC KHỎE: {topic.upper()}")
        output.append("")
        output.append(f"### Dụng Thần: {analysis['dung_than']}")
        output.append(f"### Tiên lượng: **{analysis['tien_luong']}**")
        output.append(f"### Điểm: {analysis['diem']}/100")
        output.append("")
        
        output.append("### Chi tiết:")
        for detail in analysis["chi_tiet"]:
            output.append(f"- {detail}")
        output.append("")
        
        output.append("### Lời khuyên:")
        for advice in analysis["loi_khuyen"]:
            output.append(advice)
        
        output.append("")
        output.append("> ⚠️ *Lưu ý: Đây chỉ là tham khảo từ góc độ QMDG. Luôn tuân theo chỉ định của bác sĩ.*")
        
        return "\n".join(output)


# Singleton
_health = None

def get_health_advisor():
    global _health
    if _health is None:
        _health = HealthAdvisorAI()
    return _health


if __name__ == "__main__":
    advisor = get_health_advisor()
    
    chart = {
        "nhan_ban": {6: "Sinh Môn", 2: "Tử Môn"},
        "thien_ban": {6: "Thiên Tâm", 2: "Thiên Nhuế"},
        "khong_vong": []
    }
    
    print(advisor.get_health_report(chart, "Điều trị bệnh dạ dày"))

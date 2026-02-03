"""
RELATIONSHIP AI - Phân Tích Tương Hợp
Phân tích mối quan hệ, hôn nhân, tình cảm
"""


class RelationshipAI:
    """
    AI Phân tích tương hợp
    - Đánh giá mối quan hệ tình cảm
    - Phân tích hôn nhân
    - Tư vấn quan hệ
    """
    
    def __init__(self):
        self.relationship_indicators = self._load_indicators()
    
    def _load_indicators(self):
        """Load các chỉ báo quan hệ"""
        return {
            "tinh_cam": {
                "tot": {
                    "Lục Hợp": "Thần hòa hợp, quan hệ tốt đẹp",
                    "Thái Âm": "Tình cảm sâu đậm, kín đáo",
                    "Cửu Thiên": "Được quý nhân ủng hộ"
                },
                "xau": {
                    "Đằng Xà": "Có bí mật, ghen tuông",
                    "Câu Trần": "Vướng bận, rắc rối",
                    "Huyền Vũ": "Có kẻ thứ ba, phản bội"
                }
            },
            "mon": {
                "tot": ["Khai Môn", "Hưu Môn", "Sinh Môn"],
                "xau": ["Tử Môn", "Kinh Môn", "Thương Môn"]
            },
            "ngu_hanh_hop": {
                "Mộc": {"sinh": "Hỏa", "khac": "Thổ", "bi_khac": "Kim"},
                "Hỏa": {"sinh": "Thổ", "khac": "Kim", "bi_khac": "Thủy"},
                "Thổ": {"sinh": "Kim", "khac": "Thủy", "bi_khac": "Mộc"},
                "Kim": {"sinh": "Thủy", "khac": "Mộc", "bi_khac": "Hỏa"},
                "Thủy": {"sinh": "Mộc", "khac": "Hỏa", "bi_khac": "Thổ"}
            }
        }
    
    def analyze_relationship(self, chart_data, topic):
        """Phân tích câu hỏi về quan hệ"""
        topic_lower = topic.lower()
        
        # Xác định loại quan hệ
        if any(kw in topic_lower for kw in ["hôn", "kết hôn", "cưới"]):
            rel_type = "hon_nhan"
            dung_than = "Lục Hợp + Hưu Môn"
        elif any(kw in topic_lower for kw in ["yêu", "tình", "người yêu"]):
            rel_type = "tinh_yeu"
            dung_than = "Lục Hợp"
        elif any(kw in topic_lower for kw in ["chia tay", "ly hôn"]):
            rel_type = "chia_tay"
            dung_than = "Thương Môn"
        else:
            rel_type = "quan_he_chung"
            dung_than = "Lục Hợp"
        
        # Phân tích
        score = self._calculate_relationship_score(chart_data, rel_type)
        
        return {
            "loai": rel_type,
            "dung_than": dung_than,
            "diem": score,
            "tuong_hop": self._score_to_compatibility(score),
            "chi_tiet": self._generate_relationship_details(chart_data, rel_type),
            "loi_khuyen": self._generate_relationship_advice(score, rel_type)
        }
    
    def _calculate_relationship_score(self, chart_data, rel_type):
        """Tính điểm tương hợp"""
        base_score = 50
        
        than_ban = chart_data.get('than_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        
        # Kiểm tra Lục Hợp
        for cung, than in than_ban.items():
            if "Lục Hợp" in str(than):
                base_score += 25
            elif "Huyền Vũ" in str(than):
                base_score -= 20
            elif "Đằng Xà" in str(than):
                base_score -= 10
        
        # Kiểm tra Môn
        for cung, mon in nhan_ban.items():
            if "Hưu" in str(mon):
                base_score += 15
            elif "Tử" in str(mon) or "Kinh" in str(mon):
                base_score -= 15
        
        return max(0, min(100, base_score))
    
    def _score_to_compatibility(self, score):
        """Chuyển điểm thành mức tương hợp"""
        if score >= 80:
            return "RẤT TƯƠNG HỢP - Thiên tác chi hợp"
        elif score >= 60:
            return "TƯƠNG HỢP - Quan hệ tốt đẹp"
        elif score >= 40:
            return "TRUNG BÌNH - Cần nỗ lực cả hai"
        else:
            return "KHÔNG TƯƠNG HỢP - Nhiều trở ngại"
    
    def _generate_relationship_details(self, chart_data, rel_type):
        """Tạo chi tiết phân tích quan hệ"""
        details = []
        
        than_ban = chart_data.get('than_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        
        for cung, than in than_ban.items():
            than_str = str(than)
            if than_str in self.relationship_indicators["tinh_cam"]["tot"]:
                details.append(f"✅ {than_str}: {self.relationship_indicators['tinh_cam']['tot'][than_str]}")
            elif than_str in self.relationship_indicators["tinh_cam"]["xau"]:
                details.append(f"⚠️ {than_str}: {self.relationship_indicators['tinh_cam']['xau'][than_str]}")
        
        for cung, mon in nhan_ban.items():
            mon_str = str(mon)
            if any(m in mon_str for m in self.relationship_indicators["mon"]["tot"]):
                details.append(f"✅ {mon_str}: Cửa tốt cho quan hệ")
            elif any(m in mon_str for m in self.relationship_indicators["mon"]["xau"]):
                details.append(f"⚠️ {mon_str}: Cửa xấu cho quan hệ")
        
        if not details:
            details.append("📊 Quan hệ ổn định, không có điểm đặc biệt")
        
        return details
    
    def _generate_relationship_advice(self, score, rel_type):
        """Tạo lời khuyên quan hệ"""
        if score >= 70:
            advice = [
                "❤️ Quan hệ rất tốt đẹp",
                "💍 Thích hợp tiến xa hơn (hẹn hò/kết hôn)",
                "🌟 Hai người hợp nhau, nên trân trọng"
            ]
        elif score >= 50:
            advice = [
                "💛 Quan hệ có tiềm năng nhưng cần cố gắng",
                "🤝 Cần hiểu và nhường nhịn nhau",
                "📞 Giao tiếp nhiều hơn để hiểu nhau"
            ]
        else:
            advice = [
                "💔 Quan hệ gặp nhiều khó khăn",
                "⚠️ Cân nhắc kỹ trước khi tiến xa",
                "🔍 Tìm hiểu thêm về người kia"
            ]
        
        if rel_type == "chia_tay":
            if score >= 50:
                advice = ["Có thể hàn gắn được", "Cần thời gian làm lành"]
            else:
                advice = ["Khó hàn gắn", "Nên chấp nhận và tiến về phía trước"]
        
        return advice
    
    def check_compatibility_by_element(self, element1, element2):
        """Kiểm tra tương hợp theo Ngũ hành"""
        e1 = element1.capitalize()
        e2 = element2.capitalize()
        
        if e1 not in self.relationship_indicators["ngu_hanh_hop"]:
            return {"error": "Hành không hợp lệ"}
        
        rel = self.relationship_indicators["ngu_hanh_hop"][e1]
        
        if e2 == rel["sinh"]:
            return {"compatibility": "TỐT", "detail": f"{e1} sinh {e2} - Hỗ trợ, yêu thương"}
        elif e2 == rel["khac"]:
            return {"compatibility": "XẤU", "detail": f"{e1} khắc {e2} - Xung đột, mâu thuẫn"}
        elif e2 == rel["bi_khac"]:
            return {"compatibility": "TRUNG BÌNH", "detail": f"{e1} bị {e2} khắc - Cần nhường nhịn"}
        elif e1 == e2:
            return {"compatibility": "HÒA", "detail": f"{e1} - {e2} - Cùng hành, tương đồng"}
        else:
            return {"compatibility": "BÌNH", "detail": "Không sinh không khắc"}
    
    def get_relationship_report(self, chart_data, topic):
        """Tạo báo cáo quan hệ"""
        analysis = self.analyze_relationship(chart_data, topic)
        
        output = []
        output.append(f"## ❤️ PHÂN TÍCH QUAN HỆ: {topic.upper()}")
        output.append("")
        
        output.append(f"### Dụng Thần: {analysis['dung_than']}")
        output.append(f"### Điểm tương hợp: **{analysis['diem']}/100**")
        output.append(f"**{analysis['tuong_hop']}**")
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
_relationship = None

def get_relationship_ai():
    global _relationship
    if _relationship is None:
        _relationship = RelationshipAI()
    return _relationship


if __name__ == "__main__":
    ai = get_relationship_ai()
    
    chart = {
        "than_ban": {4: "Lục Hợp", 6: "Thái Âm"},
        "nhan_ban": {4: "Hưu Môn", 6: "Khai Môn"},
    }
    
    print(ai.get_relationship_report(chart, "Hỏi về người yêu mới quen"))

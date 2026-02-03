"""
DIRECTION ADVISOR AI - Tư Vấn Phương Hướng
Phân tích phương hướng tốt/xấu theo QMDG
"""


# Cửu Cung và Phương Hướng
CUNG_HUONG = {
    1: {"huong": "Bắc", "hanh": "Thủy", "mau": "Đen"},
    2: {"huong": "Tây Nam", "hanh": "Thổ", "mau": "Vàng"},
    3: {"huong": "Đông", "hanh": "Mộc", "mau": "Xanh lá"},
    4: {"huong": "Đông Nam", "hanh": "Mộc", "mau": "Xanh lục"},
    5: {"huong": "Trung Cung", "hanh": "Thổ", "mau": "Vàng"},
    6: {"huong": "Tây Bắc", "hanh": "Kim", "mau": "Trắng"},
    7: {"huong": "Tây", "hanh": "Kim", "mau": "Trắng"},
    8: {"huong": "Đông Bắc", "hanh": "Thổ", "mau": "Vàng"},
    9: {"huong": "Nam", "hanh": "Hỏa", "mau": "Đỏ"}
}

# Phương tốt theo Can ngày
HUONG_TOT = {
    "Giáp": [1, 3, 4],  # Thủy sinh Mộc
    "Ất": [1, 3, 4],
    "Bính": [3, 4, 9],  # Mộc sinh Hỏa
    "Đinh": [3, 4, 9],
    "Mậu": [9, 2, 5, 8],  # Hỏa sinh Thổ
    "Kỷ": [9, 2, 5, 8],
    "Canh": [2, 5, 8, 6, 7],  # Thổ sinh Kim
    "Tân": [2, 5, 8, 6, 7],
    "Nhâm": [6, 7, 1],  # Kim sinh Thủy
    "Quý": [6, 7, 1]
}


class DirectionAdvisorAI:
    """
    AI Tư vấn phương hướng
    - Xác định phương tốt/xấu
    - Tư vấn hướng xuất hành
    - Phân tích hướng nhà
    """
    
    def __init__(self):
        self.cung_huong = CUNG_HUONG
        self.huong_tot = HUONG_TOT
    
    def get_good_directions(self, can_ngay):
        """Lấy các phương tốt theo Can ngày"""
        good_cung = self.huong_tot.get(can_ngay, [])
        result = []
        
        for cung in good_cung:
            info = self.cung_huong.get(cung, {})
            result.append({
                "cung": cung,
                "huong": info.get("huong", ""),
                "hanh": info.get("hanh", ""),
                "mau": info.get("mau", "")
            })
        
        return result
    
    def get_bad_directions(self, can_ngay):
        """Lấy các phương xấu (khắc Can ngày)"""
        can_hanh = {
            "Giáp": "Mộc", "Ất": "Mộc",
            "Bính": "Hỏa", "Đinh": "Hỏa",
            "Mậu": "Thổ", "Kỷ": "Thổ",
            "Canh": "Kim", "Tân": "Kim",
            "Nhâm": "Thủy", "Quý": "Thủy"
        }
        
        hanh = can_hanh.get(can_ngay, "Mộc")
        
        # Hành khắc ta
        khac_map = {
            "Mộc": "Kim",
            "Hỏa": "Thủy",
            "Thổ": "Mộc",
            "Kim": "Hỏa",
            "Thủy": "Thổ"
        }
        hanh_khac = khac_map.get(hanh, "Kim")
        
        bad_directions = []
        for cung, info in self.cung_huong.items():
            if info["hanh"] == hanh_khac:
                bad_directions.append({
                    "cung": cung,
                    "huong": info["huong"],
                    "hanh": info["hanh"],
                    "ly_do": f"{info['hanh']} khắc {hanh}"
                })
        
        return bad_directions
    
    def analyze_direction(self, chart_data, target_direction):
        """Phân tích một hướng cụ thể"""
        target_lower = target_direction.lower()
        
        # Tìm cung tương ứng
        target_cung = None
        for cung, info in self.cung_huong.items():
            if info["huong"].lower() in target_lower:
                target_cung = cung
                break
        
        if not target_cung:
            return {"error": f"Không xác định được hướng: {target_direction}"}
        
        # Lấy thông tin cung
        nhan_ban = chart_data.get('nhan_ban', {})
        thien_ban = chart_data.get('thien_ban', {})
        than_ban = chart_data.get('than_ban', {})
        
        cung_info = self.cung_huong[target_cung]
        mon = nhan_ban.get(target_cung, "")
        sao = thien_ban.get(target_cung, "")
        than = than_ban.get(target_cung, "")
        
        # Đánh giá
        score = 50
        notes = []
        
        # Kiểm tra Môn
        if "Khai" in str(mon):
            score += 25
            notes.append("✅ Khai Môn - Đại cát")
        elif "Sinh" in str(mon):
            score += 20
            notes.append("✅ Sinh Môn - Cát")
        elif "Tử" in str(mon):
            score -= 30
            notes.append("❌ Tử Môn - Đại hung")
        
        # Kiểm tra Thần
        if "Cửu Thiên" in str(than):
            score += 15
            notes.append("✅ Cửu Thiên - Có quý nhân")
        elif "Huyền Vũ" in str(than):
            score -= 15
            notes.append("⚠️ Huyền Vũ - Có kẻ tiểu nhân")
        
        score = max(0, min(100, score))
        
        return {
            "huong": cung_info["huong"],
            "cung": target_cung,
            "mon": str(mon),
            "sao": str(sao),
            "than": str(than),
            "score": score,
            "verdict": self._score_to_verdict(score),
            "notes": notes
        }
    
    def _score_to_verdict(self, score):
        """Chuyển điểm thành đánh giá"""
        if score >= 80:
            return "RẤT TỐT - Đại cát, nên đi"
        elif score >= 60:
            return "TỐT - Có thể đi"
        elif score >= 40:
            return "TRUNG BÌNH - Cẩn thận"
        else:
            return "XẤU - Nên tránh"
    
    def recommend_travel_direction(self, chart_data, can_ngay):
        """Khuyến nghị hướng xuất hành"""
        good = self.get_good_directions(can_ngay)
        bad = self.get_bad_directions(can_ngay)
        
        # Phân tích từng hướng tốt theo bàn
        recommendations = []
        for direction in good:
            analysis = self.analyze_direction(chart_data, direction["huong"])
            if analysis.get("score", 0) >= 60:
                recommendations.append({
                    **direction,
                    "score": analysis["score"],
                    "details": analysis.get("notes", [])
                })
        
        # Sắp xếp theo điểm
        recommendations.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return {
            "khuyen_nghi": recommendations[:3],
            "nen_tranh": bad,
            "can_ngay": can_ngay
        }
    
    def get_direction_report(self, chart_data, can_ngay):
        """Tạo báo cáo phương hướng"""
        rec = self.recommend_travel_direction(chart_data, can_ngay)
        
        output = []
        output.append(f"## 🧭 PHÂN TÍCH PHƯƠNG HƯỚNG")
        output.append(f"**Can ngày:** {can_ngay}")
        output.append("")
        
        output.append("### ✅ Phương khuyên dùng:")
        for r in rec["khuyen_nghi"]:
            output.append(f"- **{r['huong']}** (Cung {r['cung']}) - {r['hanh']} - Điểm: {r.get('score', 'N/A')}")
        output.append("")
        
        output.append("### ❌ Phương nên tránh:")
        for b in rec["nen_tranh"]:
            output.append(f"- **{b['huong']}** - {b.get('ly_do', '')}")
        output.append("")
        
        output.append("### Lưu ý:")
        output.append("- Nên xuất hành vào giờ Hoàng Đạo")
        output.append("- Tránh hướng có Tử Môn, Kinh Môn")
        
        return "\n".join(output)


# Singleton
_advisor = None

def get_direction_advisor():
    global _advisor
    if _advisor is None:
        _advisor = DirectionAdvisorAI()
    return _advisor


if __name__ == "__main__":
    advisor = get_direction_advisor()
    
    chart = {
        "nhan_ban": {1: "Khai Môn", 6: "Sinh Môn", 9: "Tử Môn"},
        "thien_ban": {1: "Thiên Tâm", 6: "Thiên Nhậm"},
        "than_ban": {1: "Cửu Thiên", 6: "Lục Hợp"}
    }
    
    print(advisor.get_direction_report(chart, "Giáp"))

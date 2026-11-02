"""
HEALTH ADVISOR AI - Chuyên Gia Y Dịch & Chẩn Đoán Sức Khỏe (V99.9 Deep Focus)
Phân tích trực tiếp Sao Thiên Nhuế (Bệnh tinh) vs Sao Thiên Tâm / Ất Kỳ (Bác sĩ / Thuốc men).
"""

CUNG_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


class HealthAdvisorAI:
    def __init__(self):
        pass

    def analyze_health(self, chart_data, health_topic):
        chart = chart_data if isinstance(chart_data, dict) else {}
        tb = chart.get("thien_ban", {}) or {}
        nb = chart.get("nhan_ban", {}) or {}
        sb = chart.get("than_ban", {}) or {}

        cung_nhue = 2
        cung_tam = 6
        for k, v in tb.items():
            if "Nhuế" in str(v):
                try:
                    cung_nhue = int(k)
                except Exception:
                    pass
            if "Tâm" in str(v):
                try:
                    cung_tam = int(k)
                except Exception:
                    pass

        h_nhue = CUNG_HANH.get(cung_nhue, "Thổ")
        h_tam = CUNG_HANH.get(cung_tam, "Kim")
        cua_nhue = str(nb.get(cung_nhue, nb.get(str(cung_nhue), "Đỗ Môn")))
        than_nhue = str(sb.get(cung_nhue, sb.get(str(cung_nhue), "Bạch Hổ")))

        score = 58
        details = [f"🏥 Sao Bệnh Tinh (Thiên Nhuế) đóng tại Cung {cung_nhue} ({h_nhue}), đi cùng Cửa {cua_nhue} và Thần {than_nhue}."]
        if NGU_HANH_KHAC.get(h_tam) == h_nhue:
            score += 20
            details.append(f"💊 Thiên Tâm Y Dược (Cung {cung_tam} - {h_tam}) KHẮC CHẾ Thiên Nhuế ({h_nhue}) → Gặp đúng thầy đúng thuốc, bệnh tình có cơ hội qua khỏi và hồi phục tốt.")
        elif "Tử" in cua_nhue or "Bạch Hổ" in than_nhue:
            score -= 18
            details.append(f"⚠️ Thiên Nhuế đồng cung {cua_nhue}/{than_nhue} → Bệnh diễn tiến phức tạp, cần theo dõi sát tại bệnh viện chuyên khoa.")
        else:
            details.append(f"💊 Thiên Tâm tại Cung {cung_tam} ({h_tam}) hỗ trợ điều trị ổn định, cần kiên trì theo phác đồ.")

        score = max(15, min(95, score))
        prog = "TỐT — Đáp ứng thuốc, có cơ hội hồi phục" if score >= 60 else ("CẦN THEO DÕI SÁT — Điều trị kiên trì" if score >= 45 else "NGHIÊM TRỌNG — Cần hội chẩn chuyên khoa ngay")
        return {
            "dung_than": f"Thiên Nhuế (Cung {cung_nhue}) vs Thiên Tâm (Cung {cung_tam})",
            "loai": "y_dich",
            "diem": score,
            "tien_luong": prog,
            "chi_tiet": details,
            "loi_khuyen": [f"Ưu tiên khám/điều trị theo hướng Cung Thiên Tâm (Cung {cung_tam})."],
        }

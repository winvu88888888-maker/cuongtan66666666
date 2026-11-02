"""
CAREER ADVISOR AI - Chuyên Gia Công Danh, Sự Nghiệp & Thi Cử (V99.9 Deep Focus)
Phân tích trực tiếp Cung Khai Môn (Công việc/Chức vụ), Sao Thiên Phụ (Thi cử) & Cung Nhật Can.
"""

CUNG_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


class CareerAdvisorAI:
    def __init__(self):
        pass

    def analyze_career_question(self, chart_data, career_topic):
        chart = chart_data if isinstance(chart_data, dict) else {}
        nb = chart.get("nhan_ban", {}) or {}
        tb = chart.get("thien_ban", {}) or {}
        sb = chart.get("than_ban", {}) or {}
        ctb = chart.get("can_thien_ban", {}) or {}
        can_ngay = chart.get("can_ngay", "Giáp")

        cung_khai = 6
        for k, v in nb.items():
            if "Khai" in str(v):
                try:
                    cung_khai = int(k)
                except Exception:
                    pass
                break

        cung_bt = 1
        search_c = "Mậu" if can_ngay == "Giáp" else can_ngay
        for k, v in ctb.items():
            if str(v) == str(search_c):
                try:
                    cung_bt = int(k)
                except Exception:
                    pass
                break

        h_khai = CUNG_HANH.get(cung_khai, "Kim")
        h_bt = CUNG_HANH.get(cung_bt, "Thủy")
        sao_k = str(tb.get(cung_khai, tb.get(str(cung_khai), "Thiên Tâm")))
        than_k = str(sb.get(cung_khai, sb.get(str(cung_khai), "Trực Phù")))

        score = 55
        details = []
        if NGU_HANH_SINH.get(h_khai) == h_bt or h_khai == h_bt:
            score += 20
            details.append(f"💼 Khai Môn tại Cung {cung_khai} ({h_khai}) tương hợp/sinh trợ Bản Mệnh ({h_bt}) → Cơ hội công danh, phỏng vấn, thăng tiến được cấp trên nâng đỡ.")
        elif NGU_HANH_KHAC.get(h_khai) == h_bt:
            score -= 15
            details.append(f"⚠️ Khai Môn tại Cung {cung_khai} ({h_khai}) khắc Bản Mệnh ({h_bt}) → Áp lực công việc/đối thủ cạnh tranh lớn, cần chuẩn bị kỹ hồ sơ.")
        else:
            score += 5
            details.append(f"💼 Khai Môn tại Cung {cung_khai} ({h_khai}) phối Bản Mệnh ({h_bt}) → Cần nỗ lực tự thân mới đạt mục tiêu.")

        details.append(f"🌟 Cung Quan Lộc hội Sao {sao_k} và Thần {than_k}.")
        score = max(15, min(95, score))
        verdict = "THUẬN LỢI THĂNG TIẾN" if score >= 65 else ("CẦN NỖ LỰC VƯỢT THỬ THÁCH" if score >= 45 else "NHIỀU TRỞ NGẠI - Nên củng cố nội lực")
        return {
            "loai": "su_nghiep",
            "dung_than": f"Khai Môn (Cung {cung_khai})",
            "diem": score,
            "danh_gia": verdict,
            "chi_tiet": details,
            "loi_khuyen": ["Tập trung vào chuyên môn và tận dụng quý nhân tại hướng Cung Khai Môn."],
        }

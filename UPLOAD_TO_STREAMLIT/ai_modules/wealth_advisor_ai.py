"""
WEALTH ADVISOR AI - Chuyên Gia Tài Lộc, Đầu Tư & Bất Động Sản (V99.9 Deep Focus)
Phân tích trực tiếp Cung Sinh Môn (Lợi nhuận), Cung Mậu (Vốn) & Cung Nhật Can (Người hỏi).
"""

CUNG_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


class WealthAdvisorAI:
    def __init__(self):
        pass

    def analyze_wealth(self, chart_data, wealth_topic):
        chart = chart_data if isinstance(chart_data, dict) else {}
        nb = chart.get("nhan_ban", {}) or {}
        tb = chart.get("thien_ban", {}) or {}
        sb = chart.get("than_ban", {}) or {}
        ctb = chart.get("can_thien_ban", {}) or {}
        can_ngay = chart.get("can_ngay", "Giáp")

        cung_sinh = 8
        for k, v in nb.items():
            if "Sinh" in str(v):
                try:
                    cung_sinh = int(k)
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

        h_sinh = CUNG_HANH.get(cung_sinh, "Thổ")
        h_bt = CUNG_HANH.get(cung_bt, "Thủy")
        sao_sinh = str(tb.get(cung_sinh, tb.get(str(cung_sinh), "Thiên Nhậm")))
        than_sinh = str(sb.get(cung_sinh, sb.get(str(cung_sinh), "Trực Phù")))

        score = 55
        details = []
        if NGU_HANH_SINH.get(h_sinh) == h_bt:
            score += 22
            details.append(f"💰 Sinh Môn tại Cung {cung_sinh} ({h_sinh}) TƯƠNG SINH cho Bản Mệnh Cung {cung_bt} ({h_bt}) → Lợi nhuận tự tìm đến, đầu tư/mua bán dễ sinh lời.")
        elif h_sinh == h_bt:
            score += 14
            details.append(f"💰 Sinh Môn tại Cung {cung_sinh} TỶ HÒA với Bản Mệnh ({h_bt}) → Tài chính vững vàng, giữ được vốn và có lãi ổn định.")
        elif NGU_HANH_KHAC.get(h_bt) == h_sinh:
            score += 6
            details.append(f"💼 Bản Mệnh ({h_bt}) khắc Sinh Môn ({h_sinh}) tại Cung {cung_sinh} → Phải tự thân vận động, đàm phán sát sao mới thu được lợi nhuận.")
        elif NGU_HANH_SINH.get(h_bt) == h_sinh:
            score -= 8
            details.append(f"⚠️ Bản Mệnh ({h_bt}) sinh xuất cho Sinh Môn ({h_sinh}) → Giai đoạn đầu phải bỏ vốn nhiều, thu hồi vốn chậm.")
        else:
            score -= 16
            details.append(f"⚠️ Sinh Môn tại Cung {cung_sinh} ({h_sinh}) KHẮC Bản Mệnh ({h_bt}) → Rủi ro chôn vốn hoặc giá cả bất lợi, không nên tất tay.")

        details.append(f"🌟 Cung Tài Lộc đi cùng Sao {sao_sinh} và Thần {than_sinh}.")
        score = max(15, min(95, score))
        verdict = "SINH LỜI TỐT - Thuộc Cát Cục" if score >= 65 else ("TRUNG BÌNH - Lãi mỏng / Thu hồi chậm" if score >= 45 else "RỦI RO HAO TÀI - Cần bảo toàn vốn")
        risk = "Thấp" if score >= 65 else ("Trung bình" if score >= 45 else "Cao")
        advice = ["Chia nhỏ dòng vốn, kiểm tra kỹ pháp lý và chọn đúng thời điểm ứng kỳ để chốt lời."]
        return {
            "loai": "tai_chinh",
            "rui_ro": risk,
            "diem": score,
            "danh_gia": verdict,
            "chi_tiet": details,
            "loi_khuyen": advice,
        }

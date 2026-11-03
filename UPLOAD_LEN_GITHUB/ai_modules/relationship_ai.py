"""
RELATIONSHIP AI - Chuyên Gia Phân Tích Tình Cảm, Hôn Nhân & Nhân Duyên (V99.9 Deep Focus)
Phân tích trực tiếp Cung Ất Kỳ (Nữ/Vợ), Cung Canh (Nam/Chồng), Cung Lục Hợp (Tình cảm) & Cung Nhật/Thời Can.
"""

CUNG_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

DOOR_LOVE_MEANING = {
    "Hưu": "Cửa Hưu Môn (Cát) — Tình cảm êm ấm, gắn bó, biết nhường nhịn và hướng về gia đình",
    "Sinh": "Cửa Sinh Môn (Cát) — Tình cảm vẫn đang nảy nở, còn nhiều quan tâm và vun đắp thực tế",
    "Khai": "Cửa Khai Môn (Cát) — Cởi mở, thẳng thắn, sẵn sàng sẻ chia và tháo gỡ hiểu lầm",
    "Đỗ": "Cửa Đỗ Môn (Bình/Thu mình) — Đối phương đang đóng lòng, giữ kín tâm sự, im lặng hoặc giận dỗi ngầm chứ chưa hẳn hết tình",
    "Cảnh": "Cửa Cảnh Môn (Bình) — Bề ngoài nồng nhiệt hoặc hay nói lời nóng nảy nhất thời nhưng trong lòng vẫn để ý đến nhau",
    "Thương": "Cửa Thương Môn (Hung) — Đang có tổn thương lời nói, tự ái hoặc va chạm làm sứt mẻ cảm xúc",
    "Kinh": "Cửa Kinh Môn (Hung) — Tâm lý bất an, lo lắng, nghi kỵ hoặc đang có tranh cãi căng thẳng",
    "Tử": "Cửa Tử Môn (Hung) — Cảm xúc đang bị dồn nén nặng nề, nguội lạnh hoặc bế tắc cần thời gian xoa dịu",
}

DEITY_LOVE_MEANING = {
    "Lục Hợp": "Thần Lục Hợp — Duyên nợ gắn kết sâu nặng, còn tình nghĩa vợ chồng/đôi lứa",
    "Thái Âm": "Thần Thái Âm — Tình cảm thầm lặng, quan tâm tinh tế từ phía sau",
    "Trực Phù": "Thần Trực Phù — Trọng chữ tín, trách nhiệm và tình nghĩa chính thống",
    "Cửu Địa": "Thần Cửu Địa — Tình cảm bền bỉ, trầm ổn lâu dài",
    "Cửu Thiên": "Thần Cửu Thiên — Tính cách thẳng thắn, đôi khi hơi cao ngạo",
    "Đằng Xà": "Thần Đằng Xà — Tâm tư hay suy diễn, đa nghi, dùng dằng khó dứt",
    "Bạch Hổ": "Thần Bạch Hổ — Tính khí nóng nảy, cứng nhắc, dễ gây áp lực trong lời ăn tiếng nói",
    "Huyền Vũ": "Thần Huyền Vũ — Có tâm sự giấu kín, khó nói thật lòng hoặc khoảng cách ngầm",
}


class RelationshipAI:
    def __init__(self):
        pass

    def _find_can_cung(self, chart_data, target_can):
        ctb = chart_data.get("can_thien_ban", {}) or {}
        cdb = chart_data.get("can_dia_ban") or chart_data.get("dia_ban") or chart_data.get("dia_can") or {}
        search_c = "Mậu" if target_can == "Giáp" else target_can
        for k, v in ctb.items():
            if str(v) == str(search_c):
                try:
                    return int(k)
                except Exception:
                    pass
        for k, v in cdb.items():
            if str(v) == str(search_c):
                try:
                    return int(k)
                except Exception:
                    pass
        return 2

    def _find_than_cung(self, chart_data, target_than="Lục Hợp"):
        sb = chart_data.get("than_ban", {}) or {}
        for k, v in sb.items():
            if target_than in str(v):
                try:
                    return int(k)
                except Exception:
                    pass
        return 4

    def analyze_relationship(self, chart_data, topic):
        chart = chart_data if isinstance(chart_data, dict) else {}
        q_low = (topic or "").lower()
        tb = chart.get("thien_ban", {}) or {}
        nb = chart.get("nhan_ban", {}) or {}
        sb = chart.get("than_ban", {}) or {}

        can_ngay = chart.get("can_ngay", "Giáp")
        can_gio = chart.get("can_gio", "Ất")
        cung_bt = self._find_can_cung(chart, can_ngay)
        cung_at = self._find_can_cung(chart, "Ất")    # Nữ / Người vợ
        cung_canh = self._find_can_cung(chart, "Canh") # Nam / Người chồng
        cung_lh = self._find_than_cung(chart, "Lục Hợp")

        # Xác định cung đối phương theo câu hỏi
        if "vợ" in q_low or "bạn gái" in q_low:
            target_cung = cung_at
            partner_label = f"Cung Ất Kỳ (Người Vợ/Nữ - Cung {cung_at})"
            self_cung = cung_canh if "vợ" in q_low else cung_bt
        elif "chồng" in q_low or "bạn trai" in q_low:
            target_cung = cung_canh
            partner_label = f"Cung Canh Kim (Người Chồng/Nam - Cung {cung_canh})"
            self_cung = cung_at if "chồng" in q_low else cung_bt
        else:
            target_cung = cung_lh
            partner_label = f"Cung Lục Hợp (Tình Duyên - Cung {cung_lh})"
            self_cung = cung_bt

        sao_p = str(tb.get(target_cung, tb.get(str(target_cung), "Thiên Cầm")))
        cua_p = str(nb.get(target_cung, nb.get(str(target_cung), "Đỗ Môn")))
        than_p = str(sb.get(target_cung, sb.get(str(target_cung), "Lục Hợp")))

        hanh_self = CUNG_HANH.get(self_cung, "Thổ")
        hanh_part = CUNG_HANH.get(target_cung, "Hỏa")

        score = 55
        details = []

        # 1. Quan hệ Ngũ Hành giữa Cung Bản Thân & Cung Đối Phương
        if NGU_HANH_SINH.get(hanh_part) == hanh_self:
            score += 18
            details.append(f"❤️ Tương quan Cung Mệnh: {partner_label} ({hanh_part}) TƯƠNG SINH cho bạn ({hanh_self}) → Trong lòng đối phương vẫn còn yêu thương, hướng về và lo lắng cho bạn.")
        elif hanh_part == hanh_self:
            score += 12
            details.append(f"💛 Tương quan Cung Mệnh: {partner_label} và bạn đồng hành ({hanh_part}) → Vẫn còn sự đồng cảm, gắn kết duyên nợ vợ chồng.")
        elif NGU_HANH_SINH.get(hanh_self) == hanh_part:
            score += 5
            details.append(f"💝 Tương quan Cung Mệnh: Bạn ({hanh_self}) SINH cho {partner_label} ({hanh_part}) → Bạn đang là người nặng tình, chiều chuộng và chủ động giữ gìn mối quan hệ.")
        elif NGU_HANH_KHAC.get(hanh_part) == hanh_self:
            score -= 14
            details.append(f"⚠️ Tương quan Cung Mệnh: {partner_label} ({hanh_part}) đang KHẮC cung của bạn ({hanh_self}) → Đối phương đang có sự giận dỗi, bất mãn hoặc tạo khoảng cách tâm lý.")
        else:
            score -= 8
            details.append(f"⚠️ Tương quan Cung Mệnh: Bạn ({hanh_self}) KHẮC {partner_label} ({hanh_part}) → Lời nói hoặc thái độ của bạn dễ làm đối phương áp lực, khép lòng.")

        # 2. Phân tích Cửa (Nhân bàn - Thái độ tình cảm hiện tại)
        for k_d, desc_d in DOOR_LOVE_MEANING.items():
            if k_d in cua_p:
                details.append(f"🚪 Thái độ hiện tại ({cua_p}): {desc_d}.")
                if k_d in ("Hưu", "Sinh", "Khai"):
                    score += 12
                elif k_d in ("Thương", "Kinh", "Tử"):
                    score -= 14
                elif k_d == "Đỗ":
                    score -= 4
                break

        # 3. Phân tích Thần (Bát Thần - Ẩn tình trong lòng)
        for k_t, desc_t in DEITY_LOVE_MEANING.items():
            if k_t in than_p:
                details.append(f"🔮 Tâm tư sâu kín ({than_p}): {desc_t}.")
                if k_t in ("Lục Hợp", "Thái Âm", "Trực Phù"):
                    score += 8
                elif k_t in ("Huyền Vũ", "Đằng Xà", "Bạch Hổ"):
                    score -= 8
                break

        score = max(15, min(95, score))
        if score >= 68:
            compat = "TÌNH CẢM SÂU ĐẬM & CHÂN THÀNH — Còn yêu thương gắn bó"
            advice = ["Chủ động sẻ chia, hâm nóng tình cảm để hai bên thêm gắn kết."]
        elif score >= 48:
            compat = "CÒN TÌNH NGHĨA NHƯNG ĐANG CÓ TÂM SỰ / KHOẢNG CÁCH NGẦM"
            advice = ["Đối phương chưa hết tình nhưng đang khép lòng (Cửa Đỗ/Sao Nhuế); cần nhẹ nhàng lắng nghe, tránh tra hỏi gây áp lực."]
        else:
            compat = "TÌNH CẢM ĐANG RẠN NỨT / NGUỘI LẠNH — Nhiều khúc mắc tích tụ"
            advice = ["Cần bình tĩnh tháo gỡ mâu thuẫn gốc rễ, tránh tranh cãi lúc nóng giận."]

        return {
            "loai": "tinh_cam",
            "dung_than": partner_label,
            "diem": score,
            "tuong_hop": compat,
            "chi_tiet": details,
            "loi_khuyen": advice,
        }

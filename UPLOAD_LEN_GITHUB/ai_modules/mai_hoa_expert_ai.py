"""
MAI HOA EXPERT AI - Chuyên Gia Mai Hoa Dịch Số (V99.9 Deep Focus)
Luận giải chính xác Thể - Dụng - Hỗ - Biến từ dữ liệu quẻ Mai Hoa thực tế.
"""

QUAI_MAP_NUM = {1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"}
QUAI_INFO = {
    "Càn": {"hanh": "Kim", "so": 1, "tuong": "Trời, Cứngỏi, Chủ động, Người chồng/cha, Quyền uy"},
    "Đoài": {"hanh": "Kim", "so": 2, "tuong": "Đầm, Lời nói, Trao đổi, Niềm vui hoặc Khẩu thiệt"},
    "Ly": {"hanh": "Hỏa", "so": 3, "tuong": "Lửa, Sáng tỏ, Nóng nảy, Cảm xúc nồng nhiệt, Văn thư"},
    "Chấn": {"hanh": "Mộc", "so": 4, "tuong": "Sấm, Chuyển động nhanh, Khởi phát, Nóng vội"},
    "Tốn": {"hanh": "Mộc", "so": 5, "tuong": "Gió, Mềm mỏng, Thấm dần, Dùng dằng tiến thoái"},
    "Khảm": {"hanh": "Thủy", "so": 6, "tuong": "Nước, Sâu kín, Tâm tư ẩn giấu, Trắc trở hiểm trở"},
    "Cấn": {"hanh": "Thổ", "so": 7, "tuong": "Núi, Ngưng trệ, Giữ khoảng cách, Chờ đợi"},
    "Khôn": {"hanh": "Thổ", "so": 8, "tuong": "Đất, Bao dung, Nhẫn nại, Người vợ/mẹ, Thuận tùng"},
}

NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


class MaiHoaExpertAI:
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper

    def _resolve_quai_name(self, val, default_name="Càn"):
        if isinstance(val, int) and val in QUAI_MAP_NUM:
            return QUAI_MAP_NUM[val]
        if isinstance(val, str):
            for k in QUAI_INFO:
                if k.lower() in val.lower():
                    return k
        return default_name

    def analyze_mai_hoa(self, mai_hoa_data, topic="Chung"):
        data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
        upper_raw = data.get("ten_thuong") or data.get("thuong_quai") or data.get("upper") or "Càn"
        lower_raw = data.get("ten_ha") or data.get("ha_quai") or data.get("lower") or "Khôn"
        upper = self._resolve_quai_name(upper_raw, "Càn")
        lower = self._resolve_quai_name(lower_raw, "Khôn")
        dong_hao = data.get("dong_hao", 1)
        try:
            dong_hao = int(dong_hao[0] if isinstance(dong_hao, list) and dong_hao else dong_hao)
        except Exception:
            dong_hao = 1

        if dong_hao <= 3:
            the_q, dung_q = upper, lower
            the_pos, dung_pos = "Thượng Quái", f"Hạ Quái (Động hào {dong_hao})"
        else:
            the_q, dung_q = lower, upper
            the_pos, dung_pos = "Hạ Quái", f"Thượng Quái (Động hào {dong_hao})"

        the_info = QUAI_INFO.get(the_q, QUAI_INFO["Càn"])
        dung_info = QUAI_INFO.get(dung_q, QUAI_INFO["Khôn"])
        the_h, dung_h = the_info["hanh"], dung_info["hanh"]

        ten_que = data.get("ten_que") or data.get("ten") or f"{upper}/{lower}"
        ten_ho = data.get("ten_ho") or "Hỗ Quái"
        ten_bien = data.get("ten_qua_bien") or data.get("ten_bien") or "Biến Quái"
        if ten_bien in ("Quẻ Biến", "Biến Quái"): ten_bien = f"Quẻ Hỗ {ten_ho}"

        if NGU_HANH_SINH.get(dung_h) == the_h:
            verdict, score = "ĐẠI CÁT", 88
            explain = f"Quẻ {ten_que} → {ten_bien}: Dụng ({dung_q}-{dung_h}) SINH Thể ({the_q}-{the_h}) — Đối phương/sự việc hướng về nâng đỡ bạn, thuận lợi tự nhiên ({ dung_info['tuong'] })."
        elif the_h == dung_h:
            verdict, score = "CÁT", 74
            explain = f"Quẻ {ten_que} → {ten_bien}: Thể ({the_q}-{the_h}) và Dụng ({dung_q}-{dung_h}) TỶ HÒA — Hai bên đồng lòng, tương thông và gắn kết bền vững."
        elif NGU_HANH_KHAC.get(the_h) == dung_h:
            verdict, score = "TIỂU CÁT", 62
            explain = f"Quẻ {ten_que} → {ten_bien}: Thể ({the_q}-{the_h}) KHẮC Dụng ({dung_q}-{dung_h}) — Bạn nắm quyền chủ động kiểm soát được tình thế nhưng cần kiên trì nỗ lực."
        elif NGU_HANH_SINH.get(the_h) == dung_h:
            verdict, score = "BÌNH / HAO TỔN", 46
            explain = f"Quẻ {ten_que} → {ten_bien}: Thể ({the_q}-{the_h}) SINH Dụng ({dung_q}-{dung_h}) — Bạn đang phải tiêu hao nhiều tâm sức, tình cảm hoặc tiền bạc cho đối phương/sự việc ({dung_info['tuong']})."
        else:
            verdict, score = "HUNG", 28
            explain = f"Quẻ {ten_que} → {ten_bien}: Dụng ({dung_q}-{dung_h}) KHẮC Thể ({the_q}-{the_h}) — Đối phương hoặc hoàn cảnh bên ngoài đang gây sức ép, cản trở hoặc lạnh nhạt ({dung_info['tuong']})."

        the_dung = {
            "the": {"ten": the_q, "hanh": the_h, "vi_tri": the_pos, "tuong": the_info["tuong"], "so": the_info["so"]},
            "dung": {"ten": dung_q, "hanh": dung_h, "vi_tri": dung_pos, "tuong": dung_info["tuong"], "so": dung_info["so"]},
            "dong_hao": dong_hao,
        }
        relationship = {
            "loai": verdict,
            "verdict": verdict,
            "score": score,
            "giai_thich": explain,
            "chi_tiet": f"Diễn biến trung gian ({ten_ho}) → Kết cục ({ten_bien})."
        }
        return {
            "the_dung": the_dung,
            "quan_he": relationship,
            "ho_quai": {"ten": ten_ho, "y_nghia": f"Quẻ Hỗ {ten_ho} phản ánh nội tình diễn biến ở giai đoạn giữa"},
            "bien_quai": {"ten": ten_bien, "ket_qua": f"Quẻ Biến {ten_bien} phản ánh kết cục sau cùng", "score": score},
            "thoi_gian": {"so_ngay": dung_info["so"], "mo_ta": f"Ứng kỳ theo số Tiên Thiên quẻ {dung_q} ({dung_info['so']} ngày/tuần)"},
            "so_luong": {"so_chinh": the_info["so"] + dung_info["so"], "mo_ta": f"Con số dịch lý: {the_info['so'] + dung_info['so']}"},
            "ket_luan": {"diem": score, "verdict": verdict, "tom_tat": explain, "loi_khuyen": relationship["chi_tiet"], "chi_tiet": [explain]},
        }

    def get_detailed_interpretation(self, mai_hoa_data, topic="Chung"):
        res = self.analyze_mai_hoa(mai_hoa_data, topic)
        return res["quan_he"]["giai_thich"]


_expert = None
def get_mai_hoa_expert(gemini_helper=None):
    global _expert
    if _expert is None:
        _expert = MaiHoaExpertAI(gemini_helper)
    return _expert

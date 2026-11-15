# -*- coding: utf-8 -*-
"""
CHINESE MASTER MICRO-SIGN & DIRECTED CAUSAL GRAPH ENGINE (V130.0)
=================================================================
Đối chuẩn toàn diện theo các nền tảng phân tích quẻ chuyên sâu hàng đầu Trung Quốc:
1. Nguyên Hanh Lợi Trinh (元亨利贞网 china95.net) — Lục Hào 4 Tầng Tác Động Tuyến Lộ Đồ, Quái Thân, Thế Thân, 12 Thần Sát, Tam Hình/Lục Hại/Lục Phá.
2. Vấn Chân Lục Hào & Vấn Chân Kỳ Môn (问真六爻 / 问真奇门 iwzwh.com) — Khôi phục Can thứ 9 Ký Cung Khôn 2 / Thiên Nhuế Cầm, Ám Can (暗干) 9 Cung, Tứ Hại (Không · Mộ · Kích Hình · Môn Bức), 12 Trường Sinh Lạc Cung, Phiên Cung 4 Trạm Nhân Quả (Quá khứ -> Hiện tại -> Chuyển tiếp -> Kết cục).
3. Mai Hoa Dịch Số Vạn Vật Loại Tượng — Tách Hạ Hỗ (2-3-4) & Thượng Hỗ (3-4-5), Chuỗi Mũi Tên 4 Chặng + Chu Dịch 384 Hào Từ.

Mục tiêu: KHÔNG BỎ SÓT BẤT KỲ DẤU HIỆU NHỎ NHẤT NÀO CỦA QUẺ và hiển thị trực quan
SƠ ĐỒ MŨI TÊN NHÂN QUẢ ([Yếu tố A] ──[Cơ chế tác động]──► [Yếu tố B] ══► [Kết quả thực tế chi tiết]).
"""

from typing import Any, Dict, List, Optional, Tuple
import html as _html

CHI_12 = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

CHI_ELEMENT = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
}
CAN_ELEMENT = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy",
}
SINH_EL = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
KHAC_EL = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

LUC_XUNG = {
    "Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu",
    "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão",
    "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị",
}
LUC_HOP = {
    "Tý": ("Sửu", "Thổ"), "Sửu": ("Tý", "Thổ"),
    "Dần": ("Hợi", "Mộc"), "Hợi": ("Dần", "Mộc"),
    "Mão": ("Tuất", "Hỏa"), "Tuất": ("Mão", "Hỏa"),
    "Thìn": ("Dậu", "Kim"), "Dậu": ("Thìn", "Kim"),
    "Tị": ("Thân", "Thủy"), "Thân": ("Tị", "Thủy"),
    "Ngọ": ("Mùi", "Hỏa/Thổ"), "Mùi": ("Ngọ", "Hỏa/Thổ"),
}
LUC_HAI = {
    "Tý": "Mùi", "Mùi": "Tý",
    "Sửu": "Ngọ", "Ngọ": "Sửu",
    "Dần": "Tị", "Tị": "Dần",
    "Mão": "Thìn", "Thìn": "Mão",
    "Thân": "Hợi", "Hợi": "Thân",
    "Dậu": "Tuất", "Tuất": "Dậu",
}
LUC_PHA = {
    "Tý": "Dậu", "Dậu": "Tý",
    "Ngọ": "Mão", "Mão": "Ngọ",
    "Thìn": "Sửu", "Sửu": "Thìn",
    "Tuất": "Mùi", "Mùi": "Tuất",
    "Dần": "Hợi", "Hợi": "Dần",
    "Tị": "Thân", "Thân": "Tị",
}
TAM_HINH_PAIR_DESC = {
    ("Tý", "Mão"): "Vô Lễ Chi Hình (Tý–Mão Hình: nóng vội, thiếu khéo léo dễ gây mất lòng hoặc vướng quy định)",
    ("Mão", "Tý"): "Vô Lễ Chi Hình (Mão–Tý Hình: nóng vội, thiếu khéo léo dễ gây mất lòng hoặc vướng quy định)",
    ("Dần", "Tị"): "Ỷ Thế Chi Hình (Dần–Tị Hình: va chạm quyền lực, thủ tục hoặc đi lại phát sinh ma sát)",
    ("Tị", "Dần"): "Ỷ Thế Chi Hình (Tị–Dần Hình: va chạm quyền lực, thủ tục hoặc đi lại phát sinh ma sát)",
    ("Tị", "Thân"): "Ỷ Thế Chi Hình (Tị–Thân Hình vừa Hợp vừa Hình: ngoài mặt hòa hợp nhưng bên trong giằng co lợi ích)",
    ("Thân", "Tị"): "Ỷ Thế Chi Hình (Thân–Tị Hình vừa Hợp vừa Hình: ngoài mặt hòa hợp nhưng bên trong giằng co lợi ích)",
    ("Dần", "Thân"): "Ỷ Thế Xung Hình (Dần–Thân vừa Xung vừa Hình: biến động mạnh, va chạm trực diện hoặc dịch chuyển gấp)",
    ("Thân", "Dần"): "Ỷ Thế Xung Hình (Thân–Dần vừa Xung vừa Hình: biến động mạnh, va chạm trực diện hoặc dịch chuyển gấp)",
    ("Sửu", "Tuất"): "Trì Thế Chi Hình (Sửu–Tuất Hình: nội bộ dây dưa, giấy tờ/tài chính bị giữ lại xét duyệt kỹ)",
    ("Tuất", "Sửu"): "Trì Thế Chi Hình (Tuất–Sửu Hình: nội bộ dây dưa, giấy tờ/tài chính bị giữ lại xét duyệt kỹ)",
    ("Tuất", "Mùi"): "Trì Thế Chi Hình (Tuất–Mùi Hình: giằng co trách nhiệm, ơn nghĩa cũ thành sức ép tâm lý)",
    ("Mùi", "Tuất"): "Trì Thế Chi Hình (Mùi–Tuất Hình: giằng co trách nhiệm, ơn nghĩa cũ thành sức ép tâm lý)",
    ("Sửu", "Mùi"): "Xung Kiêm Hình (Sửu–Mùi vừa Xung vừa Hình: kho tàng bị chấn động, thay đổi kế hoạch đột xuất)",
    ("Mùi", "Sửu"): "Xung Kiêm Hình (Mùi–Sửu vừa Xung vừa Hình: kho tàng bị chấn động, thay đổi kế hoạch đột xuất)",
    ("Thìn", "Thìn"): "Tự Hình (Thìn–Thìn Tự Hình: tự mình lo nghĩ luẩn quẩn, cố chấp quan điểm riêng)",
    ("Ngọ", "Ngọ"): "Tự Hình (Ngọ–Ngọ Tự Hình: tâm trạng nóng ruột, tự tạo áp lực tinh thần)",
    ("Dậu", "Dậu"): "Tự Hình (Dậu–Dậu Tự Hình: cầu toàn quá mức, dễ bắt bẻ chi tiết nhỏ)",
    ("Hợi", "Hợi"): "Tự Hình (Hợi–Hợi Tự Hình: suy tư nhiều hướng, do dự nội tâm)",
}

TAM_HOP_CUC = [
    ({"Thân", "Tý", "Thìn"}, "Thủy", "Tý"),
    ({"Dần", "Ngọ", "Tuất"}, "Hỏa", "Ngọ"),
    ({"Hợi", "Mão", "Mùi"}, "Mộc", "Mão"),
    ({"Tị", "Dậu", "Sửu"}, "Kim", "Dậu"),
]

TS_STAGES = [
    "Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan",
    "Đế Vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"
]
TS_START_BY_EL = {"Mộc": "Hợi", "Hỏa": "Dần", "Thổ": "Thân", "Kim": "Tị", "Thủy": "Thân"}

HAO_VI_MEANING = {
    1: ("Hào Sơ (Chân/Nền móng/Khởi đầu)", "Gốc rễ ban đầu, tâm tư thầm kín, bước chân đầu tiên, nền nhà/làng xóm"),
    2: ("Hào Nhị (Nội gia/Nhà ở/Thân cận)", "Không gian trong nhà, phòng bếp/phòng khách, quản lý trực tiếp, nội tình cốt lõi"),
    3: ("Hào Tam (Cửa ngõ/Ranh giới Nội-Ngoại)", "Cửa ra vào, giường ngủ, bước chuyển giao từ nội bộ ra bên ngoài, dễ dao động"),
    4: ("Hào Tứ (Cận thần/Ngoài cổng/Phụ tá)", "Cổng ngoài, cơ quan cấp gần, phương tiện di chuyển ngoài phố, bước sang môi trường mới"),
    5: ("Hào Ngũ (Quân vị/Trung tâm quyết định)", "Người đứng đầu, trục chính đại lộ, cấp thẩm quyền cao nhất, trung tâm thành bại"),
    6: ("Hào Thượng (Đỉnh ngọn/Viễn phương/Kết thúc)", "Nơi xa xôi, tầng mái/trên cao, tông miếu tâm linh, giai đoạn hạ màn cuối cùng"),
}

CUNG_META_9 = {
    1: ("Khảm", "Chính Bắc", "Thủy", ["Tý"]),
    2: ("Khôn", "Tây Nam", "Thổ", ["Mùi", "Thân"]),
    3: ("Chấn", "Chính Đông", "Mộc", ["Mão"]),
    4: ("Tốn", "Đông Nam", "Mộc", ["Thìn", "Tị"]),
    5: ("Trung Cung", "Trung Tâm (Ký Khôn 2)", "Thổ", ["Mùi", "Thân"]),
    6: ("Càn", "Tây Bắc", "Kim", ["Tuất", "Hợi"]),
    7: ("Đoài", "Chính Tây", "Kim", ["Dậu"]),
    8: ("Cấn", "Đông Bắc", "Thổ", ["Sửu", "Dần"]),
    9: ("Ly", "Chính Nam", "Hỏa", ["Ngọ"]),
}

STAR_EL = {
    "Thiên Bồng": "Thủy", "Thiên Nhuế": "Thổ", "Thiên Nhuế/Cầm": "Thổ", "Thiên Cầm": "Thổ",
    "Thiên Xung": "Mộc", "Thiên Phụ": "Mộc", "Thiên Anh": "Hỏa",
    "Thiên Nhậm": "Thổ", "Thiên Trụ": "Kim", "Thiên Tâm": "Kim",
}
DOOR_EL = {
    "Hưu": "Thủy", "Sinh": "Thổ", "Thương": "Mộc", "Đỗ": "Mộc",
    "Cảnh": "Hỏa", "Tử": "Thổ", "Kinh": "Kim", "Khai": "Kim",
}
TRIGRAM_META_8 = {
    "Càn": ((1, 1, 1), 1, 6, "Kim", "Trời, Người cha, Lãnh đạo, Kim loại quý, Tròn đầy"),
    "Đoài": ((1, 1, 0), 2, 7, "Kim", "Đầm hồ, Thiếu nữ, Lời nói, Âm nhạc, Vui vẻ, Kim khí nhỏ"),
    "Ly": ((1, 0, 1), 3, 9, "Hỏa", "Lửa, Ánh sáng, Văn thư, Mắt/Tim, Danh tiếng, Thiết bị điện"),
    "Chấn": ((1, 0, 0), 4, 3, "Mộc", "Sấm sét, Trưởng nam, Xe cộ, Chuyển động nhanh, Âm thanh vang"),
    "Tốn": ((0, 1, 1), 5, 4, "Mộc", "Gió, Trưởng nữ, Giao thương, Dây dẫn/Mạng lưới, Tin tức"),
    "Khảm": ((0, 1, 0), 6, 1, "Thủy", "Nước, Trung nam, Trí tuệ sâu, Hiểm trở, Dòng tiền ngầm"),
    "Cấn": ((0, 0, 1), 7, 8, "Thổ", "Núi, Thiếu nam, Ngôi nhà/Tường cổng, Dừng lại giữ vững"),
    "Khôn": ((0, 0, 0), 8, 2, "Thổ", "Đất, Người mẹ, Bụng/Kho chứa, Số đông, Nhu thuận"),
}
BIN_TO_TRIGRAM_8 = {v[0]: k for k, v in TRIGRAM_META_8.items()}

STEM_MEANING_SHORT = {
    "Giáp": "Nguyên thủ, Trực Phù tôn quý, khởi đầu lớn",
    "Ất": "Nhật Kỳ (Thuốc thang, mưu kế mềm dẻo, người vợ/phụ tá khéo léo)",
    "Bính": "Nguyệt Kỳ (Quyền uy sáng rõ, nhiệt huyết nhưng dễ nóng vội)",
    "Đinh": "Tinh Kỳ (Tin vui, giấy tờ chứng từ, tia sáng hy vọng mở lối)",
    "Mậu": "Thanh Long Vốn liếng (Tiền mặt, nhà đất, tài sản gốc)",
    "Kỷ": "Minh Đường Ẩn Tư (Mưu tính riêng, việc lặt vặt hoặc dục vọng ngầm)",
    "Canh": "Bạch Hổ Cản Trở (Đối thủ, nút thắt cứng, chồng/cấp trên nghiêm khắc)",
    "Tân": "Chu Tước Lỗi Sai (Sai sót chi tiết, sửa chữa đổi mới, vi phạm nhỏ)",
    "Nhâm": "Thiên Lao Dịch Chuyển (Biến động lưu thông, đi xa, rắc rối dây chuyền)",
    "Quý": "Thiên Võng Hệ Lụy (Vướng lưới thủ tục/tình cảm ngầm, việc khuất tất)",
}


def _norm_chi(c: str) -> str:
    s = str(c or "").strip().replace("Tỵ", "Tị")
    return s if s in CHI_12 else ""


def get_12_truong_sinh_el(el: str, chi: str) -> str:
    c = _norm_chi(chi)
    st = TS_START_BY_EL.get(str(el or "").strip())
    if not c or not st:
        return "Bình"
    idx = (CHI_12.index(c) - CHI_12.index(st)) % 12
    return TS_STAGES[idx]


def get_qimen_stem_palace_stage(stem: str, palace: int) -> str:
    """
    V130.0: Tính 12 Trường Sinh Lạc Cung của Thiên Can trên Cửu Cung Kỳ Môn (chuẩn Vấn Chân Kỳ Môn).
    """
    s = str(stem or "").strip()
    p = 2 if int(palace or 2) == 5 else int(palace or 2)
    branches = CUNG_META_9.get(p, ("Khôn", "Tây Nam", "Thổ", ["Mùi", "Thân"]))[3]
    start_map_yang = {"Giáp": "Hợi", "Bính": "Dần", "Mậu": "Dần", "Canh": "Tị", "Nhâm": "Thân"}
    start_map_yin = {"Ất": "Ngọ", "Đinh": "Dậu", "Kỷ": "Dậu", "Tân": "Tý", "Quý": "Mão"}
    stages = []
    for br in branches:
        if s in start_map_yang:
            idx = (CHI_12.index(br) - CHI_12.index(start_map_yang[s])) % 12
            stages.append(TS_STAGES[idx])
        elif s in start_map_yin:
            idx = (CHI_12.index(start_map_yin[s]) - CHI_12.index(br)) % 12
            stages.append(TS_STAGES[idx])
    return "/".join(stages) if stages else "Bình"


def compute_liuyao_shensha_and_bodies(
    can_ngay: str,
    chi_ngay: str,
    chi_thang: str,
    ban_lines: List[int],
    the_pos: int,
    p_element: str,
    details_ban: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    V130.0: Tính chuẩn 100% Quái Thân (卦身), Thế Thân (世身) và 12 Thần Sát Thực Chiến (chuẩn Nguyên Hanh Lợi Trinh & Vấn Chân Lục Hào).
    """
    cn = str(can_ngay or "Giáp").strip()
    chn = _norm_chi(chi_ngay) or "Tý"
    chm = _norm_chi(chi_thang) or "Dần"
    tp = int(the_pos) if 1 <= int(the_pos or 3) <= 6 else 3
    lines6 = list(ban_lines) if isinstance(ban_lines, (list, tuple)) and len(ban_lines) == 6 else [1, 1, 1, 1, 1, 1]

    # 1. Quái Thân (卦身): "Dương Thế tắc tòng Tý nguyệt khởi, Âm Thế hoàn tòng Ngọ nguyệt sinh"
    the_is_yang = (lines6[tp - 1] == 1)
    quai_than_chi = CHI_12[(0 if the_is_yang else 6) + tp - 1]
    quai_than_el = CHI_ELEMENT.get(quai_than_chi, "Thổ")

    def _lt_of(el_x: str, p_el: str) -> str:
        if el_x == p_el:
            return "Huynh Đệ"
        if SINH_EL.get(p_el) == el_x:
            return "Tử Tôn"
        if KHAC_EL.get(p_el) == el_x:
            return "Thê Tài"
        if KHAC_EL.get(el_x) == p_el:
            return "Quan Quỷ"
        if SINH_EL.get(el_x) == p_el:
            return "Phụ Mẫu"
        return "Huynh Đệ"

    quai_than_lt = _lt_of(quai_than_el, p_element or "Kim")
    qt_appear_haos = []
    the_chi = "Tý"
    if isinstance(details_ban, list) and len(details_ban) == 6:
        if 1 <= tp <= 6:
            the_chi = _norm_chi(details_ban[tp - 1].get("chi")) or "Tý"
        for d in details_ban:
            if _norm_chi(d.get("chi")) == quai_than_chi:
                qt_appear_haos.append(int(d.get("hao", 0)))

    if qt_appear_haos:
        qt_status = f"Hiện rõ tại Hào {', '.join(map(str, qt_appear_haos))} ({quai_than_chi}-{quai_than_el} · {quai_than_lt})"
        qt_meaning = "Sự thể hữu căn — Sự việc đã thành hình cụ thể, có đầu mối thực tế rõ ràng ngoài đời."
    else:
        qt_status = f"Bất Hiện / Ẩn Phục ({quai_than_chi}-{quai_than_el} · {quai_than_lt} chưa lên quẻ)"
        qt_meaning = "Sự vô đầu tự — Sự việc còn trong giai đoạn thai nghén, chưa lộ hết hình hài hoặc đối phương đang giữ kín thông tin."

    # 2. Thế Thân (世身): "Tý Ngọ trì Thế thân cư Sơ, Sửu Mùi nhị, Dần Thân tam, Mão Dậu tứ, Thìn Tuất ngũ, Tị Hợi lục"
    the_than_map = {
        "Tý": 1, "Ngọ": 1, "Sửu": 2, "Mùi": 2, "Dần": 3, "Thân": 3,
        "Mão": 4, "Dậu": 4, "Thìn": 5, "Tuất": 5, "Tị": 6, "Hợi": 6,
    }
    the_than_hao = the_than_map.get(the_chi, 3)
    the_than_lt = ""
    the_than_cc = ""
    if isinstance(details_ban, list) and len(details_ban) >= the_than_hao:
        _tt_d = details_ban[the_than_hao - 1]
        the_than_lt = str(_tt_d.get("luc_than", ""))
        the_than_cc = str(_tt_d.get("can_chi_full") or _tt_d.get("can_chi", ""))

    # 3. 12 Thần Sát Thực Chiến (十二神煞)
    quy_nhan_map = {
        "Giáp": ["Sửu", "Mùi"], "Mậu": ["Sửu", "Mùi"], "Canh": ["Sửu", "Mùi"],
        "Ất": ["Tý", "Thân"], "Kỷ": ["Tý", "Thân"],
        "Bính": ["Hợi", "Dậu"], "Đinh": ["Hợi", "Dậu"],
        "Nhâm": ["Mão", "Tị"], "Quý": ["Mão", "Tị"],
        "Tân": ["Ngọ", "Dần"],
    }
    loc_than_map = {
        "Giáp": "Dần", "Ất": "Mão", "Bính": "Tị", "Đinh": "Ngọ", "Mậu": "Tị",
        "Kỷ": "Ngọ", "Canh": "Thân", "Tân": "Dậu", "Nhâm": "Hợi", "Quý": "Tý",
    }
    duong_nhan_map = {
        "Giáp": "Mão", "Ất": "Dần", "Bính": "Ngọ", "Đinh": "Tị", "Mậu": "Ngọ",
        "Kỷ": "Tị", "Canh": "Dậu", "Tân": "Thân", "Nhâm": "Tý", "Quý": "Hợi",
    }
    van_xuong_map = {
        "Giáp": "Tị", "Ất": "Ngọ", "Bính": "Thân", "Đinh": "Dậu", "Mậu": "Thân",
        "Kỷ": "Dậu", "Canh": "Hợi", "Tân": "Tý", "Nhâm": "Dần", "Quý": "Mão",
    }

    def _tam_hop_group(ch: str) -> str:
        if ch in ("Thân", "Tý", "Thìn"):
            return "THUY"
        if ch in ("Dần", "Ngọ", "Tuất"):
            return "HOA"
        if ch in ("Tị", "Dậu", "Sửu"):
            return "KIM"
        return "MOC"

    grp = _tam_hop_group(chn)
    dich_ma = {"THUY": "Dần", "HOA": "Thân", "KIM": "Hợi", "MOC": "Tị"}[grp]
    dao_hoa = {"THUY": "Dậu", "HOA": "Mão", "KIM": "Ngọ", "MOC": "Tý"}[grp]
    hoa_cai = {"THUY": "Thìn", "HOA": "Tuất", "KIM": "Sửu", "MOC": "Mùi"}[grp]
    kiep_sat = {"THUY": "Tị", "HOA": "Hợi", "KIM": "Dần", "MOC": "Thân"}[grp]
    tai_sat = {"THUY": "Ngọ", "HOA": "Tý", "KIM": "Mão", "MOC": "Dậu"}[grp]
    muu_tinh = {"THUY": "Tuất", "HOA": "Thìn", "KIM": "Mùi", "MOC": "Sửu"}[grp]

    thien_y = CHI_12[(CHI_12.index(chm) - 1) % 12] if chm in CHI_12 else "Sửu"
    if chm in ("Dần", "Mão", "Thìn"):
        thien_hy = "Tuất"
    elif chm in ("Tị", "Ngọ", "Mùi"):
        thien_hy = "Sửu"
    elif chm in ("Thân", "Dậu", "Tuất"):
        thien_hy = "Thìn"
    else:
        thien_hy = "Mùi"

    shensha_dict = {
        "Thiên Ất Quý Nhân": quy_nhan_map.get(cn, ["Sửu", "Mùi"]),
        "Lộc Thần": [loc_than_map.get(cn, "Dần")],
        "Dương Nhẫn": [duong_nhan_map.get(cn, "Mão")],
        "Văn Xương": [van_xuong_map.get(cn, "Tị")],
        "Dịch Mã": [dich_ma],
        "Đào Hoa": [dao_hoa],
        "Hoa Cái": [hoa_cai],
        "Kiếp Sát": [kiep_sat],
        "Tai Sát": [tai_sat],
        "Mưu Tinh": [muu_tinh],
        "Thiên Y": [thien_y],
        "Thiên Hỷ": [thien_hy],
    }

    shensha_meaning = {
        "Thiên Ất Quý Nhân": "Quý nhân cấp cao nâng đỡ,逢凶化吉 (gặp hung hóa cát)",
        "Lộc Thần": "Tài lộc chính ngạch, lương bổng, nguồn thu thực chất",
        "Dương Nhẫn": "Cương quyết mạnh mẽ nhưng dễ căng thẳng, hao tán hoặc va chạm",
        "Văn Xương": "Giấy tờ, học hành, hợp đồng, trí tuệ sáng suốt",
        "Dịch Mã": "Chuyển động nhanh, đi xa, thay đổi vị trí/tiến độ tốc hành",
        "Đào Hoa": "Nhân duyên, cảm xúc, giao tiếp cuốn hút, nghệ thuật/âm nhạc",
        "Hoa Cái": "Nội tâm sâu sắc, tâm linh tôn giáo, độc lập hoặc khép kín",
        "Kiếp Sát": "Cản trở bất ngờ, hao hụt hoặc bị người khác tranh phần",
        "Tai Sát": "Cảnh báo va chạm, sức khỏe hoặc rủi ro khách quan cần phòng ngừa",
        "Mưu Tinh": "Mưu lược sắc bén, tính toán kế hoạch bài bản",
        "Thiên Y": "Thầy giỏi thuốc hay, cơ chế tự hồi phục sức khỏe & sửa lỗi",
        "Thiên Hỷ": "Tin mừng, hỷ sự, bầu không khí vui vẻ hòa thuận",
    }

    def _stars_for_branch(br: str) -> List[str]:
        b = _norm_chi(br)
        out = []
        for s_name, b_list in shensha_dict.items():
            if b in b_list:
                out.append(s_name)
        if b == quai_than_chi:
            out.append("Quái Thân")
        return out

    return {
        "quai_than": {
            "chi": quai_than_chi,
            "ngu_hanh": quai_than_el,
            "luc_than": quai_than_lt,
            "appear_haos": qt_appear_haos,
            "is_present": bool(qt_appear_haos),
            "status_str": qt_status,
            "meaning": qt_meaning,
        },
        "the_than": {
            "hao": the_than_hao,
            "the_chi": the_chi,
            "luc_than": the_than_lt,
            "can_chi": the_than_cc,
            "status_str": f"Hào {the_than_hao} ({the_than_lt} {the_than_cc})".strip(),
            "meaning": f"Trọng tâm tâm trí & hành thân của người hỏi đang đặt trực tiếp vào {the_than_lt or f'Hào {the_than_hao}'}.",
        },
        "shensha_dict": shensha_dict,
        "shensha_meaning": shensha_meaning,
        "stars_for_branch": _stars_for_branch,
    }


def _describe_branch_micro_relations(src_lbl: str, src_chi: str, dst_lbl: str, dst_chi: str, is_high_tier_src: bool = False) -> List[Tuple[str, str, int, str]]:
    """
    Kiểm tra ĐẦY ĐỦ 100% quan hệ vi mô giữa 2 Địa Chi (Sinh, Khắc, Trị, Tỷ, Lục Xung, Lục Hợp, Tam Hình, Lục Hại, Lục Phá, Mộ, Tuyệt).
    Trả về danh sách: (nhãn_mũi_tên, màu_mũi_tên, điểm_tác_động, kết_quả_thực_tế_vn)
    """
    c1, c2 = _norm_chi(src_chi), _norm_chi(dst_chi)
    if not c1 or not c2:
        return []
    el1, el2 = CHI_ELEMENT[c1], CHI_ELEMENT[c2]
    edges: List[Tuple[str, str, int, str]] = []

    # 1. Lâm Trị (Đồng Chi)
    if c1 == c2 and is_high_tier_src:
        edges.append((
            f"Lâm Trị ({c1}={c2})",
            "#22c55e",
            28,
            f"{src_lbl} ({c1}) trực tiếp lâm trị {dst_lbl} ({c2}) — năng lượng cực vượng, nắm quyền chủ động tuyệt đối và không sợ Tuần Không hay Hưu Tù.",
        ))
    elif (c1, c2) in TAM_HINH_PAIR_DESC and c1 == c2 and not is_high_tier_src:
        edges.append((
            f"Tự Hình ({c1}–{c2})",
            "#f97316",
            -10,
            f"{src_lbl} ({c1}) gây {TAM_HINH_PAIR_DESC[(c1, c2)]} lên {dst_lbl}.",
        ))

    # 2. Lục Xung & Lục Hợp
    if LUC_XUNG.get(c1) == c2:
        edges.append((
            f"Lục Xung ({c1}⚡{c2})",
            "#f59e0b",
            -18,
            f"{src_lbl} ({c1}) xung thẳng vào {dst_lbl} ({c2}) — nếu {dst_lbl} vượng là Xung Khởi/Ám Động (thúc đẩy nhanh tức thì), nếu suy yếu là Xung Phá/Tán (rung lắc, thay đổi đột ngột).",
        ))
    elif c1 in LUC_HOP and LUC_HOP[c1][0] == c2:
        edges.append((
            f"Lục Hợp ({c1}🔗{c2})",
            "#38bdf8",
            16,
            f"{src_lbl} ({c1}) tương hợp chặt với {dst_lbl} ({c2}) — nếu hào tĩnh là Hợp Khởi (kết nối quý nhân/đối tác), nếu hào đang động là Hợp Trói (bị níu giữ, trì hoãn thêm thời gian chờ Xung mở).",
        ))

    # 3. Ngũ Hành Sinh / Khắc / Tỷ Hòa
    if SINH_EL.get(el1) == el2:
        edges.append((
            f"Tương Sinh ({el1}➔{el2})",
            "#22c55e",
            20,
            f"{src_lbl} ({c1}-{el1}) tiếp khí tương sinh trực tiếp cho {dst_lbl} ({c2}-{el2}) — nguồn lực bồi đắp liên tục, việc có người/hoàn cảnh hậu thuẫn thực chất.",
        ))
    elif KHAC_EL.get(el1) == el2:
        edges.append((
            f"Tương Khắc ({el1}⚔{el2})",
            "#ef4444",
            -20,
            f"{src_lbl} ({c1}-{el1}) chế khắc trực diện {dst_lbl} ({c2}-{el2}) — gây áp lực hao tổn, lực cản thực tế hoặc kiểm soát chặt chẽ.",
        ))
    elif el1 == el2 and c1 != c2:
        edges.append((
            f"Tỷ Trợ ({el1}={el2})",
            "#4ade80",
            12,
            f"{src_lbl} ({c1}-{el1}) đồng hành trợ lực cho {dst_lbl} ({c2}-{el2}) — tăng thêm sức bền và đồng minh cùng phe.",
        ))

    # 4. Tam Hình / Lục Hại / Lục Phá (Dấu hiệu vi mô hay bị bỏ sót nhất!)
    if (c1, c2) in TAM_HINH_PAIR_DESC and c1 != c2:
        edges.append((
            f"Tương Hình ({c1}⚠{c2})",
            "#f97316",
            -12,
            f"{src_lbl} ({c1}) tác động {TAM_HINH_PAIR_DESC[(c1, c2)]} tới {dst_lbl} ({c2}).",
        ))
    if LUC_HAI.get(c1) == c2:
        edges.append((
            f"Lục Hại ({c1}🗡{c2})",
            "#fb7185",
            -10,
            f"{src_lbl} ({c1}) phạm Xuyên Tâm Lục Hại với {dst_lbl} ({c2}) — báo hiệu sự hiểu lầm ngầm, có yếu tố chọc ngang sau lưng hoặc lệch pha cảm xúc.",
        ))
    if LUC_PHA.get(c1) == c2 and LUC_XUNG.get(c1) != c2 and (c1, c2) not in TAM_HINH_PAIR_DESC:
        edges.append((
            f"Tương Phá ({c1}▫{c2})",
            "#fbbf24",
            -7,
            f"{src_lbl} ({c1}) tương phá nhẹ với {dst_lbl} ({c2}) — xuất hiện tì vết nhỏ, chậm trễ vặt hoặc giấy tờ/kế hoạch phải chỉnh sửa chi tiết.",
        ))

    # 5. Nhập Mộ / Tuyệt tại Nguồn (khi xét Nhật/Nguyệt hoặc Biến Hào thu Mộ hào gốc)
    if is_high_tier_src and c1 != c2:
        ts_dst_at_src = get_12_truong_sinh_el(el2, c1)
        if ts_dst_at_src == "Mộ":
            edges.append((
                f"Thu Nhập Mộ ({el2}➔Mộ {c1})",
                "#a855f7",
                -12,
                f"{dst_lbl} ({c2}-{el2}) lâm Mộ khố tại {src_lbl} ({c1}) — đối tượng/sự việc đang thu mình cất giấu, bị kìm giữ trong phòng/kho hoặc tâm trí bế tắc chờ ngày Xung Mộ ({LUC_XUNG.get(c1, '')}).",
            ))
        elif ts_dst_at_src == "Tuyệt":
            edges.append((
                f"Lâm Tuyệt Địa ({el2}➔Tuyệt {c1})",
                "#ef4444",
                -15,
                f"{dst_lbl} ({c2}-{el2}) rơi vào Tuyệt địa tại {src_lbl} ({c1}) — khí lực tạm thời đứt quãng, cần Nguyên Thần sinh cứu ('Tuyệt xứ phùng sinh').",
            ))
    return edges


def _render_svg_arrow(label: str, color: str = "#38bdf8") -> str:
    safe_lbl = _html.escape(str(label or ""))
    return (
        f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2px 3px;min-width:88px;flex:0 0 auto;">'
        f'<span style="font-size:0.73em;font-weight:800;color:{color};background:rgba(15,23,42,0.94);border:1px solid {color};border-radius:999px;padding:1px 7px;white-space:nowrap;margin-bottom:2px;">{safe_lbl}</span>'
        f'<svg width="82" height="16" viewBox="0 0 82 16" style="overflow:visible;">'
        f'<line x1="2" y1="8" x2="69" y2="8" stroke="{color}" stroke-width="2.4"/>'
        f'<polygon points="68,3 80,8 68,13" fill="{color}"/>'
        f'</svg></div>'
    )


def _render_node_box(tier_badge: str, title: str, subtitle: str, badges: List[str], border_color: str = "#38bdf8") -> str:
    b_html = "".join(
        f'<span style="display:inline-block;margin:2px 3px 0 0;padding:1px 6px;border-radius:6px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.16);font-size:0.74em;color:#e2e8f0;">{b}</span>'
        for b in badges if b
    )
    return (
        f'<div style="flex:1 1 168px;min-width:158px;padding:8px 10px;background:rgba(15,23,42,0.92);border:1.5px solid {border_color};border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.28);">'
        f'<div style="font-size:0.72em;font-weight:800;color:{border_color};text-transform:uppercase;letter-spacing:0.3px;margin-bottom:2px;">{tier_badge}</div>'
        f'<div style="font-size:0.88em;font-weight:900;color:#ffffff;line-height:1.32;">{title}</div>'
        f'<div style="font-size:0.78em;color:#cbd5e1;margin-top:2px;line-height:1.35;">{subtitle}</div>'
        + (f'<div style="margin-top:4px;">{b_html}</div>' if b_html else "")
        + f'</div>'
    )


def _render_outcome_box(title: str, detail: str, verdict_color: str = "#fbbf24") -> str:
    return (
        f'<div style="flex:1.2 1 210px;min-width:190px;padding:9px 12px;background:linear-gradient(135deg,rgba(30,41,59,0.96),rgba(15,23,42,0.96));border:2px solid {verdict_color};border-radius:10px;box-shadow:0 3px 14px rgba(251,191,36,0.2);">'
        f'<div style="font-size:0.74em;font-weight:900;color:{verdict_color};margin-bottom:2px;">══► KẾT QUẢ THỰC TẾ CHI TIẾT</div>'
        f'<div style="font-size:0.89em;font-weight:900;color:#ffffff;line-height:1.34;">{title}</div>'
        f'<div style="font-size:0.79em;color:#fef3c7;margin-top:3px;line-height:1.4;">{detail}</div>'
        f'</div>'
    )


def analyze_liuyao_exhaustive_micro_graph(
    luc_hao_data: Dict[str, Any],
    dung_than: str = "Bản Thân",
    topic: str = "Chung",
    question: str = "",
    chart_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    V130.0: Phân tích Lục Hào 4 Tầng Tuyến Lộ Đồ (作用关系四层路线图) + Quái Thân + Thế Thân + 12 Thần Sát
    + Kiểm kê 100% dấu hiệu của cả 6 Hào (Hào 1..6) không bỏ sót bất kỳ chi tiết nào.
    """
    lh = luc_hao_data if isinstance(luc_hao_data, dict) else {}
    cd = chart_data if isinstance(chart_data, dict) else {}
    ban = lh.get("ban") or lh.get("ban_que") or {}
    bien = lh.get("bien") or lh.get("bien_que") or {}
    haos_ban = ban.get("details") or ban.get("haos") or lh.get("haos") or []
    haos_bien = bien.get("details") or bien.get("haos") or []
    dong_list = lh.get("dong_hao") or lh.get("hao_dong") or []
    if isinstance(dong_list, (int, str)):
        dong_list = [int(dong_list)] if str(dong_list).isdigit() else []
    dong_set = {int(x) for x in dong_list if str(x).isdigit()}

    ban_name = str(ban.get("name") or lh.get("ten_que") or "Càn Vi Thiên")
    bien_name = str(bien.get("name") or lh.get("ten_que_bien") or ban_name)
    palace = str(ban.get("palace") or "Càn")
    palace_el_map = {"Càn": "Kim", "Đoài": "Kim", "Ly": "Hỏa", "Chấn": "Mộc", "Tốn": "Mộc", "Khảm": "Thủy", "Cấn": "Thổ", "Khôn": "Thổ"}
    p_el = palace_el_map.get(palace, "Kim")

    can_ngay = str(lh.get("can_ngay") or cd.get("can_ngay") or "Giáp").strip()
    chi_ngay = _norm_chi(lh.get("chi_ngay") or cd.get("chi_ngay") or "Tý") or "Tý"
    chi_thang = _norm_chi(lh.get("chi_thang") or cd.get("chi_thang") or "Tuất") or "Tuất"
    nhat_el = CHI_ELEMENT.get(chi_ngay, "Thổ")
    nguyet_el = CHI_ELEMENT.get(chi_thang, "Thổ")

    ban_lines = list(ban.get("lines") or [int(h.get("line", 1)) for h in haos_ban[:6]])
    while len(ban_lines) < 6:
        ban_lines.append(1)

    the_pos, ung_pos = 3, 6
    for idx_h, h_obj in enumerate(haos_ban[:6], 1):
        tu_s = str(h_obj.get("the_ung") or "")
        if "Thế" in tu_s:
            the_pos = idx_h
        elif "Ứng" in tu_s:
            ung_pos = idx_h

    bodies_ss = compute_liuyao_shensha_and_bodies(
        can_ngay=can_ngay, chi_ngay=chi_ngay, chi_thang=chi_thang,
        ban_lines=ban_lines, the_pos=the_pos, p_element=p_el, details_ban=haos_ban[:6]
    )
    stars_fn = bodies_ss["stars_for_branch"]

    # Định vị Hào Dụng Thần (hoặc Phục Thần nếu Dụng Thần ẩn!)
    dt_clean = str(dung_than or "Bản Thân").strip()
    dt_hao_idx = the_pos
    dt_candidates = []
    for idx_h, h_obj in enumerate(haos_ban[:6], 1):
        lt_h = str(h_obj.get("luc_than") or "")
        if dt_clean != "Bản Thân" and (lt_h == dt_clean or dt_clean in lt_h):
            dt_candidates.append(idx_h)
    if dt_candidates:
        # Ưu tiên hào Động -> Trì Thế -> Trì Ứng -> gần Thế nhất
        dt_candidates.sort(key=lambda ix: (0 if ix in dong_set else 1, 0 if ix == the_pos else (1 if ix == ung_pos else 2), abs(ix - the_pos)))
        dt_hao_idx = dt_candidates[0]

    phuc_list = lh.get("phuc_than") or []
    dt_phuc_obj = None
    if dt_clean != "Bản Thân" and not dt_candidates:
        for pt in phuc_list:
            if isinstance(pt, dict) and str(pt.get("luc_than", "")) == dt_clean:
                dt_phuc_obj = pt
                dt_hao_idx = int(pt.get("hao_pos", the_pos))
                break

    # Kiểm tra Tam Hợp Cục & Tam Hình 3 chữ toàn bàn
    active_branches = {chi_thang, chi_ngay}
    for idx_h, h_obj in enumerate(haos_ban[:6], 1):
        ch_b = _norm_chi(h_obj.get("chi") or str(h_obj.get("can_chi", "")).split("-")[0])
        if idx_h in dong_set or h_obj.get("is_am_dong") or idx_h in (the_pos, dt_hao_idx):
            if ch_b:
                active_branches.add(ch_b)
        if idx_h in dong_set and idx_h <= len(haos_bien):
            ch_bi = _norm_chi(haos_bien[idx_h - 1].get("chi") or str(haos_bien[idx_h - 1].get("can_chi", "")).split("-")[0])
            if ch_bi:
                active_branches.add(ch_bi)

    global_formations = []
    for req_set, th_el, mid_b in TAM_HOP_CUC:
        if req_set.issubset(active_branches):
            global_formations.append(f"🔗 Tam Hợp {th_el} Cục ({'-'.join(sorted(req_set))}) hội tụ khí lực cực mạnh hướng về hành {th_el}")
    if {"Dần", "Tị", "Thân"}.issubset(active_branches):
        global_formations.append("⚠️ Hội đủ Tam Hình Vô Ân/Ỷ Thế (Dần–Tị–Thân): Cảnh báo va chạm pháp lý, cạnh tranh gay gắt hoặc trục trặc đường đi/thủ tục")
    if {"Sửu", "Tuất", "Mùi"}.issubset(active_branches):
        global_formations.append("⚠️ Hội đủ Tam Hình Trì Thế (Sửu–Tuất–Mùi): Cảnh báo nội bộ giằng co dây dưa, áp lực tâm lý hoặc chậm giải ngân/giấy tờ")

    # Kiểm kê chi tiết từng Hào 1..6 & Xây dựng danh sách Cạnh Mũi Tên Nhân Quả 4 Tầng
    directed_edges: List[Dict[str, Any]] = []
    line_micro_audit: List[Dict[str, Any]] = []

    for idx_h in range(1, 7):
        h_obj = haos_ban[idx_h - 1] if idx_h <= len(haos_ban) else {}
        hb_obj = haos_bien[idx_h - 1] if idx_h <= len(haos_bien) else {}
        ch_h = _norm_chi(h_obj.get("chi") or str(h_obj.get("can_chi", "")).split("-")[0]) or "Tý"
        el_h = str(h_obj.get("ngu_hanh") or CHI_ELEMENT.get(ch_h, "Thủy"))
        lt_h = str(h_obj.get("luc_than") or "Huynh Đệ")
        cc_full = str(h_obj.get("can_chi_full") or h_obj.get("can_chi") or f"{ch_h}-{el_h}")
        nap_am = str(h_obj.get("nap_am") or "")
        l_thu = str(h_obj.get("luc_thu") or "Thanh Long")
        v_suy = str(h_obj.get("strength") or h_obj.get("vuong_suy") or "Bình")
        ts_ngay = get_12_truong_sinh_el(el_h, chi_ngay)
        is_mv = (idx_h in dong_set) or bool(h_obj.get("is_moving") or h_obj.get("dong"))
        is_ad = bool(h_obj.get("is_am_dong"))
        is_void = bool(h_obj.get("is_void"))
        k_type = str(h_obj.get("khong_type") or "")
        ss_list = stars_fn(ch_h)
        vi_name, vi_desc = HAO_VI_MEANING.get(idx_h, (f"Hào {idx_h}", ""))

        role_tags = []
        if idx_h == the_pos:
            role_tags.append("HÀO THẾ (Chủ thể/Bản thân)")
        if idx_h == ung_pos:
            role_tags.append("HÀO ỨNG (Đối phương/Hoàn cảnh)")
        if idx_h == dt_hao_idx and not dt_phuc_obj:
            role_tags.append(f"DỤNG THẦN ({dt_clean})")
        if idx_h == bodies_ss["the_than"]["hao"]:
            role_tags.append("THẾ THÂN")
        if ch_h == bodies_ss["quai_than"]["chi"]:
            role_tags.append("QUÁI THÂN")

        incoming_arrows = []
        outgoing_arrows = []

        # TẦNG 1: Nguyệt Lệnh & Nhật Thần -> Hào idx_h
        m_rels = _describe_branch_micro_relations(f"Nguyệt Lệnh {chi_thang}", chi_thang, f"Hào {idx_h} {lt_h}", ch_h, is_high_tier_src=True)
        d_rels = _describe_branch_micro_relations(f"Nhật Thần {chi_ngay}", chi_ngay, f"Hào {idx_h} {lt_h}", ch_h, is_high_tier_src=True)
        for lbl_r, col_r, pts_r, desc_r in m_rels:
            incoming_arrows.append(f"Nguyệt {chi_thang} ──[{lbl_r}]──►")
            if idx_h in (the_pos, ung_pos, dt_hao_idx) or is_mv or is_ad:
                directed_edges.append({
                    "tier": "Tầng 1 · Nguyệt Lệnh",
                    "src": f"Nguyệt Lệnh {chi_thang} ({nguyet_el})",
                    "rel": lbl_r,
                    "color": col_r,
                    "dst": f"Hào {idx_h} {lt_h} ({ch_h}-{el_h})",
                    "outcome": desc_r,
                    "delta": pts_r,
                })
        for lbl_r, col_r, pts_r, desc_r in d_rels:
            incoming_arrows.append(f"Nhật {chi_ngay} ──[{lbl_r}]──►")
            if idx_h in (the_pos, ung_pos, dt_hao_idx) or is_mv or is_ad:
                directed_edges.append({
                    "tier": "Tầng 1 · Nhật Thần",
                    "src": f"Nhật Thần {chi_ngay} ({nhat_el})",
                    "rel": lbl_r,
                    "color": col_r,
                    "dst": f"Hào {idx_h} {lt_h} ({ch_h}-{el_h})",
                    "outcome": desc_r,
                    "delta": pts_r,
                })

        # TẦNG 2 & TẦNG 3: Nếu Hào Động hoặc Ám Động -> Biến Hào tác động ngược + Tác động sang Thế / Dụng Thần
        bien_summary = "Tĩnh (giữ nguyên bản vị)"
        if is_mv and hb_obj:
            ch_b = _norm_chi(hb_obj.get("chi") or str(hb_obj.get("can_chi", "")).split("-")[0]) or ch_h
            el_b = str(hb_obj.get("ngu_hanh") or CHI_ELEMENT.get(ch_b, el_h))
            lt_b = str(hb_obj.get("luc_than") or "")
            cc_b_full = str(hb_obj.get("can_chi_full") or hb_obj.get("can_chi") or f"{ch_b}-{el_b}")
            bien_summary = f"Động hóa {lt_b} ({cc_b_full})"
            hflags = h_obj.get("hoa_flags") or []
            if "HOA_TIEN" in hflags:
                directed_edges.append({
                    "tier": "Tầng 3 · Biến Hào",
                    "src": f"Hào Biến {idx_h} ({ch_b}-{el_b})",
                    "rel": f"Hóa Tiến Thần ({ch_h}➔{ch_b})",
                    "color": "#22c55e",
                    "dst": f"Hào Động {idx_h} {lt_h} ({ch_h}-{el_h})",
                    "outcome": f"Hào {idx_h} {lt_h} hóa Tiến Thần khí lực tăng tiến từng bước vững chắc, sự việc càng về sau càng mạnh.",
                    "delta": 22,
                })
                incoming_arrows.append(f"Hào Biến {ch_b} ──[Hóa Tiến Thần]──►")
            elif "HOA_THOAI" in hflags:
                directed_edges.append({
                    "tier": "Tầng 3 · Biến Hào",
                    "src": f"Hào Biến {idx_h} ({ch_b}-{el_b})",
                    "rel": f"Hóa Thoái Thần ({ch_h}➔{ch_b})",
                    "color": "#f97316",
                    "dst": f"Hào Động {idx_h} {lt_h} ({ch_h}-{el_h})",
                    "outcome": f"Hào {idx_h} {lt_h} hóa Thoái Thần — ban đầu hăng hái nhưng sau giảm nhiệt, rút lui hoặc nhượng bộ dần.",
                    "delta": -18,
                })
                incoming_arrows.append(f"Hào Biến {ch_b} ──[Hóa Thoái Thần]──►")
            else:
                b_rels = _describe_branch_micro_relations(f"Hào Biến {idx_h} {lt_b}", ch_b, f"Hào Động {idx_h} {lt_h}", ch_h, is_high_tier_src=True)
                for lbl_b, col_b, pts_b, desc_b in b_rels[:2]:
                    hd_lbl = lbl_b.replace("Tương Sinh", "Hồi Đầu Sinh").replace("Tương Khắc", "Hồi Đầu Khắc").replace("Lục Xung", "Hồi Đầu Xung (Phản Ngâm)").replace("Lục Hợp", "Hồi Đầu Hợp")
                    directed_edges.append({
                        "tier": "Tầng 3 · Biến Hào",
                        "src": f"Hào Biến {idx_h} {lt_b} ({ch_b}-{el_b})",
                        "rel": hd_lbl,
                        "color": col_b,
                        "dst": f"Hào Động {idx_h} {lt_h} ({ch_h}-{el_h})",
                        "outcome": desc_b,
                        "delta": pts_b,
                    })
                    incoming_arrows.append(f"Hào Biến {ch_b} ──[{hd_lbl}]──►")

        # TẦNG 2: Hào Động / Ám Động tác động sang Hào Dụng Thần & Hào Thế
        if (is_mv or is_ad):
            src_kind = "Hào Động" if is_mv else "Hào Ám Động"
            targets_t2 = []
            if idx_h != dt_hao_idx and not dt_phuc_obj:
                targets_t2.append((dt_hao_idx, f"Dụng Thần Hào {dt_hao_idx}"))
            if idx_h != the_pos and the_pos != dt_hao_idx:
                targets_t2.append((the_pos, f"Hào Thế {the_pos}"))
            for t_ix, t_tag in targets_t2:
                if 1 <= t_ix <= len(haos_ban):
                    t_obj = haos_ban[t_ix - 1]
                    t_ch = _norm_chi(t_obj.get("chi") or str(t_obj.get("can_chi", "")).split("-")[0])
                    t_el = str(t_obj.get("ngu_hanh") or CHI_ELEMENT.get(t_ch, "Thổ"))
                    t_lt = str(t_obj.get("luc_than") or "")
                    t2_rels = _describe_branch_micro_relations(f"{src_kind} {idx_h} {lt_h}", ch_h, f"{t_tag} {t_lt}", t_ch, is_high_tier_src=False)
                    for lbl_2, col_2, pts_2, desc_2 in t2_rels[:2]:
                        outgoing_arrows.append(f"──[{lbl_2}]──► Hào {t_ix} {t_lt}")
                        directed_edges.append({
                            "tier": "Tầng 2 · Động Hào Chuyên Quyền",
                            "src": f"{src_kind} {idx_h} {lt_h} ({ch_h}-{el_h})",
                            "rel": lbl_2,
                            "color": col_2,
                            "dst": f"{t_tag} {t_lt} ({t_ch}-{t_el})",
                            "outcome": desc_2,
                            "delta": pts_2,
                        })

        zy_txt = str(h_obj.get("hao_tu_vn") or "").strip()
        void_str = ""
        if is_void:
            void_str = "Giả Không (Đợi Xuất Không là ứng ngay)" if k_type == "GIA_KHONG" else "Chân Không (Hiện tại rỗng/chưa thành thực chất)"

        real_life_line_note = (
            f"{vi_name}: {lt_h} ({cc_full}{', ' + nap_am if nap_am else ''}) lâm {l_thu}, khí {v_suy} (Trường Sinh ngày {chi_ngay}: {ts_ngay}). "
            + (f"Thần sát hội tại hào: {', '.join(ss_list)}. " if ss_list else "")
            + (f"Trạng thái Không Vong: {void_str}. " if void_str else "")
            + (f"Chu Dịch Hào Từ: {zy_txt}" if zy_txt and (is_mv or idx_h in (the_pos, dt_hao_idx)) else f"Phản ánh mảng: {vi_desc}.")
        )

        line_micro_audit.append({
            "hao": idx_h,
            "roles": role_tags,
            "vi_name": vi_name,
            "luc_than": lt_h,
            "can_chi_full": cc_full,
            "chi": ch_h,
            "ngu_hanh": el_h,
            "nap_am": nap_am,
            "luc_thu": l_thu,
            "vuong_suy": v_suy,
            "ts_ngay": ts_ngay,
            "shensha": ss_list,
            "is_moving": is_mv,
            "is_am_dong": is_ad,
            "is_void": is_void,
            "khong_type": k_type,
            "bien_summary": bien_summary,
            "incoming_arrows": incoming_arrows,
            "outgoing_arrows": outgoing_arrows,
            "real_life_note": real_life_line_note,
        })

    # TẦNG 4: Nếu có Phục Thần -> Mũi tên Phi Thần -> Phục Thần
    for pt in phuc_list:
        if not isinstance(pt, dict):
            continue
        p_pos = int(pt.get("hao_pos", 1))
        phi_lt = str(pt.get("phi_than_luc_than", ""))
        phi_cc = str(pt.get("phi_than_can_chi", ""))
        phuc_lt = str(pt.get("luc_than", ""))
        phuc_cc = str(pt.get("can_chi_full") or pt.get("can_chi", ""))
        dac_xuat = bool(pt.get("dac_xuat"))
        rel_p = "Phi Sinh/Lộ Phục (Đắc Xuất)" if dac_xuat else ("Phi Khắc Phục (Bị Đè Nén)" if pt.get("phi_khac_phuc") else "Ẩn Phục Chờ Xung")
        col_p = "#22c55e" if dac_xuat else "#ef4444"
        directed_edges.append({
            "tier": "Tầng 4 · Phi–Phục Ẩn Tàng",
            "src": f"Phi Thần Hào {p_pos} {phi_lt} ({phi_cc})",
            "rel": rel_p,
            "color": col_p,
            "dst": f"Phục Thần {phuc_lt} ({phuc_cc})",
            "outcome": str(pt.get("phuc_desc") or ""),
            "delta": 10 if dac_xuat else -14,
        })

    # Lắp Sơ Đồ Mũi Tên Trực Quan 4 Tầng Chính của Lục Hào
    dt_line_audit = line_micro_audit[dt_hao_idx - 1]
    the_line_audit = line_micro_audit[the_pos - 1]
    net_delta = sum(int(e.get("delta", 0)) for e in directed_edges)

    t1_node = _render_node_box(
        "Tầng 1 · Thiên Thời Trọng Tài",
        f"Nguyệt {chi_thang} ({nguyet_el}) · Nhật {chi_ngay} ({nhat_el})",
        f"Quái Thân: {bodies_ss['quai_than']['chi']} ({'Hiện' if bodies_ss['quai_than']['is_present'] else 'Ẩn'}) · Thế Thân: Hào {bodies_ss['the_than']['hao']}",
        [f"Thiên Y: {bodies_ss['shensha_dict']['Thiên Y'][0]}", f"Dịch Mã: {bodies_ss['shensha_dict']['Dịch Mã'][0]}"],
        "#38bdf8",
    )

    if dong_set:
        mv_first = sorted(dong_set)[0]
        mv_a = line_micro_audit[mv_first - 1]
        t2_node = _render_node_box(
            "Tầng 2 & 3 · Nội Nhân Phát Động",
            f"Hào {mv_first} {mv_a['luc_than']} ({mv_a['can_chi_full']})",
            mv_a["bien_summary"],
            mv_a["shensha"][:3] + ([f"Lục Thú: {mv_a['luc_thu']}"] if mv_a["luc_thu"] else []),
            "#f59e0b",
        )
        arrow_12_lbl = f"Khí {mv_a['vuong_suy']} · TS:{mv_a['ts_ngay']}"
        arrow_23_lbl = "Trực tiếp biến hóa" if mv_first == dt_hao_idx else (
            f"Sinh {dt_line_audit['luc_than']}" if SINH_EL.get(mv_a["ngu_hanh"]) == dt_line_audit["ngu_hanh"]
            else (f"Khắc {dt_line_audit['luc_than']}" if KHAC_EL.get(mv_a["ngu_hanh"]) == dt_line_audit["ngu_hanh"] else "Dẫn động khí cục")
        )
        arrow_23_col = "#22c55e" if "Sinh" in arrow_23_lbl or "biến" in arrow_23_lbl else ("#ef4444" if "Khắc" in arrow_23_lbl else "#38bdf8")
    else:
        t2_node = _render_node_box(
            "Tầng 2 · Lục Hào An Tĩnh",
            f"Hào Thế {the_pos} {the_line_audit['luc_than']} ({the_line_audit['chi']}-{the_line_audit['ngu_hanh']})",
            f"Khí {the_line_audit['vuong_suy']} · TS ngày: {the_line_audit['ts_ngay']}",
            the_line_audit["shensha"][:3] or [the_line_audit["luc_thu"]],
            "#a78bfa",
        )
        arrow_12_lbl = f"Nhật/Nguyệt ➔ Thế ({the_line_audit['vuong_suy']})"
        arrow_23_lbl = "Tương tác Thế ↔ Dụng"
        arrow_23_col = "#38bdf8"

    if dt_phuc_obj:
        t3_node = _render_node_box(
            "Tầng 4 · Đích Dụng Thần (Ẩn Phục)",
            f"Phục Thần {dt_clean} ({dt_phuc_obj.get('can_chi_full', '')})",
            f"Ẩn dưới Hào {dt_hao_idx} {dt_phuc_obj.get('phi_than_luc_than', '')} ({'Đắc Xuất' if dt_phuc_obj.get('dac_xuat') else 'Bị Đè'})",
            stars_fn(dt_phuc_obj.get("chi", ""))[:3],
            "#c084fc",
        )
    else:
        t3_node = _render_node_box(
            "Trọng Tâm · Đích Dụng Thần",
            f"Hào {dt_hao_idx} {dt_line_audit['luc_than']} ({dt_line_audit['can_chi_full']})",
            f"Khí {dt_line_audit['vuong_suy']} · TS ngày: {dt_line_audit['ts_ngay']} · {dt_line_audit['luc_thu']}",
            dt_line_audit["shensha"][:3] + (["Giả Không" if dt_line_audit["khong_type"] == "GIA_KHONG" else "Chân Không"] if dt_line_audit["is_void"] else []),
            "#34d399" if dt_line_audit["vuong_suy"] in ("Vượng", "Tướng") else "#fb7185",
        )

    lh_verdict_good = (dt_line_audit["vuong_suy"] in ("Vượng", "Tướng") or net_delta >= 8) and dt_line_audit["khong_type"] != "CHAN_KHONG"
    out_title_lh = (
        f"Dụng Thần Hữu Khí Đắc Trợ ({ban_name} ➔ {bien_name})"
        if lh_verdict_good else
        f"Dụng Thần Chịu Lực Cản / Chờ Thời Mở Khóa ({ban_name} ➔ {bien_name})"
    )
    out_detail_lh = (
        f"{bodies_ss['quai_than']['status_str']}. "
        + (f"Điểm nhấn: {global_formations[0]}. " if global_formations else "")
        + f"Ứng kỳ mở nút thắt tại chi {LUC_XUNG.get(dt_line_audit['chi'], '')} (Xung) hoặc {LUC_HOP.get(dt_line_audit['chi'], ('', ''))[0]} (Hợp)."
    )
    out_node_lh = _render_outcome_box(out_title_lh, out_detail_lh, "#22c55e" if lh_verdict_good else "#f59e0b")

    flowchart_html = (
        f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:11px;border:1px solid rgba(56,189,248,0.35);margin-bottom:8px;">'
        f'<div style="font-size:0.86em;font-weight:900;color:#7dd3fc;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
        f'<span>☯️ SƠ ĐỒ MŨI TÊN LỤC HÀO 4 TẦNG TÁC ĐỘNG (Chuẩn Nguyên Hanh Lợi Trinh · Vấn Chân Lục Hào)</span>'
        f'<span style="color:#fde68a;font-size:0.88em;">Quái Thân: {bodies_ss["quai_than"]["chi"]}-{bodies_ss["quai_than"]["luc_than"]} | Thế Thân: Hào {bodies_ss["the_than"]["hao"]}</span>'
        f'</div>'
        f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
        f'{t1_node}{_render_svg_arrow(arrow_12_lbl, "#38bdf8")}{t2_node}{_render_svg_arrow(arrow_23_lbl, arrow_23_col)}{t3_node}{_render_svg_arrow("Hội tụ Nhân Quả", "#fbbf24")}{out_node_lh}'
        f'</div></div>'
    )

    return {
        "quai_than": bodies_ss["quai_than"],
        "the_than": bodies_ss["the_than"],
        "shensha_dict": bodies_ss["shensha_dict"],
        "global_formations": global_formations,
        "directed_edges": directed_edges,
        "line_micro_audit": line_micro_audit,
        "dt_hao_idx": dt_hao_idx,
        "the_pos": the_pos,
        "ung_pos": ung_pos,
        "flowchart_html": flowchart_html,
    }


def analyze_qimen_exhaustive_micro_graph(
    chart_data: Dict[str, Any],
    target_cung: Optional[int] = None,
    dung_than: str = "Bản Thân",
    topic: str = "Chung",
    question: str = "",
) -> Dict[str, Any]:
    """
    V130.0: Phân tích Kỳ Môn Độn Giáp Vi Mô Toàn Diện (chuẩn Vấn Chân Kỳ Môn & Nguyên Hanh Lợi Trinh):
    - Khôi phục Can thứ 9 Trung Cung Ký Cung Song Can (ky_can_thien_ban & ky_can_dia_ban)
    - Ám Can (暗干) 9 Cung tiết lộ động cơ ngầm & biến số ẩn
    - Tứ Hại đầy đủ (Không Vong Ngày/Giờ · Môn Bức · Lục Nghi Kích Hình · Thiên Bàn Nhập Mộ) + 12 Trường Sinh Lạc Cung
    - Sơ Đồ Mũi Tên Lật Cung Liên Hoàn 4 Trạm (Quá khứ Gốc rễ ──► Hiện tại Trực diện ──► Chuyển tiếp Kế tiếp ──► Kết cục Cuối cùng)
    """
    cd = chart_data if isinstance(chart_data, dict) else {}
    try:
        from qmdg_data import enrich_qimen_chart_dict, find_qimen_stem_palace, resolve_six_jia_stem
        enrich_qimen_chart_dict(cd)
    except Exception:
        resolve_six_jia_stem = lambda c, ch="Tý": str(c or "Mậu")
        find_qimen_stem_palace = lambda d, s, ch="", plate="heaven": (2, False, str(s or "Mậu"))

    ctb = cd.get("can_thien_ban") or {}
    kctb = cd.get("ky_can_thien_ban") or {}
    db = cd.get("dia_ban") or cd.get("dia_can") or {}
    kdb = cd.get("ky_can_dia_ban") or {}
    tb = cd.get("thien_ban") or {}
    nb = cd.get("nhan_ban") or {}
    sb = cd.get("than_ban") or {}
    am_can_map = cd.get("am_can") or {}

    can_ngay = str(cd.get("can_ngay") or "Giáp").strip()
    chi_ngay = _norm_chi(cd.get("chi_ngay") or "Tý") or "Tý"
    can_gio = str(cd.get("can_gio") or "Giáp").strip()
    chi_gio = _norm_chi(cd.get("chi_gio") or "Tý") or "Tý"

    cung_chu, chu_is_ky, stem_chu = find_qimen_stem_palace(cd, can_ngay, chi_ngay, "heaven")
    cung_khach, khach_is_ky, stem_khach = find_qimen_stem_palace(cd, can_gio, chi_gio, "heaven")
    cung_chu = cung_chu or 2
    cung_khach = cung_khach or 8

    tc = int(target_cung) if str(target_cung).isdigit() and 1 <= int(target_cung) <= 9 else 0
    if tc == 5:
        tc = int(cd.get("p_nhue_cam") or 2)
    if not tc:
        tc = cung_khach if dung_than != "Bản Thân" else cung_chu

    kv_ngay = {int(x) for x in (cd.get("khong_vong") or []) if str(x).isdigit()}
    kv_gio = {int(x) for x in (cd.get("khong_vong_gio") or []) if str(x).isdigit()}
    ma_ngay = cd.get("dich_ma")
    ma_gio = cd.get("dich_ma_gio")

    KICH_HINH_RULES = {
        ("Mậu", 3): "Mậu lâm Chấn 3 (Giáp Tý–Mão Hình: vốn liếng/tài sản bị va đập hoặc chi tiêu bất ngờ)",
        ("Kỷ", 2): "Kỷ lâm Khôn 2 (Giáp Tuất–Mùi Hình: mưu tính riêng tự làm khó mình, nội bộ khúc mắc)",
        ("Canh", 8): "Canh lâm Cấn 8 (Giáp Thân–Dần Hình: lực cản sắc bén, tranh chấp hoặc kẹt thủ tục cứng)",
        ("Tân", 9): "Tân lâm Ly 9 (Giáp Ngọ–Ngọ Tự Hình: nóng vội mắc lỗi sai chủ quan, dễ tự ái)",
        ("Nhâm", 4): "Nhâm lâm Tốn 4 (Giáp Thìn–Thìn Tự Hình: đi lại/dòng việc rối rắm, tự trói chân)",
        ("Quý", 4): "Quý lâm Tốn 4 (Giáp Dần–Tị Hình: vướng lưới rắc rối ngầm hoặc giấy tờ rườm rà)",
    }
    NHAP_MO_CUNG = {
        "Ất": {2, 6}, "Bính": {6}, "Mậu": {6}, "Đinh": {8}, "Kỷ": {8},
        "Canh": {8}, "Tân": {4}, "Nhâm": {4}, "Quý": {4},
    }

    def _audit_single_palace(p_num: int) -> Dict[str, Any]:
        quai_n, huong_n, el_p, _ = CUNG_META_9.get(p_num, ("Khôn", "Tây Nam", "Thổ", ["Mùi", "Thân"]))
        t_stem = str(ctb.get(p_num) or ctb.get(str(p_num)) or (db.get(5) if p_num == 5 else "Mậu")).strip()
        ky_t = str(kctb.get(p_num) or kctb.get(str(p_num)) or "").strip()
        d_stem = str(db.get(p_num) or db.get(str(p_num)) or "Mậu").strip()
        ky_d = str(kdb.get(p_num) or kdb.get(str(p_num)) or "").strip()
        a_stem = str(am_can_map.get(p_num) or am_can_map.get(str(p_num)) or "").strip()
        star = str(tb.get(p_num) or tb.get(str(p_num)) or ("Thiên Cầm" if p_num == 5 else "Thiên Phụ")).strip()
        door = str(nb.get(p_num) or nb.get(str(p_num)) or ("Tử Môn (Ký Khôn 2)" if p_num == 5 else "Khai Môn")).strip()
        deity = str(sb.get(p_num) or sb.get(str(p_num)) or ("Trực Phù" if p_num == 5 else "Trực Phù")).strip()

        door_short = door.replace(" Môn", "").split()[0]
        el_door = DOOR_EL.get(door_short, "Thổ")
        tu_hai = []
        good_signs = []

        if p_num != 5 and KHAC_EL.get(el_door) == el_p:
            tu_hai.append(f"Môn Bức ({door} [{el_door}] khắc Cung {quai_n} [{el_p}])")
        elif p_num != 5 and SINH_EL.get(el_door) == el_p:
            good_signs.append(f"Môn Hòa ({door} sinh Cung)")
        elif p_num != 5 and SINH_EL.get(el_p) == el_door:
            good_signs.append(f"Môn Nghĩa (Cung sinh {door})")

        for st_chk in ([t_stem] + ([ky_t] if ky_t and ky_t != t_stem else [])):
            if (st_chk, p_num) in KICH_HINH_RULES:
                tu_hai.append(f"Kích Hình: {KICH_HINH_RULES[(st_chk, p_num)]}")
            if p_num in NHAP_MO_CUNG.get(st_chk, set()):
                tu_hai.append(f"Thiên Bàn Nhập Mộ ({st_chk} nhập Mộ tại Cung {p_num})")

        if p_num in kv_ngay:
            tu_hai.append("Tuần Không Ngày (Lực hiện tại rỗng 50–70%, chờ Xuất/Xung Không)")
        if p_num in kv_gio and p_num not in kv_ngay:
            tu_hai.append("Tuần Không Giờ (Sự việc tạm thời ẩn tàng hoặc trễ nhịp ngắn)")
        if str(ma_ngay) == str(p_num) or str(ma_gio) == str(p_num):
            good_signs.append("Đắc Dịch Mã Tinh (Chuyển động nhanh, Xung Không Xung Mộ tức thời)")

        ts_t = get_qimen_stem_palace_stage(t_stem, p_num)
        ts_d = get_qimen_stem_palace_stage(d_stem, p_num)
        t_disp = f"{t_stem}(+{ky_t})" if ky_t and ky_t != t_stem else t_stem
        d_disp = f"{d_stem}(+{ky_d})" if ky_d and ky_d != d_stem else d_stem

        return {
            "cung": p_num,
            "quai": quai_n,
            "huong": huong_n,
            "ngu_hanh": el_p,
            "can_thien": t_stem,
            "ky_can_thien": ky_t,
            "can_thien_disp": t_disp,
            "can_dia": d_stem,
            "ky_can_dia": ky_d,
            "can_dia_disp": d_disp,
            "am_can": a_stem,
            "am_can_meaning": STEM_MEANING_SHORT.get(a_stem, ""),
            "star": star,
            "door": door,
            "deity": deity,
            "ts_thien": ts_t,
            "ts_dia": ts_d,
            "tu_hai": tu_hai,
            "good_signs": good_signs,
        }

    palace_micro_audit = {p: _audit_single_palace(p) for p in range(1, 10)}
    p_cur_info = palace_micro_audit[tc]

    # XÂY DỰNG CHUỖI LẬT CUNG 4 TRẠM (奇门翻宫四站因果链 — 问真奇门):
    # Trạm 1 (Quá khứ / Nguyên nhân gốc): Thiên Can tại Cung Hiện Tại (tc) vốn từ Địa Bàn cung nào bay tới?
    p_past, _, _ = find_qimen_stem_palace(cd, p_cur_info["can_thien"], chi_gio, "earth")
    p_past = p_past or tc
    # Trạm 3 (Chuyển tiếp kế tiếp): Địa Can tại Cung Hiện Tại (tc) bay lên Thiên Bàn ở cung nào?
    p_next1, _, _ = find_qimen_stem_palace(cd, p_cur_info["can_dia"], chi_gio, "heaven")
    p_next1 = p_next1 or tc
    # Trạm 4 (Kết cục hạ màn): Địa Can của Cung p_next1 bay tiếp lên Thiên Bàn ở cung nào?
    p_next2, _, _ = find_qimen_stem_palace(cd, palace_micro_audit[p_next1]["can_dia"], chi_gio, "heaven")
    p_next2 = p_next2 or p_next1

    st_past = palace_micro_audit[p_past]
    st_cur = p_cur_info
    st_n1 = palace_micro_audit[p_next1]
    st_n2 = palace_micro_audit[p_next2]

    qimen_edges: List[Dict[str, Any]] = []
    # Mũi tên Chủ - Khách (Can Ngày <-> Can Giờ) & Trực Sử (Quyền thực thi)
    el_chu = palace_micro_audit[cung_chu]["ngu_hanh"]
    el_khach = palace_micro_audit[cung_khach]["ngu_hanh"]
    el_tc = st_cur["ngu_hanh"]
    cung_truc_su = int(cd.get("cung_dich_truc_su") or cung_khach)
    st_ts = palace_micro_audit.get(cung_truc_su, st_cur)

    if cung_chu == tc:
        ck_rel, ck_col, ck_desc = "Đồng Cung Tương Hội", "#22c55e", f"Nhật Can {stem_chu} đồng cung Dụng Thần tại Cung {tc} ({st_cur['huong']}) — người và việc gắn chặt làm một, chủ động nắm bắt trực tiếp."
    elif SINH_EL.get(el_tc) == el_chu:
        ck_rel, ck_col, ck_desc = f"Dụng Sinh Chủ ({el_tc}➔{el_chu})", "#22c55e", f"Cung Dụng Thần {tc} ({el_tc}) tương sinh Cung Bản Thân {cung_chu} ({el_chu}) — mục tiêu tự tìm đến sinh lợi thuận lợi cho bạn."
    elif KHAC_EL.get(el_tc) == el_chu:
        ck_rel, ck_col, ck_desc = f"Dụng Khắc Chủ ({el_tc}⚔{el_chu})", "#ef4444", f"Cung Dụng Thần {tc} ({el_tc}) khắc Cung Bản Thân {cung_chu} ({el_chu}) — sự việc tạo áp lực lớn, tuyệt đối không nóng vội cưỡng cầu."
    elif KHAC_EL.get(el_chu) == el_tc:
        ck_rel, ck_col, ck_desc = f"Chủ Khắc Dụng ({el_chu}➔{el_tc})", "#38bdf8", f"Cung Bản Thân {cung_chu} ({el_chu}) chế khắc Cung Dụng Thần {tc} ({el_tc}) — phải trực tiếp ra tay điều phối mới thu phục được kết quả."
    else:
        ck_rel, ck_col, ck_desc = f"Chủ Sinh/Hòa Dụng ({el_chu}↔{el_tc})", "#fbbf24", f"Cung Bản Thân {cung_chu} ({el_chu}) sinh xuất/tỷ hòa với Cung {tc} ({el_tc}) — cần đầu tư công sức và tâm huyết trước rồi mới gặt quả."

    qimen_edges.append({
        "tier": "Kỳ Môn · Trục Chủ–Dụng",
        "src": f"Cung Chủ Thể {cung_chu} ({stem_chu}{'·Ký Cung' if chu_is_ky else ''}, {palace_micro_audit[cung_chu]['door']})",
        "rel": ck_rel,
        "color": ck_col,
        "dst": f"Cung Dụng Thần {tc} ({st_cur['can_thien_disp']}/{st_cur['can_dia_disp']}, {st_cur['door']})",
        "outcome": ck_desc,
    })
    qimen_edges.append({
        "tier": "Kỳ Môn · Ám Can & Tứ Hại",
        "src": f"Ám Can [{st_cur['am_can']}] tại Cung {tc}",
        "rel": "Ẩn Cơ Phát Tác" if not st_cur["tu_hai"] else f"Kèm {len(st_cur['tu_hai'])} Tứ Hại",
        "color": "#a78bfa" if not st_cur["tu_hai"] else "#f97316",
        "dst": f"{st_cur['star']} · {st_cur['door']} · {st_cur['deity']}",
        "outcome": f"Ẩn ý Ám Can [{st_cur['am_can']}]: {st_cur['am_can_meaning']}. " + (
            f"Cảnh báo Tứ Hại: {'; '.join(st_cur['tu_hai'])}." if st_cur["tu_hai"] else "Cung thanh thuần không phạm Tứ Hại, khí lực thực thi thông suốt."
        ),
    })
    qimen_edges.append({
        "tier": "Kỳ Môn · Trực Sử Phê Duyệt",
        "src": f"Trực Sử {cd.get('truc_su', st_ts['door'])} tại Cung {cung_truc_su} ({st_ts['ngu_hanh']})",
        "rel": "Quyền Hành Thực Thi",
        "color": "#34d399" if KHAC_EL.get(st_ts["ngu_hanh"]) != el_tc else "#ef4444",
        "dst": f"Cung Dụng Thần {tc} ({el_tc})",
        "outcome": (
            f"Trực Sử Môn ({st_ts['ngu_hanh']}) khắc Cung Dụng Thần ({el_tc}) — khâu phê duyệt/thực thi cuối gặp chốt chặn quy trình."
            if KHAC_EL.get(st_ts["ngu_hanh"]) == el_tc else
            f"Trực Sử Môn ({st_ts['ngu_hanh']}) nâng đỡ/hòa hợp Cung Dụng Thần ({el_tc}) — việc triển khai thực tế ngoài đời có cửa thông qua."
        ),
    })

    n1_box = _render_node_box(
        "Trạm 1 · Nguyên Nhân Quá Khứ",
        f"Cung {p_past} {st_past['quai']} ({st_past['can_thien_disp']}/{st_past['can_dia_disp']})",
        f"{st_past['star']} · {st_past['door']} · {st_past['deity']}",
        [f"Gốc Can {st_cur['can_thien']}", f"Ám Can: {st_past['am_can']}"],
        "#94a3b8",
    )
    n2_box = _render_node_box(
        "Trạm 2 · Hiện Tại Trực Diện",
        f"Cung {tc} {st_cur['quai']} ({st_cur['can_thien_disp']}/{st_cur['can_dia_disp']})",
        f"{st_cur['star']} · {st_cur['door']} · {st_cur['deity']}",
        [f"Ám Can: {st_cur['am_can']}", f"TS: {st_cur['ts_thien']}"] + ([f"⚠️ {len(st_cur['tu_hai'])} Tứ Hại"] if st_cur["tu_hai"] else ["✅ 0 Tứ Hại"]),
        "#fbbf24",
    )
    n3_box = _render_node_box(
        "Trạm 3 · Bước Chuyển Kế Tiếp",
        f"Cung {p_next1} {st_n1['quai']} ({st_n1['can_thien_disp']}/{st_n1['can_dia_disp']})",
        f"{st_n1['star']} · {st_n1['door']} · {st_n1['deity']}",
        [f"Lật theo Can {st_cur['can_dia']}", f"Ám Can: {st_n1['am_can']}"],
        "#38bdf8",
    )
    out_km = _render_outcome_box(
        f"Trạm 4 Hạ Màn: Cung {p_next2} {st_n2['quai']} ({st_n2['door']} · {st_n2['star']})",
        f"Can {st_n2['can_thien_disp']}/{st_n2['can_dia_disp']} ({STEM_MEANING_SHORT.get(st_n2['can_thien'], '')}). Ám Can Cung Đích [{st_cur['am_can']}]: {st_cur['am_can_meaning']}.",
        "#34d399" if any(c in st_n2["door"] for c in ("Khai", "Hưu", "Sinh")) and not st_cur["tu_hai"] else "#f59e0b",
    )

    _ar_km_1 = _render_svg_arrow(f"Can {st_cur['can_thien']} bay tới", "#94a3b8")
    _ar_km_2 = _render_svg_arrow(f"Lật Can {st_cur['can_dia']}", "#38bdf8")
    _ar_km_3 = _render_svg_arrow(f"Lật Can {st_n1['can_dia']}", "#fbbf24")
    flowchart_html = (
        f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:11px;border:1px solid rgba(251,191,36,0.35);margin-bottom:8px;">'
        f'<div style="font-size:0.86em;font-weight:900;color:#fde047;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
        f'<span>🧭 SƠ ĐỒ MŨI TÊN KỲ MÔN LẬT CUNG 4 TRẠM & ÁM CAN — TỨ HẠI (Chuẩn Vấn Chân Kỳ Môn)</span>'
        f'<span style="color:#a7f3d0;font-size:0.88em;">Chủ: Cung {cung_chu} ({stem_chu}) ↔ Sự việc: Cung {cung_khach} ({stem_khach}) | Ký Cung 5: {cd.get("stem_trung_cung_5", "Mậu")}➔Cung {cd.get("p_nhue_cam", 2)}</span>'
        f'</div>'
        f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
        f'{n1_box}{_ar_km_1}{n2_box}{_ar_km_2}{n3_box}{_ar_km_3}{out_km}'
        f'</div></div>'
    )

    return {
        "target_cung": tc,
        "cung_chu": cung_chu,
        "cung_khach": cung_khach,
        "cung_truc_su": cung_truc_su,
        "phien_cung_chain": [p_past, tc, p_next1, p_next2],
        "palace_micro_audit": palace_micro_audit,
        "directed_edges": qimen_edges,
        "flowchart_html": flowchart_html,
    }


def analyze_meihua_exhaustive_micro_graph(
    mai_hoa_data: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    topic: str = "Chung",
    question: str = "",
) -> Dict[str, Any]:
    """
    V130.0: Phân tích Mai Hoa Dịch Số 4 Chặng Tiến Hóa (Bản Quái ──► Hạ Hỗ [2-3-4] ──► Thượng Hỗ [3-4-5] ──► Biến Quái + Hào Từ).
    """
    mh = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
    cd = chart_data if isinstance(chart_data, dict) else {}
    chi_thang = _norm_chi(cd.get("chi_thang") or "Tuất") or "Tuất"
    nguyet_el = CHI_ELEMENT.get(chi_thang, "Thổ")

    idx_to_trigram = {1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"}
    u_raw = mh.get("upper") or mh.get("thuong_quai") or 1
    l_raw = mh.get("lower") or mh.get("ha_quai") or 4
    up_q = idx_to_trigram.get(int(u_raw), "Càn") if str(u_raw).isdigit() else str(u_raw)
    lo_q = idx_to_trigram.get(int(l_raw), "Chấn") if str(l_raw).isdigit() else str(l_raw)
    if up_q not in TRIGRAM_META_8:
        up_q = "Càn"
    if lo_q not in TRIGRAM_META_8:
        lo_q = "Chấn"

    dong_hao = int(mh.get("dong_hao") or 4)
    if not (1 <= dong_hao <= 6):
        dong_hao = 4

    lines6 = list(TRIGRAM_META_8[lo_q][0]) + list(TRIGRAM_META_8[up_q][0])
    lines_bien = list(lines6)
    lines_bien[dong_hao - 1] = 0 if lines_bien[dong_hao - 1] == 1 else 1

    ha_ho = BIN_TO_TRIGRAM_8.get(tuple(lines6[1:4]), "Cấn")
    thuong_ho = BIN_TO_TRIGRAM_8.get(tuple(lines6[2:5]), "Tốn")
    lo_bien = BIN_TO_TRIGRAM_8.get(tuple(lines_bien[:3]), lo_q)
    up_bien = BIN_TO_TRIGRAM_8.get(tuple(lines_bien[3:]), up_q)

    the_q = up_q if dong_hao <= 3 else lo_q
    dung_q = lo_q if dong_hao <= 3 else up_q
    bien_dung_q = lo_bien if dong_hao <= 3 else up_bien

    el_the = TRIGRAM_META_8[the_q][3]
    el_dung = TRIGRAM_META_8[dung_q][3]
    el_haho = TRIGRAM_META_8[ha_ho][3]
    el_thuongho = TRIGRAM_META_8[thuong_ho][3]
    el_biendung = TRIGRAM_META_8[bien_dung_q][3]

    def _td_arrow(src_name: str, src_el: str) -> Tuple[str, str, str]:
        if SINH_EL.get(src_el) == el_the:
            return (f"{src_el} sinh Thể {el_the}", "#22c55e", f"{src_name} ({src_el}) sinh trợ trực tiếp cho Quẻ Thể {the_q} ({el_the}) — thuận lợi tự nhiên, có lộc nâng đỡ.")
        if src_el == el_the:
            return (f"Tỷ Hòa ({el_the})", "#4ade80", f"{src_name} ({src_el}) đồng hành Tỷ Hòa với Quẻ Thể {the_q} — có bạn đồng hành, nội ngoại hiệp lực.")
        if KHAC_EL.get(el_the) == src_el:
            return (f"Thể khắc {src_el}", "#38bdf8", f"Quẻ Thể {the_q} ({el_the}) chế phục {src_name} ({src_el}) — làm chủ được tình thế nhưng cần chủ động xúc tiến.")
        if SINH_EL.get(el_the) == src_el:
            return (f"Thể sinh {src_el}", "#f59e0b", f"Quẻ Thể {the_q} ({el_the}) tiết khí sinh xuất cho {src_name} ({src_el}) — hao tổn tâm sức, tiền bạc hoặc thời gian.")
        return (f"{src_el} khắc Thể {el_the}", "#ef4444", f"{src_name} ({src_el}) khắc chế Quẻ Thể {the_q} ({el_the}) — gặp lực cản thực tế hoặc áp lực khách quan.")

    r1_lbl, r1_col, r1_desc = _td_arrow(f"Dụng {dung_q}", el_dung)
    r2_lbl, r2_col, r2_desc = _td_arrow(f"Hạ Hỗ {ha_ho}", el_haho)
    r3_lbl, r3_col, r3_desc = _td_arrow(f"Thượng Hỗ {thuong_ho}", el_thuongho)
    r4_lbl, r4_col, r4_desc = _td_arrow(f"Biến Dụng {bien_dung_q}", el_biendung)

    ten_chu = str(mh.get("ten") or mh.get("ten_que") or f"{up_q}/{lo_q}")
    ten_ho = str(mh.get("ten_ho") or f"{thuong_ho}/{ha_ho}")
    ten_bien = str(mh.get("ten_qua_bien") or f"{up_bien}/{lo_bien}")
    sum_tien_thien = TRIGRAM_META_8[up_q][1] + TRIGRAM_META_8[lo_q][1]
    sum_hau_thien = TRIGRAM_META_8[up_q][2] + TRIGRAM_META_8[lo_q][2]

    mh_edges = [
        {"tier": "Mai Hoa · Chặng 1 (Khởi sự)", "src": f"Quẻ Dụng {dung_q} ({el_dung})", "rel": r1_lbl, "color": r1_col, "dst": f"Quẻ Thể {the_q} ({el_the})", "outcome": r1_desc},
        {"tier": "Mai Hoa · Chặng 2 (Nội Hỗ 2-3-4)", "src": f"Hạ Hỗ {ha_ho} ({el_haho})", "rel": r2_lbl, "color": r2_col, "dst": f"Quẻ Thể {the_q} ({el_the})", "outcome": f"Giai đoạn đầu trung gian: {r2_desc}"},
        {"tier": "Mai Hoa · Chặng 3 (Ngoại Hỗ 3-4-5)", "src": f"Thượng Hỗ {thuong_ho} ({el_thuongho})", "rel": r3_lbl, "color": r3_col, "dst": f"Quẻ Thể {the_q} ({el_the})", "outcome": f"Bước ngoặt sát kết cục: {r3_desc}"},
        {"tier": "Mai Hoa · Chặng 4 (Biến Quái Quyết Định)", "src": f"Biến Dụng {bien_dung_q} ({el_biendung})", "rel": r4_lbl, "color": r4_col, "dst": f"Quẻ Thể {the_q} ({el_the})", "outcome": f"Kết quả chung cuộc ({ten_bien}): {r4_desc}"},
    ]

    m1 = _render_node_box(
        "Chặng 1 · Khởi Đầu (Bản Quái)",
        ten_chu,
        f"Thể {the_q}({el_the}) ↔ Dụng {dung_q}({el_dung})",
        [f"Tiên Thiên: {sum_tien_thien}", f"Nguyệt khí: {nguyet_el}"],
        r1_col,
    )
    m2 = _render_node_box(
        "Chặng 2 · Nội Tình (Hạ Hỗ 2-3-4)",
        f"Hạ Hỗ {ha_ho} ({el_haho})",
        TRIGRAM_META_8[ha_ho][4],
        [r2_lbl],
        r2_col,
    )
    m3 = _render_node_box(
        "Chặng 3 · Bước Ngoặt (Thượng Hỗ 3-4-5)",
        f"Thượng Hỗ {thuong_ho} ({el_thuongho})",
        f"Hỗ Quái: {ten_ho}",
        [r3_lbl],
        r3_col,
    )
    m4_out = _render_outcome_box(
        f"Chặng 4 Kết Cục: {ten_bien} (Động Hào {dong_hao})",
        f"{r4_desc} Định lượng Quái số: Tiên Thiên = {sum_tien_thien}, Hậu Thiên = {sum_hau_thien}.",
        r4_col,
    )

    flowchart_html = (
        f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:11px;border:1px solid rgba(244,114,182,0.35);margin-bottom:8px;">'
        f'<div style="font-size:0.86em;font-weight:900;color:#f9a8d4;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
        f'<span>🌸 SƠ ĐỒ MŨI TÊN MAI HOA 4 CHẶNG TIẾN HÓA (Bản Quái ➔ Hạ Hỗ ➔ Thượng Hỗ ➔ Biến Quái)</span>'
        f'<span style="color:#fbcfe8;font-size:0.88em;">Thể: {the_q} ({el_the}) | Động Hào {dong_hao} ({HAO_VI_MEANING.get(dong_hao, ("", ""))[0]})</span>'
        f'</div>'
        f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
        f'{m1}{_render_svg_arrow(r1_lbl, r1_col)}{m2}{_render_svg_arrow(r2_lbl, r2_col)}{m3}{_render_svg_arrow(r4_lbl, r4_col)}{m4_out}'
        f'</div></div>'
    )

    return {
        "the_quai": the_q,
        "dung_quai": dung_q,
        "ha_ho": ha_ho,
        "thuong_ho": thuong_ho,
        "bien_dung_quai": bien_dung_q,
        "directed_edges": mh_edges,
        "flowchart_html": flowchart_html,
    }


def build_unified_causal_diagram_and_micro_audit(
    chart_data: Optional[Dict[str, Any]],
    luc_hao_data: Optional[Dict[str, Any]],
    mai_hoa_data: Optional[Dict[str, Any]],
    dung_than: str = "Bản Thân",
    topic: str = "Chung",
    question: str = "",
    target_cung: Optional[int] = None,
) -> Dict[str, Any]:
    """
    V130.0 MASTER SYNTHESIS:
    Kết nối đồng bộ toàn bộ dấu hiệu vi mô của Lục Hào + Kỳ Môn + Mai Hoa thành:
    1. Sơ đồ Mũi Tên Tác Động Nhân Quả Đa Tầng trực quan (HTML + SVG).
    2. Bảng Mũi Tên Vi Mô Từng Cặp Yếu Tố ([Nguồn] ──[Cơ chế]──► [Đích] ══► [Hệ quả chi tiết]).
    3. Sổ Kiểm Kê 100% Dấu Hiệu Không Bỏ Sót (Đủ 6/6 Hào Lục Hào & 9/9 Cung Kỳ Môn).
    4. Văn bản cấu trúc chuẩn cho AI Online & AI Offline suy luận không bỏ sót chi tiết nào.
    """
    ly_res = analyze_liuyao_exhaustive_micro_graph(
        luc_hao_data or {}, dung_than=dung_than, topic=topic, question=question, chart_data=chart_data
    )
    qm_res = analyze_qimen_exhaustive_micro_graph(
        chart_data or {}, target_cung=target_cung, dung_than=dung_than, topic=topic, question=question
    )
    mh_res = analyze_meihua_exhaustive_micro_graph(
        mai_hoa_data or {}, chart_data=chart_data, topic=topic, question=question
    )

    all_edges = list(ly_res["directed_edges"]) + list(qm_res["directed_edges"]) + list(mh_res["directed_edges"])

    # Giao thoa Tín Hiệu Vi Mô Tam Thức (Cross-System Micro Resonance)
    resonances: List[str] = []
    tc = qm_res["target_cung"]
    qm_tc_audit = qm_res["palace_micro_audit"].get(tc, {})
    dt_idx = ly_res["dt_hao_idx"]
    ly_dt_audit = ly_res["line_micro_audit"][dt_idx - 1]

    if ly_dt_audit["is_void"] and any("Tuần Không" in x for x in qm_tc_audit.get("tu_hai", [])):
        resonances.append("🔔 <b>Đồng bộ Không Vong Kép (Lục Hào + Kỳ Môn cùng báo Không):</b> Cả Hào Dụng Thần lẫn Cung Dụng Thần đều lâm Tuần Không — hiện trạng chưa chín muồi hoặc thông tin chưa có thật 100%, bắt buộc đợi ngày Xuất/Xung Không mới thành thực chất.")
    if ("Dịch Mã" in ly_dt_audit["shensha"] or ly_dt_audit["is_moving"] or ly_dt_audit["is_am_dong"]) and any("Dịch Mã" in x for x in qm_tc_audit.get("good_signs", [])):
        resonances.append("🐎 <b>Đồng bộ Song Mã Gia Tốc:</b> Lục Hào Động/Dịch Mã hội cùng Mã Tinh Kỳ Môn — sự việc biến chuyển tốc độ cực nhanh, có yếu tố đi lại/chuyển khoản/tin báo đến sớm.")
    if not ly_res["quai_than"]["is_present"] or qm_tc_audit.get("am_can") in ("Kỷ", "Quý"):
        resonances.append(f"🕵️ <b>Tín hiệu Ẩn Tình Vi Mô:</b> Quái Thân ({ly_res['quai_than']['status_str']}) đối ứng Ám Can [{qm_tc_audit.get('am_can', '')}] ({qm_tc_audit.get('am_can_meaning', '')}) — tồn tại chi tiết ngầm phía sau chưa nói hết ra mặt.")
    if ly_res["global_formations"]:
        resonances.extend(f"⚡ <b>Cục diện Lục Hào Đặc Biệt:</b> {gf}" for gf in ly_res["global_formations"])
    if qm_tc_audit.get("tu_hai"):
        resonances.append(f"⚠️ <b>Kiểm định Tứ Hại Kỳ Môn tại Cung {tc}:</b> {'; '.join(qm_tc_audit['tu_hai'])}.")
    if not resonances:
        resonances.append(f"✅ <b>Tam Thức Vi Mô Thuận Khí:</b> Quái Thân ({ly_res['quai_than']['status_str']}), Ám Can [{qm_tc_audit.get('am_can', '')}] ({qm_tc_audit.get('am_can_meaning', '')}) và chuỗi Lật Cung Kỳ Môn ({' ➔ '.join('Cung ' + str(x) for x in qm_res['phien_cung_chain'])}) vận hành rõ ràng, không vướng xung hình ngầm.")

    edge_rows_html = "".join(
        f'<tr style="border-bottom:1px solid rgba(148,163,184,0.16);">'
        f'<td style="padding:5px 7px;color:#94a3b8;font-weight:700;white-space:nowrap;">{e.get("tier","")}</td>'
        f'<td style="padding:5px 7px;color:#f8fafc;font-weight:800;">{e.get("src","")}</td>'
        f'<td style="padding:5px 7px;white-space:nowrap;"><span style="padding:2px 8px;border-radius:999px;background:rgba(15,23,42,0.95);border:1px solid {e.get("color","#38bdf8")};color:{e.get("color","#38bdf8")};font-weight:800;font-size:0.84em;">━━[{e.get("rel","")}]━━►</span></td>'
        f'<td style="padding:5px 7px;color:#fde68a;font-weight:800;">{e.get("dst","")}</td>'
        f'<td style="padding:5px 7px;color:#e2e8f0;">══► {e.get("outcome","")}</td>'
        f'</tr>'
        for e in all_edges
    )

    lh_6_rows_html = "".join(
        f'<tr style="border-bottom:1px solid rgba(148,163,184,0.16);{"background:rgba(251,191,36,0.08);" if ln["roles"] else ""}">'
        f'<td style="padding:5px 7px;font-weight:800;color:#7dd3fc;white-space:nowrap;">Hào {ln["hao"]}'
        + (f'<br><span style="font-size:0.78em;color:#fde047;">{" · ".join(ln["roles"])}</span>' if ln["roles"] else "")
        + f'</td>'
        f'<td style="padding:5px 7px;color:#f8fafc;"><b>{ln["luc_than"]}</b><br><span style="font-size:0.84em;color:#cbd5e1;">{ln["can_chi_full"]} ({ln["nap_am"]})</span></td>'
        f'<td style="padding:5px 7px;color:#e2e8f0;">{ln["luc_thu"]}<br><span style="font-size:0.82em;color:#c4b5fd;">{", ".join(ln["shensha"]) or "—"}</span></td>'
        f'<td style="padding:5px 7px;color:#a7f3d0;">Nguyệt: <b>{ln["vuong_suy"]}</b><br>TS Ngày: <b>{ln["ts_ngay"]}</b></td>'
        f'<td style="padding:5px 7px;color:#fed7aa;font-size:0.85em;">{"<br>".join(ln["incoming_arrows"][:3] + ln["outgoing_arrows"][:2]) or ln["bien_summary"]}</td>'
        f'<td style="padding:5px 7px;color:#f1f5f9;">{ln["real_life_note"]}</td>'
        f'</tr>'
        for ln in reversed(ly_res["line_micro_audit"])
    )

    _clean_tu_hai_ok = '<span style="color:#4ade80;">✅ Không phạm Tứ Hại</span>'
    qm_9_rows_html = "".join(
        f'<tr style="border-bottom:1px solid rgba(148,163,184,0.16);{"background:rgba(251,191,36,0.10);" if p_idx == tc else ""}">'
        f'<td style="padding:5px 7px;font-weight:800;color:#fde047;white-space:nowrap;">Cung {p_idx} {pa["quai"]}<br><span style="font-size:0.8em;color:#94a3b8;">{pa["huong"]} ({pa["ngu_hanh"]})</span></td>'
        f'<td style="padding:5px 7px;color:#f8fafc;">Thiên: <b>{pa["can_thien_disp"]}</b> ({pa["ts_thien"]})<br>Địa: <b>{pa["can_dia_disp"]}</b> ({pa["ts_dia"]})</td>'
        f'<td style="padding:5px 7px;color:#c4b5fd;"><b>Ám Can: {pa["am_can"]}</b><br><span style="font-size:0.82em;color:#cbd5e1;">{pa["am_can_meaning"]}</span></td>'
        f'<td style="padding:5px 7px;color:#7dd3fc;">{pa["star"]}<br>{pa["door"]} · {pa["deity"]}</td>'
        f'<td style="padding:5px 7px;color:#fca5a5;font-size:0.85em;">{"; ".join(pa["tu_hai"]) if pa["tu_hai"] else _clean_tu_hai_ok}'
        + (f'<br><span style="color:#86efac;">{"; ".join(pa["good_signs"])}</span>' if pa["good_signs"] else "")
        + f'</td></tr>'
        for p_idx, pa in qm_res["palace_micro_audit"].items()
    )

    res_items_html = "".join(f'<div style="margin:3px 0;font-size:0.87em;color:#f1f5f9;line-height:1.48;">• {r}</div>' for r in resonances)

    visual_flowchart_html = (
        f'<div style="margin-top:12px;padding:13px 15px;background:linear-gradient(135deg,rgba(9,13,26,0.96),rgba(23,37,84,0.92));border-radius:13px;border:1.5px solid #38bdf8;box-shadow:0 4px 18px rgba(14,165,233,0.2);">'
        f'<div style="font-size:0.96em;font-weight:900;color:#fde047;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>🗺️ SƠ ĐỒ MŨI TÊN TÁC ĐỘNG NHÂN QUẢ CHI TIẾT & KIỂM KÊ VI MÔ 100% DẤU HIỆU QUẺ (V130.0)</span>'
        f'<span style="font-size:0.78em;color:#bae6fd;background:rgba(56,189,248,0.16);padding:2px 9px;border-radius:999px;border:1px solid rgba(56,189,248,0.4);">Đối chuẩn 元亨利贞 china95 · 问真六爻/奇门 · Không bỏ sót 1 chi tiết nhỏ</span>'
        f'</div>'
        f'{ly_res["flowchart_html"]}'
        f'{qm_res["flowchart_html"]}'
        f'{mh_res["flowchart_html"]}'
        f'<div style="padding:9px 12px;background:rgba(15,23,42,0.9);border-radius:9px;border-left:4px solid #a78bfa;margin-bottom:8px;">'
        f'<div style="font-size:0.85em;font-weight:900;color:#c4b5fd;margin-bottom:3px;">🔎 TỔNG HỢP TÍN HIỆU VI MÔ & GIAO THOA TAM THỨC TRÊN QUẺ NÀY</div>'
        f'{res_items_html}'
        f'</div>'
        f'<details style="background:rgba(15,23,42,0.94);border:1px solid rgba(251,191,36,0.38);border-radius:9px;padding:8px 11px;">'
        f'<summary style="cursor:pointer;font-weight:800;color:#fde047;font-size:0.88em;">'
        f'🏹 MỞ XEM TRỌN BỘ {len(all_edges)} MŨI TÊN NHÂN QUẢ CHI TIẾT + KIỂM KÊ ĐỦ 6/6 HÀO (THẦN SÁT · NẠP ÂM) & 9/9 CUNG (ÁM CAN · KÝ CAN · TỨ HẠI)'
        f'</summary>'
        f'<div style="margin-top:10px;overflow-x:auto;">'
        f'<div style="font-weight:800;color:#38bdf8;font-size:0.88em;margin-bottom:4px;">1️⃣ BẢNG MŨI TÊN TÁC ĐỘNG NHÂN QUẢ TỪNG YẾU TỐ ([Yếu tố A] ━━► [Yếu tố B] ══► [Kết quả thực tế])</div>'
        f'<table style="width:100%;border-collapse:collapse;font-size:0.83em;text-align:left;margin-bottom:12px;">'
        f'<thead><tr style="background:rgba(56,189,248,0.16);color:#7dd3fc;"><th style="padding:5px 7px;">Tầng</th><th style="padding:5px 7px;">Yếu Tố Tác Động (A)</th><th style="padding:5px 7px;">Mũi Tên Cơ Chế</th><th style="padding:5px 7px;">Yếu Tố Chịu Tác Động (B)</th><th style="padding:5px 7px;">Kết Quả Chi Tiết Thực Tế</th></tr></thead>'
        f'<tbody>{edge_rows_html}</tbody></table>'
        f'<div style="font-weight:800;color:#a7f3d0;font-size:0.88em;margin-bottom:4px;">2️⃣ SỔ KIỂM KÊ ĐẦY ĐỦ 6/6 HÀO LỤC HÀO (Hào Vị · Kinh Phòng Nạp Âm · 12 Thần Sát · 12 Trường Sinh · Mũi Tên Tác Động)</div>'
        f'<table style="width:100%;border-collapse:collapse;font-size:0.82em;text-align:left;margin-bottom:12px;">'
        f'<thead><tr style="background:rgba(16,185,129,0.16);color:#6ee7b7;"><th style="padding:5px 7px;">Hào & Vai Trò</th><th style="padding:5px 7px;">Lục Thân & Nạp Âm</th><th style="padding:5px 7px;">Lục Thú & 12 Thần Sát</th><th style="padding:5px 7px;">Khí Lực</th><th style="padding:5px 7px;">Mũi Tên Vào/Ra</th><th style="padding:5px 7px;">Ý Nghĩa Chi Tiết Từng Hào</th></tr></thead>'
        f'<tbody>{lh_6_rows_html}</tbody></table>'
        f'<div style="font-weight:800;color:#fde047;font-size:0.88em;margin-bottom:4px;">3️⃣ SỔ KIỂM KÊ ĐẦY ĐỦ 9/9 CUNG KỲ MÔN (Ký Cung Song Can · Ám Can 暗干 · 12 Trường Sinh · Tứ Hại)</div>'
        f'<table style="width:100%;border-collapse:collapse;font-size:0.82em;text-align:left;">'
        f'<thead><tr style="background:rgba(251,191,36,0.16);color:#fde047;"><th style="padding:5px 7px;">Cung Vị</th><th style="padding:5px 7px;">Thiên/Địa Can (+Ký Can)</th><th style="padding:5px 7px;">Ám Can (Ẩn Ý)</th><th style="padding:5px 7px;">Tinh · Môn · Thần</th><th style="padding:5px 7px;">Kiểm Định Tứ Hại & Cát Tín</th></tr></thead>'
        f'<tbody>{qm_9_rows_html}</tbody></table>'
        f'</div></details></div>'
    )

    prompt_arrows_lines = [
        f"   * [{e['tier']}] {e['src']} ──[{e['rel']}]──► {e['dst']} ══► {e['outcome']}"
        for e in all_edges[:14]
    ]
    prompt_micro_chain_text = (
        "=== MẠNG LƯỚI MŨI TÊN NHÂN QUẢ VI MÔ V130.0 (CHUẨN NGUYÊN HANH LỢI TRINH & VẤN CHÂN — BẮT BUỘC DÙNG ĐỂ LUẬN SÂU KHÔNG BỎ SÓT CHI TIẾT) ===\n"
        f"- Quái Thân Lục Hào: {ly_res['quai_than']['status_str']} ({ly_res['quai_than']['meaning']}) | Thế Thân: {ly_res['the_than']['status_str']}.\n"
        f"- Kỳ Môn Ký Cung & Ám Can: Cung Dụng Thần {tc} có Thiên/Địa Can {qm_tc_audit.get('can_thien_disp','')}/{qm_tc_audit.get('can_dia_disp','')}, Ám Can [{qm_tc_audit.get('am_can','')}] ({qm_tc_audit.get('am_can_meaning','')}), Tứ Hại: {', '.join(qm_tc_audit.get('tu_hai',[])) or 'Không phạm'}.\n"
        f"- Chuỗi Lật Cung Kỳ Môn 4 Trạm (Quá khứ -> Hiện tại -> Kế tiếp -> Kết cục): {' ──► '.join('Cung ' + str(x) + ' (' + qm_res['palace_micro_audit'][x]['door'] + ')' for x in qm_res['phien_cung_chain'])}.\n"
        f"- Mai Hoa 4 Chặng: Thể {mh_res['the_quai']} ↔ Dụng {mh_res['dung_quai']} ──► Hạ Hỗ {mh_res['ha_ho']} ──► Thượng Hỗ {mh_res['thuong_ho']} ──► Biến Dụng {mh_res['bien_dung_quai']}.\n"
        + "\n".join(prompt_arrows_lines)
    )

    return {
        "liuyao_micro": ly_res,
        "qimen_micro": qm_res,
        "meihua_micro": mh_res,
        "all_directed_edges": all_edges,
        "resonances": resonances,
        "visual_flowchart_html": visual_flowchart_html,
        "prompt_micro_chain_text": prompt_micro_chain_text,
    }

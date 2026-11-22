# -*- coding: utf-8 -*-
"""
CHINESE MASTER MICRO-SIGN & DIRECTED CAUSAL GRAPH ENGINE (V143.0)
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
MO_BY_EL = {"Kim": "Sửu", "Mộc": "Mùi", "Thủy": "Thìn", "Thổ": "Thìn", "Hỏa": "Tuất"}

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


def _render_outcome_box(
    title: str,
    detail: str,
    verdict_color: str = "#fbbf24",
    header_badge: str = "══► KẾT QUẢ GIẢI ĐÁP CÂU HỎI CHÍNH",
) -> str:
    return (
        f'<div style="flex:1.35 1 235px;min-width:210px;padding:9px 12px;background:linear-gradient(135deg,rgba(30,41,59,0.97),rgba(15,23,42,0.97));border:2px solid {verdict_color};border-radius:10px;box-shadow:0 3px 14px rgba(251,191,36,0.22);">'
        f'<div style="font-size:0.74em;font-weight:900;color:{verdict_color};margin-bottom:3px;letter-spacing:0.2px;">{header_badge}</div>'
        f'<div style="font-size:0.89em;font-weight:900;color:#ffffff;line-height:1.35;">{title}</div>'
        f'<div style="font-size:0.79em;color:#fef3c7;margin-top:4px;line-height:1.44;">{detail}</div>'
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

    # Định vị Hào Dụng Thần (hoặc Phục Thần nếu Dụng Thần ẩn!) — V134.0 Chuẩn Tăng San Bốc Dịch · Dụng Thần Lưỡng Hiện Chương
    dt_clean = str(dung_than or "Bản Thân").strip()
    is_self_dt = dt_clean in ("Bản Thân", "Hào Thế", "Dụng Thần", "")
    dt_hao_idx = the_pos
    dt_candidates = []
    for idx_h, h_obj in enumerate(haos_ban[:6], 1):
        lt_h = str(h_obj.get("luc_than") or "")
        if not is_self_dt and (lt_h == dt_clean or dt_clean in lt_h):
            dt_candidates.append(idx_h)
    if dt_candidates:
        _vs_rank = {"Vượng": 0, "Tướng": 1, "Bình": 2, "Hưu": 3, "Tù": 4, "Tử": 5}

        def _dt_cand_priority(ix: int):
            ho = haos_ban[ix - 1]
            ch_c = _norm_chi(ho.get("chi") or str(ho.get("can_chi", "")).split("-")[0])
            hf_c = set(ho.get("hoa_flags") or [])
            is_act = (ix in dong_set) or bool(ho.get("is_am_dong"))
            is_self_destruct = ("HOI_DAU_KHAC" in hf_c) or ("HOA_THOAI" in hf_c)
            is_broken_static = (not is_act) and (
                bool(ho.get("is_nguyet_pha")) or bool(ho.get("is_nhat_pha")) or ho.get("khong_type") == "CHAN_KHONG"
            )
            lam_cal = 0 if ch_c in (chi_thang, chi_ngay) else 1
            vs_r = _vs_rank.get(str(ho.get("strength") or ho.get("vuong_suy") or "Bình"), 2)
            pos_r = 0 if ix == the_pos else (1 if ix == ung_pos else 2)
            # Xếp hạng: (1) Không bị Tĩnh Phá/Chân Không khi có hào lành lặn khác, (2) Động hữu lực, (3) Lâm Nhật/Nguyệt, (4) Thế/Ứng, (5) Vượng Suy, (6) Gần Thế
            return (
                1 if is_broken_static else 0,
                0 if (is_act and not is_self_destruct) else (1 if is_act else 2),
                lam_cal,
                pos_r,
                vs_r,
                abs(ix - the_pos),
            )

        dt_candidates_sorted = sorted(dt_candidates, key=_dt_cand_priority)
        dt_hao_idx = dt_candidates_sorted[0]

    phuc_list = lh.get("phuc_than") or []
    dt_phuc_obj = None
    if not is_self_dt and not dt_candidates:
        for pt in phuc_list:
            if isinstance(pt, dict) and str(pt.get("luc_than", "")) == dt_clean:
                dt_phuc_obj = pt
                dt_hao_idx = int(pt.get("hao_pos", the_pos))
                break

    # Kiểm tra Tam Hợp Cục & Tam Hình 3 chữ toàn bàn (V133.0: Chuẩn Tăng San Bốc Dịch — Tĩnh Hào Bất Hợp Cục!)
    active_branches = {chi_thang, chi_ngay}
    moving_only_branches = set()
    for idx_h, h_obj in enumerate(haos_ban[:6], 1):
        ch_b = _norm_chi(h_obj.get("chi") or str(h_obj.get("can_chi", "")).split("-")[0])
        if idx_h in dong_set or h_obj.get("is_am_dong"):
            if ch_b:
                active_branches.add(ch_b)
                moving_only_branches.add(ch_b)
        if idx_h in dong_set and idx_h <= len(haos_bien):
            ch_bi = _norm_chi(haos_bien[idx_h - 1].get("chi") or str(haos_bien[idx_h - 1].get("can_chi", "")).split("-")[0])
            if ch_bi:
                active_branches.add(ch_bi)

    global_formations = []
    tam_hop_from_lh = lh.get("tam_hop_cuc") or []
    if tam_hop_from_lh:
        for th_item in tam_hop_from_lh:
            global_formations.append(
                f"🔗 Tam Hợp Thành Hóa ({th_item.get('label', '')} ➔ {th_item.get('luc_than', '')} hành {th_item.get('element', '')}): Hội tụ khí lực đại cục không thể phá!"
            )
    else:
        for req_set, th_el, mid_b in TAM_HOP_CUC:
            if req_set.issubset(active_branches) and len(req_set & moving_only_branches) >= 2:
                global_formations.append(f"🔗 Tam Hợp {th_el} Cục ({'-'.join(sorted(req_set))}) hội tụ khí lực cực mạnh hướng về hành {th_el}")
    if {"Dần", "Tị", "Thân"}.issubset(active_branches) and len({"Dần", "Tị", "Thân"} & moving_only_branches) >= 1:
        global_formations.append("⚠️ Hội đủ Tam Hình Vô Ân/Ỷ Thế (Dần–Tị–Thân): Cảnh báo va chạm pháp lý, cạnh tranh gay gắt hoặc trục trặc đường đi/thủ tục")
    if {"Sửu", "Tuất", "Mùi"}.issubset(active_branches) and len({"Sửu", "Tuất", "Mùi"} & moving_only_branches) >= 1:
        global_formations.append("⚠️ Hội đủ Tam Hình Trì Thế (Sửu–Tuất–Mùi): Cảnh báo nội bộ giằng co dây dưa, áp lực tâm lý hoặc chậm giải ngân/giấy tờ")
    for ld_chain in (lh.get("lien_dong_chains") or []):
        global_formations.append(f"🔄 Liên Động Thông Quan: {ld_chain}")

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
            if "HOA_KHONG" in hflags:
                directed_edges.append({
                    "tier": "Tầng 3 · Biến Hào",
                    "src": f"Hào Biến {idx_h} ({ch_b} · Tuần Không)",
                    "rel": "Động Hóa Tuần Không",
                    "color": "#ef4444",
                    "dst": f"Hào Động {idx_h} {lt_h} ({ch_h}-{el_h})",
                    "outcome": f"Tăng San Bốc Dịch: 'Động bất vi Không, Hóa Không phản Không' — Hào {idx_h} phát động nhưng hóa vào Không Vong ({ch_b}), chưa Xuất Không thì sự việc hóa rỗng.",
                    "delta": -24,
                })
                incoming_arrows.append(f"Hào Biến {ch_b} ──[Hóa Không Vong]──►")
            if "HOA_NGUYET_PHA" in hflags or "HOA_NHAT_PHA" in hflags:
                pha_kind = "Nguyệt Phá" if "HOA_NGUYET_PHA" in hflags else "Nhật Phá"
                directed_edges.append({
                    "tier": "Tầng 3 · Biến Hào",
                    "src": f"Hào Biến {idx_h} ({ch_b} · {pha_kind})",
                    "rel": f"Động Hóa {pha_kind}",
                    "color": "#ef4444",
                    "dst": f"Hào Động {idx_h} {lt_h} ({ch_h}-{el_h})",
                    "outcome": f"Hào {idx_h} động hóa {ch_b} bị {pha_kind} ('Như thực mộc vô căn') — kết cục dễ đứt gãy hoặc hụt hẫng nếu không chờ ngày Thực Phá.",
                    "delta": -22,
                })
                incoming_arrows.append(f"Hào Biến {ch_b} ──[Hóa {pha_kind}]──►")

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

        ch_bien_ln = _norm_chi(hb_obj.get("chi") or str(hb_obj.get("can_chi", "")).split("-")[0]) if (is_mv and hb_obj) else ""
        el_bien_ln = str(hb_obj.get("ngu_hanh") or CHI_ELEMENT.get(ch_bien_ln, "")) if (is_mv and hb_obj) else ""
        lt_bien_ln = str(hb_obj.get("luc_than") or "") if (is_mv and hb_obj) else ""

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
            "is_xung_khong": bool(h_obj.get("is_xung_khong")),
            "has_nguyet_root": bool(h_obj.get("has_nguyet_root")),
            "is_void": is_void,
            "khong_type": k_type,
            "is_nguyet_pha": bool(h_obj.get("is_nguyet_pha")),
            "is_nhat_pha": bool(h_obj.get("is_nhat_pha")),
            "hop_status": str(h_obj.get("hop_status") or ""),
            "mo_type": str(h_obj.get("mo_type") or ""),
            "is_tao_tho_thoi_kim": bool(h_obj.get("is_tao_tho_thoi_kim")),
            "hoa_flags": list(h_obj.get("hoa_flags") or []),
            "bien_chi": ch_bien_ln,
            "bien_el": el_bien_ln,
            "bien_luc_than": lt_bien_ln,
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

    def _build_lh_flowchart(custom_out_node: Optional[str] = None) -> str:
        _onode = custom_out_node or out_node_lh
        return (
            f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:11px;border:1px solid rgba(56,189,248,0.35);margin-bottom:8px;">'
            f'<div style="font-size:0.86em;font-weight:900;color:#7dd3fc;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
            f'<span>☯️ SƠ ĐỒ 1 · LỤC HÀO 4 TẦNG TÁC ĐỘNG ══► GIẢI ĐÁP CÂU HỎI TỪ TÁC ĐỘNG CÁC HÀO</span>'
            f'<span style="color:#fde68a;font-size:0.88em;">Quái Thân: {bodies_ss["quai_than"]["chi"]}-{bodies_ss["quai_than"]["luc_than"]} | Thế Thân: Hào {bodies_ss["the_than"]["hao"]}</span>'
            f'</div>'
            f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
            f'{t1_node}{_render_svg_arrow(arrow_12_lbl, "#38bdf8")}{t2_node}{_render_svg_arrow(arrow_23_lbl, arrow_23_col)}{t3_node}{_render_svg_arrow("Tác động ra Kết Quả", "#fbbf24")}{_onode}'
            f'</div></div>'
        )

    flowchart_html = _build_lh_flowchart()

    return {
        "ban_name": ban_name,
        "bien_name": bien_name,
        "palace": palace,
        "palace_el": p_el,
        "chi_thang": chi_thang,
        "chi_ngay": chi_ngay,
        "dt_clean": dt_clean,
        "is_self_dt": is_self_dt,
        "dt_candidates": dt_candidates,
        "dt_phuc_obj": dt_phuc_obj,
        "ban_is_luc_xung": bool(lh.get("ban_is_luc_xung")),
        "ban_is_luc_hop": bool(lh.get("ban_is_luc_hop")),
        "bien_is_luc_xung": bool(lh.get("bien_is_luc_xung")),
        "bien_is_luc_hop": bool(lh.get("bien_is_luc_hop")),
        "xung_hop_transition": str(lh.get("xung_hop_transition") or ""),
        "quai_bien_rel": str(lh.get("quai_bien_rel") or ""),
        "tam_hop_cuc": list(lh.get("tam_hop_cuc") or []),
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
        "render_flowchart_fn": _build_lh_flowchart,
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

    def _find_outer_by(src_map: Dict[Any, Any], kw: str) -> int:
        for _p in (1, 2, 3, 4, 6, 7, 8, 9):
            _v = str(src_map.get(_p) or src_map.get(str(_p)) or "")
            if kw in _v:
                return _p
        return 0

    p_sinh = _find_outer_by(nb, "Sinh")
    p_khai = _find_outer_by(nb, "Khai")
    p_canh = _find_outer_by(nb, "Cảnh")
    p_thuong = _find_outer_by(nb, "Thương")
    p_nhue = _find_outer_by(tb, "Nhuế")
    p_tam = _find_outer_by(tb, "Tâm")
    p_luchop = _find_outer_by(sb, "Hợp")
    p_mau, _, _ = find_qimen_stem_palace(cd, "Mậu", chi_gio, "heaven")
    p_mau = p_mau or cung_chu

    # Kiểm tra Đại Cục Phục Ngâm / Phản Ngâm chuẩn《御定奇门宝鉴》&《神奇之门》:
    is_mon_phuc_ngam = (p_khai == 6 or p_sinh == 8)
    is_mon_phan_ngam = (p_khai == 4 or p_sinh == 2)
    is_tinh_phuc_ngam = (_find_outer_by(tb, "Tâm") == 6 or _find_outer_by(tb, "Bồng") == 1)
    is_tinh_phan_ngam = (_find_outer_by(tb, "Tâm") == 4 or _find_outer_by(tb, "Bồng") == 9)

    q_qm = f"{question} {topic}".lower()
    qm_dt_role = "GENERAL"
    tc = int(target_cung) if str(target_cung).isdigit() and 1 <= int(target_cung) <= 9 else 0
    if tc == 5:
        tc = int(cd.get("p_nhue_cam") or 2)
    if not tc:
        # Phân luồng Dụng Thần Kỳ Môn chuẩn《御定奇门宝鉴》& Vấn Chân Kỳ Môn (qm_router):
        # Nhật Can (cung_chu) = Người hỏi; Thời Can (cung_khach) = Sự việc/Hành trình; kết hợp Chuyên Đề Dụng Thần:
        if any(w in q_qm for w in ("đòi nợ", "thu nợ", "khoản nợ", "thu hồi nợ", "công nợ")):
            qm_dt_role = "DEBT"
            tc = cung_khach
        elif any(w in q_qm for w in ("tiền", "tài lộc", "lãi", "lời", "đầu tư", "kinh doanh", "mở xưởng", "mua lô hàng", "mua hàng", "doanh thu", "lợi nhuận", "buôn bán", "thương vụ", "cầu tài", "hợp tác làm ăn")):
            qm_dt_role = "WEALTH"
            tc = p_sinh or cung_khach
        elif any(w in q_qm for w in ("xin việc", "ứng tuyển", "chức vụ", "thăng chức", "bổ nhiệm", "công danh", "tuyển dụng", "sự nghiệp")):
            qm_dt_role = "CAREER"
            tc = p_khai or cung_khach
        elif any(w in q_qm for w in ("thi cử", "khoa cử", "đỗ đạt", "văn thư", "giấy tờ", "chứng chỉ", "bằng cấp", "visa", "ký hợp đồng")):
            qm_dt_role = "EXAM"
            tc = p_canh or cung_khach
        elif any(w in q_qm for w in ("hôn sự", "kết hôn", "cưới", "nhân duyên", "tình cảm", "hẹn hò")):
            qm_dt_role = "MARRIAGE"
            tc = p_luchop or cung_khach
        elif any(w in q_qm for w in ("bệnh", "ốm", "điều trị", "chữa", "phẫu thuật")):
            qm_dt_role = "ILLNESS"
            tc = p_tam or cung_khach
        else:
            qm_dt_role = "GENERAL"
            tc = cung_khach

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
        "Ất": {2}, "Bính": {6}, "Mậu": {6}, "Đinh": {8}, "Kỷ": {8},
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

    def _build_km_flowchart(custom_out_node: Optional[str] = None) -> str:
        _onode_k = custom_out_node or out_km
        return (
            f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:11px;border:1px solid rgba(251,191,36,0.35);margin-bottom:8px;">'
            f'<div style="font-size:0.86em;font-weight:900;color:#fde047;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
            f'<span>🧭 SƠ ĐỒ 2 · KỲ MÔN CHỦ–KHÁCH & LẬT CUNG 4 TRẠM ══► GIẢI ĐÁP CÂU HỎI TỪ TÁC ĐỘNG CỬU CUNG</span>'
            f'<span style="color:#a7f3d0;font-size:0.88em;">Chủ: Cung {cung_chu} ({stem_chu}) ↔ Sự việc: Cung {tc} ({st_cur["can_thien_disp"]}) | Ký Cung 5: {cd.get("stem_trung_cung_5", "Mậu")}➔Cung {cd.get("p_nhue_cam", 2)}</span>'
            f'</div>'
            f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
            f'{n1_box}{_ar_km_1}{n2_box}{_ar_km_2}{n3_box}{_ar_km_3}{_onode_k}'
            f'</div></div>'
        )

    flowchart_html = _build_km_flowchart()

    return {
        "target_cung": tc,
        "qm_dt_role": qm_dt_role,
        "cung_chu": cung_chu,
        "cung_khach": cung_khach,
        "cung_truc_su": cung_truc_su,
        "p_sinh": p_sinh,
        "p_khai": p_khai,
        "p_canh": p_canh,
        "p_thuong": p_thuong,
        "p_nhue": p_nhue,
        "p_tam": p_tam,
        "p_luchop": p_luchop,
        "p_mau": p_mau,
        "is_mon_phuc_ngam": is_mon_phuc_ngam,
        "is_mon_phan_ngam": is_mon_phan_ngam,
        "is_tinh_phuc_ngam": is_tinh_phuc_ngam,
        "is_tinh_phan_ngam": is_tinh_phan_ngam,
        "truc_su_door": str(cd.get("truc_su") or ""),
        "stem_chu": stem_chu,
        "stem_khach": stem_khach,
        "ck_rel": ck_rel,
        "ck_desc": ck_desc,
        "phien_cung_chain": [p_past, tc, p_next1, p_next2],
        "palace_micro_audit": palace_micro_audit,
        "directed_edges": qimen_edges,
        "flowchart_html": flowchart_html,
        "render_flowchart_fn": _build_km_flowchart,
    }


def analyze_meihua_exhaustive_micro_graph(
    mai_hoa_data: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    topic: str = "Chung",
    question: str = "",
    luc_hao_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    V133.2: Phân tích Mai Hoa Dịch Số 4 Chặng Tiến Hóa (Bản Quái ──► Hạ Hỗ [2-3-4] ──► Thượng Hỗ [3-4-5] ──► Biến Quái + Hào Từ).
    Đồng bộ hoàn toàn với Lục Hào Đa Hào Động (0..6 hào động) để Quẻ Biến trên sơ đồ Mai Hoa và Lục Hào khớp 100%!
    """
    mh = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
    cd = chart_data if isinstance(chart_data, dict) else {}
    lh = luc_hao_data if isinstance(luc_hao_data, dict) else {}
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
    _lh_ban_d = lh.get("ban") if isinstance(lh.get("ban"), dict) else {}
    _lh_lines_raw = _lh_ban_d.get("lines") or [
        int(h.get("line", 0)) for h in (_lh_ban_d.get("haos") or []) if isinstance(h, dict) and "line" in h
    ]
    if not mh and len(_lh_lines_raw) == 6:
        lines6 = [int(x) for x in _lh_lines_raw]
        lo_q = BIN_TO_TRIGRAM_8.get(tuple(lines6[:3]), lo_q)
        up_q = BIN_TO_TRIGRAM_8.get(tuple(lines6[3:]), up_q)
        _lh_same_hex = True
    else:
        _lh_same_hex = len(_lh_lines_raw) == 6 and [int(x) for x in _lh_lines_raw] == lines6

    if _lh_same_hex and isinstance(lh.get("dong_hao"), list):
        dong_list_mh = [int(x) for x in lh["dong_hao"] if str(x).isdigit() and 1 <= int(x) <= 6]
    else:
        dong_list_mh = [dong_hao]

    lines_bien = list(lines6)
    for d_idx in dong_list_mh:
        lines_bien[d_idx - 1] = 0 if lines_bien[d_idx - 1] == 1 else 1

    ha_ho = BIN_TO_TRIGRAM_8.get(tuple(lines6[1:4]), "Cấn")
    thuong_ho = BIN_TO_TRIGRAM_8.get(tuple(lines6[2:5]), "Tốn")
    lo_bien = BIN_TO_TRIGRAM_8.get(tuple(lines_bien[:3]), lo_q)
    up_bien = BIN_TO_TRIGRAM_8.get(tuple(lines_bien[3:]), up_q)

    # Nếu Quẻ Tĩnh (0 hào động), lấy quẻ chứa Hào Thế làm Thể; nếu có hào động, lấy quẻ tĩnh/ít hào động hơn làm Thể
    low_mv_cnt = sum(1 for x in dong_list_mh if x <= 3)
    up_mv_cnt = sum(1 for x in dong_list_mh if x >= 4)
    if not dong_list_mh:
        _the_pos_mh = int(lh.get("the_pos") or _lh_ban_d.get("the_pos") or 3)
        if _the_pos_mh <= 3:
            the_q, dung_q, bien_dung_q = lo_q, up_q, up_bien
        else:
            the_q, dung_q, bien_dung_q = up_q, lo_q, lo_bien
    elif low_mv_cnt <= up_mv_cnt and up_mv_cnt > 0:
        the_q = lo_q
        dung_q = up_q
        bien_dung_q = up_bien if up_bien != up_q else lo_bien
    else:
        the_q = up_q
        dung_q = lo_q
        bien_dung_q = lo_bien if lo_bien != lo_q else up_bien

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

    lh_ban_nm = str(_lh_ban_d.get("name") or "") if _lh_same_hex else ""
    lh_bien_nm = str((lh.get("bien") or {}).get("name") or "") if _lh_same_hex else ""
    ten_chu = lh_ban_nm or str(mh.get("ten") or mh.get("ten_que") or f"{up_q}/{lo_q}")
    ten_ho = str(mh.get("ten_ho") or f"{thuong_ho}/{ha_ho}")
    ten_bien = lh_bien_nm or str(mh.get("ten_qua_bien") or mh.get("bien_que") or f"{up_bien}/{lo_bien}")
    sum_tien_thien = TRIGRAM_META_8[up_q][1] + TRIGRAM_META_8[lo_q][1]
    sum_hau_thien = TRIGRAM_META_8[up_q][2] + TRIGRAM_META_8[lo_q][2]
    dong_disp_mh = ", ".join(map(str, dong_list_mh)) if dong_list_mh else "Tĩnh (0 hào động)"

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
        f"Chặng 4 Kết Cục: {ten_bien} (Động Hào {dong_disp_mh})",
        f"{r4_desc} Định lượng Quái số: Tiên Thiên = {sum_tien_thien}, Hậu Thiên = {sum_hau_thien}.",
        r4_col,
    )

    def _build_mh_flowchart(custom_out_node: Optional[str] = None) -> str:
        _onode_m = custom_out_node or m4_out
        return (
            f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:11px;border:1px solid rgba(244,114,182,0.35);margin-bottom:8px;">'
            f'<div style="font-size:0.86em;font-weight:900;color:#f9a8d4;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
            f'<span>🌸 SƠ ĐỒ 3 · MAI HOA THỂ–DỤNG 4 CHẶNG ══► GIẢI ĐÁP CÂU HỎI TỪ TƯỢNG QUÁI & BIẾN QUÁI</span>'
            f'<span style="color:#fbcfe8;font-size:0.88em;">Thể: {the_q} ({el_the}) | Động Hào {dong_disp_mh}</span>'
            f'</div>'
            f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
            f'{m1}{_render_svg_arrow(r1_lbl, r1_col)}{m2}{_render_svg_arrow(r2_lbl, r2_col)}{m3}{_render_svg_arrow(r4_lbl, r4_col)}{_onode_m}'
            f'</div></div>'
        )

    flowchart_html = _build_mh_flowchart()

    return {
        "ten_chu": ten_chu,
        "ten_ho": ten_ho,
        "ten_bien": ten_bien,
        "up_q": up_q,
        "lo_q": lo_q,
        "up_bien": up_bien,
        "lo_bien": lo_bien,
        "dong_disp": dong_disp_mh,
        "the_quai": the_q,
        "dung_quai": dung_q,
        "ha_ho": ha_ho,
        "thuong_ho": thuong_ho,
        "bien_dung_quai": bien_dung_q,
        "r1_lbl": r1_lbl,
        "r4_lbl": r4_lbl,
        "r4_desc": r4_desc,
        "r4_col": r4_col,
        "sum_tien_thien": sum_tien_thien,
        "sum_hau_thien": sum_hau_thien,
        "directed_edges": mh_edges,
        "flowchart_html": flowchart_html,
        "render_flowchart_fn": _build_mh_flowchart,
    }


def score_option_classical_imagery(
    option_text: str,
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    option_index: int = 1,
) -> Tuple[int, List[str]]:
    """
    V131.0: Chấm điểm Vạn Vật Loại Tượng Thực Chiến (8 Quái × 5 Hành × 6 Lục Thân × 6 Hào Vị × 9 Tinh × 8 Môn × 8 Thần).
    TUYỆT ĐỐI KHÔNG DÙNG hashlib.md5! Mọi điểm số đều bắt nguồn 100% từ tượng quẻ thật.
    """
    t = str(option_text or "").lower().strip()
    pts = 0
    evs: List[str] = []

    tc = qm_res.get("target_cung", 2)
    pa = (qm_res.get("palace_micro_audit") or {}).get(tc, {})
    door = str(pa.get("door") or "")
    star = str(pa.get("star") or "")
    deity = str(pa.get("deity") or "")
    quai_cung = str(pa.get("quai") or "")
    am_can = str(pa.get("am_can") or "")

    the_q = str(mh_res.get("the_quai") or "Càn")
    dung_q = str(mh_res.get("dung_quai") or "Chấn")
    haho_q = str(mh_res.get("ha_ho") or "Cấn")
    thuongho_q = str(mh_res.get("thuong_ho") or "Tốn")
    biendung_q = str(mh_res.get("bien_dung_quai") or dung_q)
    active_trigs = [dung_q, biendung_q, the_q, haho_q, thuongho_q, quai_cung]
    focus_trigs = (dung_q, biendung_q, quai_cung)

    dt_idx = int(ly_res.get("dt_hao_idx") or 3)
    lines = ly_res.get("line_micro_audit") or []
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    dt_chi = str(dt_ln.get("chi") or "")
    dt_el = str(dt_ln.get("ngu_hanh") or "")
    moving_lines = [ln for ln in lines if ln.get("is_moving") or ln.get("is_am_dong")]
    moving_els = {str(ln.get("ngu_hanh") or "") for ln in moving_lines}
    moving_chis = {str(ln.get("chi") or "") for ln in moving_lines}
    moving_lts = {str(ln.get("luc_than") or "") for ln in moving_lines}

    def _has_kw(*kws: str) -> bool:
        for kw in kws:
            if re.search(rf"(?<![a-zA-ZÀ-ỹ]){re.escape(kw)}(?![a-zA-ZÀ-ỹ])", t):
                return True
        return False

    import re

    # 1. ẨM THỰC: MÓN NƯỚC (Phở, Bún, Miến, Mì nước, Cháo, Súp, Canh, Lẩu, Đồ uống) vs MÓN KHÔ (Cơm, Xôi, Bánh mì, Nướng, Chiên)
    if _has_kw("phở", "bún", "miến", "hủ tiếu", "bánh canh", "cháo", "súp", "canh", "lẩu", "mì nước", "món nước", "trà", "cà phê", "bia", "nước ngọt", "sữa"):
        w_cnt = sum(2 for q in focus_trigs if q in ("Khảm", "Đoài")) + sum(1 for q in active_trigs if q in ("Khảm", "Đoài"))
        if w_cnt > 0:
            pts += w_cnt * 9
            evs.append(f"Tượng Thủy/Trạch ({', '.join(q for q in focus_trigs if q in ('Khảm', 'Đoài')) or 'Khảm/Đoài'}) chủ món nước, canh thang, chất lỏng (ứng Phở/Bún/Lẩu)")
        if dt_el == "Thủy" or "Thủy" in moving_els or any(c in ("Tý", "Hợi") for c in moving_chis | {dt_chi}):
            pts += 18
            evs.append(f"Lục Hào vượng Thủy khí ({dt_chi or 'Hợi/Tý'}) ứng trực tiếp món có nước dùng nóng hổi")
        if "Hưu" in door or "Bồng" in star or am_can in ("Nhâm", "Quý"):
            pts += 14
            evs.append(f"Kỳ Môn hội {door}/{star} (Thủy khí) xác nhận món nước")

    if _has_kw("cơm", "cơm tấm", "cơm rang", "cơm văn phòng", "xôi", "bánh mì", "bánh bao", "đồ khô", "nướng", "chiên", "rán", "thịt quay"):
        d_cnt = sum(2 for q in focus_trigs if q in ("Khôn", "Cấn", "Ly")) + sum(1 for q in active_trigs if q in ("Khôn", "Cấn", "Ly"))
        if d_cnt > 0:
            pts += d_cnt * 8
            evs.append(f"Tượng Thổ/Hỏa ({', '.join(q for q in focus_trigs if q in ('Khôn', 'Cấn', 'Ly')) or 'Khôn/Ly'}) chủ hạt gạo chín khô, cơm tấm, đồ nướng/chiên")
        if dt_el in ("Thổ", "Hỏa") and "Khảm" not in (dung_q, biendung_q):
            pts += 15
            evs.append(f"Hào Dụng Thần mang hành {dt_el} (khô ráo/nhiệt Hỏa-Thổ), không phải món nước")
        if any(x in door for x in ("Sinh", "Tử", "Cảnh")) or "Anh" in star or "Nhậm" in star:
            pts += 12
            evs.append(f"Kỳ Môn hội {door}/{star} (Thổ/Hỏa) ứng món cơm/nướng khô")

    # 2. THỰC PHẨM CỤ THỂ: THỊT LỢN/HEO vs CÁ/HẢI SẢN vs BÒ vs GÀ vs RAU CỦ
    if _has_kw("thịt lợn", "thịt heo", "lợn", "heo", "sườn", "ba chỉ", "giò"):
        if "Khảm" in active_trigs or "Hợi" in (moving_chis | {dt_chi}):
            pts += 24
            evs.append("Quẻ Khảm / Địa Chi Hợi trong Vạn Vật Loại Tượng đích danh là Lợn (Thủy súc / Hợi Trư)")
        elif "Khôn" in focus_trigs or "Đoài" in focus_trigs:
            pts += 10
            evs.append("Tượng Khôn/Đoài ứng thịt gia súc cắt miếng")
    if _has_kw("cá", "hải sản", "tôm", "cua", "mực", "ốc"):
        if "Tốn" in active_trigs or ("Khảm" in active_trigs and "Tốn" in active_trigs) or any(c in ("Thìn", "Tị") for c in (moving_chis | {dt_chi})):
            pts += 25
            evs.append("Quẻ Tốn (Thuyết Quái Truyện: Tốn vi Ngư = Con Cá) / Thìn Thủy khố ứng đích danh Cá & Hải sản")
        elif "Đoài" in focus_trigs or "Hưu" in door:
            pts += 12
            evs.append("Đoài Trạch / Hưu Môn (ao đầm sông nước) ứng thủy sản, tôm cá")
    if _has_kw("bò", "thịt bò", "phở bò", "bít tết", "trâu"):
        if "Khôn" in active_trigs or "Sửu" in (moving_chis | {dt_chi}):
            pts += 20
            evs.append("Quẻ Khôn (Khôn vi Tử Mẫu Ngưu = Con Bò) / Địa Chi Sửu ứng thịt bò")
    if _has_kw("gà", "thịt gà", "vịt", "ngan", "chim", "trứng"):
        if "Đoài" in active_trigs or "Dậu" in (moving_chis | {dt_chi}) or "Ly" in focus_trigs:
            pts += 22
            evs.append("Địa Chi Dậu / Đoài-Ly (Dậu Kê = Gà, gia cầm có cánh) ứng thịt gà/vịt")
    if _has_kw("rau", "củ", "quả", "trái cây", "chay", "đậu"):
        if any(q in ("Chấn", "Tốn") for q in focus_trigs) or dt_el == "Mộc":
            pts += 22
            evs.append("Tượng Chấn/Tốn Thảo Mộc ứng rau củ quả, đồ chay thanh đạm")

    # 3. VỊ TRÍ TRONG NHÀ / ĐỒ VẬT: GIƯỜNG / PHÒNG NGỦ / TRONG TÚI vs BÀN PHÒNG KHÁCH / NGOÀI SẢNH
    if _has_kw("giường", "trên giường", "phòng ngủ", "chăn", "gối", "nệm", "đệm", "trong phòng", "trong tủ", "trong túi", "ngăn kéo"):
        if dt_idx in (1, 2, 3):
            pts += 20
            evs.append(f"Dụng Thần đóng tại Hào {dt_idx} (Nội Quái = phòng riêng tư bên trong, giường ngủ/ngăn kín)")
        if any(q in ("Khôn", "Cấn", "Tốn") for q in focus_trigs) or any(d in door for d in ("Hưu", "Đỗ", "Tử")) or any(s in deity for s in ("Thái Âm", "Lục Hợp", "Cửu Địa")):
            pts += 18
            evs.append(f"Tượng Cấn/Khôn/Tốn (Cấn vi Sàng = Giường nằm) kết hợp {door} · {deity} (nơi nghỉ ngơi kín đáo)")
    if _has_kw("phòng khách", "ngoài bàn", "trên bàn", "bàn làm việc", "ngoài sảnh", "ngoài sân", "ngoài cửa", "kệ tivi", "bên ngoài"):
        if dt_idx in (4, 5, 6):
            pts += 20
            evs.append(f"Dụng Thần đóng tại Hào {dt_idx} (Ngoại Quái = không gian sinh hoạt chung bên ngoài / phòng khách)")
        if any(q in ("Càn", "Ly", "Chấn", "Đoài") for q in focus_trigs) or any(d in door for d in ("Khai", "Cảnh", "Thương")) or any(s in deity for s in ("Trực Phù", "Cửu Thiên", "Chu Tước")):
            pts += 18
            evs.append(f"Tượng {dung_q}/{biendung_q} phối {door} · {deity} chủ nơi sáng sủa, mặt bàn rộng mở ngoài phòng khách")

    # 4. THỜI TIẾT: MƯA / ẨM vs NẮNG / TẠNH RÁO (Tăng San Bốc Dịch · Thiên Thời Chương)
    _is_negated_rain = _has_kw("không mưa", "tạnh mưa", "hết mưa", "tạnh ráo")
    if _has_kw("mưa", "trời mưa", "mây ẩm", "giông", "bão", "ướt") and not _is_negated_rain:
        if "Phụ Mẫu" in moving_lts or (dt_ln.get("luc_than") == "Phụ Mẫu" and dt_ln.get("vuong_suy") in ("Vượng", "Tướng")):
            pts += 28
            evs.append("Lục Hào Thiên Thời: Hào Phụ Mẫu vượng/phát động chủ Vũ Thủy (trời đổ mưa)")
        if any(q == "Khảm" for q in focus_trigs) or ("Đoài" in focus_trigs and "Khảm" in active_trigs):
            pts += 22
            evs.append("Quẻ Khảm Thủy / Đoài Trạch hiện rõ tượng mây mưa ẩm ướt")
        if "Bồng" in star or "Trụ" in star or ("Hưu" in door and am_can in ("Nhâm", "Quý")):
            pts += 15
            evs.append(f"Kỳ Môn hội {star}/{door} chủ vũ lộ")
        if "Tử Tôn" in moving_lts or all(q in ("Càn", "Ly", "Tốn") for q in (dung_q, biendung_q)):
            pts -= 24
            evs.append("Quẻ toàn Càn/Ly/Tốn khô ráo hoặc Tử Tôn động (Nhật Nguyệt quang minh) bác bỏ khả năng mưa")

    if _has_kw("nắng", "trời nắng", "quang đãng", "tạnh", "tạnh ráo", "không mưa", "khô ráo"):
        if "Tử Tôn" in moving_lts or "Thê Tài" in moving_lts:
            pts += 28
            evs.append("Lục Hào Thiên Thời: Tử Tôn / Thê Tài phát động khắc chế Phụ Mẫu chủ trời quang mây tạnh")
        if any(q in ("Càn", "Ly", "Tốn") for q in focus_trigs) and "Khảm" not in focus_trigs:
            pts += 24
            evs.append(f"Quẻ {dung_q}/{biendung_q} (Càn Trời trong / Ly Nắng sáng / Tốn Gió tạnh, vắng bóng Khảm Thủy) báo trời không mưa, tạnh ráo")
        if "Cảnh" in door or "Khai" in door or "Anh" in star:
            pts += 15
            evs.append(f"Kỳ Môn đắc {door}/{star} chủ quang tạnh sáng sủa")

    # 5. ÂM NHẠC: NHẠC VUI vs NHẠC BUỒN vs NHẠC PHẬT vs NHẠC ĐÁM MA
    if _has_kw("nhạc phật", "tụng kinh", "nhạc thiền", "chú đại bi", "nhạc tâm linh"):
        if any("Hoa Cái" in ln.get("shensha", []) for ln in lines) or dt_ln.get("is_void") or any(q in ("Cấn", "Càn", "Khôn") for q in focus_trigs):
            pts += 24
            evs.append("Quẻ hội Cấn Sơn (chùa chiền/tĩnh tu) + Hoa Cái / Tuần Không (tâm không thanh tịnh) ứng Nhạc Phật / Thiền")
        if any(x in deity for x in ("Thái Âm", "Cửu Địa", "Trực Phù")) or "Đỗ" in door or "Hưu" in door:
            pts += 14
            evs.append(f"Kỳ Môn hội {deity} · {door} mang khí thiền định tĩnh lặng")
    if _has_kw("nhạc đám ma", "đám ma", "nhạc hiếu", "kèn đám ma", "bi ai"):
        if ("Bạch Hổ" in deity or dt_ln.get("luc_thu") == "Bạch Hổ") and ("Tử" in door or "Kinh" in door) and "Quan Quỷ" in moving_lts:
            pts += 30
            evs.append("Bạch Hổ + Tử/Kinh Môn + Quan Quỷ động đồng hiện ứng âm thanh tang hiếu")
        else:
            pts -= 15
    if _has_kw("nhạc buồn", "trữ tình", "bolero", "sâu lắng", "tâm trạng", "ballad"):
        if any(q in ("Khảm", "Đoài", "Tốn") for q in focus_trigs) or any(x in deity for x in ("Thái Âm", "Huyền Vũ", "Lục Hợp")) or "Hưu" in door:
            pts += 22
            evs.append("Tượng Khảm/Đoài/Tốn phối Thái Âm/Hưu Môn chủ giai điệu da diết, sâu lắng, trữ tình")
    if _has_kw("nhạc vui", "sôi động", "remix", "nhạc trẻ", "edm", "hào hứng"):
        if any(q in ("Chấn", "Ly") for q in focus_trigs) or any(x in deity for x in ("Cửu Thiên", "Chu Tước")) or "Cảnh" in door or "Thương" in door:
            pts += 24
            evs.append("Tượng Chấn Lôi (tiết tấu mạnh) / Ly Hỏa (rực rỡ) phối Cảnh Môn / Chu Tước chủ nhạc vui sôi động")

    # 6. TƯ THẾ, ĐỊA ĐIỂM NHÀ/CÔNG TY, THẬT/GIẢ, RỒI/CHƯA
    if _has_kw("ở nhà", "tại gia", "trong nhà"):
        if dt_idx <= 3 or any(d in door for d in ("Hưu", "Đỗ", "Tử", "Sinh")):
            pts += 22
            evs.append(f"Nội Quái (Hào {dt_idx}) & Cửa tĩnh ({door}) khẳng định đang ở tại nhà")
    if _has_kw("công ty", "cơ quan", "văn phòng", "ngoài đường"):
        if dt_idx >= 4 or any(d in door for d in ("Khai", "Cảnh", "Thương", "Kinh")):
            pts += 22
            evs.append(f"Ngoại Quái (Hào {dt_idx}) & Cửa động ({door}) khẳng định đang ở công ty/bên ngoài")
    if _has_kw("ngồi", "đang ngồi", "nằm", "đang nằm", "nằm nghỉ", "ngủ", "đang ngủ") and not _has_kw("nghỉ việc", "nghỉ làm", "nghỉ học", "nghỉ hưu", "cho nghỉ"):
        if not moving_lines or any(q in ("Cấn", "Khôn") for q in (the_q, dung_q)) or any(d in door for d in ("Hưu", "Tử", "Đỗ")):
            pts += 22
            evs.append("Quẻ thiên Tĩnh (Cấn/Khôn, Cửa Tĩnh) ứng tư thế ngồi/nằm nghỉ")
    if _has_kw("đứng", "đang đứng", "đi bộ", "đang đi lại", "thức", "đang thức"):
        if len(moving_lines) >= 1 and (any(q in ("Chấn", "Càn", "Tốn") for q in (the_q, dung_q, biendung_q)) or any(d in door for d in ("Thương", "Khai", "Cảnh", "Kinh"))):
            pts += 22
            evs.append("Quẻ phát động (Chấn Túc/Càn Hành, Cửa Động) ứng trạng thái đứng/di chuyển/thức")

    # 7. MÀU SẮC TRỰC TIẾP
    _COLOR_RULES = (
        (("đen", "xám đen", "xanh đen"), "Thủy", ("Khảm",), ("Huyền Vũ",)),
        (("trắng", "bạc", "xám", "ánh kim"), "Kim", ("Càn", "Đoài"), ("Bạch Hổ", "Thái Âm")),
        (("đỏ", "hồng", "cam", "tím"), "Hỏa", ("Ly",), ("Chu Tước", "Cửu Thiên")),
        (("xanh lá", "xanh lục", "xanh ngọc"), "Mộc", ("Chấn", "Tốn"), ("Lục Hợp",)),
        (("vàng", "nâu", "kem", "be"), "Thổ", ("Khôn", "Cấn"), ("Trực Phù", "Cửu Địa")),
    )
    for c_kws, c_el, c_trigs, c_deities in _COLOR_RULES:
        if _has_kw(*c_kws):
            if dt_el == c_el or any(q in c_trigs for q in focus_trigs) or any(d in deity for d in c_deities):
                pts += 22
                evs.append(f"Sắc tướng Ngũ Hành {c_el} ({dung_q}➔{biendung_q}, Thần {deity}) khớp trực tiếp màu sắc")

    return pts, evs


def _extract_multi_options_classical(question: str, option_a: str = "", option_b: str = "") -> List[str]:
    """
    V133.0: Tách đầy đủ 2..8 phương án lựa chọn (hỗ trợ cả dạng 'A hay B hay C' lẫn danh sách ngăn cách dấu phẩy
    như 'tôi đang nghe nhạc gì , nhạc vui , buồn, nhạc phật, nhạc đám ma').
    Tự động kế thừa danh từ chung đầu chuỗi (vd: 'nhạc vui, buồn' -> 'nhạc vui', 'nhạc buồn') để chấm điểm Vạn Vật Loại Tượng chuẩn 100%!
    """
    import re
    raw_q = str(question or "").strip()
    if not raw_q and not (option_a and option_b):
        return []
    if re.search(
        r"\b(tại\s+sao|vì\s+sao|nguyên\s+nhân|do\s+đâu|ý\s+đồ\s+gì|mưu\s+đồ\s+gì|đá\s+với|đấu\s+với|đội\s+nào\s+thắng)\b"
        r"|\b(?:tôi|mình|con|vợ|chồng|dạo\s+này|gần\s+đây)\s+hay\s+(?:gặp|bị|mất|ốm|đau|quên|mơ|lo|cãi|xui)\b",
        raw_q,
        flags=re.IGNORECASE,
    ):
        return []

    tail = raw_q
    # Cắt bỏ mệnh đề mở đầu câu hỏi ("tôi đang nghe nhạc gì,", "chọn cái nào:", "là gì:")
    m_split = re.search(
        r"(?:là\s+gì|nhạc\s+gì|món\s+gì|màu\s+gì|loại\s+nào|cái\s+nào|phương\s+án\s+nào|hướng\s+nào|ở\s+đâu)\s*[,:\-–—?]+\s*(.+)$",
        raw_q,
        flags=re.IGNORECASE,
    )
    prefix_noun = ""
    if m_split:
        tail = m_split.group(1).strip()
        m_noun = re.search(r"\b(nhạc|màu|món|xe|hướng|phòng|ngành|nghề)\s+(?:gì|nào)\b", raw_q, flags=re.IGNORECASE)
        if m_noun:
            prefix_noun = m_noun.group(1).lower()

    parts: List[str] = []
    if ("," in tail or "/" in tail or " hay " in tail.lower() or " hoặc " in tail.lower()) and len(tail) <= 220:
        cand = [
            re.sub(r"^[\s?.,;:!]+|[\s?.,;:!]+$", "", x)
            for x in re.split(r"\s*(?:,|/|\bhay\s+là\b|\bhay\b|\bhoặc\b)\s*", tail, flags=re.IGNORECASE)
        ]
        cand = [c for c in cand if c and len(c) <= 65 and not re.search(r"\b(tôi\s+đang|bạn\s+thử|cho\s+hỏi|xem\s+giúp)\b", c.lower())]
        if len(cand) >= 2:
            if not prefix_noun and " " in cand[0]:
                first_tok = cand[0].split()[0].lower()
                if first_tok in ("nhạc", "màu", "món", "phòng", "hướng", "xe"):
                    prefix_noun = first_tok
            norm_cand: List[str] = []
            for c_it in cand[:8]:
                if prefix_noun and not c_it.lower().startswith(prefix_noun + " ") and len(c_it.split()) <= 2:
                    norm_cand.append(f"{prefix_noun} {c_it}")
                else:
                    norm_cand.append(c_it)
            parts = norm_cand

    if len(parts) < 2 and option_a and option_b:
        # Nếu option_b còn chứa danh sách dấu phẩy hoặc 'hay', tách tiếp!
        sub_b = [x.strip(" ?.,;:") for x in re.split(r"\s*(?:,|/|\bhay\b|\bhoặc\b)\s*", str(option_b), flags=re.IGNORECASE) if x.strip(" ?.,;:")]
        raw_ab = [str(option_a).strip(" ?.,;:")] + sub_b
        parts = [p for p in raw_ab if p][:8]

    # Khử trùng lặp giữ nguyên thứ tự
    seen = set()
    uniq: List[str] = []
    for p in parts:
        k = p.lower().strip()
        if k and k not in seen:
            seen.add(k)
            uniq.append(p)
    return uniq if len(uniq) >= 2 else []


def synthesize_deep_classical_verdict(
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    dung_than: str = "Bản Thân",
    question: str = "",
    option_a: str = "",
    option_b: str = "",
) -> Dict[str, Any]:
    """
    V133.0 — BỘ ĐỘNG CƠ LUẬN QUẺ BIỆN CHỨNG TẦNG SÂU CHUẨN SÁCH BÍ TRUYỀN TRUNG HOA:
    Kết tinh trực tiếp từ Tăng San Bốc Dịch (Dã Hạc Lão Nhân), Bốc Phệ Chính Tông, Ngự Định Kỳ Môn Bảo Giám, Vấn Chân Kỳ Môn & Mai Hoa Dịch Số:
    1. Phân định Hỷ Dụng Thần vs Ưu/Kỵ Dụng Thần + Thọ Nguyên Đoán Pháp (Thượng/Trung/Hạ Thọ không ép trần tuổi giả).
    2. Lượng hóa Chuỗi Truyền Lực 4 Tầng Lục Hào (Nguyệt/Nhật [Táo/Thấp Thổ, Hợp Trói vs Hợp Khởi, Tam Mộ] -> Động [Tham Sinh Quên Khắc / Tam Hợp Cục] -> Hồi Đầu Sinh Khắc / Hóa Không / Hóa Phá / Tiến Thoái -> Thế/Dụng).
    3. Lượng hóa Chủ-Khách Kỳ Môn (Can Ngày vs Cung Sự Việc), Tứ Hại (Không, Mộ, Kích, Bức) & Ngũ Bất Ngộ Thời.
    4. Lượng hóa Đảng Thể vs Đảng Dụng Mai Hoa 4 chặng.
    5. Bệnh – Dược Ứng Kỳ Pháp (Tìm đúng Bệnh của quẻ để chỉ đúng Dược thời gian ứng nghiệm).
    6. Phân xử 2..N phương án lựa chọn (A, B, C, D...) bằng Vạn Vật Loại Tượng & Thế-Ứng Chủ-Khách (0% băm md5).
    """
    import re

    cd = chart_data if isinstance(chart_data, dict) else {}
    q_low = str(question or "").lower().strip()
    lines = ly_res.get("line_micro_audit") or []
    dt_idx = int(ly_res.get("dt_hao_idx") or 3)
    the_pos = int(ly_res.get("the_pos") or 3)
    ung_pos = int(ly_res.get("ung_pos") or 6)
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    the_ln = lines[the_pos - 1] if 1 <= the_pos <= len(lines) else {}
    ung_ln = lines[ung_pos - 1] if 1 <= ung_pos <= len(lines) else {}

    # ── TÂM PHÁP 1: NHẬN DIỆN HỶ/KỴ, BỆNH TRÌNH, THỌ NGUYÊN & THỜI THÁI CÂU HỎI (V134.0) ──
    is_weather_q = any(w in q_low for w in ("mưa", "nắng", "thời tiết", "giông", "bão", "tạnh"))
    is_illness_q = any(w in q_low for w in ("bệnh", "ốm", "sốt", "đau", "viêm", "nhập viện", "cấp cứu", "phẫu thuật", "mổ", "bình phục", "qua khỏi", "mang thai", "sinh nở", "phương thuốc", "bài thuốc"))
    is_recent_illness = is_illness_q and any(w in q_low for w in ("mới phát", "gần đây", "mới bị", "mới ốm", "mới sốt", "cấp tính", "cảm mạo"))
    is_chronic_illness = is_illness_q and any(w in q_low for w in ("lâu ngày", "bệnh nặng lâu", "mãn tính", "kinh niên", "nhiều năm", "ung thư"))
    is_worry_q = is_illness_q or any(w in q_low for w in ("tai nạn", "nguy hiểm", "âm binh", "vong", "tà khí", "bị kiện", "lo âu", "quan sự", "tai ương", "vô sự"))
    is_done_yet_q = any(w in q_low for w in ("đã bắn", "bắn chưa", "về chưa", "đến chưa", "tới chưa", "đi chưa", "ăn chưa", "xong chưa", "rồi hay chưa", "chưa hay rồi"))
    is_truth_q = any(w in q_low for w in ("thật hay giả", "nói thật", "nói dối", "có thật không", "tin được không", "lừa"))
    is_theft_q = any(w in q_low for w in ("trộm", "ăn cắp", "mất cắp", "kẻ gian", "ai lấy", "lấy cắp", "bị móc túi"))
    is_wealth_q = (
        any(w in q_low for w in ("tiền", "lương", "thưởng", "tài chính", "cầu tài", "kinh doanh", "lãi", "lời", "lợi lộc", "vốn", "giá", "bán", "mua", "đầu tư", "nợ", "vé số", "trúng thưởng", "tờ tiền", "triệu", "tỷ"))
        and not is_theft_q
        and not any(w in q_low for w in ("nghề gì", "ngành gì", "làm nghề", "mặt hàng gì"))
    )
    is_exam_q = any(w in q_low for w in ("đi thi", "kỳ thi", "thi đỗ", "thi đậu", "đỗ đạt", "thi cử", "khoa cử", "trúng tuyển"))
    is_career_q = any(w in q_low for w in ("công danh", "chức vụ", "thăng tiến", "thăng chức", "xin việc", "ứng tuyển", "bổ nhiệm", "sự nghiệp", "quan chức"))
    is_marriage_q = any(w in q_low for w in ("hôn nhân", "hôn sự", "nhân duyên", "cầu hôn", "kết hôn", "cưới", "vợ chồng")) and not is_illness_q
    is_lost_q = any(w in q_low for w in ("mất", "thất lạc", "tìm lại", "tìm thấy", "đánh rơi", "bỏ quên", "để quên"))
    is_travel_any = any(w in q_low for w in ("xuất hành", "đi xa", "trở về", "quay về", "đến lớp", "tới lớp", "chuyến đi", "qua trạm", "công tác"))
    dt_clean_ly = str(ly_res.get("dt_clean") or dung_than or "Bản Thân").strip()
    is_self_dt_ly = bool(ly_res.get("is_self_dt", dt_clean_ly in ("Bản Thân", "Hào Thế", "Dụng Thần", "")))
    is_traveler_q = is_travel_any and (not is_self_dt_ly or any(w in q_low for w in ("trở về", "đến lớp", "bao giờ về")))
    is_safety_worry_q = (
        any(w in q_low for w in ("bình an", "vô sự", "qua trạm", "lo âu", "tai ương", "kiện tụng"))
        and not is_career_q and not is_exam_q and not is_marriage_q and not is_wealth_q
    )
    is_age_longevity_q = any(w in q_low for w in ("bao nhiêu tuổi", "mấy tuổi", "thọ bao nhiêu", "hưởng thọ", "hưởng dương", "sống tới", "tuổi thọ", "thọ mệnh", "trường thọ", "sinh năm"))

    # ── TÂM PHÁP 2: CHẤM ĐIỂM BIỆN CHỨNG LỤC HÀO CỔ PHÁP V134.0 (TĂNG SAN BỐC DỊCH · BỐC PHỆ CHÍNH TÔNG) ──
    lh_pts = 0
    lh_chain_notes: List[str] = []
    vs_map = {"Vượng": 22, "Tướng": 15, "Bình": 2, "Hưu": -7, "Tù": -13, "Tử": -19}

    chi_ngay = _norm_chi(ly_res.get("chi_ngay") or cd.get("chi_ngay") or "Tý") or "Tý"
    chi_thang = _norm_chi(ly_res.get("chi_thang") or cd.get("chi_thang") or "Tuất") or "Tuất"
    chi_gio = _norm_chi(cd.get("chi_gio") or "Tý") or "Tý"
    nhat_el = CHI_ELEMENT.get(chi_ngay, "Thủy")
    nguyet_el = CHI_ELEMENT.get(chi_thang, "Thổ")
    palace_el = str(ly_res.get("palace_el") or "Kim")

    def _el_to_luc_than(e_chk: str) -> str:
        if not e_chk:
            return ""
        if e_chk == palace_el:
            return "Huynh Đệ"
        if SINH_EL.get(e_chk) == palace_el:
            return "Phụ Mẫu"
        if SINH_EL.get(palace_el) == e_chk:
            return "Tử Tôn"
        if KHAC_EL.get(e_chk) == palace_el:
            return "Quan Quỷ"
        if KHAC_EL.get(palace_el) == e_chk:
            return "Thê Tài"
        return ""

    nguyet_lt = _el_to_luc_than(nguyet_el)
    nhat_lt = _el_to_luc_than(nhat_el)

    dt_el = str(dt_ln.get("ngu_hanh") or "Thổ")
    dt_chi = str(dt_ln.get("chi") or "Thìn")
    the_el = str(the_ln.get("ngu_hanh") or "Thổ")
    the_chi = str(the_ln.get("chi") or "Thìn")
    ung_el = str(ung_ln.get("ngu_hanh") or "Thổ")
    vs = str(dt_ln.get("vuong_suy") or "Bình")
    h_flags = set(dt_ln.get("hoa_flags") or [])
    the_flags = set(the_ln.get("hoa_flags") or [])
    hop_st = str(dt_ln.get("hop_status") or "")
    mo_tp = str(dt_ln.get("mo_type") or "")
    dt_candidates = ly_res.get("dt_candidates") or []
    dt_phuc_obj = ly_res.get("dt_phuc_obj")
    ban_is_lx = bool(ly_res.get("ban_is_luc_xung"))
    ban_is_lh = bool(ly_res.get("ban_is_luc_hop"))
    bien_is_lx = bool(ly_res.get("bien_is_luc_xung"))
    bien_is_lh = bool(ly_res.get("bien_is_luc_hop"))
    xh_trans = str(ly_res.get("xung_hop_transition") or "")
    qb_rel = str(ly_res.get("quai_bien_rel") or "")

    ng_el = next((k for k, v in SINH_EL.items() if v == dt_el), "")
    ky_el = next((k for k, v in KHAC_EL.items() if v == dt_el), "")
    ng_movers: List[Dict[str, Any]] = []
    ky_movers: List[Dict[str, Any]] = []
    ky_broken: List[Dict[str, Any]] = []

    if lines:
        phuc_blocked_fatal = False
        # 2.1 Kiểm tra Dụng Thần Bất Hiện vs Nhật/Nguyệt Vi Dụng Thần (Phi Phục Thần Chương — Tăng San Bốc Dịch)
        if not is_self_dt_ly and not dt_candidates:
            # Khi Dụng Thần không hiện trên 6 hào, định Ngũ Hành chuẩn của Dụng Thần theo Bản Cung!
            _lt_to_el = {
                "Huynh Đệ": palace_el,
                "Phụ Mẫu": next((k for k, v in SINH_EL.items() if v == palace_el), "Thổ"),
                "Tử Tôn": SINH_EL.get(palace_el, "Thủy"),
                "Quan Quỷ": next((k for k, v in KHAC_EL.items() if v == palace_el), "Hỏa"),
                "Thê Tài": KHAC_EL.get(palace_el, "Mộc"),
            }
            dt_el = _lt_to_el.get(dt_clean_ly, dt_el)
            ng_el = next((k for k, v in SINH_EL.items() if v == dt_el), "")
            ky_el = next((k for k, v in KHAC_EL.items() if v == dt_el), "")
            if dt_phuc_obj:
                dt_chi = str(dt_phuc_obj.get("chi") or dt_chi)
                vs = str(dt_phuc_obj.get("strength") or "Hưu")
            if nhat_lt == dt_clean_ly or nguyet_lt == dt_clean_ly:
                # Ngoại lệ Cầu Tài Chương: Nếu quẻ không có Tài, Huynh Đệ vượng tĩnh trì Thế (được Nguyệt sinh) mà Nhật Tài KHÔNG xung Thế thì Huynh Đệ cướp Tài ('Duyên mộc cầu ngư')!
                if is_wealth_q and dt_clean_ly == "Thê Tài" and the_ln.get("luc_than") == "Huynh Đệ" and LUC_XUNG.get(the_chi) not in (chi_ngay, chi_thang) and not the_ln.get("is_nhat_pha") and not the_ln.get("is_nguyet_pha"):
                    lh_pts -= 26
                    lh_chain_notes.append("Cầu Tài Chương: Quẻ nội ngoại vô Tài, Huynh Đệ vượng trì Thế cướp khí Nhật Tài ('Như duyên mộc cầu ngư' — khó đắc tài)!")
                else:
                    lh_pts += 26
                    lh_chain_notes.append(f"Phi Phục Chương: Dụng Thần ({dt_clean_ly}) tuy ẩn trên 6 hào nhưng ĐẮC NHẬT/NGUYỆT TRỰC TIẾP LÀM DỤNG THẦN ('Dụng lâm Nhật Nguyệt hưu tầm Phục') — cực vượng!")
            elif dt_phuc_obj:
                phi_chi_p = _norm_chi(str(dt_phuc_obj.get("phi_than_can_chi") or "").split("-")[0])
                phuc_chi_p = _norm_chi(str(dt_phuc_obj.get("chi") or ""))
                tri_set_pf = {phi_chi_p, phuc_chi_p, chi_ngay}
                is_pf_tam_hinh = (tri_set_pf == {"Dần", "Tị", "Thân"}) or (tri_set_pf == {"Sửu", "Tuất", "Mùi"})
                phuc_has_root = (vs in ("Vượng", "Tướng") or SINH_EL.get(nhat_el) == dt_el or phuc_chi_p in (chi_ngay, chi_thang))
                is_phuc_void_unclashed = bool(dt_phuc_obj.get("is_void") and LUC_XUNG.get(phuc_chi_p) != chi_ngay and not phuc_has_root)
                if is_pf_tam_hinh or is_phuc_void_unclashed:
                    phuc_blocked_fatal = True
                    lh_pts -= 34
                    lh_chain_notes.append(
                        f"Phi Phục Chương (Thiên Kim Phú): Dụng Thần ({dt_clean_ly}) {'phạm Tam Hình Phi–Phục–Nhật' if is_pf_tam_hinh else 'Phục Cư Không Địa (ẩn phục vô khí lại lâm Chân Không)'} — sự dữ tâm vi, mưu cầu bất thành!"
                    )
                elif dt_phuc_obj.get("dac_xuat") or phuc_has_root:
                    lh_pts += 12 if phuc_has_root else 6
                    lh_chain_notes.append(f"Phi Phục Chương: Dụng Thần ẩn phục dưới Hào {dt_idx} nhưng Đắc Nguyệt/Nhật Sinh Vượng — Xuất Không/Xung Phi tất đắc ({dt_phuc_obj.get('can_chi_full','')})")
                else:
                    lh_pts -= 32
                    lh_chain_notes.append(f"Phi Đè Phục: Dụng Thần ({dt_clean_ly}) ẩn phục vô lực, mưu cầu khó thành")
            else:
                lh_pts -= 28
                lh_chain_notes.append(f"Dụng Thần ({dt_clean_ly}) vắng bóng hoàn toàn trên quẻ")
        else:
            lh_pts += vs_map.get(vs, 0)
            lh_chain_notes.append(f"Nguyệt Lệnh định khí Dụng Thần Hào {dt_idx} {dt_ln.get('luc_than','')} ({dt_chi}-{dt_el}) ở bậc {vs}")
            if dt_ln.get("is_tao_tho_thoi_kim"):
                lh_pts -= 8
                lh_chain_notes.append("Tăng San Bốc Dịch: Nguyệt kiến Mùi/Tuất là Táo Thổ làm giòn Kim")

            # Nguyệt Phá Chương: Động phùng Nguyệt Phá phi chung phá (đặc biệt khi Hóa Tiến / Hồi Đầu Sinh / Nhật Sinh)!
            if dt_ln.get("is_nguyet_pha"):
                if dt_ln.get("is_moving") and ("HOA_TIEN" in h_flags or "HOI_DAU_SINH" in h_flags or SINH_EL.get(nhat_el) == dt_el):
                    lh_pts -= 6
                    lh_chain_notes.append("Nguyệt Phá Chương: Dụng Thần tuy lâm Nguyệt Phá nhưng PHÁT ĐỘNG đắc Tiến/Sinh — xuất nguyệt thực phá ắt thành!")
                elif dt_ln.get("is_moving"):
                    lh_pts -= 12
                    lh_chain_notes.append("Nguyệt Phá Chương: Dụng Thần phát động lâm Nguyệt Phá ('Động bất chung phá' — chờ ngày Thực Phá/Phùng Hợp)")
                elif SINH_EL.get(nhat_el) == dt_el or hop_st == "HOP_KHOI":
                    lh_pts -= 12
                    lh_chain_notes.append("Dụng Thần tĩnh Nguyệt Phá nhưng được Nhật Thần sinh hợp cứu giải")
                else:
                    lh_pts -= 28
                    lh_chain_notes.append("Phạm Tĩnh Nguyệt Phá vô cứu (tháng xung vỡ gốc hào — tổn lực nghiêm trọng)")

            if dt_ln.get("is_am_dong"):
                lh_pts += 18
                if dt_ln.get("is_xung_khong"):
                    lh_chain_notes.append(f"Tuần Không Chương: Tĩnh Không phùng Nhật ({chi_ngay}) Xung thành Ám Động ('Xung Không Tắc Thực' — phá rỗng chuyển thành thực, ứng nhanh)")
                elif vs in ("Hưu", "Tù", "Tử"):
                    lh_chain_notes.append(f"Ám Động Chương (Dã Hạc): Tuy thất lệnh ở Nguyệt ({vs}) nhưng đắc Hào Động/Nguyệt Hợp cứu trợ nên gặp Nhật ({chi_ngay}) Xung thành Ám Động")
                else:
                    lh_chain_notes.append(f"Ám Động Chương: Dụng Thần vượng tướng đắc Nhật ({chi_ngay}) Xung thành Ám Động (ứng nghiệm cực nhanh)")
            elif dt_ln.get("is_xung_khong"):
                lh_pts += 14
                lh_chain_notes.append("Tuần Không Chương: Tĩnh Không phùng Nhật Xung ('Xung Không Tắc Thực' — phá rỗng thành thực)")
            elif dt_ln.get("is_nhat_pha"):
                lh_pts -= 24
                lh_chain_notes.append("Phạm Nhật Phá (hào suy tĩnh bị ngày xung tan rã)")

            if dt_chi == chi_ngay:
                if LUC_XUNG.get(dt_chi) == chi_thang:
                    lh_pts += 4
                    lh_chain_notes.append(f"Nguyệt Xung phùng Nhật Kiến ({chi_ngay}): 'Phá nhi bất phá, công quá tương để' — vừa đủ bù trừ Nguyệt Phá")
                else:
                    lh_pts += 22
                    lh_chain_notes.append(f"Dụng Thần Lâm Nhật Kiến ({chi_ngay}) — bất khả xâm phạm, ứng cực mạnh")
            elif SINH_EL.get(nhat_el) == dt_el:
                lh_pts += 15
                lh_chain_notes.append(f"Được Nhật Thần ({chi_ngay}-{nhat_el}) tương sinh tiếp sức")
            elif nhat_el == dt_el and LUC_XUNG.get(dt_chi) != chi_ngay:
                _CUNG_PHU_PAIRS = {
                    ("Hợi", "Tý"), ("Tý", "Hợi"),
                    ("Dần", "Mão"), ("Mão", "Dần"),
                    ("Tị", "Ngọ"), ("Ngọ", "Tị"),
                    ("Thân", "Dậu"), ("Dậu", "Thân"),
                }
                if (dt_chi, chi_ngay) in _CUNG_PHU_PAIRS:
                    lh_pts += 14
                    lh_chain_notes.append(f"Củng Phù Chương (Tăng San Bốc Dịch): Được Nhật Thần ({chi_ngay}-{nhat_el}) đồng hành Củng Phù / Tỷ Vượng tiếp khí")
                else:
                    lh_pts += 8
                    lh_chain_notes.append(f"Được Nhật Thần ({chi_ngay}-{nhat_el}) đồng hành tỷ trợ")
            elif KHAC_EL.get(nhat_el) == dt_el and not dt_ln.get("is_moving"):
                lh_pts -= 14
                if dt_ln.get("is_am_dong"):
                    lh_chain_notes.append(f"Nhật Thần ({chi_ngay}-{nhat_el}) vừa xung động vừa khắc ép — trong biến chuyển đi kèm sức ép va chạm thực tế")
                else:
                    lh_chain_notes.append(f"Bị Nhật Thần ({chi_ngay}-{nhat_el}) khắc chế")

            # Lục Hợp Chương: Hành nhân phùng Hợp bất lai vs mưu sự Hợp Khởi / Hợp Trụ
            if hop_st == "HOP_TRU":
                if is_traveler_q:
                    lh_pts -= 26
                    lh_chain_notes.append(f"Hành Nhân Chương: Dụng Thần động bị Nhật Thần ({chi_ngay}) HỢP TRÓI ('Bị hợp bất lai' — chân vướng bận chưa về)")
                else:
                    lh_pts -= 9
                    lh_chain_notes.append(f"Lục Hợp Chương: Dụng Thần ĐỘNG bị Nhật ({chi_ngay}) Hợp Trụ — chờ ngày Xung mở Hợp")
            elif hop_st == "HOP_KHOI":
                lh_pts += 16
                lh_chain_notes.append(f"Lục Hợp Chương: Dụng Thần TĨNH được Nhật ({chi_ngay}) HỢP KHỞI — chuyển tĩnh thành vượng")

            # Tam Mộ Chương: Nếu Nhật/Động xung khắc phá Mộ ('Phá Mộ như phá võng') thì thoát Mộ!
            mo_chi_dt = MO_BY_EL.get(dt_el, "")
            mo_broken_by_day = bool(mo_chi_dt and (LUC_XUNG.get(mo_chi_dt) == chi_ngay or KHAC_EL.get(nhat_el) == CHI_ELEMENT.get(mo_chi_dt, "")))
            if mo_tp == "SUY_NHAP_MO":
                if mo_broken_by_day:
                    lh_pts += 6
                    lh_chain_notes.append(f"Tam Mộ Chương: Dụng Thần nhập Mộ nhưng được Nhật ({chi_ngay}) Xung/Khắc PHÁ MỘ ('Mộ phá như phá võng, dễ dàng thoát ra'!)")
                elif dt_ln.get("is_moving"):
                    lh_pts -= 6
                    lh_chain_notes.append("Tam Mộ Chương: Dụng Thần tuy gặp Mộ lệnh nhưng đang PHÁT ĐỘNG mạnh — tới kỳ xung Mộ tất phát!")
                else:
                    lh_pts -= 20
                    lh_chain_notes.append("Tam Mộ Chương: Dụng Thần hưu tù vô khí rơi vào Chân Mộ — bế tắc")
            elif mo_tp == "VUONG_NHAP_KHO":
                lh_pts -= 4
                lh_chain_notes.append("Tam Mộ Chương: Dụng Thần hữu khí Nhập Khố (chờ ngày Xung Khố bung phát)")

        # 2.2 Kiểm tra Căn Tiên Vu Viện ('Dụng Thần vô căn, Nguyên Thần hữu lực diệc nan sinh')
        dt_is_rootless = bool(
            phuc_blocked_fatal
            or (not is_self_dt_ly and not dt_candidates and nhat_lt != dt_clean_ly and nguyet_lt != dt_clean_ly and not (dt_phuc_obj and dt_phuc_obj.get("dac_xuat")))
            or (
                not dt_ln.get("is_moving")
                and not dt_ln.get("is_am_dong")
                and (
                    ((dt_ln.get("is_nguyet_pha") or dt_ln.get("is_nhat_pha")) and (KHAC_EL.get(nhat_el) == dt_el or vs in ("Tù", "Tử")) and SINH_EL.get(nhat_el) != dt_el and nhat_el != dt_el and dt_chi != chi_ngay and hop_st != "HOP_KHOI")
                    or (dt_ln.get("khong_type") == "CHAN_KHONG" and not dt_ln.get("is_xung_khong") and not is_recent_illness)
                )
            )
        )

        # 2.3 Xét Tam Hợp Cục & Phân biệt Sinh Thế hay Sinh Ứng ('Xuất hiện vô tình') vs Ứng Động Tiếp Tục Sinh Thế ('Tham sinh quên khắc')
        veto_sinh_ung_only = False
        ung_bridges_to_the = bool(ung_ln.get("is_moving") and SINH_EL.get(ung_el) == the_el and "HOI_DAU_KHAC" not in (ung_ln.get("hoa_flags") or []))
        for th_item in (ly_res.get("tam_hop_cuc") or []):
            cuc_el = str(th_item.get("element") or "")
            cuc_lbl = str(th_item.get("label") or "")
            the_in_cuc = the_chi in set(th_item.get("active_branches") or []) or the_chi in cuc_lbl
            if (is_career_q or is_exam_q or is_wealth_q or is_marriage_q) and SINH_EL.get(cuc_el) == ung_el and SINH_EL.get(cuc_el) != the_el and not the_in_cuc and dt_idx != the_pos:
                if ung_bridges_to_the:
                    lh_pts += 26
                    lh_chain_notes.append(f"Liên Hoàn Thông Quan Đại Cát: {cuc_lbl} sinh Hào Ứng ({ung_ln.get('chi','')}) đang phát động ──► chuyển tiếp SINH THẲNG HÀO THẾ ('Tham sinh quên khắc')!")
                else:
                    veto_sinh_ung_only = True
                    lh_pts -= 42
                    lh_chain_notes.append(f"Tam Hợp Chương: {cuc_lbl} thành cục nhưng SINH ỨNG BẤT SINH THẾ ('Xuất hiện vô tình' — lộc/chức rơi vào tay người khác!)")
            elif KHAC_EL.get(cuc_el) == the_el and not is_safety_worry_q:
                lh_pts -= 24
                lh_chain_notes.append(f"Tam Hợp Cục ({cuc_lbl}) hợp đảng khắc thẳng Hào Thế — đại kỵ")
            elif cuc_el in (ng_el, dt_el):
                lh_pts += 22 if not dt_is_rootless else 0
                lh_chain_notes.append(f"Tam Hợp Cục ({cuc_lbl}) tụ khí sinh trợ Dụng Thần")
            elif cuc_el == ky_el:
                lh_pts -= 24
                lh_chain_notes.append(f"Đại Kỵ Tam Hợp Cục ({cuc_lbl}) hợp đảng khắc Dụng Thần")

        # 2.4 Nguyên Thần Ngũ Hữu Lực / Lục Vô Lực, Kỵ Thần, Cừu Thần & Kim Cương Chi Thân (Tăng San Bốc Dịch · Chu Thần Bân Sơ Thám)
        cuu_el = next((k for k, v in KHAC_EL.items() if v == ng_el), "")
        cuu_movers: List[Dict[str, Any]] = []
        bridge_bien_dt_movers: List[Dict[str, Any]] = []
        moving_others = [ln for ln in lines if (not dt_candidates and not is_self_dt_ly or ln.get("hao") != dt_idx) and (ln.get("is_moving") or ln.get("is_am_dong"))]
        for ln_m in moving_others:
            lf = set(ln_m.get("hoa_flags") or [])
            m_el = str(ln_m.get("ngu_hanh") or "")
            m_chi = str(ln_m.get("chi") or "")
            # Kiểm tra Động Biến Hóa Xuất Dụng Thần Thông Quan Sinh Thế ('Thần triệu cơ vu động' — VD Quan Tị động hóa Tài Dần hồi đầu sinh rồi sinh Thế):
            if (
                ln_m.get("is_moving")
                and not is_self_dt_ly
                and ln_m.get("bien_luc_than") == dt_clean_ly
                and "HOA_NGUYET_PHA" not in lf
                and ("HOI_DAU_SINH" in lf or SINH_EL.get(str(ln_m.get("bien_el") or ""), "") == the_el)
                and (SINH_EL.get(m_el) == the_el or m_el == the_el)
            ):
                bridge_bien_dt_movers.append(ln_m)

            if m_el == cuu_el and (ln_m.get("is_moving") or ln_m.get("is_am_dong")) and "HOI_DAU_KHAC" not in lf and "HOA_THOAI" not in lf and not ln_m.get("is_nhat_pha"):
                cuu_movers.append(ln_m)
            if m_el == ng_el:
                # Đặc Thù Nhật Nguyệt Tổ Hợp ('Kim Cương Chi Thân'): Lâm Nguyệt đắc Nhật sinh/tỷ hoặc Lâm Nhật đắc Nguyệt sinh/tỷ -> miễn nhiễm Hồi Đầu Khắc!
                is_ng_kim_cuong = (
                    (m_chi == chi_thang and (SINH_EL.get(nhat_el) == m_el or nhat_el == m_el))
                    or (m_chi == chi_ngay and (SINH_EL.get(nguyet_el) == m_el or nguyet_el == m_el))
                )
                # Động Vi Thủy Biến Vi Chung: Hào động bị Nhật Xung / Nguyệt Phá nhưng được Biến Hào Hồi Đầu Sinh hoặc Nhật Kiến tương sinh -> không phải Chân Phá!
                ng_rescued = bool(
                    ln_m.get("is_moving")
                    and (("HOI_DAU_SINH" in lf and "HOA_NGUYET_PHA" not in lf) or SINH_EL.get(nhat_el) == m_el)
                )
                is_tu_bien_quy = (ln_m.get("luc_than") == "Tử Tôn" and ln_m.get("bien_luc_than") == "Quan Quỷ")
                is_ng_disabled = (
                    ("HOI_DAU_KHAC" in lf and not is_ng_kim_cuong)
                    or "HOA_THOAI" in lf
                    or is_tu_bien_quy
                    or (ln_m.get("is_nhat_pha") and not ng_rescued)
                    or (ln_m.get("is_nguyet_pha") and ln_m.get("vuong_suy") in ("Hưu", "Tù", "Tử") and "HOA_TIEN" not in lf and not ng_rescued)
                )
                if not is_ng_disabled:
                    ng_movers.append(ln_m)
                elif is_tu_bien_quy:
                    lh_pts -= 22
                    lh_chain_notes.append(f"Nguyên Thần Hào {ln_m['hao']} Tử Tôn động BIẾN QUAN QUỶ — mất nguồn sinh trợ, phản sinh tai họa!")
            elif m_el == ky_el:
                # LƯU Ý CỐT TỬ DÃ HẠC: Kỵ Thần động HÓA TIẾN hoặc HÓA KHÔNG vẫn cực kỳ hung hãn khi Xuất Không!
                is_ky_self_defeated = (
                    "HOI_DAU_KHAC" in lf
                    or "HOA_THOAI" in lf
                    or ("HOA_NGUYET_PHA" in lf and "HOA_TIEN" not in lf)
                    or ("HOA_NHAT_PHA" in lf and "HOA_TIEN" not in lf)
                    or ln_m.get("is_nhat_pha")
                    or (ln_m.get("is_nguyet_pha") and "HOA_TIEN" not in lf and ln_m.get("chi") != chi_ngay)
                )
                if is_ky_self_defeated:
                    ky_broken.append(ln_m)
                else:
                    ky_movers.append(ln_m)

        if bridge_bien_dt_movers:
            dt_is_rootless = False
            bm0 = bridge_bien_dt_movers[0]
            lh_pts += 32
            lh_chain_notes.append(f"Động Biến Hóa Xuất Dụng Thần Thông Quan Sinh Thế: Hào {bm0['hao']} ({bm0['chi']}) động hóa ra {dt_clean_ly} ({bm0.get('bien_chi','')}) ──► tiếp lực sinh thẳng Hào Thế ('Thần triệu cơ vu động')!")

        # Tham Sinh Quên Khắc chân chính chỉ thành lập khi CẢ Kỵ Thần và Nguyên Thần đều MINH ĐỘNG (is_moving) và KHÔNG bị Cừu Thần cắt nguồn / Dụng Thần Hóa Thoái!
        real_ng_movers = [x for x in ng_movers if x.get("is_moving")]
        real_ky_movers = [x for x in ky_movers if x.get("is_moving")]
        # Nhật Nguyệt Công Quá Tương Để & Song Quyền Bất Địch Tứ Thủ: Hào lâm Nhật nhưng bị Nguyệt Xung (hoặc ngược lại) thì công quá vừa đủ triệt tiêu, không còn kim bài chắn Kỵ Thần!
        dt_lam_nhat_nguyet = bool(
            (dt_chi in (chi_ngay, chi_thang))
            and LUC_XUNG.get(dt_chi) not in (chi_thang, chi_ngay)
            and not dt_ln.get("is_nguyet_pha")
            and not dt_ln.get("is_nhat_pha")
            and len(ky_movers) == 1
            and "HOA_THOAI" not in h_flags
            and "HOI_DAU_KHAC" not in h_flags
        )

        if dt_is_rootless and ng_movers:
            lh_pts -= 16
            lh_chain_notes.append("Căn Tiên Vu Viện (Tăng San Bốc Dịch): Dụng Thần vô căn (Phá/Không bị khắc), Nguyên Thần tuy động cũng 'sinh chi bất khởi' (như cây đứt rễ)!")
        elif real_ng_movers and real_ky_movers and not cuu_movers and "HOA_THOAI" not in h_flags:
            lh_pts += 26
            lh_chain_notes.append(f"Đại Cát Tham Sinh Quên Khắc: Kỵ Thần Hào {real_ky_movers[0]['hao']} minh động sinh qua Nguyên Thần Hào {real_ng_movers[0]['hao']} ──► tiếp lực sinh Dụng Thần!")
        elif real_ng_movers and real_ky_movers and (cuu_movers or "HOA_THOAI" in h_flags):
            lh_pts -= 26
            lh_chain_notes.append("Cảnh báo 'Kỵ Dao Nguyên Động Cừu Hưng / Hóa Thoái Tuyệt Nguyên': Cừu Thần động chặn đứt mạch Nguyên Thần và Dụng Thần tự suy thoái!")
        elif ky_movers:
            ky0_f = set(ky_movers[0].get("hoa_flags") or [])
            if dt_lam_nhat_nguyet and "HOA_TIEN" not in ky0_f:
                # 'Hào ngộ Lệnh Tinh vật nan ngã hại — Hào thương Nhật đồ thụ kỳ danh' (Thiên Kim Phú):
                lh_pts -= 7
                lh_chain_notes.append(f"Thiên Kim Phú 'Hào Ngộ Lệnh Tinh Vật Nan Ngã Hại': Kỵ Thần Hào {ky_movers[0]['hao']} động nhưng Dụng Thần lâm Nhật/Nguyệt Kiến nên bất khả xâm phạm!")
            elif dt_ln.get("is_void") and dt_ln.get("khong_type") == "GIA_KHONG" and not is_chronic_illness and "HOA_TIEN" not in ky0_f and len(ky_movers) == 1:
                lh_pts -= 12
                lh_chain_notes.append(f"Tuần Không Chương 'Tị Không Đắc Cứu': Kỵ Thần Hào {ky_movers[0]['hao']} động khắc nhưng Dụng Thần ({dt_chi}) tạm lâm Giả Không né đòn, chờ Xuất Không ứng cát!")
            else:
                ky_pen = -34 if ("HOA_TIEN" in ky0_f or "HOI_DAU_SINH" in ky0_f or len(ky_movers) >= 2) else -25
                lh_pts += ky_pen
                lh_chain_notes.append(f"Kỵ Thần Hào {ky_movers[0]['hao']} ({ky_movers[0]['chi']}-{ky_el}) {'hợp đảng quần công / HÓA TIẾN cực mạnh' if ky_pen < -25 else 'độc phát'} khắc thẳng Dụng Thần!")
        elif ng_movers and cuu_movers and (MO_BY_EL.get(ng_el) in (chi_thang, chi_ngay) or vs in ("Hưu", "Tù", "Tử")):
            lh_pts -= 24
            lh_chain_notes.append(f"Cừu Thần Hào {cuu_movers[0]['hao']} ({cuu_movers[0]['chi']}) động/ám động khắc gãy Nguyên Thần Hào {ng_movers[0]['hao']} (đang hưu tù/nhập Mộ) — cắt đứt nguồn sinh Dụng Thần!")
        elif ng_movers:
            ng0_f = set(ng_movers[0].get("hoa_flags") or [])
            lh_pts += 12 if "HOA_HOP" in ng0_f else 22
            lh_chain_notes.append(f"Nguyên Thần Hào {ng_movers[0]['hao']} ({ng_movers[0]['chi']}-{ng_el}) phát động sinh phù trực tiếp Dụng Thần")
        elif ky_broken:
            lh_pts += 14
            lh_chain_notes.append(f"Kỵ Thần Hào {ky_broken[0]['hao']} tuy động nhưng tự Hóa Thoái / Hồi Đầu Khắc / Xung Phá — hoàn toàn mất lực hại Dụng Thần!")

        # 2.5 Xét Biến Hào của chính Dụng Thần (Tiến Thoái Tứ Pháp & Động Hóa Không/Phá/Mộ/Tuyệt — Tăng San Bốc Dịch)
        if is_self_dt_ly or dt_candidates:
            has_tien = "HOA_TIEN" in h_flags
            if "HOI_DAU_SINH" in h_flags:
                if "HOA_NGUYET_PHA" in h_flags or "HOA_NHAT_PHA" in h_flags:
                    lh_chain_notes.append("Dụng Thần tuy hóa Hồi Đầu Sinh nhưng Biến Hào lâm Nguyệt/Nhật Phá — nguồn sinh bị phá vỡ, không thể cứu trợ!")
                else:
                    lh_pts += 24
                    lh_chain_notes.append("Dụng Thần động hóa Hồi Đầu Sinh (tự sinh nguồn lực dồi dào)")
            if has_tien:
                lh_pts += 24
                lh_chain_notes.append("Tiến Thần Tứ Pháp: Dụng Thần động Hóa Tiến Thần (dù tạm Không/Phá đến kỳ Xuất Không Thực Phá ắt tiến mạnh!)")
            if "HOI_DAU_KHAC" in h_flags:
                # Ngoại trừ cách 'Thân thượng quỷ khử tắc an' xử lý riêng bên dưới
                if not (is_safety_worry_q and dt_idx == the_pos and dt_ln.get("luc_than") == "Quan Quỷ"):
                    lh_pts -= 32
                    lh_chain_notes.append("Dụng Thần động hóa Hồi Đầu Khắc (nhất phiếu phủ quyết — tự triệt tiêu ở chặng kết!)")
            if "HOA_THOAI" in h_flags:
                if dt_chi == chi_ngay and not is_chronic_illness and not is_age_longevity_q:
                    lh_pts -= 4
                    lh_chain_notes.append("Tiến Thoái Tứ Pháp: Dụng Thần hóa Thoái nhưng LÂM NHẬT KIẾN ('Vượng nhi bất thoái' — việc gần vẫn thành!)")
                else:
                    lh_pts -= 26 if is_chronic_illness or "huyết" in q_low else 20
                    lh_chain_notes.append("Dụng Thần động Hóa Thoái Thần (khí lực suy giảm rút lui dần)")
            if "HOA_KHONG" in h_flags and not has_tien:
                if "HOA_THOAI" in h_flags or "HOI_DAU_KHAC" in h_flags or is_chronic_illness:
                    lh_pts -= 22
                    lh_chain_notes.append("Dụng Thần suy thoái lại Hóa Không — rơi vào hư không")
                else:
                    lh_pts -= 4
                    lh_chain_notes.append("Tuần Không Chương (Dã Hạc Đính Chính): Dụng Thần động Hóa Không ('Động bất vi Không, thực không chi nhật tất thành'!)")
            if ("HOA_NGUYET_PHA" in h_flags or "HOA_NHAT_PHA" in h_flags) and not has_tien:
                lh_pts -= 20
                lh_chain_notes.append("Dụng Thần động Hóa Phá (ngọn biến tổn thương, cần chờ Thực Phá)")
            if "HOA_MO" in h_flags and not has_tien:
                lh_pts -= 5 if (vs in ("Vượng", "Tướng") or dt_chi == chi_ngay or SINH_EL.get(nhat_el) == dt_el) else 18
                lh_chain_notes.append("Dụng Thần động Hóa Mộ (vượng chờ xung khai, suy bị giam hãm)")
            if "HOA_HOP" in h_flags:
                if is_traveler_q:
                    lh_pts -= 26
                    lh_chain_notes.append("Hành Nhân Chương: Dụng Thần động Hóa Hợp ('Bị hợp bất lai' — người đi xa bị níu chân không về)")
                else:
                    lh_pts -= 6
            if "HOA_TUYET" in h_flags and "HOI_DAU_SINH" not in h_flags and not has_tien:
                lh_pts -= 6 if (vs in ("Vượng", "Tướng") or dt_chi == chi_ngay or SINH_EL.get(nhat_el) == dt_el) else 18
                lh_chain_notes.append("Dụng Thần động Hóa Tuyệt (hữu khí gặp sinh vượng vẫn thành, vô khí sức kiệt)")

            if dt_ln.get("khong_type") == "CHAN_KHONG" and not dt_ln.get("is_xung_khong") and not is_recent_illness:
                lh_pts -= 30
                lh_chain_notes.append(f"Dụng Thần rơi vào Chân Không ({dt_chi} tĩnh vô khí) — rỗng không khó thành")
            elif dt_ln.get("khong_type") == "GIA_KHONG":
                if not dt_ln.get("is_moving") and not dt_ln.get("is_am_dong") and KHAC_EL.get(nhat_el) == dt_el and not ng_movers and not is_recent_illness:
                    lh_pts -= 24
                    lh_chain_notes.append(f"Tuần Không Chương: Dụng Thần tĩnh Tuần Không lại bị Nhật ({chi_ngay}) khắc ('Không nhi hựu bị khắc' — xuất Không thụ chế, mưu cầu vô đắc)!")
                else:
                    lh_pts -= 3
                    lh_chain_notes.append(f"Dụng Thần lâm Giả Không ({dt_chi} hữu khí/động) — Xuất Không ắt ứng nghiệm!")

        # 2.6 Xét Đại Tượng Quái Biến, Lục Xung / Lục Hợp, Phục Ngâm & Tam Hình Toàn Cục (Tăng San Bốc Dịch)
        has_any_moving = any(x.get("is_moving") for x in lines)
        if qb_rel == "QUAI_HOA_HOI_DAU_KHAC":
            lh_pts = min(lh_pts - 34, -18)
            lh_chain_notes.append("Đại Tượng Quái Biến Hồi Đầu Khắc (Toàn quái biến khắc ngược gốc — bất luận Dụng Thần suy vượng đều chủ đại hung!)")
        elif xh_trans == "XUNG_HOA_HOP" and not is_chronic_illness:
            lh_pts += 28
            lh_chain_notes.append("Đại Cát Đặc Cách 'Lục Xung Biến Lục Hợp' (Tăng San Bốc Dịch: Tán nhi phục tụ, thất nhi phục đắc, tiên nan hậu dị!)")
        elif xh_trans == "HOP_HOA_XUNG" and not is_recent_illness:
            lh_pts -= 20
            lh_chain_notes.append("Cảnh báo 'Lục Hợp Biến Lục Xung' (Tiên hợp hậu ly, hữu thủy vô chung)")
        elif ban_is_lx and bien_is_lx and has_any_moving and not is_recent_illness and not (is_safety_worry_q and not is_illness_q):
            lh_pts -= 26
            lh_chain_notes.append("Đại Kỵ 'Lục Xung Biến Lục Xung' (Tăng San Bốc Dịch: Hoa vị phát nhi tiên tạ — xung chồng thêm xung, cơ sự tan vỡ!)")

        # Kiểm tra Động Biến Phục Ngâm tại Dụng Thần hoặc Hào Thế ('Động biến Phục Ngâm, hào suy bại vô dụng' — Phục Ngâm Chương):
        if (dt_ln.get("is_moving") and dt_chi and dt_chi == dt_ln.get("bien_chi")) or (the_ln.get("is_moving") and the_chi and the_chi == the_ln.get("bien_chi")):
            lh_pts -= 24
            lh_chain_notes.append("Phục Ngâm Chương: Dụng Thần / Hào Thế ĐỘNG BIẾN PHỤC NGÂM (biến nhi bất biến, rên rỉ suy bại tại chỗ)!")

        # Kiểm tra Nhật–Nguyệt–Dụng cấu thành Tam Hình Toàn Cục ({Dần, Tị, Thân} hoặc {Sửu, Tuất, Mùi}):
        if dt_chi and {chi_thang, chi_ngay, dt_chi} in ({"Dần", "Tị", "Thân"}, {"Sửu", "Tuất", "Mùi"}):
            lh_pts -= 34
            lh_chain_notes.append(f"Tam Hình Chương: Nguyệt ({chi_thang}) · Nhật ({chi_ngay}) · Dụng Thần ({dt_chi}) cấu thành TAM HÌNH TOÀN CỤC vô cứu — đại hung!")

        # 2.7 Xét Nền Tảng Hào Thế (Chủ thể người hỏi) & Thế–Dụng Tương Tác
        veto_the_pha_khac = False
        if dt_idx != the_pos:
            if "HOI_DAU_KHAC" in the_flags or (the_ln.get("is_moving") and the_ln.get("bien_luc_than") == "Quan Quỷ" and KHAC_EL.get(str(the_ln.get("bien_el") or ""), "") == the_el):
                lh_pts -= 28
                lh_chain_notes.append("Hào Thế động hóa Hồi Đầu Khắc / Biến Quỷ khắc Thế — bản thân chủ thể gặp hung hiểm hoặc tự bại!")
            elif the_ln.get("is_nguyet_pha") and not the_ln.get("is_moving") and (KHAC_EL.get(nhat_el) == the_el or the_ln.get("vuong_suy") in ("Tù", "Tử")):
                veto_the_pha_khac = bool(KHAC_EL.get(nhat_el) == the_el)
                lh_pts -= 34 if veto_the_pha_khac else 26
                lh_chain_notes.append("Hào Thế lâm Nguyệt Phá lại bị khắc ('Thế phá bị khắc, tuy hữu quan tài diệc nan hưởng')")
            elif the_ln.get("is_nhat_pha"):
                lh_pts -= 20
                lh_chain_notes.append("Hào Thế phạm Nhật Phá — căn cơ người hỏi suy sụp")

        if is_self_dt_ly or dt_candidates:
            if dt_idx == the_pos:
                lh_pts += 12
                lh_chain_notes.append("Dụng Thần Trì Thế (sự việc gắn liền bản thân)")
            elif SINH_EL.get(dt_el) == the_el or LUC_HOP.get(dt_chi, ("", ""))[0] == the_chi:
                if not (ky_movers and not real_ng_movers and not dt_lam_nhat_nguyet):
                    lh_pts += 14
                    lh_chain_notes.append(f"Dụng Thần ({dt_chi}) sinh/hợp Hào Thế ({the_chi}) — sự việc thuận tình hướng về ta")
            elif KHAC_EL.get(dt_el) == the_el:
                if is_wealth_q and dt_ln.get("luc_than") == "Thê Tài" and not the_ln.get("is_nhat_pha") and not (ky_movers and not real_ng_movers):
                    lh_pts += 16
                    lh_chain_notes.append("Đắc cách cổ pháp 'Tài Khắc Thế Tất Đắc Tài' (tiền tài tìm đến người!)")
                elif is_traveler_q and not (ky_movers and not real_ng_movers) and not dt_is_rootless:
                    lh_pts += 22
                    lh_chain_notes.append("Hành Nhân Chương: 'Dụng hào khắc Thế tất nhiên quy' — người đi xa nóng lòng quay về rất nhanh!")
                else:
                    lh_pts -= 12
                    lh_chain_notes.append("Dụng Thần khắc Hào Thế (áp lực đè lên bản thân)")
            elif KHAC_EL.get(the_el) == dt_el and is_traveler_q:
                lh_pts -= 14
                lh_chain_notes.append("Hành Nhân Chương: 'Thế khắc Dụng hề nhân vị động' — người ở xa chưa khởi hành")
            elif SINH_EL.get(the_el) == dt_el:
                lh_pts -= 4
                lh_chain_notes.append("Hào Thế sinh xuất cho Dụng Thần (hao tâm tốn sức)")

        # 2.8 Chuyên Pháp Từng Môn Theo Sách Bí Truyền (Bệnh Tật · Cầu Tài · Công Danh Khoa Cử · Thất Vật · Hành Nhân · Ưu Nghi)
        # (a) Thân Thượng Quỷ Khử Tắc An ('Thân thượng quỷ bất khử bất an' — Thiên Kim Phú):
        # Chỉ áp dụng khi Hào Thế KHÔNG bị Nhật Phá / Nguyệt Phá (nếu Thế Nhật Phá trong kiện tụng/bản thân thì bản thể bị thương!)
        # và không có Kỵ Thần Minh Động Hóa Tiến đang trực tiếp sát thương Dụng Thần!
        has_lethal_ky = any("HOA_TIEN" in (x.get("hoa_flags") or []) for x in ky_movers if x.get("is_moving"))
        if (
            (is_safety_worry_q or (is_illness_q and not is_self_dt_ly))
            and the_ln.get("luc_than") == "Quan Quỷ"
            and not has_lethal_ky
            and not (is_self_dt_ly and (the_ln.get("is_nhat_pha") or the_ln.get("is_nguyet_pha")))
        ):
            quy_removed = bool(
                "HOI_DAU_KHAC" in the_flags
                or (not is_self_dt_ly and (LUC_XUNG.get(the_chi) == chi_ngay or KHAC_EL.get(nhat_el) == the_el))
                or any(ln.get("is_moving") and KHAC_EL.get(str(ln.get("ngu_hanh") or ""), "") == the_el for ln in lines)
            )
            if quy_removed:
                lh_pts += 42
                lh_chain_notes.append("Thiên Kim Phú Đặc Pháp 'Thân Thượng Quỷ Khử Tắc An': Quan Quỷ trì Thế (nỗi lo/ách nạn đeo bám) được động hào Xung/Khắc quét sạch ➔ chuyển nguy thành bình an vô sự!")

        # (b) Chuyên Chương Tật Bệnh (Tăng San Bốc Dịch Quyển 4 Chương 99–104):
        if is_illness_q:
            if is_recent_illness:
                if (ban_is_lx or bien_is_lx) and qb_rel != "QUAI_HOA_HOI_DAU_KHAC":
                    # 'Cận bệnh phùng Lục Xung bất luận Dụng Thần suy vượng, bất dược nhi dũ!'
                    lh_pts = max(lh_pts + 42, 18)
                    lh_chain_notes.append("Y Dịch Cổ Pháp: 'Cận bệnh phùng Xung bất dược nhi dũ' — bệnh mới mắc gặp quẻ Lục Xung ắt mau khỏi (bất luận suy vượng)!")
                if (dt_ln.get("is_void") or "HOA_KHONG" in h_flags) and (dt_ln.get("is_moving") or not ban_is_lh):
                    # 'Phàm chiêm cận bệnh, Dụng Thần đắc ngộ Tuần Không giả, bất câu Nhật Nguyệt động hào khắc hại, xuất không chi nhật tức dũ!'
                    lh_pts = max(lh_pts + 42, 18)
                    lh_chain_notes.append("Y Dịch Cổ Pháp: 'Cận bệnh phùng Không tức dũ' — bệnh mới gặp Tuần Không / Hóa Không (luận Không bất luận Khắc), Xuất Không tự lui!")
            elif is_chronic_illness:
                if ban_is_lx or bien_is_lx:
                    lh_pts = min(lh_pts - 38, -20)
                    lh_chain_notes.append("Y Dịch Cổ Pháp: 'Cửu bệnh phùng Xung diệu dược nan y' — bệnh lâu ngày gặp Lục Xung cực kỳ nguy hiểm!")
                if dt_ln.get("is_void") or dt_ln.get("is_nguyet_pha"):
                    lh_pts = min(lh_pts - 30, -18)
                    lh_chain_notes.append("Y Dịch Cổ Pháp: Bệnh lâu ngày kỵ nhất Dụng Thần lâm Tuần Không / Nguyệt Phá")

            if is_self_dt_ly:
                if (
                    the_ln.get("luc_than") == "Tử Tôn"
                    and "HOI_DAU_KHAC" not in the_flags
                    and the_ln.get("khong_type") != "CHAN_KHONG"
                    and not the_ln.get("is_nhat_pha")
                ):
                    lh_pts = max(lh_pts + 42, 20)
                    lh_chain_notes.append("Y Dịch Cổ Pháp: 'Thân lâm Phúc Đức, thế tuy hiểm dĩ kham y' — Tử Tôn trì Thế ắt gặp lương y thuốc hay mà khỏi!")
                elif the_ln.get("luc_than") == "Phụ Mẫu" and ("HOA_THOAI" in the_flags or is_chronic_illness):
                    lh_pts -= 26
                    lh_chain_notes.append("Y Dịch Cổ Pháp: 'Phụ hào trì Thế diệu dược nan điều' — Phụ Mẫu trì Thế khắc chế Tử Tôn (dược thần)")

            if dt_ln.get("is_moving") and dt_ln.get("bien_luc_than") == "Quan Quỷ" and dt_clean_ly not in ("Phụ Mẫu", "Quan Quỷ") and not is_recent_illness:
                lh_pts -= 28
                lh_chain_notes.append("Y Dịch Đại Kỵ: 'Dụng hóa Quỷ thận phòng bất trắc' — người bệnh động biến Quan Quỷ")

        # (b2) Chuyên Chương Xu Tị Phòng Hại, Thọ Nguyên & Xuất Hành Bình An (Tăng San Bốc Dịch Quyển 3 Chương 39–40 & Quyển 4 Chương 91):
        # Lưu ý cổ pháp: 'Tử Tôn trì Thế bách vô ưu' chỉ ứng cho TỰ CHIÊM BẢN THÂN (is_self_dt_ly), tuyệt đối không lấy Thế Tử Tôn che cho Hành Nhân/Lục Thân khác đang bị Kỵ Thần khắc thương!
        if ((is_safety_worry_q and not is_traveler_q and not is_age_longevity_q) or (is_travel_any and is_self_dt_ly)) and not is_illness_q:
            has_tu_ton_guard = (
                (is_self_dt_ly and the_ln.get("luc_than") == "Tử Tôn" and "HOI_DAU_KHAC" not in the_flags and not the_ln.get("is_nhat_pha"))
                or (not (ky_movers and not real_ng_movers) and any(ln.get("luc_than") == "Tử Tôn" and ln.get("is_moving") and "HOI_DAU_KHAC" not in (ln.get("hoa_flags") or []) and ln.get("bien_luc_than") != "Quan Quỷ" for ln in lines))
                or (is_self_dt_ly and any(th_i.get("luc_than") == "Tử Tôn" for th_i in (ly_res.get("tam_hop_cuc") or [])))
            )
            if has_tu_ton_guard:
                lh_pts = max(lh_pts + 34, 18)
                lh_chain_notes.append("Xu Tị Chương: 'Đãn đắc Tử Tôn thừa vượng động / trì Thế, phi ương hoành họa hóa vi trần' — Phúc Đức hộ thân, vạn sự bình an!")
        if is_age_longevity_q and is_self_dt_ly and ("bình an" in q_low or "trường thọ" in q_low or "qua khỏi" in q_low):
            # Thọ Nguyên Chương: 'Nguyên thần nghi tĩnh bất nghi động, Kỵ thần tối phạ động dao'
            if real_ng_movers and not real_ky_movers:
                lh_pts = min(lh_pts - 42, -16)
                lh_chain_notes.append("Thọ Nguyên Chương: 'Chiêm thọ Nguyên Thần nghi tĩnh bất nghi động' — Nguyên Thần phát động báo hiệu có niên hạn nhập Mộ/Tuyệt!")

        if qb_rel == "QUAI_HOA_HOI_DAU_KHAC":
            lh_pts = min(lh_pts, -18)

        # (b3) Chuyên Chương Hôn Nhân (Tăng San Bốc Dịch Quyển 4 Chương 82):
        if is_marriage_q:
            if dt_clean_ly == "Quan Quỷ" and the_ln.get("luc_than") == "Tử Tôn":
                lh_pts -= 32
                lh_chain_notes.append("Hôn Nhân Chương: 'Nữ chiêm bất nghi Tử Tôn trì Thế' — khắc thương Quan tinh (phu tinh), duyên phận bất hòa/chia lìa!")
            elif dt_clean_ly == "Thê Tài" and the_ln.get("luc_than") == "Huynh Đệ" and not (the_ln.get("is_moving") and the_ln.get("bien_luc_than") == "Thê Tài") and xh_trans != "XUNG_HOA_HOP":
                lh_pts -= 26
                lh_chain_notes.append("Hôn Nhân Chương: 'Nam chiêm Huynh trì Thế phi phối ngẫu' — dễ trắc trở hoặc tổn thương thê duyên")
            # Nếu nhà gái hỏi mà hào Thê Tài bị Hồi Đầu Khắc (Lâm chi Ký Tế) thì âm dương thất phối
            for ln_mr in lines:
                if ln_mr.get("luc_than") == "Thê Tài" and ln_mr.get("is_moving") and "HOI_DAU_KHAC" in (ln_mr.get("hoa_flags") or []):
                    lh_pts -= 26
                    lh_chain_notes.append("Hôn Nhân Chương: Hào Thê Tài động bị Hồi Đầu Khắc — nam nữ bất tương sinh, hôn sự biến cố giữa chừng!")

        # (c) Chuyên Chương Cầu Tài (Tăng San Bốc Dịch Quyển 4 Chương 68):
        if is_wealth_q:
            tai_lines = [ln for ln in lines if ln.get("luc_than") == "Thê Tài"]
            if tai_lines and all(ln.get("is_void") and not ln.get("is_moving") and not ln.get("is_xung_khong") for ln in tai_lines):
                lh_pts -= 38
                lh_chain_notes.append("Cầu Tài Chương: Tất cả hào Thê Tài trên quẻ đều tĩnh lâm Tuần Không ('Lưỡng Tài giai Không, cầu tài bất đắc')")
            if the_ln.get("luc_than") == "Huynh Đệ":
                if (nhat_lt == "Thê Tài" and (LUC_XUNG.get(the_chi) == chi_ngay or KHAC_EL.get(nhat_el) == the_el)) or (
                    nguyet_lt == "Thê Tài" and (LUC_XUNG.get(the_chi) == chi_thang or KHAC_EL.get(nguyet_el) == the_el)
                ):
                    lh_pts += 30
                    lh_chain_notes.append("Cầu Tài Đặc Cách: Tuy Huynh Đệ trì Thế nhưng NHẬT/NGUYỆT TÁC TÀI TINH XUNG KHẮC THẾ — tài lộc dồn tới tất đắc!")
                elif the_ln.get("is_moving") and the_ln.get("bien_luc_than") == "Thê Tài":
                    lh_pts += 24
                    lh_chain_notes.append("Cầu Tài Đặc Cách: Huynh Đệ trì Thế động HÓA XUẤT THÊ TÀI — tới ngày Tài hiện tất đắc!")
                elif not (ng_movers and not dt_is_rootless):
                    lh_pts -= 22
                    lh_chain_notes.append("Cầu Tài Chương: 'Huynh Đệ trì Thế mạc cầu tài' — dễ hao tán hoặc cạnh tranh chia phần")
            # Huynh - Tài - Quan đồng động: Quan chế Huynh hộ Tài!
            mv_lts_all = {str(ln.get("luc_than") or "") for ln in lines if ln.get("is_moving")}
            if {"Huynh Đệ", "Thê Tài", "Quan Quỷ"}.issubset(mv_lts_all) and not dt_is_rootless:
                lh_pts += 22
                lh_chain_notes.append("Cầu Tài Chương: 'Huynh dữ Tài chấn, Quan hào phát động diệc kham cầu' — Quan Quỷ chế phục Huynh Đệ bảo vệ Tài!")

        # (d) Chuyên Chương Công Danh & Khoa Cử (Tăng San Bốc Dịch Quyển 3 Chương 49–61):
        if is_career_q or is_exam_q:
            if the_ln.get("luc_than") == "Tử Tôn":
                lh_pts -= 30
                lh_chain_notes.append("Công Danh Chương: 'Tử Tôn trì Thế hưu vọng vinh ấm' — khắc chế Quan tinh, cầu danh bất thành")
            if the_ln.get("is_void") and not the_ln.get("is_moving") and not the_ln.get("is_xung_khong"):
                lh_pts -= 16
                lh_chain_notes.append("Công Danh Chương: Hào Thế lâm Tuần Không — nền tảng bản thân chưa vững")
            if is_exam_q:
                # Khoa cử kiêm xét Phụ Mẫu (văn bài/bảng vàng)
                phu_lines = [ln for ln in lines if ln.get("luc_than") == "Phụ Mẫu"]
                best_phu = next((ln for ln in phu_lines if ln.get("hao") == the_pos or ln.get("is_moving") or ln.get("is_am_dong") or ln.get("vuong_suy") in ("Vượng", "Tướng")), None)
                if best_phu and ("HOA_TIEN" in (best_phu.get("hoa_flags") or []) or best_phu.get("is_am_dong") or best_phu.get("vuong_suy") in ("Vượng", "Tướng")):
                    lh_pts += 18
                    lh_chain_notes.append("Khoa Cử Chương: 'Phụ Vượng Quan Hưng, kham kỳ thủ tuyển' — Văn thư Phụ Mẫu vượng sáng nâng đỡ bảng vàng!")

        # (e) Chuyên Chương Thất Vật & Hành Nhân:
        if is_lost_q:
            if (ban_is_lh or bien_is_lh or xh_trans == "XUNG_HOA_HOP") and not dt_is_rootless and "HOI_DAU_KHAC" not in h_flags:
                lh_pts += 26
                lh_chain_notes.append("Thất Vật Chương: Quẻ hội Lục Hợp / Xung biến Hợp — đồ thất lạc vẫn ở quanh gần, tìm lại được!")
        if is_traveler_q:
            if the_ln.get("is_void") and bien_is_lx and vs in ("Hưu", "Tù", "Tử"):
                lh_pts -= 28
                lh_chain_notes.append("Hành Nhân Chương: Thế Không + Dụng Thần hưu tù + Biến Lục Xung — nền tảng cuộc hẹn rỗng, người không đến!")
            # Kiểm tra hào khác động hóa ra Dụng Thần và hợp chặt (VD: Tý động hóa Sửu Phụ Mẫu, Tý-Sửu hợp chặt không đến!)
            bound_by_other_hop = False
            for ln_other in lines:
                if ln_other.get("is_moving") and ln_other.get("bien_luc_than") == dt_clean_ly and "HOA_HOP" in (ln_other.get("hoa_flags") or []):
                    bound_by_other_hop = True
                    lh_pts -= 36
                    lh_chain_notes.append(f"Hành Nhân Chương: Hào {ln_other['hao']} ({ln_other['chi']}) động hóa {dt_clean_ly} ({ln_other.get('bien_chi','')}) LỤC HỢP TRÓI CHẶT ('Bị hợp bất lai')!")
            if dt_idx == the_pos and dt_ln.get("is_moving") and "HOI_DAU_KHAC" not in h_flags:
                lh_pts += 18
                lh_chain_notes.append("Hành Nhân Chương: 'Dụng Thần trì Thế phát động, xuất Không tức chí' — người đi xa về thẳng tới nhà!")
            elif bound_by_other_hop or "HOA_HOP" in h_flags or hop_st == "HOP_TRU":
                lh_pts = min(lh_pts, -14)

        if veto_sinh_ung_only or veto_the_pha_khac:
            lh_pts = min(lh_pts, -16)

    lh_norm = max(8, min(95, 52 + int(round(lh_pts * 0.65))))

    # ── TÂM PHÁP 3: KỲ MÔN CHỦ-KHÁCH, CHUYÊN ĐỀ DỤNG THẦN, PHỤC/PHẢN NGÂM, TỨ HẠI & NGŨ BẤT NGỘ THỜI ──
    tc = int(qm_res.get("target_cung") or 2)
    cung_chu = int(qm_res.get("cung_chu") or 2)
    cung_khach = int(qm_res.get("cung_khach") or tc)
    qm_dt_role = str(qm_res.get("qm_dt_role") or "GENERAL")
    p_map_qm = qm_res.get("palace_micro_audit") or {}
    pa_tc = p_map_qm.get(tc, {})
    pa_chu = p_map_qm.get(cung_chu, {})
    pa_khach = p_map_qm.get(cung_khach, {})
    el_tc = str(pa_tc.get("ngu_hanh") or "Thổ")
    el_chu = str(pa_chu.get("ngu_hanh") or "Thổ")
    door_tc = str(pa_tc.get("door") or "")
    star_tc = str(pa_tc.get("star") or "")
    deity_tc = str(pa_tc.get("deity") or "")
    tu_hai_tc = pa_tc.get("tu_hai") or []
    tu_hai_chu = pa_chu.get("tu_hai") or []
    truc_su_door = str(qm_res.get("truc_su_door") or cd.get("truc_su") or "")

    qm_pts = 0
    qm_notes: List[str] = []
    if p_map_qm:
        chu_trapped = any("Nhập Mộ" in x or "Kích Hình" in x for x in tu_hai_chu)
        if tc == cung_chu:
            if chu_trapped:
                qm_pts -= 10
                qm_notes.append(f"Cung Dụng Thần và Nhật Can đồng cung tại Cung {tc} nhưng cùng vướng Nhập Mộ/Kích Hình — tự bó tay trói chân")
            else:
                qm_pts += 12
                qm_notes.append(f"Cung Dụng Thần và Cung Người Hỏi đồng hội tại Cung {tc} (việc gắn sát thân, ứng nhanh)")
        elif SINH_EL.get(el_tc) == el_chu:
            qm_pts += 20
            qm_notes.append(f"Cung Dụng Thần ({tc}-{el_tc}) tương sinh Cung Người Hỏi ({cung_chu}-{el_chu}) — thiên thời địa lợi nâng đỡ")
        elif el_tc == el_chu:
            qm_pts += 10
            qm_notes.append(f"Cung Dụng Thần ({tc}-{el_tc}) tỷ hòa Cung Người Hỏi ({cung_chu}-{el_chu}) — thuận nhịp tương thông")
        elif KHAC_EL.get(el_chu) == el_tc:
            qm_pts += 7
            qm_notes.append(f"Cung Người Hỏi ({cung_chu}-{el_chu}) chế phục Cung Dụng Thần ({tc}-{el_tc}) — chủ động điều phối sẽ kiểm soát được")
        elif KHAC_EL.get(el_tc) == el_chu:
            qm_pts -= 18
            qm_notes.append(f"Cung Dụng Thần ({tc}-{el_tc}) khắc ngược Cung Người Hỏi ({cung_chu}-{el_chu}) — ngoại cảnh chèn ép, nhiều lực cản")
        elif SINH_EL.get(el_chu) == el_tc:
            if qm_dt_role == "WEALTH" and not tu_hai_tc and ("Sinh" in truc_su_door or any(d in str(pa_khach.get("door") or "") for d in ("Khai", "Hưu", "Sinh"))):
                qm_pts += 12
                qm_notes.append(f"Kinh Doanh Cầu Tài (Thần Kỳ Chi Môn): Sinh Môn Cung {tc} thanh tịnh vô Tứ Hại, bỏ vốn đầu tư sinh sôi thuận lợi")
            else:
                qm_pts -= 6
                qm_notes.append("Cung Người Hỏi sinh xuất cho Cung Sự Việc — hao tâm tốn sức")

        # Kiểm tra Tứ Hại tại Cung Nhật Can (Người hỏi) khi khác Cung Dụng Thần:
        if tc != cung_chu:
            for th_c in tu_hai_chu:
                if "Nhập Mộ" in th_c:
                    qm_pts -= 12
                    qm_notes.append(f"Nhật Can tại Cung {cung_chu} lâm Nhập Mộ — bản thân người hỏi đang bị bó buộc/thiếu chủ động")
                elif "Kích Hình" in th_c:
                    qm_pts -= 10
                    qm_notes.append(f"Nhật Can tại Cung {cung_chu} phạm Kích Hình — nội lực hao tổn")

        # Kiểm tra Song Trục Thời Can (Hàng hóa/Sự việc cụ thể) & Chuyên Đề Đòi Nợ / Bệnh Tật:
        if tc != cung_khach and pa_khach:
            door_kh = str(pa_khach.get("door") or "")
            th_kh = pa_khach.get("tu_hai") or []
            if any(d in door_kh for d in ("Tử", "Kinh", "Thương", "Đỗ")) and any("Tuần Không" in x or "Nhập Mộ" in x or "Kích Hình" in x for x in th_kh):
                qm_pts -= 18
                qm_notes.append(f"Thời Can sự việc/hàng hóa (Cung {cung_khach}) lâm {door_kh} lại phùng Không/Mộ/Hình — thương vụ bế tắc hoặc hàng hóa ế đọng")
            elif any(d in door_kh for d in ("Khai", "Hưu", "Sinh")) and not th_kh:
                qm_pts += 10
                qm_notes.append(f"Thời Can sự việc (Cung {cung_khach}) đắc cát môn {door_kh} thanh tịnh trợ lực")

        if qm_dt_role == "DEBT":
            p_sinh_q = int(qm_res.get("p_sinh") or 0)
            th_sinh_q = (p_map_qm.get(p_sinh_q) or {}).get("tu_hai") or []
            if any("Môn Bức" in x or "Tuần Không" in x for x in th_sinh_q):
                qm_pts -= 14
                qm_notes.append(f"Đòi nợ gặp Sinh Môn (Cung {p_sinh_q}) phạm Môn Bức / Không Vong — dòng tiền đối phương đứt gãy, khó thu hồi")
        elif qm_dt_role == "ILLNESS":
            p_nhue_q = int(qm_res.get("p_nhue") or 0)
            el_nhue_q = str((p_map_qm.get(p_nhue_q) or {}).get("ngu_hanh") or "")
            if el_nhue_q and KHAC_EL.get(el_tc) == el_nhue_q:
                qm_pts += 18
                qm_notes.append(f"Thiên Tâm Y Dược (Cung {tc}) khắc chế Bệnh Tinh Thiên Nhuế (Cung {p_nhue_q}) — thuốc đúng bệnh, mau bình phục")
            elif el_nhue_q and (KHAC_EL.get(el_nhue_q) == el_chu or p_nhue_q == cung_chu):
                qm_pts -= 16
                qm_notes.append(f"Bệnh Tinh Thiên Nhuế (Cung {p_nhue_q}) xâm khắc Nhật Can — bệnh tà còn vượng")

        if any(d in door_tc for d in ("Khai", "Hưu", "Sinh")):
            qm_pts += 14
        elif "Cảnh" in door_tc:
            qm_pts += 4
        elif any(d in door_tc for d in ("Tử", "Kinh", "Thương", "Đỗ")):
            qm_pts -= 12

        if any(s in star_tc for s in ("Tâm", "Phụ", "Nhậm", "Cầm", "Xung")):
            qm_pts += 8
        elif any(s in star_tc for s in ("Nhuế", "Bồng", "Trụ")):
            qm_pts -= 8

        for th in tu_hai_tc:
            if "Môn Bức" in th:
                qm_pts -= 14
                qm_notes.append(f"Phạm Môn Bức tại Cung {tc} (cửa cát mất nửa lực, cửa hung càng thêm hung)")
            elif "Kích Hình" in th:
                qm_pts -= 14
                qm_notes.append(f"Phạm Lục Nghi Kích Hình ({th}) — dễ va vấp thủ tục/tổn hao")
            elif "Nhập Mộ" in th:
                qm_pts -= 12
                qm_notes.append(f"Thiên Can Nhập Mộ tại Cung {tc} — bế tắc tạm thời, chưa thông suốt")
            elif "Tuần Không" in th:
                qm_pts -= 10
                qm_notes.append(f"Cung {tc} lâm Tuần Không — thông tin/kết quả còn bỏ ngỏ")

        # Kiểm tra Đại Cục Môn Phục Ngâm / Phản Ngâm & Trực Sử Tử Môn:
        if qm_res.get("is_mon_phuc_ngam") and qm_dt_role in ("WEALTH", "DEBT", "CAREER", "GENERAL") and not is_lost_q:
            qm_pts -= 18
            qm_notes.append("Đại Cục Môn Phục Ngâm (8 cửa đóng yên bản cung): khí cục trì trệ, kỵ nhập hàng/đòi nợ/tiến công gấp")
        elif qm_res.get("is_mon_phan_ngam"):
            if is_lost_q or is_recent_illness:
                qm_pts += 12
                qm_notes.append("Môn Phản Ngâm đặc pháp: tìm đồ thất lạc dễ quay về / bệnh mới mắc mau lui")
            else:
                qm_pts -= 12
                qm_notes.append("Đại Cục Môn Phản Ngâm: sự việc dễ biến động phản phúc nửa chừng")

        if "Tử" in truc_su_door and not is_lost_q:
            qm_pts -= 12
            qm_notes.append(f"Trực Sử lâm Tử Môn nắm quyền thực thi — cửa bế tắc cản trở tiến độ")

    # Kiểm tra Ngũ Bất Ngộ Thời (Can Giờ khắc Can Ngày đồng tính Âm Dương — Yên Ba Điếu Đồ Ca: 'Ngũ bất ngộ thời long bất tinh, bách sự giai hung!')
    can_n = str(cd.get("can_ngay") or "Giáp").strip()
    can_g = str(cd.get("can_gio") or "Giáp").strip()
    NGU_BAT_NGO = {
        ("Giáp", "Canh"), ("Ất", "Tân"), ("Bính", "Nhâm"), ("Đinh", "Quý"), ("Mậu", "Giáp"),
        ("Kỷ", "Ất"), ("Canh", "Bính"), ("Tân", "Đinh"), ("Nhâm", "Mậu"), ("Quý", "Kỷ"),
    }
    is_nbnt = (can_n, can_g) in NGU_BAT_NGO
    _qm_pts_pre_nbnt = qm_pts
    _is_future_horizon_q = bool(
        lines
        and any(w in q_low for w in ("tháng tới", "tháng sau", "năm tới", "năm sau", "sang năm", "sắp tới", "tương lai", "lâu dài", "cuối năm", "quý tới"))
        and not any(w in q_low for w in ("lúc này", "ngay bây giờ", "giờ này", "hôm nay", "tối nay", "sáng nay", "chiều nay"))
    )
    if is_nbnt:
        qm_pts = min(qm_pts - 38, -20)
        if _is_future_horizon_q:
            qm_notes.append(f"Lưu ý Kỳ Môn: Giờ lập quẻ chạm NGŨ BẤT NGỘ THỜI (Giờ {can_g} khắc Ngày {can_n}) — kỵ hành sự nóng vội ngay giờ này; riêng vận trình tháng/năm tới lấy Lục Hào & Nguyệt Lệnh làm gốc")
        else:
            qm_notes.append(f"Cảnh báo đại kỵ Kỳ Môn: Phạm NGŨ BẤT NGỘ THỜI (Giờ {can_g} khắc Ngày {can_n}) — bách sự giai hung, mưu sự ngay lúc này bất thành!")

    qm_norm = max(10, min(94, 52 + int(round(qm_pts * 0.72))))

    # ── TÂM PHÁP 4: MAI HOA ĐẢNG THỂ VS ĐẢNG DỤNG 4 CHẶNG + NGUYỆT LỆNH SUY VƯỢNG (THIỆU KHANG TIẾT · MAI HOA DỊCH SỐ) ──
    el_the_mh = TRIGRAM_META_8.get(mh_res.get("the_quai", "Càn"), TRIGRAM_META_8["Càn"])[3]
    el_dung_mh = TRIGRAM_META_8.get(mh_res.get("dung_quai", "Chấn"), TRIGRAM_META_8["Chấn"])[3]
    el_bien_mh = TRIGRAM_META_8.get(mh_res.get("bien_dung_quai", "Chấn"), TRIGRAM_META_8["Chấn"])[3]
    stages_mh = [
        (mh_res.get("dung_quai", "Chấn"), 1.1),
        (mh_res.get("ha_ho", "Cấn"), 0.7),
        (mh_res.get("thuong_ho", "Tốn"), 0.8),
        (mh_res.get("bien_dung_quai", "Chấn"), 1.9),
    ]
    mh_pts = 0.0
    for q_nm, w_st in stages_mh:
        q_el = TRIGRAM_META_8.get(q_nm, TRIGRAM_META_8["Càn"])[3]
        if SINH_EL.get(q_el) == el_the_mh:
            mh_pts += 15 * w_st
        elif q_el == el_the_mh:
            mh_pts += 8 * w_st
        elif KHAC_EL.get(el_the_mh) == q_el:
            mh_pts += 4 * w_st
        elif SINH_EL.get(el_the_mh) == q_el:
            mh_pts -= 9 * w_st
        elif KHAC_EL.get(q_el) == el_the_mh:
            mh_pts -= 16 * w_st

    # Thiệu Khang Tiết Suy Vượng Luận: Thể nghi vượng tướng, bất nghi suy tuyệt; Vượng Dụng khắc Suy Thể tắc đại hung!
    def _mh_season_state(e_chk: str, m_el: str) -> str:
        if e_chk == m_el:
            return "Vượng"
        if SINH_EL.get(m_el) == e_chk:
            return "Tướng"
        if SINH_EL.get(e_chk) == m_el:
            return "Hưu"
        if KHAC_EL.get(e_chk) == m_el:
            return "Tù"
        return "Tử"

    the_season_mh = _mh_season_state(el_the_mh, nguyet_el)
    dung_season_mh = _mh_season_state(el_dung_mh, nguyet_el)
    if the_season_mh in ("Vượng", "Tướng"):
        mh_pts += 12.0
    elif the_season_mh in ("Tù", "Tử"):
        mh_pts -= 12.0
    if KHAC_EL.get(el_dung_mh) == el_the_mh and dung_season_mh in ("Vượng", "Tướng") and the_season_mh in ("Hưu", "Tù", "Tử"):
        # Nếu Biến Quái không trực tiếp Hồi Đầu Sinh Thể thì Thể suy bị Vượng Dụng đốn gốc!
        if SINH_EL.get(el_bien_mh) != el_the_mh:
            mh_pts -= 28.0
    elif SINH_EL.get(el_dung_mh) == el_the_mh and dung_season_mh in ("Vượng", "Tướng"):
        mh_pts += 14.0

    mh_norm = max(12, min(92, 50 + int(round(mh_pts * 0.65))))

    # Điểm hợp nhất Tam Thức có trọng số thực chiến: Lục Hào 50% + Kỳ Môn 30% + Mai Hoa 20%
    if is_nbnt and _is_future_horizon_q:
        _qm_eff_future = max(qm_norm, max(24, min(88, 52 + int(round((_qm_pts_pre_nbnt - 10) * 0.72)))))
        composite_score = int(round(lh_norm * 0.55 + _qm_eff_future * 0.25 + mh_norm * 0.20))
    else:
        composite_score = int(round(lh_norm * 0.50 + qm_norm * 0.30 + mh_norm * 0.20))

    # ── TÂM PHÁP 5: BỆNH – DƯỢC ỨNG KỲ PHÁP (病药应期法) ──
    CHI_CLOCK = {
        "Tý": "23h–01h", "Sửu": "01h–03h", "Dần": "03h–05h", "Mão": "05h–07h",
        "Thìn": "07h–09h", "Tị": "09h–11h", "Ngọ": "11h–13h", "Mùi": "13h–15h",
        "Thân": "15h–17h", "Dậu": "17h–19h", "Tuất": "19h–21h", "Hợi": "21h–23h",
    }
    xung_dt = LUC_XUNG.get(dt_chi, "Ngọ")
    hop_dt = LUC_HOP.get(dt_chi, ("Mùi", ""))[0]
    is_hop_bound = dt_ln.get("is_moving") and (hop_dt == chi_ngay or "HOA_HOP" in h_flags)

    already_happened = bool(
        (dt_ln.get("is_moving") or dt_ln.get("is_am_dong") or dt_chi in (chi_ngay, chi_gio))
        and not dt_ln.get("is_void")
        and "HOA_KHONG" not in h_flags
        and "HOA_MO" not in h_flags
        and "HOI_DAU_KHAC" not in h_flags
        and not is_hop_bound
        and not any("Tuần Không" in x or "Nhập Mộ" in x for x in tu_hai_tc)
    )

    if dt_ln.get("is_void") or "HOA_KHONG" in h_flags:
        _kt_raw = str(dt_ln.get("khong_type") or "")
        _kt_vn = "Giả Không (tạm ẩn hữu khí, Xuất Không sẽ ứng)" if _kt_raw == "GIA_KHONG" else ("Chân Không (vô khí rỗng chân)" if _kt_raw == "CHAN_KHONG" else "Động Hóa Không")
        benh_quai = f"Bệnh tại Dụng Thần vướng Không Vong ({dt_chi} — {_kt_vn})"
        duoc_ung_ky = f"Ứng vào Ngày/Giờ XUẤT KHÔNG hoặc XUNG KHÔNG: {dt_chi} ({CHI_CLOCK.get(dt_chi,'')}) hoặc {xung_dt} ({CHI_CLOCK.get(xung_dt,'')})"
    elif "HOA_MO" in h_flags or mo_tp in ("SUY_NHAP_MO", "VUONG_NHAP_KHO"):
        mo_chi = MO_BY_EL.get(dt_el, "Thìn")
        xung_mo = LUC_XUNG.get(mo_chi, "Tuất")
        benh_quai = f"Bệnh tại Dụng Thần Lục Hào Nhập Mộ/Khố ({mo_chi})"
        duoc_ung_ky = f"Ứng vào Ngày/Giờ XUNG KHAI MỘ KHỐ: {xung_mo} ({CHI_CLOCK.get(xung_mo,'')}) hoặc trực {dt_chi}"
    elif is_hop_bound:
        benh_quai = f"Bệnh tại Hào Động phùng Hợp trói ({dt_chi} hợp {hop_dt})"
        duoc_ung_ky = f"Ứng vào Ngày/Giờ XUNG MỞ HỢP: {xung_dt} ({CHI_CLOCK.get(xung_dt,'')}) hoặc {LUC_XUNG.get(hop_dt,'')}"
    elif ky_movers and not ng_movers:
        k_chi = ky_movers[0]["chi"]
        xung_k = LUC_XUNG.get(k_chi, "Thân")
        benh_quai = f"Bệnh tại Kỵ Thần Hào {ky_movers[0]['hao']} ({k_chi}) độc phát khắc Dụng"
        duoc_ung_ky = f"Ứng khi chế phục Kỵ Thần vào Ngày/Giờ {xung_k} ({CHI_CLOCK.get(xung_k,'')}) hoặc khi Nguyên Thần {ng_el} đắc lệnh"
    elif dt_ln.get("is_nguyet_pha") or dt_ln.get("is_nhat_pha") or "HOA_NGUYET_PHA" in h_flags or "HOA_NHAT_PHA" in h_flags:
        benh_quai = f"Bệnh tại Dụng Thần bị Xung Phá ({dt_chi})"
        duoc_ung_ky = f"Cần đợi Ngày/Giờ THỰC PHÁ ({dt_chi} — {CHI_CLOCK.get(dt_chi,'')}) hoặc HỢP PHÁ ({hop_dt} — {CHI_CLOCK.get(hop_dt,'')}) mới hàn gắn"
    elif any("Nhập Mộ" in x for x in tu_hai_tc):
        _CUNG_XUNG_CHI = {1: "Ngọ", 2: "Sửu", 3: "Dậu", 4: "Hợi", 6: "Thìn", 7: "Mão", 8: "Mùi", 9: "Tý"}
        _x_cung_chi = _CUNG_XUNG_CHI.get(tc, xung_dt)
        benh_quai = f"Dụng Thần Lục Hào ({dt_chi}-{dt_el}) {vs}, riêng Thiên Can Kỳ Môn tại Cung {tc} tạm Nhập Mộ (chậm nhịp bề mặt)"
        duoc_ung_ky = f"Ứng khi Xung mở Cung {tc} vào Ngày/Giờ {_x_cung_chi} ({CHI_CLOCK.get(_x_cung_chi,'')}) hoặc trực vị Dụng Thần {dt_chi} ({CHI_CLOCK.get(dt_chi,'')})"
    elif already_happened and is_done_yet_q:
        benh_quai = "Quẻ Thông Mạch Hoàn Toàn (Dụng Thần hữu khí đã phát động / lâm Nhật Thời, không vướng Không-Mộ-Hợp)"
        duoc_ung_ky = f"Sự việc ĐÃ XẢY RA / ĐÃ NỔ NGAY TRONG KHUNG GIỜ HIỆN TẠI ({chi_gio} — {CHI_CLOCK.get(chi_gio,'')}) hoặc vừa hoàn tất trước đó!"
    elif "HOI_DAU_KHAC" in h_flags:
        _b_chi_hdk = str(dt_ln.get("bien_chi") or xung_dt)
        _x_bien = LUC_XUNG.get(_b_chi_hdk, xung_dt)
        benh_quai = f"Bệnh tại Dụng Thần động hóa Hồi Đầu Khắc ({dt_chi} hóa {_b_chi_hdk} khắc ngược)"
        duoc_ung_ky = f"Ứng khi chế phục Biến Hào vào Ngày/Giờ {_x_bien} ({CHI_CLOCK.get(_x_bien,'')}) hoặc khi Nguyên Thần {ng_el} vượng ({dt_chi})"
    elif "HOA_THOAI" in h_flags:
        benh_quai = f"Bệnh tại Dụng Thần động Hóa Thoái Thần ({dt_chi} thoái về {dt_ln.get('bien_chi','')})"
        duoc_ung_ky = f"Cần đợi Ngày/Giờ TRỰC VỊ {dt_chi} ({CHI_CLOCK.get(dt_chi,'')}) hoặc LỤC HỢP {hop_dt} ({CHI_CLOCK.get(hop_dt,'')}) kìm đà thoái"
    elif dt_ln.get("is_moving"):
        benh_quai = f"Dụng Thần ({dt_chi}) đang phát động mạnh ('Động nhi phùng Hợp tắc ứng')"
        duoc_ung_ky = f"Ứng nghiệm vào Ngày/Giờ LỤC HỢP {hop_dt} ({CHI_CLOCK.get(hop_dt,'')}) hoặc chính vị {dt_chi} ({CHI_CLOCK.get(dt_chi,'')})"
    elif dt_ln.get("is_am_dong"):
        benh_quai = f"Dụng Thần ({dt_chi}) đang Ám Động bởi Nhật ({chi_ngay}) Xung ('Ám động như minh động, phùng Hợp / Trị Nhật tất ứng')"
        duoc_ung_ky = f"Ứng nghiệm nhanh vào Ngày/Giờ LỤC HỢP {hop_dt} ({CHI_CLOCK.get(hop_dt,'')}) hoặc chính vị {dt_chi} ({CHI_CLOCK.get(dt_chi,'')})"
    elif vs in ("Tù", "Tử") and SINH_EL.get(nhat_el) != dt_el and nhat_el != dt_el and dt_chi != chi_ngay and hop_st != "HOP_KHOI":
        _ts_sinh_chi = {"Kim": "Tị", "Mộc": "Hợi", "Thủy": "Thân", "Hỏa": "Dần", "Thổ": "Thân"}.get(dt_el, dt_chi)
        benh_quai = f"Bệnh tại Dụng Thần ({dt_chi}-{dt_el}) hưu tù thất lệnh ({vs}) dưới Nguyệt Kiến {chi_thang} và đang tĩnh chưa đủ khí lực"
        duoc_ung_ky = f"Ứng khi ĐẮC SINH VƯỢNG TIẾP KHÍ vào Ngày/Giờ {_ts_sinh_chi} ({CHI_CLOCK.get(_ts_sinh_chi,'')}) hoặc chính vị {dt_chi} ({CHI_CLOCK.get(dt_chi,'')})"
    else:
        benh_quai = f"Dụng Thần ({dt_chi}) hữu khí nhưng đang An Tĩnh ('Tĩnh nhi phùng Xung tắc động')"
        duoc_ung_ky = f"Ứng nghiệm vào Ngày/Giờ XUNG ĐỘNG {xung_dt} ({CHI_CLOCK.get(xung_dt,'')}) hoặc trực {dt_chi} ({CHI_CLOCK.get(dt_chi,'')})"

    # ── TÂM PHÁP 6: CHUYÊN PHÁP ĐẶC THÙ & 4 TRỤ CỘT TIÊN TRI CHỐNG LUẬN ẢO (V143.0) ──
    special_mode = "STANDARD"
    verdict_polarity = "POSITIVE" if composite_score >= 55 else ("NEUTRAL" if composite_score >= 45 else "NEGATIVE")
    direct_headline = ""
    multi_opts = _extract_multi_options_classical(question, option_a=option_a, option_b=option_b)
    longevity_guide_note = ""

    _four_pillars: Dict[str, Any] = {}
    if not cd.get("_is_historical_liuyao_only"):
        try:
            from holographic_event_decoder import build_four_pillar_prophecy as _b4p_fn
            _four_pillars = _b4p_fn(
                ly_res=ly_res,
                qm_res=qm_res,
                mh_res=mh_res,
                deep_syn={
                    "composite_score": composite_score,
                    "lh_score": lh_norm,
                    "qm_score": qm_norm,
                    "mh_score": mh_norm,
                    "benh_quai": benh_quai,
                    "duoc_ung_ky": duoc_ung_ky,
                },
                chart_data=cd,
                dung_than=dung_than,
                question=question,
            ) or {}
        except Exception:
            _four_pillars = {}
    _uk_disp = str(_four_pillars.get("short_inline_date") or duoc_ung_ky)
    _ev_real_short = str(_four_pillars.get("concrete_event_summary") or "")
    _rel_real_short = str(_four_pillars.get("concrete_related_summary") or "")

    if is_age_longevity_q:
        ts_dt = str(dt_ln.get("ts_ngay") or "Bình")
        if lh_norm >= 68 or (vs in ("Vượng", "Tướng") and ts_dt in ("Trường Sinh", "Lâm Quan", "Đế Vượng") and "HOI_DAU_KHAC" not in h_flags):
            longevity_tier = "THƯỢNG THỌ CÁCH (80–96+ tuổi) nếu hỏi bậc cao niên/thọ nguyên; hoặc khí lực sung mãn nhất trong khung độ tuổi tương ứng vai vế"
        elif lh_norm >= 48:
            longevity_tier = "TRUNG THƯỢNG THỌ CÁCH (66–79 tuổi nếu hỏi bậc cha mẹ/cao niên; 35–58 tuổi nếu hỏi bậc trung niên)"
        else:
            longevity_tier = "HẠ/TRUNG THỌ HOẶC KHÍ SUY CẦN DƯỠNG (Dụng Thần hưu tù/bị thương khắc — cần xét kỹ vai vế ông bà/cha mẹ/trung niên/con cái trước khi chốt tuổi)"
        XT_NUM = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
        HT_NUM = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
        tq_m = str(mh_res.get("the_quai") or "Càn")
        dq_m = str(mh_res.get("dung_quai") or "Khôn")
        bq_m = str(mh_res.get("bien_dung_quai") or dq_m)
        longevity_guide_note = (
            f"[Thọ Nguyên & Quái Khí Gia Bội Pháp (Tăng San Bốc Dịch · Mai Hoa Quan Vật)]: {longevity_tier}. "
            f"Số Tiên Thiên Thể-Dụng-Biến = ({XT_NUM.get(tq_m,1)}, {XT_NUM.get(dq_m,8)}, {XT_NUM.get(bq_m,8)}), "
            f"Số Hậu Thiên Lạc Thư = ({HT_NUM.get(tq_m,6)}, {HT_NUM.get(dq_m,2)}, {HT_NUM.get(bq_m,2)}), "
            f"Cung Kỳ Môn = Cung {tc}. TUYỆT ĐỐI KHÔNG ĐƯỢC ép trần tuổi cố định 31-45 hay 50-78!"
        )

    if is_weather_q:
        special_mode = "WEATHER"
        # V134.0 (Tăng San Bốc Dịch · Thiên Thời Chương Đệ 35 — Dã Hạc Lão Nhân):
        # 'Thiên thời bất luận vượng suy, duy trọng động biến':
        # - Tử Tôn vi Nhật Nguyệt tinh đẩu, động tắc vạn lý tình quang; Thê Tài động khắc Phụ sinh Tử chủ tình minh!
        # - Phụ Mẫu vi vũ tuyết vụ sương, phát tắc bát phương nhuận trạch (tuy lâm Nguyệt Phá/Hồi Đầu Khắc, xung khai thực phá chi nhật diệc tác đại vũ; duy Phụ/Quỷ hóa Thoái Thần hoặc Phụ hóa Tử khi cầu tạnh tắc vũ chỉ thiên khai!).
        # - Quan Quỷ động (khi Phụ tĩnh, không bị Huynh Mộc đồng động sinh phong thuần túy) sinh Phụ chủ lôi đình vụ điện vũ thủy; Huynh hóa Tài/Tử chủ vân khai nhật xuất!
        asking_clear = any(w in q_low for w in ("nắng", "tạnh", "quang đãng", "hết mưa"))
        rain_pts = 0
        sun_pts = 0
        rain_evs: List[str] = []
        sun_evs: List[str] = []

        if lines:
            act_w_lines = [ln for ln in lines if ln.get("is_moving") or ln.get("is_am_dong") or ln.get("is_xung_khong")]
            mv_only_lts = {str(ln.get("luc_than") or "") for ln in lines if ln.get("is_moving")}
            seen_am_dong_keys = set()
            for ln_w in act_w_lines:
                lt_w = str(ln_w.get("luc_than") or "")
                lf_w = set(ln_w.get("hoa_flags") or [])
                blt_w = str(ln_w.get("bien_luc_than") or "")
                is_real_mv = bool(ln_w.get("is_moving"))
                if not is_real_mv:
                    ad_key = (lt_w, str(ln_w.get("chi") or ""))
                    if ad_key in seen_am_dong_keys:
                        continue
                    seen_am_dong_keys.add(ad_key)
                if lt_w == "Phụ Mẫu":
                    if is_real_mv and "HOA_THOAI" in lf_w:
                        sun_pts += 36
                        sun_evs.append("Phụ Mẫu động hóa Thoái Thần ('Phụ hóa Thoái vũ tương chỉ' — mây mưa tan dần, trời tạnh sáng)")
                    elif is_real_mv and blt_w == "Tử Tôn" and asking_clear:
                        sun_pts += 38
                        sun_evs.append("Phụ Mẫu động hóa Tử Tôn ('Phụ hóa Tử vũ hậu tình minh' — sau cơn mưa trời hửng nắng rực rỡ)")
                    elif is_real_mv and blt_w == "Huynh Đệ" and asking_clear and "Quan Quỷ" not in mv_only_lts:
                        sun_pts += 26
                        sun_evs.append("Phụ Mẫu tiết khí sang Huynh Đệ (sau đợt mưa ngắn mây tan trời tạnh, không mưa dầm)")
                    else:
                        # Nếu Thê Tài minh động trực tiếp khắc chế Phụ Mẫu chỉ Ám Động thì mưa bị kìm, chỉ có mây mỏng thoáng qua!
                        ad_rain_w = 18 if (not is_real_mv and "Thê Tài" in mv_only_lts) else 36
                        rain_pts += 44 if is_real_mv else ad_rain_w
                        rain_evs.append(f"Hào {ln_w['hao']} Phụ Mẫu ({ln_w['chi']}) {'phát động' if is_real_mv else 'ám động/xung không'} chủ Vũ Thủy (trời đổ mưa)")
                elif lt_w == "Tử Tôn":
                    if is_real_mv and "HOA_THOAI" in lf_w:
                        rain_pts += 10
                    elif is_real_mv and blt_w == "Quan Quỷ" and not asking_clear:
                        rain_pts += 18
                        rain_evs.append("Tử Tôn hóa Quan Quỷ ('Tình chi bất cửu' — nắng tắt chuyển mây âm mưa tới)")
                    else:
                        sun_pts += 46 if ("HOA_TIEN" in lf_w or is_real_mv) else 34
                        sun_evs.append(f"Hào {ln_w['hao']} Tử Tôn ({ln_w['chi']}) {'động' if is_real_mv else 'ám động/xung không'} ('Tử Tôn phát động, vạn lý tình quang' — nắng ráo quang đãng)")
                elif lt_w == "Thê Tài":
                    bonus_tc = 14 if blt_w == "Tử Tôn" else 0
                    sun_pts += (40 if is_real_mv else 34) + bonus_tc
                    sun_evs.append(f"Hào {ln_w['hao']} Thê Tài ({ln_w['chi']}) {'động' if is_real_mv else 'ám động/xung không'} khắc Phụ sinh Tử chủ trời quang mây tạnh")
                elif lt_w == "Quan Quỷ":
                    if is_real_mv and "HOA_THOAI" in lf_w:
                        sun_pts += 38
                        sun_evs.append("Quan Quỷ động hóa Thoái Thần ('Quỷ hóa Thoái vũ tương chỉ, vụ tán thiên khai' — mưa dứt trời quang)")
                    elif "Phụ Mẫu" not in mv_only_lts and "Huynh Đệ" in mv_only_lts and (ln_w.get("ngu_hanh") == "Mộc" or any(x.get("is_moving") and x.get("ngu_hanh") == "Mộc" for x in lines)):
                        # 'Chiêm vũ Phụ bất động, Huynh Quỷ đồng động, Mộc động sinh phong, vô vũ nhi hữu phong'
                        sun_pts += 22
                        sun_evs.append("Phụ Mẫu bất động, Huynh–Quỷ Mộc đồng động chỉ nổi gió lớn chứ không mưa")
                    elif not asking_clear:
                        rain_pts += 30
                        rain_evs.append(f"Hào {ln_w['hao']} Quan Quỷ ({ln_w['chi']}) động sinh Phụ Mẫu chủ lôi điện mây đen & mưa")
                elif lt_w == "Huynh Đệ":
                    if is_real_mv and (blt_w in ("Thê Tài", "Tử Tôn") or "HOA_THOAI" in lf_w):
                        sun_pts += 36
                        sun_evs.append(f"Hào {ln_w['hao']} Huynh Đệ hóa {blt_w or 'Thoái'} ('Vân trung biến xuất nhật sắc / Đệ hóa Tôn vân khai nhật xuất')")
                    elif is_real_mv and "HOA_TIEN" in lf_w:
                        rain_pts += 22
                        rain_evs.append(f"Hào {ln_w['hao']} Huynh Đệ độc phát Hóa Tiến Thần chủ phong vân tế nhật (mây mù âm u che khuất)")

            # Bổ sung Tam Hợp Cục Thiên Thời ('Tam hợp Tài/Tử cục chủ Tình, Tam hợp Phụ cục chủ Vũ')
            for th_it in (ly_res.get("tam_hop_cuc") or []):
                lt_c = str(th_it.get("luc_than") or "")
                if lt_c in ("Tử Tôn", "Thê Tài"):
                    sun_pts += 28
                    sun_evs.append(f"Tam Hợp {lt_c} Cục hội tụ quang khí trời nắng")
                elif lt_c == "Phụ Mẫu":
                    rain_pts += 28
                    rain_evs.append("Tam Hợp Phụ Mẫu Cục hội tụ vũ khí trời mưa")

            # Trường hợp Lục Hào hoàn toàn Tĩnh và không có Ám Động: mới đối chứng Vượng Suy & Kỳ Môn / Mai Hoa
            if not act_w_lines and not cd.get("_is_historical_liuyao_only"):
                r_i, r_e = score_option_classical_imagery("trời mưa giông ẩm ướt", ly_res, qm_res, mh_res, 1)
                s_i, s_e = score_option_classical_imagery("trời nắng quang đãng tạnh ráo", ly_res, qm_res, mh_res, 2)
                rain_pts += r_i
                sun_pts += s_i
                rain_evs.extend(r_e)
                sun_evs.extend(s_e)
            elif not act_w_lines:
                # Lục hào thuần tĩnh: so khí lực Phụ Mẫu vs Tử Tôn/Thê Tài; nếu hạn lâu không có Phụ/Quỷ động thì chủ Hạn (không mưa)
                if not asking_clear:
                    sun_pts += 12
                else:
                    sun_pts += 12
        else:
            r_i, r_e = score_option_classical_imagery("trời mưa giông ẩm ướt", ly_res, qm_res, mh_res, 1)
            s_i, s_e = score_option_classical_imagery("trời nắng quang đãng tạnh ráo", ly_res, qm_res, mh_res, 2)
            rain_pts += r_i
            sun_pts += s_i
            rain_evs.extend(r_e)
            sun_evs.extend(s_e)

        if rain_pts > sun_pts:
            verdict_polarity = "RAIN"
            direct_headline = f"🌧️ KẾT LUẬN THIÊN THỜI CỔ PHÁP: CÓ MƯA / TRỜI ĐỔ MƯA GIÔNG ({min(92, 58 + (rain_pts - sun_pts) // 2)}%) — {rain_evs[0] if rain_evs else 'Phụ Mẫu / Thủy khí phát động chủ Vũ'}!"
        else:
            verdict_polarity = "CLEAR"
            direct_headline = f"☀️ KẾT LUẬN THIÊN THỜI CỔ PHÁP: TRỜI NẮNG / TẠNH RÁO QUANG ĐÃNG ({min(92, 58 + max(4, sun_pts - rain_pts) // 2)}%) — {sun_evs[0] if sun_evs else 'Tử Tôn / Thê Tài đắc thế chủ Tình quang'}!"
    elif _four_pillars.get("domain") == "SPORTS_MATCH" or any(w in q_low for w in (" vs ", " v.s", "versus", "đá với", "đấu với", "đội nào thắng")):
        from holographic_event_decoder import extract_head_to_head_match_info as _ext_h2h_mg, compute_classical_head_to_head_verdict as _cmp_h2h_mg
        _h2h_mg = _four_pillars.get("match_verdict")
        if not isinstance(_h2h_mg, dict):
            _mi_mg = _ext_h2h_mg(question)
            if _mi_mg:
                _h2h_mg = _cmp_h2h_mg(
                    team_1=_mi_mg["team_1"],
                    team_2=_mi_mg["team_2"],
                    ly_res=ly_res,
                    qm_res=qm_res,
                    mh_res=mh_res,
                    chart_data=cd,
                )
        if isinstance(_h2h_mg, dict):
            special_mode = "SPORTS_COMPETITION"
            verdict_polarity = str(_h2h_mg.get("outcome_code") or "TEAM1_WIN")
            _ban_bien_sp = f"{ly_res.get('ban_name','')} ➔ {ly_res.get('bien_name','')}"
            direct_headline = (
                f"⚽ LUẬN ĐOÁN THI ĐẤU CHỦ–KHÁCH TAM THỨC ({_ban_bien_sp}): "
                f"{_h2h_mg['winner_label']} "
                f"[Xác suất: {_h2h_mg['team_1']} {_h2h_mg['p_t1']}% · Hòa {_h2h_mg['p_draw']}% · {_h2h_mg['team_2']} {_h2h_mg['p_t2']}%] — "
                f"TỶ SỐ DỰ BÁO: {_h2h_mg['score_pred'].upper()} "
                f"({_h2h_mg['the_desc']} đối {_h2h_mg['ung_desc']}) ➔ Thời điểm thi đấu: {_uk_disp}!"
            )
    elif is_done_yet_q and len(multi_opts) <= 2:
        special_mode = "DONE_YET"
        if already_happened:
            verdict_polarity = "DONE"
            direct_headline = f"✅ KẾT LUẬN THỜI THÁI THỰC TẾ: ĐÃ XẢY RA / ĐÃ HOÀN TẤT RỒI! ({benh_quai} · {_uk_disp})"
        else:
            verdict_polarity = "NOT_YET"
            direct_headline = f"⏳ KẾT LUẬN THỜI THÁI THỰC TẾ: HIỆN TẠI CHƯA XẢY RA ({benh_quai}) ➔ ỨNG NGHIỆM VÀO: {_uk_disp}!"
    elif is_truth_q and len(multi_opts) <= 2:
        special_mode = "TRUTH_CHECK"
        deceit_flags = (
            dt_ln.get("is_void")
            or ung_ln.get("is_void")
            or dt_ln.get("luc_thu") in ("Huyền Vũ", "Đằng Xà")
            or ung_ln.get("luc_thu") in ("Huyền Vũ", "Đằng Xà")
            or deity_tc in ("Huyền Vũ", "Đằng Xà")
            or any("Tuần Không" in x for x in tu_hai_tc)
        )
        if deceit_flags and composite_score < 58:
            verdict_polarity = "FALSE"
            direct_headline = f"🚨 KIỂM ĐỊNH THỰC HƯ CỔ PHÁP: KHÔNG ĐÁNG TIN / THÔNG TIN SAI LỆCH HOẶC NÓI DỐI (Ứng/Dụng vướng Không Vong · Huyền Vũ/Đằng Xà)!"
        else:
            verdict_polarity = "TRUE"
            direct_headline = f"✅ KIỂM ĐỊNH THỰC HƯ CỔ PHÁP: ĐÂY LÀ SỰ THẬT / ĐÁNG TIN CẬY ({composite_score}% — Hào Ứng & Dụng Thần hữu khí, minh bạch)!"
    elif len(multi_opts) >= 2:
        special_mode = "CHOICE_MULTI" if len(multi_opts) >= 3 else "CHOICE_AB"
        scored_opts = []
        # Hệ neo cổ pháp cho từng vị trí phương án (1: Hào Thế/Cung Chủ, 2: Hào Ứng/Cung Khách, 3: Hào Động/Biến Dụng, 4: Dụng Thần/Trực Sử...)
        anchor_lines = [the_ln, ung_ln, dt_ln] + [ln for ln in lines if ln.get("is_moving")] + lines
        for idx_o, opt_txt in enumerate(multi_opts, 1):
            o_pts, o_evs = score_option_classical_imagery(opt_txt, ly_res, qm_res, mh_res, idx_o)
            anc_ln = anchor_lines[(idx_o - 1) % max(1, len(anchor_lines))] if anchor_lines else {}
            anc_bonus = vs_map.get(str(anc_ln.get("vuong_suy") or "Bình"), 0) // 3
            if anc_ln.get("is_moving"):
                anc_bonus += 4
            if anc_ln.get("is_void") and anc_ln.get("khong_type") == "CHAN_KHONG":
                anc_bonus -= 6
            total_o = o_pts + anc_bonus
            scored_opts.append((total_o, idx_o, opt_txt, o_evs))
        scored_opts.sort(key=lambda x: (x[0], -x[1]), reverse=True)
        # Quy đổi điểm sang xác suất trực quan tổng = 100%
        min_sc = min(x[0] for x in scored_opts)
        weights = [max(6.0, float(x[0] - min_sc + 14.0)) for x in scored_opts]
        sum_w = sum(weights) or 1.0
        pcts = [int(round(w * 100.0 / sum_w)) for w in weights]
        if pcts:
            pcts[0] += (100 - sum(pcts))
        win_pts, _, win_opt, win_evs = scored_opts[0]
        breakdown_str = " · ".join(f"{it[2]} ({pcts[i]}%)" for i, it in enumerate(scored_opts))
        direct_headline = (
            f"⚖️ ĐỐI CHỨNG VẠN VẬT LOẠI TƯỢNG & TAM THỨC ({len(multi_opts)} PHƯƠNG ÁN): CHỐT «{win_opt.upper()}» ({pcts[0]}%) "
            f"[{breakdown_str}] — {win_evs[0] if win_evs else 'Ứng hợp trực tiếp tượng Quẻ Động, Lục Thú & Tinh-Môn Kỳ Môn'}!"
        )
    elif any(w in q_low for w in ["đá với", "đấu với", "đội nào thắng"]) or not any(w in q_low for w in ["bao nhiêu", "mấy ", "màu gì"]):
        # V137.0: Giải mã ĐÚNG TRỌNG TÂM 100% cho cả Câu Hỏi Mở (Ai / Ở đâu / Làm gì / Cái gì / Nghề gì / Chuyện gì / Thế nào) lẫn Câu Hỏi Cát–Hung!
        from holographic_event_decoder import TRIGRAM_PAIR_64_IMAGERY, CHI_CONCRETE_IMAGE, LUC_THU_ROLE_COLOR
        _core_reason_1 = lh_chain_notes[0] if lh_chain_notes else f"Dụng Thần {dung_than} ({dt_ln.get('vuong_suy','Bình')})"
        _ban_bien_lbl = f"{ly_res.get('ban_name','')} ➔ {ly_res.get('bien_name','')}"
        _huong_tc = str(pa_tc.get("huong") or "Đông Nam")
        _quai_tc = str(pa_tc.get("quai") or "Tốn")
        _up_m_q = str(mh_res.get("up_q") or mh_res.get("the_quai") or "Càn")
        _lo_m_q = str(mh_res.get("lo_q") or mh_res.get("dung_quai") or "Khôn")
        _up_b_q = str(mh_res.get("up_bien") or mh_res.get("bien_dung_quai") or _up_m_q)
        _lo_b_q = str(mh_res.get("lo_bien") or _lo_m_q)
        _YANG_CHIS = {"Tý", "Dần", "Thìn", "Ngọ", "Thân", "Tuất"}
        _YANG_TRIGS = {"Càn", "Chấn", "Khảm", "Cấn"}

        _is_who_q = is_theft_q or bool(re.search(r"\b(ai\s+lấy|ai\s+cầm|ai\s+ăn\s+cắp|ai\s+giúp|ai\s+đang|ai\s+nói|ai\s+hại|ai\s+cản|là\s+ai|người\s+nào)\b", q_low))
        _is_motive_q = any(w in q_low for w in ("ý đồ gì", "mưu đồ gì", "tâm ý gì", "nghĩ gì về tôi", "có ý gì"))
        _is_why_cause_q = any(w in q_low for w in ("tại sao", "vì sao", "nguyên nhân gì", "do đâu mà"))
        _is_how_remedy_q = any(w in q_low for w in ("làm cách nào", "cách nào để", "làm sao để hóa giải", "cách hóa giải", "phương pháp hóa giải"))
        _is_which_dir_q = any(w in q_low for w in ("hướng nào", "phương nào", "quay hướng gì", "chạy đi lạc hướng"))
        _is_where_doing_q = (
            any(w in q_low for w in ("ở đâu", "chỗ nào", "nơi nào", "đang làm gì", "làm gì lúc này"))
            and not is_lost_q and not _is_which_dir_q
        )
        _is_what_obj_q = (
            any(w in q_low for w in ("cái gì", "vật gì", "đồ vật gì", "thứ gì", "trong hộp", "trên bàn", "trước mặt tôi", "cầm cái gì"))
            and not is_lost_q and not _is_motive_q
        )
        _is_job_fit_q = any(w in q_low for w in ("nghề gì", "ngành gì", "làm nghề", "kinh doanh gì", "buôn bán gì", "mặt hàng gì", "hợp nghề"))
        _is_event_risk_q = any(
            w in q_low
            for w in (
                "có chuyện gì", "chuyện gì xảy ra", "xảy ra chuyện gì", "xảy ra việc gì", "sự việc gì",
                "sự kiện gì", "biến động gì", "có biến động", "thay đổi gì", "có thay đổi",
                "chuyện gì cần", "đề phòng gì", "cần đề phòng", "biến cố gì", "vận hạn gì", "tin vui gì", "có điềm gì",
            )
        )
        _is_how_outlook_q = any(w in q_low for w in ("thế nào", "như thế nào", "ra sao", "sắp tới sao", "tốt hay xấu", "ổn không")) and not _is_motive_q

        if _is_which_dir_q:
            special_mode = "WHICH_DIRECTION"
            _CHI_DIR_8 = {
                "Tý": "Chính Bắc", "Sửu": "Đông Bắc", "Dần": "Đông Bắc", "Mão": "Chính Đông",
                "Thìn": "Đông Nam", "Tị": "Đông Nam", "Ngọ": "Chính Nam", "Mùi": "Tây Nam",
                "Thân": "Tây Nam", "Dậu": "Chính Tây", "Tuất": "Tây Bắc", "Hợi": "Tây Bắc",
            }
            _chi_dir_lbl = _CHI_DIR_8.get(dt_chi, _huong_tc)
            if any(w in q_low for w in ("cửa chính", "nhà tôi", "hướng nhà", "bàn thờ", "cổng")):
                _h2_chi = str(lines[1].get("chi") if len(lines) >= 2 else dt_chi)
                _h4_chi = str(lines[3].get("chi") if len(lines) >= 4 else dt_chi)
                _door_dir = _CHI_DIR_8.get(_h4_chi, _huong_tc)
                direct_headline = (
                    f"🧭 ĐỊNH VỊ PHƯƠNG HƯỚNG PHONG THỦY GIA TRẠCH ({_ban_bien_lbl}): "
                    f"CỬA CHÍNH / MẶT TIỀN ỨNG PHƯƠNG «{_door_dir.upper()}» (Sơn {_h4_chi} — Hào 4 Môn Hộ) HOẶC HƯỚNG CUNG CHỦ «{_huong_tc.upper()}» (Cung {tc} {_quai_tc} · {door_tc}) "
                    f"➔ KHÍ PHONG THỦY: {'VƯỢNG KHÍ TỤ TÀI TỐT' if composite_score >= 50 else 'ĐANG VƯỚNG XUNG KHÍ / CẦN GIỮ SẠCH THOÁNG CỬA RA VÀO'} ({composite_score}/100)!"
                )
            else:
                direct_headline = (
                    f"🧭 ĐỊNH VỊ PHƯƠNG HƯỚNG CHÍNH XÁC TỪ QUẺ ({_ban_bien_lbl}): "
                    f"ỨNG TẠI PHƯƠNG «{_huong_tc.upper()}» (Cung {tc} {_quai_tc} · {door_tc}) KẾT HỢP PHƯƠNG ĐỊA CHI DỤNG THẦN «{_chi_dir_lbl.upper()}» (Chi {dt_chi} — {'ở gần khu vực quen' if dt_idx <= 3 else 'đi xa ra ngoài khu vực'})!"
                )
        elif _is_motive_q:
            special_mode = "HUMAN_MOTIVE"
            _u_thu = str(ung_ln.get("luc_thu") or "Thanh Long")
            _u_lt = str(ung_ln.get("luc_than") or "")
            _u_chi = str(ung_ln.get("chi") or "")
            _am_c = str(pa_tc.get("am_can") or "")
            if (SINH_EL.get(ung_el) == the_el or LUC_HOP.get(_u_chi, ("",""))[0] == the_chi) and not ung_ln.get("is_void") and _u_thu not in ("Huyền Vũ", "Đằng Xà"):
                direct_headline = (
                    f"💡 ĐỌC VỊ TÂM Ý & MỤC ĐÍCH ĐỐI PHƯƠNG ({_ban_bien_lbl}): "
                    f"Ý ĐỒ TỐT & CHÂN THÀNH ({composite_score}/100) — Hào Ứng ({_u_lt} {_u_chi} · {_u_thu}) sinh/hợp Hào Thế, thực tâm muốn kết nối, hỗ trợ hoặc hợp tác nghiêm túc!"
                )
            else:
                _mot_detail = (
                    "nhắm vào lợi ích tiền bạc / vay mượn" if _u_lt in ("Huynh Đệ", "Thê Tài")
                    else ("khéo miệng thăm dò tin tức nhưng lời nói thiếu thực chất" if _u_thu == "Chu Tước" or ung_ln.get("is_void")
                          else "có tính toán ngầm riêng tư, thiếu minh bạch")
                )
                direct_headline = (
                    f"🚨 ĐỌC VỊ TÂM Ý & MỤC ĐÍCH ĐỐI PHƯƠNG ({_ban_bien_lbl}): "
                    f"CẦN CẢNH GIÁC — Ý ĐỒ THIẾU THUẦN KHIẾT ({composite_score}/100): Đối phương ({_u_lt} {_u_chi} · {_u_thu}, Ám Can [{_am_c}]) đang {_mot_detail}; nên giữ khoảng cách và kiểm chứng kỹ!"
                )
        elif _is_why_cause_q:
            special_mode = "WHY_CAUSE_FORENSIC"
            _causes: List[str] = []
            if ky_movers:
                _km0 = ky_movers[0]
                _causes.append(f"Kỵ Thần Hào {_km0['hao']} {_km0['luc_than']} ({_km0['chi']} · {_km0.get('luc_thu','')}) phát động trực tiếp công phá Dụng Thần")
            if any("Huynh Đệ" in str(ln.get("luc_than","")) and (ln.get("is_moving") or ln.get("is_am_dong")) for ln in lines):
                _causes.append("Hào Huynh Đệ kích hoạt gây thất thoát tiền bạc qua bạn bè/cho vay/chi tiêu nóng vội")
            if tu_hai_tc:
                _causes.append(f"Cung {tc} ({_huong_tc}) vướng Tứ Hại Kỳ Môn ({tu_hai_tc[0]}) làm kế hoạch lệch nhịp")
            if not _causes:
                _causes.append(f"{benh_quai} dưới Nguyệt Lệnh {chi_thang} làm khí vận tạm chùng xuống")
            direct_headline = (
                f"🔎 TRUY TÌM CĂN NGUYÊN GỐC RỄ TRÊN BÀN QUẺ ({_ban_bien_lbl}): "
                + "  +  ".join(_causes[:2])
                + f" ➔ CÁCH HÓA GIẢI: Bồi đắp hành Thông Quan ({ng_el or 'Thủy/Mộc'}), giữ chặt tài chính và đợi mốc {_uk_disp}!"
            )
        elif _is_how_remedy_q:
            special_mode = "HOW_TO_REMEDY"
            _cat_cung_list = [f"Cung {p_i} ({p_v.get('huong','')} — {p_v.get('door','')})" for p_i, p_v in p_map_qm.items() if p_i != 5 and any(d in str(p_v.get("door","")) for d in ("Khai", "Hưu", "Sinh")) and not p_v.get("tu_hai")]
            _best_dir_rem = _cat_cung_list[0] if _cat_cung_list else f"Cung {tc} ({_huong_tc} — {door_tc})"
            direct_headline = (
                f"🛡️ PHÁP QUYẾT HÓA GIẢI VẬN HẠN CỔ PHÁP ({_ban_bien_lbl}): "
                f"[1. Mở nút thắt gốc]: {benh_quai} ➔ Dùng hành Nguyên Thần «{(ng_el or the_el).upper()}» để thông quan chuyển hung thành cát  ||  "
                f"[2. Không gian đắc lợi]: Ưu tiên làm việc/xuất hành hướng {_best_dir_rem}  ||  "
                f"[3. Thời điểm chuyển vận]: {_uk_disp} (tạm hoãn cho vay/đầu tư mạo hiểm trước mốc này)!"
            )
        elif _is_who_q:
            special_mode = "WHO_FORENSIC"
            # Đạo Tặc Chương & Nhân Sự Chương: Lấy Quan Quỷ (nếu hỏi trộm/kẻ xấu) hoặc Dụng Thần
            _qq_ln = next((ln for ln in lines if "Quan Quỷ" in str(ln.get("luc_than") or "")), dt_ln)
            _who_ln = _qq_ln if (is_theft_q or any(w in q_low for w in ("nói xấu", "hại", "cản"))) else dt_ln
            _w_hao = int(_who_ln.get("hao") or 3)
            _w_chi = str(_who_ln.get("chi") or dt_chi)
            _w_el = str(_who_ln.get("ngu_hanh") or dt_el)
            _w_thu = str(_who_ln.get("luc_thu") or "Huyền Vũ")
            _w_gender = "NAM GIỚI" if (_w_chi in _YANG_CHIS) else "NỮ GIỚI"
            _w_inout = "NGƯỜI QUEN / NỘI BỘ / RA VÀO GẦN GŨI (ở Nội Quái Hào 1–3)" if _w_hao <= 3 else "NGƯỜI BÊN NGOÀI / KHÁCH VÃNG LAI (ở Ngoại Quái Hào 4–6)"
            _w_age = "trẻ tuổi (khoảng 18–32 tuổi)" if str(_who_ln.get("ts_ngay") or "") in ("Thai", "Dưỡng", "Trường Sinh", "Mộc Dục", "Quan Đái") else ("trung niên (khoảng 33–50 tuổi)" if str(_who_ln.get("ts_ngay") or "") in ("Lâm Quan", "Đế Vượng", "Suy") else "đứng tuổi (trên 48 tuổi)")
            _tuton_act = any("Tử Tôn" in str(ln.get("luc_than") or "") and (ln.get("is_moving") or ln.get("is_am_dong")) for ln in lines)
            if is_theft_q:
                _can_recover = _tuton_act or (not dt_ln.get("is_void") and _who_ln.get("vuong_suy") in ("Hưu", "Tù", "Tử"))
                _rec_str = (
                    f"CÓ CƠ HỘI TÌM LẠI / LỘ THỦ PHẠM (do Tử Tôn chế Quỷ hoặc Quan Quỷ suy lộ tại hướng {_huong_tc} — Cung {tc})"
                    if _can_recover
                    else f"KHÓ ĐÒI LẠI TRỌN VẸN (Quan Quỷ {_w_chi} vượng / Thê Tài vướng cản, đồ đã bị tẩu tán về hướng {_huong_tc})"
                )
                direct_headline = (
                    f"🕵️ TRUY VẾT THỦ PHẠM CHUẨN «ĐẠO TẶC CHƯƠNG» ({_ban_bien_lbl}): "
                    f"ĐỐI TƯỢNG LÀ {_w_gender} ({_w_age.upper()}) — THUỘC NHÓM {_w_inout} "
                    f"[Ứng Hào {_w_hao} Quan Quỷ {_w_chi}-{_w_el} · {_w_thu}: {LUC_THU_ROLE_COLOR.get(_w_thu, '')}] "
                    f"➔ KẾT CỤC: {_rec_str} ({duoc_ung_ky})!"
                )
            else:
                direct_headline = (
                    f"👤 ĐỌC VỊ NHÂN VẬT TỪ QUẺ ({_ban_bien_lbl}): "
                    f"ĐÓ LÀ {_w_gender} ({_w_age.upper()}) — {_w_inout}, MANG KHÍ CHẤT HÀNH {_w_el.upper()} "
                    f"[Ứng Hào {_w_hao} {_who_ln.get('luc_than','')} {_w_chi} · {_w_thu} · Phương {_huong_tc} Cung {tc} ({star_tc} · {door_tc})]!"
                )
        elif _is_where_doing_q:
            special_mode = "WHERE_AND_DOING"
            _p_hao = int(dt_ln.get("hao") or the_pos)
            _p_chi = str(dt_ln.get("chi") or dt_chi)
            _p_thu = str(dt_ln.get("luc_thu") or "Thanh Long")
            _in_home = (_p_hao <= 3) and ("Khai" not in door_tc and "Thương" not in door_tc)
            _DOOR_PLACE = {
                "Hưu": "đang ở nhà / phòng nghỉ ngơi hoặc quán nước yên tĩnh",
                "Sinh": "đang ở nơi kinh doanh, cửa hàng, siêu thị hoặc khu dân cư sầm uất",
                "Thương": "đang di chuyển trên xe ngoài đường hoặc chỗ tập luyện/kỹ thuật",
                "Đỗ": "đang ở trong phòng kín, nơi riêng tư hoặc chỗ làm việc nội bộ ít người",
                "Cảnh": "đang ở quán ăn, nơi sáng đèn đông người hoặc chỗ giao tiếp/truyền thông",
                "Tử": "đang ở chỗ tĩnh lặng, nhà cũ hoặc đang bận tâm việc riêng khép kín",
                "Kinh": "đang ở nơi ồn ào, cơ quan hành chính hoặc đang tranh luận điện thoại",
                "Khai": "đang ở công ty, văn phòng, cửa hàng mở rộng hoặc nơi công cộng lớn",
            }
            _d_short = door_tc.replace(" Môn", "").split()[0]
            _place_desc = _DOOR_PLACE.get(_d_short, "ở khu vực quen thuộc")
            _THU_DOING = {
                "Thanh Long": "ăn uống, mua sắm, gặp gỡ vui vẻ hoặc bàn chuyện tài chính",
                "Chu Tước": "nói chuyện điện thoại, nhắn tin trao đổi hoặc thảo luận công việc",
                "Câu Trần": "xử lý việc tồn đọng, dọn dẹp sắp xếp hoặc làm việc văn phòng/đất đai",
                "Đằng Xà": "suy nghĩ lo toan nhiều việc lặt vặt hoặc di chuyển vòng vèo",
                "Bạch Hổ": "làm việc khẩn trương áp lực cao hoặc đi khám/chăm sóc sức khỏe",
                "Huyền Vũ": "nghỉ ngơi riêng tư, lướt điện thoại kín đáo hoặc giữ việc riêng chưa kể",
            }
            _doing_desc = _THU_DOING.get(_p_thu, "xử lý công việc cá nhân")
            direct_headline = (
                f"📍 ĐỊNH VỊ KHÔNG GIAN & HOẠT ĐỘNG TỨC THỜI ({_ban_bien_lbl}): "
                f"[1. ĐANG Ở ĐÂU]: {'TRONG NHÀ / GẦN CHỖ QUEN' if _in_home else 'BÊN NGOÀI / ĐANG ĐI RA NGOÀI'} — {_place_desc.upper()} TẠI HƯỚNG {_huong_tc.upper()} "
                f"(Cung {tc} {door_tc} · Hào {_p_hao} {_p_chi}: {CHI_CONCRETE_IMAGE.get(_p_chi, '')})  ||  "
                f"[2. ĐANG LÀM GÌ]: ĐANG {_doing_desc.upper()} (Ứng {_p_thu} · Sao {star_tc} · Quẻ Biến {mh_res.get('ten_bien','')})!"
            )
        elif _is_what_obj_q:
            special_mode = "WHAT_OBJECT_XAPHU"
            _TRIG_CONCRETE_OBJS = {
                "Càn": "đồng hồ, chìa khóa, máy tính/vỏ kim loại tròn cứng hoặc vật có giá trị cao",
                "Đoài": "cốc tách có miệng mở, tai nghe/loa, chìa khóa, dao kéo nhỏ hoặc đồ kim khí tinh xảo",
                "Ly": "điện thoại di động, màn hình sáng, bộ sạc/đèn, bật lửa hoặc tập giấy tờ/thẻ màu nổi",
                "Chấn": "thiết bị điện tử có âm thanh/rung (điện thoại/điều khiển), bút viết hoặc vật bằng gỗ/nhựa dài",
                "Tốn": "sổ tay, xấp tài liệu/hóa đơn, dây cáp sạc, hộp giấy hoặc khăn/túi vải mỏng",
                "Khảm": "chai nước, ly trà/cà phê/nước uống, lọ dung dịch hoặc vật màu đen/trong suốt",
                "Cấn": "chuột máy tính, hộp đựng kín, cốc gốm sứ dày, cục sạc vuông hoặc chồng vật dụng đặt yên",
                "Khôn": "ví tiền, túi vải/da mềm, hộp nhựa vuông, khăn giấy hoặc đồ ăn nhẹ trên bàn",
            }
            _MAT_BY_EL = {
                "Kim": "bằng KIM LOẠI / HỢP KIM / VỎ CỨNG SÁNG BÓNG (màu trắng, bạc, xám ánh kim), hình tròn hoặc sắc cạnh",
                "Mộc": "bằng GỖ / GIẤY VỞ / VẢI SỢI (màu xanh lá, nâu gỗ), dáng thon dài hoặc xếp lớp",
                "Thủy": "chứa CHẤT LỎNG / THỦY TINH / NHỰA MỀM (màu đen, xanh dương, trong suốt)",
                "Hỏa": "là THIẾT BỊ ĐIỆN TỬ PHÁT SÁNG–NHIỆT hoặc văn thư (màu đỏ, cam, tím, sáng màn hình)",
                "Thổ": "bằng GỐM SỨ / NHỰA ĐẶC / DA VẢI VUÔNG VỨC (màu vàng, nâu đất, kem)",
            }
            _obj_top = _TRIG_CONCRETE_OBJS.get(_up_m_q, "vật dụng cầm tay")
            _obj_bot = _TRIG_CONCRETE_OBJS.get(_lo_m_q, "đồ để bàn")
            _dom_el_obj = TRIGRAM_META_8.get(_up_b_q, TRIGRAM_META_8["Càn"])[3]
            _combo_obj = _obj_top if _up_m_q == _lo_m_q else f"{_obj_top} đặt cùng/trên {_obj_bot}"
            direct_headline = (
                f"🔍 XẠ PHÚC ĐỌC VỊ ĐỒ VẬT CHUẨN MAI HOA & KỲ MÔN ({_ban_bien_lbl}): "
                f"TRƯỚC MẶT BẠN LÀ «{_combo_obj.upper()}» — "
                f"CHẤT LIỆU & MÀU SẮC CHỦ ĐẠO: {_MAT_BY_EL.get(_dom_el_obj, '').upper()} "
                f"(Thượng {_up_m_q} · Hạ {_lo_m_q} biến {_up_b_q}/{_lo_b_q} · Cung {tc} {star_tc} · {door_tc})!"
            )
        elif _is_job_fit_q:
            special_mode = "CAREER_BIZ_FIT"
            # Tìm Hành Hỷ Dụng tốt nhất cho Tài Lộc & Bản Thân: Nguyên Thần sinh Thế hoặc Hành Thê Tài!
            _tai_el_fit = KHAC_EL.get(the_el, "Kim")
            _ng_the_fit = next((k for k, v in SINH_EL.items() if v == the_el), "Thủy")
            _IND_BY_EL = {
                "Kim": "Tài chính – Ngân hàng – Đầu tư, Cơ khí – Ô tô – Thiết bị kỹ thuật, Vàng bạc – Trang sức, Quản trị điều hành, Pháp chế",
                "Mộc": "Giáo dục – Đào tạo, Dược phẩm – Y tế – Đông y, Nội thất – Gỗ – Nông sản sạch, Thời trang – Thiết kế sáng tạo, Xuất bản",
                "Thủy": "Thương mại XNK – Logistics – Vận tải, Kinh doanh Online / Phân phối lưu động, Dịch vụ Du lịch – Đồ uống – Thủy hải sản",
                "Hỏa": "Công nghệ AI – Phần mềm – Điện tử, Truyền thông – Marketing – Livestream, Ẩm thực – Nhà hàng, Thẩm mỹ – Làm đẹp, Năng lượng",
                "Thổ": "Bất động sản – Xây dựng – Kiến trúc, Kho bãi – Sản xuất nguyên vật liệu, Kinh doanh mặt bằng/cửa hàng cố định, Nông nghiệp",
            }
            _coop_mode = "nên LÀM ĐỘC LẬP TỰ CHỦ (tránh hùn vốn đông người dễ hao hụt)" if any("Huynh Đệ" in str(ln.get("luc_than","")) and ln.get("is_moving") for ln in lines) else "rất hợp MỞ RỘNG HỢP TÁC ĐỐI TÁC / KHÁCH HÀNG LỚN"
            direct_headline = (
                f"💼 ĐỊNH VỊ NGÀNH NGHỀ VƯỢNG TÀI NHẤT TỪ BÀN QUẺ ({_ban_bien_lbl}): "
                f"[MŨI NHỌN SỐ 1 — HÀNH TÀI LỘC ({_tai_el_fit.upper()})]: «{_IND_BY_EL.get(_tai_el_fit, '').upper()}»  ||  "
                f"[MŨI NHỌN BỔ TRỢ — HÀNH QUÝ NHÂN SINH MỆNH ({_ng_the_fit.upper()})]: «{_IND_BY_EL.get(_ng_the_fit, '').upper()}» "
                f"➔ PHƯƠNG THỨC ĐẮC LỘC: {_coop_mode.upper()}, ƯU TIÊN PHÁT TRIỂN HƯỚNG {_huong_tc.upper()} (Cung {tc} {door_tc} · {star_tc})!"
            )
        elif _is_event_risk_q:
            special_mode = "WHAT_EVENT_RISK"
            _ev_alerts: List[str] = []
            _is_work_ev = any(w in q_low for w in ("công việc", "sự nghiệp", "cơ quan", "công ty", "đi làm", "kinh doanh"))
            for _ln_e in lines:
                if _ln_e.get("is_moving") or _ln_e.get("is_am_dong"):
                    _lt_e = str(_ln_e.get("luc_than") or "")
                    _th_e = str(_ln_e.get("luc_thu") or "")
                    _ch_e = str(_ln_e.get("chi") or "")
                    _mv_tag_e = "động" if _ln_e.get("is_moving") else "ám động"
                    if _lt_e == "Huynh Đệ":
                        _ev_alerts.append(
                            f"CÓ CẠNH TRANH ĐỒNG NGHIỆP / CHIA LẠI QUYỀN LỢI HOẶC PHÁT SINH CHI PHÍ CÔNG VIỆC (Hào {_ln_e['hao']} Huynh Đệ {_ch_e} {_mv_tag_e})"
                            if _is_work_ev
                            else f"ĐỀ PHÒNG HAO TÀI / CHI TIÊU LỚN HOẶC CHO VAY KHÓ ĐÒI (Hào {_ln_e['hao']} Huynh Đệ {_ch_e} {_mv_tag_e})"
                        )
                    elif _lt_e == "Quan Quỷ":
                        if _th_e == "Chu Tước":
                            _ev_alerts.append(f"XẢY RA HỌP RÀ SOÁT / TRANH LUẬN GIẤY TỜ – QUY CHẾ CẦN GIỮ BÌNH TĨNH LỜI NÓI (Hào {_ln_e['hao']} Quan Quỷ {_ch_e} lâm Chu Tước {_mv_tag_e})")
                        elif _th_e == "Bạch Hổ":
                            _ev_alerts.append(
                                f"ÁP LỰC CHỈ TIÊU GẮT GAO TỪ CẤP TRÊN & CHÚ Ý SỨC KHỎE ĐI LẠI (Hào {_ln_e['hao']} Quan Quỷ {_ch_e} lâm Bạch Hổ {_mv_tag_e})"
                                if _is_work_ev
                                else f"CHÚ Ý SỨC KHỎE NGƯỜI TRONG NHÀ & ĐI LẠI CẨN TRỌNG (Hào {_ln_e['hao']} Quan Quỷ {_ch_e} lâm Bạch Hổ {_mv_tag_e})"
                            )
                        elif _th_e == "Huyền Vũ":
                            _ev_alerts.append(f"CẢNH GIÁC SAI SÓT SỔ SÁCH NGẦM / MẤT ĐỒ HOẶC NGƯỜI CHƠI XẤU SAU LƯNG (Hào {_ln_e['hao']} Quan Quỷ {_ch_e} lâm Huyền Vũ {_mv_tag_e})")
                        else:
                            _ev_alerts.append(
                                f"CÓ BIẾN ĐỘNG TỪ CẤP QUẢN LÝ: ĐIỀU CHỈNH PHÂN CÔNG / RÀ SOÁT QUY TRÌNH CÔNG VIỆC (Hào {_ln_e['hao']} Quan Quỷ {_ch_e} {_mv_tag_e})"
                                if _is_work_ev
                                else f"CẦN LƯU TÂM SỨC KHỎE NGƯỜI TRONG NHÀ, LO ÂU TÂM LÝ HOẶC TRỤC TRẶC ĐIỆN NƯỚC – GIẤY TỜ GIA ĐẠO (Hào {_ln_e['hao']} Quan Quỷ {_ch_e} · {_th_e} {_mv_tag_e})"
                            )
                    elif _lt_e == "Phụ Mẫu":
                        _ev_alerts.append(
                            f"THAY ĐỔI VĂN BẢN HỢP ĐỒNG, QUYẾT ĐỊNH ĐIỀU CHUYỂN PHÒNG BAN HOẶC HỒ SƠ DỰ ÁN (Hào {_ln_e['hao']} Phụ Mẫu {_ch_e} {_mv_tag_e})"
                            if _is_work_ev
                            else f"BẬN RỘN GIẤY TỜ PHÁP LÝ, SỬA SANG NHÀ CỬA/XE CỘ HOẶC LO SỨC KHỎE BẬC TRƯỞNG BỐI (Hào {_ln_e['hao']} Phụ Mẫu {_ch_e} {_mv_tag_e})"
                        )
                    elif _lt_e == "Thê Tài":
                        _ev_alerts.append(f"CHUYỂN ĐỘNG DÒNG TIỀN: ĐÓN KHOẢN THU / THƯỞNG MỚI HOẶC ĐIỀU CHỈNH NGÂN SÁCH (Hào {_ln_e['hao']} Thê Tài {_ch_e} {_mv_tag_e})")
                    elif _lt_e == "Tử Tôn":
                        _ev_alerts.append(
                            f"MỞ HƯỚNG LÀM VIỆC TỰ CHỦ MỚI & CÓ QUÝ NHÂN GIẢI ÁP LỰC (Hào {_ln_e['hao']} Tử Tôn {_ch_e} {_mv_tag_e})"
                            if _is_work_ev
                            else f"CÓ PHÚC THẦN HÓA GIẢI TAI ÁCH, TIN VUI CON CÁI / BÌNH AN (Hào {_ln_e['hao']} Tử Tôn {_ch_e} {_mv_tag_e})"
                        )
            if not _ev_alerts:
                _ctx_lbl = "CÔNG VIỆC GIỮ NHỊP ỔN ĐỊNH, CHƯA CÓ XÁO TRỘN LỚN" if _is_work_ev else "GIA ĐẠO NHÌN CHUNG YÊN ỔN"
                _ev_alerts.append(f"{_ctx_lbl} — CHỈ CẦN LƯU Ý KHÂU {dung_than.upper()} ({benh_quai}) TẠI HƯỚNG {_huong_tc.upper()}")
            direct_headline = (
                f"🔮 TIÊN ĐOÁN SỰ VIỆC XẢY RA SÁT QUẺ ({_ban_bien_lbl} — {composite_score}/100): "
                + "  |  ".join(_ev_alerts[:2])
                + (f"  |  [{_rel_real_short}]" if _rel_real_short else "")
                + f" ➔ THỜI ĐIỂM XẢY RA CHÍNH XÁC: {_uk_disp}!"
            )
        elif _is_how_outlook_q:
            special_mode = "DETAILED_OUTLOOK"
            _h5_ln = lines[4] if len(lines) >= 5 else {}
            _h5_note = f"Cấp trên/Chính chủ (Hào 5 {_h5_ln.get('luc_than','')} {_h5_ln.get('chi','')}) đang {'phát động xoay chuyển' if _h5_ln.get('is_moving') else ('tạm giữ ý chưa quyết' if _h5_ln.get('is_void') else 'ổn định')}" if _h5_ln else ""
            _mv_lines_ol = [ln for ln in lines if ln.get("is_moving")]
            _turn_note = (
                f"Bước ngoặt nằm ở Hào {_mv_lines_ol[0]['hao']} {_mv_lines_ol[0]['luc_than']} ({_mv_lines_ol[0]['chi']}) động hóa {_mv_lines_ol[0]['bien_luc_than']} ({_mv_lines_ol[0]['bien_chi']})"
                if _mv_lines_ol else f"Quẻ tĩnh giữ nhịp theo Cung {tc} ({door_tc} · {star_tc})"
            )
            if composite_score >= 56:
                verdict_polarity = "OUTLOOK_GOOD"
                direct_headline = (
                    f"🌟 TOÀN CẢNH SỰ VIỆC SẮP TỚI ({_ban_bien_lbl} — {composite_score}/100 KHỞI SẮC TỐT): "
                    f"[1. Sự việc]: {_ev_real_short or _core_reason_1}{'; ' + _h5_note if _h5_note else ''}  |  "
                    f"[2. Chuyển biến]: {_turn_note}, Cung {tc} đắc {door_tc} · {star_tc}  |  "
                    f"[3. Thời điểm nổ]: {_uk_disp}!"
                )
            elif composite_score >= 46:
                verdict_polarity = "OUTLOOK_MIXED"
                direct_headline = (
                    f"⚖️ TOÀN CẢNH SỰ VIỆC SẮP TỚI ({_ban_bien_lbl} — {composite_score}/100 TRƯỚC CHẬM SAU THÔNG): "
                    f"[1. Điểm nghẽn thực tế]: {_ev_real_short or benh_quai}{'; ' + _h5_note if _h5_note else ''}  |  "
                    f"[2. Chuyển biến]: {_turn_note}  |  "
                    f"[3. Thời điểm tháo gỡ]: {_uk_disp}!"
                )
            else:
                verdict_polarity = "OUTLOOK_HARD"
                direct_headline = (
                    f"⚠️ TOÀN CẢNH SỰ VIỆC SẮP TỚI ({_ban_bien_lbl} — {composite_score}/100 ĐANG GẶP SỨC ÉP): "
                    f"[1. Sự việc cần lường trước]: {_ev_real_short or _core_reason_1}  |  "
                    f"[2. Điểm xoay cục diện]: {_turn_note}  |  "
                    f"[3. Mốc mở khóa]: {_uk_disp} (Nên thủ thế chắc chắn, tránh mạo hiểm lúc này)!"
                )
        elif any(w in q_low for w in ["hợp đồng", "ký kết", "chốt đơn", "đàm phán"]):
            if composite_score >= 52:
                verdict_polarity = "SUCCESS"
                direct_headline = f"📝 LUẬN ĐOÁN HỢP ĐỒNG & GIAO DỊCH ({_ban_bien_lbl}): KÝ KẾT THÀNH CÔNG ({composite_score}/100 — {_ev_real_short or _core_reason_1}) ➔ Thời điểm chốt thuận lợi: {_uk_disp}!"
            else:
                verdict_polarity = "BLOCKED"
                direct_headline = f"⚠️ LUẬN ĐOÁN HỢP ĐỒNG & GIAO DỊCH ({_ban_bien_lbl}): HIỆN TẠI VƯỚNG ĐIỀU KHOẢN / CHƯA CHỐT NGAY ĐƯỢC ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ Cần tháo gỡ và đợi {_uk_disp}!"
        elif is_wealth_q:
            if composite_score >= 58:
                verdict_polarity = "PROFIT"
                direct_headline = f"💰 LUẬN ĐOÁN CẦU TÀI & ĐẦU TƯ CỔ PHÁP ({_ban_bien_lbl}): ĐẮC TÀI / SINH LỜI TỐT ({composite_score}/100 — {_ev_real_short or _core_reason_1}) ➔ Ứng kỳ thu lợi: {_uk_disp}!"
            elif composite_score >= 50:
                verdict_polarity = "CAUTIOUS_PROFIT"
                direct_headline = f"⚖️ LUẬN ĐOÁN CẦU TÀI & ĐẦU TƯ CỔ PHÁP ({_ban_bien_lbl}): CÓ LỘC NHƯNG TRƯỚC NGHẼN SAU THÔNG ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ Chờ đúng mốc {_uk_disp} mới thu lời an toàn!"
            else:
                verdict_polarity = "LOSS_RISK"
                direct_headline = f"🚨 CẢNH BÁO CẦU TÀI & ĐẦU TƯ CỔ PHÁP ({_ban_bien_lbl}): BẤT LỢI / DỄ HAO TÀI KẸT VỐN NẾU LÀM GẤP ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ TẠM HOÃN XUỐNG TIỀN LỚN, CHỜ MỐC MỞ KHÓA: {_uk_disp}!"
        elif any(w in q_low for w in ["giao dịch", "thương vụ"]):
            if composite_score >= 52:
                verdict_polarity = "SUCCESS"
                direct_headline = f"📝 LUẬN ĐOÁN HỢP ĐỒNG & GIAO DỊCH ({_ban_bien_lbl}): KÝ KẾT THÀNH CÔNG ({composite_score}/100 — {_ev_real_short or _core_reason_1}) ➔ Thời điểm chốt thuận lợi: {_uk_disp}!"
            else:
                verdict_polarity = "BLOCKED"
                direct_headline = f"⚠️ LUẬN ĐOÁN HỢP ĐỒNG & GIAO DỊCH ({_ban_bien_lbl}): HIỆN TẠI VƯỚNG ĐIỀU KHOẢN / CHƯA CHỐT NGAY ĐƯỢC ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ Cần tháo gỡ và đợi {_uk_disp}!"
        elif any(w in q_low for w in ["thi ", "đỗ", "đậu", "ứng tuyển", "xin việc", "phỏng vấn", "thăng chức"]):
            if composite_score >= 50:
                verdict_polarity = "PASS"
                direct_headline = f"🎓 LUẬN ĐOÁN CÔNG DANH & KHOA CỬ ({_ban_bien_lbl}): ĐẠT KẾT QUẢ TỐT / ĐỖ ĐẠT ({composite_score}/100 — {_ev_real_short or _core_reason_1}; Cung {tc} {star_tc} · {door_tc}) ➔ Ứng kỳ báo tin: {_uk_disp}!"
            else:
                verdict_polarity = "FAIL_RISK"
                direct_headline = f"⚠️ LUẬN ĐOÁN CÔNG DANH & KHOA CỬ ({_ban_bien_lbl}): GẶP SỨC ÉP LỚN / KHÓ ĐẠT NGAY ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ Củng cố hồ sơ/năng lực và chờ {_uk_disp}!"
        elif any(w in q_low for w in ["tình cảm", "yêu", "hôn nhân", "quay lại", "hàn gắn", "làm lành", "vợ chồng", "cưới", "nhớ tôi"]):
            _ung_chi_s = str(ung_ln.get("chi", ""))
            _ung_sinh_hop_the = (SINH_EL.get(ung_el) == the_el or ung_el == the_el or LUC_HOP.get(_ung_chi_s, ("", ""))[0] == the_chi) and not ung_ln.get("is_void")
            _ung_void_or_khac = bool(ung_ln.get("is_void") or KHAC_EL.get(ung_el) == the_el)
            if composite_score >= 50 and _ung_sinh_hop_the:
                verdict_polarity = "HARMONY"
                direct_headline = f"💞 LUẬN ĐOÁN TÌNH DUYÊN CỔ PHÁP ({_ban_bien_lbl}): THUẬN DUYÊN / CÒN TÌNH Ý CHÂN THÀNH & DỄ LÀM LÀNH ({composite_score}/100 — Hào Ứng {_ung_chi_s}-{ung_el} sinh/hợp Hào Thế {the_chi}-{the_el}, duyên khí tương thông) ➔ Mốc gắn kết tốt: {_uk_disp}!"
            elif composite_score >= 50 and _ung_void_or_khac:
                verdict_polarity = "MIXED_HESITANT_LOVE"
                _hes_why = (
                    f"Dụng Thần vượng khí chứng tỏ duyên nợ/kỷ niệm chưa dứt hẳn, song Hào Ứng ({_ung_chi_s}-{ung_el}) "
                    + ("lâm Tuần Không nên lòng người ấy còn chênh vênh, chưa dám tiến tới ngay" if ung_ln.get("is_void") else f"tạm khắc Hào Thế ({the_chi}-{the_el}) nên còn tự ái/căng thẳng bề ngoài")
                )
                direct_headline = f"💞 LUẬN ĐOÁN TÌNH DUYÊN CỔ PHÁP ({_ban_bien_lbl}): DUYÊN CHƯA DỨT HẲN NHƯNG CÒN TỰ ÁI / NGẦN NGẠI CHƯA MỞ LỜI NGAY ({composite_score}/100 — {_hes_why}) ➔ Mốc hóa giải & kết nối lại: {_uk_disp}!"
            elif composite_score >= 50:
                verdict_polarity = "HARMONY"
                direct_headline = f"💞 LUẬN ĐOÁN TÌNH DUYÊN CỔ PHÁP ({_ban_bien_lbl}): CÓ CƠ HỘI HÀN GẮN & HÒA HỢP LẠI ({composite_score}/100 — Thế {the_chi}-{the_el} & Ứng {_ung_chi_s}-{ung_el} giữ mạch duyên ổn định, Quẻ Biến nâng đỡ) ➔ Mốc gắn kết tốt: {_uk_disp}!"
            elif _ung_sinh_hop_the:
                verdict_polarity = "LINGERING_LOVE"
                direct_headline = f"💞 LUẬN ĐOÁN TÌNH DUYÊN CỔ PHÁP ({_ban_bien_lbl}): TRONG LÒNG VẪN CÒN NHỚ & VƯƠNG VẤN NHƯNG ĐANG VƯỚNG RÀO CẢN NGOẠI CẢNH ({composite_score}/100 — Hào Ứng sinh/hợp Thế nhưng cản trở tại: {benh_quai}) ➔ Mốc mở lời kết nối lại: {_uk_disp}!"
            else:
                verdict_polarity = "CONFLICT"
                _conf_why = "Hào Ứng lâm Tuần Không / khắc Hào Thế — tâm ý đang nguôi ngoai hoặc xa cách" if _ung_void_or_khac else f"Thế ({the_chi}-{the_el}) & Ứng ({_ung_chi_s}-{ung_el}) đang lệch nhịp"
                direct_headline = f"💔 LUẬN ĐOÁN TÌNH DUYÊN CỔ PHÁP ({_ban_bien_lbl}): ĐANG XA CÁCH / KHÓ HÀN GẮN NGAY ({composite_score}/100 — {_conf_why}; {benh_quai}) ➔ Điểm mở nút thắt: {_uk_disp}!"
        elif is_travel_any:
            if composite_score >= 50:
                verdict_polarity = "SAFE_TRIP"
                direct_headline = f"🧭 LUẬN ĐOÁN XUẤT HÀNH & DI CHUYỂN ({_ban_bien_lbl}): THƯỢNG LỘ BÌNH AN & ĐẮC VIỆC ({composite_score}/100 — {_core_reason_1}; Cung {tc} {door_tc}) ➔ Khung giờ & ngày đẹp: {_uk_disp}!"
            else:
                verdict_polarity = "DELAY_TRIP"
                direct_headline = f"⚠️ LUẬN ĐOÁN XUẤT HÀNH & DI CHUYỂN ({_ban_bien_lbl}): DỄ TRỄ NHỊP / VƯỚNG ĐƯỜNG XÁ THỦ TỤC ({composite_score}/100 — {benh_quai}; Cung {tc} {door_tc}) ➔ Chuẩn bị kỹ phương tiện và chọn {_uk_disp}!"
        elif any(w in q_low for w in ("kiện", "tòa án", "tranh chấp", "đấu thầu")):
            if composite_score >= 52:
                verdict_polarity = "LAWSUIT_WIN"
                direct_headline = f"⚖️ LUẬN ĐOÁN TRANH CHẤP & PHÁP LÝ ({_ban_bien_lbl}): BÊN BẠN (HÀO THẾ {the_chi}-{the_el}) ĐẮC LÝ CHIẾM ƯU THẾ ({composite_score}/100 — {_ev_real_short or _core_reason_1}) ➔ Mốc phân xử thuận lợi: {_uk_disp}!"
            else:
                verdict_polarity = "LAWSUIT_CAUTION"
                direct_headline = f"⚠️ LUẬN ĐOÁN TRANH CHẤP & PHÁP LÝ ({_ban_bien_lbl}): ĐỐI PHƯƠNG (HÀO ỨNG {ung_ln.get('chi','')}-{ung_el}) ĐANG CỨNG — NÊN ƯU TIÊN THƯƠNG LƯỢNG HÒA GIẢI ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ Mốc tháo gỡ: {_uk_disp}!"
        elif not any(w in q_low for w in ("hướng nào",)):
            if composite_score >= 50:
                verdict_polarity = "AUSPICIOUS"
                direct_headline = f"✅ LUẬN ĐOÁN SỰ VIỆC TAM THỨC ({_ban_bien_lbl}): THUẬN LỢI THÀNH SỰ ({composite_score}/100 — {_ev_real_short or _core_reason_1}) ➔ Ứng nghiệm vào: {_uk_disp}!"
            else:
                verdict_polarity = "INAUSPICIOUS"
                direct_headline = f"⚠️ LUẬN ĐOÁN SỰ VIỆC TAM THỨC ({_ban_bien_lbl}): HIỆN ĐANG VƯỚNG NÚT THẮT CHƯA THÔNG ({composite_score}/100 — {_ev_real_short or benh_quai}) ➔ Chìa khóa mở cục: {_uk_disp}!"

    _4p_prompt_addon = ""
    if _four_pillars:
        _4p_prompt_addon = (
            f"=== 4 TRỤ CỘT TIÊN TRI CHỐNG LUẬN ẢO ĐÃ TÍNH CHUẨN TỪ QUẺ & LỊCH THIÊN VĂN (BẮT BUỘC BÁM SÁT, CẤM BỊA NGÀY GIỜ TRÁI LỊCH NÀY) ===\n"
            f"- [Trụ 1 - Sự việc thực tế xảy ra]: {_four_pillars.get('pillar1_plain','')}\n"
            f"- [Trụ 2 - Liên quan đến cái gì & ai]: {_four_pillars.get('pillar2_plain','')}\n"
            f"- [Trụ 3 - Ngày Giờ Tháng Năm Dương/Âm lịch chính xác]: {_four_pillars.get('pillar3_plain','')}\n"
            f"- [Trụ 4 - Giải pháp thực tế & hóa giải]: {_four_pillars.get('pillar4_plain','')}\n"
        )

    prompt_synthesis_block = (
        "=== HỘI ĐỒNG ĐẠI SƯ LUẬN QUẺ BIỆN CHỨNG TẦNG SÂU V143.0 (TĂNG SAN BỐC DỊCH · NGỰ ĐỊNH KỲ MÔN · MAI HOA DỊCH SỐ — CHỐNG LUẬN ẢO) ===\n"
        f"1. [Điểm Khí Lực Thực Chiến Tam Thức]: Hợp nhất = {composite_score}/100 (Lục Hào 4 tầng = {lh_norm}/100 · Kỳ Môn Chủ-Khách/Tứ Hại = {qm_norm}/100 · Mai Hoa Đảng Thể/Dụng = {mh_norm}/100).\n"
        f"2. [Chuỗi Sinh Khắc Cứu Ứng Lục Hào (Tăng San Bốc Dịch)]: {' | '.join(lh_chain_notes)}.\n"
        f"3. [Biện Chứng Chủ-Khách & Tứ Hại Kỳ Môn (Ngự Định Kỳ Môn Bảo Giám)]: {' | '.join(qm_notes) or f'Cung {tc} ({door_tc}, {star_tc}, {deity_tc}) vận hành ổn định'}.\n"
        f"4. [Chẩn Đoán BỆNH – DƯỢC ỨNG KỲ PHÁP (病药应期)]: {benh_quai} ══► {duoc_ung_ky} ({_uk_disp}).\n"
        + (f"5. {longevity_guide_note}\n" if longevity_guide_note else "")
        + (f"6. [Tham Khảo Tượng Số Chuyên Biệt ({special_mode}) — Đại sư tự đối chiếu toàn bàn để chốt]: {direct_headline}\n" if direct_headline else "")
        + _4p_prompt_addon
    )

    return {
        "special_mode": special_mode,
        "verdict_polarity": verdict_polarity,
        "composite_score": composite_score,
        "lh_score": lh_norm,
        "qm_score": qm_norm,
        "mh_score": mh_norm,
        "already_happened": already_happened,
        "is_wealth_q": is_wealth_q,
        "multi_options": multi_opts,
        "benh_quai": benh_quai,
        "duoc_ung_ky": duoc_ung_ky,
        "short_inline_date": _uk_disp,
        "four_pillars": _four_pillars,
        "lh_chain_notes": lh_chain_notes,
        "qm_notes": qm_notes,
        "direct_headline": direct_headline,
        "prompt_synthesis_block": prompt_synthesis_block,
    }


def build_unified_causal_diagram_and_micro_audit(
    chart_data: Optional[Dict[str, Any]],
    luc_hao_data: Optional[Dict[str, Any]],
    mai_hoa_data: Optional[Dict[str, Any]],
    dung_than: str = "Bản Thân",
    topic: str = "Chung",
    question: str = "",
    target_cung: Optional[int] = None,
    ai_verdict_overrides: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    V133.2 MASTER SYNTHESIS:
    Biến ô '══► KẾT QUẢ' cuối mỗi Sơ Đồ Mũi Tên (Lục Hào · Kỳ Môn · Mai Hoa + Sơ Đồ Hợp Nhất Tam Thức)
    thành PHẦN TRỰC TIẾP GIẢI ĐÁP CÂU HỎI CHÍNH thông qua cơ chế tác động nhân quả từng yếu tố của từng loại quẻ!
    """
    import re as _re_ug
    ai_ov = ai_verdict_overrides if isinstance(ai_verdict_overrides, dict) else {}
    q_clean_disp = _html.escape(str(question or "").strip())

    ly_res = analyze_liuyao_exhaustive_micro_graph(
        luc_hao_data or {}, dung_than=dung_than, topic=topic, question=question, chart_data=chart_data
    )
    qm_res = analyze_qimen_exhaustive_micro_graph(
        chart_data or {}, target_cung=target_cung, dung_than=dung_than, topic=topic, question=question
    )
    mh_res = analyze_meihua_exhaustive_micro_graph(
        mai_hoa_data or {}, chart_data=chart_data, topic=topic, question=question, luc_hao_data=luc_hao_data
    )

    all_edges = list(ly_res["directed_edges"]) + list(qm_res["directed_edges"]) + list(mh_res["directed_edges"])
    deep_syn = synthesize_deep_classical_verdict(
        ly_res=ly_res,
        qm_res=qm_res,
        mh_res=mh_res,
        chart_data=chart_data,
        dung_than=dung_than,
        question=question,
    )

    tc = qm_res["target_cung"]
    qm_tc_audit = qm_res["palace_micro_audit"].get(tc, {})
    p_end_km = qm_res["phien_cung_chain"][-1]
    qm_end_audit = qm_res["palace_micro_audit"].get(p_end_km, qm_tc_audit)
    dt_idx = ly_res["dt_hao_idx"]
    ly_dt_audit = ly_res["line_micro_audit"][dt_idx - 1]
    the_audit = ly_res["line_micro_audit"][ly_res["the_pos"] - 1]

    # ── XÂY DỰNG 4 Ô '══► KẾT QUẢ GIẢI ĐÁP CÂU HỎI CHÍNH' CHO TỪNG LOẠI QUẺ & TAM THỨC HỢP NHẤT ──
    lh_sc = int(deep_syn["lh_score"])
    qm_sc = int(deep_syn["qm_score"])
    mh_sc = int(deep_syn["mh_score"])
    comp_sc = int(deep_syn["composite_score"])

    raw_final_hl = str(ai_ov.get("headline") or deep_syn.get("direct_headline") or "").strip()
    clean_final_hl = _re_ug.sub(r"<[^>]+>", "", raw_final_hl).strip()
    if not clean_final_hl:
        if comp_sc >= 60:
            clean_final_hl = f"THUẬN LỢI / ĐẮC QUẺ ({comp_sc}%) — Tín hiệu 3 quẻ nâng đỡ rõ rệt cho câu hỏi!"
        elif comp_sc >= 46:
            clean_final_hl = f"CÓ CƠ HỘI NHƯNG CẦN ĐÚNG THỜI ĐIỂM MỞ KHÓA ({comp_sc}%)!"
        else:
            clean_final_hl = f"ĐANG VƯỚNG LỰC CẢN / CHƯA THÀNH NGAY ({comp_sc}%) — Cần hóa giải điểm nghẽn trước!"

    # 1) Ô Kết Quả Sơ Đồ 1 — Lục Hào giải đáp câu hỏi như thế nào?
    lh_col = "#22c55e" if lh_sc >= 56 else ("#fbbf24" if lh_sc >= 45 else "#ef4444")
    lh_stance = "BÁO THUẬN / THÀNH" if lh_sc >= 56 else ("BÁO CHỜ THỜI MỞ NÚT THẮT" if lh_sc >= 45 else "BÁO CẢN TRỞ / NGƯỢC Ý")
    lh_ans_title = f"Luận giải Lục Hào ({lh_sc}/100 — {lh_stance}): {ly_res['ban_name']} ➔ {ly_res['bien_name']}"
    if ai_ov.get("liuyao_box"):
        lh_ans_detail = f"<b>Tác động hào giải đáp câu hỏi:</b> {ai_ov['liuyao_box']}"
    else:
        lh_chain_short = " ➔ ".join(deep_syn["lh_chain_notes"][:3])
        lh_ans_detail = (
            f"<b>Cơ chế tác động trả lời câu hỏi:</b> {lh_chain_short}. "
            + (f"<b>Liên kết nổi bật:</b> {ly_res['global_formations'][0]}. " if ly_res["global_formations"] else "")
            + f"<b>Chốt ứng kỳ Lục Hào:</b> {deep_syn['duoc_ung_ky']}."
        )
    custom_lh_out = _render_outcome_box(
        lh_ans_title,
        lh_ans_detail,
        lh_col,
        header_badge="══► KẾT QUẢ LỤC HÀO GIẢI ĐÁP CÂU HỎI CHÍNH",
    )

    # 2) Ô Kết Quả Sơ Đồ 2 — Kỳ Môn giải đáp câu hỏi như thế nào?
    qm_col = "#22c55e" if qm_sc >= 56 else ("#fbbf24" if qm_sc >= 45 else "#ef4444")
    qm_stance = "CỬA THÔNG / ĐẮC LỢI" if qm_sc >= 56 else ("CẦN LÁCH TỨ HẠI / CHỜ THỜI" if qm_sc >= 45 else "CỬA NGHẼN / NHIỀU LỰC ÉP")
    qm_ans_title = (
        f"Luận giải Kỳ Môn ({qm_sc}/100 — {qm_stance}): Cung {tc} {qm_tc_audit.get('door','')} ➔ Hạ màn Cung {p_end_km} {qm_end_audit.get('door','')}"
    )
    if ai_ov.get("qimen_box"):
        qm_ans_detail = f"<b>Tác động Cửu Cung giải đáp câu hỏi:</b> {ai_ov['qimen_box']}"
    else:
        qm_chain_short = " · ".join(deep_syn["qm_notes"][:2]) if deep_syn["qm_notes"] else qm_res["ck_desc"]
        qm_ans_detail = (
            f"<b>Cơ chế Chủ–Khách & Tinh–Môn trả lời câu hỏi:</b> {qm_chain_short}. "
            f"Cung sự việc hội <b>{qm_tc_audit.get('star','')} · {qm_tc_audit.get('door','')} · {qm_tc_audit.get('deity','')}</b>, "
            f"Ám Can <b>[{qm_tc_audit.get('am_can','')}]</b> ({qm_tc_audit.get('am_can_meaning','')}), lật 4 trạm chốt về <b>Cung {p_end_km} ({qm_end_audit.get('door','')})</b>."
        )
    custom_km_out = _render_outcome_box(
        qm_ans_title,
        qm_ans_detail,
        qm_col,
        header_badge="══► KẾT QUẢ KỲ MÔN GIẢI ĐÁP CÂU HỎI CHÍNH",
    )

    # 3) Ô Kết Quả Sơ Đồ 3 — Mai Hoa giải đáp câu hỏi như thế nào?
    mh_col = "#22c55e" if mh_sc >= 56 else ("#fbbf24" if mh_sc >= 45 else "#ef4444")
    mh_stance = "DỤNG TRỢ THỂ (CÁT)" if mh_sc >= 56 else ("THẾ CÂN BẰNG / CẦN NỖ LỰC" if mh_sc >= 45 else "DỤNG HAO/KHẮC THỂ (KHÓ)")
    mh_ans_title = f"Luận giải Mai Hoa ({mh_sc}/100 — {mh_stance}): {mh_res['ten_chu']} ➔ {mh_res['ten_bien']}"
    if ai_ov.get("meihua_box"):
        mh_ans_detail = f"<b>Tác động Thể–Dụng & Quái Tượng giải đáp câu hỏi:</b> {ai_ov['meihua_box']}"
    else:
        mh_tuong_the = TRIGRAM_META_8.get(mh_res["the_quai"], TRIGRAM_META_8["Càn"])[4]
        mh_tuong_bien = TRIGRAM_META_8.get(mh_res["bien_dung_quai"], TRIGRAM_META_8["Càn"])[4]
        mh_ans_detail = (
            f"<b>Cơ chế Thể–Dụng 4 chặng trả lời câu hỏi:</b> Khởi đầu <b>{mh_res['r1_lbl']}</b> ➔ trung gian Hỗ Quái <b>{mh_res['ten_ho']}</b> "
            f"➔ kết cục <b>{mh_res['r4_lbl']}</b> ({mh_res['r4_desc']}) "
            f"Tượng quẻ ứng thực tế: Thể {mh_res['the_quai']} ({mh_tuong_the}) gặp Biến {mh_res['bien_dung_quai']} ({mh_tuong_bien}); Quái số Tiên/Hậu Thiên = {mh_res['sum_tien_thien']}/{mh_res['sum_hau_thien']}."
        )
    custom_mh_out = _render_outcome_box(
        mh_ans_title,
        mh_ans_detail,
        mh_col,
        header_badge="══► KẾT QUẢ MAI HOA GIẢI ĐÁP CÂU HỎI CHÍNH",
    )

    ly_flow_html = ly_res["render_flowchart_fn"](custom_lh_out)
    qm_flow_html = qm_res["render_flowchart_fn"](custom_km_out)
    mh_flow_html = mh_res["render_flowchart_fn"](custom_mh_out)

    # 4) SƠ ĐỒ 4 — HỢP LỰC TAM THỨC (LỤC HÀO 50% + KỲ MÔN 30% + MAI HOA 20%) ══► GIẢI ĐÁP CHỐT HẠ CÂU HỎI CHÍNH
    syn_n1 = _render_node_box(
        "Trụ Cột 1 · Lục Hào (50%)",
        f"{lh_sc}/100 điểm · {ly_dt_audit['luc_than']} ({ly_dt_audit['chi']}-{ly_dt_audit['ngu_hanh']})",
        f"Thế Hào {ly_res['the_pos']} ({the_audit['chi']}) · Khí {ly_dt_audit['vuong_suy']} · {ly_dt_audit['luc_thu']}",
        [lh_stance],
        lh_col,
    )
    syn_n2 = _render_node_box(
        "Trụ Cột 2 · Kỳ Môn (30%)",
        f"{qm_sc}/100 điểm · Cung {tc} ({qm_tc_audit.get('quai','')})",
        f"{qm_tc_audit.get('door','')} · {qm_tc_audit.get('star','')} · {qm_tc_audit.get('deity','')}",
        [qm_res["ck_rel"]],
        qm_col,
    )
    syn_n3 = _render_node_box(
        "Trụ Cột 3 · Mai Hoa (20%)",
        f"{mh_sc}/100 điểm · Thể {mh_res['the_quai']} ↔ Biến {mh_res['bien_dung_quai']}",
        f"{mh_res['ten_chu']} ➔ {mh_res['ten_bien']}",
        [mh_res["r4_lbl"]],
        mh_col,
    )
    when_final_disp = str(ai_ov.get("when") or deep_syn["duoc_ung_ky"]).strip()
    comp_col = "#22c55e" if comp_sc >= 56 else ("#fbbf24" if comp_sc >= 45 else "#ef4444")
    syn_final_out = _render_outcome_box(
        f"{clean_final_hl}",
        (
            (f"<b>Câu hỏi gốc:</b> «{q_clean_disp}»<br>" if q_clean_disp else "")
            + f"<b>Hợp lực 3 loại quẻ ({comp_sc}/100):</b> Lục Hào định gốc sinh khắc ({lh_sc}đ) + Kỳ Môn định không gian/nhân sự ({qm_sc}đ) + Mai Hoa định tượng biến hóa ({mh_sc}đ).<br>"
            + f"<b>Bệnh – Dược Ứng Kỳ:</b> {when_final_disp}"
        ),
        comp_col,
        header_badge="🎯 TỔNG HỢP 3 QUẺ GIẢI ĐÁP TRỰC DIỆN CÂU HỎI CHÍNH",
    )
    unified_4th_flowchart_html = (
        f'<div style="padding:11px 13px;background:linear-gradient(135deg,rgba(69,26,3,0.72),rgba(15,23,42,0.95));border-radius:11px;border:2px solid #f59e0b;margin-bottom:8px;box-shadow:0 3px 16px rgba(245,158,11,0.22);">'
        f'<div style="font-size:0.88em;font-weight:900;color:#fde68a;margin-bottom:7px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px;">'
        f'<span>🏆 SƠ ĐỒ 4 · HỘI TỤ TÁC ĐỘNG CẢ 3 LOẠI QUẺ (LỤC HÀO + KỲ MÔN + MAI HOA) ══► GIẢI ĐÁP CHỐT HẠ CÂU HỎI CHÍNH</span>'
        f'<span style="color:#fef08a;font-size:0.86em;">Hợp nhất Khí Lực Tam Thức: {comp_sc}/100</span>'
        f'</div>'
        f'<div style="display:flex;align-items:stretch;flex-wrap:wrap;gap:4px;">'
        f'{syn_n1}{_render_svg_arrow("Cộng hưởng", "#38bdf8")}{syn_n2}{_render_svg_arrow("Đối chứng", "#f472b6")}{syn_n3}{_render_svg_arrow("Chốt Đáp Án", "#fbbf24")}{syn_final_out}'
        f'</div></div>'
    )

    # Giao thoa Tín Hiệu Vi Mô Tam Thức (Cross-System Micro Resonance)
    resonances: List[str] = []
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

    _holo_res: Dict[str, Any] = {}
    try:
        from holographic_event_decoder import build_holographic_prophecy_reading
        _holo_res = build_holographic_prophecy_reading(
            ly_res=ly_res,
            qm_res=qm_res,
            mh_res=mh_res,
            deep_syn=deep_syn,
            chart_data=chart_data,
            dung_than=dung_than,
            question=question,
        ) or {}
    except Exception:
        _holo_res = {}

    res_items_html = "".join(f'<div style="margin:3px 0;font-size:0.87em;color:#f1f5f9;line-height:1.48;">• {r}</div>' for r in resonances)
    _bd_box_html = (
        f'<div style="padding:9px 12px;background:rgba(6,78,59,0.52);border-radius:9px;border-left:4px solid #34d399;margin-bottom:8px;">'
        f'<div style="font-size:0.86em;font-weight:900;color:#6ee7b7;margin-bottom:3px;">🩺 CHẨN ĐOÁN BỆNH – DƯỢC QUẺ & TRỌNG SỐ BIỆN CHỨNG TAM THỨC (V143.0 — Lục Hào {deep_syn["lh_score"]} · Kỳ Môn {deep_syn["qm_score"]} · Mai Hoa {deep_syn["mh_score"]} ➔ Hợp Nhất {deep_syn["composite_score"]}/100)</div>'
        f'<div style="font-size:0.86em;color:#ecfdf5;line-height:1.48;">'
        f'• <b>Điểm nghẽn / Bệnh của quẻ:</b> {deep_syn["benh_quai"]}<br>'
        f'• <b>Chìa khóa mở khóa / Lịch ứng kỳ chính xác:</b> <span style="color:#fde68a;font-weight:700;">{deep_syn.get("short_inline_date") or deep_syn["duoc_ung_ky"]}</span>'
        f'</div></div>'
    )

    visual_flowchart_html = (
        f'<div style="margin-top:12px;padding:13px 15px;background:linear-gradient(135deg,rgba(9,13,26,0.96),rgba(23,37,84,0.92));border-radius:13px;border:1.5px solid #38bdf8;box-shadow:0 4px 18px rgba(14,165,233,0.2);">'
        f'<div style="font-size:0.96em;font-weight:900;color:#fde047;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>🗺️ SƠ ĐỒ MŨI TÊN TÁC ĐỘNG NHÂN QUẢ CHI TIẾT & GIẢI ĐÁP TRỰC TIẾP CÂU HỎI CHÍNH (V143.0)</span>'
        f'<span style="font-size:0.78em;color:#bae6fd;background:rgba(56,189,248,0.16);padding:2px 9px;border-radius:999px;border:1px solid rgba(56,189,248,0.4);">Đối chuẩn Tăng San Bốc Dịch · Ngự Định Kỳ Môn · Mai Hoa · Đại Lục Nhâm</span>'
        f'</div>'
        f'{ly_flow_html}'
        f'{qm_flow_html}'
        f'{mh_flow_html}'
        f'{unified_4th_flowchart_html}'
        f'{_bd_box_html}'
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
        f"{deep_syn['prompt_synthesis_block']}\n"
        + (f"{_holo_res.get('holographic_prompt_text', '')}\n" if _holo_res else "")
        + "=== MẠNG LƯỚI MŨI TÊN NHÂN QUẢ VI MÔ V135.0 (CHUẨN NGUYÊN HANH LỢI TRINH & VẤN CHÂN — BẮT BUỘC DÙNG ĐỂ LUẬN SÂU KHÔNG BỎ SÓT CHI TIẾT) ===\n"
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
        "deep_synthesis": deep_syn,
        "holographic_reading": _holo_res,
        "all_directed_edges": all_edges,
        "resonances": resonances,
        "visual_flowchart_html": visual_flowchart_html,
        "prompt_micro_chain_text": prompt_micro_chain_text,
    }

# -*- coding: utf-8 -*-
"""
V129.0 — ĐỘNG CƠ ĐẠI TIÊN TRI CHUYÊN SÂU HỢP NHẤT TỪ KHO MÃ NGUỒN MỞ GITHUB
=============================================================================
Hợp nhất thuật toán định lượng & cổ pháp thực chiến từ 7 dự án mã nguồn mở lớn trên GitHub:
1. john-walks-slow/open-iching   : Chu Dịch 64 Quái Từ, Thoán Truyện, Đại Tượng & 384 Hào Từ / Tiểu Tượng
2. muyen/decoding-iching         : Điểm số Cát/Hung định lượng 384 Hào (ji_score/xiong_score) & Biến Quái 384
3. freeyeahman-ai/gaodao-iching  : Cao Đảo Dịch Đoán (Luận quyết thực chiến 64 Quẻ & 6 Tầng Động Hào)
4. yaomancy/liuyao-engine        : Lục Hào Tăng San Bốc Dịch (Tứ Quyền Hợp Thành, Dụng Thần Lưỡng Hiện, Chân Tam Hợp)
5. thangnc/i-ching-plugins       : Quy chuẩn Nạp Giáp Thiên Can + Địa Chi + 60 Nạp Âm & Vượng Tướng Hưu Tù Tử Việt Nam
6. handsomejustin/meihua-yi      : Mai Hoa Dịch Số (Thể Vượng Suy, Tam Quái Sơ-Trung-Chung & 18 Loại Chiêm Đoán)
7. kentang2017/kinqimen          : Kỳ Môn Độn Giáp (Độn Giáp Ẩn Lục Nghi, Cửu Độn, Kích Hình, Nhập Mộ, Môn Bức, Cửu Tinh Vượng Phế)
"""

from typing import Dict, Any, List, Tuple, Optional
from github_zhouyi_384_data import (
    ZHOUYI_64_FULL,
    ZHOUYI_384_LINES,
    DUNG_CUU_LUC,
    normalize_hex_name,
    get_zhouyi_hexagram,
    get_zhouyi_line,
)

# ==============================================================================
# HẰNG SỐ NGŨ HÀNH, CAN CHI & 60 HOA GIÁP NẠP ÂM CHUẨN
# ==============================================================================
CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_12 = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

SINH_EL = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
KHAC_EL = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
DUOC_SINH_BY = {v: k for k, v in SINH_EL.items()}
BI_KHAC_BY = {v: k for k, v in KHAC_EL.items()}

CHI_EL = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tị": "Hỏa", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
}
CAN_EL = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa",
    "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim",
    "Nhâm": "Thủy", "Quý": "Thủy",
}
XUNG_CHI = {
    "Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu",
    "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão",
    "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị", "Tỵ": "Hợi",
}
HOP_CHI = {
    "Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần",
    "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn",
    "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ", "Tỵ": "Thân",
}
TAM_HOP_SETS = [
    ({"Thân", "Tý", "Thìn"}, "Thủy", "Thân–Tý–Thìn Thủy Cục"),
    ({"Dần", "Ngọ", "Tuất"}, "Hỏa", "Dần–Ngọ–Tuất Hỏa Cục"),
    ({"Hợi", "Mão", "Mùi"}, "Mộc", "Hợi–Mão–Mùi Mộc Cục"),
    ({"Tị", "Dậu", "Sửu"}, "Kim", "Tị–Dậu–Sửu Kim Cục"),
]
MO_BY_EL = {"Kim": "Sửu", "Mộc": "Mùi", "Thủy": "Thìn", "Thổ": "Thìn", "Hỏa": "Tuất"}
TUYET_BY_EL = {"Kim": "Dần", "Mộc": "Thân", "Thủy": "Tị", "Thổ": "Tị", "Hỏa": "Hợi"}

NAP_AM_30_PAIRS = {
    ("Giáp Tý", "Ất Sửu"): "Hải Trung Kim (Vàng trong biển)",
    ("Bính Dần", "Đinh Mão"): "Lô Trung Hỏa (Lửa trong lò)",
    ("Mậu Thìn", "Kỷ Tị"): "Đại Lâm Mộc (Gỗ rừng lớn)",
    ("Canh Ngọ", "Tân Mùi"): "Lộ Bàng Thổ (Đất ven đường)",
    ("Nhâm Thân", "Quý Dậu"): "Kiếm Phong Kim (Vàng mũi kiếm)",
    ("Giáp Tuất", "Ất Hợi"): "Sơn Đầu Hỏa (Lửa đầu núi)",
    ("Bính Tý", "Đinh Sửu"): "Giản Hạ Thủy (Nước khe suối)",
    ("Mậu Dần", "Kỷ Mão"): "Thành Đầu Thổ (Đất tường thành)",
    ("Canh Thìn", "Tân Tị"): "Bạch Lạp Kim (Vàng chân nến)",
    ("Nhâm Ngọ", "Quý Mùi"): "Dương Liễu Mộc (Gỗ dương liễu)",
    ("Giáp Thân", "Ất Dậu"): "Tuyền Trung Thủy (Nước suối nguồn)",
    ("Bính Tuất", "Đinh Hợi"): "Ốc Thượng Thổ (Đất nóc nhà)",
    ("Mậu Tý", "Kỷ Sửu"): "Tích Lịch Hỏa (Lửa sấm sét)",
    ("Canh Dần", "Tân Mão"): "Tùng Bách Mộc (Gỗ tùng bách)",
    ("Nhâm Thìn", "Quý Tị"): "Trường Lưu Thủy (Nước chảy dài)",
    ("Giáp Ngọ", "Ất Mùi"): "Sa Trung Kim (Vàng trong cát)",
    ("Bính Thân", "Đinh Dậu"): "Sơn Hạ Hỏa (Lửa chân núi)",
    ("Mậu Tuất", "Kỷ Hợi"): "Bình Địa Mộc (Gỗ đồng bằng)",
    ("Canh Tý", "Tân Sửu"): "Bích Thượng Thổ (Đất trên vách)",
    ("Nhâm Dần", "Quý Mão"): "Kim Bạch Kim (Vàng nguyên chất)",
    ("Giáp Thìn", "Ất Tị"): "Phú Đăng Hỏa (Lửa đèn lớn)",
    ("Bính Ngọ", "Đinh Mùi"): "Thiên Hà Thủy (Nước sông Ngân)",
    ("Mậu Thân", "Kỷ Dậu"): "Đại Trạch Thổ (Đất đầm lớn)",
    ("Canh Tuất", "Tân Hợi"): "Thoa Xuyến Kim (Vàng trang sức)",
    ("Nhâm Tý", "Quý Sửu"): "Tang Đố Mộc (Gỗ cây dâu)",
    ("Giáp Dần", "Ất Mão"): "Đại Khê Thủy (Nước khe lớn)",
    ("Bính Thìn", "Đinh Tị"): "Sa Trung Thổ (Đất pha cát)",
    ("Mậu Ngọ", "Kỷ Mùi"): "Thiên Thượng Hỏa (Lửa trên trời)",
    ("Canh Thân", "Tân Dậu"): "Thạch Lựu Mộc (Gỗ thạch lựu)",
    ("Nhâm Tuất", "Quý Hợi"): "Đại Hải Thủy (Nước biển lớn)",
}
NAP_AM_60 = {}
for (_c1, _c2), _na_val in NAP_AM_30_PAIRS.items():
    NAP_AM_60[_c1] = _na_val
    NAP_AM_60[_c2] = _na_val
    NAP_AM_60[_c1.replace("Tị", "Tỵ")] = _na_val
    NAP_AM_60[_c2.replace("Tị", "Tỵ")] = _na_val


def get_seasonal_state(hanh_target: str, chi_thang: str) -> str:
    """
    Chuẩn Ngũ Hành Tứ Thời (Ngũ Hành Đại Nghĩa & Tăng San Bốc Dịch):
    Đương lệnh giả Vượng, Ngã sinh giả Tướng, Sinh ngã giả Hưu, Khắc ngã giả Tù, Ngã khắc giả Tử!
    """
    m_chi = "Tị" if chi_thang == "Tỵ" else str(chi_thang or "Tuất").strip()
    m_el = CHI_EL.get(m_chi, "Thổ")
    if not hanh_target or hanh_target not in SINH_EL:
        return "Bình"
    if hanh_target == m_el:
        return "Vượng"
    if SINH_EL[m_el] == hanh_target:
        return "Tướng"
    if SINH_EL[hanh_target] == m_el:
        return "Hưu"
    if KHAC_EL[hanh_target] == m_el:
        return "Tù"
    if KHAC_EL[m_el] == hanh_target:
        return "Tử"
    return "Bình"


# ==============================================================================
# 1. ĐỘNG CƠ CHU DỊCH 64 QUẺ & 384 HÀO TỪ + CAO ĐẢO DỊCH ĐOÁN (open-iching + decoding-iching + gaodao)
# ==============================================================================
def analyze_zhouyi_384_prophecy(
    ban_name: str,
    bien_name: str = "",
    dong_hao_list: Optional[List[int]] = None,
    topic: str = "",
) -> Dict[str, Any]:
    """
    Giải mã chính xác Quái Từ, Thoán Truyện, Đại Tượng, Hào Từ (1..384), Tiểu Tượng & Cao Đảo Dịch Đoán.
    Áp dụng chuẩn 7 quy tắc Chu Hi (Dịch Học Khải Mông) cho 0..6 hào động.
    """
    canon_ban = normalize_hex_name(ban_name)
    canon_bien = normalize_hex_name(bien_name) if bien_name else canon_ban
    hex_ban = get_zhouyi_hexagram(canon_ban)
    hex_bien = get_zhouyi_hexagram(canon_bien)

    dong_clean = sorted({int(x) for x in (dong_hao_list or []) if str(x).isdigit() and 1 <= int(x) <= 6})
    n_dong = len(dong_clean)

    # Chu Hi 7-Case Moving Line Rule (Dịch Học Khải Mông)
    primary_lines: List[Dict[str, Any]] = []
    khai_mong_rule = ""
    score_delta = 0

    if n_dong == 0:
        khai_mong_rule = "Quẻ Tĩnh (0 hào động — Chu Hi Khải Mông): Lấy Quái Từ & Đại Tượng của Bản Quái làm chủ."
        ch = hex_ban.get("cat_hung", "BÌNH")
        score_delta = 6 if "ĐẠI CÁT" in ch else (3 if "CÁT" in ch else (-5 if "HUNG" in ch else 0))
    elif n_dong == 1:
        p = dong_clean[0]
        ln = get_zhouyi_line(canon_ban, p)
        if ln:
            primary_lines.append(ln)
            score_delta = max(-10, min(10, int(round(ln.get("net_score", 0.0) * 5))))
        khai_mong_rule = f"Độc Phát 1 Hào Động (Hào {p} — Chu Hi Khải Mông): Lấy Hào Từ & Tiểu Tượng Hào {p} của Bản Quái ({canon_ban}) kết hợp xu thế Biến Quái ({canon_bien}) làm lời tiên tri trọng tâm."
    elif n_dong == 2:
        p_low, p_high = dong_clean[0], dong_clean[1]
        ln_high = get_zhouyi_line(canon_ban, p_high)
        ln_low = get_zhouyi_line(canon_ban, p_low)
        if ln_high:
            primary_lines.append(ln_high)
        if ln_low:
            primary_lines.append(ln_low)
        net_comb = (ln_high.get("net_score", 0.0) * 0.65 + ln_low.get("net_score", 0.0) * 0.35) if ln_high and ln_low else 0.0
        score_delta = max(-10, min(10, int(round(net_comb * 5))))
        khai_mong_rule = f"Nhị Hào Động (Hào {p_low} & Hào {p_high} — Chu Hi Khải Mông): Xét cả 2 Hào Từ động của Bản Quái ({canon_ban}), lấy Hào trên (Hào {p_high}) làm chủ."
    elif n_dong == 3:
        p_mid = dong_clean[1]
        ln_mid = get_zhouyi_line(canon_ban, p_mid)
        if ln_mid:
            primary_lines.append(ln_mid)
        ch_b = hex_bien.get("cat_hung", "BÌNH")
        score_delta = 5 if "CÁT" in ch_b else (-5 if "HUNG" in ch_b else 0)
        khai_mong_rule = f"Tam Hào Động ({', '.join(map(str, dong_clean))} — Chu Hi Khải Mông): Lấy Quái Từ Bản Quái ({canon_ban}) làm Trinh (hiện tại) và Quái Từ Biến Quái ({canon_bien}) làm Hối (kết cục)."
    elif n_dong == 4:
        static_pos = [i for i in range(1, 7) if i not in dong_clean]
        ln_low_st = get_zhouyi_line(canon_bien, static_pos[0])
        ln_high_st = get_zhouyi_line(canon_bien, static_pos[1])
        if ln_low_st:
            primary_lines.append(ln_low_st)
        if ln_high_st:
            primary_lines.append(ln_high_st)
        score_delta = max(-10, min(10, int(round((ln_low_st.get("net_score", 0.0) if ln_low_st else 0.0) * 5))))
        khai_mong_rule = f"Tứ Hào Động ({', '.join(map(str, dong_clean))} — Chu Hi Khải Mông): Xét 2 hào tĩnh (Hào {static_pos[0]} & {static_pos[1]}) của Biến Quái ({canon_bien}), lấy hào dưới (Hào {static_pos[0]}) làm chủ."
    elif n_dong == 5:
        static_p = [i for i in range(1, 7) if i not in dong_clean][0]
        ln_st = get_zhouyi_line(canon_bien, static_p)
        if ln_st:
            primary_lines.append(ln_st)
        score_delta = max(-10, min(10, int(round((ln_st.get("net_score", 0.0) if ln_st else 0.0) * 5))))
        khai_mong_rule = f"Ngũ Hào Động (Độc Tĩnh Hào {static_p} — Chu Hi Khải Mông): Lấy Hào Từ hào tĩnh duy nhất (Hào {static_p}) của Biến Quái ({canon_bien}) làm chủ."
    else:
        dcl = DUNG_CUU_LUC.get(canon_ban)
        if dcl:
            khai_mong_rule = f"Lục Hào Giai Động ({dcl['title']}): {dcl['vn']}"
            score_delta = 9
        else:
            khai_mong_rule = f"Lục Hào Giai Động (6 hào cùng biến — Chu Hi Khải Mông): Lấy Quái Từ & Thoán Truyện của Biến Quái ({canon_bien}) làm chủ."
            ch_b = hex_bien.get("cat_hung", "BÌNH")
            score_delta = 6 if "CÁT" in ch_b else (-6 if "HUNG" in ch_b else 0)

    main_line = primary_lines[0] if primary_lines else {}
    line_summary_html = ""
    if main_line:
        v_col = "#4ade80" if "CÁT" in main_line.get("verdict", "") else ("#f87171" if "HUNG" in main_line.get("verdict", "") else "#fde047")
        line_summary_html = (
            f"<b>{main_line['hao_title_hv']} ({main_line['hao_title_zh']} — Quẻ {main_line['vn_hex']}):</b> "
            f"<i>“{main_line['hao_tu_zh']}”</i> · Tiểu Tượng: <i>“{main_line['tieu_tuong_zh']}”</i> ➔ "
            f"<span style='color:{v_col};font-weight:800;'>{main_line['luan_giai_vn']}</span> "
            f"<span style='color:#cbd5e1;'>({main_line['gaodao_pos_vn']})</span>"
        )
    else:
        line_summary_html = (
            f"<b>Quái Từ {canon_ban} ({hex_ban.get('symbol', '')}):</b> <i>“{hex_ban.get('quai_tu_zh', '')}”</i> — "
            f"{hex_ban.get('quai_tu_vn', '')}. Đại Tượng: {hex_ban.get('dai_tuong_vn', '')}."
        )

    return {
        "canon_ban": canon_ban,
        "canon_bien": canon_bien,
        "hex_ban": hex_ban,
        "hex_bien": hex_bien,
        "khai_mong_rule": khai_mong_rule,
        "primary_lines": primary_lines,
        "main_line": main_line,
        "score_delta": score_delta,
        "line_summary_html": line_summary_html,
    }


# ==============================================================================
# 2. ĐỘNG CƠ LỤC HÀO TĂNG SAN BỐC DỊCH CHUYÊN SÂU (yaomancy/liuyao-engine + thangnc)
# ==============================================================================
TOPIC_TO_DUNG_THAN_LT = [
    (["tài lộc", "tiền", "lương", "thưởng", "kinh doanh", "đầu tư", "cổ phiếu", "mua bán", "lãi", "nợ", "vàng", "giá"], "Thê Tài"),
    (["thi cử", "học hành", "bằng cấp", "giấy tờ", "hợp đồng", "văn thư", "nhà", "đất", "bất động sản", "xe", "bố", "mẹ", "cha", "ông", "bà", "mưa", "thời tiết"], "Phụ Mẫu"),
    (["công danh", "sự nghiệp", "thăng chức", "xin việc", "quan", "kiện", "tranh chấp", "trộm", "âm binh", "ma", "tà", "chồng", "bạn trai"], "Quan Quỷ"),
    (["con cái", "sinh con", "mang thai", "thuốc", "bác sĩ", "chữa bệnh", "thú cưng", "giải hạn", "phúc khí"], "Tử Tôn"),
    (["anh", "chị", "em", "bạn bè", "đồng nghiệp", "đối tác ngang hàng", "cạnh tranh"], "Huynh Đệ"),
]


def resolve_luc_hao_dung_than(topic: str = "", question: str = "", explicit_dt: str = "") -> str:
    if explicit_dt in ("Thê Tài", "Quan Quỷ", "Phụ Mẫu", "Tử Tôn", "Huynh Đệ", "Bản Thân"):
        return explicit_dt
    combined = f"{topic} {question}".lower()
    if any(k in combined for k in ["mất đồ", "thất lạc", "để quên", "chìa khóa", "ví"]):
        return "Thê Tài"
    if any(k in combined for k in ["vợ", "bạn gái", "người yêu nữ"]):
        return "Thê Tài"
    for kw_list, lt_name in TOPIC_TO_DUNG_THAN_LT:
        if any(k in combined for k in kw_list):
            return lt_name
    return "Bản Thân"


def select_best_dung_than_line(candidates: List[Dict[str, Any]], the_pos: int, ung_pos: int) -> Tuple[Dict[str, Any], str]:
    """
    Quy tắc 'Dụng Thần Lưỡng Hiện' chuẩn Tăng San Bốc Dịch (Chương Dụng Thần Lưỡng Hiện):
    1. Xả nhàn hào nhi dụng động hào (Ưu tiên hào Động hoặc Ám Động)
    2. Xả nguyệt phá nhi dụng bất phá (Bỏ hào Nguyệt Phá / Nhật Phá)
    3. Xả tuần không nhi dụng bất không (Ưu tiên hào Không bị Chân Không)
    4. Xả hưu tù nhi dụng vượng tướng (Ưu tiên Vượng/Tướng)
    5. Như đồng tĩnh đồng động, ưu tiên hào lâm Thế hoặc Ứng!
    """
    if not candidates:
        return {}, ""
    if len(candidates) == 1:
        c = candidates[0]
        return c, f"Độc hiện tại Hào {c.get('hao')}"

    def _rank_key(h: Dict[str, Any]) -> Tuple[int, int, int, int, int]:
        is_dong = 1 if (h.get("is_moving") or h.get("dong") or h.get("is_am_dong")) else 0
        not_pha = 0 if (h.get("is_nguyet_pha") or h.get("is_nhat_pha")) else 1
        not_chan_khong = 0 if h.get("khong_type") == "CHAN_KHONG" else 1
        is_vt = 1 if h.get("strength") in ("Vượng", "Tướng") else 0
        is_the_ung = 2 if h.get("hao") == the_pos else (1 if h.get("hao") == ung_pos else 0)
        return (is_dong, not_pha, not_chan_khong, is_vt, is_the_ung)

    ranked = sorted(candidates, key=_rank_key, reverse=True)
    chosen = ranked[0]
    other_haos = [str(x.get("hao")) for x in candidates if x.get("hao") != chosen.get("hao")]
    reason = (
        f"Dụng Thần Lưỡng Hiện (tại Hào {', '.join(str(x.get('hao')) for x in candidates)}) ➔ "
        f"Theo Tăng San Bốc Dịch chọn <b>Hào {chosen.get('hao')} ({chosen.get('can_chi_full') or chosen.get('can_chi')})</b> "
        f"vì {'đang phát động/ám động' if (chosen.get('is_moving') or chosen.get('is_am_dong')) else ('lâm Thế/Ứng' if chosen.get('hao') in (the_pos, ung_pos) else 'khí lực nguyên vẹn hơn')} "
        f"(bỏ Hào {', '.join(other_haos)})"
    )
    return chosen, reason


def analyze_liuyao_zengshan_deep(
    luc_hao_data: Dict[str, Any],
    dung_than: str = "",
    topic: str = "",
    question: str = "",
    chart_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Phân tích Lục Hào chuyên sâu theo yaomancy/liuyao-engine & Tăng San Bốc Dịch:
    - Tứ Quyền Hợp Thành (Nguyệt Lệnh · Nhật Thần · Động/Ám Động · Biến Hào)
    - Dụng Thần Lưỡng Hiện & Phục Thần Đắc Xuất / Tuyệt Lộ
    - Chân Tam Hợp Cục (CHỈ tính Hào Động + Hào Biến + Nhật/Nguyệt, tuyệt đối không ghép hào tĩnh!)
    - Liên Hoàn Tương Sinh (Nguyên Thần & Kỵ Thần đồng động -> Tham Sinh Quên Khắc)
    - Hợp Bàn Trụ / Tuyệt Xứ Phùng Sinh / Chu Dịch 384 Hào Từ
    """
    if not isinstance(luc_hao_data, dict) or not luc_hao_data.get("ban"):
        return {}

    ban = luc_hao_data.get("ban", {})
    bien = luc_hao_data.get("bien", {})
    ban_name = str(ban.get("name", "Càn Vi Thiên"))
    bien_name = str(bien.get("name", ban_name))
    palace = str(ban.get("palace", "Càn"))
    haos = ban.get("details") or ban.get("haos") or []
    bien_haos = bien.get("details") or bien.get("haos") or []
    dong_list = [int(x) for x in (luc_hao_data.get("dong_hao") or []) if str(x).isdigit()]

    chi_n = str(luc_hao_data.get("chi_ngay") or (chart_data or {}).get("chi_ngay") or "Tý").strip()
    chi_m = str(luc_hao_data.get("chi_thang") or (chart_data or {}).get("chi_thang") or "Dần").strip()
    can_n = str(luc_hao_data.get("can_ngay") or (chart_data or {}).get("can_ngay") or "Giáp").strip()
    if chi_n == "Tỵ":
        chi_n = "Tị"
    if chi_m == "Tỵ":
        chi_m = "Tị"
    nh_n = CHI_EL.get(chi_n, "Thủy")
    nh_m = CHI_EL.get(chi_m, "Mộc")

    # Thế & Ứng
    the_pos = next((int(h["hao"]) for h in haos if h.get("the_ung") == "Thế"), 3)
    ung_pos = next((int(h["hao"]) for h in haos if h.get("the_ung") == "Ứng"), ((the_pos + 2) % 6) + 1)
    the_hao = haos[the_pos - 1] if 1 <= the_pos <= len(haos) else {}
    ung_hao = haos[ung_pos - 1] if 1 <= ung_pos <= len(haos) else {}

    dt_target = resolve_luc_hao_dung_than(topic=topic, question=question, explicit_dt=dung_than)
    if dt_target == "Bản Thân":
        dt_hao = the_hao
        luong_hien_note = f"Lấy Hào Thế (Hào {the_pos}) làm Dụng Thần đại diện trực tiếp cho Bản Thân"
        phuc_obj = None
    else:
        cands = [h for h in haos if dt_target in str(h.get("luc_than", ""))]
        if cands:
            dt_hao, luong_hien_note = select_best_dung_than_line(cands, the_pos, ung_pos)
            phuc_obj = None
        else:
            phuc_obj = next((p for p in (luc_hao_data.get("phuc_than") or []) if dt_target in str(p.get("luc_than", ""))), None)
            if phuc_obj:
                hp = int(phuc_obj.get("hao_pos", the_pos))
                dt_hao = {
                    "hao": hp,
                    "luc_than": dt_target,
                    "chi": phuc_obj.get("chi", "Thìn"),
                    "ngu_hanh": phuc_obj.get("element", "Thổ"),
                    "can_chi": phuc_obj.get("can_chi", ""),
                    "can_chi_full": phuc_obj.get("can_chi_full", phuc_obj.get("can_chi", "")),
                    "strength": phuc_obj.get("strength", "Hưu"),
                    "is_moving": False,
                    "is_phuc": True,
                }
                luong_hien_note = f"Dụng Thần {dt_target} khuyết trên Bản Quái ➔ Tầm Phục Thần dưới Hào {hp}: {phuc_obj.get('phuc_desc', '')}"
            else:
                dt_hao = the_hao
                luong_hien_note = f"Quy chiếu về Hào Thế (Hào {the_pos})"

    dt_pos = int(dt_hao.get("hao", the_pos))
    dt_chi = str(dt_hao.get("chi", "Thìn")).split("-")[0].strip()
    dt_nh = str(dt_hao.get("ngu_hanh") or CHI_EL.get(dt_chi, "Thổ"))
    ng_nh = DUOC_SINH_BY.get(dt_nh, "Thổ")
    ky_nh = BI_KHAC_BY.get(dt_nh, "Mộc")

    # ── KIỂM TRA CHÂN TAM HỢP CỤC & HƯ NHẤT ĐÃI DỤNG (CHUẨN TĂNG SAN BỐC DỊCH) ──
    # Chỉ lấy Địa Chi của: Hào Động + Hào Ám Động + Hào Biến của Hào Động + Nhật Thần + Nguyệt Lệnh!
    moving_line_chis = set()
    active_cuc_chis = {chi_n, chi_m}
    nguyen_moving = []
    ky_moving = []

    for h in haos:
        h_idx = int(h.get("hao", 1))
        h_chi = str(h.get("chi", "")).split("-")[0].strip()
        h_nh = str(h.get("ngu_hanh") or CHI_EL.get(h_chi, ""))
        is_d = (h_idx in dong_list) or bool(h.get("is_moving") or h.get("dong"))
        is_ad = bool(h.get("is_am_dong"))
        if is_d or is_ad:
            if h_chi:
                moving_line_chis.add(h_chi)
                active_cuc_chis.add(h_chi)
            if is_d and 1 <= h_idx <= len(bien_haos):
                b_chi = str(bien_haos[h_idx - 1].get("chi", "")).split("-")[0].strip()
                if b_chi:
                    active_cuc_chis.add(b_chi)
            if h_nh == ng_nh and not h.get("is_nguyet_pha") and h.get("khong_type") != "CHAN_KHONG":
                nguyen_moving.append(f"Hào {h_idx} {h.get('luc_than')} ({h_chi}-{h_nh})")
            elif h_nh == ky_nh and not h.get("is_nguyet_pha") and h.get("khong_type") != "CHAN_KHONG" and "HOI_DAU_KHAC" not in (h.get("hoa_flags") or []):
                ky_moving.append(f"Hào {h_idx} {h.get('luc_than')} ({h_chi}-{h_nh})")

    chan_tam_hop: List[str] = []
    tam_hop_delta = 0
    if moving_line_chis:  # Phải có ít nhất 1 hào Động/Ám Động mới được luận Tam Hợp Cục!
        for cuc_set, cuc_hanh, cuc_name in TAM_HOP_SETS:
            if cuc_set.issubset(active_cuc_chis) and (cuc_set & moving_line_chis):
                if SINH_EL[cuc_hanh] == dt_nh or cuc_hanh == dt_nh:
                    chan_tam_hop.append(f"🌟 <b>Chân Tam Hợp {cuc_name}</b> (Hào động hội Nhật/Nguyệt sinh phù Dụng Thần {dt_nh} — Đại Cát vững chắc)")
                    tam_hop_delta += 12
                elif KHAC_EL[cuc_hanh] == dt_nh:
                    chan_tam_hop.append(f"⚠️ <b>Tam Hợp {cuc_name} khắc Dụng Thần ({dt_nh})</b> (Áp lực ngoại cảnh kết thành thế mạnh)")
                    tam_hop_delta -= 10
                else:
                    chan_tam_hop.append(f"🔄 <b>Tam Hợp {cuc_name}</b> (Tiết khí/chuyển hóa sang hành {cuc_hanh})")
            elif len(cuc_set & moving_line_chis) >= 2 and len(cuc_set - active_cuc_chis) == 1:
                missing_chi = next(iter(cuc_set - active_cuc_chis))
                chan_tam_hop.append(f"⏳ <b>Tam Hợp Khuyết Nhất Đãi Dụng ({cuc_name}):</b> Đã có 2 chi phát động, chờ ngày/giờ <b>{missing_chi}</b> điền thực sẽ kết thành đại cục {cuc_hanh}!")

    # ── LIÊN HOÀN TƯƠNG SINH (THAM SINH QUÊN KHẮC) vs KỴ THẦN ĐỘC PHÁT ──
    lien_hoan_note = ""
    lien_hoan_delta = 0
    if nguyen_moving and ky_moving:
        lien_hoan_note = (
            f"🌟 <b>Liên Hoàn Tương Sinh (Tham Sinh Quên Khắc — Tăng San Bốc Dịch):</b> "
            f"Kỵ Thần ({', '.join(ky_moving)}) và Nguyên Thần ({', '.join(nguyen_moving)}) đồng động ➔ "
            f"Kỵ Thần quay sang sinh Nguyên Thần ({ky_nh} sinh {ng_nh}), Nguyên Thần dồn toàn lực sinh Dụng Thần ({ng_nh} sinh {dt_nh}), biến nguy thành ĐẠI CÁT!"
        )
        lien_hoan_delta = 14
    elif nguyen_moving:
        lien_hoan_note = f"✅ <b>Nguyên Thần Phát Động ({', '.join(nguyen_moving)}):</b> Nguồn quý nhân & hậu thuẫn tiếp sức trực tiếp cho Dụng Thần ({dt_nh})."
        lien_hoan_delta = 9
    elif ky_moving:
        # Kiểm tra nếu Dụng Thần là Quan Quỷ (hỏi bệnh/âm binh/tai ương) thì Kỵ Thần Tử Tôn động lại là ĐẠI CÁT!
        is_bad_subject = any(k in f"{topic} {question}".lower() for k in ["bệnh", "ốm", "đau", "âm binh", "ma", "tà", "tai nạn", "kiện"]) and dt_target == "Quan Quỷ"
        if is_bad_subject:
            lien_hoan_note = f"🌟 <b>Tử Tôn Phúc Thần Động Chế Quỷ ({', '.join(ky_moving)}):</b> Thuốc hay thầy giỏi / chính khí dẹp tan bệnh tật và tà khí!"
            lien_hoan_delta = 12
        else:
            lien_hoan_note = f"⚠️ <b>Kỵ Thần Độc Phát ({', '.join(ky_moving)}):</b> Lực cản trực tiếp khắc chế Dụng Thần ({dt_nh}), cần dùng hành <b>{ng_nh}</b> để thông quan hóa giải."
            lien_hoan_delta = -11

    # ── TÍNH ĐIỂM TỨ QUYỀN HỢP THÀNH (0..100) ──
    score = 52
    st_m = get_seasonal_state(dt_nh, chi_m)
    if st_m == "Vượng":
        score += 14
    elif st_m == "Tướng":
        score += 10
    elif st_m == "Hưu":
        score -= 2
    elif st_m == "Tù":
        score -= 6
    elif st_m == "Tử":
        score -= 11

    # Nhật Thần tác động
    if dt_chi == chi_n or SINH_EL[nh_n] == dt_nh or nh_n == dt_nh:
        score += 10
    elif KHAC_EL[nh_n] == dt_nh:
        score -= 8

    # Nhật Hợp Bàn Trụ vs Tuyệt Xứ Phùng Sinh
    hop_ban_note = ""
    if HOP_CHI.get(chi_n) == dt_chi:
        if dt_hao.get("is_moving"):
            hop_ban_note = f"Nhật Hợp Bàn Trụ ({chi_n} hợp {dt_chi}): Dụng Thần đang động bị Ngày hợp giữ chân tạm thời, chờ ngày <b>{XUNG_CHI.get(dt_chi, 'Thìn')}</b> xung mở sẽ ứng nghiệm."
        else:
            hop_ban_note = f"Nhật Hợp Khởi Tĩnh Hào ({chi_n} hợp {dt_chi}): Hào tĩnh được Nhật Thần hợp khởi, nâng đỡ vượng khí."
            score += 6

    tuyet_sinh_note = ""
    if TUYET_BY_EL.get(dt_nh) in (chi_n, chi_m) and (st_m in ("Vượng", "Tướng") or SINH_EL[nh_n] == dt_nh or nguyen_moving):
        tuyet_sinh_note = f"🌟 <b>Tuyệt Xứ Phùng Sinh:</b> Tuy gặp đất Tuyệt nhưng đắc sinh phù ➔ Trong cái khó ló cơ hội xoay chuyển ngoạn mục!"
        score += 6

    # Biến Hào của Dụng Thần
    h_flags = dt_hao.get("hoa_flags") or []
    if "HOI_DAU_SINH" in h_flags:
        score += 12
    if "HOA_TIEN" in h_flags:
        score += 10
    if "HOI_DAU_KHAC" in h_flags:
        score -= 14
    if "HOA_THOAI" in h_flags:
        score -= 9
    if "HOA_KHONG" in h_flags:
        score -= 8
    if dt_hao.get("khong_type") == "CHAN_KHONG":
        score -= 14
    elif dt_hao.get("khong_type") == "GIA_KHONG":
        score += 2
    if phuc_obj:
        score += (3 if phuc_obj.get("dac_xuat") else -12)

    # Kết hợp Chu Dịch 384 Hào Từ
    zy_res = analyze_zhouyi_384_prophecy(ban_name, bien_name, dong_list, topic=topic)
    score = max(8, min(96, score + tam_hop_delta + lien_hoan_delta + (zy_res.get("score_delta", 0) // 2)))

    # Ứng kỳ Lục Hào chuẩn Tăng San Bốc Dịch
    if phuc_obj:
        ung_ky_lh = f"Dụng Thần ẩn phục dưới Hào {dt_pos} ➔ Ứng kỳ vào ngày/giờ <b>{dt_chi}</b> (trị nhật) hoặc ngày/giờ <b>{XUNG_CHI.get(str(phuc_obj.get('phi_than_can_chi','Thìn')).split('-')[0].split()[-1], 'Tuất')}</b> (xung Phi lộ Phục)."
    elif dt_hao.get("khong_type") in ("CHAN_KHONG", "GIA_KHONG"):
        ung_ky_lh = f"Dụng Thần lâm Tuần Không ({dt_chi}) ➔ Ứng kỳ Xuất Không/Xung Không vào ngày/giờ <b>{dt_chi}</b> hoặc <b>{XUNG_CHI.get(dt_chi, 'Tuất')}</b>."
    elif hop_ban_note and dt_hao.get("is_moving"):
        ung_ky_lh = f"Dụng Thần động phùng Hợp ➔ Ứng kỳ Xung khai vào ngày/giờ <b>{XUNG_CHI.get(dt_chi, 'Tuất')}</b>."
    elif dt_hao.get("is_moving") or dt_hao.get("is_am_dong"):
        ung_ky_lh = f"Dụng Thần phát động ➔ Ứng kỳ Phùng Hợp / Phùng Trị vào ngày/giờ <b>{HOP_CHI.get(dt_chi, dt_chi)}</b> hoặc <b>{dt_chi}</b>."
    else:
        ung_ky_lh = f"Dụng Thần an tĩnh ➔ Ứng kỳ Xung Khởi / Lâm Trị vào ngày/giờ <b>{XUNG_CHI.get(dt_chi, dt_chi)}</b> hoặc <b>{dt_chi}</b>."

    verdict_tag = "ĐẠI CÁT" if score >= 75 else ("CÁT" if score >= 58 else ("BÌNH HÒA / CHỜ THỜI" if score >= 45 else "HUNG / CẦN HÓA GIẢI"))
    v_col = "#10b981" if score >= 58 else ("#f59e0b" if score >= 45 else "#ef4444")

    panel_html = (
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:1.5px solid {v_col};border-radius:12px;padding:14px 16px;margin:10px 0;color:#f1f5f9;font-size:13.5px;line-height:1.58;">'
        f'<div style="font-weight:900;font-size:15px;color:#38bdf8;margin-bottom:8px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>☯️ LUẬN GIẢI CHUYÊN SÂU LỤC HÀO TĂNG SAN BỐC DỊCH & CHU DỊCH 384 HÀO (V129.0 GitHub Engine)</span>'
        f'<span style="background:{v_col};color:#fff;padding:2px 10px;border-radius:999px;font-size:12px;">{verdict_tag} · {score}%</span>'
        f'</div>'
        f'• <b>Định Dụng Thần Chuẩn Cổ Pháp:</b> Dụng Thần là <b style="color:#fde047;">{dt_target}</b> — {luong_hien_note}.<br>'
        f'• <b>Tứ Quyền Hợp Thành (Nguyệt {chi_m} · Nhật {chi_n}):</b> Dụng Thần ({dt_chi}-{dt_nh}) đang <b>{st_m}</b> dưới Nguyệt Lệnh'
        + (f' · {hop_ban_note}' if hop_ban_note else '')
        + (f' · {tuyet_sinh_note}' if tuyet_sinh_note else '')
        + f'.<br>'
        + (f'• <b>Cơ Chế Động Biến & Thông Quan:</b> {lien_hoan_note}<br>' if lien_hoan_note else '')
        + (f'• <b>Tam Hợp Cục Động Hào:</b> {" | ".join(chan_tam_hop)}<br>' if chan_tam_hop else '')
        + f'• <b>Chu Dịch 384 Hào & Cao Đảo Dịch Đoán:</b> {zy_res["khai_mong_rule"]}<br>'
        f'&nbsp;&nbsp;↳ {zy_res["line_summary_html"]}<br>'
        f'• <b>Khóa Ứng Kỳ Thực Chiến:</b> <span style="color:#fde68a;">{ung_ky_lh}</span>'
        f'</div>'
    )

    return {
        "dt_target": dt_target,
        "dt_hao": dt_hao,
        "dt_pos": dt_pos,
        "luong_hien_note": luong_hien_note,
        "chan_tam_hop": chan_tam_hop,
        "lien_hoan_note": lien_hoan_note,
        "hop_ban_note": hop_ban_note,
        "tuyet_sinh_note": tuyet_sinh_note,
        "zhouyi_384": zy_res,
        "score": score,
        "verdict_tag": verdict_tag,
        "ung_ky_lh": ung_ky_lh,
        "panel_html": panel_html,
    }


# ==============================================================================
# 3. ĐỘNG CƠ MAI HOA DỊCH SỐ 18 LOẠI CHIÊM ĐOÁN (handsomejustin/meihua-yi + Thiệu Khang Tiết)
# ==============================================================================
QUAI_BAGUA_TRAITS = {
    "Càn": {"huong": "Tây Bắc", "mau": "Trắng ánh kim, Vàng kim", "benh": "Đầu, phổi, xương khớp, đại tràng", "vat": "Đồ kim khí tròn, vật quý giá, giấy tờ công quyền, nơi cao ráo"},
    "Đoài": {"huong": "Chính Tây", "mau": "Trắng, Bạc", "benh": "Miệng lưỡi, răng họng, phế quản", "vat": "Đồ kim loại nhỏ, có vết sứt/khuyết, nhạc cụ, gần chỗ nước/ao đầm"},
    "Ly": {"huong": "Chính Nam", "mau": "Đỏ, Hồng, Tím", "benh": "Mắt, tim mạch, huyết áp, nóng sốt", "vat": "Đồ điện tử, sách vở, văn thư, nơi sáng sủa hoặc gần bếp/đèn"},
    "Chấn": {"huong": "Chính Đông", "mau": "Xanh lục, Xanh rêu", "benh": "Gan mật, thần kinh, bàn chân, kinh sợ", "vat": "Đồ gỗ, thiết bị phát âm thanh/rung, nơi có tiếng động hoặc lối đi"},
    "Tốn": {"huong": "Đông Nam", "mau": "Xanh lá, Xanh ngọc", "benh": "Phong cảm, đường hô hấp, đùi, khí huyết", "vat": "Đồ gỗ mảnh/dài, dây cáp, vải sợi, giấy tờ, nơi thoáng gió/cửa sổ"},
    "Khảm": {"huong": "Chính Bắc", "mau": "Đen, Xanh dương sẫm", "benh": "Thận, tiết niệu, tai, máu huyết, cảm lạnh", "vat": "Đồ liên quan chất lỏng, chỗ trũng thấp, phòng tắm/bồn nước/ngăn kín"},
    "Cấn": {"huong": "Đông Bắc", "mau": "Vàng đất, Nâu", "benh": "Dạ dày, tỳ vị, mũi, lưng, bàn tay, u cục", "vat": "Đồ gốm đá, hộp vuông, bậc thềm, góc tường, tủ kệ cố định"},
    "Khôn": {"huong": "Tây Nam", "mau": "Vàng sẫm, Nâu đất", "benh": "Bụng, tiêu hóa, tỳ vị, suy nhược cơ thể", "vat": "Đồ vải vóc, túi xách, gốm sứ, nơi thấp tối/góc kho trong nhà"},
}


def _classify_meihua_18_category(topic: str, question: str) -> Tuple[str, str]:
    s = f"{topic} {question}".lower()
    if any(k in s for k in ["mưa", "nắng", "bão", "thời tiết", "trời"]):
        return "THIEN_THOI", "1. Thiên Thời Chiêm (Dự báo Thời tiết)"
    if any(k in s for k in ["hôn nhân", "cưới", "yêu", "tình cảm", "vợ chồng", "bạn trai", "bạn gái", "chia tay"]):
        return "HON_NHAN", "5. Hôn Nhân & Tình Duyên Chiêm"
    if any(k in s for k in ["mang thai", "sinh con", "trai hay gái", "con cái", "bầu"]):
        return "SAN_DUC", "6. Sản Dục & Tử Tức Chiêm (Sinh nở / Con cái)"
    if any(k in s for k in ["thi ", "thi cử", "đỗ", "công danh", "thăng chức", "xin việc", "sự nghiệp"]):
        return "CAU_DANH", "9. Cầu Danh & Công Danh Sự Nghiệp Chiêm"
    if any(k in s for k in ["tiền", "lương", "tài lộc", "đầu tư", "lãi", "giàu", "thưởng", "nợ", "vàng"]):
        return "CAU_TAI", "10. Cầu Tài & Tài Lộc Thực Chiến Chiêm"
    if any(k in s for k in ["hợp đồng", "giao dịch", "mua bán", "kinh doanh", "khai trương", "cửa hàng", "bán được"]):
        return "GIAO_DICH", "11. Giao Dịch & Thương Mại Hợp Đồng Chiêm"
    if any(k in s for k in ["xuất hành", "đi xa", "du lịch", "xuất khẩu lao động", "chuyến đi"]):
        return "XUAT_HANH", "12. Xuất Hành & Di Chuyển Chiêm"
    if any(k in s for k in ["bao giờ về", "mấy giờ xuống", "mấy giờ tới", "người đi", "hành nhân"]):
        return "HANH_NHAN", "13. Hành Nhân Quy Kỳ Chiêm (Người đi xa / Giờ tới)"
    if any(k in s for k in ["mất đồ", "thất lạc", "để quên", "ở đâu", "tìm đồ", "chìa khóa", "trộm"]):
        return "THAT_VAT", "15. Thất Vật Chiêm (Tìm đồ thất lạc & Phương vị)"
    if any(k in s for k in ["bệnh", "ốm", "đau", "thuốc", "khỏi không", "sức khỏe", "mất năm", "thọ"]):
        return "TAT_BENH", "16. Tật Bệnh & Thọ Nguyên Y Dịch Chiêm"
    if any(k in s for k in ["kiện", "tranh chấp", "tòa", "quan tụng"]):
        return "QUAN_TUNG", "17. Quan Tụng & Tranh Chấp Pháp Lý Chiêm"
    if any(k in s for k in ["mộ", "âm phần", "âm binh", "phúc khí", "thờ cúng", "tâm linh"]):
        return "MO_TANG", "18. Mộ Táng & Âm Trạch Tâm Linh Chiêm"
    if any(k in s for k in ["nhà", "đất", "chung cư", "gia trạch", "chuyển nhà", "xây nhà", "tầng"]):
        return "OC_XA", "3–4. Gia Trạch & Ốc Xá Điền Sản Chiêm"
    return "NHAN_SU", "2 & 8. Nhân Sự & Cầu Mưu Tổng Quyết Chiêm"


def analyze_meihua_18_categories_deep(
    mai_hoa_data: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    topic: str = "",
    question: str = "",
) -> Dict[str, Any]:
    """
    Phân tích Mai Hoa Dịch Số chuẩn Thiệu Khang Tiết (Quyển 1 & Quyển 2) + handsomejustin/meihua-yi:
    - Thể Vượng / Thể Suy dưới Nguyệt Lệnh
    - Tam Quái Diễn Tiến (Sơ Kỳ Bản Quái ➔ Trung Kỳ Hổ Quái ➔ Chung Kỳ Biến Quái)
    - 18 Loại Chiêm Đoán chuyên biệt theo chủ đề
    - Quái Khí Ứng Kỳ Pháp + Chu Dịch 384 Hào Từ của Động Hào
    """
    if not isinstance(mai_hoa_data, dict):
        return {}

    ten_chu = normalize_hex_name(mai_hoa_data.get("ten_que") or mai_hoa_data.get("ten") or "Càn Vi Thiên")
    ten_ho = normalize_hex_name(mai_hoa_data.get("ten_ho") or "Càn Vi Thiên")
    ten_bien = normalize_hex_name(mai_hoa_data.get("ten_qua_bien") or mai_hoa_data.get("ten_bien") or ten_chu)
    dong_hao = int(mai_hoa_data.get("dong_hao") or 1)

    hex_c = get_zhouyi_hexagram(ten_chu)
    hex_h = get_zhouyi_hexagram(ten_ho)
    hex_b = get_zhouyi_hexagram(ten_bien)

    up_c = mai_hoa_data.get("ten_thuong") or hex_c.get("upper", "Càn")
    lo_c = mai_hoa_data.get("ten_ha") or hex_c.get("lower", "Càn")
    if dong_hao in (1, 2, 3):
        the_q, dung_q = up_c, lo_c
        h_the = hex_c.get("upper_el", "Kim")
        h_dung = hex_c.get("lower_el", "Kim")
        bien_dung_q = hex_b.get("lower", lo_c)
        h_bien_dung = hex_b.get("lower_el", h_dung)
    else:
        the_q, dung_q = lo_c, up_c
        h_the = hex_c.get("lower_el", "Kim")
        h_dung = hex_c.get("upper_el", "Kim")
        bien_dung_q = hex_b.get("upper", up_c)
        h_bien_dung = hex_b.get("upper_el", h_dung)

    chi_m = str((chart_data or {}).get("chi_thang") or "Tuất").strip()
    the_state = get_seasonal_state(h_the, chi_m)
    dung_state = get_seasonal_state(h_dung, chi_m)

    # Quan hệ Thể - Dụng ở Sơ Kỳ (Bản Quái) & Chung Kỳ (Biến Quái)
    def _rel_code_and_score(ht: str, hd: str) -> Tuple[str, str, int]:
        if SINH_EL.get(hd) == ht:
            return "DỤNG SINH THỂ", "Đại Cát — Sự việc/ngoại cảnh tự đưa lợi lộc tới tay, không tốn sức mà dễ thành", 18
        if ht == hd:
            return "THỂ DỤNG TỶ HÒA", "Cát Tường — Hai bên đồng tâm hiệp lực, thuận buồm xuôi gió", 12
        if KHAC_EL.get(ht) == hd:
            return "THỂ KHẮC DỤNG", "Khả Thành — Bản thân làm chủ cục diện, chủ động dốc sức sẽ thu được kết quả", 5
        if SINH_EL.get(ht) == hd:
            return "THỂ SINH DỤNG", "Tiết Khí / Hao Tổn — Phải chi xuất tiền bạc, tâm sức ra trước, khó thu lợi ngay", -7
        return "DỤNG KHẮC THỂ", "Hung / Lực Cản — Ngoại cảnh đang gây áp lực đè nén lên chủ thể, chớ mạo hiểm", -16

    rel_chu_tag, rel_chu_desc, sc_chu = _rel_code_and_score(h_the, h_dung)
    rel_bien_tag, rel_bien_desc, sc_bien = _rel_code_and_score(h_the, h_bien_dung)

    # Trung Kỳ (Hổ Quái): Đảng Thể vs Đảng Dụng
    h_ho_up = hex_h.get("upper_el", "Kim")
    h_ho_lo = hex_h.get("lower_el", "Kim")
    dang_the_cnt = sum(1 for hx in (h_ho_up, h_ho_lo) if hx == h_the or SINH_EL.get(hx) == h_the)
    sc_ho = 7 if dang_the_cnt == 2 else (0 if dang_the_cnt == 1 else -7)
    sc_season = 8 if the_state in ("Vượng", "Tướng") else (-8 if the_state in ("Tù", "Tử") else 0)

    mh_score = max(8, min(96, 52 + int(sc_chu * 0.45 + sc_ho * 0.20 + sc_bien * 0.55) + sc_season))

    # 18 Loại Chiêm Đoán Chuyên Biệt
    cat_code, cat_title = _classify_meihua_18_category(topic, question)
    bien_traits = QUAI_BAGUA_TRAITS.get(bien_dung_q, QUAI_BAGUA_TRAITS["Càn"])
    the_traits = QUAI_BAGUA_TRAITS.get(the_q, QUAI_BAGUA_TRAITS["Càn"])

    if cat_code == "CAU_TAI":
        cat_verdict = (
            f"<b>Khẩu quyết Cầu Tài (Mai Hoa Quyển 2):</b> “Dụng sinh Thể tiến tài đại hỷ; Thể khắc Dụng túc khả cầu tài; Dụng khắc Thể vô tài thả phòng tổn thất”. "
            f"Hiện Quẻ Chủ <b>{rel_chu_tag}</b>, Quẻ Biến <b>{rel_bien_tag}</b>, Thể Quái {the_q} ({h_the}) đang <b>{the_state}</b> ➔ "
            + ("Tài lộc vượng phát, nguồn tiền về thuận lợi, phương cầu tài đắc lợi tại hướng <b>" + bien_traits["huong"] + "</b>."
               if mh_score >= 56 else "Tài khí hiện đang hao tiết hoặc bị kìm giữ, tránh đầu tư lướt sóng mạo hiểm, nên giữ chặt vốn gốc.")
        )
    elif cat_code == "THAT_VAT":
        cat_verdict = (
            f"<b>Khẩu quyết Thất Vật (Tìm Đồ — Mai Hoa Quyển 2):</b> “Dụng sinh Thể, Tỷ Hòa, Thể khắc Dụng ắt tìm thấy; Dụng khắc Thể khó tìm”. "
            f"Lấy Biến Quái <b>{bien_dung_q} ({h_bien_dung})</b> định nơi thất lạc: Tìm tại hướng <b>{bien_traits['huong']}</b>, liên quan tới <b>{bien_traits['vat']}</b> (màu sắc quanh đó: {bien_traits['mau']}). "
            + ("Khả năng tìm lại được RẤT CAO!" if mh_score >= 52 else "Đồ vật đã dịch chuyển xa hoặc bị che lấp rất kỹ, cần tìm ngay kẻo muộn.")
        )
    elif cat_code == "TAT_BENH":
        cat_verdict = (
            f"<b>Khẩu quyết Tật Bệnh Y Dịch (Mai Hoa Quyển 2):</b> Thể Quái <b>{the_q} ({h_the})</b> là người bệnh, Dụng/Biến là chứng bệnh & thuốc thang. "
            f"Cần lưu tâm vùng cơ thể ứng quái: <b>{the_traits['benh']}</b> (và {bien_traits['benh']}). "
            + ("Thể đắc sinh/vượng khí: bệnh tình sớm thuyên giảm bình phục, tìm thầy thuốc hướng <b>" + the_traits["huong"] + "</b>."
               if mh_score >= 54 else "Dụng/Biến khắc hao Thể: bệnh dễ kéo dài dai dẳng, cần thăm khám chuyên khoa kỹ lưỡng và bồi bổ nguyên khí hành <b>" + DUOC_SINH_BY.get(h_the, "Thổ") + "</b>.")
        )
    elif cat_code == "HON_NHAN":
        cat_verdict = (
            f"<b>Khẩu quyết Hôn Nhân Tình Duyên (Mai Hoa Quyển 2):</b> Thể Quái <b>{the_q} ({h_the})</b> là mình, Dụng Quái <b>{dung_q} ({h_dung})</b> là đối phương. "
            f"Hiện tại <b>{rel_chu_tag}</b> chuyển sang <b>{rel_bien_tag}</b> ➔ "
            + ("Duyên phận tương hòa gắn kết, đôi bên hướng về nhau, hậu vận ấm êm."
               if mh_score >= 56 else "Đang có sự lệch nhịp hoặc thử thách cảm xúc, cần bao dung lắng nghe để hóa giải xung khắc.")
        )
    elif cat_code == "HANH_NHAN":
        cat_verdict = (
            f"<b>Khẩu quyết Hành Nhân Quy Kỳ (Mai Hoa Quyển 2):</b> “Dụng sinh Thể, Tỷ Hòa người sắp về ngay; Thể sinh Dụng còn nán lại; Dụng khắc Thể có việc cản chân”. "
            f"Biến Quái <b>{bien_dung_q}</b> ({rel_bien_tag}) báo hiệu người đi từ hướng <b>{bien_traits['huong']}</b> "
            + ("đã lên đường hoặc tới rất nhanh đúng hẹn!" if mh_score >= 55 else "có chút việc bận nán lại dọc đường, sẽ tới chậm hơn dự kiến một nhịp.")
        )
    elif cat_code in ("CAU_DANH", "GIAO_DICH"):
        cat_verdict = (
            f"<b>Khẩu quyết {cat_title.split('.', 1)[-1].strip()}:</b> Quẻ Thể <b>{the_q} ({h_the} — {the_state})</b> đối chiếu Biến Quái <b>{bien_dung_q} ({rel_bien_tag})</b> ➔ "
            + ("Danh lộc & văn thư hợp đồng hanh thông, được cấp trên/đối tác tín nhiệm chốt kết quả tốt."
               if mh_score >= 56 else "Còn điều khoản hoặc thủ tục ngầm cần rà soát chặt tại giai đoạn trung gian (Quẻ Hỗ " + ten_ho + "), chớ ký vội khi chưa rõ.")
        )
    else:
        cat_verdict = (
            f"<b>Khẩu quyết {cat_title}:</b> Sơ Kỳ ({ten_chu}: <b>{rel_chu_tag}</b>) ➔ Trung Kỳ ({ten_ho}: Đảng Thể {dang_the_cnt}/2) ➔ Chung Kỳ ({ten_bien}: <b>{rel_bien_tag}</b>). "
            f"Thể Quái {the_q} ({h_the}) đang <b>{the_state}</b>, hướng cát lợi ứng tại <b>{the_traits['huong']}</b>."
        )

    # Quái Khí Ứng Kỳ Pháp (Thiệu Khang Tiết)
    XT_NUM = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
    total_ky = XT_NUM.get(up_c, 1) + XT_NUM.get(lo_c, 1) + dong_hao
    half_ky = max(1, (total_ky + 1) // 2)
    double_ky = total_ky * 2
    sinh_the_el = DUOC_SINH_BY.get(h_the, h_the)
    ung_ky_mh = (
        f"Tổng Tiên Thiên Quái Số = <b>{total_ky}</b> (Việc nhanh/đang động ứng mốc <b>{half_ky}</b> giờ/ngày; "
        f"bình thường ứng <b>{total_ky}</b> ngày/tuần; việc chậm ứng <b>{double_ky}</b> ngày) vào ngày/giờ vượng hành <b>{h_the}</b> hoặc <b>{sinh_the_el}</b>."
    )

    zy_line = get_zhouyi_line(ten_chu, dong_hao)
    zy_line_txt = (
        f"<b>{zy_line['hao_title_hv']} ({zy_line['hao_title_zh']}):</b> <i>“{zy_line['hao_tu_zh']}”</i> — {zy_line['luan_giai_vn']}"
        if zy_line else ""
    )

    v_tag = "ĐẠI CÁT" if mh_score >= 74 else ("CÁT" if mh_score >= 56 else ("BÌNH HÒA" if mh_score >= 45 else "CẦN THẬN TRỌNG"))
    v_col = "#ec4899" if mh_score >= 56 else ("#f59e0b" if mh_score >= 45 else "#ef4444")

    panel_html = (
        f'<div style="background:linear-gradient(135deg,#1e1b4b,#31102f);border:1.5px solid {v_col};border-radius:12px;padding:14px 16px;margin:10px 0;color:#fdf2f8;font-size:13.5px;line-height:1.58;">'
        f'<div style="font-weight:900;font-size:15px;color:#f9a8d4;margin-bottom:8px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>🌸 LUẬN GIẢI CHUYÊN SÂU MAI HOA DỊCH SỐ & 18 LOẠI CHIÊM (V129.0 GitHub Engine)</span>'
        f'<span style="background:{v_col};color:#fff;padding:2px 10px;border-radius:999px;font-size:12px;">{v_tag} · {mh_score}%</span>'
        f'</div>'
        f'• <b>Khí Lực Thể – Dụng Theo Mùa (Tháng {chi_m}):</b> Quẻ Thể <b>{the_q} ({h_the})</b> đang <b>{the_state}</b> ↔ Quẻ Dụng <b>{dung_q} ({h_dung})</b> đang <b>{dung_state}</b>.<br>'
        f'• <b>Diễn Tiến 3 Hồi (Bản ➔ Hỗ ➔ Biến):</b><br>'
        f'&nbsp;&nbsp;① <i>Sơ Kỳ ({ten_chu}):</i> <b>{rel_chu_tag}</b> ({rel_chu_desc}).<br>'
        f'&nbsp;&nbsp;② <i>Trung Kỳ ({ten_ho}):</i> Đảng Thể đạt <b>{dang_the_cnt}/2</b> quái trợ lực ({hex_h.get("upper")}-{h_ho_up} / {hex_h.get("lower")}-{h_ho_lo}).<br>'
        f'&nbsp;&nbsp;③ <i>Chung Kỳ ({ten_bien}):</i> Biến sang <b>{bien_dung_q} ({h_bien_dung})</b> ➔ <b>{rel_bien_tag}</b> ({rel_bien_desc}).<br>'
        f'• <b>Chuyên Mục {cat_title}:</b> {cat_verdict}<br>'
        + (f'• <b>Hào Từ Động Hào (Chu Dịch 384 Hào):</b> {zy_line_txt}<br>' if zy_line_txt else '')
        + f'• <b>Quái Khí Ứng Kỳ Pháp:</b> <span style="color:#fde68a;">{ung_ky_mh}</span>'
        f'</div>'
    )

    return {
        "the_q": the_q,
        "dung_q": dung_q,
        "h_the": h_the,
        "h_dung": h_dung,
        "the_state": the_state,
        "dung_state": dung_state,
        "rel_chu_tag": rel_chu_tag,
        "rel_bien_tag": rel_bien_tag,
        "dang_the_cnt": dang_the_cnt,
        "cat_title": cat_title,
        "cat_verdict": cat_verdict,
        "ung_ky_mh": ung_ky_mh,
        "mh_score": mh_score,
        "verdict_tag": v_tag,
        "panel_html": panel_html,
    }


# ==============================================================================
# 4. ĐỘNG CƠ KỲ MÔN ĐỘN GIÁP CHUYÊN SÂU (kentang2017/kinqimen + Kỳ Môn Thống Tông)
# ==============================================================================
CUNG_META = {
    1: ("Khảm", "Chính Bắc", "Thủy"),
    2: ("Khôn", "Tây Nam", "Thổ"),
    3: ("Chấn", "Chính Đông", "Mộc"),
    4: ("Tốn", "Đông Nam", "Mộc"),
    5: ("Trung Cung", "Trung Tâm", "Thổ"),
    6: ("Càn", "Tây Bắc", "Kim"),
    7: ("Đoài", "Chính Tây", "Kim"),
    8: ("Cấn", "Đông Bắc", "Thổ"),
    9: ("Ly", "Chính Nam", "Hỏa"),
}

# Lục Nghi Kích Hình (六仪击刑) chuẩn kentang2017/kinqimen & Kỳ Môn Độn Giáp Bảo Giám
LUC_NGHI_KICH_HINH = {
    ("Mậu", 3): "Mậu lâm Chấn Cung 3 (Giáp Tý Mậu hình Mão — Vô Lễ Chi Hình: dễ hao tài, vấp váp hoặc nôn nóng mất lễ)",
    ("Kỷ", 2): "Kỷ lâm Khôn Cung 2 (Giáp Tuất Kỷ hình Mùi — Thị Thế Chi Hình: dễ bị chèn ép hoặc cố chấp sinh thiệt)",
    ("Canh", 8): "Canh lâm Cấn Cung 8 (Giáp Thân Canh hình Dần — Vô Ân Chi Hình: cản trở gắt gao, va chạm tranh chấp)",
    ("Tân", 9): "Tân lâm Ly Cung 9 (Giáp Ngọ Tân tự hình Ngọ — Tự Hình: tự mình làm khó mình hoặc sai sót chủ quan)",
    ("Nhâm", 4): "Nhâm lâm Tốn Cung 4 (Giáp Thìn Nhâm tự hình Thìn — Nội tâm rối bời, việc di chuyển/dòng tiền bị xoắn)",
    ("Quý", 4): "Quý lâm Tốn Cung 4 (Giáp Dần Quý hình Tị — Vướng thủ tục pháp lý, giấy tờ hoặc tiểu nhân ngầm)",
}

# Thiên Bàn Can Nhập Mộ (天盘入墓)
THIEN_CAN_NHAP_MO = {
    ("Ất", 2): "Ất Mộc Nhập Mộ tại Khôn 2 (Mùi)",
    ("Ất", 6): "Ất Mộc Tọa Mộ tại Càn 6 (Tuất — Âm Mộc trường sinh Ngọ mộ Tuất)",
    ("Bính", 6): "Bính Hỏa Nhập Mộ tại Càn 6 (Tuất — Ánh sáng bị thu vào kho, lực phát huy bị kìm giữ)",
    ("Mậu", 6): "Mậu Thổ Nhập Mộ tại Càn 6 (Tuất — Vốn liếng/tài sản bị khóa chặt hoặc chôn vốn)",
    ("Đinh", 8): "Đinh Hỏa Nhập Mộ tại Cấn 8 (Sửu — Cơ hội/quý nhân đang tạm ẩn mình)",
    ("Kỷ", 8): "Kỷ Thổ Nhập Mộ tại Cấn 8 (Sửu — Mưu tính riêng đang bị đóng băng tạm thời)",
    ("Canh", 8): "Canh Kim Nhập Mộ tại Cấn 8 (Sửu — Kẻ cản trở/đối thủ cũng bị kìm chân)",
    ("Tân", 4): "Tân Kim Nhập Mộ tại Tốn 4 (Thìn — Dễ mắc lỗi cất giữ hoặc vướng mắc khó gỡ)",
    ("Nhâm", 4): "Nhâm Thủy Nhập Mộ tại Tốn 4 (Thìn — Thiên La nhập Mộ, sự việc chậm thoát)",
    ("Quý", 2): "Quý Thủy Nhập Mộ tại Khôn 2 (Mùi — Địa Võng nhập Mộ, thông tin mập mờ chưa rõ)",
}

# Bát Môn & Cửu Tinh gốc cung (để xét Phục Ngâm / Phản Ngâm)
MON_HOME_CUNG = {"Hưu": 1, "Tử": 2, "Thương": 3, "Đỗ": 4, "Khai": 6, "Kinh": 7, "Sinh": 8, "Cảnh": 9}
SAO_HOME_CUNG = {"Bồng": 1, "Nhuế": 2, "Xung": 3, "Phụ": 4, "Cầm": 2, "Tâm": 6, "Trụ": 7, "Nhậm": 8, "Anh": 9}
OPPOSITE_CUNG = {1: 9, 9: 1, 2: 8, 8: 2, 3: 7, 7: 3, 4: 6, 6: 4}
DOOR_EL = {"Hưu": "Thủy", "Sinh": "Thổ", "Thương": "Mộc", "Đỗ": "Mộc", "Cảnh": "Hỏa", "Tử": "Thổ", "Kinh": "Kim", "Khai": "Kim"}
STAR_EL = {"Bồng": "Thủy", "Nhuế": "Thổ", "Xung": "Mộc", "Phụ": "Mộc", "Cầm": "Thổ", "Tâm": "Kim", "Trụ": "Kim", "Nhậm": "Thổ", "Anh": "Hỏa"}


def resolve_qimen_stem(can: str, chi: str) -> Tuple[str, str]:
    """
    Độn Giáp Lục Giáp Ẩn Lục Nghi (kentang2017/kinqimen):
    Can 'Giáp' ẩn dưới Lục Nghi theo Tuần Thủ:
      Giáp Tý -> Mậu | Giáp Tuất -> Kỷ | Giáp Thân -> Canh | Giáp Ngọ -> Tân | Giáp Thìn -> Nhâm | Giáp Dần -> Quý
    """
    c = str(can or "Giáp").strip()
    ch = "Tị" if str(chi or "Tý").strip() == "Tỵ" else str(chi or "Tý").strip()
    if c != "Giáp":
        return c, c
    if c in CAN_10 and ch in CHI_12:
        tuan_chi_idx = (CHI_12.index(ch) - CAN_10.index(c)) % 12
        lead_map = {0: "Mậu", 10: "Kỷ", 8: "Canh", 6: "Tân", 4: "Nhâm", 2: "Quý"}
        nghi = lead_map.get(tuan_chi_idx, "Mậu")
        return nghi, f"Giáp {ch} (Độn ẩn dưới Lục Nghi {nghi})"
    return "Mậu", "Giáp (Độn ẩn dưới Mậu)"


def get_qimen_star_strength(star_el: str, month_el: str) -> str:
    """
    Cửu Tinh Vượng–Tướng–Hưu–Tù–Phế chuẩn Kỳ Môn Độn Giáp Thống Tông:
    (Khác Lục Hào ở chỗ Sao là Thiên Tinh làm khách: Ngã sinh giả Tướng, Đồng ngã giả Vượng, Khắc ngã giả Hưu, Ngã khắc giả Tù, Sinh ngã giả Phế!)
    """
    if not star_el or not month_el:
        return "Bình"
    if star_el == month_el:
        return "Vượng"
    if SINH_EL.get(star_el) == month_el:
        return "Tướng"
    if KHAC_EL.get(month_el) == star_el:
        return "Hưu"
    if KHAC_EL.get(star_el) == month_el:
        return "Tù"
    if SINH_EL.get(month_el) == star_el:
        return "Phế"
    return "Bình"


def detect_palace_special_formations(
    cung: int,
    can_thien: str,
    can_dia: str,
    cua: str,
    sao: str,
    than: str,
    can_ngay_resolved: str = "",
) -> Tuple[List[str], List[str], int]:
    """Quét Cửu Độn, Thanh Long Phản Thủ, Phi Điểu Điệt Huyệt, Tam Kỳ Đắc Sử, Kích Hình, Nhập Mộ, Môn Bức & Thập Đại Hung Cách."""
    auspicious: List[str] = []
    inauspicious: List[str] = []
    delta = 0

    clean_cua = next((k for k in DOOR_EL if k in str(cua)), "")
    clean_sao = next((k for k in STAR_EL if k in str(sao)), "")
    _, _, cung_el = CUNG_META.get(cung, ("Khôn", "Tây Nam", "Thổ"))

    # 1. Đại Cát Cách & Cửu Độn (kentang2017/kinqimen)
    if (can_thien, can_dia) == ("Mậu", "Bính"):
        auspicious.append("🐉 <b>Thanh Long Phản Thủ (Mậu + Bính):</b> Đại cát bậc nhất, mưu sự cầu tài thăng tiến đều đắc quý nhân!")
        delta += 15
    elif (can_thien, can_dia) == ("Bính", "Mậu"):
        auspicious.append("🦅 <b>Phi Điểu Điệt Huyệt (Bính + Mậu):</b> Chim bay vào tổ ấm — không tốn sức mà việc lớn tự thành (Đại Cát)!")
        delta += 15

    if can_thien == "Bính" and can_dia == "Đinh" and clean_cua == "Sinh":
        auspicious.append("☀️ <b>Thiên Độn Đại Cát Cách (Bính + Đinh + Sinh Môn):</b> Được thiên thời che chở, mưu đại sự cực lợi!")
        delta += 14
    elif can_thien == "Ất" and can_dia == "Kỷ" and clean_cua == "Khai":
        auspicious.append("🌍 <b>Địa Độn Đại Cát Cách (Ất + Kỷ + Khai Môn):</b> Nền tảng vững chắc, mở mang cơ nghiệp đại cát!")
        delta += 13
    elif can_thien == "Đinh" and clean_cua == "Hưu" and "Thái Âm" in str(than):
        auspicious.append("👤 <b>Nhân Độn Đại Cát Cách (Đinh + Hưu Môn + Thái Âm):</b> Đắc nhân hòa và quý nhân ngầm nâng đỡ!")
        delta += 13
    elif can_thien == "Ất" and clean_cua in ("Khai", "Hưu", "Sinh") and cung == 4:
        auspicious.append("🍃 <b>Phong Độn Cát Cách (Ất lâm Tốn 4 hội Tam Cát Môn):</b> Thuận gió căng buồm, xuất hành giao dịch đại lợi!")
        delta += 11
    elif can_thien == "Ất" and can_dia == "Tân" and clean_cua in ("Khai", "Hưu", "Sinh"):
        auspicious.append("☁️ <b>Vân Độn Cát Cách</b>")
        delta += 8
    elif can_thien == "Ất" and clean_cua == "Hưu" and (cung == 1 or can_dia == "Quý"):
        auspicious.append("🐲 <b>Long Độn Cát Cách (Ất + Hưu Môn tại Thủy hương):</b> Cầu tài giao thương thuận dòng vượng khí!")
        delta += 11
    elif can_thien == "Bính" and clean_cua == "Sinh" and "Cửu Thiên" in str(than):
        auspicious.append("⚡ <b>Thần Độn Cát Cách (Bính + Sinh Môn + Cửu Thiên):</b> Khí thế vươn cao, thần trợ công thành!")
        delta += 12
    elif can_thien == "Đinh" and clean_cua == "Đỗ" and "Cửu Địa" in str(than):
        auspicious.append("🛡️ <b>Quỷ Độn Cách (Đinh + Đỗ Môn + Cửu Địa):</b> Mưu lược kín đáo, hóa giải tà khí/đối thủ tuyệt hảo!")
        delta += 9

    if can_thien in ("Ất", "Bính", "Đinh") and clean_cua in ("Khai", "Hưu", "Sinh"):
        auspicious.append(f"✨ <b>Tam Kỳ Hội Tam Cát Môn ({can_thien} + {clean_cua} Môn):</b> Khí cát tường hội tụ thông suốt.")
        delta += 8

    # 2. Đại Hung Cách & Cảnh báo Kích Hình / Nhập Mộ / Môn Bức
    if (can_thien, can_dia) in LUC_NGHI_KICH_HINH or (can_thien, cung) in LUC_NGHI_KICH_HINH:
        kh_desc = LUC_NGHI_KICH_HINH.get((can_thien, cung), "")
        if kh_desc:
            inauspicious.append(f"⚡ <b>Lục Nghi Kích Hình:</b> {kh_desc}")
            delta -= 12

    if (can_thien, cung) in THIEN_CAN_NHAP_MO:
        inauspicious.append(f"🔒 <b>Thiên Bàn Nhập Mộ:</b> {THIEN_CAN_NHAP_MO[(can_thien, cung)]}")
        delta -= 8

    if clean_cua and KHAC_EL.get(DOOR_EL[clean_cua]) == cung_el:
        inauspicious.append(f"⚠️ <b>Môn Bức ({clean_cua} Môn [{DOOR_EL[clean_cua]}] bức Cung {cung} [{cung_el}]):</b> Cát môn giảm nửa lực, hung môn thêm gắt.")
        delta -= 7

    hung_pairs = {
        ("Ất", "Tân"): "Thanh Long Đào Tẩu (Ất + Tân: dễ thất thoát tiền của/nhân sự bỏ đi, nên giữ chớ tiến)",
        ("Tân", "Ất"): "Bạch Hổ Xương Cuồng (Tân + Ất: xung đột bất ngờ, tránh tranh cãi va chạm)",
        ("Đinh", "Quý"): "Chu Tước Đầu Giang (Đinh + Quý: giấy tờ/tin tức dễ chìm hoặc sinh khẩu thiệt)",
        ("Quý", "Đinh"): "Đằng Xà Yêu Kiều (Quý + Đinh: lo âu rối rắm, thị phi dây dưa)",
        ("Canh", "Bính"): "Thái Bạch Nhập Huỳnh (Canh + Bính: đề phòng hao hụt/tiểu nhân xâm lấn, lợi thủ bất lợi công)",
        ("Bính", "Canh"): "Huỳnh Nhập Thái Bạch (Bính + Canh: chướng ngại rút lui dần nhưng chớ nóng vội)",
        ("Canh", "Quý"): "Đại Cách (Canh + Quý: đi xa hay mưu sự dễ bị ngắt quãng giữa chừng)",
        ("Canh", "Kỷ"): "Hình Cách (Canh + Kỷ: dễ vướng rắc rối kỷ luật/hợp đồng)",
    }
    if (can_thien, can_dia) in hung_pairs:
        inauspicious.append(f"🔴 <b>Hung Cách {hung_pairs[(can_thien, can_dia)]}</b>")
        delta -= 10
    if can_ngay_resolved and can_thien == "Canh" and can_dia == can_ngay_resolved:
        inauspicious.append("🔴 <b>Phục Can Cách (Canh đè Can Ngày):</b> Áp lực bên ngoài đang đè trực tiếp lên bản thân, nên nhẫn nhịn chờ qua giờ/ngày xung.")
        delta -= 11
    elif can_ngay_resolved and can_thien == can_ngay_resolved and can_dia == "Canh":
        inauspicious.append("🔴 <b>Phi Can Cách (Can Ngày lâm Canh):</b> Chủ động va chạm sẽ bất lợi, nên đổi hướng mưu sự.")
        delta -= 9

    # Phục Ngâm / Phản Ngâm Môn & Tinh
    if clean_cua and MON_HOME_CUNG.get(clean_cua) == cung:
        inauspicious.append("🔁 <b>Môn Phục Ngâm:</b> Cửa nằm nguyên bản cung — sự việc trì trệ kéo dài, lợi thu hồi nợ cũ, bất lợi tốc chiến.")
    elif clean_cua and OPPOSITE_CUNG.get(MON_HOME_CUNG.get(clean_cua, 0)) == cung:
        inauspicious.append("🔄 <b>Môn Phản Ngâm:</b> Cửa xung đối bản cung — biến chuyển đảo chiều nhanh, dễ lặp đi lặp lại 2 lần.")

    return auspicious, inauspicious, delta


def analyze_kinqimen_deep_patterns(
    chart_data: Dict[str, Any],
    target_cung: Optional[int] = None,
    topic: str = "",
    question: str = "",
) -> Dict[str, Any]:
    """
    Phân tích toàn diện bàn Kỳ Môn Độn Giáp chuẩn kentang2017/kinqimen:
    - Tự động giải Độn Giáp cho Can Ngày & Can Giờ (kể cả ngày Giáp / giờ Giáp!)
    - Quét Cửu Độn, Thanh Long Phản Thủ, Phi Điểu Điệt Huyệt, Kích Hình, Nhập Mộ, Môn Bức trên toàn bàn & Cung Dụng Thần
    - Cửu Tinh Vượng–Tướng–Hưu–Tù–Phế chuẩn tiết lệnh tháng (chi_thang)
    """
    if not isinstance(chart_data, dict):
        return {}

    ctb = chart_data.get("can_thien_ban") or {}
    cdb = chart_data.get("dia_can") or chart_data.get("can_dia_ban") or chart_data.get("dia_ban") or {}
    tb = chart_data.get("thien_ban") or {}
    nb = chart_data.get("nhan_ban") or {}
    thb = chart_data.get("than_ban") or {}

    can_n = str(chart_data.get("can_ngay") or "Giáp").strip()
    chi_n = str(chart_data.get("chi_ngay") or "Tý").strip()
    can_g = str(chart_data.get("can_gio") or "Bính").strip()
    chi_g = str(chart_data.get("chi_gio") or "Thân").strip()
    chi_m = str(chart_data.get("chi_thang") or "Tuất").strip()
    nh_m = CHI_EL.get("Tị" if chi_m == "Tỵ" else chi_m, "Thổ")

    ngay_stem_res, ngay_stem_label = resolve_qimen_stem(can_n, chi_n)
    gio_stem_res, gio_stem_label = resolve_qimen_stem(can_g, chi_g)

    def _find_thien_cung(stem_s: str, default_c: int = 1) -> int:
        for k, v in ctb.items():
            if str(v).strip() == stem_s and str(k).isdigit():
                return int(k)
        for k, v in cdb.items():
            if str(v).strip() == stem_s and str(k).isdigit():
                return int(k)
        return default_c

    cung_ngay = _find_thien_cung(ngay_stem_res, target_cung or 1)
    cung_gio = _find_thien_cung(gio_stem_res, target_cung or cung_ngay)
    dt_cung = int(target_cung) if (target_cung and int(target_cung) in range(1, 10)) else cung_gio
    if dt_cung == 5:
        dt_cung = 2

    def _val(d: dict, c: int, default: str = "") -> str:
        return str(d.get(c) or d.get(str(c)) or default).strip()

    sao_dt = _val(tb, dt_cung, "Thiên Tâm")
    cua_dt = _val(nb, dt_cung, "Khai Môn")
    than_dt = _val(thb, dt_cung, "Trực Phù")
    ct_dt = _val(ctb, dt_cung, ngay_stem_res)
    cd_dt = _val(cdb, dt_cung, gio_stem_res)

    clean_sao_dt = next((k for k in STAR_EL if k in sao_dt), "Tâm")
    star_strength = get_qimen_star_strength(STAR_EL[clean_sao_dt], nh_m)
    quai_dt, huong_dt, el_dt = CUNG_META.get(dt_cung, ("Khôn", "Tây Nam", "Thổ"))
    cung_season = get_seasonal_state(el_dt, chi_m)

    aus_dt, inaus_dt, delta_dt = detect_palace_special_formations(
        dt_cung, ct_dt, cd_dt, cua_dt, sao_dt, than_dt, can_ngay_resolved=ngay_stem_res
    )

    # Quét toàn bàn 8 cung tìm Phương Cát Nhất (Cửu Độn / Tam Kỳ Tam Cát Môn không bị Kích Hình/Môn Bức/Tuần Không)
    kv_cungs = {int(x) for x in (chart_data.get("khong_vong") or []) if str(x).isdigit()}
    best_palaces = []
    for c_i in [1, 8, 3, 4, 9, 2, 7, 6]:
        ct_i = _val(ctb, c_i)
        cd_i = _val(cdb, c_i)
        cua_i = _val(nb, c_i)
        sao_i = _val(tb, c_i)
        than_i = _val(thb, c_i)
        aus_i, inaus_i, d_i = detect_palace_special_formations(c_i, ct_i, cd_i, cua_i, sao_i, than_i, ngay_stem_res)
        if c_i in kv_cungs:
            d_i -= 6
        if d_i >= 6 or (any(g in cua_i for g in ("Khai", "Hưu", "Sinh")) and not inaus_i):
            _, h_dir, _ = CUNG_META[c_i]
            best_palaces.append((d_i, f"Cung {c_i} ({h_dir} — {cua_i}, {sao_i}, {than_i}, Can {ct_i}/{cd_i})"))
    best_palaces.sort(key=lambda x: x[0], reverse=True)

    # Ứng kỳ Kỳ Môn chuẩn Thống Tông
    ma_cung = chart_data.get("dich_ma")
    if dt_cung in kv_cungs:
        ung_ky_km = f"Cung Dụng Thần ({dt_cung} — {huong_dt}) đang lâm Tuần Không ➔ Ứng kỳ Điền Thực / Xung Thực khi đến ngày/giờ lấp đầy Cung {dt_cung}."
    elif str(ma_cung) == str(dt_cung):
        ung_ky_km = f"Cung Dụng Thần ({dt_cung}) hội Dịch Mã Tinh ➔ Ứng nghiệm CỰC NHANH ngay trong giờ/ngày xung hoặc hợp Mã Tinh."
    else:
        ung_ky_km = f"Ứng theo số Lạc Thư Cung Dụng Thần (Cung {dt_cung} ➔ số <b>{dt_cung}</b> giờ/ngày) hoặc ngày/giờ Can <b>{ct_dt}</b>."

    km_score = max(10, min(96, 55 + delta_dt + (6 if star_strength in ("Vượng", "Tướng") else -4)))
    v_tag = "ĐẠI CÁT CÁCH" if km_score >= 74 else ("CÁT CỤC" if km_score >= 56 else ("BÌNH HÒA" if km_score >= 45 else "CÓ KÍCH HÌNH / CẢN TRỞ"))
    v_col = "#fbbf24" if km_score >= 56 else ("#38bdf8" if km_score >= 45 else "#ef4444")

    panel_html = (
        f'<div style="background:linear-gradient(135deg,#1c1917,#292524);border:1.5px solid {v_col};border-radius:12px;padding:14px 16px;margin:10px 0;color:#fef3c7;font-size:13.5px;line-height:1.58;">'
        f'<div style="font-weight:900;font-size:15px;color:#fde047;margin-bottom:8px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>🔮 LUẬN GIẢI CHUYÊN SÂU KỲ MÔN ĐỘN GIÁP (V129.0 GitHub KinQiMen Engine)</span>'
        f'<span style="background:{v_col};color:#111827;font-weight:900;padding:2px 10px;border-radius:999px;font-size:12px;">{v_tag} · {km_score}%</span>'
        f'</div>'
        f'• <b>Định Vị Độn Giáp Chủ – Khách:</b> Bản Thân <b>{ngay_stem_label}</b> đóng tại <b>Cung {cung_ngay} ({CUNG_META.get(cung_ngay, ("","",""))[1]})</b> '
        f'↔ Sự Việc <b>{gio_stem_label}</b> đóng tại <b>Cung {cung_gio} ({CUNG_META.get(cung_gio, ("","",""))[1]})</b>.<br>'
        f'• <b>Cung Trọng Tâm (Cung {dt_cung} — {quai_dt} {huong_dt}, Cung {cung_season}):</b> Sao <b>{sao_dt} ({star_strength})</b> · Cửa <b>{cua_dt}</b> · Thần <b>{than_dt}</b> · Thiên/Địa Can <b>{ct_dt}/{cd_dt}</b>.<br>'
        + (f'• <b>Cát Cách & Cửu Độn:</b> {" | ".join(aus_dt)}<br>' if aus_dt else '')
        + (f'• <b>Cảnh Báo Kích Hình / Nhập Mộ / Hung Cách:</b> {" | ".join(inaus_dt)}<br>' if inaus_dt else '• <b>Kiểm Định Hình–Mộ–Bức:</b> Cung Dụng Thần <b>không phạm Lục Nghi Kích Hình, Nhập Mộ hay Môn Bức</b> — khí cục thanh thuần.<br>')
        + (f'• <b>Phương Cát Lợi Nhất Toàn Bàn:</b> <span style="color:#4ade80;">{" ; ".join(x[1] for x in best_palaces[:2])}</span>.<br>' if best_palaces else '')
        + f'• <b>Ứng Kỳ Kỳ Môn:</b> <span style="color:#fde68a;">{ung_ky_km}</span>'
        f'</div>'
    )

    return {
        "ngay_stem_res": ngay_stem_res,
        "ngay_stem_label": ngay_stem_label,
        "gio_stem_res": gio_stem_res,
        "gio_stem_label": gio_stem_label,
        "cung_ngay": cung_ngay,
        "cung_gio": cung_gio,
        "dt_cung": dt_cung,
        "star_strength": star_strength,
        "cung_season": cung_season,
        "auspicious": aus_dt,
        "inauspicious": inaus_dt,
        "delta": delta_dt,
        "best_palaces": [x[1] for x in best_palaces[:3]],
        "ung_ky_km": ung_ky_km,
        "km_score": km_score,
        "verdict_tag": v_tag,
        "panel_html": panel_html,
    }

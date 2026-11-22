# -*- coding: utf-8 -*-
# qmdg_calc.py - Core calculation engine for Kỳ Môn Độn Giáp (V101.6 Standard)
import math
import datetime

# Data for calculations
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

TIET_KHI_LIST = [
    "Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập",
    "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng",
    "Hạ Chí", "Tiểu Thử", "Đại Thử", "Lập Thu", "Xử Thử", "Bạch Lộ",
    "Thu Phân", "Hàn Lộ", "Sương Giáng", "Lập Đông", "Tiểu Tuyết", "Đại Tuyết"
]

# Map Tiết khí to Cục (Thượng, Trung, Hạ)
TIET_KHI_CUC = {
    "Đông Chí": (1, 7, 4), "Tiểu Hàn": (2, 8, 5), "Đại Hàn": (3, 9, 6),
    "Lập Xuân": (8, 5, 2), "Vũ Thủy": (9, 6, 3), "Kinh Trập": (1, 7, 4),
    "Xuân Phân": (3, 9, 6), "Thanh Minh": (4, 1, 7), "Cốc Vũ": (5, 2, 8),
    "Lập Hạ": (4, 1, 7), "Tiểu Mãn": (5, 2, 8), "Mang Chủng": (6, 3, 9),
    "Hạ Chí": (9, 3, 6), "Tiểu Thử": (8, 2, 5), "Đại Thử": (7, 1, 4),
    "Lập Thu": (2, 5, 8), "Xử Thử": (1, 4, 7), "Bạch Lộ": (9, 3, 6),
    "Thu Phân": (7, 1, 4), "Hàn Lộ": (6, 9, 3), "Sương Giáng": (5, 8, 2),
    "Lập Đông": (6, 9, 3), "Tiểu Tuyết": (5, 8, 2), "Đại Tuyết": (4, 7, 1)
}


def get_vn_now():
    """Trả về thời gian thực tại Việt Nam (UTC+7, naive datetime) chuẩn xác trên cả Local & Cloud."""
    vn_tz = datetime.timezone(datetime.timedelta(hours=7))
    return datetime.datetime.now(vn_tz).replace(tzinfo=None)


def get_can_chi_year(year):
    """Calculate Can Chi for Year."""
    idx = (year - 4) % 60
    return CAN[idx % 10], CHI[idx % 12]


def get_can_chi_day(dt):
    """Calculate Can Chi for Day using reliable base. Jan 1, 2024 is Giáp Tý (index 0)."""
    if isinstance(dt, datetime.datetime):
        d_obj = dt.date()
    else:
        d_obj = dt
    base_dt = datetime.date(2024, 1, 1)
    diff = (d_obj - base_dt).days
    idx = (0 + diff) % 60
    if idx < 0:
        idx += 60
    return CAN[idx % 10], CHI[idx % 12]


def get_can_chi_hour(day_can, hour):
    """Calculate Can Chi for Hour based on Day Can."""
    # Hour index: 0(Tý) to 11(Hợi). Tý is 23h-1h.
    hour_idx = ((hour + 1) // 2) % 12
    # Giáp Kỷ khởi Giáp Tý (0), Ất Canh khởi Bính Tý (2)...
    start_can_map = {
        "Giáp": 0, "Kỷ": 0,
        "Ất": 2, "Canh": 2,
        "Bính": 4, "Tân": 4,
        "Đinh": 6, "Nhâm": 6,
        "Mậu": 8, "Quý": 8
    }
    start_can_idx = start_can_map.get(day_can, 0)
    hour_can_idx = (start_can_idx + hour_idx) % 10
    return CAN[hour_can_idx], CHI[hour_idx]


_SOLAR_TERMS_BY_LON = [
    "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng",
    "Hạ Chí", "Tiểu Thử", "Đại Thử", "Lập Thu", "Xử Thử", "Bạch Lộ",
    "Thu Phân", "Hàn Lộ", "Sương Giáng", "Lập Đông", "Tiểu Tuyết", "Đại Tuyết",
    "Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập"
]


def _solar_longitude_deg_utc(dt_utc: datetime.datetime) -> float:
    """
    V133.0: Tính Kinh độ Hoàng đạo biểu kiến của Mặt Trời (Apparent Solar Longitude λ☉, 0°..360°)
    theo thuật toán thiên văn Jean Meeus (Astronomical Algorithms, Ch. 25 — sai số < 1 phút cung).
    Đảm bảo chuyển giao 24 Tiết Khí chuẩn xác tới từng Giờ:Phút cho MỌI NĂM (1800–2200).
    """
    y = dt_utc.year
    m = dt_utc.month
    d = dt_utc.day + (
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    ) / 24.0
    if m <= 2:
        y -= 1
        m += 12
    a_val = y // 100
    b_val = 2 - a_val + (a_val // 4)
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b_val - 1524.5
    # Hiệu chỉnh ΔT xấp xỉ cho lịch hiện đại (~69 giây quanh thế kỷ 21)
    delta_t_days = (64.0 + 0.3 * (dt_utc.year - 2005)) / 86400.0
    t_cent = (jd + delta_t_days - 2451545.0) / 36525.0

    l0 = (280.46646 + 36000.76983 * t_cent + 0.0003032 * t_cent * t_cent) % 360.0
    m_anom = (357.52911 + 35999.05029 * t_cent - 0.0001537 * t_cent * t_cent) % 360.0
    m_rad = math.radians(m_anom)
    c_eq = (
        (1.914602 - 0.004817 * t_cent - 0.000014 * t_cent * t_cent) * math.sin(m_rad)
        + (0.019993 - 0.000101 * t_cent) * math.sin(2.0 * m_rad)
        + 0.000289 * math.sin(3.0 * m_rad)
    )
    true_lon = l0 + c_eq
    omega = 125.04 - 1934.136 * t_cent
    app_lon = (true_lon - 0.00569 - 0.00478 * math.sin(math.radians(omega))) % 360.0
    return app_lon


def get_tiet_khi(dt):
    """
    V133.0: Tính chính xác 24 Tiết Khí tới từng Giờ:Phút theo Kinh độ Mặt Trời Jean Meeus (UTC+7).
    Phục vụ chuẩn xác Chiết Bổ Pháp (拆補法) của Ngự Định Kỳ Môn Bảo Giám & Nguyệt Kiến Lục Hào.
    """
    if isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime):
        dt = datetime.datetime(dt.year, dt.month, dt.day, 12, 0, 0)
    elif dt.tzinfo is not None:
        try:
            vn_tz = datetime.timezone(datetime.timedelta(hours=7))
            dt = dt.astimezone(vn_tz).replace(tzinfo=None)
        except Exception:
            dt = dt.replace(tzinfo=None)
    dt_utc = dt - datetime.timedelta(hours=7)
    lam = _solar_longitude_deg_utc(dt_utc)
    term_idx = int((lam % 360.0) // 15.0) % 24
    return _SOLAR_TERMS_BY_LON[term_idx]


def get_can_chi_month(year_can, tiet_khi):
    """Calculate Can Chi for Month based on Year Can and Solar Term."""
    month_chi_map = {
        "Lập Xuân": "Dần", "Vũ Thủy": "Dần", "Kinh Trập": "Mão", "Xuân Phân": "Mão",
        "Thanh Minh": "Thìn", "Cốc Vũ": "Thìn", "Lập Hạ": "Tị", "Tiểu Mãn": "Tị",
        "Mang Chủng": "Ngọ", "Hạ Chí": "Ngọ", "Tiểu Thử": "Mùi", "Đại Thử": "Mùi",
        "Lập Thu": "Thân", "Xử Thử": "Thân", "Bạch Lộ": "Dậu", "Thu Phân": "Dậu",
        "Hàn Lộ": "Tuất", "Sương Giáng": "Tuất", "Lập Đông": "Hợi", "Tiểu Tuyết": "Hợi",
        "Đại Tuyết": "Tý", "Đông Chí": "Tý", "Tiểu Hàn": "Sửu", "Đại Hàn": "Sửu"
    }
    month_chi = month_chi_map.get(tiet_khi, "Dần")
    chi_idx = CHI.index(month_chi)
    start_can_map = {"Giáp": 2, "Kỷ": 2, "Ất": 4, "Canh": 4, "Bính": 6, "Tân": 6, "Đinh": 8, "Nhâm": 8, "Mậu": 0, "Quý": 0}
    year_can_idx = start_can_map.get(year_can, 0)
    month_offset = (chi_idx - 2) % 12
    month_can_idx = (year_can_idx + month_offset) % 10
    return CAN[month_can_idx], month_chi


def solar_to_lunar(dt):
    """
    High-precision Solar to Lunar conversion for Vietnam (UTC+7).
    Ưu tiên thuật toán Thiên văn Hồ Ngọc Đức trong xem_ngay_dep.py (chuẩn cho mọi năm 1900-2100).
    """
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    try:
        from xem_ngay_dep import solar2lunar as _hn_s2l
        lday, lmonth, lyear, is_leap = _hn_s2l(dt.day, dt.month, dt.year)
        return int(lday), int(lmonth), int(lyear), bool(is_leap)
    except Exception:
        pass

    LUNAR_CONFIG = {
        2024: (2, 10, 0, [29, 30, 29, 29, 30, 29, 30, 30, 29, 30, 30, 29]),
        2025: (1, 29, 6, [30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29]),
        2026: (2, 17, 0, [29, 30, 29, 30, 29, 29, 30, 29, 30, 30, 29, 30]),
        2027: (2, 6, 0,  [30, 29, 30, 29, 30, 29, 29, 30, 29, 30, 30, 30]),
        2028: (1, 26, 5, [29, 30, 29, 30, 30, 29, 30, 29, 29, 30, 30, 29, 30]),
        2029: (2, 13, 0, [30, 29, 30, 29, 30, 29, 30, 29, 29, 30, 30, 29]),
        2030: (2, 2, 0,  [30, 29, 30, 30, 29, 30, 29, 30, 29, 29, 30, 30]),
        2031: (1, 23, 3, [29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 29, 30, 29]),
        2032: (2, 11, 0, [30, 29, 30, 29, 30, 30, 29, 30, 30, 29, 30, 29])
    }

    y = dt.year
    if y not in LUNAR_CONFIG and (y - 1) not in LUNAR_CONFIG:
        return dt.day, dt.month, y, False

    ny_m, ny_d, leap_m, months = LUNAR_CONFIG.get(y, (1, 1, 0, []))
    new_year_dt = datetime.datetime(y, ny_m, ny_d)

    calc_y = y
    if dt < new_year_dt:
        calc_y = y - 1
        if calc_y not in LUNAR_CONFIG:
            return dt.day, dt.month, calc_y, False
        ny_m, ny_d, leap_m, months = LUNAR_CONFIG[calc_y]
        new_year_dt = datetime.datetime(calc_y, ny_m, ny_d)

    diff = (dt.date() - new_year_dt.date()).days
    curr_diff = diff
    for idx, m_len in enumerate(months):
        if curr_diff < m_len:
            physical_month_idx = idx + 1
            if leap_m > 0:
                if physical_month_idx <= leap_m:
                    return curr_diff + 1, physical_month_idx, calc_y, False
                elif physical_month_idx == leap_m + 1:
                    return curr_diff + 1, leap_m, calc_y, True
                else:
                    return curr_diff + 1, physical_month_idx - 1, calc_y, False
            else:
                return curr_diff + 1, physical_month_idx, calc_y, False
        curr_diff -= m_len

    return 1, 1, calc_y, False


# Fixed data for QMDG
SAO_GOC = {1: "Thiên Bồng", 2: "Thiên Nhuế", 3: "Thiên Xung", 4: "Thiên Phụ", 5: "Thiên Cầm", 6: "Thiên Tâm", 7: "Thiên Trụ", 8: "Thiên Nhậm", 9: "Thiên Anh"}
MON_GOC = {1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"}
CHI_CUNG_MAP = {"Tý": 1, "Sửu": 8, "Dần": 8, "Mão": 3, "Thìn": 4, "Tị": 4, "Ngọ": 9, "Mùi": 2, "Thân": 2, "Dậu": 7, "Tuất": 6, "Hợi": 6}


def get_tuan_khong(can, chi):
    """Tính Tuần Không dựa trên Can Chi (2 Chi bị trống trong vòng 60)."""
    can_idx = CAN.index(can)
    chi_idx = CHI.index(chi)
    tuan_thu_chi_idx = (chi_idx - can_idx) % 12
    khong_1 = (tuan_thu_chi_idx - 2) % 12
    khong_2 = (tuan_thu_chi_idx - 1) % 12
    return [CHI_CUNG_MAP[CHI[khong_1]], CHI_CUNG_MAP[CHI[khong_2]]]


def get_ma_ban(chi):
    """Tính Mã Bàn (Thiên Mã) dựa trên Chi."""
    ma_map = {
        "Dần": "Thân", "Ngọ": "Thân", "Tuất": "Thân",
        "Thân": "Dần", "Tý": "Dần", "Thìn": "Dần",
        "Hợi": "Tị", "Mão": "Tị", "Mùi": "Tị",
        "Tị": "Hợi", "Dậu": "Hợi", "Sửu": "Hợi"
    }
    target_chi = ma_map.get(chi, "Thân")
    return CHI_CUNG_MAP[target_chi]


def calculate_qmdg_params(dt=None):
    """Main entry point for QMDG parameters calculation (V101.6 Phù Đầu Chiết Bổ Pháp)."""
    if dt is None:
        dt = get_vn_now()
    if dt.tzinfo is not None:
        # Chuyển về giờ Việt Nam UTC+7 nếu có tzinfo
        try:
            vn_tz = datetime.timezone(datetime.timedelta(hours=7))
            dt = dt.astimezone(vn_tz).replace(tzinfo=None)
        except Exception:
            dt = dt.replace(tzinfo=None)

    tiet_khi = get_tiet_khi(dt)
    # Trong Tứ Trụ & Kỳ Môn, Năm Can Chi tính theo tiết Lập Xuân (~04/02)
    bazi_year = dt.year
    if dt.month == 1 or (dt.month == 2 and tiet_khi in ("Đông Chí", "Tiểu Hàn", "Đại Hàn")):
        bazi_year = dt.year - 1

    year_can, year_chi = get_can_chi_year(bazi_year)
    # Nếu giờ Tý muộn (23:00-23:59), sang Can Chi ngày hôm sau để tính Giờ Tý
    dt_for_day = dt + datetime.timedelta(days=1) if dt.hour == 23 else dt
    day_can, day_chi = get_can_chi_day(dt_for_day)
    hour_can, hour_chi = get_can_chi_hour(day_can, dt.hour)
    month_can, month_chi = get_can_chi_month(year_can, tiet_khi)

    # V133.0: Đồng bộ ngày Âm lịch lúc Dạ Tý (23:00-23:59) với dt_for_day để Mai Hoa · Lục Hào · Kỳ Môn khớp 100%
    lday, lmonth, lyear, is_leap = solar_to_lunar(dt_for_day)

    yang_terms = [
        "Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập",
        "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng"
    ]
    is_duong_don = tiet_khi in yang_terms

    # V101.6: Phù Đầu Định Cục (Chiết Bổ Pháp chuẩn Kỳ Môn Độn Giáp)
    # Tìm Phù Đầu (Giáp hoặc Kỷ) của tuần 5 ngày hiện tại:
    can_d_idx = CAN.index(day_can)
    chi_d_idx = CHI.index(day_chi)
    offset_phu_dau = can_d_idx % 5
    phu_dau_can = CAN[can_d_idx - offset_phu_dau]
    phu_dau_chi = CHI[(chi_d_idx - offset_phu_dau) % 12]

    if phu_dau_chi in ("Tý", "Ngọ", "Mão", "Dậu"):
        yuan = 0
        nguyen_name = "Thượng Nguyên"
    elif phu_dau_chi in ("Dần", "Thân", "Tị", "Hợi"):
        yuan = 1
        nguyen_name = "Trung Nguyên"
    else:
        yuan = 2
        nguyen_name = "Hạ Nguyên"

    cuc_tuple = TIET_KHI_CUC.get(tiet_khi, (1, 7, 4))
    cuc = cuc_tuple[yuan]

    LUC_NGHI_ORDER = ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Đinh", "Bính", "Ất"]
    dia_ban = {}
    curr = cuc
    for nghi in LUC_NGHI_ORDER:
        dia_ban[curr] = nghi
        if is_duong_don:
            curr = curr + 1 if curr < 9 else 1
        else:
            curr = curr - 1 if curr > 1 else 9

    idx_can_h = CAN.index(hour_can)
    idx_chi_h = CHI.index(hour_chi)
    leader_chi_idx = (idx_chi_h - idx_can_h) % 12
    lead_map = {0: "Mậu", 10: "Kỷ", 8: "Canh", 6: "Tân", 4: "Nhâm", 2: "Quý"}
    tuan_thu = lead_map.get(leader_chi_idx, "Mậu")
    leader_palace = 1
    for p, can in dia_ban.items():
        if can == tuan_thu:
            leader_palace = p
            break
    truc_phu = SAO_GOC.get(leader_palace, "Thiên Tâm")
    if leader_palace == 5:
        truc_phu = "Thiên Cầm"
        truc_su = "Tử"
    else:
        truc_su = MON_GOC.get(leader_palace, "Khai")

    # Calculate Void and Horse for all 4 pillars
    khong_gio = get_tuan_khong(hour_can, hour_chi)
    khong_ngay = get_tuan_khong(day_can, day_chi)
    khong_thang = get_tuan_khong(month_can, month_chi)
    khong_nam = get_tuan_khong(year_can, year_chi)

    ma_gio = get_ma_ban(hour_chi)
    ma_ngay = get_ma_ban(day_chi)
    ma_thang = get_ma_ban(month_chi)
    ma_nam = get_ma_ban(year_chi)

    return {
        'can_gio': hour_can, 'chi_gio': hour_chi,
        'can_ngay': day_can, 'chi_ngay': day_chi,
        'can_thang': month_can, 'chi_thang': month_chi,
        'can_nam': year_can, 'chi_nam': year_chi,
        'cuc': cuc, 'is_duong_don': is_duong_don,
        'am_duong_don': f"{'Dương' if is_duong_don else 'Âm'} Độn {cuc} Cục ({nguyen_name})",
        'nguyen': nguyen_name,
        'phu_dau': f"{phu_dau_can} {phu_dau_chi}",
        'tiet_khi': tiet_khi, 'tuan_thu': tuan_thu,
        'leader_palace': leader_palace,
        'truc_phu': truc_phu,
        'truc_su': truc_su + (" Môn" if " Môn" not in truc_su else ""),
        'year': dt.year, 'month': dt.month, 'day': dt.day, 'hour': dt.hour, 'minute': dt.minute,
        'lday': lday, 'lmonth': lmonth, 'lyear': lyear, 'is_leap': is_leap,
        'khong': {
            'gio': khong_gio, 'ngay': khong_ngay, 'thang': khong_thang, 'nam': khong_nam
        },
        'ma': {
            'gio': ma_gio, 'ngay': ma_ngay, 'thang': ma_thang, 'nam': ma_nam
        }
    }

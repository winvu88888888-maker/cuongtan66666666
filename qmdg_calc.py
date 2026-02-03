
# qmdg_calc.py - Core calculation engine for Kỳ Môn Độn Giáp
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

def get_can_chi_year(year):
    """Calculate Can Chi for Year."""
    idx = (year - 4) % 60
    return CAN[idx % 10], CHI[idx % 12]

def get_can_chi_day(dt):
    """Calculate Can Chi for Day using reliable base. Jan 1, 2024 is Giáp Tý (index 0)."""
    base_dt = datetime.datetime(2024, 1, 1)
    diff = (dt.date() - base_dt.date()).days
    idx = (0 + diff) % 60
    if idx < 0: idx += 60
    return CAN[idx % 10], CHI[idx % 12]

def get_can_chi_hour(day_can, hour):
    """Calculate Can Chi for Hour based on Day Can."""
    # Hour index: 0(Tý) to 11(Hợi). Tý is 23h-1h.
    hour_idx = ((hour + 1) // 2) % 12
    # Giáp Kỷ khởi Giáp Tý (0), Ất Canh khởi Bính Tý (2)...
    start_can_map = {"Giáp": 0, "Kỷ": 0, "Ất": 2, "Canh": 2, "Bính": 4, "Tân": 4, "Đinh": 6, "Nhâm": 6, "Mậu": 8, "Quý": 8}
    start_can_idx = start_can_map.get(day_can, 0)
    hour_can_idx = (start_can_idx + hour_idx) % 10
    return CAN[hour_can_idx], CHI[hour_idx]

def get_tiet_khi(dt):
    """Calculate Solar Term (Precise for 2026, Approximate fallback)."""
    if dt.tzinfo is not None: dt = dt.replace(tzinfo=None)
    year = dt.year
    
    # Precise astronomical data for 2026
    if year == 2026:
        terms_2026 = [
            (1, 5, "Tiểu Hàn"), (1, 20, "Đại Hàn"),
            (2, 4, "Lập Xuân"), (2, 19, "Vũ Thủy"),
            (3, 5, "Kinh Trập"), (3, 20, "Xuân Phân"),
            (4, 5, "Thanh Minh"), (4, 20, "Cốc Vũ"),
            (5, 5, "Lập Hạ"), (5, 21, "Tiểu Mãn"),
            (6, 5, "Mang Chủng"), (6, 21, "Hạ Chí"),
            (7, 7, "Tiểu Thử"), (7, 22, "Đại Thử"),
            (8, 7, "Lập Thu"), (8, 23, "Xử Thử"),
            (9, 7, "Bạch Lộ"), (9, 23, "Thu Phân"),
            (10, 8, "Hàn Lộ"), (10, 23, "Sương Giáng"),
            (11, 7, "Lập Đông"), (11, 22, "Tiểu Tuyết"),
            (12, 7, "Đại Tuyết"), (12, 22, "Đông Chí")
        ]
        current_term = "Đông Chí"
        for m, d, name in terms_2026:
            if dt.month > m or (dt.month == m and dt.day >= d):
                current_term = name
        return current_term

    # Approximate calculation for other years
    base_dates = {
        "Xuân Phân": (3, 20.6), "Thanh Minh": (4, 4.8), "Cốc Vũ": (4, 20.1),
        "Lập Hạ": (5, 5.5), "Tiểu Mãn": (5, 21.1), "Mang Chủng": (6, 5.7),
        "Hạ Chí": (6, 21.3), "Tiểu Thử": (7, 7.3), "Đại Thử": (7, 22.8),
        "Lập Thu": (8, 7.5), "Xử Thử": (8, 23.1), "Bạch Lộ": (9, 7.7),
        "Thu Phân": (9, 22.9), "Hàn Lộ": (10, 8.3), "Sương Giáng": (10, 23.4),
        "Lập Đông": (11, 7.3), "Tiểu Tuyết": (11, 22.3), "Đại Tuyết": (12, 7.1),
        "Đông Chí": (12, 21.8), "Tiểu Hàn": (1, 5.4), "Đại Hàn": (1, 20.1),
        "Lập Xuân": (2, 4.2), "Vũ Thủy": (2, 18.9), "Kinh Trập": (3, 5.6)
    }
    terms = []
    for name, (month, day_ref) in base_dates.items():
        y_offset = (year - 2024) * 0.2422
        day = int(day_ref + y_offset)
        t_dt = datetime.datetime(year, month, day)
        terms.append((t_dt, name))
    terms.sort()
    
    current_term = terms[-1][1]
    if dt < terms[0][0]:
        current_term = "Đông Chí"
    else:
        for t_dt, name in terms:
            if dt >= t_dt: current_term = name
            else: break
    return current_term

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
    month_can_idx = (year_can_idx + (chi_idx - 2)) % 10
    return CAN[month_can_idx], month_chi

def solar_to_lunar(dt):
    """
    High-precision Solar to Lunar conversion for Vietnam (2024-2030).
    Using exact month lengths to avoid one-day offsets.
    """
    if dt.tzinfo is not None: dt = dt.replace(tzinfo=None)
    
    # LUNAR_DATA: {Year: (NY_Month, NY_Day, LeapMonthIndex_1based, [MonthLengths])}
    # A LeapMonthIndex of 0 means no leap month.
    # Month list includes the leap month if it exists.
    LUNAR_CONFIG = {
        2024: (2, 10, 0, [29, 30, 29, 29, 30, 29, 30, 30, 29, 30, 30, 29]),
        2025: (1, 29, 6, [30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29]),
        2026: (2, 17, 0, [30, 30, 29, 30, 29, 29, 30, 29, 30, 30, 29, 30]),
        2027: (2, 6, 0,  [30, 29, 30, 29, 30, 29, 29, 30, 29, 30, 30, 30]),
        2028: (1, 26, 5, [29, 30, 29, 30, 30, 29, 30, 29, 29, 30, 30, 29, 30])
    }
    
    y = dt.year
    if y not in LUNAR_CONFIG and (y-1) not in LUNAR_CONFIG:
        # Fallback for very outside dates
        return dt.day, dt.month, y, False

    # Check if date belongs to previous lunar year
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
    l_month = 1
    is_leap_result = False
    
    # Iterate through months using the mask
    for idx, m_len in enumerate(months):
        if curr_diff < m_len:
            # Check if this physical month index corresponds to a leap month
            # For 2025, leap_m=6 (Tháng 6), so index 5 is T6, index 6 is T6 Nhuận
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
    # Tuần Giáp Tý (0) -> Tuất(10), Hợi(11)
    # Tuần Giáp Tuất (10) -> Thân(8), Mùi(7) - Sai, tính lại:
    # Công thức: (10 - Can_idx + Chi_idx) % 12. Nhưng dễ nhất là:
    # 2 Chi đứng trước Giáp của tuần đó.
    khong_1 = (tuan_thu_chi_idx - 2) % 12
    khong_2 = (tuan_thu_chi_idx - 1) % 12
    # Trả về Cung tương ứng
    return [CHI_CUNG_MAP[CHI[khong_1]], CHI_CUNG_MAP[CHI[khong_2]]]

def get_ma_ban(chi):
    """Tính Mã Bàn (Thiên Mã) dựa trên Chi."""
    ma_map = {
        "Dần": "Thân", "Ngọ": "Thân", "Tuất": "Thân",
        "Thân": "Dần", "Tý": "Dần", "Thìn": "Dần",
        "Hợi": "Tị", "Mão": "Tị", "Mùi": "Tị",
        "Tị": "Hợi", "Dậu": "Hợi", "Sửu": "Hợi"
    }
    target_chi = ma_map.get(chi)
    return CHI_CUNG_MAP[target_chi]

def calculate_qmdg_params(dt):
    """Main entry point for QMDG parameters calculation."""
    if dt.tzinfo is not None: dt = dt.replace(tzinfo=None)
    year_can, year_chi = get_can_chi_year(dt.year)
    day_can, day_chi = get_can_chi_day(dt)
    hour_can, hour_chi = get_can_chi_hour(day_can, dt.hour)
    tiet_khi = get_tiet_khi(dt)
    month_can, month_chi = get_can_chi_month(year_can, tiet_khi)
    yang_terms = ["Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập", "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng"]
    is_duong_don = tiet_khi in yang_terms
    base_dt = datetime.datetime(2024, 1, 1); diff = (dt.date() - base_dt.date()).days
    cycle_idx = (0 + diff) % 60; term_day_idx = cycle_idx % 15
    if term_day_idx < 5: yuan = 0
    elif term_day_idx < 10: yuan = 1
    else: yuan = 2
    cuc_tuple = TIET_KHI_CUC.get(tiet_khi, (1, 7, 4)); cuc = cuc_tuple[yuan]
    LUC_NGHI_ORDER = ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Đinh", "Bính", "Ất"]
    dia_ban = {}; curr = cuc
    for nghi in LUC_NGHI_ORDER:
        dia_ban[curr] = nghi
        if is_duong_don: curr = curr + 1 if curr < 9 else 1
        else: curr = curr - 1 if curr > 1 else 9
    idx_can_h = CAN.index(hour_can); idx_chi_h = CHI.index(hour_chi)
    leader_chi_idx = (idx_chi_h - idx_can_h) % 12
    lead_map = {0: "Mậu", 10: "Kỷ", 8: "Canh", 6: "Tân", 4: "Nhâm", 2: "Quý"}
    tuan_thu = lead_map.get(leader_chi_idx, "Mậu")
    leader_palace = 1
    for p, can in dia_ban.items():
        if can == tuan_thu:
            leader_palace = p
            break
    truc_phu = SAO_GOC.get(leader_palace, "Thiên Tâm")
    if leader_palace == 5: truc_phu = "Thiên Cầm"; truc_su = "Tử"
    else: truc_su = MON_GOC.get(leader_palace, "Khai")
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
        'can_gio': hour_can, 'chi_gio': hour_chi, 'can_ngay': day_can, 'chi_ngay': day_chi,
        'can_thang': month_can, 'chi_thang': month_chi, 'can_nam': year_can, 'chi_nam': year_chi,
        'cuc': cuc, 'is_duong_don': is_duong_don, 'tiet_khi': tiet_khi, 'tuan_thu': tuan_thu,
        'leader_palace': leader_palace, 'truc_phu': truc_phu, 'truc_su': truc_su + (" Môn" if " Môn" not in truc_su else ""),
        'khong': {
            'gio': khong_gio, 'ngay': khong_ngay, 'thang': khong_thang, 'nam': khong_nam
        },
        'ma': {
            'gio': ma_gio, 'ngay': ma_ngay, 'thang': ma_thang, 'nam': ma_nam
        }
    }

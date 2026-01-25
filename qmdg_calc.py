
# qmdg_calc.py - Core calculation engine for Kỳ Môn Độn Giáp
import math
from datetime import datetime, timedelta

# Data for calculations
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

TIET_KHI_LIST = [
    "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng",
    "Hạ Chí", "Tiểu Thử", "Đại Thử", "Lập Thu", "Xử Thử", "Bạch Lộ",
    "Thu Phân", "Hàn Lộ", "Sương Giáng", "Lập Đông", "Tiểu Tuyết", "Đại Tuyết",
    "Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập"
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

def get_can_chi_day(dt):
    """Simplified Can Chi for Day (Reference date: JDN)"""
    # Base date: 2024-01-01 is Giáp Tý (Simplified)
    # Actually 2024-01-01 is Giáp Thân (60-day cycle index: 20)
    base_dt = datetime(2024, 1, 1)
    diff = (dt.date() - base_dt.date()).days
    idx = (20 + diff) % 60
    return CAN[idx % 10], CHI[idx % 12]

def get_can_chi_hour(day_can, hour):
    """Calculate Can Chi for Hour based on Day Can"""
    hour_chi_idx = ((hour + 1) // 2) % 12
    # Giáp Kỷ khởi Giáp Tý, Ất Canh khởi Bính Tý...
    start_can_map = {"Giáp": 0, "Kỷ": 0, "Ất": 2, "Canh": 2, "Bính": 4, "Tân": 4, "Đinh": 6, "Nhâm": 6, "Mậu": 8, "Quý": 8}
    start_can_idx = start_can_map.get(day_can, 0)
    hour_can_idx = (start_can_idx + hour_chi_idx) % 10
    return CAN[hour_can_idx], CHI[hour_chi_idx]

def get_tiet_khi(dt):
    """Simplified Solar Term prediction (Approximate)"""
    # Based on average dates
    year = dt.year
    terms = [
        (datetime(year, 3, 20), "Xuân Phân"), (datetime(year, 4, 4), "Thanh Minh"),
        (datetime(year, 4, 20), "Cốc Vũ"), (datetime(year, 5, 5), "Lập Hạ"),
        (datetime(year, 5, 21), "Tiểu Mãn"), (datetime(year, 6, 5), "Mang Chủng"),
        (datetime(year, 6, 21), "Hạ Chí"), (datetime(year, 7, 7), "Tiểu Thử"),
        (datetime(year, 7, 23), "Đại Thử"), (datetime(year, 8, 7), "Lập Thu"),
        (datetime(year, 8, 23), "Xử Thử"), (datetime(year, 9, 7), "Bạch Lộ"),
        (datetime(year, 9, 23), "Thu Phân"), (datetime(year, 10, 8), "Hàn Lộ"),
        (datetime(year, 10, 23), "Sương Giáng"), (datetime(year, 11, 7), "Lập Đông"),
        (datetime(year, 11, 22), "Tiểu Tuyết"), (datetime(year, 12, 7), "Đại Tuyết"),
        (datetime(year, 12, 21), "Đông Chí"), (datetime(year, 1, 5), "Tiểu Hàn"),
        (datetime(year, 1, 20), "Đại Hàn"), (datetime(year, 2, 4), "Lập Xuân"),
        (datetime(year, 2, 19), "Vũ Thủy"), (datetime(year, 3, 5), "Kinh Trập")
    ]
    # Sort and find current
    terms.sort()
    current_term = terms[-1][1]
    for term_dt, term_name in terms:
        if dt < term_dt:
            break
        current_term = term_name
    return current_term

def calculate_qmdg_params(dt):
    """Main entry point for QMDG parameters calculation"""
    # Ensure dt is naive for comparison with static terms
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
        
    day_can, day_chi = get_can_chi_day(dt)
    hour_can, hour_chi = get_can_chi_hour(day_can, dt.hour)
    tiet_khi = get_tiet_khi(dt)
    
    # Determine is_duong_don (Yang/Yin cycle)
    # Đông Chí to Hạ Chí is Yang (Dương)
    yang_terms = ["Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập", "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng"]
    is_duong_don = tiet_khi in yang_terms
    
    # Determine Cuc (Simplified Phù Đầu)
    # 60 day cycle index
    base_dt = datetime(2024, 1, 1)
    diff = (dt.date() - base_dt.date()).days
    cycle_idx = (20 + diff) % 60 # 0-59
    
    # Phù đầu index within 15-day term (3 cycles of 5 days)
    # In reality it's more complex, but here's a working approximation
    term_day_idx = cycle_idx % 15
    if term_day_idx < 5: yuan = 0 # Thượng Nguyên
    elif term_day_idx < 10: yuan = 1 # Trung Nguyên
    else: yuan = 2 # Hạ Nguyên
    
    cuc_tuple = TIET_KHI_CUC.get(tiet_khi, (1, 7, 4))
    cuc = cuc_tuple[yuan]
    
    # Calculate Trực Phù and Trực Sử (Simplified logic for the board)
    # These are usually derived from the Cuc and Can of the hour
    # We will provide default values that our board can use to initialize
    return {
        'can_gio': hour_can, 'chi_gio': hour_chi,
        'can_ngay': day_can, 'chi_ngay': day_chi,
        'can_thang': "Ất", 'chi_thang': "Mùi", # Placeholders for Month/Year if needed
        'can_nam': "Giáp", 'chi_nam': "Thìn",
        'cuc': cuc, 'is_duong_don': is_duong_don,
        'tiet_khi': tiet_khi,
        'truc_phu': "Thiên Tâm", # Will be correctly calculated by lap_ban_qmdg if needed
        'truc_su': "Khai Môn"
    }


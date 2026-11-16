import random
from functools import lru_cache
from datetime import datetime, timedelta

LUC_THAN = ["Huynh Đệ", "Phụ Mẫu", "Quan Quỷ", "Thê Tài", "Tử Tôn"]
LUC_THU = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
VERSION_LH = "V133.0_TANG_SAN_BOC_DICH_CANON"
PALACE_ELEMENTS = {"Càn":"Kim", "Đoài":"Kim", "Ly":"Hỏa", "Chấn":"Mộc", "Tốn":"Mộc", "Khảm":"Thủy", "Cấn":"Thổ", "Khôn":"Thổ"}

# =====================================================
# COMPLETE 64 HEXAGRAM PALACE MAPPING (京房八宮)
# =====================================================
HEXAGRAM_PALACES = {
    # Càn Cung (Kim)
    "Càn Vi Thiên":"Càn", "Thiên Phong Cấu":"Càn", "Thiên Sơn Độn":"Càn", "Thiên Địa Bĩ":"Càn",
    "Phong Địa Quan":"Càn", "Sơn Địa Bác":"Càn", "Hỏa Địa Tấn":"Càn", "Hỏa Thiên Đại Hữu":"Càn",
    # Khôn Cung (Thổ)
    "Khôn Vi Địa":"Khôn", "Địa Lôi Phục":"Khôn", "Địa Trạch Lâm":"Khôn", "Địa Thiên Thái":"Khôn",
    "Lôi Thiên Đại Tráng":"Khôn", "Trạch Thiên Quải":"Khôn", "Thủy Thiên Nhu":"Khôn", "Thủy Địa Tỷ":"Khôn",
    # Chấn Cung (Mộc)
    "Chấn Vi Lôi":"Chấn", "Lôi Địa Dự":"Chấn", "Lôi Thủy Giải":"Chấn", "Lôi Phong Hằng":"Chấn",
    "Địa Phong Thăng":"Chấn", "Thủy Phong Tỉnh":"Chấn", "Trạch Phong Đại Quá":"Chấn", "Trạch Lôi Tùy":"Chấn",
    # Tốn Cung (Mộc)
    "Tốn Vi Phong":"Tốn", "Phong Thiên Tiểu Súc":"Tốn", "Phong Hỏa Gia Nhân":"Tốn", "Phong Lôi Ích":"Tốn",
    "Thiên Lôi Vô Vọng":"Tốn", "Hỏa Lôi Phệ Hạp":"Tốn", "Sơn Lôi Di":"Tốn", "Sơn Phong Cổ":"Tốn",
    # Khảm Cung (Thủy)
    "Khảm Vi Thủy":"Khảm", "Thủy Trạch Tiết":"Khảm", "Thủy Lôi Truân":"Khảm", "Thủy Hỏa Ký Tế":"Khảm",
    "Trạch Hỏa Cách":"Khảm", "Lôi Hỏa Phong":"Khảm", "Địa Hỏa Minh Di":"Khảm", "Địa Thủy Sư":"Khảm",
    # Ly Cung (Hỏa)
    "Ly Vi Hỏa":"Ly", "Hỏa Sơn Lữ":"Ly", "Hỏa Phong Đỉnh":"Ly", "Hỏa Thủy Vị Tế":"Ly",
    "Sơn Thủy Mông":"Ly", "Phong Thủy Hoán":"Ly", "Thiên Thủy Tụng":"Ly", "Thiên Hỏa Đồng Nhân":"Ly",
    # Cấn Cung (Thổ)
    "Cấn Vi Sơn":"Cấn", "Sơn Hỏa Bí":"Cấn", "Sơn Thiên Đại Súc":"Cấn", "Sơn Trạch Tổn":"Cấn",
    "Hỏa Trạch Khuê":"Cấn", "Thiên Trạch Lý":"Cấn", "Phong Trạch Trung Phu":"Cấn", "Phong Sơn Tiệm":"Cấn",
    # Đoài Cung (Kim)
    "Đoài Vi Trạch":"Đoài", "Trạch Thủy Khốn":"Đoài", "Trạch Địa Tụy":"Đoài", "Trạch Sơn Hàm":"Đoài",
    "Thủy Sơn Kiển":"Đoài", "Địa Sơn Khiêm":"Đoài", "Lôi Sơn Tiểu Quá":"Đoài", "Lôi Trạch Quy Muội":"Đoài",
}

# =====================================================
# THẾ/ỨNG POSITION FOR ALL 64 HEXAGRAMS
# Format: hexagram_name -> thế position (1-6)
# Ứng = ((Thế - 1 + 3) % 6) + 1
# =====================================================
THE_POSITION = {
    # Càn Cung: Pure=6, 1-world=1, 2-world=2, 3-world=3, 4-world=4, 5-world=5, Du Hồn=4, Quy Hồn=3
    "Càn Vi Thiên":6, "Thiên Phong Cấu":1, "Thiên Sơn Độn":2, "Thiên Địa Bĩ":3,
    "Phong Địa Quan":4, "Sơn Địa Bác":5, "Hỏa Địa Tấn":4, "Hỏa Thiên Đại Hữu":3,
    # Khôn Cung
    "Khôn Vi Địa":6, "Địa Lôi Phục":1, "Địa Trạch Lâm":2, "Địa Thiên Thái":3,
    "Lôi Thiên Đại Tráng":4, "Trạch Thiên Quải":5, "Thủy Thiên Nhu":4, "Thủy Địa Tỷ":3,
    # Chấn Cung
    "Chấn Vi Lôi":6, "Lôi Địa Dự":1, "Lôi Thủy Giải":2, "Lôi Phong Hằng":3,
    "Địa Phong Thăng":4, "Thủy Phong Tỉnh":5, "Trạch Phong Đại Quá":4, "Trạch Lôi Tùy":3,
    # Tốn Cung
    "Tốn Vi Phong":6, "Phong Thiên Tiểu Súc":1, "Phong Hỏa Gia Nhân":2, "Phong Lôi Ích":3,
    "Thiên Lôi Vô Vọng":4, "Hỏa Lôi Phệ Hạp":5, "Sơn Lôi Di":4, "Sơn Phong Cổ":3,
    # Khảm Cung
    "Khảm Vi Thủy":6, "Thủy Trạch Tiết":1, "Thủy Lôi Truân":2, "Thủy Hỏa Ký Tế":3,
    "Trạch Hỏa Cách":4, "Lôi Hỏa Phong":5, "Địa Hỏa Minh Di":4, "Địa Thủy Sư":3,
    # Ly Cung
    "Ly Vi Hỏa":6, "Hỏa Sơn Lữ":1, "Hỏa Phong Đỉnh":2, "Hỏa Thủy Vị Tế":3,
    "Sơn Thủy Mông":4, "Phong Thủy Hoán":5, "Thiên Thủy Tụng":4, "Thiên Hỏa Đồng Nhân":3,
    # Cấn Cung
    "Cấn Vi Sơn":6, "Sơn Hỏa Bí":1, "Sơn Thiên Đại Súc":2, "Sơn Trạch Tổn":3,
    "Hỏa Trạch Khuê":4, "Thiên Trạch Lý":5, "Phong Trạch Trung Phu":4, "Phong Sơn Tiệm":3,
    # Đoài Cung
    "Đoài Vi Trạch":6, "Trạch Thủy Khốn":1, "Trạch Địa Tụy":2, "Trạch Sơn Hàm":3,
    "Thủy Sơn Kiển":4, "Địa Sơn Khiêm":5, "Lôi Sơn Tiểu Quá":4, "Lôi Trạch Quy Muội":3,
}

# =====================================================
# NẠP GIÁP - Each trigram has 6 branches
# Positions 1-3 (indices 0-2): for INNER (lower) trigram
# Positions 4-6 (indices 3-5): for OUTER (upper) trigram
# =====================================================
NAP_GIAP_MAP = {
    "Càn":["Tý-Thủy", "Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ"],
    "Khôn":["Mùi-Thổ", "Tị-Hỏa", "Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim"],
    "Cấn":["Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ", "Tý-Thủy", "Dần-Mộc"],
    "Đoài":["Tị-Hỏa", "Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim", "Mùi-Thổ"],
    "Khảm":["Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ", "Tý-Thủy"],
    "Ly":["Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim", "Mùi-Thổ", "Tị-Hỏa"],
    "Chấn":["Tý-Thủy", "Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ"],
    "Tốn":["Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim", "Mùi-Thổ", "Tị-Hỏa", "Mão-Mộc"]
}

# V129.0: Kinh Phòng Thiên Can Nạp Giáp (Nội quái hào 1-3, Ngoại quái hào 4-6) chuẩn thangnc/i-ching-plugins & yaomancy/liuyao-engine
NAP_GIAP_CAN_MAP = {
    "Càn": ("Giáp", "Nhâm"),
    "Khôn": ("Ất", "Quý"),
    "Cấn": ("Bính", "Bính"),
    "Đoài": ("Đinh", "Đinh"),
    "Khảm": ("Mậu", "Mậu"),
    "Ly": ("Kỷ", "Kỷ"),
    "Chấn": ("Canh", "Canh"),
    "Tốn": ("Tân", "Tân"),
}

# Map trigram index to name
QUAI_IDX_TO_NAME = {1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"}

# =====================================================
# COMPLETE 64 HEXAGRAM NAMES
# =====================================================
HEXAGRAM_NAMES = {
    (1, 1): "Càn Vi Thiên", (8, 8): "Khôn Vi Địa", (6, 6): "Khảm Vi Thủy", (3, 3): "Ly Vi Hỏa",
    (4, 4): "Chấn Vi Lôi", (5, 5): "Tốn Vi Phong", (7, 7): "Cấn Vi Sơn", (2, 2): "Đoài Vi Trạch",
    # Càn Cung
    (1, 8): "Thiên Địa Bĩ", (1, 5): "Thiên Phong Cấu", (1, 7): "Thiên Sơn Độn",
    (1, 2): "Thiên Trạch Lý", (1, 3): "Thiên Hỏa Đồng Nhân", (1, 4): "Thiên Lôi Vô Vọng",
    (1, 6): "Thiên Thủy Tụng",
    # Khôn Cung
    (8, 1): "Địa Thiên Thái", (8, 4): "Địa Lôi Phục", (8, 2): "Địa Trạch Lâm",
    (8, 5): "Địa Phong Thăng", (8, 6): "Địa Thủy Sư", (8, 3): "Địa Hỏa Minh Di",
    (8, 7): "Địa Sơn Khiêm",
    # Ly Cung
    (3, 7): "Hỏa Sơn Lữ", (3, 5): "Hỏa Phong Đỉnh", (3, 6): "Hỏa Thủy Vị Tế",
    (3, 1): "Hỏa Thiên Đại Hữu", (3, 2): "Hỏa Trạch Khuê", (3, 4): "Hỏa Lôi Phệ Hạp",
    (3, 8): "Hỏa Địa Tấn",
    # Khảm Cung
    (6, 3): "Thủy Hỏa Ký Tế", (6, 2): "Thủy Trạch Tiết", (6, 4): "Thủy Lôi Truân",
    (6, 1): "Thủy Thiên Nhu", (6, 7): "Thủy Sơn Kiển", (6, 5): "Thủy Phong Tỉnh",
    (6, 8): "Thủy Địa Tỷ",
    # Chấn Cung
    (4, 1): "Lôi Thiên Đại Tráng", (4, 8): "Lôi Địa Dự", (4, 6): "Lôi Thủy Giải",
    (4, 5): "Lôi Phong Hằng", (4, 3): "Lôi Hỏa Phong", (4, 2): "Lôi Trạch Quy Muội",
    (4, 7): "Lôi Sơn Tiểu Quá",
    # Tốn Cung
    (5, 1): "Phong Thiên Tiểu Súc", (5, 3): "Phong Hỏa Gia Nhân", (5, 4): "Phong Lôi Ích",
    (5, 2): "Phong Trạch Trung Phu", (5, 6): "Phong Thủy Hoán", (5, 7): "Phong Sơn Tiệm",
    (5, 8): "Phong Địa Quan",
    # Cấn Cung
    (7, 1): "Sơn Thiên Đại Súc", (7, 3): "Sơn Hỏa Bí", (7, 2): "Sơn Trạch Tổn",
    (7, 4): "Sơn Lôi Di", (7, 6): "Sơn Thủy Mông", (7, 8): "Sơn Địa Bác",
    (7, 5): "Sơn Phong Cổ",
    # Đoài Cung
    (2, 1): "Trạch Thiên Quải", (2, 8): "Trạch Địa Tụy", (2, 3): "Trạch Hỏa Cách",
    (2, 4): "Trạch Lôi Tùy", (2, 6): "Trạch Thủy Khốn", (2, 7): "Trạch Sơn Hàm",
    (2, 5): "Trạch Phong Đại Quá",
}

def lines_to_quai_num(lines):
    m = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4, (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}
    return m.get(tuple(lines), 1)

def get_hex_name(lines):
    lower = lines_to_quai_num(lines[:3])
    upper = lines_to_quai_num(lines[3:])
    return HEXAGRAM_NAMES.get((upper, lower), f"Quẻ {upper}-{lower}")

@lru_cache(maxsize=256)
def get_nap_giap_for_hexagram(lower_idx, upper_idx):
    """Get proper Nạp Giáp for a hexagram using inner/outer trigram rules.
    Inner trigram uses positions 1-3 (indices 0-2) of its NAP_GIAP_MAP.
    Outer trigram uses positions 4-6 (indices 3-5) of its NAP_GIAP_MAP.
    """
    lower_name = QUAI_IDX_TO_NAME.get(lower_idx, "Càn")
    upper_name = QUAI_IDX_TO_NAME.get(upper_idx, "Càn")
    
    lower_nap_giap = NAP_GIAP_MAP.get(lower_name, NAP_GIAP_MAP["Càn"])
    upper_nap_giap = NAP_GIAP_MAP.get(upper_name, NAP_GIAP_MAP["Càn"])
    
    # Inner trigram: first 3 positions, Outer trigram: last 3 positions
    result = lower_nap_giap[:3] + upper_nap_giap[3:]
    return result

@lru_cache(maxsize=256)
def get_nap_giap_can_for_hexagram(lower_idx, upper_idx):
    """Lấy Thiên Can Nạp Giáp chuẩn Kinh Phòng cho 6 hào (hào 1-3 Nội quái, hào 4-6 Ngoại quái)."""
    lower_name = QUAI_IDX_TO_NAME.get(lower_idx, "Càn")
    upper_name = QUAI_IDX_TO_NAME.get(upper_idx, "Càn")
    can_in = NAP_GIAP_CAN_MAP.get(lower_name, ("Giáp", "Nhâm"))[0]
    can_out = NAP_GIAP_CAN_MAP.get(upper_name, ("Giáp", "Nhâm"))[1]
    return [can_in, can_in, can_in, can_out, can_out, can_out]

def get_element_strength(h_element, month):
    """
    V129.0 FIX CHUẨN NGŨ HÀNH ĐẠI NGHĨA & TĂNG SAN BỐC DỊCH (thangnc/i-ching-plugins):
    Đương lệnh giả Vượng, Lệnh sinh giả Tướng, Sinh lệnh giả Hưu, Khắc lệnh giả Tù, Lệnh khắc giả Tử!
    """
    chi_element_map = {
        "Dần": "Mộc", "Mão": "Mộc", "Tị": "Hỏa", "Tỵ": "Hỏa", "Ngọ": "Hỏa",
        "Thân": "Kim", "Dậu": "Kim", "Hợi": "Thủy", "Tý": "Thủy",
        "Thìn": "Thổ", "Tuất": "Thổ", "Sửu": "Thổ", "Mùi": "Thổ",
    }
    month_element_map = {
        1: "Mộc", 2: "Mộc", 4: "Hỏa", 5: "Hỏa", 7: "Kim", 8: "Kim",
        10: "Thủy", 11: "Thủy", 3: "Thổ", 6: "Thổ", 9: "Thổ", 12: "Thổ",
    }
    if isinstance(month, str) and month in chi_element_map:
        m_el = chi_element_map[month]
    else:
        m_el = month_element_map.get(month, "Thổ")

    strengths = {
        "Mộc": {"Mộc": "Vượng", "Hỏa": "Tướng", "Thủy": "Hưu", "Kim": "Tù", "Thổ": "Tử"},
        "Hỏa": {"Hỏa": "Vượng", "Thổ": "Tướng", "Mộc": "Hưu", "Thủy": "Tù", "Kim": "Tử"},
        "Thổ": {"Thổ": "Vượng", "Kim": "Tướng", "Hỏa": "Hưu", "Mộc": "Tù", "Thủy": "Tử"},
        "Kim": {"Kim": "Vượng", "Thủy": "Tướng", "Thổ": "Hưu", "Hỏa": "Tù", "Mộc": "Tử"},
        "Thủy": {"Thủy": "Vượng", "Mộc": "Tướng", "Kim": "Hưu", "Thổ": "Tù", "Hỏa": "Tử"},
    }
    return strengths.get(m_el, {}).get(h_element, "Bình")

@lru_cache(maxsize=256)
def get_tuan_khong(can_ngay, chi_ngay):
    if chi_ngay == "Tỵ": chi_ngay = "Tị"
    can_map = {"Giáp":1, "Ất":2, "Bính":3, "Đinh":4, "Mậu":5, "Kỷ":6, "Canh":7, "Tân":8, "Nhâm":9, "Quý":10}
    chi_map = {"Tý":1, "Sửu":2, "Dần":3, "Mão":4, "Thìn":5, "Tị":6, "Ngọ":7, "Mùi":8, "Thân":9, "Dậu":10, "Tuất":11, "Hợi":12}
    
    c_idx = can_map.get(can_ngay, 1)
    ch_idx = chi_map.get(chi_ngay, 1)
    
    start_phi = (ch_idx - c_idx + 1)
    if start_phi <= 0: start_phi += 12
    
    void_indices = [(start_phi + 10 - 1) % 12 + 1, (start_phi + 11 - 1) % 12 + 1]
    inv_chi_map = {v: k for k, v in chi_map.items()}
    return [inv_chi_map.get(idx) for idx in void_indices]

def get_dich_ma(chi_ngay):
    if chi_ngay == "Tỵ": chi_ngay = "Tị"
    map_ma = {
        "Thân": "Dần", "Tý": "Dần", "Thìn": "Dần",
        "Dần": "Thân", "Ngọ": "Thân", "Tuất": "Thân",
        "Tị": "Hợi", "Dậu": "Hợi", "Sửu": "Hợi",
        "Hợi": "Tị", "Mão": "Tị", "Mùi": "Tị"
    }
    return map_ma.get(chi_ngay, "")

def get_luc_than(h_element, p_element):
    """Lục Thân based on palace element vs. line element."""
    relations = {
        "Kim": {"Kim": "Huynh Đệ", "Mộc": "Thê Tài", "Hỏa": "Quan Quỷ", "Thủy": "Tử Tôn", "Thổ": "Phụ Mẫu"},
        "Mộc": {"Mộc": "Huynh Đệ", "Thổ": "Thê Tài", "Kim": "Quan Quỷ", "Hỏa": "Tử Tôn", "Thủy": "Phụ Mẫu"},
        "Thủy": {"Thủy": "Huynh Đệ", "Hỏa": "Thê Tài", "Thổ": "Quan Quỷ", "Mộc": "Tử Tôn", "Kim": "Phụ Mẫu"},
        "Hỏa": {"Hỏa": "Huynh Đệ", "Kim": "Thê Tài", "Thủy": "Quan Quỷ", "Thổ": "Tử Tôn", "Mộc": "Phụ Mẫu"},
        "Thổ": {"Thổ": "Huynh Đệ", "Thủy": "Thê Tài", "Mộc": "Quan Quỷ", "Kim": "Tử Tôn", "Hỏa": "Phụ Mẫu"},
    }
    return relations.get(p_element, {}).get(h_element, "Huynh Đệ")


from qmdg_calc import solar_to_lunar

def lap_qua_luc_hao(year, month, day, hour, topic="Chung", can_ngay="Giáp", chi_ngay="Tý", can_thang=None, chi_thang=None, **kwargs):
    # Convert to Lunar Date (V133.0: Chuẩn phút thiên văn & đồng bộ Dạ Tý 23:00-23:59)
    _min_init = int(kwargs.get("minute", 0) or 0)
    _sec_init = int(kwargs.get("second", 0) or 0)
    dt = datetime(year, month, day, hour, _min_init, _sec_init)
    dt_lunar = dt + timedelta(days=1) if hour == 23 else dt
    lday, lmonth, lyear, is_leap = solar_to_lunar(dt_lunar)
    if not chi_thang or not can_thang or (can_thang == "Giáp" and chi_thang == "Tý" and lmonth != 11):
        try:
            from qmdg_calc import calculate_qmdg_params as _calc_lh_p
            _p_lh = _calc_lh_p(dt)
            can_thang = _p_lh.get("can_thang") or can_thang or "Giáp"
            chi_thang = _p_lh.get("chi_thang") or chi_thang
            if can_ngay == "Giáp" and chi_ngay == "Tý":
                can_ngay = _p_lh.get("can_ngay", can_ngay)
                chi_ngay = _p_lh.get("chi_ngay", chi_ngay)
        except Exception:
            pass
        if not chi_thang:
            _thang_chis = ["Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]
            chi_thang = _thang_chis[(lmonth - 1) % 12]
        if not can_thang:
            can_thang = "Giáp"
    
    # Year Chi index: Tý=1, Sửu=2, ..., Hợi=12
    lyear_chi_idx = (lyear - 4) % 12 + 1
    
    # Hour animal index (Tý=1, Sửu=2... Hợi=12)
    v_hour = ((hour + 1) // 2) % 12 + 1
    if hour == 23: v_hour = 1 # Tý starts at 23:00
    
    # Standard time-based calculation using Lunar numbers
    _q_txt_lh = kwargs.get("question_text", "")
    _min_lh = kwargs.get("minute", 0)
    _sec_lh = kwargs.get("second", 0)
    _salt_lh = kwargs.get("cast_salt", 0)
    _up_ov_lh = kwargs.get("upper_override", None)
    _lo_ov_lh = kwargs.get("lower_override", None)
    _mv_ov_lh = kwargs.get("moving_override", None)
    _up_off_lh, _lo_off_lh, _dong_off_lh = 0, 0, 0
    if _q_txt_lh or _min_lh or _sec_lh or _salt_lh:
        try:
            from mai_hoa_dich_so import _compute_question_resonance_offsets
            _up_off_lh, _lo_off_lh, _dong_off_lh = _compute_question_resonance_offsets(
                question_text=_q_txt_lh, minute=_min_lh, second=_sec_lh, cast_salt=_salt_lh
            )
        except Exception:
            _up_off_lh = int(_min_lh or 0) + int(_salt_lh or 0) * 3
            _lo_off_lh = int(_min_lh or 0) + int(_sec_lh or 0) + int(_salt_lh or 0) * 5
            _dong_off_lh = int(_salt_lh or 0)
    total_upper = lyear_chi_idx + lmonth + lday + _up_off_lh
    total_lower = total_upper + v_hour + _lo_off_lh
    
    upper_idx = int(_up_ov_lh) if _up_ov_lh in (1, 2, 3, 4, 5, 6, 7, 8) else (((total_upper - 1) % 8) + 1)
    lower_idx = int(_lo_ov_lh) if _lo_ov_lh in (1, 2, 3, 4, 5, 6, 7, 8) else (((total_lower - 1) % 8) + 1)
    moving_idx = int(_mv_ov_lh) if _mv_ov_lh in (1, 2, 3, 4, 5, 6) else (((total_lower + _dong_off_lh - 1) % 6) + 1)  # 1-indexed

    # Convert trigram index to lines
    trigrams = {
        1: [1, 1, 1], 2: [1, 1, 0], 3: [1, 0, 1], 4: [1, 0, 0],
        5: [0, 1, 1], 6: [0, 1, 0], 7: [0, 0, 1], 8: [0, 0, 0]
    }

    _coin_throws = kwargs.get("coin_throws", None)
    _mv_list_ov = kwargs.get("moving_list_override", None)

    if isinstance(_coin_throws, (list, tuple)) and len(_coin_throws) == 6 and all(x in (6, 7, 8, 9) for x in _coin_throws):
        hao_results = [int(x) for x in _coin_throws]
        ban_lines = [1 if x in (7, 9) else 0 for x in hao_results]
        bien_lines = [0 if x == 9 else (1 if x == 6 else (1 if x == 7 else 0)) for x in hao_results]
        dong_list = [idx + 1 for idx, x in enumerate(hao_results) if x in (6, 9)]
        lower_idx = lines_to_quai_num(ban_lines[:3])
        upper_idx = lines_to_quai_num(ban_lines[3:])
    else:
        ban_lines = trigrams[lower_idx] + trigrams[upper_idx]
        if isinstance(_mv_list_ov, (list, tuple)):
            dong_list = sorted({int(x) for x in _mv_list_ov if str(x).isdigit() and 1 <= int(x) <= 6})
        else:
            dong_list = [moving_idx]
        hao_results = []
        bien_lines = list(ban_lines)
        for i in range(1, 7):
            if i in dong_list:
                hao_type = 9 if ban_lines[i - 1] == 1 else 6
                bien_lines[i - 1] = 0 if ban_lines[i - 1] == 1 else 1
            else:
                hao_type = 7 if ban_lines[i - 1] == 1 else 8
            hao_results.append(hao_type)

    ban_name = get_hex_name(ban_lines)
    bien_name = get_hex_name(bien_lines)
    
    # === FIX 1: Palace lookup (complete 64 hexagram mapping) ===
    palace = HEXAGRAM_PALACES.get(ban_name, "Càn")
    p_element = PALACE_ELEMENTS.get(palace, "Kim")
    
    # === FIX 2: Lục Thú - Corrected mapping ===
    start_thu = {
        "Giáp": 0, "Ất": 0, 
        "Bính": 1, "Đinh": 1, 
        "Mậu": 2, 
        "Kỷ": 3, 
        "Canh": 4, "Tân": 4, 
        "Nhâm": 5, "Quý": 5
    }.get(can_ngay, 0)
    
    # === FIX 3: Nạp Giáp Địa Chi + Thiên Can Kinh Phòng + 60 Nạp Âm (V129.0) ===
    nap_giap_ban = get_nap_giap_for_hexagram(lower_idx, upper_idx)
    nap_giap_can_ban = get_nap_giap_can_for_hexagram(lower_idx, upper_idx)
    
    # Biến hexagram trigrams for separate nạp giáp
    bien_lower_idx = lines_to_quai_num(bien_lines[:3])
    bien_upper_idx = lines_to_quai_num(bien_lines[3:])
    nap_giap_bien = get_nap_giap_for_hexagram(bien_lower_idx, bien_upper_idx)
    nap_giap_can_bien = get_nap_giap_can_for_hexagram(bien_lower_idx, bien_upper_idx)

    try:
        from github_prophecy_engine import NAP_AM_60 as _NAP_AM_60
        from github_zhouyi_384_data import get_zhouyi_line as _get_zy_line
    except Exception:
        _NAP_AM_60 = {}
        _get_zy_line = lambda _h, _p: {}
    
    # === FIX 4: Thế/Ứng - Complete lookup table ===
    the_pos = THE_POSITION.get(ban_name, 3)
    ung_pos = ((the_pos - 1 + 3) % 6) + 1
    
    # Advanced markers
    void_branches = get_tuan_khong(can_ngay, chi_ngay)
    ma_branch = get_dich_ma(chi_ngay)
    
    # Nhật phá & Nguyệt phá (Xung)
    def is_xung(chi1, chi2):
        xung_map = {"Tý":"Ngọ", "Sửu":"Mùi", "Dần":"Thân", "Mão":"Dậu", "Thìn":"Tuất", "Tị":"Hợi",
                    "Ngọ":"Tý", "Mùi":"Sửu", "Thân":"Dần", "Dậu":"Mão", "Tuất":"Thìn", "Hợi":"Tị"}
        return xung_map.get(chi1) == chi2
        
    def is_hop(chi1, chi2):
        hop_map = {"Tý":"Sửu", "Sửu":"Tý", "Dần":"Hợi", "Hợi":"Dần", "Mão":"Tuất", "Tuất":"Mão",
                   "Thìn":"Dậu", "Dậu":"Thìn", "Tị":"Thân", "Thân":"Tị", "Ngọ":"Mùi", "Mùi":"Ngọ"}
        return hop_map.get(chi1) == chi2

    _SINH_EL = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
    _KHAC_EL = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
    _CHI_EL = {
        "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
        "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
        "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
    }
    _MO_BY_EL = {"Kim": "Sửu", "Mộc": "Mùi", "Thủy": "Thìn", "Thổ": "Thìn", "Hỏa": "Tuất"}
    _TUYET_BY_EL = {"Kim": "Dần", "Mộc": "Thân", "Thủy": "Tị", "Thổ": "Tị", "Hỏa": "Hợi"}
    _TIEN_PAIRS = {("Hợi", "Tý"), ("Dần", "Mão"), ("Tị", "Ngọ"), ("Thân", "Dậu"), ("Sửu", "Thìn"), ("Mùi", "Tuất")}
    _THOAI_PAIRS = {("Tý", "Hợi"), ("Mão", "Dần"), ("Ngọ", "Tị"), ("Dậu", "Thân"), ("Thìn", "Sửu"), ("Tuất", "Mùi")}
    _LUC_XUNG_SET = {
        "Càn Vi Thiên", "Khôn Vi Địa", "Khảm Vi Thủy", "Ly Vi Hỏa",
        "Chấn Vi Lôi", "Tốn Vi Phong", "Cấn Vi Sơn", "Đoài Vi Trạch",
        "Lôi Thiên Đại Tráng", "Thiên Lôi Vô Vọng",
    }
    _LUC_HOP_SET = {
        "Địa Thiên Thái", "Thiên Địa Bĩ", "Địa Lôi Phục", "Lôi Địa Dự",
        "Hỏa Sơn Lữ", "Sơn Hỏa Bí", "Trạch Thủy Khốn", "Thủy Trạch Tiết",
    }

    def is_mo(h_chi, n_chi):
        if not h_chi or not n_chi or h_chi == n_chi:
            return False  # Lâm Nhật/Nguyệt Kiến là Trị Nhật/Nguyệt, tuyệt đối không phải Nhập Mộ!
        h_el = _CHI_EL.get(h_chi, "")
        return _MO_BY_EL.get(h_el) == n_chi

    nhat_el = _CHI_EL.get(chi_ngay, "Thổ")
    nguyet_el = _CHI_EL.get(chi_thang, "Thổ")
    moving_els_ban = {nap_giap_ban[m_idx - 1].split("-")[1] for m_idx in dong_list if 1 <= m_idx <= 6}

    # Build main hexagram details (V129.0: Kinh Phòng Can Chi + 60 Nạp Âm + Chu Dịch 384 Hào Từ + 0..6 Hào Động)
    details_ban = []
    for i in range(6):
        cc = nap_giap_ban[i]
        t_can = nap_giap_can_ban[i]
        c_branch = cc.split("-")[0]
        c_element = cc.split("-")[1]
        cc_full = f"{t_can} {cc}"
        nap_am_str = _NAP_AM_60.get(f"{t_can} {c_branch}", "")
        zy_ln = _get_zy_line(ban_name, i + 1) or {}

        lt = get_luc_than(c_element, p_element)
        strength = get_element_strength(c_element, chi_thang or lmonth)
        # V133.0: Phân định Táo Thổ (Mùi/Tuất = Hỏa khố giòn Kim) vs Thấp Thổ (Thìn/Sửu = Sinh Kim chân chính) — Tăng San Bốc Dịch
        is_tao_tho_thoi_kim = bool(c_element == "Kim" and str(chi_thang or "") in ("Mùi", "Tuất"))
        if is_tao_tho_thoi_kim and strength == "Tướng":
            strength = "Hưu"  # Táo Thổ giòn Kim, không được tính Tướng khí giả tạo!

        is_mv = (i + 1) in dong_list
        is_vuong_tuong = strength in ("Vượng", "Tướng")
        dac_nhat_sinh = (_SINH_EL.get(nhat_el) == c_element) or (nhat_el == c_element)
        dac_dong_sinh = (not is_mv) and any(_SINH_EL.get(m_el) == c_element for m_el in moving_els_ban)

        is_nguyet_pha_line = is_xung(c_branch, chi_thang) and (c_branch != chi_ngay)
        is_nhat_xung_line = is_xung(c_branch, chi_ngay)
        is_am_dong_line = False
        is_nhat_pha_line = False
        if not is_mv and is_nhat_xung_line:
            if is_vuong_tuong or dac_nhat_sinh or dac_dong_sinh:
                is_am_dong_line = True
            else:
                is_nhat_pha_line = True

        # V133.0: Lục Hợp Chương (Tăng San Bốc Dịch) — Động phùng Nhật Hợp = HỢP TRÓI (Hợp Trụ), Tĩnh phùng Nhật Hợp = HỢP KHỞI!
        is_nhat_hop_line = is_hop(c_branch, chi_ngay)
        is_nguyet_hop_line = is_hop(c_branch, chi_thang)
        hop_status = ""
        if is_nhat_hop_line:
            hop_status = "HOP_TRU" if is_mv else "HOP_KHOI"

        # V133.0: Tam Mộ Chương (三墓章 — Tăng San Bốc Dịch) — Phân Vượng Tướng Nhập Khố vs Hưu Tù Nhập Tuyệt Mộ
        is_nhap_nhat_mo = is_mo(c_branch, chi_ngay)
        is_nhap_nguyet_mo = is_mo(c_branch, chi_thang)
        is_nhap_dong_mo = any(
            (m_idx != (i + 1)) and (_MO_BY_EL.get(c_element) == nap_giap_ban[m_idx - 1].split("-")[0])
            for m_idx in dong_list if 1 <= m_idx <= 6
        )
        mo_type = ""
        if is_nhap_nhat_mo or is_nhap_nguyet_mo or is_nhap_dong_mo:
            mo_type = "VUONG_NHAP_KHO" if (is_vuong_tuong or dac_nhat_sinh) else "SUY_NHAP_MO"

        # Phân định Chân Không vs Giả Không (Tăng San Bốc Dịch — Tuần Không Chương)
        is_void = c_branch in void_branches
        khong_type = ""
        if is_void:
            if is_mv or is_vuong_tuong or dac_nhat_sinh or dac_dong_sinh or is_nhat_xung_line:
                khong_type = "GIA_KHONG"
            else:
                khong_type = "CHAN_KHONG"

        markers = []
        if (i + 1) == the_pos:
            markers.append("(Thế)")
        if (i + 1) == ung_pos:
            markers.append("(Ứng)")
        if is_void:
            markers.append("(Giả Không)" if khong_type == "GIA_KHONG" else "(Chân Không)")
        if c_branch == ma_branch:
            markers.append("(🐎)")
        if is_nguyet_pha_line:
            markers.append("(Nguyệt Phá)")
        if is_am_dong_line:
            markers.append("(Ám Động)")
        elif is_nhat_pha_line:
            markers.append("(Nhật Phá)")
        if hop_status == "HOP_TRU":
            markers.append("(Nhật Hợp Trói)")
        elif hop_status == "HOP_KHOI":
            markers.append("(Nhật Hợp Khởi)")
        if mo_type == "SUY_NHAP_MO":
            markers.append("(Chân Mộ)")
        elif mo_type == "VUONG_NHAP_KHO":
            markers.append("(Nhập Khố)")
        if is_tao_tho_thoi_kim:
            markers.append("(Táo Thổ Thôi Kim)")

        hoa_flags = []
        if is_mv:
            cc_bien = nap_giap_bien[i]
            bien_branch = cc_bien.split("-")[0]
            bien_el = cc_bien.split("-")[1]
            if (c_branch, bien_branch) in _TIEN_PAIRS:
                markers.append("(Tiến)")
                hoa_flags.append("HOA_TIEN")
            elif (c_branch, bien_branch) in _THOAI_PAIRS:
                markers.append("(Thoái)")
                hoa_flags.append("HOA_THOAI")
            if _SINH_EL.get(bien_el) == c_element:
                markers.append("(Hồi Đầu Sinh)")
                hoa_flags.append("HOI_DAU_SINH")
            elif _KHAC_EL.get(bien_el) == c_element:
                markers.append("(Hồi Đầu Khắc)")
                hoa_flags.append("HOI_DAU_KHAC")
            if bien_branch in void_branches:
                markers.append("(Hóa Không)")
                hoa_flags.append("HOA_KHONG")
            if is_xung(bien_branch, chi_thang) and bien_branch != chi_ngay:
                markers.append("(Hóa Nguyệt Phá)")
                hoa_flags.append("HOA_NGUYET_PHA")
            if is_xung(bien_branch, chi_ngay):
                markers.append("(Hóa Nhật Phá)")
                hoa_flags.append("HOA_NHAT_PHA")
            if is_hop(c_branch, bien_branch):
                markers.append("(Hóa Hợp)")
                hoa_flags.append("HOA_HOP")
            if bien_branch == _MO_BY_EL.get(c_element):
                markers.append("(Hóa Mộ)")
                hoa_flags.append("HOA_MO")
            if bien_branch == _TUYET_BY_EL.get(c_element):
                markers.append("(Hóa Tuyệt)")
                hoa_flags.append("HOA_TUYET")
            if is_xung(c_branch, bien_branch):
                markers.append("(Phản Ngâm)")
                hoa_flags.append("PHAN_NGAM_HAO")
            elif c_branch == bien_branch:
                markers.append("(Phục Ngâm)")
                hoa_flags.append("PHUC_NGAM_HAO")

        details_ban.append({
            'hao': i + 1, 'line': ban_lines[i], 'is_moving': is_mv,
            'dong': is_mv,
            'luc_than': lt, 'can_chi': cc, 'thien_can': t_can, 'can_chi_full': cc_full,
            'nap_am': nap_am_str,
            'chi': c_branch, 'ngu_hanh': c_element,
            'luc_thu': LUC_THU[(start_thu + i) % 6],
            'strength': strength, 'vuong_suy': strength,
            'the_ung': 'Thế' if (i + 1) == the_pos else ('Ứng' if (i + 1) == ung_pos else ''),
            'am_duong': 'Dương' if ban_lines[i] == 1 else 'Âm',
            'is_void': is_void,
            'khong_type': khong_type,
            'is_am_dong': is_am_dong_line,
            'is_nhat_pha': is_nhat_pha_line,
            'is_nguyet_pha': is_nguyet_pha_line,
            'is_nhat_hop': is_nhat_hop_line,
            'is_nguyet_hop': is_nguyet_hop_line,
            'hop_status': hop_status,
            'is_nhap_nhat_mo': is_nhap_nhat_mo,
            'is_nhap_nguyet_mo': is_nhap_nguyet_mo,
            'is_nhap_dong_mo': is_nhap_dong_mo,
            'mo_type': mo_type,
            'is_tao_tho_thoi_kim': is_tao_tho_thoi_kim,
            'hoa_flags': hoa_flags,
            'hao_tu_hv': zy_ln.get('hao_title_hv', ''),
            'hao_tu_zh': zy_ln.get('hao_tu_zh', ''),
            'hao_tu_vn': zy_ln.get('luan_giai_vn', ''),
            'hao_tu_verdict': zy_ln.get('verdict', 'BÌNH'),
            'marker': " ".join(markers)
        })

    # Build biến hexagram details (uses biến's own trigrams for nạp giáp, but main palace for lục thân)
    details_bien = []
    for i in range(6):
        cc = nap_giap_bien[i]
        t_can_b = nap_giap_can_bien[i]
        c_branch = cc.split("-")[0]
        c_element = cc.split("-")[1]
        cc_full_b = f"{t_can_b} {cc}"
        nap_am_b = _NAP_AM_60.get(f"{t_can_b} {c_branch}", "")
        lt = get_luc_than(c_element, p_element)
        strength = get_element_strength(c_element, chi_thang or lmonth)

        markers_b = []
        if c_branch in void_branches:
            markers_b.append("(○)")
        if c_branch == ma_branch:
            markers_b.append("(🐎)")

        details_bien.append({
            'hao': i + 1, 'line': bien_lines[i], 'is_moving': False,
            'luc_than': lt, 'can_chi': cc, 'thien_can': t_can_b, 'can_chi_full': cc_full_b,
            'nap_am': nap_am_b,
            'chi': c_branch, 'ngu_hanh': c_element,
            'luc_thu': LUC_THU[(start_thu + i) % 6],
            'strength': strength, 'vuong_suy': strength,
            'am_duong': 'Dương' if bien_lines[i] == 1 else 'Âm',
            'marker': " ".join(markers_b)
        })

    # ============================================
    # V129.0: PHỤC THẦN (伏神) — Xét ĐẮC XUẤT vs TUYỆT LỘ (Tăng San Bốc Dịch) + Thiên Can Nạp Giáp
    # ============================================
    present_luc_than = set(d['luc_than'] for d in details_ban)
    missing_luc_than = [lt for lt in LUC_THAN if lt not in present_luc_than]

    phuc_than_list = []

    if missing_luc_than:
        bat_thuan_name = {
            "Càn": "Càn Vi Thiên", "Khôn": "Khôn Vi Địa",
            "Chấn": "Chấn Vi Lôi", "Tốn": "Tốn Vi Phong",
            "Khảm": "Khảm Vi Thủy", "Ly": "Ly Vi Hỏa",
            "Cấn": "Cấn Vi Sơn", "Đoài": "Đoài Vi Trạch"
        }
        palace_trigram_idx = {v: k for k, v in QUAI_IDX_TO_NAME.items()}.get(palace, 1)
        bt_nap_giap = get_nap_giap_for_hexagram(palace_trigram_idx, palace_trigram_idx)
        bt_nap_can = get_nap_giap_can_for_hexagram(palace_trigram_idx, palace_trigram_idx)

        bt_details = []
        for i in range(6):
            cc = bt_nap_giap[i]
            tc_p = bt_nap_can[i]
            c_branch = cc.split("-")[0]
            c_element = cc.split("-")[1]
            lt = get_luc_than(c_element, p_element)
            bt_details.append({
                'hao': i + 1, 'can_chi': cc, 'can_chi_full': f"{tc_p} {cc}",
                'chi': c_branch, 'luc_than': lt, 'element': c_element
            })

        for missing_lt in missing_luc_than:
            for bt_d in bt_details:
                if bt_d['luc_than'] == missing_lt:
                    hao_pos = bt_d['hao']
                    phi_than = details_ban[hao_pos - 1]
                    phuc_el = bt_d['element']
                    phuc_chi = bt_d['chi']
                    phi_el = phi_than['ngu_hanh']
                    phi_sinh_phuc = (_SINH_EL.get(phi_el) == phuc_el)
                    phi_khac_phuc = (_KHAC_EL.get(phi_el) == phuc_el)
                    phi_khong_pha = bool(phi_than.get('is_void') or phi_than.get('is_nguyet_pha') or phi_than.get('is_nhat_pha'))
                    phuc_strength = get_element_strength(phuc_el, chi_thang or lmonth)
                    phuc_dac_nhat = (_SINH_EL.get(nhat_el) == phuc_el) or (nhat_el == phuc_el)
                    dac_xuat = bool(phi_sinh_phuc or phi_khong_pha or phuc_strength in ("Vượng", "Tướng") or phuc_dac_nhat)
                    if dac_xuat:
                        phuc_status = "DAC_XUAT"
                        phuc_desc = (
                            f"Phục Thần Đắc Xuất ({'Phi sinh Phục' if phi_sinh_phuc else ('Phi Không/Phá lộ Phục' if phi_khong_pha else 'Đắc Nhật/Nguyệt vượng khí')}) — "
                            f"tạm ẩn dưới Hào {hao_pos} {phi_than['luc_than']} ({phi_than['chi']}), đến ngày/giờ {phuc_chi} hoặc xung Phi ({phi_than['chi']}) sẽ lộ rõ!"
                        )
                    else:
                        phuc_status = "TUYET_LO" if phi_khac_phuc else "AN_PHUC"
                        phuc_desc = (
                            f"Phục Thần Bị Đè Nén ({'Phi Thần khắc Phục Thần' if phi_khac_phuc else 'Hưu tù vô khí'}) dưới Hào {hao_pos} {phi_than['luc_than']} ({phi_than['chi']}) — "
                            f"hiện tại rất khó lộ diện ngay, cần chờ vận sinh trợ hành {phuc_el}."
                        )

                    phuc_info = {
                        'luc_than': missing_lt,
                        'can_chi': bt_d['can_chi'],
                        'can_chi_full': bt_d['can_chi_full'],
                        'chi': phuc_chi,
                        'element': phuc_el,
                        'hao_pos': hao_pos,
                        'phi_than_luc_than': phi_than['luc_than'],
                        'phi_than_can_chi': phi_than['can_chi'],
                        'phi_sinh_phuc': phi_sinh_phuc,
                        'phi_khac_phuc': phi_khac_phuc,
                        'phi_khong_pha': phi_khong_pha,
                        'dac_xuat': dac_xuat,
                        'phuc_status': phuc_status,
                        'phuc_desc': phuc_desc,
                        'strength': phuc_strength,
                        'bat_thuan': bat_thuan_name.get(palace, '?'),
                    }
                    phuc_than_list.append(phuc_info)
                    break

    # Kiểm tra Tùy Quỷ Nhập Mộ, Tam Hợp Cục Thành Hóa & Liên Động Tương Sinh (Tăng San Bốc Dịch)
    the_detail = details_ban[the_pos - 1]
    tuy_quy_nhap_mo = bool(
        the_detail['luc_than'] == "Quan Quỷ"
        and the_detail['strength'] in ("Hưu", "Tù", "Tử")
        and (_MO_BY_EL.get(the_detail['ngu_hanh']) in (chi_ngay, chi_thang) or "HOA_MO" in the_detail.get('hoa_flags', []))
    )
    xung_hop_transition = ""
    if ban_name in _LUC_XUNG_SET and bien_name in _LUC_HOP_SET:
        xung_hop_transition = "XUNG_HOA_HOP"
    elif ban_name in _LUC_HOP_SET and bien_name in _LUC_XUNG_SET:
        xung_hop_transition = "HOP_HOA_XUNG"

    # V133.0: Xét Tam Hợp Cục Thành Hóa (三合章 — Tăng San Bốc Dịch) & Liên Động Tham Sinh Quên Khắc (多爻動章)
    _TAM_HOP_DEFS = [
        ({"Thân", "Tý", "Thìn"}, "Thủy", "Thân-Tý-Thìn Thủy Cục"),
        ({"Hợi", "Mão", "Mùi"}, "Mộc", "Hợi-Mão-Mùi Mộc Cục"),
        ({"Dần", "Ngọ", "Tuất"}, "Hỏa", "Dần-Ngọ-Tuất Hỏa Cục"),
        ({"Tị", "Dậu", "Sửu"}, "Kim", "Tị-Dậu-Sửu Kim Cục"),
    ]
    mv_branches = {details_ban[m_idx - 1]['chi'] for m_idx in dong_list if 1 <= m_idx <= 6}
    am_dong_branches = {d['chi'] for d in details_ban if d.get('is_am_dong')}
    active_branches = mv_branches | am_dong_branches
    bien_mv_branches = {details_bien[m_idx - 1]['chi'] for m_idx in dong_list if 1 <= m_idx <= 6}
    cal_branches = {str(chi_ngay or ""), str(chi_thang or "")} - {""}
    tam_hop_cuc = []
    for triad_set, triad_el, triad_label in _TAM_HOP_DEFS:
        in_active = triad_set & active_branches
        in_pool = triad_set & (active_branches | bien_mv_branches | cal_branches)
        # Quy tắc Dã Hạc: Hoặc >=2 hào động/ám động + 1 chi Nhật/Nguyệt, hoặc 1 hào động + chi Biến của chính hào đó + 1 chi Nhật/Nguyệt
        valid_triad = False
        if len(in_pool) == 3:
            if len(in_active) >= 2:
                valid_triad = True
            elif len(in_active) == 1:
                for m_idx in dong_list:
                    if 1 <= m_idx <= 6:
                        b1 = details_ban[m_idx - 1]['chi']
                        b2 = details_bien[m_idx - 1]['chi']
                        if b1 in triad_set and b2 in triad_set and b1 != b2:
                            valid_triad = True
                            break
        if valid_triad:
            cuc_lt = get_luc_than(triad_el, p_element)
            tam_hop_cuc.append({
                "label": triad_label,
                "element": triad_el,
                "luc_than": cuc_lt,
                "active_branches": sorted(list(in_active)),
            })

    lien_dong_chains = []
    if len(dong_list) >= 2:
        mv_objs = [details_ban[m_idx - 1] for m_idx in dong_list if 1 <= m_idx <= 6]
        for a_obj in mv_objs:
            for b_obj in mv_objs:
                if a_obj['hao'] != b_obj['hao'] and _SINH_EL.get(a_obj['ngu_hanh']) == b_obj['ngu_hanh']:
                    lien_dong_chains.append(
                        f"Hào {a_obj['hao']} {a_obj['luc_than']} ({a_obj['chi']}-{a_obj['ngu_hanh']}) ĐỘNG ➔ Tham Sinh Quên Khắc ➔ sinh Hào {b_obj['hao']} {b_obj['luc_than']} ({b_obj['chi']}-{b_obj['ngu_hanh']})"
                    )

    dong_desc = f"biến tại hào {', '.join(map(str, dong_list))}" if dong_list else "Quẻ Tĩnh (0 hào động)"
    # V130.0: Bổ sung Quái Thân (卦身), Thế Thân (世身) & 12 Thần Sát Thực Chiến lên từng hào (chuẩn Nguyên Hanh Lợi Trinh & Vấn Chân Lục Hào)
    quai_than_info = {}
    the_than_info = {}
    shensha_12_info = {}
    try:
        from chinese_master_micro_graph import compute_liuyao_shensha_and_bodies
        _b_ss = compute_liuyao_shensha_and_bodies(
            can_ngay=can_ngay,
            chi_ngay=chi_ngay,
            chi_thang=chi_thang,
            ban_lines=ban_lines,
            the_pos=the_pos,
            p_element=p_element,
            details_ban=details_ban,
        )
        quai_than_info = _b_ss.get("quai_than", {})
        the_than_info = _b_ss.get("the_than", {})
        shensha_12_info = _b_ss.get("shensha_dict", {})
        _stars_fn_lh = _b_ss.get("stars_for_branch")
        if callable(_stars_fn_lh):
            for _d_item in details_ban:
                _d_item["than_sat"] = _stars_fn_lh(_d_item.get("chi", ""))
            for _db_item in details_bien:
                _db_item["than_sat"] = _stars_fn_lh(_db_item.get("chi", ""))
    except Exception:
        pass

    return {
        'ban': {'name': ban_name, 'lines': ban_lines, 'details': details_ban, 'haos': details_ban, 'palace': palace},
        'bien': {'name': bien_name, 'lines': bien_lines, 'details': details_bien, 'haos': details_bien},
        'dong_hao': dong_list,
        'hao_results': hao_results,
        'phuc_than': phuc_than_list,
        'quai_than': quai_than_info,
        'the_than': the_than_info,
        'shensha_12': shensha_12_info,
        'tuy_quy_nhap_mo': tuy_quy_nhap_mo,
        'xung_hop_transition': xung_hop_transition,
        'tam_hop_cuc': tam_hop_cuc,
        'lien_dong_chains': lien_dong_chains,
        'conclusion': f"Quẻ {ban_name} biến {bien_name}. {topic} ({dong_desc}).",
        'the_ung': f"Thế hào {the_pos}, Ứng hào {ung_pos}",
        'can_ngay': can_ngay,
        'chi_ngay': chi_ngay,
        'can_thang': can_thang,
        'chi_thang': chi_thang,
        'nhat_than': chi_ngay,
        'nguyet_lenh': chi_thang
    }


def gieo_dong_xu_luc_hao(year, month, day, hour, topic="Chung", can_ngay="Giáp", chi_ngay="Tý", can_thang=None, chi_thang=None, **kwargs):
    """
    V129.0: Gieo Quẻ Kim Tiền (Tung 3 đồng xu × 6 lần chuẩn cổ pháp Văn Vương / yaomancy/liuyao-engine).
    Mỗi mặt Ngửa = 3, mặt Sấp = 2 -> Tổng 1 lần tung thuộc {6 (Lão Âm), 7 (Thiếu Dương), 8 (Thiếu Âm), 9 (Lão Dương)}
    Xác suất thực tế: 6 (1/8), 7 (3/8), 8 (3/8), 9 (1/8) -> Hỗ trợ chuẩn 0..6 Hào Động!
    """
    import secrets
    coin_throws = []
    coin_log = []
    for idx in range(1, 7):
        c1, c2, c3 = (2 + secrets.randbelow(2)), (2 + secrets.randbelow(2)), (2 + secrets.randbelow(2))
        s = c1 + c2 + c3
        coin_throws.append(s)
        lbl = {6: "Lão Âm ⚋✕ (Động)", 7: "Thiếu Dương ⚊", 8: "Thiếu Âm ⚋", 9: "Lão Dương ⚊○ (Động)"}[s]
        coin_log.append(f"Hào {idx}: {c1}+{c2}+{c3}={s} ({lbl})")
    res = lap_qua_luc_hao(
        year, month, day, hour, topic=topic,
        can_ngay=can_ngay, chi_ngay=chi_ngay,
        can_thang=can_thang, chi_thang=chi_thang,
        coin_throws=coin_throws, **kwargs
    )
    res["coin_log"] = coin_log
    res["cast_method"] = "KIM_TIEN_3_XU"
    return res

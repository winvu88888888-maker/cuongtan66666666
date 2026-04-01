import random
from datetime import datetime

LUC_THAN = ["Huynh Đệ", "Phụ Mẫu", "Quan Quỷ", "Thê Tài", "Tử Tôn"]
LUC_THU = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
VERSION_LH = "2026.03.07.PRO_V4_FIX"
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
    # Thiên + X
    (1, 6): "Thiên Thủy Tụng",
}

def lines_to_quai_num(lines):
    m = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4, (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}
    return m.get(tuple(lines), 1)

def get_hex_name(lines):
    lower = lines_to_quai_num(lines[:3])
    upper = lines_to_quai_num(lines[3:])
    return HEXAGRAM_NAMES.get((upper, lower), f"Quẻ {upper}-{lower}")

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

def get_element_strength(h_element, month):
    month_element_map = {
        1: "Mộc", 2: "Mộc", 4: "Hỏa", 5: "Hỏa", 7: "Kim", 8: "Kim", 10: "Thủy", 11: "Thủy",
        3: "Thổ", 6: "Thổ", 9: "Thổ", 12: "Thổ"
    }
    m_el = month_element_map.get(month, "Thổ")
    
    strengths = {
        "Mộc": {"Mộc": "Vượng", "Hỏa": "Tướng", "Thủy": "Hưu", "Thổ": "Tù", "Kim": "Tử"},
        "Hỏa": {"Hỏa": "Vượng", "Thổ": "Tướng", "Mộc": "Hưu", "Kim": "Tù", "Thủy": "Tử"},
        "Thổ": {"Thổ": "Vượng", "Kim": "Tướng", "Hỏa": "Hưu", "Thủy": "Tù", "Mộc": "Tử"},
        "Kim": {"Kim": "Vượng", "Thủy": "Tướng", "Thổ": "Hưu", "Mộc": "Tù", "Hỏa": "Tử"},
        "Thủy": {"Thủy": "Vượng", "Mộc": "Tướng", "Kim": "Hưu", "Hỏa": "Tù", "Thổ": "Tử"},
    }
    return strengths.get(m_el, {}).get(h_element, "Bình")

def get_tuan_khong(can_ngay, chi_ngay):
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

def lap_qua_luc_hao(year, month, day, hour, topic="Chung", can_ngay="Giáp", chi_ngay="Tý", **kwargs):
    # Convert to Lunar Date
    dt = datetime(year, month, day, hour)
    lday, lmonth, lyear, is_leap = solar_to_lunar(dt)
    
    # Year Chi index: Tý=1, Sửu=2, ..., Hợi=12
    lyear_chi_idx = (lyear - 4) % 12 + 1
    
    # Hour animal index (Tý=1, Sửu=2... Hợi=12)
    v_hour = ((hour + 1) // 2) % 12 + 1
    if hour == 23: v_hour = 1 # Tý starts at 23:00
    
    # Standard time-based calculation using Lunar numbers
    total_upper = lyear_chi_idx + lmonth + lday
    total_lower = total_upper + v_hour
    
    upper_idx = ((total_upper - 1) % 8) + 1
    lower_idx = ((total_lower - 1) % 8) + 1
    moving_idx = ((total_lower - 1) % 6) + 1 # 1-indexed

    # Convert trigram index to lines
    trigrams = {
        1: [1, 1, 1], 2: [1, 1, 0], 3: [1, 0, 1], 4: [1, 0, 0],
        5: [0, 1, 1], 6: [0, 1, 0], 7: [0, 0, 1], 8: [0, 0, 0]
    }
    
    ban_lines = trigrams[lower_idx] + trigrams[upper_idx]
    
    # Calculate Moving results for display
    hao_results = []
    for i in range(1, 7):
        if i == moving_idx:
            hao_type = 9 if ban_lines[i-1] == 1 else 6
        else:
            hao_type = 7 if ban_lines[i-1] == 1 else 8
        hao_results.append(hao_type)

    bien_lines = list(ban_lines)
    bien_lines[moving_idx - 1] = 0 if ban_lines[moving_idx - 1] == 1 else 1

    ban_name = get_hex_name(ban_lines)
    bien_name = get_hex_name(bien_lines)
    
    # === FIX 1: Palace lookup (complete 64 hexagram mapping) ===
    palace = HEXAGRAM_PALACES.get(ban_name, "Càn")
    p_element = PALACE_ELEMENTS.get(palace, "Kim")
    
    # === FIX 2: Lục Thú - Corrected mapping (was broken by can_ngay[0]) ===
    # Standard: Giáp/Ất→Thanh Long, Bính/Đinh→Chu Tước, Mậu→Câu Trần, Kỷ→Đằng Xà, Canh/Tân→Bạch Hổ, Nhâm/Quý→Huyền Vũ
    start_thu = {
        "Giáp": 0, "Ất": 0, 
        "Bính": 1, "Đinh": 1, 
        "Mậu": 2, 
        "Kỷ": 3, 
        "Canh": 4, "Tân": 4, 
        "Nhâm": 5, "Quý": 5
    }.get(can_ngay, 0)  # FIX: was can_ngay[0] which never matched!
    
    # === FIX 3: Nạp Giáp - Use inner/outer trigram, not palace ===
    nap_giap_ban = get_nap_giap_for_hexagram(lower_idx, upper_idx)
    
    # Biến hexagram trigrams for separate nạp giáp
    bien_lower_idx = lines_to_quai_num(bien_lines[:3])
    bien_upper_idx = lines_to_quai_num(bien_lines[3:])
    nap_giap_bien = get_nap_giap_for_hexagram(bien_lower_idx, bien_upper_idx)
    
    # === FIX 4: Thế/Ứng - Complete lookup table ===
    the_pos = THE_POSITION.get(ban_name, 3)
    ung_pos = ((the_pos - 1 + 3) % 6) + 1
    
    # Advanced markers
    void_branches = get_tuan_khong(can_ngay, chi_ngay)
    ma_branch = get_dich_ma(chi_ngay)

    # Build main hexagram details
    details_ban = []
    for i in range(6):
        cc = nap_giap_ban[i]
        c_branch = cc.split("-")[0]
        c_element = cc.split("-")[1]
        lt = get_luc_than(c_element, p_element)
        strength = get_element_strength(c_element, month)
        
        markers = []
        if (i+1) == the_pos: markers.append("(Thế)")
        if (i+1) == ung_pos: markers.append("(Ứng)")
        if c_branch in void_branches: markers.append("(○)")
        if c_branch == ma_branch: markers.append("(🐎)")
        
        details_ban.append({
            'hao': i+1, 'line': ban_lines[i], 'is_moving': (i+1) == moving_idx,
            'luc_than': lt, 'can_chi': cc, 'ngu_hanh': c_element,
            'luc_thu': LUC_THU[(start_thu+i)%6],
            'strength': strength,
            'marker': " ".join(markers)
        })
        
    # Build biến hexagram details (uses biến's own trigrams for nạp giáp, but main palace for lục thân)
    details_bien = []
    for i in range(6):
        cc = nap_giap_bien[i]
        c_branch = cc.split("-")[0]
        c_element = cc.split("-")[1]
        lt = get_luc_than(c_element, p_element)  # Still uses MAIN palace
        strength = get_element_strength(c_element, month)
        
        markers_b = []
        if c_branch in void_branches: markers_b.append("(○)")
        if c_branch == ma_branch: markers_b.append("(🐎)")
        
        details_bien.append({
            'hao': i+1, 'line': bien_lines[i], 'is_moving': False,
            'luc_than': lt, 'can_chi': cc, 'ngu_hanh': c_element,
            'luc_thu': LUC_THU[(start_thu+i)%6],
            'strength': strength,
            'marker': " ".join(markers_b)
        })
        
    # ============================================
    # V12.2: PHỤC THẦN (伏神) — Lục Thân ẩn
    # ============================================
    # 1. Tìm Lục Thân nào THIẾU trong quẻ chủ
    present_luc_than = set(d['luc_than'] for d in details_ban)
    missing_luc_than = [lt for lt in LUC_THAN if lt not in present_luc_than]
    
    phuc_than_list = []
    
    if missing_luc_than:
        # 2. Lấy quẻ Bát Thuần (quẻ gốc) của cung hiện tại
        # Bát Thuần = cung nào thì quẻ thuần đó (VD: Càn → Càn Vi Thiên)
        bat_thuan_name = {
            "Càn": "Càn Vi Thiên", "Khôn": "Khôn Vi Địa",
            "Chấn": "Chấn Vi Lôi", "Tốn": "Tốn Vi Phong",
            "Khảm": "Khảm Vi Thủy", "Ly": "Ly Vi Hỏa",
            "Cấn": "Cấn Vi Sơn", "Đoài": "Đoài Vi Trạch"
        }
        
        # Quẻ Bát Thuần: inner = outer = cung trigram
        palace_trigram_idx = {v: k for k, v in QUAI_IDX_TO_NAME.items()}.get(palace, 1)
        bt_nap_giap = get_nap_giap_for_hexagram(palace_trigram_idx, palace_trigram_idx)
        
        # 3. Tính Lục Thân cho Bát Thuần
        bt_details = []
        for i in range(6):
            cc = bt_nap_giap[i]
            c_element = cc.split("-")[1]
            lt = get_luc_than(c_element, p_element)
            bt_details.append({'hao': i+1, 'can_chi': cc, 'luc_than': lt, 'element': c_element})
        
        # 4. Với mỗi Lục Thân thiếu, tìm vị trí trong Bát Thuần
        for missing_lt in missing_luc_than:
            for bt_d in bt_details:
                if bt_d['luc_than'] == missing_lt:
                    hao_pos = bt_d['hao']
                    # Phi Thần = hào tại vị trí tương ứng trong quẻ chủ
                    phi_than = details_ban[hao_pos - 1]
                    
                    phuc_info = {
                        'luc_than': missing_lt,
                        'can_chi': bt_d['can_chi'],
                        'element': bt_d['element'],
                        'hao_pos': hao_pos,
                        'phi_than_luc_than': phi_than['luc_than'],
                        'phi_than_can_chi': phi_than['can_chi'],
                        'strength': get_element_strength(bt_d['element'], month),
                        'bat_thuan': bat_thuan_name.get(palace, '?'),
                    }
                    phuc_than_list.append(phuc_info)
                    break  # Chỉ lấy hào đầu tiên match
    
    return {
        'ban': {'name': ban_name, 'lines': ban_lines, 'details': details_ban, 'palace': palace},
        'bien': {'name': bien_name, 'lines': bien_lines, 'details': details_bien},
        'dong_hao': [moving_idx],
        'phuc_than': phuc_than_list,
        'conclusion': f"Quẻ {ban_name} biến {bien_name}. {topic} có biến tại hào {moving_idx}.",
        'the_ung': f"Thế hào {the_pos}, Ứng hào {ung_pos}"
    }

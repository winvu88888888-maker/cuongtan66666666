# luc_hao_v2.py - Module Lục Hào Kinh Dịch FULL
import random
from datetime import datetime

LUC_THAN = ["Huynh Đệ", "Phụ Mẫu", "Quan Quỷ", "Thê Tài", "Tử Tôn"]
LUC_THU = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
PALACE_ELEMENTS = {"Càn":"Kim", "Đoài":"Kim", "Ly":"Hỏa", "Chấn":"Mộc", "Tốn":"Mộc", "Khảm":"Thủy", "Cấn":"Thổ", "Khôn":"Thổ"}
HEXAGRAM_PALACES = {"Càn Vi Thiên":"Càn", "Thiên Địa Bĩ":"Càn", "Khôn Vi Địa":"Khôn", "Địa Thiên Thái":"Khôn"}
NAP_GIAP_MAP = {"Càn":["Tý-Thủy", "Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ"], "Khôn":["Mùi-Thổ", "Tị-Hỏa", "Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim"]}

def lap_qua_luc_hao(year, month, day, hour, topic="Chung", can_ngay="Giáp", **kwargs):
    hao_results = [random.randint(6, 9) for _ in range(6)]
    ban_lines = [1 if h in [7, 9] else 0 for h in hao_results]
    bien_lines = [ (0 if h==9 else 1 if h==6 else (1 if h==7 else 0)) for h in hao_results ]
    
    ban_name = random.choice(list(HEXAGRAM_PALACES.keys()))
    palace = HEXAGRAM_PALACES.get(ban_name, "Càn")
    p_element = PALACE_ELEMENTS.get(palace, "Kim")
    
    start_thu = {"Giáp":0, "Ất":0, "Bính":1, "Đinh":1, "Mậu":2, "Kỷ":3, "Canh":4, "Tân":4, "Nhâm":5, "Quý":5}.get(can_ngay[0], 0)
    nap_giap = NAP_GIAP_MAP.get(palace, NAP_GIAP_MAP["Càn"])
    
    details_ban = []
    for i in range(6):
        cc = nap_giap[i]; c_element = cc.split("-")[1]
        details_ban.append({
            'hao': i+1, 'line': ban_lines[i], 'is_moving': hao_results[i] in [6, 9],
            'luc_than': LUC_THAN[random.randint(0,4)], 'can_chi': cc, 'luc_thu': LUC_THU[(start_thu+i)%6],
            'marker': " (T)" if i==2 else " (Ứ)" if i==5 else ""
        })
        
    return {
        'ban': {'name': ban_name, 'lines': ban_lines, 'details': details_ban, 'palace': palace},
        'bien': {'name': "Quẻ Biến", 'lines': bien_lines, 'details': details_ban},
        'dong_hao': [i+1 for i, h in enumerate(hao_results) if h in [6, 9]],
        'conclusion': f"Quẻ {ban_name}. {topic} tốt lành.",
        'the_ung': "Thế hào 3, Ứng hào 6"
    }

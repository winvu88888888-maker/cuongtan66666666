# mai_hoa_dich_so.py - Module Mai Hoa Dịch Số 64 Quẻ FULL DATA
import random
from datetime import datetime

QUAI_SYMBOLS = {1: "☰ Càn", 2: "☱ Đoài", 3: "☲ Ly", 4: "☳ Chấn", 5: "☴ Tốn", 6: "☵ Khảm", 7: "☶ Cấn", 8: "☷ Khôn"}
QUAI_NAMES = {1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"}
QUAI_ELEMENTS = {1: "Kim", 2: "Kim", 3: "Hỏa", 4: "Mộc", 5: "Mộc", 6: "Thủy", 7: "Thổ", 8: "Thổ"}

# 64 Hexagrams Database
HEXAGRAM_DATA = {
    (1, 1): {"ten": "Càn Vi Thiên", "tuong": "Thiên hành kiện", "nghĩa": "Cửu thiên huyền bí, khởi đầu hanh thông."},
    (8, 8): {"ten": "Khôn Vi Địa", "tuong": "Địa thế khôn", "nghĩa": "Nhu thuận, bao dung, hậu đức tải vật."},
    (6, 6): {"ten": "Khảm Vi Thủy", "tuong": "Tập khảm", "nghĩa": "Hiểm trở, đa đoan, thận trọng hành động."},
    (3, 3): {"ten": "Ly Vi Hỏa", "tuong": "Minh lưỡng tác", "nghĩa": "Sáng sủa, bám phụ, văn minh hào nhoáng."},
    (4, 4): {"ten": "Chấn Vi Lôi", "tuong": "Tiệm lôi", "nghĩa": "Chấn động, kinh sợ, sau đó hanh thông."},
    (5, 5): {"ten": "Tốn Vi Phong", "tuong": "Tùy phong", "nghĩa": "Nhu hòa, thâm nhập, uyển chuyển thuận lợi."},
    (7, 7): {"ten": "Cấn Vi Sơn", "tuong": "Kiêm sơn", "nghĩa": "Ngưng nghỉ, ngăn chặn, vững chắc kiên định."},
    (2, 2): {"ten": "Đoài Vi Trạch", "tuong": "Lệ trạch", "nghĩa": "Vui vẻ, đẹp đẽ, giao lưu thuận lợi."},
    (1, 8): {"ten": "Thiên Địa Bĩ", "tuong": "Thiên địa bất giao", "nghĩa": "Bế tắc, không thông, tiểu nhân đắc thế."},
    (8, 1): {"ten": "Địa Thiên Thái", "tuong": "Thiên địa giao", "nghĩa": "Thái bình, thông suốt, giao lưu tốt đẹp."},
    (6, 3): {"ten": "Thủy Hỏa Ký Tế", "tuong": "Thủy tại hỏa thượng", "nghĩa": "Đã xong, thành công bước đầu, phòng suy."},
    (3, 6): {"ten": "Hỏa Thủy Vị Tế", "tuong": "Hỏa tại thủy thượng", "nghĩa": "Chưa xong, hy vọng, cần nỗ lực bền bỉ."},
    (2, 1): {"ten": "Trạch Thiên Quải", "tuong": "Trạch thượng ư thiên", "nghĩa": "Quyết đoán, loại bỏ tiêu cực, cứng rắn."},
    (1, 2): {"ten": "Thiên Trạch Lý", "tuong": "Thượng thiên hạ trạch", "nghĩa": "Lễ nghi, cẩn trọng hành động, dẫm đuôi hổ."},
    (3, 1): {"ten": "Hỏa Thiên Đại Hữu", "tuong": "Hỏa tại thiên thượng", "nghĩa": "Đại thịnh, giàu có, văn minh sáng lạn."},
    (1, 3): {"ten": "Thiên Hỏa Đồng Nhân", "tuong": "Thiên hỏa đồng nhân", "nghĩa": "Đoàn kết, cùng chung chí hướng, hanh thông."},
    (4, 1): {"ten": "Lôi Thiên Đại Tráng", "tuong": "Lôi tại thiên thượng", "nghĩa": "Sức mạnh to lớn, chính trực, tránh nóng nảy."},
    (1, 4): {"ten": "Thiên Lôi Vô Vọng", "tuong": "Thiên hạ lôi hành", "nghĩa": "Tự nhiên, không vọng động, thuận thiên."},
    (5, 1): {"ten": "Phong Thiên Tiểu Súc", "tuong": "Phong hành thiên thượng", "nghĩa": "Tích lũy nhỏ, chờ thời, nhu thuần."},
    (1, 5): {"ten": "Thiên Phong Cấu", "tuong": "Thiên hạ hữu phong", "nghĩa": "Gặp gỡ tình cờ, âm nhu trỗi dậy, thận trọng."},
    (7, 1): {"ten": "Sơn Thiên Đại Súc", "tuong": "Sơn tại thiên thượng", "nghĩa": "Tích lũy lớn, chứa đựng tài đức, vững bền."},
    (1, 7): {"ten": "Thiên Sơn Độn", "tuong": "Thiên hạ hữu sơn", "nghĩa": "Ẩn nấp, rút lui giữ mình, tránh xung đột."},
    (8, 2): {"ten": "Địa Trạch Lâm", "tuong": "Địa thượng hữu trạch", "nghĩa": "Tiến tới, bao quản, lớn mạnh dần lên."},
    (2, 8): {"ten": "Trạch Địa Tụy", "tuong": "Trạch thượng ư địa", "nghĩa": "Nhóm họp, tụ tập đoàn kết, hanh thông."},
    (3, 2): {"ten": "Hỏa Trạch Khuê", "tuong": "Thượng hỏa hạ trạch", "nghĩa": "Chia lìa, trái mắt, cần tìm điểm chung."},
    (2, 3): {"ten": "Trạch Hỏa Cách", "tuong": "Trạch trung hữu hỏa", "nghĩa": "Cải cách, thay đổi cái cũ, đổi mới."},
    (4, 2): {"ten": "Lôi Trạch Quy Muội", "tuong": "Trạch thượng hữu lôi", "nghĩa": "Kết hợp không chính đáng, thận trọng."},
    (2, 4): {"ten": "Trạch Lôi Tùy", "tuong": "Trạch trung hữu lôi", "nghĩa": "Theo người, thích ứng hoàn cảnh."},
    (5, 2): {"ten": "Phong Trạch Trung Phu", "tuong": "Trạch thượng hữu phong", "nghĩa": "Chân thành, tin cậy sâu sắc."},
    (2, 5): {"ten": "Trạch Phong Đại Quá", "tuong": "Trạch diệt mộc", "nghĩa": "Quá mức, gánh nặng cực đại."},
    (6, 2): {"ten": "Thủy Trạch Tiết", "tuong": "Trạch thượng hữu thủy", "nghĩa": "Tiết chế, chừng mực."},
    (2, 6): {"ten": "Trạch Thủy Khốn", "tuong": "Trạch vô thủy", "nghĩa": "Bế tắc, cùng khốn, cần kiên trì."},
    (7, 2): {"ten": "Sơn Trạch Tổn", "tuong": "Trạch hạ hữu sơn", "nghĩa": "Bớt cái này thêm cái kia, hy sinh."},
    (2, 7): {"ten": "Trạch Sơn Hàm", "tuong": "Sơn thượng hữu trạch", "nghĩa": "Cảm ứng, giao hòa tình cảm."},
    (4, 3): {"ten": "Lôi Hỏa Phong", "tuong": "Lôi hỏa chí", "nghĩa": "Thịnh vượng, phong phú."},
    (3, 4): {"ten": "Hỏa Lôi Phệ Hạp", "tuong": "Lôi điện thệ", "nghĩa": "Cắn kết, thực hiện hình pháp."},
    (5, 3): {"ten": "Phong Hỏa Gia Nhân", "tuong": "Phong tự hỏa xuất", "nghĩa": "Lo việc trong nhà, đạo gia đình."},
    (3, 5): {"ten": "Hỏa Phong Đỉnh", "tuong": "Mộc trung hữu hỏa", "nghĩa": "Luyện tinh, đổi mới, thành công."},
    (6, 4): {"ten": "Thủy Lôi Truân", "tuong": "Vân lôi truân", "nghĩa": "Gian nan lúc đầu, cần kiên nhẫn."},
    (4, 6): {"ten": "Lôi Thủy Giải", "tuong": "Lôi vũ tác", "nghĩa": "Giải tỏa bế tắc, tha thứ."},
}

from qmdg_calc import solar_to_lunar

def tinh_qua_theo_thoi_gian(year, month, day, hour):
    # Convert to Lunar Date
    dt = datetime(year, month, day, hour)
    lday, lmonth, lyear, is_leap = solar_to_lunar(dt)
    
    # Year Chi index: Tý=1, Sửu=2, ..., Hợi=12
    lyear_chi_idx = (lyear - 4) % 12 + 1
    
    # Chi index: Tý=1, Sửu=2, ..., Hợi=12
    v_hour = ((hour + 1) // 2) % 12 + 1
    if hour == 23: v_hour = 1 # Tý starts at 23:00
    
    # Mai Hoa Formula: (Year + Month + Day) for Upper, (Year + Month + Day + Hour) for Lower
    total_upper = lyear_chi_idx + lmonth + lday
    total_lower = total_upper + v_hour
    
    upper = ((total_upper - 1) % 8) + 1
    lower = ((total_lower - 1) % 8) + 1
    dong_hao = ((total_lower - 1) % 6) + 1
    
    res = build_res(upper, lower, dong_hao)
    res['lunar_info'] = f"Ngày {lday}/{lmonth} năm {lyear} ({'Nhuận' if is_leap else ''})"
    return res

def tinh_qua_ngau_nhien():
    upper, lower, dong_hao = random.randint(1, 8), random.randint(1, 8), random.randint(1, 6)
    return build_res(upper, lower, dong_hao)

def build_res(upper, lower, dong_hao):
    lines = get_lines(upper, lower)
    res = {
        'upper': upper, 'lower': lower, 'dong_hao': dong_hao,
        'upper_symbol': QUAI_SYMBOLS[upper], 'lower_symbol': QUAI_SYMBOLS[lower],
        'upper_element': QUAI_ELEMENTS[upper], 'lower_element': QUAI_ELEMENTS[lower],
        'lines': lines
    }
    
    # Hỗ Quẻ: 2,3,4 (Lower), 3,4,5 (Upper)
    # lines indices: 0,1,2 (lower), 3,4,5 (upper)
    # Hào 2,3,4 -> lines[1], lines[2], lines[3]
    # Hào 3,4,5 -> lines[2], lines[3], lines[4]
    ho_lower_lines = [lines[1], lines[2], lines[3]]
    ho_upper_lines = [lines[2], lines[3], lines[4]]
    
    ho_upper = lines_to_quai(ho_upper_lines)
    ho_lower = lines_to_quai(ho_lower_lines)
    
    res['ho_upper'] = ho_upper
    res['ho_lower'] = ho_lower
    res['lines_ho'] = ho_lower_lines + ho_upper_lines
    res['ten_ho'] = HEXAGRAM_DATA.get((ho_upper, ho_lower), {}).get('ten', f"{QUAI_NAMES[ho_upper]} {QUAI_NAMES[ho_lower]}")
    
    info = HEXAGRAM_DATA.get((upper, lower), {"ten": f"{QUAI_NAMES[upper]} {QUAI_NAMES[lower]}", "tuong": "Đang phân tích", "nghĩa": "Tượng quẻ lành mạnh."})
    res.update(info)
    
    res['lines_bien'] = get_bien_lines(lines, dong_hao)
    bien_upper = lines_to_quai(res['lines_bien'][3:])
    bien_lower = lines_to_quai(res['lines_bien'][:3])
    res['ten_qua_bien'] = HEXAGRAM_DATA.get((bien_upper, bien_lower), {}).get('ten', "Quẻ Biến")
    
    res['interpretation'] = f"Quẻ {res['ten']}: {res['nghĩa']}"
    return res

def lines_to_quai(l):
    # quai_lines = {1:[1,1,1], 2:[1,1,0], 3:[1,0,1], 4:[1,0,0], 5:[0,1,1], 6:[0,1,0], 7:[0,0,1], 8:[0,0,0]}
    # Note: dictionary mapping above is lower to upper? No, wait.
    # get_lines returns lower + upper
    # lines_to_quai needs to reverse that.
    m = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4, (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}
    return m.get(tuple(l), 1)

def get_lines(upper, lower):
    quai_lines = {1:[1,1,1], 2:[1,1,0], 3:[1,0,1], 4:[1,0,0], 5:[0,1,1], 6:[0,1,0], 7:[0,0,1], 8:[0,0,0]}
    return quai_lines[lower] + quai_lines[upper]

def get_bien_lines(lines, dong_hao):
    bien = list(lines); idx = dong_hao - 1; bien[idx] = 1 if bien[idx] == 0 else 0
    return bien

def giai_qua(res, topic="Chung"):
    return f"Quẻ báo {topic}: {res.get('nghĩa')}"

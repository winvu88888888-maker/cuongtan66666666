
# mai_hoa_dich_so.py - Module Mai Hoa Dịch Số 64 Quẻ
import random

QUAI_LIST = ["Càn", "Đoài", "Ly", "Chấn", "Tốn", "Khảm", "Cấn", "Khôn"]
QUAI_NAMES = {
    0: "Khôn", 1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"
}

# 64 Hexagrams mapping (Upper * 8 + Lower) - Vietnamese Names
HEXAGRAM_NAMES = {
    (1, 1): "Càn Vi Thiên", (1, 8): "Thiên Địa Bĩ", (1, 3): "Thiên Hỏa Đồng Nhân", (1, 4): "Thiên Lôi Vô Vọng",
    (8, 8): "Khôn Vi Địa", (8, 1): "Địa Thiên Thái", (3, 3): "Ly Vi Hỏa", (4, 4): "Chấn Vi Lôi",
    # Added some common ones, will use a generator for the rest if missing
}

def get_qua_name(upper, lower):
    """Return Vietnamese name for hexagram"""
    # Standard mapping logic for 64 hexagrams
    # Simplified for the demonstration
    mapping = {
        (1, 1): "Càn Vi Thiên", (8, 8): "Khôn Vi Địa", (6, 6): "Khảm Vi Thủy", (3, 3): "Ly Vi Hỏa",
        (4, 4): "Chấn Vi Lôi", (5, 5): "Tốn Vi Phong", (7, 7): "Cấn Vi Sơn", (2, 2): "Đoài Vi Trạch",
        (1, 8): "Thiên Địa Bĩ", (8, 1): "Địa Thiên Thái", (6, 3): "Thủy Hỏa Ký Tế", (3, 6): "Hỏa Thủy Vị Tế"
    }
    return mapping.get((upper, lower), f"{QUAI_NAMES.get(upper)} {QUAI_NAMES.get(lower)}")

def tinh_qua_theo_thoi_gian(dt):
    """Tính quẻ theo Giờ, Ngày, Tháng, Năm"""
    # Simplified calculation
    year_idx = (dt.year - 4) % 12 + 1
    total_upper = year_idx + dt.month + dt.day
    total_lower = total_upper + dt.hour
    
    upper = total_upper % 8
    if upper == 0: upper = 8
    
    lower = total_lower % 8
    if lower == 0: lower = 8
    
    dong_hao = total_lower % 6
    if dong_hao == 0: dong_hao = 6
    
    return {
        'upper': upper,
        'lower': lower,
        'ten_qua': get_qua_name(upper, lower),
        'qua_bien': "Quẻ Biến (Tính toán...)",
        'qua_ho': "Quẻ Hỗ (Tính toán...)",
        'dong_hao': dong_hao,
        'ngu_hanh': "Kim/Thủy/Mộc/Hỏa/Thổ"
    }

def tinh_qua_ngau_nhien():
    """Tính quẻ ngẫu hứng"""
    upper = random.randint(1, 8)
    lower = random.randint(1, 8)
    dong_hao = random.randint(1, 6)
    return {
        'upper': upper,
        'lower': lower,
        'ten_qua': get_qua_name(upper, lower),
        'dong_hao': dong_hao
    }

def giai_qua(ten_qua):
    """Trả về lời giải chi tiết cho quẻ"""
    interpretations = {
        "Càn Vi Thiên": "Vạn vật khởi đầu, hanh thông, cương kiện.",
        "Khôn Vi Địa": "Nhu thuận, bao dung, hậu đức tải vật.",
        "Địa Thiên Thái": "Thời kỳ hưng thịnh, thái bình, giao hòa.",
        "Thiên Địa Bĩ": "Bế tắc, không thông, nên thu mình.",
        "Thủy Hỏa Ký Tế": "Đã thành công, cần giữ gìn.",
        "Hỏa Thủy Vị Tế": "Chưa xong, còn hy vọng, cần nỗ lực."
    }
    return interpretations.get(ten_qua, "Lời giải đang được cập nhật từ hệ thống dữ liệu...")

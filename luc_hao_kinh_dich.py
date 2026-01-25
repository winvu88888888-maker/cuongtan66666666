
# luc_hao_kinh_dich.py - Module Lục Hào Kinh Dịch
import random

LUC_THAN = ["Huynh Đệ", "Phụ Mẫu", "Quan Quỷ", "Thê Tài", "Tử Tôn"]
LUC_THU = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]

def lap_qua_luc_hao(dt):
    """Lập quẻ Lục Hào chi tiết"""
    # Randomly generate 6 lines for demonstration
    hao_results = []
    for i in range(6):
        hao = random.randint(6, 9) # 6: Old Yin, 7: Young Yang, 8: Young Yin, 9: Old Yang
        hao_results.append(hao)
    
    # Map Lục Thú based on Day Can (Placeholder calculation)
    # Giáp/Ất -> Thanh Long, Bính/Đinh -> Chu Tước...
    luc_thu_start = random.randint(0, 5)
    luc_thu_mapped = {i+1: LUC_THU[(luc_thu_start + i) % 6] for i in range(6)}
    
    # Map Lục Thân based on Palace and Subject (Placeholder)
    luc_than_mapped = {i+1: LUC_THAN[random.randint(0, 4)] for i in range(6)}
    
    return {
        'qua_ban': "Quẻ Bản (Lập từ Hào)",
        'qua_bien': "Quẻ Biến (Lập từ Hào động)",
        'dong_hao': [i+1 for i, h in enumerate(hao_results) if h == 6 or h == 9],
        'luc_than': luc_than_mapped,
        'luc_thu': luc_thu_mapped,
        'vuong_suy': {i+1: "Vượng" if random.random() > 0.5 else "Suy" for i in range(6)},
        'the_ung': {"Thế": 3, "Ứng": 6},
        'giai_thich': "Hệ thống đang phân tích các hào động và sự tương tác sinh khắc..."
    }

def phan_tich_luc_than_theo_chu_de(topic, luc_than_map):
    """Phân tích Lục Thân dựa trên chủ đề người dùng chọn"""
    # Logic to tie topic to specific Dung Than
    return f"Dựa trên chủ đề '{topic}', Dụng Thần chính là {luc_than_map.get(1)}..."

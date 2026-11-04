"""
QUY TẮC SUY LUẬN HOÀN CHỈNH - Trả Lời MỌI Câu Hỏi Bói Toán
Không được nói "không có dữ liệu" - PHẢI suy luận từ các yếu tố có sẵn!
"""

# ============================================================
# NGUYÊN TẮC VÀNG: KHÔNG BAO GIỜ NÓI "KHÔNG CÓ DỮ LIỆU"
# ============================================================

NGUYEN_TAC_TRA_LOI = """
1. LUÔN suy luận từ các yếu tố có sẵn trong bàn cờ
2. Sử dụng Ngũ Hành để suy ra: Màu sắc, Giá trị, Khoảng cách
3. Sử dụng Can/Chi để suy ra: Giới tính, Tuổi, Tính cách
4. Sử dụng Sao/Môn/Thần để suy ra: Kết quả, Khả năng
5. KHÔNG BAO GIỜ trả lời "bàn cờ không cung cấp thông tin"
"""

# ============================================================
# PHẦN 1: MÀU SẮC VẬT MẤT (DỰA VÀO NGŨ HÀNH CUNG CHỨA DỤNG THẦN)
# ============================================================

MAU_SAC_VAT_MAT = {
    # Ngũ Hành → Màu sắc chính + phụ
    "Kim": {
        "Chinh": "TRẮNG hoặc BẠC",
        "Phu": ["Xám nhạt", "Vàng kim", "Crôm"],
        "Mo_Ta": "Xe màu TRẮNG/BẠC, có thể có chi tiết kim loại sáng bóng"
    },
    "Mộc": {
        "Chinh": "XANH LÁ hoặc XANH NGỌC",
        "Phu": ["Xanh lục", "Xanh rêu", "Xanh olive"],
        "Mo_Ta": "Xe màu XANH LÁ, có thể là xanh ngọc hoặc xanh rêu"
    },
    "Thủy": {
        "Chinh": "ĐEN hoặc XANH DƯƠNG ĐẬM",
        "Phu": ["Xanh than", "Xanh navy", "Đen bóng"],
        "Mo_Ta": "Xe màu ĐEN hoặc XANH DƯƠNG ĐẬM"
    },
    "Hỏa": {
        "Chinh": "ĐỎ hoặc CAM",
        "Phu": ["Hồng", "Tím", "Đỏ đô"],
        "Mo_Ta": "Xe màu ĐỎ, có thể là cam hoặc hồng"
    },
    "Thổ": {
        "Chinh": "VÀNG hoặc NÂU",
        "Phu": ["Be", "Kem", "Nâu đất"],
        "Mo_Ta": "Xe màu VÀNG/NÂU/BE"
    }
}

# Cung → Ngũ Hành
CUNG_NGU_HANH = {
    1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ",
    6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"
}

def tinh_mau_sac_vat(cung_so):
    """Tính màu sắc vật mất dựa vào cung"""
    hanh = CUNG_NGU_HANH.get(cung_so, "Thổ")
    mau = MAU_SAC_VAT_MAT.get(hanh, {})
    return {
        "mau_chinh": mau.get("Chinh", "Không xác định cụ thể"),
        "mau_phu": mau.get("Phu", []),
        "mo_ta": mau.get("Mo_Ta", "Cần xem thêm yếu tố khác")
    }

# ============================================================
# PHẦN 2: GIÁ TRỊ VẬT MẤT (DỰA VÀO SỐ CUNG + NGŨ HÀNH)
# ============================================================

GIA_TRI_VE_SO = {
    # Cung → Số gốc → Giá trị (triệu VNĐ)
    1: {"So": 1, "Don_Vi": "1-10", "Gia_Tri_Xe_Dap": "1-3 triệu"},
    2: {"So": 2, "Don_Vi": "2-20", "Gia_Tri_Xe_Dap": "2-5 triệu"},
    3: {"So": 3, "Don_Vi": "3-30", "Gia_Tri_Xe_Dap": "3-7 triệu"},
    4: {"So": 4, "Don_Vi": "4-40", "Gia_Tri_Xe_Dap": "4-8 triệu"},
    5: {"So": 5, "Don_Vi": "5-50", "Gia_Tri_Xe_Dap": "5-10 triệu"},
    6: {"So": 6, "Don_Vi": "6-60", "Gia_Tri_Xe_Dap": "6-15 triệu (xe tốt)"},
    7: {"So": 7, "Don_Vi": "7-70", "Gia_Tri_Xe_Dap": "2-7 triệu"},
    8: {"So": 8, "Don_Vi": "8-80", "Gia_Tri_Xe_Dap": "3-8 triệu"},
    9: {"So": 9, "Don_Vi": "9-90", "Gia_Tri_Xe_Dap": "5-20 triệu (xe cao cấp)"}
}

def tinh_gia_tri_vat(cung_so, loai_vat="xe đạp"):
    """Tính giá trị vật mất"""
    info = GIA_TRI_VE_SO.get(cung_so, {})
    return {
        "gia_tri": info.get("Gia_Tri_Xe_Dap", "2-5 triệu"),
        "so_goc": info.get("So", 5),
        "don_vi": info.get("Don_Vi", "5-50")
    }

# ============================================================
# PHẦN 3: KHOẢNG CÁCH CHI TIẾT (MÉT + KM)
# ============================================================

KHOANG_CACH_CHUAN = {
    1: {"Met": "100-1000m", "Km": "0.1-1km", "Mo_Ta": "Gần, hướng BẮC, nơi có nước"},
    2: {"Met": "50-500m", "Km": "0.05-0.5km", "Mo_Ta": "RẤT GẦN, hướng TÂY NAM, đất trống"},
    3: {"Met": "300-3000m", "Km": "0.3-3km", "Mo_Ta": "Trung bình, hướng ĐÔNG, chợ búa"},
    4: {"Met": "400-4000m", "Km": "0.4-4km", "Mo_Ta": "Khá xa, hướng ĐÔNG NAM"},
    5: {"Met": "0-200m", "Km": "0-0.2km", "Mo_Ta": "NGAY TẠI CHỖ, trong nhà hoặc xung quanh"},
    6: {"Met": "600-6000m", "Km": "0.6-6km", "Mo_Ta": "XA, hướng TÂY BẮC, nhà cao/cơ quan"},
    7: {"Met": "70-700m", "Km": "0.07-0.7km", "Mo_Ta": "Trung bình, hướng TÂY, quán xá"},
    8: {"Met": "80-800m", "Km": "0.08-0.8km", "Mo_Ta": "Gần, hướng ĐÔNG BẮC, núi đồi/kho"},
    9: {"Met": "900-9000m", "Km": "0.9-9km", "Mo_Ta": "XA, hướng NAM, trường học/nơi nóng"}
}

def tinh_khoang_cach(cung_so):
    """Tính khoảng cách chi tiết"""
    info = KHOANG_CACH_CHUAN.get(cung_so, {})
    return {
        "met": info.get("Met", "500-1000m"),
        "km": info.get("Km", "0.5-1km"),
        "mo_ta": info.get("Mo_Ta", "Trung bình xa")
    }

# ============================================================
# PHẦN 4: KẺ TRỘM CÓ BỊ BẮT KHÔNG?
# ============================================================

KHA_NANG_BI_BAT = {
    # Dựa vào Môn của cung Huyền Vũ hoặc cung chứa kẻ trộm
    "Khai Môn": {
        "Ty_Le": "75%", 
        "Ket_Luan": "CÓ KHẢ NĂNG BỊ BẮT - Khai Môn = Công an/Chính quyền can thiệp",
        "Chi_Tiet": "Nên báo công an, có người quyền lực giúp"
    },
    "Kinh Môn": {
        "Ty_Le": "70%",
        "Ket_Luan": "CÓ KHẢ NĂNG BỊ BẮT - Kinh Môn = Sợ hãi, bị phát hiện",
        "Chi_Tiet": "Kẻ trộm sẽ sợ và có thể tự thú hoặc bị bắt"
    },
    "Sinh Môn": {
        "Ty_Le": "30%",
        "Ket_Luan": "KHÓ BỊ BẮT - Sinh Môn = Kẻ trộm thoát, có lợi cho nó",
        "Chi_Tiet": "Kẻ trộm may mắn, khó bắt được"
    },
    "Hưu Môn": {
        "Ty_Le": "40%",
        "Ket_Luan": "KHÓ BỊ BẮT - Hưu Môn = Kẻ trộm nghỉ ngơi, ẩn náu",
        "Chi_Tiet": "Kẻ trộm đang ẩn náu an toàn"
    },
    "Tử Môn": {
        "Ty_Le": "60%",
        "Ket_Luan": "CÓ THỂ BỊ BẮT - Tử Môn = Kẻ trộm gặp kết cục xấu",
        "Chi_Tiet": "Kẻ trộm có thể bị bắt hoặc gặp tai họa"
    },
    "Thương Môn": {
        "Ty_Le": "65%",
        "Ket_Luan": "CÓ THỂ BỊ BẮT - Thương Môn = Có xung đột, bị tố giác",
        "Chi_Tiet": "Kẻ trộm bị người khác tố giác"
    },
    "Đỗ Môn": {
        "Ty_Le": "20%",
        "Ket_Luan": "KHÓ BỊ BẮT - Đỗ Môn = Kẻ trộm ẩn náu kỹ",
        "Chi_Tiet": "Kẻ trộm giấu kỹ, khó tìm ra"
    },
    "Cảnh Môn": {
        "Ty_Le": "50%",
        "Ket_Luan": "50/50 - Cảnh Môn = Có thể bị phát hiện nếu nhanh",
        "Chi_Tiet": "Cần hành động nhanh mới bắt được"
    }
}

# Dựa vào Thần
KHA_NANG_BI_BAT_THEO_THAN = {
    "Trực Phù": "80% BỊ BẮT - Có quý nhân can thiệp, công an giúp",
    "Đằng Xà": "40% - Kẻ trộm biến hóa, khó bắt",
    "Thái Âm": "35% - Kẻ trộm được che chở bởi phụ nữ",
    "Lục Hợp": "45% - Kẻ trộm có đồng bọn, khó bắt hết",
    "Bạch Hổ": "70% - Kẻ trộm hung hãn, dễ bị chú ý và bắt",
    "Huyền Vũ": "25% - Kẻ trộm chuyên nghiệp, rất khó bắt",
    "Cửu Địa": "55% - Kẻ trộm ẩn náu trong đất, có thể tìm được",
    "Cửu Thiên": "50% - Kẻ trộm chạy xa, 50/50 bắt được"
}

def tinh_kha_nang_bi_bat(mon, than):
    """Tính khả năng kẻ trộm bị bắt"""
    mon_key = mon.replace(" Môn", "") + " Môn" if " Môn" not in mon else mon
    mon_info = KHA_NANG_BI_BAT.get(mon_key, {})
    than_info = KHA_NANG_BI_BAT_THEO_THAN.get(than, "50% - Trung bình")
    
    return {
        "theo_mon": mon_info.get("Ket_Luan", "50/50 - Cần xem thêm"),
        "theo_than": than_info,
        "ty_le_mon": mon_info.get("Ty_Le", "50%"),
        "loi_khuyen": mon_info.get("Chi_Tiet", "Nên báo công an"),
        "ket_luan_chung": _tinh_ket_luan_bat(mon_info.get("Ty_Le", "50%"), than)
    }

def _tinh_ket_luan_bat(ty_le_mon, than):
    """Tính kết luận chung về khả năng bắt được"""
    try:
        ty_le_so = int(ty_le_mon.replace("%", ""))
    except:
        ty_le_so = 50
    
    # Điều chỉnh theo Thần
    if than in ["Trực Phù", "Bạch Hổ"]:
        ty_le_so += 15
    elif than in ["Huyền Vũ", "Thái Âm"]:
        ty_le_so -= 15
    
    ty_le_so = max(5, min(95, ty_le_so))  # Giới hạn 5-95%
    
    if ty_le_so >= 70:
        return f"CÓ KHẢ NĂNG CAO (~{ty_le_so}%) bị bắt - Nên báo công an"
    elif ty_le_so >= 50:
        return f"KHẢ NĂNG TRUNG BÌNH (~{ty_le_so}%) - Có thể bắt được nếu nhanh"
    else:
        return f"KHẢ NĂNG THẤP (~{ty_le_so}%) - Kẻ trộm khó bị bắt"

# ============================================================
# PHẦN 5: GIỚI TÍNH + TUỔI + ĐẶC ĐIỂM KẺ LẤY
# ============================================================

DAC_DIEM_KE_LAY = {
    # Theo Thiên Can
    "Giáp": {"Gioi_Tinh": "NAM", "Tuoi": "40-60", "Dac_Diem": "Đàn ông lớn tuổi, có địa vị"},
    "Ất": {"Gioi_Tinh": "NỮ", "Tuoi": "20-35", "Dac_Diem": "Phụ nữ trẻ, mảnh khảnh"},
    "Bính": {"Gioi_Tinh": "NAM/NỮ", "Tuoi": "20-40", "Dac_Diem": "Người năng động, hay di chuyển"},
    "Đinh": {"Gioi_Tinh": "NỮ", "Tuoi": "25-45", "Dac_Diem": "Phụ nữ thông minh, khéo léo"},
    "Mậu": {"Gioi_Tinh": "NAM", "Tuoi": "30-50", "Dac_Diem": "Đàn ông to con, chắc nịch"},
    "Kỷ": {"Gioi_Tinh": "NỮ", "Tuoi": "30-50", "Dac_Diem": "Phụ nữ xấu tính, hay ghen"},
    "Canh": {"Gioi_Tinh": "NAM", "Tuoi": "25-45", "Dac_Diem": "Đàn ông cứng rắn, hung dữ, có thể là đối thủ"},
    "Tân": {"Gioi_Tinh": "NỮ/NAM", "Tuoi": "18-35", "Dac_Diem": "Người trẻ, hay phạm lỗi"},
    "Nhâm": {"Gioi_Tinh": "NAM", "Tuoi": "25-50", "Dac_Diem": "Đàn ông HAY TRỘM CẮP, đi đêm"},
    "Quý": {"Gioi_Tinh": "NỮ", "Tuoi": "20-40", "Dac_Diem": "Phụ nữ lừa lọc, bí ẩn"}
}

# Theo Bát Thần
DAC_DIEM_THEO_THAN = {
    "Huyền Vũ": {"Gioi_Tinh": "NAM (90%)", "Dac_Diem": "Kẻ TRỘM CHUYÊN NGHIỆP, hay đi đêm, lén lút"},
    "Bạch Hổ": {"Gioi_Tinh": "NAM (95%)", "Dac_Diem": "Kẻ CƯỚP hung bạo, có vũ lực"},
    "Thái Âm": {"Gioi_Tinh": "NỮ (80%)", "Dac_Diem": "Phụ nữ quen biết, lén lút giấu"},
    "Lục Hợp": {"Gioi_Tinh": "NAM/NỮ", "Dac_Diem": "Có đồng bọn, người trung gian"},
    "Đằng Xà": {"Gioi_Tinh": "Khó xác định", "Dac_Diem": "Kẻ hay biến hóa, quái dị"},
    "Trực Phù": {"Gioi_Tinh": "NAM", "Dac_Diem": "Người có quyền, có thể là quen"},
    "Cửu Địa": {"Gioi_Tinh": "NỮ (60%)", "Dac_Diem": "Người già, chậm chạp, giấu trong nhà"},
    "Cửu Thiên": {"Gioi_Tinh": "NAM (70%)", "Dac_Diem": "Người năng động, mang đồ đi xa"}
}

def xac_dinh_ke_lay(can, than, cung_so):
    """Xác định chi tiết kẻ lấy đồ"""
    can_info = DAC_DIEM_KE_LAY.get(can, {})
    than_info = DAC_DIEM_THEO_THAN.get(than, {})
    
    # Tính giới tính ưu tiên
    gioi_tinh = can_info.get("Gioi_Tinh", "")
    if than in ["Huyền Vũ", "Bạch Hổ", "Cửu Thiên"]:
        gioi_tinh = "NAM (xác suất cao)"
    elif than in ["Thái Âm", "Cửu Địa"]:
        gioi_tinh = "NỮ (xác suất cao)"
    
    return {
        "gioi_tinh": gioi_tinh or than_info.get("Gioi_Tinh", "Không rõ"),
        "tuoi": can_info.get("Tuoi", "25-45"),
        "dac_diem_can": can_info.get("Dac_Diem", ""),
        "dac_diem_than": than_info.get("Dac_Diem", ""),
        "ket_luan": f"{gioi_tinh}, tuổi {can_info.get('Tuoi', '25-45')}, {than_info.get('Dac_Diem', '')}"
    }

# ============================================================
# PHẦN 6: QUEN HAY LẠ (CHI TIẾT)
# ============================================================

QUEN_LA_CHI_TIET = {
    # Theo Cung
    "Cung_1": "60% NGƯỜI LẠ - Kẻ trộm đêm, hàng xóm xa",
    "Cung_2": "70% NGƯỜI QUEN - Phụ nữ lớn tuổi gần nhà",
    "Cung_3": "50/50 - Người vội vã qua đường",
    "Cung_4": "60% QUEN - Hàng xóm, người hay đi lại",
    "Cung_5": "85% NGƯỜI NHÀ - Ngay trong nhà hoặc rất gần",
    "Cung_6": "65% NGƯỜI LẠ - Người xa, có địa vị",
    "Cung_7": "55% QUEN - Gái trẻ biết nhà",
    "Cung_8": "75% QUEN - Trẻ em hoặc thanh niên gần nhà",
    "Cung_9": "50/50 - Người nóng tính, có thể quen hoặc lạ",
    
    # Theo Thần (ưu tiên cao hơn)
    "Huyền Vũ": "90% NGƯỜI LẠ - Kẻ trộm chuyên nghiệp, không quen",
    "Bạch Hổ": "95% NGƯỜI LẠ - Kẻ cướp hung bạo",
    "Thái Âm": "70% NGƯỜI QUEN - Phụ nữ quen biết",
    "Lục Hợp": "80% NGƯỜI QUEN - Bạn bè, người thân quen",
    "Cửu Địa": "75% QUEN - Người gần nhà, hàng xóm"
}

def xac_dinh_quen_la(cung_so, than):
    """Xác định người quen hay lạ"""
    than_info = QUEN_LA_CHI_TIET.get(than, "")
    cung_info = QUEN_LA_CHI_TIET.get(f"Cung_{cung_so}", "50/50")
    
    # Ưu tiên theo Thần
    if than_info:
        return {
            "ket_luan": than_info,
            "nguon": "Theo Bát Thần (độ tin cậy cao)"
        }
    return {
        "ket_luan": cung_info,
        "nguon": "Theo Cung vị"
    }

# ============================================================
# PHẦN 7: HÀM TỔNG HỢP - TRẢ LỜI MỌI CÂU HỎI
# ============================================================

def phan_tich_toan_dien_tim_do(cung_dung_than, can, mon, than):
    """
    Phân tích TOÀN DIỆN việc tìm đồ mất
    Trả lời TẤT CẢ các câu hỏi có thể có
    """
    cung_so = cung_dung_than
    
    # 1. Màu sắc
    mau = tinh_mau_sac_vat(cung_so)
    
    # 2. Giá trị
    gia = tinh_gia_tri_vat(cung_so)
    
    # 3. Khoảng cách + Hướng
    khoang_cach = tinh_khoang_cach(cung_so)
    
    # 4. Kẻ lấy (giới tính, tuổi, đặc điểm)
    ke_lay = xac_dinh_ke_lay(can, than, cung_so)
    
    # 5. Quen hay lạ
    quen_la = xac_dinh_quen_la(cung_so, than)
    
    # 6. Khả năng lấy lại (từ qmdg_advanced_rules)
    from qmdg_advanced_rules import KHA_NANG_LAY_LAI
    mon_key = mon.replace(" Môn", "") + " Môn"
    kha_nang_lay_lai = KHA_NANG_LAY_LAI.get(mon_key, {})
    
    # 7. Kẻ trộm có bị bắt không
    bi_bat = tinh_kha_nang_bi_bat(mon, than)
    
    return {
        "mau_sac": mau,
        "gia_tri": gia,
        "khoang_cach": khoang_cach,
        "ke_lay": ke_lay,
        "quen_la": quen_la,
        "kha_nang_lay_lai": {
            "ty_le": kha_nang_lay_lai.get("Ty_Le", "50%"),
            "ket_luan": kha_nang_lay_lai.get("Ket_Luan", "Trung bình")
        },
        "ke_trom_bi_bat": bi_bat
    }

def format_ket_qua_cho_ai(ket_qua):
    """Format kết quả để AI dùng trong prompt"""
    output = []
    output.append(f"🎨 MÀU SẮC: {ket_qua['mau_sac']['mau_chinh']} ({ket_qua['mau_sac']['mo_ta']})")
    output.append(f"💰 GIÁ TRỊ: Khoảng {ket_qua['gia_tri']['gia_tri']}")
    output.append(f"📍 KHOẢNG CÁCH: {ket_qua['khoang_cach']['met']} ({ket_qua['khoang_cach']['mo_ta']})")
    output.append(f"👤 KẺ LẤY: {ket_qua['ke_lay']['ket_luan']}")
    output.append(f"🔗 QUEN/LẠ: {ket_qua['quen_la']['ket_luan']}")
    output.append(f"🔄 LẤY LẠI: {ket_qua['kha_nang_lay_lai']['ty_le']} - {ket_qua['kha_nang_lay_lai']['ket_luan']}")
    output.append(f"👮 BỊ BẮT: {ket_qua['ke_trom_bi_bat']['ket_luan_chung']}")
    return "\n".join(output)


# Export
__all__ = [
    'MAU_SAC_VAT_MAT', 'GIA_TRI_VE_SO', 'KHOANG_CACH_CHUAN',
    'KHA_NANG_BI_BAT', 'DAC_DIEM_KE_LAY', 'QUEN_LA_CHI_TIET',
    'tinh_mau_sac_vat', 'tinh_gia_tri_vat', 'tinh_khoang_cach',
    'tinh_kha_nang_bi_bat', 'xac_dinh_ke_lay', 'xac_dinh_quen_la',
    'phan_tich_toan_dien_tim_do', 'format_ket_qua_cho_ai'
]

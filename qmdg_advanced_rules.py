"""
QMDG ADVANCED RULES - Quy Tắc Liên Kết Nâng Cao
Bổ sung: Màu sắc, Quen/Lạ, 64 Quẻ, Quy tắc xác định chi tiết
"""

# ============================================================
# PHẦN 1: BẢN ĐỒ MÀU SẮC THEO NGŨ HÀNH
# ============================================================

MAU_SAC_NGU_HANH = {
    "Kim": {
        "Mau_Chinh": ["Trắng", "Bạc", "Vàng kim", "Xám nhạt"],
        "Tuong": "Xe màu trắng, bạc, kim loại sáng bóng",
        "Vat": "Đồ kim loại, xe máy, xe đạp inox"
    },
    "Mộc": {
        "Mau_Chinh": ["Xanh lá", "Xanh lục", "Xanh ngọc"],
        "Tuong": "Xe màu xanh lá, xanh ngọc, màu cỏ",
        "Vat": "Đồ gỗ, xe khung gỗ, xe tre"
    },
    "Thủy": {
        "Mau_Chinh": ["Đen", "Xanh dương đậm", "Xanh than"],
        "Tuong": "Xe màu đen, xanh đậm, tối màu",
        "Vat": "Đồ liên quan nước, xe chở nước"
    },
    "Hỏa": {
        "Mau_Chinh": ["Đỏ", "Cam", "Hồng", "Tím"],
        "Tuong": "Xe màu đỏ, cam, hồng, tím",
        "Vat": "Đồ phát sáng, xe có đèn led"
    },
    "Thổ": {
        "Mau_Chinh": ["Vàng đất", "Nâu", "Be", "Kem"],
        "Tuong": "Xe màu vàng, nâu, be, kem",
        "Vat": "Đồ đất, gạch, xi măng"
    }
}

# ============================================================
# PHẦN 2: XÁC ĐỊNH NGƯỜI QUEN HAY NGƯỜI LẠ
# ============================================================

QUEN_LA_QUY_TAC = {
    # Dựa vào Lục Thân (Quan hệ với Can Ngày)
    "Huynh_De": {
        "Quan_He": "NGƯỜI QUEN - Anh em, bạn bè, đồng nghiệp",
        "Chi_Tiet": "Cùng hành với Can Ngày = Người ngang vai, quen biết",
        "Xac_Suat": "80% là người quen"
    },
    "Phu_Mau": {
        "Quan_He": "NGƯỜI QUEN - Người lớn tuổi hơn, cha mẹ, thầy cô",
        "Chi_Tiet": "Hành sinh Can Ngày = Người bề trên",
        "Xac_Suat": "70% là người quen"
    },
    "Tu_Ton": {
        "Quan_He": "NGƯỜI QUEN - Con cháu, người nhỏ tuổi",
        "Chi_Tiet": "Can Ngày sinh ra = Người bề dưới, trẻ con",
        "Xac_Suat": "75% là người quen"
    },
    "The_Tai": {
        "Quan_He": "CÓ THỂ QUEN HOẶC LẠ - Vợ/chồng, tiền bạc, tài sản",
        "Chi_Tiet": "Can Ngày khắc = Người liên quan tài sản",
        "Xac_Suat": "50% quen, 50% lạ"
    },
    "Quan_Quy": {
        "Quan_He": "NGƯỜI LẠ - Kẻ thù, quan chức, tiểu nhân",
        "Chi_Tiet": "Khắc Can Ngày = Người đối lập, kẻ địch",
        "Xac_Suat": "80% là người lạ, tiểu nhân"
    },
    
    # Dựa vào Bát Thần
    "Huyen_Vu_Quen_La": {
        "Than": "Huyền Vũ",
        "Ket_Luan": "NGƯỜI LẠ - Kẻ trộm chuyên nghiệp, tiểu nhân",
        "Chi_Tiet": "Huyền Vũ = Lén lút, không ai biết, người lạ 90%"
    },
    "Thai_Am_Quen_La": {
        "Than": "Thái Âm", 
        "Ket_Luan": "NGƯỜI QUEN - Phụ nữ quen biết, người nhà",
        "Chi_Tiet": "Thái Âm = Ẩn giấu nhưng quen biết, 70% quen"
    },
    "Luc_Hop_Quen_La": {
        "Than": "Lục Hợp",
        "Ket_Luan": "NGƯỜI QUEN - Bạn bè thân, người môi giới quen",
        "Chi_Tiet": "Lục Hợp = Hợp tác, 85% là quen biết"
    },
    "Bach_Ho_Quen_La": {
        "Than": "Bạch Hổ",
        "Ket_Luan": "NGƯỜI LẠ - Kẻ cướp, cưỡng đoạt",
        "Chi_Tiet": "Bạch Hổ = Hung bạo, 95% là người lạ"
    },
    
    # Dựa vào Cung vị
    "Cung_1_Quen_La": "Có thể quen (hàng xóm) hoặc lạ (kẻ trộm đêm)",
    "Cung_2_Quen_La": "80% là người quen, phụ nữ lớn tuổi gần đó",
    "Cung_3_Quen_La": "50% quen 50% lạ, người vội vã",
    "Cung_4_Quen_La": "60% người quen, hàng xóm, người hay đi lại",
    "Cung_5_Quen_La": "90% trong nhà, người thân quen",
    "Cung_6_Quen_La": "70% người lạ, có quyền lực hoặc xa",
    "Cung_7_Quen_La": "60% người quen, cô gái trẻ biết nhà",
    "Cung_8_Quen_La": "80% người quen, trẻ em hoặc người trẻ quanh đó",
    "Cung_9_Quen_La": "50% quen 50% lạ, người nóng tính"
}

# ============================================================
# PHẦN 3: KHOẢNG CÁCH CHI TIẾT (ĐƠN VỊ CỤ THỂ)
# ============================================================

KHOANG_CACH_CHI_TIET = {
    1: {"So_Buoc": "1-100", "So_Met": "100-1000m", "Mo_Ta": "Về hướng Bắc, gần nơi có nước"},
    2: {"So_Buoc": "2-50", "So_Met": "50-500m", "Mo_Ta": "Rất gần, hướng Tây Nam, đất trống"},
    3: {"So_Buoc": "3-300", "So_Met": "300-3000m", "Mo_Ta": "Trung bình, hướng Đông, nơi đông người"},
    4: {"So_Buoc": "4-400", "So_Met": "400-4000m", "Mo_Ta": "Khá xa, hướng Đông Nam, nơi cao"},
    5: {"So_Buoc": "0-20", "So_Met": "0-200m", "Mo_Ta": "Ngay tại chỗ, trong nhà, xung quanh"},
    6: {"So_Buoc": "6-600", "So_Met": "600-6000m", "Mo_Ta": "Xa, hướng Tây Bắc, nhà cao/cơ quan"},
    7: {"So_Buoc": "7-70", "So_Met": "70-700m", "Mo_Ta": "Trung bình, hướng Tây, quán xá"},
    8: {"So_Buoc": "8-80", "So_Met": "80-800m", "Mo_Ta": "Gần, hướng Đông Bắc, núi đồi/kho"},
    9: {"So_Buoc": "9-900", "So_Met": "900-9000m", "Mo_Ta": "Xa, hướng Nam, nơi nóng/trường học"}
}

# ============================================================
# PHẦN 4: KHẢ NĂNG LẤY LẠI CHI TIẾT
# ============================================================

KHA_NANG_LAY_LAI = {
    # Theo Bát Môn
    "Sinh Môn": {"Ty_Le": "85%", "Ket_Luan": "RẤT CÓ THỂ lấy lại, đồ còn nguyên vẹn"},
    "Hưu Môn": {"Ty_Le": "80%", "Ket_Luan": "CÓ THỂ lấy lại, đồ đang yên ổn"},
    "Khai Môn": {"Ty_Le": "70%", "Ket_Luan": "CÓ THỂ lấy nếu nhờ công an/người quyền lực"},
    "Cảnh Môn": {"Ty_Le": "50%", "Ket_Luan": "KHÓ - đồ có thể đã đổi chủ, cần nhanh"},
    "Đỗ Môn": {"Ty_Le": "40%", "Ket_Luan": "KHÓ - đồ bị giấu kín, cần tìm kỹ"},
    "Thương Môn": {"Ty_Le": "25%", "Ket_Luan": "RẤT KHÓ - đồ có thể hỏng hoặc bị bán"},
    "Kinh Môn": {"Ty_Le": "15%", "Ket_Luan": "CỰC KHÓ - đồ đã đi xa, cần kiện tụng"},
    "Tử Môn": {"Ty_Le": "5%", "Ket_Luan": "GẦN NHƯ KHÔNG THỂ - đồ mất vĩnh viễn"},
    
    # Bổ sung theo Sao
    "Thiên Bồng_Tim": "Khó tìm - kẻ lấy là trộm chuyên nghiệp",
    "Thiên Tâm_Tim": "Dễ tìm - có quý nhân giúp đỡ",
    "Thiên Nhuế_Tim": "Trung bình - đồ ở gần nhưng bị che giấu",
    "Thiên Nhậm_Tim": "Dễ tìm - đồ nằm yên một chỗ",
    "Thiên Anh_Tim": "Khó - đồ có thể bị hư hỏng",
    
    # Bổ sung theo Tuần Không
    "Dung_Than_Khong": "KHÔNG THỂ TÌM - Dụng thần lâm Không = Đồ mất vĩnh viễn",
    "Ke_Lay_Khong": "CÓ THỂ TÌM - Kẻ lấy lâm Không = Kẻ lấy yếu, trả lại"
}

# ============================================================
# PHẦN 5: 64 QUẺ KINH DỊCH - ĐẦY ĐỦ
# ============================================================

QUE_64 = {
    # Thuần Quái (8 quẻ thuần)
    1: {"Ten": "Thuần Càn", "Tuong": "Trời", "Cat_Hung": "Đại Cát", "Luan": "Cương kiện, thành công lớn, đắc quý nhân"},
    2: {"Ten": "Thuần Khôn", "Tuong": "Đất", "Cat_Hung": "Cát", "Luan": "Thuận theo, có quý nhân nữ, chậm mà chắc"},
    3: {"Ten": "Thủy Lôi Truân", "Tuong": "Mây sấm", "Cat_Hung": "Tiểu Hung", "Luan": "Khó khăn ban đầu, sau sẽ hanh"},
    4: {"Ten": "Sơn Thủy Mông", "Tuong": "Mông muội", "Cat_Hung": "Bình", "Luan": "Cần học hỏi, tìm thầy giỏi"},
    5: {"Ten": "Thủy Thiên Nhu", "Tuong": "Chờ đợi", "Cat_Hung": "Cát", "Luan": "Cần kiên nhẫn, chờ thời cơ"},
    6: {"Ten": "Thiên Thủy Tụng", "Tuong": "Kiện tụng", "Cat_Hung": "Hung", "Luan": "Tranh chấp, nên hòa giải"},
    7: {"Ten": "Địa Thủy Sư", "Tuong": "Quân đội", "Cat_Hung": "Bình", "Luan": "Cần đông người, hợp tác"},
    8: {"Ten": "Thủy Địa Tỷ", "Tuong": "Thân cận", "Cat_Hung": "Cát", "Luan": "Hợp tác tốt, gần gũi"},
    
    # Quẻ về tìm đồ mất (đặc biệt quan trọng)
    9: {"Ten": "Phong Thiên Tiểu Súc", "Tuong": "Tích nhỏ", "Cat_Hung": "Bình", "Luan": "Đồ còn gần, từ từ tìm"},
    10: {"Ten": "Thiên Trạch Lý", "Tuong": "Giẫm", "Cat_Hung": "Bình", "Luan": "Cẩn thận từng bước, tìm được"},
    11: {"Ten": "Địa Thiên Thái", "Tuong": "Thái", "Cat_Hung": "Đại Cát", "Luan": "RẤT TỐT - mọi việc hanh thông, tìm được đồ"},
    12: {"Ten": "Thiên Địa Bĩ", "Tuong": "Bế tắc", "Cat_Hung": "Đại Hung", "Luan": "XẤU - bế tắc, đồ khó tìm"},
    
    13: {"Ten": "Thiên Hỏa Đồng Nhân", "Tuong": "Đồng lòng", "Cat_Hung": "Cát", "Luan": "Nhờ bạn bè giúp tìm"},
    14: {"Ten": "Hỏa Thiên Đại Hữu", "Tuong": "Nhiều của", "Cat_Hung": "Đại Cát", "Luan": "Tìm được, có thêm lộc"},
    15: {"Ten": "Địa Sơn Khiêm", "Tuong": "Khiêm nhường", "Cat_Hung": "Cát", "Luan": "Khiêm tốn sẽ tìm được"},
    16: {"Ten": "Lôi Địa Dự", "Tuong": "Vui vẻ", "Cat_Hung": "Cát", "Luan": "Có tin vui, tìm được đồ"},
    
    17: {"Ten": "Trạch Lôi Tùy", "Tuong": "Theo", "Cat_Hung": "Cát", "Luan": "Theo dấu vết sẽ tìm được"},
    18: {"Ten": "Sơn Phong Cổ", "Tuong": "Sửa chữa", "Cat_Hung": "Bình", "Luan": "Đồ có thể hỏng, cần sửa"},
    19: {"Ten": "Địa Trạch Lâm", "Tuong": "Đến gần", "Cat_Hung": "Đại Cát", "Luan": "Đồ sắp về, sẽ tìm được"},
    20: {"Ten": "Phong Địa Quán", "Tuong": "Quan sát", "Cat_Hung": "Bình", "Luan": "Quan sát kỹ sẽ thấy"},
    
    21: {"Ten": "Hỏa Lôi Phệ Hạp", "Tuong": "Cắn", "Cat_Hung": "Bình", "Luan": "Cần quyết liệt, kiên trì"},
    22: {"Ten": "Sơn Hỏa Bí", "Tuong": "Trang sức", "Cat_Hung": "Tiểu Cát", "Luan": "Đồ đẹp, tìm được"},
    23: {"Ten": "Sơn Địa Bác", "Tuong": "Bóc lột", "Cat_Hung": "Hung", "Luan": "Bị lấy mất, khó tìm"},
    24: {"Ten": "Địa Lôi Phục", "Tuong": "Trở lại", "Cat_Hung": "Cát", "Luan": "ĐỒ SẼ TRỞ VỀ, tìm được"},
    
    25: {"Ten": "Thiên Lôi Vô Vọng", "Tuong": "Không mong", "Cat_Hung": "Cát", "Luan": "Bất ngờ tìm được"},
    26: {"Ten": "Sơn Thiên Đại Súc", "Tuong": "Tích lớn", "Cat_Hung": "Đại Cát", "Luan": "Tích đức sẽ tìm được"},
    27: {"Ten": "Sơn Lôi Di", "Tuong": "Nuôi", "Cat_Hung": "Bình", "Luan": "Cần kiên nhẫn nuôi hy vọng"},
    28: {"Ten": "Trạch Phong Đại Quá", "Tuong": "Quá lớn", "Cat_Hung": "Hung", "Luan": "Việc quá sức, khó tìm"},
    
    29: {"Ten": "Thuần Khảm", "Tuong": "Nước", "Cat_Hung": "Hung", "Luan": "Nhiều hiểm nguy, đồ ở nơi có nước"},
    30: {"Ten": "Thuần Ly", "Tuong": "Lửa", "Cat_Hung": "Bình", "Luan": "Đồ ở phương Nam, nơi sáng"},
    
    31: {"Ten": "Trạch Sơn Hàm", "Tuong": "Cảm ứng", "Cat_Hung": "Cát", "Luan": "Có linh cảm sẽ tìm được"},
    32: {"Ten": "Lôi Phong Hằng", "Tuong": "Lâu dài", "Cat_Hung": "Cát", "Luan": "Kiên trì sẽ tìm được"},
    33: {"Ten": "Thiên Sơn Độn", "Tuong": "Lui ẩn", "Cat_Hung": "Bình", "Luan": "Đồ bị giấu, lui một bước"},
    34: {"Ten": "Lôi Thiên Đại Tráng", "Tuong": "Mạnh lớn", "Cat_Hung": "Cát", "Luan": "Mạnh mẽ tìm kiếm"},
    
    35: {"Ten": "Hỏa Địa Tấn", "Tuong": "Tiến", "Cat_Hung": "Cát", "Luan": "Tiến lên sẽ tìm được"},
    36: {"Ten": "Địa Hỏa Minh Di", "Tuong": "Tổn thương", "Cat_Hung": "Hung", "Luan": "Đồ bị hỏng, khó tìm"},
    37: {"Ten": "Phong Hỏa Gia Nhân", "Tuong": "Người nhà", "Cat_Hung": "Cát", "Luan": "Người nhà biết, hỏi trong nhà"},
    38: {"Ten": "Hỏa Trạch Khuê", "Tuong": "Trái ngược", "Cat_Hung": "Tiểu Hung", "Luan": "Có mâu thuẫn, khó hợp tác tìm"},
    
    39: {"Ten": "Thủy Sơn Kiển", "Tuong": "Khó khăn", "Cat_Hung": "Hung", "Luan": "Gặp trở ngại, đợi thời"},
    40: {"Ten": "Lôi Thủy Giải", "Tuong": "Giải thoát", "Cat_Hung": "Cát", "Luan": "Vượt khó, sẽ tìm được"},
    41: {"Ten": "Sơn Trạch Tổn", "Tuong": "Bớt", "Cat_Hung": "Bình", "Luan": "Bớt kỳ vọng, từ từ tìm"},
    42: {"Ten": "Phong Lôi Ích", "Tuong": "Thêm", "Cat_Hung": "Đại Cát", "Luan": "Có thêm manh mối, tìm được"},
    
    43: {"Ten": "Trạch Thiên Quải", "Tuong": "Quyết", "Cat_Hung": "Cát", "Luan": "Quyết tâm sẽ tìm được"},
    44: {"Ten": "Thiên Phong Cấu", "Tuong": "Gặp gỡ", "Cat_Hung": "Bình", "Luan": "Bất ngờ gặp lại đồ"},
    45: {"Ten": "Trạch Địa Tụy", "Tuong": "Tụ họp", "Cat_Hung": "Cát", "Luan": "Nhờ đông người tìm"},
    46: {"Ten": "Địa Phong Thăng", "Tuong": "Lên", "Cat_Hung": "Đại Cát", "Luan": "Vận may lên, tìm được"},
    
    47: {"Ten": "Trạch Thủy Khốn", "Tuong": "Khốn khó", "Cat_Hung": "Hung", "Luan": "Gặp khó, đợi thời"},
    48: {"Ten": "Thủy Phong Tỉnh", "Tuong": "Giếng", "Cat_Hung": "Bình", "Luan": "Đồ ở chỗ sâu/thấp"},
    49: {"Ten": "Trạch Hỏa Cách", "Tuong": "Thay đổi", "Cat_Hung": "Bình", "Luan": "Đổi cách tìm kiếm"},
    50: {"Ten": "Hỏa Phong Đỉnh", "Tuong": "Đỉnh", "Cat_Hung": "Đại Cát", "Luan": "Thành công, tìm được"},
    
    51: {"Ten": "Thuần Chấn", "Tuong": "Sấm", "Cat_Hung": "Bình", "Luan": "Có động tĩnh, tìm nhanh"},
    52: {"Ten": "Thuần Cấn", "Tuong": "Núi", "Cat_Hung": "Bình", "Luan": "Đồ nằm yên, tìm kỹ"},
    53: {"Ten": "Phong Sơn Tiệm", "Tuong": "Dần dần", "Cat_Hung": "Cát", "Luan": "Từ từ sẽ tìm được"},
    54: {"Ten": "Lôi Trạch Quy Muội", "Tuong": "Gả em", "Cat_Hung": "Hung", "Luan": "Đồ đổi chủ, khó lấy lại"},
    
    55: {"Ten": "Lôi Hỏa Phong", "Tuong": "Nhiều", "Cat_Hung": "Cát", "Luan": "Vận may đến, tìm được"},
    56: {"Ten": "Hỏa Sơn Lữ", "Tuong": "Lữ hành", "Cat_Hung": "Bình", "Luan": "Đồ đi xa, cần đi tìm"},
    57: {"Ten": "Thuần Tốn", "Tuong": "Gió", "Cat_Hung": "Tiểu Cát", "Luan": "Tin tức đến, tìm được"},
    58: {"Ten": "Thuần Đoài", "Tuong": "Đầm", "Cat_Hung": "Cát", "Luan": "Vui mừng, đồ về"},
    
    59: {"Ten": "Phong Thủy Hoán", "Tuong": "Tan rã", "Cat_Hung": "Bình", "Luan": "Đồ phân tán, khó tìm đủ"},
    60: {"Ten": "Thủy Trạch Tiết", "Tuong": "Tiết chế", "Cat_Hung": "Bình", "Luan": "Cần kiên nhẫn, tiết chế"},
    61: {"Ten": "Phong Trạch Trung Phu", "Tuong": "Thành tín", "Cat_Hung": "Cát", "Luan": "Thành tâm sẽ tìm được"},
    62: {"Ten": "Lôi Sơn Tiểu Quá", "Tuong": "Hơi quá", "Cat_Hung": "Bình", "Luan": "Đừng nóng vội"},
    
    63: {"Ten": "Thủy Hỏa Ký Tế", "Tuong": "Đã xong", "Cat_Hung": "Cát", "Luan": "Việc đã định, sẽ tìm được"},
    64: {"Ten": "Hỏa Thủy Vị Tế", "Tuong": "Chưa xong", "Cat_Hung": "Bình", "Luan": "Còn phải cố gắng thêm"}
}

# ============================================================
# PHẦN 6: QUY TẮC LIÊN KẾT TỔNG HỢP
# ============================================================

def phan_tich_tim_do_chi_tiet(cung_data):
    """
    Phân tích CHI TIẾT việc tìm đồ mất dựa trên tất cả yếu tố trong cung
    Input: dict chứa thông tin cung {cung_so, can_thien, can_dia, sao, mon, than, tuong}
    Output: dict chứa kết luận chi tiết
    """
    ket_qua = {
        "huong": None,
        "khoang_cach": None,
        "gioi_tinh": None,
        "quen_la": None,
        "mau_sac": None,
        "kha_nang_tim": None,
        "dac_diem_ke_lay": [],
        "loi_khuyen": []
    }
    
    cung_so = cung_data.get("cung_so", 5)
    
    # 1. Hướng và Khoảng cách
    if cung_so in KHOANG_CACH_CHI_TIET:
        kc = KHOANG_CACH_CHI_TIET[cung_so]
        ket_qua["huong"] = kc["Mo_Ta"].split(",")[0] if "," in kc["Mo_Ta"] else kc["Mo_Ta"]
        ket_qua["khoang_cach"] = f"{kc['So_Met']} (khoảng {kc['So_Buoc']} bước)"
    
    # 2. Giới tính (dựa vào Can + Thần + Quái)
    can = cung_data.get("can_thien") or cung_data.get("can")
    than = cung_data.get("than")
    
    diem_nam = 0
    diem_nu = 0
    
    if can in ["Canh", "Mậu", "Nhâm", "Bính"]:
        diem_nam += 2
        ket_qua["dac_diem_ke_lay"].append(f"Can {can} = thiên về ĐÀN ÔNG")
    elif can in ["Ất", "Kỷ", "Quý", "Đinh"]:
        diem_nu += 2
        ket_qua["dac_diem_ke_lay"].append(f"Can {can} = thiên về PHỤ NỮ")
    
    if than in ["Huyền Vũ", "Bạch Hổ", "Cửu Thiên"]:
        diem_nam += 1
        ket_qua["dac_diem_ke_lay"].append(f"Thần {than} = thiên về ĐÀN ÔNG")
    elif than in ["Thái Âm", "Lục Hợp"]:
        diem_nu += 1
        ket_qua["dac_diem_ke_lay"].append(f"Thần {than} = thiên về PHỤ NỮ")
    
    if cung_so in [1, 3, 6, 8]:
        diem_nam += 1
    elif cung_so in [2, 4, 7, 9]:
        diem_nu += 1
    
    ket_qua["gioi_tinh"] = "ĐÀN ÔNG" if diem_nam > diem_nu else ("PHỤ NỮ" if diem_nu > diem_nam else "KHÔNG RÕ")
    
    # 3. Quen hay Lạ
    if than == "Huyền Vũ":
        ket_qua["quen_la"] = "NGƯỜI LẠ (90%) - Kẻ trộm chuyên nghiệp"
    elif than == "Bạch Hổ":
        ket_qua["quen_la"] = "NGƯỜI LẠ (95%) - Kẻ cướp hung bạo"
    elif than == "Thái Âm":
        ket_qua["quen_la"] = "NGƯỜI QUEN (70%) - Phụ nữ quen biết"
    elif than == "Lục Hợp":
        ket_qua["quen_la"] = "NGƯỜI QUEN (85%) - Bạn bè, người thân"
    elif cung_so == 5:
        ket_qua["quen_la"] = "NGƯỜI NHÀ (90%) - Đồ ngay trong nhà"
    else:
        ket_qua["quen_la"] = QUEN_LA_QUY_TAC.get(f"Cung_{cung_so}_Quen_La", "50% quen, 50% lạ")
    
    # 4. Màu sắc (dựa vào Ngũ Hành của Cung)
    ngu_hanh_map = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
    hanh = ngu_hanh_map.get(cung_so, "Thổ")
    mau_info = MAU_SAC_NGU_HANH.get(hanh, {})
    ket_qua["mau_sac"] = ", ".join(mau_info.get("Mau_Chinh", ["Không xác định"]))
    
    # 5. Khả năng tìm được (dựa vào Môn)
    mon = cung_data.get("mon", "").replace(" Môn", "") + " Môn"
    tim_info = KHA_NANG_LAY_LAI.get(mon, {})
    if tim_info:
        ket_qua["kha_nang_tim"] = f"{tim_info.get('Ty_Le', '50%')} - {tim_info.get('Ket_Luan', 'Trung bình')}"
    else:
        ket_qua["kha_nang_tim"] = "50% - Trung bình"
    
    # 6. Lời khuyên
    if "Đại Cát" in str(tim_info) or "85%" in str(tim_info):
        ket_qua["loi_khuyen"].append("Nên tìm ngay, khả năng cao lấy lại được")
    elif "Hung" in str(tim_info) or "5%" in str(tim_info):
        ket_qua["loi_khuyen"].append("Khả năng thấp, nên báo công an")
    
    if ket_qua["quen_la"] and "QUEN" in ket_qua["quen_la"]:
        ket_qua["loi_khuyen"].append("Hỏi người xung quanh, có thể ai đó biết")
    
    return ket_qua


# Export
__all__ = [
    'MAU_SAC_NGU_HANH', 'QUEN_LA_QUY_TAC', 'KHOANG_CACH_CHI_TIET',
    'KHA_NANG_LAY_LAI', 'QUE_64', 'phan_tich_tim_do_chi_tiet'
]

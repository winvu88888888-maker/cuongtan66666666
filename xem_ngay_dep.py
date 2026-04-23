"""
XEM NGÀY ĐẸP — Module tổng hợp từ 5 sách chuẩn:
1. Hiệp Kỷ Biện Phương Thư
2. Ngọc Hạp Thông Thư
3. Đổng Công Trạch Nhật
4. Thọ Mai Gia Lễ
5. Tam Giáo Chính Hội
"""
import datetime
import math

# ══════════════════════════════════════════════════════════════
# LỊCH ÂM — Thuật toán Hồ Ngọc Đức (chuẩn UTC+7 Việt Nam)
# ══════════════════════════════════════════════════════════════

def _jdn(dd, mm, yy):
    a = int((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    return dd + int((153*m+2)/5) + 365*y + int(y/4) - int(y/100) + int(y/400) - 32045

def _new_moon(k):
    T = k / 1236.85; T2 = T*T; T3 = T2*T; dr = math.pi/180
    Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3
    Jd1 += 0.00033*math.sin((166.56+132.87*T-0.009173*T2)*dr)
    M = 359.2242+29.10535608*k-0.0000333*T2-0.00000347*T3
    Mpr = 306.0253+385.81691806*k+0.0107306*T2+0.00001236*T3
    F = 21.2964+390.67050646*k-0.0016528*T2-0.00000239*T3
    C1 = (0.1734-0.000393*T)*math.sin(M*dr)+0.0021*math.sin(2*dr*M)
    C1 -= 0.4068*math.sin(Mpr*dr)+0.0161*math.sin(dr*2*Mpr)
    C1 -= 0.0004*math.sin(dr*3*Mpr)+0.0104*math.sin(dr*2*F)
    C1 -= 0.0051*math.sin(dr*(M+Mpr))-0.0074*math.sin(dr*(M-Mpr))
    C1 += 0.0004*math.sin(dr*(2*F+M))-0.0004*math.sin(dr*(2*F-M))
    C1 -= 0.0006*math.sin(dr*(2*F+Mpr))+0.001*math.sin(dr*(2*F-Mpr))
    C1 += 0.0005*math.sin(dr*(2*Mpr+M))
    return Jd1+C1 if T < -11 else Jd1+C1-0.000058868*k+0.0001178*T2

def _sun_longitude(jdn_val):
    T = (jdn_val-2451545.0)/36525; T2 = T*T; dr = math.pi/180
    M = 357.5291+35999.0503*T-0.0001559*T2
    L0 = 280.46645+36000.76983*T+0.0003032*T2
    DL = (1.9146-0.004817*T-0.000014*T2)*math.sin(dr*M)
    DL += (0.019993-0.000101*T)*math.sin(dr*2*M)+0.00029*math.sin(dr*3*M)
    L = (L0+DL)*dr; L -= math.pi*2*int(L/(math.pi*2))
    return int(L/math.pi*6)

def _get_lunar_month_11(yy, tz=7):
    off = _jdn(31,12,yy)-2415021; k = int(off/29.530588853)
    nm = _new_moon(k)
    if _sun_longitude(nm+tz/24.0) >= 9: nm = _new_moon(k-1)
    return int(nm+0.5+tz/24.0)

def _get_leap_month_offset(a11, tz=7):
    k = int((a11-2415021.076998695)/29.530588853+0.5)
    last = 0; i = 1; arc = _sun_longitude(_new_moon(k+i)+tz/24.0)
    while True:
        last = arc; i += 1; arc = _sun_longitude(_new_moon(k+i)+tz/24.0)
        if arc != last or i >= 14: break
    return i-1

def solar2lunar(dd, mm, yy, tz=7):
    """Chuyển dương lịch → âm lịch. Returns (ngày, tháng, năm, nhuận)."""
    day_number = _jdn(dd, mm, yy)
    k = int((day_number-2415021.076998695)/29.530588853)
    month_start = int(_new_moon(k)+0.5+tz/24.0)
    if month_start > day_number: month_start = int(_new_moon(k-1)+0.5+tz/24.0)
    a11 = _get_lunar_month_11(yy, tz); b11 = a11
    if a11 >= month_start:
        lunar_year = yy; a11 = _get_lunar_month_11(yy-1, tz)
    else:
        lunar_year = yy+1; b11 = _get_lunar_month_11(yy+1, tz)
    lunar_day = day_number-month_start+1
    diff = int((month_start-a11)/29+0.5); lunar_leap = 0; lunar_month = diff+11
    if b11-a11 > 365:
        leap_offset = _get_leap_month_offset(a11, tz)
        if diff >= leap_offset:
            lunar_month = diff+10
            if diff == leap_offset: lunar_leap = 1
    if lunar_month > 12: lunar_month -= 12
    if lunar_month >= 11 and diff < 4: lunar_year -= 1
    return (lunar_day, lunar_month, lunar_year, lunar_leap)


# ══════════════════════════════════════════════════════════════
# NHỊ THẬP BÁT TÚ (28 sao — Ngọc Hạp Thông Thư)
# ══════════════════════════════════════════════════════════════
NHI_THAP_BAT_TU = [
    ("Giác",  "Mộc", "Giao",  "Cát",  "🟢", "Tốt cho xây dựng, cưới hỏi, khai trương"),
    ("Cang",  "Kim", "Long",  "Hung", "🔴", "Kỵ cưới hỏi, an táng, xuất hành"),
    ("Đê",    "Thổ", "Mạc",   "Hung", "🔴", "Kỵ động thổ, cưới hỏi"),
    ("Phòng", "Nhật","Thố",   "Cát",  "🟢", "Tốt cho cưới hỏi, khai trương, xuất hành"),
    ("Tâm",   "Nguyệt","Hồ",  "Hung", "🔴", "Kỵ mọi việc lớn"),
    ("Vĩ",    "Hỏa", "Hổ",   "Cát",  "🟢", "Tốt cho cưới hỏi, xây nhà, khai trương"),
    ("Cơ",    "Thủy","Báo",   "Cát",  "🟢", "Tốt cho cầu tài, ký kết"),
    ("Đẩu",   "Mộc", "Giải",  "Cát",  "🟢", "Tốt cho khai trương, cầu tài"),
    ("Ngưu",  "Kim", "Ngưu",  "Hung", "🔴", "Kỵ cưới hỏi, xuất hành"),
    ("Nữ",    "Thổ", "Bức",   "Hung", "🔴", "Kỵ mọi việc"),
    ("Hư",    "Nhật","Thử",   "Hung", "🔴", "Kỵ mọi việc, đặc biệt cưới hỏi"),
    ("Nguy",  "Nguyệt","Yến", "Hung", "🔴", "Kỵ mọi việc lớn"),
    ("Thất",  "Hỏa", "Trư",  "Cát",  "🟢", "Tốt cho xây nhà, cưới hỏi"),
    ("Bích",  "Thủy","Du",    "Cát",  "🟢", "Tốt cho mọi việc, đặc biệt xây nhà"),
    ("Khuê",  "Mộc", "Lang",  "Hung", "🔴", "Kỵ mọi việc"),
    ("Lâu",   "Kim", "Cẩu",   "Cát",  "🟢", "Tốt cho cưới hỏi, khai trương"),
    ("Vị",    "Thổ", "Trĩ",   "Cát",  "🟢", "Tốt cho xây nhà, cưới hỏi, khai trương"),
    ("Mão",   "Nhật","Kê",    "Hung", "🔴", "Kỵ mọi việc lớn"),
    ("Tất",   "Nguyệt","Ô",   "Cát",  "🟢", "Tốt cho xây nhà, cưới hỏi, khai trương"),
    ("Chủy",  "Hỏa", "Hầu",  "Hung", "🔴", "Kỵ mọi việc"),
    ("Sâm",   "Thủy","Viên",  "Cát",  "🟢", "Tốt cho khai trương, cầu tài"),
    ("Tỉnh",  "Mộc", "Ngan",  "Cát",  "🟢", "Tốt cho mọi việc"),
    ("Quỷ",   "Kim", "Dương", "Hung", "🔴", "Kỵ mọi việc lớn"),
    ("Liễu",  "Thổ", "Chương","Hung", "🔴", "Kỵ mọi việc"),
    ("Tinh",  "Nhật","Mã",    "Hung", "🔴", "Kỵ an táng, cưới hỏi"),
    ("Trương", "Nguyệt","Lộc","Cát",  "🟢", "Tốt cho cưới hỏi, khai trương"),
    ("Dực",   "Hỏa", "Xà",   "Hung", "🔴", "Kỵ mọi việc"),
    ("Chẩn",  "Thủy","Giun",  "Cát",  "🟢", "Tốt cho xuất hành, cầu tài"),
]

# Ngày gốc: 1/1/1900 = sao Hư (index 10)
_28TU_GOC_JDN = _jdn(1, 1, 1900)
_28TU_GOC_IDX = 10  # Sao Hư

def tinh_28_tu(dd, mm, yy):
    """Tính Nhị Thập Bát Tú theo ngày dương lịch."""
    delta = _jdn(dd, mm, yy) - _28TU_GOC_JDN
    idx = (_28TU_GOC_IDX + delta) % 28
    return NHI_THAP_BAT_TU[idx]


# ══════════════════════════════════════════════════════════════
# DƯƠNG CÔNG KỴ NHẬT (13 ngày đại kỵ theo Ngọc Hạp Thông Thư)
# ══════════════════════════════════════════════════════════════
DUONG_CONG_KY = [
    (1,13), (2,11), (3,9), (4,7), (5,5), (6,3), (7,1), (7,29),
    (8,27), (9,25), (10,23), (11,21), (12,19)
]

def kiem_tra_duong_cong_ky(thang_am, ngay_am):
    """Kiểm tra Dương Công Kỵ Nhật (13 ngày đại kỵ trong năm)."""
    return (thang_am, ngay_am) in DUONG_CONG_KY


# ══════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════
CHI_12 = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

# ── 12 TRỰC (Đổng Công Trạch Nhật) ──
TRUC_12 = ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Chấp", "Phá", "Nguy", "Thành", "Thu", "Khai", "Bế"]

TRUC_TINH_CHAT = {
    "Kiến": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Khởi đầu, sinh sôi",
             "nen": ["Nhậm chức", "Xuất hành", "Cưới hỏi", "Động thổ", "Cầu tài"],
             "ky": ["Lợp nhà", "Đào ao", "Chôn cất"]},
    "Trừ": {"cat_hung": "Bình", "icon": "🟡", "mo_ta": "Loại bỏ cái xấu",
            "nen": ["Chữa bệnh", "Quét dọn", "Cúng tế", "Cầu an"],
            "ky": ["Ký kết", "Giao dịch", "Mở kho"]},
    "Mãn": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Đầy đủ, viên mãn",
            "nen": ["Cầu phúc", "Khai trương", "Nhập kho", "Cưới hỏi"],
            "ky": ["Chôn cất", "Kiện tụng"]},
    "Bình": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Bình yên, ổn định",
             "nen": ["Sửa sang", "Chăn nuôi", "Di chuyển", "Xây bếp"],
             "ky": ["Động thổ lớn", "Khai trương"]},
    "Định": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Cố định, vẹn toàn",
             "nen": ["Giao dịch", "Ký kết", "Cưới hỏi", "Xây chuồng"],
             "ky": ["Kiện tụng", "Xuất hành", "Chữa bệnh"]},
    "Chấp": {"cat_hung": "Bình", "icon": "🟡", "mo_ta": "Giữ gìn, duy trì",
             "nen": ["Thu nhận", "Học tập", "Xây dựng"],
             "ky": ["Đầu tư lớn", "Cho vay", "Mở kho"]},
    "Phá":  {"cat_hung": "Hung", "icon": "🔴", "mo_ta": "Phá bỏ, dỡ bỏ",
             "nen": ["Tháo dỡ", "Chữa bệnh", "Dọn dẹp"],
             "ky": ["Cưới hỏi", "Khai trương", "Ký kết", "Động thổ"]},
    "Nguy": {"cat_hung": "Hung", "icon": "🔴", "mo_ta": "Nguy hiểm, rủi ro",
             "nen": ["Việc nhỏ", "Cầu an"],
             "ky": ["Xuất hành", "Động thổ", "Di chuyển", "Leo trèo"]},
    "Thành": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Thành công, viên mãn",
              "nen": ["Cưới hỏi", "Khai trương", "Nhập học", "Ký kết"],
              "ky": ["Kiện tụng"]},
    "Thu":  {"cat_hung": "Hung", "icon": "🔴", "mo_ta": "Thu hoạch, kết thúc",
             "nen": ["Thu hoạch", "Mua bán", "Nhập kho"],
             "ky": ["Động thổ", "Chôn cất", "Đi xa"]},
    "Khai": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Mở mang, bắt đầu",
             "nen": ["Khai trương", "Khởi nghiệp", "Xây dựng", "Cưới hỏi"],
             "ky": ["An táng", "Cho vay"]},
    "Bế":  {"cat_hung": "Bình", "icon": "🟡", "mo_ta": "Bế tắc, kín đáo",
            "nen": ["Đóng kho", "Sửa chữa", "Nghỉ ngơi"],
            "ky": ["Khai trương", "Động thổ", "Việc lớn"]},
}

# ── HOÀNG ĐẠO / HẮC ĐẠO (12 SAO) ──
SAO_12 = [
    ("Thanh Long",  "Hoàng Đạo", "🐉", "Cát — thích hợp mọi việc lớn"),
    ("Minh Đường",  "Hoàng Đạo", "🏛️", "Cát — thuận lợi cầu tài, cưới hỏi"),
    ("Thiên Hình",  "Hắc Đạo",   "⚔️", "Hung — dễ gặp hình phạt, kiện tụng"),
    ("Chu Tước",    "Hắc Đạo",   "🐦", "Hung — thị phi, tranh cãi"),
    ("Kim Quỹ",     "Hoàng Đạo", "💰", "Cát — có lợi tiền bạc, kinh doanh"),
    ("Kim Đường",   "Hoàng Đạo", "🏆", "Cát — quý nhân phù trợ"),
    ("Bạch Hổ",     "Hắc Đạo",   "🐅", "Hung — tang tóc, thương tích"),
    ("Ngọc Đường",  "Hoàng Đạo", "🏯", "Cát — xây dựng, khởi nghiệp"),
    ("Thiên Lao",   "Hắc Đạo",   "🔒", "Hung — tù tội, trở ngại"),
    ("Nguyên Vũ",   "Hắc Đạo",   "🐢", "Hung — mất mát, trộm cắp"),
    ("Tư Mệnh",    "Hoàng Đạo", "📜", "Cát — làm ăn, thăng tiến"),
    ("Câu Trận",    "Hắc Đạo",   "🕸️", "Hung — vướng mắc, trì trệ"),
]

# Bảng khởi điểm Hoàng Đạo theo tháng âm (tháng 1-12)
# Tháng 1 khởi Thanh Long ở Tý, tháng 2 ở Dần, tháng 3 ở Thìn...
HD_KHOI_DIEM = {1: 0, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 0, 8: 2, 9: 4, 10: 6, 11: 8, 12: 10}

# ── TAM NƯƠNG (ngày âm lịch) ──
TAM_NUONG = [3, 7, 13, 18, 22, 27]

# ── SAO TỐT / SAO XẤU THEO CAN-CHI NGÀY ──
# Thiên Đức theo tháng âm
THIEN_DUC = {1: "Đinh", 2: "Khôn", 3: "Nhâm", 4: "Tân",
             5: "Càn", 6: "Giáp", 7: "Quý", 8: "Cấn",
             9: "Bính", 10: "Ất", 11: "Tốn", 12: "Canh"}

# Nguyệt Đức theo tháng âm (Can ngày)
NGUYET_DUC = {1: "Bính", 2: "Giáp", 3: "Nhâm", 4: "Canh",
              5: "Bính", 6: "Giáp", 7: "Nhâm", 8: "Canh",
              9: "Bính", 10: "Giáp", 11: "Nhâm", 12: "Canh"}

# ── TRÙNG TANG (Thọ Mai Gia Lễ) ──
# Kết quả cung: Dần/Thân/Tỵ/Hợi = Trùng Tang, Tý/Ngọ/Mão/Dậu = Thiên Di, Thìn/Tuất/Sửu/Mùi = Nhập Mộ
TRUNG_TANG_CUNG = {
    "Dần": "TRÙNG TANG", "Thân": "TRÙNG TANG", "Tỵ": "TRÙNG TANG", "Hợi": "TRÙNG TANG",
    "Tý": "THIÊN DI", "Ngọ": "THIÊN DI", "Mão": "THIÊN DI", "Dậu": "THIÊN DI",
    "Thìn": "NHẬP MỘ", "Tuất": "NHẬP MỘ", "Sửu": "NHẬP MỘ", "Mùi": "NHẬP MỘ",
}

# ── CATEGORIES VIỆC XEM NGÀY ──
VIEC_XEM_NGAY = {
    "cuoi_hoi": {"ten": "💒 Cưới Hỏi", "truc_tot": ["Kiến", "Mãn", "Định", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Thu", "Bế"]},
    "lam_nha": {"ten": "🏠 Làm Nhà / Động Thổ", "truc_tot": ["Kiến", "Mãn", "Bình", "Định", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "xuat_hanh": {"ten": "🚀 Xuất Hành", "truc_tot": ["Kiến", "Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Định", "Bế"]},
    "an_tang": {"ten": "⚰️ An Táng / Chôn Cất", "truc_tot": ["Mãn", "Bình", "Định", "Thành"], "truc_xau": ["Kiến", "Phá", "Thu", "Khai"]},
    "tao_mo": {"ten": "🪦 Tảo Mộ / Sửa Mộ", "truc_tot": ["Mãn", "Bình", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy"]},
    "boc_mo": {"ten": "🏺 Bốc Mộ / Cải Táng", "truc_tot": ["Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế", "Thu"]},
    "khai_truong": {"ten": "🏪 Khai Trương", "truc_tot": ["Kiến", "Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "ky_ket": {"ten": "📝 Ký Kết / Giao Dịch", "truc_tot": ["Định", "Thành", "Khai", "Mãn"], "truc_xau": ["Phá", "Nguy", "Trừ"]},
    "cung_te": {"ten": "🙏 Cúng Tế / Lễ Bái", "truc_tot": ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Thành", "Khai"], "truc_xau": ["Phá"]},
    "cau_tai": {"ten": "💰 Cầu Tài / Xin Việc", "truc_tot": ["Kiến", "Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "don_nha": {"ten": "🔀 Dọn Nhà / Nhập Trạch", "truc_tot": ["Kiến", "Mãn", "Bình", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "chua_benh": {"ten": "⚕️ Chữa Bệnh / Phẫu Thuật", "truc_tot": ["Trừ", "Phá", "Khai"], "truc_xau": ["Nguy", "Bế", "Định"]},
}


# ══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════

def tinh_truc(thang_am, chi_ngay):
    """Tính Trực theo tháng âm + chi ngày (Đổng Công Trạch Nhật).
    Quy tắc: Tháng 1 khởi Kiến ở Dần, Tháng 2 khởi Kiến ở Mão...
    """
    chi_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else 0
    # Tháng 1: Kiến ở Dần (index 2), Tháng 2: Kiến ở Mão (index 3)...
    khoi = (thang_am + 1) % 12  # Tháng 1 -> khởi ở chi index 2 (Dần)
    offset = (chi_idx - khoi) % 12
    truc = TRUC_12[offset]
    return truc


def tinh_hoang_dao(thang_am, chi_ngay):
    """Tính sao Hoàng Đạo/Hắc Đạo theo tháng âm + chi ngày.
    Returns: (tên sao, loại HD/HĐ, icon, mô tả)
    """
    chi_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else 0
    khoi = HD_KHOI_DIEM.get(thang_am, 0)
    sao_idx = (chi_idx - khoi) % 12
    return SAO_12[sao_idx]


def kiem_tra_tam_nuong(ngay_am):
    """Kiểm tra ngày Tam Nương (3, 7, 13, 18, 22, 27 âm lịch)."""
    return ngay_am in TAM_NUONG


def kiem_tra_nguyet_pha(thang_am, chi_ngay):
    """Nguyệt Phá: Chi ngày XUNG Chi tháng.
    Tháng 1=Dần, Chi xung: cách 6 vị trí.
    """
    chi_thang_idx = (thang_am + 1) % 12  # Tháng 1 = Dần (idx 2)
    chi_ngay_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else -1
    return (chi_ngay_idx - chi_thang_idx) % 12 == 6


def kiem_tra_thien_duc(thang_am, can_ngay):
    """Kiểm tra ngày có Thiên Đức không."""
    td = THIEN_DUC.get(thang_am, "")
    return can_ngay == td


def kiem_tra_nguyet_duc(thang_am, can_ngay):
    """Kiểm tra ngày có Nguyệt Đức không."""
    nd = NGUYET_DUC.get(thang_am, "")
    return can_ngay == nd


def tinh_trung_tang(tuoi_mat, gioi_tinh, nam_mat, thang_mat, ngay_mat, gio_mat):
    """Tính Trùng Tang theo Thọ Mai Gia Lễ.
    tuoi_mat: tuổi âm lịch (số)
    gioi_tinh: 'nam' hoặc 'nu'
    Returns: dict với kết quả từng trụ
    """
    if gioi_tinh == 'nam':
        khoi = CHI_12.index("Dần")  # 2
        huong = 1  # thuận
    else:
        khoi = CHI_12.index("Thân")  # 8
        huong = -1  # nghịch

    ket_qua = {}
    # Đếm theo tuổi qua 4 trụ: Năm -> Tháng -> Ngày -> Giờ
    tru_values = [nam_mat, thang_mat, ngay_mat, gio_mat]
    tru_names = ["Năm", "Tháng", "Ngày", "Giờ"]

    pos = khoi
    for i, (val, name) in enumerate(zip(tru_values, tru_names)):
        # Đếm val bước
        steps = (val - 1) if val > 0 else 0
        pos = (pos + huong * steps) % 12
        cung = CHI_12[pos]
        loai = TRUNG_TANG_CUNG.get(cung, "KHÔNG RÕ")
        ket_qua[name] = {"cung": cung, "loai": loai}

    # Kết luận tổng
    trung_count = sum(1 for v in ket_qua.values() if v["loai"] == "TRÙNG TANG")
    if trung_count >= 2:
        ket_qua["ket_luan"] = "🔴 TRÙNG TANG NẶNG — Cần hóa giải!"
    elif trung_count == 1:
        ket_qua["ket_luan"] = "🟡 CÓ TRÙNG TANG — Nên cẩn trọng"
    else:
        nhap_mo = sum(1 for v in ket_qua.values() if isinstance(v, dict) and v.get("loai") == "NHẬP MỘ")
        if nhap_mo >= 2:
            ket_qua["ket_luan"] = "🟢 NHẬP MỘ — An nghỉ vĩnh viễn, tốt"
        else:
            ket_qua["ket_luan"] = "🟢 KHÔNG TRÙNG TANG — An toàn"

    return ket_qua


def danh_gia_ngay(thang_am, ngay_am, can_ngay, chi_ngay, loai_viec="cuoi_hoi", ngay_dl=None):
    """Đánh giá tổng hợp một ngày cho một loại việc cụ thể.
    ngay_dl: (dd, mm, yy) dương lịch — dùng cho 28 Tú + Dương Công Kỵ
    Returns: dict với tất cả thông tin
    """
    truc = tinh_truc(thang_am, chi_ngay)
    truc_info = TRUC_TINH_CHAT.get(truc, {})
    sao = tinh_hoang_dao(thang_am, chi_ngay)
    is_hoang_dao = sao[1] == "Hoàng Đạo"
    is_tam_nuong = kiem_tra_tam_nuong(ngay_am)
    is_nguyet_pha = kiem_tra_nguyet_pha(thang_am, chi_ngay)
    has_thien_duc = kiem_tra_thien_duc(thang_am, can_ngay)
    has_nguyet_duc = kiem_tra_nguyet_duc(thang_am, can_ngay)
    is_duong_cong_ky = kiem_tra_duong_cong_ky(thang_am, ngay_am)

    # 28 Tú
    sao_28 = None
    if ngay_dl:
        sao_28 = tinh_28_tu(ngay_dl[0], ngay_dl[1], ngay_dl[2])

    viec = VIEC_XEM_NGAY.get(loai_viec, VIEC_XEM_NGAY["cuoi_hoi"])
    truc_tot_cho_viec = truc in viec["truc_tot"]
    truc_xau_cho_viec = truc in viec["truc_xau"]

    # ── TÍNH ĐIỂM ──
    diem = 50  # Baseline
    ly_do_tot = []
    ly_do_xau = []

    # Hoàng Đạo
    if is_hoang_dao:
        diem += 20
        ly_do_tot.append(f"✅ Ngày Hoàng Đạo — {sao[0]} {sao[2]}")
    else:
        diem -= 15
        ly_do_xau.append(f"❌ Ngày Hắc Đạo — {sao[0]} {sao[2]}")

    # 12 Trực
    if truc_tot_cho_viec:
        diem += 20
        ly_do_tot.append(f"✅ Trực {truc} — {truc_info.get('mo_ta', '')} — TỐT cho {viec['ten']}")
    elif truc_xau_cho_viec:
        diem -= 25
        ly_do_xau.append(f"❌ Trực {truc} — {truc_info.get('mo_ta', '')} — XẤU cho {viec['ten']}")

    # 28 Tú
    if sao_28:
        if sao_28[3] == "Cát":
            diem += 10
            ly_do_tot.append(f"✅ Sao {sao_28[0]} ({sao_28[1]}/{sao_28[2]}) — {sao_28[5]}")
        else:
            diem -= 10
            ly_do_xau.append(f"❌ Sao {sao_28[0]} ({sao_28[1]}/{sao_28[2]}) — {sao_28[5]}")

    # Tam Nương
    if is_tam_nuong:
        diem -= 20
        ly_do_xau.append(f"❌ Ngày Tam Nương (ngày {ngay_am} âm lịch) — Kiêng kỵ việc lớn")

    # Nguyệt Phá
    if is_nguyet_pha:
        diem -= 30
        ly_do_xau.append("❌ Ngày NGUYỆT PHÁ — Xung tháng, mọi việc dễ đổ vỡ!")

    # Dương Công Kỵ
    if is_duong_cong_ky:
        diem -= 25
        ly_do_xau.append("❌ Ngày DƯƠNG CÔNG KỴ — 13 ngày đại kỵ trong năm!")

    # Thiên Đức / Nguyệt Đức
    if has_thien_duc:
        diem += 15
        ly_do_tot.append("✅ Có sao THIÊN ĐỨC — Hóa giải hung, đại cát!")
    if has_nguyet_duc:
        diem += 15
        ly_do_tot.append("✅ Có sao NGUYỆT ĐỨC — May mắn, thuận lợi!")

    # Clamp
    diem = max(0, min(100, diem))

    # Verdict
    if diem >= 80:
        verdict = "🟢 NGÀY RẤT ĐẸP"
        verdict_color = "#22c55e"
    elif diem >= 60:
        verdict = "🟢 NGÀY TỐT"
        verdict_color = "#86efac"
    elif diem >= 40:
        verdict = "🟡 NGÀY BÌNH THƯỜNG"
        verdict_color = "#fbbf24"
    elif diem >= 20:
        verdict = "🟠 NGÀY XẤU"
        verdict_color = "#f97316"
    else:
        verdict = "🔴 NGÀY RẤT XẤU"
        verdict_color = "#ef4444"

    return {
        "diem": diem,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "truc": truc,
        "truc_info": truc_info,
        "sao_hoang_dao": sao,
        "is_hoang_dao": is_hoang_dao,
        "is_tam_nuong": is_tam_nuong,
        "is_nguyet_pha": is_nguyet_pha,
        "is_duong_cong_ky": is_duong_cong_ky,
        "has_thien_duc": has_thien_duc,
        "has_nguyet_duc": has_nguyet_duc,
        "truc_tot_cho_viec": truc_tot_cho_viec,
        "truc_xau_cho_viec": truc_xau_cho_viec,
        "ly_do_tot": ly_do_tot,
        "ly_do_xau": ly_do_xau,
        "loai_viec": viec["ten"],
        "can_ngay": can_ngay,
        "chi_ngay": chi_ngay,
        "thang_am": thang_am,
        "ngay_am": ngay_am,
        "sao_28_tu": sao_28,
    }


def danh_gia_ngay_duong_lich(dd, mm, yy, can_ngay, chi_ngay, loai_viec="cuoi_hoi"):
    """Convenience: Nhận ngày dương lịch, tự chuyển âm lịch rồi đánh giá."""
    ngay_am, thang_am, _, _ = solar2lunar(dd, mm, yy)
    return danh_gia_ngay(thang_am, ngay_am, can_ngay, chi_ngay, loai_viec, ngay_dl=(dd, mm, yy))


def tim_ngay_dep(thang_am, can_chi_list, loai_viec="cuoi_hoi", top_n=5):
    """Tìm N ngày đẹp nhất từ danh sách can-chi.
    can_chi_list: [(ngay_am, can, chi), ...]
    Returns: sorted list of results
    """
    results = []
    for ngay_am, can, chi in can_chi_list:
        r = danh_gia_ngay(thang_am, ngay_am, can, chi, loai_viec)
        results.append(r)
    results.sort(key=lambda x: x["diem"], reverse=True)
    return results[:top_n]


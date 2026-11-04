"""
TỬ VI ĐẨU SỐ — Module lập lá số & luận giải
Tính: Mệnh Cung, Thân Cung, Cục, 14 Chính Tinh, Đại Hạn, Lưu Niên
"""

CAN = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
NGU_HANH = ["Kim","Thủy","Hỏa","Thổ","Mộc"]

# 12 Cung Tử Vi
CUNG_12 = ["Mệnh","Phụ Mẫu","Phúc Đức","Điền Trạch","Quan Lộc","Nô Bộc",
           "Thiên Di","Tật Ách","Tài Bạch","Tử Tức","Phu Thê","Huynh Đệ"]

# 14 Chính Tinh
CHINH_TINH_14 = ["Tử Vi","Thiên Cơ","Thái Dương","Vũ Khúc","Thiên Đồng","Liêm Trinh",
                 "Thiên Phủ","Thái Âm","Tham Lang","Cự Môn","Thiên Tướng","Thiên Lương","Thất Sát","Phá Quân"]

# Bảng Cục theo Can năm + Cung Mệnh (Chi)
# Can: 0=Giáp,1=Ất...  Cục: 2=Thủy nhị cục, 3=Mộc tam cục, 4=Kim tứ cục, 5=Thổ ngũ cục, 6=Hỏa lục cục
CUC_BANG = {
    # (can%5, chi_menh%6) -> cục số
    0: {0:6, 1:6, 2:5, 3:5, 4:4, 5:4},  # Giáp/Kỷ
    1: {0:6, 1:6, 2:5, 3:5, 4:4, 5:4},
    2: {0:2, 1:2, 2:3, 3:3, 4:4, 5:4},  # Bính/Tân
    3: {0:2, 1:2, 2:3, 3:3, 4:4, 5:4},
    4: {0:4, 1:4, 2:5, 3:5, 4:6, 5:6},  # Mậu/Quý
}

CUC_TEN = {2:"Thủy Nhị Cục",3:"Mộc Tam Cục",4:"Kim Tứ Cục",5:"Thổ Ngũ Cục",6:"Hỏa Lục Cục"}

# Bảng an Tử Vi theo Cục + ngày âm lịch (simplified mapping)
# Vị trí Tử Vi = (ngày - 1) / cục_số, mapped to 12 chi
def _vi_tri_tu_vi(ngay_am, cuc_so):
    if cuc_so == 0: cuc_so = 2
    pos = ((ngay_am - 1) // cuc_so) % 12
    remainder = (ngay_am - 1) % cuc_so
    if remainder > 0:
        pos = (pos + 1) % 12
    return pos

# Nhóm Tử Vi (6 sao đi cùng Tử Vi)
_TV_GROUP_OFFSETS = {
    "Tử Vi": 0, "Thiên Cơ": -1, "Thái Dương": -3,
    "Vũ Khúc": -4, "Thiên Đồng": -5, "Liêm Trinh": -8
}
# Nhóm Thiên Phủ (8 sao)
_TP_GROUP_OFFSETS = {
    "Thiên Phủ": 0, "Thái Âm": 1, "Tham Lang": 2, "Cự Môn": 3,
    "Thiên Tướng": 4, "Thiên Lương": 5, "Thất Sát": 6, "Phá Quân": 10
}

# Tính Ngũ Hành Nạp Âm
NAP_AM = [
    "Hải Trung Kim","Lư Trung Hỏa","Đại Lâm Mộc","Lộ Bàng Thổ","Kiếm Phong Kim","Sơn Đầu Hỏa",
    "Giản Hạ Thủy","Thành Đầu Thổ","Bạch Lạp Kim","Dương Liễu Mộc","Tuyền Trung Thủy","Ốc Thượng Thổ",
    "Tích Lịch Hỏa","Tùng Bách Mộc","Trường Lưu Thủy","Sa Trung Kim","Sơn Hạ Hỏa","Bình Địa Mộc",
    "Bích Thượng Thổ","Kim Bạch Kim","Phú Đăng Hỏa","Thiên Hà Thủy","Đại Trạch Thổ","Thoa Xuyến Kim",
    "Tang Đố Mộc","Đại Khê Thủy","Sa Trung Thổ","Thiên Thượng Hỏa","Thạch Lựu Mộc","Đại Hải Thủy"
]

def nap_am(nam_sinh):
    idx = ((nam_sinh - 4) // 2) % 30
    return NAP_AM[idx]

def can_chi_nam(nam):
    return CAN[(nam-4)%10], CHI[(nam-4)%12]

def tinh_menh_cung(thang_am, gio_chi_idx):
    """Mệnh cung = Dần + (tháng-1) - (giờ - Tý). Kết quả là index trong CHI."""
    return (2 + thang_am - 1 - gio_chi_idx) % 12

def tinh_than_cung(menh_cung_idx, gio_chi_idx):
    """Thân cung = Mệnh cung + 2*giờ."""
    return (menh_cung_idx + 2 * gio_chi_idx) % 12

def tinh_cuc(can_nam, menh_chi_idx):
    can_idx = CAN.index(can_nam) if can_nam in CAN else 0
    group = can_idx % 5
    chi_group = menh_chi_idx % 6
    # Simplified cuc mapping
    bang = {
        0: [6,6,5,5,4,4], 1: [6,6,5,5,4,4],
        2: [2,2,3,3,4,4], 3: [2,2,3,3,4,4],
        4: [4,4,5,5,6,6]
    }
    return bang.get(group, [2,2,3,3,4,4])[chi_group]

def lap_la_so(nam_sinh, thang_am, ngay_am, gio_idx, gioi_tinh='nam'):
    """Lập lá số Tử Vi đầy đủ.
    gio_idx: 0=Tý, 1=Sửu, ..., 11=Hợi
    Returns: dict với toàn bộ thông tin lá số
    """
    can_n, chi_n = can_chi_nam(nam_sinh)
    can_idx = CAN.index(can_n)

    # Mệnh & Thân
    menh_idx = tinh_menh_cung(thang_am, gio_idx)
    than_idx = tinh_than_cung(menh_idx, gio_idx)

    # Cục
    cuc = tinh_cuc(can_n, menh_idx)
    cuc_ten = CUC_TEN.get(cuc, f"Cục {cuc}")

    # Nạp Âm
    na = nap_am(nam_sinh)

    # 12 Cung
    cung_map = {}
    for i, ten_cung in enumerate(CUNG_12):
        chi_idx = (menh_idx + 12 - i) % 12  # Đi ngược
        cung_map[ten_cung] = {
            "chi": CHI[chi_idx], "chi_idx": chi_idx,
            "chinh_tinh": [], "phu_tinh": [],
            "dai_han": None
        }

    # An Tử Vi + nhóm
    tv_pos = _vi_tri_tu_vi(ngay_am, cuc)
    for star, offset in _TV_GROUP_OFFSETS.items():
        pos = (tv_pos + offset) % 12
        for cung_name, cung_data in cung_map.items():
            if cung_data["chi_idx"] == pos:
                cung_data["chinh_tinh"].append(star)

    # An Thiên Phủ + nhóm
    tp_pos = (12 - tv_pos + 4) % 12  # Thiên Phủ đối xứng Tử Vi qua trục Dần-Thân
    for star, offset in _TP_GROUP_OFFSETS.items():
        pos = (tp_pos + offset) % 12
        for cung_name, cung_data in cung_map.items():
            if cung_data["chi_idx"] == pos:
                cung_data["chinh_tinh"].append(star)

    # Dương/Âm nam (cần cho Trường Sinh + Đại Hạn)
    duong_nam = (gioi_tinh == 'nam' and can_idx % 2 == 0) or (gioi_tinh == 'nu' and can_idx % 2 == 1)

    # Phụ tinh — Lộc Tồn + Kình/Đà
    loc_ton_map = [2,3,5,6,5,6,8,9,11,0]
    loc_ton_pos = loc_ton_map[can_idx]
    kinh_pos = (loc_ton_pos + 1) % 12
    da_la_pos = (loc_ton_pos - 1) % 12

    # Văn Xương/Khúc theo giờ
    van_xuong_pos = (10 - gio_idx) % 12
    van_khuc_pos = (gio_idx + 4) % 12

    # Tả Phụ/Hữu Bật theo tháng
    ta_phu_pos = (thang_am + 3) % 12
    huu_bat_pos = (11 - thang_am) % 12

    # Thiên Khôi/Thiên Việt (Quý Nhân) theo Can năm
    khoi_map = [1,0,11,11,1,0,1,6,3,3]  # Giáp=Sửu,...
    viet_map = [7,8,9,9,7,8,7,2,5,5]
    thien_khoi_pos = khoi_map[can_idx]
    thien_viet_pos = viet_map[can_idx]

    # Hỏa Tinh theo Chi năm + giờ
    chi_nam_idx = CHI.index(chi_n)
    hoa_tinh_base = [2,3,1,9]  # Dần/Ngọ/Tuất=Dần, Thân/Tý/Thìn=Mão, Tỵ/Dậu/Sửu=Sửu, Hợi/Mão/Mùi=Dậu
    hoa_group = chi_nam_idx % 4
    hoa_tinh_pos = (hoa_tinh_base[hoa_group] + gio_idx) % 12

    # Linh Tinh theo Chi năm + giờ
    linh_base = [10,10,3,10]
    linh_tinh_pos = (linh_base[hoa_group] + gio_idx) % 12

    # Địa Không/Địa Kiếp theo giờ
    dia_khong_pos = (11 - gio_idx) % 12
    dia_kiep_pos = (gio_idx + 1) % 12

    # Thiên Mã theo Chi năm
    thien_ma_map = {0:2, 1:11, 2:8, 3:5, 4:2, 5:11, 6:8, 7:5, 8:2, 9:11, 10:8, 11:5}
    thien_ma_pos = thien_ma_map[chi_nam_idx]

    # Đào Hoa theo Chi năm
    dao_hoa_map = {0:9, 1:6, 2:3, 3:0, 4:9, 5:6, 6:3, 7:0, 8:9, 9:6, 10:3, 11:0}
    dao_hoa_pos = dao_hoa_map[chi_nam_idx]

    # Hồng Loan theo Chi năm
    hong_loan_pos = (3 - chi_nam_idx) % 12
    # Thiên Hỷ = Hồng Loan + 6
    thien_hi_pos = (hong_loan_pos + 6) % 12

    # Cô Thần/Quả Tú theo Chi năm
    co_than_map = [2,2,5,5,5,8,8,8,11,11,11,2]
    qua_tu_map = [10,10,1,1,1,4,4,4,7,7,7,10]
    co_than_pos = co_than_map[chi_nam_idx]
    qua_tu_pos = qua_tu_map[chi_nam_idx]

    # Long Trì/Phượng Các theo Chi năm
    long_tri_pos = (chi_nam_idx + 4) % 12
    phuong_cac_pos = (8 - chi_nam_idx) % 12

    # Thiên Khốc/Thiên Hư theo Chi năm
    thien_khoc_pos = (6 + chi_nam_idx) % 12
    thien_hu_pos = (6 - chi_nam_idx) % 12

    # Thiên Quan/Thiên Phúc theo Can năm
    thien_quan_map = [7,4,1,2,3,9,11,9,3,6]
    thien_phuc_map = [9,8,0,11,3,2,6,5,6,5]
    thien_quan_pos = thien_quan_map[can_idx]
    thien_phuc_pos = thien_phuc_map[can_idx]

    # Tang Môn/Bạch Hổ/Quan Phù/Điếu Khách theo Chi năm
    tang_mon_pos = (chi_nam_idx + 2) % 12
    bach_ho_pos = (chi_nam_idx + 4) % 12
    quan_phu_pos = (chi_nam_idx + 6) % 12
    dieu_khach_pos = (chi_nam_idx + 8) % 12

    # Thai/Tọa theo tháng
    thai_pos = (thang_am + 1) % 12
    toa_pos = (thang_am + 11) % 12

    # Trường Sinh 12 cung theo Cục
    TRUONG_SINH_12 = ["Trường Sinh","Mộc Dục","Quan Đới","Lâm Quan","Đế Vượng",
                      "Suy","Bệnh","Tử","Mộ","Tuyệt","Thai","Dưỡng"]
    ts_khoi = {2:8, 3:11, 4:5, 5:8, 6:2}  # Thủy=Thân, Mộc=Hợi, Kim=Tỵ, Thổ=Thân, Hỏa=Dần
    ts_start = ts_khoi.get(cuc, 2)
    ts_step = 1 if duong_nam else -1

    truong_sinh = {}
    for i, ts_name in enumerate(TRUONG_SINH_12):
        ts_pos = (ts_start + ts_step * i) % 12
        truong_sinh[ts_name] = ts_pos

    # Tổng hợp phụ tinh
    phu_tinh_list = [
        ("Lộc Tồn", loc_ton_pos), ("Kình Dương", kinh_pos), ("Đà La", da_la_pos),
        ("Văn Xương", van_xuong_pos), ("Văn Khúc", van_khuc_pos),
        ("Tả Phụ", ta_phu_pos), ("Hữu Bật", huu_bat_pos),
        ("Thiên Khôi", thien_khoi_pos), ("Thiên Việt", thien_viet_pos),
        ("Hỏa Tinh", hoa_tinh_pos), ("Linh Tinh", linh_tinh_pos),
        ("Địa Không", dia_khong_pos), ("Địa Kiếp", dia_kiep_pos),
        ("Thiên Mã", thien_ma_pos), ("Đào Hoa", dao_hoa_pos),
        ("Hồng Loan", hong_loan_pos), ("Thiên Hỷ", thien_hi_pos),
        ("Cô Thần", co_than_pos), ("Quả Tú", qua_tu_pos),
        ("Long Trì", long_tri_pos), ("Phượng Các", phuong_cac_pos),
        ("Thiên Khốc", thien_khoc_pos), ("Thiên Hư", thien_hu_pos),
        ("Thiên Quan", thien_quan_pos), ("Thiên Phúc", thien_phuc_pos),
        ("Tang Môn", tang_mon_pos), ("Bạch Hổ", bach_ho_pos),
        ("Quan Phù", quan_phu_pos), ("Điếu Khách", dieu_khach_pos),
        ("Thai", thai_pos), ("Tọa", toa_pos),
    ]
    # Trường Sinh vào phụ tinh
    for ts_name, ts_pos in truong_sinh.items():
        phu_tinh_list.append((ts_name, ts_pos))

    for star_name, pos in phu_tinh_list:
        for cung_data in cung_map.values():
            if cung_data["chi_idx"] == pos:
                cung_data["phu_tinh"].append(star_name)

    # Tứ Hóa theo Can năm
    TU_HOA = {
        0: ("Liêm Trinh","Phá Quân","Vũ Khúc","Thái Dương"),    # Giáp
        1: ("Thiên Cơ","Thiên Lương","Tử Vi","Thái Âm"),          # Ất
        2: ("Thiên Đồng","Thiên Cơ","Văn Xương","Liêm Trinh"),    # Bính
        3: ("Thái Âm","Thiên Đồng","Thiên Cơ","Cự Môn"),          # Đinh
        4: ("Tham Lang","Thái Âm","Hữu Bật","Thiên Cơ"),          # Mậu
        5: ("Vũ Khúc","Tham Lang","Thiên Lương","Văn Khúc"),      # Kỷ
        6: ("Thái Dương","Vũ Khúc","Thái Âm","Thiên Đồng"),       # Canh
        7: ("Cự Môn","Thái Dương","Văn Khúc","Văn Xương"),        # Tân
        8: ("Thiên Lương","Tử Vi","Tả Phụ","Vũ Khúc"),            # Nhâm
        9: ("Phá Quân","Cự Môn","Thái Âm","Tham Lang"),           # Quý
    }
    hoa_loc, hoa_quyen, hoa_khoa, hoa_ky = TU_HOA.get(can_idx, ("","","",""))

    # Đại Hạn (10 năm 1 hạn)
    dai_han = []
    step = 1 if duong_nam else -1
    for i in range(12):
        start = cuc + i * 10
        end = start + 9
        han_chi_idx = (menh_idx + step * i) % 12
        cung_ten = ""
        for cn, cd in cung_map.items():
            if cd["chi_idx"] == han_chi_idx:
                cung_ten = cn
                break
        dai_han.append({
            "tu": start, "den": end,
            "tuoi_range": f"{start}-{end}",
            "cung": cung_ten,
            "chi": CHI[han_chi_idx]
        })

    # Lưu Niên (năm hiện tại)
    import datetime
    nam_hien_tai = datetime.date.today().year
    tuoi_hien_tai = nam_hien_tai - nam_sinh + 1
    luu_nien_chi_idx = (nam_hien_tai - 4) % 12
    luu_nien_cung = ""
    for cn, cd in cung_map.items():
        if cd["chi_idx"] == luu_nien_chi_idx:
            luu_nien_cung = cn
            break

    return {
        "nam_sinh": nam_sinh,
        "thang_am": thang_am,
        "ngay_am": ngay_am,
        "gio": CHI[gio_idx],
        "can_nam": can_n,
        "chi_nam": chi_n,
        "nap_am": na,
        "menh_cung": {"chi": CHI[menh_idx], "idx": menh_idx},
        "than_cung": {"chi": CHI[than_idx], "idx": than_idx},
        "cuc": cuc,
        "cuc_ten": cuc_ten,
        "cung_map": cung_map,
        "tu_hoa": {"Hóa Lộc": hoa_loc, "Hóa Quyền": hoa_quyen, "Hóa Khoa": hoa_khoa, "Hóa Kỵ": hoa_ky},
        "dai_han": dai_han,
        "luu_nien": {"nam": nam_hien_tai, "tuoi": tuoi_hien_tai, "cung": luu_nien_cung, "chi": CHI[luu_nien_chi_idx]},
        "gioi_tinh": gioi_tinh,
    }


def format_la_so_text(ls):
    """Format lá số thành text để gửi cho AI."""
    lines = []
    lines.append(f"═══ LÁ SỐ TỬ VI ĐẨU SỐ ═══")
    lines.append(f"Sinh: {ls['ngay_am']}/{ls['thang_am']} ÂL, Năm {ls['can_nam']} {ls['chi_nam']} ({ls['nam_sinh']})")
    lines.append(f"Giờ: {ls['gio']} | Giới tính: {ls['gioi_tinh']}")
    lines.append(f"Nạp Âm: {ls['nap_am']}")
    lines.append(f"Mệnh Cung: {ls['menh_cung']['chi']} | Thân Cung: {ls['than_cung']['chi']}")
    lines.append(f"Cục: {ls['cuc_ten']}")
    lines.append(f"Tứ Hóa: Lộc={ls['tu_hoa']['Hóa Lộc']}, Quyền={ls['tu_hoa']['Hóa Quyền']}, Khoa={ls['tu_hoa']['Hóa Khoa']}, Kỵ={ls['tu_hoa']['Hóa Kỵ']}")
    lines.append("")
    lines.append("── 12 CUNG ──")
    for cung_name, data in ls['cung_map'].items():
        stars = ", ".join(data['chinh_tinh']) if data['chinh_tinh'] else "—"
        phu = ", ".join(data['phu_tinh']) if data['phu_tinh'] else ""
        phu_str = f" + [{phu}]" if phu else ""
        lines.append(f"  {cung_name} ({data['chi']}): {stars}{phu_str}")
    lines.append("")
    lines.append("── ĐẠI HẠN ──")
    for dh in ls['dai_han']:
        lines.append(f"  Tuổi {dh['tuoi_range']}: Cung {dh['cung']} ({dh['chi']})")
    lines.append("")
    lines.append(f"── LƯU NIÊN {ls['luu_nien']['nam']} ──")
    lines.append(f"  Tuổi {ls['luu_nien']['tuoi']}: Cung {ls['luu_nien']['cung']} ({ls['luu_nien']['chi']})")
    return "\n".join(lines)

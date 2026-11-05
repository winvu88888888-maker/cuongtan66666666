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

    _ls_res = {
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
    _ls_res["thien_ky_13_chieu"] = analyze_thien_ky_13_dimensions(_ls_res)
    return _ls_res


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
    if ls.get("thien_ky_13_chieu"):
        lines.append("")
        lines.append("── TINH HOA KHO TỬ VI 56.6GB GITHUB (Renhuai123/ziwei-doushu — NGHÊ HẢI HẠ《THIÊN KỶ》13 CHIỀU) ──")
        for k_dim, v_dim in ls["thien_ky_13_chieu"].items():
            lines.append(f"  • [{k_dim}]: {v_dim}")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# TINH HOA KHO TÀNG TỬ VI 56.6GB TRÊN GITHUB (Renhuai123/ziwei-doushu v4.0)
# Hệ thống Nghê Hải Hạ《Thiên Kỷ · Tử Vi Đẩu Số》&《Tử Vi Đẩu Số Toàn Thư》
# (674,976 Mệnh Bàn × 13 Chiều Phân Tích = 8.77 Triệu Đoạn Luận Giải Chuẩn Hóa)
# ══════════════════════════════════════════════════════════════════════════════

THIEN_KY_DIA_CHI_DIA_LY = {
    "Tý": ("Cung Khảm Thủy (Chính Bắc)", "Vùng sông nước, hồ đầm, kênh rạch hoặc nơi giao thương đường thủy; khí chất thông tuệ, thâm trầm"),
    "Sửu": ("Cung Cấn Thổ (Đông Bắc)", "Vùng đất gò đồi, chân núi, đồng bãi cần cù; tính cách kiên nhẫn, chịu thương chịu khó"),
    "Dần": ("Cung Cấn Sơn Lâm (Đông Bắc — Sơn Lâm Chi Địa)", "Vùng núi, rừng cây đại ngàn, miền sơn cước hoặc vùng cao nguyên cây cối trù phú; khí phách tự lập, vươn lên từ vùng núi"),
    "Mão": ("Cung Chấn Mộc (Chính Đông — Điền Viên Chi Địa)", "Vùng thảo mộc, vườn tược, rừng tre trúc xanh tươi; tính tình cương trực, năng động"),
    "Thìn": ("Cung Tốn Thủy Khố (Đông Nam — Long Trì Cao Nguyên)", "Vùng đất cao gần sông hồ lớn hoặc thung lũng trù phú; chí hướng lớn, có tài tổ chức"),
    "Tỵ": ("Cung Tốn Hỏa (Đông Nam — Đô Hội Giao Thương)", "Khu vực giao thương nhộn nhịp, phố chợ phát triển; đầu óc nhạy bén, hoạt bát"),
    "Ngọ": ("Cung Ly Hỏa (Chính Nam — Phồn Hoa Đô Hội)", "Trung tâm sáng sủa, cao ráo, văn minh; tính tình quang minh chính đại, nhiệt huyết"),
    "Mùi": ("Cung Khôn Thổ (Tây Nam — Thảo Nguyên Điền Thổ)", "Vùng đất rộng, đồng quê hoặc cao nguyên bằng phẳng; nhân hậu, trọng tình nghĩa gia đình"),
    "Thân": ("Cung Khôn/Đoài Kim (Tây Nam — Danh Đô Giao Lộ)", "Nơi đầu mối giao thông, thị trấn hoặc thành phố công nghiệp; lanh lợi, giỏi ứng biến"),
    "Dậu": ("Cung Đoài Kim (Chính Tây — Kim Thành Tụ Khí)", "Phố thị sầm uất hoặc vùng thung lũng trạch địa; sắc sảo, trọng danh dự và lời nói"),
    "Tuất": ("Cung Càn Hỏa Khố (Tây Bắc — Sơn Cương Cổ Địa)", "Vùng núi cao, gò đồi độc lập hoặc đất cổ truyền thống; trung thành, giữ vững nguyên tắc"),
    "Hợi": ("Cung Càn Thủy (Tây Bắc — Giang Hải Chi Địa)", "Vùng biển rộng, sông lớn hoặc nơi giao lưu bốn phương; bao dung, trí tuệ sâu rộng"),
}

THIEN_KY_14_CHINH_TINH_DOCTRINE = {
    "Tử Vi": "Đế Tinh (Bắc Đẩu Chủ — Hành Thổ): Chủ quyền uy, lãnh đạo, hậu đãi, giải ách chế hóa sát tinh; cần Tả Phụ - Hữu Bật phò tá mới thành Quân Thần Khánh Hội.",
    "Thiên Cơ": "Thiện Tinh / Mưu Thần (Nam Đẩu — Hành Mộc): Chủ trí tuệ, mưu lược, biến hóa linh hoạt, kỹ thuật, tham mưu; hợp Thiên Lương thành Cơ Lương Thiện Đàm Binh.",
    "Thái Dương": "Quang Minh Tinh (Trung Thiên — Hành Hỏa): Chủ quan lộc, danh tiếng, người cha/chồng, bác ái; đóng ban ngày (Dần-Mão-Thìn-Tỵ-Ngọ) là Nhật Lệ Trung Thiên đại cát.",
    "Vũ Khúc": "Chính Tài Tinh (Bắc Đẩu — Hành Kim): Chủ tiền bạc thực chất, quyết đoán, cương nghị, thực thi tài chính/kinh doanh.",
    "Thiên Đồng": "Phúc Tinh (Nam Đẩu — Hành Thủy): Chủ phúc thọ, hưởng thụ, hòa khí, khởi nghiệp từ hai bàn tay trắng (bạch thủ thành gia).",
    "Liêm Trinh": "Thứ Đào Hoa & Quan Tinh (Bắc Đẩu — Hành Hỏa): Chủ liêm chính, pháp luật, hành chính, kiêm duyên ngầm; gặp Thiên Phủ thì nội ngoại song toàn.",
    "Thiên Phủ": "Nam Đẩu Đế Tinh / Lộc Khố (Hành Thổ): Kho tàng tài lộc và điền sản, cẩn trọng, bảo toàn cơ nghiệp, hậu vận vững chắc.",
    "Thái Âm": "Điền Trạch & Phú Tinh (Trung Thiên — Hành Thủy): Chủ bất động sản, tích lũy tài sản ngầm, người mẹ/vợ; sáng rực từ Dậu-Tuất-Hợi-Tý (Nguyệt Lãng Thiên Môn).",
    "Tham Lang": "Chính Đào Hoa & Đa Nghệ Tinh (Bắc Đẩu — Hành Thủy/Mộc): Chủ giao tế, nghệ thuật, khát vọng lớn; hội Hỏa/Linh thành Hỏa Tham / Linh Tham bạo phát.",
    "Cự Môn": "Ám Tinh / Khẩu Tài Tinh (Bắc Đẩu — Hành Thủy): Chủ ngôn từ, biện luận, nghiên cứu chuyên sâu; gặp Thái Dương sáng chiếu thì Cự Nhật Đồng Lâm giải ám.",
    "Thiên Tướng": "Ấn Tinh (Nam Đẩu — Hành Thủy): Chủ con dấu quyền lực, phò tá trung thành, công bằng, trọng chữ tín (Phùng Phủ Khán Tướng).",
    "Thiên Lương": "Ấm Tinh / Thọ Tinh (Nam Đẩu — Hành Thổ/Mộc): Chủ che chở, y dược, giáo dục, thanh cao, giải trừ tai ách (Thọ Tinh Nhập Miếu).",
    "Thất Sát": "Tướng Tinh / Quyền Bính (Nam Đẩu — Hành Kim/Hỏa): Chủ uy dũng, khai phá, độc lập lập nghiệp nơi xa, quyết liệt.",
    "Phá Quân": "Hao Tinh / Tiên Phong (Bắc Đẩu — Hành Thủy): Chủ phá cũ lập mới, tiên phong đột phá, biến động lớn trước khi thành công.",
}

THIEN_KY_13_DIMENSIONS_NAMES = (
    "1. Bản Mệnh & Khí Chất Cốt Lõi (Mệnh - Thân)",
    "2. Cách Cục Chủ Đạo (Tam Phương Tứ Chính)",
    "3. Tứ Hóa Khâm Thiên (Lộc - Quyền - Khoa - Kỵ)",
    "4. Nguồn Gốc Xuất Thân & Song Thân (Cung Phụ Mẫu & Địa Lý Sinh Trưởng)",
    "5. Phúc Khí Tổ Tiên & Căn Cơ Tinh Thần (Cung Phúc Đức)",
    "6. Điền Trạch, Nhà Cửa & Môi Trường Sống (Cung Điền Trạch)",
    "7. Quan Lộc, Sự Nghiệp & Công Danh (Cung Quan Lộc)",
    "8. Tài Bạch, Dòng Tiền & Khả Năng Tích Lũy (Cung Tài Bạch)",
    "9. Phu Thê, Hôn Nhân & Phối Ngẫu (Cung Phu Thê)",
    "10. Tử Tức, Con Cái & Hậu Thế (Cung Tử Tức)",
    "11. Tật Ách, Cơ Độc & Ngũ Tạng Y Lý (Cung Tật Ách - Thiên Kỷ Y Dịch)",
    "12. Thiên Di, Xuất Ngoại & Quý Nhân Xã Hội (Cung Thiên Di - Nô Bộc)",
    "13. Đại Hạn 10 Năm & Lưu Niên Ứng Kỳ Thực Tế",
)


def analyze_thien_ky_13_dimensions(ls: dict) -> dict:
    """Phân tích lá số theo chuẩn 13 chiều của Kho Tử Vi 56.6GB GitHub (Renhuai123/ziwei-doushu — Nghê Hải Hạ《Thiên Kỷ》)."""
    if not isinstance(ls, dict):
        return {}
    cung_map = ls.get("cung_map") or {}
    menh_chi = (ls.get("menh_cung") or {}).get("chi", "Dần")
    than_chi = (ls.get("than_cung") or {}).get("chi", "Ngọ")
    tu_hoa = ls.get("tu_hoa") or {}
    luu_nien = ls.get("luu_nien") or {}

    def _get_stars(c_name: str) -> str:
        cd = cung_map.get(c_name) or {}
        ct = cd.get("chinh_tinh") or []
        pt = (cd.get("phu_tinh") or [])[:4]
        chi_c = cd.get("chi", "")
        s_str = ", ".join(ct) if ct else "Vô Chính Diệu (Mượn sao xung chiếu)"
        if pt:
            s_str += f" + [{', '.join(pt)}]"
        return f"Cung {chi_c} ({s_str})"

    menh_stars = (cung_map.get("Mệnh") or {}).get("chinh_tinh") or []
    quan_stars = (cung_map.get("Quan Lộc") or {}).get("chinh_tinh") or []
    tai_stars = (cung_map.get("Tài Bạch") or {}).get("chinh_tinh") or []
    tam_phuong_set = set(menh_stars + quan_stars + tai_stars)

    if tam_phuong_set & {"Sát", "Thất Sát", "Phá Quân", "Tham Lang"}:
        cach_cuc = "Cách Cục SÁT PHÁ THAM (Khai sáng, tự lập bươn chải, dám nghĩ dám làm, lập nghiệp từ thực chiến)"
    elif tam_phuong_set & {"Tử Vi", "Thiên Phủ", "Vũ Khúc", "Thiên Tướng"}:
        cach_cuc = "Cách Cục TỬ PHỦ VŨ TƯỚNG (Quản trị, tài chính, điền sản vững chắc, có uy tín lãnh đạo)"
    elif tam_phuong_set & {"Thiên Cơ", "Thái Âm", "Thiên Đồng", "Thiên Lương"}:
        cach_cuc = "Cách Cục CƠ NGUYỆT ĐỒNG LƯƠNG (Mưu lược, chuyên môn cao, tham mưu, công chức/giáo dục/kỹ thuật)"
    else:
        cach_cuc = "Cách Cục CỰ NHẬT / NHẬT NGUYỆT CHIẾU BÍCH (Trọng danh dự, trí tuệ sáng suốt, lấy chữ tín lập thân)"

    pm_chi = (cung_map.get("Phụ Mẫu") or {}).get("chi", menh_chi)
    pm_geo = THIEN_KY_DIA_CHI_DIA_LY.get(pm_chi, ("Địa mạch trung hòa", "Quê hương giàu truyền thống"))

    return {
        THIEN_KY_13_DIMENSIONS_NAMES[0]: f"Mệnh tại {menh_chi}, Thân tại {than_chi}, Cục {ls.get('cuc_ten', '')}, Nạp Âm {ls.get('nap_am', '')} — {_get_stars('Mệnh')}.",
        THIEN_KY_13_DIMENSIONS_NAMES[1]: f"{cach_cuc} | Hội chiếu Mệnh ({', '.join(menh_stars) or 'VCD'}) - Tài ({', '.join(tai_stars) or 'VCD'}) - Quan ({', '.join(quan_stars) or 'VCD'}).",
        THIEN_KY_13_DIMENSIONS_NAMES[2]: f"Hóa Lộc: {tu_hoa.get('Hóa Lộc')} (Nguồn lộc) · Hóa Quyền: {tu_hoa.get('Hóa Quyền')} (Thực quyền) · Hóa Khoa: {tu_hoa.get('Hóa Khoa')} (Quý nhân/Danh tiếng) · Hóa Kỵ: {tu_hoa.get('Hóa Kỵ')} (Điểm cần tu dưỡng).",
        THIEN_KY_13_DIMENSIONS_NAMES[3]: f"{_get_stars('Phụ Mẫu')} — Địa mạch gốc: {pm_geo[0]} ({pm_geo[1]}).",
        THIEN_KY_13_DIMENSIONS_NAMES[4]: f"{_get_stars('Phúc Đức')} — Gốc phúc đức dòng họ che chở lúc gặp biến cố.",
        THIEN_KY_13_DIMENSIONS_NAMES[5]: f"{_get_stars('Điền Trạch')} — Chủ khả năng tích lũy nhà đất, bất động sản.",
        THIEN_KY_13_DIMENSIONS_NAMES[6]: f"{_get_stars('Quan Lộc')} — Định hướng công danh, sự nghiệp trọng tâm.",
        THIEN_KY_13_DIMENSIONS_NAMES[7]: f"{_get_stars('Tài Bạch')} — Phương thức tạo dòng tiền và quản lý tài sản.",
        THIEN_KY_13_DIMENSIONS_NAMES[8]: f"{_get_stars('Phu Thê')} — Duyên phận phối ngẫu và sự đồng hành gia đạo.",
        THIEN_KY_13_DIMENSIONS_NAMES[9]: f"{_get_stars('Tử Tức')} — Đường con cái và phúc hậu vận.",
        THIEN_KY_13_DIMENSIONS_NAMES[10]: f"{_get_stars('Tật Ách')} — Cần lưu ý cân bằng âm dương ngũ tạng theo Thiên Kỷ Y Lý.",
        THIEN_KY_13_DIMENSIONS_NAMES[11]: f"Thiên Di: {_get_stars('Thiên Di')} | Nô Bộc: {_get_stars('Nô Bộc')}.",
        THIEN_KY_13_DIMENSIONS_NAMES[12]: f"Lưu Niên {luu_nien.get('nam')} ({luu_nien.get('tuoi')} tuổi) nhập cung {luu_nien.get('cung')} ({luu_nien.get('chi')}).",
    }


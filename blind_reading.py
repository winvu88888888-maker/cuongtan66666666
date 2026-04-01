# blind_reading.py - Engine Mang Đoán V5.1
# Pre-computes personal deductions from chart data using traditional rules
# Uses SEASON-BASED (Tiết Khí) Vượng/Suy - doesn't need palace positions

# ============================================================
# NGŨ HÀNH MAPPINGS
# ============================================================
CAN_NGU_HANH = {'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa', 
                'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim', 
                'Nhâm': 'Thủy', 'Quý': 'Thủy'}

CAN_AM_DUONG = {'Giáp': 'Dương', 'Ất': 'Âm', 'Bính': 'Dương', 'Đinh': 'Âm', 
                'Mậu': 'Dương', 'Kỷ': 'Âm', 'Canh': 'Dương', 'Tân': 'Âm', 
                'Nhâm': 'Dương', 'Quý': 'Âm'}

SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
KHAC = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}

# ============================================================
# SEASON-BASED VƯỢNG/SUY (Lệnh - theo Tiết Khí)
# More traditional and reliable than palace-based
# ============================================================
# Season mapping from Tiết Khí
TIET_KHI_MUA = {
    'Lập Xuân': 'Xuân', 'Vũ Thủy': 'Xuân', 'Kinh Trập': 'Xuân', 
    'Xuân Phân': 'Xuân', 'Thanh Minh': 'Xuân', 'Cốc Vũ': 'Xuân',
    'Lập Hạ': 'Hạ', 'Tiểu Mãn': 'Hạ', 'Mang Chủng': 'Hạ',
    'Hạ Chí': 'Hạ', 'Tiểu Thử': 'Hạ', 'Đại Thử': 'Hạ',
    'Lập Thu': 'Thu', 'Xử Thử': 'Thu', 'Bạch Lộ': 'Thu',
    'Thu Phân': 'Thu', 'Hàn Lộ': 'Thu', 'Sương Giáng': 'Thu',
    'Lập Đông': 'Đông', 'Tiểu Tuyết': 'Đông', 'Đại Tuyết': 'Đông',
    'Đông Chí': 'Đông', 'Tiểu Hàn': 'Đông', 'Đại Hàn': 'Đông',
}

# Hành nào Vượng/Tướng/Hưu/Tù/Tử trong mùa nào
# Format: {mùa: {hành: trạng thái}}
MUA_VUONG_SUY = {
    'Xuân': {'Mộc': 'VƯỢNG', 'Hỏa': 'TƯỚNG', 'Thổ': 'TỬ', 'Kim': 'TÙ', 'Thủy': 'HƯU'},
    'Hạ':   {'Hỏa': 'VƯỢNG', 'Thổ': 'TƯỚNG', 'Kim': 'TỬ', 'Thủy': 'TÙ', 'Mộc': 'HƯU'},
    'Thu':  {'Kim': 'VƯỢNG', 'Thủy': 'TƯỚNG', 'Mộc': 'TỬ', 'Hỏa': 'TÙ', 'Thổ': 'HƯU'},
    'Đông': {'Thủy': 'VƯỢNG', 'Mộc': 'TƯỚNG', 'Hỏa': 'TỬ', 'Thổ': 'TÙ', 'Kim': 'HƯU'},
}

# V5.2: KHÔNG dùng Vượng/Suy để đoán tuổi — phương pháp này SAI HOÀN TOÀN
# Tuổi chỉ có thể ước lượng bằng Hà Đồ số Cung + Tiên Thiên Bát Quái số
# AI sẽ tự tính từ dữ liệu quẻ, không cần module này đoán trước


def get_season_vuong_suy(hanh, tiet_khi):
    """Tính Vượng/Suy theo mùa (Lệnh)"""
    mua = TIET_KHI_MUA.get(tiet_khi, 'Xuân')
    return MUA_VUONG_SUY.get(mua, {}).get(hanh, 'TRUNG BÌNH')


def ngu_hanh_relation(e1, e2):
    """Quan hệ Ngũ Hành giữa e1 và e2"""
    if not e1 or not e2 or e1 == '?' or e2 == '?':
        return '?'
    if e1 == e2:
        return 'Tỷ Hòa (ngang sức)'
    if SINH.get(e1) == e2:
        return f'{e1} sinh {e2}'
    if SINH.get(e2) == e1:
        return f'{e2} sinh {e1}'
    if KHAC.get(e1) == e2:
        return f'{e1} khắc {e2}'
    if KHAC.get(e2) == e1:
        return f'{e2} khắc {e1}'
    return '?'


# ============================================================
# MAIN: BLIND READING
# ============================================================
def blind_read(chart_data=None, mai_hoa_data=None, luc_hao_data=None):
    """
    Pre-compute ALL personal deductions from chart data.
    Uses only basic fields: can_ngay, can_gio, can_thang, can_nam, tiet_khi
    """
    result = {}
    
    if not chart_data:
        return {"error": "Chưa có dữ liệu Kỳ Môn"}
    
    # Extract key data
    can_ngay = chart_data.get('can_ngay', '')
    can_gio = chart_data.get('can_gio', '')
    can_thang = chart_data.get('can_thang', '')
    can_nam = chart_data.get('can_nam', '')
    chi_ngay = chart_data.get('chi_ngay', '')
    tiet_khi = chart_data.get('tiet_khi', 'Lập Xuân')
    cuc = chart_data.get('cuc', '?')
    
    if not can_ngay:
        return {"error": "Thiếu Can Ngày"}
    
    can_ngay_hanh = CAN_NGU_HANH.get(can_ngay, '?')
    can_ngay_ad = CAN_AM_DUONG.get(can_ngay, '?')
    mua = TIET_KHI_MUA.get(tiet_khi, 'Xuân')
    
    # ================================
    # 1. GIỚI TÍNH (Can Ngày Âm/Dương)
    # ================================
    if can_ngay_ad == 'Dương':
        result['gioi_tinh'] = f"NAM (Can Ngày {can_ngay} - Dương Can)"
    else:
        result['gioi_tinh'] = f"NỮ (Can Ngày {can_ngay} - Âm Can)"
    
    # ================================
    # 2. TUỔI — V5.2: CHỈ cung cấp dữ liệu thô, KHÔNG đoán tuổi
    # ================================
    vuong_suy = get_season_vuong_suy(can_ngay_hanh, tiet_khi)
    result['tuoi'] = (
        f"KHÔNG XÁC ĐỊNH ĐƯỢC từ Mang Đoán. "
        f"AI hãy dùng Hà Đồ số Cung + Tiên Thiên số Quẻ để tính. "
        f"Dữ liệu thô: Can {can_ngay}({can_ngay_hanh}), mùa {mua}, Vượng/Suy={vuong_suy}, Cục={cuc}"
    )
    
    # ================================
    # 3. ANH CHỊ EM (Can Tháng + Lục Hào Huynh Đệ)
    # ================================
    ace_reasons = []
    ace_count = 3  # default
    
    if can_thang:
        thang_hanh = CAN_NGU_HANH.get(can_thang, '?')
        thang_vs = get_season_vuong_suy(thang_hanh, tiet_khi)
        
        if thang_vs in ['VƯỢNG', 'TƯỚNG']:
            ace_count = 4
            ace_reasons.append(f"KM: Can Tháng {can_thang}({thang_hanh}) {thang_vs} → nhiều anh chị em")
        elif thang_vs in ['TÙ', 'TỬ']:
            ace_count = 2
            ace_reasons.append(f"KM: Can Tháng {can_thang}({thang_hanh}) {thang_vs} → ít anh chị em")
        else:
            ace_count = 3
            ace_reasons.append(f"KM: Can Tháng {can_thang}({thang_hanh}) {thang_vs}")
    
    # Lục Hào: đếm Huynh Đệ hào
    if luc_hao_data:
        ban_details = luc_hao_data.get('ban', {}).get('details', [])
        hd_count = 0
        hd_vuong = 0
        for d in ban_details:
            lt = str(d.get('luc_than', ''))
            if 'Huynh' in lt or 'huynh' in lt:
                hd_count += 1
                s = str(d.get('strength', ''))
                if 'Vượng' in s or 'Tướng' in s:
                    hd_vuong += 1
        
        if hd_count > 0:
            lh_est = hd_count + hd_vuong
            ace_count = max(ace_count, lh_est)
            ace_reasons.append(f"LH: {hd_count} Huynh Đệ hào ({hd_vuong} Vượng)")
    
    result['anh_chi_em'] = f"{ace_count}-{ace_count + 2} người ({'; '.join(ace_reasons) if ace_reasons else 'ước lượng'})"
    
    # ================================
    # 4. TÀI LỘC
    # ================================
    tai_reasons = []
    tai_score = 0  # positive = good
    
    # Can Ngày vs Can Giờ (sinh = tiền vào)
    if can_gio:
        gio_hanh = CAN_NGU_HANH.get(can_gio, '?')
        rel = ngu_hanh_relation(gio_hanh, can_ngay_hanh)
        if 'sinh' in rel and can_ngay_hanh in rel:
            tai_score += 1
            tai_reasons.append(f"KM: Can Giờ {can_gio}({gio_hanh}) sinh Can Ngày → TÀI ĐẾN")
        elif 'khắc' in rel and can_ngay_hanh in rel.split('khắc')[0]:
            tai_score -= 1
            tai_reasons.append(f"KM: Can Giờ {can_gio}({gio_hanh}) khắc Can Ngày → HAO TÀI")
    
    # Mai Hoa Thể/Dụng
    if mai_hoa_data:
        upper_e = mai_hoa_data.get('upper_element', '')
        lower_e = mai_hoa_data.get('lower_element', '')
        if upper_e and lower_e:
            rel = ngu_hanh_relation(lower_e, upper_e)
            if 'sinh' in rel and lower_e in rel.split('sinh')[0]:
                tai_reasons.append(f"MH: Dụng({upper_e}) sinh Thể({lower_e}) → ĐƯỢC HỖ TRỢ")
                tai_score += 1
            elif 'khắc' in rel and lower_e in rel.split('khắc')[0]:
                tai_reasons.append(f"MH: Thể({lower_e}) khắc Dụng({upper_e}) → CHỦ ĐỘNG KIẾM TIỀN")
                tai_score += 1
    
    # Lục Hào Thê Tài
    if luc_hao_data:
        ban_details = luc_hao_data.get('ban', {}).get('details', [])
        for d in ban_details:
            lt = str(d.get('luc_than', ''))
            if 'Tài' in lt:
                s = str(d.get('strength', ''))
                if 'Vượng' in s or 'Tướng' in s:
                    tai_score += 1
                    tai_reasons.append(f"LH: Thê Tài {s} → TÀI VƯỢNG")
                else:
                    tai_reasons.append(f"LH: Thê Tài {s}")
                break
    
    if tai_score >= 2:
        result['tai_loc'] = f"GIÀU CÓ, tài lộc vượng ({'; '.join(tai_reasons)})"
    elif tai_score >= 1:
        result['tai_loc'] = f"KHÁ GIẢ, có tài nhưng không quá nhiều ({'; '.join(tai_reasons)})"
    elif tai_score <= -1:
        result['tai_loc'] = f"KHÓ KHĂN, hao tài tốn của ({'; '.join(tai_reasons)})"
    else:
        result['tai_loc'] = f"TRUNG BÌNH ({'; '.join(tai_reasons) if tai_reasons else 'cần phân tích thêm'})"
    
    # ================================
    # 5. HÔN NHÂN (Can Ngày vs Can Giờ)
    # ================================
    if can_gio:
        gio_hanh = CAN_NGU_HANH.get(can_gio, '?')
        rel = ngu_hanh_relation(can_ngay_hanh, gio_hanh)
        if 'sinh' in rel:
            result['hon_nhan'] = f"HÒA THUẬN, gia đình hạnh phúc (Can Ngày {can_ngay}({can_ngay_hanh}) vs Can Giờ {can_gio}({gio_hanh}): {rel})"
        elif 'Tỷ Hòa' in rel:
            result['hon_nhan'] = f"NGANG SỨC, vợ chồng bình đẳng ({rel})"
        elif 'khắc' in rel:
            result['hon_nhan'] = f"CÓ XUNG ĐỘT trong hôn nhân ({rel})"
    
    # ================================
    # 6. CON CÁI (Can Giờ + Tử Tôn)
    # ================================
    con_reasons = []
    if can_gio:
        gio_hanh = CAN_NGU_HANH.get(can_gio, '?')
        gio_vs = get_season_vuong_suy(gio_hanh, tiet_khi)
        if gio_vs in ['VƯỢNG', 'TƯỚNG']:
            con_reasons.append(f"KM: Can Giờ {can_gio}({gio_hanh}) {gio_vs} → con phát triển tốt, 2-3 con")
        elif gio_vs in ['TÙ', 'TỬ']:
            con_reasons.append(f"KM: Can Giờ {can_gio}({gio_hanh}) {gio_vs} → con ít hoặc vất vả, 1-2 con")
        else:
            con_reasons.append(f"KM: Can Giờ {can_gio}({gio_hanh}) {gio_vs} → 2 con")
    
    if luc_hao_data:
        ban_details = luc_hao_data.get('ban', {}).get('details', [])
        tt_count = 0
        for d in ban_details:
            lt = str(d.get('luc_than', ''))
            if 'Tôn' in lt or 'tôn' in lt:
                tt_count += 1
        if tt_count > 0:
            con_reasons.append(f"LH: {tt_count} Tử Tôn hào → {tt_count}-{tt_count+1} con")
    
    result['con_cai'] = '; '.join(con_reasons) if con_reasons else "2 con (ước lượng)"
    
    # ================================
    # 7. SỨC KHỎE
    # ================================
    HANH_BENH = {
        'Kim': 'phổi, hô hấp, da',
        'Mộc': 'gan, mắt, gân',
        'Thủy': 'thận, bàng quang, tai',
        'Hỏa': 'tim, mạch máu',
        'Thổ': 'dạ dày, lá lách'
    }
    
    benh_canh_bao = HANH_BENH.get(KHAC.get(can_ngay_hanh, ''), '')
    if vuong_suy in ['VƯỢNG', 'TƯỚNG']:
        result['suc_khoe'] = f"TỐT, thể lực khỏe mạnh. Cẩn thận {benh_canh_bao}" if benh_canh_bao else "TỐT"
    elif vuong_suy in ['TÙ', 'TỬ']:
        result['suc_khoe'] = f"YẾU, cần chú ý {benh_canh_bao}" if benh_canh_bao else "YẾU, cần nghỉ ngơi"
    else:
        result['suc_khoe'] = f"TRUNG BÌNH. Lưu ý {benh_canh_bao}" if benh_canh_bao else "TRUNG BÌNH"
    
    # ================================
    # 8. HƯỚNG CÁT
    # ================================
    HANH_HUONG = {
        'Mộc': 'Đông, Đông Nam',
        'Hỏa': 'Nam',
        'Thổ': 'Trung tâm, Tây Nam, Đông Bắc',
        'Kim': 'Tây, Tây Bắc',
        'Thủy': 'Bắc'
    }
    # Hướng cát = hướng của hành sinh Can Ngày
    for hanh, huong in HANH_HUONG.items():
        if SINH.get(hanh) == can_ngay_hanh:
            result['huong_cat'] = f"{huong} (Hành {hanh} sinh {can_ngay_hanh})"
            break
    
    return result


def format_blind_reading(readings):
    """Format blind reading results into text block for AI context"""
    if not readings or 'error' in readings:
        err = readings.get('error', 'Unknown') if readings else 'No data'
        return f"=== MANG ĐOÁN ===\n(Lỗi: {err})\n"
    
    lines = ["\n=== MANG ĐOÁN (Pre-computed từ quẻ) ==="]
    
    field_labels = {
        'gioi_tinh': 'GIỚI TÍNH',
        'tuoi': 'TUỔI',
        'anh_chi_em': 'ANH CHỊ EM',
        'tai_loc': 'TÀI LỘC',
        'hon_nhan': 'HÔN NHÂN',
        'con_cai': 'CON CÁI', 
        'suc_khoe': 'SỨC KHỎE',
        'huong_cat': 'HƯỚNG CÁT',
    }
    
    for key, label in field_labels.items():
        if key in readings:
            lines.append(f"★ {label}: {readings[key]}")
    
    lines.append("=== HẾT MANG ĐOÁN ===")
    return '\n'.join(lines)

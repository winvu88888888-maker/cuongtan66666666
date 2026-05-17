"""
ung_ky_engine.py — V42.9.42: Engine Ứng Kỳ Chi Tiết
Dự đoán thời gian cụ thể: GIỜ / NGÀY / THÁNG / NĂM

Nguyên lý theo sách:
1. Lục Hào: Chi DT + trạng thái (Tuần Không/Nhập Mộ/Động/Tĩnh) → timing
2. Kỳ Môn: Âm/Dương Độn + Nội/Ngoại Bàn → xa/gần
3. Mai Hoa: Tiên Thiên Số + Hậu Thiên Số → thời gian
4. Tổng hợp: Cross-reference để ra ngày/tháng/năm CỤ THỂ
"""

import datetime

# ═══ BẢNG CAN CHI ═══
THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

CHI_MONTH_MAP = {
    'Dần': 1, 'Mão': 2, 'Thìn': 3, 'Tị': 4, 'Ngọ': 5, 'Mùi': 6,
    'Thân': 7, 'Dậu': 8, 'Tuất': 9, 'Hợi': 10, 'Tý': 11, 'Sửu': 12,
}
CHI_HOUR_MAP = {
    'Tý': '23:00-01:00', 'Sửu': '01:00-03:00', 'Dần': '03:00-05:00',
    'Mão': '05:00-07:00', 'Thìn': '07:00-09:00', 'Tị': '09:00-11:00',
    'Ngọ': '11:00-13:00', 'Mùi': '13:00-15:00', 'Thân': '15:00-17:00',
    'Dậu': '17:00-19:00', 'Tuất': '19:00-21:00', 'Hợi': '21:00-23:00',
}

HANH_CHI = {
    'Kim': ['Thân', 'Dậu'], 'Mộc': ['Dần', 'Mão'], 'Thủy': ['Tý', 'Hợi'],
    'Hỏa': ['Ngọ', 'Tị'], 'Thổ': ['Thìn', 'Tuất', 'Sửu', 'Mùi']
}
LUC_XUNG = {
    'Tý': 'Ngọ', 'Sửu': 'Mùi', 'Dần': 'Thân', 'Mão': 'Dậu',
    'Thìn': 'Tuất', 'Tị': 'Hợi', 'Ngọ': 'Tý', 'Mùi': 'Sửu',
    'Thân': 'Dần', 'Dậu': 'Mão', 'Tuất': 'Thìn', 'Hợi': 'Tị',
}
LUC_HOP = {
    'Tý': 'Sửu', 'Sửu': 'Tý', 'Dần': 'Hợi', 'Mão': 'Tuất',
    'Thìn': 'Dậu', 'Tị': 'Thân', 'Ngọ': 'Mùi', 'Mùi': 'Ngọ',
    'Thân': 'Tị', 'Dậu': 'Thìn', 'Tuất': 'Mão', 'Hợi': 'Dần',
}
MO_KHO = {'Kim': 'Sửu', 'Mộc': 'Mùi', 'Thủy': 'Thìn', 'Hỏa': 'Tuất', 'Thổ': 'Tuất'}
SINH = {'Kim': 'Thủy', 'Thủy': 'Mộc', 'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim'}

# ═══ SỐ TIÊN THIÊN → NGÀY ═══
QUAI_SO = {'Càn': 1, 'Đoài': 2, 'Ly': 3, 'Chấn': 4, 'Tốn': 5, 'Khảm': 6, 'Cấn': 7, 'Khôn': 8}


def _chi_to_dates(chi, base_date=None, scope='month'):
    """Chuyển Chi thành ngày/tháng dương lịch cụ thể"""
    if not base_date:
        base_date = datetime.date.today()
    
    results = []
    
    if scope == 'hour':
        hour_range = CHI_HOUR_MAP.get(chi, '')
        if hour_range:
            results.append(f"Giờ {chi} ({hour_range})")
    
    if scope in ('day', 'month', 'year'):
        # Tìm ngày gần nhất có Chi này
        chi_idx = DIA_CHI.index(chi) if chi in DIA_CHI else -1
        if chi_idx >= 0:
            # Tìm ngày tiếp theo mang Chi này (chu kỳ 12 ngày)
            today_idx = (base_date.toordinal() + 1) % 12  # Approximate
            for delta in range(0, 365):
                check_date = base_date + datetime.timedelta(days=delta)
                # Ngày Can Chi: lấy index trong 60 Giáp Tý
                day_idx = (check_date.toordinal() + 1) % 12
                if day_idx == chi_idx:
                    results.append(f"Ngày {check_date.strftime('%d/%m/%Y')} ({chi})")
                    if len(results) >= 3:
                        break
    
    if scope in ('month', 'year'):
        month_num = CHI_MONTH_MAP.get(chi)
        if month_num:
            # Tháng âm lịch ≈ tháng dương + 1
            dl_month = month_num + 1 if month_num <= 11 else 1
            dl_year = base_date.year if dl_month >= base_date.month else base_date.year + 1
            results.append(f"Tháng {dl_month}/{dl_year} (≈ tháng {chi} âm lịch)")
    
    if scope == 'year':
        chi_idx = DIA_CHI.index(chi) if chi in DIA_CHI else -1
        if chi_idx >= 0:
            for y in range(base_date.year, base_date.year + 13):
                if (y - 4) % 12 == chi_idx:
                    results.append(f"Năm {y} (năm {chi})")
                    break
    
    return results


def calc_ung_ky_detail(
    chi_dt='',
    hanh_dt='',
    is_tuan_khong=False,
    is_nhap_mo=False,
    is_dong=False,
    ts_stage='',
    am_duong_don='',
    noi_ngoai='',
    the_quai='',
    dung_quai='',
    verdict='',
    weighted_pct=50,
):
    """
    MASTER FUNCTION: Tính Ứng Kỳ chi tiết từ GIỜ → NĂM.
    
    Returns: dict {
        'summary': str,     # Tóm tắt 1 dòng
        'hour': str,        # Giờ ứng nghiệm
        'day': str,         # Ngày ứng nghiệm  
        'month': str,       # Tháng ứng nghiệm
        'year': str,        # Năm ứng nghiệm
        'speed': str,       # Nhanh/Chậm
        'confidence': str,  # Độ tin cậy
        'method': str,      # Phương pháp tính
        'html': str,        # HTML hiển thị
    }
    """
    now = datetime.date.today()
    result = {
        'summary': '', 'hour': '', 'day': '', 'month': '', 'year': '',
        'speed': '', 'confidence': '', 'method': '', 'html': '',
    }
    
    methods_used = []
    
    # ═══ 1. XÁC ĐỊNH TỐC ĐỘ (NHANH/CHẬM) ═══
    speed_score = 0  # >0 = nhanh, <0 = chậm
    speed_reasons = []
    
    # Âm/Dương Độn
    if am_duong_don:
        if 'Dương' in am_duong_don:
            speed_score += 1
            speed_reasons.append("Dương Độn → nhanh")
        else:
            speed_score -= 1
            speed_reasons.append("Âm Độn → chậm")
    
    # Nội/Ngoại
    if noi_ngoai:
        if 'Nội' in noi_ngoai:
            speed_score += 1
            speed_reasons.append("Nội bàn → gần, nhanh")
        else:
            speed_score -= 1
            speed_reasons.append("Ngoại bàn → xa, chậm")
    
    # Trạng thái DT
    if is_tuan_khong:
        speed_score -= 2
        speed_reasons.append("Tuần Không → chờ Điền Thực")
    if is_nhap_mo:
        speed_score -= 2
        speed_reasons.append("Nhập Mộ → tắc, chờ Xung Mộ")
    if is_dong:
        speed_score += 1
        speed_reasons.append("DT Động → sự việc đang diễn ra")
    
    # Trường Sinh
    fast_stages = ['Đế Vượng', 'Lâm Quan', 'Quan Đới', 'Trường Sinh']
    slow_stages = ['Suy', 'Bệnh', 'Tử', 'Mộ', 'Tuyệt', 'Thai', 'Dưỡng']
    if ts_stage in fast_stages:
        speed_score += 1
        speed_reasons.append(f"{ts_stage} → DT mạnh, ứng nhanh")
    elif ts_stage in slow_stages:
        speed_score -= 1
        speed_reasons.append(f"{ts_stage} → DT yếu, ứng chậm")
    
    # Verdict
    if verdict in ('CÁT', 'ĐẠI CÁT') or weighted_pct >= 60:
        speed_score += 1
    elif verdict in ('HUNG', 'ĐẠI HUNG') or weighted_pct < 35:
        speed_score -= 1
    
    if speed_score >= 2:
        result['speed'] = '⚡ RẤT NHANH (vài giờ → vài ngày)'
        scope = 'day'
    elif speed_score >= 0:
        result['speed'] = '🕐 BÌNH THƯỜNG (vài ngày → vài tuần)'
        scope = 'month'
    elif speed_score >= -2:
        result['speed'] = '🐌 CHẬM (vài tuần → vài tháng)'
        scope = 'month'
    else:
        result['speed'] = '⏳ RẤT CHẬM (vài tháng → cả năm)'
        scope = 'year'
    
    methods_used.append(f"Tốc độ: {speed_score:+d} ({', '.join(speed_reasons[:3])})")
    
    # ═══ 2. TÍNH GIỜ ỨNG NGHIỆM ═══
    target_chi_hour = ''
    if chi_dt:
        if is_tuan_khong:
            target_chi_hour = chi_dt  # Điền Thực = chính Chi DT
        elif is_nhap_mo and hanh_dt:
            mo = MO_KHO.get(hanh_dt, '')
            target_chi_hour = LUC_XUNG.get(mo, '') if mo else ''
        elif is_dong:
            target_chi_hour = LUC_HOP.get(chi_dt, '')  # Hợp giữ
        else:
            target_chi_hour = LUC_XUNG.get(chi_dt, '')  # Xung kích hoạt
        
        if target_chi_hour:
            result['hour'] = f"Giờ {target_chi_hour} ({CHI_HOUR_MAP.get(target_chi_hour, '?')})"
            methods_used.append(f"Giờ: Chi {target_chi_hour}")
    
    # ═══ 3. TÍNH NGÀY ỨNG NGHIỆM ═══
    target_chi_day = target_chi_hour or chi_dt
    if target_chi_day:
        dates = _chi_to_dates(target_chi_day, now, 'day')
        if dates:
            result['day'] = dates[0] if dates else ''
            if len(dates) > 1:
                result['day'] += f" hoặc {dates[1]}"
            methods_used.append("Ngày: Chi gần nhất")
    
    # ═══ 4. TÍNH THÁNG ỨNG NGHIỆM ═══
    target_chi_month = ''
    if hanh_dt:
        hanh_chi_list = HANH_CHI.get(hanh_dt, [])
        if hanh_chi_list:
            # Tháng hành DT vượng
            target_chi_month = hanh_chi_list[0]
    
    if is_tuan_khong and chi_dt:
        target_chi_month = chi_dt
    elif is_nhap_mo and hanh_dt:
        mo = MO_KHO.get(hanh_dt, '')
        target_chi_month = LUC_XUNG.get(mo, '') if mo else target_chi_month
    
    if target_chi_month:
        month_dates = _chi_to_dates(target_chi_month, now, 'month')
        if month_dates:
            for md in month_dates:
                if 'Tháng' in md:
                    result['month'] = md
                    break
        methods_used.append(f"Tháng: Chi {target_chi_month}")
    
    # ═══ 5. TÍNH NĂM ỨNG NGHIỆM ═══
    if scope == 'year' and target_chi_month:
        year_dates = _chi_to_dates(target_chi_month, now, 'year')
        if year_dates:
            for yd in year_dates:
                if 'Năm' in yd:
                    result['year'] = yd
                    break
    
    # ═══ 6. MAI HOA BỔ SUNG ═══
    if the_quai and dung_quai:
        the_so = QUAI_SO.get(the_quai, 0)
        dung_so = QUAI_SO.get(dung_quai, 0)
        if the_so and dung_so:
            tong = the_so + dung_so
            methods_used.append(f"Mai Hoa: Thể({the_so})+Dụng({dung_so})={tong} → {tong} ngày/tháng")
            if not result['day']:
                future_day = now + datetime.timedelta(days=tong)
                result['day'] = f"~{future_day.strftime('%d/%m/%Y')} (Thể+Dụng={tong} ngày)"
    
    # ═══ 7. ĐỘ TIN CẬY ═══
    conf_count = sum(1 for v in [result['hour'], result['day'], result['month']] if v)
    if conf_count >= 3:
        result['confidence'] = '🟢 CAO (3+ phương pháp đồng thuận)'
    elif conf_count >= 2:
        result['confidence'] = '🟡 TRUNG BÌNH (2 phương pháp)'
    else:
        result['confidence'] = '🔴 THẤP (chưa đủ dữ liệu)'
    
    result['method'] = ' | '.join(methods_used[:4])
    
    # ═══ 8. SUMMARY ═══
    parts = []
    if result['hour']: parts.append(result['hour'])
    if result['day']: parts.append(result['day'])
    if result['month']: parts.append(result['month'])
    if result['year']: parts.append(result['year'])
    result['summary'] = ' → '.join(parts) if parts else 'Chưa xác định'
    
    # ═══ 9. BUILD HTML ═══
    result['html'] = _build_ung_ky_html(result, speed_reasons)
    
    return result


def _build_ung_ky_html(result, speed_reasons):
    rows = []
    if result['hour']:
        rows.append(f'<tr><td style="color:#fbbf24;font-weight:700;">⏰ GIỜ</td><td style="color:#f1f5f9;">{result["hour"]}</td></tr>')
    if result['day']:
        rows.append(f'<tr><td style="color:#34d399;font-weight:700;">📅 NGÀY</td><td style="color:#f1f5f9;">{result["day"]}</td></tr>')
    if result['month']:
        rows.append(f'<tr><td style="color:#60a5fa;font-weight:700;">🗓 THÁNG</td><td style="color:#f1f5f9;">{result["month"]}</td></tr>')
    if result['year']:
        rows.append(f'<tr><td style="color:#c084fc;font-weight:700;">📆 NĂM</td><td style="color:#f1f5f9;">{result["year"]}</td></tr>')
    
    speed_html = f'<div style="color:#fde68a;font-size:0.95em;margin-top:8px;">🚀 {result["speed"]}</div>' if result['speed'] else ''
    conf_html = f'<div style="color:#a7f3d0;font-size:0.9em;">{result["confidence"]}</div>' if result['confidence'] else ''
    
    table = ''.join(rows)
    
    return (
        f'<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);padding:18px;border-radius:14px;'
        f'margin:12px 0;border:2px solid #6366f1;box-shadow:0 4px 20px rgba(99,102,241,0.3);">'
        f'<div style="font-size:1.15em;font-weight:800;color:#a5b4fc;margin-bottom:10px;">⏱ ỨNG KỲ CHI TIẾT — Dự Đoán Thời Gian</div>'
        f'<table style="width:100%;border-collapse:collapse;">'
        f'{"".join(rows)}'
        f'</table>'
        f'{speed_html}{conf_html}'
        f'</div>'
    )

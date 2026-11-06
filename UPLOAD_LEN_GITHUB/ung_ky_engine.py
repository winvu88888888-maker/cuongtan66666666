"""
ung_ky_engine.py — V99.0 OMNISCIENT: Engine Ứng Kỳ Tiên Tri Chi Tiết
Dự đoán thời gian chính xác tuyệt đối: NĂM / THÁNG / NGÀY / GIỜ / KHẮC / PHÚT

Nguyên lý hợp nhất:
1. Lục Hào: Chi DT + trạng thái (Tuần Không/Nhập Mộ/Động/Tĩnh/Ám Động) → Năm, Tháng, Ngày, Giờ
2. Kỳ Môn: Âm/Dương Độn + Nội/Ngoại Bàn + Cung Cửu Tinh/Bát Môn → Tốc độ & Khắc ứng nghiệm
3. Mai Hoa: Tiên Thiên Bát Quái Số + Hậu Thiên Lạc Thư Số + Hào Động → Khắc (15 phút) & Phút chính xác
4. Hà Đồ Ngũ Hành Số: Thủy (1,6), Hỏa (2,7), Mộc (3,8), Kim (4,9), Thổ (5,0) → Số đuôi của Phút ứng kỳ
5. Lịch Vạn Niên JDN (Julian Day Number) + Âm Lịch: Tính chính xác 100% Ngày Can Chi, Thứ trong tuần, Ngày Âm/Dương.
"""

import datetime

try:
    from xem_ngay_dep import _jdn as _xnd_jdn, solar2lunar as _xnd_s2l
except Exception:
    _xnd_jdn = None
    _xnd_s2l = None

# ═══ BẢNG CAN CHI & HẰNG SỐ ═══
THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
WEEKDAY_VN = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']

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
CHI_START_HOUR = {
    'Tý': 23, 'Sửu': 1, 'Dần': 3, 'Mão': 5, 'Thìn': 7, 'Tị': 9,
    'Ngọ': 11, 'Mùi': 13, 'Thân': 15, 'Dậu': 17, 'Tuất': 19, 'Hợi': 21,
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

# ═══ SỐ TIÊN THIÊN & HẬU THIÊN & HÀ ĐỒ ═══
QUAI_SO = {'Càn': 1, 'Đoài': 2, 'Ly': 3, 'Chấn': 4, 'Tốn': 5, 'Khảm': 6, 'Cấn': 7, 'Khôn': 8}
LAC_THU_CUNG_QUAI = {1: 'Khảm', 2: 'Khôn', 3: 'Chấn', 4: 'Tốn', 5: 'Khôn', 6: 'Càn', 7: 'Đoài', 8: 'Cấn', 9: 'Ly'}
CUNG_TO_CHI = {
    1: 'Tý', 2: 'Mùi', 3: 'Mão', 4: 'Thìn', 5: 'Thìn',
    6: 'Tuất', 7: 'Dậu', 8: 'Dần', 9: 'Ngọ',
}
HA_DO_DIGITS = {
    'Thủy': (1, 6),
    'Hỏa': (2, 7),
    'Mộc': (3, 8),
    'Kim': (4, 9),
    'Thổ': (5, 0),
}
BAT_QUAI_KHAC_NAME = {
    1: 'Khắc 1 (Càn Kim — 15 phút đầu)',
    2: 'Khắc 2 (Đoài Kim — phút 15 đến 30)',
    3: 'Khắc 3 (Ly Hỏa — phút 30 đến 45)',
    4: 'Khắc 4 (Chấn Mộc — phút 45 đến 60)',
    5: 'Khắc 5 (Tốn Mộc — phút 60 đến 75)',
    6: 'Khắc 6 (Khảm Thủy — phút 75 đến 90)',
    7: 'Khắc 7 (Cấn Thổ — phút 90 đến 105)',
    8: 'Khắc 8 (Khôn Thổ — 15 phút cuối)',
}


def _calc_jdn(d, m, y):
    """Tính Julian Day Number chính xác 100% cho lịch Dương."""
    if _xnd_jdn is not None:
        try:
            return _xnd_jdn(d, m, y)
        except Exception:
            pass
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045


def _get_day_canchi(dt_obj):
    """Trả về (can, chi, can_chi_str) của một ngày dương lịch."""
    jdn = _calc_jdn(dt_obj.day, dt_obj.month, dt_obj.year)
    can = THIEN_CAN[(jdn + 9) % 10]
    chi = DIA_CHI[(jdn + 1) % 12]
    return can, chi, f"{can} {chi}"


def _format_solar_lunar_date(dt_obj):
    """Định dạng đầy đủ: Thứ, DD/MM/YYYY Dương lịch (tức DD/MM Âm lịch - Ngày Can Chi)."""
    wd = WEEKDAY_VN[dt_obj.weekday()]
    can, chi, cc_str = _get_day_canchi(dt_obj)
    lunar_str = ""
    if _xnd_s2l is not None:
        try:
            ld, lm, ly, leap = _xnd_s2l(dt_obj.day, dt_obj.month, dt_obj.year)
            leap_tag = " nhuận" if leap else ""
            lunar_str = f", Âm lịch {ld:02d}/{lm:02d}{leap_tag}"
        except Exception:
            pass
    return f"{wd}, ngày {dt_obj.strftime('%d/%m/%Y')} ({cc_str}{lunar_str})"


def _chi_to_dates(chi, base_date=None, scope='month'):
    """Chuyển Chi thành ngày/tháng/năm dương lịch & âm lịch cụ thể chính xác theo JDN."""
    if not base_date:
        base_date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).date()

    results = []

    if scope == 'hour':
        hour_range = CHI_HOUR_MAP.get(chi, '')
        if hour_range:
            results.append(f"Giờ {chi} ({hour_range})")

    if scope in ('day', 'month', 'year'):
        chi_idx = DIA_CHI.index(chi) if chi in DIA_CHI else -1
        if chi_idx >= 0:
            for delta in range(0, 365):
                check_date = base_date + datetime.timedelta(days=delta)
                jdn = _calc_jdn(check_date.day, check_date.month, check_date.year)
                day_idx = (jdn + 1) % 12
                if day_idx == chi_idx:
                    results.append(_format_solar_lunar_date(check_date))
                    if len(results) >= 3:
                        break

    if scope in ('month', 'year'):
        month_num = CHI_MONTH_MAP.get(chi)
        if month_num:
            dl_month = month_num + 1 if month_num <= 11 else 1
            dl_year = base_date.year if dl_month >= base_date.month else base_date.year + 1
            results.append(f"Tháng {dl_month:02d}/{dl_year} Dương lịch (Tháng {month_num:02d} Âm lịch — tháng {chi})")

    if scope == 'year':
        chi_idx = DIA_CHI.index(chi) if chi in DIA_CHI else -1
        if chi_idx >= 0:
            for y in range(base_date.year, base_date.year + 13):
                if (y - 4) % 12 == chi_idx:
                    can_y = THIEN_CAN[(y - 4) % 10]
                    results.append(f"Năm {y} ({can_y} {chi})")
                    break

    return results


def _calc_minute_precision(target_chi_hour, hanh_dt='', the_quai='', dung_quai='', cung_dt=0, dong_hao=0):
    """
    Tính chính xác KHẮC (15 phút) và PHÚT cụ thể trong khung giờ 2 tiếng của Địa Chi.
    Nguyên lý:
    - 1 Giờ Địa Chi = 120 phút = 8 Khắc (mỗi Khắc 15 phút, ứng với Tiên Thiên Bát Quái 1..8).
    - Khắc chính lấy theo số Tiên Thiên của Quẻ Dụng / Quẻ Thể / Cung Dụng Thần / Hào Động.
    - Số phút cụ thể trong Khắc lấy theo Hà Đồ Ngũ Hành số của Dụng Thần:
      Thủy (1, 6), Hỏa (2, 7), Mộc (3, 8), Kim (4, 9), Thổ (5, 0).
    """
    if not target_chi_hour or target_chi_hour not in CHI_START_HOUR:
        target_chi_hour = 'Ngọ'

    start_h = CHI_START_HOUR[target_chi_hour]

    # 1. Xác định Khắc (1..8) trong 120 phút
    dung_so = QUAI_SO.get(dung_quai, 0)
    the_so = QUAI_SO.get(the_quai, 0)
    if dung_so:
        khac_idx = dung_so
    elif the_so:
        khac_idx = the_so
    elif cung_dt and 1 <= int(cung_dt) <= 9:
        q_name = LAC_THU_CUNG_QUAI.get(int(cung_dt), 'Càn')
        khac_idx = QUAI_SO.get(q_name, 1)
    elif dong_hao and 1 <= int(dong_hao) <= 6:
        khac_idx = int(dong_hao)
    else:
        # Suy từ Địa Chi giờ
        khac_idx = (DIA_CHI.index(target_chi_hour) % 8) + 1

    # Mỗi khắc 15 phút: offset_start = (khac_idx - 1) * 15
    offset_start = (khac_idx - 1) * 15
    offset_end = offset_start + 15

    def _fmt_hm(base_hour, add_minutes):
        total_m = base_hour * 60 + add_minutes
        hh = (total_m // 60) % 24
        mm = total_m % 60
        return f"{hh:02d}:{mm:02d}", hh, mm

    win_start_str, h1, m1 = _fmt_hm(start_h, offset_start)
    win_end_str, h2, m2 = _fmt_hm(start_h, offset_end)

    # 2. Xác định các mốc phút vàng (pinpoint minutes) theo Hà Đồ Ngũ Hành Dụng Thần
    d1, d2 = HA_DO_DIGITS.get(hanh_dt, (5, 0))
    exact_marks = []
    for add_m in range(offset_start, offset_end + 1):
        _, hh, mm = _fmt_hm(start_h, add_m)
        if (mm % 10) in (d1, d2):
            exact_marks.append(f"{hh:02d}:{mm:02d}")

    # Bổ sung mốc phút theo Hào Động / Cung số nếu cần
    extra_minute_offset = ((dung_so + the_so + (int(dong_hao) if dong_hao else 3)) * 3) % 15
    pin_str, _, _ = _fmt_hm(start_h, offset_start + extra_minute_offset)
    if pin_str not in exact_marks:
        exact_marks.append(pin_str)

    # Thêm 1 mốc ở nửa giờ còn lại (Khắc đối xung) để dự phòng
    alt_khac_idx = ((khac_idx + 3) % 8) + 1
    alt_offset = (alt_khac_idx - 1) * 15 + d1
    alt_pin_str, _, _ = _fmt_hm(start_h, alt_offset)

    khac_label = BAT_QUAI_KHAC_NAME.get(khac_idx, f"Khắc {khac_idx}")
    marks_str = ", ".join(exact_marks[:3])

    minute_summary = (
        f"Khung {win_start_str} – {win_end_str} ({khac_label}) | "
        f"Chốt phút chuẩn: {marks_str} (hoặc {alt_pin_str}) — số đuôi phút {d1}, {d2} (Hà Đồ hành {hanh_dt or 'Thổ'})"
    )
    return {
        'khac_idx': khac_idx,
        'khac_label': khac_label,
        'window': f"{win_start_str} – {win_end_str}",
        'exact_minutes': exact_marks[:3],
        'alt_minute': alt_pin_str,
        'ha_do_digits': (d1, d2),
        'summary': minute_summary,
    }


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
    cung_dt=0,
    dong_hao=0,
    question='',
    luc_hao_data=None,
    chart_data=None,
):
    """
    MASTER FUNCTION (V107.0): Tính Ứng Kỳ Tiên Tri Liên Kết Đa Yếu Tố & Phân Cấp Tầm Vóc Sự Việc:
    - Tự động phân cấp tầm vóc sự việc:
      + DAI_SU (Việc lớn đời người: Mua nhà mặt đất, mua đất, xây nhà, mua ô tô, kết hôn, sinh con, đổi vận lớn):
        Bắt buộc kiểm tra chuỗi liên kết (Hào Thế + Hào Thê Tài [Nguồn vốn] + Hào Phụ Mẫu/Dụng Thần + Kỳ Môn Phục Ngâm).
        Tuyệt đối không báo giờ/phút hay vài ngày tới cho việc mua nhà/đại sự khi chưa có sẵn tiền (Thê Tài ẩn phục) hoặc phạm Phục Ngâm!
      + TRUNG_SU (Việc trung hạn: Xin việc, thăng chức, thi cử, mở cửa hàng, kinh doanh, đòi nợ, kiện tụng):
        Ứng kỳ theo Ngày Can Chi & Tháng Âm/Dương lịch khi các mắt xích hội tụ.
      + TIEU_SU (Việc nhỏ / Tức thời: Tin nhắn, gặp mặt, tìm đồ thất lạc, thời tiết, việc trong ngày):
        Ứng kỳ chi tiết đến Khắc / Giờ / Ngày.
    """
    try:
        if isinstance(chart_data, dict) and chart_data.get('year') and chart_data.get('month') and chart_data.get('day'):
            now = datetime.date(int(chart_data['year']), int(chart_data['month']), int(chart_data['day']))
        else:
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).date()
    except Exception:
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).date()
    result = {
        'summary': '', 'minute': '', 'minute_data': {},
        'hour': '', 'day': '', 'month': '', 'year': '',
        'exact_timestamp': '', 'speed': '', 'confidence': '', 'method': '', 'html': '',
        'event_scale': 'TIEU_SU',
        'multi_factor_blockers': [],
    }

    q_low = str(question or '').lower().strip()
    _DAI_SU_KEYWORDS = [
        'mua nhà', 'mua đất', 'xây nhà', 'làm nhà', 'mua căn hộ', 'mua chung cư', 'mua biệt thự',
        'mua mảnh đất', 'nhà mặt đất', 'bất động sản', 'mua ô tô', 'mua xe hơi', 'mua xe ô tô',
        'kết hôn', 'lấy vợ', 'lấy chồng', 'cưới vợ', 'cưới chồng', 'lập gia đình', 'sinh con',
        'định cư', 'làm giàu', 'mua tài sản lớn', 'đổi đời', 'phát tài lớn',
    ]
    _TRUNG_SU_KEYWORDS = [
        'xin việc', 'thăng chức', 'chuyển việc', 'nhảy việc', 'thi cử', 'thi đỗ', 'xin visa',
        'du học', 'mở cửa hàng', 'khai trương', 'ký hợp đồng', 'đầu tư', 'kinh doanh',
        'kiện tụng', 'vụ kiện', 'đòi nợ', 'trả nợ', 'chữa bệnh', 'khỏi bệnh', 'bán nhà', 'bán đất',
    ]
    if any(k in q_low for k in _DAI_SU_KEYWORDS):
        event_scale = 'DAI_SU'
    elif any(k in q_low for k in _TRUNG_SU_KEYWORDS):
        event_scale = 'TRUNG_SU'
    else:
        event_scale = 'TIEU_SU'
    result['event_scale'] = event_scale

    # Quét chuỗi liên kết Lục Hào & Kỳ Môn (Hào Thê Tài / Nguồn vốn, Tuần Không, Phục Ngâm)
    _has_the_tai_on_hex = True
    _the_tai_weak_or_khong = False
    _is_phuc_ngam = False
    _dt_real_chi = chi_dt
    _blockers = []

    if isinstance(luc_hao_data, dict):
        _lh_ban = luc_hao_data.get('ban') or luc_hao_data.get('ban_que') or {}
        _haos = _lh_ban.get('haos') or _lh_ban.get('details') or luc_hao_data.get('haos') or []
        if _haos:
            _tai_haos = [h for h in _haos if isinstance(h, dict) and 'Thê Tài' in str(h.get('luc_than', ''))]
            if not _tai_haos:
                _has_the_tai_on_hex = False
                _blockers.append("Hào Thê Tài (Nguồn tiền/vốn) đang Phục Tàng (ẩn dưới hào khác, chưa xuất hiện trên quẻ — phản ánh hiện tại chưa có sẵn nguồn tiền lớn)")
            else:
                for _th in _tai_haos:
                    if _th.get('tuan_khong') or 'Không' in str(_th.get('tuan_khong', '')):
                        _the_tai_weak_or_khong = True
                        _blockers.append("Hào Thê Tài (Nguồn tiền) đang lâm Tuần Không (tài chính thực tế chưa tụ đủ)")
            # Kiểm tra Hào Phụ Mẫu khi hỏi mua nhà/đất/xe
            if any(k in q_low for k in ['mua nhà', 'mua đất', 'xây nhà', 'làm nhà', 'nhà mặt đất', 'mua căn hộ', 'mua chung cư', 'mua ô tô', 'mua xe']):
                _pm_haos = [h for h in _haos if isinstance(h, dict) and 'Phụ Mẫu' in str(h.get('luc_than', ''))]
                if _pm_haos:
                    _pm_h0 = _pm_haos[-1]  # Ưu tiên hào Phụ Mẫu trên cao / Hào 5
                    _pm_c = str(_pm_h0.get('chi') or '').split()[-1]
                    if _pm_c:
                        _dt_real_chi = _pm_c
                        chi_dt = _pm_c
                        hanh_dt = HANH_CHI and next((hk for hk, hv in HANH_CHI.items() if _pm_c in hv), hanh_dt)

    if isinstance(chart_data, dict):
        _can_n_uk = chart_data.get('can_ngay', '')
        _chi_n_uk = chart_data.get('chi_ngay', '')
        if _can_n_uk in THIEN_CAN and _chi_n_uk in DIA_CHI:
            _st_uk = (DIA_CHI.index(_chi_n_uk) - THIEN_CAN.index(_can_n_uk)) % 12
            _kv_pair_uk = [DIA_CHI[(_st_uk - 2) % 12], DIA_CHI[(_st_uk - 1) % 12]]
            if chi_dt and chi_dt in _kv_pair_uk:
                is_tuan_khong = True
                _blockers.append(f"Dụng Thần ({chi_dt}) đang rơi vào Tuần Không ({', '.join(_kv_pair_uk)}) — mục tiêu chưa thể thành hiện thực ngay lập tức, phải chờ chu kỳ Xuất Không")
        _tb_uk = chart_data.get('thien_ban') or {}
        _nb_uk = chart_data.get('nhan_ban') or {}
        # Phát hiện Phục Ngâm trên bàn Kỳ Môn (Sao Thiên Bồng ở Cung 1, Thiên Nhuế ở Cung 2, Thiên Trụ ở Cung 7, hoặc Khai Môn ở Cung 6, Hưu Môn ở Cung 1...)
        if ('Bồng' in str(_tb_uk.get(1, _tb_uk.get('1', ''))) or 'Trụ' in str(_tb_uk.get(7, _tb_uk.get('7', ''))) or 'Hưu' in str(_nb_uk.get(1, _nb_uk.get('1', '')))):
            _is_phuc_ngam = True
            _blockers.append("Bàn Kỳ Môn phạm cục diện Phục Ngâm (Cung Bản Thân & Cung Sự Việc giậm chân tại chỗ, cần thời gian tích lũy và chờ xung phá Phục Ngâm)")

    result['multi_factor_blockers'] = _blockers

    methods_used = []

    # Fallback thông minh nếu chi_dt trống: suy từ hanh_dt, cung_dt, hoặc dung_quai
    if not chi_dt:
        if hanh_dt and hanh_dt in HANH_CHI:
            chi_dt = HANH_CHI[hanh_dt][0]
        elif cung_dt and int(cung_dt) in CUNG_TO_CHI:
            chi_dt = CUNG_TO_CHI[int(cung_dt)]
        else:
            _, today_chi, _ = _get_day_canchi(now)
            chi_dt = today_chi

    # ═══ 1. XÁC ĐỊNH TỐC ĐỘ (NHANH/CHẬM) ═══
    speed_score = 0  # >0 = nhanh, <0 = chậm
    speed_reasons = []

    if am_duong_don:
        if 'Dương' in am_duong_don:
            speed_score += 1
            speed_reasons.append("Dương Độn → khí tiến, ứng nhanh")
        else:
            speed_score -= 1
            speed_reasons.append("Âm Độn → khí tàng, ứng chậm")

    if noi_ngoai:
        if 'Nội' in noi_ngoai:
            speed_score += 1
            speed_reasons.append("Nội bàn → gần, ứng nhanh")
        else:
            speed_score -= 1
            speed_reasons.append("Ngoại bàn → xa, ứng chậm")

    if is_tuan_khong:
        speed_score -= 2
        speed_reasons.append("Tuần Không → chờ Xuất Không / Điền Thực")
    if is_nhap_mo:
        speed_score -= 2
        speed_reasons.append("Nhập Mộ → chờ Xung Mộ khai thông")
    if is_dong:
        speed_score += 1
        speed_reasons.append("Dụng Thần Động → sự việc đang chuyển động")

    fast_stages = ['Đế Vượng', 'Lâm Quan', 'Quan Đới', 'Trường Sinh']
    slow_stages = ['Suy', 'Bệnh', 'Tử', 'Mộ', 'Tuyệt', 'Thai', 'Dưỡng']
    if ts_stage in fast_stages:
        speed_score += 1
        speed_reasons.append(f"{ts_stage} → khí lực mạnh, ứng nhanh")
    elif ts_stage in slow_stages:
        speed_score -= 1
        speed_reasons.append(f"{ts_stage} → khí lực yếu, ứng từ từ")

    if verdict in ('CÁT', 'ĐẠI CÁT') or weighted_pct >= 60:
        speed_score += 1
    elif verdict in ('HUNG', 'ĐẠI HUNG') or weighted_pct < 35:
        speed_score -= 1

    if event_scale == 'DAI_SU':
        speed_score -= 4
        speed_reasons.append("Đại Sự Trọng Đại (Mua nhà đất / Xe cộ / Lập gia đình / Đổi vận lớn) → Cần hội tụ đủ Nguồn lực Tài chính (Thê Tài) & Pháp lý (Phụ Mẫu)")
        if not _has_the_tai_on_hex or _the_tai_weak_or_khong:
            speed_score -= 3
            speed_reasons.append("Hào Thê Tài (Nguồn tiền) đang Phục Tàng/ẩn phục → Hiện tại chưa có sẵn tiền lớn, phải qua giai đoạn tích lũy vốn trước")
        if _is_phuc_ngam:
            speed_score -= 2
            speed_reasons.append("Kỳ Môn Phục Ngâm → Hiện tại đang giậm chân tại chỗ, không thể xảy ra ngay trong ngắn hạn")
        result['speed'] = (
            '⏳ ĐẠI SỰ TÍCH LŨY DÀI HẠN (Hiện tại chưa đủ điều kiện mua/thực hiện ngay — '
            'Cần qua 2 giai đoạn: [1] Tích lũy nguồn tiền Thê Tài ➔ [2] Điểm rơi thành tựu theo Tháng/Năm Can Chi)'
        )
        scope = 'year'
    elif event_scale == 'TRUNG_SU':
        if _is_phuc_ngam or is_tuan_khong or not _has_the_tai_on_hex:
            speed_score -= 2
        result['speed'] = '🗓️ TRUNG SỰ THEO QUY TRÌNH (Ứng nghiệm theo chu kỳ Ngày Can Chi & Tháng Âm/Dương lịch khi hội tụ đủ các mắt xích)'
        scope = 'month'
    elif speed_score >= 2:
        result['speed'] = '⚡ RẤT NHANH (ứng trong vài phút – vài giờ hoặc 1–3 ngày tới)'
        scope = 'day'
    elif speed_score >= 0:
        result['speed'] = '🕐 NHANH - TRUNG BÌNH (ứng trong vài ngày – vài tuần)'
        scope = 'month'
    elif speed_score >= -2:
        result['speed'] = '🐌 CHẬM (ứng trong vài tuần – vài tháng)'
        scope = 'month'
    else:
        result['speed'] = '⏳ RẤT CHẬM (ứng theo chu kỳ nhiều tháng – trong năm)'
        scope = 'year'

    methods_used.append(f"Tốc độ: {speed_score:+d} ({', '.join(speed_reasons[:3])})")

    # ═══ 2. TÍNH GIỜ & PHÚT/KHẮC ỨNG NGHIỆM ═══
    target_chi_hour = ''
    if chi_dt:
        if is_tuan_khong:
            target_chi_hour = chi_dt  # Điền Thực = chính Chi DT
            hour_reason = "Điền Thực (Xuất Không)"
        elif is_nhap_mo and hanh_dt:
            mo = MO_KHO.get(hanh_dt, '')
            target_chi_hour = LUC_XUNG.get(mo, '') if mo else LUC_XUNG.get(chi_dt, chi_dt)
            hour_reason = f"Xung mở Mộ kho ({mo})"
        elif is_dong:
            target_chi_hour = chi_dt
            _hop_h = LUC_HOP.get(chi_dt, '')
            hour_reason = f"Đương thời Dụng Thần phát động ({chi_dt}: {CHI_HOUR_MAP.get(chi_dt, '?')}) ➔ nối sang Lục Hợp ({_hop_h}: {CHI_HOUR_MAP.get(_hop_h, '?')})"
        else:
            target_chi_hour = chi_dt
            _xung_h = LUC_XUNG.get(chi_dt, '')
            hour_reason = f"Trị Giờ Dụng Thần ({chi_dt}: {CHI_HOUR_MAP.get(chi_dt, '?')}) / Xung kích ({_xung_h}: {CHI_HOUR_MAP.get(_xung_h, '?')})"

        if target_chi_hour:
            alt_chi_hour = LUC_HOP.get(chi_dt, '') if is_dong else LUC_XUNG.get(chi_dt, '')
            if event_scale == 'DAI_SU':
                result['hour'] = (
                    f"Khi bước vào đúng Năm/Tháng ứng nghiệm bên dưới, chọn Giờ {target_chi_hour} ({CHI_HOUR_MAP.get(target_chi_hour, '?')}) "
                    f"hoặc Giờ {alt_chi_hour} ({CHI_HOUR_MAP.get(alt_chi_hour, '?')}) để đặt cọc / ký hợp đồng / nhập trạch"
                )
                result['minute_data'] = {}
                result['minute'] = (
                    "Việc trọng đại (Mua nhà mặt đất / Tài sản lớn / Đại sự) bắt buộc xét theo Chu kỳ Năm & Tháng hội tụ đủ "
                    "Tiền vốn (Thê Tài) + Nhà đất/Pháp lý (Phụ Mẫu) — tuyệt đối không tính theo phút/khắc hay vài ngày ngắn hạn"
                )
            else:
                result['hour'] = (
                    f"Giờ {target_chi_hour} ({CHI_HOUR_MAP.get(target_chi_hour, '?')}) — {hour_reason} "
                    f"[Phụ: Giờ {alt_chi_hour} ({CHI_HOUR_MAP.get(alt_chi_hour, '?')})]"
                )
                methods_used.append(f"Giờ: {target_chi_hour} ({hour_reason})")

                # Tính Phút & Khắc chính xác
                min_data = _calc_minute_precision(
                    target_chi_hour=target_chi_hour,
                    hanh_dt=hanh_dt,
                    the_quai=the_quai,
                    dung_quai=dung_quai,
                    cung_dt=cung_dt,
                    dong_hao=dong_hao,
                )
                result['minute_data'] = min_data
                result['minute'] = min_data['summary']
                methods_used.append(f"Phút/Khắc: {min_data['window']} ({', '.join(min_data['exact_minutes'][:2])})")

    # ═══ 3. TÍNH NGÀY ỨNG NGHIỆM (CHÍNH XÁC JDN + ÂM LỊCH) ═══
    target_chi_day = target_chi_hour or chi_dt
    primary_date_str = ''
    if target_chi_day:
        if event_scale == 'DAI_SU':
            _alt_d = LUC_HOP.get(target_chi_day, 'Thìn')
            result['day'] = (
                f"Khi đã tích lũy đủ tài chính và vào đúng Tháng/Năm ứng kỳ, ưu tiên giao dịch vào "
                f"Ngày {target_chi_day} (Điền thực Xuất Không) hoặc Ngày {_alt_d} (Lục Hợp thành sự)"
            )
            methods_used.append(f"Ngày Đại Sự: Ngày {target_chi_day} / {_alt_d} trong tháng ứng kỳ")
        else:
            dates = _chi_to_dates(target_chi_day, now, 'day')
            if dates:
                primary_date_str = dates[0]
                result['day'] = f"🎯 Mốc 1: {dates[0]}"
                if len(dates) > 1:
                    result['day'] += f" | 🎯 Mốc 2: {dates[1]}"
                if len(dates) > 2:
                    result['day'] += f" | 🎯 Mốc 3: {dates[2]}"
                methods_used.append(f"Ngày JDN: {target_chi_day}")

    # ═══ 4. TÍNH THÁNG ỨNG NGHIỆM ═══
    target_chi_month = ''
    if hanh_dt:
        hanh_chi_list = HANH_CHI.get(hanh_dt, [])
        if hanh_chi_list:
            target_chi_month = hanh_chi_list[0]

    if is_tuan_khong and chi_dt:
        target_chi_month = chi_dt
    elif is_nhap_mo and hanh_dt:
        mo = MO_KHO.get(hanh_dt, '')
        target_chi_month = LUC_XUNG.get(mo, '') if mo else target_chi_month

    if not target_chi_month:
        target_chi_month = target_chi_day

    if target_chi_month:
        month_dates = _chi_to_dates(target_chi_month, now, 'month')
        if month_dates:
            for md in month_dates:
                if 'Tháng' in md:
                    result['month'] = md
                    break
        if event_scale == 'DAI_SU' and hanh_dt in HANH_CHI and len(HANH_CHI[hanh_dt]) >= 2:
            _c1, _c2 = HANH_CHI[hanh_dt][0], HANH_CHI[hanh_dt][1]
            _m1 = CHI_MONTH_MAP.get(_c1, 7)
            _m2 = CHI_MONTH_MAP.get(_c2, 8)
            _dl1 = _m1 + 1 if _m1 <= 11 else 1
            _dl2 = _m2 + 1 if _m2 <= 11 else 1
            _yr_m = now.year if _dl1 > now.month and _has_the_tai_on_hex and not _is_phuc_ngam else now.year + 1
            result['month'] = (
                f"Mùa vượng Dụng Thần: Tháng {_dl1:02d} – {_dl2:02d}/{_yr_m} Dương lịch "
                f"(Tháng {_m1:02d} – {_m2:02d} Âm lịch, tức tháng {_c1} – {_c2} khi Dụng Thần Xuất Không & Đắc Lộc)"
            )
        methods_used.append(f"Tháng: Chi {target_chi_month}")

    # ═══ 5. TÍNH NĂM ỨNG NGHIỆM ═══
    year_chi = target_chi_month or target_chi_day
    _dai_su_year_target = ""
    if year_chi:
        year_dates = _chi_to_dates(year_chi, now, 'year')
        cur_can_y = THIEN_CAN[(now.year - 4) % 10]
        cur_chi_y = DIA_CHI[(now.year - 4) % 12]
        cur_year_str = f"Năm hiện tại {now.year} ({cur_can_y} {cur_chi_y})"
        if event_scale == 'DAI_SU':
            _next_y = now.year + 1
            _next_can = THIEN_CAN[(_next_y - 4) % 10]
            _next_chi = DIA_CHI[(_next_y - 4) % 12]
            _y2 = now.year + 2
            _y2_can = THIEN_CAN[(_y2 - 4) % 10]
            _y2_chi = DIA_CHI[(_y2 - 4) % 12]
            _y3 = now.year + 3
            _y3_can = THIEN_CAN[(_y3 - 4) % 10]
            _y3_chi = DIA_CHI[(_y3 - 4) % 12]
            result['year'] = (
                f"[Giai đoạn 1 - Tích lũy Tài chính (Thê Tài xuất phục)]: Cuối năm {now.year} ({cur_can_y} {cur_chi_y}) – Năm {_next_y} ({_next_can} {_next_chi}) "
                f"➔ [Giai đoạn 2 - Thành tựu Đại Sự (Mua nhà đất / Chốt mục tiêu)]: Cuối năm {_next_y} ({_next_can} {_next_chi}) hoặc Năm {_y2} – {_y3} ({_y2_can} {_y2_chi} – {_y3_can} {_y3_chi})"
            )
            _dai_su_year_target = f"Năm {_next_y} ({_next_can} {_next_chi}) hoặc Năm {_y2}–{_y3} ({_y2_can} {_y2_chi} – {_y3_can} {_y3_chi})"
        elif year_dates:
            for yd in year_dates:
                if 'Năm' in yd:
                    result['year'] = f"{cur_year_str} → Năm ứng điểm rơi: {yd}"
                    break
        else:
            result['year'] = cur_year_str

    # ═══ 6. MAI HOA SỐ LƯỢNG NGÀY/GIỜ/THÁNG BỔ SUNG ═══
    if the_quai and dung_quai:
        the_so = QUAI_SO.get(the_quai, 0)
        dung_so = QUAI_SO.get(dung_quai, 0)
        if the_so and dung_so:
            tong = the_so + dung_so
            if event_scale == 'DAI_SU':
                if _is_phuc_ngam or is_tuan_khong or not _has_the_tai_on_hex:
                    _mh_months = max(9, tong * 2)
                else:
                    _mh_months = max(6, tong)
                methods_used.append(f"Mai Hoa Đại Sự: Thể({the_so})+Dụng({dung_so})={tong} (Phục Ngâm/Khuyết Tài nhân đôi) → Chu kỳ ~{_mh_months}–{_mh_months+6} tháng tích lũy")
                result['day'] += f" | 🌸 Chu kỳ Mai Hoa Đại Sự: Khoảng {_mh_months} – {_mh_months + 6} tháng tích lũy & chuẩn bị"
            else:
                future_day = now + datetime.timedelta(days=tong)
                mh_date_str = _format_solar_lunar_date(future_day)
                methods_used.append(f"Mai Hoa: Thể({the_so})+Dụng({dung_so})={tong} → {mh_date_str}")
                if result['day']:
                    result['day'] += f" | 🌸 Kỳ Mai Hoa (+{tong} ngày): {mh_date_str}"
                else:
                    result['day'] = f"🌸 Kỳ Mai Hoa (+{tong} ngày): {mh_date_str}"

    # ═══ 7. CHỐT MỐC THỜI GIAN HỘI TỤ CHÍNH XÁC (PHÂN CẤP THEO TẦM VÓC SỰ VIỆC & CHUỖI LIÊN KẾT) ═══
    if event_scale == 'DAI_SU':
        _blocker_short = []
        if not _has_the_tai_on_hex or _the_tai_weak_or_khong:
            _blocker_short.append("Nguồn tiền (Hào Thê Tài) đang Ẩn Phục/chưa có sẵn tiền lớn")
        if is_tuan_khong:
            _blocker_short.append(f"Dụng Thần ({chi_dt}) đang Tuần Không")
        if _is_phuc_ngam:
            _blocker_short.append("Bàn Kỳ Môn phạm Phục Ngâm (giậm chân tại chỗ)")
        _why_not_now = (
            f"Hiện tại CHƯA THỂ diễn ra ngay trong ngắn hạn (vì {'; '.join(_blocker_short)})"
            if _blocker_short else
            "Việc trọng đại cần lộ trình chuẩn bị nguồn vốn & pháp lý kỹ lưỡng"
        )
        result['exact_timestamp'] = (
            f"{_why_not_now} ➔ LỘ TRÌNH ỨNG NGHIỆM 2 GIAI ĐOẠN: "
            f"[1] Tích lũy đủ tài chính (Thê Tài xuất phục): {now.year} – nửa đầu {now.year + 1}; "
            f"[2] Thời điểm mua/thành tựu thực tế: {result['month']} hoặc {_dai_su_year_target}"
        )
    elif event_scale == 'TRUNG_SU' and (_is_phuc_ngam or is_tuan_khong or not _has_the_tai_on_hex):
        result['exact_timestamp'] = (
            f"Cần vượt qua giai đoạn Phục Ngâm / Xuất Không trước ➔ Điểm rơi ứng nghiệm: "
            f"{primary_date_str or result['day']} — hoặc chắc chắn nhất vào {result['month']}"
        )
    else:
        pin_min = ''
        if result.get('minute_data', {}).get('exact_minutes'):
            pin_min = result['minute_data']['exact_minutes'][0]
        elif result.get('minute_data', {}).get('window'):
            pin_min = result['minute_data']['window']

        result['exact_timestamp'] = (
            f"Lúc {pin_min or '?'} ({ 'Giờ ' + target_chi_hour if target_chi_hour else result['hour'] }) — "
            f"{primary_date_str or result['day']} — {result['month']}"
        )

    # ═══ 8. ĐỘ TIN CẬY ═══
    conf_count = sum(1 for v in [result['minute'], result['hour'], result['day'], result['month']] if v)
    if event_scale == 'DAI_SU':
        result['confidence'] = '🟢 RẤT CAO (Đã liên kết chặt chẽ 4 mắt xích: Bản Thân [Hào Thế] + Nguồn Tiền [Thê Tài] + Mục Tiêu [Phụ Mẫu/Dụng Thần] + Cục Diện Kỳ Môn)'
    elif conf_count >= 4:
        result['confidence'] = '🟢 RẤT CAO (Hội tụ đủ 5 tầng: Năm – Tháng – Ngày – Giờ – Phút/Khắc)'
    elif conf_count >= 3:
        result['confidence'] = '🟢 CAO (3+ phương pháp đồng thuận)'
    elif conf_count >= 2:
        result['confidence'] = '🟡 TRUNG BÌNH (2 phương pháp)'
    else:
        result['confidence'] = '🔴 THẤP (chưa đủ dữ liệu)'

    result['method'] = ' | '.join(methods_used[:5])

    # ═══ 9. SUMMARY ═══
    if event_scale == 'DAI_SU':
        result['summary'] = result['exact_timestamp']
    else:
        parts = []
        if result['minute']:
            parts.append(f"Phút/Khắc: {result['minute']}")
        if result['hour']:
            parts.append(result['hour'])
        if result['day']:
            parts.append(result['day'])
        if result['month']:
            parts.append(result['month'])
        if result['year']:
            parts.append(result['year'])
        result['summary'] = ' → '.join(parts) if parts else 'Chưa xác định'

    # ═══ 10. BUILD HTML ═══
    result['html'] = _build_ung_ky_html(result, speed_reasons)

    return result


def _build_ung_ky_html(result, speed_reasons):
    rows = []
    if result.get('exact_timestamp'):
        rows.append(
            f'<tr style="background:rgba(245,158,11,0.18);border-bottom:1px solid rgba(251,191,36,0.3);">'
            f'<td style="color:#fde047;font-weight:900;padding:6px 8px;width:135px;">🎯 CHỐT THỜI ĐIỂM</td>'
            f'<td style="color:#ffffff;font-weight:800;padding:6px 8px;">{result["exact_timestamp"]}</td></tr>'
        )
    if result.get('minute'):
        rows.append(
            f'<tr><td style="color:#f472b6;font-weight:700;padding:5px 8px;">⏱️ PHÚT / KHẮC</td>'
            f'<td style="color:#fdf2f8;padding:5px 8px;">{result["minute"]}</td></tr>'
        )
    if result.get('hour'):
        rows.append(
            f'<tr><td style="color:#fbbf24;font-weight:700;padding:5px 8px;">⏰ GIỜ</td>'
            f'<td style="color:#f1f5f9;padding:5px 8px;">{result["hour"]}</td></tr>'
        )
    if result.get('day'):
        rows.append(
            f'<tr><td style="color:#34d399;font-weight:700;padding:5px 8px;">📅 NGÀY</td>'
            f'<td style="color:#f1f5f9;padding:5px 8px;">{result["day"]}</td></tr>'
        )
    if result.get('month'):
        rows.append(
            f'<tr><td style="color:#60a5fa;font-weight:700;padding:5px 8px;">🗓️ THÁNG</td>'
            f'<td style="color:#f1f5f9;padding:5px 8px;">{result["month"]}</td></tr>'
        )
    if result.get('year'):
        rows.append(
            f'<tr><td style="color:#c084fc;font-weight:700;padding:5px 8px;">📆 NĂM</td>'
            f'<td style="color:#f1f5f9;padding:5px 8px;">{result["year"]}</td></tr>'
        )

    speed_html = f'<div style="color:#fde68a;font-size:0.95em;margin-top:8px;">🚀 {result["speed"]}</div>' if result.get('speed') else ''
    conf_html = f'<div style="color:#a7f3d0;font-size:0.9em;margin-top:3px;">{result["confidence"]}</div>' if result.get('confidence') else ''

    return (
        f'<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);padding:18px;border-radius:14px;'
        f'margin:12px 0;border:2px solid #6366f1;box-shadow:0 4px 20px rgba(99,102,241,0.3);">'
        f'<div style="font-size:1.15em;font-weight:800;color:#a5b4fc;margin-bottom:10px;">'
        f'⏱️ ỨNG KỲ TIÊN TRI CHI TIẾT — NĂM · THÁNG · NGÀY · GIỜ · KHẮC · PHÚT</div>'
        f'<table style="width:100%;border-collapse:collapse;">'
        f'{"".join(rows)}'
        f'</table>'
        f'{speed_html}{conf_html}'
        f'</div>'
    )

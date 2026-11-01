"""
lich_van_nien_thien_van.py — Công cụ Lịch Vạn Niên, Đổi Ngày Âm - Dương 2 Chiều & Tiết Khí Thiên Văn
Tính toán dựa trên thuật toán thiên văn học (Julian Day Number, Kinh độ Hoàng Đạo Mặt Trời λ☉)
và Lịch Âm - Dương Việt Nam (múi giờ UTC+7).
"""

import math
import datetime
import calendar

try:
    import streamlit as st
    _cache_data = st.cache_data(ttl=3600, show_spinner=False)
except ImportError:
    st = None
    def _cache_data(func):
        return func

from xem_ngay_dep import _jdn, solar2lunar, CAN_10, CHI_12

WEEKDAY_NAMES = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
WEEKDAY_SHORT = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]

# Danh sách 24 Tiết Khí theo Kinh độ Hoàng Đạo Mặt Trời (bắt đầu từ Xuân Phân = 0°)
TIET_KHI_24 = [
    (0, "Xuân Phân", "Giữa xuân — Ngày và đêm dài bằng nhau, thời tiết ấm áp cân bằng."),
    (15, "Thanh Minh", "Trời trong sáng — Khí hậu mát mẻ, cây cối tốt tươi."),
    (30, "Cốc Vũ", "Mưa rào mùa xuân — Độ ẩm tăng, thuận lợi cho mùa màng sinh trưởng."),
    (45, "Lập Hạ", "Bắt đầu mùa hạ — Nhiệt độ tăng dần, ánh nắng dồi dào."),
    (60, "Tiểu Mãn", "Lúa chiêm bắt đầu chắc hạt — Nắng ấm xen kẽ mưa đầu mùa."),
    (75, "Mang Chủng", "Lúa có râu, mùa gặt và gieo trồng — Thời tiết nóng ẩm."),
    (90, "Hạ Chí", "Giữa mùa hạ — Ngày dài nhất trong năm ở Bắc bán cầu."),
    (105, "Tiểu Thử", "Nóng nhẹ — Nhiệt độ mùa hè tăng cao dần."),
    (120, "Đại Thử", "Nắng nóng đỉnh điểm — Độ ẩm và nhiệt độ cao nhất mùa hè."),
    (135, "Lập Thu", "Bắt đầu mùa thu — Gió mát bắt đầu về, nắng dịu dần."),
    (150, "Xử Thử", "Mưa ngâu / Hết nóng — Nhiệt độ giảm, tiết trời chuyển mát."),
    (165, "Bạch Lộ", "Nắng nhạt / Sương trắng — Đêm và sáng sớm bắt đầu se lạnh."),
    (180, "Thu Phân", "Giữa mùa thu — Ngày và đêm dài bằng nhau, tiết trời thu ôn hòa."),
    (195, "Hàn Lộ", "Sương lạnh — Không khí mát lạnh rõ rệt vào ban đêm."),
    (210, "Sương Giáng", "Sương mù giá lạnh — Cuối thu, chuẩn bị bước sang mùa đông."),
    (225, "Lập Đông", "Bắt đầu mùa đông — Gió mùa đông bắc hoạt động, trời chuyển lạnh."),
    (240, "Tiểu Tuyết", "Tuyết nhẹ / Hanh khô — Nhiệt độ giảm sâu hơn."),
    (255, "Đại Tuyết", "Trời rét đậm — Khí hậu mùa đông khô lạnh."),
    (270, "Đông Chí", "Giữa mùa đông — Đêm dài nhất trong năm ở Bắc bán cầu."),
    (285, "Tiểu Hàn", "Rét nhẹ — Không khí lạnh tăng cường."),
    (300, "Đại Hàn", "Rét đậm nhất năm — Giai đoạn cuối năm âm lịch."),
    (315, "Lập Xuân", "Bắt đầu mùa xuân — Vạn vật đâm chồi nảy lộc, khí ấm quay về."),
    (330, "Vũ Thủy", "Mưa xuân — Mưa phùn ẩm ướt, đất trời hồi sinh."),
    (345, "Kinh Trập", "Sâu bọ thức giấc — Sấm mùa xuân bắt đầu vang lên."),
]

GIO_DIA_CHI_INFO = [
    ("Tý", "23:00 – 01:00"),
    ("Sửu", "01:00 – 03:00"),
    ("Dần", "03:00 – 05:00"),
    ("Mão", "05:00 – 07:00"),
    ("Thìn", "07:00 – 09:00"),
    ("Tị", "09:00 – 11:00"),
    ("Ngọ", "11:00 – 13:00"),
    ("Mùi", "13:00 – 15:00"),
    ("Thân", "15:00 – 17:00"),
    ("Dậu", "17:00 – 19:00"),
    ("Tuất", "19:00 – 21:00"),
    ("Hợi", "21:00 – 23:00"),
]


@_cache_data
def calc_solar_longitude_deg(d: int, m: int, y: int, hour: float = 12.0, tz: float = 7.0) -> float:
    """
    Tính kinh độ Hoàng Đạo thực tế của Mặt Trời (0° – 360°) theo thuật toán thiên văn Jean Meeus.
    """
    jdn = _jdn(d, m, y)
    jd = jdn - 0.5 + (hour - tz) / 24.0
    T = (jd - 2451545.0) / 36525.0
    # Kinh độ trung bình của Mặt Trời (L0)
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * (T ** 2)
    L0 = L0 % 360.0
    # Dị thường trung bình của Mặt Trời (M)
    M = 357.52911 + 35999.05029 * T - 0.0001537 * (T ** 2)
    M_rad = math.radians(M % 360.0)
    # Phương trình tâm sai (C)
    C = (
        (1.914602 - 0.004817 * T - 0.000014 * (T ** 2)) * math.sin(M_rad)
        + (0.019993 - 0.000101 * T) * math.sin(2 * M_rad)
        + 0.000289 * math.sin(3 * M_rad)
    )
    true_long = (L0 + C) % 360.0
    # Hiệu chỉnh chương động biểu kiến (apparent longitude)
    omega = math.radians(125.04 - 1934.136 * T)
    lambda_sun = (true_long - 0.00569 - 0.00478 * math.sin(omega)) % 360.0
    return round(lambda_sun, 2)


@_cache_data
def get_tiet_khi_astronomical(d: int, m: int, y: int) -> dict:
    """Xác định Tiết Khí hiện tại, Kinh độ Mặt Trời và ngày sang Tiết Khí tiếp theo."""
    lon = calc_solar_longitude_deg(d, m, y)
    sector_idx = int(lon // 15) % 24
    start_deg, tk_name, tk_desc = TIET_KHI_24[sector_idx]
    next_idx = (sector_idx + 1) % 24
    next_deg, next_name, _ = TIET_KHI_24[next_idx]

    # Khoảng cách độ tới tiết khí kế tiếp (Mặt Trời di chuyển ~0.9856°/ngày)
    deg_remaining = (next_deg - lon) % 360.0
    days_remaining = max(1, int(round(deg_remaining / 0.9856)))
    next_date = datetime.date(y, m, d) + datetime.timedelta(days=days_remaining)

    return {
        "solar_longitude": lon,
        "name": tk_name,
        "start_deg": start_deg,
        "desc": tk_desc,
        "next_name": next_name,
        "next_deg": next_deg,
        "days_to_next": days_remaining,
        "next_date_str": next_date.strftime("%d/%m/%Y"),
    }


@_cache_data
def get_full_day_calendar_info(d: int, m: int, y: int) -> dict:
    """Tính toàn bộ thông tin Lịch Vạn Niên của một ngày Dương lịch."""
    dt = datetime.date(y, m, d)
    jdn = _jdn(d, m, y)
    ld, lm, ly, is_leap = solar2lunar(d, m, y)

    can_nam = CAN_10[(ly - 4) % 10]
    chi_nam = CHI_12[(ly - 4) % 12]

    # Can tháng Âm lịch (theo Ngũ Hổ Độn từ Can năm)
    can_nam_idx = (ly - 4) % 10
    start_can_dan = ((can_nam_idx % 5) * 2 + 2) % 10
    can_thang = CAN_10[(start_can_dan + (lm - 1)) % 10]
    chi_thang = CHI_12[(lm + 1) % 12]

    can_ngay_idx = (jdn + 9) % 10
    chi_ngay_idx = (jdn + 1) % 12
    can_ngay = CAN_10[can_ngay_idx]
    chi_ngay = CHI_12[chi_ngay_idx]

    # Can Giờ Tý (theo Ngũ Thử Độn từ Can ngày)
    start_can_ty = ((can_ngay_idx % 5) * 2) % 10
    hours_list = []
    for idx_h, (chi_h, range_h) in enumerate(GIO_DIA_CHI_INFO):
        can_h = CAN_10[(start_can_ty + idx_h) % 10]
        hours_list.append({
            "can_chi": f"{can_h} {chi_h}",
            "chi": chi_h,
            "range": range_h,
        })

    tk_info = get_tiet_khi_astronomical(d, m, y)

    return {
        "solar_str": dt.strftime("%d/%m/%Y"),
        "weekday": WEEKDAY_NAMES[dt.weekday()],
        "jdn": jdn,
        "lunar_day": ld,
        "lunar_month": lm,
        "lunar_year": ly,
        "is_leap": is_leap,
        "lunar_str": f"{ld:02d}/{lm:02d}/{ly}" + (" (Tháng Nhuận)" if is_leap else ""),
        "canchi_nam": f"{can_nam} {chi_nam}",
        "canchi_thang": f"{can_thang} {chi_thang}",
        "canchi_ngay": f"{can_ngay} {chi_ngay}",
        "tiet_khi": tk_info,
        "hours_list": hours_list,
    }


@_cache_data
def lunar_to_solar_search(ld_target: int, lm_target: int, ly_target: int, leap_target: bool = False):
    """
    Đổi ngược từ Ngày/Tháng/Năm Âm lịch sang Ngày/Tháng/Năm Dương lịch chính xác.
    """
    start_date = datetime.date(ly_target, 1, 1)
    end_date = datetime.date(ly_target + 1, 3, 15)
    curr = start_date
    fallback_match = None
    while curr <= end_date:
        ld, lm, ly, is_leap = solar2lunar(curr.day, curr.month, curr.year)
        if ld == ld_target and lm == lm_target and ly == ly_target:
            if bool(is_leap) == bool(leap_target):
                return curr
            if fallback_match is None:
                fallback_match = curr
        curr += datetime.timedelta(days=1)
    return fallback_match


def render_compact_today_banner():
    """Hiển thị thanh thông tin Lịch Vạn Niên & Tiết Khí hôm nay gọn nhẹ ở đầu trang."""
    today = datetime.date.today()
    info = get_full_day_calendar_info(today.day, today.month, today.year)
    tk = info["tiet_khi"]
    st.markdown(
        f"""
        <div style="background:linear-gradient(90deg,#0f172a,#1e1b4b,#0f172a);padding:10px 16px;border-radius:12px;
                    border:1px solid rgba(99,102,241,0.35);margin-bottom:14px;display:flex;flex-wrap:wrap;
                    align-items:center;justify-content:space-between;gap:8px;font-size:0.9rem;">
            <div>
                <span style="color:#38bdf8;font-weight:700;">☀️ Dương lịch:</span>
                <span style="color:#f8fafc;font-weight:600;"> {info['weekday']}, {info['solar_str']}</span>
                <span style="color:#64748b;margin:0 8px;">|</span>
                <span style="color:#fbbf24;font-weight:700;">🌙 Âm lịch:</span>
                <span style="color:#fef08a;font-weight:700;"> {info['lunar_str']}</span>
                <span style="color:#cbd5e1;"> (Ngày {info['canchi_ngay']} · Tháng {info['canchi_thang']} · Năm {info['canchi_nam']})</span>
            </div>
            <div>
                <span style="background:rgba(16,185,129,0.15);color:#6ee7b7;padding:4px 10px;border-radius:20px;
                             border:1px solid rgba(16,185,129,0.35);font-weight:600;font-size:0.85rem;">
                    🌿 Tiết khí: {tk['name']} (Mặt Trời {tk['solar_longitude']}°)
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_lich_van_nien_view():
    """Giao diện đầy đủ của Công cụ Lịch Vạn Niên, Đổi Ngày Âm - Dương & Tiết Khí Thiên Văn."""
    st.markdown(
        """
        <div style="text-align:center;margin-bottom:20px;">
            <h1 style="background:linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);-webkit-background-clip:text;
                       -webkit-text-fill-color:transparent;font-size:1.9rem;margin:0;">
                🗓️ LỊCH VẠN NIÊN & ĐỔI NGÀY ÂM – DƯƠNG THIÊN VĂN
            </h1>
            <p style="color:#94a3b8;font-size:0.92rem;margin-top:6px;">
                Tra cứu lịch Dương – Âm hai chiều • Can Chi chuẩn JDN • Kinh độ Hoàng Đạo Mặt Trời & 24 Tiết Khí thực tế
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_daily, tab_convert, tab_month, tab_tk24 = st.tabs([
        "📅 Chi Tiết Ngày & Tiết Khí",
        "🔄 Đổi Ngày Âm ⇄ Dương",
        "🗓️ Bảng Lịch Tháng",
        "🌏 24 Tiết Khí Thiên Văn",
    ])

    # ═══ TAB 1: CHI TIẾT NGÀY & TIẾT KHÍ ═══
    with tab_daily:
        col_sel, col_quick = st.columns([2, 1])
        with col_sel:
            selected_date = st.date_input(
                "Chọn ngày cần tra cứu:",
                value=datetime.date.today(),
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date(2100, 12, 31),
                key="lvn_selected_date",
            )
        with col_quick:
            st.write("")
            st.write("")
            if st.button("📍 Về Hôm Nay", use_container_width=True, key="lvn_btn_today"):
                selected_date = datetime.date.today()

        info = get_full_day_calendar_info(selected_date.day, selected_date.month, selected_date.year)
        tk = info["tiet_khi"]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f"""
                <div style="background:linear-gradient(145deg,#0f172a,#1e293b);padding:22px;border-radius:16px;
                            border:1px solid rgba(56,189,248,0.35);text-align:center;height:100%;">
                    <div style="color:#38bdf8;font-weight:700;font-size:0.95rem;letter-spacing:1px;">☀️ DƯƠNG LỊCH</div>
                    <div style="font-size:3.2rem;font-weight:900;color:#ffffff;line-height:1.1;margin:8px 0;">
                        {selected_date.day:02d}
                    </div>
                    <div style="font-size:1.15rem;color:#bae6fd;font-weight:700;">
                        {info['weekday']} — Tháng {selected_date.month:02d} Năm {selected_date.year}
                    </div>
                    <div style="color:#94a3b8;font-size:0.85rem;margin-top:8px;">
                        Số Ngày Julius (JDN): <b>{info['jdn']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div style="background:linear-gradient(145deg,#1e1b4b,#312e81);padding:22px;border-radius:16px;
                            border:1px solid rgba(251,191,36,0.4);text-align:center;height:100%;">
                    <div style="color:#fbbf24;font-weight:700;font-size:0.95rem;letter-spacing:1px;">🌙 ÂM LỊCH</div>
                    <div style="font-size:3.2rem;font-weight:900;color:#fde047;line-height:1.1;margin:8px 0;">
                        {info['lunar_day']:02d}
                    </div>
                    <div style="font-size:1.15rem;color:#fef3c7;font-weight:700;">
                        Tháng {info['lunar_month']:02d}{' (Nhuận)' if info['is_leap'] else ''} — Năm {info['canchi_nam']} ({info['lunar_year']})
                    </div>
                    <div style="color:#ddd6fe;font-size:0.9rem;margin-top:8px;">
                        Ngày: <b>{info['canchi_ngay']}</b> | Tháng: <b>{info['canchi_thang']}</b> | Năm: <b>{info['canchi_nam']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg,#064e3b,#0f172a);padding:18px 22px;border-radius:14px;
                        border:1px solid #10b981;margin:14px 0;">
                <div style="font-size:1.05rem;font-weight:800;color:#6ee7b7;margin-bottom:6px;">
                    🌏 THÔNG SỐ THIÊN VĂN & TIẾT KHÍ MẶT TRỜI (UTC+7)
                </div>
                <div style="color:#ecfdf5;font-size:0.95rem;line-height:1.6;">
                    • <b>Tiết khí hiện tại:</b> <span style="color:#fde047;font-weight:800;">{tk['name']}</span>
                    (Bắt đầu từ mốc kinh độ {tk['start_deg']}°)<br>
                    • <b>Kinh độ Hoàng Đạo Mặt Trời thực tế (λ☉):</b> <b>{tk['solar_longitude']}°</b><br>
                    • <b>Đặc điểm khí hậu / nông lịch:</b> {tk['desc']}<br>
                    • <b>Tiết khí tiếp theo:</b> <b>{tk['next_name']}</b> ({tk['next_deg']}°) —
                    dự kiến sau khoảng <b>{tk['days_to_next']} ngày</b> ({tk['next_date_str']})
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("🕐 Bảng 12 Giờ Địa Chi & Can Chi Giờ trong ngày", expanded=False):
            cols_h = st.columns(3)
            for idx, h_item in enumerate(info["hours_list"]):
                with cols_h[idx % 3]:
                    st.markdown(
                        f"<div style='background:#1e293b;padding:8px 12px;border-radius:8px;margin:4px 0;"
                        f"border-left:3px solid #38bdf8;font-size:0.9rem;'>"
                        f"<b style='color:#fde047;'>Giờ {h_item['can_chi']}</b><br>"
                        f"<span style='color:#cbd5e1;'>{h_item['range']}</span></div>",
                        unsafe_allow_html=True,
                    )

    # ═══ TAB 2: ĐỔI NGÀY ÂM ⇄ DƯƠNG HAI CHIỀU ═══
    with tab_convert:
        col_s2l, col_l2s = st.columns(2)
        with col_s2l:
            st.markdown("#### ☀️ ➜ 🌙 Đổi Dương Lịch sang Âm Lịch")
            d_in = st.date_input(
                "Chọn ngày Dương lịch:",
                value=datetime.date.today(),
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date(2100, 12, 31),
                key="conv_s2l_date",
            )
            res_s2l = get_full_day_calendar_info(d_in.day, d_in.month, d_in.year)
            st.success(
                f"**Kết quả Âm Lịch:** Ngày **{res_s2l['lunar_day']:02d}** "
                f"Tháng **{res_s2l['lunar_month']:02d}**{' (Nhuận)' if res_s2l['is_leap'] else ''} "
                f"Năm **{res_s2l['canchi_nam']} ({res_s2l['lunar_year']})**\n\n"
                f"• **Thứ:** {res_s2l['weekday']}\n"
                f"• **Can Chi:** Ngày {res_s2l['canchi_ngay']} – Tháng {res_s2l['canchi_thang']} – Năm {res_s2l['canchi_nam']}\n"
                f"• **Tiết khí:** {res_s2l['tiet_khi']['name']} ({res_s2l['tiet_khi']['solar_longitude']}°)"
            )

        with col_l2s:
            st.markdown("#### 🌙 ➜ ☀️ Đổi Âm Lịch sang Dương Lịch")
            today_l = get_full_day_calendar_info(
                datetime.date.today().day, datetime.date.today().month, datetime.date.today().year
            )
            c_ld, c_lm, c_ly = st.columns(3)
            with c_ld:
                ld_in = st.number_input("Ngày Âm:", min_value=1, max_value=30, value=int(today_l["lunar_day"]), key="conv_ld")
            with c_lm:
                lm_in = st.number_input("Tháng Âm:", min_value=1, max_value=12, value=int(today_l["lunar_month"]), key="conv_lm")
            with c_ly:
                ly_in = st.number_input("Năm Âm:", min_value=1900, max_value=2100, value=int(today_l["lunar_year"]), key="conv_ly")
            leap_in = st.checkbox("Tháng Nhuận", value=False, key="conv_leap")

            matched_solar = lunar_to_solar_search(int(ld_in), int(lm_in), int(ly_in), leap_in)
            if matched_solar:
                res_l2s = get_full_day_calendar_info(matched_solar.day, matched_solar.month, matched_solar.year)
                st.info(
                    f"**Kết quả Dương Lịch:** **{res_l2s['weekday']}, ngày {res_l2s['solar_str']}**\n\n"
                    f"• **Đối chiếu Âm lịch:** {res_l2s['lunar_str']}\n"
                    f"• **Can Chi:** Ngày {res_l2s['canchi_ngay']} – Tháng {res_l2s['canchi_thang']} – Năm {res_l2s['canchi_nam']}\n"
                    f"• **Tiết khí:** {res_l2s['tiet_khi']['name']} ({res_l2s['tiet_khi']['solar_longitude']}°)"
                )
            else:
                st.warning("Không tìm thấy ngày Âm lịch tương ứng (kiểm tra lại ngày 30 của tháng thiếu hoặc tháng nhuận).")

    # ═══ TAB 3: BẢNG LỊCH THÁNG (SONG SONG DƯƠNG - ÂM) ═══
    with tab_month:
        today_dt = datetime.date.today()
        cm1, cm2 = st.columns(2)
        with cm1:
            cal_month = st.selectbox("Tháng Dương lịch:", list(range(1, 13)), index=today_dt.month - 1, key="lvn_cal_m")
        with cm2:
            cal_year = st.number_input("Năm Dương lịch:", min_value=1900, max_value=2100, value=today_dt.year, key="lvn_cal_y")

        cal_matrix = calendar.monthcalendar(int(cal_year), int(cal_month))
        html_cal = [
            '<div style="overflow-x:auto;">',
            '<table style="width:100%;border-collapse:collapse;text-align:center;background:#0f172a;border-radius:12px;overflow:hidden;">',
            '<thead><tr style="background:#1e293b;color:#38bdf8;font-weight:800;">',
        ]
        for wd_label in WEEKDAY_SHORT:
            color_th = "#f87171" if wd_label == "CN" else "#38bdf8"
            html_cal.append(f'<th style="padding:10px 6px;border:1px solid #334155;color:{color_th};">{wd_label}</th>')
        html_cal.append('</tr></thead><tbody>')

        for week in cal_matrix:
            html_cal.append('<tr>')
            for idx_w, day_num in enumerate(week):
                if day_num == 0:
                    html_cal.append('<td style="padding:10px 4px;border:1px solid #1e293b;background:#090d16;"></td>')
                else:
                    ld_c, lm_c, _, _ = solar2lunar(day_num, int(cal_month), int(cal_year))
                    is_today = (day_num == today_dt.day and int(cal_month) == today_dt.month and int(cal_year) == today_dt.year)
                    bg_cell = "rgba(16,185,129,0.22)" if is_today else "#0f172a"
                    border_cell = "2px solid #10b981" if is_today else "1px solid #334155"
                    solar_color = "#f87171" if idx_w == 6 else ("#fde047" if is_today else "#f8fafc")
                    lunar_label = f"{ld_c}/{lm_c}" if (ld_c == 1 or day_num == 1) else f"{ld_c}"
                    lunar_color = "#fbbf24" if ld_c in (1, 15) else "#94a3b8"
                    html_cal.append(
                        f'<td style="padding:8px 4px;border:{border_cell};background:{bg_cell};">'
                        f'<div style="font-size:1.1rem;font-weight:800;color:{solar_color};">{day_num}</div>'
                        f'<div style="font-size:0.78rem;color:{lunar_color};font-weight:600;">{lunar_label}</div>'
                        f'</td>'
                    )
            html_cal.append('</tr>')
        html_cal.append('</tbody></table></div>')
        html_cal.append(
            '<div style="color:#94a3b8;font-size:0.82rem;margin-top:6px;">'
            '💡 <i>Số lớn ở trên: Ngày Dương lịch | Số nhỏ ở dưới: Ngày Âm lịch (màu vàng cam là ngày Mùng 1 và Rằm 15 Âm lịch).</i></div>'
        )
        st.markdown("".join(html_cal), unsafe_allow_html=True)

    # ═══ TAB 4: BẢNG 24 TIẾT KHÍ THIÊN VĂN ═══
    with tab_tk24:
        st.markdown("#### 🌏 Bảng Chu Kỳ 24 Tiết Khí Theo Kinh Độ Hoàng Đạo Mặt Trời")
        rows_tk = [
            '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.9rem;">',
            '<tr style="background:#1e293b;color:#38bdf8;font-weight:700;">'
            '<th style="padding:8px;border:1px solid #334155;">STT</th>'
            '<th style="padding:8px;border:1px solid #334155;">Tiết Khí</th>'
            '<th style="padding:8px;border:1px solid #334155;">Kinh độ Mặt Trời (λ☉)</th>'
            '<th style="padding:8px;border:1px solid #334155;">Ý nghĩa khí hậu & Nông lịch</th></tr>',
        ]
        for i_tk, (deg_tk, name_tk, desc_tk) in enumerate(TIET_KHI_24, 1):
            rows_tk.append(
                f'<tr style="border-bottom:1px solid #334155;">'
                f'<td style="padding:7px 8px;text-align:center;color:#94a3b8;">{i_tk}</td>'
                f'<td style="padding:7px 8px;font-weight:700;color:#fde047;">{name_tk}</td>'
                f'<td style="padding:7px 8px;text-align:center;color:#38bdf8;font-weight:600;">{deg_tk}°</td>'
                f'<td style="padding:7px 8px;color:#e2e8f0;">{desc_tk}</td></tr>'
            )
        rows_tk.append('</table></div>')
        st.markdown("".join(rows_tk), unsafe_allow_html=True)

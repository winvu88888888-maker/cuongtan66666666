"""
van_vat/__init__.py — V32.0 VẠN VẬT INDEX (Mô hình Lazy-Load)
═══════════════════════════════════════════════════════════════
AI CHỈ CẦN ĐỌC FILE NÀY (~100 dòng) rồi gọi hàm.
Dữ liệu được chia thành 5 module nhỏ theo Ngũ Hành:
    van_vat/kim.py    (~250 dòng)
    van_vat/moc.py    (~250 dòng)
    van_vat/thuy.py   (~250 dòng)
    van_vat/hoa.py    (~250 dòng)
    van_vat/tho.py    (~250 dòng)
    van_vat/truong_sinh.py  (~60 dòng) — 12 tầng trạng thái

Ưu điểm:
    ✅ AI chỉ load hành cần thiết (tiết kiệm 80% token)
    ✅ Lookup O(1) — tìm ngay không cần duyệt
    ✅ Dễ bảo trì — sửa 1 hành không ảnh hưởng hành khác
    ✅ Backward compatible — vẫn export 3 hàm cũ

Usage:
    from van_vat import get_van_vat_chi_tiet, format_van_vat_for_ai, get_tham_tu_mo_ta

V32.0 — QMDG System.
"""

# ═══ LAZY LOAD REGISTRY ═══
# Chỉ import khi cần, không load tất cả lên RAM

_CACHE = {}  # Cache đã load

def _load_hanh(hanh):
    """Load dữ liệu 1 hành duy nhất (lazy). Cache lại sau lần đầu."""
    if hanh in _CACHE:
        return _CACHE[hanh]
    
    module_map = {
        'Kim': '.kim',
        'Mộc': '.moc', 
        'Thủy': '.thuy',
        'Hỏa': '.hoa',
        'Thổ': '.tho',
    }
    
    mod_name = module_map.get(hanh)
    if not mod_name:
        return {}, {}
    
    try:
        import importlib
        mod = importlib.import_module(mod_name, package='van_vat')
        core = getattr(mod, 'CORE', {})
        expanded = getattr(mod, 'EXPANDED', {})
        _CACHE[hanh] = (core, expanded)
        return core, expanded
    except ImportError:
        return {}, {}


def _load_truong_sinh():
    """Load bảng 12 Trường Sinh."""
    if '_ts' in _CACHE:
        return _CACHE['_ts']
    try:
        from van_vat.truong_sinh import TRUONG_SINH_TRANG_THAI
        _CACHE['_ts'] = TRUONG_SINH_TRANG_THAI
        return TRUONG_SINH_TRANG_THAI
    except ImportError:
        return {}


# ═══ PUBLIC API (backward-compatible) ═══

def get_van_vat_chi_tiet(hanh, truong_sinh_stage):
    """Lấy mô tả vạn vật siêu chi tiết theo Hành + Trường Sinh.
    
    Returns: dict với 5 giác quan, đồ vật, người, bệnh, thú, cây...
    """
    core, expanded = _load_hanh(hanh)
    ts_data = _load_truong_sinh().get(truong_sinh_stage, {})
    
    if not core:
        return {'error': f'Không tìm thấy hành: {hanh}'}
    
    # Lấy đồ vật cụ thể theo tầng
    do_vat = core.get('do_vat', {}).get(truong_sinh_stage, 
             core.get('do_vat', {}).get('Lâm Quan', []))
    con_nguoi_tang = core.get('con_nguoi', {}).get(truong_sinh_stage,
                    core.get('con_nguoi', {}).get('ngoai_hinh', ''))
    nha_cua_tang = core.get('nha_cua', {}).get(truong_sinh_stage,
                   core.get('nha_cua', {}).get('chung', ''))
    dong_vat_tang = core.get('dong_vat', {}).get(truong_sinh_stage,
                    core.get('dong_vat', {}).get('chung', ''))
    
    return {
        'hanh': hanh, 'truong_sinh': truong_sinh_stage,
        'cap': ts_data.get('cap', ''),
        'tinh_chat': core.get('tinh_chat', ''),
        'hinh_dang': core.get('hinh_dang', ''),
        'kich_thuoc': ts_data.get('kich_thuoc', ''),
        'tinh_trang': ts_data.get('tinh_trang', ''),
        'tuoi_vat': ts_data.get('tuoi_vat', ''),
        'chat_luong': ts_data.get('chat_luong', ''),
        'mau_sac': core.get('mau_sac', ''),
        'chat_lieu': core.get('chat_lieu', ''),
        'thi_giac': core.get('thi_giac', {}),
        'thinh_giac': core.get('thinh_giac', {}),
        'khuu_giac': core.get('khuu_giac', {}),
        'vi_giac': core.get('vi_giac', {}),
        'xuc_giac': core.get('xuc_giac', {}),
        'trong_luong': ts_data.get('trong_luong', ''),
        'nhiet_do': ts_data.get('nhiet_do', ''),
        'am_thanh': ts_data.get('am_thanh', ''),
        'do_vat_cu_the': do_vat,
        'huong': core.get('huong', ''), 'mua': core.get('mua', ''),
        'so': ts_data.get('so', []), 'so_luong': ts_data.get('so_luong', ''),
        'con_nguoi': {
            'ngoai_hinh': core.get('con_nguoi', {}).get('ngoai_hinh', ''),
            'than_hinh': core.get('con_nguoi', {}).get('than_hinh', ''),
            'tinh_cach': core.get('con_nguoi', {}).get('tinh_cach', ''),
            'giong_noi': core.get('con_nguoi', {}).get('giong_noi', ''),
            'nghe_nghiep': core.get('con_nguoi', {}).get('nghe_nghiep', ''),
            'mo_ta_tang': con_nguoi_tang,
        },
        'nha_cua': nha_cua_tang,
        'benh_tat': {
            'loai': core.get('benh_tat', {}).get('chung', ''),
            'cu_the': core.get('benh_tat', {}).get('cu_the', []),
            'vi_tri': core.get('benh_tat', {}).get('vi_tri', ''),
        },
        'dong_vat': dong_vat_tang,
        'thuc_vat': core.get('thuc_vat', {}).get(truong_sinh_stage,
                    core.get('thuc_vat', {}).get('chung', '')),
        'xu_huong': ts_data.get('huong_phat_trien', ''),
    }


def format_van_vat_for_ai(hanh, truong_sinh_stage):
    """Format mô tả cho AI đọc — output text."""
    data = get_van_vat_chi_tiet(hanh, truong_sinh_stage)
    if 'error' in data:
        return ""
    
    ts = _load_truong_sinh().get(truong_sinh_stage, {})
    core, expanded = _load_hanh(hanh)
    
    lines = []
    lines.append(f"=== VẠN VẬT: {hanh} × {truong_sinh_stage} ({ts.get('cap', '?')}) ===")
    lines.append(f"Tính chất: {data['tinh_chat']}")
    lines.append(f"Hình dáng: {data['hinh_dang']} | Kích thước: {data['kich_thuoc']}")
    lines.append(f"Màu: {data['mau_sac']} | Chất liệu: {data['chat_lieu']}")
    lines.append(f"Tình trạng: {data['tinh_trang']} | Tuổi: {data.get('tuoi_vat', '?')}")
    lines.append(f"Chất lượng: {data['chat_luong']}")
    lines.append(f"Trọng lượng: {data['trong_luong']} | Nhiệt: {data['nhiet_do']}")
    
    # 5 giác quan
    tg = data.get('thi_giac', {})
    lines.append(f"👁️ Nhìn: {tg.get('mau', '')} | {tg.get('be_mat', '')} | {tg.get('anh_sang', '')}")
    ag = data.get('thinh_giac', {})
    lines.append(f"👂 Nghe: {ag.get('am_thanh', '')} | Giọng: {ag.get('giong_noi', '')}")
    kg = data.get('khuu_giac', {})
    lines.append(f"👃 Ngửi: {kg.get('mui', '')} | {kg.get('mui_dac_trung', '')}")
    vg = data.get('vi_giac', {})
    lines.append(f"👅 Vị: {vg.get('vi', '')} | Thực phẩm: {vg.get('thuc_pham', '')}")
    xg = data.get('xuc_giac', {})
    lines.append(f"✋ Sờ: {xg.get('cam_giac', '')} | {xg.get('be_mat', '')}")
    
    if data.get('do_vat_cu_the'):
        lines.append(f"🔮 Đồ vật: {', '.join(data['do_vat_cu_the'][:8])}")
    
    cn = data.get('con_nguoi', {})
    lines.append(f"🧑 Người: {cn.get('ngoai_hinh', '')} | {cn.get('than_hinh', '')}")
    lines.append(f"   Tính cách: {cn.get('tinh_cach', '')} | Giọng: {cn.get('giong_noi', '')}")
    lines.append(f"   Nghề: {cn.get('nghe_nghiep', '')}")
    if cn.get('mo_ta_tang'):
        lines.append(f"   Tầng {truong_sinh_stage}: {cn['mo_ta_tang']}")
    
    lines.append(f"🏠 Nhà: {data.get('nha_cua', '?')}")
    bt = data.get('benh_tat', {})
    lines.append(f"🏥 Bệnh: {bt.get('loai', '')} | Chi tiết: {', '.join(bt.get('cu_the', [])[:5])}")
    lines.append(f"🐾 Thú: {data.get('dong_vat', '')} | 🌿 Cây: {data.get('thuc_vat', '')}")
    lines.append(f"🧭 Hướng: {data['huong']} | Mùa: {data['mua']} | Số: {data['so']}")
    lines.append(f"📈 Xu hướng: {data.get('xu_huong', '?')}")
    
    # Mở rộng (nếu có)
    _LABEL = {
        'phuong_tien': '🚗 Phương tiện', 'trang_phuc': '👔 Trang phục',
        'thuc_pham': '🍜 Thực phẩm', 'do_uong': '🥤 Đồ uống',
        'khoang_san': '💎 Khoáng sản', 'cong_nghe': '📱 Công nghệ',
        'nhac_cu': '🎵 Nhạc cụ', 'the_thao': '⚽ Thể thao',
        'thoi_tiet': '🌤️ Thời tiết', 'cam_xuc': '🎭 Cảm xúc',
        'noi_that': '🛋️ Nội thất', 'y_te': '🏥 Y tế',
        'ton_giao': '⛪ Tôn giáo', 'dia_ly': '🗻 Địa lý',
        'bo_phan_co_the': '🦴 Cơ thể', 'gia_dung': '🏡 Gia dụng',
        'vu_khi': '🪖 Vũ khí', 'nong_nghiep': '🌾 Nông nghiệp',
        'nghe_thuat': '🖼️ Nghệ thuật', 'ky_thuat_so': '💻 Digital',
    }
    
    for cat, label in _LABEL.items():
        items = expanded.get(cat)
        if items is None:
            continue
        if isinstance(items, list):
            lines.append(f"{label}: {', '.join(items[:6])}")
        elif isinstance(items, dict):
            sub = items.get(truong_sinh_stage, items.get('chung', []))
            if isinstance(sub, list) and sub:
                lines.append(f"{label}: {', '.join(sub[:6])}")
    
    return "\n".join(lines)


def get_tham_tu_mo_ta(hanh, truong_sinh_stage, question=""):
    """Mô tả thám tử lắp ghép — 5 giác quan + đồ vật + người."""
    data = get_van_vat_chi_tiet(hanh, truong_sinh_stage)
    if 'error' in data:
        return ""
    
    _, expanded = _load_hanh(hanh)
    
    lines = []
    lines.append(f"🕵️ **THÁM TỬ LẮP GHÉP — {hanh} × {truong_sinh_stage}**")
    
    tg = data.get('thi_giac', {})
    lines.append(f"👁️ **Nhìn thấy:** Hình dáng {data['hinh_dang']}, kích thước {data['kich_thuoc']}. "
                 f"Màu {tg.get('mau', data['mau_sac'])}. Bề mặt {tg.get('be_mat', '')}. "
                 f"Tình trạng: {data['tinh_trang']}.")
    ag = data.get('thinh_giac', {})
    lines.append(f"👂 **Nghe:** {ag.get('am_thanh', 'Im lặng')}.")
    kg = data.get('khuu_giac', {})
    lines.append(f"👃 **Ngửi:** {kg.get('mui', 'Không mùi')}.")
    vg = data.get('vi_giac', {})
    lines.append(f"👅 **Vị:** {vg.get('vi', '?')}.")
    xg = data.get('xuc_giac', {})
    lines.append(f"✋ **Sờ:** {xg.get('cam_giac', '?')}. Nhiệt: {data.get('nhiet_do', '?')}. "
                 f"Nặng: {data.get('trong_luong', '?')}.")
    
    if data.get('do_vat_cu_the'):
        lines.append(f"🔮 **Đồ vật:** {', '.join(data['do_vat_cu_the'][:6])}")
    cn = data.get('con_nguoi', {})
    if cn.get('mo_ta_tang'):
        lines.append(f"🧑 **Người:** {cn['mo_ta_tang']}")
    
    # Quick expanded items
    _QUICK = [
        ('phuong_tien', '🚗'), ('trang_phuc', '👔'), ('khoang_san', '💎'),
        ('cam_xuc', '🎭'), ('bo_phan_co_the', '🦴'), ('gia_dung', '🏡'),
        ('y_te', '🏥'), ('dia_ly', '🗻'),
    ]
    for cat, icon in _QUICK:
        items = expanded.get(cat)
        if items is None:
            continue
        if isinstance(items, list):
            lines.append(f"{icon} **{cat.replace('_',' ').title()}:** {', '.join(items[:5])}")
        elif isinstance(items, dict):
            sub = items.get(truong_sinh_stage, items.get('chung', []))
            if isinstance(sub, list) and sub:
                lines.append(f"{icon} **{cat.replace('_',' ').title()}:** {', '.join(sub[:5])}")
    
    lines.append(f"📈 **Xu hướng:** {data.get('xu_huong', '?')}")
    return "\n".join(lines)

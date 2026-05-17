import datetime

# 1. Nhìn xa - gần (Timing)
def luan_nhin_xa_gan(is_duong_don, cung_dt, is_phan_ngam, is_phuc_ngam):
    """
    Luận xa/gần, nhanh/chậm dựa vào Dương Độn/Âm Độn, Cung, Phản/Phục ngâm
    - Dương Độn: cung 1,8,3,4 (Nội bàn) = gần/nhanh; cung 9,2,7,6 (Ngoại bàn) = xa/chậm
    - Âm Độn: ngược lại (Nội/Ngoại đảo ngược)
    - Phản ngâm = nhanh
    - Phục ngâm = chậm
    """
    if cung_dt is None or str(cung_dt) == '?':
        return "Không xác định cung Dụng Thần để luận xa-gần."
    
    try:
        cung = int(cung_dt)
    except ValueError:
        return "Cung Dụng Thần không hợp lệ."

    # Dương độn Nội bàn: 1, 8, 3, 4 | Ngoại bàn: 9, 2, 7, 6
    duong_don_noi_ban = [1, 8, 3, 4]
    
    is_noi_ban = False
    if is_duong_don:
        if cung in duong_don_noi_ban:
            is_noi_ban = True
    else:
        if cung not in duong_don_noi_ban and cung != 5:
            is_noi_ban = True # Âm độn thì Nội/Ngoại ngược lại

    # Xét Phản/Phục ngâm
    toc_do_ngam = ""
    if is_phan_ngam:
        toc_do_ngam = "Cục Phản Ngâm (nhanh, gấp gáp, thay đổi lặp lại)."
    elif is_phuc_ngam:
        toc_do_ngam = "Cục Phục Ngâm (chậm chạp, đình trệ, rên rỉ)."

    khoang_cach = "Gần, Nhanh (Nội bàn)" if is_noi_ban else "Xa, Chậm (Ngoại bàn)"
    
    res = f"Tốc độ / Khoảng cách: {khoang_cach}."
    if toc_do_ngam:
        res += f" ⚡ {toc_do_ngam}"
        
    return res

# 2. Bốn cách nhìn (Ngang, Dọc, Xa-Gần, Toàn bàn)
def luan_bon_cach_nhin(can_ngay, cua_dt, sao_dt, than_dt, hanh_can, hanh_cua, hanh_sao, xa_gan_str, tong_quan_9_cung=None):
    """
    1. Nhìn ngang: So sánh tương quan ngũ hành giữa các yếu tố cùng 1 cung (Can Ngày vs Cửa/Sao/Thần).
    2. Nhìn dọc: Thiên bàn - Địa bàn - Nhân bàn - Thần bàn phối hợp.
    3. Nhìn xa-gần: Vừa luận ở trên.
    4. Nhìn toàn bàn: Đại cục, ngoại ứng.
    """
    nhin_ngang = ""
    if hanh_can and hanh_cua:
        nhin_ngang = f"Cửa ({hanh_cua}) và Can ({hanh_can}) tương tác."
    else:
        nhin_ngang = "So sánh Ngũ Hành Cửa/Can trong cùng cung."
        
    nhin_doc = "Xem xét trục dọc: Thiên (Sao), Địa (Cung), Nhân (Cửa), Thần (Bát thần) để biết chiều sâu sự việc."
    
    nhin_toan_ban = tong_quan_9_cung if tong_quan_9_cung else "Quan sát toàn bộ 9 cung, mối quan hệ sinh khắc đại cục và ngoại ứng thực tế."
    
    return {
        "nhin_ngang": nhin_ngang,
        "nhin_doc": nhin_doc,
        "nhin_xa_gan": xa_gan_str,
        "nhin_toan_ban": nhin_toan_ban
    }

# 3. Vận hạn (Niên/Nguyệt/Nhật/Thời giá)
def luan_van_han(tu_tru_dict):
    """
    tu_tru_dict: dict chứa can_nam, chi_nam, can_thang, chi_thang, can_ngay, chi_ngay, can_gio, chi_gio
    Trả về đánh giá vận hạn theo Niên/Nguyệt/Nhật/Thời giá.
    """
    if not tu_tru_dict:
        return "Chưa có thông tin tứ trụ để luận vận hạn."
    
    nien = f"{tu_tru_dict.get('can_nam', '')} {tu_tru_dict.get('chi_nam', '')}".strip()
    nguyet = f"{tu_tru_dict.get('can_thang', '')} {tu_tru_dict.get('chi_thang', '')}".strip()
    nhat = f"{tu_tru_dict.get('can_ngay', '')} {tu_tru_dict.get('chi_ngay', '')}".strip()
    thoi = f"{tu_tru_dict.get('can_gio', '')} {tu_tru_dict.get('chi_gio', '')}".strip()
    
    return f"Niên giá ({nien}): Xem xu hướng năm. Nguyệt giá ({nguyet}): Xem trạng thái tháng. Nhật giá ({nhat}): Trạng thái ngày. Thời giá ({thoi}): Biến động tức thời."

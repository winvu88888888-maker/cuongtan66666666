"""
interaction_diagrams.py — V31.0 Dynamic Interaction Diagrams
Sơ đồ tương tác THỜI GIAN THỰC cho AI Offline Engine.

Mỗi sơ đồ có:
- template: ASCII art với {slot} placeholders → điền từ quẻ hiện tại
- formula: Công thức tính toán → score → kết luận
- keywords: Từ khóa match câu hỏi
- slot_keys: Danh sách slot cần điền
- pp_goc: Phương pháp gốc (mạnh nhất cho câu hỏi này)
- calc_func_id: ID function tính score

V31.0: Thêm SĐ_MASTER — SƠ ĐỒ QUAN TRỌNG NHẤT
→ Tập trung DT → Suy/Vượng → Vạn Vật Loại Tượng → Chi tiết câu trả lời
"""

# ═══════════════════════════════════════════════════════════════
# SĐ_MASTER — SƠ ĐỒ TRUNG TÂM: DỤNG THẦN → SUY VƯỢNG → VẠN VẬT
# ═══════════════════════════════════════════════════════════════
# Đây là sơ đồ QUAN TRỌNG NHẤT, áp dụng cho MỌI câu hỏi.
# Luôn được hiển thị dù hỏi loại gì.

DIAGRAM_MASTER = {
    'id': 'SD_MASTER',
    'name': 'SĐ MASTER: DỤNG THẦN → SUY VƯỢNG → VẠN VẬT LOẠI TƯỢNG',
    'pp_goc': ['Lục Hào', 'Kỳ Môn', 'Mai Hoa', 'Thiết Bản', 'Vạn Vật'],
    'keywords': [],  # Luôn hiển thị — không cần match
    'description': 'Sơ đồ trung tâm: Xác định Dụng Thần → Đánh giá Suy/Vượng 3 tầng → Tra Vạn Vật Loại Tượng → Chi tiết trả lời',
    'template': """
╔══════════════════════════════════════════════════════════════════════════╗
║  📐 SĐ MASTER: DỤNG THẦN → SUY VƯỢNG → VẠN VẬT LOẠI TƯỢNG            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ① XÁC ĐỊNH DỤNG THẦN                                                 ║
║  ┌─────────────────────────────────────────────┐                       ║
║  │ Câu hỏi: {question_short}                  │                       ║
║  │ Nhóm: {category_label}                      │                       ║
║  │ ➜ DỤNG THẦN: {dung_than}                    │                       ║
║  │   Hành DT: {hanh_dt}                        │                       ║
║  └─────────────────────────────────────────────┘                       ║
║       │                                                                ║
║       ▼                                                                ║
║  ② ĐÁNH GIÁ SUY VƯỢNG (3 Tầng)                                        ║
║  ┌─────────────────────────────────────────────────────────────┐       ║
║  │ Tầng 1: Lục Hào Raw Score                                  │       ║
║  │   Nguyệt Lệnh({nguyet_lenh}) {nguyet_tac_dong} DT          │       ║
║  │   + Nhật Thần({nhat_than}) {nhat_tac_dong} DT               │       ║
║  │   + NT({nguyen_than}) {nt_state}                            │       ║
║  │   − KT({ky_than}) {kt_state}                               │       ║
║  │   ± Đặc biệt: {dac_biet}                                   │       ║
║  │   ═══ LH Raw = {lh_raw_score:+d} → {lh_pct}%               │       ║
║  ├─────────────────────────────────────────────────────────────┤       ║
║  │ Tầng 2: 12 Trường Sinh                                     │       ║
║  │   {hanh_dt} tại {chi_reference} = {ts_stage}                │       ║
║  │   {ts_icon} Power = {ts_power}%                             │       ║
║  │   {ts_mota}                                                 │       ║
║  ├─────────────────────────────────────────────────────────────┤       ║
║  │ Tầng 3: Ngũ Khí                                            │       ║
║  │   {hanh_dt} tại Cung {cung_hanh} = {ngu_khi}               │       ║
║  │   Power = {nk_power}%                                       │       ║
║  └─────────────────────────────────────────────────────────────┘       ║
║       │                                                                ║
║       ▼                                                                ║
║  ╔═════════════════════════════════════════╗                           ║
║  ║ UNIFIED: {unified_pct}% — {tier_cap}   ║                           ║
║  ║ = LH({lh_pct}%)×50% + TS({ts_power}%)×30% + NK({nk_power}%)×20%   ║
║  ╚═════════════════════════════════════════╝                           ║
║       │                                                                ║
║       ▼                                                                ║
║  ③ VẠN VẬT LOẠI TƯỢNG (Hành {hanh_dt} × {tier_cap})                   ║
║  ┌─────────────────────────────────────────────────────────────┐       ║
║  │ 📐 Hình dáng   : {hinh_dang}                               │       ║
║  │ 🔧 Chất liệu   : {chat_lieu}                               │       ║
║  │ 🎨 Màu sắc     : {mau_sac}                                 │       ║
║  │ 🧭 Hướng       : {huong}                                   │       ║
║  │ 📏 Kích thước  : {kich_thuoc}                               │       ║
║  │ 🆕 Tình trạng  : {tinh_trang}                              │       ║
║  │ 🔢 Số lượng    : {so_luong}                                 │       ║
║  │ 💎 Chất lượng  : {chat_luong}                               │       ║
║  │ 🧑 Con người   : {con_nguoi}                                │       ║
║  │ 🏥 Sức khỏe    : {suc_khoe}                                │       ║
║  ├─────────────────────────────────────────────────────────────┤       ║
║  │ 🔮 Đồ vật cụ thể: {do_vat}                                 │       ║
║  │ 🏠 Nhà cửa      : {nha_cua}                                │       ║
║  │ 🧑 Người liên quan: {nguoi_lien_quan}                      │       ║
║  │ 🏥 Bệnh tật     : {benh_tat}                               │       ║
║  └─────────────────────────────────────────────────────────────┘       ║
║                                                                        ║
║  CÔNG THỨC: Unified% = LH×50% + TS×30% + NK×20%                       ║
║  → Unified ≥70% = VƯỢNG (CÁT) | 50-69% = TRUNG BÌNH | <50% = SUY     ║
╚══════════════════════════════════════════════════════════════════════════╝
""",
    'formula': 'Unified% = LH_raw_normalized×50% + TrườngSinh_power×30% + NgũKhí_power×20%',
    'conclusion_rules': {
        'high': (70, 100, '🟢 VƯỢNG — Sự việc THUẬN LỢI, đạt kết quả tốt'),
        'medium': (50, 69, '🟡 TRUNG BÌNH — Cần thêm nỗ lực, kết quả tùy điều kiện'),
        'low': (30, 49, '🟠 SUY — Khó khăn, cần cân nhắc kỹ'),
        'very_low': (0, 29, '🔴 RẤT YẾU — Bất lợi, nên tránh hoặc chờ'),
    },
}


# ═══════════════════════════════════════════════════════════════
# 17 SƠ ĐỒ THỂ LOẠI CÂU HỎI (SĐ0 — SĐ16)
# ═══════════════════════════════════════════════════════════════

DIAGRAMS = {
    'SD1': {
        'id': 'SD1',
        'name': 'SĐ1: CÓ/KHÔNG',
        'pp_goc': ['Lục Hào', 'Kỳ Môn'],
        'keywords': ['có không', 'được không', 'có nên', 'nên không', 'có thể', 'liệu có',
                     'có được', 'có thành', 'có đỗ', 'có đạt', 'có thắng', 'có tốt'],
        'template': """
┌─── SĐ1: CÓ/KHÔNG ───────────────────────────────┐
│  [Nguyệt: {nguyet_lenh}] ──{m_rel}──▶ DT        │
│                                   ▲               │
│  [Nhật: {nhat_than}] ────{n_rel}──┘               │
│                                                   │
│  DT: {dung_than} ({hanh_dt}) — {dt_state}         │
│   ▲ sinh: NT({nguyen_than}) {nt_state}            │
│   ▼ khắc: KT({ky_than}) {kt_state}               │
│            ▲ CừuT({cuu_than}) {cuu_state}         │
│                                                   │
│  ⚡ TK={tuan_khong} | NPhá={nguyet_pha}           │
│  🔄 Thế({the_state}) ↔ Ứng({ung_state})          │
│  ⚡ TSVK: {tham_sinh_vong_khac}                   │
│                                                   │
│  KM: BT(Cung{cung_bt}) {bt_sv_rel} SV(Cung{cung_sv}) │
├───────────────────────────────────────────────────┤
│ Score = {score_detail}                            │
│ = {total_score:+d} → {conclusion}                 │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Nguyệt(±8) + Nhật(±6) + NT(±6) − KT(±8) + TK(-15) + NPhá(-12) + TSVK(+10) + BT↔SV(±8)',
        'conclusion_rule': 'Score > 10 → CÓ | Score < -10 → KHÔNG | Giữa → LỠ CỠ',
    },

    'SD2': {
        'id': 'SD2',
        'name': 'SĐ2: TUỔI/SỐ',
        'pp_goc': ['Thiết Bản', 'Mai Hoa'],
        'keywords': ['tuổi', 'bao nhiêu tuổi', 'mấy tuổi', 'năm sinh', 'tuổi tác'],
        'template': """
┌─── SĐ2: TUỔI/SỐ ────────────────────────────────┐
│  Bát Quái DT: {bat_quai_dt} = số {bat_quai_so}   │
│  Tiên Thiên số: {tien_thien_so}                   │
│                                                   │
│  Tuổi tra sẵn: {tuoi_tra_san}                     │
│  ═══ Trung bình ≈ {tuoi_trung_binh} tuổi         │
│                                                   │
│  VẠN VẬT: {vv_con_nguoi}                         │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: Khoảng {tuoi_trung_binh} tuổi          │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Trung bình(Bát Quái số các PP)',
    },

    'SD3': {
        'id': 'SD3',
        'name': 'SĐ3: CÁI GÌ/LOẠI GÌ',
        'pp_goc': ['Mai Hoa', 'Vạn Vật'],
        'keywords': ['cái gì', 'loại gì', 'là gì', 'vật gì', 'sản xuất gì', 'kinh doanh gì',
                     'nghề gì', 'ngành gì', 'mặt hàng', 'sản phẩm gì', 'buôn bán gì'],
        'template': """
┌─── SĐ3: CÁI GÌ/LOẠI GÌ ────────────────────────┐
│  Thể Quái: {the_quai} ({the_quai_hanh})           │
│  Dụng Quái: {dung_quai} ({dung_quai_hanh})        │
│  Hỗ Quái: {ho_quai} (ẩn bên trong)               │
│                                                   │
│  Ngũ Hành DT: {hanh_dt}                          │
│  ┌────────────────────────────────────────┐       │
│  │ Hình: {hinh_dang}                      │       │
│  │ Chất: {chat_lieu}                      │       │
│  │ Màu:  {mau_sac}                        │       │
│  │ Hướng: {huong}                         │       │
│  │ Cơ thể: {co_the}                       │       │
│  └────────────────────────────────────────┘       │
│  Đồ vật cụ thể: {do_vat}                         │
│  Người: {nguoi_lien_quan}                         │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: Liên quan đến {hanh_dt}: {chat_lieu}   │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Bát Quái Tượng + Ngũ Hành Vật Chất + Vạn Vật Cụ Thể',
    },

    'SD4': {
        'id': 'SD4',
        'name': 'SĐ4: Ở ĐÂU/HƯỚNG NÀO',
        'pp_goc': ['Kỳ Môn', 'Đại Lục Nhâm'],
        'keywords': ['ở đâu', 'hướng nào', 'phương nào', 'tìm đâu', 'chỗ nào', 'nơi nào',
                     'để đâu', 'cất đâu'],
        'template': """
┌─── SĐ4: Ở ĐÂU ──────────────────────────────────┐
│  KM Cung DT: Cung {cung_dt} = {phuong_km}        │
│  LN Mạt Truyền: {mat_truyen} = {phuong_ln}       │
│                                                   │
│  Cửa: {cua_dt} → {cua_y_nghia}                   │
│  Bát Quái Tượng: {bat_quai_tuong}                 │
│  → Khoảng cách: {khoang_cach}                    │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: Hướng {phuong_km}, {bat_quai_tuong}    │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Cung KM → Phương + Mạt Truyền LN → Phương bổ sung',
    },

    'SD5': {
        'id': 'SD5',
        'name': 'SĐ5: KHI NÀO',
        'pp_goc': ['Đại Lục Nhâm', 'Lục Hào'],
        'keywords': ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'bao lâu'],
        'template': """
┌─── SĐ5: KHI NÀO ────────────────────────────────┐
│  LN Timeline:                                    │
│  [Sơ: {so_truyen}] → [Trung: {trung_truyen}]    │
│    (quá khứ)          (hiện tại)                 │
│                     → [Mạt: {mat_truyen}]        │
│                       (kết quả=tương lai)        │
│                                                   │
│  LH Ứng Kỳ: {ung_ky}                            │
│  DT {dt_state}: {ung_ky_detail}                  │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {ung_ky_ket_luan}                      │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Sơ→Trung→Mạt = timeline | DT Vượng+Tĩnh=nhanh | Suy=chậm',
    },

    'SD6': {
        'id': 'SD6',
        'name': 'SĐ6: TÀI LỘC/TIỀN BẠC',
        'pp_goc': ['Lục Hào', 'Kỳ Môn'],
        'keywords': ['tiền', 'tài chính', 'giàu', 'nghèo', 'đầu tư', 'lương', 'thu nhập',
                     'nợ', 'lãi', 'lỗ', 'vốn', 'kinh doanh', 'buôn bán', 'cổ phiếu', 'crypto'],
        'template': """
┌─── SĐ6: TÀI LỘC ────────────────────────────────┐
│  DT = Thê Tài ({hanh_dt})                        │
│  ThêTài: {the_tai_state}                          │
│  HuynhĐệ: {huynh_de_state} (cướp tài)           │
│  TửTôn: {tu_ton_state} (sinh tài)                │
│  QuanQuỷ: {quan_quy_state} (thuế/kiện)           │
│                                                   │
│  KM: Cửa={cua_dt} | Sinh Môn={sinh_mon}          │
│  Score = {score_detail}                           │
├───────────────────────────────────────────────────┤
│ = {total_score:+d} → {conclusion}                 │
└───────────────────────────────────────────────────┘
""",
        'formula': 'ThêTài_vượng(+10) + TửTôn_động(+6) − HuynhĐệ_động(-8) − QuanQuỷ_động(-6) + Cửa(±6)',
    },

    'SD7': {
        'id': 'SD7',
        'name': 'SĐ7: TÌNH DUYÊN',
        'pp_goc': ['Lục Hào', 'Mai Hoa'],
        'keywords': ['yêu', 'người yêu', 'vợ', 'chồng', 'hôn nhân', 'cưới', 'ly hôn',
                     'tình', 'hẹn hò', 'chia tay', 'duyên', 'tình cảm', 'lấy vợ', 'lấy chồng'],
        'template': """
┌─── SĐ7: TÌNH DUYÊN ─────────────────────────────┐
│  DT Duyên: {dt_duyen} ({dt_duyen_state})          │
│  DT+Ứng: {dt_ung_relation}                       │
│  NT hỗ trợ: {nt_relation} (gia đình ủng hộ?)     │
│  KT phá: {kt_relation} (tình địch?)              │
│                                                   │
│  MH: Thể({the_quai}) {the_dung_rel} Dụng({dung_quai}) │
│  → {the_dung_y_nghia}                             │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'DT_duyên_vượng(+10) + Hợp(+8) − Xung(-10) + Thể↔Dụng(±10)',
    },

    'SD8': {
        'id': 'SD8',
        'name': 'SĐ8: SỨC KHỎE/BỆNH TẬT',
        'pp_goc': ['Lục Hào', 'Kỳ Môn'],
        'keywords': ['bệnh', 'ốm', 'đau', 'sức khỏe', 'khỏe', 'chữa', 'phẫu thuật',
                     'ung thư', 'tai nạn', 'nguy hiểm', 'qua khỏi', 'cứu được'],
        'template': """
┌─── SĐ8: SỨC KHỎE ───────────────────────────────┐
│  Quan Quỷ (=bệnh): {quan_quy_state}              │
│    Ngũ Hành QQ: {qq_hanh} → {qq_benh}            │
│  Tử Tôn (=thuốc): {tu_ton_state}                 │
│                                                   │
│  QQ Vượng+Động = BỆNH NẶNG                       │
│  TửTôn Vượng = CHỮA ĐƯỢC                         │
│  QQ TuầnKhông = {qq_tk}                          │
│                                                   │
│  KM: TT={thien_tam} | Cửa={cua_dt}               │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'QQ_vượng(-10) + QQ_động(-8) + TửTôn_vượng(+8) + QQ_TK(+5=bệnh hư) + KM_ThiênTâm(+6)',
    },

    'SD9': {
        'id': 'SD9',
        'name': 'SĐ9: CÔNG VIỆC/SỰ NGHIỆP',
        'pp_goc': ['Lục Hào', 'Kỳ Môn'],
        'keywords': ['việc', 'công việc', 'sếp', 'thăng tiến', 'thăng chức', 'thi',
                     'xin việc', 'nghỉ việc', 'hợp đồng', 'sự nghiệp', 'khởi nghiệp'],
        'template': """
┌─── SĐ9: CÔNG VIỆC ───────────────────────────────┐
│  DT = Quan Quỷ ({hanh_dt})                       │
│  QuanQuỷ: {quan_quy_state}                       │
│  PhụMẫu: {phu_mau_state} (bảo trợ)              │
│  DT Trì Thế: {dt_tri_the}                        │
│                                                   │
│  KM: Cửa={cua_dt} | Khai Môn={khai_mon}          │
│  TA: Chủ↔Khách = {chu_khach}                     │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'QQ_vượng(+10) + PhụMẫu_vượng_động(+6) + Trì_Thế(+4) + KhaiMôn(+6) + Chủ>Khách(+5)',
    },

    'SD10': {
        'id': 'SD10',
        'name': 'SĐ10: KIỆN TỤNG',
        'pp_goc': ['Lục Hào', 'Kỳ Môn'],
        'keywords': ['kiện', 'kiện tụng', 'tòa', 'tranh chấp', 'thắng kiện', 'thua kiện'],
        'template': """
┌─── SĐ10: KIỆN TỤNG ─────────────────────────────┐
│  Thế (mình): {the_state}                         │
│  Ứng (đối phương): {ung_state}                   │
│  Thế↔Ứng: {the_ung_relation}                     │
│                                                   │
│  KM: BT(Cung{cung_bt}) {bt_sv_rel} SV(Cung{cung_sv}) │
│  Cửa: {cua_dt} → {cua_y_nghia}                   │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Thế_vượng(+10) − Ứng_vượng(-10) + BT_khắc_SV(+8) + Cửa(±6)',
    },

    'SD11': {
        'id': 'SD11',
        'name': 'SĐ11: MẤT ĐỒ/TÌM KIẾM',
        'pp_goc': ['Kỳ Môn', 'Mai Hoa'],
        'keywords': ['mất', 'tìm', 'thất lạc', 'trộm', 'mất cắp', 'đánh rơi',
                     'mất xe', 'mất điện thoại', 'mất tiền', 'mất ví'],
        'template': """
┌─── SĐ11: MẤT ĐỒ/TÌM ───────────────────────────┐
│  KM: Cung DT = Cung {cung_dt} → Hướng {phuong}   │
│  Cửa: {cua_dt} → {tim_duoc}                      │
│  Thể Quái: {the_quai} → Tượng vật: {tuong_vat}   │
│                                                   │
│  DT TuầnKhông: {dt_tk} → {tk_y_nghia}            │
│  LN Mạt Truyền: {mat_truyen} → {phuong_ln}       │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Khai/Sinh_Môn=TÌM ĐƯỢC | Tử/Tuyệt=MẤT HẲN | DT_TK=khó tìm',
    },

    'SD12': {
        'id': 'SD12',
        'name': 'SĐ12: XUẤT HÀNH/DI CHUYỂN',
        'pp_goc': ['Kỳ Môn', 'Lục Hào'],
        'keywords': ['đi', 'xuất hành', 'du lịch', 'di chuyển', 'chuyến đi', 'bay', 'về quê'],
        'template': """
┌─── SĐ12: XUẤT HÀNH ─────────────────────────────┐
│  KM: Cửa = {cua_dt} → {cua_xuat_hanh}            │
│  Dịch Mã: {dich_ma}                              │
│  KV Cung Đích: {kv_cung_dich}                    │
│  LH: DT + Dịch Mã: {dt_dich_ma}                  │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Khai/Hưu/Sinh=NÊN ĐI | Tử/Kinh=KHÔNG | DịchMã_động=SẼ ĐI',
    },

    'SD13': {
        'id': 'SD13',
        'name': 'SĐ13: AI (NGƯỜI NÀO)',
        'pp_goc': ['Mai Hoa', 'Đại Lục Nhâm'],
        'keywords': ['ai ', 'người nào', 'ai đó', 'là ai', 'ai vậy'],
        'template': """
┌─── SĐ13: AI (NGƯỜI) ────────────────────────────┐
│  MH Thể Quái: {the_quai} → {the_quai_nguoi}      │
│  Lục Thân LH: {luc_than_dt} → {luc_than_nguoi}   │
│  LN Thiên Tướng: {thien_tuong} → {tt_nguoi}      │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'Quái_tượng + Lục_Thân + Thiên_Tướng → mô tả NGƯỜI',
    },

    'SD14': {
        'id': 'SD14',
        'name': 'SĐ14: TẠI SAO/NGUYÊN NHÂN',
        'pp_goc': ['Lục Hào', 'Kỳ Môn'],
        'keywords': ['tại sao', 'vì sao', 'nguyên nhân', 'do đâu', 'lý do'],
        'template': """
┌─── SĐ14: TẠI SAO ───────────────────────────────┐
│  Kỵ Thần: {ky_than} ({kt_hanh}) → KHẮC DT       │
│  → Nguyên nhân: {kt_nguyen_nhan}                 │
│                                                   │
│  Hào Động: {hao_dong} → phát động = nguyên nhân  │
│  KM Cửa Hung: {cua_hung} → {cua_tro_ngai}        │
│  KM Thần Hung: {than_hung} → {than_nguon_goc}    │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'KỵThần_hành → loại nguyên nhân | Hào_Động → yếu tố phát động',
    },

    'SD15': {
        'id': 'SD15',
        'name': 'SĐ15: THẾ NÀO/TRẠNG THÁI',
        'pp_goc': ['Lục Hào', 'Kỳ Môn', 'Mai Hoa'],
        'keywords': ['thế nào', 'như thế nào', 'ra sao', 'tình trạng', 'tình hình'],
        'template': """
┌─── SĐ15: THẾ NÀO ───────────────────────────────┐
│  DT: {dung_than} — trạng thái: {dt_state}        │
│  Nguyệt sinh/khắc: {nguyet_xu_huong}             │
│  Hào Động/Tĩnh: {hao_dong_tinh}                  │
│                                                   │
│  MH: Thể({the_quai}) {the_dung_rel} Dụng({dung_quai}) │
│  KM: Cửa {cua_dt} + Sao {sao_dt} → {cach_giai}   │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'DT_trạng thái + Xu hướng + Cửa/Sao → CÁCH THỨC/TÌNH TRẠNG',
    },

    'SD16': {
        'id': 'SD16',
        'name': 'SĐ16: CÁI NÀO/CHỌN LỌC',
        'pp_goc': ['Mai Hoa', 'Kỳ Môn', 'Lục Hào'],
        'keywords': ['cái nào', 'chọn', 'nên chọn', 'hay là', 'hoặc', 'A hay B'],
        'template': """
┌─── SĐ16: CHỌN LỰA ─────────────────────────────┐
│  MH: Thể({the_quai}) = mình                      │
│  Dụng({dung_quai}) = lựa chọn A                  │
│  Biến({bien_quai}) = lựa chọn B                  │
│                                                   │
│  Dụng {dung_sinh_the} Thể → {dung_ket_luan}      │
│  Biến {bien_sinh_the} Thể → {bien_ket_luan}      │
│                                                   │
│  KM so sánh: Cung A({cung_a_diem}) vs B({cung_b_diem}) │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': 'So sánh: lựa chọn nào SINH Thể/DT nhiều nhất',
    },

    'SD0': {
        'id': 'SD0',
        'name': 'SĐ0: TỔNG QUÁT',
        'pp_goc': ['5 Phương Pháp'],
        'keywords': [],  # Fallback
        'template': """
┌─── SĐ0: TỔNG QUÁT ──────────────────────────────┐
│  KM: {km_verdict} | LH: {lh_verdict}             │
│  MH: {mh_verdict} | LN: {ln_verdict}             │
│  TA: {ta_verdict}                                 │
│                                                   │
│  CÁT: {cat_count}/5 | HUNG: {hung_count}/5       │
│  Unified: {unified_pct}% — {tier_cap}             │
├───────────────────────────────────────────────────┤
│ KẾT LUẬN: {conclusion}                            │
└───────────────────────────────────────────────────┘
""",
        'formula': '≥4CÁT=ĐẠI CÁT | ≥3CÁT=CÁT | 2/2=LỠ CỠ | ≥3HUNG=HUNG | ≥4HUNG=ĐẠI HUNG',
    },
}


# ═══════════════════════════════════════════════════════════════
# BẢNG PHƯƠNG → QUÁI MAPPING
# ═══════════════════════════════════════════════════════════════
CUNG_PHUONG = {
    1: 'Bắc', 2: 'Tây Nam', 3: 'Đông', 4: 'Đông Nam',
    5: 'Trung Tâm', 6: 'Tây Bắc', 7: 'Tây', 8: 'Đông Bắc', 9: 'Nam'
}

# Quái → Người (Vạn Vật Loại Tượng)
QUAI_NGUOI = {
    'Càn': 'Bố/ông, người có quyền lực, trưởng bối',
    'Khôn': 'Mẹ/bà, phụ nữ lớn tuổi, người hiền lành',
    'Chấn': 'Con trai trưởng, thanh niên năng động',
    'Tốn': 'Con gái trưởng, phụ nữ công nghệ/truyền thông',
    'Khảm': 'Con trai giữa, người trí tuệ, nghiên cứu',
    'Ly': 'Con gái giữa, người nổi tiếng, IT/truyền thông',
    'Cấn': 'Con trai út, trẻ nhỏ, người ít nói',
    'Đoài': 'Con gái út, ca sĩ, người vui vẻ',
}

# Kỵ Thần Lục Thân → Nguyên nhân
KY_THAN_NGUYEN_NHAN = {
    'Quan Quỷ': 'Áp lực công việc/bệnh tật/kiện tụng',
    'Thê Tài': 'Vấn đề tiền bạc/vợ/tình cảm',
    'Huynh Đệ': 'Bạn bè/anh em/cạnh tranh/bị lừa',
    'Phụ Mẫu': 'Gia đình/giấy tờ/hợp đồng/nhà cửa',
    'Tử Tôn': 'Con cái/phúc đức/niềm vui mất',
}


# ═══════════════════════════════════════════════════════════════
# HELPER: Match câu hỏi → Diagram ID
# ═══════════════════════════════════════════════════════════════
def match_question_to_diagram(question):
    """Match câu hỏi vào sơ đồ tương tác phù hợp nhất.
    Returns: (diagram_id, diagram_info)
    Luôn kèm SĐ_MASTER.
    """
    if not question:
        return 'SD0', DIAGRAMS['SD0']
    
    q = question.lower()
    best_id = 'SD0'
    best_score = 0
    
    for d_id, d_info in DIAGRAMS.items():
        if d_id == 'SD0':
            continue  # SD0 là fallback
        score = 0
        for kw in d_info.get('keywords', []):
            if kw in q:
                score += len(kw)
        if score > best_score:
            best_score = score
            best_id = d_id
    
    return best_id, DIAGRAMS[best_id]

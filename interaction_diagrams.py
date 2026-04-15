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

# ═══════════════════════════════════════════════════════════════
# V31.2: LÀM SẠCH CÂU HỎI (NOISE REMOVAL)
# ═══════════════════════════════════════════════════════════════

import re as _re

# Từ vô nghĩa / filler / noise thường gặp trong câu hỏi
_NOISE_WORDS = {
    # Filler / padding
    'ạ', 'á', 'ơi', 'nhé', 'nha', 'hen', 'ha', 'hả', 'nhỉ', 'đi', 'thôi',
    'vậy đó', 'đấy', 'nè', 'nghe', 'xem', 'giúp', 'giùm', 'dùm', 'hộ',
    'với', 'luôn', 'rồi', 'đây', 'kìa', 'kia', 'chút', 'xíu', 'tí', 'tý',
    # Lịch sự thừa (dài→ngắn)
    'cho tôi hỏi', 'cho em hỏi', 'em muốn hỏi', 'tôi muốn hỏi',
    'mình muốn hỏi', 'hỏi xíu', 'hỏi chút', 'hỏi tí', 'hỏi tý',
    'xin hỏi', 'cho hỏi', 'cho tôi', 'cho em', 'bạn ơi',
    'làm ơn', 'vui lòng', 'cảm ơn', 'thank', 'thanks',
    # Filler dài
    'thưa thầy', 'thưa cô', 'dạ thưa', 'dạ', 'vâng',
    # Noise internet
    'haha', 'hihi', 'huhu', 'hehe', 'lol', 'omg', 'ok', 'okay',
    '...', '!!!', '???', '!?',
}

# Regex patterns cần xóa
_NOISE_PATTERNS = [
    r'\.{2,}',           # ... (2+ dots)
    r'!{2,}',            # !!! (2+ exclamation)
    r'\?{2,}',           # ??? (2+ question marks) → giữ 1 ?
    r'~+',               # ~~~
    r'-{3,}',            # ---- 
    r'_{3,}',            # ____
    r'\*{2,}',           # ****
    r'#{2,}',            # ####
    r'@\w+',             # @username
    r'https?://\S+',     # URLs
    r'\b\d{10,}\b',      # Số điện thoại dài
    r'[^\w\sáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ,?.!;:\'\"()/-]',  # Ký tự lạ
]

def clean_question(text):
    """V31.2: Làm sạch câu hỏi — loại bỏ noise, dấu thừa, từ vô nghĩa.
    
    Input:  "xin hỏi ạ... bố tôi bệnh nặng hay không???!!! cảm ơn"
    Output: "bố tôi bệnh nặng hay không?"
    """
    if not text:
        return ""
    
    q = text.strip()
    
    # 1. Xóa regex noise patterns
    for pattern in _NOISE_PATTERNS:
        q = _re.sub(pattern, ' ', q)
    
    # 2. Xóa noise words (exact match, case-insensitive)
    # Sắp xếp dài→ngắn để match cụm từ trước
    sorted_noise = sorted(_NOISE_WORDS, key=len, reverse=True)
    q_lower = q.lower()
    for nw in sorted_noise:
        # Word boundary match để tránh xóa substring
        # VD: không xóa "ạ" trong "ạnh" 
        pattern = r'(?:^|\s)' + _re.escape(nw) + r'(?:\s|[,?.!;:]|$)'
        q = _re.sub(pattern, ' ', q, flags=_re.IGNORECASE)
    
    # 3. Normalize whitespace
    q = _re.sub(r'\s+', ' ', q).strip()
    
    # 4. Sửa dấu câu kép: "??" → "?", "!!" → "!"
    q = _re.sub(r'\?+', '?', q)
    q = _re.sub(r'!+', '!', q)
    q = _re.sub(r',+', ',', q)
    q = _re.sub(r'\.+', '.', q)
    
    # 5. Xóa dấu câu ở đầu
    q = q.lstrip(',.;:!?-_ ')
    
    # 6. Nếu sau khi clean quá ngắn (< 3 ký tự) → trả về original
    if len(q) < 3:
        return text.strip()
    
    return q


# ═══════════════════════════════════════════════════════════════
# V31.1: PHÂN TÁCH CÂU HỎI PHỨC HỢP (COMPOUND QUESTION PARSER)
# ═══════════════════════════════════════════════════════════════

# Bảng người → Dụng Thần
PERSON_DUNG_THAN = {
    # Dài nhất trước (ưu tiên match chính xác)
    'con trai': 'Tử Tôn', 'con gái': 'Tử Tôn',
    'bạn trai': 'Quan Quỷ', 'bạn gái': 'Thê Tài',
    'người yêu': 'Thê Tài',
    'anh trai': 'Huynh Đệ', 'chị gái': 'Huynh Đệ',
    'bố': 'Phụ Mẫu', 'mẹ': 'Phụ Mẫu', 'cha': 'Phụ Mẫu',
    'ba': 'Phụ Mẫu', 'má': 'Phụ Mẫu',
    'ông': 'Phụ Mẫu', 'bà': 'Phụ Mẫu',
    'con': 'Tử Tôn', 'cháu': 'Tử Tôn',
    'vợ': 'Thê Tài', 'chồng': 'Quan Quỷ',
    'anh': 'Huynh Đệ', 'chị': 'Huynh Đệ', 'em': 'Huynh Đệ',
    'sếp': 'Quan Quỷ', 'thầy': 'Phụ Mẫu', 'cô': 'Phụ Mẫu',
    'bạn': 'Huynh Đệ', 'đối tác': 'Huynh Đệ',
    'tôi': 'Bản Thân', 'mình': 'Bản Thân', 'em ': 'Bản Thân',
}

# Bảng chủ đề → Category
TOPIC_KEYWORDS = {
    'SỨC_KHỎE': ['bệnh', 'ốm', 'đau', 'sức khỏe', 'khỏe', 'chết', 'sống',
                  'chữa', 'viện', 'phẫu thuật', 'ung thư', 'tai nạn',
                  'qua khỏi', 'cứu', 'nặng', 'nhẹ', 'thuốc', 'mổ'],
    'TÀI_CHÍNH': ['tiền', 'tài chính', 'đầu tư', 'lương', 'nợ', 'vay',
                  'kinh doanh', 'buôn bán', 'lãi', 'lỗ', 'giàu', 'nghèo',
                  'vốn', 'cổ phiếu', 'crypto', 'mua bán', 'thu nhập'],
    'CÔNG_VIỆC': ['việc', 'công việc', 'sếp', 'thăng tiến', 'thi', 'đỗ',
                  'xin việc', 'nghỉ việc', 'hợp đồng', 'sự nghiệp', 'học'],
    'TÌNH_CẢM':  ['yêu', 'tình', 'hôn nhân', 'cưới', 'ly hôn', 'chia tay',
                  'duyên', 'hẹn hò', 'thật lòng', 'ngoại tình', 'tình cảm'],
    'TÌM_ĐỒ':   ['mất', 'tìm', 'ở đâu', 'thất lạc', 'trộm', 'để đâu'],
}

# Loại câu hỏi → Diagram mapping
QTYPE_PATTERNS = [
    # (keywords_list, question_type, diagram_id, label)
    (['có nên', 'có được', 'được không', 'nên không', 'có thể', 'liệu có',
      'có thành', 'có đỗ', 'có không', 'hay không', 'có tốt', 'nặng hay không',
      'khỏi không', 'sống không', 'chết chưa'], 'CÓ/KHÔNG', 'SD1', '❓ CÓ/KHÔNG'),
    (['khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'bao lâu'], 'KHI NÀO', 'SD5', '⏰ KHI NÀO'),
    (['ở đâu', 'hướng nào', 'phương nào', 'chỗ nào', 'để đâu'], 'Ở ĐÂU', 'SD4', '📍 Ở ĐÂU'),
    (['bao nhiêu tuổi', 'mấy tuổi', 'tuổi'], 'TUỔI', 'SD2', '🔢 TUỔI'),
    (['bao nhiêu', 'mấy', 'số lượng'], 'SỐ LƯỢNG', 'SD2', '🔢 SỐ LƯỢNG'),
    (['cái gì', 'loại gì', 'là gì', 'vật gì', 'nghề gì', 'ngành gì'], 'CÁI GÌ', 'SD3', '❓ CÁI GÌ'),
    (['ai ', 'người nào', 'là ai', 'ai vậy'], 'AI', 'SD13', '👤 AI'),
    (['tại sao', 'vì sao', 'nguyên nhân', 'do đâu', 'lý do'], 'TẠI SAO', 'SD14', '❓ TẠI SAO'),
    (['thế nào', 'như thế nào', 'ra sao', 'tình trạng'], 'THẾ NÀO', 'SD15', '📊 THẾ NÀO'),
    (['chọn', 'nên chọn', 'cái nào', 'hay là', 'hoặc'], 'CHỌN', 'SD16', '⚖️ CHỌN'),
]

def _detect_question_type(text):
    """Xác định loại câu hỏi từ text.
    Returns: (question_type, diagram_id, label)
    """
    q = text.lower()
    for keywords, qtype, d_id, label in QTYPE_PATTERNS:
        for kw in keywords:
            if kw in q:
                return qtype, d_id, label
    return 'CHUNG', 'SD0', '❓ TỔNG QUÁT'


def _detect_person(text):
    """Xác định hỏi cho AI (ai hỏi) và hỏi về AI (hỏi cho ai).
    Returns: (person_label, dung_than_override, person_keyword)
    """
    import re
    q = text.lower()
    # Sort by length desc → match longest first
    sorted_persons = sorted(PERSON_DUNG_THAN.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Từ ngắn dễ match sai (ông→không, ba→bao, em→em) → cần word boundary
    short_ambiguous = {'ông', 'bà', 'ba', 'má', 'em', 'cô', 'con', 'bạn'}
    
    def _word_match(keyword, text):
        """Match keyword as a whole word (không match substring)."""
        if keyword in short_ambiguous:
            # Word boundary: trước keyword phải là đầu chuỗi hoặc space
            # Sau keyword phải là cuối chuỗi, space, hoặc ' tôi', ' của'
            pattern = r'(?:^|\s)' + re.escape(keyword) + r'(?:\s|$)'
            return bool(re.search(pattern, text))
        return keyword in text
    
    # Tìm "cho ai" patterns
    for_patterns = ['cho ', 'của ', 'về ', 'hỏi ']
    for pattern in for_patterns:
        idx = q.find(pattern)
        if idx >= 0:
            remainder = q[idx + len(pattern):]
            for person_kw, dt in sorted_persons:
                if remainder.startswith(person_kw) or f' {person_kw}' in remainder[:20]:
                    return person_kw.title(), dt, person_kw
    
    # Tìm "ai + keyword" patterns (VD: "bố tôi bệnh")
    for person_kw, dt in sorted_persons:
        if _word_match(person_kw, q):
            # Bỏ qua "tôi", "mình", "em " nếu đang tìm subject (tôi = mặc định)
            if person_kw in ['tôi', 'mình', 'em ']:
                continue
            return person_kw.title(), dt, person_kw
    
    return None, None, None


def _detect_topic(text):
    """Xác định chủ đề câu hỏi.
    Returns: (topic_key, topic_label)
    """
    q = text.lower()
    best_topic = 'CHUNG'
    best_score = 0
    
    TOPIC_LABELS = {
        'SỨC_KHỎE': '🏥 Sức Khỏe',
        'TÀI_CHÍNH': '💰 Tài Chính',
        'CÔNG_VIỆC': '💼 Công Việc',
        'TÌNH_CẢM': '❤️ Tình Cảm',
        'TÌM_ĐỒ': '🔍 Tìm Đồ',
        'CHUNG': '❓ Tổng Quát',
    }
    
    for topic_key, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in q:
                score += len(kw)
        if score > best_score:
            best_score = score
            best_topic = topic_key
    
    return best_topic, TOPIC_LABELS.get(best_topic, '❓')


def split_compound_question(full_question):
    """V31.1: Phân tách câu hỏi phức hợp thành danh sách câu hỏi con.
    
    Xử lý:
    - Câu hỏi dài gộp nhiều ý
    - Nhiều câu hỏi nối bằng "và", ",", "?"
    - Xác định WHO, WHAT, TYPE cho từng câu hỏi con
    
    VD Input: "bố tôi bị bệnh nặng hay không và khi nào sẽ khỏi?"
    Output: [
        {
            'text': 'bố tôi bị bệnh nặng hay không',
            'person': 'Bố', 'dung_than': 'Phụ Mẫu',
            'topic': 'SỨC_KHỎE', 'topic_label': '🏥 Sức Khỏe',
            'qtype': 'CÓ/KHÔNG', 'diagram_id': 'SD1', 'qtype_label': '❓ CÓ/KHÔNG',
            'index': 1,
        },
        {
            'text': 'khi nào sẽ khỏi',
            'person': 'Bố', 'dung_than': 'Phụ Mẫu',  # inherited from first
            'topic': 'SỨC_KHỎE', 'topic_label': '🏥 Sức Khỏe',
            'qtype': 'KHI NÀO', 'diagram_id': 'SD5', 'qtype_label': '⏰ KHI NÀO',
            'index': 2,
        },
    ]
    """
    if not full_question or len(full_question.strip()) < 3:
        return []
    
    # V31.2: Làm sạch câu hỏi trước khi phân tách
    q = clean_question(full_question)
    if len(q) < 3:
        return []
    
    # ═══ BƯỚC 1: TÁCH CÂU HỎI ═══
    # Delimiters:?, dấu phẩy trước từ nối, "và", "thêm nữa", newline
    import re
    
    # Tách theo ? (nhưng giữ nội dung)
    parts = re.split(r'\?\s*', q)
    parts = [p.strip() for p in parts if p.strip()]
    
    # Tách tiếp theo "và" / "," nếu phần con có > 10 ký tự
    expanded = []
    for part in parts:
        # Tách theo " và " hoặc ", " khi có từ khóa câu hỏi phía sau
        sub_splits = re.split(r'\s*(?:,\s+và\s+|,\s+|\s+và\s+|\s+thêm nữa\s+|\s+ngoài ra\s+|\s+còn\s+)', part)
        for s in sub_splits:
            s = s.strip().rstrip('?.,;')
            if len(s) >= 5:  # Tối thiểu 5 ký tự
                expanded.append(s)
    
    # Nếu không tách được gì → giữ nguyên 1 câu
    if not expanded:
        expanded = [q.rstrip('?.,;')]
    
    # ═══ BƯỚC 2: PHÂN TÍCH TỪNG CÂU ═══
    results = []
    
    # Phân tích câu gốc trước → lấy context chung (person, topic)
    global_person, global_dt, global_person_kw = _detect_person(q)
    global_topic, global_topic_label = _detect_topic(q)
    
    for i, sub_q in enumerate(expanded):
        # Phân tích riêng cho từng câu con
        person, dt_override, person_kw = _detect_person(sub_q)
        topic, topic_label = _detect_topic(sub_q)
        qtype, diagram_id, qtype_label = _detect_question_type(sub_q)
        
        # Inherit context từ câu trước nếu câu con thiếu
        if not person and global_person:
            person = global_person
            dt_override = global_dt
            person_kw = global_person_kw
        
        if topic == 'CHUNG' and global_topic != 'CHUNG':
            topic = global_topic
            topic_label = global_topic_label
        
        # Xác định Dụng Thần cuối cùng
        # Priority: person override > topic default
        if not dt_override:
            TOPIC_DEFAULT_DT = {
                'SỨC_KHỎE': 'Bản Thân',
                'TÀI_CHÍNH': 'Thê Tài',
                'CÔNG_VIỆC': 'Quan Quỷ',
                'TÌNH_CẢM': 'Thê Tài',
                'TÌM_ĐỒ': 'Thê Tài',
                'CHUNG': 'Bản Thân',
            }
            dt_override = TOPIC_DEFAULT_DT.get(topic, 'Bản Thân')
        
        # Cũng match diagram nếu qtype = CHUNG
        if qtype == 'CHUNG' and diagram_id == 'SD0':
            # Thử match lại bằng topic
            TOPIC_DIAGRAM_MAP = {
                'SỨC_KHỎE': ('SỨC KHỎE', 'SD8', '🏥 SỨC KHỎE'),
                'TÀI_CHÍNH': ('TÀI LỘC', 'SD6', '💰 TÀI LỘC'),
                'CÔNG_VIỆC': ('CÔNG VIỆC', 'SD9', '💼 CÔNG VIỆC'),
                'TÌNH_CẢM': ('TÌNH DUYÊN', 'SD7', '❤️ TÌNH DUYÊN'),
                'TÌM_ĐỒ': ('MẤT ĐỒ', 'SD11', '🔍 MẤT ĐỒ'),
            }
            if topic in TOPIC_DIAGRAM_MAP:
                qtype, diagram_id, qtype_label = TOPIC_DIAGRAM_MAP[topic]
        
        results.append({
            'text': sub_q,
            'person': person,
            'person_kw': person_kw,
            'dung_than': dt_override,
            'topic': topic,
            'topic_label': topic_label,
            'qtype': qtype,
            'diagram_id': diagram_id,
            'qtype_label': qtype_label,
            'index': i + 1,
        })
    
    return results


def format_parsed_questions(parsed_list):
    """V31.1: Format kết quả phân tách thành bảng markdown hiển thị.
    """
    if not parsed_list:
        return ""
    
    lines = []
    lines.append(f"### 📋 PHÂN TÁCH CÂU HỎI ({len(parsed_list)} câu)")
    lines.append(f"| # | Câu hỏi | Hỏi cho | DT | Chủ đề | Loại | Sơ đồ |")
    lines.append(f"|:--|:--------|:--------|:---|:-------|:-----|:------|")
    
    for pq in parsed_list:
        short_q = pq['text'][:35] + '...' if len(pq['text']) > 35 else pq['text']
        person = pq.get('person', 'Bản thân') or 'Bản thân'
        lines.append(
            f"| {pq['index']} | {short_q} | {person} | {pq['dung_than']} | "
            f"{pq['topic_label']} | {pq['qtype_label']} | {pq['diagram_id']} |"
        )
    
    return "\n".join(lines)

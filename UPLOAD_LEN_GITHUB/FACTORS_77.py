"""
FACTORS_77.py — BỘ 77 YẾU TỐ TÁC ĐỘNG TOÀN DIỆN
═══════════════════════════════════════════════════
AI (Online + Offline) ĐỌC FILE NÀY để biết:
- Có bao nhiêu yếu tố tác động vào kết quả
- Mỗi yếu tố tính điểm thế nào
- Yếu tố nào quan trọng nhất
- Cách tổng hợp 77 yếu tố → 1 kết luận

Phiên bản: V32.4 — 2026-04-15
"""

# ═══════════════════════════════════════════════════════════════
# PHƯƠNG PHÁP 1: KỲ MÔN ĐỘN GIÁP (41 yếu tố)
# Trọng số: 20-30% tổng điểm tùy loại câu hỏi
# ═══════════════════════════════════════════════════════════════

KY_MON_FACTORS = {
    # --- Nhóm A: Thiên Bàn (Trời) — 9 yếu tố ---
    1:  {'id': 'KM_SAO',        'ten': 'Cửu Tinh (9 Sao)',          'nhom': 'Thiên Bàn',
         'mo_ta': '9 sao trên Thiên Bàn: Tâm/Nhậm/Phụ/Xung=CÁT, Bồng/Nhuế/Cầm/Trụ/Anh=HUNG/BÌNH',
         'diem': '+1 nếu sao CÁT tại cung BT, -1 nếu HUNG',
         'nguon': 'chart_data → thien_ban'},
    
    2:  {'id': 'KM_SAO_KB',     'ten': 'KB Sao Chi Tiết',           'nhom': 'Thiên Bàn',
         'mo_ta': 'Hành, loại, ý nghĩa chi tiết từ Knowledge Base',
         'diem': 'Bổ sung thông tin, không tính điểm trực tiếp',
         'nguon': 'SAO_KY_MON dict'},

    3:  {'id': 'KM_SAO_HANH',   'ten': 'Hành của Sao',              'nhom': 'Thiên Bàn',
         'mo_ta': 'Ngũ Hành sao tương tác với Cung → Tam Tài',
         'diem': 'Tham gia tính Tam Tài (YT #36)',
         'nguon': 'SAO_GIAI_THICH → hanh'},

    # --- Nhóm B: Nhân Bàn (Người) — 5 yếu tố ---
    4:  {'id': 'KM_CUA',        'ten': 'Bát Môn (8 Cửa)',           'nhom': 'Nhân Bàn',
         'mo_ta': 'Khai/Hưu/Sinh=CÁT, Tử/Kinh/Thương=HUNG, Đỗ/Cảnh=BÌNH',
         'diem': '+1 nếu cửa CÁT, -1 nếu HUNG',
         'nguon': 'chart_data → nhan_ban'},

    5:  {'id': 'KM_CUA_KB',     'ten': 'KB Cửa Chi Tiết',           'nhom': 'Nhân Bàn',
         'mo_ta': 'Hành, loại, ý nghĩa chi tiết từ Knowledge Base',
         'diem': 'Bổ sung thông tin',
         'nguon': 'CUA_KY_MON dict'},

    6:  {'id': 'KM_CUA_BAY',    'ten': 'Bát Môn Bay Cung',          'nhom': 'Nhân Bàn',
         'mo_ta': 'Phục Ngâm(-1)/Phản Ngâm(-2)/Nhập Mộ(-1)/Bức/Chế',
         'diem': '-1 đến -2 nếu Phục/Phản Ngâm, Nhập Mộ',
         'nguon': 'BAT_MON_BAY_CUNG dict'},

    7:  {'id': 'KM_CUA_HANH',   'ten': 'Hành của Cửa',              'nhom': 'Nhân Bàn',
         'mo_ta': 'Ngũ Hành cửa tương tác với Cung → Tam Tài',
         'diem': 'Tham gia tính Tam Tài (YT #36)',
         'nguon': 'Cửa → Hành mapping'},

    8:  {'id': 'KM_SAO_CUA',    'ten': 'Tổ Hợp Sao + Cửa',         'nhom': 'Nhân Bàn',
         'mo_ta': 'Kết hợp Sao×Cửa → tra bảng CÁT/HUNG',
         'diem': '+1 nếu combo CÁT, -1 nếu combo HUNG',
         'nguon': 'SAO_CUA_TO_HOP dict'},

    # --- Nhóm C: Thần Bàn — 3 yếu tố ---
    9:  {'id': 'KM_THAN',       'ten': 'Bát Thần (8 Thần)',          'nhom': 'Thần Bàn',
         'mo_ta': '8 Thần trên Thần Bàn',
         'diem': 'Bổ sung ý nghĩa tâm linh',
         'nguon': 'chart_data → than_ban'},

    10: {'id': 'KM_THAN_KB',    'ten': 'KB Thần Chi Tiết',           'nhom': 'Thần Bàn',
         'mo_ta': 'Hành, loại, ý nghĩa chi tiết từ Knowledge Base',
         'diem': 'Bổ sung thông tin',
         'nguon': 'THAN_KY_MON dict'},

    11: {'id': 'KM_12THAN',     'ten': '12 Thần Ứng Nghiệm',        'nhom': 'Thần Bàn',
         'mo_ta': 'Tra ứng nghiệm theo Sách Bí Cấp Toàn Thư',
         'diem': 'Mô tả chi tiết, không tính điểm',
         'nguon': 'THAP_NHI_THAN_UNG_NGHIEM dict'},

    # --- Nhóm D: Địa Bàn + Can — 8 yếu tố ---
    12: {'id': 'KM_CAN_NGAY',   'ten': 'Can Ngày (Bản Thân)',        'nhom': 'Can Chi',
         'mo_ta': 'Can Ngày = đại diện Bản Thân trong Kỳ Môn',
         'diem': 'Xác định cung BT → tính sinh khắc',
         'nguon': 'chart_data → can_ngay'},

    13: {'id': 'KM_CAN_GIO',    'ten': 'Can Giờ (Sự Việc)',          'nhom': 'Can Chi',
         'mo_ta': 'Can Giờ = đại diện Sự Việc hỏi',
         'diem': 'Xác định cung SV → so sánh BT↔SV',
         'nguon': 'chart_data → can_gio'},

    14: {'id': 'KM_NGU_HANH',   'ten': 'Ngũ Hành Can×Cung',          'nhom': 'Can Chi',
         'mo_ta': 'Hành Can Ngày vs Hành Cung → SINH/KHẮC/TỶ',
         'diem': '+2 nếu Được Sinh/Tỷ, -2 nếu Bị Khắc, -1 nếu Hao',
         'nguon': '_ngu_hanh_relation()'},

    15: {'id': 'KM_BT_SV',      'ten': 'BT vs SV (Bản Thân vs Sự Việc)', 'nhom': 'Can Chi',
         'mo_ta': 'Cung BT sinh/khắc Cung SV → ai mạnh hơn',
         'diem': 'SINH=phải bỏ công, ĐƯỢC SINH=lợi, KHẮC=kiểm soát/bị hại',
         'nguon': 'chu_cung vs sv_cung'},

    16: {'id': 'KM_CACH_CUC',   'ten': 'Cách Cục (TRUCTU_TRANH)',     'nhom': 'Can Chi',
         'mo_ta': 'Can Thiên×Can Địa → tra 81 tổ hợp → Cách Cục tên + CÁT/HUNG',
         'diem': 'Bổ sung ý nghĩa đặc biệt',
         'nguon': 'KY_MON_DATA → TRUCTU_TRANH'},

    17: {'id': 'KM_KHAC_UNG',   'ten': 'Thập Can Khắc Ứng (81 tổ hợp)', 'nhom': 'Can Chi',
         'mo_ta': 'Sách Lưu Bá Ôn — 81 tổ hợp Thiên×Địa bàn',
         'diem': '+2 ĐẠI CÁT, +1 CÁT, -1 HUNG, -2 ĐẠI HUNG',
         'nguon': 'THAP_CAN_KHAC_UNG dict'},

    18: {'id': 'KM_TUONG_Y',    'ten': 'Can Chi Tượng Ý (Y học + Hôn nhân)', 'nhom': 'Can Chi',
         'mo_ta': 'Sách Đế Vương Chi Thuật — nội tạng, cơ thể, hôn nhân',
         'diem': 'Mô tả context-aware (chỉ hiện khi hỏi bệnh/tình cảm)',
         'nguon': 'CAN_CHI_TUONG_Y dict'},

    19: {'id': 'KM_QUAI',       'ten': 'Bát Quái Tượng',              'nhom': 'Can Chi',
         'mo_ta': 'Quái tại cung BT → Vạn Vật Loại Tượng cơ bản',
         'diem': 'Mô tả chi tiết (người, hướng, vật)',
         'nguon': 'QUAI_TUONG → get_bat_quai_tuong()'},

    # --- Nhóm E: Đặc Biệt — 8 yếu tố ---
    20: {'id': 'KM_PHAN_NGAM',  'ten': 'Phản Ngâm',                   'nhom': 'Đặc Biệt',
         'mo_ta': 'Can Thiên xung Can Địa → ĐẢO NGƯỢC hoàn toàn',
         'diem': '-3 (rất nặng)',
         'nguon': '_check_phan_phuc_ngam()'},

    21: {'id': 'KM_PHUC_NGAM',  'ten': 'Phục Ngâm',                   'nhom': 'Đặc Biệt',
         'mo_ta': 'Can Thiên = Can Địa → BẾ TẮC, trì trệ',
         'diem': '-2',
         'nguon': '_check_phan_phuc_ngam()'},

    22: {'id': 'KM_TUAN_KHONG', 'ten': 'Tuần Không Tứ Trụ',           'nhom': 'Đặc Biệt',
         'mo_ta': 'Chi lâm Tuần Không = KHÔNG CÓ THẬT, hư ảo',
         'diem': '-3 nếu Chi Giờ lâm TK, -1 nếu Chi Ngày lâm TK',
         'nguon': '_get_khong_vong()'},

    23: {'id': 'KM_DICH_MA',    'ten': 'Dịch Mã Tứ Trụ',              'nhom': 'Đặc Biệt',
         'mo_ta': 'Dịch Mã = DI CHUYỂN, biến động nhanh',
         'diem': 'CÁT+Mã=đi xa tốt, HUNG+Mã=chạy trốn',
         'nguon': 'DICH_MA_MAP dict'},

    24: {'id': 'KM_TAM_KY',     'ten': 'Tam Kỳ Đắc Sử',              'nhom': 'Đặc Biệt',
         'mo_ta': 'Ất/Bính/Đinh gặp Cửa Cát → CỰC CÁT',
         'diem': '+2',
         'nguon': 'Can Thiên in [Ất, Bính, Đinh] + Cửa Cát'},

    25: {'id': 'KM_TAM_TAI',    'ten': 'Thiên Địa Nhân Tam Tài',      'nhom': 'Đặc Biệt',
         'mo_ta': 'Sao + Cửa + Cung đều tương hợp → ĐẠI CÁT',
         'diem': '+1 nếu tương hợp',
         'nguon': 'Sao_hanh + Cửa_hanh + Cung_hanh'},

    26: {'id': 'KM_VAN_VAT_CTX','ten': 'Vạn Vật Context-Aware',       'nhom': 'Đặc Biệt',
         'mo_ta': 'Vạn Vật Loại Tượng phù hợp theo nội dung câu hỏi',
         'diem': 'Mô tả chi tiết',
         'nguon': '_get_van_vat_context()'},

    27: {'id': 'KM_CACH_CUC_KB','ten': 'KB Cách Cục (Knowledge Base)', 'nhom': 'Đặc Biệt',
         'mo_ta': 'Tra Cách Cục nâng cao từ KB mở rộng',
         'diem': 'Bổ sung ý nghĩa',
         'nguon': 'KY_MON_CACH_CUC + KY_MON_CACH_CUC_MR'},

    # --- Nhóm F: Tứ Trụ — 8 yếu tố ---
    28: {'id': 'KM_TRU_NAM',    'ten': 'Trụ Năm (Gốc Rễ)',           'nhom': 'Tứ Trụ',
         'mo_ta': 'Can×Chi Năm → ông bà, xã hội, nguồn gốc',
         'diem': 'Bối cảnh nền tảng',
         'nguon': 'chart_data → can_nam, chi_nam'},

    29: {'id': 'KM_TRU_THANG',  'ten': 'Trụ Tháng (Cửa Chính)',      'nhom': 'Tứ Trụ',
         'mo_ta': 'Can×Chi Tháng → cha mẹ, sự nghiệp, lệnh tháng',
         'diem': 'Nguyệt Lệnh chi phối sức mạnh',
         'nguon': 'chart_data → can_thang, chi_thang'},

    30: {'id': 'KM_TRU_NGAY',   'ten': 'Trụ Ngày (Bản Thân)',        'nhom': 'Tứ Trụ',
         'mo_ta': 'Can×Chi Ngày → chính mình, tâm tính, nội lực',
         'diem': 'Trung tâm — xác định Dụng Thần',
         'nguon': 'chart_data → can_ngay, chi_ngay'},

    31: {'id': 'KM_TRU_GIO',    'ten': 'Trụ Giờ (Tương Lai)',        'nhom': 'Tứ Trụ',
         'mo_ta': 'Can×Chi Giờ → con cái, kết quả, hậu vận',
         'diem': '+1 nếu Giờ sinh Ngày (lợi), -1 nếu Giờ khắc Ngày',
         'nguon': 'chart_data → can_gio, chi_gio'},

    32: {'id': 'KM_SK_4TRU',    'ten': 'Sinh Khắc 4 Trụ',            'nhom': 'Tứ Trụ',
         'mo_ta': 'Ngày↔Giờ sinh khắc → ai giúp ai, ai hại ai',
         'diem': '±1 tùy quan hệ',
         'nguon': '_ngu_hanh_relation(Ngày, Giờ)'},

    # --- Nhóm G: Đếm/Tuổi/Tìm — 5 yếu tố riêng ---
    33: {'id': 'KM_DEM_SO',     'ten': 'Đếm Số Lượng',               'nhom': 'Đặc Thù',
         'mo_ta': 'Can Tháng → Quái Tiên Thiên → số lượng anh chị em',
         'diem': 'Số cụ thể',
         'nguon': 'TIEN_THIEN mapping'},

    34: {'id': 'KM_TUOI',       'ten': 'Tính Tuổi',                  'nhom': 'Đặc Thù',
         'mo_ta': 'Quái Tiên Thiên × hệ số Vượng/Suy → tuổi',
         'diem': 'Số cụ thể',
         'nguon': 'TIEN_THIEN × (5 nếu Vượng, 3 nếu Suy)'},

    35: {'id': 'KM_TIM_DO',     'ten': 'Tìm Đồ (Hướng + Nơi)',      'nhom': 'Đặc Thù',
         'mo_ta': 'Cung SV → Hướng (Bắc/Nam/...) + Nơi (gần nước/bếp/...)',
         'diem': 'Hướng + mô tả vị trí',
         'nguon': 'huong_map + noi_map'},

    # --- Nhóm H: Tổng quan 9 Cung ---
    36: {'id': 'KM_9CUNG',      'ten': 'Tổng Quan 9 Cung',           'nhom': 'Tổng Quan',
         'mo_ta': 'Hiển thị Sao/Cửa/Thần/Can tại mỗi cung → toàn cảnh',
         'diem': 'Bối cảnh tổng thể',
         'nguon': 'thien_ban + nhan_ban + than_ban + can_thien_ban'},

    # --- Nhóm I: Can Tháng ---
    37: {'id': 'KM_CAN_THANG',  'ten': 'Can Tháng (Anh Chị Em)',     'nhom': 'Can Chi',
         'mo_ta': 'Can Tháng = đại diện anh chị em, bạn bè',
         'diem': 'Xác định cung để đếm số lượng',
         'nguon': 'chart_data → can_thang'},

    # --- Nhóm J: Dia Ban ---
    38: {'id': 'KM_DIA_BAN',    'ten': 'Địa Bàn (Can Địa)',          'nhom': 'Địa Bàn',
         'mo_ta': 'Can trên Địa Bàn → tính Cách Cục, Phản/Phục Ngâm',
         'diem': 'Tham gia tính Cách Cục + Phản/Phục Ngâm',
         'nguon': 'chart_data → dia_ban / dia_can'},

    # --- Nhóm K: Sách kinh điển ---
    39: {'id': 'KM_CUNG_BT',    'ten': 'Cung Bản Thân',              'nhom': 'Cung',
         'mo_ta': 'Cung chứa Can Ngày = vị trí Bản Thân trên 9 cung',
         'diem': 'Trung tâm phân tích → score bắt đầu từ đây',
         'nguon': 'can_thien_ban → tìm can_ngay'},

    40: {'id': 'KM_CUNG_SV',    'ten': 'Cung Sự Việc',               'nhom': 'Cung',
         'mo_ta': 'Cung chứa Can Giờ = vị trí Sự Việc trên 9 cung',
         'diem': 'So sánh BT↔SV',
         'nguon': 'can_thien_ban → tìm can_gio'},

    41: {'id': 'KM_HANH_CUNG',  'ten': 'Ngũ Hành Cung BT',           'nhom': 'Cung',
         'mo_ta': 'Hành của cung Bản Thân → tính sinh khắc với Can',
         'diem': 'Nền tảng tính điểm +2/-2',
         'nguon': 'CUNG_NGU_HANH mapping'},
}


# ═══════════════════════════════════════════════════════════════
# PHƯƠNG PHÁP 2: LỤC HÀO KINH DỊCH (16 yếu tố)
# Trọng số: 25-35% tổng điểm (PP mạnh nhất)
# ═══════════════════════════════════════════════════════════════

LUC_HAO_FACTORS = {
    42: {'id': 'LH_6HAO',       'ten': '6 Hào (Dương/Âm/Động/Tĩnh)', 'nhom': 'Quẻ',
         'mo_ta': '6 hào từ dưới lên: Sơ→Nhị→Tam→Tứ→Ngũ→Thượng',
         'diem': 'Nền tảng — xác định Lục Thân, Dụng Thần',
         'nguon': 'luc_hao_data → haos[]'},

    43: {'id': 'LH_LUC_THAN',   'ten': 'Lục Thần (6 thần)',          'nhom': 'Quẻ',
         'mo_ta': 'Thanh Long/Chu Tước/Câu Trần/Đằng Xà/Bạch Hổ/Huyền Vũ',
         'diem': 'Bổ sung tính chất cho mỗi hào',
         'nguon': 'luc_hao_data → luc_than[]'},

    44: {'id': 'LH_DUNG_THAN',  'ten': 'Dụng Thần',                  'nhom': 'Lực Lượng',
         'mo_ta': 'Hào đại diện cho sự việc hỏi — quan trọng nhất',
         'diem': 'Vượng=CÁT, Suy=HUNG, Động=biến đổi',
         'nguon': 'Xác định từ loại câu hỏi'},

    45: {'id': 'LH_NGUYEN_THAN','ten': 'Nguyên Thần',                'nhom': 'Lực Lượng',
         'mo_ta': 'Hào SINH Dụng Thần = Quý Nhân giúp đỡ',
         'diem': '+6 nếu Vượng + Động, Sinh DT',
         'nguon': 'Sinh khắc luận'},

    46: {'id': 'LH_KY_THAN',    'ten': 'Kỵ Thần',                    'nhom': 'Lực Lượng',
         'mo_ta': 'Hào KHẮC Dụng Thần = Kẻ thù hại',
         'diem': '-8 nếu Vượng + Động, Khắc DT',
         'nguon': 'Sinh khắc luận'},

    47: {'id': 'LH_CUU_THAN',   'ten': 'Cừu Thần',                   'nhom': 'Lực Lượng',
         'mo_ta': 'Hào KHẮC Kỵ Thần = giải cứu (khắc kẻ thù)',
         'diem': '+4 nếu Vượng + Động',
         'nguon': 'Sinh khắc luận'},

    48: {'id': 'LH_THE',        'ten': 'Thế Hào (Mình)',             'nhom': 'Thế Ứng',
         'mo_ta': 'Hào đại diện cho mình/người hỏi',
         'diem': 'So sánh Thế↔Ứng → ai mạnh hơn',
         'nguon': 'luc_hao_data → the_hao'},

    49: {'id': 'LH_UNG',        'ten': 'Ứng Hào (Đối Phương)',       'nhom': 'Thế Ứng',
         'mo_ta': 'Hào đại diện cho đối phương/sự việc',
         'diem': 'Thế>Ứng=mình thắng, Ứng>Thế=đối phương thắng',
         'nguon': 'luc_hao_data → ung_hao'},

    50: {'id': 'LH_NGUYET',     'ten': 'Nguyệt Lệnh (Tháng)',       'nhom': 'Thời Gian',
         'mo_ta': 'Chi Tháng sinh/khắc DT → ảnh hưởng LỚN NHẤT',
         'diem': '±8 (sinh DT=+8, khắc DT=-8)',
         'nguon': 'luc_hao_data → nguyet_lenh'},

    51: {'id': 'LH_NHAT',       'ten': 'Nhật Thần (Ngày)',           'nhom': 'Thời Gian',
         'mo_ta': 'Chi Ngày sinh/khắc DT → ảnh hưởng lớn thứ 2',
         'diem': '±6 (sinh DT=+6, khắc DT=-6)',
         'nguon': 'luc_hao_data → nhat_than'},

    52: {'id': 'LH_NT_SK',      'ten': 'NT sinh/khắc DT',            'nhom': 'Lực Lượng',
         'mo_ta': 'Nguyên Thần đang sinh hay khắc Dụng Thần',
         'diem': 'Tham gia tính LH Raw Score',
         'nguon': 'Sinh khắc luận NT→DT'},

    53: {'id': 'LH_KT_SK',      'ten': 'KT sinh/khắc DT',            'nhom': 'Lực Lượng',
         'mo_ta': 'Kỵ Thần đang khắc Dụng Thần',
         'diem': 'Tham gia tính LH Raw Score',
         'nguon': 'Sinh khắc luận KT→DT'},

    54: {'id': 'LH_RAW',        'ten': 'Lục Hào Raw Score',           'nhom': 'Tổng Hợp',
         'mo_ta': 'Điểm tổng = Nguyệt ± Nhật ± NT ± KT ± Đặc biệt',
         'diem': 'Raw → normalize → 0-100% → Unified',
         'nguon': 'Tính từ các yếu tố trên'},

    55: {'id': 'LH_TRUONG_SINH','ten': '12 Trường Sinh',              'nhom': 'Suy Vượng',
         'mo_ta': 'Hành DT tại Chi tham chiếu → 12 giai đoạn',
         'diem': 'Power 0-100% (Đế Vượng=100%, Tuyệt=10%)',
         'nguon': 'TRUONG_SINH_TABLE'},

    56: {'id': 'LH_HAO_DONG',   'ten': 'Hào Động',                    'nhom': 'Biến Đổi',
         'mo_ta': 'Hào có biến (Động) → sự việc ĐANG BIẾN ĐỔI',
         'diem': 'Động=thay đổi, Tĩnh=ổn định',
         'nguon': 'luc_hao_data → dong[]'},

    57: {'id': 'LH_HOA_HAO',    'ten': 'Hóa Hào (Biến Hào)',         'nhom': 'Biến Đổi',
         'mo_ta': 'Hào Động biến thành gì → xu hướng tương lai',
         'diem': 'Hóa Sinh=tốt, Hóa Khắc=xấu, Hóa Tuyệt=cực xấu',
         'nguon': 'luc_hao_data → bien_hao[]'},
}


# ═══════════════════════════════════════════════════════════════
# PHƯƠNG PHÁP 3: MAI HOA DỊCH SỐ (7 yếu tố)
# Trọng số: 15-20%
# ═══════════════════════════════════════════════════════════════

MAI_HOA_FACTORS = {
    58: {'id': 'MH_THUONG',     'ten': 'Thượng Quái',                'nhom': 'Quẻ',
         'mo_ta': 'Quái trên (Ngoại Quái) = bên ngoài, môi trường',
         'diem': 'Xác định bối cảnh bên ngoài',
         'nguon': 'mai_hoa_data → thuong_quai'},

    59: {'id': 'MH_HA',         'ten': 'Hạ Quái',                    'nhom': 'Quẻ',
         'mo_ta': 'Quái dưới (Nội Quái) = bên trong, bản thân',
         'diem': 'Xác định tình trạng bên trong',
         'nguon': 'mai_hoa_data → ha_quai'},

    60: {'id': 'MH_BIEN',       'ten': 'Biến Quái',                  'nhom': 'Quẻ',
         'mo_ta': 'Quẻ sau khi hào động biến → xu hướng tương lai',
         'diem': 'Sinh Thể=tốt, khắc Thể=xấu',
         'nguon': 'mai_hoa_data → bien_quai'},

    61: {'id': 'MH_HO',         'ten': 'Hỗ Quái (Ẩn)',              'nhom': 'Quẻ',
         'mo_ta': 'Quái ẩn bên trong = yếu tố ngầm, tiềm ẩn',
         'diem': 'Phát hiện yếu tố chưa lộ diện',
         'nguon': 'mai_hoa_data → ho_quai'},

    62: {'id': 'MH_NGU_HANH',   'ten': 'Ngũ Hành Quái',              'nhom': 'Luận',
         'mo_ta': 'Thể Quái vs Dụng Quái → sinh khắc → kết luận',
         'diem': 'Thể sinh Dụng=hao, Dụng sinh Thể=lợi',
         'nguon': 'Bát Quái → Ngũ Hành mapping'},

    63: {'id': 'MH_HAO_DONG',   'ten': 'Hào Động Mai Hoa',           'nhom': 'Luận',
         'mo_ta': 'Hào nào động → yếu tố nào đang thay đổi',
         'diem': 'Xác định nguồn biến',
         'nguon': 'mai_hoa_data → hao_dong'},

    64: {'id': 'MH_GIAI_QUE',   'ten': 'Giải Quẻ (Interpretation)',  'nhom': 'Luận',
         'mo_ta': 'Giải thích tổng hợp từ 64 quẻ Kinh Dịch',
         'diem': 'Lời giải đầy đủ theo chủ đề',
         'nguon': 'giai_qua(mai_hoa_data, topic)'},
}


# ═══════════════════════════════════════════════════════════════
# PHƯƠNG PHÁP 4: THIẾT BẢN THẦN TOÁN (2 yếu tố)
# Trọng số: 10-15%
# ═══════════════════════════════════════════════════════════════

THIET_BAN_FACTORS = {
    65: {'id': 'TB_NAP_AM',     'ten': 'Nạp Âm Can Ngày',            'nhom': 'Thiết Bản',
         'mo_ta': 'Can×Chi Ngày → Nạp Âm (60 Giáp Tý) → đoán mệnh',
         'diem': 'Bổ sung yếu tố Mệnh vào phân tích',
         'nguon': 'Bảng Nạp Âm 60 Giáp Tý'},

    66: {'id': 'TB_VAN_VAT',    'ten': 'Vạn Vật Loại Tượng Tổng Hợp', 'nhom': 'Thiết Bản',
         'mo_ta': 'Tổng hợp Vạn Vật từ 5 phương pháp → chi tiết 2226+ items',
         'diem': 'Mô tả cụ thể: đồ vật, nhà, người, bệnh, hướng',
         'nguon': 'van_vat/ package (lazy-load)'},
}


# ═══════════════════════════════════════════════════════════════
# PHƯƠNG PHÁP 5: ĐẠI LỤC NHÂM (6 yếu tố)
# Trọng số: 10-15%
# ═══════════════════════════════════════════════════════════════

DAI_LUC_NHAM_FACTORS = {
    67: {'id': 'LN_TAM_TRUYEN', 'ten': 'Tam Truyền (Sơ/Trung/Mạt)',  'nhom': 'Lục Nhâm',
         'mo_ta': 'Sơ=quá khứ, Trung=hiện tại, Mạt=tương lai → timeline',
         'diem': 'Mạt Truyền quyết định KẾT QUẢ cuối cùng',
         'nguon': 'tinh_dai_luc_nham() → tam_truyen'},

    68: {'id': 'LN_TU_KHOA',    'ten': 'Tứ Khóa',                    'nhom': 'Lục Nhâm',
         'mo_ta': '4 cặp Can Dương/Can Âm × Chi Dương/Chi Âm',
         'diem': 'Cấu trúc nền tảng của Lục Nhâm',
         'nguon': 'tinh_dai_luc_nham() → tu_khoa'},

    69: {'id': 'LN_NGUYET_TUONG','ten': 'Nguyệt Tướng',              'nhom': 'Lục Nhâm',
         'mo_ta': 'Thiên Tướng theo Nguyệt Kiến → bối cảnh thời gian',
         'diem': 'Xác định bối cảnh vũ trụ',
         'nguon': 'tinh_dai_luc_nham() → nguyet_tuong'},

    70: {'id': 'LN_TUAN_KHONG', 'ten': 'Tuần Không Lục Nhâm',        'nhom': 'Lục Nhâm',
         'mo_ta': 'Chi lâm Tuần Không = sự việc hư ảo, không thật',
         'diem': 'DT hiện trong TK → khó thành',
         'nguon': 'phan_tich_chuyen_sau() → tuan_khong'},

    71: {'id': 'LN_DT_HIEN',    'ten': 'DT Hiện Trong Tứ Khóa',      'nhom': 'Lục Nhâm',
         'mo_ta': 'Dụng Thần CÓ hiện trong Tứ Khóa → sự việc CÓ thật',
         'diem': 'Có=sự việc khả thi, Không=khó thành',
         'nguon': 'phan_tich_chuyen_sau() → dung_than_found'},

    72: {'id': 'LN_VERDICT',    'ten': 'Lục Nhâm Verdict',            'nhom': 'Lục Nhâm',
         'mo_ta': 'Kết luận cuối: ĐẠI CÁT / CÁT / BÌNH / HUNG / ĐẠI HUNG',
         'diem': 'Đóng góp vào weighted score',
         'nguon': 'phan_tich_chuyen_sau() → verdict'},
}


# ═══════════════════════════════════════════════════════════════
# PHƯƠNG PHÁP 6: THÁI ẤT THẦN SỐ (5 yếu tố)
# Trọng số: 10%
# ═══════════════════════════════════════════════════════════════

THAI_AT_FACTORS = {
    73: {'id': 'TA_CUNG',       'ten': 'Thái Ất Cung',               'nhom': 'Thái Ất',
         'mo_ta': 'Cung số + Tên Cung + Hành Cung + Lý giải',
         'diem': 'Bối cảnh vũ trụ năm/tháng',
         'nguon': 'tinh_thai_at_than_so() → thai_at_cung'},

    74: {'id': 'TA_TICH_NIEN',  'ten': 'Tích Niên',                  'nhom': 'Thái Ất',
         'mo_ta': 'Số năm tích lũy → chu kỳ vận mệnh',
         'diem': 'Xác định giai đoạn vận mệnh',
         'nguon': 'tinh_thai_at_than_so() → tich_nien'},

    75: {'id': 'TA_BAT_TUONG',  'ten': 'Bát Tướng (4 tướng chính)',  'nhom': 'Thái Ất',
         'mo_ta': '8 Tướng xác định tại Cung → CÁT/HUNG từng tướng',
         'diem': 'Bổ sung chi tiết CÁT/HUNG',
         'nguon': 'tinh_thai_at_than_so() → bat_tuong'},

    76: {'id': 'TA_CACH_CUC',   'ten': 'Thái Ất Cách Cục',           'nhom': 'Thái Ất',
         'mo_ta': 'Cách Cục đặc biệt của Thái Ất',
         'diem': 'Bổ sung ý nghĩa đặc biệt',
         'nguon': 'tinh_thai_at_than_so() → cach_cuc'},

    77: {'id': 'TA_VERDICT',    'ten': 'Thái Ất Verdict',             'nhom': 'Thái Ất',
         'mo_ta': 'Kết luận cuối: ĐẠI CÁT / CÁT / BÌNH / HUNG / ĐẠI HUNG',
         'diem': 'Đóng góp vào weighted score',
         'nguon': 'luan_giai → verdict'},
}


# ═══════════════════════════════════════════════════════════════
# TỔNG HỢP 77 YẾU TỐ
# ═══════════════════════════════════════════════════════════════

ALL_77_FACTORS = {}
ALL_77_FACTORS.update(KY_MON_FACTORS)
ALL_77_FACTORS.update(LUC_HAO_FACTORS)
ALL_77_FACTORS.update(MAI_HOA_FACTORS)
ALL_77_FACTORS.update(THIET_BAN_FACTORS)
ALL_77_FACTORS.update(DAI_LUC_NHAM_FACTORS)
ALL_77_FACTORS.update(THAI_AT_FACTORS)


# ═══════════════════════════════════════════════════════════════
# TRỌNG SỐ THEO LOẠI CÂU HỎI
# ═══════════════════════════════════════════════════════════════

WEIGHT_MAP = {
    'SỨC_KHỎE_GIA_ĐÌNH': {'KM': 15, 'LH': 35, 'MH': 15, 'TB': 15, 'LN': 10, 'TA': 10},
    'TÀI_CHÍNH':          {'KM': 20, 'LH': 30, 'MH': 15, 'TB': 15, 'LN': 10, 'TA': 10},
    'CÔNG_VIỆC':           {'KM': 25, 'LH': 25, 'MH': 15, 'TB': 10, 'LN': 15, 'TA': 10},
    'TÌNH_CẢM':            {'KM': 15, 'LH': 30, 'MH': 20, 'TB': 10, 'LN': 10, 'TA': 15},
    'TÌM_ĐỒ':             {'KM': 35, 'LH': 15, 'MH': 20, 'TB': 10, 'LN': 10, 'TA': 10},
    'DEFAULT':             {'KM': 20, 'LH': 25, 'MH': 15, 'TB': 15, 'LN': 15, 'TA': 10},
}


# ═══════════════════════════════════════════════════════════════
# CÔNG THỨC TỔNG HỢP → 1 KẾT LUẬN
# ═══════════════════════════════════════════════════════════════

SCORING_FORMULA = """
BƯỚC 1: Mỗi PP tính Raw Score từ các yếu tố riêng
BƯỚC 2: Normalize Raw → 0-100% (map [-40,+40] → [0,100])
BƯỚC 3: Weighted Average = Σ(PP_norm × Weight_PP)
BƯỚC 4: Unified% = LH×50% + TrườngSinh×30% + NgũKhí×20%
BƯỚC 5: Verdict:
  - ≥4 CÁT/5 PP → ĐẠI CÁT
  - ≥3 CÁT      → CÁT
  - 2-3 BÌNH     → LỠ CỠ
  - ≥3 HUNG      → HUNG
  - ≥4 HUNG      → ĐẠI HUNG
  
  Unified ≥70% = VƯỢNG | 50-69% = TRUNG BÌNH | <50% = SUY
"""


# ═══════════════════════════════════════════════════════════════
# HELPER: Tra cứu nhanh
# ═══════════════════════════════════════════════════════════════

def get_factor(factor_id):
    """Tra cứu yếu tố theo ID (1-77)"""
    return ALL_77_FACTORS.get(factor_id)

def get_factors_by_method(method):
    """Lấy tất cả yếu tố của 1 phương pháp"""
    method_map = {
        'KM': KY_MON_FACTORS,
        'LH': LUC_HAO_FACTORS,
        'MH': MAI_HOA_FACTORS,
        'TB': THIET_BAN_FACTORS,
        'LN': DAI_LUC_NHAM_FACTORS,
        'TA': THAI_AT_FACTORS,
    }
    return method_map.get(method, {})

def get_factor_summary():
    """Tóm tắt số lượng yếu tố"""
    return {
        'Kỳ Môn Độn Giáp': len(KY_MON_FACTORS),
        'Lục Hào Kinh Dịch': len(LUC_HAO_FACTORS),
        'Mai Hoa Dịch Số': len(MAI_HOA_FACTORS),
        'Thiết Bản Thần Toán': len(THIET_BAN_FACTORS),
        'Đại Lục Nhâm': len(DAI_LUC_NHAM_FACTORS),
        'Thái Ất Thần Số': len(THAI_AT_FACTORS),
        'TỔNG': len(ALL_77_FACTORS),
    }

def format_all_factors_for_ai():
    """Format 77 yếu tố thành text cho AI đọc nhanh"""
    lines = ["# 77 YẾU TỐ TÁC ĐỘNG — 6 PHƯƠNG PHÁP", ""]
    for fid in sorted(ALL_77_FACTORS.keys()):
        f = ALL_77_FACTORS[fid]
        lines.append(f"[{fid:02d}] {f['ten']} ({f['nhom']}) — {f['mo_ta'][:80]}")
        lines.append(f"     Điểm: {f['diem']}")
    return "\n".join(lines)

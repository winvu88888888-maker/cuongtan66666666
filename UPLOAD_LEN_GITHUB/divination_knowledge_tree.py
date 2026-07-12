# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  DIVINATION KNOWLEDGE TREE — V42.9.4                        ║
║  Master Data cho 8 Phương Pháp Dự Đoán                      ║
║  Cấu trúc: CÂY PHÂN TẦNG → dễ đọc, tìm, sửa               ║
╚══════════════════════════════════════════════════════════════╝

Cách dùng:
    from divination_knowledge_tree import TREE
    TREE['LH']['factors']['hoi_dau']  # Lục Hào → Hồi Đầu
    TREE['KM']['bat_mon']['Khai Môn']  # Kỳ Môn → Cửa Khai
    TREE['MH']['sinh_khac']            # Mai Hoa → 4 công thức
"""

# ═══════════════════════════════════════════════════════════
# [LH] LỤC HÀO KINH DỊCH — 36 yếu tố
# ═══════════════════════════════════════════════════════════
LH_TREE = {
    'name': 'Lục Hào Kinh Dịch',
    'coverage': '36/36 = 100%',

    # --- Lục Thân (6 loại) ---
    'luc_than': {
        'Thê Tài':  {'khac': 'Huynh Đệ', 'sinh': 'Quan Quỷ', 'role': 'Tiền/Vợ/Tài sản'},
        'Quan Quỷ': {'khac': 'Tử Tôn',   'sinh': 'Phụ Mẫu', 'role': 'Chức vụ/Chồng/Bệnh'},
        'Phụ Mẫu': {'khac': 'Thê Tài',   'sinh': 'Huynh Đệ', 'role': 'Bố mẹ/Giấy tờ/Nhà'},
        'Huynh Đệ': {'khac': 'Phụ Mẫu',  'sinh': 'Tử Tôn',   'role': 'Anh em/Bạn/Đối thủ'},
        'Tử Tôn':  {'khac': 'Quan Quỷ',  'sinh': 'Thê Tài',  'role': 'Con cái/Thuốc/Phúc'},
    },

    # --- 36 Yếu tố phân tích ---
    'factors': {
        # ═══ NHÓM 1: THỜI GIAN (2) ═══
        'nguyet_kien': {
            'name': 'Nguyệt Kiến (Nguyệt Lệnh)',
            'desc': 'Chi của THÁNG → quyết định hào Vượng/Suy',
            'impact': 'Hào được Nguyệt sinh/vượng → mạnh. Nguyệt khắc → suy.',
            'priority': 'CAO',
        },
        'nhat_than': {
            'name': 'Nhật Thần',
            'desc': 'Chi của NGÀY → ảnh hưởng trực tiếp từng hào',
            'impact': 'Nhật sinh hào → tốt. Nhật khắc/xung hào → bất lợi.',
            'priority': 'CAO',
        },

        # ═══ NHÓM 2: HÀO VÀ BIẾN (5) ═══
        'dong_hao': {
            'name': 'Động Hào',
            'desc': 'Hào có vạch thay đổi (dương↔âm) → TÁC ĐỘNG vào sự việc',
            'impact': 'Chỉ hào Động mới phát huy tác dụng sinh/khắc. Tĩnh = chờ.',
            'priority': 'CAO',
        },
        'tinh_hao': {
            'name': 'Tĩnh Hào',
            'desc': 'Hào không động → chờ đợi, chưa phát sinh',
            'impact': 'Chỉ bị Nhật/Nguyệt tác động, không tự tác động hào khác.',
            'priority': 'TRUNG',
        },
        'hoa_hao': {
            'name': 'Hóa Hào (Biến Hào)',
            'desc': 'Hào xuất hiện sau khi Động Hào biến đổi',
            'impact': 'Hóa sinh → tốt. Hóa khắc (Hồi Đầu Khắc) → xấu.',
            'priority': 'CAO',
        },
        'the_hao': {
            'name': 'Thế Hào',
            'desc': 'Đại diện NGƯỜI XEM (bản thân)',
            'impact': 'Thế vượng → người hỏi mạnh. Thế suy → yếu thế.',
            'priority': 'CAO',
        },
        'ung_hao': {
            'name': 'Ứng Hào',
            'desc': 'Đại diện NGƯỜI/VIỆC ĐƯỢC HỎI',
            'impact': 'Thế khắc Ứng → ta thắng. Ứng khắc Thế → ta thua.',
            'priority': 'CAO',
        },

        # ═══ NHÓM 3: THẦN (4) ═══
        'nguyen_than': {
            'name': 'Nguyên Thần',
            'desc': 'Hào SINH Dụng Thần → nguồn sức mạnh',
            'impact': 'Nguyên Thần vượng động → DT được sinh, rất tốt.',
            'priority': 'CAO',
        },
        'ky_than': {
            'name': 'Kỵ Thần',
            'desc': 'Hào KHẮC Dụng Thần → kẻ hại',
            'impact': 'Kỵ Thần vượng động → DT bị khắc, rất xấu.',
            'priority': 'CAO',
        },
        'cuu_than': {
            'name': 'Cừu Thần',
            'desc': 'Hào KHẮC Nguyên Thần → kẻ hại gián tiếp',
            'impact': 'Cừu Thần động → Nguyên Thần bị yếu → DT mất nguồn.',
            'priority': 'TRUNG',
        },
        'phuc_than': {
            'name': 'Phục Thần',
            'desc': 'DT ẩn dưới hào khác (khi DT không xuất hiện trong quẻ)',
            'impact': 'Phục Thần lộ → sự việc sẽ xuất hiện. Phục bị khắc → khó.',
            'priority': 'CAO',
        },
        'phi_than': {
            'name': 'Phi Thần',  # ← MỚI THÊM
            'desc': 'Hào che phủ Phục Thần (hào ở vị trí đó trong quẻ chính)',
            'impact': 'Phi sinh Phục → tốt (được che chở). Phi khắc Phục → xấu.',
            'priority': 'TRUNG',
        },

        # ═══ NHÓM 4: HÓA BIẾN (4) ═══
        'tien_than': {
            'name': 'Tiến Thần',
            'desc': 'Hào động hóa sang chi cùng hành nhưng TIẾN (Dần→Mão, Tị→Ngọ)',
            'impact': 'Sự việc tiến triển, phát triển, tăng cường.',
            'priority': 'TRUNG',
        },
        'thoai_than': {
            'name': 'Thoái Thần',
            'desc': 'Hào động hóa sang chi cùng hành nhưng LÙI (Mão→Dần, Ngọ→Tị)',
            'impact': 'Sự việc thoái lui, giảm sút, thu hẹp.',
            'priority': 'TRUNG',
        },
        'hoi_dau_sinh': {
            'name': 'Hồi Đầu Sinh',  # ← MỚI THÊM
            'desc': 'Hào biến SINH lại hào gốc (hào động)',
            'impact': 'CỰC TỐT — sự việc được hỗ trợ quay lại, may mắn.',
            'priority': 'CAO',
        },
        'hoi_dau_khac': {
            'name': 'Hồi Đầu Khắc',  # ← MỚI THÊM
            'desc': 'Hào biến KHẮC lại hào gốc (hào động)',
            'impact': 'CỰC XẤU — sự việc bị chính hệ quả của nó phá hoại.',
            'priority': 'CAO',
        },

        # ═══ NHÓM 5: XUNG HỢP HÌNH PHÁ (8) ═══
        'luc_hop': {
            'name': 'Lục Hợp',
            'desc': '6 cặp hợp: Tý-Sửu, Dần-Hợi, Mão-Tuất, Thìn-Dậu, Tị-Thân, Ngọ-Mùi',
            'pairs': [('Tý','Sửu'),('Dần','Hợi'),('Mão','Tuất'),('Thìn','Dậu'),('Tị','Thân'),('Ngọ','Mùi')],
            'impact': 'Hợp → ràng buộc, chậm nhưng ổn định. Hào bị hợp trụ.',
            'priority': 'TRUNG',
        },
        'luc_xung': {
            'name': 'Lục Xung',
            'desc': '6 cặp xung: Tý-Ngọ, Sửu-Mùi, Dần-Thân, Mão-Dậu, Thìn-Tuất, Tị-Hợi',
            'pairs': [('Tý','Ngọ'),('Sửu','Mùi'),('Dần','Thân'),('Mão','Dậu'),('Thìn','Tuất'),('Tị','Hợi')],
            'impact': 'Xung → phá vỡ, xung đột, ly tán. Ám động hào tĩnh.',
            'priority': 'CAO',
        },
        'tam_hop': {
            'name': 'Tam Hợp Cục',
            'desc': 'Hợi-Mão-Mùi=Mộc, Dần-Ngọ-Tuất=Hỏa, Tị-Dậu-Sửu=Kim, Thân-Tý-Thìn=Thủy',
            'cucs': {'Mộc':('Hợi','Mão','Mùi'),'Hỏa':('Dần','Ngọ','Tuất'),'Kim':('Tị','Dậu','Sửu'),'Thủy':('Thân','Tý','Thìn')},
            'impact': 'Tam hợp cục → tăng cường sức mạnh hành đó.',
            'priority': 'TRUNG',
        },
        'ban_hop': {
            'name': 'Bán Hợp',  # ← MỚI THÊM
            'desc': '2 trong 3 chi tam hợp gặp nhau (Dần-Ngọ, Ngọ-Tuất, Dần-Tuất...)',
            'impact': 'Bán hợp → xu hướng hợp nhưng chưa đủ, cần thêm chi.',
            'priority': 'THẤP',
        },
        'tam_hinh': {
            'name': 'Tam Hình',
            'desc': 'Dần-Tị-Thân (vô ơn), Sửu-Tuất-Mùi (ỷ thế), Tý-Mão (vô lễ), Thìn-Ngọ-Dậu-Hợi (tự hình)',
            'impact': 'Hình → tai họa, tranh chấp, bệnh tật, kiện tụng.',
            'priority': 'TRUNG',
        },
        'pha': {
            'name': 'Phá',
            'desc': 'Tý-Dậu, Sửu-Thìn, Dần-Hợi, Mão-Ngọ, Tị-Thân, Mùi-Tuất',
            'impact': 'Phá → hư hại, tổn thất nhưng nhẹ hơn Xung.',
            'priority': 'THẤP',
        },
        'hai': {
            'name': 'Hại (Lục Hại)',
            'desc': 'Tý-Mùi, Sửu-Ngọ, Dần-Tị, Mão-Thìn, Thân-Hợi, Dậu-Tuất',
            'impact': 'Hại → ngầm hại, ám muội, khó phát hiện.',
            'priority': 'THẤP',
        },
        'phan_ngam': {
            'name': 'Phản Ngâm',
            'desc': 'Hào động hóa sang chi ĐỐI XUNG (Tý→Ngọ, Dần→Thân...)',
            'impact': 'Phản Ngâm → đổi chiều 180°, lật kèo, thay đổi hoàn toàn.',
            'priority': 'CAO',
        },
        'phuc_ngam': {
            'name': 'Phục Ngâm',  # ← MỚI THÊM
            'desc': 'Hào động hóa lại chính chi đó (Tý→Tý, Mão→Mão)',
            'impact': 'Phục Ngâm → lặp lại, trì trệ, không tiến triển.',
            'priority': 'TRUNG',
        },

        # ═══ NHÓM 6: TRẠNG THÁI ĐẶC BIỆT (7) ═══
        'khong_vong': {
            'name': 'Không Vong (Tuần Không)',
            'desc': '2 chi bị trống trong tuần Can Chi (mỗi tuần 10 can, 12 chi → 2 dư)',
            'impact': 'Không vong → hư, giả, chưa thành. Xuất không → thành sau.',
            'priority': 'CAO',
        },
        'triet_lo': {
            'name': 'Triệt Lộ',  # ← MỚI THÊM
            'desc': 'Vị trí ngăn cách giữa 2 tuần Can Chi',
            'impact': 'Hào lâm Triệt → bị cản trở, đứt đoạn, khó thông.',
            'priority': 'TRUNG',
        },
        'mo_kho': {
            'name': 'Mộ Khố',
            'desc': 'Hào nhập Mộ (Kim→Sửu, Mộc→Mùi, Thủy→Thìn, Hỏa→Tuất, Thổ→Thìn)',
            'mo_map': {'Kim':'Sửu','Mộc':'Mùi','Thủy':'Thìn','Hỏa':'Tuất','Thổ':'Thìn'},
            'impact': 'Nhập Mộ → bế tắc, giam giữ. Xung Mộ → giải thoát.',
            'priority': 'CAO',
        },
        'vuong_suy': {
            'name': 'Vượng/Tướng/Hưu/Tù/Tuyệt',
            'desc': 'Trạng thái hào theo Nguyệt Kiến',
            'levels': {'Vượng': 100, 'Tướng': 80, 'Hưu': 50, 'Tù': 30, 'Tuyệt': 10},
            'priority': 'CAO',
        },
        'thai_tue': {
            'name': 'Thái Tuế',
            'desc': 'Chi của NĂM → ảnh hưởng ở tầm vĩ mô',
            'impact': 'Hào trùng Thái Tuế → sự việc lớn, cấp quốc gia.',
            'priority': 'THẤP',
        },
        'tue_pha': {
            'name': 'Tuế Phá',  # ← MỚI THÊM
            'desc': 'Chi ĐỐI XUNG với Thái Tuế (năm Tý → Tuế Phá = Ngọ)',
            'impact': 'Hào lâm Tuế Phá → yếu, khó thành, trắc trở lớn.',
            'priority': 'TRUNG',
        },
        'nguyet_pha': {
            'name': 'Nguyệt Phá',
            'desc': 'Chi ĐỐI XUNG với Nguyệt Kiến (tháng Tý → Nguyệt Phá = Ngọ)',
            'impact': 'Hào lâm Nguyệt Phá → cực yếu, phá hủy, vô dụng.',
            'priority': 'CAO',
        },
        'nhat_pha': {
            'name': 'Nhật Phá',  # ← MỚI THÊM
            'desc': 'Chi ĐỐI XUNG với Nhật Thần',
            'impact': 'Nhẹ hơn Nguyệt Phá nhưng vẫn gây bất lợi trong ngày.',
            'priority': 'THẤP',
        },
    },

    # --- 12 Trường Sinh ---
    'truong_sinh': {
        'stages': ['Trường Sinh','Mộc Dục','Quan Đới','Lâm Quan','Đế Vượng',
                    'Suy','Bệnh','Tử','Mộ','Tuyệt','Thai','Dưỡng'],
        'power': {
            'Trường Sinh': 85, 'Mộc Dục': 40, 'Quan Đới': 70, 'Lâm Quan': 90,
            'Đế Vượng': 100, 'Suy': 45, 'Bệnh': 30, 'Tử': 15,
            'Mộ': 20, 'Tuyệt': 5, 'Thai': 50, 'Dưỡng': 60,
        },
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Xem Nguyệt Nhật', 'desc': 'Đánh giá sức mạnh tổng quan của các hào trong tháng/ngày'},
        'step_2': {'name': 'Tìm Dụng Thần', 'desc': 'Xác định hào đại diện cho sự việc (Dụng Thần) và hào bản thân (Thế)'},
        'step_3': {'name': 'Xét Vượng Suy', 'desc': 'Kiểm tra Dụng Thần vượng hay suy, có bị Tuần Không, Nguyệt Phá không'},
        'step_4': {'name': 'Phân tích Động Hào', 'desc': 'Xem hào động sinh hay khắc Dụng Thần, Hóa Hào tốt hay xấu'},
        'step_5': {'name': 'Xét Xung/Hợp', 'desc': 'Đánh giá tác động của Lục Xung, Lục Hợp, Tam Hợp cục'},
        'step_5b': {'name': 'Xét Bất Thường (Tuần Không/Ngâm)', 'desc': 'Kiểm tra sát sao Phản Ngâm, Phục Ngâm, Tuần Không, Nguyệt Phá'},
        'step_6': {'name': 'Định Cát Hung', 'desc': 'Kết luận cuối cùng dựa trên tương quan sinh khắc và trạng thái của Dụng Thần'},
    },

    # --- Quy tắc verdict ---
    'verdict_rules': {
        'CAT': [
            'DT vượng + được Nguyệt/Nhật sinh',
            'Nguyên Thần vượng động sinh DT',
            'Thế vượng + khắc Ứng (thi đấu)',
            'DT Hồi Đầu Sinh',
            'DT Tiến Thần',
        ],
        'HUNG': [
            'DT suy + bị Nguyệt/Nhật khắc',
            'Kỵ Thần vượng động khắc DT',
            'Thế suy + Ứng vượng (thi đấu)',
            'DT Hồi Đầu Khắc',
            'DT nhập Mộ/Không Vong/Nguyệt Phá',
            'DT Phản Ngâm',
        ],
    },
}

# Placeholder cho các PP khác (sẽ thêm trong Phase 2, 3)
# ═══════════════════════════════════════════════════════════
# [KM] KỲ MÔN ĐỘN GIÁP — 30 yếu tố
# ═══════════════════════════════════════════════════════════
KM_TREE = {
    'name': 'Kỳ Môn Độn Giáp',
    'coverage': '30/30 = 100%',

    # --- Bát Môn (8 cửa) ---
    'bat_mon': {
        'Khai Môn':  {'hanh': 'Kim', 'cat_hung': 'ĐẠI CÁT', 'y_nghia': 'Mở cửa, khởi đầu, khai trương'},
        'Hưu Môn':  {'hanh': 'Thủy','cat_hung': 'CÁT',     'y_nghia': 'Nghỉ ngơi, hưởng lộc, yên ổn'},
        'Sinh Môn':  {'hanh': 'Thổ', 'cat_hung': 'ĐẠI CÁT', 'y_nghia': 'Sinh sôi, phát triển, tài lộc'},
        'Thương Môn': {'hanh': 'Mộc','cat_hung': 'TIỂU CÁT','y_nghia': 'Kinh doanh, buôn bán, đi xa'},
        'Đỗ Môn':   {'hanh': 'Mộc', 'cat_hung': 'BÌNH',     'y_nghia': 'Bế tắc, che giấu, ẩn nấp'},
        'Cảnh Môn':  {'hanh': 'Hỏa','cat_hung': 'BÌNH',     'y_nghia': 'Phô trương, khoe khoang, kiện tụng'},
        'Tử Môn':   {'hanh': 'Thổ', 'cat_hung': 'ĐẠI HUNG','y_nghia': 'Chết chóc, tang tóc, tai họa'},
        'Kinh Môn':  {'hanh': 'Kim', 'cat_hung': 'HUNG',     'y_nghia': 'Kinh sợ, lo lắng, tranh chấp'},
    },

    # --- Cửu Tinh (9 sao) ---
    'cuu_tinh': {
        'Thiên Bồng': {'hanh': 'Thủy','cat_hung': 'HUNG',  'y_nghia': 'Trộm cắp, mưu mô, ẩn giấu'},
        'Thiên Nhậm': {'hanh': 'Thổ', 'cat_hung': 'CÁT',   'y_nghia': 'Hiền lành, nhân từ, bệnh tật'},
        'Thiên Xung': {'hanh': 'Mộc', 'cat_hung': 'CÁT',   'y_nghia': 'Dũng mãnh, xung phong, đi xa'},
        'Thiên Phụ': {'hanh': 'Mộc', 'cat_hung': 'CÁT',    'y_nghia': 'Phù trợ, giúp đỡ, quý nhân'},
        'Thiên Anh': {'hanh': 'Hỏa', 'cat_hung': 'BÌNH',   'y_nghia': 'Phô trương, văn chương, kiện tụng'},
        'Thiên Nhuế': {'hanh': 'Thổ','cat_hung': 'HUNG',    'y_nghia': 'Ngu muội, trì trệ, bệnh lâu'},
        'Thiên Cầm': {'hanh': 'Thổ', 'cat_hung': 'CÁT',    'y_nghia': 'Trung tâm, chủ tọa, ổn định'},
        'Thiên Trụ': {'hanh': 'Kim', 'cat_hung': 'HUNG',    'y_nghia': 'Phá hoại, gian dối, phản bội'},
        'Thiên Tâm': {'hanh': 'Kim', 'cat_hung': 'CÁT',    'y_nghia': 'Chữa bệnh, quân sư, mưu lược'},
    },

    # --- Bát Thần (8 thần) ---
    'bat_than': {
        'Trực Phù': {'cat_hung': 'CÁT',  'y_nghia': 'Quý nhân, chính đạo, lãnh đạo'},
        'Đằng Xà':  {'cat_hung': 'HUNG', 'y_nghia': 'Kinh sợ, ác mộng, lừa dối'},
        'Thái Âm':  {'cat_hung': 'CÁT',  'y_nghia': 'Ẩn mật, che chở, nữ quý nhân'},
        'Lục Hợp':  {'cat_hung': 'CÁT',  'y_nghia': 'Hôn nhân, hợp tác, giao dịch'},
        'Bạch Hổ':  {'cat_hung': 'HUNG', 'y_nghia': 'Hung dữ, tai nạn, đau ốm'},
        'Huyền Vũ': {'cat_hung': 'HUNG', 'y_nghia': 'Trộm cắp, gian lận, mất mát'},
        'Cửu Địa':  {'cat_hung': 'CÁT',  'y_nghia': 'Phòng thủ, ẩn náu, bất động sản'},
        'Cửu Thiên': {'cat_hung': 'CÁT', 'y_nghia': 'Tiến công, đi xa, bay cao'},
    },

    # --- Tam Kỳ (3 Kỳ) ← MỚI ---
    'tam_ky': {
        'Ất': {'ten': 'Nhật Kỳ', 'y_nghia': 'Quý nhân ban ngày, mưu sự thuận'},
        'Bính': {'ten': 'Nguyệt Kỳ', 'y_nghia': 'Uy quyền, sức mạnh, oai phong'},
        'Đinh': {'ten': 'Tinh Kỳ', 'y_nghia': 'Văn thư, thi cử, trí tuệ'},
    },

    # --- Lục Nghi (6 Nghi) ← MỚI ---
    'luc_nghi': {
        'Mậu': {'giap': 'Giáp Tý', 'y_nghia': 'Đứng đầu, chủ soái'},
        'Kỷ':  {'giap': 'Giáp Tuất', 'y_nghia': 'Phó tướng, phụ tá'},
        'Canh': {'giap': 'Giáp Thân', 'y_nghia': 'Đối thủ, hung thần, kim khí'},
        'Tân': {'giap': 'Giáp Ngọ', 'y_nghia': 'Sai lầm, trở ngại'},
        'Nhâm': {'giap': 'Giáp Thìn', 'y_nghia': 'Ngoại giao, linh hoạt'},
        'Quý': {'giap': 'Giáp Dần', 'y_nghia': 'Ẩn mật, bí mật'},
    },

    # --- Cách Cục ← MỚI ---
    'cach_cuc': {
        'cat_cach': [
            'Ất+Khai Môn → Ngọc Nữ thủ môn',
            'Bính+Sinh Môn → Phi Điểu đậu huyệt',
            'Đinh+Hưu Môn → Thanh Long phản thủ',
            'Tam Kỳ nhập cung Vượng → Đại Cát',
            'Thiên Phụ+Khai Môn+Trực Phù → Tam Cát hội',
        ],
        'hung_cach': [
            'Canh+Tử Môn → Hổ xung bách sự',
            'Canh+Kinh Môn → Đại cách hung',
            'Thiên Nhuế+Tử Môn → Cực Hung',
            'Huyền Vũ+Đằng Xà → Mưu hại, lừa dối',
            'Tam Kỳ nhập Mộ/Không → Kỳ bị phế',
        ],
    },

    # --- Factors bổ sung ---
    'factors': {
        'ma_tinh': {'name': 'Mã Tinh', 'desc': 'Ngựa di chuyển → đi xa, chuyển dời'},
        'khong_vong': {'name': 'Không Vong', 'desc': 'Hư ảo, chưa xảy ra'},
        'am_can': {'name': 'Ám Can', 'desc': 'Can ẩn trong cung → thông tin ẩn giấu'},  # ← MỚI
        'than_ban': {'name': 'Thần Bàn', 'desc': 'Bàn thần linh → yếu tố tâm linh'},  # ← MỚI
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Xác định Dụng Thần', 'desc': 'Tìm Can đại diện cho người/việc (Can ngày, Can giờ, Can năm)'},
        'step_2': {'name': 'Xem Trực Phù, Trực Sử', 'desc': 'Xác định xu hướng lớn và sự kiện chính đang chi phối'},
        'step_3': {'name': 'Phân tích Cung Dụng Thần', 'desc': 'Đánh giá Bát Môn (nhân sự), Cửu Tinh (thiên thời), Bát Thần (tâm linh)'},
        'step_4': {'name': 'Xét Thiên Can, Địa Bàn', 'desc': 'Xem tương tác giữa Can thiên bàn và Can địa bàn'},
        'step_5': {'name': 'Luận Cách Cục', 'desc': 'Xem có rơi vào Cát Cách hay Hung Cách đặc biệt không'},
        'step_5b': {'name': 'Xét Bất Thường (Không Vong/Ngâm)', 'desc': 'Kiểm tra Không Vong, Phản Ngâm, Phục Ngâm của Cung Dụng Thần'},
        'step_6': {'name': 'Định Cát Hung', 'desc': 'Kết luận tổng thể dựa trên cung Dụng Thần sinh khắc với cung Thế/Can ngày'},
    },

    'verdict_rules': {
        'CAT': ['Cửa Cát + Sao Cát + Cung Vượng', 'Tam Kỳ nhập cung', 'Cát Cách'],
        'HUNG': ['Cửa Hung + Sao Hung', 'Hung Cách', 'Tam Kỳ nhập Mộ/Không'],
    },
}
# ═══════════════════════════════════════════════════════════
# [MH] MAI HOA DỊCH SỐ — 11 yếu tố (fix 6 thiếu)
# ═══════════════════════════════════════════════════════════
MH_TREE = {
    'name': 'Mai Hoa Dịch Số',
    'coverage': '11/11 = 100%',

    # --- Quái cơ bản ---
    'quai': {
        'Nội Quái':  {'desc': 'Quẻ dưới (3 hào dưới) = Thể', 'alias': 'Hạ Quái'},
        'Ngoại Quái': {'desc': 'Quẻ trên (3 hào trên) = Dụng', 'alias': 'Thượng Quái'},
        'Hỗ Quái':  {'desc': 'Quẻ ẩn (hào 2-3-4 và 3-4-5)', 'role': 'Diễn biến giữa'},
        'Biến Quái': {'desc': 'Quẻ sau khi Động Hào biến', 'role': 'Kết quả cuối'},
    },

    # --- 4 Công thức CỐT LÕI ← FIX QUAN TRỌNG ---
    'sinh_khac': {
        'the_sinh_dung': {
            'name': 'Thể Sinh Dụng',
            'desc': 'Hành Thể Quái SINH hành Dụng Quái',
            'verdict': 'HUNG — Ta bị hao tổn, cho đi, mất mát',
            'vi_du': 'Mộc (Thể) sinh Hỏa (Dụng) → ta tốn sức cho người',
        },
        'dung_sinh_the': {
            'name': 'Dụng Sinh Thể',
            'desc': 'Hành Dụng Quái SINH hành Thể Quái',
            'verdict': 'CÁT — Ta được hưởng lợi, nhận được',
            'vi_du': 'Thủy (Dụng) sinh Mộc (Thể) → ta được giúp đỡ',
        },
        'the_khac_dung': {
            'name': 'Thể Khắc Dụng',
            'desc': 'Hành Thể Quái KHẮC hành Dụng Quái',
            'verdict': 'CÁT — Ta chiến thắng, đạt được mục tiêu',
            'vi_du': 'Kim (Thể) khắc Mộc (Dụng) → ta thắng đối phương',
        },
        'dung_khac_the': {
            'name': 'Dụng Khắc Thể',
            'desc': 'Hành Dụng Quái KHẮC hành Thể Quái',
            'verdict': 'HUNG — Ta bị hại, thất bại, tổn thương',
            'vi_du': 'Hỏa (Dụng) khắc Kim (Thể) → ta bị đối phương hại',
        },
        'ty_hoa': {
            'name': 'Tỷ Hòa',
            'desc': 'Hành Thể = Hành Dụng (cùng hành)',
            'verdict': 'BÌNH — Cân bằng, không được không mất',
        },
    },

    # --- Bát Quái mapping ---
    'bat_quai': {
        'Càn':  {'hanh': 'Kim', 'so': 1, 'huong': 'Tây Bắc', 'tuong': 'Trời/Cha'},
        'Đoài': {'hanh': 'Kim', 'so': 2, 'huong': 'Tây',      'tuong': 'Đầm/Con gái út'},
        'Ly':   {'hanh': 'Hỏa','so': 3, 'huong': 'Nam',       'tuong': 'Lửa/Con gái giữa'},
        'Chấn': {'hanh': 'Mộc','so': 4, 'huong': 'Đông',      'tuong': 'Sấm/Con trai cả'},
        'Tốn':  {'hanh': 'Mộc','so': 5, 'huong': 'Đông Nam',  'tuong': 'Gió/Con gái cả'},
        'Khảm': {'hanh': 'Thủy','so':6, 'huong': 'Bắc',       'tuong': 'Nước/Con trai giữa'},
        'Cấn':  {'hanh': 'Thổ','so': 7, 'huong': 'Đông Bắc',  'tuong': 'Núi/Con trai út'},
        'Khôn': {'hanh': 'Thổ','so': 8, 'huong': 'Tây Nam',   'tuong': 'Đất/Mẹ'},
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Xác định Thể/Dụng', 'desc': 'Quẻ không có hào động là Thể (ta), quẻ có hào động là Dụng (sự việc)'},
        'step_2': {'name': 'Phân tích Ngũ Hành Sinh Khắc', 'desc': 'Xét quan hệ Thể và Dụng (Dụng sinh Thể, Thể khắc Dụng...)'},
        'step_3': {'name': 'Đánh giá Thể Vượng/Suy', 'desc': 'Xem hành của Thể Quái có vượng theo mùa/tháng không'},
        'step_4': {'name': 'Xét Hỗ Quái', 'desc': 'Phân tích diễn biến trung gian của sự việc'},
        'step_5': {'name': 'Xét Biến Quái', 'desc': 'Xem kết quả cuối cùng sự việc qua sự sinh khắc của Biến Quái với Thể Quái'},
        'step_6': {'name': 'Định Cát Hung', 'desc': 'Đưa ra kết luận tổng quan từ cả Dụng Quái, Hỗ Quái và Biến Quái'},
    },

    'verdict_rules': {
        'CAT': ['Dụng Sinh Thể', 'Thể Khắc Dụng', 'Thể vượng + Dụng suy'],
        'HUNG': ['Thể Sinh Dụng', 'Dụng Khắc Thể', 'Thể suy + Dụng vượng'],
        'BINH': ['Tỷ Hòa'],
    },
}
# ═══════════════════════════════════════════════════════════
# [LN] ĐẠI LỤC NHÂM — 19 yếu tố (fix 5 thiếu)
# ═══════════════════════════════════════════════════════════
LN_TREE = {
    'name': 'Đại Lục Nhâm',
    'coverage': '19/19 = 100%',

    'thien_tuong': {
        'Quý Nhân':  {'cat_hung': 'CÁT', 'y_nghia': 'Quý nhân phù trợ'},
        'Đằng Xà':  {'cat_hung': 'HUNG','y_nghia': 'Kinh sợ, ác mộng'},
        'Chu Tước':  {'cat_hung': 'BÌNH','y_nghia': 'Văn thư, khẩu thiệt'},
        'Lục Hợp':  {'cat_hung': 'CÁT', 'y_nghia': 'Hôn nhân, hợp tác'},
        'Câu Trận':  {'cat_hung': 'HUNG','y_nghia': 'Tranh chấp, kiện tụng'},  # ← MỚI
        'Thanh Long': {'cat_hung': 'CÁT','y_nghia': 'Tài lộc, vui mừng'},
        'Thiên Không': {'cat_hung':'HUNG','y_nghia': 'Hư không, giả dối'},
        'Bạch Hổ':  {'cat_hung': 'HUNG','y_nghia': 'Tang tóc, bệnh tật'},
        'Thái Thường': {'cat_hung':'CÁT','y_nghia': 'Ăn uống, lễ lạc'},
        'Huyền Vũ':  {'cat_hung': 'HUNG','y_nghia': 'Trộm cắp, gian lận'},
        'Thái Âm':  {'cat_hung': 'CÁT', 'y_nghia': 'Ẩn mật, nữ quý nhân'},
        'Thiên Hậu': {'cat_hung': 'CÁT','y_nghia': 'Phụ nữ, hôn nhân'},
    },

    'tu_khoa': {
        'so_khoa':   {'name': 'Sơ Khóa', 'desc': 'Khóa thứ 1 — khởi đầu sự việc'},
        'trung_khoa': {'name': 'Trung Khóa', 'desc': 'Khóa thứ 2 — diễn biến giữa'},
        'mat_khoa':  {'name': 'Mạt Khóa', 'desc': 'Khóa thứ 3 — kết quả cuối'},
        'luu_nien':  {'name': 'Lưu Niên Khóa', 'desc': 'Khóa năm — vận hạn năm'},
    },

    'tam_truyen': {
        'so_truyen':   {'desc': 'Truyền thứ 1 — sự việc bắt đầu'},
        'trung_truyen': {'desc': 'Truyền thứ 2 — quá trình'},
        'mat_truyen':  {'desc': 'Truyền thứ 3 — kết cục'},
    },

    'factors': {
        'thien_ban': {'name': 'Thiên Bàn', 'desc': '12 chi xoay trên'},
        'dia_ban':   {'name': 'Địa Bàn', 'desc': '12 chi cố định dưới'},
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Xem Thiên Địa Bàn', 'desc': 'Đánh giá tổng quan sự việc qua sự dịch chuyển của 12 chi'},
        'step_2': {'name': 'Phân tích Tứ Khóa', 'desc': 'Xét âm dương, khách chủ, động tĩnh qua 4 khóa'},
        'step_3': {'name': 'Luận Tam Truyền', 'desc': 'Phân tích Sơ truyền (bắt đầu), Trung truyền (diễn biến), Mạt truyền (kết thúc)'},
        'step_4': {'name': 'Xét Thiên Tướng', 'desc': 'Đánh giá sự trợ giúp hay phá hoại của 12 thiên tướng (Quý Nhân, Bạch Hổ...)'},
        'step_5': {'name': 'Định Cát Hung', 'desc': 'Kết hợp toàn bộ yếu tố để đưa ra dự đoán chi tiết'},
    },

    'verdict_rules': {
        'CAT': [
            'Sơ Truyền gặp Quý Nhân/Thanh Long/Lục Hợp',
            'Tam Truyền thuận hành (không xung khắc)',
            'Thiên Tướng cát chiếu khóa chính',
            'Can ngày sinh Can chi lạc cung',
        ],
        'HUNG': [
            'Sơ Truyền gặp Bạch Hổ/Đằng Xà/Huyền Vũ',
            'Tam Truyền nghịch hành (xung khắc liên hoàn)',
            'Thiên Tướng hung chiếu khóa chính',
            'Can ngày bị khắc bởi chi lạc cung',
        ],
    },
}

# ═══════════════════════════════════════════════════════════
# [TA] THÁI ẤT THẦN SỐ — 13 yếu tố (fix 10 thiếu)
# ═══════════════════════════════════════════════════════════
TA_TREE = {
    'name': 'Thái Ất Thần Số',
    'coverage': '13/13 = 100%',

    'factors': {
        'thai_at':     {'name': 'Thái Ất', 'desc': 'Sao chủ, trung tâm hệ thống'},
        'cuu_cung':    {'name': 'Cửu Cung', 'desc': '9 cung Lạc Thư'},
        'thai_at_tich': {'name': 'Thái Ất Tích', 'desc': 'Số tích lũy theo niên'},
        'ngu_phuc':    {'name': 'Ngũ Phúc', 'desc': 'Phúc Đức Hòa Thiên — 5 phúc lành'},
        'thien_muc':   {'name': 'Thiên Mục', 'desc': 'Mắt trời — giám sát từ trên'},
        'dia_muc':     {'name': 'Địa Mục', 'desc': 'Mắt đất — giám sát từ dưới'},
        'chu_toan':    {'name': 'Chủ Toán', 'desc': 'Số chủ — bên ta'},
        'khach_toan':  {'name': 'Khách Toán', 'desc': 'Số khách — bên đối phương'},
        'trung_thien': {'name': 'Trung Thiên', 'desc': 'Trung tâm trời — vận khí'},
        'thien_ban':   {'name': 'Thiên Bàn (TA)', 'desc': 'Bàn trời Thái Ất'},
        'dia_ban':     {'name': 'Địa Bàn (TA)', 'desc': 'Bàn đất Thái Ất'},
        'cung_than':   {'name': 'Cung Thân', 'desc': 'Cung an thân → vị trí bản thân'},
        'cung_menh':   {'name': 'Cung Mệnh', 'desc': 'Cung an mệnh → số mệnh'},
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Xác định vị trí Thái Ất', 'desc': 'Xem sao Thái Ất nằm ở cung nào, có lâm hung cung không'},
        'step_2': {'name': 'Đọc Toán Số', 'desc': 'Đọc thông số Chủ Toán (đại diện bên ta) và Khách Toán (đối phương) từ dữ liệu hệ thống'},
        'step_3': {'name': 'Xét Ngũ Phúc', 'desc': 'Kiểm tra vị trí và tác động của sao Ngũ Phúc (hỗ trợ/ban phước)'},
        'step_4': {'name': 'Xem Thiên Mục/Địa Mục', 'desc': 'Đánh giá sự giám sát và các biến động từ trên và dưới'},
        'step_5': {'name': 'Định Cát Hung', 'desc': 'So sánh Chủ Toán - Khách Toán và vị trí các tinh tú để kết luận thắng bại/cát hung'},
    },

    'verdict_rules': {
        'CAT': ['Chủ Toán > Khách Toán', 'Ngũ Phúc lâm cát cung'],
        'HUNG': ['Khách Toán > Chủ Toán', 'Thái Ất lâm hung cung'],
    },
}

# ═══════════════════════════════════════════════════════════
# [TB] THIẾT BẢN THẦN SỐ — 6 yếu tố (100% đầy đủ)
# ═══════════════════════════════════════════════════════════
TB_TREE = {
    'name': 'Thiết Bản Thần Số',
    'coverage': '6/6 = 100%',
    'factors': {
        'thiet_ban': {'name': 'Thiết Bản', 'desc': 'Bảng sắt — số cố định'},
        'than_so':   {'name': 'Thần Số', 'desc': 'Số thần bí → mã vận mệnh'},
        'lac_thu':   {'name': 'Lạc Thư', 'desc': 'Ma phương 3×3 (Hậu Thiên)'},
        'ha_do':     {'name': 'Hà Đồ', 'desc': 'Số gốc Ngũ Hành (Tiên Thiên)'},
        'cuu_cung':  {'name': 'Cửu Cung', 'desc': '9 cung Lạc Thư'},
        'bat_quai':  {'name': 'Bát Quái', 'desc': '8 quẻ cơ bản'},
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Đọc Bát Tự', 'desc': 'Đọc thông tin ngày giờ tháng năm sinh từ dữ liệu đã lập'},
        'step_2': {'name': 'Phân tích Quẻ', 'desc': 'Phân tích các quẻ Tiên Thiên và Hậu Thiên đã được hệ thống tính toán'},
        'step_3': {'name': 'Đọc Thần Số', 'desc': 'Tra cứu con số Thần Số vận mệnh từ dữ liệu hệ thống'},
        'step_4': {'name': 'Tra Thiết Bản', 'desc': 'Dùng Thần Số để tra các câu văn trong sách Thiết Bản'},
        'step_5': {'name': 'Giải Đoán', 'desc': 'Luận giải vận mệnh cả đời qua các câu văn'},
    },

    'verdict_rules': {
        'CAT': [
            'Nạp Âm hành tương sinh với hành bản mệnh',
            'Thần Số rơi vào cung Cát (1, 6, 8)',
            'Câu văn Thiết Bản mang ý nghĩa thuận lợi',
        ],
        'HUNG': [
            'Nạp Âm hành xung khắc với hành bản mệnh',
            'Thần Số rơi vào cung Hung (2, 5)',
            'Câu văn Thiết Bản mang ý nghĩa trắc trở',
        ],
    },
}

# ═══════════════════════════════════════════════════════════
# [TV] TỬ VI ĐẨU SỐ — 22 yếu tố (fix 2 thiếu)
# ═══════════════════════════════════════════════════════════
TV_TREE = {
    'name': 'Tử Vi Đẩu Số',
    'coverage': '22/22 = 100%',

    'chinh_tinh': {
        'Tử Vi':     {'hanh': 'Thổ', 'role': 'Đế tinh — vua, quyền lực tối cao'},
        'Thiên Cơ':  {'hanh': 'Mộc', 'role': 'Mưu sĩ — trí tuệ, linh hoạt'},
        'Thái Dương': {'hanh': 'Hỏa','role': 'Mặt trời — nam giới, cha, quý nhân'},
        'Vũ Khúc':   {'hanh': 'Kim', 'role': 'Tài tinh — tiền bạc, quyết đoán'},
        'Thiên Đồng': {'hanh': 'Thủy','role':'Phúc tinh — hưởng thụ, lười biếng'},
        'Liêm Trinh': {'hanh': 'Hỏa','role': 'Đào hoa — sắc đẹp, thị phi'},
        'Thiên Phủ': {'hanh': 'Thổ', 'role': 'Kho tàng — giàu có, ổn định'},
        'Thái Âm':   {'hanh': 'Thủy','role': 'Mặt trăng — nữ giới, mẹ'},
        'Tham Lang':  {'hanh': 'Mộc','role': 'Đào hoa — ham muốn, đa tài'},
        'Cự Môn':    {'hanh': 'Thủy','role': 'Ám tinh — thị phi, tranh cãi'},
        'Thiên Tướng': {'hanh':'Thủy','role':'Ấn tinh — giúp đỡ, bảo hộ'},
        'Thiên Lương': {'hanh':'Mộc','role': 'Thọ tinh — hiền lành, trường thọ'},
        'Thất Sát':  {'hanh': 'Kim', 'role': 'Sát tinh — quyền lực, sát khí'},
        'Phá Quân':  {'hanh': 'Thủy','role': 'Phá hoại — đổi mới, phá cũ'},
    },

    'phu_tinh': {  # ← MỚI — top 20 phụ tinh quan trọng
        'Tả Phụ':    {'cat_hung': 'CÁT', 'role': 'Quý nhân bên trái'},
        'Hữu Bật':   {'cat_hung': 'CÁT', 'role': 'Quý nhân bên phải'},
        'Văn Xương':  {'cat_hung': 'CÁT', 'role': 'Học vấn, thi cử'},
        'Văn Khúc':   {'cat_hung': 'CÁT', 'role': 'Nghệ thuật, tài năng'},
        'Thiên Khôi': {'cat_hung': 'CÁT', 'role': 'Quý nhân dương'},
        'Thiên Việt': {'cat_hung': 'CÁT', 'role': 'Quý nhân âm'},
        'Lộc Tồn':   {'cat_hung': 'CÁT', 'role': 'Tài lộc chính'},
        'Thiên Mã':   {'cat_hung': 'CÁT', 'role': 'Di chuyển, đi xa'},
        'Hỏa Tinh':  {'cat_hung': 'HUNG','role': 'Nóng nảy, tai nạn'},
        'Linh Tinh':  {'cat_hung': 'HUNG','role': 'Bất ngờ, tai ương'},
        'Kình Dương': {'cat_hung': 'HUNG','role': 'Cứng rắn, bạo lực'},
        'Đà La':     {'cat_hung': 'HUNG','role': 'Trì trệ, chậm chạp'},
        'Địa Không':  {'cat_hung': 'HUNG','role': 'Mất mát, trống rỗng'},
        'Địa Kiếp':  {'cat_hung': 'HUNG','role': 'Cướp đoạt, phá sản'},
        'Thiên Hình': {'cat_hung': 'HUNG','role': 'Hình phạt, pháp luật'},
        'Thiên Riêu': {'cat_hung': 'HUNG','role': 'Đào hoa xấu, dâm dục'},
        'Hóa Lộc':   {'cat_hung': 'CÁT', 'role': 'Tứ Hóa — tài lộc tăng'},
        'Hóa Quyền':  {'cat_hung': 'CÁT', 'role': 'Tứ Hóa — quyền lực tăng'},
        'Hóa Khoa':  {'cat_hung': 'CÁT', 'role': 'Tứ Hóa — danh tiếng tăng'},
        'Hóa Kỵ':   {'cat_hung': 'HUNG','role': 'Tứ Hóa — trở ngại, khó khăn'},
    },

    'dai_han':  {'desc': '10 năm 1 hạn — vận hạn dài'},
    'tieu_han': {'desc': '1 năm 1 hạn — vận hạn ngắn'},  # ← MỚI
    'luu_nien': {'desc': 'Năm hiện tại — vận trong năm'},

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Xem Mệnh/Thân', 'desc': 'Đánh giá cung Mệnh (tiềm năng) và cung Thân (hành động sau 30 tuổi)'},
        'step_2': {'name': 'Khảo sát Chính Tinh', 'desc': 'Xem các sao chính chiếu Mệnh và các cung tam phương tứ chính'},
        'step_3': {'name': 'Xét Phụ Tinh, Sát Tinh', 'desc': 'Kiểm tra Lục Cát (tốt) và Lục Sát (xấu) tác động thế nào'},
        'step_4': {'name': 'Phân tích Tứ Hóa', 'desc': 'Xem Lộc, Quyền, Khoa, Kỵ làm biến đổi ý nghĩa các sao ra sao'},
        'step_5': {'name': 'Xem Vận Hạn', 'desc': 'Đánh giá Đại Hạn (10 năm) và Lưu Niên (1 năm) để dự báo sự kiện'},
    },

    'verdict_rules': {
        'CAT': [
            'Mệnh có Lục Cát tinh hội chiếu (Tả Phụ, Hữu Bật, Văn Xương, Văn Khúc, Thiên Khôi, Thiên Việt)',
            'Hóa Lộc/Hóa Quyền/Hóa Khoa chiếu Mệnh',
            'Chính Tinh miếu vượng tại cung Mệnh',
            'Đại Hạn/Lưu Niên gặp Tam Cát hóa',
        ],
        'HUNG': [
            'Mệnh có Lục Sát tinh hội chiếu (Kình Dương, Đà La, Hỏa Tinh, Linh Tinh, Địa Không, Địa Kiếp)',
            'Hóa Kỵ nhập Mệnh/Thân',
            'Chính Tinh hãm địa tại cung Mệnh',
            'Đại Hạn/Lưu Niên gặp Hóa Kỵ + Sát tinh',
        ],
    },
}

# ═══════════════════════════════════════════════════════════
# [XND] XEM NGÀY ĐẸP — 21 yếu tố (fix 4 thiếu)
# ═══════════════════════════════════════════════════════════
XND_TREE = {
    'name': 'Xem Ngày Đẹp',
    'coverage': '21/21 = 100%',

    'hoang_dao': {
        'Thanh Long':  {'cat_hung': 'CÁT', 'gio': 'Dần'},
        'Minh Đường':  {'cat_hung': 'CÁT', 'gio': 'Mão'},
        'Kim Quỹ':    {'cat_hung': 'CÁT', 'gio': 'Thìn'},
        'Thiên Đức':  {'cat_hung': 'CÁT', 'gio': 'Tị'},
        'Ngọc Đường':  {'cat_hung': 'CÁT', 'gio': 'Ngọ'},
        'Tư Mệnh':   {'cat_hung': 'CÁT', 'gio': 'Mùi'},
    },

    'hac_dao': {
        'Thiên Hình':  {'cat_hung': 'HUNG'},
        'Chu Tước':   {'cat_hung': 'HUNG'},
        'Bạch Hổ':   {'cat_hung': 'HUNG'},
        'Thiên Lao':  {'cat_hung': 'HUNG'},
        'Huyền Vũ':  {'cat_hung': 'HUNG'},
        'Câu Trận':   {'cat_hung': 'HUNG'},
    },

    'truc_12': {
        'Kiến': {'cat_hung': 'BÌNH', 'lam': 'Khởi công, khai trương'},
        'Trừ':  {'cat_hung': 'CÁT',  'lam': 'Trừ tà, dọn dẹp, chữa bệnh'},
        'Mãn':  {'cat_hung': 'CÁT',  'lam': 'Mọi việc đều tốt'},
        'Bình':  {'cat_hung': 'CÁT', 'lam': 'Sửa đường, xây dựng'},
        'Định':  {'cat_hung': 'CÁT', 'lam': 'Ổn định, hôn nhân'},
        'Chấp':  {'cat_hung': 'BÌNH','lam': 'Bắt giữ, thu hoạch'},
        'Phá':  {'cat_hung': 'HUNG', 'lam': 'Phá dỡ, không nên khởi sự'},
        'Nguy':  {'cat_hung': 'HUNG','lam': 'Nguy hiểm, không nên mạo hiểm'},
        'Thành':  {'cat_hung': 'CÁT','lam': 'Thành công, hoàn tất'},
        'Thu':  {'cat_hung': 'BÌNH', 'lam': 'Thu hoạch, cất giữ'},
        'Khai':  {'cat_hung': 'CÁT', 'lam': 'Khai trương, khởi đầu'},
        'Bế':   {'cat_hung': 'HUNG', 'lam': 'Đóng cửa, không nên làm gì'},
    },

    # --- Yếu tố kỵ ← MỚI ---
    'ky_nhat': {
        'nguyet_ky':     {'desc': 'Ngày mùng 5, 14, 23 hàng tháng — KỴ mọi việc lớn'},
        'tam_nuong':     {'desc': 'Ngày 3, 7, 13, 18, 22, 27 — KỴ cưới hỏi, khởi sự'},
        'duong_cong_ky': {'desc': '13 ngày Dương Công kỵ — KỴ tuyệt đối: 13/1, 11/2, 9/3, 7/4, 5/5, 3/6, 8/7, 6/8, 4/9, 2/10, 30/11, 28/12'},
        'sat_chu':       {'desc': 'Ngày sát chủ theo tuổi — cần tránh'},
        'thien_an':      {'desc': 'Ngày Thiên Ân — TRÁNH cưới, KỴ tang'},
    },

    # --- Sao tốt ---
    'sao_tot': {
        'Thiên Đức':  {'desc': 'Ngày có Thiên Đức hợp → mọi việc hanh thông'},
        'Nguyệt Đức': {'desc': 'Ngày có Nguyệt Đức hợp → giải được xấu'},
    },

    # --- Quy trình luận giải chuẩn ---
    'interpretation_steps': {
        'step_1': {'name': 'Loại Ngày Kỵ', 'desc': 'Tránh Tam Nương, Nguyệt Kỵ, Dương Công, Sát Chủ'},
        'step_2': {'name': 'Xét Hoàng Đạo/Hắc Đạo', 'desc': 'Ưu tiên ngày có các sao Hoàng Đạo (Thanh Long, Kim Quỹ...)'},
        'step_3': {'name': 'Xem Trực 12', 'desc': 'Chọn Trực phù hợp với việc cần làm (Khai, Thành, Mãn...)'},
        'step_4': {'name': 'Xét Ngũ Hành Sinh Khắc', 'desc': 'Ngày phải tương sinh hoặc không xung khắc với tuổi người dùng'},
        'step_5': {'name': 'Định Cát Hung', 'desc': 'Chốt ngày giờ tốt nhất cho sự kiện cụ thể'},
    },

    'verdict_rules': {
        'CAT': [
            'Ngày Hoàng Đạo (Thanh Long, Minh Đường, Kim Quỹ, Thiên Đức, Ngọc Đường, Tư Mệnh)',
            'Trực Cát (Khai, Thành, Mãn, Định, Trừ, Bình)',
            'Không trùng Tam Nương, Nguyệt Kỵ, Dương Công',
            'Ngũ Hành ngày tương sinh/tỷ hòa với tuổi',
            'Có Thiên Đức/Nguyệt Đức hợp',
        ],
        'HUNG': [
            'Ngày Hắc Đạo (Thiên Hình, Chu Tước, Bạch Hổ, Thiên Lao, Huyền Vũ, Câu Trận)',
            'Trực Hung (Phá, Nguy, Bế)',
            'Trùng Tam Nương hoặc Nguyệt Kỵ hoặc Dương Công Kỵ',
            'Ngũ Hành ngày xung khắc với tuổi',
            'Trùng Sát Chủ theo tuổi',
        ],
    },
}

# ═══════════════════════════════════════════════════════════
# [VV] VẠN VẬT TỔNG HỢP — Sơ đồ hình cây theo Ngũ Hành
# 2226+ items, phân cấp: Hành → Danh mục → Items
# Cross-ref: Trường Sinh + Suy Vượng
# ═══════════════════════════════════════════════════════════

# Import data thực từ van_vat_tong_hop.py
try:
    from van_vat_tong_hop import (
        NGU_HANH_VAN_VAT, VAN_VAT_MO_RONG, VAN_VAT_BO_SUNG,
        TRUONG_SINH_TRANG_THAI,
    )
    _VV_IMPORTED = True
except ImportError:
    NGU_HANH_VAN_VAT = {}
    VAN_VAT_MO_RONG = {}
    VAN_VAT_BO_SUNG = {}
    TRUONG_SINH_TRANG_THAI = {}
    _VV_IMPORTED = False

VV_TREE = {
    'name': 'Vạn Vật Loại Tượng Tổng Hợp',
    'total_items': '2226+',

    # ═══ TẦNG 1: NGŨ HÀNH → DANH MỤC ═══
    # Mỗi hành có 20 danh mục cơ bản + 15 mở rộng + 10 bổ sung
    'ngu_hanh': {
        'Kim': {
            'tinh_chat': 'Cứng, sắc bén, thu gom, sát phạt',
            'mau_sac': 'Trắng, bạc, vàng kim',
            'huong': 'Tây',
            'mua': 'Thu',
            'categories': list(NGU_HANH_VAN_VAT.get('Kim', {}).keys()) if NGU_HANH_VAN_VAT else [],
            'mo_rong': list(VAN_VAT_MO_RONG.get('Kim', {}).keys()) if VAN_VAT_MO_RONG else [],
            'bo_sung': list(VAN_VAT_BO_SUNG.get('Kim', {}).keys()) if VAN_VAT_BO_SUNG else [],
        },
        'Mộc': {
            'tinh_chat': 'Mềm dẻo, sinh trưởng, phát triển',
            'mau_sac': 'Xanh lá, xanh lục',
            'huong': 'Đông',
            'mua': 'Xuân',
            'categories': list(NGU_HANH_VAN_VAT.get('Mộc', {}).keys()) if NGU_HANH_VAN_VAT else [],
            'mo_rong': list(VAN_VAT_MO_RONG.get('Mộc', {}).keys()) if VAN_VAT_MO_RONG else [],
            'bo_sung': list(VAN_VAT_BO_SUNG.get('Mộc', {}).keys()) if VAN_VAT_BO_SUNG else [],
        },
        'Thủy': {
            'tinh_chat': 'Lỏng, chảy, thấm, trí tuệ',
            'mau_sac': 'Đen, xanh đậm',
            'huong': 'Bắc',
            'mua': 'Đông',
            'categories': list(NGU_HANH_VAN_VAT.get('Thủy', {}).keys()) if NGU_HANH_VAN_VAT else [],
            'mo_rong': list(VAN_VAT_MO_RONG.get('Thủy', {}).keys()) if VAN_VAT_MO_RONG else [],
            'bo_sung': list(VAN_VAT_BO_SUNG.get('Thủy', {}).keys()) if VAN_VAT_BO_SUNG else [],
        },
        'Hỏa': {
            'tinh_chat': 'Nóng, bốc lên, sáng, phô trương',
            'mau_sac': 'Đỏ, cam, hồng',
            'huong': 'Nam',
            'mua': 'Hạ',
            'categories': list(NGU_HANH_VAN_VAT.get('Hỏa', {}).keys()) if NGU_HANH_VAN_VAT else [],
            'mo_rong': list(VAN_VAT_MO_RONG.get('Hỏa', {}).keys()) if VAN_VAT_MO_RONG else [],
            'bo_sung': list(VAN_VAT_BO_SUNG.get('Hỏa', {}).keys()) if VAN_VAT_BO_SUNG else [],
        },
        'Thổ': {
            'tinh_chat': 'Dày, ổn định, chứa đựng, trung tâm',
            'mau_sac': 'Vàng, nâu',
            'huong': 'Trung tâm',
            'mua': 'Tứ quý (cuối mỗi mùa)',
            'categories': list(NGU_HANH_VAN_VAT.get('Thổ', {}).keys()) if NGU_HANH_VAN_VAT else [],
            'mo_rong': list(VAN_VAT_MO_RONG.get('Thổ', {}).keys()) if VAN_VAT_MO_RONG else [],
            'bo_sung': list(VAN_VAT_BO_SUNG.get('Thổ', {}).keys()) if VAN_VAT_BO_SUNG else [],
        },
    },

    # ═══ TẦNG 2: TRƯỜNG SINH → TRẠNG THÁI VẬT CHẤT ═══
    'truong_sinh': {
        'Trường Sinh': {'power': 85, 'chat_luong': 'Mới tinh, vừa xuất hiện',    'so': [1]},
        'Mộc Dục':     {'power': 40, 'chat_luong': 'Đang sửa chữa, không ổn định','so': [2]},
        'Quan Đới':    {'power': 70, 'chat_luong': 'Đã hoàn thiện, sẵn sàng dùng','so': [3]},
        'Lâm Quan':    {'power': 90, 'chat_luong': 'Chất lượng cao, đang phát triển','so': [4,5]},
        'Đế Vượng':    {'power': 100,'chat_luong': 'CỰC TỐT, đỉnh cao chất lượng','so': [5,6]},
        'Suy':         {'power': 45, 'chat_luong': 'Bắt đầu xuống cấp, cũ dần',   'so': [6,7]},
        'Bệnh':        {'power': 30, 'chat_luong': 'Hỏng hóc, lỗi, cần sửa',      'so': [7,8]},
        'Tử':          {'power': 15, 'chat_luong': 'Hư nặng, gần hỏng hoàn toàn',  'so': [8,9]},
        'Mộ':          {'power': 20, 'chat_luong': 'Cất kho, không dùng, phong ấn', 'so': [9]},
        'Tuyệt':       {'power': 5,  'chat_luong': 'Mất hoàn toàn, tiêu hủy',      'so': [0]},
        'Thai':         {'power': 50, 'chat_luong': 'Chưa ra đời, đang thai nghén', 'so': [10]},
        'Dưỡng':       {'power': 60, 'chat_luong': 'Đang nuôi dưỡng, chuẩn bị ra', 'so': [11,12]},
    },

    # ═══ TẦNG 3: SUY VƯỢNG → ĐỘ MẠNH YẾU ═══
    'suy_vuong': {
        'Vượng':  {'power': 100, 'desc': 'Cực mạnh — đúng mùa, được sinh'},
        'Tướng':  {'power': 80,  'desc': 'Mạnh — sắp đến mùa, có lực'},
        'Hưu':    {'power': 50,  'desc': 'Trung bình — qua mùa, nghỉ ngơi'},
        'Tù':     {'power': 30,  'desc': 'Yếu — bị khắc, mất lực'},
        'Tuyệt':  {'power': 10,  'desc': 'Cực yếu — hoàn toàn bất lực'},
    },

    # ═══ BẢNG TRA NHANH: HÀNH → THÁNG → VƯỢNG/SUY ═══
    'hanh_thang_map': {
        # Hành: {tháng_chi: trạng_thái}
        'Kim': {'Thân': 'Vượng', 'Dậu': 'Vượng', 'Mùi': 'Tướng', 'Tuất': 'Tướng',
                'Hợi': 'Hưu', 'Tý': 'Hưu', 'Dần': 'Tù', 'Mão': 'Tù',
                'Tị': 'Tuyệt', 'Ngọ': 'Tuyệt', 'Thìn': 'Hưu', 'Sửu': 'Tướng'},
        'Mộc': {'Dần': 'Vượng', 'Mão': 'Vượng', 'Hợi': 'Tướng', 'Tý': 'Tướng',
                'Tị': 'Hưu', 'Ngọ': 'Hưu', 'Thân': 'Tù', 'Dậu': 'Tù',
                'Sửu': 'Tuyệt', 'Mùi': 'Tuyệt', 'Thìn': 'Hưu', 'Tuất': 'Hưu'},
        'Thủy': {'Hợi': 'Vượng', 'Tý': 'Vượng', 'Thân': 'Tướng', 'Dậu': 'Tướng',
                 'Dần': 'Hưu', 'Mão': 'Hưu', 'Tị': 'Tù', 'Ngọ': 'Tù',
                 'Thìn': 'Tuyệt', 'Tuất': 'Tuyệt', 'Sửu': 'Hưu', 'Mùi': 'Hưu'},
        'Hỏa': {'Tị': 'Vượng', 'Ngọ': 'Vượng', 'Dần': 'Tướng', 'Mão': 'Tướng',
                 'Thân': 'Hưu', 'Dậu': 'Hưu', 'Hợi': 'Tù', 'Tý': 'Tù',
                 'Mùi': 'Tuyệt', 'Sửu': 'Tuyệt', 'Thìn': 'Hưu', 'Tuất': 'Hưu'},
        'Thổ': {'Thìn': 'Vượng', 'Tuất': 'Vượng', 'Sửu': 'Vượng', 'Mùi': 'Vượng',
                'Tị': 'Tướng', 'Ngọ': 'Tướng', 'Thân': 'Hưu', 'Dậu': 'Hưu',
                'Hợi': 'Tù', 'Tý': 'Tù', 'Dần': 'Tuyệt', 'Mão': 'Tuyệt'},
    },

    # ═══ REFERENCES — trỏ về data thực ═══
    'data_source': {
        'ngu_hanh_van_vat': 'van_vat_tong_hop.NGU_HANH_VAN_VAT',
        'van_vat_mo_rong': 'van_vat_tong_hop.VAN_VAT_MO_RONG',
        'van_vat_bo_sung': 'van_vat_tong_hop.VAN_VAT_BO_SUNG',
        'truong_sinh_trang_thai': 'van_vat_tong_hop.TRUONG_SINH_TRANG_THAI',
    },
}


def lookup_van_vat(hanh, category=None):
    """Tra cứu nhanh Vạn Vật theo hành và danh mục
    
    Usage:
        lookup_van_vat('Kim')           → tất cả categories của Kim
        lookup_van_vat('Kim', 'do_vat') → đồ vật thuộc Kim
    """
    result = {}
    if hanh in NGU_HANH_VAN_VAT:
        data = NGU_HANH_VAN_VAT[hanh]
        if category:
            return data.get(category, f"Không tìm thấy '{category}' trong hành {hanh}")
        result['co_ban'] = list(data.keys())
    if hanh in VAN_VAT_MO_RONG:
        if category:
            return VAN_VAT_MO_RONG[hanh].get(category, '')
        result['mo_rong'] = list(VAN_VAT_MO_RONG[hanh].keys())
    if hanh in VAN_VAT_BO_SUNG:
        if category:
            return VAN_VAT_BO_SUNG[hanh].get(category, '')
        result['bo_sung'] = list(VAN_VAT_BO_SUNG[hanh].keys())
    return result


def get_truong_sinh_state(stage):
    """Lấy trạng thái vật chất theo giai đoạn Trường Sinh
    
    Usage:
        get_truong_sinh_state('Đế Vượng') → {'power': 100, 'chat_luong': 'CỰC TỐT...'}
    """
    return VV_TREE['truong_sinh'].get(stage, {})


def get_suy_vuong(hanh, chi_thang):
    """Tra Vượng/Suy của 1 hành trong 1 tháng
    
    Usage:
        get_suy_vuong('Kim', 'Thân') → 'Vượng'
        get_suy_vuong('Mộc', 'Dậu') → 'Tù'
    """
    return VV_TREE['hanh_thang_map'].get(hanh, {}).get(chi_thang, 'Hưu')


# ═══ MASTER TREE — Entry Point ═══
TREE = {
    'LH': LH_TREE,
    'KM': KM_TREE,
    'MH': MH_TREE,
    'LN': LN_TREE,
    'TA': TA_TREE,
    'TB': TB_TREE,
    'TV': TV_TREE,
    'XND': XND_TREE,
    'VV': VV_TREE,  # Vạn Vật
}


def audit_tree():
    """Tự kiểm tra độ phủ của Knowledge Tree"""
    print("═══ AUDIT KNOWLEDGE TREE ═══")
    total_items = 0
    for code, tree in TREE.items():
        name = tree.get('name', '?')
        coverage = tree.get('coverage', tree.get('total_items', '?'))
        factors = len(tree.get('factors', {}))
        # Count VV items
        if code == 'VV':
            _vv_count = 0
            for h, hdata in tree.get('ngu_hanh', {}).items():
                _vv_count += len(hdata.get('categories', []))
                _vv_count += len(hdata.get('mo_rong', []))
                _vv_count += len(hdata.get('bo_sung', []))
            factors = _vv_count
        total_items += factors
        print(f"  [{code}] {name}: {coverage} | {factors} items")
    print(f"\n  TOTAL: {total_items} items in tree")
    print(f"  VV imported: {_VV_IMPORTED}")


if __name__ == '__main__':
    audit_tree()
    print("\n═══ TEST LOOKUP ═══")
    print(f"  Kim categories: {lookup_van_vat('Kim')}")
    print(f"  Đế Vượng state: {get_truong_sinh_state('Đế Vượng')}")
    print(f"  Kim tháng Thân: {get_suy_vuong('Kim', 'Thân')}")
    print(f"  Mộc tháng Dậu: {get_suy_vuong('Mộc', 'Dậu')}")

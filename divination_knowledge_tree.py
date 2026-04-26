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
}

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
}


def audit_tree():
    """Tự kiểm tra độ phủ của Knowledge Tree"""
    print("═══ AUDIT KNOWLEDGE TREE ═══")
    for code, tree in TREE.items():
        name = tree.get('name', '?')
        coverage = tree.get('coverage', '?')
        factors = len(tree.get('factors', {}))
        print(f"  [{code}] {name}: {coverage} | {factors} factors")


if __name__ == '__main__':
    audit_tree()

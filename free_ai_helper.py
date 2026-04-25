"""
Free AI Helper V42.9 — THIÊN CƠ ĐẠI SƯ (Siêu Premium UI + Answer-First + Vạn Vật 3378+ + 12 Trường Sinh)
Kết hợp Python rule-based + Gemini Online Deep Reasoning.
Sử dụng dữ liệu Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản + Đại Lục Nhâm + Thái Ất Thần Số.
V42.2: +7 thiếu sót chuyên gia (Ứng Kỳ chuyên sâu, Hóa Hồi Đầu, Hào Từ, Phản/Phục Ngâm,
       Ám Động, Lục Thần sâu, Bảng Vượng/Suy theo mùa).
V26.2: Tích hợp _calc_unified_strength_tier() — 3 tầng LH+TS+NK → Unified %.
       Ngũ Hành vật chất mapping (hình, chất liệu, màu sắc).
       Kế thừa V21.0: Lượng Hóa Suy Vượng, Tiến/Thối Thần, Nguyệt Phá.
       Kế thừa V15.0: XÂU DƯỢC + NỘI CUNG (7 tầng).
       Kế thừa V14.0: LỤC THUẬT HỢP NHẤT + Deep Reasoning.
"""

import random
import re
import json
import os
import datetime
try:
    from qmdg_data import KY_MON_DATA, QUAI_TUONG, CUNG_NGU_HANH, BAT_MON_CO_DINH_DISPLAY
    TOPIC_INTERPRETATIONS = KY_MON_DATA.get("TOPIC_INTERPRETATIONS", {})
except ImportError:
    KY_MON_DATA = {"DU_LIEU_DUNG_THAN_PHU_TRO": {"CUU_TINH": {}, "BAT_MON": {}, "BAT_THAN": {}}, "TRUCTU_TRANH": {}}
    QUAI_TUONG = {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 5: "Trung", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}
    CUNG_NGU_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
    BAT_MON_CO_DINH_DISPLAY = {}
    TOPIC_INTERPRETATIONS = {}

# Vạn Vật Loại Tượng
try:
    from van_vat_loai_tuong import BAT_QUAI_LOAI_TUONG, KINH_DICH_MAI_HOA_THIET_BAN, get_ngu_hanh_tuong, get_bat_quai_tuong
except ImportError:
    BAT_QUAI_LOAI_TUONG = {"rows": []}
    KINH_DICH_MAI_HOA_THIET_BAN = {"kinh_dich": {"data": []}, "thiet_ban": {"nap_am_table": []}}
    def get_ngu_hanh_tuong(h): return ""
    def get_bat_quai_tuong(q): return ""

# V9.0: Knowledge Base mở rộng
try:
    from kinh_dich_64_que import KINH_DICH_64, MAI_HOA_THE_DUNG, MAI_HOA_UNG_KY, THIET_BAN_60, tra_kinh_dich, tra_nap_am, tra_the_dung
except ImportError:
    KINH_DICH_64 = {}
    MAI_HOA_THE_DUNG = {}
    MAI_HOA_UNG_KY = {}
    THIET_BAN_60 = {}
    def tra_kinh_dich(t): return None
    def tra_nap_am(t): return None
    def tra_the_dung(a, b): return None

try:
    from luc_hao_ky_mon_rules import (
        DUNG_THAN_MAP, NGUYEN_KY_CUU, LUC_HAO_RULES, LUC_THAN_Y_NGHIA,
        KY_MON_CACH_CUC, SAO_KY_MON, CUA_KY_MON, THAN_KY_MON,
        PHUC_THAN_RULES, NHAT_NGUYET_RULES, KY_MON_CACH_CUC_MR,
        SAO_CUA_TO_HOP, BAN_CUNG, tra_ban_cung,
        HAO_BIEN_RULES, DONG_TINH_RULES, SAO_CUA_TO_HOP_BS,
        THAP_CAN_KHAC_UNG, BAT_MON_BAY_CUNG, CAN_CHI_TUONG_Y, THAP_NHI_THAN_UNG_NGHIEM
    )
except ImportError:
    DUNG_THAN_MAP = {}
    NGUYEN_KY_CUU = {}
    LUC_HAO_RULES = []
    LUC_THAN_Y_NGHIA = {}
    KY_MON_CACH_CUC = {}
    SAO_KY_MON = {}
    CUA_KY_MON = {}
    THAN_KY_MON = {}
    PHUC_THAN_RULES = {}
    NHAT_NGUYET_RULES = []
    KY_MON_CACH_CUC_MR = {}
    SAO_CUA_TO_HOP = {}
    BAN_CUNG = {}
    HAO_BIEN_RULES = []
    DONG_TINH_RULES = []
    SAO_CUA_TO_HOP_BS = {}
    THAP_CAN_KHAC_UNG = {}
    BAT_MON_BAY_CUNG = {}
    CAN_CHI_TUONG_Y = {}
    THAP_NHI_THAN_UNG_NGHIEM = {}
    def tra_ban_cung(t): return None, None
    def get_ngu_hanh_tuong(h): return ""
    def get_bat_quai_tuong(q): return ""

# Lục Hào Kinh Dịch
try:
    from luc_hao_kinh_dich import HEXAGRAM_PALACES, HEXAGRAM_NAMES, THE_POSITION
except ImportError:
    HEXAGRAM_PALACES = {}
    HEXAGRAM_NAMES = {}
    THE_POSITION = {}

# V10.1: Knowledge Complete — Tri thức siêu chi tiết
try:
    from qmdg_knowledge_complete import (
        CUU_CUNG, CUU_TINH, BAT_MON as BAT_MON_KB, BAT_THAN as BAT_THAN_KB,
        THAP_THIEN_CAN, tra_cuu_cung, tra_cuu_sao, tra_cuu_mon, tra_cuu_than, tra_cuu_can,
        xac_dinh_huong_khoang_cach, kha_nang_tim_duoc
    )
except ImportError:
    CUU_CUNG = {}
    CUU_TINH = {}
    BAT_MON_KB = {}
    BAT_THAN_KB = {}
    THAP_THIEN_CAN = {}
    def tra_cuu_cung(c): return {}
    def tra_cuu_sao(s): return {}
    def tra_cuu_mon(m): return {}
    def tra_cuu_than(t): return {}
    def tra_cuu_can(c): return {}
    def xac_dinh_huong_khoang_cach(c): return {}
    def kha_nang_tim_duoc(m): return ""

# V31.0: Interaction Diagrams — Sơ đồ tương tác thời gian thực
try:
    from interaction_diagrams import (
        DIAGRAM_MASTER, DIAGRAMS as INTERACTION_DIAGRAMS, 
        match_question_to_diagram, CUNG_PHUONG, QUAI_NGUOI, KY_THAN_NGUYEN_NHAN,
        clean_question,
    )
except ImportError:
    DIAGRAM_MASTER = None
    INTERACTION_DIAGRAMS = {}
    def match_question_to_diagram(q): return 'SD0', {}
    CUNG_PHUONG = {}
    QUAI_NGUOI = {}
    KY_THAN_NGUYEN_NHAN = {}
    def clean_question(q): return q.strip() if q else ""

# V32.5: Smart Question Parser — Grammar-based DT determination
try:
    from question_parser import (
        parse_question as v32_parse_question,
        format_parsed_questions_v2,
        analyze_question,
    )
except ImportError:
    def v32_parse_question(q): return []
    def format_parsed_questions_v2(lst): return ""
    def analyze_question(q): return None

# V32.0: Vạn Vật Lazy-Load Package — AI chỉ load hành cần thiết
try:
    from van_vat import get_van_vat_chi_tiet, format_van_vat_for_ai, get_tham_tu_mo_ta
    from van_vat import smart_van_vat_for_question
except ImportError:
    try:
        from van_vat_tong_hop import (
            get_van_vat_chi_tiet, format_van_vat_for_ai, get_tham_tu_mo_ta,
            smart_van_vat_for_question,
        )
    except ImportError:
        try:
            from van_vat_tong_hop import (
                get_van_vat_chi_tiet, format_van_vat_for_ai, get_tham_tu_mo_ta,
                smart_van_vat_for_question,
            )
        except ImportError:
            def get_van_vat_chi_tiet(h, ts): return {}
            def format_van_vat_for_ai(h, ts): return ""
            def get_tham_tu_mo_ta(h, ts, q=""): return ""
            def smart_van_vat_for_question(h, ts, q=""): return ("", ['full'])

# === NGŨ HÀNH ENGINE ===
SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
KHAC = {'Mộc': 'Thổ', 'Hỏa': 'Kim', 'Thổ': 'Thủy', 'Kim': 'Mộc', 'Thủy': 'Hỏa'}
CAN_NGU_HANH = {'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa', 'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim', 'Nhâm': 'Thủy', 'Quý': 'Thủy'}
CHI_NGU_HANH = {'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc', 'Thìn': 'Thổ', 'Tị': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ', 'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'}
TIEN_THIEN = {'Càn': 1, 'Đoài': 2, 'Ly': 3, 'Chấn': 4, 'Tốn': 5, 'Khảm': 6, 'Cấn': 7, 'Khôn': 8}
SAO_CAT = ['Thiên Tâm', 'Thiên Nhậm', 'Thiên Phụ', 'Thiên Xung']
SAO_HUNG = ['Thiên Bồng', 'Thiên Nhuế', 'Thiên Trụ', 'Thiên Anh', 'Thiên Cầm']
CUA_CAT = ['Hưu', 'Sinh', 'Khai']
CUA_HUNG = ['Tử', 'Kinh', 'Thương']

# Bảng Dụng Thần — V34.1 CHUẨN THEO VẠN VẬT LOẠI TƯỢNG (6 nguồn uy tín)
# Nguồn: kinhdichluchao.vn, tusachxua.com, tuviglobal.com, zhycw.com, yixiangqiankun.com
DUNG_THAN_MAP = {
    # ═══ PRIORITY 0: Cụm từ dài nhất (edge cases) ═══
    'bố tôi': 'Phụ Mẫu', 'mẹ tôi': 'Phụ Mẫu', 'cha tôi': 'Phụ Mẫu',
    'bố mình': 'Phụ Mẫu', 'mẹ mình': 'Phụ Mẫu',
    'mẹ bệnh': 'Phụ Mẫu', 'bố bệnh': 'Phụ Mẫu', 'mẹ ốm': 'Phụ Mẫu',
    'chồng có ngoại tình': 'Quan Quỷ', 'chồng ngoại tình': 'Quan Quỷ',
    'chồng có': 'Quan Quỷ', 'chồng bệnh': 'Quan Quỷ', 'chồng đi': 'Quan Quỷ',
    'chó nhà': 'Tử Tôn', 'chó mèo': 'Tử Tôn', 'con chó': 'Tử Tôn', 'con mèo': 'Tử Tôn',
    
    # ═══ PRIORITY 1: Cụm từ dài (match trước — longest first) ═══
    # --- Phụ Mẫu: Che chở, văn thư, phương tiện, trang phục, bề trên ---
    'bất động sản': 'Phụ Mẫu', 'nhà đất': 'Phụ Mẫu', 'căn hộ': 'Phụ Mẫu',
    'chung cư': 'Phụ Mẫu', 'mua nhà': 'Phụ Mẫu', 'bán nhà': 'Phụ Mẫu',
    'xây nhà': 'Phụ Mẫu', 'sửa nhà': 'Phụ Mẫu', 'thuê nhà': 'Phụ Mẫu',
    'mua xe': 'Phụ Mẫu', 'bán xe': 'Phụ Mẫu', 'mua đất': 'Phụ Mẫu',
    'hợp đồng': 'Phụ Mẫu', 'văn bằng': 'Phụ Mẫu', 'bằng cấp': 'Phụ Mẫu',
    'giấy phép': 'Phụ Mẫu', 'bằng lái': 'Phụ Mẫu', 'giấy tờ': 'Phụ Mẫu',
    'hộ chiếu': 'Phụ Mẫu', 'thẻ căn cước': 'Phụ Mẫu',
    'quần áo': 'Phụ Mẫu', 'trang phục': 'Phụ Mẫu', 'giày dép': 'Phụ Mẫu',
    'mũ nón': 'Phụ Mẫu', 'ô dù': 'Phụ Mẫu',
    'sách vở': 'Phụ Mẫu', 'văn bản': 'Phụ Mẫu',
    'máy bay': 'Phụ Mẫu', 'tàu hỏa': 'Phụ Mẫu',
    'mồ mả': 'Phụ Mẫu', 'tổ tiên': 'Phụ Mẫu', 'phong thủy': 'Phụ Mẫu',
    'bảo hiểm': 'Phụ Mẫu',
    'bố mẹ': 'Phụ Mẫu', 'cha mẹ': 'Phụ Mẫu',
    'bà ngoại': 'Phụ Mẫu', 'bà nội': 'Phụ Mẫu',
    'ông ngoại': 'Phụ Mẫu', 'ông nội': 'Phụ Mẫu',
    # --- Thê Tài: Tiền bạc, tài sản, hàng hóa, lương thực ---
    'ngoại tình': 'Thê Tài', 'đầu tư': 'Thê Tài',
    'cổ phiếu': 'Thê Tài', 'chứng khoán': 'Thê Tài',
    'mất đồ': 'Thê Tài', 'mất tiền': 'Thê Tài', 'mất điện thoại': 'Thê Tài',
    'tăng lương': 'Thê Tài', 'thu nhập': 'Thê Tài',
    'người yêu': 'Thê Tài', 'bạn trai': 'Thê Tài', 'bạn gái': 'Thê Tài',
    'hàng hóa': 'Thê Tài', 'kho hàng': 'Thê Tài', 'cửa hàng': 'Thê Tài',
    'kim cương': 'Thê Tài', 'trang sức': 'Thê Tài',
    'điện thoại': 'Thê Tài', 'laptop': 'Thê Tài',
    'lương thực': 'Thê Tài', 'thức ăn': 'Thê Tài',
    # --- Quan Quỷ: Công danh, bệnh tật, tai họa, pháp luật ---
    'thăng chức': 'Quan Quỷ', 'xin việc': 'Quan Quỷ',
    'đối tác': 'Quan Quỷ', 'khách hàng': 'Quan Quỷ',
    'ung thư': 'Quan Quỷ', 'tai nạn': 'Quan Quỷ',
    'kiện tụng': 'Quan Quỷ', 'kiện cáo': 'Quan Quỷ',
    'công chức': 'Quan Quỷ', 'công an': 'Quan Quỷ', 'quân đội': 'Quan Quỷ',
    'trầm cảm': 'Quan Quỷ', 'lo âu': 'Quan Quỷ',
    'hỏa hoạn': 'Quan Quỷ', 'lũ lụt': 'Quan Quỷ', 'động đất': 'Quan Quỷ',
    # --- Tử Tôn: Con cái, thuốc men, vật nuôi, giải trí ---
    'con trai': 'Tử Tôn', 'con gái': 'Tử Tôn', 'con dâu': 'Tử Tôn',
    'con rể': 'Tử Tôn', 'con cái': 'Tử Tôn',
    'bác sĩ': 'Tử Tôn', 'bệnh viện': 'Tử Tôn',
    'vật nuôi': 'Tử Tôn', 'thú cưng': 'Tử Tôn',
    'du lịch': 'Tử Tôn', 'giải trí': 'Tử Tôn',
    'tu hành': 'Tử Tôn', 'nhà sư': 'Tử Tôn',
    'bình an': 'Tử Tôn',
    # --- Huynh Đệ: Ngang hàng, cạnh tranh, cờ bạc ---
    'anh chị em': 'Huynh Đệ', 'anh em': 'Huynh Đệ',
    'đối thủ': 'Huynh Đệ', 'đối thủ cạnh tranh': 'Huynh Đệ',
    'cờ bạc': 'Huynh Đệ', 'đánh bạc': 'Huynh Đệ', 'xổ số': 'Huynh Đệ',
    'đồng nghiệp': 'Huynh Đệ',

    # ═══ PRIORITY 2: Từ đơn — Chủ đề ═══
    # --- Phụ Mẫu: nhà, xe, học, giấy, đất, sách, thuyền ---
    'nhà': 'Phụ Mẫu', 'xe': 'Phụ Mẫu', 'học': 'Phụ Mẫu',
    'giấy': 'Phụ Mẫu', 'đất': 'Phụ Mẫu', 'sách': 'Phụ Mẫu',
    'thi': 'Phụ Mẫu', 'trường': 'Phụ Mẫu',
    'thuyền': 'Phụ Mẫu', 'tàu': 'Phụ Mẫu',
    'áo': 'Phụ Mẫu', 'mộ': 'Phụ Mẫu', 'cúng': 'Phụ Mẫu',
    'passport': 'Phụ Mẫu', 'visa': 'Phụ Mẫu',
    # --- Thê Tài: tiền, tài, vốn, mua, bán ---
    'tiền': 'Thê Tài', 'tài': 'Thê Tài', 'lương': 'Thê Tài', 'vốn': 'Thê Tài',
    'lãi': 'Thê Tài', 'nợ': 'Thê Tài', 'lời': 'Thê Tài', 'lỗ': 'Thê Tài',
    'mua': 'Thê Tài', 'bán': 'Thê Tài',
    'mất': 'Thê Tài', 'trộm': 'Thê Tài', 'cắp': 'Thê Tài',
    'vàng': 'Thê Tài', 'crypto': 'Thê Tài', 'coin': 'Thê Tài',
    # --- Quan Quỷ: việc, sếp, bệnh, kiện, stress ---
    'việc': 'Quan Quỷ', 'sếp': 'Quan Quỷ', 'bệnh': 'Quan Quỷ',
    'kiện': 'Quan Quỷ', 'ốm': 'Quan Quỷ', 'đau': 'Quan Quỷ',
    'stress': 'Quan Quỷ', 'cháy': 'Quan Quỷ',
    # --- Tử Tôn: thuốc, chó, mèo, vui ---
    'thuốc': 'Tử Tôn', 'chó': 'Tử Tôn', 'mèo': 'Tử Tôn',
    'vui': 'Tử Tôn', 'chơi': 'Tử Tôn',

    # ═══ PRIORITY 3: Từ đơn — Người thân ═══
    'vợ': 'Thê Tài',
    'chồng': 'Quan Quỷ',  # V34.1: Nữ hỏi chồng → Quan Quỷ (khắc ta)
    'con': 'Tử Tôn', 'cháu': 'Tử Tôn',
    'bố': 'Phụ Mẫu', 'mẹ': 'Phụ Mẫu', 'cha': 'Phụ Mẫu',
    'bạn': 'Huynh Đệ', 'anh': 'Huynh Đệ', 'chị': 'Huynh Đệ', 'em': 'Huynh Đệ',

    # ═══ PRIORITY 4: Bản thân (match cuối) ═══
    'tuổi': 'Bản Thân', 'tôi': 'Bản Thân', 'mình': 'Bản Thân',
}

# V34.0: Priority-sorted keywords — dài trước ngắn, tránh "tôi" override "vợ tôi"
_DUNG_THAN_SORTED = sorted(DUNG_THAN_MAP.keys(), key=len, reverse=True)

# === V12.0: LỤC THÂN RELATIONSHIP ENGINE ===
# Mỗi thành viên gia đình/xã hội → Lục Thân + Can tương ứng trong Kỳ Môn
# Dùng để so sánh ai GIÚP / ai HẠI Dụng Thần
LUC_THAN_MEMBERS = {
    'Bản Thân': {'luc_than': 'Huynh Đệ', 'km_can': 'can_ngay',
                 'mota': 'Người hỏi (mình)', 'icon': '🧑'},
    'Bố/Mẹ': {'luc_than': 'Phụ Mẫu', 'km_can': 'can_nam',
              'mota': 'Cha mẹ, người bề trên, nhà cửa, xe cộ', 'icon': '👨‍👩'},
    'Anh Chị Em': {'luc_than': 'Huynh Đệ', 'km_can': 'can_thang',
                   'mota': 'Anh em, bạn bè, đối thủ cạnh tranh', 'icon': '👫'},
    'Vợ/Chồng': {'luc_than': 'Thê Tài', 'km_can': 'can_gio',
                 'mota': 'Vợ/chồng, tiền bạc, tài sản', 'icon': '💑'},
    'Con Cái': {'luc_than': 'Tử Tôn', 'km_can': 'can_gio',
                'mota': 'Con cái, niềm vui, phúc đức, giải trừ', 'icon': '👶'},
    'Sếp/Quan': {'luc_than': 'Quan Quỷ', 'km_can': 'can_gio',
                 'mota': 'Sếp, cơ quan, bệnh tật, áp lực, kiện tụng', 'icon': '👔'},
    'Người Lạ': {'luc_than': 'Ứng', 'km_can': 'can_gio',
                 'mota': 'Đối phương, khách hàng, người ngoài', 'icon': '🤝'},
}

# V12.0: Bảng Ngũ Hành sinh Lục Thân từ Hành của Bản Thân
# Nếu hành BT = X thì: Tỷ Hòa = Huynh Đệ, X sinh = Tử Tôn, X khắc = Thê Tài,
# Sinh X = Phụ Mẫu, Khắc X = Quan Quỷ
LUC_THAN_NGU_HANH_MAP = {
    'Huynh Đệ': 'tỷ_hòa',    # Cùng hành với BT
    'Tử Tôn': 'bt_sinh',      # BT sinh ra nó
    'Thê Tài': 'bt_khắc',     # BT khắc nó
    'Phụ Mẫu': 'sinh_bt',     # Nó sinh BT
    'Quan Quỷ': 'khắc_bt',    # Nó khắc BT
}

def _get_hanh_dt_from_luc_hao(luc_hao_data, dung_than):
    """Lấy Ngũ Hành CHUẨN của Dụng Thần từ dữ liệu Lục Hào (theo Cung Quẻ)"""
    if not luc_hao_data or not isinstance(luc_hao_data, dict):
        return None
    ban = luc_hao_data.get('ban', {})
    haos = ban.get('haos', []) or ban.get('details', [])
    for hao in haos:
        if dung_than in hao.get('luc_than', ''):
            return hao.get('ngu_hanh')
    phuc_than = luc_hao_data.get('phuc_than')
    if phuc_than and isinstance(phuc_than, list):
        for pt in phuc_than:
            if dung_than in pt.get('luc_than', ''):
                return pt.get('element') or pt.get('ngu_hanh')
    return None

def _get_luc_than_hanh(bt_hanh, luc_than_name):
    """V12.0: Tính Ngũ Hành của Lục Thân dựa trên hành Bản Thân"""
    if not bt_hanh or bt_hanh == '?':
        return '?'
    role = LUC_THAN_NGU_HANH_MAP.get(luc_than_name)
    if not role:
        return '?'
    if role == 'tỷ_hòa':
        return bt_hanh
    elif role == 'bt_sinh':
        return SINH.get(bt_hanh, '?')
    elif role == 'bt_khắc':
        return KHAC.get(bt_hanh, '?')
    elif role == 'sinh_bt':
        # Tìm hành nào sinh ra bt_hanh
        for h, s in SINH.items():
            if s == bt_hanh:
                return h
        return '?'
    elif role == 'khắc_bt':
        # Tìm hành nào khắc bt_hanh
        for h, k in KHAC.items():
            if k == bt_hanh:
                return h
        return '?'
    return '?'

# === SYNONYM MAP (V7.0) — Từ đồng nghĩa để tăng matching ===
SYNONYM_MAP = {
    # Vietnamese synonyms
    'lương': ['tiền', 'thu nhập'], 'crypto': ['bitcoin', 'coin', 'tiền điện tử'],
    'bitcoin': ['crypto', 'coin'], 'chung cư': ['căn hộ'],
    'nợ': ['vay', 'đòi'], 'thất nghiệp': ['mất việc', 'sa thải'],
    'giấc mơ': ['mộng', 'nằm mơ'], 'cúng': ['lễ', 'cầu'],
    'phẫu thuật': ['mổ'], 'trầm cảm': ['stress', 'lo âu'],
    'bảo hiểm': ['insurance'], 'ngân hàng': ['bank', 'vay'],
    'startup': ['khởi nghiệp'], 'freelance': ['tự do'],
    'youtube': ['youtuber', 'kênh'], 'tiktok': ['livestream', 'bán hàng'],
    # V41.0: English → Vietnamese (expanded)
    'job': ['việc', 'công việc', 'nghề'], 'work': ['việc', 'làm'],
    'career': ['sự nghiệp', 'công việc'], 'promotion': ['thăng chức', 'lên chức'],
    'salary': ['lương', 'thu nhập'], 'boss': ['sếp', 'chủ'],
    'love': ['yêu', 'tình', 'tình cảm'], 'crush': ['thích', 'yêu'],
    'relationship': ['quan hệ', 'tình cảm'], 'boyfriend': ['bạn trai', 'người yêu'],
    'girlfriend': ['bạn gái', 'người yêu'], 'husband': ['chồng'],
    'wife': ['vợ'], 'wedding': ['cưới', 'kết hôn'],
    'sick': ['bệnh', 'ốm'], 'health': ['sức khỏe', 'khỏe'],
    'hospital': ['bệnh viện', 'viện'], 'doctor': ['bác sĩ'],
    'cancer': ['ung thư'], 'surgery': ['mổ', 'phẫu thuật'],
    'medicine': ['thuốc'], 'pregnant': ['mang thai', 'có bầu'],
    'house': ['nhà'], 'apartment': ['căn hộ', 'chung cư'],
    'car': ['xe', 'ô tô'], 'phone': ['điện thoại'],
    'exam': ['thi', 'kiểm tra'], 'school': ['trường', 'học'],
    'university': ['đại học', 'trường'], 'study': ['học', 'thi'],
    'marry': ['cưới', 'hôn nhân', 'kết hôn'],
    'divorce': ['ly hôn', 'chia tay'], 'breakup': ['chia tay'],
    'invest': ['đầu tư'], 'investment': ['đầu tư'],
    'stock': ['chứng khoán', 'cổ phiếu'], 'trading': ['giao dịch'],
    'money': ['tiền', 'tài chính'], 'rich': ['giàu', 'tiền'],
    'travel': ['du lịch', 'đi chơi'], 'trip': ['chuyến đi', 'du lịch'],
    'business': ['kinh doanh', 'buôn bán'], 'company': ['công ty'],
    'death': ['chết', 'mất'], 'accident': ['tai nạn'],
    'lawsuit': ['kiện', 'kiện tụng'], 'court': ['tòa', 'kiện'],
    'lost': ['mất', 'thất lạc'], 'find': ['tìm', 'kiếm'],
    'steal': ['trộm', 'cắp'], 'thief': ['kẻ trộm', 'trộm'],
    'lucky': ['may mắn', 'hên'], 'unlucky': ['xui', 'xui xẻo'],
    'success': ['thành công', 'đạt'], 'fail': ['thất bại', 'trượt'],
    'should': ['có nên', 'nên'], 'when': ['khi nào', 'bao giờ'],
    'where': ['ở đâu', 'hướng nào'], 'how': ['như thế nào', 'ra sao'],
    'gamble': ['cờ bạc', 'đánh bạc'], 'lottery': ['xổ số', 'lô đề'],
    'child': ['con', 'con cái'], 'baby': ['em bé', 'con'],
    'parent': ['bố mẹ', 'cha mẹ'], 'father': ['bố', 'cha'],
    'mother': ['mẹ', 'má'], 'pet': ['thú cưng', 'vật nuôi'],
    'dog': ['chó'], 'cat': ['mèo'],
    'land': ['đất', 'bất động sản'], 'gold': ['vàng'],
    'debt': ['nợ', 'vay'], 'loan': ['vay', 'nợ'],
}

# === AUTO-LEARN FILE (V7.0) ===
LEARNED_TOPICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'learned_topics.json')

def _load_learned_topics():
    """Load câu hỏi đã học từ file JSON"""
    if os.path.exists(LEARNED_TOPICS_FILE):
        try:
            with open(LEARNED_TOPICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def _save_learned_topic(question, category, dung_than_list, goi_y):
    """Lưu câu hỏi mới vào file learned_topics.json"""
    learned = _load_learned_topics()
    words = question.strip().split()
    topic_name = " ".join(words[:5]) if len(words) > 5 else question.strip()
    topic_name = topic_name.rstrip("?!.,")
    if topic_name not in learned:
        learned[topic_name] = {
            "Dụng_Thần": dung_than_list,
            "Luận_Giải_Gợi_Ý": goi_y,
            "Nhóm": category,
            "Ngày_Tạo": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Câu_Hỏi_Gốc": question
        }
        try:
            with open(LEARNED_TOPICS_FILE, 'w', encoding='utf-8') as f:
                json.dump(learned, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

def _expand_with_synonyms(text):
    """Mở rộng text bằng từ đồng nghĩa"""
    expanded = text.lower()
    for word, syns in SYNONYM_MAP.items():
        if word in expanded:
            expanded += " " + " ".join(syns)
    return expanded


def _ngu_hanh_relation(h1, h2):
    """h1 đối với h2: sinh/khắc/bị sinh/bị khắc/tỷ hòa"""
    if not h1 or not h2:
        return "Không rõ"
    if h1 == h2:
        return "Tỷ Hòa (ngang nhau)"
    if SINH.get(h1) == h2:
        return f"{h1} SINH {h2} (hao tổn)"
    if SINH.get(h2) == h1:
        return f"{h2} sinh {h1} → ĐƯỢC SINH (tốt)"
    if KHAC.get(h1) == h2:
        return f"{h1} KHẮC {h2} (mình thắng)"
    if KHAC.get(h2) == h1:
        return f"{h2} khắc {h1} → BỊ KHẮC (xấu)"
    return "Không xác định"


def _get_dung_than(question):
    """V34.2: Xác định Dụng Thần — SUBJECT-FIRST (chủ thể luôn thắng ngữ cảnh).
    
    Nguyên lý: NGƯỜI/VẬT được hỏi (chủ thể) luôn quyết định DT.
    - "mẹ bệnh nặng" → chủ thể = mẹ → PHỤ MẪU (ko phải bệnh → Quan Quỷ)
    - "chồng ngoại tình" → chủ thể = chồng → QUAN QUỶ (ko phải ngoại tình → Thê Tài)
    - "chó nhà khỏe không" → chủ thể = chó → TỬ TÔN (ko phải nhà → Phụ Mẫu)
    
    3 tầng ưu tiên:
      T1: CHỦ THỂ (người/vật) — match đầu → RETURN luôn
      T2: NGỮ CẢNH (hành động/trạng thái) — fallback nếu ko có T1
      T3: Default = Quan Quỷ
    """
    q = question.lower()
    
    # ═══ TIER 1: CHỦ THỂ — Người / Vật được hỏi (LUÔN THẮNG) ═══
    # Sorted dài→ngắn để "con trai" match trước "con"
    _SUBJECT_DT = [
        # Phụ Mẫu — người bề trên + tài sản che chở
        ('bất động sản', 'Phụ Mẫu'), ('nhà đất', 'Phụ Mẫu'),
        ('căn hộ', 'Phụ Mẫu'), ('chung cư', 'Phụ Mẫu'),
        ('ông ngoại', 'Phụ Mẫu'), ('ông nội', 'Phụ Mẫu'),
        ('bà ngoại', 'Phụ Mẫu'), ('bà nội', 'Phụ Mẫu'),
        ('bố mẹ', 'Phụ Mẫu'), ('cha mẹ', 'Phụ Mẫu'),
        ('tổ tiên', 'Phụ Mẫu'), ('mồ mả', 'Phụ Mẫu'),
        ('hợp đồng', 'Phụ Mẫu'), ('văn bằng', 'Phụ Mẫu'), ('bằng cấp', 'Phụ Mẫu'),
        ('giấy phép', 'Phụ Mẫu'), ('bằng lái', 'Phụ Mẫu'), ('giấy tờ', 'Phụ Mẫu'),
        ('hộ chiếu', 'Phụ Mẫu'), ('thẻ căn cước', 'Phụ Mẫu'),
        ('quần áo', 'Phụ Mẫu'), ('trang phục', 'Phụ Mẫu'), ('giày dép', 'Phụ Mẫu'),
        ('mũ nón', 'Phụ Mẫu'), ('ô dù', 'Phụ Mẫu'),
        ('sách vở', 'Phụ Mẫu'), ('văn bản', 'Phụ Mẫu'),
        ('máy bay', 'Phụ Mẫu'), ('tàu hỏa', 'Phụ Mẫu'),
        ('bảo hiểm', 'Phụ Mẫu'), ('phong thủy', 'Phụ Mẫu'),
        ('nhà', 'Phụ Mẫu'), ('xe', 'Phụ Mẫu'), ('đất', 'Phụ Mẫu'),
        ('sách', 'Phụ Mẫu'), ('giấy', 'Phụ Mẫu'),
        ('thuyền', 'Phụ Mẫu'), ('tàu', 'Phụ Mẫu'),
        ('bố', 'Phụ Mẫu'), ('mẹ', 'Phụ Mẫu'), ('cha', 'Phụ Mẫu'),
        ('áo', 'Phụ Mẫu'), ('mộ', 'Phụ Mẫu'),
        ('passport', 'Phụ Mẫu'), ('visa', 'Phụ Mẫu'),

        # Thê Tài — tài sản, vợ, người yêu
        ('người yêu', 'Thê Tài'), ('bạn trai', 'Thê Tài'), ('bạn gái', 'Thê Tài'),
        ('cổ phiếu', 'Thê Tài'), ('chứng khoán', 'Thê Tài'),
        ('điện thoại', 'Thê Tài'), ('laptop', 'Thê Tài'),
        ('kim cương', 'Thê Tài'), ('trang sức', 'Thê Tài'),
        ('hàng hóa', 'Thê Tài'), ('kho hàng', 'Thê Tài'),
        ('lương thực', 'Thê Tài'), ('thức ăn', 'Thê Tài'),
        ('tiền', 'Thê Tài'), ('vốn', 'Thê Tài'), ('lương', 'Thê Tài'),
        ('vàng', 'Thê Tài'), ('nợ', 'Thê Tài'),
        ('vợ', 'Thê Tài'), ('crypto', 'Thê Tài'), ('coin', 'Thê Tài'),

        ('thi công chức', 'Phụ Mẫu'),  # thi = giáo dục, thắng công chức
        # Quan Quỷ — chồng (nữ hỏi), sếp, đối tác, tranh chấp
        ('tranh chấp', 'Quan Quỷ'), ('đối tác', 'Quan Quỷ'), ('khách hàng', 'Quan Quỷ'),
        ('công chức', 'Quan Quỷ'), ('công an', 'Quan Quỷ'), ('quân đội', 'Quan Quỷ'),
        ('chồng', 'Quan Quỷ'), ('sếp', 'Quan Quỷ'),

        # Tử Tôn — con cái, vật nuôi, bác sĩ, thuốc
        ('con trai', 'Tử Tôn'), ('con gái', 'Tử Tôn'), ('con dâu', 'Tử Tôn'),
        ('con rể', 'Tử Tôn'), ('con cái', 'Tử Tôn'),
        ('bác sĩ', 'Tử Tôn'), ('bệnh viện', 'Tử Tôn'),
        ('vật nuôi', 'Tử Tôn'), ('thú cưng', 'Tử Tôn'),
        ('nhà sư', 'Tử Tôn'), ('tu hành', 'Tử Tôn'),
        ('thuốc', 'Tử Tôn'), ('chó', 'Tử Tôn'), ('mèo', 'Tử Tôn'),
        ('con', 'Tử Tôn'), ('cháu', 'Tử Tôn'),

        # Huynh Đệ — ngang hàng
        ('anh chị em', 'Huynh Đệ'), ('anh em', 'Huynh Đệ'),
        ('đối thủ cạnh tranh', 'Huynh Đệ'),
        ('đồng nghiệp', 'Huynh Đệ'), ('đối thủ', 'Huynh Đệ'),
        ('cờ bạc', 'Huynh Đệ'), ('đánh bạc', 'Huynh Đệ'), ('xổ số', 'Huynh Đệ'),
        ('lô đề', 'Huynh Đệ'),
        ('bạn', 'Huynh Đệ'), ('anh', 'Huynh Đệ'), ('chị', 'Huynh Đệ'), ('em', 'Huynh Đệ'),

        # Bản Thân
        ('tuổi', 'Bản Thân'),
    ]
    
    # Tìm chủ thể xuất hiện SỚM NHẤT trong câu (vị trí đầu = chủ thể chính)
    best_pos = len(q) + 1
    best_dt = None
    best_kw = ''
    
    # Danh sách keywords ngắn cần kiểm tra word boundary
    # (tránh 'anh' trong 'kinh doanh', 'em' trong 'xem', 'chị' trong 'chỉ')
    _SHORT_BOUNDARY = {'anh', 'em', 'chị', 'bạn', 'con', 'áo', 'mộ', 'xe', 'tàu'}
    
    for kw, dt in _SUBJECT_DT:
        pos = q.find(kw)
        if pos >= 0:
            # Word boundary check cho keywords ngắn (≤3 chars)
            if kw in _SHORT_BOUNDARY:
                # Kiểm tra trước và sau keyword phải là space, đầu/cuối câu, hoặc dấu
                before_ok = (pos == 0) or (q[pos-1] in ' ,;.!?')
                after_pos = pos + len(kw)
                after_ok = (after_pos >= len(q)) or (q[after_pos] in ' ,;.!?')
                if not (before_ok and after_ok):
                    continue  # Skip false positive
            
            # Ưu tiên: vị trí sớm nhất, nếu cùng vị trí thì keyword dài hơn thắng
            if pos < best_pos or (pos == best_pos and len(kw) > len(best_kw)):
                best_pos = pos
                best_dt = dt
                best_kw = kw
    if best_dt:
        return best_dt
    
    # ═══ TIER 2: NGỮ CẢNH — Hành động/trạng thái (chỉ khi ko có chủ thể) ═══
    _CONTEXT_DT = [
        # Phụ Mẫu — hành động liên quan nhà, học, thi
        ('xây nhà', 'Phụ Mẫu'), ('sửa nhà', 'Phụ Mẫu'), ('thuê nhà', 'Phụ Mẫu'),
        ('mua nhà', 'Phụ Mẫu'), ('bán nhà', 'Phụ Mẫu'),
        ('mua xe', 'Phụ Mẫu'), ('bán xe', 'Phụ Mẫu'), ('mua đất', 'Phụ Mẫu'),
        ('học', 'Phụ Mẫu'), ('thi', 'Phụ Mẫu'), ('trường', 'Phụ Mẫu'),
        ('cúng', 'Phụ Mẫu'),

        # Thê Tài — mua bán, đầu tư, mất, tình duyên
        ('ngoại tình', 'Thê Tài'), ('đầu tư', 'Thê Tài'),
        ('tăng lương', 'Thê Tài'), ('thu nhập', 'Thê Tài'),
        ('tình duyên', 'Thê Tài'), ('kết hôn', 'Thê Tài'), ('ly hôn', 'Thê Tài'),
        ('kinh doanh', 'Thê Tài'), ('buôn bán', 'Thê Tài'),
        ('mua', 'Thê Tài'), ('bán', 'Thê Tài'), ('vay', 'Thê Tài'),
        ('mất', 'Thê Tài'), ('trộm', 'Thê Tài'), ('cắp', 'Thê Tài'),
        ('lãi', 'Thê Tài'), ('lời', 'Thê Tài'), ('lỗ', 'Thê Tài'),
        ('tài', 'Thê Tài'),

        # Quan Quỷ — bệnh, kiện, tai nạn, việc
        ('thăng chức', 'Quan Quỷ'), ('xin việc', 'Quan Quỷ'),
        ('kiện tụng', 'Quan Quỷ'), ('kiện cáo', 'Quan Quỷ'), ('tranh chấp', 'Quan Quỷ'),
        ('ung thư', 'Quan Quỷ'), ('tai nạn', 'Quan Quỷ'),
        ('trầm cảm', 'Quan Quỷ'), ('lo âu', 'Quan Quỷ'),
        ('hỏa hoạn', 'Quan Quỷ'), ('lũ lụt', 'Quan Quỷ'), ('động đất', 'Quan Quỷ'),
        ('việc', 'Quan Quỷ'), ('bệnh', 'Quan Quỷ'), ('kiện', 'Quan Quỷ'),
        ('ốm', 'Quan Quỷ'), ('đau', 'Quan Quỷ'), ('stress', 'Quan Quỷ'),
        ('cháy', 'Quan Quỷ'),

        # Tử Tôn — giải trí, bình an, chơi
        ('du lịch', 'Tử Tôn'), ('giải trí', 'Tử Tôn'),
        ('bình an', 'Tử Tôn'), ('vui', 'Tử Tôn'), ('chơi', 'Tử Tôn'),

        # Huynh Đệ — cờ bạc, cạnh tranh
        ('cờ bạc', 'Huynh Đệ'), ('đánh bạc', 'Huynh Đệ'), ('xổ số', 'Huynh Đệ'),
    ]
    
    for kw, dt in _CONTEXT_DT:
        if kw in q:
            return dt
    
    # ═══ TIER 3: DEFAULT ═══
    # Nếu ko match gì → xem "tôi/mình" → Bản Thân, còn lại → Quan Quỷ
    if 'tôi' in q or 'mình' in q:
        return 'Bản Thân'
    return "Quan Quỷ"


def _get_all_dung_than(question):
    """V41.0: Trả về TẤT CẢ Dụng Thần cho câu hỏi phức hợp.
    
    Ví dụ: "vợ bệnh, con thất học" → ['Thê Tài', 'Tử Tôn']
    Ví dụ: "mẹ tôi bệnh" → ['Phụ Mẫu']
    
    Returns: list[str] — danh sách DT (primary đứng đầu)
    """
    q = question.lower()
    
    # Reuse SUBJECT_DT from _get_dung_than
    _SUBJECT_DT = [
        ('bất động sản', 'Phụ Mẫu'), ('nhà đất', 'Phụ Mẫu'),
        ('ông ngoại', 'Phụ Mẫu'), ('ông nội', 'Phụ Mẫu'),
        ('bà ngoại', 'Phụ Mẫu'), ('bà nội', 'Phụ Mẫu'),
        ('bố mẹ', 'Phụ Mẫu'), ('cha mẹ', 'Phụ Mẫu'),
        ('hợp đồng', 'Phụ Mẫu'), ('giấy tờ', 'Phụ Mẫu'),
        ('nhà', 'Phụ Mẫu'), ('xe', 'Phụ Mẫu'), ('đất', 'Phụ Mẫu'),
        ('bố', 'Phụ Mẫu'), ('mẹ', 'Phụ Mẫu'), ('cha', 'Phụ Mẫu'),
        ('người yêu', 'Thê Tài'), ('bạn trai', 'Thê Tài'), ('bạn gái', 'Thê Tài'),
        ('cổ phiếu', 'Thê Tài'), ('điện thoại', 'Thê Tài'),
        ('tiền', 'Thê Tài'), ('vốn', 'Thê Tài'), ('lương', 'Thê Tài'),
        ('vợ', 'Thê Tài'), ('crypto', 'Thê Tài'),
        ('chồng', 'Quan Quỷ'), ('sếp', 'Quan Quỷ'), ('đối tác', 'Quan Quỷ'),
        ('con trai', 'Tử Tôn'), ('con gái', 'Tử Tôn'), ('con cái', 'Tử Tôn'),
        ('bác sĩ', 'Tử Tôn'), ('thuốc', 'Tử Tôn'),
        ('chó', 'Tử Tôn'), ('mèo', 'Tử Tôn'), ('con', 'Tử Tôn'), ('cháu', 'Tử Tôn'),
        ('anh em', 'Huynh Đệ'), ('đồng nghiệp', 'Huynh Đệ'),
        ('xổ số', 'Huynh Đệ'), ('cờ bạc', 'Huynh Đệ'),
        ('bạn', 'Huynh Đệ'),
    ]
    
    _SHORT_BOUNDARY = {'anh', 'em', 'chị', 'bạn', 'con', 'áo', 'mộ', 'xe', 'tàu'}
    
    found = []  # list of (position, dt_name, keyword)
    seen_dt = set()
    
    for kw, dt in _SUBJECT_DT:
        pos = q.find(kw)
        if pos >= 0:
            if kw in _SHORT_BOUNDARY:
                before_ok = (pos == 0) or (q[pos-1] in ' ,;.!?')
                after_pos = pos + len(kw)
                after_ok = (after_pos >= len(q)) or (q[after_pos] in ' ,;.!?')
                if not (before_ok and after_ok):
                    continue
            if dt not in seen_dt:
                found.append((pos, dt, kw))
                seen_dt.add(dt)
    
    # Sort by position → primary DT first
    found.sort(key=lambda x: x[0])
    result = [f[1] for f in found]
    
    if not result:
        result = [_get_dung_than(question)]
    
    return result


def _match_topic(question, topic=None):
    """V7.0 — Smart Topic Matching: Synonym + Learned Topics + Weighted Scoring"""
    if topic and topic in TOPIC_INTERPRETATIONS:
        return topic, TOPIC_INTERPRETATIONS[topic]
    
    # Merge TOPIC_INTERPRETATIONS + Learned Topics
    all_topics = dict(TOPIC_INTERPRETATIONS) if TOPIC_INTERPRETATIONS else {}
    learned = _load_learned_topics()
    all_topics.update(learned)
    
    if not all_topics:
        return None, {}
    
    q = question.lower()
    q_expanded = _expand_with_synonyms(q)
    best_topic = None
    best_score = 0
    
    for t_name, t_data in all_topics.items():
        score = 0
        t_lower = t_name.lower().replace("_", " ")
        
        # Layer 1: EXACT MATCH (x3)
        if t_lower in q:
            score += len(t_lower) * 3
        
        # Layer 2: KEYWORD MATCH (x2)
        words = t_lower.split()
        for w in words:
            if len(w) >= 2 and w in q:
                score += len(w) * 2
        
        # Layer 3: SYNONYM MATCH (x1)
        for w in words:
            if len(w) >= 2 and w in q_expanded and w not in q:
                score += len(w)
        
        # Layer 4: HINT MATCH (x1)
        hint = t_data.get("Luận_Giải_Gợi_Ý", "").lower()
        for hw in hint.replace(",", " ").replace(".", " ").split():
            if len(hw.strip()) >= 3 and hw.strip() in q:
                score += 1
        
        # Layer 5: LEARNED QUESTION MATCH
        orig_q = t_data.get("Câu_Hỏi_Gốc", "").lower()
        if orig_q and orig_q in q:
            score += 20
        
        if score > best_score:
            best_score = score
            best_topic = t_name
    
    if best_topic and best_score >= 3:
        result_data = all_topics[best_topic]
        if best_topic in learned:
            result_data['_source'] = 'learned'
        return best_topic, result_data
    return None, {}


def _is_age_question(question):
    q = question.lower()
    return any(kw in q for kw in ['tuổi', 'bao nhiêu tuổi', 'mấy tuổi', 'số tuổi', 'năm sinh',
                                   'tuoi', 'may tuoi', 'bao nhieu tuoi'])


def _is_find_question(question):
    q = question.lower()
    return any(kw in q for kw in ['ở đâu', 'tìm', 'mất', 'đánh rơi', 'để đâu',
                                   'o dau', 'tim', 'mat', 'de dau'])


def _is_yesno_question(question):
    q = question.lower()
    return any(kw in q for kw in ['có nên', 'có được', 'có không', 'nên không', 'được không', 'liệu có',
                                   'co nen', 'co duoc', 'co khong', 'nen khong', 'duoc khong'])


def _is_count_question(question):
    """Phát hiện câu hỏi đếm số lượng: bao nhiêu, mấy, số lượng"""
    q = question.lower()
    return any(kw in q for kw in ['bao nhiêu', 'mấy', 'số lượng', 'đếm', 'có mấy',
                                   'bao nhieu', 'may ', 'so luong', 'co may'])


def _is_competition_question(question):
    """V42.3: Phát hiện câu hỏi THẮNG THUA / đối kháng / cạnh tranh.
    
    Bao gồm: thể thao, kiện tụng, cạnh tranh kinh doanh, thi đấu, so sánh 2 bên.
    Khi câu hỏi là dạng so sánh 2 bên → dùng phân tích Thế vs Ứng.
    """
    q = question.lower()
    
    # Layer 1: Từ khóa trực tiếp thắng thua + đối kháng
    _COMP_DIRECT = [
        'đội nào thắng', 'đội nào thua', 'ai thắng', 'ai thua', 'bên nào thắng',
        'bên nào thua', 'phe nào thắng', 'đội nào chiến thắng', 'đội nào vô địch',
        'thắng hay thua', 'thắng thua', 'hơn hay kém',
        # Không dấu
        'doi nao thang', 'doi nao thua', 'ai thang', 'ai thua',
        'ben nao thang', 'thang hay thua', 'thang thua',
    ]
    if any(kw in q for kw in _COMP_DIRECT):
        return True
    
    # Layer 2: Pattern "A vs/và/đấu/gặp B" + câu hỏi thắng thua
    import re as _re_comp
    _COMP_PATTERNS = [
        r'đội\s+\w+\s+(vs|và|đấu|gặp|đá với)\s+đội\s+\w+',
        r'\w+\s+(vs|đấu với|gặp)\s+\w+.*(thắng|thua|hơn|kém)',
        r'(trận|cuộc)\s+\w+.*(thắng|thua|kết quả)',
        # V42.8f: Thêm pattern "A vs B" standalone (không cần thắng/thua)
        r'\w+\s+vs\.?\s+\w+',
        # V42.8f: "A hay B thắng/thua/hơn"
        r'\w+\s+hay\s+\w+\s+(thắng|thua|hơn|kém|mạnh|yếu)',
        # V42.8f: "A thắng hay B thắng"
        r'\w+\s+thắng\s+hay\s+\w+\s+thắng',
    ]
    if any(_re_comp.search(pat, q) for pat in _COMP_PATTERNS):
        return True
    
    # Layer 3: Combo — sport/contest + thắng/thua
    _SPORT_KW = ['bóng đá', 'bóng rổ', 'bóng chuyền', 'tennis', 'cầu lông',
                 'boxing', 'quyền anh', 'trận đấu', 'giải đấu', 'thi đấu',
                 'vòng bảng', 'bán kết', 'chung kết', 'tứ kết',
                 'world cup', 'champions league', 'premier league', 'ngoại hạng',
                 'v-league', 'sea games', 'olympic', 'bong da', 'tran dau']
    _PREDICT_KW = ['thắng', 'thua', 'hòa', 'kết quả', 'vô địch', 'tỷ số',
                   'thang', 'thua', 'hoa', 'ket qua', 'vo dich', 'ty so']
    _has_sport = any(kw in q for kw in _SPORT_KW)
    _has_predict = any(kw in q for kw in _PREDICT_KW)
    if _has_sport and _has_predict:
        return True
    
    return False


def _extract_two_sides(question):
    """V42.3: Trích xuất TÊN 2 BÊN từ câu hỏi thắng thua.
    
    Ví dụ:
    - "Đội MU đấu với đội Liverpool" → ("MU", "Liverpool")
    - "Việt Nam gặp Thái Lan" → ("Việt Nam", "Thái Lan")
    - "A vs B ai thắng" → ("A", "B")
    
    Returns: (side_a, side_b) hoặc ("Bên được hỏi đầu", "Đối phương") nếu không tìm thấy.
    """
    import re as _re_sides
    q = question.strip()
    
    # Pattern 1: "đội X đấu/gặp/vs đội Y" (có dấu + không dấu)
    m = _re_sides.search(r'[Đđ](?:ội|oi)\s+(.+?)\s+(?:đấu với|dau voi|đấu|dau|gặp|gap|đá với|da voi|vs\.?|và|va)\s+[Đđ]?(?:ội|oi)?\s*(.+?)(?:\s+đội|\s+doi|\s+ai|\s+bên|\s+ben|\s+thắng|\s+thang|\s+thua|\?|$)', q, _re_sides.IGNORECASE)
    if m:
        return (m.group(1).strip().rstrip(',. '), m.group(2).strip().rstrip('?,. '))
    
    # Pattern 2: "X đấu/gặp/vs Y" (không có chữ "đội")
    m = _re_sides.search(r'(?:trận\s+|tran\s+)?(.+?)\s+(?:đấu với|dau voi|đấu|dau|gặp|gap|vs\.?|đá với|da voi)\s+(.+?)(?:\s+ai|\s+đội nào|\s+doi nao|\s+bên nào|\s+ben nao|\s+thắng|\s+thang|\s+thua|\s+kết quả|\s+ket qua|\?|$)', q, _re_sides.IGNORECASE)
    if m:
        a = m.group(1).strip().rstrip(',. ')
        b = m.group(2).strip().rstrip('?,. ')
        # Bỏ prefix thừa
        for prefix in ['trận ', 'tran ', 'cuộc ', 'cuoc ', 'kết quả ', 'ket qua ', 'chung kết ', 'chung ket ']:
            if a.lower().startswith(prefix):
                a = a[len(prefix):]
        if len(a) > 1 and len(b) > 1:
            return (a, b)
    
    # Pattern 3: "X và/va Y đội nào/doi nao thắng/thang"
    m = _re_sides.search(r'(.+?)\s+(?:và|va)\s+(.+?)\s+(?:đội nào|doi nao|ai|bên nào|ben nao|thắng|thang|thua)', q, _re_sides.IGNORECASE)
    if m:
        a = m.group(1).strip().rstrip(',. ')
        b = m.group(2).strip().rstrip('?,. ')
        for prefix in ['đội ', 'Đội ', 'doi ']:
            if a.lower().startswith(prefix.lower()):
                a = a[len(prefix):]
            if b.lower().startswith(prefix.lower()):
                b = b[len(prefix):]
        if len(a) > 0 and len(b) > 0:
            return (a, b)
    
    # Pattern 4: "X hay Y thắng/thang" 
    m = _re_sides.search(r'(.+?)\s+hay\s+(.+?)\s+(?:thắng|thang|thua|hơn|hon|mạnh|manh)', q, _re_sides.IGNORECASE)
    if m:
        a = m.group(1).strip().rstrip(',. ')
        b = m.group(2).strip().rstrip('?,. ')
        if len(a) > 0 and len(b) > 0:
            return (a, b)
    
    return ("Bên được hỏi đầu", "Đối phương")

def _build_tam_thoi(question, dung_than, hanh_dt, ts_stage, ngu_khi, weighted_pct,
                     ky_mon_verdict='', ky_mon_reason='', luc_hao_verdict='', luc_hao_reason='',
                     mai_hoa_verdict='', mai_hoa_reason='', luc_nham_reason='', thai_at_reason='',
                     detected_category=''):
    """
    V35.5: TAM THỜI LUẬN GIẢI — TÍNH SỨC MẠNH THỰC TẾ cho mỗi thời kỳ.
    Dùng TS_STRENGTH (điểm sức mạnh) cho mỗi giai đoạn 12 Trường Sinh.
    Không dùng mô tả cố định — verdict VƯỢNG/BÌNH/SUY tính từ điểm thực.
    """
    lines = []
    lines.append(f"\n### 🔮 TAM THỜI LUẬN GIẢI (Quá Khứ → Hiện Tại → Tương Lai)")
    
    # Chu kỳ 12 Trường Sinh + ĐIỂM SỨC MẠNH mỗi giai đoạn
    TS_CYCLE = ['Trường Sinh', 'Mộc Dục', 'Quan Đới', 'Lâm Quan', 'Đế Vượng',
                'Suy', 'Bệnh', 'Tử', 'Mộ', 'Tuyệt', 'Thai', 'Dưỡng']
    
    TS_STRENGTH = {
        'Trường Sinh': 60, 'Mộc Dục': 35, 'Quan Đới': 50, 'Lâm Quan': 75,
        'Đế Vượng': 90, 'Suy': 40, 'Bệnh': 25, 'Tử': 10,
        'Mộ': 15, 'Tuyệt': 5, 'Thai': 20, 'Dưỡng': 45,
    }
    
    current_ts = ts_stage or 'Quan Đới'
    try:
        idx = TS_CYCLE.index(current_ts)
        prev_ts = TS_CYCLE[(idx - 1) % 12]
        next_ts = TS_CYCLE[(idx + 1) % 12]
    except ValueError:
        idx, prev_ts, next_ts = 2, 'Mộc Dục', 'Lâm Quan'
    
    prev_str = TS_STRENGTH.get(prev_ts, 50)
    curr_str = TS_STRENGTH.get(current_ts, 50)
    next_str = TS_STRENGTH.get(next_ts, 50)
    
    # DT → ngữ cảnh cụ thể
    DT_CONTEXT = {
        'Phụ Mẫu': 'nhà cửa/giấy tờ/bề trên',
        'Thê Tài': 'tiền bạc/tài sản/người yêu',
        'Quan Quỷ': 'công việc/sếp/kiện tụng',
        'Tử Tôn': 'con cái/giải trí/thuốc men',
        'Huynh Đệ': 'anh em/bạn bè/đối thủ',
    }
    dt_obj = DT_CONTEXT.get(dung_than, 'sự việc')
    
    # Ngũ Hành sinh/khắc
    HANH_SINH = {'Kim': 'Thổ sinh Kim', 'Mộc': 'Thủy sinh Mộc', 'Thủy': 'Kim sinh Thủy', 'Hỏa': 'Mộc sinh Hỏa', 'Thổ': 'Hỏa sinh Thổ'}
    HANH_KHAC = {'Kim': 'Hỏa khắc Kim', 'Mộc': 'Kim khắc Mộc', 'Thủy': 'Thổ khắc Thủy', 'Hỏa': 'Thủy khắc Hỏa', 'Thổ': 'Mộc khắc Thổ'}
    
    # === HÀM TÍNH VERDICT + MÔ TẢ TỪ ĐIỂM SỨC MẠNH ===
    def _strength_verdict(strength, stage, obj):
        """Tạo mô tả LINH HOẠT từ điểm sức mạnh thực tế"""
        if strength >= 75:
            return f"🟢 **CỰC VƯỢNG** ({strength}%)", f"{obj} rất mạnh, thuận lợi, phát triển đỉnh cao"
        elif strength >= 55:
            return f"🔵 **VƯỢNG** ({strength}%)", f"{obj} có lực, đang phát triển tốt"
        elif strength >= 40:
            return f"🟡 **BÌNH** ({strength}%)", f"{obj} ở mức trung bình, không nổi bật"
        elif strength >= 20:
            return f"🟠 **SUY** ({strength}%)", f"{obj} yếu, gặp trở ngại, cần hỗ trợ"
        else:
            return f"🔴 **CỰC SUY** ({strength}%)", f"{obj} rất yếu, gần như đình trệ"
    
    # === TÍNH XU HƯỚNG ===
    def _trend(prev_s, curr_s, next_s):
        if next_s > curr_s + 10:
            return "📈 **TĂNG MẠNH**"
        elif next_s > curr_s:
            return "📈 TĂNG NHẸ"
        elif next_s < curr_s - 10:
            return "📉 **GIẢM MẠNH**"
        elif next_s < curr_s:
            return "📉 GIẢM NHẸ"
        else:
            return "📊 ỔN ĐỊNH"
    
    trend_icon = _trend(prev_str, curr_str, next_str)
    
    # ══════ QUÁ KHỨ ══════
    qk_verdict, qk_desc = _strength_verdict(prev_str, prev_ts, dt_obj)
    lines.append(f"\n**🕰️ QUÁ KHỨ** *(Giai đoạn: {prev_ts})*")
    lines.append(f"- {dung_than} ({hanh_dt}) ở {prev_ts}: {qk_verdict}")
    lines.append(f"- {qk_desc}")
    # So sánh quá khứ vs hiện tại
    if prev_str > curr_str:
        lines.append(f"- ↘️ Quá khứ MẠNH hơn hiện tại ({prev_str}% → {curr_str}%) — đã đi xuống")
    elif prev_str < curr_str:
        lines.append(f"- ↗️ Quá khứ YẾU hơn hiện tại ({prev_str}% → {curr_str}%) — đã vươn lên")
    # Kỳ Môn xác nhận quá khứ
    if ky_mon_reason:
        lines.append(f"- 🏯 Kỳ Môn ({ky_mon_verdict}): {ky_mon_reason}")
    
    # ══════ HIỆN TẠI ══════
    ht_verdict, ht_desc = _strength_verdict(curr_str, current_ts, dt_obj)
    lines.append(f"\n**📍 HIỆN TẠI** *(Giai đoạn: **{current_ts}** | Ngũ Khí: {ngu_khi})*")
    lines.append(f"- {dung_than} ({hanh_dt}) ở {current_ts}: {ht_verdict}")
    lines.append(f"- {ht_desc}")
    lines.append(f"- Điểm thực tế: **{weighted_pct}%**")
    # Sinh/Khắc giải thích
    sinh_info = HANH_SINH.get(hanh_dt, '')
    khac_info = HANH_KHAC.get(hanh_dt, '')
    if weighted_pct >= 55 and sinh_info:
        lines.append(f"- ✅ {sinh_info} → {dung_than} được sinh trợ")
    elif weighted_pct < 45 and khac_info:
        lines.append(f"- ❌ {khac_info} → {dung_than} bị khắc chế")
    # Lục Hào hiện trạng
    if luc_hao_reason:
        lines.append(f"- 📿 Lục Hào ({luc_hao_verdict}): {luc_hao_reason}")
    if luc_nham_reason:
        lines.append(f"- 🔮 Đại Lục Nhâm: {luc_nham_reason}")
    
    # ══════ TƯƠNG LAI ══════
    tl_verdict, tl_desc = _strength_verdict(next_str, next_ts, dt_obj)
    lines.append(f"\n**🔮 TƯƠNG LAI** *(Giai đoạn: **{next_ts}**)*")
    lines.append(f"- {dung_than} ({hanh_dt}) sẽ chuyển sang {next_ts}: {tl_verdict}")
    lines.append(f"- {tl_desc}")
    lines.append(f"- Xu hướng: {trend_icon} ({curr_str}% → {next_str}%)")
    # Thái Ất dự báo
    if thai_at_reason:
        lines.append(f"- ⭐ Thái Ất: {thai_at_reason}")
    # Mai Hoa bổ sung
    if mai_hoa_reason and isinstance(mai_hoa_reason, str) and len(mai_hoa_reason) < 150:
        lines.append(f"- 🌸 Mai Hoa ({mai_hoa_verdict}): {mai_hoa_reason}")
    
    # Ứng Kỳ timing
    HA_DO_TIMING = {
        'Kim': ('tháng Thân/Dậu (7-8 ÂL)', 'ngày Canh/Tân'),
        'Mộc': ('tháng Dần/Mão (1-2 ÂL)', 'ngày Giáp/Ất'),
        'Thủy': ('tháng Hợi/Tý (10-11 ÂL)', 'ngày Nhâm/Quý'),
        'Hỏa': ('tháng Tỵ/Ngọ (4-5 ÂL)', 'ngày Bính/Đinh'),
        'Thổ': ('tháng Thìn/Tuất/Sửu/Mùi (3/6/9/12 ÂL)', 'ngày Mậu/Kỷ'),
    }
    timing_info = HA_DO_TIMING.get(hanh_dt, None)
    if timing_info:
        lines.append(f"- ⏳ **Ứng kỳ:** {timing_info[0]}, {timing_info[1]}")
    
    # Lời tiên tri — DỰA TRÊN XU HƯỚNG THỰC TẾ
    if next_str > curr_str:
        lines.append(f"\n> 📜 *\"{dung_than} ({hanh_dt}) đang từ {current_ts} ({curr_str}%) lên {next_ts} ({next_str}%). {dt_obj.capitalize()} sẽ khởi sắc!\"*")
    elif next_str < curr_str - 20:
        lines.append(f"\n> 📜 *\"{dung_than} từ {current_ts} ({curr_str}%) xuống {next_ts} ({next_str}%). Thịnh cực tất suy — hành động ngay trước khi quá muộn!\"*")
    elif next_str < curr_str:
        lines.append(f"\n> 📜 *\"{dung_than} sẽ giảm nhẹ ({curr_str}% → {next_str}%). Giữ vững, không nên mạo hiểm thêm.\"*")
    else:
        lines.append(f"\n> 📜 *\"{dung_than} duy trì ổn định tại {current_ts}. Thuận theo tự nhiên, chờ thời cơ.\"*")
    
    return "\n".join(lines)


# === SAO/CỬA/THẦN GIẢI THÍCH CHI TIẾT (V8.0) ===
SAO_GIAI_THICH = {
    'Thiên Bồng': {'tinh_chat': 'Hung tinh — Tướng quân hung mãnh, liên quan đến trộm cướp, mưu kế, sông nước', 'hanh': 'Thủy', 'van_de': 'Rủi ro, bất trắc, mưu đồ, nhưng nếu gặp Cửa Cát thì hóa giải'},
    'Thiên Nhuế': {'tinh_chat': 'Hung tinh — Bệnh tật, chậm chạp, y dược, giáo dục', 'hanh': 'Thổ', 'van_de': 'Trì trệ, cần kiên nhẫn, không nên vội vàng'},
    'Thiên Xung': {'tinh_chat': 'Cát tinh — Quân sự, động lực, cạnh tranh, di chuyển', 'hanh': 'Mộc', 'van_de': 'Hành động mạnh mẽ, thích hợp khởi sự, di chuyển'},
    'Thiên Phụ': {'tinh_chat': 'Cát tinh — Văn chương, học thuật, ẩn tàng, trí tuệ', 'hanh': 'Mộc', 'van_de': 'Thuận lợi cho học tập, nghiên cứu, lập kế hoạch'},
    'Thiên Cầm': {'tinh_chat': 'Trung tính — Lãnh đạo, trung tâm, điều hòa', 'hanh': 'Thổ', 'van_de': 'Trung bình, cần xem thêm yếu tố khác'},
    'Thiên Tâm': {'tinh_chat': 'Đại Cát tinh — Mưu lược, y học, thần bí, quý nhân', 'hanh': 'Kim', 'van_de': 'Rất tốt, có người giúp đỡ, chữa trị hiệu quả'},
    'Thiên Trụ': {'tinh_chat': 'Hung tinh — Phá hoại, gây rối, ẩn náu', 'hanh': 'Kim', 'van_de': 'Cẩn thận tiểu nhân phá hoại, thị phi'},
    'Thiên Nhậm': {'tinh_chat': 'Cát tinh — Điền sản, tài lộc, nhẫn nại', 'hanh': 'Thổ', 'van_de': 'Tốt cho nhà đất, tích lũy, nhẫn nại chờ đợi'},
    'Thiên Anh': {'tinh_chat': 'Hung tinh — Văn minh, danh vọng, hỏa hoạn', 'hanh': 'Hỏa', 'van_de': 'Nổi bật nhưng cẩn thận lửa, thị phi danh tiếng'},
    'Thiên Nhuế/Cầm': {'tinh_chat': 'Trung/Hung — Thiên Nhuế kèm Thiên Cầm, chậm chạp', 'hanh': 'Thổ', 'van_de': 'Trì trệ, cần kiên nhẫn chờ đợi'}
}

CUA_GIAI_THICH = {
    'Khai Môn': {'cat_hung': 'Đại Cát', 'y_nghia': 'Mở ra, khởi nghiệp, công việc, nhậm chức', 'loi_khuyen': 'Rất thuận lợi cho việc bắt đầu mới'},
    'Hưu Môn': {'cat_hung': 'Cát', 'y_nghia': 'Nghỉ ngơi, vui vẻ, gặp quý nhân, thư giãn', 'loi_khuyen': 'Thuận lợi cho giao tiếp, hòa giải'},
    'Sinh Môn': {'cat_hung': 'Đại Cát', 'y_nghia': 'Tài lộc, sinh sôi, kinh doanh, phát triển', 'loi_khuyen': 'Rất tốt cho cầu tài, đầu tư'},
    'Thương Môn': {'cat_hung': 'Hung', 'y_nghia': 'Cãi vã, đòi nợ, kiện cáo, xung đột', 'loi_khuyen': 'Cẩn thận tranh chấp, thị phi'},
    'Đỗ Môn': {'cat_hung': 'Bình', 'y_nghia': 'Phòng thủ, ẩn náu, kỹ thuật, bí mật', 'loi_khuyen': 'Nên giữ bí mật, phòng thủ'},
    'Cảnh Môn': {'cat_hung': 'Bình', 'y_nghia': 'Văn thư, thi cử, yến tiệc, thông tin', 'loi_khuyen': 'Thuận lợi cho thi cử, giấy tờ'},
    'Tử Môn': {'cat_hung': 'Đại Hung', 'y_nghia': 'Chấm dứt, nguy hiểm, tang lễ, kết thúc', 'loi_khuyen': 'Bất lợi mọi việc, nên tránh'},
    'Kinh Môn': {'cat_hung': 'Hung', 'y_nghia': 'Kiện tụng, tranh cãi, sợ hãi, báo động', 'loi_khuyen': 'Cẩn thận pháp lý, xung đột'},
}

THAN_GIAI_THICH = {
    'Trực Phù': {'tinh_chat': 'Quý nhân tối cao, thần che chở → Rất CÁT, được người trên giúp đỡ'},
    'Đằng Xà': {'tinh_chat': 'Dây dưa, thần quỷ, biến hóa → Cẩn thận lừa gạt, ảo giác, sự rối rắm'},
    'Thái Âm': {'tinh_chat': 'Ẩn tàng, mưu kế, giúp đỡ kín đáo → Có người âm thầm hỗ trợ'},
    'Lục Hợp': {'tinh_chat': 'Hợp tác, hôn nhân, hòa hợp → Tốt cho quan hệ, hợp tác'},
    'Bạch Hổ': {'tinh_chat': 'Binh khí, tai ương, hình phạt → Cẩn thận tai nạn, xung đột'},
    'Huyền Vũ': {'tinh_chat': 'Trộm cắp, lừa dối, ám muội → Phòng bị mất mát, gian lận'},
    'Cửu Địa': {'tinh_chat': 'Tĩnh, chậm chạp, ẩn náu → Nên kiên nhẫn, chờ đợi'},
    'Cửu Thiên': {'tinh_chat': 'Động, cao xa, xuất chinh → Thuận lợi hành động, di chuyển'},
}

# === 12 TRƯỜNG SINH ENGINE (V8.0) ===
TRUONG_SINH_STAGES = ['Trường Sinh', 'Mộc Dục', 'Quan Đới', 'Lâm Quan', 'Đế Vượng',
                       'Suy', 'Bệnh', 'Tử', 'Mộ', 'Tuyệt', 'Thai', 'Dưỡng']

TRUONG_SINH_START = {'Mộc': 'Hợi', 'Hỏa': 'Dần', 'Kim': 'Tị', 'Thủy': 'Thân', 'Thổ': 'Thân'}

CHI_ORDER = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

TRUONG_SINH_GIAI_THICH = {
    'Trường Sinh': '🌱 Khởi đầu, được nuôi dưỡng → Sự việc MỚI BẮT ĐẦU, tiềm năng tốt',
    'Mộc Dục': '🛁 Tắm rửa, chưa ổn định → Giai đoạn CHAO ĐẢO, cần kiên nhẫn',
    'Quan Đới': '👑 Đội mũ, chuẩn bị → Sự việc đang CHUẨN BỊ phát triển',
    'Lâm Quan': '🏛️ Nhậm chức, phát triển → Sự việc đang PHÁT TRIỂN MẠNH',
    'Đế Vượng': '👑 Cực thịnh, đỉnh cao → ĐỈNH CAO, nhưng thịnh cực tắc suy',
    'Suy': '📉 Bắt đầu suy giảm → Sự việc đang GIẢM SÚT, cần điều chỉnh',
    'Bệnh': '🏥 Bệnh tật, yếu đuối → GẶP KHÓ KHĂN, cần chữa trị',
    'Tử': '💀 Chết, kết thúc → CHẤM DỨT hoặc rất khó khăn',
    'Mộ': '⚰️ Chôn cất, ẩn tàng → ẨN GIẤU, cất kho, tạm dừng',
    'Tuyệt': '❌ Tuyệt diệt → HOÀN TOÀN KẾT THÚC',
    'Thai': '🤰 Mang thai, hình thành → Đang THAI NGHÉN, manh nha',
    'Dưỡng': '🍼 Nuôi dưỡng, chờ đợi → Đang NUÔI DƯỠNG, sắp khởi phát',
}

def _get_truong_sinh(hanh, chi):
    """Trả về (giai đoạn, giải thích) của hành tại chi"""
    if not hanh or not chi or hanh not in TRUONG_SINH_START:
        return None, None
    start_chi = TRUONG_SINH_START[hanh]
    if start_chi not in CHI_ORDER or chi not in CHI_ORDER:
        return None, None
    start_idx = CHI_ORDER.index(start_chi)
    chi_idx = CHI_ORDER.index(chi)
    stage_idx = (chi_idx - start_idx) % 12
    stage = TRUONG_SINH_STAGES[stage_idx]
    return stage, TRUONG_SINH_GIAI_THICH.get(stage, '')

# === V21.0: LƯỢNG HÓA LỰC LƯỢNG — POWER SCORE 12 TRƯỜNG SINH ===
TRUONG_SINH_POWER = {
    # V32.6: Chia đều 0-100 tuổi theo 12 Trường Sinh
    'Trường Sinh': {'power': 70, 'cap': '🟢 MẠNH',      'con_nguoi': 'Trẻ sơ sinh khỏe mạnh (0-5 tuổi)', 'vat': 'MỚI, SẠCH, BẮT ĐẦU', 'tuoi_min': 0, 'tuoi_max': 5},
    'Mộc Dục':     {'power': 50, 'cap': '🟡 TRUNG',      'con_nguoi': 'Trẻ nhỏ chưa tự lập (6-12 tuổi)', 'vat': 'CHƯA HOÀN CHỈNH, DAO ĐỘNG', 'tuoi_min': 6, 'tuoi_max': 12},
    'Quan Đới':    {'power': 65, 'cap': '🔵 KHÁ',        'con_nguoi': 'Thiếu niên chuẩn bị trưởng thành (13-18 tuổi)', 'vat': 'GẦN MỚI, ĐANG CHUẨN BỊ', 'tuoi_min': 13, 'tuoi_max': 18},
    'Lâm Quan':    {'power': 85, 'cap': '🟢 CỰC MẠNH',  'con_nguoi': 'Thanh niên sung sức (19-32 tuổi)', 'vat': 'LỚN, MỚI, TỐT, NHIỀU', 'tuoi_min': 19, 'tuoi_max': 32},
    'Đế Vượng':    {'power': 100,'cap': '🟢 ĐỈNH CAO',  'con_nguoi': 'Trung niên cường thịnh đỉnh cao (33-45 tuổi)', 'vat': 'LỚN NHẤT, MỚI NHẤT, NHIỀU NHẤT', 'tuoi_min': 33, 'tuoi_max': 45},
    'Suy':         {'power': 40, 'cap': '🟠 YẾU',        'con_nguoi': 'Người bắt đầu suy giảm (46-55 tuổi)', 'vat': 'CŨ, NHỎ HƠN, GIẢM SÚT', 'tuoi_min': 46, 'tuoi_max': 55},
    'Bệnh':        {'power': 25, 'cap': '🟠 RẤT YẾU',   'con_nguoi': 'Người già yếu bệnh (56-65 tuổi)', 'vat': 'HƯ HỎNG, THIẾU, CẦN SỬA', 'tuoi_min': 56, 'tuoi_max': 65},
    'Tử':          {'power': 10, 'cap': '🔴 CHẾT',       'con_nguoi': 'Người rất già hoặc đã mất (66-75 tuổi)', 'vat': 'NHỎ NHẤT, HƯ HỎNG, VỠ NÁT', 'tuoi_min': 66, 'tuoi_max': 75},
    'Mộ':          {'power': 30, 'cap': '🟠 MỘ KHỐ',     'con_nguoi': 'Ẩn khuất, cất giữ (76-85 tuổi)', 'vat': 'CẤT KHO, ẨN GIẤU, BỊ GIỮ LẠI', 'tuoi_min': 76, 'tuoi_max': 85},
    'Tuyệt':       {'power': 5,  'cap': '🔴 TUYỆT',     'con_nguoi': 'Tuyệt diệt, không còn (86-100 tuổi)', 'vat': 'KHÔNG CÒN, ĐÃ MẤT, MÒN NÁT', 'tuoi_min': 86, 'tuoi_max': 100},
    'Thai':        {'power': 35, 'cap': '🟡 MANH NHA',   'con_nguoi': 'Chưa sinh, đang hình thành', 'vat': 'RẤT NHỎ, CHƯA RÕ RÀNG', 'tuoi_min': 0, 'tuoi_max': 0},
    'Dưỡng':       {'power': 55, 'cap': '🟡 NUÔI DƯỠNG','con_nguoi': 'Sắp ra đời, đang nuôi dưỡng', 'vat': 'NHỎ, ĐANG PHÁT TRIỂN', 'tuoi_min': 0, 'tuoi_max': 2},
}

# V21.0: NGŨ KHÍ POWER — Vượng Tướng Hưu Tù Tử
NGU_KHI_POWER = {
    'Vượng': {'power': 100, 'label': 'CỰC VƯỢNG'},
    'Tướng': {'power': 80,  'label': 'TƯỚNG'},
    'Hưu':   {'power': 50,  'label': 'HƯU (nghỉ)'},
    'Tù':    {'power': 25,  'label': 'TÙ (giam)'},
    'Tử':    {'power': 10,  'label': 'TỬ (chết)'},
}

# V21.0: % LỰC LƯỢNG → MAPPING VẠN VẬT + VÒNG ĐỜI CON NGƯỜI
STRENGTH_TO_VAN_VAT = {
    'CỰC_VƯỢNG': {
        'range': (85, 100), 'cap': '🟢 CỰC VƯỢNG',
        'con_nguoi': 'Trung niên cường thịnh đỉnh cao (33-45 tuổi)',
        'kich_thuoc': 'Rất lớn, to, cao, đồ sộ', 'tinh_trang': 'Mới tinh, hoàn hảo, đẹp',
        'so_luong': 'Rất nhiều, dồi dào, dư thừa', 'chat_luong': 'Thượng hạng, đắt tiền',
        'mau_sac': 'Sáng, rực rỡ, tươi', 'toc_do': 'Rất nhanh, tức thì', 'so': '9-10',
    },
    'VƯỢNG': {
        'range': (70, 84), 'cap': '🔵 VƯỢNG',
        'con_nguoi': 'Thanh niên sung sức (19-32 tuổi)',
        'kich_thuoc': 'Lớn, to, rộng', 'tinh_trang': 'Mới, tốt, ít lỗi',
        'so_luong': 'Nhiều, đủ dùng', 'chat_luong': 'Tốt, chất lượng cao',
        'mau_sac': 'Sáng, tươi, đẹp', 'toc_do': 'Nhanh, kịp thời', 'so': '7-8',
    },
    'TRUNG_BÌNH': {
        'range': (50, 69), 'cap': '🟡 TRUNG BÌNH',
        'con_nguoi': 'Thiếu niên hoặc người trung niên (13-18 / 46-55 tuổi)',
        'kich_thuoc': 'Trung bình, vừa phải', 'tinh_trang': 'Bình thường, dùng được',
        'so_luong': 'Vừa phải, đủ', 'chat_luong': 'Trung bình, tạm',
        'mau_sac': 'Bình thường', 'toc_do': 'Trung bình, chờ đợi', 'so': '5-6',
    },
    'SUY': {
        'range': (30, 49), 'cap': '🟠 SUY',
        'con_nguoi': 'Người bắt đầu suy giảm (56-65 tuổi)',
        'kich_thuoc': 'Nhỏ, hẹp, thấp', 'tinh_trang': 'Cũ, hao mòn, xuống cấp',
        'so_luong': 'Ít, thiếu, không đủ', 'chat_luong': 'Kém, giảm giá trị',
        'mau_sac': 'Nhạt, phai, xỉn', 'toc_do': 'Chậm, trì trệ', 'so': '3-4',
    },
    'RẤT_YẾU': {
        'range': (15, 29), 'cap': '🟠 RẤT YẾU',
        'con_nguoi': 'Người rất già hoặc đã mất (66-75 tuổi)',
        'kich_thuoc': 'Rất nhỏ', 'tinh_trang': 'Hư hỏng, nứt vỡ',
        'so_luong': 'Rất ít, gần hết', 'chat_luong': 'Rất tệ, hàng lỗi',
        'mau_sac': 'Tối, bạc, xám', 'toc_do': 'Rất chậm', 'so': '1-2',
    },
    'TỬ_TUYỆT': {
        'range': (0, 14), 'cap': '🔴 TỬ/TUYỆT',
        'con_nguoi': 'Tuyệt diệt, không còn sức sống (76-100 tuổi)',
        'kich_thuoc': 'Không đáng kể, tan rã', 'tinh_trang': 'Vỡ nát, bỏ đi, phế liệu',
        'so_luong': 'Không có, 0, đã hết', 'chat_luong': 'Đồ bỏ, không giá trị',
        'mau_sac': 'Đen, tối, mất màu', 'toc_do': 'Không, đình trệ', 'so': '0',
    },
}

def _get_van_vat_from_pct(pct):
    """V21.0: Từ % lực lượng → trả về mapping vạn vật + con người"""
    pct = max(0, min(100, pct))
    for key, data in STRENGTH_TO_VAN_VAT.items():
        lo, hi = data['range']
        if lo <= pct <= hi:
            return key, data
    return 'TỬ_TUYỆT', STRENGTH_TO_VAN_VAT['TỬ_TUYỆT']


def _get_van_vat_by_hanh(hanh_dt, weighted_pct):
    """
    V35.6: Lấy Vạn Vật CỤ THỂ theo HÀNH của Dụng Thần + sức mạnh.
    - hỏi vợ → Thê Tài → Kim → VAN_VAT_CU_THE['Kim']['VƯỢNG']
    - hỏi nhà → Phụ Mẫu → Thổ → VAN_VAT_CU_THE['Thổ']['VƯỢNG']
    Mỗi DT khác nhau → Ngũ Hành khác → Vạn Vật hoàn toàn khác!
    """
    # Xác định tầng sức mạnh từ weighted_pct
    if weighted_pct >= 75:
        tang = 'CỰC_VƯỢNG'
    elif weighted_pct >= 55:
        tang = 'VƯỢNG'
    elif weighted_pct >= 40:
        tang = 'TRUNG_BÌNH'
    elif weighted_pct >= 20:
        tang = 'SUY'
    else:
        tang = 'CỰC_SUY'
    
    # Lấy data theo Hành + Tầng
    hanh_data = VAN_VAT_CU_THE.get(hanh_dt, VAN_VAT_CU_THE.get('Thổ', {}))
    tang_data = hanh_data.get(tang, hanh_data.get('TRUNG_BÌNH', {}))
    
    # Lấy thêm Ngũ Hành Vật Chất
    vat_chat = NGU_HANH_VAT_CHAT.get(hanh_dt, {})
    
    return tang, tang_data, vat_chat


def _calc_ngu_khi(hanh_chu, hanh_cung):
    """V21.0: Tính Ngũ Khí (Vượng/Tướng/Hưu/Tù/Tử) của hành chủ tại cung"""
    if not hanh_chu or not hanh_cung or hanh_chu == '?' or hanh_cung == '?':
        return 'Hưu', 50
    if hanh_chu == hanh_cung:
        return 'Vượng', 100
    if SINH.get(hanh_cung) == hanh_chu:
        return 'Tướng', 80
    if SINH.get(hanh_chu) == hanh_cung:
        return 'Hưu', 50
    if KHAC.get(hanh_chu) == hanh_cung:
        return 'Tù', 25
    if KHAC.get(hanh_cung) == hanh_chu:
        return 'Tử', 10
    return 'Hưu', 50

# V21.0: NGŨ HÀNH → ĐẶC TÍNH VẬT CHẤT (hình dáng, chất liệu, màu sắc)
NGU_HANH_VAT_CHAT = {
    'Kim': {'hinh': 'Tròn, cầu', 'chat_lieu': 'Kim loại, thép, vàng, bạc', 'mau': 'Trắng, xám bạc', 'huong': 'Tây', 'vi': 'Cay', 'co_the': 'Phổi, hô hấp, da'},
    'Mộc': {'hinh': 'Dài, thẳng, hình chữ nhật', 'chat_lieu': 'Gỗ, tre, cây', 'mau': 'Xanh lá', 'huong': 'Đông', 'vi': 'Chua', 'co_the': 'Gan, mắt, gân'},
    'Thủy': {'hinh': 'Không cố định, lượn sóng', 'chat_lieu': 'Nước, lỏng, dầu', 'mau': 'Đen, tối', 'huong': 'Bắc', 'vi': 'Mặn', 'co_the': 'Thận, bàng quang, xương'},
    'Hỏa': {'hinh': 'Nhọn, tam giác', 'chat_lieu': 'Điện, lửa, nhựa', 'mau': 'Đỏ, hồng', 'huong': 'Nam', 'vi': 'Đắng', 'co_the': 'Tim, huyết mạch, lưỡi'},
    'Thổ': {'hinh': 'Vuông, bàn phẳng, dày', 'chat_lieu': 'Đất, gạch, xi măng', 'mau': 'Vàng, nâu', 'huong': 'Trung tâm', 'vi': 'Ngọt', 'co_the': 'Dạ dày, lá lách, cơ bắp'},
}

# V26.2: VẠN VẬT CỤ THỂ = NGŨ HÀNH × TẦNG VƯỢNG SUY
# Kết hợp chất liệu (Ngũ Hành) + tình trạng (Tầng) → đồ vật cụ thể
VAN_VAT_CU_THE = {
    'Kim': {
        'CỰC_VƯỢNG': {
            'do_vat': 'Vàng ròng mới đúc, đồng hồ Rolex, xe hơi mới tinh, trang sức kim cương, kiếm thép bén sáng',
            'nha_cua': 'Biệt thự mái vòm, tòa nhà kính thép mới, két sắt lớn',
            'nguoi': 'Tướng quân, quan chức cấp cao, doanh nhân thành đạt',
            'benh': 'Phổi khỏe mạnh, hô hấp tốt, hệ miễn dịch mạnh',
        },
        'VƯỢNG': {
            'do_vat': 'Xe máy mới, điện thoại mới, dao kéo bén, nồi inox mới, đồng hồ tốt',
            'nha_cua': 'Nhà mái tôn mới, cổng sắt mới sơn, cửa nhôm kính',
            'nguoi': 'Người quyền lực, kỷ luật, có uy quyền',
            'benh': 'Phổi tốt, da đẹp, xương chắc khỏe',
        },
        'TRUNG_BÌNH': {
            'do_vat': 'Xe đạp cũ còn dùng được, đồng hồ bình thường, dao còn bén, nồi niêu dùng được',
            'nha_cua': 'Nhà mái tôn bình thường, cổng sắt xuống cấp nhẹ',
            'nguoi': 'Nhân viên văn phòng, công chức bình thường',
            'benh': 'Phổi bình thường, dễ viêm họng nhẹ',
        },
        'SUY': {
            'do_vat': 'Dao kéo cùn, đồng hồ chạy sai, xe cũ hay hỏng, nồi móp méo, điện thoại cũ',
            'nha_cua': 'Mái tôn dột, cổng sắt rỉ, cửa kính nứt',
            'nguoi': 'Người mất quyền lực, nghỉ hưu, bị giáng chức',
            'benh': 'Viêm phổi nhẹ, ho kéo dài, da khô nứt',
        },
        'RẤT_YẾU': {
            'do_vat': 'Sắt vụn rỉ sét, dao gãy, đồng hồ hỏng, phế liệu kim loại',
            'nha_cua': 'Mái tôn thủng, khung sắt gãy, nhà hoang cổng sắt',
            'nguoi': 'Người bệnh phổi nặng, tù nhân, mất tự do',
            'benh': 'Ung thư phổi, lao phổi, bệnh da nặng',
        },
        'TỬ_TUYỆT': {
            'do_vat': 'Kim loại tan rã, rỉ sét hoàn toàn, đồ vỡ không sửa được',
            'nha_cua': 'Đống sắt phế liệu, nhà đổ nát chỉ còn khung sắt',
            'nguoi': 'Người đã chết vì bệnh phổi, xương',
            'benh': 'Tử vong do phổi, hô hấp suy hết',
        },
    },
    'Mộc': {
        'CỰC_VƯỢNG': {
            'do_vat': 'Bàn ghế gỗ quý mới (gụ, trắc, hương), cây cổ thụ sum suê, sách mới in đẹp',
            'nha_cua': 'Nhà sàn gỗ lớn, rừng cây xanh tốt, vườn cây sai quả',
            'nguoi': 'Giáo sư, nhà văn nổi tiếng, quan tòa, người nhân từ',
            'benh': 'Gan khỏe, mắt sáng, gân cốt dẻo dai',
        },
        'VƯỢNG': {
            'do_vat': 'Bàn ghế gỗ tốt, cây xanh tươi, sách vở mới, gậy tre khỏe',
            'nha_cua': 'Nhà gỗ đẹp, sân vườn cây xanh, hàng rào tre',
            'nguoi': 'Thầy giáo, nhà nghiên cứu, người hiền lành',
            'benh': 'Gan tốt, mắt sáng, xương khớp linh hoạt',
        },
        'TRUNG_BÌNH': {
            'do_vat': 'Bàn ghế gỗ thường, cây cối bình thường, sách cũ còn đọc được, giấy tờ',
            'nha_cua': 'Nhà gỗ bình thường, vườn tạp',
            'nguoi': 'Giáo viên cấp 2, nhân viên hành chính',
            'benh': 'Gan hoạt động bình thường, mắt hơi mờ',
        },
        'SUY': {
            'do_vat': 'Bàn ghế gỗ cũ lung lay, cây héo úa, sách rách, giấy ố vàng',
            'nha_cua': 'Nhà gỗ mục, vườn cỏ dại, hàng rào tre gãy',
            'nguoi': 'Giáo viên về hưu, người thất học, trẻ em bỏ học',
            'benh': 'Gan yếu, mắt mờ, gân cốt cứng đau nhức',
        },
        'RẤT_YẾU': {
            'do_vat': 'Gỗ mục nát, cây chết khô, sách mốc rách nát, tre gãy mục',
            'nha_cua': 'Nhà gỗ sập, vườn hoang cỏ chết',
            'nguoi': 'Người bệnh gan nặng, mù lòa',
            'benh': 'Xơ gan, u gan, mù mắt, gân cốt teo',
        },
        'TỬ_TUYỆT': {
            'do_vat': 'Gỗ mục thành bùn, cây chết rục, giấy tờ tan rã',
            'nha_cua': 'Đống gỗ mục, nền nhà cũ chỉ còn đất',
            'nguoi': 'Người đã chết vì bệnh gan',
            'benh': 'Tử vong do gan, mật suy hết',
        },
    },
    'Thủy': {
        'CỰC_VƯỢNG': {
            'do_vat': 'Bể cá lớn sang trọng, xe sang chạy dầu, hồ bơi, thuyền du lịch, rượu quý',
            'nha_cua': 'Biệt thự ven sông, nhà mặt biển, hồ nước lớn',
            'nguoi': 'Nhà ngoại giao, thương gia quốc tế, triết gia',
            'benh': 'Thận khỏe, bàng quang tốt, xương chắc',
        },
        'VƯỢNG': {
            'do_vat': 'Bình nước mới, máy lọc nước, chai dầu tốt, mực in mới, cá cảnh đẹp',
            'nha_cua': 'Nhà gần sông suối, giếng nước trong, bể nước đầy',
            'nguoi': 'Người thông minh lanh lợi, du khách, ngư dân giàu',
            'benh': 'Thận tốt, bàng quang khỏe, xương cốt dẻo',
        },
        'TRUNG_BÌNH': {
            'do_vat': 'Chai nước bình thường, bình thủy cũ, xô chậu dùng được',
            'nha_cua': 'Nhà bình thường gần ao, giếng bình thường',
            'nguoi': 'Nhân viên bình thường, người lao động',
            'benh': 'Thận bình thường, dễ đi tiểu đêm',
        },
        'SUY': {
            'do_vat': 'Bình nước rò rỉ, ống dẫn nước cũ, mực in cạn, xô chậu nứt',
            'nha_cua': 'Nhà bị dột, giếng cạn, cống rãnh tắc',
            'nguoi': 'Người lún bún, thiếu quyết đoán, nghiện rượu',
            'benh': 'Thận yếu, phù chân, đau lưng, đi tiểu khó',
        },
        'RẤT_YẾU': {
            'do_vat': 'Ống nước vỡ, bể cá nứt, dầu cặn, nước thối',
            'nha_cua': 'Nhà ngập úng, giếng khô, cống vỡ',
            'nguoi': 'Người bệnh thận nặng, vô gia cư',
            'benh': 'Suy thận, sỏi thận, xương giòn gãy',
        },
        'TỬ_TUYỆT': {
            'do_vat': 'Nước khô cạn hoàn toàn, bể vỡ nát, ống rỉ thủng',
            'nha_cua': 'Vùng sa mạc khô hạn, giếng chết',
            'nguoi': 'Người tử vong do thận, đuối nước',
            'benh': 'Tử vong do suy thận, mất nước',
        },
    },
    'Hỏa': {
        'CỰC_VƯỢNG': {
            'do_vat': 'Đèn pha siêu sáng, bếp gas mới, TV OLED lớn, điện thoại flagship, pháo hoa',
            'nha_cua': 'Nhà lầu nhiều đèn sáng, tòa nhà kính lấp lánh',
            'nguoi': 'Minh tinh, MC nổi tiếng, chính trị gia danh tiếng',
            'benh': 'Tim mạch khỏe, huyết áp tốt, mắt sáng rõ',
        },
        'VƯỢNG': {
            'do_vat': 'Bếp điện mới, đèn LED, nến đẹp, máy tính chạy tốt, bật lửa mới',
            'nha_cua': 'Nhà ấm áp sáng sủa, bếp gas mới',
            'nguoi': 'Người nổi bật, tự tin, lãnh đạo truyền cảm',
            'benh': 'Tim mạch tốt, huyết áp ổn',
        },
        'TRUNG_BÌNH': {
            'do_vat': 'Bóng đèn bình thường, bếp cũ còn dùng được, nến vừa, bật lửa cũ',
            'nha_cua': 'Nhà ấm vừa, bếp bình thường',
            'nguoi': 'Người bình thường, hơi nóng tính',
            'benh': 'Tim bình thường, huyết áp dao động nhẹ',
        },
        'SUY': {
            'do_vat': 'Bóng đèn mờ nhấp nháy, bếp gas cũ hay tắt, nến gần cháy hết, pin yếu',
            'nha_cua': 'Nhà tối tăm, bếp hỏng, quạt cũ kêu',
            'nguoi': 'Người mất danh tiếng, hay lo lắng bất an',
            'benh': 'Tim đập nhanh, huyết áp cao nhẹ, mất ngủ',
        },
        'RẤT_YẾU': {
            'do_vat': 'Đèn cháy bóng, bếp hỏng hoàn toàn, pin hết, dây điện chập',
            'nha_cua': 'Nhà mất điện, bếp nguội lạnh',
            'nguoi': 'Người trầm cảm, bị cô lập, mất mọi danh tiếng',
            'benh': 'Suy tim, rối loạn nhịp tim, thiếu máu',
        },
        'TỬ_TUYỆT': {
            'do_vat': 'Than tàn, đèn vỡ nát, bếp bị bỏ hoang, tro tàn',
            'nha_cua': 'Nhà cháy trụi, chỉ còn tro than',
            'nguoi': 'Người chết vì tim, đột quỵ',
            'benh': 'Tử vong do tim mạch, đột quỵ',
        },
    },
    'Thổ': {
        'CỰC_VƯỢNG': {
            'do_vat': 'Tòa nhà bê tông mới, gốm sứ cao cấp, đá quý ngọc bích, gạch men đẹp',
            'nha_cua': 'Biệt thự đất rộng, khu đô thị mới, sân vườn rộng lớn',
            'nguoi': 'Đại gia bất động sản, nông dân giàu có, chủ mỏ',
            'benh': 'Dạ dày khỏe, tiêu hóa tốt, cơ bắp chắc nịch',
        },
        'VƯỢNG': {
            'do_vat': 'Chén bát mới, gạch ốp đẹp, đồ gốm tốt, xi măng mới, tường mới xây',
            'nha_cua': 'Nhà gạch mới xây, sân gạch sạch, vườn đất tốt',
            'nguoi': 'Nông dân mùa bội thu, nhà thầu xây dựng',
            'benh': 'Dạ dày tốt, tiêu hóa mạnh, ăn ngon ngủ yên',
        },
        'TRUNG_BÌNH': {
            'do_vat': 'Chén bát cũ còn dùng, gạch bình thường, đồ gốm thường',
            'nha_cua': 'Nhà gạch bình thường, sân đất',
            'nguoi': 'Nông dân bình thường, công nhân xây dựng',
            'benh': 'Dạ dày bình thường, hay đầy bụng',
        },
        'SUY': {
            'do_vat': 'Chén bát sứt mẻ, gạch vỡ, tường nứt, gốm cũ bạc màu',
            'nha_cua': 'Nhà gạch cũ nứt tường, sân đất lầy lội',
            'nguoi': 'Nông dân mất mùa, thợ xây thất nghiệp',
            'benh': 'Viêm dạ dày, đau bụng, cơ bắp yếu nhão',
        },
        'RẤT_YẾU': {
            'do_vat': 'Gạch vỡ vụn, gốm nứt không dùng được, đồ đất sét nát',
            'nha_cua': 'Tường sập, nền nhà lún, đất sạt lở',
            'nguoi': 'Người bệnh dạ dày nặng, suy dinh dưỡng',
            'benh': 'Loét dạ dày, u bướu, teo cơ',
        },
        'TỬ_TUYỆT': {
            'do_vat': 'Đống gạch vụn, đất bỏ hoang, gốm tan nát thành bụi',
            'nha_cua': 'Nhà đổ nát thành đống gạch, đất bỏ hoang không ai ở',
            'nguoi': 'Người chết vì dạ dày, ung thư tạng',
            'benh': 'Tử vong do tạng phủ suy hết',
        },
    },
}

def _get_van_vat_cu_the(hanh, tier_key):
    """V26.2: Lấy mô tả vạn vật CỤ THỂ từ Ngũ Hành + Tầng Vượng Suy"""
    hanh_data = VAN_VAT_CU_THE.get(hanh, {})
    return hanh_data.get(tier_key, {})

# V21.0: MULTI-LAYER STRENGTH TIER — Tập hợp 3 tầng để ra tầng cuối
def _calc_unified_strength_tier(lh_raw=0, ts_stage=None, ngu_khi=None, hanh_dt=None):
    """
    Tập hợp 3 nguồn:
    1. LH raw score (→ normalize 0-100) — Trọng số 50%
    2. 12 Trường Sinh stage (→ power 0-100) — Trọng số 30%
    3. Ngũ Khí (→ power 0-100) — Trọng số 20%
    → unified_pct → tầng vạn vật + ngũ hành vật chất
    """
    # LH normalize: [-40,+40] → [0,100]
    lh_pct = max(0, min(100, int(50 + (lh_raw / 40) * 50)))
    
    # Trường Sinh power
    ts_pct = TRUONG_SINH_POWER.get(ts_stage, {}).get('power', 50) if ts_stage else 50
    
    # Ngũ Khí power
    nk_pct = NGU_KHI_POWER.get(ngu_khi, {}).get('power', 50) if ngu_khi else 50
    
    # Weighted: LH 50%, TS 30%, NK 20%
    unified_pct = int(lh_pct * 0.50 + ts_pct * 0.30 + nk_pct * 0.20)
    unified_pct = max(0, min(100, unified_pct))
    
    # Lấy tầng vạn vật tương ứng
    vv_key, vv_data = _get_van_vat_from_pct(unified_pct)
    
    # Lấy đặc tính vật chất theo Ngũ Hành
    hanh_vat = NGU_HANH_VAT_CHAT.get(hanh_dt, {})
    
    # Thêm TS + NK detail
    ts_info = TRUONG_SINH_POWER.get(ts_stage, {}) if ts_stage else {}
    nk_info = NGU_KHI_POWER.get(ngu_khi, {}) if ngu_khi else {}
    
    return {
        'unified_pct': unified_pct,
        'lh_pct': lh_pct,
        'ts_pct': ts_pct,
        'nk_pct': nk_pct,
        'tier_key': vv_key,
        'tier_data': vv_data,
        'hanh_vat': hanh_vat,
        'ts_stage': ts_stage,
        'ts_info': ts_info,
        'ngu_khi': ngu_khi,
        'nk_info': nk_info,
    }

# === NẠP ÂM GIẢI THÍCH (V8.0) ===
NAP_AM_GIAI_THICH = {
    'Hải Trung Kim': 'Vàng trong biển → Tiềm lực ẨN GIẤU, cần thời cơ',
    'Lô Trung Hỏa': 'Lửa trong lò → Năng lượng BỊ KIỀM CHẾ, cần môi trường phù hợp',
    'Đại Lâm Mộc': 'Gỗ rừng lớn → Sức mạnh TO LỚN, phát triển bền vững',
    'Lộ Bàng Thổ': 'Đất ven đường → BÌNH THƯỜNG, không nổi bật',
    'Kiếm Phong Kim': 'Vàng mũi kiếm → Sắc bén, QUYẾT ĐOÁN',
    'Sơn Đầu Hỏa': 'Lửa trên núi → DANH TIẾNG cao, nhưng dễ tắt',
    'Giản Hạ Thủy': 'Nước dưới khe → ẨN MÌNH, bền bỉ',
    'Thành Đầu Thổ': 'Đất trên thành → VỮNG CHẮC, an toàn',
    'Bạch Lạp Kim': 'Vàng nến trắng → ĐẸP nhưng dễ hao tổn',
    'Dương Liễu Mộc': 'Gỗ cây liễu → MỀM MẠI, thích nghi tốt',
    'Tuyền Trung Thủy': 'Nước suối → TINH KHIẾT, nguồn lực dồi dào',
    'Ốc Thượng Thổ': 'Đất trên mái → BẢO VỆ, che chở',
    'Tích Lịch Hỏa': 'Lửa sấm sét → MẠNH MẼ, bùng nổ ngắn hạn',
    'Tùng Bách Mộc': 'Gỗ tùng bách → BỀN BỈ, kiên cường',
    'Trường Lưu Thủy': 'Nước chảy dài → KIÊN TRÌ, không ngừng tiến',
    'Sa Trung Kim': 'Vàng trong cát → Quý nhưng cần TÌM KIẾM',
    'Sơn Hạ Hỏa': 'Lửa dưới núi → SẮP BÙNG PHÁT, chờ thời cơ',
    'Bình Địa Mộc': 'Gỗ đất bằng → ỔN ĐỊNH, phát triển đều',
    'Bích Thượng Thổ': 'Đất trên tường → TRANG TRÍ, chú trọng bên trong',
    'Kim Bạc Kim': 'Vàng lá mỏng → ĐẸP nhưng MỎNG MANH',
    'Phúc Đăng Hỏa': 'Lửa đèn phủ → ẨN GIẤU, cần hỗ trợ',
    'Thiên Hà Thủy': 'Nước sông trời → CAO QUÝ, khan hiếm',
    'Đại Trạch Thổ': 'Đất bãi lớn → RỘNG RÃI, thuận mở rộng',
    'Thoa Xuyến Kim': 'Vàng trang sức → SANG TRỌNG, hưởng thụ',
    'Tang Đố Mộc': 'Gỗ cây dâu → THỰC DỤNG, tốt cho sinh kế',
    'Đại Khê Thủy': 'Nước khe lớn → DỒI DÀO, cẩn thận lũ',
    'Sa Trung Thổ': 'Đất trong cát → KHÔNG ỔN ĐỊNH, cần gia cố',
    'Thiên Thượng Hỏa': 'Lửa trên trời → RẠNG RỠ, vinh quang',
    'Thạch Lựu Mộc': 'Gỗ lựu đá → CỨNG CỎI, kiên định',
    'Đại Hải Thủy': 'Nước biển lớn → BAO LA, quyền lực lớn',
}

# === QUÁI Ý NGHĨA — Xem V9.0 mở rộng bên dưới ===
# (QUAI_Y_NGHIA được định nghĩa đầy đủ trong phần V9.0 với 10+ trường/quái)

# === LỤC THÂN GIẢI THÍCH (V8.0) ===
LUC_THAN_GIAI_THICH = {
    'Quan Quỷ': 'Công việc, sếp, bệnh tật, kiện tụng, áp lực',
    'Phụ Mẫu': 'Cha mẹ, nhà cửa, giấy tờ, hợp đồng, che chở',
    'Huynh Đệ': 'Anh em, bạn bè, đối thủ, cạnh tranh, hao tiền',
    'Thê Tài': 'Tiền tài, vợ, tài sản, thu nhập, đầu tư',
    'Tử Tôn': 'Con cái, may mắn, vui vẻ, giải trừ, khắc Quan Quỷ',
}


# === V9.0: LỤC HỢP / LỤC XUNG CHI ===
LUC_HOP_CHI = {'Tý': 'Sửu', 'Sửu': 'Tý', 'Dần': 'Hợi', 'Hợi': 'Dần', 'Mão': 'Tuất', 'Tuất': 'Mão',
               'Thìn': 'Dậu', 'Dậu': 'Thìn', 'Tị': 'Thân', 'Thân': 'Tị', 'Ngọ': 'Mùi', 'Mùi': 'Ngọ'}
LUC_XUNG_CHI = {'Tý': 'Ngọ', 'Ngọ': 'Tý', 'Sửu': 'Mùi', 'Mùi': 'Sửu', 'Dần': 'Thân', 'Thân': 'Dần',
                'Mão': 'Dậu', 'Dậu': 'Mão', 'Thìn': 'Tuất', 'Tuất': 'Thìn', 'Tị': 'Hợi', 'Hợi': 'Tị'}

# === V41.0: TAM HÌNH (Triple Punishment) — Cổ thư Tam Hình quy tắc ===
TAM_HINH = {
    # Vô Ân Chi Hình (Hình phạt vô ơn) — mạnh nhất
    frozenset(['Dần', 'Tị', 'Thân']): ('Vô Ân Chi Hình', '⚠️ TAI HỌA do phản bội/vong ơn — cực HUNG'),
    # Trì Thế Chi Hình (Hình cậy thế)
    frozenset(['Sửu', 'Tuất', 'Mùi']): ('Trì Thế Chi Hình', '⚠️ TAI HỌA do cậy quyền/ỷ thế — HUNG'),
    # Vô Lễ Chi Hình (Hình phạt vô lễ)
    frozenset(['Tý', 'Mão']): ('Vô Lễ Chi Hình', '⚠️ TAI HỌA do xúc phạm/vô lễ — HUNG'),
    # Tự Hình (Tự phạt)
    frozenset(['Thìn']): ('Tự Hình Thìn', '⚠️ Tự mình gây họa — bất lợi'),
    frozenset(['Ngọ']): ('Tự Hình Ngọ', '⚠️ Tự mình gây họa — bất lợi'),
    frozenset(['Dậu']): ('Tự Hình Dậu', '⚠️ Tự mình gây họa — bất lợi'),
    frozenset(['Hợi']): ('Tự Hình Hợi', '⚠️ Tự mình gây họa — bất lợi'),
}

# Tam Hình pair lookup (2 chi cũng trigger partial punishment)
TAM_HINH_PAIRS = {
    ('Dần', 'Tị'): 'Vô Ân Chi Hình (bán cục)', ('Tị', 'Thân'): 'Vô Ân Chi Hình (bán cục)',
    ('Dần', 'Thân'): 'Vô Ân Chi Hình (bán cục — xung)',
    ('Sửu', 'Tuất'): 'Trì Thế Chi Hình (bán cục)', ('Tuất', 'Mùi'): 'Trì Thế Chi Hình (bán cục)',
    ('Sửu', 'Mùi'): 'Trì Thế Chi Hình (bán cục — xung)',
    ('Tý', 'Mão'): 'Vô Lễ Chi Hình',
}

def _check_tam_hinh(chi1, chi2):
    """V41.0: Kiểm tra 2 Chi có tạo Tam Hình không.
    Returns: str mô tả hình phạt hoặc None."""
    if not chi1 or not chi2:
        return None
    # Tự Hình
    if chi1 == chi2 and chi1 in ['Thìn', 'Ngọ', 'Dậu', 'Hợi']:
        return f'Tự Hình ({chi1}) — tự mình gây họa'
    # Pair check (order-insensitive)
    pair = TAM_HINH_PAIRS.get((chi1, chi2)) or TAM_HINH_PAIRS.get((chi2, chi1))
    return pair

# === V9.0: TAM HỢP CỤC ===
TAM_HOP_CUC = {
    frozenset(['Thân', 'Tý', 'Thìn']): ('Thủy', 'Tam Hợp Thủy Cục — Tụ họp, lưu thông, trí tuệ'),
    frozenset(['Hợi', 'Mão', 'Mùi']): ('Mộc', 'Tam Hợp Mộc Cục — Phát triển, sinh sôi, nhân từ'),
    frozenset(['Dần', 'Ngọ', 'Tuất']): ('Hỏa', 'Tam Hợp Hỏa Cục — Rực rỡ, danh tiếng, nóng vội'),
    frozenset(['Tị', 'Dậu', 'Sửu']): ('Kim', 'Tam Hợp Kim Cục — Quyền lực, sắc bén, cứng rắn'),
}

# === V9.0: THIÊN CAN HỢP ===
THIEN_CAN_HOP = {'Giáp': 'Kỷ', 'Kỷ': 'Giáp', 'Ất': 'Canh', 'Canh': 'Ất',
                 'Bính': 'Tân', 'Tân': 'Bính', 'Đinh': 'Nhâm', 'Nhâm': 'Đinh', 'Mậu': 'Quý', 'Quý': 'Mậu'}

# === V9.0: THẦN SÁT TABLE ===
THAN_SAT_TABLE = {
    'cat': {
        'Thiên Ất Quý Nhân': {'chi_list': {'Giáp': ['Sửu', 'Mùi'], 'Mậu': ['Sửu', 'Mùi'], 'Canh': ['Sửu', 'Mùi'],
                                           'Ất': ['Thân', 'Tý'], 'Kỷ': ['Thân', 'Tý'],
                                           'Bính': ['Dậu', 'Hợi'], 'Đinh': ['Dậu', 'Hợi'],
                                           'Nhâm': ['Mão', 'Tị'], 'Quý': ['Mão', 'Tị'],
                                           'Tân': ['Dần', 'Ngọ']},
                              'giai_thich': '🌟 Quý Nhân phù hộ — Có người quý giúp đỡ, hóa hung thành cát'},
        'Thiên Đức': {'giai_thich': '🙏 Thiên Đức chiếu mệnh — Trời che chở, giảm nhẹ tai họa'},
        'Nguyệt Đức': {'giai_thich': '🌙 Nguyệt Đức chiếu mệnh — Phúc đức từ trăng, hóa giải hung sát'},
    },
    'hung': {
        'Dương Nhận': {'chi_map': {'Giáp': 'Mão', 'Bính': 'Ngọ', 'Mậu': 'Ngọ', 'Canh': 'Dậu', 'Nhâm': 'Tý'},
                       'giai_thich': '⚔️ Dương Nhận — Sắc bén cực độ, cẩn thận tai nạn, xung đột'},
        'Kiếp Sát': {'giai_thich': '💀 Kiếp Sát — Tai ương bất ngờ, cẩn thận mất mát'},
        'Vong Thần': {'giai_thich': '👻 Vong Thần — Mất mát, đau buồn, quên lãng'},
    }
}

# === V9.0: TUẦN KHÔNG (Không Vong) ===
TUAN_KHONG = {
    'Giáp Tý': ['Tuất', 'Hợi'], 'Giáp Tuất': ['Thân', 'Dậu'], 'Giáp Thân': ['Ngọ', 'Mùi'],
    'Giáp Ngọ': ['Thìn', 'Tị'], 'Giáp Thìn': ['Dần', 'Mão'], 'Giáp Dần': ['Tý', 'Sửu'],
}
CAN_LIST = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']

# === V15.0: DỊCH MÃ (Post Horse) — Tam Hợp Xung ===
DICH_MA_MAP = {
    'Thân': 'Dần', 'Tý': 'Dần', 'Thìn': 'Dần',   # Thủy cục → Mã tại Dần
    'Dần': 'Thân', 'Ngọ': 'Thân', 'Tuất': 'Thân', # Hỏa cục → Mã tại Thân
    'Tị': 'Hợi', 'Dậu': 'Hợi', 'Sửu': 'Hợi',     # Kim cục → Mã tại Hợi
    'Hợi': 'Tị', 'Mão': 'Tị', 'Mùi': 'Tị',        # Mộc cục → Mã tại Tị
}

def _get_khong_vong(can_ngay, chi_ngay):
    """V9.0: Tính Tuần Không (Không Vong) từ Can Chi ngày"""
    if not can_ngay or not chi_ngay or can_ngay not in CAN_LIST or chi_ngay not in CHI_ORDER:
        return []
    can_idx = CAN_LIST.index(can_ngay)
    chi_idx = CHI_ORDER.index(chi_ngay)
    # Tìm Giáp đầu tuần: lùi can_idx bước trên cả can và chi
    giap_chi_idx = (chi_idx - can_idx) % 12
    giap_chi = CHI_ORDER[giap_chi_idx]
    key = f"Giáp {giap_chi}"
    return TUAN_KHONG.get(key, [])

def _check_phan_phuc_ngam(can_thien, can_dia):
    """V9.0: Kiểm tra Phản Ngâm / Phục Ngâm giữa Can Thiên Bàn và Can Địa Bàn"""
    if not can_thien or not can_dia:
        return None
    if can_thien == can_dia:
        return 'PHỤC NGÂM'
    # Phản Ngâm: Can xung nhau (cùng hành đối lập)
    # Check Thiên Can xung: Giáp-Canh, Ất-Tân, Bính-Nhâm, Đinh-Quý, Mậu-Giáp (đặc biệt)
    THIEN_CAN_XUNG = {'Giáp': 'Canh', 'Canh': 'Giáp', 'Ất': 'Tân', 'Tân': 'Ất',
                      'Bính': 'Nhâm', 'Nhâm': 'Bính', 'Đinh': 'Quý', 'Quý': 'Đinh',
                      'Mậu': 'Giáp', 'Kỷ': 'Ất'}
    if THIEN_CAN_XUNG.get(can_thien) == can_dia:
        return 'PHẢN NGÂM'
    return None

def _check_tan_thoai_than(chi_dong, chi_bien):
    """V9.0: Kiểm tra Tấn Thần / Thoái Thần từ Chi hào động → Chi hào biến"""
    if not chi_dong or not chi_bien or chi_dong not in CHI_ORDER or chi_bien not in CHI_ORDER:
        return None
    dong_idx = CHI_ORDER.index(chi_dong)
    bien_idx = CHI_ORDER.index(chi_bien)
    diff = (bien_idx - dong_idx) % 12
    if diff == 1:
        return 'TẤN THẦN'  # Tiến 1 bước = phát triển
    elif diff == 11:  # Lùi 1 bước
        return 'THOÁI THẦN'  # Thoái = suy giảm
    return None

def _get_lenh_thang_hanh():
    """V9.0: Xác định Ngũ Hành vượng theo tháng hiện tại (Lệnh Tháng)"""
    now = datetime.datetime.now()
    month = now.month
    # Xuân (2,3,4) = Mộc vượng, Hạ (5,6,7) = Hỏa vượng, Thu (8,9,10) = Kim vượng, Đông (11,12,1) = Thủy vượng
    # Thổ vượng vào các tháng chuyển mùa (3,6,9,12)
    if month in [2, 3, 4]:
        return 'Mộc', 'Mùa Xuân'
    elif month in [5, 6, 7]:
        return 'Hỏa', 'Mùa Hạ'
    elif month in [8, 9, 10]:
        return 'Kim', 'Mùa Thu'
    else:
        return 'Thủy', 'Mùa Đông'

def _get_van_vat_context(quai_name, question):
    """V9.0: Lọc thông tin Vạn Vật phù hợp với câu hỏi"""
    yn = QUAI_Y_NGHIA.get(quai_name, {})
    if not yn:
        return ""
    q = question.lower() if question else ""
    parts = []
    # Luôn hiện tượng + tính chất
    parts.append(f"Tượng: {yn.get('tuong', '?')} — {yn.get('tc', '?')}")
    # Context-aware filtering
    if any(k in q for k in ['bệnh', 'ốm', 'đau', 'khỏe', 'sức khỏe', 'thuốc']):
        parts.append(f"🏥 Cơ thể: {yn.get('co_the', '?')} | Bệnh dễ mắc: {yn.get('benh', '?')}")
    if any(k in q for k in ['cha', 'mẹ', 'con', 'anh', 'em', 'bố', 'gia đình', 'vợ', 'chồng']):
        parts.append(f"👨‍👩‍👧 Gia đình: {yn.get('gia_dinh', '?')}")
    if any(k in q for k in ['hướng', 'ở đâu', 'phương', 'tìm', 'mất']):
        parts.append(f"🧭 Hướng: {yn.get('huong', '?')}")
    if any(k in q for k in ['tuổi', 'bao nhiêu', 'mấy', 'số']):
        parts.append(f"🔢 Số: {yn.get('so', '?')}")
    if any(k in q for k in ['mùa', 'thời', 'khi nào', 'tháng']):
        parts.append(f"📅 Mùa: {yn.get('mua', '?')}")
    parts.append(f"🎨 Sắc: {yn.get('sac', '?')} | Vật: {yn.get('dong_vat', '?')}")
    return "\n".join(parts)

def _get_ung_ky(hanh, verdict):
    """V9.0: Dự đoán Ứng Kỳ dựa trên Ngũ Hành"""
    ung_ky_chi = {
        'Kim': ['Thân', 'Dậu'], 'Mộc': ['Dần', 'Mão'], 'Thủy': ['Tý', 'Hợi'],
        'Hỏa': ['Ngọ', 'Tị'], 'Thổ': ['Thìn', 'Tuất', 'Sửu', 'Mùi']
    }
    if verdict == "CÁT":
        chi_list = ung_ky_chi.get(hanh, [])
        if chi_list:
            return f"Ứng nghiệm vào ngày/tháng Chi {'/'.join(chi_list)} (hành {hanh} vượng)"
    elif verdict == "HUNG":
        # Hung → chờ hành sinh để hóa giải
        for h, s in SINH.items():
            if s == hanh:
                chi_list = ung_ky_chi.get(h, [])
                if chi_list:
                    return f"Chờ ngày/tháng Chi {'/'.join(chi_list)} (hành {h} sinh {hanh}) để cải thiện"
                break
    return "Chưa xác định rõ thời điểm ứng nghiệm"


# === V42.0: ỨNG KỲ CHUYÊN SÂU — Xung/Hợp/Trị + Không Vong + Mộ ===
def _get_ung_ky_advanced(hanh_dt, verdict, chi_dt='', can_ngay='', chi_ngay='',
                         chi_thang='', ts_stage='', khong_vong_list=None):
    """V42.0: Dự đoán Ứng Kỳ chuyên sâu — 7 phương pháp kết hợp.
    
    Nguồn: phongthuythanglong.vn, phongthuytuongminh.com, tuvilyso.org
    Nguyên lý: Xung/Hợp/Trị → thời điểm ứng nghiệm
    """
    parts = []
    ung_ky_chi = {
        'Kim': ['Thân', 'Dậu'], 'Mộc': ['Dần', 'Mão'], 'Thủy': ['Tý', 'Hợi'],
        'Hỏa': ['Ngọ', 'Tị'], 'Thổ': ['Thìn', 'Tuất', 'Sửu', 'Mùi']
    }
    MO_KHO = {'Kim': 'Sửu', 'Mộc': 'Mùi', 'Thủy': 'Thìn', 'Hỏa': 'Tuất', 'Thổ': 'Tuất'}
    
    # 1. Trị (trùng hành) — hành vượng thì ứng nghiệm
    chi_list = ung_ky_chi.get(hanh_dt, [])
    if chi_list:
        parts.append(f"📅 **Trị thời:** ngày/tháng Chi {'/'.join(chi_list)} (hành {hanh_dt} vượng)")
    
    # 2. Xung — Chi xung với Chi Dụng Thần → kích hoạt sự việc
    if chi_dt and chi_dt in LUC_XUNG_CHI:
        xung_chi = LUC_XUNG_CHI[chi_dt]
        parts.append(f"⚡ **Xung kỳ:** ngày/giờ Chi {xung_chi} (xung {chi_dt} → kích hoạt)")
    
    # 3. Hợp — Chi hợp với Chi Dụng Thần → chốt kết quả
    if chi_dt and chi_dt in LUC_HOP_CHI:
        hop_chi = LUC_HOP_CHI[chi_dt]
        parts.append(f"🤝 **Hợp kỳ:** ngày/giờ Chi {hop_chi} (hợp {chi_dt} → chốt kết quả)")
    
    # 4. Không Vong → hết Không = ứng nghiệm
    if khong_vong_list and chi_dt and chi_dt in khong_vong_list:
        parts.append(f"🕳️ **Xuất Không:** chờ đến khi hết Tuần Không (gặp ngày Chi {chi_dt}) mới ứng")
    
    # 5. Nhập Mộ → cần Xung Mộ để giải thoát
    mo_chi = MO_KHO.get(hanh_dt, '')
    if ts_stage in ('Mộ', 'Tuyệt') and mo_chi:
        xung_mo = LUC_XUNG_CHI.get(mo_chi, '')
        parts.append(f"⚰️ **Xung Mộ:** DT đang {ts_stage} → chờ ngày Chi {xung_mo} (xung Mộ {mo_chi}) để phá")
    
    # 6. Can Ngày sinh/khắc → ưu tiên thời gian gần
    if can_ngay:
        hanh_ngay = CAN_NGU_HANH.get(can_ngay, '')
        if hanh_ngay and hanh_dt:
            if SINH.get(hanh_ngay) == hanh_dt:
                parts.append(f"✅ Nhật Thần ({can_ngay}={hanh_ngay}) SINH DT ({hanh_dt}) → ứng nghiệm NHANH (1-3 ngày)")
            elif KHAC.get(hanh_ngay) == hanh_dt:
                parts.append(f"⚠️ Nhật Thần ({can_ngay}={hanh_ngay}) KHẮC DT ({hanh_dt}) → ứng nghiệm CHẬM (cần chờ hành sinh)")
    
    # 7. Phán đoán gần/xa
    if verdict in ('CÁT', 'ĐẠI CÁT'):
        parts.append("🟢 Quẻ CÁT → ứng kỳ thường rơi vào thời gian Vượng/Hợp (nhanh hơn)")
    elif verdict in ('HUNG', 'ĐẠI HUNG'):
        parts.append("🔴 Quẻ HUNG → ứng kỳ khi hành Sinh đến giải cứu (chậm hơn)")
    
    if not parts:
        parts.append("Chưa xác định rõ thời điểm ứng nghiệm — cần thêm dữ liệu")
    
    return "\n".join(parts)


# === V42.0: HÓA HỒI ĐẦU PHÂN TÍCH — Biến quái chuyên sâu ===
def _analyze_hoa_hoi_dau(hanh_dong, hanh_bien, chi_dong, chi_bien,
                          can_ngay='', chi_ngay=''):
    """V42.0: Phân tích Hóa Hồi Đầu chuyên sâu cho hào biến.
    
    Nguồn: vuphac.com, art2all.net, votranh.com
    Returns: (label, description, impact) — impact: 'CÁT'/'HUNG'/'BÌNH'
    """
    results = []
    
    # 1. Hóa Hồi Đầu Sinh: hào biến sinh lại hào động
    if hanh_dong and hanh_bien and SINH.get(hanh_bien) == hanh_dong:
        results.append(('🟢 Hóa Hồi Đầu Sinh', f'{hanh_bien} sinh {hanh_dong} → Được trợ giúp mạnh mẽ, sự việc thuận lợi dần', 'CÁT'))
    
    # 2. Hóa Hồi Đầu Khắc: hào biến khắc lại hào động → RẤT XẤU
    if hanh_dong and hanh_bien and KHAC.get(hanh_bien) == hanh_dong:
        results.append(('🔴 Hóa Hồi Đầu Khắc', f'{hanh_bien} khắc {hanh_dong} → Sự việc ban đầu tốt nhưng kết quả XẤU, bị phản bội/cản trở', 'HUNG'))
    
    # 3. Hóa Mộ: Chi biến là Mộ Khố của hành hào động
    MO_KHO_MAP = {'Kim': 'Sửu', 'Mộc': 'Mùi', 'Thủy': 'Thìn', 'Hỏa': 'Tuất', 'Thổ': 'Tuất'}
    if hanh_dong and chi_bien and MO_KHO_MAP.get(hanh_dong) == chi_bien:
        results.append(('⚰️ Hóa Mộ', f'{hanh_dong} nhập mộ tại {chi_bien} → Sự việc BẾ TẮC, bị giam giữ, tạm dừng', 'HUNG'))
    
    # 4. Hóa Tuyệt: Chi biến là Tuyệt địa của hành hào động
    TUYET_MAP = {'Mộc': 'Thân', 'Hỏa': 'Hợi', 'Kim': 'Dần', 'Thủy': 'Tị', 'Thổ': 'Tị'}
    if hanh_dong and chi_bien and TUYET_MAP.get(hanh_dong) == chi_bien:
        results.append(('❌ Hóa Tuyệt', f'{hanh_dong} tuyệt tại {chi_bien} → Sự việc KHÓ THÀNH, kiệt sức, đi đến chấm dứt', 'HUNG'))
    
    # 5. Hóa Không Vong
    if chi_bien and can_ngay and chi_ngay:
        kv_list = _get_khong_vong(can_ngay, chi_ngay)
        if chi_bien in kv_list:
            results.append(('🕳️ Hóa Không Vong', f'Hào biến ({chi_bien}) rơi vào Tuần Không → Sự việc hư không, chưa thể xác định kết quả', 'HUNG'))
    
    # 6. Hóa Phản Ngâm / Phục Ngâm (Chi)
    if chi_dong and chi_bien:
        if chi_dong == chi_bien:
            results.append(('🔄 Hóa Phục Ngâm', f'{chi_dong}→{chi_bien}: Lặp lại chính mình → Trì trệ, KHÔNG TIẾN TRIỂN', 'HUNG'))
        elif chi_dong in LUC_XUNG_CHI and LUC_XUNG_CHI[chi_dong] == chi_bien:
            results.append(('⚡ Hóa Phản Ngâm', f'{chi_dong}→{chi_bien}: Đối xung → ĐẢO NGƯỢC hoàn toàn, sự việc đi ngược kỳ vọng', 'HUNG'))
    
    # 7. Hóa Hợp: Chi biến hợp Chi hào động
    if chi_dong and chi_bien and LUC_HOP_CHI.get(chi_dong) == chi_bien:
        results.append(('🤝 Hóa Hợp', f'{chi_dong} hợp {chi_bien} → Sự việc bị RÀng buộc, chưa dứt điểm', 'BÌNH'))
    
    return results


# === V42.0: ÁM ĐỘNG — Nhật xung hào tĩnh ===
def _detect_am_dong(haos, dong_hao, chi_ngay):
    """V42.0: Phát hiện Ám Động — hào tĩnh bị Nhật Thần xung.
    
    Nguồn: vuphac.com, votranh.com
    Quy tắc: Hào TĨNH (không phải hào động) mà Chi bị Nhật xung → Ám Động
    = Lực lượng ẩn tác động đến sự việc
    """
    am_dong_list = []
    if not haos or not chi_ngay:
        return am_dong_list
    
    for i, hao in enumerate(haos):
        hao_idx = i + 1
        if hao_idx in (dong_hao or []):
            continue  # Bỏ qua hào đã động
        
        chi_hao = hao.get('chi', '')
        if chi_hao and chi_hao in LUC_XUNG_CHI and LUC_XUNG_CHI.get(chi_ngay) == chi_hao:
            am_dong_list.append({
                'hao_idx': hao_idx,
                'luc_than': hao.get('luc_than', '?'),
                'can_chi': hao.get('can_chi', '?'),
                'ngu_hanh': hao.get('ngu_hanh', '?'),
                'chi': chi_hao,
                'xung_chi': chi_ngay,
            })
    return am_dong_list


# === V42.0: LỤC THẦN PHÂN TÍCH SÂU — Kết hợp Lục Thần + Lục Thân ===
LUC_THAN_DEEP = {
    'Thanh Long': {
        'hanh': 'Mộc', 'tinh_chat': 'Vui vẻ, hỷ sự, tửu sắc',
        'vuong': 'Quảng giao, ăn uống, lễ nghi, tin mừng, phát triển',
        'suy': 'Họa do tửu sắc, phóng túng, lãng phí',
        'luc_than_map': {
            'Quan Quỷ': 'Công việc vui vẻ, thăng chức có tiệc mừng',
            'Thê Tài': 'Tài lộc đến vui vẻ, thu nhập qua tiệc tùng',
            'Phụ Mẫu': 'Nhà cửa mới, giấy tờ thuận lợi',
            'Tử Tôn': 'Con cái mang lại niềm vui lớn',
            'Huynh Đệ': 'Bạn bè tụ họp vui vẻ, hao tiền tiệc tùng',
        }
    },
    'Chu Tước': {
        'hanh': 'Hỏa', 'tinh_chat': 'Thị phi, văn thư, tin tức',
        'vuong': 'Nói năng khéo léo, văn thư thuận, danh tiếng',
        'suy': 'Cãi cọ, vạ miệng, kiện tụng, thị phi',
        'luc_than_map': {
            'Quan Quỷ': 'Kiện tụng, tranh cãi công việc, bị tố cáo',
            'Thê Tài': 'Tranh chấp tiền bạc, tài sản bị kiện',
            'Phụ Mẫu': 'Giấy tờ rắc rối, hợp đồng tranh chấp',
            'Tử Tôn': 'Con cái bị thị phi, lời nói gây họa',
            'Huynh Đệ': 'Bạn bè nói xấu, anh em cãi nhau',
        }
    },
    'Câu Trần': {
        'hanh': 'Thổ', 'tinh_chat': 'Chậm chạp, cố chấp, nhà đất',
        'vuong': 'Cẩn thận, vững chắc, nhà đất tốt',
        'suy': 'Chậm trễ, bảo thủ, trì trệ, khó thay đổi',
        'luc_than_map': {
            'Quan Quỷ': 'Công việc trì trệ, chờ đợi lâu',
            'Thê Tài': 'Tiền bạc chậm đến, đầu tư lâu dài',
            'Phụ Mẫu': 'Nhà đất có vấn đề cũ, giấy tờ chậm',
            'Tử Tôn': 'Con cái chậm phát triển, cần kiên nhẫn',
            'Huynh Đệ': 'Anh em bảo thủ, khó thay đổi',
        }
    },
    'Đằng Xà': {
        'hanh': 'Thổ', 'tinh_chat': 'Lo lắng, kỳ quái, giấc mơ',
        'vuong': 'Biến hóa khôn lường, việc kỳ lạ xảy ra',
        'suy': 'Hoài nghi, stress, bệnh lạ, dây dưa khó dứt',
        'luc_than_map': {
            'Quan Quỷ': '⚠️ Bệnh lạ, ác mộng, bị ám ảnh, stress nặng',
            'Thê Tài': 'Tiền bạc rối rắm, khoản phí không minh bạch',
            'Phụ Mẫu': 'Nhà có hiện tượng lạ, giấy tờ rối',
            'Tử Tôn': 'Con cái gặp chuyện kỳ quái, hay mơ',
            'Huynh Đệ': 'Bạn bè lôi kéo vào chuyện phức tạp',
        }
    },
    'Bạch Hổ': {
        'hanh': 'Kim', 'tinh_chat': 'Hung dữ, tai nạn, máu huyết',
        'vuong': 'Quyền lực, nghiêm khắc, quân sự, phẫu thuật',
        'suy': 'Tai nạn, tang tóc, thương tích, bệnh nặng',
        'luc_than_map': {
            'Quan Quỷ': '⚠️ Tai nạn nghiêm trọng, bệnh nặng, phẫu thuật',
            'Thê Tài': 'Mất tài sản do tai nạn, thiệt hại lớn',
            'Phụ Mẫu': 'Bề trên gặp nạn, nhà cửa hư hại',
            'Tử Tôn': 'Con cái gặp nguy hiểm, cẩn thận tai nạn',
            'Huynh Đệ': 'Anh em gặp kiện tụng, xung đột bạo lực',
        }
    },
    'Huyền Vũ': {
        'hanh': 'Thủy', 'tinh_chat': 'Ám muội, trộm cắp, lừa đảo',
        'vuong': 'Mưu trí cao, bí mật, ngoại giao ngầm',
        'suy': 'Trộm cắp, lừa đảo, bí mật bại lộ, tình ái lén lút',
        'luc_than_map': {
            'Quan Quỷ': '⚠️ Bị lừa đảo, gian lận trong công việc',
            'Thê Tài': '⚠️ Mất tiền do trộm/lừa, tài sản bị chiếm đoạt',
            'Phụ Mẫu': 'Giấy tờ giả mạo, hợp đồng gian dối',
            'Tử Tôn': 'Con cái bị ảnh hưởng xấu, gian dối',
            'Huynh Đệ': 'Bạn bè lừa gạt, anh em không minh bạch',
        }
    },
}


# === V42.0: CỬU TINH + BÁT MÔN VƯỢNG SUY THEO MÙA ===
CUU_TINH_NGU_HANH = {
    'Thiên Bồng': 'Thủy', 'Thiên Nhuế': 'Thổ', 'Thiên Xung': 'Mộc',
    'Thiên Phụ': 'Mộc', 'Thiên Cầm': 'Thổ', 'Thiên Tâm': 'Kim',
    'Thiên Trụ': 'Kim', 'Thiên Nhậm': 'Thổ', 'Thiên Anh': 'Hỏa',
}
BAT_MON_NGU_HANH = {
    'Khai Môn': 'Mộc', 'Hưu Môn': 'Thủy', 'Sinh Môn': 'Thổ',
    'Thương Môn': 'Mộc', 'Đỗ Môn': 'Mộc', 'Cảnh Môn': 'Hỏa',
    'Tử Môn': 'Thổ', 'Kinh Môn': 'Kim',
}

def _get_seasonal_strength(hanh, lenh_thang_hanh):
    """V42.0: Tính Vượng/Tướng/Hưu/Tù/Tử theo Lệnh Tháng.
    
    Quy tắc Ngũ Hành:
    - Hành = Lệnh Tháng → VƯỢNG
    - Hành = Lệnh Tháng sinh → TƯỚNG  
    - Hành sinh Lệnh Tháng → HƯU (tiết khí)
    - Hành khắc Lệnh Tháng → TÙ (bị giam)
    - Lệnh Tháng khắc Hành → TỬ (bị khắc)
    """
    if not hanh or not lenh_thang_hanh:
        return 'BÌNH', '🟡'
    if hanh == lenh_thang_hanh:
        return 'VƯỢNG', '🟢'
    elif SINH.get(lenh_thang_hanh) == hanh:
        return 'TƯỚNG', '🔵'
    elif SINH.get(hanh) == lenh_thang_hanh:
        return 'HƯU', '🟡'
    elif KHAC.get(hanh) == lenh_thang_hanh:
        return 'TÙ', '🟠'
    elif KHAC.get(lenh_thang_hanh) == hanh:
        return 'TỬ', '🔴'
    return 'BÌNH', '🟡'

def _build_seasonal_strength_table(thien_ban, nhan_ban, lenh_thang_hanh):
    """V42.0: Xây bảng Vượng/Suy Cửu Tinh + Bát Môn theo mùa."""
    lines = []
    lines.append(f"\n**📊 BẢNG VƯỢNG/SUY THEO MÙA (Lệnh Tháng: {lenh_thang_hanh}):**")
    
    # Cửu Tinh
    lines.append(f"\n| Cửu Tinh | Ngũ Hành | Trạng Thái |")
    lines.append(f"|:---|:---:|:---:|")
    for sao_name, sao_hanh in CUU_TINH_NGU_HANH.items():
        status, icon = _get_seasonal_strength(sao_hanh, lenh_thang_hanh)
        lines.append(f"| {sao_name} | {sao_hanh} | {icon} {status} |")
    
    # Bát Môn  
    lines.append(f"\n| Bát Môn | Ngũ Hành | Trạng Thái |")
    lines.append(f"|:---|:---:|:---:|")
    for mon_name, mon_hanh in BAT_MON_NGU_HANH.items():
        status, icon = _get_seasonal_strength(mon_hanh, lenh_thang_hanh)
        lines.append(f"| {mon_name} | {mon_hanh} | {icon} {status} |")
    
    return "\n".join(lines)


# === V42.0: HÀO TỪ KINH DỊCH — Tra lời hào tại vị trí hào động ===
def _get_hao_tu(ten_que, hao_dong_idx):
    """V42.0: Tra Hào Từ Kinh Dịch tại hào động.
    
    Nguồn: vuphac.com, votranh.com — "Hào Từ là linh hồn của quẻ"
    """
    if not KINH_DICH_64 or not ten_que:
        return None
    
    # Tìm quẻ trong database
    que_data = None
    for k, v in KINH_DICH_64.items():
        if isinstance(v, dict):
            name = v.get('ten', '') or v.get('name', '') or str(k)
            if ten_que.lower() in name.lower() or name.lower() in ten_que.lower():
                que_data = v
                break
    
    if not que_data:
        return None
    
    # Lấy Hào Từ
    hao_tu_list = que_data.get('hao_tu', []) or que_data.get('hao', [])
    if isinstance(hao_tu_list, list) and hao_dong_idx and 1 <= hao_dong_idx <= len(hao_tu_list):
        return hao_tu_list[hao_dong_idx - 1]
    
    # Fallback: tìm key "hao_X" hoặc "hao X"
    hao_key = f'hao_{hao_dong_idx}'
    return que_data.get(hao_key, que_data.get(f'hào {hao_dong_idx}', None))


# === V42.0: CẢNH BÁO PHẢN/PHỤC NGÂM — HTML prominent ===
def _build_phan_phuc_ngam_warning(chart_data, luc_hao_data=None):
    """V42.0: Xây cảnh báo Phản/Phục Ngâm ở đầu kết luận.
    
    Nguồn: tuvilyso.org, maphuong.com — "Phản/Phục Ngâm PHẢI đặt đầu phân tích"
    """
    warnings = []
    
    if not chart_data or not isinstance(chart_data, dict):
        return ''
    
    can_thien_ban = chart_data.get('can_thien_ban', {})
    dia_ban = chart_data.get('dia_ban') or chart_data.get('dia_can', {})
    
    # Tìm cung bản thân và sự việc  
    can_ngay = chart_data.get('can_ngay', '')
    can_gio = chart_data.get('can_gio', '')
    chu_cung = None
    sv_cung = None
    
    for cung_num, can_val in can_thien_ban.items():
        cn = int(cung_num) if str(cung_num).isdigit() else None
        if cn and can_val == can_ngay:
            chu_cung = cn
        if cn and can_val == can_gio:
            sv_cung = cn
    
    if not chu_cung and can_ngay == 'Giáp':
        for cung_num, can_val in can_thien_ban.items():
            if can_val == 'Mậu':
                chu_cung = int(cung_num) if str(cung_num).isdigit() else None
                break
    
    # Kiểm tra Phản/Phục Ngâm cho cung BẢN THÂN
    if chu_cung:
        can_thien = can_thien_ban.get(chu_cung, can_thien_ban.get(str(chu_cung), ''))
        can_dia = ''
        if dia_ban:
            can_dia = dia_ban.get(chu_cung, dia_ban.get(str(chu_cung), ''))
        if can_thien and can_dia:
            ppn = _check_phan_phuc_ngam(can_thien, can_dia)
            if ppn == 'PHẢN NGÂM':
                warnings.append(('⚡ PHẢN NGÂM CUNG BẢN THÂN', '🔴 Bạn đang mâu thuẫn nội tâm, có khả năng ĐẢO NGƯỢC ý định ban đầu. Kết quả sẽ NGƯỢC lại dự kiến!', 'red'))
            elif ppn == 'PHỤC NGÂM':
                warnings.append(('🔄 PHỤC NGÂM CUNG BẢN THÂN', '🟠 Sự việc LẶP LẠI, không tiến triển, đi vòng tròn. Cần thay đổi cách tiếp cận!', 'orange'))
    
    # Kiểm tra Phản/Phục Ngâm cho cung SỰ VIỆC
    if sv_cung and sv_cung != chu_cung:
        can_thien_sv = can_thien_ban.get(sv_cung, can_thien_ban.get(str(sv_cung), ''))
        can_dia_sv = ''
        if dia_ban:
            can_dia_sv = dia_ban.get(sv_cung, dia_ban.get(str(sv_cung), ''))
        if can_thien_sv and can_dia_sv:
            ppn_sv = _check_phan_phuc_ngam(can_thien_sv, can_dia_sv)
            if ppn_sv == 'PHẢN NGÂM':
                warnings.append(('⚡ PHẢN NGÂM CUNG SỰ VIỆC', '🔴 Sự việc sẽ ĐẢO NGƯỢC hoàn toàn so với kỳ vọng!', 'red'))
            elif ppn_sv == 'PHỤC NGÂM':
                warnings.append(('🔄 PHỤC NGÂM CUNG SỰ VIỆC', '🟠 Sự việc TRÙNG LẶP, khó tiến triển, giậm chân tại chỗ!', 'orange'))
    
    if not warnings:
        return ''
    
    # Build HTML cảnh báo
    html_parts = []
    for title, desc, color in warnings:
        border_color = '#ef4444' if color == 'red' else '#f97316'
        bg_from = '#7f1d1d' if color == 'red' else '#7c2d12'
        bg_to = '#991b1b' if color == 'red' else '#9a3412'
        html_parts.append(
            f'<div style="background:linear-gradient(135deg,{bg_from},{bg_to});padding:18px;border-radius:14px;'
            f'margin:10px 0;border:3px solid {border_color};box-shadow:0 4px 20px rgba(239,68,68,0.3);">'
            f'<div style="font-size:1.3em;font-weight:900;color:#fca5a5;">{title}</div>'
            f'<div style="font-size:1.1em;color:#fecaca;margin-top:6px;">{desc}</div>'
            f'</div>'
        )
    return "\n".join(html_parts)

# === V42.1: GÓC NHÌN THIÊN-ĐỊA-NHÂN-THẦN (4 Trụ Chiến Lược KM) ===
def _build_thien_dia_nhan_than(thien_ban, nhan_ban, than_ban, chu_cung, sv_cung, lenh_thang_hanh):
    """V42.1: Xây bảng Thiên-Địa-Nhân-Thần chiến lược — góc nhìn tổng quát Kỳ Môn.
    
    Nguồn: Học viện Minh Việt — "4 trụ chiến lược KM:
    - Thiên Thời = Cửu Tinh (thời cơ, vận may)
    - Địa Lợi = Bát Quái + Cung (môi trường, điều kiện)
    - Nhân Hòa = Bát Môn (con người, hành động)
    - Thần Trợ = Bát Thần (lực lượng siêu nhiên)"
    """
    lines = []
    if not thien_ban or not nhan_ban or not than_ban:
        return ''
    
    lines.append(f"\n**🏛️ GÓC NHÌN CHIẾN LƯỢC THIÊN-ĐỊA-NHÂN-THẦN:**")
    lines.append(f"*Kỳ Môn Độn Giáp phân tích theo 4 trụ chiến lược*")
    
    # Lấy data từ cung Bản Thân
    bt_sao = thien_ban.get(chu_cung, thien_ban.get(str(chu_cung), '?')) if chu_cung else '?'
    bt_cua = nhan_ban.get(chu_cung, nhan_ban.get(str(chu_cung), '?')) if chu_cung else '?'
    bt_than = than_ban.get(chu_cung, than_ban.get(str(chu_cung), '?')) if chu_cung else '?'
    
    # Lấy data từ cung Sự Việc  
    sv_sao = thien_ban.get(sv_cung, thien_ban.get(str(sv_cung), '?')) if sv_cung else '?'
    sv_cua = nhan_ban.get(sv_cung, nhan_ban.get(str(sv_cung), '?')) if sv_cung else '?'
    sv_than = than_ban.get(sv_cung, than_ban.get(str(sv_cung), '?')) if sv_cung else '?'
    
    # Đánh giá từng trụ
    # 1. THIÊN THỜI (Cửu Tinh)
    bt_sao_hanh = CUU_TINH_NGU_HANH.get(str(bt_sao), '')
    bt_sao_status = ''
    if bt_sao_hanh and lenh_thang_hanh:
        bt_sao_strength, bt_sao_icon = _get_seasonal_strength(bt_sao_hanh, lenh_thang_hanh)
        bt_sao_status = f"{bt_sao_icon} {bt_sao_strength}"
    
    sao_cat = any(s in str(bt_sao) for s in ['Tâm', 'Nhậm', 'Phụ', 'Xung'])
    sao_hung = any(s in str(bt_sao) for s in ['Bồng', 'Nhuế', 'Trụ', 'Anh'])
    thien_verdict = '✅ THUẬN' if sao_cat else ('⚠️ NGHỊCH' if sao_hung else '🟡 BÌNH')
    lines.append(f"\n| Trụ | Yếu tố | Cung BT | Cung SV | Đánh giá |")
    lines.append(f"|:---|:---|:---:|:---:|:---:|")
    lines.append(f"| 🌤️ **THIÊN THỜI** | Cửu Tinh (thời cơ) | {bt_sao} {bt_sao_status} | {sv_sao} | {thien_verdict} |")
    
    # 2. ĐỊA LỢI (Cung + Quái)
    bt_cung_hanh = CUNG_NGU_HANH.get(chu_cung, '?') if chu_cung else '?'
    sv_cung_hanh = CUNG_NGU_HANH.get(sv_cung, '?') if sv_cung else '?'
    dia_verdict = '✅ THUẬN' if bt_cung_hanh == lenh_thang_hanh else ('⚠️ NGHỊCH' if KHAC.get(lenh_thang_hanh) == bt_cung_hanh else '🟡 BÌNH')
    lines.append(f"| 🌍 **ĐỊA LỢI** | Cung + Quái (môi trường) | Cung {chu_cung or '?'} ({bt_cung_hanh}) | Cung {sv_cung or '?'} ({sv_cung_hanh}) | {dia_verdict} |")
    
    # 3. NHÂN HÒA (Bát Môn)
    cua_cat_list = ['Khai', 'Hưu', 'Sinh']
    cua_hung_list = ['Tử', 'Kinh', 'Thương']
    bt_cua_ok = any(c in str(bt_cua) for c in cua_cat_list)
    bt_cua_bad = any(c in str(bt_cua) for c in cua_hung_list)
    nhan_verdict = '✅ THUẬN' if bt_cua_ok else ('⚠️ NGHỊCH' if bt_cua_bad else '🟡 BÌNH')
    lines.append(f"| 👥 **NHÂN HÒA** | Bát Môn (hành động) | {bt_cua} | {sv_cua} | {nhan_verdict} |")
    
    # 4. THẦN TRỢ (Bát Thần)
    than_cat_list = ['Trực Phù', 'Thái Âm', 'Lục Hợp', 'Cửu Địa', 'Cửu Thiên']
    than_hung_list = ['Bạch Hổ', 'Huyền Vũ', 'Đằng Xà']
    bt_than_ok = any(t in str(bt_than) for t in than_cat_list)
    bt_than_bad = any(t in str(bt_than) for t in than_hung_list)
    than_verdict = '✅ CÁT' if bt_than_ok else ('⚠️ HUNG' if bt_than_bad else '🟡 BÌNH')
    lines.append(f"| 🙏 **THẦN TRỢ** | Bát Thần (siêu nhiên) | {bt_than} | {sv_than} | {than_verdict} |")
    
    # Tổng kết chiến lược
    total_ok = sum([1 for v in [thien_verdict, dia_verdict, nhan_verdict, than_verdict] if '✅' in v])
    total_bad = sum([1 for v in [thien_verdict, dia_verdict, nhan_verdict, than_verdict] if '⚠️' in v])
    
    if total_ok >= 3:
        lines.append(f"\n→ **🏆 TỔNG KẾT CHIẾN LƯỢC: {total_ok}/4 trụ THUẬN** — Thiên thời + Địa lợi + Nhân hòa HỘI TỤ → ĐẠI CÁT!")
    elif total_ok >= 2:
        lines.append(f"\n→ **✅ TỔNG KẾT CHIẾN LƯỢC: {total_ok}/4 trụ THUẬN** — Đa số thuận, có thể hành động nhưng cần lưu ý trụ yếu.")
    elif total_bad >= 3:
        lines.append(f"\n→ **🔴 TỔNG KẾT CHIẾN LƯỢC: {total_bad}/4 trụ NGHỊCH** — Thiên-Địa-Nhân-Thần đều bất lợi → TUYỆT ĐỐI KHÔNG NÊN hành động!")
    else:
        lines.append(f"\n→ **🟡 TỔNG KẾT CHIẾN LƯỢC: Cân bằng** — Có thuận có nghịch, cần cân nhắc kỹ từng yếu tố.")
    
    return "\n".join(lines)


# === V42.1: PHÂN TÍCH TÁC ĐỘNG SÂU KHÔNG VONG + DỊCH MÃ ===
def _analyze_kv_dich_ma_deep(khong_vong_list, dich_ma_chi, dung_than_chi, dung_than_name,
                              haos=None, dong_hao=None, chi_ngay='', chi_thang='', verdict=''):
    """V42.1: Phân tích tác động sâu của Không Vong và Dịch Mã.
    
    Nguồn: tuvilyso.org, vuphac.com
    - Không Vong: Chân Không vs Giả Không, tác động lên DT, thời gian xuất Không
    - Dịch Mã: Mã gặp Xung/Hợp/Hào Động, phân tích di chuyển/biến động
    """
    lines = []
    
    # ====== PHÂN TÍCH KHÔNG VONG SÂU ======
    if khong_vong_list:
        # 1. Check DT lâm Không Vong
        dt_in_kv = dung_than_chi and dung_than_chi in khong_vong_list
        if dt_in_kv:
            lines.append(f"\n**🕳️ PHÂN TÍCH KHÔNG VONG CHUYÊN SÂU:**")
            lines.append(f"  Dụng Thần **{dung_than_name}** ({dung_than_chi}) lâm Tuần Không [{', '.join(khong_vong_list)}]")
            
            # Chân Không vs Giả Không
            # Chân Không: DT suy + Không Vong → thật sự không có
            # Giả Không: DT vượng + Không Vong → chỉ tạm chưa hiện, sẽ ứng khi xuất Không
            if verdict in ('HUNG', 'ĐẠI HUNG'):
                lines.append(f"  → 🔴 **CHÂN KHÔNG**: DT suy + Không Vong = Sự việc THẬT SỰ KHÔNG CÓ, hư vô!")
                lines.append(f"    *Quẻ HUNG + KV → không có cơ hội phục hồi*")
            elif verdict in ('CÁT', 'ĐẠI CÁT'):
                lines.append(f"  → 🟡 **GIẢ KHÔNG**: DT vượng + Không Vong = Sự việc ĐÃ CÓ nhưng CHƯA HIỆN")
                lines.append(f"    *Quẻ CÁT + KV → chờ xuất Không (ngày/giờ Chi {dung_than_chi}) sẽ ứng nghiệm*")
            else:
                lines.append(f"  → 🟠 **BÁN KHÔNG**: Sự việc bấp bênh, chưa rõ thực hư")
                lines.append(f"    *Cần chờ xuất Không (ngày Chi {dung_than_chi}) để xác định*")
            
            # Thời gian xuất Không
            xung_kv = LUC_XUNG_CHI.get(dung_than_chi, '')
            if xung_kv:
                lines.append(f"  → ⏰ **Xuất Không khi:** Gặp ngày/giờ Chi **{dung_than_chi}** (trùng) hoặc **{xung_kv}** (xung)")
        
        # 2. Check các hào khác lâm KV
        if haos:
            kv_haos = []
            for i, hao in enumerate(haos):
                h_chi = hao.get('chi', '')
                h_lt = hao.get('luc_than', '')
                if h_chi and h_chi in khong_vong_list and h_lt != dung_than_name:
                    kv_haos.append((i+1, h_lt, h_chi))
            if kv_haos:
                if not dt_in_kv:
                    lines.append(f"\n**🕳️ KHÔNG VONG CÁC HÀO:**")
                for h_idx, h_lt, h_chi in kv_haos:
                    impact = ''
                    if h_lt == 'Quan Quỷ':
                        impact = '→ Quan Quỷ KV = Sếp/bệnh không thực → Giảm áp lực ✅'
                    elif h_lt == 'Thê Tài':
                        impact = '→ Thê Tài KV = Tiền tài hư → Khó kiếm tiền ⚠️'
                    elif h_lt == 'Huynh Đệ':
                        impact = '→ Huynh Đệ KV = Đối thủ yếu → Bớt cạnh tranh ✅'
                    elif h_lt == 'Phụ Mẫu':
                        impact = '→ Phụ Mẫu KV = Giấy tờ hư → Hợp đồng/nhà chưa chắc ⚠️'
                    elif h_lt == 'Tử Tôn':
                        impact = '→ Tử Tôn KV = Vui vẻ hư → Niềm vui chưa đến ⚠️'
                    lines.append(f"  - Hào {h_idx} **{h_lt}** ({h_chi}) lâm KV {impact}")
    
    # ====== PHÂN TÍCH DỊCH MÃ SÂU ======
    if dich_ma_chi:
        lines.append(f"\n**🐎 PHÂN TÍCH DỊCH MÃ CHUYÊN SÂU:**")
        lines.append(f"  Dịch Mã tại Chi **{dich_ma_chi}**")
        
        # 1. Dịch Mã gặp Xung → di chuyển RẤT NHANH
        xung_ma = LUC_XUNG_CHI.get(dich_ma_chi, '')
        if xung_ma and chi_ngay and chi_ngay == xung_ma:
            lines.append(f"  → ⚡ **MÃ TINH BỊ XUNG** (Nhật {chi_ngay} xung Mã {dich_ma_chi}): Di chuyển/thay đổi CỰC NHANH!")
        
        # 2. Dịch Mã gặp Hợp → bị giữ lại, di chuyển bị cản
        hop_ma = LUC_HOP_CHI.get(dich_ma_chi, '')
        if hop_ma and chi_ngay and chi_ngay == hop_ma:
            lines.append(f"  → 🤝 **MÃ TINH BỊ HỢP** (Nhật {chi_ngay} hợp Mã {dich_ma_chi}): Bị GIỮ LẠI, muốn đi mà không đi được!")
        
        # 3. Mã rơi KV → di chuyển hư
        if khong_vong_list and dich_ma_chi in khong_vong_list:
            lines.append(f"  → 🕳️ **MÃ TINH LÂM KHÔNG VONG**: Muốn đi nhưng KHÔNG ĐI ĐƯỢC, kế hoạch di chuyển bị hủy!")
        
        # 4. DT lâm Dịch Mã
        if dung_than_chi == dich_ma_chi:
            lines.append(f"  → 🐎 **DT LÂM DỊCH MÃ**: Sự việc GẮN VỚI DI CHUYỂN, thay đổi, không ổn định tại chỗ!")
        
        # 5. Hào nào mang Dịch Mã
        if haos:
            for i, hao in enumerate(haos):
                h_chi = hao.get('chi', '')
                if h_chi == dich_ma_chi:
                    h_lt = hao.get('luc_than', '')
                    is_dong = (i+1) in (dong_hao or [])
                    dong_str = '**ĐỘNG**' if is_dong else 'tĩnh'
                    lines.append(f"  → 🏇 Hào {i+1} **{h_lt}** ({h_chi}) mang Dịch Mã ({dong_str})")
                    if is_dong:
                        lines.append(f"    *Mã Tinh PHÁT ĐỘNG = Sự di chuyển/thay đổi CHẮC CHẮN xảy ra!*")
    
    return "\n".join(lines)


# === V42.1: CẢNH BÁO NGUYỆT PHÁ VISUAL — Hiển thị prominent ===
def _build_nguyet_pha_warning(dung_than_chi, chi_thang, dung_than_name='Dụng Thần',
                                haos=None, method='LỤC HÀO'):
    """V42.1: Xây cảnh báo Nguyệt Phá prominent.
    
    Nguồn: vuphac.com, kinhdichluchao.vn
    Nguyệt Phá = Chi tháng XUNG Chi hào → Hào bị PHÁ, VÔ LỰC, suy đến cực.
    Đây là yếu tố RẤT NẶNG: dù hào có vượng cũng bị Nguyệt Phá → mất sức.
    """
    lines = []
    html_parts = []
    
    if not chi_thang:
        return '', ''
    
    # 1. Check DT bị Nguyệt Phá
    if dung_than_chi and LUC_XUNG_CHI.get(chi_thang) == dung_than_chi:
        html_parts.append(
            f'<div style="background:linear-gradient(135deg,#4a1942,#6b2fa0);padding:18px;border-radius:14px;'
            f'margin:10px 0;border:3px solid #a855f7;box-shadow:0 4px 20px rgba(168,85,247,0.3);">'
            f'<div style="font-size:1.3em;font-weight:900;color:#e9d5ff;">💥 NGUYỆT PHÁ — {dung_than_name} VÔ LỰC!</div>'
            f'<div style="font-size:1.1em;color:#f5d0fe;margin-top:6px;">'
            f'Chi tháng ({chi_thang}) XUNG {dung_than_name} ({dung_than_chi}) → Sức mạnh TAN VỠ! '
            f'Dù {dung_than_name} có vượng cũng bị Nguyệt Phá phá hoại. '
            f'Sự việc KHÓ THÀNH trong tháng này, chờ qua tháng mới có cơ hội.</div>'
            f'</div>'
        )
        lines.append(f"💥 **NGUYỆT PHÁ:** {dung_than_name} ({dung_than_chi}) bị Chi tháng ({chi_thang}) xung → VÔ LỰC!")
    
    # 2. Check các hào khác bị Nguyệt Phá (LH)
    nguyet_pha_haos = []
    if haos and method == 'LỤC HÀO':
        for i, hao in enumerate(haos):
            h_chi = hao.get('chi', '')
            h_lt = hao.get('luc_than', '')
            if h_chi and h_chi != dung_than_chi and LUC_XUNG_CHI.get(chi_thang) == h_chi:
                nguyet_pha_haos.append((i+1, h_lt, h_chi))
        
        if nguyet_pha_haos:
            lines.append(f"\n**💥 CÁC HÀO BỊ NGUYỆT PHÁ:**")
            for h_idx, h_lt, h_chi in nguyet_pha_haos:
                impact = ''
                if h_lt == 'Kỵ Thần' or h_lt == 'Quan Quỷ':
                    impact = '→ Kỵ Thần/Quan Quỷ bị phá = Áp lực GIẢM ✅'
                elif h_lt == 'Nguyên Thần':
                    impact = '→ Nguyên Thần bị phá = Nguồn trợ giúp BỊ MẤT ⚠️'
                elif h_lt == 'Thê Tài':
                    impact = '→ Thê Tài bị phá = Tài chính bị TỔN THẤT ⚠️'
                elif h_lt == 'Huynh Đệ':
                    impact = '→ Huynh Đệ bị phá = Đối thủ YẾU ĐI ✅'
                elif h_lt == 'Phụ Mẫu':
                    impact = '→ Phụ Mẫu bị phá = Giấy tờ/hợp đồng BẤT LỢI ⚠️'
                elif h_lt == 'Tử Tôn':
                    impact = '→ Tử Tôn bị phá = Niềm vui/giải trừ BỊ MẤT ⚠️'
                lines.append(f"  - Hào {h_idx} **{h_lt}** ({h_chi}) bị Nguyệt Phá {impact}")
    
    return "\n".join(lines), "\n".join(html_parts)


# === V9.0: MỞ RỘNG QUÁI Ý NGHĨA — VẠN VẬT LOẠI TƯỢNG CHI TIẾT ===
QUAI_Y_NGHIA = {
    'Càn': {'tuong': 'Trời ☰', 'tc': 'Mạnh mẽ, lãnh đạo, cha, cương kiện', 'hanh': 'Kim',
            'gia_dinh': 'Cha, người đàn ông lớn tuổi, người đứng đầu',
            'co_the': 'Đầu, xương, phổi', 'benh': 'Đau đầu, bệnh xương, phổi',
            'dong_vat': 'Ngựa, sư tử', 'huong': 'Tây Bắc', 'mua': 'Cuối thu - đầu đông',
            'sac': 'Trắng, vàng kim', 'so': '1 (Tiên Thiên)', 
            'lh': {'tài': 'Kim = tiền lớn, quý kim', 'việc': 'Quyền lực, lãnh đạo', 'tình': 'Chủ động, mạnh mẽ'}},
    'Khôn': {'tuong': 'Đất ☷', 'tc': 'Nhu thuận, bao dung, mẹ, nuôi dưỡng', 'hanh': 'Thổ',
             'gia_dinh': 'Mẹ, người phụ nữ lớn tuổi, vợ',
             'co_the': 'Bụng, dạ dày, tỳ', 'benh': 'Đau bụng, bệnh tiêu hóa, tỳ vị',
             'dong_vat': 'Trâu, bò', 'huong': 'Tây Nam', 'mua': 'Cuối hạ - đầu thu',
             'sac': 'Vàng, nâu đất', 'so': '8 (Tiên Thiên)',
             'lh': {'tài': 'Bất động sản, đất đai', 'việc': 'Hỗ trợ, phục vụ', 'tình': 'Dịu dàng, bao dung'}},
    'Chấn': {'tuong': 'Sấm ☳', 'tc': 'Động, khởi đầu, con trai trưởng, chấn động', 'hanh': 'Mộc',
             'gia_dinh': 'Con trai trưởng, thanh niên',
             'co_the': 'Chân, gan, thần kinh', 'benh': 'Đau chân, bệnh gan, co giật',
             'dong_vat': 'Rồng, rắn', 'huong': 'Đông', 'mua': 'Mùa Xuân',
             'sac': 'Xanh lá, xanh lam', 'so': '4 (Tiên Thiên)',
             'lh': {'tài': 'Phát triển nhanh', 'việc': 'Khởi nghiệp, khởi đầu mới', 'tình': 'Nóng vội, bùng nổ'}},
    'Tốn': {'tuong': 'Gió ☴', 'tc': 'Thuận, giao thương, con gái trưởng, thâm nhập', 'hanh': 'Mộc',
            'gia_dinh': 'Con gái trưởng, phụ nữ trung niên',
            'co_the': 'Bắp đùi, mông, thắt lưng', 'benh': 'Đau thắt lưng, bệnh hô hấp, cảm gió',
            'dong_vat': 'Gà, côn trùng', 'huong': 'Đông Nam', 'mua': 'Cuối xuân - đầu hạ',
            'sac': 'Xanh lá nhạt, trắng xanh', 'so': '5 (Tiên Thiên)',
            'lh': {'tài': 'Buôn bán, giao thương', 'việc': 'Thương lượng, đàm phán', 'tình': 'Lãng mạn, nhẹ nhàng'}},
    'Khảm': {'tuong': 'Nước ☵', 'tc': 'Hiểm, trí tuệ, con trai giữa, sâu thẳm', 'hanh': 'Thủy',
             'gia_dinh': 'Con trai thứ, người trung niên',
             'co_the': 'Tai, thận, máu', 'benh': 'Bệnh thận, tai, huyết áp, tiểu đường',
             'dong_vat': 'Lợn, cá', 'huong': 'Bắc', 'mua': 'Mùa Đông',
             'sac': 'Đen, tím đen', 'so': '6 (Tiên Thiên)',
             'lh': {'tài': 'Lưu thông, tiền mặt', 'việc': 'Thử thách, nguy hiểm', 'tình': 'Sâu sắc, bí ẩn'}},
    'Ly': {'tuong': 'Lửa ☲', 'tc': 'Sáng, đẹp, văn minh, con gái giữa', 'hanh': 'Hỏa',
           'gia_dinh': 'Con gái thứ, phụ nữ trẻ',
           'co_the': 'Mắt, tim, huyết mạch', 'benh': 'Bệnh mắt, tim mạch, huyết áp cao',
           'dong_vat': 'Chim trĩ, phượng', 'huong': 'Nam', 'mua': 'Mùa Hạ',
           'sac': 'Đỏ, cam, hồng', 'so': '3 (Tiên Thiên)',
           'lh': {'tài': 'Nhanh, bùng phát', 'việc': 'Danh tiếng, văn hóa', 'tình': 'Rực rỡ, nồng nhiệt'}},
    'Cấn': {'tuong': 'Núi ☶', 'tc': 'Tĩnh, dừng lại, con trai út, ổn định', 'hanh': 'Thổ',
            'gia_dinh': 'Con trai út, thiếu niên',
            'co_the': 'Tay, ngón, lưng, mũi', 'benh': 'Đau tay, lưng, bệnh xương khớp',
            'dong_vat': 'Chó, hổ, chuột', 'huong': 'Đông Bắc', 'mua': 'Cuối đông - đầu xuân',
            'sac': 'Vàng nhạt, nâu', 'so': '7 (Tiên Thiên)',
            'lh': {'tài': 'Tích trữ, bất động sản', 'việc': 'Suy ngẫm, nghiên cứu', 'tình': 'Chậm chạp, bền vững'}},
    'Đoài': {'tuong': 'Đầm ☱', 'tc': 'Vui, nói, con gái út, hưởng thụ', 'hanh': 'Kim',
             'gia_dinh': 'Con gái út, thiếu nữ',
             'co_the': 'Miệng, răng, lưỡi, phổi', 'benh': 'Đau miệng, răng, bệnh phổi, hô hấp',
             'dong_vat': 'Dê, cừu', 'huong': 'Tây', 'mua': 'Mùa Thu',
             'sac': 'Trắng, bạc', 'so': '2 (Tiên Thiên)',
             'lh': {'tài': 'Hưởng thụ, tiêu dùng', 'việc': 'Giao tiếp, ngoại giao', 'tình': 'Vui tươi, nói chuyện'}},
}

# === V9.0: THOÁN TỪ + ĐẠI TƯỢNG 8 QUẺ CƠ BẢN ===
QUE_THOAN_DAI_TUONG = {
    'Càn': {'thoan': 'Nguyên hanh lợi trinh — Đạo Trời vận hành mạnh mẽ không ngừng', 
            'dai_tuong': 'Trời đi mạnh, quân tử tự cường không nghỉ', 'lk': 'Hành động mạnh mẽ, kiên trì'},
    'Khôn': {'thoan': 'Nguyên hanh, lợi tẫn mã trinh — Đất rộng lớn, thuận theo trời',
             'dai_tuong': 'Đất thuận chở, quân tử dày đức chở vật', 'lk': 'Nhẫn nại, thuận theo tự nhiên'},
    'Khảm': {'thoan': 'Tập Khảm, có phu, duy tâm hanh — Nước chảy liên tục không ngừng',
             'dai_tuong': 'Nước chảy mãi, quân tử đạo đức hằng thường', 'lk': 'Kiên trì vượt khó, giữ tâm chính'},
    'Ly': {'thoan': 'Ly, lợi trinh, hanh — Ánh sáng bám vào, soi rọi',
           'dai_tuong': 'Sáng lặp, đại nhân nối sáng thiên hạ', 'lk': 'Sáng suốt, minh bạch, tiếp nối'},
    'Chấn': {'thoan': 'Hanh, sấm đến sợ sợ — Sấm động khiến người sợ hãi',
             'dai_tuong': 'Sấm nổi liên tiếp, quân tử sợ mà tu sửa', 'lk': 'Cẩn trọng sửa mình sau chấn động'},
    'Cấn': {'thoan': 'Cấn kỳ bối, không đạt kỳ thân — Giữ yên lưng, không thấy thân mình',
            'dai_tuong': 'Hai núi chồng, quân tử biết dừng đúng lúc', 'lk': 'Biết dừng, biết đủ, tĩnh lặng'},
    'Tốn': {'thoan': 'Tiểu hanh, lợi hữu du vãng — Thuận gió nhẹ nhàng thâm nhập',
            'dai_tuong': 'Gió theo nhau, quân tử hành mệnh lệnh', 'lk': 'Khiêm nhường thâm nhập, dần dần tiến'},
    'Đoài': {'thoan': 'Hanh, lợi trinh — Vui vẻ, hòa hợp, trao đổi',
             'dai_tuong': 'Đầm liền nhau, quân tử giảng học bàn luận', 'lk': 'Giao tiếp cởi mở, trao đổi bàn bạc'},
}

# ═══════════════════════════════════════════════════════════
# V17.0: LỤC THUẬT PHÂN CẤP — METHOD STRENGTH MAP
# Trọng số (0-100) cho mỗi PP theo loại câu hỏi
# PP có trọng số cao nhất = PP CHÍNH cho loại câu hỏi đó
# ═══════════════════════════════════════════════════════════
METHOD_STRENGTH_MAP = {
    # V32.7: RESEARCH-BACKED — Trọng số theo thế mạnh từng môn cho từng loại câu hỏi
    # LH = vua chi tiết, KM = vua chiến lược/phương vị, MH = nhanh/số, LN = diễn biến/tìm, TB = vận mệnh, TA = vĩ mô
    'tài_chính':    {'ky_mon': 50, 'luc_hao': 100, 'mai_hoa': 60, 'thiet_ban': 30, 'luc_nham': 50, 'thai_at': 20},
    'sự_nghiệp':    {'ky_mon': 60, 'luc_hao': 100, 'mai_hoa': 55, 'thiet_ban': 40, 'luc_nham': 55, 'thai_at': 30},
    'tình_cảm':     {'ky_mon': 45, 'luc_hao': 100, 'mai_hoa': 70, 'thiet_ban': 30, 'luc_nham': 60, 'thai_at': 20},
    'sức_khỏe':     {'ky_mon': 55, 'luc_hao': 100, 'mai_hoa': 45, 'thiet_ban': 40, 'luc_nham': 70, 'thai_at': 25},
    'tìm_đồ':       {'ky_mon': 100, 'luc_hao': 55, 'mai_hoa': 45, 'thiet_ban': 20, 'luc_nham': 90, 'thai_at': 15},
    'thời_gian':    {'ky_mon': 60, 'luc_hao': 100, 'mai_hoa': 85, 'thiet_ban': 35, 'luc_nham': 55, 'thai_at': 40},
    'phương_hướng': {'ky_mon': 100, 'luc_hao': 40, 'mai_hoa': 35, 'thiet_ban': 20, 'luc_nham': 80, 'thai_at': 50},
    'tranh_đấu':    {'ky_mon': 100, 'luc_hao': 70, 'mai_hoa': 45, 'thiet_ban': 30, 'luc_nham': 55, 'thai_at': 75},
    'tổng_quát':    {'ky_mon': 55, 'luc_hao': 100, 'mai_hoa': 70, 'thiet_ban': 40, 'luc_nham': 50, 'thai_at': 35},
    'nhà_đất':      {'ky_mon': 60, 'luc_hao': 100, 'mai_hoa': 55, 'thiet_ban': 50, 'luc_nham': 60, 'thai_at': 30},
    'thi_cử':       {'ky_mon': 50, 'luc_hao': 100, 'mai_hoa': 65, 'thiet_ban': 45, 'luc_nham': 50, 'thai_at': 25},
    'vận_mệnh':     {'ky_mon': 40, 'luc_hao': 55, 'mai_hoa': 50, 'thiet_ban': 100, 'luc_nham': 45, 'thai_at': 90},
    # V32.7 NEW: Tuổi/Số dùng LH Trường Sinh + MH Tiên Thiên
    'tuổi_số':      {'ky_mon': 50, 'luc_hao': 100, 'mai_hoa': 90, 'thiet_ban': 30, 'luc_nham': 40, 'thai_at': 20},
    'con_cái':      {'ky_mon': 50, 'luc_hao': 100, 'mai_hoa': 70, 'thiet_ban': 35, 'luc_nham': 55, 'thai_at': 25},
    'chiến_lược':   {'ky_mon': 100, 'luc_hao': 55, 'mai_hoa': 50, 'thiet_ban': 30, 'luc_nham': 60, 'thai_at': 70},
}

# Mapping category_label → strength key
CATEGORY_TO_STRENGTH = {
    'TÀI CHÍNH': 'tài_chính', 'KINH DOANH': 'tài_chính', 'ĐẦU TƯ': 'tài_chính', 'TIỀN': 'tài_chính',
    'SỰ NGHIỆP': 'sự_nghiệp', 'CÔNG VIỆC': 'sự_nghiệp', 'THĂNG TIẾN': 'sự_nghiệp', 'VIỆC LÀM': 'sự_nghiệp',
    'TÌNH CẢM': 'tình_cảm', 'HÔN NHÂN': 'tình_cảm', 'TÌNH YÊU': 'tình_cảm', 'VỢ CHỒNG': 'tình_cảm',
    'SỨC KHỎE': 'sức_khỏe', 'BỆNH TẬT': 'sức_khỏe', 'BỆNH': 'sức_khỏe',
    'TÌM ĐỒ': 'tìm_đồ', 'MẤT ĐỒ': 'tìm_đồ', 'TÌM NGƯỜI': 'tìm_đồ', 'Ở ĐÂU': 'tìm_đồ',
    'THỜI GIAN': 'thời_gian', 'BAO GIỜ': 'thời_gian', 'KHI NÀO': 'thời_gian', 'BAO LÂU': 'thời_gian',
    'PHƯƠNG HƯỚNG': 'phương_hướng', 'ĐI ĐÂU': 'phương_hướng',
    'TRANH ĐẤU': 'tranh_đấu', 'KIỆN TỤNG': 'tranh_đấu', 'ĐỐI THỦ': 'tranh_đấu',
    'NHÀ ĐẤT': 'nhà_đất', 'MUA NHÀ': 'nhà_đất', 'NHÀ CỬA': 'nhà_đất', 'NHÀ': 'nhà_đất',
    'THI CỬ': 'thi_cử', 'HỌC HÀNH': 'thi_cử', 'THI': 'thi_cử',
    'VẬN MỆNH': 'vận_mệnh', 'SỐ MỆNH': 'vận_mệnh',
    'XUẤT HÀNH': 'phương_hướng', 'DI CHUYỂN': 'phương_hướng', 'VỀ QUÊ': 'phương_hướng',
    # V32.7 NEW
    'TUỔI': 'tuổi_số', 'SỐ': 'tuổi_số', 'ĐẾM': 'tuổi_số', 'BAO NHIÊU': 'tuổi_số', 'MẤY': 'tuổi_số',
    'CON CÁI': 'con_cái', 'CON': 'con_cái', 'SINH CON': 'con_cái',
    'CHIẾN LƯỢC': 'chiến_lược', 'NÊN LÀM GÌ': 'chiến_lược', 'HƯỚNG': 'chiến_lược',
    'SẢN XUẤT': 'sự_nghiệp', 'CÔNG TY': 'sự_nghiệp',
}

METHOD_NAMES = {
    'ky_mon': 'Kỳ Môn', 'luc_hao': 'Lục Hào', 'mai_hoa': 'Mai Hoa',
    'thiet_ban': 'Thiết Bản', 'luc_nham': 'Đại Lục Nhâm', 'thai_at': 'Thái Ất',
}

# ═══════════════════════════════════════════════════════════
# V18.0: AI THÁM TỬ — QUÁI ATTRIBUTES (Manh mối Vạn Vật)
# Mỗi quái cho ra nhiều thuộc tính để cross-reference
# ═══════════════════════════════════════════════════════════

# V27.0: TICH HOP 3 MODULE QUAN TRONG
# Module 1: Quy tac nang cao (mau sac, khoang cach, nguoi quen/la, 64 que)
try:
    from qmdg_advanced_rules import MAU_SAC_NGU_HANH as ADV_MAU_SAC, QUEN_LA_QUY_TAC, KHOANG_CACH_CHI_TIET, KHA_NANG_LAY_LAI, QUE_64 as ADV_QUE_64
except ImportError:
    ADV_MAU_SAC = {}
    QUEN_LA_QUY_TAC = {}
    KHOANG_CACH_CHI_TIET = {}
    KHA_NANG_LAY_LAI = {}
    ADV_QUE_64 = {}

# Module 2: Quy tac suy luan (xac dinh nguoi lay, gia tri vat, kha nang bat)
try:
    from qmdg_inference_rules import (
        MAU_SAC_VAT_MAT, NGUYEN_TAC_TRA_LOI, DAC_DIEM_KE_LAY,
        GIA_TRI_VE_SO, KHA_NANG_BI_BAT, KHOANG_CACH_CHUAN,
        QUEN_LA_CHI_TIET, DAC_DIEM_THEO_THAN, KHA_NANG_BI_BAT_THEO_THAN
    )
except ImportError:
    MAU_SAC_VAT_MAT = {}
    NGUYEN_TAC_TRA_LOI = ""
    DAC_DIEM_KE_LAY = {}
    GIA_TRI_VE_SO = {}
    KHA_NANG_BI_BAT = {}
    KHOANG_CACH_CHUAN = {}
    QUEN_LA_CHI_TIET = {}
    DAC_DIEM_THEO_THAN = {}
    KHA_NANG_BI_BAT_THEO_THAN = {}

# Module 3: 64 que Kinh Dich day du (fortune, love, career, lost_item...)
try:
    from iching_integrated_data import ICHING_HEXAGRAMS, LUC_THAN_MEANINGS as ICHING_LUC_THAN
except ImportError:
    ICHING_HEXAGRAMS = {}
    ICHING_LUC_THAN = {}


# V27.0: Module 4: Blind Reading (doc mu que)
try:
    from blind_reading import get_season_vuong_suy as BLIND_VUONG_SUY
except ImportError:
    def BLIND_VUONG_SUY(h, t): return "Binh"

# V27.0: Module 5: Phan tich da tang (tuong tac giua 2 cung)
try:
    from phan_tich_da_tang import tinh_ngu_hanh_sinh_khac as DATANG_SINH_KHAC, phan_tich_yeu_to_thoi_gian as DATANG_MUA
except ImportError:
    def DATANG_SINH_KHAC(h1, h2): return "Binh Hoa"
    def DATANG_MUA(h, m): return "Binh"

# V27.0: Module 6: Database tuong tac (Sao x Mon, trong so)
try:
    from database_tuong_tac import TUONG_TAC_SAO_MON, TRONG_SO_YEU_TO, ANH_HUONG_MUA as DB_MUA
except ImportError:
    TUONG_TAC_SAO_MON = {}
    TRONG_SO_YEU_TO = {}
    DB_MUA = {}

QUAI_ATTRIBUTES = {
    'Càn': {
        'hanh': 'Kim', 'chat_lieu': ['kim loại', 'vàng', 'bạc', 'đồng', 'sắt', 'thép', 'inox'],
        'hinh_dang': ['tròn', 'cầu', 'vòng', 'nguyên vẹn'], 'mau_sac': ['trắng', 'bạc', 'vàng kim'],
        'am_thanh': ['ngân nga', 'trong trẻo', 'vang'], 'dac_biet': ['cứng', 'quý', 'bền', 'sang trọng'],
        'nguoi': ['cha', 'người đàn ông lớn tuổi', 'lãnh đạo', 'vua', 'sếp', 'người quyền lực'],
        'vat': ['ngọc', 'gương', 'đồng hồ', 'nhẫn', 'vòng', 'mũ', 'ô tô', 'máy móc kim loại'],
        'noi': ['thành phố lớn', 'cung điện', 'tòa nhà cao', 'nơi sang trọng', 'phía Tây Bắc'],
        'benh': ['đầu', 'phổi', 'xương', 'cột sống'],
        'tim_do': ['phía Tây Bắc', 'nơi cao', 'chỗ kim loại', 'gần đồ quý'],
    },
    'Khôn': {
        'hanh': 'Thổ', 'chat_lieu': ['đất', 'gốm', 'sứ', 'gạch', 'xi măng', 'vải', 'bông'],
        'hinh_dang': ['vuông', 'phẳng', 'dẹt', 'rộng'], 'mau_sac': ['vàng', 'nâu', 'be'],
        'am_thanh': ['trầm', 'đục'], 'dac_biet': ['mềm', 'nặng', 'chứa đựng', 'nuôi dưỡng'],
        'nguoi': ['mẹ', 'phụ nữ lớn tuổi', 'vợ', 'nông dân', 'bà'],
        'vat': ['bao tải', 'túi', 'nồi đất', 'thảm', 'chăn', 'xe bò', 'bàn vuông'],
        'noi': ['nông thôn', 'ruộng đồng', 'mặt đất', 'phía Tây Nam', 'nhà bếp'],
        'benh': ['bụng', 'dạ dày', 'da', 'cơ bắp'],
        'tim_do': ['phía Tây Nam', 'nơi thấp', 'trong đất', 'gần ruộng'],
    },
    'Chấn': {
        'hanh': 'Mộc', 'chat_lieu': ['gỗ', 'tre', 'nứa', 'cây', 'nhựa'],
        'hinh_dang': ['dài', 'cao', 'thẳng đứng'], 'mau_sac': ['xanh lá', 'xanh dương'],
        'am_thanh': ['sấm', 'nổ', 'rung', 'kêu to', 'rền vang', 'rung động'],
        'dac_biet': ['động', 'nhanh', 'bất ngờ', 'rung lắc', 'điện', 'sấm sét'],
        'nguoi': ['con trai trưởng', 'thanh niên', 'người nhanh nhẹn', 'vận động viên'],
        'vat': ['chuông', 'loa', 'trống', 'đàn', 'nhạc cụ', 'xe cộ', 'máy rung', 'điện thoại', 'còi'],
        'noi': ['phía Đông', 'rừng', 'nơi ồn ào', 'đường phố', 'sân vận động'],
        'benh': ['chân', 'gan', 'thần kinh', 'co giật'],
        'tim_do': ['phía Đông', 'nơi ồn', 'gần cây', 'nơi rung động'],
    },
    'Tốn': {
        'hanh': 'Mộc', 'chat_lieu': ['gỗ', 'dây', 'sợi', 'lụa', 'giấy', 'vải'],
        'hinh_dang': ['dài', 'mảnh', 'uốn cong', 'mềm'], 'mau_sac': ['xanh lá', 'xanh ngọc'],
        'am_thanh': ['gió', 'vi vu', 'nhẹ nhàng'], 'dac_biet': ['mềm', 'dịu', 'thâm nhập', 'gió', 'lan tỏa'],
        'nguoi': ['con gái trưởng', 'phụ nữ trung niên', 'thương nhân', 'người đi lại nhiều'],
        'vat': ['dây', 'quạt', 'máy bay', 'hương', 'bút', 'sách', 'thư từ', 'giấy tờ'],
        'noi': ['phía Đông Nam', 'chợ', 'đường đi', 'nơi thoáng gió', 'sân bay'],
        'benh': ['đùi', 'cảm gió', 'hô hấp', 'ruột'],
        'tim_do': ['phía Đông Nam', 'nơi có gió', 'gần cây dài', 'nơi thoáng'],
    },
    'Ly': {
        'hanh': 'Hỏa', 'chat_lieu': ['lửa', 'điện', 'ánh sáng', 'nhựa', 'da'],
        'hinh_dang': ['nhọn', 'tam giác', 'rỗng giữa'], 'mau_sac': ['đỏ', 'cam', 'hồng', 'tím'],
        'am_thanh': ['nổ', 'cháy', 'lách tách'], 'dac_biet': ['sáng', 'nóng', 'đẹp', 'rỗng', 'bám dính'],
        'nguoi': ['con gái giữa', 'người đẹp', 'học giả', 'quân nhân', 'bác sĩ'],
        'vat': ['đèn', 'nến', 'gương', 'kính', 'tranh', 'vũ khí', 'máy ảnh', 'điện thoại'],
        'noi': ['phía Nam', 'nơi sáng', 'nhà bếp', 'sân khấu', 'bệnh viện'],
        'benh': ['tim', 'mắt', 'huyết áp', 'viêm'],
        'tim_do': ['phía Nam', 'nơi sáng', 'gần lửa/điện', 'nơi đẹp'],
    },
    'Khảm': {
        'hanh': 'Thủy', 'chat_lieu': ['nước', 'kính', 'chất lỏng', 'mực', 'rượu', 'xăng'],
        'hinh_dang': ['lượn sóng', 'không đều', 'có lỗ'], 'mau_sac': ['đen', 'xanh đậm', 'xanh dương'],
        'am_thanh': ['chảy', 'róc rách', 'ầm ầm'], 'dac_biet': ['hiểm', 'sâu', 'ẩm', 'lạnh', 'chảy'],
        'nguoi': ['con trai giữa', 'kẻ trộm', 'người hiểm', 'thủy thủ', 'người kinh doanh rượu'],
        'vat': ['nước', 'rượu', 'mực', 'xăng', 'bánh xe', 'gương', 'kính'],
        'noi': ['phía Bắc', 'sông hồ', 'nhà vệ sinh', 'nơi ẩm ướt', 'quán rượu'],
        'benh': ['thận', 'tai', 'bàng quang', 'huyết', 'lạnh'],
        'tim_do': ['phía Bắc', 'gần nước', 'nơi ẩm tối', 'nơi lạnh'],
    },
    'Cấn': {
        'hanh': 'Thổ', 'chat_lieu': ['đá', 'đất', 'gạch', 'xi măng', 'gốm'],
        'hinh_dang': ['vuông nhỏ', 'khối', 'lồi lõm'], 'mau_sac': ['vàng', 'nâu đất', 'xám'],
        'am_thanh': ['yên lặng', 'trầm'], 'dac_biet': ['tĩnh', 'dừng', 'ngăn cản', 'bền chắc'],
        'nguoi': ['con trai út', 'trẻ em', 'nhà sư', 'bảo vệ', 'người ít nói'],
        'vat': ['tường', 'cửa', 'tủ', 'hộp', 'đá quý', 'bàn', 'ghế'],
        'noi': ['phía Đông Bắc', 'núi', 'nơi cao', 'gần tường', 'trong hộp'],
        'benh': ['tay', 'lưng', 'xương', 'dạ dày'],
        'tim_do': ['phía Đông Bắc', 'nơi cao', 'gần tường/núi', 'trong hộp/tủ'],
    },
    'Đoài': {
        'hanh': 'Kim', 'chat_lieu': ['kim loại mỏng', 'dao', 'kéo', 'gương'],
        'hinh_dang': ['miệng mở', 'lõm', 'khuyết', 'có lỗ'], 'mau_sac': ['trắng', 'bạc', 'ánh kim'],
        'am_thanh': ['nói', 'hát', 'cười', 'ca hát', 'vui vẻ', 'vang'],
        'dac_biet': ['vui', 'giao tiếp', 'cắt', 'sắc bén', 'mở', 'hư hỏng ở miệng'],
        'nguoi': ['con gái út', 'ca sĩ', 'MC', 'diễn giả', 'thiếu nữ', 'người vui vẻ'],
        'vat': ['chén', 'cốc', 'loa', 'mic', 'kèn', 'dao', 'kéo', 'chuông nhỏ', 'tiền xu'],
        'noi': ['phía Tây', 'hồ đầm', 'quán karaoke', 'sân khấu', 'nơi vui chơi'],
        'benh': ['miệng', 'họng', 'răng', 'phổi'],
        'tim_do': ['phía Tây', 'nơi vui', 'gần ao hồ', 'nơi có tiếng'],
    },
}

# Ngũ Hành attribute mapping (bổ sung cho cross-reference)
NGU_HANH_DETECT = {
    'Kim': {'chat_lieu': ['kim loại', 'sắt', 'thép', 'vàng', 'bạc', 'đồng'], 'mau': ['trắng', 'bạc'], 'huong': 'Tây'},
    'Mộc': {'chat_lieu': ['gỗ', 'tre', 'giấy', 'vải', 'cây'], 'mau': ['xanh'], 'huong': 'Đông'},
    'Thủy': {'chat_lieu': ['nước', 'kính', 'chất lỏng', 'mực', 'rượu'], 'mau': ['đen', 'xanh đậm'], 'huong': 'Bắc'},
    'Hỏa': {'chat_lieu': ['lửa', 'điện', 'ánh sáng', 'nhựa'], 'mau': ['đỏ', 'cam'], 'huong': 'Nam'},
    'Thổ': {'chat_lieu': ['đất', 'đá', 'gạch', 'gốm', 'sứ'], 'mau': ['vàng', 'nâu'], 'huong': 'Trung ương'},
}


class FreeAIHelper:

    """
    Offline AI V34.6 — SUBJECT-FIRST DT + Detective Validator + Flexible Answers.
    V34.6: Full Năm-Tháng-Ngày-Giờ Ứng Kỳ + Vạn Vật Loại Tượng chi tiết.
    V34.4: Thám Tử Kiểm Chứng + Linh Hoạt câu trả lời (THẾ NÀO/AI/CÁI GÌ).
    V34.3: Decisive Conclusions — không còn mơ hồ (LỠ CỠ/CÒN PHẢI XEM).
    V34.2: SUBJECT-FIRST DT Engine + Word Boundary + 265 test 100%.
    Kế thừa V21.0: Weighted scoring 5 PP, Tiến/Thối Thần, Nguyệt Phá.
    Kế thừa V12.0: Lục Thân Relationship Engine.
    Kế thừa V9.0: Phản/Phục Ngâm, Tam Kỳ, Tam Tài, Không Vong.
    """
    def __init__(self, api_key=None):
        self.name = "Thiên Cơ Đại Sư (V42.2 Siêu Premium + Answer-First + 28 Handlers + VV 3378 + KV/DM Chuẩn QMDG)"
        self.version = "V35.8-Full-Pipeline"
        self.model_name = "offline-rule-engine-v35.0"
        self.logs = []
        self.learned_count = len(_load_learned_topics())
        self._api_key = api_key  # Lưu API key để gọi Gemini khi cần
        
        # V25.0: RAG Feedback Loop
        try:
            from ai_modules.feedback_rag import FeedbackRAG
            self.feedback_rag = FeedbackRAG()
        except ImportError:
            self.feedback_rag = None

    def log_step(self, step, status, detail=""):
        self.logs.append({"step": step, "status": status, "detail": detail})

    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        # V11.0: KHÔNG gọi answer_question để tránh lặp output 2 lần
        return f"⚠️ AI Online không khả dụng. Vui lòng xem kết quả AI Offline ở trên."

    def _process_response(self, text):
        return text if text else "Không có phản hồi."

    # ═══════════════════════════════════════════════════════════════
    # V31.0: SƠ ĐỒ TƯƠNG TÁC THỜI GIAN THỰC
    # ═══════════════════════════════════════════════════════════════
    
    def _fill_master_diagram(self, question, category_label, dung_than, hanh_dt,
                              unified_v22, v23_lh_factors, chart_data, luc_hao_data,
                              mai_hoa_data=None, v24_km_factors=None):
        """V34.0: Điền yếu tố THỜI GIAN THỰC vào SĐ_MASTER — 60+ yếu tố từ 6 PP.
        
        SĐ_MASTER = Sơ đồ QUAN TRỌNG NHẤT:
        DT → Suy/Vượng (3 tầng: LH + 12TS + Ngũ Khí) → Vạn Vật Loại Tượng → Chi tiết
        """
        if not DIAGRAM_MASTER:
            return "", {}
        
        # === Extract data ===
        v22 = unified_v22 or {}
        lh_raw = v22.get('lh_pct', 50)
        ts_stage = v22.get('ts_stage', 'N/A')
        ts_power = TRUONG_SINH_POWER.get(ts_stage, {}).get('power', 50) if ts_stage else 50
        ts_icon = TRUONG_SINH_POWER.get(ts_stage, {}).get('cap', '?') if ts_stage else '?'
        ts_mota = TRUONG_SINH_GIAI_THICH.get(ts_stage, '') if ts_stage else ''
        ngu_khi = v22.get('ngu_khi', '?')
        nk_power = NGU_KHI_POWER.get(ngu_khi, {}).get('power', 50) if ngu_khi else 50
        unified_pct = v22.get('unified_pct', 50)
        tier_cap = v22.get('tier_cap', '?')
        
        # Ngũ Hành vật chất
        hanh_vat = v22.get('hanh_vat', NGU_HANH_VAT_CHAT.get(hanh_dt, {}))
        vv_cu_the = v22.get('van_vat_cu_the', {})
        vv_mapping = v22.get('tier_data', {})
        
        # Chi reference cho 12 Trường Sinh
        chi_ref = ''
        if luc_hao_data:
            if isinstance(luc_hao_data, dict):
                chi_ref = luc_hao_data.get('chi_ngay', '')
            elif hasattr(luc_hao_data, 'chi_ngay'):
                chi_ref = getattr(luc_hao_data, 'chi_ngay', '')
        if not chi_ref and chart_data:
            chi_ref = chart_data.get('chi_ngay', '')
        
        # Cung hành
        cung_hanh = ''
        if chart_data:
            can_ngay = chart_data.get('can_ngay', '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            # V40.2: Giáp ẩn duới Mậu HOẶC Kỷ (tùy theo chart)
            _can_proxy = can_ngay
            if can_ngay == 'Giáp':
                # Tìm Mậu truớc, nếu không có thì tìm Kỷ
                _found_mau = any(v == 'Mậu' for v in can_thien_ban.values())
                _can_proxy = 'Mậu' if _found_mau else 'Kỷ'
            elif can_ngay == 'Kỷ': _can_proxy = 'Kỷ'
            for c_num, c_can in can_thien_ban.items():
                if c_can == _can_proxy:
                    cung_hanh = CUNG_NGU_HANH.get(int(c_num), '?') if c_num else '?'
                    break
            if not cung_hanh or cung_hanh == '?':
                # Fallback: dùng chi_ngay hành
                _chi_ngay = chart_data.get('chi_ngay', '')
                cung_hanh = CHI_NGU_HANH.get(_chi_ngay, '?')
        
        # LH factors -> extract NT, KT, Nguyệt, Nhật
        nguyet_lenh = ''
        nhat_than = ''
        nguyen_than = ''
        ky_than = ''
        nt_state = ''
        kt_state = ''
        nguyet_tac_dong = ''
        nhat_tac_dong = ''
        dac_biet = []
        lh_raw_score = 0
        
        if v23_lh_factors:
            for f in v23_lh_factors:
                if 'Nguyệt' in f and 'DT' in f:
                    # V32.5: Extract tác động chính xác
                    if 'sinh' in f: nguyet_tac_dong = 'sinh'
                    elif 'khắc' in f: nguyet_tac_dong = 'khắc'
                    elif 'tỷ hòa' in f: nguyet_tac_dong = 'tỷ hòa'
                    else: nguyet_tac_dong = 'không tác động'
                    nguyet_lenh = f.split('(')[1].split(')')[0] if '(' in f else '?'
                elif 'Nhật' in f and 'DT' in f:
                    if 'sinh' in f: nhat_tac_dong = 'sinh'
                    elif 'khắc' in f: nhat_tac_dong = 'khắc'
                    elif 'tỷ hòa' in f: nhat_tac_dong = 'tỷ hòa'
                    else: nhat_tac_dong = 'không tác động'
                    nhat_than = f.split('(')[1].split(')')[0] if '(' in f else '?'
                elif 'NT(' in f or 'Nguyên Thần' in f:
                    nguyen_than = f.split('(')[1].split(')')[0] if '(' in f else '?'
                    if 'vượng' in f.lower(): nt_state = 'Vượng'
                    elif 'suy' in f.lower(): nt_state = 'Suy'
                    elif 'động' in f.lower(): nt_state = 'Động'
                    elif 'bình' in f.lower(): nt_state = 'Bình'
                    elif 'ẩn' in f.lower(): nt_state = 'Ẩn'
                    else: nt_state = '?'
                elif 'KT(' in f or 'Kỵ Thần' in f:
                    ky_than = f.split('(')[1].split(')')[0] if '(' in f else '?'
                    if 'vượng+động' in f.lower(): kt_state = 'Vượng+Động'
                    elif 'vượng' in f.lower(): kt_state = 'Vượng'
                    elif 'suy' in f.lower(): kt_state = 'Suy'
                    elif 'động' in f.lower(): kt_state = 'Động'
                    elif 'bình' in f.lower(): kt_state = 'Bình'
                    elif 'ẩn' in f.lower(): kt_state = 'Ẩn'
                    else: kt_state = '?'
                elif 'THAM SINH' in f.upper():
                    dac_biet.append('⚡ THAM SINH VONG KHẮC')
                elif 'PHẢN NGÂM' in f.upper():
                    dac_biet.append('🔄 Phản Ngâm')
                elif 'PHỤC NGÂM' in f.upper():
                    dac_biet.append('🔄 Phục Ngâm')
                elif 'Tuần Không' in f:
                    dac_biet.append('⭕ Tuần Không')
                elif 'Nguyệt Phá' in f:
                    dac_biet.append('💥 Nguyệt Phá')
            
            # LH raw score 
            for f in v23_lh_factors:
                try:
                    parts = f.split()
                    for p in parts:
                        if p.startswith('+') or p.startswith('-'):
                            lh_raw_score += int(p)
                            break
                except:
                    pass
        
        # V32.5: Fallback Nguyệt/Nhật nếu v23_lh_factors không có
        if not nguyet_lenh or nguyet_lenh == '?':
            try:
                import datetime as _dt_fm
                from qmdg_calc import calculate_qmdg_params as _calc_fm
                _pf = _calc_fm(_dt_fm.datetime.now())
                nguyet_lenh = _pf.get('chi_thang', '?')
                if not nhat_than or nhat_than == '?':
                    nhat_than = _pf.get('can_ngay', '?')
            except:
                pass
        
        dac_biet_str = ', '.join(dac_biet) if dac_biet else 'Không có'
        
        # Build short question
        q_short = question[:40] + '...' if len(question) > 40 else question
        
        # ═══ V34.0: EXTRACT ALL NEW FACTORS ═══
        
        # --- LỤC HÀO: Biến Hào, Lục Hợp/Xung, Tam Hợp, Phục Thần ---
        cuu_than = ''
        cuu_state = ''
        tuan_khong_str = ''
        nguyet_pha_str = ''
        tsvk_str = ''
        phan_phuc_str = ''
        the_state = ''
        ung_state = ''
        bien_hao_str = 'Không biến'
        dong_hao_list_str = 'Không có'
        bien_que_str = ''
        bien_hao_dt_str = ''
        luc_hop_xung_str = 'Không phát hiện'
        tam_hop_cuc_str = 'Không phát hiện' 
        tien_thoai_str = 'N/A'
        phuc_than_str = 'Không có'
        
        if v23_lh_factors:
            for f in v23_lh_factors:
                f_upper = f.upper()
                if 'CỪU' in f_upper or 'Cừu' in f:
                    cuu_than = f.split('(')[1].split(')')[0] if '(' in f else '?'
                    if 'vượng' in f.lower(): cuu_state = 'Vượng'
                    elif 'suy' in f.lower(): cuu_state = 'Suy'
                    elif 'động' in f.lower(): cuu_state = 'Động'
                    elif 'khắc' in f.lower(): cuu_state = 'Khắc KT'
                    elif '+' in f: cuu_state = 'Hỗ trợ'
                    elif '-' in f: cuu_state = 'Tiếp sức KT'
                    else: cuu_state = 'Có'
                elif 'TUẦN KHÔNG' in f_upper:
                    tuan_khong_str = f
                elif 'NGUYỆT PHÁ' in f_upper:
                    nguyet_pha_str = f
                elif 'THAM SINH' in f_upper:
                    tsvk_str = f
                elif 'PHẢN NGÂM' in f_upper:
                    phan_phuc_str += 'Phản Ngâm '
                elif 'PHỤC NGÂM' in f_upper:
                    phan_phuc_str += 'Phục Ngâm '
                elif 'Thế(' in f and 'Ứng(' in f:
                    # V34.0: Match "Thế(Thân/Kim) khắc Ứng(Hợi/Thủy)" 
                    import re as _re_tu
                    _m_the = _re_tu.search(r'Thế\(([^)]+)\)', f)
                    _m_ung = _re_tu.search(r'Ứng\(([^)]+)\)', f)
                    if _m_the: the_state = _m_the.group(1)
                    if _m_ung: ung_state = _m_ung.group(1)
                elif 'THẾ' in f and 'ỨNG' not in f and ('vượng' in f.lower() or 'suy' in f.lower()):
                    the_state = f
                elif 'ỨNG' in f and ('vượng' in f.lower() or 'suy' in f.lower()):
                    ung_state = f
                elif 'LỤC HỢP' in f_upper or 'LỤC XUNG' in f_upper:
                    luc_hop_xung_str = f
                elif 'hợp dt' in f.lower() or ('hợp' in f.lower() and 'dt' in f_upper):
                    luc_hop_xung_str = f'☯ {f}'
                elif 'xung dt' in f.lower() or 'ÁM ĐỘNG' in f_upper:
                    if luc_hop_xung_str == 'Không phát hiện': luc_hop_xung_str = f'⚡ {f}'
                    else: luc_hop_xung_str += f' | ⚡ {f}'
                elif 'TAM HỢP' in f_upper or 'Tam Hợp' in f:
                    tam_hop_cuc_str = f
                elif 'TIẾN THẦN' in f_upper:
                    tien_thoai_str = 'Tiến Thần ↗'
                elif 'THOÁI THẦN' in f_upper:
                    tien_thoai_str = 'Thoái Thần ↘'
                elif 'Hóa Hồi' in f or 'Hóa Phục' in f or 'Hóa TUYỆT' in f or 'Hóa MỘ' in f:
                    # V34.0: Capture Hóa Hồi Đầu info
                    if not bien_hao_dt_str or bien_hao_dt_str == '?':
                        bien_hao_dt_str = f
        
        # V34.0: Fallback Thế/Ứng + Cừu từ luc_hao_data nếu v23 không cung cấp
        if luc_hao_data and isinstance(luc_hao_data, dict):
            if not the_state or not ung_state:
                _haos_fb = (luc_hao_data.get('haos', []) or 
                           luc_hao_data.get('hao', []) or
                           luc_hao_data.get('hao_list', []))
                if not _haos_fb:
                    _ban_fb = luc_hao_data.get('ban', {})
                    if _ban_fb:
                        _haos_fb = _ban_fb.get('haos', []) or _ban_fb.get('details', [])
                for _hfb in _haos_fb:
                    if isinstance(_hfb, dict):
                        _tu_fb = str(_hfb.get('the_ung', '') or _hfb.get('marker', ''))
                        _chi_fb = _hfb.get('chi', '?')
                        _hanh_fb = _hfb.get('hanh', '') or _hfb.get('ngu_hanh', '?')
                        if 'Thế' in _tu_fb and not the_state:
                            the_state = f"{_chi_fb}/{_hanh_fb}"
                        elif 'Ứng' in _tu_fb and not ung_state:
                            ung_state = f"{_chi_fb}/{_hanh_fb}"
            if not cuu_than:
                _cuu_fb = luc_hao_data.get('cuu_than', '')
                if _cuu_fb:
                    cuu_than = str(_cuu_fb)
                    cuu_state = cuu_state or 'Có'
                else:
                    cuu_than = 'N/A'
                    cuu_state = 'N/A'
        
        # Extract Biến Hào, Phục Thần from luc_hao_data
        if luc_hao_data and isinstance(luc_hao_data, dict):
            # Biến Hào 
            dong_hao = luc_hao_data.get('dong_hao', [])
            if dong_hao:
                dong_hao_list_str = ', '.join([f'Hào {h}' for h in dong_hao])
                bien = luc_hao_data.get('bien', {})
                if bien:
                    bien_que_str = bien.get('name', '?')
                    bien_details = bien.get('details', [])
                    # Tìm hào biến DT
                    for dh in dong_hao:
                        for bd in bien_details:
                            if isinstance(bd, dict) and bd.get('hao') == dh:
                                bien_hao_dt_str += f"Hào {dh} biến {bd.get('luc_than', '?')} ({bd.get('can_chi', '?')}) "
                bien_hao_str = f"Hào {', '.join(map(str, dong_hao))} ĐỘNG → Biến {bien_que_str}"
            
            # Phục Thần
            phuc_than = luc_hao_data.get('phuc_than', [])
            if phuc_than:
                pts = []
                for pt in phuc_than:
                    if isinstance(pt, dict):
                        pts.append(f"{pt.get('luc_than', '?')} ({pt.get('can_chi', '?')}) ẩn dưới hào {pt.get('hao_pos', '?')}")
                if pts:
                    phuc_than_str = ' | '.join(pts)
        
        # --- KỲ MÔN: Trực Phù/Sử, Không Vong, Mã Tinh, Tam Kỳ, Cục, 4 Trụ ---
        truc_phu = ''
        truc_su = ''
        khong_vong_km = ''
        ma_tinh = ''
        tam_ky = 'Không có'
        km_cuc = ''
        am_duong_don = ''
        tu_tru = ''
        cung_dt_str = ''
        cung_dt_hanh_str = ''
        sao_dt_str = ''
        cua_dt_str = ''
        than_dt_str = ''
        cung_bt_str = ''
        cung_sv_str = ''
        bt_sv_rel_str = ''
        dia_ban_dt_str = ''
        km_phan_phuc_str = 'Không có'
        
        if chart_data and isinstance(chart_data, dict):
            truc_phu = chart_data.get('truc_phu', '?')
            truc_su = chart_data.get('truc_su', '?')
            
            # Không Vong
            kv = chart_data.get('khong', {})
            if kv:
                kv_parts = []
                for period, cung_list in kv.items():
                    if isinstance(cung_list, list):
                        kv_parts.append(f"{period}: Cung {','.join(map(str, cung_list))}")
                khong_vong_km = ' | '.join(kv_parts) if kv_parts else '?'
            
            # Mã Tinh
            ma = chart_data.get('ma', {})
            if ma:
                ma_tinh = f"Giờ:{ma.get('gio','N/A')} Ngày:{ma.get('ngay','N/A')}"
                _ma_thang = ma.get('thang', '')
                _ma_nam = ma.get('nam', '')
                if _ma_thang: ma_tinh += f" Tháng:{_ma_thang}"
                if _ma_nam: ma_tinh += f" Năm:{_ma_nam}"
            
            # Tam Kỳ (Ất/Bính/Đinh)
            can_ngay_km = chart_data.get('can_ngay', '')
            if can_ngay_km in ['Ất', 'Bính', 'Đinh']:
                tam_ky = f"{can_ngay_km} (Tam Kỳ)"
            
            # Cục 
            km_cuc = str(chart_data.get('cuc', '?'))
            am_duong_don = 'Dương Độn' if chart_data.get('is_duong_don') else 'Âm Độn'
            
            # 4 Trụ
            tu_tru = (
                f"Năm: {chart_data.get('can_nam', '?')}{chart_data.get('chi_nam', '?')} | "
                f"Tháng: {chart_data.get('can_thang', '?')}{chart_data.get('chi_thang', '?')} | "
                f"Ngày: {chart_data.get('can_ngay', '?')}{chart_data.get('chi_ngay', '?')} | "
                f"Giờ: {chart_data.get('can_gio', '?')}{chart_data.get('chi_gio', '?')}"
            )
            
            # V34.0: Extract Cung/Sao/Cửa/Thần DT TRỰC TIẾP từ chart_data
            can_thien_ban = chart_data.get('can_thien_ban', {})
            thien_ban = chart_data.get('thien_ban', {})
            nhan_ban = chart_data.get('nhan_ban', {})
            than_ban = chart_data.get('than_ban', {})
            
            # Tìm Cung DT
            _dt_can_map_km = {
                'Quan Quỷ': chart_data.get('can_gio', ''),
                'Thê Tài': chart_data.get('can_gio', ''),
                'Tử Tôn': chart_data.get('can_gio', ''),
                'Phụ Mẫu': chart_data.get('can_nam', ''),
                'Huynh Đệ': chart_data.get('can_thang', ''),
                'Bản Thân': can_ngay_km,
            }
            _dt_can_km = _dt_can_map_km.get(dung_than, chart_data.get('can_gio', ''))
            _dt_cung_num = None
            _bt_cung_num = None
            for _cn, _cv in can_thien_ban.items():
                if _cv == can_ngay_km: _bt_cung_num = int(_cn) if _cn else None
                if not _bt_cung_num and can_ngay_km == 'Giáp' and _cv in ('Mậu', 'Kỷ'): _bt_cung_num = int(_cn) if _cn else None
            for _cn, _cv in can_thien_ban.items():
                if _cv == _dt_can_km: _dt_cung_num = int(_cn) if _cn else None
                if not _dt_cung_num and _dt_can_km == 'Giáp' and _cv in ('Mậu', 'Kỷ'): _dt_cung_num = int(_cn) if _cn else None
            
            if _dt_cung_num:
                _dt_cung_hanh = CUNG_NGU_HANH.get(_dt_cung_num, '?')
                cung_dt_str = str(_dt_cung_num)
                cung_dt_hanh_str = _dt_cung_hanh
                # Sao
                _sao_raw = thien_ban.get(_dt_cung_num, thien_ban.get(str(_dt_cung_num), '?'))
                sao_dt_str = str(_sao_raw)
                # Cửa
                _cua_raw = nhan_ban.get(_dt_cung_num, nhan_ban.get(str(_dt_cung_num), '?'))
                cua_dt_str = str(_cua_raw)
                # Thần
                _than_raw = than_ban.get(_dt_cung_num, than_ban.get(str(_dt_cung_num), '?'))
                than_dt_str = str(_than_raw)
                # BT Cung
                if _bt_cung_num:
                    cung_bt_str = str(_bt_cung_num)
                    _bt_hanh = CUNG_NGU_HANH.get(_bt_cung_num, '?')
                    # BT↔SV relation
                    if _dt_cung_hanh and _bt_hanh and _bt_hanh != '?':
                        if SINH.get(_bt_hanh) == _dt_cung_hanh: bt_sv_rel_str = '→ BT sinh DT (CÁT)'
                        elif KHAC.get(_bt_hanh) == _dt_cung_hanh: bt_sv_rel_str = '→ BT khắc DT'
                        elif SINH.get(_dt_cung_hanh) == _bt_hanh: bt_sv_rel_str = '→ DT sinh BT (hao)'
                        elif KHAC.get(_dt_cung_hanh) == _bt_hanh: bt_sv_rel_str = '→ DT khắc BT (chủ động)'
                        elif _bt_hanh == _dt_cung_hanh: bt_sv_rel_str = '→ Tỷ Hòa'
                # Cung SV (= Cung DT trong most cases)
                cung_sv_str = cung_dt_str
                # Địa Bàn DT
                _DIA_BAN_CAN = {1: 'Mậu', 2: 'Kỷ', 3: 'Canh', 4: 'Tân', 5: 'Mậu', 6: 'Nhâm', 7: 'Quý', 8: 'Ất', 9: 'Bính'}
                _dia_can = _DIA_BAN_CAN.get(_dt_cung_num, '?')
                dia_ban_dt_str = f"Can {_dia_can} (Địa Bàn Cung {_dt_cung_num})"
                # Phản/Phục Ngâm cung
                _dac_biet_km = chart_data.get('dac_biet', [])
                if isinstance(_dac_biet_km, list):
                    for _db in _dac_biet_km:
                        _db_str = str(_db).upper()
                        if 'PHẢN NGÂM' in _db_str: km_phan_phuc_str = '🔄 Phản Ngâm (Thiên Bàn xung Địa Bàn)'
                        elif 'PHỤC NGÂM' in _db_str: km_phan_phuc_str = '🔄 Phục Ngâm (Thiên Bàn = Địa Bàn)'
        
        # Fallback: parse v24_km_factors text nếu direct extract failed
        if (not cung_dt_str or cung_dt_str == '?') and v24_km_factors:
            for f in v24_km_factors if isinstance(v24_km_factors, list) else []:
                f_str = str(f)
                if 'Cung DT' in f_str or 'cung_dt' in f_str:
                    cung_dt_str = f_str
                elif 'Sao' in f_str and 'DT' in f_str:
                    sao_dt_str = f_str
                elif 'Cửa' in f_str and 'DT' in f_str:
                    cua_dt_str = f_str
                elif 'Thần' in f_str and 'DT' in f_str:
                    than_dt_str = f_str
                elif 'BT' in f_str and 'SV' in f_str:
                    bt_sv_rel_str = f_str
        
        # --- MAI HOA: Thể/Dụng Vượng Suy, Hỗ Quái, Biến Quái ---
        the_quai_str = ''
        the_quai_hanh_str = ''
        the_vuong_suy = ''
        dung_quai_str = ''
        dung_quai_hanh_str = ''
        dung_vuong_suy = ''
        ho_quai_str = ''
        bien_quai_mh_str = ''
        the_dung_rel_str = ''
        the_dung_y_nghia_str = ''
        ho_the_rel_str = ''
        ho_the_y_nghia_str = ''
        ho_dung_rel_str = ''
        ho_dung_y_nghia_str = ''
        dong_hao_mh_str = '?'
        mh_interpretation_str = ''
        
        if mai_hoa_data and isinstance(mai_hoa_data, dict):
            the_quai_str = mai_hoa_data.get('upper_symbol', mai_hoa_data.get('ten_thuong', '?'))
            the_quai_hanh_str = mai_hoa_data.get('upper_element', mai_hoa_data.get('hanh_thuong', '?'))
            dung_quai_str = mai_hoa_data.get('lower_symbol', mai_hoa_data.get('ten_ha', '?'))
            dung_quai_hanh_str = mai_hoa_data.get('lower_element', mai_hoa_data.get('hanh_ha', '?'))
            ho_quai_str = mai_hoa_data.get('ten_ho', '?')
            bien_quai_mh_str = mai_hoa_data.get('ten_qua_bien', '?')
            dong_hao_mh_str = str(mai_hoa_data.get('dong_hao', '?'))
            mh_interpretation_str = mai_hoa_data.get('interpretation', mai_hoa_data.get('nghĩa', ''))[:80]
            
            # Thể/Dụng Vượng Suy (theo tháng hiện tại)
            chi_thang = ''
            if chart_data:
                chi_thang = chart_data.get('chi_thang', '')
            mua_hanh = CHI_NGU_HANH.get(chi_thang, '')
            if the_quai_hanh_str and mua_hanh:
                if the_quai_hanh_str == mua_hanh:
                    the_vuong_suy = 'VƯỢNG (đương lệnh)'
                elif SINH.get(mua_hanh) == the_quai_hanh_str:
                    the_vuong_suy = 'TƯỚNG (được sinh)'
                elif SINH.get(the_quai_hanh_str) == mua_hanh:
                    the_vuong_suy = 'HƯU (tiết khí)'
                elif KHAC.get(the_quai_hanh_str) == mua_hanh:
                    the_vuong_suy = 'TÙ (bị tiết)'
                elif KHAC.get(mua_hanh) == the_quai_hanh_str:
                    the_vuong_suy = 'TỬ (bị khắc)'
                else:
                    the_vuong_suy = '?'
            if dung_quai_hanh_str and mua_hanh:
                if dung_quai_hanh_str == mua_hanh:
                    dung_vuong_suy = 'VƯỢNG'
                elif SINH.get(mua_hanh) == dung_quai_hanh_str:
                    dung_vuong_suy = 'TƯỚNG'
                elif SINH.get(dung_quai_hanh_str) == mua_hanh:
                    dung_vuong_suy = 'HƯU'
                elif KHAC.get(dung_quai_hanh_str) == mua_hanh:
                    dung_vuong_suy = 'TÙ'
                elif KHAC.get(mua_hanh) == dung_quai_hanh_str:
                    dung_vuong_suy = 'TỬ'
                else:
                    dung_vuong_suy = '?'
            
            # Thể↔Dụng quan hệ
            if the_quai_hanh_str and dung_quai_hanh_str:
                if SINH.get(the_quai_hanh_str) == dung_quai_hanh_str:
                    the_dung_rel_str = 'sinh'
                    the_dung_y_nghia_str = 'Thể sinh Dụng → hao tổn, bất lợi cho ta'
                elif SINH.get(dung_quai_hanh_str) == the_quai_hanh_str:
                    the_dung_rel_str = 'được sinh'
                    the_dung_y_nghia_str = 'Dụng sinh Thể → CÁT, thuận lợi'
                elif KHAC.get(the_quai_hanh_str) == dung_quai_hanh_str:
                    the_dung_rel_str = 'khắc'
                    the_dung_y_nghia_str = 'Thể khắc Dụng → ta thắng, CÁT'
                elif KHAC.get(dung_quai_hanh_str) == the_quai_hanh_str:
                    the_dung_rel_str = 'bị khắc'
                    the_dung_y_nghia_str = 'Dụng khắc Thể → ta bị hại, HUNG'
                elif the_quai_hanh_str == dung_quai_hanh_str:
                    the_dung_rel_str = 'tỷ hòa'
                    the_dung_y_nghia_str = 'Thể Dụng đồng hành → hòa hợp, bình thường'
            
            # V34.0: Hỗ Quái → Thể/Dụng quan hệ
            ho_hanh = mai_hoa_data.get('hanh_ho', '')
            if not ho_hanh and ho_quai_str and ho_quai_str != '?':
                # Derive hành from quái name
                _quai_hanh_map = {'Càn': 'Kim', 'Đoài': 'Kim', 'Ly': 'Hỏa', 'Chấn': 'Mộc',
                                  'Tốn': 'Mộc', 'Khảm': 'Thủy', 'Cấn': 'Thổ', 'Khôn': 'Thổ'}
                for _qn, _qh in _quai_hanh_map.items():
                    if _qn in ho_quai_str:
                        ho_hanh = _qh
                        break
            if ho_hanh and the_quai_hanh_str:
                if SINH.get(ho_hanh) == the_quai_hanh_str:
                    ho_the_rel_str = 'sinh'
                    ho_the_y_nghia_str = 'Hỗ sinh Thể → nội lực hỗ trợ'
                elif KHAC.get(ho_hanh) == the_quai_hanh_str:
                    ho_the_rel_str = 'khắc'
                    ho_the_y_nghia_str = 'Hỗ khắc Thể → nội bộ trở ngại'
                elif SINH.get(the_quai_hanh_str) == ho_hanh:
                    ho_the_rel_str = 'tiết'
                    ho_the_y_nghia_str = 'Thể sinh Hỗ → hao tổn nội lực'
                elif KHAC.get(the_quai_hanh_str) == ho_hanh:
                    ho_the_rel_str = 'bị khắc'
                    ho_the_y_nghia_str = 'Thể khắc Hỗ → kiểm soát nội bộ'
                elif ho_hanh == the_quai_hanh_str:
                    ho_the_rel_str = 'tỷ hòa'
                    ho_the_y_nghia_str = 'Hỗ đồng hành Thể'
            if ho_hanh and dung_quai_hanh_str:
                if SINH.get(ho_hanh) == dung_quai_hanh_str:
                    ho_dung_rel_str = 'sinh'
                    ho_dung_y_nghia_str = 'Hỗ sinh Dụng → ẩn ý tăng cường'
                elif KHAC.get(ho_hanh) == dung_quai_hanh_str:
                    ho_dung_rel_str = 'khắc'
                    ho_dung_y_nghia_str = 'Hỗ khắc Dụng → ẩn ý cản trở'
                elif SINH.get(dung_quai_hanh_str) == ho_hanh:
                    ho_dung_rel_str = 'tiết'
                    ho_dung_y_nghia_str = 'Dụng sinh Hỗ → hao tổn'
                elif KHAC.get(dung_quai_hanh_str) == ho_hanh:
                    ho_dung_rel_str = 'bị khắc'
                    ho_dung_y_nghia_str = 'Dụng khắc Hỗ'
                elif ho_hanh == dung_quai_hanh_str:
                    ho_dung_rel_str = 'tỷ hòa'
                    ho_dung_y_nghia_str = 'Hỗ đồng hành Dụng'
        
        # --- V34.0: ĐẠI LỤC NHÂM — GỌI TRỰC TIẾP OFFLINE ENGINE ---
        so_truyen = '?'
        trung_truyen = '?'
        mat_truyen = '?'
        thien_tuong = '?'
        tu_khoa = 'N/A'
        can_chi_lac_cung = 'N/A'
        
        try:
            from dai_luc_nham import tinh_dai_luc_nham as _dln_calc, CAN_KY_CHI as _DLN_CAN_KY
            if chart_data and chart_data.get('can_ngay'):
                _dln = _dln_calc(
                    chart_data.get('can_ngay', 'Giáp'),
                    chart_data.get('chi_ngay', 'Tý'),
                    chart_data.get('chi_gio', 'Ngọ'),
                    chart_data.get('tiet_khi', 'Đông Chí')
                )
                _tt = _dln.get('tam_truyen', {})
                so_truyen = f"{_tt.get('so_truyen', '?')} ({_tt.get('so_truyen_hanh', '?')})"
                trung_truyen = f"{_tt.get('trung_truyen', '?')} ({_tt.get('trung_truyen_hanh', '?')})"
                mat_truyen = f"{_tt.get('mat_truyen', '?')} ({_tt.get('mat_truyen_hanh', '?')})"
                # Thiên Tướng Sơ Truyền
                _tt_full = _dln.get('thien_tuong_full', {})
                _so_chi = _tt.get('so_truyen', '')
                _tuong = _tt_full.get(_so_chi, {})
                thien_tuong = _tuong.get('ten', '?') if _tuong else '?'
                # Tứ Khóa summary
                _tk = _dln.get('tu_khoa', [])
                if _tk:
                    tu_khoa = ' | '.join([f"K{i+1}: {k.get('thien','?')}/{k.get('dia','?')}" for i, k in enumerate(_tk)])
                # Can Chi lạc cung
                _can_ky = _DLN_CAN_KY.get(chart_data.get('can_ngay', ''), '?')
                can_chi_lac_cung = f"Can {chart_data.get('can_ngay','')} ký tại {_can_ky}"
        except Exception:
            pass
        
        # --- V34.0: THIẾT BẢN + THÁI ẤT — GỌI TRỰC TIẾP ---
        nap_am_ten = '?'
        nap_am_hanh = '?'
        nap_am_giai_thich = ''
        chu_khach = '?'
        ta_cuc = '?'
        
        # Extract Nạp Âm from chart_data
        if chart_data and isinstance(chart_data, dict):
            nap_am_ten = chart_data.get('nap_am', chart_data.get('nap_am_ten', '?'))
            nap_am_hanh = chart_data.get('nap_am_hanh', '?') 
            nap_am_giai_thich = chart_data.get('nap_am_giai_thich', '')
        
        # V34.0: Gọi Thái Ất trực tiếp
        try:
            from thai_at_than_so import tinh_thai_at_than_so as _ta_calc
            import datetime as _dt_ta
            _now_ta = _dt_ta.datetime.now()
            _ta_can = chart_data.get('can_ngay', 'Giáp') if chart_data else 'Giáp'
            _ta_chi = chart_data.get('chi_ngay', 'Tý') if chart_data else 'Tý'
            _ta_data = _ta_calc(_now_ta.year, _now_ta.month, _ta_can, _ta_chi)
            # Chủ↔Khách
            _bat_tuong = _ta_data.get('bat_tuong', {})
            _chu = _bat_tuong.get('Chủ Đại Tướng', {})
            _khach = _bat_tuong.get('Khách Đại Tướng', {})
            if _chu and _khach:
                _chu_h = _chu.get('hanh_cung', '?')
                _khach_h = _khach.get('hanh_cung', '?')
                _ta_rel = ''
                if _chu_h and _khach_h and _chu_h != '?' and _khach_h != '?':
                    if KHAC.get(_chu_h) == _khach_h: _ta_rel = 'Chủ KHẮC Khách → CÁT'
                    elif KHAC.get(_khach_h) == _chu_h: _ta_rel = 'Khách KHẮC Chủ → HUNG'
                    elif SINH.get(_khach_h) == _chu_h: _ta_rel = 'Khách SINH Chủ → CÁT'
                    elif SINH.get(_chu_h) == _khach_h: _ta_rel = 'Chủ SINH Khách → HUNG'
                    else: _ta_rel = 'Tỷ Hòa'
                chu_khach = f"Chủ({_chu_h}) vs Khách({_khach_h}) → {_ta_rel}"
            # Cách Cục
            _cach_cuc = _ta_data.get('cach_cuc', [])
            if _cach_cuc:
                ta_cuc = ' | '.join([cc[:30] for cc in _cach_cuc[:3]])
            else:
                ta_cuc = 'Không có cách cục đặc biệt'
        except Exception:
            pass
        
        # === V34.0: FIX ALL REMAINING '?' SLOTS ===
        
        # --- 1) NHẬT THẦN: extract từ chart_data nếu v23 không có ---
        if (not nhat_than or nhat_than == '?') and chart_data:
            _nt_can = chart_data.get('can_ngay', '')
            _nt_chi = chart_data.get('chi_ngay', '')
            if _nt_can and _nt_chi:
                nhat_than = f"{_nt_chi}/{CHI_NGU_HANH.get(_nt_chi, '?')}"
                # Tính tác động: Nhật Thần hành vs DT hành
                _nt_hanh = CHI_NGU_HANH.get(_nt_chi, '')
                if _nt_hanh and hanh_dt:
                    if _nt_hanh == hanh_dt: nhat_tac_dong = 'tỷ hòa'
                    elif SINH.get(_nt_hanh) == hanh_dt: nhat_tac_dong = 'sinh'
                    elif KHAC.get(_nt_hanh) == hanh_dt: nhat_tac_dong = 'khắc'
                    elif SINH.get(hanh_dt) == _nt_hanh: nhat_tac_dong = 'bị tiết'
                    elif KHAC.get(hanh_dt) == _nt_hanh: nhat_tac_dong = 'bị khắc'
                    else: nhat_tac_dong = 'không tác động'
        
        # --- 2) THẾ/ỨNG: extract vượng suy từ luc_hao_data ---
        if (not the_state or the_state == '?') and luc_hao_data and isinstance(luc_hao_data, dict):
            ban = luc_hao_data.get('ban', {})
            haos = ban.get('haos', [])
            for hao in haos:
                if isinstance(hao, dict):
                    _tu = hao.get('the_ung', '')
                    if _tu == 'Thế':
                        _vs = hao.get('vuong_suy', '?')
                        _lt = hao.get('luc_than', '?')
                        _chi = hao.get('chi', '?')
                        the_state = f"{_lt}({_chi}) {_vs}"
                    elif _tu == 'Ứng':
                        _vs = hao.get('vuong_suy', '?')
                        _lt = hao.get('luc_than', '?')
                        _chi = hao.get('chi', '?')
                        ung_state = f"{_lt}({_chi}) {_vs}"
        
        # --- 3) CỬU THẦN: Cửu Thần = hành khắc Kỵ Thần ---
        if (not cuu_than or cuu_than == '?') and ky_than:
            _kt_hanh = ky_than  # ky_than đã là hành (VD: 'Thủy')
            if _kt_hanh in KHAC:
                # Cửu Thần khắc Kỵ Thần → tìm hành khắc KT
                for _h, _k in KHAC.items():
                    if _k == _kt_hanh:
                        cuu_than = _h
                        cuu_state = 'Hỗ trợ DT'
                        break
        
        # --- 4) NẠP ÂM GIẢI THÍCH ---
        if (not nap_am_giai_thich or nap_am_giai_thich == '?') and nap_am_ten and nap_am_ten != '?':
            _NAP_AM_GIAI = {
                'Hải Trung Kim': 'Vàng trong biển — tiềm ẩn, chưa lộ',
                'Lô Trung Hỏa': 'Lửa trong lò — sức mạnh kiểm soát',
                'Đại Lâm Mộc': 'Cây rừng lớn — vững chắc, che chở',
                'Lộ Bàng Thổ': 'Đất bên đường — khiêm tốn, phổ thông',
                'Kiếm Phong Kim': 'Vàng mũi kiếm — sắc bén, quyết đoán',
                'Sơn Đầu Hỏa': 'Lửa trên núi — tỏa sáng, uy nghi',
                'Giản Hạ Thủy': 'Nước khe suối — linh hoạt, trong sáng',
                'Thành Đầu Thổ': 'Đất trên thành — vững chãi, bảo vệ',
                'Bạch Lạp Kim': 'Vàng sáp trắng — mềm dẻo, tinh tế',
                'Dương Liễu Mộc': 'Cây dương liễu — mềm mại, uyển chuyển',
                'Tuyền Trung Thủy': 'Nước trong suối — thanh tịnh, ẩn giấu',
                'Ốc Thượng Thổ': 'Đất trên mái — cao sang, bền vững',
                'Bích Thượng Thổ': 'Đất trên tường — kiên cố, bảo vệ',
                'Kim Bạc Kim': 'Vàng lá mỏng — quý nhưng mỏng manh',
                'Phú Đăng Hỏa': 'Lửa đèn dầu — nhỏ nhưng sáng',
                'Thiên Hà Thủy': 'Nước sông Ngân — may mắn, quý hiếm',
                'Đại Dịch Thổ': 'Đất trạm dịch — rộng lớn, phát triển',
                'Thoa Xuyến Kim': 'Vàng trang sức — đẹp đẽ, giá trị',
                'Tang Đố Mộc': 'Gỗ cây dâu — cứng cáp, hữu dụng',
                'Đại Khê Thủy': 'Nước suối lớn — dồi dào, thuận lợi',
                'Sa Trung Thổ': 'Đất trong cát — mong manh, bất ổn',
                'Thiên Thượng Hỏa': 'Lửa trên trời — mạnh mẽ, tỏa sáng',
                'Thạch Lựu Mộc': 'Cây lựu đá — cứng cáp, sống dai',
                'Đại Hải Thủy': 'Nước biển lớn — bao la, khó kiểm soát',
                'Sa Trung Kim': 'Vàng trong cát — tiềm ẩn giá trị',
                'Sơn Hạ Hỏa': 'Lửa dưới núi — âm ỉ, tiềm tàng',
                'Bình Địa Mộc': 'Cây đồng bằng — thẳng thắn, phát triển',
                'Trường Lưu Thủy': 'Nước chảy dài — bền bỉ, kiên trì',
                'Tích Lịch Hỏa': 'Lửa sấm sét — bùng nổ, mãnh liệt',
                'Tùng Bách Mộc': 'Cây tùng bách — trường thọ, kiên cường',
            }
            nap_am_giai_thich = _NAP_AM_GIAI.get(nap_am_ten, f'{nap_am_ten} — {nap_am_hanh}')
        
        # --- 5) VẠN VẬT CỤ THỂ FALLBACK ---
        if not vv_cu_the or all(v == '?' for v in vv_cu_the.values() if isinstance(v, str)):
            _VV_FALLBACK = {
                'Kim': {'do_vat': 'Dao, kéo, kim loại, trang sức', 'nha_cua': 'Nhà kiên cố, tường cao',
                        'nguoi': 'Người cương nghị, quyết đoán', 'benh': 'Phổi, hô hấp, xương'},
                'Mộc': {'do_vat': 'Sách, vải, đồ gỗ, cây cối', 'nha_cua': 'Nhà gỗ, gần cây xanh',
                        'nguoi': 'Người nhân từ, thanh cao', 'benh': 'Gan, mật, gân cốt'},
                'Thủy': {'do_vat': 'Nước, rượu, mực, đồ lỏng', 'nha_cua': 'Nhà gần sông, ao hồ',
                        'nguoi': 'Người thông minh, linh hoạt', 'benh': 'Thận, bàng quang, tai'},
                'Hỏa': {'do_vat': 'Đèn, lửa, điện tử, sách vở', 'nha_cua': 'Nhà hướng Nam, nhiều ánh sáng',
                        'nguoi': 'Người sôi nổi, nhiệt tình', 'benh': 'Tim, mắt, huyết áp'},
                'Thổ': {'do_vat': 'Gạch, đá, gốm sứ, xi măng', 'nha_cua': 'Nhà trệt, nền đất rộng',
                        'nguoi': 'Người trung thực, đáng tin', 'benh': 'Dạ dày, tỳ vị, cơ bắp'},
            }
            _fb = _VV_FALLBACK.get(hanh_dt, {})
            if _fb:
                vv_cu_the = _fb
        
        # --- 6) VẠN VẬT MAPPING FALLBACK ---  
        _VV_TIER_MAPPING = {
            'VƯỢNG': {'kich_thuoc': 'Lớn', 'tinh_trang': 'Mới, tốt', 'so_luong': 'Nhiều', 'chat_luong': 'Cao', 'con_nguoi': 'Khỏe mạnh, thành đạt'},
            'TRUNG BÌNH': {'kich_thuoc': 'Vừa', 'tinh_trang': 'Bình thường', 'so_luong': 'Vừa phải', 'chat_luong': 'Trung bình', 'con_nguoi': 'Bình thường, ổn định'},
            'SUY': {'kich_thuoc': 'Nhỏ', 'tinh_trang': 'Cũ, hỏng', 'so_luong': 'Ít', 'chat_luong': 'Thấp', 'con_nguoi': 'Yếu, khó khăn'},
        }
        _tier_key = tier_cap if tier_cap in _VV_TIER_MAPPING else 'TRUNG BÌNH'
        if not vv_mapping or all(vv_mapping.get(k) in ('?', None, '') for k in ['kich_thuoc', 'tinh_trang']):
            vv_mapping = _VV_TIER_MAPPING.get(_tier_key, {})
        
        # === Fill template ===
        slots = {
            'question_short': q_short,
            'category_label': category_label,
            'dung_than': dung_than,
            'hanh_dt': hanh_dt,
            # LỤC HÀO — 16 yếu tố
            'nguyet_lenh': nguyet_lenh or '?',
            'nguyet_tac_dong': nguyet_tac_dong or '?',
            'nhat_than': nhat_than or '?',
            'nhat_tac_dong': nhat_tac_dong or '?',
            'nguyen_than': nguyen_than or '?',
            'nt_state': nt_state or '?',
            'ky_than': ky_than or '?',
            'kt_state': kt_state or '?',
            'cuu_than': cuu_than or '?',
            'cuu_state': cuu_state or '?',
            'tuan_khong': tuan_khong_str or 'Không',
            'nguyet_pha': nguyet_pha_str or 'Không',
            'tham_sinh_vong_khac': tsvk_str or 'Không',
            'phan_phuc_ngam': phan_phuc_str.strip() or 'Không',
            'the_state': the_state or '?',
            'ung_state': ung_state or '?',
            'bien_hao': bien_hao_str,
            'dong_hao_list': dong_hao_list_str,
            'bien_que': bien_que_str or '?',
            'bien_hao_dt': bien_hao_dt_str or '?',
            'luc_hop_xung': luc_hop_xung_str,
            'tam_hop_cuc': tam_hop_cuc_str,
            'tien_thoai': tien_thoai_str,
            'phuc_than_info': phuc_than_str,
            'dac_biet': dac_biet_str,
            'lh_raw_score': lh_raw_score,
            'lh_pct': lh_raw,
            # KỲ MÔN — 14 yếu tố
            'cung_dt': cung_dt_str or '?',
            'cung_dt_hanh': cung_dt_hanh_str or '?',
            'sao_dt': sao_dt_str or '?',
            'cua_dt': cua_dt_str or '?',
            'than_dt': than_dt_str or '?',
            'truc_phu': truc_phu or '?',
            'truc_su': truc_su or '?',
            'khong_vong_km': khong_vong_km or '?',
            'ma_tinh': ma_tinh or '?',
            'tam_ky': tam_ky,
            'km_cuc': km_cuc or '?',
            'am_duong_don': am_duong_don or '?',
            'tu_tru': tu_tru or '?',
            'cung_bt': cung_bt_str or '?',
            'cung_sv': cung_sv_str or '?',
            'bt_sv_rel': bt_sv_rel_str or '?',
            'dia_ban_dt': dia_ban_dt_str or '?',
            'km_phan_phuc': km_phan_phuc_str,
            # MAI HOA — 10 yếu tố
            'the_quai': the_quai_str or '?',
            'the_quai_hanh': the_quai_hanh_str or '?',
            'the_vuong_suy': the_vuong_suy or '?',
            'dung_quai': dung_quai_str or '?',
            'dung_quai_hanh': dung_quai_hanh_str or '?',
            'dung_vuong_suy': dung_vuong_suy or '?',
            'ho_quai': ho_quai_str or '?',
            'bien_quai_mh': bien_quai_mh_str or '?',
            'the_dung_rel': the_dung_rel_str or '?',
            'the_dung_y_nghia': the_dung_y_nghia_str or '?',
            'ho_the_rel': ho_the_rel_str or 'N/A',
            'ho_the_y_nghia': ho_the_y_nghia_str or 'N/A',
            'ho_dung_rel': ho_dung_rel_str or 'N/A',
            'ho_dung_y_nghia': ho_dung_y_nghia_str or 'N/A',
            'dong_hao_mh': dong_hao_mh_str,
            'mh_interpretation': mh_interpretation_str or '?',
            # ĐAI LỤC NHÂM — 7 yếu tố
            'so_truyen': so_truyen,
            'trung_truyen': trung_truyen,
            'mat_truyen': mat_truyen,
            'thien_tuong': thien_tuong,
            'tu_khoa': tu_khoa,
            'can_chi_lac_cung': can_chi_lac_cung,
            # THIẾT BẢN + THÁI ẤT — 5 yếu tố
            'nap_am_ten': nap_am_ten,
            'nap_am_hanh': nap_am_hanh,
            'nap_am_giai_thich': nap_am_giai_thich or '?',
            'chu_khach': chu_khach,
            'ta_cuc': ta_cuc,
            # ĐÁNH GIÁ TỔNG HỢP
            'chi_reference': chi_ref or '?',
            'ts_stage': ts_stage or 'N/A',
            'ts_icon': ts_icon,
            'ts_power': ts_power,
            'ts_mota': ts_mota or '',
            'cung_hanh': cung_hanh or '?',
            'ngu_khi': ngu_khi or '?',
            'nk_power': nk_power,
            'unified_pct': unified_pct,
            'tier_cap': tier_cap,
            # Vạn Vật Vật Chất
            'hinh_dang': hanh_vat.get('hinh', '?'),
            'chat_lieu': hanh_vat.get('chat_lieu', '?'),
            'mau_sac': hanh_vat.get('mau', '?'),
            'huong': hanh_vat.get('huong', '?'),
            # Vạn Vật Mapping
            'kich_thuoc': vv_mapping.get('kich_thuoc', '?'),
            'tinh_trang': vv_mapping.get('tinh_trang', '?'),
            'so_luong': vv_mapping.get('so_luong', '?'),
            'chat_luong': vv_mapping.get('chat_luong', '?'),
            'con_nguoi': vv_mapping.get('con_nguoi', '?'),
            'suc_khoe': hanh_vat.get('co_the', '?'),
            # Vạn Vật Cụ Thể (Ngũ Hành × Tầng)
            'do_vat': vv_cu_the.get('do_vat', '?'),
            'nha_cua': vv_cu_the.get('nha_cua', '?'),
            'nguoi_lien_quan': vv_cu_the.get('nguoi', '?'),
            'benh_tat': vv_cu_the.get('benh', '?'),
        }
        
        # Fill template
        try:
            template = DIAGRAM_MASTER.get('template', '')
            filled = template
            for k, v in slots.items():
                filled = filled.replace('{' + k + '}', str(v))
            # Xử lý {lh_raw_score:+d} format specifier
            filled = filled.replace('{lh_raw_score:+d}', f'{lh_raw_score:+d}')
        except Exception:
            filled = f"[SĐ_MASTER Error] Không thể điền sơ đồ"
        
        # === Conclusion from formula ===
        conclusion = ''
        rules = DIAGRAM_MASTER.get('conclusion_rules', {})
        for _, (lo, hi, desc) in rules.items():
            if lo <= unified_pct <= hi:
                conclusion = desc
                break
        if not conclusion:
            conclusion = f"Unified = {unified_pct}%"
        
        formula_detail = (
            f"LH({lh_raw}%)×50% + TS({ts_power}%)×30% + NK({nk_power}%)×20% "
            f"= {unified_pct}%"
        )
        
        # V40.2: Thay thế nghiêng thuận mơ hồ bằng ngôn ngữ dứt khoát
        conclusion = conclusion.replace('Nghiêng thuận', 'CÓ THỂ ĐƯỢC')
        conclusion = conclusion.replace('nghiêng thuận', 'có thể được')
        
        return filled, {
            'conclusion': conclusion,
            'formula_detail': formula_detail,
            'unified_pct': unified_pct,
            'tier_cap': tier_cap,
            'slots': slots,
        }
    
    def _fill_question_diagram(self, diagram_id, question, dung_than, hanh_dt,
                                unified_v22, v23_lh_factors, v24_km_factors,
                                v24_mh_factors, chart_data, luc_hao_data, mai_hoa_data,
                                verdicts_dict=None):
        """V31.0: Điền yếu tố thời gian thực vào sơ đồ câu hỏi (SĐ0-SĐ16).
        
        Trả về: (filled_template, info_dict)
        """
        if not INTERACTION_DIAGRAMS or diagram_id not in INTERACTION_DIAGRAMS:
            return "", {}
        
        diagram = INTERACTION_DIAGRAMS[diagram_id]
        v22 = unified_v22 or {}
        vd = verdicts_dict or {}
        
        # === Common slots ===
        common = {
            'dung_than': dung_than,
            'hanh_dt': hanh_dt,
            'unified_pct': v22.get('unified_pct', 50),
            'tier_cap': v22.get('tier_cap', '?'),
        }
        
        # Extract common LH data
        dt_state = v22.get('tier_cap', '?')
        
        # Verdicts
        km_v = vd.get('km', '?')
        lh_v = vd.get('lh', '?')
        mh_v = vd.get('mh', '?')
        ln_v = vd.get('ln', '?')
        ta_v = vd.get('ta', '?')
        
        # Count
        _vl = [km_v, lh_v, mh_v, ln_v, ta_v]
        cat_c = sum(1 for v in _vl if v and 'CÁT' in str(v).upper())
        hung_c = sum(1 for v in _vl if v and 'HUNG' in str(v).upper())
        
        # === Diagram-specific slots ===
        slots = dict(common)
        
        # ——— SĐ0: TỔNG QUÁT ———
        if diagram_id == 'SD0':
            if cat_c >= 4: concl = 'ĐẠI CÁT'
            elif cat_c >= 3: concl = 'CÁT'
            elif hung_c >= 4: concl = 'ĐẠI HUNG'
            elif hung_c >= 3: concl = 'HUNG'
            elif cat_c > hung_c: concl = 'CÓ — THUẬN LỢI'
            elif hung_c > cat_c: concl = 'KHÔNG — BẤT LỢI'
            else: concl = 'CÓ THỂ — CẦN THẬN TRỌNG'
            
            slots.update({
                'km_verdict': km_v, 'lh_verdict': lh_v, 'mh_verdict': mh_v,
                'ln_verdict': ln_v, 'ta_verdict': ta_v,
                'cat_count': cat_c, 'hung_count': hung_c,
                'conclusion': concl,
            })
        
        # ——— SĐ1: CÓ/KHÔNG ———
        elif diagram_id == 'SD1':
            # Extract from factors
            nguyet = nhat = nt = kt = cuu = ''
            m_rel = n_rel = nt_st = kt_st = cuu_st = ''
            the_st = ung_st = tsvk = tk = npha = ''
            cung_bt = cung_sv = bt_sv = ''
            score_parts = []
            total = 0
            
            for f in (v23_lh_factors or []):
                if 'Nguyệt' in f:
                    # Extract chi/hành from "Nguyệt Lệnh(Thìn/Thổ)" or similar
                    if '(' in f:
                        nguyet = f.split('(')[1].split(')')[0]
                    if 'sinh' in f.lower():
                        m_rel = 'sinh ✅'
                    elif 'khắc' in f.lower():
                        m_rel = 'khắc ❌'
                    elif 'không tác động' in f.lower():
                        m_rel = 'bình ⚪'
                    else:
                        m_rel = 'bình' if nguyet else '?'
                elif 'Nhật' in f:
                    if '(' in f:
                        nhat = f.split('(')[1].split(')')[0]
                    if 'sinh' in f.lower():
                        n_rel = 'sinh ✅'
                    elif 'khắc' in f.lower():
                        n_rel = 'khắc ❌'
                    elif 'không tác động' in f.lower():
                        n_rel = 'bình ⚪'
                    else:
                        n_rel = 'bình' if nhat else '?'
                elif 'NT(' in f:
                    nt = f.split('(')[1].split(')')[0] if '(' in f else '?'
                    if 'Vượng' in f or '+' in f:
                        nt_st = 'Vượng ✅'
                    elif 'Suy' in f or '-' in f:
                        nt_st = 'Suy ❌'
                    else:
                        nt_st = 'Bình'
                elif 'KT(' in f:
                    kt = f.split('(')[1].split(')')[0] if '(' in f else '?'
                    if 'ẩn' in kt.lower() or 'Ẩn' in f:
                        kt_st = '(ẩn) ✅'
                    elif '-' in f:
                        kt_st = 'Vượng ⚠️'
                    else:
                        kt_st = 'Có'
                elif 'Cừu' in f:
                    cuu = f.split('(')[1].split(')')[0] if '(' in f else '?'
                    cuu_st = '⚠️ Tiếp sức KT' if '-' in f else 'Yếu ✅'
                elif 'Thế' in f and 'Ứng' in f:
                    the_st = 'Vượng' if 'khắc Ứng' in f else 'Suy'
                    ung_st = 'Suy' if 'khắc Ứng' in f else 'Vượng'
                elif 'THAM SINH' in f.upper():
                    tsvk = '⚡ CÓ → CÁT'
                elif 'Tuần Không' in f:
                    tk = 'CÓ ⭕ (chưa thành)'
                elif 'Nguyệt Phá' in f:
                    npha = 'CÓ 💥'
                
                # Extract score
                try:
                    for p in f.split():
                        if (p.startswith('+') or p.startswith('-')) and p[1:].isdigit():
                            val = int(p)
                            total += val
                            score_parts.append(p)
                            break
                except: pass
            
            # KM BT/SV + Thế/Ứng
            for f in (v24_km_factors or []):
                if 'BT' in f and 'SV' in f:
                    bt_sv = 'BT thắng SV ✅' if ('+' in f) else 'SV thắng ❌'
                    # Extract cung (số thuần, template đã có prefix 'Cung')
                    import re as _re2
                    cm = _re2.findall(r'Cung(\d+)', f)
                    if len(cm) >= 2:
                        cung_bt = cm[0]
                        cung_sv = cm[1]
                    elif len(cm) == 1:
                        cung_bt = cm[0]
                elif 'Thế' in f and ('khắc' in f.lower() or 'sinh' in f.lower()):
                    if 'khắc Ứng' in f or ('+' in f):
                        the_st = the_st or 'Vượng'
                        ung_st = ung_st or 'Suy'
                    else:
                        the_st = the_st or 'Suy'
                        ung_st = ung_st or 'Vượng'
            
            # V32.7d: Fallback — lấy Cừu, Thế/Ứng, BT/SV cung từ data gốc
            if not cuu and luc_hao_data and isinstance(luc_hao_data, dict):
                cuu = luc_hao_data.get('cuu_than', '')
                if cuu:
                    cuu_st = cuu_st or 'Có'
                else:
                    cuu = 'N/A'
                    cuu_st = 'N/A'
            
            if not the_st and luc_hao_data and isinstance(luc_hao_data, dict):
                # Try multiple keys for hào list
                hao_list = (luc_hao_data.get('hao', []) or 
                           luc_hao_data.get('haos', []) or 
                           luc_hao_data.get('hao_list', []))
                ban_lh = luc_hao_data.get('ban', {})
                if not hao_list and ban_lh:
                    hao_list = (ban_lh.get('haos', []) or 
                               ban_lh.get('details', []) or 
                               ban_lh.get('hao_list', []))
                for hao in hao_list:
                    if isinstance(hao, dict):
                        tu = str(hao.get('the_ung', '') or hao.get('marker', ''))
                        hanh_h = hao.get('hanh', '') or hao.get('ngu_hanh', '')
                        chi_h = hao.get('chi', '')
                        label = f"{chi_h}/{hanh_h}" if chi_h and hanh_h else (hanh_h or chi_h or 'N/A')
                        if 'Thế' in tu and not the_st:
                            the_st = label
                        elif 'Ứng' in tu and not ung_st:
                            ung_st = label
            
            # Fallback cung_bt/sv từ v24_km_factors text "BT(Cung2)...SV(Cung7)" 
            if not cung_bt:
                import re as _re3
                for f in (v24_km_factors or []):
                    cm2 = _re3.findall(r'Cung(\d+)', f)
                    if len(cm2) >= 2:
                        cung_bt = cm2[0]
                        cung_sv = cm2[1]
                        break
                    elif len(cm2) == 1 and 'BT' in f:
                        cung_bt = cm2[0]
            
            if not cung_bt and chart_data and isinstance(chart_data, dict):
                cung_bt = str(chart_data.get('cung_ban_than', '?')).replace('Cung', '')
                cung_sv = str(chart_data.get('cung_su_viec', '?')).replace('Cung', '')
            
            concl = 'CÓ ✅' if total > 10 else 'KHÔNG ❌' if total < -10 else ('NGHIÊNG CÓ 🟡' if total >= 0 else 'NGHIÊNG KHÔNG 🟡')
            
            slots.update({
                'nguyet_lenh': nguyet or '?', 'nhat_than': nhat or '?',
                'm_rel': m_rel or '?', 'n_rel': n_rel or '?',
                'dt_state': dt_state,
                'nguyen_than': nt or '?', 'nt_state': nt_st or '?',
                'ky_than': kt or '?', 'kt_state': kt_st or '?',
                'cuu_than': cuu or '?', 'cuu_state': cuu_st or '?',
                'tuan_khong': tk or 'Không',
                'nguyet_pha': npha or 'Không',
                'the_state': the_st or '?', 'ung_state': ung_st or '?',
                'tham_sinh_vong_khac': tsvk or 'Không có',
                'cung_bt': cung_bt or '?', 'cung_sv': cung_sv or '?',
                'bt_sv_rel': bt_sv or '?',
                'score_detail': ' '.join(score_parts[:6]) if score_parts else '?',
                'total_score': total,
                'conclusion': concl,
            })
        
        # ——— SĐ2-SĐ16: Fill based on available data ———
        else:
            # Generic fill — use dt_state and vạn vật
            hanh_vat = v22.get('hanh_vat', NGU_HANH_VAT_CHAT.get(hanh_dt, {}))
            vv_cu_the = v22.get('van_vat_cu_the', {})
            
            generic_slots = {
                'dt_state': dt_state,
                'hinh_dang': hanh_vat.get('hinh', '?'),
                'chat_lieu': hanh_vat.get('chat_lieu', '?'),
                'mau_sac': hanh_vat.get('mau', '?'),
                'huong': hanh_vat.get('huong', '?'),
                'co_the': hanh_vat.get('co_the', '?'),
                'do_vat': vv_cu_the.get('do_vat', '?'),
                'nguoi_lien_quan': vv_cu_the.get('nguoi', '?'),
                # Verdicts
                'km_verdict': km_v, 'lh_verdict': lh_v, 'mh_verdict': mh_v,
                'ln_verdict': ln_v, 'ta_verdict': ta_v,
                'cat_count': cat_c, 'hung_count': hung_c,
            }
            
            # MH data
            if mai_hoa_data and isinstance(mai_hoa_data, dict):
                # V32.5: Unified key mapping — check all possible key names
                the_q = mai_hoa_data.get('the_quai', '') or mai_hoa_data.get('ten_ha', '') or mai_hoa_data.get('lower', '') or '?'
                dung_q = mai_hoa_data.get('dung_quai', '') or mai_hoa_data.get('ten_thuong', '') or mai_hoa_data.get('upper', '') or '?'
                if isinstance(the_q, dict): the_q = the_q.get('ten', '?')
                if isinstance(dung_q, dict): dung_q = dung_q.get('ten', '?')
                generic_slots['the_quai'] = str(the_q)
                generic_slots['dung_quai'] = str(dung_q)
                generic_slots['ho_quai'] = str(mai_hoa_data.get('ho_quai', '') or mai_hoa_data.get('ten_ho', '') or '?')
                generic_slots['bien_quai'] = str(mai_hoa_data.get('bien_quai', '') or mai_hoa_data.get('ten_qua_bien', '') or '?')
                the_h = mai_hoa_data.get('hanh_ha', '') or mai_hoa_data.get('lower_element', '') or '?'
                dung_h = mai_hoa_data.get('hanh_thuong', '') or mai_hoa_data.get('upper_element', '') or '?'
                if isinstance(the_q, dict): the_h = the_q.get('hanh', the_h)
                if isinstance(dung_q, dict): dung_h = dung_q.get('hanh', dung_h)
                generic_slots['the_quai_hanh'] = the_h  
                generic_slots['dung_quai_hanh'] = dung_h
                if the_h != '?' and dung_h != '?':
                    generic_slots['the_dung_rel'] = _ngu_hanh_relation(the_h, dung_h).split('(')[0] if the_h and dung_h else '?'
                else:
                    generic_slots['the_dung_rel'] = '?'
            
            # KM data
            if chart_data and isinstance(chart_data, dict):
                generic_slots['cung_bt'] = '?'
                generic_slots['cung_sv'] = '?'
                generic_slots['cung_dt'] = '?'
                generic_slots['phuong_km'] = '?'
                
                can_ngay = chart_data.get('can_ngay', '')
                can_thien_ban = chart_data.get('can_thien_ban', {})
                nhan_ban = chart_data.get('nhan_ban', {})
                thien_ban = chart_data.get('thien_ban', {})
                
                for c_num, c_can in can_thien_ban.items():
                    if c_can == can_ngay:
                        generic_slots['cung_bt'] = str(c_num)
                    elif c_can == chart_data.get('can_gio', ''):
                        generic_slots['cung_sv'] = str(c_num)
                        generic_slots['cung_dt'] = str(c_num)
                        generic_slots['phuong_km'] = CUNG_PHUONG.get(int(c_num), '?') if c_num else '?'
                
                # V32.7e: Fallback cung_dt từ cung_bt
                if generic_slots['cung_dt'] == '?' and generic_slots['cung_bt'] != '?':
                    generic_slots['cung_dt'] = generic_slots['cung_bt']
                    generic_slots['phuong_km'] = CUNG_PHUONG.get(int(generic_slots['cung_bt']), '?')
                
                # V32.7e: Fallback cung_sv — cung đối diện BT
                if generic_slots['cung_sv'] == '?' and generic_slots['cung_bt'] != '?':
                    bt_num = int(generic_slots['cung_bt'])
                    _OPP = {1:9, 2:8, 3:7, 4:6, 6:4, 7:3, 8:2, 9:1}
                    generic_slots['cung_sv'] = str(_OPP.get(bt_num, bt_num))
                
                # Cửa at DT cung
                dt_cung = generic_slots.get('cung_dt', '')
                if dt_cung and dt_cung.isdigit():
                    cua_val = nhan_ban.get(int(dt_cung), nhan_ban.get(dt_cung, '?'))
                    generic_slots['cua_dt'] = str(cua_val)
                    cua_key = str(cua_val) if 'Môn' in str(cua_val) else str(cua_val) + ' Môn'
                    cua_info = CUA_GIAI_THICH.get(cua_key, {})
                    generic_slots['cua_y_nghia'] = cua_info.get('y_nghia', '?')
                    
                    sao_val = thien_ban.get(int(dt_cung), thien_ban.get(dt_cung, '?'))
                    generic_slots['sao_dt'] = str(sao_val)
                else:
                    generic_slots['cua_dt'] = '?'
                    generic_slots['sao_dt'] = '?'
                    generic_slots['cua_y_nghia'] = '?'
                
                # V32.7e: Fallback cua_dt từ v24_km_factors
                if generic_slots['cua_dt'] == '?':
                    for f in (v24_km_factors or []):
                        if 'Cửa' in f:
                            parts = f.split('Cửa')[-1].strip().split(' ')
                            cua_name = ' '.join(parts[:2]).strip()
                            if cua_name:
                                generic_slots['cua_dt'] = cua_name
                                cua_key2 = cua_name if 'Môn' in cua_name else cua_name + ' Môn'
                                cua_info2 = CUA_GIAI_THICH.get(cua_key2, {})
                                generic_slots['cua_y_nghia'] = cua_info2.get('y_nghia', cua_name)
                            break
                
                generic_slots['bt_sv_rel'] = '?'
                for f in (v24_km_factors or []):
                    if 'BT' in f and ('sinh' in f or 'khắc' in f):
                        generic_slots['bt_sv_rel'] = f.split('(')[0].strip() if '(' in f else f[:30]
            
            # Auto-conclusion based on cat/hung (V34.3: QUYẾT ĐOÁN)
            if cat_c >= 3:
                generic_slots['conclusion'] = 'THUẬN LỢI ✅'
            elif hung_c >= 3:
                generic_slots['conclusion'] = 'BẤT LỢI ❌'
            elif cat_c > hung_c:
                generic_slots['conclusion'] = f'CÓ — THUẬN LỢI ✅ ({cat_c} cát vs {hung_c} hung)'
            elif hung_c > cat_c:
                generic_slots['conclusion'] = f'KHÔNG — BẤT LỢI ⚠️ ({hung_c} hung vs {cat_c} cát)'
            else:
                generic_slots['conclusion'] = f'CÓ THỂ — CẦN THẬN TRỌNG ({cat_c} cát = {hung_c} hung)'
            
            # V32.6: Fill SĐ2 (TUỔI/SỐ) slots — dùng TRƯỜNG SINH stage
            if _is_age_question(question) or _is_count_question(question):
                # Xác định Bát Quái từ DT  
                bt_quai_name = '?'
                bt_quai_so = 0
                tt_so = 0
                
                # Từ Mai Hoa: Thể quái
                if mai_hoa_data and isinstance(mai_hoa_data, dict):
                    the_q = mai_hoa_data.get('ten_ha', '') or mai_hoa_data.get('the_quai', '') or mai_hoa_data.get('lower', '')
                    if isinstance(the_q, dict): the_q = the_q.get('ten', '')
                    if the_q and the_q in TIEN_THIEN:
                        bt_quai_name = the_q
                        bt_quai_so = TIEN_THIEN[the_q]
                        tt_so = bt_quai_so
                
                # Từ KM: Quái cung BT
                if bt_quai_so == 0 and chart_data and isinstance(chart_data, dict):
                    CUNG_QUAI_MAP = {1: 'Khảm', 2: 'Khôn', 3: 'Chấn', 4: 'Tốn', 6: 'Càn', 7: 'Đoài', 8: 'Cấn', 9: 'Ly'}
                    bt_cung = generic_slots.get('cung_bt', '')
                    if bt_cung and bt_cung.isdigit():
                        bt_quai_name = CUNG_QUAI_MAP.get(int(bt_cung), '?')
                        bt_quai_so = TIEN_THIEN.get(bt_quai_name, 0)
                        tt_so = bt_quai_so
                
                # V32.6 CORE: Tuổi từ TRƯỜNG SINH stage (lấy trực tiếp từ v22)
                # V34.0 FIX: ts_stage không tồn tại trong scope này → lấy từ v22
                ts_stage_direct = v22.get('ts_stage', 'N/A')
                ts_data_direct = TRUONG_SINH_POWER.get(ts_stage_direct, {})
                ts_tuoi_min = ts_data_direct.get('tuoi_min', 0)
                ts_tuoi_max = ts_data_direct.get('tuoi_max', 0)
                ts_stage_name = ts_stage_direct
                
                # Nếu Thai/Dưỡng (chưa sinh) → fallback Ngũ Khí
                if ts_tuoi_max <= 2 and ngu_khi:
                    NGU_KHI_TUOI = {
                        'Vượng': (33, 45), 'Tướng': (19, 32),
                        'Hưu': (46, 55), 'Tù': (56, 65), 'Tử': (66, 75),
                    }
                    nk_range = NGU_KHI_TUOI.get(ngu_khi, (19, 55))
                    ts_tuoi_min, ts_tuoi_max = nk_range
                    ts_stage_name = f"{ts_stage_direct}→{ngu_khi}"
                
                tuoi_estimate = (ts_tuoi_min + ts_tuoi_max) // 2 if ts_tuoi_max > 0 else 0
                tuoi_range = f"{ts_tuoi_min}-{ts_tuoi_max}" if ts_tuoi_max > 0 else '?'
                
                generic_slots['bat_quai_dt'] = bt_quai_name
                generic_slots['bat_quai_so'] = str(bt_quai_so) if bt_quai_so else '?'
                generic_slots['tien_thien_so'] = str(tt_so) if tt_so else '?'
                generic_slots['tuoi_tra_san'] = tuoi_range
                generic_slots['tuoi_trung_binh'] = str(tuoi_estimate) if tuoi_estimate else tuoi_range
                generic_slots.setdefault('vv_con_nguoi', vv_cu_the.get('nguoi', hanh_vat.get('co_the', '?')) if vv_cu_the else '?')
            
            # V32.7e: Fill ALL SD-specific slots
            # --- Lục Thân states ---
            _lts = {}
            if luc_hao_data and isinstance(luc_hao_data, dict):
                _hl = (luc_hao_data.get('haos', []) or luc_hao_data.get('hao_list', []) or luc_hao_data.get('hao', []))
                _ban = luc_hao_data.get('ban', {})
                if not _hl and _ban:
                    _hl = _ban.get('haos', []) or _ban.get('details', [])
                for _h in _hl:
                    if isinstance(_h, dict):
                        _lt = _h.get('luc_than', '')
                        _chi = _h.get('chi', '')
                        _hh = _h.get('hanh', '') or _h.get('ngu_hanh', '')
                        _dong = '🔄Động' if (_h.get('dong') or _h.get('is_moving')) else 'Tĩnh'
                        _tu = str(_h.get('the_ung', '') or _h.get('marker', ''))
                        if _lt and _lt not in _lts:
                            _lts[_lt] = f"{_chi}/{_hh} {_dong}"
                        if 'Thế' in _tu:
                            generic_slots.setdefault('the_state', f"{_chi}/{_hh}")
                        elif 'Ứng' in _tu:
                            generic_slots.setdefault('ung_state', f"{_chi}/{_hh}")
            
            generic_slots.setdefault('the_tai_state', _lts.get('Thê Tài', 'N/A'))
            generic_slots.setdefault('huynh_de_state', _lts.get('Huynh Đệ', 'N/A'))
            generic_slots.setdefault('tu_ton_state', _lts.get('Tử Tôn', 'N/A'))
            generic_slots.setdefault('quan_quy_state', _lts.get('Quan Quỷ', 'N/A'))
            generic_slots.setdefault('phu_mau_state', _lts.get('Phụ Mẫu', 'N/A'))
            
            # --- SD10 Thế↔Ứng ---
            _ts = generic_slots.get('the_state', '?')
            _us = generic_slots.get('ung_state', '?')
            _th10 = _ts.split('/')[-1] if '/' in str(_ts) else ''
            _uh10 = _us.split('/')[-1] if '/' in str(_us) else ''
            generic_slots.setdefault('the_ung_relation', _ngu_hanh_relation(_th10, _uh10) if _th10 and _uh10 else 'N/A')
            
            # --- SD11 Tìm đồ ---
            _cdt = generic_slots.get('cua_dt', '?')
            _ccat = ['Khai Môn', 'Hưu Môn', 'Sinh Môn']
            _chung = ['Tử Môn', 'Kinh Môn', 'Thương Môn']
            if any(c in str(_cdt) for c in _ccat):
                generic_slots.setdefault('tim_duoc', 'TÌM ĐƯỢC ✅')
            elif any(c in str(_cdt) for c in _chung):
                generic_slots.setdefault('tim_duoc', 'KHÓ TÌM ❌')
            else:
                generic_slots.setdefault('tim_duoc', 'CÒN CƠ HỘI 🟡')
            generic_slots.setdefault('phuong', generic_slots.get('phuong_km', '?'))
            _QTUONG = {'Càn':'Kim loại, tròn','Khôn':'Đất, vải, vuông','Chấn':'Gỗ, dài','Tốn':'Gỗ, dây, hoa','Khảm':'Nước, chất lỏng','Ly':'Lửa, điện tử','Cấn':'Đá, đất, nhỏ','Đoài':'Kim loại, hỏng'}
            _tqn = generic_slots.get('the_quai', '')
            generic_slots.setdefault('tuong_vat', _QTUONG.get(_tqn, hanh_vat.get('chat_lieu', '?')))
            generic_slots.setdefault('dt_tk', 'Không')
            generic_slots.setdefault('tk_y_nghia', 'Bình thường')
            generic_slots.setdefault('mat_truyen', 'N/A')
            generic_slots.setdefault('phuong_ln', 'N/A')
            
            # --- V34.0: SD5 KHI NÀO — Fill Tam Truyền + Ứng Kỳ ---
            if diagram_id == 'SD5':
                # DLN Tam Truyền
                try:
                    from dai_luc_nham import tinh_dai_luc_nham
                    _dln = tinh_dai_luc_nham(chart_data) if chart_data else {}
                    if isinstance(_dln, dict):
                        generic_slots['so_truyen'] = _dln.get('so_truyen', 'N/A')
                        generic_slots['trung_truyen'] = _dln.get('trung_truyen', 'N/A')
                except:
                    pass
                generic_slots.setdefault('so_truyen', 'N/A')
                generic_slots.setdefault('trung_truyen', 'N/A')
                
                # Ứng Kỳ — dựa trên DT vượng/suy
                _uk = 'Tùy DT vượng/suy'
                _uk_detail = f'DT({dung_than}) hành {hanh_dt}'
                _uk_concl = ''
                _tier = v22.get('tier_cap', '?')
                if 'VƯỢNG' in str(_tier).upper() or 'CỰC' in str(_tier).upper():
                    _uk = 'Nhanh — Chi sinh/hợp DT'
                    _uk_detail = 'DT Vượng → sự việc xảy ra NHANH'
                    _uk_concl = f'Ứng vào ngày/tháng có Chi sinh/hợp {hanh_dt}'
                elif 'SUY' in str(_tier).upper() or 'YẾU' in str(_tier).upper():
                    _uk = 'Chậm — Chi xung/khắc DT'
                    _uk_detail = 'DT Suy → sự việc xảy ra CHẬM, cần đợi'
                    _uk_concl = f'Ứng vào ngày/tháng có Chi sinh phù {hanh_dt}'
                else:
                    _uk_concl = f'Trung bình — cần xem thêm yếu tố phụ'
                generic_slots.setdefault('ung_ky', _uk)
                generic_slots.setdefault('ung_ky_detail', _uk_detail)
                generic_slots.setdefault('ung_ky_ket_luan', _uk_concl)
                generic_slots.setdefault('dt_state', dt_state)
            
            # --- SD4 Ở đâu ---
            _QT4 = {'Càn':'Trời, tròn, xa','Khôn':'Đất, vuông, gần','Chấn':'Sấm, dài, xa','Tốn':'Gió, dài, xa','Khảm':'Nước, sâu','Ly':'Lửa, sáng','Cấn':'Núi, nhỏ, gần','Đoài':'Đầm, thấp, gần'}
            generic_slots.setdefault('bat_quai_tuong', _QT4.get(_tqn, hanh_vat.get('hinh', '?')))
            _HKC = {'Kim':'Gần, trong nhà','Mộc':'Trung bình','Thủy':'Xa, bên nước','Hỏa':'Gần, nơi sáng','Thổ':'Rất gần, tại chỗ'}
            generic_slots.setdefault('khoang_cach', _HKC.get(hanh_dt, '?'))
            
            # --- SD12 Xuất hành ---
            if any(c in str(_cdt) for c in _ccat):
                generic_slots.setdefault('cua_xuat_hanh', 'NÊN ĐI ✅')
            elif any(c in str(_cdt) for c in _chung):
                generic_slots.setdefault('cua_xuat_hanh', 'KHÔNG NÊN ❌')
            else:
                generic_slots.setdefault('cua_xuat_hanh', 'CÂN NHẮC 🟡')
            generic_slots.setdefault('dich_ma', 'N/A')
            generic_slots.setdefault('kv_cung_dich', generic_slots.get('phuong_km', '?'))
            generic_slots.setdefault('dt_dich_ma', 'N/A')
            
            # --- SD13 AI ---
            _QNGUOI = {'Càn':'Bố/ông','Khôn':'Mẹ/bà','Chấn':'Thanh niên','Tốn':'Phụ nữ','Khảm':'Trí tuệ','Ly':'Nổi tiếng','Cấn':'Trẻ nhỏ','Đoài':'Con gái'}
            generic_slots.setdefault('the_quai_nguoi', _QNGUOI.get(_tqn, '?'))
            _TNGUOI = {'Quan Quỷ':'Sếp, người có quyền','Thê Tài':'Vợ/bạn gái','Huynh Đệ':'Bạn bè, đối thủ','Phụ Mẫu':'Bố mẹ, thầy cô','Tử Tôn':'Con cái'}
            generic_slots.setdefault('luc_than_dt', dung_than)
            generic_slots.setdefault('luc_than_nguoi', _TNGUOI.get(dung_than, '?'))
            generic_slots.setdefault('thien_tuong', 'N/A')
            generic_slots.setdefault('tt_nguoi', 'N/A')
            
            # --- SD14 Tại sao ---
            _kth = {v: k for k, v in KHAC.items()}.get(hanh_dt, '')
            generic_slots.setdefault('kt_hanh', _kth or '?')
            _KTNN = {'Kim':'Pháp luật/tranh chấp','Mộc':'Stress/gan','Thủy':'Cảm xúc/thận','Hỏa':'Tim/mắt','Thổ':'Chậm trễ/ì trệ'}
            generic_slots.setdefault('ky_than', f"{_kth} ({KY_THAN_NGUYEN_NHAN.get(dung_than, '?')})" if _kth else '?')
            generic_slots.setdefault('kt_nguyen_nhan', _KTNN.get(_kth, '?'))
            _dl = [h.get('luc_than','?') for h in (_hl if '_hl' in dir() else []) if isinstance(h, dict) and (h.get('dong') or h.get('is_moving'))]
            generic_slots.setdefault('hao_dong', ', '.join(_dl) if _dl else 'Không có hào động')
            generic_slots.setdefault('cua_hung', str(_cdt) if any(c in str(_cdt) for c in _chung) else 'Không')
            generic_slots.setdefault('cua_tro_ngai', 'Trở ngại' if generic_slots.get('cua_hung','') != 'Không' else 'Không có')
            generic_slots.setdefault('than_hung', 'N/A')
            generic_slots.setdefault('than_nguon_goc', 'N/A')
            
            # --- SD15 Thế nào ---
            generic_slots.setdefault('nguyet_xu_huong', 'N/A')
            generic_slots.setdefault('hao_dong_tinh', ', '.join(_dl) if _dl else 'Tĩnh (ổn định)')
            generic_slots.setdefault('cach_giai', generic_slots.get('cua_y_nghia', '?'))
            
            # --- SD16 Chọn lựa ---
            _tdr = generic_slots.get('the_dung_rel', '?')
            if 'sinh' in str(_tdr).lower():
                generic_slots.setdefault('dung_sinh_the', 'SINH ✅')
                generic_slots.setdefault('dung_ket_luan', 'Lựa chọn A HỖ TRỢ')
            elif 'khắc' in str(_tdr).lower():
                generic_slots.setdefault('dung_sinh_the', 'KHẮC ❌')
                generic_slots.setdefault('dung_ket_luan', 'Lựa chọn A BẤT LỢI')
            else:
                generic_slots.setdefault('dung_sinh_the', str(_tdr))
                generic_slots.setdefault('dung_ket_luan', 'Trung lập')
            generic_slots.setdefault('bien_sinh_the', 'N/A')
            generic_slots.setdefault('bien_ket_luan', 'Cần xem biến quái')
            generic_slots.setdefault('cung_a_diem', generic_slots.get('cung_bt', '?'))
            generic_slots.setdefault('cung_b_diem', generic_slots.get('cung_sv', '?'))
            
            # --- SD6/7/8/9 ---
            generic_slots.setdefault('score_detail', 'Auto từ 5PP')
            generic_slots.setdefault('total_score', 0)
            generic_slots.setdefault('sinh_mon', 'N/A')
            generic_slots.setdefault('dt_duyen', dung_than)
            generic_slots.setdefault('dt_duyen_state', dt_state)
            generic_slots.setdefault('dt_ung_relation', generic_slots.get('the_ung_relation', '?'))
            generic_slots.setdefault('nt_relation', 'N/A')
            generic_slots.setdefault('kt_relation', 'N/A')
            generic_slots.setdefault('the_dung_y_nghia', _tdr)
            _qqh = {v: k for k, v in SINH.items()}.get(hanh_dt, '')
            _HB = {'Kim':'Phổi, da','Mộc':'Gan, mật','Thủy':'Thận, xương','Hỏa':'Tim, mắt','Thổ':'Dạ dày, lá lách'}
            generic_slots.setdefault('qq_hanh', _qqh or '?')
            generic_slots.setdefault('qq_benh', _HB.get(_qqh, '?'))
            generic_slots.setdefault('qq_tk', 'Không')
            generic_slots.setdefault('thien_tam', 'N/A')
            generic_slots.setdefault('dt_tri_the', 'Có' if dung_than == 'Quan Quỷ' else 'Không')
            generic_slots.setdefault('khai_mon', 'N/A')
            generic_slots.setdefault('chu_khach', 'N/A')
            
            # V32.7d: Generic slots chỉ điền key chưa có
            for k, v in generic_slots.items():
                if k not in slots or slots[k] in ('', '?', None):
                    slots[k] = v
        
        # === Fill template ===
        try:
            template = diagram.get('template', '')
            filled = template
            for k, v in slots.items():
                filled = filled.replace('{' + k + '}', str(v))
            # Handle format specifiers
            filled = filled.replace('{total_score:+d}', f'{slots.get("total_score", 0):+d}')
        except Exception as e:
            filled = f"[{diagram_id} Error] {str(e)[:50]}"
        
        formula = diagram.get('formula', '')
        
        return filled, {
            'diagram_name': diagram.get('name', diagram_id),
            'formula': formula,
            'conclusion': slots.get('conclusion', '?'),
            'pp_goc': diagram.get('pp_goc', []),
        }

    # ═══════════════════════════════════════════════════════════════
    # V32.5: SƠ ĐỒ TƯƠNG TÁC 77 YẾU TỐ — CHI TIẾT TÁC ĐỘNG
    # ═══════════════════════════════════════════════════════════════
    def _build_factor_interaction_map(self, chart_data, luc_hao_data, mai_hoa_data,
                                       dung_than, hanh_dt, question='',
                                       km_verdict='', lh_verdict='', mh_verdict='',
                                       ln_verdict='', ta_verdict=''):
        """V32.5: Sinh sơ đồ tương tác chi tiết — hiện TẤT CẢ yếu tố + tác động lẫn nhau."""
        lines = []
        cd = chart_data if isinstance(chart_data, dict) else {}
        
        # ━━━━━━━ KỲ MÔN ĐỘN GIÁP (41 yếu tố) ━━━━━━━
        thien_ban = cd.get('thien_ban', {})
        nhan_ban = cd.get('nhan_ban', {})
        than_ban = cd.get('than_ban', {})
        can_tb = cd.get('can_thien_ban', {})
        dia_ban = cd.get('dia_ban', {})
        can_ngay = cd.get('can_ngay', '?')
        can_gio = cd.get('can_gio', '?')
        
        # Tìm cung BT và SV
        chu_cung = sv_cung = None
        for cn, cv in can_tb.items():
            if cv == can_ngay: chu_cung = int(cn) if cn else None
            if cv == can_gio: sv_cung = int(cn) if cn else None
        if not chu_cung and can_ngay == 'Giáp':
            for cn, cv in can_tb.items():
                if cv == 'Mậu': chu_cung = int(cn) if cn else None; break
        
        lines.append("### 🔮 SƠ ĐỒ TƯƠNG TÁC 6 PHƯƠNG PHÁP")
        lines.append("")
        
        # ── KỲ MÔN 9 CUNG ──
        if thien_ban:
            lines.append("#### ⚔️ KỲ MÔN ĐỘN GIÁP — 9 Cung")
            lines.append(f"Can Ngày=**{can_ngay}** (BT) | Can Giờ=**{can_gio}** (SV) | "
                        f"Tiết Khí={cd.get('tiet_khi','?')} | Cục={cd.get('cuc','?')}")
            lines.append("")
            lines.append("| Cung | Sao | Cửa | Thần | Can Thiên | Can Địa | Vai trò |")
            lines.append("|:----:|:----|:----|:-----|:---------|:--------|:--------|")
            for i in range(1, 10):
                if i == 5:
                    # Cung 5 = Trung Cung → QMDG không xếp Sao/Cửa/Thần
                    ct5 = can_tb.get(5, can_tb.get('5', '—'))
                    cd5 = dia_ban.get(5, dia_ban.get('5', '—')) if dia_ban else '—'
                    lines.append(f"| 5 | *(Trung Cung)* | — | — | {ct5} | {cd5} |  |")
                    continue
                sao = thien_ban.get(i, thien_ban.get(str(i), '?'))
                cua = nhan_ban.get(i, nhan_ban.get(str(i), '?'))
                than = than_ban.get(i, than_ban.get(str(i), '?'))
                ct = can_tb.get(i, can_tb.get(str(i), '?'))
                cd_val = dia_ban.get(i, dia_ban.get(str(i), '?')) if dia_ban else '?'
                role = ""
                if i == chu_cung: role = "⭐ **BẢN THÂN**"
                elif i == sv_cung: role = "🎯 **SỰ VIỆC**"
                lines.append(f"| {i} | {sao} | {cua} | {than} | {ct} | {cd_val} | {role} |")
            
            # Tác động BT
            if chu_cung:
                bt_sao = thien_ban.get(chu_cung, thien_ban.get(str(chu_cung), '?'))
                bt_cua = nhan_ban.get(chu_cung, nhan_ban.get(str(chu_cung), '?'))
                bt_than = than_ban.get(chu_cung, than_ban.get(str(chu_cung), '?'))
                hanh_cung = CUNG_NGU_HANH.get(chu_cung, '?')
                hanh_can = CAN_NGU_HANH.get(can_ngay, '?')
                rel = _ngu_hanh_relation(hanh_can, hanh_cung)
                
                lines.append("")
                lines.append("**📊 Chuỗi tác động BẢN THÂN:**")
                lines.append(f"```")
                lines.append(f"Can {can_ngay}({hanh_can}) ──→ Cung {chu_cung}({hanh_cung}) = {rel}")
                lines.append(f"  ├── Sao: {bt_sao} → {'CÁT ✅' if any(s in str(bt_sao) for s in ['Tâm','Nhậm','Phụ','Xung']) else 'HUNG/BÌNH ⚠️'}")
                lines.append(f"  ├── Cửa: {bt_cua} → {'CÁT ✅' if any(c in str(bt_cua) for c in ['Khai','Hưu','Sinh']) else 'HUNG ❌' if any(c in str(bt_cua) for c in ['Tử','Kinh','Thương']) else 'BÌNH 🟡'}")
                lines.append(f"  └── Thần: {bt_than}")
                
                if sv_cung and sv_cung != chu_cung:
                    sv_hanh = CUNG_NGU_HANH.get(sv_cung, '?')
                    bt_sv_rel = _ngu_hanh_relation(hanh_cung, sv_hanh)
                    lines.append(f"  BT(Cung{chu_cung}) ──{bt_sv_rel}──→ SV(Cung{sv_cung})")
                lines.append(f"```")
            
            # Đặc biệt
            specials = []
            can_thien = can_tb.get(str(chu_cung), can_tb.get(chu_cung, '')) if chu_cung else ''
            can_dia_bt = dia_ban.get(chu_cung, '') if dia_ban and chu_cung else ''
            if can_thien and can_dia_bt:
                pp = _check_phan_phuc_ngam(can_thien, can_dia_bt) if can_thien and can_dia_bt else None
                if pp: specials.append(f"⚠️ {pp}")
            if can_thien in ['Ất', 'Bính', 'Đinh']:
                specials.append(f"✨ Tam Kỳ ({can_thien})")
            if specials:
                lines.append(f"**⚡ Đặc biệt:** {' | '.join(specials)}")
            
            lines.append(f"**→ KỲ MÔN: {km_verdict}**")
            lines.append("")
        
        # ── LỤC HÀO ──
        lh = luc_hao_data if isinstance(luc_hao_data, dict) else {}
        if lh:
            lines.append("#### 📜 LỤC HÀO KINH DỊCH — 6 Hào")
            ban_lh = lh.get('ban', {})
            haos = lh.get('haos', lh.get('hao_list', [])) or ban_lh.get('haos', ban_lh.get('details', []))
            nguyet = lh.get('nguyet_lenh', lh.get('chi_thang', ''))
            nhat = lh.get('nhat_than', lh.get('can_ngay', ''))
            
            # V32.5: Fallback Nguyệt/Nhật từ calculate_qmdg_params
            if not nguyet or nguyet == '?':
                try:
                    import datetime as _dt_im
                    from qmdg_calc import calculate_qmdg_params as _calc_im
                    _pi = _calc_im(_dt_im.datetime.now())
                    nguyet = _pi.get('chi_thang', '?')
                    if not nhat: nhat = _pi.get('can_ngay', '?')
                except:
                    nguyet = nguyet or '?'
            nhat = nhat or '?'
            
            if haos and isinstance(haos, list):
                lines.append(f"Nguyệt Lệnh=**{nguyet}** | Nhật Thần=**{nhat}**")
                lines.append("")
                lines.append("| Hào | Lục Thân | Chi | Hành | Động | Vai trò |")
                lines.append("|:---:|:---------|:----|:-----|:----:|:--------|")
                for idx, hao in enumerate(haos):
                    if isinstance(hao, dict):
                        pos = ['Sơ', 'Nhị', 'Tam', 'Tứ', 'Ngũ', 'Thượng'][idx] if idx < 6 else str(idx+1)
                        lt = hao.get('luc_than', '?')
                        chi = hao.get('chi', '') or (hao.get('can_chi','').split('-')[0] if hao.get('can_chi') else '?')
                        hanh = hao.get('hanh', '') or hao.get('ngu_hanh', '?')
                        dong = '🔄' if (hao.get('dong') or hao.get('is_moving')) else '—'
                        role = ''
                        tu = hao.get('the_ung', '') or hao.get('marker', '')
                        if lt == dung_than:
                            role = '⭐ DT'
                        elif dung_than == 'Bản Thân' and 'Thế' in str(tu):
                            role = '⭐ DT'
                        if 'Thế' in str(tu): role += ' 👤Thế'
                        if 'Ứng' in str(tu): role += ' 🎯Ứng'
                        lines.append(f"| {pos} | {lt} | {chi} | {hanh} | {dong} | {role} |")
            
            lines.append("")
            lines.append("**📊 Chuỗi tác động LỤC HÀO:**")
            lines.append(f"```")
            lines.append(f"Nguyệt({nguyet}) ──sinh/khắc──→ Dụng Thần({dung_than})")
            lines.append(f"Nhật({nhat})   ──sinh/khắc──→ Dụng Thần({dung_than})")
            lines.append(f"Nguyên Thần ──SINH──→ DT (giúp đỡ)")
            lines.append(f"Kỵ Thần    ──KHẮC──→ DT (phá hoại)")
            lines.append(f"Cừu Thần   ──KHẮC──→ Kỵ Thần (giải cứu)")
            lines.append(f"```")
            lines.append(f"**→ LỤC HÀO: {lh_verdict}**")
            lines.append("")
        
        # ── MAI HOA ──
        mh = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
        if mh:
            lines.append("#### 🌸 MAI HOA DỊCH SỐ")
            thuong = mh.get('ten_thuong', mh.get('thuong_quai', mh.get('upper', '?')))
            ha = mh.get('ten_ha', mh.get('ha_quai', mh.get('lower', '?')))
            bien = mh.get('ten_qua_bien', mh.get('bien_quai', '?'))
            ho = mh.get('ten_ho', mh.get('ho_quai', '?'))
            ten = mh.get('ten', mh.get('ten_que', '?'))
            hao_dong = mh.get('dong_hao', mh.get('hao_dong', '?'))
            tuong = mh.get('tuong', '')
            hanh_thuong = mh.get('hanh_thuong', mh.get('upper_element', '?'))
            hanh_ha = mh.get('hanh_ha', mh.get('lower_element', '?'))
            
            lines.append(f"Quẻ: **{ten}** | Hào Động: {hao_dong} | Tượng: {tuong}")
            lines.append(f"```")
            lines.append(f"Thượng Quái: {thuong} ({hanh_thuong}) = Ngoại/Môi trường")
            lines.append(f"  │")
            lines.append(f"Hạ Quái:    {ha} ({hanh_ha}) = Nội/Bản thân")
            lines.append(f"  │")
            lines.append(f"  ├── Biến Quái: {bien} (Tương lai)")
            lines.append(f"  └── Hỗ Quái:  {ho} (Ẩn bên trong)")
            lines.append(f"")
            lines.append(f"Thể({hanh_ha}) ←sinh/khắc→ Dụng({hanh_thuong}) = KẾT QUẢ")
            lines.append(f"```")
            
            interp = mh.get('interpretation', '')
            if interp:
                lines.append(f"📖 *{str(interp)[:150]}*")
            lines.append(f"**→ MAI HOA: {mh_verdict}**")
            lines.append("")
        
        # ── ĐẠI LỤC NHÂM ──
        if cd.get('can_ngay'):
            lines.append("#### 🔯 ĐẠI LỤC NHÂM")
            lines.append(f"```")
            lines.append(f"[Sơ Truyền]  →  [Trung Truyền]  →  [Mạt Truyền]")
            lines.append(f" (Nguyên nhân)    (Diễn biến)       (Kết quả)")
            lines.append(f"```")
            lines.append(f"**→ ĐẠI LỤC NHÂM: {ln_verdict}**")
            lines.append("")
        
        # ── THÁI ẤT ──
        lines.append("#### ⭐ THÁI ẤT THẦN SỐ")
        lines.append(f"```")
        lines.append(f"Thái Ất Cung → Bát Tướng → Cách Cục → Verdict")
        lines.append(f"```")
        lines.append(f"**→ THÁI ẤT: {ta_verdict}**")
        lines.append("")
        
        # ── TỔNG HỢP 6PP ──
        lines.append("#### 🏆 TỔNG HỢP 6 PHƯƠNG PHÁP")
        lines.append(f"```")
        lines.append(f"┌─────────┬─────────┬─────────┐")
        lines.append(f"│ KỲ MÔN  │ LỤC HÀO │ MAI HOA │")
        lines.append(f"│ {km_verdict:^7s} │ {lh_verdict:^7s} │ {mh_verdict:^7s} │")
        lines.append(f"├─────────┼─────────┼─────────┤")
        lines.append(f"│ THIẾT   │ LỤC     │ THÁI    │")
        lines.append(f"│ BẢN     │ NHÂM    │ ẤT      │")
        lines.append(f"│  BÌNH   │ {ln_verdict:^7s} │ {ta_verdict:^7s} │")
        lines.append(f"└─────────┴─────────┴─────────┘")
        lines.append(f"         ↓ TỔNG HỢP ↓")
        verdicts = [km_verdict, lh_verdict, mh_verdict, ln_verdict, ta_verdict]
        cat = sum(1 for v in verdicts if 'CÁT' in str(v).upper())
        hung = sum(1 for v in verdicts if 'HUNG' in str(v).upper())
        lines.append(f"    CÁT: {cat}/5 | HUNG: {hung}/5")
        lines.append(f"```")
        
        return "\n".join(lines)

    # V27.0: ENHANCED DETECTIVE - Tich hop qmdg_advanced_rules + qmdg_inference_rules
    def _enhanced_detective(self, chart_data, question, hanh_dt=None):
        """V27.0: Bo sung chi tiet cho V18 Detective tu 2 module moi.
        Tra ve string bo sung them cho detective analysis."""
        extras = []
        if not hanh_dt:
            return ""
        
        q_lower = question.lower() if question else ""
        is_tim_do = any(kw in q_lower for kw in ['tim', 'mat', 'trom', 'lay', 'danh roi', 'de quen',
                                                   'tìm', 'mất', 'trộm', 'lấy', 'đánh rơi', 'để quên'])
        
        # 1) Mau sac vat mat (tu qmdg_inference_rules)
        if is_tim_do and MAU_SAC_VAT_MAT:
            mau_data = MAU_SAC_VAT_MAT.get(hanh_dt, {})
            if mau_data:
                extras.append(f"[V27-MAU SAC] Hanh {hanh_dt}: {mau_data.get('Chinh','')} | Phu: {', '.join(mau_data.get('Phu',['?']))}")
        
        # 2) Nguoi quen hay nguoi la (tu qmdg_advanced_rules)
        if is_tim_do and QUEN_LA_QUY_TAC:
            # Xac dinh dua tren Luc Than cua Dung Than
            for lt_key, lt_data in QUEN_LA_QUY_TAC.items():
                if isinstance(lt_data, dict) and lt_data.get('Quan_He'):
                    extras.append(f"[V27-NGUOI] {lt_key}: {lt_data['Quan_He'][:60]}")
                    break  # Chi lay 1 mau dau tien lam vi du
        
        # 3) Khoang cach (tu qmdg_advanced_rules)
        if is_tim_do and KHOANG_CACH_CHI_TIET:
            kc_data = KHOANG_CACH_CHI_TIET.get(hanh_dt, {})
            if kc_data:
                extras.append(f"[V27-KC] {kc_data}")
        
        # 4) Kha nang lay lai
        if is_tim_do and KHA_NANG_LAY_LAI:
            kn_data = KHA_NANG_LAY_LAI.get(hanh_dt, '')
            if kn_data:
                extras.append(f"[V27-KHA NANG] {kn_data}")
        
        # 5) Dac diem ke lay (tu qmdg_inference_rules)
        if is_tim_do and DAC_DIEM_KE_LAY:
            for hanh_key, dd_data in DAC_DIEM_KE_LAY.items():
                if hanh_key == hanh_dt:
                    extras.append(f"[V27-KE LAY] Hanh {hanh_key}: {dd_data}")
                    break
        
        if extras:
            return "\n--- V27 DETECTIVE NANG CAO ---\n" + "\n".join(extras) + "\n"
        return ""

    # V27.0: VERDICT COMPACT BLOCK - Tom tat co cau truc de Gemini luon doc duoc
    def _build_verdict_compact_block(self, od):
        """V27.0: Tao block tom tat compact ~1200 ky tu chua TAT CA du lieu quan trong.
        Block nay luon nam DAU prompt -> Gemini doc duoc 100% du full report bi cat."""
        lines = []
        lines.append("\n=== [V27 VERDICT COMPACT] DU LIEU THEN CHOT ===")
        
        # 1) Verdict 6 phuong phap
        lines.append(f"DT={od.get('dung_than','?')} | Cat={od.get('category_label','?')}")
        lines.append(f"KM={od.get('ky_mon_verdict','?')} LH={od.get('luc_hao_verdict','?')} MH={od.get('mai_hoa_verdict','?')} LN={od.get('luc_nham_verdict','?')} TA={od.get('thai_at_verdict','?')}")
        
        # 2) V22 Lực Lượng Tổng Hợp (V28: BỎ % — chỉ giữ trạng thái định tính)
        v22 = od.get('v22_unified_strength', {})
        if v22:
            lines.append(f"Tier={v22.get('tier_cap','?')} NguKhi={v22.get('ngu_khi','?')} HanhDT={v22.get('hanh_dt','?')} 12TS={v22.get('ts_stage','?')}")
            vv = v22.get('van_vat_cu_the', {})
            if vv:
                lines.append(f"VanVat: DoVat={vv.get('do_vat','')} Nguoi={vv.get('nguoi','')} Benh={vv.get('benh','')}")
        
        # 3) V15 Xau Duoc compact
        if od.get('v15_bt_score') or od.get('v15_dt_score'):
            lines.append(f"V15: BT={od.get('v15_bt_score','?')} DT={od.get('v15_dt_score','?')} Time={od.get('v15_timeline','?')} UngKy={od.get('v15_timing','?')}")
        
        # 4) V16 Scoring compact
        v16_parts = []
        for k, label in [('v16_lh_score','LH'),('v16_mh_score','MH'),('v16_tb_score','TB'),('v16_ln_score','LN'),('v16_ta_score','TA')]:
            if od.get(k):
                v16_parts.append(f"{label}={od[k]}")
        if v16_parts:
            lines.append(f"V16: {' '.join(v16_parts)}")
        
        # 5) V17 Method Routing compact (chi 200 ky tu)
        if od.get('v17_routing'):
            lines.append(f"V17: {od['v17_routing'][:400]}")
        
        # 6) V18 Detective
        if od.get('v18_detective'):
            lines.append(f"{od['v18_detective']}")
        
        # 7) V29.5: SMART FACTOR INJECTION — CHỈ inject PP GỐC theo câu hỏi
        q_lower = str(od.get('_question', '')).lower()
        
        # Xác định PP GỐC
        if any(kw in q_lower for kw in ['tuổi','mấy tuổi','bao nhiêu tuổi']):
            primary_keys = [('v24_tb_factors','TB','Thiết Bản'), ('v24_mh_factors','MH','Mai Hoa')]
            q_label = 'TUỔI'
        elif any(kw in q_lower for kw in ['cái gì','loại gì','là gì','vật gì']):
            primary_keys = [('v24_mh_factors','MH','Mai Hoa'), ('v24_tb_factors','TB','Thiết Bản')]
            q_label = 'CÁI GÌ'
        elif any(kw in q_lower for kw in ['ai ','người nào','ai đó','là ai']):
            primary_keys = [('v24_mh_factors','MH','Mai Hoa'), ('v24_ln_factors','LN','Đại Lục Nhâm')]
            q_label = 'AI (NGƯỜI)'
        elif any(kw in q_lower for kw in ['ở đâu','nơi nào','phương nào','hướng nào']):
            primary_keys = [('v24_km_factors','KM','Kỳ Môn'), ('v24_ln_factors','LN','Đại Lục Nhâm')]
            q_label = 'Ở ĐÂU'
        elif any(kw in q_lower for kw in ['khi nào','bao giờ','lúc nào','thời điểm']):
            primary_keys = [('v24_ln_factors','LN','Đại Lục Nhâm'), ('v23_lh_factors','LH','Lục Hào')]
            q_label = 'KHI NÀO'
        elif any(kw in q_lower for kw in ['tại sao','vì sao','nguyên nhân','do đâu']):
            primary_keys = [('v23_lh_factors','LH','Lục Hào'), ('v24_km_factors','KM','Kỳ Môn')]
            q_label = 'TẠI SAO'
        elif any(kw in q_lower for kw in ['thế nào','như thế nào','ra sao','tình trạng']):
            primary_keys = [('v23_lh_factors','LH','Lục Hào'), ('v24_km_factors','KM','Kỳ Môn')]
            q_label = 'THẾ NÀO'
        elif any(kw in q_lower for kw in ['cái nào','người nào','chọn','nên chọn','hay là','hoặc']):
            primary_keys = [('v24_mh_factors','MH','Mai Hoa'), ('v24_km_factors','KM','Kỳ Môn')]
            q_label = 'CÁI NÀO (CHỌN)'
        elif any(kw in q_lower for kw in ['bao nhiêu','mấy','số lượng']):
            primary_keys = [('v24_tb_factors','TB','Thiết Bản'), ('v24_mh_factors','MH','Mai Hoa')]
            q_label = 'SỐ LƯỢNG'
        else:
            primary_keys = [('v23_lh_factors','LH','Lục Hào'), ('v24_km_factors','KM','Kỳ Môn')]
            q_label = 'CÓ/KHÔNG'
        
        # Inject FULL factors cho PP GỐC
        primary_labels = [pk[1] for pk in primary_keys]
        lines.append(f"\n🎯 PP GỐC cho câu hỏi [{q_label}]: {', '.join(pk[2] for pk in primary_keys)}")
        
        for fkey, flabel, fname in primary_keys:
            fdata = od.get(fkey, [])
            if fdata and isinstance(fdata, list) and len(fdata) > 0:
                lines.append(f"\n--- ★ {fname} ({len(fdata)} yếu tố) [PP GỐC] ---")
                for f in fdata:
                    lines.append(f"  • {f}")
        
        # PP PHỤ: chỉ hiện verdict tóm tắt (KHÔNG liệt kê factors)
        ALL_METHODS = [
            ('v24_km_factors','KM','Kỳ Môn'), ('v23_lh_factors','LH','Lục Hào'),
            ('v24_mh_factors','MH','Mai Hoa'), ('v24_tb_factors','TB','Thiết Bản'),
            ('v24_ln_factors','LN','Đại Lục Nhâm'), ('v24_ta_factors','TA','Thái Ất')
        ]
        secondary = [m for m in ALL_METHODS if m[1] not in primary_labels]
        sec_parts = []
        for fkey, flabel, fname in secondary:
            fdata = od.get(fkey, [])
            count = len(fdata) if fdata and isinstance(fdata, list) else 0
            sec_parts.append(f"{fname}({count} yếu tố)")
        if sec_parts:
            lines.append(f"\n--- PP Phụ (chỉ tham khảo): {', '.join(sec_parts)} ---")
        
        lines.append("=== [HET V27 COMPACT] ===\n")
        return "\n".join(lines)

    def test_connection(self):
        return True, "V27.0 Unified + Deep Integration — Offline + Online fallback"

    def _try_online_ai(self, question, chart_data=None, mai_hoa_data=None, luc_hao_data=None, topic=None,
                        offline_analysis_data=None):
        """V11.1: AI Online là phân tích CHÍNH.
        Nhận raw data từ 3 phương pháp + offline analysis → phân tích sâu, loại bỏ vô lý."""
        try:
            import streamlit as st
            # V35.8-FIX: AGGRESSIVE KEY RESOLUTION — tìm key từ TẤT CẢ nguồn
            api_key = self._api_key
            
            # Source 2: session_state.gemini_key (set bởi app.py khi activate)
            if not api_key:
                api_key = getattr(st, 'session_state', {}).get('gemini_key')
            
            # Source 3: session_state._resolved_api_key (set bởi auto-init)
            if not api_key:
                api_key = getattr(st, 'session_state', {}).get('_resolved_api_key')
            
            # Source 4: Lấy từ gemini_helper object trong session (nếu GeminiQMDGHelper đã init)
            if not api_key:
                _gh = getattr(st, 'session_state', {}).get('gemini_helper')
                if _gh and hasattr(_gh, 'api_key') and _gh.api_key:
                    api_key = _gh.api_key
                elif _gh and hasattr(_gh, 'api_keys') and _gh.api_keys:
                    api_key = _gh.api_keys[0]
            
            # Source 5: st.secrets (Streamlit Cloud secrets.toml)
            if not api_key:
                try:
                    api_key = st.secrets.get('GEMINI_API_KEY', '')
                except Exception:
                    pass
            
            if not api_key:
                self.log_step("Online AI", "SKIP", "Không tìm thấy API Key từ bất kỳ nguồn nào")
                return None  # Không có key → fallback về Python
            
            # V35.8-FIX: Cache key cho lần gọi sau
            self._api_key = api_key
            
            from gemini_helper import GeminiQMDGHelper
            gemini = GeminiQMDGHelper(api_key)
            # V13.0: Bỏ test_connection() — tiết kiệm 1 API call/câu hỏi
            
            self.log_step("Online AI", "RUNNING", f"Gemini đang phân tích sâu: {question[:50]}...")
            
            # ══════════════════════════════════════════════════════════════════
            # V36.0: AI ONLINE ĐỘC LẬP — ĐỌC RAW DATA TRƯỚC, VERDICT SAU
            # ══════════════════════════════════════════════════════════════════
            
            od = offline_analysis_data or {}
            v22 = od.get('v22_unified_strength', {})
            
            # ═══ PHẦN 1: RAW DATA — Gemini TỰ ĐỌC QUẺ ═══
            raw_data_section = ""
            
            # --- 1A: THÔNG TIN CHUNG ---
            dung_than_ak = od.get('dung_than', '?')
            hanh_dt = v22.get('hanh_dt', '?')
            category_label = od.get('category_label', '?')
            
            raw_data_section += (
                f"═══ THÔNG TIN CHUNG ═══\n"
                f"Câu hỏi: {question}\n"
                f"Dụng Thần CHÍNH: {dung_than_ak} | Hành DT: {hanh_dt}\n"
                f"Chủ đề: {category_label}\n"
            )
            # V41.0: Multi-DT cho câu hỏi phức hợp
            all_dts = _get_all_dung_than(question)
            if len(all_dts) > 1:
                raw_data_section += f"⚠️ CÂU HỎI PHỨC HỢP — Có {len(all_dts)} Dụng Thần: {' + '.join(all_dts)}\n"
                raw_data_section += f"   → Phân tích primary DT ({all_dts[0]}) trước, rồi bổ sung secondary DT ({', '.join(all_dts[1:])})\n"
            raw_data_section += "\n"
            
            # --- 1B: RAW LỤC HÀO (chi tiết nhất) ---
            if od.get('v23_lh_factors'):
                raw_data_section += f"═══ [1] LỤC HÀO — DỮ LIỆU THÔ ═══\n"
                for f_item in od['v23_lh_factors']:
                    raw_data_section += f"• {f_item}\n"
                raw_data_section += "\n"
            
            # --- 1C: RAW KỲ MÔN ---
            if od.get('v24_km_factors'):
                raw_data_section += f"═══ [2] KỲ MÔN ĐỘN GIÁP — DỮ LIỆU THÔ ═══\n"
                for f_item in od['v24_km_factors']:
                    raw_data_section += f"• {f_item}\n"
                raw_data_section += "\n"
            
            # --- 1D: RAW MAI HOA ---
            if od.get('v24_mh_factors'):
                raw_data_section += f"═══ [3] MAI HOA DỊCH SỐ — DỮ LIỆU THÔ ═══\n"
                mh_items = od['v24_mh_factors'] if isinstance(od['v24_mh_factors'], list) else [od['v24_mh_factors']]
                for f_item in mh_items:
                    raw_data_section += f"• {f_item}\n"
                raw_data_section += "\n"
            
            # --- 1E: RAW ĐẠI LỤC NHÂM ---
            luc_nham_ctx = ""
            try:
                from dai_luc_nham import tinh_dai_luc_nham, phan_tich_chuyen_sau
                if chart_data and isinstance(chart_data, dict) and 'can_ngay' in chart_data:
                    ln_data = tinh_dai_luc_nham(chart_data.get('can_ngay','Giáp'), chart_data.get('chi_ngay','Tý'), chart_data.get('chi_gio','Ngọ'), chart_data.get('tiet_khi','Đông Chí'))
                    ln_deep = phan_tich_chuyen_sau(ln_data, question, topic or 'chung')
                    luc_nham_ctx = f"═══ [4] ĐẠI LỤC NHÂM — DỮ LIỆU THÔ ═══\n"
                    for d in ln_deep.get('details', []): luc_nham_ctx += f"• {d}\n"
                    luc_nham_ctx += f"• Sơ-Trung-Mạt Truyền verdict: {ln_deep.get('verdict', '?')}\n\n"
            except Exception: pass
            if od.get('v24_ln_factors'):
                luc_nham_ctx += f"═══ [4b] ĐẠI LỤC NHÂM — FACTORS BỔ SUNG ═══\n"
                ln_items = od['v24_ln_factors'] if isinstance(od['v24_ln_factors'], list) else [od['v24_ln_factors']]
                for f_item in ln_items:
                    luc_nham_ctx += f"• {f_item}\n"
                luc_nham_ctx += "\n"
            raw_data_section += luc_nham_ctx
            
            # --- 1F: RAW THIẾT BẢN + THÁI ẤT ---
            if od.get('v24_tb_factors'):
                raw_data_section += f"═══ [5] THIẾT BẢN THẦN SỐ — DỮ LIỆU THÔ ═══\n"
                tb_items = od['v24_tb_factors'] if isinstance(od['v24_tb_factors'], list) else [od['v24_tb_factors']]
                for f_item in tb_items:
                    raw_data_section += f"• {f_item}\n"
                raw_data_section += "\n"
            
            thai_at_ctx = ""
            try:
                from thai_at_than_so import tinh_thai_at_than_so
                import datetime
                now = datetime.datetime.now()
                ta_can = chart_data.get('can_ngay','Giáp') if chart_data and isinstance(chart_data, dict) else 'Giáp'
                ta_chi = chart_data.get('chi_ngay','Tý') if chart_data and isinstance(chart_data, dict) else 'Tý'
                ta_data = tinh_thai_at_than_so(now.year, now.month, ta_can, ta_chi)
                thai_at_ctx = f"═══ [6] THÁI ẤT THẦN SỐ — DỮ LIỆU THÔ ═══\n"
                ta_cung = ta_data.get('thai_at_cung', {})
                thai_at_ctx += f"• Cung {ta_cung.get('cung','?')} ({ta_cung.get('ten_cung','?')}) {ta_cung.get('hanh_cung','?')}\n"
                for d in ta_data.get('luan_giai', {}).get('details', []): thai_at_ctx += f"• {d}\n"
                thai_at_ctx += "\n"
            except Exception: pass
            if od.get('v24_ta_factors'):
                thai_at_ctx += f"═══ [6b] THÁI ẤT — FACTORS BỔ SUNG ═══\n"
                ta_items = od['v24_ta_factors'] if isinstance(od['v24_ta_factors'], list) else [od['v24_ta_factors']]
                for f_item in ta_items:
                    thai_at_ctx += f"• {f_item}\n"
                thai_at_ctx += "\n"
            raw_data_section += thai_at_ctx
            
            # --- 1G: SĐ_MASTER (sơ đồ tổng hợp) ---
            if od.get('v31_master_diagram'):
                raw_data_section += f"═══ SĐ MASTER — SƠ ĐỒ TƯƠNG TÁC TỔNG HỢP ═══\n"
                raw_data_section += od['v31_master_diagram'] + "\n\n"
            
            # --- 1H: BẢNG WEIGHTED SCORING ---
            if v22:
                raw_data_section += (
                    f"═══ BẢNG SCORING (chỉ tham khảo) ═══\n"
                    f"• Điểm Tổng Hợp: {v22.get('unified_pct', '?')}%\n"
                    f"• Hành DT: {v22.get('hanh_dt', '?')} | Trường Sinh: {v22.get('ts_stage', '?')} | Ngũ Khí: {v22.get('ngu_khi', '?')}\n"
                    f"• Tier: {v22.get('tier_cap', '?')}\n\n"
                )
            
            # --- 1I: YẾU TỐ TÁC ĐỘNG (từ offline engine) ---
            if od.get('impact_evidence'):
                raw_data_section += f"═══ YẾU TỐ TÁC ĐỘNG VÀO DỤNG THẦN ═══\n"
                for e in od['impact_evidence'][:15]:  # tối đa 15
                    raw_data_section += f"• {e}\n"
                raw_data_section += "\n"
            
            # --- V40.4: MAI HOA — HỖ QUÁI + BIẾN QUÁI + NGHĨA (INJECT TRỰC TIẾP) ---
            _mh_ho = od.get('mai_hoa_ho_quai', '')
            _mh_bien = od.get('mai_hoa_bien_quai', '')
            _mh_nghia = od.get('mai_hoa_nghia', '')
            _mh_interp = od.get('mai_hoa_interpretation', '')
            if _mh_ho or _mh_bien or _mh_nghia:
                raw_data_section += f"═══ [3b] MAI HOA — HỖ QUÁI + BIẾN QUÁI ═══\n"
                if _mh_ho: raw_data_section += f"• Hỗ Quái: {_mh_ho}\n"
                if _mh_bien: raw_data_section += f"• Biến Quái: {_mh_bien}\n"
                if _mh_nghia: raw_data_section += f"• Quẻ Nghĩa: {_mh_nghia}\n"
                if _mh_interp: raw_data_section += f"• Giải nghĩa: {_mh_interp}\n"
                raw_data_section += "\n"
            
            # --- V40.4: LỤC HÀO — TÊN QUẺ + CUNG (INJECT TRỰC TIẾP) ---
            _lh_ten = od.get('luc_hao_ten_que', '')
            _lh_cung = od.get('luc_hao_cung', '')
            if _lh_ten or _lh_cung:
                raw_data_section += f"═══ [1b] LỤC HÀO — TÊN QUẺ + CUNG ═══\n"
                if _lh_ten: raw_data_section += f"• Tên quẻ: {_lh_ten}\n"
                if _lh_cung: raw_data_section += f"• Cung: {_lh_cung}\n"
                raw_data_section += "\n"
            
            # --- V40.5: LỤC HÀO — BẢNG 6 HÀO RAW (chi tiết từng hào) ---
            if luc_hao_data and isinstance(luc_hao_data, dict):
                _lh_ban = luc_hao_data.get('ban', {})
                if _lh_ban and isinstance(_lh_ban, dict):
                    raw_data_section += f"═══ [1c] LỤC HÀO — BẢNG 6 HÀO CHI TIẾT ═══\n"
                    _dong_hao = luc_hao_data.get('dong_hao', [])
                    for _h_num in range(1, 7):
                        _h = _lh_ban.get(_h_num, _lh_ban.get(str(_h_num), {}))
                        if isinstance(_h, dict):
                            _chi = _h.get('chi', '?')
                            _hanh = _h.get('hanh', '?')
                            _lt = _h.get('luc_than', _h.get('luc_thu', '?'))
                            _dong = '🔴 ĐỘNG' if _h_num in _dong_hao else '⚪ Tĩnh'
                            _hoa = _h.get('hoa', _h.get('bien', ''))
                            _the_ung = ''
                            if _h.get('the'): _the_ung = ' [THẾ]'
                            if _h.get('ung'): _the_ung = ' [ỨNG]'
                            _line = f"• Hào {_h_num}: {_chi}({_hanh}) | {_lt}{_the_ung} | {_dong}"
                            if _hoa: _line += f" → Hóa {_hoa}"
                            raw_data_section += _line + "\n"
                    # Chi tháng/ngày bổ sung
                    _ct = luc_hao_data.get('chi_thang', '')
                    _cn = luc_hao_data.get('chi_ngay', '')
                    if _ct or _cn:
                        raw_data_section += f"• Nguyệt Kiến: {_ct} | Nhật Thần: {_cn}\n"
                    raw_data_section += "\n"
            
            # --- V40.5: KỲ MÔN — BÀN 9 CUNG RAW (layout đầy đủ) ---
            if chart_data and isinstance(chart_data, dict):
                _tb = chart_data.get('thien_ban', {})
                _nb = chart_data.get('nhan_ban', {})
                _sb = chart_data.get('than_ban', {})
                _ctb = chart_data.get('can_thien_ban', {})
                if _tb and isinstance(_tb, dict) and len(_tb) >= 8:
                    raw_data_section += f"═══ [2b] KỲ MÔN — BÀN 9 CUNG CHI TIẾT ═══\n"
                    raw_data_section += f"• Cục: {chart_data.get('cuc', '?')} | Tiết Khí: {chart_data.get('tiet_khi', '?')}\n"
                    raw_data_section += f"• Can Ngày: {chart_data.get('can_ngay', '?')}{chart_data.get('chi_ngay', '?')} | Can Giờ: {chart_data.get('can_gio', '?')}{chart_data.get('chi_gio', '?')}\n"
                    for _cung in range(1, 10):
                        _sao = _tb.get(_cung, _tb.get(str(_cung), ''))
                        _cua = _nb.get(_cung, _nb.get(str(_cung), ''))
                        _than = _sb.get(_cung, _sb.get(str(_cung), ''))
                        _can = _ctb.get(_cung, _ctb.get(str(_cung), ''))
                        if _sao or _cua or _than:
                            _sao_str = _sao if isinstance(_sao, str) else str(_sao.get('sao', '?')) if isinstance(_sao, dict) else str(_sao)
                            _cua_str = _cua if isinstance(_cua, str) else str(_cua.get('mon', '?')) if isinstance(_cua, dict) else str(_cua)
                            _than_str = _than if isinstance(_than, str) else str(_than.get('than', '?')) if isinstance(_than, dict) else str(_than)
                            raw_data_section += f"• Cung {_cung}: Sao={_sao_str} | Cửa={_cua_str} | Thần={_than_str} | Can={_can}\n"
                    raw_data_section += "\n"
            
            # --- V40.5: VẠN VẬT LOẠI TƯỢNG — TRỰC TIẾP TỪ FILE TỔNG HỢP (2226+ items) ---
            _vv_hanh = v22.get('hanh_dt', '')
            _ts_stage = v22.get('ts_stage', '')
            if _vv_hanh:
                try:
                    from van_vat_tong_hop import smart_van_vat_for_question, get_tham_tu_mo_ta, TRUONG_SINH_TRANG_THAI
                    # V40.9: Smart filter — chỉ lấy categories LIÊN QUAN câu hỏi
                    _vv_text, _vv_topics = smart_van_vat_for_question(_vv_hanh, _ts_stage or 'Quan Đới', question)
                    if _vv_text:
                        _topic_str = ', '.join(_vv_topics)
                        raw_data_section += f"═══ VẠN VẬT LOẠI TƯỢNG — LỌC THEO CÂU HỎI [{_topic_str}] ═══\n"
                        raw_data_section += _vv_text + "\n\n"
                    # Thám tử mô tả chi tiết (cho câu hỏi cụ thể)
                    _thamtu_text = get_tham_tu_mo_ta(_vv_hanh, _ts_stage or 'Quan Đới', question)
                    if _thamtu_text:
                        raw_data_section += _thamtu_text + "\n\n"
                    
                    # V41.2: INJECT SỐ LƯỢNG TỪ VẠN VẬT — ĐÂY LÀ NGUỒN CHÍNH CHO CÂU HỎI SỐ
                    _ts_trang_thai = TRUONG_SINH_TRANG_THAI.get(_ts_stage or 'Quan Đới', {})
                    _HD_SO = {'Thủy': '1,6', 'Hỏa': '2,7', 'Mộc': '3,8', 'Kim': '4,9', 'Thổ': '5,10'}
                    raw_data_section += f"═══ SỐ HỌC VẠN VẬT (NGUỒN CHÍNH CHO CÂU HỎI SỐ LƯỢNG) ═══\n"
                    raw_data_section += f"• Hành DT: {_vv_hanh} → Hà Đồ Số: {_HD_SO.get(_vv_hanh, '5,10')}\n"
                    raw_data_section += f"• 12 Trường Sinh: {_ts_stage} → Số lượng: {_ts_trang_thai.get('so_luong', '?')}\n"
                    raw_data_section += f"• Con số cụ thể: {_ts_trang_thai.get('so', '?')}\n"
                    raw_data_section += f"• Kích thước: {_ts_trang_thai.get('kich_thuoc', '?')}\n"
                    raw_data_section += f"• Chất lượng: {_ts_trang_thai.get('chat_luong', '?')}\n"
                    raw_data_section += f"• Tình trạng: {_ts_trang_thai.get('tinh_trang', '?')}\n"
                    raw_data_section += f"• Trọng lượng: {_ts_trang_thai.get('trong_luong', '?')}\n"
                    raw_data_section += f"• Nhiệt độ: {_ts_trang_thai.get('nhiet_do', '?')}\n"
                    raw_data_section += f"• Âm thanh: {_ts_trang_thai.get('am_thanh', '?')}\n"
                    raw_data_section += f"• Xu hướng: {_ts_trang_thai.get('huong_phat_trien', '?')}\n"
                    raw_data_section += f"⚠️ KHI TRẢ LỜI CÂU HỎI SỐ LƯỢNG: PHẢI dùng con số từ mục này, KHÔNG ĐƯỢC nói 'không xác định'\n\n"
                except Exception:
                    # Fallback: dùng data inline nếu file không có
                    _vv_vat = v22.get('hanh_vat', NGU_HANH_VAT_CHAT.get(_vv_hanh, {}))
                    _vv_cu_the = v22.get('van_vat_cu_the', {})
                    _vv_tier = v22.get('tier_cap', '')
                    raw_data_section += f"═══ VẠN VẬT LOẠI TƯỢNG — TRỰC TIẾP ═══\n"
                    raw_data_section += f"• Hành DT: {_vv_hanh} | Tier: {_vv_tier}\n"
                    raw_data_section += f"• Hình dáng: {_vv_vat.get('hinh', '?')}\n"
                    raw_data_section += f"• Chất liệu: {_vv_vat.get('chat_lieu', '?')}\n"
                    raw_data_section += f"• Màu sắc: {_vv_vat.get('mau', '?')}\n"
                    raw_data_section += f"• Hướng: {_vv_vat.get('huong', '?')}\n"
                    raw_data_section += f"• Vị: {_vv_vat.get('vi', '?')}\n"
                    raw_data_section += f"• Cơ thể: {_vv_vat.get('co_the', '?')}\n"
                    if _vv_cu_the:
                        raw_data_section += f"• Đồ vật: {_vv_cu_the.get('do_vat', '?')}\n"
                        raw_data_section += f"• Nhà: {_vv_cu_the.get('nha_cua', '?')}\n"
                        raw_data_section += f"• Người: {_vv_cu_the.get('nguoi', '?')}\n"
                        raw_data_section += f"• Bệnh: {_vv_cu_the.get('benh', '?')}\n"
                    raw_data_section += "\n"
            
            # --- V40.4: 12 TRƯỜNG SINH — TRỰC TIẾP (chi tiết đầy đủ) ---
            _ts_stage = v22.get('ts_stage', '')
            _ts_info = TRUONG_SINH_POWER.get(_ts_stage, {}) if _ts_stage else {}
            if _ts_stage:
                raw_data_section += f"═══ 12 TRƯỜNG SINH — TRỰC TIẾP ═══\n"
                raw_data_section += f"• Giai đoạn hiện tại: {_ts_stage}\n"
                raw_data_section += f"• Power: {_ts_info.get('power', '?')}% | Cấp: {_ts_info.get('cap', '?')}\n"
                raw_data_section += f"• Con người: {_ts_info.get('con_nguoi', '?')}\n"
                raw_data_section += f"• Tình trạng vật: {_ts_info.get('vat', '?')}\n"
                raw_data_section += f"• Tuổi ước lượng: {_ts_info.get('tuoi_min', '?')}-{_ts_info.get('tuoi_max', '?')}\n"
                # Ngũ Khí bổ sung
                _nk = v22.get('ngu_khi', '')
                _nk_info = NGU_KHI_POWER.get(_nk, {})
                if _nk:
                    raw_data_section += f"• Ngũ Khí: {_nk} — {_nk_info.get('label', '?')} (power={_nk_info.get('power', '?')}%)\n"
                raw_data_section += "\n"
            
            # V40.5: Giới hạn RAW data section → 40K chars max (đủ cho bảng hào + 9 cung)
            if len(raw_data_section) > 40000:
                raw_data_section = raw_data_section[:18000] + "\n\n[...DỮ LIỆU CẮT NGẮN...]\n\n" + raw_data_section[-18000:]
            
            # ═══ PHẦN 2: OFFLINE VERDICT (chỉ 1 block ngắn để so sánh) ═══
            offline_verdict_block = (
                f"═══ VERDICT OFFLINE (Python Engine — tham khảo) ═══\n"
                f"KỲ MÔN: {od.get('ky_mon_verdict','?')} — {od.get('ky_mon_reason','')[:100]}\n"
                f"LỤC HÀO: {od.get('luc_hao_verdict','?')} — {od.get('luc_hao_reason','')[:100]}\n"
                f"MAI HOA: {od.get('mai_hoa_verdict','?')} — {od.get('mai_hoa_reason','')[:100]}\n"
                f"ĐẠI LỤC NHÂM: {od.get('luc_nham_verdict','?')} — {od.get('luc_nham_reason','')[:100]}\n"
                f"THÁI ẤT: {od.get('thai_at_verdict','?')} — {od.get('thai_at_reason','')[:100]}\n"
                f"TỔNG: Điểm = {v22.get('unified_pct', '?')}% | Mức = {v22.get('tier_cap', '?')}\n"
            )
            
            # ═══ PHẦN 3: PHÂN LOẠI CÂU HỎI ═══
            q_lower_online = question.lower()
            if any(kw in q_lower_online for kw in ['cái gì','loại gì','sản xuất gì','làm gì','mặt hàng','sản phẩm gì','buôn bán gì','kinh doanh gì','nghề gì','ngành gì','là gì','thuộc loại','hình dạng','màu gì','chất liệu','tên gì','ai vậy','người nào','giống gì','như thế nào','trông như','nó là gì','loại nào','mẫu gì','kiểu gì','thể loại']):
                question_type = 'WHAT'
                question_type_label = 'CÂU HỎI CỤ THỂ (CÁI GÌ/LOẠI GÌ/AI?)'
            elif any(kw in q_lower_online for kw in ['ở đâu','hướng nào','phương nào','tìm đâu','chỗ nào','nơi nào']):
                question_type = 'WHERE'
                question_type_label = 'CÂU HỎI VỀ VỊ TRÍ/HƯỚNG'
            elif any(kw in q_lower_online for kw in ['khi nào','bao giờ','lúc nào','thời điểm']):
                question_type = 'WHEN'
                question_type_label = 'CÂU HỎI VỀ THỜI GIAN'
            elif any(kw in q_lower_online for kw in ['tuổi','bao nhiêu tuổi','mấy tuổi']):
                question_type = 'AGE'
                question_type_label = 'CÂU HỎI VỀ TUỔI TÁC'
            elif any(kw in q_lower_online for kw in ['bao nhiêu','mấy','số lượng']):
                question_type = 'COUNT'
                question_type_label = 'CÂU HỎI VỀ SỐ LƯỢNG'
            else:
                question_type = 'YESNO'
                question_type_label = 'CÂU HỎI CÓ/KHÔNG hoặc TỔNG QUÁT'
            
            # ═══ PHẦN 4: V38.2 AI ONLINE ĐỘC LẬP — LUẬN GIẢI TỰ DO ═══
            # V38.2: AI Online KHÔNG dùng 27 bước (chỉ dành cho Offline)
            # AI Online luận giải ĐỘC LẬP → so sánh Offline → KẾT LUẬN CHÍNH
            deep_prompt = (
                f"<system_role>\n"
                f"BẠN LÀ THIÊN CƠ ĐẠI SƯ V41.2 — BẬC THẦY HUYỀN HỌC ĐẲNG CẤP CAO NHẤT.\n"
                f"Kết hợp 6 PP: Kỳ Môn Độn Giáp + Lục Hào + Mai Hoa Dịch Số + Thiết Bản + Đại Lục Nhâm + Thái Ất.\n\n"
                f"NHIỆM VỤ V41.2: TỰ ĐỌC DỮ LIỆU THÔ + VẠN VẬT LOẠI TƯỢNG VÀ LUẬN GIẢI ĐỘC LẬP.\n"
                f"KHÔNG nhại lại verdict offline. PHẢI phân tích từng yếu tố, tìm mối liên hệ, và đưa ra nhận định RIÊNG.\n\n"
                f"QUY TẮC TUYỆT ĐỐI V41.2:\n"
                f"① VẠN VẬT LOẠI TƯỢNG là NGUỒN CHÍNH để trả lời mọi câu hỏi cụ thể.\n"
                f"② Câu hỏi SỐ LƯỢNG (bao nhiêu/mấy) → PHẢI tra Hà Đồ Số + Trường Sinh Số → trả SỐ CỤ THỂ.\n"
                f"③ Câu hỏi VẬT GÌ (cái gì/loại gì/sản xuất gì) → PHẢI tra đồ vật theo Hành + Trường Sinh.\n"
                f"④ Câu hỏi Ở ĐÂU → PHẢI tra hướng theo Ngũ Hành (Kim=Tây, Mộc=Đông, Thủy=Bắc, Hỏa=Nam, Thổ=Trung Tâm).\n"  
                f"⑤ TUYỆT ĐỐI KHÔNG được nói 'không thể xác định' hoặc 'không biết' — PHẢI cho câu trả lời cụ thể từ VẠN VẬT.\n"
                f"</system_role>\n\n"
                
                f"<question>\n"
                f"LOẠI: {question_type_label}\n"
                f"CÂU HỎI: {question}\n"
                f"</question>\n\n"
                
                f"<raw_chart_data>\n"
                f"DƯới đây là DỮ LIỆU THÔ từ 6 phương pháp. BẠN PHẢI ĐỌC KỸ TỪNG YẾU TỐ và TỰ LUẬN GIẢI.\n\n"
                f"{raw_data_section}"
                f"</raw_chart_data>\n\n"
                
                f"<offline_verdict_reference>\n"
                f"Dưới đây là kết luận của ENGINE OFFLINE (Python tính toán). Chỉ dùng để SO SÁNH SAU KHI bạn đã luận giải xong.\n"
                f"KHÔNG ĐƯỢC copy verdict này. Phải TỰ phân tích trước.\n\n"
                f"{offline_verdict_block}"
                f"</offline_verdict_reference>\n\n"
                
                f"<ngu_hanh_rules>\n"
                f"SINH: Mộc→Hỏa→Thổ→Kim→Thủy→Mộc | KHẮC: Mộc→Thổ→Thủy→Hỏa→Kim→Mộc\n"
                f"DT: tiền=Thê Tài | sếp/bệnh=Quan Quỷ | con/phúc=Tử Tôn | nhà/cha mẹ=Phụ Mẫu | bạn=Huynh Đệ\n"
                f"VƯỢNG: Nguyệt lệnh sinh/tỷ → VƯỢNG | khắc/tiết → SUY\n"
                f"12 Trường Sinh: Trường Sinh→Đế Vượng=MẠNH | Suy→Tuyệt=YẾU | Thai/Dưỡng=mầm mống\n"
                f"</ngu_hanh_rules>\n\n"
                
                f"<count_number_rules>\n"
                f"KHI CÂU HỎI VỀ SỐ LƯỢNG (bao nhiêu, mấy, số lượng):\n"
                f"PHẢI TRA BẢNG HÀ ĐỒ: Thủy=1,6 | Hỏa=2,7 | Mộc=3,8 | Kim=4,9 | Thổ=5,10\n"
                f"BẢNG LẠC THƯ: Thủy=1 | Mộc=3 | Thổ=5 | Kim=7 | Hỏa=9\n"
                f"BẢNG QUÁI SỐ: Càn=1 | Đoài=2 | Ly=3 | Chấn=4 | Tốn=5 | Khảm=6 | Cấn=7 | Khôn=8\n"
                f"QUY TẮC: DT VƯỢNG → lấy THÀNH SỐ (lớn) | DT BÌNH → lấy SINH SỐ (nhỏ) | DT SUY → giảm 1\n"
                f"VÍ DỤ: Hỏi 'mấy đứa con', DT=Tử Tôn(Thổ), Vượng → Số = 10 | Bình → Số = 5 | Suy → Số = 4\n"
                f"PHẢI KHẲNG ĐỊNH SỐ CỤ THỂ, KHÔNG ĐƯỢC nói 'không thể xác định'!\n"
                f"</count_number_rules>\n\n"
                
                f"<method_expertise>\n"
                f"THẾ MẠNH TỪNG PP (dùng đúng sở trường):\n"
                f"① LỤC HÀO: MẠNH NHẤT cho DỤNG THẦN vượng/suy, CÓ/KHÔNG, tình trạng.\n"
                f"   Key: Nguyệt lệnh ±8 | Nhật thần ±6 | Nguyên Thần sinh ±6 | Kỵ Thần khắc -8\n"
                f"   Tuần Không = chưa thành | Nguyệt Phá = phá | Phục Thần = ẩn giấu\n"
                f"   Hào động = đang thay đổi | Tiến Thần/Thoái Thần | Phản/Phục Ngâm\n\n"
                f"② KỲ MÔN: MẠNH NHẤT cho PHƯƠNG HƯỚNG + CHIẾN LƯỢC + TIMING.\n"
                f"   Key: BT(Can ngày) vs SV(Can giờ) | Cửu Tinh(Sao) | Bát Môn(Cửa) | Bát Thần\n"
                f"   Cửa CÁT: Khai+Hưu+Sinh | Cửa HUNG: Tử+Kinh+Thương\n"
                f"   Sao CÁT: Tâm+Nhậm+Phụ+Xung | Sao HUNG: Bồng+Nhuế+Trụ+Cầm\n"
                f"   Cách Cục: 81 cách đặc biệt → ảnh hưởng cực mạnh\n\n"
                f"③ MAI HOA: MẠNH NHẤT cho QUAN HỆ 2 BÊN, kết quả cuối.\n"
                f"   Key: Thể(mình) vs Dụng(đối phương) → Sinh/Khắc/Tỷ\n"
                f"   Dụng sinh Thể=ĐẠI CÁT | Thể sinh Dụng=MẤT | Dụng khắc Thể=HUNG\n"
                f"   Hỗ Quái=diễn biến giữa | Biến Quái=kết quả cuối\n\n"
                f"④ ĐẠI LỤC NHÂM: MẠNH cho DIỄN BIẾN THỜI GIAN.\n"
                f"   Key: Sơ Truyền=QUÁ KHỨ | Trung Truyền=HIỆN TẠI | Mạt Truyền=TƯƠNG LAI\n\n"
                f"⑤ THIẾT BẢN: MẠNH cho VẬT THỂ + SỐ LƯỢNG.\n"
                f"⑥ THÁI ẤT: MẠNH cho BỨC TRANH LỚN, xu hướng.\n"
                f"</method_expertise>\n\n"
                
                f"<reasoning_protocol_v38>\n"
                f"BẠN PHẢI THỰC HIỆN 4 BƯỚC SAU (THEO THỨ TỰ):\n\n"
                f"BƯỚC 1 — ĐỌC QUẺ ĐỘC LẬP:\n"
                f"  Đọc <raw_chart_data>, trích xuất TỪNG yếu tố quan trọng từ MỖI phương pháp.\n"
                f"  Phân tích: yếu tố đó CÁT hay HUNG? TẠI SAO? Dựa trên quy tắc nào?\n"
                f"  PHẢI trích dẫn DỮ LIỆU CỤ THỂ (VD: 'Nguyệt Lệnh sinh DT (+8) → vượng')\n\n"
                f"BƯỚC 2 — LUẬN GIẢI TỔNG HỢP:\n"
                f"  Kết hợp các yếu tố từ 6 PP → đưa ra VERDICT ĐỘC LẬP của BẠN.\n"
                f"  Phải giải thích LOGIC: Tại sao CÁT? Tại sao HUNG? Yếu tố nào quyết định?\n"
                f"  Chỉ ra: Yếu tố THUẬN (hỗ trợ) vs Yếu tố NGHỊCH (cản trở)\n\n"
                f"BƯỚC 3 — SO SÁNH VỚI OFFLINE:\n"
                f"  Đọc <offline_verdict_reference> → so sánh với phân tích CỦA BẠN.\n"
                f"  Ở đâu ĐỒNG Ý? Ở đâu KHÁC? Nếu khác → giải thích TẠI SAO bạn nghĩ khác.\n\n"
                f"BƯỚC 4 — KẾT LUẬN CUỐI CÙNG:\n"
                f"  Tổng hợp cả 2 góc nhìn (Online + Offline) → đưa ra KẾT LUẬN CUỐI.\n"
                f"  Phải TRẢ LỜI TRỰC TIẾP câu hỏi — KHÔNG né tránh.\n"
                f"</reasoning_protocol_v38>\n\n"
                
                f"<output_format_v42>\n"
                f"FORMAT BẮT BUỘC — DÒNG ĐẦU TIÊN LÀ VERDICT:\n\n"
                f"### 🏆 KẾT LUẬN CUỐI CÙNG\n"
                + (
                    # WHAT questions → trả lời VẬT GÌ, KHÔNG phải CÓ/KHÔNG
                    f"**📢 CÂU TRẢ LỜI: [Mô tả CỤ THỂ vật/sản phẩm/nghề/loại hình dựa trên Vạn Vật Loại Tượng của hành Dụng Thần]**\n"
                    f"**📦 HÀNH DT → VẬT:** [Kim=kim loại,máy móc | Mộc=gỗ,giấy,vải | Thủy=nước,chất lỏng | Hỏa=điện,lửa | Thổ=đất,gạch,gốm]\n"
                    f"**📋 MÔ TẢ:** [Chất liệu + Hình dạng + Màu sắc + Kích thước từ Ngũ Hành + 12 Trường Sinh]\n"
                    if question_type == 'WHAT' else
                    # WHERE questions → trả lời HƯỚNG/VỊ TRÍ
                    f"**📢 CÂU TRẢ LỜI: [Hướng/Vị trí CỤ THỂ dựa trên Ngũ Hành: Kim=TÂY, Mộc=ĐÔNG, Thủy=BẮC, Hỏa=NAM, Thổ=TRUNG TÂM]**\n"
                    f"**🧭 HƯỚNG:** [Phương hướng + khoảng cách + đặc điểm địa hình]\n"
                    if question_type == 'WHERE' else
                    # WHEN questions → trả lời THỜI GIAN
                    f"**📢 CÂU TRẢ LỜI: [Thời gian CỤ THỂ dựa trên Ứng Kỳ: ngày/tháng/năm Chi nào]**\n"
                    f"**⏳ ỨNG KỲ:** [Ngày/tháng/giờ Chi cụ thể + lý do]\n"
                    if question_type == 'WHEN' else
                    # Default (YESNO/AGE/COUNT) → CÓ/KHÔNG
                    f"**📢 VERDICT: [CÁT/HUNG/BÌNH] — [CÓ/KHÔNG/NÊN/KHÔNG NÊN] ([XX]%)**\n"
                    f"**📋 1 CÂU TÓM TẮT:** [Trả lời trực tiếp câu hỏi trong 1 câu ngắn gọn, dứt khoát]\n"
                ) +
                f"\n---\n\n"
                f"### 🔮 AI ONLINE — LUẬN GIẢI ĐỘC LẬP\n\n"
                f"**📖 ĐỌC QUẺ (Bước 1):**\n"
                f"• **Lục Hào:** [phân tích 3-5 yếu tố quan trọng nhất từ raw data LH]\n"
                f"• **Kỳ Môn:** [phân tích 3-5 yếu tố quan trọng nhất từ raw data KM]\n"
                f"• **Mai Hoa:** [phân tích Thể/Dụng/Hỗ/Biến + sinh khắc]\n"
                f"• **Đại Lục Nhâm / Thái Ất:** [tóm tắt ngắn]\n\n"
                f"**⚖️ TỔNG HỢP (Bước 2):**\n"
                f"• Yếu tố THUẬN: [liệt kê]\n"
                f"• Yếu tố NGHỊCH: [liệt kê]\n\n"
                f"**📊 SO SÁNH (Bước 3):**\n"
                f"• Đồng ý/Khác biệt với Offline Engine\n\n"
                f"**📢 CÂU TRẢ LỜI:** "
                + (
                    f"[MÔ TẢ CỤ THỂ vật/sản phẩm/người/loại dựa trên Vạn Vật — KHÔNG trả lời CÓ/KHÔNG]\n"
                    if question_type in ('WHAT', 'WHERE', 'WHEN') else
                    f"[KHẲNG ĐỊNH CÓ/KHÔNG — DỨT KHOÁT]\n"
                ) +
                f"**📋 VÌ SAO:** [TOP 3 bằng chứng CỤ THỂ trích từ data thô, có số điểm]\n"
                f"**⏳ ỨNG KỲ:** [Tháng/ngày/hướng cụ thể dựa trên Hành của DT — BẮT BUỘC]\n"
                f"**🔧 GIẢI PHÁP:** [Hành động cụ thể: nên làm gì, đợi khi nào, bổ sung hành gì]\n\n"
                f"GIỚI HẠN: Tối đa 800 chữ. Mỗi yếu tố phải TRÍCH DẪN từ data.\n"
                f"⛔ QUAN TRỌNG: DÒNG ĐẦU TIÊN PHẢI LÀ '### 🏆 KẾT LUẬN CUỐI CÙNG' + CÂU TRẢ LỜI.\n"
                f"CẤM TUYỆT ĐỐI: Bịa yếu tố, nói 'không thể xác định', nhại lại offline verdict.\n"
                + (
                f"⚠️ ĐÂY LÀ CÂU HỎI '{question_type_label}' → PHẢI trả lời MÔ TẢ CỤ THỂ (VẬT GÌ/Ở ĐÂU/KHI NÀO), KHÔNG trả lời CÓ/KHÔNG!\n"
                    if question_type in ('WHAT', 'WHERE', 'WHEN') else
                    f"BẮT BUỘC: Phải KHẲNG ĐỊNH CÓ hoặc KHÔNG. KHÔNG được né tránh.\n"
                ) +
                f"</output_format_v42>\n\n"
            )
            
            # ═══ V42.8e: THÊM DỮ LIỆU TỬ VI + XEM NGÀY CHO AI ONLINE ═══
            # Phát hiện dữ liệu Tử Vi / Xem Ngày trong câu hỏi → thêm rules tương ứng
            _has_tv_data = 'DỮ LIỆU TỬ VI ĐẨU SỐ' in question
            _has_xn_data = 'DỮ LIỆU XEM NGÀY ĐẸP' in question
            
            if _has_tv_data or _has_xn_data:
                deep_prompt += "\n<tu_vi_xem_ngay_rules>\n"
                deep_prompt += "═══ QUAN TRỌNG: CÂU HỎI CÓ DỮ LIỆU TỬ VI / XEM NGÀY ═══\n"
                deep_prompt += "Bạn PHẢI đọc và phân tích TOÀN BỘ dữ liệu này CÙNG với 6 PP huyền học.\n\n"
                
                if _has_tv_data:
                    deep_prompt += (
                        "═══ PHƯƠNG PHÁP LUẬN GIẢI TỬ VI (7 BƯỚC BẮT BUỘC) ═══\n"
                        "BƯỚC 1 — ĐỊNH CỤC DIỆN: Xét Âm Dương thuận/nghịch, Mệnh-Cục tương sinh/khắc.\n"
                        "  → Cục sinh Mệnh = thuận; Mệnh khắc Cục = khó.\n"
                        "BƯỚC 2 — MỆNH + THÂN: Chính tinh Miếu/Vượng/Đắc/Hãm + phụ tinh.\n"
                        "  → 14 Chính Tinh: Tử Vi, Thiên Cơ, Thái Dương, Vũ Khúc, Thiên Đồng, Liêm Trinh,\n"
                        "     Thiên Phủ, Thái Âm, Tham Lang, Cự Môn, Thiên Tướng, Thiên Lương, Thất Sát, Phá Quân.\n"
                        "BƯỚC 3 — TAM GIÁC VÀNG: Mệnh + Tài Bạch + Quan Lộc → tổng thể thành công.\n"
                        "BƯỚC 4 — TỨ HÓA: Lộc=tài lộc, Quyền=quyền lực, Khoa=danh tiếng, Kỵ=trở ngại.\n"
                        "  → Hóa Kỵ vào cung nào = cung đó gặp trở ngại lớn nhất.\n"
                        "  → Hóa Lộc+Quyền cùng cung = rất mạnh. Kỵ+Kình/Đà = tai họa.\n"
                        "BƯỚC 5 — ĐẠI HẠN + LƯU NIÊN: ĐH=10 năm, LN=năm nay.\n"
                        "  → ĐH tốt+LN xấu = bớt xấu; ĐH xấu+LN tốt = tạm vượt.\n"
                        "  → Xem chính tinh tại cung ĐH/LN + Tứ Hóa bay vào cung nào.\n"
                        "BƯỚC 6 — KẾT HỢP KỲ MÔN: Tử Vi (dài hạn) + Kỳ Môn (thời điểm) → phối hợp.\n"
                        "BƯỚC 7 — KẾT LUẬN: Trả lời DỰA TRÊN cả Tử Vi + Kỳ Môn. Lời khuyên CỤ THỂ.\n\n"
                        "LƯU Ý TỬ VI:\n"
                        "• Sao sáng (Miếu/Vượng) tại Mệnh = thuận lợi, Hãm = khó khăn\n"
                        "• Lộc Tồn + Hóa Lộc cùng cung = Song Lộc = rất giàu\n"
                        "• Kình Dương + Đà La + Hỏa/Linh = Sát tinh = khó khăn, nhưng có thể tốt nếu gặp Tử Vi/Thiên Phủ\n"
                        "• Tả Phụ + Hữu Bật + Thiên Khôi + Thiên Việt = quý nhân phù trợ\n"
                        "• Cô Thần + Quả Tú = cô đơn tình cảm\n"
                        "• Hồng Loan + Đào Hoa = tình duyên phong phú\n\n"
                    )
                
                if _has_xn_data:
                    deep_prompt += (
                        "═══ PHƯƠNG PHÁP ĐÁNH GIÁ XEM NGÀY (10 BƯỚC BẮT BUỘC) ═══\n"
                        "1. ĐIỂM NGÀY: ≥70=TỐT, 50-69=TRUNG BÌNH, <50=XẤU.\n"
                        "2. NGUYỆT PHÁ: CÓ → CẢNH BÁO MẠNH, tuyệt đối tránh việc lớn.\n"
                        "3. DƯƠNG CÔNG KỴ: CÓ → 13 ngày đại kỵ, tránh mọi việc quan trọng.\n"
                        "4. TAM NƯƠNG: CÓ → không nên khởi sự việc mới.\n"
                        "5. 12 TRỰC: Phân tích Trực có phù hợp loại việc không.\n"
                        "   Trực CÁT: Kiến, Mãn, Bình, Định, Thành, Khai\n"
                        "   Trực HUNG: Phá, Nguy, Thu, Bế\n"
                        "   Trực BÌNH: Trừ, Chấp\n"
                        "6. 28 TÚ: Sao CÁT=tốt, HUNG=cẩn thận.\n"
                        "7. HOÀNG ĐẠO/HẮC ĐẠO: Hoàng Đạo=thuận, Hắc Đạo=bất lợi.\n"
                        "   Sao Hoàng Đạo: Thanh Long, Minh Đường, Kim Quỹ, Kim Đường, Ngọc Đường, Tư Mệnh\n"
                        "   Sao Hắc Đạo: Thiên Hình, Chu Tước, Bạch Hổ, Thiên Lao, Nguyên Vũ, Câu Trận\n"
                        "8. THIÊN/NGUYỆT ĐỨC: CÓ → hóa giải hung, tăng cát.\n"
                        "9. KẾT HỢP KỲ MÔN: Ngày tốt+Cửa tốt=TIẾN, Ngày xấu+Cửa xấu=TRÁNH.\n"
                        "10. GỢI Ý: Ngày xấu → đề xuất ngày tốt gần. Ngày tốt → gợi ý giờ đẹp.\n\n"
                    )
                
                deep_prompt += (
                    "OUTPUT BỔ SUNG KHI CÓ TỬ VI / XEM NGÀY:\n"
                    "Sau phần 🔮 AI ONLINE, thêm MỤC MỚI:\n\n"
                )
                if _has_tv_data:
                    deep_prompt += (
                        "### 🔯 LUẬN GIẢI TỬ VI\n"
                        "• **Mệnh/Thân:** [phân tích chính tinh + trạng thái]\n"
                        "• **Tam Giác Vàng:** [Mệnh + Tài + Quan]\n"
                        "• **Tứ Hóa:** [Lộc/Quyền/Khoa/Kỵ → vào cung nào → ý nghĩa]\n"
                        "• **Đại Hạn + Lưu Niên:** [xu hướng hiện tại]\n"
                        "• **Kết hợp Kỳ Môn:** [vận mệnh + thời điểm → khuyên gì]\n\n"
                    )
                if _has_xn_data:
                    deep_prompt += (
                        "### 📅 ĐÁNH GIÁ NGÀY\n"
                        "• **Điểm/Verdict:** [X/100 — tốt/xấu]\n"
                        "• **Yếu tố TỐT:** [liệt kê lý do tốt]\n"
                        "• **Yếu tố XẤU:** [liệt kê lý do xấu]\n"
                        "• **Kết hợp Kỳ Môn:** [ngày + cửa + sao → tổng hợp]\n"
                        "• **Gợi ý:** [giờ đẹp hoặc ngày thay thế]\n\n"
                    )
                
                deep_prompt += "</tu_vi_xem_ngay_rules>\n"


            
            # V29.0: BỎ raw_que_data/_get_paranoid_context() — data ĐÃ CÓ ĐẦY ĐỦ trong offline_ctx + factors + answer_key
            # _get_paranoid_context chứa prompt CŨ ghi đè V28.9 → gây liệt kê PP, bịa %, CÁT/HUNG sai
            
            
            # V29.3: Gọi _call_ai (ĐÚNG tên method) — _call_ai_raw KHÔNG TỒN TẠI!
            result = gemini._call_ai(deep_prompt, use_hub=False)
            
            if result and len(str(result)) > 50:
                # V29.4: Strip phần "old format" mà Gemini tự thêm (bỏ qua output_format constraint)
                result_str = str(result)
                CUT_MARKERS = [
                    '📊 PHÂN TÍCH', '📊 PHÂ', 
                    '\n🎴 1.', '\n☯️ 2.', '\n🌸 3.', '\n🏯 4.', '\n🌟 5.',
                    '\n📝 TỔNG KẾT', '\n💡 HƯỚNG DẪN', '\n⏰ THỜI VẬN',
                    '\n🔮 TỔNG HỢP',
                    '\n📋 TỔNG HỢP', '\nBẮT BUỘC DIỄN GIẢI',
                ]
                for marker in CUT_MARKERS:
                    idx = result_str.find(marker)
                    if idx > 100:  # chỉ cắt nếu đã có nội dung phía trước (>100 chars)
                        result_str = result_str[:idx].rstrip()
                        break
                
                self.log_step("Online AI", "DONE", f"Gemini trả lời {len(result_str)} ký tự (stripped)")
                return result_str
            
            return None
            
        except Exception as e:
            self.log_step("Online AI", "SKIP", f"Lỗi: {str(e)[:80]}")
            return None

    # ===========================
    # V15.0: PHÂN TÍCH NỘI CUNG — XÂU DƯỢC (INTRA-PALACE FACTOR INTERACTION)
    # ===========================
    # Cung → Chi tương ứng (Lạc Thư Cửu Cung)
    CUNG_CHI_MAP = {1: 'Tý', 2: 'Sửu', 3: 'Dần', 4: 'Mão', 5: None, 6: 'Tuất', 7: 'Dậu', 8: 'Thìn', 9: 'Ngọ'}
    
    THAN_CAT_LIST = ['Trực Phù', 'Thái Âm', 'Lục Hợp', 'Cửu Thiên', 'Cửu Địa']
    THAN_HUNG_LIST = ['Đằng Xà', 'Bạch Hổ', 'Huyền Vũ']
    
    def _analyze_cung_factors(self, cung_num, chart_data, question, role_label):
        """
        V15.0: Phân tích TOÀN DIỆN các yếu tố TRONG 1 CUNG.
        
        Áp dụng 7 tầng: Quái Tượng, Sao↔Cung, Cửa↔Cung, Thần↔Cung,
        81 Cách Cục, Tuần Không, Dịch Mã + Tứ Trụ.
        
        role_label: "BẢN THÂN" hoặc "DỤNG THẦN (tên)"
        Trả về: (score, factors_detail_list, strength_label)
        """
        if not cung_num or not chart_data or not isinstance(chart_data, dict):
            return 0, [], "?"
        
        score = 0
        details = []
        q = question.lower() if question else ""
        
        hanh_cung = CUNG_NGU_HANH.get(cung_num, '?')
        quai_cung = QUAI_TUONG.get(cung_num, '?')
        thien_ban = chart_data.get('thien_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        than_ban = chart_data.get('than_ban', {})
        can_thien_ban = chart_data.get('can_thien_ban', {})
        dia_ban = chart_data.get('dia_ban', {})  # Can Địa Bàn
        
        # Lấy yếu tố tại cung
        sao = str(thien_ban.get(cung_num, thien_ban.get(str(cung_num), '?')))
        cua = str(nhan_ban.get(cung_num, nhan_ban.get(str(cung_num), '?')))
        than = str(than_ban.get(cung_num, than_ban.get(str(cung_num), '?')))
        can_thien = str(can_thien_ban.get(cung_num, can_thien_ban.get(str(cung_num), '')))
        can_dia = str(dia_ban.get(cung_num, dia_ban.get(str(cung_num), '')))
        
        details.append(f"**{'🏠' if 'BẢN THÂN' in role_label else '🎯'} NỘI CUNG {role_label} — Cung {cung_num} ({quai_cung}, {hanh_cung}):**")
        details.append(f"├ Sao: {sao} | Cửa: {cua} | Thần: {than}")
        details.append(f"├ Can Thiên: {can_thien} | Can Địa: {can_dia}")
        
        # ═══════ ① SAO ↔ CUNG ═══════
        sao_data = SAO_KY_MON.get(sao, {}) if SAO_KY_MON else {}
        sao_hanh = sao_data.get('hanh', SAO_GIAI_THICH.get(sao, {}).get('hanh', ''))
        sao_loai = sao_data.get('loai', '')
        
        if sao_hanh and hanh_cung and sao_hanh != '?' and hanh_cung != '?':
            if SINH.get(hanh_cung) == sao_hanh:  # Cung sinh Sao
                score += 5
                details.append(f"├ ① Sao {sao}({sao_hanh}): Cung {hanh_cung} SINH sao → sao được nuôi dưỡng (+5)")
            elif SINH.get(sao_hanh) == hanh_cung:  # Sao sinh Cung
                score += 8
                details.append(f"├ ① Sao {sao}({sao_hanh}): Sao SINH cung {hanh_cung} → cung được hỗ trợ (+8)")
            elif KHAC.get(sao_hanh) == hanh_cung:  # Sao khắc Cung
                score -= 5
                details.append(f"├ ① Sao {sao}({sao_hanh}): Sao KHẮC cung {hanh_cung} → cung bị phá (-5)")
            elif KHAC.get(hanh_cung) == sao_hanh:  # Cung khắc Sao
                score -= 8
                details.append(f"├ ① Sao {sao}({sao_hanh}): Cung {hanh_cung} KHẮC sao → sao bị chế (-8)")
            elif sao_hanh == hanh_cung:
                score += 3
                details.append(f"├ ① Sao {sao}({sao_hanh}): TỶ HÒA với cung → ổn định (+3)")
        
        # Sao Cát/Hung bonus
        if sao in SAO_CAT:
            score += 5
            details.append(f"├ ① ✅ Sao {sao} = CÁT TINH (+5)")
        elif sao in SAO_HUNG:
            score -= 5
            details.append(f"├ ① ⚠️ Sao {sao} = HUNG TINH (-5)")
        
        # ═══════ ② CỬA ↔ CUNG ═══════
        cua_data = CUA_KY_MON.get(cua, {}) if CUA_KY_MON else {}
        cua_hanh = cua_data.get('hanh', '')
        cua_loai = cua_data.get('loai', '')
        # Fallback: check with 'Môn' suffix
        if not cua_hanh:
            cua_key = cua if 'Môn' in cua else cua + ' Môn'
            cua_data = CUA_KY_MON.get(cua_key, {}) if CUA_KY_MON else {}
            cua_hanh = cua_data.get('hanh', '')
            cua_loai = cua_data.get('loai', '')
        
        if cua_hanh and hanh_cung and cua_hanh != '?' and hanh_cung != '?':
            if KHAC.get(cua_hanh) == hanh_cung:  # Cửa khắc Cung = BỨC (xấu nhất!)
                score -= 10
                details.append(f"├ ② Cửa {cua}({cua_hanh}): KHẮC cung {hanh_cung} → **BỨC** (xấu nhất! -10)")
            elif KHAC.get(hanh_cung) == cua_hanh:  # Cung khắc Cửa = CHẾ
                score -= 5
                details.append(f"├ ② Cửa {cua}({cua_hanh}): Cung {hanh_cung} khắc cửa → **CHẾ** (-5)")
            elif SINH.get(cua_hanh) == hanh_cung:  # Cửa sinh Cung
                score += 8
                details.append(f"├ ② Cửa {cua}({cua_hanh}): Cửa SINH cung {hanh_cung} → cung được tăng lực (+8)")
            elif SINH.get(hanh_cung) == cua_hanh:  # Cung sinh Cửa
                score += 5
                details.append(f"├ ② Cửa {cua}({cua_hanh}): Cung {hanh_cung} sinh cửa → ổn (+5)")
            elif cua_hanh == hanh_cung:
                score += 3
                details.append(f"├ ② Cửa {cua}({cua_hanh}): TỶ HÒA với cung → hòa hợp (+3)")
        
        # Cửa Cát/Hung bonus
        cua_name = cua.replace(' Môn', '').replace('Môn', '').strip()
        if cua_name in CUA_CAT or cua in CUA_CAT:
            score += 8
            details.append(f"├ ② ✅ Cửa {cua} = ĐẠI CÁT MÔN (+8)")
        elif cua_name in CUA_HUNG or cua in CUA_HUNG:
            score -= 8
            details.append(f"├ ② ⚠️ Cửa {cua} = HUNG MÔN (-8)")
        
        # ═══════ ③ THẦN ↔ CUNG ═══════
        than_data = THAN_KY_MON.get(than, {}) if THAN_KY_MON else {}
        than_hanh = than_data.get('hanh', '')
        
        if than_hanh and hanh_cung and than_hanh != '?' and hanh_cung != '?':
            if SINH.get(than_hanh) == hanh_cung:  # Thần sinh Cung
                score += 6
                details.append(f"├ ③ Thần {than}({than_hanh}): SINH cung {hanh_cung} → hỗ trợ (+6)")
            elif SINH.get(hanh_cung) == than_hanh:  # Cung sinh Thần
                score += 3
                details.append(f"├ ③ Thần {than}({than_hanh}): Cung {hanh_cung} nuôi thần → OK (+3)")
            elif KHAC.get(than_hanh) == hanh_cung:  # Thần khắc Cung
                score -= 6
                details.append(f"├ ③ Thần {than}({than_hanh}): KHẮC cung {hanh_cung} → cản trở (-6)")
            elif KHAC.get(hanh_cung) == than_hanh:  # Cung khắc Thần
                score -= 3
                details.append(f"├ ③ Thần {than}({than_hanh}): Cung chế thần → giảm lực thần (-3)")
        
        # Thần Cát/Hung bonus
        if than in self.THAN_CAT_LIST:
            score += 5
            details.append(f"├ ③ ✅ Thần {than} = CÁT THẦN (+5)")
        elif than in self.THAN_HUNG_LIST:
            score -= 5
            details.append(f"├ ③ ⚠️ Thần {than} = HUNG THẦN (-5)")
        
        # ═══════ ④ SAO + CỬA TỔ HỢP ═══════
        sao_cua_key = (sao, cua if 'Môn' in cua else cua + ' Môn')
        sao_cua_match = SAO_CUA_TO_HOP.get(sao_cua_key, SAO_CUA_TO_HOP_BS.get(sao_cua_key, {}))
        if sao_cua_match:
            luan = sao_cua_match.get('luan', '')
            if 'ĐẠI CÁT' in luan:
                score += 10
                details.append(f"├ ④ Tổ hợp {sao}+{cua}: **{luan}** (+10)")
            elif 'CÁT' in luan and 'HUNG' not in luan:
                score += 6
                details.append(f"├ ④ Tổ hợp {sao}+{cua}: {luan} (+6)")
            elif 'ĐẠI HUNG' in luan:
                score -= 10
                details.append(f"├ ④ Tổ hợp {sao}+{cua}: **{luan}** (-10)")
            elif 'HUNG' in luan:
                score -= 6
                details.append(f"├ ④ Tổ hợp {sao}+{cua}: {luan} (-6)")
            else:
                details.append(f"├ ④ Tổ hợp {sao}+{cua}: {luan}")
        
        # ═══════ ⑤ 81 CÁCH CỤC (Can Thiên × Địa) ═══════
        if can_thien and can_dia and can_thien != '?' and can_dia != '?':
            cach_key = f"{can_thien}+{can_dia}"
            cach_data = THAP_CAN_KHAC_UNG.get(cach_key, {})
            if cach_data:
                ten_cach = cach_data.get('ten', '?')
                cat_hung = cach_data.get('cat_hung', '?')
                luan = cach_data.get('luan', '')
                if 'ĐẠI CÁT' in cat_hung:
                    score += 15
                    details.append(f"├ ⑤ Cách Cục: **{ten_cach}** ({cach_key}) — {cat_hung} (+15)")
                elif cat_hung == 'CÁT':
                    score += 10
                    details.append(f"├ ⑤ Cách Cục: **{ten_cach}** ({cach_key}) — {cat_hung} (+10)")
                elif 'ĐẠI HUNG' in cat_hung:
                    score -= 15
                    details.append(f"├ ⑤ Cách Cục: **{ten_cach}** ({cach_key}) — {cat_hung} (-15)")
                elif cat_hung == 'HUNG':
                    score -= 10
                    details.append(f"├ ⑤ Cách Cục: **{ten_cach}** ({cach_key}) — {cat_hung} (-10)")
                else:  # CÁT/HUNG or BÌNH
                    details.append(f"├ ⑤ Cách Cục: **{ten_cach}** ({cach_key}) — {cat_hung}")
                details.append(f"│  └ 📖 {luan[:80]}")
            # Phản Ngâm / Phục Ngâm check
            phn = _check_phan_phuc_ngam(can_thien, can_dia)
            if phn == 'PHỤC NGÂM':
                score -= 8
                details.append(f"├ ⑤ ⚠️ {can_thien}+{can_dia} = **PHỤC NGÂM** (trì trệ, không tiến) (-8)")
            elif phn == 'PHẢN NGÂM':
                score -= 12
                details.append(f"├ ⑤ 🔴 {can_thien}+{can_dia} = **PHẢN NGÂM** (đảo ngược, phản bội) (-12)")
        
        # ═══════ ⑥ TUẦN KHÔNG ═══════
        can_ngay = chart_data.get('can_ngay', '')
        chi_ngay = chart_data.get('chi_ngay', '')
        khong_vong_list = _get_khong_vong(can_ngay, chi_ngay)
        cung_chi = self.CUNG_CHI_MAP.get(cung_num)
        
        if cung_chi and khong_vong_list and cung_chi in khong_vong_list:
            score -= 15
            details.append(f"├ ⑥ 🔴 Chi cung ({cung_chi}) lâm **TUẦN KHÔNG** → sự việc HƯ KHÔNG, không thực (-15)")
        
        # ═══════ ⑦ DỊCH MÃ ═══════
        chi_ngay_val = chart_data.get('chi_ngay', '')
        dich_ma = DICH_MA_MAP.get(chi_ngay_val, '')
        if cung_chi and dich_ma and cung_chi == dich_ma:
            if any(k in q for k in ['di chuyển', 'đi', 'xuất hành', 'du lịch', 'chuyển', 'đổi']):
                score += 5
                details.append(f"├ ⑦ ✅ Cung lâm **DỊCH MÃ** ({cung_chi}) → thuận lợi di chuyển/thay đổi (+5)")
            elif any(k in q for k in ['ổn định', 'giữ', 'ở yên', 'nhà', 'bất động']):
                score -= 5
                details.append(f"├ ⑦ ⚠️ Cung lâm **DỊCH MÃ** ({cung_chi}) → khó ổn định, hay biến động (-5)")
            else:
                details.append(f"├ ⑦ ℹ️ Cung lâm **DỊCH MÃ** ({cung_chi}) → có yếu tố di chuyển/thay đổi")
        
        # ═══════ Tính Can Tượng Ý (Tứ Trụ context) ═══════
        if can_thien and CAN_CHI_TUONG_Y.get(can_thien):
            can_tuong = CAN_CHI_TUONG_Y[can_thien]
            loai = can_tuong.get('loai_tuong', '')
            if loai and len(details) < 15:  # Giới hạn output
                details.append(f"├ 📋 Can {can_thien} tượng: {loai[:60]}")
        
        # ═══════════════════════════════════════
        # NGOẠI CUNG — YẾU TỐ BÊN NGOÀI TÁC ĐỘNG
        # ═══════════════════════════════════════
        details.append(f"├")
        details.append(f"├ **🌏 NGOẠI CUNG (yếu tố bên ngoài tác động):**")
        
        # ═══════ ⑧ LỆNH THÁNG / MÙA — Vượng Suy theo thời tiết ═══════
        try:
            lenh_hanh, lenh_mua = _get_lenh_thang_hanh()
            if lenh_hanh and hanh_cung and hanh_cung != '?':
                # Vượng: Cung hành = hành đang vượng theo mùa
                # Tướng: Cung hành được hành vượng sinh
                # Hưu: Cung hành sinh hành vượng (hao lực)
                # Tù: Cung hành khắc hành vượng (bị phản)
                # Tử: Cung hành bị hành vượng khắc
                if hanh_cung == lenh_hanh:
                    score += 10
                    details.append(f"├ ⑧ 🟢 {lenh_mua}: Cung {hanh_cung} = hành đang **VƯỢNG** theo mùa (+10)")
                elif SINH.get(lenh_hanh) == hanh_cung:  # Hành vượng sinh cung
                    score += 6
                    details.append(f"├ ⑧ 🔵 {lenh_mua}: Cung {hanh_cung} được {lenh_hanh} SINH → **TƯỚNG** (+6)")
                elif SINH.get(hanh_cung) == lenh_hanh:  # Cung sinh hành vượng → hao
                    score -= 3
                    details.append(f"├ ⑧ 🟡 {lenh_mua}: Cung {hanh_cung} sinh {lenh_hanh} → **HƯU** (hao lực) (-3)")
                elif KHAC.get(hanh_cung) == lenh_hanh:  # Cung khắc hành vượng → tù
                    score -= 5
                    details.append(f"├ ⑧ 🟠 {lenh_mua}: Cung {hanh_cung} khắc {lenh_hanh} → **TÙ** (lực phản) (-5)")
                elif KHAC.get(lenh_hanh) == hanh_cung:  # Hành vượng khắc cung → tử
                    score -= 8
                    details.append(f"├ ⑧ 🔴 {lenh_mua}: {lenh_hanh} KHẮC cung {hanh_cung} → **THẤT LỆNH** (-8)")
        except Exception:
            pass
        
        # ═══════ ⑨ NHẬT THẦN — Can Ngày tác động cung ═══════
        if can_ngay and hanh_cung and hanh_cung != '?':
            hanh_nhat = CAN_NGU_HANH.get(can_ngay, '')
            if hanh_nhat:
                if SINH.get(hanh_nhat) == hanh_cung:  # Nhật sinh Cung
                    score += 6
                    details.append(f"├ ⑨ ✅ Nhật Thần {can_ngay}({hanh_nhat}) SINH cung {hanh_cung} → được NGÀY hỗ trợ (+6)")
                elif KHAC.get(hanh_nhat) == hanh_cung:  # Nhật khắc Cung
                    score -= 6
                    details.append(f"├ ⑨ ⚠️ Nhật Thần {can_ngay}({hanh_nhat}) KHẮC cung {hanh_cung} → bị NGÀY phá (-6)")
                elif hanh_nhat == hanh_cung:
                    score += 3
                    details.append(f"├ ⑨ ✅ Nhật Thần {can_ngay}({hanh_nhat}) tỷ hòa với cung {hanh_cung} → ổn định (+3)")
                elif SINH.get(hanh_cung) == hanh_nhat:  # Cung sinh Nhật → hao
                    details.append(f"├ ⑨ ℹ️ Nhật Thần {can_ngay}({hanh_nhat}): cung {hanh_cung} sinh ngày → hao nhẹ")
        
        # ═══════ ⑩ TỨ TRỤ — Năm/Tháng/Ngày/Giờ Can tác động ═══════
        tu_tru_parts = []
        can_nam = chart_data.get('can_nam', '')
        can_thang = chart_data.get('can_thang', '')
        can_gio = chart_data.get('can_gio', '')
        chi_gio = chart_data.get('chi_gio', '')
        
        # Kiểm tra Tứ Trụ Can có sinh/khắc hành cung không (ngoài Can Ngày đã xét)
        tu_tru_cans = [
            ('Năm', can_nam), ('Tháng', can_thang), ('Giờ', can_gio)
        ]
        tu_tru_sinh = 0
        tu_tru_khac = 0
        for tru_label, tru_can in tu_tru_cans:
            if tru_can and hanh_cung and hanh_cung != '?':
                tru_hanh = CAN_NGU_HANH.get(tru_can, '')
                if tru_hanh:
                    if SINH.get(tru_hanh) == hanh_cung:  # Trụ sinh cung
                        tu_tru_sinh += 1
                        tu_tru_parts.append(f"Can {tru_label} {tru_can}({tru_hanh}) sinh cung")
                    elif KHAC.get(tru_hanh) == hanh_cung:  # Trụ khắc cung
                        tu_tru_khac += 1
                        tu_tru_parts.append(f"Can {tru_label} {tru_can}({tru_hanh}) khắc cung")
        
        if tu_tru_sinh > 0 or tu_tru_khac > 0:
            net = tu_tru_sinh - tu_tru_khac
            bonus = net * 3
            score += bonus
            if net > 0:
                details.append(f"├ ⑩ ✅ Tứ Trụ: {tu_tru_sinh} trụ SINH, {tu_tru_khac} trụ KHẮC → thuận ({'+' if bonus >= 0 else ''}{bonus})")
            elif net < 0:
                details.append(f"├ ⑩ ⚠️ Tứ Trụ: {tu_tru_sinh} trụ sinh, {tu_tru_khac} trụ KHẮC → bất lợi ({bonus})")
            else:
                details.append(f"├ ⑩ ℹ️ Tứ Trụ: {tu_tru_sinh} trụ sinh = {tu_tru_khac} trụ khắc → cân bằng")
            if tu_tru_parts and len(details) < 20:
                details.append(f"│  └ {', '.join(tu_tru_parts[:3])}")
        
        # ═══════ ⑪ CHI NGÀY / CHI GIỜ — Lục Xung với Chi Cung ═══════
        if cung_chi:
            xung_parts = []
            if chi_ngay and LUC_XUNG_CHI.get(chi_ngay) == cung_chi:
                score -= 5
                xung_parts.append(f"Chi ngày {chi_ngay} XUNG chi cung {cung_chi}")
            if chi_gio and LUC_XUNG_CHI.get(chi_gio) == cung_chi:
                score -= 4
                xung_parts.append(f"Chi giờ {chi_gio} XUNG chi cung {cung_chi}")
            # Lục Hợp
            if chi_ngay and LUC_HOP_CHI.get(chi_ngay) == cung_chi:
                score += 4
                xung_parts.append(f"Chi ngày {chi_ngay} HỢP chi cung {cung_chi}")
            
            if xung_parts:
                for xp in xung_parts:
                    if 'XUNG' in xp:
                        details.append(f"├ ⑪ ⚠️ {xp} → bị phá (-5)")
                    else:
                        details.append(f"├ ⑪ ✅ {xp} → ổn định (+4)")
        
        # ═══════ TỔNG KẾT CUNG ═══════
        score = max(-80, min(80, score))  # Clamp V15.1: wider for ngoai cung
        if score >= 25:
            strength = "🟢 VƯỢNG"
        elif score >= 10:
            strength = "🔵 TƯỚNG"
        elif score >= -5:
            strength = "🟡 HƯU"
        elif score >= -20:
            strength = "🟠 TÙ"
        else:
            strength = "🔴 TỬ"
        
        details.append(f"└ **TỔNG ĐIỂM CUNG: {score} → {strength}**")
        
        return score, details, strength
    
    # ===========================
    # V15.2: PHÂN TÍCH QUÁ KHỨ / HIỆN TẠI / TƯƠNG LAI
    # Dựa trên 3 tầng: Địa Bàn (Past), Nhân Bàn (Present), Thiên Bàn (Future)
    # ===========================
    def _analyze_timeline(self, cung_num, chart_data, question, role_label):
        """
        V15.2: Phân tích Quá Khứ / Hiện Tại / Tương Lai dựa trên 3 tầng cung.
        
        Theo Kỳ Môn cổ điển:
          - ĐỊA BÀN (Can Địa) = QUÁ KHỨ / GỐC RỄ — nền tảng, nguyên nhân sâu xa
          - NHÂN BÀN (Cửa)    = HIỆN TẠI / TRẠNG THÁI — hành động, con người, tình huống
          - THIÊN BÀN (Sao+Can) = TƯƠNG LAI / XU HƯỚNG — kết quả, diễn biến sắp tới
          - THẦN BÀN (Thần)    = LỰC ẨN — yếu tố vô hình chi phối
        
        Trả về: list of timeline details
        """
        if not cung_num or not chart_data or not isinstance(chart_data, dict):
            return []
        
        details = []
        hanh_cung = CUNG_NGU_HANH.get(cung_num, '?')
        quai_cung = QUAI_TUONG.get(cung_num, '?')
        thien_ban = chart_data.get('thien_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        than_ban = chart_data.get('than_ban', {})
        can_thien_ban = chart_data.get('can_thien_ban', {})
        dia_ban = chart_data.get('dia_ban', {})
        
        sao = str(thien_ban.get(cung_num, thien_ban.get(str(cung_num), '?')))
        cua = str(nhan_ban.get(cung_num, nhan_ban.get(str(cung_num), '?')))
        than = str(than_ban.get(cung_num, than_ban.get(str(cung_num), '?')))
        can_thien = str(can_thien_ban.get(cung_num, can_thien_ban.get(str(cung_num), '')))
        can_dia = str(dia_ban.get(cung_num, dia_ban.get(str(cung_num), '')))
        
        details.append(f"**{'🏠' if 'BẢN THÂN' in role_label else '🎯'} DIỄN BIẾN {role_label} — Cung {cung_num} ({quai_cung}):**")
        
        # ══════ QUÁ KHỨ / GỐC RỄ — Địa Bàn Can ══════
        qk_parts = []
        if can_dia:
            hanh_dia = CAN_NGU_HANH.get(can_dia, '?')
            can_tuong = CAN_CHI_TUONG_Y.get(can_dia, {})
            loai_tuong = can_tuong.get('loai_tuong', '')
            
            # Mối quan hệ Can Địa ↔ Hành Cung
            if hanh_dia and hanh_cung and hanh_dia != '?' and hanh_cung != '?':
                if hanh_dia == hanh_cung:
                    qk_parts.append("nền tảng vững chắc, gốc rễ hài hòa")
                elif SINH.get(hanh_dia) == hanh_cung:
                    qk_parts.append("gốc rễ hỗ trợ, nền tảng tốt sinh cung")
                elif KHAC.get(hanh_dia) == hanh_cung:
                    qk_parts.append("gốc rễ có mâu thuẫn, nền tảng khắc cung")
                elif SINH.get(hanh_cung) == hanh_dia:
                    qk_parts.append("cung phải nuôi dưỡng gốc rễ, hơi hao lực")
                elif KHAC.get(hanh_cung) == hanh_dia:
                    qk_parts.append("cung chế ngự gốc rễ, quá khứ bị kìm nén")
            
            if loai_tuong:
                qk_parts.append(f"tượng: {loai_tuong[:50]}")
        
        if qk_parts:
            details.append(f"├ ⏪ **QUÁ KHỨ** (Địa Bàn — {can_dia}/{CAN_NGU_HANH.get(can_dia, '?')}): {'; '.join(qk_parts)}")
        else:
            details.append(f"├ ⏪ **QUÁ KHỨ** (Địa Bàn): không đủ dữ liệu")
        
        # ══════ HIỆN TẠI / HÀNH ĐỘNG — Nhân Bàn Cửa ══════
        ht_parts = []
        cua_key = cua if 'Môn' in cua else cua + ' Môn'
        cua_data = CUA_KY_MON.get(cua, CUA_KY_MON.get(cua_key, {}))
        cua_hanh = cua_data.get('hanh', '')
        cua_yn = cua_data.get('y_nghia', '')
        cua_loai = cua_data.get('loai', '')
        
        if cua_yn:
            ht_parts.append(cua_yn[:50])
        
        # Cửa ↔ Cung relationship hiện tại
        if cua_hanh and hanh_cung and cua_hanh != '?' and hanh_cung != '?':
            if KHAC.get(cua_hanh) == hanh_cung:
                ht_parts.append("đang bị BỨC — cửa phá cung, tình huống căng thẳng")
            elif SINH.get(cua_hanh) == hanh_cung:
                ht_parts.append("đang được cửa sinh cung — thuận lợi, trôi chảy")
            elif cua_hanh == hanh_cung:
                ht_parts.append("hòa hợp — tình huống ổn định")
        
        # Cửa + Thần hiện tại → trạng thái cảm xúc
        than_data_tl = THAN_KY_MON.get(than, {})
        than_yn = than_data_tl.get('y_nghia', '')
        if than_yn:
            ht_parts.append(f"lực ẩn ({than}): {than_yn[:40]}")
        
        if ht_parts:
            details.append(f"├ ⏩ **HIỆN TẠI** (Nhân Bàn — {cua}/{cua_loai}): {'; '.join(ht_parts)}")
        else:
            details.append(f"├ ⏩ **HIỆN TẠI** (Nhân Bàn): không đủ dữ liệu")
        
        # ══════ TƯƠNG LAI / XU HƯỚNG — Thiên Bàn Sao + Can ══════
        tl_parts = []
        sao_data_tl = SAO_KY_MON.get(sao, {})
        sao_yn = sao_data_tl.get('y_nghia', '')
        sao_loai = sao_data_tl.get('loai', '')
        sao_hanh = sao_data_tl.get('hanh', '')
        
        if sao_yn:
            tl_parts.append(sao_yn[:50])
        
        # Can Thiên ↔ Hành Cung → xu hướng tương lai
        if can_thien:
            hanh_thien = CAN_NGU_HANH.get(can_thien, '?')
            if hanh_thien and hanh_cung and hanh_thien != '?' and hanh_cung != '?':
                if SINH.get(hanh_thien) == hanh_cung:
                    tl_parts.append("xu hướng thuận lợi — trời sinh cung")
                elif KHAC.get(hanh_thien) == hanh_cung:
                    tl_parts.append("xu hướng bất lợi — trời khắc cung")
                elif hanh_thien == hanh_cung:
                    tl_parts.append("xu hướng ổn định — trời hòa cung")
            
            can_thien_tuong = CAN_CHI_TUONG_Y.get(can_thien, {})
            tuong_tl = can_thien_tuong.get('loai_tuong', '')
            if tuong_tl:
                tl_parts.append(f"tượng: {tuong_tl[:40]}")
        
        # 81 Cách Cục → kết quả cuối cùng
        if can_thien and can_dia:
            cach_key = f"{can_thien}+{can_dia}"
            cach_data = THAP_CAN_KHAC_UNG.get(cach_key, {})
            if cach_data:
                tl_parts.append(f"Cách {cach_data.get('ten', '?')} → {cach_data.get('luan', '')[:40]}")
        
        if tl_parts:
            details.append(f"├ ⏭️ **TƯƠNG LAI** (Thiên Bàn — {sao}/{sao_loai} + {can_thien}): {'; '.join(tl_parts)}")
        else:
            details.append(f"├ ⏭️ **TƯƠNG LAI** (Thiên Bàn): không đủ dữ liệu")
        
        # ══════ TỔNG HỢP DÒNG THỜI GIAN ══════
        # So sánh quá khứ → hiện tại → tương lai trends
        trend_score = 0
        # Đánh giá Quá Khứ (Can Địa)
        if can_dia:
            hd = CAN_NGU_HANH.get(can_dia, '')
            if hd and hanh_cung:
                if hd == hanh_cung or SINH.get(hd) == hanh_cung:
                    trend_score += 1  # Past good
                elif KHAC.get(hd) == hanh_cung:
                    trend_score -= 1  # Past bad
        # Đánh giá Hiện Tại (Cửa)
        if cua_loai:
            if 'CÁT' in cua_loai and 'HUNG' not in cua_loai:
                trend_score += 1  # Present good
            elif 'HUNG' in cua_loai:
                trend_score -= 1  # Present bad
        # Đánh giá Tương Lai (Sao)
        if sao_loai:
            if 'CÁT' in sao_loai and 'HUNG' not in sao_loai:
                trend_score += 1  # Future good
            elif 'HUNG' in sao_loai:
                trend_score -= 1  # Future bad
        
        # Tạo narrative
        if trend_score >= 2:
            details.append(f"└ 📈 **XU HƯỚNG: TIẾN TRIỂN TỐT** — Quá khứ → Hiện tại → Tương lai đều thuận")
        elif trend_score <= -2:
            details.append(f"└ 📉 **XU HƯỚNG: SUY GIẢM** — Nhiều yếu tố bất lợi xuyên suốt")
        elif trend_score == 1:
            details.append(f"└ 📊 **XU HƯỚNG: KHỞI SẮC** — Có yếu tố tích cực, cần nỗ lực thêm")
        elif trend_score == -1:
            details.append(f"└ 📊 **XU HƯỚNG: BIẾN ĐỘNG** — Có trở ngại, cần cẩn thận")
        else:
            details.append(f"└ 📊 **XU HƯỚNG: CÂN BẰNG** — Tình hình trung tính, chờ thêm biến số")
        
        return details
    
    # ===========================
    # V15.3: ỨNG KỲ — DỰ ĐOÁN THỜI GIAN SỰ VIỆC XẢY RA
    # ===========================
    # Chi → Giờ tương ứng
    CHI_GIO_MAP = {
        'Tý': '23h-1h', 'Sửu': '1h-3h', 'Dần': '3h-5h', 'Mão': '5h-7h',
        'Thìn': '7h-9h', 'Tị': '9h-11h', 'Ngọ': '11h-13h', 'Mùi': '13h-15h',
        'Thân': '15h-17h', 'Dậu': '17h-19h', 'Tuất': '19h-21h', 'Hợi': '21h-23h',
    }
    # Chi → Tháng âm lịch
    CHI_THANG_MAP = {
        'Dần': 'tháng 1', 'Mão': 'tháng 2', 'Thìn': 'tháng 3', 'Tị': 'tháng 4',
        'Ngọ': 'tháng 5', 'Mùi': 'tháng 6', 'Thân': 'tháng 7', 'Dậu': 'tháng 8',
        'Tuất': 'tháng 9', 'Hợi': 'tháng 10', 'Tý': 'tháng 11', 'Sửu': 'tháng 12',
    }
    # Cửa → tốc độ sự việc
    CUA_SPEED = {
        'Khai Môn': ('NHANH', 'Cửa mở ra — sự việc khởi động nhanh'),
        'Hưu Môn': ('CHẬM', 'Cửa nghỉ — sự việc từ từ, chờ thời'),
        'Sinh Môn': ('TRUNG BÌNH', 'Cửa sinh — sự việc phát triển dần, có kết quả'),
        'Thương Môn': ('NHANH nhưng bất ngờ', 'Cửa tổn thương — sự việc xảy ra đột ngột'),
        'Đỗ Môn': ('RẤT CHẬM', 'Cửa bế — sự việc bị tắc, cần chờ đợi lâu'),
        'Cảnh Môn': ('TRUNG BÌNH', 'Cửa cảnh — sự việc cần xem xét, không vội'),
        'Tử Môn': ('CHẬM/KHÔNG XẢY RA', 'Cửa tử — sự việc khó thành hoặc kết thúc'),
        'Kinh Môn': ('NHANH nhưng bất an', 'Cửa kinh — sự việc xảy ra gấp gáp, gây lo lắng'),
    }
    # Sao → tác động tốc độ
    SAO_SPEED = {
        'Thiên Xung': ('NHANH', 'Sao xung — hành động mạnh, nhanh, quyết đoán'),
        'Thiên Bồng': ('NHANH nhưng bí mật', 'Sao bồng — mưu kế nhanh, ẩn giấu'),
        'Thiên Nhậm': ('CHẬM MÀ CHẮC', 'Sao nhậm — nhẫn nại, từ từ nhưng bền vững'),
        'Thiên Tâm': ('NHANH VÀ CHUẨN', 'Sao tâm — trí tuệ, mưu lược, đạt nhanh'),
        'Thiên Phụ': ('TRUNG BÌNH', 'Sao phụ — cần văn thư, giấy tờ, không vội'),
        'Thiên Nhuế': ('RẤT CHẬM', 'Sao nhuế — bệnh tật, trì trệ, cần kiên nhẫn'),
        'Thiên Trụ': ('CHẬM/PHÁ', 'Sao trụ — phá hoại, gián đoạn, khó tiến'),
        'Thiên Anh': ('TRUNG BÌNH', 'Sao anh — sáng suốt nhưng không nhanh'),
        'Thiên Cầm': ('TÙY CẢNH', 'Sao cầm — trung tâm, tùy Cửa+Thần đi kèm'),
    }
    
    def _analyze_timing(self, cung_dt, chart_data, question, dung_than, cung_score=0):
        """
        V15.3: Dự đoán THỜI GIAN sự việc xảy ra (Ứng Kỳ).
        
        Phân tích:
        1. Tốc độ (nhanh/chậm) dựa trên Cửa + Sao
        2. Ứng kỳ: Chi xung/sinh/hợp DT → giờ/ngày/tháng/năm
        3. Tuần Không → chờ xuất Không
        
        Trả về: list of timing details
        """
        if not cung_dt or not chart_data or not isinstance(chart_data, dict):
            return []
        
        details = []
        details.append(f"**⏰ ỨNG KỲ — DỰ ĐOÁN THỜI GIAN SỰ VIỆC ({dung_than}):**")
        
        thien_ban = chart_data.get('thien_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        
        sao = str(thien_ban.get(cung_dt, thien_ban.get(str(cung_dt), '?')))
        cua = str(nhan_ban.get(cung_dt, nhan_ban.get(str(cung_dt), '?')))
        
        # ═══════ 1. TỐC ĐỘ SỰ VIỆC ═══════
        cua_key = cua if 'Môn' in cua else cua + ' Môn'
        cua_speed_data = self.CUA_SPEED.get(cua_key, self.CUA_SPEED.get(cua, None))
        sao_speed_data = self.SAO_SPEED.get(sao, None)
        
        speed_label = 'TRUNG BÌNH'
        if cua_speed_data:
            speed_label = cua_speed_data[0]
            details.append(f"├ 🚀 Tốc độ (Cửa {cua}): **{cua_speed_data[0]}** — {cua_speed_data[1]}")
        if sao_speed_data:
            details.append(f"├ 🚀 Tốc độ (Sao {sao}): **{sao_speed_data[0]}** — {sao_speed_data[1]}")
        
        # Dịch Mã tăng tốc
        chi_ngay = chart_data.get('chi_ngay', '')
        cung_chi = self.CUNG_CHI_MAP.get(cung_dt)
        dich_ma = DICH_MA_MAP.get(chi_ngay, '')
        if cung_chi and dich_ma and cung_chi == dich_ma:
            details.append(f"├ 🐎 **DỊCH MÃ** lâm cung → sự việc xảy ra **NHANH HƠN**, có di chuyển")
        
        # ═══════ 2. ỨNG KỲ — NGÀY/THÁNG/NĂM XẢY RA ═══════
        hanh_cung = CUNG_NGU_HANH.get(cung_dt, '?')
        can_ngay = chart_data.get('can_ngay', '')
        
        # Tìm Chi XUNG và Chi SINH cho cung
        chi_xung_cung = LUC_XUNG_CHI.get(cung_chi, '') if cung_chi else ''
        chi_hop_cung = LUC_HOP_CHI.get(cung_chi, '') if cung_chi else ''
        
        # Tìm Chi mà hành của nó SINH hành cung
        chi_sinh_cung = []
        for chi, hanh in CHI_NGU_HANH.items():
            if SINH.get(hanh) == hanh_cung:
                chi_sinh_cung.append(chi)
        
        # Tuần Không check
        khong_vong = _get_khong_vong(can_ngay, chi_ngay)
        is_khong_vong = cung_chi and khong_vong and cung_chi in khong_vong
        
        # Quy tắc ứng kỳ theo vượng/suy
        if cung_score >= 10:  # DT Vượng
            details.append(f"├ 📅 DT **VƯỢNG** → ứng vào ngày/tháng **XUNG** (phát động)")
            if chi_xung_cung:
                gio = self.CHI_GIO_MAP.get(chi_xung_cung, '?')
                thang = self.CHI_THANG_MAP.get(chi_xung_cung, '?')
                details.append(f"│  └ Chi xung = **{chi_xung_cung}** → giờ {gio}, {thang}")
        elif cung_score <= -10:  # DT Suy
            details.append(f"├ 📅 DT **SUY** → ứng vào ngày/tháng **SINH** hoặc **HỢP** (cần hỗ trợ)")
            if chi_sinh_cung:
                chi_s = chi_sinh_cung[0]
                gio = self.CHI_GIO_MAP.get(chi_s, '?')
                thang = self.CHI_THANG_MAP.get(chi_s, '?')
                details.append(f"│  └ Chi sinh cung = **{chi_s}** → giờ {gio}, {thang}")
            if chi_hop_cung:
                gio = self.CHI_GIO_MAP.get(chi_hop_cung, '?')
                thang = self.CHI_THANG_MAP.get(chi_hop_cung, '?')
                details.append(f"│  └ Chi hợp = **{chi_hop_cung}** → giờ {gio}, {thang}")
        else:  # Bình thường
            details.append(f"├ 📅 DT **BÌNH** → ứng vào ngày/tháng Chi tương ứng cung")
            if cung_chi:
                gio = self.CHI_GIO_MAP.get(cung_chi, '?')
                thang = self.CHI_THANG_MAP.get(cung_chi, '?')
                details.append(f"│  └ Chi cung = **{cung_chi}** → giờ {gio}, {thang}")
        
        # ═══════ 3. TUẦN KHÔNG → CHẬM TRỄ ═══════
        if is_khong_vong:
            details.append(f"├ ⏳ 🔴 DT lâm **TUẦN KHÔNG** → sự việc **CHƯA XẢY RA**, chờ xuất Không")
            # Xuất Không = khi chi ngày/giờ trùng hoặc xung chi Tuần Không
            if cung_chi:
                details.append(f"│  └ Chờ đến ngày/giờ Chi **{cung_chi}** hoặc xung {cung_chi} mới ứng")
        
        # ═══════ 4. TỔNG KẾT TỐC ĐỘ ═══════
        # Xét combo Cửa + Sao + Dịch Mã + Tuần Không
        speed_score = 0
        if cua_speed_data:
            s = cua_speed_data[0]
            if 'NHANH' in s and 'CHẬM' not in s:
                speed_score += 2
            elif 'CHẬM' in s:
                speed_score -= 2
        if sao_speed_data:
            s = sao_speed_data[0]
            if 'NHANH' in s:
                speed_score += 1
            elif 'CHẬM' in s:
                speed_score -= 1
        if cung_chi and dich_ma == cung_chi:
            speed_score += 2  # Dịch Mã tăng tốc
        if is_khong_vong:
            speed_score -= 3  # Tuần Không → chậm rất nhiều
        
        if speed_score >= 3:
            details.append(f"└ ⚡ **TỔNG KẾT: SỰ VIỆC XẢY RA RẤT NHANH** — nhiều yếu tố thúc đẩy")
        elif speed_score >= 1:
            details.append(f"└ 🏃 **TỔNG KẾT: SỰ VIỆC XẢY RA NHANH** — có động lực")
        elif speed_score >= -1:
            details.append(f"└ 🚶 **TỔNG KẾT: SỰ VIỆC BÌNH THƯỜNG** — không nhanh không chậm")
        elif speed_score >= -2:
            details.append(f"└ 🐢 **TỔNG KẾT: SỰ VIỆC CHẬM TRỄ** — cần kiên nhẫn chờ đợi")
        else:
            details.append(f"└ ⏳ **TỔNG KẾT: SỰ VIỆC RẤT CHẬM / CHƯA XẢY RA** — nhiều cản trở")
        
        return details
    
    # ═══════════════════════════════════════════════════════════
    # V38.2: PROTOCOL 27 BƯỚC — LOGIC LIỀN MẠCH
    # Câu hỏi → Dụng Thần → Sơ Đồ → 27 Bước → Kết Luận
    # Mỗi bước TỰ ĐỌC data thô, LUẬN GIẢI, rồi GOM kết quả
    # ═══════════════════════════════════════════════════════════
    
    def _apply_27step_protocol(self, question, dung_than, hanh_dt,
                                km_factors, lh_factors, mh_factors,
                                km_score, lh_score, mh_score,
                                tb_factors, ln_factors, ta_factors,
                                tb_score, ln_score, ta_score,
                                weighted_pct, chart_data=None,
                                luc_hao_data=None, mai_hoa_data=None):
        """V38.2: Protocol 27 bước — logic liền mạch, không tách rời.
        
        MỖI BƯỚC: Đọc data thô → Luận giải → Kết quả → Chuyển sang bước tiếp
        KẾT LUẬN: Dựa trên CHUỖI bằng chứng từ 27 bước
        """
        import re
        lines = []
        evidence_chain = []  # Chuỗi bằng chứng tích lũy qua 27 bước
        accumulated_score = 0  # Điểm tích lũy qua từng bước
        
        def _escore(f):
            """Trích điểm từ factor text"""
            m = re.search(r'([+-]\d+)\s*$', f)
            return int(m.group(1)) if m else 0
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # BƯỚC 0: CÂU HỎI → DỤNG THẦN (Khởi đầu chuỗi logic)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("## 🔮 PROTOCOL 27 BƯỚC — LUẬN GIẢI THỐNG NHẤT V42.9")
        lines.append("")
        lines.append("### BƯỚC 0: CÂU HỎI → DỤNG THẦN")
        lines.append(f"- **Câu hỏi:** {question}")
        lines.append(f"- **Dụng Thần (DT):** {dung_than} — Hành: **{hanh_dt}**")
        
        # Xác định raw data
        cd = chart_data if isinstance(chart_data, dict) else {}
        lh = luc_hao_data if isinstance(luc_hao_data, dict) else {}
        mh = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
        
        can_ngay = cd.get('can_ngay', '?')
        chi_ngay = cd.get('chi_ngay', '?')
        can_gio = cd.get('can_gio', '?')
        chi_thang = lh.get('chi_thang', '') or cd.get('chi_thang', '?')
        
        lines.append(f"- **Thời gian:** Can Ngày={can_ngay}, Chi Ngày={chi_ngay}, Chi Tháng={chi_thang}")
        lines.append(f"- **→ Mọi phân tích dưới đây XEM XÉT {dung_than}({hanh_dt}) là trung tâm**")
        lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # SƠ ĐỒ YẾU TỐ — Data thô từ 3 phương pháp chính
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("### 📐 SƠ ĐỒ: DỮ LIỆU THÔ → DỤNG THẦN LÀ TRUNG TÂM")
        lines.append("```")
        
        # KM raw data
        thien_ban = cd.get('thien_ban', {})
        nhan_ban = cd.get('nhan_ban', {})
        than_ban = cd.get('than_ban', {})
        can_tb = cd.get('can_thien_ban', {})
        
        # Tìm cung BT/DT
        bt_cung = sv_cung = None
        for cn, cv in can_tb.items():
            if cv == can_ngay: bt_cung = int(cn) if cn else None
            if cv == can_gio: sv_cung = int(cn) if cn else None
        if not bt_cung and can_ngay == 'Giáp':
            for cn, cv in can_tb.items():
                if cv == 'Mậu': bt_cung = int(cn) if cn else None; break
        
        bt_sao = str(thien_ban.get(bt_cung, thien_ban.get(str(bt_cung), '?'))) if bt_cung else '?'
        bt_cua = str(nhan_ban.get(bt_cung, nhan_ban.get(str(bt_cung), '?'))) if bt_cung else '?'
        bt_than = str(than_ban.get(bt_cung, than_ban.get(str(bt_cung), '?'))) if bt_cung else '?'
        sv_sao = str(thien_ban.get(sv_cung, thien_ban.get(str(sv_cung), '?'))) if sv_cung else '?'
        sv_cua = str(nhan_ban.get(sv_cung, nhan_ban.get(str(sv_cung), '?'))) if sv_cung else '?'
        
        # LH raw data
        ban_lh = lh.get('ban', {})
        haos = ban_lh.get('haos', ban_lh.get('details', lh.get('haos', [])))
        dt_hao_pos = '?'
        dt_chi_val = '?'
        dt_hanh_val = '?'
        dt_vuong_val = '?'
        if haos and isinstance(haos, list):
            for i, hao in enumerate(haos):
                lt = hao.get('luc_than', '')
                tu = str(hao.get('the_ung', '') or hao.get('marker', ''))
                if lt == dung_than or (dung_than == 'Bản Thân' and 'Thế' in tu):
                    dt_hao_pos = ['Sơ','Nhị','Tam','Tứ','Ngũ','Thượng'][i] if i < 6 else str(i+1)
                    dt_chi_val = hao.get('chi', '') or (hao.get('can_chi','').split('-')[0] if hao.get('can_chi') else '?')
                    dt_hanh_val = hao.get('ngu_hanh', '') or hao.get('hanh', '?')
                    dt_vuong_val = str(hao.get('vuong_suy', '') or hao.get('strength', '') or '?')
                    break
        
        # MH raw data
        mh_ten = mh.get('ten', mh.get('ten_que', '?'))
        mh_thuong = mh.get('ten_thuong', mh.get('thuong_quai', '?'))
        mh_ha = mh.get('ten_ha', mh.get('ha_quai', '?'))
        mh_hanh_t = mh.get('hanh_thuong', '?')
        mh_hanh_h = mh.get('hanh_ha', '?')
        
        lines.append(f"┌─────────────────── CÂU HỎI: {question[:40]}{'...' if len(question)>40 else ''}")
        lines.append(f"│")
        lines.append(f"├─→ DỤNG THẦN: {dung_than} ({hanh_dt})")
        lines.append(f"│")
        lines.append(f"├─── KỲ MÔN ─────────────────────────────────────")
        lines.append(f"│    BT: Cung {bt_cung or '?'} | Sao={bt_sao} | Cửa={bt_cua} | Thần={bt_than}")
        lines.append(f"│    SV: Cung {sv_cung or '?'} | Sao={sv_sao} | Cửa={sv_cua}")
        lines.append(f"│")
        lines.append(f"├─── LỤC HÀO ────────────────────────────────────")
        lines.append(f"│    DT tại Hào {dt_hao_pos} | Chi={dt_chi_val} | Hành={dt_hanh_val}")
        lines.append(f"│    Trạng thái: {dt_vuong_val}")
        lines.append(f"│    Nguyệt Lệnh: {chi_thang} | Nhật Thần: {can_ngay}")
        lines.append(f"│")
        lines.append(f"├─── MAI HOA ─────────────────────────────────────")
        lines.append(f"│    Quẻ: {mh_ten} | Thượng={mh_thuong}({mh_hanh_t}) | Hạ={mh_ha}({mh_hanh_h})")
        lines.append(f"│")
        lines.append(f"└─── Ngũ Hành: {hanh_dt} ← Sinh/Khắc ← Mọi yếu tố")
        lines.append("```")
        lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PHẦN I: LỤC HÀO — 12 BƯỚC (Mỗi bước tự đọc + luận)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("---")
        lines.append("### 📜 I. LỤC HÀO — 12 BƯỚC LUẬN GIẢI")
        lines.append("")
        
        lh_step_defs = [
            ('LH-B1', 'DT Vượng/Suy', ['DT Vượng','DT Tướng','DT Suy','DT Tử','DT Bệnh','DT Mộ','DT Trường','DT Đế','DT ẩn','Phục Thần']),
            ('LH-B2', 'Nguyệt Lệnh → DT', ['Nguyệt']),
            ('LH-B3', 'Nhật Thần → DT', ['Nhật(','Nhật Xung','ÁM ĐỘNG']),
            ('LH-B4', 'Nguyên Thần (sinh DT)', ['NT(','Nguyên Thần']),
            ('LH-B5', 'Kỵ Thần (khắc DT)', ['KT(','Kỵ Thần']),
            ('LH-B6', 'Cừu Thần + Tham Sinh', ['Cừu Thần','THAM SINH','mất nguồn','chain']),
            ('LH-B7', 'DT Động/Tĩnh + Tiến/Thối', ['DT ĐỘNG','DT TĨNH','TIẾN THẦN','THỐI THẦN','Hóa Hồi','Hóa Phục']),
            ('LH-B8', 'Tuần Không + Nguyệt Phá', ['Tuần Không','NGUYỆT PHÁ']),
            ('LH-B9', 'Phản/Phục Ngâm + Hóa Tuyệt/Mộ', ['PHẢN NGÂM','PHỤC NGÂM','Hóa TUYỆT','Hóa MỘ']),
            ('LH-B10', 'Thế vs Ứng + DT Trì Thế', ['Thế khắc','Ứng khắc','TRÌ THẾ']),
            ('LH-B11', 'Tam Hợp/Lục Xung/Hào Động khác', ['Tam Hợp','xung DT','hợp DT','Hào động','hào','Lục Hợp']),
        ]
        
        lh_used = set()
        lh_running_total = 0
        
        for step_id, step_name, keywords in lh_step_defs:
            matched = []
            for f in lh_factors:
                if f in lh_used:
                    continue
                for kw in keywords:
                    if kw.lower() in f.lower():
                        matched.append(f)
                        lh_used.add(f)
                        break
            
            step_score = sum(_escore(m) for m in matched)
            lh_running_total += step_score
            
            if matched:
                icon = '✅' if step_score > 0 else ('🔴' if step_score < 0 else '🟡')
                evidence_chain.append((step_id, step_name, step_score, matched[0]))
                lines.append(f"**{step_id}. {step_name}** {icon} ({step_score:+d})")
                for m in matched:
                    lines.append(f"  → {m}")
                lines.append(f"  *Tích lũy sau {step_id}: {lh_running_total:+d}*")
                lines.append("")
            # Bỏ qua bước không có data — không in "(không phát hiện)"
        
        # Các factor LH chưa phân loại
        remaining_lh = [f for f in lh_factors if f not in lh_used]
        if remaining_lh:
            rem_score = sum(_escore(f) for f in remaining_lh)
            lh_running_total += rem_score
            lines.append(f"**LH-Bổ sung** ({len(remaining_lh)} yếu tố, {rem_score:+d})")
            for f in remaining_lh[:4]:
                lines.append(f"  → {f}")
            if len(remaining_lh) > 4:
                lines.append(f"  → (+{len(remaining_lh)-4} yếu tố khác)")
            lines.append("")
        
        # LH Tổng kết
        lh_verdict = 'CÁT' if lh_score >= 5 else ('HUNG' if lh_score <= -5 else 'BÌNH')
        lh_icon = '✅' if lh_score >= 5 else ('🔴' if lh_score <= -5 else '🟡')
        lines.append(f"**LH-B12. ⚖️ TỔNG KẾT LỤC HÀO: {lh_icon} {lh_verdict} (Σ={lh_score:+d}, {len(lh_factors)} yếu tố)**")
        evidence_chain.append(('LH-B12', 'TỔNG KẾT LH', lh_score, lh_verdict))
        lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PHẦN II: KỲ MÔN — 9 BƯỚC
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("---")
        lines.append("### ⚔️ II. KỲ MÔN ĐỘN GIÁP — 9 BƯỚC LUẬN GIẢI")
        lines.append("")
        
        km_step_defs = [
            ('KM-B1', 'Sinh Khắc Cung BT↔DT', ['Cung DT','Cung BT','tương sinh','Tỷ hòa']),
            ('KM-B2', 'Sao tại Cung DT', ['Sao']),
            ('KM-B3', 'Cửa tại Cung DT', ['Cửa']),
            ('KM-B4', 'Thần tại Cung DT', ['Thần']),
            ('KM-B5', 'Can DT Vượng/Suy tại Cung', ['Can DT']),
            ('KM-B6', 'Tuần Không + Mã Tinh', ['Không Vong','Mã Tinh']),
            ('KM-B7', 'Cách Cục Đặc Biệt + Phản/Phục', ['Tam Kỳ','Ngọc Nữ','Thanh Long','Cách cục','Phản','Phục','Thiên Cầm']),
            ('KM-B8', 'Nguyệt lệnh + Tương tác Sao×Cửa', ['Nguyệt','Tương tác','Sao-Cửa','Bát Thần']),
        ]
        
        km_used = set()
        km_running_total = 0
        
        for step_id, step_name, keywords in km_step_defs:
            matched = []
            for f in km_factors:
                if f in km_used:
                    continue
                for kw in keywords:
                    if kw.lower() in f.lower():
                        matched.append(f)
                        km_used.add(f)
                        break
            
            step_score = sum(_escore(m) for m in matched)
            km_running_total += step_score
            
            if matched:
                icon = '✅' if step_score > 0 else ('🔴' if step_score < 0 else '🟡')
                evidence_chain.append((step_id, step_name, step_score, matched[0]))
                lines.append(f"**{step_id}. {step_name}** {icon} ({step_score:+d})")
                for m in matched:
                    lines.append(f"  → {m}")
                lines.append(f"  *Tích lũy sau {step_id}: {km_running_total:+d}*")
                lines.append("")
        
        remaining_km = [f for f in km_factors if f not in km_used]
        if remaining_km:
            rem_score = sum(_escore(f) for f in remaining_km)
            km_running_total += rem_score
            lines.append(f"**KM-Bổ sung** ({len(remaining_km)} yếu tố, {rem_score:+d})")
            for f in remaining_km[:3]:
                lines.append(f"  → {f}")
            lines.append("")
        
        km_verdict = 'CÁT' if km_score >= 3 else ('HUNG' if km_score <= -3 else 'BÌNH')
        km_icon = '✅' if km_score >= 3 else ('🔴' if km_score <= -3 else '🟡')
        lines.append(f"**KM-B9. ⚖️ TỔNG KẾT KỲ MÔN: {km_icon} {km_verdict} (Σ={km_score:+d}, {len(km_factors)} yếu tố)**")
        evidence_chain.append(('KM-B9', 'TỔNG KẾT KM', km_score, km_verdict))
        lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PHẦN III: MAI HOA — 6 BƯỚC
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("---")
        lines.append("### 🌸 III. MAI HOA DỊCH SỐ — 6 BƯỚC LUẬN GIẢI")
        lines.append("")
        
        mh_step_defs = [
            ('MH-B1', 'Thể↔Dụng sinh khắc', ['Dụng sinh','Dụng khắc','Thể khắc','Thể sinh','Tỷ Hòa']),
            ('MH-B2', 'Hỗ Quái → Thể', ['Hỗ']),
            ('MH-B3', 'Biến Quái → Thể', ['Biến']),
            ('MH-B4', 'Nguyệt Lệnh + Nhật Thần', ['lệnh','Tháng','Ngày','vượng tại']),
            ('MH-B5', 'Quái Tượng 64 Quẻ', ['Quẻ','KINH','IChing']),
        ]
        
        mh_used = set()
        mh_running_total = 0
        
        for step_id, step_name, keywords in mh_step_defs:
            matched = []
            for f in mh_factors:
                if f in mh_used:
                    continue
                for kw in keywords:
                    if kw.lower() in f.lower():
                        matched.append(f)
                        mh_used.add(f)
                        break
            
            step_score = sum(_escore(m) for m in matched)
            mh_running_total += step_score
            
            if matched:
                icon = '✅' if step_score > 0 else ('🔴' if step_score < 0 else '🟡')
                evidence_chain.append((step_id, step_name, step_score, matched[0]))
                lines.append(f"**{step_id}. {step_name}** {icon} ({step_score:+d})")
                for m in matched:
                    lines.append(f"  → {m}")
                lines.append(f"  *Tích lũy sau {step_id}: {mh_running_total:+d}*")
                lines.append("")
        
        remaining_mh = [f for f in mh_factors if f not in mh_used]
        if remaining_mh:
            rem_score = sum(_escore(f) for f in remaining_mh)
            lines.append(f"**MH-Bổ sung** ({len(remaining_mh)}, {rem_score:+d}): {'; '.join(remaining_mh[:2])}")
            lines.append("")
        
        mh_verdict = 'CÁT' if mh_score >= 3 else ('HUNG' if mh_score <= -3 else 'BÌNH')
        mh_icon = '✅' if mh_score >= 3 else ('🔴' if mh_score <= -3 else '🟡')
        lines.append(f"**MH-B6. ⚖️ TỔNG KẾT MAI HOA: {mh_icon} {mh_verdict} (Σ={mh_score:+d}, {len(mh_factors)} yếu tố)**")
        evidence_chain.append(('MH-B6', 'TỔNG KẾT MH', mh_score, mh_verdict))
        lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PHẦN IV: TỔNG HỢP 6PP + CHUỖI BẰNG CHỨNG
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("---")
        lines.append("### 🏆 IV. TỔNG HỢP + CHUỖI BẰNG CHỨNG")
        lines.append("")
        
        tb_verdict = 'CÁT' if tb_score >= 3 else ('HUNG' if tb_score <= -3 else 'BÌNH')
        ln_verdict = 'CÁT' if ln_score >= 3 else ('HUNG' if ln_score <= -3 else 'BÌNH')
        ta_verdict_s = 'CÁT' if ta_score >= 3 else ('HUNG' if ta_score <= -3 else 'BÌNH')
        total_factors = len(lh_factors)+len(km_factors)+len(mh_factors)+len(tb_factors)+len(ln_factors)+len(ta_factors)
        
        lines.append("| PP | Verdict | Σ Điểm | Yếu tố |")
        lines.append("|:---|:--------|-------:|-------:|")
        lines.append(f"| 📜 Lục Hào | **{lh_verdict}** | {lh_score:+d} | {len(lh_factors)} |")
        lines.append(f"| ⚔️ Kỳ Môn | **{km_verdict}** | {km_score:+d} | {len(km_factors)} |")
        lines.append(f"| 🌸 Mai Hoa | **{mh_verdict}** | {mh_score:+d} | {len(mh_factors)} |")
        lines.append(f"| 📕 Thiết Bản | **{tb_verdict}** | {tb_score:+d} | {len(tb_factors)} |")
        lines.append(f"| 🔯 Lục Nhâm | **{ln_verdict}** | {ln_score:+d} | {len(ln_factors)} |")
        lines.append(f"| ⭐ Thái Ất | **{ta_verdict_s}** | {ta_score:+d} | {len(ta_factors)} |")
        lines.append(f"| **TỔNG** | **{weighted_pct}%** | | **{total_factors}** |")
        lines.append("")
        
        # Chuỗi bằng chứng — chỉ các bước có tác động mạnh
        strong_evidence = [e for e in evidence_chain if abs(e[2]) >= 5]
        if strong_evidence:
            lines.append("**🔗 CHUỖI BẰNG CHỨNG (các bước tác động mạnh):**")
            for step_id, step_name, sc, detail in strong_evidence:
                icon = '✅' if sc > 0 else '🔴'
                lines.append(f"  {icon} {step_id} ({step_name}): {sc:+d} — {detail[:60]}")
            lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PHẦN V: KẾT LUẬN — DỰA TRÊN CHUỖI BẰNG CHỨNG
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        all_verdicts = [lh_verdict, km_verdict, mh_verdict, tb_verdict, ln_verdict, ta_verdict_s]
        cat_count = sum(1 for v in all_verdicts if v == 'CÁT')
        hung_count = sum(1 for v in all_verdicts if v == 'HUNG')
        
        if weighted_pct >= 70:
            final_verdict = 'ĐẠI CÁT'
            final_icon = '🟢'
        elif weighted_pct >= 55:
            final_verdict = 'CÁT — THUẬN LỢI'
            final_icon = '✅'
        elif weighted_pct >= 45:
            final_verdict = 'BÌNH — CÓ THỂ' if weighted_pct >= 50 else 'BÌNH — CẦN CÂN NHẮC'
            final_icon = '🟡'
        elif weighted_pct >= 30:
            final_verdict = 'HUNG — KHÓ KHĂN'
            final_icon = '🔴'
        else:
            final_verdict = 'ĐẠI HUNG'
            final_icon = '⛔'
        
        # Override nếu evidence mâu thuẫn với %
        if hung_count >= 4 and weighted_pct >= 50:
            final_verdict = 'HUNG — ĐA SỐ PP BẤT LỢI'
            final_icon = '🔴'
            weighted_pct = min(weighted_pct, 42)
        elif cat_count >= 4 and weighted_pct < 50:
            final_verdict = 'CÁT — ĐA SỐ PP THUẬN'
            final_icon = '✅'
            weighted_pct = max(weighted_pct, 55)
        
        lines.append("---")
        lines.append(f"### {final_icon} V. KẾT LUẬN CHÍNH THỨC (từ 27 bước + {total_factors} yếu tố)")
        lines.append("")
        lines.append(f"**{final_icon} VERDICT: {final_verdict} ({weighted_pct}%)**")
        lines.append(f"**Đồng thuận 6PP:** {cat_count} CÁT — {hung_count} HUNG — {6-cat_count-hung_count} BÌNH")
        lines.append("")
        
        # Narrative dựa trên evidence chain
        lines.append("**📝 LUẬN GIẢI:**")
        pos_evidence = [e for e in evidence_chain if e[2] > 0 and 'TỔNG' not in e[1]]
        neg_evidence = [e for e in evidence_chain if e[2] < 0 and 'TỔNG' not in e[1]]
        
        if pos_evidence:
            pos_text = ', '.join(f"{e[0]}({e[2]:+d})" for e in pos_evidence[:4])
            lines.append(f"- Thuận lợi từ: {pos_text}")
        if neg_evidence:
            neg_text = ', '.join(f"{e[0]}({e[2]:+d})" for e in neg_evidence[:4])
            lines.append(f"- Bất lợi từ: {neg_text}")
        
        net = sum(e[2] for e in evidence_chain if 'TỔNG' not in e[1])
        lines.append(f"- **Net Score:** {net:+d} → Xu hướng {'THUẬN' if net > 0 else ('NGHỊCH' if net < 0 else 'CÂN BẰNG')}")
        lines.append("")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # CÂU TRẢ LỜI KHẲNG ĐỊNH + VÌ SAO + ỨNG KỲ + GIẢI PHÁP
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        q_lower = question.lower()
        
        # 1. XÁC ĐỊNH CÂU TRẢ LỜI KHẲNG ĐỊNH
        # V41.0: Thêm branch COUNT/AGE — trả số cụ thể từ Ngũ Hành
        _HANH_SO_VERDICT = {
            'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 10)
        }
        
        if any(kw in q_lower for kw in ['bao nhiêu', 'mấy', 'số lượng', 'có mấy', 'bao nhieu', 'may ']):
            # Câu hỏi SỐ LƯỢNG → trả con số cụ thể
            _hd = _HANH_SO_VERDICT.get(hanh_dt, (5, 10))
            _so_chinh = _hd[0]  # Sinh số
            _so_phu = _hd[1]    # Thành số
            # Chọn số dựa trên Vượng/Suy
            if weighted_pct >= 60:
                _so_ket = _so_phu  # Vượng → dùng thành số (lớn hơn)
            elif weighted_pct >= 40:
                _so_ket = _so_chinh  # Bình → dùng sinh số
            else:
                _so_ket = max(1, _so_chinh - 1)  # Suy → giảm
            lines.append(f"> 📢 **CÂU TRẢ LỜI: SỐ LƯỢNG = {_so_ket}** (Hành {hanh_dt}: sinh số {_so_chinh}, thành số {_so_phu})")
            lines.append(f"> *Phạm vi: {_so_chinh} — {_so_phu} | DT {hanh_dt} {'VƯỢNG→lấy thành số' if weighted_pct >= 60 else 'BÌNH→lấy sinh số' if weighted_pct >= 40 else 'SUY→giảm'}*")
        elif any(kw in q_lower for kw in ['tuổi', 'bao nhiêu tuổi', 'mấy tuổi']):
            # Câu hỏi TUỔI → trả tuổi từ 12 Trường Sinh
            _ts_tuoi = TRUONG_SINH_POWER.get(ts_stage, {})
            _tuoi_min = _ts_tuoi.get('tuoi_min', '?')
            _tuoi_max = _ts_tuoi.get('tuoi_max', '?')
            lines.append(f"> 📢 **CÂU TRẢ LỜI: KHOẢNG {_tuoi_min}–{_tuoi_max} TUỔI** (Trường Sinh: {ts_stage})")
        elif any(kw in q_lower for kw in ['có nên', 'nên không', 'có được', 'được không']):
            if weighted_pct >= 55:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: CÓ — NÊN LÀM ({weighted_pct}%)**")
            elif weighted_pct >= 45:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: CÓ THỂ LÀM — nhưng phải THẬN TRỌNG ({weighted_pct}%)**")
            else:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: KHÔNG NÊN — BẤT LỢI ({weighted_pct}%)**")
        elif any(kw in q_lower for kw in ['sống', 'chết', 'mất', 'qua khỏi', 'qua được']):
            if weighted_pct >= 50:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: CÒN SỐNG / QUA ĐƯỢC ({weighted_pct}%)**")
            elif weighted_pct >= 40:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: CÒN SỐNG nhưng NGUY KỊCH ({weighted_pct}%)**")
            else:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: ĐÃ MẤT hoặc KHÔNG QUA ĐƯỢC ({weighted_pct}%)**")
        elif any(kw in q_lower for kw in ['có không', 'không', 'chưa', 'thắng', 'thua', 'đỗ', 'trượt']):
            if weighted_pct >= 55:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: CÓ — THÀNH CÔNG ({weighted_pct}%)**")
            elif weighted_pct >= 45:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: KHÓ THÀNH — cần đổi cách hoặc đợi ({weighted_pct}%)**")
            else:
                lines.append(f"> 📢 **CÂU TRẢ LỜI: KHÔNG — THẤT BẠI ({weighted_pct}%)**")
        else:
            if weighted_pct >= 55:
                lines.append(f"> 📢 **KẾT LUẬN: THUẬN LỢI ({weighted_pct}%)**")
            elif weighted_pct >= 45:
                lines.append(f"> 📢 **KẾT LUẬN: CÓ THỂ ĐƯỢC — nhưng CẦN THẬN TRỌNG ({weighted_pct}%)**")
            else:
                lines.append(f"> 📢 **KẾT LUẬN: KHÔNG THUẬN — nên hoãn hoặc đổi hướng ({weighted_pct}%)**")
        
        lines.append("")
        
        # 2. VÌ SAO — Trích dẫn bằng chứng CỤ THỂ từ evidence_chain
        lines.append("**📋 VÌ SAO:**")
        _top_pos = [e for e in evidence_chain if e[2] > 0 and 'TỔNG' not in e[1]][:3]
        _top_neg = [e for e in evidence_chain if e[2] < 0 and 'TỔNG' not in e[1]][:3]
        for i, (sid, sname, sc, detail) in enumerate(_top_pos, 1):
            lines.append(f"  ✅ {sid} ({sname}): {detail[:60]} ({sc:+d})")
        for i, (sid, sname, sc, detail) in enumerate(_top_neg, 1):
            lines.append(f"  🔴 {sid} ({sname}): {detail[:60]} ({sc:+d})")
        if not _top_pos and not _top_neg:
            lines.append(f"  • Tổng hợp {total_factors} yếu tố → Điểm: {weighted_pct}%")
        lines.append("")
        
        # 3. ỨNG KỲ — Thời gian cụ thể dựa trên Hành DT
        _27_UK = {
            'Kim': ('tháng 7-8 ÂL (Thân/Dậu)', 'ngày Canh/Tân', 'Tây'),
            'Mộc': ('tháng 1-2 ÂL (Dần/Mão)', 'ngày Giáp/Ất', 'Đông'),
            'Thủy': ('tháng 10-11 ÂL (Hợi/Tý)', 'ngày Nhâm/Quý', 'Bắc'),
            'Hỏa': ('tháng 4-5 ÂL (Tỵ/Ngọ)', 'ngày Bính/Đinh', 'Nam'),
            'Thổ': ('tháng 3/6/9/12 ÂL (Tứ Quý)', 'ngày Mậu/Kỷ', 'Trung Tâm'),
        }
        _uk27 = _27_UK.get(hanh_dt, None)
        if _uk27:
            lines.append(f"**⏳ ỨNG KỲ:** {_uk27[0]}, {_uk27[1]} | Hướng: {_uk27[2]}")
        lines.append("")
        
        # 4. GIẢI PHÁP
        if weighted_pct >= 55:
            lines.append(f"**🔧 GIẢI PHÁP:** Tiến hành, nắm bắt cơ hội. Chọn thời điểm hành {hanh_dt} vượng.")
        elif weighted_pct >= 45:
            _sinh_hanh = {v: k for k, v in SINH.items()}.get(hanh_dt, '?')
            lines.append(f"**🔧 GIẢI PHÁP:** Có thể tiến hành nhưng cần bổ sung hành {_sinh_hanh} (sinh {hanh_dt}) để tăng lực.")
        else:
            _sinh_hanh = {v: k for k, v in SINH.items()}.get(hanh_dt, '?')
            lines.append(f"**🔧 GIẢI PHÁP:** Hoãn lại. Đợi tháng hành {_sinh_hanh} vượng hoặc tìm hướng đi mới.")
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 5. VẠN VẬT LOẠI TƯỢNG — SECTION NỔI BẬT (V41.0)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        lines.append("")
        lines.append("---")
        lines.append("### 🎴 VẠN VẬT LOẠI TƯỢNG")
        lines.append("")
        
        # A. Vạn Vật theo Ngũ Hành DT
        _VV_HANH_MAP = {
            'Kim': {'tuong': '⚔️ Kim loại, dao kéo, trang sức', 'mau': 'Trắng, bạc',
                    'huong': 'Tây', 'co_the': 'Phổi, hô hấp, xương, da',
                    'nguoi': 'Người cương nghị, sắc sảo, quyết đoán',
                    'nha': 'Nhà kiên cố, tường gạch, gần đường lớn'},
            'Mộc': {'tuong': '🌳 Gỗ, sách vở, vải, cây cối', 'mau': 'Xanh lá',
                    'huong': 'Đông', 'co_the': 'Gan, mật, gân, mắt',
                    'nguoi': 'Người nhân từ, thanh cao, gầy cao',
                    'nha': 'Nhà gỗ, gần cây xanh, vườn'},
            'Thủy': {'tuong': '💧 Nước, rượu, mực, đồ lỏng', 'mau': 'Đen, xanh đen',
                     'huong': 'Bắc', 'co_the': 'Thận, bàng quang, tai, xương',
                     'nguoi': 'Người thông minh, linh hoạt, mập',
                     'nha': 'Nhà gần sông/ao, nơi ẩm thấp'},
            'Hỏa': {'tuong': '🔥 Đèn, lửa, điện tử, đồ nóng', 'mau': 'Đỏ, tím',
                     'huong': 'Nam', 'co_the': 'Tim, mắt, huyết áp, lưỡi',
                     'nguoi': 'Người sôi nổi, nóng tính, hồng hào',
                     'nha': 'Nhà hướng Nam, nhiều ánh sáng'},
            'Thổ': {'tuong': '🏔️ Đá, gạch, gốm sứ, xi măng', 'mau': 'Vàng, nâu',
                    'huong': 'Trung tâm', 'co_the': 'Dạ dày, tỳ vị, miệng, cơ bắp',
                    'nguoi': 'Người trung thực, chắc nịch, đáng tin',
                    'nha': 'Nhà trệt, nền đất rộng, bằng phẳng'},
        }
        
        vv_data = _VV_HANH_MAP.get(hanh_dt, {})
        if vv_data:
            lines.append(f"**Hành Dụng Thần:** {hanh_dt}")
            lines.append(f"- 🎨 **Tượng vật:** {vv_data.get('tuong', '?')}")
            lines.append(f"- 🧭 **Hướng:** {vv_data.get('huong', '?')} | **Màu sắc:** {vv_data.get('mau', '?')}")
            
            # Context-aware: chỉ hiện thông tin liên quan đến câu hỏi
            if any(k in q_lower for k in ['bệnh', 'ốm', 'đau', 'khỏe', 'sức khỏe', 'thuốc', 'viện']):
                lines.append(f"- 🏥 **Cơ thể cần chú ý:** {vv_data.get('co_the', '?')}")
            if any(k in q_lower for k in ['nhà', 'đất', 'ở', 'mua nhà', 'xây']):
                lines.append(f"- 🏠 **Nhà cửa:** {vv_data.get('nha', '?')}")
            if any(k in q_lower for k in ['tìm', 'mất', 'trộm', 'ai', 'người']):
                lines.append(f"- 👤 **Người liên quan:** {vv_data.get('nguoi', '?')}")
                lines.append(f"- 🎨 **Màu sắc vật/người:** {vv_data.get('mau', '?')}")
                lines.append(f"- 🧭 **Hướng tìm:** {vv_data.get('huong', '?')}")
            
            # Luôn hiện tượng + người mặc định nếu không match context
            if not any(k in q_lower for k in ['bệnh', 'nhà', 'tìm', 'mất', 'ai']):
                lines.append(f"- 👤 **Người liên quan:** {vv_data.get('nguoi', '?')}")
                lines.append(f"- 🏠 **Nhà cửa/Vị trí:** {vv_data.get('nha', '?')}")
        
        # B. Quái Tượng từ Mai Hoa (nếu có)
        try:
            if mai_hoa_data and isinstance(mai_hoa_data, dict):
                _mh_ten = mai_hoa_data.get('ten_thuong', mai_hoa_data.get('thuong_quai', ''))
                _mh_ha = mai_hoa_data.get('ten_ha', mai_hoa_data.get('ha_quai', ''))
                _q_up = QUAI_Y_NGHIA.get(_mh_ten, {})
                _q_lo = QUAI_Y_NGHIA.get(_mh_ha, {})
                if _q_up or _q_lo:
                    lines.append("")
                    lines.append(f"**Quái Tượng:**")
                    if _q_up:
                        lines.append(f"- Thượng Quái ({_mh_ten}): {_q_up.get('tuong', '?')} — {_q_up.get('tc', '?')}")
                    if _q_lo:
                        lines.append(f"- Hạ Quái ({_mh_ha}): {_q_lo.get('tuong', '?')} — {_q_lo.get('tc', '?')}")
        except Exception:
            pass
        
        lines.append("")
        
        protocol_text = "\n".join(lines)
        conclusion_text = f"{final_icon} {final_verdict} ({weighted_pct}%) — {cat_count}/6 CÁT — {total_factors} yếu tố"
        
        return protocol_text, conclusion_text, weighted_pct
    
    @staticmethod
    def _extract_score_from_factor(factor_text):
        """Trích điểm số từ factor string. VD: 'DT Vượng +10' → 10"""
        import re
        match = re.search(r'([+-]\d+)\s*$', factor_text)
        if match:
            return int(match.group(1))
        return 0
    
    # ═══════════════════════════════════════════════════════════
    # V16.0 / V26.2: ĐẠI THỐNG NHẤT SCORING ĐA PHƯƠNG PHÁP
    # ═══════════════════════════════════════════════════════════
    
    def _ky_mon_scoring(self, chart_data, dung_than):
        """V26.2: Chấm điểm Kỳ Môn Độn Giáp — 10 tầng scoring."""
        if not chart_data or not isinstance(chart_data, dict):
            return 0, "Không có dữ liệu Kỳ Môn", []
            
        score = 0
        factors = []
        
        can_ngay = chart_data.get('can_ngay', '')
        chi_ngay = chart_data.get('chi_ngay', '')
        can_thien_ban = chart_data.get('can_thien_ban', {})
        thien_ban = chart_data.get('thien_ban', {})
        nhan_ban = chart_data.get('nhan_ban', {})
        than_ban = chart_data.get('than_ban', {})
        
        # 1. Xác định Can của Dụng Thần
        dt_can_map = {
            'Quan Quỷ': chart_data.get('can_gio', ''),
            'Thê Tài': chart_data.get('can_gio', ''),
            'Tử Tôn': chart_data.get('can_gio', ''),
            'Phụ Mẫu': chart_data.get('can_nam', ''),
            'Huynh Đệ': chart_data.get('can_thang', ''),
            'Bản Thân': can_ngay,
        }
        dt_can = dt_can_map.get(dung_than, chart_data.get('can_gio', ''))
        
        # Cung BT và DT
        bt_cung = None
        dt_cung = None
        for cung_num, can_val in can_thien_ban.items():
            if can_val == can_ngay: bt_cung = int(cung_num) if cung_num else None
            # V40.2: Giáp ẩn duới Mậu HOẶC Kỷ
            if not bt_cung and can_ngay == 'Giáp' and can_val in ('Mậu', 'Kỷ'):
                bt_cung = int(cung_num) if cung_num else None
                
        for cung_num, can_val in can_thien_ban.items():
            if can_val == dt_can: dt_cung = int(cung_num) if cung_num else None
            if not dt_cung and dt_can == 'Giáp' and can_val in ('Mậu', 'Kỷ'):
                dt_cung = int(cung_num) if cung_num else None
        
        if not dt_cung:
            return 0, "Không tìm thấy Cung Dụng Thần KM", []
            
        bt_hanh = CUNG_NGU_HANH.get(bt_cung, '') if bt_cung else ''
        dt_hanh_cung = CUNG_NGU_HANH.get(dt_cung, '')
        dt_hanh_can = CAN_NGU_HANH.get(dt_can, '')
        
        # ① Sinh Khắc Cung (DT vs BT) (±8)
        if bt_hanh and dt_hanh_cung and bt_cung != dt_cung:
            if SINH.get(dt_hanh_cung) == bt_hanh:
                score += 8
                factors.append(f"KM Cung DT tương sinh BT +8")
            elif KHAC.get(dt_hanh_cung) == bt_hanh:
                score -= 8
                factors.append(f"KM Cung DT khắc BT -8")
            elif KHAC.get(bt_hanh) == dt_hanh_cung:
                score += 5
                factors.append(f"KM Cung BT khắc DT (chủ động) +5")
            elif SINH.get(bt_hanh) == dt_hanh_cung:
                score -= 4
                factors.append(f"KM Cung BT sinh DT (hao) -4")
            elif bt_hanh == dt_hanh_cung:
                score += 2
                factors.append(f"KM Cung DT và BT Tỷ hòa +2")
                
        # ② Sao tại cung DT (±5)
        dt_sao = str(thien_ban.get(dt_cung, thien_ban.get(str(dt_cung), '')))
        sao_info = SAO_GIAI_THICH.get(dt_sao, {})
        sao_ch = sao_info.get('cat_hung', '')
        if 'Đại Cát' in sao_ch: score += 5; factors.append(f"KM Sao {dt_sao} Cát +5")
        elif 'Cát' in sao_ch: score += 3; factors.append(f"KM Sao {dt_sao} Cát +3")
        elif 'Đại Hung' in sao_ch: score -= 5; factors.append(f"KM Sao {dt_sao} Hung -5")
        elif 'Hung' in sao_ch: score -= 3; factors.append(f"KM Sao {dt_sao} Hung -3")
        
        # ③ Cửa tại cung DT (±6)
        dt_cua = str(nhan_ban.get(dt_cung, nhan_ban.get(str(dt_cung), '')))
        cua_key = dt_cua if 'Môn' in dt_cua else dt_cua + ' Môn'
        cua_info = CUA_GIAI_THICH.get(cua_key, {})
        cua_ch = cua_info.get('cat_hung', '')
        if 'Đại Cát' in cua_ch: score += 6; factors.append(f"KM Cửa {dt_cua} Cát +6")
        elif 'Cát' in cua_ch: score += 4; factors.append(f"KM Cửa {dt_cua} Cát +4")
        elif 'Đại Hung' in cua_ch: score -= 6; factors.append(f"KM Cửa {dt_cua} Hung -6")
        elif 'Hung' in cua_ch: score -= 4; factors.append(f"KM Cửa {dt_cua} Hung -4")
        
        # ④ Thần tại cung DT (±4)
        dt_than = str(than_ban.get(dt_cung, than_ban.get(str(dt_cung), '')))
        than_info = THAN_GIAI_THICH.get(dt_than, {})
        than_tc = than_info.get('tinh_chat', '')
        if any(k in than_tc for k in ['CÁT', 'cát', 'giúp']): score += 4; factors.append(f"KM Thần {dt_than} Cát +4")
        elif any(k in than_tc for k in ['tai', 'lừa', 'phá', 'HUNG', 'hung']): score -= 4; factors.append(f"KM Thần {dt_than} Hung -4")
        
        # ⑤ Vượng Suy Can tại Cung (±4)
        if dt_hanh_can and dt_hanh_cung:
            if dt_hanh_can == dt_hanh_cung: score += 4; factors.append(f"KM Can DT Vượng tại Cung +4")
            elif SINH.get(dt_hanh_cung) == dt_hanh_can: score += 2; factors.append(f"KM Can DT Tướng tại Cung +2")
            elif KHAC.get(dt_hanh_cung) == dt_hanh_can: score -= 4; factors.append(f"KM Can DT Tử tại Cung -4")
            elif KHAC.get(dt_hanh_can) == dt_hanh_cung: score -= 2; factors.append(f"KM Can DT Tù tại Cung -2")
            
        # ⑥ Tuần Không (-10)
        cung_chi_km = {
            1: ['Tý'], 8: ['Sửu', 'Dần'], 3: ['Mão'], 4: ['Thìn', 'Tị', 'Tỵ'],
            9: ['Ngọ'], 2: ['Mùi', 'Thân'], 7: ['Dậu'], 6: ['Tuất', 'Hợi']
        }
        khong_vong = _get_khong_vong(can_ngay, chi_ngay) if can_ngay and chi_ngay else []
        cung_chis = cung_chi_km.get(dt_cung, [])
        if any(c in khong_vong for c in cung_chis):
            score -= 10
            factors.append(f"KM Cung DT Không Vong -10")
            
        # ⑦ Mã Tinh (+3)
        ma_tinh_map = {'Thân': 'Dần', 'Tý': 'Dần', 'Thìn': 'Dần',
                       'Dần': 'Thân', 'Ngọ': 'Thân', 'Tuất': 'Thân',
                       'Tị': 'Hợi', 'Dậu': 'Hợi', 'Sửu': 'Hợi',
                       'Hợi': 'Tị', 'Mão': 'Tị', 'Mùi': 'Tị'}
        chi_ma = ma_tinh_map.get(chi_ngay, '')
        if chi_ma and chi_ma in cung_chis:
            score += 3
            factors.append(f"KM Cung DT có Mã Tinh +3")
            
        if score >= 15: strength = "🟢 CỰC VƯỢNG"
        elif score >= 8: strength = "🟢 VƯỢNG"
        elif score >= 3: strength = "🔵 TƯỚNG"
        elif score >= -3: strength = "🟡 BÌNH"
        elif score >= -8: strength = "🟠 SUY"
        else: strength = "🔴 TỬ"
        
        summary = f"KM Điểm={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V40.2: V27 BONUS FACTORS — save base, try bonus, restore on fail
        _base_score, _base_factors = score, list(factors)
        try:
            # Factor 1: Tuong tac Sao x Mon
            if TUONG_TAC_SAO_MON and dt_cung is not None:
                sao_dt = ''
                mon_dt = ''
                if isinstance(thien_ban, dict):
                    sao_dt = thien_ban.get(dt_cung, {}).get('sao', '') if isinstance(thien_ban.get(dt_cung), dict) else str(thien_ban.get(dt_cung, ''))
                if isinstance(nhan_ban, dict):
                    mon_dt = nhan_ban.get(dt_cung, {}).get('mon', '') if isinstance(nhan_ban.get(dt_cung), dict) else str(nhan_ban.get(dt_cung, ''))
                sao_mon_key = (sao_dt, mon_dt)
                sm_result = TUONG_TAC_SAO_MON.get(sao_mon_key, '')
                if sm_result:
                    if 'Cat' in str(sm_result) or 'Cát' in str(sm_result):
                        score += 5
                        factors.append(f"KM Sao×Môn Cát +5: {sao_dt}×{mon_dt}")
                    else:
                        score -= 3
                        factors.append(f"KM Sao×Môn: {sm_result}")
            # Factor 2: Sinh khac BT<->DT
            if bt_cung is not None and dt_cung is not None:
                hanh_bt_cung = CUNG_NGU_HANH.get(bt_cung, '')
                hanh_dt_cung = CUNG_NGU_HANH.get(dt_cung, '')
                if hanh_bt_cung and hanh_dt_cung:
                    rel = DATANG_SINH_KHAC(hanh_bt_cung, hanh_dt_cung)
                    if 'Sinh' in str(rel) and 'Bi' not in str(rel):
                        score += 6
                        factors.append(f"KM Cung BT sinh DT +6 ({hanh_bt_cung}→{hanh_dt_cung})")
                    elif 'Khac' in str(rel) or 'Khắc' in str(rel):
                        if 'Bi' in str(rel) or 'Bị' in str(rel):
                            score -= 6
                            factors.append(f"KM Cung BT bị khắc -6 ({hanh_bt_cung}←{hanh_dt_cung})")
                        else:
                            score += 4
                            factors.append(f"KM Cung BT khắc DT +4")
            # Factor 3: Vuong Suy theo mua
            if dt_can:
                can_hanh_km = CAN_NGU_HANH.get(dt_can, '')
                tiet_khi = chart_data.get('tiet_khi', '')
                if can_hanh_km and tiet_khi:
                    vs = BLIND_VUONG_SUY(can_hanh_km, tiet_khi)
                    if vs:
                        vs_str = str(vs)
                        if 'Vuong' in vs_str or 'Vượng' in vs_str:
                            score += 5
                            factors.append(f"KM DT Vượng mùa +5")
                        elif 'Tu' in vs_str or 'Tử' in vs_str or 'Tù' in vs_str:
                            score -= 5
                            factors.append(f"KM DT Tử/Tù mùa -5")
            # Factor 5: Cách Cục
            if dt_cung and can_thien_ban:
                thien_can_dt = can_thien_ban.get(dt_cung, can_thien_ban.get(str(dt_cung), ''))
                DIA_BAN_CAN = {1: 'Mậu', 2: 'Kỷ', 3: 'Canh', 4: 'Tân', 5: 'Mậu', 6: 'Nhâm', 7: 'Quý', 8: 'Ất', 9: 'Bính'}
                dia_can_dt = DIA_BAN_CAN.get(dt_cung if isinstance(dt_cung, int) else int(dt_cung), '')
                if thien_can_dt and dia_can_dt:
                    CAT_CACH = {
                        ('Ất', 'Bính'): 'Nhật Kỳ → CÁT',
                        ('Ất', 'Đinh'): 'Tinh Kỳ → CÁT',
                        ('Bính', 'Đinh'): 'Nhật Nguyệt Kỳ → ĐẠI CÁT',
                        ('Đinh', 'Ất'): 'Ngọc Nữ → CÁT',
                    }
                    HUNG_CACH = {
                        ('Canh', 'Ất'): 'Bạch Hổ xướng cuồng → HUNG',
                        ('Canh', 'Bính'): 'Phi Can Cách → HUNG',
                        ('Canh', 'Đinh'): 'Thiên Ất → HUNG',
                        ('Tân', 'Ất'): 'Thanh Long đào giấu → HUNG',
                        ('Tân', 'Bính'): 'Đằng Xà yêu kiếp → HUNG',
                        ('Tân', 'Đinh'): 'Chu Tước → HƯU',
                    }
                    key_cc = (str(thien_can_dt), str(dia_can_dt))
                    if key_cc in CAT_CACH:
                        score += 6
                        factors.append(f"KM Cách Cục: {CAT_CACH[key_cc]} +6 ({thien_can_dt}/{dia_can_dt})")
                    elif key_cc in HUNG_CACH:
                        score -= 6
                        factors.append(f"KM Cách Cục: {HUNG_CACH[key_cc]} -6 ({thien_can_dt}/{dia_can_dt})")
            # Factor 6: Tam Kỳ nhập cung DT
            if dt_cung and can_thien_ban:
                thien_can_at_dt = can_thien_ban.get(dt_cung, can_thien_ban.get(str(dt_cung), ''))
                if thien_can_at_dt in ('Ất', 'Bính', 'Đinh'):
                    score += 5
                    tam_ky_name = {'Ất': 'Nhật Kỳ', 'Bính': 'Nguyệt Kỳ', 'Đinh': 'Tinh Kỳ'}.get(thien_can_at_dt, '')
                    factors.append(f"KM Tam Kỳ: {tam_ky_name}({thien_can_at_dt}) nhập cung DT +5")
            # Factor 7: Cung Sự Việc
            sv_cung = None
            can_gio = chart_data.get('can_gio', '')
            if can_gio and can_thien_ban:
                for cung_num, can_val in can_thien_ban.items():
                    if can_val == can_gio:
                        sv_cung = int(cung_num) if cung_num else None
                        break
            if sv_cung and bt_cung and sv_cung != bt_cung:
                sv_hanh = CUNG_NGU_HANH.get(sv_cung, '')
                if bt_hanh and sv_hanh:
                    if KHAC.get(bt_hanh) == sv_hanh:
                        score += 5
                        factors.append(f"KM BT khắc Cung SV → chủ THẮNG +5")
                    elif KHAC.get(sv_hanh) == bt_hanh:
                        score -= 5
                        factors.append(f"KM Cung SV khắc BT → bị THUA -5")
                    elif SINH.get(sv_hanh) == bt_hanh:
                        score += 3
                        factors.append(f"KM Cung SV sinh BT → được giúp +3")
        except Exception:
            score, factors = _base_score, _base_factors
        
        return score, summary, factors

    def _luc_hao_scoring(self, luc_hao_data, dung_than):
        """V16.0: Chấm điểm Lục Hào — 8 tầng scoring."""
        if not luc_hao_data or not isinstance(luc_hao_data, dict):
            return 0, "Không có dữ liệu Lục Hào", []
        
        score = 0
        factors = []
        ban = luc_hao_data.get('ban', {})
        bien = luc_hao_data.get('bien', {})
        dong_hao = luc_hao_data.get('dong_hao', [])
        haos = ban.get('haos') or ban.get('details', [])
        if not haos:
            return 0, "Không có hào", []
        
        # Tìm DT hào
        dt_hao = None
        dt_idx = None
        the_hao = None
        for i, hao in enumerate(haos):
            lt = hao.get('luc_than', '')
            tu = hao.get('the_ung', '') or hao.get('marker', '')
            if lt == dung_than:
                dt_hao = hao
                dt_idx = i + 1
            elif dung_than == 'Bản Thân' and ('Thế' in str(tu)):
                dt_hao = hao
                dt_idx = i + 1
            if 'Thế' in str(tu):
                the_hao = hao
        
        is_phuc_than = False
        if not dt_hao:
            # FIX V42.9: Nếu Dụng Thần không xuất hiện, tìm trong Phục Thần
            phuc_than_list = luc_hao_data.get('phuc_than', [])
            if isinstance(phuc_than_list, list):
                for pt in phuc_than_list:
                    if pt.get('luc_than') == dung_than:
                        dt_hao = pt
                        dt_hao['ngu_hanh'] = pt.get('element') or pt.get('ngu_hanh', '')
                        dt_hao['marker'] = '(Phục Thần)'
                        is_phuc_than = True
                        break
            
            # Chỉ fallback vào Hào Thế nếu đang hỏi "Bản Thân"
            if not dt_hao and dung_than == 'Bản Thân' and the_hao:
                dt_hao = the_hao
            
            # Nếu vẫn không thấy
            if not dt_hao:
                return -10, "DT hào ẩn (Phục Thần) → -10", ["DT ẩn (Phục Thần) -10"]
        
        # V32.5: Unified key mapping — support both old (vuong_suy/chi) and new (strength/can_chi) format
        def _get_vuong(h):
            return str(h.get('vuong_suy', '') or h.get('strength', '') or '')
        def _get_chi(h):
            c = h.get('chi', '')
            if not c:
                cc = h.get('can_chi', '')  # Format: 'Sửu-Thổ'
                if cc and '-' in cc:
                    c = cc.split('-')[0]
            return c
        def _is_dong(h, idx):
            if h.get('dong') or h.get('is_moving'):
                return True
            return idx in (dong_hao or [])
        
        dt_hanh = dt_hao.get('ngu_hanh', '')
        dt_vuong = _get_vuong(dt_hao)
        dt_chi = _get_chi(dt_hao)
        
        # FIX V42.9: Phạt điểm ngay lập tức nếu là Phục Thần
        if is_phuc_than:
            score -= 10
            factors.append(f"⚠️ PHỤC THẦN: DT ({dung_than}) ẩn, chưa lộ diện -10")
        
        # ① DT Vượng/Suy (±10)
        if 'Vượng' in dt_vuong or 'Tướng' in dt_vuong or 'Đế Vượng' in dt_vuong:
            score += 10
            factors.append(f"DT {dt_vuong} +10")
        elif 'Trường Sinh' in dt_vuong or 'Mộc Dục' in dt_vuong:
            score += 6
            factors.append(f"DT {dt_vuong} +6")
        elif 'Suy' in dt_vuong or 'Bệnh' in dt_vuong:
            score -= 8
            factors.append(f"DT {dt_vuong} -8")
        elif 'Tử' in dt_vuong or 'Tuyệt' in dt_vuong:
            score -= 10
            factors.append(f"DT {dt_vuong} -10")
        elif 'Mộ' in dt_vuong:
            score -= 6
            factors.append(f"DT Mộ -6")
        
        # ② Nguyệt lệnh sinh/khắc DT (±8)
        chi_thang = luc_hao_data.get('chi_thang', '') or ban.get('chi_thang', '')
        can_ngay = luc_hao_data.get('can_ngay', '') or ban.get('can_ngay', '')
        chi_ngay = luc_hao_data.get('chi_ngay', '') or ban.get('chi_ngay', '')
        
        # V32.5: Fallback từ chart_data khi LH không có Nguyệt/Nhật
        if not chi_thang:
            try:
                import datetime as _dt_lh
                from qmdg_calc import calculate_qmdg_params as _calc_lh
                _p = _calc_lh(_dt_lh.datetime.now())
                chi_thang = _p.get('chi_thang', '')
                if not can_ngay: can_ngay = _p.get('can_ngay', '')
                if not chi_ngay: chi_ngay = _p.get('chi_ngay', '')
            except:
                pass
        
        hanh_thang = CHI_NGU_HANH.get(chi_thang, '')
        if hanh_thang and dt_hanh:
            if SINH.get(hanh_thang) == dt_hanh:
                score += 8
                factors.append(f"Nguyệt({chi_thang}/{hanh_thang}) sinh DT +8")
            elif KHAC.get(hanh_thang) == dt_hanh:
                score -= 8
                factors.append(f"Nguyệt({chi_thang}/{hanh_thang}) khắc DT -8")
            elif hanh_thang == dt_hanh:
                score += 4
                factors.append(f"Nguyệt({chi_thang}/{hanh_thang}) tỷ hòa DT +4")
            else:
                factors.append(f"Nguyệt({chi_thang}/{hanh_thang}) không tác động DT +0")
        
        # ③ Nhật Thần sinh/khắc DT (±6)
        hanh_ngay = CAN_NGU_HANH.get(can_ngay, '')
        if hanh_ngay and dt_hanh:
            if SINH.get(hanh_ngay) == dt_hanh:
                score += 6
                factors.append(f"Nhật({can_ngay}/{hanh_ngay}) sinh DT +6")
            elif KHAC.get(hanh_ngay) == dt_hanh:
                score -= 6
                factors.append(f"Nhật({can_ngay}/{hanh_ngay}) khắc DT -6")
            elif hanh_ngay == dt_hanh:
                score += 3
                factors.append(f"Nhật({can_ngay}/{hanh_ngay}) tỷ hòa DT +3")
            else:
                factors.append(f"Nhật({can_ngay}/{hanh_ngay}) không tác động DT +0")
        
        # ④ Nguyên Thần (sinh DT) status (±6)
        nguyen_hanh = [h for h, s in SINH.items() if s == dt_hanh] if dt_hanh else []
        nt_found = False
        for hao in haos:
            h_hanh = hao.get('ngu_hanh', '')
            if h_hanh in nguyen_hanh:
                h_vuong = _get_vuong(hao)
                h_lt = hao.get('luc_than', '')
                h_idx = haos.index(hao) + 1
                if 'Vượng' in h_vuong or 'Tướng' in h_vuong:
                    score += 6
                    factors.append(f"NT({h_hanh}) Nguyên Thần vượng +6")
                elif 'Suy' in h_vuong or 'Tử' in h_vuong or 'Bệnh' in h_vuong:
                    score -= 3
                    factors.append(f"NT({h_hanh}) Nguyên Thần suy -3")
                else:
                    # V32.5: vuong_suy trống → vẫn ghi nhận NT tồn tại
                    is_dong_nt = _is_dong(hao, h_idx)
                    if is_dong_nt:
                        score += 5
                        factors.append(f"NT({h_hanh}) Nguyên Thần động +5")
                    else:
                        score += 2
                        factors.append(f"NT({h_hanh}) Nguyên Thần bình +2")
                nt_found = True
                break
        if not nt_found and nguyen_hanh:
            factors.append(f"NT(ẩn) Nguyên Thần ẩn +0")
        
        # ⑤ Kỵ Thần (khắc DT) status (±6)
        ky_hanh = [h for h, k in KHAC.items() if k == dt_hanh] if dt_hanh else []
        kt_found = False
        for hao in haos:
            h_hanh = hao.get('ngu_hanh', '')
            if h_hanh in ky_hanh:
                h_vuong = _get_vuong(hao)
                h_idx = haos.index(hao) + 1
                is_dong_kt = _is_dong(hao, h_idx)
                if ('Vượng' in h_vuong or 'Tướng' in h_vuong) and is_dong_kt:
                    score -= 8
                    factors.append(f"KT({h_hanh}) Kỵ Thần vượng+động -8")
                elif 'Vượng' in h_vuong or 'Tướng' in h_vuong:
                    score -= 5
                    factors.append(f"KT({h_hanh}) Kỵ Thần vượng -5")
                elif 'Suy' in h_vuong or 'Tử' in h_vuong or 'Bệnh' in h_vuong:
                    score += 3
                    factors.append(f"KT({h_hanh}) Kỵ Thần suy +3")
                else:
                    # V32.5: vuong_suy trống
                    if is_dong_kt:
                        score -= 4
                        factors.append(f"KT({h_hanh}) Kỵ Thần động -4")
                    else:
                        score -= 1
                        factors.append(f"KT({h_hanh}) Kỵ Thần bình -1")
                kt_found = True
                break
        if not kt_found and ky_hanh:
            factors.append(f"KT(ẩn) Kỵ Thần ẩn +0")
        
        # ⑥ Hào Động — DT Động = phát động (±5)
        if dt_idx and dong_hao and dt_idx in dong_hao:
            bien_haos = bien.get('haos') or bien.get('details', []) if bien else []
            if bien_haos and dt_idx <= len(bien_haos):
                bien_hao = bien_haos[dt_idx - 1]
                bien_hanh = bien_hao.get('ngu_hanh', '')
                if bien_hanh and dt_hanh:
                    if SINH.get(bien_hanh) == dt_hanh:
                        score += 8
                        factors.append("Hóa Hồi sinh +8")
                    elif KHAC.get(bien_hanh) == dt_hanh:
                        score -= 8
                        factors.append("Hóa Hồi khắc -8")
                    elif bien_hanh == dt_hanh:
                        score += 3
                        factors.append("Hóa Phục +3")
                    
                    # V21.0: TIẾN THẦN / THỐI THẦN (±8)
                    bien_chi = bien_hao.get('chi', '')
                    if dt_chi and bien_chi and dt_chi != bien_chi:
                        TIEN_THAN = {'Dần': 'Mão', 'Mão': 'Thìn', 'Tị': 'Ngọ', 'Ngọ': 'Mùi',
                                     'Thân': 'Dậu', 'Dậu': 'Tuất', 'Hợi': 'Tý', 'Tý': 'Sửu',
                                     'Sửu': 'Dần', 'Thìn': 'Tị', 'Mùi': 'Thân', 'Tuất': 'Hợi'}
                        THOI_THAN = {v: k for k, v in TIEN_THAN.items()}
                        if TIEN_THAN.get(dt_chi) == bien_chi:
                            score += 8
                            factors.append(f"TIẾN THẦN ({dt_chi}→{bien_chi}) +8")
                        elif THOI_THAN.get(dt_chi) == bien_chi:
                            score -= 8
                            factors.append(f"THỐI THẦN ({dt_chi}→{bien_chi}) -8")
        
        # ⑦ Tuần Không (−15)
        chi_ngay = luc_hao_data.get('chi_ngay', '') or ban.get('chi_ngay', '')
        if can_ngay and chi_ngay and dt_chi:
            kv = _get_khong_vong(can_ngay, chi_ngay)
            if kv and dt_chi in kv:
                score -= 15
                factors.append("DT Tuần Không -15")
        
        # ⑧ V21.0: NGUYỆT PHÁ — chi tháng xung chi DT hào (−12)
        chi_thang_lh = luc_hao_data.get('chi_thang', '')
        if chi_thang_lh and dt_chi:
            CHI_XUNG = {'Tý': 'Ngọ', 'Ngọ': 'Tý', 'Sửu': 'Mùi', 'Mùi': 'Sửu',
                        'Dần': 'Thân', 'Thân': 'Dần', 'Mão': 'Dậu', 'Dậu': 'Mão',
                        'Thìn': 'Tuất', 'Tuất': 'Thìn', 'Tị': 'Hợi', 'Hợi': 'Tị'}
            if CHI_XUNG.get(chi_thang_lh) == dt_chi:
                score -= 12
                factors.append(f"NGUYỆT PHÁ ({chi_thang_lh}⇔{dt_chi}) -12")
        
        # ⑨ Thế↔Ứng (±5)
        the_h = None
        ung_h = None
        for hao in haos:
            if hao.get('the_ung') == 'Thế':
                the_h = hao.get('ngu_hanh', '')
            elif hao.get('the_ung') == 'Ứng':
                ung_h = hao.get('ngu_hanh', '')
        if the_h and ung_h:
            if KHAC.get(the_h) == ung_h:
                score += 5
                factors.append("Thế khắc Ứng +5")
            elif KHAC.get(ung_h) == the_h:
                score -= 5
                factors.append("Ứng khắc Thế -5")
        
        # ═══════════════════════════════════════════════════════════
        # V26.2: THÊM 14 YẾU TỐ MỚI (⑩-㉓) — TOÀN DIỆN AI OFFLINE
        # ═══════════════════════════════════════════════════════════
        
        # ⑩ Cừu Thần (hành sinh Kỵ Thần → tăng sức khắc DT) (±4)
        if dt_hanh:
            ky_hanh_list = [h for h, k in KHAC.items() if k == dt_hanh]
            cuu_hanh_list = []
            for kh in ky_hanh_list:
                cuu_hanh_list.extend([h for h, s in SINH.items() if s == kh])
            for hao in haos:
                h_hanh = hao.get('ngu_hanh', '')
                h_idx = haos.index(hao) + 1
                if h_hanh in cuu_hanh_list and hao != dt_hao:
                    h_vuong = str(hao.get('vuong_suy', ''))
                    if 'Vượng' in h_vuong and h_idx in (dong_hao or []):
                        score -= 4
                        factors.append(f"Cừu Thần ({h_hanh}) vượng+động -4")
                    elif 'Vượng' in h_vuong:
                        score -= 2
                        factors.append(f"Cừu Thần ({h_hanh}) vượng -2")
                    break
        
        # ⑪⑫ Phản Ngâm / Phục Ngâm (DT động → biến)
        bien_haos = bien.get('haos') or bien.get('details', []) if bien else []
        if dt_idx and dong_hao and dt_idx in dong_hao and bien_haos and dt_idx <= len(bien_haos):
            bien_hao = bien_haos[dt_idx - 1]
            bien_chi = bien_hao.get('chi', '')
            # Phản Ngâm: chi DT xung chi biến (đảo ngược 180°)
            if dt_chi and bien_chi and LUC_XUNG_CHI.get(dt_chi) == bien_chi:
                score -= 10
                factors.append(f"PHẢN NGÂM ({dt_chi}⇔{bien_chi}) -10")
            # Phục Ngâm: chi biến = chi DT (dậm chân tại chỗ)
            elif dt_chi and bien_chi and dt_chi == bien_chi:
                score -= 6
                factors.append(f"PHỤC NGÂM ({dt_chi}={bien_chi}) -6")
            
            # ㉒ Hóa Tuyệt / Hóa Mộ — DT biến vào giai đoạn tiêu tan
            bien_vuong = str(bien_hao.get('vuong_suy', ''))
            if 'Tuyệt' in bien_vuong:
                score -= 8
                factors.append(f"Hóa TUYỆT ({bien_chi}) -8")
            elif 'Mộ' in bien_vuong:
                score -= 5
                factors.append(f"Hóa MỘ ({bien_chi}) -5")
        
        # ⑬ Nhật Hợp DT — Nhật chi hợp chi DT (bị ràng buộc)
        chi_ngay = luc_hao_data.get('chi_ngay', '') or ban.get('chi_ngay', '')
        if chi_ngay and dt_chi and LUC_HOP_CHI.get(chi_ngay) == dt_chi:
            if dt_idx and dong_hao and dt_idx in dong_hao:
                score += 4
                factors.append(f"Nhật Hợp DT động +4")
            else:
                score -= 4
                factors.append(f"Nhật Hợp DT tĩnh (ràng buộc) -4")
        
        # ⑭ Nhật Xung DT / Ám Động — Nhật chi xung chi DT khi DT tĩnh
        if chi_ngay and dt_chi and LUC_XUNG_CHI.get(chi_ngay) == dt_chi:
            dt_is_dong = dt_idx and dong_hao and dt_idx in dong_hao
            if not dt_is_dong:
                # DT tĩnh bị Nhật xung = Ám Động (lay động)
                dt_vuong_check = str(dt_hao.get('vuong_suy', ''))
                if 'Vượng' in dt_vuong_check or 'Tướng' in dt_vuong_check:
                    score += 5
                    factors.append(f"ÁM ĐỘNG vượng ({chi_ngay}⇔{dt_chi}) +5")
                else:
                    score -= 5
                    factors.append(f"Nhật Xung DT suy ({chi_ngay}⇔{dt_chi}) -5")
        
        # ⑮ Lục Hợp chi DT — Hào khác hợp chi DT (bị giữ lại)
        for hao in haos:
            if hao == dt_hao:
                continue
            h_chi = hao.get('chi', '')
            if h_chi and dt_chi and LUC_HOP_CHI.get(h_chi) == dt_chi:
                h_lt = hao.get('luc_than', '')
                score -= 3
                factors.append(f"Hào {h_lt}({h_chi}) hợp DT -3")
                break  # Chỉ tính 1 lần
        
        # ⑯ Lục Xung chi DT — Hào khác xung chi DT (bất ổn)
        for hao in haos:
            if hao == dt_hao:
                continue
            h_chi = hao.get('chi', '')
            h_idx = haos.index(hao) + 1
            if h_chi and dt_chi and LUC_XUNG_CHI.get(h_chi) == dt_chi:
                if h_idx in (dong_hao or []):
                    score -= 4
                    factors.append(f"Hào động ({h_chi}) xung DT -4")
                    break
        
        # ⑰ Tam Hợp Cục sinh/khắc DT
        if dt_hanh:
            all_chi = [h.get('chi', '') for h in haos if h.get('chi')]
            for tam_hop_set, (thc_hanh, thc_desc) in TAM_HOP_CUC.items():
                matching = [c for c in all_chi if c in tam_hop_set]
                if len(matching) >= 3:
                    if SINH.get(thc_hanh) == dt_hanh:
                        score += 6
                        factors.append(f"Tam Hợp {thc_hanh} sinh DT +6")
                    elif KHAC.get(thc_hanh) == dt_hanh:
                        score -= 6
                        factors.append(f"Tam Hợp {thc_hanh} khắc DT -6")
                    break
        # ⑰b V41.0: TAM HÌNH — Chi DT bị Hình phạt (HUNG mạnh)
        if dt_chi:
            all_chi = [h.get('chi', '') for h in haos if h.get('chi')]
            # Check Tam Hình pairs giữa DT chi và các hào khác
            for h_chi in all_chi:
                if h_chi == dt_chi:
                    continue
                hinh = _check_tam_hinh(dt_chi, h_chi)
                if hinh:
                    score -= 5
                    factors.append(f"TAM HÌNH: DT({dt_chi})↔({h_chi}) = {hinh} -5")
                    break  # Chỉ tính 1 lần
            # Check Tam Hình giữa DT chi và Chi Ngày
            if chi_ngay and chi_ngay != dt_chi:
                hinh_ngay = _check_tam_hinh(dt_chi, chi_ngay)
                if hinh_ngay:
                    score -= 3
                    factors.append(f"TAM HÌNH: DT({dt_chi})↔Nhật({chi_ngay}) = {hinh_ngay} -3")
        
        # ⑱ Hào Động KHÁC sinh/khắc DT (QUAN TRỌNG NHẤT — scan TẤT CẢ hào động)
        if dong_hao and dt_hanh:
            dong_sinh_count = 0
            dong_khac_count = 0
            for d_idx in dong_hao:
                if d_idx == dt_idx:
                    continue  # Bỏ qua DT
                if d_idx <= len(haos):
                    d_hao = haos[d_idx - 1]
                    d_hanh = d_hao.get('ngu_hanh', '')
                    d_lt = d_hao.get('luc_than', '')
                    if d_hanh and SINH.get(d_hanh) == dt_hanh:
                        dong_sinh_count += 1
                        score += 5
                        factors.append(f"Hào {d_idx} {d_lt}({d_hanh}) động sinh DT +5")
                    elif d_hanh and KHAC.get(d_hanh) == dt_hanh:
                        dong_khac_count += 1
                        score -= 5
                        factors.append(f"Hào {d_idx} {d_lt}({d_hanh}) động khắc DT -5")
        
        # ⑲ DT Động / Tĩnh
        dt_is_dong = dt_idx and dong_hao and dt_idx in dong_hao
        if dt_is_dong:
            score += 3
            factors.append("DT ĐỘNG (phát động) +3")
        else:
            score -= 2
            factors.append("DT TĨNH (chờ đợi) -2")
        
        # ⑳ DT Trì Thế — DT cùng hào với Thế
        the_idx_found = None
        for i, hao in enumerate(haos):
            if hao.get('the_ung') == 'Thế':
                the_idx_found = i + 1
                break
        if dt_idx and the_idx_found and dt_idx == the_idx_found:
            score += 4
            factors.append("DT TRÌ THẾ +4")
        
        # ㉑ Nguyên Thần bị Kỵ Thần khắc — chain effect
        if dt_hanh:
            nguyen_hanh_list = [h for h, s in SINH.items() if s == dt_hanh]
            ky_hanh_list2 = [h for h, k in KHAC.items() if k == dt_hanh]
            nt_found = None
            kt_found = None
            for hao in haos:
                h_hanh = hao.get('ngu_hanh', '')
                if h_hanh in nguyen_hanh_list and hao != dt_hao:
                    nt_found = hao
                if h_hanh in ky_hanh_list2 and hao != dt_hao:
                    kt_found = hao
            if nt_found and kt_found:
                nt_hanh = nt_found.get('ngu_hanh', '')
                kt_hanh = kt_found.get('ngu_hanh', '')
                if KHAC.get(kt_hanh) == nt_hanh:
                    kt_idx = haos.index(kt_found) + 1
                    if kt_idx in (dong_hao or []):
                        score -= 5
                        factors.append(f"KT({kt_hanh}) động khắc NT({nt_hanh}) → DT mất nguồn -5")
                    else:
                        score -= 3
                        factors.append(f"KT({kt_hanh}) khắc NT({nt_hanh}) → chain -3")
                        
                # ㉒ THAM SINH VONG KHẮC — KT + NT cùng ĐỘNG → KT tham sinh NT → quên khắc DT → HÓA CÁT!
                if nt_found and kt_found and dong_hao:
                    nt_idx_chk = haos.index(nt_found) + 1
                    kt_idx_chk = haos.index(kt_found) + 1
                    if nt_idx_chk in dong_hao and kt_idx_chk in dong_hao:
                        # KT sinh NT? (VD: KT=Mộc, NT=Hỏa → Mộc sinh Hỏa → KT tham sinh)
                        nt_h = nt_found.get('ngu_hanh', '')
                        kt_h = kt_found.get('ngu_hanh', '')
                        if SINH.get(kt_h) == nt_h:
                            score += 10
                            factors.append(f"⚡ THAM SINH VONG KHẮC: KT({kt_h}) tham sinh NT({nt_h}) → quên khắc DT → HÓA CÁT +10")
        
        # ㉓ Vị trí hào DT (ý nghĩa ngữ cảnh)
        if dt_idx:
            if dt_idx == 6:
                score += 2
                factors.append("DT ở hào 6 (cao, xa, khó) +2")
            elif dt_idx == 5:
                score += 2
                factors.append("DT ở hào 5 (quân vương, trung tâm) +2")
            elif dt_idx == 1:
                score -= 2
                factors.append("DT ở hào 1 (thấp, yếu, mới bắt đầu) -2")
        
        # ═══════════════════════════════════════════════════════════
        # V26.2: STRENGTH LABEL với thang điểm mở rộng
        # ═══════════════════════════════════════════════════════════
        if score >= 25: strength = "🟢 CỰC VƯỢNG"
        elif score >= 15: strength = "🟢 VƯỢNG"
        elif score >= 5: strength = "🔵 TƯỚNG"
        elif score >= -5: strength = "🟡 BÌNH"
        elif score >= -15: strength = "🟠 SUY"
        elif score >= -25: strength = "🟠 RẤT YẾU"
        else: strength = "🔴 TỬ"
        
        summary = f"LH Điểm={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:6])}{'...' if len(factors) > 6 else ''})"
        return score, summary, factors
    
    def _mai_hoa_scoring(self, mai_hoa_data, chart_data=None):
        """V26.2: Chấm điểm Mai Hoa — 8 tầng scoring. Bổ sung Nhật/Nguyệt/Tỷ Hòa."""
        if not mai_hoa_data or not isinstance(mai_hoa_data, dict):
            return 0, "Không có dữ liệu Mai Hoa", []
        
        try:
            from mai_hoa_dich_so import QUAI_ELEMENTS, QUAI_NAMES
        except ImportError:
            return 0, "Thiếu module mai_hoa_dich_so", []
        
        score = 0
        factors = []
        
        dong_hao = mai_hoa_data.get('dong_hao', 1)
        upper = mai_hoa_data.get('upper', 0)
        lower = mai_hoa_data.get('lower', 0)
        
        if dong_hao <= 3:
            the_quai, dung_quai = upper, lower
        else:
            the_quai, dung_quai = lower, upper
        
        the_el = QUAI_ELEMENTS.get(the_quai, '')
        dung_el = QUAI_ELEMENTS.get(dung_quai, '')
        the_name = QUAI_NAMES.get(the_quai, '?')
        
        if not the_el or not dung_el:
            return 0, "Thiếu Ngũ Hành Thể/Dụng", []
        
        # ① Thể↔Dụng sinh khắc (±10)
        if SINH.get(dung_el) == the_el:
            score += 10
            factors.append(f"MH Dụng sinh Thể +10")
        elif KHAC.get(dung_el) == the_el:
            score -= 10
            factors.append(f"MH Dụng khắc Thể -10")
        elif KHAC.get(the_el) == dung_el:
            score += 8
            factors.append(f"MH Thể khắc Dụng (thuận lợi) +8")
        elif SINH.get(the_el) == dung_el:
            score -= 5
            factors.append(f"MH Thể sinh Dụng (hao mòn) -5")
        else:
            score += 2
            factors.append(f"MH Tỷ Hòa +2")
        
        # ② Hỗ Quái sinh/khắc Thể (±8)
        ho_name = mai_hoa_data.get('ten_ho', '')
        if ho_name:
            ho_yn = QUAI_Y_NGHIA.get(ho_name, {})
            ho_el = ho_yn.get('hanh', '')
            if ho_el and the_el:
                if SINH.get(ho_el) == the_el:
                    score += 8
                    factors.append(f"MH Hỗ sinh Thể +8")
                elif KHAC.get(ho_el) == the_el:
                    score -= 8
                    factors.append(f"MH Hỗ khắc Thể -8")
        
        # ③ Biến Quái sinh/khắc Thể (±8)
        ten_bien = mai_hoa_data.get('ten_qua_bien', '')
        if ten_bien:
            for bp in ten_bien.split():
                bien_yn = QUAI_Y_NGHIA.get(bp, {})
                if bien_yn:
                    bien_el = bien_yn.get('hanh', '')
                    if bien_el and the_el:
                        if SINH.get(bien_el) == the_el:
                            score += 8
                            factors.append(f"MH Biến sinh Thể +8")
                        elif KHAC.get(bien_el) == the_el:
                            score -= 8
                            factors.append(f"MH Biến khắc Thể -8")
                    break
        
        # ④ Nguyệt lệnh (±6)
        lenh_hanh, lenh_mua = _get_lenh_thang_hanh()
        if the_el and lenh_hanh:
            if the_el == lenh_hanh:
                score += 5
                factors.append(f"MH Thể đắc lệnh (Tháng) +5")
            elif SINH.get(lenh_hanh) == the_el:
                score += 3
                factors.append(f"MH Tháng sinh Thể +3")
            elif KHAC.get(lenh_hanh) == the_el:
                score -= 5
                factors.append(f"MH Thể bị Tháng khắc (Thất lệnh) -5")
                
        # ⑤ Nhật Thần (±6) - V26.2 thêm vào
        if chart_data and isinstance(chart_data, dict):
            chi_ngay = chart_data.get('chi_ngay', '')
            ngay_hanh = CHI_NGU_HANH.get(chi_ngay, '')
            if ngay_hanh and the_el:
                if the_el == ngay_hanh:
                    score += 5
                    factors.append(f"MH Thể vượng tại Ngày +5")
                elif SINH.get(ngay_hanh) == the_el:
                    score += 4
                    factors.append(f"MH Ngày sinh Thể +4")
                elif KHAC.get(ngay_hanh) == the_el:
                    score -= 6
                    factors.append(f"MH Ngày khắc Thể -6")
        
        # ⑥ Quái Tượng 64 quẻ (±5)
        ten_que = mai_hoa_data.get('ten', '')
        if ten_que and KINH_DICH_64:
            for k, v in KINH_DICH_64.items():
                if k in ten_que or ten_que in k:
                    cat_hung = v.get('cat_hung', '')
                    if 'Cát' in cat_hung or 'Hanh' in cat_hung:
                        score += 5
                        factors.append(f"MH Quẻ {ten_que} Cát +5")
                    elif 'Hung' in cat_hung or 'Nguy' in cat_hung:
                        score -= 5
                        factors.append(f"MH Quẻ {ten_que} Hung -5")
                    break
        
        # Strength label
        if score >= 15: strength = "🟢 CỰC VƯỢNG"
        elif score >= 5: strength = "🔵 TƯỚNG"
        elif score >= -5: strength = "🟡 BÌNH"
        elif score >= -15: strength = "🟠 SUY"
        else: strength = "🔴 TỬ"
        
        summary = f"MH Thể={the_name}({the_el}), Điểm={score}, {strength} ({len(factors)} yếu: {', '.join(factors[:3])}...)"
        
        # V27.0: Enrichment tu ICHING_HEXAGRAMS (64 que chi tiet)
        if ICHING_HEXAGRAMS:
            try:
                hex_num = None
                if mai_hoa_data and isinstance(mai_hoa_data, dict):
                    hex_num = mai_hoa_data.get('que_so') or mai_hoa_data.get('hex_number')
                if hex_num and hex_num in ICHING_HEXAGRAMS:
                    ic = ICHING_HEXAGRAMS[hex_num]
                    cat_key = topic.lower() if topic else 'general'
                    # Map topic to ICHING key
                    topic_map = {
                        'tai_chinh': 'fortune', 'tinh_cam': 'love', 'hon_nhan': 'love',
                        'cong_viec': 'career', 'suc_khoe': 'sickness', 'benh_tat': 'sickness',
                        'tim_do': 'lost_item', 'mat_do': 'lost_item',
                    }
                    ic_key = topic_map.get(cat_key, 'general')
                    ic_text = ic.get(ic_key, ic.get('general', ''))
                    if ic_text:
                        factors.append(f"[KINH DỊCH] Que {ic.get('name','?')}: {str(ic_text)[:200]}")
                        if 'cat' in str(ic_text).lower() or 'hanh' in str(ic_text).lower():
                            score += 3
                        elif 'hung' in str(ic_text).lower() or 'nan' in str(ic_text).lower():
                            score -= 3
            except Exception:
                pass

        return score, summary, factors
    
    def _thiet_ban_scoring(self, chart_data, luc_hao_data, mai_hoa_data):
        """V41.0: Chấm điểm Thiết Bản — 7 tiêu chí, luôn >= 3 yếu tố.
        
        FIX: NAP_AM_GIAI_THICH dùng tên Nạp Âm làm key nhưng code lookup bằng CanChi
        → Thêm bảng 60 Giáp Tý Nạp Âm chuẩn để tra ngược.
        """
        score = 0
        factors = []
        
        can_ngay = ''
        chi_ngay = ''
        chi_nam = ''
        can_hanh = ''
        
        # === BẢNG 60 GIÁP TỬ NẠP ÂM (Chính xác theo cổ thư) ===
        _NAP_AM_60 = {
            'GiápTý': ('Hải Trung Kim', 'Kim'), 'ẤtSửu': ('Hải Trung Kim', 'Kim'),
            'BínhDần': ('Lô Trung Hỏa', 'Hỏa'), 'ĐinhMão': ('Lô Trung Hỏa', 'Hỏa'),
            'MậuThìn': ('Đại Lâm Mộc', 'Mộc'), 'KỷTị': ('Đại Lâm Mộc', 'Mộc'),
            'CanhNgọ': ('Lộ Bàng Thổ', 'Thổ'), 'TânMùi': ('Lộ Bàng Thổ', 'Thổ'),
            'NhâmThân': ('Kiếm Phong Kim', 'Kim'), 'QuýDậu': ('Kiếm Phong Kim', 'Kim'),
            'GiápTuất': ('Sơn Đầu Hỏa', 'Hỏa'), 'ẤtHợi': ('Sơn Đầu Hỏa', 'Hỏa'),
            'BínhTý': ('Giản Hạ Thủy', 'Thủy'), 'ĐinhSửu': ('Giản Hạ Thủy', 'Thủy'),
            'MậuDần': ('Thành Đầu Thổ', 'Thổ'), 'KỷMão': ('Thành Đầu Thổ', 'Thổ'),
            'CanhThìn': ('Bạch Lạp Kim', 'Kim'), 'TânTị': ('Bạch Lạp Kim', 'Kim'),
            'NhâmNgọ': ('Dương Liễu Mộc', 'Mộc'), 'QuýMùi': ('Dương Liễu Mộc', 'Mộc'),
            'GiápThân': ('Tuyền Trung Thủy', 'Thủy'), 'ẤtDậu': ('Tuyền Trung Thủy', 'Thủy'),
            'BínhTuất': ('Ốc Thượng Thổ', 'Thổ'), 'ĐinhHợi': ('Ốc Thượng Thổ', 'Thổ'),
            'MậuTý': ('Tích Lịch Hỏa', 'Hỏa'), 'KỷSửu': ('Tích Lịch Hỏa', 'Hỏa'),
            'CanhDần': ('Tùng Bách Mộc', 'Mộc'), 'TânMão': ('Tùng Bách Mộc', 'Mộc'),
            'NhâmThìn': ('Trường Lưu Thủy', 'Thủy'), 'QuýTị': ('Trường Lưu Thủy', 'Thủy'),
            'GiápNgọ': ('Sa Trung Kim', 'Kim'), 'ẤtMùi': ('Sa Trung Kim', 'Kim'),
            'BínhThân': ('Sơn Hạ Hỏa', 'Hỏa'), 'ĐinhDậu': ('Sơn Hạ Hỏa', 'Hỏa'),
            'MậuTuất': ('Bình Địa Mộc', 'Mộc'), 'KỷHợi': ('Bình Địa Mộc', 'Mộc'),
            'CanhTý': ('Bích Thượng Thổ', 'Thổ'), 'TânSửu': ('Bích Thượng Thổ', 'Thổ'),
            'NhâmDần': ('Kim Bạc Kim', 'Kim'), 'QuýMão': ('Kim Bạc Kim', 'Kim'),
            'GiápThìn': ('Phúc Đăng Hỏa', 'Hỏa'), 'ẤtTị': ('Phúc Đăng Hỏa', 'Hỏa'),
            'BínhNgọ': ('Thiên Hà Thủy', 'Thủy'), 'ĐinhMùi': ('Thiên Hà Thủy', 'Thủy'),
            'MậuThân': ('Đại Trạch Thổ', 'Thổ'), 'KỷDậu': ('Đại Trạch Thổ', 'Thổ'),
            'CanhTuất': ('Thoa Xuyến Kim', 'Kim'), 'TânHợi': ('Thoa Xuyến Kim', 'Kim'),
            'NhâmTý': ('Tang Đố Mộc', 'Mộc'), 'QuýSửu': ('Tang Đố Mộc', 'Mộc'),
            'GiápDần': ('Đại Khê Thủy', 'Thủy'), 'ẤtMão': ('Đại Khê Thủy', 'Thủy'),
            'BínhThìn': ('Sa Trung Thổ', 'Thổ'), 'ĐinhTị': ('Sa Trung Thổ', 'Thổ'),
            'MậuNgọ': ('Thiên Thượng Hỏa', 'Hỏa'), 'KỷMùi': ('Thiên Thượng Hỏa', 'Hỏa'),
            'CanhThân': ('Thạch Lựu Mộc', 'Mộc'), 'TânDậu': ('Thạch Lựu Mộc', 'Mộc'),
            'NhâmTuất': ('Đại Hải Thủy', 'Thủy'), 'QuýHợi': ('Đại Hải Thủy', 'Thủy'),
        }
        
        # Nạp Âm MẠNH/YẾU phân loại (theo cổ thư Thiết Bản)
        _NAP_AM_STRENGTH = {
            'Đại Lâm Mộc': 8, 'Đại Hải Thủy': 8, 'Thiên Thượng Hỏa': 8,  # Cực mạnh
            'Kiếm Phong Kim': 6, 'Tùng Bách Mộc': 6, 'Thiên Hà Thủy': 6,  # Mạnh
            'Đại Khê Thủy': 5, 'Thạch Lựu Mộc': 5, 'Thành Đầu Thổ': 5,   # Khá mạnh
            'Trường Lưu Thủy': 4, 'Bình Địa Mộc': 4, 'Ốc Thượng Thổ': 4, # Trung bình khá
            'Hải Trung Kim': 3, 'Sa Trung Kim': 3, 'Tuyền Trung Thủy': 3, # Ẩn giấu
            'Sơn Đầu Hỏa': 2, 'Tích Lịch Hỏa': 2, 'Đại Trạch Thổ': 2,   # Bình
            'Lô Trung Hỏa': 1, 'Giản Hạ Thủy': 1, 'Lộ Bàng Thổ': 1,     # Yếu
            'Sơn Hạ Hỏa': 0, 'Tang Đố Mộc': 0, 'Sa Trung Thổ': 0,       # Yếu thể
            'Bạch Lạp Kim': -1, 'Kim Bạc Kim': -1, 'Dương Liễu Mộc': -1, # Mỏng manh
            'Phúc Đăng Hỏa': -2, 'Bích Thượng Thổ': -2, 'Thoa Xuyến Kim': -2, # Khá yếu
        }
        
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            chi_ngay = chart_data.get('chi_ngay', '')
            chi_nam = chart_data.get('chi_nam', '')
            can_hanh = CAN_NGU_HANH.get(can_ngay, '')
        
        # ① NẠP ÂM NGÀY — Tra bảng 60 Giáp Tý (±5)
        nap_am_ten = ''
        nap_am_hanh = ''
        can_chi_key = can_ngay + chi_ngay if can_ngay and chi_ngay else ''
        if can_chi_key and can_chi_key in _NAP_AM_60:
            nap_am_ten, nap_am_hanh = _NAP_AM_60[can_chi_key]
            na_str = _NAP_AM_STRENGTH.get(nap_am_ten, 0)
            na_desc = NAP_AM_GIAI_THICH.get(nap_am_ten, nap_am_ten)
            if na_str >= 5:
                score += 5
                factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] MẠNH ({na_desc}) +5")
            elif na_str >= 2:
                score += 2
                factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] TRUNG ({na_desc}) +2")
            elif na_str <= -1:
                score -= 3
                factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] YẾU ({na_desc}) -3")
            else:
                score += 0
                factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] BÌNH ({na_desc}) +0")
        elif can_ngay and chi_ngay:
            # Fallback: Nạp Âm từ chart_data
            nap_am_ten = chart_data.get('nap_am', chart_data.get('nap_am_ten', '')) if chart_data else ''
            nap_am_hanh = chart_data.get('nap_am_hanh', '') if chart_data else ''
            if nap_am_ten and nap_am_ten != '?':
                na_str = _NAP_AM_STRENGTH.get(nap_am_ten, 0)
                if na_str >= 5:
                    score += 5
                    factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] MẠNH +5")
                elif na_str <= -1:
                    score -= 3
                    factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] YẾU -3")
                else:
                    factors.append(f"TB-1 Nạp Âm [{nap_am_ten}] BÌNH +0")
        
        # ② NẠP ÂM vs DỤNG THẦN HÀNH — Sinh Khắc (±4)
        if nap_am_hanh and can_hanh:
            if SINH.get(nap_am_hanh) == can_hanh:
                score += 4
                factors.append(f"TB-2 Nạp Âm({nap_am_hanh}) SINH Mệnh({can_hanh}) +4")
            elif KHAC.get(nap_am_hanh) == can_hanh:
                score -= 4
                factors.append(f"TB-2 Nạp Âm({nap_am_hanh}) KHẮC Mệnh({can_hanh}) -4")
            elif nap_am_hanh == can_hanh:
                score += 2
                factors.append(f"TB-2 Nạp Âm Tỷ Hòa Mệnh +2")
            elif SINH.get(can_hanh) == nap_am_hanh:
                score -= 1
                factors.append(f"TB-2 Mệnh TIẾT KHÍ cho Nạp Âm -1")
            else:
                factors.append(f"TB-2 Nạp Âm({nap_am_hanh}) ↔ Mệnh({can_hanh}) Bình hòa +0")
        
        # ③ THIÊN ĐỊA SINH KHẮC — Can Ngày vs Chi Ngày (±4)
        chi_hanh = CHI_NGU_HANH.get(chi_ngay, '')
        if can_hanh and chi_hanh:
            if SINH.get(chi_hanh) == can_hanh:
                score += 4
                factors.append(f"TB-3 Địa Chi({chi_ngay}/{chi_hanh}) SINH Thiên Can({can_ngay}/{can_hanh}) +4")
            elif KHAC.get(chi_hanh) == can_hanh:
                score -= 4
                factors.append(f"TB-3 Địa Chi({chi_ngay}/{chi_hanh}) KHẮC Thiên Can({can_ngay}/{can_hanh}) -4")
            elif can_hanh == chi_hanh:
                score += 2
                factors.append(f"TB-3 Thiên Địa Tỷ Hòa({can_hanh}) +2")
        
        # ④ THÁI TUẾ (Lưu Niên) sinh khắc Mệnh Chủ (±6)
        if can_ngay and chi_nam:
            nam_hanh = CHI_NGU_HANH.get(chi_nam, '')
            if can_hanh and nam_hanh:
                if SINH.get(nam_hanh) == can_hanh:
                    score += 6
                    factors.append(f"TB-4 Thái Tuế({chi_nam}/{nam_hanh}) SINH Mệnh +6")
                elif KHAC.get(nam_hanh) == can_hanh:
                    score -= 6
                    factors.append(f"TB-4 Thái Tuế({chi_nam}/{nam_hanh}) KHẮC Mệnh -6")
                elif nam_hanh == can_hanh:
                    score += 3
                    factors.append(f"TB-4 Mệnh đắc Thái Tuế +3")
        
        # ⑤ 12 TRƯỜNG SINH — Mệnh tại Chi Ngày (±8)
        if can_hanh and chi_ngay:
            ts_stage, ts_explain = _get_truong_sinh(can_hanh, chi_ngay)
            if ts_stage:
                if ts_stage in ['Đế Vượng', 'Lâm Quan', 'Trường Sinh']:
                    score += 8
                    factors.append(f"TB-5 12TrSinh Mệnh ở [{ts_stage}] CỰC VƯỢNG +8")
                elif ts_stage in ['Quan Đới', 'Mộc Dục']:
                    score += 4
                    factors.append(f"TB-5 12TrSinh Mệnh ở [{ts_stage}] KHÁ +4")
                elif ts_stage in ['Tử', 'Mộ', 'Tuyệt']:
                    score -= 8
                    factors.append(f"TB-5 12TrSinh Mệnh ở [{ts_stage}] CỰC SUY -8")
                elif ts_stage in ['Suy', 'Bệnh']:
                    score -= 4
                    factors.append(f"TB-5 12TrSinh Mệnh ở [{ts_stage}] SUY -4")
                elif ts_stage == 'Thai':
                    score += 1
                    factors.append(f"TB-5 12TrSinh Mệnh ở [Thai] khởi đầu mới +1")
                elif ts_stage == 'Dưỡng':
                    score += 2
                    factors.append(f"TB-5 12TrSinh Mệnh ở [Dưỡng] đang nuôi dưỡng +2")
        
        # ⑥ QUẺ TƯỢNG Cát Hung (±5)
        que_name = ''
        if luc_hao_data:
            que_name = luc_hao_data.get('ban', {}).get('name', '')
        if not que_name and mai_hoa_data:
            que_name = mai_hoa_data.get('ten', '')
        if que_name and KINH_DICH_64:
            for k, v in KINH_DICH_64.items():
                if k in que_name or que_name in k:
                    cat_hung = v.get('cat_hung', '')
                    if 'Cát' in cat_hung:
                        score += 5
                        factors.append(f"TB-6 Quẻ [{que_name}] Cát +5")
                    elif 'Hung' in cat_hung:
                        score -= 5
                        factors.append(f"TB-6 Quẻ [{que_name}] Hung -5")
                    else:
                        factors.append(f"TB-6 Quẻ [{que_name}] Bình +0")
                    break
        
        # ⑦ MÙA VƯỢNG SUY — Mệnh Hành vs Mùa hiện tại (±3)
        try:
            mua_hanh, mua_ten = _get_lenh_thang_hanh()
            if mua_hanh and can_hanh:
                if mua_hanh == can_hanh:
                    score += 3
                    factors.append(f"TB-7 Mệnh({can_hanh}) ĐẮCL LỆNH {mua_ten} +3")
                elif SINH.get(mua_hanh) == can_hanh:
                    score += 2
                    factors.append(f"TB-7 Mệnh({can_hanh}) được {mua_ten}({mua_hanh}) sinh +2")
                elif KHAC.get(mua_hanh) == can_hanh:
                    score -= 3
                    factors.append(f"TB-7 Mệnh({can_hanh}) bị {mua_ten}({mua_hanh}) khắc -3")
        except Exception:
            pass
        
        # === VERDICT ===
        if score >= 12: strength = "🟢 CỰC VƯỢNG"
        elif score >= 5: strength = "🔵 TƯỚNG"
        elif score >= -3: strength = "🟡 BÌNH"
        elif score >= -8: strength = "🟠 SUY"
        else: strength = "🔴 TỬ TUYỆT"
        
        summary = f"TB Điểm={score}, {strength} ({len(factors)} yếu tố: {' | '.join(factors[:4])})"
        
        # V27.0: Bổ sung Đại Vận/Lưu Niên từ JSON (nếu có)
        try:
            import datetime as _dt_tb
            current_year = _dt_tb.datetime.now().year
            import json as _json_tb
            tb_json_path = os.path.join(os.path.dirname(__file__), 'thiet_ban_than_toan.json')
            if os.path.exists(tb_json_path):
                with open(tb_json_path, 'r', encoding='utf-8') as _f:
                    tb_json = _json_tb.load(_f)
                    luu_nien = tb_json.get('luu_nien', {}).get(str(current_year), {})
                    if luu_nien:
                        ln_hanh = luu_nien.get('hanh', '')
                        if ln_hanh and can_hanh:
                            if SINH.get(ln_hanh) == can_hanh:
                                score += 4
                                factors.append(f"TB-X Lưu Niên {current_year} sinh Mệnh +4")
                            elif KHAC.get(ln_hanh) == can_hanh:
                                score -= 4
                                factors.append(f"TB-X Lưu Niên {current_year} khắc Mệnh -4")
        except Exception:
            pass

        return score, summary, factors
    
    def _luc_nham_scoring(self, chart_data):
        """V16.0: Chấm điểm Đại Lục Nhâm — Tam Truyền + Thiên Tướng + Tuần Không."""
        if not chart_data or not isinstance(chart_data, dict):
            return 0, "Không có chart_data", []
        
        score = 0
        factors = []
        
        try:
            from dai_luc_nham import tinh_dai_luc_nham, phan_tich_chuyen_sau, tinh_tuan_khong, CHI_NGU_HANH as LN_CHI_HANH
        except ImportError:
            return 0, "Thiếu module dai_luc_nham", []
        
        can_ngay = chart_data.get('can_ngay', 'Giáp')
        chi_ngay = chart_data.get('chi_ngay', 'Tý')
        chi_gio = chart_data.get('chi_gio', 'Ngọ')
        tiet_khi = chart_data.get('tiet_khi', 'Đông Chí')
        
        try:
            ln_data = tinh_dai_luc_nham(can_ngay, chi_ngay, chi_gio, tiet_khi)
            tam_truyen = ln_data.get('tam_truyen', {})
            can_hanh = CAN_NGU_HANH.get(can_ngay, '')
            
            # ① Sơ Truyền ↔ Can Ngày (±8)
            so_hanh = tam_truyen.get('so_truyen_hanh', '')
            if so_hanh and can_hanh:
                if SINH.get(so_hanh) == can_hanh:
                    score += 8
                    factors.append(f"LN Sơ Truyền sinh Can +8")
                elif KHAC.get(so_hanh) == can_hanh:
                    score -= 8
                    factors.append(f"LN Sơ Truyền khắc Can -8")
                elif KHAC.get(can_hanh) == so_hanh:
                    score += 5
                    factors.append(f"LN Can khắc Sơ Truyền +5")
            
            # ② Mạt Truyền ↔ Can Ngày (±8) — kết quả
            mat_hanh = tam_truyen.get('mat_truyen_hanh', '')
            if mat_hanh and can_hanh:
                if SINH.get(mat_hanh) == can_hanh:
                    score += 8
                    factors.append(f"LN Mạt Truyền sinh Can +8 (KQ tốt)")
                elif KHAC.get(mat_hanh) == can_hanh:
                    score -= 8
                    factors.append(f"LN Mạt Truyền khắc Can -8 (KQ xấu)")
            
            # ③ Thiên Tướng Sơ Truyền (±5)
            thien_tuong = ln_data.get('thien_tuong_full', {})
            so_chi = tam_truyen.get('so_truyen', '')
            tuong = thien_tuong.get(so_chi, {})
            if tuong:
                cat_hung = tuong.get('cat_hung', '')
                if 'Cát' in cat_hung:
                    score += 5
                    factors.append(f"LN Thiên Tướng của Sơ Truyền Cát +5")
                elif 'Hung' in cat_hung:
                    score -= 5
                    factors.append(f"LN Thiên Tướng của Sơ Truyền Hung -5")
            
            # ④ Tuần Không (−12)
            tuan_khong = tinh_tuan_khong(can_ngay, chi_ngay)
            if so_chi in tuan_khong:
                score -= 12
                factors.append(f"LN Sơ Truyền rơi Tuần Không -12")
            
            # ⑤ Tam Truyền xu hướng (±4)
            trung_hanh = tam_truyen.get('trung_truyen_hanh', '')
            if so_hanh and mat_hanh:
                if SINH.get(so_hanh) == trung_hanh and SINH.get(trung_hanh) == mat_hanh:
                    score += 4
                    factors.append(f"LN Tam Truyền sinh tiến +4")
                elif so_hanh == trung_hanh == mat_hanh:
                    score += 2
                    factors.append(f"LN Tam Truyền đồng khí +2")
        except Exception:
            pass
        
        if score >= 12: strength = "🟢 CỰC VƯỢNG"
        elif score >= 4: strength = "🔵 TƯỚNG"
        elif score >= -4: strength = "🟡 BÌNH"
        elif score >= -12: strength = "🟠 SUY"
        else: strength = "🔴 TỬ"
        
        summary = f"LN Điểm={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V27.0: Bo sung Phan Tich Luc Nham
        # Factor: Sinh khac Tam Truyen voi Can Ngay (chi tiet hon)
        try:
            trung_hanh = tam_truyen.get('trung_truyen_hanh', '')
            mat_hanh = tam_truyen.get('mat_truyen_hanh', '')
            
            # Trung Truyen (Hien Tai) - trong so trung binh
            if trung_hanh and can_hanh:
                if SINH.get(trung_hanh) == can_hanh:
                    score += 5
                    factors.append(f"LN Trung Truyen sinh Can +5")
                elif KHAC.get(trung_hanh) == can_hanh:
                    score -= 5
                    factors.append(f"LN Trung Truyen khac Can -5")
            
            # Mat Truyen (Tuong Lai) - trong so thap
            if mat_hanh and can_hanh:
                if SINH.get(mat_hanh) == can_hanh:
                    score += 3
                    factors.append(f"LN Mat Truyen sinh Can +3 (tuong lai tot)")
                elif KHAC.get(mat_hanh) == can_hanh:
                    score -= 3
                    factors.append(f"LN Mat Truyen khac Can -3 (tuong lai xau)")
            
            # Thien Tuong
            thien_tuong = ln_data.get('thien_tuong', {})
            if thien_tuong:
                for tt_name, tt_val in thien_tuong.items():
                    if isinstance(tt_val, dict) and tt_val.get('cat_hung'):
                        ch = str(tt_val['cat_hung'])
                        if 'Cat' in ch or 'Cát' in ch:
                            score += 2
                            factors.append(f"LN Thien Tuong {tt_name} Cat +2")
                        elif 'Hung' in ch:
                            score -= 2
                            factors.append(f"LN Thien Tuong {tt_name} Hung -2")
                        if len(factors) > 20:
                            break
        except Exception:
            pass

        # V28.8: BỔ SUNG THẦN SÁT ĐẠI LỤC NHÂM
        try:
            # ⑥ DỊCH MÃ trong Tam Truyền (±4) — chỉ sự di chuyển, tốc độ
            DICH_MA_MAP = {
                'Thân': 'Dần', 'Tý': 'Dần', 'Thìn': 'Dần',
                'Dần': 'Thân', 'Ngọ': 'Thân', 'Tuất': 'Thân',
                'Tỵ': 'Hợi', 'Dậu': 'Hợi', 'Sửu': 'Hợi',
                'Hợi': 'Tỵ', 'Mão': 'Tỵ', 'Mùi': 'Tỵ'
            }
            chi_ma_ln = DICH_MA_MAP.get(chi_ngay, '')
            if chi_ma_ln:
                so_chi = tam_truyen.get('so_truyen', '')
                trung_chi = tam_truyen.get('trung_truyen', '')
                mat_chi = tam_truyen.get('mat_truyen', '')
                if chi_ma_ln in (so_chi, trung_chi, mat_chi):
                    score += 4
                    truyen_name = 'Sơ' if chi_ma_ln == so_chi else ('Trung' if chi_ma_ln == trung_chi else 'Mạt')
                    factors.append(f"LN Dịch Mã nhập {truyen_name} Truyền → tốc độ NHANH +4")
            
            # ⑦ LỘC THẦN trong Tam Truyền (+5) — chỉ tài lộc, phúc đức
            LOC_THAN_MAP = {
                'Giáp': 'Dần', 'Ất': 'Mão', 'Bính': 'Tỵ', 'Đinh': 'Ngọ',
                'Mậu': 'Tỵ', 'Kỷ': 'Ngọ', 'Canh': 'Thân', 'Tân': 'Dậu',
                'Nhâm': 'Hợi', 'Quý': 'Tý'
            }
            loc_chi = LOC_THAN_MAP.get(can_ngay, '')
            if loc_chi:
                so_chi = tam_truyen.get('so_truyen', '')
                trung_chi = tam_truyen.get('trung_truyen', '')
                mat_chi = tam_truyen.get('mat_truyen', '')
                if loc_chi in (so_chi, trung_chi, mat_chi):
                    score += 5
                    truyen_name = 'Sơ' if loc_chi == so_chi else ('Trung' if loc_chi == trung_chi else 'Mạt')
                    factors.append(f"LN Lộc Thần nhập {truyen_name} Truyền → TÀI LỘC +5")
            
            # ⑧ Mạt Truyền lâm Tuần Không (-8) — kết quả trống rỗng
            mat_chi = tam_truyen.get('mat_truyen', '')
            if mat_chi and mat_chi in tuan_khong:
                score -= 8
                factors.append(f"LN Mạt Truyền Tuần Không → KQ trống rỗng -8")
            
            # ⑨ Trung Truyền lâm Tuần Không (-4)
            trung_chi = tam_truyen.get('trung_truyen', '')
            if trung_chi and trung_chi in tuan_khong:
                score -= 4
                factors.append(f"LN Trung Truyền Tuần Không → quá trình gián đoạn -4")
            
            # ⑩ KHÓA THỂ — xác định dạng quẻ (thông tin ngữ cảnh)
            khoa_the = ln_data.get('khoa_the', '')
            if khoa_the:
                factors.append(f"LN Khóa Thể: {str(khoa_the)[:60]}")
            
            # ⑪ Tam Truyền → VẠN VẬT LOẠI TƯỢNG (mapping chi → Bát Quái → đồ vật)
            CHI_BAT_QUAI = {
                'Tý': 'Khảm', 'Sửu': 'Cấn', 'Dần': 'Cấn', 'Mão': 'Chấn',
                'Thìn': 'Tốn', 'Tỵ': 'Tốn', 'Ngọ': 'Ly', 'Mùi': 'Khôn',
                'Thân': 'Khôn', 'Dậu': 'Đoài', 'Tuất': 'Càn', 'Hợi': 'Càn'
            }
            so_chi = tam_truyen.get('so_truyen', '')
            mat_chi = tam_truyen.get('mat_truyen', '')
            if so_chi:
                quai_so = CHI_BAT_QUAI.get(so_chi, '')
                if quai_so:
                    factors.append(f"LN Sơ Truyền({so_chi})={quai_so} → nguồn gốc/khởi đầu")
            if mat_chi:
                quai_mat = CHI_BAT_QUAI.get(mat_chi, '')
                if quai_mat:
                    factors.append(f"LN Mạt Truyền({mat_chi})={quai_mat} → kết quả/đích đến")
        except Exception:
            pass

        return score, summary, factors
    
    def _thai_at_scoring(self, chart_data):
        """V16.0: Chấm điểm Thái Ất — Chủ↔Khách + Văn Xương + Cách Cục."""
        if not chart_data or not isinstance(chart_data, dict):
            return 0, "Không có chart_data", []
        
        score = 0
        factors = []
        
        try:
            from thai_at_than_so import tinh_thai_at_than_so
            import datetime as _dt
            now = _dt.datetime.now()
            can_ngay = chart_data.get('can_ngay', 'Giáp')
            chi_ngay = chart_data.get('chi_ngay', 'Tý')
            ta_data = tinh_thai_at_than_so(now.year, now.month, can_ngay, chi_ngay)
            
            luan_giai = ta_data.get('luan_giai', {})
            bat_tuong = ta_data.get('bat_tuong', {})
            cach_cuc = ta_data.get('cach_cuc', [])
            
            # ① Chủ↔Khách Đại Tướng (±10)
            chu = bat_tuong.get('Chủ Đại Tướng', {})
            khach = bat_tuong.get('Khách Đại Tướng', {})
            if chu and khach:
                chu_h = chu.get('hanh_cung', '')
                khach_h = khach.get('hanh_cung', '')
                if chu_h and khach_h:
                    if KHAC.get(chu_h) == khach_h:
                        score += 10
                        factors.append(f"TA Chủ khắc Khách +10")
                    elif KHAC.get(khach_h) == chu_h:
                        score -= 10
                        factors.append(f"TA Khách khắc Chủ -10")
                    elif SINH.get(khach_h) == chu_h:
                        score += 5
                        factors.append(f"TA Khách sinh Chủ +5")
                    elif SINH.get(chu_h) == khach_h:
                        score -= 5
                        factors.append(f"TA Chủ sinh Khách -5")
            
            # ② Văn Xương ↔ Thái Ất (±6)
            van_xuong = bat_tuong.get('Văn Xương', {})
            ta_cung = ta_data.get('thai_at_cung', {})
            if van_xuong and ta_cung:
                vx_h = van_xuong.get('hanh_cung', '')
                ta_h = ta_cung.get('hanh_cung', '')
                if vx_h and ta_h:
                    if SINH.get(vx_h) == ta_h:
                        score += 6
                        factors.append(f"TA Văn Xương sinh Thái Ất +6")
                    elif KHAC.get(vx_h) == ta_h:
                        score -= 6
                        factors.append(f"TA Văn Xương khắc Thái Ất -6")
            
            # ③ Cách Cục (±4 mỗi cách)
            for cc in cach_cuc[:3]:
                if 'YỂM' in cc or 'KÍCH' in cc or 'TÙ' in cc:
                    score -= 4
                    factors.append(f"TA Cách cục Hung ({cc[:10]}...) -4")
                elif 'BẢO' in cc or 'HÒA' in cc:
                    score += 3
                    factors.append(f"TA Cách cục Cát ({cc[:10]}...) +3")
                elif 'CÁCH' in cc:
                    score -= 3
                    factors.append(f"TA Cách cục cản trở ({cc[:10]}...) -3")
            
            # ④ Bát Tướng Cát/Hung (±3)
            cat_count = sum(1 for t in bat_tuong.values() if t.get('cat_hung') in ('Cát', 'Đại Cát'))
            hung_count = sum(1 for t in bat_tuong.values() if t.get('cat_hung') in ('Hung', 'Đại Hung'))
            if cat_count > hung_count:
                score += 3
                factors.append(f"TA Bát Tướng đa Cát +3")
            elif hung_count > cat_count:
                score -= 3
                factors.append(f"TA Bát Tướng đa Hung -3")
        except Exception:
            pass
        
        if score >= 12: strength = "🟢 CỰC VƯỢNG"
        elif score >= 4: strength = "🔵 TƯỚNG"
        elif score >= -4: strength = "🟡 BÌNH"
        elif score >= -12: strength = "🟠 SUY"
        else: strength = "🔴 TỬ"
        
        summary = f"TA Điểm={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V27.0: Bo sung Thai At
        # Factor: Sinh khac voi Can Ngay
        try:
            ta_cung = ta_data.get('thai_at_cung', {})
            hanh_cung_ta = ta_cung.get('hanh_cung', '')
            can_h = CAN_NGU_HANH.get(can_ngay, '')
            if hanh_cung_ta and can_h:
                if SINH.get(hanh_cung_ta) == can_h:
                    score += 6
                    factors.append(f"TA Thai At sinh Can Ngay +6")
                elif KHAC.get(hanh_cung_ta) == can_h:
                    score -= 6
                    factors.append(f"TA Thai At khac Can Ngay -6")
                elif hanh_cung_ta == can_h:
                    score += 3
                    factors.append(f"TA Thai At dong hanh Can +3")
            
            # Bat Tuong diem
            if bat_tuong:
                cat_count = 0
                hung_count = 0
                for bt_name, bt_val in bat_tuong.items():
                    if isinstance(bt_val, dict):
                        ly = str(bt_val.get('ly', ''))
                        if 'Cat' in ly or 'Cát' in ly or 'tot' in ly.lower():
                            cat_count += 1
                        elif 'Hung' in ly or 'xau' in ly.lower():
                            hung_count += 1
                if cat_count > hung_count:
                    score += 4
                    factors.append(f"TA Bat Tuong Cat nhieu +4 ({cat_count}C/{hung_count}H)")
                elif hung_count > cat_count:
                    score -= 4
                    factors.append(f"TA Bat Tuong Hung nhieu -4 ({cat_count}C/{hung_count}H)")
        except Exception:
            pass

        # V28.8: BỔ SUNG THÁI ẤT
        try:
            # ⑤ THIÊN ẤT — tôn thần chủ chốt, vị trí quyết định đại cục
            thien_at = bat_tuong.get('Thiên Ất', bat_tuong.get('Thái Ất', {}))
            if thien_at and isinstance(thien_at, dict):
                ta_hanh_thien = thien_at.get('hanh_cung', '')
                can_h = CAN_NGU_HANH.get(can_ngay, '')
                if ta_hanh_thien and can_h:
                    if SINH.get(ta_hanh_thien) == can_h:
                        score += 6
                        factors.append(f"TA Thiên Ất sinh Can Ngày → ĐẠI CÁT +6")
                    elif KHAC.get(ta_hanh_thien) == can_h:
                        score -= 6
                        factors.append(f"TA Thiên Ất khắc Can Ngày → ĐẠI HUNG -6")
                    elif ta_hanh_thien == can_h:
                        score += 3
                        factors.append(f"TA Thiên Ất đồng hành Can → CÁT +3")
                ta_cat_hung = thien_at.get('cat_hung', '')
                if 'Cát' in str(ta_cat_hung):
                    score += 4
                    factors.append(f"TA Thiên Ất CÁT +4")
                elif 'Hung' in str(ta_cat_hung):
                    score -= 4
                    factors.append(f"TA Thiên Ất HUNG -4")
            
            # ⑥ THAM TƯỚNG Chủ/Khách — phụ tá cho Đại Tướng
            tham_chu = bat_tuong.get('Chủ Tham Tướng', bat_tuong.get('Tham Tướng Chủ', {}))
            tham_khach = bat_tuong.get('Khách Tham Tướng', bat_tuong.get('Tham Tướng Khách', {}))
            if tham_chu and isinstance(tham_chu, dict):
                tc_hanh = tham_chu.get('hanh_cung', '')
                chu_h = chu.get('hanh_cung', '') if chu else ''
                if tc_hanh and chu_h:
                    if SINH.get(tc_hanh) == chu_h:
                        score += 4
                        factors.append(f"TA Tham Tướng sinh Chủ → hỗ trợ +4")
                    elif KHAC.get(tc_hanh) == chu_h:
                        score -= 4
                        factors.append(f"TA Tham Tướng khắc Chủ → nội bộ bất hòa -4")
            
            # ⑦ DƯƠNG CỬU / BÁCH LỤC — hạn vận lớn
            duong_cuu = ta_data.get('duong_cuu', '')
            bach_luc = ta_data.get('bach_luc', '')
            if duong_cuu and 'hạn' in str(duong_cuu).lower():
                score -= 8
                factors.append(f"TA Dương Cửu hạn kỳ → tai ách -8")
            if bach_luc and 'hạn' in str(bach_luc).lower():
                score -= 8
                factors.append(f"TA Bách Lục hạn kỳ → tai họa -8")
            
            # ⑧ VĂN XƯƠNG chi tiết — vị trí + cát hung
            if van_xuong and isinstance(van_xuong, dict):
                vx_cung = van_xuong.get('cung', '')
                vx_ten = van_xuong.get('ten_cung', '')
                vx_cat = van_xuong.get('cat_hung', '')
                if vx_cung:
                    factors.append(f"TA Văn Xương tại cung {vx_cung}({vx_ten}) {'CÁT' if 'Cát' in str(vx_cat) else 'HUNG' if 'Hung' in str(vx_cat) else 'BÌNH'}")
                    if 'Cát' in str(vx_cat):
                        score += 3
                    elif 'Hung' in str(vx_cat):
                        score -= 3
            
            # ⑨ THÁI ẤT CUNG Không Vong (Tuần Không) (-6)
            ta_cung_so = ta_cung.get('cung', 0) if ta_cung else 0
            CUNG_CHI_TA = {1: 'Tý', 2: 'Sửu', 3: 'Dần', 4: 'Mão', 5: None, 6: 'Tuất', 7: 'Dậu', 8: 'Thìn', 9: 'Ngọ'}
            ta_chi_mapped = CUNG_CHI_TA.get(int(ta_cung_so) if ta_cung_so else 0, '')
            khong_vong_ta = _get_khong_vong(can_ngay, chi_ngay) if can_ngay and chi_ngay else []
            if ta_chi_mapped and ta_chi_mapped in khong_vong_ta:
                score -= 6
                factors.append(f"TA Thái Ất Cung lâm Không Vong → trì trệ -6")
        except Exception:
            pass

        return score, summary, factors
    
    # ═══════════════════════════════════════════════════════════
    # V17.0: LỤC THUẬT PHÂN CẤP — ROUTING + ĐỐI CHIẾU %
    # ═══════════════════════════════════════════════════════════
    
    def _get_method_routing(self, category_label, verdicts, scores):
        """V17.0: Xác định PP CHÍNH + đối chiếu % giữa 6 PP.
        
        Args:
            category_label: Nhóm câu hỏi (VD: 'TÀI CHÍNH')
            verdicts: dict {ky_mon: 'CÁT', luc_hao: 'HUNG', ...}
            scores: dict {ky_mon: 23, luc_hao: 18, ...} (V16 scores)
        
        Returns:
            dict with primary_method, weighted_scores, consensus, routing_text
        """
        # Map category to strength key
        strength_key = CATEGORY_TO_STRENGTH.get(category_label.upper(), 'tổng_quát')
        strengths = METHOD_STRENGTH_MAP.get(strength_key, METHOD_STRENGTH_MAP['tổng_quát'])
        
        # Tính Weighted Score = V16 Score × Trọng số ÷ 100
        weighted = {}
        for method, weight in strengths.items():
            raw_score = scores.get(method, 0)
            # Normalize: score có thể âm, ta dùng abs + sign để giữ hướng
            weighted[method] = round(raw_score * weight / 100, 1)
        
        # PP CHÍNH = weighted cao nhất (dương nhất)
        sorted_methods = sorted(weighted.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_methods[0][0]
        primary_weight = strengths[primary]
        
        # Đối chiếu: bao nhiêu PP đồng ý (CÁT vs HUNG)
        cat_count = sum(1 for v in verdicts.values() if v in ('CÁT', 'ĐẠI CÁT'))
        hung_count = sum(1 for v in verdicts.values() if v in ('HUNG', 'ĐẠI HUNG'))
        total = len(verdicts)
        
        primary_verdict = verdicts.get(primary, 'BÌNH')
        if primary_verdict in ('CÁT', 'ĐẠI CÁT'):
            consensus_pct = round(cat_count / total * 100) if total else 0
        elif primary_verdict in ('HUNG', 'ĐẠI HUNG'):
            consensus_pct = round(hung_count / total * 100) if total else 0
        else:
            consensus_pct = 50
        
        # Tìm mâu thuẫn
        conflicts = []
        for m, v in verdicts.items():
            if m != primary and v != primary_verdict and v != 'BÌNH':
                conflicts.append(f"{METHOD_NAMES.get(m, m)}={v}")
        
        # Build routing text
        primary_name = METHOD_NAMES.get(primary, primary)
        parts = []
        parts.append(f"Loại câu hỏi: {strength_key.upper().replace('_', ' ')}")
        parts.append(f"PP CHÍNH: {primary_name} (trọng số {primary_weight}%) → {primary_verdict}, Điểm={scores.get(primary, 0)}")
        
        # Top 2 PP phụ
        for m, ws in sorted_methods[1:3]:
            m_name = METHOD_NAMES.get(m, m)
            m_weight = strengths[m]
            parts.append(f"PP PHỤ: {m_name} ({m_weight}%) → {verdicts.get(m, 'BÌNH')}, Điểm={scores.get(m, 0)}")
        
        parts.append(f"Đồng thuận: {cat_count}/{total} CÁT, {hung_count}/{total} HUNG = {consensus_pct}%")
        if conflicts:
            parts.append(f"Mâu thuẫn: {', '.join(conflicts[:3])}")
        
        # V32.7: Phát hiện lệch mạnh (>2 cấp) giữa PP chính và PP phụ
        VERDICT_LEVEL = {'ĐẠI CÁT': 4, 'CÁT': 3, 'BÌNH': 2, 'HUNG': 1, 'ĐẠI HUNG': 0}
        primary_level = VERDICT_LEVEL.get(primary_verdict, 2)
        deviations = []
        for m, ws in sorted_methods[1:4]:
            m_verdict = verdicts.get(m, 'BÌNH')
            m_level = VERDICT_LEVEL.get(m_verdict, 2)
            diff = abs(primary_level - m_level)
            if diff >= 2:
                m_name = METHOD_NAMES.get(m, m)
                deviations.append(f"{m_name}({m_verdict}) lệch {diff} cấp vs {primary_name}({primary_verdict})")
        
        if deviations:
            parts.append(f"⚠️ LỆCH MẠNH: {' | '.join(deviations)}")
        
        return {
            'primary': primary,
            'primary_name': primary_name,
            'primary_weight': primary_weight,
            'primary_verdict': primary_verdict,
            'weighted_scores': weighted,
            'consensus_pct': consensus_pct,
            'cat_count': cat_count,
            'hung_count': hung_count,
            'total': total,
            'conflicts': conflicts,
            'deviations': deviations,  # V32.7: Danh sách PP lệch mạnh
            'routing_text': ' | '.join(parts),
        }
    
    # ═══════════════════════════════════════════════════════════
    # V18.0: AI THÁM TỬ — DETECTIVE DEDUCTION
    # Trích manh mối từ tất cả PP → ghép lại → suy luận vật/người/nơi
    # ═══════════════════════════════════════════════════════════
    
    def _detective_deduction(self, chart_data, mai_hoa_data, luc_hao_data, question):
        """V18.0: Trích tất cả manh mối quái tượng → cross-reference → suy luận cụ thể."""
        clues = {
            'quai_list': [],        # Danh sách quái xuất hiện
            'chat_lieu': [],        # Chất liệu
            'hinh_dang': [],        # Hình dạng
            'mau_sac': [],          # Màu sắc
            'am_thanh': [],         # Âm thanh
            'dac_biet': [],         # Đặc biệt
            'nguoi': [],            # Người
            'vat': [],              # Vật
            'noi': [],              # Nơi
            'benh': [],             # Bệnh
            'tim_do': [],           # Tìm đồ
            'phuong_huong': [],     # Phương hướng
        }
        
        def _add_quai(quai_name, source):
            """Thêm thuộc tính từ 1 quái vào clues."""
            if not quai_name or quai_name not in QUAI_ATTRIBUTES:
                return
            clues['quai_list'].append(f"{quai_name}({source})")
            qa = QUAI_ATTRIBUTES[quai_name]
            for key in ['chat_lieu', 'hinh_dang', 'mau_sac', 'am_thanh', 'dac_biet',
                        'nguoi', 'vat', 'noi', 'benh', 'tim_do']:
                for item in qa.get(key, []):
                    if item not in clues[key]:
                        clues[key].append(item)
            # Phương hướng từ Ngũ Hành
            hanh = qa.get('hanh', '')
            if hanh and NGU_HANH_DETECT.get(hanh, {}).get('huong'):
                h = NGU_HANH_DETECT[hanh]['huong']
                if h not in clues['phuong_huong']:
                    clues['phuong_huong'].append(h)
        
        # ① Mai Hoa: Thể, Dụng, Hỗ, Biến Quái
        if mai_hoa_data and isinstance(mai_hoa_data, dict):
            try:
                from mai_hoa_dich_so import QUAI_NAMES
                upper = mai_hoa_data.get('upper', 0)
                lower = mai_hoa_data.get('lower', 0)
                dong_hao = mai_hoa_data.get('dong_hao', 1)
                if dong_hao <= 3:
                    _add_quai(QUAI_NAMES.get(upper, ''), 'MH-Thể')
                    _add_quai(QUAI_NAMES.get(lower, ''), 'MH-Dụng')
                else:
                    _add_quai(QUAI_NAMES.get(lower, ''), 'MH-Thể')
                    _add_quai(QUAI_NAMES.get(upper, ''), 'MH-Dụng')
                # Hỗ Quái
                ho_name = mai_hoa_data.get('ten_ho', '')
                if ho_name:
                    for q in QUAI_ATTRIBUTES:
                        if q in ho_name:
                            _add_quai(q, 'MH-Hỗ')
                            break
                # Biến Quái
                bien_name = mai_hoa_data.get('ten_qua_bien', '')
                if bien_name:
                    for q in QUAI_ATTRIBUTES:
                        if q in bien_name:
                            _add_quai(q, 'MH-Biến')
                            break
            except ImportError:
                pass
        
        # ② Kỳ Môn: Cung → Quái
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            # Tìm cung BT
            for cn, cv in can_thien_ban.items():
                if cv == can_ngay:
                    cung = int(cn) if cn else None
                    if cung:
                        quai = QUAI_TUONG.get(cung, '')
                        _add_quai(quai, 'KM-BT')
                    break
        
        # ③ Lục Hào: Cung quẻ → Quái
        if luc_hao_data and isinstance(luc_hao_data, dict):
            palace = luc_hao_data.get('ban', {}).get('palace', '')
            if palace:
                _add_quai(palace, 'LH-Cung')
        
        # ④ Cross-reference: Tìm thuộc tính TRÙNG giữa nhiều quái
        # Đếm tần suất mỗi vật xuất hiện
        vat_freq = {}
        for v in clues['vat']:
            vat_freq[v] = vat_freq.get(v, 0) + 1
        
        # Tìm vật trùng (xuất hiện >= 2 nguồn khác nhau)
        top_vat = sorted(vat_freq.items(), key=lambda x: x[1], reverse=True)
        
        # ⑤ Suy luận dựa trên combo thuộc tính
        deductions = []
        cl = set(clues['chat_lieu'])
        am = set(clues['am_thanh'])
        db = set(clues['dac_biet'])
        
        # Combo rules
        if cl & {'kim loại', 'sắt', 'thép'} and (am & {'kêu to', 'rung', 'vang', 'rền vang'} or db & {'điện', 'rung lắc'}):
            deductions.append(('LOA / CHUÔNG ĐIỆN / ĐIỆN THOẠI', 90))
        if cl & {'kim loại', 'vàng', 'bạc'} and db & {'quý', 'sang trọng', 'bền'}:
            deductions.append(('TRANG SỨC / ĐỒNG HỒ / ĐỒ QUÝ', 85))
        if db & {'sáng', 'điện tử', 'phát sáng', 'màn hình'}:
            deductions.append(('ĐIỆN THOẠI / MÁY TÍNH / TV', 88))
        if cl & {'nước', 'chất lỏng'} and db & {'lạnh', 'ẩm'}:
            deductions.append(('BÌNH NƯỚC / MÁY GIẶT / TỦ LẠNH', 80))
        if cl & {'gỗ', 'tre'} and db & {'tĩnh', 'chắc chắn'}:
            deductions.append(('BÀN / TỦ / KHUNG GỖ', 75))
        if am & {'vi vu', 'gió'} and db & {'bay', 'gió'}:
            deductions.append(('QUẠT / MÁY LẠNH / ĐIỀU HÒA', 82))
        if cl & {'kính', 'thủy tinh'} and db & {'sáng', 'đẹp'}:
            deductions.append(('GƯƠNG / MẮT KÍNH / BÌNH THỦY TINH', 78))
        if db & {'cắt', 'sắc bén'} and cl & {'kim loại', 'kim loại mỏng'}:
            deductions.append(('DAO / KÉO / DỤNG CỤ CẮT', 80))
        if cl & {'đất', 'đá', 'gạch'} and db & {'nặng', 'chắc chắn'}:
            deductions.append(('ĐÁ / GẠCH / VẬT LIỆU XÂY', 75))
        if am & {'hát', 'nói', 'ca hát'} and cl & {'kim loại mỏng'}:
            deductions.append(('LOA / MIC / KARAOKE', 88))
        
        # Sort deductions by confidence
        deductions.sort(key=lambda x: x[1], reverse=True)
        
        # ⑥ Build detective text
        parts = []
        parts.append(f"🔎 MANH MỐI ({len(clues['quai_list'])} quái): {', '.join(clues['quai_list'][:6])}")
        
        if clues['chat_lieu']:
            parts.append(f"📦 Chất liệu: {', '.join(clues['chat_lieu'][:5])}")
        if clues['hinh_dang']:
            parts.append(f"📐 Hình dạng: {', '.join(clues['hinh_dang'][:4])}")
        if clues['am_thanh']:
            parts.append(f"🔊 Âm thanh: {', '.join(clues['am_thanh'][:4])}")
        if clues['dac_biet']:
            parts.append(f"⚡ Đặc biệt: {', '.join(clues['dac_biet'][:5])}")
        if clues['mau_sac']:
            parts.append(f"🎨 Màu sắc: {', '.join(clues['mau_sac'][:4])}")
        if clues['phuong_huong']:
            parts.append(f"🧭 Phương hướng: {', '.join(clues['phuong_huong'])}")
        
        # Người
        if clues['nguoi']:
            parts.append(f"👤 Người: {', '.join(clues['nguoi'][:5])}")
        # Vật
        if top_vat:
            vat_text = ', '.join([f"{v}({'⭐' if c > 1 else ''})" for v, c in top_vat[:6]])
            parts.append(f"📱 Vật: {vat_text}")
        # Nơi
        if clues['noi']:
            parts.append(f"📍 Nơi: {', '.join(clues['noi'][:5])}")
        # Tìm đồ
        if clues['tim_do']:
            parts.append(f"🔍 Tìm ở: {', '.join(clues['tim_do'][:4])}")
        # Bệnh
        if clues['benh']:
            parts.append(f"🏥 Bệnh: {', '.join(clues['benh'][:4])}")
        
        # Deductions
        if deductions:
            ded_text = ' | '.join([f"{d[0]} ({d[1]}%)" for d in deductions[:3]])
            parts.append(f"🎯 SUY LUẬN: {ded_text}")
        
        return ' | '.join(parts[:8]), clues, deductions
    
    # ===========================
    # V10.0: PHÂN TÍCH TÁC ĐỘNG YẾU TỐ VÀO CHU THỂ
    # ===========================
    def _build_element_impact_analysis(self, question, dung_than, category_label,
                                       chart_data, luc_hao_data, mai_hoa_data,
                                       ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict,
                                       ky_mon_reason, luc_hao_reason, mai_hoa_reason,
                                       age_numbers=None, count_numbers=None, **kwargs):
        """
        V10.0: Phân tích TÁC ĐỘNG của các yếu tố quẻ vào Chu Thể (Dụng Thần)
        theo ngữ cảnh câu hỏi thực tế — KHÔNG dùng mẫu cứng.
        
        Trả về (impact_text, direct_answer, evidence_list)
        """
        q = question.lower()
        impacts = []
        evidence = []
        
        # ═══════════════════════════════════════════════
        # V10.2: TRỌNG TÂM — DỤNG THẦN (CENTER OF ALL ANALYSIS)
        # ═══════════════════════════════════════════════
        dt_summary = []
        dt_summary.append(f"**🎯 DỤNG THẦN: {dung_than}**")
        
        # --- A. TÌM DỤNG THẦN TRONG KỲ MÔN ---
        dt_ky_mon_cung = None
        bt_ky_mon_cung = None
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            thien_ban = chart_data.get('thien_ban', {})
            nhan_ban = chart_data.get('nhan_ban', {})
            than_ban = chart_data.get('than_ban', {})
            
            # Map Dụng Thần → Can tương ứng trong Kỳ Môn
            dt_can_map = {
                'Quan Quỷ': chart_data.get('can_gio', ''),
                'Thê Tài': chart_data.get('can_gio', ''),
                'Tử Tôn': chart_data.get('can_gio', ''),
                'Phụ Mẫu': chart_data.get('can_nam', ''),
                'Huynh Đệ': chart_data.get('can_thang', ''),
                'Bản Thân': can_ngay,
            }
            dt_can = dt_can_map.get(dung_than, chart_data.get('can_gio', ''))
            dt_can_label = {'Quan Quỷ': 'Can Giờ', 'Thê Tài': 'Can Giờ', 'Tử Tôn': 'Can Giờ',
                           'Phụ Mẫu': 'Can Năm', 'Huynh Đệ': 'Can Tháng', 'Bản Thân': 'Can Ngày'}.get(dung_than, 'Can Giờ')
            
            # Tìm cung DT
            for cung_num, can_val in can_thien_ban.items():
                if can_val == dt_can:
                    dt_ky_mon_cung = int(cung_num) if cung_num else None
                    break
            
            # Tìm cung BT
            for cung_num, can_val in can_thien_ban.items():
                if can_val == can_ngay:
                    bt_ky_mon_cung = int(cung_num) if cung_num else None
                    break
            if not bt_ky_mon_cung and can_ngay == 'Giáp':
                for cung_num, can_val in can_thien_ban.items():
                    if can_val == 'Mậu':
                        bt_ky_mon_cung = int(cung_num) if cung_num else None
                        break
            
            if dt_ky_mon_cung:
                dt_sao = str(thien_ban.get(dt_ky_mon_cung, thien_ban.get(str(dt_ky_mon_cung), '?')))
                dt_cua = str(nhan_ban.get(dt_ky_mon_cung, nhan_ban.get(str(dt_ky_mon_cung), '?')))
                dt_than = str(than_ban.get(dt_ky_mon_cung, than_ban.get(str(dt_ky_mon_cung), '?')))
                dt_hanh_cung = CUNG_NGU_HANH.get(dt_ky_mon_cung, '?')
                dt_quai = QUAI_TUONG.get(dt_ky_mon_cung, '?')
                dt_hanh_can = CAN_NGU_HANH.get(dt_can, '?')
                
                dt_summary.append(f"📍 **Kỳ Môn:** {dung_than} = {dt_can_label} ({dt_can}) → Cung {dt_ky_mon_cung} ({dt_quai}, {dt_hanh_cung})")
                dt_summary.append(f"   Sao: **{dt_sao}** | Cửa: **{dt_cua}** | Thần: **{dt_than}**")
                
                # Vượng/Suy của DT Can tại cung
                if dt_hanh_can != '?' and dt_hanh_cung != '?':
                    if dt_hanh_can == dt_hanh_cung:
                        dt_summary.append(f"   💪 Trạng thái: **VƯỢNG** (đắc địa)")
                    elif SINH.get(dt_hanh_cung) == dt_hanh_can:
                        dt_summary.append(f"   💪 Trạng thái: **TƯỚNG** (được sinh)")
                    elif SINH.get(dt_hanh_can) == dt_hanh_cung:
                        dt_summary.append(f"   😐 Trạng thái: HƯU (nghỉ)")
                    elif KHAC.get(dt_hanh_can) == dt_hanh_cung:
                        dt_summary.append(f"   😰 Trạng thái: TÙ (bị giam)")
                    elif KHAC.get(dt_hanh_cung) == dt_hanh_can:
                        dt_summary.append(f"   🔴 Trạng thái: **TỬ** (bị khắc)")
                
                # Nguyên Thần (cái gì SINH DT?)
                nguyen_than_hanh = {v: k for k, v in SINH.items()}.get(dt_hanh_can, '')
                if nguyen_than_hanh:
                    dt_summary.append(f"   ✅ Nguyên Thần (sinh DT): Hành **{nguyen_than_hanh}**")
                
                # Kỵ Thần (cái gì KHẮC DT?)
                ky_than_hanh = {v: k for k, v in KHAC.items()}.get(dt_hanh_can, '')
                if ky_than_hanh:
                    dt_summary.append(f"   ⚠️ Kỵ Thần (khắc DT): Hành **{ky_than_hanh}**")
                
                # DT ↔ BT relationship
                if bt_ky_mon_cung and bt_ky_mon_cung != dt_ky_mon_cung:
                    bt_hanh = CUNG_NGU_HANH.get(bt_ky_mon_cung, '?')
                    rel = _ngu_hanh_relation(bt_hanh, dt_hanh_cung)
                    dt_summary.append(f"   🔄 BT (Cung {bt_ky_mon_cung}, {bt_hanh}) ↔ DT (Cung {dt_ky_mon_cung}, {dt_hanh_cung}): {rel}")
        
        # --- B. TÌM DỤNG THẦN TRONG LỤC HÀO ---
        if luc_hao_data and isinstance(luc_hao_data, dict):
            ban = luc_hao_data.get('ban', {})
            haos = ban.get('haos') or ban.get('details', [])
            dt_hao_lh = None
            the_hao_lh = None
            
            for i, hao in enumerate(haos):
                lt = hao.get('luc_than', '')
                tu = hao.get('the_ung', '')
                if lt == dung_than or (dung_than in ['Bản Thân'] and tu == 'Thế'):
                    dt_hao_lh = hao
                elif 'Phụ Mẫu' in dung_than and 'Phụ Mẫu' in lt:
                    dt_hao_lh = hao
                if tu == 'Thế':
                    the_hao_lh = hao
            
            if not dt_hao_lh and dung_than == 'Bản Thân':
                dt_hao_lh = the_hao_lh
            
            if dt_hao_lh:
                dt_hao_num = dt_hao_lh.get('hao', '?')
                dt_canchi = dt_hao_lh.get('can_chi', '?')
                dt_vuong = dt_hao_lh.get('vuong_suy', '?')
                dt_hanh_lh = dt_hao_lh.get('ngu_hanh', '?')
                dt_summary.append(f"📍 **Lục Hào:** {dung_than} tại Hào {dt_hao_num} ({dt_canchi}) — {dt_vuong}")
                
                # Tìm Nguyên Thần hào (hào nào SINH DT?)
                if dt_hanh_lh and dt_hanh_lh != '?':
                    nguyen_hanh = {v: k for k, v in SINH.items()}.get(dt_hanh_lh, '')
                    ky_hanh = {v: k for k, v in KHAC.items()}.get(dt_hanh_lh, '')
                    for hao in haos:
                        h_hanh = hao.get('ngu_hanh', '')
                        h_lt = hao.get('luc_than', '')
                        if h_hanh == nguyen_hanh and hao != dt_hao_lh:
                            dt_summary.append(f"   ✅ Nguyên Thần hào: {h_lt} ({hao.get('can_chi','')}, {h_hanh}) sinh {dung_than}")
                            break
                    for hao in haos:
                        h_hanh = hao.get('ngu_hanh', '')
                        h_lt = hao.get('luc_than', '')
                        if h_hanh == ky_hanh and hao != dt_hao_lh:
                            dt_summary.append(f"   ⚠️ Kỵ Thần hào: {h_lt} ({hao.get('can_chi','')}, {h_hanh}) khắc {dung_than}")
                            break
            else:
                dt_summary.append(f"📍 **Lục Hào:** {dung_than} KHÔNG xuất hiện → Phục Thần (ẩn)")
        
        # Thêm DT summary vào impacts
        if len(dt_summary) > 1:
            impacts.append("\n" + "\n".join(dt_summary))
            evidence.append(f"DT={dung_than}")
        
        # --- 1. PHÂN TÍCH TÁC ĐỘNG TỪ KỲ MÔN ---
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            hanh_can = CAN_NGU_HANH.get(can_ngay, '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            thien_ban = chart_data.get('thien_ban', {})
            nhan_ban = chart_data.get('nhan_ban', {})
            than_ban = chart_data.get('than_ban', {})
            
            # Tìm cung bản thân
            chu_cung = None
            for cung_num, can_val in can_thien_ban.items():
                if can_val == can_ngay:
                    chu_cung = int(cung_num) if cung_num else None
                    break
            if not chu_cung and can_ngay == 'Giáp':
                for cung_num, can_val in can_thien_ban.items():
                    if can_val == 'Mậu':
                        chu_cung = int(cung_num) if cung_num else None
                        break
            
            if chu_cung:
                sao = str(thien_ban.get(chu_cung, thien_ban.get(str(chu_cung), '?')))
                cua = str(nhan_ban.get(chu_cung, nhan_ban.get(str(chu_cung), '?')))
                than = str(than_ban.get(chu_cung, than_ban.get(str(chu_cung), '?')))
                hanh_cung = CUNG_NGU_HANH.get(chu_cung, '?')
                
                # Sao → tác động vào Dụng Thần
                sao_info = SAO_GIAI_THICH.get(sao, {})
                sao_hanh = sao_info.get('hanh', '')
                if sao_hanh and hanh_can:
                    sao_rel = _ngu_hanh_relation(sao_hanh, hanh_can)
                    if 'KHẮC' in sao_rel:
                        impacts.append(f"⚠️ Sao **{sao}** ({sao_hanh}) KHẮC chủ thể ({hanh_can}) → {dung_than} chịu ÁP LỰC từ hoàn cảnh")
                        evidence.append(f"Sao {sao} khắc chủ")
                    elif 'SINH' in sao_rel and 'BỊ' not in sao_rel:
                        impacts.append(f"✅ Sao **{sao}** ({sao_hanh}) SINH chủ thể ({hanh_can}) → {dung_than} được NĂNG LƯỢNG hỗ trợ")
                        evidence.append(f"Sao {sao} sinh chủ")
                    elif 'ĐƯỢC SINH' in sao_rel:
                        impacts.append(f"✅ Chủ thể ({hanh_can}) SINH Sao **{sao}** ({sao_hanh}) → Năng lượng từ chủ tỏa ra ngoài, hao tốn nhẹ")
                
                # Cửa → tác động theo NGỮ CẢNH câu hỏi
                cua_key = cua if 'Môn' in cua else cua + ' Môn'
                cua_info = CUA_GIAI_THICH.get(cua_key, {})
                cua_cat_hung = cua_info.get('cat_hung', '')
                cua_y_nghia = cua_info.get('y_nghia', '')
                
                # Map Cửa vào ngữ cảnh CỤ THỂ của câu hỏi
                if any(k in q for k in ['bệnh', 'ốm', 'đau', 'khỏe', 'sức khỏe', 'mất', 'chết', 'sống']):
                    if 'Tử' in cua_key:
                        impacts.append(f"🔴 Cửa **{cua}** (Đại Hung) tại cung BT khi hỏi sức khỏe → DẤU HIỆU NGUY HIỂM, {dung_than} gặp vấn đề nghiêm trọng")
                        evidence.append(f"Tử Môn + hỏi sức khỏe")
                    elif 'Sinh' in cua_key:
                        impacts.append(f"✅ Cửa **{cua}** (Đại Cát) tại cung BT khi hỏi sức khỏe → SỨC SỐNG TỐT, {dung_than} hồi phục")
                        evidence.append(f"Sinh Môn + hỏi sức khỏe")
                    elif 'Kinh' in cua_key:
                        impacts.append(f"⚠️ Cửa **{cua}** (Hung) tại cung BT → Có SỢ HÃI/LO LẮNG liên quan {dung_than}")
                    elif 'Khai' in cua_key:
                        impacts.append(f"✅ Cửa **{cua}** (Đại Cát) → Tình hình MỞ RA hướng tốt cho {dung_than}")
                    elif 'Thương' in cua_key:
                        impacts.append(f"⚠️ Cửa **{cua}** (Hung) → Có XUNG ĐỘT/TỔN THƯƠNG liên quan {dung_than}")
                    else:
                        impacts.append(f"{'✅' if 'Cát' in cua_cat_hung else '⚠️'} Cửa **{cua}** ({cua_cat_hung}) → {cua_y_nghia}")
                elif any(k in q for k in ['tiền', 'tài', 'mua', 'bán', 'đầu tư', 'kinh doanh', 'lương']):
                    if 'Sinh' in cua_key:
                        impacts.append(f"✅ Cửa **{cua}** (Đại Cát) tại cung BT khi hỏi tài chính → TÀI LỘC VƯỢNG, {dung_than} sinh sôi")
                        evidence.append(f"Sinh Môn + hỏi tài chính")
                    elif 'Tử' in cua_key:
                        impacts.append(f"🔴 Cửa **{cua}** (Đại Hung) → Tiền CHẤM DỨT/MẤT MÁT, tránh giao dịch lớn")
                        evidence.append(f"Tử Môn + hỏi tài")
                    elif 'Thương' in cua_key:
                        impacts.append(f"⚠️ Cửa **{cua}** (Hung) → TRANH CHẤP TIỀN BẠC, cẩn thận đối tác")
                    else:
                        impacts.append(f"{'✅' if 'Cát' in cua_cat_hung else '⚠️'} Cửa **{cua}** ({cua_cat_hung}) → {cua_y_nghia}")
                elif any(k in q for k in ['yêu', 'tình', 'vợ', 'chồng', 'cưới', 'hôn nhân']):
                    if 'Hưu' in cua_key:
                        impacts.append(f"✅ Cửa **{cua}** (Cát) khi hỏi tình cảm → HAI BÊN VUI VẺ, hợp nhau")
                        evidence.append(f"Hưu Môn + hỏi tình cảm")
                    elif 'Kinh' in cua_key or 'Thương' in cua_key:
                        impacts.append(f"⚠️ Cửa **{cua}** (Hung) khi hỏi tình cảm → CÃI VÃ/XUNG ĐỘT trong mối quan hệ")
                        evidence.append(f"{cua_key} + hỏi tình cảm")
                    elif 'Tử' in cua_key:
                        impacts.append(f"🔴 Cửa **{cua}** (Đại Hung) → Mối quan hệ có nguy cơ CHẤM DỨT")
                    else:
                        impacts.append(f"{'✅' if 'Cát' in cua_cat_hung else '⚠️'} Cửa **{cua}** ({cua_cat_hung}) → {cua_y_nghia}")
                else:
                    # Generic nhưng vẫn mô tả tác động
                    if 'Đại Cát' in cua_cat_hung:
                        impacts.append(f"✅ Cửa **{cua}** ({cua_cat_hung}) → {dung_than} được MỞ ĐƯỜNG, thuận lợi: {cua_y_nghia}")
                    elif 'Đại Hung' in cua_cat_hung:
                        impacts.append(f"🔴 Cửa **{cua}** ({cua_cat_hung}) → {dung_than} bị CHẶN ĐƯỜNG: {cua_y_nghia}")
                    elif 'Hung' in cua_cat_hung:
                        impacts.append(f"⚠️ Cửa **{cua}** ({cua_cat_hung}) → {dung_than} gặp trở ngại: {cua_y_nghia}")
                    else:
                        impacts.append(f"ℹ️ Cửa **{cua}** ({cua_cat_hung}) → Ảnh hưởng trung tính: {cua_y_nghia}")
                
                # Thần → tác động theo ngữ cảnh
                than_info = THAN_GIAI_THICH.get(than, {})
                than_tc = than_info.get('tinh_chat', '')
                if than_tc:
                    if any(k in than_tc for k in ['CÁT', 'giúp đỡ', 'che chở', 'hỗ trợ', 'hợp tác']):
                        impacts.append(f"✅ Thần **{than}** → {dung_than} được BẢO VỆ: {than_tc}")
                        evidence.append(f"Thần {than} cát")
                    elif any(k in than_tc for k in ['tai', 'lừa', 'trộm', 'phá', 'ám']):
                        impacts.append(f"⚠️ Thần **{than}** → {dung_than} phải CẢNH GIÁC: {than_tc}")
                        evidence.append(f"Thần {than} hung")
                    else:
                        impacts.append(f"ℹ️ Thần **{than}** → {than_tc}")
            
            # --- V10.1: TÌM VÀ PHÂN TÍCH CUNG DỤNG THẦN TRONG KỲ MÔN ---
            # Xác định Can đại diện Dụng Thần
            dt_can_map = {
                'Quan Quỷ': chart_data.get('can_gio', ''),     # Sự việc/Công việc = Can Giờ
                'Thê Tài': chart_data.get('can_gio', ''),       # Tài sản = Can Giờ  
                'Tử Tôn': chart_data.get('can_gio', ''),        # Con cái = Can Giờ
                'Phụ Mẫu': chart_data.get('can_nam', ''),       # Bố mẹ = Can Năm
                'Huynh Đệ': chart_data.get('can_thang', ''),    # Anh em = Can Tháng
                'Bản Thân': can_ngay,                            # Bản thân = Can Ngày
            }
            dt_can = dt_can_map.get(dung_than, chart_data.get('can_gio', ''))
            
            # Tìm cung Dụng Thần
            dt_cung = None
            if dt_can and dt_can != can_ngay:  # Chỉ phân tích nếu DT khác BT
                for cung_num, can_val in can_thien_ban.items():
                    if can_val == dt_can:
                        dt_cung = int(cung_num) if cung_num else None
                        break
            
            if dt_cung and dt_cung != chu_cung:
                dt_sao = str(thien_ban.get(dt_cung, thien_ban.get(str(dt_cung), '?')))
                dt_cua = str(nhan_ban.get(dt_cung, nhan_ban.get(str(dt_cung), '?')))
                dt_than_val = str(than_ban.get(dt_cung, than_ban.get(str(dt_cung), '?')))
                dt_hanh_cung = CUNG_NGU_HANH.get(dt_cung, '?')
                dt_quai = QUAI_TUONG.get(dt_cung, '?')
                
                impacts.append(f"\n**🔍 CUNG DỤNG THẦN ({dung_than}) — Cung {dt_cung} ({dt_quai}):**")
                impacts.append(f"📊 Sao: **{dt_sao}** | Cửa: **{dt_cua}** | Thần: **{dt_than_val}** | Hành: {dt_hanh_cung}")
                
                # Phân tích Sao tại cung DT
                dt_sao_info = SAO_GIAI_THICH.get(dt_sao, {})
                dt_sao_ch = dt_sao_info.get('cat_hung', dt_sao_info.get('tinh_chat', ''))
                if dt_sao_ch:
                    impacts.append(f"→ Sao {dt_sao}: {dt_sao_ch}")
                
                # Phân tích Cửa tại cung DT
                dt_cua_key = dt_cua if 'Môn' in dt_cua else dt_cua + ' Môn'
                dt_cua_info = CUA_GIAI_THICH.get(dt_cua_key, {})
                dt_cua_ch = dt_cua_info.get('cat_hung', '')
                dt_cua_yn = dt_cua_info.get('y_nghia', '')
                if dt_cua_yn:
                    impacts.append(f"→ Cửa {dt_cua}: {dt_cua_ch} — {dt_cua_yn}")
                
                # Phân tích quan hệ BT cung ↔ DT cung
                if chu_cung and hanh_can:
                    bt_hanh_c = CUNG_NGU_HANH.get(chu_cung, '?')
                    rel_cung = _ngu_hanh_relation(bt_hanh_c, dt_hanh_cung)
                    impacts.append(f"→ BT Cung {chu_cung} ({bt_hanh_c}) vs DT Cung {dt_cung} ({dt_hanh_cung}): {rel_cung}")
                    evidence.append(f"BT↔DT: {rel_cung[:20]}")
        
        # --- V15.0: PHÂN TÍCH NỘI CUNG (XÂU DƯỢC) — BẢN THÂN + DỤNG THẦN ---
        if chart_data and isinstance(chart_data, dict):
            # Phân tích nội cung BẢN THÂN
            if chu_cung:
                bt_score, bt_details, bt_strength = self._analyze_cung_factors(
                    chu_cung, chart_data, question, "BẢN THÂN")
                if bt_details:
                    impacts.append(f"\n{'─' * 40}")
                    for d in bt_details:
                        impacts.append(d)
                    evidence.append(f"NộiCung BT={bt_score}({bt_strength.split()[-1]})")
            
            # Phân tích nội cung DỤNG THẦN (nếu khác cung BT)
            if dt_cung and dt_cung != chu_cung:
                dt_score_v15, dt_details, dt_strength = self._analyze_cung_factors(
                    dt_cung, chart_data, question, f"DỤNG THẦN ({dung_than})")
                if dt_details:
                    impacts.append(f"\n{'─' * 40}")
                    for d in dt_details:
                        impacts.append(d)
                    evidence.append(f"NộiCung DT={dt_score_v15}({dt_strength.split()[-1]})")
        
        # --- V15.2: PHÂN TÍCH QUÁ KHỨ / HIỆN TẠI / TƯƠNG LAI ---
        if chart_data and isinstance(chart_data, dict):
            # Timeline cung BẢN THÂN
            if chu_cung:
                bt_timeline = self._analyze_timeline(chu_cung, chart_data, question, "BẢN THÂN")
                if bt_timeline:
                    impacts.append(f"\n{'─' * 40}")
                    for t in bt_timeline:
                        impacts.append(t)
            
            # Timeline cung DỤNG THẦN (nếu khác BT)
            if dt_cung and dt_cung != chu_cung:
                dt_timeline = self._analyze_timeline(dt_cung, chart_data, question, f"DỤNG THẦN ({dung_than})")
                if dt_timeline:
                    impacts.append(f"\n{'─' * 40}")
                    for t in dt_timeline:
                        impacts.append(t)
        
        # --- V15.3: ỨNG KỲ — THỜI GIAN SỰ VIỆC XẢY RA ---
        if chart_data and isinstance(chart_data, dict) and dt_cung:
            # Lấy score DT cung từ V15.0 (nếu có) hoặc mặc định 0
            dt_cung_score = 0
            try:
                dt_cung_score = dt_score_v15
            except NameError:
                pass
            timing_details = self._analyze_timing(
                dt_cung, chart_data, question, dung_than, cung_score=dt_cung_score)
            if timing_details:
                impacts.append(f"\n{'─' * 40}")
                for td in timing_details:
                    impacts.append(td)
        
        # --- 1.5 V10.1: TRUY VẤN TRI THỨC SÂU TỪ KNOWLEDGE COMPLETE ---
        if chart_data and isinstance(chart_data, dict) and chu_cung:
            try:
                # Tra cứu chi tiết cung BT từ Knowledge Complete
                kc_cung = tra_cuu_cung(chu_cung)
                if kc_cung:
                    kc_parts = []
                    
                    # Theo NGỮ CẢNH câu hỏi → lấy dữ liệu phù hợp
                    if any(k in q for k in ['tìm', 'mất', 'đâu', 'nơi', 'chỗ', 'ở đâu', 'cất', 'giấu']):
                        # TÌM ĐỒ → Nơi + Vật + Hướng + Khả năng tìm
                        if kc_cung.get('Noi'): kc_parts.append(f"📍 Nơi: {kc_cung['Noi']}")
                        if kc_cung.get('Huong'): kc_parts.append(f"🧭 Hướng: {kc_cung['Huong']}")
                        if kc_cung.get('Vat'): kc_parts.append(f"🔎 Vật gần: {kc_cung['Vat']}")
                        # Tra Sao tại cung → Tim_Do
                        sao_kb = tra_cuu_sao(sao) if sao != '?' else {}
                        if sao_kb.get('Tim_Do'): kc_parts.append(f"🔮 Sao {sao}: {sao_kb['Tim_Do']}")
                        # Tra Cửa → Tim_Do + Khả năng
                        cua_kb = tra_cuu_mon(cua) if cua != '?' else {}
                        if cua_kb.get('Tim_Do'): kc_parts.append(f"🚪 Cửa {cua}: Khả năng tìm: {cua_kb['Tim_Do']}")
                        # Tra Thần → Tim_Do
                        than_kb = tra_cuu_than(than) if than != '?' else {}
                        if than_kb.get('Tim_Do'): kc_parts.append(f"👤 Thần {than}: {than_kb['Tim_Do']}")
                        
                    elif any(k in q for k in ['bệnh', 'ốm', 'đau', 'khỏe', 'sức khỏe', 'chết', 'sống']):
                        # SỨC KHỎE → Thân Thể + Bệnh + Người
                        if kc_cung.get('Than_The'): kc_parts.append(f"🏥 Bộ phận: {kc_cung['Than_The']}")
                        sao_kb = tra_cuu_sao(sao) if sao != '?' else {}
                        if sao_kb.get('Benh'): kc_parts.append(f"💊 Sao {sao} → Bệnh: {sao_kb['Benh']}")
                        if kc_cung.get('Nguoi'): kc_parts.append(f"👤 Người: {kc_cung['Nguoi']}")
                        
                    elif any(k in q for k in ['việc', 'công', 'nghề', 'thi', 'học', 'thăng', 'sếp', 'đỗ']):
                        # CÔNG VIỆC → Việc Tốt/Xấu + Tính cách
                        sao_kb = tra_cuu_sao(sao) if sao != '?' else {}
                        if sao_kb.get('Viec_Tot'): kc_parts.append(f"✅ Sao {sao} — Việc tốt: {sao_kb['Viec_Tot']}")
                        if sao_kb.get('Viec_Xau'): kc_parts.append(f"⚠️ Sao {sao} — Việc xấu: {sao_kb['Viec_Xau']}")
                        cua_kb = tra_cuu_mon(cua) if cua != '?' else {}
                        if cua_kb.get('Viec_Tot'): kc_parts.append(f"✅ Cửa {cua} — Việc tốt: {cua_kb['Viec_Tot']}")
                        if cua_kb.get('Viec_Xau'): kc_parts.append(f"⚠️ Cửa {cua} — Việc xấu: {cua_kb['Viec_Xau']}")
                        if kc_cung.get('Tinh_Cach'): kc_parts.append(f"🧠 Tính cách: {kc_cung['Tinh_Cach']}")
                        
                    elif any(k in q for k in ['tiền', 'tài', 'mua', 'bán', 'đầu tư', 'kinh doanh', 'lương', 'nhà', 'đất']):
                        # TÀI CHÍNH → Vật + Nơi + Việc Tốt/Xấu
                        cua_kb = tra_cuu_mon(cua) if cua != '?' else {}
                        if cua_kb.get('Viec_Tot'): kc_parts.append(f"✅ Cửa {cua} — Tốt cho: {cua_kb['Viec_Tot']}")
                        if cua_kb.get('Viec_Xau'): kc_parts.append(f"⚠️ Cửa {cua} — Xấu cho: {cua_kb['Viec_Xau']}")
                        if kc_cung.get('Vat'): kc_parts.append(f"💰 Vật phẩm: {kc_cung['Vat']}")
                        if kc_cung.get('Noi'): kc_parts.append(f"📍 Nơi: {kc_cung['Noi']}")
                    
                    elif any(k in q for k in ['yêu', 'tình', 'vợ', 'chồng', 'cưới', 'bạn gái', 'bạn trai', 'hôn']):
                        # TÌNH CẢM → Người + Tính cách + Tượng
                        if kc_cung.get('Nguoi'): kc_parts.append(f"👤 Người: {kc_cung['Nguoi']}")
                        if kc_cung.get('Tinh_Cach'): kc_parts.append(f"🧠 Tính cách: {kc_cung['Tinh_Cach']}")
                        if kc_cung.get('Tuong'): kc_parts.append(f"🔮 Tượng: {kc_cung['Tuong']}")
                    
                    else:
                        # TỔNG QUÁT → Người + Vật + Tính cách + Tượng
                        sao_kb = tra_cuu_sao(sao) if sao != '?' else {}
                        if kc_cung.get('Tuong'): kc_parts.append(f"🔮 Tượng Cung {chu_cung}: {kc_cung['Tuong']}")
                        if sao_kb.get('Tuong'): kc_parts.append(f"⭐ Tượng Sao {sao}: {sao_kb['Tuong']}")
                        if kc_cung.get('Tinh_Cach'): kc_parts.append(f"🧠 Tính cách: {kc_cung['Tinh_Cach']}")
                    
                    # Tra Can Ngày → thêm thông tin người
                    can_kb = tra_cuu_can(chart_data.get('can_ngay', '')) if THAP_THIEN_CAN else {}
                    if can_kb.get('Nguoi') and len(kc_parts) < 5:
                        kc_parts.append(f"👤 Can {chart_data.get('can_ngay','')}: {can_kb['Nguoi']}")
                    
                    if kc_parts:
                        impacts.append(f"\n**📚 TRI THỨC SÂU (Knowledge Complete):**")
                        for part in kc_parts[:6]:  # Max 6 items
                            impacts.append(f"- {part}")
                        evidence.append("KB Complete")
            except Exception:
                pass
        
        # --- 2. PHÂN TÍCH TÁC ĐỘNG TỪ LỤC HÀO ---
        if luc_hao_data and isinstance(luc_hao_data, dict):
            ban = luc_hao_data.get('ban', {})
            haos = ban.get('haos') or ban.get('details', [])
            dong_hao = luc_hao_data.get('dong_hao', [])
            
            # Tìm hào Dụng Thần
            dt_hao = None
            the_hao = None
            for i, hao in enumerate(haos):
                lt = hao.get('luc_than', '')
                tu = hao.get('the_ung', '')
                if lt == dung_than or (dung_than in ['Bản Thân', 'Phụ Mẫu (Cha)', 'Phụ Mẫu (Mẹ)'] and 'Phụ Mẫu' in lt):
                    dt_hao = hao
                elif dung_than == 'Bản Thân' and tu == 'Thế':
                    the_hao = hao
                elif tu == 'Thế':
                    the_hao = hao
            
            if not dt_hao and dung_than == 'Bản Thân':
                dt_hao = the_hao
            
            if dt_hao:
                dt_vuong = str(dt_hao.get('vuong_suy', ''))
                dt_hanh = dt_hao.get('ngu_hanh', '')
                dt_canchi = dt_hao.get('can_chi', '')
                
                # Mô tả TÁC ĐỘNG vượng/suy theo ngữ cảnh
                if 'Vượng' in dt_vuong or 'Tướng' in dt_vuong:
                    if any(k in q for k in ['bệnh', 'ốm', 'chết', 'mất']):
                        impacts.append(f"✅ Hào {dung_than} ({dt_canchi}) **VƯỢNG** → {dung_than} CÒN SỨC, tình trạng KHẢ QUAN")
                    elif any(k in q for k in ['tiền', 'tài', 'lương', 'đầu tư']):
                        impacts.append(f"✅ Hào {dung_than} ({dt_canchi}) **VƯỢNG** → Tài chính THUẬN LỢI, có khả năng sinh lời")
                    elif any(k in q for k in ['việc', 'thi', 'đỗ', 'thăng']):
                        impacts.append(f"✅ Hào {dung_than} ({dt_canchi}) **VƯỢNG** → Công việc/Thi cử CÓ KẾT QUẢ TỐT")
                    else:
                        impacts.append(f"✅ Hào {dung_than} ({dt_canchi}) **VƯỢNG** → {dung_than} MẠNH MẼ, sự việc thuận lợi")
                    evidence.append(f"Dụng Thần {dung_than} Vượng")
                elif 'Tử' in dt_vuong or 'Tuyệt' in dt_vuong:
                    if any(k in q for k in ['bệnh', 'ốm', 'chết', 'mất', 'sống']):
                        impacts.append(f"🔴 Hào {dung_than} ({dt_canchi}) **{dt_vuong}** → {dung_than} RẤT YẾU, tình trạng NGUY HIỂM")
                    else:
                        impacts.append(f"🔴 Hào {dung_than} ({dt_canchi}) **{dt_vuong}** → {dung_than} gần như VÔ LỰC, sự việc KHÓ THÀNH")
                    evidence.append(f"Dụng Thần {dung_than} {dt_vuong}")
                elif 'Suy' in dt_vuong or 'Bệnh' in dt_vuong:
                    if any(k in q for k in ['bệnh', 'ốm', 'chết', 'mất']):
                        impacts.append(f"⚠️ Hào {dung_than} ({dt_canchi}) **{dt_vuong}** → {dung_than} ĐANG YẾU, cần hỗ trợ gấp")
                    else:
                        impacts.append(f"⚠️ Hào {dung_than} ({dt_canchi}) **{dt_vuong}** → {dung_than} suy giảm, sự việc gặp TRỞ NGẠI")
                    evidence.append(f"Dụng Thần {dung_than} {dt_vuong}")
                
                # Kiểm tra hào động ảnh hưởng đến Dụng Thần
                if dong_hao:
                    for d in dong_hao:
                        if d <= len(haos):
                            h_dong = haos[d-1]
                            h_hanh = h_dong.get('ngu_hanh', '')
                            h_lt = h_dong.get('luc_than', '')
                            if dt_hanh and h_hanh:
                                rel = _ngu_hanh_relation(h_hanh, dt_hanh)
                                if 'thắng' in rel:  # h_dong khắc dt
                                    impacts.append(f"⚠️ Hào {d} ({h_lt} {h_dong.get('can_chi','')}) ĐỘNG + KHẮC {dung_than} → Có lực lượng GÂY HẠI cho {dung_than}")
                                    evidence.append(f"Hào {d} {h_lt} khắc DT")
                                elif 'SINH' in rel and 'BỊ' not in rel:  # h_dong sinh dt
                                    impacts.append(f"✅ Hào {d} ({h_lt} {h_dong.get('can_chi','')}) ĐỘNG + SINH {dung_than} → Có lực lượng HỖ TRỢ {dung_than}")
                                    evidence.append(f"Hào {d} {h_lt} sinh DT")
        
        # --- 3. TỔNG HỢP → TRẢ LỜI TRỰC TIẾP ---
        # V14.0: Mở rộng từ 3 → 5 verdicts (thêm Lục Nhâm + Thái Ất)
        luc_nham_v = kwargs.get('luc_nham_verdict', 'BÌNH')
        thai_at_v = kwargs.get('thai_at_verdict', 'BÌNH')
        
        # V26.3: Dùng weighted_pct từ bên ngoài truyền vào (Nếu có)
        ext_pct = kwargs.get('weighted_pct', None)
        if ext_pct is not None:
            pct = ext_pct
            if pct >= 60:
                final_verdict = 'CÁT'
            elif pct <= 45:
                final_verdict = 'HUNG'
            else:
                final_verdict = 'BÌNH'
        else:
            # FALLBACK: dùng logic đếm cũ nếu không có weighted_pct
            verdicts = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict, luc_nham_v, thai_at_v]
            cat_count = sum(1 for v in verdicts if v in ['CÁT', 'ĐẠI CÁT'])
            hung_count = sum(1 for v in verdicts if v in ['HUNG', 'ĐẠI HUNG'])
            if cat_count > hung_count:
                final_verdict = 'CÁT'
                pct = min(90, 50 + (cat_count / max(len(verdicts), 1)) * 30)
            elif hung_count > cat_count:
                final_verdict = 'HUNG'
                pct = max(10, 50 - (hung_count / max(len(verdicts), 1)) * 30)
            else:
                final_verdict = 'BÌNH'
                pct = 50
            pct = max(5, min(95, int(pct)))
        
        # --- Build output ---
        impact_text = ""
        if impacts:
            impact_text = f"\n**📌 TÁC ĐỘNG VÀO CHU THỂ ({dung_than}):**\n"
            for imp in impacts:
                impact_text += f"- {imp}\n"
        
        # --- Trả lời trực tiếp câu hỏi ---
        direct_answer = self._generate_direct_answer(question, dung_than, final_verdict, pct,
                                                     0, 0, evidence, impacts,
                                                     ky_mon_reason, luc_hao_reason, mai_hoa_reason,
                                                     age_numbers=age_numbers, count_numbers=count_numbers,
                                                     chart_data=chart_data,
                                                     lh_factors=kwargs.get('lh_factors'),
                                                     km_factors=kwargs.get('km_factors'),
                                                     mh_factors=kwargs.get('mh_factors'),
                                                     luc_hao_data=luc_hao_data,
                                                     mai_hoa_data=kwargs.get('mai_hoa_data'))
        
        return impact_text, direct_answer, evidence
    
    def _calc_competition_scores(self, chart_data, luc_hao_data, mai_hoa_data):
        _the_score = 0
        _ung_score = 0
        _the_ung_detail = []
        
        # --- LỤC HÀO: Thế vs Ứng ---
        if luc_hao_data and isinstance(luc_hao_data, dict):
            _lh_ban = luc_hao_data.get('ban', {})
            _lh_haos = _lh_ban.get('haos') or _lh_ban.get('details', [])
            _the_h = None
            _ung_h = None
            for _h in _lh_haos:
                _tu = str(_h.get('the_ung', '') or _h.get('marker', ''))
                if 'Thế' in _tu:
                    _the_h = _h
                elif 'Ứng' in _tu:
                    _ung_h = _h
            if _the_h and _ung_h:
                _the_hanh = _the_h.get('ngu_hanh', '')
                _ung_hanh = _ung_h.get('ngu_hanh', '')
                _the_vs = str(_the_h.get('vuong_suy', '') or _the_h.get('strength', ''))
                _ung_vs = str(_ung_h.get('vuong_suy', '') or _ung_h.get('strength', ''))
                # Điểm Vượng/Suy
                _VS_SCORE = {'Đế Vượng': 10, 'Lâm Quan': 8, 'Trường Sinh': 6, 'Mộc Dục': 4,
                             'Quan Đới': 3, 'Dưỡng': 2, 'Thai': 1, 'Suy': -4, 'Bệnh': -6,
                             'Tử': -8, 'Mộ': -5, 'Tuyệt': -10}
                for _stage, _sc in _VS_SCORE.items():
                    if _stage in _the_vs:
                        _the_score += _sc
                        break
                for _stage, _sc in _VS_SCORE.items():
                    if _stage in _ung_vs:
                        _ung_score += _sc
                        break
                # Sinh/Khắc
                if SINH.get(_the_hanh) == _ung_hanh:
                    _the_score -= 3  # Thế sinh Ứng = Thế hao tổn
                    _ung_score += 3
                elif KHAC.get(_the_hanh) == _ung_hanh:
                    _the_score += 5  # Thế khắc Ứng = Thế thắng
                    _ung_score -= 5
                elif SINH.get(_ung_hanh) == _the_hanh:
                    _the_score += 3  # Ứng sinh Thế = Thế được lợi
                    _ung_score -= 3
                elif KHAC.get(_ung_hanh) == _the_hanh:
                    _the_score -= 5  # Ứng khắc Thế = Thế thua
                    _ung_score += 5
                _the_ung_detail.append(f"LH: Thế({_the_hanh}/{_the_vs}) {_the_score:+d} vs Ứng({_ung_hanh}/{_ung_vs}) {_ung_score:+d}")
        
        # --- KỲ MÔN: Chủ (Nhật Can) vs Khách (Thời Can) ---
        if chart_data and isinstance(chart_data, dict):
            _can_ngay_km = chart_data.get('can_ngay', '')
            _can_gio_km = chart_data.get('can_gio', '')
            _hanh_chu = CAN_NGU_HANH.get(_can_ngay_km, '')
            _hanh_khach = CAN_NGU_HANH.get(_can_gio_km, '')
            if _hanh_chu and _hanh_khach:
                if KHAC.get(_hanh_chu) == _hanh_khach:
                    _the_score += 4
                elif SINH.get(_hanh_chu) == _hanh_khach:
                    _the_score -= 2
                elif KHAC.get(_hanh_khach) == _hanh_chu:
                    _ung_score += 4
                elif SINH.get(_hanh_khach) == _hanh_chu:
                    _ung_score -= 2
                _the_ung_detail.append(f"KM: Chủ({_can_ngay_km}/{_hanh_chu}) vs Khách({_can_gio_km}/{_hanh_khach})")
        
        # --- MAI HOA: Thể vs Dụng ---
        if mai_hoa_data and isinstance(mai_hoa_data, dict):
            _mh_hanh_thuong = mai_hoa_data.get('hanh_thuong', '')
            _mh_hanh_ha = mai_hoa_data.get('hanh_ha', '')
            _mh_dong = mai_hoa_data.get('dong_hao', 0)
            if _mh_dong and int(_mh_dong) <= 3:
                _the_hanh_mh = _mh_hanh_thuong
                _dung_hanh_mh = _mh_hanh_ha
            else:
                _the_hanh_mh = _mh_hanh_ha
                _dung_hanh_mh = _mh_hanh_thuong
            if _the_hanh_mh and _dung_hanh_mh:
                if KHAC.get(_the_hanh_mh) == _dung_hanh_mh:
                    _the_score += 3
                elif SINH.get(_dung_hanh_mh) == _the_hanh_mh:
                    _the_score += 2
                elif KHAC.get(_dung_hanh_mh) == _the_hanh_mh:
                    _ung_score += 3
                elif SINH.get(_the_hanh_mh) == _dung_hanh_mh:
                    _ung_score += 2
                _the_ung_detail.append(f"MH: Thể({_the_hanh_mh}) vs Dụng({_dung_hanh_mh})")

        return _the_score, _ung_score, _the_ung_detail

    def _generate_direct_answer(self, question, dung_than, final_verdict, pct,
                                 cat_count, hung_count, evidence, impacts,
                                 ky_mon_reason, luc_hao_reason, mai_hoa_reason,
                                 age_numbers=None, count_numbers=None, chart_data=None,
                                 lh_factors=None, km_factors=None, mh_factors=None,
                                 luc_hao_data=None, mai_hoa_data=None):
        """
        V34.4: Sinh câu trả lời TRỰC TIẾP + THÁM TỬ KIỂM CHỨNG.
        - Bước 1: THÁM TỬ kiểm tra % có đúng ko
        - Bước 2: Xác định DẠNG câu hỏi (CÓ/KHÔNG, AI, CÁI GÌ, THẾ NÀO, Ở ĐÂU, KHI NÀO...)
        - Bước 3: Trả lời LINH HOẠT dựa trên Vạn Vật Loại Tượng
        """
        q = question.lower()
        # V36.1: Normalize không dấu → có dấu (same as _detect_category)
        _THAMTU_NORM = {
            # Sống/Chết
            'qua duoc': 'qua được', 'qua khoi': 'qua khỏi', 'chet chua': 'chết chưa',
            'con song': 'còn sống', 'da mat': 'đã mất', 'qua doi': 'qua đời',
            'tu vong': 'tử vong', 'song sot': 'sống sót', 'benh nang': 'bệnh nặng',
            'nguy kich': 'nguy kịch', 'hap hoi': 'hấp hối', 'cuu duoc': 'cứu được',
            'mat roi': 'mất rồi', 'song hay': 'sống hay', 'song khong': 'sống không',
            # CÓ/KHÔNG + NÊN/KHÔNG NÊN
            'co nen': 'có nên', 'co duoc': 'có được', 'duoc khong': 'được không',
            'nen khong': 'nên không', 'co khong': 'có không',
            'co tot': 'có tốt', 'co thanh': 'có thành', 'co do': 'có đỗ',
            'co dat': 'có đạt', 'co thang': 'có thắng', 'co loi': 'có lời',
            # THẾ NÀO / RA SAO
            'the nao': 'thế nào', 'nhu the nao': 'như thế nào', 'ra sao': 'ra sao',
            'nhu nao': 'như nào', 'sao roi': 'sao rồi', 'tinh sao': 'tính sao',
            # KHI NÀO / BAO GIỜ
            'khi nao': 'khi nào', 'bao gio': 'bao giờ', 'luc nao': 'lúc nào',
            'thoi diem': 'thời điểm', 'thang nao': 'tháng nào', 'nam nao': 'năm nào',
            'ngay nao': 'ngày nào', 'mua nao': 'mùa nào',
            # Ở ĐÂU / TÌM ĐÂU
            'o dau': 'ở đâu', 'cho nao': 'chỗ nào', 'huong nao': 'hướng nào',
            'phuong nao': 'phương nào', 'noi nao': 'nơi nào', 'tim dau': 'tìm đâu',
            'de dau': 'để đâu', 'de cho': 'để chỗ', 'de o': 'để ở',
            'cat dau': 'cất đâu', 'cat o': 'cất ở', 'giau dau': 'giấu đâu',
            'vi tri': 'vị trí', 'nam dau': 'nằm đâu',
            # CÁI GÌ / VẬT GÌ / SẢN PHẨM  
            'cai gi': 'cái gì', 'dieu gi': 'điều gì', 'lam gi': 'làm gì',
            'san pham': 'sản phẩm', 'hang gi': 'hàng gì', 'do gi': 'đồ gì',
            'loai gi': 'loại gì', 'mat hang': 'mặt hàng', 'san xuat gi': 'sản xuất gì',
            'ban gi': 'bán gì', 'kinh doanh gi': 'kinh doanh gì', 'buon gi': 'buôn gì',
            'mua gi': 'mua gì', 'dau tu gi': 'đầu tư gì', 'nganh gi': 'ngành gì',
            'nghe gi': 'nghề gì', 'trong gi': 'trồng gì', 'nuoi gi': 'nuôi gì',
            'bang gi': 'bằng gì', 'la gi': 'là gì', 'gi vay': 'gì vậy', 'gi day': 'gì đây',
            'thuoc loai': 'thuộc loại', 'loai nao': 'loại nào', 'kieu gi': 'kiểu gì',
            'san xuat cai': 'sản xuất cái', 'san xuat': 'sản xuất',
            'vat gi': 'vật gì', 'chuyen gi': 'chuyện gì', 'viec gi': 'việc gì',
            'muon gi': 'muốn gì', 'hoi gi': 'hỏi gì', 'noi gi': 'nói gì',
            # MÀU SẮC
            'mau gi': 'màu gì', 'mau nao': 'màu nào', 'mau sac': 'màu sắc',
            'chon mau': 'chọn màu', 'son mau': 'sơn màu',
            # SỐ
            'so may': 'số mấy', 'chon so': 'chọn số', 'so nao': 'số nào',
            'bien so': 'biển số', 'so dep': 'số đẹp', 'so may man': 'số may mắn',
            # GIẢI PHÁP
            'lam sao': 'làm sao', 'giai phap': 'giải pháp', 'cach nao': 'cách nào',
            'khac phuc': 'khắc phục', 'cai thien': 'cải thiện', 'hoa giai': 'hóa giải',
            # SO SÁNH
            'chon cai nao': 'chọn cái nào', 'nen chon': 'nên chọn',
            'cai nao tot': 'cái nào tốt', 'lua chon': 'lựa chọn',
            # LỪA ĐẢO
            'lua dao': 'lừa đảo', 'that gia': 'thật giả', 'dang tin': 'đáng tin',
            'co that': 'có thật', 'gian lan': 'gian lận',
            # TÌNH CẢM
            'hon nhan': 'hôn nhân', 'tinh cam': 'tình cảm', 'chia tay': 'chia tay',
            'quay lai': 'quay lại', 'nguoi yeu': 'người yêu', 'vo chong': 'vợ chồng',
            'ket hon': 'kết hôn', 'tai hop': 'tái hợp', 'ngoai tinh': 'ngoại tình',
            'chung thuy': 'chung thủy', 'dam cuoi': 'đám cưới',
            # BỆNH TẬT
            'benh gi': 'bệnh gì', 'suc khoe': 'sức khỏe', 'khoi benh': 'khỏi bệnh',
            'phau thuat': 'phẫu thuật', 'trieu chung': 'triệu chứng',
            # MẤT ĐỒ
            'mat do': 'mất đồ', 'tim do': 'tìm đồ', 'tim thay': 'tìm thấy',
            'danh mat': 'đánh mất', 'mat xe': 'mất xe', 'mat tien': 'mất tiền',
            # KIỆN TỤNG
            'tranh chap': 'tranh chấp', 'thang kien': 'thắng kiện',
            'phap ly': 'pháp lý', 'to cao': 'tố cáo', 'khieu nai': 'khiếu nại',
            # THỜI TIẾT
            'thoi tiet': 'thời tiết',
            # THAI SẢN
            'mang thai': 'mang thai', 'co thai': 'có thai', 'sinh con': 'sinh con',
            'trai hay gai': 'trai hay gái', 'gioi tinh': 'giới tính', 'co bau': 'có bầu',
            # HỢP TÁC
            'hop tac': 'hợp tác', 'doi tac': 'đối tác', 'cong su': 'cộng sự',
            'chung von': 'chung vốn', 'gop von': 'góp vốn', 'lam chung': 'làm chung',
            # ĐÚNG/SAI
            'dung khong': 'đúng không', 'sai khong': 'sai không', 'dung hay sai': 'đúng hay sai',
            'co dung': 'có đúng', 'co sai': 'có sai', 'noi doi': 'nói dối', 'noi that': 'nói thật',
            # CHỜ / HÀNH ĐỘNG
            'cho hay': 'chờ hay', 'doi hay': 'đợi hay', 'nen doi': 'nên đợi',
            'nen cho': 'nên chờ', 'tien hay lui': 'tiến hay lùi', 'xuat phat': 'xuất phát',
            # NHÀ CỬA
            'xay nha': 'xây nhà', 'mua nha': 'mua nhà', 'nha moi': 'nhà mới',
            'phong thuy': 'phong thủy', 'sua nha': 'sửa nhà', 'chuyen nha': 'chuyển nhà',
            'nha dat': 'nhà đất', 'dat dai': 'đất đai', 'lo dat': 'lô đất',
            # THI CỬ
            'ket qua thi': 'kết quả thi', 'diem thi': 'điểm thi',
            'hoc hanh': 'học hành', 'xet tuyen': 'xét tuyển', 'trung tuyen': 'trúng tuyển',
            # BAO LÂU
            'bao lau': 'bao lâu', 'mat bao lau': 'mất bao lâu', 'keo dai': 'kéo dài',
            'may ngay': 'mấy ngày', 'may thang': 'mấy tháng',
            # TẠI SAO
            'tai sao': 'tại sao', 'vi sao': 'vì sao', 'nguyen nhan': 'nguyên nhân',
            'do dau': 'do đâu', 'ly do': 'lý do',
            # BAO NHIÊU  
            'bao nhieu': 'bao nhiêu', 'so luong': 'số lượng',
            'may nguoi': 'mấy người', 'may cai': 'mấy cái', 'may dua': 'mấy đứa',
            # TUỔI
            'bao nhieu tuoi': 'bao nhiêu tuổi', 'may tuoi': 'mấy tuổi',
            'nam sinh': 'năm sinh',
            # Gia đình
            'bo': 'bố', 'me': 'mẹ', 'vo': 'vợ', 'chong': 'chồng',
            'ong ngoai': 'ông ngoại', 'ba ngoai': 'bà ngoại',
            'ong noi': 'ông nội', 'ba noi': 'bà nội', 'ong': 'ông', 'ba': 'bà',
        }
        for _nd, _cd in sorted(_THAMTU_NORM.items(), key=lambda x: len(x[0]), reverse=True):
            if _nd in q:
                q = q.replace(_nd, _cd)
        lines = []
        # V40.3: Derive hanh_dt
        hanh_dt = _get_hanh_dt_from_luc_hao(luc_hao_data, dung_than)
        if not hanh_dt:
            _LT_HANH = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
            hanh_dt = _LT_HANH.get(dung_than, '')
        if not lh_factors: lh_factors = []
        if not km_factors: km_factors = []
        if not mh_factors: mh_factors = []
        
        lines.append(f'\n<div style="background:linear-gradient(135deg,#1e293b,#334155);padding:16px 20px;border-radius:12px;margin:10px 0;border-left:5px solid #f59e0b;"><span style="color:#fbbf24;font-size:1.1em;font-weight:800;">❓ CÂU HỎI:</span> <span style="color:#f1f5f9;font-size:1.05em;font-weight:600;">{question}</span></div>')
        
        # ═══════════════════════════════════════════════
        # BƯỚC 1: THÁM TỬ KIỂM CHỨNG (Detective Validator)
        # ═══════════════════════════════════════════════
        detective_issues = []
        
        # Check 1: pct phải nằm trong 5-95
        if pct < 5 or pct > 95:
            detective_issues.append(f"⚠️ pct={pct}% ngoài phạm vi [5,95]")
            pct = max(5, min(95, pct))
        
        # Check 2: verdict phải khớp với pct — V35.0: Mở rộng vùng hợp lệ
        if final_verdict == 'CÁT' and pct < 45:
            detective_issues.append(f"⚠️ verdict=CÁT nhưng pct={pct}%<45 → chỉnh verdict=BÌNH")
            final_verdict = 'BÌNH'
        elif final_verdict == 'HUNG' and pct > 55:
            detective_issues.append(f"⚠️ verdict=HUNG nhưng pct={pct}%>55 → chỉnh verdict=BÌNH")
            final_verdict = 'BÌNH'
        
        # Check 3: evidence phải có ít nhất 1 bằng chứng
        if not evidence:
            detective_issues.append(f"⚠️ Không có bằng chứng → dùng pct={pct}% làm cơ sở")
        
        # Check 4: V35.0: CHỈ CẢNH BÁO, KHÔNG override pct từ weighted_pct
        # weighted_pct đã tính chính xác từ 6 PP + 12 Trường Sinh — KHÔNG nên thay đổi
        good_impacts = [i for i in impacts if i.startswith('✅')]
        bad_impacts = [i for i in impacts if i.startswith('🔴')]
        # V35.0: ⚠️ chỉ tính là bất lợi NẾU chứa từ khóa xác thực (tránh đếm thông tin trung tính)
        REAL_BAD_KEYWORDS = ['KHẮC', 'YẾU', 'TỬ', 'TUYỆT', 'HUNG', 'GÂY HẠI', 'CHẶN', 'BẾ TẮC',
                             'NGUY HIỂM', 'MẤT MÁT', 'XUNG ĐỘT', 'CHẤM DỨT', 'SUY', 'BỊ KHẮC']
        for i in impacts:
            if i.startswith('⚠️') and any(kw in i.upper() for kw in REAL_BAD_KEYWORDS):
                bad_impacts.append(i)
        total_impacts = len(good_impacts) + len(bad_impacts)
        
        if total_impacts >= 3:
            impact_ratio = len(good_impacts) / total_impacts
            impact_pct = int(impact_ratio * 100)
            # V35.0: CHỈ CẢNH BÁO nếu chênh lệch lớn, KHÔNG override pct
            if abs(pct - impact_pct) > 30:
                detective_issues.append(
                    f"ℹ️ Lưu ý: pct={pct}% vs impact={impact_pct}% (chênh {abs(pct-impact_pct)}%)"
                    f" — GIỮ NGUYÊN weighted_pct (đã tính chính xác từ 6 PP)"
                )
        
        if detective_issues:
            lines.append(f'\n<div style="background:rgba(30,27,75,0.8);padding:12px 16px;border-radius:10px;border-left:4px solid #f59e0b;"><b style="color:#fbbf24;font-size:1em;">🔍 THÁM TỬ KIỂM CHỨNG</b></div>')
            for issue in detective_issues:
                lines.append(f"- {issue}")
            lines.append(f'- <span style="color:#16a34a;font-weight:700;">✅ Đã hiệu chỉnh → pct={pct}%, verdict={final_verdict}</span>')
        
        # ═══════════════════════════════════════════════
        # BƯỚC 2: Lấy Vạn Vật Loại Tượng chi tiết — V40.6: dùng file TỔNG HỢP
        # ═══════════════════════════════════════════════
        vv_key, vv_data = _get_van_vat_from_pct(pct)
        # V40.6: Lấy thêm Vạn Vật TỔNG HỢP đầy đủ (5 giác quan + đồ vật + người)
        _vv_full_text = ''
        try:
            from van_vat_tong_hop import smart_van_vat_for_question
            _ts_map = {}
            if pct >= 75: _ts_map = 'Đế Vượng'
            elif pct >= 55: _ts_map = 'Lâm Quan'
            elif pct >= 40: _ts_map = 'Quan Đới'
            elif pct >= 25: _ts_map = 'Suy'
            elif pct >= 10: _ts_map = 'Bệnh'
            else: _ts_map = 'Tử'
            # V40.9: Smart filter cho AI Online
            _vv_full_text, _vv_topics = smart_van_vat_for_question(hanh_dt or 'Thổ', _ts_map, question)
        except Exception:
            pass
        
        # Lấy Bát Quái info từ chart
        cd = chart_data if isinstance(chart_data, dict) else {}
        the_quai = cd.get('the_quai', '')
        dung_quai = cd.get('dung_quai', '')
        ung_quai = cd.get('ung_quai', '')
        
        # Icon theo verdict
        if final_verdict == 'CÁT':
            icon = '🟢'
        elif final_verdict == 'HUNG':
            icon = '🔴'
        else:
            icon = '🟡'
        
        # V40.6: Tái khẳng định câu hỏi ở TẤT CẢ dạng
        _q_short = question[:80] if len(question) > 80 else question
        
        # ═══════════════════════════════════════════════
        # BƯỚC 3: XÁC ĐỊNH DẠNG CÂU HỎI + TRẢ LỜI LINH HOẠT
        # ═══════════════════════════════════════════════
        
        # V42.8f FIX: THẮNG THUA / COMPETITION phải check ĐẦU TIÊN
        # (tránh "ai thắng" bị catch bởi pattern "ai " → hiển thị sai)
        is_competition = _is_competition_question(question)
        if is_competition:
            _side_a_disp, _side_b_disp = _extract_two_sides(question)
            # Verdict color
            _comp_color = '#22c55e' if pct >= 55 else '#ef4444' if pct <= 40 else '#eab308'
            
            # --- V42.9: TÍNH ĐIỂM CHỦ VS KHÁCH THỰC SỰ ---
            _the_s, _ung_s, _the_ung_detail = self._calc_competition_scores(chart_data, luc_hao_data, mai_hoa_data)
            _diff = _the_s - _ung_s
            
            if _diff >= 5:
                _winner = _side_a_disp
                _loser = _side_b_disp
                _win_icon = '✅'
                _win_text = f"THẮNG ĐẬM (Điểm: +{_diff})"
            elif _diff >= 2:
                _winner = _side_a_disp
                _loser = _side_b_disp
                _win_icon = '↗️'
                _win_text = f"HƠI TRỘI HƠN (Điểm: +{_diff})"
            elif _diff >= -1:
                _winner = f'{_side_a_disp} ≈ {_side_b_disp}'
                _loser = 'HÒA'
                _win_icon = '⚖️'
                _win_text = f"HÒA / CÂN TÀI (Chênh: {_diff:+d})"
            elif _diff >= -4:
                _winner = _side_b_disp
                _loser = _side_a_disp
                _win_icon = '↗️'
                _win_text = f"HƠI TRỘI HƠN (Điểm: {abs(_diff)})"
            else:
                _winner = _side_b_disp
                _loser = _side_a_disp
                _win_icon = '✅'
                _win_text = f"THẮNG ĐẬM (Điểm: {abs(_diff)})"
            
            lines.append(
                f'\n<div style="background:linear-gradient(135deg,#064e3b,#065f46);padding:22px;border-radius:16px;'
                f'border:3px solid {_comp_color};margin:12px 0;box-shadow:0 4px 20px rgba(0,0,0,0.4);">'
                f'<span style="font-size:1.4em;font-weight:900;color:#fbbf24;">⚔️ PHÂN TÍCH THẮNG THUA (CHỦ VS KHÁCH)</span><br><br>'
                f'<span style="font-size:1.5em;font-weight:900;color:#ffffff;">'
                f'{_side_a_disp} <span style="color:#94a3b8;">vs</span> {_side_b_disp}</span><br><br>'
                f'<span style="font-size:1.3em;font-weight:900;color:{_comp_color};">'
                f'{_win_icon} PHÁN QUYẾT: {_winner} {_win_text}</span>'
                f'</div>'
            )
            
            # Liệt kê chi tiết điểm số Ngũ Hành
            lines.append(f"\n**📊 CHI TIẾT ĐIỂM SỐ NGŨ HÀNH (Chủ: {_the_s} vs Khách: {_ung_s})**")
            for _detail in _the_ung_detail:
                lines.append(f"- {_detail}")
            
            lines.append(f"\n**🔍 Nguồn phân bổ lực lượng:**")
            lines.append(f"- Lục Hào: Thế = {_side_a_disp}, Ứng = {_side_b_disp}")
            lines.append(f"- Kỳ Môn: Nhật Can (Chủ = {_side_a_disp}), Thời Can (Khách = {_side_b_disp})")
            lines.append(f"- Mai Hoa: Thể Quái = {_side_a_disp}, Dụng Quái = {_side_b_disp}")
        
        # THẾ NÀO / RA SAO / NHƯ NÀO / NGHĨ GÌ / HÀNH ĐỘNG — mô tả chi tiết
        if any(k in q for k in ['thế nào', 'ra sao', 'như thế nào', 'như nào', 'sao rồi',
                                  'nghĩ gì', 'hành động', 'làm gì', 'xử lý', 'tính sao']):
            _color = '#16a34a' if pct >= 55 else '#dc2626' if pct <= 40 else '#ca8a04'
            lines.append(f'\n<div style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:18px 22px;border-radius:14px;border-left:6px solid {_color};margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:{_color};">{icon} VỀ "{_q_short}"</span><br><span style="font-size:1.15em;color:#f1f5f9;font-weight:700;">{vv_data["cap"]} — {pct}%</span></div>')
            lines.append(f'\n<b style="color:#94a3b8;font-size:0.95em;">📋 Mô tả chi tiết (Vạn Vật Loại Tượng {hanh_dt} × {_ts_map}):</b>')
            if _vv_full_text:
                for _line in _vv_full_text.split('\n')[:30]:
                    if _line.strip():
                        lines.append(f"  {_line}")
            else:
                lines.append(f"- 👤 Con người: {vv_data.get('con_nguoi', '?')}")
                lines.append(f"- 🔧 Tình trạng: {vv_data.get('tinh_trang', '?')}")
                lines.append(f"- 🎨 Chất lượng: {vv_data.get('chat_luong', '?')}")
            if pct >= 60:
                lines.append(f"\n→ Tình hình **THUẬN LỢI** ({pct}%). Xu hướng tốt lên.")
            elif pct <= 40:
                lines.append(f"\n→ Tình hình **KHÓ KHĂN** ({pct}%). Cần chú ý, cải thiện.")
            else:
                lines.append(f"\n→ Tình hình **TRUNG BÌNH** ({pct}%). Ổn nhưng cần nỗ lực thêm.")
        
        # AI / NGƯỜI NÀO — dùng Lục Thân để xác định
        if any(k in q for k in ['ai ', 'người nào', 'ai đó', 'người gì', 'người như thế nào']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: Đặc điểm người được hỏi ({dung_than})**")
            lines.append(f"\n📋 **Mô tả (Vạn Vật Loại Tượng — {vv_key}):**")
            lines.append(f"- 👤 {vv_data.get('con_nguoi', '?')}")
            lines.append(f"- 🎨 Màu sắc liên tưởng: {vv_data.get('mau_sac', '?')}")

            lines.append(f"- 📏 Dáng vóc: {vv_data.get('kich_thuoc', '?')}")
            lines.append(f"- ⚡ Tâm tính: {'Mạnh mẽ, tự tin' if pct >= 60 else 'Yếu đuối, do dự' if pct <= 40 else 'Trung tính, ổn định'}")
            if dung_than == 'Quan Quỷ':
                lines.append(f"- 🏢 Mối quan hệ: Sếp, cấp trên, chồng (nữ), đối tác")
            elif dung_than == 'Thê Tài':
                lines.append(f"- 💰 Mối quan hệ: Vợ, người yêu, khách hàng, đối tượng tài chính")
            elif dung_than == 'Phụ Mẫu':
                lines.append(f"- 👨‍👩‍👧 Mối quan hệ: Bố mẹ, bề trên, thầy cô, người bảo trợ")
            elif dung_than == 'Tử Tôn':
                lines.append(f"- 👶 Mối quan hệ: Con cái, học trò, người dưới quyền")
            elif dung_than == 'Huynh Đệ':
                lines.append(f"- 🤝 Mối quan hệ: Anh em, bạn bè, đồng nghiệp, đối thủ")
        
        # CÁI GÌ / VẬT GÌ / SẢN PHẨM GÌ / ĐỒ GÌ — V42.0: Vạn Vật Loại Tượng chuyên sâu
        if any(k in q for k in ['cái gì', 'điều gì', 'muốn gì', 'hỏi gì', 'nói gì', 'làm gì',
                                   'chuyện gì', 'việc gì', 'vật gì', 'sản phẩm', 'hàng gì',
                                   'đồ gì', 'loại gì', 'mặt hàng', 'sản xuất gì', 'bán gì',
                                   'kinh doanh gì', 'buôn gì', 'mua gì', 'đầu tư gì', 'ngành gì',
                                   'nghề gì', 'trồng gì', 'nuôi gì', 'bằng gì', 'là gì',
                                   'gì vậy', 'gì đây', 'thuộc loại', 'loại nào', 'kiểu gì']):
            # V42.0: SẢN PHẨM CỤ THỂ theo Hành DT — chi tiết hơn
            HANH_SAN_PHAM = {
                'Mộc': '🌳 GỖ, GIẤY, VẢI, may mặc, nội thất gỗ, sách vở, thuốc thảo dược, rau quả, nông sản, cây cảnh, đồ handmade',
                'Hỏa': '🔥 ĐIỆN TỬ, công nghệ, ánh sáng, năng lượng, mỹ phẩm, thực phẩm nấu chín, nhà hàng, quảng cáo, truyền thông, giải trí',
                'Thổ': '🏔️ BẤT ĐỘNG SẢN, vật liệu xây dựng, gạch đá, xi măng, gốm sứ, thực phẩm chế biến, nông nghiệp, khoáng sản',
                'Kim': '⚔️ KIM LOẠI, máy móc, ô tô, xe máy, thiết bị cơ khí, trang sức, vàng bạc, công nghiệp nặng, linh kiện',
                'Thủy': '💧 NƯỚC UỐNG, đồ uống, thủy sản, vận tải biển, du lịch, logistics, hóa chất lỏng, dầu mỡ, nhà hàng hải sản',
            }
            # FIX V42.9
            hanh_dt = _get_hanh_dt_from_luc_hao(luc_hao_data, dung_than)
            if not hanh_dt:
                _LT_HANH = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
                hanh_dt = _LT_HANH.get(dung_than, 'Thổ')

            HANH_HUONG = {'Mộc': 'Đông', 'Hỏa': 'Nam', 'Thổ': 'Trung Tâm', 'Kim': 'Tây', 'Thủy': 'Bắc'}
            HANH_MAU = {'Mộc': 'Xanh lá', 'Hỏa': 'Đỏ, cam', 'Thổ': 'Vàng, nâu', 'Kim': 'Trắng, bạc', 'Thủy': 'Đen, xanh dương'}
            HANH_CHAT = {'Mộc': 'Gỗ, sợi, organic', 'Hỏa': 'Nhựa, điện tử', 'Thổ': 'Đất, gốm, xi măng', 'Kim': 'Kim loại, inox', 'Thủy': 'Lỏng, dầu, nước'}
            HANH_HINH = {'Mộc': 'Dài, hình trụ, thẳng', 'Hỏa': 'Nhọn, tam giác', 'Thổ': 'Vuông, dẹt', 'Kim': 'Tròn, hình cầu', 'Thủy': 'Lượn sóng, không đều'}
            
            # Map DT → nội dung sự việc
            dt_noi_dung = {
                'Phụ Mẫu': 'NHÀ CỬA, GIẤY TỜ, HỌC HÀNH, BỐ MẸ/BỀ TRÊN',
                'Thê Tài': 'TIỀN BẠC, TÀI SẢN, MUA BÁN, TÌNH CẢM',
                'Quan Quỷ': 'CÔNG VIỆC, BỆNH TẬT, KIỆN TỤNG, SẾP/CHỒNG',
                'Tử Tôn': 'CON CÁI, GIẢI TRÍ, THUỐC MEN, VẬT NUÔI',
                'Huynh Đệ': 'ANH EM, BẠN BÈ, CẠNH TRANH, TIÊU XÀI',
            }
            
            _sp = HANH_SAN_PHAM.get(hanh_dt, '?')
            _huong = HANH_HUONG.get(hanh_dt, '?')
            _mau = HANH_MAU.get(hanh_dt, '?')
            _chat = HANH_CHAT.get(hanh_dt, '?')
            _hinh = HANH_HINH.get(hanh_dt, '?')
            _noidung = dt_noi_dung.get(dung_than, '?')
            
            # Mức chất lượng theo %
            if pct >= 75: _quality = 'CAO CẤP, đắt tiền, brand lớn, quy mô lớn'
            elif pct >= 55: _quality = 'TRUNG-CAO, chất lượng khá, quy mô vừa'
            elif pct >= 40: _quality = 'TRUNG BÌNH, phổ thông, quy mô nhỏ-vừa'
            elif pct >= 20: _quality = 'THẤP, cũ, secondhand, nhỏ, giá rẻ'
            else: _quality = 'RẤT NHỎ, hư hỏng, phế liệu'
            
            _qcolor = '#22c55e' if pct >= 55 else '#ef4444' if pct <= 40 else '#eab308'
            
            lines.append(
                f'\n<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);padding:22px;border-radius:14px;'
                f'border-left:6px solid {_qcolor};margin:12px 0;">'
                f'<span style="font-size:1.3em;font-weight:900;color:#c4b5fd;">🔮 PHÂN TÍCH VẠN VẬT: "{_q_short}"</span><br><br>'
                f'<span style="font-size:1.15em;font-weight:800;color:{_qcolor};">📦 Hành {hanh_dt} → {_sp}</span><br><br>'
                f'<span style="color:#e2e8f0;font-size:1.05em;">'
                f'- <b>Lĩnh vực (DT {dung_than}):</b> {_noidung}<br>'
                f'- <b>Chất liệu:</b> {_chat}<br>'
                f'- <b>Hình dạng:</b> {_hinh}<br>'
                f'- <b>Màu sắc:</b> {_mau}<br>'
                f'- <b>Hướng tốt:</b> {_huong}</span><br><br>'
                f'<span style="color:{_qcolor};font-weight:700;">📊 Mức chất lượng: {_quality} ({pct}%)</span>'
                f'</div>'
            )
            
            # Hành nên tránh (bị khắc)
            HANH_KHAC = {'Mộc': 'Kim', 'Hỏa': 'Thủy', 'Thổ': 'Mộc', 'Kim': 'Hỏa', 'Thủy': 'Thổ'}
            _hanh_tranh = HANH_KHAC.get(hanh_dt, '')
            if _hanh_tranh and _hanh_tranh in HANH_SAN_PHAM:
                lines.append(f"\n⛔ **NÊN TRÁNH (Hành {_hanh_tranh} khắc {hanh_dt}):**")
                lines.append(f"- {HANH_SAN_PHAM[_hanh_tranh]}")
            
            # Vạn Vật tổng hợp nếu có
            if _vv_full_text:
                lines.append(f"\n📋 **VẠN VẬT LOẠI TƯỢNG CHI TIẾT (Hành {hanh_dt}):**")
                for _vvl in _vv_full_text.split('\n')[:10]:
                    if _vvl.strip():
                        lines.append(f"  {_vvl.strip()}")
        
        # V36.1: SỐNG/CHẾT — PHẢI CHECK TRƯỚC CÓ/KHÔNG
        elif any(k in q for k in ['mất hay chưa', 'chết chưa', 'còn sống', 'sống không',
                                   'qua khỏi', 'cứu được', 'mất chưa', 'đã mất', 'sống hay',
                                   'mất rồi', 'chết hay', 'sống chết', 'còn hay mất',
                                   'qua đời', 'tử vong', 'sống sót', 'qua được',
                                   'bệnh nặng', 'nguy kịch', 'hấp hối']):
            if pct >= 50:
                lines.append(f'\n<div style="background:#052e16;padding:18px;border-radius:14px;border-left:6px solid #22c55e;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#22c55e;">✅ CÂU TRẢ LỜI: CÒN SỐNG</span><br><span style="color:#bbf7d0;font-size:1.1em;">{dung_than} có SINH KHÍ ({pct}%)</span></div>')
                lines.append(f"- {dung_than} VƯỢNG/BÌNH → còn sinh khí, có thể hồi phục.")
                if any('động' in str(ev).lower() for ev in good_impacts):
                    lines.append(f"- DT phát ĐỘNG = đang hoạt động, có sự sống.")
                if any('sinh' in str(ev).lower() for ev in good_impacts):
                    lines.append(f"- Có yếu tố SINH DT = được nuôi dưỡng, hỗ trợ.")
            elif pct >= 40:
                lines.append(f'\n<div style="background:#422006;padding:18px;border-radius:14px;border-left:6px solid #f59e0b;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#fbbf24;">⚠️ CÂU TRẢ LỜI: CÒN SỐNG nhưng RẤT YẾU</span><br><span style="color:#fef3c7;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- {dung_than} suy nhưng chưa tuyệt → vẫn còn nhưng nguy hiểm.")
                lines.append(f"- Cần can thiệp KHẨN CẤP.")
            else:
                lines.append(f'\n<div style="background:#450a0a;padding:18px;border-radius:14px;border-left:6px solid #ef4444;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#ef4444;">🔴 CÂU TRẢ LỜI: ĐÃ MẤT hoặc NGUY KỊCH</span><br><span style="color:#fecaca;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- {dung_than} SUY TUYỆT → sinh khí cạn kiệt.")
                if any('tuần không' in str(ev).lower() for ev in bad_impacts):
                    lines.append(f"- DT Tuần Không = HƯ VÔ → ĐÃ MẤT.")
                if any('tuyệt' in str(ev).lower() for ev in bad_impacts):
                    lines.append(f"- DT Hóa Tuyệt → giai đoạn TUYỆT = kết thúc.")
        
        # V36.1: CÓ NÊN — Tách riêng TRƯỚC CÓ/KHÔNG, thresholds khớp Phase D (55/45)
        elif any(k in q for k in ['có nên', 'nên không', 'nên hay']):
            if pct >= 55:
                lines.append(f'\n<div style="background:#052e16;padding:18px;border-radius:14px;border-left:6px solid #22c55e;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#22c55e;">✅ CÂU TRẢ LỜI: NÊN — THUẬN LỢI</span><br><span style="color:#bbf7d0;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- {dung_than} VƯỢNG, thời điểm tốt. Nên tiến hành.")
            elif pct >= 45:
                lines.append(f'\n<div style="background:#422006;padding:18px;border-radius:14px;border-left:6px solid #eab308;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#fbbf24;">🟡 CÓ THỂ nhưng CẦN THẬN TRỌNG</span><br><span style="color:#fef3c7;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- Thế trận chưa rõ ({len(good_impacts)} thuận vs {len(bad_impacts)} nghịch). Chuẩn bị phương án B.")
            else:
                lines.append(f'\n<div style="background:#450a0a;padding:18px;border-radius:14px;border-left:6px solid #ef4444;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#ef4444;">🔴 KHÔNG NÊN — BẤT LỢI</span><br><span style="color:#fecaca;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- {dung_than} SUY, nhiều trở ngại. Chờ thời điểm tốt hơn.")
        
        # CÓ/KHÔNG — thresholds khớp Phase D (55/50/45)
        elif any(k in q for k in ['có được', 'được không', 'có thể',
                                 'có thành', 'có đỗ', 'có đạt', 'có thắng', 'có tốt',
                                 'có không', 'không']):
            if pct >= 55:
                lines.append(f'\n<div style="background:#052e16;padding:18px;border-radius:14px;border-left:6px solid #22c55e;margin:12px 0;"><span style="font-size:1.4em;font-weight:900;color:#22c55e;">✅ CÓ — Thành công</span><br><span style="color:#bbf7d0;font-size:1.2em;font-weight:700;">{pct}%</span></div>')
                lines.append(f"- {dung_than} VƯỢNG, thuận lợi. Nắm bắt cơ hội.")
            elif pct >= 50:
                lines.append(f'\n<div style="background:#052e16;padding:18px;border-radius:14px;border-left:6px solid #86efac;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#86efac;">🟢 CÓ nhưng KHÓ</span><br><span style="color:#bbf7d0;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- Nghiêng CÓ ({len(good_impacts)} thuận vs {len(bad_impacts)} nghịch). Cần nỗ lực thêm.")
            elif pct >= 45:
                lines.append(f'\n<div style="background:#422006;padding:18px;border-radius:14px;border-left:6px solid #eab308;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#fbbf24;">🟡 KHÓ nhưng chưa hẳn KHÔNG</span><br><span style="color:#fef3c7;font-size:1.1em;">{pct}%</span></div>')
                lines.append(f"- Nghiêng KHÔNG ({len(bad_impacts)} nghịch vs {len(good_impacts)} thuận). Cần nỗ lực lớn.")
            else:
                lines.append(f'\n<div style="background:#450a0a;padding:18px;border-radius:14px;border-left:6px solid #ef4444;margin:12px 0;"><span style="font-size:1.4em;font-weight:900;color:#ef4444;">🔴 KHÔNG — Bất lợi</span><br><span style="color:#fecaca;font-size:1.2em;font-weight:700;">{pct}%</span></div>')
                lines.append(f"- {dung_than} SUY, nhiều trở ngại. Nên chờ hoặc đổi hướng.")
        
        # KHI NÀO / THÁNG NÀO / BAO GIỜ — trả lời CỤ THỂ tháng/chi
        elif any(k in q for k in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'khi nao',
                                   'tháng nào', 'tháng mấy', 'năm nào', 'ngày nào', 'mùa nào']):
            # Lấy hành DT để tính Ứng Kỳ (V42.9: đã tính ở trên, tái sử dụng)
            if not hanh_dt:
                _LT_HANH_UK = {
                    'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa',
                    'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc', 'Bản Thân': 'Thổ'
                }
                hanh_dt = _LT_HANH_UK.get(dung_than, 'Thổ')
            
            # Chi → Tháng Âm Lịch
            CHI_THANG = {
                'Dần': 'T1 ÂL (Giêng)', 'Mão': 'T2 ÂL', 'Thìn': 'T3 ÂL',
                'Tị': 'T4 ÂL', 'Ngọ': 'T5 ÂL', 'Mùi': 'T6 ÂL',
                'Thân': 'T7 ÂL', 'Dậu': 'T8 ÂL', 'Tuất': 'T9 ÂL',
                'Hợi': 'T10 ÂL', 'Tý': 'T11 ÂL', 'Sửu': 'T12 ÂL',
            }
            # Chi → Giờ (12 thời thần)
            CHI_GIO = {
                'Tý': '23h-1h', 'Sửu': '1h-3h', 'Dần': '3h-5h',
                'Mão': '5h-7h', 'Thìn': '7h-9h', 'Tị': '9h-11h',
                'Ngọ': '11h-13h', 'Mùi': '13h-15h', 'Thân': '15h-17h',
                'Dậu': '17h-19h', 'Tuất': '19h-21h', 'Hợi': '21h-23h',
            }
            # Chi → Năm gần nhất (từ 2024-2036)
            CHI_NAM = {
                'Tý': [2024, 2036], 'Sửu': [2025, 2037], 'Dần': [2026, 2038],
                'Mão': [2027, 2039], 'Thìn': [2028, 2040], 'Tị': [2029, 2041],
                'Ngọ': [2030, 2042], 'Mùi': [2031, 2043], 'Thân': [2032, 2044],
                'Dậu': [2033, 2045], 'Tuất': [2034, 2046], 'Hợi': [2035, 2047],
            }
            
            # Ngũ Hành → Chi ứng kỳ
            UNG_KY_CHI = {
                'Kim': ['Thân', 'Dậu'], 'Mộc': ['Dần', 'Mão'], 'Thủy': ['Tý', 'Hợi'],
                'Hỏa': ['Ngọ', 'Tị'], 'Thổ': ['Thìn', 'Tuất', 'Sửu', 'Mùi']
            }
            SINH_MAP = {'Kim': 'Thổ', 'Mộc': 'Thủy', 'Thủy': 'Kim', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa'}
            
            # Xác định Chi dùng (CÁT=vượng, HUNG=sinh)
            if final_verdict == 'CÁT' or pct >= 55:
                chi_dung = UNG_KY_CHI.get(hanh_dt, [])
                ly_do = f"hành {hanh_dt} vượng"
            else:
                hanh_sinh = SINH_MAP.get(hanh_dt, '')
                chi_dung = UNG_KY_CHI.get(hanh_sinh, [])
                ly_do = f"hành {hanh_sinh} sinh {hanh_dt}"
            
            ung_ky_text = _get_ung_ky(hanh_dt, final_verdict) if hanh_dt else ''
            
            # V42.8f: Tính NGÀY CỤ THỂ (DL) cho mỗi Chi ứng kỳ
            def _find_next_chi_day(target_chi_idx):
                """Tìm ngày DL tiếp theo mang Chi cho trước.
                Chi index: 0=Tý,1=Sửu,...11=Hợi
                Dùng JDN: chi_ngay = (jdn + 1) % 12
                """
                import datetime
                from xem_ngay_dep import _jdn as _jdn_calc
                today = datetime.date.today()
                CANS = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                CHIS = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                THU = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật']
                
                results = []
                for offset in range(1, 400):  # scan 400 ngày tới
                    d = today + datetime.timedelta(days=offset)
                    jdn = _jdn_calc(d.day, d.month, d.year)
                    chi_idx = (jdn + 1) % 12
                    if chi_idx == target_chi_idx:
                        can_idx = (jdn + 9) % 10
                        can_ngay = CANS[can_idx]
                        chi_ngay = CHIS[chi_idx]
                        thu = THU[d.weekday()]
                        results.append({
                            'date': d,
                            'date_str': f"{d.day:02d}/{d.month:02d}/{d.year}",
                            'thu': thu,
                            'can_chi': f"{can_ngay} {chi_ngay}",
                            'days_from_now': offset,
                        })
                        if len(results) >= 3:  # 3 ngày gần nhất
                            break
                return results
            
            def _find_next_chi_month(target_chi_idx):
                """Tìm tháng ÂL tiếp theo mang Chi cho trước."""
                import datetime
                from xem_ngay_dep import solar2lunar
                today = datetime.date.today()
                d_al, m_al, y_al, _ = solar2lunar(today.day, today.month, today.year)
                
                # Chi tháng: T1=Dần(2), T2=Mão(3),...T11=Tý(0), T12=Sửu(1)
                CHI_THANG_IDX = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 10:9, 11:10, 0:11, 1:12}
                # Reverse: từ thang_al → chi_idx
                THANG_TO_CHI = {1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:9, 9:10, 10:11, 11:0, 12:1}
                
                # Tìm tháng ÂL tiếp theo có chi = target
                for thang, chi in THANG_TO_CHI.items():
                    if chi == target_chi_idx:
                        target_month_al = thang
                        break
                else:
                    return None
                
                # Nếu tháng target > tháng hiện tại → cùng năm, ngược lại → năm sau
                if target_month_al > m_al:
                    return f"Tháng {target_month_al} ÂL năm {y_al}"
                elif target_month_al == m_al:
                    return f"Tháng {target_month_al} ÂL năm {y_al} (THÁNG NÀY!)"
                else:
                    return f"Tháng {target_month_al} ÂL năm {y_al + 1}"
            
            # Build bảng Năm-Tháng-Ngày CỤ THỂ-Giờ
            CHIS_LIST = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
            
            timing_detailed = []
            for chi in chi_dung:
                chi_idx = CHIS_LIST.index(chi) if chi in CHIS_LIST else -1
                gio = CHI_GIO.get(chi, '?')
                nam_list = CHI_NAM.get(chi, [])
                
                import datetime
                now_year = datetime.datetime.now().year
                nam_gan = [n for n in nam_list if n >= now_year]
                nam_str = str(nam_gan[0]) if nam_gan else str(nam_list[0]) if nam_list else '?'
                
                # Tìm ngày DL cụ thể
                next_days = _find_next_chi_day(chi_idx) if chi_idx >= 0 else []
                # Tìm tháng ÂL cụ thể
                next_month = _find_next_chi_month(chi_idx) if chi_idx >= 0 else None
                
                timing_detailed.append({
                    'chi': chi, 'gio': gio, 'nam': nam_str,
                    'next_days': next_days,
                    'next_month': next_month or CHI_THANG.get(chi, '?'),
                })
            
            # === OUTPUT ===
            if final_verdict == 'CÁT' or pct >= 55:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: SẮP TỚI — Thuận lợi ({pct}%)**")
            elif pct <= 40:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: CHƯA TỚI THỜI ({pct}%) — chờ Chi sinh**")
            else:
                lines.append(f"\n🟡 **CÂU TRẢ LỜI: TRONG 1-3 THÁNG TỚI ({pct}%)**")
            
            if timing_detailed:
                lines.append(f"\n📅 **ỨNG KỲ CHI TIẾT (DT hành {hanh_dt} — {ly_do}):**")
                
                for t in timing_detailed:
                    lines.append(f"\n**🔮 Chi {t['chi']}:**")
                    
                    # Ngày CỤ THỂ
                    if t['next_days']:
                        lines.append(f"- 📆 **NGÀY GẦN NHẤT:**")
                        for nd in t['next_days']:
                            delta_txt = f"(còn {nd['days_from_now']} ngày)" if nd['days_from_now'] <= 30 else f"(còn {nd['days_from_now']} ngày)"
                            lines.append(f"  → **{nd['date_str']}** ({nd['thu']}) — ngày {nd['can_chi']} {delta_txt}")
                    
                    # Giờ
                    lines.append(f"- ⏰ **GIỜ:** {t['gio']} (giờ {t['chi']})")
                    
                    # Tháng  
                    lines.append(f"- 🗓️ **THÁNG:** {t['next_month']}")
                    
                    # Năm
                    lines.append(f"- 📅 **NĂM:** {t['nam']}")
                
                # Tóm tắt ngày gần nhất
                all_first_days = []
                for t in timing_detailed:
                    if t['next_days']:
                        all_first_days.append(t['next_days'][0])
                
                if all_first_days:
                    nearest = min(all_first_days, key=lambda x: x['days_from_now'])
                    lines.append(f"\n🎯 **DỰ ĐOÁN NGÀY SỚM NHẤT:** **{nearest['date_str']}** ({nearest['thu']}) — ngày {nearest['can_chi']} — lúc {timing_detailed[0]['gio']}")
                    lines.append(f"   _(Còn {nearest['days_from_now']} ngày nữa)_")
                
                lines.append(f"\n- 📌 {ung_ky_text}")
                lines.append(f"- 💡 Ưu tiên: **ngày** > giờ > tháng (ngày gần nhất ảnh hưởng trực tiếp)")
        
        # TUỔI
        if any(k in q for k in ['bao nhiêu tuổi', 'tuổi', 'năm tuổi']):
            if age_numbers:
                all_nums = [n for _, n in age_numbers]
                avg = int(sum(all_nums) / len(all_nums)) if all_nums else 0
                detail = ', '.join(f'{pp}={n}' for pp, n in age_numbers)
                lines.append(f"\n🎂 **TUỔI: Khoảng {avg} tuổi**")
                lines.append(f"- Dựa trên {len(age_numbers)} phương pháp: {detail}")
            else:
                lines.append(f"\n🎂 **TUỔI:** Không đủ dữ liệu tuổi từ quẻ.")
        
        # BAO NHIÊU / MẤY — V41.0: Luôn trả số cụ thể
        if any(k in q for k in ['bao nhiêu', 'mấy người', 'mấy cái', 'mấy đứa', 'mấy anh', 'mấy chị', 'số lượng', 'mấy tầng', 'mấy con', 'mấy']):
            # V41.0: Nếu chưa có count_numbers → tự tính từ Ngũ Hành
            if not count_numbers and hanh_dt:
                _HD = {'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 10)}
                _hd = _HD.get(hanh_dt, (5, 10))
                if pct >= 60:
                    _so = _hd[1]  # Thành số
                elif pct >= 40:
                    _so = _hd[0]  # Sinh số
                else:
                    _so = max(1, _hd[0] - 1)
                count_numbers = [('Ngũ Hành Hà Đồ', _so)]
            
            if count_numbers:
                all_nums = [n for _, n in count_numbers]
                avg = int(round(sum(all_nums) / len(all_nums))) if all_nums else 0
                detail = ', '.join(f'{pp}={n}' for pp, n in count_numbers)
                lines.append(f"\n👥 **SỐ LƯỢNG: {avg} người** (Hành DT: {hanh_dt})")
                lines.append(f"- Nguồn: {detail}")
            else:
                lines.append(f"\n👥 **SỐ LƯỢNG: 5** (mặc định Thổ — không xác định hành)")

        
        # Ở ĐÂU / CHỖ NÀO / NƠI NÀO / TÌM ĐÂU
        elif any(k in q for k in ['ở đâu', 'hướng nào', 'phương nào', 'tìm đâu', 'chỗ nào',
                                   'nơi nào', 'ở chỗ', 'vị trí', 'nằm đâu', 'để đâu', 'để chỗ',
                                   'để ở', 'cất đâu', 'cất ở', 'giấu đâu', 'giấu ở']):
            quai_huong = {'Khảm': 'Bắc', 'Ly': 'Nam', 'Chấn': 'Đông', 'Đoài': 'Tây',
                         'Cấn': 'Đông Bắc', 'Tốn': 'Đông Nam', 'Càn': 'Tây Bắc', 'Khôn': 'Tây Nam'}
            quai_mota = {
                'Khảm': 'nơi có nước (nhà vệ sinh, bếp nước, bờ sông, hồ)',
                'Ly': 'nơi sáng, có lửa/điện (phòng khách, gần đèn, bếp)',
                'Chấn': 'nơi có tiếng động, đường lớn, cửa chính',
                'Đoài': 'nơi vui vẻ, gần ao hồ, đầm lầy, quán ăn',
                'Cấn': 'nơi cao, núi đồi, tủ, kệ, góc nhà, trên lầu',
                'Tốn': 'nơi có gió, gần cửa sổ, ban công, nhà bếp',
                'Càn': 'nơi trang trọng, tủ kim loại, nơi có người lớn/sếp',
                'Khôn': 'nơi thấp, bằng phẳng, nhà kho, nơi có đất/gạch'
            }
            # Tìm cung Sự Việc từ chart_data
            sv_cung = None
            sv_quai = ''
            if chart_data and isinstance(chart_data, dict):
                can_gio = chart_data.get('can_gio', '')
                can_thien_ban = chart_data.get('can_thien_ban', {})
                for cung_num, can_val in can_thien_ban.items():
                    if can_val == can_gio:
                        sv_cung = int(cung_num) if cung_num else None
                        break
            
            if sv_cung:
                sv_quai = QUAI_TUONG.get(sv_cung, '')
                huong = quai_huong.get(sv_quai, '?')
                mota = quai_mota.get(sv_quai, '')
                hanh_sv = CUNG_NGU_HANH.get(sv_cung, '?')
                lines.append(f'\n<div style="background:#1e1b4b;padding:18px;border-radius:14px;border-left:6px solid #818cf8;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#a5b4fc;">📍 HƯỚNG {huong.upper()}</span><br><span style="color:#c7d2fe;font-size:1.05em;">Cung {sv_cung} — {sv_quai} — {hanh_sv}</span></div>')
                lines.append(f"- Vị trí: {mota}")
                lines.append(f"- Ngũ Hành cung: {hanh_sv}")
                # Thêm thông tin Sao/Cửa tại cung SV để suy luận sâu
                if chart_data:
                    sao_sv = chart_data.get('thien_ban', {}).get(sv_cung, chart_data.get('thien_ban', {}).get(str(sv_cung), '?'))
                    cua_sv = chart_data.get('nhan_ban', {}).get(sv_cung, chart_data.get('nhan_ban', {}).get(str(sv_cung), '?'))
                    lines.append(f"- Sao tại cung SV: **{sao_sv}**, Cửa: **{cua_sv}**")
                    # Suy luận thêm
                    if 'Khai' in str(cua_sv):
                        lines.append(f"- ✅ Cửa Khai Môn = ĐỒ ĐANG Ở NƠI MỞ, DỄ TÌM")
                    elif 'Tử' in str(cua_sv):
                        lines.append(f"- 🔴 Cửa Tử Môn = ĐỒ BỊ CHÔN VÙI/ẨN, KHÓ TÌM")
                    elif 'Đỗ' in str(cua_sv):
                        lines.append(f"- ⚠️ Cửa Đỗ Môn = ĐỒ BỊ CHẮN, CẦN LỤC TÌM")
                    elif 'Sinh' in str(cua_sv):
                        lines.append(f"- ✅ Cửa Sinh Môn = ĐỒ CÒN NGUYÊN, TÌM SẼ THẤY")
                    elif 'Hưu' in str(cua_sv):
                        lines.append(f"- ✅ Cửa Hưu Môn = ĐỒ Ở NƠI YÊN TĨNH, AN TOÀN")
            else:
                lines.append(f"\n📍 **CÂU TRẢ LỜI:** Không xác định được Cung Sự Việc để tra hướng.")
        
        # ═══ V40.9: BỔ SUNG 12 DẠNG CÂU HỎI MỚI ═══
        
        # [11] TẠI SAO / VÌ SAO — phân tích nguyên nhân
        elif any(k in q for k in ['tại sao', 'vì sao', 'nguyên nhân', 'do đâu', 'lý do',
                                   'vì đâu', 'tại vì', 'nguyên cớ', 'căn nguyên']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: PHÂN TÍCH NGUYÊN NHÂN**")
            # Nguyên nhân từ Kỵ Thần
            KY_THAN_MAP = {
                'Phụ Mẫu': 'Do NHÀ CỬA, GIẤY TỜ, HỌC HÀNH, hoặc ÁP LỰC TỪ BỀ TRÊN',
                'Thê Tài': 'Do TIỀN BẠC, TÀI CHÍNH, MUA BÁN, hoặc VẤN ĐỀ TÌNH CẢM',
                'Quan Quỷ': 'Do CÔNG VIỆC, BỆNH TẬT, KIỆN TỤNG, hoặc SẾP/CHÍNH QUYỀN',
                'Tử Tôn': 'Do CON CÁI, GIẢI TRÍ, MẤT TẬP TRUNG, hoặc QUÁ LẠC QUAN',
                'Huynh Đệ': 'Do BẠN BÈ, ĐỐI THỦ, CẠNH TRANH, hoặc TIÊU XÀI HOANG PHÍ',
            }
            # Kỵ Thần = cái khắc DT
            KY_MAP = {'Phụ Mẫu': 'Thê Tài', 'Thê Tài': 'Huynh Đệ', 'Quan Quỷ': 'Tử Tôn',
                      'Tử Tôn': 'Quan Quỷ', 'Huynh Đệ': 'Quan Quỷ'}
            ky_than = KY_MAP.get(dung_than, '')
            lines.append(f"\n📋 **Nguyên nhân chính (từ Kỵ Thần = {ky_than}):**")
            lines.append(f"- {KY_THAN_MAP.get(ky_than, 'Chưa xác định')}")
            lines.append(f"\n📊 **Mức độ nghiêm trọng:** {'Nhẹ, dễ khắc phục' if pct >= 55 else 'Nghiêm trọng, khó giải quyết nhanh' if pct <= 40 else 'Trung bình, cần nỗ lực'}")
            lines.append(f"- 🔧 **Giải pháp:** Bổ sung Hành {hanh_dt} (Nguyên Thần sinh DT)")
        
        # [12] BAO LÂU / MẤT BAO LÂU — tính thời gian
        elif any(k in q for k in ['bao lâu', 'mất bao lâu', 'mấy ngày', 'mấy tháng',
                                   'mấy năm', 'bao nhiêu ngày', 'kéo dài']):
            # Ước tính dựa trên Hành DT + pct
            HANH_TGIAN = {'Mộc': '3-8 ngày/tháng', 'Hỏa': '2-7 ngày/tháng', 'Thổ': '5-10 ngày/tháng',
                          'Kim': '4-9 ngày/tháng', 'Thủy': '1-6 ngày/tháng'}
            tg = HANH_TGIAN.get(hanh_dt, '?')
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: ƯỚC TÍNH THỜI GIAN**")
            lines.append(f"- ⏱️ **Dự kiến:** {tg} (theo Hành {hanh_dt} của Dụng Thần)")
            if pct >= 60:
                lines.append(f"- ✅ Thời gian **NGẮN**, thuận lợi giải quyết nhanh")
            elif pct <= 40:
                lines.append(f"- 🔴 Thời gian **DÀI**, nhiều trở ngại kéo dài")
            else:
                lines.append(f"- 🟡 Thời gian **TRUNG BÌNH**, cần kiên nhẫn")
        
        # [13] MÀU GÌ / MÀU SẮC — theo Hành DT
        elif any(k in q for k in ['màu gì', 'màu nào', 'màu sắc', 'mặc màu', 'chọn màu',
                                   'sơn màu', 'xe màu']):
            HANH_MAU = {
                'Mộc': ('🟢 XANH LÁ, xanh ngọc, xanh rêu', 'Đỏ, cam, hồng (Hỏa khắc Mộc)'),
                'Hỏa': ('🔴 ĐỎ, cam, hồng, tím', 'Đen, xanh dương (Thủy khắc Hỏa)'),
                'Thổ': ('🟡 VÀNG, nâu, be, kem', 'Xanh lá (Mộc khắc Thổ)'),
                'Kim': ('⚪ TRẮNG, bạc, xám, ánh kim', 'Đỏ, cam (Hỏa khắc Kim)'),
                'Thủy': ('⚫ ĐEN, xanh dương, tím than', 'Vàng, nâu (Thổ khắc Thủy)'),
            }
            mau_tot, mau_tranh = HANH_MAU.get(hanh_dt, ('?', '?'))
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: MÀU SẮC PHÙ HỢP (Hành {hanh_dt})**")
            lines.append(f"- ✅ **Nên dùng:** {mau_tot}")
            lines.append(f"- ⛔ **Nên tránh:** {mau_tranh}")
            # Hành sinh DT
            SINH_DT = {'Mộc': 'Thủy', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa', 'Kim': 'Thổ', 'Thủy': 'Kim'}
            hanh_sinh = SINH_DT.get(hanh_dt, '')
            if hanh_sinh:
                mau_sinh, _ = HANH_MAU.get(hanh_sinh, ('?', '?'))
                lines.append(f"- 💡 **Màu bổ trợ (Hành {hanh_sinh} sinh {hanh_dt}):** {mau_sinh}")
        
        # [14] SỐ MẤY / CHỌN SỐ — theo Hành DT
        elif any(k in q for k in ['số mấy', 'chọn số', 'số nào', 'biển số', 'số đẹp',
                                   'số điện thoại', 'số may mắn', 'con số']):
            HANH_SO = {
                'Mộc': ('3, 8', 'Số liên quan Đông phương'),
                'Hỏa': ('2, 7', 'Số liên quan Nam phương'),
                'Thổ': ('5, 0, 10', 'Số liên quan Trung ương'),
                'Kim': ('4, 9', 'Số liên quan Tây phương'),
                'Thủy': ('1, 6', 'Số liên quan Bắc phương'),
            }
            so_tot, so_note = HANH_SO.get(hanh_dt, ('?', '?'))
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: SỐ MAY MẮN (Hành {hanh_dt})**")
            lines.append(f"- ✅ **Số tốt:** {so_tot} — {so_note}")
            SINH_DT = {'Mộc': 'Thủy', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa', 'Kim': 'Thổ', 'Thủy': 'Kim'}
            hanh_sinh = SINH_DT.get(hanh_dt, '')
            if hanh_sinh:
                so_sinh, _ = HANH_SO.get(hanh_sinh, ('?', '?'))
                lines.append(f"- 💡 **Số bổ trợ ({hanh_sinh} sinh {hanh_dt}):** {so_sinh}")
            HANH_KHAC = {'Mộc': 'Kim', 'Hỏa': 'Thủy', 'Thổ': 'Mộc', 'Kim': 'Hỏa', 'Thủy': 'Thổ'}
            hanh_xau = HANH_KHAC.get(hanh_dt, '')
            if hanh_xau:
                so_xau, _ = HANH_SO.get(hanh_xau, ('?', '?'))
                lines.append(f"- ⛔ **Số nên tránh ({hanh_xau} khắc {hanh_dt}):** {so_xau}")
        
        # [15] GIẢI PHÁP / LÀM SAO / CÁCH NÀO — hành động cụ thể
        elif any(k in q for k in ['làm sao', 'giải pháp', 'cách nào', 'khắc phục', 'cải thiện',
                                   'phải làm', 'nên làm', 'hóa giải', 'giải cứu', 'thoát khỏi']):
            HANH_GIAI_PHAP = {
                'Mộc': 'Trồng cây, dùng đồ gỗ, mặc xanh lá, hướng Đông, ăn rau xanh',
                'Hỏa': 'Thắp đèn sáng, dùng đồ đỏ, hướng Nam, tập thể dục, kinh doanh ánh sáng',
                'Thổ': 'Bất động sản, đeo đá quý, dùng đồ vàng/nâu, hướng Trung Tâm, kiên nhẫn',
                'Kim': 'Đeo vàng/bạc, dùng đồ kim loại, hướng Tây, tập kỷ luật, cắt giảm',
                'Thủy': 'Uống nhiều nước, gần sông hồ, hướng Bắc, linh hoạt, du lịch, mặc đen/xanh dương',
            }
            SINH_DT = {'Mộc': 'Thủy', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa', 'Kim': 'Thổ', 'Thủy': 'Kim'}
            hanh_sinh = SINH_DT.get(hanh_dt, '')
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: GIẢI PHÁP CỤ THỂ**")
            lines.append(f"\n🔧 **Bổ sung Hành {hanh_dt} (DT {dung_than}):**")
            lines.append(f"- {HANH_GIAI_PHAP.get(hanh_dt, '?')}")
            if hanh_sinh:
                lines.append(f"\n💡 **Bổ sung Hành {hanh_sinh} (sinh {hanh_dt}):**")
                lines.append(f"- {HANH_GIAI_PHAP.get(hanh_sinh, '?')}")
            HANH_KHAC = {'Mộc': 'Kim', 'Hỏa': 'Thủy', 'Thổ': 'Mộc', 'Kim': 'Hỏa', 'Thủy': 'Thổ'}
            hanh_tranh = HANH_KHAC.get(hanh_dt, '')
            if hanh_tranh:
                lines.append(f"\n⛔ **Tránh Hành {hanh_tranh} (khắc {hanh_dt}):**")
                lines.append(f"- {HANH_GIAI_PHAP.get(hanh_tranh, '?')}")
        
        # [16] SO SÁNH / CHỌN A HAY B — so hành
        elif any(k in q for k in ['hay là', 'hay B', ' hay ', 'chọn cái nào', 'nên chọn',
                                   'cái nào tốt', 'lựa chọn', 'option', 'phương án']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: SO SÁNH & LỰA CHỌN**")
            lines.append(f"\n📋 **Nguyên tắc chọn (Dụng Thần = {dung_than}, Hành {hanh_dt}):**")
            lines.append(f"- ✅ Chọn phương án **thuộc Hành {hanh_dt}** hoặc **Hành sinh {hanh_dt}**")
            SINH_DT = {'Mộc': 'Thủy', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa', 'Kim': 'Thổ', 'Thủy': 'Kim'}
            lines.append(f"- 💡 Hành sinh: **{SINH_DT.get(hanh_dt, '?')}** → hỗ trợ DT")
            HANH_KHAC = {'Mộc': 'Kim', 'Hỏa': 'Thủy', 'Thổ': 'Mộc', 'Kim': 'Hỏa', 'Thủy': 'Thổ'}
            lines.append(f"- ⛔ Tránh phương án **thuộc Hành {HANH_KHAC.get(hanh_dt, '?')}** (khắc DT)")
            if pct >= 55:
                lines.append(f"- 🟢 Phương án **ĐẦU TIÊN** (trong quẻ) trội hơn")
            else:
                lines.append(f"- 🔴 Phương án **THỨ HAI** có thể tốt hơn (DT yếu → chọn an toàn)")
        
        # [17] LỪA ĐẢO / THẬT GIẢ — kiểm tra Huynh Đệ + Quan Quỷ
        elif any(k in q for k in ['lừa đảo', 'lừa', 'giả', 'thật giả', 'tin được',
                                   'có thật', 'đáng tin', 'trung thực', 'gian lận', 'bịp']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: KIỂM TRA ĐỘ TIN CẬY**")
            # Huynh Đệ vượng = tranh giành, lừa đảo
            if pct <= 40:
                lines.append(f"- 🔴 **CẢNH BÁO CAO:** Huynh Đệ vượng, nhiều dấu hiệu KHÔNG ĐÁNG TIN")
                lines.append(f"- ⚠️ Cần KIỂM TRA KỸ, có khả năng bị lừa/giả dối")
            elif pct >= 60:
                lines.append(f"- ✅ **ĐỘ TIN CẬY CAO:** DT vượng, tình hình minh bạch")
                lines.append(f"- 💡 Có thể tin tưởng, nhưng vẫn nên kiểm tra hợp đồng/giấy tờ")
            else:
                lines.append(f"- 🟡 **CẦN THẬN:** Chưa rõ ràng, vừa có yếu tố tốt vừa đáng ngờ")
                lines.append(f"- ⚠️ Nên xác minh thêm trước khi cam kết")
        
        # [18] TÌNH CẢM / HÔN NHÂN / YÊU ĐƯƠNG
        elif any(k in q for k in ['yêu', 'hợp không', 'có cưới', 'hôn nhân', 'tình cảm',
                                   'chia tay', 'quay lại', 'người yêu', 'vợ chồng', 'kết hôn',
                                   'tái hợp', 'ngoại tình', 'chung thủy', 'có người', 'đám cưới']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: TÌNH CẢM / HÔN NHÂN**")
            lines.append(f"\n📋 **Phân tích (DT: {dung_than}, Hành {hanh_dt}):**")
            if pct >= 60:
                lines.append(f"- ✅ **THUẬN LỢI** — Tình cảm tốt, có cơ hội phát triển")
                lines.append(f"- 💕 DT vượng → hai bên hòa hợp, có tương lai")
            elif pct <= 40:
                lines.append(f"- 🔴 **BẤT LỢI** — Nhiều trở ngại, khó hòa hợp")
                lines.append(f"- 💔 DT suy → mâu thuẫn, thiếu tin tưởng")
            else:
                lines.append(f"- 🟡 **BÌNH THƯỜNG** — Có một số thử thách cần vượt qua")
                lines.append(f"- 💛 Cần kiên nhẫn và hy sinh từ cả hai phía")
            # Thế Ứng sinh khắc
            lines.append(f"- 📊 Tình trạng: {vv_data.get('tinh_trang', '?')}")
        
        # [19] BỆNH TẬT / SỨC KHỎE — Quan Quỷ Hành → Tạng phủ
        elif any(k in q for k in ['bệnh gì', 'bệnh', 'sức khỏe', 'ốm', 'đau', 'khỏi bệnh',
                                   'nặng không', 'viện', 'mổ', 'phẫu thuật', 'thuốc', 'chữa',
                                   'khám', 'triệu chứng', 'tạng', 'tim', 'gan', 'phổi']):
            HANH_BENH = {
                'Mộc': '🌳 GAN-MẬT, mắt, gân cơ, tay chân, đau đầu, stress',
                'Hỏa': '🔥 TIM-MẠCH, huyết áp, mắt, lưỡi, sốt, viêm',
                'Thổ': '🏔️ DẠ DÀY-TỤNG, tiêu hóa, da, miệng, phù thũng',
                'Kim': '⚔️ PHỔI-ĐẠI TRÀNG, hô hấp, da, mũi, răng, xương',
                'Thủy': '💧 THẬN-BÀNG QUANG, sinh dục, tai, xương sống, tiểu tiện',
            }
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: PHÂN TÍCH SỨC KHỎE**")
            # Bệnh theo Hành Quan Quỷ (gây bệnh)
            lines.append(f"\n🏥 **Tạng phủ bị ảnh hưởng (Hành {hanh_dt}):**")
            lines.append(f"- {HANH_BENH.get(hanh_dt, '?')}")
            if pct >= 60:
                lines.append(f"\n- ✅ **Tiên lượng TỐT:** Bệnh nhẹ, dễ hồi phục")
                lines.append(f"- 💊 Tử Tôn (thuốc) mạnh → điều trị hiệu quả")
            elif pct <= 40:
                lines.append(f"\n- 🔴 **Tiên lượng XẤU:** Bệnh có thể kéo dài, cần chữa tích cực")
                lines.append(f"- ⚠️ Quan Quỷ vượng → bệnh mạnh, cần can thiệp y tế")
            else:
                lines.append(f"\n- 🟡 **Tiên lượng TRUNG BÌNH:** Bệnh điều trị được nhưng cần thời gian")
        
        # [20] MẤT ĐỒ / TÌM VẬT — Thê Tài + Hướng
        elif any(k in q for k in ['mất đồ', 'tìm đồ', 'tìm thấy', 'mất rồi', 'đánh mất',
                                   'để quên', 'rơi ở', 'trộm', 'mất cắp', 'mất xe', 'mất tiền']):
            HANH_HUONG = {'Mộc': 'Đông', 'Hỏa': 'Nam', 'Thổ': 'Trung Tâm', 'Kim': 'Tây', 'Thủy': 'Bắc'}
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: TÌM ĐỒ MẤT**")
            if pct >= 55:
                lines.append(f"- ✅ **TÌM THẤY ĐƯỢC!** Đồ vật còn nguyên")
                lines.append(f"- 🧭 Hướng tìm: **{HANH_HUONG.get(hanh_dt, '?')}**")
                lines.append(f"- 📍 Vật ở: {vv_data.get('hinh', '?')} — nơi {vv_data.get('tinh_trang', '?')}")
            elif pct <= 40:
                lines.append(f"- 🔴 **KHÓ TÌM!** Đồ có thể đã mất hẳn hoặc bị phá hủy")
                lines.append(f"- ⚠️ DT suy → vật không còn nguyên vẹn")
            else:
                lines.append(f"- 🟡 **CÓ THỂ TÌM nhưng tốn thời gian**")
                lines.append(f"- 🧭 Hướng: **{HANH_HUONG.get(hanh_dt, '?')}**, kiểm tra kỹ")
        
        # [21] KIỆN TỤNG / TRANH CHẤP
        elif any(k in q for k in ['kiện', 'tòa', 'tranh chấp', 'thắng kiện', 'thưa kiện',
                                   'pháp lý', 'luật sư', 'tố cáo', 'khiếu nại', 'đòi lại']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: KIỆN TỤNG / TRANH CHẤP**")
            if pct >= 55:
                lines.append(f"- ✅ **THUẬN LỢI — Có khả năng THẮNG** ({pct}%)")
                lines.append(f"- 📋 DT vượng, bên mình có lý, pháp luật ủng hộ")
            elif pct <= 40:
                lines.append(f"- 🔴 **BẤT LỢI — Khó THẮNG** ({pct}%)")
                lines.append(f"- ⚠️ DT suy, đối phương mạnh hơn. Nên hòa giải thay vì kiện")
            else:
                lines.append(f"- 🟡 **50/50 — Kết quả chưa rõ**")
                lines.append(f"- 💡 Nên tìm luật sư giỏi, chuẩn bị bằng chứng kỹ")
        
        # [22] THỜI TIẾT / MƯA NẮNG
        elif any(k in q for k in ['thời tiết', 'mưa', 'nắng', 'gió', 'bão', 'lũ',
                                   'trời', 'nóng', 'lạnh', 'ẩm']):
            HANH_THOITIET = {
                'Thủy': '🌧️ MƯA, ẩm ướt, có nước',
                'Hỏa': '☀️ NẮNG, nóng, khô ráo',
                'Mộc': '🌬️ GIÓ, mát mẻ, se se',
                'Kim': '❄️ LẠNH, hanh khô, có sương',
                'Thổ': '☁️ ÂM U, nhiều mây, oi bức',
            }
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: DỰ BÁO THỜI TIẾT (theo Huyền Học)**")
            lines.append(f"- 🌤️ **Xu hướng (Hành {hanh_dt} thịnh):** {HANH_THOITIET.get(hanh_dt, '?')}")
            if pct >= 55:
                lines.append(f"- ✅ Thời tiết ỔN ĐỊNH, thuận lợi cho hoạt động ngoài trời")
            else:
                lines.append(f"- ⚠️ Thời tiết KHÔNG ỔN ĐỊNH, nên chuẩn bị phương án dự phòng")
        
        # [23] THAI SẢN / TRAI HAY GÁI / MANG THAI
        elif any(k in q for k in ['mang thai', 'có thai', 'sinh con', 'trai hay gái', 'giới tính',
                                   'đẻ', 'bầu', 'em bé', 'sinh đôi', 'mấy con', 'có bầu']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: THAI SẢN**")
            if any(k in q for k in ['trai hay gái', 'giới tính']):
                # Âm Dương quái → giới tính
                if the_quai:
                    from free_ai_helper import QUAI_AM_DUONG
                    _ad = QUAI_AM_DUONG.get(the_quai, '') if 'QUAI_AM_DUONG' in dir() else ''
                if pct >= 55:
                    lines.append(f"- 👶 **Nghiêng CON TRAI** (Dương khí vượng, {pct}%)")
                else:
                    lines.append(f"- 👶 **Nghiêng CON GÁI** (Âm khí thịnh, {pct}%)")
                lines.append(f"- 📌 Lưu ý: Dự đoán giới tính bằng huyền học chỉ mang tính THAM KHẢO")
            else:
                if pct >= 55:
                    lines.append(f"- ✅ **CÓ THAI / SẼ CÓ** — Tử Tôn vượng ({pct}%)")
                    lines.append(f"- 💡 Thời gian thuận lợi, nên tiến hành")
                elif pct <= 40:
                    lines.append(f"- 🔴 **KHÓ / CHƯA ĐÚNG LÚC** ({pct}%)")
                    lines.append(f"- ⚠️ Tử Tôn suy, cần bổ sung sức khỏe, chờ thời điểm tốt")
                else:
                    lines.append(f"- 🟡 **CÓ THỂ nhưng cần chú ý sức khỏe** ({pct}%)")
        
        # [24] HỢP TÁC / ĐỐI TÁC / CỘNG SỰ
        elif any(k in q for k in ['hợp tác', 'đối tác', 'cộng sự', 'liên kết', 'chung vốn',
                                   'góp vốn', 'làm chung', 'partner', 'joint']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: HỢP TÁC / ĐỐI TÁC**")
            if pct >= 60:
                lines.append(f"- ✅ **NÊN HỢP TÁC** — Hai bên hòa hợp ({pct}%)")
                lines.append(f"- 💡 Lợi ích chung, đôi bên cùng có lợi")
            elif pct <= 40:
                lines.append(f"- 🔴 **KHÔNG NÊN** — Nguy cơ mâu thuẫn ({pct}%)")
                lines.append(f"- ⚠️ Huynh Đệ (tranh giành) mạnh → dễ xung đột lợi ích")
            else:
                lines.append(f"- 🟡 **CÓ THỂ nhưng cần hợp đồng RÕ RÀNG** ({pct}%)")
                lines.append(f"- 📋 Phân chia lợi nhuận/trách nhiệm minh bạch trước khi bắt đầu")
        
        # [25] ĐÚNG HAY SAI / TIN ĐƯỢC KHÔNG
        elif any(k in q for k in ['đúng không', 'sai không', 'đúng hay sai', 'có đúng',
                                   'có sai', 'đúng sai', 'nói thật', 'nói dối', 'tin được']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: KIỂM TRA ĐÚNG/SAI**")
            if pct >= 60:
                lines.append(f"- ✅ **ĐÚNG / TIN ĐƯỢC** ({pct}%)")
                lines.append(f"- 📋 Thế trận minh bạch, thông tin đáng tin cậy")
            elif pct <= 35:
                lines.append(f"- 🔴 **SAI / KHÔNG TIN ĐƯỢC** ({pct}%)")
                lines.append(f"- ⚠️ Nhiều yếu tố gian dối, cần xác minh kỹ")
            else:
                lines.append(f"- 🟡 **CHƯA RÕ — Có phần đúng, có phần sai** ({pct}%)")
                lines.append(f"- 📋 Cần kiểm chứng thêm từ nguồn khác")
        
        # [26] CHỜ HAY HÀNH ĐỘNG / LÀM NGAY HAY ĐỢI
        elif any(k in q for k in ['chờ hay', 'đợi hay', 'làm ngay', 'chờ đợi', 'hành động ngay',
                                   'nên đợi', 'nên chờ', 'tiến hay lùi', 'xuất phát']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: CHỜ HAY HÀNH ĐỘNG?**")
            if pct >= 60:
                lines.append(f"- ✅ **HÀNH ĐỘNG NGAY!** — Thời cơ đã đến ({pct}%)")
                lines.append(f"- 🚀 DT vượng, cơ hội thuận lợi, không nên lần lữa")
            elif pct <= 40:
                lines.append(f"- 🔴 **NÊN CHỜ!** — Chưa đúng thời điểm ({pct}%)")
                lines.append(f"- ⏳ DT suy, hành động bây giờ nhiều rủi ro. Chờ Ứng Kỳ phù hợp")
            else:
                lines.append(f"- 🟡 **CÓ THỂ HÀNH ĐỘNG nhưng CẨN THẬN** ({pct}%)")
                lines.append(f"- 💡 Nên chuẩn bị kỹ, có phương án dự phòng trước khi tiến")
        
        # [27] NHÀ CỬA / PHONG THỦY / XÂY NHÀ
        elif any(k in q for k in ['xây nhà', 'mua nhà', 'nhà mới', 'phong thủy', 'sửa nhà',
                                   'dọn nhà', 'chuyển nhà', 'nhà đất', 'đất đai', 'lô đất']):
            HANH_HUONG_NT = {'Mộc': 'Đông/Đông Nam', 'Hỏa': 'Nam', 'Thổ': 'Trung Tâm/Tây Nam/Đông Bắc', 'Kim': 'Tây/Tây Bắc', 'Thủy': 'Bắc'}
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: NHÀ CỬA / PHONG THỦY**")
            if pct >= 55:
                lines.append(f"- ✅ **THUẬN LỢI** — Nên tiến hành ({pct}%)")
            elif pct <= 40:
                lines.append(f"- 🔴 **CHƯA NÊN** — Nhiều trở ngại ({pct}%)")
            else:
                lines.append(f"- 🟡 **CẨN THẬN** — Cần xem xét kỹ ({pct}%)")
            lines.append(f"- 🧭 **Hướng tốt:** {HANH_HUONG_NT.get(hanh_dt, '?')} (Hành {hanh_dt})")
            lines.append(f"- 🎨 **Màu sơn tốt:** {HANH_MAU.get(hanh_dt, '?') if 'HANH_MAU' in dir() else '?'}")
        
        # [28] THI CỬ / HỌC HÀNH / ĐỖ ĐẠT
        elif any(k in q for k in ['thi', 'đỗ', 'đạt', 'trượt', 'kết quả thi', 'điểm thi',
                                   'học hành', 'xét tuyển', 'trúng tuyển', 'đậu', 'rớt']):
            lines.append(f"\n{icon} **CÂU TRẢ LỜI: THI CỬ / HỌC HÀNH**")
            if pct >= 60:
                lines.append(f"- ✅ **ĐỖ / ĐẠT KẾT QUẢ TỐT** ({pct}%)")
                lines.append(f"- 📚 Phụ Mẫu (giấy tờ, bằng cấp) thuận lợi")
            elif pct <= 40:
                lines.append(f"- 🔴 **TRƯỢT / KẾT QUẢ KHÔNG TỐT** ({pct}%)")
                lines.append(f"- ⚠️ Cần chuẩn bị thêm, ôn luyện kỹ hơn")
            else:
                lines.append(f"- 🟡 **BIÊN — Có thể đỗ sát sao** ({pct}%)")
                lines.append(f"- 💡 Cần nỗ lực thêm, không nên chủ quan")
        
        # DEFAULT — V42.0: TRẢ LỜI TRỰC TIẾP + VÌ SAO + ỨNG KỲ + GIẢI PHÁP
        else:
            # V40.6: Tái khẳng định câu hỏi
            _q_short = question[:80] if len(question) > 80 else question
            
            # Detect loại câu hỏi để trả lời đúng kiểu
            _is_what = any(k in q for k in ['cái gì', 'loại gì', 'sản xuất gì', 'làm gì', 'sản phẩm gì', 'mặt hàng',
                                             'buôn bán gì', 'kinh doanh gì', 'nghề gì', 'ngành gì', 'là gì', 'thuộc loại',
                                             'hình dạng', 'màu gì', 'chất liệu', 'tên gì', 'giống gì', 'nó là gì',
                                             'loại nào', 'mẫu gì', 'kiểu gì', 'thể loại', 'gì vậy', 'gì đây',
                                             'bán gì', 'làm nghề gì', 'sản xuất cái', 'trồng gì', 'nuôi gì',
                                             'mua gì', 'bằng gì', 'nguyên liệu gì', 'vật liệu gì'])
            _is_who = any(k in q for k in ['ai ', 'người nào', 'là ai', 'ai vậy', 'ai đó'])
            _is_how = any(k in q for k in ['thế nào', 'như nào', 'ra sao', 'nghĩ gì', 'hành động', 'làm sao'])
            _is_yesno = any(k in q for k in ['có ', 'được', 'không', 'chứ', 'hả', 'có nên', 'nên không'])
            
            if _is_what:
                # V42.0: Câu hỏi "CÁI GÌ?" → Dùng Vạn Vật Loại Tượng chuyên sâu
                # FIX V42.9
                _hanh = hanh_dt or 'Thổ'
                _vv = NGU_HANH_VAT_CHAT.get(_hanh, {})
                _vv_do_vat = _vv.get('do_vat', '') or _vv.get('vat', '')
                _vv_chat = _vv.get('chat_lieu', '') or _vv.get('chat', '')
                _vv_hinh = _vv.get('hinh', '') or _vv.get('hinh_dang', '')
                _vv_mau = _vv.get('mau', '') or _vv.get('sac', '')
                _vv_huong = _vv.get('huong', '')
                
                # Xây mô tả Vạn Vật chi tiết
                _what_parts = []
                if _vv_chat:
                    _what_parts.append(f"**Chất liệu:** {_vv_chat}")
                if _vv_do_vat:
                    _what_parts.append(f"**Đồ vật/Sản phẩm:** {_vv_do_vat}")
                if _vv_hinh:
                    _what_parts.append(f"**Hình dạng:** {_vv_hinh}")
                if _vv_mau:
                    _what_parts.append(f"**Màu sắc:** {_vv_mau}")
                if _vv_huong:
                    _what_parts.append(f"**Hướng/Vùng:** {_vv_huong}")
                
                # Map hành → mô tả sản phẩm cụ thể  
                _HANH_SAN_PHAM = {
                    'Kim': 'Sản phẩm kim loại, máy móc, dao kéo, linh kiện điện tử, xe cộ, vũ khí, trang sức, vàng bạc, inox, nhôm, sắt thép',
                    'Mộc': 'Sản phẩm gỗ, giấy, vải, quần áo, nội thất, nông sản, trái cây, rau, thuốc thảo dược, sách vở, đồ handmade',
                    'Thủy': 'Sản phẩm liên quan nước, chất lỏng, hải sản, thủy sản, nước giải khát, rượu bia, mực, sơn, dầu, xăng, hóa chất',
                    'Hỏa': 'Sản phẩm liên quan lửa/điện: điện tử, đèn, pin, năng lượng, mỹ phẩm, nhựa, thực phẩm chế biến, bếp, gas',
                    'Thổ': 'Sản phẩm từ đất: gạch, gốm sứ, xi măng, bất động sản, nông sản (lúa, ngũ cốc), vật liệu xây dựng, đá quý',
                }
                _san_pham = _HANH_SAN_PHAM.get(_hanh, 'Chưa xác định')
                
                # Trường Sinh → mức độ sản phẩm
                _TS_QUALITY = {
                    (75, 100): ('Sản phẩm CAO CẤP, đắt tiền, brand lớn, quy mô lớn, mới nhất', '#22c55e'),
                    (55, 74): ('Sản phẩm TRUNG-CAO, chất lượng khá, quy mô vừa', '#3b82f6'),
                    (40, 54): ('Sản phẩm TRUNG BÌNH, phổ thông, quy mô nhỏ-vừa', '#eab308'),
                    (20, 39): ('Sản phẩm THẤP, cũ, secondhand, nhỏ, giá rẻ', '#f97316'),
                    (0, 19): ('Sản phẩm RẤT NHỎ, hư hỏng, phế liệu, tái chế', '#ef4444'),
                }
                _quality_text = 'Sản phẩm trung bình'
                _q_color = '#eab308'
                for (lo, hi), (txt, clr) in _TS_QUALITY.items():
                    if lo <= pct <= hi:
                        _quality_text = txt
                        _q_color = clr
                        break
                
                lines.append(
                    f'\n<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);padding:22px;border-radius:14px;'
                    f'border-left:6px solid {_q_color};margin:12px 0;">'
                    f'<span style="font-size:1.3em;font-weight:900;color:#c4b5fd;">🔮 TRẢ LỜI: "{_q_short}"</span><br><br>'
                    f'<span style="font-size:1.2em;font-weight:800;color:{_q_color};">📦 Hành {_hanh} → {_san_pham}</span><br><br>'
                    f'<span style="color:#e2e8f0;font-size:1.05em;">'
                    + '<br>'.join(f'- {p}' for p in _what_parts)
                    + f'</span><br><br>'
                    f'<span style="color:{_q_color};font-weight:700;">📊 Mức chất lượng: {_quality_text} ({pct}%)</span>'
                    f'</div>'
                )
                
                # Thêm Vạn Vật tổng hợp nếu có
                if _vv_full_text:
                    lines.append(f"\n**📋 VẠN VẬT LOẠI TƯỢNG CHI TIẾT (hành {_hanh}):**")
                    for _vvl in _vv_full_text.split('\n')[:10]:
                        if _vvl.strip():
                            lines.append(f"  {_vvl.strip()}")
                
            elif _is_who:
                # Câu hỏi AI/NGƯỜI NÀO → dùng Vạn Vật mô tả người
                # FIX V42.9
                _hanh = hanh_dt or 'Thổ'
                _vv = NGU_HANH_VAT_CHAT.get(_hanh, {})
                _HANH_NGUOI = {
                    'Kim': 'Người da trắng, gầy, cao, gương mặt vuông/dài, tính cách quyết đoán, nghiêm khắc, làm ngành kỹ thuật/ngân hàng/quân đội',
                    'Mộc': 'Người cao gầy, thanh tú, da ngăm, tốt bụng, thích thiên nhiên, làm giáo dục/y tế/nông nghiệp',
                    'Thủy': 'Người mập tròn, da đen/ngăm, thông minh lanh lợi, linh hoạt, làm thương mại/vận tải/truyền thông',
                    'Hỏa': 'Người nóng tính, da đỏ/sáng, hoạt bát, nói nhiều, làm quảng cáo/nghệ thuật/CNTT/bếp',
                    'Thổ': 'Người chắc khỏe, mặt đầy đặn, chậm rãi, trung thực, làm xây dựng/bất động sản/nông nghiệp',
                }
                _nguoi_desc = _HANH_NGUOI.get(_hanh, 'Chưa xác định')
                _wcolor = '#c084fc'
                lines.append(
                    f'\n<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);padding:20px;border-radius:14px;'
                    f'border-left:6px solid {_wcolor};margin:12px 0;">'
                    f'<span style="font-size:1.2em;font-weight:900;color:#c4b5fd;">👤 VỀ: "{_q_short}"</span><br>'
                    f'<span style="color:#e2e8f0;font-size:1.05em;">Hành {_hanh}: {_nguoi_desc}</span><br>'
                    f'<span style="color:{_wcolor};font-weight:700;">Mức độ: {pct}% ({final_verdict})</span>'
                    f'</div>'
                )
                
            elif _is_how:
                # Câu hỏi MÔ TẢ → dùng Vạn Vật
                # FIX V42.9
                _hanh = hanh_dt or 'Thổ'
                _vv = NGU_HANH_VAT_CHAT.get(_hanh, {})
                if pct >= 55:
                    _mota = f"Tích cực, chủ động, có thiện ý. Tính chất {_hanh}: {_vv.get('hinh', '')}."
                elif pct <= 40:
                    _mota = f"Tiêu cực, e dè, có ý đồ không tốt. Tính chất {_hanh}: bất lợi."
                else:
                    _mota = f"Trung lập, chưa rõ ràng, cân nhắc. Tính chất {_hanh}: {_vv.get('hinh', '')}."
                _dcolor = '#16a34a' if pct >= 55 else '#dc2626' if pct <= 40 else '#ca8a04'
                lines.append(f'\n<div style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:18px;border-radius:14px;border-left:6px solid {_dcolor};margin:12px 0;"><span style="font-size:1.2em;font-weight:900;color:{_dcolor};">📋 VỀ: "{_q_short}"</span><br><span style="color:#e2e8f0;font-size:1em;">- {_mota}</span><br><span style="color:{_dcolor};font-weight:700;">Mức độ: {pct}% ({final_verdict})</span></div>')
            elif _is_yesno:
                # Câu hỏi CÓ/KHÔNG → dứt khoát
                if final_verdict == 'CÁT' or pct >= 55:
                    lines.append(f'\n<div style="background:#052e16;padding:18px;border-radius:14px;border-left:6px solid #22c55e;margin:12px 0;"><span style="font-size:1.4em;font-weight:900;color:#22c55e;">✅ CÓ</span> <span style="color:#bbf7d0;font-size:1.1em;">cho "{_q_short}" — {pct}%</span></div>')
                elif final_verdict == 'HUNG' or pct <= 40:
                    lines.append(f'\n<div style="background:#450a0a;padding:18px;border-radius:14px;border-left:6px solid #ef4444;margin:12px 0;"><span style="font-size:1.4em;font-weight:900;color:#ef4444;">❌ KHÔNG</span> <span style="color:#fecaca;font-size:1.1em;">cho "{_q_short}" — {pct}%</span></div>')
                else:
                    lines.append(f'\n<div style="background:#422006;padding:18px;border-radius:14px;border-left:6px solid #eab308;margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:#fbbf24;">🟡 CÓ THỂ ĐƯỢC</span> <span style="color:#fef3c7;font-size:1.05em;">cho "{_q_short}" — cần thận trọng ({pct}%)</span></div>')
            else:
                # Câu hỏi TỔNG QUÁT → khẳng định + context
                _gcolor = '#22c55e' if pct >= 55 else '#ef4444' if pct <= 40 else '#eab308'
                _gtext = 'THUẬN LỢI' if pct >= 55 else 'BẤT LỢI' if pct <= 40 else 'TRUNG BÌNH'
                lines.append(f'\n<div style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:18px;border-radius:14px;border-left:6px solid {_gcolor};margin:12px 0;"><span style="font-size:1.3em;font-weight:900;color:{_gcolor};">{icon} VỀ "{_q_short}"</span><br><span style="color:#f1f5f9;font-size:1.15em;font-weight:700;">{_gtext} — {pct}%</span></div>')
        
        # --- V40.6: VÌ SAO — bằng chứng THẬT từ factors + evidence ---
        lines.append(f'\n<div style="background:#1e1b4b;padding:14px 18px;border-radius:10px;border-left:5px solid #818cf8;margin:12px 0;"><b style="color:#a5b4fc;font-size:1.05em;">📋 VÌ SAO — BẰNG CHỨNG TỪ QUẺ</b></div>')
        _vi_sao_items = []
        # Ưu tiên factors thật từ engine
        if lh_factors:
            for f in lh_factors[:3]:
                _vi_sao_items.append(f"📿 LH: {f}")
        if km_factors:
            for f in km_factors[:2]:
                _vi_sao_items.append(f"🏯 KM: {f}")
        if mh_factors:
            for f in mh_factors[:1]:
                _vi_sao_items.append(f"🌸 MH: {f}")
        # Fallback: dùng evidence đã thu thập + reason
        if not _vi_sao_items:
            if evidence:
                for ev in evidence[:3]:
                    _vi_sao_items.append(f"📌 {ev}")
            if ky_mon_reason:
                _vi_sao_items.append(f"🏯 Kỳ Môn: {ky_mon_reason}")
            if luc_hao_reason:
                _vi_sao_items.append(f"📿 Lục Hào: {luc_hao_reason}")
            if mai_hoa_reason:
                _vi_sao_items.append(f"🌸 Mai Hoa: {mai_hoa_reason}")
        if not _vi_sao_items:
            _vi_sao_items.append(f"📊 Tổng hợp 6PP → weighted_pct={pct}%")
        for item in _vi_sao_items[:6]:
            lines.append(f"- {item}")
        
        # --- V40.3: ỨNG KỲ — thời gian cụ thể ---
        _UK_TIMING = {
            'Kim': {'thang': 'Thân/Dậu (tháng 7-8 ÂL)', 'ngay': 'Canh/Tân', 'huong': 'Tây'},
            'Mộc': {'thang': 'Dần/Mão (tháng 1-2 ÂL)', 'ngay': 'Giáp/Ất', 'huong': 'Đông'},
            'Thủy': {'thang': 'Hợi/Tý (tháng 10-11 ÂL)', 'ngay': 'Nhâm/Quý', 'huong': 'Bắc'},
            'Hỏa': {'thang': 'Tị/Ngọ (tháng 4-5 ÂL)', 'ngay': 'Bính/Đinh', 'huong': 'Nam'},
            'Thổ': {'thang': 'Thìn/Tuất/Sửu/Mùi (tháng 3/6/9/12 ÂL)', 'ngay': 'Mậu/Kỷ', 'huong': 'Trung Tâm'},
        }
        _dt_hanh = hanh_dt or ''
        _uk = _UK_TIMING.get(_dt_hanh, {})
        if _uk:
            lines.append(f'\n<div style="background:#172554;padding:14px 18px;border-radius:10px;border-left:5px solid #60a5fa;margin:8px 0;"><b style="color:#93c5fd;font-size:1.05em;">⏳ ỨNG KỲ:</b> <span style="color:#dbeafe;font-weight:600;">{_uk.get("thang","?")}</span> | Ngày <span style="color:#dbeafe;font-weight:600;">{_uk.get("ngay","?")}</span> | Hướng <span style="color:#fbbf24;font-weight:700;">{_uk.get("huong","?")}</span></div>')
        
        # --- V40.6: GIẢI PHÁP — cụ thể theo câu hỏi + Ngũ Hành ---
        lines.append(f'\n<div style="background:#14532d;padding:14px 18px;border-radius:10px;border-left:5px solid #4ade80;margin:12px 0;"><b style="color:#86efac;font-size:1.05em;">🔧 GIẢI PHÁP CHO "{_q_short}"</b></div>')
        _HANH_HELP = {
            'Kim': 'Tìm quý nhân hành Thổ (sinh Kim). Hướng Tây. Màu trắng/bạc.',
            'Mộc': 'Tìm quý nhân hành Thủy (sinh Mộc). Hướng Đông. Màu xanh lá.',
            'Thủy': 'Tìm quý nhân hành Kim (sinh Thủy). Hướng Bắc. Màu đen/xanh đậm.',
            'Hỏa': 'Tìm quý nhân hành Mộc (sinh Hỏa). Hướng Nam. Màu đỏ/cam.',
            'Thổ': 'Tìm quý nhân hành Hỏa (sinh Thổ). Hướng Trung Tâm. Màu vàng/nâu.',
        }
        if final_verdict == 'CÁT' or pct >= 55:
            if any(k in q for k in ['mua', 'đầu tư', 'kinh doanh', 'vốn', 'tiền', 'thuế']):
                lines.append("- ✅ Thời điểm tốt để giao dịch. Kiểm tra kỹ giấy tờ trước khi ký.")
            elif any(k in q for k in ['bệnh', 'ốm', 'khỏe', 'sức khỏe', 'đau']):
                lines.append("- ✅ Bệnh sẽ hồi phục, tìm bác sĩ chuyên khoa để trị dứt.")
            elif any(k in q for k in ['yêu', 'tình', 'vợ', 'chồng', 'cưới', 'hẹn hò']):
                lines.append("- ✅ Mối quan hệ thuận lợi, chủ động bày tỏ.")
            elif any(k in q for k in ['việc', 'công ty', 'thi', 'đỗ', 'sếp', 'lương']):
                lines.append("- ✅ Thời cơ tốt, hành động quyết đoán sẽ thành công.")
            else:
                lines.append("- ✅ Nắm bắt cơ hội ngay, đừng chần chừ.")
        elif final_verdict == 'HUNG' or pct <= 40:
            if any(k in q for k in ['bệnh', 'ốm', 'khỏe', 'chết', 'mất']):
                lines.append("- ⚠️ Cần đi khám ngay, không nên tự chữa. Theo dõi sát.")
            elif any(k in q for k in ['mua', 'đầu tư', 'vốn', 'tiền', 'thuế']):
                lines.append("- ❌ KHÔNG nên giao dịch lúc này. Chờ 2-4 tuần hoặc sang tháng sinh hành.")
            else:
                lines.append("- ❌ Kiên nhẫn chờ đợi, tìm quý nhân hỗ trợ.")
            lines.append(f"- 💡 {_HANH_HELP.get(hanh_dt, 'Tìm người hỗ trợ.')}")
        else:
            lines.append("- ⏸️ Chuẩn bị kỹ, chờ thời điểm hành vượng mới hành động.")
            lines.append(f"- 💡 {_HANH_HELP.get(hanh_dt, 'Cân nhắc kỹ.')}")
        
        # V40.6: Thêm impacts tóm tắt cuối
        if good_impacts and len(good_impacts) > 0:
            lines.append(f"\n✅ **Thuận lợi ({len(good_impacts)}):** {good_impacts[0][:80]}")
        if bad_impacts and len(bad_impacts) > 0:
            lines.append(f"⚠️ **Trở ngại ({len(bad_impacts)}):** {bad_impacts[0][:80]}")
        
        
        return "\n".join(lines)

    # ===========================
    # V12.0: LỤC THÂN RELATIONSHIP ENGINE
    # So sánh BT/Bố Mẹ/ACE/Vợ/Con/Sếp/Người Lạ với Dụng Thần
    # ===========================
    def _extract_dung_than_from_all_methods(self, dung_than, chart_data, luc_hao_data, mai_hoa_data):
        """
        V12.0: Trích xuất thông tin Dụng Thần từ TẤT CẢ 5 phương pháp.
        Trả về dict: {method: {hanh, vuong_suy, sao, cua, ...}}
        """
        dt_info = {}
        dt_hanh_primary = None  # Hành chính của DT (dùng cho so sánh)
        
        # --- 1. KỲ MÔN: DT = Can tương ứng → tìm cung → lấy Sao/Cửa/Thần ---
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            dt_can_map = {
                'Quan Quỷ': chart_data.get('can_gio', ''),
                'Thê Tài': chart_data.get('can_gio', ''),
                'Tử Tôn': chart_data.get('can_gio', ''),
                'Phụ Mẫu': chart_data.get('can_nam', ''),
                'Phụ Mẫu (Cha)': chart_data.get('can_nam', ''),
                'Phụ Mẫu (Mẹ)': chart_data.get('can_nam', ''),
                'Huynh Đệ': chart_data.get('can_thang', ''),
                'Bản Thân': can_ngay,
            }
            dt_can = dt_can_map.get(dung_than, chart_data.get('can_gio', ''))
            dt_hanh_can = CAN_NGU_HANH.get(dt_can, '?')
            
            # Tìm cung DT
            dt_cung = None
            for cn, cv in can_thien_ban.items():
                if cv == dt_can:
                    dt_cung = int(cn) if cn else None
                    break
            
            km_info = {'can': dt_can, 'hanh_can': dt_hanh_can, 'cung': dt_cung}
            if dt_cung:
                km_info['hanh_cung'] = CUNG_NGU_HANH.get(dt_cung, '?')
                km_info['sao'] = str(chart_data.get('thien_ban', {}).get(dt_cung, chart_data.get('thien_ban', {}).get(str(dt_cung), '?')))
                km_info['cua'] = str(chart_data.get('nhan_ban', {}).get(dt_cung, chart_data.get('nhan_ban', {}).get(str(dt_cung), '?')))
                km_info['than'] = str(chart_data.get('than_ban', {}).get(dt_cung, chart_data.get('than_ban', {}).get(str(dt_cung), '?')))
                # Sao cát/hung
                km_info['sao_cat'] = any(s in km_info['sao'] for s in ['Tâm', 'Nhậm', 'Phụ', 'Xung'])
                km_info['cua_cat'] = any(c in km_info['cua'] for c in CUA_CAT)
                km_info['cua_hung'] = any(c in km_info['cua'] for c in CUA_HUNG)
            
            dt_info['Kỳ Môn'] = km_info
            if dt_hanh_can != '?':
                dt_hanh_primary = dt_hanh_can
        
        # --- 2. LỤC HÀO: Tìm hào DT → lấy Ngũ Hành, Vượng/Suy ---
        if luc_hao_data and isinstance(luc_hao_data, dict):
            ban = luc_hao_data.get('ban', {})
            haos = ban.get('haos') or ban.get('details', [])
            dt_hao = None
            for hao in haos:
                lt = hao.get('luc_than', '')
                tu = hao.get('the_ung', '') or hao.get('marker', '')
                if lt == dung_than or (dung_than in ['Phụ Mẫu (Cha)', 'Phụ Mẫu (Mẹ)'] and 'Phụ Mẫu' in lt):
                    dt_hao = hao
                    break
                if dung_than == 'Bản Thân' and 'Thế' in str(tu):
                    dt_hao = hao
                    break
            
            if dt_hao:
                vs = str(dt_hao.get('vuong_suy', '') or dt_hao.get('strength', '') or '?')
                cc = dt_hao.get('can_chi', '') or dt_hao.get('chi', '') or '?'
                lh_info = {
                    'hao': dt_hao.get('hao', '?'),
                    'can_chi': cc,
                    'hanh': dt_hao.get('ngu_hanh', '?'),
                    'vuong_suy': vs,
                }
                dt_info['Lục Hào'] = lh_info
                if not dt_hanh_primary and lh_info['hanh'] != '?':
                    dt_hanh_primary = lh_info['hanh']
            else:
                dt_info['Lục Hào'] = {'hao': 'Phục Thần (ẩn)', 'hanh': '?', 'vuong_suy': 'Ẩn'}
        
        # --- 3. MAI HOA: Thể/Dụng quái → Hành ---
        if mai_hoa_data and isinstance(mai_hoa_data, dict):
            the_quai = mai_hoa_data.get('the_quai', '')
            dung_quai = mai_hoa_data.get('dung_quai', '')
            the_yn = QUAI_Y_NGHIA.get(the_quai, {})
            dung_yn = QUAI_Y_NGHIA.get(dung_quai, {})
            mh_info = {
                'the_quai': the_quai, 'dung_quai': dung_quai,
                'the_hanh': the_yn.get('hanh', '?'),
                'dung_hanh': dung_yn.get('hanh', '?'),
            }
            if mh_info['the_hanh'] != '?' and mh_info['dung_hanh'] != '?':
                mh_info['relation'] = _ngu_hanh_relation(mh_info['the_hanh'], mh_info['dung_hanh'])
            dt_info['Mai Hoa'] = mh_info
        
        # --- 4. THIẾT BẢN: Nạp Âm Ngũ Hành ---
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            chi_ngay = chart_data.get('chi_ngay', '')
            if can_ngay and chi_ngay:
                nap_am = tra_nap_am(f"{can_ngay} {chi_ngay}")
                if nap_am:
                    na_ten = nap_am.get('ten', '') or nap_am.get('nap_am', '?')
                    na_hanh = nap_am.get('hanh', '?')
                    na_gt = nap_am.get('giai_thich', '') or NAP_AM_GIAI_THICH.get(na_ten, '')
                    tb_info = {'nap_am': na_ten, 'hanh': na_hanh, 'giai_thich': na_gt}
                    dt_info['Thiết Bản'] = tb_info
        
        # --- 5. VẠN TƯỢNG: Quái Tượng Cung BT/DT ---
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            bt_cung = None
            for cn, cv in can_thien_ban.items():
                if cv == can_ngay:
                    bt_cung = int(cn) if cn else None
                    break
            if not bt_cung and can_ngay == 'Giáp':
                for cn, cv in can_thien_ban.items():
                    if cv == 'Mậu':
                        bt_cung = int(cn) if cn else None
                        break
            if bt_cung:
                quai_bt = QUAI_TUONG.get(bt_cung, '')
                vt_info = {'quai': quai_bt, 'hanh': CUNG_NGU_HANH.get(bt_cung, '?')}
                yn = QUAI_Y_NGHIA.get(quai_bt, {})
                if yn:
                    vt_info['tuong'] = yn.get('tuong', '?')
                dt_info['Vạn Tượng'] = vt_info
        
        dt_info['_hanh_primary'] = dt_hanh_primary or '?'
        return dt_info
    
    def _build_luc_than_relationship_table(self, question, dung_than, chart_data, luc_hao_data, mai_hoa_data):
        """
        V12.0: Xây dựng bảng quan hệ Lục Thân với Dụng Thần.
        So sánh từng thành viên (BT/Bố Mẹ/ACE/Vợ/Con/Sếp/Người Lạ) với Dụng Thần.
        
        Trả về markdown string chứa bảng so sánh.
        """
        if not chart_data and not luc_hao_data:
            return ""
        
        # 1. Xác định hành của Bản Thân (để tính Lục Thân)
        bt_hanh = '?'
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            bt_hanh = CAN_NGU_HANH.get(can_ngay, '?')
        
        if bt_hanh == '?':
            return ""
        
        # 2. Trích xuất DT từ tất cả phương pháp
        dt_info = self._extract_dung_than_from_all_methods(dung_than, chart_data, luc_hao_data, mai_hoa_data)
        dt_hanh = dt_info.get('_hanh_primary', '?')
        
        if dt_hanh == '?':
            return ""
        
        # 3. Xây dựng bảng quan hệ
        lines = []
        lines.append("")
        lines.append("**👥 BẢNG QUAN HỆ LỤC THÂN VỚI DỤNG THẦN:**")
        lines.append(f"*Dụng Thần = **{dung_than}** (hành **{dt_hanh}**) | Bản Thân hành **{bt_hanh}***")
        lines.append("")
        lines.append("| Thành viên | Lục Thân | Hành | Quan hệ với DT | Tác động | Chi tiết |")
        lines.append("|:---|:---|:---:|:---|:---:|:---|")
        
        help_members = []
        harm_members = []
        neutral_members = []
        
        for member_name, member_info in LUC_THAN_MEMBERS.items():
            luc_than = member_info['luc_than']
            icon = member_info['icon']
            
            # Tính hành của thành viên này
            if luc_than == 'Ứng':
                # Người Lạ = Ứng hào → lấy từ Lục Hào nếu có
                member_hanh = '?'
                if luc_hao_data and isinstance(luc_hao_data, dict):
                    ban = luc_hao_data.get('ban', {})
                    haos = ban.get('haos') or ban.get('details', [])
                    for hao in haos:
                        if hao.get('the_ung') == 'Ứng':
                            member_hanh = hao.get('ngu_hanh', '?')
                            break
                if member_hanh == '?':
                    # Fallback: dùng Can Giờ
                    can_gio = chart_data.get('can_gio', '') if chart_data else ''
                    member_hanh = CAN_NGU_HANH.get(can_gio, '?')
            elif member_name == 'Bản Thân':
                member_hanh = bt_hanh
            else:
                member_hanh = _get_luc_than_hanh(bt_hanh, luc_than)
            
            if member_hanh == '?':
                lines.append(f"| {icon} {member_name} | {luc_than} | ? | Không rõ | ❓ | Thiếu dữ liệu |")
                continue
            
            # So sánh member_hanh với dt_hanh (Dụng Thần)
            rel = _ngu_hanh_relation(member_hanh, dt_hanh)
            
            # Phân loại tác động
            detail = ""
            if 'SINH' in rel and 'BỊ' not in rel:
                # Member sinh DT → GIÚP (Nguyên Thần vai trò)
                impact = '✅ GIÚP'
                detail = f"{member_name} ({member_hanh}) sinh {dung_than} ({dt_hanh}) → hỗ trợ sự việc"
                help_members.append(member_name)
            elif 'ĐƯỢC SINH' in rel:
                # DT sinh Member → member hao DT
                impact = '⚠️ HAO'
                detail = f"{dung_than} ({dt_hanh}) phải nuôi {member_name} ({member_hanh}) → hao tổn năng lượng DT"
                neutral_members.append(member_name)
            elif 'thắng' in rel:
                # Member khắc DT → HẠI (Kỵ Thần vai trò)
                impact = '🔴 HẠI'
                detail = f"{member_name} ({member_hanh}) khắc {dung_than} ({dt_hanh}) → gây cản trở"
                harm_members.append(member_name)
            elif 'BỊ KHẮC' in rel:
                # DT khắc Member → DT kiểm soát member
                impact = '✅ THUẬN'
                detail = f"{dung_than} ({dt_hanh}) khắc chế {member_name} ({member_hanh}) → DT mạnh hơn"
                help_members.append(member_name)
            elif 'Tỷ' in rel:
                # Cùng hành → ngang nhau
                impact = '🟡 BÌNH'
                detail = f"{member_name} ({member_hanh}) tỷ hòa {dung_than} ({dt_hanh}) → cân bằng"
                neutral_members.append(member_name)
            else:
                impact = '❓'
                detail = rel
                neutral_members.append(member_name)
            
            # Thêm thông tin từ Kỳ Môn (nếu có Can tương ứng)
            km_can_key = member_info['km_can']
            km_extra = ""
            if chart_data and isinstance(chart_data, dict):
                km_can_val = chart_data.get(km_can_key, '')
                if km_can_val:
                    km_extra = f" (Can: {km_can_val})"
            
            lines.append(f"| {icon} {member_name} | {luc_than} | {member_hanh} | {rel[:30]} | {impact} | {detail}{km_extra} |")
        
        # 4. Tổng kết
        lines.append("")
        if help_members:
            lines.append(f"✅ **Giúp sức DT:** {', '.join(help_members)}")
        if harm_members:
            lines.append(f"🔴 **Hại DT:** {', '.join(harm_members)}")
        if neutral_members:
            lines.append(f"🟡 **Trung tính/Hao:** {', '.join(neutral_members)}")
        
        # 5. Thêm thông tin DT từ các phương pháp
        lines.append("")
        lines.append("**🔎 DỤNG THẦN QUA 5 PHƯƠNG PHÁP:**")
        
        # Kỳ Môn
        km = dt_info.get('Kỳ Môn', {})
        if km.get('cung'):
            sao_icon = '✅' if km.get('sao_cat') else ('🔴' if not km.get('sao_cat') else '🟡')
            cua_icon = '✅' if km.get('cua_cat') else ('🔴' if km.get('cua_hung') else '🟡')
            lines.append(f"- **Kỳ Môn:** DT ({km.get('can','?')}) tại Cung {km['cung']} — Sao: {km.get('sao','?')} {sao_icon} | Cửa: {km.get('cua','?')} {cua_icon} | Thần: {km.get('than','?')}")
        
        # Lục Hào
        lh = dt_info.get('Lục Hào', {})
        if lh.get('hao'):
            vs = lh.get('vuong_suy', '?')
            vs_icon = '✅' if any(k in vs for k in ['Vượng', 'Tướng', 'Lâm', 'Đế']) else ('🔴' if any(k in vs for k in ['Tử', 'Tuyệt', 'Mộ']) else '🟡')
            lines.append(f"- **Lục Hào:** DT hào {lh['hao']} ({lh.get('can_chi','?')}) — {lh.get('hanh','?')} — {vs} {vs_icon}")
        
        # Mai Hoa
        mh = dt_info.get('Mai Hoa', {})
        if mh.get('the_quai'):
            rel_mh = mh.get('relation', '?')
            lines.append(f"- **Mai Hoa:** Thể ({mh['the_quai']}/{mh.get('the_hanh','?')}) vs Dụng ({mh['dung_quai']}/{mh.get('dung_hanh','?')}) → {rel_mh}")
        
        # Thiết Bản
        tb = dt_info.get('Thiết Bản', {})
        if tb.get('nap_am'):
            lines.append(f"- **Thiết Bản:** Nạp Âm: {tb['nap_am']} ({tb.get('hanh','?')}) — {tb.get('giai_thich','')}")
        
        # Vạn Tượng
        vt = dt_info.get('Vạn Tượng', {})
        if vt.get('quai'):
            lines.append(f"- **Vạn Tượng:** Quái BT: {vt['quai']} ({vt.get('hanh','?')}) — {vt.get('tuong','?')}")
        
        return "\n".join(lines)

    # ===========================
    # V11.0: UNIFIED NARRATIVE SYNTHESIS
    # Kết nối TẤT CẢ dữ kiện thành 1 câu trả lời thống nhất
    # ===========================
    def _build_unified_narrative(self, question, dung_than, chart_data, luc_hao_data, mai_hoa_data,
                                  ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict,
                                  ky_mon_reason, luc_hao_reason, mai_hoa_reason,
                                  impact_evidence=None,
                                  luc_nham_verdict='BÌNH', luc_nham_reason='',
                                  thai_at_verdict='BÌNH', thai_at_reason='',
                                  final_pct=None,
                                  lh_factors=None, km_factors=None, mh_factors=None):
        """
        V11.0: Tổng hợp THỐNG NHẤT — Thu thập Dụng Thần từ cả 3 phương pháp,
        kết nối thành chuỗi nhân quả, tạo 1 câu trả lời duy nhất.
        """
        q = question.lower()
        lines = []
        
        # ════════════════════════════════════════════
        # PHASE A: THU THẬP DỤNG THẦN TỪ 3 PHƯƠNG PHÁP
        # ════════════════════════════════════════════
        dt_statuses = []  # List of (method, status_text, good_or_bad)
        chain_evidence = []  # Chuỗi bằng chứng để nối narrative
        
        # --- A1. KỲ MÔN: DT tại cung nào? ---
        km_dt_info = None
        km_bt_info = None
        km_rel = None
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            can_gio = chart_data.get('can_gio', '')
            can_thien_ban = chart_data.get('can_thien_ban', {})
            thien_ban = chart_data.get('thien_ban', {})
            nhan_ban = chart_data.get('nhan_ban', {})
            than_ban = chart_data.get('than_ban', {})
            
            dt_can_map = {
                'Quan Quỷ': can_gio, 'Thê Tài': can_gio, 'Tử Tôn': can_gio,
                'Phụ Mẫu': chart_data.get('can_nam', ''),
                'Phụ Mẫu (Cha)': chart_data.get('can_nam', ''),
                'Phụ Mẫu (Mẹ)': chart_data.get('can_nam', ''),
                'Huynh Đệ': chart_data.get('can_thang', ''),
                'Bản Thân': can_ngay,
            }
            dt_can = dt_can_map.get(dung_than, can_gio)
            
            # Tìm cung BT
            bt_cung = None
            for cn, cv in can_thien_ban.items():
                if cv == can_ngay:
                    bt_cung = int(cn) if cn else None
                    break
            if not bt_cung and can_ngay == 'Giáp':
                for cn, cv in can_thien_ban.items():
                    if cv == 'Mậu':
                        bt_cung = int(cn) if cn else None
                        break
            
            # Tìm cung DT
            dt_cung = None
            if dt_can and dt_can != can_ngay:
                for cn, cv in can_thien_ban.items():
                    if cv == dt_can:
                        dt_cung = int(cn) if cn else None
                        break
            
            if bt_cung:
                bt_sao = str(thien_ban.get(bt_cung, thien_ban.get(str(bt_cung), '?')))
                bt_cua = str(nhan_ban.get(bt_cung, nhan_ban.get(str(bt_cung), '?')))
                bt_than = str(than_ban.get(bt_cung, than_ban.get(str(bt_cung), '?')))
                bt_hanh = CUNG_NGU_HANH.get(bt_cung, '?')
                hanh_can = CAN_NGU_HANH.get(can_ngay, '?')
                km_bt_info = {'cung': bt_cung, 'sao': bt_sao, 'cua': bt_cua, 'than': bt_than, 'hanh': bt_hanh, 'hanh_can': hanh_can}
                
                # Đánh giá BT
                bt_sao_ok = any(s in bt_sao for s in ['Tâm', 'Nhậm', 'Phụ', 'Xung'])
                bt_cua_ok = any(c in bt_cua for c in CUA_CAT)
                bt_cua_bad = any(c in bt_cua for c in CUA_HUNG)
                bt_status = ''
                if bt_sao_ok and bt_cua_ok:
                    bt_status = 'MẠNH (Sao cát + Cửa cát)'
                    chain_evidence.append(f"Người hỏi (Cung {bt_cung}): Sao {bt_sao} CÁT + Cửa {bt_cua} CÁT → MẠNH")
                elif bt_cua_bad:
                    bt_status = 'YẾU (Cửa hung)'
                    chain_evidence.append(f"Người hỏi (Cung {bt_cung}): Cửa {bt_cua} HUNG → YẾU")
                else:
                    bt_status = 'BÌNH'
                    chain_evidence.append(f"Người hỏi (Cung {bt_cung}): Sao {bt_sao}, Cửa {bt_cua} → BÌNH")
            
            if dt_cung and dt_cung != bt_cung:
                dt_sao = str(thien_ban.get(dt_cung, thien_ban.get(str(dt_cung), '?')))
                dt_cua = str(nhan_ban.get(dt_cung, nhan_ban.get(str(dt_cung), '?')))
                dt_than = str(than_ban.get(dt_cung, than_ban.get(str(dt_cung), '?')))
                dt_hanh_c = CUNG_NGU_HANH.get(dt_cung, '?')
                km_dt_info = {'cung': dt_cung, 'sao': dt_sao, 'cua': dt_cua, 'than': dt_than, 'hanh': dt_hanh_c}
                
                # Đánh giá DT trong KM
                dt_sao_ok = any(s in dt_sao for s in ['Tâm', 'Nhậm', 'Phụ', 'Xung'])
                dt_cua_ok = any(c in dt_cua for c in CUA_CAT)
                dt_cua_bad = any(c in dt_cua for c in CUA_HUNG)
                
                if dt_sao_ok and dt_cua_ok:
                    dt_statuses.append(('Kỳ Môn', f'{dung_than} tại Cung {dt_cung}: Sao {dt_sao} CÁT + Cửa {dt_cua} CÁT → SỰ VIỆC THUẬN LỢI', 'good'))
                    chain_evidence.append(f"Sự việc (Cung {dt_cung}): Sao {dt_sao} CÁT + Cửa {dt_cua} CÁT → THUẬN LỢI")
                elif dt_cua_bad:
                    dt_statuses.append(('Kỳ Môn', f'{dung_than} tại Cung {dt_cung}: Cửa {dt_cua} HUNG → SỰ VIỆC GẶP TRỞ NGẠI', 'bad'))
                    chain_evidence.append(f"Sự việc (Cung {dt_cung}): Cửa {dt_cua} HUNG → TRỞ NGẠI")
                else:
                    dt_statuses.append(('Kỳ Môn', f'{dung_than} tại Cung {dt_cung}: Sao {dt_sao}, Cửa {dt_cua} → BÌNH', 'neutral'))
                    chain_evidence.append(f"Sự việc (Cung {dt_cung}): Sao {dt_sao}, Cửa {dt_cua} → BÌNH")
                
                # BT → DT quan hệ
                if bt_cung and bt_hanh != '?' and dt_hanh_c != '?':
                    rel = _ngu_hanh_relation(bt_hanh, dt_hanh_c)
                    km_rel = rel
                    if 'SINH' in rel and 'BỊ' not in rel:
                        chain_evidence.append(f"BT sinh SV: Người hỏi phải BỎ CÔNG SỨC cho sự việc")
                    elif 'ĐƯỢC SINH' in rel:
                        chain_evidence.append(f"SV sinh BT: Sự việc ĐEM LẠI LỢI ÍCH cho người hỏi")
                    elif 'thắng' in rel:
                        chain_evidence.append(f"BT khắc SV: Người hỏi KIỂM SOÁT sự việc")
                    elif 'BỊ KHẮC' in rel:
                        chain_evidence.append(f"SV khắc BT: Sự việc GÂY KHÓ KHĂN cho người hỏi")
                    elif 'Tỷ' in rel:
                        chain_evidence.append(f"BT tỷ hòa SV: Cân bằng giữa người hỏi và sự việc")
            elif bt_cung:
                # DT cùng cung BT → dùng thông tin BT
                dt_statuses.append(('Kỳ Môn', f'{dung_than} cùng cung BT (Cung {bt_cung})', 'neutral'))
        
        # --- A2. LỤC HÀO: DT hào nào? ---
        if luc_hao_data and isinstance(luc_hao_data, dict):
            ban = luc_hao_data.get('ban', {})
            haos = ban.get('haos') or ban.get('details', [])
            dong_hao = luc_hao_data.get('dong_hao', [])
            
            dt_hao = None
            the_hao = None
            for i, hao in enumerate(haos):
                lt = hao.get('luc_than', '')
                tu = hao.get('the_ung', '')
                if lt == dung_than or (dung_than in ['Phụ Mẫu (Cha)', 'Phụ Mẫu (Mẹ)'] and 'Phụ Mẫu' in lt):
                    dt_hao = hao
                if tu == 'Thế':
                    the_hao = hao
                if dung_than == 'Bản Thân' and tu == 'Thế':
                    dt_hao = hao
            
            if not dt_hao and dung_than == 'Bản Thân':
                dt_hao = the_hao
            
            if dt_hao:
                dt_vuong = str(dt_hao.get('vuong_suy', ''))
                dt_canchi = dt_hao.get('can_chi', '?')
                dt_hanh_lh = dt_hao.get('ngu_hanh', '?')
                hao_num = dt_hao.get('hao', '?')
                is_dong = hao_num in dong_hao if isinstance(hao_num, int) else False
                
                if 'Vượng' in dt_vuong or 'Tướng' in dt_vuong:
                    dt_statuses.append(('Lục Hào', f'{dung_than} hào {hao_num} ({dt_canchi}) {dt_vuong}{" + ĐỘNG" if is_dong else ""} → DT MẠNH MẼ', 'good'))
                    chain_evidence.append(f"Lục Hào: {dung_than} ({dt_canchi}) {dt_vuong} → MẠNH")
                elif 'Tử' in dt_vuong or 'Tuyệt' in dt_vuong:
                    dt_statuses.append(('Lục Hào', f'{dung_than} hào {hao_num} ({dt_canchi}) {dt_vuong} → DT RẤT YẾU', 'bad'))
                    chain_evidence.append(f"Lục Hào: {dung_than} ({dt_canchi}) {dt_vuong} → RẤT YẾU")
                elif 'Suy' in dt_vuong or 'Bệnh' in dt_vuong:
                    dt_statuses.append(('Lục Hào', f'{dung_than} hào {hao_num} ({dt_canchi}) {dt_vuong} → DT ĐANG SUY', 'bad'))
                    chain_evidence.append(f"Lục Hào: {dung_than} ({dt_canchi}) {dt_vuong} → SUY")
                else:
                    dt_statuses.append(('Lục Hào', f'{dung_than} hào {hao_num} ({dt_canchi}) {dt_vuong}', 'neutral'))
                    chain_evidence.append(f"Lục Hào: {dung_than} ({dt_canchi}) {dt_vuong}")
                
                # Thế/Ứng quan hệ
                if the_hao and dt_hao != the_hao:
                    the_hanh = the_hao.get('ngu_hanh', '')
                    if the_hanh and dt_hanh_lh and dt_hanh_lh != '?':
                        rel_lh = _ngu_hanh_relation(the_hanh, dt_hanh_lh)
                        if 'KHẮC' in rel_lh:
                            chain_evidence.append(f"Lục Hào: Thế hào ({the_hanh}) vs {dung_than} ({dt_hanh_lh}): {rel_lh}")
                
                # Hào động tác động DT
                if dong_hao:
                    for d in dong_hao:
                        if d <= len(haos) and haos[d-1] != dt_hao:
                            h_dong = haos[d-1]
                            h_hanh = h_dong.get('ngu_hanh', '')
                            h_lt = h_dong.get('luc_than', '')
                            if dt_hanh_lh and h_hanh and dt_hanh_lh != '?':
                                rel_d = _ngu_hanh_relation(h_hanh, dt_hanh_lh)
                                if 'thắng' in rel_d:
                                    chain_evidence.append(f"Hào {d} ({h_lt}) ĐỘNG khắc {dung_than} → GÂY HẠI")
                                elif 'SINH' in rel_d and 'BỊ' not in rel_d:
                                    chain_evidence.append(f"Hào {d} ({h_lt}) ĐỘNG sinh {dung_than} → HỖ TRỢ")
            else:
                dt_statuses.append(('Lục Hào', f'{dung_than} không xuất hiện → Phục Thần (ẩn, yếu)', 'bad'))
                chain_evidence.append(f"Lục Hào: {dung_than} KHÔNG xuất hiện trong quẻ → ẨN (yếu)")
        
        # --- A3. MAI HOA: Thể/Dụng sinh khắc ---
        if mai_hoa_data and isinstance(mai_hoa_data, dict):
            thuong = mai_hoa_data.get('thuong', '')
            ha = mai_hoa_data.get('ha', '')
            the_quai = mai_hoa_data.get('the_quai', '')
            dung_quai = mai_hoa_data.get('dung_quai', '')
            interp = mai_hoa_data.get('interpretation', '')
            
            # V11.0: FILTER — loại bỏ text rác (TikTok, Livestream, Bán Hàng)
            if interp and isinstance(interp, str):
                noise_words = ['TikTok', 'Livestream', 'Bán Hàng', 'tiktok', 'livestream']
                if any(nw in interp for nw in noise_words):
                    interp = ''  # Đặt rỗng để không dùng
            
            if the_quai and dung_quai:
                the_yn = QUAI_Y_NGHIA.get(the_quai, {})
                dung_yn = QUAI_Y_NGHIA.get(dung_quai, {})
                the_h = the_yn.get('hanh', '')
                dung_h = dung_yn.get('hanh', '')
                
                if the_h and dung_h:
                    rel_mh = _ngu_hanh_relation(the_h, dung_h)
                    if 'SINH' in rel_mh and 'BỊ' not in rel_mh:
                        dt_statuses.append(('Mai Hoa', f'Thể ({the_quai}/{the_h}) sinh Dụng ({dung_quai}/{dung_h}) → Hao sức cho sự việc', 'neutral'))
                    elif 'ĐƯỢC SINH' in rel_mh:
                        dt_statuses.append(('Mai Hoa', f'Dụng ({dung_quai}/{dung_h}) sinh Thể ({the_quai}/{the_h}) → SỰ VIỆC SINH LỢI', 'good'))
                    elif 'thắng' in rel_mh:
                        dt_statuses.append(('Mai Hoa', f'Thể ({the_quai}/{the_h}) khắc Dụng ({dung_quai}/{dung_h}) → KIỂM SOÁT sự việc', 'good'))
                    elif 'BỊ KHẮC' in rel_mh:
                        dt_statuses.append(('Mai Hoa', f'Dụng ({dung_quai}/{dung_h}) khắc Thể ({the_quai}/{the_h}) → SỰ VIỆC GÂY HẠI', 'bad'))
                    elif 'Tỷ' in rel_mh:
                        dt_statuses.append(('Mai Hoa', f'Thể/Dụng tỷ hòa ({the_h}) → CÂN BẰNG', 'neutral'))
                    chain_evidence.append(f"Mai Hoa: Thể({the_quai}/{the_h}) vs Dụng({dung_quai}/{dung_h}): {rel_mh}")
            elif interp and isinstance(interp, str) and len(interp) > 20:
                short_interp = interp[:100]
                chain_evidence.append(f"Mai Hoa: {short_interp}")
        
        # ════════════════════════════════════════════
        # PHASE B: (V36.0: Bỏ bảng cũ — đã chuyển sang Phase D chi tiết hơn)
        # ════════════════════════════════════════════
        good_count = sum(1 for _, _, gb in dt_statuses if gb == 'good')
        bad_count = sum(1 for _, _, gb in dt_statuses if gb == 'bad')
        
        # ════════════════════════════════════════════
        # PHASE B2: BẢNG QUAN HỆ LỤC THÂN VỚI DỤNG THẦN (V12.0)
        # ════════════════════════════════════════════
        relationship_table = self._build_luc_than_relationship_table(
            question, dung_than, chart_data, luc_hao_data, mai_hoa_data
        )
        if relationship_table:
            lines.append("")
            lines.append(relationship_table)
        
        # ════════════════════════════════════════════
        # PHASE C: XÂY DỰNG CHUỖI NHÂN QUẢ → NARRATIVE
        # ════════════════════════════════════════════
        lines.append("")
        lines.append("**🔗 CHUỖI LẬP LUẬN:**")
        
        # Nối chuỗi bằng chứng
        for i, ev in enumerate(chain_evidence[:8]):  # Max 8 điểm
            connector = "→" if i > 0 else "•"
            lines.append(f"{connector} {ev}")
        
        # ════════════════════════════════════════════
        # PHASE D: KẾT LUẬN THỐNG NHẤT V39.0 — ANSWER-FIRST + VÌ SAO + GIẢI PHÁP
        # Mọi suy luận → 1 KẾT LUẬN KHẲNG ĐỊNH + LÝ DO + LỜI KHUYÊN
        # ════════════════════════════════════════════
        
        # Tổng hợp verdicts
        verdicts_map = {
            'Kỳ Môn': (ky_mon_verdict, ky_mon_reason),
            'Lục Hào': (luc_hao_verdict, luc_hao_reason),
            'Mai Hoa': (mai_hoa_verdict, mai_hoa_reason if isinstance(mai_hoa_reason, str) else ''),
            'Đại Lục Nhâm': (luc_nham_verdict, luc_nham_reason),
            'Thái Ất': (thai_at_verdict, thai_at_reason),
        }
        
        thuan_factors = []
        nghich_factors = []
        binh_factors = []
        
        for method, (verdict, reason) in verdicts_map.items():
            v_upper = str(verdict).upper() if verdict else ''
            reason_short = str(reason)[:120] if reason else ''
            if 'CÁT' in v_upper:
                thuan_factors.append(f"{method}: {verdict} — {reason_short}")
            elif 'HUNG' in v_upper:
                nghich_factors.append(f"{method}: {verdict} — {reason_short}")
            else:
                binh_factors.append(f"{method}: {verdict} — {reason_short}")
        
        for ev in chain_evidence:
            ev_lower = ev.lower()
            if any(k in ev_lower for k in ['thuận', 'mạnh', 'cát', 'sinh lợi', 'hỗ trợ', 'kiểm soát', 'vượng', 'good']):
                thuan_factors.append(ev)
            elif any(k in ev_lower for k in ['hung', 'yếu', 'suy', 'khắc', 'trở ngại', 'gây hại', 'tử', 'tuyệt', 'ẩn']):
                nghich_factors.append(ev)
        
        pct = final_pct if final_pct is not None else 50
        cat_count = len(thuan_factors)
        hung_count = len(nghich_factors)
        
        # V39.0: KHÔNG override pct — weighted_pct đã tính chính xác từ 6PP + 12TS
        # Chỉ xác định overall label từ pct gốc
        if pct >= 55:
            overall = 'THUẬN LỢI'
        elif pct < 45:
            overall = 'BẤT LỢI'
        elif pct >= 50:
            overall = 'CÓ — cần nỗ lực thêm'
        else:
            overall = 'KHÓ THÀNH — cần đổi hướng hoặc đợi'
        
        # ══════════════════════════════════════════════════════════
        # ★★★ PHẦN 0: PHÁN QUYẾT — ĐẶT ĐẦU TIÊN (ANSWER-FIRST) ★★★
        # ══════════════════════════════════════════════════════════
        lines.append("")
        
        q_lower_kl = question.lower()
        _PD_NORM = {
            'qua duoc': 'qua được', 'qua khoi': 'qua khỏi', 'chet chua': 'chết chưa',
            'con song': 'còn sống', 'da mat': 'đã mất', 'qua doi': 'qua đời',
            'tu vong': 'tử vong', 'song sot': 'sống sót', 'benh nang': 'bệnh nặng',
            'nguy kich': 'nguy kịch', 'hap hoi': 'hấp hối', 'cuu duoc': 'cứu được',
            'co nen': 'có nên', 'nen khong': 'nên không', 'co duoc': 'có được',
            'duoc khong': 'được không', 'co khong': 'có không',
        }
        for _nd, _cd in sorted(_PD_NORM.items(), key=lambda x: len(x[0]), reverse=True):
            if _nd in q_lower_kl:
                q_lower_kl = q_lower_kl.replace(_nd, _cd)
        
        _hanh_dt_kl = '?'
        if chart_data and isinstance(chart_data, dict):
            _hanh_dt_kl = chart_data.get('hanh_dt', '?')
        if _hanh_dt_kl == '?':
            _DT_HANH_DEFAULT = {'Phụ Mẫu': 'Mộc', 'Thê Tài': 'Hỏa', 'Quan Quỷ': 'Thổ', 'Tử Tôn': 'Kim', 'Huynh Đệ': 'Thủy', 'Bản Thân': 'Thủy'}
            _hanh_dt_kl = _DT_HANH_DEFAULT.get(dung_than, '?')
        
        # Phân loại câu hỏi
        is_life_death = any(kw in q_lower_kl for kw in [
            'sống', 'chết', 'mất', 'còn sống', 'đã mất', 'qua đời', 'qua khỏi',
            'cứu được', 'sống sót', 'nguy hiểm', 'tử vong', 'chết chưa',
            'sống hay', 'mất rồi', 'còn hay', 'sống không', 'qua được',
            'bệnh nặng', 'nguy kịch', 'hấp hối'
        ])
        is_yesno_kl = any(kw in q_lower_kl for kw in [
            'có không', 'được không', 'không', 'hay không',
            'có được', 'có tốt', 'chưa', 'rồi chưa', 'xong chưa',
            'thắng', 'thua', 'đỗ', 'trượt', 'có lời', 'lỗ không'
        ])
        is_should = any(kw in q_lower_kl for kw in [
            'có nên', 'nên không', 'nên chưa', 'nên hay', 'có nên mua',
            'có nên bán', 'có nên đi', 'có nên làm', 'có nên đầu tư'
        ])
        
        # V42.3: Phát hiện competition ở tầng kết luận
        is_competition_kl = _is_competition_question(question)
        _side_a, _side_b = _extract_two_sides(question) if is_competition_kl else ('Bên A', 'Bên B')
        
        # V42.3: Phát hiện câu hỏi THỜI GIAN (Ứng Kỳ)
        is_timing_kl = any(kw in q_lower_kl for kw in [
            'khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'bao lâu',
            'tháng nào', 'tháng mấy', 'năm nào', 'ngày nào', 'mùa nào',
            'nhanh', 'chậm', 'kéo dài', 'tồn tại', 'bao nhiêu năm',
            'bao nhiêu tháng', 'bao nhiêu ngày', 'trong bao lâu',
            'xảy ra lúc', 'biết kết quả', 'có kết quả',
        ])
        
        # V42.3: TÍNH ỨNG KỲ CỤ THỂ (ngày dương lịch)
        _timing_fast = ''
        _timing_slow = ''
        _timing_detail = []
        if is_timing_kl:
            import datetime as _dt_uk
            _now_uk = _dt_uk.datetime.now()
            
            _UNG_KY_CHI = {
                'Kim': ['Thân', 'Dậu'], 'Mộc': ['Dần', 'Mão'], 'Thủy': ['Tý', 'Hợi'],
                'Hỏa': ['Ngọ', 'Tị'], 'Thổ': ['Thìn', 'Tuất', 'Sửu', 'Mùi']
            }
            _CHI_GIO = {
                'Tý': '23h-1h', 'Sửu': '1h-3h', 'Dần': '3h-5h', 'Mão': '5h-7h',
                'Thìn': '7h-9h', 'Tị': '9h-11h', 'Ngọ': '11h-13h', 'Mùi': '13h-15h',
                'Thân': '15h-17h', 'Dậu': '17h-19h', 'Tuất': '19h-21h', 'Hợi': '21h-23h',
            }
            _CHI_THANG = {
                'Dần': 'T1 ÂL', 'Mão': 'T2 ÂL', 'Thìn': 'T3 ÂL', 'Tị': 'T4 ÂL',
                'Ngọ': 'T5 ÂL', 'Mùi': 'T6 ÂL', 'Thân': 'T7 ÂL', 'Dậu': 'T8 ÂL',
                'Tuất': 'T9 ÂL', 'Hợi': 'T10 ÂL', 'Tý': 'T11 ÂL', 'Sửu': 'T12 ÂL',
            }
            # Tìm ngày Chi gần nhất từ hôm nay — dùng JDN chuẩn
            def _next_chi_date(chi_name, from_date):
                """Tìm ngày dương lịch gần nhất có Chi = chi_name, dùng JDN"""
                from xem_ngay_dep import _jdn as _jdn_uk
                chi_idx = CHI_ORDER.index(chi_name) if chi_name in CHI_ORDER else 0
                _CANS_UK = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                _CHIS_UK = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                _THU_UK = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật']
                
                for offset in range(1, 400):
                    d = from_date + _dt_uk.timedelta(days=offset)
                    if hasattr(d, 'date'):
                        d_date = d.date() if hasattr(d, 'date') else d
                    else:
                        d_date = d
                    jdn = _jdn_uk(d_date.day, d_date.month, d_date.year)
                    chi_day = (jdn + 1) % 12
                    if chi_day == chi_idx:
                        can_day = _CANS_UK[(jdn + 9) % 10]
                        chi_day_name = _CHIS_UK[chi_day]
                        thu = _THU_UK[d_date.weekday()]
                        return d, f"{can_day} {chi_day_name}", thu, offset
                return from_date + _dt_uk.timedelta(days=12), chi_name, "?", 12
            
            _SINH_MAP = {'Kim': 'Thổ', 'Mộc': 'Thủy', 'Thủy': 'Kim', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa'}
            
            # Chi nhanh (vượng) và chi chậm (sinh)
            _chi_fast = _UNG_KY_CHI.get(_hanh_dt_kl, [])
            _hanh_sinh = _SINH_MAP.get(_hanh_dt_kl, '')
            _chi_slow = _UNG_KY_CHI.get(_hanh_sinh, []) if _hanh_sinh else []
            
            # Tìm ngày gần nhất cho từng Chi (3 ngày đầu cho mỗi chi)
            _fast_dates = []
            for _c in _chi_fast:
                _d, _cc, _thu, _off = _next_chi_date(_c, _now_uk)
                _d_date = _d.date() if hasattr(_d, 'date') else _d
                _fast_dates.append((_c, _d_date, _cc, _thu, _off))
            _slow_dates = []
            for _c in _chi_slow:
                _d, _cc, _thu, _off = _next_chi_date(_c, _now_uk)
                _d_date = _d.date() if hasattr(_d, 'date') else _d
                _slow_dates.append((_c, _d_date, _cc, _thu, _off))
            
            if _fast_dates:
                _earliest = min(_fast_dates, key=lambda x: x[4])
                _timing_fast = f"Nhanh nhất: ngày {_earliest[2]} ({_earliest[1].strftime('%d/%m/%Y')}) ({_earliest[3]}) — giờ {_CHI_GIO.get(_earliest[0], '?')} — tháng {_CHI_THANG.get(_earliest[0], '?')} (còn {_earliest[4]} ngày)"
                for _c, _d, _cc, _thu, _off in _fast_dates:
                    _timing_detail.append(f"NHANH: Ngày {_cc} = {_d.strftime('%d/%m/%Y')} ({_thu}) (giờ {_CHI_GIO.get(_c, '?')}) — còn {_off} ngày")
            if _slow_dates:
                _latest = max(_slow_dates, key=lambda x: x[4])
                _timing_slow = f"Chậm nhất: ngày {_latest[2]} ({_latest[1].strftime('%d/%m/%Y')}) ({_latest[3]}) — giờ {_CHI_GIO.get(_latest[0], '?')} — tháng {_CHI_THANG.get(_latest[0], '?')} (còn {_latest[4]} ngày)"
                for _c, _d, _cc, _thu, _off in _slow_dates:
                    _timing_detail.append(f"CHẬM: Ngày {_cc} = {_d.strftime('%d/%m/%Y')} ({_thu}) (giờ {_CHI_GIO.get(_c, '?')}) — còn {_off} ngày")
        
        # ═══ V42.3: PHÂN TÍCH THẾ VS ỨNG (cho câu hỏi THẮNG THUA) ═══
        _the_score = 0
        _ung_score = 0
        _the_ung_detail = []
        if is_competition_kl:
            _the_score, _ung_score, _the_ung_detail = self._calc_competition_scores(chart_data, luc_hao_data, mai_hoa_data)
        
        # ═══ TẠO PHÁN QUYẾT KHẲNG ĐỊNH ═══
        if is_competition_kl:
            # --- PHÁN QUYẾT THẮNG THUA dựa trên Thế vs Ứng ---
            _diff = _the_score - _ung_score
            if _diff >= 5:
                verdict_line = f"📢 **PHÁN QUYẾT: {_side_a} THẮNG ✅ (Thế +{_diff}) — {_side_b} THUA**"
            elif _diff >= 2:
                verdict_line = f"📢 **PHÁN QUYẾT: {_side_a} HƠI TRỘI ↗️ (Thế +{_diff}) — {_side_b} yếu hơn**"
            elif _diff >= -1:
                verdict_line = f"📢 **PHÁN QUYẾT: HÒA / CÂN BẰNG ⚖️ ({_side_a} ≈ {_side_b}, chênh {_diff:+d})**"
            elif _diff >= -4:
                verdict_line = f"📢 **PHÁN QUYẾT: {_side_b} HƠI TRỘI ↗️ (Ứng {abs(_diff):+d}) — {_side_a} yếu hơn**"
            else:
                verdict_line = f"📢 **PHÁN QUYẾT: {_side_b} THẮNG ✅ (Ứng {abs(_diff):+d}) — {_side_a} THUA**"
        elif is_life_death:
            if pct >= 50:
                verdict_line = f"📢 **PHÁN QUYẾT: CÒN SỐNG / QUA ĐƯỢC ({pct}%)**"
            elif pct >= 40:
                verdict_line = f"📢 **PHÁN QUYẾT: CÒN SỐNG nhưng NGUY KỊCH ({pct}%)**"
            else:
                verdict_line = f"📢 **PHÁN QUYẾT: ĐÃ MẤT hoặc KHÔNG QUA ĐƯỢC ({pct}%)**"
        elif is_should:
            if pct >= 55:
                verdict_line = f"📢 **PHÁN QUYẾT: NÊN — THUẬN LỢI ({pct}%)**"
            elif pct >= 45:
                verdict_line = f"📢 **PHÁN QUYẾT: CÓ THỂ — nhưng phải THẬN TRỌNG ({pct}%)**"
            else:
                verdict_line = f"📢 **PHÁN QUYẾT: KHÔNG NÊN — BẤT LỢI ({pct}%)**"
        elif is_yesno_kl:
            if pct >= 55:
                verdict_line = f"📢 **PHÁN QUYẾT: CÓ — THÀNH CÔNG ({pct}%)**"
            elif pct >= 50:
                verdict_line = f"📢 **PHÁN QUYẾT: CÓ — nhưng cần NỖ LỰC ({pct}%)**"
            elif pct >= 45:
                verdict_line = f"📢 **PHÁN QUYẾT: KHÓ THÀNH — cần đổi hướng hoặc đợi ({pct}%)**"
            else:
                verdict_line = f"📢 **PHÁN QUYẾT: KHÔNG — BẤT LỢI ({pct}%)**"
        elif is_timing_kl:
            # --- PHÁN QUYẾT THỜI GIAN ---
            if pct >= 55 and _timing_fast:
                verdict_line = f"📢 **PHÁN QUYẾT: SẮP TỚI — {_timing_fast}**"
            elif pct >= 45 and _timing_fast:
                verdict_line = f"📢 **PHÁN QUYẾT: TRUNG BÌNH — {_timing_fast}**"
            elif _timing_slow:
                verdict_line = f"📢 **PHÁN QUYẾT: CHẬM / CHƯA TỚI — {_timing_slow}**"
            else:
                verdict_line = f"📢 **PHÁN QUYẾT: CHƯA XÁC ĐỊNH THỜI GIAN ({pct}%)**"
        else:
            if pct >= 55:
                verdict_line = f"📢 **PHÁN QUYẾT: THUẬN LỢI ({pct}%)**"
            elif pct >= 50:
                verdict_line = f"📢 **PHÁN QUYẾT: CÓ THỂ ĐƯỢC — nhưng CẦN THẬN TRỌNG ({pct}%)**"
            elif pct >= 45:
                verdict_line = f"📢 **PHÁN QUYẾT: KHÓ KHĂN — cần tìm giải pháp ({pct}%)**"
            else:
                verdict_line = f"📢 **PHÁN QUYẾT: KHÔNG THUẬN — nên hoãn hoặc đổi hướng ({pct}%)**"
        
        lines.append(verdict_line)
        lines.append("")
        
        # ══════════════════════════════════════════════════════════
        # ★★★ PHẦN 0B: VÌ SAO — BẰNG CHỨNG THẬT TỪ DATA QUẺ ★★★
        # ══════════════════════════════════════════════════════════
        lines.append("**📋 VÌ SAO KẾT LUẬN NHƯ VẬY:**")
        
        import re as _re_vs
        def _extract_top_factors(factors, max_n=3):
            """Trích TOP factors theo |điểm| lớn nhất"""
            if not factors:
                return []
            scored = []
            for f in factors:
                m = _re_vs.search(r'([+-]\d+)\s*$', str(f))
                sc = int(m.group(1)) if m else 0
                scored.append((abs(sc), sc, str(f)))
            scored.sort(key=lambda x: x[0], reverse=True)
            return scored[:max_n]
        
        top_evidence = []
        
        # ① Lục Hào — DỮ LIỆU THẬT từ factors (ưu tiên cao nhất)
        _lh_top = _extract_top_factors(lh_factors or [], 3)
        if _lh_top:
            lh_icon = '✅' if 'CÁT' in str(luc_hao_verdict).upper() else ('🔴' if 'HUNG' in str(luc_hao_verdict).upper() else '🟡')
            _lh_details = '; '.join(f"{t[2][:70]}" for t in _lh_top)
            top_evidence.append(f"{lh_icon} **Lục Hào ({luc_hao_verdict}):** {_lh_details}")
        elif luc_hao_reason and len(str(luc_hao_reason)) > 5:
            lh_icon = '✅' if 'CÁT' in str(luc_hao_verdict).upper() else ('🔴' if 'HUNG' in str(luc_hao_verdict).upper() else '🟡')
            top_evidence.append(f"{lh_icon} **Lục Hào ({luc_hao_verdict}):** {str(luc_hao_reason)[:120]}")
        
        # ② Kỳ Môn — DỮ LIỆU THẬT từ factors
        _km_top = _extract_top_factors(km_factors or [], 3)
        if _km_top:
            km_icon = '✅' if 'CÁT' in str(ky_mon_verdict).upper() else ('🔴' if 'HUNG' in str(ky_mon_verdict).upper() else '🟡')
            _km_details = '; '.join(f"{t[2][:70]}" for t in _km_top)
            top_evidence.append(f"{km_icon} **Kỳ Môn ({ky_mon_verdict}):** {_km_details}")
        elif ky_mon_reason and len(str(ky_mon_reason)) > 5:
            km_icon = '✅' if 'CÁT' in str(ky_mon_verdict).upper() else ('🔴' if 'HUNG' in str(ky_mon_verdict).upper() else '🟡')
            top_evidence.append(f"{km_icon} **Kỳ Môn ({ky_mon_verdict}):** {str(ky_mon_reason)[:120]}")
        
        # ③ Mai Hoa — DỮ LIỆU THẬT từ factors
        _mh_top = _extract_top_factors(mh_factors or [], 2)
        if _mh_top:
            mh_icon = '✅' if 'CÁT' in str(mai_hoa_verdict).upper() else ('🔴' if 'HUNG' in str(mai_hoa_verdict).upper() else '🟡')
            _mh_details = '; '.join(f"{t[2][:70]}" for t in _mh_top)
            top_evidence.append(f"{mh_icon} **Mai Hoa ({mai_hoa_verdict}):** {_mh_details}")
        elif mai_hoa_reason and len(str(mai_hoa_reason)) > 5:
            mh_icon = '✅' if 'CÁT' in str(mai_hoa_verdict).upper() else ('🔴' if 'HUNG' in str(mai_hoa_verdict).upper() else '🟡')
            top_evidence.append(f"{mh_icon} **Mai Hoa ({mai_hoa_verdict}):** {str(mai_hoa_reason)[:120]}")
        
        # ④ Đại Lục Nhâm (nếu có verdict rõ)
        if luc_nham_reason and ('CÁT' in str(luc_nham_verdict).upper() or 'HUNG' in str(luc_nham_verdict).upper()):
            ln_icon = '✅' if 'CÁT' in str(luc_nham_verdict).upper() else '🔴'
            top_evidence.append(f"{ln_icon} **Đại Lục Nhâm ({luc_nham_verdict}):** {str(luc_nham_reason)[:80]}")
        
        # ⑤ Thái Ất (nếu có verdict rõ)
        if thai_at_reason and ('CÁT' in str(thai_at_verdict).upper() or 'HUNG' in str(thai_at_verdict).upper()):
            ta_icon = '✅' if 'CÁT' in str(thai_at_verdict).upper() else '🔴'
            top_evidence.append(f"{ta_icon} **Thái Ất ({thai_at_verdict}):** {str(thai_at_reason)[:80]}")
        
        # Hiển thị TOP evidence với đánh số
        for i, ev in enumerate(top_evidence[:5], 1):
            lines.append(f"  {i}. {ev}")
        
        if not top_evidence:
            lines.append(f"  • Điểm tổng hợp 6 phương pháp: **{pct}%** (>50% = thuận, <50% = nghịch)")
        
        # Tóm tắt đếm PP
        cat_pp = sum(1 for _, (v, _) in verdicts_map.items() if 'CÁT' in str(v).upper())
        hung_pp = sum(1 for _, (v, _) in verdicts_map.items() if 'HUNG' in str(v).upper())
        binh_pp = 5 - cat_pp - hung_pp
        lines.append(f"\n→ **Tổng kết: {cat_pp}/5 PP cho CÁT, {hung_pp}/5 PP cho HUNG, {binh_pp}/5 PP BÌNH** → Điểm: {pct}%")
        lines.append("")
        
        # ══════════════════════════════════════════════════════════
        # ★★★ PHẦN 0C: ỨNG KỲ — THỜI GIAN CỤ THỂ ★★★
        # ══════════════════════════════════════════════════════════
        _UK_TIMING = {
            'Kim': {'thang': 'tháng Thân/Dậu (tháng 7-8 ÂL)', 'ngay': 'ngày Canh/Tân', 'huong': 'Tây'},
            'Mộc': {'thang': 'tháng Dần/Mão (tháng 1-2 ÂL)', 'ngay': 'ngày Giáp/Ất', 'huong': 'Đông'},
            'Thủy': {'thang': 'tháng Hợi/Tý (tháng 10-11 ÂL)', 'ngay': 'ngày Nhâm/Quý', 'huong': 'Bắc'},
            'Hỏa': {'thang': 'tháng Tỵ/Ngọ (tháng 4-5 ÂL)', 'ngay': 'ngày Bính/Đinh', 'huong': 'Nam'},
            'Thổ': {'thang': 'tháng Thìn/Tuất/Sửu/Mùi (tháng 3/6/9/12 ÂL)', 'ngay': 'ngày Mậu/Kỷ', 'huong': 'Trung Tâm'},
        }
        _uk_info = _UK_TIMING.get(_hanh_dt_kl, None)
        if _uk_info:
            lines.append(f"**⏳ ỨNG KỲ (Thời gian sự việc ứng nghiệm):**")
            if pct >= 50:
                lines.append(f"  • Thuận lợi nhất: **{_uk_info['thang']}**, {_uk_info['ngay']}")
                lines.append(f"  • Hướng tốt: **{_uk_info['huong']}** (theo hành {_hanh_dt_kl} của DT)")
            else:
                # Khi bất lợi → nên ĐỢI tháng hành sinh DT
                _hanh_sinh_dt = {v: k for k, v in SINH.items()}.get(_hanh_dt_kl, '?')
                _uk_sinh = _UK_TIMING.get(_hanh_sinh_dt, {})
                lines.append(f"  • Nên ĐỢI: **{_uk_sinh.get('thang', '?')}** (hành {_hanh_sinh_dt} sinh {_hanh_dt_kl})")
                lines.append(f"  • Tránh: {_uk_info['thang']} (hành {_hanh_dt_kl} bị khắc = thêm bất lợi)")
            lines.append("")
        
        # ══════════════════════════════════════════════════════════
        # PHẦN 1: PHÂN TÍCH CHI TIẾT 5PP (collapsible)
        # ══════════════════════════════════════════════════════════
        lines.append("**📖 PHÂN TÍCH 5 PHƯƠNG PHÁP:**")
        for method, (verdict, reason) in verdicts_map.items():
            v_upper = str(verdict).upper() if verdict else ''
            icon = '✅' if 'CÁT' in v_upper else ('🔴' if 'HUNG' in v_upper else '🟡')
            method_detail = ''
            for m, s, _ in dt_statuses:
                if m == method:
                    method_detail = s
                    break
            reason_str = str(reason)[:150] if reason else ''
            if method_detail:
                lines.append(f"{icon} **{method} ({verdict}):** {method_detail}")
                if reason_str and reason_str != method_detail:
                    lines.append(f"   → {reason_str}")
            else:
                lines.append(f"{icon} **{method} ({verdict}):** {reason_str}")
        
        # PHẦN 2: YẾU TỐ THUẬN vs NGHỊCH
        lines.append("")
        lines.append("**⚖️ TỔNG HỢP YẾU TỐ:**")
        if thuan_factors:
            lines.append(f"**✅ THUẬN ({len(thuan_factors)}):**")
            for f in thuan_factors[:5]:
                lines.append(f"• {f}")
        if nghich_factors:
            lines.append(f"**🔴 NGHỊCH ({len(nghich_factors)}):**")
            for f in nghich_factors[:5]:
                lines.append(f"• {f}")
        
        # Cross-method notes
        km_v = str(ky_mon_verdict).upper() if ky_mon_verdict else ''
        lh_v = str(luc_hao_verdict).upper() if luc_hao_verdict else ''
        mh_v = str(mai_hoa_verdict).upper() if mai_hoa_verdict else ''
        
        cross_notes = []
        if ('CÁT' in km_v and 'HUNG' in lh_v) or ('HUNG' in km_v and 'CÁT' in lh_v):
            cross_notes.append(f"⚡ KM ({ky_mon_verdict}) ngược LH ({luc_hao_verdict}): khởi đầu khác quá trình.")
        if ('CÁT' in mh_v and 'HUNG' in lh_v):
            cross_notes.append(f"⚡ MH ({mai_hoa_verdict}) thuận nhưng LH ({luc_hao_verdict}) nghịch: quan hệ tốt nhưng DT yếu.")
        
        all_verdicts = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict, luc_nham_verdict, thai_at_verdict]
        non_binh = [v for v in all_verdicts if v and v != 'BÌNH']
        if non_binh and all('CÁT' in str(v).upper() for v in non_binh):
            cross_notes.append("🌟 TẤT CẢ PP cho CÁT → Cực kỳ rõ ràng, không mâu thuẫn.")
        elif non_binh and all('HUNG' in str(v).upper() for v in non_binh):
            cross_notes.append("⛔ TẤT CẢ PP cho HUNG → Cực kỳ rõ ràng — PHẢI dừng/đổi hướng.")
        
        if cross_notes:
            lines.append("")
            lines.append("**🔗 PHÂN TÍCH CHÉO:**")
            for note in cross_notes:
                lines.append(note)
        
        # ══════════════════════════════════════════════════════════
        # ★★★ PHẦN 3: KẾT LUẬN KHẲNG ĐỊNH + GIẢI PHÁP + LỜI KHUYÊN ★★★
        # ══════════════════════════════════════════════════════════
        lines.append("")
        lines.append(f"**✅ KẾT LUẬN KHẲNG ĐỊNH (Điểm: {pct}%):**")
        
        # === TẠO KẾT LUẬN DỨT KHOÁT THEO TỪNG LOẠI CÂU HỎI ===
        if is_competition_kl:
            # ═══ V42.3: KẾT LUẬN THẮNG THUA — THẾ VS ỨNG ═══
            _diff_kl = _the_score - _ung_score
            
            # Bằng chứng từ 3 phương pháp
            _evidence_lines = []
            for _td in _the_ung_detail:
                _evidence_lines.append(f"• {_td}")
            _evidence_str = '\n'.join(_evidence_lines) if _evidence_lines else '• Chưa đủ dữ liệu chi tiết'
            
            if _diff_kl >= 5:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: ✅ {_side_a} THẮNG — {_side_b} THUA (Chênh: +{_diff_kl})**\n"
                    f"• {_side_a} (Thế={_the_score:+d}) >> {_side_b} (Ứng={_ung_score:+d}) → {_side_a} áp đảo.\n"
                    f"\n**📊 CĂN CỨ 3 PHƯƠNG PHÁP:**\n"
                    f"{_evidence_str}\n"
                    f"\n**🏆 QUY TẮC XÁC ĐỊNH THẮNG THUA:**\n"
                    f"• **Lục Hào:** {_side_a} = hào Thế (己方), {_side_b} = hào Ứng (對方) — so Vượng/Suy + Sinh/Khắc\n"
                    f"• **Kỳ Môn:** {_side_a} = Nhật Can (Chủ), {_side_b} = Thời Can (Khách)\n"
                    f"• **Mai Hoa:** {_side_a} = Thể Quái, {_side_b} = Dụng Quái\n"
                    f"\n💡 **LỜI KHUYÊN:** {_side_a} có ưu thế lớn. Nếu đặt cược → chọn {_side_a}."
                )
            elif _diff_kl >= 2:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: ↗️ {_side_a} HƠI TRỘI hơn {_side_b} (Chênh: +{_diff_kl})**\n"
                    f"• {_side_a} (Thế={_the_score:+d}) > {_side_b} (Ứng={_ung_score:+d}) → {_side_a} nhỉnh hơn.\n"
                    f"\n**📊 CĂN CỨ:**\n{_evidence_str}\n"
                    f"\n💡 **LỜI KHUYÊN:** Nghiêng về {_side_a} nhưng không áp đảo. Cần thêm yếu tố phụ."
                )
            elif _diff_kl >= -1:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: ⚖️ HÒA — {_side_a} ≈ {_side_b} (Chênh: {_diff_kl:+d})**\n"
                    f"• {_side_a} (Thế={_the_score:+d}) ≈ {_side_b} (Ứng={_ung_score:+d}) → Ngang sức.\n"
                    f"\n**📊 CĂN CỨ:**\n{_evidence_str}\n"
                    f"\n💡 **LỜI KHUYÊN:** {_side_a} và {_side_b} ngang sức. Phụ thuộc yếu tố phụ."
                )
            elif _diff_kl >= -4:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: ↗️ {_side_b} HƠI TRỘI hơn {_side_a} (Chênh: {_diff_kl:+d})**\n"
                    f"• {_side_b} (Ứng={_ung_score:+d}) > {_side_a} (Thế={_the_score:+d}) → {_side_b} nhỉnh hơn.\n"
                    f"\n**📊 CĂN CỨ:**\n{_evidence_str}\n"
                    f"\n💡 **LỜI KHUYÊN:** Nghiêng về {_side_b}. {_side_a} cần thêm trợ lực."
                )
            else:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: ✅ {_side_b} THẮNG — {_side_a} THUA (Chênh: {_diff_kl:+d})**\n"
                    f"• {_side_b} (Ứng={_ung_score:+d}) >> {_side_a} (Thế={_the_score:+d}) → {_side_b} áp đảo.\n"
                    f"\n**📊 CĂN CỨ 3 PHƯƠNG PHÁP:**\n"
                    f"{_evidence_str}\n"
                    f"\n**🏆 QUY TẮC XÁC ĐỊNH:**\n"
                    f"• **Lục Hào:** {_side_b} (Ứng) vượng hơn {_side_a} (Thế)\n"
                    f"• **Kỳ Môn:** {_side_b} (Khách) khắc/trội {_side_a} (Chủ)\n"
                    f"• **Mai Hoa:** {_side_b} (Dụng) khắc {_side_a} (Thể)\n"
                    f"\n💡 **LỜI KHUYÊN:** {_side_b} có ưu thế lớn. Nếu đặt cược → chọn {_side_b}."
                )
        elif is_timing_kl:
            # ═══ V42.3: KẾT LUẬN THỜI GIAN CỤ THỂ ═══
            _td_lines = []
            for _td in _timing_detail:
                _td_lines.append(f"• {_td}")
            _td_str = '\n'.join(_td_lines) if _td_lines else '• Không đủ dữ liệu'
            
            if pct >= 55:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: SỰ VIỆC SẮP XẢY RA ({pct}%)**\n"
                    f"• {dung_than} ({_hanh_dt_kl}) VƯỢNG → sự việc đến NHANH.\n"
                    f"\n**⏰ THỜI GIAN CỤ THỂ:**\n"
                    f"• ⚡ {_timing_fast}\n"
                    f"• 🕒 {_timing_slow}\n"
                    f"\n**📊 CHI TIẾT ỨNG KỲ TỪ 3 PHƯƠNG PHÁP:**\n{_td_str}\n"
                    f"\n**🏆 QUY TẮC XÁC ĐỊNH:**\n"
                    f"• DT hành {_hanh_dt_kl} VƯỢNG → ứng nghiệm vào ngày/tháng/năm Chi cùng hành (Trị)\n"
                    f"• DT hành {_hanh_dt_kl} SUY → chờ hành SINH ({SINH.get(_hanh_dt_kl, '?')}) đến giải cứu\n"
                    f"\n💡 **LỜI KHUYÊN:** Sự việc sẽ đến SớM. Chú ý những ngày Chi vượng đã nêu (ưu tiên ngày gần nhất)."
                )
            elif pct >= 45:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: SỰ VIỆC ĐẾN TRUNG BÌNH ({pct}%)**\n"
                    f"• {dung_than} ({_hanh_dt_kl}) BÌNH → không nhanh không chậm.\n"
                    f"\n**⏰ THỜI GIAN CỤ THỂ:**\n"
                    f"• ⚡ {_timing_fast}\n"
                    f"• 🕒 {_timing_slow}\n"
                    f"\n**📊 CHI TIẾT:**\n{_td_str}\n"
                    f"\n💡 **LỜI KHUYÊN:** Sự việc sẽ đến nhưng cần kiên nhẫn. Chú ý các ngày Chi nêu trên."
                )
            else:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: SỰ VIỆC ĐẾN CHẬM / CHƯA TỚI ({pct}%)**\n"
                    f"• {dung_than} ({_hanh_dt_kl}) SUY → chưa đủ lực, cần chờ hành sinh.\n"
                    f"\n**⏰ THỜI GIAN CỤ THỂ:**\n"
                    f"• ⚡ {_timing_fast or 'Khó đến nhanh'}\n"
                    f"• 🕒 {_timing_slow or 'Cần chờ thêm'}\n"
                    f"\n**📊 CHI TIẾT:**\n{_td_str}\n"
                    f"\n💡 **LỜI KHUYÊN:** Sự việc chưa tới lúc. Kiên nhẫn chờ hành {SINH.get(_hanh_dt_kl, '?')} vượng (xem bảng \u1ee8ng K\u1ef3)."
                )
        elif is_life_death:
            if pct >= 50:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: CÒN SỐNG / QUA ĐƯỢC ({pct}%).**\n"
                    f"• {dung_than} ({_hanh_dt_kl}) CÓ SINH KHÍ — chưa tuyệt.\n"
                )
                ev_lines = []
                if luc_hao_reason: ev_lines.append(f"Lục Hào: {luc_hao_reason[:80]}")
                if any('sinh' in str(e).lower() for e in chain_evidence): ev_lines.append("Có yếu tố SINH → được nuôi dưỡng")
                if any('động' in str(e).lower() for e in chain_evidence): ev_lines.append("DT ĐỘNG → còn hoạt động")
                if ev_lines: conclusion += f"• Bằng chứng: {'; '.join(ev_lines[:3])}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Cần chăm sóc tích cực, tìm phương sinh (hành {SINH.get(_hanh_dt_kl, '?')}) để tăng sinh khí.\n"
                    f"💡 **LỜI KHUYÊN:** Tuy còn sống nhưng có {hung_count} yếu tố nghịch. Không chủ quan — hành động ngay để cải thiện."
                )
            elif pct >= 40:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: CÒN SỐNG nhưng NGUY KỊCH ({pct}%).**\n"
                    f"• {dung_than} ({_hanh_dt_kl}) SUY nhưng CHƯA TUYỆT.\n"
                    f"\n🔧 **GIẢI PHÁP:** Can thiệp KHẨN CẤP. Tìm Tử Tôn (thuốc/bác sĩ) hỗ trợ. Dùng hành {SINH.get(_hanh_dt_kl, '?')} để cứu.\n"
                    f"💡 **LỜI KHUYÊN:** Tình trạng nguy — mỗi phút đều quý. Đừng chần chừ."
                )
            else:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: ĐÃ MẤT hoặc KHÔNG QUA ĐƯỢC ({pct}%).**\n"
                    f"• {dung_than} ({_hanh_dt_kl}) SUY TUYỆT — sinh khí cạn.\n"
                    f"\n🔧 **GIẢI PHÁP:** Nếu chưa mất: cần phép lạ hoặc can thiệp đặc biệt. Chuẩn bị tinh thần.\n"
                    f"💡 **LỜI KHUYÊN:** Chấp nhận thực tế. Lo hậu sự hoặc tìm cách giảm đau khổ."
                )
                
        elif is_should:
            if pct >= 55:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: NÊN LÀM — THUẬN LỢI ({pct}%).**\n"
                    f"• {dung_than} vượng, {cat_count} yếu tố thuận > {hung_count} nghịch.\n"
                )
                if ky_mon_reason: conclusion += f"• KM: {ky_mon_reason[:70]}.\n"
                if luc_hao_reason: conclusion += f"• LH: {luc_hao_reason[:70]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Tiến hành ngay. Chọn thời điểm hành {_hanh_dt_kl} vượng. Tránh ngày xung khắc.\n"
                    f"💡 **LỜI KHUYÊN:** Đây là thời cơ tốt. Hành động quyết đoán, không do dự."
                )
            elif pct >= 45:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: CÓ THỂ LÀM — nhưng THẬN TRỌNG ({pct}%).**\n"
                    f"• Thế trận chưa rõ ({cat_count} thuận vs {hung_count} nghịch).\n"
                )
                if thuan_factors: conclusion += f"• Thuận: {thuan_factors[0][:60]}.\n"
                if nghich_factors: conclusion += f"• Rủi ro: {nghich_factors[0][:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Chuẩn bị phương án B. Giảm rủi ro bằng cách bổ sung hành {SINH.get(_hanh_dt_kl, '?')}.\n"
                    f"💡 **LỜI KHUYÊN:** Tiến hành ĐƯỢC nhưng không nên ALL-IN. Dự phòng 30-40% cho trường hợp xấu."
                )
            else:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: KHÔNG NÊN LÀM — BẤT LỢI ({pct}%).**\n"
                    f"• {dung_than} suy ({hung_count} nghịch > {cat_count} thuận).\n"
                )
                if ky_mon_reason: conclusion += f"• KM: {ky_mon_reason[:70]}.\n"
                if luc_hao_reason: conclusion += f"• LH: {luc_hao_reason[:70]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Hoãn lại. Đợi khi {dung_than} ({_hanh_dt_kl}) được sinh trợ (tháng hành {SINH.get(_hanh_dt_kl, '?')}).\n"
                    f"💡 **LỜI KHUYÊN:** Thời điểm này KHÔNG thuận. Kiên nhẫn chờ — không ép khi thế yếu."
                )
                
        elif is_yesno_kl:
            if pct >= 55:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: CÓ / ĐƯỢC / THÀNH ({pct}%).**\n"
                    f"• {dung_than} vượng, {cat_count} thuận > {hung_count} nghịch.\n"
                )
                if ky_mon_reason: conclusion += f"• KM: {ky_mon_reason[:60]}.\n"
                if luc_hao_reason: conclusion += f"• LH: {luc_hao_reason[:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Tận dụng cơ hội hiện tại. Hành động sớm để đạt kết quả tối ưu.\n"
                    f"💡 **LỜI KHUYÊN:** Sự việc CÓ KHẢ NĂNG THÀNH. Nắm bắt, không chần chừ."
                )
            elif pct >= 50:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: CÓ — nhưng phải NỖ LỰC ({pct}%).**\n"
                    f"• Nghiêng CÓ ({cat_count} thuận vs {hung_count} nghịch) nhưng chưa chắc chắn.\n"
                )
                if thuan_factors: conclusion += f"• Yếu tố quyết định: {thuan_factors[0][:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Cần bổ sung lực. Dùng hành {SINH.get(_hanh_dt_kl, '?')} để tăng {dung_than}.\n"
                    f"💡 **LỜI KHUYÊN:** Tỷ lệ thành >50% nhưng KHÔNG dễ. Cần nỗ lực thêm 20-30%."
                )
            elif pct >= 45:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: KHÓ THÀNH ({pct}%) — cần đổi cách hoặc đợi.**\n"
                    f"• Nghiêng KHÔNG ({hung_count} nghịch > {cat_count} thuận).\n"
                )
                if nghich_factors: conclusion += f"• Trở ngại chính: {nghich_factors[0][:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Đổi phương pháp tiếp cận hoặc đợi tháng {_hanh_dt_kl} vượng.\n"
                    f"💡 **LỜI KHUYÊN:** Không nên ép. Thay đổi chiến lược hoặc kiên nhẫn chờ thời."
                )
            else:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: KHÔNG / THẤT BẠI ({pct}%).**\n"
                    f"• {dung_than} suy ({hung_count} nghịch >> {cat_count} thuận).\n"
                )
                if ky_mon_reason: conclusion += f"• KM: {ky_mon_reason[:60]}.\n"
                if luc_hao_reason: conclusion += f"• LH: {luc_hao_reason[:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Dừng lại. Tìm hướng đi mới hoặc đợi lúc {dung_than} ({_hanh_dt_kl}) được sinh trợ.\n"
                    f"💡 **LỜI KHUYÊN:** Sự việc KHÓ THÀNH. Chuyển hướng là lựa chọn khôn ngoan nhất."
                )
        else:
            # CÂU HỎI TỔNG QUÁT — vẫn KHẲNG ĐỊNH rõ ràng
            if pct >= 55:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: THUẬN LỢI ({pct}%).**\n"
                    f"• {dung_than} được hỗ trợ mạnh ({cat_count} thuận > {hung_count} nghịch).\n"
                )
                if ky_mon_reason: conclusion += f"• KM: {ky_mon_reason[:70]}.\n"
                if luc_hao_reason: conclusion += f"• LH: {luc_hao_reason[:70]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Tận dụng thế mạnh hiện tại. Phát triển theo hướng hành {_hanh_dt_kl}.\n"
                    f"💡 **LỜI KHUYÊN:** Tình hình TỐT. Nắm bắt cơ hội, mở rộng."
                )
            elif pct >= 50:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: CÓ THỂ ĐƯỢC — nhưng CẦN THẬN TRỌNG ({pct}%).**\n"
                    f"• {cat_count} thuận vs {hung_count} nghịch — hơi nghiêng tốt.\n"
                )
                if thuan_factors: conclusion += f"• Thuận: {thuan_factors[0][:60]}.\n"
                if nghich_factors: conclusion += f"• Chú ý: {nghich_factors[0][:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Giữ vững. Tránh mạo hiểm. Bổ sung hành {SINH.get(_hanh_dt_kl, '?')} để tăng lực.\n"
                    f"💡 **LỜI KHUYÊN:** Tình hình OK nhưng KHÔNG phải lúc liều. Ổn định là ưu tiên."
                )
            elif pct >= 45:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: KHÓ KHĂN — cần giải pháp ({pct}%).**\n"
                    f"• {hung_count} nghịch > {cat_count} thuận — thế trận bất lợi.\n"
                )
                if nghich_factors: conclusion += f"• Trở ngại: {nghich_factors[0][:60]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Giảm thiểu rủi ro. Tìm quý nhân (hành {SINH.get(_hanh_dt_kl, '?')}) hỗ trợ. Không nên hành động lớn.\n"
                    f"💡 **LỜI KHUYÊN:** Giai đoạn PHÒNG THỦ. Bảo toàn lực lượng, chờ cơ hội tốt hơn."
                )
            else:
                conclusion = (
                    f"**👉 KHẲNG ĐỊNH: BẤT LỢI ({pct}%) — cần đổi hướng.**\n"
                    f"• {dung_than} suy ({hung_count} nghịch >> {cat_count} thuận).\n"
                )
                if ky_mon_reason: conclusion += f"• KM: {ky_mon_reason[:70]}.\n"
                if luc_hao_reason: conclusion += f"• LH: {luc_hao_reason[:70]}.\n"
                conclusion += (
                    f"\n🔧 **GIẢI PHÁP:** Dừng kế hoạch hiện tại. Đợi tháng hành {SINH.get(_hanh_dt_kl, '?')} vượng hoặc tìm hướng mới.\n"
                    f"💡 **LỜI KHUYÊN:** Thời điểm XẤU. Lui một bước để tiến hai bước — kiên nhẫn là vũ khí."
                )
        
        lines.append(conclusion)
        
        return "\n".join(lines)

    # ===========================
    # CORE: ANSWER QUESTION
    # ===========================
    def answer_question(self, question, chart_data=None, topic=None, selected_subject=None, mai_hoa_data=None, luc_hao_data=None, **kwargs):
        """Trả lời câu hỏi bằng phân tích rule-based từ dữ liệu quẻ"""
        
        if not question or len(question.strip()) < 2:
            return "Vui lòng nhập câu hỏi."
        
        # Greeting — V9.0: Dùng word-level matching (tránh "hi" match "nhiêu")
        social = ["chào", "hello", "hi", "bạn ơi"]
        q_words = question.lower().split()
        if len(q_words) < 5 and any(k in q_words or k == question.lower().strip() for k in social):
            lc = len(_load_learned_topics())
            return f"Chào bạn, tôi là THIÊN CƠ ĐẠI SƯ (V42.2 — Answer-First + 100% Data Direct + KV/DM Chuẩn QMDG). 6 phương pháp (KM+LH+MH+TB+LN+TA) → 78 yếu tố → 1 câu trả lời! Vạn Vật 2226+ items. Đã học {lc} câu hỏi mới."
        

        # V31.2: LÀM SẠCH CÂU HỎI — loại bỏ từ thừa, dấu thừa, noise
        original_question = question
        question = clean_question(question)
        if len(question) < 2:
            question = original_question.strip()
        
        # ═══════════════════════════════════════════════════════
        # V32.4: TỰ ĐỘNG GIEO QUẺ KHI KHÔNG CÓ DỮ LIỆU
        # Đảm bảo 6/6 phương pháp LUÔN có data, kể cả Hỏi Nhanh
        # ═══════════════════════════════════════════════════════
        import datetime as _dt324
        _now324 = _dt324.datetime.now()
        _y, _m, _d, _h = _now324.year, _now324.month, _now324.day, _now324.hour
        
        # 1. Mai Hoa: gieo theo thời gian
        if not mai_hoa_data:
            try:
                from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, giai_qua
                mai_hoa_data = tinh_qua_theo_thoi_gian(_y, _m, _d, _h)
                mai_hoa_data['interpretation'] = giai_qua(mai_hoa_data, topic or 'Chung')
                self.log_step("V32.4 AutoCast", "MAI_HOA", f"Quẻ: {mai_hoa_data.get('ten_que', '?')}")
            except Exception as e:
                self.log_step("V32.4 AutoCast", "MH_ERR", str(e)[:60])
        
        # 2. Lục Hào: gieo theo thời gian
        if not luc_hao_data:
            try:
                from luc_hao_kinh_dich import lap_qua_luc_hao
                _can_ngay = 'Giáp'
                _chi_ngay = 'Tý'
                if chart_data and isinstance(chart_data, dict):
                    _can_ngay = chart_data.get('can_ngay', 'Giáp')
                    _chi_ngay = chart_data.get('chi_ngay', 'Tý')
                else:
                    # Tính Can Ngày từ thời gian
                    _cans = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
                    _chis = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                    # V42.8f FIX: Dùng _jdn chuẩn thay vì formula sai (lệch 11-13 ngày!)
                    try:
                        from xem_ngay_dep import _jdn as _jdn_func
                        _jdn_val = _jdn_func(_d, _m, _y)
                    except ImportError:
                        # Fallback: accurate Gregorian JDN
                        _a = (14 - _m) // 12
                        _yy = _y + 4800 - _a
                        _mm = _m + 12 * _a - 3
                        _jdn_val = _d + (153 * _mm + 2) // 5 + 365 * _yy + _yy // 4 - _yy // 100 + _yy // 400 - 32045
                    _can_ngay = _cans[(_jdn_val + 9) % 10]
                    _chi_ngay = _chis[(_jdn_val + 1) % 12]
                
                luc_hao_data = lap_qua_luc_hao(
                    _y, _m, _d, _h,
                    topic=topic or 'Chung',
                    can_ngay=_can_ngay,
                    chi_ngay=_chi_ngay
                )
                self.log_step("V32.4 AutoCast", "LUC_HAO", f"Can={_can_ngay}, Chi={_chi_ngay}")
            except Exception as e:
                self.log_step("V32.4 AutoCast", "LH_ERR", str(e)[:60])
        
        # 3. Chart Data (Kỳ Môn ĐẦY ĐỦ 9 CUNG): gọi hàm thật từ qmdg_calc + qmdg_data
        if not chart_data or not isinstance(chart_data, dict) or not chart_data.get('thien_ban'):
            try:
                from qmdg_calc import calculate_qmdg_params
                from qmdg_data import lap_ban_qmdg
                
                # Tính tham số Kỳ Môn từ thời gian hiện tại
                _params = calculate_qmdg_params(_now324)
                
                # Lập bàn 9 cung đầy đủ (Sao/Cửa/Thần/Can Thiên bàn)
                _thien_ban, _can_thien_ban, _nhan_ban, _than_ban, _truc_phu_cung = lap_ban_qmdg(
                    _params['cuc'],
                    _params['truc_phu'],
                    _params['truc_su'],
                    _params['can_gio'],
                    _params['chi_gio'],
                    _params['is_duong_don']
                )
                
                # Tạo dia_ban từ qmdg_calc
                from qmdg_data import an_bai_luc_nghi
                _dia_ban = an_bai_luc_nghi(_params['cuc'], _params['is_duong_don'])
                
                chart_data = {
                    'can_ngay': _params['can_ngay'],
                    'chi_ngay': _params['chi_ngay'],
                    'can_gio': _params['can_gio'],
                    'chi_gio': _params['chi_gio'],
                    'can_thang': _params['can_thang'],
                    'chi_thang': _params['chi_thang'],
                    'can_nam': _params['can_nam'],
                    'chi_nam': _params['chi_nam'],
                    'tiet_khi': _params['tiet_khi'],
                    'cuc': _params['cuc'],
                    'is_duong_don': _params['is_duong_don'],
                    'tuan_thu': _params['tuan_thu'],
                    'truc_phu': _params['truc_phu'],
                    'truc_su': _params['truc_su'],
                    'thien_ban': _thien_ban,
                    'can_thien_ban': _can_thien_ban,
                    'nhan_ban': _nhan_ban,
                    'than_ban': _than_ban,
                    'dia_ban': _dia_ban,
                    '_auto_generated': True
                }
                self.log_step("V32.5 AutoCast", "CHART_FULL", 
                    f"9 Cung OK | Can={_params['can_ngay']} {_params['chi_ngay']} | "
                    f"Cục={_params['cuc']} | TK={_params['tiet_khi']}")
            except Exception as e:
                self.log_step("V32.5 AutoCast", "CHART_ERR", str(e)[:100])
                # Fallback tối thiểu
                try:
                    _cans = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
                    _chis = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                    # V42.8f FIX: Dùng _jdn chuẩn thay vì formula sai
                    try:
                        from xem_ngay_dep import _jdn as _jdn_func2
                        _jdn_val2 = _jdn_func2(_d, _m, _y)
                    except ImportError:
                        _a2 = (14 - _m) // 12
                        _yy2 = _y + 4800 - _a2
                        _mm2 = _m + 12 * _a2 - 3
                        _jdn_val2 = _d + (153 * _mm2 + 2) // 5 + 365 * _yy2 + _yy2 // 4 - _yy2 // 100 + _yy2 // 400 - 32045
                    chart_data = {
                        'can_ngay': _cans[(_jdn_val2 + 9) % 10],
                        'chi_ngay': _chis[(_jdn_val2 + 1) % 12],
                        'chi_gio': _chis[(_h // 2) % 12],
                        'can_thien_ban': {},
                        '_auto_generated': True
                    }
                except:
                    pass

        # ====== V8.2: SMART CATEGORY DETECTION ======
        # Phân loại câu hỏi theo 6 nhóm lớn thay vì match 220+ topics cụ thể
        q_lower = question.lower()
        
        # V36.0: HỖ TRỢ KHÔNG DẤU — map từ không dấu → có dấu
        _VN_NO_DIAC_MAP = {
            'benh': 'bệnh', 'om': 'ốm', 'dau': 'đau', 'suc khoe': 'sức khỏe', 'khoe': 'khỏe',
            'chet': 'chết', 'song': 'sống', 'chua': 'chữa', 'benh vien': 'bệnh viện',
            'phau thuat': 'phẫu thuật', 'ung thu': 'ung thư', 'tai nan': 'tai nạn',
            'qua khoi': 'qua khỏi', 'thuoc': 'thuốc', 'tri benh': 'trị bệnh',
            'gia dinh': 'gia đình', 'mang thai': 'mang thai',
            'tien': 'tiền', 'tai chinh': 'tài chính', 'mua ban': 'mua bán',
            'dau tu': 'đầu tư', 'giau': 'giàu', 'ngheo': 'nghèo', 'luong': 'lương',
            'thu nhap': 'thu nhập', 'no': 'nợ', 'vay': 'vay', 'kinh doanh': 'kinh doanh',
            'buon ban': 'buôn bán', 'lai': 'lãi', 'lo': 'lỗ', 'co phieu': 'cổ phiếu',
            'bat dong san': 'bất động sản', 'mua nha': 'mua nhà', 'nha dat': 'nhà đất',
            'von': 'vốn', 'trung so': 'trúng số', 'tai san': 'tài sản', 'vang': 'vàng',
            'viec': 'việc', 'cong viec': 'công việc', 'sep': 'sếp',
            'thang tien': 'thăng tiến', 'thang chuc': 'thăng chức',
            'thi': 'thi', 'do': 'đỗ', 'truot': 'trượt', 'phong van': 'phỏng vấn',
            'xin viec': 'xin việc', 'nghi viec': 'nghỉ việc', 'sa thai': 'sa thải',
            'hop dong': 'hợp đồng', 'du an': 'dự án', 'kien': 'kiện', 'toa': 'tòa',
            'su nghiep': 'sự nghiệp', 'khoi nghiep': 'khởi nghiệp',
            'yeu': 'yêu', 'nguoi yeu': 'người yêu', 'vo': 'vợ', 'chong': 'chồng',
            'hon nhan': 'hôn nhân', 'cuoi': 'cưới', 'ly hon': 'ly hôn',
            'tinh': 'tình', 'hen ho': 'hẹn hò', 'chia tay': 'chia tay',
            'ngoai tinh': 'ngoại tình', 'duyen': 'duyên', 'ban trai': 'bạn trai',
            'ban gai': 'bạn gái', 'tinh cam': 'tình cảm', 'hanh phuc': 'hạnh phúc',
            'lay vo': 'lấy vợ', 'lay chong': 'lấy chồng', 'ket hon': 'kết hôn',
            'tinh yeu': 'tình yêu', 'that long': 'thật lòng',
            'tim': 'tìm', 'mat do': 'mất đồ', 'o dau': 'ở đâu', 'that lac': 'thất lạc',
            'trom': 'trộm', 'mat cap': 'mất cắp', 'cho nao': 'chỗ nào',
            'mat vi': 'mất ví', 'de dau': 'để đâu', 'cat dau': 'cất đâu',
            'nha': 'nhà', 'xay nha': 'xây nhà', 'sua nha': 'sửa nhà',
            'can ho': 'căn hộ', 'chung cu': 'chung cư', 'phong thuy': 'phong thủy',
            'huong nha': 'hướng nhà', 'don nha': 'dọn nhà', 'chuyen nha': 'chuyển nhà',
            'dat': 'đất', 'lo dat': 'lô đất',
            've que': 'về quê', 'di xa': 'đi xa', 'du lich': 'du lịch',
            'xuat hanh': 'xuất hành', 'di choi': 'đi chơi', 'chuyen di': 'chuyến đi',
            'may bay': 'máy bay', 'di cong tac': 'đi công tác',
            'toi': 'tôi', 'bo': 'bố', 'me': 'mẹ', 'cha': 'cha',
            'ong ngoai': 'ông ngoại', 'ba ngoai': 'bà ngoại',
            'ong noi': 'ông nội', 'ba noi': 'bà nội', 'ong': 'ông', 'ba': 'bà',
            'con trai': 'con trai', 'con gai': 'con gái',
            'anh': 'anh', 'chi': 'chị', 'em': 'em',
            'doi tac': 'đối tác', 'khach hang': 'khách hàng',
            'qua duoc': 'qua được', 'chet chua': 'chết chưa',
            'con song': 'còn sống', 'da mat': 'đã mất', 'qua doi': 'qua đời',
            'co nen': 'có nên', 'co duoc': 'có được', 'co tot': 'có tốt',
            'co loi': 'có lợi', 'nhu the nao': 'như thế nào', 'the nao': 'thế nào',
            'bao gio': 'bao giờ', 'khi nao': 'khi nào', 'luc nao': 'lúc nào',
            'bao nhieu': 'bao nhiêu', 'may': 'mấy',
            'ban hang': 'bán hàng', 'loi nhuan': 'lợi nhuận',
            'bay gio': 'bây giờ', 'hien tai': 'hiện tại', 'sau nay': 'sau này',
            'nam nay': 'năm nay', 'thang nay': 'tháng này', 'tuan nay': 'tuần này',
            'sang nam': 'sang năm', 'nam sau': 'năm sau',
            # V36.1: Bổ sung từ search — câu hỏi phổ biến nhất
            # === TÌNH DUYÊN ===
            'tinh duyen': 'tình duyên', 'gia dao': 'gia đạo', 'luc duc': 'lục đục',
            'bat hoa': 'bất hòa', 'chan thanh': 'chân thành', 'that long': 'thật lòng',
            'lam an': 'làm ăn', 'thuan loi': 'thuận lợi', 'bat loi': 'bất lợi',
            'hanh phuc': 'hạnh phúc', 'ganh ghet': 'gắn kết', 'ket hon': 'kết hôn',
            'dan ong': 'đàn ông', 'dan ba': 'đàn bà', 'phu nu': 'phụ nữ',
            # === CÔNG DANH / HỌC TẬP ===
            'thi dau': 'thi đậu', 'thi do': 'thi đỗ', 'thi rot': 'thi rớt',
            'thi truot': 'thi trượt', 'tang luong': 'tăng lương',
            'thang tien': 'thăng tiến', 'thang chuc': 'thăng chức',
            'doi cong viec': 'đổi công việc', 'chuyen viec': 'chuyển việc',
            'phong van': 'phỏng vấn', 'nhan viec': 'nhận việc',
            'dai hoc': 'đại học', 'tot nghiep': 'tốt nghiệp',
            # === TÀI LỘC / KINH DOANH ===
            'thua lo': 'thua lỗ', 'thu hoi von': 'thu hồi vốn',
            'khai truong': 'khai trương', 'dong tho': 'động thổ',
            'hop tac': 'hợp tác', 'gop von': 'góp vốn', 'hun von': 'hùn vốn',
            'hoa hong': 'hoa hồng', 'doanh thu': 'doanh thu',
            'loi lai': 'lời lãi', 'thu loi': 'thu lời',
            # === SỨC KHỎE / SINH TỬ ===
            'hoi phuc': 'hồi phục', 'benh nang': 'bệnh nặng',
            'nguy kich': 'nguy kịch', 'hap hoi': 'hấp hối',
            'nam vien': 'nằm viện', 'nhap vien': 'nhập viện',
            'song sot': 'sống sót', 'tu vong': 'tử vong',
            'khoi benh': 'khỏi bệnh', 'chua benh': 'chữa bệnh',
            'suc khoe': 'sức khỏe', 'the luc': 'thể lực',
            # === KIỆN TỤNG / PHÁP LÝ ===
            'kien tung': 'kiện tụng', 'thua kien': 'thua kiện', 'thang kien': 'thắng kiện',
            'ra toa': 'ra tòa', 'tranh chap': 'tranh chấp', 'giai quyet': 'giải quyết',
            # === VẬN MỆNH / TỔNG QUÁT ===
            'van menh': 'vận mệnh', 'van han': 'vận hạn', 'may man': 'may mắn',
            'quy nhan': 'quý nhân', 'an toan': 'an toàn', 'nguy hiem': 'nguy hiểm',
            'tot': 'tốt', 'xau': 'xấu', 'hung': 'hung', 'cat': 'cát',
            'tuong lai': 'tương lai', 'dien bien': 'diễn biến',
            'tro ngai': 'trở ngại', 'kho khan': 'khó khăn',
            # === XUẤT HÀNH / DI CHUYỂN ===
            'di nuoc ngoai': 'đi nước ngoài', 'xuat ngoai': 'xuất ngoại',
            'dinh cu': 'định cư', 'di may bay': 'đi máy bay',
            'huong di': 'hướng đi', 'huong tot': 'hướng tốt',
            # === GIA ĐÌNH / NHÀ CỬA ===
            'sinh con': 'sinh con', 'co con': 'có con', 'con cai': 'con cái',
            'chia tai san': 'chia tài sản', 'thua ke': 'thừa kế',
            'xay nha': 'xây nhà', 'sua chua': 'sửa chữa', 'dong tho': 'động thổ',
        }
        
        # Tạo q_lower_normalized: thay thế ALL từ không dấu → có dấu
        q_normalized = q_lower
        # Sort by length descending → match cụm dài trước (VD: "nguoi yeu" trước "yeu")
        for _nd, _cd in sorted(_VN_NO_DIAC_MAP.items(), key=lambda x: len(x[0]), reverse=True):
            if _nd in q_normalized:
                q_normalized = q_normalized.replace(_nd, _cd)
        
        # Dùng q_normalized cho category detection thay vì q_lower
        q_lower = q_normalized

        CATEGORIES = {
            "SỨC_KHỎE_GIA_ĐÌNH": {
                "keywords": ["bệnh", "ốm", "đau", "sức khỏe", "khỏe", "chết", "mất người",
                             "gia đình", "thai", "mang thai", "bố mất", "mẹ mất", "chết chưa",
                             "sống", "chữa", "bệnh viện", "phẫu thuật", "ung thư", "tai nạn", "nguy hiểm",
                             "qua khỏi", "cứu được", "nằm viện", "thuốc", "trị bệnh", "khỏi bệnh"],
                "dung_than": "Bản Thân",
                "dung_than_detail": {"bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu", "cha": "Phụ Mẫu", "bố mẹ": "Phụ Mẫu",
                                     "ông ngoại": "Phụ Mẫu", "bà ngoại": "Phụ Mẫu", "ông nội": "Phụ Mẫu", "bà nội": "Phụ Mẫu",
                                     "ông": "Phụ Mẫu", "bà": "Phụ Mẫu",
                                     "con": "Tử Tôn", "con trai": "Tử Tôn", "con gái": "Tử Tôn",
                                     "vợ": "Thê Tài", "chồng": "Quan Quỷ",
                                     "anh": "Huynh Đệ", "chị": "Huynh Đệ", "em": "Huynh Đệ"},
                "label": "🏥 Sức Khỏe / Gia Đình",
                "hint": "Xem bệnh: DT = Hào Thế (Bản Thân). Quan Quỷ = bệnh tinh. Tử Tôn = thuốc/bác sĩ. Xem cho người khác → DT theo Lục Thân."
            },
            "TÀI_CHÍNH": {
                "keywords": ["tiền", "tài chính", "mua bán", "đầu tư", "giàu", "nghèo", "lương", "thu nhập", "nợ", 
                             "vay", "cho vay", "kinh doanh", "buôn bán", "lãi", "lỗ", "cổ phiếu", "crypto",
                             "bitcoin", "nhà đất", "mua nhà", "bất động sản", "vốn", "hùn vốn", "trúng số",
                             "tài sản", "vàng", "bạc", "kim cương", "trang sức", "lương tháng",
                             "bán hàng", "lợi nhuận", "doanh thu", "thu lời", "lời lãi", "hoa hồng",
                             "làm ăn", "khai trương", "góp vốn", "hợp tác", "thua lỗ", "thu hồi vốn"],
                "dung_than": "Thê Tài",
                "dung_than_detail": {},
                "label": "💰 Tài Chính / Tiền Bạc",
                "hint": "Phân tích tài chính. Thê Tài = tiền bạc. Sinh Môn/Mậu = cầu tài."
            },
            "CÔNG_VIỆC": {
                "keywords": ["việc", "công việc", "sếp", "thăng tiến", "thăng chức", "thi", "đỗ", "trượt", "phỏng vấn",
                             "xin việc", "nghỉ việc", "sa thải", "hợp đồng", "dự án", "thầu", "đấu thầu",
                             "kiện", "kiện tụng", "tòa", "quan chức", "chức vụ", "đề bạt",
                             "du học", "học hành", "thi cử", "đại học", "đi làm", "chức", "sự nghiệp",
                             "khởi nghiệp", "startup", "bổ nhiệm", "chuyển công tác",
                             "sản xuất", "phát triển", "thụt lùi", "công ty", "nhà máy", "xưởng",
                             "doanh nghiệp", "cơ sở", "kinh doanh", "mở rộng", "phá sản"],
                "dung_than": "Quan Quỷ",
                "dung_than_detail": {"con trai": "Tử Tôn", "con gái": "Tử Tôn", "con": "Tử Tôn",
                                     "vợ": "Thê Tài", "chồng": "Quan Quỷ",
                                     "bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu"},
                "label": "💼 Công Việc / Sự Nghiệp / Thi Cử",
                "hint": "Phân tích công việc, thi cử. Quan Quỷ = sếp/cơ quan. Khai Môn = khởi đầu."
            },
            "TÌNH_CẢM": {
                "keywords": ["yêu", "người yêu", "vợ", "chồng", "hôn nhân", "cưới", "ly hôn", "tình", 
                             "hẹn hò", "chia tay", "ngoại tình", "duyên", "vợ chồng", "đám cưới",
                             "bạn trai", "bạn gái", "tình cảm", "hạnh phúc", "ghen",
                             "lấy vợ", "lấy chồng", "kết hôn", "thật lòng", "tình yêu", "hôn"],
                "dung_than": "Thê Tài",
                "dung_than_detail": {"vợ chồng": "Thê Tài", "vợ": "Thê Tài", "chồng": "Quan Quỷ", 
                                     "bạn gái": "Thê Tài", "bạn trai": "Quan Quỷ"},
                "label": "❤️ Tình Cảm / Hôn Nhân",
                "hint": "Phân tích tình cảm. Thê Tài = vợ/bạn gái. Quan Quỷ = chồng/bạn trai. Ứng hào = đối phương."
            },
            "TÌM_ĐỒ": {
                "keywords": ["tìm", "mất đồ", "ở đâu", "thất lạc", "trộm", "mất cắp", "chỗ nào",
                             "mất xe", "mất điện thoại", "mất tiền", "tìm đường", "lạc đường",
                             "mất ví", "mất đồ", "giấy tờ", "để đâu", "cất đâu"],
                "dung_than": "Thê Tài",
                "dung_than_detail": {},
                "label": "🔍 Tìm Đồ / Tìm Người",
                "hint": "Phân tích hướng tìm. Dùng 9 cung Kỳ Môn → hướng. Cảnh Môn = đồ điện tử."
            },
            "NHÀ_CỬA": {
                "keywords": ["nhà", "tầng", "phòng", "căn hộ", "chung cư", "xây nhà", "sửa nhà", 
                             "nhà tôi", "nhà mấy", "phong thủy", "hướng nhà", "cửa nhà",
                             "dọn nhà", "chuyển nhà", "đất", "thửa đất", "lô đất"],
                "dung_than": "Phụ Mẫu",
                "dung_than_detail": {"tăng giá": "Thê Tài", "giá nhà": "Thê Tài", "bán nhà": "Thê Tài",
                                     "mua nhà": "Thê Tài", "tiền nhà": "Thê Tài", "bán": "Thê Tài",
                                     "bao nhiêu": "Thê Tài", "giá bao": "Thê Tài",
                                     "phong thủy": "Phụ Mẫu", "sửa nhà": "Phụ Mẫu"},
                "label": "🏠 Nhà Cửa / Bất Động Sản",
                "hint": "Phân tích nhà cửa. Phụ Mẫu = nhà/giấy tờ. Thê Tài = giá tiền/mua bán."
            },
            "XUẤT_HÀNH": {
                "keywords": ["về quê", "đi xa", "du lịch", "xuất hành", "đi chơi", "chuyến đi",
                             "di chuyển", "đi bay", "máy bay", "đi tàu", "đi xe", "đi công tác",
                             "ra nước ngoài", "đi nước ngoài", "đi đâu", "đi xa", "lên đường",
                             "khởi hành", "hành trình", "đi về"],
                "dung_than": "Bản Thân",
                "dung_than_detail": {},
                "label": "✈️ Xuất Hành / Di Chuyển",
                "hint": "Phân tích xuất hành. Cửa Khai/Hưu/Sinh=NÊN ĐI. Tử/Kinh=KHÔNG. Dịch Mã=DI CHUYỂN."
            },
            "THẮNG_THUA": {
                "keywords": ["thắng", "thua", "đội nào", "ai thắng", "ai thua", "bên nào",
                             "bóng đá", "trận đấu", "giải đấu", "thi đấu", "đối kháng",
                             "cạnh tranh", "vô địch", "hòa", "tỷ số", "kết quả trận",
                             "thắng thua", "tranh tài", "đấu", "gặp", "vs"],
                "dung_than": "Bản Thân",
                "dung_than_detail": {},
                "label": "⚔️ Thắng Thua / Đối Kháng",
                "hint": "Phân tích thắng thua dựa trên Thế vs Ứng (Lục Hào), Chủ vs Khách (Kỳ Môn), Thể vs Dụng (Mai Hoa). Thế = bên chủ/bên hỏi. Ứng = đối phương."
            },
            "CHUNG": {
                "keywords": ["vận mệnh", "năm nay", "tháng này", "an toàn", "quý nhân", "may mắn",
                             "tuổi", "bao nhiêu tuổi", "mấy tuổi"],
                "dung_than": "Bản Thân",
                "dung_than_detail": {"vợ": "Thê Tài", "chồng": "Quan Quỷ", "bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu",
                                     "con": "Tử Tôn", "anh": "Huynh Đệ", "chị": "Huynh Đệ"},
                "label": "❓ Tổng Quát",
                "hint": "Phân tích tổng quát dựa trên ngũ hành sinh khắc và tổng hợp 6 phương pháp."
            }
        }
        
        # V21.0: Phân loại thông minh — SỬA LỖI BONUS has_person
        detected_category = "CHUNG"
        max_score = 0
        
        # V21.0: Phát hiện context trước — tránh nhầm "bố" thành SỨC_KHỎE khi hỏi TÌNH CẢM/CÔNG VIỆC
        sk_only_keywords = ["bệnh", "ốm", "đau", "chết", "sống", "chữa", "viện", "phẫu", "ung thư", 
                            "tai nạn", "qua khỏi", "khỏe", "thuốc", "mất người"]
        has_sk_context = any(kw in q_lower for kw in sk_only_keywords)
        
        for cat_key, cat_info in CATEGORIES.items():
            if cat_key == "CHUNG":
                # CHUNG: chỉ match nếu không category nào khác match
                score = 0
                for kw in cat_info["keywords"]:
                    if kw in q_lower:
                        score += len(kw)
                if score > max_score:
                    max_score = score
                    detected_category = cat_key
                continue
            
            score = 0
            for kw in cat_info["keywords"]:
                if kw in q_lower:
                    score += len(kw)
            
            # V21.0: TÌM ĐỒ penalty khi có người (chỉ khi KHÔNG hỏi ở đâu)
            nguoi_keywords = ["bố", "mẹ", "cha", "ông", "bà", "con trai", "con gái", "vợ", "chồng"]
            has_person = any(nk in q_lower for nk in nguoi_keywords)
            
            if cat_key == "TÌM_ĐỒ" and has_person:
                if "ở đâu" not in q_lower and "chỗ nào" not in q_lower and "hướng" not in q_lower:
                    score = 0
            
            # V21.0: SỨC_KHỎE chỉ bonus khi CÓ từ khóa sức khỏe thực sự
            if cat_key == "SỨC_KHỎE_GIA_ĐÌNH" and has_person and has_sk_context:
                score += 5
            
            if score > max_score:
                max_score = score
                detected_category = cat_key
        
        cat_data = CATEGORIES[detected_category]
        
        # ═══ V35.8: PERSON + TOPIC → DT (100% accuracy) ═══
        # Bước 1: Detect PERSON (ai được hỏi) — dùng word boundary
        PERSON_DT_MAP = {
            "ông ngoại": "Phụ Mẫu", "bà ngoại": "Phụ Mẫu",
            "ông nội": "Phụ Mẫu", "bà nội": "Phụ Mẫu",
            "bố mẹ": "Phụ Mẫu", "cha mẹ": "Phụ Mẫu", "vợ chồng": "Thê Tài",
            "anh chị em": "Huynh Đệ", "anh em": "Huynh Đệ",
            "con trai": "Tử Tôn", "con gái": "Tử Tôn", "con dâu": "Tử Tôn", "con rể": "Tử Tôn",
            "em gái": "Huynh Đệ", "em trai": "Huynh Đệ",
            "bạn gái": "Thê Tài", "bạn trai": "Quan Quỷ", "người yêu": "Thê Tài",
            "bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu", "cha": "Phụ Mẫu",
            "ông": "Phụ Mẫu", "bà": "Phụ Mẫu",
            "con": "Tử Tôn", "vợ": "Thê Tài", "chồng": "Quan Quỷ",
            "anh": "Huynh Đệ", "chị": "Huynh Đệ", "em": "Huynh Đệ",
            "sếp": "Quan Quỷ", "đối tác": "Quan Quỷ", "khách hàng": "Quan Quỷ",
        }
        import re as _re_person
        _person_items = sorted(PERSON_DT_MAP.items(), key=lambda x: len(x[0]), reverse=True)
        _detected_person = None
        _person_dt = None
        for _pk, _pd in _person_items:
            _pat = r'(?:^|[\s,;.!?])' + _re_person.escape(_pk) + r'(?:[\s,;.!?]|$)'
            if _re_person.search(_pat, q_lower):
                _detected_person = _pk
                _person_dt = _pd
                break
        
        # Bước 2: Gán DT
        if _person_dt:
            dung_than = _person_dt
        elif 'tôi' in q_lower and detected_category in ('CHUNG', 'SỨC_KHỎE_GIA_ĐÌNH'):
            # "tôi" = Bản Thân CHỈ khi hỏi CHUNG hoặc SỨC_KHỎE (hào Thế)
            # TÀI_CHÍNH "tôi giàu?" → DT = Thê Tài, CÔNG_VIỆC → Quan Quỷ
            dung_than = 'Bản Thân'
        else:
            dung_than = cat_data["dung_than"]
        
        # Bước 3: Topic overrides (đặc biệt)
        # NHÀ_CỬA không có person → check bán/mua/giá → Thê Tài
        if detected_category == "NHÀ_CỬA" and not _detected_person:
            _nha_tt_kw = ['tăng giá', 'giá nhà', 'bán nhà', 'mua nhà', 'tiền nhà',
                          'bán', 'bao nhiêu', 'giá bao', 'mua']
            for _nk in sorted(_nha_tt_kw, key=len, reverse=True):
                if _nk in q_lower:
                    dung_than = 'Thê Tài'
                    break
        
        # CHUNG: khi không detect person → giữ default = Bản Thân (hào Thế)
        # (Không override sang Quan Quỷ nữa — hỏi chung = hỏi cho mình)
        
        # XUẤT_HÀNH → luôn Bản Thân
        if detected_category == "XUẤT_HÀNH":
            dung_than = "Bản Thân"
        
        # TÌM_ĐỒ → luôn Thê Tài
        if detected_category == "TÌM_ĐỒ":
            dung_than = "Thê Tài"
        
        # Anh chị em override (mạnh nhất)
        if any(kw in q_lower for kw in ['anh chị em', 'anh em', 'mấy anh', 'mấy chị', 'bao nhiêu anh']):
            dung_than = 'Huynh Đệ'
            
        # V35.8: Dropdown CHỈ override khi user chủ động chọn (không phải default "Bản thân")
        # Default "👤 Bản thân" → để V35.8 PERSON+TOPIC tự detect
        _DROPDOWN_DEFAULTS = {"Không Rõ", "👤 Bản thân", "Bản thân", "Bản Thân", ""}
        if selected_subject and selected_subject not in _DROPDOWN_DEFAULTS:
            # User chủ động chọn: "👴👵 Bố mẹ", "👶 Con cái", etc.
            _DROPDOWN_DT_MAP = {
                "👨‍👩‍👧 Anh chị em": "Huynh Đệ",
                "👴👵 Bố mẹ": "Phụ Mẫu",
                "👶 Con cái": "Tử Tôn",
                "🤝 Người lạ (theo Can sinh)": "Quan Quỷ",
            }
            dung_than = _DROPDOWN_DT_MAP.get(selected_subject, dung_than)
        
        is_age = _is_age_question(question)
        is_find = _is_find_question(question) and detected_category == "TÌM_ĐỒ"
        is_yesno = _is_yesno_question(question)
        is_count = _is_count_question(question)
        is_competition = _is_competition_question(question) or detected_category == "THẮNG_THUA"
        
        # V42.3: Nếu là competition → force DT = Bản Thân (Thế = bên chủ)
        if is_competition:
            dung_than = 'Bản Thân'
            detected_category = 'THẮNG_THUA'
        
        # V8.2: Nếu topic được truyền từ dropdown → vẫn match topic cũ
        # Nếu topic=None (Q&A tự do) → dùng smart category
        if topic:
            matched_topic, topic_data = _match_topic(question, topic)
        else:
            matched_topic, topic_data = None, None
        
        sections = []
        sections.append(f"## 🔮 THIÊN CƠ ĐẠI SƯ — V42.9 Phân Tích Thống Nhất\n")
        sections.append(f"**Câu hỏi:** {question}\n")
        
        # ═══════════════════════════════════════════════════
        # V32.5: PHÂN TÁCH + NGỮ PHÁP CÂU HỎI (Grammar-based DT)
        # ═══════════════════════════════════════════════════
        v31_parsed_questions = []
        v31_primary = None  # Câu hỏi chính (dùng để xác định DT)
        category_label = cat_data['label']
        
        try:
            v31_parsed_questions = v32_parse_question(question)
            if v31_parsed_questions and len(v31_parsed_questions) >= 1:
                v31_primary = v31_parsed_questions[0]
                
                # V35.8: Grammar parser info (chỉ hiển thị, KHÔNG override DT)
                # DT đã được xác định chính xác ở V35.8 PERSON+TOPIC logic
                parser_dt = v31_primary.get('dung_than')
                focus = v31_primary.get('inquiry_focus', '')
                purpose = v31_primary.get('ask_purpose', 'CHO')
                reason = v31_primary.get('dung_than_reason', '')
                if parser_dt:
                    self.log_step("V32.5 Grammar", "INFO", 
                                  f"Parser suggest: {parser_dt} | V35.8 final: {dung_than} | {reason[:60]}")
                
                # Hiển thị bảng phân tách
                if len(v31_parsed_questions) > 1:
                    parsed_table = format_parsed_questions_v2(v31_parsed_questions)
                    if parsed_table:
                        sections.append(parsed_table)
                        sections.append("")
                elif len(v31_parsed_questions) == 1:
                    pq = v31_parsed_questions[0]
                    focus = pq.get('inquiry_focus', pq.get('person', 'Bản thân'))
                    purpose = pq.get('ask_purpose', '?')
                    person_info = f" | Hỏi {purpose}: **{focus}**" if focus else ""
                    dt_reason = pq.get('dung_than_reason', '')
                    sections.append(f"📋 **Phân loại:** {pq['qtype_label']} — {pq['topic_label']}{person_info} — DT: {pq['dung_than']} — SĐ: {pq['diagram_id']}")
                    if dt_reason:
                        sections.append(f"└─ *{dt_reason[:100]}*")
                    sections.append("")
        except Exception as e:
            self.log_step("V32.5 Grammar", "ERROR", str(e)[:80])
        
        # BƯỚC 1: DỤNG THẦN & CHỦ ĐỀ
        sections.append(f"### BƯỚC 1 — DỤNG THẦN & CHỦ ĐỀ")
        if matched_topic:
            source_tag = " 🧠(Đã học)" if topic_data.get('_source') == 'learned' else ""
            sections.append(f"- 📌 **Chủ đề phù hợp:** {matched_topic}{source_tag}")
            dt_list = topic_data.get("Dụng_Thần", [])
            if dt_list:
                sections.append(f"- **Dụng Thần (theo chủ đề):** {', '.join(dt_list)}")
                for dt in dt_list:
                    dt_info = KY_MON_DATA.get('DU_LIEU_DUNG_THAN_PHU_TRO', {}).get('BAT_MON', {}).get(dt, {})
                    if dt_info:
                        sections.append(f"  → **{dt}**: {dt_info.get('Luận_Đoán', '')}")
            hint = topic_data.get("Luận_Giải_Gợi_Ý", "")
            if hint:
                sections.append(f"- **💡 Hướng dẫn phân tích:** {hint}")
        else:
            # V8.2 SMART CATEGORY — phân loại tự động
            sections.append(f"- 🧠 **Nhóm câu hỏi:** {cat_data['label']}")
            sections.append(f"- 🎯 **Dụng Thần:** {dung_than}")
            sections.append(f"- 💡 **Hướng phân tích:** {cat_data['hint']}")
        
        # V8.0: Hiển thị loại câu hỏi
        q_types = []
        if is_age: q_types.append("Đếm tuổi")
        if is_find: q_types.append("Tìm đồ")
        if is_yesno: q_types.append("Có/Không")
        if is_count: q_types.append("Đếm số lượng")
        if q_types:
            sections.append(f"- 🎯 **Loại câu hỏi:** {', '.join(q_types)}")
            if is_count:
                sections.append(f"- 📊 **Phương pháp đếm số:** Quái Tiên Thiên (Kỳ Môn) + Đếm Hào (Lục Hào) + Tỷ Hòa (Mai Hoa)")
        
        sections.append(f"- **Dụng Thần (Ngũ Hành):** {dung_than}")
        if topic and topic != matched_topic:
            sections.append(f"- Chủ đề gốc: **{topic}**")
        sections.append("")
        
        ky_mon_verdict = "BÌNH"
        ky_mon_reason = ""
        luc_hao_verdict = "BÌNH"
        luc_hao_reason = ""
        mai_hoa_verdict = "BÌNH"
        mai_hoa_reason = ""
        luc_nham_verdict = "BÌNH"
        luc_nham_reason = ""
        thai_at_verdict = "BÌNH"
        thai_at_reason = ""
        age_numbers = []
        count_numbers = []  # V8.0: dùng cho đếm số
        
        # BƯỚC 2-5: Wrap trong <details> để collapse (V11.0)
        sections.append("\n<details>")
        sections.append("<summary><b>🔍 XEM CHI TIẾT PHÂN TÍCH 5 PHƯƠNG PHÁP (nhấn để mở)</b></summary>\n")
        
        # BƯỚC 2: KỲ MÔN
        sections.append(f"### BƯỚC 2 — KỲ MÔN ĐỘN GIÁP")
        if chart_data and isinstance(chart_data, dict):
            ky_mon_section, ky_mon_verdict, km_age, km_reason, km_count = self._analyze_ky_mon(chart_data, dung_than, is_age, is_find, is_count, question)
            sections.append(ky_mon_section)
            ky_mon_reason = km_reason
            if km_age:
                age_numbers.append(("Kỳ Môn", km_age))
            if km_count is not None:
                count_numbers.append(("Kỳ Môn", km_count))
        else:
            sections.append("- Chưa có dữ liệu Kỳ Môn.\n")
        
        # BƯỚC 3: LỤC HÀO
        sections.append(f"### BƯỚC 3 — LỤC HÀO KINH DỊCH")
        if luc_hao_data and isinstance(luc_hao_data, dict):
            lh_section, luc_hao_verdict, lh_age, lh_reason, lh_count = self._analyze_luc_hao_full(luc_hao_data, dung_than, is_age, is_count)
            sections.append(lh_section)
            luc_hao_reason = lh_reason
            if lh_age:
                age_numbers.append(("Lục Hào", lh_age))
            if lh_count is not None:
                count_numbers.append(("Lục Hào", lh_count))
        else:
            sections.append("- Chưa có dữ liệu Lục Hào.\n")
        
        # BƯỚC 4: MAI HOA
        sections.append(f"### BƯỚC 4 — MAI HOA DỊCH SỐ")
        if mai_hoa_data and isinstance(mai_hoa_data, dict):
            mh_section, mai_hoa_verdict, mh_age = self._analyze_mai_hoa_full(mai_hoa_data, is_age)
            sections.append(mh_section)
            # V8.0: Extract reason from MAI HOA verdict line
            mai_hoa_reason = ""
            for ln in mh_section.split('\n'):
                if 'MAI HOA:' in ln:
                    mai_hoa_reason = ln.split('(')[-1].rstrip(')').strip() if '(' in ln else ''
            if mh_age:
                age_numbers.append(("Mai Hoa", mh_age))
        else:
            sections.append("- Chưa có dữ liệu Mai Hoa.\n")
        
        # BƯỚC 5: THIẾT BẢN + KINH DỊCH + VẠN VẬT LOẠI TƯỢNG
        sections.append(f"### BƯỚC 5 — THIẾT BẢN + KINH DỊCH + VẠN VẬT")
        tb_section = self._analyze_thiet_ban_kinh_dich_van_vat(question, chart_data, luc_hao_data, mai_hoa_data)
        sections.append(tb_section)
        
        # ========================================
        # V14.0: BƯỚC 5.5 — ĐẠI LỤC NHÂM (大六壬)
        # ========================================
        sections.append(f"### BƯỚC 5.5 — ĐẠI LỤC NHÂM (大六壬)")
        try:
            from dai_luc_nham import tinh_dai_luc_nham, phan_tich_chuyen_sau
            if chart_data and isinstance(chart_data, dict) and chart_data.get('can_ngay'):
                ln_data = tinh_dai_luc_nham(
                    chart_data.get('can_ngay', 'Giáp'),
                    chart_data.get('chi_ngay', 'Tý'),
                    chart_data.get('chi_gio', 'Ngọ'),
                    chart_data.get('tiet_khi', 'Đông Chí')
                )
                # Xác định topic cho Lục Nhâm từ category
                ln_topic = 'chung'
                if detected_category == 'TÀI_CHÍNH': ln_topic = 'tai_chinh'
                elif detected_category == 'CÔNG_VIỆC': ln_topic = 'cong_viec'
                elif detected_category == 'SỨC_KHỎE_GIA_ĐÌNH': ln_topic = 'suc_khoe'
                elif detected_category == 'TÌNH_CẢM': ln_topic = 'tinh_cam'
                elif detected_category == 'TÌM_ĐỒ': ln_topic = 'tim_do'
                
                ln_deep = phan_tich_chuyen_sau(ln_data, question, ln_topic)
                luc_nham_verdict = ln_deep.get('verdict', 'BÌNH')
                
                # Build section content
                ln_lines = []
                tam_truyen = ln_data.get('tam_truyen', {})
                if tam_truyen:
                    ln_lines.append(f"- **Sơ Truyền (Quá khứ):** {tam_truyen.get('so_truyen', '?')} ({tam_truyen.get('so_truyen_hanh', '?')})")
                    ln_lines.append(f"- **Trung Truyền (Hiện tại):** {tam_truyen.get('trung_truyen', '?')} ({tam_truyen.get('trung_truyen_hanh', '?')})")
                    ln_lines.append(f"- **Mạt Truyền (Tương lai):** {tam_truyen.get('mat_truyen', '?')} ({tam_truyen.get('mat_truyen_hanh', '?')})")
                
                # Chi tiết từ phan_tich_chuyen_sau
                for d in ln_deep.get('details', [])[:8]:
                    ln_lines.append(f"- {d}")
                
                # Dụng Thần
                if ln_deep.get('dung_than_found'):
                    ln_lines.append(f"- ✅ Dụng Thần HIỆN trong Tứ Khóa")
                else:
                    ln_lines.append(f"- ❌ Dụng Thần KHÔNG hiện trong Tứ Khóa → sự việc khó thành")
                
                # Tuần Không
                tuan_khong = ln_deep.get('tuan_khong', [])
                if tuan_khong:
                    ln_lines.append(f"- Tuần Không: {', '.join(tuan_khong)}")
                
                luc_nham_reason = f"Mạt Truyền {tam_truyen.get('mat_truyen', '?')} ({tam_truyen.get('mat_truyen_hanh', '?')})" if tam_truyen else ''
                ln_lines.append(f"\n→ **ĐẠI LỤC NHÂM: {luc_nham_verdict}** ({luc_nham_reason})")
                sections.append("\n".join(ln_lines))
            else:
                sections.append("- Chưa có đủ dữ liệu Can/Chi để tính Đại Lục Nhâm.\n")
        except Exception as e:
            sections.append(f"- ⚠️ Lỗi tính Đại Lục Nhâm: {str(e)[:80]}\n")
        
        # ========================================
        # V14.0: BƯỚC 5.6 — THÁI ẤT THẦN SỐ (太乙神数)
        # ========================================
        sections.append(f"### BƯỚC 5.6 — THÁI ẤT THẦN SỐ (太乙神数)")
        try:
            from thai_at_than_so import tinh_thai_at_than_so
            import datetime as _dt
            now = _dt.datetime.now()
            ta_can_ngay = chart_data.get('can_ngay', 'Giáp') if chart_data else 'Giáp'
            ta_chi_ngay = chart_data.get('chi_ngay', 'Tý') if chart_data else 'Tý'
            ta_data = tinh_thai_at_than_so(now.year, now.month, ta_can_ngay, ta_chi_ngay)
            
            ta_lines = []
            ta_cung = ta_data.get('thai_at_cung', {})
            ta_lines.append(f"- **Thái Ất:** Cung {ta_cung.get('cung', '?')} ({ta_cung.get('ten_cung', '?')}) — {ta_cung.get('hanh_cung', '?')} — {ta_cung.get('ly', '?')}")
            ta_lines.append(f"- **Tích Niên:** {ta_data.get('tich_nien', '?')}")
            
            # Bát Tướng
            bat_tuong = ta_data.get('bat_tuong', {})
            if bat_tuong:
                ta_lines.append(f"- **Bát Tướng:**")
                for bt_name, bt_info in list(bat_tuong.items())[:4]:  # Hiện 4 tướng chính
                    ta_lines.append(f"  - {bt_name}: Cung {bt_info.get('cung', '?')} ({bt_info.get('ten_cung', '?')}) — {bt_info.get('cat_hung', '?')}")
            
            # Luận Giải
            luan_giai = ta_data.get('luan_giai', {})
            for d in luan_giai.get('details', [])[:6]:
                ta_lines.append(f"- {d}")
            
            thai_at_verdict = luan_giai.get('verdict', 'BÌNH')
            
            # Cách Cục
            cach_cuc = ta_data.get('cach_cuc', [])
            if cach_cuc:
                for cc in cach_cuc[:3]:
                    ta_lines.append(f"- {cc}")
            
            thai_at_reason = f"Cung {ta_cung.get('cung', '?')} ({ta_cung.get('ten_cung', '?')}), {ta_cung.get('hanh_cung', '?')}"
            ta_lines.append(f"\n→ **THÁI ẤT THẦN SỐ: {thai_at_verdict}** ({thai_at_reason})")
            sections.append("\n".join(ta_lines))
        except Exception as e:
            sections.append(f"- ⚠️ Lỗi tính Thái Ất Thần Số: {str(e)[:80]}\n")
        
        # Đóng </details>
        sections.append("\n</details>\n")
        
        # V21.0: SCORING METHODS — tính trước khi BƯỚC 6 dùng
        v16_lh_score_str = ''
        v16_mh_score_str = ''
        v16_tb_score_str = ''
        v16_ln_score_str = ''
        v16_ta_score_str = ''
        v16_km_raw = 0
        v16_lh_raw = 0
        v16_mh_raw = 0
        v16_tb_raw = 0
        v16_ln_raw = 0
        v16_ta_raw = 0
        v23_lh_factors = []  # V26.2: Lưu toàn bộ factors chi tiết
        v24_km_factors = []
        v24_mh_factors = []
        v24_tb_factors = []
        v24_ln_factors = []
        v24_ta_factors = []
        
        try:
            km_s, km_sum, v24_km_factors = self._ky_mon_scoring(chart_data, dung_than)
            v16_km_raw = km_s
            # Override km_verdict_to_score from raw calculation
        except Exception:
            pass
            
        try:
            lh_s, lh_sum, v23_lh_factors = self._luc_hao_scoring(luc_hao_data, dung_than)
            v16_lh_score_str = lh_sum
            v16_lh_raw = lh_s
        except Exception:
            pass
        try:
            mh_s, mh_sum, v24_mh_factors = self._mai_hoa_scoring(mai_hoa_data, chart_data)
            v16_mh_score_str = mh_sum
            v16_mh_raw = mh_s
        except Exception:
            pass
        try:
            tb_s, tb_sum, v24_tb_factors = self._thiet_ban_scoring(chart_data, luc_hao_data, mai_hoa_data)
            v16_tb_score_str = tb_sum
            v16_tb_raw = tb_s
        except Exception:
            pass
        try:
            ln_s, ln_sum, v24_ln_factors = self._luc_nham_scoring(chart_data)
            v16_ln_score_str = ln_sum
            v16_ln_raw = ln_s
        except Exception:
            pass
        try:
            ta_s, ta_sum, v24_ta_factors = self._thai_at_scoring(chart_data)
            v16_ta_score_str = ta_sum
            v16_ta_raw = ta_s
        except Exception:
            pass
        
        # V21.0 BƯỚC 6: TỔNG HỢP + WEIGHTED SCORING — 5 PHƯƠNG PHÁP
        sections.append(f"### ĐỐI CHIẾU MỌI PHƯƠNG PHÁP")
        verdicts = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict, luc_nham_verdict, thai_at_verdict]
        reasons = [ky_mon_reason, luc_hao_reason, mai_hoa_reason, luc_nham_reason, thai_at_reason]
        
        # V21.0: Normalize raw scores → 0-100% per method
        # KM đã có score thực nên không lấy từ estimation nữa
        if v16_km_raw == 0:
            km_verdict_to_score = {'ĐẠI CÁT': 25, 'CÁT': 15, 'BÌNH': 0, 'HUNG': -15, 'ĐẠI HUNG': -25}
            v16_km_raw = km_verdict_to_score.get(ky_mon_verdict, 0)
        
        raw_scores = {
            'KM': v16_km_raw,
            'LH': v16_lh_raw,
            'MH': v16_mh_raw,
            'TB': v16_tb_raw,
            'LN': v16_ln_raw,
            'TA': v16_ta_raw,
        }
        # Normalize: map [-40,+40] → [0,100]
        def _norm_score(s, scale=40):
            return max(0, min(100, int(50 + (s / scale) * 50)))
        
        norm_scores = {k: _norm_score(v) for k, v in raw_scores.items()}
        
        # V32.7c: WEIGHTED AVERAGE — dùng METHOD_STRENGTH_MAP (research-backed)
        # detected_category = key từ CATEGORIES (VD: 'TÀI_CHÍNH', 'TÌM_ĐỒ', 'CÔNG_VIỆC')
        _CAT_TO_STRENGTH_DIRECT = {
            'TÀI_CHÍNH': 'tài_chính', 'CÔNG_VIỆC': 'sự_nghiệp',
            'TÌNH_CẢM': 'tình_cảm', 'SỨC_KHỎE_GIA_ĐÌNH': 'sức_khỏe',
            'TÌM_ĐỒ': 'tìm_đồ', 'CHUNG': 'tổng_quát',
        }
        strength_key_w = _CAT_TO_STRENGTH_DIRECT.get(detected_category, CATEGORY_TO_STRENGTH.get(detected_category, 'tổng_quát'))
        method_w = METHOD_STRENGTH_MAP.get(strength_key_w, METHOD_STRENGTH_MAP.get('tổng_quát', {}))
        weights = {
            'KM': method_w.get('ky_mon', 55),
            'LH': method_w.get('luc_hao', 100),
            'MH': method_w.get('mai_hoa', 70),
            'TB': method_w.get('thiet_ban', 40),
            'LN': method_w.get('luc_nham', 50),
            'TA': method_w.get('thai_at', 35),
        }
        
        weighted_pct = sum(norm_scores[k] * weights[k] for k in norm_scores) / sum(weights.values())
        weighted_pct = max(5, min(95, int(weighted_pct)))
        
        # V21.0: 12 Trường Sinh bonus/penalty
        ts_bonus = 0
        ts_stage = None
        if chart_data and isinstance(chart_data, dict):
            can_dt = chart_data.get('can_ngay', '')
            chi_dt = chart_data.get('chi_ngay', '')
            hanh_dt = CAN_NGU_HANH.get(can_dt, '')
            if hanh_dt and chi_dt:
                ts_stage, _ = _get_truong_sinh(hanh_dt, chi_dt)
                if ts_stage:
                    ts_power = TRUONG_SINH_POWER.get(ts_stage, {}).get('power', 50)
                    ts_bonus = int((ts_power - 50) * 0.15)  # ±7.5 max
        weighted_pct = max(5, min(95, weighted_pct + ts_bonus))
        
        sections.append(f"| Phương pháp | Kết luận | Điểm | % | Trọng số |")
        sections.append(f"|---|---|---|---|---|")
        pp_names = ['Kỳ Môn', 'Lục Hào', 'Mai Hoa', 'Thiết Bản', 'Đại Lục Nhâm', 'Thái Ất']
        pp_keys = ['KM', 'LH', 'MH', 'TB', 'LN', 'TA']
        for i, (pp_name, pp_key) in enumerate(zip(pp_names, pp_keys)):
            v = verdicts[i] if i < len(verdicts) else 'BÌNH'
            r = reasons[i] if i < len(reasons) else ''
            r_short = r[:60] if isinstance(r, str) else ''
            ns = norm_scores.get(pp_key, 50)
            w = weights.get(pp_key, 10)
            sections.append(f"| {pp_name} | **{v}** | {raw_scores.get(pp_key, 0):+d} | {ns}% | {w}% |")
        sections.append(f"\n**📊 ĐIỂM TỔNG HỢP: {weighted_pct}%** (có tính 12 Trường Sinh: {ts_bonus:+d}%)")
        
        # ═══════════════════════════════════════════════════════
        # V26.2: BƯỚC 5.7 — LƯỢNG HÓA LỰC LƯỢNG 3 TẦNG (LỰC LƯỢNG THỐNG NHẤT)
        # V32.3: Auto-detect Hành DT từ thời gian khi không có chart_data
        # ═══════════════════════════════════════════════════════
        hanh_dt_v22 = ''
        cung_bt_hanh_v22 = ''
        ngu_khi_state_v22 = 'Hưu'
        ngu_khi_pwr_v22 = 50
        unified_v22 = None
        
        # V32.3: Nếu không có chart_data → tự tính từ thời gian hiện tại
        if not chart_data or not isinstance(chart_data, dict):
            try:
                import datetime
                now = datetime.datetime.now()
                # Tính Can giờ hiện tại (đơn giản) → Hành DT
                can_idx = (now.year % 10)
                chi_idx = (now.hour // 2) % 12
                _auto_cans = ['Canh', 'Tân', 'Nhâm', 'Quý', 'Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ']
                _auto_can = _auto_cans[can_idx]
                hanh_dt_v22 = CAN_NGU_HANH.get(_auto_can, 'Thổ')
                
                # Tính 12 Trường Sinh từ Chi giờ
                _auto_chis = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
                _auto_chi = _auto_chis[chi_idx]
                cung_bt_hanh_v22 = CHI_NGU_HANH.get(_auto_chi, 'Thổ')
                
                ngu_khi_state_v22, ngu_khi_pwr_v22 = _calc_ngu_khi(hanh_dt_v22, cung_bt_hanh_v22)
                
                # Tính Trường Sinh từ thời gian
                if not ts_stage:
                    _ts_stages = ['Trường Sinh', 'Mộc Dục', 'Quan Đới', 'Lâm Quan', 'Đế Vượng', 'Suy',
                                  'Bệnh', 'Tử', 'Mộ', 'Tuyệt', 'Thai', 'Dưỡng']
                    ts_stage = _ts_stages[chi_idx]
                
                self.log_step("V32.3 AutoDetect", "OK", f"Hành={hanh_dt_v22}, Chi={_auto_chi}, TS={ts_stage}")
            except Exception as e:
                hanh_dt_v22 = 'Thổ'
                self.log_step("V32.3 AutoDetect", "FALLBACK", str(e)[:60])

        if chart_data and isinstance(chart_data, dict):
            # V35.8: Tính Hành DT từ Can Ngày + Dụng Thần (Lục Hào Ngũ Hành)
            # Can Ngày → Hành bản thân, rồi map DT → Hành theo sinh khắc
            _hanh_ban_than = CAN_NGU_HANH.get(chart_data.get('can_ngay', ''), 'Thổ')
            
            # LỤC HÀO NGŨ HÀNH MAPPING: self_hanh → {DT → hanh_DT}
            _DT_HANH = {
                'Mộc': {'Bản Thân': 'Mộc', 'Huynh Đệ': 'Mộc', 'Phụ Mẫu': 'Thủy', 'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa'},
                'Hỏa': {'Bản Thân': 'Hỏa', 'Huynh Đệ': 'Hỏa', 'Phụ Mẫu': 'Mộc', 'Quan Quỷ': 'Thủy', 'Thê Tài': 'Kim', 'Tử Tôn': 'Thổ'},
                'Thổ': {'Bản Thân': 'Thổ', 'Huynh Đệ': 'Thổ', 'Phụ Mẫu': 'Hỏa', 'Quan Quỷ': 'Mộc', 'Thê Tài': 'Thủy', 'Tử Tôn': 'Kim'},
                'Kim': {'Bản Thân': 'Kim', 'Huynh Đệ': 'Kim', 'Phụ Mẫu': 'Thổ', 'Quan Quỷ': 'Hỏa', 'Thê Tài': 'Mộc', 'Tử Tôn': 'Thủy'},
                'Thủy': {'Bản Thân': 'Thủy', 'Huynh Đệ': 'Thủy', 'Phụ Mẫu': 'Kim', 'Quan Quỷ': 'Thổ', 'Thê Tài': 'Hỏa', 'Tử Tôn': 'Mộc'},
            }
            
            # Map dung_than → hành
            # FIX V42.9: Sử dụng hành DT từ Lục Hào trước tiên
            _hanh_dt_lh = _get_hanh_dt_from_luc_hao(luc_hao_data, dung_than)
            if _hanh_dt_lh:
                hanh_dt_v22 = _hanh_dt_lh
            else:
                _dt_map = _DT_HANH.get(_hanh_ban_than, {})
                hanh_dt_v22 = _dt_map.get(dung_than, _hanh_ban_than)
            
            self.log_step("V35.8 HanhDT", "MAP", 
                          f"Can={chart_data.get('can_ngay','')} → BT={_hanh_ban_than} | DT={dung_than} → Hành={hanh_dt_v22}")
            
            # Tìm cung BT để tính Ngũ Khí
            can_ngay_v22 = chart_data.get('can_ngay', '')
            can_thien_ban_v22 = chart_data.get('can_thien_ban', {})
            chu_cung_v22 = None
            for cn, cv in can_thien_ban_v22.items():
                if cv == can_ngay_v22:
                    chu_cung_v22 = int(cn) if cn else None
                    break
            if not chu_cung_v22 and can_ngay_v22 == 'Giáp':
                for cn, cv in can_thien_ban_v22.items():
                    if cv == 'Mậu':
                        chu_cung_v22 = int(cn) if cn else None
                        break
            if chu_cung_v22:
                cung_bt_hanh_v22 = CUNG_NGU_HANH.get(chu_cung_v22, '')
            
            ngu_khi_state_v22, ngu_khi_pwr_v22 = _calc_ngu_khi(hanh_dt_v22, cung_bt_hanh_v22)
        
        unified_v22 = _calc_unified_strength_tier(
            lh_raw=v16_lh_raw,
            ts_stage=ts_stage,
            ngu_khi=ngu_khi_state_v22,
            hanh_dt=hanh_dt_v22
        )
        
        # Bảng vạn vật từ weighted_pct (5 PP) — giữ lại như cũ
        vv_key, vv_data = _get_van_vat_from_pct(weighted_pct)
        
        sections.append(f"\n### 🧬 BƯỚC 5.7: LƯỢNG HÓA LỰC LƯỢNG (V42.9 LỰC LƯỢNG THỐNG NHẤT)")
        
        # A. Bảng 3 tầng Unified
        sections.append(f"\n**A. 3 TẦNG ĐO LỰC LƯỢNG DT:**")
        sections.append(f"| Tầng | Nguồn | Điểm | Trọng số |")
        sections.append(f"|---|---|---|---|")
        sections.append(f"| ① Lục Hào thô | Điểm={v16_lh_raw:+d} → chuẩn hóa | {unified_v22['lh_pct']}% | 50% |")
        sections.append(f"| ② 12 Trường Sinh | {ts_stage or 'N/A'} ({TRUONG_SINH_POWER.get(ts_stage, {}).get('cap', '?') if ts_stage else '?'}) | {unified_v22['ts_pct']}% | 30% |")
        sections.append(f"| ③ Ngũ Khí | {ngu_khi_state_v22} ({hanh_dt_v22} @ {cung_bt_hanh_v22 or '?'}) | {unified_v22['nk_pct']}% | 20% |")
        sections.append(f"| **TỔNG HỢP** | **3 tầng tổng hợp** | **{unified_v22['unified_pct']}%** | {unified_v22['tier_data']['cap']} |")
        sections.append(f"| **TỔNG HỢP 5PP** | **KM+LH+MH+LN+TA** | **{weighted_pct}%** | {vv_data['cap']} |")
        
        # A2. V26.2: BẢNG THỐNG KÊ TOÀN BỘ YẾU TỐ TÁC ĐỘNG DT
        if v23_lh_factors:
            # Phân loại factors
            noi_tai = []  # Yếu tố nội tại DT
            ben_ngoai = []  # Yếu tố bên ngoài (Nhật/Nguyệt/Hào khác)
            doi_nghich = []  # Yếu tố đối nghịch (Kỵ/Cừu/Phản Ngâm/Hóa Tuyệt)
            
            for f in v23_lh_factors:
                f_lower = f.lower()
                if any(k in f for k in ['DT ', 'DT(', 'Dụng', 'ĐỘNG', 'TĨNH', 'TRÌ THẾ', 'hào 6', 'hào 5', 'hào 1']):
                    noi_tai.append(f)
                elif any(k in f for k in ['Kỵ', 'Cừu', 'PHẢN', 'PHỤC', 'Hóa T', 'Hóa M', 'khắc DT', 'xung DT', 'THỐI', 'Ứng khắc', 'KT(']):
                    doi_nghich.append(f)
                else:
                    ben_ngoai.append(f)
            
            tong_diem_tot = sum(1 for f in v23_lh_factors if '+' in f)
            tong_diem_xau = sum(1 for f in v23_lh_factors if '-' in f and '+' not in f)
            
            sections.append(f"\n**A2. 📋 THỐNG KÊ TOÀN BỘ YẾU TỐ TÁC ĐỘNG DT (V42.9) — {len(v23_lh_factors)} yếu tố:**")
            sections.append(f"*✅ Thuận lợi: {tong_diem_tot} | ⚠️ Bất lợi: {tong_diem_xau} | Tổng: {v16_lh_raw:+d}*")
            
            if noi_tai:
                sections.append(f"\n**🔵 NỘI TẠI (DT bản thân):** ({len(noi_tai)} yếu tố)")
                for f in noi_tai:
                    icon = '✅' if '+' in f else '⚠️'
                    sections.append(f"- {icon} {f}")
            
            if ben_ngoai:
                sections.append(f"\n**🟢 BÊN NGOÀI (Nhật/Nguyệt/Hào khác):** ({len(ben_ngoai)} yếu tố)")
                for f in ben_ngoai:
                    icon = '✅' if '+' in f else '⚠️'
                    sections.append(f"- {icon} {f}")
            
            if doi_nghich:
                sections.append(f"\n**🔴 ĐỐI NGHỊCH (Kỵ/Cừu/Phản Ngâm/Hóa Tuyệt):** ({len(doi_nghich)} yếu tố)")
                for f in doi_nghich:
                    sections.append(f"- ⚠️ {f}")
        
        # B. Ngũ Hành vật chất từ unified
        hv = unified_v22.get('hanh_vat', {})
        if hv:
            sections.append(f"\n**B. NGŨ HÀNH VẬT CHẤT ({hanh_dt_v22}):**")
            sections.append(f"| Thuộc tính | Giá trị |")
            sections.append(f"|---|---|")
            sections.append(f"| 📐 Hình dáng | {hv.get('hinh', '?')} |")
            sections.append(f"| 🔧 Chất liệu | {hv.get('chat_lieu', '?')} |")
            sections.append(f"| 🎨 Màu sắc | {hv.get('mau', '?')} |")
            sections.append(f"| 🧭 Hướng | {hv.get('huong', '?')} |")
            sections.append(f"| 👅 Vị | {hv.get('vi', '?')} |")
            sections.append(f"| 🏥 Cơ thể | {hv.get('co_the', '?')} |")
        
        # C. Mapping vạn vật từ weighted_pct
        sections.append(f"\n**C. MAPPING VẠN VẬT ({vv_data['cap']}):**")
        sections.append(f"| Tiêu chí | Giá trị |")
        sections.append(f"|---|---|")
        sections.append(f"| 🎯 % Lực lượng (5PP) | **{weighted_pct}%** — {vv_data['cap']} |")
        sections.append(f"| 🎯 % Lực lượng (3 tầng) | **{unified_v22['unified_pct']}%** — {unified_v22['tier_data']['cap']} |")
        sections.append(f"| 🧑 Vòng đời con người | {vv_data['con_nguoi']} |")
        sections.append(f"| 📐 Kích thước | {vv_data['kich_thuoc']} |")
        sections.append(f"| 🆕 Tình trạng | {vv_data['tinh_trang']} |")
        sections.append(f"| 🔢 Số lượng | {vv_data['so_luong']} |")
        sections.append(f"| 💎 Chất lượng | {vv_data['chat_luong']} |")
        sections.append(f"| 🎨 Màu sắc | {vv_data['mau_sac']} |")
        sections.append(f"| ⏱️ Tốc độ | {vv_data['toc_do']} |")
        sections.append(f"| 🔢 Con số | {vv_data['so']} |")
        
        # D. 12 Trường Sinh chi tiết
        if ts_stage:
            ts_info = TRUONG_SINH_POWER.get(ts_stage, {})
            sections.append(f"\n**D. 12 TRƯỜNG SINH:** {ts_stage} ({ts_info.get('cap', '?')}) — Power={ts_info.get('power', 50)}%")
            sections.append(f"→ Con người: {ts_info.get('con_nguoi', '?')} | Vật: {ts_info.get('vat', '?')}")
        
        # E. V26.2: VẠN VẬT CỤ THỂ = Ngũ Hành × Tầng Vượng Suy
        vv_cu_the = _get_van_vat_cu_the(hanh_dt_v22, unified_v22.get('tier_key', 'TRUNG_BÌNH'))
        if vv_cu_the:
            sections.append(f"\n**E. 🎯 VẠN VẬT CỤ THỂ ({hanh_dt_v22} × {unified_v22['tier_data']['cap']}):**")
            sections.append(f"| Loại | Mô tả cụ thể |")
            sections.append(f"|---|---|")
            sections.append(f"| 🔮 Đồ vật | {vv_cu_the.get('do_vat', '?')} |")
            sections.append(f"| 🏠 Nhà cửa | {vv_cu_the.get('nha_cua', '?')} |")
            sections.append(f"| 🧑 Người | {vv_cu_the.get('nguoi', '?')} |")
            sections.append(f"| 🏥 Bệnh | {vv_cu_the.get('benh', '?')} |")
        
        # Đếm số lượng (V41.0 — ENHANCED: Tự động tính số từ Ngũ Hành + Quái + Vạn Vật)
        if is_count or is_age:
            # V41.0: Nếu count_numbers rỗng → TỰ ĐỘNG tính từ Vạn Vật + Ngũ Hành + Quái
            _HANH_SO_HA_DO = {
                'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 10)
            }
            _HANH_SO_LAC_THU = {
                'Thủy': 1, 'Hỏa': 9, 'Mộc': 3, 'Kim': 7, 'Thổ': 5
            }
            _QUAI_SO = {
                'Càn': 1, 'Đoài': 2, 'Ly': 3, 'Chấn': 4,
                'Tốn': 5, 'Khảm': 6, 'Cấn': 7, 'Khôn': 8
            }
            
            if not count_numbers and hanh_dt_v22:
                # ① Số từ Ngũ Hành DT (Hà Đồ — sinh số + thành số)
                hd_so = _HANH_SO_HA_DO.get(hanh_dt_v22, (5, 10))
                count_numbers.append(('Ngũ Hành (Hà Đồ)', hd_so[0]))
                count_numbers.append(('Ngũ Hành (Thành Số)', hd_so[1]))
                
                # ② Số từ Lạc Thư
                lt_so = _HANH_SO_LAC_THU.get(hanh_dt_v22, 5)
                count_numbers.append(('Lạc Thư', lt_so))
                
                # ③ Số từ Quái Tượng (Mai Hoa Thượng Quái)
                if mai_hoa_data and isinstance(mai_hoa_data, dict):
                    _mh_ten = mai_hoa_data.get('ten_thuong', mai_hoa_data.get('thuong_quai', ''))
                    for qname, qnum in _QUAI_SO.items():
                        if qname in str(_mh_ten):
                            count_numbers.append(('Quái Tượng (Thượng)', qnum))
                            break
                    _mh_ha = mai_hoa_data.get('ten_ha', mai_hoa_data.get('ha_quai', ''))
                    for qname, qnum in _QUAI_SO.items():
                        if qname in str(_mh_ha):
                            count_numbers.append(('Quái Tượng (Hạ)', qnum))
                            break
                
                # ④ Số từ Vạn Vật tier (vv_data['so'] = "7-8")
                vv_so_str = vv_data.get('so', '')
                if vv_so_str:
                    try:
                        if '-' in str(vv_so_str):
                            parts = str(vv_so_str).split('-')
                            vv_so_avg = (int(parts[0]) + int(parts[1])) / 2
                        else:
                            vv_so_avg = float(vv_so_str)
                        count_numbers.append(('Vạn Vật (Vượng/Suy)', int(round(vv_so_avg))))
                    except (ValueError, IndexError):
                        pass
            
            if count_numbers:
                sections.append(f"\n**📊 BẢNG SỐ LƯỢNG TỪ CÁC PHƯƠNG PHÁP:**")
                sections.append(f"| Phương Pháp | Số |")
                sections.append(f"|---|---|")
                for pp, num in count_numbers:
                    sections.append(f"| {pp} | **{num}** |")
                all_nums = [n for _, n in count_numbers]
                if len(all_nums) >= 2:
                    # Lấy MEDIAN (trung vị) thay vì trung bình → tránh bị kéo lệch
                    sorted_nums = sorted(all_nums)
                    mid = len(sorted_nums) // 2
                    median = sorted_nums[mid] if len(sorted_nums) % 2 else int(round((sorted_nums[mid-1] + sorted_nums[mid]) / 2))
                    avg = sum(all_nums) / len(all_nums)
                    sections.append(f"\n→ **🔢 KẾT LUẬN SỐ LƯỢNG: {median}** (Trung vị) hoặc **{int(round(avg))}** (TB) — từ {len(count_numbers)} nguồn")
                    sections.append(f"→ *Phạm vi: {min(all_nums)} — {max(all_nums)}*")
                elif len(all_nums) == 1:
                    sections.append(f"\n→ **🔢 KẾT LUẬN SỐ LƯỢNG: {all_nums[0]}**")
        elif is_age and age_numbers:
            sections.append(f"\n**📊 Bảng số tuổi từ các phương pháp:**")
            for pp, num in age_numbers:
                sections.append(f"- {pp}: **{num}**")
            all_nums = [n for _, n in age_numbers]
            avg = sum(all_nums) / len(all_nums) if all_nums else 0
            sections.append(f"\n→ **KẾT LUẬN TUỔI: Khoảng {int(avg)} tuổi** (trung bình từ {len(age_numbers)} phương pháp)")
        
        # ========================================
        # BƯỚC 7: TÁC ĐỘNG VÀO CHU THỂ (giữ lại chỉ impact_text, không còn direct_answer)
        # ========================================
        impact_text, direct_answer, impact_evidence = self._build_element_impact_analysis(
            question=question,
            dung_than=dung_than,
            category_label=cat_data['label'],
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            ky_mon_verdict=ky_mon_verdict,
            luc_hao_verdict=luc_hao_verdict,
            mai_hoa_verdict=mai_hoa_verdict,
            ky_mon_reason=ky_mon_reason,
            luc_hao_reason=luc_hao_reason,
            mai_hoa_reason=mai_hoa_reason,
            age_numbers=age_numbers,
            count_numbers=count_numbers,
            luc_nham_verdict=luc_nham_verdict,
            thai_at_verdict=thai_at_verdict,
            weighted_pct=weighted_pct,
            lh_factors=v23_lh_factors,
            km_factors=v24_km_factors if 'v24_km_factors' in dir() else [],
            mh_factors=v24_mh_factors if 'v24_mh_factors' in dir() else [],
        )
        
        # V42.9: direct_answer GIỮ trong sections[] → offline_full_output chứa THÁM TỬ/PHÁN QUYẾT
        # Collapse output SẼ KHÔNG append direct_answer RIÊNG → chỉ có 1 bản duy nhất
        if direct_answer:
            sections.append(f"\n### 🔍 THÁM TỬ KIỂM CHỨNG + CÂU TRẢ LỜI")
            sections.append(direct_answer)
        
        # V42.9: KẾT LUẬN THỐNG NHẤT đã được tính trong v38_protocol_text
        # (phần V. KẾT LUẬN CHÍNH THỨC) → không cần duplicate ở đây
        unified_narrative = self._build_unified_narrative(
            question=question,
            dung_than=dung_than,
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            ky_mon_verdict=ky_mon_verdict,
            luc_hao_verdict=luc_hao_verdict,
            mai_hoa_verdict=mai_hoa_verdict,
            ky_mon_reason=ky_mon_reason,
            luc_hao_reason=luc_hao_reason,
            mai_hoa_reason=mai_hoa_reason,
            impact_evidence=impact_evidence,
            luc_nham_verdict=luc_nham_verdict,
            luc_nham_reason=luc_nham_reason,
            thai_at_verdict=thai_at_verdict,
            thai_at_reason=thai_at_reason,
            final_pct=weighted_pct,
            lh_factors=v23_lh_factors,
            km_factors=v24_km_factors,
            mh_factors=v24_mh_factors
        )
        # unified_narrative vẫn tính nhưng KHÔNG append vào sections
        # → Dùng cho offline_analysis_data gửi AI Online
        
        sections.append(f"\n---\n*🤖 Thiên Cơ Đại Sư V42.9 — Lực Lượng Tổng Hợp: Tổng Hợp 5PP={weighted_pct}%, Tổng Hợp 3 Tầng={unified_v22['unified_pct']}%, Ngũ Khí={ngu_khi_state_v22}.*")
        
        # ========================================
        # V11.1: AI ONLINE LÀ PHÂN TÍCH CHÍNH
        # AI Offline chỉ hiện khi nhấn nút
        # ========================================
        offline_full_output = "\n".join(sections)
        
        # V15.3: Extract V15 analysis summaries for Online AI
        v15_bt_score = ''
        v15_dt_score = ''
        v15_timeline = ''
        v15_timing = ''
        try:
            if chart_data and isinstance(chart_data, dict):
                can_ngay_v15 = chart_data.get('can_ngay', '')
                can_thien_ban_v15 = chart_data.get('can_thien_ban', {})
                
                # Tìm cung BT
                chu_cung_v15 = None
                for cn, cv in can_thien_ban_v15.items():
                    if cv == can_ngay_v15:
                        chu_cung_v15 = int(cn) if cn else None
                        break
                if not chu_cung_v15 and can_ngay_v15 == 'Giáp':
                    for cn, cv in can_thien_ban_v15.items():
                        if cv in ('Mậu', 'Kỷ'):  # V40.2: Giáp ẩn dưới Mậu HOẶC Kỷ
                            chu_cung_v15 = int(cn) if cn else None
                            break
                
                # Tìm cung DT
                dt_can_map_v15 = {
                    'Quan Quỷ': chart_data.get('can_gio', ''),
                    'Thê Tài': chart_data.get('can_gio', ''),
                    'Tử Tôn': chart_data.get('can_gio', ''),
                    'Phụ Mẫu': chart_data.get('can_nam', ''),
                    'Huynh Đệ': chart_data.get('can_thang', ''),
                    'Bản Thân': can_ngay_v15,
                }
                dt_can_v15 = dt_can_map_v15.get(dung_than, chart_data.get('can_gio', ''))
                dt_cung_v15 = None
                if dt_can_v15 and dt_can_v15 != can_ngay_v15:
                    for cn, cv in can_thien_ban_v15.items():
                        if cv == dt_can_v15:
                            dt_cung_v15 = int(cn) if cn else None
                            break
                
                # BT Score summary
                if chu_cung_v15:
                    bt_s, bt_d, bt_str = self._analyze_cung_factors(chu_cung_v15, chart_data, question, "BẢN THÂN")
                    v15_bt_score = f"Cung {chu_cung_v15} ({QUAI_TUONG.get(chu_cung_v15, '?')}, {CUNG_NGU_HANH.get(chu_cung_v15, '?')}): Score={bt_s}, {bt_str}"
                
                # DT Score summary
                dt_score_val = 0
                if dt_cung_v15:
                    if dt_cung_v15 != chu_cung_v15:
                        dt_s, dt_d, dt_str = self._analyze_cung_factors(dt_cung_v15, chart_data, question, f"DỤNG THẦN ({dung_than})")
                        v15_dt_score = f"Cung {dt_cung_v15} ({QUAI_TUONG.get(dt_cung_v15, '?')}, {CUNG_NGU_HANH.get(dt_cung_v15, '?')}): Score={dt_s}, {dt_str}"
                        dt_score_val = dt_s
                    else:
                        # V40.2: BT=DT cùng cung → dùng BT score
                        v15_dt_score = v15_bt_score.replace('BẢN THÂN', f'DỤNG THẦN ({dung_than})') if v15_bt_score else ''
                
                # Timeline summary
                tl_cung = dt_cung_v15 or chu_cung_v15
                if tl_cung:
                    tl_details = self._analyze_timeline(tl_cung, chart_data, question, dung_than)
                    # Lấy dòng xu hướng cuối cùng
                    for td in reversed(tl_details):
                        if 'XU HƯỚNG' in td:
                            v15_timeline = td.replace('└ ', '').replace('**', '').strip()
                            break
                
                # Timing/Ứng Kỳ summary
                timing_cung = dt_cung_v15 or chu_cung_v15
                if timing_cung:
                    tm_details = self._analyze_timing(timing_cung, chart_data, question, dung_than, cung_score=dt_score_val)
                    # Lấy tốc độ + ứng kỳ
                    tm_parts = []
                    for td in tm_details:
                        if 'TỔNG KẾT' in td:
                            tm_parts.append(td.replace('└ ', '').replace('**', '').strip())
                        elif '📅' in td and ('XUNG' in td or 'SINH' in td or 'Chi' in td):
                            tm_parts.append(td.replace('├ ', '').replace('│', '').replace('**', '').strip())
                        elif 'DỊCH MÃ' in td:
                            tm_parts.append(td.replace('├ ', '').replace('**', '').strip())
                        elif 'TUẦN KHÔNG' in td:
                            tm_parts.append(td.replace('├ ', '').replace('**', '').strip())
                    if tm_parts:
                        v15_timing = ' | '.join(tm_parts[:3])
        except Exception:
            pass  # V15 summaries are optional, don't break main flow
        
        # V21.0: Reuse scores already computed before BƯỚC 6
        v16_lh_score = v16_lh_score_str
        v16_mh_score = v16_mh_score_str
        v16_tb_score = v16_tb_score_str
        v16_ln_score = v16_ln_score_str
        v16_ta_score = v16_ta_score_str
        
        # V17.0: Method Routing — xác định PP CHÍNH + đối chiếu %
        v17_routing = ''
        try:
            v17_verdicts = {
                'ky_mon': ky_mon_verdict,
                'luc_hao': luc_hao_verdict,
                'mai_hoa': mai_hoa_verdict,
                'luc_nham': luc_nham_verdict,
                'thai_at': thai_at_verdict,
                'thiet_ban': 'BÌNH',  # Thiết Bản không có verdict riêng
            }
            v17_scores = {
                'ky_mon': 0, 'luc_hao': 0, 'mai_hoa': 0,
                'thiet_ban': 0, 'luc_nham': 0, 'thai_at': 0,
            }
            # Extract numeric scores from V16 summaries
            import re as _re
            for key, summary in [('luc_hao', v16_lh_score), ('mai_hoa', v16_mh_score),
                                 ('thiet_ban', v16_tb_score), ('luc_nham', v16_ln_score),
                                 ('thai_at', v16_ta_score)]:
                m = _re.search(r'Score=(-?\d+)', str(summary))
                if m:
                    v17_scores[key] = int(m.group(1))
            # KM score from V15
            if v15_bt_score:
                m = _re.search(r'Score=(-?\d+)', v15_bt_score)
                if m:
                    v17_scores['ky_mon'] = int(m.group(1))
            
            routing = self._get_method_routing(cat_data['label'], v17_verdicts, v17_scores)
            v17_routing = routing.get('routing_text', '')
        except Exception:
            pass
        
        # V18.0: Detective Deduction
        v18_detective = ''
        try:
            det_text, det_clues, det_deductions = self._detective_deduction(chart_data, mai_hoa_data, luc_hao_data, question)
            v18_detective = det_text
        except Exception:
            pass
        
        # V15.3: Thu thập dữ liệu TOÀN DIỆN cho AI Online
        offline_analysis_data = {
            'dung_than': dung_than,
            'category_label': cat_data['label'],
            'ky_mon_verdict': ky_mon_verdict,
            'ky_mon_reason': ky_mon_reason,
            'luc_hao_verdict': luc_hao_verdict,
            'luc_hao_reason': luc_hao_reason,
            'mai_hoa_verdict': mai_hoa_verdict,
            'mai_hoa_reason': mai_hoa_reason,
            'luc_nham_verdict': luc_nham_verdict,
            'luc_nham_reason': luc_nham_reason,
            'thai_at_verdict': thai_at_verdict,
            'thai_at_reason': thai_at_reason,
            'count_numbers': count_numbers,
            'age_numbers': age_numbers,
            'impact_evidence': impact_evidence,
            'unified_narrative': unified_narrative,
            # V15.3: Structured V15 analysis summaries for Online AI
            'v15_bt_score': v15_bt_score,
            'v15_dt_score': v15_dt_score,
            'v15_timeline': v15_timeline,
            'v15_timing': v15_timing,
            # V16.0: Multi-method scoring
            'v16_lh_score': v16_lh_score,
            'v16_mh_score': v16_mh_score,
            'v16_tb_score': v16_tb_score,
            'v16_ln_score': v16_ln_score,
            'v16_ta_score': v16_ta_score,
            # V17.0: Method routing
            'v17_routing': v17_routing,
            'v17_primary_method': routing.get('primary_name', '?') if routing else '?',
            'v17_primary_verdict': routing.get('primary_verdict', '?') if routing else '?',
            'v17_deviations': routing.get('deviations', []) if routing else [],
            # V18.0: Detective deduction
            'v18_detective': v18_detective,
            # V26.2: Lực Lượng Tổng Hợp — 3 tầng tổng hợp
            'v22_unified_strength': {
                'unified_pct': unified_v22['unified_pct'] if unified_v22 else 50,
                'lh_pct': unified_v22['lh_pct'] if unified_v22 else 50,
                'ts_pct': unified_v22['ts_pct'] if unified_v22 else 50,
                'nk_pct': unified_v22['nk_pct'] if unified_v22 else 50,
                'tier_cap': unified_v22['tier_data']['cap'] if unified_v22 else '?',
                'ngu_khi': ngu_khi_state_v22,
                'hanh_dt': hanh_dt_v22,
                'ts_stage': ts_stage or 'N/A',
                'hanh_vat': unified_v22.get('hanh_vat', {}) if unified_v22 else {},
                'van_vat_cu_the': _get_van_vat_cu_the(hanh_dt_v22, unified_v22.get('tier_key', 'TRUNG_BÌNH')) if unified_v22 else {},
            },
            # V26.2: Toàn bộ yếu tố tác động Đa Môn Phái
            'v23_lh_factors': v23_lh_factors,
            'v24_km_factors': v24_km_factors,
            'v24_mh_factors': v24_mh_factors,
            'v24_tb_factors': v24_tb_factors,
            'v24_ln_factors': v24_ln_factors,
            'v24_ta_factors': v24_ta_factors,
            # V14.0: Gửi báo cáo offline (V26.3: giảm xuống 4000 ký tự tránh Gemini ngộp)
            'full_offline_report': offline_full_output[:4000] if offline_full_output else '',
            # V40.2: Mai Hoa — Hỗ Quái + Biến Quái + Nghĩa (keys thật từ engine)
            'mai_hoa_ho_quai': mai_hoa_data.get('ten_ho', '') if mai_hoa_data else '',
            'mai_hoa_bien_quai': mai_hoa_data.get('ten_qua_bien', '') if mai_hoa_data else '',
            'mai_hoa_nghia': mai_hoa_data.get('nghĩa', mai_hoa_data.get('nghia', '')) if mai_hoa_data else '',
            'mai_hoa_interpretation': mai_hoa_data.get('interpretation', '') if mai_hoa_data else '',
            # V40.2: Lục Hào — Tên quẻ
            'luc_hao_ten_que': luc_hao_data.get('ban', {}).get('name', '') if luc_hao_data and isinstance(luc_hao_data, dict) else '',
            'luc_hao_cung': luc_hao_data.get('ban', {}).get('palace', '') if luc_hao_data and isinstance(luc_hao_data, dict) else '',
        }
        
        # ═══════════════════════════════════════════════════════════
        # V31.0: TẠO SƠ ĐỒ TƯƠNG TÁC THỜI GIAN THỰC
        # ═══════════════════════════════════════════════════════════
        v31_master_diagram = ""
        v31_master_info = {}
        v31_question_diagram = ""
        v31_question_info = {}
        v31_diagram_id = 'SD0'
        
        try:
            # 1. SĐ_MASTER: DT → Suy/Vượng → Vạn Vật (LUÔN hiển thị)
            v31_v22_data = {
                'lh_pct': unified_v22['lh_pct'] if unified_v22 else 50,
                'ts_stage': ts_stage or 'N/A',
                'ts_power': TRUONG_SINH_POWER.get(ts_stage, {}).get('power', 50) if ts_stage else 50,
                'ngu_khi': ngu_khi_state_v22,
                'nk_power': NGU_KHI_POWER.get(ngu_khi_state_v22, {}).get('power', 50) if ngu_khi_state_v22 else 50,
                'unified_pct': unified_v22['unified_pct'] if unified_v22 else 50,
                'tier_cap': unified_v22['tier_data']['cap'] if unified_v22 else '?',
                'tier_data': unified_v22.get('tier_data', {}) if unified_v22 else {},
                'hanh_vat': unified_v22.get('hanh_vat', {}) if unified_v22 else {},
                'van_vat_cu_the': _get_van_vat_cu_the(hanh_dt_v22, unified_v22.get('tier_key', 'TRUNG_BÌNH')) if unified_v22 else {},
            }
            
            v31_master_diagram, v31_master_info = self._fill_master_diagram(
                question=question,
                category_label=category_label,
                dung_than=dung_than,
                hanh_dt=hanh_dt_v22,
                unified_v22=v31_v22_data,
                v23_lh_factors=v23_lh_factors,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                v24_km_factors=v24_km_factors,
            )
            
            # 2. Sơ đồ theo loại câu hỏi (SĐ1-SĐ16)
            v31_diagram_id, v31_diagram_info = match_question_to_diagram(question)
            
            v31_verdicts = {
                'km': ky_mon_verdict, 'lh': luc_hao_verdict,
                'mh': mai_hoa_verdict, 'ln': luc_nham_verdict,
                'ta': thai_at_verdict,
            }
            
            v31_question_diagram, v31_question_info = self._fill_question_diagram(
                diagram_id=v31_diagram_id,
                question=question,
                dung_than=dung_than,
                hanh_dt=hanh_dt_v22,
                unified_v22=v31_v22_data,
                v23_lh_factors=v23_lh_factors,
                v24_km_factors=v24_km_factors,
                v24_mh_factors=v24_mh_factors,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                verdicts_dict=v31_verdicts,
            )
            
            # Inject vào offline_analysis_data cho Gemini
            offline_analysis_data['v31_master_diagram'] = v31_master_diagram
            offline_analysis_data['v31_question_diagram'] = v31_question_diagram
            offline_analysis_data['v31_diagram_id'] = v31_diagram_id
            offline_analysis_data['v31_master_conclusion'] = v31_master_info.get('conclusion', '')
            offline_analysis_data['v31_formula'] = v31_master_info.get('formula_detail', '')
            
        except Exception as e:
            self.log_step("V31 Diagrams", "ERROR", str(e)[:80])
        
        # ═══════════════════════════════════════════════════════════
        # V38.1: ÁP DỤNG PROTOCOL 27 BƯỚC
        # ═══════════════════════════════════════════════════════════
        v38_protocol_text = ''
        v38_conclusion = ''
        try:
            v38_protocol_text, v38_conclusion, weighted_pct = self._apply_27step_protocol(
                question=question,
                dung_than=dung_than,
                hanh_dt=hanh_dt_v22,
                km_factors=v24_km_factors,
                lh_factors=v23_lh_factors,
                mh_factors=v24_mh_factors,
                km_score=v16_km_raw,
                lh_score=v16_lh_raw,
                mh_score=v16_mh_raw,
                tb_factors=v24_tb_factors,
                ln_factors=v24_ln_factors,
                ta_factors=v24_ta_factors,
                tb_score=v16_tb_raw,
                ln_score=v16_ln_raw,
                ta_score=v16_ta_raw,
                weighted_pct=weighted_pct,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
            )
            self.log_step("V38.1", "27-STEP OK", v38_conclusion[:80])
        except Exception as e:
            self.log_step("V38.1", "ERROR", str(e)[:80])
        
        # Gọi AI Online (Gemini) — phân tích sâu
        online_result = self._try_online_ai(
            question=question,
            chart_data=chart_data,
            mai_hoa_data=mai_hoa_data,
            luc_hao_data=luc_hao_data,
            topic=topic,
            offline_analysis_data=offline_analysis_data
        )
        
        if online_result:
            # V31.0: AI Online + Sơ Đồ Tương Tác
            final_parts = []
            
            # V40.9: Extract verdict line from online_result for header display
            _online_verdict_line = ""
            _online_visao = ""
            _online_ungky = ""
            _online_giaiphap = ""
            for _line in online_result.split('\n'):
                _stripped = _line.strip()
                if '📢' in _stripped and 'CÂU TRẢ LỜI' in _stripped.upper():
                    _online_verdict_line = _stripped.replace('**', '').replace('📢', '').replace('CÂU TRẢ LỜI:', '').replace('CÂU TRẢ LỜI', '').strip()
                elif '📋' in _stripped and 'VÌ SAO' in _stripped.upper():
                    _online_visao = _stripped.replace('**', '').replace('📋', '').replace('VÌ SAO:', '').strip()
                elif '⏳' in _stripped and 'ỨNG KỲ' in _stripped.upper():
                    _online_ungky = _stripped.replace('**', '').replace('⏳', '').replace('ỨNG KỲ:', '').strip()
                elif '🔧' in _stripped and 'GIẢI PHÁP' in _stripped.upper():
                    _online_giaiphap = _stripped.replace('**', '').replace('🔧', '').replace('GIẢI PHÁP:', '').strip()
            
            if not _online_verdict_line:
                _online_verdict_line = "Xem chi tiết bên dưới"
            
            # === V42.0: CẢNH BÁO PHẢN/PHỤC NGÂM — Hiển thị TRƯỚC kết luận ===
            try:
                _ppn_warning_online = _build_phan_phuc_ngam_warning(chart_data, luc_hao_data)
                if _ppn_warning_online:
                    final_parts.append(_ppn_warning_online)
            except Exception:
                pass
            
            # === V42.1: CẢNH BÁO NGUYỆT PHÁ — Hiển thị TRƯỚC kết luận ===
            try:
                _lh_dt_chi_np = ''
                _lh_chi_thang_np = ''
                if luc_hao_data:
                    _lh_haos_np = luc_hao_data.get('ban', {}).get('haos', luc_hao_data.get('haos', []))
                    _lh_chi_thang_np = luc_hao_data.get('chi_thang', '')
                    if _lh_haos_np and dung_than:
                        for _h_np in _lh_haos_np:
                            if _h_np.get('luc_than', '') == dung_than:
                                _lh_dt_chi_np = _h_np.get('chi', '')
                                break
                    if _lh_dt_chi_np and _lh_chi_thang_np:
                        _, _np_html_online = _build_nguyet_pha_warning(
                            _lh_dt_chi_np, _lh_chi_thang_np,
                            dung_than_name=dung_than or 'Dụng Thần'
                        )
                        if _np_html_online:
                            final_parts.append(_np_html_online)
            except Exception:
                pass
            
            # === ÔÔ NÂU TO — KẾT LUẬN AI ONLINE ===
            final_parts.append(
                f'<div style="background:linear-gradient(135deg,#78350f,#92400e);padding:28px;border-radius:16px;margin:16px 0;border:3px solid #f59e0b;box-shadow:0 4px 25px rgba(245,158,11,0.4);">'
                f'<div style="font-size:1.2em;font-weight:700;color:#fde68a;margin-bottom:10px;">🌐 KẾT LUẬN AI ONLINE (Gemini V42.9)</div>'
                f'<div style="font-size:2.2em;font-weight:900;color:#ffffff;line-height:1.3;margin-bottom:12px;">📢 {_online_verdict_line}</div>'
                + (f'<div style="font-size:1.1em;color:#fef3c7;margin-bottom:6px;">📋 <b>Vì sao:</b> {_online_visao}</div>' if _online_visao else '')
                + (f'<div style="font-size:1.1em;color:#fde68a;margin-bottom:6px;">⏳ <b>Ứng kỳ:</b> {_online_ungky}</div>' if _online_ungky else '')
                + (f'<div style="font-size:1.1em;color:#fbbf24;">🔧 <b>Giải pháp:</b> {_online_giaiphap}</div>' if _online_giaiphap else '')
                + f'</div>'
            )
            
            # Chi tiết phân tích Online → collapse
            final_parts.append("\n<details>")
            final_parts.append(f"<summary><b>📖 XEM CHI TIẾT PHÂN TÍCH AI ONLINE (nhấn để mở)</b></summary>\n")
            final_parts.append(online_result)
            final_parts.append("\n</details>")
            final_parts.append("")
            
            # V40.9: LUÔN HIỆN Ô XANH LÁ — KẾT LUẬN AI OFFLINE (ngay cả khi có Online)
            # Tính verdict offline
            _off_v_icon = '🟢' if weighted_pct >= 65 else '🟡' if weighted_pct >= 45 else '🔴'
            _off_verdict = 'CÁT' if weighted_pct >= 65 else 'BÌNH' if weighted_pct >= 45 else 'HUNG'
            
            # Extract câu trả lời từ direct_answer
            _off_answer = ""
            _off_evidence = []
            if direct_answer:
                for _line in direct_answer.split('\n'):
                    _s = _line.strip()
                    if not _off_answer:
                        if any(x in _s for x in ['📢', '🟢 CÓ', '🔴 KHÔNG', '🟡 CẦN', '🟢 NÊN', '🔴 KHÔNG NÊN',
                                                  '🟢 ĐƯỢC', '🟢 TỐT', '🔴 XẤU', '✅ CÂU TRẢ LỜI', '✅ CÓ', '🔴 KHÔNG']):
                            _off_answer = _s.replace('**', '').replace('#', '').strip()
                        elif 'CÂU TRẢ LỜI' in _s.upper():
                            _off_answer = _s.replace('**', '').replace('#', '').strip()
                        elif _s.startswith(('🟢', '🔴', '🟡')) and len(_s) > 5:
                            _off_answer = _s.replace('**', '').replace('#', '').strip()
                    elif len(_off_evidence) < 3:
                        if _s.startswith(('- ✅', '- 🔴', '- ⚠️', '- 📌', '- 🏭', '- 🧭', '- ⛔', '- 🏥', '- ⏱️')):
                            _off_evidence.append(_s)
            
            if not _off_answer:
                # V42.0: Detect câu hỏi WHAT/WHERE/WHEN → trả lời đúng kiểu
                _q_lower_off = question.lower()
                _is_what_off = any(k in _q_lower_off for k in ['cái gì', 'loại gì', 'sản xuất gì', 'làm gì', 'sản phẩm gì',
                    'buôn bán gì', 'kinh doanh gì', 'nghề gì', 'ngành gì', 'gì vậy', 'gì đây',
                    'bán gì', 'trồng gì', 'nuôi gì', 'mua gì', 'bằng gì', 'sản xuất cái'])
                _is_where_off = any(k in _q_lower_off for k in ['ở đâu', 'hướng nào', 'phương nào', 'chỗ nào', 'nơi nào'])
                _is_when_off = any(k in _q_lower_off for k in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm'])
                
                if _is_what_off:
                    _LT_HANH_OFF = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
                    _hanh_off = _LT_HANH_OFF.get(dung_than, 'Thổ')
                    _HANH_SP = {'Kim': 'Kim loại/Máy móc/Linh kiện', 'Mộc': 'Gỗ/Vải/Nông sản/Giấy', 
                                'Thủy': 'Nước/Chất lỏng/Hải sản/Hóa chất', 'Hỏa': 'Điện tử/Năng lượng/Thực phẩm chế biến', 
                                'Thổ': 'Gạch/Gốm sứ/Vật liệu XD/Nông sản'}
                    _off_answer = f"🔮 Hành {_hanh_off}: {_HANH_SP.get(_hanh_off, '?')} ({weighted_pct}%)"
                elif _is_where_off:
                    _LT_HANH_OFF2 = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
                    _hanh_off2 = _LT_HANH_OFF2.get(dung_than, 'Thổ')
                    _HANH_HUONG = {'Kim': 'HƯỚNG TÂY', 'Mộc': 'HƯỚNG ĐÔNG', 'Thủy': 'HƯỚNG BẮC', 'Hỏa': 'HƯỚNG NAM', 'Thổ': 'TRUNG TÂM'}
                    _off_answer = f"🧭 {_HANH_HUONG.get(_hanh_off2, '?')} (Hành {_hanh_off2}) — {weighted_pct}%"
                elif _is_when_off:
                    # V42.8f: Tính ngày cụ thể cho header
                    try:
                        from xem_ngay_dep import _jdn as _jdn_header
                        import datetime as _dt_header
                        _LT_HANH_WHEN = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc', 'Bản Thân': 'Thổ'}
                        _h_when = _LT_HANH_WHEN.get(dung_than, 'Thổ')
                        _UKC = {'Kim': [8,9], 'Mộc': [2,3], 'Thủy': [0,11], 'Hỏa': [6,5], 'Thổ': [4,10,1,7]}
                        _SINH_W = {'Kim': 'Thổ', 'Mộc': 'Thủy', 'Thủy': 'Kim', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa'}
                        if weighted_pct >= 55:
                            _target_chis = _UKC.get(_h_when, [4])
                        else:
                            _h_sinh = _SINH_W.get(_h_when, 'Thổ')
                            _target_chis = _UKC.get(_h_sinh, [4])
                        
                        _CHIS_W = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                        _CANS_W = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                        _CHI_GIO_W = {'Tý':'23h-1h','Sửu':'1h-3h','Dần':'3h-5h','Mão':'5h-7h','Thìn':'7h-9h','Tị':'9h-11h',
                                      'Ngọ':'11h-13h','Mùi':'13h-15h','Thân':'15h-17h','Dậu':'17h-19h','Tuất':'19h-21h','Hợi':'21h-23h'}
                        _today = _dt_header.date.today()
                        _nearest_date = None
                        for _off2 in range(1, 200):
                            _d2 = _today + _dt_header.timedelta(days=_off2)
                            _j2 = _jdn_header(_d2.day, _d2.month, _d2.year)
                            _chi2 = (_j2 + 1) % 12
                            if _chi2 in _target_chis:
                                _can2 = _CANS_W[(_j2 + 9) % 10]
                                _chi2_name = _CHIS_W[_chi2]
                                _THU_W = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật']
                                _thu2 = _THU_W[_d2.weekday()]
                                _gio_txt = _CHI_GIO_W.get(_chi2_name, '')
                                _nearest_date = f"📆 {_d2.day:02d}/{_d2.month:02d}/{_d2.year} ({_thu2}) lúc {_gio_txt} — ngày {_can2} {_chi2_name} (còn {_off2} ngày)"
                                break
                        _off_answer = _nearest_date or f"⏳ Xem Ứng Kỳ chi tiết bên dưới ({weighted_pct}%)"
                    except Exception:
                        _off_answer = f"⏳ Xem Ứng Kỳ chi tiết bên dưới ({weighted_pct}%)"
                elif _off_verdict == 'CÁT':
                    _off_answer = f"{_off_v_icon} CÓ — THUẬN LỢI ({weighted_pct}%)"
                elif _off_verdict == 'HUNG':
                    _off_answer = f"{_off_v_icon} KHÔNG — BẤT LỢI ({weighted_pct}%)"
                else:
                    _off_answer = f"{_off_v_icon} CẦN CÂN NHẮC — {_off_verdict} ({weighted_pct}%)"
            
            _off_ev_html = ""
            if _off_evidence:
                _off_ev_html = '<div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.2);">'
                for _ev in _off_evidence:
                    _off_ev_html += f'<div style="font-size:1em;color:#d1fae5;margin:4px 0;">{_ev}</div>'
                _off_ev_html += '</div>'
            
            final_parts.append(
                f'<div style="background:linear-gradient(135deg,#064e3b,#065f46);padding:28px;border-radius:16px;margin:16px 0;border:3px solid #34d399;box-shadow:0 4px 25px rgba(52,211,153,0.4);">'
                f'<div style="font-size:1.2em;font-weight:700;color:#6ee7b7;margin-bottom:10px;">🖥️ KẾT LUẬN AI OFFLINE — THIÊN CƠ ĐẠI SƯ V42.9</div>'
                f'<div style="font-size:2em;font-weight:900;color:#ffffff;line-height:1.3;margin-bottom:8px;">{_off_answer}</div>'
                f'<div style="font-size:1.05em;color:#a7f3d0;">📊 Điểm: <b>{weighted_pct}%</b> | DT: <b>{dung_than}</b> | KM: {ky_mon_verdict} | LH: {luc_hao_verdict} | MH: {mai_hoa_verdict}</div>'
                + _off_ev_html
                + f'</div>'
            )
            
            # V42.9: Chi tiết Offline → 1 collapse DUY NHẤT (LUÔN có offline_full_output)
            final_parts.append("\n<details>")
            final_parts.append(f"<summary><b>📖 XEM CHI TIẾT PHÂN TÍCH AI OFFLINE (nhấn để mở)</b></summary>\n")
            if v38_protocol_text:
                final_parts.append(v38_protocol_text)
            # V42.9: THÁM TỬ đã nằm trong offline_full_output → không append riêng
            # V42.9 FIX: LUÔN include offline_full_output — chứa Ứng Kỳ Chuyên Sâu,
            # Ám Động, Thần Sát, Không Vong, Tam Hợp, Lục Xung/Hợp, Dịch Mã, Thoán Từ...
            if offline_full_output:
                final_parts.append("\n---")
                final_parts.append(offline_full_output)
            final_parts.append("\n</details>")
            final_parts.append("")
            
            return "\n".join(final_parts)
        else:
            # AI Online không khả dụng → Hiện KếT LUẬN trực tiếp, offline chi tiết ẩn sau
            error_reasons = []
            for log in self.logs:
                if log.get('step') == 'Online AI' and log.get('status') in ['SKIP', 'ERROR']:
                    error_reasons.append(log.get('detail', ''))
            
            error_msg = error_reasons[-1] if error_reasons else "Không có API Key hoặc hết hạn mức"
            
            # === V35.0: BUILD COMPREHENSIVE OFFLINE CONCLUSION — DÙNG weighted_pct ===
            pct_short = weighted_pct  # Từ BƯỚC 6 đã tính (giữ nội bộ)
            
            # V35.0: Dùng weighted_pct (đã tính chính xác) thay vì đếm verdict thô
            _verdicts_list = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict, luc_nham_verdict, thai_at_verdict]
            _cat_count = sum(1 for v in _verdicts_list if v and 'CÁT' in str(v).upper())
            _hung_count = sum(1 for v in _verdicts_list if v and 'HUNG' in str(v).upper())
            
            # V35.0: XÁC ĐỊNH verdict TỪ weighted_pct (chính xác hơn verdict counting)
            if weighted_pct >= 70:
                overall_short = 'ĐẠI CÁT'
                v_icon = '✅'
            elif weighted_pct >= 55:
                overall_short = 'CÁT'
                v_icon = '✅'
            elif weighted_pct >= 45:
                overall_short = 'CÓ THỂ ĐƯỢC — CẦN THẬN TRỌNG' if weighted_pct >= 50 else 'BÌNH'
                v_icon = '🟡'
            elif weighted_pct >= 30:
                overall_short = 'HUNG'
                v_icon = '🔴'
            else:
                overall_short = 'ĐẠI HUNG'
                v_icon = '🔴'
            
            final_parts = []
            
            # V42.9.2: SMART Extract — short verdicts from direct_answer for green box header
            # Key change: For VẠN VẬT HTML blocks → extract ONLY the short summary line
            #             For TUỔI/SỐ LƯỢNG → extract the clean one-liner
            import re as _re_extract
            _offline_short_answer_list = []
            _offline_evidence = []
            if direct_answer:
                for _line in direct_answer.split('\n'):
                    _s = _line.strip()
                    if not _s:
                        continue
                    _s_spaced = _s.replace('<br>', ' ').replace('</div>', ' ')
                    
                    # --- CASE 1: PHÁN QUYẾT (competition/yes-no verdict) ---
                    if 'PHÁN QUYẾT:' in _s:
                        _m = _re_extract.search(r'(?:✅|⚖️|↗️)?\s*PHÁN QUYẾT:.*?(?=</span>|</div>|<br)', _s)
                        if _m:
                            _ans = _m.group(0).replace('**', '').replace('#', '').strip()
                            if not _ans.startswith(('✅', '⚖️', '↗️')): _ans = "✅ " + _ans
                            if _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                        else:
                            _clean_s = _re_extract.sub(r'<[^>]+>', '', _s_spaced)
                            _ans = _clean_s.replace('**', '').replace('#', '').strip()
                            if _ans and _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                    
                    # --- CASE 2: YES/NO quick icons ---
                    elif any(x in _s for x in ['📢', '🟢 CÓ', '🔴 KHÔNG', '🟡 CẦN', '🟢 NÊN', '🔴 KHÔNG NÊN', '🟢 ĐƯỢC', '🟢 TỐT', '🔴 XẤU']):
                        _clean_s = _re_extract.sub(r'<[^>]+>', '', _s_spaced)
                        _ans = _clean_s.replace('**', '').replace('#', '').strip()
                        if _ans and _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                    
                    # --- CASE 3: VẠN VẬT HTML block (LONG) → extract SHORT summary ---
                    elif 'PHÂN TÍCH VẠN VẬT' in _s and '📦 Hành' in _s:
                        # This is the big HTML div — extract only the key info
                        _m_hanh = _re_extract.search(r'📦 Hành (\S+) → ([^<]+)', _s)
                        if _m_hanh:
                            _hanh_name = _m_hanh.group(1)
                            _hanh_sp = _m_hanh.group(2).strip()
                            # Truncate product list to first 3 items
                            _sp_parts = [p.strip() for p in _hanh_sp.split(',')]
                            _sp_short = ', '.join(_sp_parts[:3])
                            if len(_sp_parts) > 3:
                                _sp_short += '...'
                            _ans = f"🔮 Nghề/Ngành: Hành {_hanh_name} → {_sp_short}"
                            if _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                        else:
                            _ans = "🔮 Xem chi tiết Vạn Vật bên dưới"
                            if _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                    
                    # --- CASE 4: TUỔI line (🎂 **TUỔI: Khoảng X tuổi**) ---
                    elif '🎂' in _s and 'TUỔI' in _s.upper():
                        _clean_s = _re_extract.sub(r'<[^>]+>', '', _s_spaced)
                        _ans = _clean_s.replace('**', '').replace('#', '').strip()
                        if _ans and _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                    
                    # --- CASE 5: SỐ LƯỢNG line (👥 **SỐ LƯỢNG: X người**) ---
                    elif '👥' in _s and 'SỐ LƯỢNG' in _s.upper():
                        _clean_s = _re_extract.sub(r'<[^>]+>', '', _s_spaced)
                        _ans = _clean_s.replace('**', '').replace('#', '').strip()
                        if _ans and _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                    
                    # --- CASE 6: Legacy CÂU TRẢ LỜI / 📦 Hành (standalone lines) ---
                    elif 'CÂU TRẢ LỜI' in _s.upper() or '📦 Hành' in _s:
                        _clean_s = _re_extract.sub(r'<[^>]+>', '', _s_spaced)
                        _ans = _clean_s.replace('**', '').replace('#', '').strip()
                        # Remove "CÂU TRẢ LỜI:" prefix
                        _ans = _re_extract.sub(r'CÂU TRẢ LỜI\s*:?\s*', '', _ans).strip()
                        if _ans and len(_ans) > 2 and _ans not in _offline_short_answer_list:
                            _offline_short_answer_list.append(_ans)
                    
                    # --- CASE 7: Generic verdict icons (short lines only, skip evidence) ---
                    elif _s.startswith(('🟢', '🔴', '🟡', '✅', '⚖️', '↗️')) and 5 < len(_s) < 200:
                        # Skip evidence/detail lines
                        if any(skip in _s for skip in ['Thuận lợi (', 'Bất lợi (', 'Thần ', 'Thần Trực', '→ Huynh', '→ Quan', '→ Thê', '→ Phụ', '→ Tử']):
                            pass
                        else:
                            _clean_s = _re_extract.sub(r'<[^>]+>', '', _s_spaced)
                            _ans = _clean_s.replace('**', '').replace('#', '').strip()
                            if _ans and len(_ans) < 100 and _ans not in _offline_short_answer_list: _offline_short_answer_list.append(_ans)
                    
                    # --- Evidence lines (top 3) ---
                    elif len(_offline_evidence) < 3:
                        if _s.startswith(('- ✅', '- 🔴', '- ⚠️', '- 📌', '- 📊', '- 💡')):
                            _offline_evidence.append(_s)

            _offline_short_answer = "<br>".join(_offline_short_answer_list) if _offline_short_answer_list else ""
            
            if not _offline_short_answer:
                # V42.9.2: MULTI-INTENT FALLBACK — detect ALL intent types INDEPENDENTLY
                # Bug fix: Old code used if/elif → only first intent got answered
                # New code: Each intent is independent → ALL get collected into _fb_parts[]
                _q_lower_off2 = question.lower()
                _is_competition_off = _is_competition_question(question)
                _fb_parts = []  # Collect ALL matching intent answers
                
                _LT_HANH_FB = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
                _hanh_fb = _LT_HANH_FB.get(dung_than, 'Thổ')
                _HANH_SP_FB = {'Kim': 'Kim loại/Máy móc/Linh kiện', 'Mộc': 'Gỗ/Vải/Nông sản/Giấy', 
                             'Thủy': 'Nước/Chất lỏng/Hải sản/Hóa chất', 'Hỏa': 'Điện tử/Năng lượng/Thực phẩm', 
                             'Thổ': 'Gạch/Gốm sứ/Vật liệu XD/Nông sản'}
                
                if _is_competition_off:
                    # COMPETITION — Extract kết quả thắng/thua
                    _side_a, _side_b = _extract_two_sides(question)
                    _the_score = 0
                    _ung_score = 0
                    for _f in (v23_lh_factors or []):
                        if '+' in str(_f):
                            try:
                                import re as _re_comp
                                _m = _re_comp.search(r'\+(\d+)', str(_f))
                                if _m: _the_score += int(_m.group(1))
                            except: _the_score += 3
                        elif '-' in str(_f):
                            try:
                                import re as _re_comp2
                                _m2 = _re_comp2.search(r'-(\d+)', str(_f))
                                if _m2: _ung_score += int(_m2.group(1))
                            except: _ung_score += 3
                    _net = _the_score - _ung_score
                    if _net > 3:
                        _fb_parts.append(f"⚽ {_side_a} THẮNG ✅ (Chênh: +{_net})")
                    elif _net < -3:
                        _fb_parts.append(f"⚽ {_side_b} THẮNG ✅ (Chênh: {_net})")
                    else:
                        _fb_parts.append(f"⚽ HÒA ⚖️ — {_side_a} ≈ {_side_b} (Chênh: {_net:+d})")
                
                # NGHỀ GÌ / CÁI GÌ — independent
                if any(k in _q_lower_off2 for k in ['cái gì', 'loại gì', 'sản xuất gì', 'làm gì', 'sản phẩm gì',
                    'buôn bán gì', 'kinh doanh gì', 'nghề gì', 'ngành gì', 'gì vậy', 'gì đây',
                    'bán gì', 'trồng gì', 'nuôi gì', 'mua gì', 'bằng gì', 'sản xuất cái']):
                    _fb_parts.append(f"🔮 Nghề/Ngành: Hành {_hanh_fb} → {_HANH_SP_FB.get(_hanh_fb, '?')}")
                
                # TUỔI — independent
                if any(k in _q_lower_off2 for k in ['bao nhiêu tuổi', 'tuổi', 'năm tuổi']):
                    # Tính tuổi từ age_numbers nếu có
                    if age_numbers:
                        _age_nums = [n for _, n in age_numbers]
                        _age_avg = int(sum(_age_nums) / len(_age_nums)) if _age_nums else 0
                        _fb_parts.append(f"🎂 Tuổi: Khoảng {_age_avg} tuổi")
                    else:
                        # Ước tính từ Ngũ Hành
                        _HD_AGE = {'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 10)}
                        _hd_age = _HD_AGE.get(_hanh_fb, (5, 10))
                        _age_est = _hd_age[1] * 5 if weighted_pct >= 55 else _hd_age[0] * 5
                        _fb_parts.append(f"🎂 Tuổi: Khoảng {_age_est} tuổi")
                
                # BAO NHIÊU / MẤY — independent
                if any(k in _q_lower_off2 for k in ['bao nhiêu', 'mấy người', 'mấy cái', 'mấy đứa', 'mấy anh', 'mấy chị', 'số lượng', 'mấy tầng', 'mấy con', 'mấy']):
                    if count_numbers:
                        _cnt_nums = [n for _, n in count_numbers]
                        _cnt_avg = int(round(sum(_cnt_nums) / len(_cnt_nums))) if _cnt_nums else 0
                        _fb_parts.append(f"👥 Số lượng: {_cnt_avg} người")
                    else:
                        _HD_CNT = {'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 10)}
                        _hd_cnt = _HD_CNT.get(_hanh_fb, (5, 10))
                        _cnt_est = _hd_cnt[0] if weighted_pct < 60 else _hd_cnt[1]
                        _fb_parts.append(f"👥 Số lượng: {_cnt_est} người")
                
                # Ở ĐÂU — independent
                if any(k in _q_lower_off2 for k in ['ở đâu', 'hướng nào', 'phương nào', 'chỗ nào', 'nơi nào']):
                    _HANH_HUONG_FB = {'Kim': 'HƯỚNG TÂY', 'Mộc': 'HƯỚNG ĐÔNG', 'Thủy': 'HƯỚNG BẮC', 'Hỏa': 'HƯỚNG NAM', 'Thổ': 'TRUNG TÂM'}
                    _fb_parts.append(f"🧭 {_HANH_HUONG_FB.get(_hanh_fb, '?')} (Hành {_hanh_fb})")
                
                # KHI NÀO — independent
                if any(k in _q_lower_off2 for k in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm']):
                    try:
                        from xem_ngay_dep import _jdn as _jdn_h2
                        import datetime as _dt_h2
                        _h2 = _hanh_fb
                        _UKC2 = {'Kim': [8,9], 'Mộc': [2,3], 'Thủy': [0,11], 'Hỏa': [6,5], 'Thổ': [4,10,1,7]}
                        _SINH2 = {'Kim': 'Thổ', 'Mộc': 'Thủy', 'Thủy': 'Kim', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa'}
                        _tc2 = _UKC2.get(_h2, [4]) if weighted_pct >= 55 else _UKC2.get(_SINH2.get(_h2, 'Thổ'), [4])
                        _CHIS2 = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                        _CANS2 = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                        _CGW2 = {'Tý':'23h-1h','Sửu':'1h-3h','Dần':'3h-5h','Mão':'5h-7h','Thìn':'7h-9h','Tị':'9h-11h',
                                 'Ngọ':'11h-13h','Mùi':'13h-15h','Thân':'15h-17h','Dậu':'17h-19h','Tuất':'19h-21h','Hợi':'21h-23h'}
                        _td2 = _dt_h2.date.today()
                        for _o2 in range(1, 200):
                            _dd2 = _td2 + _dt_h2.timedelta(days=_o2)
                            _jj2 = _jdn_h2(_dd2.day, _dd2.month, _dd2.year)
                            _cc2 = (_jj2 + 1) % 12
                            if _cc2 in _tc2:
                                _cn2 = _CANS2[(_jj2 + 9) % 10]
                                _chn2 = _CHIS2[_cc2]
                                _TW2 = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật']
                                _tw2 = _TW2[_dd2.weekday()]
                                _gt2 = _CGW2.get(_chn2, '')
                                _fb_parts.append(f"📆 {_dd2.day:02d}/{_dd2.month:02d}/{_dd2.year} ({_tw2}) lúc {_gt2}")
                                break
                    except Exception:
                        _fb_parts.append(f"⏳ Xem Ứng Kỳ chi tiết bên dưới")
                
                # Build final answer from collected parts
                if _fb_parts:
                    _offline_short_answer = "<br>".join(_fb_parts)
                elif overall_short in ('CÁT', 'ĐẠI CÁT'):
                    _offline_short_answer = f"{v_icon} CÓ — THUẬN LỢI ({weighted_pct}%)"
                elif overall_short in ('HUNG', 'ĐẠI HUNG'):
                    _offline_short_answer = f"{v_icon} KHÔNG — BẤT LỢI ({weighted_pct}%)"
                else:
                    _offline_short_answer = f"{v_icon} CẦN CÂN NHẮC — {overall_short} ({weighted_pct}%)"
            
            # === V42.0: CẢNH BÁO PHẢN/PHỤC NGÂM ===
            try:
                _ppn_warning = _build_phan_phuc_ngam_warning(chart_data, luc_hao_data)
                if _ppn_warning:
                    final_parts.append(_ppn_warning)
            except Exception:
                pass
            
            # === V42.1: CẢNH BÁO NGUYỆT PHÁ ===
            try:
                _lh_dt_chi_np2 = ''
                _lh_chi_thang_np2 = ''
                if luc_hao_data:
                    _lh_haos_np2 = luc_hao_data.get('ban', {}).get('haos', luc_hao_data.get('haos', []))
                    _lh_chi_thang_np2 = luc_hao_data.get('chi_thang', '')
                    if _lh_haos_np2 and dung_than:
                        for _h_np2 in _lh_haos_np2:
                            if _h_np2.get('luc_than', '') == dung_than:
                                _lh_dt_chi_np2 = _h_np2.get('chi', '')
                                break
                    if _lh_dt_chi_np2 and _lh_chi_thang_np2:
                        _, _np_html_offline = _build_nguyet_pha_warning(
                            _lh_dt_chi_np2, _lh_chi_thang_np2,
                            dung_than_name=dung_than or 'Dụng Thần'
                        )
                        if _np_html_offline:
                            final_parts.append(_np_html_offline)
            except Exception:
                pass
            
            # ═══════════════════════════════════════════════════════════
            # V42.9: Ô XANH LÁ — KẾT LUẬN AI OFFLINE (DUY NHẤT)
            # ═══════════════════════════════════════════════════════════
            _evidence_html = ""
            if _offline_evidence:
                _evidence_html = '<div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.2);">'
                for _ev in _offline_evidence:
                    _evidence_html += f'<div style="font-size:1em;color:#d1fae5;margin:4px 0;">{_ev}</div>'
                _evidence_html += '</div>'
            
            # V42.9: Competition → thêm chi tiết 2 đội vào header
            _comp_detail_html = ""
            _is_comp_final = _is_competition_question(question)
            if _is_comp_final:
                _sa, _sb = _extract_two_sides(question)
                _comp_detail_html = (
                    f'<div style="margin-top:14px;padding:14px;background:rgba(0,0,0,0.2);border-radius:10px;">'
                    f'<div style="font-size:1.15em;color:#6ee7b7;font-weight:700;margin-bottom:8px;">📊 Phương pháp: Thế vs Ứng</div>'
                    f'<div style="color:#d1fae5;font-size:1.05em;">• Lục Hào: Thế = {_sa}, Ứng = {_sb}</div>'
                    f'<div style="color:#d1fae5;font-size:1.05em;">• Kỳ Môn: Nhật Can (Chủ = {_sa}), Thời Can (Khách = {_sb})</div>'
                    f'<div style="color:#d1fae5;font-size:1.05em;">• Mai Hoa: Thể Quái = {_sa}, Dụng Quái = {_sb}</div>'
                    f'</div>'
                )
            
            final_parts.append(
                f'<div style="background:linear-gradient(135deg,#064e3b,#065f46);padding:28px;border-radius:16px;margin:16px 0;border:3px solid #34d399;box-shadow:0 4px 25px rgba(52,211,153,0.4);">'
                f'<div style="font-size:1.2em;font-weight:700;color:#6ee7b7;margin-bottom:10px;">🖥️ KẾT LUẬN AI OFFLINE — THIÊN CƠ ĐẠI SƯ V42.9</div>'
                f'<div style="font-size:2em;font-weight:900;color:#ffffff;line-height:1.3;margin-bottom:8px;">{_offline_short_answer}</div>'
                f'<div style="font-size:1.05em;color:#a7f3d0;">📊 Điểm: <b>{weighted_pct}%</b> | DT: <b>{dung_than}</b> | KM: {ky_mon_verdict} | LH: {luc_hao_verdict} | MH: {mai_hoa_verdict}</div>'
                + _comp_detail_html
                + _evidence_html
                + f'</div>'
            )
            final_parts.append("")
            
            # ═══════════════════════════════════════════════════════════
            # V42.9: 1 COLLAPSE DUY NHẤT — TẤT CẢ chi tiết
            # KHÔNG có section nào hiển thị bên ngoài collapse
            # ═══════════════════════════════════════════════════════════
            final_parts.append("\n<details>")
            final_parts.append(f"<summary><b>📖 XEM CHI TIẾT PHÂN TÍCH AI OFFLINE (nhấn để mở)</b></summary>\n")
            
            # 1. Protocol 27 bước (NẾU CÓ)
            if v38_protocol_text:
                final_parts.append(v38_protocol_text)
            else:
                final_parts.append(f"## {v_icon} KẾT LUẬN: {overall_short} (Điểm Tổng Hợp: {weighted_pct}%)")
            
            # V42.9: THÁM TỬ đã nằm trong offline_full_output
            # KHÔNG append direct_answer riêng → tránh trùng lặp
            
            # 3. VẠN VẬT CỤ THỂ (CHỈ cho câu hỏi KHÔNG PHẢI competition)
            if not _is_comp_final:
                vv_cu_the_kl = _get_van_vat_cu_the(hanh_dt_v22, unified_v22.get('tier_key', 'TRUNG_BÌNH') if unified_v22 else 'TRUNG_BÌNH')
                if vv_cu_the_kl and hanh_dt_v22:
                    final_parts.append(f"\n### 🎯 VẠN VẬT CỤ THỂ ({hanh_dt_v22} × {unified_v22['tier_data']['cap'] if unified_v22 else '?'})")
                    final_parts.append(f"- 🔮 **Đồ vật:** {vv_cu_the_kl.get('do_vat', '?')}")
                    final_parts.append(f"- 🏠 **Nhà cửa:** {vv_cu_the_kl.get('nha_cua', '?')}")
                    final_parts.append(f"- 🧑 **Người:** {vv_cu_the_kl.get('nguoi', '?')}")
                    final_parts.append(f"- 🏥 **Bệnh:** {vv_cu_the_kl.get('benh', '?')}")
            
            # 4. V31 Sơ đồ Master
            if v31_master_diagram:
                final_parts.append(f"\n### 🏆 SĐ MASTER: DỤNG THẦN → SUY VƯỢNG → VẠN VẬT")
                final_parts.append(f"```")
                final_parts.append(v31_master_diagram)
                final_parts.append(f"```")
                final_parts.append(f"**📊 CÔNG THỨC:** {v31_master_info.get('formula_detail', '?')}")
                final_parts.append(f"**🎯 KẾT LUẬN MASTER:** {v31_master_info.get('conclusion', '?')}")
            
            # 5. V31 Sơ đồ câu hỏi
            if v31_question_diagram and v31_diagram_id != 'SD0':
                final_parts.append(f"\n### 📐 CHÚ GIẢI: {v31_question_info.get('diagram_name', 'Sơ Đồ')}")
                final_parts.append(f"```")
                final_parts.append(v31_question_diagram)
                final_parts.append(f"```")
                final_parts.append(f"**📊 CÔNG THỨC:** {v31_question_info.get('formula', '?')}")
                final_parts.append(f"**🎯 KẾT LUẬN:** {v31_question_info.get('conclusion', '?')}")
            
            # 6. V32.5: Sơ đồ tương tác 6PP
            try:
                v325_interaction = self._build_factor_interaction_map(
                    chart_data=chart_data,
                    luc_hao_data=luc_hao_data,
                    mai_hoa_data=mai_hoa_data,
                    dung_than=dung_than,
                    hanh_dt=hanh_dt_v22,
                    question=question,
                    km_verdict=ky_mon_verdict or 'BÌNH',
                    lh_verdict=luc_hao_verdict or 'BÌNH',
                    mh_verdict=mai_hoa_verdict or 'BÌNH',
                    ln_verdict=luc_nham_verdict or 'BÌNH',
                    ta_verdict=thai_at_verdict or 'BÌNH'
                )
                if v325_interaction:
                    final_parts.append("\n### 🔮 SƠ ĐỒ TƯƠNG TÁC 6PP CHI TIẾT")
                    final_parts.append(v325_interaction)
            except Exception as e:
                self.log_step("V32.5", "INTERACTION_ERR", str(e)[:100])
            
            # 7. Thống kê yếu tố
            all_factors = v24_km_factors + v23_lh_factors + v24_mh_factors + v24_tb_factors + v24_ln_factors + v24_ta_factors
            if all_factors:
                final_parts.append(f"\n### 📋 THỐNG KÊ CHI TIẾT CÁC YẾU TỐ ({len(all_factors)})")
                for f in all_factors:
                    if '+' in f:
                        final_parts.append(f"- ✅ **THUẬN LỢI:** {f}")
                    elif '-' in f:
                        final_parts.append(f"- ⚠️ **BẤT LỢI:** {f}")
                    else:
                        final_parts.append(f"- ℹ️ **THÔNG TIN:** {f}")
            
            # 8. V26.2: Full offline output (gốc)
            if offline_full_output:
                final_parts.append("\n---")
                final_parts.append(offline_full_output)
            
            final_parts.append("\n</details>")
            final_parts.append(f"\n💡 Để dùng AI thông minh hơn, nhập API Key tại [Google AI Studio](https://aistudio.google.com/).")
            return "\n".join(final_parts)


    def _custom_reasoning(self, question, dung_than, chart_data):
        """Suy luận riêng bằng Python khi câu hỏi không trùng 220+ chủ đề"""
        lines = []
        q = question.lower()
        
        # 1. Phân loại câu hỏi theo 12 nhóm
        CATEGORIES = {
            "TÀI CHÍNH": {
                "keywords": ["tiền", "vốn", "lương", "nợ", "vay", "đầu tư", "lời", "lỗ", "mua", "bán", "giá", "thu nhập", "chi phí", "lợi nhuận", "bitcoin", "coin", "chứng khoán", "cổ phiếu", "vàng"],
                "dung_than": ["Sinh Môn", "Mậu", "Thê Tài"],
                "sao_cua_focus": {"sao": "Thiên Nhậm", "cua": "Sinh Môn", "than": "Trực Phù"},
                "ngu_hanh_tot": "Thổ",
                "goi_y": "Xem Sinh Môn (tài lộc) có vượng không, Mậu (vốn) ở cung nào, Cung bản thân được Sinh hay Khắc"
            },
            "SỨC KHỎE": {
                "keywords": ["bệnh", "ốm", "khỏe", "đau", "thuốc", "bác sĩ", "phẫu thuật", "mổ", "viện", "khám", "sức khỏe", "tiểu đường", "huyết áp", "ung thư", "covid"],
                "dung_than": ["Thiên Nhuế", "Thiên Tâm", "Ất"],
                "sao_cua_focus": {"sao": "Thiên Tâm", "cua": "Sinh Môn", "than": "Trực Phù"},
                "ngu_hanh_tot": "Mộc",
                "goi_y": "Thiên Nhuế = Bệnh, Thiên Tâm = Bác sĩ, Ất = Thuốc. Xem 3 yếu tố này ở cung nào, vượng/suy"
            },
            "TÌNH CẢM": {
                "keywords": ["yêu", "người yêu", "vợ", "chồng", "hẹn hò", "tình", "cưới", "chia tay", "ly hôn", "ngoại tình", "crush", "thích", "hôn nhân", "đám cưới"],
                "dung_than": ["Lục Hợp", "Ất", "Canh"],
                "sao_cua_focus": {"sao": "Thiên Phụ", "cua": "Hưu Môn", "than": "Lục Hợp"},
                "ngu_hanh_tot": "Mộc",
                "goi_y": "Ất = Nữ, Canh = Nam, Lục Hợp = Hôn nhân. Xem Can Ngày-Giờ có hợp không, Lục Hợp vượng/suy"
            },
            "CÔNG VIỆC": {
                "keywords": ["việc", "công ty", "sếp", "lương", "thăng", "nghỉ", "sa thải", "tuyển", "phỏng vấn", "cv", "career", "nghề", "chức", "đồng nghiệp"],
                "dung_than": ["Khai Môn", "Trực Phù", "Can Ngày"],
                "sao_cua_focus": {"sao": "Thiên Tâm", "cua": "Khai Môn", "than": "Trực Phù"},
                "ngu_hanh_tot": "Kim",
                "goi_y": "Khai Môn = Công việc, Trực Phù = Sếp/Lãnh đạo. Xem Cung chứa Khai Môn + quan hệ Can Ngày"
            },
            "HỌC TẬP": {
                "keywords": ["học", "thi", "điểm", "đỗ", "trượt", "trường", "đại học", "ielts", "bằng", "chứng chỉ", "nghiên cứu", "luận văn"],
                "dung_than": ["Cảnh Môn", "Đinh", "Thiên Phụ"],
                "sao_cua_focus": {"sao": "Thiên Phụ", "cua": "Cảnh Môn", "than": "Trực Phù"},
                "ngu_hanh_tot": "Hỏa",
                "goi_y": "Cảnh Môn = Bài thi/Kết quả, Đinh = Điểm, Thiên Phụ = Kiến thức. Cảnh Môn vượng → Đỗ"
            },
            "PHÁP LÝ": {
                "keywords": ["kiện", "tòa", "luật", "pháp", "tù", "bắt", "phạt", "tranh chấp", "hợp đồng", "bản quyền"],
                "dung_than": ["Khai Môn", "Kinh Môn", "Canh"],
                "sao_cua_focus": {"sao": "Thiên Tâm", "cua": "Khai Môn", "than": "Bạch Hổ"},
                "ngu_hanh_tot": "Kim",
                "goi_y": "Khai Môn = Tòa, Kinh Môn = Kiện tụng, Canh = Đối phương. Can Ngày thắng Canh → Thắng kiện"
            },
            "NHÀ ĐẤT": {
                "keywords": ["nhà", "đất", "phòng", "thuê", "xây", "sửa", "phong thủy", "hướng", "chung cư", "căn hộ"],
                "dung_than": ["Sinh Môn", "Tử Môn", "Can Ngày"],
                "sao_cua_focus": {"sao": "Thiên Nhậm", "cua": "Sinh Môn", "than": "Cửu Địa"},
                "ngu_hanh_tot": "Thổ",
                "goi_y": "Sinh Môn = Nhà, Tử Môn = Đất. Cửu Địa = Nền móng. Xem Sinh Môn vượng/suy ở cung nào"
            },
            "DI CHUYỂN": {
                "keywords": ["đi", "về", "bay", "xe", "đường", "du lịch", "chuyến", "visa", "xuất cảnh", "nhập cảnh", "lái"],
                "dung_than": ["Mã Tinh", "Khai Môn", "Can Ngày"],
                "sao_cua_focus": {"sao": "Thiên Xung", "cua": "Khai Môn", "than": "Cửu Thiên"},
                "ngu_hanh_tot": "Mộc",
                "goi_y": "Mã Tinh = Sự di chuyển, Khai Môn = Hướng đi. Cửu Thiên = Xuất hành. Xem cung Mã Tinh"
            },
            "TÂM LINH": {
                "keywords": ["cúng", "chùa", "thần", "ma", "mộ", "tâm linh", "xăm", "quẻ", "bùa", "thiền", "tu", "phật"],
                "dung_than": ["Trực Phù", "Thiên Tâm", "Đằng Xà"],
                "sao_cua_focus": {"sao": "Thiên Tâm", "cua": "Khai Môn", "than": "Trực Phù"},
                "ngu_hanh_tot": "Thủy",
                "goi_y": "Trực Phù = Thần linh, Đằng Xà = Quỷ thần. Xem Trực Phù vượng → Được phù hộ"
            },
            "GIA ĐÌNH": {
                "keywords": ["cha", "mẹ", "con", "anh", "chị", "em", "gia đình", "bố", "ông", "bà", "cháu"],
                "dung_than": ["Can Năm", "Lục Hợp", "Can Ngày"],
                "sao_cua_focus": {"sao": "Thiên Nhậm", "cua": "Hưu Môn", "than": "Lục Hợp"},
                "ngu_hanh_tot": "Thổ",
                "goi_y": "Can Năm = Cha mẹ, Can Tháng = Anh em, Can Giờ = Con cái. Lục Hợp = Gắn kết gia đình"
            },
            "MẤT MÁT": {
                "keywords": ["mất", "trộm", "lừa", "cướp", "tìm", "lạc", "thất lạc", "đánh rơi"],
                "dung_than": ["Huyền Vũ", "Can Giờ", "Thương Môn"],
                "sao_cua_focus": {"sao": "Thiên Bồng", "cua": "Thương Môn", "than": "Huyền Vũ"},
                "ngu_hanh_tot": "Thủy",
                "goi_y": "Huyền Vũ = Kẻ trộm, Can Giờ = Vật mất. Xem Cung Huyền Vũ → Hướng kẻ gian, Cung Can Giờ → Hướng tìm"
            },
            "CHUNG": {
                "keywords": [],
                "dung_than": ["Can Ngày", "Can Giờ", "Trực Phù"],
                "sao_cua_focus": {"sao": "Thiên Tâm", "cua": "Khai Môn", "than": "Trực Phù"},
                "ngu_hanh_tot": "Thổ",
                "goi_y": "Xem Can Ngày (bản thân) vs Can Giờ (sự việc). Cung nào vượng hơn → Bên đó lợi thế"
            }
        }
        
        # 2. Tìm nhóm phù hợp nhất
        best_cat = "CHUNG"
        best_score = 0
        for cat_name, cat_data in CATEGORIES.items():
            score = sum(1 for kw in cat_data["keywords"] if kw in q)
            if score > best_score:
                best_score = score
                best_cat = cat_name
        
        cat = CATEGORIES[best_cat]
        
        # 3. Output suy luận
        lines.append(f"- **Nhóm suy luận:** {best_cat}")
        lines.append(f"- **Dụng Thần (suy luận):** {', '.join(cat['dung_than'])}")
        lines.append(f"- **Sao trọng tâm:** {cat['sao_cua_focus']['sao']}")
        lines.append(f"- **Cửa trọng tâm:** {cat['sao_cua_focus']['cua']}")
        lines.append(f"- **Thần trọng tâm:** {cat['sao_cua_focus']['than']}")
        lines.append(f"- **Ngũ Hành thuận lợi:** {cat['ngu_hanh_tot']}")
        lines.append(f"- **💡 Gợi ý phân tích:** {cat['goi_y']}")
        
        # 4. Phân tích SÂU từ chart_data (V7.0 Deep Reasoning)
        confidence = 50  # Base confidence
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            can_gio = chart_data.get('can_gio', '')
            hanh_bn = CAN_NGU_HANH.get(can_ngay, '')
            hanh_tot = cat['ngu_hanh_tot']
            
            if hanh_bn:
                rel = _ngu_hanh_relation(hanh_bn, hanh_tot)
                lines.append(f"- **Bản thân ({can_ngay}/{hanh_bn}) vs Ngũ Hành thuận ({hanh_tot}):** {rel}")
                if 'ĐƯỢC SINH' in rel or 'Tỷ' in rel:
                    confidence += 15
                elif 'BỊ KHẮC' in rel:
                    confidence -= 15
                
                # Vạn Vật cho hành bản thân
                vvlt = get_ngu_hanh_tuong(hanh_bn)
                if vvlt:
                    lines.append(f"\n  **📊 Vạn Vật ({hanh_bn}):**")
                    for vl in vvlt.split('\n')[1:4]:
                        lines.append(f"  {vl}")
            
            # 4b. Cách Cục (Can Thiên/Địa)
            can_thien_ban = chart_data.get('can_thien_ban', {})
            chu_cung = None
            for cung_num, can_val in can_thien_ban.items():
                if can_val == can_ngay:
                    chu_cung = int(cung_num) if cung_num else None
                    break
            
            if chu_cung:
                thien_ban = chart_data.get('thien_ban', {})
                nhan_ban = chart_data.get('nhan_ban', {})
                than_ban = chart_data.get('than_ban', {})
                sao = thien_ban.get(chu_cung, '')
                cua = nhan_ban.get(chu_cung, '')
                than = than_ban.get(chu_cung, '')
                
                lines.append(f"\n  **🔍 Phân tích Cung Bản Thân (Cung {chu_cung}):**")
                lines.append(f"  - Sao: **{sao}** | Cửa: **{cua}** | Thần: **{than}**")
                
                # Đánh giá Sao/Cửa
                sao_ok = any(s in str(sao) for s in ['Tâm', 'Nhậm', 'Phụ', 'Xung'])
                cua_ok = any(c in str(cua) for c in CUA_CAT)
                if sao_ok:
                    lines.append(f"  - Sao **CÁT** ✅")
                    confidence += 10
                if cua_ok:
                    lines.append(f"  - Cửa **CÁT** ✅")
                    confidence += 10
                
                # Quái tượng Vạn Vật
                quai = QUAI_TUONG.get(chu_cung, '')
                if quai:
                    vvlt_quai = get_bat_quai_tuong(quai)
                    if vvlt_quai:
                        lines.append(f"\n  **📊 Vạn Vật ({quai}):**")
                        for vl in vvlt_quai.split('\n')[1:5]:
                            lines.append(f"  {vl}")
        
        # 5. Confidence score
        confidence = max(10, min(95, confidence))
        lines.append(f"\n- **📈 Độ tin cậy suy luận: {confidence}%**")
        
        # 6. Lời khuyên theo nhóm (V7.0)
        advice_map = {
            "TÀI CHÍNH": "Cẩn thận với quyết định tài chính lớn, nên tham khảo thêm.",
            "SỨC KHỎE": "Nên đi khám bác sĩ để chắc chắn, không nên chủ quan.",
            "TÌNH CẢM": "Lắng nghe trái tim nhưng cũng cần lý trí phân tích.",
            "CÔNG VIỆC": "Chuẩn bị kỹ và chờ thời cơ phù hợp để hành động.",
            "HỌC TẬP": "Kiên trì ôn luyện, kết quả sẽ đến.",
            "PHÁP LÝ": "Nên tìm luật sư tư vấn, chuẩn bị chứng cứ đầy đủ.",
            "NHÀ ĐẤT": "Xem kỹ giấy tờ pháp lý và phong thủy trước khi quyết định.",
            "DI CHUYỂN": "Chọn giờ đẹp xuất hành, chuẩn bị kỹ hành lý.",
            "TÂM LINH": "Giữ tâm thanh tịnh, thành tâm cầu nguyện.",
            "GIA ĐÌNH": "Hòa khí sinh tài, nhẫn nhịn để gia đình êm ấm.",
            "MẤT MÁT": "Tìm theo hướng được chỉ dẫn, báo cơ quan nếu cần.",
            "CHUNG": "Quan sát thêm tình hình trước khi đưa ra quyết định."
        }
        lines.append(f"- **💬 Lời khuyên:** {advice_map.get(best_cat, '')}")
        
        # 7. AUTO-LEARN: Lưu câu hỏi mới vào database (V7.0)
        _save_learned_topic(
            question=question,
            category=best_cat,
            dung_than_list=cat['dung_than'],
            goi_y=cat['goi_y']
        )
        lines.append(f"- 🧠 **Auto-Learn:** Đã lưu câu hỏi này để tra cứu lần sau!")
        
        return "\n".join(lines)

    # ===========================
    # KỲ MÔN ANALYSIS (V8.0 — Deep Interpretation)
    # ===========================
    def _analyze_ky_mon(self, chart_data, dung_than, is_age, is_find, is_count=False, question=""):
        lines = []
        verdict = "BÌNH"
        reason = ""
        age_num = None
        count_num = None
        
        qmdg_input = chart_data if isinstance(chart_data, dict) else {}
        
        # Tìm cung bản thân (Can Ngày) và sự việc (Can Giờ)
        can_ngay = qmdg_input.get('can_ngay', '')
        can_gio = qmdg_input.get('can_gio', '')
        can_thang = qmdg_input.get('can_thang', '')
        chu_cung = None
        sv_cung = None
        thang_cung = None  # V8.0: Cung Can Tháng (anh chị em)
        
        can_thien_ban = qmdg_input.get('can_thien_ban', {})
        for cung_num, can_val in can_thien_ban.items():
            cn = int(cung_num) if cung_num else None
            if can_val == can_ngay:
                chu_cung = cn
            if can_val == can_gio:
                sv_cung = cn
            if can_thang and can_val == can_thang:
                thang_cung = cn
        
        # V8.1: Xử lý "Giáp" ẩn — trong QMDG, Giáp luôn ẩn dưới Mậu
        if not chu_cung and can_ngay == 'Giáp':
            for cung_num, can_val in can_thien_ban.items():
                if can_val == 'Mậu':
                    chu_cung = int(cung_num) if cung_num else None
                    break
        
        # V8.1: Fallback — nếu vẫn không tìm được, dùng cung 5 (Trung Cung)
        if not chu_cung and can_thien_ban:
            chu_cung = 5  # Trung Cung — fallback
        
        # V8.1: TỔNG QUAN 9 CUNG (hiển thị trước khi phân tích chi tiết)
        thien_ban = qmdg_input.get('thien_ban', {})
        nhan_ban = qmdg_input.get('nhan_ban', {})
        than_ban = qmdg_input.get('than_ban', {})
        dia_ban = qmdg_input.get('dia_ban') or qmdg_input.get('dia_can', {})
        
        if thien_ban:
            lines.append(f"**📊 TỔNG QUAN 9 CUNG:**")
            for cn_i in range(1, 10):
                if cn_i == 5:
                    lines.append(f"  Cung 5: *(Trung Cung)* — không xếp Sao/Cửa/Thần")
                    continue
                s = thien_ban.get(cn_i, thien_ban.get(str(cn_i), '?'))
                c = nhan_ban.get(cn_i, nhan_ban.get(str(cn_i), '?'))
                t = than_ban.get(cn_i, than_ban.get(str(cn_i), '?'))
                ct = can_thien_ban.get(cn_i, can_thien_ban.get(str(cn_i), '?'))
                marker = ""
                if cn_i == chu_cung:
                    marker = " ← **BẢN THÂN**"
                elif cn_i == sv_cung:
                    marker = " ← **SỰ VIỆC**"
                lines.append(f"  Cung {cn_i}: Sao {s} | Cửa {c} | Thần {t} | Can {ct}{marker}")
            lines.append("")
        
        # V42.2: BẢNG NHÂN BÀN (BÁT MÔN) RÕ RÀNG
        if nhan_ban:
            lines.append(f"**🚪 NHÂN BÀN (Bát Môn):**")
            nb_row = []
            for cn_i in range(1, 10):
                if cn_i == 5:
                    nb_row.append("5: —")
                    continue
                c = nhan_ban.get(cn_i, nhan_ban.get(str(cn_i), '?'))
                nb_row.append(f"{cn_i}:{c}")
            lines.append("  " + " | ".join(nb_row))
            lines.append("")
        
        # V42.2: BẢNG THẦN BÀN (BÁT THẦN) RÕ RÀNG
        if than_ban:
            lines.append(f"**👁️ THẦN BÀN (Bát Thần):**")
            tb_row = []
            for cn_i in range(1, 10):
                if cn_i == 5:
                    tb_row.append("5: —")
                    continue
                t = than_ban.get(cn_i, than_ban.get(str(cn_i), '?'))
                tb_row.append(f"{cn_i}:{t}")
            lines.append("  " + " | ".join(tb_row))
            lines.append("")
        
            # V42.0: BẢNG VƯỢNG/SUY CỬU TINH + BÁT MÔN THEO MÙA
            try:
                _lenh_result_km = _get_lenh_thang_hanh()
                if isinstance(_lenh_result_km, tuple):
                    _lenh_hanh_km = _lenh_result_km[0]
                else:
                    _lenh_hanh_km = _lenh_result_km
                if _lenh_hanh_km:
                    _seasonal_table = _build_seasonal_strength_table(thien_ban, nhan_ban, _lenh_hanh_km)
                    if _seasonal_table:
                        lines.append(_seasonal_table)
                        lines.append("")
            except Exception:
                pass
            
            # V42.1: GÓC NHÌN CHIẾN LƯỢC THIÊN-ĐỊA-NHÂN-THẦN
            try:
                _lenh_hanh_tdnt = _lenh_hanh_km if '_lenh_hanh_km' in dir() else None
                if not _lenh_hanh_tdnt:
                    _lr = _get_lenh_thang_hanh()
                    _lenh_hanh_tdnt = _lr[0] if isinstance(_lr, tuple) else _lr
                if _lenh_hanh_tdnt and chu_cung:
                    _tdnt_view = _build_thien_dia_nhan_than(
                        thien_ban, nhan_ban, than_ban,
                        chu_cung, sv_cung, _lenh_hanh_tdnt
                    )
                    if _tdnt_view:
                        lines.append(_tdnt_view)
                        lines.append("")
            except Exception:
                pass
        
        if chu_cung:
            score = 0
            reasons_list = []
            sao = thien_ban.get(chu_cung, '?')
            cua = nhan_ban.get(chu_cung, '?')
            than = than_ban.get(chu_cung, '?')
            hanh_cung = CUNG_NGU_HANH.get(chu_cung, '?')
            hanh_can = CAN_NGU_HANH.get(can_ngay, '?')
            quai = QUAI_TUONG.get(chu_cung, '?')
            
            relation = _ngu_hanh_relation(hanh_can, hanh_cung)
            
            lines.append(f"- **Bản thân** (Can Ngày **{can_ngay}**) tại **Cung {chu_cung} ({quai})**")
            lines.append(f"  - Hành Can: {hanh_can} | Hành Cung: {hanh_cung} → {relation}")
            lines.append(f"  - Sao: **{sao}** | Cửa: **{cua}** | Thần: **{than}**")
            
            # V8.0: GIẢI THÍCH CHI TIẾT Sao/Cửa/Thần
            sao_info = SAO_GIAI_THICH.get(str(sao), {})
            if sao_info:
                lines.append(f"  - 📖 **Ý nghĩa Sao {sao}:** {sao_info.get('tinh_chat', '')} → {sao_info.get('van_de', '')}")
            # V9.0 KB: Chi tiết Sao từ Knowledge Base
            sao_kb = SAO_KY_MON.get(str(sao), {}) if SAO_KY_MON else {}
            if sao_kb:
                lines.append(f"  - 📚 **[KB] Sao {sao}:** Hành {sao_kb.get('hanh','')} | {sao_kb.get('loai','')} — {sao_kb.get('y_nghia','')}")
            
            cua_key = str(cua).replace(' Môn', '') + ' Môn' if 'Môn' not in str(cua) else str(cua)
            cua_info = CUA_GIAI_THICH.get(cua_key, {})
            if cua_info:
                lines.append(f"  - 📖 **Ý nghĩa Cửa {cua}:** {cua_info.get('cat_hung', '')} — {cua_info.get('y_nghia', '')}")
            # V9.0 KB: Chi tiết Cửa từ Knowledge Base
            cua_kb = CUA_KY_MON.get(cua_key, {}) if CUA_KY_MON else {}
            if cua_kb:
                lines.append(f"  - 📚 **[KB] Cửa {cua}:** Hành {cua_kb.get('hanh','')} | {cua_kb.get('loai','')} — {cua_kb.get('y_nghia','')}")
            
            than_info = THAN_GIAI_THICH.get(str(than), {})
            if than_info:
                lines.append(f"  - 📖 **Ý nghĩa Thần {than}:** {than_info.get('tinh_chat', '')}")
            # V9.0 KB: Chi tiết Thần từ Knowledge Base
            than_kb = THAN_KY_MON.get(str(than), {}) if THAN_KY_MON else {}
            if than_kb:
                lines.append(f"  - 📚 **[KB] Thần {than}:** Hành {than_kb.get('hanh','')} | {than_kb.get('loai','')} — {than_kb.get('y_nghia','')}")
            
            # V8.0: CÁCH CỤC — Tra TRUCTU_TRANH
            can_dia = dia_ban.get(chu_cung, '') if dia_ban else ''
            can_thien = can_thien_ban.get(str(chu_cung), can_thien_ban.get(chu_cung, ''))
            if can_thien and can_dia and can_thien not in ['Giáp', 'N/A'] and can_dia not in ['Giáp', 'N/A']:
                cach_cuc_key = str(can_thien).strip() + str(can_dia).strip()
                cach_cuc = KY_MON_DATA.get('TRUCTU_TRANH', {}).get(cach_cuc_key, {})
                if cach_cuc and cach_cuc.get('Tên_Cách_Cục', '') != 'Không có':
                    cuc_name = cach_cuc.get('Tên_Cách_Cục', '?')
                    cuc_cat_hung = cach_cuc.get('Cát_Hung', 'Bình')
                    cuc_luan_giai = cach_cuc.get('Luận_Giải', '')
                    lines.append(f"\n  **⚡ Cách Cục: {cuc_name} ({cuc_cat_hung})**")
                    lines.append(f"  - {cuc_luan_giai}")
            
            # V9.0 KB: Tra cứu Kỳ Môn cách cục từ Knowledge Base
            cuc_found = False
            for cuc_dict in [KY_MON_CACH_CUC, KY_MON_CACH_CUC_MR]:
                if cuc_found:
                    break
                if cuc_dict:
                    for cuc_id, cuc_data in cuc_dict.items():
                        dk = cuc_data.get('dk', '')
                        if str(sao) in dk and (str(cua) in dk or str(than) in dk):
                            lines.append(f"  - 📚 **[KB Cách Cục] {cuc_id}:** {cuc_data.get('luan','')}")
                            lines.append(f"    Ứng dụng: {cuc_data.get('ung_dung','')}")
                            cuc_found = True
                            break
            
            # V9.0 KB: SAO + CỬA tổ hợp tra cứu
            sao_cua_key = (str(sao), cua_key)
            sc_info = None
            if SAO_CUA_TO_HOP:
                sc_info = SAO_CUA_TO_HOP.get(sao_cua_key)
            if not sc_info and SAO_CUA_TO_HOP_BS:
                sc_info = SAO_CUA_TO_HOP_BS.get(sao_cua_key)
            if sc_info:
                lines.append(f"  - 📚 **[KB Sao+Cửa] {sao} + {cua}:** {sc_info.get('luan','')}")
                lines.append(f"    Ứng dụng: {sc_info.get('ung_dung','')}")
                if 'CÁT' in sc_info.get('luan', ''):
                    score += 1
                    reasons_list.append(f"Sao+Cửa combo CÁT")
                elif 'HUNG' in sc_info.get('luan', ''):
                    score -= 1
                    reasons_list.append(f"Sao+Cửa combo HUNG")
            
            # V10.0 KB: THẬP CAN KHẮC ỨNG — 81 tổ hợp Thiên×Địa bàn (Sách Lưu Bá Ôn)
            can_dia = dia_ban.get(chu_cung, '') if dia_ban else ''
            can_thien = can_thien_ban.get(str(chu_cung), can_thien_ban.get(chu_cung, ''))
            if can_thien and can_dia and THAP_CAN_KHAC_UNG:
                khac_ung_key = f"{can_thien}+{can_dia}"
                khac_ung = THAP_CAN_KHAC_UNG.get(khac_ung_key)
                if khac_ung:
                    ku_cat_hung = khac_ung.get('cat_hung', '')
                    lines.append(f"\n  **📖 [Sách] Khắc Ứng: {khac_ung.get('ten','')} ({ku_cat_hung})**")
                    lines.append(f"  - {khac_ung.get('luan','')}")
                    if 'ĐẠI CÁT' in ku_cat_hung:
                        score += 2
                        reasons_list.append(f"📖 Khắc Ứng ĐẠI CÁT")
                    elif 'CÁT' in ku_cat_hung and 'HUNG' not in ku_cat_hung:
                        score += 1
                        reasons_list.append(f"📖 Khắc Ứng CÁT")
                    elif 'ĐẠI HUNG' in ku_cat_hung:
                        score -= 2
                        reasons_list.append(f"📖 Khắc Ứng ĐẠI HUNG")
                    elif 'HUNG' in ku_cat_hung:
                        score -= 1
                        reasons_list.append(f"📖 Khắc Ứng HUNG")
            
            # V10.0 KB: BÁT MÔN BAY CUNG — Trạng thái Cửa tại Cung (Sách Kỳ Môn Cơ Bản)
            if BAT_MON_BAY_CUNG and cua_key and chu_cung:
                mon_data = BAT_MON_BAY_CUNG.get(cua_key)
                if mon_data:
                    cung_num = int(chu_cung) if str(chu_cung).isdigit() else 0
                    if cung_num > 0:
                        trang_thai = None
                        if cung_num == mon_data.get('phuc_ngam'):
                            trang_thai = '⚠️ Phục Ngâm (Cửa tại cung gốc → Trì trệ)'
                            score -= 1
                        elif cung_num == mon_data.get('phan_ngam'):
                            trang_thai = '🔴 Phản Ngâm (Cửa đối cung → Đảo ngược)'
                            score -= 2
                        elif cung_num == mon_data.get('nhap_mo'):
                            trang_thai = '⚰️ Nhập Mộ (Cửa vào Mộ → Bế tắc)'
                            score -= 1
                        elif cung_num in mon_data.get('buc', []):
                            trang_thai = '💢 Bức (Cửa khắc Cung → Ép buộc)'
                        elif cung_num in mon_data.get('che', []):
                            trang_thai = '🛡️ Chế (Cung khắc Cửa → Bị kiềm chế)'
                        
                        if trang_thai:
                            lines.append(f"  - 📖 **[Sách] {cua_key} bay Cung {chu_cung}:** {trang_thai}")
                            if 'Phục Ngâm' in trang_thai or 'Nhập Mộ' in trang_thai:
                                reasons_list.append(f"📖 Cửa {trang_thai.split('(')[0].strip()}")
            
            # V10.0 KB: CAN CHI TƯỢNG Ý — Y học + Hôn nhân (Sách Đế Vương Chi Thuật)
            if CAN_CHI_TUONG_Y and can_thien:
                tuong_y = CAN_CHI_TUONG_Y.get(can_thien)
                if tuong_y:
                    q_lower_local = question.lower() if question else ''
                    if any(k in q_lower_local for k in ['bệnh', 'ốm', 'đau', 'khỏe', 'sức khỏe', 'thuốc', 'phẫu thuật']):
                        lines.append(f"  - 📖 **[Sách] Tượng Ý Y Học ({can_thien}):** Nội tạng: {tuong_y.get('an_tang','')} | Cơ thể: {tuong_y.get('co_the','')}")
                        lines.append(f"    Bệnh dễ mắc: {tuong_y.get('benh','')}")
                    if any(k in q_lower_local for k in ['vợ', 'chồng', 'yêu', 'hôn', 'cưới', 'tình', 'ngoại tình', 'bồ']):
                        lines.append(f"  - 📖 **[Sách] Tượng Ý Hôn Nhân ({can_thien}):** {tuong_y.get('hon_nhan','')}")
            
            # V10.0 KB: THẬP NHỊ THẦN ỨNG NGHIỆM — 12 Thần (Sách Bí Cấp Toàn Thư)
            if THAP_NHI_THAN_UNG_NGHIEM and than:
                than_ung = THAP_NHI_THAN_UNG_NGHIEM.get(str(than))
                if than_ung:
                    lines.append(f"  - 📖 **[Sách] 12 Thần Ứng Nghiệm ({than}):** {than_ung.get('ung_nghiem','')}")
            
            # Vạn Vật Loại Tượng
            vvlt_quai = get_bat_quai_tuong(quai)
            if vvlt_quai:
                lines.append(f"\n  **📊 Vạn Vật Loại Tượng ({quai}):**")
                for vl in vvlt_quai.split('\n')[1:5]:
                    lines.append(f"  {vl}")
            
            # Đánh giá tổng hợp
            sao_ok = any(s in str(sao) for s in ['Tâm', 'Nhậm', 'Phụ', 'Xung'])
            cua_ok = any(c in str(cua) for c in CUA_CAT)
            cua_bad = any(c in str(cua) for c in CUA_HUNG)
            
            # score và reasons_list đã khởi tạo ở đầu block chu_cung
            if 'ĐƯỢC SINH' in relation or 'Tỷ' in relation:
                score += 2
                reasons_list.append("Ngũ Hành thuận")
            elif 'BỊ KHẮC' in relation:
                score -= 2
                reasons_list.append("Ngũ Hành khắc")
            elif 'hao' in relation:
                score -= 1
                reasons_list.append("Ngũ Hành hao")
            
            if sao_ok:
                score += 1
                reasons_list.append(f"Sao {sao} Cát")
            if cua_ok:
                score += 1
                reasons_list.append(f"Cửa {cua} Cát")
            if cua_bad:
                score -= 1
                reasons_list.append(f"Cửa {cua} Hung")
            
            # ====== V9.0: PHẢN NGÂM / PHỤC NGÂM ======
            can_dia = dia_ban.get(chu_cung, '') if dia_ban else ''
            can_thien = can_thien_ban.get(str(chu_cung), can_thien_ban.get(chu_cung, ''))
            phan_phuc = _check_phan_phuc_ngam(can_thien, can_dia) if can_thien and can_dia else None
            if phan_phuc == 'PHỤC NGÂM':
                score -= 2
                reasons_list.append("⚠️ PHỤC NGÂM")
                lines.append(f"\n  **⚠️ PHỤC NGÂM tại Cung BT:** Can Thiên = Can Địa = {can_thien}")
                lines.append(f"  → Sự việc BẾ TẮC, TRÌ TRỆ, khó tiến triển. Nên ẩn nhẫn chờ thời!")
            elif phan_phuc == 'PHẢN NGÂM':
                score -= 3
                reasons_list.append("🔴 PHẢN NGÂM")
                lines.append(f"\n  **🔴 PHẢN NGÂM tại Cung BT:** Can Thiên {can_thien} xung Can Địa {can_dia}")
                lines.append(f"  → Sự việc ĐẢO NGƯỢC hoàn toàn! Kế hoạch bị phá vỡ, TUYỆT ĐỐI không nên hành động!")
            
            # ====== V15.0: TUẦN KHÔNG TỨ TRỤ (Void Period — 4 Pillars) ======
            can_nam_km = qmdg_input.get('can_nam', '')
            chi_nam_km = qmdg_input.get('chi_nam', '')
            chi_thang_km = qmdg_input.get('chi_thang', '')
            chi_ngay_km = qmdg_input.get('chi_ngay', '')
            chi_gio_km = qmdg_input.get('chi_gio', '')
            
            # Tính Tuần Không cho từng trụ
            tuan_khong_results = {}
            if can_ngay and chi_ngay_km:
                kv_ngay = _get_khong_vong(can_ngay, chi_ngay_km)
                if kv_ngay:
                    tuan_khong_results['Ngày'] = kv_ngay
            if can_nam_km and chi_nam_km:
                kv_nam = _get_khong_vong(can_nam_km, chi_nam_km)
                if kv_nam:
                    tuan_khong_results['Năm'] = kv_nam
            if can_thang and chi_thang_km:
                kv_thang = _get_khong_vong(can_thang, chi_thang_km)
                if kv_thang:
                    tuan_khong_results['Tháng'] = kv_thang
            
            if tuan_khong_results:
                lines.append(f"\n  **🕳️ TUẦN KHÔNG TỨ TRỤ:**")
                lines.append(f"  ⚡ *Chi lâm Tuần Không = KHÔNG CÓ THẬT, sự việc trống rỗng!*")
                for tru_name, kv_list in tuan_khong_results.items():
                    lines.append(f"  - Tuần Không Trụ {tru_name}: **{', '.join(kv_list)}**")
                
                # Check: Chi Giờ (Sự Việc) có lâm Tuần Không Ngày không?
                kv_ngay_check = tuan_khong_results.get('Ngày', [])
                if chi_gio_km and chi_gio_km in kv_ngay_check:
                    score -= 3
                    reasons_list.append(f"🕳️ Chi Giờ ({chi_gio_km}) lâm Tuần Không")
                    lines.append(f"  - 🔴 **Chi Giờ ({chi_gio_km}) LÂM TUẦN KHÔNG!** → Sự việc KHÔNG CÓ THẬT, hư ảo!")
                
                # Check: Chi Ngày (Bản Thân) có lâm Tuần Không Tháng/Năm không?
                kv_thang_check = tuan_khong_results.get('Tháng', [])
                kv_nam_check = tuan_khong_results.get('Năm', [])
                if chi_ngay_km and (chi_ngay_km in kv_thang_check or chi_ngay_km in kv_nam_check):
                    score -= 1
                    reasons_list.append(f"⚠️ Chi Ngày ({chi_ngay_km}) lâm Tuần Không")
                    lines.append(f"  - ⚠️ Chi Ngày ({chi_ngay_km}) lâm Tuần Không → Bản thân YẾU ĐI, thiếu nội lực")
                
                # Check: Chi của cung Sự Việc (can_gio cung) có lâm Tuần Không?
                if sv_cung and kv_ngay_check:
                    # Lấy Can Thiên bàn tại Cung SV
                    sv_can = can_thien_ban.get(str(sv_cung), can_thien_ban.get(sv_cung, ''))
                    if sv_can:
                        sv_hanh_check = CAN_NGU_HANH.get(sv_can, '')
                        # Kiểm tra theo chi tương ứng
                        for chi_check in kv_ngay_check:
                            chi_hanh = CHI_NGU_HANH.get(chi_check, '')
                            if chi_hanh == sv_hanh_check:
                                lines.append(f"  - ⚠️ Cung SV ({sv_cung}) có Can {sv_can} đồng hành Tuần Không → Sự việc bấp bênh")
                                break
            
            # ====== V15.0: DỊCH MÃ TỨ TRỤ (Post Horse — 4 Pillars) ======
            dich_ma_results = {}
            tru_chi_map = {}
            if chi_nam_km: tru_chi_map['Năm'] = chi_nam_km
            if chi_thang_km: tru_chi_map['Tháng'] = chi_thang_km
            if chi_ngay_km: tru_chi_map['Ngày'] = chi_ngay_km
            if chi_gio_km: tru_chi_map['Giờ'] = chi_gio_km
            
            for tru_name, chi_val in tru_chi_map.items():
                ma = DICH_MA_MAP.get(chi_val, '')
                if ma:
                    dich_ma_results[tru_name] = (chi_val, ma)
            
            if dich_ma_results:
                lines.append(f"\n  **🐎 DỊCH MÃ TỨ TRỤ:**")
                lines.append(f"  ⚡ *Dịch Mã = DI CHUYỂN, biến động, thay đổi nhanh chóng*")
                for tru_name, (chi_val, ma_chi) in dich_ma_results.items():
                    lines.append(f"  - Trụ {tru_name} ({chi_val}) → Dịch Mã tại **{ma_chi}**")
                
                # Check: Chi Giờ có phải Dịch Mã của Chi Ngày không?
                ma_ngay = DICH_MA_MAP.get(chi_ngay_km, '') if chi_ngay_km else ''
                if chi_gio_km and ma_ngay and chi_gio_km == ma_ngay:
                    # Giờ chính là Dịch Mã → Sự việc DI CHUYỂN mạnh
                    if verdict in ['CÁT', 'ĐẠI CÁT', 'BÌNH']:
                        reasons_list.append(f"🐎 Dịch Mã kích hoạt (Giờ={chi_gio_km}=Mã Ngày)")
                        lines.append(f"  - ✅ Chi Giờ ({chi_gio_km}) = Dịch Mã Ngày → Sự việc BIẾN ĐỘNG NHANH + CÁT = Đi xa CÁT LỢI")
                    else:
                        reasons_list.append(f"🐎 Dịch Mã + Hung")
                        lines.append(f"  - ⚠️ Chi Giờ ({chi_gio_km}) = Dịch Mã Ngày → BIẾN ĐỘNG MẠNH + HUNG = Chạy trốn, bỏ đi")
                
                # Check: Chi Ngày có phải Dịch Mã của Chi Giờ không?
                ma_gio = DICH_MA_MAP.get(chi_gio_km, '') if chi_gio_km else ''
                if chi_ngay_km and ma_gio and chi_ngay_km == ma_gio:
                    lines.append(f"  - 🔄 Chi Ngày ({chi_ngay_km}) = Dịch Mã Giờ → Bản thân cũng đang di chuyển, thay đổi")
            
            # ====== V15.0: TỨ TRỤ Ý NGHĨA (Four Pillars Meaning) ======
            can_nam_display = qmdg_input.get('can_nam', '?')
            chi_nam_display = chi_nam_km or '?'
            can_thang_display = can_thang or '?'
            chi_thang_display = chi_thang_km or '?'
            chi_ngay_display = chi_ngay_km or '?'
            chi_gio_display = chi_gio_km or '?'
            
            has_tru_data = can_nam_display != '?' or can_thang_display != '?'
            if has_tru_data:
                lines.append(f"\n  **📜 TỨ TRỤ Ý NGHĨA:**")
                
                # Trụ Năm
                hanh_can_nam = CAN_NGU_HANH.get(can_nam_display, '?')
                hanh_chi_nam = CHI_NGU_HANH.get(chi_nam_display, '?')
                lines.append(f"  - 🌳 **Trụ Năm** ({can_nam_display} {chi_nam_display}): Hành {hanh_can_nam}/{hanh_chi_nam}")
                lines.append(f"    → GỐC RỄ (ông bà, xã hội, nền tảng, nguồn gốc sự việc)")
                
                # Trụ Tháng
                hanh_can_thang = CAN_NGU_HANH.get(can_thang_display, '?')
                hanh_chi_thang = CHI_NGU_HANH.get(chi_thang_display, '?')
                lines.append(f"  - 🚪 **Trụ Tháng** ({can_thang_display} {chi_thang_display}): Hành {hanh_can_thang}/{hanh_chi_thang}")
                lines.append(f"    → CỬA CHÍNH (cha mẹ, sự nghiệp, lệnh tháng chi phối)")
                
                # Trụ Ngày
                hanh_chi_ngay = CHI_NGU_HANH.get(chi_ngay_display, '?')
                lines.append(f"  - 🧑 **Trụ Ngày** ({can_ngay} {chi_ngay_display}): Hành {hanh_can}/{hanh_chi_ngay}")
                lines.append(f"    → BẢN THÂN (chính mình, tâm tính, nội lực)")
                
                # Trụ Giờ
                hanh_can_gio = CAN_NGU_HANH.get(can_gio, '?')
                hanh_chi_gio = CHI_NGU_HANH.get(chi_gio_display, '?')
                lines.append(f"  - 🔮 **Trụ Giờ** ({can_gio} {chi_gio_display}): Hành {hanh_can_gio}/{hanh_chi_gio}")
                lines.append(f"    → TƯƠNG LAI (con cái, kết quả, hậu vận, diễn biến cuối)")
                
                # Phân tích sinh khắc giữa các trụ
                if hanh_can != '?' and hanh_can_gio != '?':
                    rel_ngay_gio = _ngu_hanh_relation(hanh_can, hanh_can_gio)
                    if 'SINH' in rel_ngay_gio and 'BỊ' not in rel_ngay_gio:
                        lines.append(f"  - 📊 Ngày ({hanh_can}) SINH Giờ ({hanh_can_gio}): Mình phải BỎ CÔNG SỨC ra")
                    elif 'ĐƯỢC SINH' in rel_ngay_gio:
                        lines.append(f"  - 📊 Giờ ({hanh_can_gio}) sinh Ngày ({hanh_can}): Kết quả ĐEM LẠI LỢI ÍCH")
                        score += 1
                        reasons_list.append("Giờ sinh Ngày (lợi)")
                    elif 'BỊ KHẮC' in rel_ngay_gio:
                        lines.append(f"  - 📊 Giờ ({hanh_can_gio}) khắc Ngày ({hanh_can}): Kết quả GÂY BẤT LỢI")
                        score -= 1
                        reasons_list.append("Giờ khắc Ngày (bất lợi)")
                    elif 'thắng' in rel_ngay_gio:
                        lines.append(f"  - 📊 Ngày ({hanh_can}) khắc Giờ ({hanh_can_gio}): Mình KIỂM SOÁT kết quả")
            
            # ====== V9.0: TAM KỲ ĐẮC SỬ ======
            tam_ky = ['Ất', 'Bính', 'Đinh']
            if can_thien in tam_ky and cua_ok:
                score += 2
                reasons_list.append(f"✨ Tam Kỳ Đắc Sử ({can_thien}+{cua})")
                lines.append(f"\n  **✨ TAM KỲ ĐẮC SỬ:** Can {can_thien} (Tam Kỳ) gặp Cửa Cát {cua}")
                if can_thien == 'Ất':
                    lines.append(f"  → Nhật Kỳ (Mặt Trời) — Cực CÁT, mọi việc hanh thông, quý nhân giúp đỡ!")
                elif can_thien == 'Bính':
                    lines.append(f"  → Nguyệt Kỳ (Mặt Trăng) — Rất tốt, giảm lo âu, vui vẻ, thăng tiến!")
                elif can_thien == 'Đinh':
                    lines.append(f"  → Tinh Kỳ (Sao) — Linh thiêng nhất, tránh tai họa, được phù hộ!")
            
            # ====== V9.0: THIÊN ĐỊA NHÂN TAM TÀI ======
            sao_hanh = SAO_GIAI_THICH.get(str(sao), {}).get('hanh', '')
            if sao_hanh and hanh_cung:
                sao_rel = _ngu_hanh_relation(sao_hanh, hanh_cung)
                cua_hanh = {'Khai Môn': 'Kim', 'Hưu Môn': 'Thủy', 'Sinh Môn': 'Thổ',
                           'Thương Môn': 'Mộc', 'Đỗ Môn': 'Mộc', 'Cảnh Môn': 'Hỏa',
                           'Tử Môn': 'Thổ', 'Kinh Môn': 'Kim'}.get(cua_key, '')
                if cua_hanh:
                    cua_rel = _ngu_hanh_relation(cua_hanh, hanh_cung)
                    all_sinh = ('SINH' in sao_rel or 'Tỷ' in sao_rel) and ('SINH' in cua_rel or 'Tỷ' in cua_rel)
                    any_khac = 'KHẮC' in sao_rel or 'KHẮC' in cua_rel
                    if all_sinh:
                        score += 1
                        reasons_list.append("Tam Tài hợp")
                        lines.append(f"\n  **🌟 THIÊN ĐỊA NHÂN TAM TÀI TƯƠNG HỢP:**")
                        lines.append(f"  → Sao ({sao_hanh}) + Cửa ({cua_hanh}) đều thuận Cung ({hanh_cung}) — ĐẠI CÁT!")
                    elif any_khac:
                        lines.append(f"\n  **⚡ Tam Tài xung khắc:**")
                        lines.append(f"  → Sao ({sao_hanh}) {sao_rel} Cung | Cửa ({cua_hanh}) {cua_rel} Cung")
            
            # ====== V9.0: VẠN VẬT CONTEXT-AWARE ======
            vvlt_ctx = _get_van_vat_context(quai, question)
            if vvlt_ctx:
                lines.append(f"\n  **📊 Vạn Vật Loại Tượng ({quai}):**")
                for vl in vvlt_ctx.split('\n'):
                    lines.append(f"  {vl}")
            
            # Final verdict
            if score >= 3:
                verdict = "ĐẠI CÁT"
                reason = " + ".join(reasons_list)
            elif score >= 2:
                verdict = "CÁT"
                reason = " + ".join(reasons_list)
            elif score <= -2:
                verdict = "ĐẠI HUNG"
                reason = " + ".join(reasons_list)
            elif score <= -1:
                verdict = "HUNG"
                reason = " + ".join(reasons_list)
            else:
                verdict = "BÌNH"
                reason = "Cân bằng"
            
            lines.append(f"\n  → **KỲ MÔN: {verdict}** ({reason})")
            
            # V8.0: Phân tích Cung SỰ VIỆC (Can Giờ)
            if sv_cung and sv_cung != chu_cung:
                sv_sao = thien_ban.get(sv_cung, '?')
                sv_cua = nhan_ban.get(sv_cung, '?')
                sv_hanh = CUNG_NGU_HANH.get(sv_cung, '?')
                sv_quai = QUAI_TUONG.get(sv_cung, '?')
                rel_sv = _ngu_hanh_relation(hanh_cung, sv_hanh)
                lines.append(f"\n- **Sự việc** (Can Giờ {can_gio}) tại **Cung {sv_cung} ({sv_quai})**")
                lines.append(f"  - Sao: {sv_sao} | Cửa: {sv_cua} | Hành: {sv_hanh}")
                lines.append(f"  - **Bản thân vs Sự việc:** Cung {chu_cung} ({hanh_cung}) → Cung {sv_cung} ({sv_hanh}): {rel_sv}")
                if 'SINH' in rel_sv and 'BỊ' not in rel_sv:
                    lines.append(f"  - 📝 BT sinh SV → Mình phải bỏ công sức ra, hao tổn")
                elif 'ĐƯỢC SINH' in rel_sv:
                    lines.append(f"  - 📝 SV sinh BT → Sự việc ĐEM LẠI LỢI ÍCH cho mình")
                elif 'thắng' in rel_sv:
                    lines.append(f"  - 📝 BT khắc SV → Mình KIỂM SOÁT được sự việc")
                elif 'BỊ KHẮC' in rel_sv:
                    lines.append(f"  - 📝 SV khắc BT → Sự việc GÂY KHÓ KHĂN cho mình")
            
            # V8.0: ĐẾM SỐ LƯỢNG (anh chị em = Can Tháng)
            if is_count:
                # Đếm qua Can Tháng (đại diện anh chị em, bạn bè)
                if thang_cung:
                    thang_quai = QUAI_TUONG.get(thang_cung, '')
                    thang_hanh = CUNG_NGU_HANH.get(thang_cung, '')
                    if thang_quai and thang_quai in TIEN_THIEN:
                        tt_num = TIEN_THIEN[thang_quai]
                        # Vượng = nhiều, Suy = ít
                        hanh_thang = CUNG_NGU_HANH.get(thang_cung, '')
                        is_vuong = (SINH.get(hanh_can) == hanh_thang) or (hanh_can == hanh_thang)
                        if is_vuong:
                            count_num = tt_num
                        else:
                            count_num = max(1, tt_num - 2)
                        lines.append(f"\n  **📊 ĐẾM SỐ (Kỳ Môn):**")
                        lines.append(f"  - Can Tháng (**{can_thang}**) = Đại diện anh chị em")
                        lines.append(f"  - Can Tháng tại Cung {thang_cung} ({thang_quai})")
                        lines.append(f"  - Quái Tiên Thiên {thang_quai} = **{TIEN_THIEN.get(thang_quai, '?')}**")
                        lines.append(f"  - Hành Cung: {thang_hanh} {'(Vượng → nhiều)' if is_vuong else '(Suy → ít hơn)'}")
                        lines.append(f"  - → **Số anh chị em (Kỳ Môn): khoảng {count_num} người**")
                else:
                    # Nếu không có Can Tháng, dùng Quái bản thân
                    if quai in TIEN_THIEN:
                        count_num = max(1, TIEN_THIEN[quai] - 1)
                        lines.append(f"\n  **📊 ĐẾM SỐ (Kỳ Môn):**")
                        lines.append(f"  - Dùng Quái bản thân {quai} (Tiên Thiên = {TIEN_THIEN[quai]})")
                        lines.append(f"  - → **Số lượng ước tính: khoảng {count_num}**")
            
            # Tuổi — V32.6: Dùng Trường Sinh stage thay vì Tiên Thiên × 3/5
            if is_age:
                # Xác định Ngũ Khí trạng thái → Trường Sinh stage → tuổi
                if 'ĐƯỢC SINH' in relation or 'Tỷ' in relation:
                    km_age_stage = 'Đế Vượng'  # Vượng → 31-45
                elif 'BỊ SINH' in relation:
                    km_age_stage = 'Lâm Quan'  # Tướng → 16-30
                elif 'BỊ KHẮC' in relation:
                    km_age_stage = 'Suy'  # Suy → 46-55
                elif 'KHẮC' in relation:
                    km_age_stage = 'Bệnh'  # Bệnh → 56-65
                else:
                    km_age_stage = 'Quan Đới'  # Trung bình → 8-15
                
                ts_data = TRUONG_SINH_POWER.get(km_age_stage, {})
                tuoi_min = ts_data.get('tuoi_min', 0)
                tuoi_max = ts_data.get('tuoi_max', 0)
                age_num = (tuoi_min + tuoi_max) // 2
                tt_num = TIEN_THIEN.get(quai, 0) if quai else 0
                lines.append(f"  - Trường Sinh: **{km_age_stage}** → {tuoi_min}-{tuoi_max} tuổi")
                lines.append(f"  - Tiên Thiên {quai}={tt_num} (tham khảo)")
                lines.append(f"  - → **Tuổi ước tính (KM): khoảng {tuoi_min}-{tuoi_max} tuổi**")
            
            # Tìm đồ
            if is_find:
                huong_map = {1: 'Bắc', 2: 'Tây Nam', 3: 'Đông', 4: 'Đông Nam', 6: 'Tây Bắc', 7: 'Tây', 8: 'Đông Bắc', 9: 'Nam'}
                noi_map = {1: 'gần nước/nhà tắm', 2: 'nơi thấp/đất', 3: 'gần cửa/xe', 4: 'gần cửa sổ', 6: 'tầng trên/nơi cao', 7: 'phòng khách', 8: 'trong tủ/góc', 9: 'nơi sáng/bếp'}
                dt_cung = sv_cung or chu_cung
                lines.append(f"  - 📍 **HƯỚNG TÌM: {huong_map.get(dt_cung, '?')}** — {noi_map.get(dt_cung, '?')}")
        else:
            lines.append("- Không xác định được Cung bản thân từ dữ liệu.")
            reason = "Thiếu dữ liệu"
        
        lines.append("")
        return "\n".join(lines), verdict, age_num, reason, count_num

    # ===========================
    # LỤC HÀO ANALYSIS
    # ===========================
    def _analyze_luc_hao_full(self, luc_hao_data, dung_than, is_age, is_count=False):
        """V8.0 — Phân tích Lục Hào chi tiết: 6 hào, Nguyên/Kỵ/Cừu Thần, Thế/Ứng, 12 Trường Sinh"""
        lines = []
        verdict = "BÌNH"
        reason = ""
        age_num = None
        count_num = None
        
        ban = luc_hao_data.get('ban', {})
        bien = luc_hao_data.get('bien', {})
        dong_hao = luc_hao_data.get('dong_hao', [])
        haos = ban.get('haos') or ban.get('details', [])
        
        lines.append(f"- **Quẻ Chủ:** {ban.get('name', '?')} ({ban.get('palace', '?')})")
        lines.append(f"- **Quẻ Biến:** {bien.get('name', '?')}")
        lines.append(f"- **Hào Động:** {', '.join(map(str, dong_hao)) if dong_hao else 'Tĩnh'}")
        
        # V8.0: Vạn Vật Loại Tượng cho Cung quẻ
        palace = ban.get('palace', '')
        if palace:
            vvlt = get_bat_quai_tuong(palace)
            if vvlt:
                lines.append(f"\n  **📊 Vạn Vật ({palace}):**")
                for vl in vvlt.split('\n')[1:5]:
                    lines.append(f"  {vl}")
        
        # V8.0: HIỂN THỊ 6 HÀO CHI TIẾT
        the_hao = None
        the_idx = None
        ung_hao = None
        ung_idx = None
        dung_than_hao = None
        dung_than_idx = None
        huynh_de_count = 0  # Đếm Huynh Đệ cho is_count
        
        if haos:
            lines.append(f"\n**☯️ Bảng 6 Hào (Lục Thần + Lục Thân):**")
            lines.append(f"| Hào | Lục Thần | Lục Thân | Can Chi | Ngũ Hành | Thế/Ứng | Động |")
            lines.append(f"|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
            for i, hao in enumerate(haos):
                luc_than = hao.get('luc_than', '?')
                luc_than_td = hao.get('luc_than_td', hao.get('luc_thu', hao.get('luc_than_kd', '—')))
                can_chi = hao.get('can_chi', '?')
                ngu_hanh = hao.get('ngu_hanh', '?')
                the_ung = hao.get('the_ung', '')
                is_dong = '🔴 Động' if (i+1) in dong_hao else ''
                
                lines.append(f"| {i+1} | {luc_than_td} | {luc_than} | {can_chi} | {ngu_hanh} | {the_ung} | {is_dong} |")

                
                # Track Thế/Ứng
                if the_ung == 'Thế':
                    the_hao = hao
                    the_idx = i + 1
                elif the_ung == 'Ứng':
                    ung_hao = hao
                    ung_idx = i + 1
                
                # Track Dụng Thần
                if luc_than == dung_than or (dung_than == 'Bản Thân' and the_ung == 'Thế'):
                    dung_than_hao = hao
                    dung_than_idx = i + 1
                
                # Đếm Huynh Đệ
                if luc_than == 'Huynh Đệ':
                    huynh_de_count += 1
            
            # V8.0: Giải thích Lục Thân trong quẻ
            luc_than_in_que = set(h.get('luc_than', '') for h in haos)
            for lt in luc_than_in_que:
                if lt and lt in LUC_THAN_GIAI_THICH:
                    lines.append(f"  - **{lt}**: {LUC_THAN_GIAI_THICH[lt]}")
        
        # Tìm Dụng Thần
        if dung_than_hao:
            lines.append(f"\n- **🎯 Dụng Thần ({dung_than}):** Hào {dung_than_idx} — {dung_than_hao.get('luc_than', '?')} {dung_than_hao.get('can_chi', '?')} ({dung_than_hao.get('ngu_hanh', '?')})")
        elif the_hao:
            dung_than_hao = the_hao
            dung_than_idx = the_idx
            lines.append(f"\n- **🎯 Dụng Thần (Thế hào):** Hào {the_idx} — {the_hao.get('can_chi', '?')} ({the_hao.get('ngu_hanh', '?')})")
        
        # V9.0 Phase 4: PHỤC THẦN — Khi Dụng Thần không xuất hiện trong quẻ
        if not dung_than_hao and PHUC_THAN_RULES:
            lines.append(f"\n- ⚠️ **PHỤC THẦN:** Dụng Thần ({dung_than}) KHÔNG xuất hiện trong quẻ!")
            lines.append(f"  → Dụng Thần ẩn (Phục Thần), sự việc chưa lộ diện.")
            for pt_id, pt_data in PHUC_THAN_RULES.items():
                lines.append(f"  - 📚 **{pt_id}:** {pt_data.get('dk', '')} → {pt_data.get('ket_luan', '')}")
        
        # V9.0 Phase 4: ĐỘNG/TĨNH QUY TẮC
        if DONG_TINH_RULES:
            n_dong = len(dong_hao) if dong_hao else 0
            for dt_rule in DONG_TINH_RULES:
                if (dt_rule['id'] == 'DT01' and n_dong == 1) or \
                   (dt_rule['id'] == 'DT02' and n_dong >= 5) or \
                   (dt_rule['id'] == 'DT03' and n_dong == 0):
                    lines.append(f"\n- 📚 **[KB] {dt_rule['ten']}:** {dt_rule['ket_luan']}")
                    break
        
        # V9.0 KB: Tra Nguyên Thần / Kỵ Thần / Cừu Thần
        if dung_than_hao and NGUYEN_KY_CUU:
            dt_hanh = dung_than_hao.get('ngu_hanh', '')
            nkc = NGUYEN_KY_CUU.get(dt_hanh, {})
            if nkc:
                lines.append(f"- 📚 **[KB] Nguyên Thần** (sinh Dụng Thần): hành **{nkc.get('nguyen_than','')}** → Tìm hào {nkc.get('nguyen_than','')} vượng = CÁT")
                lines.append(f"- 📚 **[KB] Kỵ Thần** (khắc Dụng Thần): hành **{nkc.get('ky_than','')}** → Nếu vượng + động = HUNG")
                lines.append(f"- 📚 **[KB] Cừu Thần** (sinh Kỵ Thần): hành **{nkc.get('cuu_than','')}** → Tăng sức Kỵ Thần")
        
        # Đánh giá Dụng Thần
        reasons_list = []
        if dung_than_hao:
            vuong = dung_than_hao.get('vuong_suy', '')
            hanh = dung_than_hao.get('ngu_hanh', '')
            chi = dung_than_hao.get('chi', '')
            
            # V8.0: 12 Trường Sinh
            if hanh and chi:
                ts_stage, ts_explain = _get_truong_sinh(hanh, chi)
                if ts_stage:
                    lines.append(f"- **🔄 12 Trường Sinh ({hanh} tại {chi}):** {ts_stage}")
                    lines.append(f"  → {ts_explain}")
            
            if 'Vượng' in str(vuong) or 'Tướng' in str(vuong):
                verdict = "CÁT"
                reasons_list.append("Dụng Thần Vượng")
                lines.append(f"- Dụng Thần **VƯỢNG** → Sự việc **THUẬN LỢI**")
            elif 'Tử' in str(vuong) or 'Tuyệt' in str(vuong) or 'Mộ' in str(vuong):
                verdict = "HUNG"
                reasons_list.append("Dụng Thần Suy/Tử")
                lines.append(f"- Dụng Thần **SUY/TUYỆT** → Sự việc **KHÓ KHĂN**")
            elif 'Suy' in str(vuong) or 'Bệnh' in str(vuong):
                verdict = "HUNG"
                reasons_list.append(f"Dụng Thần {vuong}")
                lines.append(f"- Dụng Thần **{vuong}** → Sự việc **BẤT LỢI**")
            else:
                verdict = "BÌNH"
                reasons_list.append(f"Dụng Thần {vuong}")
                lines.append(f"- Dụng Thần ở trạng thái: {vuong}")
            
            # V8.0: NGUYÊN THẦN / KỴ THẦN / CỪU THẦN
            if hanh:
                nguyen_than_hanh = [h for h, s in SINH.items() if s == hanh]  # Hành sinh DT
                ky_than_hanh = [h for h, k in KHAC.items() if k == hanh]  # Hành khắc DT
                
                for i2, hao2 in enumerate(haos):
                    h2_hanh = hao2.get('ngu_hanh', '')
                    h2_lt = hao2.get('luc_than', '')
                    if h2_hanh in nguyen_than_hanh and i2 != (dung_than_idx - 1 if dung_than_idx else -1):
                        lines.append(f"  - 🟢 **Nguyên Thần** (sinh Dụng Thần): Hào {i2+1} {h2_lt} {hao2.get('can_chi', '?')} ({h2_hanh}) → Hỗ trợ")
                        if (i2+1) in dong_hao:
                            lines.append(f"    → Nguyên Thần ĐỘNG = Sự hỗ trợ MẠNH MẼ ✅")
                            reasons_list.append("Nguyên Thần động")
                        break
                
                for i2, hao2 in enumerate(haos):
                    h2_hanh = hao2.get('ngu_hanh', '')
                    h2_lt = hao2.get('luc_than', '')
                    if h2_hanh in ky_than_hanh and i2 != (dung_than_idx - 1 if dung_than_idx else -1):
                        lines.append(f"  - 🔴 **Kỵ Thần** (khắc Dụng Thần): Hào {i2+1} {h2_lt} {hao2.get('can_chi', '?')} ({h2_hanh}) → Gây hại")
                        if (i2+1) in dong_hao:
                            lines.append(f"    → Kỵ Thần ĐỘNG = Bất lợi NGHIÊM TRỌNG ⚠️")
                            reasons_list.append("Kỵ Thần động")
                            if verdict == "CÁT":
                                verdict = "BÌNH"
                        break
            
            # V8.0: THẾ/ỨNG SINH KHẮC
            if the_hao and ung_hao:
                the_hanh = the_hao.get('ngu_hanh', '')
                ung_hanh = ung_hao.get('ngu_hanh', '')
                if the_hanh and ung_hanh:
                    rel_tu = _ngu_hanh_relation(the_hanh, ung_hanh)
                    lines.append(f"\n- **Thế (Hào {the_idx}) vs Ứng (Hào {ung_idx}):** {the_hanh} vs {ung_hanh} → {rel_tu}")
                    if 'thắng' in rel_tu:
                        lines.append(f"  → Thế KHẮC Ứng = Mình THẮNG đối phương ✅")
                        reasons_list.append("Thế khắc Ứng")
                    elif 'BỊ KHẮC' in rel_tu:
                        lines.append(f"  → Ứng KHẮC Thế = Đối phương MẠNH hơn ⚠️")
                        reasons_list.append("Thế bị Ứng khắc")
            
            # V8.0: HÀO ĐỘNG chi tiết + V9.0 TẤN/THOÁI THẦN + V42.0 HÓA HỒI ĐẦU + HÀO TỪ
            if dong_hao:
                lines.append(f"\n**🔴 Phân tích Hào Động:**")
                bien_haos = bien.get('haos') or bien.get('details', []) if bien else []
                
                # V42.0: Lấy tên quẻ để tra Hào Từ
                _ten_que_lh = ban.get('name', '') or ban.get('ten', '')
                
                for d in dong_hao:
                    if d <= len(haos):
                        h = haos[d-1]
                        lt = h.get('luc_than', '?')
                        cc = h.get('can_chi', '?')
                        nh = h.get('ngu_hanh', '?')
                        lt_info = LUC_THAN_GIAI_THICH.get(lt, '')
                        lines.append(f"- Hào {d} ĐỘNG: **{lt}** {cc} ({nh})")
                        if lt_info:
                            lines.append(f"  → Ý nghĩa: {lt} = {lt_info}")
                        
                        # V42.0: HÀO TỪ KINH DỊCH tại hào động
                        hao_tu = _get_hao_tu(_ten_que_lh, d)
                        if hao_tu:
                            if isinstance(hao_tu, dict):
                                ht_text = hao_tu.get('loi', '') or hao_tu.get('text', '') or str(hao_tu)
                                ht_giai = hao_tu.get('giai', '') or hao_tu.get('explain', '')
                            else:
                                ht_text = str(hao_tu)
                                ht_giai = ''
                            if ht_text:
                                lines.append(f"  → 📜 **Hào Từ Kinh Dịch:** {ht_text[:200]}")
                            if ht_giai:
                                lines.append(f"  → 📖 **Giải:** {ht_giai[:200]}")
                        
                        # V42.0: LỤC THẦN PHÂN TÍCH SÂU
                        _luc_thu = h.get('luc_thu', '') or h.get('luc_than_kd', '')
                        if _luc_thu and _luc_thu in LUC_THAN_DEEP:
                            _ltd = LUC_THAN_DEEP[_luc_thu]
                            # Xét vượng/suy dựa trên Ngũ Hành Lục Thần vs lệnh tháng
                            _lenh = _get_lenh_thang_hanh()
                            _ltd_hanh = _ltd['hanh']
                            if _lenh == _ltd_hanh or SINH.get(_lenh) == _ltd_hanh:
                                lines.append(f"  → 🎭 **{_luc_thu} (VƯỢNG):** {_ltd['vuong']}")
                            else:
                                lines.append(f"  → 🎭 **{_luc_thu} (SUY):** {_ltd['suy']}")
                            # Kết hợp Lục Thần + Lục Thân
                            _ltd_map = _ltd.get('luc_than_map', {})
                            if lt in _ltd_map:
                                lines.append(f"  → 🔗 **{_luc_thu} + {lt}:** {_ltd_map[lt]}")
                        
                        # Giải thích ảnh hưởng
                        if lt == 'Thê Tài':
                            lines.append(f"  → 💰 Tiền tài BIẾN ĐỘNG — Có thay đổi về tài chính")
                        elif lt == 'Quan Quỷ':
                            lines.append(f"  → ⚖️ Công việc/Bệnh BIẾN ĐỘNG — Cẩn thận áp lực")
                        elif lt == 'Huynh Đệ':
                            lines.append(f"  → 👥 Anh em/Cạnh tranh BIẾN ĐỘNG — Cẩn thận hao tổn")
                        elif lt == 'Tử Tôn':
                            lines.append(f"  → 😊 May mắn BIẾN ĐỘNG — Vui vẻ nhưng không ổn định")
                        elif lt == 'Phụ Mẫu':
                            lines.append(f"  → 🏠 Nhà cửa/Giấy tờ BIẾN ĐỘNG — Có thay đổi")
                        
                        # V9.0: TẤN THẦN / THOÁI THẦN
                        chi_dong = h.get('chi', '')
                        chi_bien = ''
                        if bien_haos and d <= len(bien_haos):
                            chi_bien = bien_haos[d-1].get('chi', '')
                        if chi_dong and chi_bien:
                            tan_thoai = _check_tan_thoai_than(chi_dong, chi_bien)
                            if tan_thoai == 'TẤN THẦN':
                                lines.append(f"  → 📈 **TẤN THẦN** ({chi_dong}→{chi_bien}): Tiến lên! Sự việc PHÁT TRIỂN tốt ✅")
                                reasons_list.append("Tấn Thần")
                            elif tan_thoai == 'THOÁI THẦN':
                                lines.append(f"  → 📉 **THOÁI THẦN** ({chi_dong}→{chi_bien}): Thụt lùi! Sự việc SUY GIẢM ⚠️")
                                reasons_list.append("Thoái Thần")
                        
                        # V42.0: HÓA HỒI ĐẦU CHUYÊN SÂU
                        if chi_dong and chi_bien:
                            hanh_bien_hao = bien_haos[d-1].get('ngu_hanh', '') if bien_haos and d <= len(bien_haos) else ''
                            hoa_results = _analyze_hoa_hoi_dau(
                                nh, hanh_bien_hao, chi_dong, chi_bien,
                                _lh_can_ngay if '_lh_can_ngay' in dir() else '',
                                _lh_chi_ngay if '_lh_chi_ngay' in dir() else ''
                            )
                            for hoa_label, hoa_desc, hoa_impact in hoa_results:
                                lines.append(f"  → {hoa_label}: {hoa_desc}")
                                if hoa_impact == 'HUNG':
                                    reasons_list.append(hoa_label.replace('🔴 ', '').replace('⚰️ ', '').replace('❌ ', '').replace('🕳️ ', '').replace('⚡ ', '').replace('🔄 ', ''))
                                elif hoa_impact == 'CÁT':
                                    reasons_list.append(hoa_label.replace('🟢 ', ''))
            
            # ====== V9.0: KHÔNG VONG (Tuần Không) ======
            can_ngay_lh = luc_hao_data.get('can_ngay', '') or luc_hao_data.get('ban', {}).get('can_ngay', '')
            chi_ngay_lh = luc_hao_data.get('chi_ngay', '') or luc_hao_data.get('ban', {}).get('chi_ngay', '')
            khong_vong_list = _get_khong_vong(can_ngay_lh, chi_ngay_lh)
            if khong_vong_list and dung_than_hao:
                dt_chi = dung_than_hao.get('chi', '')
                if dt_chi in khong_vong_list:
                    lines.append(f"\n**🕳️ KHÔNG VONG:** Dụng Thần ({dt_chi}) lâm Tuần Không [{', '.join(khong_vong_list)}]")
                    lines.append(f"  → Sự việc HƯ, TRỐNG RỖNG — Chờ đến khi Xuất Không (gặp Chi {dt_chi}) mới ứng nghiệm!")
                    reasons_list.append("Dụng Thần Không Vong")
                    if verdict == "CÁT":
                        verdict = "BÌNH"
            
            # ====== V42.0: ÁM ĐỘNG (Nhật xung hào tĩnh) ======
            am_dong_results = _detect_am_dong(haos, dong_hao, chi_ngay_lh)
            if am_dong_results:
                lines.append(f"\n**👁️ ÁM ĐỘNG — Lực lượng ẩn:**")
                for ad in am_dong_results:
                    ad_lt = ad['luc_than']
                    lines.append(f"  - Hào {ad['hao_idx']} **{ad_lt}** {ad['can_chi']} ({ad['ngu_hanh']}) — Nhật ({ad['xung_chi']}) xung {ad['chi']}")
                    if ad_lt == dung_than:
                        lines.append(f"    → ⚠️ DỤng Thần bị Ám Động = Sự việc ĐANG có biến ĐỘT NGỘT từ bên ngoài!")
                        reasons_list.append("DT bị Ám Động")
                    elif ad_lt == 'Quan Quỷ':
                        lines.append(f"    → ⚠️ Quan Quỷ Ám Động = Có áp lực/bệnh ẩn đang phát tác")
                    elif ad_lt == 'Thê Tài':
                        lines.append(f"    → 💰 Thê Tài Ám Động = Tài chính biến động bất ngờ")
                    elif ad_lt == 'Huynh Đệ':
                        lines.append(f"    → 👥 Huynh Đệ Ám Động = Cạnh tranh ẩn, hao tổn bất ngờ")
                    else:
                        lines.append(f"    → {ad_lt} Ám Động = Yếu tố này đang ngầm ảnh hưởng sự việc")
            
            # ====== V42.1: PHÂN TÍCH SÂU KHÔNG VONG + DỊCH MÃ ======
            try:
                _dt_chi_deep = dung_than_hao.get('chi', '') if dung_than_hao else ''
                _dm_chi = DICH_MA_MAP.get(chi_ngay_lh, '') if chi_ngay_lh else ''
                _chi_thang_lh_deep = luc_hao_data.get('chi_thang', '')
                _kv_dm_deep = _analyze_kv_dich_ma_deep(
                    khong_vong_list, _dm_chi, _dt_chi_deep, dung_than or '',
                    haos=haos, dong_hao=dong_hao,
                    chi_ngay=chi_ngay_lh, chi_thang=_chi_thang_lh_deep,
                    verdict=verdict
                )
                if _kv_dm_deep:
                    lines.append(_kv_dm_deep)
            except Exception:
                pass
            
            # ====== V42.1: NGUYỆT PHÁ NÂNG CẤP — Visual Warning ======
            chi_thang_lh = luc_hao_data.get('chi_thang', '')
            if chi_thang_lh and dung_than_hao:
                dt_chi = dung_than_hao.get('chi', '')
                _np_text, _np_html = _build_nguyet_pha_warning(
                    dt_chi, chi_thang_lh, dung_than_name=dung_than or 'Dụng Thần',
                    haos=haos, method='LỤC HÀO'
                )
                if dt_chi and LUC_XUNG_CHI.get(chi_thang_lh) == dt_chi:
                    lines.append(f"\n**💥 NGUYỆT PHÁ:** Chi tháng {chi_thang_lh} xung Dụng Thần ({dt_chi})")
                    lines.append(f"  → Dụng Thần bị NGUYỆT PHÁ = Sức mạnh TAN VỠ, sự việc KHÓ THÀNH! ⚠️")
                    reasons_list.append("Dụng Thần Nguyệt Phá")
                    verdict = "HUNG"
                if _np_text:
                    lines.append(_np_text)
            
            # ====== V9.0: TAM HỢP CỤC ======
            if haos:
                all_chi = [h.get('chi', '') for h in haos if h.get('chi')]
                for tam_hop_set, (thc_hanh, thc_desc) in TAM_HOP_CUC.items():
                    matching = [c for c in all_chi if c in tam_hop_set]
                    if len(matching) >= 3:
                        lines.append(f"\n**🔗 TAM HỢP CỤC:** {thc_desc}")
                        if hanh:
                            thc_rel = _ngu_hanh_relation(thc_hanh, hanh)
                            if 'SINH' in thc_rel and 'BỊ' not in thc_rel:
                                lines.append(f"  → Tam Hợp {thc_hanh} SINH Dụng Thần ({hanh}) = ĐẠI CÁT! ✅")
                                reasons_list.append(f"Tam Hợp sinh DT")
                            elif 'KHẮC' in thc_rel:
                                lines.append(f"  → Tam Hợp {thc_hanh} KHẮC Dụng Thần ({hanh}) = Bất lợi ⚠️")
                                reasons_list.append(f"Tam Hợp khắc DT")
                        break
            
            # ====== V9.0: LỤC XUNG / LỤC HỢP giữa Thế - Ứng ======
            if the_hao and ung_hao:
                the_chi = the_hao.get('chi', '')
                ung_chi = ung_hao.get('chi', '')
                if the_chi and ung_chi:
                    if LUC_XUNG_CHI.get(the_chi) == ung_chi:
                        lines.append(f"\n**⚡ LỤC XUNG THẾ-ỨNG:** {the_chi} xung {ung_chi}")
                        lines.append(f"  → Người hỏi và đối phương/sự việc XUNG ĐỘT, khó hòa hợp!")
                        reasons_list.append("Thế Ứng Lục Xung")
                    elif LUC_HOP_CHI.get(the_chi) == ung_chi:
                        lines.append(f"\n**🤝 LỤC HỢP THẾ-ỨNG:** {the_chi} hợp {ung_chi}")
                        lines.append(f"  → Người hỏi và đối phương HÒA HỢP, sự việc THUẬN LỢI! ✅")
                        reasons_list.append("Thế Ứng Lục Hợp")
            
            # ====== V9.0 Phase 4: LỤC HÀO RULES (18 QUY TẮC VÀNG) ======
            if LUC_HAO_RULES and dung_than_hao:
                matched_rules = []
                dt_hanh_r = dung_than_hao.get('ngu_hanh', '')
                dt_vuong_r = str(dung_than_hao.get('vuong_suy', ''))
                dt_chi_r = dung_than_hao.get('chi', '')
                is_dt_dong = (dung_than_idx in dong_hao) if dung_than_idx and dong_hao else False
                
                for rule in LUC_HAO_RULES:
                    rid = rule.get('id', '')
                    # R01: Dụng Thần Vượng
                    if rid == 'R01' and ('Vượng' in dt_vuong_r or 'Tướng' in dt_vuong_r):
                        matched_rules.append(rule)
                    # R02: Dụng Thần Suy
                    elif rid == 'R02' and ('Suy' in dt_vuong_r or 'Tử' in dt_vuong_r or 'Tuyệt' in dt_vuong_r):
                        matched_rules.append(rule)
                    # R03: Không Vong (cần chart_data — bỏ qua nếu không có)
                    elif rid == 'R03':
                        pass  # Skip: chart_data không có trong scope _analyze_luc_hao_full
                    # R05: Nguyên Thần Vượng Động
                    elif rid == 'R05' and 'Nguyên Thần động' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    # R06: Kỵ Thần Vượng Động
                    elif rid == 'R06' and 'Kỵ Thần động' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    # R10: Tấn Thần
                    elif rid == 'R10' and 'Tấn Thần' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    # R11: Thoái Thần
                    elif rid == 'R11' and 'Thoái Thần' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    # R13: Thế Vượng Ứng Suy
                    elif rid == 'R13' and 'Thế khắc Ứng' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    # R14: Ứng Khắc Thế
                    elif rid == 'R14' and 'Thế bị Ứng khắc' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    # R15/R16: Lục Hợp/Xung Quái
                    elif rid == 'R15' and 'Thế Ứng Lục Hợp' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                    elif rid == 'R16' and 'Thế Ứng Lục Xung' in ' '.join(reasons_list):
                        matched_rules.append(rule)
                
                if matched_rules:
                    lines.append(f"\n**📚 [KB] LỤC HÀO RULES MATCHED ({len(matched_rules)}):**")
                    for mr in matched_rules[:5]:  # Max 5 để tránh quá dài
                        lines.append(f"  - **{mr['ten']}** ({mr['id']}): {mr['ket_luan']}")
                        # Cập nhật verdict nếu rule khẳng định mạnh
                        if mr.get('muc_do') == 'ĐẠI CÁT' and verdict != 'HUNG':
                            verdict = 'CÁT'
                        elif mr.get('muc_do') == 'ĐẠI HUNG' and verdict != 'CÁT':
                            verdict = 'HUNG'
            
            # ====== V9.0 Phase 4: NHẬT NGUYỆT RULES (8 quy tắc) ======
            # Lấy can/chi ngày từ luc_hao_data thay vì chart_data (không có trong scope)
            _lh_can_ngay = luc_hao_data.get('can_ngay', '') or luc_hao_data.get('ban', {}).get('can_ngay', '')
            _lh_chi_ngay = luc_hao_data.get('chi_ngay', '') or luc_hao_data.get('ban', {}).get('chi_ngay', '')
            _lh_chi_thang = luc_hao_data.get('chi_thang', '')
            if NHAT_NGUYET_RULES and dung_than_hao and (_lh_can_ngay or _lh_chi_ngay):
                dt_hanh_nn = dung_than_hao.get('ngu_hanh', '')
                dt_chi_nn = dung_than_hao.get('chi', '')
                chi_ngay_nn = _lh_chi_ngay
                chi_thang_nn = _lh_chi_thang
                can_ngay_nn = _lh_can_ngay
                hanh_ngay = CAN_NGU_HANH.get(can_ngay_nn, '')
                hanh_thang = CHI_NGU_HANH.get(chi_thang_nn, '')
                
                nn_matched = []
                for nn_rule in NHAT_NGUYET_RULES:
                    nid = nn_rule.get('id', '')
                    # NN01: Nhật Thần Sinh DT
                    if nid == 'NN01' and hanh_ngay and dt_hanh_nn and SINH.get(hanh_ngay) == dt_hanh_nn:
                        nn_matched.append(nn_rule)
                    # NN02: Nhật Thần Khắc DT
                    elif nid == 'NN02' and hanh_ngay and dt_hanh_nn and KHAC.get(hanh_ngay) == dt_hanh_nn:
                        nn_matched.append(nn_rule)
                    # NN03: Nguyệt Thần Sinh DT
                    elif nid == 'NN03' and hanh_thang and dt_hanh_nn and SINH.get(hanh_thang) == dt_hanh_nn:
                        nn_matched.append(nn_rule)
                    # NN04: Nguyệt Phá
                    elif nid == 'NN04' and chi_thang_nn and dt_chi_nn and LUC_XUNG_CHI.get(chi_thang_nn) == dt_chi_nn:
                        nn_matched.append(nn_rule)
                    # NN07: Nhật Hợp DT
                    elif nid == 'NN07' and chi_ngay_nn and dt_chi_nn and LUC_HOP_CHI.get(chi_ngay_nn) == dt_chi_nn:
                        nn_matched.append(nn_rule)
                    # NN08: Nhật Xung DT (Ám Động)
                    elif nid == 'NN08' and chi_ngay_nn and dt_chi_nn and LUC_XUNG_CHI.get(chi_ngay_nn) == dt_chi_nn and not (dung_than_idx and dung_than_idx in (dong_hao or [])):
                        nn_matched.append(nn_rule)
                
                # NN05/NN06: Kiểm tra Nhật Nguyệt đồng sinh/khắc
                ngay_sinh_dt = hanh_ngay and dt_hanh_nn and SINH.get(hanh_ngay) == dt_hanh_nn
                thang_sinh_dt = hanh_thang and dt_hanh_nn and SINH.get(hanh_thang) == dt_hanh_nn
                ngay_khac_dt = hanh_ngay and dt_hanh_nn and KHAC.get(hanh_ngay) == dt_hanh_nn
                thang_khac_dt = hanh_thang and dt_hanh_nn and KHAC.get(hanh_thang) == dt_hanh_nn
                if ngay_sinh_dt and thang_sinh_dt:
                    for nr in NHAT_NGUYET_RULES:
                        if nr.get('id') == 'NN05':
                            nn_matched.append(nr)
                            break
                if ngay_khac_dt and thang_khac_dt:
                    for nr in NHAT_NGUYET_RULES:
                        if nr.get('id') == 'NN06':
                            nn_matched.append(nr)
                            break
                
                if nn_matched:
                    lines.append(f"\n**📚 [KB] NHẬT NGUYỆT RULES ({len(nn_matched)}):**")
                    for nmr in nn_matched[:4]:
                        lines.append(f"  - **{nmr['ten']}** ({nmr['id']}): {nmr['ket_luan']}")
                        if nmr.get('muc_do') == 'ĐẠI CÁT':
                            if verdict in ['BÌNH', 'HUNG']:
                                verdict = 'CÁT'
                                reasons_list.append(nmr['ten'])
                        elif nmr.get('muc_do') == 'ĐẠI HUNG':
                            verdict = 'HUNG'
                            reasons_list.append(nmr['ten'])
            
            # ====== V9.0 Phase 4: HÀO BIẾN RULES (5 quy tắc) ======
            if HAO_BIEN_RULES and dung_than_hao and dong_hao and dung_than_idx and dung_than_idx in dong_hao:
                bien_haos_r = bien.get('haos') or bien.get('details', []) if bien else []
                if bien_haos_r and dung_than_idx <= len(bien_haos_r):
                    bien_hao = bien_haos_r[dung_than_idx - 1]
                    bien_hanh = bien_hao.get('ngu_hanh', '')
                    bien_chi = bien_hao.get('chi', '')
                    dt_hanh_hb = dung_than_hao.get('ngu_hanh', '')
                    dt_chi_hb = dung_than_hao.get('chi', '')
                    
                    hb_matched = []
                    for hb_rule in HAO_BIEN_RULES:
                        hbid = hb_rule.get('id', '')
                        # HB01: Hóa Hồi Đầu Sinh
                        if hbid == 'HB01' and bien_hanh and dt_hanh_hb and SINH.get(bien_hanh) == dt_hanh_hb:
                            hb_matched.append(hb_rule)
                        # HB02: Hóa Hợp
                        elif hbid == 'HB02' and bien_chi and dt_chi_hb and LUC_HOP_CHI.get(dt_chi_hb) == bien_chi:
                            hb_matched.append(hb_rule)
                        # HB03: Hóa Không Vong (dùng can/chi ngày từ luc_hao_data)
                        elif hbid == 'HB03' and bien_chi and _lh_can_ngay and _lh_chi_ngay:
                            kv_hb = _get_khong_vong(_lh_can_ngay, _lh_chi_ngay)
                            if bien_chi in kv_hb:
                                hb_matched.append(hb_rule)
                    
                    if hb_matched:
                        lines.append(f"\n**📚 [KB] HÀO BIẾN RULES ({len(hb_matched)}):**")
                        for hbm in hb_matched:
                            lines.append(f"  - **{hbm['ten']}** ({hbm['id']}): {hbm['ket_luan']}")
                            if hbm.get('muc_do') == 'ĐẠI CÁT' and verdict != 'HUNG':
                                verdict = 'CÁT'
                                reasons_list.append(hbm['ten'])
                            elif hbm.get('muc_do') in ['HUNG', 'ĐẠI HUNG']:
                                verdict = 'HUNG'
                                reasons_list.append(hbm['ten'])
            
            # ====== V42.0: ỨNG KỲ CHUYÊN SÂU ======
            if hanh and verdict:
                # Basic ứng kỳ
                ung_ky_text = _get_ung_ky(hanh, verdict)
                lines.append(f"\n**⏰ ỨNG KỲ CHUYÊN SÂU:**")
                lines.append(f"  {ung_ky_text}")
                # Advanced ứng kỳ
                dt_chi_uk = dung_than_hao.get('chi', '') if dung_than_hao else ''
                uk_advanced = _get_ung_ky_advanced(
                    hanh, verdict, dt_chi_uk,
                    can_ngay_lh, chi_ngay_lh,
                    luc_hao_data.get('chi_thang', ''),
                    '',  # ts_stage not available in LH scope
                    khong_vong_list
                )
                if uk_advanced:
                    for uk_line in uk_advanced.split('\n'):
                        lines.append(f"  {uk_line}")
            
            # V8.0: ĐẾM SỐ LƯỢNG (anh chị em = Huynh Đệ)
            if is_count:
                lines.append(f"\n**📊 ĐẾM SỐ (Lục Hào):**")
                lines.append(f"- Số hào Huynh Đệ trong quẻ: **{huynh_de_count}**")
                if huynh_de_count > 0:
                    count_num = huynh_de_count
                    lines.append(f"- → **Số anh chị em (Lục Hào): khoảng {count_num} người**")
                else:
                    count_num = 1
                    lines.append(f"- Không có Huynh Đệ → Ít anh em, khoảng 1")
            
            # Tuổi — V32.6: Dùng Trường Sinh stage
            if is_age and the_hao:
                vuong_str = str(vuong)
                lh_age_stage = ''
                for stage_name in TRUONG_SINH_POWER:
                    if stage_name in vuong_str:
                        lh_age_stage = stage_name
                        break
                if not lh_age_stage:
                    if 'Vượng' in vuong_str: lh_age_stage = 'Đế Vượng'
                    elif 'Tướng' in vuong_str: lh_age_stage = 'Lâm Quan'
                    elif 'Hưu' in vuong_str: lh_age_stage = 'Suy'
                    elif 'Tù' in vuong_str: lh_age_stage = 'Bệnh'
                    elif 'Tử' in vuong_str: lh_age_stage = 'Tử'
                    else: lh_age_stage = 'Quan Đới'
                
                ts_d = TRUONG_SINH_POWER.get(lh_age_stage, {})
                t_min = ts_d.get('tuoi_min', 0)
                t_max = ts_d.get('tuoi_max', 0)
                age_num = (t_min + t_max) // 2
                lines.append(f"- Trường Sinh DT: **{lh_age_stage}** → {t_min}-{t_max} tuổi")
                lines.append(f"- → **Tuổi ước tính (LH): khoảng {t_min}-{t_max} tuổi**")
        else:
            lines.append("- Không tìm thấy Dụng Thần trong quẻ.")
            reasons_list.append("Thiếu Dụng Thần")
        
        reason = " + ".join(reasons_list) if reasons_list else "Cân bằng"
        lines.append(f"\n  → **LỤC HÀO: {verdict}** ({reason})")
        lines.append("")
        return "\n".join(lines), verdict, age_num, reason, count_num


    # ===========================
    # MAI HOA ANALYSIS
    # ===========================
    def _analyze_mai_hoa_full(self, mai_hoa_data, is_age):
        """V8.0 — Mai Hoa: Hỗ Quái + Ý nghĩa quái tượng + Liên hệ câu hỏi"""
        lines = []
        verdict = "BÌNH"
        age_num = None
        
        try:
            from mai_hoa_dich_so import QUAI_ELEMENTS, QUAI_NAMES
        except ImportError:
            QUAI_ELEMENTS = {}
            QUAI_NAMES = {}
        
        dong_hao = mai_hoa_data.get('dong_hao', 1)
        upper = mai_hoa_data.get('upper', 0)
        lower = mai_hoa_data.get('lower', 0)
        
        if dong_hao <= 3:
            the_quai, dung_quai = upper, lower
            the_label, dung_label = "Thượng quái", "Hạ quái"
        else:
            the_quai, dung_quai = lower, upper
            the_label, dung_label = "Hạ quái", "Thượng quái"
        
        the_el = QUAI_ELEMENTS.get(the_quai, '?')
        dung_el = QUAI_ELEMENTS.get(dung_quai, '?')
        the_name = QUAI_NAMES.get(the_quai, '?')
        dung_name = QUAI_NAMES.get(dung_quai, '?')
        
        lines.append(f"- **🌟 Thể Quẻ ({the_label}):** {the_name} | Hành {the_el}")
        lines.append(f"- **⚡ Dụng Quẻ ({dung_label}):** {dung_name} | Hành {dung_el}")
        lines.append(f"- **Quẻ Chủ:** {mai_hoa_data.get('ten', '?')}")
        lines.append(f"- **Quẻ Biến:** {mai_hoa_data.get('ten_qua_bien', '?')}")
        lines.append(f"- **Hào Động:** {dong_hao}")
        
        # V42.2: Hỗ Quẻ từ data (nếu có sẵn)
        if mai_hoa_data.get('ten_ho'):
            lines.append(f"- **🔍 Hỗ Quẻ (Quẻ ẩn):** {mai_hoa_data.get('ten_ho', '?')}")
        if mai_hoa_data.get('ten_bien'):
            lines.append(f"- **🔄 Biến Quẻ:** {mai_hoa_data.get('ten_bien', mai_hoa_data.get('ten_qua_bien', '?'))}")

        
        # V8.1: Đọc Tượng Quẻ + Ý Nghĩa từ phần mềm (nếu có)
        tuong = mai_hoa_data.get('tuong', '')
        nghia = mai_hoa_data.get('nghĩa', '') or mai_hoa_data.get('nghia', '')
        interpretation = mai_hoa_data.get('interpretation', '')
        if tuong:
            lines.append(f"- 🖼️ **Tượng Quẻ:** {tuong}")
        if nghia:
            lines.append(f"- 📖 **Ý nghĩa:** {nghia}")
        if interpretation:
            lines.append(f"- 💡 **Luận giải phần mềm:** {interpretation[:300]}")
        
        # V8.0: Ý NGHĨA QUÁI TƯỢNG
        the_yn = QUAI_Y_NGHIA.get(the_name, {})
        dung_yn = QUAI_Y_NGHIA.get(dung_name, {})
        if the_yn:
            lines.append(f"\n  📖 **Thể ({the_name}):** {the_yn.get('tuong', '')} — {the_yn.get('tc', '')}")
        if dung_yn:
            lines.append(f"  📖 **Dụng ({dung_name}):** {dung_yn.get('tuong', '')} — {dung_yn.get('tc', '')}")
        
        # V8.1: HỖ QUÁI — quẻ ẩn bên trong (nguyên nhân sâu xa)
        hao_list = mai_hoa_data.get('hao_list', []) or mai_hoa_data.get('lines', [])  # V8.1: fallback
        # V8.1: Nếu phần mềm đã tính sẵn Hỗ Quái
        if mai_hoa_data.get('ten_ho'):
            lines.append(f"\n  **🔍 Hỗ Quái:** {mai_hoa_data.get('ten_ho', '?')}")
            ho_yn = QUAI_Y_NGHIA.get(mai_hoa_data.get('ten_ho', ''), {})
            if ho_yn:
                lines.append(f"  - Ý nghĩa ẩn: {ho_yn.get('tuong', '')} — {ho_yn.get('tc', '')}")
        elif len(hao_list) >= 6:
            # Hỗ Quái: Hạ Hỗ = Hào 2,3,4; Thượng Hỗ = Hào 3,4,5
            ha_ho = (hao_list[1], hao_list[2], hao_list[3])
            thuong_ho = (hao_list[2], hao_list[3], hao_list[4])
            # Convert to quái number
            ha_ho_num = ha_ho[0] + ha_ho[1]*2 + ha_ho[2]*4
            thuong_ho_num = thuong_ho[0] + thuong_ho[1]*2 + thuong_ho[2]*4
            ha_ho_name = QUAI_NAMES.get(ha_ho_num, '?')
            thuong_ho_name = QUAI_NAMES.get(thuong_ho_num, '?')
            ha_ho_el = QUAI_ELEMENTS.get(ha_ho_num, '?')
            thuong_ho_el = QUAI_ELEMENTS.get(thuong_ho_num, '?')
            lines.append(f"\n  **🔍 Hỗ Quái (nguyên nhân sâu xa):**")
            lines.append(f"  - Thượng Hỗ: **{thuong_ho_name}** ({thuong_ho_el})")
            lines.append(f"  - Hạ Hỗ: **{ha_ho_name}** ({ha_ho_el})")
            ho_yn = QUAI_Y_NGHIA.get(thuong_ho_name, {})
            if ho_yn:
                lines.append(f"  - Ý nghĩa ẩn: {ho_yn.get('tuong', '')} — {ho_yn.get('tc', '')}")
        
        # Vạn Vật cho Thể Dụng
        vvlt_the = get_bat_quai_tuong(the_name)
        if vvlt_the:
            lines.append(f"\n  **📊 Vạn Vật Thể ({the_name}):**")
            for vl in vvlt_the.split('\n')[1:5]:
                lines.append(f"  {vl}")
        vvlt_dung = get_bat_quai_tuong(dung_name)
        if vvlt_dung:
            lines.append(f"\n  **📊 Vạn Vật Dụng ({dung_name}):**")
            for vl in vvlt_dung.split('\n')[1:5]:
                lines.append(f"  {vl}")
        
        # Sinh khắc Thể-Dụng
        reason = "Cân bằng"
        if the_el and dung_el and the_el != '?' and dung_el != '?':
            if SINH.get(dung_el) == the_el:
                verdict = "CÁT"
                reason = f"Dụng ({dung_el}) SINH Thể ({the_el})"
                lines.append(f"- Dụng SINH Thể → **CÁT** (được lợi) ✅")
            elif KHAC.get(dung_el) == the_el:
                verdict = "HUNG"
                reason = f"Dụng ({dung_el}) KHẮC Thể ({the_el})"
                lines.append(f"- Dụng KHẮC Thể → **HUNG** (bất lợi) ⚠️")
            elif KHAC.get(the_el) == dung_el:
                verdict = "CÁT"
                reason = f"Thể ({the_el}) KHẮC Dụng ({dung_el})"
                lines.append(f"- Thể KHẮC Dụng → **CÁT** (mình thắng) ✅")
            elif SINH.get(the_el) == dung_el:
                verdict = "BÌNH"
                reason = f"Thể ({the_el}) SINH Dụng ({dung_el}) = hao tổn"
                lines.append(f"- Thể SINH Dụng → **BÌNH** (hao tổn)")
            else:
                reason = "Tỷ Hòa"
                lines.append(f"- Thể-Dụng Tỷ Hòa → **BÌNH**")
        
        # V9.0 KB: Tra MAI_HOA_THE_DUNG cho phân tích chi tiết
        if the_el and dung_el and the_el != '?' and dung_el != '?' and MAI_HOA_THE_DUNG:
            td_key = (the_el, dung_el)
            td_info = MAI_HOA_THE_DUNG.get(td_key, {})
            if td_info:
                lines.append(f"\n  **📊 [KB] Thể Dụng Chi Tiết:** {td_info.get('quan_he', '')} → **{td_info.get('ket_luan', '')}**")
                lines.append(f"  → {td_info.get('chi_tiet', '')}")
                # Ứng Kỳ KB
                if MAI_HOA_UNG_KY:
                    uk_info = MAI_HOA_UNG_KY.get(td_info.get('quan_he', ''), {})
                    if uk_info:
                        lines.append(f"  ⏰ Ứng Kỳ: {uk_info.get('giai_thich', '')} (tốc độ: {uk_info.get('toc_do', '?')})")
        
        # ====== V9.0: LỆNH THÁNG VƯỢNG SUY ======
        lenh_hanh, lenh_mua = _get_lenh_thang_hanh()
        if the_el and the_el != '?':
            if the_el == lenh_hanh:
                lines.append(f"\n**🌿 LỆNH THÁNG:** {lenh_mua} — {lenh_hanh} vượng")
                lines.append(f"  → Thể quái ({the_el}) ĐANG VƯỢNG theo mùa = Sức mạnh TĂNG GẤP ĐÔI! ✅")
                if verdict == "HUNG":
                    verdict = "BÌNH"
                    reason += " + Thể vượng lệnh"
            elif KHAC.get(lenh_hanh) == the_el:
                lines.append(f"\n**🍂 LỆNH THÁNG:** {lenh_mua} — {lenh_hanh} vượng")
                lines.append(f"  → Thể quái ({the_el}) BỊ KHẮC bởi Lệnh Tháng ({lenh_hanh}) = SUY YẾU ⚠️")
                if verdict == "CÁT":
                    verdict = "BÌNH"
                    reason += " + Thể suy lệnh"
        
        # ====== V9.0: HỖ QUÁI SINH KHẮC THỂ ======
        ho_el = None
        ho_name_for_check = mai_hoa_data.get('ten_ho', '')
        if ho_name_for_check:
            ho_yn_check = QUAI_Y_NGHIA.get(ho_name_for_check, {})
            ho_el = ho_yn_check.get('hanh', '')
        if ho_el and the_el and the_el != '?':
            if SINH.get(ho_el) == the_el:
                lines.append(f"\n**🤝 HỖ QUÁI SINH THỂ:** Hỗ ({ho_el}) sinh Thể ({the_el})")
                lines.append(f"  → Có QUÝ NHÂN ẨN giúp đỡ, sự việc có nền tảng bên trong! ✅")
            elif KHAC.get(ho_el) == the_el:
                lines.append(f"\n**⚠️ HỖ QUÁI KHẮC THỂ:** Hỗ ({ho_el}) khắc Thể ({the_el})")
                lines.append(f"  → Có TRỞ NGẠI ẨN chưa thấy, bên trong có vấn đề ngầm!")
        
        # ====== V9.0: BIẾN QUÁI SINH KHẮC THỂ ======
        ten_bien = mai_hoa_data.get('ten_qua_bien', '')
        if ten_bien:
            # Tìm quái biến trong QUAI_Y_NGHIA
            bien_parts = ten_bien.split()
            for bp in bien_parts:
                bien_yn = QUAI_Y_NGHIA.get(bp, {})
                if bien_yn:
                    bien_el = bien_yn.get('hanh', '')
                    if bien_el and the_el and the_el != '?':
                        if SINH.get(bien_el) == the_el:
                            lines.append(f"\n**🔮 BIẾN QUÁI SINH THỂ:** Biến ({bien_el}) sinh Thể ({the_el})")
                            lines.append(f"  → Kết cục TỐT HƠN dự kiến, có chuyển biến tích cực! ✅")
                        elif KHAC.get(bien_el) == the_el:
                            lines.append(f"\n**🔮 BIẾN QUÁI KHẮC THỂ:** Biến ({bien_el}) khắc Thể ({the_el})")
                            lines.append(f"  → Kết cục XẤU HƠN, hậu quả lâu dài, cần đề phòng! ⚠️")
                    break
        
        # ====== V9.0: ỨNG KỲ MAI HOA ======
        if the_el and the_el != '?':
            ung_ky_text = _get_ung_ky(the_el, verdict)
            lines.append(f"\n**⏰ ỨNG KỲ:** {ung_ky_text}")
        
        lines.append(f"\n  → **MAI HOA: {verdict}** ({reason})")
        
        # Tuổi — V32.6: Dùng Trường Sinh từ Thể-Dụng
        if is_age:
            if verdict == 'CÁT':
                mh_age_stage = 'Đế Vượng'  # 31-45
            elif verdict == 'HUNG':
                mh_age_stage = 'Suy'  # 46-55
            else:
                mh_age_stage = 'Lâm Quan'  # 16-30
            
            ts_mh = TRUONG_SINH_POWER.get(mh_age_stage, {})
            tm_min = ts_mh.get('tuoi_min', 0)
            tm_max = ts_mh.get('tuoi_max', 0)
            age_num = (tm_min + tm_max) // 2
            lines.append(f"- Trường Sinh: **{mh_age_stage}** → {tm_min}-{tm_max} tuổi")
            lines.append(f"- → **Tuổi ước tính (MH): khoảng {tm_min}-{tm_max} tuổi**")
        
        lines.append("")
        return "\n".join(lines), verdict, age_num


    # ===========================
    # THIẾT BẢN + KINH DỊCH + VẠN VẬT
    # ===========================
    def _analyze_thiet_ban_kinh_dich_van_vat(self, question, chart_data, luc_hao_data, mai_hoa_data):
        lines = []
        
        # --- A. THIẾT BẢN THẦN TOÁN (Nạp Âm) ---
        lines.append("**📜 A. Thiết Bản Thần Toán:**")
        nap_am_found = False
        
        # Extract Nạp Âm từ câu hỏi
        if question and 'Nạp Âm' in question:
            nap_am_matches = re.findall(r'Nạp Âm[^:]*:\s*(.+?)(?:\n|$)', question)
            for na in nap_am_matches:
                na_clean = na.strip()
                lines.append(f"- Nạp Âm: **{na_clean}**")
                nap_am_found = True
                
                # Tra bảng Nạp Âm từ Vạn Vật Loại Tượng
                nap_am_table = KINH_DICH_MAI_HOA_THIET_BAN.get("thiet_ban", {}).get("nap_am_table", [])
                for row in nap_am_table:
                    if len(row) >= 4 and row[1] in na_clean:
                        lines.append(f"  → Can Chi: {row[0]} | Hành: **{row[2]}** | Nghĩa: {row[3]}")
                        # V8.0: Giải thích ý nghĩa biểu tượng
                        na_explain = NAP_AM_GIAI_THICH.get(row[1].strip(), '')
                        if na_explain:
                            lines.append(f"  → 📖 **Ý nghĩa:** {na_explain}")
                        break
        
        if not nap_am_found:
            # Thử lấy từ chart_data nếu có
            if chart_data and isinstance(chart_data, dict):
                can_ngay = chart_data.get('can_ngay', '')
                chi_ngay = chart_data.get('chi_ngay', '')
                if can_ngay and chi_ngay:
                    lines.append(f"- Trụ Ngày: **{can_ngay} {chi_ngay}**")
                    # Tra Nạp Âm
                    nap_am_table = KINH_DICH_MAI_HOA_THIET_BAN.get("thiet_ban", {}).get("nap_am_table", [])
                    pair = f"{can_ngay} {chi_ngay}"
                    for row in nap_am_table:
                        if len(row) >= 4 and pair in row[0]:
                            lines.append(f"  → Nạp Âm: **{row[1]}** ({row[2]}) — {row[3]}")
                            # V8.0: Giải thích ý nghĩa biểu tượng
                            na_explain = NAP_AM_GIAI_THICH.get(row[1].strip(), '')
                            if na_explain:
                                lines.append(f"  → 📖 **Ý nghĩa:** {na_explain}")
                            nap_am_found = True
                            break
                # V9.0 KB: Fallback tra THIET_BAN_60 nếu bảng cũ không có
                if not nap_am_found and can_ngay and chi_ngay and THIET_BAN_60:
                    pair = f"{can_ngay} {chi_ngay}"
                    tb60 = THIET_BAN_60.get(pair, {})
                    if tb60:
                        lines.append(f"  → Nạp Âm: **{tb60['nap_am']}** ({tb60['hanh']}) — {tb60['giai_thich']}")
                        nap_am_found = True
            if not nap_am_found:
                lines.append("- Chưa tra được Nạp Âm từ dữ liệu hiện có.")
        # ====== V9.0: TRƯỜNG SINH CHO NẠP ÂM ======
        if nap_am_found and chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            chi_ngay = chart_data.get('chi_ngay', '')
            hanh_can = CAN_NGU_HANH.get(can_ngay, '')
            if hanh_can and chi_ngay:
                ts_stage, ts_explain = _get_truong_sinh(hanh_can, chi_ngay)
                if ts_stage:
                    lines.append(f"\n  **🔄 Trường Sinh Nạp Âm:** {hanh_can} tại {chi_ngay} = **{ts_stage}**")
                    lines.append(f"  → {ts_explain}")
        
        # ====== V9.0: THẦN SÁT ANALYSIS ======
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            chi_ngay = chart_data.get('chi_ngay', '')
            than_sat_results = []
            
            # Check Thiên Ất Quý Nhân
            qn_data = THAN_SAT_TABLE['cat'].get('Thiên Ất Quý Nhân', {})
            qn_chi_list = qn_data.get('chi_list', {}).get(can_ngay, [])
            if chi_ngay in qn_chi_list:
                than_sat_results.append(('CÁT', qn_data['giai_thich']))
            
            # Check Dương Nhận
            dn_data = THAN_SAT_TABLE['hung'].get('Dương Nhận', {})
            dn_chi = dn_data.get('chi_map', {}).get(can_ngay, '')
            if dn_chi and chi_ngay == dn_chi:
                than_sat_results.append(('HUNG', dn_data['giai_thich']))
            
            if than_sat_results:
                lines.append(f"\n**🌟 THẦN SÁT:**")
                for sat_type, sat_desc in than_sat_results:
                    lines.append(f"  - {sat_desc}")
        
        # --- B. KINH DỊCH (64 Quẻ) ---
        lines.append("")
        lines.append("**☯️ B. Kinh Dịch — Quẻ Tượng:**")
        
        hex_name = None
        hex_palace = None
        
        if luc_hao_data and isinstance(luc_hao_data, dict):
            ban = luc_hao_data.get('ban', {})
            hex_name = ban.get('name', '')
            hex_palace = ban.get('palace', '')
            
            if hex_name:
                lines.append(f"- Quẻ Chủ: **{hex_name}**")
                if hex_palace:
                    lines.append(f"- Thuộc Cung: **{hex_palace}**")
                
                # V9.0 Phase 4: Tra BAN_CUNG từ Knowledge Base
                if BAN_CUNG and hex_name:
                    bc_cung, bc_hanh = tra_ban_cung(hex_name)
                    if bc_cung:
                        lines.append(f"  - 📚 **[KB Bản Cung]** {hex_name} → Cung **{bc_cung}** (Hành **{bc_hanh}**)")
                
                # Thế/Ứng
                the_pos = THE_POSITION.get(hex_name)
                if the_pos:
                    ung_pos = ((the_pos - 1 + 3) % 6) + 1
                    lines.append(f"- Hào Thế: **{the_pos}** | Hào Ứng: **{ung_pos}**")
                
                # Tra Kinh Dịch cơ bản
                kinh_dich_data = KINH_DICH_MAI_HOA_THIET_BAN.get("kinh_dich", {}).get("data", [])
                for qd in kinh_dich_data:
                    if qd.get("tượng", "") in hex_name or hex_name.startswith(qd.get("quẻ", "").replace("☰ ", "").replace("☱ ", "").replace("☲ ", "").replace("☳ ", "").replace("☴ ", "").replace("☵ ", "").replace("☶ ", "").replace("☷ ", "")):
                        lines.append(f"  → Tượng: {qd.get('tượng', '?')} | Đức: {qd.get('đức', '?')} | Ý nghĩa: {qd.get('ý_nghĩa', '?')}")
                        break
                
                # ====== V9.0: THOÁN TỪ + ĐẠI TƯỢNG ======
                if hex_palace:
                    thoan_info = QUE_THOAN_DAI_TUONG.get(hex_palace, {})
                    if thoan_info:
                        lines.append(f"\n  **📜 THOÁN TỪ:** {thoan_info.get('thoan', '')}")
                        lines.append(f"  **🏔️ ĐẠI TƯỢNG:** {thoan_info.get('dai_tuong', '')}")
                        lines.append(f"  **💡 Lời khuyên:** {thoan_info.get('lk', '')}")
                
                # V9.0 KB: Tra 64 quẻ Kinh Dịch chi tiết
                if hex_name and KINH_DICH_64:
                    kd64 = KINH_DICH_64.get(hex_name, {})
                    if kd64:
                        lines.append(f"\n  **📚 [KB 64 QUẺ] {hex_name}:**")
                        lines.append(f"  - 📜 Thoán Từ: {kd64.get('thoan', '')}")
                        lines.append(f"  - 🏔️ Đại Tượng: {kd64.get('dai_tuong', '')}")
                        lines.append(f"  - 💡 Ý nghĩa: {kd64.get('y_nghia', '')}")
                        lines.append(f"  - 🎯 Lời khuyên: {kd64.get('loi_khuyen', '')}")
                        lines.append(f"  - {'✅' if 'CÁT' in kd64.get('cat_hung','') else '⚠️'} Cát/Hung: **{kd64.get('cat_hung', 'BÌNH')}**")
                    
                    # Cũng tra quẻ biến
                    bien = luc_hao_data.get('bien', {})
                    bien_name = bien.get('name', '')
                    if bien_name:
                        kd64_bien = KINH_DICH_64.get(bien_name, {})
                        if kd64_bien:
                            lines.append(f"\n  **📚 [KB] Quẻ Biến {bien_name}:** {kd64_bien.get('y_nghia', '')} → **{kd64_bien.get('cat_hung', 'BÌNH')}**")
                
                # ====== V9.0: HÀO VỊ CHÍNH/BẤT CHÍNH ======
                haos = ban.get('haos') or ban.get('details', [])
                if haos and the_pos:
                    hao_the = haos[the_pos - 1] if the_pos <= len(haos) else None
                    if hao_the:
                        am_duong = hao_the.get('am_duong', '')
                        # Vị lẻ (1,3,5) = Dương vị, vị chẵn (2,4,6) = Âm vị
                        vi_duong = the_pos % 2 == 1
                        hao_duong = am_duong in ['dương', 'Dương', '⚊', '---', 1, '1']
                        is_chinh = (hao_duong and vi_duong) or (not hao_duong and not vi_duong)
                        is_trung = the_pos in [2, 5]
                        
                        chinh_text = "CHÍNH VỊ ✅" if is_chinh else "BẤT CHÍNH ⚠️"
                        trung_text = " + TRUNG (cân bằng hoàn hảo) 🌟" if is_trung else ""
                        lines.append(f"\n  **📐 HÀO VỊ:** Hào Thế ({the_pos}) = **{chinh_text}**{trung_text}")
                        if is_chinh and is_trung:
                            lines.append(f"  → Chính + Trung = Vị trí HOÀN HẢO — Sự việc THUẬN LỢI nhất!")
                        elif not is_chinh:
                            lines.append(f"  → Bất Chính = Sai vị trí — Cần ĐIỀU CHỈNH phương pháp tiếp cận")
            
            bien = luc_hao_data.get('bien', {})
            bien_name = bien.get('name', '')
            if bien_name:
                lines.append(f"- Quẻ Biến: **{bien_name}**")
        elif mai_hoa_data and isinstance(mai_hoa_data, dict):
            ten_qua = mai_hoa_data.get('ten', '')
            if ten_qua:
                lines.append(f"- Quẻ (Mai Hoa): **{ten_qua}**")
                hex_palace = HEXAGRAM_PALACES.get(ten_qua, '')
                if hex_palace:
                    lines.append(f"- Thuộc Cung: **{hex_palace}**")
                    # V9.0: Thoán Từ cho Mai Hoa
                    thoan_info = QUE_THOAN_DAI_TUONG.get(hex_palace, {})
                    if thoan_info:
                        lines.append(f"\n  **📜 THOÁN TỪ:** {thoan_info.get('thoan', '')}")
                        lines.append(f"  **💡 Lời khuyên:** {thoan_info.get('lk', '')}")
        else:
            lines.append("- Chưa có dữ liệu Kinh Dịch (cần Lục Hào hoặc Mai Hoa).")
        
        # --- C. VẠN VẬT LOẠI TƯỢNG (Bát Quái) ---
        lines.append("")
        lines.append("**🏔️ C. Vạn Vật Loại Tượng:**")
        
        # Xác định quải liên quan
        quai_to_check = set()
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            hanh_can = CAN_NGU_HANH.get(can_ngay, '')
            # Map hành → quái
            hanh_quai = {'Kim': 'CÀN', 'Mộc': 'CHẤN', 'Thủy': 'KHẢM', 'Hỏa': 'LY', 'Thổ': 'KHÔN'}
            if hanh_can in hanh_quai:
                quai_to_check.add(hanh_quai[hanh_can])
        
        if hex_palace:
            quai_to_check.add(hex_palace.upper())
        
        if quai_to_check and BAT_QUAI_LOAI_TUONG.get("rows"):
            headers = BAT_QUAI_LOAI_TUONG.get("headers", [])
            # Tìm index cột cho quái
            quai_col_map = {}
            for i, h in enumerate(headers):
                for q in ["CÀN", "ĐOÀI", "LY", "CHẤN", "TỐN", "KHẢM", "CẤN", "KHÔN"]:
                    if q in h.upper():
                        quai_col_map[q] = i
                        break
            
            for quai in quai_to_check:
                col_idx = quai_col_map.get(quai)
                if col_idx is None:
                    continue
                lines.append(f"\n**Quái {quai}:**")
                # Show key rows
                important_rows = ["Tượng Thiên Nhiên", "Nhân Vật", "Bộ Phận Cơ Thể", "Tật Bệnh", "Động Vật", "Sắc Thái"]
                for row in BAT_QUAI_LOAI_TUONG["rows"]:
                    if len(row) > col_idx and row[0] in important_rows:
                        lines.append(f"- {row[0]}: **{row[col_idx]}**")
        else:
            lines.append("- Chưa xác định được Quái liên quan từ dữ liệu.")
        
        lines.append("")
        return "\n".join(lines)

    # ===========================
    # LEGACY: analyze_palace
    # ===========================
    def analyze_palace(self, palace_data, topic):
        p_num = palace_data.get('num')
        star = palace_data.get('star')
        door = palace_data.get('door')
        deity = palace_data.get('deity')
        stem_top = palace_data.get('can_thien')
        stem_bottom = palace_data.get('can_dia')
        
        star_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(star, {})
        door_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(door + " Môn" if door else "", {})
        deity_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(deity, {})
        
        stem_key = f"{stem_top}{stem_bottom}"
        stem_info = KY_MON_DATA['TRUCTU_TRANH'].get(stem_key, {})
        
        hanh_cung = CUNG_NGU_HANH.get(p_num, '?')
        hanh_can = CAN_NGU_HANH.get(stem_top, '?')
        rel = _ngu_hanh_relation(hanh_can, hanh_cung)
        
        return f"""
### 📋 Phân Tích Cung {p_num} ({QUAI_TUONG.get(p_num)}) — Offline V6.0

**1. Sao: {star}** — {star_info.get('Tính_Chất', 'N/A')} (Hành: {star_info.get('Hành', '?')})
**2. Cửa: {door}** — {door_info.get('Cát_Hung', 'Bình')} | {door_info.get('Luận_Đoán', '')}
**3. Thần: {deity}** — {deity_info.get('Tính_Chất', 'N/A')}
**4. Can: {stem_top}/{stem_bottom}** — {stem_info.get('Tên_Cách_Cục', 'Bình thường')} ({stem_info.get('Cát_Hung', 'Bình')})
**5. Ngũ Hành:** {hanh_can} vs Cung {hanh_cung} → {rel}

**💡 Kết luận:** {door_info.get('Cát_Hung', 'Bình')}. Cách cục {stem_info.get('Tên_Cách_Cục', 'N/A')}.
"""

    def explain_element(self, element_type, element_name):
        info = ""
        category = ""
        if element_type == 'star':
            category = "Cửu Tinh"
            data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(element_name, {})
            info = f"Ngũ hành: {data.get('Hành')}. {data.get('Tính_Chất')}"
        elif element_type == 'door':
            category = "Bát Môn"
            name_lookup = element_name if "Môn" in element_name else element_name + " Môn"
            data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(name_lookup, {})
            info = f"Cát/Hung: {data.get('Cát_Hung')}. {data.get('Luận_Đoán')}"
        elif element_type == 'deity':
            category = "Bát Thần"
            data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(element_name, {})
            info = f"{data.get('Tính_Chất')}"
        elif element_type == 'stem':
            category = "Thiên Can"
            info = "Tra cứu bảng Thiên Can để biết chi tiết."
        return f"**Giải thích {category}: {element_name}**\n\n{info}"

    def comprehensive_analysis(self, chart_data, topic, dung_than_list=None):
        return self.answer_question("Phân tích tổng quan", chart_data=chart_data, topic=topic)

    def analyze_luc_hao(self, luc_hao_res, topic="Chung"):
        # V32.5: Dùng grammar parser nếu có, fallback sang _get_dung_than
        dt = 'Quan Quỷ'
        try:
            parsed = v32_parse_question(topic)
            if parsed and parsed[0].get('dung_than'):
                dt = parsed[0]['dung_than']
            else:
                dt = _get_dung_than(topic)
        except Exception:
            dt = _get_dung_than(topic)
        section, verdict, _, _reason, _cnt = self._analyze_luc_hao_full(luc_hao_res, dt, False)
        return f"### ☯️ Luận Giải Lục Hào — Offline V8.0\n**Chủ đề:** {topic}\n\n{section}\n→ Kết luận: **{verdict}**"

    def analyze_mai_hoa(self, mai_hoa_res, topic="Chung"):
        section, verdict, _ = self._analyze_mai_hoa_full(mai_hoa_res, False)
        return f"### 🌸 Luận Giải Mai Hoa — Offline V8.0\n**Chủ đề:** {topic}\n\n{section}\n→ Kết luận: **{verdict}**"

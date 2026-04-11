"""
Free AI Helper V27.0 — THIÊN CƠ ĐẠI SƯ (LỤC THUẬT HỢP NHẤT + LƯỢNG HÓA SUY VƯỢNG TOÀN DIỆN)
Kết hợp Python rule-based + Gemini Online Deep Reasoning.
Sử dụng dữ liệu Kỳ Môn + Mai Hoa + Lục Hào + Thiết Bản + Đại Lục Nhâm + Thái Ất Thần Số.
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

# Bảng Dụng Thần
DUNG_THAN_MAP = {
    'tiền': 'Thê Tài', 'tài': 'Thê Tài', 'đầu tư': 'Thê Tài', 'lương': 'Thê Tài', 'vốn': 'Thê Tài',
    'việc': 'Quan Quỷ', 'sếp': 'Quan Quỷ', 'bệnh': 'Quan Quỷ', 'kiện': 'Quan Quỷ', 'thi': 'Quan Quỷ',
    'con': 'Tử Tôn', 'bình an': 'Tử Tôn', 'vui': 'Tử Tôn',
    'nhà': 'Phụ Mẫu', 'xe': 'Phụ Mẫu', 'học': 'Phụ Mẫu', 'giấy': 'Phụ Mẫu', 'hợp đồng': 'Phụ Mẫu',
    'bạn': 'Huynh Đệ', 'đối thủ': 'Huynh Đệ', 'anh': 'Huynh Đệ', 'chị': 'Huynh Đệ', 'em': 'Huynh Đệ',
    'anh chị em': 'Huynh Đệ', 'anh em': 'Huynh Đệ',
    'tuổi': 'Bản Thân', 'tôi': 'Bản Thân', 'mình': 'Bản Thân',
}

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
    'lương': ['tiền', 'thu nhập'], 'crypto': ['bitcoin', 'coin', 'tiền điện tử'],
    'bitcoin': ['crypto', 'coin'], 'chung cư': ['căn hộ'],
    'job': ['việc', 'công việc'], 'work': ['việc'],
    'love': ['yêu', 'tình'], 'crush': ['thích', 'yêu'],
    'sick': ['bệnh', 'ốm'], 'health': ['sức khỏe', 'khỏe'],
    'house': ['nhà'], 'car': ['xe', 'ô tô'],
    'exam': ['thi', 'kiểm tra'], 'marry': ['cưới', 'hôn nhân', 'kết hôn'],
    'divorce': ['ly hôn', 'chia tay'], 'invest': ['đầu tư'],
    'stock': ['chứng khoán', 'cổ phiếu'], 'travel': ['du lịch', 'đi chơi'],
    'startup': ['khởi nghiệp'], 'freelance': ['tự do'],
    'youtube': ['youtuber', 'kênh'], 'tiktok': ['livestream', 'bán hàng'],
    'bảo hiểm': ['insurance'], 'ngân hàng': ['bank', 'vay'],
    'phẫu thuật': ['mổ'], 'trầm cảm': ['stress', 'lo âu'],
    'nợ': ['vay', 'đòi'], 'thất nghiệp': ['mất việc', 'sa thải'],
    'giấc mơ': ['mộng', 'nằm mơ'], 'cúng': ['lễ', 'cầu'],
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
    """Xác định Dụng Thần từ câu hỏi"""
    q = question.lower()
    for keyword, dt in DUNG_THAN_MAP.items():
        if keyword in q:
            return dt
    return "Quan Quỷ"  # Default


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
    return any(kw in q for kw in ['tuổi', 'bao nhiêu tuổi', 'mấy tuổi', 'số tuổi', 'năm sinh'])


def _is_find_question(question):
    q = question.lower()
    return any(kw in q for kw in ['ở đâu', 'tìm', 'mất', 'đánh rơi', 'để đâu'])


def _is_yesno_question(question):
    q = question.lower()
    return any(kw in q for kw in ['có nên', 'có được', 'có không', 'nên không', 'được không', 'liệu có'])


def _is_count_question(question):
    """Phát hiện câu hỏi đếm số lượng: bao nhiêu, mấy, số lượng"""
    q = question.lower()
    return any(kw in q for kw in ['bao nhiêu', 'mấy', 'số lượng', 'đếm', 'có mấy'])


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
    'Trường Sinh': {'power': 70, 'cap': '🟢 MẠNH',      'con_nguoi': 'Trẻ sơ sinh khỏe mạnh (0-3 tuổi)', 'vat': 'MỚI, SẠCH, BẮT ĐẦU'},
    'Mộc Dục':     {'power': 50, 'cap': '🟡 TRUNG',      'con_nguoi': 'Trẻ nhỏ chưa tự lập (4-7 tuổi)', 'vat': 'CHƯA HOÀN CHỈNH, DAO ĐỘNG'},
    'Quan Đới':    {'power': 65, 'cap': '🔵 KHÁ',        'con_nguoi': 'Thiếu niên chuẩn bị (8-15 tuổi)', 'vat': 'GẦN MỚI, ĐANG CHUẨN BỊ'},
    'Lâm Quan':    {'power': 85, 'cap': '🟢 CỰC MẠNH',  'con_nguoi': 'Thanh niên sung sức (16-30 tuổi)', 'vat': 'LỚN, MỚI, TỐT, NHIỀU'},
    'Đế Vượng':    {'power': 100,'cap': '🟢 ĐỈNH CAO',  'con_nguoi': 'Trung niên cường thịnh (31-45 tuổi)', 'vat': 'LỚN NHẤT, MỚI NHẤT, NHIỀU NHẤT'},
    'Suy':         {'power': 40, 'cap': '🟠 YẾU',        'con_nguoi': 'Người bắt đầu già (46-55 tuổi)', 'vat': 'CŨ, NHỎ HƠN, GIẢM SÚT'},
    'Bệnh':        {'power': 25, 'cap': '🟠 RẤT YẾU',   'con_nguoi': 'Người bệnh nặng (56-65 tuổi)', 'vat': 'HƯ HỎNG, THIẾU, CẦN SỬA'},
    'Tử':          {'power': 10, 'cap': '🔴 CHẾT',       'con_nguoi': 'Người đã chết (66-75 tuổi)', 'vat': 'NHỎ NHẤT, HƯ HỎNG, VỠ NÁT'},
    'Mộ':          {'power': 30, 'cap': '🟠 MỘ KHỐ',     'con_nguoi': 'Được cất giữ/chôn cất, ẩn khuất', 'vat': 'CẤT KHO, ẨN GIẤU, BỊ GIỮ LẠI'},
    'Tuyệt':       {'power': 5,  'cap': '🔴 TUYỆT',     'con_nguoi': 'Tuyệt diệt, không còn dấu vết', 'vat': 'KHÔNG CÒN, ĐÃ MẤT, MÒN NÁT'},
    'Thai':        {'power': 35, 'cap': '🟡 MANH NHA',   'con_nguoi': 'Thai nhi chưa thành hình', 'vat': 'RẤT NHỎ, CHƯA RÕ RÀNG'},
    'Dưỡng':       {'power': 55, 'cap': '🟡 NUÔI DƯỠNG','con_nguoi': 'Thai gần sinh, sắp ra đời', 'vat': 'NHỎ, ĐANG PHÁT TRIỂN'},
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
        'con_nguoi': 'Trung niên sung sức nhất (31-45 tuổi)',
        'kich_thuoc': 'Rất lớn, to, cao, đồ sộ', 'tinh_trang': 'Mới tinh, hoàn hảo, đẹp',
        'so_luong': 'Rất nhiều, dồi dào, dư thừa', 'chat_luong': 'Thượng hạng, đắt tiền',
        'mau_sac': 'Sáng, rực rỡ, tươi', 'toc_do': 'Rất nhanh, tức thì', 'so': '9-10',
    },
    'VƯỢNG': {
        'range': (70, 84), 'cap': '🔵 VƯỢNG',
        'con_nguoi': 'Thanh niên sung sức (16-30 tuổi)',
        'kich_thuoc': 'Lớn, to, rộng', 'tinh_trang': 'Mới, tốt, ít lỗi',
        'so_luong': 'Nhiều, đủ dùng', 'chat_luong': 'Tốt, chất lượng cao',
        'mau_sac': 'Sáng, tươi, đẹp', 'toc_do': 'Nhanh, kịp thời', 'so': '7-8',
    },
    'TRUNG_BÌNH': {
        'range': (50, 69), 'cap': '🟡 TRUNG BÌNH',
        'con_nguoi': 'Thiếu niên hoặc trung niên bình thường (8-15 / 46-55 tuổi)',
        'kich_thuoc': 'Trung bình, vừa phải', 'tinh_trang': 'Bình thường, dùng được',
        'so_luong': 'Vừa phải, đủ', 'chat_luong': 'Trung bình, tạm',
        'mau_sac': 'Bình thường', 'toc_do': 'Trung bình, chờ đợi', 'so': '5-6',
    },
    'SUY': {
        'range': (30, 49), 'cap': '🟠 SUY',
        'con_nguoi': 'Người già bắt đầu yếu (56-65 tuổi)',
        'kich_thuoc': 'Nhỏ, hẹp, thấp', 'tinh_trang': 'Cũ, hao mòn, xuống cấp',
        'so_luong': 'Ít, thiếu, không đủ', 'chat_luong': 'Kém, giảm giá trị',
        'mau_sac': 'Nhạt, phai, xỉn', 'toc_do': 'Chậm, trì trệ', 'so': '3-4',
    },
    'RẤT_YẾU': {
        'range': (15, 29), 'cap': '🟠 RẤT YẾU',
        'con_nguoi': 'Người bệnh nặng, nằm liệt (66-75 tuổi)',
        'kich_thuoc': 'Rất nhỏ', 'tinh_trang': 'Hư hỏng, nứt vỡ',
        'so_luong': 'Rất ít, gần hết', 'chat_luong': 'Rất tệ, hàng lỗi',
        'mau_sac': 'Tối, bạc, xám', 'toc_do': 'Rất chậm', 'so': '1-2',
    },
    'TỬ_TUYỆT': {
        'range': (0, 14), 'cap': '🔴 TỬ/TUYỆT',
        'con_nguoi': 'Người đã chết, không còn sức sống',
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
    'tài_chính':    {'ky_mon': 70, 'luc_hao': 95, 'mai_hoa': 75, 'thiet_ban': 40, 'luc_nham': 60, 'thai_at': 30},
    'sự_nghiệp':    {'ky_mon': 80, 'luc_hao': 90, 'mai_hoa': 70, 'thiet_ban': 50, 'luc_nham': 65, 'thai_at': 40},
    'tình_cảm':     {'ky_mon': 65, 'luc_hao': 90, 'mai_hoa': 80, 'thiet_ban': 40, 'luc_nham': 70, 'thai_at': 30},
    'sức_khỏe':     {'ky_mon': 80, 'luc_hao': 90, 'mai_hoa': 60, 'thiet_ban': 50, 'luc_nham': 55, 'thai_at': 35},
    'tìm_đồ':       {'ky_mon': 95, 'luc_hao': 70, 'mai_hoa': 60, 'thiet_ban': 30, 'luc_nham': 85, 'thai_at': 25},
    'thời_gian':    {'ky_mon': 95, 'luc_hao': 75, 'mai_hoa': 65, 'thiet_ban': 45, 'luc_nham': 70, 'thai_at': 50},
    'phương_hướng': {'ky_mon': 95, 'luc_hao': 50, 'mai_hoa': 45, 'thiet_ban': 30, 'luc_nham': 80, 'thai_at': 60},
    'tranh_đấu':    {'ky_mon': 90, 'luc_hao': 75, 'mai_hoa': 55, 'thiet_ban': 40, 'luc_nham': 65, 'thai_at': 85},
    'tổng_quát':    {'ky_mon': 75, 'luc_hao': 80, 'mai_hoa': 85, 'thiet_ban': 55, 'luc_nham': 65, 'thai_at': 45},
    'nhà_đất':      {'ky_mon': 75, 'luc_hao': 85, 'mai_hoa': 70, 'thiet_ban': 60, 'luc_nham': 75, 'thai_at': 40},
    'thi_cử':       {'ky_mon': 70, 'luc_hao': 85, 'mai_hoa': 75, 'thiet_ban': 55, 'luc_nham': 60, 'thai_at': 35},
    'vận_mệnh':     {'ky_mon': 60, 'luc_hao': 70, 'mai_hoa': 65, 'thiet_ban': 80, 'luc_nham': 60, 'thai_at': 75},
}

# Mapping category_label → strength key
CATEGORY_TO_STRENGTH = {
    'TÀI CHÍNH': 'tài_chính', 'KINH DOANH': 'tài_chính', 'ĐẦU TƯ': 'tài_chính',
    'SỰ NGHIỆP': 'sự_nghiệp', 'CÔNG VIỆC': 'sự_nghiệp', 'THĂNG TIẾN': 'sự_nghiệp',
    'TÌNH CẢM': 'tình_cảm', 'HÔN NHÂN': 'tình_cảm', 'TÌNH YÊU': 'tình_cảm',
    'SỨC KHỎE': 'sức_khỏe', 'BỆNH TẬT': 'sức_khỏe',
    'TÌM ĐỒ': 'tìm_đồ', 'MẤT ĐỒ': 'tìm_đồ', 'TÌM NGƯỜI': 'tìm_đồ',
    'THỜI GIAN': 'thời_gian', 'BAO GIỜ': 'thời_gian', 'KHI NÀO': 'thời_gian',
    'PHƯƠNG HƯỚNG': 'phương_hướng', 'ĐI ĐÂU': 'phương_hướng',
    'TRANH ĐẤU': 'tranh_đấu', 'KIỆN TỤNG': 'tranh_đấu', 'ĐỐI THỦ': 'tranh_đấu',
    'NHÀ ĐẤT': 'nhà_đất', 'MUA NHÀ': 'nhà_đất',
    'THI CỬ': 'thi_cử', 'HỌC HÀNH': 'thi_cử',
    'VẬN MỆNH': 'vận_mệnh', 'SỐ MỆNH': 'vận_mệnh',
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
    Offline AI V26.2 — Lượng Hóa Suy Vượng Toàn Diện + 3 Tầng Unified Strength.
    V26.2: Tích hợp _calc_unified_strength_tier() (LH+TS+NK) + Ngũ Hành vật chất.
    Kế thừa V21.0: Weighted scoring 5 PP, Tiến/Thối Thần, Nguyệt Phá.
    Kế thừa V12.0: Lục Thân Relationship Engine.
    Kế thừa V9.0: Phản/Phục Ngâm, Tam Kỳ, Tam Tài, Không Vong.
    """
    def __init__(self, api_key=None):
        self.name = "Thiên Cơ Đại Sư (V27.0 Unified + Deep Integration)"
        self.version = "V26.2-Unified-Strength"
        self.model_name = "offline-rule-engine-v22.0"
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
        
        # 2) V22 Unified Strength  
        v22 = od.get('v22_unified_strength', {})
        if v22:
            lines.append(f"Unified={v22.get('unified_pct','?')}% LH={v22.get('lh_pct','?')}% TS={v22.get('ts_pct','?')}% NK={v22.get('nk_pct','?')}%")
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
            lines.append(f"V17: {od['v17_routing'][:200]}")
        
        # 6) V18 Detective compact (chi 200 ky tu)
        if od.get('v18_detective'):
            lines.append(f"V18: {od['v18_detective'][:200]}")
        
        # 7) Top factors (tat ca phuong phap, chi lay top 3 moi loai)
        factor_parts = []
        for fkey, flabel in [('v23_lh_factors','LH'),('v24_km_factors','KM'),('v24_mh_factors','MH'),('v24_ln_factors','LN'),('v24_ta_factors','TA')]:
            fdata = od.get(fkey, [])
            if fdata and isinstance(fdata, list) and len(fdata) > 0:
                factor_parts.append(f"{flabel}:[{';'.join(str(f) for f in fdata[:3])}]")
        if factor_parts:
            lines.append(f"Factors: {' | '.join(factor_parts)}")
        
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
            # V13.0: Fix key lookup — session_state uses 'gemini_key', not 'api_key'
            api_key = self._api_key
            if not api_key:
                api_key = getattr(st, 'session_state', {}).get('gemini_key')
            if not api_key:
                api_key = getattr(st, 'session_state', {}).get('_resolved_api_key')
            if not api_key:
                try:
                    api_key = st.secrets.get('GEMINI_API_KEY', '')
                except Exception:
                    pass
            
            if not api_key:
                return None  # Không có key → fallback về Python
            
            from gemini_helper import GeminiQMDGHelper
            gemini = GeminiQMDGHelper(api_key)
            # V13.0: Bỏ test_connection() — tiết kiệm 1 API call/câu hỏi
            
            self.log_step("Online AI", "RUNNING", f"Gemini đang phân tích sâu: {question[:50]}...")
            
            # === BUILD DEEP ANALYSIS PROMPT (V13.0 — Deep Reasoning) ===
            offline_ctx = ""
            rag_prompt = ""
            
            # V25.0: Truy Xuất Án Lệ Thực Tế (RAG FEEDBACK LOOP)
            if self.feedback_rag and offline_analysis_data:
                dung_than = offline_analysis_data.get('dung_than', '')
                exps = self.feedback_rag.search_experience(question, dung_than, top_k=2)
                rag_prompt = self.feedback_rag.build_rag_prompt(exps)

            if offline_analysis_data:
                od = offline_analysis_data
                
                # V27.0: VERDICT COMPACT BLOCK - Chen truoc tat ca du lieu khac
                offline_ctx += self._build_verdict_compact_block(od)
                
                # 1) Thông tin cơ bản
                offline_ctx += (
                    f"\n=== DỮ LIỆU TỪ AI OFFLINE (rule-based Python, chính xác 100%) ===\n"
                    f"Dụng Thần: {od.get('dung_than', '?')}\n"
                    f"Nhóm câu hỏi: {od.get('category_label', '?')}\n"
                )
                
                # 2) Verdicts từ 5 phương pháp (V14.0 LỤC THUẬT)
                offline_ctx += (
                    f"\n--- VERDICTS (KẾT QUẢ TỪ TỪNG PHƯƠNG PHÁP) ---\n"
                    f"Kỳ Môn: {od.get('ky_mon_verdict', '?')} — {od.get('ky_mon_reason', '')}\n"
                    f"Lục Hào: {od.get('luc_hao_verdict', '?')} — {od.get('luc_hao_reason', '')}\n"
                    f"Mai Hoa: {od.get('mai_hoa_verdict', '?')} — {od.get('mai_hoa_reason', '')}\n"
                    f"Đại Lục Nhâm: {od.get('luc_nham_verdict', '?')} — {od.get('luc_nham_reason', '')}\n"
                    f"Thái Ất Thần Số: {od.get('thai_at_verdict', '?')} — {od.get('thai_at_reason', '')}\n"
                )
                
                # 3) Số lượng/tuổi (nếu có)
                if od.get('count_numbers'):
                    offline_ctx += f"Kết quả đếm số: {od['count_numbers']}\n"
                if od.get('age_numbers'):
                    offline_ctx += f"Kết quả tuổi: {od['age_numbers']}\n"
                
                # 4) Bằng chứng tác động (chain evidence)
                if od.get('impact_evidence'):
                    offline_ctx += f"\n--- BẰNG CHỨNG TÁC ĐỘNG (từ Python engine) ---\n"
                    for e in od['impact_evidence'][:20]:
                        offline_ctx += f"• {e}\n"
                
                # 5) UNIFIED NARRATIVE
                if od.get('unified_narrative'):
                    offline_ctx += f"\n--- KẾT LUẬN THỐNG NHẤT TỪ AI OFFLINE ---\n"
                    offline_ctx += od['unified_narrative'] + "\n"
                
                # V13.0: FULL OFFLINE REPORT — Toàn bộ phân tích chi tiết
                if od.get('full_offline_report'):
                    offline_ctx += f"\n--- BÁO CÁO ĐẦY ĐỦ (PHÂN TÍCH CHI TIẾT TỪ PYTHON) ---\n"
                    offline_ctx += od['full_offline_report'] + "\n"
                
                # V15.3: STRUCTURED V15 ANALYSIS — Nội/Ngoại Cung + Timeline + Ứng Kỳ
                if od.get('v15_bt_score') or od.get('v15_dt_score'):
                    offline_ctx += f"\n--- V15 XÂU DƯỢC (PHÂN TÍCH NỘI/NGOẠI CUNG CHẤM ĐIỂM) ---\n"
                    if od.get('v15_bt_score'):
                        offline_ctx += f"Bản Thân: {od['v15_bt_score']}\n"
                    if od.get('v15_dt_score'):
                        offline_ctx += f"Dụng Thần: {od['v15_dt_score']}\n"
                    if od.get('v15_timeline'):
                        offline_ctx += f"Timeline: {od['v15_timeline']}\n"
                    if od.get('v15_timing'):
                        offline_ctx += f"Ứng Kỳ: {od['v15_timing']}\n"
                
                # V16.0: STRUCTURED V16 SCORING — All 5 methods
                has_v16 = any(od.get(k) for k in ['v16_lh_score','v16_mh_score','v16_tb_score','v16_ln_score','v16_ta_score'])
                if has_v16:
                    offline_ctx += f"\n--- V16 LỤC THUẬT XÂU DƯỢC (SCORING 5 PHƯƠNG PHÁP) ---\n"
                    if od.get('v16_lh_score'):
                        offline_ctx += f"Lục Hào: {od['v16_lh_score']}\n"
                    if od.get('v16_mh_score'):
                        offline_ctx += f"Mai Hoa: {od['v16_mh_score']}\n"
                    if od.get('v16_tb_score'):
                        offline_ctx += f"Thiết Bản: {od['v16_tb_score']}\n"
                    if od.get('v16_ln_score'):
                        offline_ctx += f"Đại Lục Nhâm: {od['v16_ln_score']}\n"
                    if od.get('v16_ta_score'):
                        offline_ctx += f"Thái Ất: {od['v16_ta_score']}\n"
                
                # V17.0: STRUCTURED V17 METHOD ROUTING
                if od.get('v17_routing'):
                    offline_ctx += f"\n--- V17 LỤC THUẬT PHÂN CẤP (PP CHÍNH + ĐỐI CHIẾU %) ---\n"
                    offline_ctx += od['v17_routing'] + "\n"
                
                # V18.0: DETECTIVE DEDUCTION
                if od.get('v18_detective'):
                    offline_ctx += f"\n--- V18 AI THÁM TỬ (LẮP GHÉP MANH MỐI) ---\n"
                    offline_ctx += od['v18_detective'] + "\n"

                # V27.0: Enhanced Detective (tu qmdg_advanced_rules + inference_rules)
                if chart_data and isinstance(chart_data, dict):
                    hanh_dt_v27 = od.get('v22_unified_strength', {}).get('hanh_dt', '')
                    enhanced_det = self._enhanced_detective(chart_data, question, hanh_dt_v27)
                    if enhanced_det:
                        offline_ctx += enhanced_det
                
                offline_ctx += f"=== HẾT DỮ LIỆU OFFLINE ===\n\n"
            
            # V14.0: Inject Đại Lục Nhâm + Thái Ất data
            luc_nham_ctx = ""
            thai_at_ctx = ""
            try:
                from dai_luc_nham import tinh_dai_luc_nham, phan_tich_chuyen_sau
                if chart_data and isinstance(chart_data, dict) and 'can_ngay' in chart_data:
                    ln_data = tinh_dai_luc_nham(
                        chart_data.get('can_ngay', 'Giáp'),
                        chart_data.get('chi_ngay', 'Tý'),
                        chart_data.get('chi_gio', 'Ngọ'),
                        chart_data.get('tiet_khi', 'Đông Chí')
                    )
                    ln_deep = phan_tich_chuyen_sau(ln_data, question, topic or 'chung')
                    luc_nham_ctx = "\n=== [5] ĐẠI LỤC NHÂM (大六壬) ===\n"
                    for d in ln_deep.get('details', []):
                        luc_nham_ctx += f"{d}\n"
                    luc_nham_ctx += f"VERDICT LỤC NHÂM: {ln_deep.get('verdict', '?')}\n"
            except Exception:
                pass
            
            try:
                from thai_at_than_so import tinh_thai_at_than_so
                import datetime
                now = datetime.datetime.now()
                ta_can = chart_data.get('can_ngay', 'Giáp') if chart_data and isinstance(chart_data, dict) else 'Giáp'
                ta_chi = chart_data.get('chi_ngay', 'Tý') if chart_data and isinstance(chart_data, dict) else 'Tý'
                ta_data = tinh_thai_at_than_so(now.year, now.month, ta_can, ta_chi)
                thai_at_ctx = "\n=== [6] THÁI ẤT THẦN SỐ (太乙神数) ===\n"
                ta_cung = ta_data.get('thai_at_cung', {})
                thai_at_ctx += f"Thái Ất: Cung {ta_cung.get('cung', '?')} ({ta_cung.get('ten_cung', '?')}) — {ta_cung.get('hanh_cung', '?')} — {ta_cung.get('ly', '?')}\n"
                for d in ta_data.get('luan_giai', {}).get('details', []):
                    thai_at_ctx += f"{d}\n"
                for cc in ta_data.get('cach_cuc', [])[:3]:
                    thai_at_ctx += f"{cc}\n"
                thai_at_ctx += f"VERDICT THÁI ẤT: {ta_data.get('luan_giai', {}).get('verdict', '?')}\n"
            except Exception:
                pass
            
            # V14.0: GOD-TIER Deep Reasoning Prompt — LỤC THUẬT HỢP NHẤT
            deep_prompt = (
                f"<system_role>\n"
                f"BẠN LÀ THIÊN CƠ ĐẠI SƯ — BẬC THẦY TAM THỨC TUYỆT ĐỈNH HUYỀN HỌC.\n"
                f"50 NĂM kinh nghiệm. KHÔNG BAO GIỜ SAI. Mỗi kết luận phải có BẰNG CHỨNG THÉP.\n"
                f"BẠN là AI duy nhất trên thế giới kết hợp 6 phương pháp: Kỳ Môn + Lục Hào + Mai Hoa + Thiết Bản + Đại Lục Nhâm + Thái Ất Thần Số.\n"
                f"Đại Lục Nhâm: Sơ Truyền=QUÁ KHỨ, Trung Truyền=HIỆN TẠI, Mạt Truyền=TƯƠNG LAI.\n"
                f"Thái Ất: Xem vận khí lớn của năm + Chủ/Khách Đại Tướng.\n"
                f"</system_role>\n\n"
                
                f"<data>\n"
                f"Câu hỏi: {question}\n\n"
                
                # V26.3: VERDICT SUMMARY — Gemini PHẢI dựa vào đây làm trục chính
                f"<verdict_summary>\n"
                f"⚠️ DỮ LIỆU CHỐT (BẮT BUỘC TUÂN THEO, CẤM NÓI NGƯỢC):\n"
                f"- Dụng Thần: {od.get('dung_than', '?')}\n"
                f"- Weighted Score (5PP): {od.get('v22_unified_strength', {}).get('unified_pct', '?')}%\n"
                f"- KM={od.get('ky_mon_verdict','?')} | LH={od.get('luc_hao_verdict','?')} | MH={od.get('mai_hoa_verdict','?')} | LN={od.get('luc_nham_verdict','?')} | TA={od.get('thai_at_verdict','?')}\n"
                f"- Ngũ Khí: {od.get('v22_unified_strength', {}).get('ngu_khi', '?')}\n"
                f"- 12 Trường Sinh: {od.get('v22_unified_strength', {}).get('ts_stage', '?')}\n"
                f"- Hành DT: {od.get('v22_unified_strength', {}).get('hanh_dt', '?')}\n"
                f"→ NẾU Weighted Score >= 60% → phán CÁT/THUẬN LỢI.\n"
                f"→ NẾU Weighted Score <= 45% → phán HUNG/KHÓ KHĂN.\n"  
                f"→ NẾU 46-59% → phán BÌNH/CHƯA RÕ.\n"
                f"BẠN CẤM ĐƯỢC PHÁN NGƯỢC LẠI CON SỐ NÀY!\n"
                f"</verdict_summary>\n\n"
                
                f"{rag_prompt}\n"
                f"{offline_ctx}"
                f"{luc_nham_ctx}"
                f"{thai_at_ctx}"
                f"</data>\n\n"
                
                f"<absolute_rules>\n"
                f"⛔ CẤM TUYỆT ĐỐI:\n"
                f"- CẤM nói: 'có vẻ', 'có thể', 'tùy trường hợp', 'cần xem thêm', 'theo kinh nghiệm'\n"
                f"- CẤM tự bịa dữ liệu không có trong <data>\n"
                f"- CẤM dùng kiến thức chung thay cho dữ liệu quẻ\n"
                f"- CẤM bỏ qua bất kỳ phương pháp nào\n"
                f"- CẤM kết luận mà không trích dẫn dữ liệu cụ thể\n\n"
                
                f"✅ BẮT BUỘC:\n"
                f"- Mỗi câu kết luận PHẢI kèm: [Nguồn: PP gì] + [Dữ liệu: giá trị cụ thể] + [Logic: vì sao]\n"
                f"- Format trích dẫn: '📌 Dữ liệu: [tên_trường] = [giá_trị] → vì [A] nên [B]'\n"
                f"- Kết luận DỨT KHOÁT: CÓ hoặc KHÔNG, NÊN hoặc KHÔNG NÊN, CÁT hoặc HUNG\n"
                f"- Xác suất PHẢI có con số cụ thể: 65%, 80%, không được nói 'khá cao'\n"
                f"</absolute_rules>\n\n"
                
                f"<ngu_hanh_rules>\n"
                f"NGŨ HÀNH TƯƠNG SINH: Mộc→Hỏa→Thổ→Kim→Thủy→Mộc (sinh = hỗ trợ, TỐT)\n"
                f"NGŨ HÀNH TƯƠNG KHẮC: Mộc→Thổ→Thủy→Hỏa→Kim→Mộc (khắc = phá hủy, XẤU)\n"
                f"DỤNG THẦN: Hỏi tiền/tài=Thê Tài | Việc/sếp/kiện/bệnh=Quan Quỷ | Con/bình an/phúc=Tử Tôn | Nhà/xe/học/cha mẹ=Phụ Mẫu | Bạn/đối thủ/anh em=Huynh Đệ\n"
                f"</ngu_hanh_rules>\n\n"
                
                f"<master_luc_hao_method>\n"
                f"=== KHẨU QUYẾT BẬC THẦY LỤC HÀO (10 BƯỚC) ===\n"
                f"一看空 (1-Xem Không Vong): Dụng Thần lâm Tuần Không → sự việc CHƯA THÀNH, chờ xuất Không mới ứng\n"
                f"二看冲 (2-Xem Xung): DT bị Nguyệt/Nhật xung → phá tan, Lục Xung quẻ → sự việc tan rã\n"
                f"三看刑合衰旺中 (3-Xem Hình Hợp Suy Vượng): DT Vượng+Hợp=TỐT, Suy+Hình=XẤU\n"
                f"四看化出进退死 (4-Xem Hóa): Hào động hóa Tiến Thần (VD: Dần→Mão)=tiến bộ, hóa Thoái Thần (VD: Mão→Dần)=thụt lùi, hóa Tuyệt=chết\n"
                f"五看神煞凶不凶 (5-Xem Thần Sát): Lục Thú (Thanh Long=vui, Bạch Hổ=tang, Đằng Xà=lo sợ, Câu Trần=chậm, Chu Tước=kiện, Huyền Vũ=mất)\n"
                f"六看用爻之位置 (6-Vị trí Dụng Thần): Hào 1=gần/thấp, Hào 6=xa/cao, Hào Thế=mình, Hào Ứng=đối phương\n"
                f"七看伏神出牢笼 (7-Phục Thần): DT không hiện → tìm Phục Thần, Phục Thần được Phi Thần sinh=sẽ xuất hiện\n"
                f"八看反伏吟流泪 (8-Phản/Phục Ngâm): Phản Ngâm=đảo ngược, Phục Ngâm=đau khổ không thay đổi\n"
                f"九看外应 (9-Ngoại Ứng): Dấu hiệu bên ngoài lúc gieo quẻ\n"
                f"十观容 (10-Quan Tướng): Tượng lấy từ Bát Quái → hình dáng sự vật\n\n"
                
                f"=== NGUYÊN THẦN / KỴ THẦN / CỪU THẦN ===\n"
                f"NGUYÊN THẦN = hào SINH Dụng Thần → Nguyên Thần vượng + động = DT được cứu = CÁT\n"
                f"KỴ THẦN = hào KHẮC Dụng Thần → Kỵ Thần vượng + động = DT bị hại = HUNG\n"
                f"CỪU THẦN = hào SINH Kỵ Thần → Cừu Thần giúp Kỵ Thần mạnh hơn = càng HUNG\n"
                f"⚡ THAM SINH VONG KHẮC: Nếu Kỵ Thần + Nguyên Thần cùng ĐỘNG → Kỵ Thần tham sinh Nguyên Thần → quên khắc DT → HÓA CÁT!\n\n"
                
                f"=== VƯỢNG SUY CHUẨN XÁC ===\n"
                f"VƯỢNG: DT được Nguyệt lệnh sinh/trợ + Nhật thần sinh/trợ + có Nguyên Thần động\n"
                f"SUY: DT bị Nguyệt lệnh khắc + Nhật thần khắc + Kỵ Thần động + Tuần Không/Nguyệt Phá\n"
                f"→ DT VƯỢNG = sự việc THÀNH, DT SUY = sự việc BẠI\n"
                f"</master_luc_hao_method>\n\n"
                
                f"<master_ky_mon_method>\n"
                f"=== PHƯƠNG PHÁP ĐOÁN KỲ MÔN CHUẨN XÁC ===\n"
                f"4 TẦNG PHÂN TÍCH (PHẢI LÀM ĐỦ):\n"
                f"① THIÊN BÀN (Cửu Tinh/Sao): Thiên Bồng/Nhậm/Xung=Cát | Thiên Nhuế/Cầm/Trụ=Hung | Thiên Phụ/Anh/Tâm=Trung\n"
                f"② NHÂN BÀN (Bát Môn/Cửa): Khai+Hưu+Sinh=ĐẠI CÁT | Thương+Đỗ=Trung Hung | Kinh+Tử+Cảnh=HUNG\n"
                f"③ THẦN BÀN (Bát Thần): Trực Phù/Thái Âm/Lục Hợp/Cửu Thiên/Cửu Địa=Cát | Đằng Xà/Bạch Hổ/Huyền Vũ=Hung\n"
                f"④ ĐỊA BÀN (Can Địa): Ngũ Hành Can + Cung → Vượng/Suy\n\n"
                
                f"CUNG CHỦ vs CUNG KHÁCH:\n"
                f"- Can Ngày = BẢN THÂN → tìm ở Cung nào → đó là Cung Chủ\n"
                f"- Can Giờ = SỰ VIỆC → tìm ở Cung nào → đó là Cung Khách\n"
                f"- Cung Chủ KHẮC Cung Khách → mình THẮNG đối phương = CÁT\n"
                f"- Cung Khách KHẮC Cung Chủ → mình THUA = HUNG\n"
                f"- Cung Chủ SINH Cung Khách → mình BỎ SỨC cho đối phương = HƯU\n"
                f"- Ngũ Hành ĐẠI TIỂU: Thiên Can trên Địa Bàn - xem Can Thiên+Địa khắc/sinh → Cách Cục (81 cách)\n"
                f"</master_ky_mon_method>\n\n"
                
                f"<master_mai_hoa_method>\n"
                f"=== PHƯƠNG PHÁP MAI HOA DỊCH SỐ CHUẨN XÁC ===\n"
                f"QUY TẮC THỂ DỤNG (THIỆU UNG):\n"
                f"① Dụng SINH Thể = ta ĐƯỢC LỢI → ĐẠI CÁT\n"
                f"② Thể SINH Dụng = ta BỎ SỨC cho người → HUNG (mất mát)\n"
                f"③ Thể KHẮC Dụng = ta THẮNG → CÁT (nhưng vất vả)\n"
                f"④ Dụng KHẮC Thể = ta BỊ HẠI → HUNG\n"
                f"⑤ Thể Dụng TỶ HÒA = cân bằng → BÌNH\n\n"
                f"HỖ QUÁI = diễn biến GIỮA CHỪNG (quá trình xảy ra)\n"
                f"BIẾN QUÁI = KẾT QUẢ CUỐI CÙNG\n"
                f"→ Hỗ Quái sinh Thể = quá trình thuận lợi\n"
                f"→ Biến Quái khắc Thể = kết quả xấu DÙ quá trình tốt\n"
                f"</master_mai_hoa_method>\n\n"
                
                f"<reasoning_protocol>\n"
                f"LÀM THEO THỨ TỰ NÀY — MỖI BƯỚC PHẢI TRÍCH DẪN DỮ LIỆU CỤ THỂ:\n\n"
                
                f"BƯỚC 0 — DỤNG THẦN: Xác định ĐÚNG theo bảng tra ở trên\n\n"
                
                f"BƯỚC 1 — KỲ MÔN (4 tầng):\n"
                f"Cung BT: Cung [số] — Sao [tên] (Cát/Hung) — Cửa [tên] (Cát/Hung) — Thần [tên] (Cát/Hung)\n"
                f"Cung SV: Cung [số] — tương tự\n"
                f"Quan hệ BT↔SV: Ngũ Hành [X] vs [Y] → [sinh/khắc] → CÁT/HUNG\n"
                f"Cách Cục: Can Thiên+Địa tạo thành [tên cách] → ý nghĩa\n"
                f"→ PHÁN KỲ MÔN: CÁT/HUNG [X]%\n\n"
                
                f"BƯỚC 2 — LỤC HÀO (10 bước khẩu quyết):\n"
                f"Áp dụng 10 bước ở trên → đặc biệt chú ý:\n"
                f"- Tuần Không? Nguyệt Phá?\n"
                f"- Nguyên Thần động không? Kỵ Thần động không?\n"
                f"- Tham Sinh Vong Khắc?\n"
                f"- Hào động hóa Tiến/Thoái?\n"
                f"→ PHÁN LỤC HÀO: CÁT/HUNG [X]%\n\n"
                
                f"BƯỚC 3 — MAI HOA (Thể Dụng):\n"
                f"Thể [tên] (Hành [X]) vs Dụng [tên] (Hành [Y]) → quy tắc ①-⑤\n"
                f"Hỗ Quái → diễn biến\n"
                f"Biến Quái → kết quả\n"
                f"→ PHÁN MAI HOA: CÁT/HUNG [X]%\n\n"
                
                f"BƯỚC 4 — ĐẠI LỤC NHÂM (Tam Truyền):\n"
                f"Sơ Truyền = QUÁ KHỨ/NGUYÊN NHÂN → chi gì? Lục Thân gì? Thiên Tướng gì?\n"
                f"Trung Truyền = HIỆN TẠI → đang diễn biến ra sao?\n"
                f"Mạt Truyền = TƯƠNG LAI/KẾT QUẢ → kết thúc thế nào?\n"
                f"Tuần Không? Dụng Thần có hiện trong Tứ Khóa không?\n"
                f"→ PHÁN LỤC NHÂM: CÁT/HUNG [X]%\n\n"
                
                f"BƯỚC 5 — THÁI ẤT THẦN SỐ (Vận khí năm):\n"
                f"Thái Ất ở Cung nào? Lý Thiên/Địa/Nhân?\n"
                f"Chủ Đại Tướng vs Khách Đại Tướng: ai khắc ai?\n"
                f"Văn Xương sinh/khắc Thái Ất?\n"
                f"Cách Cục: Yểm/Kích/Cách/Đối?\n"
                f"→ PHÁN THÁI ẤT: CÁT/HUNG [X]%\n\n"
                
                f"BƯỚC 6 — BẢNG TỔNG HỢP 5 PHƯƠNG PHÁP + XÂU DƯỢC + ỨNG KỲ:\n"
                f"| PP | Phán | % | Dữ kiện chính |\n"
                f"4/5 hoặc 5/5 CÁT → ĐẠI CÁT | 3/5 → CÁT | 2/5 → LỠ | 4-5/5 HUNG → ĐẠI HUNG\n\n"
                
                f"BƯỚC 7 — NẾU MÂU THUẪN: PP nào có DT VƯỢNG nhất = tin cậy nhất\n\n"
                
                f"BƯỚC 8 — XÂU DƯỢC (NỘI/NGOẠI CUNG V15.0):\n"
                f"Cung BT: Score [X] → [Vượng/Tướng/Hưu/Tù/Tử]\n"
                f"Cung DT: Score [Y] → [Vượng/Tướng/Hưu/Tù/Tử]\n"
                f"BT vs DT: SINH/KHẮC/TỶ HÒA → ta thắng/thua\n"
                f"Nội Cung (7 tầng): Sao↔Cung, Cửa↔Cung, Thần↔Cung, Tổ Hợp, Cách Cục, Tuần Không, Dịch Mã\n"
                f"Ngoại Cung (4 tầng): Lệnh Tháng/Mùa, Nhật Thần, Tứ Trụ, Lục Xung/Hợp\n"
                f"→ DT VƯỢNG (Score>10) = sự việc THÀNH, DT SUY (Score<-10) = sự việc BẠI\n\n"
                
                f"BƯỚC 9 — TIMELINE + ỨNG KỲ (V15.2-V15.3):\n"
                f"Timeline: QUÁ KHỨ (Địa Bàn Can) → HIỆN TẠI (Nhân Bàn Cửa) → TƯƠNG LAI (Thiên Bàn Sao+Can)\n"
                f"Xu hướng: Tiến triển tốt / Suy giảm / Cân bằng?\n"
                f"Tốc độ (Cửa+Sao): Khai Môn=NHANH, Đỗ Môn=RẤT CHẬM, Thiên Xung=NHANH, Thiên Nhuế=RẤT CHẬM\n"
                f"Dịch Mã lâm cung → tăng tốc | Tuần Không → chưa xảy ra, chờ xuất Không\n"
                f"Ứng kỳ: DT Vượng → ứng ngày XUNG | DT Suy → ứng ngày SINH/HỢP\n"
                f"→ PHÁN: Sự việc xảy ra KHI NÀO? NHANH hay CHẬM? Chi cụ thể → giờ/ngày/tháng\n\n"
                
                f"BƯỚC 10 — LỤC THUẬT PHÂN CẤP (V17.0):\n"
                f"Xem bảng V17 METHOD ROUTING → PP nào là CHÍNH cho câu hỏi này?\n"
                f"PP CHÍNH (trọng số cao nhất) → trả lời CHI TIẾT, dùng dữ liệu PP này làm trục chính\n"
                f"PP PHỤ → đối chiếu: đồng ý = tăng % tin cậy, không đồng ý = giảm %\n"
                f"VD: 'Lục Hào (PP chính 95%) cho thấy DT Vượng = CÁT. 4/6 PP đồng ý (67%). Kỳ Môn cũng CÁT → ĐỘ TIN CẬY CAO'\n"
                f"NẾU mâu thuẫn: PP CHÍNH luôn ưu tiên, PP PHỤ chỉ là tham khảo\n\n"
                
                f"BƯỚC 11 — AI THÁM TỬ (V18.0):\n"
                f"Xem mục V18 MANH MỐI → AI là thám tử lắp ghép các mảnh ghép thành câu trả lời cụ thể\n"
                f"Mỗi quái cho ra thuộc tính: chất liệu + hình dạng + âm thanh + đặc biệt\n"
                f"CROSS-REFERENCE: Tìm thuộc tính TRÙNG giữa nhiều nguồn → độ chính xác tăng\n"
                f"VD: Kim loại(Càn) + Kêu to(Chấn) + Điện(Đoài+Ly) → 95% là LOA ĐIỆN\n"
                f"DANH SÁCH: VẬt, Người, Nơi, Bệnh, Phương hướng → dùng để trả lời câu hỏi cụ thể\n"
                f"→ PHÁN CỤ THỂ: Đồ vật là gì? Người như nào? Nơi ở đâu? Với % tin cậy\n"
                f"</reasoning_protocol>\n\n"
                
                f"<output_format>\n"
                f"TIẾNG VIỆT, MARKDOWN, UYỂN CHUYỂN — KHÔNG BÁM FORMAT CỨNG.\n\n"
                
                f"QUY TẮC VIẾT:\n"
                f"1. MỞ ĐẦU = KẾT LUẬN THẲNG: Trả lời CÓ/KHÔNG/NÊN/KHÔNG NÊN ngay câu đầu tiên + % tin cậy\n"
                f"2. SAU ĐÓ tùy câu hỏi mà uyển chuyển:\n"
                f"   - Hỏi CÓ/KHÔNG → trả lời ngắn gọn 5-10 dòng, nêu lý do chính\n"
                f"   - Hỏi TẠI SAO → giải thích nhân quả, trích dữ kiện quẻ\n"
                f"   - Hỏi BAO GIỜ → tập trung ứng kỳ, ngày tháng Can Chi\n"
                f"   - Hỏi AI/NGƯỜI NÀO → mô tả tượng ý từ 12 Thiên Tướng + Bát Quái\n"
                f"   - Hỏi Ở ĐÂU → phương hướng từ cung vị, Bát Quái tượng\n"
                f"   - Hỏi phức tạp → phân tích sâu nhưng TÓM GỌN ý chính\n"
                f"3. GIỌNG VĂN: Như một thầy phong thủy giỏi đang tư vấn — tự tin, rõ ràng, uyển chuyển\n"
                f"4. TRÍCH DẪN: Mỗi nhận định phải kèm 1 dữ kiện cụ thể (VD: 'vì Dụng Thần Dậu-Kim được Nguyệt lệnh sinh')\n"
                f"5. KHÔNG LẶP: Không liệt kê lại toàn bộ dữ liệu — chỉ trích CÁI QUAN TRỌNG nhất\n"
                f"6. LIÊN KẾT: Nối các PP với nhau tự nhiên (VD: 'Kỳ Môn cho thấy thuận lợi, Lục Hào cũng xác nhận vì DT vượng')\n"
                f"7. KẾT: Luôn có 1-2 câu lời khuyên cụ thể + ứng kỳ (nếu có)\n"
                f"8. XÂU DƯỢC: Khi cần CHỨNG MINH DT vượng/suy → trích dẫn Score V15 (VD: 'DT tại Cung 7 đạt +32 = VƯỢNG vì Khai Môn + Thiên Tâm + Lệnh Tháng sinh')\n"
                f"9. TIMELINE: Liên kết Quá Khứ-Hiện Tại-Tương Lai thành 1 câu chuyện mạch lạc (VD: 'Gốc rễ vững (Địa Bàn), đang thuận nhờ Cửa Sinh, tương lai sáng nhờ Sao Cát')\n"
                f"10. ỨNG KỲ: Trả lời BAO GIỊ? PHẢI kèm giờ/ngày/tháng Can Chi cụ thể (VD: 'Ứng vào giờ Tý 23h-1h, tháng 11 âm lịch. Sự việc NHANH')\n"
                f"11. TỔNG HỢP LINH HOẠT: Kết hợp 5 PP + Xâu Dược + Timeline + Ứng Kỳ để đưa ra câu trả lời PHU HỢP VỚI CÂU HỎI. Không list luận thiên về 1 PP nào, phải xâu chuỗi tất cả thành 1 câu chuyện logic\n\n"
                
                f"CẤM:\n"
                f"- Không viết kiểu bảng biểu cứng nhắc mọi câu hỏi\n"
                f"- Không copy paste dữ liệu thô → phải DIỄN GIẢI\n"
                f"- Không dùng từ mơ hồ: 'có thể', 'tùy trường hợp', 'cần xem thêm'\n"
                f"- Không viết quá 1500 chữ\n"
                f"</output_format>\n"
            )
            
            # V14.0: Gọi Gemini TRỰC TIẾP — không qua answer_question (tránh double-wrapping prompt)
            # Thêm RAW DATA từ _get_paranoid_context vào prompt
            raw_que_data = ""
            try:
                raw_que_data = gemini._get_paranoid_context(
                    chart_data, topic or "Chung", question, None, mai_hoa_data, luc_hao_data
                )
            except Exception:
                pass
            
            if raw_que_data:
                deep_prompt += f"\n<raw_que_data>\n{raw_que_data}\n</raw_que_data>\n"
            
            # V14.0: LN+TA context đã được inject vào <data> block ở trên
            
            # Gọi trực tiếp _call_ai_raw — KHÔNG qua answer_question (tránh 2 prompt xung đột)
            result = gemini._call_ai_raw(deep_prompt)
            
            if result and len(str(result)) > 50:
                self.log_step("Online AI", "DONE", f"Gemini trả lời {len(str(result))} ký tự")
                return str(result)
            
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
            # Trường hợp Lục Nghi Kích Hình: Giáp ẩn dưới Mậu
            if not bt_cung and can_ngay == 'Giáp' and can_val == 'Mậu':
                bt_cung = int(cung_num) if cung_num else None
                
        for cung_num, can_val in can_thien_ban.items():
            if can_val == dt_can: dt_cung = int(cung_num) if cung_num else None
            if not dt_cung and dt_can == 'Giáp' and can_val == 'Mậu':
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
        
        summary = f"KM Score={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V27.0: 5 FACTORS BO SUNG CHO KY MON
        # Factor 1: Tuong tac Sao x Mon (tu database_tuong_tac)
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
                    factors.append(f"V27 KM Sao×Môn Cát +5: {sao_dt}×{mon_dt}")
                else:
                    score -= 3
                    factors.append(f"V27 KM Sao×Môn: {sm_result}")
        
        # Factor 2: Sinh khac Cung BT <-> DT (tu phan_tich_da_tang)
        if bt_cung is not None and dt_cung is not None:
            hanh_bt_cung = CUNG_NGU_HANH.get(bt_cung, '')
            hanh_dt_cung = CUNG_NGU_HANH.get(dt_cung, '')
            if hanh_bt_cung and hanh_dt_cung:
                rel = DATANG_SINH_KHAC(hanh_bt_cung, hanh_dt_cung)
                if 'Sinh' in str(rel) and 'Bi' not in str(rel):
                    score += 6
                    factors.append(f"V27 KM Cung BT sinh DT +6 ({hanh_bt_cung}→{hanh_dt_cung})")
                elif 'Khac' in str(rel) or 'Khắc' in str(rel):
                    if 'Bi' in str(rel) or 'Bị' in str(rel):
                        score -= 6
                        factors.append(f"V27 KM Cung BT bị khắc -6 ({hanh_bt_cung}←{hanh_dt_cung})")
                    else:
                        score += 4
                        factors.append(f"V27 KM Cung BT khắc DT +4")
        
        # Factor 3: Vuong Suy theo mua (tu blind_reading)
        if dt_can:
            can_hanh_km = CAN_NGU_HANH.get(dt_can, '')
            tiet_khi = chart_data.get('tiet_khi', '')
            if can_hanh_km and tiet_khi:
                vs = BLIND_VUONG_SUY(can_hanh_km, tiet_khi)
                if vs:
                    vs_str = str(vs)
                    if 'Vuong' in vs_str or 'Vượng' in vs_str:
                        score += 5
                        factors.append(f"V27 KM DT Vượng mùa +5")
                    elif 'Tu' in vs_str or 'Tử' in vs_str or 'Tù' in vs_str:
                        score -= 5
                        factors.append(f"V27 KM DT Tử/Tù mùa -5")
        
        # Factor 4: Anh huong mua len Hanh DT (tu database_tuong_tac)
        if DB_MUA and can_hanh_km:
            for mua_key, mua_data in DB_MUA.items():
                if isinstance(mua_data, dict) and can_hanh_km in mua_data:
                    trang_thai = mua_data[can_hanh_km]
                    if 'Vuong' in str(trang_thai) or 'Vượng' in str(trang_thai):
                        factors.append(f"V27 KM Mua {mua_key}: DT {trang_thai}")
                    break

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
            tu = hao.get('the_ung', '')
            if lt == dung_than:
                dt_hao = hao
                dt_idx = i + 1
            elif dung_than == 'Bản Thân' and tu == 'Thế':
                dt_hao = hao
                dt_idx = i + 1
            if tu == 'Thế':
                the_hao = hao
        
        if not dt_hao:
            if the_hao:
                dt_hao = the_hao
            else:
                return -10, "DT hào ẩn (Phục Thần) → -10"
        
        dt_hanh = dt_hao.get('ngu_hanh', '')
        dt_vuong = str(dt_hao.get('vuong_suy', ''))
        dt_chi = dt_hao.get('chi', '')
        
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
        chi_thang = luc_hao_data.get('chi_thang', '')
        hanh_thang = CHI_NGU_HANH.get(chi_thang, '')
        if hanh_thang and dt_hanh:
            if SINH.get(hanh_thang) == dt_hanh:
                score += 8
                factors.append(f"Nguyệt sinh DT +8")
            elif KHAC.get(hanh_thang) == dt_hanh:
                score -= 8
                factors.append(f"Nguyệt khắc DT -8")
        
        # ③ Nhật Thần sinh/khắc DT (±6)
        can_ngay = luc_hao_data.get('can_ngay', '') or ban.get('can_ngay', '')
        hanh_ngay = CAN_NGU_HANH.get(can_ngay, '')
        if hanh_ngay and dt_hanh:
            if SINH.get(hanh_ngay) == dt_hanh:
                score += 6
                factors.append(f"Nhật sinh DT +6")
            elif KHAC.get(hanh_ngay) == dt_hanh:
                score -= 6
                factors.append(f"Nhật khắc DT -6")
        
        # ④ Nguyên Thần (sinh DT) status (±6)
        nguyen_hanh = [h for h, s in SINH.items() if s == dt_hanh] if dt_hanh else []
        for hao in haos:
            h_hanh = hao.get('ngu_hanh', '')
            if h_hanh in nguyen_hanh:
                h_vuong = str(hao.get('vuong_suy', ''))
                if 'Vượng' in h_vuong:
                    score += 6
                    factors.append("Nguyên Thần vượng +6")
                elif 'Suy' in h_vuong or 'Tử' in h_vuong:
                    score -= 3
                    factors.append("Nguyên Thần suy -3")
                break
        
        # ⑤ Kỵ Thần (khắc DT) status (±6)
        ky_hanh = [h for h, k in KHAC.items() if k == dt_hanh] if dt_hanh else []
        for hao in haos:
            h_hanh = hao.get('ngu_hanh', '')
            if h_hanh in ky_hanh:
                h_vuong = str(hao.get('vuong_suy', ''))
                h_idx = haos.index(hao) + 1
                if 'Vượng' in h_vuong and h_idx in (dong_hao or []):
                    score -= 8
                    factors.append("Kỵ Thần vượng+động -8")
                elif 'Vượng' in h_vuong:
                    score -= 5
                    factors.append("Kỵ Thần vượng -5")
                elif 'Suy' in h_vuong or 'Tử' in h_vuong:
                    score += 3
                    factors.append("Kỵ Thần suy +3")
                break
        
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
        
        summary = f"LH Score={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:6])}{'...' if len(factors) > 6 else ''})"
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
        
        summary = f"MH Thể={the_name}({the_el}), Score={score}, {strength} ({len(factors)} yếu: {', '.join(factors[:3])}...)"
        
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
                        factors.append(f"[V27 KINH DICH] Que {ic.get('name','?')}: {str(ic_text)[:200]}")
                        if 'cat' in str(ic_text).lower() or 'hanh' in str(ic_text).lower():
                            score += 3
                        elif 'hung' in str(ic_text).lower() or 'nan' in str(ic_text).lower():
                            score -= 3
            except Exception:
                pass

        return score, summary, factors
    
    def _thiet_ban_scoring(self, chart_data, luc_hao_data, mai_hoa_data):
        """V26.2: Chấm điểm Thiết Bản — Đại Vận/Nạp Âm + 12 Trường Sinh + Quái Tượng."""
        score = 0
        factors = []
        
        can_ngay = ''
        chi_ngay = ''
        chi_nam = ''
        
        # ① Nạp Âm & Sinh khắc Can-Chi Ngày (±6)
        if chart_data and isinstance(chart_data, dict):
            can_ngay = chart_data.get('can_ngay', '')
            chi_ngay = chart_data.get('chi_ngay', '')
            chi_nam = chart_data.get('chi_nam', '')
            can_chi = can_ngay + chi_ngay if can_ngay and chi_ngay else ''
            
            # Nạp âm mệnh
            if can_chi and NAP_AM_GIAI_THICH:
                nap_am = NAP_AM_GIAI_THICH.get(can_chi, {})
                if nap_am:
                    cat_hung = nap_am.get('cat_hung', '')
                    if 'Cát' in str(cat_hung):
                        score += 5
                        factors.append(f"TB Nạp Âm {can_chi} Cát +5")
                    elif 'Hung' in str(cat_hung):
                        score -= 5
                        factors.append(f"TB Nạp Âm {can_chi} Hung -5")
            
            # Sinh khắc Can (Thiên) Chi (Địa) Ngày
            can_hanh = CAN_NGU_HANH.get(can_ngay, '')
            chi_hanh = CHI_NGU_HANH.get(chi_ngay, '')
            if can_hanh and chi_hanh:
                if SINH.get(chi_hanh) == can_hanh:
                    score += 4
                    factors.append(f"TB Địa Chi sinh Thiên Can +4")
                elif KHAC.get(chi_hanh) == can_hanh:
                    score -= 4
                    factors.append(f"TB Địa Chi khắc Thiên Can -4")
                elif can_hanh == chi_hanh:
                    score += 2
                    factors.append(f"TB Thiên Địa Tỷ Hòa +2")
        
        # ② Thái Tuế (Lưu Niên) sinh khắc Mệnh Chủ (Can Ngày) (±6)
        if can_ngay and chi_nam:
            can_hanh = CAN_NGU_HANH.get(can_ngay, '')
            nam_hanh = CHI_NGU_HANH.get(chi_nam, '')
            if can_hanh and nam_hanh:
                if SINH.get(nam_hanh) == can_hanh:
                    score += 6
                    factors.append(f"TB Thái Tuế ({chi_nam}) sinh Mệnh +6")
                elif KHAC.get(nam_hanh) == can_hanh:
                    score -= 6
                    factors.append(f"TB Thái Tuế ({chi_nam}) khắc Mệnh -6")
                elif nam_hanh == can_hanh:
                    score += 3
                    factors.append(f"TB Mệnh đắc Thái Tuế +3")
        
        # ③ 12 Trường Sinh (±8)
        if chart_data and isinstance(chart_data, dict):
            hanh_can = CAN_NGU_HANH.get(can_ngay, '')
            if hanh_can and chi_ngay:
                ts_stage, ts_explain = _get_truong_sinh(hanh_can, chi_ngay)
                if ts_stage:
                    if ts_stage in ['Đế Vượng', 'Lâm Quan', 'Trường Sinh']:
                        score += 8
                        factors.append(f"TB 12TrSinh Mệnh {ts_stage} +8")
                    elif ts_stage in ['Tử', 'Mộ', 'Tuyệt']:
                        score -= 8
                        factors.append(f"TB 12TrSinh Mệnh {ts_stage} -8")
                    elif ts_stage in ['Suy', 'Bệnh']:
                        score -= 4
                        factors.append(f"TB 12TrSinh Mệnh {ts_stage} -4")
                        
        # ④ Bổ trợ từ Quẻ (±5)
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
                        factors.append(f"TB Cục diện Quẻ {que_name} Cát +5")
                    elif 'Hung' in cat_hung:
                        score -= 5
                        factors.append(f"TB Cục diện Quẻ {que_name} Hung -5")
                    break
        
        if score >= 10: strength = "🟢 CỰC VƯỢNG"
        elif score >= 4: strength = "🔵 TƯỚNG"
        elif score >= -3: strength = "🟡 BÌNH"
        elif score >= -8: strength = "🟠 SUY"
        else: strength = "🔴 TỬ"
        
        summary = f"TB Score={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V27.0: Bo sung Thiet Ban - Dai Van/Luu Nien
        try:
            import datetime as _dt_tb
            current_year = _dt_tb.datetime.now().year
            # Load thiet_ban_than_toan.json neu co
            import json as _json_tb
            tb_json_path = os.path.join(os.path.dirname(__file__), 'thiet_ban_than_toan.json')
            if os.path.exists(tb_json_path):
                with open(tb_json_path, 'r', encoding='utf-8') as _f:
                    tb_json = _json_tb.load(_f)
                    # Tim Luu Nien hien tai
                    luu_nien = tb_json.get('luu_nien', {}).get(str(current_year), {})
                    if luu_nien:
                        ln_hanh = luu_nien.get('hanh', '')
                        if ln_hanh and can_hanh:
                            if SINH.get(ln_hanh) == can_hanh:
                                score += 4
                                factors.append(f"V27 TB Luu Nien {current_year} sinh Menh +4")
                            elif KHAC.get(ln_hanh) == can_hanh:
                                score -= 4
                                factors.append(f"V27 TB Luu Nien {current_year} khac Menh -4")
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
        
        summary = f"LN Score={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V27.0: Bo sung Phan Tich Luc Nham
        # Factor: Sinh khac Tam Truyen voi Can Ngay (chi tiet hon)
        try:
            trung_hanh = tam_truyen.get('trung_truyen_hanh', '')
            mat_hanh = tam_truyen.get('mat_truyen_hanh', '')
            
            # Trung Truyen (Hien Tai) - trong so trung binh
            if trung_hanh and can_hanh:
                if SINH.get(trung_hanh) == can_hanh:
                    score += 5
                    factors.append(f"V27 LN Trung Truyen sinh Can +5")
                elif KHAC.get(trung_hanh) == can_hanh:
                    score -= 5
                    factors.append(f"V27 LN Trung Truyen khac Can -5")
            
            # Mat Truyen (Tuong Lai) - trong so thap
            if mat_hanh and can_hanh:
                if SINH.get(mat_hanh) == can_hanh:
                    score += 3
                    factors.append(f"V27 LN Mat Truyen sinh Can +3 (tuong lai tot)")
                elif KHAC.get(mat_hanh) == can_hanh:
                    score -= 3
                    factors.append(f"V27 LN Mat Truyen khac Can -3 (tuong lai xau)")
            
            # Thien Tuong
            thien_tuong = ln_data.get('thien_tuong', {})
            if thien_tuong:
                for tt_name, tt_val in thien_tuong.items():
                    if isinstance(tt_val, dict) and tt_val.get('cat_hung'):
                        ch = str(tt_val['cat_hung'])
                        if 'Cat' in ch or 'Cát' in ch:
                            score += 2
                            factors.append(f"V27 LN Thien Tuong {tt_name} Cat +2")
                        elif 'Hung' in ch:
                            score -= 2
                            factors.append(f"V27 LN Thien Tuong {tt_name} Hung -2")
                        if len(factors) > 20:
                            break
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
        
        summary = f"TA Score={score}, {strength} ({len(factors)} yếu tố: {', '.join(factors[:3])}...)"
        
        # V27.0: Bo sung Thai At
        # Factor: Sinh khac voi Can Ngay
        try:
            ta_cung = ta_data.get('thai_at_cung', {})
            hanh_cung_ta = ta_cung.get('hanh_cung', '')
            can_h = CAN_NGU_HANH.get(can_ngay, '')
            if hanh_cung_ta and can_h:
                if SINH.get(hanh_cung_ta) == can_h:
                    score += 6
                    factors.append(f"V27 TA Thai At sinh Can Ngay +6")
                elif KHAC.get(hanh_cung_ta) == can_h:
                    score -= 6
                    factors.append(f"V27 TA Thai At khac Can Ngay -6")
                elif hanh_cung_ta == can_h:
                    score += 3
                    factors.append(f"V27 TA Thai At dong hanh Can +3")
            
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
                    factors.append(f"V27 TA Bat Tuong Cat nhieu +4 ({cat_count}C/{hung_count}H)")
                elif hung_count > cat_count:
                    score -= 4
                    factors.append(f"V27 TA Bat Tuong Hung nhieu -4 ({cat_count}C/{hung_count}H)")
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
        parts.append(f"PP CHÍNH: {primary_name} (trọng số {primary_weight}%) → {primary_verdict}, Score={scores.get(primary, 0)}")
        
        # Top 2 PP phụ
        for m, ws in sorted_methods[1:3]:
            m_name = METHOD_NAMES.get(m, m)
            m_weight = strengths[m]
            parts.append(f"PP PHỤ: {m_name} ({m_weight}%) → {verdicts.get(m, 'BÌNH')}, Score={scores.get(m, 0)}")
        
        parts.append(f"Đồng thuận: {cat_count}/{total} CÁT, {hung_count}/{total} HUNG = {consensus_pct}%")
        if conflicts:
            parts.append(f"Mâu thuẫn: {', '.join(conflicts[:3])}")
        
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
                                                     chart_data=chart_data)
        
        return impact_text, direct_answer, evidence
    
    def _generate_direct_answer(self, question, dung_than, final_verdict, pct,
                                 cat_count, hung_count, evidence, impacts,
                                 ky_mon_reason, luc_hao_reason, mai_hoa_reason,
                                 age_numbers=None, count_numbers=None, chart_data=None):
        """
        V10.0: Sinh câu trả lời TRỰC TIẾP dựa trên phân tích thực,
        KHÔNG dùng mẫu cứng theo keyword.
        """
        q = question.lower()
        lines = []
        
        lines.append(f"\n**❓ Câu hỏi của bạn:** {question}")
        
        # Tổng kết bằng chứng CỤ THỂ từ quẻ
        good_impacts = [i for i in impacts if i.startswith('✅')]
        bad_impacts = [i for i in impacts if i.startswith('🔴') or i.startswith('⚠️')]
        
        # Icon theo verdict
        if final_verdict == 'CÁT':
            icon = '🟢'
        elif final_verdict == 'HUNG':
            icon = '🔴'
        else:
            icon = '🟡'
        
        # --- Xác định dạng câu hỏi và trả lời thông minh ---
        
        # CÓ/KHÔNG ("có nên", "có được", "đỗ không", etc.)
        if any(k in q for k in ['có nên', 'có được', 'được không', 'nên không', 'có thể',
                                 'có thành', 'có đỗ', 'có đạt', 'có thắng', 'có tốt']):
            if final_verdict == 'CÁT':
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: CÓ — Khả năng thành công {pct}%**")
            elif final_verdict == 'HUNG':
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: KHÔNG NÊN — Xác suất bất lợi {100-pct}%**")
            else:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: CÒN PHẢI XEM — Tình thế chưa rõ ({pct}%)**")
        
        # SỐNG/CHẾT — câu hỏi nhạy cảm về sinh tử
        elif any(k in q for k in ['mất hay chưa', 'chết chưa', 'còn sống', 'sống không',
                                   'qua khỏi', 'cứu được', 'mất chưa']):
            if final_verdict == 'CÁT' and len(good_impacts) >= 2:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: TÌNH TRẠNG KHẢ QUAN ({pct}%)**")
                lines.append(f"- Quẻ cho thấy {dung_than} CÒN SỨC, có dấu hiệu hồi phục.")
            elif final_verdict == 'HUNG' and len(bad_impacts) >= 2:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: TÌNH TRẠNG NGHIÊM TRỌNG ({pct}%)**")
                lines.append(f"- Quẻ cho thấy {dung_than} RẤT YẾU, cần hành động khẩn cấp.")
            else:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: CHƯA THỂ KHẲNG ĐỊNH ({pct}%)**")
                lines.append(f"- Các phương pháp cho kết quả trái chiều, cần theo dõi sát.")
        
        # KHI NÀO — "khi nào", "bao giờ"
        elif any(k in q for k in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'khi nao']):
            if final_verdict == 'CÁT':
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: Thời điểm HIỆN TẠI đã thuận lợi ({pct}%)**")
                lines.append(f"- Nên hành động trong 1-7 ngày tới.")
            else:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: Chưa phải thời điểm tốt**")
                lines.append(f"- Nên chờ 1-3 tháng để tình hình chuyển biến.")
        
        # TUỔI
        elif any(k in q for k in ['bao nhiêu tuổi', 'tuổi', 'năm tuổi']):
            if age_numbers:
                all_nums = [n for _, n in age_numbers]
                avg = int(sum(all_nums) / len(all_nums)) if all_nums else 0
                detail = ', '.join(f'{pp}={n}' for pp, n in age_numbers)
                lines.append(f"\n📊 **CÂU TRẢ LỜI: Khoảng {avg} TUỔI**")
                lines.append(f"- Dựa trên {len(age_numbers)} phương pháp: {detail}")
            else:
                lines.append(f"\n📊 **CÂU TRẢ LỜI:** Không đủ dữ liệu tuổi từ quẻ.")
        
        # BAO NHIÊU / MẤY
        elif any(k in q for k in ['bao nhiêu', 'mấy người', 'mấy cái', 'mấy đứa', 'mấy anh', 'mấy chị', 'số lượng']):
            if count_numbers:
                all_nums = [n for _, n in count_numbers]
                avg = int(round(sum(all_nums) / len(all_nums))) if all_nums else 0
                detail = ', '.join(f'{pp}={n}' for pp, n in count_numbers)
                lines.append(f"\n📊 **CÂU TRẢ LỜI: Khoảng {avg}**")
                lines.append(f"- Dựa trên {len(count_numbers)} phương pháp: {detail}")
            elif age_numbers:
                all_nums = [n for _, n in age_numbers]
                avg = int(sum(all_nums) / len(all_nums)) if all_nums else 0
                detail = ', '.join(f'{pp}={n}' for pp, n in age_numbers)
                lines.append(f"\n📊 **CÂU TRẢ LỜI: Khoảng {avg}**")
                lines.append(f"- Dựa trên {len(age_numbers)} phương pháp: {detail}")
            else:
                lines.append(f"\n📊 **CÂU TRẢ LỜI:** Không đủ dữ liệu số lượng từ quẻ.")
        
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
                lines.append(f"\n📍 **CÂU TRẢ LỜI: HƯỚNG {huong.upper()} (Cung {sv_cung} - {sv_quai})**")
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
        
        # DEFAULT — Câu hỏi chung
        else:
            if final_verdict == 'CÁT':
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: THUẬN LỢI ({pct}%)**")
            elif final_verdict == 'HUNG':
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: KHÓ KHĂN ({pct}%)**")
            else:
                lines.append(f"\n{icon} **CÂU TRẢ LỜI: CHƯA RÕ RÀNG ({pct}%)**")
        
        # --- V10.0: BẰNG CHỨNG CỤ THỂ TỪ QUẺ (thay vì mẫu chung) ---
        lines.append(f"\n**📋 Bằng chứng từ quẻ (tại sao kết luận như trên):**")
        lines.append(f"- Kỳ Môn ({ky_mon_reason if ky_mon_reason else 'Bình'})")
        lines.append(f"- Lục Hào ({luc_hao_reason if luc_hao_reason else 'Bình'})")
        if mai_hoa_reason and isinstance(mai_hoa_reason, str) and len(mai_hoa_reason) < 100:
            lines.append(f"- Mai Hoa ({mai_hoa_reason})")
        
        if good_impacts:
            lines.append(f"\n**✅ Yếu tố thuận lợi ({len(good_impacts)}):**")
            for gi in good_impacts[:3]:
                lines.append(f"- {gi.replace('✅ ', '')}")
        
        if bad_impacts:
            lines.append(f"\n**⚠️ Yếu tố bất lợi ({len(bad_impacts)}):**")
            for bi in bad_impacts[:3]:
                lines.append(f"- {bi.replace('🔴 ', '').replace('⚠️ ', '')}")
        
        # --- LỜI KHUYÊN DỰA TRÊN NGỮ CẢNH CÂU HỎI + BẰNG CHỨNG ---
        lines.append(f"\n**💡 Lời khuyên hành động:**")
        if final_verdict == 'CÁT':
            if any(k in q for k in ['mua', 'đầu tư', 'kinh doanh', 'vốn', 'tiền']):
                lines.append("- ✅ Thời điểm tốt để giao dịch. Kiểm tra kỹ giấy tờ.")
            elif any(k in q for k in ['bệnh', 'ốm', 'khỏe', 'sức khỏe', 'đau']):
                lines.append("- ✅ Bệnh sẽ khỏi, tìm bác sĩ chuyên khoa để trị dứt.")
            elif any(k in q for k in ['yêu', 'tình', 'vợ', 'chồng', 'cưới']):
                lines.append("- ✅ Mối quan hệ tốt đẹp, thời điểm thuận lợi.")
            elif any(k in q for k in ['việc', 'công ty', 'thi', 'đỗ']):
                lines.append("- ✅ Công việc/thi cử thuận lợi, hành động ngay.")
            else:
                lines.append("- ✅ Nên hành động sớm, tận dụng thời cơ.")
        elif final_verdict == 'HUNG':
            if any(k in q for k in ['bệnh', 'ốm', 'khỏe', 'chết', 'mất']):
                lines.append("- ⚠️ Cần đi khám sớm, không tự chữa tại nhà.")
            elif any(k in q for k in ['mua', 'đầu tư', 'vốn', 'tiền']):
                lines.append("- ❌ Chưa nên giao dịch lớn, chờ thêm 2-4 tuần.")
            else:
                lines.append("- ❌ Kiên nhẫn chờ đợi, tìm quý nhân hỗ trợ.")
        else:
            lines.append("- ⏸️ Giữ nguyên hiện trạng, quan sát thêm.")
        
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
                tu = hao.get('the_ung', '')
                if lt == dung_than or (dung_than in ['Phụ Mẫu (Cha)', 'Phụ Mẫu (Mẹ)'] and 'Phụ Mẫu' in lt):
                    dt_hao = hao
                    break
                if dung_than == 'Bản Thân' and tu == 'Thế':
                    dt_hao = hao
                    break
            
            if dt_hao:
                lh_info = {
                    'hao': dt_hao.get('hao', '?'),
                    'can_chi': dt_hao.get('can_chi', '?'),
                    'hanh': dt_hao.get('ngu_hanh', '?'),
                    'vuong_suy': str(dt_hao.get('vuong_suy', '?')),
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
                    tb_info = {'nap_am': nap_am.get('ten', '?'), 'hanh': nap_am.get('hanh', '?')}
                    tb_info['giai_thich'] = NAP_AM_GIAI_THICH.get(tb_info['nap_am'], '')
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
                                  final_pct=None):
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
        # PHASE B: BẢNG TỔNG HỢP DỤNG THẦN 5 PHƯƠNG PHÁP
        # ════════════════════════════════════════════
        lines.append("**📊 DỤNG THẦN QUA 5 PHƯƠNG PHÁP:**")
        lines.append(f"| Phương Pháp | Dụng Thần ({dung_than}) | Đánh Giá |")
        lines.append("|:---|:---|:---:|")
        
        good_count = 0
        bad_count = 0
        for method, status, gb in dt_statuses:
            icon = '✅' if gb == 'good' else ('🔴' if gb == 'bad' else '🟡')
            lines.append(f"| {method} | {status} | {icon} |")
            if gb == 'good': good_count += 1
            elif gb == 'bad': bad_count += 1
        
        if not dt_statuses:
            lines.append("| (chưa có đủ dữ liệu) | — | — |")
        
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
        # PHASE D: KẾT LUẬN THỐNG NHẤT
        # ════════════════════════════════════════════
        lines.append("")
        
        # Tổng hợp verdicts
        verdicts = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict, luc_nham_verdict, thai_at_verdict]
        cat_v = sum(1 for v in verdicts if v in ['CÁT', 'ĐẠI CÁT'])
        hung_v = sum(1 for v in verdicts if v in ['HUNG', 'ĐẠI HUNG'])
        
        # Tính tổng score
        total_good = good_count + cat_v
        total_bad = bad_count + hung_v
        
        # Build narrative paragraph
        narrative_parts = []
        
        # Part 1: Mở đầu — trạng thái DT (V26.0 dùng Điểm Trọng Số Thống Nhất)
        if final_pct is not None:
            pct = final_pct
            if pct >= 60:
                overall = 'THUẬN LỢI'
                narrative_parts.append(f"Tổng hợp **5 phương pháp** cho thấy {dung_than} (sự việc) đang ở thế **THUẬN LỢI** ({pct}%).")
            elif pct <= 45:
                overall = 'KHÓ KHĂN'
                narrative_parts.append(f"Tổng hợp **5 phương pháp** cho thấy {dung_than} (sự việc) đang ở thế **KHÓ KHĂN** ({pct}%).")
            else:
                overall = 'CHƯA RÕ'
                narrative_parts.append(f"Tổng hợp **5 phương pháp** cho kết quả **CHƯA RÕ RÀNG / BÌNH BÌNH** ({pct}%) — thế trận giằng co.")
        else:
            if total_good > total_bad:
                overall = 'THUẬN LỢI'
                pct = min(90, 50 + (total_good - total_bad) * 10)
                narrative_parts.append(f"Tổng hợp **5 phương pháp** cho thấy {dung_than} (sự việc) đang ở thế **THUẬN LỢI** ({pct}%).")
            elif total_bad > total_good:
                overall = 'KHÓ KHĂN'
                pct = max(10, 50 - (total_bad - total_good) * 10)
                narrative_parts.append(f"Tổng hợp **5 phương pháp** cho thấy {dung_than} (sự việc) đang ở thế **KHÓ KHĂN** ({pct}%).")
            else:
                overall = 'CHƯA RÕ'
                pct = 50
                narrative_parts.append(f"Tổng hợp **5 phương pháp** cho kết quả **CHƯA RÕ RÀNG** — các phương pháp cho kết quả trái chiều.")
        
        # Part 2: Bằng chứng cụ thể từ mỗi phương pháp
        method_summaries = []
        if ky_mon_reason:
            method_summaries.append(f"Kỳ Môn ({ky_mon_verdict}: {ky_mon_reason})")
        if luc_hao_reason:
            method_summaries.append(f"Lục Hào ({luc_hao_verdict}: {luc_hao_reason})")
        if mai_hoa_reason and isinstance(mai_hoa_reason, str) and len(mai_hoa_reason) < 100:
            method_summaries.append(f"Mai Hoa ({mai_hoa_verdict}: {mai_hoa_reason})")
        if luc_nham_reason:
            method_summaries.append(f"Đại Lục Nhâm ({luc_nham_verdict}: {luc_nham_reason})")
        if thai_at_reason:
            method_summaries.append(f"Thái Ất ({thai_at_verdict}: {thai_at_reason})")
        
        if method_summaries:
            narrative_parts.append("Cụ thể: " + "; ".join(method_summaries) + ".")
        
        # Part 3: Kết luận dứt khoát theo CÂU HỎI (V26.0: Xóa bỏ hardcode keyword match dễ lỗi)
        if overall == 'THUẬN LỢI':
            narrative_parts.append(f"👉 **KẾT LUẬN TRỰC TIẾP CHO '{question}': KHẢ THI / RẤT TỐT ({pct}%).** {dung_than} được hỗ trợ mạnh mẽ, nên hành động quyết đoán.")
            narrative_parts.append("💡 **Khuyên:** Thời điểm vượng khí, hãy tận dụng thời cơ đang có để triển khai rốt ráo.")
        elif overall == 'KHÓ KHĂN':
            narrative_parts.append(f"👉 **KẾT LUẬN TRỰC TIẾP CHO '{question}': KHÔNG ĐƯỢC / XẤU ({pct}%).** {dung_than} suy yếu, bế tắc, vạn sự khó thành.")
            narrative_parts.append("💡 **Khuyên:** Năng lượng yếu, tạm thời đình chỉ hành động hoặc tìm thêm nhân tố trợ lực (Quý nhân).")
        else:
            narrative_parts.append(f"👉 **KẾT LUẬN TRỰC TIẾP CHO '{question}': BÌNH BÌNH ({pct}%).** Các yếu tố đang ở mức giằng co, lấp lửng thiếu rõ ràng.")
            narrative_parts.append("💡 **Khuyên:** Quan sát thêm, thu thập thêm thông tin mở rộng cục diện rồi mới quyết định.")
        
        # Kết hợp narrative
        lines.append("\n".join(narrative_parts))
        
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
            return f"Chào bạn, tôi là THIÊN CƠ ĐẠI SƯ (V27.0 Unified + Deep Integration). 6 phương pháp (KM+LH+MH+TB+LN+TA) → 1 câu trả lời! Tích hợp 3 tầng LH+TS+NK. Đã học {lc} câu hỏi mới."
        
        # ====== V8.2: SMART CATEGORY DETECTION ======
        # Phân loại câu hỏi theo 6 nhóm lớn thay vì match 220+ topics cụ thể
        q_lower = question.lower()
        
        CATEGORIES = {
            "SỨC_KHỎE_GIA_ĐÌNH": {
                "keywords": ["bệnh", "ốm", "đau", "sức khỏe", "khỏe", "chết", "mất người",
                             "gia đình", "thai", "mang thai", "bố mất", "mẹ mất", "chết chưa",
                             "sống", "chữa", "bệnh viện", "phẫu thuật", "ung thư", "tai nạn", "nguy hiểm",
                             "qua khỏi", "cứu được", "nằm viện", "thuốc", "trị bệnh", "khỏi bệnh"],
                "dung_than": "Bản Thân",
                "dung_than_detail": {"bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu", "cha": "Phụ Mẫu", 
                                     "con": "Tử Tôn", "con trai": "Tử Tôn", "con gái": "Tử Tôn",
                                     "vợ": "Thê Tài", "chồng": "Quan Quỷ",
                                     "anh": "Huynh Đệ", "chị": "Huynh Đệ", "em": "Huynh Đệ"},
                "label": "🏥 Sức Khỏe / Gia Đình",
                "hint": "Phân tích sức khỏe. DT mặc định = hào Thế (Bản Thân). Quan Quỷ = bệnh tinh (nguyên nhân bệnh). Phụ Mẫu = bố mẹ. Tử Tôn = con cái."
            },
            "TÀI_CHÍNH": {
                "keywords": ["tiền", "tài chính", "mua bán", "đầu tư", "giàu", "nghèo", "lương", "thu nhập", "nợ", 
                             "vay", "cho vay", "kinh doanh", "buôn bán", "lãi", "lỗ", "cổ phiếu", "crypto",
                             "bitcoin", "nhà đất", "mua nhà", "bất động sản", "vốn", "hùn vốn", "trúng số",
                             "tài sản", "vàng", "bạc", "kim cương", "trang sức"],
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
                             "khởi nghiệp", "startup", "bổ nhiệm", "chuyển công tác"],
                "dung_than": "Quan Quỷ",
                "dung_than_detail": {"con trai": "Tử Tôn", "con gái": "Tử Tôn", "con": "Tử Tôn"},
                "label": "💼 Công Việc / Sự Nghiệp / Thi Cử",
                "hint": "Phân tích công việc, thi cử. Quan Quỷ = sếp/cơ quan. Khai Môn = khởi đầu."
            },
            "TÌNH_CẢM": {
                "keywords": ["yêu", "người yêu", "vợ", "chồng", "hôn nhân", "cưới", "ly hôn", "tình", 
                             "hẹn hò", "chia tay", "ngoại tình", "duyên", "vợ chồng", "đám cưới",
                             "bạn trai", "bạn gái", "tình cảm", "hạnh phúc", "ghen",
                             "lấy vợ", "lấy chồng", "kết hôn", "thật lòng", "tình yêu", "hôn"],
                "dung_than": "Thê Tài",
                "dung_than_detail": {"vợ": "Thê Tài", "chồng": "Quan Quỷ", "bạn gái": "Thê Tài", "bạn trai": "Quan Quỷ"},
                "label": "❤️ Tình Cảm / Hôn Nhân",
                "hint": "Phân tích tình cảm. Thê Tài = vợ/bạn gái. Quan Quỷ = chồng/bạn trai. Ứng hào = đối phương."
            },
            "TÌM_ĐỒ": {
                "keywords": ["tìm", "mất đồ", "ở đâu", "thất lạc", "trộm", "mất cắp", "chỗ nào",
                             "mất xe", "mất điện thoại", "mất tiền", "tìm đường", "lạc đường",
                             "mất ví", "mất đồ", "giấy tờ", "hướng nào", "để đâu", "cất đâu"],
                "dung_than": "Thê Tài",
                "dung_than_detail": {},
                "label": "🔍 Tìm Đồ / Tìm Người",
                "hint": "Phân tích hướng tìm. Dùng 9 cung Kỳ Môn → hướng. Cảnh Môn = đồ điện tử."
            },
            "NHÀ_CỬA": {
                "keywords": ["nhà", "tầng", "phòng", "căn hộ", "chung cư", "xây nhà", "sửa nhà", 
                             "nhà tôi", "nhà mấy", "phong thủy", "hướng nhà", "cửa nhà",
                             "dọn nhà", "chuyển nhà", "đất", "thửa đất", "lô đất"],
                "dung_than": "Thê Tài",
                "dung_than_detail": {},
                "label": "🏠 Nhà Cửa / Bất Động Sản",
                "hint": "Phân tích nhà cửa. Thê Tài = tài sản/nhà. Cấn = núi/nhà cao tầng."
            },
            "CHUNG": {
                "keywords": ["vận mệnh", "năm nay", "tháng này", "an toàn", "quý nhân", "may mắn"],
                "dung_than": "Bản Thân",
                "dung_than_detail": {},
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
        
        # V21.0: Xác định Dụng Thần chính xác — ưu tiên keyword dài hơn
        dung_than = cat_data["dung_than"]
        # Sort detail keywords by length (longest first) for best match
        detail_items = sorted(cat_data.get("dung_than_detail", {}).items(), key=lambda x: len(x[0]), reverse=True)
        for detail_kw, detail_dt in detail_items:
            if detail_kw in q_lower:
                dung_than = detail_dt
                break
        # V21.0: Override DT cho các trường hợp đặc biệt — CHỈ OVERRIDE khi CHƯA match detail người thân
        family_matched = dung_than != cat_data["dung_than"]  # True nếu đã match detail (bố→Phụ Mẫu, con→Tử Tôn...)
        if not family_matched:
            if 'sức khỏe tôi' in q_lower or 'tôi khỏe' in q_lower or ('tôi bệnh' in q_lower and 'bố tôi bệnh' not in q_lower and 'mẹ tôi bệnh' not in q_lower):
                dung_than = 'Bản Thân'
        if any(kw in q_lower for kw in ['anh chị em', 'anh em', 'mấy anh', 'mấy chị', 'bao nhiêu anh']):
            dung_than = 'Huynh Đệ'
            
        # V26.1: TÔN TRỌNG tuyệt đối quyết định tự chọn Dụng Thần của người dùng (từ Dropdown Streamlit)
        if selected_subject and selected_subject != "Không Rõ":
            dung_than = selected_subject
        
        is_age = _is_age_question(question)
        is_find = _is_find_question(question) and detected_category == "TÌM_ĐỒ"
        is_yesno = _is_yesno_question(question)
        is_count = _is_count_question(question)
        
        # V8.2: Nếu topic được truyền từ dropdown → vẫn match topic cũ
        # Nếu topic=None (Q&A tự do) → dùng smart category
        if topic:
            matched_topic, topic_data = _match_topic(question, topic)
        else:
            matched_topic, topic_data = None, None
        
        sections = []
        sections.append(f"## 🔮 THIÊN CƠ ĐẠI SƯ — V27.0 Unified + Deep Integration\n")
        sections.append(f"**Câu hỏi:** {question}\n")
        
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
        
        # V21.0: WEIGHTED AVERAGE — trọng số theo loại câu hỏi
        WEIGHT_MAP = {
            'SỨC_KHỎE_GIA_ĐÌNH': {'KM': 15, 'LH': 35, 'MH': 15, 'TB': 15, 'LN': 10, 'TA': 10},
            'TÀI_CHÍNH':         {'KM': 20, 'LH': 30, 'MH': 15, 'TB': 10, 'LN': 15, 'TA': 10},
            'CÔNG_VIỆC':          {'KM': 25, 'LH': 25, 'MH': 15, 'TB': 10, 'LN': 15, 'TA': 10},
            'TÌNH_CẢM':           {'KM': 15, 'LH': 30, 'MH': 20, 'TB': 10, 'LN': 15, 'TA': 10},
            'TÌM_ĐỒ':            {'KM': 35, 'LH': 20, 'MH': 15, 'TB': 10, 'LN': 10, 'TA': 10},
            'NHÀ_CỬA':           {'KM': 25, 'LH': 25, 'MH': 15, 'TB': 10, 'LN': 15, 'TA': 10},
            'CHUNG':              {'KM': 20, 'LH': 20, 'MH': 20, 'TB': 15, 'LN': 15, 'TA': 10},
        }
        weights = WEIGHT_MAP.get(detected_category, WEIGHT_MAP['CHUNG'])
        
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
        
        sections.append(f"| Phương pháp | Kết luận | Score | % | Trọng số |")
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
        sections.append(f"\n**📊 WEIGHTED SCORE: {weighted_pct}%** (có tính 12 Trường Sinh: {ts_bonus:+d}%)")
        
        # ═══════════════════════════════════════════════════════
        # V26.2: BƯỚC 5.7 — LƯỢNG HÓA LỰC LƯỢNG 3 TẦNG (UNIFIED STRENGTH)
        # Tích hợp _calc_unified_strength_tier() — hàm V21.0 viết nhưng chưa gọi
        # 3 nguồn: LH raw (50%) + 12 Trường Sinh (30%) + Ngũ Khí (20%)
        # ═══════════════════════════════════════════════════════
        hanh_dt_v22 = ''
        cung_bt_hanh_v22 = ''
        ngu_khi_state_v22 = 'Hưu'
        ngu_khi_pwr_v22 = 50
        unified_v22 = None
        
        if chart_data and isinstance(chart_data, dict):
            hanh_dt_v22 = CAN_NGU_HANH.get(chart_data.get('can_ngay', ''), '')
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
        
        sections.append(f"\n### 🧬 BƯỚC 5.7: LƯỢNG HÓA LỰC LƯỢNG (V26.2 UNIFIED STRENGTH)")
        
        # A. Bảng 3 tầng Unified
        sections.append(f"\n**A. 3 TẦNG ĐO LỰC LƯỢNG DT:**")
        sections.append(f"| Tầng | Nguồn | Score | Trọng số |")
        sections.append(f"|---|---|---|---|")
        sections.append(f"| ① Lục Hào raw | Score={v16_lh_raw:+d} → normalize | {unified_v22['lh_pct']}% | 50% |")
        sections.append(f"| ② 12 Trường Sinh | {ts_stage or 'N/A'} ({TRUONG_SINH_POWER.get(ts_stage, {}).get('cap', '?') if ts_stage else '?'}) | {unified_v22['ts_pct']}% | 30% |")
        sections.append(f"| ③ Ngũ Khí | {ngu_khi_state_v22} ({hanh_dt_v22} @ {cung_bt_hanh_v22 or '?'}) | {unified_v22['nk_pct']}% | 20% |")
        sections.append(f"| **UNIFIED** | **3 tầng tổng hợp** | **{unified_v22['unified_pct']}%** | {unified_v22['tier_data']['cap']} |")
        sections.append(f"| **WEIGHTED 5PP** | **KM+LH+MH+LN+TA** | **{weighted_pct}%** | {vv_data['cap']} |")
        
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
            
            sections.append(f"\n**A2. 📋 THỐNG KÊ TOÀN BỘ YẾU TỐ TÁC ĐỘNG DT (V26.2) — {len(v23_lh_factors)} yếu tố:**")
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
        
        # Đếm số lượng (V8.0)
        if is_count and count_numbers:
            sections.append(f"\n**📊 Bảng số lượng từ các phương pháp:**")
            for pp, num in count_numbers:
                sections.append(f"- {pp}: **{num}**")
            all_nums = [n for _, n in count_numbers]
            if len(all_nums) >= 2:
                avg = sum(all_nums) / len(all_nums)
                sections.append(f"\n→ **KẾT LUẬN SỐ LƯỢNG: Khoảng {int(round(avg))}** (tổng hợp từ {len(count_numbers)} phương pháp)")
            elif len(all_nums) == 1:
                sections.append(f"\n→ **KẾT LUẬN SỐ LƯỢNG: Khoảng {all_nums[0]}**")
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
            weighted_pct=weighted_pct
        )
        
        # ========================================
        # KẾT LUẬN THỐNG NHẤT (V11.0)
        # ========================================
        sections.append(f"\n### 🏆 KẾT LUẬN THỐNG NHẤT")
        
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
            final_pct=weighted_pct
        )
        sections.append(unified_narrative)
        
        sections.append(f"\n---\n*🤖 Thiên Cơ Đại Sư V26.2 — Unified Strength: Weighted 5PP={weighted_pct}%, Unified 3-Tier={unified_v22['unified_pct']}%, Ngũ Khí={ngu_khi_state_v22}.*")
        
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
                        if cv == 'Mậu':
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
                if dt_cung_v15 and dt_cung_v15 != chu_cung_v15:
                    dt_s, dt_d, dt_str = self._analyze_cung_factors(dt_cung_v15, chart_data, question, f"DỤNG THẦN ({dung_than})")
                    v15_dt_score = f"Cung {dt_cung_v15} ({QUAI_TUONG.get(dt_cung_v15, '?')}, {CUNG_NGU_HANH.get(dt_cung_v15, '?')}): Score={dt_s}, {dt_str}"
                    dt_score_val = dt_s
                
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
            # V18.0: Detective deduction
            'v18_detective': v18_detective,
            # V26.2: Unified Strength — 3 tầng tổng hợp
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
        }
        
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
            # AI Online thành công → Hiện Online TRƯỚC, Offline ẩn sau
            final_parts = []
            final_parts.append(f"## 🌐 AI ONLINE — KẾT LUẬN CUỐI CÙNG (Gemini)")
            final_parts.append(online_result)
            final_parts.append("")
            final_parts.append("\n<details>")
            final_parts.append("<summary><b>📦 Xem Chi Tiết AI Offline — THIÊN CƠ ĐẠI SƯ V26.2 (nhấn để mở)</b></summary>\n")
            final_parts.append(offline_full_output)
            final_parts.append("\n</details>")
            return "\n".join(final_parts)
        else:
            # AI Online không khả dụng → Hiện KếT LUẬN trực tiếp, offline chi tiết ẩn sau
            error_reasons = []
            for log in self.logs:
                if log.get('step') == 'Online AI' and log.get('status') in ['SKIP', 'ERROR']:
                    error_reasons.append(log.get('detail', ''))
            
            error_msg = error_reasons[-1] if error_reasons else "Không có API Key hoặc hết hạn mức"
            
            # === V26.2: BUILD COMPREHENSIVE OFFLINE CONCLUSION ===
            pct_short = weighted_pct  # Từ BƯỚC 6 đã tính
            unified_pct_short = unified_v22['unified_pct'] if unified_v22 else pct_short
            
            if pct_short >= 65:
                overall_short = 'THUẬN LỢI'
                v_icon = '✅'
            elif pct_short >= 50:
                overall_short = 'BÌNH THƯỜNG'
                v_icon = '🟡'
            elif pct_short >= 35:
                overall_short = 'KHÓ KHĂN'
                v_icon = '🔴'
            else:
                overall_short = 'RẤT KHÓ KHĂN'
                v_icon = '🔴'
            
            final_parts = []
            final_parts.append(f"## 🖥️ AI OFFLINE — THIÊN CƠ ĐẠI SƯ V26.2")
            final_parts.append(f"*⚠️ AI Online không khả dụng: {error_msg}*")
            final_parts.append("")
            final_parts.append(f"## {v_icon} KẾT LUẬN: {overall_short} ({pct_short}%)")
            final_parts.append(f"**Dụng Thần:** {dung_than} | **KM:** {ky_mon_verdict} | **LH:** {luc_hao_verdict} | **MH:** {mai_hoa_verdict} | **LN:** {luc_nham_verdict} | **TA:** {thai_at_verdict}")
            final_parts.append(f"\n**📊 Unified Strength (3 tầng):** {unified_pct_short}% ({unified_v22['tier_data']['cap'] if unified_v22 else '?'}) | **Ngũ Khí:** {ngu_khi_state_v22} | **12 Trường Sinh:** {ts_stage or 'N/A'}")
            
            # V26.2: VẠN VẬT CỤ THỂ trong KẾT LUẬN
            vv_cu_the_kl = _get_van_vat_cu_the(hanh_dt_v22, unified_v22.get('tier_key', 'TRUNG_BÌNH') if unified_v22 else 'TRUNG_BÌNH')
            if vv_cu_the_kl and hanh_dt_v22:
                final_parts.append(f"\n### 🎯 VẠN VẬT CỤ THỂ ({hanh_dt_v22} × {unified_v22['tier_data']['cap'] if unified_v22 else '?'})")
                final_parts.append(f"- 🔮 **Đồ vật:** {vv_cu_the_kl.get('do_vat', '?')}")
                final_parts.append(f"- 🏠 **Nhà cửa:** {vv_cu_the_kl.get('nha_cua', '?')}")
                final_parts.append(f"- 🧑 **Người:** {vv_cu_the_kl.get('nguoi', '?')}")
                final_parts.append(f"- 🏥 **Bệnh:** {vv_cu_the_kl.get('benh', '?')}")
            
            # ═══════════════════════════════════════════════════════
            # V21.0: TRẢ LỜI TRỰC TIẾP — THÔNG MINH THEO LOẠI CÂU HỎI
            # ═══════════════════════════════════════════════════════
            q_lower = question.lower()
            
            # --- 1. CÓ/KHÔNG ---
            is_yesno = any(k in q_lower for k in ['có nên', 'có được', 'được không', 'nên không', 'có thể',
                                                    'có thành', 'có đỗ', 'có đạt', 'có thắng', 'có tốt',
                                                    'có nên mua', 'nên đầu tư', 'có đi', 'có lấy'])
            # --- 2. SINH TỬ ---
            is_health_critical = any(k in q_lower for k in ['mất hay chưa', 'chết chưa', 'còn sống', 'sống không',
                                                             'qua khỏi', 'cứu được', 'mất chưa', 'bệnh nặng',
                                                             'phẫu thuật', 'ung thư', 'nguy hiểm'])
            # --- 3. KHI NÀO ---
            is_when = any(k in q_lower for k in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'khi nao'])
            # --- 4. BAO NHIÊU ---
            is_count_q = any(k in q_lower for k in ['bao nhiêu', 'mấy người', 'mấy cái', 'mấy đứa', 'mấy anh',
                                                     'mấy chị', 'số lượng', 'có mấy'])
            # --- 5. Ở ĐÂU ---
            is_find = any(k in q_lower for k in ['ở đâu', 'hướng nào', 'phương nào', 'tìm đâu', 'chỗ nào',
                                                   'nơi nào', 'để đâu', 'để chỗ', 'cất đâu'])
            # --- 6. TÌNH CẢM ---
            is_emotion = any(k in q_lower for k in ['thật lòng', 'yêu thương', 'còn yêu', 'ngoại tình',
                                                      'chung thủy', 'lấy vợ', 'lấy chồng', 'cưới', 'chia tay'])
            # --- 7. SỨC KHỎE (không phải sinh tử) ---
            is_health = any(k in q_lower for k in ['sức khỏe', 'khỏe', 'bệnh', 'ốm', 'đau']) and not is_health_critical
            
            final_parts.append("")
            final_parts.append(f"**❓ Câu hỏi:** {question}")
            final_parts.append("")
            
            # ═══════ TRẢ LỜI THEO LOẠI ═══════
            if is_health_critical:
                if pct_short >= 60:
                    final_parts.append(f"### 🟢 CÂU TRẢ LỜI: TÌNH TRẠNG KHẢ QUAN — {pct_short}%")
                    final_parts.append(f"Quẻ cho thấy **{dung_than}** còn sức, có dấu hiệu hồi phục.")
                    final_parts.append(f"- Dụng Thần được sinh trợ → có quý nhân giúp đỡ, y thuật hiệu quả.")
                    final_parts.append(f"- Nên tích cực điều trị, tuân thủ phác đồ bác sĩ.")
                elif pct_short >= 40:
                    final_parts.append(f"### 🟡 CÂU TRẢ LỜI: TÌNH TRẠNG CẦN THEO DÕI SÁT — {pct_short}%")
                    final_parts.append(f"**{dung_than}** đang ở mức trung bình, chưa nguy kịch nhưng cần cẩn thận.")
                    final_parts.append(f"- Nên hội chẩn nhiều bác sĩ, không tự ý dùng thuốc.")
                    final_parts.append(f"- Theo dõi sát, tìm phương pháp điều trị phù hợp.")
                else:
                    final_parts.append(f"### 🔴 CÂU TRẢ LỜI: TÌNH TRẠNG NGHIÊM TRỌNG — {pct_short}%")
                    final_parts.append(f"**{dung_than}** rất yếu, cần hành động khẩn cấp.")
                    final_parts.append(f"- Quẻ cho thấy nhiều yếu tố bất lợi → cần can thiệp y tế NGAY.")
                    final_parts.append(f"- Nên tìm bác sĩ giỏi nhất có thể, không trì hoãn.")
                    
            elif is_yesno:
                if pct_short >= 65:
                    final_parts.append(f"### ✅ CÂU TRẢ LỜI: CÓ — Khả năng thành công {pct_short}%")
                    final_parts.append(f"Quẻ cho thấy {dung_than} vượng ({pct_short}%), điều kiện THUẬN LỢI.")
                    # Advice per category
                    if detected_category == 'TÀI_CHÍNH':
                        final_parts.append(f"- 💰 Thời điểm tốt để giao dịch. Kiểm tra kỹ giấy tờ, hợp đồng.")
                        final_parts.append(f"- Nên hành động nhanh, tận dụng cơ hội trước khi khí chuyển.")
                    elif detected_category == 'CÔNG_VIỆC':
                        final_parts.append(f"- 💼 Công việc/thi cử thuận lợi. Hãy TỰ TIN hành động.")
                        final_parts.append(f"- Có quý nhân hỗ trợ, nắm bắt cơ hội ngay.")
                    elif detected_category == 'TÌNH_CẢM':
                        final_parts.append(f"- 💕 Duyên phận thuận lợi, mối quan hệ có triển vọng tốt đẹp.")
                    else:
                        final_parts.append(f"- Nên hành động sớm, tận dụng thời cơ.")
                elif pct_short >= 45:
                    final_parts.append(f"### 🟡 CÂU TRẢ LỜI: CÒN PHẢI XEM — Tình thế chưa rõ ({pct_short}%)")
                    final_parts.append(f"Quẻ ở mức CÂN BẰNG — không hẳn tốt, không hẳn xấu.")
                    final_parts.append(f"- Nên thu thập thêm thông tin, thăm dò trước khi quyết định.")
                    final_parts.append(f"- Chờ 1-2 tuần sẽ có tín hiệu rõ ràng hơn.")
                else:
                    final_parts.append(f"### 🔴 CÂU TRẢ LỜI: KHÔNG NÊN — Xác suất bất lợi {100-pct_short}%")
                    final_parts.append(f"Quẻ cho thấy {dung_than} suy ({pct_short}%), nhiều yếu tố CẢN TRỞ.")
                    if detected_category == 'TÀI_CHÍNH':
                        final_parts.append(f"- ❌ Không nên giao dịch lớn lúc này. Chờ 2-4 tuần.")
                        final_parts.append(f"- Huynh Đệ (kiếp tài) mạnh → dễ mất tiền, hao tài.")
                    elif detected_category == 'CÔNG_VIỆC':
                        final_parts.append(f"- ❌ Chưa phải lúc. Nên chuẩn bị thêm, chờ thời cơ mới.")
                    else:
                        final_parts.append(f"- ❌ Kiên nhẫn chờ đợi, tìm quý nhân hỗ trợ.")
                        
            elif is_when:
                final_parts.append(f"### ⏰ CÂU TRẢ LỜI VỀ THỜI GIAN")
                if pct_short >= 60:
                    final_parts.append(f"- Thời điểm HIỆN TẠI đã thuận lợi ({pct_short}%). Nên hành động trong **1-7 ngày tới**.")
                    final_parts.append(f"- Dụng Thần {dung_than} đang vượng → sự việc sẽ xảy ra NHANH.")
                elif pct_short >= 40:
                    final_parts.append(f"- Sự việc cần thêm thời gian ({pct_short}%). Dự kiến **1-3 tháng** tới.")
                    final_parts.append(f"- Dụng Thần ở mức trung bình → cần chờ khí vượng lên.")
                else:
                    final_parts.append(f"- Sự việc CHẬM TRỄ ({pct_short}%). Có thể cần **3-6 tháng** hoặc lâu hơn.")
                    final_parts.append(f"- Dụng Thần suy → cần có yếu tố mới xoay chuyển tình thế.")
                # Thêm gợi ý từ Trường Sinh
                if ts_stage:
                    ts_time_hint = {
                        'Trường Sinh': 'Sự việc MỚI BẮT ĐẦU, sẽ phát triển dần',
                        'Mộc Dục': 'Đang trong giai đoạn CHUẨN BỊ, chưa rõ ràng',
                        'Quan Đới': 'SẮP ĐẾN thời điểm hành động',
                        'Lâm Quan': 'ĐÚNG LÚC, hành động ngay',
                        'Đế Vượng': 'ĐỈNH ĐIỂM — không chờ thêm, làm NGAY',
                        'Suy': 'Đã qua thời điểm tốt nhất, còn cơ hội nhỏ',
                        'Bệnh': 'Chậm trễ, cần kiên nhẫn chờ',
                        'Tử': 'RẤT CHẬM, sự việc đình đốn',
                        'Mộ': 'Sự việc bị GIỮ LẠI, chờ giải thoát',
                        'Tuyệt': 'Sự việc ngưng trệ, chờ chu kỳ mới',
                        'Thai': 'Mầm mống mới đang hình thành',
                        'Dưỡng': 'Sắp có tin tức, kiên nhẫn thêm chút nữa',
                    }
                    final_parts.append(f"- 📅 **12 Trường Sinh:** {ts_stage} → {ts_time_hint.get(ts_stage, '')}")
                    
            elif is_count_q:
                final_parts.append(f"### 📊 CÂU TRẢ LỜI VỀ SỐ LƯỢNG")
                if count_numbers:
                    all_nums_s = [n for _, n in count_numbers]
                    avg_s = int(round(sum(all_nums_s) / len(all_nums_s))) if all_nums_s else 0
                    detail_s = ', '.join(f'{pp}={n}' for pp, n in count_numbers)
                    final_parts.append(f"- Kết luận: Khoảng **{avg_s}** (từ {len(count_numbers)} phương pháp: {detail_s})")
                else:
                    # Estimate from weighted_pct
                    if pct_short >= 70: est_count = '4-5+'
                    elif pct_short >= 50: est_count = '2-3'
                    elif pct_short >= 30: est_count = '1-2'
                    else: est_count = '0-1'
                    final_parts.append(f"- Ước tính: Khoảng **{est_count}** (dựa trên lực lượng DT {pct_short}%)")
                # Thêm vạn vật mapping liên quan
                vv_key_c, vv_data_c = _get_van_vat_from_pct(pct_short)
                final_parts.append(f"- Vạn Vật: {vv_data_c['so_luong']} | Con số: {vv_data_c['so']}")
                    
            elif is_find:
                final_parts.append(f"### 📍 CÂU TRẢ LỜI VỀ VỊ TRÍ/HƯỚNG")
                # Extract from direct_answer if available
                if direct_answer and ('HƯỚNG' in direct_answer or 'hướng' in direct_answer.lower()):
                    for line in direct_answer.split('\n'):
                        if line.strip():
                            final_parts.append(line)
                else:
                    final_parts.append(f"- Xem phần chi tiết bên dưới để biết hướng chính xác từ Kỳ Môn Độn Giáp.")
                if pct_short >= 50:
                    final_parts.append(f"- ✅ Khả năng TÌM THẤY: **CAO** ({pct_short}%)")
                else:
                    final_parts.append(f"- ⚠️ Khả năng tìm thấy: **THẤP** ({pct_short}%), đồ có thể đã hư hỏng hoặc mất hẳn.")
                    
            elif is_emotion:
                final_parts.append(f"### 💕 CÂU TRẢ LỜI VỀ TÌNH CẢM")
                if pct_short >= 65:
                    final_parts.append(f"- ✅ Mối quan hệ **TỐT ĐẸP** ({pct_short}%). Đối phương THẬT LÒNG.")
                    final_parts.append(f"- Dụng Thần {dung_than} vượng → tình cảm chân thành, bền vững.")
                    if 'lấy vợ' in q_lower or 'lấy chồng' in q_lower or 'cưới' in q_lower:
                        final_parts.append(f"- 💒 Duyên phận thuận lợi, nên tiến tới.")
                elif pct_short >= 40:
                    final_parts.append(f"- 🟡 Mối quan hệ ở mức **BÌNH THƯỜNG** ({pct_short}%). Cần thêm thời gian.")
                    final_parts.append(f"- Có yếu tố chưa rõ ràng → nên trò chuyện thẳng thắn.")
                else:
                    final_parts.append(f"- 🔴 Mối quan hệ **GẶP KHÓ KHĂN** ({pct_short}%). Đối phương KHÔNG thật lòng.")
                    final_parts.append(f"- Dụng Thần {dung_than} suy → tình cảm phai nhạt, có dấu hiệu lừa dối.")
                    
            elif is_health:
                final_parts.append(f"### 🏥 CÂU TRẢ LỜI VỀ SỨC KHỎE")
                if pct_short >= 60:
                    final_parts.append(f"- ✅ Sức khỏe **TỐT** ({pct_short}%). Thể trạng khỏe mạnh.")
                    final_parts.append(f"- Duy trì lối sống lành mạnh, tập thể dục đều đặn.")
                elif pct_short >= 40:
                    final_parts.append(f"- 🟡 Sức khỏe **BÌNH THƯỜNG** ({pct_short}%). Có vấn đề nhỏ cần chú ý.")
                    final_parts.append(f"- Nên đi khám định kỳ, điều chỉnh chế độ ăn uống.")
                else:
                    final_parts.append(f"- 🔴 Sức khỏe **CẦN LƯU Ý** ({pct_short}%). Có dấu hiệu suy yếu.")
                    final_parts.append(f"- Nên đi khám bác sĩ sớm, không tự chữa tại nhà.")
            else:
                # DEFAULT — câu hỏi chung (vận mệnh, quý nhân, tổng quát...)
                final_parts.append(f"### 🔮 CÂU TRẢ LỜI")
                if pct_short >= 65:
                    final_parts.append(f"- ✅ **THUẬN LỢI** ({pct_short}%). Tình hình khả quan, sự việc phát triển tốt.")
                    final_parts.append(f"- {dung_than} vượng → bạn đang ở thế chủ động, tự tin hành động.")
                elif pct_short >= 50:
                    final_parts.append(f"- 🟡 **BÌNH THƯỜNG** ({pct_short}%). Không nổi bật nhưng không tiêu cực.")
                    final_parts.append(f"- Giữ nguyên hiện trạng, quan sát thêm diễn biến.")
                elif pct_short >= 35:
                    final_parts.append(f"- 🔴 **KHÓ KHĂN** ({pct_short}%). Nhiều trở ngại cần vượt qua.")
                    final_parts.append(f"- Kiên nhẫn chờ đợi, tìm quý nhân, tránh liều lĩnh.")
                else:
                    final_parts.append(f"- 🔴 **RẤT KHÓ KHĂN** ({pct_short}%). Tình hình bất lợi nghiêm trọng.")
                    final_parts.append(f"- Không nên ép buộc, chờ chu kỳ mới khởi phát.")
            
            # ═══════ GIẢI THÍCH TẠI SAO ═══════
            final_parts.append(f"\n### 📋 TẠI SAO KẾT LUẬN NHƯ VẬY?")
            
            # Xếp PP theo score mạnh→yếu
            pp_ranking = sorted(
                [('Kỳ Môn', v16_km_raw, ky_mon_verdict), 
                 ('Lục Hào', v16_lh_raw, luc_hao_verdict),
                 ('Mai Hoa', v16_mh_raw, mai_hoa_verdict),
                 ('Thiết Bản', v16_tb_raw, 'BÌNH'),
                 ('Đại Lục Nhâm', v16_ln_raw, luc_nham_verdict),
                 ('Thái Ất', v16_ta_raw, thai_at_verdict)],
                key=lambda x: x[1], reverse=True
            )
            
            for pp_name, pp_raw, pp_verdict in pp_ranking:
                if pp_raw > 5:
                    final_parts.append(f"- ✅ **{pp_name}**: {pp_verdict} (score {pp_raw:+d}) → Yếu tố THUẬN LỢI")
                elif pp_raw < -5:
                    final_parts.append(f"- 🔴 **{pp_name}**: {pp_verdict} (score {pp_raw:+d}) → Yếu tố BẤT LỢI")
                else:
                    final_parts.append(f"- 🟡 **{pp_name}**: {pp_verdict} (score {pp_raw:+d}) → Trung tính")
            
            # V26.2: THỐNG KÊ TOÀN DIỆN CÁC YẾU TỐ (ĐA MÔN PHÁI)
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
            
            # Trường Sinh context
            if ts_stage:
                ts_info = TRUONG_SINH_POWER.get(ts_stage, {})
                final_parts.append(f"\n**12 Trường Sinh:** {ts_stage} ({ts_info.get('cap', '?')}, power={ts_info.get('power', 50)}%)")
                final_parts.append(f"→ Con người: {ts_info.get('con_nguoi', '?')}")
                final_parts.append(f"→ Vật: {ts_info.get('vat', '?')}")
            
            # V21.0: MAPPING VẠN VẬT
            vv_key_f, vv_data_f = _get_van_vat_from_pct(pct_short)
            final_parts.append(f"\n### 🧬 MAPPING VẠN VẬT ({vv_data_f['cap']})")
            final_parts.append(f"🧑 **Vòng đời:** {vv_data_f['con_nguoi']}")
            final_parts.append(f"📐 **Kích thước:** {vv_data_f['kich_thuoc']} | 🆕 **Tình trạng:** {vv_data_f['tinh_trang']}")
            final_parts.append(f"🔢 **Số lượng:** {vv_data_f['so_luong']} | 💎 **Chất lượng:** {vv_data_f['chat_luong']}")
            final_parts.append(f"🔢 **Con số:** {vv_data_f['so']}")
            
            # Lời khuyên cuối
            final_parts.append(f"\n### 💡 LỜI KHUYÊN HÀNH ĐỘNG")
            if pct_short >= 65:
                final_parts.append("- ✅ Hành động sớm, tận dụng thời cơ. Mọi điều kiện đang có lợi cho bạn.")
            elif pct_short >= 50:
                final_parts.append("- ⏸️ Quan sát thêm, thu thập thông tin rồi quyết định. Không vội vàng.")
            elif pct_short >= 35:
                final_parts.append("- ❌ Kiên nhẫn chờ đợi. Tìm quý nhân hỗ trợ, không nên ép buộc.")
            else:
                final_parts.append("- 🛑 Dừng lại, không hành động. Chờ chu kỳ mới, mọi thứ sẽ chuyển biến.")
            
            final_parts.append("")
            
            # MỌI THỨ chi tiết ẩn sau 1 nút bấm duy nhất
            final_parts.append("\n<details>")
            final_parts.append("<summary><b>📦 Xem Chi Tiết Phân Tích V26.2 (nhấn để mở)</b></summary>\n")
            final_parts.append(offline_full_output)
            final_parts.append("\n</details>")
            final_parts.append(f"\n💡 Để dùng AI thông minh hơn, nhập API Key tại [Google AI Studio](https://aistudio.google.com/).")
            return "\n".join(final_parts)

    # ===========================
    # SUY LUẬN RIÊNG (khi không trùng chủ đề)
    # ===========================
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
                lines.append(f"\n  **🕳️ TUẦN KHÔNG TỨ TRỤ (V15.0):**")
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
                lines.append(f"\n  **🐎 DỊCH MÃ TỨ TRỤ (V15.0):**")
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
                lines.append(f"\n  **📜 TỨ TRỤ Ý NGHĨA (V15.0):**")
                
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
            
            # Tuổi
            if is_age and quai in TIEN_THIEN:
                tt_num = TIEN_THIEN[quai]
                if 'ĐƯỢC SINH' in relation or 'Tỷ' in relation:
                    age_num = tt_num * 5
                else:
                    age_num = tt_num * 3
                lines.append(f"  - Tuổi (Tiên Thiên {quai}={tt_num}): **{age_num}**")
            
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
            lines.append(f"\n**☯️ Bảng 6 Hào:**")
            lines.append(f"| Hào | Lục Thân | Can Chi | Ngũ Hành | Thế/Ứng | Động |")
            lines.append(f"|:---:|:---:|:---:|:---:|:---:|:---:|")
            for i, hao in enumerate(haos):
                luc_than = hao.get('luc_than', '?')
                can_chi = hao.get('can_chi', '?')
                ngu_hanh = hao.get('ngu_hanh', '?')
                the_ung = hao.get('the_ung', '')
                is_dong = '🔴 Động' if (i+1) in dong_hao else ''
                
                lines.append(f"| {i+1} | {luc_than} | {can_chi} | {ngu_hanh} | {the_ung} | {is_dong} |")
                
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
            
            # V8.0: HÀO ĐỘNG chi tiết + V9.0 TẤN/THOÁI THẦN
            if dong_hao:
                lines.append(f"\n**🔴 Phân tích Hào Động:**")
                bien_haos = bien.get('haos') or bien.get('details', []) if bien else []
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
            
            # ====== V9.0: KHÔNG VONG (Tuần Không) ======
            can_ngay_lh = luc_hao_data.get('can_ngay', '') or luc_hao_data.get('ban', {}).get('can_ngay', '')
            chi_ngay_lh = luc_hao_data.get('chi_ngay', '') or luc_hao_data.get('ban', {}).get('chi_ngay', '')
            khong_vong_list = _get_khong_vong(can_ngay_lh, chi_ngay_lh)
            if khong_vong_list and dung_than_hao:
                dt_chi = dung_than_hao.get('chi', '')
                if dt_chi in khong_vong_list:
                    lines.append(f"\n**🕳️ KHÔNG VONG (V9.0):** Dụng Thần ({dt_chi}) lâm Tuần Không [{', '.join(khong_vong_list)}]")
                    lines.append(f"  → Sự việc HƯ, TRỐNG RỖNG — Chờ đến khi Xuất Không (gặp Chi {dt_chi}) mới ứng nghiệm!")
                    reasons_list.append("Dụng Thần Không Vong")
                    if verdict == "CÁT":
                        verdict = "BÌNH"
            
            # ====== V9.0: NGUYỆT PHÁ ======
            chi_thang_lh = luc_hao_data.get('chi_thang', '')
            if chi_thang_lh and dung_than_hao:
                dt_chi = dung_than_hao.get('chi', '')
                if dt_chi and LUC_XUNG_CHI.get(chi_thang_lh) == dt_chi:
                    lines.append(f"\n**💥 NGUYỆT PHÁ (V9.0):** Chi tháng {chi_thang_lh} xung Dụng Thần ({dt_chi})")
                    lines.append(f"  → Dụng Thần bị NGUYỆT PHÁ = Sức mạnh TAN VỠ, sự việc KHÓ THÀNH! ⚠️")
                    reasons_list.append("Dụng Thần Nguyệt Phá")
                    verdict = "HUNG"
            
            # ====== V9.0: TAM HỢP CỤC ======
            if haos:
                all_chi = [h.get('chi', '') for h in haos if h.get('chi')]
                for tam_hop_set, (thc_hanh, thc_desc) in TAM_HOP_CUC.items():
                    matching = [c for c in all_chi if c in tam_hop_set]
                    if len(matching) >= 3:
                        lines.append(f"\n**🔗 TAM HỢP CỤC (V9.0):** {thc_desc}")
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
                        lines.append(f"\n**⚡ LỤC XUNG THẾ-ỨNG (V9.0):** {the_chi} xung {ung_chi}")
                        lines.append(f"  → Người hỏi và đối phương/sự việc XUNG ĐỘT, khó hòa hợp!")
                        reasons_list.append("Thế Ứng Lục Xung")
                    elif LUC_HOP_CHI.get(the_chi) == ung_chi:
                        lines.append(f"\n**🤝 LỤC HỢP THẾ-ỨNG (V9.0):** {the_chi} hợp {ung_chi}")
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
            
            # ====== V9.0: ỨNG KỲ ======
            if hanh and verdict:
                ung_ky_text = _get_ung_ky(hanh, verdict)
                lines.append(f"\n**⏰ ỨNG KỲ (V9.0):** {ung_ky_text}")
            
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
            
            # Tuổi
            if is_age and the_hao:
                chi_t = the_hao.get('chi', '')
                hanh_chi = CHI_NGU_HANH.get(chi_t, '')
                for q, h in {'Càn': 'Kim', 'Đoài': 'Kim', 'Ly': 'Hỏa', 'Chấn': 'Mộc', 'Tốn': 'Mộc', 'Khảm': 'Thủy', 'Cấn': 'Thổ', 'Khôn': 'Thổ'}.items():
                    if h == hanh_chi:
                        tt = TIEN_THIEN[q]
                        if 'Vượng' in str(vuong):
                            age_num = tt * 5
                        else:
                            age_num = tt * 3
                        lines.append(f"- Tuổi (Lục Hào: {chi_t} → {q}, Tiên Thiên={tt}): **{age_num}**")
                        break
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
        
        lines.append(f"- **Quẻ Chủ:** {mai_hoa_data.get('ten', '?')}")
        lines.append(f"- **Quẻ Biến:** {mai_hoa_data.get('ten_qua_bien', '?')}")
        lines.append(f"- **Hào Động:** {dong_hao}")
        lines.append(f"- **Thể ({the_label}):** {the_name} ({the_el})")
        lines.append(f"- **Dụng ({dung_label}):** {dung_name} ({dung_el})")
        
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
                lines.append(f"\n**🌿 LỆNH THÁNG (V9.0):** {lenh_mua} — {lenh_hanh} vượng")
                lines.append(f"  → Thể quái ({the_el}) ĐANG VƯỢNG theo mùa = Sức mạnh TĂNG GẤP ĐÔI! ✅")
                if verdict == "HUNG":
                    verdict = "BÌNH"
                    reason += " + Thể vượng lệnh"
            elif KHAC.get(lenh_hanh) == the_el:
                lines.append(f"\n**🍂 LỆNH THÁNG (V9.0):** {lenh_mua} — {lenh_hanh} vượng")
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
                lines.append(f"\n**🤝 HỖ QUÁI SINH THỂ (V9.0):** Hỗ ({ho_el}) sinh Thể ({the_el})")
                lines.append(f"  → Có QUÝ NHÂN ẨN giúp đỡ, sự việc có nền tảng bên trong! ✅")
            elif KHAC.get(ho_el) == the_el:
                lines.append(f"\n**⚠️ HỖ QUÁI KHẮC THỂ (V9.0):** Hỗ ({ho_el}) khắc Thể ({the_el})")
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
                            lines.append(f"\n**🔮 BIẾN QUÁI SINH THỂ (V9.0):** Biến ({bien_el}) sinh Thể ({the_el})")
                            lines.append(f"  → Kết cục TỐT HƠN dự kiến, có chuyển biến tích cực! ✅")
                        elif KHAC.get(bien_el) == the_el:
                            lines.append(f"\n**🔮 BIẾN QUÁI KHẮC THỂ (V9.0):** Biến ({bien_el}) khắc Thể ({the_el})")
                            lines.append(f"  → Kết cục XẤU HƠN, hậu quả lâu dài, cần đề phòng! ⚠️")
                    break
        
        # ====== V9.0: ỨNG KỲ MAI HOA ======
        if the_el and the_el != '?':
            ung_ky_text = _get_ung_ky(the_el, verdict)
            lines.append(f"\n**⏰ ỨNG KỲ (V9.0):** {ung_ky_text}")
        
        lines.append(f"\n  → **MAI HOA: {verdict}** ({reason})")
        
        # Tuổi
        if is_age and the_name in TIEN_THIEN:
            tt = TIEN_THIEN[the_name]
            if verdict == "CÁT":
                age_num = tt * 5
            else:
                age_num = tt * 3
            lines.append(f"- Tuổi (Mai Hoa: Thể={the_name}, Tiên Thiên={tt}): **{age_num}**")
        
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
                    lines.append(f"\n  **🔄 Trường Sinh Nạp Âm (V9.0):** {hanh_can} tại {chi_ngay} = **{ts_stage}**")
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
                lines.append(f"\n**🌟 THẦN SÁT (V9.0):**")
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
                        lines.append(f"\n  **📜 THOÁN TỪ (V9.0):** {thoan_info.get('thoan', '')}")
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
                        lines.append(f"\n  **📐 HÀO VỊ (V9.0):** Hào Thế ({the_pos}) = **{chinh_text}**{trung_text}")
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
                        lines.append(f"\n  **📜 THOÁN TỪ (V9.0):** {thoan_info.get('thoan', '')}")
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
        section, verdict, _, _reason, _cnt = self._analyze_luc_hao_full(luc_hao_res, _get_dung_than(topic), False)
        return f"### ☯️ Luận Giải Lục Hào — Offline V8.0\n**Chủ đề:** {topic}\n\n{section}\n→ Kết luận: **{verdict}**"

    def analyze_mai_hoa(self, mai_hoa_res, topic="Chung"):
        section, verdict, _ = self._analyze_mai_hoa_full(mai_hoa_res, False)
        return f"### 🌸 Luận Giải Mai Hoa — Offline V8.0\n**Chủ đề:** {topic}\n\n{section}\n→ Kết luận: **{verdict}**"

"""
INDEX.py — V32.1 BẢN ĐỒ TOÀN BỘ HỆ THỐNG QMDG
═══════════════════════════════════════════════════
AI ĐỌC FILE NÀY ĐẦU TIÊN — Biết mọi thứ ở đâu trong < 2 giây.

Cấu trúc: REGISTRY dict chứa metadata cho TỪNG file.
    - desc: Mô tả ngắn
    - role: Vai trò (engine/data/ui/util/test)
    - key_funcs: Các hàm chính AI cần biết
    - key_data: Các biến/dict dữ liệu quan trọng
    - imports: Cách import
    - size_kb: Kích thước
    - priority: 1=luôn cần, 2=thường dùng, 3=ít dùng, 4=util/test

Lookup: REGISTRY['tên_file'] → thông tin ngay lập tức.
Tìm theo chức năng: find_module('câu hỏi') → file phù hợp.
"""

# ═══════════════════════════════════════════════════
# REGISTRY — BẢN ĐỒ TOÀN BỘ CODE
# ═══════════════════════════════════════════════════

REGISTRY = {
    # ═══════════════════════════════════════════════
    # 🧠 CORE ENGINE (AI Logic) — Priority 1-2
    # ═══════════════════════════════════════════════
    
    'free_ai_helper.py': {
        'desc': 'ENGINE CHÍNH — Xử lý câu hỏi, tính offline, gọi AI online',
        'role': 'engine',
        'size_kb': 518,
        'lines': 9154,
        'priority': 1,
        'class': 'FreeAIHelper',
        'key_funcs': [
            'answer_question(question) → str: HÀM CHÍNH — nhận câu hỏi, trả lời',
            'tinh_offline(question) → dict: Tính toán offline (Kỳ Môn, Lục Hào, Mai Hoa...)',
            'build_ai_prompt(data) → str: Tạo prompt cho AI online',
            'get_ngu_hanh_tuong() → dict: Ngũ Hành tương ứng',
            'get_bat_quai_tuong() → dict: Bát Quái tương ứng',
            'tra_kinh_dich() → dict: Tra Kinh Dịch',
        ],
        'key_data': [
            'SINH, KHAC: Dict sinh khắc ngũ hành',
            'CAN_NGU_HANH, CHI_NGU_HANH: Can Chi → Ngũ Hành',
            'SAO_CAT, SAO_HUNG: Phân loại sao',
            'TRUONG_SINH_POWER: 12 tầng trường sinh',
        ],
        'imports': 'from free_ai_helper import FreeAIHelper',
        'note': 'FILE LỚN NHẤT — Chứa toàn bộ logic. AI nên dùng find_section() để nhảy đến phần cần',
    },
    
    'gemini_helper.py': {
        'desc': 'Gọi API Gemini — Gửi prompt, nhận response, xử lý fallback',
        'role': 'engine',
        'size_kb': 169,
        'lines': 2860,
        'priority': 2,
        'class': 'GeminiQMDGHelper',
        'key_funcs': [
            'answer_question(question) → str: Gọi AI trả lời',
            'test_connection() → bool: Test API key',
            'set_n8n_url(url): Set N8N webhook',
        ],
        'imports': 'from gemini_helper import GeminiQMDGHelper',
    },
    
    'interaction_diagrams.py': {
        'desc': 'Sơ đồ tương tác — Phân loại câu hỏi, tách câu phức hợp, clean noise',
        'role': 'engine',
        'size_kb': 50,
        'lines': 902,
        'priority': 1,
        'key_funcs': [
            'match_question_to_diagram(q) → (sd_code, diagram): Phân loại câu hỏi → Sơ đồ phù hợp',
            'split_compound_question(q) → list: Tách câu hỏi ghép thành danh sách',
            'clean_question(q) → str: Loại bỏ noise, từ thừa, dấu thừa',
            'format_parsed_questions(lst) → str: Format danh sách câu hỏi',
        ],
        'key_data': [
            'DIAGRAM_MASTER: Dict tất cả sơ đồ SD0-SD20',
            'DIAGRAMS: Alias cho DIAGRAM_MASTER',
            'CUNG_PHUONG: Cung phương vị',
            'QUAI_NGUOI: Quái ↔ Người',
        ],
        'imports': 'from interaction_diagrams import match_question_to_diagram, split_compound_question, clean_question',
    },
    
    'app.py': {
        'desc': 'Streamlit UI — Giao diện web, nhập câu hỏi, hiển thị kết quả',
        'role': 'ui',
        'size_kb': 177,
        'lines': 3687,
        'priority': 2,
        'class': 'PhoenixOrchestrator',
        'imports': 'import app  # Khởi chạy: streamlit run app.py',
    },
    
    'orchestrator.py': {
        'desc': 'Điều phối AI — Pipeline xử lý từ câu hỏi → kết quả cuối',
        'role': 'engine',
        'size_kb': 13,
        'lines': 238,
        'priority': 2,
        'class': 'AIOrchestrator',
        'key_funcs': ['run_pipeline(question) → result', 'render_logs() → str'],
        'imports': 'from orchestrator import AIOrchestrator',
    },
    
    # ═══════════════════════════════════════════════
    # 📊 DATA — Dữ liệu tĩnh (Knowledge Base)
    # ═══════════════════════════════════════════════
    
    'qmdg_data.py': {
        'desc': 'DỮ LIỆU QMDG TỔNG — Bảng tra Kỳ Môn, Sao, Cửa, Thần',
        'role': 'data',
        'size_kb': 93,
        'lines': 841,
        'priority': 1,
        'key_funcs': ['load_excel_data() → dict', 'load_advanced_knowledge() → dict'],
        'key_data': ['SAO_*, CUA_*, THAN_*: Bảng tra sao/cửa/thần', 'CACH_CUC_81: 81 cách cục'],
        'imports': 'from qmdg_data import load_excel_data',
    },
    
    'kinh_dich_64_que.py': {
        'desc': '64 Quẻ Kinh Dịch — Tên, tượng, hào, ý nghĩa đầy đủ',
        'role': 'data',
        'size_kb': 44,
        'lines': 677,
        'priority': 2,
        'key_funcs': ['tra_kinh_dich(que) → dict', 'tra_nap_am(can, chi) → str', 'tra_the_dung(que) → dict'],
        'imports': 'from kinh_dich_64_que import tra_kinh_dich',
    },
    
    'luc_hao_ky_mon_rules.py': {
        'desc': 'Rules Lục Hào + Kỳ Môn — Quy tắc phân tích, tra bàn cung',
        'role': 'data',
        'size_kb': 59,
        'lines': 861,
        'priority': 2,
        'key_funcs': ['tra_ban_cung(cung) → dict'],
        'imports': 'from luc_hao_ky_mon_rules import tra_ban_cung',
    },
    
    'luc_hao_kinh_dich.py': {
        'desc': 'Lục Hào Kinh Dịch — Nạp Giáp, Ngũ Hành cho hào',
        'role': 'data',
        'size_kb': 19,
        'lines': 386,
        'priority': 2,
        'key_funcs': ['get_hex_name(lines)', 'get_nap_giap_for_hexagram(hex)', 'get_element_strength(el)'],
        'imports': 'from luc_hao_kinh_dich import get_hex_name',
    },
    
    'qmdg_knowledge_complete.py': {
        'desc': 'Tra cứu hoàn chỉnh — Cung, Sao, Môn, Thần chi tiết',
        'role': 'data',
        'size_kb': 30,
        'lines': 575,
        'priority': 2,
        'key_funcs': ['tra_cuu_cung(cung)', 'tra_cuu_sao(sao)', 'tra_cuu_mon(mon)', 'tra_cuu_than(than)'],
        'imports': 'from qmdg_knowledge_complete import tra_cuu_cung, tra_cuu_sao',
    },
    
    'qmdg_advanced_rules.py': {
        'desc': 'Rules nâng cao — Phân tích tìm đồ chi tiết',
        'role': 'data',
        'size_kb': 19,
        'lines': 336,
        'priority': 3,
        'key_funcs': ['phan_tich_tim_do_chi_tiet(data) → str'],
        'imports': 'from qmdg_advanced_rules import phan_tich_tim_do_chi_tiet',
    },
    
    'qmdg_inference_rules.py': {
        'desc': 'Rules suy luận — Tính màu sắc, giá trị, khoảng cách vật',
        'role': 'data',
        'size_kb': 16,
        'lines': 371,
        'priority': 3,
        'key_funcs': ['tinh_mau_sac_vat(hanh)', 'tinh_gia_tri_vat()', 'tinh_khoang_cach()', 'tinh_kha_nang_bi_bat()'],
        'imports': 'from qmdg_inference_rules import tinh_mau_sac_vat',
    },
    
    'iching_integrated_data.py': {
        'desc': 'Data Kinh Dịch tích hợp — Bảng tra tổng hợp',
        'role': 'data',
        'size_kb': 23,
        'lines': 410,
        'priority': 3,
        'imports': 'from iching_integrated_data import *',
    },
    
    'dai_luc_nham.py': {
        'desc': 'Đại Lục Nhâm — Tính toán Đại Lục Nhâm',
        'role': 'data',
        'size_kb': 28,
        'lines': 671,
        'priority': 3,
        'imports': 'from dai_luc_nham import *',
    },
    
    'thai_at_than_so.py': {
        'desc': 'Thái Ất Thần Số — Tính tích niên, cung, bát tướng, cách cục',
        'role': 'data',
        'size_kb': 14,
        'lines': 318,
        'priority': 3,
        'key_funcs': ['tinh_tich_nien(year)', 'tinh_thai_at_cung()', 'tinh_bat_tuong()', 'tinh_cach_cuc()'],
        'imports': 'from thai_at_than_so import tinh_tich_nien',
    },
    
    'mai_hoa_dich_so.py': {
        'desc': 'Mai Hoa Dịch Số — Tính quẻ theo thời gian hoặc ngẫu nhiên',
        'role': 'data',
        'size_kb': 9,
        'lines': 142,
        'priority': 3,
        'key_funcs': ['tinh_qua_theo_thoi_gian(dt) → dict', 'tinh_qua_ngau_nhien() → dict'],
        'imports': 'from mai_hoa_dich_so import tinh_qua_theo_thoi_gian',
    },
    
    # ═══════════════════════════════════════════════
    # 🔮 VẠN VẬT — Package riêng (Lazy-Load)
    # ═══════════════════════════════════════════════
    
    'van_vat/': {
        'desc': 'VẠN VẬT PACKAGE — 2226+ items, 25 danh mục, lazy-load theo hành',
        'role': 'data',
        'size_kb': 120,
        'priority': 1,
        'structure': {
            '__init__.py': 'INDEX + API (AI đọc file này)',
            'truong_sinh.py': '12 tầng trạng thái (dùng chung)',
            'kim.py': 'Hành Kim — CORE + EXPANDED',
            'moc.py': 'Hành Mộc — CORE + EXPANDED',
            'thuy.py': 'Hành Thủy — CORE + EXPANDED',
            'hoa.py': 'Hành Hỏa — CORE + EXPANDED',
            'tho.py': 'Hành Thổ — CORE + EXPANDED',
        },
        'key_funcs': [
            'get_van_vat_chi_tiet(hanh, ts) → dict: Lấy mô tả chi tiết',
            'format_van_vat_for_ai(hanh, ts) → str: Format cho AI đọc',
            'get_tham_tu_mo_ta(hanh, ts, q) → str: Mô tả thám tử lắp ghép',
        ],
        'imports': 'from van_vat import get_van_vat_chi_tiet, format_van_vat_for_ai, get_tham_tu_mo_ta',
    },
    
    # ═══════════════════════════════════════════════
    # 🔧 UTILITY — Công cụ hỗ trợ
    # ═══════════════════════════════════════════════
    
    'qmdg_calc.py': {
        'desc': 'Tính Can Chi, Tiết Khí — Core calculation',
        'role': 'util',
        'size_kb': 12,
        'lines': 271,
        'priority': 2,
        'key_funcs': ['get_can_chi_year(y)', 'get_can_chi_day(dt)', 'get_can_chi_hour(dt)', 'get_tiet_khi(dt)'],
        'imports': 'from qmdg_calc import get_can_chi_year, get_can_chi_day',
    },
    
    'qmdg_decoder.py': {
        'desc': 'Giải mã cụ thể — Bệnh, đồ mất, kẻ trộm...',
        'role': 'util',
        'size_kb': 10,
        'lines': 203,
        'priority': 3,
        'key_funcs': ['decode_illness(data)', 'decode_lost_item(data)', 'decode_thief(data)'],
        'imports': 'from qmdg_decoder import decode_illness',
    },
    
    'skill_library.py': {
        'desc': 'Thư viện kỹ năng — Tra cứu khái niệm',
        'role': 'util',
        'size_kb': 19,
        'lines': 336,
        'priority': 3,
        'key_funcs': ['lookup_concept(keyword) → str'],
        'imports': 'from skill_library import lookup_concept',
    },
    
    'ai_tools.py': {
        'desc': 'Công cụ AI — Lịch âm, Khổng Minh Lục Diệu',
        'role': 'util',
        'size_kb': 6,
        'lines': 149,
        'priority': 3,
        'key_funcs': ['get_khong_minh_luc_dieu(dt)', 'solar_to_lunar(y, m, d)'],
        'imports': 'from ai_tools import get_khong_minh_luc_dieu',
    },
    
    'n8n_integration.py': {
        'desc': 'N8N webhook — Tích hợp workflow automation',
        'role': 'util',
        'size_kb': 15,
        'lines': 435,
        'priority': 4,
        'class': 'N8nClient',
        'imports': 'from n8n_integration import N8nClient',
    },
    
    'blind_reading.py': {
        'desc': 'Blind Reading — Đọc quẻ không cần câu hỏi',
        'role': 'util',
        'size_kb': 13,
        'lines': 313,
        'priority': 3,
        'imports': 'from blind_reading import *',
    },
}

# ═══════════════════════════════════════════════════
# 🔍 TÌM KIẾM NHANH — AI dùng hàm này
# ═══════════════════════════════════════════════════

# Mapping từ khóa → file
_KEYWORD_MAP = {
    # Câu hỏi / Phân loại
    'cau_hoi': 'interaction_diagrams.py',
    'phan_loai': 'interaction_diagrams.py',
    'tach_cau': 'interaction_diagrams.py',
    'clean': 'interaction_diagrams.py',
    'question': 'interaction_diagrams.py',
    'so_do': 'interaction_diagrams.py',
    'diagram': 'interaction_diagrams.py',
    
    # Tính toán chính
    'answer': 'free_ai_helper.py',
    'tra_loi': 'free_ai_helper.py',
    'offline': 'free_ai_helper.py',
    'prompt': 'free_ai_helper.py',
    'engine': 'free_ai_helper.py',
    'ngu_hanh': 'free_ai_helper.py',
    'truong_sinh': 'free_ai_helper.py',
    
    # API
    'gemini': 'gemini_helper.py',
    'api': 'gemini_helper.py',
    'online': 'gemini_helper.py',
    
    # Data lookup
    'kinh_dich': 'kinh_dich_64_que.py',
    '64_que': 'kinh_dich_64_que.py',
    'que': 'kinh_dich_64_que.py',
    'luc_hao': 'luc_hao_kinh_dich.py',
    'nap_giap': 'luc_hao_kinh_dich.py',
    'sao': 'qmdg_knowledge_complete.py',
    'cua': 'qmdg_knowledge_complete.py',
    'than': 'qmdg_knowledge_complete.py',
    'cung': 'qmdg_knowledge_complete.py',
    'cach_cuc': 'qmdg_data.py',
    'ky_mon': 'luc_hao_ky_mon_rules.py',
    'mai_hoa': 'mai_hoa_dich_so.py',
    'dai_luc_nham': 'dai_luc_nham.py',
    'luc_nham': 'dai_luc_nham.py',
    'thai_at': 'thai_at_than_so.py',
    
    # Vạn vật
    'van_vat': 'van_vat/',
    'do_vat': 'van_vat/',
    'tham_tu': 'van_vat/',
    'giac_quan': 'van_vat/',
    'loai_tuong': 'van_vat/',
    
    # Giải mã
    'benh': 'qmdg_decoder.py',
    'mat_do': 'qmdg_decoder.py',
    'ke_trom': 'qmdg_decoder.py',
    'mau_sac': 'qmdg_inference_rules.py',
    'khoang_cach': 'qmdg_inference_rules.py',
    
    # Can Chi
    'can_chi': 'qmdg_calc.py',
    'tiet_khi': 'qmdg_calc.py',
    'lich_am': 'ai_tools.py',
    'luc_dieu': 'ai_tools.py',
    
    # UI
    'streamlit': 'app.py',
    'giao_dien': 'app.py',
    'ui': 'app.py',
}


def find_module(keyword):
    """Tìm file chứa chức năng theo từ khóa.
    
    Args:
        keyword: str — VD: 'kinh_dich', 'van_vat', 'benh', 'gemini'
    
    Returns: dict {file, desc, imports, key_funcs}
    """
    kw = keyword.lower().replace(' ', '_')
    
    # Exact match
    if kw in _KEYWORD_MAP:
        fname = _KEYWORD_MAP[kw]
        info = REGISTRY.get(fname, {})
        return {
            'file': fname,
            'desc': info.get('desc', ''),
            'imports': info.get('imports', ''),
            'key_funcs': info.get('key_funcs', []),
        }
    
    # Partial match
    for k, v in _KEYWORD_MAP.items():
        if kw in k or k in kw:
            info = REGISTRY.get(v, {})
            return {
                'file': v,
                'desc': info.get('desc', ''),
                'imports': info.get('imports', ''),
                'key_funcs': info.get('key_funcs', []),
            }
    
    return {'file': None, 'desc': 'Không tìm thấy', 'imports': '', 'key_funcs': []}


def get_priority_files(max_priority=2):
    """Lấy danh sách file quan trọng nhất (priority 1-2)."""
    return {k: v for k, v in REGISTRY.items() 
            if v.get('priority', 99) <= max_priority}


def get_files_by_role(role):
    """Lấy file theo vai trò: engine/data/ui/util."""
    return {k: v for k, v in REGISTRY.items() if v.get('role') == role}


# ═══════════════════════════════════════════════════
# QUICK REFERENCE — AI đọc nhanh
# ═══════════════════════════════════════════════════

FLOW_MAP = """
CÂU HỎI → interaction_diagrams.py (phân loại + clean)
       → free_ai_helper.py (tính offline: Kỳ Môn, Lục Hào, Mai Hoa...)
       → van_vat/ (tra vạn vật theo Hành + Trường Sinh)
       → gemini_helper.py (gọi AI online)
       → app.py (hiển thị kết quả)

DATA FLOW:
  qmdg_data.py → qmdg_knowledge_complete.py → free_ai_helper.py
  kinh_dich_64_que.py → luc_hao_kinh_dich.py → free_ai_helper.py
  mai_hoa_dich_so.py → free_ai_helper.py
  van_vat/ → free_ai_helper.py
"""

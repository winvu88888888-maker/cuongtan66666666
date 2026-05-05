"""
question_parser.py — V32.5 Smart Question Parser
Bộ phân tích câu hỏi thông minh 3 tầng:
  Tầng 1: SmartPreprocessor — Làm sạch noise mà KHÔNG mất nghĩa
  Tầng 2: ContextSplitter — Tách câu hỏi phức hợp dựa trên ngữ cảnh
  Tầng 3: EntityExtractor — Trích xuất WHO / WHAT / HOW / DT / DIAGRAM

Design Principles:
  1. NEVER xóa từ có nghĩa ở giữa câu
  2. Chỉ tách khi phần sau là câu hỏi MỚI (có keyword hỏi hoặc topic mới)
  3. Word-boundary matching cho các từ ngắn (ai, ba, ông, em, cô, con)
  4. Thống nhất 1 bảng Dụng Thần duy nhất (UNIFIED_DT_TABLE)
"""

import re

# ═══════════════════════════════════════════════════════════════
# UNIFIED DỤNG THẦN TABLE — Single Source of Truth
# Tất cả modules (interaction_diagrams, free_ai_helper) import từ đây
# ═══════════════════════════════════════════════════════════════

UNIFIED_PERSON_DT = {
    # CỤM TỪ DÀI → ưu tiên match trước (sort by length desc)
    'con trai': {'dt': 'Tử Tôn', 'label': 'Con trai'},
    'con gái': {'dt': 'Tử Tôn', 'label': 'Con gái'},
    'bạn trai': {'dt': 'Quan Quỷ', 'label': 'Bạn trai'},
    'bạn gái': {'dt': 'Thê Tài', 'label': 'Bạn gái'},
    'người yêu': {'dt': 'Thê Tài', 'label': 'Người yêu'},
    'anh trai': {'dt': 'Huynh Đệ', 'label': 'Anh trai'},
    'chị gái': {'dt': 'Huynh Đệ', 'label': 'Chị gái'},
    'con dâu': {'dt': 'Thê Tài', 'label': 'Con dâu'},
    'con rể': {'dt': 'Quan Quỷ', 'label': 'Con rể'},
    'ông nội': {'dt': 'Phụ Mẫu', 'label': 'Ông nội'},
    'bà nội': {'dt': 'Phụ Mẫu', 'label': 'Bà nội'},
    'ông ngoại': {'dt': 'Phụ Mẫu', 'label': 'Ông ngoại'},
    'bà ngoại': {'dt': 'Phụ Mẫu', 'label': 'Bà ngoại'},
    'đối tác': {'dt': 'Huynh Đệ', 'label': 'Đối tác'},
    'đối thủ': {'dt': 'Huynh Đệ', 'label': 'Đối thủ'},
    # TỪ ĐƠN — cần kiểm tra word boundary
    'bố': {'dt': 'Phụ Mẫu', 'label': 'Bố', 'boundary': True},
    'mẹ': {'dt': 'Phụ Mẫu', 'label': 'Mẹ', 'boundary': True},
    'cha': {'dt': 'Phụ Mẫu', 'label': 'Cha', 'boundary': True},
    'ba': {'dt': 'Phụ Mẫu', 'label': 'Ba', 'boundary': True},
    'má': {'dt': 'Phụ Mẫu', 'label': 'Má', 'boundary': True},
    'ông': {'dt': 'Phụ Mẫu', 'label': 'Ông', 'boundary': True},
    'bà': {'dt': 'Phụ Mẫu', 'label': 'Bà', 'boundary': True},
    'con': {'dt': 'Tử Tôn', 'label': 'Con', 'boundary': True},
    'cháu': {'dt': 'Tử Tôn', 'label': 'Cháu', 'boundary': True},
    'vợ': {'dt': 'Thê Tài', 'label': 'Vợ', 'boundary': True},
    'chồng': {'dt': 'Quan Quỷ', 'label': 'Chồng', 'boundary': True},
    'anh': {'dt': 'Huynh Đệ', 'label': 'Anh', 'boundary': True},
    'chị': {'dt': 'Huynh Đệ', 'label': 'Chị', 'boundary': True},
    'em': {'dt': 'Huynh Đệ', 'label': 'Em', 'boundary': True},
    'sếp': {'dt': 'Quan Quỷ', 'label': 'Sếp', 'boundary': True},
    'thầy': {'dt': 'Phụ Mẫu', 'label': 'Thầy', 'boundary': True},
    'cô': {'dt': 'Phụ Mẫu', 'label': 'Cô', 'boundary': True},
    'bạn': {'dt': 'Huynh Đệ', 'label': 'Bạn', 'boundary': True},
}

# ═══════════════════════════════════════════════════════════════
# TOPIC KEYWORDS — Sử dụng cho cả offline engine và parser
# ═══════════════════════════════════════════════════════════════

UNIFIED_TOPICS = {
    'SỨC_KHỎE': {
        'keywords': ['bệnh', 'ốm', 'đau', 'sức khỏe', 'khỏe', 'chết', 'sống',
                     'chữa', 'viện', 'phẫu thuật', 'ung thư', 'tai nạn',
                     'qua khỏi', 'cứu', 'nặng', 'nhẹ', 'thuốc', 'mổ',
                     'mang thai', 'thai', 'sinh', 'bệnh viện', 'trị bệnh',
                     'khỏi bệnh', 'nguy hiểm', 'nằm viện', 'mất người',
                     'bố mất', 'mẹ mất', 'chết chưa', 'thọ'],
        'negative_keywords': [],  # Từ loại trừ
        'default_dt': 'Bản Thân',
        'label': '🏥 Sức Khỏe',
        'diagram_fallback': ('SỨC KHỎE', 'SD8', '🏥 SỨC KHỎE'),
    },
    'TÀI_CHÍNH': {
        'keywords': ['tiền', 'tài chính', 'đầu tư', 'lương', 'thu nhập', 'nợ',
                     'vay', 'cho vay', 'kinh doanh', 'buôn bán', 'lãi', 'lỗ',
                     'cổ phiếu', 'crypto', 'bitcoin', 'nhà đất', 'mua nhà',
                     'bất động sản', 'vốn', 'hùn vốn', 'trúng số', 'tài sản',
                     'vàng', 'mua bán', 'giàu', 'nghèo'],
        'negative_keywords': [],
        'default_dt': 'Thê Tài',
        'label': '💰 Tài Chính',
        'diagram_fallback': ('TÀI LỘC', 'SD6', '💰 TÀI LỘC'),
    },
    'CÔNG_VIỆC': {
        'keywords': ['việc', 'công việc', 'sếp', 'thăng tiến', 'thăng chức',
                     'thi', 'đỗ', 'trượt', 'phỏng vấn', 'xin việc', 'nghỉ việc',
                     'hợp đồng', 'dự án', 'thầu', 'kiện', 'kiện tụng', 'tòa',
                     'quan chức', 'đề bạt', 'du học', 'học hành', 'thi cử',
                     'đại học', 'sự nghiệp', 'khởi nghiệp', 'startup',
                     'công ty', 'nhà máy', 'xưởng', 'doanh nghiệp'],
        'negative_keywords': [],
        'default_dt': 'Quan Quỷ',
        'label': '💼 Công Việc',
        'diagram_fallback': ('CÔNG VIỆC', 'SD9', '💼 CÔNG VIỆC'),
    },
    'TÌNH_CẢM': {
        'keywords': ['yêu', 'người yêu', 'vợ chồng', 'hôn nhân', 'cưới',
                     'ly hôn', 'tình', 'hẹn hò', 'chia tay', 'ngoại tình',
                     'duyên', 'đám cưới', 'bạn trai', 'bạn gái', 'tình cảm',
                     'hạnh phúc', 'ghen', 'lấy vợ', 'lấy chồng', 'kết hôn',
                     'thật lòng', 'tình yêu'],
        'negative_keywords': [],
        'default_dt': 'Thê Tài',
        'label': '❤️ Tình Cảm',
        'diagram_fallback': ('TÌNH DUYÊN', 'SD7', '❤️ TÌNH DUYÊN'),
    },
    'TÌM_ĐỒ': {
        'keywords': ['mất đồ', 'thất lạc', 'trộm', 'mất cắp',
                     'mất xe', 'mất điện thoại', 'mất tiền', 'mất ví',
                     'tìm đường', 'lạc đường', 'để đâu', 'cất đâu'],
        'negative_keywords': ['bố mất', 'mẹ mất', 'mất người', 'chết',
                              'mất mạng', 'mất tích'],
        'default_dt': 'Thê Tài',
        'label': '🔍 Tìm Đồ',
        'diagram_fallback': ('MẤT ĐỒ', 'SD11', '🔍 MẤT ĐỒ'),
    },
    'NHÀ_CỬA': {
        'keywords': ['xây nhà', 'sửa nhà', 'phong thủy', 'hướng nhà',
                     'cửa nhà', 'dọn nhà', 'chuyển nhà', 'thửa đất',
                     'lô đất', 'căn hộ', 'chung cư', 'tầng'],
        'negative_keywords': [],
        'default_dt': 'Thê Tài',
        'label': '🏠 Nhà Cửa',
        'diagram_fallback': None,
    },
    'XUẤT_HÀNH': {
        'keywords': ['du lịch', 'xuất hành', 'chuyến đi', 'di chuyển',
                     'máy bay', 'đi công tác', 'ra nước ngoài', 'đi nước ngoài',
                     'khởi hành', 'hành trình', 'về quê', 'đi xa'],
        'negative_keywords': [],
        'default_dt': 'Bản Thân',
        'label': '✈️ Xuất Hành',
        'diagram_fallback': None,
    },
}

# ═══════════════════════════════════════════════════════════════
# QUESTION TYPE PATTERNS — Loại câu hỏi → Sơ đồ tương tác
# ═══════════════════════════════════════════════════════════════

# Mỗi entry: (keywords, qtype, diagram_id, label)
# Sắp xếp theo ĐỘ ƯU TIÊN — match đầu tiên thắng
QTYPE_RULES = [
    # CÓ/KHÔNG — rất phổ biến, keywords phải SORT DÀI→NGẮN trong detect
    {
        'keywords': ['thành công không', 'thuận lợi không', 'nặng hay không',
                     'tìm được không', 'nguy hiểm không',
                     'được không', 'nên không', 'khỏi không', 'sống không',
                     'đúng không', 'phải không', 'trúng không',
                     'thắng không', 'thua không',
                     'có nên', 'có được', 'có thể', 'liệu có',
                     'có thành', 'có đỗ', 'có không', 'hay không',
                     'có tốt', 'có đậu', 'có qua', 'có lời', 'có lãi',
                     'chết chưa', 'sinh chưa'],
        'qtype': 'CÓ/KHÔNG',
        'diagram_id': 'SD1',
        'label': '❓ CÓ/KHÔNG',
        # Regex fallback: "...không" / "...không?" ở cuối câu
        'regex_extra': r'(?:đỗ|đậu|tốt|nặng|qua|khỏi|giàu|nghèo|thắng|thua|tìm|sống|chết|an toàn|thuận lợi|thành|trúng|lời|lãi|xong|được|nguy|tình)\s+không(?:\s|[?!.]|$)',
    },
    # KHI NÀO
    {
        'keywords': ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm', 'bao lâu',
                     'tháng mấy', 'năm nào', 'ngày nào', 'mấy giờ'],
        'qtype': 'KHI NÀO',
        'diagram_id': 'SD5',
        'label': '⏰ KHI NÀO',
    },
    # Ở ĐÂU
    {
        'keywords': ['ở đâu', 'hướng nào', 'phương nào', 'chỗ nào', 'để đâu',
                     'cất đâu', 'nơi nào', 'tìm đâu', 'tìm ở'],
        'qtype': 'Ở ĐÂU',
        'diagram_id': 'SD4',
        'label': '📍 Ở ĐÂU',
    },
    # TUỔI
    {
        'keywords': ['bao nhiêu tuổi', 'mấy tuổi', 'tuổi tác', 'năm sinh'],
        'qtype': 'TUỔI',
        'diagram_id': 'SD2',
        'label': '🔢 TUỔI',
    },
    # SỐ LƯỢNG
    {
        'keywords': ['bao nhiêu', 'mấy người', 'mấy cái', 'mấy con',
                     'số lượng', 'bao nhiêu tiền', 'giá bao nhiêu'],
        'qtype': 'SỐ LƯỢNG',
        'diagram_id': 'SD2',
        'label': '🔢 SỐ LƯỢNG',
    },
    # CÁI GÌ
    {
        'keywords': ['cái gì', 'loại gì', 'là gì', 'vật gì', 'nghề gì',
                     'ngành gì', 'mặt hàng gì', 'sản phẩm gì', 'buôn bán gì',
                     'kinh doanh gì', 'bệnh gì', 'lý do gì'],
        'qtype': 'CÁI GÌ',
        'diagram_id': 'SD3',
        'label': '❓ CÁI GÌ',
    },
    # TẠI SAO — trước AI vì "tại sao" > "ai"
    {
        'keywords': ['tại sao', 'vì sao', 'nguyên nhân', 'do đâu', 'lý do',
                     'tại vì', 'vì lẽ gì', 'sao lại'],
        'qtype': 'TẠI SAO',
        'diagram_id': 'SD14',
        'label': '❓ TẠI SAO',
    },
    # AI — PHẢI dùng word boundary (không match "con trAI", "ngoAI")
    {
        'keywords': ['người nào', 'là ai', 'ai vậy', 'ai đó'],
        'qtype': 'AI',
        'diagram_id': 'SD13',
        'label': '👤 AI',
        'regex_extra': r'(?:^|\s)ai(?:\s|[?!,.]|$)',  # word-boundary "ai"
    },
    # THẾ NÀO
    {
        'keywords': ['thế nào', 'như thế nào', 'ra sao', 'tình trạng',
                     'tình hình', 'tiến triển'],
        'qtype': 'THẾ NÀO',
        'diagram_id': 'SD15',
        'label': '📊 THẾ NÀO',
    },
    # CHỌN
    {
        'keywords': ['nên chọn', 'chọn cái nào', 'cái nào tốt hơn',
                     'cái nào', 'hay là', 'a hay b', 'chọn',
                     'nào tốt nhất', 'nào tốt hơn', 'nên mua',
                     'nên đi', 'bên nào', 'nào hơn'],
        'qtype': 'CHỌN',
        'diagram_id': 'SD16',
        'label': '⚖️ CHỌN',
    },
]


# ═══════════════════════════════════════════════════════════════
# TẦNG 1: SMART PREPROCESSOR
# ═══════════════════════════════════════════════════════════════

class SmartPreprocessor:
    """Làm sạch câu hỏi — chỉ xóa noise VÀ KHÔNG bao giờ mất nghĩa.
    
    Nguyên tắc vàng:
    - CỤM từ lịch sự → xóa toàn bộ cụm (không xóa từng từ)
    - Ký tự lặp (!!!, ???, ...) → rút gọn
    - Internet noise (haha, lol) → xóa
    - Từ đơn (đi, thôi, với, nha) → KHÔNG BAO GIỜ XÓA (có nghĩa!)
    """
    
    # Cụm từ lịch sự — xóa nguyên cụm (dài→ngắn)
    POLITE_PHRASES = [
        # Câu chào/kết
        'cho tôi hỏi', 'cho em hỏi', 'em muốn hỏi', 'tôi muốn hỏi',
        'mình muốn hỏi', 'xin cho hỏi', 'xin hỏi',
        'cho hỏi', 'hỏi xíu', 'hỏi chút', 'hỏi tí', 'hỏi tý',
        'cảm ơn bạn', 'cảm ơn nhiều', 'cảm ơn',
        'thank you', 'thanks', 'thank',
        'vui lòng cho biết', 'vui lòng',
        'làm ơn cho biết', 'làm ơn',
        'thưa thầy', 'thưa cô', 'dạ thưa',
    ]
    
    # Từ đệm CHỈ XÓA khi ở VỊ TRÍ CUỐI câu
    TRAILING_FILLERS = [
        'ạ', 'nhé', 'nha', 'hen', 'nhỉ', 'hả', 'á', 'vậy',
        'vậy đó', 'đấy', 'ha', 'hehe', 'hihi',
    ]
    
    # Từ đệm CHỈ XÓA khi ở VỊ TRÍ ĐẦU câu  
    LEADING_FILLERS = [
        'dạ', 'vâng', 'ừ', 'ờ', 'à',
    ]
    
    # Internet/emoji noise — xóa ở mọi vị trí
    INTERNET_NOISE = [
        'haha', 'hehe', 'hihi', 'huhu', 'hoho',
        'lol', 'lmao', 'omg', 'ok', 'okay', 'okie',
    ]
    
    # Regex patterns luôn xóa
    NOISE_PATTERNS = [
        r'\.{2,}',           # ... (2+ dots)
        r'!{2,}',            # !!! (2+ exclamation)
        # NOTE: ??? → "? " (keep single ? for splitting, not collapse all)
        r'\?{3,}',           # ???? (3+ question marks → keep as single ?)
        r'~+',               # ~~~
        r'-{3,}',            # ----
        r'_{3,}',            # ____
        r'\*{2,}',           # ****
        r'#{2,}',            # ####
        r'@\w+',             # @username
        r'https?://\S+',     # URLs
        r'\b\d{10,}\b',      # Số điện thoại dài
    ]
    
    # Ký tự lạ — xóa (giữ Unicode tiếng Việt)
    FOREIGN_CHAR_PATTERN = r'[^\w\sáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđĐ,?.!;:\'"()/-]'
    
    def clean(self, text):
        """Làm sạch câu hỏi, trả về text đã clean."""
        if not text or not text.strip():
            return ""
        
        q = text.strip()
        
        # 1. Xóa regex noise patterns
        for pattern in self.NOISE_PATTERNS:
            if '\\?' in pattern or '?' in pattern:
                # For ? patterns: replace with single ? (preserve split boundary)
                q = re.sub(pattern, '? ', q)
            else:
                q = re.sub(pattern, ' ', q)
        
        # 2. Xóa ký tự lạ
        q = re.sub(self.FOREIGN_CHAR_PATTERN, ' ', q)
        
        # 3. Xóa internet noise (word boundary, case-insensitive)
        for noise in self.INTERNET_NOISE:
            q = re.sub(r'\b' + re.escape(noise) + r'\b',
                       ' ', q, flags=re.IGNORECASE)
        
        # 4. Xóa cụm từ lịch sự (dài → ngắn, toàn bộ cụm)
        sorted_phrases = sorted(self.POLITE_PHRASES, key=len, reverse=True)
        for phrase in sorted_phrases:
            q = re.sub(r'(?:^|\s)' + re.escape(phrase) + r'(?:\s|[,?.!;:]|$)',
                       ' ', q, flags=re.IGNORECASE)
        
        # 5. Xóa LEADING fillers (chỉ ở đầu câu)
        for filler in sorted(self.LEADING_FILLERS, key=len, reverse=True):
            pattern = r'^' + re.escape(filler) + r'(?:\s|[,;:])'
            q = re.sub(pattern, '', q.strip(), flags=re.IGNORECASE)
        
        # 6. Xóa TRAILING fillers (chỉ ở cuối câu)
        for filler in sorted(self.TRAILING_FILLERS, key=len, reverse=True):
            pattern = r'(?:\s|[,;:])' + re.escape(filler) + r'$'
            q = re.sub(pattern, '', q.strip(), flags=re.IGNORECASE)
        
        # 7. Normalize whitespace
        q = re.sub(r'\s+', ' ', q).strip()
        
        # 8. Sửa dấu câu kép
        q = re.sub(r'\?+', '?', q)
        q = re.sub(r'!+', '!', q)
        q = re.sub(r',+', ',', q)
        q = re.sub(r'\.+', '.', q)
        
        # 9. Xóa dấu câu ở đầu
        q = q.lstrip(',.;:!?-_ ')
        
        # 10. Nếu quá ngắn → kiểm tra có word thật không trước khi fallback
        if len(q) < 3:
            # Check if original text has any real Vietnamese words
            _leftover_noise = {'ok', 'okay', 'okie', 'yes', 'no', 'yep', 'nope', 'uh', 'um',
                               'haha', 'hehe', 'hihi', 'huhu', 'hoho', 'lol', 'lmao', 'omg'}
            orig_words = [w for w in text.strip().split()
                          if len(w) >= 2 
                          and w.lower() not in _leftover_noise
                          and not re.match(r'^[?.!,;:\-_~#@*]+$', w)
                          and re.search(r'[áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđĐa-zA-Z]', w)]
            if not orig_words:
                return ""
            return text.strip()
        
        # 11. Kiểm tra còn từ có nghĩa không (ít nhất 1 từ >= 2 ký tự Unicode)
        # Loại bỏ các leftover noise words
        _leftover_noise = {'ok', 'okay', 'okie', 'yes', 'no', 'yep', 'nope', 'uh', 'um'}
        words = [w for w in q.split() 
                 if len(w) >= 2 
                 and w.lower() not in _leftover_noise
                 and re.search(r'[\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđĐ]', w)]
        if not words:
            return ""
        
        return q


# ═══════════════════════════════════════════════════════════════
# TẦNG 2: CONTEXT-AWARE SPLITTER
# ═══════════════════════════════════════════════════════════════

class ContextSplitter:
    """Tách câu hỏi phức hợp dựa trên ngữ cảnh, không chỉ dấu câu.
    
    Nguyên tắc:
    - Dấu ? → LUÔN tách (đây là ranh giới câu hỏi rõ ràng)
    - " và " → chỉ tách khi 2 vế có TOPIC/QTYPE KHÁC NHAU
    - ", " → chỉ tách khi phần SAU có question marker hoặc topic mới
    - Phần quá ngắn (< 5 ký tự) → KHÔNG tách, gộp vào phần trước
    """
    
    # Từ khóa báo hiệu câu hỏi MỚI
    QUESTION_MARKERS = {
        'có ', 'không', 'nào', 'nên', 'khi nào', 'bao giờ',
        'ở đâu', 'thế nào', 'ra sao', 'bao nhiêu', 'tại sao',
        'vì sao', 'đâu', 'ai ', 'mấy', 'được không', 'liệu',
        'có nên', 'có được', 'có thể', 'gì', 'cái gì', 'chưa'
    }
    
    # Từ khóa topic riêng biệt
    TOPIC_MARKERS = {
        'sức khỏe', 'tài chính', 'tình cảm', 'công việc', 'tình hình',
        'bệnh', 'tiền', 'yêu', 'việc', 'thi', 'kinh doanh', 'công ty',
        'thu nhập', 'lương', 'vợ', 'chồng', 'con', 'nhà', 'xe', 'đất'
    }
    
    # Từ nối — dùng để tách nhưng chỉ khi context khác
    CONJUNCTIONS = [
        r',\s+và\s+',     # ", và "
        r'\s+và\s+',      # " và "
        r'\s+thêm nữa\s+',
        r'\s+ngoài ra\s+',
        r'\s+còn\s+',
    ]
    
    # Từ khóa xưng hô / gọi (vocative) — "bố ơi", "mẹ ơi" → không phải câu hỏi
    VOCATIVE_PATTERNS = [
        r'^(bố|mẹ|cha|ba|má|ông|bà|anh|chị|em|thầy|cô|bạn)\s+ơi\b',
    ]
    
    def _has_question_signal(self, text):
        """Kiểm tra text có tín hiệu câu hỏi mới không."""
        q = text.lower().strip()
        if len(q) < 5:
            return False
        
        # Vocative check: "bố ơi" alone is NOT a question
        for voc in self.VOCATIVE_PATTERNS:
            if re.match(voc, q) and len(q) < 12:
                return False
        
        # Check question markers
        for marker in self.QUESTION_MARKERS:
            if marker in q:
                return True
        
        # Check topic markers
        for marker in self.TOPIC_MARKERS:
            if marker in q:
                return True
        
        return False
    
    def _segments_have_different_topics(self, seg1, seg2):
        """Kiểm tra 2 segment có topic khác nhau không."""
        topics1 = set()
        topics2 = set()
        for marker in self.TOPIC_MARKERS:
            if marker in seg1.lower():
                topics1.add(marker)
            if marker in seg2.lower():
                topics2.add(marker)
        
        # Nếu cả 2 đều có topic và khác nhau → tách
        if topics1 and topics2 and not topics1.intersection(topics2):
            return True
        return False
    
    def split(self, text):
        """Tách câu hỏi thành danh sách segments.
        
        Returns: list of str (mỗi str là 1 câu hỏi con)
        """
        if not text or len(text.strip()) < 5:
            return [text.strip()] if text and text.strip() else []
        
        q = text.strip()
        
        # ═══ BƯỚC 1: Tách theo dấu ? (luôn tách) ═══
        parts = re.split(r'\?\s*', q)
        parts = [p.strip() for p in parts if p.strip()]
        
        # ═══ BƯỚC 2: Tách theo " và " / ", " (có context check) ═══
        expanded = []
        for part in parts:
            # Thử tách theo conjunctions
            sub_candidates = [part]
            for conj in self.CONJUNCTIONS:
                new_candidates = []
                for candidate in sub_candidates:
                    splits = re.split(conj, candidate)
                    if len(splits) > 1:
                        # Kiểm tra có nên tách không
                        valid_splits = [splits[0]]
                        for i in range(1, len(splits)):
                            prev = valid_splits[-1]
                            curr = splits[i].strip()
                            
                            # Tách nếu:
                            # 1. Phần sau có tín hiệu câu hỏi mới
                            # 2. Hoặc 2 phần có topic khác nhau
                            if (self._has_question_signal(curr) or
                                self._segments_have_different_topics(prev, curr)):
                                valid_splits.append(curr)
                            else:
                                # Không tách → gộp lại
                                valid_splits[-1] = prev + ' và ' + curr
                        
                        new_candidates.extend(valid_splits)
                    else:
                        new_candidates.append(candidate)
                sub_candidates = new_candidates
            
            # Thêm dấu , splitting (chặt hơn: chỉ khi phần sau có question marker hoặc topic/dụng thần mới)
            final_subs = []
            for sub in sub_candidates:
                comma_splits = re.split(r',\s+', sub)
                if len(comma_splits) > 1:
                    merged = [comma_splits[0]]
                    for i in range(1, len(comma_splits)):
                        curr = comma_splits[i].strip()
                        prev = merged[-1]
                        
                        # V42.9.10+: Tách mạnh qua dấu phẩy nếu:
                        # 1. Có tín hiệu câu hỏi
                        # 2. Có Topic khác nhau
                        # 3. Có Dụng Thần (Person) khác nhau
                        has_signal = self._has_question_signal(curr)
                        diff_topic = self._segments_have_different_topics(prev, curr)
                        
                        p1 = set(k for k in UNIFIED_PERSON_DT if re.search(r'\b'+k+r'\b', prev.lower()))
                        p2 = set(k for k in UNIFIED_PERSON_DT if re.search(r'\b'+k+r'\b', curr.lower()))
                        diff_person = bool(p2 and not p1.intersection(p2))
                        
                        # Hoặc nếu là câu đủ dài và độc lập (có marker)
                        if (has_signal or diff_topic or diff_person) and len(curr) >= 5:
                            merged.append(curr)
                        else:
                            # Gộp lại
                            merged[-1] = merged[-1] + ', ' + curr
                    final_subs.extend(merged)
                else:
                    final_subs.append(sub)
            
            expanded.extend(final_subs)
        
        # ═══ BƯỚC 2.5: Tách câu hỏi LIÊN TIẾPP KHÔNG DẤU ═══
        # Pattern: "...không...không...không" (Việt Nam thường hỏi nhiều câu không dấu)
        # Ví dụ: "nó có tốt không giàu không nó có yêu thật lòng không"
        #       → "nó có tốt không" | "giàu không" | "nó có yêu thật lòng không"
        implicit_expanded = []
        for seg in expanded:
            # Đếm số lần "không" xuất hiện
            khong_count = len(re.findall(r'kh\u00f4ng|không', seg.lower()))
            if khong_count >= 2:
                # Tách tại mỗi ranh giới "không" + từ tiếp theo
                # "nó có tốt không giàu không có yêu thật lòng không"
                #                   ↑            ↑                      ↑
                # Split SAU mỗi "không" khi phần sau là câu hỏi mới
                parts = re.split(r'(không)', seg, flags=re.IGNORECASE)
                # parts = ['nó có tốt ', 'không', ' giàu ', 'không', ' có yêu...', 'không']
                rebuilt = []
                current = ''
                for p in parts:
                    if p.lower() == 'không':
                        current += p
                        rebuilt.append(current.strip())
                        current = ''
                    else:
                        current += p
                if current.strip():
                    # Leftover text sau "không" cuối cùng
                    if rebuilt:
                        rebuilt[-1] = rebuilt[-1] + ' ' + current.strip()
                    else:
                        rebuilt.append(current.strip())
                
                # Filter quá ngắn
                valid = [r for r in rebuilt if len(r.strip()) >= 5]
                if len(valid) >= 2:
                    implicit_expanded.extend(valid)
                else:
                    implicit_expanded.append(seg)
            else:
                # Tương tự: tách theo "chưa" pattern
                chua_count = len(re.findall(r'chưa', seg.lower()))
                if chua_count >= 2:
                    parts = re.split(r'(chưa)', seg, flags=re.IGNORECASE)
                    rebuilt = []
                    current = ''
                    for p in parts:
                        if p.lower() == 'chưa':
                            current += p
                            rebuilt.append(current.strip())
                            current = ''
                        else:
                            current += p
                    if current.strip():
                        if rebuilt:
                            rebuilt[-1] = rebuilt[-1] + ' ' + current.strip()
                        else:
                            rebuilt.append(current.strip())
                    valid = [r for r in rebuilt if len(r.strip()) >= 5]
                    if len(valid) >= 2:
                        implicit_expanded.extend(valid)
                    else:
                        implicit_expanded.append(seg)
                else:
                    implicit_expanded.append(seg)
        
        expanded = implicit_expanded
        
        # ═══ BƯỚC 3: Trim, filter, merge tiny segments ═══
        result = []
        for seg in expanded:
            seg = seg.strip().rstrip('?.,;')
            if len(seg) >= 5:  # Minimum viable question length
                result.append(seg)
            elif seg and result:
                # Too short → append to previous segment
                result[-1] = result[-1] + ', ' + seg
        
        # ═══ BƯỚC 4: Merge vocative segments ("bố ơi", "mẹ ơi") vào câu sau ═══
        if len(result) > 1:
            merged = []
            skip_next = False
            for i in range(len(result)):
                if skip_next:
                    skip_next = False
                    continue
                seg = result[i]
                is_vocative = False
                for voc in self.VOCATIVE_PATTERNS:
                    if re.match(voc, seg.lower().strip()):
                        is_vocative = True
                        break
                if is_vocative and i + 1 < len(result):
                    # Merge vocative + next
                    merged.append(seg + ', ' + result[i + 1])
                    skip_next = True
                else:
                    merged.append(seg)
            result = merged
        
        # Nếu không tách được → giữ nguyên
        if not result:
            return [q.rstrip('?.,;')]
        
        return result


# ═══════════════════════════════════════════════════════════════
# TẦNG 3: ENTITY EXTRACTOR
# ═══════════════════════════════════════════════════════════════

class EntityExtractor:
    """Trích xuất WHO / WHAT / HOW / DT / DIAGRAM cho mỗi câu hỏi con.
    
    Word-boundary matching for short Vietnamese words:
    - "ai " → KHÔNG match "con trAI", "ngoAI tình"
    - "ba " → KHÔNG match "BAo nhiêu"
    - "ông" → KHÔNG match "khÔNG"
    """
    
    # ═══════════════════════════════════════════════════════════
    # VIETNAMESE TOKENIZER — Phân tích cấu trúc tiếng Việt
    # ═══════════════════════════════════════════════════════════
    
    # Đại từ sở hữu: "X tôi" → X thuộc về tôi → đối tượng = X
    POSSESSIVE_PRONOUNS = {'tôi', 'tao', 'mình', 'ta', 'em', 'anh', 'chị',
                           'tớ', 'cậu', 'chúng tôi', 'bọn tôi'}
    
    # Đại từ chỉ định (nó, hắn, ấy) — thường đi sau person
    DEMONSTRATIVE_PRONOUNS = {'nó', 'hắn', 'ấy', 'đó', 'này', 'kia'}
    
    def _tokenize(self, text):
        """Tokenize tiếng Việt thành danh sách từ/cụm từ.
        
        Vietnamese tokenization rules:
        - Split by whitespace
        - Try to match multi-word person keywords first (greedy)
        
        Returns: list of tokens (lowercase)
        """
        words = text.lower().split()
        return words
    
    def _find_person_in_tokens(self, tokens, start=0, end=None):
        """Tìm person keyword trong danh sách tokens.
        
        Greedy: thử match cụm dài trước (con trai, bạn gái, ông ngoại...)
        rồi mới match từ đơn (bố, mẹ, vợ...).
        
        Returns: (person_label, dung_than, person_kw, match_start, match_end)
                 or (None, None, None, -1, -1)
        """
        if end is None:
            end = len(tokens)
        
        # Sort by keyword length desc (greedy: longest first)
        sorted_persons = sorted(
            UNIFIED_PERSON_DT.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for person_kw, info in sorted_persons:
            # Skip "tôi", "mình" — these are possessive pronouns, not subjects
            if person_kw in ('tôi', 'mình', 'ta', 'tao'):
                continue
            
            kw_tokens = person_kw.split()
            kw_len = len(kw_tokens)
            
            # Scan through tokens in range [start, end)
            for i in range(start, end - kw_len + 1):
                if tokens[i:i+kw_len] == kw_tokens:
                    return info['label'], info['dt'], person_kw, i, i + kw_len
        
        return None, None, None, -1, -1
    
    def detect_person(self, text, full_context=None):
        """Xác định hỏi cho ai — Phân tích cấu trúc tiếng Việt.
        
        Quy tắc ngữ pháp tiếng Việt:
        ┌─────────────────────────────────────────────────────┐
        │ "tôi"        → bản thân (skip, default)            │
        │ "bố tôi"     → bố (của tôi) → subject = BỐ        │
        │ "chị tôi"    → chị (của tôi) → subject = CHỊ       │
        │ "của bố tôi" → thuộc bố (tôi) → subject = BỐ      │
        │ "cho bố tôi" → dành cho bố → subject = BỐ          │
        │ "A của B"    → subject = A (trước "của")            │
        │ "người yêu của cháu gái chị tôi"                   │
        │   → subject = người yêu (trước "của")              │
        └─────────────────────────────────────────────────────┘
        
        Returns: (person_label, dung_than, person_keyword)
        """
        tokens = self._tokenize(text)
        if not tokens:
            return None, None, None
        
        # ═══ BƯỚC 1: Tìm "của" → phân tách subject vs possessor ═══
        # "người yêu CỦA cháu gái chị tôi" → subject = "người yêu"
        # "bệnh CỦA bố tôi" → subject ở SAU "của" = "bố"
        # "xe CỦA em tôi" → subject ở SAU "của" = "em"
        if 'của' in tokens:
            cua_idx = tokens.index('của')
            
            # Tìm person TRƯỚC "của"
            before_person = self._find_person_in_tokens(tokens, 0, cua_idx)
            if before_person[0] is not None:
                # "người yêu CỦA ..." → subject = người yêu
                return before_person[0], before_person[1], before_person[2]
            
            # Nếu trước "của" không có person → tìm SAU "của"
            # "bệnh CỦA bố tôi" → subject = bố
            after_person = self._find_person_in_tokens(tokens, cua_idx + 1)
            if after_person[0] is not None:
                return after_person[0], after_person[1], after_person[2]
        
        # ═══ BƯỚC 2: Tìm "cho/về" + person → subject ═══
        for marker in ('cho', 'về'):
            if marker in tokens:
                marker_idx = tokens.index(marker)
                after_person = self._find_person_in_tokens(tokens, marker_idx + 1)
                if after_person[0] is not None:
                    return after_person[0], after_person[1], after_person[2]
        
        # ═══ BƯỚC 3: Tìm person ở ĐẦU câu (chủ ngữ) ═══
        # "bố tôi bệnh nặng" → [bố] [tôi] → subject = bố
        # "con trai tôi thi đỗ" → [con trai] [tôi] → subject = con trai
        # Nhưng: "tôi có giàu không" → [tôi] → skip (bản thân)
        person = self._find_person_in_tokens(tokens)
        if person[0] is not None:
            return person[0], person[1], person[2]
        
        return None, None, None
    
    def detect_topic(self, text):
        """Xác định chủ đề câu hỏi.
        
        Returns: (topic_key, topic_label, default_dt)
        """
        q = text.lower()
        best_topic = 'CHUNG'
        best_score = 0
        
        # Context: phát hiện người để suppress TÌM_ĐỒ
        person_keywords = ['bố', 'mẹ', 'cha', 'ông', 'bà', 'con trai',
                           'con gái', 'vợ', 'chồng']
        has_person = any(pk in q for pk in person_keywords)
        has_location = any(lk in q for lk in ['ở đâu', 'chỗ nào', 'hướng'])
        
        for topic_key, topic_info in UNIFIED_TOPICS.items():
            score = 0
            
            # Check negative keywords first — nếu match → skip topic này
            skip = False
            for neg_kw in topic_info.get('negative_keywords', []):
                if neg_kw in q:
                    skip = True
                    break
            if skip:
                continue
            
            # Score keywords
            for kw in topic_info['keywords']:
                if kw in q:
                    score += len(kw)
            
            # TÌM_ĐỒ penalty khi có person (trừ khi hỏi ở đâu)
            if topic_key == 'TÌM_ĐỒ' and has_person and not has_location:
                score = 0
            
            # SỨC_KHỎE bonus khi có person + health context
            if topic_key == 'SỨC_KHỎE' and has_person:
                health_ctx = ['bệnh', 'ốm', 'đau', 'chết', 'sống',
                              'chữa', 'viện', 'thuốc', 'tai nạn', 'khỏe']
                if any(hk in q for hk in health_ctx):
                    score += 5
            
            if score > best_score:
                best_score = score
                best_topic = topic_key
        
        if best_topic in UNIFIED_TOPICS:
            info = UNIFIED_TOPICS[best_topic]
            return best_topic, info['label'], info['default_dt']
        
        return 'CHUNG', '❓ Tổng Quát', 'Bản Thân'
    
    def detect_question_type(self, text):
        """Xác định loại câu hỏi (CÓ/KHÔNG, KHI NÀO, Ở ĐÂU, ...).
        
        Strategy: Scan ALL rules, find BEST match (longest keyword wins).
        This prevents 'có ' from beating 'khi nào' in 'khi nào sẽ có lãi'.
        
        Returns: (qtype, diagram_id, label)
        """
        q = text.lower()
        
        best_match = None
        best_kw_len = 0
        
        for rule in QTYPE_RULES:
            # Check standard keywords — find longest match
            for kw in rule['keywords']:
                if kw in q and len(kw) > best_kw_len:
                    best_kw_len = len(kw)
                    best_match = (rule['qtype'], rule['diagram_id'], rule['label'])
            
            # Check regex_extra (cho "ai" word boundary, CÓ/KHÔNG regex)
            if 'regex_extra' in rule:
                m = re.search(rule['regex_extra'], q)
                if m:
                    match_len = len(m.group())
                    if match_len > best_kw_len:
                        best_kw_len = match_len
                        best_match = (rule['qtype'], rule['diagram_id'], rule['label'])
        
        if best_match:
            return best_match
        
        return 'CHUNG', 'SD0', '❓ TỔNG QUÁT'
    
    def extract(self, text, global_context=None):
        """Trích xuất toàn bộ entity cho 1 câu hỏi.
        
        Args:
            text: câu hỏi con
            global_context: dict từ câu hỏi gốc (để inherit person/topic)
        
        Returns: dict với keys: text, person, dung_than, topic, qtype, diagram_id, ...
        """
        ctx = global_context or {}
        
        # 1. Detect person
        person, dt_override, person_kw = self.detect_person(text)
        
        # 2. Detect topic
        topic, topic_label, topic_default_dt = self.detect_topic(text)
        
        # 3. Detect question type
        qtype, diagram_id, qtype_label = self.detect_question_type(text)
        
        # 4. Inherit context nếu thiếu
        if not person and ctx.get('person'):
            person = ctx['person']
            dt_override = ctx.get('dt_override')
            person_kw = ctx.get('person_kw')
        
        if topic == 'CHUNG' and ctx.get('topic') and ctx['topic'] != 'CHUNG':
            topic = ctx['topic']
            topic_label = ctx.get('topic_label', '❓')
            topic_default_dt = ctx.get('topic_default_dt', 'Bản Thân')
        
        # 5. Xác định Dụng Thần cuối cùng
        # Priority: person override > topic default
        final_dt = dt_override or topic_default_dt or 'Bản Thân'
        
        # 6. Diagram fallback: nếu qtype=CHUNG, thử map từ topic
        if qtype == 'CHUNG' and diagram_id == 'SD0' and topic in UNIFIED_TOPICS:
            fallback = UNIFIED_TOPICS[topic].get('diagram_fallback')
            if fallback:
                qtype, diagram_id, qtype_label = fallback
        
        return {
            'text': text,
            'person': person,
            'person_kw': person_kw,
            'dung_than': final_dt,
            'topic': topic,
            'topic_label': topic_label,
            'qtype': qtype,
            'diagram_id': diagram_id,
            'qtype_label': qtype_label,
        }


# ═══════════════════════════════════════════════════════════════
# MAIN API: parse_question()
# ═══════════════════════════════════════════════════════════════

# Singleton instances
_preprocessor = SmartPreprocessor()
_splitter = ContextSplitter()
_extractor = EntityExtractor()
_grammar = None  # Lazy init — VietnameseGrammarAnalyzer defined below


def _get_grammar():
    """Lazy singleton cho VietnameseGrammarAnalyzer (defined later in file)."""
    global _grammar
    if _grammar is None:
        _grammar = VietnameseGrammarAnalyzer()
    return _grammar


def parse_question(full_question):
    """V32.5 Smart Question Parser — API chính.
    
    Mỗi câu hỏi con được phân tích ngữ pháp RIÊNG BIỆT,
    xác định DT riêng cho từng câu.
    
    Input:  "người yêu của cháu gái chị tôi nó có tốt không giàu không
             nó có yêu thật lòng không"
    
    Output: [
        {
            'text': 'người yêu của cháu gái chị tôi nó có tốt không',
            'person': 'Người yêu', 'dung_than': 'Thê Tài',
            'topic': 'TÌNH_CẢM', 'topic_label': '❤️ Tình Cảm',
            'qtype': 'CÓ/KHÔNG', 'diagram_id': 'SD1',
            'ask_purpose': 'VỀ',
            'inquiry_focus': 'Người yêu',
            'dung_than_reason': 'Hỏi VỀ Người yêu...',
            'grammar': { ... full grammar analysis ... },
            'index': 1,
        },
        {
            'text': 'giàu không',
            'person': 'Người yêu', 'dung_than': 'Thê Tài',
            'topic': 'TÀI_CHÍNH', ...
            'ask_purpose': 'VỀ',
            'inquiry_focus': 'Người yêu',
            'index': 2,
        },
        {
            'text': 'nó có yêu thật lòng không',
            'person': 'Người yêu', 'dung_than': 'Thê Tài',
            'topic': 'TÌNH_CẢM', ...
            'ask_purpose': 'VỀ',
            'inquiry_focus': 'Người yêu',
            'index': 3,
        },
    ]
    """
    if not full_question or len(full_question.strip()) < 3:
        return []
    
    # Tầng 1: Làm sạch
    cleaned = _preprocessor.clean(full_question)
    if not cleaned or len(cleaned) < 3:
        return []
    
    # Tầng 2: Tách câu hỏi
    segments = _splitter.split(cleaned)
    if not segments:
        return []
    
    # Tầng 3: Trích xuất entities (cũ — cho topic, qtype, diagram)
    global_person, global_dt, global_person_kw = _extractor.detect_person(cleaned)
    global_topic, global_topic_label, global_topic_dt = _extractor.detect_topic(cleaned)
    
    global_context = {
        'person': global_person,
        'dt_override': global_dt,
        'person_kw': global_person_kw,
        'topic': global_topic,
        'topic_label': global_topic_label,
        'topic_default_dt': global_topic_dt,
    }
    
    # Tầng 4: Grammar analysis trên CÂU GỐC → lấy global grammar
    global_grammar = _get_grammar().analyze(cleaned)
    
    results = []
    for i, seg in enumerate(segments):
        # Entity extraction (topic, qtype, diagram)
        parsed = _extractor.extract(seg, global_context)
        parsed['index'] = i + 1
        
        # Grammar analysis cho từng câu con ← MỚI
        grammar = _get_grammar().analyze(seg)
        if grammar:
            grammar_dt = grammar['dung_than']
            entity_dt = parsed['dung_than']
            
            # Grammar DT override logic:
            # - Grammar trả về cụ thể (PERSON/THING/verb-derived) → dùng grammar
            # - Grammar trả về 'Bản Thân' (default) → giữ entity-extractor DT (topic-based)
            if grammar_dt != 'Bản Thân':
                # Grammar có kết quả cụ thể → ưu tiên grammar
                parsed['dung_than'] = grammar_dt
                parsed['dung_than_reason'] = grammar['dung_than_reason']
            else:
                # Grammar = default → giữ entity-extractor DT nếu có
                if entity_dt and entity_dt != 'Bản Thân':
                    parsed['dung_than_reason'] = f"Theo topic: {parsed.get('topic_label', '?')} → DT = {entity_dt}"
                else:
                    parsed['dung_than'] = grammar_dt
                    parsed['dung_than_reason'] = grammar['dung_than_reason']
            
            parsed['ask_purpose'] = grammar['ask_purpose']
            parsed['inquiry_focus'] = grammar['inquiry_focus']
            
            # Update person từ grammar nếu chính xác hơn 
            if grammar['subject']['type'] == 'PERSON' and grammar['subject']['label'] != 'Bản thân':
                parsed['person'] = grammar['subject']['label']
            
            parsed['grammar'] = grammar
        else:
            parsed['dung_than_reason'] = ''
            parsed['ask_purpose'] = 'CHO'
            parsed['inquiry_focus'] = parsed.get('person', 'Bản thân')
            parsed['grammar'] = None
        
        # Inherit grammar từ global nếu sub-question thiếu info
        # NHƯNG: nếu sub có "tôi/mình" → KHÔNG inherit (câu đó hỏi về BẢN THÂN)
        if grammar and grammar['subject']['type'] == 'SELF' and global_grammar:
            seg_tokens = seg.lower().split()
            has_self_pronoun = any(t in ('tôi', 'mình', 'ta', 'tao', 'tớ') for t in seg_tokens)
            
            if not has_self_pronoun and global_grammar['subject']['type'] == 'PERSON':
                # "giàu không" (không có "tôi") kế thừa "Người yêu" từ câu gốc
                parsed['person'] = global_grammar['subject']['label']
                parsed['dung_than'] = global_grammar['dung_than']
                parsed['inquiry_focus'] = global_grammar['inquiry_focus']
                parsed['ask_purpose'] = global_grammar['ask_purpose']
                parsed['dung_than_reason'] = (
                    f"Kế thừa từ câu gốc: {global_grammar['dung_than_reason']}"
                )
        
        results.append(parsed)
    
    return results


def clean_question_v2(text):
    """V32.5 Smart clean — wrapper cho SmartPreprocessor."""
    return _preprocessor.clean(text)


def format_parsed_questions_v2(parsed_list):
    """V32.5: Format kết quả phân tách thành bảng markdown."""
    if not parsed_list:
        return ""
    
    lines = []
    lines.append(f"### 📋 PHÂN TÁCH CÂU HỎI ({len(parsed_list)} câu)")
    lines.append(f"| # | Câu hỏi | Khảo sát | DT | Mục đích | Chủ đề | Loại | SĐ |")
    lines.append(f"|:--|:--------|:---------|:---|:---------|:-------|:-----|:---|")
    
    for pq in parsed_list:
        short_q = pq['text'][:30] + '...' if len(pq['text']) > 30 else pq['text']
        focus = pq.get('inquiry_focus', pq.get('person', 'Bản thân')) or 'Bản thân'
        purpose = pq.get('ask_purpose', '?')
        lines.append(
            f"| {pq['index']} | {short_q} | {focus} | {pq['dung_than']} | "
            f"Hỏi {purpose} | {pq['topic_label']} | {pq['qtype_label']} | {pq['diagram_id']} |"
        )
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# TẦNG 4: VIETNAMESE GRAMMAR ANALYZER (Bộ phân tích ngữ pháp)
# Phân tích CẤU TRÚC câu tiếng Việt:
#   - Ai hỏi? (người hỏi / asker)
#   - Hỏi về ai / cái gì? (chủ ngữ — subject)
#   - Subject là NGƯỜI hay VẬT?
#   - Hành động / trạng thái gì? (vị ngữ — predicate)
#   - Tác động lên ai / cái gì? (tân ngữ — object)
#   - Dụng Thần dựa trên quan hệ + vai trò
#   - Chủ thể bị tác động (thụ thể — patient)
# ═══════════════════════════════════════════════════════════════

# Bảng mapping VẬT → Dụng Thần
# Khi đối tượng hỏi là VẬT (không phải NGƯỜI), DT phụ thuộc vào loại vật
OBJECT_DT_MAP = {
    # ═══ PHỤ MẪU — Sinh ngã (sinh ra ta) ═══
    # Che chở, bảo vệ, bao bọc, văn thư, bề trên
    # Nhà cửa, xe cộ, quần áo (vật che chở/bao bọc)
    # Giấy tờ, văn bằng, hợp đồng, sách vở
    'nhà': 'Phụ Mẫu', 'nhà cửa': 'Phụ Mẫu', 'đất': 'Phụ Mẫu',
    'phòng': 'Phụ Mẫu', 'căn hộ': 'Phụ Mẫu', 'chung cư': 'Phụ Mẫu',
    'xe': 'Phụ Mẫu', 'xe máy': 'Phụ Mẫu', 'ô tô': 'Phụ Mẫu',
    'tàu': 'Phụ Mẫu', 'máy bay': 'Phụ Mẫu', 'thuyền': 'Phụ Mẫu',
    'quần áo': 'Phụ Mẫu', 'áo': 'Phụ Mẫu', 'nón': 'Phụ Mẫu',
    'mũ': 'Phụ Mẫu', 'ô': 'Phụ Mẫu', 'chăn': 'Phụ Mẫu',
    'giấy tờ': 'Phụ Mẫu', 'hợp đồng': 'Phụ Mẫu', 'giấy phép': 'Phụ Mẫu',
    'bằng': 'Phụ Mẫu', 'bằng cấp': 'Phụ Mẫu', 'chứng chỉ': 'Phụ Mẫu',
    'sổ': 'Phụ Mẫu', 'hồ sơ': 'Phụ Mẫu', 'đơn': 'Phụ Mẫu',
    'thư': 'Phụ Mẫu', 'tin nhắn': 'Phụ Mẫu', 'sách': 'Phụ Mẫu',
    'trường': 'Phụ Mẫu', 'bệnh viện': 'Phụ Mẫu', 'công ty': 'Phụ Mẫu',
    'tường': 'Phụ Mẫu', 'mái': 'Phụ Mẫu', 'móng': 'Phụ Mẫu',
    
    # ═══ THÊ TÀI — Ngã khắc (ta khắc chế) ═══
    # Tiền bạc, tài sản có giá trị, vật ta sở hữu/chi phối
    # Vợ (nam mệnh), nhân viên, gia súc
    'tiền': 'Thê Tài', 'vàng': 'Thê Tài', 'bạc': 'Thê Tài',
    'tài sản': 'Thê Tài', 'của cải': 'Thê Tài', 'vốn': 'Thê Tài',
    'lương': 'Thê Tài', 'nợ': 'Thê Tài', 'lãi': 'Thê Tài',
    'cổ phiếu': 'Thê Tài', 'crypto': 'Thê Tài', 'bitcoin': 'Thê Tài',
    'ví': 'Thê Tài', 'đồng hồ': 'Thê Tài', 'trang sức': 'Thê Tài',
    'hàng': 'Thê Tài', 'hàng hóa': 'Thê Tài', 'sản phẩm': 'Thê Tài',
    'điện thoại': 'Thê Tài', 'máy tính': 'Thê Tài', 'laptop': 'Thê Tài',
    'túi': 'Thê Tài', 'đồ quý': 'Thê Tài', 'kim cương': 'Thê Tài',
    'nhà đất': 'Thê Tài',  # Khi hỏi GIÁ TRỊ/MUA BÁN (context tài chính)
    'cửa hàng': 'Thê Tài',
    
    # ═══ QUAN QUỶ — Khắc ngã (khắc chế ta) ═══
    # Công việc, chức vụ, bệnh tật, tai ương, kiện tụng
    # Sếp, chính quyền, trộm cướp
    'việc': 'Quan Quỷ', 'công việc': 'Quan Quỷ', 'chức': 'Quan Quỷ',
    'dự án': 'Quan Quỷ', 'kiện': 'Quan Quỷ', 'tòa': 'Quan Quỷ',
    'vụ': 'Quan Quỷ', 'thầu': 'Quan Quỷ', 'quan': 'Quan Quỷ',
    'bệnh': 'Quan Quỷ', 'ung thư': 'Quan Quỷ', 'tai nạn': 'Quan Quỷ',
    'dịch': 'Quan Quỷ', 'phẫu thuật': 'Quan Quỷ', 'đau': 'Quan Quỷ',
    'quy hoạch': 'Quan Quỷ', 'pháp lý': 'Quan Quỷ',
    
    # ═══ TỬ TÔN — Ngã sinh (ta sinh ra) ═══
    # Con cái, phúc đức, thuốc men, bác sĩ, thú cưng
    # Niềm vui, giải trí, hóa giải tai họa
    'thuốc': 'Tử Tôn', 'bác sĩ': 'Tử Tôn',
    'thú cưng': 'Tử Tôn', 'chó': 'Tử Tôn', 'mèo': 'Tử Tôn',
    'cá': 'Tử Tôn', 'gia súc': 'Tử Tôn', 'gia cầm': 'Tử Tôn',
    'thức ăn': 'Tử Tôn', 'đồ chơi': 'Tử Tôn',
    
    # ═══ HUYNH ĐỆ — Tỷ hòa (ngang hàng) ═══
    # Cạnh tranh, chia sẻ, hao tán, chi phí sửa chữa
    'chi phí': 'Huynh Đệ', 'phí': 'Huynh Đệ',
}

# Bảng ĐẠI TỪ nhân xưng — phân biệt ngôi
PRONOUN_MAP = {
    # Ngôi 1: người hỏi
    'tôi': 'ngoi_1', 'tao': 'ngoi_1', 'mình': 'ngoi_1',
    'ta': 'ngoi_1', 'tớ': 'ngoi_1',
    'em': 'ngoi_1_or_3',  # "em" có thể là ngôi 1 (em hỏi) hoặc ngôi 3 (em tôi)
    'con': 'ngoi_1_or_3', # "con" có thể là ngôi 1 (con hỏi bố) hoặc ngôi 3 (con tôi)
    
    # Ngôi 2: người được hỏi (ít dùng trong bói)
    'bạn': 'ngoi_2_or_3',
    
    # Ngôi 3: đối tượng hỏi
    'nó': 'ngoi_3', 'hắn': 'ngoi_3', 'ảnh': 'ngoi_3',
    'chị ấy': 'ngoi_3', 'anh ấy': 'ngoi_3', 'cô ấy': 'ngoi_3',
}

# Từ chỉ hành động / trạng thái (Vietnamese Verb patterns)
VERB_PATTERNS = {
    # Trạng thái sức khỏe
    'bệnh': 'health', 'ốm': 'health', 'đau': 'health', 'chết': 'health',
    'sống': 'health', 'khỏe': 'health', 'mổ': 'health', 'sinh': 'health',
    'mang thai': 'health', 'qua khỏi': 'health',
    
    # Hành động tài chính
    'mua': 'finance', 'bán': 'finance', 'vay': 'finance', 'trả': 'finance',
    'đầu tư': 'finance', 'kinh doanh': 'finance', 'lời': 'finance', 'lỗ': 'finance',
    'giàu': 'finance', 'nghèo': 'finance', 'lãi': 'finance',
    'buôn bán': 'finance', 'hùn vốn': 'finance',
    
    # Hành động tình cảm
    'yêu': 'love', 'cưới': 'love', 'chia tay': 'love', 'ly hôn': 'love',
    'ngoại tình': 'love', 'hẹn hò': 'love', 'thật lòng': 'love',
    
    # Hành động công việc
    'thi': 'work', 'đỗ': 'work', 'trượt': 'work', 'xin việc': 'work',
    'thăng chức': 'work', 'sa thải': 'work', 'phỏng vấn': 'work',
    'học': 'work', 'giỏi': 'work', 'dốt': 'work',
    
    # Hành động di chuyển
    'đi': 'move', 'về': 'move', 'đến': 'move', 'chuyển': 'move',
    
    # Hành động tìm kiếm
    'mất': 'find', 'tìm': 'find', 'trộm': 'find', 'lấy cắp': 'find',
}


class VietnameseGrammarAnalyzer:
    """Bộ phân tích cấu trúc ngữ pháp tiếng Việt cho câu hỏi.
    
    Cấu trúc câu tiếng Việt:
    ┌─────────────────────────────────────────────────────────────┐
    │     [Người hỏi]  +  [Chủ ngữ]  +  [Vị ngữ]  +  [Tân ngữ] │
    │     (asker)         (subject)     (predicate)   (object)    │
    │                                                             │
    │ VD: (tôi hỏi)   bố tôi       bệnh nặng     không?        │
    │     (tôi hỏi)   xe của chị   mất           ở đâu?         │
    │     (tôi hỏi)   người yêu    có tốt        không?         │
    │                  của cháu gái                               │
    │                  chị tôi                                    │
    └─────────────────────────────────────────────────────────────┘
    
    Quy tắc xác định Dụng Thần:
    1. Subject = NGƯỜI → DT dựa trên MỐI QUAN HỆ với người hỏi
       - Bố/Mẹ/Thầy/Cô → Phụ Mẫu
       - Vợ/Người yêu → Thê Tài
       - Con/Cháu → Tử Tôn
       - Anh/Chị/Em/Bạn → Huynh Đệ
       - Sếp/Chồng → Quan Quỷ
    
    2. Subject = VẬT → DT dựa trên LOẠI VẬT
       - Tiền/xe/nhà → Thê Tài
       - Bệnh/kiện → Quan Quỷ
       - Thuốc/thú cưng → Tử Tôn
       - Giấy tờ/bằng cấp → Phụ Mẫu
    
    3. Subject = BẢN THÂN → DT dựa trên CHỦ ĐỀ HỎI
       - Hỏi sức khỏe → Thế (bản thân)
       - Hỏi tiền bạc → Thê Tài
       - Hỏi công việc → Quan Quỷ
    """
    
    def _tokenize(self, text):
        """Tokenize câu thành danh sách từ."""
        return text.lower().split()
    
    def _find_person_tokens(self, tokens, start=0, end=None):
        """Tìm person keyword trong tokens. Returns (label, dt, kw, pos_start, pos_end)."""
        if end is None:
            end = len(tokens)
        
        sorted_persons = sorted(
            UNIFIED_PERSON_DT.items(),
            key=lambda x: len(x[0].split()),
            reverse=True
        )
        
        for person_kw, info in sorted_persons:
            if person_kw in ('tôi', 'mình', 'ta', 'tao'):
                continue
            kw_tokens = person_kw.split()
            kw_len = len(kw_tokens)
            for i in range(start, end - kw_len + 1):
                if tokens[i:i+kw_len] == kw_tokens:
                    return info['label'], info['dt'], person_kw, i, i + kw_len
        
        return None, None, None, -1, -1
    
    def _find_object_tokens(self, tokens, start=0, end=None):
        """Tìm object keyword (VẬT) trong tokens."""
        if end is None:
            end = len(tokens)
        
        # Sort by length desc (greedy)
        sorted_objects = sorted(OBJECT_DT_MAP.items(), key=lambda x: len(x[0].split()), reverse=True)
        
        for obj_kw, dt in sorted_objects:
            kw_tokens = obj_kw.split()
            kw_len = len(kw_tokens)
            for i in range(start, end - kw_len + 1):
                if tokens[i:i+kw_len] == kw_tokens:
                    return obj_kw, dt, i, i + kw_len
        
        return None, None, -1, -1
    
    def _find_verb(self, tokens):
        """Tìm vị ngữ (verb/predicate) trong tokens."""
        sorted_verbs = sorted(VERB_PATTERNS.items(), key=lambda x: len(x[0].split()), reverse=True)
        
        for verb_kw, category in sorted_verbs:
            kw_tokens = verb_kw.split()
            kw_len = len(kw_tokens)
            for i in range(len(tokens) - kw_len + 1):
                if tokens[i:i+kw_len] == kw_tokens:
                    return verb_kw, category, i, i + kw_len
        
        return None, None, -1, -1
    
    def _detect_asker(self, tokens):
        """Xác định người hỏi (ngôi 1).
        
        Quy tắc:
        - "tôi" đứng ĐẦU CÂU hoặc đứng MỘT MÌNH → ngôi 1 (bản thân)
        - "tôi" đứng SAU person keyword → sở hữu (bố TÔI = bố của tôi)
        """
        # Mặc định: người hỏi là "tôi" (bản thân)
        asker = 'Bản thân'
        asker_pronoun = None
        
        for i, token in enumerate(tokens):
            if token in ('tôi', 'mình', 'tao', 'ta', 'tớ'):
                # Kiểm tra: tôi đứng sau person keyword → sở hữu, không phải asker
                if i > 0:
                    # Kiểm tra trước "tôi" có person keyword không
                    prev_check = self._find_person_tokens(tokens, 0, i + 1)
                    if prev_check[0] is not None and prev_check[4] == i:
                        # "bố [tôi]" → bố = person, tôi = sở hữu
                        continue
                
                asker = 'Bản thân'
                asker_pronoun = token
                break
        
        return asker, asker_pronoun
    
    def _detect_subject(self, tokens):
        """Xác định chủ ngữ (subject) — đối tượng được hỏi.
        
        Trả về:
          - subject_type: 'PERSON' hoặc 'THING' hoặc 'SELF'
          - subject_label: tên subject
          - subject_dt: Dụng Thần tương ứng
          - subject_relationship: mối quan hệ với người hỏi
        
        Quy tắc tiếng Việt:
        ┌──────────────────────────────────────────────────────┐
        │ Pattern              │ Subject     │ Type            │
        ├──────────────────────┼─────────────┼─────────────────┤
        │ "bố tôi bệnh"       │ bố          │ PERSON          │
        │ "xe của chị mất"     │ xe          │ THING (chị=owner)│
        │ "tôi có giàu"       │ tôi         │ SELF            │
        │ "bệnh của bố nặng"  │ bệnh        │ THING (bố=owner)│
        │ "con trai thi đỗ"   │ con trai    │ PERSON          │
        │ "người yêu có tốt"  │ người yêu   │ PERSON          │
        └──────────────────────────────────────────────────────┘
        """
        result = {
            'type': 'SELF',       # PERSON / THING / SELF
            'label': 'Bản thân',
            'dt': 'Bản Thân',
            'relationship': None,
            'owner': None,        # Người sở hữu (nếu subject là VẬT)
            'owner_dt': None,
        }
        
        # ═══ Bước 1: Xử lý "của" — phân tách chủ sở hữu ═══
        if 'của' in tokens:
            cua_idx = tokens.index('của')
            
            # Tìm person TRƯỚC "của"
            before_person = self._find_person_tokens(tokens, 0, cua_idx)
            
            if before_person[0] is not None:
                # "người yêu CỦA cháu gái" → subject = người yêu
                result['type'] = 'PERSON'
                result['label'] = before_person[0]
                result['dt'] = before_person[1]
                result['relationship'] = before_person[2]
                
                # Tìm owner SAU "của" 
                after_person = self._find_person_tokens(tokens, cua_idx + 1)
                if after_person[0]:
                    result['owner'] = after_person[0]
                    result['owner_dt'] = after_person[1]
                return result
            
            # Tìm object TRƯỚC "của" (VẬT)
            before_obj = self._find_object_tokens(tokens, 0, cua_idx)
            if before_obj[0] is not None:
                # "xe CỦA chị tôi" → subject = xe (THING), owner = chị
                result['type'] = 'THING'
                result['label'] = before_obj[0]
                result['dt'] = before_obj[1]
                
                after_person = self._find_person_tokens(tokens, cua_idx + 1)
                if after_person[0]:
                    result['owner'] = after_person[0]
                    result['owner_dt'] = after_person[1]
                return result
            
            # Không tìm được trước "của" → tìm SAU "của"
            after_person = self._find_person_tokens(tokens, cua_idx + 1)
            if after_person[0] is not None:
                # "bệnh CỦA bố tôi" → subject = bệnh (THING), owner = bố
                # Tìm object TRƯỚC "của"
                before_text = ' '.join(tokens[:cua_idx])
                for obj_kw, dt in sorted(OBJECT_DT_MAP.items(), key=lambda x: len(x[0]), reverse=True):
                    if obj_kw in before_text:
                        result['type'] = 'THING'
                        result['label'] = obj_kw
                        result['dt'] = dt
                        result['owner'] = after_person[0]
                        result['owner_dt'] = after_person[1]
                        return result
                
                # Không tìm thấy vật → owner chính là subject
                result['type'] = 'PERSON'
                result['label'] = after_person[0]
                result['dt'] = after_person[1]
                result['relationship'] = after_person[2]
                return result
        
        # ═══ Bước 2: Tìm person keyword (không có "của") ═══
        person = self._find_person_tokens(tokens)
        if person[0] is not None:
            result['type'] = 'PERSON'
            result['label'] = person[0]
            result['dt'] = person[1]
            result['relationship'] = person[2]
            return result
        
        # ═══ Bước 3: Kiểm tra "tôi" ở đầu câu → SELF (uu tiên trước VẬT) ═══
        # "tôi bệnh nặng không" → SELF (đừng nhầm "bệnh" là THING)
        if tokens and tokens[0] in ('tôi', 'mình', 'ta', 'tao', 'tớ'):
            result['type'] = 'SELF'
            result['label'] = 'Bản thân'
            result['dt'] = 'Bản Thân'
            return result
        
        # ═══ Bước 4: Tìm object keyword (VẬT) ═══
        obj = self._find_object_tokens(tokens)
        if obj[0] is not None:
            result['type'] = 'THING'
            result['label'] = obj[0]
            result['dt'] = obj[1]
            return result
        
        return result
    
    def analyze(self, text):
        """Phân tích toàn diện cấu trúc câu tiếng Việt.
        
        Returns dict:
        {
            'original': 'bố tôi bệnh nặng hay không',
            'asker': 'Bản thân',              # Ai hỏi
            'subject': {
                'type': 'PERSON',              # PERSON / THING / SELF
                'label': 'Bố',                # Tên subject
                'dt': 'Phụ Mẫu',              # Dụng Thần
                'relationship': 'bố',          # Quan hệ với người hỏi
                'owner': None,                 # Chủ sở hữu (nếu VẬT)
                'owner_dt': None,
            },
            'predicate': {
                'verb': 'bệnh',               # Hành động / trạng thái
                'category': 'health',          # Phân loại vị ngữ
            },
            'object': {                        # Tân ngữ (nếu có)
                'label': None,
                'dt': None,
            },
            'dung_than': 'Phụ Mẫu',           # DT cuối cùng
            'dung_than_reason': 'Hỏi cho BỐ (Phụ Mẫu)',
        }
        """
        tokens = self._tokenize(text)
        if not tokens:
            return None
        
        # 1. Người hỏi
        asker, asker_pronoun = self._detect_asker(tokens)
        
        # 2. Chủ ngữ (subject)
        subject = self._detect_subject(tokens)
        
        # 3. Vị ngữ (predicate)
        verb, verb_cat, v_start, v_end = self._find_verb(tokens)
        predicate = {'verb': verb, 'category': verb_cat}
        
        # 4. Tân ngữ (object) — tìm VẬT sau vị ngữ
        obj_label, obj_dt = None, None
        if v_end > 0:
            obj = self._find_object_tokens(tokens, v_end)
            if obj[0]:
                obj_label, obj_dt = obj[0], obj[1]
        
        # 5. Xác định Dụng Thần cuối cùng + lý do + mục đích
        final_dt, dt_reason, ask_purpose = self._determine_dung_than(
            subject, predicate, obj_label, obj_dt, tokens
        )
        
        # 6. Inquiry focus: đối tượng chính bị khảo sát
        if subject['type'] == 'PERSON':
            inquiry_focus = subject['label']
        elif subject['type'] == 'THING':
            inquiry_focus = subject['label']
        else:
            inquiry_focus = 'Bản thân'
        
        return {
            'original': text,
            'asker': asker,
            'subject': subject,
            'predicate': predicate,
            'object': {'label': obj_label, 'dt': obj_dt},
            'dung_than': final_dt,
            'dung_than_reason': dt_reason,
            'ask_purpose': ask_purpose,
            'inquiry_focus': inquiry_focus,
        }
    
    def _determine_dung_than(self, subject, predicate, obj_label, obj_dt, tokens):
        """Xác định Dụng Thần cuối cùng dựa trên TOÀN BỘ cấu trúc câu.
        
        Quy tắc cốt lõi:
        ┌──────────────────────────────────────────────────────────────┐
        │ DT luôn tập trung vào ĐỐI TƯỢNG ĐƯỢC KHẢO SÁT             │
        │                                                              │
        │ "người yêu của cháu gái có tốt không"                       │
        │  → Đối tượng khảo sát = NGƯỜI YÊU (không phải cháu gái)    │
        │  → DT = Thê Tài (vì người yêu = Thê Tài trong Lục Hào)    │
        │  → Mục đích: Hỏi VỀ người yêu NHƯ THẾ NÀO                 │
        │                                                              │
        │ "bố tôi bệnh nặng không"                                    │
        │  → Đối tượng khảo sát = BỐ                                  │
        │  → DT = Phụ Mẫu (bố = Phụ Mẫu)                            │
        │  → Mục đích: Hỏi CHO bố (sức khỏe bố)                     │
        └──────────────────────────────────────────────────────────────┘
        
        Phân biệt:
        - "Hỏi CHO": hỏi vì lợi ích / tình trạng của người đó  
          (bố bệnh, con thi đỗ, vợ sinh chưa)
        - "Hỏi VỀ": hỏi để ĐÁNH GIÁ phẩm chất / tính cách người đó
          (người yêu có tốt không, đối tác tin được không, nó thật lòng không)
        """
        # === Xác định mục đích: HỎI CHO vs HỎI VỀ ===
        ask_about_keywords = ['tốt', 'xấu', 'tốt không', 'thật lòng', 'tin',
                              'tin cậy', 'trung thành', 'tử tế', 'đàng hoàng',
                              'giàu', 'nghèo', 'như nào', 'thế nào', 'ra sao',
                              'giỏi', 'dốt', 'đẹp', 'xấu trai', 'đẹp trai',
                              'có tốt', 'có giàu', 'có yêu']
        
        text_lower = ' '.join(tokens)
        is_asking_about = any(kw in text_lower for kw in ask_about_keywords)
        ask_purpose = 'VỀ' if is_asking_about else 'CHO'
        
        if subject['type'] == 'PERSON':
            dt = subject['dt']
            label = subject['label']
            
            if ask_purpose == 'VỀ':
                reason = f"Hỏi VỀ {label} như thế nào → DT tập trung vào {label} ({dt})"
            else:
                reason = f"Hỏi CHO {label} → DT = {dt}"
            
            # Thêm chuỗi sở hữu nếu có
            if subject.get('owner'):
                reason += f"\n      ↳ {label} thuộc về {subject['owner']} ({subject['owner_dt']})"
                reason += f"\n      ↳ DT hào = {dt} — khảo sát hào {dt} trong quẻ"
            
            return dt, reason, ask_purpose
        
        elif subject['type'] == 'THING':
            dt = subject['dt']
            reason = f"Hỏi về VẬT: {subject['label']} → DT = {dt}"
            if subject.get('owner'):
                reason += f"\n      ↳ {subject['label']} của {subject['owner']} ({subject['owner_dt']})"
            return dt, reason, ask_purpose
        
        else:  # SELF
            if predicate.get('category') == 'health':
                return 'Bản Thân', "Hỏi sức khỏe bản thân → xem hào Thế", 'CHO'
            elif predicate.get('category') == 'finance':
                return 'Thê Tài', "Hỏi tài chính bản thân → DT = Thê Tài", 'CHO'
            elif predicate.get('category') == 'love':
                return 'Thê Tài', "Hỏi tình cảm bản thân → DT = Thê Tài", 'CHO'
            elif predicate.get('category') == 'work':
                return 'Quan Quỷ', "Hỏi công việc bản thân → DT = Quan Quỷ", 'CHO'
            elif obj_dt:
                return obj_dt, f"Hỏi về {obj_label} → DT = {obj_dt}", 'VỀ'
            else:
                return 'Bản Thân', "Hỏi chung → xem hào Thế (Bản Thân)", 'CHO'




def analyze_question(text):
    """Phân tích ngữ pháp câu hỏi tiếng Việt.
    
    Returns: dict với đầy đủ thông tin ngữ pháp.
    """
    return _get_grammar().analyze(text)


def format_grammar_analysis(analysis):
    """Format kết quả phân tích ngữ pháp thành bảng đẹp."""
    if not analysis:
        return ""
    
    s = analysis['subject']
    p = analysis['predicate']
    o = analysis['object']
    purpose = analysis.get('ask_purpose', '?')
    focus = analysis.get('inquiry_focus', s['label'])
    
    lines = [
        f"### 🔬 PHÂN TÍCH NGỮ PHÁP",
        f"```",
        f"📝 Câu gốc:    {analysis['original']}",
        f"",
        f"👤 Người hỏi:   {analysis['asker']}",
        f"🎯 Đối tượng:   {s['label']} ({s['type']})",
    ]
    
    if s['type'] == 'PERSON':
        lines.append(f"   └─ Quan hệ:  {s.get('relationship', '-')}")
    if s.get('owner'):
        chain = f"{s['label']} → của {s['owner']}"
        if s.get('owner_dt'):
            chain += f" ({s['owner_dt']})"
        lines.append(f"   └─ Chuỗi:    {chain}")
    
    lines.append(f"📊 Vị ngữ:      {p.get('verb', '-')} [{p.get('category', '-')}]")
    
    if o.get('label'):
        lines.append(f"📦 Tân ngữ:     {o['label']} ({o['dt']})")
    
    lines.append(f"🔎 Mục đích:    Hỏi {purpose} {focus}")
    
    lines.extend([
        f"",
        f"⭐ DỤNG THẦN:   {analysis['dung_than']}",
        f"   └─ Lý do:    {analysis['dung_than_reason']}",
        f"```",
    ])
    
    return "\n".join(lines)



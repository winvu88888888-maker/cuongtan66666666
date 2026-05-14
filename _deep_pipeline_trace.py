# -*- coding: utf-8 -*-
"""DEEP PIPELINE TRACE — Trace chính xác DT + Category + Scoring cho câu hỏi thực"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import FreeAIHelper, _get_dung_than, v32_parse_question

helper = FreeAIHelper()

TEST_CASES = [
    "nam nay co nen dau tu kinh doanh khong",
    "toi co mua duoc nha khong",
    "me toi benh co khoi khong",
    "nam nay lam an co phat tai khong",
    "bao gio toi co nguoi yeu",
    "nam nay co nen chuyen viec khong",
]

# Simulate the full answer_question pipeline to capture DT + Category
for q in TEST_CASES:
    print(f"\n{'='*80}")
    print(f"📋 Q: {q}")
    print(f"{'='*80}")
    
    # Step 1: _get_dung_than (standalone)
    dt_standalone = _get_dung_than(q)
    print(f"  🔍 _get_dung_than (standalone): {dt_standalone}")
    
    # Step 2: Simulate answer_question category detection
    q_lower = q.lower()
    
    # Normalize (same as in answer_question)
    _VN_NO_DIAC_MAP = {
        'me toi': 'mẹ tôi', 'bo toi': 'bố tôi', 'cha toi': 'cha tôi',
        'vo toi': 'vợ tôi', 'chong toi': 'chồng tôi', 'con toi': 'con tôi',
        'nguoi yeu': 'người yêu', 'ban trai': 'bạn trai', 'ban gai': 'bạn gái',
        'di xa': 'đi xa', 'du lich': 'du lịch', 'mat do': 'mất đồ',
        'mua nha': 'mua nhà', 'ban nha': 'bán nhà', 'xay nha': 'xây nhà',
        'mua xe': 'mua xe', 'ban xe': 'bán xe', 'mua dat': 'mua đất',
        'kinh doanh': 'kinh doanh', 'dau tu': 'đầu tư',
        'tang luong': 'tăng lương', 'thang tien': 'thăng tiến',
        'suc khoe': 'sức khỏe', 'benh': 'bệnh', 'chua benh': 'chữa bệnh',
        'kien tung': 'kiện tụng', 'thuan loi': 'thuận lợi', 'nam nay': 'năm nay',
        'me': 'mẹ', 'bo': 'bố', 'cha': 'cha', 'vo': 'vợ', 'chong': 'chồng',
        'phat tai': 'phát tài', 'lam an': 'làm ăn', 'chuyen viec': 'chuyển việc',
    }
    
    q_norm = q_lower
    for nk, ck in sorted(_VN_NO_DIAC_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        if nk in q_norm:
            q_norm = q_norm.replace(nk, ck)
    print(f"  📝 q_normalized: {q_norm}")
    
    # Step 3: Category detection (replicate logic from answer_question)
    CATEGORIES_KEYWORDS = {
        'TÀI_CHÍNH': ['đầu tư', 'cổ phiếu', 'chứng khoán', 'lãi suất', 'kinh doanh',
                       'mua bán', 'buôn bán', 'tiền bạc', 'tài chính', 'phát tài', 'làm ăn',
                       'thu nhập', 'tăng lương', 'ngoại tệ', 'crypto', 'coin', 'bitcoin',
                       'vay', 'nợ', 'lãi', 'lời', 'lỗ', 'vốn', 'lương'],
        'TÌNH_CẢM': ['tình duyên', 'người yêu', 'kết hôn', 'ly hôn', 'hôn nhân', 'ngoại tình',
                      'chia tay', 'cưới', 'yêu', 'bạn gái', 'bạn trai', 'duyên', 'tình yêu'],
        'CÔNG_VIỆC': ['thăng chức', 'xin việc', 'chuyển việc', 'nghề', 'sự nghiệp', 'công việc',
                       'đối tác', 'hợp tác', 'làm ăn', 'start up'],
        'SỨC_KHỎE': ['bệnh', 'ốm', 'đau', 'sức khỏe', 'chữa bệnh', 'thuốc', 'viện',
                      'phẫu thuật', 'ung thư', 'tai nạn'],
        'NHÀ_CỬA': ['nhà', 'căn hộ', 'chung cư', 'bất động sản', 'nhà đất', 'mua nhà',
                     'bán nhà', 'xây nhà', 'sửa nhà', 'thuê nhà', 'mua đất'],
        'XUẤT_HÀNH': ['về quê', 'đi xa', 'du lịch', 'xuất hành', 'đi chơi'],
        'CHUNG': ['năm nay', 'tháng này', 'may mắn', 'tuổi'],
    }
    
    detected_cat = 'CHUNG'
    max_score = 0
    for cat_key, kws in CATEGORIES_KEYWORDS.items():
        score = 0
        matched_kws = []
        for kw in kws:
            if kw in q_norm:
                score += len(kw)
                matched_kws.append(kw)
        if score > max_score:
            max_score = score
            detected_cat = cat_key
        if matched_kws:
            print(f"  📂 {cat_key}: score={score} matched={matched_kws}")
    
    print(f"  🏷️  DETECTED CATEGORY: {detected_cat} (score={max_score})")
    
    # Step 4: Person detection
    import re
    PERSON_DT_MAP = {
        "bố mẹ": "Phụ Mẫu", "cha mẹ": "Phụ Mẫu",
        "bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu", "cha": "Phụ Mẫu",
        "vợ": "Thê Tài", "chồng": "Quan Quỷ",
        "con": "Tử Tôn", "anh": "Huynh Đệ", "chị": "Huynh Đệ", "em": "Huynh Đệ",
        "sếp": "Quan Quỷ",
    }
    _person_items = sorted(PERSON_DT_MAP.items(), key=lambda x: len(x[0]), reverse=True)
    _detected_person = None
    _person_dt = None
    for pk, pd in _person_items:
        pat = r'(?:^|[\s,;.!?])' + re.escape(pk) + r'(?:[\s,;.!?]|$)'
        if re.search(pat, q_norm):
            _detected_person = pk
            _person_dt = pd
            break
    
    # Step 5: Final DT assignment (replicate logic)
    CAT_DT = {
        'TÀI_CHÍNH': 'Thê Tài',
        'TÌNH_CẢM': 'Thê Tài',
        'CÔNG_VIỆC': 'Quan Quỷ',
        'SỨC_KHỎE': 'Quan Quỷ',
        'NHÀ_CỬA': 'Phụ Mẫu',
        'XUẤT_HÀNH': 'Bản Thân',
        'CHUNG': 'Bản Thân',
    }
    
    if _person_dt:
        final_dt = _person_dt
        dt_source = f"PERSON ({_detected_person})"
    elif 'tôi' in q_norm and detected_cat in ('CHUNG', 'SỨC_KHỎE'):
        final_dt = 'Bản Thân'
        dt_source = "tôi + CHUNG/SỨC_KHỎE"
    else:
        final_dt = CAT_DT.get(detected_cat, 'Bản Thân')
        dt_source = f"CATEGORY ({detected_cat})"
    
    print(f"  👤 Person detected: {_detected_person} → DT: {_person_dt}")
    print(f"  🎯 FINAL DT: {final_dt} (source: {dt_source})")
    
    # Check: does answer_question use the q_lower (NOT NORMALIZED) for category?
    # This could be the bug — q_lower doesn't have diacritics!
    print(f"\n  ⚠️  CRITICAL CHECK:")
    print(f"     q_lower (original): {q_lower}")
    print(f"     q_norm (normalized): {q_norm}")
    
    # Check if category keywords match q_lower vs q_norm
    cat_match_lower = 0
    cat_match_norm = 0
    for cat_key, kws in CATEGORIES_KEYWORDS.items():
        for kw in kws:
            if kw in q_lower:
                cat_match_lower += 1
            if kw in q_norm:
                cat_match_norm += 1
    print(f"     Keywords matching q_lower: {cat_match_lower}")
    print(f"     Keywords matching q_norm: {cat_match_norm}")
    if cat_match_norm > cat_match_lower:
        print(f"     🔴 BUG: answer_question dùng q_lower (thiếu dấu) → MISS {cat_match_norm - cat_match_lower} keywords!")

print("\n" + "="*80)
print("🏁 DONE — Kiểm tra xem answer_question dùng q_lower hay q_normalized cho category detection")
print("="*80)

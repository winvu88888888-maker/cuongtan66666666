# -*- coding: utf-8 -*-
"""Test Vietnamese WITH diacritics - exact simulation of answer_question"""
import sys; sys.stdout.reconfigure(encoding='utf-8')

# ====== SIMULATE EXACT answer_question flow ======
# Test with Vietnamese DIACRITICS
q = 'Năm nay có nên đầu tư kinh doanh không'
q_lower = q.lower()
print(f'q_lower: {q_lower}')

# Normalize (should be no-op since already has diacritics)
# Load actual _VN_NO_DIAC_MAP from module
from free_ai_helper import FreeAIHelper
import inspect

# Just test category detection directly with the question
# Simulate category detection with real keywords from CATEGORIES
CATEGORIES_KW = {
    'TÀI_CHÍNH': ['tiền', 'tài chính', 'mua bán', 'đầu tư', 'giàu', 'nghèo', 'lương', 'thu nhập', 'nợ',
                   'vay', 'cho vay', 'kinh doanh', 'buôn bán', 'lãi', 'lỗ', 'cổ phiếu', 'crypto',
                   'bitcoin', 'nhà đất', 'mua nhà', 'bất động sản', 'vốn', 'hùn vốn', 'trúng số',
                   'tài sản', 'vàng', 'bạc', 'kim cương', 'trang sức', 'lương tháng',
                   'bán hàng', 'lợi nhuận', 'doanh thu', 'thu lời', 'lời lãi', 'hoa hồng',
                   'làm ăn', 'khai trương', 'góp vốn', 'hợp tác', 'thua lỗ', 'thu hồi vốn'],
    'CHUNG': ['vận mệnh', 'năm nay', 'tháng này', 'an toàn', 'quý nhân', 'may mắn',
              'tuổi', 'bao nhiêu tuổi', 'mấy tuổi'],
    'CÔNG_VIỆC': ['việc', 'công việc', 'sếp', 'thăng tiến', 'thăng chức', 'thi', 'đỗ', 'trượt', 'phỏng vấn',
                  'xin việc', 'nghỉ việc', 'sa thải', 'hợp đồng', 'dự án', 'thầu', 'đấu thầu',
                  'kiện', 'kiện tụng', 'tòa', 'quan chức', 'chức vụ', 'đề bạt',
                  'du học', 'học hành', 'thi cử', 'đại học', 'đi làm', 'chức', 'sự nghiệp',
                  'khởi nghiệp', 'startup', 'bổ nhiệm', 'chuyển công tác',
                  'sản xuất', 'phát triển', 'thụt lùi', 'công ty', 'nhà máy', 'xưởng',
                  'doanh nghiệp', 'cơ sở', 'kinh doanh', 'mở rộng', 'phá sản'],
}

tests = [
    'Năm nay có nên đầu tư kinh doanh không',  # CÓ DẤU
    'nam nay co nen dau tu kinh doanh khong',  # KHÔNG DẤU
    'Tôi có nên mua nhà không',                 # CÓ DẤU
    'Mẹ tôi bệnh có khỏi không',                # CÓ DẤU
    'Bao giờ tôi có người yêu',                  # CÓ DẤU
]

for q in tests:
    q_lower = q.lower()
    detected_category = 'CHUNG'
    max_score = 0
    all_matches = {}
    
    for cat, kws in CATEGORIES_KW.items():
        score = 0
        matched = []
        for kw in kws:
            if kw in q_lower:
                score += len(kw)
                matched.append(kw)
        all_matches[cat] = (score, matched)
        if score > max_score:
            max_score = score
            detected_category = cat
    
    DT_MAP = {'TÀI_CHÍNH': 'Thê Tài', 'CHUNG': 'Bản Thân', 'CÔNG_VIỆC': 'Quan Quỷ',
              'SỨC_KHỎE_GIA_ĐÌNH': 'Bản Thân', 'TÌNH_CẢM': 'Thê Tài'}
    dt = DT_MAP.get(detected_category, 'Bản Thân')
    
    print(f'Q: {q}')
    for cat, (sc, ma) in sorted(all_matches.items(), key=lambda x: -x[1][0]):
        if sc > 0:
            print(f'  {cat}: score={sc} matched={ma}')
    print(f'  => category={detected_category}, DT={dt}')
    expected_ok = (q == tests[0] and detected_category == 'TÀI_CHÍNH')
    if q == tests[0]:
        print(f'  {"PASS" if detected_category == "TÀI_CHÍNH" else "FAIL"}: expected TÀI_CHÍNH, got {detected_category}')
    print()

# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import FreeAIHelper
ai = FreeAIHelper()

tests = [
    ('Người đó bao nhiêu tuổi?', 'AGE'),
    ('Mấy tuổi rồi?', 'AGE'),
    ('Khi nào thì tốt?', 'TIMING'),
    ('Bao giờ có kết quả?', 'TIMING'),
    ('Đồ mất ở đâu?', 'LOCATION'),
    ('Tìm ở chỗ nào?', 'LOCATION'),
    ('Hướng nào tốt nhất?', 'DIRECTION'),
    ('Hướng nhà nên quay về đâu?', 'DIRECTION'),
    ('Người này có thật lòng không?', 'PERSON'),
    ('Cô ấy tính cách thế nào?', 'PERSON'),
    ('Có nên mua nhà không?', 'YES_NO'),
    ('Làm việc này có được không?', 'YES_NO'),
    ('Tình hình như thế nào?', 'DESCRIBE'),
    ('Bệnh gì vậy?', 'HEALTH_DETAIL'),
    ('Được bao nhiêu tiền?', 'QUANTITY'),
    ('Vận mệnh năm nay', 'GENERAL'),
]

ok = 0
for q, expect in tests:
    got = ai._detect_question_type(q)
    status = 'OK' if got == expect else 'FAIL'
    if got == expect: ok += 1
    print(f"  {q:40s} -> {got:15s} (expect {expect:15s}) {status}")

print(f"\nResult: {ok}/{len(tests)} PASSED")

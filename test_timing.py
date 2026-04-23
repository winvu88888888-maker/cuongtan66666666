"""Test timing/Ứng Kỳ questions"""
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

QUESTIONS = [
    "Bao giờ tôi biết kết quả trúng tuyển?",
    "5 tháng nữa nhà này có bị phá không?",
    "Nhà này tồn tại được bao nhiêu năm?",
    "Chuyến đi ngày mai thế nào?",
    "Khi nào tôi lấy được chồng?",
]

for q in QUESTIONS:
    print("=" * 80)
    print(f"❓ {q}")
    print("=" * 80)
    r = h.answer_question(q)
    for l in r.split('\n'):
        if any(kw in l for kw in ['PHÁN QUYẾT', 'KHẲNG ĐỊNH', 'Nhanh', 'Chậm', 'NHANH', 'CHẬM',
                                   'ỨNG KỲ', 'THỜI GIAN', 'ngày', 'tháng', 'LỜI KHUYÊN',
                                   'Sự việc', '⚡', '🕒', '⏰']):
            print(f"  📋 {l.strip()[:120]}")
    print()

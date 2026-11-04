"""
TEST: AI Offline ra kết luận THẮNG THUA có rõ ràng không?
"""
import sys
sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

QUESTIONS = [
    "Đội MU đấu với đội Liverpool đội nào thắng?",
    "Đội Việt Nam đấu đội Thái Lan ai thắng trận tối nay?",
    "Trận chung kết Real Madrid gặp Barcelona đội nào vô địch?",
]

for q in QUESTIONS:
    print("=" * 80)
    print(f"❓ CÂU HỎI: {q}")
    print("=" * 80)
    result = helper.answer_question(q)
    
    # Trích ra phần QUAN TRỌNG
    lines = result.split('\n')
    important_sections = []
    capture = False
    for l in lines:
        # Bắt các phần kết luận quan trọng
        if any(kw in l for kw in [
            'PHÁN QUYẾT', 'KHẲNG ĐỊNH', 'Thế=', 'Ứng=', 
            'CĂN CỨ', 'LH:', 'KM:', 'MH:', 'PHƯƠNG PHÁP',
            'LỜI KHUYÊN', 'Thắng Thua', '⚔️', 'BÊN CHỦ', 'BÊN KHÁCH',
            'KẾT LUẬN', 'Dụng Thần', 'áp đảo', 'ngang sức', 'chênh lệch',
            'Chênh', 'bên Thế', 'bên Ứng', 'CÂN BẰNG', 'HÒA'
        ]):
            important_sections.append(l.strip())
    
    if important_sections:
        print("\n🎯 PHẦN KẾT LUẬN QUAN TRỌNG:")
        print("-" * 60)
        for line in important_sections:
            print(f"  {line[:120]}")
    else:
        print("\n⚠️ KHÔNG TÌM THẤY KẾT LUẬN THẮNG THUA!")
        # Show full output for debugging
        print("\n📋 FULL OUTPUT (first 50 lines):")
        for l in lines[:50]:
            if l.strip():
                print(f"  {l.strip()[:100]}")
    print()

# -*- coding: utf-8 -*-
"""Test câu hỏi đời thường — xem AI Offline trả lời có thông minh không"""
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

# Các câu hỏi thực tế mà user thường hỏi
test_cases = [
    ("ngày mai tôi nên ăn gì", "Phải suy luận từ Ngũ Hành → loại đồ ăn"),
    ("hôm nay mặc màu gì may mắn", "Ngũ Hành → màu sắc tương ứng"),
    ("nên đi hướng nào để gặp may", "Ngũ Hành → phương hướng"),
    ("con số may mắn hôm nay", "Ngũ Hành → số"),
    ("tôi có nên mua nhà không", "Yes/No + Vạn Vật nhà cửa"),
    ("bạn trai tôi có yêu tôi không", "Tình cảm + Thế Ứng"),
    ("khi nào tôi giàu", "Timing + Tài lộc"),
    ("sức khỏe tôi thế nào", "Sức khỏe + Ngũ Hành tạng phủ"),
    ("nên đầu tư vàng hay bất động sản", "So sánh → Ngũ Hành Kim vs Thổ"),
    ("mèo nhà tôi lạc ở đâu", "Tìm đồ + Phương hướng"),
]

for i, (question, expected) in enumerate(test_cases, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}: {question}")
    print(f"KỲ VỌNG: {expected}")
    print(f"{'='*60}")
    
    r = h.answer_question(question, chart_data=None, topic=None)
    
    # Extract the HEADER answer (visible part)
    lines = r.split('\n')
    header_text = ""
    for line in lines:
        # Find the big answer text in header
        if 'font-size:2em' in line:
            import re
            m = re.search(r'>(.*?)</div>', line)
            if m:
                header_text = m.group(1)
                break
    
    # Find the PHÁN QUYẾT / direct answer
    verdict_text = ""
    for line in lines:
        if 'PHÁN' in line and 'color:#fbbf24' in line:
            m = re.search(r'>(.*?)</b>', line)
            if m:
                verdict_text = m.group(1)
                break
    
    # Check for Vạn Vật usage
    van_vat_used = 'VẠN VẬT' in r or 'Vạn Vật' in r
    ngu_hanh_used = any(h in r for h in ['hành Kim', 'hành Mộc', 'hành Thủy', 'hành Hỏa', 'hành Thổ'])
    
    # Check answer quality
    quality_markers = {
        'Có Ngũ Hành': ngu_hanh_used,
        'Có Vạn Vật': van_vat_used,
        'Có Header rõ ràng': bool(header_text),
        'Không phải generic': 'CẦN CÂN NHẮC' not in header_text,
    }
    
    print(f"  📋 HEADER: {header_text[:100] if header_text else '(trống)'}")
    print(f"  📋 VERDICT: {verdict_text[:100] if verdict_text else '(trống)'}")
    for label, ok in quality_markers.items():
        status = '✅' if ok else '❌'
        print(f"  {status} {label}")
    
    # Specific checks per question type
    if 'ăn gì' in question:
        has_food = any(f in r for f in ['thức ăn', 'đồ ăn', 'nóng', 'lạnh', 'cay', 'ngọt', 'mặn',
                                         'rau', 'thịt', 'cá', 'gạo', 'trái cây', 'hải sản', 'kem'])
        print(f"  {'✅' if has_food else '❌'} Có gợi ý đồ ăn cụ thể")
    elif 'màu' in question:
        has_color = any(c in r for c in ['trắng', 'đỏ', 'xanh', 'vàng', 'đen', 'nâu', 'cam'])
        print(f"  {'✅' if has_color else '❌'} Có gợi ý màu sắc")
    elif 'hướng' in question:
        has_dir = any(d in r for d in ['Đông', 'Tây', 'Nam', 'Bắc', 'Trung'])
        print(f"  {'✅' if has_dir else '❌'} Có gợi ý hướng")
    elif 'số' in question:
        has_num = any(n in r for n in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
        print(f"  {'✅' if has_num else '❌'} Có gợi ý số")

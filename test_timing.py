# -*- coding: utf-8 -*-
"""Test Ứng Kỳ ngày cụ thể"""
import sys, os
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper
helper = FreeAIHelper()

tests = [
    "Bao giờ tôi xin được việc mới?",
    "Khi nào khách đến chơi nhà?",
    "Bao giờ tôi có người yêu?",
    "Tháng nào kinh doanh tốt nhất?",
]

for q in tests:
    print("=" * 70)
    print(f"Q: {q}")
    result = helper.answer_question(q, chart_data=None, topic=None)
    
    # Extract timing section
    lines = result.split('\n')
    in_timing = False
    timing_lines = []
    header_line = ""
    
    for line in lines:
        s = line.strip()
        # Find header with date
        if '📆' in s and ('/' in s) and ('ngày' in s.lower() or 'lúc' in s.lower()):
            if not header_line:
                header_line = s
        # Find timing block
        if 'ỨNG KỲ CHI TIẾT' in s or 'Chi ' in s and '🔮' in s:
            in_timing = True
        if in_timing:
            timing_lines.append(s)
            if 'Ưu tiên' in s:
                in_timing = False
        # Find verdict
        if 'KHẲNG ĐỊNH' in s:
            if not header_line:
                header_line = s
        if 'DỰ ĐOÁN NGÀY SỚM NHẤT' in s:
            timing_lines.append(s)
    
    # Show header
    if header_line:
        print(f"  HEADER: {header_line[:150]}")
    
    # Show timing
    if timing_lines:
        print(f"  TIMING ({len(timing_lines)} lines):")
        for tl in timing_lines[:20]:
            if tl:
                print(f"    {tl[:120]}")
    else:
        # Try to find any date references
        date_lines = [l.strip() for l in lines if '📆' in l or 'DỰ ĐOÁN' in l or 'NGÀY GẦN' in l]
        if date_lines:
            print(f"  DATE REFS:")
            for dl in date_lines[:5]:
                print(f"    {dl[:120]}")
        else:
            print("  ⚠️ No specific dates found!")
    
    print()

print("DONE!")

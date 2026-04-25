# -*- coding: utf-8 -*-
"""Xem chính xác HEADER hiện gì cho user"""
import sys, re; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

test_questions = [
    'ngày mai tôi nên ăn gì',
    'hôm nay mặc màu gì may mắn',
    'nên đi hướng nào để gặp may',
    'con số may mắn hôm nay',
    'tôi có nên mua nhà không',
    'bạn trai tôi có yêu tôi không',
    'khi nào tôi giàu',
    'sức khỏe tôi thế nào',
    'nên đầu tư vàng hay bất động sản',
    'mèo nhà tôi lạc ở đâu',
]

for i, q in enumerate(test_questions, 1):
    r = h.answer_question(q, chart_data=None, topic=None)
    
    # Extract header answer (the big text)
    m = re.search(r'font-size:2em.*?>(.*?)</div>', r)
    header_answer = m.group(1) if m else '?'
    
    # Extract score line
    m2 = re.search(r'Điểm:.*?<b>(\d+)%</b>.*?DT:.*?<b>(.*?)</b>', r)
    score = m2.group(1) if m2 else '?'
    dt = m2.group(2) if m2 else '?'
    
    print(f"[{i}] Q: {q}")
    print(f"    → HEADER: {header_answer}")
    print(f"    → Score: {score}% | DT: {dt}")
    print()

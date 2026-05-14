# -*- coding: utf-8 -*-
"""Quick DT + Multi-intent trace"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from free_ai_helper import _get_dung_than, _get_all_dung_than, v32_parse_question

tests = [
    "nam nay toi co mua duoc nha khong",
    "toi co nen dau tu kinh doanh nam nay khong",
    "bao gio toi co nguoi yeu",
    "nam nay co mua duoc nha khong",
    "toi co duoc tang luong khong",
    "benh cua me toi co chua duoc khong",
]

for q in tests:
    dt = _get_dung_than(q)
    all_dts = _get_all_dung_than(q)
    parsed = v32_parse_question(q)
    
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"DT: {dt} | All DTs: {all_dts}")
    print(f"Parsed: {len(parsed)} sub-questions")
    
    for i, p in enumerate(parsed):
        text = p.get('text', '?')
        pdt = p.get('dung_than', '?')
        print(f"  [{i+1}] '{text}' → DT={pdt}")
    
    # Đánh giá
    issues = []
    if len(parsed) > 1 and len(q.split()) <= 10:
        issues.append(f"MULTI-SPLIT SAI: Câu hỏi đơn ({len(q.split())} từ) bị split thành {len(parsed)}")
    
    # Check DT logic
    q_lower = q.lower()
    expected_dt = None
    if any(k in q_lower for k in ['mua', 'tiền', 'kinh doanh', 'đầu tư', 'dau tu', 'nha', 'nhà', 'xe', 'tài']):
        expected_dt = 'Thê Tài'
    elif any(k in q_lower for k in ['nguoi yeu', 'người yêu', 'vợ', 'chồng', 'tình']):
        expected_dt = 'Quan Quỷ'  # Nữ hỏi tình = Quan Quỷ
    elif any(k in q_lower for k in ['bệnh', 'benh', 'ốm', 'sức khỏe']):
        expected_dt = 'Quan Quỷ'
    elif any(k in q_lower for k in ['lương', 'luong', 'việc', 'viec', 'thăng']):
        expected_dt = 'Quan Quỷ'
    
    if expected_dt and dt != expected_dt:
        issues.append(f"DT SAI: Got '{dt}' nhưng expected '{expected_dt}'")
    
    if issues:
        for iss in issues:
            print(f"  ⚠️ {iss}")
    else:
        print(f"  ✅ OK")

# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from question_parser import parse_question

tests = [
    'xe của chị tôi mất ở đâu',
    'nhà tôi có bán được không',
    'bệnh của bố tôi nặng không',
    'hợp đồng có ký được không',
    'chó tôi mất rồi tìm đâu',
    'thuốc này có tốt không',
    'tiền của tôi mất ở đâu',
    'xe máy có bị hư không',
    'giấy tờ nhà bao giờ xong',
]

print("=" * 70)
print("TEST: OBJECT_DT_MAP — Vạn Vật Loại Tượng chính xác")
print("=" * 70)
for t in tests:
    r = parse_question(t)
    if r:
        p = r[0]
        g = p.get('grammar', {}) or {}
        s = g.get('subject', {}) if g else {}
        label = s.get('label', '?')
        stype = s.get('type', '?')
        owner = s.get('owner', '')
        owner_dt = s.get('owner_dt', '')
        dt = p['dung_than']
        
        owner_info = f" | Của: {owner} ({owner_dt})" if owner else ""
        print(f"  '{t}'")
        print(f"    Subject: {label} ({stype}){owner_info}")
        print(f"    DT: {dt}")
        print()

# Validate specific cases
print("=" * 70)
print("VALIDATE: Xe/Nhà = Phụ Mẫu (kinh điển)")
print("=" * 70)
checks = [
    ('xe của chị tôi mất ở đâu', 'Phụ Mẫu'),
    ('bệnh của bố tôi nặng không', 'Quan Quỷ'),
    ('tiền của tôi mất ở đâu', 'Thê Tài'),
]
all_ok = True
for q, expected_dt in checks:
    r = parse_question(q)
    got_dt = r[0]['dung_than'] if r else '?'
    ok = got_dt == expected_dt
    icon = '✅' if ok else '❌'
    print(f"  {icon} '{q[:40]}...' → DT={got_dt} (expected={expected_dt})")
    if not ok:
        all_ok = False

print()
if all_ok:
    print("🎉 ALL OBJECT DT CHECKS PASSED!")
else:
    print("⚠️ Some checks failed")

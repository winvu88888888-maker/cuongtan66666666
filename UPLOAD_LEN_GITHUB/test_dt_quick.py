"""Quick DT detail match test"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

q = 'bố tôi bệnh nặng có qua khỏi không?'
q_lower = q.lower()
detail = {
    'bố': 'Phụ Mẫu', 'mẹ': 'Phụ Mẫu', 'cha': 'Phụ Mẫu',
    'con': 'Tử Tôn', 'con trai': 'Tử Tôn', 'con gái': 'Tử Tôn',
    'vợ': 'Thê Tài', 'chồng': 'Quan Quỷ',
    'anh': 'Huynh Đệ', 'chị': 'Huynh Đệ', 'em': 'Huynh Đệ'
}

# Sort by length desc (as in engine)
items = sorted(detail.items(), key=lambda x: len(x[0]), reverse=True)
print(f"Question: {q}")
print(f"q_lower: {q_lower}")
print(f"'bố' in q_lower = {'bố' in q_lower}")
for kw, dt in items:
    found = kw in q_lower
    print(f"  Check '{kw}' in q_lower = {found}")
    if found:
        print(f"  => MATCH: {kw} -> {dt}")
        break

# Also check override
if 'sức khỏe tôi' in q_lower or 'tôi khỏe' in q_lower or 'tôi bệnh' in q_lower:
    print("  => OVERRIDE to Bản Thân!")

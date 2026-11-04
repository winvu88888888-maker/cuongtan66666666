# -*- coding: utf-8 -*-
"""V42.9 FINAL FIX: 
1. Chuẩn hóa factor labels V27/V28 → bỏ prefix version
2. Bỏ V34.0 trong SĐ MASTER
3. Verify THÁM TỬ hiện cho MỌI loại câu hỏi
"""
import re

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ═══ FIX 1: Bỏ prefix V27/V28 trong factor labels ═══
# Các factor như "V28 KM BT khắc Cung SV → chủ THẮNG +5" → "KM BT khắc Cung SV → chủ THẮNG +5"
# "V27 KM Sao×Môn Cát +5" → "KM Sao×Môn Cát +5"

# Replace in factor append lines
factor_patterns = [
    # KỲ MÔN factors
    (r'f"V27 KM ', 'f"KM '),
    (r'f"V28 KM ', 'f"KM '),
    # LỤC HÀO factors  
    (r'f"V27 LH ', 'f"LH '),
    (r'f"V28 LH ', 'f"LH '),
    # LỤC NHÂM factors
    (r'f"V27 LN ', 'f"LN '),
    (r'f"V28 LN ', 'f"LN '),
    # THÁI ẤT factors
    (r'f"V27 TA ', 'f"TA '),
    (r'f"V28 TA ', 'f"TA '),
    # KINH DỊCH
    (r'"[V27 KINH DICH]', '"[KINH DỊCH]'),
]

for old, new in factor_patterns:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        changes += 1
        print(f"  ✅ Bỏ version prefix: {old} → {new} ({count}x)")

# ═══ FIX 2: V34.0 trong SĐ MASTER ═══
old_sd = 'SĐ MASTER V34.0:'
new_sd = 'SĐ MASTER:'
count = content.count(old_sd)
if count > 0:
    content = content.replace(old_sd, new_sd)
    changes += 1
    print(f"  ✅ Bỏ V34.0 từ SĐ MASTER ({count}x)")

# ═══ FIX 3: V18 trong detective ═══  
old_v18 = 'f"V18: '
new_v18 = 'f"'
count = content.count(old_v18)
if count > 0:
    content = content.replace(old_v18, new_v18)
    changes += 1
    print(f"  ✅ Bỏ V18 prefix từ detective ({count}x)")

# Save
with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'='*60}")
print(f"Tổng: {changes} thay đổi")

# Verify non-V42 versions remaining
remaining = re.findall(r'factors\.append\(f"V\d+', content)
if remaining:
    print(f"\n⚠️ Remaining V-prefix in factors: {set(remaining)}")
else:
    print(f"\n✅ ALL factor labels clean!")

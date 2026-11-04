# -*- coding: utf-8 -*-
"""Fix last 2 missing slots: SD14.ky_than + SD2.vv_con_nguoi"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'free_ai_helper.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: SD14 ky_than — template has {ky_than} but generic_slots sets kt_hanh not ky_than
# The slot name in template is 'ky_than' but code uses 'kt_hanh' for the Kỵ Thần's hành
# Need to add generic_slots.setdefault('ky_than', ...) 
marker = "generic_slots.setdefault('kt_nguyen_nhan'"
if marker in content:
    idx = content.find(marker)
    # Find the line start
    line_start = content.rfind('\n', 0, idx) + 1
    # Insert ky_than default before kt_nguyen_nhan
    insert_line = "            generic_slots.setdefault('ky_than', f\"{_kth} ({KY_THAN_NGUYEN_NHAN.get(dung_than, '?')})\" if _kth else '?')\n"
    content = content[:line_start] + insert_line + content[line_start:]
    print("✅ Fix 1: Added SD14 ky_than slot")
else:
    print("❌ Fix 1: Marker not found")

# Fix 2: SD2 vv_con_nguoi — template has {vv_con_nguoi} but generic_slots doesn't set it
# Need to add generic_slots.setdefault('vv_con_nguoi', ...)
marker2 = "generic_slots['tuoi_trung_binh']"
if marker2 in content:
    idx2 = content.find(marker2)
    # Find end of that line
    line_end = content.find('\n', idx2) + 1
    # Add vv_con_nguoi after tuoi_trung_binh
    insert_line2 = "                generic_slots.setdefault('vv_con_nguoi', vv_cu_the.get('nguoi', hanh_vat.get('co_the', '?')) if vv_cu_the else '?')\n"
    content = content[:line_end] + insert_line2 + content[line_end:]
    print("✅ Fix 2: Added SD2 vv_con_nguoi slot")
else:
    print("❌ Fix 2: Marker not found")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All fixes applied!")

# -*- coding: utf-8 -*-
"""DEEP AUDIT: Tìm chính xác nội dung trùng lặp giữa 3 biến output chính"""
import sys, re; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

r = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

# Split output by <details> collapse
parts = r.split('<details>')
print(f"Có {len(parts)} phần (1 visible + {len(parts)-1} collapse)")

# Now trace what's INSIDE the collapse
if len(parts) >= 2:
    collapse_content = parts[1].split('</details>')[0]
    
    # Find section headers inside collapse
    print("\n=== NỘI DUNG TRONG COLLAPSE ===")
    for i, line in enumerate(collapse_content.split('\n')):
        s = line.strip()
        if s.startswith(('##', '###', '**⏰', '**🔍', '**🕳', '**⚡', '**🤝', '**🔗', 
                         '**🌿', '**🍂', '**🔮', '**📐', '**🌟', '**💥', '**👁',
                         '**🚪', '**📜', '**🐎', '📢', '✅ KẾT', '**✅',
                         '🔮 PROTOCOL', 'BƯỚC', '📐 SƠ ĐỒ')):
            print(f"  [{i:4d}] {s[:140]}")
        # Also find ỨNG KỲ, THÁM TỬ, VẠN VẬT headings
        if any(k in s for k in ['ỨNG KỲ', 'THÁM TỬ', 'VẠN VẬT', 'PHÁN QUYẾT', 'KHẲNG ĐỊNH', 'PROTOCOL 27']):
            print(f"  [{i:4d}] ★ {s[:140]}")

# Count duplicates of key sections within collapse
print("\n=== TRÙNG LẶP TRONG COLLAPSE ===")
dup_checks = {
    'PROTOCOL 27 BƯỚC': 'PROTOCOL 27',
    'THÁM TỬ KIỂM CHỨNG': 'THÁM TỬ KIỂM CHỨNG',
    'ỨNG KỲ (header)': '⏰ ỨNG KỲ',
    'PHÁN QUYẾT': '📢',
    'KHẲNG ĐỊNH': 'KHẲNG ĐỊNH',
    'VẠN VẬT LOẠI TƯỢNG': 'VẠN VẬT LOẠI TƯỢNG',
    'THIÊN CƠ ĐẠI SƯ': 'THIÊN CƠ ĐẠI SƯ',
    'KẾT LUẬN CHÍNH THỨC': 'KẾT LUẬN CHÍNH THỨC',
    'CHUỖI BẰNG CHỨNG': 'CHUỖI BẰNG CHỨNG',
    'CÂU TRẢ LỜI': 'CÂU TRẢ LỜI',
    'TỔNG HỢP + CHUỖI': 'TỔNG HỢP',
    'LUẬN GIẢI': 'LUẬN GIẢI',
    'BƯỚC 0': 'BƯỚC 0',
    'BƯỚC 1': 'BƯỚC 1',
    'SƠ ĐỒ': 'SƠ ĐỒ',
}
for label, kw in dup_checks.items():
    count = collapse_content.count(kw)
    status = '✅' if count <= 1 else f'⚠️ TRÙNG {count}x!'
    print(f"  {status} {label}: {count}")

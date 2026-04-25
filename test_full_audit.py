# -*- coding: utf-8 -*-
"""Test toàn diện: kiểm tra TẤT CẢ section quan trọng có trong output"""
import sys, re; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

r = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

print("=" * 60)
print("KIỂM TRA ĐẦY ĐỦ CÁC SECTION QUAN TRỌNG")
print("=" * 60)

# Nhóm 1: Ứng Kỳ, Ám Động, Nguyệt Phá, Bát Môn
group1 = {
    'Ứng Kỳ (bất kỳ)': 'Ứng Kỳ',
    'Ứng Kỳ Chuyên Sâu': 'ỨNG KỲ CHUYÊN SÂU',
    'Ám Động': 'ÁM ĐỘNG',
    'Nguyệt Phá': 'NGUYỆT PHÁ',
    'Bát Môn (Nhân Bàn)': 'NHÂN BÀN',
    'Bát Thần (Thần Bàn)': 'THẦN BÀN',
    'Bảng 6 Hào': 'Bảng 6 Hào',
}

# Nhóm 2: Không Vong, Tam Hợp, Dịch Mã, Thoán Từ  
group2 = {
    'Không Vong': 'Không Vong',
    'Tam Hợp': 'Tam Hợp',
    'Lục Xung': 'Lục Xung',
    'Dịch Mã': 'Dịch Mã',
    'Thoán Từ': 'Thoán Từ',
    'Thần Sát': 'Thần Sát',
    'Hào Vị': 'Hào Vị',
    'Lệnh Tháng': 'Lệnh Tháng',
    'Trường Sinh': 'Trường Sinh',
    'Hỗ Quái': 'Hỗ Quái',
    'Biến Quái': 'Biến Quái',
}

# Nhóm 3: Output structure
group3 = {
    'KẾT LUẬN AI OFFLINE': 'KẾT LUẬN AI OFFLINE',
    'PROTOCOL 27': 'PROTOCOL 27',
    'THÁM TỬ': 'THÁM TỬ',
    'VẠN VẬT': 'VẠN VẬT',
    'PHÁN QUYẾT': 'PHÁN QUYẾT',
    'KHẲNG ĐỊNH': 'KHẲNG ĐỊNH',
}

print("\n--- NHÓM 1: Ứng Kỳ, Ám Động, Nguyệt Phá, Bát Môn ---")
for name, keyword in group1.items():
    count = r.count(keyword)
    status = '✅' if count > 0 else '❌'
    print(f"  {status} {name}: {count}x")

print("\n--- NHÓM 2: Không Vong, Tam Hợp, Dịch Mã, Thoán Từ ---")
for name, keyword in group2.items():
    count = r.count(keyword)
    status = '✅' if count > 0 else '❌'
    print(f"  {status} {name}: {count}x")

print("\n--- NHÓM 3: Cấu trúc output ---")
for name, keyword in group3.items():
    count = r.count(keyword)
    status = '✅' if count == 1 else ('⚠️' if count > 1 else '❌')
    print(f"  {status} {name}: {count}x {'(DUY NHẤT ✓)' if count == 1 else ''}")

# Version check
print("\n--- PHIÊN BẢN HIỂN THỊ ---")
versions = re.findall(r'V\d+\.?\d*[a-z]?', r)
from collections import Counter
vc = Counter(versions)
for v, c in sorted(vc.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {v}: {c}x")

print(f"\nTổng: {len(r)} chars, {len(r.split(chr(10)))} lines")

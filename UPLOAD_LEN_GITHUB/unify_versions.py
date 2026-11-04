# -*- coding: utf-8 -*-
"""V42.9: Thống nhất tất cả phiên bản trong OUTPUT thành V42.9
Chỉ thay đổi TIÊU ĐỀ HIỆN CHO USER, không thay đổi logic code bên trong."""
import re

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# ═══ 1. Thay đổi TIÊU ĐỀ/HEADER hiện cho user ═══

# Header file docstring
content = content.replace(
    'Free AI Helper V42.2 — THIÊN CƠ ĐẠI SƯ (Siêu Premium UI + Answer-First + Vạn Vật 3378+ + 12 Trường Sinh)',
    'Free AI Helper V42.9 — THIÊN CƠ ĐẠI SƯ (Siêu Premium UI + Answer-First + Vạn Vật 3378+ + 12 Trường Sinh)'
)

# THIÊN CƠ ĐẠI SƯ version in output headers
content = content.replace('THIÊN CƠ ĐẠI SƯ — V31.1 Phân Tích Thống Nhất', 'THIÊN CƠ ĐẠI SƯ — V42.9 Phân Tích Thống Nhất')

# PROTOCOL 27 BƯỚC
content = content.replace('PROTOCOL 27 BƯỚC — LUẬN GIẢI THỐNG NHẤT V38.2', 'PROTOCOL 27 BƯỚC — LUẬN GIẢI THỐNG NHẤT V42.9')

# V26.2 LỰC LƯỢNG THỐNG NHẤT (section header shown to user)
content = content.replace('LƯỢNG HÓA LỰC LƯỢNG (V26.2 LỰC LƯỢNG THỐNG NHẤT)', 'LƯỢNG HÓA LỰC LƯỢNG (V42.9 LỰC LƯỢNG THỐNG NHẤT)')

# V26.2 footer
content = content.replace('Thiên Cơ Đại Sư V26.2 — Lực Lượng Tổng Hợp', 'Thiên Cơ Đại Sư V42.9 — Lực Lượng Tổng Hợp')

# THỐNG KÊ TOÀN BỘ YẾU TỐ TÁC ĐỘNG DT (V26.2)
content = content.replace('THỐNG KÊ TOÀN BỘ YẾU TỐ TÁC ĐỘNG DT (V26.2)', 'THỐNG KÊ TOÀN BỘ YẾU TỐ TÁC ĐỘNG DT (V42.9)')

# KẾT LUẬN AI OFFLINE header — already updated to V42.9 in previous commit, but double-check
content = content.replace('KẾT LUẬN AI OFFLINE — THIÊN CƠ ĐẠI SƯ V40.9', 'KẾT LUẬN AI OFFLINE — THIÊN CƠ ĐẠI SƯ V42.9')

# KẾT LUẬN AI ONLINE header  
content = content.replace('KẾT LUẬN AI ONLINE (Gemini V40.9)', 'KẾT LUẬN AI ONLINE (Gemini V42.9)')

# AI OFFLINE — PROTOCOL 27 BƯỚC (V38.1)
content = content.replace('AI OFFLINE — PROTOCOL 27 BƯỚC (V38.1)', 'AI OFFLINE — PROTOCOL 27 BƯỚC (V42.9)')

# PHÂN TÍCH DETERMINISTIC (Python Engine V41.0)
content = content.replace('PHÂN TÍCH DETERMINISTIC (Python Engine V41.0)', 'PHÂN TÍCH DETERMINISTIC (Python Engine V42.9)')

# ═══ 2. Thay đổi version trong SECTION HEADERS bên trong details/collapse ═══

# V42.2 in Bát Môn/Bát Thần/Lục Hào headers
content = content.replace('NHÂN BÀN (Bát Môn) — V42.2', 'NHÂN BÀN (Bát Môn)')
content = content.replace('THẦN BÀN (Bát Thần) — V42.2', 'THẦN BÀN (Bát Thần)')
content = content.replace('Bảng 6 Hào (V42.2 — Lục Thần + Lục Thân đầy đủ)', 'Bảng 6 Hào (Lục Thần + Lục Thân)')

# V42.0 Ứng Kỳ + Ám Động
content = content.replace('ỨNG KỲ CHUYÊN SÂU (V42.0)', 'ỨNG KỲ CHUYÊN SÂU')
content = content.replace('ÁM ĐỘNG (V42.0) — Lực lượng ẩn', 'ÁM ĐỘNG — Lực lượng ẩn')

# V42.1 Nguyệt Phá
content = content.replace('NGUYỆT PHÁ (V42.1)', 'NGUYỆT PHÁ')

# V9.0 sections — remove version tag
for old_v9 in [
    'KHÔNG VONG (V9.0)', 'TAM HỢP CỤC (V9.0)', 'LỤC XUNG THẾ-ỨNG (V9.0)',
    'LỤC HỢP THẾ-ỨNG (V9.0)', 'LỆNH THÁNG (V9.0)', 'HỖ QUÁI SINH THỂ (V9.0)',
    'HỖ QUÁI KHẮC THỂ (V9.0)', 'BIẾN QUÁI SINH THỂ (V9.0)', 'BIẾN QUÁI KHẮC THỂ (V9.0)',
    'ỨNG KỲ (V9.0)', 'Trường Sinh Nạp Âm (V9.0)', 'THẦN SÁT (V9.0)',
    'THOÁN TỪ (V9.0)', 'HÀO VỊ (V9.0)',
]:
    new_v9 = old_v9.replace(' (V9.0)', '')
    content = content.replace(old_v9, new_v9)

# V15.0 sections
for old_v15 in [
    'TUẦN KHÔNG TỨ TRỤ (V15.0)', 'DỊCH MÃ TỨ TRỤ (V15.0)', 'TỨ TRỤ Ý NGHĨA (V15.0)',
]:
    new_v15 = old_v15.replace(' (V15.0)', '')
    content = content.replace(old_v15, new_v15)

# Save
with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"Original size: {original_len}")
print(f"New size: {new_len}")
print(f"Diff: {new_len - original_len}")

# Verify — count remaining old version references in output headers
remaining = []
for pattern in ['V9.0', 'V15.0', 'V26.2', 'V31.1', 'V38.1', 'V38.2', 'V40.9', 'V41.0', 'V42.0', 'V42.1', 'V42.2']:
    lines_with = []
    for i, line in enumerate(content.split('\n'), 1):
        if pattern in line and ('append' in line or 'final_parts' in line):
            lines_with.append(i)
    if lines_with:
        remaining.append(f"  {pattern}: {len(lines_with)} output lines remaining")

if remaining:
    print(f"\n⚠️ Remaining old versions in output:")
    for r in remaining:
        print(r)
else:
    print("\n✅ ALL output headers unified to V42.9!")

# -*- coding: utf-8 -*-
"""AUDIT TOÀN BỘ PIPELINE — Tìm mọi bước xử lý + phiên bản"""
import re

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=" * 80)
print("AUDIT TOÀN DIỆN: FREE_AI_HELPER.PY")
print(f"Tổng: {len(lines)} dòng")
print("=" * 80)

# 1. Tìm tất cả hàm def
print("\n=== 1. TẤT CẢ CÁC HÀM (def) ===")
funcs = []
for i, line in enumerate(lines, 1):
    m = re.match(r'\s*(def\s+(\w+)\s*\()', line)
    if m:
        indent = len(line) - len(line.lstrip())
        funcs.append((i, m.group(2), indent))
        
print(f"Tổng hàm: {len(funcs)}")
for line_no, name, indent in funcs:
    marker = "  " if indent > 0 else ""
    print(f"  Line {line_no:5d}: {marker}{name}")

# 2. Tìm các BƯỚC trong pipeline chính (answer_question)
print("\n=== 2. CÁC BƯỚC TRONG answer_question() ===")
in_answer = False
for i, line in enumerate(lines, 1):
    if 'def answer_question' in line:
        in_answer = True
        print(f"  START: Line {i}")
        continue
    if in_answer:
        if re.match(r'    def ', line) and 'lambda' not in line:
            print(f"  END: Line {i}")
            break
        # Find version comments and step markers
        stripped = line.strip()
        if stripped.startswith('# V') or stripped.startswith('# ===') or stripped.startswith('# ───'):
            if any(k in stripped for k in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9',
                                           'BƯỚC', 'BUILD', 'INJECT', 'PROTOCOL', 'ONLINE', 'OFFLINE',
                                           'KẾT LUẬN', 'THÁM TỬ', 'VẠN VẬT', 'CẢNH BÁO']):
                print(f"  Line {i:5d}: {stripped[:120]}")

# 3. Tìm các biến output chính
print("\n=== 3. CÁC BIẾN OUTPUT CHÍNH ===")
output_vars = ['offline_full_output', 'direct_answer', 'v38_protocol_text', 'online_result',
               'v31_master_diagram', 'v31_question_diagram', 'v325_interaction',
               'v38_conclusion', 'v18_detective', 'v17_routing']
for var in output_vars:
    assigned = []
    used_in_append = []
    for i, line in enumerate(lines, 1):
        if f'{var} =' in line or f'{var}=' in line:
            if 'if' not in line.split('=')[0] and 'for' not in line.split('=')[0]:
                assigned.append(i)
        if var in line and ('append' in line or 'final_parts' in line):
            used_in_append.append(i)
    print(f"  {var}:")
    print(f"    Assigned at: {assigned[:5]}")
    print(f"    Used in output at: {used_in_append[:5]}")

# 4. Tìm sections mà tạo output text (lines.append / sections.append)
print("\n=== 4. CÁC HÀM TẠO OUTPUT TEXT ===")
output_funcs = []
for i, line in enumerate(lines, 1):
    if 'def ' in line and ('_build_' in line or '_generate_' in line or '_apply_' in line or '_fill_' in line):
        name = re.search(r'def\s+(\w+)', line)
        if name:
            output_funcs.append((i, name.group(1)))
for line_no, name in output_funcs:
    print(f"  Line {line_no:5d}: {name}")

# 5. Tìm duplicate logic (cùng keyword xuất hiện nhiều nơi)
print("\n=== 5. LOGIC TRÙNG LẶP (cùng phân tích ở nhiều chỗ) ===")
duplicate_checks = {
    'Ứng Kỳ analysis': 'ỨNG KỲ',
    'Ám Động analysis': 'ÁM ĐỘNG',
    'Nguyệt Phá analysis': 'NGUYỆT PHÁ',
    'Không Vong analysis': 'KHÔNG VONG',
    'Thần Sát analysis': 'THẦN SÁT',
    'Lục Xung analysis': 'LỤC XUNG',
    'Competition/Thắng Thua': 'THẮNG',
    'Protocol 27 steps': 'PROTOCOL 27',
    'THÁM TỬ': 'THÁM TỬ',
}
for label, keyword in duplicate_checks.items():
    append_lines = []
    for i, line in enumerate(lines, 1):
        if keyword in line and ('append' in line):
            append_lines.append(i)
    if len(append_lines) > 1:
        # Check if they're in different functions
        print(f"  {label}: {len(append_lines)} append points → lines {append_lines[:8]}")

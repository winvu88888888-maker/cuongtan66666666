# -*- coding: utf-8 -*-
"""V42.9 COMPREHENSIVE TEST: Test với dữ liệu giả lập ĐẦY ĐỦ
để xác định CHÍNH XÁC yếu tố nào hoạt động, yếu tố nào hỏng."""
import sys, re; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

# === TEST 1: Competition (không dấu) ===
print("=" * 70)
print("TEST 1: COMPETITION (u17 viet nam vs malaysia)")
print("=" * 70)
r1 = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

# === TEST 2: Timing (khi nào) ===
print("\n" + "=" * 70)
print("TEST 2: TIMING (khi nào lấy được vợ)")
print("=" * 70)
r2 = h.answer_question('khi nào tôi lấy được vợ', chart_data=None, topic=None)

# === TEST 3: Yes/No ===
print("\n" + "=" * 70)
print("TEST 3: YES/NO (có nên đầu tư)")
print("=" * 70)
r3 = h.answer_question('có nên đầu tư bất động sản không', chart_data=None, topic=None)

# === TEST 4: Where ===
print("\n" + "=" * 70)
print("TEST 4: WHERE (ở đâu)")
print("=" * 70)
r4 = h.answer_question('nên kinh doanh ở đâu', chart_data=None, topic=None)

# === TEST 5: What ===
print("\n" + "=" * 70)
print("TEST 5: WHAT (buôn bán gì)")  
print("=" * 70)
r5 = h.answer_question('nên buôn bán gì để giàu', chart_data=None, topic=None)

# === KIỂM TRA TOÀN DIỆN MỖI TEST ===
tests = {
    'Competition': r1,
    'Timing': r2,
    'Yes/No': r3,
    'Where': r4,
    'What': r5,
}

# Sections quan trọng phải CÓ
critical_sections = [
    ('HEADER: KẾT LUẬN AI OFFLINE', 'KẾT LUẬN AI OFFLINE'),
    ('PROTOCOL 27', 'PROTOCOL 27'),
    ('THIÊN CƠ ĐẠI SƯ', 'THIÊN CƠ ĐẠI SƯ'),
    ('THÁM TỬ (HTML)', '<b style="color:#fbbf24'),
    ('PHÁN QUYẾT (visible)', 'THẮNG'),  # For competition
    ('Bảng 6 Hào', 'Bảng 6 Hào'),
    ('Bát Môn (Nhân Bàn)', 'NHÂN BÀN'),
    ('Bát Thần (Thần Bàn)', 'THẦN BÀN'),
    ('Ứng Kỳ', 'Ứng Kỳ'),
    ('Không Vong', 'Không Vong'),
    ('Tam Hợp', 'Tam Hợp'),
    ('Dịch Mã', 'Dịch Mã'),
    ('Thoán Từ', 'Thoán Từ'),
    ('Lệnh Tháng', 'Lệnh Tháng'),
    ('Trường Sinh', 'Trường Sinh'),
    ('Hỗ Quái', 'Hỗ Quái'),
    ('Biến Quái', 'Biến Quái'),
    ('SĐ MASTER', 'SĐ MASTER'),
    ('SƠ ĐỒ TƯƠNG TÁC 6PP', 'SƠ ĐỒ TƯƠNG TÁC'),
    ('THỐNG KÊ YẾU TỐ', 'THỐNG KÊ CHI TIẾT'),
    ('CHUỖI BẰNG CHỨNG', 'CHUỖI BẰNG CHỨNG'),
    ('VẠN VẬT LOẠI TƯỢNG', 'VẠN VẬT LOẠI TƯỢNG'),
    ('V42.9 version', 'V42.9'),
]

# Sections CONDITIONAL (chỉ khi có data)
conditional_sections = [
    ('Ứng Kỳ CHUYÊN SÂU', 'ỨNG KỲ CHUYÊN SÂU'),
    ('Ám Động', 'ÁM ĐỘNG'),
    ('Nguyệt Phá', 'NGUYỆT PHÁ'),
    ('Thần Sát', 'Thần Sát'),
    ('Hào Vị', 'Hào Vị'),
    ('Lục Xung', 'Lục Xung'),
    ('Lục Hợp', 'Lục Hợp'),
]

print("\n" + "=" * 70)
print("BẢNG KIỂM TRA TOÀN DIỆN")
print("=" * 70)

# Header
header = f"{'Section':<30} | {'Comp':>6} | {'Time':>6} | {'Y/N':>6} | {'Where':>6} | {'What':>6}"
print(header)
print("-" * len(header))

for name, keyword in critical_sections:
    row = f"{name:<30}"
    for test_name, test_output in tests.items():
        count = test_output.count(keyword)
        status = f"{'✅'+str(count):>6}" if count > 0 else f"{'❌':>6}"
        row += f" | {status}"
    print(row)

print("\n--- CONDITIONAL (cần real data) ---")
for name, keyword in conditional_sections:
    row = f"{name:<30}"
    for test_name, test_output in tests.items():
        count = test_output.count(keyword)
        status = f"{'✅'+str(count):>6}" if count > 0 else f"{'⬜':>6}"
        row += f" | {status}"
    print(row)

# Uniqueness check
print("\n--- KIỂM TRA TRÙNG LẶP (phải = 1) ---")
unique_checks = [
    ('KẾT LUẬN AI OFFLINE', 'KẾT LUẬN AI OFFLINE'),
    ('PROTOCOL 27', 'PROTOCOL 27'),
    ('THIÊN CƠ ĐẠI SƯ', 'THIÊN CƠ ĐẠI SƯ'),
]
for name, keyword in unique_checks:
    row = f"{name:<30}"
    for test_name, test_output in tests.items():
        count = test_output.count(keyword)
        status = f"{'✅1':>6}" if count == 1 else f"{'❌'+str(count):>6}"
        row += f" | {status}"
    print(row)

# Output stats
print("\n--- OUTPUT STATS ---")
for test_name, test_output in tests.items():
    lines = len(test_output.split('\n'))
    chars = len(test_output)
    versions = re.findall(r'V\d+\.?\d*[a-z]?', test_output)
    non_v42 = [v for v in versions if not v.startswith('V42')]
    print(f"  {test_name}: {chars:,} chars, {lines} lines, V42.9: {versions.count('V42.9')}x, non-V42: {non_v42}")

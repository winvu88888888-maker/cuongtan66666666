"""
V42.8 FIX VERIFICATION — Test tất cả các sửa lỗi
"""
import sys
import datetime

# Test 1: Sidebar Lunar Date — 23/04/2026 phải ra ngày 7/3 Bính Ngọ
print("=" * 60)
print("TEST 1: Sidebar Lunar Date (xem_ngay_dep.solar2lunar)")
print("=" * 60)
from xem_ngay_dep import solar2lunar, tinh_28_tu
d, m, y, leap = solar2lunar(23, 4, 2026)
print(f"  23/04/2026 DL = ngày {d}/{m}/{y} ÂL (nhuận={leap})")
assert d == 7, f"FAIL: ngày phải là 7, nhận được {d}"
assert m == 3, f"FAIL: tháng phải là 3, nhận được {m}"
assert y == 2026, f"FAIL: năm ÂL phải là 2026"
print("  ✅ PASS: 23/04/2026 = 7/3/2026 ÂL\n")

# Test 2: qmdg_calc.solar_to_lunar — cũng phải ra ngày 7/3
print("=" * 60)
print("TEST 2: qmdg_calc.solar_to_lunar (hardcoded table)")
print("=" * 60)
import qmdg_calc
dt = datetime.datetime(2026, 4, 23)
d2, m2, y2, leap2 = qmdg_calc.solar_to_lunar(dt)
print(f"  23/04/2026 DL = ngày {d2}/{m2}/{y2} ÂL")
assert d2 == 7, f"FAIL: ngày phải là 7, nhận được {d2}"
assert m2 == 3, f"FAIL: tháng phải là 3, nhận được {m2}"
print("  ✅ PASS: qmdg_calc cũng ra 7/3\n")

# Test 3: Tử Vi — 15/01/1990 phải ra Kỷ Tỵ (1989), KHÔNG PHẢI Canh Ngọ (1990)
print("=" * 60)
print("TEST 3: Tử Vi Lunar Year (15/01/1990 → Kỷ Tỵ)")
print("=" * 60)
d3, m3, y3, leap3 = solar2lunar(15, 1, 1990)
print(f"  15/01/1990 DL = ngày {d3}/{m3}/{y3} ÂL")
can_idx = (y3 - 4) % 10
chi_idx = (y3 - 4) % 12
CAN = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
can_chi = f"{CAN[can_idx]} {CHI[chi_idx]}"
print(f"  Năm Can Chi (ÂL): {can_chi}")
assert CAN[can_idx] == "Kỷ", f"FAIL: Can phải là Kỷ, nhận được {CAN[can_idx]}"
assert CHI[chi_idx] == "Tỵ", f"FAIL: Chi phải là Tỵ, nhận được {CHI[chi_idx]}"
assert m3 == 12, f"FAIL: tháng ÂL phải là 12, nhận được {m3}"
assert y3 == 1989, f"FAIL: năm ÂL phải là 1989, nhận được {y3}"
print("  ✅ PASS: 15/01/1990 = Kỷ Tỵ (1989), tháng 12\n")

# Test 4: Tử Vi lap_la_so — dùng năm ÂL (1989) thay vì DL (1990)
print("=" * 60)
print("TEST 4: lap_la_so sử dụng năm Kỷ Tỵ (1989)")
print("=" * 60)
from tu_vi import lap_la_so
ls = lap_la_so(y3, m3, d3, 5, 'nam')  # Giờ Tỵ (idx 5)
print(f"  Năm sinh (truyền vào): {y3}")
print(f"  Can/Chi năm: {ls['can_nam']} {ls['chi_nam']}")
print(f"  Tứ Hóa: Lộc={ls['tu_hoa']['Hóa Lộc']}, Quyền={ls['tu_hoa']['Hóa Quyền']}, Khoa={ls['tu_hoa']['Hóa Khoa']}, Kỵ={ls['tu_hoa']['Hóa Kỵ']}")
assert ls['can_nam'] == "Kỷ", f"FAIL: Can phải là Kỷ, nhận được {ls['can_nam']}"
assert ls['chi_nam'] == "Tỵ", f"FAIL: Chi phải là Tỵ, nhận được {ls['chi_nam']}"
# Kỷ: Lộc=Vũ Khúc, Quyền=Tham Lang, Khoa=Thiên Lương, Kỵ=Văn Khúc
assert ls['tu_hoa']['Hóa Lộc'] == "Vũ Khúc", f"FAIL: Hóa Lộc Kỷ phải là Vũ Khúc"
assert ls['tu_hoa']['Hóa Quyền'] == "Tham Lang", f"FAIL: Hóa Quyền Kỷ phải là Tham Lang"
print("  ✅ PASS: Tử Vi dùng Kỷ Tỵ, Tứ Hóa theo Kỷ\n")

# Test 5: 28 Sao — 23/04/2026 phải ra Tỉnh (Mộc/Ngan)
print("=" * 60)
print("TEST 5: 28 Sao (Nhị Thập Bát Tú)")
print("=" * 60)
sao = tinh_28_tu(23, 4, 2026)
print(f"  23/04/2026 → Sao {sao[0]} ({sao[1]}/{sao[2]}) — {sao[3]}")
assert sao[0] == "Tỉnh", f"FAIL: phải là Tỉnh, nhận được {sao[0]}"
print("  ✅ PASS: 28 sao = Tỉnh Mộc Hãn\n")

# Test 6: Bổ sung — kiểm tra các ngày khác
print("=" * 60)
print("TEST 6: Kiểm tra bổ sung nhiều ngày")
print("=" * 60)

# 01/01/2026 (trước Tết)
d6, m6, y6, _ = solar2lunar(1, 1, 2026)
print(f"  01/01/2026 = {d6}/{m6}/{y6} ÂL")
can6 = CAN[(y6-4)%10]
chi6 = CHI[(y6-4)%12]
print(f"    → Năm {can6} {chi6}")
assert y6 == 2025, f"01/01/2026 phải thuộc ÂL 2025"
assert can6 == "Ất" and chi6 == "Tỵ", "Phải là Ất Tỵ"
print("  ✅ 01/01/2026 = năm Ất Tỵ (2025)")

# 17/02/2026 (mùng 1 Tết)
d7, m7, y7, _ = solar2lunar(17, 2, 2026)
print(f"  17/02/2026 = {d7}/{m7}/{y7} ÂL")
assert m7 == 1, f"17/02/2026 phải là tháng 1 ÂL"
print(f"  ✅ 17/02/2026 = mùng {d7} tháng {m7}")

print()
print("=" * 60)
print("🎉 TẤT CẢ TEST ĐÃ PASS! V42.8 FIX THÀNH CÔNG!")
print("=" * 60)

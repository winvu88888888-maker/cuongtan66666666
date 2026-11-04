# -*- coding: utf-8 -*-
"""Check Can Chi + 28 Sao accuracy"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xem_ngay_dep import _jdn, tinh_28_tu

CANS = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
CHIS = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']

# Check _jdn vs simple formula
print("=== JDN COMPARISON ===")
for dd, mm, yy in [(24,4,2026), (23,4,2026), (15,1,1990), (1,1,2026)]:
    j_acc = _jdn(dd, mm, yy)
    j_simple = int(365.25 * (yy + 4716)) + int(30.6001 * (mm + 1)) + dd - 1524
    can_acc = CANS[(j_acc + 9) % 10]
    chi_acc = CHIS[(j_acc + 1) % 12]
    can_sim = CANS[(j_simple + 9) % 10]
    chi_sim = CHIS[(j_simple + 1) % 12]
    diff = j_simple - j_acc
    print(f"  {dd:02d}/{mm:02d}/{yy}: accurate={can_acc} {chi_acc} (JDN={j_acc}) | simple={can_sim} {chi_sim} (JDN={j_simple}) | diff={diff}")

# Check 28 sao for a range of days
print()
print("=== 28 SAO: April 2026 ===")
for day in range(20, 28):
    s = tinh_28_tu(day, 4, 2026)
    name = s[0] if s else "?"
    print(f"  {day}/4/2026: {name}")

# Check app.py's inline Can/Chi calculation
print()
print("=== APP.PY INLINE Can/Chi (line 3303-3305) ===")
# _jdn = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day - 1524
# _cn = _cans[(_jdn + 9) % 10]
# _chi_n = _chis[(_jdn + 1) % 12]
# Problem: This simplified Julian Day formula is INACCURATE for Gregorian dates!
# It doesn't properly handle Gregorian-Julian calendar transition
# The correct JDN uses: correct month/year adjustment + century correction
print("This formula gives WRONG Can/Chi for the inline Xem Ngay section!")
print("The Can/Chi passed to danh_gia_ngay() will be WRONG -> wrong scoring!")

# Show impact: what Can/Chi does danh_gia_ngay receive vs what it should receive
from xem_ngay_dep import danh_gia_ngay, solar2lunar

dd, mm, yy = 24, 4, 2026
j_simple = int(365.25 * (yy + 4716)) + int(30.6001 * (mm + 1)) + dd - 1524
cn_wrong = CANS[(j_simple + 9) % 10]
chi_wrong = CHIS[(j_simple + 1) % 12]

j_acc = _jdn(dd, mm, yy)
cn_right = CANS[(j_acc + 9) % 10]
chi_right = CHIS[(j_acc + 1) % 12]

d_al, m_al, y_al, _ = solar2lunar(dd, mm, yy)

print(f"\n  Date: {dd}/{mm}/{yy} = AL {d_al}/{m_al}")
print(f"  WRONG Can/Chi (app.py inline): {cn_wrong} {chi_wrong}")
print(f"  RIGHT Can/Chi (xem_ngay_dep): {cn_right} {chi_right}")
print()

# Show scoring difference
xn_wrong = danh_gia_ngay(m_al, d_al, cn_wrong, chi_wrong, 'cuoi_hoi', ngay_dl=(dd, mm, yy))
xn_right = danh_gia_ngay(m_al, d_al, cn_right, chi_right, 'cuoi_hoi', ngay_dl=(dd, mm, yy))

print(f"  Score with WRONG Can/Chi: {xn_wrong['diem']}/100 - {xn_wrong['verdict']}")
print(f"  Score with RIGHT Can/Chi: {xn_right['diem']}/100 - {xn_right['verdict']}")
print(f"  Trực WRONG: {xn_wrong['truc']} | RIGHT: {xn_right['truc']}")
print(f"  28 sao WRONG: {xn_wrong.get('sao_28_tu', ['?'])[0]} | RIGHT: {xn_right.get('sao_28_tu', ['?'])[0]}")

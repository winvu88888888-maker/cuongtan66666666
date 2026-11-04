# test_count.py - Test COUNT logic V41.2
import sys
sys.path.insert(0, '.')
from van_vat_tong_hop import TRUONG_SINH_TRANG_THAI

hanh = 'Thổ'
HD_SO = {'Thủy': (1,6), 'Hỏa': (2,7), 'Mộc': (3,8), 'Kim': (4,9), 'Thổ': (5,10)}

print("=== TEST: Hoi 'may dua con' (DT=Tu Ton, Hanh=Tho) ===")
print(f"Ha Do: sinh={HD_SO[hanh][0]}, thanh={HD_SO[hanh][1]}")
print()

for ts in ['Trường Sinh', 'Lâm Quan', 'Đế Vượng', 'Suy', 'Tử']:
    d = TRUONG_SINH_TRANG_THAI.get(ts, {})
    so = d.get('so', '?')
    sl = d.get('so_luong', '?')
    print(f"  TS={ts}: so={so} | so_luong={sl}")

print()
print("=== KET LUAN ===")
print(f"Vuong (>=60%) -> thanh so = {HD_SO[hanh][1]}")
print(f"Binh (40-59%) -> sinh so  = {HD_SO[hanh][0]}")
print(f"Suy (<40%)    -> giam     = {max(1, HD_SO[hanh][0]-1)}")
print()

# Test all 5 hanh
print("=== HA DO CHO 5 HANH ===")
for h, (s, t) in HD_SO.items():
    print(f"  {h}: sinh={s}, thanh={t}")

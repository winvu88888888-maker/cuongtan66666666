"""Script to split van_vat_tong_hop into modular files"""
import sys, os, pprint

base = r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix'
sys.path.insert(0, base)
out_dir = os.path.join(base, 'van_vat')

from van_vat_tong_hop import TRUONG_SINH_TRANG_THAI, NGU_HANH_VAN_VAT
from van_vat_tong_hop import VAN_VAT_MO_RONG, VAN_VAT_BO_SUNG

pp = pprint.PrettyPrinter(indent=4, width=120)

# 1) truong_sinh.py
with open(os.path.join(out_dir, 'truong_sinh.py'), 'w', encoding='utf-8') as f:
    f.write('"""12 Trường Sinh - Trạng thái vật chất (dùng chung cho 5 hành)"""\n\n')
    f.write('TRUONG_SINH_TRANG_THAI = ')
    f.write(pp.pformat(TRUONG_SINH_TRANG_THAI))
    f.write('\n')
print('Written truong_sinh.py')

# 2) Per-element files
hanh_map = {
    'Kim': 'kim', 'Mộc': 'moc', 'Thủy': 'thuy', 'Hỏa': 'hoa', 'Thổ': 'tho'
}

for hanh, fname in hanh_map.items():
    core = NGU_HANH_VAN_VAT.get(hanh, {})
    mr = VAN_VAT_MO_RONG.get(hanh, {})
    bs = VAN_VAT_BO_SUNG.get(hanh, {})
    
    # Merge expanded
    expanded = {}
    expanded.update(mr)
    expanded.update(bs)
    
    filepath = os.path.join(out_dir, f'{fname}.py')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f'"""Vạn Vật — Hành {hanh} (CORE + EXPANDED)"""\n\n')
        f.write('# CORE: 5 giác quan, đồ vật theo 12 tầng, con người, bệnh, thú, cây\n')
        f.write('CORE = ')
        f.write(pp.pformat(core))
        f.write('\n\n')
        f.write('# EXPANDED: Phương tiện, Trang phục, Thực phẩm, Khoáng sản, Công nghệ...\n')
        f.write('EXPANDED = ')
        f.write(pp.pformat(expanded))
        f.write('\n')
    
    print(f'Written {fname}.py — CORE: {len(str(core))} chars, EXPANDED: {len(str(expanded))} chars')

print('\nAll module files created!')

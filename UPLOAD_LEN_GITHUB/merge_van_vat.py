# Script to merge van_vat files into one
import sys, os

base = r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix'
sys.path.insert(0, base)

# Read source files
with open(os.path.join(base, 'van_vat_chi_tiet.py'), 'r', encoding='utf-8') as f:
    c1 = f.read()
with open(os.path.join(base, 'van_vat_mo_rong.py'), 'r', encoding='utf-8') as f:
    c2 = f.read()

# Extract data from file 1: TRUONG_SINH + NGU_HANH (up to helper functions)
idx_helper = c1.index('# HELPER: L')
data1 = c1[:idx_helper]

# Extract data from file 2: VAN_VAT_MO_RONG + VAN_VAT_BO_SUNG
idx_helper2 = c2.index('# HELPER: MERGE')
# Find start of VAN_VAT_MO_RONG
idx_start2 = c2.index('VAN_VAT_MO_RONG = {')
data2 = c2[idx_start2:idx_helper2]

# Extract helper functions from file 1, fix imports
helpers = c1[idx_helper:]
helpers = helpers.replace(
    'from van_vat_mo_rong import VAN_VAT_MO_RONG, VAN_VAT_BO_SUNG',
    '# V31.6: Data already in this file (merged)')
helpers = helpers.replace(
    'from van_vat_mo_rong import VAN_VAT_MO_RONG',
    '# V31.6: Data already in this file (merged)')

# Build header
header = '''"""
van_vat_tong_hop.py \u2014 V31.6 V\u1ea0N V\u1eacT T\u1ed4NG H\u1ee2P (FILE DUY NH\u1ea4T)
\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550

G\u1ed9p T\u1ea4T C\u1ea2 d\u1eef li\u1ec7u V\u1ea1n V\u1eadt v\u00e0o 1 file duy nh\u1ea5t.
AI Offline + Online ch\u1ec9 c\u1ea7n import file n\u00e0y.

T\u1ed4NG: 2226+ items, bao g\u1ed3m:
- 12 TR\u01af\u1edcNG SINH \u2192 Tr\u1ea1ng th\u00e1i v\u1eadt ch\u1ea5t (138 items)
- 5 H\u00c0NH x \u0110\u1ed3 v\u1eadt/Ng\u01b0\u1eddi/B\u1ec7nh/Th\u00fa/C\u00e2y (670 items)
- 15 danh m\u1ee5c m\u1edf r\u1ed9ng x 5 H\u00e0nh (865 items)
- 10 danh m\u1ee5c b\u1ed5 sung x 5 H\u00e0nh (553 items)

Usage:
    from van_vat_tong_hop import (
        get_van_vat_chi_tiet, format_van_vat_for_ai, get_tham_tu_mo_ta,
    )

V31.6 \u2014 T\u1ea1o b\u1edfi AI Engine cho QMDG System.
"""

'''

# Remove old docstring from data1
if '"""' in data1:
    # Skip everything up to and including the closing """
    parts = data1.split('"""')
    # parts[0] is before first """, parts[1] is docstring content, parts[2:] is after
    if len(parts) >= 3:
        data1_clean = '"""'.join(parts[2:]).strip()
    else:
        data1_clean = data1.strip()
else:
    data1_clean = data1.strip()

merged = header + data1_clean + '\n\n\n' + data2.strip() + '\n\n\n' + helpers.strip() + '\n'

# Write output
out_path = os.path.join(base, 'van_vat_tong_hop.py')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(merged)

print(f"Created: {out_path}")
print(f"Size: {len(merged)} bytes, {merged.count(chr(10))} lines")

# Verify
import py_compile
py_compile.compile(out_path, doraise=True)
print("Syntax OK!")

# Verify imports work
exec(open(out_path, encoding='utf-8').read())
print("All data loaded OK!")

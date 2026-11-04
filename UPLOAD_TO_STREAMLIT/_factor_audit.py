"""Kiểm tra CHI TIẾT số yếu tố trong Knowledge Tree vs thực tế"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from divination_knowledge_tree import TREE

print("=" * 80)
print("🔍 KIỂM TRA CHI TIẾT YẾU TỐ TRONG KNOWLEDGE TREE")
print("=" * 80)

def count_all_keys(d, depth=0, prefix=""):
    """Đếm TẤT CẢ keys ở mọi tầng"""
    total = 0
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            if k in ('name', 'desc', 'verdict', 'vi_du', 'so', 'huong', 'tuong', 'hanh'):
                continue  # Skip metadata keys
            total += 1
            sub_count = 0
            if isinstance(v, dict) and len(v) > 0:
                # Check if it's a leaf or branch
                has_children = any(isinstance(vv, dict) for vv in v.values())
                if has_children:
                    sub_count, sub_items = count_all_keys(v, depth+1, f"{prefix}.{k}")
            items.append((k, sub_count))
    return total, items

for method_key in ['LH', 'KM', 'MH', 'LN', 'TA', 'TB', 'TV', 'XND']:
    if method_key not in TREE:
        print(f"\n❌ [{method_key}] KHÔNG TỒN TẠI!")
        continue
    
    t = TREE[method_key]
    name = t.get('name', '?')
    print(f"\n{'='*60}")
    print(f"📋 [{method_key}] {name}")
    print(f"{'='*60}")
    
    # Count top-level sections
    sections = [k for k in t.keys() if k not in ('name', 'desc')]
    print(f"  📂 Sections: {len(sections)}")
    
    total_factors = 0
    for section_key in sections:
        section = t[section_key]
        if isinstance(section, dict):
            items = len(section)
            # Count sub-items
            sub_total = 0
            for sk, sv in section.items():
                if isinstance(sv, dict):
                    sub_total += len(sv)
                elif isinstance(sv, list):
                    sub_total += len(sv)
            
            if section_key == 'interpretation_steps':
                print(f"  📝 {section_key}: {items} bước luận giải")
            elif section_key == 'verdict_rules':
                cat = len(section.get('CAT', []))
                hung = len(section.get('HUNG', []))
                binh = len(section.get('BINH', []))
                print(f"  ⚖️ {section_key}: CÁT={cat}, HUNG={hung}, BÌNH={binh}")
            else:
                total_factors += items
                detail_items = []
                for sk in list(section.keys())[:8]:
                    sv = section[sk]
                    if isinstance(sv, dict):
                        detail_items.append(f"{sk}({len(sv)})")
                    elif isinstance(sv, list):
                        detail_items.append(f"{sk}[{len(sv)}]")
                    else:
                        detail_items.append(sk)
                extra = "..." if len(section) > 8 else ""
                print(f"  📦 {section_key}: {items} items → {', '.join(detail_items)}{extra}")
        elif isinstance(section, list):
            total_factors += len(section)
            print(f"  📦 {section_key}: {len(section)} items (list)")
    
    print(f"  ═══ TỔNG YẾU TỐ: {total_factors}")

# ═══════════════════════════════════════════
# KIỂM TRA CỤ THỂ TỪNG PP
# ═══════════════════════════════════════════
print("\n\n" + "=" * 80)
print("🔬 SO SÁNH VỚI YÊU CẦU THỰC TẾ")
print("=" * 80)

# KỲ MÔN: Cần có 44 yếu tố
print("\n📋 [KM] KỲ MÔN ĐỘN GIÁP — Yêu cầu ~44 yếu tố:")
km = TREE.get('KM', {})
KM_REQUIRED = {
    'cuu_tinh': ('9 Cửu Tinh', 9),
    'bat_mon': ('8 Bát Môn', 8),
    'bat_than': ('8 Bát Thần', 8),
    'thien_can': ('10 Thiên Can', 10),
    'dia_chi': ('12 Địa Chi', 12),
    'cuu_cung': ('9 Cửu Cung', 9),
    'luc_nghi': ('6 Lục Nghi', 6),
    'tam_ky': ('3 Tam Kỳ', 3),
    'bat_quai': ('8 Bát Quái', 8),
}
km_total = 0
for key, (label, expected) in KM_REQUIRED.items():
    actual = len(km.get(key, {}))
    status = "✅" if actual >= expected else "❌"
    print(f"  {status} {label}: {actual}/{expected}")
    km_total += actual

print(f"  ═══ TỔNG: {km_total} yếu tố (mục tiêu: ~44+)")

# LỤC HÀO: Cần có đủ yếu tố
print("\n📋 [LH] LỤC HÀO KINH DỊCH — Yêu cầu:")
lh = TREE.get('LH', {})
LH_REQUIRED = {
    'luc_than': ('6 Lục Thân', 6),
    'luc_thu': ('6 Lục Thú', 6),
    'ngu_hanh': ('5 Ngũ Hành', 5),
    'ung_ky': ('Ứng Kỳ', 1),
    'the_ung': ('Thế Ứng', 1),
    'dong_hao': ('Động Hào', 1),
    'hoa_hao': ('Hóa Hào', 1),
}
lh_total = 0
for key, (label, expected) in LH_REQUIRED.items():
    actual = len(lh.get(key, {})) if isinstance(lh.get(key), dict) else (1 if key in lh else 0)
    status = "✅" if actual >= expected else "❌"
    print(f"  {status} {label}: {actual}/{expected}")
    lh_total += actual

print(f"  ═══ TỔNG: {lh_total} yếu tố")

# MAI HOA: Cần có đủ yếu tố
print("\n📋 [MH] MAI HOA DỊCH SỐ — Yêu cầu:")
mh = TREE.get('MH', {})
MH_REQUIRED = {
    'the_dung_quan_he': ('Thể Dụng quan hệ', 3),
    'bat_quai': ('8 Bát Quái', 8),
    'ngu_hanh_sinh_khac': ('Ngũ Hành Sinh Khắc', 2),
}
mh_total = 0
for key, (label, expected) in MH_REQUIRED.items():
    actual = len(mh.get(key, {})) if isinstance(mh.get(key), dict) else 0
    status = "✅" if actual >= expected else "❌"
    print(f"  {status} {label}: {actual}/{expected}")
    mh_total += actual

print(f"  ═══ TỔNG: {mh_total} yếu tố")

# ĐẠI LỤC NHÂM
print("\n📋 [LN] ĐẠI LỤC NHÂM — Yêu cầu:")
ln = TREE.get('LN', {})
for key in [k for k in ln.keys() if k not in ('name', 'desc', 'interpretation_steps', 'verdict_rules')]:
    val = ln[key]
    count = len(val) if isinstance(val, (dict, list)) else 1
    print(f"  📦 {key}: {count} items")

# THÁI ẤT
print("\n📋 [TA] THÁI ẤT THẦN SỐ — Yêu cầu:")
ta = TREE.get('TA', {})
for key in [k for k in ta.keys() if k not in ('name', 'desc', 'interpretation_steps', 'verdict_rules')]:
    val = ta[key]
    count = len(val) if isinstance(val, (dict, list)) else 1
    print(f"  📦 {key}: {count} items")

# THIẾT BẢN
print("\n📋 [TB] THIẾT BẢN THẦN SỐ — Yêu cầu:")
tb = TREE.get('TB', {})
for key in [k for k in tb.keys() if k not in ('name', 'desc', 'interpretation_steps', 'verdict_rules')]:
    val = tb[key]
    count = len(val) if isinstance(val, (dict, list)) else 1
    print(f"  📦 {key}: {count} items")

# TỬ VI
print("\n📋 [TV] TỬ VI ĐẨU SỐ — Yêu cầu:")
tv = TREE.get('TV', {})
for key in [k for k in tv.keys() if k not in ('name', 'desc', 'interpretation_steps', 'verdict_rules')]:
    val = tv[key]
    count = len(val) if isinstance(val, (dict, list)) else 1
    print(f"  📦 {key}: {count} items")

# XEM NGÀY
print("\n📋 [XND] XEM NGÀY ĐẸP — Yêu cầu:")
xnd = TREE.get('XND', {})
for key in [k for k in xnd.keys() if k not in ('name', 'desc', 'interpretation_steps', 'verdict_rules')]:
    val = xnd[key]
    count = len(val) if isinstance(val, (dict, list)) else 1
    print(f"  📦 {key}: {count} items")

# ═══════════════════════════════════════════
# KIỂM TRA qmdg_data.py (nguồn chính Kỳ Môn)
# ═══════════════════════════════════════════
print("\n\n" + "=" * 80)
print("🔬 KIỂM TRA DỮ LIỆU GỐC (qmdg_data.py)")
print("=" * 80)
try:
    from qmdg_data import KY_MON_DATA
    main_keys = list(KY_MON_DATA.keys())
    print(f"  KY_MON_DATA keys ({len(main_keys)}): {main_keys[:10]}...")
    
    # Chi tiết
    for mk in main_keys[:15]:
        val = KY_MON_DATA[mk]
        if isinstance(val, dict):
            print(f"    📦 {mk}: {len(val)} items")
        elif isinstance(val, list):
            print(f"    📦 {mk}: {len(val)} items (list)")
        else:
            print(f"    📦 {mk}: {type(val).__name__}")
except Exception as e:
    print(f"  ❌ {e}")

# ═══════════════════════════════════════════
# KIỂM TRA kinh_dich_64_que.py
# ═══════════════════════════════════════════
print("\n📦 KIỂM TRA kinh_dich_64_que.py:")
try:
    from kinh_dich_64_que import KINH_DICH_64, MAI_HOA_THE_DUNG, MAI_HOA_UNG_KY, THIET_BAN_60
    print(f"  ✅ KINH_DICH_64: {len(KINH_DICH_64)} quẻ")
    print(f"  ✅ MAI_HOA_THE_DUNG: {len(MAI_HOA_THE_DUNG)} items")
    print(f"  ✅ MAI_HOA_UNG_KY: {len(MAI_HOA_UNG_KY)} items")
    print(f"  ✅ THIET_BAN_60: {len(THIET_BAN_60)} nạp âm")
except Exception as e:
    print(f"  ❌ {e}")

print("\n" + "=" * 80)
print("DONE")

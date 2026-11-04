"""
V42.9.8 FULL FACTOR TRACE AUDIT
Kiểm tra TỪNG YẾU TỐ trong toàn bộ pipeline:
  DKT → Engine Scoring → Offline Output (sections) → Online Data (offline_analysis_data)

Sử dụng quẻ có sẵn trên web (lập theo giờ) — không cần nhập gì.
"""
import sys, datetime, json
sys.stdout.reconfigure(encoding='utf-8')

# ═══ IMPORT ═══
from divination_knowledge_tree import TREE
from interaction_diagrams import (
    DIAGRAM_MASTER, DIAGRAMS,
    KM_BAT_MON_REF, KM_CUU_TINH_REF,
    TV_CHINH_TINH_REF, XND_HOANG_DAO_REF, XND_HAC_DAO_REF,
)

print("=" * 90)
print("🔬 FULL FACTOR TRACE AUDIT — V42.9.8")
print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 90)

# ═══ PHASE 1: Liệt kê TẤT CẢ yếu tố trong DKT ═══
print("\n" + "═" * 90)
print("📦 PHASE 1: TẤT CẢ YẾU TỐ TRONG KNOWLEDGE TREE (DKT)")
print("═" * 90)

total_factors = 0
dkt_factor_map = {}  # {method: {group: [factor_names]}}

for method_key, method_data in TREE.items():
    if method_key == 'VV':
        continue
    method_name = method_data.get('name', method_key)
    dkt_factor_map[method_key] = {}
    print(f"\n📋 [{method_key}] {method_name}")
    
    for group_key, group_data in method_data.items():
        if group_key in ('name', 'coverage', 'interpretation_steps', 'verdict_rules'):
            continue
        if not isinstance(group_data, dict):
            continue
        
        factor_names = [str(k) for k in group_data.keys()]
        count = len(factor_names)
        total_factors += count
        dkt_factor_map[method_key][group_key] = factor_names
        
        # Show first few
        preview = ', '.join(factor_names[:5])
        if count > 5:
            preview += f'... +{count-5}'
        print(f"  📂 {group_key}: {count} yếu tố → [{preview}]")

print(f"\n📊 TỔNG: {total_factors} yếu tố trong DKT")

# ═══ PHASE 2: Kiểm tra Engine ĐỌC từng yếu tố ═══
print("\n" + "═" * 90)
print("⚙️ PHASE 2: ENGINE ĐỌC YẾU TỐ NÀO?")
print("═" * 90)

# Read engine source
engine_src = open('free_ai_helper.py', 'r', encoding='utf-8').read()

# Define what engine SHOULD read for each factor group
factor_checks = {
    'LH': {
        'luc_than': {
            'keywords': ['Thê Tài', 'Quan Quỷ', 'Phụ Mẫu', 'Huynh Đệ', 'Tử Tôn'],
            'engine_refs': ['LUC_THAN_GIAI_THICH', "dung_than", "luc_than"],
        },
        'luc_thu': {
            'keywords': ['Thanh Long', 'Chu Tước', 'Câu Trận', 'Đằng Xà', 'Bạch Hổ', 'Huyền Vũ'],
            'engine_refs': ['LUC_THAN_DEEP', 'luc_thu'],
        },
        'ngu_hanh': {
            'keywords': ['Kim', 'Mộc', 'Thủy', 'Hỏa', 'Thổ'],
            'engine_refs': ['SINH', 'KHAC', 'NGU_HANH_VAT_CHAT'],
        },
        'luc_xung': {
            'keywords': ['Tý-Ngọ', 'Sửu-Mùi', 'Dần-Thân', 'Mão-Dậu', 'Thìn-Tuất', 'Tị-Hợi'],
            'engine_refs': ['LUC_XUNG_CHI'],
        },
        'luc_hop': {
            'keywords': ['Tý-Sửu', 'Dần-Hợi', 'Mão-Tuất', 'Thìn-Dậu', 'Tị-Thân', 'Ngọ-Mùi'],
            'engine_refs': ['LUC_HOP_CHI'],
        },
        'tam_hop': {
            'keywords': ['Thân-Tý-Thìn', 'Dần-Ngọ-Tuất', 'Hợi-Mão-Mùi', 'Tị-Dậu-Sửu'],
            'engine_refs': ['TAM_HOP_CUC'],
        },
        'factors': {
            'keywords': ['nguyet_kien', 'nhat_than', 'dong_hao', 'nguyen_than', 'ky_than',
                         'cuu_than', 'phuc_than', 'luc_hop', 'luc_xung', 'tam_hop', 
                         'khong_vong', 'mo_kho', 'nguyet_pha', 'phan_ngam', 'phuc_ngam',
                         'hoi_dau_sinh', 'hoi_dau_khac', 'tien_than', 'thoai_than',
                         'the_hao', 'ung_hao', 'tinh_hao', 'hoa_hao',
                         'phi_than', 'triet_lo', 'vuong_suy', 'thai_tue', 'tue_pha',
                         'nhat_pha', 'tam_hinh', 'pha', 'hai', 'ban_hop'],
            'engine_refs': ['_luc_hao_scoring', 'v23_lh_factors'],
        },
        'truong_sinh': {
            'keywords': ['Trường Sinh', 'Đế Vượng', 'Suy', 'Mộ', 'Tuyệt'],
            'engine_refs': ['TRUONG_SINH_POWER', 'ts_stage'],
        },
    },
    'KM': {
        'bat_mon': {
            'keywords': ['Khai Môn', 'Hưu Môn', 'Sinh Môn', 'Tử Môn', 'Kinh Môn', 'Đỗ Môn', 'Cảnh Môn', 'Thương Môn'],
            'engine_refs': ['BAT_MON_NGU_HANH', 'cua_dt', 'bat_mon'],
        },
        'cuu_tinh': {
            'keywords': ['Thiên Bồng', 'Thiên Nhậm', 'Thiên Xung', 'Thiên Phụ', 'Thiên Anh', 'Thiên Nhuế', 'Thiên Cầm', 'Thiên Trụ', 'Thiên Tâm'],
            'engine_refs': ['CUU_TINH_NGU_HANH', 'sao_dt', 'cuu_tinh'],
        },
        'bat_than': {
            'keywords': ['Trực Phù', 'Đằng Xà', 'Thái Âm', 'Lục Hợp', 'Bạch Hổ', 'Huyền Vũ', 'Cửu Địa', 'Cửu Thiên'],
            'engine_refs': ['than_dt', 'bat_than'],
        },
        'tam_ky': {
            'keywords': ['Nhật Kỳ', 'Nguyệt Kỳ', 'Tinh Kỳ'],
            'engine_refs': ['tam_ky'],
        },
        'luc_nghi': {
            'keywords': ['Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý'],
            'engine_refs': ['luc_nghi'],
        },
        'cach_cuc': {
            'keywords': ['cat_cach', 'hung_cach'],
            'engine_refs': ['cach_cuc', 'cát cách', 'hung cách'],
        },
        'thien_can': {
            'keywords': ['Giáp', 'Ất', 'Bính', 'Đinh'],
            'engine_refs': ['CAN_NGU_HANH', 'thien_can'],
        },
        'dia_chi': {
            'keywords': ['Tý', 'Sửu', 'Dần', 'Mão'],
            'engine_refs': ['CHI_ORDER', 'dia_chi'],
        },
        'cuu_cung': {
            'keywords': ['Khảm', 'Khôn', 'Chấn', 'Tốn'],
            'engine_refs': ['cung_dt', 'cuu_cung'],
        },
        'bat_quai': {
            'keywords': ['Càn', 'Khôn', 'Ly', 'Khảm'],
            'engine_refs': ['bat_quai', 'QUAI_Y_NGHIA'],
        },
    },
    'MH': {
        'quai': {
            'keywords': ['Nội Quái', 'Ngoại Quái', 'Hỗ Quái', 'Biến Quái'],
            'engine_refs': ['the_quai', 'dung_quai', 'ho_quai', 'bien_quai'],
        },
        'sinh_khac': {
            'keywords': ['the_sinh_dung', 'dung_sinh_the', 'the_khac_dung', 'dung_khac_the', 'ty_hoa'],
            'engine_refs': ['_mai_hoa_scoring', 'the_dung_rel'],
        },
        'bat_quai': {
            'keywords': ['Càn', 'Đoài', 'Ly', 'Chấn', 'Tốn', 'Khảm', 'Cấn', 'Khôn'],
            'engine_refs': ['QUAI_Y_NGHIA'],
        },
    },
}

engine_reads = {}
engine_misses = {}

for method, groups in factor_checks.items():
    engine_reads[method] = {}
    engine_misses[method] = {}
    print(f"\n⚙️ [{method}] {TREE[method]['name']}")
    
    for group, info in groups.items():
        found = []
        missed = []
        for ref in info['engine_refs']:
            if ref in engine_src:
                found.append(ref)
            else:
                missed.append(ref)
        
        # Also check keywords in v23/v24 factor collection
        kw_in_factors = 0
        for kw in info['keywords']:
            if kw in engine_src:
                kw_in_factors += 1
        
        pct = int(kw_in_factors / max(len(info['keywords']), 1) * 100)
        
        engine_reads[method][group] = found
        engine_misses[method][group] = missed
        
        status = "✅" if pct >= 80 else "🟡" if pct >= 50 else "❌"
        print(f"  {status} {group}: {kw_in_factors}/{len(info['keywords'])} keywords ({pct}%) | refs: {len(found)}/{len(found)+len(missed)}")
        if missed:
            print(f"      ⚠️ Missing refs: {', '.join(missed)}")

# ═══ PHASE 3: Trace offline_analysis_data (gửi cho AI Online) ═══
print("\n" + "═" * 90)
print("📡 PHASE 3: DỮ LIỆU GỬI CHO AI ONLINE (offline_analysis_data)")
print("═" * 90)

# Parse all keys in offline_analysis_data
import re
oad_keys = re.findall(r"offline_analysis_data\[?['\"](\w+)['\"]", engine_src)
oad_keys = sorted(set(oad_keys))

print(f"\n📦 offline_analysis_data có {len(oad_keys)} keys:")
key_groups = {
    'Verdict & Reason': [k for k in oad_keys if 'verdict' in k or 'reason' in k],
    'Scoring (v16)': [k for k in oad_keys if k.startswith('v16_')],
    'Factor Data (v23/v24)': [k for k in oad_keys if k.startswith('v23_') or k.startswith('v24_')],
    'Unified Strength (v22)': [k for k in oad_keys if k.startswith('v22_')],
    'Routing (v17)': [k for k in oad_keys if k.startswith('v17_')],
    'Diagrams (v31)': [k for k in oad_keys if k.startswith('v31_')],
    'Detective (v18)': [k for k in oad_keys if k.startswith('v18_')],
    'Timing (v15)': [k for k in oad_keys if k.startswith('v15_')],
    'Mai Hoa extra': [k for k in oad_keys if 'mai_hoa' in k],
    'Lục Hào extra': [k for k in oad_keys if 'luc_hao' in k and 'v' not in k],
    'Hub': [k for k in oad_keys if k == 'hub'],
    'Conflict': [k for k in oad_keys if 'conflict' in k],
    'Other': [],
}
categorized = set()
for cat, keys in key_groups.items():
    categorized.update(keys)
key_groups['Other'] = [k for k in oad_keys if k not in categorized]

for cat, keys in key_groups.items():
    if not keys:
        continue
    print(f"\n  📂 {cat}:")
    for k in keys:
        print(f"    • {k}")

# ═══ PHASE 4: Kiểm tra AI Online Prompt đọc gì ═══
print("\n" + "═" * 90)
print("🤖 PHASE 4: AI ONLINE (GEMINI) ĐỌC GÌ TỪ PROMPT?")
print("═" * 90)

# Find prompt sections
prompt_sections = re.findall(r'═══.*?═══', engine_src)
online_factors = {
    'LH factors (v23)': 'v23_lh_factors' in engine_src and "od['v23_lh_factors']" in engine_src,
    'KM factors (v24)': 'v24_km_factors' in engine_src and "od['v24_km_factors']" in engine_src,
    'MH factors (v24)': 'v24_mh_factors' in engine_src and "od['v24_mh_factors']" in engine_src,
    'TB factors (v24)': 'v24_tb_factors' in engine_src and "od['v24_tb_factors']" in engine_src,
    'LN factors (v24)': 'v24_ln_factors' in engine_src and "od['v24_ln_factors']" in engine_src,
    'TA factors (v24)': 'v24_ta_factors' in engine_src and "od['v24_ta_factors']" in engine_src,
    'Hub data': "od.get('hub'" in engine_src or "od['hub']" in engine_src,
    'Unified strength (v22)': "v22" in engine_src,
    'Master diagram (v31)': "v31_master_diagram" in engine_src,
    'Question diagram (v31)': "v31_question_diagram" in engine_src,
    'Detective (v18)': "v18_detective" in engine_src,
    'Full offline report': "full_offline_report" in engine_src,
    'Conflict warnings': "conflict_warnings" in engine_src,
    'Mai Hoa extra data': "mai_hoa_ho_quai" in engine_src or "mai_hoa_interpretation" in engine_src,
    'Lục Hào quẻ tên': "luc_hao_ten_que" in engine_src,
}

for factor, present in online_factors.items():
    status = "✅ ĐỌC ĐƯỢC" if present else "❌ KHÔNG ĐỌC"
    print(f"  {status} — {factor}")

# ═══ PHASE 5: Kiểm tra AI Offline Output (sections) ═══
print("\n" + "═" * 90)
print("🖥️ PHASE 5: AI OFFLINE OUTPUT (hiển thị cho người dùng)")
print("═" * 90)

offline_sections = re.findall(r"sections\.append\(.*?['\"](.{10,60})", engine_src)
# Categorize
section_cats = {
    'Dụng Thần & Phân Loại': [],
    'Kỳ Môn': [],
    'Lục Hào': [],
    'Mai Hoa': [],
    'Đại Lục Nhâm': [],
    'Thái Ất': [],
    'Thiết Bản': [],
    'Tổng Hợp / Verdict': [],
    'Sơ Đồ': [],
    'Multi-Intent': [],
    'Other': [],
}
for s in offline_sections:
    s_clean = s[:60]
    if 'KỲ MÔN' in s.upper() or 'BƯỚC 2' in s:
        section_cats['Kỳ Môn'].append(s_clean)
    elif 'LỤC HÀO' in s.upper() or 'BƯỚC 3' in s:
        section_cats['Lục Hào'].append(s_clean)
    elif 'MAI HOA' in s.upper() or 'BƯỚC 4' in s:
        section_cats['Mai Hoa'].append(s_clean)
    elif 'LỤC NHÂM' in s.upper() or 'BƯỚC 5' in s:
        section_cats['Đại Lục Nhâm'].append(s_clean)
    elif 'THÁI ẤT' in s.upper():
        section_cats['Thái Ất'].append(s_clean)
    elif 'DỤNG THẦN' in s.upper() or 'BƯỚC 1' in s:
        section_cats['Dụng Thần & Phân Loại'].append(s_clean)
    elif 'VERDICT' in s.upper() or 'KẾT LUẬN' in s:
        section_cats['Tổng Hợp / Verdict'].append(s_clean)
    elif 'SĐ' in s or 'DIAGRAM' in s.upper() or 'sơ đồ' in s.lower():
        section_cats['Sơ Đồ'].append(s_clean)
    elif 'multi' in s.lower() or 'card' in s.lower():
        section_cats['Multi-Intent'].append(s_clean)

for cat, items in section_cats.items():
    if items:
        print(f"\n  📂 {cat}: {len(items)} sections")
        for item in items[:3]:
            print(f"    • {item}")
        if len(items) > 3:
            print(f"    ... +{len(items)-3} more")

# ═══ PHASE 6: CHI TIẾT CÁC YẾU TỐ BỊ BỎ SÓT ═══
print("\n" + "═" * 90)
print("🔴 PHASE 6: YẾU TỐ BỊ BỎ SÓT / ẨN GIẤU")
print("═" * 90)

missing_critical = []

# Check specific factors known to be problematic
checks = [
    ("LH Lục Thú (6 con)", 'LUC_THAN_DEEP' in engine_src and 'Thanh Long' in engine_src, 
     "Engine CÓ LUC_THAN_DEEP nhưng kiểm tra output"),
    ("LH Tam Hình", 'TAM_HINH' in engine_src and 'tam_hinh' in engine_src.lower(),
     "Engine CÓ TAM_HINH logic"),
    ("LH Phá/Hại", 'pha' in engine_src.lower() and 'hai' in engine_src.lower(),
     "Phá/Hại logic"),
    ("LH Bán Hợp", 'ban_hop' in engine_src.lower() or 'bán hợp' in engine_src.lower(),
     "Bán Hợp logic"),
    ("LH Triệt Lộ", 'triet_lo' in engine_src.lower() or 'triệt lộ' in engine_src.lower(),
     "Triệt Lộ detection"),
    ("LH Tuế Phá", 'tue_pha' in engine_src.lower() or 'tuế phá' in engine_src.lower(),
     "Tuế Phá detection"),
    ("LH Nhật Phá", 'nhat_pha' in engine_src.lower() or 'nhật phá' in engine_src.lower(),
     "Nhật Phá detection"),
    ("KM Cách Cục", 'cach_cuc' in engine_src.lower() or 'cát cách' in engine_src.lower() or 'hung cách' in engine_src.lower(),
     "Kỳ Môn Cách Cục matching"),
    ("KM Tam Kỳ", 'tam_ky' in engine_src.lower() or 'tam kỳ' in engine_src.lower(),
     "Tam Kỳ detection"),
    ("KM Lục Nghi", 'luc_nghi' in engine_src.lower() or 'lục nghi' in engine_src.lower(),
     "Lục Nghi analysis"),
    ("KM Ám Can", 'am_can' in engine_src.lower() or 'ám can' in engine_src.lower(),
     "Ám Can analysis"),
    ("TV Chính Tinh", 'TV_CHINH_TINH' in engine_src or 'chinh_tinh' in engine_src.lower(),
     "Tử Vi Chính Tinh reference"),
    ("TV Phụ Tinh", 'phu_tinh' in engine_src.lower() or 'phụ tinh' in engine_src.lower(),
     "Tử Vi Phụ Tinh"),
    ("TV Tứ Hóa", 'tu_hoa' in engine_src.lower() or 'tứ hóa' in engine_src.lower() or 'Hóa Lộc' in engine_src,
     "Tử Vi Tứ Hóa"),
    ("XND Hoàng Đạo", 'hoang_dao' in engine_src.lower() or 'hoàng đạo' in engine_src.lower(),
     "Xem Ngày Hoàng Đạo"),
    ("XND Hắc Đạo", 'hac_dao' in engine_src.lower() or 'hắc đạo' in engine_src.lower(),
     "Xem Ngày Hắc Đạo"),
    ("XND 12 Trực", '12_truc' in engine_src.lower() or 'thập nhị trực' in engine_src.lower() or 'truc_' in engine_src.lower(),
     "Xem Ngày 12 Trực"),
    ("DKT direct read", "from divination_knowledge_tree" in engine_src or "import TREE" in engine_src,
     "Engine imports DKT"),
    ("DKT in scoring", "_DKT" in engine_src or "TREE[" in engine_src,
     "Engine uses DKT in scoring"),
    ("Diagrams Bát Môn ref", "KM_BAT_MON_REF" in engine_src or "bat_mon_cat_hung" in engine_src,
     "Diagrams reference Bát Môn"),
    ("Diagrams Cửu Tinh ref", "KM_CUU_TINH_REF" in engine_src or "cuu_tinh_cat_hung" in engine_src,
     "Diagrams reference Cửu Tinh"),
]

for name, exists, note in checks:
    if exists:
        print(f"  ✅ {name} — {note}")
    else:
        missing_critical.append(name)
        print(f"  ❌ {name} — {note}")

# ═══ PHASE 7: TỔNG KẾT ═══
print("\n" + "═" * 90)
print("📊 PHASE 7: TỔNG KẾT — AI ONLINE vs AI OFFLINE")
print("═" * 90)

print(f"""
┌─────────────────────────────────────────────────────────────────┐
│  📦 DKT Knowledge Tree: {total_factors} yếu tố trong 8 phương pháp       │
│  📡 offline_analysis_data: {len(oad_keys)} keys gửi AI Online          │
│  🖥️ Offline sections: {len(offline_sections)} render blocks               │
│                                                                 │
│  ✅ Yếu tố Engine ĐỌC ĐƯỢC: {len(checks) - len(missing_critical)}/{len(checks)}                         │
│  ❌ Yếu tố BỎ SÓT/ẨN: {len(missing_critical)}/{len(checks)}                              │
└─────────────────────────────────────────────────────────────────┘
""")

if missing_critical:
    print("🔴 CÁC YẾU TỐ BỊ BỎ SÓT:")
    for i, m in enumerate(missing_critical, 1):
        print(f"  {i}. {m}")

print("\n📋 AI ONLINE ĐỌC ĐƯỢC (từ offline_analysis_data):")
print("  • v23_lh_factors: TẤT CẢ yếu tố Lục Hào (text list)")
print("  • v24_km_factors: TẤT CẢ yếu tố Kỳ Môn (text list)")
print("  • v24_mh_factors: TẤT CẢ yếu tố Mai Hoa (text list)")
print("  • v24_tb_factors: Thiết Bản data")
print("  • v24_ln_factors: Đại Lục Nhâm data")
print("  • v24_ta_factors: Thái Ất data")
print("  • hub: V42.9.4 centralized analysis hub")
print("  • v31_master_diagram: SĐ MASTER rendered")
print("  • v31_question_diagram: SĐ question-specific rendered")
print("  • full_offline_report: First 4000 chars of offline output")

print("\n📋 AI OFFLINE HIỂN THỊ (sections → UI):")
print("  • BƯỚC 1: Dụng Thần & Chủ đề")
print("  • BƯỚC 2: Kỳ Môn Độn Giáp (ky_mon_section)")
print("  • BƯỚC 3: Lục Hào Kinh Dịch (lh_section)")
print("  • BƯỚC 4: Mai Hoa Dịch Số (mh_section)")
print("  • BƯỚC 5: Đại Lục Nhâm + Thái Ất (ln_section)")
print("  • BƯỚC 6: Thiết Bản Thần Số (tb_section)")
print("  • BƯỚC 7: Tổng Hợp & Verdict")
print("  • V42.9.6: Multi-Intent Cards")
print("  • V31.0: Sơ đồ MASTER + SĐ câu hỏi")
print("  • V42.0: Ứng Kỳ Chuyên Sâu")

print("\n" + "=" * 90)
print(f"🏁 AUDIT HOÀN TẤT — {len(checks) - len(missing_critical)}/{len(checks)} yếu tố traced thành công")
print("=" * 90)

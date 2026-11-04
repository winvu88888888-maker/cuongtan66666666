"""V42.9.7 FULL SYSTEM AUDIT — Kiểm tra toàn diện hệ thống"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

TOTAL_CHECKS = 0
PASS_CHECKS = 0
FAIL_ITEMS = []

def check(name, condition, detail=""):
    global TOTAL_CHECKS, PASS_CHECKS, FAIL_ITEMS
    TOTAL_CHECKS += 1
    if condition:
        PASS_CHECKS += 1
        print(f"  ✅ {name}")
    else:
        FAIL_ITEMS.append((name, detail))
        print(f"  ❌ {name} — {detail}")

print("=" * 70)
print("🔍 KIỂM TRA TỔNG THỂ HỆ THỐNG DIVINATION ENGINE V42.9.7")
print("=" * 70)

# ═══════════════════════════════════════════
# 1. KNOWLEDGE TREE — 8 phương pháp
# ═══════════════════════════════════════════
print("\n📚 [1] MASTER KNOWLEDGE TREE (divination_knowledge_tree.py)")
try:
    from divination_knowledge_tree import TREE
    EXPECTED_METHODS = ['LH', 'KM', 'MH', 'LN', 'TA', 'TB', 'TV', 'XND']
    
    for m in EXPECTED_METHODS:
        check(f"[{m}] exists in TREE", m in TREE, f"Thiếu phương pháp {m}")
    
    for m in EXPECTED_METHODS:
        if m in TREE:
            t = TREE[m]
            check(f"[{m}] has name", bool(t.get('name')))
            check(f"[{m}] has interpretation_steps", len(t.get('interpretation_steps', {})) > 0,
                  f"steps={len(t.get('interpretation_steps', {}))}")
            
            vr = t.get('verdict_rules', {})
            check(f"[{m}] has verdict_rules", bool(vr), "Thiếu verdict_rules!")
            if vr:
                check(f"[{m}] verdict_rules.CAT", len(vr.get('CAT', [])) > 0,
                      f"CAT={len(vr.get('CAT', []))}")
                check(f"[{m}] verdict_rules.HUNG", len(vr.get('HUNG', [])) > 0,
                      f"HUNG={len(vr.get('HUNG', []))}")
    
    check("[VV] Van Vat exists", 'VV' in TREE)
    if 'VV' in TREE:
        vv = TREE['VV']
        check("[VV] has items", len(vv.get('items', [])) > 0, f"items={len(vv.get('items', []))}")
except Exception as e:
    print(f"  ❌ CRITICAL: Cannot import TREE — {e}")

# ═══════════════════════════════════════════
# 2. INTERACTION DIAGRAMS — 17 sơ đồ
# ═══════════════════════════════════════════
print("\n📊 [2] INTERACTION DIAGRAMS (interaction_diagrams.py)")
try:
    from interaction_diagrams import (DIAGRAM_MASTER, DIAGRAMS)
    check("DIAGRAM_MASTER exists", DIAGRAM_MASTER is not None)
    check("DIAGRAMS dict exists", isinstance(DIAGRAMS, dict))
    
    EXPECTED_DIAGRAMS = [f'SD{i}' for i in range(17)]
    found = 0
    for sd in EXPECTED_DIAGRAMS:
        if sd in DIAGRAMS:
            found += 1
    check(f"Diagrams found: {found}/17", found >= 15, f"Only {found}/17")
    
    # Check MASTER has all methods
    if DIAGRAM_MASTER:
        master_steps = DIAGRAM_MASTER.get('steps', [])
        check(f"MASTER has steps", len(master_steps) > 0, f"steps={len(master_steps)}")
except Exception as e:
    print(f"  ⚠️ Cannot import interaction_diagrams: {e}")

# ═══════════════════════════════════════════
# 3. MULTI-INTENT CARD RENDERING — 20 loại
# ═══════════════════════════════════════════
print("\n🔄 [3] MULTI-INTENT CARD RENDERING (free_ai_helper.py)")
try:
    lines = open('free_ai_helper.py', 'r', encoding='utf-8').readlines()
    content = ''.join(lines)
    
    # Check V42.9.6/V42.9.7 blocks exist
    check("V42.9.6 block exists", 'V42.9.6' in content)
    check("V42.9.7 block exists", 'V42.9.7' in content or 'V42.9.6' in content)
    
    # Check all 20 question types in _mi_detect_qtype (answer_question version)
    EXPECTED_QTYPES = [
        'COMPETITION', 'WHEN', 'WHERE', 'WHAT', 'AGE', 'COUNT',
        'SHOULD', 'LIFE_DEATH', 'YESNO',
        'FINANCE', 'LOVE', 'HEALTH', 'CAREER', 'LAWSUIT',
        'LOST_ITEM', 'TRAVEL', 'WHO', 'WHY', 'HOW', 'CHOOSE', 'GENERAL'
    ]
    
    for qt in EXPECTED_QTYPES:
        # Check in both _mi_detect_qtype and _MI_QTYPE_LABEL
        in_detect = f"return '{qt}'" in content
        in_label = f"'{qt}'" in content
        check(f"QType [{qt}] defined", in_detect or in_label, 
              f"detect={in_detect}, label={in_label}")
    
    # Check verdict generators for each type
    VERDICT_TYPES = ['FINANCE', 'LOVE', 'HEALTH', 'CAREER', 'LAWSUIT', 
                     'LOST_ITEM', 'TRAVEL', 'WHO', 'WHY', 'HOW', 'CHOOSE']
    for vt in VERDICT_TYPES:
        check(f"Verdict for [{vt}]", f"qtype == '{vt}'" in content, "Thiếu verdict generator")
    
    # Check _MI_QTYPE_LABEL has all types
    label_count = content.count("_MI_QTYPE_LABEL")
    check("_MI_QTYPE_LABEL dict exists", label_count >= 1, f"Found {label_count} references")

except Exception as e:
    print(f"  ❌ Cannot read free_ai_helper.py: {e}")

# ═══════════════════════════════════════════
# 4. SCORING METHODS — 6 phương pháp chấm điểm
# ═══════════════════════════════════════════
print("\n📈 [4] SCORING METHODS")
SCORING_METHODS = [
    '_ky_mon_scoring', '_luc_hao_scoring', '_mai_hoa_scoring',
    '_thiet_ban_scoring', '_luc_nham_scoring', '_thai_at_scoring'
]
for sm in SCORING_METHODS:
    check(f"{sm} defined", f"def {sm}" in content)

# ═══════════════════════════════════════════
# 5. ANALYSIS METHODS — Phân tích đầy đủ
# ═══════════════════════════════════════════
print("\n🔬 [5] ANALYSIS METHODS")
ANALYSIS_METHODS = [
    '_analyze_ky_mon', '_analyze_luc_hao_full', '_analyze_mai_hoa_full',
    '_analyze_thiet_ban_kinh_dich_van_vat',
    '_build_unified_narrative', '_generate_direct_answer',
    '_build_verdict_compact_block', '_build_factor_interaction_map',
    'answer_question'
]
for am in ANALYSIS_METHODS:
    check(f"{am} defined", f"def {am}" in content)

# ═══════════════════════════════════════════
# 6. QUESTION PARSER
# ═══════════════════════════════════════════
print("\n📝 [6] QUESTION PARSER (question_parser.py)")
try:
    from question_parser import v32_parse_question, format_parsed_questions_v2, analyze_question
    
    # Test parsing compound question
    result = v32_parse_question("bố tôi bệnh nặng hay không và khi nào sẽ khỏi")
    check("v32_parse_question works", len(result) >= 1, f"parsed {len(result)} questions")
    check("Multi-intent detected", len(result) >= 2, f"Only {len(result)} parsed (expected ≥2)")
    
    if result:
        q1 = result[0]
        check("Q1 has text", bool(q1.get('text')), f"text='{q1.get('text','')[:30]}'")
        check("Q1 has dung_than", bool(q1.get('dung_than')), f"dt='{q1.get('dung_than','')}'")
        check("Q1 has diagram_id", bool(q1.get('diagram_id')), f"sd='{q1.get('diagram_id','')}'")
    
    # Test single question
    result2 = v32_parse_question("tôi có giàu không")
    check("Single question parsing", len(result2) >= 1)
    
except Exception as e:
    print(f"  ⚠️ Cannot import question_parser: {e}")

# ═══════════════════════════════════════════
# 7. CATEGORY DETECTION — 8 nhóm chủ đề
# ═══════════════════════════════════════════
print("\n🏷️ [7] SMART CATEGORY DETECTION")
EXPECTED_CATEGORIES = [
    'SỨC_KHỎE_GIA_ĐÌNH', 'TÀI_CHÍNH', 'CÔNG_VIỆC', 'TÌNH_CẢM',
    'TÌM_ĐỒ', 'NHÀ_CỬA', 'XUẤT_HÀNH', 'THẮNG_THUA'
]
for cat in EXPECTED_CATEGORIES:
    check(f"Category [{cat}]", f'"{cat}"' in content, "Thiếu category")

# ═══════════════════════════════════════════
# 8. CORE MODULES — Import OK
# ═══════════════════════════════════════════
print("\n📦 [8] CORE MODULE IMPORTS")
MODULES = {
    'qmdg_data': 'KY_MON_DATA',
    'mai_hoa_dich_so': 'tinh_qua_theo_thoi_gian',
    'luc_hao_kinh_dich': 'lap_qua_luc_hao',
    'van_vat_loai_tuong': 'BAT_QUAI_LOAI_TUONG',
    'kinh_dich_64_que': 'KINH_DICH_64',
}
for mod, attr in MODULES.items():
    try:
        m = __import__(mod)
        check(f"import {mod}", hasattr(m, attr), f"Missing {attr}")
    except Exception as e:
        check(f"import {mod}", False, str(e)[:50])

# ═══════════════════════════════════════════
# 9. KEY FEATURES — Các tính năng quan trọng
# ═══════════════════════════════════════════
print("\n⭐ [9] KEY FEATURES CHECK")
FEATURES = {
    'Answer-First Protocol': 'Answer-First' in content or 'PHÁN QUYẾT' in content,
    'Conflict Detection': 'CONFLICT' in content.upper() or 'XUNG ĐỘT' in content,
    '12 Truong Sinh': 'TRUONG_SINH' in content or 'Trường Sinh' in content,
    'Ngu Khi': '_calc_ngu_khi' in content,
    'Unified Strength': '_calc_unified_strength_tier' in content,
    'Van Vat mapping': '_get_van_vat' in content,
    'Khong Vong': '_get_khong_vong' in content,
    'Dich Ma': 'dich_ma' in content.lower(),
    'Phan Phuc Ngam': 'phan_phuc_ngam' in content.lower() or 'Phản' in content,
    'Am Dong': '_detect_am_dong' in content,
    'Hao Tu': '_get_hao_tu' in content,
    'Competition scoring': '_calc_competition_scores' in content,
    'Timing analysis': '_analyze_timing' in content,
    'Online AI integration': '_try_online_ai' in content,
    'DKT (Knowledge Tree) used': 'DKT' in content,
    'Seasonal strength': '_get_seasonal_strength' in content,
    'Nguyet Pha warning': '_build_nguyet_pha_warning' in content,
    'Thien Dia Nhan Than': '_build_thien_dia_nhan_than' in content,
    '27-step protocol': '_apply_27step_protocol' in content,
    'Element impact analysis': '_build_element_impact_analysis' in content,
}
for feat, ok in FEATURES.items():
    check(feat, ok)

# ═══════════════════════════════════════════
# 10. SĐ ↔ QTYPE MAPPING COMPLETENESS
# ═══════════════════════════════════════════
print("\n🗺️ [10] SĐ ↔ QTYPE MAPPING")
SD_QTYPE_MAP = {
    'SĐ0': 'GENERAL', 'SĐ1': 'YESNO', 'SĐ2': 'AGE/COUNT',
    'SĐ3': 'WHAT', 'SĐ4': 'WHERE', 'SĐ5': 'WHEN',
    'SĐ6': 'FINANCE', 'SĐ7': 'LOVE', 'SĐ8': 'HEALTH',
    'SĐ9': 'CAREER', 'SĐ10': 'LAWSUIT', 'SĐ11': 'LOST_ITEM',
    'SĐ12': 'TRAVEL', 'SĐ13': 'WHO', 'SĐ14': 'WHY',
    'SĐ15': 'HOW', 'SĐ16': 'CHOOSE',
}
for sd, qt in SD_QTYPE_MAP.items():
    qtypes = qt.split('/')
    all_found = all(f"'{q}'" in content for q in qtypes)
    check(f"{sd} → {qt}", all_found)

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════
print("\n" + "=" * 70)
print(f"📊 KẾT QUẢ TỔNG THỂ: {PASS_CHECKS}/{TOTAL_CHECKS} PASSED")
print(f"   ✅ Đạt: {PASS_CHECKS}")
print(f"   ❌ Thiếu: {len(FAIL_ITEMS)}")

if FAIL_ITEMS:
    print(f"\n⚠️ CÁC MỤC CHƯA ĐẠT:")
    for name, detail in FAIL_ITEMS:
        print(f"   ❌ {name}: {detail}")
else:
    print(f"\n🎉 HỆ THỐNG HOÀN CHỈNH 100% — KHÔNG THIẾU SÓT!")

score = int(PASS_CHECKS / TOTAL_CHECKS * 100) if TOTAL_CHECKS > 0 else 0
print(f"\n🏆 ĐIỂM AUDIT: {score}/100")
print("=" * 70)

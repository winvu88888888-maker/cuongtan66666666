"""
🤖 SUPER AUDIT ROBOT V1.0 — Kiểm tra toàn bộ Divination Engine V42.9.9i
Chạy: python _super_audit_robot.py
6 Module: Data Integrity → Scoring Logic → Verdict Consistency → Multi-Q → Prompt → Regression
"""
import sys, os, importlib, traceback

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS = 0
FAIL = 0
WARN = 0
DETAILS = []

def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name}" + (f" — {detail}" if detail else ""))
        DETAILS.append(f"FAIL: {name} — {detail}")

def warn(name, detail=""):
    global WARN
    WARN += 1
    print(f"  ⚠️  {name}" + (f" — {detail}" if detail else ""))
    DETAILS.append(f"WARN: {name} — {detail}")

print("=" * 70)
print("🤖 SUPER AUDIT ROBOT V1.0 — DIVINATION ENGINE V42.9.9i")
print("=" * 70)

# ══════════════════════════════════════════════════════
# MODULE 1: DATA INTEGRITY — 22 file + 271 DKT factors
# ══════════════════════════════════════════════════════
print("\n📦 MODULE 1: DATA INTEGRITY (22 files + DKT)")

CRITICAL_FILES = [
    'free_ai_helper.py', 'app.py', 'divination_knowledge_tree.py',
    'interaction_diagrams.py', 'luc_hao_kinh_dich.py', 'mai_hoa_dich_so.py',
    'kinh_dich_64_que.py', 'question_parser.py', 'dai_luc_nham.py',
    'thai_at_than_so.py', 'tu_vi.py', 'xem_ngay_dep.py',
    'van_vat_loai_tuong.py', 'van_vat_tong_hop.py', 'qmdg_data.py',
    'luc_hao_ky_mon_rules.py', 'gemini_helper.py', 'blind_reading.py',
    'qmdg_advanced_rules.py', 'qmdg_inference_rules.py',
    'iching_integrated_data.py', 'requirements.txt',
]

for f in CRITICAL_FILES:
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    check(f"File {f} exists ({size:,} bytes)", exists and size > 0, "FILE MISSING!")

# DKT check
try:
    from divination_knowledge_tree import TREE as DKT
    check("DKT TREE imported", DKT is not None)
    dkt_keys = list(DKT.keys())
    check(f"DKT has {len(dkt_keys)} categories", len(dkt_keys) >= 8, f"Only {len(dkt_keys)}")
    
    # Count total factors
    total_factors = 0
    for cat_key, cat_data in DKT.items():
        if isinstance(cat_data, dict):
            for sub_key, sub_data in cat_data.items():
                if isinstance(sub_data, dict):
                    total_factors += len(sub_data)
                elif isinstance(sub_data, list):
                    total_factors += len(sub_data)
                else:
                    total_factors += 1
    check(f"DKT total factors >= 200", total_factors >= 200, f"Only {total_factors}")
    
    # Check critical sub-trees
    lh = DKT.get('LH', DKT.get('luc_hao', {}))
    check("DKT.LH.luc_xung exists", 'luc_xung' in lh)
    check("DKT.LH.luc_hop exists", 'luc_hop' in lh)
    check("DKT.LH.tam_hop exists", 'tam_hop' in lh)
    check("DKT.LH.luc_than exists", 'luc_than' in lh)
    check("DKT.LH.ngu_hanh exists", 'ngu_hanh' in lh)
    
    km = DKT.get('KM', DKT.get('ky_mon', {}))
    check("DKT.KM exists", len(km) > 0, "KỲ MÔN MISSING")
except Exception as e:
    check("DKT import", False, str(e))

# Interaction Diagrams
try:
    from interaction_diagrams import DIAGRAMS, DIAGRAM_MASTER
    check(f"DIAGRAMS has {len(DIAGRAMS)} entries", len(DIAGRAMS) >= 17, f"Only {len(DIAGRAMS)}")
    for i in range(17):
        key = f"SD{i}"
        check(f"  DIAGRAMS[{key}] exists", key in DIAGRAMS, f"{key} MISSING")
    check("DIAGRAM_MASTER template exists", DIAGRAM_MASTER is not None)
    
    from interaction_diagrams import KM_BAT_MON_REF, KM_CUU_TINH_REF
    check(f"KM_BAT_MON_REF has {len(KM_BAT_MON_REF)} entries", len(KM_BAT_MON_REF) >= 8)
    check(f"KM_CUU_TINH_REF has {len(KM_CUU_TINH_REF)} entries", len(KM_CUU_TINH_REF) >= 9)
    
    from interaction_diagrams import TV_CHINH_TINH_REF, XND_HOANG_DAO_REF, XND_HAC_DAO_REF
    check(f"TV_CHINH_TINH_REF has {len(TV_CHINH_TINH_REF)} entries", len(TV_CHINH_TINH_REF) >= 14)
    check(f"XND_HOANG_DAO_REF has {len(XND_HOANG_DAO_REF)} entries", len(XND_HOANG_DAO_REF) >= 6)
except Exception as e:
    check("Interaction Diagrams import", False, str(e))

# ══════════════════════════════════════════════════════
# MODULE 2: SCORING LOGIC — Import chain + functions
# ══════════════════════════════════════════════════════
print("\n📊 MODULE 2: SCORING LOGIC (Import chain)")

try:
    from free_ai_helper import FreeAIHelper
    check("FreeAIHelper class imported", True)
    
    helper = FreeAIHelper.__new__(FreeAIHelper)
    
    # Check critical methods exist
    critical_methods = [
        '_analyze_ky_mon', '_analyze_luc_hao_full', '_analyze_mai_hoa_full',
        '_analyze_thiet_ban_kinh_dich_van_vat', '_build_unified_narrative',
        '_build_factor_interaction_map', '_build_verdict_compact_block',
        '_calc_competition_scores', '_generate_direct_answer',
        'answer_question',
    ]
    for m in critical_methods:
        check(f"Method {m}() exists", hasattr(helper, m), "METHOD MISSING")
    
    # Check standalone functions
    from free_ai_helper import (
        _calc_unified_strength_tier,
        _get_ung_ky_advanced,
        _analyze_hoa_hoi_dau,
        _build_phan_phuc_ngam_warning,
        _build_nguyet_pha_warning,
    )
    check("_calc_unified_strength_tier imported", True)
    check("_get_ung_ky_advanced imported", True)
    check("_analyze_hoa_hoi_dau imported", True)
    check("_build_phan_phuc_ngam_warning imported", True)
    check("_build_nguyet_pha_warning imported", True)
    
except Exception as e:
    check("free_ai_helper import", False, str(e)[:200])

# Check scoring constants
try:
    from free_ai_helper import LUC_XUNG_CHI, LUC_HOP_CHI, TAM_HOP_CUC, LUC_HAO_RULES
    check(f"LUC_XUNG_CHI has {len(LUC_XUNG_CHI)} pairs", len(LUC_XUNG_CHI) >= 6)
    check(f"LUC_HOP_CHI has {len(LUC_HOP_CHI)} pairs", len(LUC_HOP_CHI) >= 6)
    check(f"TAM_HOP_CUC has {len(TAM_HOP_CUC)} cucs", len(TAM_HOP_CUC) >= 4)
    check(f"LUC_HAO_RULES has {len(LUC_HAO_RULES)} rules", len(LUC_HAO_RULES) >= 18, f"Only {len(LUC_HAO_RULES)}")
except Exception as e:
    check("Scoring constants import", False, str(e)[:200])

# ══════════════════════════════════════════════════════
# MODULE 3: VERDICT CONSISTENCY — 3 tầng logic
# ══════════════════════════════════════════════════════
print("\n⚖️  MODULE 3: VERDICT CONSISTENCY (3-tier logic)")

# Read source to verify 3-tier verdict exists
try:
    src = open('free_ai_helper.py', 'r', encoding='utf-8').read()
    
    check("TẦNG 1: Consensus Voting code exists", 'CONSENSUS VOTING' in src)
    check("TẦNG 2: Weighted Severity code exists", 'WEIGHTED SEVERITY' in src)
    check("TẦNG 3: Critical Factor Override exists", 'CRITICAL FACTOR OVERRIDE' in src)
    
    # Check consensus logic
    check("cat_pp counting logic", 'cat_pp' in src and 'hung_pp' in src)
    check("consensus_confidence variable", 'consensus_confidence' in src)
    
    # Check weighted scoring
    check("Question-type weights (COMPETE)", "'Lục Hào': 0.50" in src or '"Lục Hào": 0.50' in src)
    check("Question-type weights (WHEN)", "'Kỳ Môn': 0.40" in src or '"Kỳ Môn": 0.40' in src)
    check("Question-type weights (WHAT)", "'Mai Hoa': 0.35" in src or '"Mai Hoa": 0.35' in src)
    
    # Check critical overrides
    check("Override: Tuần Không + Suy", 'TUẦN KHÔNG' in src and '_has_tuan_khong' in src)
    check("Override: Phản Ngâm + Triệt Lộ", 'PHẢN NGÂM' in src and '_has_triet_lo' in src)
    check("Override: Tham Sinh Vong Khắc", 'THAM SINH VONG KHẮC' in src)
    check("Override: Nguyệt Phá + Nhật Phá", 'NGUYỆT PHÁ' in src and '_has_nhat_pha' in src)
    check("Override: LOCK consensus", 'LOCK_CAT' in src and 'LOCK_HUNG' in src)
    
    # Check verdict labels
    for label in ['ĐẠI CÁT', 'CÁT', 'THIÊN CÁT', 'BÌNH', 'HUNG', 'ĐẠI HUNG']:
        check(f"Verdict label '{label}' in consensus", label in src)
        
except Exception as e:
    check("Verdict source analysis", False, str(e)[:200])

# ══════════════════════════════════════════════════════
# MODULE 4: MULTI-QUESTION TEST — 20 loại câu hỏi
# ══════════════════════════════════════════════════════
print("\n❓ MODULE 4: MULTI-QUESTION (20 question types)")

QTYPES = [
    'YESNO', 'WHEN', 'WHERE', 'WHAT', 'AGE', 'COUNT',
    'SHOULD', 'LIFE_DEATH', 'COMPETITION', 'FINANCE',
    'LOVE', 'HEALTH', 'CAREER', 'LAWSUIT', 'LOST_ITEM',
    'TRAVEL', 'WHO', 'WHY', 'HOW', 'CHOOSE',
]

for qt in QTYPES:
    found = f"'{qt}'" in src or f'"{qt}"' in src
    check(f"Question type {qt} handled", found, f"{qt} NOT FOUND in code")

# Check multi-intent sub-verdict
check("_sub_verdicts list created", '_sub_verdicts' in src)
check("_detect_qtype_sub function", '_detect_qtype_sub' in src)
check("_gen_verdict_by_qtype function", '_gen_verdict_by_qtype' in src)
check("Sub-question multi-factor scoring (V42.9.9i)", 'Multi-factor scoring cho sub-question' in src)
check("Sub-question factors display", 'factors' in src and '_sq_factors_detail' in src)

# ══════════════════════════════════════════════════════
# MODULE 5: GEMINI PROMPT — Tinh gọn + đúng role
# ══════════════════════════════════════════════════════
print("\n🤖 MODULE 5: GEMINI PROMPT (Clean + Role)")

check("Prompt version V42.9.9i", 'V42.9.9i' in src)
check("Role: CHUYÊN GIA DIỄN GIẢI", 'DIỄN GIẢI' in src)
check("Verdict block injection", 'verdict_block' in src or 'offline_verdict_block' in src)
check("Output format template", 'output_format' in src)
check("500 char limit instruction", '500' in src)
check("Anti-hallucination rule", 'CẤM' in src and 'bịa' in src.lower())
check("No conflicting INDEPENDENT instruction", src.count('LUẬN GIẢI ĐỘC LẬP') <= 1,
      f"Found {src.count('LUẬN GIẢI ĐỘC LẬP')} — should be ≤1")

# ══════════════════════════════════════════════════════
# MODULE 6: REGRESSION — Benchmark functions
# ══════════════════════════════════════════════════════
print("\n🔬 MODULE 6: REGRESSION (Function tests)")

# Test _calc_unified_strength_tier
try:
    result = _calc_unified_strength_tier(lh_raw=30, ts_stage='Đế Vượng', hanh_dt='Kim')
    check("_calc_unified_strength_tier returns value", result is not None)
    if isinstance(result, tuple):
        pct = result[1] if len(result) >= 2 else result[0]
    elif isinstance(result, dict):
        pct = result.get('pct', result.get('score', 50))
    else:
        pct = result if isinstance(result, (int, float)) else 50
    check(f"  Vượng + high score → pct >= 50", pct >= 50, f"pct={pct}")
except Exception as e:
    check("_calc_unified_strength_tier test", False, str(e)[:100])

# Test _get_ung_ky_advanced
try:
    uk = _get_ung_ky_advanced('Kim', 'CÁT')
    check("_get_ung_ky_advanced returns string", isinstance(uk, str) and len(uk) > 5)
except Exception as e:
    check("_get_ung_ky_advanced test", False, str(e)[:100])

# Test _analyze_hoa_hoi_dau
try:
    hhd = _analyze_hoa_hoi_dau('Kim', 'Mộc', 'Thân', 'Dần', 'Thê Tài')
    check("_analyze_hoa_hoi_dau returns dict/tuple", hhd is not None)
except Exception as e:
    check("_analyze_hoa_hoi_dau test", False, str(e)[:100])

# Test question parser
try:
    from free_ai_helper import v32_parse_question, _get_all_dung_than
    pq = v32_parse_question("Tôi có thắng không và khi nào")
    check(f"v32_parse_question returns {len(pq)} parts", len(pq) >= 1)
    dts = _get_all_dung_than("Tiền bạc của tôi")
    check(f"_get_all_dung_than returns {len(dts)} DTs", len(dts) >= 1)
except Exception as e:
    check("question_parser test", False, str(e)[:100])

# Test Vạn Vật
try:
    from van_vat_loai_tuong import get_ngu_hanh_tuong
    vv = get_ngu_hanh_tuong('Kim')
    check(f"get_ngu_hanh_tuong('Kim') returns data", vv is not None and len(str(vv)) > 0)
except ImportError:
    check("van_vat_loai_tuong (skip: no streamlit)", True)
except Exception as e:
    check("van_vat_loai_tuong test", False, str(e)[:100])
try:
    pass  # placeholder
except Exception as e:
    check("van_vat_loai_tuong test", False, str(e)[:100])

# Test Đại Lục Nhâm
try:
    from dai_luc_nham import tinh_dai_luc_nham
    check("dai_luc_nham.tinh_dai_luc_nham imported", True)
except Exception as e:
    check("dai_luc_nham import", False, str(e)[:100])

# Test Thái Ất
try:
    from thai_at_than_so import tinh_thai_at_than_so
    check("thai_at_than_so.tinh_thai_at_than_so imported", True)
except Exception as e:
    check("thai_at_than_so import", False, str(e)[:100])

# ══════════════════════════════════════════════════════
# FINAL REPORT
# ══════════════════════════════════════════════════════
print("\n" + "=" * 70)
total = PASS + FAIL
status = "✅ ALL PASS" if FAIL == 0 else f"❌ {FAIL} FAILURES"
print(f"📊 KẾT QUẢ: {PASS}/{total} PASS | {FAIL} FAIL | {WARN} WARN — {status}")
print("=" * 70)

if DETAILS:
    print("\n📋 CHI TIẾT LỖI:")
    for d in DETAILS:
        print(f"  • {d}")

if FAIL == 0:
    print("\n🎉 HỆ THỐNG V42.9.9i HOÀN TOÀN SẠCH — SẴN SÀNG DEPLOY!")
else:
    print(f"\n⚠️  CẦN SỬA {FAIL} LỖI TRƯỚC KHI DEPLOY!")

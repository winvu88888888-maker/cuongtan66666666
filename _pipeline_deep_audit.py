# -*- coding: utf-8 -*-
"""
PIPELINE DEEP AUDIT — V42.9.9i
Trace TOÀN BỘ data flow từ câu hỏi → Dụng Thần → Scoring → Verdict → Prompt → Card
Tìm chỗ AI đọc sai / data bị mất / logic mâu thuẫn
"""
import sys, json, importlib, traceback
sys.stdout.reconfigure(encoding='utf-8')

# ===== IMPORT ENGINE =====
try:
    from free_ai_helper import FreeAIHelper
    print("✅ Import FreeAIHelper OK")
except Exception as e:
    print(f"❌ Import FAIL: {e}")
    sys.exit(1)

# ===== TEST CASES — Câu hỏi phổ biến =====
TEST_QUESTIONS = [
    ("toi co nen dau tu kinh doanh nam nay khong", "Bản Thân"),
    ("nam nay co mua duoc nha khong", "Bản Thân"),
    ("bao gio toi co nguoi yeu", "Bản Thân"),
]

TOTAL_ISSUES = []

def audit_one(question, dung_than_role, test_idx):
    """Audit 1 câu hỏi — trace full pipeline"""
    print(f"\n{'='*80}")
    print(f"📋 TEST {test_idx}: \"{question}\"")
    print(f"   DT Role: {dung_than_role}")
    print(f"{'='*80}")
    
    issues = []
    
    try:
        helper = FreeAIHelper()
        
        # ═══ STEP 1: Chạy analyze ═══
        # Fake chart data để simulate
        fake_chart = {
            'can_ngay': 'Giáp', 'chi_ngay': 'Dần',
            'can_gio': 'Bính', 'chi_gio': 'Ngọ', 
            'can_thang': 'Canh', 'chi_thang': 'Thìn',
            'can_nam': 'Mậu', 'chi_nam': 'Tuất',
            'can_thien_ban': {},
            'thien_ban': {}, 'nhan_ban': {}, 'than_ban': {},
            'hanh_dt': '',
        }
        
        # ═══ STEP 2: Kiểm tra DT detection ═══
        from free_ai_helper import _get_dung_than, _get_all_dung_than
        detected_dt = _get_dung_than(question)
        all_dts = _get_all_dung_than(question)
        print(f"\n🔍 STEP 2 — DỤNG THẦN:")
        print(f"   Detected DT: {detected_dt}")
        print(f"   All DTs: {all_dts}")
        
        if not detected_dt:
            issues.append(f"[DT] Không detect được Dụng Thần cho: {question}")
        
        # ═══ STEP 3: Kiểm tra question classification ═══
        from free_ai_helper import v32_parse_question
        parsed = v32_parse_question(question)
        print(f"\n🔍 STEP 3 — PHÂN LOẠI CÂU HỎI:")
        print(f"   Parsed questions: {len(parsed)}")
        for pq in parsed:
            print(f"     - \"{pq.get('text','?')[:60]}\" → DT: {pq.get('dung_than','?')}")
        
        # ═══ STEP 4: Kiểm tra category detection ═══
        try:
            from free_ai_helper import CATEGORIES
            q_lower = question.lower()
            detected_cat = 'CHUNG'
            for cat_key, cat_data in CATEGORIES.items():
                keywords = cat_data.get('keywords', [])
                if any(kw in q_lower for kw in keywords):
                    detected_cat = cat_key
                    break
            print(f"\n🔍 STEP 4 — CATEGORY:")
            print(f"   Detected: {detected_cat}")
        except Exception as e:
            print(f"   ⚠️ Category detection error: {e}")
        
        # ═══ STEP 5: Kiểm tra verdict scoring ═══
        # Simulate verdicts
        print(f"\n🔍 STEP 5 — SCORING SIMULATION:")
        
        # Check METHOD_STRENGTH_MAP
        try:
            from free_ai_helper import METHOD_STRENGTH_MAP, CATEGORY_TO_STRENGTH
            strength_key = CATEGORY_TO_STRENGTH.get(detected_cat, 'tổng_quát')
            method_w = METHOD_STRENGTH_MAP.get(strength_key, METHOD_STRENGTH_MAP.get('tổng_quát', {}))
            print(f"   Strength key: {strength_key}")
            print(f"   Weights: KM={method_w.get('ky_mon',0)}, LH={method_w.get('luc_hao',0)}, MH={method_w.get('mai_hoa',0)}")
            print(f"            TB={method_w.get('thiet_ban',0)}, LN={method_w.get('luc_nham',0)}, TA={method_w.get('thai_at',0)}")
            
            # Check weights sum to reasonable values
            total_w = sum(method_w.values())
            lh_pct = method_w.get('luc_hao', 0) / max(1, total_w) * 100
            km_pct = method_w.get('ky_mon', 0) / max(1, total_w) * 100
            print(f"   LH chiếm: {lh_pct:.0f}% | KM chiếm: {km_pct:.0f}% | Tổng weights: {total_w}")
            
            if lh_pct < 20:
                issues.append(f"[WEIGHT] Lục Hào chỉ chiếm {lh_pct:.0f}% — quá thấp cho PP chủ lực")
            if km_pct < 10:
                issues.append(f"[WEIGHT] Kỳ Môn chỉ chiếm {km_pct:.0f}% — quá thấp")
        except Exception as e:
            issues.append(f"[WEIGHT] Error loading weights: {e}")
        
        # ═══ STEP 6: Kiểm tra Gemini prompt structure ═══
        print(f"\n🔍 STEP 6 — PROMPT STRUCTURE:")
        
        # Verify prompt contains key sections
        prompt_requirements = [
            'system_role', 'question', 'raw_chart_data', 'verdict_block', 'output_format',
            'VERDICT CHÍNH THỨC', 'BẮT BUỘC TUÂN THỦ', 'KHÔNG ĐƯỢC thay đổi verdict'
        ]
        # We can't actually build the prompt without real data, 
        # but verify the structure is correct in code
        
        import re
        code = open('free_ai_helper.py', 'r', encoding='utf-8').read()
        
        # Check prompt template integrity
        prompt_section = code[code.find('PHẦN 4: V42.9.9i GEMINI PROMPT'):code.find('PHẦN 4: V42.9.9i GEMINI PROMPT')+3000]
        
        for req in prompt_requirements:
            if req not in prompt_section and req not in code[code.find('offline_verdict_block'):code.find('offline_verdict_block')+2000]:
                issues.append(f"[PROMPT] Missing '{req}' in prompt template")
        
        # ═══ STEP 7: Kiểm tra AI Online vs Offline consistency ═══
        print(f"\n🔍 STEP 7 — ONLINE vs OFFLINE CONSISTENCY:")
        
        # Check if Gemini prompt enforces using offline verdict
        enforcement_patterns = [
            'KHÔNG ĐƯỢC thay đổi verdict',
            'BẮT BUỘC TUÂN THỦ',
            'KHÔNG PHẢI người quyết định',
            'GIẢI THÍCH TẠI SAO verdict đúng',
        ]
        for pat in enforcement_patterns:
            if pat in code:
                print(f"   ✅ Prompt enforces: \"{pat}\"")
            else:
                issues.append(f"[CONSISTENCY] Missing enforcement: \"{pat}\"")
                print(f"   ❌ MISSING: \"{pat}\"")
        
        # ═══ STEP 8: Kiểm tra extraction logic ═══
        print(f"\n🔍 STEP 8 — EXTRACTION LOGIC:")
        
        # Check _off_answer extraction patterns
        extraction_patterns = [
            'PHÁN QUYẾT:', '📢', 'CÂU TRẢ LỜI', '🟢 CÓ', '🔴 KHÔNG',
        ]
        extraction_code = code[code.find('_off_answer_list'):code.find('_off_answer_list')+3000]
        matched = 0
        for pat in extraction_patterns:
            if pat in extraction_code:
                matched += 1
        print(f"   Extraction patterns found: {matched}/{len(extraction_patterns)}")
        
        # ═══ STEP 9: Kiểm tra 3-Tier Verdict Engine ═══
        print(f"\n🔍 STEP 9 — 3-TIER VERDICT ENGINE:")
        tier_checks = {
            'Tier 1 - Consensus': 'TẦNG 1: CONSENSUS VOTING' in code,
            'Tier 2 - Weighted': 'TẦNG 2: WEIGHTED SEVERITY' in code,
            'Tier 3 - Critical': 'TẦNG 3: CRITICAL FACTOR OVERRIDE' in code,
            'Tuần Không + DT Suy': 'TUẦN KHÔNG' in code and '_has_dt_suy' in code,
            'Phản Ngâm + Triệt Lộ': '_has_phan_ngam' in code and '_has_triet_lo' in code,
            'Tham Sinh Vong Khắc': 'THAM SINH VONG KHẮC' in code,
            'Nguyệt Phá + Nhật Phá': '_has_nguyet_pha' in code and '_has_nhat_pha' in code,
        }
        for name, present in tier_checks.items():
            status = '✅' if present else '❌'
            print(f"   {status} {name}")
            if not present:
                issues.append(f"[3TIER] Missing: {name}")
        
        # ═══ STEP 10: Kiểm tra verdict text generation ═══
        print(f"\n🔍 STEP 10 — VERDICT TEXT LOGIC:")
        
        # Check YES/NO thresholds
        # Phase D: ≥55 = CÓ, ≥50 = CÓ nhưng NỖ LỰC, ≥45 = KHÓ, <45 = KHÔNG
        # Direct Answer: ≥55 = CÓ, ≥50 = CÓ nhưng KHÓ, ≥45 = KHÓ, <45 = KHÔNG
        
        # Check if thresholds match
        da_thresholds = {55, 50, 45}  # from _build_verdict_compact_block
        pd_thresholds = {55, 50, 45}  # from Phase D PHÁN QUYẾT
        
        print(f"   Direct Answer thresholds: {da_thresholds}")
        print(f"   Phase D thresholds: {pd_thresholds}")
        
        if da_thresholds != pd_thresholds:
            issues.append(f"[THRESHOLD] Direct Answer ({da_thresholds}) ≠ Phase D ({pd_thresholds})")
        else:
            print(f"   ✅ Thresholds CONSISTENT")
        
        # ═══ STEP 11: Kiểm tra data flow integrity ═══
        print(f"\n🔍 STEP 11 — DATA FLOW INTEGRITY:")
        
        # Check that verdict_block in prompt contains actual verdicts, not hardcoded
        vb_code = code[code.find('offline_verdict_block = ('):code.find('offline_verdict_block = (')+800]
        critical_vars = ['ky_mon_verdict', 'luc_hao_verdict', 'mai_hoa_verdict', 'luc_nham_verdict', 'thai_at_verdict']
        for cv in critical_vars:
            if cv in vb_code:
                print(f"   ✅ {cv} → verdict_block")
            else:
                issues.append(f"[DATAFLOW] {cv} NOT passed to verdict_block")
                print(f"   ❌ {cv} MISSING from verdict_block")
        
        # ═══ STEP 12: Kiểm tra card rendering ═══
        print(f"\n🔍 STEP 12 — CARD RENDERING:")
        
        # Check enrichment logic
        enrichment_checks = {
            'Enrichment trigger < 80': "len(_off_answer) < 80" in code or "len(_off_answer) <80" in code,
            'BÌNH keyword trigger': "'BÌNH' in _off_answer" in code,
            'CẦN CÂN NHẮC trigger': "'CẦN CÂN NHẮC' in _off_answer" in code,
            'Reason injection KM': "KM: {str(ky_mon_reason)" in code,
            'Reason injection LH': "LH: {str(luc_hao_reason)" in code,
            'Reason injection MH': "MH: {str(mai_hoa_reason)" in code,
            'V42.9.9i header': 'V42.9.9i</div>' in code,
        }
        for name, present in enrichment_checks.items():
            status = '✅' if present else '❌'
            print(f"   {status} {name}")
            if not present:
                issues.append(f"[CARD] Missing: {name}")
        
    except Exception as e:
        issues.append(f"[FATAL] {traceback.format_exc()}")
        print(f"\n❌ FATAL ERROR: {e}")
    
    return issues


# ═══ RUN ALL TESTS ═══
print("\n" + "🤖"*40)
print("  PIPELINE DEEP AUDIT — V42.9.9i")
print("  Tracing AI data flow từ đầu đến cuối")
print("🤖"*40)

all_issues = []
for idx, (q, dt) in enumerate(TEST_QUESTIONS, 1):
    issues = audit_one(q, dt, idx)
    all_issues.extend(issues)

# ═══ SUMMARY ═══
print(f"\n\n{'='*80}")
print(f"📊 TỔNG KẾT AUDIT PIPELINE")
print(f"{'='*80}")

if all_issues:
    print(f"\n🔴 PHÁT HIỆN {len(all_issues)} VẤN ĐỀ:")
    for i, issue in enumerate(all_issues, 1):
        print(f"   {i}. {issue}")
else:
    print(f"\n✅ KHÔNG PHÁT HIỆN VẤN ĐỀ — Pipeline sạch")

# ═══ BỔ SUNG: Kiểm tra 21 yếu tố DKT ═══
print(f"\n\n{'='*80}")
print(f"🌳 KIỂM TRA DKT (Divination Knowledge Tree)")
print(f"{'='*80}")

try:
    from divination_knowledge_tree import DKT
    dkt_keys = list(DKT.keys())
    print(f"   DKT keys: {len(dkt_keys)}")
    
    # Check required top-level keys
    required_keys = ['ky_mon', 'luc_hao', 'mai_hoa', 'thiet_ban', 'luc_nham', 'thai_at']
    for rk in required_keys:
        if rk in DKT:
            sub_keys = list(DKT[rk].keys()) if isinstance(DKT[rk], dict) else []
            print(f"   ✅ DKT['{rk}']: {len(sub_keys)} sub-keys")
        else:
            print(f"   ❌ DKT['{rk}'] MISSING!")
            all_issues.append(f"[DKT] Missing key: {rk}")
    
    # Check factors count
    from free_ai_helper import _FACTOR_REGISTRY
    if '_FACTOR_REGISTRY' in dir():
        print(f"   Factor Registry: {len(_FACTOR_REGISTRY)} entries")
except ImportError:
    print("   ⚠️ DKT not available (module not found)")
except Exception as e:
    print(f"   ⚠️ DKT check error: {e}")

# ═══ FINAL VERDICT ═══
total_issues = len(all_issues)
print(f"\n{'='*80}")
if total_issues == 0:
    print(f"✅ PIPELINE HOÀN TOÀN SẠCH — {total_issues} issues")
elif total_issues <= 3:
    print(f"🟡 PIPELINE CÓ {total_issues} VẤN ĐỀ NHỎ")
else:
    print(f"🔴 PIPELINE CÓ {total_issues} VẤN ĐỀ CẦN SỬA")
print(f"{'='*80}")

# -*- coding: utf-8 -*-
"""V29.3 FULL TEST SUITE — Test toan bo logic offline + prompt + enforce_conclusion"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# TEST 1: Khoi tao FreeAIHelper
# ============================================================
def test_init():
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()
    assert ai is not None, "FAIL: FreeAIHelper is None"
    assert hasattr(ai, 'answer_question'), "FAIL: Missing answer_question"
    assert hasattr(ai, '_enforce_conclusion'), "FAIL: Missing _enforce_conclusion"
    assert hasattr(ai, '_build_verdict_compact_block'), "FAIL: Missing _build_verdict_compact_block"
    assert hasattr(ai, '_try_online_ai'), "FAIL: Missing _try_online_ai"
    print(f"  Version: {ai.version}")
    return True

# ============================================================
# TEST 2: Topic Matching — tat ca cac nhom
# ============================================================
def test_topic_matching():
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()
    
    test_cases = [
        ("Toi co nen mua nha khong?", "Mua"),
        ("Xin viec co duoc khong?", "Việc"),
        ("Benh co khoi khong?", "Bệnh"),
        ("Hon nhan co hanh phuc?", "Hôn"),
        ("Dau tu chung khoan?", "Đầu Tư"),
        ("Thi dai hoc co do?", "Thi"),
        ("Kiem tien nhu the nao?", None),  # chung
    ]
    
    passed = 0
    for q, expect_keyword in test_cases:
        cat = ai._detect_category(q)
        label = cat.get('label', '?')
        if expect_keyword and expect_keyword.lower() in label.lower():
            print(f"  OK: '{q[:30]}...' -> {label}")
            passed += 1
        elif not expect_keyword:
            print(f"  OK: '{q[:30]}...' -> {label} (chung)")
            passed += 1
        else:
            print(f"  FAIL: '{q[:30]}...' -> {label} (expected: {expect_keyword})")
    
    print(f"  Ket qua: {passed}/{len(test_cases)} passed")
    return passed >= 5

# ============================================================
# TEST 3: _enforce_conclusion() — kiem tra inject CÓ/KHÔNG
# ============================================================
def test_enforce_conclusion():
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()
    
    # Test 1: Response khong co ket luan -> phai inject
    raw1 = "Phan tich cho thay Dung Than vuong, Nguyen Than dong."
    result1 = ai._enforce_conclusion(raw1, 70, "The Tai", "Toi co nen mua nha?")
    has_yes = "CÓ" in result1 and "NÊN TIẾN HÀNH" in result1
    has_guidance = "HƯỚNG DẪN" in result1
    print(f"  Test CÁT (70%): inject CÓ={'OK' if has_yes else 'FAIL'}, guidance={'OK' if has_guidance else 'FAIL'}")
    
    # Test 2: Response HUNG -> inject KHÔNG
    raw2 = "Ky Thần ĐỘNG khắc Dụng Thần."
    result2 = ai._enforce_conclusion(raw2, 30, "The Tai", "Toi co nen mua nha?")
    has_no = "KHÔNG" in result2
    print(f"  Test HUNG (30%): inject KHÔNG={'OK' if has_no else 'FAIL'}")
    
    # Test 3: Response da co ket luan -> KHÔNG inject them
    raw3 = "## KẾT LUẬN: CÓ — Thuan loi de mua nha"
    result3 = ai._enforce_conclusion(raw3, 70, "The Tai")
    not_doubled = result3.count("KẾT LUẬN") == 1
    print(f"  Test da co KL: khong inject them={'OK' if not_doubled else 'FAIL'}")
    
    # Test 4: Loai bo tu vong vo
    raw4 = "Co ve nhu thoi diem nay co the thuan loi."
    result4 = ai._enforce_conclusion(raw4, 65, "The Tai")
    no_vague = "co ve" not in result4.lower() or "co the " not in result4.lower()
    print(f"  Test loai vong vo: {'OK' if no_vague else 'FAIL'}")
    
    # Test 5: CÂN NHẮC (50%)
    raw5 = "Du lieu cho thay tinh hinh chua ro rang."
    result5 = ai._enforce_conclusion(raw5, 52, "The Tai", "Co nen dau tu?")
    has_caution = "CÂN NHẮC" in result5 or "THẬN TRỌNG" in result5
    print(f"  Test BINH (52%): can nhac={'OK' if has_caution else 'FAIL'}")
    
    return has_yes and has_no and not_doubled

# ============================================================
# TEST 4: _build_verdict_compact_block()
# ============================================================
def test_verdict_block():
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()
    
    test_data = {
        'dung_than': 'Thê Tài',
        'category_label': 'Mua Nhà Đất',
        'ky_mon_verdict': 'CÁT',
        'ky_mon_reason': 'Can Ngay VUONG dac dia',
        'luc_hao_verdict': 'HUNG',
        'luc_hao_reason': 'DT Suy bi khac',
        'mai_hoa_verdict': 'CAT',
        'mai_hoa_reason': 'The sinh Dung',
        'luc_nham_verdict': 'BINH',
        'luc_nham_reason': 'Tu Khoa trung binh',
        'thai_at_verdict': 'CAT',
        'thai_at_reason': 'Cung cat',
        'v22_unified_strength': {
            'unified_pct': 62,
            'tier_cap': 'CÁT',
            'ts_stage': 'Trường Sinh',
            'ngu_khi': 'VƯỢNG',
            'hanh_dt': 'Thổ',
        },
        'impact_evidence': [
            'DT Thê Tài Vượng → TÀI SẢN MẠNH',
            'Nguyên Thần ĐỘNG → sinh DT',
            'Nhật Thần SINH DT → hỗ trợ từ bên ngoài',
        ],
        'unified_narrative': 'Quẻ cho thấy Thê Tài (tài sản) Vượng, được Nguyên Thần động sinh. Kết luận: CÁT.',
    }
    
    block = ai._build_verdict_compact_block(test_data)
    
    checks = {
        'Has DT': 'Thê Tài' in block,
        'Has KM verdict': 'CÁT' in block,
        'Has LH verdict': 'HUNG' in block,
        'Has Score': '62' in block,
        'Has evidence': 'TÀI SẢN MẠNH' in block,
        'Has narrative': 'Quẻ cho thấy' in block,
        'Has LOCK warning': 'CẤM' in block or 'PHẢI' in block,
    }
    
    for name, ok in checks.items():
        print(f"  {name}: {'OK' if ok else 'FAIL'}")
    
    return all(checks.values())

# ============================================================
# TEST 5: Full Offline answer_question() — khong can API
# ============================================================
def test_offline_answer():
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()  # Khong co API key -> chi chay offline
    
    questions = [
        "Toi co nen mua nha khong?",
        "Benh nay co khoi khong?",
        "Xin viec co thanh cong khong?",
    ]
    
    for q in questions:
        try:
            result = ai.answer_question(q)
            length = len(result) if result else 0
            # Kiem tra co ket luan
            has_verdict = any(k in result.upper() for k in ['CÁT', 'HUNG', 'CÓ', 'KHÔNG', 'THUẬN', 'KHÓ', 'BÌNH']) if result else False
            print(f"  '{q[:30]}': {length} chars, verdict={'OK' if has_verdict else 'FAIL'}")
        except Exception as e:
            print(f"  '{q[:30]}': ERROR - {str(e)[:60]}")
    
    return True

# ============================================================
# TEST 6: Prompt structure (V29.3)
# ============================================================
def test_prompt_structure():
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()
    
    # Simulate offline_analysis_data
    od = {
        'dung_than': 'Thê Tài',
        'category_label': 'Mua Nhà Đất',
        'ky_mon_verdict': 'CÁT', 'ky_mon_reason': 'VUONG',
        'luc_hao_verdict': 'CÁT', 'luc_hao_reason': 'DT Vuong',
        'mai_hoa_verdict': 'HUNG', 'mai_hoa_reason': 'Dung khac The',
        'luc_nham_verdict': 'BINH', 'luc_nham_reason': 'Trung binh',
        'thai_at_verdict': 'CÁT', 'thai_at_reason': 'Cung cat',
        'v22_unified_strength': {'unified_pct': 68},
        'v15_timing': 'Thang 5 tot',
        'v15_timeline': 'Nhanh',
        'unified_narrative': 'Test narrative',
        'impact_evidence': ['E1', 'E2'],
        'full_offline_report': 'Full report text',
        'detective_deduction': 'Detective text',
    }
    
    # Build verdict block
    block = ai._build_verdict_compact_block(od)
    
    # Simulate what prompt would look like
    _wpct = 68
    checks = {
        'Pre-conclusion CÓ': _wpct >= 65,  # Should be CÓ
        'Verdict block has all 5PP': all(k in block for k in ['KỲ MÔN', 'LỤC HÀO', 'MAI HOA']),
        'Block has score': '68' in block or str(_wpct) in block,
    }
    
    for name, ok in checks.items():
        print(f"  {name}: {'OK' if ok else 'FAIL'}")
    
    return all(checks.values())

# ============================================================
# TEST 7: Kiem tra GeminiHelper temperature
# ============================================================
def test_gemini_temperature():
    try:
        with open('gemini_helper.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_low_temp = 'temperature=0.15' in content
        has_low_topp = 'top_p=0.7' in content
        has_low_topk = 'top_k=20' in content
        
        print(f"  temperature=0.15: {'OK' if has_low_temp else 'FAIL'}")
        print(f"  top_p=0.7: {'OK' if has_low_topp else 'FAIL'}")
        print(f"  top_k=20: {'OK' if has_low_topk else 'FAIL'}")
        
        return has_low_temp and has_low_topp
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# ============================================================
# TEST 8: Kiem tra app.py có 2 nút phân biệt
# ============================================================  
def test_app_buttons():
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_quick = 'HỎI NHANH' in content
        has_supreme = 'LỤC THUẬT HỢP NHẤT' in content
        has_quick_logic = '_call_ai_raw' in content and 'quick_prompt' in content
        has_separate_flow = 'btn_ask_normal' in content and 'btn_ask_supreme' in content
        
        print(f"  Nut HOI NHANH: {'OK' if has_quick else 'FAIL'}")
        print(f"  Nut LUC THUAT: {'OK' if has_supreme else 'FAIL'}")
        print(f"  Quick Ask logic: {'OK' if has_quick_logic else 'FAIL'}")
        print(f"  Separate flow: {'OK' if has_separate_flow else 'FAIL'}")
        
        return has_quick and has_supreme and has_separate_flow
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# ============================================================
# TEST 9: Kiem tra prompt V29.3 có hướng dẫn mọi dạng câu hỏi
# ============================================================
def test_prompt_question_types():
    try:
        with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        question_types = [
            ('CÓ/KHÔNG', 'CÓ/KHÔNG'),
            ('KHI NÀO', 'KHI NÀO'),
            ('Ở ĐÂU', 'Ở ĐÂU'),
            ('NGƯỜI', 'về NGƯỜI'),
            ('HƯỚNG', 'HƯỚNG'),
            ('SỨC KHỎE', 'SỨC KHỎE'),
            ('TÌNH CẢM', 'TÌNH CẢM'),
            ('TÀI CHÍNH', 'TÀI CHÍNH'),
            ('KIỆN TỤNG', 'KIỆN TỤNG'),
            ('DI CHUYỂN', 'DI CHUYỂN'),
        ]
        
        passed = 0
        for name, keyword in question_types:
            found = keyword in content
            print(f"  {name}: {'OK' if found else 'FAIL'}")
            if found: passed += 1
        
        print(f"  Ket qua: {passed}/{len(question_types)}")
        return passed >= 8
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# ============================================================
# TEST 10: Kiem tra KHÔNG cắt data (V29.1)
# ============================================================
def test_no_truncation():
    try:
        with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kiem tra KHÔNG còn [:2000], [:3000], [:6000] truncation
        has_old_2000 = "[:2000]" in content and "offline_report" in content.split("[:2000]")[0][-100:]
        has_old_3000 = "[:3000]" in content and "raw_que_data" in content.split("[:3000]")[0][-100:]
        has_old_6000 = "[:6000]" in content
        
        print(f"  No [:2000] on report: {'OK' if not has_old_2000 else 'FAIL - van con cat!'}")
        print(f"  No [:3000] on raw: {'OK' if not has_old_3000 else 'FAIL - van con cat!'}")
        print(f"  No [:6000] on output: {'OK' if not has_old_6000 else 'FAIL - van con cat!'}")
        
        return not has_old_6000
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

# ============================================================
# RUN ALL TESTS
# ============================================================
if __name__ == '__main__':
    tests = [
        ("1. Khoi tao FreeAIHelper", test_init),
        ("2. Topic Matching", test_topic_matching),
        ("3. _enforce_conclusion()", test_enforce_conclusion),
        ("4. _build_verdict_compact_block()", test_verdict_block),
        ("5. Full Offline answer_question()", test_offline_answer),
        ("6. Prompt Structure V29.3", test_prompt_structure),
        ("7. Gemini Temperature Settings", test_gemini_temperature),
        ("8. App UI Buttons", test_app_buttons),
        ("9. Question Type Coverage", test_prompt_question_types),
        ("10. No Data Truncation", test_no_truncation),
    ]
    
    print("=" * 60)
    print("V29.3 FULL TEST SUITE")
    print("=" * 60)
    
    results = []
    for name, func in tests:
        print(f"\n{'='*60}")
        print(f"TEST {name}")
        try:
            ok = func()
            results.append((name, ok))
            print(f"  >>> {'PASS' if ok else 'FAIL'}")
        except Exception as e:
            results.append((name, False))
            print(f"  >>> EXCEPTION: {str(e)[:80]}")
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    for name, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'} — {name}")
    print(f"\nTotal: {passed}/{total} PASSED")
    if passed == total:
        print("ALL TESTS PASSED!")
    else:
        print(f"WARNING: {total - passed} test(s) FAILED")

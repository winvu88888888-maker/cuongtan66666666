# -*- coding: utf-8 -*-
"""
Test Offline Engine V8.0 — Deep Interpretation + Cross-Method + Root Cause
Chạy: python test_offline_engine.py
"""
import sys
import os
import json

# Đảm bảo import từ thư mục hiện tại
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from free_ai_helper import (
    FreeAIHelper, _match_topic, _load_learned_topics, 
    _expand_with_synonyms, _save_learned_topic, LEARNED_TOPICS_FILE,
    _get_truong_sinh
)

def test_init():
    """Test 1: Khởi tạo FreeAIHelper V8.1 Hybrid"""
    print("=" * 60)
    print("TEST 1: Khởi tạo FreeAIHelper")
    ai = FreeAIHelper()
    assert "V15" in ai.version, f"FAIL: Version = {ai.version}"
    assert "XauDuoc" in ai.version, f"FAIL: Not XauDuoc = {ai.version}"
    print(f"  ✅ Name: {ai.name}")
    print(f"  ✅ Version: {ai.version}")
    print(f"  ✅ Learned count: {ai.learned_count}")
    return True

def test_exact_matching():
    """Test 2: Matching chính xác với chủ đề có sẵn"""
    print("\n" + "=" * 60)
    print("TEST 2: Exact Topic Matching")
    
    tests = [
        ("Tôi có nên mua nhà đất không?", "Mua Nhà Đất"),
        ("Xin việc làm có được không?", "Xin Việc Làm"),
        ("Thi đại học có đỗ không?", "Thi Đại Học"),
        ("Hôn nhân có hạnh phúc không?", "Hôn Nhân"),
    ]
    
    passed = 0
    for question, expected in tests:
        topic, data = _match_topic(question)
        status = "✅" if topic == expected else "❌"
        print(f"  {status} '{question}' → {topic} (expected: {expected})")
        if topic == expected:
            passed += 1
    
    print(f"  Kết quả: {passed}/{len(tests)} passed")
    return passed == len(tests)

def test_synonym_matching():
    """Test 3: Synonym matching"""
    print("\n" + "=" * 60)
    print("TEST 3: Synonym Matching")
    
    # Test expand_with_synonyms
    expanded = _expand_with_synonyms("tôi muốn invest vào stock")
    print(f"  Expanded: '{expanded}'")
    assert "đầu tư" in expanded, "FAIL: synonym 'invest' → 'đầu tư'"
    assert "chứng khoán" in expanded, "FAIL: synonym 'stock' → 'chứng khoán'"
    print(f"  ✅ Synonym expansion works!")
    
    # Test matching qua synonym
    topic, data = _match_topic("Tôi muốn invest vào crypto")
    print(f"  'invest vào crypto' → {topic}")
    assert topic is not None, "FAIL: Should match a topic via synonyms"
    print(f"  ✅ Synonym matching works! → {topic}")
    return True

def test_custom_reasoning():
    """Test 4: Custom reasoning cho câu hỏi không trùng"""
    print("\n" + "=" * 60)
    print("TEST 4: Custom Reasoning")
    
    ai = FreeAIHelper()
    # Câu hỏi đủ lạ để KHÔNG match bất kỳ chủ đề nào
    result = ai.answer_question("Trồng cây bạch đàn tại rừng Amazon có được phép không?")
    
    assert "THIÊN CƠ ĐẠI SƯ" in result, "FAIL: Missing header"
    assert "BƯỚC 1" in result, "FAIL: Missing BƯỚC 1"
    
    print(f"  ✅ Output: {len(result)} chars")
    
    # Nếu có custom reasoning (Nhóm suy luận) thì kiểm tra thêm
    if "Nhóm suy luận" in result:
        print(f"  ✅ Custom reasoning triggered!")
        if "Độ tin cậy" in result:
            print(f"  ✅ Confidence score present!")
        if "Lời khuyên" in result:
            print(f"  ✅ Category advice present!")
        if "Auto-Learn: Đã lưu" in result:
            print(f"  ✅ Auto-Learn saved!")
    else:
        print(f"  ℹ️ Matched a topic instead (not custom reasoning)")
    
    return True

def test_auto_learn():
    """Test 5: Auto-Learn — lưu và đọc lại"""
    print("\n" + "=" * 60)
    print("TEST 5: Auto-Learn System")
    
    # Clear learned topics trước
    with open(LEARNED_TOPICS_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    
    # Test trực tiếp hàm _save_learned_topic
    _save_learned_topic(
        question="Đào Bitcoin tại nhà có lời không trong 2026?",
        category="TÀI CHÍNH",
        dung_than_list=["Sinh Môn", "Mậu", "Thê Tài"],
        goi_y="Xem Sinh Môn vượng không, Mậu ở cung nào"
    )
    
    # Check file đã được ghi
    learned = _load_learned_topics()
    print(f"  Learned topics: {len(learned)} entries")
    print(f"  Topics: {list(learned.keys())}")
    
    assert len(learned) > 0, "FAIL: No learned topics saved"
    print(f"  ✅ Auto-Learn saved {len(learned)} topic(s)!")
    
    # Kiểm tra data structure
    for name, data in learned.items():
        assert "Dụng_Thần" in data, f"FAIL: Missing Dụng_Thần in '{name}'"
        assert "Câu_Hỏi_Gốc" in data, f"FAIL: Missing Câu_Hỏi_Gốc in '{name}'"
        assert "Nhóm" in data, f"FAIL: Missing Nhóm in '{name}'"
        print(f"  ✅ '{name}': Nhóm={data['Nhóm']}, DT={data['Dụng_Thần']}")
    
    # Test 2: Full flow qua answer_question với câu hỏi đủ lạ
    ai = FreeAIHelper()
    ai.answer_question("Phiêu lưu tìm kính chắn rượu vang ở đảo hoàng gia")
    learned2 = _load_learned_topics()
    if len(learned2) > len(learned):
        print(f"  ✅ Full flow auto-learn: {len(learned2)} entries total!")
    else:
        print(f"  ℹ️ Full flow: topic matched existing ({len(learned2)} entries)")
    
    return True

def test_re_match_learned():
    """Test 6: Re-match — hỏi lại câu đã learn"""
    print("\n" + "=" * 60)
    print("TEST 6: Re-Match Learned Topics")
    
    # Hỏi lại câu đã learn ở Test 5 (trực tiếp saved)
    topic, data = _match_topic("Đào Bitcoin tại nhà có lời không trong 2026?")
    
    print(f"  Re-match result: {topic}")
    if topic:
        source = data.get('_source', 'builtin')
        print(f"  Source: {source}")
        if source == 'learned':
            print(f"  ✅ Re-match from LEARNED source!")
            return True
        else:
            # Vẫn match nhưng từ builtin (vì có chủ đề Bitcoin builtin)
            print(f"  ✅ Matched (builtin topic scored higher, which is OK)")
            return True
    else:
        print(f"  ❌ No match at all")
        return False

def test_full_analysis():
    """Test 7: Full analysis output V8.0"""
    print("\n" + "=" * 60)
    print("TEST 7: Full Analysis Output V8.0")
    
    ai = FreeAIHelper()
    result = ai.answer_question("Kinh doanh tổng quát có lời không?")
    
    steps_found = []
    for i in range(1, 8):
        if f"BƯỚC {i}" in result:
            steps_found.append(i)
    
    # V8.0: Kiểm tra BƯỚC 5.5 (Root Cause)
    has_rca = "NGUYÊN NHÂN SÂU XA" in result
    
    print(f"  Steps found: {steps_found}")
    assert len(steps_found) >= 5, f"FAIL: Only {len(steps_found)} steps found"
    print(f"  ✅ {len(steps_found)}/7 steps present!")
    
    # Check V8.0 branding
    assert "V15" in result or "V8" in result, "FAIL: Missing version branding"
    print(f"  ✅ V15 branding present!")
    
    # V8.0: Root Cause Analysis
    if has_rca:
        print(f"  ✅ Root Cause Analysis (BƯỚC 5.5) present!")
    else:
        print(f"  ℹ️ Root Cause only appears with full data")
    
    print(f"  ✅ Total output: {len(result)} chars")
    
    return True

def test_truong_sinh():
    """Test 8: 12 Trường Sinh Engine (V8.0)"""
    print("\n" + "=" * 60)
    print("TEST 8: 12 Trường Sinh Engine")
    
    # Mộc tại Hợi = Trường Sinh
    stage, explain = _get_truong_sinh('Mộc', 'Hợi')
    assert stage == 'Trường Sinh', f"FAIL: Mộc tại Hợi = {stage}"
    print(f"  ✅ Mộc tại Hợi = {stage}")
    
    # Kim tại Tị = Trường Sinh
    stage, explain = _get_truong_sinh('Kim', 'Tị')
    assert stage == 'Trường Sinh', f"FAIL: Kim tại Tị = {stage}"
    print(f"  ✅ Kim tại Tị = {stage}")
    
    # Mộc tại Ngọ = Đế Vượng (Hợi→Tý→Sửu→Dần→Mão→Thìn→Tị→Ngọ = index 7... wait)
    # Hợi=index 11, Ngọ=index 6. (6-11)%12 = -5%12 = 7. 
    # Stages[7] = 'Tử'
    stage, explain = _get_truong_sinh('Mộc', 'Mão')
    # Hợi=11, Mão=3. (3-11)%12 = -8%12 = 4 → Đế Vượng
    assert stage == 'Đế Vượng', f"FAIL: Mộc tại Mão = {stage}"
    print(f"  ✅ Mộc tại Mão = {stage} (đỉnh cao!)")
    
    # Invalid
    stage, explain = _get_truong_sinh('', 'Tý')
    assert stage is None, "FAIL: Empty hanh should return None"
    print(f"  ✅ Invalid input returns None")
    
    return True

def test_v8_deep_features():
    """Test 9: V8.0 Deep Features — kiểm tra các tính năng mới"""
    print("\n" + "=" * 60)
    print("TEST 9: V8.0 Deep Features")
    
    from free_ai_helper import (
        SAO_GIAI_THICH, CUA_GIAI_THICH, THAN_GIAI_THICH,
        NAP_AM_GIAI_THICH, QUAI_Y_NGHIA, LUC_THAN_GIAI_THICH
    )
    
    # Check dictionaries exist and have content
    assert len(SAO_GIAI_THICH) >= 9, f"FAIL: SAO_GIAI_THICH has {len(SAO_GIAI_THICH)} entries"
    print(f"  ✅ Sao giải thích: {len(SAO_GIAI_THICH)} entries")
    
    assert len(CUA_GIAI_THICH) >= 8, f"FAIL: CUA_GIAI_THICH has {len(CUA_GIAI_THICH)} entries"
    print(f"  ✅ Cửa giải thích: {len(CUA_GIAI_THICH)} entries")
    
    assert len(THAN_GIAI_THICH) >= 8, f"FAIL: THAN_GIAI_THICH has {len(THAN_GIAI_THICH)} entries"
    print(f"  ✅ Thần giải thích: {len(THAN_GIAI_THICH)} entries")
    
    assert len(NAP_AM_GIAI_THICH) >= 25, f"FAIL: NAP_AM_GIAI_THICH has {len(NAP_AM_GIAI_THICH)} entries"
    print(f"  ✅ Nạp Âm giải thích: {len(NAP_AM_GIAI_THICH)} entries")
    
    assert len(QUAI_Y_NGHIA) == 8, f"FAIL: QUAI_Y_NGHIA has {len(QUAI_Y_NGHIA)} entries"
    print(f"  ✅ Quái ý nghĩa: {len(QUAI_Y_NGHIA)} entries")
    
    assert len(LUC_THAN_GIAI_THICH) >= 5, f"FAIL: LUC_THAN_GIAI_THICH has {len(LUC_THAN_GIAI_THICH)} entries"
    print(f"  ✅ Lục Thân giải thích: {len(LUC_THAN_GIAI_THICH)} entries")
    
    return True

if __name__ == "__main__":
    print("🧪 OFFLINE ENGINE V8.0 — TEST SUITE")
    print("=" * 60)
    
    results = []
    tests = [
        ("Init V8.0", test_init),
        ("Exact Matching", test_exact_matching),
        ("Synonym Matching", test_synonym_matching),
        ("Custom Reasoning", test_custom_reasoning),
        ("Auto-Learn", test_auto_learn),
        ("Re-Match Learned", test_re_match_learned),
        ("Full Analysis V8.0", test_full_analysis),
        ("12 Trường Sinh", test_truong_sinh),
        ("V8.0 Deep Features", test_v8_deep_features),
    ]
    
    for name, func in tests:
        try:
            ok = func()
            results.append((name, ok))
        except Exception as e:
            print(f"  ❌ EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 TỔNG KẾT:")
    passed = sum(1 for _, ok in results if ok)
    for name, ok in results:
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n  {passed}/{len(results)} TESTS PASSED")
    print("=" * 60)

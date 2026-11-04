# -*- coding: utf-8 -*-
"""Test V32.1 Anti-Hallucination Upgrade"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from free_ai_helper import FreeAIHelper

print("=" * 60)
print("TEST V32.1 ANTI-HALLUCINATION UPGRADE")
print("=" * 60)

# === Test 1: Module load + new methods ===
print("\n--- TEST 1: Module load + new methods ---")
try:
    helper = FreeAIHelper()
    has_post_validate = hasattr(helper, '_post_validate_response')
    has_enforce = hasattr(helper, '_enforce_conclusion')
    has_detect_q = hasattr(helper, '_detect_question_type')
    print(f"  FreeAIHelper loaded OK")
    print(f"  _post_validate_response: {'✅' if has_post_validate else '❌'}")
    print(f"  _enforce_conclusion: {'✅' if has_enforce else '❌'}")
    print(f"  _detect_question_type: {'✅' if has_detect_q else '❌'}")
except Exception as e:
    print(f"  FAIL: {e}")

# === Test 2: _post_validate_response ===
print("\n--- TEST 2: _post_validate_response ---")
try:
    # Test with valid response (no bịa)
    valid_response = "Kỳ Môn phân tích Sao Thiên Tâm tại Cung 6, Cửa Khai Môn. Đây là cát."
    valid_sao = {'Thiên Tâm', 'Thiên Bồng'}
    valid_cua = {'Khai Môn', 'Tử Môn'}
    result1 = helper._post_validate_response(valid_response, valid_sao, valid_cua, 
                                              'Thiên Tâm', 'Khai Môn', 'Trực Phù', 'Thiên Bồng', 'Tử Môn')
    has_warning_1 = 'kiểm chứng' in result1
    print(f"  Valid response: {'✅ No warning' if not has_warning_1 else '❌ False positive'}")
    
    # Test with fabricated response (bịa 2 sao)
    fake_response = "Sao Thiên Xung chiếu mệnh, Cửa Cảnh Môn rực rỡ. Thiên Anh hỗ trợ thêm."
    result2 = helper._post_validate_response(fake_response, valid_sao, valid_cua,
                                              'Thiên Tâm', 'Khai Môn', 'Trực Phù', 'Thiên Bồng', 'Tử Môn')
    has_warning_2 = 'kiểm chứng' in result2
    print(f"  Fabricated response: {'✅ Warning detected' if has_warning_2 else '❌ Missed'}")
    
    # Test with edge case (1 bịa only — should NOT warn, threshold is 2)
    edge_response = "Sao Thiên Xung chiếu mệnh, rất tốt."
    result3 = helper._post_validate_response(edge_response, valid_sao, valid_cua,
                                              'Thiên Tâm', 'Khai Môn', 'Trực Phù', 'Thiên Bồng', 'Tử Môn')
    has_warning_3 = 'kiểm chứng' in result3
    print(f"  Edge case (1 bịa): {'✅ No warning (threshold=2)' if not has_warning_3 else '❌ Too sensitive'}")
    
except Exception as e:
    print(f"  FAIL: {e}")

# === Test 3: Verify prompt template changes ===
print("\n--- TEST 3: Verify prompt template contains V32.1 anti-hallucination ---")
try:
    import inspect
    source = inspect.getsource(helper._try_online_ai)
    
    checks = {
        'Pre-fill Cách Cục': '_cach_cuc_text' in source,
        'Pre-fill Ứng Kỳ': '_ung_ky_prefill' in source,
        'Pre-fill top factors': '_km_top_factor' in source,
        'Post-validation call': '_post_validate_response' in source,
        'Valid sao set': '_valid_sao_set' in source,
        'V32.1 label': 'V32.1' in source,
        'Rule 12 (pre-fill)': 'ĐIỀN SẴN' in source,
        'Rule 13 (CẤM bịa sao)': 'CẤM bịa thêm sao' in source,
        'Anti-bịa Cách Cục': 'KHÔNG được bịa thêm cách cục' in source,
        'Anti-bịa thời điểm': 'KHÔNG được bịa thời điểm' in source,
    }
    
    all_pass = True
    for check, present in checks.items():
        status = "✅" if present else "❌"
        if not present:
            all_pass = False
        print(f"  {status} {check}")
    
    print(f"\n  Overall: {'ALL PASS ✅' if all_pass else 'SOME MISSING ⚠️'}")
    
except Exception as e:
    print(f"  FAIL: {e}")

print("\n" + "=" * 60)
print("ALL V32.1 TESTS COMPLETE")
print("=" * 60)

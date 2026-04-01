# -*- coding: utf-8 -*-
"""
Test V12.0 Lục Thân Relationship Engine
Chạy: python test_v12_luc_than.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from free_ai_helper import (
    FreeAIHelper, _get_luc_than_hanh, _ngu_hanh_relation,
    LUC_THAN_MEMBERS, LUC_THAN_NGU_HANH_MAP, SINH, KHAC
)

def test_version():
    """Test 1: Kiểm tra version V12.0"""
    print("=" * 60)
    print("TEST 1: Version V12.0")
    ai = FreeAIHelper()
    assert "V12.0" in ai.version, f"FAIL: version = {ai.version}"
    assert "V12.0" in ai.name, f"FAIL: name = {ai.name}"
    print(f"  ✅ Name: {ai.name}")
    print(f"  ✅ Version: {ai.version}")
    return True

def test_luc_than_members():
    """Test 2: Kiểm tra LUC_THAN_MEMBERS constant"""
    print("\n" + "=" * 60)
    print("TEST 2: LUC_THAN_MEMBERS")
    assert len(LUC_THAN_MEMBERS) == 7, f"FAIL: {len(LUC_THAN_MEMBERS)} members"
    expected = ['Bản Thân', 'Bố/Mẹ', 'Anh Chị Em', 'Vợ/Chồng', 'Con Cái', 'Sếp/Quan', 'Người Lạ']
    for name in expected:
        assert name in LUC_THAN_MEMBERS, f"FAIL: Missing {name}"
        info = LUC_THAN_MEMBERS[name]
        assert 'luc_than' in info, f"FAIL: {name} missing luc_than"
        assert 'km_can' in info, f"FAIL: {name} missing km_can"
        print(f"  ✅ {name}: {info['luc_than']} (Can: {info['km_can']})")
    return True

def test_get_luc_than_hanh():
    """Test 3: Kiểm tra _get_luc_than_hanh()"""
    print("\n" + "=" * 60)
    print("TEST 3: _get_luc_than_hanh()")
    
    # BT = Mộc
    # Huynh Đệ = tỷ hòa = Mộc
    assert _get_luc_than_hanh('Mộc', 'Huynh Đệ') == 'Mộc', "FAIL: Huynh Đệ != Mộc"
    print("  ✅ Huynh Đệ (BT=Mộc) = Mộc (tỷ hòa)")
    
    # Tử Tôn = BT sinh = Mộc sinh Hỏa
    assert _get_luc_than_hanh('Mộc', 'Tử Tôn') == 'Hỏa', "FAIL: Tử Tôn != Hỏa"
    print("  ✅ Tử Tôn (BT=Mộc) = Hỏa (BT sinh)")
    
    # Thê Tài = BT khắc = Mộc khắc Thổ
    assert _get_luc_than_hanh('Mộc', 'Thê Tài') == 'Thổ', "FAIL: Thê Tài != Thổ"
    print("  ✅ Thê Tài (BT=Mộc) = Thổ (BT khắc)")
    
    # Phụ Mẫu = sinh BT = Thủy sinh Mộc
    assert _get_luc_than_hanh('Mộc', 'Phụ Mẫu') == 'Thủy', "FAIL: Phụ Mẫu != Thủy"
    print("  ✅ Phụ Mẫu (BT=Mộc) = Thủy (sinh BT)")
    
    # Quan Quỷ = khắc BT = Kim khắc Mộc
    assert _get_luc_than_hanh('Mộc', 'Quan Quỷ') == 'Kim', "FAIL: Quan Quỷ != Kim"
    print("  ✅ Quan Quỷ (BT=Mộc) = Kim (khắc BT)")
    
    # Edge case: empty hanh
    assert _get_luc_than_hanh('', 'Huynh Đệ') == '?', "FAIL: empty hanh"
    assert _get_luc_than_hanh('?', 'Huynh Đệ') == '?', "FAIL: '?' hanh"
    print("  ✅ Edge cases (empty/unknown) = '?'")
    
    return True

def test_extract_dung_than():
    """Test 4: _extract_dung_than_from_all_methods()"""
    print("\n" + "=" * 60)
    print("TEST 4: _extract_dung_than_from_all_methods()")
    
    ai = FreeAIHelper()
    
    # Mock chart data
    chart = {
        'can_ngay': 'Giáp', 'chi_ngay': 'Tý',
        'can_gio': 'Bính', 'can_thang': 'Ất', 'can_nam': 'Nhâm',
        'can_thien_ban': {1: 'Giáp', 3: 'Bính', 5: 'Ất', 7: 'Nhâm'},
        'thien_ban': {1: 'Thiên Tâm', 3: 'Thiên Nhậm', 5: 'Thiên Xung', 7: 'Thiên Bồng'},
        'nhan_ban': {1: 'Khai Môn', 3: 'Sinh Môn', 5: 'Hưu Môn', 7: 'Tử Môn'},
        'than_ban': {1: 'Trực Phù', 3: 'Lục Hợp', 5: 'Thái Âm', 7: 'Huyền Vũ'},
    }
    
    result = ai._extract_dung_than_from_all_methods('Quan Quỷ', chart, None, None)
    
    assert 'Kỳ Môn' in result, "FAIL: Missing Kỳ Môn data"
    km = result['Kỳ Môn']
    assert km['can'] == 'Bính', f"FAIL: DT Can = {km['can']}"
    assert km['cung'] == 3, f"FAIL: DT Cung = {km['cung']}"
    print(f"  ✅ Kỳ Môn: DT (Bính) tại Cung {km['cung']} — Sao: {km.get('sao')}, Cửa: {km.get('cua')}")
    
    assert '_hanh_primary' in result, "FAIL: Missing hanh_primary"
    print(f"  ✅ Hành chính DT: {result['_hanh_primary']}")
    
    return True

def test_relationship_table():
    """Test 5: _build_luc_than_relationship_table() — output đầy đủ"""
    print("\n" + "=" * 60)
    print("TEST 5: _build_luc_than_relationship_table()")
    
    ai = FreeAIHelper()
    
    chart = {
        'can_ngay': 'Giáp', 'chi_ngay': 'Tý',
        'can_gio': 'Bính', 'can_thang': 'Ất', 'can_nam': 'Nhâm',
        'can_thien_ban': {1: 'Giáp', 3: 'Bính', 5: 'Ất', 7: 'Nhâm'},
        'thien_ban': {1: 'Thiên Tâm', 3: 'Thiên Nhậm', 5: 'Thiên Xung', 7: 'Thiên Bồng'},
        'nhan_ban': {1: 'Khai Môn', 3: 'Sinh Môn', 5: 'Hưu Môn', 7: 'Tử Môn'},
        'than_ban': {1: 'Trực Phù', 3: 'Lục Hợp', 5: 'Thái Âm', 7: 'Huyền Vũ'},
    }
    
    result = ai._build_luc_than_relationship_table(
        "Bố tôi có khỏe không?", "Phụ Mẫu", chart, None, None
    )
    
    assert len(result) > 100, f"FAIL: Output too short ({len(result)} chars)"
    print(f"  ✅ Output: {len(result)} chars")
    
    # Kiểm tra bảng có đủ thành viên
    for member in ['Bản Thân', 'Bố/Mẹ', 'Anh Chị Em', 'Vợ/Chồng', 'Con Cái', 'Sếp/Quan', 'Người Lạ']:
        assert member in result, f"FAIL: Missing {member}"
    print("  ✅ Tất cả 7 thành viên Lục Thân đều có trong bảng")
    
    # Kiểm tra có phần giúp/hại
    has_giup = 'GIÚP' in result or 'THUẬN' in result
    has_hai = 'HẠI' in result or 'HAO' in result
    print(f"  {'✅' if has_giup else '⚠️'} Có yếu tố GIÚP: {has_giup}")
    print(f"  {'✅' if has_hai else '⚠️'} Có yếu tố HẠI: {has_hai}")
    
    # Kiểm tra DT từ 5 phương pháp
    assert 'DỤNG THẦN QUA 5 PHƯƠNG PHÁP' in result, "FAIL: Missing 5-method section"
    print("  ✅ Phần DT qua 5 phương pháp hiện đầy đủ")
    
    print("\n--- SAMPLE OUTPUT ---")
    for line in result.split('\n')[:20]:
        print(f"  {line}")
    print("  ...")
    
    return True

def test_full_answer():
    """Test 6: Full answer_question() với V12.0"""
    print("\n" + "=" * 60)
    print("TEST 6: Full answer_question() V12.0")
    
    ai = FreeAIHelper()
    
    chart = {
        'can_ngay': 'Đinh', 'chi_ngay': 'Mão',
        'can_gio': 'Canh', 'can_thang': 'Nhâm', 'can_nam': 'Bính',
        'can_thien_ban': {1: 'Đinh', 4: 'Canh', 6: 'Nhâm', 9: 'Bính'},
        'thien_ban': {1: 'Thiên Phụ', 4: 'Thiên Trụ', 6: 'Thiên Anh', 9: 'Thiên Tâm'},
        'nhan_ban': {1: 'Cảnh Môn', 4: 'Thương Môn', 6: 'Đỗ Môn', 9: 'Khai Môn'},
        'than_ban': {1: 'Trực Phù', 4: 'Bạch Hổ', 6: 'Đằng Xà', 9: 'Cửu Thiên'},
    }
    
    result = ai.answer_question("Bố tôi có khỏe không?", chart_data=chart)
    
    assert 'V12.0' in result, "FAIL: Missing V12.0 in output"
    print(f"  ✅ V12.0 branding present")
    
    assert 'BƯỚC 1' in result, "FAIL: Missing BƯỚC 1"
    print(f"  ✅ BƯỚC 1 present")
    
    # Kiểm tra relationship table xuất hiện trong output
    has_luc_than = 'BẢNG QUAN HỆ LỤC THÂN' in result or 'QUAN HỆ LỤC THÂN' in result
    print(f"  {'✅' if has_luc_than else '⚠️'} Bảng Lục Thân Quan Hệ: {has_luc_than}")
    
    has_5pp = 'DỤNG THẦN QUA 5 PHƯƠNG PHÁP' in result
    print(f"  {'✅' if has_5pp else '⚠️'} DT qua 5 phương pháp: {has_5pp}")
    
    print(f"  ✅ Total output: {len(result)} chars")
    
    return True

if __name__ == "__main__":
    print("🧪 V12.0 LỤC THÂN RELATIONSHIP ENGINE — TEST SUITE")
    print("=" * 60)
    
    results = []
    tests = [
        ("Version V12.0", test_version),
        ("LUC_THAN_MEMBERS", test_luc_than_members),
        ("_get_luc_than_hanh()", test_get_luc_than_hanh),
        ("Extract DT All Methods", test_extract_dung_than),
        ("Relationship Table", test_relationship_table),
        ("Full Answer V12.0", test_full_answer),
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

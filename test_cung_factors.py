# -*- coding: utf-8 -*-
"""
Test V15.0 Xâu Dược — Phân tích Nội Cung Kỳ Môn
Chạy: python test_cung_factors.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from free_ai_helper import (
    FreeAIHelper, _get_khong_vong, _check_phan_phuc_ngam,
    CUNG_NGU_HANH, QUAI_TUONG, SINH, KHAC, DICH_MA_MAP
)

def make_mock_chart(can_ngay='Giáp', chi_ngay='Tý', can_gio='Bính',
                    thien_ban=None, nhan_ban=None, than_ban=None,
                    can_thien_ban=None, dia_ban=None):
    """Tạo mock chart data cho test"""
    return {
        'can_ngay': can_ngay,
        'chi_ngay': chi_ngay,
        'can_gio': can_gio,
        'can_nam': 'Mậu',
        'can_thang': 'Canh',
        'chi_gio': 'Ngọ',
        'thien_ban': thien_ban or {
            1: 'Thiên Tâm', 2: 'Thiên Bồng', 3: 'Thiên Nhậm',
            4: 'Thiên Xung', 6: 'Thiên Nhuế', 7: 'Thiên Phụ',
            8: 'Thiên Anh', 9: 'Thiên Trụ',
        },
        'nhan_ban': nhan_ban or {
            1: 'Khai Môn', 2: 'Tử Môn', 3: 'Sinh Môn',
            4: 'Thương Môn', 6: 'Hưu Môn', 7: 'Cảnh Môn',
            8: 'Đỗ Môn', 9: 'Kinh Môn',
        },
        'than_ban': than_ban or {
            1: 'Trực Phù', 2: 'Đằng Xà', 3: 'Lục Hợp',
            4: 'Thái Âm', 6: 'Bạch Hổ', 7: 'Cửu Thiên',
            8: 'Huyền Vũ', 9: 'Cửu Địa',
        },
        'can_thien_ban': can_thien_ban or {
            1: 'Mậu', 2: 'Kỷ', 3: 'Canh', 4: 'Tân',
            6: 'Nhâm', 7: 'Quý', 8: 'Bính', 9: 'Đinh',
        },
        'dia_ban': dia_ban or {
            1: 'Mậu', 2: 'Kỷ', 3: 'Canh', 4: 'Tân',
            6: 'Nhâm', 7: 'Quý', 8: 'Ất', 9: 'Đinh',
        },
    }

def test_cung_factors_cat():
    """Test 1: Cung có nhiều yếu tố CÁT → score > 0"""
    print("=" * 60)
    print("TEST 1: Cung CÁT (Sao Cát + Cửa Cát + Thần Cát)")
    
    ai = FreeAIHelper()
    # Cung 1: Thiên Tâm (Cát) + Khai Môn (Đại Cát) + Trực Phù (Cát)
    chart = make_mock_chart()
    score, details, strength = ai._analyze_cung_factors(1, chart, "Tôi có nên đầu tư?", "BẢN THÂN")
    
    print(f"  Score: {score}")
    print(f"  Strength: {strength}")
    for d in details[:8]:
        print(f"  {d}")
    if len(details) > 8:
        print(f"  ... và {len(details)-8} dòng nữa")
    
    assert score > 0, f"FAIL: Score={score}, expected > 0 for all-cat cung"
    assert "VƯỢNG" in strength or "TƯỚNG" in strength, f"FAIL: Strength={strength}, expected VƯỢNG/TƯỚNG"
    print(f"  ✅ PASS: Score={score}, {strength}")
    return True

def test_cung_factors_hung():
    """Test 2: Cung có nhiều yếu tố HUNG → score < 0"""
    print("\n" + "=" * 60)
    print("TEST 2: Cung HUNG (Sao Hung + Cửa Hung + Thần Hung)")
    
    ai = FreeAIHelper()
    # Cung 2: Thiên Bồng (Hung) + Tử Môn (Đại Hung) + Đằng Xà (Hung)
    chart = make_mock_chart()
    score, details, strength = ai._analyze_cung_factors(2, chart, "Bệnh có nặng không?", "DỤNG THẦN (Quan Quỷ)")
    
    print(f"  Score: {score}")
    print(f"  Strength: {strength}")
    for d in details[:8]:
        print(f"  {d}")
    
    assert score < 0, f"FAIL: Score={score}, expected < 0 for hung cung"
    assert "TÙ" in strength or "TỬ" in strength, f"FAIL: Strength={strength}, expected TÙ/TỬ"
    print(f"  ✅ PASS: Score={score}, {strength}")
    return True

def test_cach_cuc_81():
    """Test 3: 81 Cách Cục detection"""
    print("\n" + "=" * 60)
    print("TEST 3: 81 Cách Cục (Can Thiên × Địa)")
    
    ai = FreeAIHelper()
    # Cung 8: Can Thiên = Bính, Can Địa = Ất → "Nhật Nguyệt Tinh Hành" = CÁT
    chart = make_mock_chart(
        can_thien_ban={8: 'Bính', 1: 'Mậu', 2: 'Kỷ', 3: 'Canh', 4: 'Tân', 6: 'Nhâm', 7: 'Quý', 9: 'Đinh'},
        dia_ban={8: 'Ất', 1: 'Mậu', 2: 'Kỷ', 3: 'Canh', 4: 'Tân', 6: 'Nhâm', 7: 'Quý', 9: 'Đinh'},
    )
    score, details, strength = ai._analyze_cung_factors(8, chart, "Có nên khởi nghiệp?", "BẢN THÂN")
    
    # Check Cách Cục is detected  
    cach_found = any("Cách Cục" in d for d in details)
    print(f"  Score: {score}")
    print(f"  Cách Cục detected: {cach_found}")
    for d in details:
        if "Cách" in d or "📖" in d:
            print(f"  → {d}")
    
    assert cach_found, "FAIL: Cách Cục not detected for Bính+Ất"
    print(f"  ✅ PASS: Cách Cục detected, Score={score}")
    return True

def test_tuan_khong():
    """Test 4: Tuần Không detection"""
    print("\n" + "=" * 60)
    print("TEST 4: Tuần Không lâm cung")
    
    ai = FreeAIHelper()
    # Giáp Tý tuần → Tuần Không = [Tuất, Hợi]
    # Cung 6 = Chi Tuất → lâm Tuần Không!
    chart = make_mock_chart(can_ngay='Giáp', chi_ngay='Tý')
    score, details, strength = ai._analyze_cung_factors(6, chart, "Việc có thành không?", "DỤNG THẦN")
    
    tuan_khong_found = any("TUẦN KHÔNG" in d for d in details)
    print(f"  Score: {score}")
    print(f"  Tuần Không detected: {tuan_khong_found}")
    for d in details:
        if "TUẦN KHÔNG" in d:
            print(f"  → {d}")
    
    assert tuan_khong_found, "FAIL: Tuần Không not detected for Cung 6 (Tuất) in Giáp Tý tuần"
    print(f"  ✅ PASS: Tuần Không detected at Cung 6, Score={score}")
    return True

def test_dich_ma():
    """Test 5: Dịch Mã detection"""
    print("\n" + "=" * 60)
    print("TEST 5: Dịch Mã")
    
    ai = FreeAIHelper()
    # Chi ngày = Tý → Dịch Mã tại Dần (Thủy cục)
    # Cung 3 = Chi Dần → lâm Dịch Mã!
    chart = make_mock_chart(chi_ngay='Tý')
    score, details, strength = ai._analyze_cung_factors(3, chart, "Tôi có nên đi du lịch?", "BẢN THÂN")
    
    dich_ma_found = any("DỊCH MÃ" in d for d in details)
    print(f"  Score: {score}")
    print(f"  Dịch Mã detected: {dich_ma_found}")
    for d in details:
        if "DỊCH MÃ" in d:
            print(f"  → {d}")
    
    assert dich_ma_found, "FAIL: Dịch Mã not detected for Cung 3 (Dần) with Chi ngày Tý"
    print(f"  ✅ PASS: Dịch Mã detected at Cung 3")
    return True

def test_invalid_input():
    """Test 6: Invalid input → graceful handling"""
    print("\n" + "=" * 60)
    print("TEST 6: Invalid input")
    
    ai = FreeAIHelper()
    score, details, strength = ai._analyze_cung_factors(None, {}, "", "BẢN THÂN")
    assert score == 0 and len(details) == 0, f"FAIL: Expected (0, [], '?') for None input"
    print(f"  ✅ None cung: score={score}, details={len(details)}")
    
    score, details, strength = ai._analyze_cung_factors(5, make_mock_chart(), "", "BẢN THÂN")
    print(f"  ✅ Cung 5 (Trung): score={score}, details={len(details)}")
    return True

def test_full_integration():
    """Test 7: Full integration trong _build_element_impact_analysis"""
    print("\n" + "=" * 60)
    print("TEST 7: Full Integration")
    
    ai = FreeAIHelper()
    chart = make_mock_chart()
    
    impact_text, direct_answer, evidence = ai._build_element_impact_analysis(
        question="Tôi có nên đầu tư không?",
        dung_than="Thê Tài",
        category_label="TÀI CHÍNH",
        chart_data=chart,
        luc_hao_data=None,
        mai_hoa_data=None,
        ky_mon_verdict="CÁT",
        luc_hao_verdict="BÌNH",
        mai_hoa_verdict="CÁT",
        ky_mon_reason="Sao cát cửa cát",
        luc_hao_reason="",
        mai_hoa_reason="Quẻ tốt",
    )
    
    has_noi_cung = "NỘI CUNG" in impact_text
    has_score = "TỔNG ĐIỂM CUNG" in impact_text
    has_cung_evidence = any("NộiCung" in e for e in evidence)
    
    print(f"  Impact text length: {len(impact_text)} chars")
    print(f"  Has NỘI CUNG analysis: {has_noi_cung}")
    print(f"  Has TỔNG ĐIỂM CUNG: {has_score}")
    print(f"  Has cung evidence: {has_cung_evidence}")
    print(f"  Evidence list: {evidence[:5]}")
    
    assert has_noi_cung, "FAIL: NỘI CUNG not in impact_text"
    assert has_score, "FAIL: TỔNG ĐIỂM CUNG not in impact_text"
    print(f"  ✅ PASS: V15.0 Nội Cung integrated into impact analysis")
    return True

def test_version():
    """Test 8: Version check"""
    print("\n" + "=" * 60)
    print("TEST 8: Version Check")
    
    ai = FreeAIHelper()
    assert "V15.0" in ai.version, f"FAIL: Version={ai.version}"
    assert "XauDuoc" in ai.version, f"FAIL: Version={ai.version}"
    print(f"  ✅ Version: {ai.version}")
    print(f"  ✅ Name: {ai.name}")
    return True

if __name__ == "__main__":
    print("🧪 V15.0 XÂU DƯỢC — TEST SUITE")
    print("=" * 60)
    
    results = []
    tests = [
        ("Version Check", test_version),
        ("Cung CÁT", test_cung_factors_cat),
        ("Cung HUNG", test_cung_factors_hung),
        ("81 Cách Cục", test_cach_cuc_81),
        ("Tuần Không", test_tuan_khong),
        ("Dịch Mã", test_dich_ma),
        ("Invalid Input", test_invalid_input),
        ("Full Integration", test_full_integration),
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

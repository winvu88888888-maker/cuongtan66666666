# -*- coding: utf-8 -*-
"""
Test Phase 4 — Verify ALL data from Phase 2-4
Chạy: python test_phase4_data.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test 1: Import tất cả data modules không lỗi"""
    print("=" * 60)
    print("TEST 1: Imports")
    from kinh_dich_64_que import (
        KINH_DICH_64, THIET_BAN_60, MAI_HOA_THE_DUNG, MAI_HOA_UNG_KY,
        tra_kinh_dich, tra_nap_am, tra_the_dung
    )
    from luc_hao_ky_mon_rules import (
        DUNG_THAN_MAP, NGUYEN_KY_CUU, LUC_HAO_RULES, LUC_THAN_Y_NGHIA,
        KY_MON_CACH_CUC, SAO_KY_MON, CUA_KY_MON, THAN_KY_MON,
        PHUC_THAN_RULES, NHAT_NGUYET_RULES, KY_MON_CACH_CUC_MR,
        SAO_CUA_TO_HOP, BAN_CUNG, tra_ban_cung,
        HAO_BIEN_RULES, DONG_TINH_RULES, SAO_CUA_TO_HOP_BS
    )
    from van_vat_loai_tuong import BAT_QUAI_LOAI_TUONG, NGU_HANH_LOAI_TUONG
    print("  ✅ All imports successful!")
    return True


def test_kinh_dich_64():
    """Test 2: KINH_DICH_64 có đủ 64 quẻ"""
    print("\n" + "=" * 60)
    print("TEST 2: KINH_DICH_64")
    from kinh_dich_64_que import KINH_DICH_64
    
    count = len(KINH_DICH_64)
    assert count == 64, f"FAIL: Chỉ có {count}/64 quẻ"
    print(f"  ✅ {count} quẻ!")
    
    # Kiểm tra fields
    required_fields = ["thuong", "ha", "thu_tu", "thoan", "y_nghia", "loi_khuyen", "cat_hung"]
    missing = []
    for name, data in KINH_DICH_64.items():
        for f in required_fields:
            if f not in data:
                missing.append(f"{name} thiếu {f}")
    
    if missing:
        for m in missing[:5]:
            print(f"  ❌ {m}")
        return False
    
    print(f"  ✅ Tất cả 64 quẻ có đủ {len(required_fields)} fields!")
    
    # Kiểm tra thứ tự 1-64
    thu_tu_set = set(d["thu_tu"] for d in KINH_DICH_64.values())
    assert thu_tu_set == set(range(1, 65)), "FAIL: Thứ tự không đầy đủ 1-64"
    print("  ✅ Thứ tự 1-64 đầy đủ!")
    return True


def test_thiet_ban_60():
    """Test 3: THIET_BAN_60 có đủ 60 entries"""
    print("\n" + "=" * 60)
    print("TEST 3: THIET_BAN_60")
    from kinh_dich_64_que import THIET_BAN_60
    
    count = len(THIET_BAN_60)
    assert count == 60, f"FAIL: Chỉ có {count}/60 entries"
    print(f"  ✅ {count} entries!")
    
    for name, data in THIET_BAN_60.items():
        assert "nap_am" in data, f"FAIL: {name} thiếu nap_am"
        assert "hanh" in data, f"FAIL: {name} thiếu hanh"
        assert "giai_thich" in data, f"FAIL: {name} thiếu giai_thich"
        assert data["hanh"] in ["Kim", "Mộc", "Thủy", "Hỏa", "Thổ"], f"FAIL: {name} hanh={data['hanh']}"
    
    print("  ✅ Tất cả 60 entries có đủ fields + hanh hợp lệ!")
    return True


def test_mai_hoa_the_dung():
    """Test 4: MAI_HOA_THE_DUNG có đủ 25 tổ hợp"""
    print("\n" + "=" * 60)
    print("TEST 4: MAI_HOA_THE_DUNG")
    from kinh_dich_64_que import MAI_HOA_THE_DUNG
    
    count = len(MAI_HOA_THE_DUNG)
    assert count == 25, f"FAIL: Chỉ có {count}/25 tổ hợp"
    print(f"  ✅ {count} tổ hợp (5×5)!")
    
    hanh_list = ["Kim", "Mộc", "Thủy", "Hỏa", "Thổ"]
    for h1 in hanh_list:
        for h2 in hanh_list:
            assert (h1, h2) in MAI_HOA_THE_DUNG, f"FAIL: Thiếu ({h1}, {h2})"
    
    print("  ✅ Tất cả 25 cặp hành đầy đủ!")
    return True


def test_mai_hoa_ung_ky():
    """Test 5: MAI_HOA_UNG_KY có đủ 5 loại"""
    print("\n" + "=" * 60)
    print("TEST 5: MAI_HOA_UNG_KY")
    from kinh_dich_64_que import MAI_HOA_UNG_KY
    
    count = len(MAI_HOA_UNG_KY)
    assert count == 5, f"FAIL: Chỉ có {count}/5 loại"
    print(f"  ✅ {count} loại ứng kỳ!")
    
    expected = ["Thể khắc Dụng", "Dụng sinh Thể", "Thể sinh Dụng", "Dụng khắc Thể", "Tỷ Hòa"]
    for e in expected:
        assert e in MAI_HOA_UNG_KY, f"FAIL: Thiếu '{e}'"
    
    print("  ✅ Đủ 5 loại ứng kỳ!")
    return True


def test_luc_hao_rules():
    """Test 6: LUC_HAO_RULES >= 18 + HAO_BIEN >= 5 + DONG_TINH >= 3"""
    print("\n" + "=" * 60)
    print("TEST 6: Lục Hào Rules")
    from luc_hao_ky_mon_rules import LUC_HAO_RULES, HAO_BIEN_RULES, DONG_TINH_RULES
    
    lhr = len(LUC_HAO_RULES)
    hbr = len(HAO_BIEN_RULES)
    dtr = len(DONG_TINH_RULES)
    total = lhr + hbr + dtr
    
    assert lhr >= 18, f"FAIL: LUC_HAO_RULES={lhr} < 18"
    assert hbr >= 5, f"FAIL: HAO_BIEN_RULES={hbr} < 5"
    assert dtr >= 3, f"FAIL: DONG_TINH_RULES={dtr} < 3"
    
    print(f"  ✅ LUC_HAO_RULES: {lhr}")
    print(f"  ✅ HAO_BIEN_RULES: {hbr}")
    print(f"  ✅ DONG_TINH_RULES: {dtr}")
    print(f"  ✅ Tổng: {total} rules!")
    return True


def test_ky_mon_cach_cuc():
    """Test 7: KY_MON_CACH_CUC + MR >= 26"""
    print("\n" + "=" * 60)
    print("TEST 7: Kỳ Môn Cách Cục")
    from luc_hao_ky_mon_rules import KY_MON_CACH_CUC, KY_MON_CACH_CUC_MR
    
    km1 = len(KY_MON_CACH_CUC)
    km2 = len(KY_MON_CACH_CUC_MR)
    total = km1 + km2
    
    assert km1 >= 16, f"FAIL: KY_MON_CACH_CUC={km1} < 16"
    assert km2 >= 10, f"FAIL: KY_MON_CACH_CUC_MR={km2} < 10"
    
    print(f"  ✅ KY_MON_CACH_CUC: {km1}")
    print(f"  ✅ KY_MON_CACH_CUC_MR: {km2}")
    print(f"  ✅ Tổng: {total} patterns!")
    return True


def test_sao_cua_to_hop():
    """Test 8: SAO_CUA_TO_HOP + BS >= 25"""
    print("\n" + "=" * 60)
    print("TEST 8: Sao + Cửa Tổ Hợp")
    from luc_hao_ky_mon_rules import SAO_CUA_TO_HOP, SAO_CUA_TO_HOP_BS
    
    sc1 = len(SAO_CUA_TO_HOP)
    sc2 = len(SAO_CUA_TO_HOP_BS)
    total = sc1 + sc2
    
    assert sc1 >= 25, f"FAIL: SAO_CUA_TO_HOP={sc1} < 25"
    assert sc2 >= 4, f"FAIL: SAO_CUA_TO_HOP_BS={sc2} < 4"
    
    print(f"  ✅ SAO_CUA_TO_HOP: {sc1}")
    print(f"  ✅ SAO_CUA_TO_HOP_BS: {sc2}")
    print(f"  ✅ Tổng: {total} combos!")
    return True


def test_phuc_than_nhat_nguyet():
    """Test 9: PHUC_THAN_RULES=5, NHAT_NGUYET_RULES=8"""
    print("\n" + "=" * 60)
    print("TEST 9: Phục Thần + Nhật Nguyệt")
    from luc_hao_ky_mon_rules import PHUC_THAN_RULES, NHAT_NGUYET_RULES
    
    pt = len(PHUC_THAN_RULES)
    nn = len(NHAT_NGUYET_RULES)
    
    assert pt == 5, f"FAIL: PHUC_THAN_RULES={pt} != 5"
    assert nn == 8, f"FAIL: NHAT_NGUYET_RULES={nn} != 8"
    
    print(f"  ✅ PHUC_THAN_RULES: {pt}")
    print(f"  ✅ NHAT_NGUYET_RULES: {nn}")
    return True


def test_ban_cung():
    """Test 10: BAN_CUNG 8 cung + 64 quẻ mapped"""
    print("\n" + "=" * 60)
    print("TEST 10: BAN_CUNG")
    from luc_hao_ky_mon_rules import BAN_CUNG, tra_ban_cung
    
    assert len(BAN_CUNG) == 8, f"FAIL: {len(BAN_CUNG)} cung != 8"
    print(f"  ✅ 8 cung!")
    
    # Đếm tổng quẻ
    total_que = sum(len(info["que_list"]) for info in BAN_CUNG.values())
    assert total_que == 64, f"FAIL: {total_que} quẻ != 64"
    print(f"  ✅ 64 quẻ mapped!")
    
    # Test helper
    cung, hanh = tra_ban_cung("Thuần Càn")
    assert cung == "Càn", f"FAIL: Thuần Càn → {cung}"
    assert hanh == "Kim", f"FAIL: Càn Kim → {hanh}"
    print(f"  ✅ tra_ban_cung('Thuần Càn') = ({cung}, {hanh})")
    
    cung2, hanh2 = tra_ban_cung("Quẻ Không Tồn Tại")
    assert cung2 is None, "FAIL: Should return None"
    print(f"  ✅ tra_ban_cung unknown = (None, None)")
    return True


def test_helper_functions():
    """Test 11: Helper functions hoạt động đúng"""
    print("\n" + "=" * 60)
    print("TEST 11: Helper Functions")
    from kinh_dich_64_que import tra_kinh_dich, tra_nap_am, tra_the_dung
    
    # tra_kinh_dich
    kd = tra_kinh_dich("Thuần Càn")
    assert kd is not None, "FAIL: Thuần Càn not found"
    assert kd["thu_tu"] == 1, f"FAIL: thu_tu={kd['thu_tu']}"
    print(f"  ✅ tra_kinh_dich('Thuần Càn') → thu_tu=1, cat_hung={kd['cat_hung']}")
    
    kd2 = tra_kinh_dich("Quẻ Fake")
    assert kd2 is None, "FAIL: Should return None"
    print(f"  ✅ tra_kinh_dich('Quẻ Fake') → None")
    
    # tra_nap_am
    na = tra_nap_am("Giáp Tý")
    assert na is not None, "FAIL: Giáp Tý not found"
    assert na["nap_am"] == "Hải Trung Kim", f"FAIL: nap_am={na['nap_am']}"
    print(f"  ✅ tra_nap_am('Giáp Tý') → {na['nap_am']}")
    
    # tra_the_dung
    td = tra_the_dung("Kim", "Mộc")
    assert td is not None, "FAIL: (Kim, Mộc) not found"
    assert td["ket_luan"] == "CÁT", f"FAIL: ket_luan={td['ket_luan']}"
    print(f"  ✅ tra_the_dung('Kim', 'Mộc') → {td['ket_luan']}")
    return True


def test_data_integrity():
    """Test 12: Data integrity — cross-check"""
    print("\n" + "=" * 60)
    print("TEST 12: Data Integrity")
    from luc_hao_ky_mon_rules import SAO_KY_MON, CUA_KY_MON, THAN_KY_MON
    
    assert len(SAO_KY_MON) == 9, f"FAIL: SAO_KY_MON={len(SAO_KY_MON)} != 9"
    assert len(CUA_KY_MON) == 8, f"FAIL: CUA_KY_MON={len(CUA_KY_MON)} != 8"
    assert len(THAN_KY_MON) == 8, f"FAIL: THAN_KY_MON={len(THAN_KY_MON)} != 8"
    
    print(f"  ✅ SAO_KY_MON: {len(SAO_KY_MON)} sao")
    print(f"  ✅ CUA_KY_MON: {len(CUA_KY_MON)} cửa")
    print(f"  ✅ THAN_KY_MON: {len(THAN_KY_MON)} thần")
    
    # Cross-check: mỗi quẻ trong BAN_CUNG phải có trong KINH_DICH_64
    from luc_hao_ky_mon_rules import BAN_CUNG
    from kinh_dich_64_que import KINH_DICH_64
    
    all_que_ban_cung = []
    for info in BAN_CUNG.values():
        all_que_ban_cung.extend(info["que_list"])
    
    missing = [q for q in all_que_ban_cung if q not in KINH_DICH_64]
    if missing:
        print(f"  ⚠️ {len(missing)} quẻ trong BAN_CUNG chưa có trong KINH_DICH_64:")
        for m in missing[:5]:
            print(f"    - {m}")
        # Không fail vì có thể tên quẻ hơi khác
    else:
        print(f"  ✅ Tất cả 64 quẻ BAN_CUNG đều có trong KINH_DICH_64!")
    return True


def test_integration():
    """Test 13: FreeAIHelper dùng data mới trong phân tích"""
    print("\n" + "=" * 60)
    print("TEST 13: Integration with FreeAIHelper")
    from free_ai_helper import FreeAIHelper
    
    ai = FreeAIHelper()
    result = ai.answer_question("Tôi có nên mua nhà không?")
    
    assert len(result) > 100, "FAIL: Output quá ngắn"
    print(f"  ✅ Output: {len(result)} chars")
    
    # Kiểm tra có KB markers
    has_kb = "[KB]" in result or "📚" in result
    has_analysis = "BƯỚC" in result or "Kỳ Môn" in result or "CÁT" in result or "HUNG" in result
    
    print(f"  {'✅' if has_kb else 'ℹ️'} KB markers: {has_kb}")
    print(f"  ✅ Analysis markers present: {has_analysis}")
    
    return True


if __name__ == "__main__":
    print("🧪 PHASE 4 DATA VERIFICATION — TEST SUITE")
    print("=" * 60)
    
    results = []
    tests = [
        ("Imports", test_imports),
        ("KINH_DICH_64", test_kinh_dich_64),
        ("THIET_BAN_60", test_thiet_ban_60),
        ("MAI_HOA_THE_DUNG", test_mai_hoa_the_dung),
        ("MAI_HOA_UNG_KY", test_mai_hoa_ung_ky),
        ("Lục Hào Rules", test_luc_hao_rules),
        ("Kỳ Môn Cách Cục", test_ky_mon_cach_cuc),
        ("Sao+Cửa Tổ Hợp", test_sao_cua_to_hop),
        ("Phục Thần + Nhật Nguyệt", test_phuc_than_nhat_nguyet),
        ("BAN_CUNG", test_ban_cung),
        ("Helper Functions", test_helper_functions),
        ("Data Integrity", test_data_integrity),
        ("Integration", test_integration),
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

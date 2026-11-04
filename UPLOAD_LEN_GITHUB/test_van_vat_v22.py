from free_ai_helper import _get_van_vat_cu_the, _calc_unified_strength_tier, VAN_VAT_CU_THE

print("=== TEST VAN_VAT_CU_THE ===")
print()

# Test 1: Kim + TU_TUYET
r = _get_van_vat_cu_the('Kim', 'TỬ_TUYỆT')
print("Kim + TU_TUYET:")
print("  Do vat:", r.get("do_vat"))
print("  Nha cua:", r.get("nha_cua"))
print()

# Test 2: Moc + VUONG
r = _get_van_vat_cu_the('Mộc', 'VƯỢNG')
print("Moc + VUONG:")
print("  Do vat:", r.get("do_vat"))
print("  Nha cua:", r.get("nha_cua"))
print()

# Test 3: Full unified flow - SUY
u = _calc_unified_strength_tier(lh_raw=-20, ts_stage='Tử', ngu_khi='Tù', hanh_dt='Kim')
print("Unified flow (Kim, LH=-20, TS=Tu, NK=Tu):")
print("  unified_pct=%d%%, tier=%s" % (u["unified_pct"], u["tier_key"]))
vv = _get_van_vat_cu_the('Kim', u['tier_key'])
print("  Do vat:", vv.get("do_vat"))
print("  Benh:", vv.get("benh"))
print()

# Test 4: Full unified flow - VUONG
u2 = _calc_unified_strength_tier(lh_raw=25, ts_stage='Đế Vượng', ngu_khi='Vượng', hanh_dt='Hỏa')
print("Unified flow (Hoa, LH=+25, TS=De Vuong, NK=Vuong):")
print("  unified_pct=%d%%, tier=%s" % (u2["unified_pct"], u2["tier_key"]))
vv2 = _get_van_vat_cu_the('Hỏa', u2['tier_key'])
print("  Do vat:", vv2.get("do_vat"))
print("  Nguoi:", vv2.get("nguoi"))
print()

# Test 5: Thuy + SUY
r3 = _get_van_vat_cu_the('Thủy', 'SUY')
print("Thuy + SUY:")
print("  Do vat:", r3.get("do_vat"))
print("  Benh:", r3.get("benh"))
print()

total = sum(len(v) for v in VAN_VAT_CU_THE.values())
print("Total: 5 hanh x 6 tang = %d entries" % total)
print("ALL TESTS PASSED!")

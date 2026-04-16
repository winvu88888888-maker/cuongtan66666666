# -*- coding: utf-8 -*-
"""
TEST TOÀN DIỆN V32.5 — 3 Phần:
  PHẦN 1: DT + Phân loại câu hỏi (40+ cases)
  PHẦN 2: Sơ đồ + Yếu tố (SD MASTER, SD1-SD16)
  PHẦN 3: Kết luận khớp câu hỏi
"""
import sys, os
sys.path.insert(0, '.')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from question_parser import parse_question, format_parsed_questions_v2

pass_count = 0
fail_count = 0

def check(label, got, expected):
    global pass_count, fail_count
    ok = got == expected
    icon = '✅' if ok else '❌'
    if ok:
        pass_count += 1
    else:
        fail_count += 1
        print(f"    {icon} {label}: GOT={got} | EXPECTED={expected}")
    return ok

# ═══════════════════════════════════════════════════════════════
# PHẦN 1: DT + PHÂN LOẠI — 40+ câu hỏi đa dạng
# ═══════════════════════════════════════════════════════════════
print("=" * 80)
print("PHẦN 1: DỤNG THẦN + PHÂN LOẠI CÂU HỎI")
print("=" * 80)

DT_TESTS = [
    # === NGƯỜI — Lục Thân ===
    # (câu hỏi, expected_dt, expected_diagram_prefix, description)
    ("bố tôi bệnh nặng không", "Phụ Mẫu", "SD", "Bố = Phụ Mẫu"),
    ("mẹ tôi khỏe không", "Phụ Mẫu", "SD", "Mẹ = Phụ Mẫu"),
    ("ông ngoại có qua khỏi không", "Phụ Mẫu", "SD", "Ông = Phụ Mẫu"),
    ("vợ tôi ngoại tình không", "Thê Tài", "SD", "Vợ = Thê Tài"),
    ("chồng tôi có thăng chức không", "Quan Quỷ", "SD", "Chồng = Quan Quỷ"),
    ("con trai thi đỗ không", "Tử Tôn", "SD", "Con trai = Tử Tôn"),
    ("con gái lấy chồng được không", "Tử Tôn", "SD", "Con gái = Tử Tôn"),
    ("anh tôi xin việc được không", "Huynh Đệ", "SD", "Anh = Huynh Đệ"),
    ("chị tôi buôn bán có lời không", "Huynh Đệ", "SD", "Chị = Huynh Đệ"),
    ("em tôi đi nước ngoài được không", "Huynh Đệ", "SD", "Em = Huynh Đệ"),
    ("sếp có cho tăng lương không", "Quan Quỷ", "SD", "Sếp = Quan Quỷ"),
    ("bạn trai có tốt không", "Quan Quỷ", "SD", "Bạn trai = Quan Quỷ"),
    ("người yêu có thật lòng không", "Thê Tài", "SD", "Người yêu = Thê Tài"),
    
    # === VẬT — Vạn Vật Loại Tượng ===
    ("xe tôi bán được không", "Phụ Mẫu", "SD", "Xe = Phụ Mẫu (che chở)"),
    ("nhà có bán được giá không", "Phụ Mẫu", "SD", "Nhà = Phụ Mẫu (che chở)"),
    ("hợp đồng ký được không", "Phụ Mẫu", "SD", "Hợp đồng = Phụ Mẫu (văn thư)"),
    ("giấy tờ bao giờ xong", "Phụ Mẫu", "SD", "Giấy tờ = Phụ Mẫu (văn thư)"),
    ("tiền mất ở đâu", "Thê Tài", "SD", "Tiền = Thê Tài"),
    ("điện thoại mất tìm đâu", "Thê Tài", "SD", "Điện thoại = Thê Tài"),
    ("bệnh có nặng không", "Quan Quỷ", "SD", "Bệnh = Quan Quỷ"),
    ("kiện tụng có thắng không", "Quan Quỷ", "SD", "Kiện = Quan Quỷ"),
    ("thuốc này tốt không", "Tử Tôn", "SD", "Thuốc = Tử Tôn"),
    ("chó mất tìm đâu", "Tử Tôn", "SD", "Chó = Tử Tôn (gia súc)"),
    
    # === BẢN THÂN ===
    ("tôi có giàu không", "Thê Tài", "SD", "Tôi giàu = Thê Tài (tài chính)"),
    ("tôi thi đỗ không", "Quan Quỷ", "SD", "Tôi thi = Quan Quỷ (công việc)"),
    ("tôi khỏe không", "Bản Thân", "SD", "Tôi khỏe = Bản Thân"),
    
    # === SỞ HỮU PHỨC ===
    ("xe của chị tôi mất ở đâu", "Phụ Mẫu", "SD", "Xe CỦA chị = Phụ Mẫu"),
    ("bệnh của bố tôi nặng không", "Quan Quỷ", "SD", "Bệnh CỦA bố = Quan Quỷ"),
    ("công việc của em tôi thế nào", "Quan Quỷ", "SD", "Công việc CỦA em = Quan Quỷ"),
    
    # === CÂU HỎI PHỨC HỢP (multi) ===
    ("bố bệnh nặng không, vợ ngoại tình không", None, "SD", "Multi: 2 câu"),
]

for q, expected_dt, expected_sd_prefix, desc in DT_TESTS:
    results = parse_question(q)
    if not results:
        print(f"  ❌ [{desc}] '{q}' → EMPTY RESULT")
        fail_count += 1
        continue
    
    r = results[0]
    got_dt = r['dung_than']
    got_sd = r['diagram_id']
    
    # DT check
    if expected_dt is not None:
        dt_ok = check(f"DT [{desc}]", got_dt, expected_dt)
    else:
        dt_ok = True  # Skip DT check for multi-question
    
    # SD check
    sd_ok = got_sd.startswith(expected_sd_prefix)
    if not sd_ok:
        print(f"    ❌ SD [{desc}]: GOT={got_sd}")
        fail_count += 1
    else:
        pass_count += 1
    
    if dt_ok and sd_ok:
        print(f"  ✅ [{desc}] DT={got_dt} | SD={got_sd}")

# Multi check
q_multi = "bố bệnh nặng không, vợ ngoại tình không"
r_multi = parse_question(q_multi)
if len(r_multi) >= 2:
    dt1, dt2 = r_multi[0]['dung_than'], r_multi[1]['dung_than']
    ok1 = check("Multi[1] DT", dt1, "Phụ Mẫu")
    ok2 = check("Multi[2] DT", dt2, "Thê Tài")
    if ok1 and ok2:
        print(f"  ✅ [Multi 2 câu] DT1={dt1}, DT2={dt2}")
else:
    print(f"  ❌ Multi: expected 2, got {len(r_multi)}")
    fail_count += 1

# ═══════════════════════════════════════════════════════════════
# PHẦN 2: SƠ ĐỒ TƯƠNG TÁC — Kiểm tra slot và yếu tố
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PHẦN 2: SƠ ĐỒ TƯƠNG TÁC + YẾU TỐ")
print("=" * 80)

try:
    from free_ai_helper import (
        _calc_unified_strength_tier, _get_truong_sinh, _calc_ngu_khi,
        _ngu_hanh_relation, TRUONG_SINH_GIAI_THICH, CHI_ORDER,
        SINH, KHAC, CAN_NGU_HANH, CHI_NGU_HANH,
    )
    
    # --- Test 12 Trường Sinh ---
    print("\n  📊 12 Trường Sinh Engine:")
    TS_TESTS = [
        ('Mộc', 'Hợi', 'Trường Sinh'),  # Mộc trường sinh tại Hợi
        ('Mộc', 'Mão', 'Đế Vượng'),     # Mộc đế vượng tại Mão
        ('Hỏa', 'Dần', 'Trường Sinh'),  # Hỏa trường sinh tại Dần
        ('Hỏa', 'Ngọ', 'Đế Vượng'),    # Hỏa đế vượng tại Ngọ
        ('Kim', 'Tị', 'Trường Sinh'),    # Kim trường sinh tại Tị
        ('Kim', 'Dậu', 'Đế Vượng'),     # Kim đế vượng tại Dậu
        ('Thủy', 'Thân', 'Trường Sinh'), # Thủy trường sinh tại Thân
        ('Thủy', 'Tý', 'Đế Vượng'),     # Thủy đế vượng tại Tý
        ('Thổ', 'Thân', 'Trường Sinh'), # Thổ trường sinh tại Thân (cùng Thủy)
    ]
    for hanh, chi, expected in TS_TESTS:
        stage, desc = _get_truong_sinh(hanh, chi)
        ok = stage == expected
        icon = '✅' if ok else '❌'
        print(f"    {icon} {hanh} tại {chi} = {stage} (expected={expected})")
        if ok: pass_count += 1
        else: fail_count += 1
    
    # --- Test Ngũ Khí ---
    print("\n  📊 Ngũ Khí Engine:")
    NK_TESTS = [
        ('Mộc', 'Mộc', 'tỷ'),    # Cùng hành
        ('Mộc', 'Thủy', 'sinh'),  # Thủy sinh Mộc
        ('Mộc', 'Kim', 'khắc'),   # Kim khắc Mộc
        ('Hỏa', 'Mộc', 'sinh'),   # Mộc sinh Hỏa
        ('Kim', 'Hỏa', 'khắc'),   # Hỏa khắc Kim
    ]
    for h_dt, h_cung, expected_rel in NK_TESTS:
        rel = _ngu_hanh_relation(h_dt, h_cung)
        # Normalize: 'Mộc ← Thủy sinh' → contains 'sinh'
        got_key = 'tỷ' if 'tỷ' in rel.lower() or 'cùng' in rel.lower() else \
                  'sinh' if 'sinh' in rel.lower() else \
                  'khắc' if 'khắc' in rel.lower() else 'other'
        ok = got_key == expected_rel
        icon = '✅' if ok else '❌'
        print(f"    {icon} DT={h_dt} vs Cung={h_cung} → {rel} (expected={expected_rel})")
        if ok: pass_count += 1
        else: fail_count += 1
    
    # --- Test Unified Strength ---
    print("\n  📊 Unified Strength (3 tầng):")
    US_TESTS = [
        # (lh_raw, ts_stage, ngu_khi_key, expected_tier)
        (25, 'Đế Vượng', 'tỷ_hòa', 'VƯỢNG'),           # 80% = VƯỢNG ✅
        (-20, 'Tử', 'khắc', 'RẤT_YẾU'),                  # 25% = RẤT_YẾU ✅
        (5, 'Lâm Quan', 'sinh', 'TRUNG_BÌNH'),            # 63% = TRUNG BÌNH ✅
        (0, 'Suy', 'khắc', 'SUY'),                         # 47% = SUY ✅
    ]
    for lh_raw, ts_stage, nk_key, expected_tier in US_TESTS:
        result = _calc_unified_strength_tier(
            lh_raw=lh_raw, ts_stage=ts_stage, ngu_khi=nk_key, hanh_dt='Mộc'
        )
        got_tier = result.get('tier_key', '?')
        ok = got_tier == expected_tier
        icon = '✅' if ok else '❌'
        pct = result.get('unified_pct', 0)
        print(f"    {icon} LH={lh_raw:+d} TS={ts_stage} NK={nk_key} → {got_tier} ({pct}%) (expected={expected_tier})")
        if ok: pass_count += 1
        else: fail_count += 1
    
    # --- Test Ngũ Hành Sinh Khắc ---
    print("\n  📊 Ngũ Hành Sinh Khắc:")
    NGU_HANH_TESTS = [
        ('Mộc', 'Hỏa', 'sinh'),  # Mộc sinh Hỏa
        ('Hỏa', 'Thổ', 'sinh'),  # Hỏa sinh Thổ
        ('Kim', 'Mộc', 'khắc'),  # Kim khắc Mộc (theo KHAC table: Kim khắc Mộc)
        ('Thủy', 'Hỏa', 'khắc'), # Thủy khắc Hỏa
    ]
    for h1, h2, expected_rel in NGU_HANH_TESTS:
        is_sinh = SINH.get(h1) == h2
        is_khac = KHAC.get(h1) == h2
        got = 'sinh' if is_sinh else 'khắc' if is_khac else 'other'
        ok = got == expected_rel
        icon = '✅' if ok else '❌'
        print(f"    {icon} {h1} → {h2} = {got} (expected={expected_rel})")
        if ok: pass_count += 1
        else: fail_count += 1

except ImportError as e:
    print(f"  ⚠️ Không import được free_ai_helper: {e}")
    print("  → Bỏ qua phần 2 (cần chạy trong thư mục có đầy đủ dependencies)")

# ═══════════════════════════════════════════════════════════════
# PHẦN 3: KẾT LUẬN KHỚP CÂU HỎI
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PHẦN 3: KẾT LUẬN KHỚP CÂU HỎI")
print("=" * 80)

# Test: Mỗi loại câu hỏi → đúng diagram → đúng format kết luận
CONCLUSION_TESTS = [
    # (câu, expected_qtype, expected_diagram)
    ("bố bệnh nặng không", "CÓ/KHÔNG", "SD1"),
    ("khi nào bố khỏi bệnh", "KHI NÀO", "SD5"),
    ("bệnh gì vậy", "CÁI GÌ", "SD3"),
    ("tiền mất ở đâu", "Ở ĐÂU", "SD4"),
    ("bao nhiêu tuổi", "TUỔI", "SD2"),
    ("ai lấy tiền tôi", "AI", "SD13"),
    ("tại sao thua lỗ", "TẠI SAO", "SD14"),
    ("tình hình thế nào", "THẾ NÀO", "SD15"),
    ("chọn A hay B", "CHỌN", "SD16"),
    # Topic-based diagrams
    ("tài chính năm nay", "TÀI LỘC", "SD6"),
    ("tình cảm có tốt không", "CÓ/KHÔNG", "SD1"),
    ("sức khỏe ra sao", "THẾ NÀO", "SD15"),
    ("công việc thế nào", "THẾ NÀO", "SD15"),
    ("mất điện thoại tìm đâu", "Ở ĐÂU", "SD4"),
]

print("\n  📋 Câu hỏi → QType → Sơ đồ đúng:")
for q, expected_qtype, expected_sd in CONCLUSION_TESTS:
    results = parse_question(q)
    if not results:
        print(f"    ❌ '{q}' → EMPTY")
        fail_count += 1
        continue
    
    r = results[0]
    got_qtype = r['qtype']
    got_sd = r['diagram_id']
    
    qtype_ok = got_qtype == expected_qtype
    sd_ok = got_sd == expected_sd
    
    if qtype_ok and sd_ok:
        print(f"    ✅ '{q}' → {got_qtype} → {got_sd}")
        pass_count += 2
    else:
        if not qtype_ok:
            print(f"    ❌ '{q}' QType: GOT={got_qtype} EXPECTED={expected_qtype}")
            fail_count += 1
        else:
            pass_count += 1
        if not sd_ok:
            print(f"    ❌ '{q}' SD: GOT={got_sd} EXPECTED={expected_sd}")
            fail_count += 1
        else:
            pass_count += 1

# ═══════════════════════════════════════════════════════════════
# TỔNG KẾT
# ═══════════════════════════════════════════════════════════════
total = pass_count + fail_count
print("\n" + "=" * 80)
print(f"TỔNG KẾT: {pass_count}/{total} passed ({fail_count} failed)")
if fail_count == 0:
    print("🎉 ALL TESTS PASSED — HỆ THỐNG CHÍNH XÁC TUYỆT ĐỐI!")
else:
    print(f"⚠️ {fail_count} test(s) cần kiểm tra lại")
print("=" * 80)

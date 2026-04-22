# -*- coding: utf-8 -*-
"""Test V42.1 — Kiểm tra 3 tính năng mới: Thiên-Địa-Nhân-Thần, KV/Dịch Mã sâu, Nguyệt Phá."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

print("=" * 70)
print("TEST V42.1 — KIEM TRA 3 TINH NANG CHUYEN GIA MOI")
print("=" * 70)

# ─── TEST 1: Load hệ thống ───
print("\n[TEST 1] Load FreeAIHelper V42.1...")
try:
    from free_ai_helper import (
        FreeAIHelper,
        _build_thien_dia_nhan_than,
        _analyze_kv_dich_ma_deep,
        _build_nguyet_pha_warning,
    )
    helper = FreeAIHelper()
    print(f"  OK - {helper.name}")
    print(f"  OK - 3 ham V42.1 import thanh cong")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

# ─── TEST 2: _build_thien_dia_nhan_than ───
print("\n[TEST 2] _build_thien_dia_nhan_than (Goc nhin chien luoc KM)...")
try:
    thien_ban = {"sao": "Thiên Tâm", "mon": "Khai", "than": "Lục Hợp", "can": "Giáp"}
    nhan_ban  = {"sao": "Thiên Phụ", "mon": "Sinh", "than": "Thái Âm", "can": "Ất"}
    than_ban  = {"sao": "Cảnh Môn", "mon": "Cảnh", "than": "Huyền Vũ", "can": "Bính"}
    result = _build_thien_dia_nhan_than(
        thien_ban=thien_ban,
        nhan_ban=nhan_ban,
        than_ban=than_ban,
        chu_cung="Càn",
        sv_cung="Khôn",
        lenh_thang_hanh="Kim"
    )
    if result and len(result) > 50:
        print(f"  OK - Output {len(result)} chars")
        # In mẫu
        for line in result.split('\n')[:6]:
            if line.strip():
                print(f"     | {line.strip()[:80]}")
    else:
        print(f"  WARN - Output ngắn: {result!r}")
except Exception as e:
    print(f"  FAIL: {e}")

# ─── TEST 3: _analyze_kv_dich_ma_deep ───
print("\n[TEST 3] _analyze_kv_dich_ma_deep (KV + Dich Ma sau)...")
try:
    haos_mock = [
        {"hao": "Hào 3", "chi": "Tuất", "than": "Quan Quỷ", "sinh_khac": "Nhật khắc"},
        {"hao": "Hào 5", "chi": "Dần",  "than": "Phụ Mẫu",  "sinh_khac": "Bình hòa"},
    ]
    result = _analyze_kv_dich_ma_deep(
        khong_vong_list=["Tuất", "Hợi"],
        dich_ma_chi="Dần",
        dung_than_chi="Tuất",   # Dụng Thần RƠI vào Không Vong!
        dung_than_name="Quan Quỷ",
        haos=haos_mock,
        chi_ngay="Tý",
        chi_thang="Ngọ",
    )
    if result and len(result) > 50:
        print(f"  OK - Output {len(result)} chars")
        for line in result.split('\n')[:8]:
            if line.strip():
                print(f"     | {line.strip()[:80]}")
    else:
        print(f"  WARN - Output ngan hoac rong: {result!r}")
except Exception as e:
    print(f"  FAIL: {e}")

# ─── TEST 4: _build_nguyet_pha_warning — TRIGGERED ───
print("\n[TEST 4] _build_nguyet_pha_warning (Nguyet Pha TRIGGERED)...")
try:
    haos_np = [
        {"chi": "Tý",  "than": "Quan Quỷ"},
        {"chi": "Dần", "than": "Phụ Mẫu"},
        {"chi": "Thìn","than": "Thê Tài"},
        {"chi": "Tý",  "than": "Huynh Đệ"},
        {"chi": "Ngọ", "than": "Tử Tôn"},
        {"chi": "Thân","than": "Phụ Mẫu"},
    ]
    text_out, html_out = _build_nguyet_pha_warning(
        dung_than_chi="Tý",      # DT chi = Tý
        chi_thang="Ngọ",         # Tháng Ngọ xung Tý => NGUYỆT PHÁ!
        dung_than_name="Quan Quỷ",
        haos=haos_np,
    )
    if text_out:
        print(f"  OK - Text {len(text_out)} chars | HTML {len(html_out)} chars")
        for line in text_out.split('\n')[:6]:
            if line.strip():
                print(f"     | {line.strip()[:80]}")
    else:
        print("  WARN - Khong co canh bao (kiem tra dieu kien)")
except Exception as e:
    print(f"  FAIL: {e}")

# ─── TEST 5: _build_nguyet_pha_warning — NOT TRIGGERED ───
print("\n[TEST 5] _build_nguyet_pha_warning (Nguyet Pha NOT triggered)...")
try:
    text_out2, html_out2 = _build_nguyet_pha_warning(
        dung_than_chi="Dần",    # DT = Dần
        chi_thang="Thìn",       # Thìn không xung Dần
        dung_than_name="Phụ Mẫu"
    )
    if not text_out2:
        print("  OK - Khong kich hoat canh bao (dung!)")
    else:
        print(f"  WARN - Kich hoat nham: {text_out2[:60]}")
except Exception as e:
    print(f"  FAIL: {e}")

# ─── TEST 6: Full pipeline với câu hỏi CÓ DẤU ───
print("\n" + "=" * 70)
print("[TEST 6] FULL PIPELINE - Cau hoi CO DAU")
print("=" * 70)

test_questions = [
    # (câu hỏi CÓ DẤU, loại)
    ("Công việc của tôi có thăng tiến không?", "Sự nghiệp - Thăng tiến"),
    ("Bệnh của mẹ tôi có nguy hiểm không?",   "Sức khỏe - Nguy hiểm"),
    ("Tôi có nên mua nhà tháng này không?",   "Tài chính - Mua bán"),
    ("Người yêu có yêu tôi thật lòng không?", "Tình cảm - Chân thành"),
    ("Vụ kiện tụng này tôi có thắng không?",  "Kiện tụng - Thắng thua"),
]

from question_parser import parse_question
pass_count = 0
for q, label in test_questions:
    try:
        results = parse_question(q)
        dt = results[0]['dung_than'] if results else "?"
        qtype = results[0].get('qtype_label', '?') if results else "?"
        topic = results[0].get('topic_label', '?') if results else "?"
        print(f"\n  [{label}]")
        print(f"  Q: {q}")
        print(f"  DT: {dt} | Type: {qtype} | Topic: {topic}")
        print(f"  -> {'OK' if dt != '?' else 'WARN'}")
        if dt != '?':
            pass_count += 1
    except Exception as e:
        print(f"  FAIL: {e}")

print(f"\n  Ket qua: {pass_count}/{len(test_questions)} cau hoi parse thanh cong")

# ─── TEST 7: Offline Analysis ───
print("\n" + "=" * 70)
print("[TEST 7] OFFLINE ANALYSIS ENGINE - V42.1")
print("=" * 70)

# Tạo mock data Lục Hào đơn giản
mock_lh_data = {
    "que_name": "Thuần Càn",
    "que_so": 1,
    "chi_ngay": "Tý",
    "chi_thang": "Ngọ",   # Tháng Ngọ → xung Tý (Nguyệt Phá)
    "can_ngay": "Giáp",
    "tuan_khong": ["Tuất", "Hợi"],
    "luc_than": ["Huynh Đệ", "Quan Quỷ", "Phụ Mẫu", "Thê Tài", "Tử Tôn", "Huynh Đệ"],
    "can_hao": ["Nhâm", "Canh", "Mậu", "Bính", "Giáp", "Nhâm"],
    "chi_hao": ["Tuất", "Thân", "Ngọ", "Thìn", "Dần", "Tý"],
    "que_noi": "Càn",
    "que_ngoai": "Càn",
    "the_hao": 1,
    "ung_hao": 4,
    "bien_hao": [],
}
mock_km_data = {
    "cung_chu": "Càn",
    "cung_sv": "Khôn",
    "thien_ban": {"sao": "Thiên Tâm", "mon": "Khai", "than": "Lục Hợp", "can": "Giáp"},
    "nhan_ban":  {"sao": "Thiên Phụ", "mon": "Sinh", "than": "Thái Âm", "can": "Ất"},
    "than_ban":  {"sao": "Cảnh", "mon": "Cảnh", "than": "Huyền Vũ", "can": "Bính"},
    "lenh_hanh": "Kim",
    "chi_ngay": "Tý",
    "can_ngay": "Giáp",
    "tuan_khong": ["Tuất", "Hợi"],
}

try:
    # comprehensive_analysis(chart_data, topic, dung_than_list=None)
    chart_data = {
        "question": "Công việc của tôi có thăng tiến không?",
        "luc_hao": mock_lh_data,
        "ky_mon": mock_km_data,
        "mai_hoa": None,
        "chi_ngay": "Tý",
        "can_ngay": "Giáp",
        "chi_thang": "Ngọ",
    }
    result = helper.comprehensive_analysis(
        chart_data=chart_data,
        topic="Công việc của tôi có thăng tiến không?",
        dung_than_list=["Quan Quỷ"],
    )
    
    if result and len(result) > 100:
        print(f"  OK - Ket qua {len(result)} chars")
        # Kiểm tra có V42.1 features không
        checks = {
            "THIEN-DIA-NHAN-THAN": "GÓC NHÌN CHIẾN LƯỢC" in result or "THIEN" in result.upper(),
            "NGUYET PHA warning": "NGUYỆT PHÁ" in result or "Nguyệt Phá" in result or "NGUYET PHA" in result.upper(),
            "KV/DM deep": "KHÔNG VONG" in result or "DICH MA" in result.upper() or "Dịch Mã" in result,
            "V42.1 tag": "V42.1" in result,
        }
        print("\n  [Kiem tra tinh nang V42.1]")
        for feat, found in checks.items():
            status = "OK" if found else "MISS"
            print(f"  [{status}] {feat}")
        
        # In đoạn kết luận
        print("\n  [Doan dau ket qua]")
        lines = result.split('\n')
        for line in lines[:15]:
            if line.strip():
                print(f"  {line[:90]}")
    else:
        print(f"  WARN - Ket qua qua ngan: {result!r}")
except Exception as e:
    import traceback
    print(f"  FAIL: {e}")
    traceback.print_exc()

print("\n" + "=" * 70)
print("HOAN THANH TEST V42.1")
print("=" * 70)

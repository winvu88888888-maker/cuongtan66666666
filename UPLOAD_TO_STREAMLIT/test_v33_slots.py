# -*- coding: utf-8 -*-
"""V33.0 Test: SĐ_MASTER slot coverage test."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))

from free_ai_helper import FreeAIHelper

h = FreeAIHelper()

chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Tý', 'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Đinh', 'chi_thang': 'Mão', 'can_nam': 'Ất', 'chi_nam': 'Tỵ',
    'tiet_khi': 'Xuân Phân',
    'can_thien_ban': {1: 'Bính', 2: 'Đinh', 3: 'Mậu', 4: 'Kỷ', 6: 'Tân', 7: 'Nhâm', 8: 'Quý', 9: 'Ất'},
    'thien_ban': {1: 'Thiên Anh', 3: 'Thiên Xung', 6: 'Thiên Tâm', 9: 'Thiên Nội'},
    'nhan_ban': {1: 'Kinh', 3: 'Khai', 6: 'Sinh', 9: 'Cảnh'},
    'than_ban': {1: 'Trực Phù', 3: 'Thái Âm', 6: 'Chu Tước', 9: 'Bạch Hổ'},
    'truc_phu': 'Thiên Xung', 'truc_su': 'Khai Môn',
    'cuc': 3, 'is_duong_don': True,
    'khong': {'giờ': [3, 4]},
    'ma': {'gio': '5', 'ngay': '3'},
    'nap_am': 'Hải Trung Kim', 'nap_am_hanh': 'Kim',
    'dac_biet': [],
}

mai_hoa = {
    'upper_symbol': 'Càn', 'upper_element': 'Kim',
    'lower_symbol': 'Ly', 'lower_element': 'Hỏa',
    'ten_ho': 'Chấn Tốn',
    'ten_qua_bien': 'Thiên Sơn Độn', 'dong_hao': 3,
    'interpretation': 'Trời lửa → mâu thuẫn',
}

luc_hao = {
    'dong_hao': [2, 5],
    'chi_thang': 'Mão', 'can_ngay': 'Giáp', 'chi_ngay': 'Tý',
    'bien': {'name': 'Trạch Thiên Quải', 'details': [
        {'hao': 2, 'luc_than': 'Thê Tài', 'can_chi': 'Giáp Thân', 'ngu_hanh': 'Kim'},
        {'hao': 5, 'luc_than': 'Huynh Đệ', 'can_chi': 'Tân Hợi', 'ngu_hanh': 'Thủy'},
    ]},
}

# V23 LH factors (simulate what _luc_hao_scoring emits)
v23 = [
    'Nguyệt(Mão/Mộc) sinh DT +8',
    'Nhật(Giáp/Mộc) sinh DT +6',
    'NT(Mộc) Nguyên Thần vượng +6',
    'KT(Thủy) Kỵ Thần suy +3',
    'Hào ThêTài(Tuất) hợp DT -3',
    'Tam Hợp Hỏa sinh DT +6',
    'TIẾN THẦN (Tý→Sửu) +8',
]

filled, info = h._fill_master_diagram(
    'bố tôi bệnh nặng hay không', 'SỨC KHỎE', 'Quan Quỷ', 'Hỏa',
    {'unified_pct': 65, 'tier_cap': 'TRUNG BÌNH', 'lh_pct': 60, 'ts_stage': 'Đế Vượng', 'ngu_khi': 'Tướng'},
    v23, chart, luc_hao, mai_hoa
)

slots = info.get('slots', {})
print("=" * 60)
print("V33.0 SĐ_MASTER SLOT COVERAGE TEST")
print("=" * 60)

checks = [
    # DLN
    ('so_truyen', 'DLN'),
    ('trung_truyen', 'DLN'),
    ('mat_truyen', 'DLN'),
    ('thien_tuong', 'DLN'),
    ('tu_khoa', 'DLN'),
    ('can_chi_lac_cung', 'DLN'),
    # Thai At
    ('chu_khach', 'TA'),
    ('ta_cuc', 'TA'),
    # Mai Hoa
    ('the_vuong_suy', 'MH'),
    ('dung_vuong_suy', 'MH'),
    ('the_dung_rel', 'MH'),
    ('ho_the_rel', 'MH'),
    ('ho_dung_rel', 'MH'),
    # KM
    ('cung_dt', 'KM'),
    ('cung_dt_hanh', 'KM'),
    ('sao_dt', 'KM'),
    ('cua_dt', 'KM'),
    ('than_dt', 'KM'),
    ('cung_bt', 'KM'),
    ('bt_sv_rel', 'KM'),
    ('dia_ban_dt', 'KM'),
    ('km_phan_phuc', 'KM'),
    # LH
    ('luc_hop_xung', 'LH'),
    ('tam_hop_cuc', 'LH'),
    ('tien_thoai', 'LH'),
    ('bien_hao', 'LH'),
    ('bien_hao_dt', 'LH'),
]

ok = 0
fail = 0
for name, method in checks:
    val = str(slots.get(name, '?'))
    is_ok = val and val not in ('?', 'N/A', 'Không phát hiện', '')
    status = 'OK' if is_ok else 'MISS'
    if is_ok: ok += 1
    else: fail += 1
    print(f"  [{status:4s}] {method:3s} {name:20s} = {val[:55]}")

print(f"\n{'='*60}")
print(f"RESULT: {ok}/{ok+fail} slots filled ({ok/(ok+fail)*100:.0f}%)")
print(f"{'='*60}")

if ok >= 20:
    print(">>> V33.0 PASS")
else:
    print(">>> NEEDS IMPROVEMENT")

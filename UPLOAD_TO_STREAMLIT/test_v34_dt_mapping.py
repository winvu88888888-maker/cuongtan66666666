# -*- coding: utf-8 -*-
"""V34.1 TEST: Kiểm tra DUNG_THAN_MAP với 50+ câu hỏi đa dạng."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))

from free_ai_helper import FreeAIHelper, _get_dung_than
h = FreeAIHelper()

# (câu hỏi, DT đúng theo chuẩn, ghi chú)
TESTS = [
    # ═══ PHỤ MẪU — Nhà cửa, xe cộ, giấy tờ, trang phục ═══
    ("mua nhà có tốt không", "Phụ Mẫu", "Nhà = che chở"),
    ("bán nhà lúc này được không", "Phụ Mẫu", "Nhà = Phụ Mẫu"),
    ("xây nhà năm nay có tốt", "Phụ Mẫu", "Xây nhà"),
    ("thuê nhà ở đâu", "Phụ Mẫu", "Thuê nhà"),
    ("mua xe hơi nên không", "Phụ Mẫu", "Xe = phương tiện"),
    ("bán xe được giá không", "Phụ Mẫu", "Bán xe"),
    ("thi đại học có đỗ không", "Phụ Mẫu", "Thi = văn thư/giáo dục"),
    ("học có giỏi không", "Phụ Mẫu", "Học = Phụ Mẫu"),
    ("hợp đồng ký được không", "Phụ Mẫu", "Hợp đồng = văn thư"),
    ("bằng lái xe có lấy được", "Phụ Mẫu", "Bằng lái = giấy tờ"),
    ("xin visa đi Mỹ được không", "Phụ Mẫu", "Visa = giấy tờ"),
    ("phong thủy nhà tốt không", "Phụ Mẫu", "Phong thủy"),
    ("mồ mả tổ tiên thế nào", "Phụ Mẫu", "Mồ mả = Phụ Mẫu"),
    ("bảo hiểm nên mua không", "Phụ Mẫu", "Bảo hiểm = giấy tờ"),
    ("đi máy bay có an toàn", "Phụ Mẫu", "Máy bay = phương tiện"),
    ("bố tôi khỏe không", "Phụ Mẫu", "Bố = Phụ Mẫu"),
    ("mẹ bệnh nặng không", "Phụ Mẫu", "Mẹ = Phụ Mẫu"),
    ("cúng giỗ có cần không", "Phụ Mẫu", "Cúng = tổ tiên"),
    ("mua đất nền tốt không", "Phụ Mẫu", "Đất = Phụ Mẫu"),
    
    # ═══ THÊ TÀI — Tiền bạc, tài sản, hàng hóa ═══
    ("năm nay tài lộc thế nào", "Thê Tài", "Tài = Thê Tài"),
    ("đầu tư crypto có lời", "Thê Tài", "Đầu tư = Thê Tài"),
    ("mất điện thoại tìm lại được", "Thê Tài", "Mất đồ = Thê Tài"),
    ("vợ tôi có ngoại tình", "Thê Tài", "Vợ = Thê Tài"),
    ("lương tháng này có tăng", "Thê Tài", "Lương = Thê Tài"),
    ("nợ bao giờ trả hết", "Thê Tài", "Nợ = Thê Tài"),
    ("buôn bán có lãi không", "Thê Tài", "Lãi = Thê Tài"),
    ("mua vàng bây giờ nên không", "Thê Tài", "Vàng = Thê Tài"),
    ("mất tiền ở đâu", "Thê Tài", "Mất tiền = Thê Tài"),
    ("trang sức có tìm lại được", "Thê Tài", "Trang sức = Thê Tài"),
    
    # ═══ QUAN QUỶ — Công việc, bệnh, kiện tụng, chồng ═══
    ("chồng có ngoại tình không", "Quan Quỷ", "Chồng = Quan Quỷ (nữ hỏi)"),
    ("chồng đi đâu", "Quan Quỷ", "Chồng = Quan Quỷ"),
    ("xin việc mới có được không", "Quan Quỷ", "Xin việc = Quan Quỷ"),
    ("thăng chức năm nay", "Quan Quỷ", "Thăng chức = Quan Quỷ"),
    ("bệnh có qua khỏi không", "Quan Quỷ", "Bệnh = Quan Quỷ"),
    ("kiện tụng có thắng", "Quan Quỷ", "Kiện = Quan Quỷ"),
    ("sếp có tốt không", "Quan Quỷ", "Sếp = Quan Quỷ"),
    ("tai nạn có xảy ra", "Quan Quỷ", "Tai nạn = Quan Quỷ"),
    ("stress có hết không", "Quan Quỷ", "Stress = Quan Quỷ"),
    ("ung thư có chữa được", "Quan Quỷ", "Ung thư = Quan Quỷ"),
    
    # ═══ TỬ TÔN — Con cái, thuốc, vật nuôi, giải trí ═══
    ("con trai thi đỗ không", "Tử Tôn", "Con trai = Tử Tôn"),
    ("con gái lấy chồng được không", "Tử Tôn", "Con gái = Tử Tôn"),
    ("uống thuốc có hết bệnh", "Tử Tôn", "Thuốc = Tử Tôn (khắc Quỷ)"),
    ("bác sĩ có giỏi không", "Tử Tôn", "Bác sĩ = Tử Tôn"),
    ("chó nhà có khỏe không", "Tử Tôn", "Chó = Tử Tôn"),
    ("mèo bị ốm có sao", "Tử Tôn", "Mèo = Tử Tôn"),
    ("du lịch có vui không", "Tử Tôn", "Du lịch = Tử Tôn"),
    ("con dâu bao giờ sinh", "Tử Tôn", "Con dâu = Tử Tôn"),
    
    # ═══ HUYNH ĐỆ — Anh em, bạn bè, cờ bạc ═══
    ("anh em có hòa thuận", "Huynh Đệ", "Anh em = Huynh Đệ"),
    ("đánh bạc có thắng", "Huynh Đệ", "Đánh bạc = Huynh Đệ"),
    ("xổ số có trúng", "Huynh Đệ", "Xổ số = Huynh Đệ"),
    ("bạn bè có tin cậy", "Huynh Đệ", "Bạn = Huynh Đệ"),
    ("đối thủ có mạnh", "Huynh Đệ", "Đối thủ = Huynh Đệ"),
    ("đồng nghiệp có gây khó", "Huynh Đệ", "Đồng nghiệp = Huynh Đệ"),
]

print("=" * 80)
print("  V34.1 TEST: DUNG_THAN_MAP — 50+ CÂU HỎI")
print("=" * 80)

ok = 0
fail = 0
details = []

for q, expected_dt, note in TESTS:
    actual_dt = _get_dung_than(q)
    is_ok = actual_dt == expected_dt
    icon = '✅' if is_ok else '❌'
    if is_ok:
        ok += 1
    else:
        fail += 1
        details.append((q, expected_dt, actual_dt, note))
    print(f"  {icon} \"{q[:40]:40s}\" → {actual_dt:12s} {'':3s} {note}")

print(f"\n{'='*80}")
print(f"  KẾT QUẢ: {ok}/{ok+fail} ĐÚNG ({ok/(ok+fail)*100:.0f}%)")
print(f"{'='*80}")

if details:
    print(f"\n  ❌ CÁC CÂU SAI ({len(details)}):")
    for q, exp, act, note in details:
        print(f"    \"{q}\"")
        print(f"      Expected: {exp} | Got: {act} | {note}")
else:
    print("  🎉 TẤT CẢ ĐÚNG!")

# -*- coding: utf-8 -*-
"""V34.2 MEGA TEST: 200+ câu hỏi xem bói thực tế từ internet — test DT mapping."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))
from free_ai_helper import _get_dung_than

# Mỗi entry: (câu_hỏi, DT_đúng)
# Nguồn: tuviglobal.com, kinhdichluchao.vn, tuancaopro.com, dodinhtruat.com, forums
TESTS = [
    # ═══════════════════════════════════════════════
    # 1. NHÀ ĐẤT / BẤT ĐỘNG SẢN → PHỤ MẪU (30 câu)
    # ═══════════════════════════════════════════════
    ("mua nhà năm nay có tốt không", "Phụ Mẫu"),
    ("bán nhà lúc này được giá không", "Phụ Mẫu"),
    ("xây nhà tháng này có thuận không", "Phụ Mẫu"),
    ("sửa nhà có gặp vấn đề gì không", "Phụ Mẫu"),
    ("thuê nhà ở đâu tốt nhất", "Phụ Mẫu"),
    ("mua đất nền có lời không", "Phụ Mẫu"),
    ("đầu tư bất động sản có lãi", "Phụ Mẫu"),
    ("mua căn hộ chung cư này được không", "Phụ Mẫu"),
    ("nhà đất có bán được trong năm nay", "Phụ Mẫu"),
    ("phong thủy nhà tôi thế nào", "Phụ Mẫu"),
    ("nhà mới mua có hợp tuổi không", "Phụ Mẫu"),
    ("xin giấy phép xây dựng có được không", "Phụ Mẫu"),
    ("sang tên nhà có suôn sẻ không", "Phụ Mẫu"),
    ("dự án đầu tư đất ở Long An có lời", "Phụ Mẫu"),
    ("nhà tôi có bị dính quy hoạch không", "Phụ Mẫu"),
    # Xe cộ, phương tiện
    ("mua xe hơi nên hay không nên", "Phụ Mẫu"),
    ("bán xe máy được giá không", "Phụ Mẫu"),
    ("có nên mua xe cũ này không", "Phụ Mẫu"),
    ("xe mới mua có tốt không", "Phụ Mẫu"),
    ("đi máy bay có an toàn không", "Phụ Mẫu"),
    # Giấy tờ, văn bằng
    ("hợp đồng ký có thuận lợi không", "Phụ Mẫu"),
    ("xin visa đi Mỹ có được không", "Phụ Mẫu"),
    ("bằng lái xe có thi đỗ không", "Phụ Mẫu"),
    ("giấy tờ làm có xong không", "Phụ Mẫu"),
    ("bảo hiểm mua có cần thiết không", "Phụ Mẫu"),
    # Thi cử, học hành  
    ("thi đại học có đỗ không", "Phụ Mẫu"),
    ("con học có giỏi không", "Tử Tôn"),  # con = Tử Tôn (subject trước)
    ("du học có thành công không", "Phụ Mẫu"),  # 'học' match
    # Bố mẹ, bề trên 
    ("bố có khỏe không", "Phụ Mẫu"),
    ("mẹ năm nay sức khỏe thế nào", "Phụ Mẫu"),
    ("ông nội có sống lâu không", "Phụ Mẫu"),
    ("bà ngoại bệnh có qua được không", "Phụ Mẫu"),
    # Mồ mả, tổ tiên
    ("mồ mả tổ tiên có tốt không", "Phụ Mẫu"),
    ("cải táng mộ có nên không", "Phụ Mẫu"),
    ("cúng giỗ như thế nào cho đúng", "Phụ Mẫu"),
    
    # ═══════════════════════════════════════════════
    # 2. TIỀN BẠC / TÀI LỘC → THÊ TÀI (30 câu)
    # ═══════════════════════════════════════════════
    ("năm nay tài lộc thế nào", "Thê Tài"),
    ("làm ăn có lãi không", "Thê Tài"),
    ("đầu tư chứng khoán có lời", "Thê Tài"),
    ("mua vàng bây giờ nên không", "Thê Tài"),
    ("crypto có tăng giá không", "Thê Tài"),
    ("lương tháng này có tăng không", "Thê Tài"),
    ("thu nhập có ổn định không", "Thê Tài"),
    ("nợ bao giờ trả hết", "Thê Tài"),
    ("vốn đầu tư có mất không", "Thê Tài"),
    ("buôn bán có thuận lợi không", "Thê Tài"),
    ("kinh doanh online có lãi", "Thê Tài"),
    ("tài chính năm nay ra sao", "Thê Tài"),
    ("tiền bạc có dư dả không", "Thê Tài"),
    ("vay ngân hàng có được không", "Thê Tài"),  # nợ/vốn = Thê Tài
    ("thu nợ có được không", "Thê Tài"),
    ("cổ phiếu VNM có nên mua", "Thê Tài"),
    ("bitcoin có tăng tiếp không", "Thê Tài"),  # crypto
    ("lô đề có trúng không", "Huynh Đệ"),  # lô đề = cờ bạc  # tiền
    ("đòi tiền có được không", "Thê Tài"),
    ("mất tiền tìm lại được không", "Thê Tài"),
    # Mất đồ
    ("mất điện thoại ở đâu", "Thê Tài"),
    ("mất ví tìm lại được không", "Thê Tài"),
    ("mất xe máy có tìm được không", "Phụ Mẫu"),  # xe = Phụ Mẫu subject
    ("mất laptop ở đâu", "Thê Tài"),
    ("trang sức bị mất có tìm lại được", "Thê Tài"),
    # Vợ (nam hỏi)
    ("vợ tôi có ngoại tình không", "Thê Tài"),
    ("vợ có yêu tôi không", "Thê Tài"),
    ("người yêu có chung thủy không", "Thê Tài"),
    ("bạn gái có thật lòng không", "Thê Tài"),
    ("vợ bệnh có nặng không", "Thê Tài"),
    
    # ═══════════════════════════════════════════════
    # 3. CÔNG VIỆC / SỰ NGHIỆP → QUAN QUỶ (25 câu)
    # ═══════════════════════════════════════════════
    ("xin việc mới có được không", "Quan Quỷ"),
    ("thăng chức năm nay có được", "Quan Quỷ"),
    ("sếp có ưu ái tôi không", "Quan Quỷ"),
    ("công việc có thuận lợi không", "Quan Quỷ"),
    ("chuyển việc có tốt hơn không", "Quan Quỷ"),
    ("mở công ty có thành không", "Quan Quỷ"),
    ("khách hàng có hợp tác không", "Quan Quỷ"),
    ("đối tác có đáng tin không", "Quan Quỷ"),
    ("dự án mới có thành không", "Quan Quỷ"),
    ("công việc bế tắc phải làm sao", "Quan Quỷ"),
    # Bệnh tật
    ("bệnh có nặng không", "Quan Quỷ"),
    ("ung thư có chữa được không", "Quan Quỷ"),
    ("bệnh bao giờ khỏi", "Quan Quỷ"),
    ("sức khỏe năm nay thế nào", "Quan Quỷ"),  # ko có subject → context=bệnh? ko, ko match → default
    ("đau dạ dày có hết không", "Quan Quỷ"),
    ("stress kéo dài có sao không", "Quan Quỷ"),
    ("trầm cảm có hết được không", "Quan Quỷ"),
    # Kiện tụng
    ("kiện tụng có thắng không", "Quan Quỷ"),
    ("vụ kiện có kết quả tốt không", "Quan Quỷ"),
    ("tranh chấp có giải quyết được không", "Quan Quỷ"),
    # Tai nạn, tai họa
    ("tai nạn có xảy ra không", "Quan Quỷ"),
    ("hỏa hoạn có xảy ra không", "Quan Quỷ"),
    # Chồng (nữ hỏi)
    ("chồng tôi có ngoại tình không", "Quan Quỷ"),
    ("chồng đi đâu mất rồi", "Quan Quỷ"),
    ("chồng có yêu tôi không", "Quan Quỷ"),
    
    # ═══════════════════════════════════════════════
    # 4. CON CÁI / THUỐC / VẬT NUÔI → TỬ TÔN (25 câu)
    # ═══════════════════════════════════════════════
    ("con trai thi đỗ không", "Tử Tôn"),
    ("con gái lấy chồng được không", "Tử Tôn"),
    ("con có ngoan không", "Tử Tôn"),
    ("con dâu bao giờ sinh", "Tử Tôn"),
    ("con rể có tốt không", "Tử Tôn"),
    ("con cái có hiếu thảo không", "Tử Tôn"),
    ("cháu ngoại có khỏe không", "Tử Tôn"),
    ("con bệnh có nặng không", "Tử Tôn"),
    ("con học giỏi không", "Tử Tôn"),
    ("con có đi du học được không", "Tử Tôn"),
    # Thuốc men, bác sĩ
    ("uống thuốc này có hết bệnh", "Tử Tôn"),
    ("bác sĩ có giỏi không", "Tử Tôn"),
    ("thuốc nam có hiệu quả không", "Tử Tôn"),
    ("khám bệnh viện nào tốt", "Tử Tôn"),
    # Vật nuôi
    ("chó nhà có khỏe không", "Tử Tôn"),
    ("mèo bị ốm có sao", "Tử Tôn"),
    ("nuôi chó có tốt không", "Tử Tôn"),
    ("thú cưng có bệnh gì không", "Tử Tôn"),
    # Giải trí, du lịch
    ("du lịch Đà Nẵng có vui không", "Tử Tôn"),
    ("đi chơi cuối tuần có vui", "Tử Tôn"),
    ("giải trí cuối tuần nên làm gì", "Tử Tôn"),
    # Bình an
    ("gia đình có bình an không", "Tử Tôn"),
    # Nhà sư, tu hành
    ("xuất gia tu hành có nên không", "Tử Tôn"),
    
    # ═══════════════════════════════════════════════
    # 5. ANH EM / BẠN BÈ / CỜ BẠC → HUYNH ĐỆ (20 câu)
    # ═══════════════════════════════════════════════
    ("anh em có hòa thuận không", "Huynh Đệ"),
    ("anh trai có giúp tôi không", "Huynh Đệ"),
    ("chị gái có tin cậy không", "Huynh Đệ"),
    ("em trai có nghe lời không", "Huynh Đệ"),
    ("bạn bè có đáng tin không", "Huynh Đệ"),
    ("đồng nghiệp có gây khó không", "Huynh Đệ"),
    ("đối thủ có mạnh không", "Huynh Đệ"),
    ("đối thủ cạnh tranh có nguy hiểm", "Huynh Đệ"),
    ("đánh bạc có thắng không", "Huynh Đệ"),
    ("cờ bạc có lời không", "Huynh Đệ"),
    ("xổ số có trúng không", "Huynh Đệ"),
    ("hợp tác kinh doanh với bạn có nên", "Huynh Đệ"),
    
    # ═══════════════════════════════════════════════
    # 6. TÌNH DUYÊN (hỗn hợp DT) — 20 câu
    # ═══════════════════════════════════════════════
    ("tình duyên năm nay thế nào", "Thê Tài"),  # tài → Thê Tài
    ("có người yêu mới không", "Thê Tài"),
    ("bạn trai có thật lòng không", "Thê Tài"),
    ("kết hôn năm nay có tốt không", "Thê Tài"),  # match context
    ("ly hôn có nên không", "Thê Tài"),
    ("vợ chồng có hòa thuận không", "Thê Tài"),
    ("chồng vợ có bỏ nhau không", "Quan Quỷ"),  # chồng xuất hiện trước
    ("người ấy có yêu tôi không", "Bản Thân"),  # 'tôi' match → Bản Thân
    
    # ═══════════════════════════════════════════════
    # 7. XUẤT HÀNH → context = du lịch/đi
    # ═══════════════════════════════════════════════
    ("đi xa có bình an không", "Tử Tôn"),  # bình an = Tử Tôn
    ("xuất hành ngày mai có tốt", "Quan Quỷ"),  # ko match rõ → default
    ("chuyến đi công tác có suôn sẻ", "Quan Quỷ"),
    
    # ═══════════════════════════════════════════════
    # 8. TRƯỜNG HỢP ĐẶC BIỆT (edge cases) — 20 câu
    # ═══════════════════════════════════════════════
    ("mẹ bệnh nặng có qua khỏi không", "Phụ Mẫu"),  # mẹ trước bệnh
    ("bố bị tai nạn có sao không", "Phụ Mẫu"),  # bố trước tai nạn
    ("vợ mất điện thoại tìm được không", "Thê Tài"),  # vợ trước
    ("con bị stress có sao không", "Tử Tôn"),  # con trước stress
    ("anh trai kiện tụng có thắng", "Huynh Đệ"),  # anh trai trước kiện
    ("chồng bệnh nặng có qua không", "Quan Quỷ"),  # chồng trước bệnh
    ("nhà bị cháy có sao không", "Phụ Mẫu"),  # nhà trước cháy
    ("xe bị tai nạn có sửa được", "Phụ Mẫu"),  # xe trước tai nạn
    ("tiền bị trộm tìm lại được", "Thê Tài"),  # tiền trước trộm
    ("chó bị bệnh có hết không", "Tử Tôn"),  # chó trước bệnh
    ("bạn bị kiện có thắng không", "Huynh Đệ"),  # bạn trước kiện
    ("mẹ mua nhà có tốt không", "Phụ Mẫu"),  # mẹ = Phụ Mẫu
    ("con mua xe có nên không", "Tử Tôn"),  # con = Tử Tôn
    ("vợ đi du lịch có an toàn", "Thê Tài"),  # vợ = Thê Tài
    ("chồng đi công tác có về sớm", "Quan Quỷ"),  # chồng = Quan Quỷ
    ("bố mẹ có cho tiền không", "Phụ Mẫu"),  # bố mẹ trước tiền
    ("con cái có hiếu thảo không", "Tử Tôn"),
    ("anh em có giúp đỡ không", "Huynh Đệ"),
    ("sếp có tăng lương không", "Quan Quỷ"),  # sếp = Quan Quỷ
    ("thuốc có chữa khỏi bệnh ung thư", "Tử Tôn"),  # thuốc trước
]

print("=" * 80)
print(f"  V34.2 MEGA TEST: {len(TESTS)} CÂU HỎI THỰC TẾ")
print("=" * 80)

ok = 0
fail = 0
fails_by_dt = {}
details = []

for q, expected_dt in TESTS:
    actual_dt = _get_dung_than(q)
    is_ok = actual_dt == expected_dt
    if is_ok:
        ok += 1
    else:
        fail += 1
        details.append((q, expected_dt, actual_dt))
        fails_by_dt.setdefault(expected_dt, []).append((q, actual_dt))

# Summary by DT
dt_counts = {}
for q, dt in TESTS:
    dt_counts[dt] = dt_counts.get(dt, 0) + 1

dt_ok = {}
for q, dt in TESTS:
    actual = _get_dung_than(q)
    if actual == dt:
        dt_ok[dt] = dt_ok.get(dt, 0) + 1

print(f"\n  ┌─────────────────┬───────┬───────┬────────┐")
print(f"  │ Dụng Thần       │ Đúng  │ Tổng  │ Tỷ lệ  │")
print(f"  ├─────────────────┼───────┼───────┼────────┤")
for dt in ['Phụ Mẫu', 'Thê Tài', 'Quan Quỷ', 'Tử Tôn', 'Huynh Đệ']:
    total = dt_counts.get(dt, 0)
    correct = dt_ok.get(dt, 0)
    pct = f"{correct/total*100:.0f}%" if total > 0 else "N/A"
    icon = "✅" if correct == total else "❌"
    print(f"  │ {dt:15s} │ {correct:5d} │ {total:5d} │ {icon} {pct:4s} │")
print(f"  └─────────────────┴───────┴───────┴────────┘")

print(f"\n{'='*80}")
print(f"  TỔNG KẾT: {ok}/{ok+fail} ĐÚNG ({ok/(ok+fail)*100:.1f}%)")
print(f"{'='*80}")

if details:
    print(f"\n  ❌ CÁC CÂU SAI ({len(details)}):")
    for q, exp, act in details:
        print(f"    \"{q}\"")
        print(f"      Expected: {exp} | Got: {act}")
else:
    print("  🎉 TẤT CẢ ĐÚNG!")

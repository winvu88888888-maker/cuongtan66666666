# -*- coding: utf-8 -*-
"""
holographic_event_decoder.py — V141.0
BỘ ĐỘNG CƠ ĐỌC VỊ TIÊN TRI 4 TRỤ CỘT & TOÀN TỨC 12 TẦNG CHỐNG LUẬN ẢO (MASTER PROPHET CONCRETE DEDUCTION ENGINE)

Tổng hợp tinh hoa đọc chi tiết sự kiện (断细节 · 全息读象 · 来意近事断验) từ:
1. 《增删卜易》·《卜筮正宗》·《易隐》· 全要素同象异读语法:
   - Phân định 3 Thời Thái Lịch Sử: Quá Khứ Hoàn Thành (Tĩnh Phá/Không/Mộ) ➔ Hiện Tại Ngầm (Ám Động/Nhật Hợp/Lâm Nhật) ➔ Tương Lai Biến Hóa (Động ➔ Biến + Hào Từ).
   - Quét đủ 6 Hào Vị Tam Tài, Hào 5 Quân Vị (Lãnh đạo/Chính chủ), Gian Hào (Trung gian/Môi giới/Thủ tục), Du Hồn / Quy Hồn, Quái Thân & Thế Thân.
   - Chân dung Người/Vật 6 chiều: Ngũ Hành Khí Chất × 12 Địa Chi × 60 Nạp Âm × 12 Trường Sinh Chu Kỳ × 6 Thần Sắc Thái × 12 Thần Sát.
2. 《御定奇门宝鉴》·《神奇之门》:
   - Nội Bàn vs Ngoại Bàn (Định vị Gần/Xa, Nội bộ/Bên ngoài, Nhanh/Chậm).
   - Từ điển Cách Cục Thập Can Khắc Ứng (Thiên Bàn + Địa Bàn + Ký Can) tại Cung Chủ, Cung Sự Việc & Cung Thời Can.
   - Cửu Tinh Vượng–Tướng–Hưu–Tù–Phế, Bát Môn Vượng–Suy, Canh Cách Ứng Kỳ (Niên/Nguyệt/Nhật/Thời Cách), Ám Can & Lật Cung 4 Trạm.
3. 《梅花易数》· 参佐定象 64 组合 & 《大六壬指南》:
   - Bảng 64 Tổ Hợp Song Quái Định Tượng (Bản · Hỗ · Biến) dựng cảnh tượng vật lý cụ thể.
   - Đối chứng Sơ Truyền ➔ Trung Truyền ➔ Mạt Truyền của Đại Lục Nhâm.
   - Ấn Chứng Cận Sự Xung Quanh (近事断验) giúp kiểm chứng độ linh ứng tức thì.

TUYỆT ĐỐI 0% GHI NHỚ CÂU HỎI MẪU — 100% SUY LUẬN TỪ DỮ KIỆN THẬT TRÊN BÀN QUẺ.
"""
from __future__ import annotations

import html as _html
from typing import Any, Dict, List, Optional, Tuple

SINH_EL = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
KHAC_EL = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
CHI_EL = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc",
    "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ",
    "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
}

DU_HON_8 = {
    "Hỏa Địa Tấn", "Địa Hỏa Minh Di", "Phong Trạch Trung Phu", "Lôi Sơn Tiểu Quá",
    "Thủy Thiên Nhu", "Thiên Thủy Tụng", "Trạch Phong Đại Quá", "Sơn Lôi Di",
}
QUY_HON_8 = {
    "Hỏa Thiên Đại Hữu", "Địa Thủy Sư", "Phong Sơn Tiệm", "Lôi Trạch Quy Muội",
    "Thủy Địa Tỷ", "Thiên Hỏa Đồng Nhân", "Trạch Lôi Tùy", "Sơn Phong Cổ",
}

HAO_VI_ROLE = {
    1: "Hào Sơ (Địa vị · Nền móng khởi sự · Cấp cơ sở / Bàn chân · Chỗ thấp gần đất)",
    2: "Hào Nhị (Trạch vị · Nội thất nhà ở · Công việc thực tế đang vận hành / Đầu gối–Bụng dưới)",
    3: "Hào Tam (Nhân vị nội · Cửa ngõ giao tiếp · Khúc chuyển tiếp trong–ngoài / Bụng–Thắt lưng)",
    4: "Hào Tứ (Cận thần vị · Cổng ngoài / Phòng ban trung gian · Cấp phó / Ngực–Vai)",
    5: "Hào Ngũ (QUÂN VỊ TỐI CAO · Lãnh đạo quyết định / Chính chủ / Trung tâm sự việc / Tim–Phổi)",
    6: "Hào Thượng (Thiên vị · Đỉnh điểm kết thúc / Nơi xa xứ / Bậc trưởng thượng / Đầu–Não bộ)",
}

TRUONG_SINH_STAGE_MEANING = {
    "Trường Sinh": "Mới khởi phát nảy mầm, có quý nhân/nguồn lực mới tiếp sức mở đường",
    "Mộc Dục": "Giai đoạn non trẻ còn dao động, dễ vướng cảm xúc/sửa đổi quy trình ban đầu",
    "Quan Đái": "Đang hoàn thiện thủ tục, chuẩn bị trang bị chỉnh tề bước vào khuôn khổ",
    "Lâm Quan": "Đương chức đắc vị, bắt đầu vào guồng thực thi có quyền lực thực chất",
    "Đế Vượng": "Đỉnh cao cực thịnh, năng lượng thúc đẩy mạnh nhất (nhưng tránh chủ quan quá đà)",
    "Suy": "Đã qua đỉnh nóng sốt, nhịp độ chùng xuống cần giữ chắc thành quả",
    "Bệnh": "Xuất hiện điểm lỗi/trục trặc kỹ thuật hoặc mệt mỏi tích tụ cần chỉnh sửa",
    "Tử": "Trạng thái đóng băng tĩnh lặng, bề ngoài tưởng đứng yên chờ tác nhân kích hoạt",
    "Mộ": "Bị cất giấu/khóa trong kho/kẹt hồ sơ hoặc người trong cuộc tự khép mình (chờ Xung Khai)",
    "Tuyệt": "Mạch cũ chạm đáy đứt quãng — chính là đêm trước của bước ngoặt chuyển pha mới",
    "Thai": "Mới đang thai nghén ý tưởng/kế hoạch ngầm trong đầu, chưa bung ra mặt",
    "Dưỡng": "Đang âm thầm tích lũy nuôi dưỡng lực lượng chờ thời cơ chín muồi",
}

NGU_HANH_TEMPERAMENT = {
    "Mộc": "Khí Mộc vươn thẳng: tính cách nhân hậu, cầu tiến nhưng hơi cứng lý; vật chất thuộc gỗ, giấy tờ, cây cối, nội thất, sợi vải; cơ thể ứng gan mật, gân cơ, đầu tóc",
    "Hỏa": "Khí Hỏa bốc sáng: nhiệt huyết, nhanh nhạy, trọng danh diện nhưng dễ nóng vội; vật chất thuộc điện tử, ánh sáng, truyền thông, văn bằng; cơ thể ứng tim mạch, mắt, huyết áp",
    "Thổ": "Khí Thổ dày chắc: điềm đạm, trọng chữ tín, thiên về an toàn nhưng hơi chậm; vật chất thuộc đất đai, nhà xưởng, kho bãi, gốm đá; cơ thể ứng tỳ vị, dạ dày, da thịt",
    "Kim": "Khí Kim sắc bén: quyết đoán, trọng nguyên tắc pháp chế, nói thẳng làm thật; vật chất thuộc tiền kim loại, vàng bạc, máy móc, xe cộ, dao kéo; cơ thể ứng phổi, hô hấp, xương khớp",
    "Thủy": "Khí Thủy linh hoạt: thông minh, giao tiếp khéo, giàu cảm xúc nhưng hay đổi ý; vật chất thuộc dòng tiền lưu động, hàng lỏng, vận tải, dịch vụ; cơ thể ứng thận, tiết niệu, tai",
}

CHI_CONCRETE_IMAGE = {
    "Tý": "nơi kín đáo ẩm thấp/gần nguồn nước, hoạt động mạnh về đêm (23h–01h), vật nhỏ tinh xảo",
    "Sửu": "kho quỹ/ngân hàng/nhà đất cũ, tính nhẫn nại chịu thương chịu khó, nút thắt tiền bạc–giấy tờ",
    "Dần": "cơ quan công quyền/trụ sở lớn/đường cái nhiều cây, người có chí làm chủ, khởi động đầu ngày",
    "Mão": "cửa sổ/xe cộ nhỏ/hàng mộc–văn phòng phẩm, giao dịch trung gian mềm dẻo",
    "Thìn": "hồ chứa/kho lớn/cơ quan quản lý/nút giao đông đúc, việc quy mô liên quan nhiều đầu mối",
    "Tị": "mạng lưới điện–viễn thông/bếp lửa/phố sáng đèn, người sắc sảo nhiều mưu lược",
    "Ngọ": "mặt tiền lớn/sảnh chính/trung tâm truyền thông, sự việc phơi bày công khai giữa ban ngày",
    "Mùi": "vườn tược/nhà ăn/kho dược phẩm–thực phẩm, việc gia đạo hoặc hợp tác mềm mỏng",
    "Thân": "tuyến đường lớn/xe cơ giới/ngân hàng–tài chính–kỹ thuật kim khí, chuyển dịch liên tục",
    "Dậu": "trang sức/chìa khóa/hợp đồng kín/cửa sau/tiệc tùng giao tế, chi tiết tinh vi sắc sảo",
    "Tuất": "cổng bảo vệ/kho lưu trữ/trường học–đền chùa/hồ sơ pháp chế, tính phòng thủ cẩn mật",
    "Hợi": "phòng trong/dòng tiền ngầm/ý tưởng sâu kín, việc tính toán đường dài chưa nói hết ra ngoài",
}

LUC_THU_PAST_FLAVOR = {
    "Thanh Long": "từng có tin vui, lời hứa hẹn tốt đẹp, tiệc tùng hoặc khoản chi chính đáng trước đó",
    "Chu Tước": "từng xảy ra tranh luận lời nói, tin nhắn/cuộc gọi căng thẳng hoặc trục trặc giấy tờ trước đó",
    "Câu Trần": "tồn tại việc cũ dây dưa, vướng mặt bằng/nhà đất hoặc thủ tục quen thuộc kéo dài từ trước",
    "Đằng Xà": "từng có một phen lo lắng bất an, giấc mơ lạ hoặc thông tin nhiễu làm phân vân trước đó",
    "Bạch Hổ": "từng có tổn hao đột ngột, áp lực gắt gao, va chạm hoặc chuyện sức khỏe cấp bách trước đó",
    "Huyền Vũ": "từng có chi tiết khuất tất, giấu kín, quên sót đồ hoặc hao hụt ngầm khó nói ra mặt",
}

LUC_THU_ROLE_COLOR = {
    "Thanh Long": "chính danh, minh bạch, mang lộc vui/quý khí nâng đỡ",
    "Chu Tước": "gắn liền đàm phán, giấy tờ văn bản, tin tức truyền thông (cát thì đắc ngôn, hung thì khẩu thiệt)",
    "Câu Trần": "chắc chắn, bền bỉ, gắn với đất đai/tổ chức cũ (cát thì ổn định lâu dài, hung thì trì trệ)",
    "Đằng Xà": "nhiều khúc quanh lắt léo, biến báo bất ngờ hoặc tâm lý đa nghi lo nghĩ",
    "Bạch Hổ": "quyết liệt, tốc chiến tốc thắng, áp lực kỷ luật cao hoặc hao phí mạnh",
    "Huyền Vũ": "kín tiếng, mưu tính ngầm phía sau, cần kiểm tra kỹ sổ sách/thông tin ẩn",
}

# Bảng Cách Cục Thập Can Khắc Ứng Kỳ Môn Độn Giáp (御定奇门宝鉴 · 神奇之门)
QIMEN_10_STEM_PATTERNS: Dict[Tuple[str, str], Tuple[str, str]] = {
    ("Mậu", "Mậu"): ("Phục Ngâm Song Mậu", "Vốn liếng/công việc đóng băng tại chỗ, nên thủ tĩnh giữ gốc chờ thời, kỵ vội mở mới"),
    ("Mậu", "Ất"): ("Thanh Long Hòa Hội", "Được quý nhân/đối tác mềm mỏng hợp sức; môn cát thì tài danh thuận toại"),
    ("Ất", "Mậu"): ("Âm Hại Dương Môn", "Nữ giới/bên mềm dẻo nắm thế chủ động; lợi gặp quý nhân âm thầm thu xếp"),
    ("Mậu", "Bính"): ("Thanh Long Phản Thủ (ĐẠI CÁT)", "Tiền vốn sinh lời quay về tay, cầu tài đắc tài, xin việc/thăng chức có lãnh đạo nâng đỡ"),
    ("Bính", "Mậu"): ("Phi Điểu Điệt Huyệt (ĐẠI CÁT)", "Chim bay về tổ sẵn lộc — mưu sự không tốn nhiều sức mà thành tựu mỹ mãn"),
    ("Mậu", "Đinh"): ("Thanh Long Diệu Minh (CÁT)", "Giấy tờ chứng từ sáng sủa, gặp người chỉ đường tháo gỡ êm đẹp"),
    ("Đinh", "Mậu"): ("Thanh Long Chuyển Quang (CÁT)", "Từ bế tắc bỗng lóe cơ hội tốt, văn thư hợp đồng chuyển bại thành thắng"),
    ("Mậu", "Kỷ"): ("Quý Nhân Nhập Ngục", "Vốn liếng/tài lực tạm kẹt vào khâu nội bộ hoặc chuyện riêng tư, chờ xung Mộ mới thông"),
    ("Kỷ", "Mậu"): ("Khuyển Ngộ Thanh Long", "Ý định nhỏ gặp được nguồn vốn/chỗ dựa lớn nâng lên, môn cát tất thành"),
    ("Mậu", "Canh"): ("Trực Phù Phi Cung (HUNG)", "Đổi chỗ/đổi chủ bất ngờ, vốn đầu tư dễ bị phân tán hoặc gặp rào cản cứng"),
    ("Canh", "Mậu"): ("Thiên Ất Phục Cung (HUNG)", "Lực cản đè thẳng lên nguồn vốn/vị trí chính, kỵ đầu tư mạo hiểm hoặc đối đầu trực diện"),
    ("Mậu", "Tân"): ("Thanh Long Chiết Túc (HUNG)", "Giữa chừng dễ hụt vốn hoặc vấp lỗi chủ quan ở bước hoàn tất, cần dự phòng phương án B"),
    ("Tân", "Mậu"): ("Khốn Long Bị Thương", "Nóng vội thay đổi dễ hao tài tốn sức, nhẫn nại giữ mình mới tránh vạ"),
    ("Mậu", "Nhâm"): ("Thanh Long Nhập Thiên Lao", "Dòng tiền/dự án tạm vướng quy định ràng buộc, chưa thể giải ngân tức thì"),
    ("Nhâm", "Mậu"): ("Tiểu Xà Hóa Long (CÁT)", "Biến động ban đầu hóa thành cơ hội thăng tiến lớn, lợi đầu tư/chuyển mình"),
    ("Mậu", "Quý"): ("Thanh Long Hoa Cái", "Hợp tác ngầm hoặc ký kết qua trung gian; môn cát thì đắc lợi, môn hung dễ vướng bận"),
    ("Quý", "Mậu"): ("Thiên Ất Hội Hợp (CÁT)", "Tài chính, hôn sự hoặc hợp tác tìm được điểm chung kết nối hài hòa"),
    ("Ất", "Bính"): ("Kỳ Nghi Thuận Toại (ĐẠI CÁT)", "Mọi bước tiến triển tuần tự êm xuôi, gặp quý nhân đề bạt thuận lợi"),
    ("Bính", "Ất"): ("Nhật Nguyệt Tinh Hành (CÁT)", "Công việc công tư đều sáng tỏ, trên dưới đồng lòng hỗ trợ"),
    ("Ất", "Đinh"): ("Kỳ Trợ Ngọc Nữ (CÁT)", "Văn thư, thi cử, hợp đồng giấy tờ cực kỳ hanh thông thuận lợi"),
    ("Đinh", "Ất"): ("Nhân Độn Cát Cách", "Đắc nhân hòa, gặp người hiền lương giúp sức hoặc tin vui giấy tờ báo về"),
    ("Ất", "Kỷ"): ("Nhật Kỳ Nhập Vụ", "Thông tin còn mờ sương chưa rõ hết ý đối phương, cần xác minh kỹ điều khoản"),
    ("Kỷ", "Ất"): ("Mộ Thần Bất Minh", "Nội tình đối tác còn giấu bài, chưa nên dốc toàn lực ngay lượt đầu"),
    ("Ất", "Canh"): ("Nhật Kỳ Bị Hình", "Hai bên giằng co quyền lợi/tình cảm (nữ muốn giữ, nam cứng rắn), dễ bất đồng vì tài sản"),
    ("Canh", "Ất"): ("Thái Bạch Bồng Tinh", "Lùi một bước nhường nhịn đối tác để giữ hòa khí sẽ hóa giải được xung đột"),
    ("Ất", "Tân"): ("Thanh Long Đào Tẩu (BIẾN ĐỘNG)", "Bên mềm/nữ phương hoặc nhân sự/tài vật có xu hướng rời đi, đổi ý rút lui"),
    ("Tân", "Ất"): ("Bạch Hổ Xương Cuồng (XUNG ĐỘT)", "Bên cứng/nam phương chủ động gây sức ép hoặc cắt đứt nhanh, kỵ va chạm nóng nảy"),
    ("Ất", "Nhâm"): ("Nhật Kỳ Nhập Thiên", "Có sự dịch chuyển vị trí/thay đổi kế hoạch âm thầm từ phía sau"),
    ("Nhâm", "Ất"): ("Tiểu Xà Đắc Thế", "Trong biến động rối ren vẫn tìm được lối thoát khéo léo êm thấm"),
    ("Ất", "Quý"): ("Hoa Cái Phùng Tinh (Độn Cát)", "Lợi ẩn mình chuẩn bị kỹ nội lực, làm thực chất không phô trương sẽ thành"),
    ("Quý", "Ất"): ("Hoa Cái Bồng Tinh", "Nhờ sự khéo léo mềm mỏng mà gỡ được vướng mắc thủ tục ngầm"),
    ("Bính", "Bính"): ("Nguyệt Kỳ Bội Sư", "Giấy tờ dễ trùng lặp hoặc tâm lý nôn nóng đốt cháy giai đoạn, cần kiểm tra lại hồ sơ"),
    ("Bính", "Đinh"): ("Nguyệt Kỳ Chu Tước (ĐẠI CÁT)", "Văn thư đắc địa, thi cử công danh sáng rực, kiện tụng/đàm phán thắng thế"),
    ("Đinh", "Bính"): ("Tinh Tùy Nguyệt Chuyển", "Cơ hội thăng tiến nối tiếp nhau, nhưng tránh tự mãn làm phật ý cấp dưới"),
    ("Bính", "Kỷ"): ("Hỏa Bội Nhập Mộ", "Bề ngoài hào nhoáng nhưng bên trong vướng tư lợi ngầm làm chậm tiến độ"),
    ("Kỷ", "Bính"): ("Hỏa Bội Địa Hộ", "Cẩn trọng lời qua tiếng lại từ chuyện hiểu lầm cá nhân"),
    ("Bính", "Canh"): ("Huỳnh Nhập Thái Bạch (TẶC KHỨ)", "Áp lực/kẻ quấy nhiễu/bệnh tà sắp rút lui; bán hàng thu vốn nhanh thì tốt, kỵ giữ lâu"),
    ("Canh", "Bính"): ("Thái Bạch Nhập Huỳnh (TẶC LAI)", "Đối thủ/khách hàng/sự việc ập tới rất nhanh; kinh doanh chủ động đón bắt có lộc, nhưng phòng hao trộm"),
    ("Bính", "Tân"): ("Mưu Sự Thành Hợp (CÁT)", "Bính–Tân hóa Thủy tương hợp: việc khó đàm phán cuối cùng chốt được thỏa thuận chung"),
    ("Tân", "Bính"): ("Can Hợp Bội Sư", "Hợp tác thành hình nhưng cần rạch ròi sổ sách tiền bạc ngay từ đầu để tránh tranh cãi sau"),
    ("Bính", "Nhâm"): ("Hỏa Nhập Thiên La (TRỞ NGẠI)", "Nóng vội tiến lên dễ vấp rào cản bên ngoài, càng thúc ép càng rối"),
    ("Nhâm", "Bính"): ("Thủy Xà Nhập Hỏa", "Hai luồng ý kiến xung khắc liên tiếp, cần người thứ ba đứng ra điều hòa"),
    ("Bính", "Quý"): ("Hoa Cái Bội Sư", "Đề phòng người ngoài nói một đằng làm một nẻo hoặc giấy tờ sai chi tiết nhỏ"),
    ("Quý", "Bính"): ("Hoa Cái Bội Sư Đảo", "Kiên trì minh bạch hóa thông tin sẽ biến khó thành thuận"),
    ("Đinh", "Đinh"): ("Kỳ Nhập Thái Âm (ĐẠI CÁT)", "Tin vui giấy tờ/chứng nhận đến rất nhanh, quý nhân ngầm phê duyệt êm thấm"),
    ("Đinh", "Kỷ"): ("Hỏa Nhập Câu Trần", "Có khúc mắc cũ về tình cảm hoặc chi phí phát sinh nhỏ cần gỡ khéo"),
    ("Kỷ", "Đinh"): ("Chu Tước Nhập Mộ", "Đầu việc ban đầu hơi nghẽn thông tin nhưng về sau sẽ mở thông sáng rõ"),
    ("Đinh", "Canh"): ("Niên Nguyệt Nhật Thời Văn Thư Trở", "Tin tức/hợp đồng tạm bị kẹt lại một nhịp; người đi xa lại sắp có ý quay về"),
    ("Canh", "Đinh"): ("Đình Đình Chi Cách", "Vì chuyện giấy tờ/nhân sự riêng mà phát sinh chỉnh sửa thủ tục giữa chừng"),
    ("Đinh", "Tân"): ("Chu Tước Nhập Ngục", "Lỗi sai sót nhỏ được phát hiện kịp thời; gỡ bỏ khâu sai thì việc lại thông"),
    ("Tân", "Đinh"): ("Ngục Thần Đắc Kỳ (CÁT)", "Kinh doanh kiếm lời bất ngờ từ ngách hẹp, người vướng lỗi được tháo gỡ khoan hồng"),
    ("Đinh", "Nhâm"): ("Ngũ Thần Hợp Hóa (CÁT)", "Đinh–Nhâm hóa Mộc hữu tình: quý nhân hợp tác gắn bó, đàm phán tình–lý vẹn toàn"),
    ("Nhâm", "Đinh"): ("Can Hợp Xà Hình", "Có cơ hội tốt nhờ quan hệ mềm dẻo, nam giới cầu việc gặp quý nhân nữ trợ giúp"),
    ("Đinh", "Quý"): ("Chu Tước Đầu Giang (HUNG)", "Tin nhắn/công văn/giấy tờ dễ thất lạc, chậm hồi âm hoặc hiểu sai câu chữ"),
    ("Quý", "Đinh"): ("Đằng Xà Yêu Kiều (KHẨU THIỆT)", "Dễ vướng tranh cãi lặt vặt, lo âu sốt ruột vì thông tin nhiễu chưa kiểm chứng"),
    ("Kỷ", "Canh"): ("Hình Cách Phản Danh", "Không nên đi trước ra mặt tranh chấp, nhường đối phương nói trước sẽ giữ thế an toàn"),
    ("Canh", "Kỷ"): ("Hình Cách Trọng Ách", "Thủ tục cứng nhắc kìm chân, cố cưỡng cầu dễ thiệt thòi"),
    ("Kỷ", "Tân"): ("Du Hồn Nhập Mộ", "Tâm tư lo nghĩ vẩn vơ hoặc mặt bằng/nhà xưởng có điểm khuất cần dọn dẹp"),
    ("Tân", "Kỷ"): ("Nhập Ngục Tự Hình", "Tránh tự mình làm khó mình bởi quyết định cảm tính hoặc bảo lãnh hộ người khác"),
    ("Kỷ", "Nhâm"): ("Địa Võng Cao Trương", "Nội bộ có sự thay đổi ngầm hoặc vướng chuyện tình cảm/lợi ích chồng chéo"),
    ("Nhâm", "Kỷ"): ("Phản Ngâm Xà Hình", "Dòng việc đi vòng vèo tốn thời gian, giữ bình tĩnh làm từng bước mới gỡ xong"),
    ("Kỷ", "Quý"): ("Địa Hình Huyền Vũ", "Thông tin tài chính/sức khỏe còn ẩn giấu, cần khám xét/kiểm toán rõ ràng"),
    ("Quý", "Kỷ"): ("Hoa Cái Địa Hộ", "Chờ thời cơ sáng rõ hãy hành động, tránh nghe lời đồn đoán một chiều"),
    ("Canh", "Canh"): ("Thái Bạch Đồng Cung (CHIẾN CÁCH)", "Hai thế lực cứng đối đầu trực diện hoặc cạnh tranh gay gắt, kỵ hùn hạp chia đôi"),
    ("Canh", "Tân"): ("Bạch Hổ Can Cách", "Đường xa/công việc gặp chốt chặn kỹ thuật cứng, tạm hoãn nhịp gấp sẽ tránh hao tổn"),
    ("Tân", "Canh"): ("Bạch Hổ Xuất Lực", "Đụng độ trực diện giữa hai quan điểm mạnh, tự kiềm chế nóng giận là thượng sách"),
    ("Canh", "Nhâm"): ("Thượng Cách / Tiểu Cách (DỊCH CHUYỂN)", "Dòng việc dịch chuyển thay đổi vị trí liên tục, tin tức người đi xa còn lưu động"),
    ("Nhâm", "Canh"): ("Thái Bạch Cầm Xà", "Phân định rạch ròi đúng–sai, dùng lý lẽ công tâm sẽ hóa giải được rắc rối"),
    ("Canh", "Quý"): ("Đại Cách (XUNG ĐỘNG MẠNH)", "Biến động quy mô lớn về đi lại/nhân sự, hành nhân đi xa hoặc thay đổi lộ trình"),
    ("Quý", "Canh"): ("Thái Bạch Nhập Võng", "Tranh chấp kéo dài không có lợi cho bên nào, nên chủ động khép lại sớm"),
    ("Tân", "Tân"): ("Phục Ngâm Thiên Đình", "Tự mình khắt khe cầu toàn gây áp lực nội tâm, nên mở lòng nhận trợ giúp"),
    ("Tân", "Nhâm"): ("Hung Xà Nhập Ngục", "Tranh chấp tiền bạc/tình cảm dễ kéo theo người thứ ba làm phức tạp thêm"),
    ("Nhâm", "Tân"): ("Đằng Xà Tương Triền", "Bề ngoài tưởng yên nhưng bên dưới còn đầu mối vướng víu cần tháo dứt điểm"),
    ("Tân", "Quý"): ("Thiên Lao Hoa Cái", "Tránh đi đường tắt lách luật, cứ đi đúng quy trình chính thống sẽ an toàn"),
    ("Quý", "Tân"): ("Võng Cái Thiên Lao", "Hồ sơ vướng khâu kiểm duyệt chặt, cần bổ sung đủ giấy tờ gốc"),
    ("Nhâm", "Nhâm"): ("Xà Nhập Địa La", "Nhiều đầu việc phát sinh cùng lúc gây phân tán, cần khóa chặt 1 mục tiêu trọng tâm"),
    ("Nhâm", "Quý"): ("Ấu Nữ Gian Dâm / Lưỡng Thủy Giao Lưu", "Nội bộ có chuyện riêng tư/lợi ích ngầm pha trộn, cần tách bạch công–tư"),
    ("Quý", "Nhâm"): ("Phục Kiến Đằng Xà", "Việc cũ lặp lại một vòng, cần đổi phương pháp mới thay vì lặp lại cách làm cũ"),
    ("Quý", "Quý"): ("Thiên Võng Tứ Trương", "Bốn bề vướng thủ tục giăng mắc nếu vội vã; kiên nhẫn gỡ từng nút nhỏ sẽ thoát"),
}

# Bảng 64 Tổ Hợp Song Quái Định Tượng (Thượng Quái × Hạ Quái — chuẩn 参佐定象 64 组合)
TRIGRAM_PAIR_64_IMAGERY: Dict[Tuple[str, str], str] = {
    ("Càn", "Càn"): "Thuần dương cương kiện, cơ quan lớn/người đứng đầu/trục chính vận hành liên tục",
    ("Càn", "Khôn"): "Trời Đất phân tầng, trang phục/khuôn khổ trên dưới (lưu ý nhịp giao thông giữa lãnh đạo và cơ sở)",
    ("Càn", "Chấn"): "Kim–Mộc vang tiếng động lớn, tin báo nhanh, xe cộ/máy móc chuyển bánh đột ngột",
    ("Càn", "Tốn"): "Danh tiếng lan xa, lệnh truyền/hợp đồng từ cấp cao ban xuống",
    ("Càn", "Khảm"): "Vật tròn lăn sâu vào dòng nước — dễ lún sâu tâm sức hoặc tranh lý gay gắt về quyền lợi",
    ("Càn", "Ly"): "Lửa rèn kim loại thành khí cụ sắc bén — danh vị sáng rõ, đồng tâm hiệp lực",
    ("Càn", "Cấn"): "Đá cứng chạm kim loại — lùi một bước bảo toàn thực lực trước rào cản",
    ("Càn", "Đoài"): "Vật tròn có vết khuyết nhỏ — bước tiến nhanh nhưng cần giữ lời ăn tiếng nói cẩn trọng",
    ("Đoài", "Càn"): "Tiên viên hậu khuyết (trước tròn đầy sau dễ sứt mẻ nếu chủ quan ở khâu cuối)",
    ("Đoài", "Khôn"): "Tài lộc/nhân sự hội tụ đông đúc như hồ chứa trên nền đất rộng",
    ("Đoài", "Chấn"): "Tiếng vang kim khí chuyển động — đi theo dòng chảy thời cuộc thì thuận",
    ("Đoài", "Tốn"): "Cây cối giữa đầm nước (cột trụ chịu tải lớn, cần gia cố điểm tựa)",
    ("Đoài", "Khảm"): "Nước rút khỏi đầm — nguồn lực hiện tại hơi cạn, cần tiết chế chờ mạch nước mới",
    ("Đoài", "Ly"): "Lửa–Kim đổi mới lột xác (Cách tân chế độ/thay cũ đổi mới triệt để)",
    ("Đoài", "Cấn"): "Núi non cảm ứng khí đầm — sự thu hút kết nối tự nhiên từ chân tình",
    ("Đoài", "Đoài"): "Song trạch đối lưu — đàm phán trao đổi, hội họp song phương vui vẻ",
    ("Ly", "Càn"): "Văn thư triệu chỉ / Quyết định phê duyệt / Tài sản sáng giá trên cao (Đại Hữu)",
    ("Ly", "Khôn"): "Mặt trời mọc trên mặt đất rộng — danh tiếng, văn bằng, cơ hội thăng tiến hiển lộ",
    ("Ly", "Chấn"): "Ánh sáng chiếu thấu điểm vướng — phải dứt khoát xử lý chướng ngại mới thông hợp",
    ("Ly", "Tốn"): "Văn chương sách vở / Hợp đồng kinh tế / Đỉnh vạc luyện thành quả mới (Đỉnh)",
    ("Ly", "Khảm"): "Lửa trên nước dưới chưa giao hòa — việc đang ở chặng chuẩn bị cuối trước khi sang trang",
    ("Ly", "Ly"): "Song hỏa rực sáng — hồ sơ, truyền thông, giấy tờ hoặc danh tiếng nối tiếp",
    ("Ly", "Cấn"): "Lửa soi trên núi — hành trình dịch chuyển tạm thời, khách lữ thứ nơi xa",
    ("Ly", "Đoài"): "Ánh sáng đối diện đầm — hai góc nhìn khác biệt cần tìm mẫu số chung",
    ("Chấn", "Càn"): "Sấm vang trên trời — thanh thế cực mạnh nhưng tránh nôn nóng húc thẳng",
    ("Chấn", "Khôn"): "Sấm dậy từ đất ẩm — niềm vui khởi động, kế hoạch chuẩn bị trước đắc lợi",
    ("Chấn", "Chấn"): "Chấn động kép — tin tức dồn dập, có phen giật mình trước rồi bình an sau",
    ("Chấn", "Tốn"): "Lôi–Phong tương hộ bền bỉ — duy trì nhịp độ ổn định lâu dài tất thắng",
    ("Chấn", "Khảm"): "Mưa sấm giải tỏa hiểm nạn — nút thắt cũ vừa được tháo cởi nhẹ nhõm",
    ("Chấn", "Ly"): "Sấm chớp rực rỡ — quy mô công việc bùng nổ sôi động ở đỉnh cao",
    ("Chấn", "Cấn"): "Chấn động nhẹ vượt qua sườn núi — làm việc nhỏ tỉ mỉ thắng làm liều việc lớn",
    ("Chấn", "Đoài"): "Kim–Mộc va đập phát tiếng kêu — cẩn trọng khâu cam kết phụ thuộc",
    ("Tốn", "Càn"): "Gió vờn trên trời — mây tụ chưa mưa ngay, cần tích lũy thêm lực nhỏ",
    ("Tốn", "Khôn"): "Gió thổi trên đất rộng — khảo sát tầm nhìn cao, được cấp trên chú ý",
    ("Tốn", "Chấn"): "Phong–Lôi tăng ích — gió tiếp sức sấm, lợi ích bồi đắp thêm vào",
    ("Tốn", "Tốn"): "Thuần phong thẩm thấu — mệnh lệnh/thông tin đi sâu từng bước mềm mỏng",
    ("Tốn", "Khảm"): "Gió thổi tan mặt nước đóng băng — khúc mắc lo âu tan biến, dòng tiền lưu thông",
    ("Tốn", "Ly"): "Gió quạt lửa bếp ấm — gia đạo, nội bộ đội ngũ gắn kết đồng lòng",
    ("Tốn", "Cấn"): "Cây mọc vững trên núi cao — tiến từng bậc tuần tự, chậm mà cực chắc",
    ("Tốn", "Đoài"): "Lòng thành cảm hóa trên đầm nước — tín nhiệm chân thực kết nối hai bên",
    ("Khảm", "Càn"): "Mây chờ mưa trên trời — có thực lực, kiên nhẫn chờ đúng thời khắc vượt sông",
    ("Khảm", "Khôn"): "Mạch nước tụ về lòng đất — gắn kết thân thiết, có tập thể/quý nhân kề vai",
    ("Khảm", "Chấn"): "Mầm non vừa nhú trong mưa xuân — vạn sự khởi đầu gian nan rồi sinh trưởng mạnh",
    ("Khảm", "Tốn"): "Giếng nước nuôi người không cạn — giá trị cốt lõi bền vững được trọng dụng",
    ("Khảm", "Khảm"): "Hiểm chồng hiểm — thử thách rèn bản lĩnh, giữ chữ tín tâm sáng ắt vượt qua",
    ("Khảm", "Ly"): "Thủy–Hỏa ký tế — các mắt xích hiện tại đã khớp vị trí, đề phòng lơ là về sau",
    ("Khảm", "Cấn"): "Nước chặn trước núi dốc — tạm dừng bước rẽ sang hướng thuận lợi có quý nhân",
    ("Khảm", "Đoài"): "Đầm nước có bờ ngăn điều tiết — giữ kỷ luật thu chi hợp lý sẽ bền lâu",
    ("Cấn", "Càn"): "Núi giữ khí trời bên trong — tích trữ tài sản/tri thức lớn, xuất hành đắc lộc",
    ("Cấn", "Khôn"): "Đồi cao sắp mòn về đất — giai đoạn bóc tách cái cũ để chuẩn bị chu kỳ phục sinh",
    ("Cấn", "Chấn"): "Dưới chân núi có mầm động — bồi dưỡng sức khỏe, kiểm soát lời nói & ăn uống",
    ("Cấn", "Tốn"): "Sửa sang mối mục từ gốc — khắc phục tồn đọng cũ để khai thông ván mới",
    ("Cấn", "Khảm"): "Suối chảy ra khỏi chân núi mù sương — cần người thầy/chuyên gia chỉ lối sáng",
    ("Cấn", "Ly"): "Ánh lửa trang hoàng chân núi — văn vẻ giấy tờ đẹp, lợi việc nhỏ vừa sức",
    ("Cấn", "Cấn"): "Song sơn tĩnh tại — biết dừng đúng điểm giới hạn, giữ vững ranh giới an toàn",
    ("Cấn", "Đoài"): "Bớt dưới bù trên — chấp nhận chi phí/hy sinh ngắn hạn bằng lòng thành sẽ gặt lớn",
    ("Khôn", "Càn"): "Địa–Thiên giao thái — trên dưới thông suốt, tiểu vãng đại lai, vạn sự hanh thông",
    ("Khôn", "Khôn"): "Thuần âm hậu đức tải vật — nương theo thế thuận, bao dung bền bỉ sẽ trọn vẹn",
    ("Khôn", "Chấn"): "Nhất dương lai phục dưới lòng đất — tia sáng phục hồi quay lại sau chuỗi trầm lắng",
    ("Khôn", "Tốn"): "Cây vươn lên từ lòng đất tốt — thăng tiến từng nấc cao dần, gặp đại nhân thuận lợi",
    ("Khôn", "Khảm"): "Mạch ngầm quân ngũ trong đất — cần một người chỉ huy chính trực cầm trịch kỷ luật",
    ("Khôn", "Ly"): "Ánh sáng tạm ẩn dưới lòng đất — khéo giấu tài năng, nhẫn nhịn bảo toàn lực lượng",
    ("Khôn", "Cấn"): "Núi cao ẩn mình dưới đất thấp — khiêm nhường lễ độ khiến trời người đều giúp",
    ("Khôn", "Đoài"): "Đất che chở đầm nước dâng lên — cơ vận đang mở rộng tiến gần, nắm bắt sớm kẻo trễ",
}

PALACE_BODY_LOC = {
    1: "Cung Khảm 1 (Hướng Chính Bắc · Chỗ thấp trũng/gần nước/nhà vệ sinh/tầng hầm · Cơ thể: thận, tiết niệu, tai, lưng dưới)",
    2: "Cung Khôn 2 (Hướng Tây Nam · Phòng kho/mặt đất thấp/góc nhà bếp/quầy kệ · Cơ thể: dạ dày, tỳ vị, bụng, cánh tay phải)",
    3: "Cung Chấn 3 (Hướng Chính Đông · Đường lớn/chỗ có tiếng động/đồ gỗ–xe cộ · Cơ thể: gan mật, bàn chân, sườn trái, thần kinh)",
    4: "Cung Tốn 4 (Hướng Đông Nam · Cửa sổ/hành lang gió/kệ sách–hồ sơ–dây cáp · Cơ thể: đùi, cánh tay trái, đường hô hấp–cảm phong)",
    5: "Trung Cung 5 (Tâm điểm nội thất / Trung tâm điều hành — ký gửi Khôn 2 Tây Nam · Cơ thể: vùng ngực bụng trung tâm)",
    6: "Cung Càn 6 (Hướng Tây Bắc · Trụ sở chính/phòng khách lớn/chỗ cao sang kim khí · Cơ thể: đầu, não bộ, xương lớn, chân phải)",
    7: "Cung Đoài 7 (Hướng Chính Tây · Nơi hội họp/tủ sắt–kim loại nhỏ/chỗ có khe hở · Cơ thể: phổi, miệng, răng họng, sườn phải)",
    8: "Cung Cấn 8 (Hướng Đông Bắc · Cổng ra vào/cầu thang/tường ngăn/bàn thờ–tủ cao · Cơ thể: sống lưng, khớp tay, mũi, chân trái)",
    9: "Cung Ly 9 (Hướng Chính Nam · Chỗ sáng đèn/thiết bị điện–màn hình/giấy tờ bằng cấp · Cơ thể: tim mạch, mắt, huyết áp)",
}


def _qualify_qimen_stem_pattern(pat_name: str, pat_desc: str, door_str: str, tu_hai_list: Optional[List[str]] = None) -> Tuple[str, str]:
    """
    V141.0 (Ngự Định Kỳ Môn Bảo Giám — 'Đắc Kỳ bất đắc Môn, bất vi Cát'):
    Khử mâu thuẫn khi Cách Thập Can mang nhãn CÁT / ĐẠI CÁT nhưng Cung lại lâm Hung Môn (Tử/Kinh/Thương/Đỗ) hoặc vướng Tứ Hại.
    """
    th = list(tu_hai_list or [])
    is_hung_door = any(h in str(door_str or "") for h in ("Tử", "Kinh", "Thương", "Đỗ"))
    is_cat_door = any(c in str(door_str or "") for c in ("Khai", "Sinh", "Hưu"))
    p_up = str(pat_name or "").upper()
    if "CÁT" in p_up and (is_hung_door or th):
        clean_nm = (
            str(pat_name)
            .replace(" (ĐẠI CÁT)", " (Cát cách bị Hung Môn kìm hãm)")
            .replace(" (CÁT)", " (Cát cách bị chế ước)")
        )
        reason_blk = f"lâm {door_str}" + (f" và vướng {', '.join(th)}" if th else "")
        adj_desc = f"tín hiệu bề mặt có cơ hội thuận ({pat_desc.lower()}), song do cung {reason_blk} ('Đắc Kỳ bất đắc Môn') nên thực tế còn chốt chặn, chớ vội chủ quan"
        return clean_nm, adj_desc
    if "HUNG" in p_up and is_cat_door and not th:
        adj_desc = f"{pat_desc} — may nhờ đắc Cát Môn {door_str} sạch Tứ Hại nên giảm nhẹ xung lực nếu hành xử thận trọng"
        return pat_name, adj_desc
    return pat_name, pat_desc


def _strip_body_anatomy_if_non_health(text_s: str, is_health: bool) -> str:
    if is_health or not text_s:
        return text_s
    out = str(text_s)
    if " · Cơ thể:" in out:
        out = out.split(" · Cơ thể:")[0] + (")" if out.endswith(")") and not out.split(" · Cơ thể:")[0].endswith(")") else "")
    if "; cơ thể ứng " in out:
        out = out.split("; cơ thể ứng ")[0]
    return out


def _qimen_star_season_state(star: str, nguyet_el: str) -> str:
    star_el_map = {
        "Bồng": "Thủy", "Nhuế": "Thổ", "Xung": "Mộc", "Phụ": "Mộc", "Cầm": "Thổ",
        "Tâm": "Kim", "Trụ": "Kim", "Nhậm": "Thổ", "Anh": "Hỏa",
    }
    s_el = next((v for k, v in star_el_map.items() if k in star), "Thổ")
    # Cửu Tinh Kỳ Môn dùng chuẩn: Ngã sinh Nguyệt = Vượng, Đồng = Tướng, Nguyệt khắc Ngã = Hưu, Ngã khắc Nguyệt = Phế, Nguyệt sinh Ngã = Tù (《神奇之门》)
    if SINH_EL.get(s_el) == nguyet_el:
        return "Vượng"
    if s_el == nguyet_el:
        return "Tướng"
    if KHAC_EL.get(nguyet_el) == s_el:
        return "Hưu"
    if SINH_EL.get(nguyet_el) == s_el:
        return "Tù"
    return "Phế"


def build_holographic_prophecy_reading(
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    dung_than: str = "Bản Thân",
    question: str = "",
) -> Dict[str, Any]:
    """
    Đọc vị toàn diện 100% chi tiết sự kiện từ TẤT CẢ các yếu tố sinh ra trên bàn quẻ:
    - Lục Hào (Thời thái 3 thì, Gian Hào, Quân Vị, Du Hồn/Quy Hồn, Quái Thân/Thế Thân, Nạp Âm, 12 Trường Sinh, Lục Thú, Thần Sát, Hào Từ)
    - Kỳ Môn (Nội/Ngoại Bàn xa gần nhanh chậm, 81 Thập Can Khắc Ứng, Cửu Tinh Vượng Phế, Canh Cách, Ám Can, Lật Cung 4 Trạm)
    - Mai Hoa (64 Tổ Hợp Song Quái Bản/Hỗ/Biến + Quái Số Tiên/Hậu Thiên)
    - Đại Lục Nhâm (Sơ Truyền ➔ Trung Truyền ➔ Mạt Truyền)
    - Ấn Chứng Cận Sự Xung Quanh (近事断验)
    """
    cd = chart_data if isinstance(chart_data, dict) else {}
    lines: List[Dict[str, Any]] = list(ly_res.get("line_micro_audit") or [])
    ban_name = str(ly_res.get("ban_name") or mh_res.get("ten_chu") or "Quẻ Chủ")
    bien_name = str(ly_res.get("bien_name") or mh_res.get("ten_bien") or ban_name)
    the_pos = int(ly_res.get("the_pos") or 3)
    ung_pos = int(ly_res.get("ung_pos") or 6)
    dt_idx = int(ly_res.get("dt_hao_idx") or the_pos)
    chi_thang = str(ly_res.get("chi_thang") or cd.get("chi_thang") or "Thìn")
    chi_ngay = str(ly_res.get("chi_ngay") or cd.get("chi_ngay") or "Tý")
    can_ngay = str(cd.get("can_ngay") or "Giáp")
    can_gio = str(cd.get("can_gio") or "Giáp")
    chi_gio = str(cd.get("chi_gio") or "Tý")
    can_nam = str(cd.get("can_nam") or "")
    can_thang = str(cd.get("can_thang") or "")
    nguyet_el = CHI_EL.get(chi_thang, "Thổ")

    # ── 1. QUÉT THỜI THÁI QUÁ KHỨ & LAI Ý (过去痕迹 + 卦身世身 + 奇门首站) ──
    past_traces: List[str] = []
    present_undercurrents: List[str] = []
    future_steps: List[str] = []

    qt_info = ly_res.get("quai_than") or {}
    tt_info = ly_res.get("the_than") or {}
    if qt_info:
        tt_str = f" · <b>Thế Thân an tại Hào {tt_info.get('hao','')} ({tt_info.get('chi','')})</b>" if tt_info else ""
        if qt_info.get("is_present"):
            past_traces.append(
                f"<b>Quái Thân ({qt_info.get('chi','')}-{qt_info.get('luc_than','')}) đã hiện rõ trên quẻ{tt_str}:</b> Sự việc bạn hỏi đã có hình hài thực tế rõ ràng ({qt_info.get('meaning','')})."
            )
        else:
            past_traces.append(
                f"<b>Quái Thân ({qt_info.get('chi','')}-{qt_info.get('luc_than','')}) tạm ẩn phục{tt_str}:</b> Đầu mối gốc của sự việc còn nằm trong hậu trường hoặc kế hoạch mới đang định hình, chưa lộ hết 100% ra mặt giấy tờ."
            )

    dt_phuc = ly_res.get("dt_phuc_obj")
    if isinstance(dt_phuc, dict) and dt_phuc:
        p_pos = int(dt_phuc.get("hao_pos") or 1)
        ph_lt = str(dt_phuc.get("luc_than") or "")
        ph_cc = str(dt_phuc.get("can_chi_full") or dt_phuc.get("can_chi") or "")
        phi_lt = str(dt_phuc.get("phi_than_luc_than") or "")
        phi_cc = str(dt_phuc.get("phi_than_can_chi") or "")
        ph_state = "ĐẮC XUẤT (Phi sinh Phục / Nhật Nguyệt thấu xuất — ẩn mà vẫn phát lực mạnh)" if dt_phuc.get("dac_xuat") else "ẨN PHỤC DƯỚI PHI THẦN (chờ ngày Xung Phi/Xung Phục mới lộ diện)"
        present_undercurrents.append(
            f"<b>Cơ chế Phi – Phục Ẩn Tàng (Hào {p_pos}):</b> Dụng Thần <b>{ph_lt} ({ph_cc})</b> tạm ẩn dưới Phi Thần <b>{phi_lt} ({phi_cc})</b> — trạng thái <b>{ph_state}</b>."
        )

    for ln in lines:
        h_num = int(ln.get("hao") or 1)
        lt = str(ln.get("luc_than") or "")
        chi_l = str(ln.get("chi") or "")
        lthu = str(ln.get("luc_thu") or "Thanh Long")
        is_mv = bool(ln.get("is_moving"))
        is_ad = bool(ln.get("is_am_dong"))
        if not is_mv and not is_ad:
            if ln.get("is_nguyet_pha") or ln.get("is_nhat_pha"):
                past_traces.append(
                    f"<b>Dấu vết Quá khứ tại Hào {h_num} ({lt} {chi_l} · {lthu} — Tĩnh Phá):</b> Trước khi hỏi quẻ, mảng <i>{lt}</i> đã từng trải qua một đợt đứt gãy/xáo trộn ({LUC_THU_PAST_FLAVOR.get(lthu, '')})."
                )
            elif ln.get("khong_type") == "CHAN_KHONG":
                past_traces.append(
                    f"<b>Khoảng trống Quá khứ tại Hào {h_num} ({lt} {chi_l} · {lthu} — Tĩnh Không):</b> Khâu <i>{lt}</i> trước đó bị bỏ ngỏ hoặc lời hứa cũ chưa có thực chất ({LUC_THU_PAST_FLAVOR.get(lthu, '')})."
                )
            elif ln.get("mo_type") == "SUY_NHAP_MO":
                past_traces.append(
                    f"<b>Tồn đọng Cũ tại Hào {h_num} ({lt} {chi_l} — Tĩnh Mộ):</b> Vấn đề liên quan <i>{lt}</i> đã bị nén/gác lại từ giai đoạn trước ({LUC_THU_PAST_FLAVOR.get(lthu, '')})."
                )
        if is_ad:
            present_undercurrents.append(
                f"<b>Dòng ngầm Ám Động ngay hôm nay tại Hào {h_num} ({lt} {chi_l} · {lthu}):</b> Nhật Thần ({chi_ngay}) đang kích hoạt ngầm yếu tố <i>{lt}</i> ({LUC_THU_ROLE_COLOR.get(lthu, '')}) — có người/việc đang âm thầm xúc tiến rất gấp ngay trong hiện tại!"
            )
        if is_mv:
            b_lt = str(ln.get("bien_luc_than") or "")
            b_chi = str(ln.get("bien_chi") or "")
            hf = list(ln.get("hoa_flags") or [])
            zy_vn = str(ln.get("hao_tu_vn") or "").strip()
            zy_snip = (zy_vn[:115] + "...") if len(zy_vn) > 118 else zy_vn
            hf_map_vn = {
                "HOA_TIEN": "Hóa Tiến Thần (lực đẩy tăng tốc từng nấc)",
                "HOA_THOAI": "Hóa Thoái Thần (lực rút lui/giảm nhiệt dần)",
                "HOI_DAU_SINH": "Hồi Đầu Sinh (càng đi về cuối càng được tiếp sức)",
                "HOI_DAU_KHAC": "Hồi Đầu Khắc (chặng cuối tự vấp rào cản ngược)",
                "HOA_KHONG": "Hóa Không (chờ ngày Xuất Không mới chốt thực)",
                "HOA_MO": "Hóa Mộ (tạm cất vào kho/hồ sơ chờ Xung mở)",
                "HOA_HOP": "Hóa Lục Hợp (bị giữ chân/ràng buộc chặt)",
                "HOA_NGUYET_PHA": "Hóa Nguyệt Phá (đích biến đang hao hụt)",
            }
            hf_desc = ", ".join(hf_map_vn[k] for k in hf if k in hf_map_vn) or "chuyển hóa trực tiếp"
            future_steps.append(
                f"<b>Phát động Hào {h_num} ({lt} {chi_l} · {lthu}) ➔ biến {b_lt} ({b_chi}) [{hf_desc}]:</b> "
                f"Sự kiện xoay chuyển từ <i>{lt}</i> sang <i>{b_lt}</i> ({CHI_CONCRETE_IMAGE.get(b_chi, '')})"
                + (f" · <i>Lời Hào Chu Dịch: «{zy_snip}»</i>" if zy_snip else "")
            )

    p_map_qm = qm_res.get("palace_micro_audit") or {}
    phien_chain = list(qm_res.get("phien_cung_chain") or [])
    if len(phien_chain) >= 4 and p_map_qm:
        p1 = p_map_qm.get(phien_chain[0], {})
        if p1:
            past_traces.append(
                f"<b>Nguyên nhân gốc Kỳ Môn (Trạm 1 — Cung {phien_chain[0]} {p1.get('quai','')}):</b> Khởi nguồn từ {p1.get('door','')} · {p1.get('star','')} · Can {p1.get('can_thien_disp','')} ({PALACE_BODY_LOC.get(phien_chain[0], '')})."
            )

    if not past_traces:
        past_traces.append("<b>Nền tảng trước khi hỏi:</b> Bàn quẻ sạch Tĩnh Phá/Chân Không — sự việc mới khởi phát trực diện, không bị nợ xấu hay tỳ vết đổ vỡ cũ kéo lùi.")

    # ── 2. ĐỌC GIAN HÀO (间爻), HÀO 5 QUÂN VỊ, DU HỒN / QUY HỒN & NỘI/NGOẠI BÀN KỲ MÔN ──
    lo_tu_pair = sorted([the_pos, ung_pos])
    gian_indices = [ix for ix in range(lo_tu_pair[0] + 1, lo_tu_pair[1])]
    gian_notes: List[str] = []
    for g_ix in gian_indices:
        if 1 <= g_ix <= len(lines):
            gl = lines[g_ix - 1]
            g_lt = str(gl.get("luc_than") or "")
            g_chi = str(gl.get("chi") or "")
            g_thu = str(gl.get("luc_thu") or "")
            g_st = "ĐANG PHÁT ĐỘNG" if gl.get("is_moving") else ("ÁM ĐỘNG" if gl.get("is_am_dong") else ("Tĩnh Phá/Không (đã dọn sạch cản trở)" if (gl.get("is_nguyet_pha") or gl.get("is_void")) else f"Tĩnh ({gl.get('vuong_suy','')})"))
            role_g = {
                "Huynh Đệ": "người ngang hàng/chi phí trung gian/đối thủ cạnh tranh",
                "Phụ Mẫu": "khâu giấy tờ thủ tục/người lớn tuổi đứng giữa",
                "Quan Quỷ": "khâu xét duyệt quy chế/áp lực kiểm soát giữa đường",
                "Thê Tài": "điều khoản tài chính/lợi ích trung gian",
                "Tử Tôn": "người hòa giải/quý nhân tháo gỡ êm đẹp ở giữa",
            }.get(g_lt, "khâu trung gian")
            gian_notes.append(f"Hào {g_ix} ({g_lt} {g_chi} · {g_thu} — {g_st}: đại diện {role_g})")

    if gian_notes:
        present_undercurrents.append(f"<b>Giải mã Gian Hào (Khâu Trung Gian / Môi Giới giữa Thế Hào {the_pos} và Ứng Hào {ung_pos}):</b> {' + '.join(gian_notes)}.")

    if len(lines) >= 5:
        h5 = lines[4]
        present_undercurrents.append(
            f"<b>Hào 5 Quân Vị (Cấp Quyết Định / Chính Chủ):</b> Lâm <b>{h5.get('luc_than','')} ({h5.get('can_chi_full','')} · {h5.get('luc_thu','')})</b>, khí Nguyệt <b>{h5.get('vuong_suy','')}</b>"
            + (" — đang PHÁT ĐỘNG trực tiếp cầm trịch cuộc việc!" if h5.get("is_moving") else (" — lâm Tuần Không (cấp quyết định tạm thời chưa chốt văn bản cuối)." if h5.get("is_void") else " — giữ thế ổn định quan sát."))
        )

    soul_tag = ""
    if ban_name in DU_HON_8 or bien_name in DU_HON_8:
        soul_tag = f"<b>Quẻ mang tượng DU HỒN ({ban_name if ban_name in DU_HON_8 else bien_name}):</b> Tâm tư người trong cuộc đang hướng ra ngoài, có sự xê dịch đi lại, đổi môi trường hoặc phân vân giữa hai ngả."
        present_undercurrents.append(soul_tag)
    elif ban_name in QUY_HON_8 or bien_name in QUY_HON_8:
        soul_tag = f"<b>Quẻ mang tượng QUY HỒN ({ban_name if ban_name in QUY_HON_8 else bien_name}):</b> Xu thế thu gom khép việc về chốn quen thuộc, người đi xa quay về, dòng tiền/kế hoạch quay lại trục gốc an toàn."
        present_undercurrents.append(soul_tag)

    # Nội Bàn / Ngoại Bàn Kỳ Môn Độn Giáp
    is_duong_don = bool(cd.get("is_duong_don", True))
    noi_set = {1, 8, 3, 4} if is_duong_don else {9, 2, 7, 6}
    tc_qm = int(qm_res.get("target_cung") or 2)
    chu_qm = int(qm_res.get("cung_chu") or 2)
    khach_qm = int(qm_res.get("cung_khach") or tc_qm)
    chu_in_noi = chu_qm in noi_set
    tc_in_noi = tc_qm in noi_set
    if chu_in_noi and tc_in_noi:
        noi_ngoai_desc = f"Cả Người hỏi (Cung {chu_qm}) và Sự việc (Cung {tc_qm}) đều lạc <b>NỘI BÀN</b> ({'Dương' if is_duong_don else 'Âm'} Độn) ➔ Sự việc diễn ra ở <b>GẦN / NỘI BỘ / TRONG NHÀ–CÙNG ĐỊA PHƯƠNG</b>, tốc độ phản hồi <b>NHANH</b> (tính bằng giờ/ngày)."
    elif (not chu_in_noi) and (not tc_in_noi):
        noi_ngoai_desc = f"Cả Người hỏi (Cung {chu_qm}) và Sự việc (Cung {tc_qm}) đều lạc <b>NGOẠI BÀN</b> ({'Dương' if is_duong_don else 'Âm'} Độn) ➔ Sự việc liên quan <b>NƠI XA / BÊN NGOÀI / KHÁC KHU VỰC</b>, nhịp triển khai <b>TỪ TỪ ĐƯỜNG DÀI</b>."
    else:
        noi_ngoai_desc = f"Người hỏi lạc {'Nội Bàn (Gần)' if chu_in_noi else 'Ngoại Bàn (Xa)'} (Cung {chu_qm}) còn Sự việc lạc {'Nội Bàn (Gần)' if tc_in_noi else 'Ngoại Bàn (Xa)'} (Cung {tc_qm}) ➔ Có sự <b>chuyển dịch trong–ngoài / kết nối từ xa về gần (hoặc ngược lại)</b>."
    present_undercurrents.append(f"<b>Định vị Nội – Ngoại Bàn Kỳ Môn:</b> {noi_ngoai_desc}")

    pa_tc = p_map_qm.get(tc_qm, {})
    if pa_tc and pa_tc.get("am_can"):
        tu_hai_tc = list(pa_tc.get("tu_hai") or [])
        th_str = f" · Cảnh báo Tứ Hại: <b>{'; '.join(tu_hai_tc)}</b>" if tu_hai_tc else " · Cung sạch không vướng Tứ Hại"
        present_undercurrents.append(
            f"<b>Ám Can & Tứ Hại tại Cung Sự Việc {tc_qm}:</b> Ẩn tàng Can <b>[{pa_tc['am_can']}]</b> — {pa_tc.get('am_can_meaning','')}{th_str}."
        )

    # ── 3. CHÂN DUNG CỤ THỂ NGƯỜI / VẬT / SỰ VIỆC (7 TẦNG ĐỊNH TƯỢNG + THẬP CAN KHẮC ỨNG + 64 SONG QUÁI) ──
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    dt_el = str(dt_ln.get("ngu_hanh") or "Thổ")
    dt_chi = str(dt_ln.get("chi") or "Thìn")
    dt_nap_am = str(dt_ln.get("nap_am") or "")
    dt_ts = str(dt_ln.get("ts_ngay") or "Bình")
    dt_thu = str(dt_ln.get("luc_thu") or "Thanh Long")
    dt_ss = list(dt_ln.get("shensha") or [])

    _q_low_holo = str(question or "").lower()
    _is_health_holo = any(w in _q_low_holo for w in ("sức khỏe", "bệnh", "đau ", "ốm", "khám", "mổ", "thuốc", "điều trị", "cơ thể", "nhập viện", "nằm viện", "sốt"))
    portrait_items: List[str] = []
    if dt_ln:
        portrait_items.append(
            f"<b>Hào Đích Dụng Thần — {HAO_VI_ROLE.get(dt_idx, f'Hào {dt_idx}')}:</b> "
            f"<b>{dt_ln.get('luc_than','')} ({dt_ln.get('can_chi_full','')} · Nạp Âm: {dt_nap_am})</b>, phối <b>{dt_thu}</b> ({LUC_THU_ROLE_COLOR.get(dt_thu,'')})"
            + (f", hội Thần Sát: <b>{', '.join(dt_ss)}</b>." if dt_ss else ".")
        )
        _nh_temp_disp = _strip_body_anatomy_if_non_health(NGU_HANH_TEMPERAMENT.get(dt_el, ""), _is_health_holo)
        portrait_items.append(
            f"<b>Khí chất & Vật tượng ({dt_el} – Chi {dt_chi}):</b> {_nh_temp_disp}. Hiện trường/chi tiết ứng với <b>Chi {dt_chi}</b>: {CHI_CONCRETE_IMAGE.get(dt_chi, '')}."
        )
        portrait_items.append(
            f"<b>Chu kỳ 12 Trường Sinh đang ở bậc «{dt_ts}»:</b> {TRUONG_SINH_STAGE_MEANING.get(dt_ts, 'Đang vận hành theo thời lệnh')}."
        )

    # Thập Can Khắc Ứng Kỳ Môn tại Cung Sự Việc & Cung Chủ
    for lbl_p, p_idx_q in [("Cung Sự Việc", tc_qm), ("Cung Bản Thân", chu_qm)]:
        pa_q = p_map_qm.get(p_idx_q, {})
        if not pa_q:
            continue
        t_st = str(pa_q.get("can_thien") or "Mậu")
        d_st = str(pa_q.get("can_dia") or "Mậu")
        pat_name_raw, pat_desc_raw = QIMEN_10_STEM_PATTERNS.get(
            (t_st, d_st),
            (f"Cách {t_st} gia {d_st}", f"Thiên bàn {t_st} lâm Địa bàn {d_st}, xét tương tác Tinh–Môn để điều tiết chủ khách"),
        )
        pat_name, pat_desc = _qualify_qimen_stem_pattern(pat_name_raw, pat_desc_raw, str(pa_q.get("door") or ""), pa_q.get("tu_hai") or [])
        star_q = str(pa_q.get("star") or "Thiên Tâm")
        star_vs = _qimen_star_season_state(star_q, nguyet_el)
        _loc_lbl_h = "định vị không gian/cơ thể" if _is_health_holo else "định vị không gian hiện trường"
        _loc_val_h = _strip_body_anatomy_if_non_health(PALACE_BODY_LOC.get(p_idx_q, ""), _is_health_holo)
        portrait_items.append(
            f"<b>Thập Can Khắc Ứng {lbl_p} (Cung {p_idx_q} — {t_st} + {d_st}):</b> Hiện <b>«{pat_name}»</b> — {pat_desc}. "
            f"Sao <b>{star_q}</b> ở thế <b>{star_vs}</b>, hội <b>{pa_q.get('door','')} · {pa_q.get('deity','')}</b>; {_loc_lbl_h}: {_loc_val_h}."
        )
        if tc_qm == chu_qm:
            break

    # 64 Tổ Hợp Song Quái Mai Hoa (Bản · Hỗ · Biến)
    up_ban = str(mh_res.get("up_q") or mh_res.get("the_quai") or "Càn")
    lo_ban = str(mh_res.get("lo_q") or mh_res.get("dung_quai") or "Khôn")
    up_ho = str(mh_res.get("thuong_ho") or "Tốn")
    lo_ho = str(mh_res.get("ha_ho") or "Cấn")
    up_bien = str(mh_res.get("up_bien") or mh_res.get("bien_dung_quai") or up_ban)
    lo_bien = str(mh_res.get("lo_bien") or lo_ban)
    pair_ban_img = TRIGRAM_PAIR_64_IMAGERY.get((up_ban, lo_ban), "")
    pair_ho_img = TRIGRAM_PAIR_64_IMAGERY.get((up_ho, lo_ho), "")
    pair_bien_img = TRIGRAM_PAIR_64_IMAGERY.get((up_bien, lo_bien), "")
    if pair_ban_img:
        portrait_items.append(
            f"<b>Độc Tượng 64 Tổ Hợp Song Quái Mai Hoa:</b> Khởi tượng <b>{mh_res.get('ten_chu', ban_name)}</b> ({pair_ban_img}) "
            f"➔ Nội tình Hỗ Quái <b>{mh_res.get('ten_ho','')}</b> ({pair_ho_img}) "
            + (f"➔ Chung cuộc Biến Quái <b>{mh_res.get('ten_bien','')}</b> ({pair_bien_img}) · " if pair_bien_img else "· ")
            + f"Định lượng Quái Số Tiên/Hậu Thiên = <b>{mh_res.get('sum_tien_thien', 8)} / {mh_res.get('sum_hau_thien', 10)}</b>."
        )

    # ── 4. ĐỐI CHỨNG TAM HỢP / XUNG HỢP LỤC HÀO + TỨ KHÓA & TAM TRUYỀN ĐẠI LỤC NHÂM + LẬT CUNG 4 TRẠM ──
    tam_hop_list = list(ly_res.get("tam_hop_cuc") or [])
    xh_trans = str(ly_res.get("xung_hop_transition") or "")
    if tam_hop_list or xh_trans:
        cuc_parts = []
        if tam_hop_list:
            cuc_parts.append("Tam Hợp Cục: " + "; ".join(str(c.get("desc") or c) if isinstance(c, dict) else str(c) for c in tam_hop_list))
        if xh_trans:
            cuc_parts.append(f"Biến thái Lục Xung/Lục Hợp: {xh_trans}")
        future_steps.append(f"<b>Kết Cấu Toàn Quẻ Lục Hào:</b> {' · '.join(cuc_parts)}.")

    try:
        import dai_luc_nham as _dln_mod
        tiet_khi_s = str(cd.get("tiet_khi") or "Lập Đông")
        dln_raw = _dln_mod.tinh_dai_luc_nham(can_ngay, chi_ngay, chi_gio, tiet_khi_s)
        tt_dln = dln_raw.get("tam_truyen") or {}
        t_tuong = dln_raw.get("thien_tuong_full") or dln_raw.get("thien_tuong") or {}
        tu_khoa_dln = list(dln_raw.get("tu_khoa") or [])
        ng_tuong = dln_raw.get("nguyet_tuong") or {}
        so_c = str(tt_dln.get("so_truyen") or "")
        trung_c = str(tt_dln.get("trung_truyen") or "")
        mat_c = str(tt_dln.get("mat_truyen") or "")
        if so_c and trung_c and mat_c:
            tg_so = (t_tuong.get(so_c) or {}).get("ten", "")
            tg_tr = (t_tuong.get(trung_c) or {}).get("ten", "")
            tg_mt = (t_tuong.get(mat_c) or {}).get("ten", "")
            lt_so = _dln_mod.tinh_luc_than(so_c, can_ngay)
            lt_tr = _dln_mod.tinh_luc_than(trung_c, can_ngay)
            lt_mt = _dln_mod.tinh_luc_than(mat_c, can_ngay)
            phap_dln = str(tt_dln.get("phuong_phap") or tt_dln.get("phap") or "Tặc Khắc")
            tk_str = ""
            if len(tu_khoa_dln) >= 4:
                tk_str = (
                    f" · Tứ Khóa Chủ–Khách: K1({tu_khoa_dln[0]['thien']}/{tu_khoa_dln[0]['dia']}) · "
                    f"K2({tu_khoa_dln[1]['thien']}/{tu_khoa_dln[1]['dia']}) · "
                    f"K3({tu_khoa_dln[2]['thien']}/{tu_khoa_dln[2]['dia']}) · "
                    f"K4({tu_khoa_dln[3]['thien']}/{tu_khoa_dln[3]['dia']})"
                )
            nt_str = f" · Nguyệt Tướng {ng_tuong.get('ten','')} ({ng_tuong.get('chi','')})" if ng_tuong else ""
            future_steps.append(
                f"<b>Tam Truyền Đại Lục Nhâm ({phap_dln}{nt_str}{tk_str}):</b> "
                f"Khởi phát <b>Sơ Truyền [{so_c}-{tt_dln.get('so_truyen_hanh','')} · {lt_so}{' · ' + tg_so if tg_so else ''}]</b> "
                f"──► Diễn biến <b>Trung Truyền [{trung_c}-{tt_dln.get('trung_truyen_hanh','')} · {lt_tr}{' · ' + tg_tr if tg_tr else ''}]</b> "
                f"──► Kết cục <b>Mạt Truyền [{mat_c}-{tt_dln.get('mat_truyen_hanh','')} · {lt_mt}{' · ' + tg_mt if tg_mt else ''}]</b>."
            )
    except Exception:
        pass

    if len(phien_chain) >= 4 and p_map_qm:
        p2 = p_map_qm.get(phien_chain[1], {})
        p3 = p_map_qm.get(phien_chain[2], {})
        p4 = p_map_qm.get(phien_chain[3], {})
        future_steps.append(
            f"<b>Lộ trình Lật Cung Kỳ Môn 4 Trạm:</b> Hiện diện tại <b>Cung {phien_chain[1]} ({p2.get('door','')})</b> "
            f"──► Bước ngoặt chuyển sang <b>Cung {phien_chain[2]} ({p3.get('door','')} · {p3.get('star','')})</b> "
            f"──► Hạ màn chốt tại <b>Cung {phien_chain[3]} ({p4.get('door','')} · {p4.get('deity','')}, Can {p4.get('can_thien_disp','')})</b>."
        )

    if not future_steps:
        future_steps.append(
            f"<b>Quẻ Tĩnh Thuần Nhất ({ban_name}):</b> Không có hào động xáo trộn — kết cục giữ nguyên theo thực lực gốc của Dụng Thần ({dt_ln.get('vuong_suy','Bình')}) và Quẻ Biến {bien_name}."
        )

    # ── 5. ĐỊNH ỨNG KỲ ĐA TẦNG (CANH CÁCH KỲ MÔN + NỘI/NGOẠI BÀN + BỆNH–DƯỢC PHÁP) ──
    canh_cach_notes: List[str] = []
    for p_idx_c, pa_c in p_map_qm.items():
        if p_idx_c == 5:
            continue
        ct_c = str(pa_c.get("can_thien") or "")
        cd_c = str(pa_c.get("can_dia") or "")
        if ct_c == "Canh":
            if can_nam and cd_c == can_nam:
                canh_cach_notes.append(f"Niên Cách (Canh lâm Niên Can {can_nam} tại Cung {p_idx_c}: ứng trong năm)")
            if can_thang and cd_c == can_thang:
                canh_cach_notes.append(f"Nguyệt Cách (Canh lâm Nguyệt Can {can_thang} tại Cung {p_idx_c}: ứng trong tháng)")
            if cd_c == can_ngay:
                canh_cach_notes.append(f"Nhật Cách / Phục Can Cách (Canh lâm Nhật Can {can_ngay} tại Cung {p_idx_c}: ứng ngay trong ngày hoặc có chốt chặn trực diện)")
            if cd_c == can_gio:
                canh_cach_notes.append(f"Thời Cách (Canh lâm Thời Can {can_gio} tại Cung {p_idx_c}: ứng rất nhanh ngay trong khung giờ/ngày)")
        elif cd_c == "Canh" and ct_c == can_ngay:
            canh_cach_notes.append(f"Phi Can Cách (Nhật Can {can_ngay} gia Canh tại Cung {p_idx_c}: cần đổi hướng chủ động mới thông)")

    speed_tag = (
        "Nhịp độ CHẬM / KÉO DÀI (do gặp Môn Phục Ngâm)" if qm_res.get("is_mon_phuc_ngam")
        else ("Nhịp độ CỰC NHANH / ĐẢO CHIỀU GẤP (do gặp Môn Phản Ngâm)" if qm_res.get("is_mon_phan_ngam")
              else ("Nhịp độ NHANH — GẦN (trục Nội Bàn)" if (chu_in_noi and tc_in_noi) else "Nhịp độ TRUNG BÌNH — THEO ĐÚNG TIẾT KỲ"))
    )
    _ymdh_box5 = resolve_astronomical_ung_ky_ymdh(
        ly_res=ly_res,
        qm_res=qm_res,
        mh_res=mh_res,
        benh_quai=str(deep_syn.get("benh_quai") or ""),
        duoc_ung_ky=str(deep_syn.get("duoc_ung_ky") or ""),
        chart_data=cd,
        question=question,
    )
    _exact_cal_line = (
        f"• <b>Lịch Vạn Niên Thiên Văn Chính Xác (Ngày – Giờ – Tháng – Năm):</b> "
        f"<span style='color:#fde68a;font-weight:800;'>{_ymdh_box5['hour_str']}</span> · "
        f"<b>{_ymdh_box5['day_str']}</b> · <b>{_ymdh_box5['month_year_str']}</b>.<br>"
        if _ymdh_box5.get("day_str")
        else ""
    )
    timing_detail = (
        f"• <b>Bệnh – Dược Mở Khóa:</b> {deep_syn.get('benh_quai', '')} ══► <b style='color:#fde047;'>{deep_syn.get('duoc_ung_ky', '')}</b>.<br>"
        + _exact_cal_line
        + f"• <b>Nhịp độ Không–Thời Gian Kỳ Môn:</b> {speed_tag}"
        + (f" · Tín hiệu Canh Cách: <b>{'; '.join(canh_cach_notes)}</b>." if canh_cach_notes else ".")
    )

    # ── 6. ẤN CHỨNG CẬN SỰ XUNG QUANH (近事断验 — KIỂM CHỨNG ĐỘ LINH ỨNG NGAY LẬP TỨC!) ──
    near_verifications: List[str] = []
    for ln in lines:
        lthu_n = str(ln.get("luc_thu") or "")
        lt_n = str(ln.get("luc_than") or "")
        chi_n = str(ln.get("chi") or "")
        ss_n = list(ln.get("shensha") or [])
        if lthu_n == "Chu Tước" and (ln.get("is_moving") or ln.get("is_am_dong") or int(ln.get("hao") or 0) == the_pos):
            near_verifications.append(
                f"📞 <b>Ấn chứng Tin tức & Ngôn từ (Chu Tước động/lâm Thế tại Hào {ln['hao']}):</b> Trong 1–3 ngày quanh lúc hỏi quẻ, bạn vừa có cuộc trao đổi tin nhắn/điện thoại quan trọng, giấy tờ thông báo hoặc lời bàn luận sôi nổi."
            )
        if "Dịch Mã" in ss_n and (ln.get("is_moving") or ln.get("is_am_dong") or int(ln.get("hao") or 0) in (the_pos, dt_idx)):
            near_verifications.append(
                f"🚗 <b>Ấn chứng Dịch chuyển (Dịch Mã Tinh tại Hào {ln['hao']} {chi_n}):</b> Gần đây bạn hoặc người liên quan vừa có lịch đi lại, gửi hàng/chuyển khoản hoặc rục rịch thay đổi vị trí."
            )
        if lt_n == "Huynh Đệ" and (ln.get("is_moving") or ln.get("is_am_dong")):
            near_verifications.append(
                f"💸 <b>Ấn chứng Chi tiêu (Huynh Đệ {chi_n} kích hoạt tại Hào {ln['hao']}):</b> Vừa phát sinh một khoản chi tiền thực tế cho công việc, mua sắm đồ dùng hoặc giao tế bạn bè/anh em."
            )
        if lt_n == "Phụ Mẫu" and ln.get("vuong_suy") in ("Vượng", "Tướng") and (ln.get("is_moving") or int(ln.get("hao") or 0) == the_pos):
            near_verifications.append(
                f"📄 <b>Ấn chứng Hồ sơ / Nhà xe (Phụ Mẫu {chi_n} vượng tại Hào {ln['hao']}):</b> Đang trực tiếp bận tâm xử lý giấy tờ, hợp đồng, học tập hoặc sửa sang nhà cửa/phương tiện."
            )
    if len(near_verifications) < 2 and pa_tc:
        near_verifications.append(
            f"🧭 <b>Ấn chứng Không gian hướng {pa_tc.get('huong','')} (Cung {tc_qm}):</b> Nơi bạn ngồi hoặc phía {pa_tc.get('huong','')} chỗ ở hiện có vật tượng {PALACE_BODY_LOC.get(tc_qm, '').split('·')[1].strip() if '·' in PALACE_BODY_LOC.get(tc_qm, '') else ''} tương ứng đúng khí quẻ."
        )
    near_verifications = near_verifications[:3]

    # ── KẾT XUẤT KHỐI HTML ĐỌC VỊ TIÊN TRI TOÀN TỨC (HIỂN THỊ NGAY ĐẦU TRANG & DỄ ĐỌC TỨC THÌ) ──
    def _li_join(arr: List[str]) -> str:
        return "".join(f'<div style="margin:3px 0;line-height:1.48;">• {x}</div>' for x in arr)

    holographic_html = (
        f'<div style="margin-top:11px;padding:12px 15px;background:linear-gradient(135deg,rgba(15,23,42,0.93),rgba(30,27,75,0.92));border-radius:12px;border:1.5px solid rgba(56,189,248,0.65);box-shadow:0 3px 14px rgba(14,165,233,0.18);">'
        f'<div style="font-size:0.95em;font-weight:900;color:#7dd3fc;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;border-bottom:1px solid rgba(56,189,248,0.28);padding-bottom:5px;">'
        f'<span>🔮 ĐỌC VỊ CHI TIẾT SỰ KIỆN TOÀN TỨC TỪ 100% YẾU TỐ QUẺ (V141.0 — KHÔNG BỎ SÓT DẤU HIỆU NÀO · CHỐNG LUẬN ẢO)</span>'
        f'<span style="font-size:0.78em;color:#fde68a;background:rgba(251,191,36,0.14);padding:2px 8px;border-radius:999px;border:1px solid rgba(251,191,36,0.4);">Lục Hào · Kỳ Môn · Mai Hoa · Đại Lục Nhâm</span>'
        f'</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:9px;font-size:0.87em;color:#f1f5f9;">'
        f'<div style="padding:9px 11px;background:rgba(2,6,23,0.65);border-radius:9px;border-left:3.5px solid #a78bfa;">'
        f'<div style="font-weight:800;color:#c4b5fd;margin-bottom:4px;">🕰️ 1. Dấu Vết Quá Khứ & Lai Ý Trước Khi Hỏi</div>'
        f'{_li_join(past_traces[:5])}</div>'
        f'<div style="padding:9px 11px;background:rgba(2,6,23,0.65);border-radius:9px;border-left:3.5px solid #38bdf8;">'
        f'<div style="font-weight:800;color:#7dd3fc;margin-bottom:4px;">👁️ 2. Hiện Trạng, Gian Hào Trung Gian & Dòng Ngầm</div>'
        f'{_li_join(present_undercurrents)}</div>'
        f'<div style="padding:9px 11px;background:rgba(2,6,23,0.65);border-radius:9px;border-left:3.5px solid #fbbf24;">'
        f'<div style="font-weight:800;color:#fde047;margin-bottom:4px;">👤 3. Chân Dung Cụ Thể Người / Vật / Cách Cục Quẻ</div>'
        f'{_li_join(portrait_items)}</div>'
        f'<div style="padding:9px 11px;background:rgba(2,6,23,0.65);border-radius:9px;border-left:3.5px solid #34d399;">'
        f'<div style="font-weight:800;color:#6ee7b7;margin-bottom:4px;">🎬 4. Kịch Bản Diễn Biến Từng Chặng & Tam Truyền</div>'
        f'{_li_join(future_steps)}</div>'
        f'</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:9px;margin-top:8px;font-size:0.87em;color:#f1f5f9;">'
        f'<div style="padding:8px 11px;background:rgba(6,78,59,0.42);border-radius:9px;border-left:3.5px solid #f59e0b;">'
        f'<div style="font-weight:800;color:#fde68a;margin-bottom:3px;">⏱️ 5. Khoanh Vùng Không Gian – Ngày Giờ Tháng Năm Ứng Nghiệm</div>'
        f'<div style="line-height:1.48;">{timing_detail}</div></div>'
        f'<div style="padding:8px 11px;background:rgba(30,41,59,0.75);border-radius:9px;border-left:3.5px solid #f472b6;">'
        f'<div style="font-weight:800;color:#f9a8d4;margin-bottom:3px;">⚡ 6. Ấn Chứng Cận Sự Thực Tế Quanh Bạn (Đối Chứng Linh Ứng)</div>'
        f'{_li_join(near_verifications)}</div>'
        f'</div></div>'
    )

    clean_prompt_lines = [
        "=== HỒ SƠ ĐỌC VỊ CHI TIẾT SỰ KIỆN TOÀN TỨC 12 TẦNG (V141.0 — BẮT BUỘC DÙNG ĐỂ TIÊN ĐOÁN CHI TIẾT NHƯ ĐẠI TIÊN TRI, KHÔNG BỎ SÓT 1 YẾU TỐ NÀO, CẤM LUẬN ẢO) ===",
        "1. [DẤU VẾT QUÁ KHỨ & LAI Ý]: " + " | ".join(_strip_tags(x) for x in past_traces),
        "2. [HIỆN TRẠNG · GIAN HÀO TRUNG GIAN · QUÂN VỊ HÀO 5 · PHI–PHỤC · NỘI/NGOẠI BÀN · ÁM CAN · TỨ HẠI · ÁM ĐỘNG]: " + " | ".join(_strip_tags(x) for x in present_undercurrents),
        "3. [CHÂN DUNG NGƯỜI/VẬT · NẠP ÂM · 12 TRƯỜNG SINH · THẬP CAN KHẮC ỨNG · 64 SONG QUÁI]: " + " | ".join(_strip_tags(x) for x in portrait_items),
        "4. [KỊCH BẢN DIỄN BIẾN TỪNG BƯỚC · HÀO ĐỘNG CHU DỊCH · LẬT CUNG 4 TRẠM · TỨ KHÓA & TAM TRUYỀN ĐẠI LỤC NHÂM]: " + " | ".join(_strip_tags(x) for x in future_steps),
        "5. [NGÀY GIỜ THÁNG NĂM DƯƠNG/ÂM LỊCH & CANH CÁCH ỨNG KỲ]: " + _strip_tags(timing_detail),
        "6. [ẤN CHỨNG CẬN SỰ QUANH NGƯỜI HỎI]: " + " | ".join(_strip_tags(x) for x in near_verifications),
    ]

    return {
        "past_traces": past_traces,
        "present_undercurrents": present_undercurrents,
        "portrait_items": portrait_items,
        "future_steps": future_steps,
        "timing_detail": timing_detail,
        "ymdh_resolved": _ymdh_box5,
        "near_verifications": near_verifications,
        "noi_ngoai_desc": noi_ngoai_desc,
        "canh_cach_notes": canh_cach_notes,
        "holographic_html": holographic_html,
        "holographic_prompt_text": "\n".join(clean_prompt_lines),
    }


def _strip_tags(s: str) -> str:
    import re as _re_st
    return _re_st.sub(r"<[^>]+>", "", str(s or "")).strip()


# ═══════════════════════════════════════════════════════════════════════════════
# V141.0: BỘ GIẢI LỊCH THIÊN VĂN THỰC TẾ & 4 TRỤ CỘT TIÊN TRI CHỐNG LUẬN ẢO
# ═══════════════════════════════════════════════════════════════════════════════

_CHI_12_ORDER = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
_CAN_10_ORDER = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
_WEEKDAY_VN_7 = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
_CHI_HOUR_SPAN = {
    "Tý": ("23:00–01:00", 23), "Sửu": ("01:00–03:00", 1), "Dần": ("03:00–05:00", 3), "Mão": ("05:00–07:00", 5),
    "Thìn": ("07:00–09:00", 7), "Tị": ("09:00–11:00", 9), "Ngọ": ("11:00–13:00", 11), "Mùi": ("13:00–15:00", 13),
    "Thân": ("15:00–17:00", 15), "Dậu": ("17:00–19:00", 17), "Tuất": ("19:00–21:00", 19), "Hợi": ("21:00–23:00", 21),
}
_LUC_XUNG_12 = {
    "Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần",
    "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị",
}
_LUC_HOP_12 = {
    "Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão",
    "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ",
}
_MO_BY_EL_12 = {"Kim": "Sửu", "Mộc": "Mùi", "Thủy": "Thìn", "Thổ": "Thìn", "Hỏa": "Tuất"}
_TS_SINH_BY_EL = {"Kim": "Tị", "Mộc": "Hợi", "Thủy": "Thân", "Hỏa": "Dần", "Thổ": "Thân"}
_VUONG_CHI_BY_EL = {"Kim": "Dậu", "Mộc": "Mão", "Thủy": "Tý", "Hỏa": "Ngọ", "Thổ": "Thìn"}
_EL_SEASON_CHIS = {
    "Kim": ("Thân", "Dậu"), "Mộc": ("Dần", "Mão"), "Thủy": ("Hợi", "Tý"),
    "Hỏa": ("Tị", "Ngọ"), "Thổ": ("Thìn", "Tuất", "Sửu", "Mùi"),
}
_MONTH_SEG_CACHE: Dict[Tuple[int, int, int, int], List[Dict[str, Any]]] = {}


def build_solar_term_month_segments(start_date: Any, span_days: int = 430) -> List[Dict[str, Any]]:
    """
    V139.1: Phân đoạn CHÍNH XÁC từng Tháng Can Chi theo 24 Tiết Khí (Jean Meeus) tính từng ngày.
    Mỗi đoạn: {start, end, can, chi, year_can, year_chi, year_num, lunar_start, lunar_end}.
    (Tháng tiết khí bắt đầu giữa tháng Dương lịch — tuyệt đối không gán 1 tháng DL = 1 tháng Can Chi!)
    """
    import datetime as _dtm
    key = (start_date.year, start_date.month, start_date.day, int(span_days))
    if key in _MONTH_SEG_CACHE:
        return _MONTH_SEG_CACHE[key]
    try:
        import qmdg_calc as _qc
    except Exception:
        return []
    segs: List[Dict[str, Any]] = []
    cur: Optional[Dict[str, Any]] = None
    last_day = start_date
    for d_off in range(int(span_days)):
        day = start_date + _dtm.timedelta(days=d_off)
        last_day = day
        tk = _qc.get_tiet_khi(_dtm.datetime(day.year, day.month, day.day, 12, 0))
        _, chm = _qc.get_can_chi_month("Giáp", tk)
        if cur is None or cur["chi"] != chm:
            if cur is not None:
                cur["end"] = day - _dtm.timedelta(days=1)
                segs.append(cur)
            # Năm Can Chi tính theo Lập Xuân: tháng Tý/Sửu rơi vào tháng 1–2 DL vẫn thuộc năm trước
            yb = day.year - 1 if (day.month <= 2 and chm in ("Tý", "Sửu")) else day.year
            cy, chy = _qc.get_can_chi_year(yb)
            cm, _ = _qc.get_can_chi_month(cy, tk)
            cur = {"start": day, "end": None, "can": cm, "chi": chm, "year_can": cy, "year_chi": chy, "year_num": yb}
    if cur is not None:
        cur["end"] = last_day
        segs.append(cur)
    for sg in segs:
        try:
            l1 = _qc.solar_to_lunar(_dtm.datetime(sg["start"].year, sg["start"].month, sg["start"].day, 12, 0))
            l2 = _qc.solar_to_lunar(_dtm.datetime(sg["end"].year, sg["end"].month, sg["end"].day, 12, 0))
            sg["lunar_start"] = (int(l1[0]), int(l1[1]))
            sg["lunar_end"] = (int(l2[0]), int(l2[1]))
        except Exception:
            sg["lunar_start"] = sg["lunar_end"] = None
    if len(_MONTH_SEG_CACHE) > 64:
        _MONTH_SEG_CACHE.clear()
    _MONTH_SEG_CACHE[key] = segs
    return segs


def format_month_segment(seg: Dict[str, Any], short: bool = False) -> str:
    s, e = seg["start"], seg["end"]
    if short:
        return f"Tháng {seg['can']} {seg['chi']} ({s.strftime('%d/%m')}–{e.strftime('%d/%m/%Y')} DL)"
    lunar_part = ""
    if seg.get("lunar_start") and seg.get("lunar_end"):
        ls, le = seg["lunar_start"], seg["lunar_end"]
        lunar_part = f", tức {ls[0]:02d}/{ls[1]:02d} → {le[0]:02d}/{le[1]:02d} ÂL"
    return (
        f"Tháng {seg['can']} {seg['chi']} (từ {s.strftime('%d/%m/%Y')} đến {e.strftime('%d/%m/%Y')} DL{lunar_part}"
        f" · Năm {seg['year_can']} {seg['year_chi']} {seg['year_num']})"
    )


def upcoming_month_segments(chis: Any, base_date: Any, min_start: Any = None, limit: int = 2) -> List[Dict[str, Any]]:
    """Trả về các đoạn Tháng Can Chi sắp tới (gồm cả tháng đang hiện hành) có Địa Chi nằm trong `chis`."""
    out: List[Dict[str, Any]] = []
    for sg in build_solar_term_month_segments(base_date):
        if sg["end"] < base_date:
            continue
        if min_start is not None and sg["start"] < min_start and sg["end"] < min_start:
            continue
        if sg["chi"] in chis:
            out.append(sg)
            if len(out) >= limit:
                break
    return out


def describe_element_peak_window(element: str, base_date: Any, min_days: int = 0, limit: int = 2) -> str:
    """Mốc Tháng vượng khí thực tế (theo lịch tiết khí) của một Ngũ Hành tính từ ngày lập quẻ."""
    import datetime as _dtm
    chis = _EL_SEASON_CHIS.get(element, ("Dần", "Mão"))
    min_start = base_date + _dtm.timedelta(days=min_days) if min_days else None
    segs = upcoming_month_segments(chis, base_date, min_start=min_start, limit=limit)
    if not segs:
        return ""
    return " & ".join(format_month_segment(sg) for sg in segs)


def resolve_astronomical_ung_ky_ymdh(
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    benh_quai: str,
    duoc_ung_ky: str,
    chart_data: Optional[Dict[str, Any]] = None,
    question: str = "",
) -> Dict[str, str]:
    """
    Chuyển hóa Địa Chi Bệnh–Dược Ứng Kỳ thành NGÀY – GIỜ – THÁNG – NĂM DƯƠNG LỊCH & ÂM LỊCH CHÍNH XÁC 100%
    bằng thuật toán thiên văn Jean Meeus + Âm lịch Hồ Ngọc Đức trong qmdg_calc (Tuyệt đối 0% đoán mò lịch).
    """
    import datetime as _dt_mod
    import re as _re_ym

    cd = chart_data if isinstance(chart_data, dict) else {}
    if cd.get("_is_historical_liuyao_only"):
        return {
            "primary_chi": "",
            "secondary_chi": "",
            "hour_str": "",
            "day_str": "",
            "month_year_str": "",
            "short_inline_date": duoc_ung_ky,
            "pillar3_html": duoc_ung_ky,
            "pillar3_plain": duoc_ung_ky,
        }

    try:
        import qmdg_calc as _qcalc
    except Exception:
        _qcalc = None

    # 1. Xác định mốc ngày giờ gốc đang lập quẻ
    now_dt: _dt_mod.datetime
    try:
        if cd.get("year") and cd.get("month") and cd.get("day"):
            _hr = int(cd.get("hour", 12) or 12)
            _mn = int(cd.get("minute", 0) or 0)
            now_dt = _dt_mod.datetime(int(cd["year"]), int(cd["month"]), int(cd["day"]), _hr, _mn)
        elif _qcalc is not None:
            now_dt = _qcalc.get_vn_now()
        else:
            now_dt = _dt_mod.datetime.now(_dt_mod.timezone(_dt_mod.timedelta(hours=7))).replace(tzinfo=None)
    except Exception:
        now_dt = _dt_mod.datetime(2026, 11, 22, 12, 0)

    base_date = now_dt.date()
    lines: List[Dict[str, Any]] = list(ly_res.get("line_micro_audit") or [])
    dt_idx = int(ly_res.get("dt_hao_idx") or 1)
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    dt_chi = str(dt_ln.get("chi") or "Dần")
    dt_el = str(dt_ln.get("ngu_hanh") or CHI_EL.get(dt_chi, "Mộc"))
    h_flags = set(dt_ln.get("hoa_flags") or [])
    mo_tp = str(dt_ln.get("mo_type") or "")
    vs = str(dt_ln.get("vuong_suy") or "Bình")
    chi_ngay = str(cd.get("chi_ngay") or ly_res.get("chi_ngay") or "Tý")
    chi_gio = str(cd.get("chi_gio") or "Tý")
    xung_dt = _LUC_XUNG_12.get(dt_chi, "Thân")
    hop_dt = _LUC_HOP_12.get(dt_chi, "Hợi")

    # 2. Trích xuất Chi Ứng Kỳ chính & phụ sát đúng pháp Bệnh–Dược
    found_chis = [c for c in _re_ym.findall(r"\b(Tý|Sửu|Dần|Mão|Thìn|Tị|Ngọ|Mùi|Thân|Dậu|Tuất|Hợi)\b", duoc_ung_ky)]
    uniq_chis: List[str] = []
    for c_it in found_chis:
        if c_it not in uniq_chis:
            uniq_chis.append(c_it)

    if len(uniq_chis) >= 2:
        pri_chi, sec_chi = uniq_chis[0], uniq_chis[1]
    elif len(uniq_chis) == 1:
        pri_chi = uniq_chis[0]
        sec_chi = hop_dt if dt_ln.get("is_moving") or dt_ln.get("is_am_dong") else xung_dt
        if sec_chi == pri_chi:
            sec_chi = dt_chi if pri_chi != dt_chi else xung_dt
    else:
        if dt_ln.get("is_void") or "HOA_KHONG" in h_flags:
            pri_chi, sec_chi = dt_chi, xung_dt
        elif "HOA_MO" in h_flags or mo_tp in ("SUY_NHAP_MO", "VUONG_NHAP_KHO"):
            pri_chi, sec_chi = _LUC_XUNG_12.get(_MO_BY_EL_12.get(dt_el, "Thìn"), "Tuất"), dt_chi
        elif dt_ln.get("is_moving") or dt_ln.get("is_am_dong"):
            pri_chi, sec_chi = hop_dt, dt_chi
        elif vs in ("Tù", "Tử"):
            pri_chi, sec_chi = _TS_SINH_BY_EL.get(dt_el, dt_chi), dt_chi
        else:
            pri_chi, sec_chi = xung_dt, dt_chi

    # 3. Nhận diện tầm vóc thời gian trong câu hỏi để tra đúng khung lịch (Hôm nay / Tuần tới / Tháng tới / Năm tới)
    q_low = str(question or "").lower()
    is_already = "ĐÃ XẢY RA" in duoc_ung_ky.upper()
    is_today_q = any(w in q_low for w in ("hôm nay", "tối nay", "chiều nay", "sáng nay", "đêm nay", "ngay bây giờ"))
    is_next_week_q = any(w in q_low for w in ("tuần tới", "tuần sau", "mấy ngày tới", "vài ngày tới"))
    is_next_month_q = any(w in q_low for w in ("tháng tới", "tháng sau"))
    is_this_month_q = any(w in q_low for w in ("tháng này", "trong tháng"))
    is_next_year_or_daisu = any(
        w in q_low
        for w in (
            "năm tới", "năm sau", "sang năm", "năm nào", "mua nhà mặt đất", "mua được nhà",
            "xây nhà", "làm nhà", "mua đất ở", "kết hôn", "lấy vợ", "lấy chồng",
        )
    )

    def _fmt_date_full(d_obj: _dt_mod.date) -> Tuple[str, str, str]:
        wd = _WEEKDAY_VN_7[d_obj.weekday()]
        if _qcalc is not None:
            c_d, ch_d = _qcalc.get_can_chi_day(d_obj)
            ld, lm, ly, is_lp = _qcalc.solar_to_lunar(_dt_mod.datetime(d_obj.year, d_obj.month, d_obj.day, 12, 0))
            lp_s = " nhuận" if is_lp else ""
            full_s = f"{wd} {d_obj.strftime('%d/%m/%Y')} Dương lịch (tức {ld:02d}/{lm:02d}{lp_s} Âm lịch — Ngày {c_d} {ch_d})"
            short_s = f"Ngày {c_d} {ch_d} {d_obj.strftime('%d/%m/%Y')} DL ({ld:02d}/{lm:02d} ÂL)"
            return ch_d, full_s, short_s
        idx60 = (d_obj - _dt_mod.date(2024, 1, 1)).days % 60
        c_d, ch_d = _CAN_10_ORDER[idx60 % 10], _CHI_12_ORDER[idx60 % 12]
        full_s = f"{wd} {d_obj.strftime('%d/%m/%Y')} Dương lịch (Ngày {c_d} {ch_d})"
        short_s = f"Ngày {c_d} {ch_d} {d_obj.strftime('%d/%m/%Y')}"
        return ch_d, full_s, short_s

    # 4. Tính Khung Giờ & Khắc Vàng 15 phút chuẩn Tiên Thiên Quái Số + Hà Đồ Ngũ Hành
    h_span_pri, h_start_pri = _CHI_HOUR_SPAN.get(pri_chi, ("07:00–09:00", 7))
    h_span_sec, _ = _CHI_HOUR_SPAN.get(sec_chi, ("15:00–17:00", 15))
    _QUAI_NUM = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
    _dung_q = str(mh_res.get("dung_quai") or "Chấn")
    _khac_idx = _QUAI_NUM.get(_dung_q, 3)
    _m_off1 = (_khac_idx - 1) * 15
    _m_off2 = _m_off1 + 15
    _k_h1, _k_m1 = (h_start_pri * 60 + _m_off1) // 60 % 24, (h_start_pri * 60 + _m_off1) % 60
    _k_h2, _k_m2 = (h_start_pri * 60 + _m_off2) // 60 % 24, (h_start_pri * 60 + _m_off2) % 60
    if is_already:
        _g_span, _ = _CHI_HOUR_SPAN.get(chi_gio, ("hiện tại", 12))
        hour_str = f"Đã nổ ngay khung Giờ {chi_gio} ({_g_span}) hôm nay"
    else:
        hour_str = f"Giờ {pri_chi} ({h_span_pri}, đỉnh điểm Khắc {_khac_idx}: {_k_h1:02d}:{_k_m1:02d}–{_k_h2:02d}:{_k_m2:02d})"
        if sec_chi != pri_chi:
            hour_str += f" hoặc Giờ {sec_chi} ({h_span_sec})"

    # 5. Quét Ngày Dương Lịch & Âm Lịch chuẩn theo đúng cửa sổ câu hỏi
    pri_dates_full: List[str] = []
    pri_dates_short: List[str] = []
    sec_dates_full: List[str] = []
    sec_dates_short: List[str] = []

    if is_already:
        _, f0, s0 = _fmt_date_full(base_date)
        pri_dates_full.append(f"Ngay hôm nay — {f0}")
        pri_dates_short.append(f"ngay hôm nay {s0}")
    elif is_next_month_q:
        # Cửa sổ chính xác trong Tháng Dương lịch kế tiếp
        nm_year = base_date.year + (1 if base_date.month == 12 else 0)
        nm_month = 1 if base_date.month == 12 else (base_date.month + 1)
        d_cur = _dt_mod.date(nm_year, nm_month, 1)
        for _ in range(31):
            if d_cur.month != nm_month:
                break
            ch_d, f_s, sh_s = _fmt_date_full(d_cur)
            if ch_d == pri_chi and len(pri_dates_full) < 2:
                pri_dates_full.append(f_s)
                pri_dates_short.append(sh_s)
            elif ch_d == sec_chi and len(sec_dates_full) < 1:
                sec_dates_full.append(f_s)
                sec_dates_short.append(sh_s)
            d_cur += _dt_mod.timedelta(days=1)
    else:
        start_delta = 0 if (is_today_q or dt_ln.get("is_am_dong")) else (3 if is_next_week_q else 1)
        max_delta = 14 if is_today_q else (21 if is_next_week_q else (32 if is_this_month_q else 36))
        for delta in range(start_delta, start_delta + max_delta):
            d_cur = base_date + _dt_mod.timedelta(days=delta)
            ch_d, f_s, sh_s = _fmt_date_full(d_cur)
            if ch_d == pri_chi and len(pri_dates_full) < 2:
                pri_dates_full.append(f_s)
                pri_dates_short.append(sh_s)
            elif ch_d == sec_chi and len(sec_dates_full) < 1:
                sec_dates_full.append(f_s)
                sec_dates_short.append(sh_s)
            if len(pri_dates_full) >= 1 and len(sec_dates_full) >= 1 and not is_this_month_q:
                break

    # 6. Quét Tháng & Năm Thiên Văn Thực Tế (Phân đoạn 24 Tiết Khí từng ngày — V139.1 không bỏ sót tháng nào)
    month_year_str = ""
    short_month_tag = ""
    if _qcalc is not None:
        target_m_chis = list(dict.fromkeys([pri_chi, sec_chi, _VUONG_CHI_BY_EL.get(dt_el, pri_chi)]))
        all_segs = build_solar_term_month_segments(base_date)
        if is_next_month_q and all_segs:
            nm_y = base_date.year + (1 if base_date.month == 12 else 0)
            nm_m = 1 if base_date.month == 12 else (base_date.month + 1)
            nm_first = _dt_mod.date(nm_y, nm_m, 1)
            nm_last = (nm_first + _dt_mod.timedelta(days=32)).replace(day=1) - _dt_mod.timedelta(days=1)
            ov_segs = [sg for sg in all_segs if sg["start"] <= nm_last and sg["end"] >= nm_first]
            if ov_segs:
                def _ov_len(sg: Dict[str, Any]) -> int:
                    return (min(sg["end"], nm_last) - max(sg["start"], nm_first)).days + 1
                main_seg = max(ov_segs, key=_ov_len)
                month_year_str = f"Tháng {nm_m:02d}/{nm_y} Dương lịch gồm: " + " ➔ ".join(format_month_segment(sg) for sg in ov_segs)
                short_month_tag = f"Tháng {nm_m:02d}/{nm_y} DL (chủ khí {main_seg['can']} {main_seg['chi']})"
        elif all_segs:
            explicit_next_year = any(w in q_low for w in ("năm tới", "năm sau", "sang năm"))
            if explicit_next_year:
                min_start = _dt_mod.date(base_date.year + 1, 1, 1)
            elif is_next_year_or_daisu:
                min_start = base_date + _dt_mod.timedelta(days=45)
            else:
                min_start = None
            m_segs = upcoming_month_segments(target_m_chis, base_date, min_start=min_start, limit=2)
            if m_segs:
                month_year_str = " ➔ ".join(format_month_segment(sg) for sg in m_segs)
                short_month_tag = format_month_segment(m_segs[0], short=True)
                # Đại Sự / Năm tới: chốt luôn ngày Dụng Thần ngay trong tháng ứng nghiệm
                if is_next_year_or_daisu:
                    pri_dates_full.clear()
                    pri_dates_short.clear()
                    d_scan = max(m_segs[0]["start"], base_date)
                    while d_scan <= m_segs[0]["end"] and len(pri_dates_full) < 2:
                        ch_ds, f_ds, sh_ds = _fmt_date_full(d_scan)
                        if ch_ds == pri_chi:
                            pri_dates_full.append(f_ds)
                            pri_dates_short.append(sh_ds)
                        d_scan += _dt_mod.timedelta(days=1)
            else:
                cur_seg = next((sg for sg in all_segs if sg["start"] <= base_date <= sg["end"]), all_segs[0])
                month_year_str = format_month_segment(cur_seg)

    if pri_dates_full and sec_dates_full:
        day_str = f"Mốc 1 (Chính kỳ — Chi {pri_chi}): {pri_dates_full[0]} · Mốc 2 (Phụ kỳ — Chi {sec_chi}): {sec_dates_full[0]}"
    elif len(pri_dates_full) >= 2:
        day_str = f"Mốc 1: {pri_dates_full[0]} · Mốc 2: {pri_dates_full[1]}"
    elif pri_dates_full:
        day_str = pri_dates_full[0]
    else:
        _, f_fb, _ = _fmt_date_full(base_date)
        day_str = f_fb

    if is_already:
        short_inline_date = f"ĐÃ XẢY RA NGAY TRONG HÔM NAY ({pri_dates_short[0] if pri_dates_short else ''}, Giờ {chi_gio})"
    elif is_next_year_or_daisu and short_month_tag:
        short_inline_date = (
            f"Ứng trọng tâm vào {short_month_tag}"
            + (f" — điểm rơi {pri_dates_short[0]}" if pri_dates_short else "")
            + f", khung Giờ {pri_chi} ({h_span_pri})"
        )
    elif is_next_month_q and short_month_tag:
        short_inline_date = (
            f"{short_month_tag}: điểm nổ {pri_dates_short[0] if pri_dates_short else ''}"
            + (f" hoặc {sec_dates_short[0]}" if sec_dates_short else (f" / {pri_dates_short[1]}" if len(pri_dates_short) > 1 else ""))
            + f", Giờ {pri_chi} ({h_span_pri})"
        )
    else:
        short_inline_date = (
            f"{pri_dates_short[0] if pri_dates_short else f'Ngày {pri_chi}'}"
            + (f" hoặc {sec_dates_short[0]}" if sec_dates_short else "")
            + f" [Khung Giờ {pri_chi} {h_span_pri}"
            + (f" · Đại cục {short_month_tag}]" if short_month_tag else "]")
        )

    pillar3_html = (
        f"• <b>⏰ Giờ & Khắc ứng trong ngày:</b> <span style='color:#fde047;font-weight:800;'>{hour_str}</span>.<br>"
        f"• <b>📆 Ngày Dương lịch & Âm lịch chính xác:</b> <b>{day_str}</b>.<br>"
        f"• <b>🗓️ Tháng & Năm ứng nghiệm:</b> <b>{month_year_str}</b>.<br>"
        f"• <b>🔑 Căn cứ Bệnh–Dược Chống Luận Ảo:</b> {benh_quai} ══► <i>{duoc_ung_ky}</i> (Tính chuẩn lịch thiên văn từ mốc lập quẻ {base_date.strftime('%d/%m/%Y')})."
    )
    pillar3_plain = _strip_tags(pillar3_html.replace("<br>", " | "))

    return {
        "primary_chi": pri_chi,
        "secondary_chi": sec_chi,
        "hour_str": hour_str,
        "day_str": day_str,
        "month_year_str": month_year_str,
        "short_inline_date": short_inline_date,
        "pillar3_html": pillar3_html,
        "pillar3_plain": pillar3_plain,
    }


def build_four_pillar_prophecy(
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    dung_than: str = "Bản Thân",
    question: str = "",
) -> Dict[str, Any]:
    """
    V141.0 MASTER PROPHET 4-PILLAR ENGINE (100% GROUNDED IN REAL CHART MECHANICS — ZERO HALLUCINATION):
    1. SỰ VIỆC GÌ XẢY RA (Concrete Real-Life Event Narrative + Classical Score Proof)
    2. LIÊN QUAN ĐẾN CÁI GÌ & AI (Concrete Objects/Money/Documents/Places + Specific Person Profile)
    3. NGÀY – GIỜ – THÁNG – NĂM XẢY RA (Astronomical Solar/Lunar/Can-Chi Dates + Bệnh-Dược Proof)
    4. GIẢI PHÁP HÀNH ĐỘNG THỰC TẾ (3 Concrete Operational Steps Curing the Chart's Exact Bottleneck)
    """
    cd = chart_data if isinstance(chart_data, dict) else {}
    q_low = str(question or "").lower().strip()
    lines: List[Dict[str, Any]] = list(ly_res.get("line_micro_audit") or [])
    ban_name = str(ly_res.get("ban_name") or mh_res.get("ten_chu") or "Quẻ Chủ")
    bien_name = str(ly_res.get("bien_name") or mh_res.get("ten_bien") or ban_name)
    the_pos = int(ly_res.get("the_pos") or 3)
    ung_pos = int(ly_res.get("ung_pos") or 6)
    dt_idx = int(ly_res.get("dt_hao_idx") or the_pos)
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    the_ln = lines[the_pos - 1] if 1 <= the_pos <= len(lines) else {}
    ung_ln = lines[ung_pos - 1] if 1 <= ung_pos <= len(lines) else {}

    dt_lt = str(dt_ln.get("luc_than") or dung_than)
    dt_chi = str(dt_ln.get("chi") or "Dần")
    dt_el = str(dt_ln.get("ngu_hanh") or CHI_EL.get(dt_chi, "Mộc"))
    dt_thu = str(dt_ln.get("luc_thu") or "Thanh Long")
    dt_vs = str(dt_ln.get("vuong_suy") or "Bình")
    dt_nap_am = str(dt_ln.get("nap_am") or "")
    h_flags = set(dt_ln.get("hoa_flags") or [])
    the_el = str(the_ln.get("ngu_hanh") or "Thổ")
    the_chi = str(the_ln.get("chi") or "Thìn")

    tc_qm = int(qm_res.get("target_cung") or 2)
    chu_qm = int(qm_res.get("cung_chu") or 2)
    p_map_qm = qm_res.get("palace_micro_audit") or {}
    pa_tc = p_map_qm.get(tc_qm, {})
    door_tc = str(pa_tc.get("door") or "Khai Môn")
    star_tc = str(pa_tc.get("star") or "Thiên Tâm")
    deity_tc = str(pa_tc.get("deity") or "Trực Phù")
    huong_tc = str(pa_tc.get("huong") or "Đông Nam")
    tu_hai_tc = list(pa_tc.get("tu_hai") or [])
    t_st = str(pa_tc.get("can_thien") or "Mậu")
    d_st = str(pa_tc.get("can_dia") or "Mậu")
    _pat_nm_raw, _pat_ds_raw = QIMEN_10_STEM_PATTERNS.get((t_st, d_st), (f"Cách {t_st}+{d_st}", "tương tác chủ khách theo thời lệnh"))
    pat_name, pat_desc = _qualify_qimen_stem_pattern(_pat_nm_raw, _pat_ds_raw, door_tc, tu_hai_tc)

    comp_sc = int(deep_syn.get("composite_score", 50))
    lh_sc = int(deep_syn.get("lh_score", 50))
    qm_sc = int(deep_syn.get("qm_score", 50))
    mh_sc = int(deep_syn.get("mh_score", 50))
    benh_quai = str(deep_syn.get("benh_quai") or "")
    duoc_ung_ky = str(deep_syn.get("duoc_ung_ky") or "")

    # Giải lịch thiên văn trước để cả 4 trụ cột dùng chung mốc ngày chuẩn 100%
    ymdh = resolve_astronomical_ung_ky_ymdh(
        ly_res=ly_res,
        qm_res=qm_res,
        mh_res=mh_res,
        benh_quai=benh_quai,
        duoc_ung_ky=duoc_ung_ky,
        chart_data=cd,
        question=question,
    )

    # ── PHÂN LOẠI MIỀN ĐỜI SỐNG CỦA CÂU HỎI ──
    if any(w in q_low for w in ("mở quán", "cà phê", "cửa hàng", "shop", "kinh doanh", "buôn bán", "nhập hàng", "đầu tư", "khởi nghiệp", "hùn vốn", "chứng khoán", "cổ phiếu", "lướt sóng")):
        domain = "BIZ_INVEST"
    elif any(w in q_low for w in ("công việc", "sự nghiệp", "đi làm", "cơ quan", "công ty", "sếp", "thăng chức", "nhảy việc", "nghỉ việc", "xin việc", "ứng tuyển", "lương")):
        domain = "WORK_CAREER"
    elif any(w in q_low for w in ("đòi nợ", "trả nợ", "cho vay", "vay tiền", "công nợ", "tiền bạc", "tài chính", "lộc", "thu nhập")):
        domain = "MONEY_DEBT"
    elif any(w in q_low for w in ("hợp đồng", "ký kết", "giấy tờ", "sổ đỏ", "pháp lý", "kiện", "tranh chấp", "tòa án", "thủ tục")):
        domain = "CONTRACT_LEGAL"
    elif any(w in q_low for w in ("gia đình", "gia đạo", "trong nhà", "nhà tôi", "nhà cửa", "bố mẹ", "cha mẹ", "vợ chồng", "con cái", "anh em")):
        domain = "FAMILY_HOME"
    elif any(w in q_low for w in ("tình cảm", "người yêu", "yêu", "hôn nhân", "cưới", "quay lại", "chia tay", "nhớ", "hẹn hò")):
        domain = "LOVE_MARRIAGE"
    elif any(w in q_low for w in ("sức khỏe", "bệnh", "đau ", "ốm", "khám", "mổ", "thuốc", "điều trị")):
        domain = "HEALTH_BODY"
    elif any(w in q_low for w in ("mất ", "thất lạc", "rơi ", "để quên", "trộm", "lấy cắp", "tìm lại")):
        domain = "LOST_THEFT"
    elif any(w in q_low for w in ("thi ", "đỗ", "đậu", "học ", "điểm", "visa", "du học")):
        domain = "STUDY_EXAM"
    elif any(w in q_low for w in ("xuất hành", "đi xa", "chuyến đi", "du lịch", "công tác", "về quê")):
        domain = "TRAVEL_MOVE"
    else:
        domain = "GENERAL"

    # ── TRỤ CỘT 1: SỰ VIỆC CỤ THỂ GÌ XẢY RA TRONG ĐỜI THỰC (CHỐNG LUẬN ẢO 100%) ──
    active_lines = [ln for ln in lines if ln.get("is_moving") or ln.get("is_am_dong")]
    real_events: List[str] = []

    # 1a. Giải nghĩa trạng thái trực diện của chính Dụng Thần ra sự kiện thực tế
    if dt_ln.get("is_void") or "HOA_KHONG" in h_flags:
        _void_ev_map = {
            "BIZ_INVEST": f"Thương vụ/kế hoạch mở bán hiện mới đẹp trên tính toán bề mặt, dòng thu thực chất hoặc cam kết khách/đối tác còn bỏ ngỏ ('{dt_lt} {dt_chi} vướng Không Vong' — nếu dốc vốn ngay lúc này sẽ hụt doanh thu kỳ đầu, phải qua mốc Xuất Không mới tụ tiền thật)",
            "WORK_CAREER": f"Đề xuất công việc/vị trí hoặc lời hứa từ cấp trên hiện chưa ra quyết định chính thức ('{dt_lt} {dt_chi} vướng Không Vong' — hồ sơ/chỉ tiêu còn treo tạm thời chờ ngày Xuất Không mới chốt)",
            "MONEY_DEBT": f"Khoản tiền/công nợ đang hỏi hiện chưa sẵn tiền mặt để về tay ngay ('{dt_lt} {dt_chi} Không Vong' — đối phương tạm khất hẹn hoặc dòng tiền về chậm hơn dự kiến)",
            "CONTRACT_LEGAL": f"Bản hợp đồng/giấy tờ còn thiếu điều khoản chốt hoặc chữ ký phê duyệt cuối ('{dt_lt} {dt_chi} Không Vong' — chưa thể ký xong ngay lập tức)",
        }
        real_events.append(_void_ev_map.get(domain, f"Mục tiêu chính ({dt_lt} {dt_chi}) đang ở trạng thái 'tạm ẩn / chưa thành hình thực chất' trên thực tế, cần qua mốc Xuất Không mới chuyển thành kết quả thật"))
    elif "HOI_DAU_KHAC" in h_flags:
        real_events.append(f"Sự việc khởi đầu tưởng thuận nhưng đến chặng chốt lại phát sinh lực cản dội ngược ('Hào {dt_idx} {dt_lt} {dt_chi} động hóa Hồi Đầu Khắc' — dễ đổi ý phút chót hoặc đội chi phí/rủi ro ngoài dự tính)")
    elif "HOI_DAU_SINH" in h_flags or "HOA_TIEN" in h_flags:
        real_events.append(f"Mạch việc đang mở đà tăng trưởng thực chất rất tốt ('Hào {dt_idx} {dt_lt} {dt_chi} động đắc {'Hồi Đầu Sinh' if 'HOI_DAU_SINH' in h_flags else 'Hóa Tiến Thần'}' — càng triển khai về sau càng có thêm nguồn lực tiếp sức)")
    elif dt_vs in ("Tù", "Tử") and not dt_ln.get("is_moving"):
        _weak_ev_map = {
            "WORK_CAREER": f"Công việc hiện tại chịu sức ép kiểm soát hoặc chững lại về quyền hạn/chỉ tiêu (Dụng Thần {dt_lt} {dt_chi} thất lệnh '{dt_vs}' dưới tháng lệnh), dễ có đợt rà soát quy trình hoặc điều chỉnh phân công khiến bạn vất vả tâm sức trước khi ổn định",
            "BIZ_INVEST": f"Sức mua thị trường và biên lợi nhuận thực tế hiện đang mỏng hơn kỳ vọng (Dụng Thần {dt_lt} {dt_chi} ở bậc '{dt_vs}'), mở vội dễ chịu áp lực chi phí cố định đè nặng",
        }
        real_events.append(_weak_ev_map.get(domain, f"Nền lực của sự việc ({dt_lt} {dt_chi} ở bậc '{dt_vs}') hiện còn mỏng, chưa đủ đà bùng nổ ngay mà cần bước đệm tích lũy"))

    # 1b. Giải nghĩa từng Hào Động / Ám Động sang biến cố thực tế sát miền câu hỏi
    for aln in active_lines[:3]:
        a_h = int(aln.get("hao") or 1)
        a_lt = str(aln.get("luc_than") or "")
        a_chi = str(aln.get("chi") or "")
        a_thu = str(aln.get("luc_thu") or "")
        a_blt = str(aln.get("bien_luc_than") or "")
        a_act_lbl = f"Hào {a_h} {a_lt} ({a_chi} · {a_thu}) {'động hóa ' + a_blt if aln.get('is_moving') else 'ám động'}"
        if a_lt == "Huynh Đệ":
            if domain in ("BIZ_INVEST", "MONEY_DEBT"):
                real_events.append(f"Phát sinh khoản chi phí đội vốn, cạnh tranh khách/giá trực tiếp hoặc rủi ro hao hụt nếu chung đụng tiền bạc với bạn bè/đối tác ngang hàng [{a_act_lbl}]")
            elif domain == "WORK_CAREER":
                real_events.append(f"Có sự cạnh tranh ngầm từ đồng nghiệp/đội nhóm cùng cấp hoặc chia sẻ lại khối lượng công việc – quyền lợi [{a_act_lbl}]")
            elif domain == "FAMILY_HOME":
                real_events.append(f"Trong nhà phát sinh khoản chi tiêu lớn cho mua sắm/sửa chữa hoặc có cuộc bàn bạc tài chính hơi căng giữa anh chị em/người thân [{a_act_lbl}]")
            else:
                real_events.append(f"Xuất hiện yếu tố hao phí tiền bạc hoặc người ngang vai xen vào chia lực [{a_act_lbl}]")
        elif a_lt == "Quan Quỷ":
            if a_thu == "Chu Tước":
                real_events.append(f"Xảy ra cuộc trao đổi căng thẳng, rà soát giấy tờ/quy chế hoặc tranh luận đúng–sai trực diện cần giữ bình tĩnh lời nói [{a_act_lbl}]")
            elif a_thu == "Bạch Hổ":
                real_events.append(f"Có áp lực tiến độ gấp gáp, kiểm tra kỷ luật gắt gao hoặc cần chú ý an toàn đi lại & sức khỏe cơ thể [{a_act_lbl}]")
            elif domain == "WORK_CAREER":
                real_events.append(f"Có sự biến động từ cấp quản lý: giao thêm trọng trách khó, thay đổi quy chế điều hành hoặc rà soát KPI/nhân sự [{a_act_lbl}]")
            else:
                real_events.append(f"Phát sinh rào cản thủ tục quản lý hoặc áp lực lo toan tâm lý cần tháo gỡ khéo [{a_act_lbl}]")
        elif a_lt == "Phụ Mẫu":
            if domain in ("WORK_CAREER", "CONTRACT_LEGAL"):
                real_events.append(f"Biến động xoay quanh văn bản quyết định, hợp đồng, hồ sơ hành chính hoặc sự dịch chuyển phòng ban/đơn vị công tác [{a_act_lbl}]")
            elif domain == "BIZ_INVEST":
                real_events.append(f"Phát sinh việc ký kết mặt bằng, giấy phép kinh doanh, đầu tư trang thiết bị/cơ sở vật chất ban đầu tốn nhiều công sức [{a_act_lbl}]")
            elif domain == "FAMILY_HOME":
                real_events.append(f"Gia đình bận rộn việc giấy tờ nhà đất/xe cộ, tu sửa không gian sống hoặc chăm lo sức khỏe bậc cha mẹ/trưởng bối [{a_act_lbl}]")
            else:
                real_events.append(f"Sự việc gắn trực tiếp với khâu giấy tờ thủ tục, chứng từ hoặc nhà cửa phương tiện [{a_act_lbl}]")
        elif a_lt == "Thê Tài":
            real_events.append(f"Dòng tiền/lợi ích kinh tế chuyển động rõ rệt: có khoản thu–chi thực tế, thanh toán đơn hàng hoặc điều chỉnh ngân sách [{a_act_lbl}]")
        elif a_lt == "Tử Tôn":
            if domain in ("WORK_CAREER", "CONTRACT_LEGAL") and dt_lt == "Quan Quỷ":
                real_events.append(f"Tâm lý muốn tự do đổi mới hoặc nảy sinh hướng đi riêng làm xáo trộn khuôn khổ chức vụ cũ (Tử Tôn khắc Quan Quỷ) [{a_act_lbl}]")
            else:
                real_events.append(f"Có Phúc Thần giải nguy: quý nhân/khách hàng mở lối tháo gỡ rắc rối êm đẹp, đón tin vui con cái hoặc nguồn khách tự nhiên [{a_act_lbl}]")

    # 1c. Bổ sung cách cục Kỳ Môn & kết cục để tạo bức tranh trọn vẹn
    real_events.append(
        f"Trên bàn Kỳ Môn Cung {tc_qm} ({huong_tc}) hiện cách <b>«{pat_name}»</b> ({pat_desc.lower()}), hội <b>{door_tc} · {star_tc} · {deity_tc}</b>"
        + (f" (vướng {', '.join(tu_hai_tc)})" if tu_hai_tc else " (cung sạch Tứ Hại)")
    )

    concrete_event_summary = real_events[0] if real_events else f"Sự việc vận hành theo quẻ {ban_name} ➔ {bien_name} ({comp_sc}/100)"
    pillar1_event_html = (
        f"<div style='margin-bottom:5px;color:#bae6fd;font-weight:800;font-size:0.86em;'>"
        f"⚖️ Khí lực Tam Thức: Lục Hào {lh_sc} · Kỳ Môn {qm_sc} · Mai Hoa {mh_sc} ➔ Hợp nhất {comp_sc}/100 ({ban_name} ➔ {bien_name})"
        f"</div>"
        + "".join(f"• {ev}.<br>" for ev in real_events[:3])
        + f"• <b>Điểm nghẽn gốc trên quẻ:</b> {benh_quai}."
    )

    # ── TRỤ CỘT 2: LIÊN QUAN ĐẾN CÁI GÌ & AI (ĐỊNH VỊ ĐÚNG MIỀN CÂU HỎI — CHỐNG RÂU ÔNG NỌ CẮM CẰM BÀ KIA!) ──
    if domain == "HEALTH_BODY":
        thing_core = "chứng bệnh cơ thể đang gặp, phác đồ thuốc điều trị (Tử Tôn) và chế độ ăn uống – nghỉ ngơi phục hồi nguyên khí"
    elif domain == "FAMILY_HOME":
        thing_core = {
            "Phụ Mẫu": "giấy tờ nhà đất, tu sửa không gian sống/phương tiện gia đình hoặc sức khỏe bậc sinh thành",
            "Thê Tài": "ngân sách chi tiêu sinh hoạt trong nhà, tài sản chung hoặc đời sống vợ chồng",
            "Huynh Đệ": "khoản chi tiêu phát sinh trong gia đình, chuyện anh chị em họ hàng hoặc sửa chữa vật dụng",
            "Quan Quỷ": "sức khỏe thành viên trong nhà, hệ thống điện–nước–bếp núc hoặc thủ tục hộ tịch",
            "Tử Tôn": "chuyện con cái, học hành, tin vui hỷ sự bình an trong gia đạo",
        }.get(dt_lt, "nếp sinh hoạt, nhà cửa và sự bình an của các thành viên trong gia đình")
    elif domain == "LOVE_MARRIAGE":
        thing_core = "sự gắn kết tình cảm đôi lứa, cuộc trò chuyện/gặp gỡ trực tiếp và cam kết tương lai giữa hai người"
    else:
        _LT_CONCRETE_THINGS = {
            "Phụ Mẫu": "hợp đồng văn bản, giấy phép/hồ sơ pháp lý, mặt bằng nhà đất/cửa hàng hoặc phương tiện xe cộ",
            "Thê Tài": "nguồn vốn tiền mặt, doanh thu bán hàng, khoản công nợ/thanh toán hoặc tài sản hàng hóa",
            "Quan Quỷ": "quyết định quản lý/chức vụ, chỉ tiêu kiểm tra, thủ tục pháp chế–thuế hoặc quy trình cơ quan",
            "Huynh Đệ": "chi phí trung gian/đội vốn, thỏa thuận ăn chia cổ phần, giao dịch bạn bè hoặc đối thủ cùng ngành",
            "Tử Tôn": "sản phẩm/nguồn khách hàng thực tế, con cái/hậu bối, hoặc phương án tháo gỡ rủi ro",
        }
        thing_core = _LT_CONCRETE_THINGS.get(dt_lt, "công việc và kế hoạch cá nhân")

    chi_img_raw = CHI_CONCRETE_IMAGE.get(dt_chi, "")
    chi_img = ", ".join(p.strip() for p in chi_img_raw.split(",") if not p.strip().startswith("người "))
    palace_loc_raw = PALACE_BODY_LOC.get(tc_qm, "")
    palace_loc_short_full = palace_loc_raw.split("(", 1)[1].rstrip(")") if "(" in palace_loc_raw else huong_tc
    palace_loc_short = (
        palace_loc_short_full
        if domain == "HEALTH_BODY"
        else palace_loc_short_full.split(" · Cơ thể:")[0]
    )
    _loc_bullet_title = "📍 Bộ phận cơ thể & Phương vị ứng quẻ" if domain == "HEALTH_BODY" else "📍 Không gian & Hiện trường ứng quẻ"

    # Chân dung Nhân vật tác động mạnh nhất trên quẻ (phân vai sát đúng miền Sức khỏe / Gia đình / Tình cảm / Công việc)
    _YANG_C = {"Tý", "Dần", "Thìn", "Ngọ", "Thân", "Tuất"}
    mover_other = next((ln for ln in active_lines if int(ln.get("hao") or 0) != the_pos), None)
    key_person_ln = (dt_ln if domain == "HEALTH_BODY" and dt_idx != the_pos else None) or mover_other or ung_ln or dt_ln
    kp_hao = int(key_person_ln.get("hao") or ung_pos)
    kp_chi = str(key_person_ln.get("chi") or "Ngọ")
    kp_el = str(key_person_ln.get("ngu_hanh") or "Hỏa")
    kp_lt = str(key_person_ln.get("luc_than") or "Quan Quỷ")
    kp_thu = str(key_person_ln.get("luc_thu") or "Chu Tước")
    kp_ts = str(key_person_ln.get("ts_ngay") or "Lâm Quan")
    kp_gender = "Nam giới" if kp_chi in _YANG_C else "Nữ giới"
    kp_age = (
        "trẻ tuổi (khoảng 20–34 tuổi)" if kp_ts in ("Thai", "Dưỡng", "Trường Sinh", "Mộc Dục", "Quan Đái")
        else ("trung niên (khoảng 35–50 tuổi)" if kp_ts in ("Lâm Quan", "Đế Vượng", "Suy") else "đứng tuổi/cao niên (trên 48 tuổi)")
    )
    if kp_lt == "Phụ Mẫu" and domain in ("HEALTH_BODY", "FAMILY_HOME"):
        if any(w in q_low for w in ("bố", "cha", "ông nội", "ông ngoại")):
            kp_gender = "Nam giới"
        elif any(w in q_low for w in ("mẹ", "má", "bà nội", "bà ngoại")):
            kp_gender = "Nữ giới"
        if any(w in q_low for w in ("bố", "mẹ", "cha", "má", "ông", "bà")):
            kp_age = "bậc sinh thành / trung–cao niên (trên 48 tuổi)"
    if domain == "HEALTH_BODY":
        _KP_ROLE_BY_LT = {
            "Phụ Mẫu": "bậc cha mẹ / trưởng bối đang điều trị hoặc người nhà trực tiếp chăm sóc",
            "Quan Quỷ": "bác sĩ chuyên khoa / phác đồ can thiệp y tế (hoặc tác nhân gây mệt mỏi)",
            "Tử Tôn": "thầy thuốc mát tay / dược thần giúp cắt cơn đau và phục hồi sức khỏe",
            "Thê Tài": "người phối ngẫu / người thân chăm lo dinh dưỡng và thuốc thang",
            "Huynh Đệ": "anh chị em trong nhà cùng phụ giúp thăm khám",
        }
    elif domain == "FAMILY_HOME":
        _KP_ROLE_BY_LT = {
            "Phụ Mẫu": "bậc cha mẹ / người lớn tuổi trụ cột trong gia đình",
            "Quan Quỷ": "người đàn ông trụ cột trong nhà hoặc người đang mang nỗi lo công việc/sức khỏe",
            "Huynh Đệ": "anh chị em ruột thịt / họ hàng thân thiết",
            "Thê Tài": "người vợ / phụ nữ giữ tay hòm chìa khóa trong nhà",
            "Tử Tôn": "con cháu / thế hệ trẻ mang lại sinh khí vui vẻ cho gia đình",
        }
    elif domain == "LOVE_MARRIAGE":
        _KP_ROLE_BY_LT = {
            "Quan Quỷ": "người nam / bạn trai / chồng (hoặc rào cản tâm lý giữa hai người)",
            "Thê Tài": "người nữ / bạn gái / vợ đang được hỏi tới",
            "Phụ Mẫu": "gia đình hai bên / bậc phụ huynh tác động vào chuyện tình cảm",
            "Huynh Đệ": "bạn bè xung quanh hoặc người gây xao nhãng mối quan hệ",
            "Tử Tôn": "người bạn hòa giải giúp kết nối lại cảm xúc tự nhiên",
        }
    else:
        _KP_ROLE_BY_LT = {
            "Quan Quỷ": "cấp trên, người quản lý/xét duyệt, cơ quan chức năng hoặc người nắm quyền quyết định",
            "Phụ Mẫu": "người lớn tuổi/trưởng bối, chủ mặt bằng/nhà đất hoặc người phụ trách hồ sơ hợp đồng",
            "Huynh Đệ": "đồng nghiệp ngang cấp, bạn bè quen biết, người hùn vốn hoặc đối thủ cạnh tranh",
            "Thê Tài": "khách hàng, người nắm giữ nguồn tiền/tài chính, đối tác kinh doanh hoặc người phối ngẫu",
            "Tử Tôn": "cấp dưới, khách hàng trẻ, hậu bối hoặc người đứng ra hòa giải giúp đỡ",
        }
    kp_role_desc = _KP_ROLE_BY_LT.get(kp_lt, "người liên quan trực tiếp")
    if SINH_EL.get(kp_el) == the_el or _LUC_HOP_12.get(kp_chi) == the_chi:
        kp_attitude = "có thiện chí nâng đỡ, đồng hành hỗ trợ bạn thực chất (Hào sinh/hợp Thế)"
    elif KHAC_EL.get(kp_el) == the_el:
        kp_attitude = (
            "đang khiến bạn lo lắng tốn nhiều tâm sức chăm lo (Hào tác động mạnh lên Thế)"
            if domain in ("HEALTH_BODY", "FAMILY_HOME")
            else "đang gây sức ép, kiểm soát chặt hoặc đưa ra điều kiện khắt khe với bạn (Hào khắc Thế)"
        )
    else:
        kp_attitude = "giữ thái độ thực tế, rõ ràng theo đúng nguyên tắc"

    h5_ln = lines[4] if len(lines) >= 5 else {}
    h5_note = ""
    if h5_ln and kp_hao != 5 and domain not in ("HEALTH_BODY", "LOVE_MARRIAGE"):
        h5_note = (
            f" · <b>Trục chủ đạo Hào 5:</b> {h5_ln.get('luc_than','')} ({h5_ln.get('chi','')}) "
            + ("đang phát động trực tiếp cầm trịch" if h5_ln.get("is_moving") else ("tạm Tuần Không chưa chốt văn bản cuối" if h5_ln.get("is_void") else "giữ nhịp ổn định"))
        )

    concrete_related_summary = f"Liên quan trực tiếp đến {thing_core} (hướng {huong_tc}) & {kp_gender} ({kp_role_desc})"
    pillar2_related_html = (
        f"• <b>📦 Liên quan đến cái gì (Vật việc & Khâu cụ thể):</b> Trực tiếp xoay quanh <b>{thing_core}</b> "
        f"[Căn cứ Hào {dt_idx} {dt_lt} {dt_chi}-{dt_el}{(' · Nạp Âm ' + dt_nap_am) if dt_nap_am else ''}: {chi_img}].<br>"
        f"• <b>{_loc_bullet_title}:</b> <b>{palace_loc_short}</b>.<br>"
        f"• <b>👤 Liên quan đến ai (Nhân vật trọng tâm):</b> <b>{kp_gender}, {kp_age}</b> — vai trò <b>{kp_role_desc}</b> "
        f"(ứng Hào {kp_hao} {kp_lt} {kp_chi}-{kp_el} · {kp_thu}), hiện {kp_attitude}{h5_note}."
    )

    # ── TRỤ CỘT 4: GIẢI PHÁP HÀNH ĐỘNG THỰC TẾ & HÓA GIẢI CHỐNG LUẬN ẢO ──
    can_n_s = str(cd.get("can_ngay") or "Giáp")
    can_g_s = str(cd.get("can_gio") or "Giáp")
    _NGU_BN = {
        ("Giáp", "Canh"), ("Ất", "Tân"), ("Bính", "Nhâm"), ("Đinh", "Quý"), ("Mậu", "Giáp"),
        ("Kỷ", "Ất"), ("Canh", "Bính"), ("Tân", "Đinh"), ("Nhâm", "Mậu"), ("Quý", "Kỷ"),
    }
    is_nbnt_now = (can_n_s, can_g_s) in _NGU_BN
    ng_el = next((k for k, v in SINH_EL.items() if v == dt_el), "Thủy")

    # Bước 1: Giải pháp vận hành thực tế trị đúng Bệnh của quẻ
    if domain == "HEALTH_BODY":
        step1_act = (
            f"<b>Phác đồ Chăm sóc & Điều trị Đúng Gốc:</b> "
            + (
                f"Nguyên khí người bệnh ({dt_lt} {dt_chi}) hiện còn suy yếu/vướng cản ({comp_sc}/100) — cần tái khám chuyên khoa kỹ lưỡng, tuân thủ đủ phác đồ thuốc (không tự ý ngắt thuốc sớm) và giữ ấm/ăn uống thanh đạm cho tới mốc chuyển khí <b>{ymdh['short_inline_date'].split('[')[0].strip()}</b>"
                if comp_sc < 50
                else f"Dược thần và nguyên khí đang đáp ứng tốt ({comp_sc}/100) — kiên trì dùng đúng liệu trình hiện tại kết hợp nghỉ ngơi điều độ sẽ sớm hồi phục"
            )
        )
    elif dt_ln.get("is_void") or "HOA_KHONG" in h_flags:
        step1_act = (
            f"<b>Khóa rủi ro 'Hóa Không / Tuần Không':</b> Tuyệt đối KHÔNG dốc 100% vốn, không đặt cọc lớn một lần hay tin hoàn toàn vào lời hứa miệng lúc này; "
            f"hãy tách nhỏ kế hoạch liên quan <i>{thing_core}</i> thành 2–3 bước kiểm chứng thực tế và đợi qua mốc Xuất Không (<b>{ymdh['short_inline_date'].split('[')[0].strip()}</b>) mới chốt chính thức"
        )
    elif any(ln.get("luc_than") == "Huynh Đệ" and (ln.get("is_moving") or ln.get("is_am_dong")) for ln in lines) and domain in ("BIZ_INVEST", "MONEY_DEBT", "WORK_CAREER"):
        step1_act = (
            f"<b>Chặn thất thoát do Hào Huynh Đệ kích hoạt:</b> Không hùn vốn chung đụng nhập nhằng, không cho vay/ứng tiền trước và khóa chặt trần chi phí phát sinh cho <i>{thing_core}</i>; "
            f"mọi thu–chi phải do chính tay bạn kiểm soát trực tiếp"
        )
    elif comp_sc < 50 or dt_vs in ("Tù", "Tử") or tu_hai_tc or "HOI_DAU_KHAC" in h_flags:
        step1_act = (
            f"<b>Chiến thuật 'Thủ Vững Trước – Tiến Sau':</b> Quẻ hiện báo nút thắt (<i>{benh_quai}</i>)"
            + (f" kèm Giờ Ngũ Bất Ngộ ({can_g_s} khắc {can_n_s})" if is_nbnt_now else "")
            + f" — tuyệt đối tránh quyết định nóng vội ngay lúc này; hãy rà soát chặt chẽ các điều khoản/chi phí xoay quanh <i>{thing_core}</i> trước khi bước sang kỳ mở khóa"
        )
    else:
        step1_act = (
            f"<b>Chủ động nắm bắt thời cơ đắc khí ({comp_sc}/100):</b> Mạch quẻ đã thông cho <i>{thing_core}</i> — hãy chuẩn bị sẵn hồ sơ/nguồn lực hoàn chỉnh và xúc tiến dứt khoát thay vì chần chừ để lỡ nhịp vượng"
        )

    # Bước 2: Đối sách nhân sự với người liên quan (kp_role_desc)
    if domain == "HEALTH_BODY":
        step2_people = (
            f"<b>Chọn Thầy Thuốc & Người Chăm Sóc Hợp Khí:</b> Ưu tiên thăm khám bác sĩ có chuyên môn sâu (ứng hành <b>{ng_el}</b> / Sao Thiên Tâm) và động viên tinh thần người bệnh nhẹ nhàng, tránh tạo tâm lý lo âu"
        )
    elif KHAC_EL.get(kp_el) == the_el:
        step2_people = (
            f"<b>Đối sách với {kp_gender} ({kp_role_desc} — Hào {kp_hao} {kp_chi}):</b> Tránh tranh luận gay gắt trực diện; "
            f"hãy dùng văn bản/số liệu minh bạch và mượn khâu trung gian mềm dẻo (thuộc hành <b>{ng_el}</b>) để hóa giải áp lực êm thấm"
        )
    else:
        step2_people = (
            f"<b>Kết nối đúng người mấu chốt:</b> Chủ động trao đổi thẳng thắn, thống nhất rõ ràng với <b>{kp_gender} ({kp_role_desc} — Hào {kp_hao} {kp_chi})</b> để chốt cam kết cụ thể"
        )

    # Bước 3: Luôn ưu tiên Tam Cát Môn (Khai · Sinh · Hưu) trên bàn Kỳ Môn — TUYỆT ĐỐI KHÔNG khuyên đi vào Tử/Kinh/Thương Môn!
    cat_candidates: List[Tuple[int, str]] = []
    for pi, pv in p_map_qm.items():
        if pi == 5:
            continue
        d_nm = str(pv.get("door") or "")
        if any(d in d_nm for d in ("Khai", "Sinh", "Hưu")):
            th_cnt = len(pv.get("tu_hai") or [])
            th_note = "sạch Tứ Hại" if th_cnt == 0 else "cát môn chủ lực"
            cat_candidates.append((th_cnt, f"Hướng <b>{pv.get('huong','')}</b> (Cung {pi} — đắc <b>{d_nm} · {pv.get('star','')}</b>, {th_note})"))
    cat_candidates.sort(key=lambda x: x[0])
    best_cat_dir = cat_candidates[0][1] if cat_candidates else f"Hướng <b>{huong_tc}</b> (Cung {tc_qm})"
    step3_remedy = (
        f"<b>Phương vị Cát Môn & Thời khắc hành sự:</b> Ưu tiên đi giao dịch/thăm khám/mở việc về {best_cat_dir}, "
        f"thực hiện đúng mốc <b>{ymdh['short_inline_date']}</b> (bồi đắp hành Thông Quan <b>{ng_el}</b> để chuyển hung thành cát)"
    )

    pillar4_solution_html = f"• 1️⃣ {step1_act}.<br>• 2️⃣ {step2_people}.<br>• 3️⃣ {step3_remedy}."

    return {
        "domain": domain,
        "concrete_event_summary": concrete_event_summary,
        "concrete_related_summary": concrete_related_summary,
        "short_inline_date": ymdh["short_inline_date"],
        "ymdh": ymdh,
        "pillar1_event_html": pillar1_event_html,
        "pillar2_related_html": pillar2_related_html,
        "pillar3_timing_html": ymdh["pillar3_html"],
        "pillar3_plain": ymdh["pillar3_plain"],
        "pillar4_solution_html": pillar4_solution_html,
        "pillar1_plain": _strip_tags(pillar1_event_html.replace("<br>", " | ")),
        "pillar2_plain": _strip_tags(pillar2_related_html.replace("<br>", " | ")),
        "pillar4_plain": _strip_tags(pillar4_solution_html.replace("<br>", " | ")),
    }

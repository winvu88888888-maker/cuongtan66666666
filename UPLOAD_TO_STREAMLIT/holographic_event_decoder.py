# -*- coding: utf-8 -*-
"""
holographic_event_decoder.py — V135.0
BỘ ĐỘNG CƠ ĐỌC VỊ TOÀN TỨC 12 TẦNG CHI TIẾT SỰ KIỆN CỦA BẬC ĐẠI TIÊN TRI (ZERO-OMISSION HOLOGRAPHIC DECODER)

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

    portrait_items: List[str] = []
    if dt_ln:
        portrait_items.append(
            f"<b>Hào Đích Dụng Thần — {HAO_VI_ROLE.get(dt_idx, f'Hào {dt_idx}')}:</b> "
            f"<b>{dt_ln.get('luc_than','')} ({dt_ln.get('can_chi_full','')} · Nạp Âm: {dt_nap_am})</b>, phối <b>{dt_thu}</b> ({LUC_THU_ROLE_COLOR.get(dt_thu,'')})"
            + (f", hội Thần Sát: <b>{', '.join(dt_ss)}</b>." if dt_ss else ".")
        )
        portrait_items.append(
            f"<b>Khí chất & Vật tượng ({dt_el} – Chi {dt_chi}):</b> {NGU_HANH_TEMPERAMENT.get(dt_el, '')}. Hiện trường/chi tiết ứng với <b>Chi {dt_chi}</b>: {CHI_CONCRETE_IMAGE.get(dt_chi, '')}."
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
        pat_name, pat_desc = QIMEN_10_STEM_PATTERNS.get(
            (t_st, d_st),
            (f"Cách {t_st} gia {d_st}", f"Thiên bàn {t_st} lâm Địa bàn {d_st}, xét tương tác Tinh–Môn để điều tiết chủ khách"),
        )
        star_q = str(pa_q.get("star") or "Thiên Tâm")
        star_vs = _qimen_star_season_state(star_q, nguyet_el)
        portrait_items.append(
            f"<b>Thập Can Khắc Ứng {lbl_p} (Cung {p_idx_q} — {t_st} + {d_st}):</b> Đắc cách <b>«{pat_name}»</b> — {pat_desc}. "
            f"Sao <b>{star_q}</b> ở thế <b>{star_vs}</b>, hội <b>{pa_q.get('door','')} · {pa_q.get('deity','')}</b>; định vị không gian/cơ thể: {PALACE_BODY_LOC.get(p_idx_q, '')}."
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
    timing_detail = (
        f"• <b>Bệnh – Dược Mở Khóa:</b> {deep_syn.get('benh_quai', '')} ══► <b style='color:#fde047;'>{deep_syn.get('duoc_ung_ky', '')}</b>.<br>"
        f"• <b>Nhịp độ Không–Thời Gian Kỳ Môn:</b> {speed_tag}"
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
        f'<span>🔮 ĐỌC VỊ CHI TIẾT SỰ KIỆN TOÀN TỨC TỪ 100% YẾU TỐ QUẺ (V135.0 — KHÔNG BỎ SÓT DẤU HIỆU NÀO)</span>'
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
        f'<div style="font-weight:800;color:#fde68a;margin-bottom:3px;">⏱️ 5. Khoanh Vùng Không Gian – Thời Điểm Ứng Nghiệm Đa Tầng</div>'
        f'<div style="line-height:1.48;">{timing_detail}</div></div>'
        f'<div style="padding:8px 11px;background:rgba(30,41,59,0.75);border-radius:9px;border-left:3.5px solid #f472b6;">'
        f'<div style="font-weight:800;color:#f9a8d4;margin-bottom:3px;">⚡ 6. Ấn Chứng Cận Sự Thực Tế Quanh Bạn (Đối Chứng Linh Ứng)</div>'
        f'{_li_join(near_verifications)}</div>'
        f'</div></div>'
    )

    clean_prompt_lines = [
        "=== HỒ SƠ ĐỌC VỊ CHI TIẾT SỰ KIỆN TOÀN TỨC 12 TẦNG (V135.0 — BẮT BUỘC DÙNG ĐỂ TIÊN ĐOÁN CHI TIẾT NHƯ ĐẠI TIÊN TRI, KHÔNG BỎ SÓT 1 YẾU TỐ NÀO) ===",
        "1. [DẤU VẾT QUÁ KHỨ & LAI Ý]: " + " | ".join(_strip_tags(x) for x in past_traces),
        "2. [HIỆN TRẠNG · GIAN HÀO TRUNG GIAN · QUÂN VỊ HÀO 5 · PHI–PHỤC · NỘI/NGOẠI BÀN · ÁM CAN · TỨ HẠI · ÁM ĐỘNG]: " + " | ".join(_strip_tags(x) for x in present_undercurrents),
        "3. [CHÂN DUNG NGƯỜI/VẬT · NẠP ÂM · 12 TRƯỜNG SINH · THẬP CAN KHẮC ỨNG · 64 SONG QUÁI]: " + " | ".join(_strip_tags(x) for x in portrait_items),
        "4. [KỊCH BẢN DIỄN BIẾN TỪNG BƯỚC · HÀO ĐỘNG CHU DỊCH · LẬT CUNG 4 TRẠM · TỨ KHÓA & TAM TRUYỀN ĐẠI LỤC NHÂM]: " + " | ".join(_strip_tags(x) for x in future_steps),
        "5. [KHÔNG GIAN & THỜI ĐIỂM ỨNG KỲ CANH CÁCH]: " + _strip_tags(timing_detail),
        "6. [ẤN CHỨNG CẬN SỰ QUANH NGƯỜI HỎI]: " + " | ".join(_strip_tags(x) for x in near_verifications),
    ]

    return {
        "past_traces": past_traces,
        "present_undercurrents": present_undercurrents,
        "portrait_items": portrait_items,
        "future_steps": future_steps,
        "timing_detail": timing_detail,
        "near_verifications": near_verifications,
        "noi_ngoai_desc": noi_ngoai_desc,
        "canh_cach_notes": canh_cach_notes,
        "holographic_html": holographic_html,
        "holographic_prompt_text": "\n".join(clean_prompt_lines),
    }


def _strip_tags(s: str) -> str:
    import re as _re_st
    return _re_st.sub(r"<[^>]+>", "", str(s or "")).strip()

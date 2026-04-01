# -*- coding: utf-8 -*-
"""
KINH DỊCH 64 QUẺ + THIẾT BẢN 60 NẠP ÂM + MAI HOA THỂ DỤNG
Knowledge Base V9.0 Phase 2
Nguồn: wikipedia Kinh Dịch, simkinhdich.com, tuvilyso.org, bocdich.com
"""

# ======================================================================
# 1. KINH DỊCH 64 QUẺ — Thoán Từ + Đại Tượng + Ý nghĩa + Lời khuyên
# ======================================================================
KINH_DICH_64 = {
    # === 8 QUẺ THUẦN (Quẻ 1-8 theo thứ tự truyền thống) ===
    "Thuần Càn": {
        "thuong": "Càn", "ha": "Càn", "thu_tu": 1,
        "thoan": "Nguyên Hanh Lợi Trinh — Khởi đầu hanh thông, lợi ích chính đáng",
        "dai_tuong": "Trời đi mạnh, quân tử tự cường không nghỉ",
        "y_nghia": "Sức mạnh sáng tạo, cương kiện, lãnh đạo, cha",
        "loi_khuyen": "Hành động mạnh mẽ, kiên trì, tự lực cánh sinh",
        "cat_hung": "ĐẠI CÁT"
    },
    "Thuần Khôn": {
        "thuong": "Khôn", "ha": "Khôn", "thu_tu": 2,
        "thoan": "Nguyên Hanh, lợi tẫn mã trinh — Đất rộng thuận theo trời",
        "dai_tuong": "Đất thuận chở, quân tử dày đức chở vật",
        "y_nghia": "Nhu thuận, bao dung, nuôi dưỡng, mẹ, đất",
        "loi_khuyen": "Nhẫn nại, thuận theo tự nhiên, không tranh đấu",
        "cat_hung": "CÁT"
    },
    "Thủy Lôi Truân": {
        "thuong": "Khảm", "ha": "Chấn", "thu_tu": 3,
        "thoan": "Nguyên Hanh Lợi Trinh, chớ vội dùng — Khó khăn ban đầu",
        "dai_tuong": "Mây sấm giao nhau, quân tử kinh luân sắp đặt",
        "y_nghia": "Khó khăn khởi đầu, cần kiên nhẫn vượt qua gian nan",
        "loi_khuyen": "Kiên nhẫn chờ đợi, chuẩn bị kỹ, đừng vội vàng",
        "cat_hung": "BÌNH"
    },
    "Sơn Thủy Mông": {
        "thuong": "Cấn", "ha": "Khảm", "thu_tu": 4,
        "thoan": "Hanh, phi ngã cầu đồng mông — Mông muội cầu ta, không phải ta cầu",
        "dai_tuong": "Dưới núi có suối, quân tử nuôi đức hạnh",
        "y_nghia": "Mông muội, cần học hỏi, giáo dục, khai sáng",
        "loi_khuyen": "Khiêm tốn học hỏi, tìm thầy, kiên nhẫn giáo dục",
        "cat_hung": "BÌNH"
    },
    "Thủy Thiên Nhu": {
        "thuong": "Khảm", "ha": "Càn", "thu_tu": 5,
        "thoan": "Hữu phu, quang hanh trinh cát — Có lòng thành, sáng sủa hanh thông",
        "dai_tuong": "Mây lên trời, quân tử ẩm thực yến lạc",
        "y_nghia": "Chờ đợi, nuôi dưỡng, kiên nhẫn chờ thời cơ",
        "loi_khuyen": "Chờ đợi đúng lúc, không nóng vội, chuẩn bị sẵn sàng",
        "cat_hung": "CÁT"
    },
    "Thiên Thủy Tụng": {
        "thuong": "Càn", "ha": "Khảm", "thu_tu": 6,
        "thoan": "Hữu phu truất dịch — Có lòng thành nhưng bị ngăn trở",
        "dai_tuong": "Trời nước trái chiều, quân tử mưu sự từ đầu",
        "y_nghia": "Tranh chấp, kiện tụng, bất hòa, cần hòa giải",
        "loi_khuyen": "Tránh tranh chấp, tìm người phân xử, đừng cố chấp",
        "cat_hung": "HUNG"
    },
    "Địa Thủy Sư": {
        "thuong": "Khôn", "ha": "Khảm", "thu_tu": 7,
        "thoan": "Trinh, trượng nhân cát — Chính đáng, người lớn tuổi cát",
        "dai_tuong": "Đất chứa nước, quân tử dung dân nuôi chúng",
        "y_nghia": "Quân đội, tổ chức, kỷ luật, cần người lãnh đạo",
        "loi_khuyen": "Cần kỷ luật, tổ chức tốt, tìm người có kinh nghiệm",
        "cat_hung": "BÌNH"
    },
    "Thủy Địa Tỷ": {
        "thuong": "Khảm", "ha": "Khôn", "thu_tu": 8,
        "thoan": "Cát, nguyên phệ nguyên vĩnh trinh — Tốt lành, gần gũi thân mật",
        "dai_tuong": "Nước trên đất, quân tử thân cận chư hầu",
        "y_nghia": "Thân cận, hợp tác, liên minh, đoàn kết",
        "loi_khuyen": "Đoàn kết, tìm đồng minh, hợp tác chân thành",
        "cat_hung": "CÁT"
    },
    # === QUẺ 9-16 ===
    "Phong Thiên Tiểu Súc": {
        "thuong": "Tốn", "ha": "Càn", "thu_tu": 9,
        "thoan": "Hanh, mật vân bất vũ — Mây dày chưa mưa, tích lũy nhỏ",
        "dai_tuong": "Gió trên trời, quân tử văn đức",
        "y_nghia": "Tích lũy nhỏ, chưa đủ lực, cần kiên nhẫn thêm",
        "loi_khuyen": "Tích lũy từ từ, đừng cố làm lớn khi chưa đủ sức",
        "cat_hung": "CÁT"
    },
    "Thiên Trạch Lý": {
        "thuong": "Càn", "ha": "Đoài", "thu_tu": 10,
        "thoan": "Lý hổ vĩ, bất điệt nhân — Giẫm đuôi hổ mà không bị cắn",
        "dai_tuong": "Trời trên đầm, quân tử phân biệt trên dưới",
        "y_nghia": "Lễ nghi, cẩn trọng, đi đúng đường, phân biệt",
        "loi_khuyen": "Cẩn thận từng bước, giữ lễ, biết trên biết dưới",
        "cat_hung": "CÁT"
    },
    "Địa Thiên Thái": {
        "thuong": "Khôn", "ha": "Càn", "thu_tu": 11,
        "thoan": "Tiểu vãng đại lai, cát hanh — Nhỏ đi lớn đến, cát hanh thông",
        "dai_tuong": "Trời đất giao hòa, quân tử tài thành thiên địa đạo",
        "y_nghia": "Thái bình, hanh thông, âm dương hòa hợp, vạn sự tốt",
        "loi_khuyen": "Tận dụng thời kỳ thuận lợi, mở rộng, hợp tác",
        "cat_hung": "ĐẠI CÁT"
    },
    "Thiên Địa Bĩ": {
        "thuong": "Càn", "ha": "Khôn", "thu_tu": 12,
        "thoan": "Bĩ chi phỉ nhân — Bế tắc, trời đất không giao",
        "dai_tuong": "Trời đất không giao, quân tử kiệm đức tránh nạn",
        "y_nghia": "Bế tắc, trì trệ, âm dương cách biệt, vạn sự khó",
        "loi_khuyen": "Kiên nhẫn chờ đợi, tiết kiệm, tránh mạo hiểm",
        "cat_hung": "HUNG"
    },
    "Thiên Hỏa Đồng Nhân": {
        "thuong": "Càn", "ha": "Ly", "thu_tu": 13,
        "thoan": "Đồng Nhân vu dã, hanh — Cùng người ngoài đồng, hanh thông",
        "dai_tuong": "Trời với lửa, quân tử loại tộc biện vật",
        "y_nghia": "Đồng tâm hiệp lực, hợp tác, cộng đồng, hòa hợp",
        "loi_khuyen": "Đoàn kết, hợp tác rộng rãi, công bằng với mọi người",
        "cat_hung": "CÁT"
    },
    "Hỏa Thiên Đại Hữu": {
        "thuong": "Ly", "ha": "Càn", "thu_tu": 14,
        "thoan": "Nguyên hanh — Có lớn, rất hanh thông",
        "dai_tuong": "Lửa trên trời, quân tử ngăn ác dương thiện thuận mệnh trời",
        "y_nghia": "Giàu có, thịnh vượng, sở hữu lớn, vinh quang",
        "loi_khuyen": "Khiêm tốn trong giàu có, dùng tài sản làm việc thiện",
        "cat_hung": "ĐẠI CÁT"
    },
    "Địa Sơn Khiêm": {
        "thuong": "Khôn", "ha": "Cấn", "thu_tu": 15,
        "thoan": "Hanh, quân tử hữu chung — Khiêm tốn hanh thông trọn vẹn",
        "dai_tuong": "Núi trong đất, quân tử bớt nhiều thêm ít, cân bằng",
        "y_nghia": "Khiêm tốn, nhún nhường, đức hạnh cao quý",
        "loi_khuyen": "Giữ khiêm tốn trong mọi hoàn cảnh, được lòng người",
        "cat_hung": "CÁT"
    },
    "Lôi Địa Dự": {
        "thuong": "Chấn", "ha": "Khôn", "thu_tu": 16,
        "thoan": "Lợi kiến hầu hành sư — Sấm vang đất, vui vẻ, khởi sự",
        "dai_tuong": "Sấm ra từ đất, tiên vương tác nhạc sùng đức",
        "y_nghia": "Vui vẻ, hân hoan, thuận lợi khởi sự, lạc quan",
        "loi_khuyen": "Hành động khi hứng khởi, nhưng đừng quá phóng túng",
        "cat_hung": "CÁT"
    },
    # === QUẺ 17-24 ===
    "Trạch Lôi Tùy": {
        "thuong": "Đoài", "ha": "Chấn", "thu_tu": 17,
        "thoan": "Nguyên hanh lợi trinh — Đi theo, thuận theo tự nhiên",
        "dai_tuong": "Đầm có sấm, quân tử hướng tối nhập nghỉ",
        "y_nghia": "Thuận theo, thích ứng, đi theo xu hướng",
        "loi_khuyen": "Thuận theo hoàn cảnh, linh hoạt thích ứng",
        "cat_hung": "CÁT"
    },
    "Sơn Phong Cổ": {
        "thuong": "Cấn", "ha": "Tốn", "thu_tu": 18,
        "thoan": "Nguyên hanh, lợi thiệp đại xuyên — Sửa chữa sai lầm của cha",
        "dai_tuong": "Dưới núi có gió, quân tử chấn dân dục đức",
        "y_nghia": "Mục nát, cần sửa chữa, cải cách, khắc phục lỗi cũ",
        "loi_khuyen": "Sửa chữa sai lầm cũ, cải cách mạnh mẽ, đừng để mục nát",
        "cat_hung": "BÌNH"
    },
    "Địa Trạch Lâm": {
        "thuong": "Khôn", "ha": "Đoài", "thu_tu": 19,
        "thoan": "Nguyên hanh lợi trinh, chí vu bát nguyệt hữu hung — Đến gần, tiếp cận",
        "dai_tuong": "Đất trên đầm, quân tử giáo dục vô cùng",
        "y_nghia": "Tiếp cận, giám sát, lãnh đạo tiếp cận dân chúng",
        "loi_khuyen": "Chủ động tiếp cận, nhưng biết rằng thịnh sẽ suy",
        "cat_hung": "CÁT"
    },
    "Phong Địa Quan": {
        "thuong": "Tốn", "ha": "Khôn", "thu_tu": 20,
        "thoan": "Quán nhi bất tiến, hữu phu ngung nhược — Quan sát từ trên cao",
        "dai_tuong": "Gió trên đất, quân tử tuần phương quan dân",
        "y_nghia": "Quan sát, chiêm nghiệm, nhìn nhận toàn cảnh",
        "loi_khuyen": "Quan sát kỹ trước khi hành động, suy ngẫm",
        "cat_hung": "BÌNH"
    },
    "Hỏa Lôi Phệ Hạp": {
        "thuong": "Ly", "ha": "Chấn", "thu_tu": 21,
        "thoan": "Hanh, lợi dụng ngục — Cắn đứt vật cản, xử phạt",
        "dai_tuong": "Sấm sét cùng lửa, tiên vương minh phạt sắc pháp",
        "y_nghia": "Phán xét, xử phạt, loại bỏ chướng ngại",
        "loi_khuyen": "Giải quyết dứt khoát, công bằng, loại bỏ trở ngại",
        "cat_hung": "CÁT"
    },
    "Sơn Hỏa Bí": {
        "thuong": "Cấn", "ha": "Ly", "thu_tu": 22,
        "thoan": "Hanh, tiểu lợi hữu du vãng — Trang sức, văn vẻ đẹp đẽ",
        "dai_tuong": "Dưới núi có lửa, quân tử minh thứ triết ngục",
        "y_nghia": "Trang sức, vẻ đẹp bề ngoài, văn hóa, nghệ thuật",
        "loi_khuyen": "Chú trọng nội dung hơn hình thức, đẹp phải có chất",
        "cat_hung": "CÁT"
    },
    "Sơn Địa Bác": {
        "thuong": "Cấn", "ha": "Khôn", "thu_tu": 23,
        "thoan": "Bất lợi hữu du vãng — Bóc lột, sụp đổ, tan rã",
        "dai_tuong": "Núi trên đất mỏng, quân tử dày người dưới an nhà",
        "y_nghia": "Sụp đổ, tan rã, hao mòn, tiểu nhân thắng thế",
        "loi_khuyen": "Kiên nhẫn chịu đựng, không hành động, chờ vận mới",
        "cat_hung": "HUNG"
    },
    "Địa Lôi Phục": {
        "thuong": "Khôn", "ha": "Chấn", "thu_tu": 24,
        "thoan": "Hanh, xuất nhập vô tật — Trở lại, hồi phục, chu kỳ mới",
        "dai_tuong": "Sấm trong đất, tiên vương chí nhật bế quan",
        "y_nghia": "Trở lại, hồi phục, khởi đầu mới sau suy thoái",
        "loi_khuyen": "Bắt đầu lại từ nhỏ, kiên nhẫn phục hồi",
        "cat_hung": "CÁT"
    },
    # === QUẺ 25-32 ===
    "Thiên Lôi Vô Vọng": {
        "thuong": "Càn", "ha": "Chấn", "thu_tu": 25,
        "thoan": "Nguyên hanh lợi trinh — Không sai lầm, thuận theo tự nhiên",
        "dai_tuong": "Dưới trời có sấm, vạn vật thuận tự nhiên",
        "y_nghia": "Chân thành, không giả dối, thuận theo đạo trời",
        "loi_khuyen": "Sống chân thành, đừng toan tính, thuận theo tự nhiên",
        "cat_hung": "CÁT"
    },
    "Sơn Thiên Đại Súc": {
        "thuong": "Cấn", "ha": "Càn", "thu_tu": 26,
        "thoan": "Lợi trinh, bất gia thực cát — Tích lũy lớn, nuôi hiền tài",
        "dai_tuong": "Trời trong núi, quân tử đa thức tiền ngôn vãng hạnh",
        "y_nghia": "Tích lũy lớn, nuôi dưỡng tài năng, kiềm chế sức mạnh",
        "loi_khuyen": "Tích lũy tri thức và tài lực, nuôi chí lớn",
        "cat_hung": "ĐẠI CÁT"
    },
    "Sơn Lôi Di": {
        "thuong": "Cấn", "ha": "Chấn", "thu_tu": 27,
        "thoan": "Trinh cát, quan di tự cầu khẩu thực — Nuôi dưỡng, ăn uống",
        "dai_tuong": "Dưới núi có sấm, quân tử thận ngôn ngữ tiết ẩm thực",
        "y_nghia": "Nuôi dưỡng thân tâm, ăn uống, lời nói cẩn thận",
        "loi_khuyen": "Cẩn thận lời nói và ăn uống, nuôi dưỡng đúng cách",
        "cat_hung": "BÌNH"
    },
    "Trạch Phong Đại Quá": {
        "thuong": "Đoài", "ha": "Tốn", "thu_tu": 28,
        "thoan": "Đống nạo, lợi hữu du vãng — Cột kèo yếu, quá tải",
        "dai_tuong": "Đầm ngập cây, quân tử độc lập bất cụ",
        "y_nghia": "Quá tải, vượt giới hạn, áp lực quá lớn",
        "loi_khuyen": "Hành động táo bạo khi cần, nhưng cẩn thận quá tải",
        "cat_hung": "HUNG"
    },
    "Thuần Khảm": {
        "thuong": "Khảm", "ha": "Khảm", "thu_tu": 29,
        "thoan": "Tập Khảm hữu phu, duy tâm hanh — Nước chảy liên tiếp, hiểm",
        "dai_tuong": "Nước chảy mãi, quân tử dùng đức hạnh hằng ngày",
        "y_nghia": "Nguy hiểm chồng chất, cần giữ tâm chính, vượt khó",
        "loi_khuyen": "Kiên trì vượt khó, giữ lòng thành, đừng sợ hãi",
        "cat_hung": "HUNG"
    },
    "Thuần Ly": {
        "thuong": "Ly", "ha": "Ly", "thu_tu": 30,
        "thoan": "Lợi trinh, hanh — Bám vào cái đúng, sáng suốt",
        "dai_tuong": "Sáng lặp lại, đại nhân nối sáng thiên hạ",
        "y_nghia": "Sáng suốt, phụ thuộc, bám vào chính đạo",
        "loi_khuyen": "Sáng suốt, minh bạch, bám vào điều đúng đắn",
        "cat_hung": "CÁT"
    },
    "Trạch Sơn Hàm": {
        "thuong": "Đoài", "ha": "Cấn", "thu_tu": 31,
        "thoan": "Hanh lợi trinh, thủ nữ cát — Cảm ứng, hôn nhân tốt",
        "dai_tuong": "Trên núi có đầm, quân tử hư tâm thụ nhân",
        "y_nghia": "Cảm ứng, thu hút, tình cảm, hôn nhân",
        "loi_khuyen": "Mở lòng đón nhận, chân thành trong tình cảm",
        "cat_hung": "CÁT"
    },
    "Lôi Phong Hằng": {
        "thuong": "Chấn", "ha": "Tốn", "thu_tu": 32,
        "thoan": "Hanh vô cữu, lợi trinh — Bền bỉ lâu dài, kiên định",
        "dai_tuong": "Sấm gió cùng nhau, quân tử lập bất dịch phương",
        "y_nghia": "Bền bỉ, kiên định, hằng tâm, lâu dài",
        "loi_khuyen": "Giữ vững lập trường, kiên trì không thay đổi",
        "cat_hung": "CÁT"
    },
    # === QUẺ 33-40 ===
    "Thiên Sơn Độn": {
        "thuong": "Càn", "ha": "Cấn", "thu_tu": 33,
        "thoan": "Hanh, tiểu lợi trinh — Rút lui đúng lúc",
        "dai_tuong": "Dưới trời có núi, quân tử viễn tiểu nhân",
        "y_nghia": "Rút lui, ẩn mình, tránh tiểu nhân, biết lùi",
        "loi_khuyen": "Biết lùi đúng lúc, tránh xa kẻ xấu, bảo toàn",
        "cat_hung": "BÌNH"
    },
    "Lôi Thiên Đại Tráng": {
        "thuong": "Chấn", "ha": "Càn", "thu_tu": 34,
        "thoan": "Lợi trinh — Sức mạnh lớn, cần chính đáng",
        "dai_tuong": "Sấm trên trời, quân tử phi lễ bất lý",
        "y_nghia": "Sức mạnh lớn, hùng tráng, cần dùng đúng đắn",
        "loi_khuyen": "Dùng sức mạnh đúng đắn, đừng lạm dụng quyền lực",
        "cat_hung": "CÁT"
    },
    "Hỏa Địa Tấn": {
        "thuong": "Ly", "ha": "Khôn", "thu_tu": 35,
        "thoan": "Khang hầu dụng tích mã phồn thứ — Tiến lên, thăng tiến",
        "dai_tuong": "Mặt trời mọc trên đất, quân tử tự chiếu minh đức",
        "y_nghia": "Tiến bộ, thăng tiến, sáng sủa, phát triển",
        "loi_khuyen": "Tiến lên với đức sáng, phát triển nhanh chóng",
        "cat_hung": "CÁT"
    },
    "Địa Hỏa Minh Di": {
        "thuong": "Khôn", "ha": "Ly", "thu_tu": 36,
        "thoan": "Lợi gian trinh — Ánh sáng bị che, ẩn nhẫn",
        "dai_tuong": "Sáng vào trong đất, quân tử dụng hối mà minh",
        "y_nghia": "Bị áp chế, tài năng bị che giấu, ẩn nhẫn",
        "loi_khuyen": "Ẩn nhẫn chờ thời, giấu tài năng, tránh kẻ xấu",
        "cat_hung": "HUNG"
    },
    "Phong Hỏa Gia Nhân": {
        "thuong": "Tốn", "ha": "Ly", "thu_tu": 37,
        "thoan": "Lợi nữ trinh — Gia đình hòa thuận, đàn bà chính",
        "dai_tuong": "Gió từ lửa, quân tử ngôn hữu vật hành hữu hằng",
        "y_nghia": "Gia đình, nội trợ, hòa thuận trong nhà",
        "loi_khuyen": "Chú trọng gia đình, lời nói phải có thực, hành vi nhất quán",
        "cat_hung": "CÁT"
    },
    "Hỏa Trạch Khuê": {
        "thuong": "Ly", "ha": "Đoài", "thu_tu": 38,
        "thoan": "Tiểu sự cát — Đối lập, mâu thuẫn, chỉ làm việc nhỏ",
        "dai_tuong": "Lửa trên đầm, quân tử đồng mà dị",
        "y_nghia": "Mâu thuẫn, bất đồng, đối lập nhưng bổ sung",
        "loi_khuyen": "Hòa giải mâu thuẫn, tìm điểm chung trong khác biệt",
        "cat_hung": "BÌNH"
    },
    "Thủy Sơn Kiển": {
        "thuong": "Khảm", "ha": "Cấn", "thu_tu": 39,
        "thoan": "Lợi Tây Nam, bất lợi Đông Bắc — Khó khăn, hiểm trở",
        "dai_tuong": "Trên núi có nước, quân tử phản thân tu đức",
        "y_nghia": "Khó khăn, trở ngại, cần tìm đường tránh",
        "loi_khuyen": "Tránh khó khăn, đi đường vòng, tu sửa bản thân",
        "cat_hung": "HUNG"
    },
    "Lôi Thủy Giải": {
        "thuong": "Chấn", "ha": "Khảm", "thu_tu": 40,
        "thoan": "Lợi Tây Nam, vô sở vãng — Thoát khó, giải thoát",
        "dai_tuong": "Sấm mưa nổi, quân tử xá lỗi giảm tội",
        "y_nghia": "Giải thoát, thoát khỏi khó khăn, tha thứ",
        "loi_khuyen": "Tha thứ, giải quyết nhanh, đừng chần chừ sau khi thoát khó",
        "cat_hung": "CÁT"
    },
    # === QUẺ 41-48 ===
    "Sơn Trạch Tổn": {
        "thuong": "Cấn", "ha": "Đoài", "thu_tu": 41,
        "thoan": "Hữu phu, nguyên cát — Giảm bớt có lòng thành là tốt",
        "dai_tuong": "Dưới núi có đầm, quân tử trừng phẫn trật dục",
        "y_nghia": "Giảm bớt, hy sinh, tiết kiệm, tổn trên lợi dưới",
        "loi_khuyen": "Chấp nhận hy sinh ngắn hạn để được lợi lâu dài",
        "cat_hung": "BÌNH"
    },
    "Phong Lôi Ích": {
        "thuong": "Tốn", "ha": "Chấn", "thu_tu": 42,
        "thoan": "Lợi hữu du vãng, lợi thiệp đại xuyên — Tăng thêm, thu được lợi",
        "dai_tuong": "Gió sấm cùng nhau, quân tử thấy thiện liền làm",
        "y_nghia": "Tăng thêm, lợi ích, phát triển, bề trên giúp bề dưới",
        "loi_khuyen": "Hành động khi có cơ hội, làm việc thiện, giúp đỡ người",
        "cat_hung": "ĐẠI CÁT"
    },
    "Trạch Thiên Quải": {
        "thuong": "Đoài", "ha": "Càn", "thu_tu": 43,
        "thoan": "Dương vu vương đình — Quyết đoán, loại bỏ kẻ xấu",
        "dai_tuong": "Đầm trên trời, quân tử thí lộc cập hạ",
        "y_nghia": "Quyết đoán, đoạn tuyệt, loại bỏ cái xấu",
        "loi_khuyen": "Quyết đoán loại bỏ xấu, nhưng cẩn thận phản ứng ngược",
        "cat_hung": "BÌNH"
    },
    "Thiên Phong Cấu": {
        "thuong": "Càn", "ha": "Tốn", "thu_tu": 44,
        "thoan": "Nữ tráng, vật dụng thủ nữ — Gặp gỡ bất ngờ, đàn bà mạnh",
        "dai_tuong": "Dưới trời có gió, hậu thi mệnh cáo tứ phương",
        "y_nghia": "Gặp gỡ bất ngờ, hội ngộ, cần cẩn thận",
        "loi_khuyen": "Cẩn thận với gặp gỡ bất ngờ, đừng quá tin",
        "cat_hung": "BÌNH"
    },
    "Trạch Địa Tụy": {
        "thuong": "Đoài", "ha": "Khôn", "thu_tu": 45,
        "thoan": "Hanh, vương cách hữu miếu — Tụ họp, tập trung",
        "dai_tuong": "Đầm trên đất, quân tử trừ nhung khí giới phòng bất trắc",
        "y_nghia": "Tụ họp, tập hợp lực lượng, đoàn kết",
        "loi_khuyen": "Tập hợp lực lượng, chuẩn bị phòng ngừa bất trắc",
        "cat_hung": "CÁT"
    },
    "Địa Phong Thăng": {
        "thuong": "Khôn", "ha": "Tốn", "thu_tu": 46,
        "thoan": "Nguyên hanh, dụng kiến đại nhân — Đi lên, thăng tiến",
        "dai_tuong": "Cây mọc trong đất, quân tử thuận đức tích tiểu thành cao",
        "y_nghia": "Thăng tiến, đi lên, phát triển từ từ vững chắc",
        "loi_khuyen": "Phát triển từ từ, vững bước đi lên, tìm quý nhân",
        "cat_hung": "ĐẠI CÁT"
    },
    "Trạch Thủy Khốn": {
        "thuong": "Đoài", "ha": "Khảm", "thu_tu": 47,
        "thoan": "Hanh, trinh đại nhân cát — Khốn cùng nhưng giữ chí",
        "dai_tuong": "Đầm không có nước, quân tử trí mệnh toại chí",
        "y_nghia": "Khốn cùng, bế tắc, thiếu thốn, cần giữ chí",
        "loi_khuyen": "Giữ vững ý chí trong khó khăn, chờ cơ hội",
        "cat_hung": "HUNG"
    },
    "Thủy Phong Tỉnh": {
        "thuong": "Khảm", "ha": "Tốn", "thu_tu": 48,
        "thoan": "Cải ấp bất cải tỉnh — Giếng nước không thay đổi, nguồn gốc",
        "dai_tuong": "Trên cây có nước, quân tử lao dân khuyến tướng",
        "y_nghia": "Nguồn gốc, cội nguồn, nuôi dưỡng không ngừng",
        "loi_khuyen": "Giữ gốc, nuôi dưỡng nguồn lực, phục vụ mọi người",
        "cat_hung": "CÁT"
    },
    # === QUẺ 49-56 ===
    "Trạch Hỏa Cách": {
        "thuong": "Đoài", "ha": "Ly", "thu_tu": 49,
        "thoan": "Tị nhật nãi phu — Đến ngày đổi mới mới tin",
        "dai_tuong": "Đầm có lửa, quân tử trị lịch minh thời",
        "y_nghia": "Cách mạng, thay đổi, đổi mới, biến cách",
        "loi_khuyen": "Thay đổi khi đúng thời điểm, cải cách mạnh mẽ",
        "cat_hung": "CÁT"
    },
    "Hỏa Phong Đỉnh": {
        "thuong": "Ly", "ha": "Tốn", "thu_tu": 50,
        "thoan": "Nguyên cát, hanh — Vạc nấu ăn, nuôi hiền",
        "dai_tuong": "Trên cây có lửa, quân tử chính vị ngưng mệnh",
        "y_nghia": "Nuôi dưỡng, chuyển hóa, nấu nướng, văn minh",
        "loi_khuyen": "Chuyển hóa tài nguyên, nuôi dưỡng nhân tài",
        "cat_hung": "ĐẠI CÁT"
    },
    "Thuần Chấn": {
        "thuong": "Chấn", "ha": "Chấn", "thu_tu": 51,
        "thoan": "Hanh, sấm đến khiếp khiếp — Sấm lặp gây sợ rồi vui",
        "dai_tuong": "Sấm nổi liên tiếp, quân tử sợ mà tu sửa",
        "y_nghia": "Chấn động, sợ hãi rồi tỉnh ngộ, thay đổi",
        "loi_khuyen": "Cẩn trọng sửa mình sau chấn động, không hoảng loạn",
        "cat_hung": "BÌNH"
    },
    "Thuần Cấn": {
        "thuong": "Cấn", "ha": "Cấn", "thu_tu": 52,
        "thoan": "Cấn kỳ bối, bất hoạch kỳ thân — Giữ yên, không thấy thân",
        "dai_tuong": "Hai núi chồng, quân tử biết dừng đúng lúc",
        "y_nghia": "Dừng lại, tĩnh lặng, biết đủ, ổn định",
        "loi_khuyen": "Biết dừng, biết đủ, tĩnh tâm suy ngẫm",
        "cat_hung": "BÌNH"
    },
    "Phong Sơn Tiệm": {
        "thuong": "Tốn", "ha": "Cấn", "thu_tu": 53,
        "thoan": "Nữ quy cát, lợi trinh — Tiến từ từ, thuận lợi",
        "dai_tuong": "Trên núi có cây, quân tử cư hiền đức thiện tục",
        "y_nghia": "Tiến từ từ, phát triển tuần tự, hôn nhân",
        "loi_khuyen": "Tiến bước từ từ, không vội vàng, phát triển bền vững",
        "cat_hung": "CÁT"
    },
    "Lôi Trạch Quy Muội": {
        "thuong": "Chấn", "ha": "Đoài", "thu_tu": 54,
        "thoan": "Chinh hung, vô du lợi — Gả em gái, bất lợi",
        "dai_tuong": "Trên đầm có sấm, quân tử dĩ vĩnh chung tri tệ",
        "y_nghia": "Hôn nhân không thuận, quan hệ bất chính, vội vàng",
        "loi_khuyen": "Cẩn thận trong quan hệ, đừng vội vàng kết hợp",
        "cat_hung": "HUNG"
    },
    "Lôi Hỏa Phong": {
        "thuong": "Chấn", "ha": "Ly", "thu_tu": 55,
        "thoan": "Hanh, vương cách chi — Phong phú, cực thịnh",
        "dai_tuong": "Sấm điện cùng đến, quân tử chiết ngục trí hình",
        "y_nghia": "Phong phú, thịnh vượng, cực thịnh nhưng sẽ suy",
        "loi_khuyen": "Tận hưởng thịnh vượng nhưng biết rằng sẽ suy, chuẩn bị",
        "cat_hung": "CÁT"
    },
    "Hỏa Sơn Lữ": {
        "thuong": "Ly", "ha": "Cấn", "thu_tu": 56,
        "thoan": "Tiểu hanh, lữ trinh cát — Lữ hành, dừng chân ngắn",
        "dai_tuong": "Trên núi có lửa, quân tử minh thận dụng hình",
        "y_nghia": "Lữ hành, tạm thời, không ổn định, du lịch",
        "loi_khuyen": "Khiêm tốn khi ở nơi lạ, đừng kiêu ngạo, linh hoạt",
        "cat_hung": "BÌNH"
    },
    # === QUẺ 57-64 ===
    "Thuần Tốn": {
        "thuong": "Tốn", "ha": "Tốn", "thu_tu": 57,
        "thoan": "Tiểu hanh, lợi hữu du vãng — Gió thuận thâm nhập",
        "dai_tuong": "Gió theo nhau, quân tử thân mệnh hành sự",
        "y_nghia": "Thuận, thâm nhập, nhẹ nhàng, buôn bán",
        "loi_khuyen": "Khiêm nhường thâm nhập, dần dần tiến, linh hoạt",
        "cat_hung": "CÁT"
    },
    "Thuần Đoài": {
        "thuong": "Đoài", "ha": "Đoài", "thu_tu": 58,
        "thoan": "Hanh, lợi trinh — Vui vẻ, hòa hợp",
        "dai_tuong": "Đầm liền nhau, quân tử bằng hữu giảng tập",
        "y_nghia": "Vui vẻ, trao đổi, giao tiếp, hưởng thụ",
        "loi_khuyen": "Giao tiếp cởi mở, vui vẻ chia sẻ, trao đổi bàn bạc",
        "cat_hung": "CÁT"
    },
    "Phong Thủy Hoán": {
        "thuong": "Tốn", "ha": "Khảm", "thu_tu": 59,
        "thoan": "Hanh, vương cách hữu miếu — Tan rã rồi hội tụ",
        "dai_tuong": "Gió trên nước, tiên vương hưởng vu đế lập miếu",
        "y_nghia": "Phân tán, tan rã, rồi tập hợp lại, lưu thông",
        "loi_khuyen": "Phá bỏ rào cản, tập hợp lại sau phân tán",
        "cat_hung": "BÌNH"
    },
    "Thủy Trạch Tiết": {
        "thuong": "Khảm", "ha": "Đoài", "thu_tu": 60,
        "thoan": "Hanh, khổ tiết bất khả trinh — Tiết chế, điều độ",
        "dai_tuong": "Trên đầm có nước, quân tử chế số độ nghị đức hạnh",
        "y_nghia": "Tiết chế, điều độ, giới hạn, kỷ luật",
        "loi_khuyen": "Giữ điều độ, tiết chế chi tiêu và hành vi",
        "cat_hung": "CÁT"
    },
    "Phong Trạch Trung Phu": {
        "thuong": "Tốn", "ha": "Đoài", "thu_tu": 61,
        "thoan": "Đồn ngư cát, lợi thiệp đại xuyên — Lòng thành cảm hóa",
        "dai_tuong": "Trên đầm có gió, quân tử nghị ngục hoãn tử",
        "y_nghia": "Trung thành, tin tưởng, lòng thành, cảm hóa",
        "loi_khuyen": "Giữ lòng thành, tin tưởng lẫn nhau, cảm hóa người",
        "cat_hung": "CÁT"
    },
    "Lôi Sơn Tiểu Quá": {
        "thuong": "Chấn", "ha": "Cấn", "thu_tu": 62,
        "thoan": "Hanh lợi trinh, khả tiểu sự — Vượt nhỏ, làm việc nhỏ tốt",
        "dai_tuong": "Trên núi có sấm, quân tử hành quá cung, tang quá ai",
        "y_nghia": "Vượt qua nhỏ, làm việc nhỏ, khiêm tốn hạ mình",
        "loi_khuyen": "Chỉ làm việc nhỏ, đừng tham lam, khiêm tốn",
        "cat_hung": "BÌNH"
    },
    "Thủy Hỏa Ký Tế": {
        "thuong": "Khảm", "ha": "Ly", "thu_tu": 63,
        "thoan": "Hanh tiểu, lợi trinh, sơ cát chung loạn — Đã xong việc",
        "dai_tuong": "Nước trên lửa, quân tử tư hoạn nhi dự phòng",
        "y_nghia": "Đã hoàn thành, mọi việc đâu vào đấy, nhưng cần phòng suy",
        "loi_khuyen": "Cẩn thận sau thành công, phòng ngừa suy thoái",
        "cat_hung": "CÁT"
    },
    "Hỏa Thủy Vị Tế": {
        "thuong": "Ly", "ha": "Khảm", "thu_tu": 64,
        "thoan": "Hanh, tiểu hồ kỷ tế — Chưa hoàn thành, còn tiếp tục",
        "dai_tuong": "Lửa trên nước, quân tử thận biện vật cư phương",
        "y_nghia": "Chưa hoàn thành, vẫn tiếp tục, tiềm năng phía trước",
        "loi_khuyen": "Kiên nhẫn hoàn thành, đừng bỏ cuộc, vẫn còn cơ hội",
        "cat_hung": "BÌNH"
    },
}

# ======================================================================
# 2. THIẾT BẢN 60 HOA GIÁP NẠP ÂM — Đầy đủ 60 Can Chi
# ======================================================================
THIET_BAN_60 = {
    "Giáp Tý": {"nap_am": "Hải Trung Kim", "hanh": "Kim", "giai_thich": "Vàng trong biển — Tiềm lực ẩn giấu, cần thời cơ"},
    "Ất Sửu": {"nap_am": "Hải Trung Kim", "hanh": "Kim", "giai_thich": "Vàng trong biển — Tiềm lực ẩn giấu, cần thời cơ"},
    "Bính Dần": {"nap_am": "Lô Trung Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa trong lò — Năng lượng bị kiềm chế, cần môi trường phù hợp"},
    "Đinh Mão": {"nap_am": "Lô Trung Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa trong lò — Năng lượng bị kiềm chế, cần môi trường phù hợp"},
    "Mậu Thìn": {"nap_am": "Đại Lâm Mộc", "hanh": "Mộc", "giai_thich": "Gỗ rừng lớn — Sức mạnh to lớn, phát triển bền vững"},
    "Kỷ Tị": {"nap_am": "Đại Lâm Mộc", "hanh": "Mộc", "giai_thich": "Gỗ rừng lớn — Sức mạnh to lớn, phát triển bền vững"},
    "Canh Ngọ": {"nap_am": "Lộ Bàng Thổ", "hanh": "Thổ", "giai_thich": "Đất ven đường — Bình thường, không nổi bật"},
    "Tân Mùi": {"nap_am": "Lộ Bàng Thổ", "hanh": "Thổ", "giai_thich": "Đất ven đường — Bình thường, không nổi bật"},
    "Nhâm Thân": {"nap_am": "Kiếm Phong Kim", "hanh": "Kim", "giai_thich": "Vàng mũi kiếm — Sắc bén, quyết đoán"},
    "Quý Dậu": {"nap_am": "Kiếm Phong Kim", "hanh": "Kim", "giai_thich": "Vàng mũi kiếm — Sắc bén, quyết đoán"},
    "Giáp Tuất": {"nap_am": "Sơn Đầu Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa trên núi — Danh tiếng cao, nhưng dễ tắt"},
    "Ất Hợi": {"nap_am": "Sơn Đầu Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa trên núi — Danh tiếng cao, nhưng dễ tắt"},
    "Bính Tý": {"nap_am": "Giản Hạ Thủy", "hanh": "Thủy", "giai_thich": "Nước dưới khe — Ẩn mình, bền bỉ"},
    "Đinh Sửu": {"nap_am": "Giản Hạ Thủy", "hanh": "Thủy", "giai_thich": "Nước dưới khe — Ẩn mình, bền bỉ"},
    "Mậu Dần": {"nap_am": "Thành Đầu Thổ", "hanh": "Thổ", "giai_thich": "Đất trên thành — Vững chắc, an toàn"},
    "Kỷ Mão": {"nap_am": "Thành Đầu Thổ", "hanh": "Thổ", "giai_thich": "Đất trên thành — Vững chắc, an toàn"},
    "Canh Thìn": {"nap_am": "Bạch Lạp Kim", "hanh": "Kim", "giai_thich": "Vàng nến trắng — Đẹp nhưng dễ hao tổn"},
    "Tân Tị": {"nap_am": "Bạch Lạp Kim", "hanh": "Kim", "giai_thich": "Vàng nến trắng — Đẹp nhưng dễ hao tổn"},
    "Nhâm Ngọ": {"nap_am": "Dương Liễu Mộc", "hanh": "Mộc", "giai_thich": "Gỗ cây liễu — Mềm mại, thích nghi tốt"},
    "Quý Mùi": {"nap_am": "Dương Liễu Mộc", "hanh": "Mộc", "giai_thich": "Gỗ cây liễu — Mềm mại, thích nghi tốt"},
    "Giáp Thân": {"nap_am": "Tuyền Trung Thủy", "hanh": "Thủy", "giai_thich": "Nước suối — Tinh khiết, nguồn lực dồi dào"},
    "Ất Dậu": {"nap_am": "Tuyền Trung Thủy", "hanh": "Thủy", "giai_thich": "Nước suối — Tinh khiết, nguồn lực dồi dào"},
    "Bính Tuất": {"nap_am": "Ốc Thượng Thổ", "hanh": "Thổ", "giai_thich": "Đất trên mái — Bảo vệ, che chở"},
    "Đinh Hợi": {"nap_am": "Ốc Thượng Thổ", "hanh": "Thổ", "giai_thich": "Đất trên mái — Bảo vệ, che chở"},
    "Mậu Tý": {"nap_am": "Tích Lịch Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa sấm sét — Mạnh mẽ, bùng nổ ngắn hạn"},
    "Kỷ Sửu": {"nap_am": "Tích Lịch Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa sấm sét — Mạnh mẽ, bùng nổ ngắn hạn"},
    "Canh Dần": {"nap_am": "Tùng Bách Mộc", "hanh": "Mộc", "giai_thich": "Gỗ tùng bách — Bền bỉ, kiên cường"},
    "Tân Mão": {"nap_am": "Tùng Bách Mộc", "hanh": "Mộc", "giai_thich": "Gỗ tùng bách — Bền bỉ, kiên cường"},
    "Nhâm Thìn": {"nap_am": "Trường Lưu Thủy", "hanh": "Thủy", "giai_thich": "Nước chảy dài — Kiên trì, không ngừng tiến"},
    "Quý Tị": {"nap_am": "Trường Lưu Thủy", "hanh": "Thủy", "giai_thich": "Nước chảy dài — Kiên trì, không ngừng tiến"},
    "Giáp Ngọ": {"nap_am": "Sa Trung Kim", "hanh": "Kim", "giai_thich": "Vàng trong cát — Quý nhưng cần tìm kiếm"},
    "Ất Mùi": {"nap_am": "Sa Trung Kim", "hanh": "Kim", "giai_thich": "Vàng trong cát — Quý nhưng cần tìm kiếm"},
    "Bính Thân": {"nap_am": "Sơn Hạ Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa dưới núi — Sắp bùng phát, chờ thời cơ"},
    "Đinh Dậu": {"nap_am": "Sơn Hạ Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa dưới núi — Sắp bùng phát, chờ thời cơ"},
    "Mậu Tuất": {"nap_am": "Bình Địa Mộc", "hanh": "Mộc", "giai_thich": "Gỗ đất bằng — Ổn định, phát triển đều"},
    "Kỷ Hợi": {"nap_am": "Bình Địa Mộc", "hanh": "Mộc", "giai_thich": "Gỗ đất bằng — Ổn định, phát triển đều"},
    "Canh Tý": {"nap_am": "Bích Thượng Thổ", "hanh": "Thổ", "giai_thich": "Đất trên tường — Trang trí, chú trọng bên trong"},
    "Tân Sửu": {"nap_am": "Bích Thượng Thổ", "hanh": "Thổ", "giai_thich": "Đất trên tường — Trang trí, chú trọng bên trong"},
    "Nhâm Dần": {"nap_am": "Kim Bạc Kim", "hanh": "Kim", "giai_thich": "Vàng lá mỏng — Đẹp nhưng mỏng manh"},
    "Quý Mão": {"nap_am": "Kim Bạc Kim", "hanh": "Kim", "giai_thich": "Vàng lá mỏng — Đẹp nhưng mỏng manh"},
    "Giáp Thìn": {"nap_am": "Phúc Đăng Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa đèn phủ — Ẩn giấu, cần hỗ trợ"},
    "Ất Tị": {"nap_am": "Phúc Đăng Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa đèn phủ — Ẩn giấu, cần hỗ trợ"},
    "Bính Ngọ": {"nap_am": "Thiên Hà Thủy", "hanh": "Thủy", "giai_thich": "Nước sông trời — Cao quý, khan hiếm"},
    "Đinh Mùi": {"nap_am": "Thiên Hà Thủy", "hanh": "Thủy", "giai_thich": "Nước sông trời — Cao quý, khan hiếm"},
    "Mậu Thân": {"nap_am": "Đại Trạch Thổ", "hanh": "Thổ", "giai_thich": "Đất bãi lớn — Rộng rãi, thuận mở rộng"},
    "Kỷ Dậu": {"nap_am": "Đại Trạch Thổ", "hanh": "Thổ", "giai_thich": "Đất bãi lớn — Rộng rãi, thuận mở rộng"},
    "Canh Tuất": {"nap_am": "Thoa Xuyến Kim", "hanh": "Kim", "giai_thich": "Vàng trang sức — Sang trọng, hưởng thụ"},
    "Tân Hợi": {"nap_am": "Thoa Xuyến Kim", "hanh": "Kim", "giai_thich": "Vàng trang sức — Sang trọng, hưởng thụ"},
    "Nhâm Tý": {"nap_am": "Tang Đố Mộc", "hanh": "Mộc", "giai_thich": "Gỗ cây dâu — Thực dụng, tốt cho sinh kế"},
    "Quý Sửu": {"nap_am": "Tang Đố Mộc", "hanh": "Mộc", "giai_thich": "Gỗ cây dâu — Thực dụng, tốt cho sinh kế"},
    "Giáp Dần": {"nap_am": "Đại Khê Thủy", "hanh": "Thủy", "giai_thich": "Nước khe lớn — Dồi dào, cẩn thận lũ"},
    "Ất Mão": {"nap_am": "Đại Khê Thủy", "hanh": "Thủy", "giai_thich": "Nước khe lớn — Dồi dào, cẩn thận lũ"},
    "Bính Thìn": {"nap_am": "Sa Trung Thổ", "hanh": "Thổ", "giai_thich": "Đất trong cát — Không ổn định, cần gia cố"},
    "Đinh Tị": {"nap_am": "Sa Trung Thổ", "hanh": "Thổ", "giai_thich": "Đất trong cát — Không ổn định, cần gia cố"},
    "Mậu Ngọ": {"nap_am": "Thiên Thượng Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa trên trời — Rạng rỡ, vinh quang"},
    "Kỷ Mùi": {"nap_am": "Thiên Thượng Hỏa", "hanh": "Hỏa", "giai_thich": "Lửa trên trời — Rạng rỡ, vinh quang"},
    "Canh Thân": {"nap_am": "Thạch Lựu Mộc", "hanh": "Mộc", "giai_thich": "Gỗ lựu đá — Cứng cỏi, kiên định"},
    "Tân Dậu": {"nap_am": "Thạch Lựu Mộc", "hanh": "Mộc", "giai_thich": "Gỗ lựu đá — Cứng cỏi, kiên định"},
    "Nhâm Tuất": {"nap_am": "Đại Hải Thủy", "hanh": "Thủy", "giai_thich": "Nước biển lớn — Bao la, quyền lực lớn"},
    "Quý Hợi": {"nap_am": "Đại Hải Thủy", "hanh": "Thủy", "giai_thich": "Nước biển lớn — Bao la, quyền lực lớn"},
}

# ======================================================================
# 3. MAI HOA THỂ DỤNG — Bảng quan hệ sinh khắc 25 tổ hợp
# ======================================================================
MAI_HOA_THE_DUNG = {
    # Key = (Hành_Thể, Hành_Dụng) → kết luận
    ("Kim", "Kim"): {"quan_he": "Tỷ Hòa", "ket_luan": "BÌNH", "chi_tiet": "Thể Dụng cùng hành, ngang nhau, sự việc bình thường"},
    ("Kim", "Mộc"): {"quan_he": "Thể khắc Dụng", "ket_luan": "CÁT", "chi_tiet": "Kim khắc Mộc, ta chiến thắng, mình thắng đối phương"},
    ("Kim", "Thủy"): {"quan_he": "Thể sinh Dụng", "ket_luan": "HUNG", "chi_tiet": "Kim sinh Thủy, ta hao tổn sức lực cho người, mất mát"},
    ("Kim", "Hỏa"): {"quan_he": "Dụng khắc Thể", "ket_luan": "ĐẠI HUNG", "chi_tiet": "Hỏa khắc Kim, ta bị khắc chế, rất bất lợi"},
    ("Kim", "Thổ"): {"quan_he": "Dụng sinh Thể", "ket_luan": "ĐẠI CÁT", "chi_tiet": "Thổ sinh Kim, ta được hỗ trợ, rất thuận lợi"},
    ("Mộc", "Mộc"): {"quan_he": "Tỷ Hòa", "ket_luan": "BÌNH", "chi_tiet": "Thể Dụng cùng hành, ngang nhau, sự việc bình thường"},
    ("Mộc", "Hỏa"): {"quan_he": "Thể sinh Dụng", "ket_luan": "HUNG", "chi_tiet": "Mộc sinh Hỏa, ta hao tổn sức lực cho người"},
    ("Mộc", "Thổ"): {"quan_he": "Thể khắc Dụng", "ket_luan": "CÁT", "chi_tiet": "Mộc khắc Thổ, ta chiến thắng đối phương"},
    ("Mộc", "Kim"): {"quan_he": "Dụng khắc Thể", "ket_luan": "ĐẠI HUNG", "chi_tiet": "Kim khắc Mộc, ta bị khắc chế, rất bất lợi"},
    ("Mộc", "Thủy"): {"quan_he": "Dụng sinh Thể", "ket_luan": "ĐẠI CÁT", "chi_tiet": "Thủy sinh Mộc, ta được hỗ trợ, rất thuận lợi"},
    ("Thủy", "Thủy"): {"quan_he": "Tỷ Hòa", "ket_luan": "BÌNH", "chi_tiet": "Thể Dụng cùng hành, ngang nhau"},
    ("Thủy", "Mộc"): {"quan_he": "Thể sinh Dụng", "ket_luan": "HUNG", "chi_tiet": "Thủy sinh Mộc, ta hao tổn sức lực cho người"},
    ("Thủy", "Hỏa"): {"quan_he": "Thể khắc Dụng", "ket_luan": "CÁT", "chi_tiet": "Thủy khắc Hỏa, ta chiến thắng đối phương"},
    ("Thủy", "Thổ"): {"quan_he": "Dụng khắc Thể", "ket_luan": "ĐẠI HUNG", "chi_tiet": "Thổ khắc Thủy, ta bị khắc chế, rất bất lợi"},
    ("Thủy", "Kim"): {"quan_he": "Dụng sinh Thể", "ket_luan": "ĐẠI CÁT", "chi_tiet": "Kim sinh Thủy, ta được hỗ trợ, rất thuận lợi"},
    ("Hỏa", "Hỏa"): {"quan_he": "Tỷ Hòa", "ket_luan": "BÌNH", "chi_tiet": "Thể Dụng cùng hành, ngang nhau"},
    ("Hỏa", "Thổ"): {"quan_he": "Thể sinh Dụng", "ket_luan": "HUNG", "chi_tiet": "Hỏa sinh Thổ, ta hao tổn sức lực cho người"},
    ("Hỏa", "Kim"): {"quan_he": "Thể khắc Dụng", "ket_luan": "CÁT", "chi_tiet": "Hỏa khắc Kim, ta chiến thắng đối phương"},
    ("Hỏa", "Thủy"): {"quan_he": "Dụng khắc Thể", "ket_luan": "ĐẠI HUNG", "chi_tiet": "Thủy khắc Hỏa, ta bị khắc chế, rất bất lợi"},
    ("Hỏa", "Mộc"): {"quan_he": "Dụng sinh Thể", "ket_luan": "ĐẠI CÁT", "chi_tiet": "Mộc sinh Hỏa, ta được hỗ trợ, rất thuận lợi"},
    ("Thổ", "Thổ"): {"quan_he": "Tỷ Hòa", "ket_luan": "BÌNH", "chi_tiet": "Thể Dụng cùng hành, ngang nhau"},
    ("Thổ", "Kim"): {"quan_he": "Thể sinh Dụng", "ket_luan": "HUNG", "chi_tiet": "Thổ sinh Kim, ta hao tổn sức lực cho người"},
    ("Thổ", "Thủy"): {"quan_he": "Thể khắc Dụng", "ket_luan": "CÁT", "chi_tiet": "Thổ khắc Thủy, ta chiến thắng đối phương"},
    ("Thổ", "Mộc"): {"quan_he": "Dụng khắc Thể", "ket_luan": "ĐẠI HUNG", "chi_tiet": "Mộc khắc Thổ, ta bị khắc chế, rất bất lợi"},
    ("Thổ", "Hỏa"): {"quan_he": "Dụng sinh Thể", "ket_luan": "ĐẠI CÁT", "chi_tiet": "Hỏa sinh Thổ, ta được hỗ trợ, rất thuận lợi"},
}

# ======================================================================
# 4. MAI HOA ỨNG KỲ — Thời điểm ứng nghiệm theo Ngũ Hành
# ======================================================================
MAI_HOA_UNG_KY = {
    "Thể khắc Dụng": {
        "toc_do": "nhanh",
        "giai_thich": "Ta thắng → ứng nghiệm sớm, vào ngày/tháng hành bị khắc vượng",
        "vi_du": "Kim khắc Mộc → ứng vào ngày Dần/Mão (Mộc) hoặc Thân/Dậu (Kim vượng)"
    },
    "Dụng sinh Thể": {
        "toc_do": "nhanh",
        "giai_thich": "Được giúp → ứng sớm, vào ngày/tháng hành sinh Thể vượng",
        "vi_du": "Thủy sinh Mộc → ứng vào ngày Hợi/Tý (Thủy vượng)"
    },
    "Thể sinh Dụng": {
        "toc_do": "chậm",
        "giai_thich": "Ta hao → suy yếu dần, ứng khi hành Thể được sinh trở lại",
        "vi_du": "Mộc sinh Hỏa (ta hao) → ứng khi gặp Thủy (Thủy sinh Mộc, phục hồi)"
    },
    "Dụng khắc Thể": {
        "toc_do": "chậm",
        "giai_thich": "Bị khắc → xấu, ứng khi hành khắc Dụng xuất hiện (cứu giải)",
        "vi_du": "Hỏa khắc Kim (ta bị khắc) → chờ Thủy (Thủy khắc Hỏa) giải cứu"
    },
    "Tỷ Hòa": {
        "toc_do": "bình",
        "giai_thich": "Ngang nhau → ứng vào ngày/tháng hành tương sinh với Thể",
        "vi_du": "Mộc-Mộc → ứng ngày Hợi/Tý (Thủy sinh Mộc)"
    },
}

# ======================================================================
# 5. HÀM HELPER — Tra cứu nhanh
# ======================================================================
def tra_kinh_dich(ten_que):
    """Trả về dict ý nghĩa từ tên quẻ. None nếu không tìm thấy."""
    return KINH_DICH_64.get(ten_que, None)

def tra_nap_am(can_chi):
    """Trả về dict Nạp Âm từ Can Chi (VD: 'Giáp Tý'). None nếu không tìm thấy."""
    return THIET_BAN_60.get(can_chi, None)

def tra_the_dung(hanh_the, hanh_dung):
    """Trả về dict quan hệ Thể-Dụng. None nếu không tìm thấy."""
    return MAI_HOA_THE_DUNG.get((hanh_the, hanh_dung), None)


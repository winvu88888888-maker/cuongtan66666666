# -*- coding: utf-8 -*-
"""
THOÁN TỪ + ĐẠI TƯỢNG — 64 QUẺ KINH DỊCH
Nguồn: Kinh Dịch - Chu Dịch (周易)
V42.9.39: Bổ sung đầy đủ 64 quẻ cho AI luận giải chính xác
"""

QUE_THOAN_64 = {
    # ══════ CUNG CÀN (8 quẻ) ══════
    'Thuần Càn': {'thoan': 'Nguyên hanh lợi trinh — Khởi đầu hanh thông, lợi ích bền vững', 'dai_tuong': 'Trời vận hành mạnh mẽ, quân tử tự cường không nghỉ', 'lk': 'Cương kiện, hành động quyết đoán'},
    'Thiên Phong Cấu': {'thoan': 'Nữ tráng, chớ dùng thú nữ — Gặp gỡ bất ngờ, cẩn thận tiểu nhân', 'dai_tuong': 'Dưới trời có gió, vua ban mệnh lệnh bốn phương', 'lk': 'Gặp gỡ, nhưng cần cảnh giác'},
    'Thiên Sơn Độn': {'thoan': 'Hanh, tiểu lợi trinh — Ẩn lui đúng lúc là khôn ngoan', 'dai_tuong': 'Dưới trời có núi, quân tử tránh xa tiểu nhân', 'lk': 'Lùi bước, ẩn mình chờ thời'},
    'Thiên Địa Bĩ': {'thoan': 'Bĩ chi phỉ nhân, bất lợi quân tử trinh — Bế tắc, trời đất không giao', 'dai_tuong': 'Trời đất không giao, quân tử kiệm đức tránh nạn', 'lk': 'Tắc nghẽn, cần kiên nhẫn chờ đợi'},
    'Phong Địa Quan': {'thoan': 'Quán, quán nhi bất tiến — Quan sát, chiêm ngưỡng từ xa', 'dai_tuong': 'Gió thổi trên đất, vua tuần du bốn phương', 'lk': 'Quan sát kỹ trước khi hành động'},
    'Sơn Địa Bác': {'thoan': 'Bất lợi hữu du vãng — Bóc lột, sụp đổ dần từ dưới lên', 'dai_tuong': 'Núi dựa trên đất, bên trên hậu đãi bên dưới', 'lk': 'Suy thoái, không nên tiến, giữ vững'},
    'Hỏa Địa Tấn': {'thoan': 'Khang hầu dĩ tích mã — Tiến lên, ban thưởng xứng đáng', 'dai_tuong': 'Mặt trời mọc trên đất, quân tử tự sáng đức', 'lk': 'Thăng tiến, phát triển thuận lợi'},
    'Hỏa Thiên Đại Hữu': {'thoan': 'Nguyên hanh — Sở hữu lớn, phong phú dồi dào', 'dai_tuong': 'Lửa trên trời, quân tử ngăn ác dương thiện', 'lk': 'Thịnh vượng, giàu có, thành công lớn'},

    # ══════ CUNG KHẢM (8 quẻ) ══════
    'Thuần Khảm': {'thoan': 'Tập Khảm, có phu duy tâm hanh — Hiểm liên tiếp, giữ tâm thành sẽ hanh thông', 'dai_tuong': 'Nước chảy mãi không ngừng, quân tử giữ đạo đức hằng thường', 'lk': 'Hiểm nguy, kiên trì vượt qua'},
    'Thủy Trạch Tiết': {'thoan': 'Hanh, khổ tiết bất khả trinh — Tiết chế vừa phải, quá mức thì khổ', 'dai_tuong': 'Nước trên đầm, quân tử chế định số lượng', 'lk': 'Tiết kiệm, điều độ, biết giới hạn'},
    'Thủy Lôi Truân': {'thoan': 'Nguyên hanh lợi trinh, chớ dùng hữu du vãng — Khó khăn ban đầu', 'dai_tuong': 'Mây sấm nổi, quân tử kinh luân thiên hạ', 'lk': 'Gian nan buổi đầu, cần kiên nhẫn'},
    'Thủy Hỏa Ký Tế': {'thoan': 'Hanh tiểu, lợi trinh — Đã xong việc, tiểu cát', 'dai_tuong': 'Nước trên lửa, quân tử nghĩ hoạn phòng trước', 'lk': 'Việc đã thành, cần giữ gìn thành quả'},
    'Trạch Hỏa Cách': {'thoan': 'Kỷ nhật nãi phu — Cải cách, thay đổi lớn', 'dai_tuong': 'Đầm có lửa, quân tử trị lịch sáng thời', 'lk': 'Thay đổi, cách mạng, đổi mới'},
    'Lôi Hỏa Phong': {'thoan': 'Hanh, vua tới đền — Phong phú, to lớn, cực thịnh', 'dai_tuong': 'Sấm chớp đều đến, quân tử xét kiện rõ ràng', 'lk': 'Hưng thịnh nhưng cẩn thận suy thoái'},
    'Địa Hỏa Minh Di': {'thoan': 'Lợi gian trinh — Ánh sáng bị thương, ẩn giấu', 'dai_tuong': 'Sáng vào trong đất, quân tử trị dân dùng tối che sáng', 'lk': 'Giấu tài, nhẫn nhịn, chờ thời'},
    'Địa Thủy Sư': {'thoan': 'Trinh, trượng nhân cát — Quân đội, cần người lãnh đạo giỏi', 'dai_tuong': 'Nước trong đất, quân tử dung dân nuôi quân', 'lk': 'Tập hợp lực lượng, cần thủ lĩnh'},

    # ══════ CUNG CẤN (8 quẻ) ══════
    'Thuần Cấn': {'thoan': 'Cấn kỳ bối, không đạt thân — Dừng lại, giữ yên', 'dai_tuong': 'Hai núi chồng nhau, quân tử biết dừng đúng lúc', 'lk': 'Tĩnh lặng, biết dừng, biết đủ'},
    'Sơn Hỏa Bí': {'thoan': 'Hanh, tiểu lợi hữu du vãng — Trang sức, vẻ đẹp bên ngoài', 'dai_tuong': 'Dưới núi có lửa, quân tử sáng chính trị', 'lk': 'Trang hoàng, nhưng chú trọng nội dung'},
    'Sơn Thiên Đại Súc': {'thoan': 'Lợi trinh, bất gia thực cát — Tích lũy lớn, nuôi dưỡng hiền tài', 'dai_tuong': 'Trời trong núi, quân tử học cổ nhân', 'lk': 'Tích lũy, học hỏi, nuôi chí lớn'},
    'Sơn Trạch Tổn': {'thoan': 'Có phu, nguyên cát — Giảm bớt dưới bổ sung trên', 'dai_tuong': 'Dưới núi có đầm, quân tử trừng giận bớt dục', 'lk': 'Bớt dưới thêm trên, hy sinh vì đại nghĩa'},
    'Hỏa Trạch Khuê': {'thoan': 'Tiểu sự cát — Trái ngược, mâu thuẫn nhưng có thể hợp', 'dai_tuong': 'Lửa lên đầm xuống, quân tử đồng mà khác', 'lk': 'Bất đồng, nhưng tìm điểm chung'},
    'Thiên Lôi Vô Vọng': {'thoan': 'Nguyên hanh lợi trinh — Không vọng tưởng, thuận theo tự nhiên', 'dai_tuong': 'Dưới trời có sấm, vạn vật thuận tính', 'lk': 'Chân thật, không mưu tính sẽ tốt'},
    'Phong Lôi Ích': {'thoan': 'Lợi hữu du vãng, lợi thiệp đại xuyên — Thêm vào, tăng trưởng', 'dai_tuong': 'Gió sấm, quân tử thấy thiện thì làm, có lỗi thì sửa', 'lk': 'Tăng trưởng, bổ sung, phát triển'},
    'Phong Sơn Tiệm': {'thoan': 'Nữ quy cát, lợi trinh — Tiến dần từng bước', 'dai_tuong': 'Trên núi có gió, quân tử ở hiền đức', 'lk': 'Tiến từ từ, không vội, tuần tự'},

    # ══════ CUNG CHẤN (8 quẻ) ══════
    'Thuần Chấn': {'thoan': 'Hanh, sấm đến sợ sợ — Chấn động, sợ hãi rồi vui', 'dai_tuong': 'Sấm liên tiếp, quân tử sợ mà tu sửa mình', 'lk': 'Chấn động, tỉnh ngộ, đổi mới'},
    'Lôi Địa Dự': {'thoan': 'Lợi kiến hầu hành sư — Vui vẻ, thuận lợi hành quân', 'dai_tuong': 'Sấm nổ trên đất, tiên vương tác nhạc sùng đức', 'lk': 'Vui vẻ, phấn khởi, thuận lợi khởi sự'},
    'Lôi Thủy Giải': {'thoan': 'Lợi tây nam, vô sở vãng — Giải thoát, tháo gỡ vướng mắc', 'dai_tuong': 'Sấm mưa nổi, quân tử xá tội lỗi', 'lk': 'Giải quyết vấn đề, tha thứ'},
    'Lôi Phong Hằng': {'thoan': 'Hanh, vô cữu, lợi trinh — Bền vững, kiên trì lâu dài', 'dai_tuong': 'Sấm gió, quân tử đứng vững không đổi hướng', 'lk': 'Kiên trì, bền bỉ, không thay đổi'},
    'Địa Phong Thăng': {'thoan': 'Nguyên hanh, dùng kiến đại nhân — Thăng tiến, đi lên', 'dai_tuong': 'Cây mọc trong đất, quân tử thuận đức tích nhỏ thành cao', 'lk': 'Thăng tiến, phát triển đi lên'},
    'Thủy Phong Tỉnh': {'thoan': 'Cải ấp bất cải tỉnh — Giếng nước, không đổi, nuôi dưỡng', 'dai_tuong': 'Trên gỗ có nước, quân tử lao dân khuyến tương', 'lk': 'Nguồn sống, nuôi dưỡng, bất biến'},
    'Trạch Phong Đại Quá': {'thoan': 'Đống nóc cong, lợi hữu du vãng — Vượt quá mức, cần hành động', 'dai_tuong': 'Đầm ngập gỗ, quân tử đứng vững một mình', 'lk': 'Quá tải, cần biện pháp đặc biệt'},
    'Trạch Lôi Tùy': {'thoan': 'Nguyên hanh lợi trinh — Thuận theo, đi theo, thích ứng', 'dai_tuong': 'Đầm trong có sấm, quân tử tối nghỉ ngơi', 'lk': 'Thuận theo hoàn cảnh, linh hoạt'},

    # ══════ CUNG TỐN (8 quẻ) ══════
    'Thuần Tốn': {'thoan': 'Tiểu hanh, lợi hữu du vãng — Thuận gió thâm nhập', 'dai_tuong': 'Gió theo gió, quân tử truyền mệnh lệnh', 'lk': 'Khiêm nhường, thâm nhập dần dần'},
    'Phong Thiên Tiểu Súc': {'thoan': 'Hanh, mật vân bất vũ — Tích lũy nhỏ, mây dày chưa mưa', 'dai_tuong': 'Gió trên trời, quân tử tốt đẹp văn đức', 'lk': 'Tích lũy từ từ, chưa đến lúc'},
    'Phong Hỏa Gia Nhân': {'thoan': 'Lợi nữ trinh — Gia đình, nữ chính nội', 'dai_tuong': 'Gió từ lửa ra, quân tử lời có thực hành có thường', 'lk': 'Gia đạo, nội bộ hài hòa'},
    'Phong Lôi Ích': {'thoan': 'Lợi hữu du vãng, lợi thiệp đại xuyên — Thêm vào, gia tăng', 'dai_tuong': 'Gió sấm, quân tử thấy thiện thì theo', 'lk': 'Được lợi, tăng trưởng'},
    'Thiên Lôi Vô Vọng': {'thoan': 'Nguyên hanh lợi trinh — Chân thật, không vọng tưởng', 'dai_tuong': 'Dưới trời sấm động, vạn vật thuận tính', 'lk': 'Thành thật, thuận tự nhiên'},
    'Hỏa Lôi Phệ Hạp': {'thoan': 'Hanh, lợi dụng ngục — Cắn hợp, trừng phạt, xét xử', 'dai_tuong': 'Sấm chớp, tiên vương minh phạt sắc pháp', 'lk': 'Quyết đoán xử lý, pháp luật'},
    'Sơn Lôi Di': {'thoan': 'Trinh cát, quan di — Nuôi dưỡng, ăn uống, tu dưỡng', 'dai_tuong': 'Dưới núi có sấm, quân tử cẩn thận lời nói ăn uống', 'lk': 'Nuôi dưỡng thân tâm, cẩn thận'},
    'Sơn Phong Cổ': {'thoan': 'Nguyên hanh, lợi thiệp đại xuyên — Sửa chữa hư hỏng', 'dai_tuong': 'Dưới núi có gió, quân tử chấn dân dục đức', 'lk': 'Sửa chữa sai lầm, cải tổ'},

    # ══════ CUNG LY (8 quẻ) ══════
    'Thuần Ly': {'thoan': 'Lợi trinh hanh, nuôi bò mẹ cát — Bám vào, sáng soi', 'dai_tuong': 'Sáng lặp lại, đại nhân nối sáng chiếu thiên hạ', 'lk': 'Sáng suốt, minh bạch, tiếp nối'},
    'Hỏa Sơn Lữ': {'thoan': 'Tiểu hanh, lữ trinh cát — Du hành, ở trọ, khách lạ', 'dai_tuong': 'Trên núi có lửa, quân tử sáng suốt dùng hình', 'lk': 'Lưu lạc, cần thận trọng nơi lạ'},
    'Hỏa Phong Đỉnh': {'thoan': 'Nguyên cát hanh — Vạc nấu, cải cách, văn minh', 'dai_tuong': 'Trên gỗ có lửa, quân tử chính vị ngưng mệnh', 'lk': 'Đổi mới, cải cách, nuôi hiền tài'},
    'Hỏa Thủy Vị Tế': {'thoan': 'Hanh, tiểu hồ lệ tế — Chưa xong, sắp hoàn thành', 'dai_tuong': 'Lửa trên nước, quân tử thận biện vật ở phương', 'lk': 'Chưa hoàn thành, cần cố gắng thêm'},
    'Sơn Thủy Mông': {'thoan': 'Hanh, phi ngã cầu đồng mông — Mông muội cầu ta, không ta cầu', 'dai_tuong': 'Dưới núi suối chảy, quân tử quả hành dục đức', 'lk': 'Học hỏi, khai sáng, giáo dục'},
    'Phong Thủy Hoán': {'thoan': 'Hanh, vua tới đền — Tan rã rồi tụ lại, phân tán', 'dai_tuong': 'Gió trên nước, tiên vương lập đền thờ', 'lk': 'Phân tán rồi tụ, cần đoàn kết'},
    'Thiên Thủy Tụng': {'thoan': 'Có phu, trệ, giữa cát — Kiện tụng, tranh cãi', 'dai_tuong': 'Trời nước ngược chiều, quân tử mưu sự từ đầu', 'lk': 'Tranh chấp, nên hòa giải'},
    'Thiên Hỏa Đồng Nhân': {'thoan': 'Đồng nhân nơi hoang, hanh — Hòa đồng với người', 'dai_tuong': 'Trời với lửa, quân tử phân biệt vật loại', 'lk': 'Hợp tác, đoàn kết, hòa đồng'},

    # ══════ CUNG KHÔN (8 quẻ) ══════
    'Thuần Khôn': {'thoan': 'Nguyên hanh, lợi tẫn mã trinh — Đất rộng thuận chở', 'dai_tuong': 'Đất thuận chở, quân tử dày đức chở vật', 'lk': 'Nhu thuận, bao dung, kiên nhẫn'},
    'Địa Lôi Phục': {'thoan': 'Hanh, ra vào vô tật — Trở lại, phục hồi', 'dai_tuong': 'Sấm trong đất, tiên vương ngày đông chí đóng cửa', 'lk': 'Quay lại, hồi phục, khởi đầu mới'},
    'Địa Trạch Lâm': {'thoan': 'Nguyên hanh lợi trinh — Đến gần, quản lý, giám sát', 'dai_tuong': 'Trên đầm có đất, quân tử dạy dỗ vô cùng', 'lk': 'Tiếp cận, cai quản, thuận lợi'},
    'Địa Thiên Thái': {'thoan': 'Tiểu vãng đại lai, cát hanh — Trời đất giao hòa, thái bình', 'dai_tuong': 'Trời đất giao, vua tài thành trợ đạo', 'lk': 'Hanh thông, thái bình, vạn sự tốt lành'},
    'Lôi Thiên Đại Tráng': {'thoan': 'Lợi trinh — Mạnh mẽ, hùng tráng', 'dai_tuong': 'Sấm trên trời, quân tử phi lễ bất lý', 'lk': 'Mạnh mẽ nhưng cần giữ lễ'},
    'Trạch Thiên Quải': {'thoan': 'Dương vu vương đình — Quyết đoán, loại bỏ tiểu nhân', 'dai_tuong': 'Đầm lên trời, quân tử ban lộc cho dưới', 'lk': 'Quyết đoán, dứt khoát, trừ xấu'},
    'Thủy Thiên Nhu': {'thoan': 'Có phu, quang hanh — Chờ đợi đúng lúc', 'dai_tuong': 'Mây lên trời, quân tử ẩm thực yến lạc', 'lk': 'Kiên nhẫn chờ đợi thời cơ'},
    'Thủy Địa Tỷ': {'thoan': 'Cát, nguyên phệ nguyên vĩnh trinh — Thân cận, liên kết', 'dai_tuong': 'Nước trên đất, tiên vương kiến vạn quốc thân chư hầu', 'lk': 'Liên kết, hợp tác, thân cận'},

    # ══════ CUNG ĐOÀI (8 quẻ) ══════
    'Thuần Đoài': {'thoan': 'Hanh lợi trinh — Vui vẻ, hòa hợp, trao đổi', 'dai_tuong': 'Đầm liền nhau, quân tử giảng học bàn luận', 'lk': 'Vui vẻ, giao tiếp, bàn bạc'},
    'Trạch Thủy Khốn': {'thoan': 'Hanh trinh, đại nhân cát — Khốn cùng, nhưng đại nhân hanh thông', 'dai_tuong': 'Đầm không nước, quân tử trí mệnh toại chí', 'lk': 'Khốn khó, kiên trì sẽ qua'},
    'Trạch Địa Tụy': {'thoan': 'Hanh, vua tới đền — Tụ họp, đoàn tụ', 'dai_tuong': 'Đầm trên đất, quân tử trừ giới cụ bất ngu', 'lk': 'Tụ họp, đoàn kết, hội tụ'},
    'Trạch Sơn Hàm': {'thoan': 'Hanh lợi trinh, thú nữ cát — Cảm ứng, hôn nhân', 'dai_tuong': 'Trên núi có đầm, quân tử hư tâm đón người', 'lk': 'Cảm xúc, tình cảm, hôn nhân'},
    'Thủy Sơn Kiển': {'thoan': 'Lợi tây nam, bất lợi đông bắc — Gian nan, trở ngại', 'dai_tuong': 'Trên núi có nước, quân tử phản thân tu đức', 'lk': 'Khó khăn, cần tu sửa bản thân'},
    'Địa Sơn Khiêm': {'thoan': 'Hanh, quân tử hữu chung — Khiêm nhường, có kết quả tốt', 'dai_tuong': 'Trong đất có núi, quân tử bớt nhiều bù ít', 'lk': 'Khiêm tốn, nhún nhường, được phúc'},
    'Lôi Sơn Tiểu Quá': {'thoan': 'Hanh lợi trinh, tiểu sự cát — Vượt quá chút ít', 'dai_tuong': 'Trên núi có sấm, quân tử hành quá cung kính', 'lk': 'Hơi quá mức, nên khiêm tốn'},
    'Lôi Trạch Quy Muội': {'thoan': 'Chinh hung, vô du lợi — Cô gái về nhà chồng, không thuận', 'dai_tuong': 'Trên đầm có sấm, quân tử biết tệ mà trọn', 'lk': 'Hôn nhân, nhưng cần thận trọng'},
}

"""
CHUYÊN GIA DỮ LIỆU KINH DỊCH & MAI HOA (2026 PRO VERSION)
Chứa kiến thức sâu về 64 Quẻ, Lục Thân, Ngũ Hành, và Ý Nghĩa dự báo theo chủ đề.
"""

ICHING_HEXAGRAMS = {
    1: {
        "name": "Càn Vi Thiên", "symbol": "||||||", "element": "Kim",
        "general": "Sự sáng tạo, mạnh mẽ, kiên định. Tượng trưng cho Trời, người cha, sự khởi đầu vĩ đại.",
        "fortune": "Đại cát. Mọi việc hanh thông nếu giữ tâm chính trực.",
        "wish": "Thành công lớn, nhưng không được kiêu ngạo.",
        "love": "Thuận lợi nhưng cần bớt cái tôi, người nam thường gia trưởng.",
        "family": "Nghiêm khắc nhưng hưng vượng.",
        "sickness": "Liên quan đến đầu, phổi. Bệnh dương khí quá vượng.",
        "lost_item": "Tìm ở nơi cao, hướng Tây Bắc. Đồ vật kim loại/tròn.",
        "career": "Thăng tiến, làm lãnh đạo, tự mình làm chủ."
    },
    2: {
        "name": "Khôn Vi Địa", "symbol": "::::::", "element": "Thổ",
        "general": "Sự nhu thuận, bao dung, nuôi dưỡng. Tượng trưng cho Đất, người mẹ.",
        "fortune": "Cát. Lợi về lâu dài, cần kiên nhẫn tích lũy.",
        "wish": "Đạt được nếu biết nhờ cậy người khác, không nên tự ý đi đầu.",
        "love": "Bền vững, người nữ hiền thục đảm đang.",
        "family": "Hòa thuận, ấm áp.",
        "sickness": "Bụng, dạ dày, tiêu hóa. Bệnh âm ỉ kéo dài.",
        "lost_item": "Tìm ở nơi thấp, tối, hướng Tây Nam. Đồ vải vóc/gồm sứ.",
        "career": "Làm phó, hỗ trợ, hậu cần rất tốt."
    },
    3: {
        "name": "Thủy Lôi Truân", "symbol": "|:::|:", "element": "Thủy/Mộc",
        "general": "Gian nan lúc đầu, vạn sự khởi đầu nan. Mầm non mới nhú gặp bão tuyết.",
        "fortune": "Hung trước Cát sau. Cần kiên nhẫn chờ thời.",
        "wish": "Khó khăn, trắc trở, chưa thành ngay được.",
        "love": "Nhiều sóng gió, hiểu lầm, gia đình ngăn cản.",
        "family": "Bất hòa, lo lắng.",
        "sickness": "Bệnh về thận, bàng quang, chân.",
        "lost_item": "Bị che lấp, khó tìm. Hướng Bắc hoặc Đông.",
        "career": "Khởi nghiệp gian nan, cần người dẫn dắt."
    },
    4: {
        "name": "Sơn Thủy Mông", "symbol": ":|:::|", "element": "Thổ/Thủy",
        "general": "Mờ mịt, chưa rõ ràng, ngu ngơ. Cần được giáo dục, chỉ dẫn.",
        "fortune": "Trung bình. Đừng làm gì khi chưa hiểu rõ.",
        "wish": "Mơ hồ, không thực tế.",
        "love": "Tình cảm chưa chín chắn, dễ bị lừa dối.",
        "family": "Thiếu sự thấu hiểu.",
        "sickness": "Bệnh do ăn uống, trúng độc, tai mũi họng.",
        "lost_item": "Bị giấu kỹ, tìm ở gần núi hoặc nơi ẩm ướt.",
        "career": "Cần học hỏi thêm, chưa đủ sức đảm đương."
    },
    5: {
        "name": "Thủy Thiên Nhu", "symbol": ":|:|||", "element": "Thủy/Kim",
        "general": "Chờ đợi, ăn uống tiệc tùng. Nhu thuận để chờ thời cơ.",
        "fortune": "Cần kiên nhẫn. Nóng vội sẽ hỏng việc.",
        "wish": "Chưa đến lúc, chờ đợi sẽ có kết quả.",
        "love": "Cần thời gian tìm hiểu, đừng ép buộc.",
        "family": "Bình yên nhưng có sự trì trệ.",
        "sickness": "Bệnh tiêu hóa, phù nề, ăn uống quá độ.",
        "lost_item": "Sẽ tìm thấy sau một thời gian.",
        "career": "Chờ cơ hội, đừng chuyển việc lúc này."
    },
    6: {
        "name": "Thiên Thủy Tụng", "symbol": "|||:|:", "element": "Kim/Thủy",
        "general": "Tranh chấp, kiện tụng, bất đồng quan điểm.",
        "fortune": "Hung. Đề phòng khẩu thiệt thị phi.",
        "wish": "Bị cản trở, tranh cãi.",
        "love": "Cãi vã, bất đồng, dễ chia tay.",
        "family": "Bất hòa, tranh chấp tài sản.",
        "sickness": "Đầu óc căng thẳng, bệnh máu huyết.",
        "lost_item": "Bị người khác lấy hoặc tranh chấp.",
        "career": "Kiện tụng, đồng nghiệp chơi xấu."
    },
    7: {
        "name": "Địa Thủy Sư", "symbol": ":|::::", "element": "Thổ/Thủy",
        "general": "Quân đội, đám đông, chiến tranh. Cần kỷ luật sắt.",
        "fortune": "Có hung hiểm nhưng nếu kỷ luật sẽ thắng.",
        "wish": "Khó khăn, phải đấu tranh mới có.",
        "love": "Phức tạp, có người thứ ba hoặc tình tay ba.",
        "family": "Có tranh chấp nhưng giải quyết được bằng uy quyền.",
        "sickness": "Dịch bệnh lây lan, sốt.",
        "lost_item": "Mất nơi đông người.",
        "career": "Cạnh tranh khốc liệt, quân đội công an tốt."
    },
    8: {
        "name": "Thủy Địa Tỷ", "symbol": "::::|:", "element": "Thủy/Thổ",
        "general": "Thân thiết, giúp đỡ lẫn nhau, hòa hợp.",
        "fortune": "Cát. Có quý nhân phù trợ, bạn bè giúp đỡ.",
        "wish": "Thành công nhờ sự hợp tác.",
        "love": "Tình cảm thắm thiết, xứng đôi vừa lứa.",
        "family": "Hòa thuận, vui vẻ.",
        "sickness": "Mau khỏi nhờ thầy giỏi thuốc hay.",
        "lost_item": "Tìm thấy nhờ người khác chỉ giúp.",
        "career": "Hợp tác làm ăn tốt, ngoại giao thuận lợi."
    },
    9: {
        "name": "Phong Thiên Tiểu Súc", "symbol": "||:|||", "element": "Mộc/Kim",
        "general": "Tích lũy nhỏ, ngăn trở tạm thời. Mây đen kéo đến nhưng chưa mưa.",
        "fortune": "Trung bình. Chỉ nên làm việc nhỏ.",
        "wish": "Chưa thành, bị kìm hãm.",
        "love": "Có chút trục trặc nhỏ, giận hờn vu vơ.",
        "family": "Có bất đồng ý kiến nhưng không lớn.",
        "sickness": "Bệnh hô hấp nhẹ, ngực bụng đầy trướng.",
        "lost_item": "Tìm thấy ở gần, phía Đông Nam.",
        "career": "Chưa thăng tiến ngay, cần tích lũy thêm."
    },
    10: {
        "name": "Thiên Trạch Lý", "symbol": "|||||:", "element": "Kim/Kim",
        "general": "Dẫm lên đuôi hổ. Nguy hiểm nhưng cẩn thận sẽ qua.",
        "fortune": "Có rủi ro. Cần cư xử đúng mực, lễ phép.",
        "wish": "Thành công nếu biết khiêm tốn và tuân thủ quy tắc.",
        "love": "Chênh lệch địa vị, cần khéo léo cư xử.",
        "family": "Nề nếp gia phong.",
        "sickness": "Bệnh phổi, miệng lưỡi, xương khớp.",
        "lost_item": "Khó tìm, hoặc vật nguy hiểm.",
        "career": "Làm việc với người khó tính, cần cẩn trọng."
    },
    11: {
        "name": "Địa Thiên Thái", "symbol": ":::|||", "element": "Thổ/Kim",
        "general": "Thái bình, thông suốt, âm dương giao hòa. Thời vận tốt nhất.",
        "fortune": "Đại cát. Mọi việc thuận lợi.",
        "wish": "Cầu được ước thấy.",
        "love": "Hạnh phúc, hòa hợp tuyệt đối.",
        "family": "Giàu sang, an khang thịnh vượng.",
        "sickness": "Mau lành, sức khỏe dồi dào.",
        "lost_item": "Sẽ tìm thấy, đồ vật còn nguyên vẹn.",
        "career": "Thăng quan tiến chức, kinh doanh phát đạt."
    },
    12: {
        "name": "Thiên Địa Bĩ", "symbol": "|||:::", "element": "Kim/Thổ",
        "general": "Bế tắc, không thông. Tiểu nhân đắc chí, quân tử rút lui.",
        "fortune": "Hung. Mọi việc đình trệ.",
        "wish": "Không thành. Bị cản trở.",
        "love": "Chia ly, không hợp nhau.",
        "family": "Lạnh nhạt, ly tán.",
        "sickness": "Bệnh nặng, tắc nghẽn khí huyết.",
        "lost_item": "Mất hẳn, không tìm được.",
        "career": "Bị chèn ép, giáng chức, thất nghiệp."
    },
    13: {
        "name": "Thiên Hỏa Đồng Nhân", "symbol": "|||||:", "element": "Kim/Hỏa",
        "general": "Cùng người, đoàn kết, hợp tác, đại đồng.",
        "fortune": "Cát. Hợp tác thành công.",
        "wish": "Thành tựu nhờ sức mạnh tập thể.",
        "love": "Tình yêu trong sáng, được mọi người ủng hộ.",
        "family": "Đoàn tụ, vui vẻ.",
        "sickness": "Sốt cao, viêm nhiễm nhưng mau khỏi.",
        "lost_item": "Tìm thấy ở nơi công cộng, sáng sủa.",
        "career": "Hội nhóm, công ty cổ phần phát triển."
    },
    14: {
        "name": "Hỏa Thiên Đại Hữu", "symbol": "|:||||", "element": "Hỏa/Kim",
        "general": "Có lớn, giàu có, thịnh vượng. Mặt trời giữa trưa.",
        "fortune": "Đại cát. Tài lộc dồi dào.",
        "wish": "Thành công rực rỡ.",
        "love": "Hào nhoáng, đối phương điều kiện tốt.",
        "family": "Phú quý, danh giá.",
        "sickness": "Sốt cao, bệnh tim mạch, mắt.",
        "lost_item": "Tìm thấy ở nơi cao, sáng, hướng Nam.",
        "career": "Thành đạt, danh tiếng vang xa."
    },
    15: {
        "name": "Địa Sơn Khiêm", "symbol": ":::|::", "element": "Thổ/Thổ",
        "general": "Khiêm tốn, nhún nhường. Núi dấu dưới đất.",
        "fortune": "Cát. Càng khiêm tốn càng được lợi.",
        "wish": "Thành công chậm nhưng chắc.",
        "love": "Tình cảm chân thành, bền vững.",
        "family": "Kính trên nhường dưới.",
        "sickness": "Bệnh tỳ vị, tiêu hóa mãn tính.",
        "lost_item": "Nằm dưới thấp, bị che lấp.",
        "career": "Thăng tiến nhờ đức độ."
    },
    16: {
        "name": "Lôi Địa Dự", "symbol": "::|:::", "element": "Mộc/Thổ",
        "general": "Vui vẻ, chuẩn bị, dự phòng. Sấm nổ trên đất.",
        "fortune": "Cát. Niềm vui đến bất ngờ.",
        "wish": "Thuận lợi.",
        "love": "Vui vẻ, lãng mạn.",
        "family": "Có hỷ sự, tiệc tùng.",
        "sickness": "Bệnh gan, chấn động thần kinh.",
        "lost_item": "Tìm thấy ở hướng Đông.",
        "career": "Mở rộng kinh doanh, khởi công tốt."
    },
    17: {
        "name": "Trạch Lôi Tùy", "symbol": "|::||:", "element": "Kim/Mộc",
        "general": "Đi theo, tùy tùng, thuận theo thời thế.",
        "fortune": "Bình hòa. Nên theo người khác thì tốt.",
        "wish": "Được như ý nếu không cố chấp.",
        "love": "Người nữ theo người nam, thuận tình.",
        "family": "Hòa thuận.",
        "sickness": "Bệnh lây truyền, di chuyển.",
        "lost_item": "Đã bị mang đi xa, hoặc rơi khi đi đường.",
        "career": "Làm nhân viên tốt, đổi việc theo hướng mới."
    },
    18: {
        "name": "Sơn Phong Cổ", "symbol": "|:::||", "element": "Thổ/Mộc",
        "general": "Đổ nát, hỏng hóc, sự cố. Cần sửa chữa.",
        "fortune": "Hung. Mọi việc đang xuống cấp.",
        "wish": "Không thành, cần sửa sai.",
        "love": "Mối quan hệ độc hại, có sự lừa dối.",
        "family": "Gia đạo suy đồi, con cái hư hỏng.",
        "sickness": "Trúng độc, bệnh di truyền, ký sinh trùng.",
        "lost_item": "Đã hỏng hoặc bị sâu mọt.",
        "career": "Công việc trì trệ, cần cải tổ."
    },
    19: {
        "name": "Địa Trạch Lâm", "symbol": "::||||", "element": "Thổ/Kim",
        "general": "Đến gần, bao quản, lớn mạnh. Giáo dục, cai trị.",
        "fortune": "Cát. Đang đà phát triển.",
        "wish": "Tiến triển tốt.",
        "love": "Tình cảm mặn nồng, quan tâm chăm sóc.",
        "family": "Sum vầy, bảo bọc.",
        "sickness": "Bệnh phụ khoa, tiêu hóa.",
        "lost_item": "Tìm thấy ở gần nước.",
        "career": "Quản lý, giám sát tốt."
    },
    20: {
        "name": "Phong Địa Quan", "symbol": "||||::", "element": "Mộc/Thổ",
        "general": "Quan sát, xem xét, chiêm nghiệm. Gió thổi trên đất.",
        "fortune": "Trung bình. Nên xem xét kỹ trước khi làm.",
        "wish": "Chưa vội được.",
        "love": "Đang tìm hiểu, chưa quyết định.",
        "family": "Nghiêm túc, soi xét lẫn nhau.",
        "sickness": "Bệnh phong, khí huyết kém.",
        "lost_item": "Tìm thấy ở nơi thoáng gió.",
        "career": "Nghiên cứu, đánh giá, kiểm tra."
    },
    21: {
        "name": "Hỏa Lôi Phệ Hạp", "symbol": "|:|::|", "element": "Hỏa/Mộc",
        "general": "Cắn vỡ, hình phạt, răn đe. Cần cương quyết loại bỏ cản trở.",
        "fortune": "Có trở ngại nhưng sẽ vượt qua nếu quyết đoán.",
        "wish": "Phải tranh đấu mới được.",
        "love": "Hay cãi vã, ghen tuông.",
        "family": "Có xích mích, kiện tụng.",
        "sickness": "Đau răng, xương khớp, ăn uống kém.",
        "lost_item": "Bị kẹt ở đâu đó, hoặc bị người lấy.",
        "career": "Pháp luật, thi hành án, cải tổ mạnh."
    },
    22: {
        "name": "Sơn Hỏa Bí", "symbol": "|::::|", "element": "Thổ/Hỏa",
        "general": "Trang trí, văn vẻ, hào nhoáng bên ngoài. Hoàng hôn đẹp nhưng sắp tắt.",
        "fortune": "Tiểu cát. Tốt mã rã đám.",
        "wish": "Được tiếng mà không được miếng.",
        "love": "Lãng mạn nhưng thiếu thực tế.",
        "family": "Bề ngoài vui vẻ, bên trong lo âu.",
        "sickness": "Bệnh ngoài da, tim mạch nhẹ.",
        "lost_item": "Tìm thấy ở nơi có ánh sáng, trang trí đẹp.",
        "career": "Nghệ thuật, quảng cáo, trang trí tốt."
    },
    23: {
        "name": "Sơn Địa Bác", "symbol": ":::::|", "element": "Thổ/Thổ",
        "general": "Bóc mòn, sụp đổ, điêu tàn. Tiểu nhân lộng hành.",
        "fortune": "Đại hung. Không nên làm gì lớn.",
        "wish": "Thất bại.",
        "love": "Bị phản bội, chia ly.",
        "family": "Gia đạo sa sút.",
        "sickness": "Bệnh nặng, cơ thể suy kiệt.",
        "lost_item": "Đã mất hẳn, hoặc bị hỏng nát.",
        "career": "Phá sản, mất chức."
    },
    24: {
        "name": "Địa Lôi Phục", "symbol": "|:::::", "element": "Thổ/Mộc",
        "general": "Trở lại, phục hồi. Dương khí bắt đầu sinh.",
        "fortune": "Cát. Mọi việc dần tốt lên từ đáy.",
        "wish": "Cơ hội thứ hai.",
        "love": "Gương vỡ lại lành, tái hợp.",
        "family": "Đoàn tụ sau xa cách.",
        "sickness": "Bệnh cũ tái phát hoặc đang hồi phục.",
        "lost_item": "Tự nhiên tìm thấy hoặc người cầm trả lại.",
        "career": "Khôi phục vị trí cũ, quay lại nghề cũ."
    },
    25: {
        "name": "Thiên Lôi Vô Vọng", "symbol": "|||::|", "element": "Kim/Mộc",
        "general": "Không xằng bậy, ngây thơ, tai họa bất ngờ (nếu làm bậy).",
        "fortune": "Bình thường nếu giữ đạo lý. Làm sai gặp họa.",
        "wish": "Không nên cưỡng cầu.",
        "love": "Đừng toan tính, hãy chân thành.",
        "family": "Có chuyện bất ngờ xảy ra.",
        "sickness": "Bệnh lạ, tai nạn bất ngờ.",
        "lost_item": "Bị cầm nhầm, khó tìm.",
        "career": "Làm việc chân chính thì bền."
    },
    26: {
        "name": "Sơn Thiên Đại Súc", "symbol": "|:::||", "element": "Thổ/Kim",
        "general": "Tích lũy lớn, chứa đựng, nuôi dưỡng hiền tài.",
        "fortune": "Cát. Tiền tài danh vọng đều có.",
        "wish": "Thành công lớn.",
        "love": "Tình yêu bền vững, gia đình môn đăng hộ đối.",
        "family": "Giàu có, con cái thành đạt.",
        "sickness": "Bệnh tích tụ lâu ngày, khối u.",
        "lost_item": "Ở trong kho, tủ, nơi chứa đồ.",
        "career": "Quản lý kho bãi, ngân hàng, giáo dục."
    },
    27: {
        "name": "Sơn Lôi Di", "symbol": "|::::|", "element": "Thổ/Mộc",
        "general": "Nuôi dưỡng, ăn uống. Cái miệng họa phúc khôn lường.",
        "fortune": "Cát hung tùy lời nói và việc làm.",
        "wish": "Thành công nếu biết chăm sóc, nuôi dưỡng.",
        "love": "Quan tâm chăm sóc nhau qua ăn uống.",
        "family": "Sum họp ăn uống.",
        "sickness": "Bệnh miệng, dạ dày, tiêu hóa.",
        "lost_item": "Tìm ở nhà bếp, phòng ăn.",
        "career": "Ẩm thực, giáo dục, chăn nuôi."
    },
    28: {
        "name": "Trạch Phong Đại Quá", "symbol": ":||||:", "element": "Kim/Mộc",
        "general": "Quá mức, gánh nặng quá lớn. Cột nhà cong vênh.",
        "fortune": "Hung. Áp lực lớn, dễ gãy đổ.",
        "wish": "Quá sức, khó thành.",
        "love": "Tình yêu chênh lệch tuổi tác/địa vị quá lớn.",
        "family": "Gánh vác nợ nần, lo âu.",
        "sickness": "Bệnh nặng, đột quỵ, gan thận.",
        "lost_item": "Bị đè lấp, khó tìm.",
        "career": "Đảm nhận việc quá sức, rủi ro cao."
    },
    29: {
        "name": "Khảm Vi Thủy", "symbol": ":|::|:", "element": "Thủy",
        "general": "Hiểm trở, hãm vào vực sâu. Khó khăn chồng chất.",
        "fortune": "Đại hung. Cẩn thận tai nạn nước lửa.",
        "wish": "Thất bại, gặp nguy hiểm.",
        "love": "Lừa dối, đau khổ, nước mắt.",
        "family": "Chia ly, buồn phiền.",
        "sickness": "Bệnh thận, máu huyết, tai.",
        "lost_item": "Rơi xuống nước/cống, mất hẳn.",
        "career": "Bế tắc, nguy cơ tù tội/phá sản."
    },
    30: {
        "name": "Ly Vi Hỏa", "symbol": "|:|:|:", "element": "Hỏa",
        "general": "Sáng sủa, bám vào, lệ thuộc. Lửa cháy sáng cần nhiên liệu.",
        "fortune": "Trung bình. Tốt nếu biết dựa vào người tài.",
        "wish": "Thành công nhờ sự giúp đỡ.",
        "love": "Nồng nhiệt nhưng dễ tàn, hay ghen.",
        "family": "Vẻ vang nhưng nội bộ nóng nảy.",
        "sickness": "Bệnh mắt, tim mạch, sốt cao.",
        "lost_item": "Tìm thấy ở hướng Nam, nơi sáng.",
        "career": "Văn hóa, nghệ thuật, cần người đỡ đầu."
    },
    31: {
        "name": "Trạch Sơn Hàm", "symbol": ":||::|", "element": "Kim/Thổ",
        "general": "Cảm ứng, rung động, trai gái tìm hiểu nhau.",
        "fortune": "Cát. Nhân duyên tốt.",
        "wish": "Thành công nhanh chóng.",
        "love": "Tình yêu sét đánh, cưới xin thuận lợi.",
        "family": "Hòa thuận, vui vẻ.",
        "sickness": "Bệnh lây nhiễm, cảm cúm, chân.",
        "lost_item": "Tìm thấy nhờ linh tính mách bảo.",
        "career": "Ngoại giao, tiếp thị, nghệ thuật."
    },
    32: {
        "name": "Lôi Phong Hằng", "symbol": "::|||:", "element": "Mộc/Mộc",
        "general": "Lâu dài, bền vững, kiên định. Vợ chồng già.",
        "fortune": "Cát. Lợi về lâu dài.",
        "wish": "Thành công nhưng cần kiên trì.",
        "love": "Bền lâu, gắn bó keo sơn.",
        "family": "Ổn định, bình an.",
        "sickness": "Bệnh mãn tính, dai dẳng.",
        "lost_item": "Tìm thấy ở chỗ cũ, không mất đi đâu.",
        "career": "Công việc ổn định, thâm niên cao."
    },
    # [Tiếp tục bổ sung các quẻ còn lại để đảm bảo đủ 64 quẻ cho AI]
}

# Bổ sung mapping nhanh cho các quẻ còn lại để tránh lỗi key
DEFAULT_HEX = {"name": "Chưa xác định", "general": "Đang cập nhật...", "fortune": "Bình", "element": "Thổ"}
for i in range(1, 65):
    if i not in ICHING_HEXAGRAMS:
        ICHING_HEXAGRAMS[i] = DEFAULT_HEX

LUC_THAN_MEANINGS = {
    "Huynh Đệ": {
        "general": "Anh em, bạn bè, đồng nghiệp. Cạnh tranh, tốn tiền.",
        "wealth": "Khắc Thê Tài -> Hao tài, mất tiền, bị lừa gạt.",
        "career": "Cạnh tranh gay gắt, tiểu nhân cản trở.",
        "love": "Kẻ thứ ba chen ngang, bạn bè phản đối.",
        "health": "Tốt cho sức khỏe (khắc Quan Quỷ).",
        "lost_item": "Khó tìm, bị người quen cầm."
    },
    "Tử Tôn": {
        "general": "Con cái, phúc đức, giải thần. Vui vẻ, hưởng thụ.",
        "wealth": "Sinh Thê Tài -> Nguồn tiền, khách hàng, lợi nhuận.",
        "career": "Khắc Quan Quỷ -> Mất chức, thất nghiệp, muốn nghỉ hưu/đổi nghề.",
        "love": "Con cái, tình dục, vui chơi.",
        "health": "Thuốc hay thầy giỏi, giải trừ bệnh tật.",
        "lost_item": "Dễ tìm, vật còn nguyên."
    },
    "Thê Tài": {
        "general": "Vợ, tiền bạc, tài sản, người làm.",
        "wealth": "Tiền vào, lợi nhuận, lương bổng.",
        "career": "Sinh Quan Quỷ -> Dùng tiền mua danh, đầu tư cho công việc.",
        "love": "Vợ, người yêu nữ. Tình cảm mặn nồng.",
        "health": "Ăn uống tốt, nhưng coi chừng bệnh do ăn chơi.",
        "lost_item": "Vật có giá trị, tìm thấy ở bếp/kho."
    },
    "Quan Quỷ": {
        "general": "Công danh, chức vụ, chồng. Tai họa, bệnh tật, ma quỷ.",
        "wealth": "Hao tốn (Khắc Huynh Đệ - cướp tiền của Huynh Đệ? Không, Quan Quỷ khắc Huynh Đệ là bảo vệ Tài. Nhưng Quan Quỷ tiết khí Tài -> Tốn tiền cho danh vọng).",
        "career": "Thăng chức, quyền lực, nổi tiếng.",
        "love": "Chồng, người yêu nam. Áp lực trong tình cảm.",
        "health": "Bệnh tật, tai nạn, vong ám.",
        "lost_item": "Mất hẳn, bị trộm cắp.",
        "legal": "Kiện tụng, rắc rối pháp luật."
    },
    "Phụ Mẫu": {
        "general": "Cha mẹ, giấy tờ, nhà cửa, xe cộ, tin tức.",
        "wealth": "Khắc Tử Tôn -> Chặn đường làm ăn, vất vả, lao tâm khổ tứ.",
        "career": "Hợp đồng, bằng cấp, dự án, sự bảo trợ.",
        "love": "Đăng ký kết hôn, cha mẹ hai bên (thường ngăn cản hoặc lo lắng).",
        "health": "Thuốc men, sự chăm sóc (nhưng khắc Tử Tôn -> thuốc không hợp?).",
        "lost_item": "Quần áo, giấy tờ. Tìm ở phòng khách/thư phòng."
    }
}

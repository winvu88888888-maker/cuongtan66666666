"""
QMDG KNOWLEDGE COMPLETE - Bộ Tri Thức Siêu Chi Tiết
Bao gồm: Kỳ Môn Độn Giáp, Mai Hoa Dịch Số, Kinh Dịch
"""

# ============================================================
# PHẦN 1: CỬU CUNG (9 CUNG) - CHI TIẾT
# ============================================================

CUU_CUNG = {
    1: {
        "Ten": "Khảm Cung", "Quai": "Khảm", "Ngu_Hanh": "Thủy",
        "Huong": "Bắc", "Mau_Sac": "Đen, Xanh dương đậm",
        "Than_The": "Thận, Tai, Máu, Bộ phận sinh dục",
        "Nguoi": "Con trai giữa, đàn ông trung niên (30-45)",
        "Tuong": "Nước, ao hồ, sông, mưa, trộm cắp, gian lận, hiểm nguy",
        "Tinh_Cach": "Thông minh, mưu mô, lén lút, hay lo lắng",
        "Vat": "Đồ lỏng, rượu bia, mực, cá, lợn",
        "Noi": "Nhà vệ sinh, hầm, nơi có nước, bar, quán nhậu",
        "So": 1, "Sac_Thai": "Âm, lạnh, ẩm ướt"
    },
    2: {
        "Ten": "Khôn Cung", "Quai": "Khôn", "Ngu_Hanh": "Thổ",
        "Huong": "Tây Nam", "Mau_Sac": "Vàng, Nâu",
        "Than_The": "Bụng, Dạ dày, Da thịt, Tỳ",
        "Nguoi": "Mẹ, bà ngoại, phụ nữ lớn tuổi, người hầu",
        "Tuong": "Đất, đồng ruộng, thuận theo, hiền lành, nhu mì",
        "Tinh_Cach": "Nhu thuận, cần kiệm, chậm chạp, tham lam",
        "Vat": "Vải vóc, đồ gốm, ngũ cốc, bò, thóc lúa",
        "Noi": "Nhà cấp 4, đất trống, đồng ruộng, kho chứa",
        "So": 2, "Sac_Thai": "Âm, thuần, thấp"
    },
    3: {
        "Ten": "Chấn Cung", "Quai": "Chấn", "Ngu_Hanh": "Mộc",
        "Huong": "Đông", "Mau_Sac": "Xanh lá, Xanh lục",
        "Than_The": "Chân, Gan, Tóc, Thanh quản",
        "Nguoi": "Con trai cả, thanh niên (18-35), người vội vã",
        "Tuong": "Sấm sét, động đất, tiếng nổ, sự bắt đầu, phấn khích",
        "Tinh_Cach": "Năng động, nóng vội, quyết đoán, hay giật mình",
        "Vat": "Đồ gỗ, cây cối, xe cộ, nhạc cụ, tre trúc",
        "Noi": "Chợ, nơi đông người, rừng, đường lớn",
        "So": 3, "Sac_Thai": "Dương, động, nhanh"
    },
    4: {
        "Ten": "Tốn Cung", "Quai": "Tốn", "Ngu_Hanh": "Mộc",
        "Huong": "Đông Nam", "Mau_Sac": "Xanh lá nhạt",
        "Than_The": "Đùi, Thần kinh, Tóc, Mật",
        "Nguoi": "Con gái cả, phụ nữ trẻ (20-35), người tu hành",
        "Tuong": "Gió, khí, thông tin, tin đồn, thuận theo, thương mại",
        "Tinh_Cach": "Khéo léo, ngoại giao, hay thay đổi, thiếu quyết đoán",
        "Vat": "Gỗ dài, thừng dây, lông gà, thư từ, giấy tờ",
        "Noi": "Văn phòng, bưu điện, công viên, nơi cao, chùa",
        "So": 4, "Sac_Thai": "Âm Mộc, mềm mỏng"
    },
    5: {
        "Ten": "Trung Cung", "Quai": "Trung Cung", "Ngu_Hanh": "Thổ",
        "Huong": "Trung tâm (Tại chỗ)", "Mau_Sac": "Vàng đất",
        "Than_The": "Tỳ Vị, Trung tâm cơ thể",
        "Nguoi": "Chính mình, người trung gian, trọng tâm vấn đề",
        "Tuong": "Tâm điểm, sự cân bằng, không xác định rõ, biến hóa",
        "Tinh_Cach": "Trung dung, khó xác định, hay thay đổi",
        "Vat": "Đồ đất, ngũ cốc, vật trung tính",
        "Noi": "Trong nhà, nơi quen thuộc, trung tâm thành phố",
        "So": 5, "Sac_Thai": "Trung Thổ, biến"
    },
    6: {
        "Ten": "Càn Cung", "Quai": "Càn", "Ngu_Hanh": "Kim",
        "Huong": "Tây Bắc", "Mau_Sac": "Trắng, Vàng kim",
        "Than_The": "Đầu, Phổi, Xương, Da",
        "Nguoi": "Cha, ông nội, đàn ông lớn tuổi (>50), lãnh đạo, vua",
        "Tuong": "Trời, quyền lực, kim loại quý, kiên cố, cứng rắn",
        "Tinh_Cach": "Mạnh mẽ, quyết đoán, uy nghiêm, cứng nhắc",
        "Vat": "Vàng bạc, kim loại, đá quý, đồng hồ, xe sang",
        "Noi": "Tòa nhà cao, cơ quan nhà nước, đền chùa, nơi cao quý",
        "So": 6, "Sac_Thai": "Dương Kim, cứng, cao"
    },
    7: {
        "Ten": "Đoài Cung", "Quai": "Đoài", "Ngu_Hanh": "Kim",
        "Huong": "Tây", "Mau_Sac": "Trắng",
        "Than_The": "Miệng, Răng, Phổi, Lưỡi",
        "Nguoi": "Con gái út, thiếu nữ (<25), ca sĩ, thầy bói",
        "Tuong": "Đầm, hồ, vui vẻ, nói cười, ca hát, ăn uống",
        "Tinh_Cach": "Vui vẻ, khéo ăn nói, hay cười, thích ăn diện",
        "Vat": "Đồ kim loại nhỏ, nhạc cụ, gương, dao kéo",
        "Noi": "Quán xá, karaoke, hồ nước, nơi giải trí",
        "So": 7, "Sac_Thai": "Âm Kim, mềm, vui"
    },
    8: {
        "Ten": "Cấn Cung", "Quai": "Cấn", "Ngu_Hanh": "Thổ",
        "Huong": "Đông Bắc", "Mau_Sac": "Vàng, Nâu",
        "Than_The": "Tay, Lưng, Mũi, Ngón tay",
        "Nguoi": "Con trai út, trẻ em, thanh niên (<25), thầy tu",
        "Tuong": "Núi, dừng lại, cố chấp, trì trệ, yên tĩnh",
        "Tinh_Cach": "Ít nói, cứng đầu, bền bỉ, chậm chạp, trung thực",
        "Vat": "Đá, núi, cửa, vật nhỏ gọn, chó",
        "Noi": "Núi đồi, cửa hàng, nhà ở, kho bãi, chùa",
        "So": 8, "Sac_Thai": "Thiếu Thổ, tĩnh, dừng"
    },
    9: {
        "Ten": "Ly Cung", "Quai": "Ly", "Ngu_Hanh": "Hỏa",
        "Huong": "Nam", "Mau_Sac": "Đỏ, Cam, Tím",
        "Than_The": "Mắt, Tim, Máu, Tiểu trường",
        "Nguoi": "Con gái giữa, phụ nữ trung niên (30-45), văn sĩ",
        "Tuong": "Lửa, ánh sáng, văn minh, danh vọng, sự rực rỡ",
        "Tinh_Cach": "Thông minh, sáng tạo, nóng tính, hay nói",
        "Vat": "Đèn, lửa, sách vở, tranh ảnh, chim chóc",
        "Noi": "Trường học, nhà hàng, nhà bếp, nơi nóng, phương Nam",
        "So": 9, "Sac_Thai": "Âm Hỏa, sáng, nóng"
    }
}

# ============================================================
# PHẦN 2: CỬU TINH (9 SAO) - CHI TIẾT
# ============================================================

CUU_TINH = {
    "Thiên Bồng": {
        "Ngu_Hanh": "Thủy", "Cung_Goc": 1, "Cat_Hung": "Hung Tinh",
        "Tuong": "Tướng quân, trộm cướp, đầu lĩnh",
        "Nguoi": "Kẻ trộm, đạo tặc, thủy thủ, ngư dân",
        "Tinh_Cach": "Dũng mãnh, mưu mô, hung hãn, thích mạo hiểm",
        "Viec_Tot": "Đánh giặc, bắt trộm, đi biển, mưu lược",
        "Viec_Xau": "Trộm cắp, cướp bóc, lừa đảo",
        "Benh": "Bệnh thận, bệnh đường tiết niệu",
        "Tim_Do": "Kẻ lấy có thể là trộm chuyên nghiệp, đi đêm"
    },
    "Thiên Nhuế": {
        "Ngu_Hanh": "Thổ", "Cung_Goc": 2, "Cat_Hung": "Hung Tinh",
        "Tuong": "Bệnh tật, thầy thuốc, nữ nhân",
        "Nguoi": "Thầy thuốc, bà đỡ, người bệnh, nông dân",
        "Tinh_Cach": "Chậm chạp, thích giúp đỡ, hay lo lắng",
        "Viec_Tot": "Chữa bệnh, y học, nông nghiệp",
        "Viec_Xau": "Kiện tụng, đi xa, mọi việc trì trệ",
        "Benh": "Bệnh tiêu hóa, bệnh da liễu",
        "Tim_Do": "Đồ ở gần, có thể trong nhà người quen"
    },
    "Thiên Xung": {
        "Ngu_Hanh": "Mộc", "Cung_Goc": 3, "Cat_Hung": "Bình",
        "Tuong": "Quân sự, cạnh tranh, xung đột",
        "Nguoi": "Lính tráng, vận động viên, người năng động",
        "Tinh_Cach": "Năng động, nóng vội, hay tranh cãi",
        "Viec_Tot": "Thể thao, thi đấu, cạnh tranh",
        "Viec_Xau": "Đánh nhau, cãi vã, tai nạn",
        "Benh": "Đau chân, đau gan",
        "Tim_Do": "Đồ có thể bị di chuyển nhanh, ở nơi đông người"
    },
    "Thiên Phụ": {
        "Ngu_Hanh": "Mộc", "Cung_Goc": 4, "Cat_Hung": "Cát Tinh",
        "Tuong": "Văn chương, học thuật, gió, thông tin",
        "Nguoi": "Thầy giáo, văn sĩ, nhà báo, người tu hành",
        "Tinh_Cach": "Nho nhã, hiền lành, thích học hỏi",
        "Viec_Tot": "Học tập, thi cử, viết lách, xuất bản",
        "Viec_Xau": "Tin đồn thất thiệt",
        "Benh": "Đau thần kinh, cảm gió",
        "Tim_Do": "Đồ có thể trong tài liệu, nơi có sách vở"
    },
    "Thiên Cầm": {
        "Ngu_Hanh": "Thổ", "Cung_Goc": 5, "Cat_Hung": "Đại Cát",
        "Tuong": "Trung tâm, lãnh đạo, đế vương, cân bằng",
        "Nguoi": "Vua chúa, lãnh đạo cao nhất, người quyền lực",
        "Tinh_Cach": "Uy nghiêm, công bằng, toàn diện",
        "Viec_Tot": "Mọi việc lớn, quyết định quan trọng",
        "Viec_Xau": "Không có (trừ khi gặp Phục Ngâm)",
        "Benh": "Bệnh ở trung tâm cơ thể",
        "Tim_Do": "Đồ ngay trong nhà, tại chỗ, không bị mất"
    },
    "Thiên Tâm": {
        "Ngu_Hanh": "Kim", "Cung_Goc": 6, "Cat_Hung": "Đại Cát",
        "Tuong": "Mưu lược, thầy thuốc, y học, đền chùa",
        "Nguoi": "Bác sĩ giỏi, quân sư, người có mưu",
        "Tinh_Cach": "Thông minh, mưu lược, bí ẩn, hay giúp người",
        "Viec_Tot": "Chữa bệnh, mưu kế, tìm quý nhân",
        "Viec_Xau": "Không tốt cho kẻ gian",
        "Benh": "Đau đầu, đau xương",
        "Tim_Do": "Đồ có thể được người tốt bụng giữ, dễ tìm lại"
    },
    "Thiên Trụ": {
        "Ngu_Hanh": "Kim", "Cung_Goc": 7, "Cat_Hung": "Hung Tinh",
        "Tuong": "Phá hoại, mưa gió, khẩu thiệt",
        "Nguoi": "Thầy bói, luật sư, người hay nói",
        "Tinh_Cach": "Hay phá phách, nói nhiều, thích tranh cãi",
        "Viec_Tot": "Kiện tụng (nếu đúng), phá vỡ điều xấu",
        "Viec_Xau": "Miệng lưỡi, thị phi, mất của",
        "Benh": "Đau miệng, đau răng, đau phổi",
        "Tim_Do": "Đồ bị người nhiều mồm giữ, có thể bị bán"
    },
    "Thiên Nhậm": {
        "Ngu_Hanh": "Thổ", "Cung_Goc": 8, "Cat_Hung": "Cát Tinh",
        "Tuong": "Núi, đất đai, bất động sản, ổn định",
        "Nguoi": "Người làm ruộng, người tu hành, trẻ em",
        "Tinh_Cach": "Trung thực, chậm rãi, đáng tin cậy",
        "Viec_Tot": "Mua nhà đất, xây dựng, ổn định",
        "Viec_Xau": "Chậm tiến, trì trệ",
        "Benh": "Đau tay, đau lưng",
        "Tim_Do": "Đồ ở yên một chỗ, gần núi đồi hoặc trong nhà"
    },
    "Thiên Anh": {
        "Ngu_Hanh": "Hỏa", "Cung_Goc": 9, "Cat_Hung": "Hung Tinh",
        "Tuong": "Lửa, ánh sáng, hỏa hoạn, danh vọng",
        "Nguoi": "Văn nhân, người nổi tiếng, người đỏ mắt",
        "Tinh_Cach": "Nóng nảy, hay nói, thích nổi tiếng",
        "Viec_Tot": "Văn chương, thể hiện, phát sáng",
        "Viec_Xau": "Hỏa hoạn, tranh cãi, thị phi",
        "Benh": "Đau mắt, đau tim, sốt",
        "Tim_Do": "Đồ có thể bị cháy hỏng, ở phương Nam"
    }
}

# ============================================================
# PHẦN 3: BÁT MÔN (8 CỬA) - CHI TIẾT
# ============================================================

BAT_MON = {
    "Khai Môn": {
        "Ngu_Hanh": "Kim", "Cung_Goc": 6, "Cat_Hung": "Đại Cát",
        "Tuong": "Mở cửa, sự nghiệp, quan chức, khởi đầu",
        "Y_Nghia": "Mở đường, thuận lợi, công việc suôn sẻ",
        "Viec_Tot": "Khai trương, xin việc, thăng chức, xuất hành",
        "Viec_Xau": "Ẩn náu, trốn tránh (vì quá sáng)",
        "Tim_Do": "Cao, có thể tìm lại, ở nơi công cộng"
    },
    "Hưu Môn": {
        "Ngu_Hanh": "Thủy", "Cung_Goc": 1, "Cat_Hung": "Cát",
        "Tuong": "Nghỉ ngơi, yên ổn, quý nhân, phúc lộc",
        "Y_Nghia": "Nghỉ ngơi, gặp quý nhân, an lành",
        "Viec_Tot": "Nghỉ ngơi, gặp quý nhân, cầu phúc, du lịch",
        "Viec_Xau": "Việc cần nhanh (vì chậm)",
        "Tim_Do": "Cao, đồ đang yên, chưa bị di chuyển xa"
    },
    "Sinh Môn": {
        "Ngu_Hanh": "Thổ", "Cung_Goc": 8, "Cat_Hung": "Đại Cát",
        "Tuong": "Sinh sôi, tài lộc, kinh doanh, nhà cửa",
        "Y_Nghia": "Tài lộc, sinh lợi, phát triển",
        "Viec_Tot": "Kinh doanh, cầu tài, mua nhà, sinh con",
        "Viec_Xau": "Kiện tụng (vì hòa khí)",
        "Tim_Do": "Rất cao, đồ còn nguyên vẹn, dễ tìm"
    },
    "Thương Môn": {
        "Ngu_Hanh": "Mộc", "Cung_Goc": 3, "Cat_Hung": "Hung",
        "Tuong": "Tổn thương, cãi vã, săn bắt, đòi nợ",
        "Y_Nghia": "Có tổn thương, tranh chấp, mất mát",
        "Viec_Tot": "Đòi nợ, bắt trộm, săn bắn, kiện tụng",
        "Viec_Xau": "Mọi việc khác (gặp hung)",
        "Tim_Do": "Thấp, đồ có thể bị hỏng hoặc bán đi"
    },
    "Đỗ Môn": {
        "Ngu_Hanh": "Mộc", "Cung_Goc": 4, "Cat_Hung": "Bình",
        "Tuong": "Cửa đóng, ẩn náu, bí mật, kỹ thuật",
        "Y_Nghia": "Ẩn náu, phòng thủ, giấu kín",
        "Viec_Tot": "Ẩn náu, tu hành, làm việc bí mật, kỹ thuật",
        "Viec_Xau": "Xuất hành, mở cửa, giao tiếp",
        "Tim_Do": "Trung bình, đồ bị giấu kín trong góc"
    },
    "Cảnh Môn": {
        "Ngu_Hanh": "Hỏa", "Cung_Goc": 9, "Cat_Hung": "Bình",
        "Tuong": "Cảnh đẹp, văn thư, yến tiệc, sáng sủa",
        "Y_Nghia": "Rực rỡ, danh vọng, văn bản, công khai",
        "Viec_Tot": "Văn thư, thi cử, yến tiệc, giảng dạy",
        "Viec_Xau": "Việc cần bí mật",
        "Tim_Do": "Trung bình, đồ có thể đổi chủ, cần tìm nhanh"
    },
    "Tử Môn": {
        "Ngu_Hanh": "Thổ", "Cung_Goc": 2, "Cat_Hung": "Đại Hung",
        "Tuong": "Cái chết, kết thúc, tang tóc, dừng lại",
        "Y_Nghia": "Kết thúc, chấm dứt, bế tắc hoàn toàn",
        "Viec_Tot": "Mai táng, chấm dứt việc xấu, kết thúc",
        "Viec_Xau": "Mọi việc sống (cực kỳ xấu)",
        "Tim_Do": "Rất thấp, đồ có thể mất vĩnh viễn hoặc hủy"
    },
    "Kinh Môn": {
        "Ngu_Hanh": "Kim", "Cung_Goc": 7, "Cat_Hung": "Hung",
        "Tuong": "Sợ hãi, kinh hoàng, kiện tụng, cãi vã",
        "Y_Nghia": "Có chuyện đáng sợ, lo lắng, tranh chấp",
        "Viec_Tot": "Kiện tụng chính đáng, báo động, cảnh giác",
        "Viec_Xau": "Mọi việc bình thường",
        "Tim_Do": "Thấp, đồ bị di chuyển xa, khó lấy lại"
    }
}

# ============================================================
# PHẦN 4: BÁT THẦN (8 THẦN) - CHI TIẾT
# ============================================================

BAT_THAN = {
    "Trực Phù": {
        "Tinh_Chat": "Đại Cát", "Chu_Te": "Quý nhân tối cao, thần che chở",
        "Tuong": "Lãnh đạo, người có quyền lực, uy tín cao nhất",
        "Nguoi": "Sếp lớn, quan chức, người có thế lực",
        "Y_Nghia": "Được quý nhân phù trợ, mọi việc hanh thông",
        "Tim_Do": "Có người quyền lực giữ, có thể nhờ cấp trên giúp"
    },
    "Đằng Xà": {
        "Tinh_Chat": "Hung", "Chu_Te": "Quái dị, biến hóa, ác mộng",
        "Tuong": "Rắn, sự biến đổi kỳ lạ, lừa dối, thần quỷ",
        "Nguoi": "Kẻ lừa đảo, người ma quái, hay thay đổi",
        "Y_Nghia": "Có điều quái lạ, bị lừa gạt, ác mộng",
        "Tim_Do": "Kẻ lấy hay thay đổi hình dạng, khó xác định giới tính"
    },
    "Thái Âm": {
        "Tinh_Chat": "Cát", "Chu_Te": "Ẩn tàng, mưu kế, nữ quý nhân",
        "Tuong": "Mặt trăng, sự ẩn giấu, người phụ nữ giúp đỡ",
        "Nguoi": "Nữ quý nhân, người giúp đỡ ngấm ngầm",
        "Y_Nghia": "Được giúp đỡ kín đáo, có mưu kế hay",
        "Tim_Do": "Có người phụ nữ biết, hỏi phụ nữ sẽ tìm được"
    },
    "Lục Hợp": {
        "Tinh_Chat": "Cát", "Chu_Te": "Hợp tác, hôn nhân, đoàn kết",
        "Tuong": "Sự hòa hợp, kết nối, trung gian, mai mối",
        "Nguoi": "Mai mối, môi giới, người trung gian",
        "Y_Nghia": "Sự hợp tác thành công, hôn nhân tốt đẹp",
        "Tim_Do": "Có thể nhờ người trung gian tìm, đồ ở nơi có cặp đôi"
    },
    "Bạch Hổ": {
        "Tinh_Chat": "Đại Hung", "Chu_Te": "Máu huyết, tai nạn, binh khí",
        "Tuong": "Hổ trắng, chiến tranh, hình phạt, thương tích",
        "Nguoi": "Kẻ cướp, người võ lực, quân nhân, đồ tể",
        "Y_Nghia": "Có tai nạn, mất máu, bị phạt, hung bạo",
        "Tim_Do": "Kẻ lấy là đàn ông hung hãn, có thể dùng vũ lực"
    },
    "Huyền Vũ": {
        "Tinh_Chat": "Hung", "Chu_Te": "Trộm cắp, lừa dối, ám muội",
        "Tuong": "Rùa đen, sự tối tăm, mờ ám, tiểu nhân",
        "Nguoi": "Kẻ trộm, người lừa đảo, tiểu nhân lén lút",
        "Y_Nghia": "Bị trộm cắp, lừa dối, có điều mờ ám",
        "Tim_Do": "KẺ TRỘM CHUYÊN NGHIỆP, đàn ông hay đi đêm"
    },
    "Cửu Địa": {
        "Tinh_Chat": "Cát", "Chu_Te": "Đất mẹ, ổn định, ẩn náu",
        "Tuong": "Đất, sự vững chãi, phòng thủ, chậm rãi",
        "Nguoi": "Người già, người bảo thủ, người làm ruộng",
        "Y_Nghia": "Ổn định, có lợi cho phòng thủ, ẩn náu",
        "Tim_Do": "Đồ chôn dưới đất hoặc trong nhà kho"
    },
    "Cửu Thiên": {
        "Tinh_Chat": "Cát", "Chu_Te": "Trời cao, bay bổng, hành động",
        "Tuong": "Bầu trời, sự cao xa, tiến công, hoạt động",
        "Nguoi": "Người hoạt động, phi công, người năng động",
        "Y_Nghia": "Có lợi cho hành động, tiến công, bay cao",
        "Tim_Do": "Đồ ở nơi cao hoặc đã bị mang đi xa"
    }
}

# ============================================================
# PHẦN 5: THẬP THIÊN CAN - CHI TIẾT
# ============================================================

THAP_THIEN_CAN = {
    "Giáp": {
        "Ngu_Hanh": "Dương Mộc", "Tuong": "Cây lớn, nguyên soái, lãnh đạo",
        "Nguoi": "Người đứng đầu, thủ lĩnh, người chính trực",
        "Tinh_Cach": "Mạnh mẽ, thẳng thắn, hay ẩn náu",
        "Than_The": "Đầu, gan, thần kinh",
        "Gioi_Tinh": "Dương - ĐÀN ÔNG lớn tuổi, lãnh đạo",
        "Vat": "Cây to, đồ gỗ lớn, tháp",
        "Lien_Quan": "Giáp luôn ẩn tàng, hiếm khi lộ diện"
    },
    "Ất": {
        "Ngu_Hanh": "Âm Mộc", "Tuong": "Cây nhỏ, hoa cỏ, thảo mộc",
        "Nguoi": "PHỤ NỮ trẻ, thầy thuốc, người mềm mỏng",
        "Tinh_Cach": "Mềm mại, uốn éo, khéo léo, hay thay đổi",
        "Than_The": "Cổ, gan, cơ bắp",
        "Gioi_Tinh": "Âm - PHỤ NỮ, nữ giới, người mềm mỏng",
        "Vat": "Thảo dược, hoa, rau, đồ gỗ nhỏ",
        "Lien_Quan": "Ất = Nữ trong hôn nhân, thuốc trong y học"
    },
    "Bính": {
        "Ngu_Hanh": "Dương Hỏa", "Tuong": "Mặt trời, ánh sáng lớn",
        "Nguoi": "Người hoạt bát, hay di chuyển, lính",
        "Tinh_Cach": "Nóng bỏng, rực rỡ, công khai, thẳng thắn",
        "Than_The": "Vai, tim, mắt trái",
        "Gioi_Tinh": "Dương - NAM hoặc NỮ trẻ năng động",
        "Vat": "Lửa to, đèn sáng, mặt trời, bếp lò",
        "Lien_Quan": "Bính = Ánh sáng, sự rõ ràng, công khai"
    },
    "Đinh": {
        "Ngu_Hanh": "Âm Hỏa", "Tuong": "Ngọn nến, lửa nhỏ, tinh tế",
        "Nguoi": "PHỤ NỮ thông minh, trí thức, văn nhân",
        "Tinh_Cach": "Tinh tế, thông minh, bí ẩn, khéo léo",
        "Than_The": "Tim, lưỡi, mắt phải",
        "Gioi_Tinh": "Âm - PHỤ NỮ thông minh, khéo léo",
        "Vat": "Nến, bật lửa, văn bản, giấy tờ",
        "Lien_Quan": "Đinh = Văn bản, thông tin bí mật"
    },
    "Mậu": {
        "Ngu_Hanh": "Dương Thổ", "Tuong": "Núi lớn, đất lớn, thành lũy",
        "Nguoi": "ĐÀN ÔNG trung thực, chắc chắn, to lớn",
        "Tinh_Cach": "Trung thực, ổn định, mạnh mẽ, thô",
        "Than_The": "Dạ dày, cơ bắp lớn, xương",
        "Gioi_Tinh": "Dương - ĐÀN ÔNG to, mập mạp, trung thực",
        "Vat": "Đất thịt, núi, thành, tiền vốn",
        "Lien_Quan": "Mậu = Tiền vốn, tài sản cố định"
    },
    "Kỷ": {
        "Ngu_Hanh": "Âm Thổ", "Tuong": "Đất ruộng, đất ẩm, vườn",
        "Nguoi": "PHỤ NỮ xấu tính, người gian, tiểu nhân",
        "Tinh_Cach": "Ẩm ướt, hay ẩn giấu, gian xảo, tiểu nhân",
        "Than_The": "Ruột, bụng, da thịt",
        "Gioi_Tinh": "Âm - PHỤ NỮ xấu tính, hay gian lận",
        "Vat": "Đất ruộng, phân bón, đồ dơ bẩn",
        "Lien_Quan": "Kỷ = Sự ẩn giấu, dâm dục, bệnh tật"
    },
    "Canh": {
        "Ngu_Hanh": "Dương Kim", "Tuong": "Kim loại lớn, vũ khí, đường xá",
        "Nguoi": "ĐÀN ÔNG cứng rắn, hung dữ, quân nhân, đối thủ",
        "Tinh_Cach": "Cứng rắn, quyết đoán, hung hăng, trở ngại",
        "Than_The": "Phổi, xương, răng, da",
        "Gioi_Tinh": "Dương - ĐÀN ÔNG mạnh, cứng rắn, hung dữ",
        "Vat": "Dao, kiếm, xe cộ, kim loại lớn",
        "Lien_Quan": "Canh = Đối thủ, trở ngại, kẻ thù"
    },
    "Tân": {
        "Ngu_Hanh": "Âm Kim", "Tuong": "Kim loại nhỏ, trang sức, dao nhỏ",
        "Nguoi": "Phụ nữ xinh đẹp, thợ kim hoàn, người lỗi lầm",
        "Tinh_Cach": "Tinh tế, sắc bén, hay phạm lỗi",
        "Than_The": "Răng, móng tay, xương nhỏ",
        "Gioi_Tinh": "Âm - Có thể nam hoặc nữ, hay phạm lỗi",
        "Vat": "Nhẫn, vàng bạc nhỏ, dao kéo, kim khí nhỏ",
        "Lien_Quan": "Tân = Sai lầm, tội lỗi, đổi mới"
    },
    "Nhâm": {
        "Ngu_Hanh": "Dương Thủy", "Tuong": "Sông lớn, biển, nước chảy",
        "Nguoi": "ĐÀN ÔNG trộm cắp, thủy thủ, người hay đi đêm",
        "Tinh_Cach": "Hay di chuyển, mưu mô, trộm cắp, lưu động",
        "Than_The": "Bàng quang, hệ tiết niệu",
        "Gioi_Tinh": "Dương - ĐÀN ÔNG trộm cướp, hay đi đêm",
        "Vat": "Sông biển, tàu thuyền, xe chở nước",
        "Lien_Quan": "Nhâm = Trộm cắp, phạm nhân, di chuyển xa"
    },
    "Quý": {
        "Ngu_Hanh": "Âm Thủy", "Tuong": "Nước nhỏ, mưa, sương, mây",
        "Nguoi": "PHỤ NỮ lừa lọc, người bí mật, tù nhân",
        "Tinh_Cach": "Bí mật, hay lẩn trốn, lừa lọc, âm mưu",
        "Than_The": "Thận, chân, hệ sinh sản",
        "Gioi_Tinh": "Âm - PHỤ NỮ lừa lọc, bí mật, hay trốn",
        "Vat": "Mưa, suối, ao nhỏ, đồ lỏng",
        "Lien_Quan": "Quý = Thiên võng, tù nhân, mưa gió"
    }
}

# ============================================================
# PHẦN 6: TUẦN KHÔNG & DỊCH MÃ
# ============================================================

TUAN_KHONG_GIAI_THICH = {
    "Y_Nghia": "Tuần Không (Không Vong) là 2 Chi không có Can trong 1 tuần (10 ngày). Yếu tố lâm Không = Vô hiệu/giảm lực.",
    "Cat_Lam_Khong": "Cát lâm Không = Cát giảm, không thực, hứa suông",
    "Hung_Lam_Khong": "Hung lâm Không = Hung giảm, thoát nạn, nhẹ bệnh",
    "Dung_Than_Khong": "Dụng thần lâm Không = Việc không thành, người không đến, tiền không có",
    "Tim_Do": "Đồ mất mà Dụng thần lâm Không = Đã mất vĩnh viễn hoặc không tìm được"
}

DICH_MA_GIAI_THICH = {
    "Y_Nghia": "Dịch Mã (Mã Tinh) chỉ sự di chuyển, vận động. Cung có Mã = Nơi có sự biến động.",
    "Cach_Tinh": {
        "Thân_Tý_Thìn": "Mã ở Dần (Cung 8)",
        "Dần_Ngọ_Tuất": "Mã ở Thân (Cung 2)", 
        "Tị_Dậu_Sửu": "Mã ở Hợi (Cung 6)",
        "Hợi_Mão_Mùi": "Mã ở Tị (Cung 4)"
    },
    "Tim_Do": "Đồ mất mà Dụng thần lâm Mã = Đã bị mang đi xa, cần tìm ở hướng của Mã"
}

# ============================================================
# PHẦN 7: 64 QUẺ KINH DỊCH (TÓM TẮT)
# ============================================================

QUE_KINH_DICH = {
    "Thuần Càn": {"So": 1, "Cat_Hung": "Đại Cát", "Tom_Tat": "Trời, sức mạnh, thành công lớn"},
    "Thuần Khôn": {"So": 2, "Cat_Hung": "Cát", "Tom_Tat": "Đất, thuận theo, có quý nhân"},
    "Thủy Lôi Truân": {"So": 3, "Cat_Hung": "Bình", "Tom_Tat": "Khó khăn ban đầu, sẽ tốt dần"},
    "Sơn Thủy Mông": {"So": 4, "Cat_Hung": "Bình", "Tom_Tat": "Mông muội, cần học hỏi"},
    "Thủy Thiên Nhu": {"So": 5, "Cat_Hung": "Cát", "Tom_Tat": "Chờ đợi, sẽ có kết quả"},
    "Thiên Thủy Tụng": {"So": 6, "Cat_Hung": "Hung", "Tom_Tat": "Tranh tụng, cãi vã"},
    "Địa Thủy Sư": {"So": 7, "Cat_Hung": "Bình", "Tom_Tat": "Cần hợp tác, đông người"},
    "Thủy Địa Tỷ": {"So": 8, "Cat_Hung": "Cát", "Tom_Tat": "Thân cận, hợp tác tốt"},
    "Phong Thiên Tiểu Súc": {"So": 9, "Cat_Hung": "Bình", "Tom_Tat": "Tích lũy nhỏ, từ từ"},
    "Thiên Trạch Lý": {"So": 10, "Cat_Hung": "Bình", "Tom_Tat": "Cẩn thận từng bước"},
    "Địa Thiên Thái": {"So": 11, "Cat_Hung": "Đại Cát", "Tom_Tat": "Thái bình, hanh thông, rất tốt"},
    "Thiên Địa Bĩ": {"So": 12, "Cat_Hung": "Đại Hung", "Tom_Tat": "Bế tắc, không thông"},
    # ... (Có thể mở rộng thêm 52 quẻ còn lại)
}

# ============================================================
# PHẦN 8: HÀM TRA CỨU
# ============================================================

def tra_cuu_cung(cung_so):
    """Tra cứu thông tin chi tiết của 1 cung"""
    return CUU_CUNG.get(cung_so, {})

def tra_cuu_sao(ten_sao):
    """Tra cứu thông tin chi tiết của sao"""
    return CUU_TINH.get(ten_sao, {})

def tra_cuu_mon(ten_mon):
    """Tra cứu thông tin chi tiết của cửa"""
    # Xử lý tên có "Môn" hoặc không
    ten = ten_mon.replace(" Môn", "").strip() + " Môn"
    return BAT_MON.get(ten, {})

def tra_cuu_than(ten_than):
    """Tra cứu thông tin chi tiết của thần"""
    return BAT_THAN.get(ten_than, {})

def tra_cuu_can(ten_can):
    """Tra cứu thông tin chi tiết của can"""
    return THAP_THIEN_CAN.get(ten_can, {})

def xac_dinh_gioi_tinh_ke_lay(cung_data):
    """Xác định giới tính kẻ lấy dựa vào các yếu tố trong cung"""
    ket_qua = {"gioi_tinh": "Chưa xác định", "dac_diem": [], "do_tin_cay": 0}
    
    # Kiểm tra Can
    can = cung_data.get("can_thien") or cung_data.get("can")
    if can:
        can_info = THAP_THIEN_CAN.get(can, {})
        gioi_tinh = can_info.get("Gioi_Tinh", "")
        if "ĐÀN ÔNG" in gioi_tinh or "NAM" in gioi_tinh:
            ket_qua["gioi_tinh"] = "ĐÀN ÔNG"
            ket_qua["dac_diem"].append(f"{can}: {gioi_tinh}")
            ket_qua["do_tin_cay"] += 30
        elif "PHỤ NỮ" in gioi_tinh or "NỮ" in gioi_tinh:
            ket_qua["gioi_tinh"] = "PHỤ NỮ"
            ket_qua["dac_diem"].append(f"{can}: {gioi_tinh}")
            ket_qua["do_tin_cay"] += 30
    
    # Kiểm tra Thần
    than = cung_data.get("than")
    if than:
        than_info = BAT_THAN.get(than, {})
        tim_do = than_info.get("Tim_Do", "")
        if "đàn ông" in tim_do.lower() or "nam" in tim_do.lower():
            if ket_qua["gioi_tinh"] != "PHỤ NỮ":
                ket_qua["gioi_tinh"] = "ĐÀN ÔNG"
            ket_qua["dac_diem"].append(f"{than}: {tim_do}")
            ket_qua["do_tin_cay"] += 25
        elif "phụ nữ" in tim_do.lower():
            if ket_qua["gioi_tinh"] != "ĐÀN ÔNG":
                ket_qua["gioi_tinh"] = "PHỤ NỮ"
            ket_qua["dac_diem"].append(f"{than}: {tim_do}")
            ket_qua["do_tin_cay"] += 25
    
    # Kiểm tra Quái của Cung
    cung_so = cung_data.get("cung_so")
    if cung_so:
        cung_info = CUU_CUNG.get(cung_so, {})
        nguoi = cung_info.get("Nguoi", "")
        ket_qua["dac_diem"].append(f"Cung {cung_so}: {nguoi}")
        ket_qua["do_tin_cay"] += 20
    
    return ket_qua

def xac_dinh_huong_khoang_cach(cung_so):
    """Xác định hướng và khoảng cách dựa vào cung"""
    cung_info = CUU_CUNG.get(cung_so, {})
    return {
        "huong": cung_info.get("Huong", "Không xác định"),
        "noi": cung_info.get("Noi", "Không xác định"),
        "khoang_cach": "Gần" if cung_info.get("Ngu_Hanh") == "Thổ" else (
            "Xa" if cung_info.get("Ngu_Hanh") in ["Kim", "Thủy"] else "Trung bình"
        )
    }

def kha_nang_tim_duoc(mon_name):
    """Đánh giá khả năng tìm được đồ dựa vào Môn"""
    mon_info = BAT_MON.get(mon_name, {})
    return mon_info.get("Tim_Do", "Không xác định")


# Export
__all__ = [
    'CUU_CUNG', 'CUU_TINH', 'BAT_MON', 'BAT_THAN', 'THAP_THIEN_CAN',
    'tra_cuu_cung', 'tra_cuu_sao', 'tra_cuu_mon', 'tra_cuu_than', 'tra_cuu_can',
    'xac_dinh_gioi_tinh_ke_lay', 'xac_dinh_huong_khoang_cach', 'kha_nang_tim_duoc'
]

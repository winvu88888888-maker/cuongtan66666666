"""
van_vat_chi_tiet.py — V31.3 VẠN VẬT LOẠI TƯỢNG SIÊU CHI TIẾT
═══════════════════════════════════════════════════════════════
Bảng tra 5 HÀNH × 12 TRƯỜNG SINH = 60 tầng mô tả vạn vật.

Mỗi tầng bao gồm:
- 👁️ THỊ GIÁC: Hình dáng, kích thước, màu sắc, chất liệu, tình trạng
- 👂 THÍNH GIÁC: Âm thanh đặc trưng
- 👃 KHỨU GIÁC: Mùi hương
- 👅 VỊ GIÁC: Vị
- ✋ XÚC GIÁC: Cảm giác sờ, nhiệt độ, trọng lượng
- 🧑 CON NGƯỜI: Ngoại hình, tính cách, nghề nghiệp, giàu/nghèo
- 🔮 ĐỒ VẬT CỤ THỂ: Danh sách vật thể chính xác
- 🏠 NHÀ CỬA: Kiểu nhà, vị trí
- 🏥 BỆNH TẬT: Bệnh cụ thể
- 🐾 ĐỘNG VẬT: Con vật điển hình
- 🌿 THỰC VẬT: Cây cỏ
- 🔢 CON SỐ: Số liên quan

Công thức: NGŨ HÀNH → LOẠI + 12 TRƯỜNG SINH → TRẠNG THÁI
VD: Kim + Mộ = vật kim loại nhỏ, cũ, đã hỏng, bị chôn/cất kỹ = chìa khóa cũ, đồng xu cổ

V31.3 — Tạo bởi AI Engine cho QMDG System.
"""

# ═══════════════════════════════════════════════════════════════
# BẢNG 12 TRƯỜNG SINH → TRẠNG THÁI VẬT CHẤT
# ═══════════════════════════════════════════════════════════════

TRUONG_SINH_TRANG_THAI = {
    'Trường Sinh': {
        'cap': '🟢 Mới sinh',
        'kich_thuoc': 'Nhỏ, mới hình thành',
        'tinh_trang': 'MỚI TINH, vừa xuất hiện, chưa dùng',
        'tuoi_vat': 'Mới ra lò, vừa sản xuất, còn nguyên seal',
        'chat_luong': 'Tốt nhưng chưa ổn định, cần phát triển thêm',
        'trong_luong': 'Nhẹ, gọn',
        'nhiet_do': 'Ấm nhẹ (khí mới sinh)',
        'am_thanh': 'Tiếng nhỏ, yếu ớt, mới phát ra',
        'so_luong': '1-2',
        'so': [1],
        'huong_phat_trien': 'Đang lớn lên, sẽ mạnh dần',
    },
    'Mộc Dục': {
        'cap': '🟡 Tắm gội',
        'kich_thuoc': 'Nhỏ → vừa, đang phát triển',
        'tinh_trang': 'Đang được CHỈNH SỬA, tân trang, có vết trầy xước nhẹ',
        'tuoi_vat': 'Mới dùng 1-2 lần, hơi cũ nhưng còn tốt',
        'chat_luong': 'KHÔNG ỔN ĐỊNH, lúc tốt lúc xấu, dễ hỏng vặt',
        'trong_luong': 'Nhẹ - trung bình',
        'nhiet_do': 'Ấm (vừa tiếp xúc nước/dung dịch)',
        'am_thanh': 'Tiếng nước chảy, tiếng lau chùi, tiếng rửa',
        'so_luong': '1-3',
        'so': [2],
        'huong_phat_trien': 'Đang được cải thiện, chưa hoàn chỉnh',
    },
    'Quan Đới': {
        'cap': '🟢 Trưởng thành',
        'kich_thuoc': 'Vừa phải, cân đối',
        'tinh_trang': 'CHUẨN BỊ DÙNG, mới mặc/đeo, sẵn sàng',
        'tuoi_vat': 'Mới mua, đang học cách sử dụng',
        'chat_luong': 'Tốt, đang trong giai đoạn tốt nhất',
        'trong_luong': 'Trung bình, vừa tay',
        'nhiet_do': 'Mát mẻ, dễ chịu',
        'am_thanh': 'Tiếng mặc đồ, tiếng đeo, tiếng chuẩn bị',
        'so_luong': '2-3',
        'so': [3],
        'huong_phat_trien': 'Sắp đạt đỉnh, chuẩn bị tỏa sáng',
    },
    'Lâm Quan': {
        'cap': '🟢🟢 Vượng',
        'kich_thuoc': 'Lớn, to khỏe, đầy đặn',
        'tinh_trang': 'ĐANG DÙNG, hoạt động tốt, hiệu suất cao',
        'tuoi_vat': 'Đang ở prime, sử dụng hàng ngày, rất hữu ích',
        'chat_luong': 'RẤT TỐT, bền bỉ, đáng tin cậy',
        'trong_luong': 'Nặng, chắc chắn, có trọng lượng',
        'nhiet_do': 'Ấm nóng (đang hoạt động)',
        'am_thanh': 'Tiếng mạnh, rõ ràng, vang dội',
        'so_luong': '3-5',
        'so': [5, 7],
        'huong_phat_trien': 'Đang đỉnh cao, phát triển mạnh',
    },
    'Đế Vượng': {
        'cap': '🟢🟢🟢 Cực vượng',
        'kich_thuoc': 'CỰC LỚN, hoành tráng, nổi bật',
        'tinh_trang': 'ĐỈNH CAO, hoàn hảo, toàn vẹn, lung linh',
        'tuoi_vat': 'Đang ở đỉnh cao nhất, được mọi người biết đến',
        'chat_luong': 'HOÀN HẢO, cao cấp nhất, sang trọng, xa xỉ',
        'trong_luong': 'Rất nặng, đồ sộ, uy nghi',
        'nhiet_do': 'NÓNG, nhiệt lượng cao, bừng bừng',
        'am_thanh': 'Tiếng lớn, hùng hồn, vang xa, uy nghiêm',
        'so_luong': '5-9',
        'so': [9, 10],
        'huong_phat_trien': 'Đỉnh điểm rồi, sẽ bắt đầu đi xuống',
    },
    'Suy': {
        'cap': '🟡 Bắt đầu suy',
        'kich_thuoc': 'Vừa → nhỏ dần, hơi co lại',
        'tinh_trang': 'BẮT ĐẦU CŨ, có vết bẩn, trầy xước, phai màu',
        'tuoi_vat': 'Đã dùng lâu, bắt đầu lỗi thời, hết trend',
        'chat_luong': 'VẪN DÙNG ĐƯỢC nhưng kém hơn trước, có lỗi nhỏ',
        'trong_luong': 'Nhẹ dần, bớt chắc chắn',
        'nhiet_do': 'Hơi lạnh, bắt đầu nguội',
        'am_thanh': 'Tiếng nhỏ dần, hơi rè, không còn trong trẻo',
        'so_luong': '2-4',
        'so': [4, 6],
        'huong_phat_trien': 'Đang đi xuống, cần chăm sóc',
    },
    'Bệnh': {
        'cap': '🟠 Bệnh',
        'kich_thuoc': 'Nhỏ lại, méo mó, biến dạng nhẹ',
        'tinh_trang': 'HỎNG VẶT, có vấn đề, chạy chập chờn, lỗi',
        'tuoi_vat': 'Cũ, cần sửa chữa, nhiều vết xước/lõm',
        'chat_luong': 'KÉM, không đáng tin, hay trục trặc',
        'trong_luong': 'Nhẹ, lỏng lẻo, mong manh',
        'nhiet_do': 'Lạnh, ẩm ướt, có mùi ẩm mốc',
        'am_thanh': 'Tiếng kêu lạch cạch, rè, khò khè, không đều',
        'so_luong': '1-3',
        'so': [4],
        'huong_phat_trien': 'Đang xuống dốc, cần can thiệp',
    },
    'Tử': {
        'cap': '🔴 Chết',
        'kich_thuoc': 'RẤT NHỎ, teo lại, co quắp',
        'tinh_trang': 'HỎNG HẲN, không hoạt động, chết máy, đứng hình',
        'tuoi_vat': 'Rất cũ, bỏ không dùng, vứt xó, phế liệu',
        'chat_luong': 'PHẾ PHẨM, không giá trị, bỏ đi',
        'trong_luong': 'Rất nhẹ (đã mất phần bên trong) hoặc nặng trĩu (chết cứng)',
        'nhiet_do': 'LẠNH NGẮT, không có nhiệt, tê liệt',
        'am_thanh': 'IM LẶNG, không phát ra âm thanh, câm',
        'so_luong': '0-1',
        'so': [0],
        'huong_phat_trien': 'Đã hết, không cứu được',
    },
    'Mộ': {
        'cap': '🔴 Chôn/Cất',
        'kich_thuoc': 'Nhỏ gọn, bị nén, bị ép',
        'tinh_trang': 'BỊ CẤT KỸ, chôn giấu, khóa lại, niêm phong',
        'tuoi_vat': 'Cũ, lâu năm, cổ vật, đồ xưa, bị quên lãng',
        'chat_luong': 'CŨ nhưng CÓ GIÁ TRỊ tiềm ẩn (đồ cổ, kỷ niệm)',
        'trong_luong': 'Nặng (bị chất đống) hoặc nhẹ (bị quên trong hộp)',
        'nhiet_do': 'Lạnh, tối, ẩm (dưới đất, trong kho)',
        'am_thanh': 'Im lìm, bị bịt, không có tiếng, nghẹn',
        'so_luong': '1 (duy nhất, cô lập)',
        'so': [4, 8],
        'huong_phat_trien': 'Bị giữ lại, chờ ai đó tìm thấy',
    },
    'Tuyệt': {
        'cap': '🔴🔴 Tuyệt diệt',
        'kich_thuoc': 'CỰC NHỎ hoặc đã tan biến, gần như không còn',
        'tinh_trang': 'TAN RÃ, vỡ vụn, phân hủy, biến mất, bốc hơi',
        'tuoi_vat': 'Đã bị phá hủy, không thể phục hồi, bụi tro',
        'chat_luong': 'KHÔNG CÒN GIÁ TRỊ, rác, bụi, tro',
        'trong_luong': 'Gần bằng 0, bay theo gió',
        'nhiet_do': 'Không cảm nhận được (đã tan biến)',
        'am_thanh': 'TUYỆT ĐỐI IM LẶNG, hư vô',
        'so_luong': '0',
        'so': [0],
        'huong_phat_trien': 'Đã kết thúc hoàn toàn, chờ chu kỳ mới',
    },
    'Thai': {
        'cap': '💜 Thai nghén',
        'kich_thuoc': 'Cực nhỏ, vi mô, mầm mống',
        'tinh_trang': 'ĐANG HÌNH THÀNH, chưa rõ hình dạng, mơ hồ',
        'tuoi_vat': 'Chưa sinh ra, đang thai nghén, ý tưởng, bản vẽ',
        'chat_luong': 'TIỀM NĂNG, chưa biết tốt xấu, chờ đợi',
        'trong_luong': 'Gần như không trọng lượng',
        'nhiet_do': 'Ấm bên trong (được ấp ủ)',
        'am_thanh': 'Tiếng rất nhỏ, thì thầm, ý nghĩ',
        'so_luong': '0-1 (sắp có)',
        'so': [1, 6],
        'huong_phat_trien': 'Sắp sinh ra, đầy hứa hẹn',
    },
    'Dưỡng': {
        'cap': '💜🟢 Nuôi dưỡng',
        'kich_thuoc': 'Nhỏ nhưng đang lớn dần',
        'tinh_trang': 'ĐANG ĐƯỢC CHĂM SÓC, nuôi dưỡng, ấp ủ',
        'tuoi_vat': 'Từ mầm non, đang phát triển, được bảo vệ',
        'chat_luong': 'ĐANG CẢI THIỆN từng ngày, triển vọng tốt',
        'trong_luong': 'Nhẹ nhưng đang nặng dần',
        'nhiet_do': 'Ấm áp (được giữ ấm, ấp)',
        'am_thanh': 'Tiếng nhẹ nhàng, êm ái, ru',
        'so_luong': '1-2',
        'so': [2, 6],
        'huong_phat_trien': 'Đang lớn dần, sắp ra ánh sáng',
    },
}


# ═══════════════════════════════════════════════════════════════
# BẢNG NGŨ HÀNH → VẠN VẬT SIÊU CHI TIẾT
# ═══════════════════════════════════════════════════════════════
# Mỗi hành có đặc tính CỐ ĐỊNH (không đổi theo trường sinh)

NGU_HANH_VAN_VAT = {
    'Kim': {
        # ═══ ĐẶC TÍNH CỐ ĐỊNH ═══
        'hanh': 'Kim',
        'tinh_chat': 'Cứng, sắc bén, sáng bóng, lạnh, trong trẻo',
        'hinh_dang': 'Tròn, cong, lõm, vòng cung, hình cầu',
        'mau_sac': 'Trắng, bạc, vàng kim, xám bạc, ánh kim',
        'chat_lieu': 'Kim loại (sắt, thép, đồng, nhôm, vàng, bạc, inox)',
        'huong': 'Tây',
        'mua': 'Thu',
        'ngay': 'Thứ 6 (Kim nhật)',
        'gio': 'Thân-Dậu (15h-19h)',
        
        # ═══ 5 GIÁC QUAN ═══
        'thi_giac': {
            'mau': 'Trắng sáng, bạc lấp lánh, vàng ánh kim, chrome',
            'anh_sang': 'Phản chiếu mạnh, lấp lánh, có ánh kim',
            'be_mat': 'Bóng loáng, nhẵn mịn, hoặc có cạnh sắc',
            'do_trong': 'Có thể phản chiếu hình ảnh',
        },
        'thinh_giac': {
            'am_thanh': 'Leng keng, lanh canh, tiếng kim loại va chạm',
            'giong_noi': 'Trong trẻo, vang, dứt khoát, gọn gàng',
            'nhac_cu': 'Chuông, chũm chọe, kèn đồng, phong linh',
        },
        'khuu_giac': {
            'mui': 'Không mùi hoặc mùi kim loại tanh nhẹ, mùi sắt',
            'mui_dac_trung': 'Mùi đồng xu, mùi chìa khóa, mùi thép',
        },
        'vi_giac': {
            'vi': 'Cay nồng, hăng (hành tỏi, gừng, ớt)',
            'thuc_pham': 'Hành, tỏi, gừng, ớt, rau thơm mùi mạnh',
        },
        'xuc_giac': {
            'cam_giac': 'Lạnh, cứng, trơn, sắc cạnh',
            'nhiet_do': 'Lạnh khi chạm, dẫn nhiệt nhanh',
            'be_mat': 'Nhẵn bóng hoặc có gờ sắc',
            'trong_luong': 'Nặng so với kích thước',
        },
        
        # ═══ ĐỒ VẬT CỤ THỂ (A-Z) ═══
        'do_vat': {
            'Đế Vượng': ['Xe hơi hạng sang', 'Tủ sắt ngân hàng', 'Cần cẩu', 'Máy bay', 'Dao kiếm bảo vật', 'Đồng hồ Rolex', 'Trang sức vàng ròng', 'Két sắt lớn'],
            'Lâm Quan': ['Xe máy', 'Điện thoại iPhone', 'Laptop', 'Dao bếp tốt', 'Nhẫn vàng', 'Kéo chuyên dụng', 'Kìm, búa, cờ lê', 'Ổ khóa mới'],
            'Quan Đới': ['Chìa khóa mới', 'Kéo văn phòng', 'Đinh ốc mới', 'Thìa dĩa mới', 'Kim khâu', 'Ghim bấm', 'Kẹp giấy', 'Nồi inox mới'],
            'Trường Sinh': ['Đinh nhỏ mới', 'Kim châm cứu', 'Dây thép mới', 'Chiếc nhẫn nhỏ', 'Ghim cài áo', 'Cúc áo kim loại', 'Khuy đồng'],
            'Mộc Dục': ['Dao đã mài lại', 'Chìa khóa cũ đánh bóng', 'Xe đạp sửa xong', 'Nồi niêu rửa sạch', 'Điện thoại reset'],
            'Suy': ['Dao cùn', 'Chìa khóa cũ', 'Xe đạp hoen rỉ', 'Nồi cũ', 'Kéo cùn', 'Ổ khóa kẹt', 'Điện thoại lag', 'Vòng tay bạc xỉn'],
            'Bệnh': ['Máy hỏng', 'Kim gỉ', 'Xe máy chết máy', 'Đồng hồ chạy sai', 'Laptop lỗi màn hình', 'Quạt kêu to', 'Ống nước rò rỉ'],
            'Tử': ['Sắt vụn', 'Kim loại phế liệu', 'Xe nát', 'Máy bỏ', 'Dao gãy', 'Kéo gãy', 'Điện thoại chết hẳn', 'Bình gas rỗng'],
            'Mộ': ['Đồng xu cổ', 'Kiếm cổ trong hộp', 'Trang sức gia truyền', 'Chìa khóa bí ẩn', 'Két sắt khóa', 'Vàng chôn', 'Kho vũ khí'],
            'Tuyệt': ['Mạt sắt', 'Bụi kim loại', 'Vụn dao', 'Gỉ sét', 'Xỉ hàn', 'Tro kim loại', 'Bức xạ'],
            'Thai': ['Quặng mỏ', 'Kim loại thô', 'Thiết kế dao mới', 'Bản vẽ máy', 'Ý tưởng công nghệ'],
            'Dưỡng': ['Dao đang rèn', 'Kim loại đang đúc', 'Trang sức đang chế tác', 'Máy đang lắp ráp', 'Xe đang sản xuất'],
        },
        
        # ═══ CON NGƯỜI ═══
        'con_nguoi': {
            'ngoai_hinh': 'Da trắng sáng, mặt vuông/tròn, mũi cao, mắt sáng, tóc thưa hoặc đen bóng',
            'than_hinh': 'Cao gầy hoặc cân đối, xương to, vai rộng',
            'tinh_cach': 'Cương quyết, dứt khoát, nghiêm túc, kỷ luật, ít nói',
            'giong_noi': 'Trong trẻo, gọn gàng, dứt khoát, ngắn gọn',
            'nghe_nghiep': 'Quân đội, công an, bác sĩ phẫu thuật, thợ cơ khí, thợ vàng, IT, tài chính, ngân hàng',
            'Đế Vượng': 'Lãnh đạo uy quyền, giàu có, da trắng, dáng cao, ăn mặc sang trọng, đeo vàng/kim cương, CEO, tướng quân',
            'Lâm Quan': 'Người có chức vụ, khá giả, gọn gàng, chuyên nghiệp, quản lý, kỹ sư',
            'Suy': 'Người gầy, da xanh xao, hơi mệt mỏi, thu nhập giảm, đang gặp khó khăn',
            'Bệnh': 'Người bệnh phổi/da, ho, khó thở, sụt cân, xanh xao',
            'Tử': 'Người rất yếu/sắp mất, xương xẩu, tiều tụy, không có sức sống',
            'Mộ': 'Người ẩn dật, sống khép kín, không giao tiếp, bí ẩn, giữ bí mật',
            'Tuyệt': 'Người cô đơn, không ai biết, biến mất, vô gia cư, lang thang',
            'Thai': 'Thai nhi, em bé sắp sinh, người sắp bắt đầu sự nghiệp mới',
            'Dưỡng': 'Em bé nhỏ, người được chăm sóc, học sinh, người mới vào nghề, thực tập sinh',
        },
        
        # ═══ NHÀ CỬA ═══
        'nha_cua': {
            'chung': 'Nhà có nhiều kim loại, cửa sắt, lan can inox, mái tôn',
            'Đế Vượng': 'Biệt thự mái tôn sang trọng, nhà kho lớn, xưởng cơ khí lớn, ngân hàng',
            'Suy': 'Nhà cũ có mái tôn rỉ, cửa sắt kẹt, lan can lung lay',
            'Mộ': 'Nhà kho khóa kín, két sắt, phòng bí mật, hầm',
        },
        
        # ═══ BỆNH TẬT ═══
        'benh_tat': {
            'chung': 'Bệnh PHỔI, đường hô hấp, DA, xương, răng',
            'cu_the': ['Viêm phổi', 'Hen suyễn', 'Viêm phế quản', 'Viêm da', 'Dị ứng da', 'Gãy xương', 
                       'Đau răng', 'Viêm xoang', 'Cảm cúm', 'Covid', 'Lao phổi', 'Ho kéo dài',
                       'Ung thư phổi', 'Viêm họng', 'Sỏi thận (kim loại/canxi)'],
            'vi_tri': 'Phổi, phế quản, da, ruột già, mũi, xương',
        },
        
        # ═══ ĐỘNG VẬT ═══
        'dong_vat': {
            'chung': 'Hổ, báo, ngựa, gà, khỉ, chim ưng, đại bàng',
            'Đế Vượng': 'Hổ lớn, sư tử, đại bàng, ngựa chiến — mạnh mẽ, hung dữ',
            'Suy': 'Mèo lười, gà già, chim non — yếu ớt',
            'Tử': 'Xương động vật, da thú khô, nhện — liên quan cái chết',
            'Mộ': 'Chuột (sống trong hang), rắn (ẩn dưới đất) — ẩn nấp',
        },
        
        # ═══ THỰC VẬT ═══
        'thuc_vat': {
            'chung': 'Cây có gai, cây cứng, lá nhọn, cây bonsai, cây xương rồng',
            'Đế Vượng': 'Cây tùng bách đại thụ, cây bonsai quý, lan quý — cao giá',
            'Suy': 'Cây héo, lá vàng, cành khô — yếu ớt',
        },
    },
    
    'Mộc': {
        'hanh': 'Mộc',
        'tinh_chat': 'Mềm dẻo, có sức sống, phát triển, linh hoạt',
        'hinh_dang': 'Dài, thẳng, hình trụ, hình chữ nhật, thanh mảnh',
        'mau_sac': 'Xanh lá, xanh ngọc, xanh lục, nâu gỗ, be',
        'chat_lieu': 'Gỗ, tre, nứa, mây, giấy, vải bông, cao su, nhựa (từ cây)',
        'huong': 'Đông',
        'mua': 'Xuân',
        'ngay': 'Thứ 5 (Mộc nhật)',
        'gio': 'Dần-Mão (3h-7h)',
        
        'thi_giac': {
            'mau': 'Xanh lá tươi, xanh đậm, nâu gỗ, nâu nhạt',
            'anh_sang': 'Ánh sáng mềm, tự nhiên, xanh mát',
            'be_mat': 'Có vân gỗ, sớ vải, kết cấu tự nhiên',
            'do_trong': 'Mờ đục, có sớ, có vân',
        },
        'thinh_giac': {
            'am_thanh': 'Tiếng kẽo kẹt, tiếng lá xào xạc, tiếng gỗ gõ',
            'giong_noi': 'Ấm áp, nhẹ nhàng, trầm ấm, uyển chuyển',
            'nhac_cu': 'Đàn guitar, đàn tranh, sáo trúc, mõ gỗ',
        },
        'khuu_giac': {
            'mui': 'Mùi gỗ thơm, mùi cây xanh, mùi lá tươi, mùi đất',
            'mui_dac_trung': 'Mùi trầm hương, mùi gỗ thông, mùi tre, mùi giấy mới',
        },
        'vi_giac': {
            'vi': 'Chua (chanh, me, giấm, trái cây chua)',
            'thuc_pham': 'Rau xanh, trái cây, đậu, ngũ cốc, cơm, mì',
        },
        'xuc_giac': {
            'cam_giac': 'Ấm nhẹ, mềm nhưng dai, co giãn, linh hoạt',
            'nhiet_do': 'Ấm tự nhiên, không lạnh',
            'be_mat': 'Thô ráp tự nhiên, có vân, có sớ',
            'trong_luong': 'Nhẹ đến trung bình',
        },
        
        'do_vat': {
            'Đế Vượng': ['Bàn gỗ gụ/lim đại', 'Tủ sách gỗ quý', 'Cây đại thụ', 'Thuyền gỗ lớn', 'Đàn piano grand', 'Giường ngủ king size gỗ'],
            'Lâm Quan': ['Bàn làm việc gỗ', 'Ghế sofa vải', 'Sách vở', 'Cây cảnh lớn', 'Bút vẽ', 'Khung tranh', 'Tủ quần áo'],
            'Quan Đới': ['Bút mới', 'Tập vở mới', 'Quần áo mới', 'Giấy A4', 'Hoa tươi', 'Khăn mới'],
            'Trường Sinh': ['Hạt giống', 'Cây con', 'Giấy gấp', 'Bút chì nhỏ', 'Lá thư', 'Bookmark'],
            'Mộc Dục': ['Thớt gỗ rửa xong', 'Quần áo giặt xong', 'Sách cũ lau sạch', 'Cây tưới xong'],
            'Suy': ['Bàn gỗ cũ', 'Sách cũ ố vàng', 'Quần áo cũ', 'Dép cũ', 'Ghế lung lay', 'Cây héo'],
            'Bệnh': ['Gỗ mối mọt', 'Sách ẩm mốc', 'Quần áo rách', 'Cây bị sâu', 'Bút hết mực'],
            'Tử': ['Gỗ mục', 'Giấy nát', 'Vải rách nát', 'Cây chết khô', 'Bút gãy', 'Dép đứt'],
            'Mộ': ['Sách cổ trong rương', 'Gỗ trầm chôn', 'Quần áo cất kỹ', 'Hạt giống giữ', 'Bản thảo cũ'],
            'Tuyệt': ['Mùn gỗ', 'Tro giấy', 'Bụi vải', 'Rác thực vật', 'Phân bón hữu cơ'],
            'Thai': ['Hạt giống chưa nảy mầm', 'Ý tưởng viết sách', 'Bản thiết kế nội thất', 'Phôi gỗ'],
            'Dưỡng': ['Cây mới trồng', 'Sách đang viết', 'Quần áo đang may', 'Bàn đang đóng'],
        },
        
        'con_nguoi': {
            'ngoai_hinh': 'Da ngăm/nâu sáng, dáng cao gầy, mắt dài, tay chân dài, tóc dày',
            'than_hinh': 'Cao, gầy, thanh mảnh, linh hoạt, dẻo dai',
            'tinh_cach': 'Nhân hậu, từ bi, yêu thiên nhiên, sáng tạo, kiên nhẫn',
            'giong_noi': 'Trầm ấm, nhẹ nhàng, dễ nghe, uyển chuyển',
            'nghe_nghiep': 'Giáo viên, nhà văn, họa sĩ, nhà thiết kế, bác sĩ Đông y, thợ mộc, nông dân, kiến trúc sư',
            'Đế Vượng': 'Giáo sư nổi tiếng, nhà văn uy tín, CEO ngành gỗ/nội thất, kiến trúc sư lớn — cao gầy, da sáng, ăn mặc thanh lịch',
            'Lâm Quan': 'Giáo viên giỏi, thợ mộc lành nghề, nhà thiết kế — cần cù, chuyên nghiệp',
            'Suy': 'Người làm vườn mệt mỏi, giáo viên stress, thợ mộc thu nhập giảm — gầy, mắt thâm',
            'Bệnh': 'Người bệnh gan, đau mắt, co giật, tay chân tê — xanh xao, yếu ớt',
            'Tử': 'Người kiệt sức, da vàng bệnh gan, rất gầy, không còn sức sống',
            'Mộ': 'Nhà sư, người ẩn cư trong rừng, thầy phong thủy sống biệt lập',
            'Tuyệt': 'Vô gia cư sống ngoài trời, người bị bỏ rơi, mất tích trong rừng',
            'Thai': 'Thai nhi, em bé sắp sinh, sinh viên sắp ra trường',
            'Dưỡng': 'Em bé tập đi, học sinh tiểu học, nhà văn tập sự, thợ học việc',
        },
        
        'nha_cua': {
            'chung': 'Nhà gỗ, nhà sàn, nhà có nhiều cây xanh, ban công trồng cây',
            'Đế Vượng': 'Biệt thự gỗ cao cấp, nhà vườn rộng, khu resort sinh thái',
            'Suy': 'Nhà gỗ cũ mục nát, sàn gỗ kêu, cửa gỗ mối ăn',
            'Mộ': 'Nhà trong rừng, cabin gỗ biệt lập, nhà kho gỗ cũ',
        },
        
        'benh_tat': {
            'chung': 'Bệnh GAN, MẬT, MẮT, gân cốt, chân tay',
            'cu_the': ['Viêm gan A/B/C', 'Xơ gan', 'Sỏi mật', 'Cận thị', 'Đau mắt đỏ', 'Thoát vị đĩa đệm',
                       'Đau lưng', 'Co cơ', 'Gout', 'Trầm cảm', 'Stress', 'Mất ngủ',
                       'Động kinh', 'Tay chân tê bì', 'Viêm khớp'],
            'vi_tri': 'Gan, mật, mắt, gân, cơ, đầu gối, vai gáy',
        },
        
        'dong_vat': {
            'chung': 'Thỏ, mèo, chim, bướm, sâu, côn trùng, rắn non',
            'Đế Vượng': 'Rồng (biểu tượng), đại bàng, ngựa chiến — mạnh mẽ phi thường',
            'Suy': 'Chim non, thỏ yếu, sâu bọ — nhỏ bé',
            'Tử': 'Gỗ lũa (cây chết), cành khô, xác lá',
        },
        
        'thuc_vat': {
            'chung': 'Tre, trúc, tùng, bách, sen, lan, hoa hồng',
            'Đế Vượng': 'Đại thụ, cây đa, cây sanh, cổ thụ ngàn năm — vĩ đại',
            'Suy': 'Cây cúc tàn, hoa héo, cỏ úa — sắp tàn',
        },
    },
    
    'Thủy': {
        'hanh': 'Thủy',
        'tinh_chat': 'Lỏng, mềm mại, linh hoạt, thấm nhuần, biến hóa',
        'hinh_dang': 'Vô định hình, uốn lượn, gợn sóng, nhấp nhô, giọt',
        'mau_sac': 'Đen, xanh đậm, xanh navy, tím đậm, trong suốt',
        'chat_lieu': 'Nước, thủy tinh, pha lê, nhựa trong, mực, dầu, xăng',
        'huong': 'Bắc',
        'mua': 'Đông',
        'ngay': 'Thứ 4 (Thủy nhật)',
        'gio': 'Hợi-Tý (21h-1h)',
        
        'thi_giac': {
            'mau': 'Đen sâu, xanh đậm, xanh nước biển, trong suốt',
            'anh_sang': 'Phản chiếu, lấp lánh trên mặt nước, lung linh',
            'be_mat': 'Bóng ướt, trong suốt, có bọt, gợn sóng',
            'do_trong': 'Trong suốt đến đục (tùy trạng thái)',
        },
        'thinh_giac': {
            'am_thanh': 'Tiếng nước chảy, tiếng mưa, tiếng sóng, tí tách',
            'giong_noi': 'Nhẹ nhàng, êm ái, lưu loát, trôi chảy',
            'nhac_cu': 'Trống nước, đàn bầu, tiếng suối, tiếng mưa',
        },
        'khuu_giac': {
            'mui': 'Mùi nước, mùi biển mặn, mùi mưa, mùi ẩm',
            'mui_dac_trung': 'Mùi nước hoa, mùi cá biển, mùi rong rêu, mùi ao hồ',
        },
        'vi_giac': {
            'vi': 'Mặn (muối, nước mắm, hải sản)',
            'thuc_pham': 'Nước, trà, cà phê, rượu, bia, sữa, nước mắm, muối, hải sản',
        },
        'xuc_giac': {
            'cam_giac': 'Lạnh, ướt, trơn, mềm, mát, lỏng',
            'nhiet_do': 'Lạnh, mát (trừ nước nóng)',
            'be_mat': 'Trơn ướt, lỏng, không nắm được',
            'trong_luong': 'Nhẹ (giọt) đến rất nặng (biển cả)',
        },
        
        'do_vat': {
            'Đế Vượng': ['Bể cá koi đại', 'Du thuyền', 'Bể bơi', 'Đài phun nước', 'Chai rượu vang quý', 'Nước hoa Chanel No.5', 'Máy lọc nước công nghiệp'],
            'Lâm Quan': ['Bình nước', 'Máy giặt', 'Bồn tắm', 'Chai rượu', 'Bể cá', 'Nước hoa', 'Máy lọc nước gia đình'],
            'Quan Đới': ['Ly nước mới', 'Bình trà', 'Chai nước suối', 'Mực viết', 'Son dưỡng ẩm', 'Kem dưỡng da'],
            'Trường Sinh': ['Giọt sương', 'Nước mắt', 'Giọt mực nhỏ', 'Bong bóng nước', 'Sữa non'],
            'Mộc Dục': ['Nước tắm', 'Xà phòng', 'Dầu gội', 'Nước rửa tay', 'Nước lau sàn'],
            'Suy': ['Nước cũ trong bình', 'Rượu để lâu', 'Kem hết hạn', 'Trà nguội', 'Nước hoa bay mùi'],
            'Bệnh': ['Nước bẩn', 'Nước cống', 'Mực loãng', 'Sơn ướt bong tróc', 'Bồn rò rỉ', 'Nước đá chảy'],
            'Tử': ['Nước thối', 'Ao tù', 'Mực cạn', 'Bình nước vỡ', 'Nước tiểu', 'Nước bọt khô'],
            'Mộ': ['Nước ngầm', 'Giếng sâu', 'Bể ngầm', 'Chai rượu chôn', 'Nước khoáng dưới đất', 'Suối ngầm'],
            'Tuyệt': ['Hơi nước bay hơi', 'Sa mạc khô', 'Giếng cạn', 'Sông khô', 'Bụi muối'],
            'Thai': ['Mây (chứa nước)', 'Hơi nước', 'Sương mù', 'Ý tưởng nước hoa mới'],
            'Dưỡng': ['Mưa phùn', 'Sương mai', 'Giọt nước đầu vòi', 'Nước ươm hạt'],
        },
        
        'con_nguoi': {
            'ngoai_hinh': 'Da đen/ngăm, mặt tròn đầy, mắt to, môi dày, tóc đen nhánh',
            'than_hinh': 'Mập, tròn trịa, hoặc cao to thuỷ vượng',
            'tinh_cach': 'Thông minh, lanh lợi, khéo léo, uyển chuyển, hay thay đổi',
            'giong_noi': 'Nhỏ nhẹ, trôi chảy, lưu loát, nhiều ngôn ngữ',
            'nghe_nghiep': 'Thủy thủ, ngư dân, pha chế, bartender, nhà ngoại giao, gián điệp, nhà tâm lý, thuỷ lợi, phong thủy',
            'Đế Vượng': 'Thương nhân giàu có (buôn bán quốc tế), ngoại giao gia, nhà tâm lý nổi tiếng — đen bóng, mập, ăn nói lưu loát',
            'Lâm Quan': 'Bartender giỏi, kỹ sư thủy lợi, nhà buôn — lanh lợi, xởi lởi',
            'Suy': 'Người buôn bán ế ẩm, ngư dân nghèo — gầy, da đen nhăm, mệt',
            'Bệnh': 'Người bệnh thận, phù nề, tiểu đường — mặt sưng, chân phù',
            'Tử': 'Người đuối nước, nghiện rượu, mất phương hướng — tiều tụy',
            'Mộ': 'Người sống dưới tàu, thợ lặn, người làm việc dưới nước/ngầm',
            'Tuyệt': 'Người mất tích trên biển, lưu lạc xa, không liên lạc',
            'Thai': 'Thai nhi trong bụng mẹ (được nước ối bao bọc)',
            'Dưỡng': 'Em bé sơ sinh, người đang phục hồi sức khỏe, uống thuốc',
        },
        
        'nha_cua': {
            'chung': 'Nhà gần sông, biển, hồ, nhà có bể cá, đài phun nước',
            'Đế Vượng': 'Resort ven biển, nhà hàng trên thuyền, biệt thự mặt hồ',
            'Suy': 'Nhà dột, ống nước rò rỉ, bồn cầu hỏng',
            'Mộ': 'Nhà dưới tầng hầm, gần giếng, nhà nổi',
        },
        
        'benh_tat': {
            'chung': 'Bệnh THẬN, BÀNG QUANG, sinh dục, tai, xương tuỷ, máu',
            'cu_the': ['Suy thận', 'Sỏi thận', 'Viêm bàng quang', 'Tiểu đường', 'Bệnh lậu', 'Bệnh thận',
                       'Phù nề', 'Cao huyết áp', 'Thiếu máu', 'Bệnh tai', 'Điếc',
                       'Tiểu tiện bất thường', 'Xuất huyết', 'Bạch cầu bất thường'],
            'vi_tri': 'Thận, bàng quang, tai, xương tủy, tử cung, tiền liệt',
        },
        
        'dong_vat': {
            'chung': 'Cá, tôm, cua, ốc, rùa, rắn nước, cá heo, cá voi',
            'Đế Vượng': 'Cá voi, cá heo, rồng (biểu tượng nước) — khổng lồ',
            'Suy': 'Cá nhỏ, tôm riu, ốc nhỏ — bé tẹo',
            'Tử': 'Cá chết, ốc chết — thối rữa',
        },
        
        'thuc_vat': {
            'chung': 'Sen, súng, rong rêu, bèo, tảo, cây thủy sinh',
            'Đế Vượng': 'Sen hồng nở rộ, cây bồ đề, cây đa ven sông — đẹp',
            'Suy': 'Bèo tấm, rong rêu, tảo xanh — tầm thường',
        },
    },
    
    'Hỏa': {
        'hanh': 'Hỏa',
        'tinh_chat': 'Nóng, sáng, bùng cháy, lan tỏa, mạnh mẽ, biến đổi nhanh',
        'hinh_dang': 'Nhọn, tam giác, hình ngọn lửa, hình nón, tháp',
        'mau_sac': 'Đỏ, cam, tím, hồng, đỏ rực, đỏ tươi, đỏ son',
        'chat_lieu': 'Đèn, nến, nhựa (cháy), sợi tổng hợp, điện tử, pin, acquy',
        'huong': 'Nam',
        'mua': 'Hạ',
        'ngay': 'Thứ 3 (Hỏa nhật)',
        'gio': 'Tỵ-Ngọ (9h-13h)',
        
        'thi_giac': {
            'mau': 'Đỏ rực, cam cháy, tím ánh, hồng sen',
            'anh_sang': 'Tỏa sáng, lấp lánh, rực rỡ, chói loa',
            'be_mat': 'Bóng (khi cháy), gập ghềnh (tro, than)',
            'do_trong': 'Sáng rực, phát quang',
        },
        'thinh_giac': {
            'am_thanh': 'Tiếng lửa cháy tí tách, tiếng nổ, tiếng bùng',
            'giong_noi': 'To, nhanh, nhiệt huyết, nồng nhiệt, sôi nổi',
            'nhac_cu': 'Trống, thanh la, kèn trumpet, guitar điện',
        },
        'khuu_giac': {
            'mui': 'Mùi khói, mùi cháy, mùi nóng, mùi nhựa nóng',
            'mui_dac_trung': 'Mùi than nướng, mùi hương trầm cháy, mùi pháo nổ, mùi nến thơm',
        },
        'vi_giac': {
            'vi': 'Đắng (khổ qua, cà phê đen, trà đặc, thuốc)',
            'thuc_pham': 'BBQ, đồ nướng, cà phê, sô cô la đen, rau đắng, thuốc nam',
        },
        'xuc_giac': {
            'cam_giac': 'Nóng, bỏng, châm chích, khô ráo',
            'nhiet_do': 'NÓNG, từ ấm đến bỏng tay',
            'be_mat': 'Khô, nóng, có thể bỏng',
            'trong_luong': 'Nhẹ (lửa, ánh sáng không có trọng lượng)',
        },
        
        'do_vat': {
            'Đế Vượng': ['Lò sưởi lớn', 'Hệ thống chiếu sáng sân vận động', 'Tivi 85 inch', 'Pháo hoa hoành tráng', 'Đuốc Olympic', 'Lò phản ứng hạt nhân', 'Đèn pha sân khấu'],
            'Lâm Quan': ['Bếp gas', 'Lò vi sóng', 'Tivi', 'Máy tính chơi game', 'Đèn LED', 'Bóng đèn', 'Bật lửa Zippo'],
            'Quan Đới': ['Nến thơm mới', 'Pin mới', 'Bóng đèn mới', 'Match que diêm', 'Đèn bàn'],
            'Trường Sinh': ['Tia lửa nhỏ', 'Đốm sáng', 'LED nhỏ', 'Pin cúc áo', 'Ngọn nến nhỏ'],
            'Mộc Dục': ['Đèn vừa lau', 'Lò vừa vệ sinh', 'Que diêm vừa sấy', 'Bóng đèn lau sạch'],
            'Suy': ['Đèn mờ', 'Nến cháy gần hết', 'Pin yếu', 'Tivi cũ', 'Bếp gas lửa yếu', 'Bật lửa sắp hết gas'],
            'Bệnh': ['Đèn nhấp nháy', 'Bóng đèn sắp cháy', 'Pin phồng', 'Tivi nhiễu', 'Bếp gas rò rỉ', 'Ổ điện cháy'],
            'Tử': ['Đèn tắt', 'Nến tàn', 'Pin chết', 'Bóng đèn cháy', 'Tivi vỡ', 'Than tro nguội', 'Diêm hết'],
            'Mộ': ['Than đá trong mỏ', 'Dầu mỏ dưới đất', 'Núi lửa ngủ', 'Lò nung cổ', 'Đuốc trong hầm mộ'],
            'Tuyệt': ['Tro tàn', 'Khói tan', 'Tia lửa tắt', 'Bụi than', 'Màn đêm tối đen'],
            'Thai': ['Magma dưới đất', 'Tia lửa sắp bùng', 'Ý tưởng phim', 'Kịch bản chưa quay'],
            'Dưỡng': ['Đốm lửa nhỏ', 'Than hồng', 'Bếp đang nhóm', 'Đèn dimmer', 'Nến mới thắp'],
        },
        
        'con_nguoi': {
            'ngoai_hinh': 'Da đỏ/hồng, mặt nhọn/tam giác, mắt sáng, tóc xoăn/đỏ nâu',
            'than_hinh': 'Trung bình, nhanh nhẹn, linh hoạt, hay vung tay',
            'tinh_cach': 'Nóng tính, nhiệt huyết, tràn đầy năng lượng, sáng tạo, bốc đồng',
            'giong_noi': 'To, nhanh, sôi nổi, nhiệt tình, hay cười',
            'nghe_nghiep': 'Nghệ sĩ, MC, diễn viên, đầu bếp, thợ hàn, lính cứu hỏa, nhà báo, marketer, KOL',
            'Đế Vượng': 'Ngôi sao nổi tiếng, CEO công nghệ, KOL triệu followers — sáng bóng, nổi bật, ăn mặc lộng lẫy',
            'Lâm Quan': 'MC truyền hình, đầu bếp nổi tiếng, marketer giỏi — tự tin, sáng rỡ',
            'Suy': 'Nghệ sĩ hết thời, diễn viên quá đát — mệt mỏi, buồn, hơi mập',
            'Bệnh': 'Người bệnh tim, huyết áp cao, mặt đỏ, hay bừng nóng, khó thở',
            'Tử': 'Người đột quỵ, nhồi máu, sốc nhiệt — mặt tím tái',
            'Mộ': 'Nghệ sĩ ẩn dật, người sống trong ký ức quá khứ huy hoàng',
            'Tuyệt': 'Người bị quên lãng, ngôi sao lụi tàn, không ai nhớ',
            'Thai': 'Thai nhi, ý tưởng nghệ thuật, startup sắp ra mắt',
            'Dưỡng': 'Em bé hiếu động, thực tập sinh marketing, idol trainee',
        },
        
        'nha_cua': {
            'chung': 'Nhà nhiều cửa kính, nhà hướng Nam, nhiều ánh sáng, bếp lửa',
            'Đế Vượng': 'Penthouse view thành phố rực sáng, nhà hàng, sân khấu, studio',
            'Suy': 'Nhà thiếu ánh sáng, bếp gas cũ, đèn mờ',
            'Mộ': 'Nhà dưới hầm, phòng tối, studio ngầm',
        },
        
        'benh_tat': {
            'chung': 'Bệnh TIM, MẠCH MÁU, MẮT (viêm), RUỘT NON, lưỡi',
            'cu_the': ['Nhồi máu cơ tim', 'Đột quỵ', 'Cao huyết áp', 'Viêm mắt', 'Sốt cao', 
                       'Viêm ruột', 'Lở loét miệng', 'Nóng trong', 'Mụn nhọt',
                       'Bỏng', 'Nhiễm trùng', 'Viêm da mẩn đỏ', 'Mất ngủ do nóng'],
            'vi_tri': 'Tim, ruột non, mắt, lưỡi, mạch máu, não',
        },
        
        'dong_vat': {
            'chung': 'Chim phượng, công, ngựa, cừu, ve sầu, đom đóm, bọ cánh cứng đỏ',
            'Đế Vượng': 'Phượng hoàng (biểu tượng), công đực xòe đuôi — rực rỡ',
            'Suy': 'Ve sầu cuối hạ, đom đóm leo lắt — sắp tắt',
        },
        
        'thuc_vat': {
            'chung': 'Hoa hồng đỏ, hoa phượng, hoa gạo, ớt, hoa tulip đỏ',
            'Đế Vượng': 'Hoa phượng nở rực trời, mùa hoa ban đỏ — lộng lẫy',
            'Suy': 'Hoa héo, cánh rụng, lá vàng mùa thu — tàn phai',
        },
    },
    
    'Thổ': {
        'hanh': 'Thổ',
        'tinh_chat': 'Nặng, chắc chắn, ổn định, dày, thấm hút',
        'hinh_dang': 'Vuông, khối, dày dặn, phẳng, bằng bệ',
        'mau_sac': 'Vàng, nâu đất, cam đất, be, kem, terracotta',
        'chat_lieu': 'Đất, đá, gạch, xi măng, bê tông, gốm sứ, thủy tinh đục, sành',
        'huong': 'Trung Tâm (hoặc Tây Nam / Đông Bắc)',
        'mua': 'Cuối hạ / giao mùa',
        'ngay': 'Thứ 7 (Thổ nhật)',
        'gio': 'Sửu-Thìn-Mùi-Tuất (1h-3h, 7h-9h, 13h-15h, 19h-21h)',
        
        'thi_giac': {
            'mau': 'Vàng đất, nâu sậm, be kem, cam đất, terracotta',
            'anh_sang': 'Ánh sáng ấm, mờ nhạt, tự nhiên, không chói',
            'be_mat': 'Thô ráp, có hạt, có lỗ nhỏ (gốm), dày dặn',
            'do_trong': 'Đục, không xuyên sáng, dày đặc',
        },
        'thinh_giac': {
            'am_thanh': 'Tiếng đất vỡ, tiếng gõ gốm, tiếng nghiền, tiếng nặng đặt xuống',
            'giong_noi': 'Trầm, chậm, đều đặn, nặng nề, chắc chắn',
            'nhac_cu': 'Cồng chiêng, trống đất, ocarina, xylophone',
        },
        'khuu_giac': {
            'mui': 'Mùi ĐẤT sau mưa, mùi đất ẩm, mùi gạch nung, mùi sét',
            'mui_dac_trung': 'Mùi bùn, mùi ruộng đồng, mùi xi măng mới, mùi gốm nung',
        },
        'vi_giac': {
            'vi': 'Ngọt (đường, mật ong, trái cây chín, khoai)',
            'thuc_pham': 'Khoai lang, khoai tây, cơm, bánh mì, đường, mật ong, ngô, bí',
        },
        'xuc_giac': {
            'cam_giac': 'Nặng, thô, dày, chắc, ổn định',
            'nhiet_do': 'Ấm nhẹ (giữ nhiệt tốt), mát khi dưới đất',
            'be_mat': 'Thô ráp, có hạt sần sùi, nặng tay',
            'trong_luong': 'NẶNG, rất nặng, cần sức để nhấc',
        },
        
        'do_vat': {
            'Đế Vượng': ['Tòa nhà cao tầng', 'Kim tự tháp', 'Bức tường thành', 'Đất ruộng mênh mông', 'Tượng Phật lớn', 'Container', 'Xe tải lớn'],
            'Lâm Quan': ['Bàn gạch', 'Tượng gốm', 'Chậu sứ', 'Gạch lát', 'Bê tông', 'Tường nhà', 'Bao xi măng'],
            'Quan Đới': ['Bát đĩa sứ mới', 'Chậu cây mới', 'Gạch xây mới', 'Đất trồng', 'Bình gốm'],
            'Trường Sinh': ['Hòn sỏi nhỏ', 'Viên đất sét', 'Hạt cát', 'Viên gạch nhỏ', 'Nắp chén'],
            'Mộc Dục': ['Bát đĩa rửa sạch', 'Sàn nhà lau xong', 'Gạch mới rửa', 'Tường sơn lại'],
            'Suy': ['Tường loang lổ', 'Gạch vỡ', 'Bát mẻ', 'Sàn nứt', 'Đất khô cằn', 'Tượng bạc màu'],
            'Bệnh': ['Tường nứt', 'Nền lún', 'Gạch vỡ vụn', 'Sàn trơn trượt', 'Đất ô nhiễm'],
            'Tử': ['Gạch vỡ nát', 'Tường đổ', 'Bình vỡ', 'Đất chết (không trồng được)', 'Cát bỏ hoang', 'Tro tàn đất'],
            'Mộ': ['Mộ phần', 'Đất chôn kho báu', 'Hầm đất', 'Hang động', 'Đá quý trong mỏ', 'Gốm cổ chôn'],
            'Tuyệt': ['Bụi đất', 'Cát bay sa mạc', 'Đá vôite tan', 'Sỏi nghiền', 'Tro than'],
            'Thai': ['Đất sét nhồi (chưa nặn)', 'Bản vẽ kiến trúc', 'Đá thô chưa đẽo', 'Ý tưởng xây nhà'],
            'Dưỡng': ['Đất đang ủ phân', 'Gốm đang nung', 'Xi măng đang đổ', 'Tường đang xây', 'Nền đang san'],
        },
        
        'con_nguoi': {
            'ngoai_hinh': 'Da vàng/nâu, mặt vuông, má bầu, mũi to, môi dày, tóc dày đen',
            'than_hinh': 'MẬP, thấp, chắc khỏe, bụng to, vai rộng, tay chân chắc',
            'tinh_cach': 'Trung thực, kiên nhẫn, chung thủy, bảo thủ, chậm rãi, đáng tin',
            'giong_noi': 'Trầm, chậm, nặng, đều đều, ít nói, nói gì chắc nấy',
            'nghe_nghiep': 'Nhà nông, xây dựng, kiến trúc, bất động sản, đầu bếp, thợ gốm, kế toán',
            'Đế Vượng': 'Đại gia bất động sản, địa chủ lớn, chủ công ty xây dựng — mập, da vàng, đeo vàng nặng trĩu, uy nghi',
            'Lâm Quan': 'Kiến trúc sư, kỹ sư xây dựng, nông dân giàu — chắc khỏe, đáng tin',
            'Suy': 'Nông dân nghèo, thợ xây mệt, kế toán stress — mệt, vai gù',
            'Bệnh': 'Người bệnh dạ dày, đầy bụng, khó tiêu, sưng phù — bụng to, mặt vàng',
            'Tử': 'Người dinh dưỡng kém, gầy gò xanh xao, không ăn được — thiếu sức sống',
            'Mộ': 'Người giữ kho, bảo tàng, thợ đào mộ, khảo cổ — bí ẩn, trầm lặng',
            'Tuyệt': 'Người bị mất đất, vô gia cư sống ngoài đường, lang thang',
            'Thai': 'Thai nhi, ý tưởng kinh doanh bđs, sinh viên kiến trúc',
            'Dưỡng': 'Em bé mập, trẻ nhỏ khoẻ, thợ xây học việc, nông dân mới bắt đầu',
        },
        
        'nha_cua': {
            'chung': 'Nhà gạch, nhà bê tông, chung cư, nhà trệt, nhà có sân rộng',
            'Đế Vượng': 'Tòa nhà chọc trời, biệt thự lớn, đất đai mênh mông, lâu đài',
            'Suy': 'Nhà cấp 4 cũ nát, tường loang, nền lún, mái dột',
            'Mộ': 'Hầm ngầm, phòng kho, nhà mồ, hang động, nhà trong núi',
        },
        
        'benh_tat': {
            'chung': 'Bệnh DẠ DÀY, LÁCH, MIỆNG, cơ bắp, da thịt',
            'cu_the': ['Đau dạ dày', 'Viêm loét dạ dày', 'Béo phì', 'Tiểu đường type 2', 'Viêm lách',
                       'Đầy bụng', 'Khó tiêu', 'Nấm da', 'Mụn cóc', 'Sưng phù',
                       'Ung thư dạ dày', 'Viêm miệng lưỡi', 'Teo cơ', 'Loãng xương'],
            'vi_tri': 'Dạ dày, lách, miệng, cơ bắp, mô mỡ, da thịt',
        },
        
        'dong_vat': {
            'chung': 'Trâu, bò, chó, dê, gấu, lợn, giun đất, kiến',
            'Đế Vượng': 'Voi, tê giác, trâu rừng — lớn, nặng, uy nghi',
            'Suy': 'Giun đất, kiến, sâu — nhỏ bé, sống dưới đất',
            'Mộ': 'Chuột chũi, dế, giun — sống trong hang dưới đất',
        },
        
        'thuc_vat': {
            'chung': 'Khoai, sắn, ngô, lúa, nấm, địa y, cây mía',
            'Đế Vượng': 'Cây đa cổ thụ, cây bồ đề — gốc to, bám đất chắc',
            'Suy': 'Khoai sắn héo, ngô khô, rau úa — sắp thu hoạch',
        },
    },
}


# ═══════════════════════════════════════════════════════════════
# HELPER: LẤY MÔ TẢ CHI TIẾT THEO HÀNH + TRƯỜNG SINH
# ═══════════════════════════════════════════════════════════════

def get_van_vat_chi_tiet(hanh, truong_sinh_stage):
    """Lấy mô tả vạn vật siêu chi tiết theo Ngũ Hành + 12 Trường Sinh.
    
    Args:
        hanh: str — Kim/Mộc/Thủy/Hỏa/Thổ
        truong_sinh_stage: str — Trường Sinh/Mộc Dục/.../Dưỡng
    
    Returns: dict với MỌI thông tin chi tiết (5 giác quan, đồ vật, người, bệnh...)
    """
    hanh_data = NGU_HANH_VAN_VAT.get(hanh, {})
    ts_data = TRUONG_SINH_TRANG_THAI.get(truong_sinh_stage, {})
    
    if not hanh_data:
        return {'error': f'Không tìm thấy hành: {hanh}'}
    
    # Lấy đồ vật cụ thể theo tầng
    do_vat_cu_the = hanh_data.get('do_vat', {}).get(truong_sinh_stage, 
                    hanh_data.get('do_vat', {}).get('Lâm Quan', []))
    
    # Lấy mô tả con người theo tầng
    con_nguoi_tang = hanh_data.get('con_nguoi', {}).get(truong_sinh_stage,
                     hanh_data.get('con_nguoi', {}).get('ngoai_hinh', ''))
    
    # Lấy nhà cửa theo tầng
    nha_cua_tang = hanh_data.get('nha_cua', {}).get(truong_sinh_stage,
                   hanh_data.get('nha_cua', {}).get('chung', ''))
    
    # Lấy thú theo tầng
    dong_vat_tang = hanh_data.get('dong_vat', {}).get(truong_sinh_stage,
                    hanh_data.get('dong_vat', {}).get('chung', ''))
    
    result = {
        # === THÔNG TIN CƠ BẢN ===
        'hanh': hanh,
        'truong_sinh': truong_sinh_stage,
        'cap': ts_data.get('cap', ''),
        'tinh_chat': hanh_data.get('tinh_chat', ''),
        
        # === HÌNH DÁNG & KÍCH THƯỚC ===
        'hinh_dang': hanh_data.get('hinh_dang', ''),
        'kich_thuoc': ts_data.get('kich_thuoc', ''),
        'tinh_trang': ts_data.get('tinh_trang', ''),
        'tuoi_vat': ts_data.get('tuoi_vat', ''),
        'chat_luong': ts_data.get('chat_luong', ''),
        
        # === MÀU SẮC & CHẤT LIỆU ===
        'mau_sac': hanh_data.get('mau_sac', ''),
        'chat_lieu': hanh_data.get('chat_lieu', ''),
        
        # === 5 GIÁC QUAN ===
        'thi_giac': hanh_data.get('thi_giac', {}),
        'thinh_giac': hanh_data.get('thinh_giac', {}),
        'khuu_giac': hanh_data.get('khuu_giac', {}),
        'vi_giac': hanh_data.get('vi_giac', {}),
        'xuc_giac': hanh_data.get('xuc_giac', {}),
        
        # === TRỌNG LƯỢNG & NHIỆT ĐỘ ===
        'trong_luong': ts_data.get('trong_luong', ''),
        'nhiet_do': ts_data.get('nhiet_do', ''),
        'am_thanh': ts_data.get('am_thanh', ''),
        
        # === ĐỒ VẬT CỤ THỂ ===
        'do_vat_cu_the': do_vat_cu_the,
        
        # === HƯỚNG, MÙA, SỐ ===
        'huong': hanh_data.get('huong', ''),
        'mua': hanh_data.get('mua', ''),
        'so': ts_data.get('so', []),
        'so_luong': ts_data.get('so_luong', ''),
        
        # === CON NGƯỜI ===
        'con_nguoi': {
            'ngoai_hinh': hanh_data.get('con_nguoi', {}).get('ngoai_hinh', ''),
            'than_hinh': hanh_data.get('con_nguoi', {}).get('than_hinh', ''),
            'tinh_cach': hanh_data.get('con_nguoi', {}).get('tinh_cach', ''),
            'giong_noi': hanh_data.get('con_nguoi', {}).get('giong_noi', ''),
            'nghe_nghiep': hanh_data.get('con_nguoi', {}).get('nghe_nghiep', ''),
            'mo_ta_tang': con_nguoi_tang,
        },
        
        # === NHÀ CỬA ===
        'nha_cua': nha_cua_tang,
        
        # === BỆNH TẬT ===
        'benh_tat': {
            'loai': hanh_data.get('benh_tat', {}).get('chung', ''),
            'cu_the': hanh_data.get('benh_tat', {}).get('cu_the', []),
            'vi_tri': hanh_data.get('benh_tat', {}).get('vi_tri', ''),
        },
        
        # === ĐỘNG VẬT ===
        'dong_vat': dong_vat_tang,
        
        # === THỰC VẬT ===
        'thuc_vat': hanh_data.get('thuc_vat', {}).get(truong_sinh_stage,
                    hanh_data.get('thuc_vat', {}).get('chung', '')),
        
        # === DỰ BÁO XU HƯỚNG ===
        'xu_huong': ts_data.get('huong_phat_trien', ''),
    }
    
    return result


def format_van_vat_for_ai(hanh, truong_sinh_stage):
    """Format vạn vật chi tiết thành text cho AI đọc và đối chiếu.
    Output ngắn gọn nhưng ĐẦY ĐỦ để AI trả lời chính xác.
    """
    data = get_van_vat_chi_tiet(hanh, truong_sinh_stage)
    if 'error' in data:
        return data['error']
    
    lines = []
    lines.append(f"=== VẠN VẬT: {hanh} × {truong_sinh_stage} ({data['cap']}) ===")
    lines.append(f"Tính chất: {data['tinh_chat']}")
    lines.append(f"Hình dáng: {data['hinh_dang']} | Kích thước: {data['kich_thuoc']}")
    lines.append(f"Màu: {data['mau_sac']} | Chất liệu: {data['chat_lieu']}")
    lines.append(f"Tình trạng: {data['tinh_trang']} | Tuổi: {data['tuoi_vat']}")
    lines.append(f"Chất lượng: {data['chat_luong']}")
    lines.append(f"Trọng lượng: {data['trong_luong']} | Nhiệt: {data['nhiet_do']}")
    
    # 5 giác quan
    tg = data.get('thi_giac', {})
    lines.append(f"👁️ Nhìn: {tg.get('mau', '')} | {tg.get('be_mat', '')} | {tg.get('anh_sang', '')}")
    ag = data.get('thinh_giac', {})
    lines.append(f"👂 Nghe: {ag.get('am_thanh', '')} | Giọng: {ag.get('giong_noi', '')}")
    kg = data.get('khuu_giac', {})
    lines.append(f"👃 Ngửi: {kg.get('mui', '')} | {kg.get('mui_dac_trung', '')}")
    vg = data.get('vi_giac', {})
    lines.append(f"👅 Vị: {vg.get('vi', '')} | Thực phẩm: {vg.get('thuc_pham', '')}")
    xg = data.get('xuc_giac', {})
    lines.append(f"✋ Sờ: {xg.get('cam_giac', '')} | {xg.get('be_mat', '')}")
    
    # Đồ vật cụ thể
    if data.get('do_vat_cu_the'):
        items = ', '.join(data['do_vat_cu_the'][:8])
        lines.append(f"🔮 Đồ vật: {items}")
    
    # Con người
    cn = data.get('con_nguoi', {})
    lines.append(f"🧑 Người: {cn.get('ngoai_hinh', '')} | {cn.get('than_hinh', '')}")
    lines.append(f"   Tính cách: {cn.get('tinh_cach', '')} | Giọng: {cn.get('giong_noi', '')}")
    lines.append(f"   Nghề: {cn.get('nghe_nghiep', '')}")
    if cn.get('mo_ta_tang'):
        lines.append(f"   Tầng {truong_sinh_stage}: {cn['mo_ta_tang']}")
    
    # Nhà, bệnh, động vật
    lines.append(f"🏠 Nhà: {data.get('nha_cua', '')}")
    bt = data.get('benh_tat', {})
    lines.append(f"🏥 Bệnh: {bt.get('loai', '')} | Chi tiết: {', '.join(bt.get('cu_the', [])[:5])}")
    lines.append(f"🐾 Thú: {data.get('dong_vat', '')} | 🌿 Cây: {data.get('thuc_vat', '')}")
    lines.append(f"🧭 Hướng: {data.get('huong', '')} | Mùa: {data.get('mua', '')} | Số: {data.get('so', [])}")
    lines.append(f"📈 Xu hướng: {data.get('xu_huong', '')}")
    
    return "\n".join(lines)


def get_tham_tu_mo_ta(hanh, truong_sinh_stage, question=""):
    """V31.3 THÁM TỬ: Lắp ghép manh mối từ Vạn Vật để mô tả cực chi tiết.
    Trả về mô tả như thám tử đang kể lại — cụ thể đến mức nhìn thấy, nghe thấy, ngửi thấy.
    """
    data = get_van_vat_chi_tiet(hanh, truong_sinh_stage)
    if 'error' in data:
        return ""
    
    q = question.lower() if question else ""
    
    lines = []
    lines.append(f"🕵️ **THÁM TỬ LẮP GHÉP — {hanh} × {truong_sinh_stage}**")
    
    # Mô tả như thám tử nhìn thấy hiện trường
    tg = data.get('thi_giac', {})
    lines.append(f"👁️ **Nhìn thấy:** Một vật có hình dáng {data['hinh_dang']}, kích thước {data['kich_thuoc']}. "
                 f"Màu sắc {tg.get('mau', data['mau_sac'])}. Bề mặt {tg.get('be_mat', '')}. "
                 f"Tình trạng: {data['tinh_trang']}.")
    
    ag = data.get('thinh_giac', {})
    lines.append(f"👂 **Nghe thấy:** {ag.get('am_thanh', 'Im lặng')}.")
    
    kg = data.get('khuu_giac', {})
    lines.append(f"👃 **Ngửi thấy:** {kg.get('mui', 'Không mùi')}.")
    
    vg = data.get('vi_giac', {})
    lines.append(f"👅 **Vị:** Liên quan đến vị {vg.get('vi', '?')}.")
    
    xg = data.get('xuc_giac', {})
    lines.append(f"✋ **Sờ thấy:** {xg.get('cam_giac', '?')}. Nhiệt độ: {data.get('nhiet_do', '?')}. "
                 f"Trọng lượng: {data.get('trong_luong', '?')}.")
    
    # Đồ vật khả nghi
    if data.get('do_vat_cu_the'):
        items = data['do_vat_cu_the'][:6]
        lines.append(f"🔮 **Đồ vật khả năng cao:** {', '.join(items)}")
    
    # Người liên quan
    cn = data.get('con_nguoi', {})
    if cn.get('mo_ta_tang'):
        lines.append(f"🧑 **Người liên quan:** {cn['mo_ta_tang']}")
    
    # V31.4: Thêm dữ liệu mở rộng
    try:
        from van_vat_mo_rong import VAN_VAT_MO_RONG, VAN_VAT_BO_SUNG
        expanded = VAN_VAT_MO_RONG.get(hanh, {})
        bo_sung = VAN_VAT_BO_SUNG.get(hanh, {})
        
        # Phương tiện
        pt = expanded.get('phuong_tien', {})
        pt_items = pt.get(truong_sinh_stage, pt.get('chung', []))
        if pt_items:
            lines.append(f"🚗 **Phương tiện:** {', '.join(pt_items[:5])}")
        
        # Trang phục
        tp = expanded.get('trang_phuc', {})
        tp_items = tp.get(truong_sinh_stage, tp.get('chung', []))
        if tp_items:
            lines.append(f"👔 **Trang phục:** {', '.join(tp_items[:5])}")
        
        # Thực phẩm
        food = expanded.get('thuc_pham_chi_tiet', {})
        food_items = food.get('chung', [])
        drink_items = food.get('do_uong', [])
        if food_items:
            lines.append(f"🍜 **Thực phẩm:** {', '.join(food_items[:6])}")
        if drink_items:
            lines.append(f"🥤 **Đồ uống:** {', '.join(drink_items[:5])}")
        
        # Khoáng sản
        ks = expanded.get('khoang_san', [])
        if ks:
            lines.append(f"💎 **Khoáng sản/Đá quý:** {', '.join(ks[:5])}")
        
        # Thể thao
        tt = expanded.get('the_thao', [])
        if tt:
            lines.append(f"⚽ **Thể thao:** {', '.join(tt[:5])}")
        
        # Cảm xúc
        cx = expanded.get('cam_xuc', [])
        if cx:
            lines.append(f"🎭 **Cảm xúc:** {', '.join(cx[:5])}")
        
        # Thời tiết
        tw = expanded.get('thoi_tiet', [])
        if isinstance(tw, list) and tw:
            lines.append(f"🌤️ **Thời tiết:** {', '.join(tw[:4])}")
        
        # V31.5: BỔ SUNG — Nội thất, Y tế, Tôn giáo, Địa lý, Cơ thể
        nt = bo_sung.get('noi_that', [])
        if nt:
            lines.append(f"🛋️ **Nội thất:** {', '.join(nt[:5])}")
        
        yt = bo_sung.get('y_te', [])
        if yt:
            lines.append(f"🏥 **Y tế:** {', '.join(yt[:5])}")
        
        tg_rel = bo_sung.get('ton_giao', [])
        if tg_rel:
            lines.append(f"⛪ **Tôn giáo:** {', '.join(tg_rel[:5])}")
        
        dl = bo_sung.get('dia_ly', [])
        if dl:
            lines.append(f"🗻 **Địa lý:** {', '.join(dl[:5])}")
        
        bp = bo_sung.get('bo_phan_co_the', [])
        if bp:
            lines.append(f"🦴 **Bộ phận cơ thể:** {', '.join(bp[:6])}")
        
        gd = bo_sung.get('gia_dung', [])
        if gd:
            lines.append(f"🏡 **Gia dụng:** {', '.join(gd[:5])}")
    except ImportError:
        pass
    
    # Xu hướng
    lines.append(f"📈 **Xu hướng:** {data.get('xu_huong', '?')}")
    
    return "\n".join(lines)


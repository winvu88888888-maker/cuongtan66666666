# -*- coding: utf-8 -*-
"""
VẠN VẬT LOẠI TƯỢNG - BẢNG PHÂN LOẠI NGŨ HÀNH TOÀN DIỆN
Bao gồm: Ngũ Hành cơ bản, Bát Quái tượng, và các phân loại mở rộng
Tham chiếu: Hoàng Đế Nội Kinh, Kinh Dịch, Mai Hoa Dịch Số, Thiết Bản Thần Toán
"""

import streamlit as st

# ======================================================================
# BẢNG 1: NGŨ HÀNH VẠN VẬT LOẠI TƯỢNG (5 cột: Mộc, Hỏa, Thổ, Kim, Thủy)
# ======================================================================
NGU_HANH_LOAI_TUONG = {
    "headers": ["Phân Loại", "🌳 MỘC", "🔥 HỎA", "🏔️ THỔ", "⚔️ KIM", "💧 THỦY"],
    "rows": [
        # === THIÊN VĂN & THỜI GIAN ===
        ["Thiên Can", "Giáp, Ất", "Bính, Đinh", "Mậu, Kỷ", "Canh, Tân", "Nhâm, Quý"],
        ["Địa Chi", "Dần, Mão", "Tỵ, Ngọ", "Thìn, Tuất, Sửu, Mùi", "Thân, Dậu", "Hợi, Tý"],
        ["Phương Vị", "Đông", "Nam", "Trung ương", "Tây", "Bắc"],
        ["Mùa", "Xuân", "Hạ", "Trưởng Hạ (cuối hạ)", "Thu", "Đông"],
        ["Tháng", "Tháng 1, 2", "Tháng 4, 5", "Tháng 3, 6, 9, 12", "Tháng 7, 8", "Tháng 10, 11"],
        ["Ngày", "Giáp Ất", "Bính Đinh", "Mậu Kỷ", "Canh Tân", "Nhâm Quý"],
        ["Giờ", "Dần, Mão (3-7h)", "Tỵ, Ngọ (9-13h)", "Thìn Tuất Sửu Mùi", "Thân, Dậu (15-19h)", "Hợi, Tý (21-1h)"],
        ["Thiên Thời", "Gió", "Nóng, Nắng", "Ẩm, Sương mù", "Lạnh, Sương giá", "Mưa, Tuyết"],

        # === NGŨ SẮC, NGŨ VỊ, NGŨ ÂM ===
        ["Ngũ Sắc", "Xanh lá", "Đỏ", "Vàng", "Trắng", "Đen"],
        ["Ngũ Vị", "Chua", "Đắng", "Ngọt", "Cay", "Mặn"],
        ["Ngũ Âm", "Giốc (角)", "Chủy (徵)", "Cung (宫)", "Thương (商)", "Vũ (羽)"],
        ["Ngũ Khí", "Phong (gió)", "Nhiệt (nóng)", "Thấp (ẩm)", "Táo (khô)", "Hàn (lạnh)"],
        ["Ngũ Hóa", "Sinh", "Trưởng", "Hóa", "Thu", "Tàng"],

        # === NHÂN THỂ - Y HỌC ===
        ["Ngũ Tạng", "Gan", "Tim", "Tỳ (Lách)", "Phổi", "Thận"],
        ["Ngũ Phủ", "Mật", "Ruột non", "Dạ dày", "Ruột già", "Bàng quang"],
        ["Ngũ Quan", "Mắt", "Lưỡi", "Miệng", "Mũi", "Tai"],
        ["Ngũ Thể", "Gân", "Mạch máu", "Thịt", "Da, Lông", "Xương"],
        ["Ngũ Chí (Tình)", "Giận (Nộ)", "Vui (Hỷ)", "Lo (Tư)", "Buồn (Bi)", "Sợ (Khủng)"],
        ["Ngũ Dịch", "Nước mắt", "Mồ hôi", "Nước dãi", "Nước mũi", "Nước bọt"],
        ["Tật Bệnh", "Bệnh gan, mắt, gân cơ", "Bệnh tim, huyết áp", "Bệnh dạ dày, tiêu hóa", "Bệnh phổi, da liễu", "Bệnh thận, xương khớp"],

        # === TÍNH TÌNH & ĐẠO ĐỨC ===
        ["Tính Tình", "Nhân từ, hiền lành", "Lễ phép, nhiệt tình", "Thành tín, trung thực", "Nghĩa khí, cương trực", "Trí tuệ, thông minh"],
        ["Ngũ Đức", "Nhân (仁)", "Lễ (禮)", "Tín (信)", "Nghĩa (義)", "Trí (智)"],
        ["Ngũ Thường", "Mộc đức", "Hỏa đức", "Thổ đức", "Kim đức", "Thủy đức"],

        # === ĐỊA LÝ ===
        ["Địa Lý", "Rừng, vườn, sông suối", "Núi lửa, sa mạc nóng", "Đồng bằng, đất ruộng", "Mỏ kim loại, núi đá", "Ao hồ, sông biển"],
        ["Hình Thái", "Cao, thẳng, dài", "Nhọn, tam giác", "Vuông, bằng phẳng", "Tròn, hình cung", "Uốn lượn, bất định"],

        # === VẠN VẬT ===
        ["Nhân Vật", "Người hiền, học giả", "Tướng quân, chiến sĩ", "Nông dân, trưởng giả", "Thợ kim hoàn, quân nhân", "Ngư dân, thương gia"],
        ["Động Vật", "Hổ, Mèo, Thỏ", "Ngựa, Rắn, Phượng", "Trâu, Bò, Chó", "Gà, Khỉ, Hạc", "Chuột, Lợn, Cá"],
        ["Thực Vật", "Tre, Tùng, Liễu", "Hoàng hoa, Hướng dương", "Lúa, Ngô, Khoai", "Cúc, phong lan", "Sen, Rong, Tảo"],
        ["Đồ Ăn", "Rau xanh, đồ chua", "Đồ nướng, đồ đắng", "Ngũ cốc, đồ ngọt", "Đồ cay, gia vị", "Hải sản, đồ mặn"],
        ["Tĩnh Vật", "Gỗ, giấy, sách", "Đèn, nến, điện tử", "Gạch, đất, gốm sứ", "Kim loại, dao, kéo", "Bình nước, gương"],
        ["Số", "3, 8", "2, 7", "5, 10", "4, 9", "1, 6"],

        # === XẾP HẠNG VƯỢNG SUY ===
        ["Vượng ở mùa", "Xuân (T1-3)", "Hạ (T4-6)", "Tứ Quý (cuối mùa)", "Thu (T7-9)", "Đông (T10-12)"],
        ["Tương Sinh", "Thủy sinh Mộc", "Mộc sinh Hỏa", "Hỏa sinh Thổ", "Thổ sinh Kim", "Kim sinh Thủy"],
        ["Tương Khắc", "Kim khắc Mộc", "Thủy khắc Hỏa", "Mộc khắc Thổ", "Hỏa khắc Kim", "Thổ khắc Thủy"],
    ]
}

# ======================================================================
# BẢNG 2: BÁT QUÁI VẠN VẬT LOẠI TƯỢNG (Kinh Dịch + Mai Hoa + Thiết Bản)
# ======================================================================
BAT_QUAI_LOAI_TUONG = {
    "headers": ["Phân Loại", "☰ CÀN", "☱ ĐOÀI", "☲ LY", "☳ CHẤN", "☴ TỐN", "☵ KHẢM", "☶ CẤN", "☷ KHÔN"],
    "rows": [
        # === CƠ BẢN ===
        ["Ngũ Hành", "Kim", "Kim", "Hỏa", "Mộc", "Mộc", "Thủy", "Thổ", "Thổ"],
        ["Tượng Thiên Nhiên", "Trời", "Đầm, Hồ", "Lửa, Mặt trời", "Sấm sét", "Gió", "Nước, Trăng", "Núi", "Đất"],
        ["Phương Vị", "Tây Bắc", "Tây", "Nam", "Đông", "Đông Nam", "Bắc", "Đông Bắc", "Tây Nam"],
        ["Số Tiên Thiên", "1", "2", "3", "4", "5", "6", "7", "8"],
        ["Số Hậu Thiên", "6", "7", "9", "3", "4", "1", "8", "2"],
        ["Mùa", "Cuối Thu", "Thu", "Hạ", "Xuân", "Đầu Hạ", "Đông", "Đầu Xuân", "Cuối Hạ"],
        # === GIA ĐÌNH ===
        ["Nhân Vật", "Cha, Vua, Lão ông", "Thiếu nữ, Ca sĩ", "Trung nữ, Văn nhân", "Trưởng nam, Quân nhân", "Trưởng nữ, Thương nhân", "Trung nam, Ngư dân", "Thiếu nam, Tăng lữ", "Mẹ, Hoàng hậu, Lão bà"],
        ["Quan Hệ", "Cha", "Con gái út", "Con gái giữa", "Con trai cả", "Con gái cả", "Con trai giữa", "Con trai út", "Mẹ"],
        ["Tuổi Tác", "Người già trên 60", "Thiếu nữ 15-30", "Trung nữ 30-45", "Thanh niên 30-45", "Phụ nữ 30-50", "Trung niên 30-50", "Thiếu niên 7-15", "Người già, bà cụ"],
        ["Dáng Người", "Cao lớn, oai phong, đầy đặn", "Nhỏ nhắn, má lúm, miệng đẹp", "Thon gầy, mắt sáng, da hồng", "Cao ráo, vai rộng, vẻ mạnh mẽ", "Cao gầy, tóc thưa", "Tròn mập, da ngăm đen", "Thấp, chắc khỏe, lưng dày", "Mập mạp, béo tốt, hiền từ"],
        # === TÍNH TÌNH ===
        ["Tính Cách", "Cương kiện, quyết đoán, lãnh đạo", "Vui vẻ, hòa nhã, khéo nói", "Sáng suốt, văn nhã, nóng tính", "Xông xáo, nóng nảy, phóng khoáng", "Linh hoạt, ưa tự do", "Thâm sâu, mưu trí", "Trầm tĩnh, bướng bỉnh", "Thuần hậu, bao dung, cần cù"],
        ["Tâm Lý", "Kiêu ngạo, tự tin", "Lạc quan, hưởng thụ", "Sốt ruột, hay lo", "Giận dữ, bốc đồng", "Do dự, hay thay đổi", "Lo sợ, đa nghi", "Cố chấp, ương bướng", "Hy sinh, nhẫn nhịn"],
        # === NHÂN THỂ CHI TIẾT ===
        ["Bộ Phận Cơ Thể", "Đầu, Phổi, Xương, Não", "Miệng, Răng, Lưỡi, Cổ họng", "Mắt, Tim, Máu, Mạch", "Chân, Gan, Tóc, Thần kinh", "Đùi, Mật, Hơi thở, Gân", "Tai, Thận, Bàng quang, Tủy", "Tay, Lưng, Ngón tay, Mũi", "Bụng, Tỳ, Dạ dày, Thịt"],
        ["Tật Bệnh", "Đau đầu, phổi, xương, gãy xương", "Bệnh miệng, răng, ho, viêm họng", "Bệnh mắt, tim, huyết áp, sốt", "Bệnh chân, gan, co giật, động kinh", "Cảm gió, dị ứng, cảm cúm", "Bệnh tai, thận, tiết niệu, lây nhiễm", "Bệnh tay, lưng, khớp, u bướu", "Bệnh bụng, dạ dày, tiêu hóa, béo phì"],
        # === NGHỀ NGHIỆP ===
        ["Nghề Nghiệp", "Lãnh đạo, CEO, Tổng thống, Sĩ quan cao cấp", "Ca sĩ, MC, Diễn viên, Luật sư, Thợ kim hoàn", "Giáo viên, Nhà văn, Họa sĩ, Nhiếp ảnh, Lính cứu hỏa", "Quân nhân, Cảnh sát, Phi công, Lái xe, VĐV", "Thương nhân, Tiếp viên, Du lịch, Ngoại giao", "Ngư dân, Thủy thủ, Trinh sát, Nhà nghiên cứu", "Tu sĩ, Bảo vệ, Địa ốc, Kiến trúc sư, Kho bãi", "Nông dân, Đầu bếp, Y tá, Giáo dục, Thợ xây"],
        # === ĐỘNG VẬT CHI TIẾT ===
        ["Động Vật", "Ngựa, Sư tử, Voi, Đại bàng, Thiên nga", "Dê, Gà mái, Khỉ, Vẹt, Chim sẻ", "Chim trĩ, Phượng hoàng, Cua, Tôm, Sò", "Rồng, Rắn hổ, Ong, Côn trùng bay", "Gà trống, Bướm, Chuồn chuồn, Chim ưng", "Lợn, Cá, Chuột, Rái cá, Ếch, Ba ba", "Chó, Hổ, Gấu, Trâu rừng, Rùa", "Trâu, Bò, Ngựa cái, Kiến, Mối, Giun"],
        # === THỰC VẬT ===
        ["Thực Vật", "Cây đại thụ, Tùng bách, Cây cổ thụ", "Hoa lan, Hoa cúc, Nho, Lê, Quả ngọt", "Hoa hồng đỏ, Hướng dương, Cà chua, Ớt", "Tre, Trúc, Rau xanh, Mầm non, Cây mọc nhanh", "Dây leo, Hành tỏi, Rau thơm, Gia vị", "Sen, Rong rêu, Tảo, Bèo, Lau sậy", "Nấm, Khoai, Củ, Cây lùn, Cây núi", "Lúa, Ngô, Đậu, Ngũ cốc, Bông vải"],
        # === ĐỒ DÙNG ===
        ["Đồ Dùng", "Đồng hồ, Mũ, Vương miện, Ngọc, Vàng", "Nhạc cụ, Loa, Micro, Chuông, Gương, Bát đĩa", "Sách, Tranh, Đèn, Nến, Kính mắt, Bản đồ", "Trống, Điện thoại, Máy tính, Loa, Đồ điện", "Quạt, Bút, Thước, Lưới, Dây thừng", "Rượu, Muối, Bút mực, Xô, Bình nước, Đồ lỏng", "Đá, Bàn, Ghế, Tủ, Kệ sách, Ví tiền", "Nồi, Vải, Chăn gối, Quần áo, Đồ gốm"],
        # === PHƯƠNG TIỆN ===
        ["Phương Tiện", "Máy bay, Siêu xe, Xe hạng sang", "Du thuyền nhỏ, Xe ca, Xe khách", "Xe cứu hỏa, Xe thể thao đỏ, Xe đua", "Xe tải, Tàu hỏa, Xe mô tô, Xe tăng", "Thuyền buồm, Drone, Xe đạp", "Tàu thủy, Tàu ngầm, Ca nô, Kayak", "Xe tải nặng, Xe ủi, Máy xúc", "Xe bò, Xe thồ, Cày máy, Xe hai bánh"],
        # === ĐỊA LÝ CHI TIẾT ===
        ["Địa Lý", "Kinh đô, Cung điện, Trụ sở chính phủ", "Đầm, Giếng, Karaoke, Nhà hát, Sân khấu", "Bếp, Chợ, Thư viện, Trường học, Rạp chiếu", "Rừng rậm, Nhà ga, Bến xe, Sân vận động", "Vườn cây, Bưu điện, Công ty, Cảng", "Sông, Suối sâu, Quán rượu, Bể bơi, Nhà tắm", "Núi, Chùa, Đền, Nhà kho, Phòng kín, Nhà tù", "Đồng ruộng, Bãi đất, Công trường, Nghĩa trang"],
        # === KIẾN TRÚC ===
        ["Kiến Trúc", "Nhà cao tầng, Biệt thự, Tòa nhà CP", "Nhà nhỏ xinh, Quán café, Tiệm bánh", "Nhà kính, Studio, Phòng triển lãm", "Nhà xưởng, Gara, Trung tâm thể thao", "Sảnh lớn, Hành lang, Siêu thị, Cửa hàng", "Hầm ngầm, Phòng tối, Nhà bếp, Tầng hầm", "Nhà kho, Phòng thiền, Am thất, Phòng nhỏ", "Nhà cấp 4, Lều trại, Nhà ngang, Nhà kho lớn"],
        # === THIÊN VĂN ===
        ["Thiên Thời", "Trời trong, Nắng đẹp, Sấm xa", "Mưa nhỏ, Sương, Ráng chiều", "Nắng gắt, Sấm chớp, Cầu vồng", "Sấm sét, Bão, Động đất, Lốc", "Gió, Mưa phùn, Lốc xoáy nhẹ", "Mưa lớn, Tuyết, Lũ lụt, Sương mù dày", "Mây đặc, Sương mù, Trời u ám", "Âm u, Mây đen, Nồm ẩm"],
        # === MÀU SẮC ===
        ["Sắc Thái", "Trắng, Vàng kim, Bạc", "Trắng, Hồng nhạt, Phấn", "Đỏ, Tím, Cam, Hồng đậm", "Xanh lá đậm, Xanh biếch", "Xanh lá nhạt, Pastel", "Đen, Xanh tối, Navy", "Nâu, Vàng đất, Be", "Vàng, Đen, Nâu đậm"],
        # === HÌNH DÁNG ===
        ["Hình Dáng", "Tròn, vòm, bầu", "Miệng mở, vỡ, khuyết", "Rỗng giữa, dính, bám", "Ngược lên, nẩy, bật", "Dài, thẳng, lan tỏa", "Cong, uốn lượn, chảy", "Vuông, khối, chồng chất", "Bằng phẳng, rộng, mỏng"],
        # === HƯƠNG VỊ ===
        ["Hương Vị", "Cay, nồng, mạnh", "Ngọt, thơm, thanh", "Đắng, khét, nóng", "Chua, chát", "Thơm nhẹ, dịu, mát", "Mặn, tanh", "Ngọt đất, bùi", "Ngọt béo, nhạt, bùi béo"],
        # === TÌNH HUỐNG ===
        ["Tình Huống CÁT", "Thăng tiến, đắc quyền, quý nhân phù trợ", "Vui, tiệc tùng, hợp tác thành công", "Thi đậu, thành danh, trí tuệ tỏa sáng", "Khởi nghiệp, đột phá, hành động quyết liệt", "Buôn bán lãi, giao dịch tốt, du lịch", "Mưu sự thành, vượt khó, bí mật thắng lợi", "Tu dưỡng, tích trữ, ẩn nhẫn chờ thời", "Thu hoạch, bình an, gia đình hòa thuận"],
        ["Tình Huống HUNG", "Kiêu ngạo, cô độc, cứng nhắc", "Cãi vã, lừa gạt bằng lời, khẩu thiệt", "Kiện tụng, cháy nổ, tách ly, phản bội", "Tai nạn, giận mất khôn, phá hoại", "Tin đồn, lừa đảo, gió chiều nào che đó", "Trộm cắp, rượu chè, tai nạn nước", "Bế tắc, cô lập, chia rẽ", "Lười biếng, yếu đuối, mất phương hướng"],
        # === PHONG THỦY ===
        ["Phong Thủy", "Cửa chính hướng TN, nhà cao, mái vòm", "Ao đầm trước nhà, cửa sổ hướng Tây", "Bếp lửa, đèn sáng, phòng khách phía Nam", "Cầu thang, cửa lớn, sân rộng phía Đông", "Cây xanh trước cửa, hành lang dài", "Nhà cạnh sông, bể nước, giếng", "Tường cao, đá trang trí, hướng ĐB", "Sân rộng, đất bằng, vườn hướng TN"],
        # === KIM LOẠI / KHOÁNG SẢN ===
        ["Kim Loại/KS", "Vàng ròng, Bạch kim, Ngọc, Kim cương", "Bạc, Đồng trắng, Pha lê, Thủy tinh", "Đồng đỏ, Sắt nóng, Than, Diêm sinh", "Sắt, Thép, Kẽm, Đồng thau", "Thiếc, Nhôm, Fiber, Gỗ quý", "Chì, Thủy ngân, Dầu mỏ, Nước khoáng", "Đá hoa cương, Thạch anh, Xi măng", "Đất sét, Gạch, Ngói, Gốm sứ"],
        # === ÂM THANH ===
        ["Âm Thanh", "Tiếng chuông, giọng trầm, tiếng vang", "Tiếng cười, tiếng hát, giọng trong", "Tiếng nổ, tiếng kêu, lách tách", "Tiếng sấm, tiếng trống, tiếng gầm", "Tiếng gió, thì thầm, vi vu", "Tiếng nước chảy, mưa, sóng", "Tiếng vọng, tiếng dội, đá rơi", "Tiếng trầm, tiếng thở, ru êm"],
        # === MÙI ===
        ["Mùi Hương", "Trầm hương, mùi cao cấp, kim loại", "Mùi hoa, trái cây ngọt, nước hoa nhẹ", "Mùi khói, mùi cháy, nồng nàn", "Mùi cỏ tươi, mùi đất sau mưa", "Mùi gỗ, lá cây, tinh dầu, thảo mộc", "Mùi tanh, ẩm mốc, biển", "Mùi đất, đá, sương núi", "Mùi bùn, ngũ cốc, rơm rạ"],
        # === THIẾT BỊ HIỆN ĐẠI ===
        ["Thiết Bị HĐ", "Máy tính C/C, Server, Robot, AI", "Loa bluetooth, Tai nghe, Micro, Karaoke", "TV, Màn hình, Camera, Đèn LED, Laser", "Máy phát điện, Pin, Sạc, Mô tơ điện", "Wifi, Router, Anten, Drone, Quạt", "Máy lọc nước, Máy giặt, Tủ lạnh", "USB, Ổ cứng, Két sắt, Tủ đông", "Máy cày, Nồi cơm, Lò vi sóng, Máy xay"],
    ]
}



# ======================================================================
# BẢNG 3: TỔNG HỢP KINH DỊCH - MAI HOA - THIẾT BẢN
# ======================================================================
KINH_DICH_MAI_HOA_THIET_BAN = {
    "kinh_dich": {
        "title": "☯️ KINH DỊCH - 8 QUẺ CƠ BẢN",
        "data": [
            {"quẻ": "☰ Càn", "hành": "Kim", "tượng": "Trời", "đức": "Kiện (Mạnh)", "ý_nghĩa": "Sáng tạo, cương kiện, quân tử"},
            {"quẻ": "☷ Khôn", "hành": "Thổ", "tượng": "Đất", "đức": "Thuận (Mềm)", "ý_nghĩa": "Bao dung, thuần hậu, tiếp nhận"},
            {"quẻ": "☳ Chấn", "hành": "Mộc", "tượng": "Sấm", "đức": "Động (Chuyển)", "ý_nghĩa": "Khởi đầu, hành động, chấn động"},
            {"quẻ": "☴ Tốn", "hành": "Mộc", "tượng": "Gió", "đức": "Nhập (Thấm)", "ý_nghĩa": "Thấm nhuần, linh hoạt, thuận theo"},
            {"quẻ": "☵ Khảm", "hành": "Thủy", "tượng": "Nước", "đức": "Hãm (Hiểm)", "ý_nghĩa": "Nguy hiểm, thâm sâu, trí tuệ"},
            {"quẻ": "☲ Ly", "hành": "Hỏa", "tượng": "Lửa", "đức": "Lệ (Sáng)", "ý_nghĩa": "Văn minh, sáng suốt, phụ thuộc"},
            {"quẻ": "☶ Cấn", "hành": "Thổ", "tượng": "Núi", "đức": "Chỉ (Dừng)", "ý_nghĩa": "Tĩnh lặng, kiên định, ẩn tu"},
            {"quẻ": "☱ Đoài", "hành": "Kim", "tượng": "Đầm", "đức": "Duyệt (Vui)", "ý_nghĩa": "Hòa vui, giao tiếp, khẩu tài"},
        ]
    },
    "mai_hoa": {
        "title": "🌸 MAI HOA DỊCH SỐ - QUY TẮC LOẠI TƯỢNG",
        "rules": [
            "SỐ → QUẺ: Càn(1), Đoài(2), Ly(3), Chấn(4), Tốn(5), Khảm(6), Cấn(7), Khôn(8)",
            "THƯỢNG QUÁI = (Số thượng ÷ 8) dư → Quẻ",
            "HẠ QUÁI = (Số hạ ÷ 8) dư → Quẻ",
            "ĐỘNG HÀO = (Tổng số ÷ 6) dư → Hào động",
            "THỂ DỤNG: Quẻ không chứa hào động = THỂ (mình). Quẻ chứa hào động = DỤNG (đối phương/sự việc)",
            "SINH KHẮC: Dụng sinh Thể → Cát. Thể khắc Dụng → Cát. Dụng khắc Thể → Hung.",
        ]
    },
    "thiet_ban": {
        "title": "📜 THIẾT BẢN THẦN TOÁN - NẠP ÂM NGŨ HÀNH",
        "nap_am_table": [
            ["Giáp Tý - Ất Sửu", "Hải Trung Kim", "Kim", "Vàng trong biển"],
            ["Bính Dần - Đinh Mão", "Lô Trung Hỏa", "Hỏa", "Lửa trong lò"],
            ["Mậu Thìn - Kỷ Tỵ", "Đại Lâm Mộc", "Mộc", "Cây rừng lớn"],
            ["Canh Ngọ - Tân Mùi", "Lộ Bàng Thổ", "Thổ", "Đất ven đường"],
            ["Nhâm Thân - Quý Dậu", "Kiếm Phong Kim", "Kim", "Vàng đầu kiếm"],
            ["Giáp Tuất - Ất Hợi", "Sơn Đầu Hỏa", "Hỏa", "Lửa đầu núi"],
            ["Bính Tý - Đinh Sửu", "Giản Hạ Thủy", "Thủy", "Nước dưới khe"],
            ["Mậu Dần - Kỷ Mão", "Thành Đầu Thổ", "Thổ", "Đất trên thành"],
            ["Canh Thìn - Tân Tỵ", "Bạch Lạp Kim", "Kim", "Vàng trong nến"],
            ["Nhâm Ngọ - Quý Mùi", "Dương Liễu Mộc", "Mộc", "Cây dương liễu"],
            ["Giáp Thân - Ất Dậu", "Tuyền Trung Thủy", "Thủy", "Nước trong suối"],
            ["Bính Tuất - Đinh Hợi", "Ốc Thượng Thổ", "Thổ", "Đất trên nóc"],
            ["Mậu Tý - Kỷ Sửu", "Tích Lịch Hỏa", "Hỏa", "Lửa sấm sét"],
            ["Canh Dần - Tân Mão", "Tùng Bách Mộc", "Mộc", "Cây tùng bách"],
            ["Nhâm Thìn - Quý Tỵ", "Trường Lưu Thủy", "Thủy", "Nước chảy dài"],
            ["Giáp Ngọ - Ất Mùi", "Sa Trung Kim", "Kim", "Vàng trong cát"],
            ["Bính Thân - Đinh Dậu", "Sơn Hạ Hỏa", "Hỏa", "Lửa dưới núi"],
            ["Mậu Tuất - Kỷ Hợi", "Bình Địa Mộc", "Mộc", "Cây đồng bằng"],
            ["Canh Tý - Tân Sửu", "Bích Thượng Thổ", "Thổ", "Đất trên vách"],
            ["Nhâm Dần - Quý Mão", "Kim Bạc Kim", "Kim", "Vàng lá bạc"],
            ["Giáp Thìn - Ất Tỵ", "Phúc Đăng Hỏa", "Hỏa", "Lửa đèn phật"],
            ["Bính Ngọ - Đinh Mùi", "Thiên Hà Thủy", "Thủy", "Nước sông Ngân"],
            ["Mậu Thân - Kỷ Dậu", "Đại Trạch Thổ", "Thổ", "Đất đầm lớn"],
            ["Canh Tuất - Tân Hợi", "Thoa Xuyến Kim", "Kim", "Vàng trang sức"],
            ["Nhâm Tý - Quý Sửu", "Tang Đố Mộc", "Mộc", "Cây dâu tằm"],
            ["Giáp Dần - Ất Mão", "Đại Khê Thủy", "Thủy", "Nước suối lớn"],
            ["Bính Thìn - Đinh Tỵ", "Sa Trung Thổ", "Thổ", "Đất trong cát"],
            ["Mậu Ngọ - Kỷ Mùi", "Thiên Thượng Hỏa", "Hỏa", "Lửa trên trời"],
            ["Canh Thân - Tân Dậu", "Thạch Lựu Mộc", "Mộc", "Cây thạch lựu"],
            ["Nhâm Tuất - Quý Hợi", "Đại Hải Thủy", "Thủy", "Nước biển lớn"],
        ]
    }
}


# ======================================================================
# RENDER FUNCTION CHO STREAMLIT
# ======================================================================
def render_van_vat_view():
    """Render toàn bộ bảng Vạn Vật Loại Tượng trong Streamlit"""

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 50%, #1e3a5f 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid #63b3ed;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    ">
        <h1 style="color: #fbd38d; margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            📊 VẠN VẬT LOẠI TƯỢNG
        </h1>
        <p style="color: #e2e8f0; font-size: 1.1rem; margin-top: 10px;">
            Bảng phân loại Vạn Vật theo Ngũ Hành & Bát Quái — Nền tảng Kinh Dịch, Mai Hoa, Thiết Bản
        </p>
    </div>
    """, unsafe_allow_html=True)

    # === TAB LAYOUT ===
    tab1, tab2, tab3 = st.tabs([
        "🌳🔥🏔️⚔️💧 Ngũ Hành Loại Tượng",
        "☯️ Bát Quái Loại Tượng",
        "📜 Kinh Dịch • Mai Hoa • Thiết Bản"
    ])

    # ─── TAB 1: NGŨ HÀNH ───
    with tab1:
        st.markdown("### 🌳🔥🏔️⚔️💧 BẢNG NGŨ HÀNH VẠN VẬT LOẠI TƯỢNG")
        st.markdown("> *Phân loại toàn bộ vạn vật trong vũ trụ theo 5 hành: Mộc, Hỏa, Thổ, Kim, Thủy*")

        # Color mapping for Ngũ Hành
        hanh_colors = {
            "MỘC": "#22c55e",
            "HỎA": "#ef4444",
            "THỔ": "#eab308",
            "KIM": "#f8fafc",
            "THỦY": "#3b82f6"
        }

        # Build HTML table
        html = """<div style="overflow-x: auto;">
        <table style="width:100%; border-collapse: collapse; font-size: 0.95rem;">
        <thead>
        <tr>"""

        # Headers
        header_colors = ["#334155", "#16a34a", "#dc2626", "#ca8a04", "#64748b", "#2563eb"]
        headers = NGU_HANH_LOAI_TUONG["headers"]
        for i, h in enumerate(headers):
            bg = header_colors[i] if i < len(header_colors) else "#334155"
            html += f'<th style="background:{bg};color:#fff;padding:12px 8px;text-align:center;font-weight:800;border:1px solid #475569;white-space:nowrap;">{h}</th>'
        html += "</tr></thead><tbody>"

        # Rows
        for row_idx, row in enumerate(NGU_HANH_LOAI_TUONG["rows"]):
            bg_row = "#f8fafc" if row_idx % 2 == 0 else "#e2e8f0"
            html += f'<tr style="background:{bg_row};">'
            for col_idx, cell in enumerate(row):
                if col_idx == 0:
                    # Category column
                    html += f'<td style="padding:10px 8px;font-weight:800;color:#1e293b;border:1px solid #cbd5e1;background:#f1f5f9;white-space:nowrap;">{cell}</td>'
                else:
                    html += f'<td style="padding:10px 8px;color:#1e293b;border:1px solid #cbd5e1;text-align:center;font-weight:600;">{cell}</td>'
            html += "</tr>"

        html += "</tbody></table></div>"
        st.markdown(html, unsafe_allow_html=True)

        # Sinh Khắc diagram
        st.markdown("---")
        st.markdown("### ♻️ VÒNG SINH KHẮC NGŨ HÀNH")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:#f0fdf4;border:2px solid #22c55e;border-radius:15px;padding:20px;">
                <h4 style="color:#16a34a;text-align:center;">✅ TƯƠNG SINH (Hỗ trợ)</h4>
                <p style="text-align:center;font-size:1.3rem;font-weight:800;color:#1e293b;">
                    💧→🌳→🔥→🏔️→⚔️→💧
                </p>
                <p style="text-align:center;color:#374151;font-weight:700;">
                    Thủy sinh Mộc → Mộc sinh Hỏa → Hỏa sinh Thổ → Thổ sinh Kim → Kim sinh Thủy
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:#fef2f2;border:2px solid #ef4444;border-radius:15px;padding:20px;">
                <h4 style="color:#dc2626;text-align:center;">❌ TƯƠNG KHẮC (Kìm hãm)</h4>
                <p style="text-align:center;font-size:1.3rem;font-weight:800;color:#1e293b;">
                    💧→🔥→⚔️→🌳→🏔️→💧
                </p>
                <p style="text-align:center;color:#374151;font-weight:700;">
                    Thủy khắc Hỏa → Hỏa khắc Kim → Kim khắc Mộc → Mộc khắc Thổ → Thổ khắc Thủy
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ─── TAB 2: BÁT QUÁI ───
    with tab2:
        st.markdown("### ☯️ BẢNG BÁT QUÁI VẠN VẬT LOẠI TƯỢNG")
        st.markdown("> *8 Quẻ cơ bản biểu tượng cho mọi hiện tượng tự nhiên và nhân sự*")

        # Build HTML table
        html2 = """<div style="overflow-x: auto;">
        <table style="width:100%; border-collapse: collapse; font-size: 0.9rem;">
        <thead>
        <tr>"""

        quai_colors = ["#334155", "#ca8a04", "#ca8a04", "#dc2626", "#16a34a", "#16a34a", "#2563eb", "#78716c", "#78716c"]
        headers2 = BAT_QUAI_LOAI_TUONG["headers"]
        for i, h in enumerate(headers2):
            bg = quai_colors[i] if i < len(quai_colors) else "#334155"
            html2 += f'<th style="background:{bg};color:#fff;padding:10px 6px;text-align:center;font-weight:800;border:1px solid #475569;white-space:nowrap;font-size:0.85rem;">{h}</th>'
        html2 += "</tr></thead><tbody>"

        for row_idx, row in enumerate(BAT_QUAI_LOAI_TUONG["rows"]):
            bg_row = "#f8fafc" if row_idx % 2 == 0 else "#e2e8f0"
            html2 += f'<tr style="background:{bg_row};">'
            for col_idx, cell in enumerate(row):
                if col_idx == 0:
                    html2 += f'<td style="padding:8px 6px;font-weight:800;color:#1e293b;border:1px solid #cbd5e1;background:#f1f5f9;white-space:nowrap;">{cell}</td>'
                else:
                    html2 += f'<td style="padding:8px 6px;color:#1e293b;border:1px solid #cbd5e1;text-align:center;font-weight:600;font-size:0.85rem;">{cell}</td>'
            html2 += "</tr>"

        html2 += "</tbody></table></div>"
        st.markdown(html2, unsafe_allow_html=True)

    # ─── TAB 3: KINH DỊCH + MAI HOA + THIẾT BẢN ───
    with tab3:
        data = KINH_DICH_MAI_HOA_THIET_BAN

        # --- KINH DỊCH ---
        st.markdown(f"### {data['kinh_dich']['title']}")
        kd_html = """<div style="overflow-x: auto;">
        <table style="width:100%;border-collapse:collapse;">
        <thead><tr>
            <th style="background:#1e3a5f;color:#fbd38d;padding:12px;border:1px solid #2c5282;">Quẻ</th>
            <th style="background:#1e3a5f;color:#fbd38d;padding:12px;border:1px solid #2c5282;">Ngũ Hành</th>
            <th style="background:#1e3a5f;color:#fbd38d;padding:12px;border:1px solid #2c5282;">Tượng</th>
            <th style="background:#1e3a5f;color:#fbd38d;padding:12px;border:1px solid #2c5282;">Đức</th>
            <th style="background:#1e3a5f;color:#fbd38d;padding:12px;border:1px solid #2c5282;">Ý Nghĩa</th>
        </tr></thead><tbody>"""

        hanh_badge = {"Kim": "#64748b", "Mộc": "#16a34a", "Hỏa": "#dc2626", "Thủy": "#2563eb", "Thổ": "#ca8a04"}
        for i, item in enumerate(data['kinh_dich']['data']):
            bg = "#f8fafc" if i % 2 == 0 else "#e2e8f0"
            badge_color = hanh_badge.get(item['hành'], '#334155')
            kd_html += f"""<tr style="background:{bg};">
                <td style="padding:10px;border:1px solid #cbd5e1;font-weight:800;font-size:1.1rem;text-align:center;">{item['quẻ']}</td>
                <td style="padding:10px;border:1px solid #cbd5e1;text-align:center;">
                    <span style="background:{badge_color};color:#fff;padding:4px 12px;border-radius:20px;font-weight:700;">{item['hành']}</span>
                </td>
                <td style="padding:10px;border:1px solid #cbd5e1;text-align:center;font-weight:700;">{item['tượng']}</td>
                <td style="padding:10px;border:1px solid #cbd5e1;text-align:center;font-weight:700;">{item['đức']}</td>
                <td style="padding:10px;border:1px solid #cbd5e1;font-weight:600;">{item['ý_nghĩa']}</td>
            </tr>"""
        kd_html += "</tbody></table></div>"
        st.markdown(kd_html, unsafe_allow_html=True)

        st.markdown("---")

        # --- MAI HOA ---
        st.markdown(f"### {data['mai_hoa']['title']}")
        for idx, rule in enumerate(data['mai_hoa']['rules'], 1):
            st.markdown(f"""
            <div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:10px 15px;margin:8px 0;border-radius:0 8px 8px 0;">
                <strong style="color:#92400e;">📌 Quy tắc {idx}:</strong>
                <span style="color:#451a03;font-weight:600;"> {rule}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # --- THIẾT BẢN 60 NẠP ÂM ---
        st.markdown(f"### {data['thiet_ban']['title']}")
        st.markdown("> *Bảng 60 Hoa Giáp Nạp Âm — Nền tảng Thiết Bản Thần Toán*")

        na_html = """<div style="overflow-x: auto;">
        <table style="width:100%;border-collapse:collapse;">
        <thead><tr>
            <th style="background:#7c2d12;color:#fef3c7;padding:10px;border:1px solid #9a3412;">Trụ Can Chi</th>
            <th style="background:#7c2d12;color:#fef3c7;padding:10px;border:1px solid #9a3412;">Nạp Âm</th>
            <th style="background:#7c2d12;color:#fef3c7;padding:10px;border:1px solid #9a3412;">Hành</th>
            <th style="background:#7c2d12;color:#fef3c7;padding:10px;border:1px solid #9a3412;">Ý Nghĩa</th>
        </tr></thead><tbody>"""

        for i, row in enumerate(data['thiet_ban']['nap_am_table']):
            bg = "#fefce8" if i % 2 == 0 else "#fff7ed"
            badge_color = hanh_badge.get(row[2], '#334155')
            na_html += f"""<tr style="background:{bg};">
                <td style="padding:8px;border:1px solid #fed7aa;font-weight:700;white-space:nowrap;">{row[0]}</td>
                <td style="padding:8px;border:1px solid #fed7aa;font-weight:800;color:#7c2d12;">{row[1]}</td>
                <td style="padding:8px;border:1px solid #fed7aa;text-align:center;">
                    <span style="background:{badge_color};color:#fff;padding:3px 10px;border-radius:15px;font-weight:700;font-size:0.85rem;">{row[2]}</span>
                </td>
                <td style="padding:8px;border:1px solid #fed7aa;font-weight:600;color:#451a03;">{row[3]}</td>
            </tr>"""
        na_html += "</tbody></table></div>"
        st.markdown(na_html, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #fcd34d;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
        text-align: center;
        font-weight: 700;
        border-bottom: 4px solid #f59e0b;
    ">
        📊 Vạn Vật Loại Tượng — Tham khảo: Hoàng Đế Nội Kinh, Kinh Dịch, Mai Hoa Dịch Số, Thiết Bản Thần Toán
    </div>
    """, unsafe_allow_html=True)

# ======================================================================
# HELPER FUNCTIONS CHO AI (GEMINI)
# ======================================================================
def get_ngu_hanh_tuong(hanh_name):
    """
    Trích xuất Vạn Vật Loại Tượng theo Ngũ Hành để đưa vào Prompt AI.
    hanh_name: 'Mộc', 'Hỏa', 'Thổ', 'Kim', 'Thủy'
    """
    if not hanh_name: return ""
    
    hanh_name_upper = str(hanh_name).strip().upper()
    
    # Mapping index in table (MỘC:1, HỎA:2, THỔ:3, KIM:4, THỦY:5)
    hanh_map = {
        "MỘC": 1, "MOC": 1,
        "HỎA": 2, "HOA": 2,
        "THỔ": 3, "THO": 3,
        "KIM": 4,
        "THỦY": 5, "THUY": 5
    }
    
    idx = None
    for k, v in hanh_map.items():
        if hanh_name_upper in k or k in hanh_name_upper:
            idx = v
            break
            
    if idx is None: return ""
    
    tuong_list = []
    for row in NGU_HANH_LOAI_TUONG["rows"]:
        category = row[0]
        if len(row) > idx:
            tuong_list.append(f"- {category}: {row[idx]}")
            
    hanh_display = ["?", "Mộc", "Hỏa", "Thổ", "Kim", "Thủy"][idx]
    return f"TƯỢNG NGŨ HÀNH [{hanh_display}]:\n" + "\n".join(tuong_list) if tuong_list else ""


def get_bat_quai_tuong(quai_name):
    """
    Trích xuất Vạn Vật Loại Tượng theo Bát Quái để đưa vào Prompt AI.
    quai_name: 'Càn', 'Đoài', 'Ly', 'Chấn', 'Tốn', 'Khảm', 'Cấn', 'Khôn' hoặc chứa số cung (e.g. 'Cung 1')
    """
    if not quai_name: return ""
    
    quai_name_upper = str(quai_name).strip().upper()
    
    # Mapping index: CÀN:1, ĐOÀI:2, LY:3, CHẤN:4, TỐN:5, KHẢM:6, CẤN:7, KHÔN:8
    # Map số cung Lạc Thư → Bát Quái (1:Khảm, 2:Khôn, 3:Chấn, 4:Tốn, 6:Càn, 7:Đoài, 8:Cấn, 9:Ly)
    quai_map = {
        "CÀN": 1, "CAN": 1, "CUNG 6": 1,
        "ĐOÀI": 2, "DOAI": 2, "CUNG 7": 2,
        "LY": 3, "CUNG 9": 3,
        "CHẤN": 4, "CHAN": 4, "CUNG 3": 4,
        "TỐN": 5, "TON": 5, "CUNG 4": 5,
        "KHẢM": 6, "KHAM": 6, "CUNG 1": 6,
        "CẤN": 7, "CUNG 8": 7,
        "KHÔN": 8, "KHON": 8, "CUNG 2": 8
    }
    
    idx = None
    for k, v in quai_map.items():
        if quai_name_upper == k or k in quai_name_upper:
            idx = v
            break
            
    if idx is None: return ""
    
    quai_ten = BAT_QUAI_LOAI_TUONG["headers"][idx].replace("☰", "").replace("☱", "").replace("☲", "").replace("☳", "").replace("☴", "").replace("☵", "").replace("☶", "").replace("☷", "").strip()

    tuong_list = []
    for row in BAT_QUAI_LOAI_TUONG["rows"]:
        category = row[0]
        if len(row) > idx:
            tuong_list.append(f"- {category}: {row[idx]}")
            
    return f"TƯỢNG BÁT QUÁI [{quai_ten}]:\n" + "\n".join(tuong_list) if tuong_list else ""


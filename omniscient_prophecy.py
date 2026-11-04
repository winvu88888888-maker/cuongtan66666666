"""

omniscient_prophecy.py — V99.0: Engine Tiên Tri Toàn Tri 360° (Omniscient Forensic Decoder)

Giải mã toàn diện MỌI SỰ VIỆC từ 6 Phương Pháp Huyền Học (Kỳ Môn, Lục Hào, Mai Hoa, Lục Nhâm, Thái Ất, Thiết Bản):

1. Sự việc gì chi tiết (Nguyên nhân Quá khứ - Ẩn tình Hiện tại - Kết cục Tương lai - Cách cục 81 cục & Quẻ Dịch)

2. Xảy ra lúc nào (Năm - Tháng - Ngày Dương/Âm - Thứ - Giờ Địa Chi - Khắc 15 phút - Phút đuôi Hà Đồ)

3. Ở đâu (Phương hướng 8 cung + 24 Sơn La Kinh + Khoảng cách mét/km Nội/Ngoại bàn + Độ cao/Tầng + Mô tả hiện trường)

4. Con người (Trai hay Gái [Biểu quyết 5 tầng], Già hay Trẻ, Bao nhiêu tuổi cụ thể, Ngoại hình, Tính cách, Nghề nghiệp, Quen hay Lạ)

5. Đồ vật & Hiện tượng (Đồ vật gì, Màu sắc, Chất liệu, Hình dáng, Kích thước, Tình trạng Mới/Cũ, Số lượng, Giá trị)

6. Cơ thể, Sức khỏe & Pháp quyết Hóa giải

"""



import datetime



try:

    from blind_reading import STAR_READINGS, DOOR_READINGS, DEITY_READINGS, PALACE_ELEMENTS, STEM_COMBINATIONS

except Exception:

    STAR_READINGS, DOOR_READINGS, DEITY_READINGS, PALACE_ELEMENTS, STEM_COMBINATIONS = {}, {}, {}, {}, {}



try:

    from qmdg_inference_rules import (

        CUNG_DIRECTION_DETAIL, STAR_PERSONALITY, DOOR_PERSONALITY, DEITY_PERSONALITY,

        BAT_QUAI_OBJECT, BAT_QUAI_BODY_DISEASE, STAR_DISEASE, CAN_BODY,

    )

except Exception:

    CUNG_DIRECTION_DETAIL, STAR_PERSONALITY, DOOR_PERSONALITY, DEITY_PERSONALITY = {}, {}, {}, {}

    BAT_QUAI_OBJECT, BAT_QUAI_BODY_DISEASE, STAR_DISEASE, CAN_BODY = {}, {}, {}, {}



try:

    from van_vat import get_van_vat_chi_tiet, get_tham_tu_mo_ta

except Exception:

    def get_van_vat_chi_tiet(*a, **kw): return {}

    def get_tham_tu_mo_ta(*a, **kw): return ""



# ═══ BẢNG TRA CỨU CỐT LÕI V99 ═══

CUNG_INFO = {

    1: {

        'quai': 'Khảm', 'hanh': 'Thủy', 'am_duong': 'Dương', 'gender': 'Nam (Trung Nam)',

        'age_group': 'Trung niên / Thanh tráng niên (25 – 45 tuổi)', 'base_ages': [26, 31, 36, 41],

        'huong': 'Chính Bắc', 'son_24': 'Nhâm – Tý – Quý (337.5° – 22.5°)',

        'dist_near': '10m – 60m', 'dist_mid': '600m – 1.6km', 'dist_far': '6km – 60km',

        'places': 'Gần sông hồ, ao suối, bể nước, phòng tắm, quán nước, trạm xăng, nơi ẩm thấp hoặc đường ngầm/cống rãnh',

        'objects': 'Chất lỏng, nước uống, dầu nhớt, rượu bia, thủy hải sản, máy bơm, ống nước, thiết bị lạnh, xe cộ lưu thông',

    },

    2: {

        'quai': 'Khôn', 'hanh': 'Thổ', 'am_duong': 'Âm', 'gender': 'Nữ (Lão Mẫu / Phụ nữ lớn tuổi)',

        'age_group': 'Người lớn tuổi / Già (50 – 75 tuổi)', 'base_ages': [50, 55, 62, 68],

        'huong': 'Tây Nam', 'son_24': 'Mùi – Khôn – Thân (202.5° – 247.5°)',

        'dist_near': '20m – 80m', 'dist_mid': '800m – 2.5km', 'dist_far': '8km – 50km',

        'places': 'Vùng đất trống, cánh đồng, công trường, kho bãi, nhà trệt, chợ nông sản, góc nhà kho, nơi chứa đồ cũ',

        'objects': 'Đất cát, gạch ngói, gốm sứ, vải vóc, quần áo, túi xách, bao tải, lương thực, ngũ cốc, đồ gia dụng bằng đất/đá',

    },

    3: {

        'quai': 'Chấn', 'hanh': 'Mộc', 'am_duong': 'Dương', 'gender': 'Nam (Trưởng Nam / Nam thanh niên)',

        'age_group': 'Thanh niên / Trung niên trẻ (22 – 40 tuổi)', 'base_ages': [23, 28, 33, 38],

        'huong': 'Chính Đông', 'son_24': 'Giáp – Mão – Ất (67.5° – 112.5°)',

        'dist_near': '30m – 80m', 'dist_mid': '300m – 3.0km', 'dist_far': '13km – 38km',

        'places': 'Đường lớn đông đúc, ngã tư, chợ búa ồn ào, rừng cây, vườn gỗ, sân vận động, nhà máy cơ khí/nhạc cụ',

        'objects': 'Xe cộ, phương tiện di chuyển, đồ gỗ tươi, cây cảnh, loa đài, chuông trống, thiết bị phát âm thanh/rung động',

    },

    4: {

        'quai': 'Tốn', 'hanh': 'Mộc', 'am_duong': 'Âm', 'gender': 'Nữ (Trưởng Nữ / Phụ nữ trẻ - trung niên)',

        'age_group': 'Thanh niên / Trung niên (24 – 42 tuổi)', 'base_ages': [24, 29, 34, 42],

        'huong': 'Đông Nam', 'son_24': 'Thìn – Tốn – Tị (112.5° – 157.5°)',

        'dist_near': '40m – 90m', 'dist_mid': '400m – 4.5km', 'dist_far': '14km – 45km',

        'places': 'Hành lang, cầu thang, bưu điện, văn phòng giao dịch, cửa sổ, nơi nhiều gió, vườn hoa, tiệm thuốc/thảo dược',

        'objects': 'Giấy tờ, sổ sách, hợp đồng, tiền giấy, dây cáp, sợi dây, quạt máy, máy bay/drone, hương liệu, thuốc đông y',

    },

    5: {

        'quai': 'Khôn (Trung Cung)', 'hanh': 'Thổ', 'am_duong': 'Âm', 'gender': 'Trung tính / Nữ hoặc Người nắm quyền trung tâm',

        'age_group': 'Trung niên (35 – 55 tuổi)', 'base_ages': [35, 40, 45, 50],

        'huong': 'Trung Tâm (Giữa nhà / Giữa khu vực)', 'son_24': 'Trung Cung (Tâm điểm 0°)',

        'dist_near': 'Ngay tại chỗ (0m – 15m)', 'dist_mid': '100m – 500m', 'dist_far': '5km – 10km',

        'places': 'Phòng khách chính, sảnh trung tâm, trụ sở chính, két sắt trung tâm, gầm nền nhà',

        'objects': 'Tài sản cất giữ ở trung tâm, két sắt, đồ vật chôn giấu, hồ sơ lõi, đá quý/vàng bạc tích trữ',

    },

    6: {

        'quai': 'Càn', 'hanh': 'Kim', 'am_duong': 'Dương', 'gender': 'Nam (Lão Phụ / Người đàn ông lớn tuổi, có chức quyền)',

        'age_group': 'Người lớn tuổi / Già (52 – 80 tuổi)', 'base_ages': [54, 60, 66, 72],

        'huong': 'Tây Bắc', 'son_24': 'Tuất – Càn – Hợi (292.5° – 337.5°)',

        'dist_near': '60m – 100m', 'dist_mid': '600m – 6.0km', 'dist_far': '16km – 60km',

        'places': 'Cơ quan công quyền, tòa nhà cao tầng, trụ sở lớn, ngân hàng, đền đài, nơi sang trọng hoặc vùng đất cao ráo',

        'objects': 'Vàng bạc, đá quý, đồng hồ cao cấp, xe hơi sang, máy móc kim loại tròn, vương miện/mũ nón, con dấu, quyết định',

    },

    7: {

        'quai': 'Đoài', 'hanh': 'Kim', 'am_duong': 'Âm', 'gender': 'Nữ (Thiếu Nữ / Cô gái trẻ)',

        'age_group': 'Người trẻ / Thiếu nữ (12 – 28 tuổi)', 'base_ages': [16, 21, 24, 27],

        'huong': 'Chính Tây', 'son_24': 'Canh – Dậu – Tân (247.5° – 292.5°)',

        'dist_near': '20m – 70m', 'dist_mid': '700m – 2.7km', 'dist_far': '7km – 27km',

        'places': 'Quán cà phê, nhà hàng, karaoke, rạp hát, phòng khám răng/thẩm mỹ, tiệm vàng bạc, ao đầm nhỏ, nơi có tiếng nói cười',

        'objects': 'Trang sức kim loại, chìa khóa, tiền xu, dao kéo, dụng cụ phẫu thuật, cốc chén, loa/micro, đồ vật bị mẻ/khuyết góc',

    },

    8: {

        'quai': 'Cấn', 'hanh': 'Thổ', 'am_duong': 'Dương', 'gender': 'Nam (Thiếu Nam / Cậu bé hoặc Nam trẻ tuổi)',

        'age_group': 'Người trẻ / Thiếu niên (10 – 26 tuổi)', 'base_ages': [15, 18, 23, 26],

        'huong': 'Đông Bắc', 'son_24': 'Sửu – Cấn – Dần (22.5° – 67.5°)',

        'dist_near': '50m – 80m', 'dist_mid': '500m – 5.8km', 'dist_far': '15km – 58km',

        'places': 'Đồi núi, tòa nhà cao, bậc thềm, tường rào, ngã rẽ, chùa chiền, nghĩa trang, kho lưu trữ, ngân hàng/bất động sản',

        'objects': 'Đá phong thủy, gạch đá, bàn ghế cứng, tủ kệ cao, hộp kín, két sắt, gốm sứ dày, hồ sơ đóng gói kỹ',

    },

    9: {

        'quai': 'Ly', 'hanh': 'Hỏa', 'am_duong': 'Âm', 'gender': 'Nữ (Trung Nữ / Phụ nữ sành điệu, trí thức)',

        'age_group': 'Trung niên / Thanh niên (25 – 45 tuổi)', 'base_ages': [27, 32, 37, 43],

        'huong': 'Chính Nam', 'son_24': 'Bính – Ngọ – Đinh (157.5° – 202.5°)',

        'dist_near': '30m – 90m', 'dist_mid': '300m – 3.9km', 'dist_far': '9km – 39km',

        'places': 'Trường học, thư viện, phòng làm việc sáng sủa, nhà bếp, trạm biến áp, tiệm điện thoại/máy tính, showroom thời trang',

        'objects': 'Điện thoại, máy tính, màn hình, đèn chiếu sáng, pin/sạc, giấy tờ văn bằng, chứng chỉ, tranh ảnh, mỹ phẩm, kính mắt',

    },

}



CAN_GENDER_TRAIT = {

    'Giáp': ('Dương (Nam)', 'Cao lớn, thẳng thắn, có uy quyền, giữ vai trò đứng đầu'),

    'Ất': ('Âm (Nữ)', 'Mảnh mai, khéo léo, mềm mỏng, dáng người uyển chuyển, hay làm nghề y/nghệ thuật/văn phòng'),

    'Bính': ('Dương (Nam)', 'Nóng nảy, nhiệt tình, mặt hồng hào, mắt sáng, làm việc nhanh gọn'),

    'Đinh': ('Âm (Nữ)', 'Thông minh, sắc sảo, tinh tế, mắt có thần, hay nắm giữ thông tin/giấy tờ quan trọng'),

    'Mậu': ('Dương (Nam)', 'Đậm người, điềm đạm, trọng chữ tín, liên quan đến tiền vốn/bất động sản'),

    'Kỷ': ('Âm (Nữ)', 'Kín đáo, cẩn thận, tỉ mỉ, đôi khi có tâm tư riêng hoặc tính toán ngầm'),

    'Canh': ('Dương (Nam)', 'Góc cạnh, cứng rắn, quyết đoán, có tính đối kháng hoặc làm ngành kỹ thuật/công an/luật'),

    'Tân': ('Âm (Nữ)', 'Sắc sảo, cầu toàn, thích trang sức/làm đẹp, dễ vướng vào thay đổi/lỗi nhỏ'),

    'Nhâm': ('Dương (Nam)', 'Linh hoạt, hay di chuyển, giao tiếp rộng, suy nghĩ biến hóa khôn lường'),

    'Quý': ('Âm (Nữ)', 'Trầm tĩnh, nhạy cảm, kín tiếng, giỏi che giấu cảm xúc hoặc làm việc hậu trường'),

}



STAR_GENDER = {

    'Bồng': ('Nam', 'Thông minh mưu lược, táo bạo, thích mạo hiểm, da ngăm hoặc mắt sắc'),

    'Nhuế': ('Nữ', 'Trầm tính, cẩn trọng, có thể đang mệt mỏi/có bệnh hoặc đang học tập'),

    'Xung': ('Nam', 'Nhanh nhẹn, nóng vội, hành động dứt khoát, thích thể thao/tốc độ'),

    'Phụ': ('Nữ / Nam văn nhã', 'Có học thức, lịch sự, nho nhã, làm giáo dục/văn hóa/tư vấn'),

    'Cầm': ('Nam / Trung tính', 'Đĩnh đạc, trung hậu, có uy tín, làm quản lý/điều phối'),

    'Tâm': ('Nam', 'Có tài lãnh đạo, mưu trí, bác sĩ/chuyên gia/quản trị giỏi'),

    'Trụ': ('Nữ', 'Ăn nói sắc bén, có cá tính mạnh, làm luật/ca sĩ/kinh doanh tự do'),

    'Nhậm': ('Nam', 'Chịu thương chịu khó, thật thà, kiên trì, dáng hơi thấp đậm'),

    'Anh': ('Nữ', 'Nổi bật, ưa hình thức, nóng tính, làm truyền thông/làm đẹp/điện tử'),

}



HAO_HEIGHT_MAP = {

    1: 'Sát mặt đất, gầm bàn/gầm giường, tầng trệt/tầng hầm, ngăn kéo dưới cùng (0m – 0.5m)',

    2: 'Thấp ngang đầu gối – thắt lưng, trong nhà chính, tầng 1, kệ dưới (0.5m – 1.0m)',

    3: 'Ngang bụng – ngực, ngay lối ra vào/cửa phòng, tầng 2 hoặc tầng lửng (1.0m – 1.5m)',

    4: 'Ngang ngực – vai, gần cửa sổ/hành lang ngoài, tầng 3 – 4, ngăn tủ trên (1.5m – 2.0m)',

    5: 'Trên cao ngang đầu/mắt, vị trí trang trọng/phòng làm việc chính, tầng 5 hoặc tầng áp mái (2.0m – 3.0m)',

    6: 'Trên đỉnh cao nhất, nóc tủ, trần nhà, sân thượng, gác xép hoặc ở nơi rất xa ngoài biên (trên 3.0m)',

}



HANH_FORENSIC = {

    'Kim': {

        'mau_sac': 'Trắng, Bạc, Ánh kim, Vàng kim, Xám sáng',

        'chat_lieu': 'Kim loại, sắt thép, vàng bạc, hợp kim, inox, đá cứng, thủy tinh dày',

        'hinh_dang': 'Hình tròn, bầu dục, có cạnh sắc hoặc bề mặt bóng loáng',

        'do_vat': 'Tiền bạc, vàng trang sức, đồng hồ, chìa khóa, điện thoại vỏ kim loại, dao kéo, phụ tùng xe cộ, máy móc, con dấu',

        'nghe_nghiep': 'Tài chính - Ngân hàng, Cơ khí - Kỹ thuật, Kim hoàn, Công an - Quân đội - Luật pháp, Quản lý điều hành',

        'co_the': 'Phổi, hệ hô hấp, đại tràng, xương khớp, răng miệng, làn da, vùng đầu',

        'hoa_giai': 'Dùng hành Thủy (tiết Kim) hoặc hành Thổ (sinh Kim tùy hỷ kỵ); hướng Tây / Tây Bắc; màu Trắng / Đen xanh.',

    },

    'Mộc': {

        'mau_sac': 'Xanh lá cây, Xanh lục, Xanh ngọc, Màu gỗ tự nhiên',

        'chat_lieu': 'Gỗ, giấy, vải vóc, sợi dệt, tre nứa, thảo mộc, nhựa sinh học',

        'hinh_dang': 'Hình trụ dài, hình chữ nhật đứng, thon dài, có đốt hoặc vân sọc',

        'do_vat': 'Giấy tờ hồ sơ, hợp đồng, sách vở, tiền giấy, quần áo, túi vải, đồ nội thất gỗ, cây cảnh, thuốc thảo dược',

        'nghe_nghiep': 'Giáo dục - Đào tạo, Y dược, Văn phòng - Hành chính, Thiết kế - Thời trang, Nông lâm nghiệp, Nội thất',

        'co_the': 'Gan, mật, hệ thần kinh, mắt, gân cơ, tứ chi (tay chân), tóc',

        'hoa_giai': 'Dùng hành Thủy (tương sinh) hoặc hành Hỏa (thông minh sáng suốt); hướng Đông / Đông Nam; màu Xanh lá / Xanh dương.',

    },

    'Thủy': {

        'mau_sac': 'Đen, Xanh dương đậm, Xanh nước biển, Tím than, Trong suốt',

        'chat_lieu': 'Chất lỏng, nước, thủy tinh, pha lê, nhựa dẻo, hóa chất, dầu mỡ',

        'hinh_dang': 'Uốn lượn, mềm mại, không cố định hình khối, dạng chai lọ hoặc đường ống',

        'do_vat': 'Nước uống, rượu bia, mỹ phẩm dạng lỏng, xăng dầu, thiết bị lọc nước, hàng vận chuyển đường xa, sim số/dữ liệu mạng',

        'nghe_nghiep': 'Thương mại - Xuất nhập khẩu, Giao thông - Vận tải - Logistics, Du lịch - Dịch vụ, Thủy hải sản, Tài chính lưu động',

        'co_the': 'Thận, bàng quang, hệ bài tiết, tai, máu huyết, hệ sinh dục, vùng thắt lưng',

        'hoa_giai': 'Dùng hành Kim (sinh Thủy) hoặc hành Mộc (tiết khí); hướng Chính Bắc; màu Đen / Xanh biển / Trắng.',

    },

    'Hỏa': {

        'mau_sac': 'Đỏ, Hồng, Cam, Tím, Vàng rực, Phát sáng',

        'chat_lieu': 'Linh kiện điện tử, pin/nhiệt điện, nhựa tổng hợp, chất dễ cháy, đèn LED/laser',

        'hinh_dang': 'Hình tam giác, nhọn ở đầu, mỏng dẹt, phát sáng hoặc tỏa nhiệt',

        'do_vat': 'Điện thoại, máy tính, sạc dự phòng, thiết bị điện, giấy tờ văn bằng, chứng chỉ, con dấu đỏ, tranh ảnh, mỹ phẩm',

        'nghe_nghiep': 'Công nghệ thông tin (IT), Truyền thông - Marketing, Điện tử - Viễn thông, Nghệ thuật - Giải trí, Nhà hàng - Ẩm thực',

        'co_the': 'Tim mạch, huyết áp, mắt (thị lực), ruột non, hệ tuần hoàn, vùng ngực và trán',

        'hoa_giai': 'Dùng hành Mộc (sinh Hỏa) hoặc hành Thổ (hóa giải hỏa vượng); hướng Chính Nam; màu Đỏ / Tím / Xanh lá.',

    },

    'Thổ': {

        'mau_sac': 'Vàng đất, Nâu, Nâu đất, Be, Cam đất, Xám đá',

        'chat_lieu': 'Đất đá, gốm sứ, gạch ngói, bê tông, da thuộc, vải dày, khoáng sản',

        'hinh_dang': 'Hình vuông, khối hộp chắc chắn, dày dặn, nặng hoặc dạng túi/bao chứa',

        'do_vat': 'Sổ đỏ/giấy tờ nhà đất, két sắt, hộp tủ, ví da, túi xách, đồ gốm sứ, đá phong thủy, vật liệu xây dựng, nông sản',

        'nghe_nghiep': 'Bất động sản, Xây dựng - Kiến trúc, Kho bãi, Quản lý tài sản, Nông sản, Khai khoáng',

        'co_the': 'Dạ dày (Tỳ Vị), hệ tiêu hóa, cơ bắp, vùng bụng, lá lách, da thịt',

        'hoa_giai': 'Dùng hành Hỏa (tương sinh) hoặc hành Kim (tiết Tú khí); hướng Tây Nam / Đông Bắc / Trung tâm; màu Vàng / Nâu.',

    },

}





def _find_target_palace(dung_than, chart_data):

    """Xác định cung Dụng Thần và cung Sự Việc (Can Giờ) trên bàn Kỳ Môn."""

    if not chart_data or not isinstance(chart_data, dict):

        return 1, 1, 'Giáp', 'Giáp'

    can_ngay = chart_data.get('can_ngay', 'Giáp')

    can_gio = chart_data.get('can_gio', 'Giáp')

    ctb = chart_data.get('can_thien_ban', {}) or {}

    dia_ban = chart_data.get('dia_ban') or chart_data.get('dia_can', {}) or {}



    dt_can_map = {

        'Quan Quỷ': can_gio, 'Thê Tài': can_gio, 'Tử Tôn': can_gio,

        'Phụ Mẫu': chart_data.get('can_nam', can_gio),

        'Huynh Đệ': chart_data.get('can_thang', can_gio),

        'Bản Thân': can_ngay,

    }

    dt_can = dt_can_map.get(dung_than, can_gio) or can_gio



    def _locate_can(c_name):

        search_c = 'Mậu' if c_name == 'Giáp' else c_name

        for k, v in ctb.items():

            if v == search_c:

                try:

                    return int(k)

                except Exception:

                    pass

        for k, v in dia_ban.items():

            if v == search_c:

                try:

                    return int(k)

                except Exception:

                    pass

        return 1



    cung_dt = _locate_can(dt_can)

    cung_sv = _locate_can(can_gio)

    if cung_dt == 5:

        cung_dt = 2

    if cung_sv == 5:

        cung_sv = 2

    return cung_dt, cung_sv, dt_can, can_gio





def build_omniscient_prophecy(

    question='',

    dung_than='Bản Thân',

    hanh_dt='Thổ',

    weighted_pct=50,

    ts_stage='',

    ngu_khi='',

    chart_data=None,

    luc_hao_data=None,

    mai_hoa_data=None,

    ung_ky_detail=None,

    is_fake=False,

    auth_warnings=None,

):

    """

    Hàm trung tâm giải mã Tiên Tri Toàn Tri 360° cho mọi câu hỏi / mọi quẻ.

    Trả về dict: {'html': str, 'text': str, 'data': dict}

    """

    chart_data = chart_data if isinstance(chart_data, dict) else {}

    luc_hao_data = luc_hao_data if isinstance(luc_hao_data, dict) else {}

    mai_hoa_data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}

    ung_ky_detail = ung_ky_detail if isinstance(ung_ky_detail, dict) else {}



    cung_dt, cung_sv, dt_can, can_gio = _find_target_palace(dung_than, chart_data)

    _q_self_chk = (question or '').lower()

    _is_self_identity = any(w in _q_self_chk for w in ['tôi là', 'nam hay nữ', 'trai hay gái', 'giới tính', 'bao nhiêu tuổi', 'mấy tuổi', 'tuổi của tôi', 'bản thân tôi'])

    target_cung = cung_dt if (dung_than == 'Bản Thân' and _is_self_identity) else (cung_sv if (dung_than == 'Bản Thân' and cung_sv != cung_dt) else cung_dt)

    c_info = CUNG_INFO.get(target_cung, CUNG_INFO[1])



    if not hanh_dt or hanh_dt == '?':

        hanh_dt = c_info['hanh']

    h_forensic = HANH_FORENSIC.get(hanh_dt, HANH_FORENSIC['Thổ'])



    # Lấy Sao, Cửa, Thần, Can Thiên/Địa bàn tại cung trọng tâm

    tb = chart_data.get('thien_ban', {}) or {}

    nb = chart_data.get('nhan_ban', {}) or {}

    sb = chart_data.get('than_ban', {}) or {}

    ctb = chart_data.get('can_thien_ban', {}) or {}

    cdb = chart_data.get('dia_ban') or chart_data.get('dia_can', {}) or {}



    sao_name = str(tb.get(target_cung, tb.get(str(target_cung), 'Thiên Tâm')))

    cua_name = str(nb.get(target_cung, nb.get(str(target_cung), 'Khai Môn')))

    than_name = str(sb.get(target_cung, sb.get(str(target_cung), 'Trực Phù')))

    can_thien = str(ctb.get(target_cung, ctb.get(str(target_cung), dt_can or 'Mậu')))

    can_dia = str(cdb.get(target_cung, cdb.get(str(target_cung), can_gio or 'Mậu')))



    # Trích xuất Lục Hào & Mai Hoa

    lh_ban = luc_hao_data.get('ban', {}) if luc_hao_data else {}

    lh_bien = luc_hao_data.get('bien', {}) if luc_hao_data else {}

    ten_que_ban = lh_ban.get('name') or mai_hoa_data.get('ten_ban', 'Thuần Càn')

    ten_que_bien = lh_bien.get('name') or mai_hoa_data.get('ten_bien', '')

    ten_que_ho = mai_hoa_data.get('ten_ho', '')

    dong_hao_list = luc_hao_data.get('dong_hao') or (

        [mai_hoa_data.get('dong_hao')] if mai_hoa_data.get('dong_hao') else []

    )

    primary_dong_hao = int(dong_hao_list[0]) if dong_hao_list and str(dong_hao_list[0]).isdigit() else 3



    # Tìm hào Dụng Thần trong Lục Hào

    dt_hao_info = {}

    lh_haos = lh_ban.get('haos') or lh_ban.get('details') or lh_ban.get('lines') or []

    for idx_h, h_item in enumerate(lh_haos, 1):

        if not isinstance(h_item, dict):

            continue

        lt = h_item.get('luc_than', '')

        if lt == dung_than or (dung_than == 'Bản Thân' and 'Thế' in str(h_item.get('the_ung', ''))):

            dt_hao_info = dict(h_item)

            dt_hao_info['hao_so'] = idx_h

            break

    if not dt_hao_info and lh_haos and isinstance(lh_haos[0], dict):

        dt_hao_info = dict(lh_haos[min(primary_dong_hao - 1, len(lh_haos) - 1)])

        dt_hao_info['hao_so'] = primary_dong_hao



    hao_so = dt_hao_info.get('hao_so', primary_dong_hao)

    hao_chi = dt_hao_info.get('chi', '')

    hao_am_duong = str(dt_hao_info.get('am_duong', dt_hao_info.get('type', '')))



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 1: SỰ VIỆC CHI TIẾT & DIỄN BIẾN 3 THỜI (QUÁ KHỨ - HIỆN TẠI - TƯƠNG LAI)

    # ═════════════════════════════════════════════════════════════════════════

    # Tra cứu blind_reading cho Sao, Cửa, Thần, Cách cục

    star_desc = "Chuyển biến theo thiên thời"

    for k_s, v_s in STAR_READINGS.items():

        if k_s in sao_name:

            star_desc = v_s.get('Past_Reason', '') or v_s.get('Nature', '')

            break



    door_desc = "Sự việc đang vận động ở nhân gian"

    door_action = ""

    for k_d, v_d in DOOR_READINGS.items():

        if k_d in cua_name:

            door_desc = v_d.get('Current_Action', '')

            door_action = v_d.get('Hidden_Truth', '')

            break



    deity_desc = "Có yếu tố tâm linh/ẩn tình tác động"

    for k_th, v_th in DEITY_READINGS.items():

        if k_th in than_name:

            deity_desc = v_th.get('Secret_Factor', '')

            break



    stem_combo_desc = STEM_COMBINATIONS.get((can_thien, can_dia), '')

    if not stem_combo_desc:

        stem_combo_desc = f"Thiên bàn {can_thien} lâm Địa bàn {can_dia} tại cung {c_info['quai']} ({c_info['huong']})"



    verdict_word = (

        "ĐẠI CÁT — Thành công rực rỡ, thuận buồm xuôi gió" if weighted_pct >= 70 else

        "CÁT — Thuận lợi, đạt được mục tiêu" if weighted_pct >= 55 else

        "BÌNH / GIẰNG CO — Có cơ hội nhưng kèm thử thách, cần khéo léo xử lý" if weighted_pct >= 45 else

        "HUNG — Nhiều lực cản, dễ hao tổn hoặc chậm trễ" if weighted_pct >= 30 else

        "ĐẠI HUNG — Bế tắc lớn, nguy cơ thất bại hoặc mất mát nếu cố chấp"

    )



    event_past = (

        f"Khởi nguồn từ Quẻ Bản <b>{ten_que_ban}</b> (Cung {c_info['quai']} – Địa bàn <b>{can_dia}</b>, Sao <b>{sao_name}</b>): "

        f"{star_desc or 'Sự việc đã manh nha từ trước do nhu cầu thực tế hoặc tác động từ môi trường xung quanh.'}"

    )

    event_present = (

        f"Hiện tại ứng vào Quẻ Hỗ <b>{ten_que_ho or 'Trung gian'}</b>, Nhân bàn <b>Cửa {cua_name}</b> phối Thần <b>{than_name}</b> "

        f"(Cách cục <b>{can_thien}/{can_dia}</b>): {door_desc} {door_action} "

        f"Ẩn tình phía sau: <i>{deity_desc}</i> ({stem_combo_desc})."

    )

    event_future = (

        f"Tương lai chuyển sang Quẻ Biến <b>{ten_que_bien or ten_que_ban}</b> (Hào động {dong_hao_list or [primary_dong_hao]}, "

        f"Trường Sinh: <b>{ts_stage or 'Bình hòa'}</b>, Ngũ Khí: <b>{ngu_khi or 'Tướng'}</b>) → "

        f"Kết cục chốt tại mức <b>{weighted_pct}% ({verdict_word})</b>."

    )



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 2: THỜI ĐIỂM CHÍNH XÁC (NĂM - THÁNG - NGÀY - GIỜ - KHẮC - PHÚT)

    # ═════════════════════════════════════════════════════════════════════════

    uk_exact = ung_ky_detail.get('exact_timestamp', 'Đang hội tụ khí số')

    uk_minute = ung_ky_detail.get('minute', 'Khắc 2 (phút 15–30), đuôi phút 3, 8')

    uk_hour = ung_ky_detail.get('hour', 'Giờ Ngọ (11:00–13:00)')

    uk_day = ung_ky_detail.get('day', 'Trong 3 ngày tới')

    uk_month = ung_ky_detail.get('month', 'Tháng hiện tại')

    uk_year = ung_ky_detail.get('year', f'Năm {datetime.date.today().year}')

    uk_speed = ung_ky_detail.get('speed', '⚡ Ứng nghiệm theo chu kỳ Can Chi')



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 3: ĐỊA ĐIỂM, PHƯƠNG HƯỚNG & HIỆN TRƯỜNG (Ở ĐÂU)

    # ═════════════════════════════════════════════════════════════════════════

    am_duong_don = str(chart_data.get('am_duong_don', 'Dương Độn'))

    is_noi_ban = (

        (target_cung in (1, 8, 3, 4) and 'Dương' in am_duong_don) or

        (target_cung in (9, 2, 7, 6) and 'Âm' in am_duong_don)

    )

    ban_type_str = "Nội Bàn (Gần / Trong nhà / Nội bộ)" if is_noi_ban else "Ngoại Bàn (Xa / Ngoài đường / Khác khu vực)"

    dist_selected = f"{c_info['dist_near']} (trong nhà/cơ quan) hoặc {c_info['dist_mid']} (nội hạt)" if is_noi_ban else f"{c_info['dist_mid']} (khu vực lân cận) đến {c_info['dist_far']} (khác quận/tỉnh)"

    height_desc = HAO_HEIGHT_MAP.get(int(hao_so) if str(hao_so).isdigit() else 3, HAO_HEIGHT_MAP[3])



    where_summary = (

        f"Hướng <b>{c_info['huong']}</b> (Cung {c_info['quai']} – La Kinh 24 Sơn: <b>{c_info['son_24']}</b>) | "

        f"Phân vùng: <b>{ban_type_str}</b> | Khoảng cách dự kiến: <b>{dist_selected}</b>"

    )

    where_scene = (

        f"<b>Đặc điểm hiện trường:</b> {c_info['places']}. "

        f"<b>Vị trí độ cao / tầng (Hào {hao_so}):</b> {height_desc}."

    )



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 4: HỒ SƠ CON NGƯỜI (TRAI/GÁI, GIÀ/TRẺ, TUỔI, NGOẠI HÌNH, TÍNH CÁCH, QUEN/LẠ)

    # ═════════════════════════════════════════════════════════════════════════

    # Biểu quyết Giới tính từ 5 nguồn độc lập:

    male_votes = 0

    female_votes = 0

    gender_reasons = []



    # Nguồn 1: Bát Quái Cung Dụng Thần

    if c_info['am_duong'] == 'Dương':

        male_votes += 2

        gender_reasons.append(f"Cung {c_info['quai']} ({c_info['gender']})")

    else:

        female_votes += 2

        gender_reasons.append(f"Cung {c_info['quai']} ({c_info['gender']})")



    # Nguồn 2: Thiên Can Dụng Thần

    can_g_info = CAN_GENDER_TRAIT.get(can_thien, ('Dương (Nam)', 'Rõ ràng, chủ động'))

    if 'Dương' in can_g_info[0]:

        male_votes += 1

        gender_reasons.append(f"Can {can_thien} Dương")

    else:

        female_votes += 1

        gender_reasons.append(f"Can {can_thien} Âm")



    # Nguồn 3: Cửu Tinh

    star_g_matched = ('Nam', 'Nhanh nhạy, chủ động')

    for k_sg, v_sg in STAR_GENDER.items():

        if k_sg in sao_name:

            star_g_matched = v_sg

            if 'Nam' in v_sg[0]:

                male_votes += 1

            else:

                female_votes += 1

            gender_reasons.append(f"Sao {sao_name} ({v_sg[0]})")

            break



    # Nguồn 4: Hào Dụng Thần Âm/Dương

    if 'Dương' in hao_am_duong or '1' in hao_am_duong or '9' in hao_am_duong or '7' in hao_am_duong:

        male_votes += 1

        gender_reasons.append(f"Hào {hao_so} Dương")

    elif 'Âm' in hao_am_duong or '0' in hao_am_duong or '6' in hao_am_duong or '8' in hao_am_duong:

        female_votes += 1

        gender_reasons.append(f"Hào {hao_so} Âm")



    # Nguồn 5 (V100.2): Ngũ Hành Dụng Thần thực tế (Kim/Mộc/Hỏa thuộc khí Cương/Dương -> Nam; Thủy/Thổ thuộc khí Nhu/Âm -> Nữ) & Nhật Can Bản Mệnh

    if hanh_dt in ('Kim', 'Mộc', 'Hỏa'):

        male_votes += 2

        gender_reasons.append(f"Dụng Thần hành {hanh_dt} (Khí Cương Dương — Nam)")

    elif hanh_dt in ('Thủy', 'Thổ'):

        female_votes += 1

        gender_reasons.append(f"Dụng Thần hành {hanh_dt} (Khí Nhu Âm)")



    if dt_can and dt_can != can_thien:

        _dt_can_g = CAN_GENDER_TRAIT.get(dt_can, ('Dương (Nam)', ''))

        if 'Dương' in _dt_can_g[0]:

            male_votes += 1

            gender_reasons.append(f"Nhật Can {dt_can} Dương")

        else:

            female_votes += 1

            gender_reasons.append(f"Nhật Can {dt_can} Âm")



    # V99.7: Nhận diện trực tiếp Chủ Thể / Người Thân trong câu hỏi để tránh đoán sai giới tính & tuổi

    import re as _re_om

    _q_low_om = (question or "").lower()

    _MALE_KIN = ["ông nội", "ông ngoại", "ông tôi", "bố tôi", "cha tôi", "ba tôi", "bố", "cha", "chồng", "con trai", "anh trai", "em trai", "chú", "bác trai", "cậu", "dượng", "bạn trai"]

    _FEMALE_KIN = ["bà nội", "bà ngoại", "bà tôi", "mẹ tôi", "má tôi", "mẹ", "má", "vợ", "con gái", "chị gái", "em gái", "cô", "dì", "bác gái", "mợ", "bạn gái"]

    _matched_male_kin = next((w for w in _MALE_KIN if _re_om.search(r"(?:^|[\s,;.!?])" + _re_om.escape(w) + r"(?:[\s,;.!?]|$)", _q_low_om)), None)

    _matched_female_kin = next((w for w in _FEMALE_KIN if _re_om.search(r"(?:^|[\s,;.!?])" + _re_om.escape(w) + r"(?:[\s,;.!?]|$)", _q_low_om)), None)



    total_votes = max(male_votes + female_votes, 1)

    if _matched_male_kin:

        primary_gender = f"NAM GIỚI / ĐÀN ÔNG (Chủ thể: {_matched_male_kin.upper()} — 100%)"

        secondary_gender = f"Ứng với hào Dụng Thần ({dung_than}) và Cung {c_info['quai']}"

    elif _matched_female_kin:

        primary_gender = f"NỮ GIỚI / PHỤ NỮ (Chủ thể: {_matched_female_kin.upper()} — 100%)"

        secondary_gender = f"Ứng với hào Dụng Thần ({dung_than}) và Cung {c_info['quai']}"

    elif male_votes >= female_votes:

        primary_gender = f"NAM GIỚI / ĐÀN ÔNG (Trai — độ hội tụ {int(round(male_votes * 100 / total_votes))}%)"

        secondary_gender = "Có thể có 1 Nữ giới hỗ trợ/đi kèm ở vòng ngoài" if female_votes >= 2 else "Chủ yếu là Nam giới"

    else:

        primary_gender = f"NỮ GIỚI / PHỤ NỮ (Gái — độ hội tụ {int(round(female_votes * 100 / total_votes))}%)"

        secondary_gender = "Có thể có 1 Nam giới liên đới/đứng sau" if male_votes >= 2 else "Chủ yếu là Nữ giới"



    # Độ tuổi (Già hay Trẻ, bao nhiêu tuổi cụ thể)

    cur_year = datetime.date.today().year

    base_ages = list(c_info['base_ages'])

    _yr_match = _re_om.search(r"(?:sinh năm|tuổi|sn|năm)\s*(19\d\d|20[0-2]\d)", _q_low_om)

    if _yr_match:

        _by = int(_yr_match.group(1))

        _exact_age = max(1, cur_year - _by)

        age_tier = f"XÁC ĐỊNH THEO NĂM SINH ({_by} — {_exact_age} tuổi)"

        est_ages = [_exact_age]

    elif any(w in (_matched_male_kin or _matched_female_kin or "") for w in ["ông", "bà"]):

        age_tier = "CAO NIÊN / LÃO NIÊN (68 – 90+ tuổi)"

        est_ages = [68 + (base_ages[0] % 7), 75 + (base_ages[1] % 7), 82 + (base_ages[2] % 7)]

    elif any(w in (_matched_male_kin or _matched_female_kin or "") for w in ["bố", "mẹ", "cha", "má", "ba", "chú", "bác", "cô", "dì", "cậu", "mợ"]):

        age_tier = "TRUNG NIÊN CAO / LỚN TUỔI (50 – 78 tuổi)"

        est_ages = [52 + (base_ages[0] % 6), 60 + (base_ages[1] % 6), 68 + (base_ages[2] % 7)]

    elif any(w in (_matched_male_kin or _matched_female_kin or "") for w in ["con trai", "con gái", "con"]): 

        age_tier = "THANH THIẾU NIÊN / TRẺ TUỔI (5 – 30 tuổi)"

        est_ages = [8 + (base_ages[0] % 6), 16 + (base_ages[1] % 6), 24 + (base_ages[2] % 6)]

    elif ts_stage in ('Trường Sinh', 'Mộc Dục', 'Quan Đới', 'Lâm Quan', 'Thai', 'Dưỡng'):

        age_tier = "THANH NIÊN / TRUNG NIÊN TRẺ (DƯỚI 45 TUỔI — Khoảng 22 – 38 tuổi)"

        est_ages = [22 + (base_ages[0] % 5), 29 + (base_ages[1] % 5), 36 + (base_ages[2] % 5)]

    elif ts_stage in ('Đế Vượng',):

        age_tier = "TRUNG NIÊN ĐỘ CHÍN (DƯỚI 50 TUỔI — Khoảng 28 – 45 tuổi)"

        est_ages = [28 + (base_ages[0] % 5), 35 + (base_ages[1] % 5), 42 + (base_ages[2] % 4)]

    elif ts_stage in ('Suy', 'Bệnh', 'Tử', 'Mộ', 'Tuyệt'):

        age_tier = "NGƯỜI LỚN TUỔI / TRUNG NIÊN CAO (GIÀ DẶN)"

        est_ages = [min(78, a + 12) for a in base_ages[:3]]

    else:

        age_tier = c_info['age_group'].upper()

        est_ages = base_ages[:3]



    birth_years = [f"{cur_year - a} ({a} tuổi)" for a in est_ages]



    # Ngoại hình, Tính cách, Nghề nghiệp, Quen hay Lạ

    appearance_str = f"{can_g_info[1]}; thần thái mang nét {star_g_matched[1].lower()}."

    if _matched_male_kin or _matched_female_kin:

        _kin_lbl = (_matched_male_kin or _matched_female_kin).upper()

        familiar_str = f"NGƯỜI THÂN RUỘT THỊT TRONG GIA ĐÌNH (Chủ thể: {_kin_lbl})"

    else:

        familiar_str = (

            "NGƯỜI QUEN / NỘI BỘ (Người trong nhà, đồng nghiệp, bạn bè hoặc người từng tiếp xúc)"

            if is_noi_ban else

            "NGƯỜI LẠ / BÊN NGOÀI (Người ở xa, khách vãng lai, đối tác mới hoặc người ngoài khu vực)"

        )

    if 'Huyền Vũ' in than_name:

        motive_str = "Có tâm lý giấu giếm thông tin hoặc còn điều khuất tất chưa nói rõ."

    elif 'Thái Âm' in than_name:

        motive_str = "Tính cách sâu sắc, kín đáo, hay suy tư và giữ tâm sự riêng trong lòng."

    elif 'Bạch Hổ' in than_name or 'Kinh' in cua_name or 'Thương' in cua_name:

        motive_str = "Tính khí quyết liệt, gây sức ép, nóng nảy hoặc liên quan đến tranh chấp/cơ quan chức năng."

    elif 'Trực Phù' in than_name or 'Cửu Thiên' in than_name or 'Khai' in cua_name or 'Sinh' in cua_name:

        motive_str = "Đàng hoàng, có vị thế/uy tín, mang tính chất công việc chính thống hoặc quý nhân giúp đỡ."

    else:

        motive_str = "Hành xử linh hoạt theo tình huống, có sự tính toán thực tế."



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 5: HỒ SƠ ĐỒ VẬT, TÀI SẢN & CON SỐ ĐỊNH LƯỢNG

    # ═════════════════════════════════════════════════════════════════════════

    tier_vv = 'VƯỢNG' if weighted_pct >= 60 else ('SUY' if weighted_pct < 45 else 'TRUNG_BÌNH')

    try:

        vv_detail = get_van_vat_chi_tiet(hanh_dt, tier_vv)

    except Exception:

        vv_detail = {}

    vv_do_vat = ''

    if isinstance(vv_detail, dict):

        raw_dv = vv_detail.get('do_vat', '')

        if isinstance(raw_dv, list):

            vv_do_vat = ', '.join(str(x) for x in raw_dv[:6])

        elif isinstance(raw_dv, str):

            vv_do_vat = raw_dv[:120]

    combined_objects = f"{h_forensic['do_vat']}; {c_info['objects']}" + (f" ({vv_do_vat})" if vv_do_vat else "")



    if ts_stage in ('Đế Vượng', 'Lâm Quan', 'Quan Đới', 'Trường Sinh') and not any(x in cua_name for x in ('Tử', 'Thương', 'Kinh')):

        item_condition = "MỚI / NGUYÊN VẸN (Đang hoạt động tốt, giá trị cao, chưa bị hư hại)"

        item_size = "Kích thước LỚN hoặc đầy đặn, dễ nhận biết"

    elif any(x in cua_name for x in ('Thương', 'Kinh', 'Đỗ')) or ts_stage in ('Suy', 'Bệnh'):

        item_condition = "ĐÃ QUA SỬ DỤNG / CŨ HOẶC TRẦY XƯỚC NHẸ (Có vết xước, hết pin hoặc bị kẹt/che khuất một phần)"

        item_size = "Kích thước VỪA PHẢI"

    else:

        item_condition = "CŨ HOẶC HƯ HỎNG / BỊ VÙI LẤP (Đang bị che kín trong góc tối/hộp kín, cần tìm kỹ mới thấy)"

        item_size = "Kích thước NHỎ GỌN hoặc bị gấp/nén lại"



    # Tính Số lượng / Giá trị (Hà Đồ + Lạc Thư + Tiên Thiên)

    ha_do_map = {'Thủy': (1, 6), 'Hỏa': (2, 7), 'Mộc': (3, 8), 'Kim': (4, 9), 'Thổ': (5, 10)}

    tien_thien_map = {'Càn': 1, 'Đoài': 2, 'Ly': 3, 'Chấn': 4, 'Tốn': 5, 'Khảm': 6, 'Cấn': 7, 'Khôn': 8}

    hd_1, hd_2 = ha_do_map.get(hanh_dt, (5, 10))

    lt_num = target_cung

    tt_num = tien_thien_map.get(c_info['quai'].split()[0], 5)

    nums_sorted = sorted(list({hd_1, hd_2, lt_num, tt_num}))

    quantity_str = (

        f"Con số định lượng chuẩn: <b>{', '.join(str(n) for n in nums_sorted)}</b> "

        f"(Số lượng: <b>{hd_1}</b> hoặc <b>{lt_num}</b> đơn vị; "

        f"Bội số giá trị/tài lộc: <b>{hd_1}0, {lt_num}0, {hd_2}00</b>)"

    )



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 5B (V103.1): GIẢI MÃ TỬ TỨC / CON CÁI & ĐỘ TUỔI CON GÁI - CON TRAI SÁT TỪ LIÊN KẾT ĐA HỆ THỐNG

    # ═════════════════════════════════════════════════════════════════════════

    _has_age_kw_om = any(w in _q_low_om for w in ['tuổi', 'mấy tuổi', 'bao nhiêu tuổi', 'năm sinh', 'sinh năm'])

    _is_children_age_q = _has_age_kw_om and any(w in _q_low_om for w in [

        'con gái', 'con trai', 'con của tôi', 'con tôi', 'mấy đứa con', 'hai đứa con', '2 đứa con', 'các con', 'con cái', 'đứa con', 'chúng nó'

    ])

    _is_children_q = (not _has_age_kw_om) and (any(w in _q_low_om for w in [

        'người con', 'mấy con', 'bao nhiêu con', 'mấy đứa con', 'mấy trai mấy gái',

        'con trai hay con gái', 'sinh con trai hay', 'sinh trai hay gái', 'tử tức',

        'con cái', 'có mấy người con', 'bao nhiêu người con'

    ]) or (('con' in _q_low_om and not any(bad in _q_low_om for bad in ['con số', 'con đường', 'con xe', 'con dao', 'con cá', 'con gà', 'con chó', 'con mèo', 'bà con', 'con thứ mấy', 'con trưởng', 'con út', 'con đầu'])) and any(w in _q_low_om for w in ['bao nhiêu', 'mấy trai', 'mấy gái', 'có mấy'])))



    # Phân tích Quẻ Chủ, Quẻ Hỗ, Quẻ Biến, Hào Tử Tôn và Cung Kỳ Môn để tính số con & trai/gái:

    _YANG_TRIGRAMS = {'Càn': 'Cha/Nam (Dương Kim)', 'Chấn': 'Trưởng Nam (Con trai lớn)', 'Khảm': 'Trung Nam (Con trai thứ)', 'Cấn': 'Thiếu Nam (Con trai út)'}

    _YIN_TRIGRAMS = {'Khôn': 'Mẹ/Nữ (Âm Thổ)', 'Tốn': 'Trưởng Nữ (Con gái lớn)', 'Ly': 'Trung Nữ (Con gái thứ)', 'Đoài': 'Thiếu Nữ (Con gái út)'}

    _HEX_TRIGRAM_SPLIT = {

        'Trạch Địa Tụy': ('Đoài', 'Khôn'), 'Thiên Địa Bĩ': ('Càn', 'Khôn'), 'Địa Thiên Thái': ('Khôn', 'Càn'),

        'Phong Sơn Tiệm': ('Tốn', 'Cấn'), 'Tốn Cấn': ('Tốn', 'Cấn'), 'Sơn Phong Cổ': ('Cấn', 'Tốn'),

        'Thuần Càn': ('Càn', 'Càn'), 'Thuần Khôn': ('Khôn', 'Khôn'), 'Thủy Lôi Truân': ('Khảm', 'Chấn'),

        'Sơn Thủy Mông': ('Cấn', 'Khảm'), 'Thủy Thiên Nhu': ('Khảm', 'Càn'), 'Thiên Thủy Tụng': ('Càn', 'Khảm'),

        'Địa Thủy Sư': ('Khôn', 'Khảm'), 'Thủy Địa Tỷ': ('Khảm', 'Khôn'), 'Phong Thiên Tiểu Súc': ('Tốn', 'Càn'),

        'Thiên Trạch Lý': ('Càn', 'Đoài'), 'Thiên Hỏa Đồng Nhân': ('Càn', 'Ly'), 'Hỏa Thiên Đại Hữu': ('Ly', 'Càn'),

        'Địa Sơn Khiêm': ('Khôn', 'Cấn'), 'Lôi Địa Dự': ('Chấn', 'Khôn'), 'Trạch Lôi Tùy': ('Đoài', 'Chấn'),

        'Địa Trạch Lâm': ('Khôn', 'Đoài'), 'Phong Địa Quan': ('Tốn', 'Khôn'), 'Hỏa Lôi Phệ Hạp': ('Ly', 'Chấn'),

        'Sơn Hỏa Bí': ('Cấn', 'Ly'), 'Sơn Địa Bác': ('Cấn', 'Khôn'), 'Địa Lôi Phục': ('Khôn', 'Chấn'),

        'Thiên Lôi Vô Vọng': ('Càn', 'Chấn'), 'Sơn Thiên Đại Súc': ('Cấn', 'Càn'), 'Sơn Lôi Di': ('Cấn', 'Chấn'),

        'Trạch Phong Đại Quá': ('Đoài', 'Tốn'), 'Thuần Khảm': ('Khảm', 'Khảm'), 'Thuần Ly': ('Ly', 'Ly'),

        'Trạch Sơn Hàm': ('Đoài', 'Cấn'), 'Lôi Phong Hằng': ('Chấn', 'Tốn'), 'Thiên Sơn Độn': ('Càn', 'Cấn'),

        'Lôi Thiên Đại Tráng': ('Chấn', 'Càn'), 'Hỏa Địa Tấn': ('Ly', 'Khôn'), 'Địa Hỏa Minh Di': ('Khôn', 'Ly'),

        'Phong Hỏa Gia Nhân': ('Tốn', 'Ly'), 'Hỏa Trạch Khuê': ('Ly', 'Đoài'), 'Thủy Sơn Kiển': ('Khảm', 'Cấn'),

        'Lôi Thủy Giải': ('Chấn', 'Khảm'), 'Sơn Trạch Tổn': ('Cấn', 'Đoài'), 'Phong Lôi Ích': ('Tốn', 'Chấn'),

        'Trạch Thiên Quải': ('Đoài', 'Càn'), 'Thiên Phong Cấu': ('Càn', 'Tốn'), 'Địa Phong Thăng': ('Khôn', 'Tốn'),

        'Trạch Thủy Khốn': ('Đoài', 'Khảm'), 'Thủy Phong Tỉnh': ('Khảm', 'Tốn'), 'Trạch Hỏa Cách': ('Đoài', 'Ly'),

        'Hỏa Phong Đỉnh': ('Ly', 'Tốn'), 'Thuần Chấn': ('Chấn', 'Chấn'), 'Thuần Cấn': ('Cấn', 'Cấn'),

        'Lôi Trạch Quy Muội': ('Chấn', 'Đoài'), 'Lôi Hỏa Phong': ('Chấn', 'Ly'), 'Hỏa Sơn Lữ': ('Ly', 'Cấn'),

        'Thuần Tốn': ('Tốn', 'Tốn'), 'Thuần Đoài': ('Đoài', 'Đoài'), 'Phong Thủy Hoán': ('Tốn', 'Khảm'),

        'Thủy Trạch Tiết': ('Khảm', 'Đoài'), 'Phong Trạch Trung Phu': ('Tốn', 'Đoài'), 'Lôi Sơn Tiểu Quá': ('Chấn', 'Cấn'),

        'Thủy Hỏa Ký Tế': ('Khảm', 'Ly'), 'Hỏa Thủy Vị Tế': ('Ly', 'Khảm'),

    }



    _boy_pts = 0

    _girl_pts = 0

    _child_evidences = []



    # 1. Phân tích Quẻ Chủ, Quẻ Hỗ, Quẻ Biến

    for _q_lbl, _q_nm in [('Quẻ Chủ', ten_que_ban), ('Quẻ Hỗ', ten_que_ho), ('Quẻ Biến', ten_que_bien)]:

        if not _q_nm:

            continue

        _pair = _HEX_TRIGRAM_SPLIT.get(_q_nm)

        if not _pair:

            for _tk in list(_YANG_TRIGRAMS.keys()) + list(_YIN_TRIGRAMS.keys()):

                if _tk in _q_nm:

                    _pair = (_tk, _tk)

                    break

        if _pair:

            for _tg in _pair:

                if _tg in _YANG_TRIGRAMS:

                    _boy_pts += 1

                    _child_evidences.append(f"{_q_lbl} <b>{_q_nm}</b> có quái <b>{_tg}</b> ({_YANG_TRIGRAMS[_tg]})")

                elif _tg in _YIN_TRIGRAMS:

                    _girl_pts += 1

                    _child_evidences.append(f"{_q_lbl} <b>{_q_nm}</b> có quái <b>{_tg}</b> ({_YIN_TRIGRAMS[_tg]})")



    # 2. Phân tích Hào Tử Tôn trong Lục Hào

    _tu_ton_lines = []

    for _idx_h, _h_it in enumerate(lh_haos, 1):

        if isinstance(_h_it, dict) and _h_it.get('luc_than') == 'Tử Tôn':

            _h_ad = str(_h_it.get('am_duong', _h_it.get('type', '')))

            _h_cc = _h_it.get('can_chi') or _h_it.get('chi', '')

            _h_nh = _h_it.get('ngu_hanh', hanh_dt)

            if any(x in _h_ad for x in ['Dương', '1', '7', '9']) or (_idx_h % 2 == 1):

                _boy_pts += 2

                _tu_ton_lines.append(f"Hào Tử Tôn tại Hào {_idx_h} ({_h_cc} hành {_h_nh} — Dương/Con Trai)")

            else:

                _girl_pts += 2

                _tu_ton_lines.append(f"Hào Tử Tôn tại Hào {_idx_h} ({_h_cc} hành {_h_nh} — Âm/Con Gái)")

    if _tu_ton_lines:

        _child_evidences.extend(_tu_ton_lines)

    else:

        _child_evidences.append(f"Dụng Thần <b>Tử Tôn</b> mang hành <b>{hanh_dt}</b> (vòng Trường Sinh: <b>{ts_stage or 'Thai/Dưỡng'}</b>)")



    # 3. Phân tích Cung Kỳ Môn (Cung + Sao + Cửa)

    _quai_short = c_info['quai'].split()[0]

    if _quai_short in _YANG_TRIGRAMS:

        _boy_pts += 1

        _child_evidences.append(f"Kỳ Môn Cung {target_cung} <b>{_quai_short}</b> ({_YANG_TRIGRAMS[_quai_short]})")

    elif _quai_short in _YIN_TRIGRAMS:

        _girl_pts += 1

        _child_evidences.append(f"Kỳ Môn Cung {target_cung} <b>{_quai_short}</b> ({_YIN_TRIGRAMS[_quai_short]})")



    if 'Nam' in star_g_matched[0]:

        _boy_pts += 1

        _child_evidences.append(f"Sao <b>{sao_name}</b> (Dương tinh — ứng Con Trai)")

    else:

        _girl_pts += 1

        _child_evidences.append(f"Sao <b>{sao_name}</b> (Âm tinh — ứng Con Gái)")



    if any(m in cua_name for m in ['Khai', 'Hưu', 'Sinh', 'Thương']):

        _boy_pts += 1

        _child_evidences.append(f"Cửa <b>{cua_name}</b> (Dương môn — ứng Con Trai)")

    else:

        _girl_pts += 1

        _child_evidences.append(f"Cửa <b>{cua_name}</b> (Âm môn — ứng Con Gái)")



    # Chốt số lượng con và cơ cấu Trai / Gái sát thực tế:

    # Số Tiên Thiên của quái cung + số lượng hào Tử Tôn quyết định số con chủ đạo (thường từ 2 đến 3 người con)

    if tt_num in (1, 2) or hd_1 in (1, 2):

        _main_child_cnt = 2

        _range_child_str = "2 người con (hoặc 2 – 3 con nếu tính đủ lộc Tử Tức)"

    else:

        _main_child_cnt = 2 if (_boy_pts > 0 and _girl_pts > 0) else 3

        _range_child_str = f"{_main_child_cnt} người con (dao động 2 – 3 con theo số quẻ)"



    if _boy_pts > 0 and _girl_pts > 0:

        if _boy_pts > _girl_pts + 2:

            _bg_str = "1 – 2 Con Trai và 1 Con Gái (Dương khí nhỉnh hơn — dễ có 2 Trai 1 Gái hoặc 1 Trai 1 Gái)"

        elif _girl_pts > _boy_pts + 2:

            _bg_str = "1 Con Trai và 1 – 2 Con Gái (Âm khí nhỉnh hơn — dễ có 1 Trai 1 Gái hoặc 1 Trai 2 Gái)"

        else:

            _bg_str = "1 Con Trai và 1 Con Gái — Đủ cả nếp lẫn tẻ (Nếu sinh 3 con thì ứng 2 Trai 1 Gái hoặc 1 Trai 2 Gái)"

    elif _boy_pts > 0:

        _bg_str = "Chủ yếu là Con Trai (1 – 2 Con Trai)"

    else:

        _bg_str = "Chủ yếu là Con Gái (1 – 2 Con Gái)"



    auth_warnings = auth_warnings if isinstance(auth_warnings, list) else []

    _uniq_ev = []

    for _ev in _child_evidences:

        if _ev not in _uniq_ev:

            _uniq_ev.append(_ev)

    _hex_child_reasons = "; kết hợp ".join(_uniq_ev[:5]) + "."



    # V103.1: Kiểm tra sâu Hào Tử Tôn có thực sự bị Chân Không hay đang Hữu Khí / được Hào Động sinh trợ!

    _CHI_NH_OM = {'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc', 'Thìn': 'Thổ', 'Tị': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ', 'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'}

    _SINH_NH_OM = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}

    _HOP_CHI_OM = {'Tý': 'Sửu', 'Sửu': 'Tý', 'Dần': 'Hợi', 'Hợi': 'Dần', 'Mão': 'Tuất', 'Tuất': 'Mão', 'Thìn': 'Dậu', 'Dậu': 'Thìn', 'Tị': 'Thân', 'Thân': 'Tị', 'Ngọ': 'Mùi', 'Mùi': 'Ngọ'}

    _TAM_HOP_OM = [{'Thân', 'Tý', 'Thìn'}, {'Dần', 'Ngọ', 'Tuất'}, {'Hợi', 'Mão', 'Mùi'}, {'Tị', 'Dậu', 'Sửu'}]

    _can_n_chk = chart_data.get('can_ngay', 'Giáp')

    _chi_n_chk = chart_data.get('chi_ngay', 'Tý')

    _CAN_10_OM = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']

    _CHI_12_OM = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

    try:

        _st_om = (_CHI_12_OM.index(_chi_n_chk) - _CAN_10_OM.index(_can_n_chk)) % 12

        _kv_chk_om = [_CHI_12_OM[(_st_om - 2) % 12], _CHI_12_OM[(_st_om - 1) % 12]]

    except Exception:

        _kv_chk_om = []

    _dong_lst_chk = luc_hao_data.get('dong_hao') or lh_ban.get('dong_hao') or []

    _tt_real_support = []

    _tt_chi_primary = ''

    _tt_nh_primary = hanh_dt

    _tt_idx_primary = 1

    _dong_chi_primary = ''

    _dong_nh_primary = ''

    _dong_idx_primary = 0

    _bien_chi_primary = ''

    _lh_bien_haos = (luc_hao_data.get('bien', {}) or {}).get('haos') or []



    for _ix_c, _h_c in enumerate(lh_haos, 1):

        if not isinstance(_h_c, dict):

            continue

        _lt_c = str(_h_c.get('luc_than') or '')

        _raw_c = str(_h_c.get('chi') or _h_c.get('can_chi') or '')

        _ch_c = _raw_c.split()[-1] if _raw_c else ''

        _nh_c = _h_c.get('ngu_hanh') or _h_c.get('hanh') or _CHI_NH_OM.get(_ch_c, '')

        _id_c = bool(_h_c.get('is_dong') or _h_c.get('dong') or _h_c.get('is_moving') or (_ix_c in _dong_lst_chk))

        if _id_c and not _dong_chi_primary:

            _dong_chi_primary = _ch_c

            _dong_nh_primary = _nh_c

            _dong_idx_primary = _ix_c

            if _ix_c <= len(_lh_bien_haos) and isinstance(_lh_bien_haos[_ix_c - 1], dict):

                _b_raw = str(_lh_bien_haos[_ix_c - 1].get('chi') or _lh_bien_haos[_ix_c - 1].get('can_chi') or '')

                _bien_chi_primary = _b_raw.split()[-1] if _b_raw else ''

        if _lt_c == 'Tử Tôn' and not _tt_chi_primary:

            _tt_chi_primary = _ch_c

            _tt_nh_primary = _nh_c

            _tt_idx_primary = _ix_c

            if _ch_c not in _kv_chk_om:

                _tt_real_support.append(f"Hào Tử Tôn tại Hào {_ix_c} ({_ch_c}-{_nh_c}) hoàn toàn KHÔNG phạm Tuần Không ({', '.join(_kv_chk_om)})")

            elif _id_c:

                _tt_real_support.append(f"Hào Tử Tôn tại Hào {_ix_c} ({_ch_c}) phát động (Động bất vi Không)")



    if _tt_chi_primary and _dong_chi_primary and _dong_idx_primary != _tt_idx_primary:

        if _SINH_NH_OM.get(_dong_nh_primary) == _tt_nh_primary or _dong_nh_primary == _tt_nh_primary or _HOP_CHI_OM.get(_dong_chi_primary) == _tt_chi_primary or any({_dong_chi_primary, _tt_chi_primary}.issubset(_s) for _s in _TAM_HOP_OM):

            _tt_real_support.append(f"Hào {_dong_idx_primary} ({_dong_chi_primary}-{_dong_nh_primary}) phát động sinh trợ & hợp cục trực tiếp với Hào {_tt_idx_primary} Tử Tôn ({_tt_chi_primary}-{_tt_nh_primary})")



    if _tt_real_support and (_is_children_q or _is_children_age_q or dung_than == 'Tử Tôn'):

        is_fake = False



    # V103.1: Giải mã chuyên sâu Độ Tuổi & Năm Sinh của CON GÁI và CON TRAI từ Liên kết Lục Hào + Mai Hoa + Kỳ Môn + Thiết Bản

    _TT_MAP_AGE = {'Càn': 1, 'Đoài': 2, 'Ly': 3, 'Chấn': 4, 'Tốn': 5, 'Khảm': 6, 'Cấn': 7, 'Khôn': 8}

    _HT_MAP_AGE = {'Khảm': 1, 'Khôn': 2, 'Chấn': 3, 'Tốn': 4, 'Càn': 6, 'Đoài': 7, 'Cấn': 8, 'Ly': 9}

    _CHI_ORD_AGE = {'Tý': 1, 'Sửu': 2, 'Dần': 3, 'Mão': 4, 'Thìn': 5, 'Tị': 6, 'Ngọ': 7, 'Mùi': 8, 'Thân': 9, 'Dậu': 10, 'Tuất': 11, 'Hợi': 12}



    def _fmt_yr_cc(yr_val: int) -> str:

        _c_y = _CAN_10_OM[(yr_val - 4) % 10]

        _ch_y = _CHI_12_OM[(yr_val - 4) % 12]

        return f"{yr_val} ({_c_y} {_ch_y} — {max(1, cur_year - yr_val)} tuổi)"



    _yin_quai_found = []

    _yang_quai_found = []

    for _ql_a, _qn_a in [('Quẻ Chủ', ten_que_ban), ('Quẻ Biến', ten_que_bien), ('Quẻ Hỗ', ten_que_ho)]:

        _pr_a = _HEX_TRIGRAM_SPLIT.get(_qn_a or '')

        if _pr_a:

            for _tg_a in _pr_a:

                if _tg_a in _YIN_TRIGRAMS and _tg_a not in [x[0] for x in _yin_quai_found]:

                    _yin_quai_found.append((_tg_a, _ql_a, _qn_a))

                elif _tg_a in _YANG_TRIGRAMS and _tg_a not in [x[0] for x in _yang_quai_found]:

                    _yang_quai_found.append((_tg_a, _ql_a, _qn_a))



    _g_quai_main = _yin_quai_found[0][0] if _yin_quai_found else 'Đoài'

    _g_quai_sec = _yin_quai_found[1][0] if len(_yin_quai_found) > 1 else 'Ly'

    _b_quai_main = _yang_quai_found[0][0] if _yang_quai_found else 'Chấn'

    _b_quai_sec = _yang_quai_found[1][0] if len(_yang_quai_found) > 1 else 'Càn'



    _g_n1 = min(_TT_MAP_AGE.get(_g_quai_main, 2), _HT_MAP_AGE.get(_g_quai_main, 7))

    _g_n2 = _CHI_ORD_AGE.get(_tt_chi_primary, 4) if _tt_chi_primary else _TT_MAP_AGE.get(_g_quai_sec, 3)

    if _g_n2 == _g_n1:

        _g_n2 = _g_n1 + 2

    _g_low_a, _g_high_a = min(_g_n1, _g_n2), max(_g_n1, _g_n2)

    _g_mid1 = max(_HT_MAP_AGE.get(_g_quai_main, 7), 7)

    _g_mid2 = max(_HT_MAP_AGE.get(_g_quai_sec, 9), _g_mid1 + 2)

    _g_teen1, _g_teen2 = 10 + _g_low_a, 10 + max(_g_high_a, 5)



    _b_n1 = min(_TT_MAP_AGE.get(_b_quai_main, 4), _HT_MAP_AGE.get(_b_quai_main, 3))

    _b_n2 = _CHI_ORD_AGE.get(_bien_chi_primary or _dong_chi_primary, 5)

    if _b_n2 > 9:

        _b_n2 = (_b_n2 % 6) + 3

    _b_low_a, _b_high_a = min(_b_n1, _b_n2), max(_b_n1, _b_n2, _b_n1 + 2)

    _b_mid1 = max(hd_2, 8)

    _b_mid2 = _b_mid1 + 2

    _b_teen1, _b_teen2 = 10 + max(1, _b_low_a - 2), 10 + _b_high_a



    # Tìm các năm sinh khớp trực tiếp Địa Chi Hào Tử Tôn & Hào Động/Biến

    _girl_yrs_small = [_fmt_yr_cc(cur_year - a) for a in sorted(list({_g_low_a, (_g_low_a + _g_high_a) // 2, _g_high_a}))[:3]]

    _girl_yrs_mid = [_fmt_yr_cc(cur_year - a) for a in [_g_mid1, _g_mid2]]

    _girl_yrs_teen = [_fmt_yr_cc(cur_year - a) for a in [_g_teen1, _g_teen2]]



    _boy_yrs_small = [_fmt_yr_cc(cur_year - a) for a in sorted(list({_b_low_a, (_b_low_a + _b_high_a) // 2, _b_high_a}))[:3]]

    _boy_yrs_mid = [_fmt_yr_cc(cur_year - a) for a in [_b_mid1, _b_mid2]]

    _boy_yrs_teen = [_fmt_yr_cc(cur_year - a) for a in [_b_teen1, _b_teen2]]



    _testing_note_str = ""

    if auth_warnings and not is_fake:

        _testing_note_str = (

            " (🔍 Nghiệm chứng Liên kết Đa tầng: Hào Tử Tôn hữu khí/được Hào Động sinh trợ khẳng định bạn ĐANG CÓ CON THẬT NGOÀI ĐỜI — "

            "còn Nhật Can chạm Tuần Không là dấu hiệu bạn đặt câu hỏi để THỬ NGHIỆM ĐỘ NHẠY CỦA QUẺ!)"

        )



    children_age_headline = (

        f"👧👦 KẾT LUẬN TỪ LIÊN KẾT ĐA HỆ THỐNG ({ten_que_ban.upper()} ➔ {(ten_que_bien or 'BIẾN QUÁI').upper()}): "

        f"BẠN ĐANG CÓ {_main_child_cnt} NGƯỜI CON THẬT NGOÀI ĐỜI (CÓ CON GÁI & CON TRAI) — "

        f"ĐỘ TUỔI ỨNG NGHIỆM: [CON GÁI]: KHOẢNG {_g_low_a}–{_g_high_a} TUỔI HOẶC {_g_mid1}–{_g_mid2} TUỔI (NẾU LỚN: {_g_teen1}–{_g_teen2} TUỔI) | "

        f"[CON TRAI]: KHOẢNG {_b_low_a}–{_b_high_a} TUỔI HOẶC {_b_mid1}–{_b_mid2} TUỔI (NẾU LỚN: {_b_teen1}–{_b_teen2} TUỔI)!"

    )

    children_age_why = (

        f"<b>1. Liên kết Thực/Hư & Nhân Đinh (Lục Hào · Mai Hoa · Kỳ Môn):</b> {'; '.join(_tt_real_support) if _tt_real_support else _hex_child_reasons}. "

        f"Quẻ Chủ <b>{ten_que_ban}</b> biến <b>{ten_que_bien or 'Bình hòa'}</b> hội đủ tượng Âm Nữ (<b>{_g_quai_main}, {_g_quai_sec}</b>) và Dương Nam (<b>{_b_quai_main}</b>) ➔ Khẳng định thực tế bạn <b>đang có {_main_child_cnt} người con (có Con Gái và Con Trai)</b>, bác bỏ hoàn toàn luận giải 'không có con' đơn thuần.{_testing_note_str} "

        f"<b>2. Luận tuổi CON GÁI:</b> Quái Âm <b>{_g_quai_main}</b> (Tiên thiên {_TT_MAP_AGE.get(_g_quai_main, 2)}, Hậu thiên {_HT_MAP_AGE.get(_g_quai_main, 7)}) + <b>{_g_quai_sec}</b> (Tiên thiên {_TT_MAP_AGE.get(_g_quai_sec, 3)}, Hậu thiên {_HT_MAP_AGE.get(_g_quai_sec, 9)}) + Hào {_tt_idx_primary} Tử Tôn (<b>{_tt_chi_primary or 'Mão'}-{_tt_nh_primary}</b>, số {_g_n2}) ➔ Ứng khung nhỏ <b>{_g_low_a}–{_g_high_a} tuổi</b> ({', '.join(_girl_yrs_small[:2])}) hoặc <b>{_g_mid1}–{_g_mid2} tuổi</b> ({', '.join(_girl_yrs_mid)}); khung thiếu niên <b>{_g_teen1}–{_g_teen2} tuổi</b> ({', '.join(_girl_yrs_teen)}). "

        f"<b>3. Luận tuổi CON TRAI:</b> Quái Dương <b>{_b_quai_main}</b> (Hậu thiên {_HT_MAP_AGE.get(_b_quai_main, 3)}, Tiên thiên {_TT_MAP_AGE.get(_b_quai_main, 4)}) + Hào Động {_dong_idx_primary or 3} (<b>{_dong_chi_primary or 'Hợi'} ➔ {_bien_chi_primary or 'Thìn'}</b>) + Kỳ Môn Cung {target_cung} ➔ Ứng khung nhỏ <b>{_b_low_a}–{_b_high_a} tuổi</b> ({', '.join(_boy_yrs_small[:2])}) hoặc <b>{_b_mid1}–{_b_mid2} tuổi</b> ({', '.join(_boy_yrs_mid)}); khung thiếu niên <b>{_b_teen1}–{_b_teen2} tuổi</b> ({', '.join(_boy_yrs_teen)})."

    )



    if is_fake:

        children_summary = (

            f"NGHIỆM CHỨNG TỪ QUẺ (PHÁT HIỆN CHÂN KHÔNG / VÔ KHÍ): HIỆN TẠI CHƯA CÓ CON (0 NGƯỜI CON) "

            f"— HOẶC ĐANG HỎI THỬ MỘT VIỆC CHƯA TỒN TẠI! "

            f"(Nếu xét tiềm năng tương lai khi xuất Không: Khoảng {_range_child_str} — gồm {_bg_str})"

        )

        _clean_aw = [w.replace('🔹 ', '') for w in auth_warnings[:4]]

        children_reasons = (

            "<b>Quẻ bắt bài câu hỏi chưa có thật ở hiện tại:</b> "

            + " | ".join(_clean_aw)

            + f". <i>(Luận phụ cho tương lai khi xuất Không: {_hex_child_reasons})</i>"

        )

    else:

        children_summary = (

            f"QUẺ BÁO TỬ TỨC (ĐÃ XÁC THỰC HỮU KHÍ): BẠN ĐANG CÓ KHOẢNG {_range_child_str.upper()} — GỒM {_bg_str.upper()}!"

            + (" (Kèm dấu hiệu Nhật Can Tuần Không: Bạn đã có con thực tế và đang hỏi thử độ nhạy của quẻ)" if auth_warnings else "")

        )

        children_reasons = (

            (f"<b>Liên kết Lục Hào & Mai Hoa xác nhận thực tế có con:</b> {'; '.join(_tt_real_support)}. " if _tt_real_support else "")

            + _hex_child_reasons

            + (_testing_note_str if _testing_note_str else "")

        )

    children_traits = (

        f"Hào Tử Tôn hành <b>{hanh_dt}</b> ({ts_stage or 'Vượng'}) hội Sao <b>{sao_name}</b> và Cửa <b>{cua_name}</b> tại hướng <b>{c_info['huong']}</b>: "

        f"báo hiệu các con có tư chất thông minh, lanh lợi, tính tự lập cao ({star_g_matched[1].lower()}), lớn lên có chính kiến và biết lo cho gia đình."

    )

    children_advice = (

        f"Để bồi đắp phúc khí cho con cái (Cung Tử Tức tại <b>{c_info['huong']}</b>), cha mẹ nên khích lệ sự tự lập của con, "

        f"bố trí góc học tập/phòng ngủ của con ưu tiên hướng <b>{c_info['huong']}</b> và dùng các gam màu <b>{h_forensic['mau_sac']}</b>."

    )

    children_age_when = (

        f"<b>Địa Chi năm sinh sáng nhất hiện trực tiếp trên hào quẻ:</b> Trục Hào Tử Tôn <b>{_tt_chi_primary or 'Mão'}</b> (Tam hợp Hợi – Mão – Mùi) "

        f"và trục Hào Động/Biến <b>{_dong_chi_primary or 'Hợi'} – {_bien_chi_primary or 'Thìn'} – Dần – Tuất</b>. {children_traits}"

    )

    children_age_advice = children_advice







    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 5C (V101.2): BỘ GIẢI MÃ DỨT KHOÁT CÂU HỎI LỰA CHỌN "A HAY B" & VỊ TRÍ/TRẠNG THÁI THỰC TẾ

    # (Chấm dứt 100% lỗi trả lời "CẦN CÂN NHẮC — BÌNH / giằng co" hoặc tự bịa không bám sát quẻ)

    # ═════════════════════════════════════════════════════════════════════════

    _is_quit_work_q = any(w in _q_low_om for w in ['nghỉ hay', 'nên nghỉ', 'nghỉ việc', 'bỏ việc', 'xin nghỉ', 'làm tiếp hay', 'đi hay ở', 'ở lại hay'])

    _is_who_age_q = any(w in _q_low_om for w in ['nam hay nữ', 'nữ hay nam', 'trai hay gái', 'gái hay trai', 'giới tính', 'bao nhiêu tuổi', 'mấy tuổi'])

    _is_where_home_work_q = (

        any(w in _q_low_om for w in ['ở nhà hay', 'hay ở nhà', 'ở công ty', 'ở cơ quan', 'ở văn phòng', 'ở quán', 'ngoài đường', 'trong nhà hay', 'ngoài sân'])

        and ('nhà' in _q_low_om or 'công ty' in _q_low_om or 'cơ quan' in _q_low_om or 'văn phòng' in _q_low_om or 'ngoài' in _q_low_om or 'phòng' in _q_low_om)

    )

    _is_posture_state_q = any(w in _q_low_om for w in ['đứng hay ngồi', 'ngồi hay đứng', 'nằm hay ngồi', 'ngồi hay nằm', 'đang đứng hay', 'đang ngồi hay', 'đang nằm hay', 'ngủ hay thức', 'thức hay ngủ'])

    _is_true_false_q = any(w in _q_low_om for w in ['thật hay giả', 'giả hay thật', 'nói thật hay', 'nói dối hay', 'có thật không', 'thật không'])

    _is_done_yet_q = any(w in _q_low_om for w in ['rồi hay chưa', 'chưa hay rồi', 'hay chưa', 'ăn cơm chưa', 'ăn chưa', 'về chưa', 'đi chưa', 'xong chưa', 'đã ăn', 'đã về', 'đã đi'])



    is_binary_factual_q = False

    binary_verdict_headline = ""

    binary_why_reasons = ""

    binary_when_note = ""

    binary_action_advice = ""



    _can_n_om = chart_data.get('can_ngay', 'Giáp')

    _chi_n_om = chart_data.get('chi_ngay', 'Tý')

    _can_g_om = chart_data.get('can_gio', 'Giáp')

    _CAN_LIST_OM = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']

    _CHI_LIST_OM = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

    try:

        _ci_om = _CAN_LIST_OM.index(_can_n_om)

        _chi_i_om = _CHI_LIST_OM.index(_chi_n_om)

        _start_chi_om = (_chi_i_om - _ci_om) % 12

        _kv_om = [_CHI_LIST_OM[(_start_chi_om - 2) % 12], _CHI_LIST_OM[(_start_chi_om - 1) % 12]]

    except Exception:

        _kv_om = []



    _dong_list_om = (

        luc_hao_data.get('dong_hao')

        or lh_ban.get('dong_hao')

        or (luc_hao_data.get('ban_main', {}) or {}).get('dong_hao')

        or []

    )



    if _is_where_home_work_q:

        is_binary_factual_q = True

        _home_pts = 0

        _work_pts = 0

        _loc_evidences = []

        for _idx_h, _h_it in enumerate(lh_haos, 1):

            if not isinstance(_h_it, dict):

                continue

            _lt_h = str(_h_it.get('luc_than') or '')

            _raw_cc_h = str(_h_it.get('chi') or _h_it.get('can_chi') or '')

            _chi_h = _raw_cc_h.split()[-1] if _raw_cc_h else ''

            _tu_h = str(_h_it.get('the_ung') or _h_it.get('tu') or '')

            _is_d_h = bool(_h_it.get('is_dong') or _h_it.get('dong') or _h_it.get('is_moving') or (_idx_h in _dong_list_om))



            if 'Quan Quỷ' in _lt_h:

                if _chi_h in _kv_om:

                    _home_pts += 4

                    _loc_evidences.append(

                        f"<b>Lục Hào (Hào Công ty bị Tuần Không):</b> Hào <b>Quan Quỷ</b> (đại diện cho Công ty/Cơ quan) tại Hào {_idx_h} (<b>{_chi_h}</b>) rơi vào <b>Tuần Không ({', '.join(_kv_om)})</b> — chứng tỏ vị trí ở công ty đang trống không, bạn <b>KHÔNG có mặt ở công ty</b>"

                    )

                else:

                    if _is_d_h or 'Thế' in _tu_h or _idx_h in (4, 5, 6):

                        _work_pts += 3

                        _loc_evidences.append(f"<b>Lục Hào (Hào Công sở đắc vị):</b> Hào <b>Quan Quỷ</b> (Công ty/Cơ quan) tại Hào {_idx_h} ({_chi_h}) không phạm Tuần Không và đang hoạt động hữu khí trên trục Ngoại Quái/Thế")

            if 'Tử Tôn' in _lt_h and _is_d_h:

                _home_pts += 4

                _loc_evidences.append(

                    f"<b>Lục Hào (Hào Nghỉ ngơi ở nhà phát động):</b> Hào {_idx_h} <b>Tử Tôn ({_chi_h})</b> — đại diện cho sự nghỉ ngơi, thoải mái tại gia — phát động mạnh khắc trực tiếp hào <b>Quan Quỷ (Công ty)</b>"

                )

            if 'Phụ Mẫu' in _lt_h and ('Thế' in _tu_h or _idx_h == 2):

                _home_pts += 2

                _loc_evidences.append(f"<b>Lục Hào (Hào Gia trạch):</b> Hào <b>Phụ Mẫu ({_chi_h} — Nhà cửa/Mái ấm)</b> tọa tại {'Hào Thế' if 'Thế' in _tu_h else 'Hào 2 Trạch vị'}")

            if 'Thế' in _tu_h:

                if _idx_h in (1, 2, 3):

                    _home_pts += 2

                    _loc_evidences.append(f"<b>Vị trí Hào Thế:</b> Hào Thế đóng ở <b>Nội Quái (Hào {_idx_h})</b> — tượng người đang ở bên trong nhà (Tại gia)")

                else:

                    _work_pts += 2

                    _loc_evidences.append(f"<b>Vị trí Hào Thế:</b> Hào Thế đóng ở <b>Ngoại Quái (Hào {_idx_h})</b> — tượng người đang ở bên ngoài / nơi làm việc")



        _nhat_cung_om = target_cung

        for _c_k, _c_v in ctb.items():

            if str(_c_v) == str(_can_n_om):

                _nhat_cung_om = int(_c_k)

                break

        _mon_nhat = str(nb.get(_nhat_cung_om, nb.get(str(_nhat_cung_om), cua_name)))

        _than_nhat = str(sb.get(_nhat_cung_om, sb.get(str(_nhat_cung_om), than_name)))

        _sao_nhat = str(tb.get(_nhat_cung_om, tb.get(str(_nhat_cung_om), sao_name)))



        if any(m in _mon_nhat for m in ['Tử', 'Hưu', 'Đỗ', 'Sinh']):

            _home_pts += 3

            _loc_evidences.append(

                f"<b>Kỳ Môn Độn Giáp (Nhật Can lâm {_mon_nhat}):</b> Nhật Can <b>{_can_n_om}</b> (bạn) tại Cung {_nhat_cung_om} lâm cửa tĩnh <b>{_mon_nhat}</b> (đóng cửa nghỉ ngơi/tĩnh tọa trong nhà, không phải Khai Môn công sở)"

            )

        elif any(m in _mon_nhat for m in ['Khai', 'Thương', 'Cảnh', 'Kinh']):

            _work_pts += 3

            _loc_evidences.append(

                f"<b>Kỳ Môn Độn Giáp (Nhật Can lâm {_mon_nhat}):</b> Nhật Can <b>{_can_n_om}</b> (bạn) tại Cung {_nhat_cung_om} lâm cửa động <b>{_mon_nhat}</b> (môi trường công sở/bên ngoài)"

            )



        if is_fake:

            _loc_evidences.append(

                f"<b>Nghiệm Chứng Câu Hỏi Thử:</b> Nhật Can rơi vào <b>Tuần Không</b> cho thấy bạn biết rõ vị trí của mình và đang đặt câu hỏi này để <b>thử độ chuẩn xác của quẻ</b>"

            )



        if _home_pts >= _work_pts:

            binary_verdict_headline = "🏠 KẾT LUẬN DỨT KHOÁT TỪ QUẺ: HIỆN TẠI BẠN ĐANG Ở NHÀ (100% KHÔNG PHẢI Ở CÔNG TY)!"

            binary_when_note = (

                f"<b>Đặc điểm nơi bạn đang ngồi ({c_info['huong']}):</b> Không gian yên tĩnh trong nhà ({c_info['places']}), "

                f"gần bạn có nhóm vật dụng <b>{h_forensic['do_vat'].split(',')[0]}</b> (Màu sắc quanh chỗ ngồi: <b>{h_forensic['mau_sac']}</b>)."

            )

            binary_action_advice = (

                f"Quẻ đã bắt trúng 100% việc hào <b>Quan Quỷ (Công ty)</b> bị Tuần Không/khắc triệt và Nhật Can lâm <b>{_mon_nhat}</b> để khẳng định bạn <b>đang ở nhà</b> chứ không phải ở công ty."

            )

        else:

            binary_verdict_headline = "🏢 KẾT LUẬN DỨT KHOÁT TỪ QUẺ: HIỆN TẠI BẠN ĐANG Ở CÔNG TY / BÊN NGOÀI (KHÔNG PHẢI Ở NHÀ)!"

            binary_when_note = (

                f"<b>Đặc điểm không gian hiện tại ({c_info['huong']}):</b> Môi trường công sở/làm việc ({_mon_nhat} · Sao {_sao_nhat}), "

                f"xung quanh có thiết bị làm việc, giấy tờ hoặc đồng nghiệp."

            )

            binary_action_advice = (

                f"Quẻ xác định rõ hào <b>Quan Quỷ / {_mon_nhat}</b> đang hoạt động hữu khí, khẳng định bạn đang ở <b>công ty / bên ngoài</b>."

            )

        binary_why_reasons = "; ".join(_loc_evidences[:4]) + "."



    elif _is_posture_state_q:

        is_binary_factual_q = True

        _static_posture = any(m in cua_name for m in ['Hưu', 'Đỗ', 'Tử', 'Sinh']) or ('Cửu Địa' in than_name) or ('Thái Âm' in than_name)

        if _static_posture:

            binary_verdict_headline = "🪑 KẾT LUẬN DỨT KHOÁT TỪ QUẺ: BẠN ĐANG NGỒI HOẶC NẰM NGHỈ TẠI CHỖ (TRẠNG THÁI TĨNH — KHÔNG PHẢI ĐANG ĐỨNG/ĐI LẠI)!"

            binary_why_reasons = f"Cung bản mệnh lâm cửa tĩnh <b>{cua_name}</b> đi cùng thần <b>{than_name}</b> và sao <b>{sao_name}</b> — biểu thị tư thế tĩnh tọa (đang ngồi trên ghế/giường hoặc tựa lưng nghỉ ngơi)."

        else:

            binary_verdict_headline = "🚶 KẾT LUẬN DỨT KHOÁT TỪ QUẺ: BẠN ĐANG ĐỨNG HOẶC ĐANG DI CHUYỂN HOẠT ĐỘNG (TRẠNG THÁI ĐỘNG)!"

            binary_why_reasons = f"Cung bản mệnh lâm cửa động <b>{cua_name}</b> đi cùng thần <b>{than_name}</b> — biểu thị cơ thể đang ở tư thế đứng hoặc vừa di chuyển."

        binary_when_note = f"Hướng không gian trước mặt bạn ứng với hướng <b>{c_info['huong']}</b> ({c_info['places']})."

        binary_action_advice = f"Dấu hiệu nghiệm chứng cơ thể đi kèm: vùng <b>{h_forensic['co_the']}</b>."



    elif _is_true_false_q:

        is_binary_factual_q = True

        if is_fake or any(t in than_name for t in ['Huyền Vũ', 'Đằng Xà']):

            binary_verdict_headline = "🚨 KẾT LUẬN DỨT KHOÁT TỪ QUẺ: ĐÂY LÀ CHUYỆN GIẢ / LỜI NÓI DỐI — KHÔNG CÓ THẬT TRÊN THỰC TẾ!"

            binary_why_reasons = "; ".join([w.replace('🔹 ', '') for w in (auth_warnings or [])[:3]]) or f"Quẻ lâm thần <b>{than_name}</b> và phạm <b>Tuần Không</b> — báo hiệu thông tin bịa đặt, hư cấu hoặc che giấu sự thật."

            binary_when_note = "Sự thật sẽ phơi bày rõ ràng ngay khi bước sang ngày/giờ xung thực Tuần Không."

            binary_action_advice = "Tuyệt đối không tin theo lời đồn hoặc thông tin chưa có chứng cứ xác thực này."

        else:

            binary_verdict_headline = "✅ KẾT LUẬN DỨT KHOÁT TỪ QUẺ: ĐÂY LÀ SỰ THẬT — THÔNG TIN ĐÁNG TIN CẬY!"

            binary_why_reasons = f"Dụng Thần <b>{dung_than}</b> hữu khí (không phạm Tuần Không), hội Sao <b>{sao_name}</b> và Cửa <b>{cua_name}</b> — khẳng định sự việc có thật và có căn cứ thực tế."

            binary_when_note = f"Thời điểm xác nhận rõ nhất: <b>{uk_exact}</b>."

            binary_action_advice = "Bạn có thể yên tâm căn cứ vào thông tin này để triển khai kế hoạch."



    elif _is_done_yet_q:

        is_binary_factual_q = True

        if is_fake or ts_stage in ('Thai', 'Dưỡng', 'Tử', 'Mộ', 'Tuyệt') or any(m in cua_name for m in ['Đỗ', 'Tử']):

            binary_verdict_headline = "⏳ KẾT LUẬN DỨT KHOÁT TỪ QUẺ: CHƯA THỰC HIỆN (SỰ VIỆC CHƯA DIỄN RA)!"

            binary_why_reasons = f"Dụng Thần <b>{dung_than}</b> đang ở trạng thái tĩnh/Tuần Không ({ts_stage or 'Tĩnh'}) kèm Cửa <b>{cua_name}</b> — báo hiệu hành động đó <b>chưa diễn ra</b>."

        else:

            binary_verdict_headline = "✅ KẾT LUẬN DỨT KHOÁT TỪ QUẺ: ĐÃ THỰC HIỆN RỒI (SỰ VIỆC ĐÃ DIỄN RA)!"

            binary_why_reasons = f"Hào Dụng Thần <b>{dung_than}</b> đã phát động/vượng khí ({ts_stage or 'Vượng'}) kèm Cửa <b>{cua_name}</b> — báo hiệu việc đó <b>đã được thực hiện xong</b>."

        binary_when_note = f"Khung giờ ứng nghiệm liên quan: <b>{uk_hour}</b>."

        binary_action_advice = f"Hướng không gian liên quan trực tiếp: <b>{c_info['huong']}</b>."



    elif (" hay " in _q_low_om) and not _is_quit_work_q and not _is_who_age_q and not _is_children_q and not any(w in _q_low_om for w in ['hay không', 'có nên', 'mưa hay nắng', 'nắng hay mưa', 'thời tiết', 'thắng hay', 'ai thắng', 'đối phương thắng', 'vụ kiện', 'tranh chấp', 'cao hay thấp', 'béo hay gầy', 'kết hôn chưa', 'độc thân', 'có vợ chưa', 'có chồng chưa', 'ở một mình hay', 'con trưởng hay']):

        # Bộ giải mã tổng quát cho MỌI câu hỏi lựa chọn "Phương án A hay Phương án B"

        import re as _re_ab

        _m_ab = _re_ab.search(r'(?:đang\s+|là\s+|nên\s+|chọn\s+)?([^,?.;!]+?)\s+hay\s+([^,?.;!]+)', _q_low_om)

        if _m_ab:

            _opt_a = _m_ab.group(1).strip()

            _opt_b = _m_ab.group(2).strip()

            for _pfx in ['tôi đang ', 'tôi ', 'bạn đang ', 'nó đang ', 'hiện tại đang ', 'hiện tại ']:

                if _opt_a.startswith(_pfx):

                    _opt_a = _opt_a[len(_pfx):].strip()

            if _opt_a and _opt_b and _opt_a != _opt_b:

                is_binary_factual_q = True

                # So sánh Trục 1 (Hào Thế / Nội Quái / Quẻ Chủ = Phương án A) và Trục 2 (Hào Ứng / Ngoại Quái / Quẻ Biến = Phương án B)

                _ung_in_kv = False

                _the_in_kv = False

                for _h_it in lh_haos:

                    if isinstance(_h_it, dict):

                        _tu_h = str(_h_it.get('the_ung') or _h_it.get('tu') or '')

                        _chi_h = str(_h_it.get('chi') or _h_it.get('can_chi') or '').split()[-1] if (_h_it.get('chi') or _h_it.get('can_chi')) else ''

                        if 'Ứng' in _tu_h and _chi_h in _kv_om:

                            _ung_in_kv = True

                        if 'Thế' in _tu_h and _chi_h in _kv_om:

                            _the_in_kv = True

                if _ung_in_kv or (weighted_pct >= 50 and not _the_in_kv):

                    _chosen_opt = _opt_a.upper()

                    _rejected_opt = _opt_b.upper()

                    _ab_reason = (

                        f"Quẻ Chủ <b>{ten_que_ban}</b> (ứng với phương án 1: <b>{_opt_a}</b>) đang nắm chủ quyền tại Cung {target_cung} ({c_info['quai']} · Sao {sao_name} · Cửa {cua_name}), "

                        f"trong khi phương án 2 (<b>{_opt_b}</b>) bị Tuần Không/suy khí trên trục Ứng/Biến ({ten_que_bien or 'Biến quái'})."

                    )

                else:

                    _chosen_opt = _opt_b.upper()

                    _rejected_opt = _opt_a.upper()

                    _ab_reason = (

                        f"Hào Động trên quẻ <b>{ten_que_ban}</b> chuyển hóa mạnh sang Quẻ Biến <b>{ten_que_bien or 'Biến cuộc'}</b> (ứng với phương án 2: <b>{_opt_b}</b>) "

                        f"tại Cung {target_cung} ({c_info['quai']} · Sao {sao_name} · Cửa {cua_name}), vượt trội hơn phương án 1 (<b>{_opt_a}</b>)."

                    )

                binary_verdict_headline = f"🎯 KẾT LUẬN DỨT KHOÁT TỪ QUẺ: {_chosen_opt} (LOẠI TRỪ PHƯƠNG ÁN: {_rejected_opt})!"

                binary_why_reasons = _ab_reason

                binary_when_note = f"Thời điểm & không gian ứng nghiệm: <b>{uk_exact}</b> tại hướng <b>{c_info['huong']}</b>."

                binary_action_advice = f"Quẻ đã phân định dứt khoát nghiêng hẳn về <b>{_chosen_opt}</b> dựa trên hào Thế/Ứng, Tuần Không và bàn Kỳ Môn."



    # ═════════════════════════════════════════════════════════════════════════

    # CHIỀU 6: CƠ THỂ, SỨC KHỎE & PHÁP QUYẾT HÓA GIẢI

    # ═════════════════════════════════════════════════════════════════════════

    health_str = (

        f"<b>Bộ phận cơ thể ứng quẻ ({hanh_dt} – Cung {c_info['quai']}):</b> {h_forensic['co_the']}. "

        f"Nếu xem bệnh hoặc sức khỏe người liên quan: lưu ý triệu chứng tại vùng này do Sao <b>{sao_name}</b> tác động."

    )

    remedy_str = f"<b>Pháp quyết hành động & Hóa giải:</b> {h_forensic['hoa_giai']}"



    # ═════════════════════════════════════════════════════════════════════════

    # BUILD MARKDOWN TEXT (CHO OFFLINE FULL OUTPUT & GEMINI PROMPT)

    # ═════════════════════════════════════════════════════════════════════════

    text_lines = [

        "### 🔮 HỒ SƠ TIÊN TRI TOÀN TRI 360° — GIẢI MÃ CHI TIẾT MỌI SỰ VIỆC (V99)",

        f"1. **📜 SỰ VIỆC CHI TIẾT & DIỄN BIẾN 3 THỜI:**",

        f"   - **Quá khứ (Nguyên nhân):** {event_past}",

        f"   - **Hiện tại (Ẩn tình & Thực tế):** {event_present}",

        f"   - **Tương lai (Kết cục):** {event_future}",

        f"2. **⏰ THỜI ĐIỂM XẢY RA CHÍNH XÁC (NĂM – THÁNG – NGÀY – GIỜ – KHẮC – PHÚT):**",

        f"   - **Chốt thời điểm hội tụ:** {uk_exact}",

        f"   - **Phút / Khắc ứng nghiệm:** {uk_minute}",

        f"   - **Giờ ứng nghiệm:** {uk_hour}",

        f"   - **Ngày ứng nghiệm:** {uk_day}",

        f"   - **Tháng & Năm:** {uk_month} | {uk_year} ({uk_speed})",

        f"3. **📍 ĐỊA ĐIỂM, PHƯƠNG HƯỚNG & HIỆN TRƯỜNG (Ở ĐÂU):**",

        f"   - **Phương hướng & Khoảng cách:** {where_summary}",

        f"   - **Hiện trường & Độ cao:** {where_scene}",

        f"4. **👤 HỒ SƠ CON NGƯỜI (TRAI HAY GÁI, GIÀ HAY TRẺ, TUỔI, NGOẠI HÌNH, QUEN HAY LẠ):**",

        f"   - **Giới tính:** {primary_gender} ({', '.join(gender_reasons)}) — {secondary_gender}",

        f"   - **Độ tuổi (Già hay Trẻ):** {age_tier} | **Tuổi cụ thể dự báo:** {', '.join(birth_years)}",

        f"   - **Ngoại hình & Thần thái:** {appearance_str}",

        f"   - **Tâm lý & Động cơ:** {motive_str}",

        f"   - **Nghề nghiệp & Quan hệ:** Ngành {h_forensic['nghe_nghiep']} | Quan hệ: **{familiar_str}**",

        f"5. **📦 HỒ SƠ ĐỒ VẬT, TÀI SẢN & SỐ LƯỢNG (ĐỒ VẬT GÌ, MÀU SẮC, CHẤT LIỆU, MỚI/CŨ):**",

        f"   - **Đồ vật / Sự vật cụ thể:** {combined_objects}",

        f"   - **Màu sắc & Chất liệu:** Màu **{h_forensic['mau_sac']}** | Chất liệu: **{h_forensic['chat_lieu']}**",

        f"   - **Hình dáng & Tình trạng:** {h_forensic['hinh_dang']} ({item_size}) | Tình trạng: **{item_condition}**",

        f"   - **Số lượng & Con số:** {quantity_str}",

        f"6. **🏥 CƠ THỂ, SỨC KHỎE & HÓA GIẢI:**",

        f"   - {health_str}",

        f"   - {remedy_str}",

    ]

    plain_text = "\n".join(text_lines)



    # ═════════════════════════════════════════════════════════════════════════

    # BUILD GIAO DIỆN HTML — V99.9: CHỈ HIỂN THỊ ĐÚNG TRỌNG TÂM CÂU HỎI

    # (Hỏi gì trả lời đúng trọng tâm đó, tuyệt đối không hiện mục lan man không liên quan)

    # ═════════════════════════════════════════════════════════════════════════

    _q_focus = (question or '').lower()

    _is_health_focus = any(w in _q_focus for w in [

        'bệnh', 'ốm', 'đau', 'khỏe', 'sức khỏe', 'qua khỏi', 'qua được', 'sống', 'chết',

        'viện', 'thuốc', 'mổ', 'phẫu thuật', 'ung thư', 'tai nạn', 'hồi phục', 'nguy kịch', 'khám'

    ])

    _is_love_focus = any(w in _q_focus for w in [

        'yêu', 'tình cảm', 'hôn nhân', 'vợ', 'chồng', 'người yêu', 'bạn trai', 'bạn gái',

        'cưới', 'chia tay', 'ly hôn', 'quay lại', 'thật lòng', 'ngoại tình', 'duyên'

    ]) and not _is_health_focus

    _is_find_where_focus = any(w in _q_focus for w in [

        'tìm', 'mất', 'thất lạc', 'trộm', 'ở đâu', 'chỗ nào', 'hướng nào', 'để đâu', 'cất đâu',

        'nhà', 'đất', 'mộ', 'phong thủy', 'xuất hành', 'đi xa', 'du lịch', 'chuyển nhà'

    ]) and not _is_love_focus

    # Chỉ đoán Giới tính (Trai/Gái) & Tuổi khi câu hỏi thực sự hỏi AI / TRAI HAY GÁI / BAO NHIÊU TUỔI / KẺ GIAN

    _is_person_focus = any(w in _q_focus for w in [

        'là ai', 'ai lấy', 'ai làm', 'người nào', 'trai hay gái', 'nam hay nữ',

        'bao nhiêu tuổi', 'mấy tuổi', 'già hay trẻ', 'trộm', 'kẻ gian', 'người lạ',

        'người con', 'mấy con', 'bao nhiêu con', 'mấy trai', 'mấy gái', 'con cái', 'anh chị em'

    ])

    _is_object_count_focus = any(w in _q_focus for w in [

        'cái gì', 'đồ gì', 'vật gì', 'trong hộp', 'mất ví', 'mất đồ', 'thất lạc', 'điện thoại',

        'chìa khóa', 'sổ đỏ', 'giấy tờ', 'trang sức', 'mấy cái', 'con số', 'định giá'

    ]) and not _is_health_focus and not _is_love_focus and not _is_person_focus and not _is_children_q



    # V99.9.7: Nối toàn bộ diễn biến Quá khứ - Hiện tại - Tương lai, Trọng tâm câu hỏi & Ứng kỳ thành các đoạn văn liền mạch dễ đọc

    _focus_prose = ""

    if _is_love_focus:

        _who_lbl = "người vợ" if "vợ" in _q_focus else ("người chồng" if "chồng" in _q_focus else "đối phương")

        _focus_prose = (

            f" Xét riêng về tâm lý và tình cảm của {_who_lbl} (ứng tại Cung {target_cung} {c_info['quai']}, hành {hanh_dt}, "

            f"đi cùng Sao {sao_name}, Cửa {cua_name} và Thần {than_name}), {motive_str[0].lower() + motive_str[1:]}"

        )

    elif _is_health_focus:

        _focus_prose = f" Về mặt Y Dịch và sức khỏe cơ thể: {health_str}"

    elif _is_find_where_focus:

        _focus_prose = f" Về phương vị và địa điểm thực tế: {where_summary} Đặc điểm hiện trường xung quanh: {where_scene}"

    elif _is_person_focus:

        _focus_prose = (

            f" Về đặc điểm người liên quan trong quẻ: ứng vào giới tính <b>{primary_gender}</b> "

            f"({age_tier}, khoảng năm sinh {', '.join(birth_years[:3])}), mối quan hệ thuộc nhóm <b>{familiar_str}</b>. "

            f"{appearance_str} {motive_str}"

        )

    elif _is_object_count_focus:

        _focus_prose = (

            f" Về đặc điểm sự vật và định lượng: ứng với nhóm <b>{combined_objects}</b>, "

            f"màu sắc chủ đạo là <b>{h_forensic['mau_sac']}</b>, chất liệu <b>{h_forensic['chat_lieu']}</b> "

            f"({item_condition}). {quantity_str}"

        )



    _para_story = (

        f"Xét mạch vận động của sự việc từ gốc tới ngọn: <b>Về khởi nguồn</b>, {event_past[0].lower() + event_past[1:].rstrip('.') if event_past else ''}. "

        f"<b>Bước sang thực trạng hiện tại</b>, {event_present[0].lower() + event_present[1:].rstrip('.') if event_present else ''}."

        f"{_focus_prose} "

        f"<b>Dự báo về xu hướng sắp tới</b>, {event_future[0].lower() + event_future[1:].rstrip('.') if event_future else ''}."

    )



    _para_timing = (

        f"<b>Về thời điểm ứng nghiệm và hướng xử lý:</b> Mốc thời gian hội tụ khí số rõ nét nhất rơi vào khoảng "

        f"<b style='color:#fef08a;'>{uk_exact}</b> (khung giờ thuận lợi: {uk_hour}). "

        f"Để thúc đẩy cục diện chuyển biến theo chiều hướng tốt nhất, bạn nên áp dụng pháp quyết: {h_forensic['hoa_giai']}"

    )



    html_block = (

        f'<div style="margin-top:14px;padding:18px 20px;background:linear-gradient(135deg,rgba(15,23,42,0.92),rgba(30,27,75,0.92));'

        f'border-radius:14px;border:2px solid #f59e0b;box-shadow:0 4px 20px rgba(245,158,11,0.22);line-height:1.75;font-size:0.98em;">'

        f'<div style="font-size:1.08em;font-weight:900;color:#fbbf24;margin-bottom:10px;border-bottom:1px solid rgba(251,191,36,0.3);padding-bottom:6px;">'

        f'🔮 DIỄN BIẾN SỰ VIỆC & CHẨN ĐOÁN CHUYÊN SÂU THEO TRỌNG TÂM CÂU HỎI</div>'

        f'<p style="margin:0 0 12px 0;color:#e2e8f0;text-align:justify;">{_para_story}</p>'

        f'<p style="margin:0;color:#fef3c7;text-align:justify;">{_para_timing}</p>'

        f'</div>'

    )



    # V99.9: Lọc plain_text theo đúng trọng tâm câu hỏi để AI Online không bị nhiễu bởi dữ liệu đồ vật/giới tính không liên quan

    _filtered_lines = [

        "### 🔮 HỒ SƠ CHUYÊN SÂU ĐÚNG TRỌNG TÂM CÂU HỎI (V99.9)",

        f"1. **📜 DIỄN BIẾN SỰ VIỆC 3 THỜI (QUÁ KHỨ - HIỆN TẠI - TƯƠNG LAI):**",

        f"   - **Quá khứ (Nguyên nhân):** {event_past}",

        f"   - **Hiện tại (Ẩn tình & Thực tế):** {event_present}",

        f"   - **Tương lai (Kết cục):** {event_future}",

        f"2. **⏰ THỜI ĐIỂM ỨNG KỲ CHÍNH XÁC:** {uk_exact} ({uk_day} | {uk_hour} | {uk_minute})",

    ]

    if _is_love_focus:

        _filtered_lines.append(f"3. **❤️ TÂM LÝ & TÌNH CẢM ĐỐI PHƯƠNG:** Cung {target_cung} ({c_info['quai']}), Sao {sao_name}, Cửa {cua_name}, Thần {than_name} — {door_desc} {motive_str} ({deity_desc})")

    if _is_health_focus:

        _filtered_lines.append(f"3. **🏥 CHẨN ĐOÁN Y DỊCH & CƠ THỂ:** {health_str}")

    if _is_find_where_focus:

        _filtered_lines.append(f"3. **📍 ĐỊA ĐIỂM & HIỆN TRƯỜNG:** {where_summary} | {where_scene}")

    if is_binary_factual_q:

        _filtered_lines.append(f"3. **🎯 KẾT LUẬN DỨT KHOÁT CÂU HỎI LỰA CHỌN / THỰC TẾ TỪ QUẺ:** {binary_verdict_headline}")

        _filtered_lines.append(f"   - **Căn cứ bắt bài từ quẻ:** {binary_why_reasons}")

        _filtered_lines.append(f"   - **Đặc điểm không gian/thời gian:** {binary_when_note}")

        _filtered_lines.append(f"   - **Kết luận nghiệm chứng:** {binary_action_advice}")

    elif _is_children_q:

        _filtered_lines.append(f"3. **👶 LUẬN ĐOÁN TỬ TỨC / CON CÁI SÁT TỪ QUẺ:** {children_summary}")

        _filtered_lines.append(f"   - **Căn cứ từ Quẻ Chủ/Hỗ/Biến, Hào Tử Tôn & Cung Kỳ Môn:** {children_reasons}")

        _filtered_lines.append(f"   - **Tính cách & Tương lai các con:** {children_traits}")

        _filtered_lines.append(f"   - **Lời khuyên cho cha mẹ:** {children_advice}")

    elif _is_person_focus:

        _filtered_lines.append(f"4. **👤 NHẬN DẠNG NGƯỜI LIÊN QUAN:** Giới tính {primary_gender}, Độ tuổi {age_tier} ({', '.join(birth_years)}), Ngoại hình: {appearance_str}")

    if _is_object_count_focus:

        _filtered_lines.append(f"5. **📦 ĐẶC ĐIỂM ĐỒ VẬT & ĐỊNH LƯỢNG:** {combined_objects} | Màu {h_forensic['mau_sac']} | {item_condition} | {quantity_str}")

    _filtered_lines.append(f"6. **🧭 PHÁP QUYẾT HÓA GIẢI:** {remedy_str}")

    plain_text = "\n".join(_filtered_lines)



    return {

        'html': html_block,

        'text': plain_text,

        'data': {

            'target_cung': target_cung,

            'quai': c_info['quai'],

            'hanh_dt': hanh_dt,

            'hanh': hanh_dt,

            'c_info': c_info,

            'sao_name': sao_name,

            'cua_name': cua_name,

            'than_name': than_name,

            'ts_stage': ts_stage,

            'ten_que_ban': ten_que_ban,

            'ten_que_bien': ten_que_bien,

            'gender': primary_gender,

            'gender_reasons': ', '.join(gender_reasons),

            'age_tier': age_tier,

            'birth_years': birth_years,

            'is_fake': bool(is_fake),

            'auth_warnings': auth_warnings,

            'fake_summary': (

                "NGHIỆM CHỨNG TỪ QUẺ (PHÁT HIỆN TUẦN KHÔNG / KHÔNG VONG): SỰ VIỆC HOẶC ĐỐI TƯỢNG BẠN HỎI HIỆN KHÔNG CÓ THẬT NGOÀI ĐỜI (HOẶC CHƯA TỒN TẠI / BẠN ĐANG HỎI THỬ LÒNG QUẺ)!"

                if is_fake else ""

            ),

            'is_binary_factual_q': is_binary_factual_q,

            'binary_verdict_headline': binary_verdict_headline,

            'binary_why_reasons': binary_why_reasons,

            'binary_when_note': binary_when_note,

            'binary_action_advice': binary_action_advice,

            'is_children_question': _is_children_q,

            'is_children_age_question': _is_children_age_q,

            'children_summary': children_summary,

            'children_reasons': children_reasons,

            'children_traits': children_traits,

            'children_advice': children_advice,

            'children_age_headline': children_age_headline,

            'children_age_why': children_age_why,

            'children_age_when': children_age_when,

            'children_age_advice': children_age_advice,

            'testing_mindset_note': _testing_note_str,

            'where_summary': where_summary,

            'where_scene': where_scene,

            'objects': combined_objects,

            'colors': h_forensic['mau_sac'],

            'materials': h_forensic['chat_lieu'],

            'material': h_forensic['chat_lieu'],

            'shape': h_forensic['hinh_dang'],

            'condition': item_condition,

            'item_condition': item_condition,

            'appearance': appearance_str,

            'personality': appearance_str,

            'career': h_forensic.get('nghe_nghiep', ''),

            'motive': motive_str,

            'quantity': quantity_str,

            'exact_timestamp': uk_exact,

            'minute': uk_minute,

            'co_the': h_forensic['co_the'],

            'hoa_giai': h_forensic['hoa_giai'],

            'huong': c_info['huong'],

            'quai_name': c_info['quai'],

            'places': c_info['places'],

            'height_desc': height_desc,

        },

    }


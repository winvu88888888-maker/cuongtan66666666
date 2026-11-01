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
    target_cung = cung_sv if (dung_than == 'Bản Thân' and cung_sv != cung_dt) else cung_dt
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
    lh_haos = lh_ban.get('haos') or lh_ban.get('details', []) or []
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

    total_votes = max(male_votes + female_votes, 1)
    if male_votes >= female_votes:
        primary_gender = f"NAM GIỚI / ĐÀN ÔNG (Trai — độ hội tụ {int(round(male_votes * 100 / total_votes))}%)"
        secondary_gender = "Có thể có 1 Nữ giới hỗ trợ/đi kèm ở vòng ngoài" if female_votes >= 2 else "Chủ yếu là Nam giới"
    else:
        primary_gender = f"NỮ GIỚI / PHỤ NỮ (Gái — độ hội tụ {int(round(female_votes * 100 / total_votes))}%)"
        secondary_gender = "Có thể có 1 Nam giới liên đới/đứng sau" if male_votes >= 2 else "Chủ yếu là Nữ giới"

    # Độ tuổi (Già hay Trẻ, bao nhiêu tuổi cụ thể)
    base_ages = list(c_info['base_ages'])
    if ts_stage in ('Trường Sinh', 'Mộc Dục', 'Thai', 'Dưỡng'):
        age_tier = "NGƯỜI TRẺ TUỔI / THANH THIẾU NIÊN"
        est_ages = [max(16, a - 12) for a in base_ages[:3]]
    elif ts_stage in ('Suy', 'Bệnh', 'Tử', 'Mộ', 'Tuyệt'):
        age_tier = "NGƯỜI LỚN TUỔI / TRUNG NIÊN CAO (GIÀ DẶN)"
        est_ages = [min(78, a + 12) for a in base_ages[:3]]
    else:
        age_tier = c_info['age_group'].upper()
        est_ages = base_ages[:3]

    cur_year = datetime.date.today().year
    birth_years = [f"{cur_year - a} ({a} tuổi)" for a in est_ages]

    # Ngoại hình, Tính cách, Nghề nghiệp, Quen hay Lạ
    appearance_str = f"{can_g_info[1]}; thần thái mang nét {star_g_matched[1].lower()}."
    familiar_str = (
        "NGƯỜI QUEN / NỘI BỘ (Người trong nhà, đồng nghiệp, bạn bè hoặc người từng tiếp xúc)"
        if is_noi_ban else
        "NGƯỜI LẠ / BÊN NGOÀI (Người ở xa, khách vãng lai, đối tác mới hoặc người ngoài khu vực)"
    )
    if 'Huyền Vũ' in than_name or 'Thái Âm' in than_name:
        motive_str = "Hành động lén lút, kín đáo, che giấu thông tin hoặc có mưu tính ngầm."
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
        f"(Số lượng: <b>{hd_1}</b> hoặc <b>{lt_num}</b> cái/đơn vị; "
        f"Bội số giá trị/tài lộc: <b>{hd_1}0, {lt_num}0, {hd_2}00</b>)"
    )

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
    # BUILD GIAO DIỆN HTML (HIỂN THỊ TRỰC TIẾP TRONG CARD KẾT LUẬN CHÍNH)
    # ═════════════════════════════════════════════════════════════════════════
    html_block = (
        f'<div style="margin-top:14px;padding:18px;background:linear-gradient(135deg,rgba(15,23,42,0.92),rgba(30,27,75,0.92));'
        f'border-radius:14px;border:2px solid #f59e0b;box-shadow:0 4px 20px rgba(245,158,11,0.25);">'
        f'<div style="font-size:1.15em;font-weight:900;color:#fbbf24;margin-bottom:6px;border-bottom:1px solid rgba(251,191,36,0.3);padding-bottom:8px;">'
        f'🔮 TỔNG HỢP LUẬN GIẢI CHI TIẾT 360° — SỰ VIỆC · THỜI GIAN · ĐỊA ĐIỂM · CON NGƯỜI · ĐỒ VẬT</div>'
        f'<div style="font-size:0.82em;color:#cbd5e1;margin-bottom:10px;font-style:italic;">'
        f'ℹ️ Lưu ý: Các thông tin dưới đây được suy diễn từ quy tắc biểu tượng cổ học truyền thống (Kinh Dịch, Kỳ Môn, Lục Hào, Mai Hoa), chỉ mang tính chất tham khảo văn hóa và chiêm nghiệm.</div>'

        # 1. SỰ VIỆC CHI TIẾT
        f'<div style="margin-bottom:10px;padding:10px 12px;background:rgba(255,255,255,0.05);border-radius:10px;border-left:4px solid #38bdf8;">'
        f'<div style="color:#38bdf8;font-weight:800;font-size:0.98em;margin-bottom:4px;">📜 1. SỰ VIỆC CHI TIẾT & DIỄN BIẾN 3 THỜI (QUÁ KHỨ – HIỆN TẠI – TƯƠNG LAI)</div>'
        f'<div style="color:#e2e8f0;font-size:0.9em;line-height:1.55;">'
        f'• <b>Khởi nguồn (Quá khứ):</b> {event_past}<br>'
        f'• <b>Diễn biến thật (Hiện tại):</b> {event_present}<br>'
        f'• <b>Kết cục (Tương lai):</b> {event_future}'
        f'</div></div>'

        # 2. THỜI ĐIỂM CHÍNH XÁC (NĂM - THÁNG - NGÀY - GIỜ - KHẮC - PHÚT)
        f'<div style="margin-bottom:10px;padding:10px 12px;background:rgba(245,158,11,0.1);border-radius:10px;border-left:4px solid #fbbf24;">'
        f'<div style="color:#fde047;font-weight:800;font-size:0.98em;margin-bottom:4px;">⏰ 2. XẢY RA LÚC NÀO? (NĂM – THÁNG – NGÀY – GIỜ – KHẮC – PHÚT CHÍNH XÁC)</div>'
        f'<div style="color:#f8fafc;font-size:0.9em;line-height:1.55;">'
        f'• 🎯 <b>Chốt thời điểm hội tụ:</b> <span style="color:#fef08a;font-weight:700;">{uk_exact}</span><br>'
        f'• ⏱️ <b>Phút & Khắc ứng nghiệm:</b> {uk_minute}<br>'
        f'• 🕐 <b>Giờ Địa Chi:</b> {uk_hour}<br>'
        f'• 📅 <b>Ngày Dương / Âm lịch:</b> {uk_day}<br>'
        f'• 🗓️ <b>Tháng & Năm:</b> {uk_month} | {uk_year} — <i>{uk_speed}</i>'
        f'</div></div>'

        # 3. Ở ĐÂU (ĐỊA ĐIỂM, PHƯƠNG HƯỚNG, KHOẢNG CÁCH, ĐỘ CAO)
        f'<div style="margin-bottom:10px;padding:10px 12px;background:rgba(16,185,129,0.08);border-radius:10px;border-left:4px solid #34d399;">'
        f'<div style="color:#34d399;font-weight:800;font-size:0.98em;margin-bottom:4px;">📍 3. Ở ĐÂU? (PHƯƠNG HƯỚNG – KHOẢNG CÁCH – ĐỘ CAO – MÔ TẢ HIỆN TRƯỜNG)</div>'
        f'<div style="color:#e2e8f0;font-size:0.9em;line-height:1.55;">'
        f'• 🧭 {where_summary}<br>'
        f'• 🏠 {where_scene}'
        f'</div></div>'

        # 4. CON NGƯỜI (TRAI HAY GÁI, GIÀ HAY TRẺ, TUỔI, NGOẠI HÌNH, QUEN HAY LẠ)
        f'<div style="margin-bottom:10px;padding:10px 12px;background:rgba(168,85,247,0.1);border-radius:10px;border-left:4px solid #c084fc;">'
        f'<div style="color:#e9d5ff;font-weight:800;font-size:0.98em;margin-bottom:4px;">👤 4. CON NGƯỜI LIÊN QUAN (TRAI HAY GÁI · GIÀ HAY TRẺ · TUỔI · NGOẠI HÌNH · QUEN HAY LẠ)</div>'
        f'<div style="color:#f3e8ff;font-size:0.9em;line-height:1.55;">'
        f'• 🚻 <b>Giới tính (Trai hay Gái):</b> <span style="color:#fde047;font-weight:700;">{primary_gender}</span> '
        f'<span style="color:#cbd5e1;font-size:0.88em;">[{", ".join(gender_reasons)}] — {secondary_gender}</span><br>'
        f'• 🎂 <b>Độ tuổi (Già hay Trẻ):</b> <b>{age_tier}</b> | 🎯 <b>Tuổi dự báo sát nhất:</b> <b>{", ".join(birth_years)}</b><br>'
        f'• 🧑 <b>Ngoại hình & Tính cách:</b> {appearance_str} {motive_str}<br>'
        f'• 💼 <b>Nghề nghiệp & Quan hệ:</b> Lĩnh vực {h_forensic["nghe_nghiep"]} | <b>{familiar_str}</b>'
        f'</div></div>'

        # 5. ĐỒ VẬT, MÀU SẮC, CHẤT LIỆU, SỐ LƯỢNG
        f'<div style="margin-bottom:10px;padding:10px 12px;background:rgba(236,72,153,0.08);border-radius:10px;border-left:4px solid #f472b6;">'
        f'<div style="color:#fbcfe8;font-weight:800;font-size:0.98em;margin-bottom:4px;">📦 5. ĐỒ VẬT & TÀI SẢN (ĐỒ VẬT GÌ · MÀU SẮC · CHẤT LIỆU · HÌNH DÁNG · MỚI/CŨ · SỐ LƯỢNG)</div>'
        f'<div style="color:#fce7f3;font-size:0.9em;line-height:1.55;">'
        f'• 🔮 <b>Đồ vật / Sự vật cụ thể:</b> <b>{combined_objects}</b><br>'
        f'• 🎨 <b>Màu sắc & Chất liệu:</b> Màu <b>{h_forensic["mau_sac"]}</b> | Chất liệu: <b>{h_forensic["chat_lieu"]}</b><br>'
        f'• 📐 <b>Hình dáng & Tình trạng:</b> {h_forensic["hinh_dang"]} ({item_size}) — <b>{item_condition}</b><br>'
        f'• 🔢 <b>Số lượng & Giá trị:</b> {quantity_str}'
        f'</div></div>'

        # 6. CƠ THỂ & HÓA GIẢI
        f'<div style="padding:10px 12px;background:rgba(59,130,246,0.08);border-radius:10px;border-left:4px solid #60a5fa;">'
        f'<div style="color:#93c5fd;font-weight:800;font-size:0.98em;margin-bottom:4px;">🏥 6. CƠ THỂ, SỨC KHỎE & PHÁP QUYẾT HÓA GIẢI</div>'
        f'<div style="color:#dbeafe;font-size:0.9em;line-height:1.55;">'
        f'• {health_str}<br>'
        f'• {remedy_str}'
        f'</div></div>'
        f'</div>'
    )

    return {
        'html': html_block,
        'text': plain_text,
        'data': {
            'target_cung': target_cung,
            'quai': c_info['quai'],
            'hanh_dt': hanh_dt,
            'gender': primary_gender,
            'age_tier': age_tier,
            'birth_years': birth_years,
            'where_summary': where_summary,
            'where_scene': where_scene,
            'objects': combined_objects,
            'colors': h_forensic['mau_sac'],
            'materials': h_forensic['chat_lieu'],
            'condition': item_condition,
            'quantity': quantity_str,
            'exact_timestamp': uk_exact,
            'minute': uk_minute,
        },
    }

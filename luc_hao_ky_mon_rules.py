# -*- coding: utf-8 -*-
"""
LỤC HÀO QUY TẮC LUẬN GIẢI NÂNG CAO
+ KỲ MÔN CÁCH CỤC
Nguồn: bocdich.com, kinhdichluchao.vn, phongthuynhattam.com
"""

# ======================================================================
# 1. DỤNG THẦN — Bảng tra theo chủ đề
# ======================================================================
DUNG_THAN_MAP = {
    "tài_lộc": {"luc_than": "Thê Tài", "mo_ta": "Tài lộc, tiền bạc, vợ (nam hỏi)", "ky_mon": "Can Giờ"},
    "công_danh": {"luc_than": "Quan Quỷ", "mo_ta": "Sự nghiệp, thi cử, chồng (nữ hỏi), bệnh", "ky_mon": "Can Giờ"},
    "con_cái": {"luc_than": "Tử Tôn", "mo_ta": "Con cái, bình an, thuốc, cầu phúc", "ky_mon": "Can Giờ"},
    "cha_mẹ": {"luc_than": "Phụ Mẫu", "mo_ta": "Cha mẹ, nhà cửa, xe cộ, văn thư, hợp đồng", "ky_mon": "Can Năm"},
    "anh_em": {"luc_than": "Huynh Đệ", "mo_ta": "Anh chị em, bạn bè, đối thủ cạnh tranh", "ky_mon": "Can Tháng"},
    "bản_thân": {"luc_than": "Thế Hào", "mo_ta": "Bản thân, sức khỏe, tâm trạng", "ky_mon": "Can Ngày"},
    "hôn_nhân": {"luc_than": "Thê Tài/Quan Quỷ", "mo_ta": "Nam: Thê Tài = vợ. Nữ: Quan Quỷ = chồng", "ky_mon": "Can Giờ"},
    "kiện_tụng": {"luc_than": "Quan Quỷ", "mo_ta": "Quan = thắng kiện. Thế hào = bên mình", "ky_mon": "Can Giờ"},
    "bệnh_tật": {"luc_than": "Quan Quỷ", "mo_ta": "Quan Quỷ = bệnh. Tử Tôn = thuốc. Phụ Mẫu = bác sĩ", "ky_mon": "Can Giờ"},
    "tìm_đồ": {"luc_than": "Thê Tài", "mo_ta": "Thê Tài = đồ vật. Cung/Hào chỉ hướng/nơi", "ky_mon": "Can Giờ"},
    "xuất_hành": {"luc_than": "Thế Hào", "mo_ta": "Thế sinh Ứng = đi được. Ứng khắc Thế = nguy", "ky_mon": "Can Ngày"},
    "đầu_tư": {"luc_than": "Thê Tài", "mo_ta": "Thê Tài vượng = có lời. Huynh Đệ động = thua lỗ", "ky_mon": "Can Giờ"},
}

# ======================================================================
# 2. NGUYÊN THẦN / KỴ THẦN / CỪU THẦN — Quan hệ Ngũ Hành
# ======================================================================
NGUYEN_KY_CUU = {
    "Kim": {"nguyen_than": "Thổ", "ky_than": "Hỏa", "cuu_than": "Mộc"},
    "Mộc": {"nguyen_than": "Thủy", "ky_than": "Kim", "cuu_than": "Thổ"},
    "Thủy": {"nguyen_than": "Kim", "ky_than": "Thổ", "cuu_than": "Hỏa"},
    "Hỏa": {"nguyen_than": "Mộc", "ky_than": "Thủy", "cuu_than": "Kim"},
    "Thổ": {"nguyen_than": "Hỏa", "ky_than": "Mộc", "cuu_than": "Thủy"},
}

# ======================================================================
# 3. QUY TẮC LUẬN GIẢI LỤC HÀO (18 QUY TẮC VÀNG)
# ======================================================================
LUC_HAO_RULES = [
    # === NHÓM 1: DỤNG THẦN VƯỢNG SUY ===
    {
        "id": "R01", "ten": "Dụng Thần Vượng",
        "dk": "Dụng Thần được Nhật/Nguyệt sinh hoặc tỷ hòa",
        "ket_luan": "ĐẠI CÁT — Sự việc thành công, thuận lợi", "muc_do": "ĐẠI CÁT"
    },
    {
        "id": "R02", "ten": "Dụng Thần Suy", 
        "dk": "Dụng Thần bị Nhật/Nguyệt khắc, hưu tù",
        "ket_luan": "HUNG — Sự việc khó thành, gặp trở ngại", "muc_do": "HUNG"
    },
    {
        "id": "R03", "ten": "Dụng Thần Không Vong",
        "dk": "Dụng Thần lâm Tuần Không",
        "ket_luan": "Sự việc trống rỗng, chưa có kết quả. Chờ xuất Không mới ứng", "muc_do": "HUNG"
    },
    {
        "id": "R04", "ten": "Dụng Thần Nguyệt Phá",
        "dk": "Dụng Thần Chi bị Nguyệt lệnh xung",
        "ket_luan": "Hư hại, tan vỡ, mất mát. Phải chờ qua tháng xung mới hồi phục", "muc_do": "ĐẠI HUNG"
    },
    # === NHÓM 2: NGUYÊN THẦN - KỴ THẦN ===
    {
        "id": "R05", "ten": "Nguyên Thần Vượng Động",
        "dk": "Nguyên Thần động + vượng → sinh Dụng Thần",
        "ket_luan": "CÁT — Có quý nhân giúp đỡ, sự việc hanh thông", "muc_do": "CÁT"
    },
    {
        "id": "R06", "ten": "Kỵ Thần Vượng Động",
        "dk": "Kỵ Thần động + vượng → khắc Dụng Thần",
        "ket_luan": "HUNG — Có kẻ phá hoại, sự việc bị cản trở", "muc_do": "HUNG"
    },
    {
        "id": "R07", "ten": "Kỵ Thần Động nhưng Nguyên Thần cứu",
        "dk": "Kỵ Thần động nhưng Nguyên Thần cũng động + vượng",
        "ket_luan": "Trước khó sau dễ — Gặp khó khăn rồi có người giúp vượt qua", "muc_do": "BÌNH"
    },
    # === NHÓM 3: HÀO ĐỘNG + BIẾN ===
    {
        "id": "R08", "ten": "Hào Động Sinh Dụng Thần",
        "dk": "Hào động sinh Dụng Thần (Ngũ Hành)",
        "ket_luan": "CÁT — Có lực hỗ trợ, sự việc được thúc đẩy", "muc_do": "CÁT"
    },
    {
        "id": "R09", "ten": "Hào Động Khắc Dụng Thần",
        "dk": "Hào động khắc Dụng Thần",
        "ket_luan": "HUNG — Có lực cản trở, gặp đối thủ mạnh", "muc_do": "HUNG"
    },
    {
        "id": "R10", "ten": "Hóa Tiến Thần",
        "dk": "Dụng Thần động hóa ra hào cùng hành nhưng tiến lên (VD: Dần→Mão)",
        "ket_luan": "ĐẠI CÁT — Tiến triển mạnh mẽ, phát triển nhanh", "muc_do": "ĐẠI CÁT"
    },
    {
        "id": "R11", "ten": "Hóa Thoái Thần",
        "dk": "Dụng Thần động hóa ra hào cùng hành nhưng lùi (VD: Mão→Dần)",
        "ket_luan": "HUNG — Thoái lui, suy giảm, mất mát", "muc_do": "HUNG"
    },
    {
        "id": "R12", "ten": "Hóa Hồi Đầu Khắc",
        "dk": "Dụng Thần động hóa ra hào khắc chính nó",
        "ket_luan": "ĐẠI HUNG — Tự làm hại mình, hành động phản tác dụng", "muc_do": "ĐẠI HUNG"
    },
    # === NHÓM 4: THẾ ỨNG - LỤC XUNG/HỢP ===
    {
        "id": "R13", "ten": "Thế Vượng Ứng Suy",
        "dk": "Hào Thế vượng, hào Ứng suy",
        "ket_luan": "Ta mạnh người yếu — Chủ động, có lợi thế", "muc_do": "CÁT"
    },
    {
        "id": "R14", "ten": "Ứng Khắc Thế",
        "dk": "Hào Ứng khắc hào Thế",
        "ket_luan": "Đối phương bất lợi cho ta — Cẩn thận kẻ thù, đối thủ", "muc_do": "HUNG"
    },
    {
        "id": "R15", "ten": "Lục Hợp Quái",
        "dk": "Quẻ thuộc loại Lục Hợp (6 hào hợp nhau)",
        "ket_luan": "Hòa hợp, thuận lợi, mọi việc suôn sẻ", "muc_do": "CÁT"
    },
    {
        "id": "R16", "ten": "Lục Xung Quái",
        "dk": "Quẻ thuộc loại Lục Xung (6 hào xung nhau)",
        "ket_luan": "Xung đột, tan rã, không bền vững", "muc_do": "HUNG"
    },
    # === NHÓM 5: ỨNG KỲ ===
    {
        "id": "R17", "ten": "Ứng Kỳ Vượng",
        "dk": "Dụng Thần vượng",
        "ket_luan": "Ứng vào ngày xung Dụng Thần Chi (xung phá = phát động)", "muc_do": "THAM_KHẢO"
    },
    {
        "id": "R18", "ten": "Ứng Kỳ Suy",
        "dk": "Dụng Thần suy",
        "ket_luan": "Ứng vào ngày sinh Dụng Thần hoặc ngày hợp Dụng Thần", "muc_do": "THAM_KHẢO"
    },
]

# ======================================================================
# 4. LỤC THẦN (Lục Thú) — Ý NGHĨA CHI TIẾT
# ======================================================================
LUC_THAN_Y_NGHIA = {
    "Thanh Long": {
        "hanh": "Mộc", "tinh_chat": "CÁT",
        "y_nghia": "Vui mừng, qúy nhân, rượu tiệc, tài lộc. Tin tốt, may mắn",
        "benh": "Gan, nghiện rượu", "nguoi": "Quý nhân, người giàu sang"
    },
    "Chu Tước": {
        "hanh": "Hỏa", "tinh_chat": "HUNG",
        "y_nghia": "Kiện tụng, thị phi, văn thư, tin tức. Cãi vã, tranh chấp",
        "benh": "Mắt, tim, miệng lưỡi", "nguoi": "Người hay nói, luật sư"
    },
    "Câu Trần": {
        "hanh": "Thổ", "tinh_chat": "HUNG",
        "y_nghia": "Chậm trễ, trì trệ, đất đai, nhà cửa. Ruộng đất, công chức",
        "benh": "Dạ dày, bụng", "nguoi": "Nông dân, công chức, quân nhân"
    },
    "Đằng Xà": {
        "hanh": "Hỏa", "tinh_chat": "HUNG",
        "y_nghia": "Lo lắng, ác mộng, quái dị, qủy quái. Sợ hãi, bất an",
        "benh": "Tim, thần kinh, ác mộng", "nguoi": "Phụ nữ xấu, kẻ lừa đảo"
    },
    "Bạch Hổ": {
        "hanh": "Kim", "tinh_chat": "ĐẠI HUNG",
        "y_nghia": "Tang tóc, bệnh tật, tai nạn, máu me. Hung hiểm, đau đớn",
        "benh": "Phổi, xương, máu, phẫu thuật", "nguoi": "Bác sĩ, quân nhân, người hung dữ"
    },
    "Huyền Vũ": {
        "hanh": "Thủy", "tinh_chat": "HUNG",
        "y_nghia": "Trộm cắp, lừa đảo, mất mát, bí mật. Mờ ám, không rõ ràng",
        "benh": "Thận, sinh dục, nghiện ngập", "nguoi": "Kẻ trộm, người lừa đảo, gián điệp"
    },
}

# ======================================================================
# 5. KỲ MÔN CÁCH CỤC — 20+ MẪU PHỔ BIẾN
# ======================================================================
KY_MON_CACH_CUC = {
    # === ĐẠI CÁT ===
    "Thiên Độn": {
        "dk": "Bính + Thiên Tâm hoặc Bính + Khai Môn tại cùng cung",
        "luan": "ĐẠI CÁT — Trời che chở, mưu sự thành công, bách chiến bách thắng",
        "muc_do": "ĐẠI CÁT", "ung_dung": "Mưu sự lớn, xuất hành, kinh doanh"
    },
    "Địa Độn": {
        "dk": "Ất + Cửu Địa hoặc Ất + Khai Môn tại cùng cung",
        "luan": "CÁT — Đất nương tựa, ẩn nấp, bảo vệ. Lợi thủ bất lợi công",
        "muc_do": "CÁT", "ung_dung": "Phòng thủ, ẩn nấp, bảo toàn"
    },
    "Nhân Độn": {
        "dk": "Đinh + Thái Âm hoặc Đinh + Hưu Môn tại cùng cung",
        "luan": "CÁT — Được người giúp, quý nhân phò trợ, giao dịch thuận",
        "muc_do": "CÁT", "ung_dung": "Tìm quý nhân, hợp tác, xin việc"
    },
    "Thần Độn": {
        "dk": "Đinh + Cửu Thiên hoặc Bính + Cửu Thiên tại cùng cung",
        "luan": "ĐẠI CÁT — Thần linh che chở, mưu sự thần kỳ thành công",
        "muc_do": "ĐẠI CÁT", "ung_dung": "Cầu nguyện, mưu lược, siêu phàm"
    },
    "Quỷ Độn": {
        "dk": "Đinh + Đằng Xà tại cùng cung",
        "luan": "CÁT (đặc biệt) — Mưu lược cao siêu, bất ngờ, quỷ kế thành công",
        "muc_do": "CÁT", "ung_dung": "Mưu kế, bất ngờ, đánh úp"
    },
    "Phong Độn": {
        "dk": "Ất + Lục Hợp hoặc Tốn cung + Khai Môn",
        "luan": "CÁT — Gió thuận, đi lại thuận lợi, tin tức tốt",
        "muc_do": "CÁT", "ung_dung": "Xuất hành, giao tiếp, thương mại"
    },
    "Vân Độn": {
        "dk": "Ất + Cửu Thiên hoặc Ất + Trực Phù tại cùng cung",
        "luan": "CÁT — Mây che, ẩn núp tốt, mưu sự bí mật thành",
        "muc_do": "CÁT", "ung_dung": "Ẩn nấp, bí mật, tránh né"
    },
    "Long Độn": {
        "dk": "Ất + Lục Hợp + Thiên Phụ tại Tốn cung",
        "luan": "CÁT — Rồng xanh xuất hiện, đại cát đại lợi",
        "muc_do": "CÁT", "ung_dung": "Đại sự, khởi nghiệp"
    },
    "Hổ Độn": {
        "dk": "Bính + Bạch Hổ + Thiên Nhậm tại Cấn cung",
        "luan": "CÁT (đặc biệt) — Hổ trắng ẩn núi, binh quyền mạnh mẽ",
        "muc_do": "CÁT", "ung_dung": "Quân sự, quyền lực, tranh đấu"
    },
    # === HUNG ===
    "Phản Ngâm": {
        "dk": "Sao/Cửa lâm cung đối diện cung gốc (VD: gốc cung 1 → lâm cung 9)",
        "luan": "ĐẠI HUNG — Phản bội, phản trắc, sự việc đảo ngược hoàn toàn",
        "muc_do": "ĐẠI HUNG", "ung_dung": "Mọi việc đều nguy hiểm"
    },
    "Phục Ngâm": {
        "dk": "Sao/Cửa lâm đúng cung gốc (Thiên Bồng tại cung 1, Khai Môn tại cung 1)",
        "luan": "HUNG — Trì trệ, đình trệ, ủ rũ, không tiến được",
        "muc_do": "HUNG", "ung_dung": "Mọi việc đều chậm trễ"
    },
    "Ngũ Bất Ngộ Thời": {
        "dk": "Can Giờ khắc Can Ngày (cùng Âm/Dương). VD: Canh(Kim) khắc Giáp(Mộc), cùng Dương",
        "luan": "ĐẠI HUNG — Ngày xấu nhất, không nên làm gì quan trọng",
        "muc_do": "ĐẠI HUNG", "ung_dung": "Tuyệt đối tránh xuất hành, mưu sự"
    },
    "Thiên Cầm": {
        "dk": "Thiên Nhuế/Cầm nhập Trung cung (Cung 5)",
        "luan": "Đại CÁT hoặc Đại HUNG tùy tổ hợp — Cầm = trung tâm, chủ soái",
        "muc_do": "ĐẶC_BIỆT", "ung_dung": "Phụ thuộc vào Cửa + Thần đi kèm"
    },
    "Khai Môn + Thiên Tâm": {
        "dk": "Khai Môn + Thiên Tâm + Trực Phù tại cùng cung",
        "luan": "ĐẠI CÁT — Tam cát hội tụ, mưu sự bách phát bách trúng",
        "muc_do": "ĐẠI CÁT", "ung_dung": "Mưu lược, quyết định lớn, xuất hành"
    },
    "Tử Môn + Thiên Nhuế": {
        "dk": "Tử Môn + Thiên Nhuế tại cùng cung",
        "luan": "ĐẠI HUNG — Tử sát kết hợp, nguy hiểm tính mạng, bệnh nặng",
        "muc_do": "ĐẠI HUNG", "ung_dung": "Tuyệt đối tránh, có nguy cơ chết"
    },
    "Kinh Môn + Bạch Hổ": {
        "dk": "Kinh Môn + Thiên Trụ + Bạch Hổ tại cùng cung",
        "luan": "HUNG — Kinh sợ, tai nạn, hao tổn, kiện tụng",
        "muc_do": "HUNG", "ung_dung": "Cẩn thận tai nạn, tránh kiện tụng"
    },
}

# ======================================================================
# 6. SAO KỲ MÔN — Ý NGHĨA CHI TIẾT
# ======================================================================
SAO_KY_MON = {
    "Thiên Bồng": {"cung_goc": 1, "hanh": "Thủy", "loai": "ĐẠI HUNG", "y_nghia": "Trộm cắp, gian tà, mưu hại. Lợi cho quân sự, bất lợi cho dân sự"},
    "Thiên Nhuế": {"cung_goc": 2, "hanh": "Thổ", "loai": "HUNG", "y_nghia": "Bệnh tật, tranh chấp, kiện tụng. Lợi cho phòng thủ"},
    "Thiên Xung": {"cung_goc": 3, "hanh": "Mộc", "loai": "CÁT HUNG NỬA", "y_nghia": "Xung đột, hành động, quyết đoán. Can đảm nhưng manh động"},
    "Thiên Phụ": {"cung_goc": 4, "hanh": "Mộc", "loai": "CÁT", "y_nghia": "Văn hóa, giáo dục, trí tuệ. Lợi cho học hành, thi cử"},
    "Thiên Cầm": {"cung_goc": 5, "hanh": "Thổ", "loai": "ĐẠI CÁT", "y_nghia": "Trung tâm, chủ soái, quyết định. Lợi cho mưu lược lớn"},
    "Thiên Tâm": {"cung_goc": 6, "hanh": "Kim", "loai": "ĐẠI CÁT", "y_nghia": "Mưu lược, y học, quý nhân. Lợi cho mọi việc, đặc biệt y cùng mưu"},
    "Thiên Trụ": {"cung_goc": 7, "hanh": "Kim", "loai": "HUNG", "y_nghia": "Phá hoại, gian trá, phản bội. Lợi cho phá hủy bất lợi cho xây dựng"},
    "Thiên Nhậm": {"cung_goc": 8, "hanh": "Thổ", "loai": "CÁT", "y_nghia": "Nhân từ, đạo đức, nuôi dưỡng. Lợi cho giáo dục, từ thiện"},
    "Thiên Anh": {"cung_goc": 9, "hanh": "Hỏa", "loai": "CÁT HUNG NỬA", "y_nghia": "Sáng suốt, văn minh, lễ nghĩa. Lợi cho văn hóa, bất lợi cho quân sự"},
}

CUA_KY_MON = {
    "Khai Môn": {"cung_goc": 6, "hanh": "Kim", "loai": "ĐẠI CÁT", "y_nghia": "Mở ra, khởi sự, nhậm chức, làm ăn. Cửa tốt nhất"},
    "Hưu Môn": {"cung_goc": 1, "hanh": "Thủy", "loai": "CÁT", "y_nghia": "Nghỉ ngơi, gặp quý nhân, cầu tài. Bình yên, vui vẻ"},
    "Sinh Môn": {"cung_goc": 8, "hanh": "Thổ", "loai": "ĐẠI CÁT", "y_nghia": "Sinh sôi, phát tài, lợi nhuận. Lợi cho kinh doanh, đầu tư"},
    "Thương Môn": {"cung_goc": 3, "hanh": "Mộc", "loai": "CÁT HUNG NỬA", "y_nghia": "Công đường, kiện tụng. Trung tính, lợi cho quan chức"},
    "Đỗ Môn": {"cung_goc": 4, "hanh": "Mộc", "loai": "CÁT HUNG NỬA", "y_nghia": "Bế tắc, ẩn nấp. Lợi cho trốn tránh, bất lợi cho xuất hành"},
    "Cảnh Môn": {"cung_goc": 9, "hanh": "Hỏa", "loai": "BÌNH", "y_nghia": "Phong cảnh, văn thư, thi cử. Lợi cho học hành, bất lợi cho kiện"},
    "Tử Môn": {"cung_goc": 2, "hanh": "Thổ", "loai": "ĐẠI HUNG", "y_nghia": "Chết chóc, tang thương, hình phạt. Cửa xấu nhất"},
    "Kinh Môn": {"cung_goc": 7, "hanh": "Kim", "loai": "HUNG", "y_nghia": "Kinh sợ, động đất, tai biến. Bất lợi cho mọi việc"},
}

THAN_KY_MON = {
    "Trực Phù": {"hanh": "Thổ", "loai": "ĐẠI CÁT", "y_nghia": "Quý nhân tối cao, thần che chở. Được bề trên giúp đỡ"},
    "Đằng Xà": {"hanh": "Hỏa", "loai": "HUNG", "y_nghia": "Lo lắng, ác mộng, quái dị. Sợ hãi, bất an, lừa dối"},
    "Thái Âm": {"hanh": "Kim", "loai": "CÁT", "y_nghia": "Phụ nữ, bí mật, che giấu. Lợi cho mưu kế ẩn"},
    "Lục Hợp": {"hanh": "Mộc", "loai": "CÁT", "y_nghia": "Hợp tác, hôn nhân, giao dịch. Đoàn kết, hòa hợp"},
    "Bạch Hổ": {"hanh": "Kim", "loai": "HUNG", "y_nghia": "Hung hiểm, bệnh tật, tang tóc. Cẩn thận tai nạn"},
    "Huyền Vũ": {"hanh": "Thủy", "loai": "HUNG", "y_nghia": "Trộm cắp, mất mát, mờ ám. Bất minh, nghi ngờ"},
    "Cửu Địa": {"hanh": "Thổ", "loai": "CÁT", "y_nghia": "Đất mẹ, bảo hộ, ẩn nấp. Lợi cho phòng thủ, không lợi cho tấn công"},
    "Cửu Thiên": {"hanh": "Kim", "loai": "CÁT", "y_nghia": "Trời cao, uy quyền, hành động. Lợi cho tấn công, mưu lược lớn"},
}

# ======================================================================
# 7. PHỤC THẦN / PHI THẦN — Khi Dụng Thần không hiện trong quẻ
# Nguồn: bocdich.com, kinhdichluchao.vn
# ======================================================================
PHUC_THAN_RULES = {
    "phuc_than_vuong": {
        "dk": "Phục Thần được Nhật/Nguyệt sinh hoặc được hào động sinh",
        "ket_luan": "CÁT — Phục Thần sắp xuất hiện, sự việc sẽ thành nhưng chậm",
        "muc_do": "CÁT"
    },
    "phuc_than_suy": {
        "dk": "Phục Thần bị khắc, hưu tù, không được trợ giúp",
        "ket_luan": "HUNG — Sự việc khó thành, Dụng Thần ẩn quá sâu",
        "muc_do": "HUNG"
    },
    "phi_than_sinh_phuc": {
        "dk": "Phi Thần (hào che Phục Thần) sinh Phục Thần",
        "ket_luan": "CÁT — Người chèn ép lại giúp đỡ, chuyện xấu hóa tốt",
        "muc_do": "CÁT"
    },
    "phi_than_khac_phuc": {
        "dk": "Phi Thần khắc Phục Thần",
        "ket_luan": "HUNG — Bị kẻ trên đè nén, sự việc bị chôn vùi",
        "muc_do": "ĐẠI HUNG"
    },
    "phi_than_khong_vong": {
        "dk": "Phi Thần lâm Không Vong hoặc bị Nguyệt Phá",
        "ket_luan": "CÁT — Lớp che bị phá, Phục Thần tự xuất hiện",
        "muc_do": "CÁT"
    },
}

# ======================================================================
# 8. NHẬT THẦN / NGUYỆT THẦN — Quy tắc ảnh hưởng
# Nguồn: votranh.com, kinhdichluchao.vn
# ======================================================================
NHAT_NGUYET_RULES = [
    {
        "id": "NN01", "ten": "Nhật Thần Sinh Dụng Thần",
        "dk": "Ngũ Hành ngày sinh Dụng Thần",
        "ket_luan": "CÁT — Được ngày hỗ trợ, sự việc thuận lợi trong ngày",
        "muc_do": "CÁT"
    },
    {
        "id": "NN02", "ten": "Nhật Thần Khắc Dụng Thần",
        "dk": "Ngũ Hành ngày khắc Dụng Thần",
        "ket_luan": "HUNG — Ngày bất lợi, gặp trở ngại trong ngày",
        "muc_do": "HUNG"
    },
    {
        "id": "NN03", "ten": "Nguyệt Thần Sinh Dụng Thần",
        "dk": "Ngũ Hành tháng sinh Dụng Thần",
        "ket_luan": "ĐẠI CÁT — VƯỢNG nhất: được tháng sinh = sức mạnh cả tháng",
        "muc_do": "ĐẠI CÁT"
    },
    {
        "id": "NN04", "ten": "Nguyệt Thần Khắc Dụng Thần (Nguyệt Phá)",
        "dk": "Chi tháng xung Chi Dụng Thần",
        "ket_luan": "ĐẠI HUNG — Nguyệt Phá = tan vỡ, hư hại cả tháng",
        "muc_do": "ĐẠI HUNG"
    },
    {
        "id": "NN05", "ten": "Nhật Nguyệt Đồng Sinh",
        "dk": "Cả ngày lẫn tháng đều sinh Dụng Thần",
        "ket_luan": "ĐẠI CÁT — Cực vượng, bách chiến bách thắng",
        "muc_do": "ĐẠI CÁT"
    },
    {
        "id": "NN06", "ten": "Nhật Nguyệt Đồng Khắc",
        "dk": "Cả ngày lẫn tháng đều khắc Dụng Thần",
        "ket_luan": "ĐẠI HUNG — Cực suy, không còn cứu vãn",
        "muc_do": "ĐẠI HUNG"
    },
    {
        "id": "NN07", "ten": "Nhật Hợp Dụng Thần",
        "dk": "Chi ngày hợp (Lục Hợp) Chi Dụng Thần",
        "ket_luan": "CÁT — Bị giữ lại (hợp = ràng buộc), chờ ngày xung để phát",
        "muc_do": "BÌNH"
    },
    {
        "id": "NN08", "ten": "Nhật Xung Dụng Thần (Ám Động)",
        "dk": "Chi ngày xung Chi Dụng Thần (Dụng Thần tĩnh)",
        "ket_luan": "Ám Động — Hào tĩnh bị ngày xung = tự động, sự việc bất ngờ xảy ra",
        "muc_do": "ĐẶC_BIỆT"
    },
]

# ======================================================================
# 9. KỲ MÔN CÁCH CỤC MỞ RỘNG — Thêm 10+ patterns
# ======================================================================
KY_MON_CACH_CUC_MR = {
    # === CÁT CỤC ===
    "Tam Kỳ Đắc Sử": {
        "dk": "Ất/Bính/Đinh + Cửa Cát (Khai/Hưu/Sinh) tại cùng cung",
        "luan": "ĐẠI CÁT — Tam Kỳ gặp Cửa Cát, mưu sự tất thành, quý nhân phù trợ",
        "muc_do": "ĐẠI CÁT", "ung_dung": "Mọi việc đều rất tốt"
    },
    "Ngọc Nữ Thủ Môn": {
        "dk": "Đinh + Khai Môn tại cùng cung",
        "luan": "CÁT — Ngọc nữ giữ cửa, mưu sự kín đáo thành công",
        "muc_do": "CÁT", "ung_dung": "Mưu sự bí mật, tình cảm, đàm phán"
    },
    "Thiên Mã Lâm Môn": {
        "dk": "Thiên Xung + Khai Môn hoặc Sinh Môn tại cùng cung",
        "luan": "CÁT — Di chuyển nhanh, cơ hội đến bất ngờ",
        "muc_do": "CÁT", "ung_dung": "Xuất hành, thay đổi, di chuyển nhanh"
    },
    "Cửu Thiên Cao Phi": {
        "dk": "Cửu Thiên + Khai Môn + Bính/Đinh tại cùng cung",
        "luan": "ĐẠI CÁT — Bay cao bay xa, quyền uy mạnh mẽ, thăng tiến nhanh",
        "muc_do": "ĐẠI CÁT", "ung_dung": "Thăng tiến, mở rộng, xuất ngoại"
    },
    "Tam Cát Hội Cung": {
        "dk": "Sao Cát + Cửa Cát + Thần Cát tại cùng 1 cung",
        "luan": "ĐẠI CÁT — Thiên Địa Nhân tam tài tương hợp, cực kỳ tốt lành",
        "muc_do": "ĐẠI CÁT", "ung_dung": "Bách chiến bách thắng"
    },
    # === HUNG CỤC ===
    "Đại Cách (Canh+Canh)": {
        "dk": "Can Thiên Bàn = Canh + Can Địa Bàn = Canh (cùng cung)",
        "luan": "ĐẠI HUNG — Đại cách = tranh chấp kịch liệt, xung đột dữ dội",
        "muc_do": "ĐẠI HUNG", "ung_dung": "Kiện tụng, chiến tranh, xung đột"
    },
    "Thiên Lao (Hưu+Thiên Nhuế)": {
        "dk": "Hưu Môn + Thiên Nhuế tại cùng cung",
        "luan": "HUNG — Thiên Lao = bị giam giữ, ràng buộc, mất tự do",
        "muc_do": "HUNG", "ung_dung": "Bị kiểm soát, tù đày, nợ nần"
    },
    "Hình Cách (Canh+Kỷ)": {
        "dk": "Can Thiên Bàn = Canh + Can Địa Bàn = Kỷ (hoặc ngược lại)",
        "luan": "HUNG — Hình phạt, tai nạn, thương tích, kiện tụng",
        "muc_do": "HUNG", "ung_dung": "Kiện cáo, phạt, tai nạn"
    },
    "Bức Cách (Canh+Nhâm)": {
        "dk": "Can Thiên Bàn = Canh + Can Địa Bàn = Nhâm (hoặc ngược lại)",
        "luan": "HUNG — Bị ép buộc, không có lối thoát, áp lực lớn",
        "muc_do": "HUNG", "ung_dung": "Bị ép, nợ đòi, áp lực tứ bề"
    },
    "Phi Can Cách (Canh+Giáp)": {
        "dk": "Can Thiên Bàn = Canh + Can Địa Bàn = Giáp (hoặc ngược lại)",
        "luan": "ĐẠI HUNG — Phi Can = dao chém gỗ, tai họa, mất tài sản",
        "muc_do": "ĐẠI HUNG", "ung_dung": "Mất của, tai nạn, thua lỗ nặng"
    },
}

# ======================================================================
# 10. SAO + CỬA TỔ HỢP — Ý nghĩa khi Sao và Cửa gặp nhau
# Nguồn: phongthuynhattam.com, vuphac.com
# ======================================================================
SAO_CUA_TO_HOP = {
    # Key = (Sao, Cửa) → ý nghĩa
    # === THIÊN TÂM (Kim - ĐẠI CÁT) ===
    ("Thiên Tâm", "Khai Môn"): {"luan": "ĐẠI CÁT — Trí tuệ mở đường, mưu sự bách phát bách trúng", "ung_dung": "Khởi nghiệp, mưu lược lớn"},
    ("Thiên Tâm", "Hưu Môn"): {"luan": "CÁT — Quý nhân nghỉ ngơi, gặp bạn tốt, hưởng thụ", "ung_dung": "Giao tiếp, hòa giải"},
    ("Thiên Tâm", "Sinh Môn"): {"luan": "ĐẠI CÁT — Trí tuệ + Tài lộc, kinh doanh đạt lợi nhuận cao", "ung_dung": "Đầu tư, kinh doanh"},
    ("Thiên Tâm", "Tử Môn"): {"luan": "BÌNH — Trí tuệ bị giới hạn, cần cẩn thận sức khỏe", "ung_dung": "Khám bệnh, y tế"},
    # === THIÊN NHẬM (Thổ - CÁT) ===
    ("Thiên Nhậm", "Sinh Môn"): {"luan": "ĐẠI CÁT — Nhẫn nại + Tài lộc, đầu tư bất động sản cực tốt", "ung_dung": "Nhà đất, tích lũy"},
    ("Thiên Nhậm", "Khai Môn"): {"luan": "CÁT — Chậm mà chắc, khởi sự bền vững", "ung_dung": "Khởi nghiệp kiên nhẫn"},
    ("Thiên Nhậm", "Hưu Môn"): {"luan": "CÁT — Nghỉ ngơi bình an, không lo lắng", "ung_dung": "Dưỡng sức, phục hồi"},
    # === THIÊN PHỤ (Mộc - CÁT) ===
    ("Thiên Phụ", "Khai Môn"): {"luan": "CÁT — Văn chương mở đường, thi cử đỗ đạt", "ung_dung": "Thi cử, học tập"},
    ("Thiên Phụ", "Cảnh Môn"): {"luan": "CÁT — Văn học gặp tin tốt, giấy tờ thuận lợi", "ung_dung": "Giấy tờ, hợp đồng"},
    ("Thiên Phụ", "Sinh Môn"): {"luan": "CÁT — Tri thức sinh tài, kinh doanh giáo dục tốt", "ung_dung": "Giáo dục, sách vở"},
    # === THIÊN XUNG (Mộc - CÁT HUNG NỬA) ===
    ("Thiên Xung", "Khai Môn"): {"luan": "CÁT — Hành động mạnh mẽ, khởi sự nhanh chóng", "ung_dung": "Khởi nghiệp nhanh"},
    ("Thiên Xung", "Thương Môn"): {"luan": "HUNG — Xung đột + Tranh cãi, kiện tụng kéo dài", "ung_dung": "Tránh tranh chấp"},
    ("Thiên Xung", "Kinh Môn"): {"luan": "HUNG — Động thái gây sợ hãi, tai nạn di chuyển", "ung_dung": "Cẩn thận lái xe"},
    # === THIÊN BỒNG (Thủy - ĐẠI HUNG) ===
    ("Thiên Bồng", "Tử Môn"): {"luan": "ĐẠI HUNG — Hung + Chết = nguy hiểm tính mạng", "ung_dung": "Tuyệt đối tránh"},
    ("Thiên Bồng", "Khai Môn"): {"luan": "BÌNH — Hung tinh gặp Cửa Cát, hung hóa bình", "ung_dung": "Cẩn thận nhưng có cơ hội"},
    ("Thiên Bồng", "Sinh Môn"): {"luan": "BÌNH — Mưu kế sinh tài, nhưng cách thức không chính đáng", "ung_dung": "Cẩn thận pháp luật"},
    # === THIÊN NHUẾ (Thổ - HUNG) ===
    ("Thiên Nhuế", "Tử Môn"): {"luan": "ĐẠI HUNG — Bệnh tật + Chết = rất nguy hiểm, bệnh nặng", "ung_dung": "Khẩn cấp chữa trị"},
    ("Thiên Nhuế", "Sinh Môn"): {"luan": "BÌNH — Bệnh + Sinh = bệnh khỏi, hồi phục", "ung_dung": "Chữa bệnh thành công"},
    ("Thiên Nhuế", "Kinh Môn"): {"luan": "HUNG — Bệnh + Kinh sợ = hoảng loạn, phẫu thuật", "ung_dung": "Cẩn thận phẫu thuật"},
    # === THIÊN TRỤ (Kim - HUNG) ===
    ("Thiên Trụ", "Tử Môn"): {"luan": "ĐẠI HUNG — Phá hoại + Chết = cực kỳ nguy hiểm", "ung_dung": "Tránh mọi hoạt động"},
    ("Thiên Trụ", "Khai Môn"): {"luan": "BÌNH — Phá hoại + Mở = phá để xây mới, cải cách", "ung_dung": "Phá cũ xây mới"},
    ("Thiên Trụ", "Kinh Môn"): {"luan": "HUNG — Phá hoại + Kinh sợ = thiên tai, trộm cướp", "ung_dung": "Phòng chống thiên tai"},
    # === THIÊN ANH (Hỏa - CÁT HUNG NỬA) ===
    ("Thiên Anh", "Cảnh Môn"): {"luan": "CÁT — Sáng + Cảnh = danh tiếng lẫy lừng", "ung_dung": "Quảng cáo, truyền thông"},
    ("Thiên Anh", "Tử Môn"): {"luan": "HUNG — Lửa + Chết = hỏa hoạn, tai nạn lửa", "ung_dung": "Phòng cháy chữa cháy"},
    ("Thiên Anh", "Khai Môn"): {"luan": "CÁT — Danh tiếng mở đường, nổi tiếng nhanh", "ung_dung": "Marketing, quảng bá"},
}

# ======================================================================
# 11. BẢN CUNG 8 CUNG — Quẻ thuộc cung nào + Ngũ Hành cung
# Nguồn: kinhdichluchao.vn
# ======================================================================
BAN_CUNG = {
    "Càn": {"hanh": "Kim", "que_list": ["Thuần Càn", "Thiên Phong Cấu", "Thiên Sơn Độn", "Thiên Địa Bĩ", "Phong Địa Quan", "Sơn Địa Bác", "Hỏa Địa Tấn", "Hỏa Thiên Đại Hữu"]},
    "Khảm": {"hanh": "Thủy", "que_list": ["Thuần Khảm", "Thủy Trạch Tiết", "Thủy Lôi Truân", "Thủy Hỏa Ký Tế", "Trạch Hỏa Cách", "Lôi Hỏa Phong", "Địa Hỏa Minh Di", "Địa Thủy Sư"]},
    "Cấn": {"hanh": "Thổ", "que_list": ["Thuần Cấn", "Sơn Hỏa Bí", "Sơn Thiên Đại Súc", "Sơn Trạch Tổn", "Hỏa Trạch Khuê", "Thiên Trạch Lý", "Phong Trạch Trung Phu", "Phong Sơn Tiệm"]},
    "Chấn": {"hanh": "Mộc", "que_list": ["Thuần Chấn", "Lôi Địa Dự", "Lôi Thủy Giải", "Lôi Phong Hằng", "Địa Phong Thăng", "Thủy Phong Tỉnh", "Trạch Phong Đại Quá", "Trạch Lôi Tùy"]},
    "Tốn": {"hanh": "Mộc", "que_list": ["Thuần Tốn", "Phong Thiên Tiểu Súc", "Phong Hỏa Gia Nhân", "Phong Lôi Ích", "Thiên Lôi Vô Vọng", "Hỏa Lôi Phệ Hạp", "Sơn Lôi Di", "Sơn Phong Cổ"]},
    "Ly": {"hanh": "Hỏa", "que_list": ["Thuần Ly", "Hỏa Sơn Lữ", "Hỏa Phong Đỉnh", "Hỏa Thủy Vị Tế", "Sơn Thủy Mông", "Phong Thủy Hoán", "Thiên Thủy Tụng", "Thiên Hỏa Đồng Nhân"]},
    "Khôn": {"hanh": "Thổ", "que_list": ["Thuần Khôn", "Địa Lôi Phục", "Địa Trạch Lâm", "Địa Thiên Thái", "Lôi Thiên Đại Tráng", "Trạch Thiên Quải", "Thủy Thiên Nhu", "Thủy Địa Tỷ"]},
    "Đoài": {"hanh": "Kim", "que_list": ["Thuần Đoài", "Trạch Thủy Khốn", "Trạch Địa Tụy", "Trạch Sơn Hàm", "Thủy Sơn Kiển", "Địa Sơn Khiêm", "Lôi Sơn Tiểu Quá", "Lôi Trạch Quy Muội"]},
}

# Hàm helper: tra Bản Cung của 1 quẻ
def tra_ban_cung(ten_que):
    """Trả về (tên cung, hành cung) từ tên quẻ"""
    for cung, info in BAN_CUNG.items():
        if ten_que in info["que_list"]:
            return cung, info["hanh"]
    return None, None

# ======================================================================
# 12. HÀO BIẾN QUY TẮC — Dụng Thần hóa ra hào nào
# Nguồn: bocdich.com, kinhdichluchao.vn
# ======================================================================
HAO_BIEN_RULES = [
    {
        "id": "HB01", "ten": "Hóa Hồi Đầu Sinh",
        "dk": "Dụng Thần động hóa ra hào SINH chính nó (VD: Mộc hóa Thủy)",
        "ket_luan": "ĐẠI CÁT — Tự có lực hỗ trợ, sự việc tự thuận lợi",
        "muc_do": "ĐẠI CÁT"
    },
    {
        "id": "HB02", "ten": "Hóa Hợp",
        "dk": "Dụng Thần động hóa ra hào Lục Hợp với chính nó (VD: Tý hóa Sửu)",
        "ket_luan": "BÌNH — Bị hợp giữ lại, sự việc bị ràng buộc, chờ xung để giải",
        "muc_do": "BÌNH"
    },
    {
        "id": "HB03", "ten": "Hóa Không Vong",
        "dk": "Dụng Thần động hóa ra hào lâm Tuần Không",
        "ket_luan": "HUNG — Hóa ra hư không, sự việc thành rồi lại mất",
        "muc_do": "HUNG"
    },
    {
        "id": "HB04", "ten": "Hóa Mộ",
        "dk": "Dụng Thần động hóa ra hào Mộ Khố của chính nó (VD: Mộc hóa Mùi)",
        "ket_luan": "HUNG — Bị nhốt, giam giữ, sự việc bế tắc không lối thoát",
        "muc_do": "HUNG"
    },
    {
        "id": "HB05", "ten": "Hóa Tuyệt",
        "dk": "Dụng Thần động hóa ra hào Tuyệt của chính nó",
        "ket_luan": "ĐẠI HUNG — Tuyệt đường, sự việc hoàn toàn thất bại",
        "muc_do": "ĐẠI HUNG"
    },
]

# ======================================================================
# 13. ĐỘNG TĨNH QUY TẮC — Số hào động trong quẻ
# Nguồn: kinhdichluchao.vn
# ======================================================================
DONG_TINH_RULES = [
    {
        "id": "DT01", "ten": "Độc Phát (1 hào động)",
        "dk": "Quẻ chỉ có DUY NHẤT 1 hào động",
        "ket_luan": "Hào động là trọng tâm — Xem hào đó sinh/khắc Dụng Thần để luận",
        "muc_do": "THAM_KHẢO"
    },
    {
        "id": "DT02", "ten": "Loạn Động (5-6 hào động)",
        "dk": "Quẻ có 5 hoặc 6 hào đều động",
        "ket_luan": "HUNG — Quá nhiều biến động, sự việc hỗn loạn, khó kiểm soát. Xem hào TĨNH để luận",
        "muc_do": "HUNG"
    },
    {
        "id": "DT03", "ten": "Toàn Tĩnh (0 hào động)",
        "dk": "Quẻ không có hào nào động",
        "ket_luan": "BÌNH — Sự việc yên ắng, chưa có biến chuyển. Chờ Nhật/Nguyệt xung để ám động",
        "muc_do": "BÌNH"
    },
]

# ======================================================================
# 14. THIÊN CẦM SAO + CỬA TỔ HỢP BỔ SUNG
# ======================================================================
SAO_CUA_TO_HOP_BS = {
    ("Thiên Cầm", "Khai Môn"): {"luan": "ĐẠI CÁT — Chủ soái mở đường, quyết sách đúng đắn, lãnh đạo tài ba", "ung_dung": "Quyết định lớn, lãnh đạo"},
    ("Thiên Cầm", "Sinh Môn"): {"luan": "CÁT — Trung tâm sinh tài, kinh doanh bền vững, nền tảng vững chắc", "ung_dung": "Đầu tư dài hạn"},
    ("Thiên Cầm", "Tử Môn"): {"luan": "ĐẠI HUNG — Trung tâm gặp tử, tình thế nguy cấp, cần thay đổi chiến lược", "ung_dung": "Tránh quyết định lớn"},
    ("Thiên Cầm", "Hưu Môn"): {"luan": "CÁT — Trung tâm nghỉ ngơi, thời điểm tĩnh lặng để tích lũy sức mạnh", "ung_dung": "Dưỡng sức, chờ thời"},
}

# ======================================================================
# 15. THẬP CAN KHẮC ỨNG — 81 tổ hợp Thiên Can × Địa Bàn Can
# Nguồn: Lưu Bá Ôn — Kỳ Môn Độn Giáp Phần 1 (DOCX)
# ======================================================================
THAP_CAN_KHAC_UNG = {
    # === MẬU (Thiên Bàn) × 9 Can Địa Bàn ===
    "Mậu+Mậu": {"ten": "Phục Ngâm", "cat_hung": "BÌNH", "luan": "Ẩn náu, bình tĩnh chờ thời sẽ cát lợi. Phàm sự nên thủ, không nên động"},
    "Mậu+Ất": {"ten": "Thanh Long Hợp Linh", "cat_hung": "CÁT/HUNG", "luan": "Cửa cát sự cát, cửa xấu sự hung. Mọi việc tùy thuộc cửa đi kèm"},
    "Mậu+Bính": {"ten": "Thanh Long Phản Thủ", "cat_hung": "ĐẠI CÁT", "luan": "Yết kiến quý nhân, cầu công danh đại cát. Gặp mộ bức thì thị phi"},
    "Mậu+Đinh": {"ten": "Thanh Long Điệu Minh", "cat_hung": "CÁT", "luan": "Yết quý cầu danh cát lợi. Gặp mộ bức thì chiêu thị phi"},
    "Mậu+Kỷ": {"ten": "Quý Nhân Nhập Ngục", "cat_hung": "HUNG", "luan": "Công tư giai bất lợi. Dù việc công hay tư đều không cát lợi"},
    "Mậu+Canh": {"ten": "Trực Phù Phi Cung", "cat_hung": "ĐẠI HUNG", "luan": "Việc tốt chuyển thành xấu, việc xấu càng thêm hung hiểm"},
    "Mậu+Tân": {"ten": "Thanh Long Chiết Túc", "cat_hung": "CÁT/HUNG", "luan": "Cửa cát được người giúp đỡ. Cửa xấu mất tiền tài, tai họa, tật chân"},
    "Mậu+Nhâm": {"ten": "Thanh Long Nhập Thiên Lao", "cat_hung": "HUNG", "luan": "Bất lợi cho cả nam nữ trong nhà. Âm dương giai bất cát"},
    "Mậu+Quý": {"ten": "Thanh Long Hoa Cái", "cat_hung": "CÁT/HUNG", "luan": "Cách tốt tăng phúc vận. Cửa xấu ẩn chứa nhiều hung họa"},

    # === ẤT (Thiên Bàn) × 9 Can Địa Bàn ===
    "Ất+Mậu": {"ten": "Lợi Âm Hại Dương", "cat_hung": "HUNG", "luan": "Gặp cửa xấu áp chế, phá tài, thương tổn người trong nhà"},
    "Ất+Ất": {"ten": "Nhật Kỳ Phục Ngâm", "cat_hung": "HUNG", "luan": "Bất lợi yết kiến quý nhân, cầu công danh. Nên an phận thủ thường"},
    "Ất+Bính": {"ten": "Kỳ Nghi Thuận Toại", "cat_hung": "CÁT/HUNG", "luan": "Cát tinh thăng tiến. Hung tinh vợ chồng phân ly"},
    "Ất+Đinh": {"ten": "Kỳ Nghi Tương Tá", "cat_hung": "CÁT", "luan": "Mọi việc đều có thể tiến hành, đặc biệt lợi cho văn thư, thư tín"},
    "Ất+Kỷ": {"ten": "Nhật Kỳ Nhập Vũ", "cat_hung": "HUNG", "luan": "Tiền đồ mù mịt. Cửa xấu nhất định hung. Gặp Tam kỳ = Địa Độn"},
    "Ất+Canh": {"ten": "Nhật Kỳ Bị Hình", "cat_hung": "HUNG", "luan": "Thị phi, tiền tài tan nát, vợ chồng bất hòa, mang tư tình riêng"},
    "Ất+Tân": {"ten": "Thanh Long Đào Tẩu", "cat_hung": "HUNG", "luan": "Tiền tài bị kẻ dưới trộm mất, lục súc thương tổn"},
    "Ất+Nhâm": {"ten": "Nhật Kỳ Nhập Địa", "cat_hung": "HUNG", "luan": "Tôn ty đảo lộn, phát sinh quan tụng thị phi"},
    "Ất+Quý": {"ten": "Hoa Cái Phùng Tinh Quan", "cat_hung": "CÁT", "luan": "Lợi cho ẩn cư tu đạo, tránh nạn. Đội tích tu đạo, ẩn nặc"},

    # === BÍNH (Thiên Bàn) × 9 Can Địa Bàn ===
    "Bính+Mậu": {"ten": "Phi Điểu Diệt Huyệt", "cat_hung": "ĐẠI CÁT", "luan": "Mưu vi bách sự, mọi việc tốt lành. Chim bay về tổ"},
    "Bính+Ất": {"ten": "Nhật Nguyệt Tinh Hành", "cat_hung": "CÁT", "luan": "Dù việc công hay tư đều cát lợi"},
    "Bính+Bính": {"ten": "Nguyệt Kỳ Bội Sư", "cat_hung": "HUNG", "luan": "Thư tín công văn bức bách, tổn hao tiền tài"},
    "Bính+Đinh": {"ten": "Nguyệt Kỳ Chu Tước", "cat_hung": "CÁT", "luan": "Quý nhân văn thư cát lợi, cuộc sống yên ổn. Gặp Tam kỳ = Thiên Độn"},
    "Bính+Kỷ": {"ten": "Thái Bội Nhập Hình", "cat_hung": "HUNG", "luan": "Họa lao ngục, bị chỉ trích. Cửa cát muôn sự như ý, cửa xấu hung hiểm"},
    "Bính+Canh": {"ten": "Huỳnh Nhập Thái Bạch", "cat_hung": "HUNG", "luan": "Gia nghiệp phá bại, gặp trộm cướp, tiền tài tổn hao"},
    "Bính+Tân": {"ten": "Mưu Sự Tựu Thành", "cat_hung": "CÁT", "luan": "Mưu sự thành công, có lợi cho người bệnh"},
    "Bính+Nhâm": {"ten": "Hỏa Nhập Thiên La", "cat_hung": "HUNG", "luan": "Bất lợi cho khách, gặp nhiều thị phi"},
    "Bính+Quý": {"ten": "Hoa Cái Bội Sư", "cat_hung": "HUNG", "luan": "Âm nhân hại sự, tai họa tần sinh"},

    # === ĐINH (Thiên Bàn) × 9 Can Địa Bàn ===
    "Đinh+Mậu": {"ten": "Thanh Long Chuyển Quang", "cat_hung": "CÁT", "luan": "Quan nhân thăng chức, thường nhân uy thế. Cát lợi mọi việc"},
    "Đinh+Ất": {"ten": "Nhân Độn Cát Cách", "cat_hung": "CÁT", "luan": "Được thăng chức, gặp nhiều việc vui, phát tài"},
    "Đinh+Bính": {"ten": "Tinh Tùy Nguyệt Chuyển", "cat_hung": "CÁT/HUNG", "luan": "Được thăng chức cao nhưng bách tính phát sinh việc đầu hàng"},
    "Đinh+Đinh": {"ten": "Kỳ Nhập Thái Âm", "cat_hung": "CÁT", "luan": "Thư tín công văn đưa đến nhanh chóng, phát đạt"},
    "Đinh+Kỷ": {"ten": "Hỏa Nhập Câu Trần", "cat_hung": "HUNG", "luan": "Vì người phụ nữ mà sinh quan hệ mờ ám"},
    "Đinh+Canh": {"ten": "Nguyệt Nhất Thời Cách", "cat_hung": "HUNG", "luan": "Văn thư không được truyền đi, người ra ngoài nhất định sẽ về nhà"},
    "Đinh+Tân": {"ten": "Chu Tước Nhập Ngục", "cat_hung": "CÁT/HUNG", "luan": "Người có tội được thả. Nhưng người làm quan sẽ mất chức"},
    "Đinh+Nhâm": {"ten": "Ngũ Thần Hỗ Hợp", "cat_hung": "CÁT", "luan": "Quý nhân được ban thưởng, quan tụng được giải quyết công bằng hợp lý"},
    "Đinh+Quý": {"ten": "Chu Tước Đầu Giang", "cat_hung": "ĐẠI HUNG", "luan": "Liên lụy văn thư, mất văn kiện quan trọng, tranh chấp cãi cọ, thông tin không đến"},

    # === KỶ (Thiên Bàn) × 9 Can Địa Bàn ===
    "Kỷ+Mậu": {"ten": "Khuyển Ngộ Thanh Long", "cat_hung": "CÁT/HUNG", "luan": "Cửa cát mưu vọng toại ý, người địa vị cao gặp vui. Cửa xấu hung họa"},
    "Kỷ+Ất": {"ten": "Mộ Thần Bất Minh", "cat_hung": "HUNG", "luan": "Địa hộ gặp tinh, nên ẩn náu tháo chạy mới được cát lợi"},
    "Kỷ+Bính": {"ten": "Hỏa Bội Địa Hộ", "cat_hung": "HUNG", "luan": "Nam giới tương hại oan uổng. Người phụ nữ phát sinh việc dâm loạn"},
    "Kỷ+Đinh": {"ten": "Chu Tước Nhập Mộ", "cat_hung": "BÌNH", "luan": "Phát sinh kiện tụng, ban đầu oan khuất nhưng cuối cùng được hóa giải"},
    "Kỷ+Kỷ": {"ten": "Địa Hộ Phùng Quỷ", "cat_hung": "ĐẠI HUNG", "luan": "Người bệnh nhất định khó giữ tính mạng, mọi việc không như ý"},
    "Kỷ+Canh": {"ten": "Lợi Cách Phản Danh", "cat_hung": "HUNG", "luan": "Kiện tụng, người hành động trước bất lợi. Gặp sao âm có mưu hại"},
    "Kỷ+Tân": {"ten": "Du Hồn Nhập Mộ", "cat_hung": "HUNG", "luan": "Người địa vị cao gặp việc quái dị. Người thấp bị âm hồn quấy nhiễu"},
    "Kỷ+Nhâm": {"ten": "Địa Võng Cao Trương", "cat_hung": "HUNG", "luan": "Gặp họa sát thương. Mệnh nữ có gian tình"},
    "Kỷ+Quý": {"ten": "Địa Linh Huyền Vũ", "cat_hung": "ĐẠI HUNG", "luan": "Nam nữ mắc bệnh nguy hiểm tính mạng, kiện tụng, họa lao ngục"},

    # === CANH (Thiên Bàn) × 9 Can Địa Bàn ===
    "Canh+Mậu": {"ten": "Thái Bạch Thiên Ất Phục Cung", "cat_hung": "ĐẠI HUNG", "luan": "Mọi việc đều không nên làm, bách sự bất khả mưu"},
    "Canh+Ất": {"ten": "Thái Bạch Bổng Tinh", "cat_hung": "HUNG", "luan": "Nên cố thủ, kỵ xuất quân. Thoái cát tiến hung"},
    "Canh+Bính": {"ten": "Thái Bạch Nhập Huỳnh", "cat_hung": "HUNG", "luan": "Dễ gặp trộm cướp, là khách được lợi, là chủ tổn hao tiền tài"},
    "Canh+Đinh": {"ten": "Đình Đình Chỉ Cách", "cat_hung": "HUNG", "luan": "Vì tư tình nam nữ phát sinh kiện tụng. Gặp cửa cát có thể bổ cứu"},
    "Canh+Kỷ": {"ten": "Hình Cách", "cat_hung": "ĐẠI HUNG", "luan": "Phát sinh kiện tụng, hình phạt nặng nề"},
    "Canh+Canh": {"ten": "Thái Bạch Đồng Cung", "cat_hung": "ĐẠI HUNG", "luan": "Họa quan trường, tai họa bất ngờ, anh em không hợp nhau"},
    "Canh+Tân": {"ten": "Bạch Hổ Can Cách", "cat_hung": "ĐẠI HUNG", "luan": "Bất lợi đi xa, xe hỏng ngựa chết dọc đường"},
    "Canh+Nhâm": {"ten": "Thượng Cách", "cat_hung": "HUNG", "luan": "Đi xa lạc đường, thông tin sai lệch"},
    "Canh+Quý": {"ten": "Đại Cách", "cat_hung": "ĐẠI HUNG", "luan": "Phụ nữ sinh con mẹ con đều bị thương hại"},

    # === TÂN (Thiên Bàn) × 9 Can Địa Bàn ===
    "Tân+Mậu": {"ten": "Khốn Long Bị Thương", "cat_hung": "HUNG", "luan": "Kiện tụng gia nghiệp phá bại. Nên an phận thủ thường, manh động có tai họa"},
    "Tân+Ất": {"ten": "Bạch Hổ Xương Cuồng", "cat_hung": "ĐẠI HUNG", "luan": "Trong nhà thương vong, gia nghiệp phá bại, đi xa tai họa. Người lớn bất lợi, xe hỏng"},
    "Tân+Bính": {"ten": "Can Hợp Bội Sư", "cat_hung": "HUNG", "luan": "Cầu mưa không mưa, cầu nắng hạn. Vì tài sản gặp họa kiện tụng"},
    "Tân+Đinh": {"ten": "Ngục Thần Đắc Kỳ", "cat_hung": "CÁT", "luan": "Kinh doanh được nhiều lợi nhuận, người trong ngục được miễn tội phóng thích"},
    "Tân+Kỷ": {"ten": "Nhập Ngục Tự Hình", "cat_hung": "HUNG", "luan": "Người hầu phản bội chủ, kiện tụng không công bằng"},
    "Tân+Canh": {"ten": "Bạch Hổ Xuất Lực", "cat_hung": "HUNG", "luan": "Chủ khách tàn sát lẫn nhau. Biết khiêm nhường thì hòa giải"},
    "Tân+Tân": {"ten": "Phục Ngâm Thiên Đình", "cat_hung": "BÌNH", "luan": "Việc công thất bại, việc tư có thể thành. Kiện tụng tự gây ra tội danh"},
    "Tân+Nhâm": {"ten": "Hung Xà Nhập Ngục", "cat_hung": "HUNG", "luan": "Tranh chấp tình cảm, họa kiện tụng. Người hành động trước mắc tội"},
    "Tân+Quý": {"ten": "Thiên Lao Hoa Cái", "cat_hung": "HUNG", "luan": "Nhật nguyệt mất ánh sáng, lạc vào thiên võng, mọi việc không thuận lợi"},

    # === NHÂM (Thiên Bàn) × 9 Can Địa Bàn ===
    "Nhâm+Mậu": {"ten": "Tiểu Xà Hóa Long", "cat_hung": "CÁT", "luan": "Mệnh nam phát đạt tiến xa. Mệnh nữ sinh con"},
    "Nhâm+Ất": {"ten": "Tiểu Xà Nhật Kỳ", "cat_hung": "CÁT", "luan": "Mệnh nữ tính tình ôn hòa, mệnh nam hay than trách. Chiêm thai sinh con trai, tiền đồ sáng"},
    "Nhâm+Bính": {"ten": "Thủy Xà Nhập Hỏa", "cat_hung": "ĐẠI HUNG", "luan": "Kiện tụng thị phi gặp họa lao ngục, nhiều việc bất hạnh"},
    "Nhâm+Đinh": {"ten": "Can Hợp Xà Hình", "cat_hung": "CÁT/HUNG", "luan": "Bị liên lụy vì thư tín công văn, quý nhân vội vàng. Nam cát, nữ hung"},
    "Nhâm+Kỷ": {"ten": "Hung Xà Nhập Mộ", "cat_hung": "ĐẠI HUNG", "luan": "Tai họa nguy hiểm. Nên an phận thủ thường, kiện tụng đuối lý mắc tội"},
    "Nhâm+Canh": {"ten": "Thái Bạch Cầm Xà", "cat_hung": "BÌNH", "luan": "Kiện tụng phát sinh nhưng cuối cùng được giải quyết công bằng"},
    "Nhâm+Tân": {"ten": "Đằng Xà Tương Triền", "cat_hung": "HUNG", "luan": "Dù được cửa cát cũng không bình an, dễ bị lừa gạt"},
    "Nhâm+Nhâm": {"ten": "Xà Nhập Địa La", "cat_hung": "HUNG", "luan": "Ảnh hưởng bên ngoài lâm hoàn cảnh khốn khó, nội bộ mâu thuẫn. Cát tinh cửa cát tránh nạn"},
    "Nhâm+Quý": {"ten": "Ấu Nữ Gian Dâm", "cat_hung": "HUNG", "luan": "Trong nhà nhiều tiếng xấu. Cửa tốt sao xấu từ hung chuyển cát, tăng phúc"},

    # === QUÝ (Thiên Bàn) × 9 Can Địa Bàn ===
    "Quý+Mậu": {"ten": "Thiên Ất Hội Hợp", "cat_hung": "CÁT", "luan": "Tài vận thịnh vượng, nhiều việc vui. Được sự giúp đỡ gặt hái thành công. Cửa xấu bức chế thì họa kiện tụng"},
    "Quý+Ất": {"ten": "Hoa Cái Bồng Tinh", "cat_hung": "CÁT", "luan": "Quý nhân được lộc vị, bách tính cuộc sống ổn định"},
    "Quý+Bính": {"ten": "Hoa Cái Bội Sư (Quý)", "cat_hung": "CÁT", "luan": "Dù mệnh sang hèn, có vận mệnh tốt sẽ liên tiếp gặp việc vui"},
    "Quý+Đinh": {"ten": "Đằng Xà Yêu Kiều", "cat_hung": "HUNG", "luan": "Vì thư tín công văn dẫn đến họa kiện tụng, hỏa hoạn"},
    "Quý+Kỷ": {"ten": "Hoa Cái Địa Hộ", "cat_hung": "HUNG", "luan": "Dù nam hay nữ tin tức đều trở ngại, nên ẩn mình tránh nạn mới cát lợi"},
    "Quý+Canh": {"ten": "Thái Bạch Nhập Võng", "cat_hung": "BÌNH", "luan": "Kiện tụng phát sinh nhưng cương quyết tranh tụng cuối cùng hóa giải"},
    "Quý+Tân": {"ten": "Võng Cái Thiên Lao", "cat_hung": "ĐẠI HUNG", "luan": "Chiêm kiện tụng hay bệnh tật đều kết quả không tốt, nguy hiểm tính mạng"},
    "Quý+Nhâm": {"ten": "Phục Kiến Đằng Xà", "cat_hung": "HUNG", "luan": "Vợ chồng dễ phân ly tái hôn. Nữ xuất giá muộn khó có con, tuổi thọ không cao"},
    "Quý+Quý": {"ten": "Thiên Võng Tứ Trương", "cat_hung": "ĐẠI HUNG", "luan": "Bạn đồng hành lạc lối, bản thân bệnh hay kiện tụng đều bị thương hại"},
}

# ======================================================================
# 16. BÁT MÔN BAY CUNG — Trạng thái khi mỗi cửa bay đến từng cung
# Nguồn: Kỳ Môn Độn Giáp (1).docx (Cơ Bản)
# ======================================================================
BAT_MON_BAY_CUNG = {
    "Hưu Môn": {
        "cung_goc": 1, "hanh": "Thủy", "y_nghia": "Nghỉ ngơi, gia đình, quý nhân",
        "phuc_ngam": 1, "phan_ngam": 9,
        "nhap_mo": 4, "che": [2, 8], "buc": [9], "nghia": [6, 7], "tuong": [3],
        "note": "Hưu Môn Thủy cuộc (Thân-Tý-Thìn). Bay đến cung 4 nhập Mộ (Thìn)"
    },
    "Tử Môn": {
        "cung_goc": 2, "hanh": "Thổ", "y_nghia": "Chết chóc, mộ phần, sẹo vết thương không phai",
        "phuc_ngam": 2, "phan_ngam": 8,
        "nhap_mo": 4, "che": [3], "buc": [1], "nghia": [9], "tuong": [],
        "note": "Tử Môn Thổ Thủy đồng cung. Bay đến cung 4(Tốn) nhập Mộ"
    },
    "Thương Môn": {
        "cung_goc": 3, "hanh": "Mộc", "y_nghia": "Tổn thương, xe cộ, người bán hàng, lái xe giỏi",
        "phuc_ngam": 3, "phan_ngam": 7,
        "nhap_mo": 2, "che": [6], "buc": [8], "nghia": [1], "tuong": [4],
        "note": "Thương Môn Mộc cuộc (Hợi-Mão-Mùi). Bay đến cung 2 nhập Mộ"
    },
    "Đỗ Môn": {
        "cung_goc": 4, "hanh": "Mộc", "y_nghia": "Xây dựng, kỹ thuật, bảo mật, dừng lại",
        "phuc_ngam": 4, "phan_ngam": 6,
        "nhap_mo": 2, "che": [7], "buc": [8], "nghia": [1], "tuong": [3],
        "note": "Đỗ Môn Mộc. Bay đến cung 2 nhập Mộ"
    },
    "Cảnh Môn": {
        "cung_goc": 9, "hanh": "Hỏa", "y_nghia": "Du lịch, ăn uống, tranh thư pháp, giấy tờ",
        "phuc_ngam": 9, "phan_ngam": 1,
        "nhap_mo": 6, "che": [], "buc": [7], "nghia": [3, 4], "tuong": [],
        "note": "Cảnh Môn Hỏa. Bay đến cung 6(Càn) nhập Mộ"
    },
    "Khai Môn": {
        "cung_goc": 6, "hanh": "Kim", "y_nghia": "Công việc, sự nghiệp, công ty, khai mở",
        "phuc_ngam": 6, "phan_ngam": 4,
        "nhap_mo": 8, "che": [9], "buc": [3], "nghia": [2], "tuong": [],
        "note": "Khai Môn Kim cuộc (Tỵ-Dậu-Sửu). Bay đến cung 8(Cấn) nhập Mộ"
    },
    "Kinh Môn": {
        "cung_goc": 7, "hanh": "Kim", "y_nghia": "Thị phi, kiện tụng, kinh sợ, lo lắng",
        "phuc_ngam": 7, "phan_ngam": 3,
        "nhap_mo": 8, "che": [9], "buc": [4], "nghia": [2], "tuong": [],
        "note": "Kinh Môn Kim. Bay đến cung 8(Cấn) nhập Mộ"
    },
    "Sinh Môn": {
        "cung_goc": 8, "hanh": "Thổ", "y_nghia": "Lợi nhuận, nhà cửa, sinh sôi",
        "phuc_ngam": 8, "phan_ngam": 2,
        "nhap_mo": 4, "che": [3], "buc": [1], "nghia": [9], "tuong": [],
        "note": "Sinh Môn Thổ Thủy đồng cung. Bay đến cung 4(Tốn) nhập Mộ"
    },
}

# ======================================================================
# 17. CAN CHI TƯỢNG Ý — 10 Thiên Can tượng ý y học, hôn nhân, sự nghiệp
# Nguồn: Đế Vương Chi Thuật (Vương Phượng Lân) + Kỳ Môn Cơ Bản DOCX
# ======================================================================
CAN_CHI_TUONG_Y = {
    "Giáp": {
        "hanh": "Mộc Dương", "an_tang": "Mật", "co_the": "Đầu",
        "loai_tuong": "Thủ lĩnh, chủ soái, cao lớn. Không xuất hiện trong trận, ẩn trong Lục Nghi",
        "benh": "Mật, đầu", "tinh_cach": "Cương kiện, quyết đoán",
        "hon_nhan": "Không trực tiếp hiện, ẩn giấu", "mua": "Xuân", "phuong": "Đông"
    },
    "Ất": {
        "hanh": "Mộc Âm", "an_tang": "Gan", "co_the": "Cổ, Gáy, Tai",
        "loai_tuong": "Đông Y, người vợ. Nhật Kỳ trong Tam Kỳ",
        "benh": "Gan, cổ, gáy", "tinh_cach": "Ôn thuận, trầm tĩnh",
        "hon_nhan": "Ất = người vợ. Ất+Bính = vợ đang có bồ", "mua": "Xuân", "phuong": "Đông"
    },
    "Bính": {
        "hanh": "Hỏa Dương", "an_tang": "Ruột non", "co_the": "Trán, Máu me",
        "loai_tuong": "Người có quyền lực, lộn xộn cần kiểm soát. Nguyệt Kỳ trong Tam Kỳ",
        "benh": "Ruột non, trán, máu me", "tinh_cach": "Mạnh mẽ nóng nảy, phập phù không ổn định",
        "hon_nhan": "Bính = người đàn ông thứ 3 xen vào. Cấu trúc tốt thì đàng hoàng", "mua": "Hạ", "phuong": "Nam"
    },
    "Đinh": {
        "hanh": "Hỏa Âm", "an_tang": "Tim", "co_the": "Đầu, Lưỡi, Ngực, Mắt",
        "loai_tuong": "Ngọc nữ, con gái đẹp. Tinh Kỳ trong Tam Kỳ",
        "benh": "Tim, mắt, lưỡi", "tinh_cach": "Văn minh, lễ nghĩa",
        "hon_nhan": "Đinh = phụ nữ thứ 3 xen vào. Canh+Đinh = chồng có bồ", "mua": "Hạ", "phuong": "Nam"
    },
    "Mậu": {
        "hanh": "Thổ Dương", "an_tang": "Dạ dày (Bao tử)", "co_the": "Sườn hai bên hông",
        "loai_tuong": "Tài sản, tiền vốn, Thiên môn. Đại diện tư bản, tiền tài",
        "benh": "Dạ dày, sườn, mũi", "tinh_cach": "Mạnh mẽ, thần thái vững vàng",
        "hon_nhan": "Mậu = trung tâm, chủ của gia đình", "mua": "Tứ quý", "phuong": "Trung ương"
    },
    "Kỷ": {
        "hanh": "Thổ Âm", "an_tang": "Tỳ vị (Lá lách)", "co_the": "Bụng, Mặt",
        "loai_tuong": "Mộ phần, Địa hộ. Lòng tham, cái hố. Ôn thuận trầm tĩnh",
        "benh": "Lá lách, bụng", "tinh_cach": "Ôn thuận, trầm tĩnh, giáo hóa",
        "hon_nhan": "Kỷ = nền tảng, đất, phần mộ", "mua": "Tứ quý", "phuong": "Trung ương"
    },
    "Canh": {
        "hanh": "Kim Dương", "an_tang": "Đại tràng (Ruột già)", "co_the": "Rốn, Gần",
        "loai_tuong": "Đối thủ, kẻ thù, LLVT, công an. Cản trở, tắc nghẽn",
        "benh": "Đại tràng, ruột già. Có Canh có thể bị ung thư (tắc nghẽn khí huyết)",
        "tinh_cach": "Cương kiện, nhạy bén, độc đoán",
        "hon_nhan": "Canh = người chồng. Canh+Đinh = chồng có bồ", "mua": "Thu", "phuong": "Tây"
    },
    "Tân": {
        "hanh": "Kim Âm", "an_tang": "Phổi", "co_the": "Ngực, Đùi",
        "loai_tuong": "Phạm nhân, người có vấn đề. Sự việc sai lầm",
        "benh": "Phổi, ngực, đùi", "tinh_cach": "Trung thành thoải mái, đôn hậu rắn rỏi",
        "hon_nhan": "Tân = vấn đề, sai lầm trong quan hệ", "mua": "Thu", "phuong": "Tây"
    },
    "Nhâm": {
        "hanh": "Thủy Dương", "an_tang": "Bàng quang (Tam tiêu)", "co_the": "Bắp chân",
        "loai_tuong": "Sự di chuyển lưu động, nước, cạm bẫy, ngục tù, dòng chảy, hệ thống",
        "benh": "Bàng quang, tam tiêu", "tinh_cach": "Nhu hòa mà hiểm độc, khéo đưa đẩy hay thay đổi, thông minh",
        "hon_nhan": "Nhâm = di chuyển, thay đổi trong quan hệ", "mua": "Đông", "phuong": "Bắc"
    },
    "Quý": {
        "hanh": "Thủy Âm", "an_tang": "Thận (Tâm bào)", "co_the": "Bàn chân",
        "loai_tuong": "Tình dục, đời sống tình dục, người/sự vật liên quan tính dục",
        "benh": "Thận, tâm bào, bàn chân", "tinh_cach": "Từ rồng biến hóa, nhu nhược thiếu ý chí",
        "hon_nhan": "Quý = tình dục, đời sống riêng tư", "mua": "Đông", "phuong": "Bắc"
    },
}

# ======================================================================
# 18. THẬP NHỊ THẦN ỨNG NGHIỆM — 12 thần ứng nghiệm khi vào cửa
# Nguồn: Bí Cấp Toàn Thư (Trương Tử Phòng, NXB Khai Trí 1961), tr.18
# ======================================================================
THAP_NHI_THAN_UNG_NGHIEM = {
    "Thiên Ất": {
        "ung_nghiem": "Quý nhân xe ngựa. Người đi về mau. Trưởng giả mừng vui",
        "loai": "CÁT", "nguoi": "Quý nhân, trưởng giả"
    },
    "Đằng Xà": {
        "ung_nghiem": "Nửa đường quay lại. Quái lạ hoảng kinh. Gió mưa rập rình. Nghe kêu chim khách. Có người đuổi nhanh",
        "loai": "HUNG", "nguoi": "Kẻ đuổi theo, quái dị"
    },
    "Chu Tước": {
        "ung_nghiem": "Xa nghe tiếng trống. Vật sống trên đường. Lưu loát văn chương",
        "loai": "BÌNH", "nguoi": "Văn nhân, người làm văn thư"
    },
    "Lục Hợp": {
        "ung_nghiem": "Người ấm áo đẹp. Đường gặp ngựa xe. Thấy trẻ cười khoe",
        "loai": "CÁT", "nguoi": "Trẻ em, người sang trọng"
    },
    "Câu Trận": {
        "ung_nghiem": "Việc làm ngắc ngứ, chậm trễ đứt đoạn. Đường gặp đánh nhau. Mưu chẳng đến đâu",
        "loai": "HUNG", "nguoi": "Người gây sự, đánh nhau"
    },
    "Thanh Long": {
        "ung_nghiem": "Đường gặp Quan Sứ. Có triệu vui mừng. Áo gấm tưng bừng",
        "loai": "CÁT", "nguoi": "Quan sứ, quý nhân áo gấm"
    },
    "Thiên Không": {
        "ung_nghiem": "Dương thêm Âm bước. Vật hỏng trên đường. Cười nói huyênh hoang",
        "loai": "HUNG", "nguoi": "Kẻ khoác lác, vật hỏng"
    },
    "Bạch Hổ": {
        "ung_nghiem": "Cửa quan lo sợ. Thấy chết, nghe bi. Binh cách đường đi",
        "loai": "ĐẠI HUNG", "nguoi": "Quan binh, tang tóc"
    },
    "Thái Thường": {
        "ung_nghiem": "Phường tuồng con hát. Rượu thịt thấy đống. Tranh đẹp thần thông",
        "loai": "CÁT", "nguoi": "Nghệ sĩ, hát tuồng, ăn uống"
    },
    "Huyền Vũ": {
        "ung_nghiem": "Không là sư sãi thì trộm cắp, rơi lăn. Hoặc kẻ xin ăn",
        "loai": "HUNG", "nguoi": "Sư sãi, trộm cắp, kẻ ăn xin"
    },
    "Thái Âm": {
        "ung_nghiem": "Âm tư, hòa hợp. Cầu ít được nhiều. Âm nhạc cùng theo",
        "loai": "CÁT", "nguoi": "Người hòa hợp, âm nhạc"
    },
    "Thiên Hậu": {
        "ung_nghiem": "Đàn bà biếu vật. Trẻ nhỏ cười reo. Gái về nhà chồng",
        "loai": "CÁT", "nguoi": "Đàn bà, trẻ nhỏ, cô dâu"
    },
}

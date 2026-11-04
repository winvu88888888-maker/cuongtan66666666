
# QMDG DECODER - BỘ GIẢI MÃ CHI TIẾT
# Module này cung cấp dữ liệu tra cứu cực kỳ chi tiết cho các câu hỏi cụ thể.

def get_detailed_context(intent, palace_data):
    """
    Hàm chính để lấy thông tin giải mã dựa trên ý định và dữ liệu cung.
    """
    if not palace_data: return ""
    
    star = palace_data.get('star', '')
    door = palace_data.get('door', '')
    stem = palace_data.get('stem', '') # Thiên Can
    palace_num = palace_data.get('num', 0)
    
    context = []
    
    # 1. GIẢI MÃ BỆNH TẬT (Y TẾ & SỨC KHỎE)
    if intent in ["SICKNESS", "BENH_TAT", "HEALTH"]:
        context.append(decode_illness(star, stem, palace_num))

    # 2. GIẢI MÃ MẤT CỦA (TIM_DO, LOST_ITEM)
    elif intent in ["LOST_ITEM", "MAT_CUA", "TIM_DO"]:
        context.append(decode_lost_item(door, palace_num))
        context.append(decode_thief(star)) # Đặc điểm kẻ trộm

    # 3. GIẢI MÃ NGOẠI HÌNH / TÍNH CÁCH (PARTNER, LOVE)
    elif intent in ["PROFILE", "LOVE", "NGUOI_YEU", "DOI_TAC"]:
        context.append(decode_appearance(star))
        context.append(decode_character(door))

    # 4. GIẢI MÃ CON SỐ (GIÁ TIỀN, KHOẢNG CÁCH)
    # Luôn luôn cung cấp con số dự báo nếu có thể
    context.append(decode_numbers(palace_num, stem))
    
    # 5. GIẢI MÃ MÀU SẮC
    context.append(decode_color(star, stem))

    return "\n".join(context)

# --- A. BỆNH TẬT ---
def decode_illness(star, stem, palace_num):
    # Mapping Sao -> Bộ phận cơ thể / Loại bệnh
    star_map = {
        "Thiên Bồng": "Bệnh về thận, bàng quang, hệ bài tiết, máu huyết, tai.",
        "Thiên Nhu": "Bệnh về tỳ vị (dạ dày), tử cung, bụng, u bướu, ung thư (ác tính).",
        "Thiên Xung": "Bệnh về gan mật, chân tay, gân cốt, thần kinh, chấn thương đột ngột.",
        "Thiên Phụ": "Bệnh về gan, đùi, hông, phong thấp, trúng gió.",
        "Thiên Anh": "Bệnh về tim mạch, mắt, đầu, máu nóng, sốt cao.",
        "Thiên Nhậm": "Bệnh về tỳ, mũi, lưng, cột sống, béo phì, bệnh mãn tính.",
        "Thiên Trụ": "Bệnh về phổi, phế quản, miệng, răng, họng, xương khớp, gãy xương.",
        "Thiên Tâm": "Bệnh về phổi, đầu, xương, người già, hoặc là bác sĩ/thuốc (Cát).",
        "Thiên Cầm": "Bệnh ở tỳ vị, trung khu thần kinh."
    }
    
    # Mapping Cung -> Vị trí trên cơ thể
    palace_body_map = {
        1: "Thận, tai, máu, bộ phận sinh dục.",
        2: "Bụng, dạ dày, tử cung.",
        3: "Chân, gan, mật.",
        4: "Đùi, hông, dây thần kinh, tóc.",
        9: "Đầu, mắt, tim, máu.",
        8: "Tay, mũi, lưng, cột sống.",
        7: "Miệng, phổi, ngực, xương sườn.",
        6: "Đầu, phổi, xương, da."
    }
    
    details = f"[💉 CHI TIẾT BỆNH TẬT]:\n"
    details += f"- Do sao {star}: {star_map.get(star, 'Chưa rõ bệnh.')}\n"
    details += f"- Vị trí cơ thể (Cung {palace_num}): {palace_body_map.get(palace_num, '')}\n"
    
    # Mẹo chữa trị
    if star == "Thiên Tâm" or stem == "Ất":
        details += "- LƯU Ý: Có Thiên Tâm/Ất Kỳ là gặp được thầy thuốc giỏi, bệnh sẽ khỏi.\n"
    elif star == "Thiên Nhu" or star == "Tử Môn":
        details += "- CẢNH BÁO: Bệnh có chiều hướng nặng/mãn tính, cần kiên trì.\n"
        
    return details

# --- B. MẤT CỦA & KẺ TRỘM ---
def decode_lost_item(door, palace_num):
    direction_map = {
        1: "Hướng Bắc (Khảm). Nơi ẩm ướt, gần nước, sông hồ hoặc nhà vệ sinh, phòng tắm.",
        2: "Hướng Tây Nam (Khôn). Nơi đất trống, nhà kho, phòng ngủ người già, nơi u tối.",
        3: "Hướng Đông (Chấn). Nơi ồn ào, đường cái, chợ, hoặc trong đống gỗ, cây cối.",
        4: "Hướng Đông Nam (Tốn). Nơi thoáng gió, cửa sổ, vườn tược, hoặc dưới vật bằng gỗ.",
        9: "Hướng Nam (Ly). Nơi cao ráo, sáng sủa, gần lò bếp, thiết bị điện, ban thờ.",
        8: "Hướng Đông Bắc (Cấn). Nơi núi đồi, gò đất, tường vách, hoặc gần cửa ra vào.",
        7: "Hướng Tây (Đoài). Nơi ao đầm, giếng, hoặc gần vật kim loại, nhạc cụ.",
        6: "Hướng Tây Bắc (Càn). Nơi cao, mái nhà, phòng khách, hoặc gần vật cứng, xe cộ."
    }
    
    environment_map = {
        "Hưu Môn": "Gần nước, nơi nghỉ ngơi.",
        "Sinh Môn": "Nơi núi đá, cầu cống, hoặc phòng khách.",
        "Thương Môn": "Nơi xe cộ, đường đi, hoặc bị che khuất.",
        "Đỗ Môn": "Nơi kín đáo, bị che lấp, khó tìm.",
        "Cảnh Môn": "Nơi cao, lộ thiên, dễ nhìn thấy.",
        "Tử Môn": "Nơi đất hoang, mồ mả, hoặc thùng rác.",
        "Kinh Môn": "Nơi ồn ào, hoặc trong hang hốc.",
        "Khai Môn": "Nơi rộng rãi, công sở, hoặc ngoài đường."
    }
    
    return f"[🔍 VỊ TRÍ MẤT CỦA]:\n- Phương hướng: {direction_map.get(palace_num, '')}\n- Môi trường (Cửa {door}): {environment_map.get(door, '')}\n"

def decode_thief(star):
    thief_map = {
        "Thiên Bồng": "Nam giới, trung niên, mặt đen, mắt to, tính gian xảo, là trộm chuyên nghiệp.",
        "Thiên Nhu": "Nữ giới hoặc người béo, tính chậm chạp, có thể là người quen lấy trộm.",
        "Thiên Xung": "Nam giới, cao lớn, nóng tính, hành động nhanh, có thể đã đi xa.",
        "Thiên Phụ": "Nữ giới hoặc người có học thức, tóc dài, vẻ ngoài lịch sự.",
        "Thiên Anh": "Nữ giới, mặt đỏ hoặc hồng hào, mắt sáng, ăn mặc chải chuốt.",
        "Thiên Nhậm": "Nam giới, thấp béo, lưng hơi gù, tính lầm lì, tham lam.",
        "Thiên Trụ": "Nam giới, gầy gò, miệng rộng, răng hô, có thể có tật ở miệng/chân.",
        "Thiên Tâm": "Nam giới, người già hoặc có chức quyền, tính cẩn thận.",
        "Thiên Cầm": "Người trung tính, đàng hoàng, có thể cầm nhầm chứ không phải trộm."
    }
    return f"[👤 ĐẶC ĐIỂM KẺ LẤY (Nghi vấn)]: {thief_map.get(star, 'Khó xác định.')}\n"

# --- C. NGOẠI HÌNH ---
def decode_appearance(star):
    app_map = {
        "Thiên Bồng": "Mắt to có thần, râu quai nón (nam), da ngăm đen. Tính tình phóng khoáng.",
        "Thiên Nhu": "Mặt tròn, người đầy đặn (béo), da ngăm hoặc vàng. Tính ôn hòa nhưng bảo thủ.",
        "Thiên Xung": "Dáng cao, thanh mảnh, chân dài. Tính nóng nảy, nhanh nhẹn.",
        "Thiên Phụ": "Dáng người cân đối, thanh tú, tóc đẹp/dài (nữ). Phong thái nho nhã.",
        "Thiên Anh": "Mặt trái xoan, mắt sáng, sắc mặt hồng hào. Dáng người vừa phải, ăn mặc đẹp.",
        "Thiên Nhậm": "Dáng thấp đậm, vai rộng, lưng dày (hoặc gù). Mặt vuông vức.",
        "Thiên Trụ": "Dáng gầy, xương xẩu, lộ hầu. Tiếng nói vang hoặc chói tai.",
        "Thiên Tâm": "Dáng người tròn trịa, phúc hậu, trán cao. Có tướng lãnh đạo.",
        "Thiên Cầm": "Dáng người đẫy đà, đoan chính."
    }
    return f"[🧍 NGOẠI HÌNH]: {app_map.get(star, '')}\n"

def decode_character(door):
    char_map = {
        "Hưu Môn": "Trầm tính, thích nghỉ ngơi, lười biếng hoặc an phận.",
        "Sinh Môn": "Thực tế, ham kiếm tiền, hoạt bát, tốt bụng.",
        "Thương Môn": "Hiếu thắng, hay gây gổ, thích thể thao/hoạt động mạnh.",
        "Đỗ Môn": "Kín đáo, bí ẩn, ít nói, giỏi kỹ thuật/nghiên cứu.",
        "Cảnh Môn": "Sôi nổi, thích thể hiện, nóng nảy, trọng hư danh.",
        "Tử Môn": "Lầm lì, cố chấp, hay thù dai, khó gần.",
        "Kinh Môn": "Khéo nói nhưng hay lo lắng, hoang mang, nghi ngờ.",
        "Khai Môn": "Cởi mở, phóng khoáng, thích công việc, có chí tiến thủ."
    }
    return f"[🧠 TÍNH CÁCH]: {char_map.get(door, '')}\n"

# --- D. CON SỐ (GIÁ TIỀN, KHOẢNG CÁCH) ---
def decode_numbers(palace_num, stem):
    # Số Hà Đồ (Tiên Thiên) và Lạc Thư (Hậu Thiên)
    # Cung 1: 1, 6
    # Cung 2: 2, 5, 8, 10
    # Cung 3: 3, 4, 8
    # Cung 4: 3, 4, 5, 8
    # Cung 9: 9, 2, 7
    # Cung 8: 5, 7, 8, 10
    # Cung 7: 4, 9, 7
    # Cung 6: 1, 4, 6, 9
    
    # Số ước lượng dựa trên cung
    num_map = {
        1: "1, 6, 16, 60, 100, 600",
        2: "2, 5, 8, 10, 200, 500, 800",
        3: "3, 4, 8, 30, 40, 80, 300, 400",
        4: "3, 4, 5, 8, 300, 400, 500",
        9: "9, 2, 7, 27, 72, 90, 900",
        8: "5, 7, 8, 10, 50, 70, 80, 500",
        7: "4, 9, 7, 49, 90, 700",
        6: "1, 4, 6, 9, 100, 400, 600, 900"
    }
    
    base_nums = num_map.get(palace_num, "1, 5, 10")
    
    return f"[🔢 CON SỐ DỰ BÁO (Giá tiền/Số lượng/Khoảng cách)]: Liên quan đến các số {base_nums}. (Tùy bối cảnh để chọn đơn vị nghìn/triệu/km).\n"

# --- E. MÀU SẮC ---
def decode_color(star, stem):
    # Sao (Ngũ hành) quy định màu
    star_colors = {
        "Thiên Bồng": "Đen, Xanh nước biển (Thủy)",
        "Thiên Nhu": "Vàng, Nâu đất (Thổ)",
        "Thiên Xung": "Xanh lá cây, Xanh lục (Mộc)",
        "Thiên Phụ": "Xanh biếc, màu Gỗ (Mộc)",
        "Thiên Anh": "Đỏ, Hồng, Tím, Cam (Hỏa)",
        "Thiên Nhậm": "Vàng sậm, Nâu, màu đất (Thổ)",
        "Thiên Trụ": "Trắng, Bạc, Ghi, Xám (Kim)",
        "Thiên Tâm": "Trắng, Kim loại, Vàng kim (Kim)",
        "Thiên Cầm": "Vàng, Nâu (Thổ)"
    }
    
    # Can (Ngũ hành)
    stem_colors = {
        "Giáp": "Xanh lá", "Ất": "Xanh nown",
        "Bính": "Đỏ rực", "Đinh": "Hồng/Tím",
        "Mậu": "Vàng đất", "Kỷ": "Vàng nâu",
        "Canh": "Trắng sáng", "Tân": "Trắng trang sức",
        "Nhâm": "Đen/Xám", "Quý": "Đen/Xanh đen"
    }
    
    res = f"[🎨 MÀU SẮC DỰ BÁO]: Chủ đạo là {star_colors.get(star, 'Không rõ')}"
    if stem:
        res += f", pha lẫn {stem_colors.get(stem, '')}."
    return res + "\n"

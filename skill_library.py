
# TỪ ĐIỂN TRA CỨU NHANH KỲ MÔN - MAI HOA - LỤC HÀO (HARDCODED SKILL)
# Đây là "Kỹ năng cốt lõi" giúp AI không bao giờ trả lời sai các thuật ngữ cơ bản.

CORE_CONCEPTS = {
    # =========================================================================
    # 1. KỲ MÔN ĐỘN GIÁP (QMDG)
    # =========================================================================
    # --- TÀI CHÍNH / TIỀN BẠC ---
    "tiền": {
        "summary": "Tiền bạc trong Kỳ Môn được đại diện bởi các Dụng Thần: Giáp, Canh, Mậu, Sinh Môn.",
        "details": [
            "- **Mậu (Thổ):** Đại diện cho Vốn liếng, tiền gốc, tài sản tích lũy.",
            "- **Sinh Môn:** Đại diện cho Lợi nhuận, tiền lãi, bất động sản.",
            "- **Canh (Kim):** Đại diện cho Tiền lớn, nhưng cũng là kẻ thù cướp đoạt.",
            "- **Cửu Địa:** Tiền chôn giấu, tiết kiệm lâu dài.",
            "- **Huyền Vũ:** Đầu cơ, tiền ảo, tham ô (tiền mờ ám)."
        ]
    },
    "tiền dụng thần": {"ref": "tiền"},
    "đầu tư": {
        "summary": "Đầu tư cần xem Sinh Môn (Lợi) và Giáp Tý Mậu (Vốn).",
        "details": [
            "- Mậu sinh Sinh Môn: Đầu tư có lãi.",
            "- Sinh Môn khắc Mậu: Mất vốn, thua lỗ.",
            "- Sinh Môn ở Cung Vượng: Lãi nhiều.",
            "- Sinh Môn gặp Không Vong: Đầu tư ảo, mất trắng."
        ]
    },
    "sinh môn": {
        "summary": "Cửa của sự sinh trưởng, sự sống, lợi nhuận, bất động sản (Nhà Đất).",
        "details": [
            "- **Ngũ Hành:** Thổ (Cung Cấn).",
            "- **Ý nghĩa Tài chính:** Lợi nhuận, Bất động sản, Tiền lãi.",
            "- **Ý nghĩa Đời sống:** Sự sống, nhà cửa, đất đai, người xem bói.",
            "- **Tính chất:** Cát môn (Cửa tốt), chủ về tăng trưởng, sinh sôi."
        ]
    },

    # --- CÔNG AN / PHÁP LUẬT ---
    "công an": {
        "summary": "Lực lượng chức năng, đại diện cho sự trấn áp, kiểm soát.",
        "details": [
            "- **Bạch Hổ (White Tiger):** Hung thần, đại diện cho công an hình sự, sự hung hãn, bắt bớ.",
            "- **Thương Môn (Door of Injury):** Cửa của sự tổn thương, cũng đại diện cho cảnh sát, người thi hành công vụ.",
            "- **Canh (Kim):** Đại diện cho sự cứng rắn, ngăn chặn.",
            "- **Thiên Bồng:** Đại diện cho tội phạm lớn, trộm cướp (đối lập công an)."
        ]
    },
    "cảnh sát": {"ref": "công an"},
    "tòa án": {
        "summary": "Cơ quan xét xử, pháp luật.",
        "details": [
            "- **Khai Môn (Open Door):** Đại diện cho Tòa án, Quan tòa.",
            "- **Cảnh Môn (Scenery Door):** Đại diện cho văn bản pháp lý, đơn từ, trát tòa.",
            "- **Đinh (Hỏa):** Văn thư, giấy tờ chứng cứ."
        ]
    },

    # --- TÌNH CẢM ---
    "tình yêu": {
        "summary": "Tình cảm nam nữ, hôn nhân.",
        "details": [
            "- **Lục Hợp (Six Harmony):** Thần chuyên về mai mối, kết hợp, hòa hợp.",
            "- **Ất (Mộc):** Đại diện cho người Nữ (Vợ).",
            "- **Canh (Kim):** Đại diện cho người Nam (Chồng).",
            "- **Hưu Môn:** Sự nghỉ ngơi, gia đình êm ấm."
        ]
    },
    "kết hôn": {"ref": "tình yêu"},
    
    # --- SỨC KHỎE ---
    "bệnh": {
        "summary": "Bệnh tật và chữa trị.",
        "details": [
            "- **Thiên Nhu:** Ngôi sao đại diện cho bệnh tật.",
            "- **Tử Môn:** Cửa chết, tình trạng nguy kịch.",
            "- **Ất/Thiên Tâm:** Bác sĩ, thuốc men chữa trị."
        ]
    },

    # =========================================================================
    # 2. MAI HOA DỊCH SỐ (PLUM BLOSSOM)
    # =========================================================================
    "thể dụng": {
        "summary": "Cặp phạm trù cốt lõi trong Mai Hoa Dịch Số.",
        "details": [
            "- **Thể (Body):** Đại diện cho Chủ thể, Bản thân, Bên mình (Tĩnh).",
            "- **Dụng (Function):** Đại diện cho Khách thể, Sự việc, Đối phương (Động).",
            "- **Nguyên tắc:** Thể cần vượng, Dụng cần sinh cho Thể (Tốt). Dụng khắc Thể (Xấu)."
        ]
    },
    "thể": {"ref": "thể dụng"},
    "dụng": {"ref": "thể dụng"},
    
    "hỗ quẻ": {
        "summary": "Quẻ nằm giữa, thể hiện diễn biến trung gian hoặc nội tình sự việc.",
        "details": [
            "- Được tạo từ các hào 2,3,4 (Hạ hỗ) và 3,4,5 (Thượng hỗ) của quẻ gốc.",
            "- Cho biết quá trình diễn ra sự việc nhanh hay chậm, thuận hay nghịch."
        ]
    },
    
    "biến quẻ": {
        "summary": "Quẻ kết quả sau khi hào động biến đổi (Dương -> Âm, Âm -> Dương).",
        "details": [
            "- Đại diện cho kết quả cuối cùng, tương lai của sự việc.",
            "- Cần xem quan hệ Sinh/Khắc giữa Biến và Thể."
        ]
    },

    # =========================================================================
    # 3. LỤC HÀO / BỐC DỊCH (SIX LINES DIVINATION)
    # =========================================================================
    "thế ứng": {
        "summary": "Trục tọa độ chính trong bàn Lục Hào.",
        "details": [
            "- **Hào Thế (Subject):** Đại diện cho người hỏi, bản thân mình.",
            "- **Hào Ứng (Object):** Đại diện cho đối phương, sự việc, người mình quan tâm.",
            "- Thế Ứng tương sinh/nhị hợp là Tốt. Thế Ứng tương khắc/xung là Xấu."
        ]
    },
    "hào thế": {"ref": "thế ứng"},
    "hào ứng": {"ref": "thế ứng"},

    "lục thân": {
        "summary": "6 mối quan hệ (Dụng thần) trong Lục Hào.",
        "details": [
            "- **Phụ Mẫu:** Cha mẹ, giấy tờ, văn thư, dự án, xe cộ, nhà cửa.",
            "- **Huynh Đệ:** Anh em, bạn bè, đối thủ cạnh tranh, hao tài.",
            "- **Tử Tôn:** Con cái, phúc đức, giải thần, thuốc men, khách hàng.",
            "- **Thê Tài:** Vợ, tiền bạc, tài lộc, nhân viên.",
            "- **Quan Quỷ:** Chồng, công danh, chức vụ, bệnh tật, họa hoạn, ma quỷ."
        ]
    },
    "dụng thần lục hào": {"ref": "lục thân"},
    "phụ mẫu": {"ref": "lục thân"},
    "huynh đệ": {"ref": "lục thân"},
    "tử tôn": {"ref": "lục thân"},
    "thê tài": {"ref": "lục thân"},
    "quan quỷ": {"ref": "lục thân"},

    "phi phục": {
        "summary": "Mối quan hệ ẩn hiện của các hào.",
        "details": [
            "- **Phi Thần:** Hào hiện rõ trên quẻ.",
            "- **Phục Thần:** Hào ẩn đi (không hiện), nằm dưới Phi Thần.",
            "- Khi Dụng thần không hiện trên quẻ, phải tìm Phục Thần. Phục Thần cần Vượng/Sinh/Phi Thần Không Vong mới lộ ra được."
        ]
    },
    "bốc dịch": {
        "summary": "Phương pháp dự đoán dựa trên sự gieo quẻ (Lục hào).",
        "details": [
            "- Dùng 3 đồng xu gieo 6 lần để lập quẻ.",
            "- Cần ghi nhận ngày/tháng gieo (Nhật/Nguyệt Kìến) để luận vượng suy."
        ]
    },

    # =========================================================================
    # 4. KỸ NĂNG ỨNG KỲ (TIMING - KHI NÀO XẢY RA?) - SÁCH CHUẨN
    # =========================================================================
    "ứng kỳ": {
        "summary": "Quy tắc xác định mốc thời gian dựa trên trạng thái cung và cục diện.",
        "details": [
            "- **Định hướng Nhanh/Chậm (Tốc độ):**",
            "  + **Nhanh (Cận kỳ):** Dụng thần ở Nội Ban (Cung 1, 8, 3, 4). Phản Ngâm. Cửu tinh vượng tướng. Các sao Thiên Xung, Thiên Bồng.",
            "  + **Chậm (Viễn kỳ):** Dụng thần ở Ngoại Ban (Cung 9, 2, 7, 6). Phục Ngâm. Cửu tinh hưu tù tử. Dụng thần gặp Tuần Không, Nhập Mộ.",
            "- **Xác định mốc thời gian cụ thể (Điểm rơi):**",
            "  + **Tuần Không (Empty):** Ứng vào ngày/giờ 'Điền thực' (Lấp đầy) hoặc 'Xung thực' (Bị xung phá). Ví dụ: Tuần không ở Dần -> Ứng ngày Dần hoặc Thân.",
            "  + **Nhập Mộ (Tomb):** Ứng vào ngày/giờ 'Xung mộ'. Ví dụ: Mộ ở Thìn -> Ứng ngày Tuất.",
            "  + **Mã Tinh (Horse):** Ứng vào ngày/giờ Mã Tinh 'Động' (đúng chi của Mã) hoặc bị xung. Ví dụ: Mã ở Dần -> Ứng ngày Dần hoặc Thân.",
            "  + **Trực Phù/Trực Sử:** Ứng nghiệm vào ngày/giờ có Thiên can trùng với Trực Phù hoặc Cung của Trực Sử.",
            "- **Phân loại Quá khứ/Tương lai:**",
            "  + Dụng thần ở Phía sau (đã qua): Đại diện cho việc đã xảy ra.",
            "  + Dụng thần ở Phía trước (sắp tới): Đại diện cho việc tương lai.",
            "  + Địa chi bị Xung: Việc đã xong hoặc sắp đổ vỡ."
        ]
    },
    
    # =========================================================================
    # 5. KỸ NĂNG XEM TÍNH CÁCH (PERSONALITY PROFILING)
    # =========================================================================
    "tính cách": {
        "summary": "Tra cứu tính cách qua Cửu Tinh (Bẩm sinh) và Bát Môn (Hành vi).",
        "details": [
            "- **Thiên Bồng:** Thông minh, can đảm, nhưng cũng gian xảo, liều lĩnh, thích mạo hiểm (đen đỏ).",
            "- **Thiên Nhu:** Ôn hòa, nhu thuận, học thức, nhưng chậm chạp, bảo thủ, hay lo nghĩ.",
            "- **Thiên Xung:** Nóng nảy, thẳng thắn, làm việc nhanh, tốt bụng nhưng dễ gây gổ.",
            "- **Thiên Phụ:** Văn nhã, có giáo dục, thích giúp người, phong thái quân tử (hoặc giả tạo).",
            "- **Thiên Anh:** Nhiệt tình, hào nhoáng, thích hư danh, coi trọng vẻ bề ngoài, dễ nóng giận.",
            "- **Thiên Nhậm:** Thật thà, cam chịu, kiên trì, nhưng cũng cố chấp, chậm hiểu, ky bo.",
            "- **Thiên Trụ:** Miệng lưỡi sắc bén, logic, phá cách, nhưng hay châm chọc, kinh hãi người khác.",
            "- **Thiên Tâm:** Mưu trí, lãnh đạo, bao dung, có tâm đức, giỏi quản lý.",
            "- **Khai Môn:** Cởi mở, hướng ngoại, thích công danh. | **Hưu Môn:** Trầm tính, thích an nhàn.",
            "- **Sinh Môn:** Thực tế, ham kiếm tiền. | **Thương Môn:** Hiếu thắng, hay làm tổn thương người khác.",
            "- **Đỗ Môn:** Kín đáo, bí mật, kỹ thuật. | **Cảnh Môn:** Hào nhoáng, thích thể hiện.",
            "- **Tử Môn:** Lầm lì, hướng nội, cố chấp. | **Kinh Môn:** Hay kêu ca, lo lắng, nghi ngờ."
        ]
    },

    # =========================================================================
    # 6. KỸ NĂNG XEM GIỚI TÍNH (NAM/NỮ)
    # =========================================================================
    "nam nữ": {
        "summary": "Nguyên tắc xác định giới tính qua Âm Dương của Can/Sao.",
        "details": [
            "- **Dương (Nam):**",
            "  + Thiên Can: Giáp, Bính, Mậu, Canh, Nhâm.",
            "  + Cửu Tinh: Bồng, Nhậm, Xung, Phụ, Cầm (Trung nam).",
            "  + Bát Môn: Khai, Hưu, Sinh, Thương.",
            "- **Âm (Nữ):**",
            "  + Thiên Can: Ất, Đinh, Kỷ, Tân, Quý.",
            "  + Cửu Tinh: Nhu, Anh, Trụ, Tâm.",
            "  + Bát Môn: Đỗ, Cảnh, Tử, Kinh."
        ]
    },
    "trai hay gái": {"ref": "nam nữ"},
    "là nam hay nữ": {"ref": "nam nữ"},
    "trai": {"ref": "nam nữ"},
    "gái": {"ref": "nam nữ"},

    # =========================================================================
    # 7. KỸ NĂNG HÓA GIẢI (REMEDY - LÀM GÌ ĐỂ TỐT HƠN?)
    # =========================================================================
    "hóa giải": {
        "summary": "Phương pháp dùng vật phẩm hoặc hành động để giảm hung tăng cát.",
        "details": [
            "- **Nguyên tắc:** Lấy cung khắc chế hung tinh hoặc cung sinh cho dụng thần.",
            "- **Vật phẩm tiêu biểu:**",
            "  + Hệ Thủy (Hóa Kim/Thổ hung): Thác nước, bể cá, pha lê xanh.",
            "  + Hệ Mộc (Hóa Thủy hung): Cây xanh, tranh phong cảnh rừng.",
            "  + Hệ Hỏa (Hóa Mộc hung): Đèn đỏ, thảm đỏ, đá thạch anh tím.",
            "  + Hệ Thổ (Hóa Hỏa hung): Đá muối, bình gốm, thạch anh vàng.",
            "  + Hệ Kim (Hóa Thổ hung): Chuông gió kim loại, tiền xu cổ."
        ]
    },

    # =========================================================================
    # 8. KỸ NĂNG DỰ BÁO THỜI TIẾT (WEATHER)
    # =========================================================================
    "thời tiết": {
        "summary": "Dự báo mưa nắng qua các Tinh/Môn/Thần.",
        "details": [
            "- **Mưa:** Thiên Bồng (Mưa lớn), Huyền Vũ (Mưa dầm), Thiên Trụ (Gió mưa).",
            "- **Nắng:** Cảnh Môn (Nắng gắt), Thiên Anh (Trời trong), Cửu Ly (Ánh sáng).",
            "- **Gió:** Thiên Tốn (Gió mạnh), Thương Môn (Gió giật).",
            "- **Mây/Sương:** Đỗ Môn (Mây mù), Thái Âm (Sương giá)."
        ]
    },

    # =========================================================================
    # 9. CẤU TRÚC CỤC DIỆN (ADVANCED PATTERNS)
    # =========================================================================
    "cấu trúc": {
        "summary": "Các cách cục lớn ảnh hưởng tới toàn bộ bàn cờ.",
        "details": [
            "- **Phản Ngâm:** Các sao/cửa đối xung nhau. Chủ về biến động cực nhanh, đảo lộn, lặp đi lặp lại. Cần hành động tốc chiến tốc thắng.",
            "- **Phục Ngâm:** Các sao/cửa nằm đúng vị trí gốc. Chủ về trì trệ, bế tắc, không nên động đậy. Việc gì cũng kéo dài, khó dứt điểm.",
            "- **Thiên Võng Khôi Khôi (Lưới trời lồng lộng):** Quý nhân lâm Cung 6,7,8,9. Chủ về bị bao vây, pháp luật, khó thoát ra ngoài.",
            "- **Minh Phù Ám Hợp:** Có người giúp đỡ bí mật từ phía sau, hoặc có giao dịch ngầm thành công.",
            "- **Ngũ Bất Ngộ Thời:** Giờ khắc Can Ngày. Trăm việc đều xấu, không nên khởi sự."
        ]
    },
    "phục ngâm": {"ref": "cấu trúc"},
    "cách cục": {"ref": "cấu trúc"},

    # =========================================================================
    # 10. DANH MỤC TRA CỨU DỤNG THẦN (REFERENCE OBJECTS)
    # =========================================================================
    "dụng thần": {
        "summary": "Tra cứu xem đối tượng cần hỏi được đại diện bởi yếu tố nào trong bàn cờ.",
        "details": [
            "- **Bản thân (Tôi/Mình):** Nhật Can (Can ngày), Cung vị của Can Năm sinh (Bản mệnh).",
            "- **Đối thủ / Kẻ thù / Người ghét mình:** Canh (Đại diện cho sự ngăn trở), Cung khắc với Nhật Can, hoặc Thiên Bồng / Huyền Vũ (Tiểu nhân).",
            "- **Vợ / Bạn gái:** Ất Kỳ.",
            "- **Chồng / Bạn trai:** Canh Kim.",
            "- **Con cái:** Thời Can (Can giờ).",
            "- **Cấp trên / Sếp / Cha mẹ:** Trực Phù, Can Năm (Tuế Can).",
            "- **Đồng nghiệp / Bạn bè:** Nguyệt Can (Can Tháng).",
            "- **Kiện tụng / Pháp luật:** Kinh Môn (Lời buộc tội), Khai Môn (Thẩm phán), Trực Phù (Nguyên cáo), Thiên Ất (Bị cáo).",
            "- **Xuất hành / Đi xa:** Mã Tinh (Tốc độ), Cửu Thiên (Đường bộ/Hàng không).",
            "- **Tiền bạc / Lợi nhuận:** Sinh Môn, Giáp Tý Mậu.",
            "- **Bệnh tật:** Thiên Nhu (Bệnh), Thiên Tâm (Thuốc), Tử Môn (Tình trạng nặng)."
        ]
    },
    "người ghét": {"ref": "dụng thần"},
    "kẻ thù": {"ref": "dụng thần"},
    "đối thủ": {"ref": "dụng thần"},
    "bệnh": {"ref": "dụng thần"},
    "vợ": {"ref": "dụng thần"},
    "chồng": {"ref": "dụng thần"},
    "con": {"ref": "dụng thần"},
    "sếp": {"ref": "dụng thần"},
    "cha mẹ": {"ref": "dụng thần"},
    "bạn": {"ref": "dụng thần"},
    "kiện": {"ref": "dụng thần"},
    "đi xa": {"ref": "dụng thần"},

    # =========================================================================
    # 11. KINH DỊCH & MAI HOA DỊCH SỐ (I-CHING & PLUM BLOSSOM)
    # =========================================================================
    "dịch lý": {
        "summary": "Nguyên lý biến hóa của 64 quẻ và quan hệ Thể Dụng.",
        "details": [
            "- **Mai Hoa Dịch Số (Thể/Dụng):**",
            "  + **Thể (Chủ):** Bản thân, sự việc hiện tại.",
            "  + **Dụng (Biến):** Kết quả, đối phương, tương lai.",
            "  + Thể khắc Dụng hoặc Dụng sinh Thể: Vạn sự như ý, có lợi nhuận.",
            "  + Thể sinh Dụng hoặc Dụng khắc Thể: Hao tài tốn của, gặp trở ngại.",
            "- **Kinh Dịch (64 Quẻ):**",
            "  + **Hào Động:** Là điểm mấu chốt gây ra sự thay đổi.",
            "  + **Trung Chính:** Hào 2 (Hạ quẻ) và Hào 5 (Thượng quẻ) là vị trí đẹp nhất, chủ sự hanh thông.",
            "  + **Lời Tượng/Truyện:** Cần căn cứ vào hình ảnh thiên nhiên (Trời, Đất, Sấm, Gió...) để luận đoán bối cảnh."
        ]
    },
    "quẻ": {"ref": "dịch lý"},
    "mai hoa": {"ref": "dịch lý"},
    "kinh dịch": {"ref": "dịch lý"}
}

def lookup_concept(query):
    query = query.lower()
    
    # Direct Key Match
    if query in CORE_CONCEPTS:
        entry = CORE_CONCEPTS[query]
        if "ref" in entry: return CORE_CONCEPTS[entry["ref"]]
        return entry

    # Fuzzy Search inside Keys
    for key, entry in CORE_CONCEPTS.items():
        if key in query: # e.g. "thế ứng là gì" contains "thế ứng"
            if "ref" in entry: return CORE_CONCEPTS[entry["ref"]]
            return entry
            
    return None

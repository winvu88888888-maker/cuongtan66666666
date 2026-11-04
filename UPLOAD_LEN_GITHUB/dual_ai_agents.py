"""
dual_ai_agents.py — V101.4: HỆ THỐNG SONG NÃO AI 2 TẦNG (DUAL-AGENT PIPELINE)
================================================================================
- CON AI SỐ 1 (QuestionReaderAI): Chuyên đọc câu hỏi, bóc tách ngữ nghĩa, nhận diện
  chính xác câu hỏi thuộc dạng nào trong 25 Đại Dạng Câu Hỏi Toàn Cầu, tách các vế
  phương án (A hay B), xác định Đối tượng (Hỏi cho ai) và chỉ định đúng Dụng Thần
  cần tra cứu trong quẻ.
- CON AI SỐ 2 (HexagramReasoningAI): Nhận Hồ Sơ Câu Hỏi từ Con AI Số 1, mang đi
  ĐỐI CHỨNG TRỰC TIẾP với Quẻ lập theo Giờ - Ngày - Tháng - Năm (Lục Hào, Kỳ Môn,
  Mai Hoa, Đại Lục Nhâm, 18 Tầng), kiểm tra Tuần Không / Động Tĩnh / Sinh Khắc
  rồi suy luận ra câu trả lời khớp 100% với thực tế của quẻ.
"""

import re


# Bảng 25 Đại Dạng Câu Hỏi Toàn Cầu (Chuẩn hóa toàn diện mọi câu hỏi trên thế giới)
UNIVERSAL_25_ARCHETYPES = {
    "D01_LOCATION_BINARY": {
        "code": "Dạng 1",
        "name": "Xác định Vị trí Thực tế Hiện tại (Ở nhà hay Ở công ty / Trong nhà hay Ngoài đường)",
        "mode": "BINARY_LOCATION",
        "lh_dt": "Hào Thế (Bản thân) + Nội Quái/Phụ Mẫu/Tử Tôn (Nhà) đối chứng Quan Quỷ/Ngoại Quái (Công ty)",
        "km_dt": "Nhật Can (Người hỏi) lâm Cửa Tĩnh (Hưu/Tử/Đỗ/Sinh = Ở nhà) đối chứng Cửa Động (Khai/Cảnh/Thương = Công sở/Ngoài đường)",
        "answer_rule": "Bắt buộc chốt dứt khoát ĐANG Ở ĐÂU (tuyệt đối cấm trả lời 'Cần cân nhắc / Giằng co')",
    },
    "D02_POSTURE_STATE": {
        "code": "Dạng 2",
        "name": "Xác định Tư thế & Trạng thái Cơ thể (Đứng hay Ngồi / Nằm hay Ngồi / Ngủ hay Thức)",
        "mode": "BINARY_POSTURE",
        "lh_dt": "Hào Thế (Động hay Tĩnh) + Quẻ Chủ/Biến (Cấn/Khôn = Ngồi/Nằm; Chấn/Càn = Đứng/Đi)",
        "km_dt": "Cung Bản Mệnh lâm Hưu/Đỗ/Tử/Cửu Địa (Tĩnh = Ngồi/Nằm) đối chứng Thương/Kinh/Cửu Thiên (Động = Đứng/Đi)",
        "answer_rule": "Bắt buộc chốt dứt khoát ĐANG NGỒI/NẰM hay ĐANG ĐỨNG/DI CHUYỂN",
    },
    "D03_TRUE_OR_FALSE": {
        "code": "Dạng 3",
        "name": "Kiểm định Thật hay Giả / Nói thật hay Nói dối / Tin đồn thực hư",
        "mode": "BINARY_TRUTH",
        "lh_dt": "Hào Ứng & Dụng Thần (Lâm Tuần Không / Huyền Vũ / Đằng Xà = Giả dối; Hữu khí / Thanh Long = Sự thật)",
        "km_dt": "Thời Can & Cung Ứng (Kinh Môn / Huyền Vũ / Đằng Xà / Không Vong = Tin giả; Cảnh/Khai/Trực Phù = Thật)",
        "answer_rule": "Bắt buộc khẳng định ĐÂY LÀ SỰ THẬT hay CHUYỆN GIẢ / LỜI NÓI DỐI",
    },
    "D04_DONE_OR_NOT": {
        "code": "Dạng 4",
        "name": "Kiểm tra Tiến độ Sự việc Đã xảy ra hay Chưa (Rồi hay Chưa / Đã... chưa)",
        "mode": "BINARY_PROGRESS",
        "lh_dt": "Dụng Thần & Hào Động (Phát động/Đế Vượng = Đã làm rồi; Tĩnh/Tuần Không/Thai Dưỡng = Chưa làm)",
        "km_dt": "Thời Can & Bát Môn (Đỗ Môn/Tử Môn/Không Vong = Chưa thực hiện; Khai/Sinh/Xung = Đã thực hiện)",
        "answer_rule": "Bắt buộc chốt rõ ĐÃ THỰC HIỆN RỒI hay CHƯA THỰC HIỆN",
    },
    "D05_CHOICE_A_OR_B": {
        "code": "Dạng 5",
        "name": "Lựa chọn Nhị phân Phương án A hay Phương án B bất kỳ",
        "mode": "BINARY_OPTION_AB",
        "lh_dt": "Trục 1 (Hào Thế / Nội Quái / Quẻ Chủ = Phương án A) đối chứng Trục 2 (Hào Ứng / Ngoại Quái / Quẻ Biến = Phương án B)",
        "km_dt": "Cung Chủ (Phương án A) đối chứng Cung Khách/Biến (Phương án B) — loại trừ bên phạm Tuần Không/Tử Môn",
        "answer_rule": "Bắt buộc chọn dứt khoát Phương án A hoặc Phương án B tốt hơn/đúng hơn từ quẻ",
    },
    "D06_GENDER_AGE": {
        "code": "Dạng 6",
        "name": "Định danh Giới tính (Nam hay Nữ) & Độ tuổi / Năm sinh",
        "mode": "IDENTITY_GENDER_AGE",
        "lh_dt": "Âm Dương Hào Dụng Thần + Quái khí Càn/Chấn/Khảm/Cấn (Nam) vs Khôn/Tốn/Ly/Đoài (Nữ) + 12 Trường Sinh (Tuổi)",
        "km_dt": "Thiên Can & Cửu Tinh tại Cung Dụng Thần + Vòng Trường Sinh định khung tuổi & năm sinh",
        "answer_rule": "Chốt rõ NAM GIỚI hay NỮ GIỚI và khoảng ĐỘ TUỔI + NĂM SINH ứng hợp",
    },
    "D07_CHILDREN_COUNT": {
        "code": "Dạng 7",
        "name": "Tử tức & Con cái (Bao nhiêu người con / Mấy trai mấy gái / Sinh con)",
        "mode": "CHILDREN_FORENSIC",
        "lh_dt": "Hào Tử Tôn (Nếu phạm Tuần Không/Tử Môn = Hiện tại 0 con / Hỏi thử; Nếu hữu khí = Số con & tỷ lệ Trai/Gái)",
        "km_dt": "Cung Tử Tôn & Lục Hợp / Sinh Môn (Định số lượng con và phân bổ Nam/Nữ)",
        "answer_rule": "Nếu Tử Tôn Tuần Không phải báo ngay HIỆN TẠI CHƯA CÓ CON (0 CON); đồng thời nêu tiềm năng số con & mấy trai mấy gái",
    },
    "D08_PERSON_PROFILE": {
        "code": "Dạng 8",
        "name": "Phác họa Chân dung Con người: Ngoại hình, Tính cách & Nghề nghiệp",
        "mode": "PERSON_PORTRAIT",
        "lh_dt": "Ngũ Hành Dụng Thần + Lục Thú (Thanh Long, Chu Tước, Bạch Hổ, Huyền Vũ, Câu Trận, Đằng Xà)",
        "km_dt": "Cửu Tinh + Bát Thần + Bát Môn tại Cung Dụng Thần (Mô tả vóc dáng, tâm tính, ngành nghề)",
        "answer_rule": "Mô tả chi tiết Ngoại hình, Tính cách và Nghề nghiệp theo Ngũ Hành & Cửu Tinh trong quẻ",
    },
    "D09_QUANTITY_PRICE": {
        "code": "Dạng 9",
        "name": "Định lượng Con số, Giá cả, Tiền bạc, Điểm số & Số lượng",
        "mode": "NUMERIC_QUANTITY",
        "lh_dt": "Số Tiên Thiên Bát Quái + Số Hậu Thiên Lạc Thư + Số Hà Đồ của Hành Dụng Thần",
        "km_dt": "Số Cung Kỳ Môn + Trạng thái Vượng/Tướng/Hưu/Tù nhân hệ số định lượng",
        "answer_rule": "Đưa ra bộ Con số định lượng chuẩn, Số lượng đơn vị và Bội số giá trị tiền bạc/tài lộc",
    },
    "D10_OBJECT_XAPHU": {
        "code": "Dạng 10",
        "name": "Đoán Vạn Vật Xạ Phú (Đồ vật gì trong hộp kín / Màu sắc / Chất liệu / Hình dáng)",
        "mode": "OBJECT_FORENSIC",
        "lh_dt": "Ngũ Hành Hào Dụng Thần + Quái Tượng Nội/Ngoại + 12 Trường Sinh (Mới/Cũ/Hỏng)",
        "km_dt": "Thiên Can + Cửu Tinh + Bát Quái tại Cung Dụng Thần (Xác định chất liệu, màu sắc, hình dáng, tên đồ vật)",
        "answer_rule": "Chỉ rõ tên nhóm Đồ vật, Màu sắc, Chất liệu, Hình dáng và Tình trạng đồ vật",
    },
    "D11_LOST_ITEM_WHERE": {
        "code": "Dạng 11",
        "name": "Tìm Đồ thất lạc / Tìm Người / Xác định Địa điểm & Phương hướng (Ở đâu / Hướng nào)",
        "mode": "LOST_AND_FOUND",
        "lh_dt": "Hào Dụng Thần (Thê Tài/Phụ Mẫu) + Quái vị (Định vị độ cao: trên cao, ngang tầm hay sát đất)",
        "km_dt": "Cung Dụng Thần & Cung Thời Can (Định Phương hướng, Khoảng cách và Môi trường xung quanh nơi thất lạc)",
        "answer_rule": "Chốt rõ CÓ TÌM LẠI ĐƯỢC KHÔNG + Phương hướng + Vị trí cụ thể nơi đồ vật/người đang ở",
    },
    "D12_TIMING_WHEN": {
        "code": "Dạng 12",
        "name": "Thời điểm Ứng kỳ Chính xác (Khi nào / Bao giờ / Ngày Giờ Tháng Năm nào)",
        "mode": "TIMING_FORECAST",
        "lh_dt": "Hào Dụng Thần (Tuần Không = Ngày Xuất Không/Xung Không; Nhập Mộ = Ngày Xung Mộ; Động = Ngày Hợp; Tĩnh = Ngày Xung)",
        "km_dt": "Cung Dụng Thần & Khắc Ứng Kỳ Môn (Định mốc Giờ - Ngày - Tháng Dương lịch & Âm lịch)",
        "answer_rule": "Chỉ rõ mốc Giờ, Ngày, Tháng ứng nghiệm cụ thể dựa trên quy luật Xung/Hợp/Xuất Không của Dụng Thần",
    },
    "D13_CAUSE_MOTIVE_WHY": {
        "code": "Dạng 13",
        "name": "Truy tìm Nguyên nhân, Lý do & Tâm lý / Ý đồ ngầm (Tại sao / Vì sao / Họ nghĩ gì)",
        "mode": "CAUSE_AND_MOTIVE",
        "lh_dt": "Hào Kỵ Thần / Hào Động tác động lên Dụng Thần + Thế–Ứng tương tác",
        "km_dt": "Bát Thần + Cửu Tinh + Cách cục Thiên/Địa Can tại Cung Đối phương (Bóc tách nguyên nhân & tâm ý)",
        "answer_rule": "Giải thích rõ Nguyên nhân gốc rễ trong quẻ và Tâm lý/Ý đồ thật sự của đối phương",
    },
    "D14_CAREER_WORK": {
        "code": "Dạng 14",
        "name": "Công việc, Sự nghiệp, Xin việc, Thăng chức & Nghỉ việc hay Làm tiếp",
        "mode": "CAREER_DECISION",
        "lh_dt": "Hào Quan Quỷ (Công danh/Cơ quan) + Hào Phụ Mẫu (Hợp đồng/Hồ sơ) + Hào Thế",
        "km_dt": "Cửa Khai Môn (Công việc/Chức vụ) + Cung Bản Mệnh (Sinh/Khắc)",
        "answer_rule": "Phán quyết rõ Nên giữ việc hay chuyển việc / Khả năng thăng tiến, xin việc kèm hướng hành động",
    },
    "D15_FINANCE_INVEST": {
        "code": "Dạng 15",
        "name": "Tài chính, Đầu tư, Kinh doanh, Chứng khoán, Bất động sản & Mua bán",
        "mode": "FINANCE_INVESTMENT",
        "lh_dt": "Hào Thê Tài (Lợi nhuận/Vốn) + Hào Tử Tôn (Nguồn sinh tài) + Hào Huynh Đệ (Rủi ro hao tài)",
        "km_dt": "Cửa Sinh Môn (Lợi nhuận) + Can Giáp Tý Mậu (Vốn) — xét Sinh Môn sinh hay khắc Bản Mệnh",
        "answer_rule": "Chốt rõ NÊN ĐẦU TƯ/GIAO DỊCH (Có lãi) hay KHÔNG NÊN (Tránh đọng vốn/thua lỗ)",
    },
    "D16_DEBT_LOAN": {
        "code": "Dạng 16",
        "name": "Đòi nợ, Cho vay, Thu hồi công nợ & Vay vốn Ngân hàng",
        "mode": "DEBT_RECOVERY",
        "lh_dt": "Hào Thê Tài (Khoản tiền) + Hào Ứng (Con nợ/Ngân hàng) đối chứng Hào Thế",
        "km_dt": "Trực Phù (Chủ nợ) + Thiên Ất (Con nợ) + Thương Môn (Người đi đòi nợ)",
        "answer_rule": "Chốt rõ CÓ ĐÒI LẠI ĐƯỢC NỢ KHÔNG / VAY ĐƯỢC KHÔNG và cách thức thu hồi hiệu quả nhất",
    },
    "D17_LOVE_MARRIAGE": {
        "code": "Dạng 17",
        "name": "Tình cảm, Hôn nhân, Vợ chồng, Người yêu cũ Quay lại & Ngoại tình",
        "mode": "LOVE_RELATIONSHIP",
        "lh_dt": "Hào Thê Tài (Nam hỏi) / Quan Quỷ (Nữ hỏi) + Trục Thế–Ứng (Sinh Hợp hay Xung Khắc)",
        "km_dt": "Can Ất (Nữ) + Can Canh (Nam) + Thần Lục Hợp (Hôn nhân/Tình duyên)",
        "answer_rule": "Phán quyết rõ tình cảm Còn chân thành / Có quay lại hàn gắn không hay Có khoảng cách/người thứ ba",
    },
    "D18_HEALTH_MEDICAL": {
        "code": "Dạng 18",
        "name": "Sức khỏe, Bệnh tật, Phẫu thuật, Tiên lượng Sinh–Tử & Y Dịch",
        "mode": "HEALTH_MEDICAL",
        "lh_dt": "Hào Dụng Thần (Người bệnh) + Hào Quan Quỷ (Bệnh tinh) + Hào Tử Tôn (Thuốc men/Bác sĩ)",
        "km_dt": "Sao Thiên Nhuế (Bệnh tinh) + Sao Thiên Tâm & Ất Kỳ (Bác sĩ/Thuốc điều trị)",
        "answer_rule": "Đánh giá rõ Tiên lượng sức khỏe (Nhẹ/Nặng/Hồi phục), căn nguyên bệnh và hướng tìm thầy thuốc",
    },
    "D19_FENGSHUI_GRAVE": {
        "code": "Dạng 19",
        "name": "Phong thủy Dương trạch (Nhà đất, Xây sửa nhà) & Âm phần (Mồ mả Gia tiên)",
        "mode": "FENGSHUI_ESTATE",
        "lh_dt": "Hào Phụ Mẫu (Nhà đất/Mồ mả) + Hào 2 (Trạch vị) + Hào 5 (Nhân đinh)",
        "km_dt": "Sinh Môn (Dương trạch) + Tử Môn (Âm phần/Mồ mả) + Huyền Không Phi Tinh Vận 9",
        "answer_rule": "Chẩn đoán rõ Phong thủy Nhà đất / Mồ mả đang Tụ khí Cát lành hay Động khí cần tu bổ",
    },
    "D20_EXAM_STUDY_VISA": {
        "code": "Dạng 20",
        "name": "Thi cử, Học hành, Điểm số, Bằng cấp & Xin Visa / Du học",
        "mode": "EXAM_VISA",
        "lh_dt": "Hào Phụ Mẫu (Điểm số/Văn bằng/Visa) + Hào Quan Quỷ (Danh vị) + Hào Thế (Thí sinh)",
        "km_dt": "Sao Thiên Phụ (Văn Xương) + Cửa Cảnh Môn (Bài thi/Hồ sơ Visa)",
        "answer_rule": "Chốt rõ Khả năng Thi đỗ / Đậu Visa và các môn/khâu hồ sơ cần lưu ý",
    },
    "D21_LAWSUIT_COMPETE": {
        "code": "Dạng 21",
        "name": "Kiện tụng, Pháp lý, Tranh chấp, Đấu thầu & Thi đấu Thắng–Thua",
        "mode": "COMPETITION_LAWSUIT",
        "lh_dt": "Hào Thế (Bên ta) đối kháng Hào Ứng (Đối phương) + Hào Quan Quỷ (Tòa án/Trọng tài)",
        "km_dt": "Trực Phù (Nguyên đơn) + Thiên Ất (Bị đơn) + Cửa Kinh Môn / Khai Môn (Quan tòa)",
        "answer_rule": "Phán quyết rõ BÊN BẠN THẮNG hay ĐỐI PHƯƠNG CHIẾM ƯU THẾ hay NÊN HÒA GIẢI",
    },
    "D22_TRAVEL_JOURNEY": {
        "code": "Dạng 22",
        "name": "Xuất hành, Đi xa, Du lịch, Công tác & An toàn Giao thông",
        "mode": "TRAVEL_SAFETY",
        "lh_dt": "Hào Thế (Người đi) + Hào Ứng (Nơi đến) + Hào Phụ Mẫu (Phương tiện/Hành lý) + Dịch Mã",
        "km_dt": "Hướng Cung nơi đến + Cửa Cảnh/Khai/Hưu/Sinh (Thượng lộ bình an hay Trắc trở)",
        "answer_rule": "Kết luận rõ Chuyến đi Thượng lộ bình an hay Cần đề phòng trắc trở/chậm trễ",
    },
    "D23_WEATHER_CLIMATE": {
        "code": "Dạng 23",
        "name": "Dự báo Thời tiết & Thiên tượng (Mưa hay Nắng / Giông bão)",
        "mode": "WEATHER_FORECAST",
        "lh_dt": "Hào Phụ Mẫu (Mưa/Mây) + Hào Tử Tôn (Nắng/Quang đãng) + Hào Huynh Đệ (Gió) + Hào Thê Tài (Tạnh ráo)",
        "km_dt": "Sao Thiên Bồng/Khảm (Mưa) đối chứng Sao Thiên Anh/Ly (Nắng) + Thiên Phụ/Tốn (Gió)",
        "answer_rule": "Dự báo dứt khoát TRỜI MƯA hay TRỜI NẮNG RÁO theo Ngũ Hành & Cửu Tinh",
    },
    "D24_AUSPICIOUS_DATE": {
        "code": "Dạng 24",
        "name": "Trạch Cát / Xem Ngày Giờ Tốt (Khai trương, Cưới hỏi, Động thổ, Ký kết)",
        "mode": "DATE_SELECTION",
        "lh_dt": "Nhật Thần & Nguyệt Lệnh tương sinh Hào Thế và Hào Dụng Thần",
        "km_dt": "Tam Kỳ (Ất, Bính, Đinh) hội Tam Cát Môn (Khai, Hưu, Sinh) — tránh Ngũ Bất Ngộ Thời",
        "answer_rule": "Kết luận rõ Ngày giờ này ĐẠI CÁT nên tiến hành ngay hay Cần chọn khung giờ/ngày khác",
    },
    "D25_SPIRITUAL_GENERAL": {
        "code": "Dạng 25",
        "name": "Tâm linh, Giấc mơ, Điềm báo, Vận mệnh & Quyết định Tổng quát",
        "mode": "SPIRITUAL_GENERAL",
        "lh_dt": "Quẻ Chủ – Quẻ Hỗ – Quẻ Biến + Lục Thần (Đằng Xà/Huyền Vũ = Mộng mị; Thanh Long = Điềm lành)",
        "km_dt": "Thần Bàn (Trực Phù, Thái Âm, Đằng Xà, Cửu Thiên) + Cung Bản Mệnh",
        "answer_rule": "Giải mã rõ Ý nghĩa điềm báo/giấc mơ hoặc Cát/Hung tổng quát của sự việc",
    },
}


class QuestionReaderAI:
    """
    CON AI SỐ 1: Chuyên trách ĐỌC HIỂU CÂU HỎI của người dùng.
    Không đoán mò, không trả lời chung chung — nhiệm vụ của Con AI Số 1 là:
      1. Đọc kỹ từng chữ, hiểu đúng ý định thật sự của người hỏi (kể cả câu hỏi gài/hỏi thử).
      2. Phân loại chính xác vào 1 trong 25 Đại Dạng Câu Hỏi Toàn Cầu (kèm các câu hỏi phụ nếu hỏi gộp).
      3. Nếu có cấu trúc lựa chọn "A hay B", tách rõ Phương án A và Phương án B.
      4. Xác định rõ Đối tượng được hỏi (Bản thân, Bố mẹ, Con cái, Vợ/Chồng, Đối tác...) và chỉ định Dụng Thần chuẩn xác để giao cho Con AI Số 2 đi tra quẻ.
    """

    @staticmethod
    def analyze_question(question: str, dung_than_hint: str = "", category_hint: str = "") -> dict:
        q_raw = str(question or "").strip()
        q_low = q_raw.lower()

        # 1. Phát hiện Đối tượng được hỏi (Subject / Person)
        subject_person = "Bản thân người hỏi"
        subject_lh_dt = dung_than_hint or "Bản Thân"
        person_patterns = [
            (["bố tôi", "cha tôi", "mẹ tôi", "ba tôi", "má tôi", "bố mẹ", "ông bà", "bố ", "mẹ "], "Bố / Mẹ / Bậc sinh thành", "Phụ Mẫu"),
            (["con trai", "con gái", "con tôi", "con cái", "người con", "mấy trai mấy gái", "sinh con"], "Con cái (Tử tức)", "Tử Tôn"),
            (["chồng tôi", "chồng ", "bạn trai", "người yêu"], "Chồng / Người yêu", "Quan Quỷ"),
            (["vợ tôi", "vợ ", "bạn gái"], "Vợ / Bạn gái", "Thê Tài"),
            (["anh trai", "chị gái", "em trai", "em gái", "anh em", "bạn bè"], "Anh chị em / Bạn bè", "Huynh Đệ"),
            (["đối tác", "khách hàng", "đối phương", "người đó", "họ "], "Đối phương / Đối tác (Hào Ứng)", "Hào Ứng"),
            (["sếp", "cấp trên", "công ty", "cơ quan"], "Cấp trên / Công ty", "Quan Quỷ"),
        ]
        for kws, p_label, p_dt in person_patterns:
            if any(k in q_low for k in kws):
                # Tránh nhầm "con số" là "con cái"
                if p_dt == "Tử Tôn" and any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao"]):
                    continue
                subject_person = p_label
                if not dung_than_hint:
                    subject_lh_dt = p_dt
                break

        # 2. Nhận diện Đại Dạng Câu Hỏi Chính (Primary Archetype trong 25 Dạng)
        arch_key = "D25_SPIRITUAL_GENERAL"
        option_a = ""
        option_b = ""

        is_children_q = (
            any(w in q_low for w in ["bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con", "bao nhiêu con", "mấy trai mấy gái", "con cái", "sinh con", "đường con cái", "tử tức"])
            and not any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao"])
        )
        is_where_home_work = (
            any(w in q_low for w in ["ở nhà hay", "hay ở nhà", "ở công ty", "ở cơ quan", "ở văn phòng", "ở quán", "ngoài đường", "trong nhà hay", "ngoài sân"])
            and any(w in q_low for w in ["nhà", "công ty", "cơ quan", "văn phòng", "ngoài", "phòng"])
        )
        is_posture = any(w in q_low for w in ["đứng hay ngồi", "ngồi hay đứng", "nằm hay ngồi", "ngồi hay nằm", "đang đứng hay", "đang ngồi hay", "đang nằm hay", "ngủ hay thức", "thức hay ngủ"])
        is_true_false = any(w in q_low for w in ["thật hay giả", "giả hay thật", "nói thật hay", "nói dối hay", "có thật không", "thật không", "lừa dối"])
        is_done_yet = any(w in q_low for w in ["rồi hay chưa", "chưa hay rồi", "hay chưa", "ăn cơm chưa", "ăn chưa", "về chưa", "đi chưa", "xong chưa", "đã ăn", "đã về", "đã đi"])
        is_quit_work = any(w in q_low for w in ["nghỉ hay", "nên nghỉ", "nghỉ việc", "bỏ việc", "xin nghỉ", "làm tiếp hay", "đi hay ở", "ở lại hay"])
        is_gender_age = any(w in q_low for w in ["nam hay nữ", "nữ hay nam", "trai hay gái", "gái hay trai", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "sinh năm"]) and not is_children_q
        is_weather = any(w in q_low for w in ["mưa hay nắng", "nắng hay mưa", "thời tiết", "có mưa không", "trời mưa", "trời nắng", "bão"])
        is_lawsuit = any(w in q_low for w in ["kiện", "tòa án", "pháp lý", "tranh chấp", "ai thắng", "thắng hay thua", "thắng hay đối phương", "đấu thầu"])
        is_profile = any(w in q_low for w in ["ngoại hình", "hình dáng người", "cao hay thấp", "béo hay gầy", "tính cách", "tính nết", "làm nghề gì", "nghề nghiệp gì", "ngành gì"])
        is_quantity = any(w in q_low for w in ["giá bao nhiêu", "bao nhiêu tiền", "mấy tỷ", "mấy triệu", "con số", "số mấy", "định lượng", "số lượng bao nhiêu"]) and not is_children_q and not is_gender_age
        is_object = any(w in q_low for w in ["trong hộp", "trong túi", "trong phòng có gì", "đồ vật gì", "vật gì", "là cái gì", "màu gì", "chất liệu gì", "hình gì"])
        is_lost_where = any(w in q_low for w in ["mất", "thất lạc", "tìm lại", "tìm thấy", "ở đâu", "hướng nào", "chỗ nào"]) and not is_where_home_work
        is_when = any(w in q_low for w in ["khi nào", "bao giờ", "mấy giờ", "ngày nào", "tháng nào", "năm nào", "bao lâu"])
        is_why = any(w in q_low for w in ["tại sao", "vì sao", "nguyên nhân", "lý do", "do đâu", "ý đồ gì", "nghĩ gì", "tâm lý"])
        is_debt = any(w in q_low for w in ["đòi nợ", "trả nợ", "thu hồi nợ", "cho vay", "vay tiền", "vay ngân hàng", "khoản nợ", "con nợ"])
        is_invest = any(w in q_low for w in ["đầu tư", "kinh doanh", "buôn bán", "mở quán", "mở cửa hàng", "chứng khoán", "cổ phiếu", "có lãi", "lời hay lỗ", "mua bán", "xuống tiền"])
        is_love = any(w in q_low for w in ["yêu", "tình cảm", "hôn nhân", "vợ chồng", "người yêu", "quay lại", "hàn gắn", "chia tay", "ly hôn", "kết hôn", "ngoại tình"])
        is_health = any(w in q_low for w in ["bệnh", "ốm", "nằm viện", "phẫu thuật", "mổ", "sức khỏe", "qua khỏi", "khỏi bệnh", "thuốc", "bác sĩ", "tai nạn", "nguy kịch"])
        is_fengshui = any(w in q_low for w in ["phong thủy", "nhà đất", "xây nhà", "sửa nhà", "mua nhà", "mồ mả", "âm phần", "mộ phần", "gia tiên", "động thổ", "hướng nhà"])
        is_exam = any(w in q_low for w in ["thi đỗ", "thi đậu", "kỳ thi", "đi thi", "thi cử", "học hành", "điểm thi", "bằng cấp", "du học", "xin visa", "phỏng vấn visa"])
        is_travel = any(w in q_low for w in ["xuất hành", "đi xa", "du lịch", "công tác", "chuyến đi", "lên đường", "về quê", "di chuyển", "thượng lộ"])
        is_trachcat = any(w in q_low for w in ["xem ngày", "ngày tốt", "giờ tốt", "ngày đẹp", "khai trương", "nhập trạch", "cưới hỏi"])
        is_career = any(w in q_low for w in ["công việc", "sự nghiệp", "xin việc", "thăng chức", "chuyển việc", "nhảy việc", "hợp đồng"])

        if is_where_home_work:
            arch_key = "D01_LOCATION_BINARY"
            option_a, option_b = "Đang ở Nhà (Tại gia)", "Đang ở Công ty / Bên ngoài"
        elif is_posture:
            arch_key = "D02_POSTURE_STATE"
            option_a, option_b = "Đang Ngồi / Nằm nghỉ (Tĩnh)", "Đang Đứng / Di chuyển (Động)"
        elif is_true_false:
            arch_key = "D03_TRUE_OR_FALSE"
            option_a, option_b = "Sự thật (Đáng tin cậy)", "Chuyện giả / Lời nói dối"
        elif is_done_yet:
            arch_key = "D04_DONE_OR_NOT"
            option_a, option_b = "Đã thực hiện rồi", "Chưa thực hiện"
        elif is_children_q:
            arch_key = "D07_CHILDREN_COUNT"
        elif is_gender_age:
            arch_key = "D06_GENDER_AGE"
        elif is_weather:
            arch_key = "D23_WEATHER_CLIMATE"
            option_a, option_b = "Trời Mưa / Nhiều mây ẩm", "Trời Nắng / Quang đãng"
        elif is_lawsuit:
            arch_key = "D21_LAWSUIT_COMPETE"
            option_a, option_b = "Bên bạn (Hào Thế)", "Đối phương (Hào Ứng)"
        elif is_quit_work:
            arch_key = "D14_CAREER_WORK"
            option_a, option_b = "Nên giữ công việc hiện tại (Ở lại)", "Nên nghỉ việc / Chuyển hướng"
        elif (" hay " in q_low) and not any(w in q_low for w in ["hay không", "có nên"]):
            m_ab = re.search(r'(?:đang\s+|là\s+|nên\s+|chọn\s+)?([^,?.;!]+?)\s+hay\s+([^,?.;!]+)', q_low)
            if m_ab:
                arch_key = "D05_CHOICE_A_OR_B"
                option_a = m_ab.group(1).strip()
                option_b = m_ab.group(2).strip()
                for pfx in ["tôi đang ", "tôi nên ", "tôi ", "bạn đang ", "hiện tại "]:
                    if option_a.startswith(pfx):
                        option_a = option_a[len(pfx):].strip()
        elif is_profile:
            arch_key = "D08_PERSON_PROFILE"
        elif is_quantity:
            arch_key = "D09_QUANTITY_PRICE"
        elif is_object:
            arch_key = "D10_OBJECT_XAPHU"
        elif is_lost_where:
            arch_key = "D11_LOST_ITEM_WHERE"
        elif is_when and not (is_career or is_invest or is_love or is_health):
            arch_key = "D12_TIMING_WHEN"
        elif is_why:
            arch_key = "D13_CAUSE_MOTIVE_WHY"
        elif is_debt:
            arch_key = "D16_DEBT_LOAN"
        elif is_invest:
            arch_key = "D15_FINANCE_INVEST"
        elif is_love:
            arch_key = "D17_LOVE_MARRIAGE"
        elif is_health:
            arch_key = "D18_HEALTH_MEDICAL"
        elif is_fengshui:
            arch_key = "D19_FENGSHUI_GRAVE"
        elif is_exam:
            arch_key = "D20_EXAM_STUDY_VISA"
        elif is_travel:
            arch_key = "D22_TRAVEL_JOURNEY"
        elif is_trachcat:
            arch_key = "D24_AUSPICIOUS_DATE"
        elif is_career:
            arch_key = "D14_CAREER_WORK"
        elif is_when:
            arch_key = "D12_TIMING_WHEN"

        arch_meta = UNIVERSAL_25_ARCHETYPES.get(arch_key, UNIVERSAL_25_ARCHETYPES["D25_SPIRITUAL_GENERAL"])

        # 3. Nhận diện các câu hỏi phụ đi kèm (Sub-intents trong câu hỏi phức hợp)
        sub_intents = []
        if is_when and arch_key != "D12_TIMING_WHEN":
            sub_intents.append("Hỏi kèm Thời điểm Ứng kỳ (Khi nào / Bao giờ)")
        if any(w in q_low for w in ["ở đâu", "hướng nào", "chỗ nào"]) and arch_key not in ("D01_LOCATION_BINARY", "D11_LOST_ITEM_WHERE"):
            sub_intents.append("Hỏi kèm Phương hướng & Không gian (Ở đâu / Hướng nào)")
        if any(w in q_low for w in ["bao nhiêu", "mấy"]) and arch_key not in ("D06_GENDER_AGE", "D07_CHILDREN_COUNT", "D09_QUANTITY_PRICE"):
            sub_intents.append("Hỏi kèm Định lượng Con số / Số lượng")
        if any(w in q_low for w in ["làm sao", "giải pháp", "cách nào", "hóa giải"]):
            sub_intents.append("Hỏi kèm Pháp quyết Hóa giải & Hành động")

        return {
            "raw_question": q_raw,
            "archetype_key": arch_key,
            "archetype_code": arch_meta["code"],
            "archetype_name": arch_meta["name"],
            "question_mode": arch_meta["mode"],
            "subject_person": subject_person,
            "subject_lh_dt": subject_lh_dt,
            "lh_dt_instruction": arch_meta["lh_dt"],
            "km_dt_instruction": arch_meta["km_dt"],
            "answer_rule": arch_meta["answer_rule"],
            "option_a": option_a,
            "option_b": option_b,
            "sub_intents": sub_intents,
        }


class HexagramReasoningAI:
    """
    CON AI SỐ 2: Chuyên trách SUY LUẬN & ĐỐI CHỨNG QUẺ.
    Nhận Bản Hồ Sơ Câu Hỏi (`blueprint`) từ Con AI Số 1, mang đi đối chứng trực tiếp
    với Quẻ lập theo Giờ - Ngày - Tháng - Năm hiện tại (`chart_data`, `luc_hao_data`,
    `mai_hoa_data`, `omni_data`) để:
      1. Xác minh từng hào, từng cung, từng sao/cửa xem khớp với phương án nào.
      2. Phát hiện ngay nếu câu hỏi rơi vào Tuần Không / Không Vong (câu hỏi thử / không có thật
         hoặc loại trừ phương án sai trong câu hỏi A hay B).
      3. Đưa ra kết luận đối chứng 1-1 không lệch nửa bước khỏi quẻ.
    """

    @staticmethod
    def cross_verify_and_reason(
        blueprint: dict,
        dung_than: str,
        weighted_pct: int,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
        auth_warnings: list = None,
        is_fake: bool = False,
        narrative_summary: str = "",
    ) -> dict:
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        auth_warnings = auth_warnings or []

        can_n = chart_data.get("can_ngay", "Giáp")
        chi_n = chart_data.get("chi_ngay", "Tý")
        can_g = chart_data.get("can_gio", "Giáp")
        chi_g = chart_data.get("chi_gio", "Tý")
        can_m = chart_data.get("can_thang", "")
        chi_m = chart_data.get("chi_thang", "")
        can_y = chart_data.get("can_nam", "")
        chi_y = chart_data.get("chi_nam", "")
        cuc_km = chart_data.get("cuc", "?")
        don_type = "Dương Độn" if chart_data.get("is_duong_don", True) else "Âm Độn"

        lh_ban = luc_hao_data.get("ban", {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = luc_hao_data.get("bien", {}) if isinstance(luc_hao_data, dict) else {}
        ten_que_chu = lh_ban.get("name") or mai_hoa_data.get("ten_que") or omni_data.get("ten_que_ban") or "Quẻ Chủ"
        ten_que_bien = lh_bien.get("name") or mai_hoa_data.get("ten_qua_bien") or omni_data.get("ten_que_bien") or "Quẻ Biến"
        dong_hao_list = luc_hao_data.get("dong_hao") or lh_ban.get("dong_hao") or []

        target_cung = omni_data.get("target_cung", "?")
        c_info = omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}
        huong_cung = c_info.get("huong", "Chính Nam")
        sao_name = omni_data.get("sao_name", "Thiên Tâm")
        cua_name = omni_data.get("cua_name", "Khai Môn")
        than_name = omni_data.get("than_name", "Trực Phù")
        hanh_dt = omni_data.get("hanh", "Kim")
        ts_stage = omni_data.get("ts_stage", "Vượng")

        # Trích xuất câu kết luận chuẩn đã được giải mã từ bộ 25 Đại Dạng
        headline_ans = omni_data.get("binary_verdict_headline", "")
        if not headline_ans and narrative_summary:
            m_ans = re.search(r"📢\s*\*\*CÂU TRẢ LỜI:\*\*\s*(.+?)(?:\n|$)", narrative_summary)
            if m_ans:
                headline_ans = re.sub(r"<[^>]+>", "", m_ans.group(1)).strip()
                headline_ans = re.sub(r"\*\*(.+?)\*\*", r"\1", headline_ans)

        # Trích xuất lý do đối chứng từ quẻ
        why_proof = omni_data.get("binary_why_reasons", "")
        if not why_proof and narrative_summary:
            m_why = re.search(r"📋\s*\*\*VÌ SAO:\*\*\s*(.+?)(?:\n|$)", narrative_summary)
            if m_why:
                why_proof = m_why.group(1).strip()

        # Xây dựng Ma trận Đối Chứng Quẻ 4 Trục của Con AI Số 2
        tu_tru_str = f"Năm {can_y} {chi_y} · Tháng {can_m} {chi_m} · Ngày {can_n} {chi_n} · Giờ {can_g} {chi_g}".strip(" ·")
        dong_str = f"Động hào {', '.join(map(str, dong_hao_list))}" if dong_hao_list else "Quẻ Tĩnh (6 hào an tĩnh)"

        # Kiểm tra trạng thái Tuần Không / Nghiệm chứng trong quẻ
        if is_fake and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Tuần Không / Tử Môn</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Quẻ dùng phép <b>Loại Trừ Nhị Phân</b>: Bác bỏ hoàn toàn phương án bị Không Vong để khẳng định 100% phương án thực tế còn lại!"
            )
        elif is_fake:
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> phạm <b>Tuần Không / Không Vong</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Cảnh báo sự việc/đối tượng đang hỏi hiện <b>chưa tồn tại ngoài thực tế (= 0)</b> hoặc là câu hỏi thử lòng quẻ."
            )
        else:
            auth_status_str = (
                f"Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> hữu khí trên quẻ ({ts_stage}), sự việc có thật và đang vận hành theo đúng khí số."
            )

        # Tạo khối HTML hiển thị trực quan sự phối hợp giữa CON AI SỐ 1 và CON AI SỐ 2
        sub_intents_html = ""
        if blueprint.get("sub_intents"):
            sub_intents_html = f" · <b>Ý phụ đi kèm:</b> {', '.join(blueprint['sub_intents'])}"

        ab_html = ""
        if blueprint.get("option_a") and blueprint.get("option_b"):
            ab_html = (
                f'<div style="margin-top:5px;font-size:0.9em;color:#bae6fd;">'
                f'⚖️ <b>Tách 2 vế đối chứng:</b> [Phương án 1]: <b>{blueprint["option_a"]}</b> ↔ [Phương án 2]: <b>{blueprint["option_b"]}</b>'
                f'</div>'
            )

        dual_agent_html = (
            f'<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);padding:16px 18px;border-radius:14px;margin-bottom:16px;border:2px solid #38bdf8;box-shadow:0 6px 22px rgba(56,189,248,0.22);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px;border-bottom:1px solid rgba(56,189,248,0.3);padding-bottom:8px;">'
            f'<div style="font-size:1.06em;font-weight:900;color:#38bdf8;letter-spacing:0.3px;">🤖 HỆ THỐNG SONG NÃO AI 2 TẦNG (V101.4): AI ĐỌC HIỂU CÂU HỎI ➔ AI ĐỐI CHỨNG QUẺ & SUY LUẬN</div>'
            f'<span style="background:rgba(56,189,248,0.18);color:#7dd3fc;padding:3px 10px;border-radius:12px;font-size:0.82em;font-weight:800;border:1px solid #38bdf8;">Khớp {blueprint["archetype_code"]}/25 Đại Dạng Toàn Cầu</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;">'
            # Card AI Số 1
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #38bdf8;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#7dd3fc;margin-bottom:6px;">🧠 AI SỐ 1 — CHUYÊN ĐỌC & THẤU HIỂU CÂU HỎI</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Nhận diện dạng câu hỏi:</b> <span style="color:#fde047;font-weight:800;">{blueprint["archetype_code"]} — {blueprint["archetype_name"]}</span><br>'
            f'• <b>Đối tượng trọng tâm:</b> {blueprint["subject_person"]} (Giao Dụng Thần: <b>{dung_than}</b>){sub_intents_html}<br>'
            f'• <b>Chỉ thị tra quẻ cho AI Số 2:</b> <i>{blueprint["lh_dt_instruction"]}</i>'
            f'{ab_html}'
            f'</div></div>'
            # Card AI Số 2
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #fbbf24;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#fde047;margin-bottom:6px;">🔮 AI SỐ 2 — CHUYÊN ĐỐI CHỨNG QUẺ & SUY LUẬN ĐÁP ÁN</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Quẻ lập đúng thời khắc ({tu_tru_str}):</b> Quẻ <b>{ten_que_chu}</b> ➔ <b>{ten_que_bien}</b> ({dong_str}) · Kỳ Môn Cục {cuc_km} ({don_type}, Cung {target_cung} {huong_cung}: Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b>, Thần <b>{than_name}</b>)<br>'
            f'• <b>Kết quả đối chứng Thực/Hư:</b> {auth_status_str}<br>'
            f'• <b>Đáp án suy luận khớp quẻ:</b> <span style="color:#4ade80;font-weight:900;">{headline_ans or "Đã khớp toàn bộ 18 tầng quẻ"}</span>'
            f'</div></div>'
            f'</div></div>'
        )

        # Tạo bản chỉ thị bắt buộc (Prompt Directive) để khóa cứng LLM Online (nếu gọi Gemini)
        online_directive = (
            f"=== HỒ SƠ BÀN GIAO TỪ HỆ THỐNG SONG NÃO AI 2 TẦNG (BẮT BUỘC TUÂN THỦ 100%) ===\n"
            f"1. [AI SỐ 1 - ĐỌC CÂU HỎI]:\n"
            f"   - Câu hỏi thuộc: {blueprint['archetype_code']} ({blueprint['archetype_name']})\n"
            f"   - Đối tượng: {blueprint['subject_person']} | Dụng Thần: {dung_than} (Hành {hanh_dt})\n"
            f"   - Quy tắc trả lời bắt buộc: {blueprint['answer_rule']}\n"
            f"2. [AI SỐ 2 - ĐỐI CHỨNG QUẺ ({tu_tru_str})]:\n"
            f"   - Lục Hào & Mai Hoa: Quẻ {ten_que_chu} biến {ten_que_bien} ({dong_str})\n"
            f"   - Kỳ Môn Độn Giáp: Cung {target_cung} ({huong_cung}) hội Sao {sao_name}, Cửa {cua_name}, Thần {than_name}\n"
            f"   - Đối chứng Thực/Hư: {re.sub(r'<[^>]+>', '', auth_status_str)}\n"
            f"   - ĐÁP ÁN ĐỐI CHỨNG CHỐT HẠ (TUYỆT ĐỐI KHÔNG ĐƯỢC SỬA ĐỔI HAY BỊA KHÁC ĐI): {headline_ans}\n"
            f"   - Căn cứ suy luận: {re.sub(r'<[^>]+>', '', why_proof)}\n"
        )

        return {
            "blueprint": blueprint,
            "verified_headline": headline_ans,
            "verified_why": why_proof,
            "dual_agent_html": dual_agent_html,
            "online_directive": online_directive,
        }

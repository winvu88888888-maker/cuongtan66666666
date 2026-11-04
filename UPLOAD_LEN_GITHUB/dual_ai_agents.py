"""
dual_ai_agents.py — V101.6: HỆ THỐNG SONG NÃO AI 2 TẦNG (DUAL-AGENT PIPELINE)
================================================================================
- CON AI SỐ 1 (QuestionReaderAI): Chạy NGAY ĐẦU TIÊN khi nhận câu hỏi để đọc hiểu
  ngữ nghĩa, bóc tách chính xác đối tượng được hỏi (nhà mấy tầng, ở tầng mấy, mấy phòng,
  mấy anh chị em, mặc áo màu gì, đi xe gì, ở nhà hay công ty, đã kết hôn chưa...),
  khóa cứng Dụng Thần chuẩn (ví dụ: Nhà cửa/Số tầng = Phụ Mẫu + Hào Thế, tuyệt đối
  không để nhầm sang Thê Tài đầu tư BĐS).
- CON AI SỐ 2 (HexagramReasoningAI): Nhận Hồ Sơ Câu Hỏi từ Con AI Số 1, mang đi
  ĐỐI CHỨNG TRỰC TIẾP với Quẻ lập theo Giờ - Ngày - Tháng - Năm (Lục Hào, Kỳ Môn,
  Mai Hoa, Đại Lục Nhâm, 18 Tầng), suy luận ra câu trả lời trực diện khớp 100% với
  câu hỏi và quẻ, khóa cứng toàn bộ đầu ra Online & Offline.
"""

import re


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
        "name": "Định lượng Con số, Số tầng nhà, Số phòng, Số người, Kích thước & Giá trị",
        "mode": "NUMERIC_QUANTITY",
        "lh_dt": "Hào Phụ Mẫu & Hào Thế (Đoán số tầng nhà/vị trí tầng) + Số Tiên/Hậu Thiên Bát Quái + Số Hà Đồ Lạc Thư",
        "km_dt": "Số Cung Kỳ Môn + Trạng thái Vượng/Tướng/Hưu/Tù định lượng con số thực tế",
        "answer_rule": "Chốt trực diện con số thực tế cho đúng đối tượng được hỏi (mấy tầng, tầng mấy, mấy phòng, mấy người, giá bao nhiêu...)",
    },
    "D10_OBJECT_XAPHU": {
        "code": "Dạng 10",
        "name": "Đoán Vạn Vật Xạ Phú (Đồ vật gì / Mặc áo màu gì / Đi xe gì / Chất liệu / Hình dáng)",
        "mode": "OBJECT_FORENSIC",
        "lh_dt": "Ngũ Hành Hào Dụng Thần (Phụ Mẫu = Áo/Xe; Thê Tài = Đồ vật) + Quái Tượng Nội/Ngoại + 12 Trường Sinh",
        "km_dt": "Thiên Can + Cửu Tinh + Bát Quái tại Cung Dụng Thần (Xác định màu sắc, chất liệu, hình dáng, tên đồ vật)",
        "answer_rule": "Chỉ rõ Màu sắc, Tên đồ vật/trang phục/xe cộ, Chất liệu, Hình dáng và Tình trạng thực tế",
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
        "name": "Tình cảm, Hôn nhân, Tình trạng Độc thân/Kết hôn, Vợ chồng & Quay lại",
        "mode": "LOVE_RELATIONSHIP",
        "lh_dt": "Hào Thê Tài (Nam hỏi) / Quan Quỷ (Nữ hỏi) + Trục Thế–Ứng (Sinh Hợp hay Xung Khắc / Tuần Không)",
        "km_dt": "Can Ất (Nữ) + Can Canh (Nam) + Thần Lục Hợp (Hôn nhân/Tình duyên)",
        "answer_rule": "Phán quyết rõ Đã có gia đình/người yêu hay Độc thân; Còn yêu hay Có quay lại hàn gắn không",
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
    CON AI SỐ 1: Chuyên trách ĐỌC HIỂU CÂU HỎI của người dùng (Chạy ở Bước 0).
    Phân tích chính xác câu hỏi đang hỏi về CÁI GÌ, SỐ LƯỢNG GÌ, AI, Ở ĐÂU, LỰA CHỌN NÀO,
    và chỉ định Dụng Thần bắt buộc (`authoritative_dt`) để Con AI Số 2 đối chứng với quẻ.
    """

    @staticmethod
    def analyze_question(question: str, dung_than_hint: str = "", category_hint: str = "") -> dict:
        q_raw = str(question or "").strip()
        q_low = q_raw.lower()

        # 1. Phát hiện các mục tiêu câu hỏi đặc thù (Specific Question Targets)
        specific_target = ""
        authoritative_dt = ""
        subject_person = "Bản thân người hỏi"

        # A. Hỏi về Số tầng nhà / Ở tầng mấy / Số phòng / Diện tích nhà
        is_house_floors_q = any(w in q_low for w in [
            "mấy tầng", "bao nhiêu tầng", "tầng mấy", "tầng thứ mấy", "tầng bao nhiêu",
            "nhà cao mấy", "nhà mấy lầu", "mấy lầu", "lầu mấy", "mấy phòng", "bao nhiêu phòng",
            "diện tích bao nhiêu", "rộng bao nhiêu", "bao nhiêu m2", "bao nhiêu mét vuông"
        ])
        # B. Hỏi về Số anh chị em trong gia đình / Con thứ mấy
        is_siblings_q = any(w in q_low for w in [
            "mấy anh chị em", "bao nhiêu anh chị em", "mấy anh em", "bao nhiêu anh em",
            "mấy chị em", "con thứ mấy", "thứ mấy trong nhà", "con trưởng hay con út", "con đầu hay"
        ])
        # C. Hỏi về Tình trạng Hôn nhân thực tế (Đã kết hôn chưa / Có vợ chồng chưa / Độc thân hay có gia đình)
        is_marital_status_q = any(w in q_low for w in [
            "kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
            "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"
        ])
        # D. Hỏi về Trang phục đang mặc / Xe cộ đang đi / Màu sắc áo, xe, nhà / Biển số xe
        is_clothing_vehicle_q = any(w in q_low for w in [
            "mặc áo màu gì", "áo màu gì", "quần áo màu gì", "trang phục màu gì", "mặc đồ màu gì",
            "đi xe gì", "xe màu gì", "xe của tôi màu gì", "biển số xe", "số nhà bao nhiêu",
            "số nhà mấy", "nhà màu gì", "nhà sơn màu gì", "cửa màu gì"
        ])
        # E. Hỏi về Xung quanh / Trong phòng có mấy người / Có ai bên cạnh không
        is_people_around_q = any(w in q_low for w in [
            "xung quanh tôi có mấy người", "trong phòng có mấy người", "ở đây có mấy người",
            "bên cạnh tôi có ai", "có mấy người đang", "tôi đang ở một mình hay", "ở một mình hay"
        ])

        has_age_word = any(w in q_low for w in ["bao nhiêu tuổi", "mấy tuổi", "tuổi", "sinh năm", "năm sinh"])
        is_children_age_q = (
            has_age_word
            and any(w in q_low for w in [
                "con gái", "con trai", "con của tôi", "con tôi", "mấy đứa con", "hai đứa con",
                "2 đứa con", "các con", "con cái", "đứa con", "chúng nó"
            ])
            and not is_siblings_q
        )
        is_children_q = (
            (not has_age_word)
            and any(w in q_low for w in [
                "bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con",
                "bao nhiêu con", "mấy trai mấy gái", "con cái", "sinh con", "đường con cái", "tử tức",
                "có con chưa", "mấy đứa"
            ])
            and not any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao", "con thứ mấy"])
            and not is_siblings_q
        )

        is_where_home_work = (
            any(w in q_low for w in ["ở nhà hay", "hay ở nhà", "ở công ty", "ở cơ quan", "ở văn phòng", "ở quán", "ngoài đường", "trong nhà hay", "ngoài sân"])
            and any(w in q_low for w in ["nhà", "công ty", "cơ quan", "văn phòng", "ngoài", "phòng"])
        )
        is_posture = any(w in q_low for w in ["đứng hay ngồi", "ngồi hay đứng", "nằm hay ngồi", "ngồi hay nằm", "đang đứng hay", "đang ngồi hay", "đang nằm hay", "ngủ hay thức", "thức hay ngủ"])
        is_true_false = any(w in q_low for w in ["thật hay giả", "giả hay thật", "nói thật hay", "nói dối hay", "có thật không", "thật không", "lừa dối"])
        is_done_yet = (
            any(w in q_low for w in ["rồi hay chưa", "chưa hay rồi", "hay chưa", "ăn cơm chưa", "ăn chưa", "về chưa", "đi chưa", "xong chưa", "đã ăn", "đã về", "đã đi"])
            and not is_marital_status_q and not is_children_q
        )
        is_quit_work = any(w in q_low for w in ["nghỉ hay", "nên nghỉ", "nghỉ việc", "bỏ việc", "xin nghỉ", "làm tiếp hay", "đi hay ở", "ở lại hay"])
        is_gender_age = any(w in q_low for w in ["nam hay nữ", "nữ hay nam", "trai hay gái", "gái hay trai", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "sinh năm"]) and not is_children_q
        is_weather = any(w in q_low for w in ["mưa hay nắng", "nắng hay mưa", "thời tiết", "có mưa không", "trời mưa", "trời nắng", "bão"])
        is_lawsuit = any(w in q_low for w in ["kiện", "tòa án", "pháp lý", "tranh chấp", "ai thắng", "thắng hay thua", "thắng hay đối phương", "đấu thầu"])
        is_profile = any(w in q_low for w in ["ngoại hình", "hình dáng người", "cao hay thấp", "béo hay gầy", "tính cách", "tính nết", "làm nghề gì", "nghề nghiệp gì", "ngành gì", "cao bao nhiêu", "nặng bao nhiêu"])
        is_object = any(w in q_low for w in ["trong hộp", "trong túi", "trong phòng có gì", "trước mặt tôi có", "trên bàn có", "cầm cái gì", "đồ vật gì", "vật gì", "là cái gì", "màu gì", "chất liệu gì", "hình gì"]) and not is_clothing_vehicle_q
        is_when = any(w in q_low for w in ["khi nào", "bao giờ", "mấy giờ", "ngày nào", "tháng nào", "năm nào", "bao lâu", "tháng mấy"])
        # Mọi câu hỏi có từ "mấy" hoặc "bao nhiêu" hoặc "số mấy" (không phải tuổi, con cái, thời gian)
        has_numeric_word = bool(re.search(r"\b(mấy|bao nhiêu|số mấy|thứ mấy|định lượng|số lượng)\b", q_low))
        is_quantity = (
            has_numeric_word
            and not is_children_q
            and not is_gender_age
            and not is_when
        )
        is_lost_where = any(w in q_low for w in ["mất", "thất lạc", "tìm lại", "tìm thấy", "ở đâu", "hướng nào", "chỗ nào"]) and not is_where_home_work and not is_house_floors_q
        is_why = any(w in q_low for w in ["tại sao", "vì sao", "nguyên nhân", "lý do", "do đâu", "ý đồ gì", "nghĩ gì", "tâm lý"])
        is_debt = any(w in q_low for w in ["đòi nợ", "trả nợ", "thu hồi nợ", "cho vay", "vay tiền", "vay ngân hàng", "khoản nợ", "con nợ"])
        is_invest = any(w in q_low for w in ["đầu tư", "kinh doanh", "buôn bán", "mở quán", "mở cửa hàng", "chứng khoán", "cổ phiếu", "có lãi", "lời hay lỗ", "mua bán", "xuống tiền", "mua đất", "bán đất", "mua nhà", "bán nhà"])
        is_love = any(w in q_low for w in ["yêu", "tình cảm", "hôn nhân", "vợ chồng", "người yêu", "quay lại", "hàn gắn", "chia tay", "ly hôn", "kết hôn", "ngoại tình"])
        is_health = any(w in q_low for w in ["bệnh", "ốm", "nằm viện", "phẫu thuật", "mổ", "sức khỏe", "qua khỏi", "khỏi bệnh", "thuốc", "bác sĩ", "tai nạn", "nguy kịch"])
        is_fengshui = any(w in q_low for w in ["phong thủy", "nhà đất", "xây nhà", "sửa nhà", "mồ mả", "âm phần", "mộ phần", "gia tiên", "động thổ", "hướng nhà"]) and not is_house_floors_q and not is_invest
        is_exam = any(w in q_low for w in ["thi đỗ", "thi đậu", "kỳ thi", "đi thi", "thi cử", "học hành", "điểm thi", "bằng cấp", "du học", "xin visa", "phỏng vấn visa"])
        is_travel = any(w in q_low for w in ["xuất hành", "đi xa", "du lịch", "công tác", "chuyến đi", "lên đường", "về quê", "di chuyển", "thượng lộ"])
        is_trachcat = any(w in q_low for w in ["xem ngày", "ngày tốt", "giờ tốt", "ngày đẹp", "khai trương", "nhập trạch", "cưới hỏi"])
        is_career = any(w in q_low for w in ["công việc", "sự nghiệp", "xin việc", "thăng chức", "chuyển việc", "nhảy việc", "hợp đồng"])

        arch_key = "D25_SPIRITUAL_GENERAL"
        option_a = ""
        option_b = ""

        if is_house_floors_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "HOUSE_FLOORS"
            subject_person = "Ngôi nhà & Vị trí tầng người hỏi đang ở"
            authoritative_dt = "Phụ Mẫu"
        elif is_siblings_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "SIBLINGS_COUNT"
            subject_person = "Anh chị em trong gia đình & Thứ bậc bản thân"
            authoritative_dt = "Huynh Đệ"
        elif is_people_around_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "PEOPLE_AROUND"
            subject_person = "Không gian & Số người xung quanh bạn"
            authoritative_dt = "Bản Thân"
        elif is_marital_status_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "MARITAL_STATUS_NOW"
            subject_person = "Tình trạng Hôn nhân / Tình duyên hiện tại"
            authoritative_dt = "Thê Tài"
        elif is_clothing_vehicle_q:
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "CLOTHING_VEHICLE"
            subject_person = "Trang phục / Phương tiện / Màu sắc & Biển số thực tế"
            authoritative_dt = "Phụ Mẫu"
        elif is_where_home_work:
            arch_key = "D01_LOCATION_BINARY"
            specific_target = "LOCATION_HOME_WORK"
            option_a, option_b = "Đang ở Nhà (Tại gia)", "Đang ở Công ty / Bên ngoài"
        elif is_posture:
            arch_key = "D02_POSTURE_STATE"
            specific_target = "POSTURE_STATE"
            option_a, option_b = "Đang Ngồi / Nằm nghỉ (Tĩnh)", "Đang Đứng / Di chuyển (Động)"
        elif is_true_false:
            arch_key = "D03_TRUE_OR_FALSE"
            specific_target = "TRUE_OR_FALSE"
            option_a, option_b = "Sự thật (Đáng tin cậy)", "Chuyện giả / Lời nói dối"
        elif is_done_yet:
            arch_key = "D04_DONE_OR_NOT"
            specific_target = "DONE_OR_NOT"
            option_a, option_b = "Đã thực hiện rồi", "Chưa thực hiện"
        elif is_children_age_q:
            arch_key = "D06_GENDER_AGE"
            specific_target = "CHILDREN_AGE"
            if "con gái" in q_low and "con trai" in q_low:
                subject_person = "Con gái & Con trai của người hỏi (Tử tức)"
            elif "con gái" in q_low:
                subject_person = "Con gái của người hỏi (Tử tức)"
            elif "con trai" in q_low:
                subject_person = "Con trai của người hỏi (Tử tức)"
            else:
                subject_person = "Các con của người hỏi (Tử tức)"
            authoritative_dt = "Tử Tôn"
        elif is_children_q:
            arch_key = "D07_CHILDREN_COUNT"
            specific_target = "CHILDREN_COUNT"
            subject_person = "Con cái (Tử tức)"
            authoritative_dt = "Tử Tôn"
        elif is_gender_age:
            arch_key = "D06_GENDER_AGE"
            specific_target = "GENDER_AGE"
        elif is_weather:
            arch_key = "D23_WEATHER_CLIMATE"
            specific_target = "WEATHER"
            option_a, option_b = "Trời Mưa / Nhiều mây ẩm", "Trời Nắng / Quang đãng"
        elif is_lawsuit:
            arch_key = "D21_LAWSUIT_COMPETE"
            specific_target = "LAWSUIT"
            option_a, option_b = "Bên bạn (Hào Thế)", "Đối phương (Hào Ứng)"
        elif is_quit_work:
            arch_key = "D14_CAREER_WORK"
            specific_target = "QUIT_OR_STAY"
            option_a, option_b = "Nên giữ công việc hiện tại (Ở lại)", "Nên nghỉ việc / Chuyển hướng"
        elif (" hay " in q_low) and not any(w in q_low for w in ["hay không", "có nên"]):
            m_ab = re.search(r'(?:đang\s+|là\s+|nên\s+|chọn\s+)?([^,?.;!]+?)\s+hay\s+([^,?.;!]+)', q_low)
            if m_ab:
                arch_key = "D05_CHOICE_A_OR_B"
                specific_target = "GENERIC_AB"
                option_a = m_ab.group(1).strip()
                option_b = m_ab.group(2).strip()
                for pfx in ["tôi đang ", "tôi nên ", "tôi ", "bạn đang ", "hiện tại "]:
                    if option_a.startswith(pfx):
                        option_a = option_a[len(pfx):].strip()
        elif is_profile:
            arch_key = "D08_PERSON_PROFILE"
            specific_target = "PERSON_PROFILE"
        elif is_object:
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "HIDDEN_OBJECT"
        elif is_quantity:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "GENERAL_QUANTITY"
        elif is_lost_where:
            arch_key = "D11_LOST_ITEM_WHERE"
            specific_target = "LOST_ITEM"
        elif is_when and not (is_career or is_invest or is_love or is_health):
            arch_key = "D12_TIMING_WHEN"
            specific_target = "TIMING_WHEN"
        elif is_why:
            arch_key = "D13_CAUSE_MOTIVE_WHY"
            specific_target = "CAUSE_WHY"
        elif is_debt:
            arch_key = "D16_DEBT_LOAN"
            specific_target = "DEBT_LOAN"
            authoritative_dt = "Thê Tài"
        elif is_invest:
            arch_key = "D15_FINANCE_INVEST"
            specific_target = "INVEST_PROFIT"
            authoritative_dt = "Thê Tài"
        elif is_love:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "LOVE_MARRIAGE"
        elif is_health:
            arch_key = "D18_HEALTH_MEDICAL"
            specific_target = "HEALTH_MEDICAL"
        elif is_fengshui:
            arch_key = "D19_FENGSHUI_GRAVE"
            specific_target = "FENGSHUI_GRAVE"
            authoritative_dt = "Phụ Mẫu"
        elif is_exam:
            arch_key = "D20_EXAM_STUDY_VISA"
            specific_target = "EXAM_VISA"
            authoritative_dt = "Phụ Mẫu"
        elif is_travel:
            arch_key = "D22_TRAVEL_JOURNEY"
            specific_target = "TRAVEL_SAFETY"
        elif is_trachcat:
            arch_key = "D24_AUSPICIOUS_DATE"
            specific_target = "AUSPICIOUS_DATE"
        elif is_career:
            arch_key = "D14_CAREER_WORK"
            specific_target = "CAREER_WORK"
            authoritative_dt = "Quan Quỷ"
        elif is_when:
            arch_key = "D12_TIMING_WHEN"
            specific_target = "TIMING_WHEN"

        arch_meta = UNIVERSAL_25_ARCHETYPES.get(arch_key, UNIVERSAL_25_ARCHETYPES["D25_SPIRITUAL_GENERAL"])

        sub_intents = []
        if is_when and arch_key != "D12_TIMING_WHEN":
            sub_intents.append("Hỏi kèm Thời điểm Ứng kỳ (Khi nào / Bao giờ)")
        if any(w in q_low for w in ["ở đâu", "hướng nào", "chỗ nào"]) and arch_key not in ("D01_LOCATION_BINARY", "D11_LOST_ITEM_WHERE"):
            sub_intents.append("Hỏi kèm Phương hướng & Không gian (Ở đâu / Hướng nào)")
        if has_numeric_word and arch_key not in ("D06_GENDER_AGE", "D07_CHILDREN_COUNT", "D09_QUANTITY_PRICE"):
            sub_intents.append("Hỏi kèm Định lượng Con số / Số lượng")

        return {
            "raw_question": q_raw,
            "archetype_key": arch_key,
            "archetype_code": arch_meta["code"],
            "archetype_name": arch_meta["name"],
            "question_mode": arch_meta["mode"],
            "specific_target": specific_target,
            "authoritative_dt": authoritative_dt,
            "subject_person": subject_person,
            "subject_lh_dt": authoritative_dt or dung_than_hint or "Bản Thân",
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
    `mai_hoa_data`, `omni_data`) để giải mã trực diện từng câu hỏi đặc thù!
    """

    @staticmethod
    def deduce_specialized_answer(
        blueprint: dict,
        dung_than: str,
        weighted_pct: int,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
        auth_warnings: list = None,
        is_fake: bool = False,
    ) -> dict:
        """
        Giải mã chuyên biệt của CON AI SỐ 2 cho các câu hỏi thực tế đời sống
        (Nhà mấy tầng, Ở tầng mấy, Mấy phòng, Mấy anh chị em, Kết hôn chưa, Mặc áo màu gì, Đi xe gì...)
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        target = blueprint.get("specific_target", "")
        q_low = blueprint.get("raw_question", "").lower()

        lh_ban = luc_hao_data.get("ban", {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = luc_hao_data.get("bien", {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or []
        ten_que_chu = lh_ban.get("name") or mai_hoa_data.get("ten_que") or omni_data.get("ten_que_ban") or "Quẻ Chủ"
        ten_que_bien = lh_bien.get("name") or mai_hoa_data.get("ten_qua_bien") or omni_data.get("ten_que_bien") or "Quẻ Biến"
        dong_list = luc_hao_data.get("dong_hao") or lh_ban.get("dong_hao") or []

        the_idx = 3
        the_hao = {}
        ung_idx = 6
        ung_hao = {}
        pm_idx = 2
        pm_hao = {}
        hd_count = 0
        hd_haos = []
        pm_haos = []
        tt_haos = []

        for idx, h in enumerate(haos, 1):
            if not isinstance(h, dict):
                continue
            tu = str(h.get("the_ung") or h.get("tu") or "")
            lt = str(h.get("luc_than") or "")
            if "Thế" in tu:
                the_idx = idx
                the_hao = h
            elif "Ứng" in tu:
                ung_idx = idx
                ung_hao = h
            if "Phụ Mẫu" in lt:
                pm_idx = idx
                pm_hao = h
                pm_haos.append((idx, h))
            if "Huynh Đệ" in lt:
                hd_count += 1
                hd_haos.append((idx, h))
            if "Tử Tôn" in lt:
                tt_haos.append((idx, h))

        c_info = omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}
        huong_cung = c_info.get("huong", "Chính Nam")
        target_cung = omni_data.get("target_cung", 3)
        sao_name = omni_data.get("sao_name", "Thiên Tâm")
        cua_name = omni_data.get("cua_name", "Khai Môn")
        than_name = omni_data.get("than_name", "Trực Phù")
        hanh_dt = omni_data.get("hanh", "Mộc")
        colors_str = omni_data.get("colors", "Trắng, Xanh, Vàng")

        # ── 1. GIẢI MÃ: TÔI Ở NHÀ MẤY TẦNG / ĐANG Ở TẦNG MẤY / NHÀ CÓ MẤY PHÒNG ──
        if target == "HOUSE_FLOORS":
            # Tính số tầng nhà theo Quái số Mai Hoa + vị trí Hào Phụ Mẫu (Nhà) & Hào Thế (Người ở)
            QUAI_FLOOR_MAP = {
                "Khôn": (1, 2, "Nhà thấp tầng (1 – 2 tầng / nhà trệt kiên cố)"),
                "Cấn": (2, 3, "Nhà 2 – 3 tầng (kết cấu vững chãi như núi)"),
                "Khảm": (2, 3, "Nhà 2 – 3 tầng (hoặc có tầng lửng/hầm)"),
                "Chấn": (3, 4, "Nhà 3 – 4 tầng (vươn lên thẳng đứng)"),
                "Tốn": (3, 4, "Nhà 3 – 4 tầng (thoáng gió, nhiều cửa sổ)"),
                "Ly": (3, 4, "Nhà 3 – 4 tầng (sáng sủa, mặt tiền thoáng)"),
                "Đoài": (2, 3, "Nhà 2 – 3 tầng (thiết kế hiện đại)"),
                "Càn": (4, 5, "Nhà cao 4 – 5 tầng (hoặc tòa nhà/chung cư cao tầng)"),
            }
            quai_cung_name = c_info.get("quai", "Ly")
            mh_upper = str(mai_hoa_data.get("upper") or "")
            mh_lower = str(mai_hoa_data.get("lower") or "")
            mh_the = str(mai_hoa_data.get("the_quai") or mh_upper or quai_cung_name)
            mh_dung = str(mai_hoa_data.get("dung_quai") or mh_lower or quai_cung_name)
            mh_bien_dung = str(mai_hoa_data.get("bien_dung_quai") or "")
            pm_positions = [idx for idx, _ in pm_haos] if pm_haos else [pm_idx]
            is_bat_thuan = bool(mh_upper and mh_upper == mh_lower) or ("Thuần " in str(ten_que_chu))
            primary_quai = mh_the if mh_the in QUAI_FLOOR_MAP else (mh_upper if mh_upper in QUAI_FLOOR_MAP else quai_cung_name)
            # Xác định Thượng Quái & Hạ Quái từ tên quẻ
            base_f1, base_f2, desc_f = QUAI_FLOOR_MAP.get(primary_quai, (2, 3, "Nhà 2 – 3 tầng"))
            if primary_quai == "Khôn" and (mh_bien_dung in ("Chấn", "Cấn", "Khảm", "Ly") or max(pm_positions) >= 2):
                base_f1, base_f2 = 2, 3
            active_hao = dong_list[0] if dong_list else (pm_positions[0] if is_bat_thuan else the_idx)
            if max(pm_positions) <= 2 and (not dong_list or max(dong_list) <= 2) and primary_quai in ("Khôn", "Cấn", "Khảm", "Đoài"):
                floor_main = f"NHÀ {base_f1} – {base_f2} TẦNG (ỨNG MẠNH NHẤT: NHÀ {base_f1} TẦNG HOẶC {base_f2} TẦNG / 1 TRỆT {base_f1} LẦU)"
                cur_floor = f"Tầng 1 (Tầng trệt — ứng Hào {active_hao}) hoặc Tầng 2 (Chính Trạch — Hào Phụ Mẫu tại Hào {pm_positions[0]})"
            elif (not is_bat_thuan) and the_idx in (5, 6) and primary_quai == "Càn":
                floor_main = f"NHÀ CAO {base_f1} – {base_f2} TẦNG (HOẶC TÒA NHÀ / CHUNG CƯ)"
                cur_floor = f"Tầng {base_f1} – {base_f2} (hoặc Tầng {the_idx - 1}–{the_idx} nếu ở chung cư)"
            else:
                floor_main = locals().get("floor_main", "")
                cur_f_low = min(max(1, active_hao), base_f1)
                floor_main = f"NHÀ {base_f1} – {base_f2} TẦNG (ỨNG MẠNH: NHÀ {base_f1} TẦNG HOẶC {base_f2} TẦNG)"
                cur_f_high = min(max(cur_f_low + 1, pm_positions[0]), base_f2)
                cur_floor = f"Tầng {cur_f_low} hoặc Tầng {cur_f_high}"
            if False and the_idx in (1, 2) and pm_idx in (1, 2) and not dong_list:
                floor_main = "NHÀ 1 – 2 TẦNG (NHÀ TRỆT HOẶC NHÀ 2 TẦNG)"
                cur_floor = "Tầng 1 (Tầng trệt)" if the_idx == 1 else "Tầng 1 hoặc Tầng 2"
            elif False and the_idx in (5, 6):
                extra_txt = "TÒA NHÀ / CHUNG CƯ CAO TẦNG" if base_f2 >= 5 else f"NHÀ {base_f2} – 5 TẦNG / CHUNG CƯ"
                floor_main = f"NHÀ {base_f1} – {base_f2} TẦNG (HOẶC {extra_txt})"
                cur_floor = f"Tầng {base_f1} – {base_f2}"
                pass
            else:
                floor_main = locals().get("floor_main", "")
                pass
                pass

            if any(w in q_low for w in ["mấy phòng", "bao nhiêu phòng"]):
                room_n1 = max(2, int(target_cung) if str(target_cung).isdigit() else 3)
                room_n2 = room_n1 + 2
                headline = f"🏠 KẾT LUẬN TỪ QUẺ GIA TRẠCH: NGÔI NHÀ CÓ KHOẢNG {room_n1} – {room_n2} PHÒNG CHÍNH (KẾT CẤU {floor_main})!"
            elif any(w in q_low for w in ["đang ở tầng mấy", "ngồi ở tầng mấy", "phòng ở tầng mấy"]):
                headline = f"🏠 KẾT LUẬN TỪ QUẺ GIA TRẠCH: HIỆN TẠI BẠN ĐANG Ở {cur_floor.upper()} (TRONG {floor_main})!"
            else:
                headline = f"🏠 KẾT LUẬN TỪ QUẺ GIA TRẠCH ({ten_que_chu.upper()}): BẠN ĐANG Ở {floor_main} — VỊ TRÍ SINH HOẠT CHÍNH ỨNG VỚI {cur_floor.upper()}!"

            pm_desc = (
                f"Hào <b>Phụ Mẫu</b> (Dụng Thần đại diện cho Ngôi nhà/Gia trạch) tại Hào {pm_idx} ({pm_hao.get('chi', '')}-{pm_hao.get('ngu_hanh', hanh_dt)})"
                if pm_hao else f"Dụng Thần <b>Phụ Mẫu</b> (Gia trạch hành {hanh_dt}) ẩn phục dưới Hào {the_idx}"
            )
            why_s = (
                f"Xét theo Pháp Gia Trạch Lục Hào & Mai Hoa Dịch Số: Quẻ lập được là <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>. "
                f"{pm_desc}, kết hợp <b>Hào Thế</b> (bản thân bạn) đóng tại <b>Hào {the_idx}</b> ({the_hao.get('chi', '')}-{the_hao.get('ngu_hanh', '')}) "
                f"và Cung Gia Trạch tại <b>Cung {target_cung} ({quai_cung_name} — {huong_cung})</b> hội Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b> "
                f"➔ Khẳng định ngôi nhà mang kết cấu <b>{floor_main.lower()}</b> (nếu tính cả tầng tum/mái hoặc gác lửng là +1 tầng) và vị trí bạn đang ngồi ứng với <b>{cur_floor}</b>."
            )
            when_s = (
                f"<b>Đặc điểm nhận diện ngôi nhà ({huong_cung}):</b> Tông màu tường/cửa chủ đạo có sắc <b>{colors_str}</b>; "
                f"không gian quanh nhà có đặc trưng của <b>{c_info.get('places', 'khu dân cư yên tĩnh')}</b>."
            )
            adv_s = (
                f"Phong thủy Gia Trạch tại Cung {target_cung} ({cua_name} · {than_name}): Giữ thông thoáng khu vực <b>{cur_floor}</b> "
                f"và hướng <b>{huong_cung}</b> để tụ khí vượng tài."
            )
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 2. GIẢI MÃ: NHÀ TÔI CÓ MẤY ANH CHỊ EM / CON THỨ MẤY TRONG NHÀ ──
        if target == "SIBLINGS_COUNT":
            sib_min = max(2, hd_count + 1)
            sib_max = sib_min + 1
            is_elder = (the_idx in (5, 6, 3)) or (str(the_hao.get("chi", "")) in ("Tý", "Dần", "Thìn", "Ngọ", "Thân", "Tuất"))
            order_str = "CON TRƯỞNG / ANH CHỊ ĐẦU (HOẶC THỨ 2)" if is_elder else "CON THỨ / CON ÚT TRONG GIA ĐÌNH"
            headline = f"👨‍👩‍👧‍👦 KẾT LUẬN TỪ QUẺ HUYNH ĐỆ: GIA ĐÌNH BẠN CÓ KHOẢNG {sib_min} – {sib_max} ANH CHỊ EM — BẠN ỨNG VỚI VỊ TRÍ {order_str}!"
            why_s = (
                f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, hào <b>Huynh Đệ</b> (Anh chị em) xuất hiện {hd_count} hào trên quẻ chính "
                f"kết hợp Quái số Cung {target_cung} ({huong_cung}) cho ra tổng số <b>{sib_min} – {sib_max} anh chị em</b>; "
                f"Hào Thế tại Hào {the_idx} mang khí {'Dương/Thượng vị' if is_elder else 'Âm/Hạ vị'} ứng với vai <b>{order_str.lower()}</b>."
            )
            when_s = f"Mối quan hệ anh chị em trong nhà: Tuy mỗi người một tính cách nhưng khi hữu sự vẫn hỗ trợ nhau tốt (Sao {sao_name} · Cửa {cua_name})."
            adv_s = f"Giữ sự hòa thuận, tương trợ lẫn nhau theo phương vị <b>{huong_cung}</b>."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 3. GIẢI MÃ: XUNG QUANH / TRONG PHÒNG CÓ MẤY NGƯỜI ──
        if target == "PEOPLE_AROUND":
            if is_fake or any(m in cua_name for m in ["Tử", "Đỗ", "Hưu"]) and not dong_list:
                headline = "👤 KẾT LUẬN TỪ QUẺ: HIỆN TẠI BẠN ĐANG Ở MỘT MÌNH TRONG PHÒNG (KHÔNG CÓ NGƯỜI LẠ BÊN CẠNH)!"
                why_s = f"Hào Thế tại Hào {the_idx} an tĩnh, Cung Bản Mệnh lâm cửa tĩnh <b>{cua_name}</b> — báo hiệu không gian riêng tư, bạn đang ngồi một mình."
            else:
                p_cnt = max(1, len(dong_list) + 1)
                headline = f"👥 KẾT LUẬN TỪ QUẺ: QUANH KHU VỰC BẠN ĐANG Ở CÓ KHOẢNG {p_cnt} – {p_cnt + 1} NGƯỜI (TÍNH CẢ BẠN HOẶC NGƯỜI TRONG NHÀ)!"
                why_s = f"Quẻ <b>{ten_que_chu}</b> có {len(dong_list)} hào động tương tác với Hào Thế tại Cung {target_cung} ({cua_name} · {sao_name})."
            when_s = f"Hướng không gian xung quanh bạn: <b>{huong_cung}</b> ({c_info.get('places', '')})."
            adv_s = f"Đồ vật gần bạn nhất: <b>{omni_data.get('objects', 'Điện thoại, bàn ghế')}</b>."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 4. GIẢI MÃ: ĐÃ KẾT HÔN CHƯA / CÓ VỢ CHỒNG CHƯA / ĐỘC THÂN HAY CÓ GIA ĐÌNH ──
        if target == "MARITAL_STATUS_NOW":
            if is_fake or ("Tuần Không" in str(auth_warnings)):
                headline = "💫 KẾT LUẬN TỪ QUẺ: HIỆN TẠI BẠN CHƯA KẾT HÔN / ĐANG ĐỘC THÂN (HOẶC ĐANG SỐNG ĐỘC LẬP)!"
                why_s = (
                    f"Hào Dụng Thần Phối Ngẫu (<b>{dung_than}</b>) rơi vào <b>Tuần Không / Không Vong</b> trên quẻ <b>{ten_que_chu}</b> — "
                    f"chứng tỏ vị trí hôn nhân/phối ngẫu hiện đang trống, bạn chưa lập gia đình hoặc đang độc thân."
                )
            else:
                headline = "💍 KẾT LUẬN TỪ QUẺ: BẠN ĐÃ CÓ NGƯỜI THƯƠNG / ĐÃ LẬP GIA ĐÌNH (CÓ MỐI QUAN HỆ GẮN BÓ)!"
                why_s = (
                    f"Trục <b>Hào Thế (Hào {the_idx}) – Hào Ứng (Hào {ung_idx})</b> và Dụng Thần <b>{dung_than}</b> hữu khí trên quẻ <b>{ten_que_chu}</b>, "
                    f"hội Cửa <b>{cua_name}</b> và Thần <b>{than_name}</b> — báo hiệu đã có nhân duyên/gia thất thực tế."
                )
            when_s = f"Mốc vượng nhân duyên / gia đạo: <b>{omni_data.get('exact_timestamp', 'Trong năm nay')}</b>."
            adv_s = f"Phương vị kích hoạt đào hoa & hòa hợp gia đạo: <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 5. GIẢI MÃ: MẶC ÁO MÀU GÌ / ĐI XE GÌ, MÀU GÌ / BIỂN SỐ XE MẤY ──
        if target == "CLOTHING_VEHICLE":
            qty_str = omni_data.get("quantity", "3, 4, 9")
            if "xe" in q_low or "biển số" in q_low:
                headline = f"🛵 KẾT LUẬN TỪ QUẺ PHỤ MẪU: XE CỦA BẠN MANG TÔNG MÀU {colors_str.upper()} — CHỮ SỐ ĐUÔI BIỂN SỐ / ĐỊNH LƯỢNG ỨNG VỚI: {qty_str.upper()}!"
                why_s = (
                    f"Xét Hào <b>Phụ Mẫu</b> (Phương tiện/Biển số) tại Hào {pm_idx} và Hào Thế tại Hào {the_idx} trên quẻ <b>{ten_que_chu}</b>: "
                    f"Ngũ hành <b>{hanh_dt}</b> tại Cung {target_cung} ({huong_cung}) chỉ định rõ màu xe thuộc nhóm <b>{colors_str}</b>."
                )
            else:
                headline = f"👕 KẾT LUẬN TỪ QUẺ: TRANG PHỤC / MÀU SẮC HIỆN TẠI CỦA BẠN MANG TÔNG MÀU {colors_str.upper()} (HÀNH {hanh_dt.upper()})!"
                why_s = (
                    f"Xét Hào <b>Phụ Mẫu</b> (Quần áo/Trang phục) và <b>Hào Thế</b> (cơ thể bạn) tại Hào {the_idx} trên quẻ <b>{ten_que_chu}</b>: "
                    f"Khí Ngũ hành <b>{hanh_dt}</b> hội Sao <b>{sao_name}</b> phản ánh rõ sắc màu <b>{colors_str}</b>."
                )
            when_s = f"Chất liệu & Kiểu dáng: <b>{omni_data.get('material', 'Vải/Kim loại bền đẹp')}</b> ({omni_data.get('shape', 'Cân đối')})."
            adv_s = f"Bộ số may mắn đi kèm: <b>{qty_str}</b> | Hướng cát lợi: <b>{huong_cung}</b>."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 6. GIẢI MÃ CHUYÊN SÂU: ĐỘ TUỔI CON GÁI & CON TRAI / CÁC CON (LIÊN KẾT ĐA HỆ THỐNG LỤC HÀO · MAI HOA · KỲ MÔN · THIẾT BẢN) ──
        if target == "CHILDREN_AGE":
            headline = omni_data.get("children_age_headline") or (
                f"👧👦 KẾT LUẬN TỪ LIÊN KẾT ĐA TẦNG QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                f"BẠN ĐANG CÓ 2 NGƯỜI CON THẬT NGOÀI ĐỜI (CÓ CON GÁI & CON TRAI) — "
                f"CON GÁI ỨNG KHOẢNG 2–4 TUỔI HOẶC 7–9 TUỔI (LỚN: 12–15 TUỔI) | CON TRAI ỨNG KHOẢNG 3–6 TUỔI HOẶC 8–10 TUỔI (LỚN: 11–14 TUỔI)!"
            )
            why_s = omni_data.get("children_age_why") or (
                f"Liên kết Lục Hào (Hào Tử Tôn hữu khí/được Hào Động sinh trợ), Mai Hoa Dịch Số (Quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>) "
                f"và Kỳ Môn Cung {target_cung} ({huong_cung}) khẳng định bạn có con thật ngoài đời (bác bỏ Chân Không) và tính chính xác khung tuổi từ Quái số Âm/Dương."
            )
            when_s = omni_data.get("children_age_when") or f"Các năm sinh Địa Chi ứng mạnh nhất theo Hào Tử Tôn và Hào Động tại hướng <b>{huong_cung}</b>."
            adv_s = omni_data.get("children_age_advice") or f"Bồi đắp phúc khí cho các con theo hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 7. GIẢI MÃ CHUYÊN SÂU: SỐ LƯỢNG CON CÁI / MẤY TRAI MẤY GÁI (LIÊN KẾT ĐA HỆ THỐNG) ──
        if target == "CHILDREN_COUNT":
            headline = omni_data.get("children_summary") or "👶 KẾT LUẬN TỪ QUẺ: BẠN CÓ KHOẢNG 2 NGƯỜI CON — GỒM 1 CON TRAI VÀ 1 CON GÁI (ĐỦ CẢ NẾP LẪN TẺ)!"
            why_s = omni_data.get("children_reasons") or f"Xác định từ Hào Tử Tôn trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> và Cung Tử Tức tại Cung {target_cung}."
            when_s = omni_data.get("children_traits") or f"Cung Tử Tức hội Sao <b>{sao_name}</b> và Cửa <b>{cua_name}</b> tại hướng <b>{huong_cung}</b>."
            adv_s = omni_data.get("children_advice") or f"Phương vị tốt cho con cái: <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8. GIẢI MÃ CHUYÊN SÂU: GIỚI TÍNH & ĐỘ TUỔI / NĂM SINH CỦA NGƯỜI BẤT KỲ ──
        if target == "GENDER_AGE":
            _g_lbl = omni_data.get("gender", "NAM GIỚI / ĐÀN ÔNG")
            _a_lbl = omni_data.get("age_tier", "THANH NIÊN / TRUNG NIÊN TRẺ")
            _by_lst = ", ".join(omni_data.get("birth_years", [])[:3])
            headline = f"👤 KẾT LUẬN ĐỊNH DANH & ĐỘ TUỔI TỪ QUẺ ({ten_que_chu.upper()}): {_g_lbl} — {_a_lbl} (ỨNG NĂM SINH: {_by_lst.upper()})!"
            why_s = (
                f"Xét Dụng Thần <b>{dung_than}</b> (Hành <b>{hanh_dt}</b>) trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> "
                f"kết hợp Cung {target_cung} ({huong_cung} · Sao {sao_name} · Cửa {cua_name}): {omni_data.get('gender_reasons', 'Khí số hội tụ rõ nét')}."
            )
            when_s = f"Các mốc năm sinh & độ tuổi khớp nhất với hào vị và Quái số Tiên/Hậu Thiên: <b>{_by_lst}</b>."
            adv_s = f"Đặc điểm ngoại hình & tính cách: {omni_data.get('appearance', '')} (Hướng ứng: <b>{huong_cung}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        return {"has_override": False}

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

        # Kiểm tra xem Con AI Số 2 có bộ giải mã chuyên biệt cho câu hỏi này không
        spec_res = HexagramReasoningAI.deduce_specialized_answer(
            blueprint=blueprint,
            dung_than=dung_than,
            weighted_pct=weighted_pct,
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            auth_warnings=auth_warnings,
            is_fake=is_fake,
        )

        headline_ans = spec_res.get("headline") or omni_data.get("binary_verdict_headline", "")
        why_proof = spec_res.get("why") or omni_data.get("binary_why_reasons", "")
        when_proof = spec_res.get("when") or omni_data.get("binary_when_note", "")
        advice_proof = spec_res.get("advice") or omni_data.get("binary_action_advice", "")

        if not headline_ans and narrative_summary:
            m_ans = re.search(r"👉\s*(.+?)</div>", narrative_summary)
            if m_ans:
                headline_ans = re.sub(r"<[^>]+>", "", m_ans.group(1)).strip()
            else:
                m_ans2 = re.search(r"📢\s*\*\*CÂU TRẢ LỜI:\*\*\s*(.+?)(?:\n|$)", narrative_summary)
                if m_ans2:
                    headline_ans = re.sub(r"<[^>]+>", "", m_ans2.group(1)).strip()

        if not why_proof and narrative_summary:
            m_why = re.search(r"🔍 NGUYÊN NHÂN CỐT LÕI</div><div[^>]*>(.+?)</div>", narrative_summary)
            if m_why:
                why_proof = m_why.group(1).strip()

        tu_tru_str = f"Năm {can_y} {chi_y} · Tháng {can_m} {chi_m} · Ngày {can_n} {chi_n} · Giờ {can_g} {chi_g}".strip(" ·")
        dong_str = f"Động hào {', '.join(map(str, dong_hao_list))}" if dong_hao_list else "Quẻ Tĩnh (6 hào an tĩnh)"

        if is_fake and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Tuần Không / Tử Môn</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Quẻ dùng phép <b>Loại Trừ Nhị Phân</b>: Bác bỏ hoàn toàn phương án bị Không Vong để khẳng định 100% phương án thực tế còn lại!"
            )
        elif is_fake and blueprint.get("specific_target") not in ("HOUSE_FLOORS", "CLOTHING_VEHICLE", "SIBLINGS_COUNT", "CHILDREN_AGE", "CHILDREN_COUNT"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Chân Không / Không Vong Vô Khí</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Cảnh báo sự việc/đối tượng đang hỏi hiện <b>chưa tồn tại ngoài thực tế (= 0)</b> hoặc là câu hỏi thử lòng quẻ."
            )
        elif auth_warnings and not is_fake:
            auth_status_str = (
                f"<b>Liên kết sâu Lục Hào – Mai Hoa – Kỳ Môn:</b> Hào Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> hoàn toàn hữu khí / được Hào Động sinh trợ "
                f"khẳng định <b>đối tượng/con cái bạn hỏi LÀ CÓ THẬT 100% NGOÀI ĐỜI (bác bỏ Chân Không)</b>; còn dấu hiệu Tuần Không ở Nhật Can bắt bài bạn đang <b>đặt câu hỏi để thử độ nhạy bén của quẻ</b>!"
            )
        else:
            auth_status_str = (
                f"Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> đối chứng trực tiếp trên quẻ ({ts_stage}), khớp chính xác vào câu hỏi."
            )

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
            f'<div style="font-size:1.06em;font-weight:900;color:#38bdf8;letter-spacing:0.3px;">🤖 HỆ THỐNG SONG NÃO AI 2 TẦNG (V101.6): AI ĐỌC HIỂU CÂU HỎI ➔ AI ĐỐI CHỨNG QUẺ & SUY LUẬN</div>'
            f'<span style="background:rgba(56,189,248,0.18);color:#7dd3fc;padding:3px 10px;border-radius:12px;font-size:0.82em;font-weight:800;border:1px solid #38bdf8;">Khớp {blueprint["archetype_code"]}/25 Đại Dạng Toàn Cầu</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;">'
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #38bdf8;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#7dd3fc;margin-bottom:6px;">🧠 AI SỐ 1 — CHUYÊN ĐỌC & THẤU HIỂU CÂU HỎI</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Nhận diện dạng câu hỏi:</b> <span style="color:#fde047;font-weight:800;">{blueprint["archetype_code"]} — {blueprint["archetype_name"]}</span><br>'
            f'• <b>Đối tượng trọng tâm:</b> {blueprint["subject_person"]} (Giao Dụng Thần: <b>{dung_than}</b>){sub_intents_html}<br>'
            f'• <b>Chỉ thị tra quẻ cho AI Số 2:</b> <i>{blueprint["lh_dt_instruction"]}</i>'
            f'{ab_html}'
            f'</div></div>'
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #fbbf24;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#fde047;margin-bottom:6px;">🔮 AI SỐ 2 — CHUYÊN ĐỐI CHỨNG QUẺ & SUY LUẬN ĐÁP ÁN</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Quẻ lập đúng thời khắc ({tu_tru_str}):</b> Quẻ <b>{ten_que_chu}</b> ➔ <b>{ten_que_bien}</b> ({dong_str}) · Kỳ Môn Cục {cuc_km} ({don_type}, Cung {target_cung} {huong_cung}: Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b>, Thần <b>{than_name}</b>)<br>'
            f'• <b>Kết quả đối chứng Thực/Hư:</b> {auth_status_str}<br>'
            f'• <b>Đáp án suy luận khớp quẻ:</b> <span style="color:#4ade80;font-weight:900;">{headline_ans or "Đã khớp toàn bộ 18 tầng quẻ"}</span>'
            f'</div></div>'
            f'</div></div>'
        )

        online_directive = (
            f"=== HỒ SƠ BÀN GIAO TỪ HỆ THỐNG SONG NÃO AI 2 TẦNG (BẮT BUỘC TUÂN THỦ 100%) ===\n"
            f"1. [AI SỐ 1 - ĐỌC CÂU HỎI]:\n"
            f"   - Câu hỏi thuộc: {blueprint['archetype_code']} ({blueprint['archetype_name']})\n"
            f"   - Đối tượng: {blueprint['subject_person']} | Dụng Thần: {dung_than} (Hành {hanh_dt})\n"
            f"   - Quy tắc trả lời bắt buộc: {blueprint['answer_rule']}\n"
            f"2. [AI SỐ 2 - ĐỐI CHỨNG QUẺ ({tu_tru_str})]:\n"
            f"   - Lục Hào & Mai Hoa: Quẻ {ten_que_chu} biến {ten_que_bien} ({dong_str})\n"
            f"   - Kỳ Môn Độn Giáp: Cung {target_cung} ({huong_cung}) hội Sao {sao_name}, Cửa {cua_name}, Thần {than_name}\n"
            f"   - ĐÁP ÁN ĐỐI CHỨNG CHỐT HẠ (TUYỆT ĐỐI KHÔNG ĐƯỢC SỬA ĐỔI HAY BỊA KHÁC ĐI): {headline_ans}\n"
            f"   - Căn cứ suy luận: {re.sub(r'<[^>]+>', '', why_proof)}\n"
        )

        return {
            "blueprint": blueprint,
            "has_specialized_override": bool(spec_res.get("has_override")),
            "verified_headline": headline_ans,
            "verified_why": why_proof,
            "verified_when": when_proof,
            "verified_advice": advice_proof,
            "dual_agent_html": dual_agent_html,
            "online_directive": online_directive,
        }

"""
CHART INTERPRETER AI - Siêu Thông Minh
Luận giải bàn Kỳ Môn Độn Giáp với độ chính xác cao
- Quá khứ: Đã xảy ra gì?
- Hiện tại: Đang diễn ra như nào?
- Tương lai: Sẽ xảy ra gì? Khi nào? Bao nhiêu?
"""

import json
from datetime import datetime, timedelta

# Ngũ Hành sinh khắc
NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
NGU_HANH_BI_KHAC = {"Mộc": "Kim", "Kim": "Hỏa", "Hỏa": "Thủy", "Thủy": "Thổ", "Thổ": "Mộc"}

# Cung số -> Ngũ Hành
CUNG_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}

# Sao tính chất
SAO_CAT = ["Thiên Tâm", "Thiên Phụ", "Thiên Cầm", "Thiên Nhậm"]
SAO_HUNG = ["Thiên Bồng", "Thiên Nhuế", "Thiên Trụ", "Thiên Anh"]
SAO_BINH = ["Thiên Xung"]

# Môn tính chất
MON_CAT = ["Khai Môn", "Hưu Môn", "Sinh Môn"]
MON_HUNG = ["Tử Môn", "Kinh Môn", "Thương Môn"]
MON_BINH = ["Đỗ Môn", "Cảnh Môn"]

# Thần tính chất
THAN_CAT = ["Cửu Địa", "Cửu Thiên", "Trực Phù"]
THAN_HUNG = ["Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
THAN_BINH = ["Lục Hợp", "Thái Âm", "Câu Trần"]


class ChartInterpreterAI:
    """
    AI Siêu Thông Minh luận giải bàn Kỳ Môn Độn Giáp
    Trả lời chính xác: Quá khứ, Hiện tại, Tương lai, Số lượng, Thời gian
    """
    
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper
        self.interpretation_rules = self._load_rules()
    
    def _load_rules(self):
        """Load luận giải rules từ database"""
        return {
            # Thời gian dựa trên Môn
            "time_indicators": {
                "Khai Môn": {"speed": "nhanh", "days": "3-7 ngày"},
                "Hưu Môn": {"speed": "chậm", "days": "1-2 tháng"},
                "Sinh Môn": {"speed": "trung bình", "days": "2-4 tuần"},
                "Thương Môn": {"speed": "gấp", "days": "1-3 ngày"},
                "Đỗ Môn": {"speed": "trì hoãn", "days": "3-6 tháng"},
                "Cảnh Môn": {"speed": "bất ngờ", "days": "7-14 ngày"},
                "Tử Môn": {"speed": "không xảy ra", "days": "N/A"},
                "Kinh Môn": {"speed": "đột ngột", "days": "1-5 ngày"}
            },
            # Số lượng dựa trên Cung số
            "quantity_base": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9},
            # Hệ số nhân dựa trên Sao
            "quantity_multiplier": {
                "Thiên Tâm": 10, "Thiên Phụ": 8, "Thiên Nhậm": 7,
                "Thiên Cầm": 5, "Thiên Xung": 3, "Thiên Bồng": 1,
                "Thiên Nhuế": 0.5, "Thiên Trụ": 2, "Thiên Anh": 1.5
            }
        }
    
    def analyze_timeline(self, chart_data, topic):
        """
        Phân tích timeline: Quá khứ - Hiện tại - Tương lai
        """
        # Xác định cung Dụng Thần (mục tiêu)
        dung_than_palace = self._find_dung_than_palace(chart_data, topic)
        
        # Xác định cung Bản Thân
        ban_than_palace = self._find_ban_than_palace(chart_data)
        
        # Lấy thông tin chi tiết
        dung_info = self._get_palace_info(chart_data, dung_than_palace)
        ban_info = self._get_palace_info(chart_data, ban_than_palace)
        
        # Phân tích quan hệ
        relationship = self._analyze_relationship(ban_info, dung_info)
        
        # Tính thời gian
        timing = self._calculate_timing(dung_info, chart_data)
        
        # Tính xác suất
        probability = self._calculate_probability(dung_info, ban_info, relationship)
        
        # Tính số lượng
        quantity = self._calculate_quantity(dung_info, chart_data)
        
        return {
            "qua_khu": self._interpret_past(chart_data, topic, dung_info),
            "hien_tai": self._interpret_present(chart_data, topic, dung_info, ban_info),
            "tuong_lai": self._interpret_future(chart_data, topic, dung_info, relationship, timing),
            "thoi_gian": timing,
            "xac_suat": probability,
            "so_luong": quantity,
            "chi_tiet": {
                "cung_dung_than": dung_than_palace,
                "cung_ban_than": ban_than_palace,
                "quan_he": relationship
            }
        }
    
    def _find_dung_than_palace(self, chart_data, topic):
        """Tìm cung Dụng Thần dựa trên chủ đề"""
        topic_lower = topic.lower()
        
        # Mapping chủ đề -> Môn/Sao
        topic_mapping = {
            # Tiền bạc, tài chính
            "tiền": ["Sinh Môn", "Thiên Phụ"],
            "tài": ["Sinh Môn", "Thiên Phụ"],
            "lương": ["Sinh Môn"],
            "đầu tư": ["Sinh Môn", "Khai Môn"],
            
            # Công việc
            "công việc": ["Khai Môn", "Thiên Tâm"],
            "sự nghiệp": ["Khai Môn"],
            "thăng tiến": ["Khai Môn", "Cửu Thiên"],
            
            # Tình cảm
            "tình": ["Lục Hợp", "Hưu Môn"],
            "yêu": ["Lục Hợp", "Cảnh Môn"],
            "hôn nhân": ["Lục Hợp", "Thái Âm"],
            
            # Sức khỏe
            "bệnh": ["Thiên Tâm", "Tử Môn"],
            "sức khỏe": ["Thiên Tâm"],
            
            # Kiện tụng
            "kiện": ["Kinh Môn", "Bạch Hổ"],
            "tranh chấp": ["Kinh Môn"],
            
            # Di chuyển
            "đi": ["Mã Tinh", "Thiên Xung"],
            "xuất hành": ["Khai Môn", "Mã Tinh"]
        }
        
        target_elements = []
        for key, elements in topic_mapping.items():
            if key in topic_lower:
                target_elements.extend(elements)
        
        # Tìm cung chứa yếu tố Dụng Thần
        if target_elements:
            for palace_num in range(1, 10):
                mon = chart_data.get('nhan_ban', {}).get(palace_num, '')
                sao = chart_data.get('thien_ban', {}).get(palace_num, '')
                than = chart_data.get('than_ban', {}).get(palace_num, '')
                
                for elem in target_elements:
                    if elem in [mon, sao, than] or elem in mon:
                        return palace_num
        
        # Mặc định: Cung có Can Giờ
        can_gio = chart_data.get('can_gio', '')
        for palace_num in range(1, 10):
            if chart_data.get('can_thien_ban', {}).get(palace_num) == can_gio:
                return palace_num
        
        return 5  # Trung cung mặc định
    
    def _find_ban_than_palace(self, chart_data):
        """Tìm cung Bản Thân (Can Ngày)"""
        can_ngay = chart_data.get('can_ngay', '')
        for palace_num in range(1, 10):
            if chart_data.get('can_thien_ban', {}).get(palace_num) == can_ngay:
                return palace_num
        return 1
    
    def _get_palace_info(self, chart_data, palace_num):
        """Lấy thông tin đầy đủ của một cung (hỗ trợ cả key int và str)"""
        tb = chart_data.get('thien_ban', {}) or {}
        nb = chart_data.get('nhan_ban', {}) or {}
        sb = chart_data.get('than_ban', {}) or {}
        ctb = chart_data.get('can_thien_ban', {}) or {}
        cdb = chart_data.get('dia_ban') or chart_data.get('dia_can', {}) or {}
        return {
            "num": palace_num,
            "sao": str(tb.get(palace_num, tb.get(str(palace_num), 'Thiên Cầm'))),
            "mon": str(nb.get(palace_num, nb.get(str(palace_num), 'Đỗ Môn'))),
            "than": str(sb.get(palace_num, sb.get(str(palace_num), 'Trực Phù'))),
            "can_thien": str(ctb.get(palace_num, ctb.get(str(palace_num), 'Mậu'))),
            "can_dia": str(cdb.get(palace_num, cdb.get(str(palace_num), 'Mậu'))),
            "hanh": CUNG_HANH.get(palace_num, 'Thổ'),
            "khong_vong": palace_num in (chart_data.get('khong_vong') or []),
            "dich_ma": palace_num == chart_data.get('dich_ma', 0)
        }
    
    def _analyze_relationship(self, ban_info, dung_info):
        """Phân tích quan hệ sinh khắc giữa Bản Thân và Dụng Thần"""
        ban_hanh = ban_info["hanh"]
        dung_hanh = dung_info["hanh"]
        
        if NGU_HANH_SINH.get(dung_hanh) == ban_hanh:
            return {"type": "dung_sinh_ban", "meaning": "Dụng Thần sinh Bản Thân", "score": 90, "verdict": "ĐẠI CÁT"}
        elif NGU_HANH_SINH.get(ban_hanh) == dung_hanh:
            return {"type": "ban_sinh_dung", "meaning": "Bản Thân sinh Dụng Thần (hao tốn)", "score": 40, "verdict": "PHÍ SỨC"}
        elif NGU_HANH_KHAC.get(ban_hanh) == dung_hanh:
            return {"type": "ban_khac_dung", "meaning": "Bản Thân khắc Dụng Thần", "score": 70, "verdict": "CÁT"}
        elif NGU_HANH_BI_KHAC.get(ban_hanh) == dung_hanh:
            return {"type": "dung_khac_ban", "meaning": "Dụng Thần khắc Bản Thân", "score": 20, "verdict": "HUNG"}
        else:
            return {"type": "hoa", "meaning": "Ngũ hành ngang nhau", "score": 50, "verdict": "BÌNH"}
    
    def _calculate_timing(self, dung_info, chart_data):
        """Tính toán thời gian xảy ra sự việc"""
        mon = dung_info["mon"]
        base_timing = self.interpretation_rules["time_indicators"].get(
            mon.replace(" Môn", "") + " Môn", 
            {"speed": "trung bình", "days": "2-4 tuần"}
        )
        
        # Điều chỉnh theo Không Vong
        if dung_info["khong_vong"]:
            return {
                "speed": "trì hoãn hoặc không thành",
                "days": "Không xác định",
                "note": "Cung rơi vào Không Vong - Sự việc bế tắc hoặc chưa tới lúc"
            }
        
        # Điều chỉnh theo Dịch Mã
        if dung_info["dich_ma"]:
            return {
                "speed": "rất nhanh",
                "days": "1-3 ngày",
                "note": "Có Dịch Mã - Sự việc chuyển động nhanh"
            }
        
        # Tính ngày cụ thể
        now = datetime.now()
        cung_num = dung_info["num"]
        
        # Ngày ứng kỳ dựa trên số cung
        ngay_ung = now + timedelta(days=cung_num)
        
        return {
            "speed": base_timing["speed"],
            "days": base_timing["days"],
            "ngay_ung": ngay_ung.strftime("%d/%m/%Y"),
            "note": f"Dựa trên {mon}"
        }
    
    def _calculate_probability(self, dung_info, ban_info, relationship):
        """Tính xác suất thành công"""
        base_score = relationship["score"]
        
        # Điều chỉnh theo Sao
        sao = dung_info["sao"]
        if sao in SAO_CAT:
            base_score += 15
        elif sao in SAO_HUNG:
            base_score -= 20
        
        # Điều chỉnh theo Môn
        mon = dung_info["mon"]
        if any(m in mon for m in MON_CAT):
            base_score += 15
        elif any(m in mon for m in MON_HUNG):
            base_score -= 20
        
        # Điều chỉnh theo Thần
        than = dung_info["than"]
        if than in THAN_CAT:
            base_score += 10
        elif than in THAN_HUNG:
            base_score -= 15
        
        # Điều chỉnh theo Không Vong
        if dung_info["khong_vong"]:
            base_score -= 40
        
        # Giới hạn 0-100%
        base_score = max(0, min(100, base_score))
        
        return {
            "phan_tram": base_score,
            "danh_gia": self._score_to_verdict(base_score),
            "chi_tiet": f"Sao: {sao}, Môn: {mon}, Thần: {than}"
        }
    
    def _score_to_verdict(self, score):
        """Chuyển điểm thành đánh giá"""
        if score >= 80:
            return "RẤT TỐT - Khả năng cao thành công"
        elif score >= 60:
            return "TỐT - Thuận lợi, có thể đạt được"
        elif score >= 40:
            return "TRUNG BÌNH - Cần nỗ lực thêm"
        elif score >= 20:
            return "KHÓ KHĂN - Nhiều trở ngại"
        else:
            return "RẤT KHÓ - Nên xem xét lại"
    
    def _calculate_quantity(self, dung_info, chart_data):
        """Tính toán số lượng (tiền, người, vật...)"""
        cung_num = dung_info["num"]
        sao = dung_info["sao"]
        
        base = self.interpretation_rules["quantity_base"].get(cung_num, 5)
        multiplier = self.interpretation_rules["quantity_multiplier"].get(sao, 1)
        
        # Đơn vị tùy theo ngữ cảnh
        result = base * multiplier
        
        return {
            "so_co_ban": base,
            "he_so": multiplier,
            "ket_qua": result,
            "y_nghia": f"Con số liên quan: {int(result)} (đơn vị: triệu/người/tháng tùy ngữ cảnh)"
        }
    
    def _interpret_past(self, chart_data, topic, dung_info):
        """Luận giải quá khứ"""
        sao = dung_info["sao"]
        mon = dung_info["mon"]
        
        past_indicators = []
        
        # Phân tích Can Địa (quá khứ)
        can_dia = dung_info["can_dia"]
        if can_dia:
            past_indicators.append(f"Từ trước đến nay, sự việc liên quan đến '{topic}' đã có nền tảng từ {can_dia}")
        
        # Phân tích theo Thần (ảnh hưởng từ trước)
        than = dung_info["than"]
        if than in THAN_CAT:
            past_indicators.append("Trước đây đã có người/lực lượng hỗ trợ")
        elif than in THAN_HUNG:
            past_indicators.append("Trước đây đã gặp nhiều khó khăn, cản trở")
        
        return {
            "tom_tat": "Quá khứ có nền tảng" if dung_info["hanh"] in ["Thổ", "Kim"] else "Quá khứ còn nhiều biến động",
            "chi_tiet": past_indicators
        }
    
    def _interpret_present(self, chart_data, topic, dung_info, ban_info):
        """Luận giải hiện tại"""
        present_status = []
        
        # Trạng thái hiện tại dựa trên Môn
        mon = dung_info["mon"]
        if "Khai" in mon:
            present_status.append("Hiện tại đang có cơ hội mở ra, nên nắm bắt ngay")
        elif "Sinh" in mon:
            present_status.append("Hiện tại đang trong giai đoạn tích lũy, phát triển")
        elif "Hưu" in mon:
            present_status.append("Hiện tại đang trong giai đoạn nghỉ ngơi, chờ thời cơ")
        elif "Tử" in mon:
            present_status.append("Hiện tại đang bế tắc, cần thay đổi hướng đi")
        elif "Kinh" in mon:
            present_status.append("Hiện tại đang có áp lực, căng thẳng")
        elif "Thương" in mon:
            present_status.append("Hiện tại đang có xung đột, cần giải quyết gấp")
        elif "Đỗ" in mon:
            present_status.append("Hiện tại đang bị tắc nghẽn, cần kiên nhẫn")
        elif "Cảnh" in mon:
            present_status.append("Hiện tại đang rõ ràng, có thể nhìn thấy tình hình")
        
        # Trạng thái Không Vong
        if dung_info["khong_vong"]:
            present_status.append("⚠️ Cung Dụng Thần rơi Không Vong - Sự việc chưa định hình rõ")
        
        return {
            "tom_tat": "Đang có cơ hội" if any(m in mon for m in MON_CAT) else "Đang gặp khó khăn",
            "chi_tiet": present_status
        }
    
    def _interpret_future(self, chart_data, topic, dung_info, relationship, timing):
        """Luận giải tương lai"""
        future_prediction = []
        
        # Dự đoán dựa trên quan hệ sinh khắc
        verdict = relationship["verdict"]
        if verdict == "ĐẠI CÁT":
            future_prediction.append(f"✅ Sự việc '{topic}' SẼ THÀNH CÔNG với xác suất cao")
            future_prediction.append(f"⏰ Thời gian: {timing['days']}")
        elif verdict == "CÁT":
            future_prediction.append(f"✅ Sự việc '{topic}' có thể đạt được nhưng cần chủ động")
            future_prediction.append(f"⏰ Thời gian: {timing['days']}")
        elif verdict == "BÌNH":
            future_prediction.append(f"⚖️ Sự việc '{topic}' có thể thành hoặc bại tùy nỗ lực")
        elif verdict == "PHÍ SỨC":
            future_prediction.append(f"⚠️ Sự việc '{topic}' tốn nhiều công sức, kết quả không tương xứng")
        else:
            future_prediction.append(f"❌ Sự việc '{topic}' gặp nhiều trở ngại, khó thành")
        
        # Thêm ngày ứng kỳ
        if timing.get("ngay_ung"):
            future_prediction.append(f"📅 Ngày ứng kỳ: {timing['ngay_ung']}")
        
        return {
            "tom_tat": verdict,
            "chi_tiet": future_prediction,
            "khuyen_nghi": self._generate_advice(dung_info, relationship)
        }
    
    def _generate_advice(self, dung_info, relationship):
        """Tạo lời khuyên cụ thể"""
        advice = []
        
        verdict = relationship["verdict"]
        if verdict in ["ĐẠI CÁT", "CÁT"]:
            advice.append("👉 Nên tiến hành ngay, đừng chần chừ")
        elif verdict == "BÌNH":
            advice.append("👉 Cần chuẩn bị kỹ lưỡng trước khi hành động")
        else:
            advice.append("👉 Nên hoãn lại hoặc tìm phương án khác")
        
        # Lời khuyên theo Không Vong
        if dung_info["khong_vong"]:
            advice.append("⚠️ Sự việc chưa đến lúc, nên chờ thêm")
        
        # Lời khuyên theo Dịch Mã
        if dung_info["dich_ma"]:
            advice.append("🐎 Nên di chuyển, thay đổi vị trí sẽ có lợi")
        
        return advice
    
    def get_super_interpretation(self, chart_data, topic):
        """
        API chính: Lấy luận giải siêu thông minh
        Trả về tất cả thông tin chi tiết
        """
        analysis = self.analyze_timeline(chart_data, topic)
        
        # Format output dễ đọc
        output = []
        output.append(f"## 🔮 LUẬN GIẢI SIÊU CHI TIẾT: {topic.upper()}")
        output.append("")
        
        # Xác suất
        prob = analysis["xac_suat"]
        output.append(f"### 📊 XÁC SUẤT THÀNH CÔNG: {prob['phan_tram']}%")
        output.append(f"**Đánh giá:** {prob['danh_gia']}")
        output.append("")
        
        # Thời gian
        time = analysis["thoi_gian"]
        output.append("### ⏰ THỜI GIAN")
        output.append(f"- **Tốc độ:** {time['speed']}")
        output.append(f"- **Khoảng thời gian:** {time['days']}")
        if time.get('ngay_ung'):
            output.append(f"- **Ngày ứng kỳ:** {time['ngay_ung']}")
        if time.get('note'):
            output.append(f"- **Ghi chú:** {time['note']}")
        output.append("")
        
        # Số lượng
        qty = analysis["so_luong"]
        output.append("### 🔢 SỐ LƯỢNG")
        output.append(f"- **Con số liên quan:** {int(qty['ket_qua'])}")
        output.append(f"- {qty['y_nghia']}")
        output.append("")
        
        # Quá khứ
        past = analysis["qua_khu"]
        output.append("### ⏮️ QUÁ KHỨ")
        output.append(f"**{past['tom_tat']}**")
        for detail in past["chi_tiet"]:
            output.append(f"- {detail}")
        output.append("")
        
        # Hiện tại
        present = analysis["hien_tai"]
        output.append("### ⏸️ HIỆN TẠI")
        output.append(f"**{present['tom_tat']}**")
        for detail in present["chi_tiet"]:
            output.append(f"- {detail}")
        output.append("")
        
        # Tương lai
        future = analysis["tuong_lai"]
        output.append("### ⏭️ TƯƠNG LAI")
        output.append(f"**{future['tom_tat']}**")
        for detail in future["chi_tiet"]:
            output.append(f"- {detail}")
        output.append("")
        output.append("### 💡 LỜI KHUYÊN")
        for advice in future["khuyen_nghi"]:
            output.append(f"- {advice}")
        
        return "\n".join(output)


# Singleton instance
_interpreter = None

def get_chart_interpreter(gemini_helper=None):
    """Lấy instance của ChartInterpreterAI"""
    global _interpreter
    if _interpreter is None:
        _interpreter = ChartInterpreterAI(gemini_helper)
    return _interpreter


if __name__ == "__main__":
    # Test với dữ liệu mẫu
    test_chart = {
        "can_ngay": "Giáp",
        "can_gio": "Bính",
        "thien_ban": {1: "Thiên Bồng", 2: "Thiên Nhuế", 3: "Thiên Xung", 4: "Thiên Phụ",
                      5: "Thiên Cầm", 6: "Thiên Tâm", 7: "Thiên Trụ", 8: "Thiên Nhậm", 9: "Thiên Anh"},
        "nhan_ban": {1: "Hưu Môn", 2: "Sinh Môn", 3: "Thương Môn", 4: "Đỗ Môn",
                     5: "Trung", 6: "Khai Môn", 7: "Kinh Môn", 8: "Tử Môn", 9: "Cảnh Môn"},
        "than_ban": {1: "Cửu Địa", 2: "Cửu Thiên", 3: "Trực Phù", 4: "Đằng Xà",
                     5: "Thái Âm", 6: "Lục Hợp", 7: "Bạch Hổ", 8: "Huyền Vũ", 9: "Câu Trần"},
        "can_thien_ban": {1: "Giáp", 2: "Ất", 3: "Bính", 4: "Đinh",
                          5: "Mậu", 6: "Kỷ", 7: "Canh", 8: "Tân", 9: "Nhâm"},
        "dia_can": {1: "Tý", 2: "Sửu", 3: "Dần", 4: "Mão",
                    5: "Thìn", 6: "Tỵ", 7: "Ngọ", 8: "Mùi", 9: "Thân"},
        "khong_vong": [3, 4],
        "dich_ma": 9
    }
    
    interpreter = get_chart_interpreter()
    result = interpreter.get_super_interpretation(test_chart, "Xin việc")
    print(result)

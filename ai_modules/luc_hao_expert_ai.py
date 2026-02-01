"""
LUC HAO EXPERT AI - Chuyên Gia Lục Hào Kinh Dịch
Luận giải quẻ Lục Hào chi tiết với dự đoán chính xác
"""

from datetime import datetime

# Lục Thân
LUC_THAN = {
    "Phụ Mẫu": {"tuong": "Cha mẹ, Tài liệu, Nhà cửa, Xe cộ", "hanh_dong": "Bảo vệ, Che chở"},
    "Huynh Đệ": {"tuong": "Anh em, Bạn bè, Đối thủ cạnh tranh", "hanh_dong": "Cạnh tranh, Hao tài"},
    "Tử Tôn": {"tuong": "Con cháu, Niềm vui, Y dược", "hanh_dong": "Khắc Quan Quỷ, Sinh Tài"},
    "Thê Tài": {"tuong": "Tiền bạc, Vợ, Tài sản", "hanh_dong": "Khắc Phụ Mẫu, Đem lợi"},
    "Quan Quỷ": {"tuong": "Công việc, Chồng, Áp lực, Bệnh", "hanh_dong": "Khắc Huynh Đệ, Sinh Phụ Mẫu"},
    "Phúc Đức": {"tuong": "May mắn, Phúc lộc", "hanh_dong": "Tốt lành"}
}

# Dụng Thần theo chủ đề
DUNG_THAN_BY_TOPIC = {
    "tiền": "Thê Tài",
    "tài": "Thê Tài", 
    "lương": "Thê Tài",
    "đầu tư": "Thê Tài",
    "việc": "Quan Quỷ",
    "công việc": "Quan Quỷ",
    "thăng tiến": "Quan Quỷ",
    "kiện": "Quan Quỷ",
    "chồng": "Quan Quỷ",
    "vợ": "Thê Tài",
    "con": "Tử Tôn",
    "cháu": "Tử Tôn",
    "sức khỏe": "Tử Tôn",  # Tử Tôn khắc Quan Quỷ (bệnh)
    "bệnh": "Quan Quỷ",
    "cha": "Phụ Mẫu",
    "mẹ": "Phụ Mẫu",
    "nhà": "Phụ Mẫu",
    "xe": "Phụ Mẫu",
    "học": "Phụ Mẫu",
    "thi": "Phụ Mẫu",
    "bạn": "Huynh Đệ",
    "anh": "Huynh Đệ",
    "em": "Huynh Đệ"
}

# Trạng thái hào
HAO_STRENGTH = {
    "Vượng": {"score": 100, "mo_ta": "Cực mạnh, thành công cao"},
    "Tướng": {"score": 80, "mo_ta": "Mạnh, thuận lợi"},
    "Hưu": {"score": 50, "mo_ta": "Nghỉ ngơi, chờ đợi"},
    "Tù": {"score": 30, "mo_ta": "Bị kìm hãm, khó khăn"},
    "Tử": {"score": 10, "mo_ta": "Yếu nhất, thất bại"}
}


class LucHaoExpertAI:
    """
    Chuyên gia Lục Hào Kinh Dịch
    Luận giải với độ chính xác cao:
    - Xác định Dụng Thần đúng
    - Phân tích hào động, hào biến
    - Tính thời gian ứng nghiệm
    - Dự đoán kết quả
    """
    
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper
    
    def analyze_luc_hao(self, luc_hao_data, topic="Chung"):
        """Phân tích toàn diện quẻ Lục Hào"""
        
        # Xác định Dụng Thần
        dung_than = self._find_dung_than(topic, luc_hao_data)
        
        # Phân tích trạng thái Dụng Thần
        dung_than_status = self._analyze_dung_than_status(dung_than, luc_hao_data)
        
        # Phân tích hào động
        dong_hao_analysis = self._analyze_dong_hao(luc_hao_data)
        
        # Phân tích Thế/Ứng
        the_ung = self._analyze_the_ung(luc_hao_data)
        
        # Phân tích quẻ Biến
        bien_analysis = self._analyze_bien_quai(luc_hao_data)
        
        # Tính thời gian
        timing = self._calculate_timing(dung_than_status, luc_hao_data)
        
        # Kết luận
        conclusion = self._make_conclusion(dung_than_status, dong_hao_analysis, bien_analysis, topic)
        
        return {
            "dung_than": dung_than,
            "dung_than_status": dung_than_status,
            "dong_hao": dong_hao_analysis,
            "the_ung": the_ung,
            "bien": bien_analysis,
            "thoi_gian": timing,
            "ket_luan": conclusion
        }
    
    def _find_dung_than(self, topic, data):
        """Tìm Dụng Thần phù hợp với chủ đề"""
        topic_lower = topic.lower()
        
        for key, luc_than in DUNG_THAN_BY_TOPIC.items():
            if key in topic_lower:
                return {
                    "ten": luc_than,
                    "tuong": LUC_THAN.get(luc_than, {}).get("tuong", ""),
                    "ly_do": f"Việc '{topic}' thuộc về {luc_than}"
                }
        
        # Mặc định
        return {
            "ten": "Thê Tài",
            "tuong": LUC_THAN["Thê Tài"]["tuong"],
            "ly_do": "Mặc định xem Tài vận"
        }
    
    def _analyze_dung_than_status(self, dung_than, data):
        """Phân tích trạng thái Dụng Thần"""
        dung_than_name = dung_than["ten"]
        
        # Tìm hào Dụng Thần trong quẻ
        ban = data.get('ban', {})
        details = ban.get('details', [])
        
        dung_hao = None
        for d in details:
            if d.get('luc_than') == dung_than_name or dung_than_name in str(d.get('luc_thu', '')):
                dung_hao = d
                break
        
        if dung_hao:
            is_moving = dung_hao.get('is_moving', False)
            hao_num = dung_hao.get('hao', 0)
            can_chi = dung_hao.get('can_chi', '')
            
            # Đánh giá sức mạnh (simplified)
            strength = "Vượng" if is_moving else "Hưu"
            score = HAO_STRENGTH.get(strength, {}).get("score", 50)
            
            return {
                "hao": hao_num,
                "can_chi": can_chi,
                "dong": is_moving,
                "strength": strength,
                "score": score,
                "mo_ta": f"Dụng Thần {dung_than_name} ở Hào {hao_num} ({can_chi}), trạng thái {strength}"
            }
        
        return {
            "hao": 0,
            "can_chi": "?",
            "dong": False,
            "strength": "Hưu",
            "score": 50,
            "mo_ta": f"Dụng Thần {dung_than_name} không rõ vị trí"
        }
    
    def _analyze_dong_hao(self, data):
        """Phân tích các hào động"""
        dong_hao_list = data.get('dong_hao', [])
        
        if not dong_hao_list:
            return {
                "so_luong": 0,
                "mo_ta": "Không có hào động - Việc yên tĩnh, ít thay đổi",
                "y_nghia": "Tình hình ổn định, kết quả phụ thuộc vào trạng thái hiện tại"
            }
        
        analyses = []
        for hao in dong_hao_list:
            if hao <= 3:
                analyses.append(f"Hào {hao} động (Nội quái): Thay đổi từ bên trong, bản thân chủ động")
            else:
                analyses.append(f"Hào {hao} động (Ngoại quái): Thay đổi từ bên ngoài, hoàn cảnh tác động")
        
        meanings = {
            1: "động ở chỗ khởi đầu",
            2: "động ở giữa nội",
            3: "động ở biên nội",
            4: "động ở biên ngoại",
            5: "động ở giữa ngoại",
            6: "động ở đỉnh cao"
        }
        
        return {
            "so_luong": len(dong_hao_list),
            "danh_sach": dong_hao_list,
            "mo_ta": "; ".join(analyses),
            "y_nghia": f"Có {len(dong_hao_list)} hào động - Sự việc có nhiều biến chuyển"
        }
    
    def _analyze_the_ung(self, data):
        """Phân tích Thế/Ứng"""
        the_ung = data.get('the_ung', 'Thế Hào 1, Ứng Hào 4')
        
        return {
            "mo_ta": the_ung,
            "y_nghia": "Thế = Bản thân, Ứng = Đối phương/Hoàn cảnh",
            "quan_he": "Thế Ứng sinh hợp thì tốt, xung khắc thì xấu"
        }
    
    def _analyze_bien_quai(self, data):
        """Phân tích quẻ Biến"""
        bien = data.get('bien', {})
        bien_name = bien.get('name', 'Không xác định')
        
        # Mapping quẻ biến phổ biến
        bien_meanings = {
            "Thiên Địa Thái": "ĐẠI CÁT - Mọi việc hanh thông",
            "Địa Thiên Bĩ": "HUNG - Bế tắc, không thông",
            "Thuần Càn": "CÁT - Mạnh mẽ, thành công",
            "Thuần Khôn": "BÌNH - Thuận theo, chờ đợi",
            "Thủy Lôi Truân": "Khó khăn đầu, sau tốt dần",
            "Hỏa Thủy Vị Tế": "Chưa hoàn thành, cần kiên nhẫn"
        }
        
        return {
            "ten": bien_name,
            "y_nghia": bien_meanings.get(bien_name, f"Quẻ {bien_name} cho thấy kết quả cuối cùng"),
            "giai_doan": "Kết quả sau khi các hào động biến"
        }
    
    def _calculate_timing(self, dung_than_status, data):
        """Tính thời gian ứng nghiệm"""
        hao_num = dung_than_status.get("hao", 1)
        is_moving = dung_than_status.get("dong", False)
        
        # Thời gian cơ bản theo hào
        base_days = hao_num
        
        if is_moving:
            # Hào động: Việc nhanh hơn
            multiplier = 1
            speed = "nhanh"
        else:
            # Hào tĩnh: Việc chậm hơn
            multiplier = 7
            speed = "chậm"
        
        days = base_days * multiplier
        
        return {
            "so_ngay": days,
            "khoang": f"{days} ngày" if days < 30 else f"{days // 30} tháng",
            "toc_do": speed,
            "mo_ta": f"Dựa trên Hào {hao_num} {'động' if is_moving else 'tĩnh'}, việc sẽ ứng trong khoảng {days} ngày"
        }
    
    def _make_conclusion(self, dung_status, dong_hao, bien, topic):
        """Đưa ra kết luận"""
        score = dung_status.get("score", 50)
        
        # Điều chỉnh theo số hào động
        if dong_hao["so_luong"] == 0:
            score = score * 0.8  # Ít biến động
        elif dong_hao["so_luong"] > 3:
            score = score * 0.7  # Quá nhiều biến động
        
        # Điều chỉnh theo quẻ biến
        if "CÁT" in bien["y_nghia"]:
            score += 15
        elif "HUNG" in bien["y_nghia"]:
            score -= 20
        
        score = max(0, min(100, score))
        
        if score >= 75:
            verdict = "CÁT"
            advice = "Việc có thể tiến hành, khả năng thành công cao"
        elif score >= 50:
            verdict = "BÌNH"
            advice = "Việc có thể thành hoặc bại, cần xem xét thêm"
        else:
            verdict = "HUNG"
            advice = "Việc gặp nhiều trở ngại, nên hoãn lại"
        
        return {
            "diem": round(score),
            "verdict": verdict,
            "tom_tat": f"Việc '{topic}': {verdict} ({round(score)}%)",
            "loi_khuyen": advice
        }
    
    def get_detailed_interpretation(self, luc_hao_data, topic="Chung"):
        """API chính: Lấy luận giải chi tiết"""
        analysis = self.analyze_luc_hao(luc_hao_data, topic)
        
        output = []
        output.append(f"## 📜 LUẬN GIẢI LỤC HÀO: {topic.upper()}")
        output.append("")
        
        # Kết luận
        ket_luan = analysis["ket_luan"]
        output.append(f"### 📊 KẾT QUẢ: {ket_luan['verdict']} ({ket_luan['diem']}%)")
        output.append(f"**{ket_luan['loi_khuyen']}**")
        output.append("")
        
        # Dụng Thần
        dung_than = analysis["dung_than"]
        dung_status = analysis["dung_than_status"]
        output.append("### 🎯 DỤNG THẦN")
        output.append(f"- **{dung_than['ten']}**: {dung_than['tuong']}")
        output.append(f"- {dung_than['ly_do']}")
        output.append(f"- Trạng thái: {dung_status['mo_ta']}")
        output.append("")
        
        # Hào động
        dong_hao = analysis["dong_hao"]
        output.append("### ⚡ HÀO ĐỘNG")
        output.append(f"- {dong_hao['y_nghia']}")
        if dong_hao['so_luong'] > 0:
            output.append(f"- {dong_hao['mo_ta']}")
        output.append("")
        
        # Thế Ứng
        the_ung = analysis["the_ung"]
        output.append("### ☯️ THẾ/ỨNG")
        output.append(f"- {the_ung['mo_ta']}")
        output.append(f"- {the_ung['quan_he']}")
        output.append("")
        
        # Quẻ biến
        bien = analysis["bien"]
        output.append("### 🔄 QUẺ BIẾN")
        output.append(f"- **{bien['ten']}**: {bien['y_nghia']}")
        output.append("")
        
        # Thời gian
        timing = analysis["thoi_gian"]
        output.append("### ⏰ THỜI GIAN")
        output.append(f"- {timing['mo_ta']}")
        output.append(f"- Khoảng: **{timing['khoang']}**")
        
        return "\n".join(output)


# Singleton
_expert = None

def get_luc_hao_expert(gemini_helper=None):
    global _expert
    if _expert is None:
        _expert = LucHaoExpertAI(gemini_helper)
    return _expert


if __name__ == "__main__":
    expert = get_luc_hao_expert()
    
    test_data = {
        "ban": {
            "name": "Thiên Địa Thái",
            "palace": "Càn",
            "details": [
                {"hao": 1, "luc_than": "Thê Tài", "can_chi": "Tý Thủy", "is_moving": False},
                {"hao": 2, "luc_than": "Quan Quỷ", "can_chi": "Dần Mộc", "is_moving": True},
                {"hao": 3, "luc_than": "Tử Tôn", "can_chi": "Thìn Thổ", "is_moving": False},
                {"hao": 4, "luc_than": "Phụ Mẫu", "can_chi": "Ngọ Hỏa", "is_moving": False},
                {"hao": 5, "luc_than": "Huynh Đệ", "can_chi": "Thân Kim", "is_moving": True},
                {"hao": 6, "luc_than": "Quan Quỷ", "can_chi": "Tuất Thổ", "is_moving": False}
            ]
        },
        "bien": {"name": "Địa Thiên Bĩ"},
        "dong_hao": [2, 5],
        "the_ung": "Thế Hào 3, Ứng Hào 6"
    }
    
    print(expert.get_detailed_interpretation(test_data, "Công việc"))

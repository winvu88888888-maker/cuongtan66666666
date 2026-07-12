"""
MAI HOA EXPERT AI - Chuyên Gia Mai Hoa Dịch Số
Luận giải quẻ Mai Hoa siêu chi tiết với dự đoán chính xác
"""

from datetime import datetime

# 8 Quái
QUAI_INFO = {
    "Càn": {"hanh": "Kim", "so": 1, "tuong": "Trời, Cha, Lãnh đạo, Kim loại", "sac": "Trắng, Vàng kim"},
    "Đoài": {"hanh": "Kim", "so": 2, "tuong": "Đầm, Con gái út, Miệng, Vui vẻ", "sac": "Trắng"},
    "Ly": {"hanh": "Hỏa", "so": 3, "tuong": "Lửa, Con gái giữa, Mắt, Văn minh", "sac": "Đỏ, Cam"},
    "Chấn": {"hanh": "Mộc", "so": 4, "tuong": "Sấm, Con trai cả, Chân, Động", "sac": "Xanh lá"},
    "Tốn": {"hanh": "Mộc", "so": 5, "tuong": "Gió, Con gái cả, Đùi, Thuận", "sac": "Xanh lá"},
    "Khảm": {"hanh": "Thủy", "so": 6, "tuong": "Nước, Con trai giữa, Tai, Hiểm", "sac": "Đen, Xanh dương"},
    "Cấn": {"hanh": "Thổ", "so": 7, "tuong": "Núi, Con trai út, Tay, Dừng", "sac": "Vàng, Nâu"},
    "Khôn": {"hanh": "Thổ", "so": 8, "tuong": "Đất, Mẹ, Bụng, Thuận", "sac": "Vàng, Nâu"}
}

# Ngũ Hành
NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


class MaiHoaExpertAI:
    """
    Chuyên gia Mai Hoa Dịch Số
    Luận giải quẻ với độ chính xác cao về:
    - Thể/Dụng quan hệ
    - Thời gian ứng nghiệm
    - Số lượng liên quan
    - Kết quả cuối cùng
    """
    
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper
    
    def analyze_mai_hoa(self, mai_hoa_data, topic="Chung"):
        """
        Phân tích toàn diện quẻ Mai Hoa
        """
        # Xác định Thể/Dụng
        the_dung = self._determine_the_dung(mai_hoa_data)
        
        # Phân tích quan hệ sinh khắc
        relationship = self._analyze_the_dung_relationship(the_dung)
        
        # Phân tích quẻ Hỗ (diễn biến trung gian)
        ho_analysis = self._analyze_ho_quai(mai_hoa_data)
        
        # Phân tích quẻ Biến (kết quả cuối)
        bien_analysis = self._analyze_bien_quai(mai_hoa_data)
        
        # Tính thời gian ứng nghiệm
        timing = self._calculate_timing(mai_hoa_data, the_dung)
        
        # Tính số lượng
        quantity = self._calculate_quantity(mai_hoa_data)
        
        # Kết luận tổng hợp
        conclusion = self._make_conclusion(relationship, ho_analysis, bien_analysis, topic)
        
        return {
            "the_dung": the_dung,
            "quan_he": relationship,
            "ho_quai": ho_analysis,
            "bien_quai": bien_analysis,
            "thoi_gian": timing,
            "so_luong": quantity,
            "ket_luan": conclusion
        }
    
    def _determine_the_dung(self, data):
        """Xác định Thể quái và Dụng quái"""
        dong_hao = data.get('dong_hao', 1)
        upper = data.get('upper', 'Càn')
        lower = data.get('lower', 'Khôn')
        
        # Hào động 1-3: Hạ quái động -> Hạ là Dụng, Thượng là Thể
        # Hào động 4-6: Thượng quái động -> Thượng là Dụng, Hạ là Thể
        if dong_hao <= 3:
            the_quai = upper  # Thượng quái là Thể
            dung_quai = lower  # Hạ quái là Dụng
            the_vi_tri = "Thượng"
            dung_vi_tri = "Hạ (Động)"
        else:
            the_quai = lower  # Hạ quái là Thể
            dung_quai = upper  # Thượng quái là Dụng
            the_vi_tri = "Hạ"
            dung_vi_tri = "Thượng (Động)"
        
        the_info = QUAI_INFO.get(the_quai, {})
        dung_info = QUAI_INFO.get(dung_quai, {})
        
        return {
            "the": {
                "ten": the_quai,
                "hanh": the_info.get("hanh", "?"),
                "vi_tri": the_vi_tri,
                "tuong": the_info.get("tuong", ""),
                "so": the_info.get("so", 0)
            },
            "dung": {
                "ten": dung_quai,
                "hanh": dung_info.get("hanh", "?"),
                "vi_tri": dung_vi_tri,
                "tuong": dung_info.get("tuong", ""),
                "so": dung_info.get("so", 0)
            },
            "dong_hao": dong_hao
        }
    
    def _analyze_the_dung_relationship(self, the_dung):
        """Phân tích quan hệ Thể/Dụng"""
        the_hanh = the_dung["the"]["hanh"]
        dung_hanh = the_dung["dung"]["hanh"]
        
        # Các mối quan hệ:
        # 1. Dụng sinh Thể -> Đại Cát (việc đến tay, có người giúp)
        # 2. Thể khắc Dụng -> Cát (chủ động được việc)
        # 3. Thể Dụng tỷ hòa -> Bình (không tốt không xấu)
        # 4. Thể sinh Dụng -> Hung (hao tốn, mất mát)
        # 5. Dụng khắc Thể -> Đại Hung (thất bại, tổn hại)
        
        if NGU_HANH_SINH.get(dung_hanh) == the_hanh:
            return {
                "loai": "DUNG_SINH_THE",
                "verdict": "ĐẠI CÁT",
                "score": 95,
                "giai_thich": f"{dung_hanh} sinh {the_hanh}: Sự việc tự đến, có quý nhân phù trợ",
                "chi_tiet": "Dụng quái sinh Thể quái - Đây là cách tốt nhất. Việc sẽ thành công mà không cần cố gắng nhiều."
            }
        elif NGU_HANH_KHAC.get(the_hanh) == dung_hanh:
            return {
                "loai": "THE_KHAC_DUNG",
                "verdict": "CÁT",
                "score": 75,
                "giai_thich": f"{the_hanh} khắc {dung_hanh}: Chủ động kiểm soát được tình hình",
                "chi_tiet": "Thể quái khắc Dụng quái - Bạn có thể chinh phục được mục tiêu, nhưng cần nỗ lực."
            }
        elif the_hanh == dung_hanh:
            return {
                "loai": "TY_HOA",
                "verdict": "BÌNH",
                "score": 50,
                "giai_thich": f"{the_hanh} = {dung_hanh}: Hai bên cân bằng, chờ thời cơ",
                "chi_tiet": "Thể Dụng tỷ hòa - Tình hình ổn định, kết quả tùy thuộc vào các yếu tố khác."
            }
        elif NGU_HANH_SINH.get(the_hanh) == dung_hanh:
            return {
                "loai": "THE_SINH_DUNG",
                "verdict": "HUNG",
                "score": 30,
                "giai_thich": f"{the_hanh} sinh {dung_hanh}: Bạn phải tốn sức, hao tài",
                "chi_tiet": "Thể quái sinh Dụng quái - Bạn sẽ phải bỏ ra nhiều hơn những gì nhận lại."
            }
        elif NGU_HANH_KHAC.get(dung_hanh) == the_hanh:
            return {
                "loai": "DUNG_KHAC_THE",
                "verdict": "ĐẠI HUNG",
                "score": 10,
                "giai_thich": f"{dung_hanh} khắc {the_hanh}: Bị áp đảo, thất bại",
                "chi_tiet": "Dụng quái khắc Thể quái - Tình hình bất lợi, nên tránh hoặc hoãn lại."
            }
        else:
            return {
                "loai": "KHONG_XAC_DINH",
                "verdict": "BÌNH",
                "score": 50,
                "giai_thich": "Quan hệ không rõ ràng",
                "chi_tiet": "Cần xem thêm các yếu tố khác."
            }
    
    def _analyze_ho_quai(self, data):
        """Phân tích quẻ Hỗ - Diễn biến trung gian"""
        ho_quai = data.get('ten_ho', 'Không xác định')
        
        # Mapping quẻ Hỗ -> ý nghĩa
        ho_meanings = {
            "Thuần Càn": "Quá trình mạnh mẽ, gặp nhiều thử thách từ cấp trên",
            "Thuần Khôn": "Quá trình thuận lợi nhờ sự hỗ trợ, cần kiên nhẫn",
            "Thủy Lôi Truân": "Khởi đầu khó khăn nhưng sẽ tốt dần",
            "Sơn Thủy Mông": "Cần học hỏi, tìm người hướng dẫn",
            "Thiên Thủy Tụng": "Có tranh chấp, cãi vã trong quá trình",
            "Địa Thủy Sư": "Cần có đội ngũ, không nên làm một mình"
        }
        
        return {
            "ten": ho_quai,
            "y_nghia": ho_meanings.get(ho_quai, f"Quẻ {ho_quai} chỉ diễn biến trung gian của sự việc"),
            "giai_doan": "Giai đoạn giữa - Quá trình thực hiện"
        }
    
    def _analyze_bien_quai(self, data):
        """Phân tích quẻ Biến - Kết quả cuối cùng"""
        bien_quai = data.get('ten_qua_bien', 'Không xác định')
        
        # Mapping quẻ Biến -> kết quả
        bien_meanings = {
            "Thuần Càn": {"ket_qua": "Thành công rực rỡ", "score": 90},
            "Thuần Khôn": {"ket_qua": "Thuận lợi nếu biết chờ đợi", "score": 70},
            "Thủy Lôi Truân": {"ket_qua": "Khó khăn ban đầu, sau sẽ ổn", "score": 60},
            "Địa Thiên Thái": {"ket_qua": "Rất tốt, mọi việc hanh thông", "score": 95},
            "Thiên Địa Bĩ": {"ket_qua": "Bế tắc, nên hoãn lại", "score": 20},
            "Thuần Khảm": {"ket_qua": "Nhiều hiểm nguy, cẩn thận", "score": 30}
        }
        
        default = {"ket_qua": f"Xem quẻ {bien_quai} để biết kết quả", "score": 50}
        bien_info = bien_meanings.get(bien_quai, default)
        
        return {
            "ten": bien_quai,
            "ket_qua": bien_info["ket_qua"],
            "score": bien_info["score"],
            "giai_doan": "Giai đoạn cuối - Kết quả cuối cùng"
        }
    
    def _calculate_timing(self, data, the_dung):
        """Tính thời gian ứng nghiệm"""
        dong_hao = data.get('dong_hao', 1)
        dung_so = the_dung["dung"]["so"]
        the_so = the_dung["the"]["so"]
        
        # Thời gian ứng = Số của quẻ Dụng (đơn vị: ngày/tuần/tháng tùy quẻ)
        tong = dung_so + the_so
        
        return {
            "so_ngay": dung_so,
            "so_tuan": tong // 7 if tong >= 7 else None,
            "so_thang": dung_so if dung_so <= 12 else dung_so % 12,
            "mo_ta": f"Ứng nghiệm trong khoảng {dung_so} ngày hoặc {dung_so} tháng",
            "chi_tiet": f"Dựa trên số của Dụng quái ({the_dung['dung']['ten']} = {dung_so})"
        }
    
    def _calculate_quantity(self, data):
        """Tính số lượng liên quan"""
        upper_info = QUAI_INFO.get(data.get('upper', 'Càn'), {})
        lower_info = QUAI_INFO.get(data.get('lower', 'Khôn'), {})
        
        upper_so = upper_info.get('so', 1)
        lower_so = lower_info.get('so', 1)
        
        return {
            "so_chinh": upper_so + lower_so,
            "so_phu": upper_so * lower_so,
            "mo_ta": f"Con số chính: {upper_so + lower_so}, con số phụ: {upper_so * lower_so}",
            "y_nghia": "Có thể là số tiền (triệu), số người, số ngày, tùy ngữ cảnh"
        }
    
    def _make_conclusion(self, relationship, ho_analysis, bien_analysis, topic):
        """Đưa ra kết luận tổng hợp"""
        # Tính điểm tổng hợp
        score = (relationship["score"] + bien_analysis["score"]) / 2
        
        if score >= 80:
            verdict = "ĐẠI CÁT"
            advice = "Nên tiến hành ngay, thời cơ rất tốt"
        elif score >= 60:
            verdict = "CÁT"
            advice = "Có thể tiến hành, nhưng cần chuẩn bị kỹ"
        elif score >= 40:
            verdict = "BÌNH"
            advice = "Cân nhắc kỹ, có thể thành hoặc bại"
        elif score >= 20:
            verdict = "HUNG"
            advice = "Nên hoãn lại hoặc thay đổi cách tiếp cận"
        else:
            verdict = "ĐẠI HUNG"
            advice = "Không nên tiến hành, tránh xa hoàn toàn"
        
        return {
            "diem": round(score),
            "verdict": verdict,
            "tom_tat": f"Việc '{topic}': {verdict} ({round(score)}%)",
            "loi_khuyen": advice,
            "chi_tiet": [
                f"• Quan hệ Thể/Dụng: {relationship['verdict']} - {relationship['giai_thich']}",
                f"• Quá trình: {ho_analysis['y_nghia']}",
                f"• Kết quả cuối: {bien_analysis['ket_qua']}"
            ]
        }
    
    def get_detailed_interpretation(self, mai_hoa_data, topic="Chung"):
        """API chính: Lấy luận giải chi tiết"""
        analysis = self.analyze_mai_hoa(mai_hoa_data, topic)
        
        output = []
        output.append(f"## 🌸 LUẬN GIẢI MAI HOA: {topic.upper()}")
        output.append("")
        
        # Kết luận
        ket_luan = analysis["ket_luan"]
        output.append(f"### 📊 KẾT QUẢ: {ket_luan['verdict']} ({ket_luan['diem']}%)")
        output.append(f"**{ket_luan['loi_khuyen']}**")
        output.append("")
        
        # Thể/Dụng
        the_dung = analysis["the_dung"]
        output.append("### ☯️ THỂ/DỤNG")
        output.append(f"- **Thể ({the_dung['the']['vi_tri']}):** {the_dung['the']['ten']} ({the_dung['the']['hanh']})")
        output.append(f"  Tượng: {the_dung['the']['tuong']}")
        output.append(f"- **Dụng ({the_dung['dung']['vi_tri']}):** {the_dung['dung']['ten']} ({the_dung['dung']['hanh']})")
        output.append(f"  Tượng: {the_dung['dung']['tuong']}")
        output.append("")
        
        # Quan hệ
        quan_he = analysis["quan_he"]
        output.append("### 🔄 QUAN HỆ SINH KHẮC")
        output.append(f"**{quan_he['verdict']}**: {quan_he['giai_thich']}")
        output.append(f"{quan_he['chi_tiet']}")
        output.append("")
        
        # Thời gian
        timing = analysis["thoi_gian"]
        output.append("### ⏰ THỜI GIAN ỨNG NGHIỆM")
        output.append(f"- {timing['mo_ta']}")
        output.append(f"- {timing['chi_tiet']}")
        output.append("")
        
        # Số lượng
        qty = analysis["so_luong"]
        output.append("### 🔢 SỐ LƯỢNG")
        output.append(f"- {qty['mo_ta']}")
        output.append(f"- {qty['y_nghia']}")
        output.append("")
        
        # Chi tiết
        output.append("### 📋 CHI TIẾT")
        for detail in ket_luan["chi_tiet"]:
            output.append(detail)
        
        return "\n".join(output)


# Singleton
_expert = None

def get_mai_hoa_expert(gemini_helper=None):
    global _expert
    if _expert is None:
        _expert = MaiHoaExpertAI(gemini_helper)
    return _expert


if __name__ == "__main__":
    expert = get_mai_hoa_expert()
    
    test_data = {
        "upper": "Càn",
        "lower": "Khôn", 
        "dong_hao": 2,
        "ten": "Thiên Địa Bĩ",
        "ten_ho": "Sơn Thủy Mông",
        "ten_qua_bien": "Địa Thiên Thái"
    }
    
    print(expert.get_detailed_interpretation(test_data, "Kinh doanh"))

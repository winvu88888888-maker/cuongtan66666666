
import random
from qmdg_data import KY_MON_DATA, QUAI_TUONG, CUNG_NGU_HANH, BAT_MON_CO_DINH_DISPLAY

class FreeAIHelper:
    """
    Offline AI Helper using rule-based logic and existing database.
    Does not require API Key.
    """
    def __init__(self, api_key=None):
        self.name = "Free AI (Offline)"
        
    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        """Alias for offline compatibility"""
        return self.answer_question(prompt)

    def analyze_palace(self, palace_data, topic):
        """
        Generate detailed analysis for a palace using rule-based template.
        """
        p_num = palace_data.get('num')
        star = palace_data.get('star')
        door = palace_data.get('door')
        deity = palace_data.get('deity')
        stem_top = palace_data.get('can_thien')
        stem_bottom = palace_data.get('can_dia')
        
        # Get data from QMDG_DATA
        star_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(star, {})
        door_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(door + " Môn", {})
        deity_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(deity, {})
        
        stem_key = f"{stem_top}{stem_bottom}"
        stem_info = KY_MON_DATA['TRUCTU_TRANH'].get(stem_key, {})
        
        # Assemble response
        response = f"""
### 📋 Phân Tích Cung {p_num} ({QUAI_TUONG.get(p_num)}) - Chế độ Offline

**1. Tinh (Sao): {star}**
- Ngũ hành: {star_info.get('Hành', 'N/A')}
- Ý nghĩa: {star_info.get('Tính_Chất', 'Không có dữ liệu')}

**2. Môn (Cửa): {door}**
- Đánh giá: {door_info.get('Cát_Hung', 'Bình')}
- Luận đoán: {door_info.get('Luận_Đoán', 'Không có dữ liệu')}

**3. Thần: {deity}**
- Tính chất: {deity_info.get('Tính_Chất', 'Không có dữ liệu')}

**4. Cách Cục (Thien/Địa): {stem_top}/{stem_bottom}**
- Tên cách cục: {stem_info.get('Tên_Cách_Cục', 'Bình thường')}
- Đánh giá: {stem_info.get('Cát_Hung', 'Bình')}
- Giải nghĩa: {stem_info.get('Luận_Giải', 'Tương tác bình thường giữa hai can.')}

**💡 Kết luận sơ bộ cho chủ đề "{topic}":**
Dựa trên các yếu tố trên, Cung này có trạng thái **{door_info.get('Cát_Hung', 'Bình')}**. 
Lưu ý đặc biệt về **{door}** và cách cục **{stem_info.get('Tên_Cách_Cục', 'N/A')}**.
"""
        return response

    def explain_element(self, element_type, element_name):
        """Explain a specific element"""
        info = ""
        category = ""
        
        if element_type == 'star':
            category = "Cửu Tinh"
            data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(element_name, {})
            info = f"Ngũ hành: {data.get('Hành')}. {data.get('Tính_Chất')}"
        elif element_type == 'door':
            category = "Bát Môn"
            # Try appending " Môn" if missing
            name_lookup = element_name if "Môn" in element_name else element_name + " Môn"
            data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(name_lookup, {})
            info = f"Cát/Hung: {data.get('Cát_Hung')}. {data.get('Luận_Đoán')}"
        elif element_type == 'deity':
            category = "Bát Thần"
            data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(element_name, {})
            info = f"{data.get('Tính_Chất')}"
        elif element_type == 'stem':
            category = "Thiên Can"
            # Stem logic usually simpler in dictionary
            info = "Tra cứu bảng Thiên Can để biết chi tiết."
            
        return f"**Giải thích {category}: {element_name}**\n\n{info}"

    def comprehensive_analysis(self, chart_data, topic, dung_than_list=None):
        """Generate a full chart report"""
        
        report = [f"### 🛡️ BÁO CÁO TỔNG QUAN (OFFLINE MODE)\n**Chủ đề:** {topic}\n"]
        
        if dung_than_list:
            report.append(f"**Dụng Thần trọng tâm:** {', '.join(dung_than_list)}\n")
            
        # Analyze Dụng Thần palaces first if possible, otherwise just summary
        report.append("#### 1. Đánh giá sơ bộ các cung:")
        
        good_palaces = []
        bad_palaces = []
        
        for p_num in range(1, 10):
            if p_num == 5: continue
            
            door = chart_data['nhan_ban'].get(p_num)
            door_full = door + " Môn" if door else ""
            door_info = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(door_full, {})
            cat_hung = door_info.get('Cát_Hung', 'Bình')
            
            if cat_hung in ['Đại Cát', 'Cát']:
                good_palaces.append(f"Cung {p_num} ({door})")
            elif cat_hung in ['Đại Hung', 'Hung']:
                bad_palaces.append(f"Cung {p_num} ({door})")
                
        report.append(f"- **Các cung Cát lợi:** {', '.join(good_palaces) if good_palaces else 'Không rõ rệt'}")
        report.append(f"- **Các cung Bất lợi:** {', '.join(bad_palaces) if bad_palaces else 'Không rõ rệt'}")
        
        report.append("\n#### 2. Lời khuyên chung:")
        report.append("Đây là phân tích tự động dựa trên dữ liệu tra cứu. Hãy tập trung vào các cung có Cửa Sinh, Cửa Khai, Cửa Hưu cho các việc tốt, và tránh Cửa Tử, Cửa Kinh.")
        
        return "\n".join(report)

    def answer_question(self, question, chart_data=None, topic=None):
        """Offline Q&A"""
        return f"""
**🤖 Chế độ Free AI (Offline)**

Tôi đang chạy ở chế độ không có Internet/API Key, nên không thể trả lời câu hỏi tự do:
_"{question}"_

Tuy nhiên, bạn có thể sử dụng các nút chức năng có sẵn trên giao diện để xem phân tích chi tiết từ dữ liệu đã được lập trình sẵn.

Để sử dụng AI thông minh (Gemini), vui lòng nhập API Key trong phần Cấu Hình.
"""

    def analyze_luc_hao(self, luc_hao_res, topic="Chung"):
        """Offline analysis for Luc Hao"""
        ban = luc_hao_res.get('ban', {})
        bien = luc_hao_res.get('bien', {})
        dong_hao = luc_hao_res.get('dong_hao', [])
        
        status = "Cát lợi" if not dong_hao else "Có sự biến hóa"
        
        report = [
            f"### ☯️ Luận Giải Lục Hào (Offline) - Việc: {topic}",
            f"**Quẻ Chủ:** {ban.get('name')} ({ban.get('palace')})",
            f"**Quẻ Biến:** {bien.get('name')}",
            f"**Hào Động:** {', '.join(map(str, dong_hao)) if dong_hao else 'Tĩnh'}",
            "\n**💡 Phân tích sơ bộ:**",
            f"- Quẻ chủ của bạn là **{ban.get('name')}**, báo hiệu trạng thái ban đầu.",
            f"- Quẻ biến **{bien.get('name')}** cho thấy kết quả hoặc diễn biến sau này."
        ]
        
        if dong_hao:
            report.append(f"- Bạn có {len(dong_hao)} hào động. Sự thay đổi này là trọng tâm của quẻ.")
        else:
            report.append("- Quẻ tĩnh, sự việc ít có biến động bất ngờ.")
            
        report.append(f"\n**Kết luận:** Chủ đề '{topic}' đang ở trạng thái {status}. Hãy xem bảng chi tiết hào để biết thêm về các yếu tố Lục Thân và Lục Thú.")
        
        return "\n".join(report)

    def analyze_mai_hoa(self, mai_hoa_res, topic="Chung"):
        """Offline analysis for Mai Hoa"""
        # Determine The/Dung
        if mai_hoa_res['dong_hao'] <= 3:
            the_quai, dung_quai = mai_hoa_res['upper'], mai_hoa_res['lower']
        else:
            the_quai, dung_quai = mai_hoa_res['lower'], mai_hoa_res['upper']
            
        from mai_hoa_dich_so import QUAI_ELEMENTS, QUAI_NAMES
        the_el = QUAI_ELEMENTS.get(the_quai)
        dung_el = QUAI_ELEMENTS.get(dung_quai)
        
        report = [
            f"### 🌸 Luận Giải Mai Hoa (Offline) - Việc: {topic}",
            f"**Quẻ Chủ:** {mai_hoa_res['ten']}",
            f"**Hào Động:** {mai_hoa_res['dong_hao']}",
            f"**Quẻ Biến:** {mai_hoa_res['ten_qua_bien']}",
            f"\n**Phân tích Thể/Dụng:**",
            f"- **Thể (Ta):** {QUAI_NAMES[the_quai]} ({the_el})",
            f"- **Dụng (Việc):** {QUAI_NAMES[dung_quai]} ({dung_el})",
            f"\n**💡 Ý nghĩa:**",
            f"- Quẻ chủ **{mai_hoa_res['ten']}** báo hiệu sự việc hiện tại: {mai_hoa_res['nghĩa']}",
            f"- Diễn biến hướng về quẻ **{mai_hoa_res['ten_qua_bien']}**."
        ]
        
        return "\n".join(report)

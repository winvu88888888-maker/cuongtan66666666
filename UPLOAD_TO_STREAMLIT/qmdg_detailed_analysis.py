
# Placeholder for qmdg_detailed_analysis module
# This prevents ModuleNotFoundError if the full module is not available.


from database_tuong_tac import SINH_KHAC_MATRIX, LUC_THAN_MAPPING
from qmdg_data import KY_MON_DATA

def phan_tich_chi_tiet_cung(topic, palace_data):
    """
    Detailed palace analysis using rule-based logic.
    """
    sao = palace_data.get('star')
    cua = palace_data.get('door')
    hanh = palace_data.get('hanh')
    p_num = palace_data.get('num')
    
    analysis = f"**Phân tích sâu Cung {p_num}:**\n"
    analysis += f"- Ngũ hành cung: {hanh}\n"
    
    # Simple logic for now, can be expanded
    if sao:
        s_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CU_TINH' if 'CU_TINH' in KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO'] else 'CUU_TINH'].get(sao, {})
        analysis += f"- Sao {sao} ({s_data.get('Hành', 'N/A')}): {s_data.get('Tính_Chất', '')}\n"
    
    if cua:
        c_data = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(cua + " Môn", {})
        analysis += f"- Cửa {cua} ({c_data.get('Cát_Hung', 'Bình')}): {c_data.get('Luận_Đoán', '')}\n"
        
    return analysis

def so_sanh_chi_tiet_chu_khach(topic, chu_data, khach_data):
    """
    Detailed host/guest comparison based on elements and topics.
    """
    h_chu = chu_data.get('hanh', 'N/A')
    h_khach = khach_data.get('hanh', 'N/A')
    
    interaction = SINH_KHAC_MATRIX.get(h_chu, {}).get(h_khach, "Bình Hòa")
    
    # Determine Lục Thân based on interaction
    luc_than = LUC_THAN_MAPPING.get(interaction, "Huynh Đệ")
    
    analysis = f"Mối quan hệ giữa Chủ ({h_chu}) và Khách ({h_khach}) là **{interaction}**.\n"
    analysis += f"Trong chủ đề {topic}, Khách đóng vai trò là **{luc_than}** đối với Chủ.\n"
    
    if interaction == "Sinh":
        advice = "Chủ đang sinh cho Khách, hao tổn sức lực, cần cẩn trọng."
    elif interaction == "Khắc":
        advice = "Chủ khắc Khách, chiếm ưu thế nhưng cần dùng sức mạnh đúng chỗ."
    elif interaction == "Được Sinh":
        advice = "Chủ được Khách sinh, gặp nhiều thuận lợi, quý nhân phù trợ."
    elif interaction == "Bị Khắc":
        advice = "Chủ bị Khách khắc, gặp nhiều áp lực, cần phòng thủ."
    else:
        advice = "Mối quan hệ bình hòa, thuận theo tự nhiên."
        
    return {
        "ngu_hanh_sinh_khac": interaction,
        "phan_tich": advice,
        "luc_than": luc_than
    }


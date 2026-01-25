import json
import os
import sys
from datetime import datetime

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- CẤU HÌNH FILE DỮ LIỆU TÙY CHỈNH ---
CUSTOM_DATA_FILE = resource_path('custom_data.json')
EXCEL_DATA_FILE = resource_path('qmdg_excel_full.json')
ADVANCED_DATA_FILE = resource_path('qmdg_advanced_knowledge.json')

def load_excel_data():
    """Tải dữ liệu đã trích xuất từ Excel và trộn vào KY_MON_DATA."""
    if os.path.exists(EXCEL_DATA_FILE):
        try:
            with open(EXCEL_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def merge_excel_data(base_data):
    """Trộn dữ liệu Excel vào cấu trúc dữ liệu chính."""
    excel_data = load_excel_data()
    if not excel_data:
        return base_data
    
    # Trộn Stem Combos vào TRUCTU_TRANH
    stem_combos = excel_data.get("STEM_COMBOS", {})
    for key, content in stem_combos.items():
        if key not in base_data["TRUCTU_TRANH"]:
            base_data["TRUCTU_TRANH"][key] = {
                "Tên_Cách_Cục": "Tra cứu Excel",
                "Cát_Hung": "Tra cứu",
                "Luận_Giải": content
            }
        else:
            # Bổ sung thêm diễn giải từ Excel nếu đã có
            base_data["TRUCTU_TRANH"][key]["Luận_Giải"] += f"\n (Excel: {content})"
            
    base_data["ENRICHED_DATA"] = excel_data
    return base_data

def load_advanced_knowledge():
    """Tải dữ liệu nâng cao từ các nguồn PDF/Book."""
    if os.path.exists(ADVANCED_DATA_FILE):
        try:
            with open(ADVANCED_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def load_custom_data():
    """Tải dữ liệu tùy chỉnh từ file JSON, nếu không có thì trả về cấu trúc rỗng."""
    if os.path.exists(CUSTOM_DATA_FILE):
        try:
            with open(CUSTOM_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Nếu file bị lỗi định dạng hoặc không đọc được
            return {"TRUCTU_TRANH": {}}
    return {"TRUCTU_TRANH": {}}

def save_custom_data(data):
    """Lưu dữ liệu tùy chỉnh vào file JSON."""
    try:
        with open(CUSTOM_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False

# ======================================================================
# PHẦN 1: DỮ LIỆU CỐ ĐỊNH KY MÔN
# ======================================================================

# Cấu trúc 9 cung
CUNG_NGU_HANH = {
    1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ",
    6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"
}

QUAI_TUONG = {
    1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 5: "Trung Cung",
    6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"
}

# Dữ liệu Bát Môn Cố Định (Tra cứu tên gọi hiển thị)
BAT_MON_CO_DINH_DISPLAY = {
    "Khai": "Khai Môn", "Hưu": "Hưu Môn", "Sinh": "Sinh Môn", 
    "Thương": "Thương Môn", "Đỗ": "Đỗ Môn", "Cảnh": "Cảnh Môn", 
    "Tử": "Tử Môn", "Kinh": "Kinh Môn"
}

# Vị trí Bát Môn Cố Định theo Cung (không dùng cung 5)
BAT_MON_CO_DINH_CUNG = {
    1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 6: "Kinh", 7: "Khai", 8: "Sinh", 9: "Cảnh"
}

# Địa Chi Giờ
CAN_CHI_Gio = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# DỮ LIỆU CHÍNH
KY_MON_DATA = {
    # Dữ liệu từ Excel sẽ được trộn vào đây nếu có
    "ENRICHED_DATA": load_excel_data(),
    "DU_LIEU_DUNG_THAN_PHU_TRO": {
        "CUU_TINH": {
            "Thiên Bồng": {"Hành": "Thủy", "Tính_Chất": "Tướng quân, thích hợp trộm cướp, binh đao."},
            "Thiên Nhuế": {"Hành": "Thổ", "Tính_Chất": "Y dược, giáo dục, bất lợi xuất hành."},
            "Thiên Xung": {"Hành": "Mộc", "Tính_Chất": "Quân sự, cạnh tranh, động tĩnh."},
            "Thiên Phụ": {"Hành": "Mộc", "Tính_Chất": "Văn chương, học thuật, ẩn tàng."},
            "Thiên Cầm": {"Hành": "Thổ", "Tính_Chất": "Lãnh đạo, trung tâm, điều hòa."},
            "Thiên Tâm": {"Hành": "Kim", "Tính_Chất": "Mưu lược, y học, thần bí."},
            "Thiên Trụ": {"Hành": "Kim", "Tính_Chất": "Võ thuật, ẩn náu, gây rối."},
            "Thiên Nhậm": {"Hành": "Thổ", "Tính_Chất": "Điền sản, tài lộc, chậm chạp."},
            "Thiên Anh": {"Hành": "Hỏa", "Tính_Chất": "Văn minh, danh vọng, hỏa hoạn."}
        },
        "BAT_MON": {
            "Khai Môn": {"Cát_Hung": "Đại Cát", "Luận_Đoán": "Thích hợp khai trương, nhậm chức, xuất hành."},
            "Hưu Môn": {"Cát_Hung": "Cát", "Luận_Đoán": "Thích hợp tĩnh dưỡng, nghỉ ngơi, gặp quý nhân."},
            "Sinh Môn": {"Cát_Hung": "Đại Cát", "Luận_Đoán": "Thích hợp cầu tài, sinh sản, kinh doanh."},
            "Thương Môn": {"Cát_Hung": "Hung", "Luận_Đoán": "Thích hợp săn bắt, đòi nợ, kiện cáo (bất lợi)."},
            "Đỗ Môn": {"Cát_Hung": "Bình", "Luận_Đoán": "Thích hợp ẩn náu, phòng thủ, kỹ thuật."},
            "Cảnh Môn": {"Cát_Hung": "Bình", "Luận_Đoán": "Thích hợp văn thư, thi cử, yến tiệc."},
            "Tử Môn": {"Cát_Hung": "Đại Hung", "Luận_Đoán": "Bất lợi mọi việc, chỉ thích hợp mai táng, săn bắn."},
            "Kinh Môn": {"Cát_Hung": "Hung", "Luận_Đoán": "Thích hợp kiện tụng, tranh cãi, báo động."}
        },
        "BAT_THAN": {
            "Trực Phù": {"Tính_Chất": "Quý nhân tối cao, thần che chở, cát lợi."},
            "Đằng Xà": {"Tính_Chất": "Dây dưa, thần quỷ, biến hóa khôn lường."},
            "Thái Âm": {"Tính_Chất": "Ẩn tàng, mưu kế, giúp đỡ kín đáo."},
            "Lục Hợp": {"Tính_Chất": "Hợp tác, hôn nhân, hòa hợp, công bằng."},
            "Bạch Hổ": {"Tính_Chất": "Binh khí, tai ương, hình phạt, uy vũ."},
            "Huyền Vũ": {"Tính_Chất": "Trộm cắp, lừa dối, ám muội."},
            "Cửu Địa": {"Tính_Chất": "Tĩnh, chậm chạp, có lợi ẩn náu."},
            "Cửu Thiên": {"Tính_Chất": "Động, cao xa, có lợi xuất chinh, hành động."}
        }
    },
    
    "CAN_CHI_LUAN_GIAI": {
        "Giáp": {"Hành": "Mộc", "Tính_Chất": "Nguyên soái, chỉ huy, ẩn tàng."},
        "Ất": {"Hành": "Mộc", "Tính_Chất": "Nữ nhân, thần y, thảo dược, cong."},
        "Bính": {"Hành": "Hỏa", "Tính_Chất": "Văn thư, ánh sáng, đột ngột, tai họa."},
        "Đinh": {"Hành": "Hỏa", "Tính_Chất": "Lửa nhỏ, thần tài, văn thư, bí mật."},
        "Mậu": {"Hành": "Thổ", "Tính_Chất": "Tiền vốn, tài sản, người trung thực."},
        "Kỷ": {"Hành": "Thổ", "Tính_Chất": "Đất thấp, dâm dục, bệnh tật, ẩn giấu."},
        "Canh": {"Hành": "Kim", "Tính_Chất": "Đối thủ, trở ngại, đường xá, hình pháp."},
        "Tân": {"Hành": "Kim", "Tính_Chất": "Tội lỗi, sai lầm, kim khí nhỏ."},
        "Nhâm": {"Hành": "Thủy", "Tính_Chất": "Sông nước, trộm cắp, phạm nhân."},
        "Quý": {"Hành": "Thủy", "Tính_Chất": "Thiên võng, tù nhân, mưa gió."}
    },
    
    # Cách cục cố định (Dữ liệu tùy chỉnh sẽ được ghi đè/bổ sung tại đây)
    "TRUCTU_TRANH": {
        # Ất (Thiên)
        "ẤtẤt": {"Tên_Cách_Cục": "Nhật Kỳ Phục Vịnh", "Cát_Hung": "Bình/Hung", "Luận_Giải": "Trì trệ, rối rắm, cần kiên nhẫn."},
        "ẤtBính": {"Tên_Cách_Cục": "Kỳ Nghi Hợp Môn", "Cát_Hung": "Đại Cát", "Luận_Giải": "Tài lộc lớn, tốt cho đầu tư, kết hôn."},
        "ẤtĐinh": {"Tên_Cách_Cục": "Kỳ Nghi Tương Tùy", "Cát_Hung": "Cát", "Luận_Giải": "Hôn nhân tốt, kiện tụng hòa giải."},
        "ẤtMậu": {"Tên_Cách_Cục": "Cầm Tác", "Cát_Hung": "Cát", "Luận_Giải": "Được tài lộc từ người quý, đắc lợi lớn."},
        "ẤtKỷ": {"Tên_Cách_Cục": "Nhật Kỳ Nhập Vọng", "Cát_Hung": "Hung", "Luận_Giải": "Công việc rối rắm, gặp khó khăn."},
        "ẤtCanh": {"Tên_Cách_Cục": "Nhật Kỳ Bách Cách", "Cát_Hung": "Đại Hung", "Luận_Giải": "Mất người, mất tiền, gặp tai họa, đại hung."},
        "ẤtTân": {"Tên_Cách_Cục": "Thanh Long Triết Túc", "Cát_Hung": "Đại Hung", "Luận_Giải": "Bị thương tật chân tay, tài lộc bị mất."},
        "ẤtNhâm": {"Tên_Cách_Cục": "Nhật Kỳ Nhập Địa", "Cát_Hung": "Đại Hung", "Luận_Giải": "Thuyền chìm gặp sóng gió, mọi việc thất bại."},
        "ẤtQuý": {"Tên_Cách_Cục": "Hoa Cái Mão Mệnh", "Cát_Hung": "Cát", "Luận_Giải": "Vận may đến, công danh tốt."},
        # Bính (Thiên)
        "BínhẤt": {"Tên_Cách_Cục": "Hỏa Mộc Tương Sinh", "Cát_Hung": "Cát", "Luận_Giải": "Được quý nhân giúp đỡ, có người cầu hôn."},
        "BínhBính": {"Tên_Cách_Cục": "Tuế Tinh Phục Vịnh", "Cát_Hung": "Bình/Hung", "Luận_Giải": "Trì trệ, nhiều lời đồn, kiện tụng bất lợi."},
        "BínhĐinh": {"Tên_Cách_Cục": "Tinh Kỳ Nhập Tọa", "Cát_Hung": "Cát", "Luận_Giải": "Tốt cho văn chương, khoa cử, thi cử."},
        "BínhMậu": {"Tên_Cách_Cục": "Thanh Long Hồi Đầu", "Cát_Hung": "Đại Cát", "Luận_Giải": "Tiền của đến dồn dập, đầu tư phát đạt, cực kỳ tốt."},
        "BínhKỷ": {"Tên_Cách_Cục": "Hỏa Thổ Tương Sinh", "Cát_Hung": "Cát", "Luận_Giải": "Gặp quý nhân, mọi việc hanh thông."},
        "BínhCanh": {"Tên_Cách_Cục": "Oai Hùng Hỏa Tinh", "Cát_Hung": "Đại Hung", "Luận_Giải": "Kiện tụng thua kiện, tai nạn, tổn hại tài sản."},
        "BínhTân": {"Tên_Cách_Cục": "Hình Cách", "Cát_Hung": "Hung", "Luận_Giải": "Dễ bị phạm tội, kiện cáo, mọi việc không thông."},
        "BínhNhâm": {"Tên_Cách_Cục": "Tuế Tinh Nhập Thiên", "Cát_Hung": "Đại Hung", "Luận_Giải": "Cẩn thận tai họa sông nước, mất của."},
        "BínhQuý": {"Tên_Cách_Cục": "Hoa Cái", "Cát_Hung": "Hung", "Luận_Giải": "Dễ gặp thị phi, kiện tụng bất lợi."},
        # Đinh (Thiên)
        "ĐinhẤt": {"Tên_Cách_Cục": "Nhân Hợp", "Cát_Hung": "Cát", "Luận_Giải": "Tình cảm hòa hợp, hợp tác tốt, hôn nhân thành công."},
        "ĐinhBính": {"Tên_Cách_Cục": "Tinh Kỳ Vọng Trợ", "Cát_Hung": "Cát", "Luận_Giải": "Tốt cho văn thư, giấy tờ, thi cử."},
        "ĐinhĐinh": {"Tên_Cách_Cục": "Tinh Kỳ Phục Vịnh", "Cát_Hung": "Bình/Cát", "Luận_Giải": "Có lợi cho văn chương, thi cử, việc khác trì trệ."},
        "ĐinhMậu": {"Tên_Cách_Cục": "Thanh Long Chuyển Quang", "Cát_Hung": "Đại Cát", "Luận_Giải": "Tốt cho mọi việc, đặc biệt văn chương, thi cử, người đi xa."},
        "ĐinhKỷ": {"Tên_Cách_Cục": "Âm Cung", "Cát_Hung": "Đại Hung", "Luận_Giải": "Bị lừa gạt, mất của, kiện tụng thua kiện."},
        "ĐinhCanh": {"Tên_Cách_Cục": "Hỏa Kim Hình Cách", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho kiện tụng, đề phòng tiểu nhân."},
        "ĐinhTân": {"Tên_Cách_Cục": "Chu Tước Nhập Ngục", "Cát_Hung": "Đại Hung", "Luận_Giải": "Bị nhốt, kiện tụng bất lợi."},
        "ĐinhNhâm": {"Tên_Cách_Cục": "Nguyệt Hợp", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho kiện tụng, có nguy cơ phạm tội."},
        "ĐinhQuý": {"Tên_Cách_Cục": "Đằng Xà Giao", "Cát_Hung": "Hung", "Luận_Giải": "Cẩn thận lời nói, thị phi, kiện tụng."},
        # Mậu (Thiên)
        "MậuẤt": {"Tên_Cách_Cục": "Cầm Trác", "Cát_Hung": "Cát", "Luận_Giải": "Được người quý nhân phù trợ, dễ kiếm tiền."},
        "MậuBính": {"Tên_Cách_Cục": "Thanh Long Hồi Đầu", "Cát_Hung": "Đại Cát", "Luận_Giải": "Cực tốt, tiền của dồi dào, mọi sự hanh thông."},
        "MậuĐinh": {"Tên_Cách_Cục": "Thanh Long Chuyển Quang", "Cát_Hung": "Đại Cát", "Luận_Giải": "Tốt cho mọi việc, đặc biệt văn chương, thi cử."},
        "MậuMậu": {"Tên_Cách_Cục": "Phục Vịnh", "Cát_Hung": "Bình/Hung", "Luận_Giải": "Trì trệ, cần nhiều vốn, chậm lợi nhuận."},
        "MậuKỷ": {"Tên_Cách_Cục": "Thanh Long Nhập Thổ", "Cát_Hung": "Đại Hung", "Luận_Giải": "Hung tàn, dễ bị kiện tụng, khó khăn chồng chất."},
        "MậuCanh": {"Tên_Cách_Cục": "Trực Phù Phanh Cách", "Cát_Hung": "Đại Hung", "Luận_Giải": "Mất hết tiền tài, bị thương, cực xấu."},
        "MậuTân": {"Tên_Cách_Cục": "Thanh Long Hiến Giáp", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho kiện tụng, tranh chấp tài sản."},
        "MậuNhâm": {"Tên_Cách_Cục": "Thanh Long Đào Tẩu", "Cát_Hung": "Đại Hung", "Luận_Giải": "Xấu cho kiện tụng, tài sản bị mất mát, dễ bị cướp."},
        "MậuQuý": {"Tên_Cách_Cục": "Thanh Long Cấu Hợp", "Cát_Hung": "Hung", "Luận_Giải": "Hôn nhân, tình duyên xấu, dễ có quan hệ bất chính."},
        # Kỷ (Thiên)
        "KỷẤt": {"Tên_Cách_Cục": "Địa Hình Mộ Khắc", "Cát_Hung": "Hung", "Luận_Giải": "Xấu, dễ bị kiện cáo, cẩn thận người nhà."},
        "KỷBính": {"Tên_Cách_Cục": "Địa Hỏa Mộc Sinh", "Cát_Hung": "Cát", "Luận_Giải": "Tài lộc dồi dào, công việc phát triển."},
        "KỷĐinh": {"Tên_Cách_Cục": "Địa Tinh", "Cát_Hung": "Cát", "Luận_Giải": "Văn chương, thi cử tốt."},
        "KỷMậu": {"Tên_Cách_Cục": "Khuyển Nhập Địa Võng", "Cát_Hung": "Hung", "Luận_Giải": "Công việc khó khăn, bị lừa gạt, trộm cắp."},
        "KỷKỷ": {"Tên_Cách_Cục": "Địa Hộ Phục Vịnh", "Cát_Hung": "Bình/Hung", "Luận_Giải": "Công việc trì trệ, không thể tiến hành, nên nằm im."},
        "KỷCanh": {"Tên_Cách_Cục": "Hình Cách", "Cát_Hung": "Đại Hung", "Luận_Giải": "Xấu, dễ bị kiện cáo, phạt tù."},
        "KỷTân": {"Tên_Cách_Cục": "Hình Khắc", "Cát_Hung": "Hung", "Luận_Giải": "Cẩn thận kiện tụng, bị nhốt, mắc bệnh."},
        "KỷNhâm": {"Tên_Cách_Cục": "Địa Lưới", "Cát_Hung": "Hung", "Luận_Giải": "Đi lại không tốt, không nên ra ngoài, dễ mất của."},
        "KỷQuý": {"Tên_Cách_Cục": "Địa Võng", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho làm ăn, kiện tụng thất bại."},
        # Canh (Thiên)
        "CanhẤt": {"Tên_Cách_Cục": "Canh Cách", "Cát_Hung": "Đại Hung", "Luận_Giải": "Kiện tụng, thất bại, đề phòng tiểu nhân."},
        "CanhBính": {"Tên_Cách_Cục": "Canh Hỏa Tương Xung", "Cát_Hung": "Đại Hung", "Luận_Giải": "Dễ bị trộm cướp, lửa tai họa."},
        "CanhĐinh": {"Tên_Cách_Cục": "Hỏa Kim Tương Hình", "Cát_Hung": "Hung", "Luận_Giải": "Có người đến gây sự, kiện tụng không xong."},
        "CanhMậu": {"Tên_Cách_Cục": "Thiên Cách", "Cát_Hung": "Đại Hung", "Luận_Giải": "Rất xấu, tài sản bị mất, bị phạt."},
        "CanhKỷ": {"Tên_Cách_Cục": "Hình Cách", "Cát_Hung": "Hung", "Luận_Giải": "Kiện tụng, dễ bị phạt, cẩn thận tai nạn."},
        "CanhCanh": {"Tên_Cách_Cục": "Thái Bạch Phục Vịnh", "Cát_Hung": "Đại Hung", "Luận_Giải": "Chiến tranh, tai họa, không thể tiến hành, nên tránh."},
        "CanhTân": {"Tên_Cách_Cục": "Bạch Hổ Xung Khắc", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tai nạn giao thông, gặp tiểu nhân, bị phạt."},
        "CanhNhâm": {"Tên_Cách_Cục": "Bạch Hổ Xâm Đại", "Cát_Hung": "Đại Hung", "Luận_Giải": "Cẩn thận tai họa sông nước, kiện tụng tù tội."},
        "CanhQuý": {"Tên_Cách_Cục": "Bàng Quỹ", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tù tội, bệnh nặng, không thể thoát."},
        # Tân (Thiên)
        "TânẤt": {"Tên_Cách_Cục": "Thanh Long Triết Túc", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tàn tật, mất của, bệnh tật tái phát."},
        "TânBính": {"Tên_Cách_Cục": "Hợp Hình", "Cát_Hung": "Hung", "Luận_Giải": "Kiện tụng thua kiện, tai nạn, mất của."},
        "TânĐinh": {"Tên_Cách_Cục": "Chu Tước Nhập Ngục", "Cát_Hung": "Đại Hung", "Luận_Giải": "Bị nhốt, phạt tù."},
        "TânMậu": {"Tên_Cách_Cục": "Thanh Long Hiến Giáp", "Cát_Hung": "Hung", "Luận_Giải": "Kiện tụng bất lợi, cẩn thận trộm cướp."},
        "TânKỷ": {"Tên_Cách_Cục": "Hình Khắc", "Cát_Hung": "Hung", "Luận_Giải": "Dễ bị kiện cáo, cẩn thận mất của."},
        "TânCanh": {"Tên_Cách_Cục": "Bạch Hổ Xung Khắc", "Cát_Hung": "Đại Hung", "Luận_Giải": "Mất tiền, tai nạn."},
        "TânTân": {"Tên_Cách_Cục": "Thiên Đình Phục Vịnh", "Cát_Hung": "Bình/Hung", "Luận_Giải": "Kiện tụng bất lợi, việc chậm tiến."},
        "TânNhâm": {"Tên_Cách_Cục": "Thiên Lao Khổ", "Cát_Hung": "Đại Hung", "Luận_Giải": "Bị nhốt, kiện tụng không xong."},
        "TânQuý": {"Tên_Cách_Cục": "Thiên Đình Cấu Hợp", "Cát_Hung": "Hung", "Luận_Giải": "Kiện tụng liên miên, bệnh tật kéo dài."},
        # Nhâm (Thiên)
        "NhâmẤt": {"Tên_Cách_Cục": "Xà Yêu Triền Thân", "Cát_Hung": "Hung", "Luận_Giải": "Có thị phi, lừa gạt, hôn nhân xấu."},
        "NhâmBính": {"Tên_Cách_Cục": "Xà Thủy Vọng Giang", "Cát_Hung": "Đại Hung", "Luận_Giải": "Gặp tai họa sông nước, kiện tụng bất lợi."},
        "NhâmĐinh": {"Tên_Cách_Cục": "Thủy Hỏa Tương Sát", "Cát_Hung": "Hung", "Luận_Giải": "Kiện tụng, tranh chấp, dễ phạm tội."},
        "NhâmMậu": {"Tên_Cách_Cục": "Thanh Long Đào Tẩu", "Cát_Hung": "Đại Hung", "Luận_Giải": "Kiện tụng thua, mất của, bỏ trốn."},
        "NhâmKỷ": {"Tên_Cách_Cục": "Địa Lưới", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho đi lại, dễ bị nhốt, mất của."},
        "NhâmCanh": {"Tên_Cách_Cục": "Đại Bạch Hổ", "Cát_Hung": "Đại Hung", "Luận_Giải": "Bệnh tật nặng, dễ chết, cẩn thận tai nạn."},
        "NhâmTân": {"Tên_Cách_Cục": "Thiên Lao Khổ", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tù tội, bệnh tật khó chữa."},
        "NhâmNhâm": {"Tên_Cách_Cục": "Thiên Phạt Phục Vịnh", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tai họa, kiện tụng kéo dài, không nên hành động."},
        "NhâmQuý": {"Tên_Cách_Cục": "Thuyền Chìm", "Cát_Hung": "Đại Hung", "Luận_Giải": "Mất của, tai họa lớn, kiện tụng thua."},
        # Quý (Thiên)
        "QuýẤt": {"Tên_Cách_Cục": "Hoa Cái Mão Mệnh", "Cát_Hung": "Cát", "Luận_Giải": "Tốt cho công danh, có quý nhân phù trợ."},
        "QuýBính": {"Tên_Cách_Cục": "Hoa Cái", "Cát_Hung": "Hung", "Luận_Giải": "Dễ gặp thị phi, kiện tụng."},
        "QuýĐinh": {"Tên_Cách_Cục": "Đằng Xà Giao", "Cát_Hung": "Hung", "Luận_Giải": "Bị lừa gạt, gặp thị phi, kiện tụng."},
        "QuýMậu": {"Tên_Cách_Cục": "Thanh Long Cấu Hợp", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho hôn nhân, tình cảm, dễ có quan hệ bất chính."},
        "QuýKỷ": {"Tên_Cách_Cục": "Địa Võng", "Cát_Hung": "Hung", "Luận_Giải": "Xấu cho đi lại, dễ bị nhốt."},
        "QuýCanh": {"Tên_Cách_Cục": "Bàng Quỹ", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tù tội, bệnh tật nặng, không thể thoát."},
        "QuýTân": {"Tên_Cách_Cục": "Thiên Đình Cấu Hợp", "Cát_Hung": "Hung", "Luận_Giải": "Kiện tụng, tranh chấp kéo dài, bệnh tật khó chữa."},
        "QuýNhâm": {"Tên_Cách_Cục": "Thiên Võng", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tai họa, mất của, kiện tụng thua."},
        "QuýQuý": {"Tên_Cách_Cục": "Thiên Võng Phục Vịnh", "Cát_Hung": "Đại Hung", "Luận_Giải": "Tù tội, tai họa liên tiếp, không nên hành động."}
    },

    "TOPIC_INTERPRETATIONS": {
        "Kinh Doanh Tổng Quát": {"Dụng_Thần": ["Sinh Môn", "Mậu", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có kiếm được tiền không, lợi nhuận cao không. Sinh Môn = Lợi nhuận. Mậu = Vốn"},
        "Khai Trương Cửa Hàng": {"Dụng_Thần": ["Khai Môn", "Sinh Môn", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem ngày khai trương có tốt không. Khai Môn = Mở cửa. Sinh Môn = Tài lộc"},
        "Ký Kết Hợp Đồng": {"Dụng_Thần": ["Lục Hợp", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có ký được hợp đồng không. Lục Hợp = Hợp tác. Cảnh Môn = Văn bản"},
        "Đàm Phán Thương Mại": {"Dụng_Thần": ["Can Ngày", "Can Giờ", "Lục Hợp"], "Luận_Giải_Gợi_Ý": "Xem đàm phán có thành công không. Can Ngày = Mình. Can Giờ = Đối tác"},
        "Mua Bán Hàng Hóa": {"Dụng_Thần": ["Can Ngày", "Can Giờ", "Sinh Môn"], "Luận_Giải_Gợi_Ý": "Xem mua bán có lời không. Sinh Môn = Lợi nhuận"},
        "Đầu Tư Chứng Khoán": {"Dụng_Thần": ["Mậu", "Sinh Môn", "Bính/Đinh"], "Luận_Giải_Gợi_Ý": "Xem mua mã chứng khoán này có lời không. Mậu = Vốn đầu tư. Sinh Môn = Lợi nhuận. Bính/Đinh = Biến động đỏ/xanh"},
        "Đầu Tư Bất Động Sản": {"Dụng_Thần": ["Sinh Môn", "Tử Môn", "Mậu"], "Luận_Giải_Gợi_Ý": "Xem đầu tư nhà đất có sinh lời không. Sinh Môn = Nhà. Tử Môn = Đất"},
        "Vay Mượn Tiền Bạc": {"Dụng_Thần": ["Trực Phù", "Can Ngày", "Mậu"], "Luận_Giải_Gợi_Ý": "Xem có vay được tiền không. Trực Phù = Người cho vay"},
        "Đòi Nợ Thu Hồi": {"Dụng_Thần": ["Thương Môn", "Canh"], "Luận_Giải_Gợi_Ý": "Xem có đòi được nợ không. Thương Môn = Đòi nợ. Canh = Con nợ"},
        "Cầu Tài Lộc": {"Dụng_Thần": ["Sinh Môn", "Trực Phù", "Mậu"], "Luận_Giải_Gợi_Ý": "Xem có được tài lộc không. Sinh Môn = Tài. Trực Phù = Quý nhân"},
        "Mở Rộng Kinh Doanh": {"Dụng_Thần": ["Khai Môn", "Sinh Môn"], "Luận_Giải_Gợi_Ý": "Xem có mở rộng được không. Khai Môn = Mở rộng"},
        "Hợp Tác Đối Tác": {"Dụng_Thần": ["Lục Hợp", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem hợp tác có tốt không. Lục Hợp = Hợp tác"},
        "Xin Việc Làm": {"Dụng_Thần": ["Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có xin được việc không. Khai Môn = Công việc"},
        "Thăng Chức Thăng Tiến": {"Dụng_Thần": ["Khai Môn", "Trực Phù", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem có được thăng chức không. Khai Môn = Chức vụ. Trực Phù = Lãnh đạo"},
        "Chuyển Công Tác": {"Dụng_Thần": ["Khai Môn", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem có chuyển được không. Khai Môn = Việc mới. Mã Tinh = Di chuyển"},
        "Thi Đại Học": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Thiên Phụ"], "Luận_Giải_Gợi_Ý": "Xem có đỗ đại học không. Cảnh Môn = Bài thi. Đinh = Điểm"},
        "Hôn Nhân": {"Dụng_Thần": ["Ất", "Canh", "Lục Hợp"], "Luận_Giải_Gợi_Ý": "Xem có kết hôn được không. Ất = Nữ. Canh = Nam. Lục Hợp = Hôn nhân"},
        "Bệnh Tật Chữa Trị": {"Dụng_Thần": ["Thiên Nhuế", "Thiên Tâm", "Ất"], "Luận_Giải_Gợi_Ý": "Xem bệnh có khỏi không. Thiên Nhuế = Bệnh. Thiên Tâm = Thầy. Ất = Thuốc"},
        "Kiện Tụng": {"Dụng_Thần": ["Khai Môn", "Trực Phù", "Canh"], "Luận_Giải_Gợi_Ý": "Xem kiện tụng thắng hay thua. Khai Môn = Tòa. Trực Phù = Mình. Canh = Đối phương"},
        "Mua Nhà Đất": {"Dụng_Thần": ["Sinh Môn", "Tử Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có mua được nhà không. Sinh Môn = Nhà. Tử Môn = Đất"},
        "Xuất Hành Xa": {"Dụng_Thần": ["Mã Tinh", "Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem đi xa có thuận lợi không. Mã Tinh = Xe cộ. Khai Môn = Hướng đi"},
        "Du Lịch": {"Dụng_Thần": ["Hưu Môn", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem chuyến du lịch có vui không. Hưu Môn = Vui chơi. Cảnh Môn = Phong cảnh"},
        "Tìm Người Thất Lạc": {"Dụng_Thần": ["Lục Hợp", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem có tìm được người không. Lục Hợp = Hướng. Can Giờ = Người mất"},
        "Tìm Đồ Vật Mất": {"Dụng_Thần": ["Can Giờ", "Huyền Vũ"], "Luận_Giải_Gợi_Ý": "Xem có tìm được đồ không. Can Giờ = Vật. Huyền Vũ = Trộm"},
        "Gặp Quý Nhân": {"Dụng_Thần": ["Trực Phù", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có gặp quý nhân không. Trực Phù = Quý nhân"},
        "Thi Đấu Thể Thao": {"Dụng_Thần": ["Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem thi đấu thắng hay thua. Can Ngày = Mình. Can Giờ = Đối thủ"},
        "Thời Tiết": {"Dụng_Thần": ["Thiên Trụ", "Thiên Anh"], "Luận_Giải_Gợi_Ý": "Xem thời tiết mưa hay nắng. Thiên Trụ = Mưa. Thiên Anh = Nắng"},
        "Vận Mệnh Năm": {"Dụng_Thần": ["Can Năm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem vận mệnh cả năm. Can Năm = Vận năm"},
        "Cạnh Tranh Kinh Doanh": {"Dụng_Thần": ["Can Ngày", "Can Giờ", "Thương Môn"], "Luận_Giải_Gợi_Ý": "Xem có thắng đối thủ không. Can Ngày = Mình. Can Giờ = Đối thủ. Thương Môn = Cạnh tranh"},
        "Phá Sản Rủi Ro": {"Dụng_Thần": ["Tử Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có bị phá sản không. Tử Môn = Phá sản, ngưng trệ. Can Ngày = Mình"},
        "Xuất Nhập Khẩu": {"Dụng_Thần": ["Sinh Môn", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem xuất nhập khẩu có lời không. Sinh Môn = Lợi nhuận. Mã Tinh = Vận chuyển xa"},
        "Kinh Doanh Online": {"Dụng_Thần": ["Sinh Môn", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem kinh doanh online có thành công không. Sinh Môn = Lợi nhuận. Cảnh Môn = Thông tin, mạng lưới"},
        "Mở Chi Nhánh": {"Dụng_Thần": ["Khai Môn", "Sinh Môn", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem có nên mở chi nhánh không. Khai Môn = Mở mới. Sinh Môn = Lợi nhuận. Mã Tinh = Vị trí xa"},
        "Sáp Nhập Công Ty": {"Dụng_Thần": ["Lục Hợp", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem có nên sáp nhập không. Lục Hợp = Hợp nhất. Trực Phù = Lãnh đạo cao nhất"},
        "Phá Sản Thanh Lý": {"Dụng_Thần": ["Tử Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có nên thanh lý không. Tử Môn = Kết thúc, dừng lại. Can Ngày = Mình"},
        "Đấu Thầu Dự Án": {"Dụng_Thần": ["Khai Môn", "Trực Phù", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có trúng thầu không. Khai Môn = Dự án. Trực Phù = Chủ đầu tư. Can Ngày = Mình"},
        "Ký Quỹ Đảm Bảo": {"Dụng_Thần": ["Mậu", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem có nên ký quỹ không. Mậu = Tiền mặt. Trực Phù = Cơ quan đảm bảo"},
        "Bảo Lãnh Ngân Hàng": {"Dụng_Thần": ["Trực Phù", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có được bảo lãnh không. Trực Phù = Ngân hàng, uy tín lớn. Can Ngày = Mình"},
        "Vay Tín Chấp": {"Dụng_Thần": ["Trực Phù", "Mậu", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có vay được tín chấp không. Trực Phù = Ngân hàng. Mậu = Khoản vay. Can Ngày = Mình"},
        "Cho Vay Lãi Suất": {"Dụng_Thần": ["Sinh Môn", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem có nên cho vay không. Sinh Môn = Lãi suất. Can Giờ = Người vay"},
        "Đầu Tư Vàng Bạc": {"Dụng_Thần": ["Mậu", "Sinh Môn"], "Luận_Giải_Gợi_Ý": "Xem đầu tư vàng có lời không. Mậu = Vàng bạc, kim loại quý. Sinh Môn = Lời"},
        "Đầu Tư Ngoại Tệ": {"Dụng_Thần": ["Mậu", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem đầu tư ngoại tệ có lời không. Mậu = Tiền tệ. Thiên Bồng = Đầu cơ mạo hiểm"},
        "Kinh Doanh Xuất Khẩu": {"Dụng_Thần": ["Sinh Môn", "Mã Tinh", "Khai Môn"], "Luận_Giải_Gợi_Ý": "Xem xuất khẩu có lời không. Sinh Môn = Lời. Mã Tinh = Vận chuyển quốc tế. Khai Môn = Xuất đi"},
        "Nhập Khẩu Hàng Hóa": {"Dụng_Thần": ["Sinh Môn", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem nhập khẩu có lời không. Sinh Môn = Lợi nhuận. Mã Tinh = Hàng từ xa về"},
        "Kinh Doanh Dịch Vụ": {"Dụng_Thần": ["Sinh Môn", "Hưu Môn"], "Luận_Giải_Gợi_Ý": "Xem kinh doanh dịch vụ có lời không. Sinh Môn = Lợi nhuận. Hưu Môn = Giải trí, dịch vụ"},
        "Thương Mại Điện Tử": {"Dụng_Thần": ["Sinh Môn", "Cảnh Môn", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem thương mại điện tử có lời không. Sinh Môn = Lời. Cảnh Môn = Mạng. Thiên Bồng = Giao dịch trực tuyến"},
        "Phỏng Vấn Tuyển Dụng": {"Dụng_Thần": ["Khai Môn", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem phỏng vấn có đạt không. Khai Môn = Công việc. Cảnh Môn = Thông tin, phỏng vấn. Can Ngày = Mình"},
        "Nghỉ Việc Thôi Việc": {"Dụng_Thần": ["Khai Môn", "Tử Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có nên thôi việc không. Khai Môn = Công việc cũ. Tử Môn = Chấm dứt. Can Ngày = Mình"},
        "Bị Sa Thải": {"Dụng_Thần": ["Khai Môn", "Huyền Vũ", "Canh"], "Luận_Giải_Gợi_Ý": "Xem có bị mất việc không. Khai Môn = Việc. Huyền Vũ = Mất mát bí mật. Canh = Trở ngại kinh khủng"},
        "Thành Lập Công Ty": {"Dụng_Thần": ["Khai Môn", "Trực Phù", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem mở công ty mới có phát đạt bền vững không. Khai Môn = Sự khởi nghiệp. Can Giờ = Tương lai công ty"},
        "Thay Đổi Cấp Trên": {"Dụng_Thần": ["Trực Phù", "Can Năm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem sếp mới có tốt không. Trực Phù = Cấp trên. Can Năm = Sếp lớn. Can Ngày = Mình"},
        "Quan Hệ Đồng Nghiệp": {"Dụng_Thần": ["Lục Hợp", "Can Tháng", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem quan hệ với đồng nghiệp thế nào. Lục Hợp = Sự hòa hợp. Can Tháng = Đồng nghiệp. Can Ngày = Mình"},
        "Quan Hệ Lãnh Đạo": {"Dụng_Thần": ["Trực Phù", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem quan hệ với sếp trực tiếp. Trực Phù = Lãnh đạo. Can Ngày = Mình"},
        "Khen Thưởng Kỷ Luật": {"Dụng_Thần": ["Cảnh Môn", "Trực Phù", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem có được khen thưởng hay bị kỷ luật không. Cảnh Môn = Khen thưởng, giấy khen. Trực Phù = Lãnh đạo ra quyết định"},
        "Đi Công Tác": {"Dụng_Thần": ["Mã Tinh", "Khai Môn", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem chuyến công tác có thuận lợi không. Mã Tinh = Di chuyển. Khai Môn = Việc công. Can Giờ = Kết quả chuyến đi"},
        "Đào Tạo Bồi Dưỡng": {"Dụng_Thần": ["Thiên Phụ", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem học tập bồi dưỡng có tiến bộ không. Thiên Phụ = Thầy giáo, kiến thức. Can Ngày = Mình. Can Giờ = Kết quả học"},
        "Chứng Chỉ Hành Nghề": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem có lấy được chứng chỉ chuyên môn không. Cảnh Môn = Giấy tờ. Đinh = Văn bằng tước hiệu. Trực Phù = Cơ quan cấp"},
        "Bầu Cử Đề Bạt": {"Dụng_Thần": ["Trực Phù", "Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có được đề bạt vào vị trí mới không. Trực Phù = Cấp trên đề bạt. Khai Môn = Chức vụ mới. Can Ngày = Mình"},
        "Chức Danh Nghề Nghiệp": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem có đạt được học hàm/học vị/chức danh không. Cảnh Môn = Danh hiệu. Đinh = Bằng cấp. Can Năm = Nhà nước/Cơ quan"},
        "Môi Trường Làm Việc": {"Dụng_Thần": ["Khai Môn", "Cung vị"], "Luận_Giải_Gợi_Ý": "Xem môi trường làm việc mới thế nào. Khai Môn = Công việc. Cung chứa Khai Môn = Môi trường (Cung 9: nóng, Cung 1: lạnh...)"},
        "Áp Lực Công Việc": {"Dụng_Thần": ["Canh", "Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem công việc có quá áp lực không. Canh = Áp lực, khó khăn. Khai Môn = Việc. Can Ngày = Mình"},
        "Đánh Giá Nhân Sự": {"Dụng_Thần": ["Trực Phù", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem đánh giá cuối năm có tốt không. Trực Phù = Người đánh giá. Cảnh Môn = Bản đánh giá"},
        "Lương Thưởng Phúc Lợi": {"Dụng_Thần": ["Mậu", "Sinh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem lương thưởng có tăng không. Mậu = Lương cơ bản. Sinh Môn = Tiền thưởng. Can Ngày = Mình"},
        "Điều Động Luân Chuyển": {"Dụng_Thần": ["Khai Môn", "Mã Tinh", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có bị luân chuyển công tác không. Khai Môn = Việc. Mã Tinh = Điều động đi xa. Can Ngày = Mình"},
        "Nghỉ Hưu": {"Dụng_Thần": ["Khai Môn", "Hưu Môn", "Tử Môn"], "Luận_Giải_Gợi_Ý": "Xem nghỉ hưu có an nhàn không. Khai Môn = Sự nghiệp kết thúc. Hưu Môn = Nghỉ ngơi. Tử Môn = An nghỉ"},
        "Khởi Nghiệp Tự Do": {"Dụng_Thần": ["Sinh Môn", "Thiên Nhuế", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem làm Freelance/tự do có ổn không. Sinh Môn = Tiền tự kiếm. Thiên Nhuế = Chuyên môn cá nhân. Can Ngày = Mình"},
        "Nghề Phụ Tay Trái": {"Dụng_Thần": ["Sinh Môn", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem làm thêm nghề tay trái có lời không. Sinh Môn = Lợi nhuận. Can Giờ = Nghề phụ (Giao dịch thêm)"},
        "Uy Tín Thương Hiệu Cá Nhân": {"Dụng_Thần": ["Cảnh Môn", "Trực Phù", "Thiên Anh"], "Luận_Giải_Gợi_Ý": "Xem thương hiệu cá nhân có lên không. Cảnh Môn = Sự nổi tiếng. Trực Phù = Uy tín. Thiên Anh = Hình ảnh"},
        "Thi Tốt Nghiệp": {"Dụng_Thần": ["Cảnh Môn", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem có đỗ tốt nghiệp không. Cảnh Môn = Văn bằng, kết quả thi. Can Ngày = Thí sinh"},
        "Thi Tuyển Sinh lớp 10": {"Dụng_Thần": ["Khai Môn", "Cảnh Môn", "Thiên Phụ"], "Luận_Giải_Gợi_Ý": "Xem có đỗ vào trường mong muốn không. Khai Môn = Trường học. Cảnh Môn = Bài thi. Thiên Phụ = Kiến thức"},
        "Thi THPT Quốc Gia": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Canh"], "Luận_Giải_Gợi_Ý": "Xem kết quả thi THPT Quốc Gia. Cảnh Môn = Đề thi. Đinh = Điểm số. Canh = Trở ngại"},
        "Thi Chứng Chỉ Ngoại Ngữ": {"Dụng_Thần": ["Cảnh Môn", "Thiên Phụ", "Canh"], "Luận_Giải_Gợi_Ý": "Xem có đạt chứng chỉ IELTS/TOEIC... không. Cảnh Môn = Chứng chỉ. Thiên Phụ = Ngôn ngữ. Canh = Khó khăn bài thi"},
        "Thi Cao Học": {"Dụng_Thần": ["Thiên Phụ", "Đinh", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem thi Thạc sĩ có đỗ không. Thiên Phụ = Tri thức cao. Đinh = Tước hiệu. Cảnh Môn = Bài thi"},
        "Thi Tiến Sĩ": {"Dụng_Thần": ["Cảnh Môn", "Trực Phù", "Thiên Phụ"], "Luận_Giải_Gợi_Ý": "Xem bảo vệ luận án Tiến sĩ có thành công không. Cảnh Môn = Luận án. Trực Phù = Hội đồng chấm. Thiên Phụ = Kiến thức chuyên sâu"},
        "Thi Nâng Bậc Chuyên Môn": {"Dụng_Thần": ["Khai Môn", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem thi nâng ngạch, nâng bậc có đỗ không. Khai Môn = Ngạch công tác. Cảnh Môn = Bài thi sát hạch"},
        "Thi Công Chức Viên Chức": {"Dụng_Thần": ["Khai Môn", "Trực Phù", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem thi vào nhà nước có đỗ không. Khai Môn = Cơ quan nhà nước. Trực Phù = Người tuyển dụng. Can Năm = Chính sách"},
        "Học Bổng Du Học": {"Dụng_Thần": ["Thiên Phụ", "Cảnh Môn", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem có xin được học bổng đi nước ngoài không. Thiên Phụ = Học bổng. Cảnh Môn = Giấy tờ. Mã Tinh = Đi xa"},
        "Chọn Trường Học": {"Dụng_Thần": ["Khai Môn", "Thiên Phụ", "Cung vị"], "Luận_Giải_Gợi_Ý": "Xem chọn trường này có tốt cho tương lai không. Khai Môn = Trường học. Cung chứa Khai Môn = Chất lượng trường"},
        "Chọn Ngành Học": {"Dụng_Thần": ["Khai Môn", "Sinh Môn", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem chọn ngành này sau này có việc làm tốt không. Khai Môn = Nghề nghiệp. Sinh Môn = Thu nhập sau này. Can Giờ = Kết quả"},
        "Kết Quả Học Tập": {"Dụng_Thần": ["Cảnh Môn", "Thiên Phụ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem điểm số, học lực học kỳ này. Cảnh Môn = Điểm số. Thiên Phụ = Sức học. Can Ngày = Mình"},
        "Quan Hệ Thầy Trò": {"Dụng_Thần": ["Thiên Phụ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem quan hệ với thầy cô giáo. Thiên Phụ = Thầy giáo. Can Ngày = Học trò"},
        "Đỗ Hay Trượt": {"Dụng_Thần": ["Cảnh Môn", "Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem kết quả thi cử cuối cùng. Cảnh Môn = Điểm. Khai Môn = Đỗ vào. Can Ngày = Mình"},
        "Tìm Bạn Đời": {"Dụng_Thần": ["Ất (Nữ)", "Canh (Nam)", "Lục Hợp"], "Luận_Giải_Gợi_Ý": "Xem khi nào gặp được ý trung nhân. Ất = Nữ. Canh = Nam. Lục Hợp = Duyên phận"},
        "Tình Duyên Tổng Quát": {"Dụng_Thần": ["Lục Hợp", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem vận trình tình cảm trong giai đoạn này. Lục Hợp = Tình cảm. Can Ngày = Mình. Can Giờ = Chuyện tình cảm"},
        "Xem Tuổi Hợp Hôn Nhân": {"Dụng_Thần": ["Ất", "Canh", "Can Năm sinh của 2 người"], "Luận_Giải_Gợi_Ý": "Xem hai người có hợp tuổi để kết hôn không. Ất = Nữ. Canh = Nam. Can Năm = Mệnh tuổi"},
        "Đính Hôn Ăn Hỏi": {"Dụng_Thần": ["Lục Hợp", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem lễ đính hôn có thuận lợi không. Lục Hợp = Hôn ước. Cảnh Môn = Lễ nghi rình rang"},
        "Đám Cưới": {"Dụng_Thần": ["Lục Hợp", "Hưu Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem việc tổ chức đám cưới. Lục Hợp = Hôn sự. Hưu Môn = Vui vẻ, nghỉ ngơi, ngày lễ"},
        "Hòa Hợp Vợ Chồng": {"Dụng_Thần": ["Lục Hợp", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem đời sống vợ chồng có ấm êm không. Lục Hợp = Sự hòa thuận. Can Ngày = Mình. Can Giờ = Bạn đời"},
        "Mâu Thuẫn Gia Đình": {"Dụng_Thần": ["Canh", "Thương Môn", "Lục Hợp"], "Luận_Giải_Gợi_Ý": "Xem nguyên nhân và cách hóa giải mâu thuẫn. Canh = Xung đột. Thương Môn = Cãi vã. Lục Hợp = Gia đình"},
        "Ngoại Tình Người Thứ Ba": {"Dụng_Thần": ["Ất", "Canh", "Can Khác"], "Luận_Giải_Gợi_Ý": "Xem có người thứ ba xen vào không. Ất = Vợ/Nữ. Canh = Chồng/Nam. Can khác lâm Lục Hợp = Có người thứ ba"},
        "Ly Hôn Ly Thân": {"Dụng_Thần": ["Tử Môn", "Lục Hợp", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có dẫn đến ly hôn không. Tử Môn = Chấm dứt. Lục Hợp = Hôn nhân"},
        "Tái Hợp Người Yêu Cũ": {"Dụng_Thần": ["Canh", "Ất", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem có quay lại với người cũ được không. Canh/Ất = Người cũ. Trực Phù = Phục ngâm (quay lại)"},
        "Người Yêu Phương Xa": {"Dụng_Thần": ["Lục Hợp", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem tình cảm với người ở xa. Lục Hợp = Tình cảm. Mã Tinh = Khoảng cách địa lý"},
        "Tình Yêu Đơn Phương": {"Dụng_Thần": ["Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem người kia có tình cảm với mình không. Can Ngày = Mình. Can Giờ = Người mình thầm yêu"},
        "Mai Mối Giới Thiệu": {"Dụng_Thần": ["Lục Hợp", "Can Tháng"], "Luận_Giải_Gợi_Ý": "Xem người được giới thiệu có hợp không. Lục Hợp = Mai mối. Can Tháng = Người giới thiệu"},
        "Con Cái Sau Hôn Nhân": {"Dụng_Thần": ["Sinh Môn", "Thiên Nhuế"], "Luận_Giải_Gợi_Ý": "Xem khi nào có con, con cái thế nào. Sinh Môn = Sinh sản. Thiên Nhuế = Tử cung, thai nghén"},
        "Mẹ Chồng Nàng Dâu": {"Dụng_Thần": ["Can Năm (Mẹ)", "Ất (Dâu)"], "Luận_Giải_Gợi_Ý": "Xem quan hệ giữa mẹ chồng và nàng dâu. Can Năm = Mẹ chồng. Ất = Nàng dâu"},
        "Gia Đình Nội Ngoại": {"Dụng_Thần": ["Can Năm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem quan hệ với hai bên gia đình. Can Năm = Bố mẹ/Hàng gia trưởng. Can Ngày = Vợ chồng"},
        "Sự Phản Bội": {"Dụng_Thần": ["Huyền Vũ", "Thiên Nhuế", "Lục Hợp"], "Luận_Giải_Gợi_Ý": "Xem có bị phản bội trong tình cảm không. Huyền Vũ = Sự lừa dối. Thiên Nhuế = Sai lầm. Lục Hợp = Hôn nhân"},
        "Xem Ngày Kết Hôn": {"Dụng_Thần": ["Can Ngày", "Can Giờ", "Lục Hợp"], "Luận_Giải_Gợi_Ý": "Xem ngày này cưới có đại cát không. Can Ngày = Ngày cưới. Can Giờ = Giờ cưới. Lục Hợp = Sự kết hợp"},
        "Hẹn Hò Lần Đầu": {"Dụng_Thần": ["Hưu Môn", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem buổi hẹn đầu tiên có ấn tượng tốt không. Hưu Môn = Vui vẻ thư giãn. Cảnh Môn = Vẻ bề ngoài"},
        "Sức Khỏe Tổng Quát": {"Dụng_Thần": ["Thiên Nhuế", "Can Ngày", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem tình trạng sức khỏe hiện tại. Thiên Nhuế = Bệnh tật. Can Ngày = Bản thân. Trực Phù = Sức đề kháng"},
        "Xem Bệnh Nan Y": {"Dụng_Thần": ["Thiên Nhuế", "Tử Môn", "Thiên Tâm"], "Luận_Giải_Gợi_Ý": "Xem bệnh nặng có chữa được không. Thiên Nhuế = Bệnh. Tử Môn = Nguy hiểm tính mạng. Thiên Tâm = Thầy thuốc"},
        "Phẫu Thuật Cấp Cứu": {"Dụng_Thần": ["Thiên Tâm", "Canh", "Thiên Nhuế"], "Luận_Giải_Gợi_Ý": "Xem ca mổ có thành công không. Thiên Tâm = Bác sĩ phẫu thuật. Canh = Dao kéo. Thiên Nhuế = Vết thương"},
        "Thai Sản Quá Trình": {"Dụng_Thần": ["Thiên Nhuế", "Côn", "Sinh Môn"], "Luận_Giải_Gợi_Ý": "Xem quá trình mang thai có ổn định không. Thiên Nhuế = Thai nhi. Côn = Mẹ mang bầu. Sinh Môn = Sự phát triển"},
        "Sinh Con Chuyển Dạ": {"Dụng_Thần": ["Khai Môn", "Sinh Môn", "Thiên Nhuế"], "Luận_Giải_Gợi_Ý": "Xem việc sinh nở có dễ dàng không. Khai Môn = Cửa tử cung mở. Sinh Môn = Đứa trẻ chào đời"},
        "Bệnh Tâm Thần Trầm Cảm": {"Dụng_Thần": ["Thiên Nhuế", "Đằng Xà", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem tình trạng tâm lý, thần kinh. Thiên Nhuế = Bệnh. Đằng Xà = Tâm thần rối loạn. Can Ngày = Mình"},
        "Bệnh Xương Khớp": {"Dụng_Thần": ["Thiên Nhuế", "Cung 6/7/8"], "Luận_Giải_Gợi_Ý": "Xem bệnh về xương, cột sống. Cung 6, 7, 8 tượng cho khung xương và tay chân"},
        "Bệnh Tiêu Hóa": {"Dụng_Thần": ["Thiên Nhuế", "Cung 2/5/8"], "Luận_Giải_Gợi_Ý": "Xem bệnh dạ dày, đường ruột. Cung 2 (Khôn), 5 (Trung), 8 (Cấn) thuộc Thổ tượng cho hệ tiêu hóa"},
        "Bệnh Hô Hấp": {"Dụng_Thần": ["Thiên Nhuế", "Cung 7"], "Luận_Giải_Gợi_Ý": "Xem bệnh phổi, mũi họng. Cung 7 (Đoài) tượng cho phổi và cuống họng"},
        "Bệnh Tim Mạch": {"Dụng_Thần": ["Thiên Nhuế", "Cung 9"], "Luận_Giải_Gợi_Ý": "Xem bệnh liên quan đến tim, huyết áp. Cung 9 (Ly) tượng cho tim và huyết áp"},
        "Tìm Thầy Tìm Thuốc": {"Dụng_Thần": ["Thiên Tâm", "Ất", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có gặp được bác sĩ giỏi không. Thiên Tâm = Bác sĩ. Ất = Đơn thuốc. Can Ngày = Mình"},
        "Tai Nạn Thương Tích": {"Dụng_Thần": ["Canh", "Bạch Hổ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có gặp tai nạn đột ngột không. Canh = Va chạm. Bạch Hổ = Máu huyết, tai nạn. Can Ngày = Mình"},
        "Sức Khỏe Người Già": {"Dụng_Thần": ["Can Năm", "Thiên Nhuế", "Cửu Địa"], "Luận_Giải_Gợi_Ý": "Xem sức khỏe cho cha mẹ, ông bà cao tuổi. Can Năm = Người già. Thiên Nhuế = Bệnh. Cửu Địa = Thọ"},
        "Sức Khỏe Trẻ Em": {"Dụng_Thần": ["Thiên Nhuế", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem trẻ nhỏ đau ốm thế nào. Can Giờ = Trẻ nhỏ. Thiên Nhuế = Bệnh"},
        "Di Chứng Sau Bệnh": {"Dụng_Thần": ["Thiên Nhuế", "Tử Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem sau khi khỏi bệnh có để lại di chứng gì không. Thiên Nhuế = Gốc bệnh. Tử Môn = Chú chết, di chứng"},
        "Ngày Đi Khám Bệnh": {"Dụng_Thần": ["Thiên Tâm", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem chọn ngày nào đi khám cho chuẩn. Can Ngày = Ngày khám. Can Giờ = Kết quả khám"},
        "Hiếm Muộn Vô Sinh": {"Dụng_Thần": ["Sinh Môn", "Thiên Nhuế", "Tử Môn"], "Luận_Giải_Gợi_Ý": "Xem nguyên nhân và khả năng có con. Tử Môn lâm cung Thai = Khó có con. Sinh Môn lâm Không = Hết hy vọng"},
        "Nguyên Nhân Bệnh Tật": {"Dụng_Thần": ["Thiên Nhuế", "Cửu Thiên / Cửu Địa"], "Luận_Giải_Gợi_Ý": "Xem bệnh do tạng phủ hay do tâm linh. Cửu Thiên = Do thời tiết/trời. Cửu Địa = Do ăn uống/đất"},
        "Phục Hồi Sức Khỏe": {"Dụng_Thần": ["Thiên Tâm", "Sinh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem sau ốm có mau khỏe lại không. Thiên Tâm = Thuốc. Sinh Môn = Sức sống mới"},
        "Thắng Thua Kiện Tụng": {"Dụng_Thần": ["Khai Môn", "Kinh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem kết quả cuối cùng của vụ kiện. Khai Môn = Thẩm phán. Kinh Môn = Kiện tụng. Can Ngày = Mình"},
        "Thời Điểm Khởi Kiện": {"Dụng_Thần": ["Khai Môn", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem khi nào nộp đơn kiện là tốt nhất. Khai Môn = Tòa tiếp nhận. Can Giờ = Kết quả nộp đơn"},
        "Thuê Luật Sư": {"Dụng_Thần": ["Trực Phù", "Thiên Tâm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem luật sư có giỏi và giúp được mình không. Trực Phù = Luật sư bảo vệ. Thiên Tâm = Trí tuệ luật pháp"},
        "Hòa Giải Dân Sự": {"Dụng_Thần": ["Lục Hợp", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem hai bên có thể hòa giải thỏa đáng không. Lục Hợp = Sự thỏa hiệp, trung gian"},
        "Bị Khởi Kiện": {"Dụng_Thần": ["Kinh Môn", "Can Giờ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem mình bị người khác kiện có sao không. Can Giờ = Người kiện mình. Kinh Môn = Rắc rối pháp lý"},
        "Tranh Chấp Đất Đai": {"Dụng_Thần": ["Tử Môn", "Khai Môn", "Thổ"], "Luận_Giải_Gợi_Ý": "Xem kiện tụng về đất đai sẽ thế nào. Tử Môn = Đất đai. Khai Môn = Tòa xét xử"},
        "Tranh Chấp Tài Sản": {"Dụng_Thần": ["Mậu", "Sinh Môn", "Kinh Môn"], "Luận_Giải_Gợi_Ý": "Xem kiện đòi lại tài sản/tiền bạc. Mậu = Tiền gốc. Sinh Môn = Tài sản. Kinh Môn = Tranh chấp"},
        "Thừa Kế Pháp Luật": {"Dụng_Thần": ["Can Năm", "Lục Hợp", "Sinh Môn"], "Luận_Giải_Gợi_Ý": "Xem việc phân chia thừa kế có công bằng không. Can Năm = Tổ tiên để lại. Lục Hợp = Phân chia. Sinh Môn = Sản nghiệp"},
        "Thi Hành Bản Án": {"Dụng_Thần": ["Canh", "Khai Môn", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem bản án có được thực thi nhanh không. Canh = Cưỡng chế. Khai Môn = Lệnh thi hành"},
        "Bị Bắt Giữ Tạm Giam": {"Dụng_Thần": ["Địa Vong", "Kinh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem người bị bắt có sớm được ra không. Địa Vong = Lưới đất, giam giữ. Kinh Môn = Cửa ngục"},
        "Mua Nhà Chung Cư": {"Dụng_Thần": ["Sinh Môn", "Cảnh Môn", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem mua chung cư có tốt và pháp lý ổn không. Sinh Môn = Nhà. Cảnh Môn = Giấy tờ pháp lý chung cư"},
        "Bán Nhà Đất": {"Dụng_Thần": ["Sinh Môn", "Can Giờ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem bán nhà có nhanh và được giá không. Can Giờ = Người mua. Sinh Môn = Giá bán"},
        "Sửa Chữa Nhà Cửa": {"Dụng_Thần": ["Sinh Môn", "Thiên Nhuế", "Canh"], "Luận_Giải_Gợi_Ý": "Xem sửa nhà có thuận lợi, thợ tốt không. Thiên Nhuế = Chỗ cần sửa. Canh = Thợ thuyền dao kéo"},
        "Thuê Nhà Ở": {"Dụng_Thần": ["Sinh Môn", "Trực Phù", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem nhà thuê có hợp phong thủy, chủ nhà tốt không. Trực Phù = Chủ nhà. Sinh Môn = Nhà thuê"},
        "Thiết Kế Kiến Trúc": {"Dụng_Thần": ["Cảnh Môn", "Sinh Môn", "Thiên Phụ"], "Luận_Giải_Gợi_Ý": "Xem thiết kế nhà có đẹp và hợp không. Cảnh Môn = Bản vẽ. Thiên Phụ = Kiến trúc sư"},
        "Chọn Hướng Nhà": {"Dụng_Thần": ["Sinh Môn", "Cung vị hướng nhà"], "Luận_Giải_Gợi_Ý": "Xem hướng nhà này có đại cát không. Sinh Môn lâm hướng nào thì hướng đó quan trọng"},
        "Thủ Tục Đất Đai": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem làm sổ đỏ, giấy tờ đất có thông không. Cảnh Môn = Giấy tờ. Đinh = Hồ sơ. Trực Phù = Cơ quan duyệt"},
        "Phong Thủy Nhà Ở": {"Dụng_Thần": ["Sinh Môn", "Trực Phù", "Cửu Địa"], "Luận_Giải_Gợi_Ý": "Xem phong thủy nhà có vượng tài lộc không. Sinh Môn = Khí của nhà. Cửu Địa = Khí của đất"},
        "Chuyển Về Nhà Mới": {"Dụng_Thần": ["Sinh Môn", "Hưu Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem ngày giờ nhập trạch có đại cát không. Sinh Môn = Nhà mới. Hưu Môn = Sự an cư. Can Ngày = Mình"},
        "Giải Phóng Mặt Bằng": {"Dụng_Thần": ["Khai Môn", "Tử Môn", "Mậu"], "Luận_Giải_Gợi_Ý": "Xem đền bù giải tỏa có thỏa đáng không. Khai Môn = Cơ quan nhà nước. Tử Môn = Đất bị thu hồi. Mậu = Tiền đền bù"},
        "Đi Xuất Khẩu Lao Động": {"Dụng_Thần": ["Mã Tinh", "Khai Môn", "Thiên Phụ"], "Luận_Giải_Gợi_Ý": "Xem đi nước ngoài làm việc có tốt không. Mã Tinh = Xuất ngoại. Khai Môn = Việc làm. Thiên Phụ = Kiến thức tay nghề"},
        "Thủ Tục Visa Hộ Chiếu": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem xin visa có đạt không. Cảnh Môn = Visa. Đinh = Hộ chiếu. Trực Phù = Đại sứ quán"},
        "Định Cư Nước Ngoài": {"Dụng_Thần": ["Sinh Môn", "Mã Tinh", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem định cư lâu dài có ổn không. Sinh Môn = Nơi ở mới. Mã Tinh = Sự di dời. Can Năm = Người lãnh đạo quốc gia"},
        "Sự Cố Trên Đường Đi": {"Dụng_Thần": ["Canh", "Bạch Hổ", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem hành trình có gặp tai nạn/hỏng xe không. Canh = Va chạm. Bạch Hổ = Tai nạn. Cảnh Môn = Lộ hành"},
        "Mất Hành Lý": {"Dụng_Thần": ["Huyền Vũ", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem hành lý có bị thất lạc trên đường không. Huyền Vũ = Mất mát bí mật. Can Giờ = Hành lý"},
        "Tìm Tài Liệu Mất": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem tài liệu quan trọng bị mất ở đâu. Cảnh Môn = Tài liệu, sách vở. Đinh = Thông tin lưu trữ"},
        "Tìm Thú Cưng Lạc": {"Dụng_Thần": ["Tử Tôn (Quái)", "Thiên Nhuế", "Cung"], "Luận_Giải_Gợi_Ý": "Xem thú cưng đi lạc về hướng nào. Thiên Nhuế = Vật nuôi bệnh/lạc. Cung = Hướng tìm"},
        "Bị Lừa Đảo Tài Chính": {"Dụng_Thần": ["Huyền Vũ", "Thiên Bồng", "Mậu"], "Luận_Giải_Gợi_Ý": "Xem có bị kẻ gian lừa tiền không. Huyền Vũ = Kẻ gian. Thiên Bồng = Đại tặc. Mậu = Tiền"},
        "Thông Tin Sai Lệch": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Đằng Xà"], "Luận_Giải_Gợi_Ý": "Xem tin đồn hoặc thông tin nhận được có thật không. Cảnh Môn = Tin tức. Đằng Xà = Sự giả tạo, không thật"},
        "Gia Nhập Câu Lạc Bộ": {"Dụng_Thần": ["Lục Hợp", "Hưu Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem tham gia hội nhóm có vui và lợi không. Lục Hợp = Hội nhóm. Hưu Môn = Vui chơi giải trí"},
        "Tổ Chức Sự Kiện": {"Dụng_Thần": ["Cảnh Môn", "Trực Phù", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem sự kiện nổ ra có thành công tốt đẹp không. Cảnh Môn = Sự kiện vinh quang. Can Giờ = Kết quả buổi lễ"},
        "Thi Đấu Esport": {"Dụng_Thần": ["Khai Môn", "Cảnh Môn", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem thi đấu game điện tử có thắng không. Khai Môn = Trận đấu. Cảnh Môn = Mạng/Skill. Thiên Bồng = Chiến thuật"},
        "Dẫn Đầu Xu Hướng": {"Dụng_Thần": ["Thiên Anh", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem mình có tạo được trend thành công không. Thiên Anh = Sự nổi bật. Cảnh Môn = Trendy. Can Ngày = Mình"},
        "Gặp Gỡ Thần Tượng": {"Dụng_Thần": ["Thiên Anh", "Trực Phù", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có cơ hội gặp người mình hâm mộ không. Thiên Anh = Ngôi sao/Thần tượng. Can Ngày = Mình"},
        "Tìm Đồ May Mắn": {"Dụng_Thần": ["Lục Hợp", "Thiên Tâm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem tìm vật phẩm phong thủy/may mắn bị lạc. Lục Hợp = Vật phẩm gắn kết. Thiên Tâm = Đồ có giá trị tinh thần"},
        "Xung Đột Hàng Xóm": {"Dụng_Thần": ["Lục Hợp", "Thương Môn", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem mâu thuẫn với hàng xóm có giải quyết được không. Can Giờ = Hàng xóm. Thương Môn = Cãi vã. Lục Hợp = Quan hệ"},
        "Tham Gia Biểu Diễn": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem buổi biểu diễn sân khấu có thành công không. Cảnh Môn = Sân khấu rực lửa. Thiên Anh = Tài năng diễn xuất"},
        "Xem Ngày Xuất Hành": {"Dụng_Thần": ["Mã Tinh", "Hưu Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem chọn ngày giờ đi xa cho đại cát. Mã Tinh = Sự chuyển dịch. Hưu Môn = Điềm lành khi đi"},
        "Gặp Tin Tức Giả": {"Dụng_Thần": ["Huyền Vũ", "Đằng Xà", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem thông tin này có phải lừa bịp không. Huyền Vũ = Mờ ám. Đằng Xà = Giả dối. Cảnh Môn = Tin tức"},
        "Thi Tuyển Idol": {"Dụng_Thần": ["Thiên Anh", "Cảnh Môn", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem thi vào làm thực tập sinh/Idol có đỗ không. Thiên Anh = Tài năng tỏa sáng. Cảnh Môn = Ngành giải trí"},
        "Công Việc Freelance": {"Dụng_Thần": ["Sinh Môn", "Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem làm nghề tự do có ổn định thu nhập không. Sinh Môn = Lợi nhuận. Khai Môn = Tính chất việc"},
        "Xây Dựng Website": {"Dụng_Thần": ["Cảnh Môn", "Khai Môn", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem làm web có thu hút nhiều người truy cập không. Cảnh Môn = Giao diện web. Khai Môn = Public. Thiên Bồng = Online"},
        "Dịch Vụ Tư Vấn": {"Dụng_Thần": ["Thiên Tâm", "Thiên Phụ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem làm nghề tư vấn có đắt khách không. Thiên Tâm = Lời khuyên. Thiên Phụ = Kiến thức tư vấn"},
        "Trở Thành Youtuber": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem làm kênh Youtube có thành công, nổi tiếng không. Thiên Anh = Hình ảnh cá nhân. Cảnh Môn = Kênh nội dung"},
        "Quay Phim Chụp Ảnh": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Canh"], "Luận_Giải_Gợi_Ý": "Xem buổi quay/chụp có cho sản phẩm đẹp không. Cảnh Môn = Sản phẩm hình ảnh. Thiên Anh = Mỹ thuật"},
        "Thiết Kế Nội Thất": {"Dụng_Thần": ["Sinh Môn", "Cảnh Môn", "Thiên Phụ"], "Luận_Giải_Gợi_Ý": "Xem trang trí nhà cửa có đẹp và hợp ý không. Sinh Môn = Ngôi nhà. Cảnh Môn = Nội thất thẩm mỹ"},
        "Làm Nghề Thủ Công": {"Dụng_Thần": ["Thiên Nhuế", "Sinh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem làm đồ Handmade có khách mua không. Thiên Nhuế = Kỹ năng tay chân. Sinh Môn = Bán đồ có lời"},
        "Viết Sách Tác Giả": {"Dụng_Thần": ["Cảnh Môn", "Thiên Phụ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem viết sách có nổi tiếng và xuất bản được không. Cảnh Môn = Cuốn sách. Thiên Phụ = Văn chương chữ nghĩa"},
        "Thiết Kế Đồ Họa": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem sản phẩm Design có được khách duyệt không. Cảnh Môn = Bản thiết kế. Can Giờ = Khách hàng"},
        "Học Nghề Làm Đẹp": {"Dụng_Thần": ["Thiên Anh", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem học nghề Spa/Makeup... có thành công không. Thiên Anh = Thẩm mỹ. Cảnh Môn = Nghề làm đẹp"},
        "Sáng Tạo Nội Dung": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem làm Content Creator có nhiều Follow không. Cảnh Môn = Content. Thiên Anh = Sáng tạo. Can Giờ = Fans"},
        "Cầu Tự Cúng Bái": {"Dụng_Thần": ["Trực Phù", "Thiên Nhuế", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem việc cúng bái có được linh ứng không. Trực Phù = Thần linh. Thiên Nhuế = Vật cúng. Can Ngày = Người cúng"},
        "Giải Hạn Tam Tai": {"Dụng_Thần": ["Thiên Tâm", "Lục Hợp", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem giải hạn có bớt vận rủi không. Thiên Tâm = Sự cứu giải. Lục Hợp = Hóa giải xung đột"},
        "Xem Đồng Thầy": {"Dụng_Thần": ["Trực Phù", "Thiên Tâm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem thầy cúng có thực tài và định hướng đúng không. Trực Phù = Thầy có căn cơ. Thiên Tâm = Đạo hạnh"},
        "Mồ Mả Gia Tiên": {"Dụng_Thần": ["Tử Môn", "Can Năm", "Cửu Địa"], "Luận_Giải_Gợi_Ý": "Xem mồ mả có yên ổn hay bị động. Tử Môn = Ngôi mộ. Can Năm = Tổ tiên. Cửu Địa = Đất mộ"},
        "Tu Tập Thiền Định": {"Dụng_Thần": ["Hưu Môn", "Thiên Tâm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem việc tu tập có tiến bộ, tâm có tịnh không. Hưu Môn = Trạng thái tĩnh. Thiên Tâm = Tâm linh cao"},
        "Vật Phẩm Tâm Linh": {"Dụng_Thần": ["Trực Phù", "Thiên Tâm", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem linh vật/vòng tay có năng lượng tốt không. Trực Phù = Linh khí. Thiên Tâm = Sự hộ mệnh. Cảnh Môn = Vẻ ngoài"},
        "Mua Xe Ô Tô": {"Dụng_Thần": ["Khai Môn", "Cảnh Môn", "Mã Tinh"], "Luận_Giải_Gợi_Ý": "Xem mua xe có bền, đi đứng an toàn không. Khai Môn = Máy móc. Cảnh Môn = Ngoại thất. Mã Tinh = Di chuyển"},
        "Mất Điện Thoại": {"Dụng_Thần": ["Cảnh Môn", "Đinh", "Huyền Vũ"], "Luận_Giải_Gợi_Ý": "Xem điện thoại mất có tìm lại được không. Cảnh Môn = Điện thoại. Đinh = Chíp/Sim. Huyền Vũ = Mất trộm"},
        "Đồ Vật Gia Bảo": {"Dụng_Thần": ["Cửu Địa", "Can Năm", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem đồ cổ/đồ gia bảo trong nhà có linh không. Cửu Địa = Đồ lâu đời. Can Năm = Tổ tiên để lại"},
        "Thời Tiết Đi Du Lịch": {"Dụng_Thần": ["Thiên Anh", "Thiên Trụ", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem ngày đi du lịch trời có đẹp không. Thiên Anh = Trời nắng đẹp. Thiên Trụ = Mưa bão"},
        "Dự Báo Mưa Bão": {"Dụng_Thần": ["Thiên Trụ", "Thiên Phụ", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem sắp tới có mưa to bão lớn không. Thiên Trụ = Gió bão. Thiên Bồng = Mưa lớn"},
        "Thiên Tai Động Đất": {"Dụng_Thần": ["Tử Môn", "Thiên Nhuế", "Cửu Địa"], "Luận_Giải_Gợi_Ý": "Xem vùng này có nguy cơ thiên tai không. Tử Môn = Đất chết. Thiên Nhuế = Tai ương. Cửu Địa = Địa tầng"},
        "Vụ Mùa Bội Thu": {"Dụng_Thần": ["Sinh Môn", "Thiên Nhuế", "Can Năm"], "Luận_Giải_Gợi_Ý": "Xem mùa màng nông nghiệp có được mùa không. Sinh Môn = Sản vật. Thiên Nhuế = Đất/Nông nghiệp"},
        "Phát Triển Chăn Nuôi": {"Dụng_Thần": ["Thiên Nhuế", "Sinh Môn", "Thiên Bồng"], "Luận_Giải_Gợi_Ý": "Xem nuôi gia súc có thuận lợi không. Thiên Nhuế = Con giống. Sinh Môn = Phát triển. Thiên Bồng = Lợn/Thủy sản"},
        "Đánh Bắt Thủy Sản": {"Dụng_Thần": ["Thiên Bồng", "Hưu Môn", "Thê Tài"], "Luận_Giải_Gợi_Ý": "Xem đi biển, đánh cá có trúng đậm không. Thiên Bồng = Cá/Thủy sản. Hưu Môn = Sông biển"},
        "Tìm Nguồn Nước": {"Dụng_Thần": ["Hưu Môn", "Thiên Bồng", "Khảm"], "Luận_Giải_Gợi_Ý": "Xem khoan giếng, tìm mạch nước có được không. Hưu Môn = Nguồn nước. Thiên Bồng = Nước ngầm"},
        "Xem Cảnh Đẹp Thiên Nhiên": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem đi ngắm cảnh có thấy được cảnh đẹp không. Cảnh Môn = Cảnh đẹp. Thiên Anh = Sự mỹ lệ"},
        "Bảo Vệ Môi Trường": {"Dụng_Thần": ["Thiên Phụ", "Sinh Môn", "Thiên Tâm"], "Luận_Giải_Gợi_Ý": "Xem dự án môi trường có tác động tốt không. Thiên Phụ = Cây xanh/Môi trường. Sinh Môn = Sự sống mới"},
        "Dự Báo Lũ Lụt": {"Dụng_Thần": ["Thiên Bồng", "Hưu Môn", "Huyền Vũ"], "Luận_Giải_Gợi_Ý": "Xem nước lũ có tràn về gây hại không. Thiên Bồng = Nguồn nước lớn. Huyền Vũ = Sự tràn lan"},
        "Sự Việc Đột Xuất": {"Dụng_Thần": ["Thương Môn", "Can Giờ", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem sự việc bất ngờ xảy ra là cát hay hung. Thương Môn = Sự đột ngột. Can Giờ = Sự việc nảy sinh"},
        "Lựa Chọn Phương Án": {"Dụng_Thần": ["Khai Môn", "Thiên Tâm", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem phương án nào tối ưu nhất lúc này. Khai Môn = Giải pháp. Thiên Tâm = Sự sáng suốt"},
        "Xem Điềm Báo Giấc Mơ": {"Dụng_Thần": ["Đằng Xà", "Cảnh Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem giấc mơ đêm qua báo hiệu điều gì. Đằng Xà = Giấc mơ kịch tính. Cảnh Môn = Hình ảnh trong mơ"},
        "Kế Hoạch Dự Phòng": {"Dụng_Thần": ["Hỗ Quái (trong logic)", "Thiên Tâm", "Cửu Địa"], "Luận_Giải_Gợi_Ý": "Xem có cần kế hoạch B cho công việc không. Cửu Địa = Sự phòng thủ vững chắc. Thiên Tâm = Mưu lược"},
        "Tìm Quý Nhân Giúp Đỡ": {"Dụng_Thần": ["Trực Phù", "Thiên Ất", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem quý nhân ở phương nào, là ai. Trực Phù = Quý nhân lớn nhất. Thiên Ất = Người trợ giúp"},
        "Chống Lại Áp Lực": {"Dụng_Thần": ["Trực Phù", "Thiên Tâm", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem khả năng chịu đựng và vượt qua áp lực. Trực Phù = Khả năng chịu đựng. Can Ngày = Bản thân"},
        "Mở Rộng Tầm Nhìn": {"Dụng_Thần": ["Cửu Thiên", "Thiên Phụ", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem có nên thay đổi tư duy, hướng đi mới không. Cửu Thiên = Tầm nhìn xa. Thiên Phụ = Kiến thức mới"},
        "Gìn Giữ Hòa Khí": {"Dụng_Thần": ["Lục Hợp", "Hưu Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem cách duy trì các mối quan hệ êm đẹp. Lục Hợp = Sự gắn kết. Hưu Môn = Sự hòa nhã"},
        "Vay Vốn Ngân Hàng": {"Dụng_Thần": ["Mậu (Vốn)", "Khai Môn (Ngân hàng)", "Trực Phù"], "Luận_Giải_Gợi_Ý": "Xem vay ngân hàng có được giải ngân không. Mậu là tiền vay. Khai Môn là tổ chức tín dụng"},
        "Thanh Toán Nợ Nần": {"Dụng_Thần": ["Can Ngày (Mình)", "Can Giờ (Chủ nợ)", "Mậu"], "Luận_Giải_Gợi_Ý": "Xem chủ nợ có đòi gắt không, trả được không. Mậu là số tiền nợ cần trả"},
        "Tranh Chấp Bản Quyền": {"Dụng_Thần": ["Thiên Phụ", "Cảnh Môn", "Kinh Môn"], "Luận_Giải_Gợi_Ý": "Xem kiện tụng về bản quyền, chất xám. Thiên Phụ = Trí tuệ. Cảnh Môn = Tác phẩm. Kinh Môn = Kiện tụng"},
        "Bảo Mật Thông Tin": {"Dụng_Thần": ["Huyền Vũ", "Thiên Bồng", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Xem dữ liệu có bị rò rỉ hoặc hacker tấn công không. Huyền Vũ = Hacker/Kẻ trộm tin. Cảnh Môn = Thông tin bảo mật"},
        "Đầu Tư Tiền Điện Tử": {"Dụng_Thần": ["Thiên Bồng", "Đinh", "Sinh Môn"], "Luận_Giải_Gợi_Ý": "Xem đầu tư Coin, tiền ảo có rủi ro không. Thiên Bồng = Sự mạo hiểm cao. Đinh = Công nghệ số"},
        "Đầu Tư Vàng": {"Dụng_Thần": ["Mậu", "Sinh Môn", "Cung 6/7"], "Luận_Giải_Gợi_Ý": "Xem mua vàng tích trữ lúc này có tốt không. Cung 6 (Càn)/7 (Đoài) thuộc Kim tượng cho Vàng"},
        "Giải Thể Công Ty": {"Dụng_Thần": ["Tử Môn", "Khai Môn", "Can Ngày"], "Luận_Giải_Gợi_Ý": "Xem đóng cửa doanh nghiệp có êm xuôi không. Tử Môn = Kết thúc. Khai Môn = Hình thức pháp lý công ty"},
        "Tìm Người Đi Lạc": {"Dụng_Thần": ["Lục Thân (theo vai vế)", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem người thân đi lạc đang ở hướng nào, có về không. Can Giờ tượng cho người đi lạc nói chung"},
        "Thang Máy Nhà Ở": {"Dụng_Thần": ["Khai Môn", "Cảnh Môn", "Canh"], "Luận_Giải_Gợi_Ý": "Xem lắp đặt thang máy có an toàn, vận hành tốt không. Khai Môn = Máy móc thang máy. Canh = Kim loại/Cáp"},
        "Tổ Chức Tiệc Cưới": {"Dụng_Thần": ["Lục Hợp", "Cảnh Môn", "Ất/Canh"], "Luận_Giải_Gợi_Ý": "Xem đám cưới có diễn ra suôn sẻ, vui vẻ không. Lục Hợp = Hôn lễ. Cảnh Môn = Sự náo nhiệt. Ất/Canh = Vợ chồng"},
        "Mua Sắm Nội Thất": {"Dụng_Thần": ["Sinh Môn", "Cảnh Môn", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Xem mua đồ nội thất có bền và hợp phong thủy không. Sinh Môn = Nhà. Cảnh Môn = Đồ nội thất trang trí"},
        "Dự Đoán Kết Quả Xổ Số": {"Dụng_Thần": ["Mậu", "Thiên Bồng", "Thê Tài"], "Luận_Giải_Gợi_Ý": "Xem có lộc về tiền bạc bất ngờ không. Mậu = Tiền mặt. Thiên Bồng = May rủi. Thê Tài = Tài lộc"},
        "Tìm Chỗ Đỗ Xe": {"Dụng_Thần": ["Khai Môn", "Cung 2/5/8"], "Luận_Giải_Gợi_Ý": "Xem đến nơi có dễ tìm chỗ đậu xe không. Khai Môn = Cửa mở. Cung Thổ = Bãi đất/Bãi đỗ"},
        "Kiểm Tra An Ninh": {"Dụng_Thần": ["Trực Phù", "Cảnh Môn", "Huyền Vũ"], "Luận_Giải_Gợi_Ý": "Xem hệ thống an ninh nhà xưởng có ổn không. Trực Phù = Bảo vệ. Cảnh Môn = Hệ thống Camera"},
        "Sửa Chữa Điện Nước": {"Dụng_Thần": ["Thiên Nhuế", "Khai Môn", "Ất"], "Luận_Giải_Gợi_Ý": "Xem gọi thợ sửa điện nước có nhanh và triệt để không. Thiên Nhuế = Chỗ hỏng. Khai Môn = Thợ sửa. Ất = Dây điện/Ống nước"},
        "Bệnh Mãn Tính": {"Dụng_Thần": ["Thiên Nhuế", "Cửu Địa", "can Ngày"], "Luận_Giải_Gợi_Ý": "Xem bệnh mãn tính có ổn định hoặc thuyên giảm không. Thiên Nhuế = Bệnh. Cửu Địa = Trì trệ, lâu dài"},
        "Ma quỷ": {"Dụng_Thần": ["Đằng Xà", "Huyền Vũ", "Tử Môn"], "Luận_Giải_Gợi_Ý": "Xem có bị quấy phá bởi năng lượng âm hoặc thực thể vô hình không. Đằng Xà = Quái dị. Huyền Vũ = Ám muội. Tử Môn = Âm khí"},
        "Thần thánh": {"Dụng_Thần": ["Trực Phù", "Cửu Thiên", "Thái Âm"], "Luận_Giải_Gợi_Ý": "Xem có được thần linh, gia tiên phù hộ hay không. Trực Phù = Thần tối cao. Cửu Thiên = Thần linh. Thái Âm = Quý nhân âm"},
        "Dự Đoán Tỉ Số Bóng Đá": {"Dụng_Thần": ["Cảnh Môn", "Thiên Anh", "Can Ngày", "Can Giờ"], "Luận_Giải_Gợi_Ý": "Cảnh Môn = Bàn thắng. Thiên Anh = Sự hào hứng/Kết quả nổi bật. Can Ngày = Đội chủ nhà. Can Giờ = Đội khách. Cung Khắc/Sinh giữa Cảnh Môn và Can để đoán tỉ số."},
        "Trận Đấu Thể Thao (Thắng/Thua)": {"Dụng_Thần": ["Can Ngày", "Can Giờ", "Trực Phù", "Cửu Thiên"], "Luận_Giải_Gợi_Ý": "Can Ngày = Đội nhà/Mình cổ vũ. Can Giờ = Đội khách/Đối thủ. Trực Phù = Trọng tài/Lực lượng điều hành. Cửu Thiên = Ưu thế tấn công."},
        "Dự Đoán Kết Quả Trận Đấu": {"Dụng_Thần": ["Can Ngày (Chủ)", "Can Giờ (Khách)", "Khai Môn", "Cảnh Môn"], "Luận_Giải_Gợi_Ý": "Khai Môn = Sự khởi đầu/Trận đấu chính thức. Cảnh Môn = Tỉ số/Danh tiếng đạt được. Xem sự tương tác giữa 2 cung Can Ngày/Giờ."}
    }
}
# ======================================================================
# PHẦN 2: LOGIC TÍNH TOÁN CƠ BẢN (CHÍNH XÁC THEO QMDG)
# ======================================================================

def tinh_dia_chi_gio(gio_hien_tai):
    """Tìm Địa Chi Giờ dựa trên giờ hiện tại."""
    # Tý (23h-1h) -> Hợi (21h-23h)
    index = int((gio_hien_tai + 1) / 2) % 12
    return CAN_CHI_Gio[index]

def an_bai_luc_nghi(cuc, is_duong_don):
    """
    An bài Lục Nghi (Địa Bàn) dựa vào Cục và Âm/Dương Độn.
    Thứ tự: Mậu, Kỷ, Canh, Tân, Nhâm, Quý, Đinh, Bính, Ất.
    Dương Độn: Thuận (1->9). Âm Độn: Nghịch (9->1).
    Args:
        cuc (int): Số cục (1-9).
        is_duong_don (bool): True = Dương Độn, False = Âm Độn.
    Returns:
        dict: {cung_so: 'Can'}
    """
    # Lục nghi tam kỳ thứ tự: Mậu Kỷ Canh Tân Nhâm Quý Đinh Bính Ất
    LUC_NGHI_ORDER = ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Đinh", "Bính", "Ất"]
    dia_ban = {}
    
    current_pos = cuc
    
    for nghi in LUC_NGHI_ORDER:
        dia_ban[current_pos] = nghi
        if is_duong_don:
            current_pos += 1
            if current_pos > 9: current_pos = 1
        else:
            current_pos -= 1
            if current_pos < 1: current_pos = 9
            
    return dia_ban

def tinh_ngu_hanh_sinh_khac(hanh1, hanh2):
    """Tính Ngũ Hành Sinh Khắc."""
    if hanh1 == 'N/A' or hanh2 == 'N/A': return "N/A"
    if hanh1 == hanh2: return "Bình Hòa"
    
    rules = {
        ("Kim", "Thủy"): "Sinh", ("Thủy", "Mộc"): "Sinh", ("Mộc", "Hỏa"): "Sinh",
        ("Hỏa", "Thổ"): "Sinh", ("Thổ", "Kim"): "Sinh",
        
        ("Kim", "Mộc"): "Khắc", ("Mộc", "Thổ"): "Khắc", ("Thổ", "Thủy"): "Khắc",
        ("Thủy", "Hỏa"): "Khắc", ("Hỏa", "Kim"): "Khắc"
    }
    
    result = rules.get((hanh1, hanh2))
    if result == "Sinh": return f"{hanh1} Sinh {hanh2} (Cát)"
    if result == "Khắc": return f"{hanh1} Khắc {hanh2} (Hung)"
    
    result_nguoc = rules.get((hanh2, hanh1))
    if result_nguoc == "Sinh": return f"{hanh1} Bị {hanh2} Sinh (Tiểu Cát)" 
    if result_nguoc == "Khắc": return f"{hanh1} Bị {hanh2} Khắc (Đại Hung)" 
    
    return "Bình Hòa"


def kiem_tra_cau_truc_tranh(can_thien_ban, dia_can):
    """Kiểm tra các cặp Can Thiên/Can Địa có nằm trong TRUCTU_TRANH không."""
    ket_qua = {}
    
    # Chuẩn bị Can Thiên Bàn đầy đủ (thêm Mậu vào cung 5 nếu chưa có)
    can_thien_ban_full = can_thien_ban.copy()
    if 5 not in can_thien_ban_full or can_thien_ban_full[5] == 'N/A':
        can_thien_ban_full[5] = "Mậu" 
        
    tranh_data_all = KY_MON_DATA["TRUCTU_TRANH"] 

    for cung_so in range(1, 10):
        can_thien = can_thien_ban_full.get(cung_so, 'N/A')
        can_dia = dia_can.get(cung_so, 'N/A')
        
        if can_thien and can_dia and can_thien not in ["Giáp", "N/A"] and can_dia not in ["Giáp", "N/A"]:
            # Key: Can Thiên + Can Địa (ví dụ: ẤtBính)
            key = can_thien.strip() + can_dia.strip()
            
            result = tranh_data_all.get(key, {})
            
            if result:
                ket_qua[cung_so] = result
            else:
                ket_qua[cung_so] = {"Tên_Cách_Cục": "Không có", "Cát_Hung": "Bình", "Luận_Giải": "Không có cách cục đặc biệt được lưu."}
                
        else:
            ket_qua[cung_so] = {"Tên_Cách_Cục": "Không có", "Cát_Hung": "Bình", "Luận_Giải": "Không có cách cục đặc biệt được lưu."}

    return ket_qua


def tinh_khong_vong(can_gio, dia_chi_gio):
    """Tính Khổng Vong dựa vào Can Giờ và Chi Giờ."""
    if not can_gio: return []
    CAN_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    CHI_LIST = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    try:
        idx_can = CAN_LIST.index(can_gio)
        idx_chi = CHI_LIST.index(dia_chi_gio)
        
        # Tìm Tuần Không (Khoảng cách từ Chi đến Can)
        diff = idx_chi - idx_can
        if diff < 0: diff += 12
        
        # Tuần Thủ tại: (Chi - Can) % 12? Không, Tuần Thủ là Giáp tại vị trí đó
        # Tuần Không là 2 chi tiếp theo sau khi kết thúc 10 can
        # Ví dụ: Giáp Tý (0,0) -> Tuần Không là Tuất Hợi (10, 11)
        # Công thức: Tìm chi của Quý. Chi sau Quý là Tuần Không.
        # Chi Quý = (idx_chi + (9 - idx_can)) % 12
        idx_chi_quy = (idx_chi + (9 - idx_can)) % 12
        
        kv1_idx = (idx_chi_quy + 1) % 12
        kv2_idx = (idx_chi_quy + 2) % 12
        
        kv1 = CHI_LIST[kv1_idx]
        kv2 = CHI_LIST[kv2_idx]
        
        # Ánh xạ Chi sang Cung
        CHI_CUNG_MAP = {
            "Tý": 1, "Sửu": 8, "Dần": 8, "Mão": 3, "Thìn": 4, "Tị": 4,
            "Ngọ": 9, "Mùi": 2, "Thân": 2, "Dậu": 7, "Tuất": 6, "Hợi": 6
        }
        
        return list(set([CHI_CUNG_MAP[kv1], CHI_CUNG_MAP[kv2]]))
        
    except ValueError:
        return []


def tinh_dich_ma(dia_chi_gio):
    """Tính Dịch Mã thực tế."""
    # Thân Tý Thìn -> Dần (Cung 8)
    # Dần Ngọ Tuất -> Thân (Cung 2)
    # Tị Dậu Sửu -> Hợi (Cung 6)
    # Hợi Mão Mùi -> Tị (Cung 4)
    if dia_chi_gio in ["Thân", "Tý", "Thìn"]: return 8
    if dia_chi_gio in ["Dần", "Ngọ", "Tuất"]: return 2
    if dia_chi_gio in ["Tị", "Dậu", "Sửu"]: return 6
    if dia_chi_gio in ["Hợi", "Mão", "Mùi"]: return 4
    return None


def lap_ban_qmdg(cuc, truc_phu_star, truc_su_door, can_gio, chi_gio, is_duong_don):
    """
    Lập bàn QMDG đầy đủ theo quy luật chuyển động.
    """
    # 1. Định nghĩa vị trí Cố Định (Gốc)
    # Cửu Tinh Gốc (Địa Bàn)
    SAO_GOC = {
        1: "Thiên Bồng", 2: "Thiên Nhuế", 3: "Thiên Xung", 4: "Thiên Phụ",
        5: "Thiên Cầm", 6: "Thiên Tâm", 7: "Thiên Trụ", 8: "Thiên Nhậm", 9: "Thiên Anh"
    }
    # Bát Môn Gốc
    MON_GOC = {
        1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 
        6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"
    }
    
    # 2. Lập Địa Bàn (Lục Nghi)
    dia_ban = an_bai_luc_nghi(cuc, is_duong_don)
    
    # 3. Tìm vị trí hiện tại của Trực Phù (Star) và Trực Sử (Door) trên Địa Bàn
    # Trực Phù và Trực Sử đã được xác định tên ở ngoài, giờ tìm vị trí gốc của chúng
    # Để biết chúng "mang" Can nào đi đâu.
    
    # Tìm cung gốc của Sao Trực Phù
    cung_goc_truc_phu = 0
    for c, s in SAO_GOC.items():
        if s in truc_phu_star: # Sử dụng 'in' để khớp "Thiên Nhuế/Cầm"
            cung_goc_truc_phu = c
            break
            
    # Tìm cung gốc của Môn Trực Sử
    cung_goc_truc_su = 0
    for c, m in MON_GOC.items():
        if m == truc_su_door:
            cung_goc_truc_su = c
            break
    if cung_goc_truc_su == 0 and truc_su_door == "Tử": cung_goc_truc_su = 2 # Fallback cho Tử
    
    # 4. Xác định Cung Đích của Trực Phù (Thiên Bàn)
    # Trực Phù bay đến cung có Can Giờ trên Địa Bàn.
    target_stem = can_gio
    if target_stem == "Giáp":
        # Tìm Tuần Thủ dựa trên Chi Giờ (Vì Can là Giáp)
        # Giáp Tý -> Mậu, Giáp Tuất -> Kỷ ...
        # Mapping Chi -> Tuần Thủ (chỉ đúng khi Can là Giáp)
        # Tý(0)->Mậu, Tuất(10)->Kỷ, Thân(8)->Canh, Ngọ(6)->Tân, Thìn(4)->Nhâm, Dần(2)->Quý
        map_giap = {"Tý": "Mậu", "Tuất": "Kỷ", "Thân": "Canh", "Ngọ": "Tân", "Thìn": "Nhâm", "Dần": "Quý"}
        target_stem = map_giap.get(chi_gio, "Mậu")
    
    cung_dich_truc_phu = 0
    for c, can in dia_ban.items():
        if can == target_stem:
            cung_dich_truc_phu = c
            break
            
    if cung_dich_truc_phu == 0:
        # Fallback nếu không tìm thấy
        cung_dich_truc_phu = cung_goc_truc_phu

    # 5. Xoay Thiên Bàn (Chuyển Sao và Can Thiên)
    # Tính độ lệch (Offset)
    # Logic xoay vòng: 1->8->3->4->9->2->7->6 (Vòng Cửu Cung Lạc Thư)
    QUEUE_CUNG = [1, 8, 3, 4, 9, 2, 7, 6]
    
    try:
        idx_src = QUEUE_CUNG.index(cung_goc_truc_phu)
        idx_dst = QUEUE_CUNG.index(cung_dich_truc_phu)
        offset_sao = idx_dst - idx_src
    except ValueError:
        # Cung 5 (Trung Cung)? Thiên Cầm (5) thường đi theo Thiên Nhuế (2)
        if cung_goc_truc_phu == 5:
            # Thiên Cầm ký ở cung 2
            try:
                idx_src = QUEUE_CUNG.index(2)
                idx_dst = QUEUE_CUNG.index(cung_dich_truc_phu)
                offset_sao = idx_dst - idx_src
            except: offset_sao = 0
        else:
            offset_sao = 0

    thien_ban = {}
    can_thien_ban = {}
    
    # Sao và Can gốc di chuyển cùng nhau
    for c_goc in SAO_GOC:
        sao = SAO_GOC[c_goc]
        can_goc = dia_ban.get(c_goc, "N/A") # Can Thiên lấy từ Địa Bàn gốc tại vị trí sao đứng
        
        # Cung 5 (Thiên Cầm) đi cùng Cung 2 (Thiên Nhuế)
        target_c_goc = c_goc
        if c_goc == 5: target_c_goc = 2
            
        try:
            current_idx = QUEUE_CUNG.index(target_c_goc)
            new_idx = (current_idx + offset_sao) % 8
            cung_moi = QUEUE_CUNG[new_idx]
            
            # Lưu Thiên Bàn
            if c_goc == 5: # Thiên Cầm
                 # Thiên Cầm đi cùng Thiên Nhuế (2)
                 pass
            else:
                thien_ban[cung_moi] = sao
                can_thien_ban[cung_moi] = can_goc
                
                # Nếu cung này là nơi Thiên Nhuế đến, gán thêm Thiên Cầm
                if sao == "Thiên Nhuế":
                    # Tìm can của Thiên Cầm (từ cung gốc 5)
                    can_cam = dia_ban.get(5, "Mậu")
                    # Gán Thiên Cầm vào cùng cung
                    # Trong hiển thị, ta có thể dùng dấu / hoặc newline, 
                    # nhưng cấu trúc hiện tại là 1 string.
                    thien_ban[cung_moi] = "Thiên Nhuế/Cầm"
                    # Can thiên cũng có thể kép hoặc lấy của Nhuế? 
                    # Thường Cầm và Nhuế dùng chung Can Thiên của cung đích.
                
        except ValueError: pass
        
    # Xử lý Thiên Cầm đặc biệt: Luôn đi kèm Thiên Nhuế
    # Tìm cung mới của Thiên Nhuế
    for c, s in thien_ban.items():
        if s == "Thiên Nhuế":
            # Gán thêm Thiên Cầm hoặc đánh dấu?
            # Để đơn giản, ta không lưu key riêng cho Cầm ở các cung khác 5,
            # Mà mặc định Cầm đi theo Nhuế trong hiển thị (App lo).
            # Ở đây ta trả về Cầm ở vị trí của Nhuế để tham khảo
            pass

    # 6. Xoay Nhân Bàn (Chuyển Môn)
    # Trực Sử (Lead Door) di chuyển theo số giờ (Chi Giờ)
    # Nguyên tắc: Từ Cung của Phù Đầu (Leader), đếm thuận/nghịch theo Dương/Âm Độn
    # cho đến Chi Giờ hiện tại.
    # Mỗi giờ (1 canh) đi 1 cung.
    # Thứ tự cung đi: 1, 2, 3, 4, 5, 6, 7, 8, 9 (Theo Lạc Thư số)
    # Nếu gặp 5 thì chuyển sang 2 (Khôn).
    
    # a. Tìm chênh lệch giờ (Chi Giờ - Chi Leader)
    # Leader Stem (Mậu/Kỷ...) ẩn Giáp. 
    # Ta biết cung của Leader (cung_tuan_thu -> cung_goc_truc_su)
    # Nhưng ta cần biết Chi của Leader.
    # Leader là Giáp Tý, Giáp Tuất...?
    # Trong hàm calculate_qmdg_params có tính luc_nghi_tuan_thu (Mậu..). 
    # Nhưng ở đây ta chỉ có can_gio, chi_gio.
    # Ta cần tính lại Tuần Thủ của giờ hiện tại để biết Chi khởi đầu.
    # Ví dụ: Giờ Bính Dần.
    # Dần (2) - Bính (2) = 0 -> Giáp Tý (0). Chi Leader = Tý.
    # Khoảng cách = Dần - Tý = 2.
    
    # Tính lại Chi Leader
    CAN_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    CHI_LIST = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    try:
        idx_can = CAN_LIST.index(can_gio)
        idx_chi = CHI_LIST.index(chi_gio)
        diff_val = (idx_chi - idx_can) % 12 # Chi - Can
        # Leader start at this diff. 
        # Ví dụ: Bính(2) Dần(2) -> Diff=0 (Tý). Leader là Giáp Tý.
        # Bính(2) Thân(8). 8-2=6 (Ngọ). Leader là Giáp Ngọ.
        idx_chi_leader = diff_val
        
        # Số bước di chuyển = Chi Giờ - Chi Leader
        steps = (idx_chi - idx_chi_leader) % 12
    except ValueError: 
        steps = 0
        
    # b. Di chuyển từ Cung Leader (cung_tuan_thu)
    # Thay vì từ Cung Gốc của Môn (2), ta phải đi từ vị trí thực tế của Leader (5).
    # Ví dụ: Leader Mậu tại 5. Môn là Tử (2). Ta bắt đầu đi từ 5.
    
    current_cung = cung_goc_truc_phu
    
    for _ in range(steps):
        if is_duong_don:
            current_cung += 1
            if current_cung > 9: current_cung = 1
        else:
            current_cung -= 1
            if current_cung < 1: current_cung = 9
            
    # Sau khi chạy hết steps, ta có cung đích
    if current_cung == 5: current_cung = 2
    cung_dich_truc_su = current_cung
    
    # Tính offset Môn (Xoay Nhân Bàn)
    # Môn ở Cung Đích phải là Trực Sử (Môn Gốc)
    try:
        idx_src_mon = QUEUE_CUNG.index(cung_goc_truc_su)
        idx_dst_mon = QUEUE_CUNG.index(cung_dich_truc_su)
        
        # Môn đi thuận hay nghịch?
        # QMDG đa số phái: Môn xoay thuận chiều kim đồng hồ trên vòng tròn cung.
        offset_mon = idx_dst_mon - idx_src_mon
    except ValueError: offset_mon = 0
    
    nhan_ban = {}
    for c_goc in MON_GOC:
        mon = MON_GOC[c_goc]
        if c_goc == 5: continue # Không có Môn ở 5
        
        try:
            current_idx = QUEUE_CUNG.index(c_goc)
            new_idx = (current_idx + offset_mon) % 8
            cung_moi = QUEUE_CUNG[new_idx]
            nhan_ban[cung_moi] = mon
        except: pass
        
    # 7. An Thần Bàn (Bát Thần)
    # Trực Phù (Thần) đi theo Trực Phù (Sao) -> Tức là về cung_dich_truc_phu
    THAN_ORDER = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]
    
    than_ban = {}
    try:
        start_idx_cung = QUEUE_CUNG.index(cung_dich_truc_phu)
        
        for i, than in enumerate(THAN_ORDER):
            if is_duong_don:
                # Dương Độn: Thần đi Thuận
                cung_idx = (start_idx_cung + i) % 8
            else:
                # Âm Độn: Thần đi Nghịch
                cung_idx = (start_idx_cung - i) % 8
                
            cung_than = QUEUE_CUNG[cung_idx]
            than_ban[cung_than] = than
            
    except ValueError: pass

    # Trả về kết quả
    return thien_ban, can_thien_ban, nhan_ban, than_ban, cung_dich_truc_phu


def lap_ban_qmdg_thủ_công(sao_cung_1, cua_cung_1, can_thien_cung_1, than_cung_1):
    """
    Lập bàn QMDG thủ công (giữ nguyên logic cũ).
    """
    SAO_LIST = list(KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["CUU_TINH"].keys())
    MON_LIST = list(BAT_MON_CO_DINH_DISPLAY.keys())
    THAN_LIST = list(KY_MON_DATA["DU_LIEU_DUNG_THAN_PHU_TRO"]["BAT_THAN"].keys())
    CAN_LIST_NON_GIAP = [c for c in KY_MON_DATA["CAN_CHI_LUAN_GIAI"].keys() if c != "Giáp"]
    
    CUNG_AN_BAI = [1, 2, 3, 4, 5, 6, 7, 8, 9] 
    
    try: sao_cung_1_index = SAO_LIST.index(sao_cung_1)
    except ValueError: sao_cung_1_index = 0
    
    try: can_cung_1_index = CAN_LIST_NON_GIAP.index(can_thien_cung_1)
    except ValueError: can_cung_1_index = 0
    
    try: cua_cung_1_index = MON_LIST.index(cua_cung_1)
    except ValueError: cua_cung_1_index = 0
        
    try: than_cung_1_index = THAN_LIST.index(than_cung_1)
    except ValueError: than_cung_1_index = 0
        
    thien_ban = {}; can_thien_ban = {}; nhan_ban = {}; than_ban = {}
    
    sao_counter = 0; can_counter = 0; mon_counter = 0; than_counter = 0
    
    for cung_so in CUNG_AN_BAI:
        if cung_so != 5:
            thien_ban[cung_so] = SAO_LIST[(sao_cung_1_index + sao_counter) % len(SAO_LIST)]
            can_thien_ban[cung_so] = CAN_LIST_NON_GIAP[(can_cung_1_index + can_counter) % len(CAN_LIST_NON_GIAP)]
            nhan_ban[cung_so] = MON_LIST[(cua_cung_1_index + mon_counter) % len(MON_LIST)]
            than_ban[cung_so] = THAN_LIST[(than_cung_1_index + than_counter) % len(THAN_LIST)]
            sao_counter += 1; can_counter += 1; mon_counter += 1; than_counter += 1
        else:
            thien_ban[5] = "Thiên Cầm"; can_thien_ban[5] = "Mậu"

    dia_can = an_bai_luc_nghi(1, True) # Mặc định
    truc_phu_cung_so = 1

    return thien_ban, can_thien_ban, nhan_ban, than_ban, truc_phu_cung_so, dia_can

# Tải dữ liệu tùy chỉnh khi khởi động
KY_MON_DATA_CUSTOM = load_custom_data()
if KY_MON_DATA_CUSTOM and "TRUCTU_TRANH" in KY_MON_DATA_CUSTOM:
    KY_MON_DATA["TRUCTU_TRANH"].update(KY_MON_DATA_CUSTOM["TRUCTU_TRANH"])

# NEW: Trộn dữ liệu từ Excel vào KY_MON_DATA
KY_MON_DATA = merge_excel_data(KY_MON_DATA)

# NEW: Trộn dữ liệu nâng cao (PDF Knowledge)
KY_MON_DATA["ADVANCED_KNOWLEDGE"] = load_advanced_knowledge()

TOPIC_INTERPRETATIONS = KY_MON_DATA.get("TOPIC_INTERPRETATIONS", {})

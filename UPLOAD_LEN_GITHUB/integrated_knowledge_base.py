# -*- coding: utf-8 -*-
"""
INTEGRATED GITHUB CLASSICAL DIVINATION KNOWLEDGE BASE (V115.0)
==============================================================
Hợp nhất toàn bộ dữ liệu suy đoán từ các kho mã nguồn mở & cổ tịch lớn nhất trên GitHub:
1. KỲ MÔN ĐỘN GIÁP (`kentang2017/kinqimen`, `ChesterRa/mingpan`,《Yên Ba Điếu Tẩu Ca》,《Ngự Định Kỳ Môn Bảo Giám》, `qmdg_knowledge_complete.py`)
2. MAI HOA DỊCH SỐ (`handsomejustin/meihua-yi`, `westernwaterfall/yi-basic`,《Mai Hoa Dịch Số Toàn Thư — 18 Chiêm Pháp & Tam Yếu Thập Ứng》, `van_vat_tong_hop.py`)
3. LỤC HÀO KINH DỊCH (`muyen/decoding-iching`, `Brhiza/mingyu`,《Tăng San Bốc Dịch》,《Bốc Phệ Chính Tông》,《Hoàng Kim Sách Thiên Kim Phú》, `kinh_dich_64_que.py`, `thoan_tu_64.py`, `iching_integrated_data.py`)
4. THIẾT BẢN THẦN TOÁN & HOÀNG CỰC KINH THẾ (`Ryanlyly-ai/huangji-jingshi`, `Horace-Maxwell/Horosa`,《Thiết Bản Thần Toán 12.000 Điều Văn — Thái Huyền Số & Hoàng Cực Nguyên Hội Vận Thế》)
5. TỬ VI ĐẨU SỐ THIÊN KỶ 56.6GB (`Renhuai123/ziwei-doushu` — Nghê Hải Hạ《Thiên Kỷ》13 Chiều & Địa Lý 12 Cung, `tu_vi.py`)
"""

from __future__ import annotations
from typing import Dict, Any, List, Tuple

try:
    from qmdg_knowledge_complete import CUU_CUNG as _KM_CUU_CUNG
except Exception:
    _KM_CUU_CUNG = {}

try:
    from kinh_dich_64_que import KINH_DICH_64 as _KD64_FULL
except Exception:
    _KD64_FULL = {}

try:
    from thoan_tu_64 import QUE_THOAN_64 as _THOAN64_FULL
except Exception:
    _THOAN64_FULL = {}

try:
    from iching_integrated_data import ICHING_HEXAGRAMS as _IC64_PRO
except Exception:
    _IC64_PRO = {}

try:
    from van_vat_tong_hop import TRUONG_SINH_TRANG_THAI as _TS_12_STATE
except Exception:
    _TS_12_STATE = {}

try:
    from tu_vi import THIEN_KY_DIA_CHI_DIA_LY as _TV_DIA_LY_12
except Exception:
    _TV_DIA_LY_12 = {}


# ══════════════════════════════════════════════════════════════════════════════
# KHO 1: THIẾT BẢN THẦN TOÁN & HOÀNG CỰC KINH THẾ (GitHub: Ryanlyly-ai/huangji-jingshi & Horosa)
# Phép tính Thái Huyền Số + Tiên/Hậu Thiên Quái Số + Khấu Đinh Điều Văn (1001 -> 12960)
# ══════════════════════════════════════════════════════════════════════════════

THAI_HUYEN_CAN_SO = {
    "Giáp": 9, "Kỷ": 9,
    "Ất": 8, "Canh": 8,
    "Bính": 7, "Tân": 7,
    "Đinh": 6, "Nhâm": 6,
    "Mậu": 5, "Quý": 5,
}

THAI_HUYEN_CHI_SO = {
    "Tý": 9, "Ngọ": 9,
    "Sửu": 8, "Mùi": 8,
    "Dần": 7, "Thân": 7,
    "Mão": 6, "Dậu": 6,
    "Thìn": 5, "Tuất": 5,
    "Tỵ": 4, "Hợi": 4,
}

TIEN_THIEN_QUAI_SO = {
    "Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4,
    "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8,
}

HAU_THIEN_QUAI_SO = {
    "Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4,
    "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9,
}

# Bảng Khấu Đinh Điều Văn Thiết Bản Thần Toán theo 8 Cung Quẻ & Hào Động (1-6)
THIET_BAN_DIEU_VAN_CORE = {
    ("Càn", 1): ("Tiềm long vật dụng, căn cơ ẩn tàng nơi đất tĩnh, hậu vận đắc thời vươn cao", "Số định 1, 6, 9"),
    ("Càn", 2): ("Hiện long tại điền, quý nhân xuất lộ, lợi kiến đại nhân", "Số định 2, 6, 9"),
    ("Càn", 3): ("Quân tử chung nhật càn càn, tự lực lập thân, tiền khổ hậu cam", "Số định 3, 6"),
    ("Càn", 4): ("Hoặc dược tại uyên, chuyển mình qua bước ngoặt lớn sẽ đại phát", "Số định 4, 6, 9"),
    ("Càn", 5): ("Phi long tại thiên, công danh tài lộc hội tụ đỉnh cao", "Số định 5, 1, 9"),
    ("Càn", 6): ("Kháng long hữu hối, biết điểm dừng và giữ mình thì bảo toàn phúc lộc", "Số định 6, 1"),
    ("Khôn", 1): ("Lý sương kiên băng chí, gốc rễ từ miền đất tĩnh/vùng cao, tích tiểu thành đại", "Số định 1, 2, 8"),
    ("Khôn", 2): ("Trực phương đại, bất tập vô bất lợi — điền sản và gia đạo vững bền", "Số định 2, 8"),
    ("Khôn", 3): ("Hàm chương khả trinh, ẩn tài chờ thời, làm việc lớn có hậu quả tốt", "Số định 3, 2, 8"),
    ("Khôn", 4): ("Quát nang vô cữu vô dự, kín đáo giữ của, tránh phô trương", "Số định 4, 2, 8"),
    ("Khôn", 5): ("Hoàng thường nguyên cát, đức dày tải vật, trung vận phú quý", "Số định 5, 2, 8"),
    ("Khôn", 6): ("Long chiến vu dã, vượt qua cạnh tranh gay gắt để xác lập vị thế", "Số định 6, 2, 8"),
    ("Chấn", 1): ("Chấn lai hách hách, hậu tiếu ngôn ách ách — khởi đầu vất vả, sau hưởng phúc lành", "Số định 1, 3, 4"),
    ("Chấn", 2): ("Chấn lai lệ, ức táng bối — tài vật tạm hao nhưng giữ được gốc, qua 7 ngày/tháng tự hoàn", "Số định 2, 3, 4"),
    ("Chấn", 3): ("Chấn tô tô, chấn hành vô眚 — bình tĩnh hành động sẽ vượt qua trở lực", "Số định 3, 4"),
    ("Chấn", 4): ("Chấn toại nê — sự việc đang bị kìm chân nơi bùn lầy, cần ngoại lực phá cục", "Số định 4, 3"),
    ("Chấn", 5): ("Chấn vãng lai lệ, ức vô táng — bôn ba ngược xuôi nhưng cơ nghiệp vẫn giữ vững", "Số định 5, 3, 4"),
    ("Chấn", 6): ("Chấn sách sách, thị矍矍 — chớ nóng vội lúc giao thời, lùi một bước sẽ an toàn", "Số định 6, 3, 4"),
    ("Tốn", 1): ("Tiến thoái, lợi vũ nhân chi trinh — quyết đoán dứt khoát sẽ nắm bắt được cơ hội", "Số định 1, 4, 5"),
    ("Tốn", 2): ("Tốn tại sàng hạ, dùng bậc quân sư/chuyên gia trợ giúp thì cát lợi", "Số định 2, 4, 5"),
    ("Tốn", 3): ("Tần tốn, lận — suy tính quá nhiều dễ lỡ nhịp, cần chốt phương án sớm", "Số định 3, 4, 5"),
    ("Tốn", 4): ("Hối vong, điền hoạch tam phẩm — cầu tài, đầu tư hoặc thi cử thu hoạch cả 3 phần", "Số định 4, 5"),
    ("Tốn", 5): ("Trinh cát hối vong, tiên canh tam nhật hậu canh tam nhật — đổi mới phương pháp sẽ thành tựu", "Số định 5, 4"),
    ("Tốn", 6): ("Tốn tại sàng hạ, táng kỳ tư phủ — đề phòng hao tài nhỏ do cả tin", "Số định 6, 4, 5"),
    ("Khảm", 1): ("Tập khảm, nhập vu khảm đạm — gốc rễ từ vùng khe suối/sơn khê, cần giữ chính đạo", "Số định 1, 6"),
    ("Khảm", 2): ("Khảm hữu hiểm, cầu tiểu đắc — việc lớn cần làm từng bước nhỏ, cầu tài nhỏ đắc lợi", "Số định 2, 6, 1"),
    ("Khảm", 3): ("Lai chi khảm khảm, chớ vội vàng tiến bừa khi điều kiện tài chính chưa đủ", "Số định 3, 6, 1"),
    ("Khảm", 4): ("Tôn tửu quỹ nhị, nạp ước tự牖 — chân thành giản dị kết nối đúng người sẽ thông", "Số định 4, 6, 1"),
    ("Khảm", 5): ("Khảm bất doanh, chỉ ký bình — nước dâng ngang bờ,险 nạn qua đi, bắt đầu hanh thông", "Số định 5, 6, 1"),
    ("Khảm", 6): ("Hệ dụng huy mặc, trí vu tùng c棘 — kiên nhẫn tháo gỡ từng nút thắt", "Số định 6, 1"),
    ("Ly", 1): ("Lý thác nhiên, kính chi vô cữu — bước đầu cẩn trọng lễ nghĩa thì không mắc lỗi", "Số định 1, 3, 9"),
    ("Ly", 2): ("Hoàng ly nguyên cát — đắc trung đạo, văn thư giấy tờ và danh tiếng đại cát", "Số định 2, 3, 9"),
    ("Ly", 3): ("Nhật昃 chi ly — giữ tâm bình hòa, tránh nóng nảy bốc đồng", "Số định 3, 9"),
    ("Ly", 4): ("Đột như kỳ lai như, phần như — biến động hoặc cơn sốt/nhiệt bùng phát nhanh rồi hạ", "Số định 4, 3, 9"),
    ("Ly", 5): ("Xuất thế đà nhược, thích nhược, cát — sau lo âu vất vả là quý nhân nâng đỡ", "Số định 5, 3, 9"),
    ("Ly", 6): ("Vương dụng xuất chinh, chiết thủ hoạch phỉ — dứt điểm triệt để gốc rễ vấn đề", "Số định 6, 3, 9"),
    ("Cấn", 1): ("Cấn kỳ chỉ, vô cữu — gốc rễ vững chãi nơi vùng núi/đất cao, giữ tĩnh tại bước đầu", "Số định 1, 7, 8"),
    ("Cấn", 2): ("Cấn kỳ phỉ, tâm vị khoái — muốn tiến nhưng hoàn cảnh còn giữ lại, chờ thời mở cục", "Số định 2, 7, 8"),
    ("Cấn", 3): ("Cấn kỳ hạn, liệt kỳ夤 — tránh cưỡng cầu cứng nhắc, cần linh hoạt điều hòa", "Số định 3, 7, 8"),
    ("Cấn", 4): ("Cấn kỳ thân, vô cữu — tự chủ bản thân, giữ vững thành quả hiện có", "Số định 4, 7, 8"),
    ("Cấn", 5): ("Cấn kỳ phụ, ngôn hữu tự — lời nói có trật tự, uy tín, đàm phán thành công", "Số định 5, 7, 8"),
    ("Cấn", 6): ("Đôn cấn cát — hậu vận dày phúc, điền sản và gia trạch vững như bàn thạch", "Số định 6, 7, 8"),
    ("Đoài", 1): ("Hòa đoài cát — khởi sự thuận hòa, giao tiếp đắc lộc", "Số định 1, 2, 7"),
    ("Đoài", 2): ("Phu đoài cát, hối vong — giữ chữ tín, tài lộc/vàng bạc cất giữ an toàn (ứng số 2)", "Số định 2, 7"),
    ("Đoài", 3): ("Lai đoài hung — tránh chạy theo lời đường mật hoặc đầu cơ mạo hiểm", "Số định 3, 2, 7"),
    ("Đoài", 4): ("Thương đoài vị ninh, giới tật hữu hỷ — cân nhắc kỹ lưỡng, bệnh tật mau khỏi có tin vui", "Số định 4, 2, 7"),
    ("Đoài", 5): ("Phu vu bóc, hữu lệ — tỉnh táo quản lý tài chính, không giao tiền cho người thiếu uy tín", "Số định 5, 2, 7"),
    ("Đoài", 6): ("Dẫn đoài — thu hút nhân tâm, hợp tác đôi bên cùng có lợi", "Số định 6, 2, 7"),
}


def compute_thiet_ban_hoang_cuc(
    can_y: str, chi_y: str,
    can_m: str, chi_m: str,
    can_n: str, chi_n: str,
    can_g: str, chi_g: str,
    up_quai: str, lo_quai: str, dong_hao: int
) -> Dict[str, Any]:
    """
    Tính toán Điều Văn Thiết Bản Thần Toán & Hoàng Cực Kinh Thế (GitHub: Ryanlyly-ai/huangji-jingshi & Horosa).
    """
    y_num = THAI_HUYEN_CAN_SO.get(can_y, 7) * 10 + THAI_HUYEN_CHI_SO.get(chi_y, 9)
    m_num = THAI_HUYEN_CAN_SO.get(can_m, 5) * 10 + THAI_HUYEN_CHI_SO.get(chi_m, 5)
    d_num = THAI_HUYEN_CAN_SO.get(can_n, 6) * 10 + THAI_HUYEN_CHI_SO.get(chi_n, 4)
    h_num = THAI_HUYEN_CAN_SO.get(can_g, 7) * 10 + THAI_HUYEN_CHI_SO.get(chi_g, 4)

    tt_up = TIEN_THIEN_QUAI_SO.get(up_quai, 8)
    tt_lo = TIEN_THIEN_QUAI_SO.get(lo_quai, 6)
    ht_up = HAU_THIEN_QUAI_SO.get(up_quai, 2)
    ht_lo = HAU_THIEN_QUAI_SO.get(lo_quai, 1)
    d_idx = max(1, min(6, int(dong_hao or 1)))

    # Công thức Khấu Đinh Điều Văn Hoàng Cực (1001 -> 12960)
    hoang_cuc_base = (y_num * 100 + m_num * 10 + d_num + h_num + tt_up * 64 + tt_lo * 8 + d_idx)
    dieu_van_so = 1001 + (hoang_cuc_base % 11960)

    dv_text, dv_num_hint = THIET_BAN_DIEU_VAN_CORE.get(
        (up_quai, d_idx),
        ("Khí số Hoàng Cực vận chuyển theo chính đạo, thuận thời tất thành", f"Số định {tt_up}, {ht_lo}, {d_idx}")
    )
    return {
        "dieu_van_so": dieu_van_so,
        "thai_huyen_tu_tru": {"nam": y_num, "thang": m_num, "ngay": d_num, "gio": h_num},
        "tien_thien_pair": (tt_up, tt_lo),
        "hau_thien_pair": (ht_up, ht_lo),
        "dieu_van_text": dv_text,
        "dieu_van_num_hint": dv_num_hint,
    }


# ══════════════════════════════════════════════════════════════════════════════
# KHO 2: LỤC HÀO KINH DỊCH — HOÀNG KIM SÁCH & TĂNG SAN BỐC DỊCH & 6 HÀO VỊ
# (GitHub: muyen/decoding-iching, ChesterRa/mingpan, Brhiza/mingyu)
# ══════════════════════════════════════════════════════════════════════════════

LUC_HAO_6_VI_TUONG_PHAP = {
    1: {
        "ten_hao": "Hào 1 (Hào Sơ — Gốc Rễ / Thuở Sơ Sinh / Nền Đất)",
        "dia_ly": "Nơi chôn nhau cắt rốn lúc mới chào đời, vùng quê/nông thôn/chân núi, nền đất, móng nhà, tầng trệt",
        "nhan_su": "Thuở ấu thơ/sơ sinh, người dân thường, con cái nhỏ, bước khởi đầu sự việc",
        "co_the": "Bàn chân, ngón chân, gót chân",
    },
    2: {
        "ten_hao": "Hào 2 (Nội Quái Trung Vị — Ngôi Nhà / Nội Thất / Gia Trạch)",
        "dia_ly": "Bên trong ngôi nhà đang ở, phòng khách/phòng ngủ, ngăn tủ tầm thấp/trung, quê hương nội tộc",
        "nhan_su": "Người vợ/chồng trong nhà, quản gia, cấp cơ sở vững chắc",
        "co_the": "Bắp chân, đầu gối, cẳng chân",
    },
    3: {
        "ten_hao": "Hào 3 (Nội Quái Thượng Vị — Cửa Nhà / Ranh Giới Nội Ngoại)",
        "dia_ly": "Cửa chính ngôi nhà, cổng ngõ, bậc thềm, vùng giáp ranh giữa quê và tỉnh",
        "nhan_su": "Chủ hộ, trưởng phòng, người đứng mũi chịu sào chuyển tiếp nội-ngoại",
        "co_the": "Bụng dưới, thắt lưng, hông, thận, gan",
    },
    4: {
        "ten_hao": "Hào 4 (Ngoại Quái Hạ Vị — Ngoài Ngõ / Xã Hội / Cấp Tỉnh)",
        "dia_ly": "Ngoài cửa, đường phố gần nhà, khu phố/thị xã, tầng lầu trên",
        "nhan_su": "Cố vấn, phó giám đốc, quan chức địa phương, người thân bên ngoài",
        "co_the": "Ngực, tim, sườn, lưng trên",
    },
    5: {
        "ten_hao": "Hào 5 (Hào Quân Vương / Chí Tôn — Trung Tâm Lớn / Đô Hội / Đường Xa)",
        "dia_ly": "Kinh đô, thành phố lớn, trục đường chính, trung tâm hành chính, tầng cao",
        "nhan_su": "Lãnh đạo cao nhất, cha/chồng, giám đốc, quyết định tối cao",
        "co_the": "Cổ họng, phổi, mặt, ngũ quan",
    },
    6: {
        "ten_hao": "Hào 6 (Hào Thượng — Tận Cùng / Viễn Phương / Tông Miếu / Quê Tổ)",
        "dia_ly": "Nơi rất xa, vùng biên viễn/núi cao hoặc nước ngoài, mái nhà, bàn thờ/tông miếu, quê tổ",
        "nhan_su": "Ông bà tổ tiên, người nghỉ hưu, bậc cao niên, kết cục cuối cùng",
        "co_the": "Đỉnh đầu, não bộ, tóc",
    },
}

TANG_SAN_BOC_DICH_GOLDEN_RULES = {
    "DOC_PHAT": "《Tăng San Bốc Dịch · Độc Phát Chương》: Lục hào có 1 hào phát động gọi là Độc Phát — thần cơ của cả quẻ tập trung tại hào này (nếu là Nguyên Thần động sinh Dụng Thần thì trăm việc đều thành; nếu là Kỵ Thần động khắc Dụng Thần thì hiện tại đang phát sinh biến cố/bệnh chứng trực tiếp tại đó).",
    "TUAN_KHONG_LOAI_TRU": "《Bốc Phệ Chính Tông · Tuần Không Luận》: Hào lâm Tuần Không như cây không rễ, phòng không người; trong câu hỏi chọn lựa A hay B, phương án nào ứng với hào/hành bị Tuần Không Vô Khí thì bị bác bỏ để khẳng định phương án thực hữu còn lại.",
    "PHUC_TANG_NGUON_TIEN": "《Hoàng Kim Sách · Cầu Tài Điền Trạch》: Hào Thê Tài là gốc của nguồn tiền, Phụ Mẫu là gốc của nhà đất giấy tờ; khi Thê Tài Phục Tàng dưới hào khác và chưa được Nhật/Nguyệt xung phi lộ diện, nghĩa là tiền vốn thực tế chưa có sẵn trong tay, đại sự mua nhà đất phải chờ đến vận Thê Tài xuất lộ và Phụ Mẫu xuất Không.",
    "Y_DICH_PHAN_DINH": "《Tăng San Bốc Dịch · Tật Bệnh Chương》: Hào Kỵ Thần/Quan Quỷ khắc Dụng Thần phản ánh triệu chứng bệnh đang phát tác (như Hỏa khắc Kim là đang sốt cao/viêm hô hấp); còn Dụng Thần đắc Nguyệt lệnh hoặc có Nguyên Thần động là Tiên lượng cứu ứng (có thuốc chữa và chính khí vững nên mau bình phục).",
}


# ══════════════════════════════════════════════════════════════════════════════
# KHO 3: MAI HOA DỊCH SỐ — 18 CHIÊM PHÁP & TAM YẾU THẬP ỨNG
# (GitHub: handsomejustin/meihua-yi, westernwaterfall/yi-basic)
# ══════════════════════════════════════════════════════════════════════════════

MAI_HOA_18_CHIEM_PHAP = {
    "GIA_TRACH_NOI_SINH": "《Mai Hoa Dịch Số · Gia Trạch & Địa Lý Chiêm》: Càn là Kinh đô/Đô thị lớn nhà cao tầng; Ly là Phố thị đèn hoa chợ búa; Cấn là Vùng núi/Đồi núi/Sơn địa; Khôn là Vùng quê/Đồng ruộng/Đất rừng rộng; Khảm là Khe suối/Sông nước; Chấn/Tốn là Rừng cây đại ngàn (Sơn Lâm); Đoài là Ao đầm/Thung lũng.",
    "CAU_TAI_DINH_LUONG": "《Mai Hoa Dịch Số · Cầu Tài & Vật Số Chiêm》: Quẻ Thể là Chủ (Nhà/Người), Quẻ Dụng là Vật/Tài. Định lượng vật thể trong nhà phải lấy Tiên Thiên Quái Số của chính Quái Vật Thể kết hợp Hậu Thiên Nội Quái và Hào Động; nếu Quẻ Biến là Khốn/Tổn/Tiểu Súc thì quy mô nhỏ, lấy số hội tụ nhỏ nhất.",
    "TAT_BENH_CHIEM": "《Mai Hoa Dịch Số · Tật Bệnh Chiêm》: Định vị Quái Chủ Thể theo người bệnh (Con gái = Đoài Kim, Con trai = Chấn/Cấn, Cha = Càn, Mẹ = Khôn). Nếu gặp Ly Hỏa khắc Đoài Kim là triệu chứng đang sốt cao, viêm họng/phổi; có Thổ quái (Khôn/Cấn) đứng giữa là thuốc hạ sốt tiết Hỏa sinh Kim.",
    "THAT_VAT_TIM_DO": "《Mai Hoa Dịch Số · Thất Vật Chiêm》: Nội Quái (Hào 1-3) là mất ở trong nhà; Ngoại Quái (Hào 4-6) là ở ngoài sân/ngoài đường. Cấn là trên bàn/tủ/nơi gần núi đá; Khôn là nơi đất thấp/hộp kín; Đoài/Càn là gần đồ kim loại; Ly là gần đèn/bếp/cửa sổ; Khảm là nơi ẩm nước.",
}


# ══════════════════════════════════════════════════════════════════════════════
# KHO 4: KỲ MÔN ĐỘN GIÁP — YÊN BA ĐIẾU TẨU CA & NGỰ ĐỊNH KỲ MÔN BẢO GIÁM
# (GitHub: kentang2017/kinqimen, ChesterRa/mingpan)
# ══════════════════════════════════════════════════════════════════════════════

KY_MON_CACH_CUC_CANON = {
    "PHUC_NGAM": "《Yên Ba Điếu Tẩu Ca · Phục Ngâm Cục》: Tinh và Môn đều nằm nguyên tại bản cung — chủ sự việc giậm chân tại chỗ, trì trệ lặp lại, tiền bạc hay hàng hóa đang cất giữ yên một chỗ, tuyệt đối không thể bùng nổ ngay trong 1-2 ngày mà phải chờ xung mở.",
    "PHAN_NGAM": "《Yên Ba Điếu Tẩu Ca · Phản Ngâm Cục》: Tinh và Môn đối xung bản cung — chủ biến động nhanh, đảo chiều gấp, việc tưởng thành lại đổi, đồ mất dễ di chuyển nhưng bệnh cấp tính cũng hạ nhanh khi qua giờ xung.",
    "DO_MON_CAT_GIAU": "《Ngự Định Kỳ Môn Bảo Giám · Đỗ Môn》: Đỗ Môn thuộc Dương Mộc (bản cung Tốn 4), chủ đóng kín, cất giấu bí mật, kỹ thuật nội bộ. Hỏi tài sản/vàng bạc gặp Đỗ Môn là đang cất kỹ trong hộp/tủ kín đáo.",
    "TU_MON_SON_DIA": "《Ngự Định Kỳ Môn Bảo Giám · Tử Môn》: Tử Môn thuộc Âm Thổ (bản cung Khôn 2), khi đóng tại Cung 8 Cấn Đông Bắc chủ vùng núi đồi, đất đai nguyên sơ, yên tĩnh trầm mặc.",
    "THUONG_MON_XUNG_TINH": "《Ngự Định Kỳ Môn Bảo Giám · Thương Môn & Thiên Xung》: Thương Môn hội Sao Thiên Xung (Lôi Mộc) chủ chấn động mạnh, phát nhiệt cấp tính (sốt cao, đau nhức cấp) hoặc phương tiện di chuyển tốc độ cao.",
    "SINH_MON_DIEN_TRACH": "《Yên Ba Điếu Tẩu Ca · Sinh Môn》: Sinh Môn thuộc Dương Thổ (bản cung Cấn 8), là Đại Cát Môn chủ nhà cửa, đất đai, bất động sản, lợi nhuận kinh doanh và sinh khí hồi phục.",
}


# ══════════════════════════════════════════════════════════════════════════════
# API TRUY XUẤT HỢP NHẤT CHO DUAL AI AGENTS & APP
# ══════════════════════════════════════════════════════════════════════════════

def get_comprehensive_palace_info(palace_num: int) -> Dict[str, Any]:
    """Trả về thông tin chi tiết của Cung Kỳ Môn từ kho `qmdg_knowledge_complete.py`."""
    p_idx = int(palace_num) if str(palace_num).isdigit() else 5
    raw = _KM_CUU_CUNG.get(p_idx) or _KM_CUU_CUNG.get(5) or {}
    return {
        "name": raw.get("Ten", f"Cung {p_idx}"),
        "quai": raw.get("Quai", "Trung Cung"),
        "element": raw.get("Ngu_Hanh", "Thổ"),
        "huong": raw.get("Huong", "Trung tâm"),
        "mau_sac": raw.get("Mau_Sac", "Vàng đất"),
        "than_the": raw.get("Than_The", "Tỳ Vị"),
        "nguoi": raw.get("Nguoi", "Bản thân"),
        "tuong": raw.get("Tuong", "Trung tâm hội tụ"),
        "vat": raw.get("Vat", "Đồ gốm, đất đá"),
        "noi": raw.get("Noi", "Trong nhà"),
        "so": raw.get("So", p_idx),
    }


def synthesize_github_canon_evidence(
    ten_que_chu: str,
    ten_que_ho: str,
    ten_que_bien: str,
    up_chu: str,
    lo_chu: str,
    dong_hao: int,
    target_cung: int,
    sao_name: str,
    cua_name: str,
    than_name: str,
    can_y: str = "Bính", chi_y: str = "Ngọ",
    can_m: str = "Mậu", chi_m: str = "Tuất",
    can_n: str = "Đinh", chi_n: str = "Tỵ",
    can_g: str = "Tân", chi_g: str = "Hợi",
) -> Dict[str, Any]:
    """
    Tổng hợp toàn bộ dẫn chứng từ 5 Kho Dữ Liệu GitHub (Kỳ Môn + Mai Hoa + Lục Hào Kinh Dịch + Thiết Bản + Tử Vi Thiên Kỷ)
    cho quẻ hiện tại để cung cấp trực tiếp cho bộ suy luận `HexagramReasoningAI`.
    """
    d_idx = max(1, min(6, int(dong_hao or 1)))
    kd_chu = _KD64_FULL.get(ten_que_chu) or _THOAN64_FULL.get(ten_que_chu) or {}
    kd_bien = _KD64_FULL.get(ten_que_bien) or _THOAN64_FULL.get(ten_que_bien) or {}
    kd_ho = _KD64_FULL.get(ten_que_ho) or _THOAN64_FULL.get(ten_que_ho) or {}

    tb_info = compute_thiet_ban_hoang_cuc(
        can_y, chi_y, can_m, chi_m, can_n, chi_n, can_g, chi_g,
        up_chu, lo_chu, d_idx
    )
    hao_vi_info = LUC_HAO_6_VI_TUONG_PHAP.get(d_idx, LUC_HAO_6_VI_TUONG_PHAP[1])
    palace_info = get_comprehensive_palace_info(target_cung)

    km_canon_note = ""
    if "Đỗ" in cua_name:
        km_canon_note = KY_MON_CACH_CUC_CANON["DO_MON_CAT_GIAU"]
    elif "Tử" in cua_name and int(target_cung or 0) == 8:
        km_canon_note = KY_MON_CACH_CUC_CANON["TU_MON_SON_DIA"]
    elif "Thương" in cua_name:
        km_canon_note = KY_MON_CACH_CUC_CANON["THUONG_MON_XUNG_TINH"]
    elif "Sinh" in cua_name:
        km_canon_note = KY_MON_CACH_CUC_CANON["SINH_MON_DIEN_TRACH"]

    return {
        "kd_chu_thoan": kd_chu.get("thoan", ""),
        "kd_chu_dai_tuong": kd_chu.get("dai_tuong", ""),
        "kd_chu_y_nghia": kd_chu.get("y_nghia") or kd_chu.get("lk", ""),
        "kd_ho_thoan": kd_ho.get("thoan", ""),
        "kd_bien_thoan": kd_bien.get("thoan", ""),
        "kd_bien_y_nghia": kd_bien.get("y_nghia") or kd_bien.get("lk", ""),
        "thiet_ban": tb_info,
        "hao_dong_vi_tuong": hao_vi_info,
        "km_palace_detail": palace_info,
        "km_canon_note": km_canon_note,
    }


def format_info_for_display(info: Dict[str, Any]) -> str:
    return str(info)


def get_qua_info(qua_name: str) -> Dict[str, Any]:
    return _KD64_FULL.get(qua_name) or _THOAN64_FULL.get(qua_name) or {"name": qua_name, "desc": "Quẻ Kinh Dịch 64 Quẻ"}


def get_sao_info(sao_name: str) -> Dict[str, Any]:
    return {"name": sao_name, "desc": f"Cửu Tinh Kỳ Môn: {sao_name}"}


def get_mon_info(mon_name: str) -> Dict[str, Any]:
    return {"name": mon_name, "desc": f"Bát Môn Kỳ Môn: {mon_name}"}


def get_can_info(can_name: str) -> Dict[str, Any]:
    return {"name": can_name, "thai_huyen_so": THAI_HUYEN_CAN_SO.get(can_name, 5)}


# ══════════════════════════════════════════════════════════════════════════════
# V116.0 — MẢNH GHÉP 2: KHỚP NIÊN MỆNH (CAN CHI NĂM SINH) VÀO KỲ MÔN & LỤC HÀO
# (Xử lý 100% trên RAM tức thời — TUYỆT ĐỐI KHÔNG lưu câu hỏi hay dữ liệu cá nhân)
# ══════════════════════════════════════════════════════════════════════════════

_CAN_10_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
_CHI_12_LIST = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
_CAN_HANH_MAP = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa", "Mậu": "Thổ",
    "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim", "Nhâm": "Thủy", "Quý": "Thủy",
}
_CHI_HANH_MAP = {
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa",
    "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
}
_HOP_CHI_MAP = {
    "Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão",
    "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ",
}
_XUNG_CHI_MAP = {
    "Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần",
    "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị",
}
_CUNG_HUONG_MAP = {
    1: ("Khảm", "Chính Bắc", "Thủy"),
    2: ("Khôn", "Tây Nam", "Thổ"),
    3: ("Chấn", "Chính Đông", "Mộc"),
    4: ("Tốn", "Đông Nam", "Mộc"),
    5: ("Trung Cung", "Trung Tâm", "Thổ"),
    6: ("Càn", "Tây Bắc", "Kim"),
    7: ("Đoài", "Chính Tây", "Kim"),
    8: ("Cấn", "Đông Bắc", "Thổ"),
    9: ("Ly", "Chính Nam", "Hỏa"),
}


def extract_nien_menh_and_match_hexagram(
    question: str = "",
    chart_data: Dict[str, Any] = None,
    haos: List[Dict[str, Any]] = None,
    dong_list: List[int] = None,
    kv_list: List[str] = None,
) -> Dict[str, Any]:
    """
    V116.0 (Mảnh ghép 2): Tự động bóc tách Năm Sinh / Tuổi Can Chi của người được hỏi ngay trong câu hỏi
    (hoặc từ thông tin lá số tạm thời trên RAM) và đối chiếu trực tiếp vào:
    1) Bàn Kỳ Môn Độn Giáp (Tìm Cung chứa Thiên Can Niên Mệnh — chuẩn《Yên Ba Điếu Tẩu Ca》&《Ngự Định Kỳ Môn Bảo Giám》)
    2) Quẻ Lục Hào Kinh Dịch (Tìm Hào Bản Mệnh trùng/hợp/xung với Địa Chi Năm Sinh — chuẩn《Tăng San Bốc Dịch》)
    Hoàn toàn xử lý tức thời trên RAM, tuyệt đối không lưu lại câu hỏi hay thông tin bí mật của người dùng.
    """
    import re as _re_nm
    chart_data = chart_data or {}
    haos = haos or []
    dong_list = dong_list or []
    kv_list = kv_list or []

    q_text = str(question or "").strip()
    birth_year = None
    can_menh = ""
    chi_menh = ""

    # 1. Tìm năm sinh dạng 4 chữ số (1930 - 2030) trong câu hỏi (tránh nhầm với năm dự báo tương lai như "năm 2026", "năm 2027" nếu không có từ khóa sinh/tuổi)
    _yr_explicit = _re_nm.search(
        r"(?:sinh\s+năm|sn|tuổi|năm\s+sinh|sinh)\s*(19[3-9]\d|20[0-2]\d)\b",
        q_text,
         flags=_re_nm.IGNORECASE,
    )
    if _yr_explicit:
        birth_year = int(_yr_explicit.group(1))
    else:
        # Nếu câu hỏi có năm 1940..2023 đứng độc lập (không phải năm hiện tại/tương lai 2025-2030)
        _yr_any = _re_nm.search(r"\b(19[4-9]\d|20[0-1]\d|202[0-4])\b", q_text)
        if _yr_any:
            birth_year = int(_yr_any.group(1))
        elif chart_data.get("nam_sinh_user"):
            try:
                birth_year = int(chart_data.get("nam_sinh_user"))
            except Exception:
                birth_year = None

    if birth_year:
        can_menh = _CAN_10_LIST[(birth_year - 4) % 10]
        chi_menh = _CHI_12_LIST[(birth_year - 4) % 12]
    else:
        # Tìm cặp Can Chi tuổi trực tiếp trong câu hỏi (ví dụ: "tuổi Ất Sửu", "sinh năm Mậu Tuất", "Bính Tý")
        _q_low = q_text.lower()
        _chi_variants = {
            "tý": "Tý", "sửu": "Sửu", "dần": "Dần", "mão": "Mão", "thìn": "Thìn",
            "tỵ": "Tị", "tị": "Tị", "ngọ": "Ngọ", "mùi": "Mùi", "thân": "Thân", "dậu": "Dậu", "tuất": "Tuất", "hợi": "Hợi",
        }
        for _c10 in _CAN_10_LIST:
            for _ch_k, _ch_v in _chi_variants.items():
                if _re_nm.search(rf"(?<![a-zA-ZÀ-ỹ]){_c10.lower()}\s+{_ch_k}(?![a-zA-ZÀ-ỹ])", _q_low):
                    can_menh = _c10
                    chi_menh = _ch_v
                    break
            if can_menh:
                break

    if not can_menh or not chi_menh:
        return {"has_nien_menh": False, "summary_str": "", "prompt_line": ""}

    hanh_can_nm = _CAN_HANH_MAP.get(can_menh, "Thổ")
    hanh_chi_nm = _CHI_HANH_MAP.get(chi_menh, "Thổ")
    # Nếu Can Niên Mệnh là Giáp -> Độn ẩn dưới Mậu theo nguyên lý Độn Giáp
    can_km_lookup = "Mậu" if can_menh == "Giáp" else can_menh

    # 2. Định vị Cung Niên Mệnh trên Bàn Kỳ Môn Độn Giáp (Thiên Bàn & Địa Bàn)
    ctb = chart_data.get("can_thien_ban") or {}
    cdb = chart_data.get("can_dia_ban") or {}
    tb_stars = chart_data.get("thien_ban") or {}
    nb_doors = chart_data.get("nhan_ban") or {}
    sb_gods = chart_data.get("than_ban") or {}

    cung_nm = None
    for _c_idx in range(1, 10):
        _ct_val = str(ctb.get(_c_idx) or ctb.get(str(_c_idx)) or "").strip()
        if _ct_val == can_km_lookup:
            cung_nm = _c_idx
            break
    if cung_nm is None:
        for _c_idx in range(1, 10):
            _cd_val = str(cdb.get(_c_idx) or cdb.get(str(_c_idx)) or "").strip()
            if _cd_val == can_km_lookup:
                cung_nm = _c_idx
                break
    if cung_nm is None:
        # Dự phòng theo Hậu Thiên Địa Chi Năm Sinh
        _CHI_TO_CUNG = {
            "Tý": 1, "Sửu": 8, "Dần": 8, "Mão": 3, "Thìn": 4, "Tị": 4,
            "Ngọ": 9, "Mùi": 2, "Thân": 2, "Dậu": 7, "Tuất": 6, "Hợi": 6,
        }
        cung_nm = _CHI_TO_CUNG.get(chi_menh, 5)

    quai_nm, huong_nm, hanh_cung_nm = _CUNG_HUONG_MAP.get(cung_nm, ("Trung Cung", "Trung Tâm", "Thổ"))
    sao_nm = str(tb_stars.get(cung_nm) or tb_stars.get(str(cung_nm)) or "Thiên Tâm").strip()
    cua_nm = str(nb_doors.get(cung_nm) or nb_doors.get(str(cung_nm)) or "Khai Môn").strip()
    than_nm = str(sb_gods.get(cung_nm) or sb_gods.get(str(cung_nm)) or "Trực Phù").strip()

    # 3. Định vị Hào Bản Mệnh trên 6 Hào Lục Hào Kinh Dịch
    hao_bm_matches = []
    hao_hop_xung = []
    for _ix, _h in enumerate(haos, 1):
        if not isinstance(_h, dict):
            continue
        _ch = str(_h.get("chi") or _h.get("can_chi") or "").split()[-1]
        _lt = str(_h.get("luc_than") or "")
        _nh = str(_h.get("ngu_hanh") or _h.get("hanh") or _CHI_HANH_MAP.get(_ch, "Thổ"))
        _is_d = (_ix in dong_list) or bool(_h.get("dong") or _h.get("is_dong"))
        _is_kv = _ch in kv_list
        if _ch == chi_menh or (_ch == "Tị" and chi_menh == "Tỵ"):
            hao_bm_matches.append(
                f"Hào {_ix} {_lt} ({_ch}-{_nh}){' [ĐỘNG]' if _is_d else ''}{' [Tuần Không]' if _is_kv else ' [Hữu khí]'}"
            )
        elif _HOP_CHI_MAP.get(chi_menh) == _ch:
            hao_hop_xung.append(f"Lục Hợp với Hào {_ix} {_lt} ({_ch}-{_nh})")
        elif _XUNG_CHI_MAP.get(chi_menh) == _ch:
            hao_hop_xung.append(f"Lục Xung với Hào {_ix} {_lt} ({_ch}-{_nh})")

    bm_lh_str = (
        f"Trùng Hào Bản Mệnh tại {', '.join(hao_bm_matches)}"
        if hao_bm_matches else
        (f"Tương tác Bản Mệnh: {', '.join(hao_hop_xung[:2])}" if hao_hop_xung else f"Chi mệnh {chi_menh} ({hanh_chi_nm}) điều phối khí lực")
    )
    yr_lbl = f"{birth_year} ({can_menh} {chi_menh})" if birth_year else f"Tuổi {can_menh} {chi_menh}"
    summary_str = (
        f"👤 <b>Khớp Niên Mệnh Đích Danh ({yr_lbl} — Can {can_menh} [{hanh_can_nm}] / Chi {chi_menh} [{hanh_chi_nm}]):</b> "
        f"Trên bàn Kỳ Môn, Can Niên Mệnh <b>{can_menh}{' (ẩn dưới Mậu)' if can_menh == 'Giáp' else ''}</b> đóng tại <b>Cung {cung_nm} ({quai_nm} — {huong_nm}, Hành {hanh_cung_nm})</b> "
        f"hội <b>Sao {sao_nm} · Cửa {cua_nm} · Thần {than_nm}</b>; trên Lục Hào Kinh Dịch: <b>{bm_lh_str}</b>."
    )
    prompt_line = (
        f"  - Khớp Niên Mệnh ({yr_lbl}): Can mệnh {can_menh}落 Cung {cung_nm} ({quai_nm} - {huong_nm}) hội Sao {sao_nm}, Cửa {cua_nm}, Thần {than_nm}; Lục Hào: {bm_lh_str}.\n"
    )
    return {
        "has_nien_menh": True,
        "birth_year": birth_year,
        "can_menh": can_menh,
        "chi_menh": chi_menh,
        "hanh_can_nm": hanh_can_nm,
        "hanh_chi_nm": hanh_chi_nm,
        "cung_nm": cung_nm,
        "quai_nm": quai_nm,
        "huong_nm": huong_nm,
        "sao_nm": sao_nm,
        "cua_nm": cua_nm,
        "than_nm": than_nm,
        "bm_lh_str": bm_lh_str,
        "summary_str": summary_str,
        "prompt_line": prompt_line,
    }


# ══════════════════════════════════════════════════════════════════════════════
# V116.0 — MẢNH GHÉP 3: PHÁP QUYẾT HÓA GIẢI & VẬN TRÙ THỰC TẾ (DỤNG THẦN THÔNG QUAN)
# (Chuẩn《Trích Thiên Tủy》,《Tăng San Bốc Dịch》&《Kỳ Môn Pháp Khiếu》)
# ══════════════════════════════════════════════════════════════════════════════

_THONG_QUAN_MATRIX = {
    ("Hỏa", "Kim"): {
        "ten_xung": "Hỏa khắc Kim (Nhiệt độc/Áp lực thiêu đốt Kim khí — chủ sốt cao, viêm hô hấp, hao tài hoặc khẩu thiệt)",
        "hanh_thong_quan": "Thổ (kiêm Thủy điều hậu)",
        "nguyen_ly": "Dùng Hành Thổ làm cầu nối Thông Quan (Hỏa sinh Thổ ➔ Thổ sinh Kim: tiết bớt Hỏa sát để bồi bổ Kim khí) kết hợp Hành Thủy làm mát hạ nhiệt",
        "huong_hoa_giai": "Đông Bắc (Cung Cấn Thổ) hoặc Tây Nam (Cung Khôn Thổ) & Chính Tây/Tây Bắc (Hành Kim)",
        "mau_sac_vat_dung": "Vàng đất, Kem, Nâu nhạt, Trắng, Bạc (tránh màu Đỏ rực/Tím và tránh hướng Chính Nam đang vượng Hỏa)",
        "hanh_dong_thuc_te": "Nếu về sức khỏe: bù nước ấm/điện giải (Thủy), giữ ấm tỳ vị (Thổ), nằm phòng thoáng mát hướng Tây/Đông Bắc; nếu về công việc/tài chính: dùng sự điềm tĩnh, giấy tờ cam kết rõ ràng (Thổ/Phụ Mẫu) để hóa giải tranh chấp",
    },
    ("Kim", "Mộc"): {
        "ten_xung": "Kim khắc Mộc (Kim khí sắc bén chèn ép Mộc — chủ đau nhức gân cốt/đầu, áp lực cấp trên hoặc cản trở khởi sự)",
        "hanh_thong_quan": "Thủy",
        "nguyen_ly": "Dùng Hành Thủy làm cầu nối Thông Quan (Kim sinh Thủy ➔ Thủy sinh Mộc: hóa Sát thành Ấn, biến áp lực thành nguồn lực nuôi dưỡng)",
        "huong_hoa_giai": "Chính Bắc (Cung Khảm Thủy) & Chính Đông/Đông Nam (Hành Mộc)",
        "mau_sac_vat_dung": "Đen, Xanh nước biển, Xanh lục (tránh đồ kim loại sắc nhọn hoặc tranh cãi gay gắt)",
        "hanh_dong_thuc_te": "Lấy nhu thắng cương, dùng sự mềm mỏng linh hoạt và trí tuệ (Thủy) để thương lượng, tránh đối đầu trực diện",
    },
    ("Mộc", "Thổ"): {
        "ten_xung": "Mộc khắc Thổ (Mộc khí khắc phạt Điền Thổ — chủ rối loạn tiêu hóa/tỳ vị, biến động nhà đất hoặc hao tổn nền tảng)",
        "hanh_thong_quan": "Hỏa",
        "nguyen_ly": "Dùng Hành Hỏa làm cầu nối Thông Quan (Mộc sinh Hỏa ➔ Hỏa sinh Thổ: chuyển hóa sức ép thành năng lượng bồi đắp nền tảng)",
        "huong_hoa_giai": "Chính Nam (Cung Ly Hỏa) & Đông Bắc/Tây Nam (Hành Thổ)",
        "mau_sac_vat_dung": "Đỏ nhạt, Hồng, Cam, Vàng ấm (tăng cường ánh sáng và sự ấm áp trong không gian)",
        "hanh_dong_thuc_te": "Làm rõ thông tin minh bạch, công khai giấy tờ văn thư (Ly Hỏa/Cảnh Môn) và giữ ấm cơ thể/gia đạo",
    },
    ("Thổ", "Thủy"): {
        "ten_xung": "Thổ khắc Thủy (Thổ dày ngăn dòng Thủy — chủ tắc nghẽn dòng tiền, trì trệ công việc hoặc mệt mỏi thận/tiết niệu)",
        "hanh_thong_quan": "Kim",
        "nguyen_ly": "Dùng Hành Kim làm cầu nối Thông Quan (Thổ sinh Kim ➔ Kim sinh Thủy: tiết bớt sự trì trệ của Thổ để khai thông nguồn mạch Thủy)",
        "huong_hoa_giai": "Chính Tây (Cung Đoài Kim) hoặc Tây Bắc (Cung Càn Kim) & Chính Bắc (Hành Thủy)",
        "mau_sac_vat_dung": "Trắng, Bạc, Ánh kim, Xanh dương",
        "hanh_dong_thuc_te": "Cắt giảm các khâu trung gian rườm rà, quyết đoán dứt khoát (Kim) để giải phóng dòng vốn và tiến độ",
    },
    ("Thủy", "Hỏa"): {
        "ten_xung": "Thủy khắc Hỏa (Hàn Thủy dập Hỏa khí — chủ nhiễm lạnh, huyết áp/tim mạch hoặc kế hoạch bị dội gáo nước lạnh)",
        "hanh_thong_quan": "Mộc",
        "nguyen_ly": "Dùng Hành Mộc làm cầu nối Thông Quan (Thủy sinh Mộc ➔ Mộc sinh Hỏa: chuyển hóa lực cản thành nhiên liệu nuôi dưỡng Hỏa khí)",
        "huong_hoa_giai": "Chính Đông (Cung Chấn Mộc) hoặc Đông Nam (Cung Tốn Mộc) & Chính Nam (Hành Hỏa)",
        "mau_sac_vat_dung": "Xanh lá cây, Xanh ngọc, Đỏ cam ấm",
        "hanh_dong_thuc_te": "Chủ động học hỏi, mở rộng kết nối nhân duyên và từng bước nuôi dưỡng lại sinh khí (Mộc sinh Hỏa)",
    },
}

_SINH_ELEMENT_MAP = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
_DUOC_SINH_BY_MAP = {"Hỏa": "Mộc", "Thổ": "Hỏa", "Kim": "Thổ", "Thủy": "Kim", "Mộc": "Thủy"}
_KHAC_ELEMENT_MAP = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


def compute_thong_quan_remedy(
    hanh_the: str = "Thổ",
    hanh_dung: str = "Thủy",
    dt_nh: str = "Kim",
    dt_chi: str = "Dậu",
    is_phuc_ngam: bool = False,
    is_dt_kv: bool = False,
    chart_data: Dict[str, Any] = None,
    target_cung: int = 8,
    cua_name: str = "Sinh Môn",
    sao_name: str = "Thiên Tâm",
) -> Dict[str, Any]:
    """
    V116.0 (Mảnh ghép 3): Tính toán Pháp Quyết Hóa Giải & Vận Trù Thực Tế dựa trên:
    1) Ngũ Hành Thông Quan (khi có xung khắc giữa Thể - Dụng hoặc Kỵ Thần - Dụng Thần)
    2) Kỳ Môn Độn Giáp Trạch Cát (Tìm Cung Cát Môn Sinh/Khai/Hưu trên bàn Kỳ Môn hiện tại để mượn khí)
    3) Khung Giờ Lục Hợp / Nguyên Thần để kích hoạt ứng kỳ nhanh nhất.
    """
    chart_data = chart_data or {}
    # Kiểm tra cặp xung khắc cần Thông Quan
    conflict_pair = None
    if (hanh_dung, hanh_the) in _THONG_QUAN_MATRIX:
        conflict_pair = (hanh_dung, hanh_the)
    elif (hanh_the, hanh_dung) in _THONG_QUAN_MATRIX:
        conflict_pair = (hanh_the, hanh_dung)
    else:
        # Nếu Dụng Thần đang bị khắc bởi hành đối nghịch
        for _attacker, _victim in _KHAC_ELEMENT_MAP.items():
            if _victim == dt_nh and _attacker in (hanh_the, hanh_dung):
                conflict_pair = (_attacker, _victim)
                break

    if conflict_pair and conflict_pair in _THONG_QUAN_MATRIX:
        tq_info = _THONG_QUAN_MATRIX[conflict_pair]
        hanh_tq = tq_info["hanh_thong_quan"]
        nguyen_ly_tq = f"<b>{tq_info['ten_xung']}</b> ➔ {tq_info['nguyen_ly']}"
        huong_tq = tq_info["huong_hoa_giai"]
        mau_tq = tq_info["mau_sac_vat_dung"]
        hd_tq = tq_info["hanh_dong_thuc_te"]
    else:
        # Bồi bổ Nguyên Thần sinh trợ trực tiếp cho Dụng Thần (dt_nh) và Quẻ Thể (hanh_the)
        ng_than_hanh = _DUOC_SINH_BY_MAP.get(dt_nh, "Thổ")
        _HUONG_BY_HANH = {
            "Kim": "Chính Tây (Đoài) & Tây Bắc (Càn)",
            "Mộc": "Chính Đông (Chấn) & Đông Nam (Tốn)",
            "Thủy": "Chính Bắc (Khảm)",
            "Hỏa": "Chính Nam (Ly)",
            "Thổ": "Đông Bắc (Cấn) & Tây Nam (Khôn)",
        }
        _MAU_BY_HANH = {
            "Kim": "Trắng, Bạc, Ánh kim",
            "Mộc": "Xanh lá cây, Xanh ngọc",
            "Thủy": "Xanh nước biển, Đen",
            "Hỏa": "Đỏ, Cam, Hồng",
            "Thổ": "Vàng đất, Kem, Nâu",
        }
        hanh_tq = f"{ng_than_hanh} (Nguyên Thần sinh {dt_nh})"
        nguyen_ly_tq = f"Dùng <b>Nguyên Thần hành {ng_than_hanh}</b> để tương sinh trực tiếp cho Dụng Thần ({dt_nh}) và củng cố Quẻ Thể ({hanh_the})"
        huong_tq = _HUONG_BY_HANH.get(ng_than_hanh, "Đông Bắc & Chính Tây")
        mau_tq = _MAU_BY_HANH.get(ng_than_hanh, "Vàng đất, Trắng")
        hd_tq = "Tập trung bồi đắp nguồn lực cốt lõi (Nguyên Thần), hành sự đúng thời điểm Lục Hợp để đạt hiệu quả tối đa"

    # Tìm Cung Cát Môn (Sinh Môn, Khai Môn, Hưu Môn) trên bàn Kỳ Môn hiện tại
    nb_doors = chart_data.get("nhan_ban") or {}
    tb_stars = chart_data.get("thien_ban") or {}
    cat_cung_list = []
    for _c_i in range(1, 10):
        _d_str = str(nb_doors.get(_c_i) or nb_doors.get(str(_c_i)) or "").strip()
        _s_str = str(tb_stars.get(_c_i) or tb_stars.get(str(_c_i)) or "").strip()
        if any(cm in _d_str for cm in ("Sinh", "Khai", "Hưu")):
            _q_c, _h_c, _ = _CUNG_HUONG_MAP.get(_c_i, ("", "", ""))
            cat_cung_list.append(f"Cung {_c_i} ({_h_c} — Cửa {_d_str}, Sao {_s_str})")
    km_cat_phuong_str = " | ".join(cat_cung_list[:3]) if cat_cung_list else f"Cung {target_cung} (Cửa {cua_name}, Sao {sao_name})"

    # Khung giờ Lục Hợp & Xung Không/Xung Phục Ngâm
    hop_chi = _HOP_CHI_MAP.get(dt_chi, "Thìn")
    xung_chi = _XUNG_CHI_MAP.get(dt_chi, "Tuất")
    special_note = ""
    if is_phuc_ngam:
        special_note = f"⚡ <b>Phá giải Phục Ngâm:</b> Bàn Kỳ Môn đang Phục Ngâm (trì trệ lặp lại), cần đổi cách tiếp cận mới và chọn <b>Giờ/Ngày {xung_chi} (Lục Xung)</b> để xung động mở cục. "
    elif is_dt_kv:
        special_note = f"⚡ <b>Điền Thực / Xuất Không:</b> Hào Dụng Thần ({dt_chi}) đang Tuần Không, mọi việc chỉ thực sự ngã ngũ vào <b>Giờ/Ngày {dt_chi} (Thực Không)</b> hoặc <b>Giờ/Ngày {xung_chi} (Xung Không)</b>. "

    remedy_html = (
        f"🛡️ <b>Pháp Quyết Hóa Giải & Vận Trù Thực Tế (Ngũ Hành Thông Quan & Kỳ Môn Trạch Cát):</b><br>"
        f"&nbsp;&nbsp;• <b>Dụng Thần Thông Quan:</b> Bổ sung hành <b style='color:#fde047;'>{hanh_tq}</b> — {nguyen_ly_tq}.<br>"
        f"&nbsp;&nbsp;• <b>Phương vị & Sắc thái trợ vận:</b> Ưu tiên hướng <b>{huong_tq}</b> (Màu hợp: <b>{mau_tq}</b>) | "
        f"<b>Tam Cát Môn trên bàn Kỳ Môn hiện tại:</b> <span style='color:#4ade80;'>{km_cat_phuong_str}</span>.<br>"
        f"&nbsp;&nbsp;• <b>Ứng dụng thực tế & Thời cơ:</b> {special_note}{hd_tq} (Khung giờ/ngày hợp khí nhất: <b>Giờ/Ngày {hop_chi} [Lục Hợp]</b> hoặc <b>{dt_chi}</b>)."
    )
    return {
        "hanh_thong_quan": hanh_tq,
        "huong_hoa_giai": huong_tq,
        "mau_sac": mau_tq,
        "km_cat_phuong": km_cat_phuong_str,
        "hop_chi": hop_chi,
        "xung_chi": xung_chi,
        "remedy_html": remedy_html,
    }


# ══════════════════════════════════════════════════════════════════════════════
# V117.0 — BỘ GIẢI MÃ SÂU 24 YẾU TỐ TÁC ĐỘNG NGẦM & PHÂN TÍCH A→Z TỪNG BƯỚC
# (Lục Xung/Lục Hợp/Du Hồn/Quy Hồn · 12 Trường Sinh & Nhập Mộ · 6 Lục Thú ·
#  Nguyên/Kỵ/Cừu Thần · Ám Động & Nguyệt Phá · Hóa Tiến/Thoái/Hồi Đầu ·
#  Tam Hợp Cục · Phục/Phi Thần · Đảng Thể/Dụng Quẻ Hỗ · Môn Bức/Chế ·
#  Cung Can Ngày vs Can Giờ · 81 Cách Cục Lưu Bá Ôn · Nội/Ngoại Bàn)
# ══════════════════════════════════════════════════════════════════════════════

_LUC_XUNG_HEXAGRAMS = {
    "Càn Vi Thiên", "Khôn Vi Địa", "Khảm Vi Thủy", "Ly Vi Hỏa",
    "Chấn Vi Lôi", "Tốn Vi Phong", "Cấn Vi Sơn", "Đoài Vi Trạch",
    "Lôi Thiên Đại Tráng", "Thiên Lôi Vô Vọng",
}

_LUC_HOP_HEXAGRAMS = {
    "Địa Thiên Thái", "Thiên Địa Bĩ", "Trạch Lôi Tùy", "Sơn Phong Cổ",
    "Địa Lôi Phục", "Lôi Địa Dự", "Thủy Trạch Tiết", "Hỏa Sơn Lữ",
}

_DU_HON_HEXAGRAMS = {
    "Hỏa Địa Tấn", "Thủy Thiên Nhu", "Sơn Trạch Tổn", "Phong Lôi Ích",
    "Địa Hỏa Minh Di", "Thiên Thủy Tụng", "Trạch Sơn Hàm", "Lôi Phong Hằng",
}

_QUY_HON_HEXAGRAMS = {
    "Hỏa Thiên Đại Hữu", "Thủy Địa Tỷ", "Sơn Lôi Di", "Phong Trạch Trung Phu",
    "Thiên Hỏa Đồng Nhân", "Địa Thủy Sư", "Lôi Sơn Tiểu Quá", "Trạch Phong Đại Quá",
}

_TIEN_THAN_PAIRS = {
    ("Hợi", "Tý"), ("Dần", "Mão"), ("Tị", "Ngọ"), ("Thân", "Dậu"),
    ("Sửu", "Thìn"), ("Thìn", "Mùi"), ("Mùi", "Tuất"),
}

_THOAI_THAN_PAIRS = {
    ("Tý", "Hợi"), ("Mão", "Dần"), ("Ngọ", "Tị"), ("Dậu", "Thân"),
    ("Tuất", "Mùi"), ("Mùi", "Thìn"), ("Thìn", "Sửu"),
}

_TAM_HOP_CUCS = [
    ({"Thân", "Tý", "Thìn"}, "Thủy", "Tam Hợp Thân–Tý–Thìn Thủy Cục (Nguồn Thủy khí tuôn chảy mạnh mẽ)"),
    ({"Dần", "Ngọ", "Tuất"}, "Hỏa", "Tam Hợp Dần–Ngọ–Tuất Hỏa Cục (Hỏa khí bùng phát rực rỡ)"),
    ({"Hợi", "Mão", "Mùi"}, "Mộc", "Tam Hợp Hợi–Mão–Mùi Mộc Cục (Mộc khí sinh sôi vững chắc)"),
    ({"Tị", "Dậu", "Sửu"}, "Kim", "Tam Hợp Tị–Dậu–Sửu Kim Cục (Kim khí hội tụ sắc bén)"),
]

_MO_KHO_BY_HANH = {
    "Kim": "Sửu",
    "Mộc": "Mùi",
    "Thủy": "Thìn",
    "Hỏa": "Tuất",
    "Thổ": "Thìn",
}

_TRUONG_SINH_START = {
    "Mộc": "Hợi",
    "Hỏa": "Dần",
    "Thổ": "Dần",
    "Kim": "Tị",
    "Thủy": "Thân",
}

_TRUONG_SINH_12_NAMES = [
    "Trường Sinh (Khởi sinh tràn đầy sức sống)",
    "Mộc Dục (Non nớt/Nhạy cảm/Đào hoa)",
    "Quan Đới (Trưởng thành/Vào khuôn khổ)",
    "Lâm Quan (Vững vàng/Đắc lộc)",
    "Đế Vượng (Cực thịnh/Đỉnh cao năng lượng)",
    "Suy (Bắt đầu chững lại/Giảm nhiệt)",
    "Bệnh (Mệt mỏi/Có điểm yếu cần khắc phục)",
    "Tử (Khí lực trầm lắng/Khép kín)",
    "Mộ (Nhập kho cất giữ/Ẩn tàng/Thu liễm)",
    "Tuyệt (Tận cùng/Chờ chuyển hóa sang chu kỳ mới)",
    "Thai (Manh nha thai nghén ý định mới)",
    "Dưỡng (Nuôi dưỡng/Bồi đắp chờ thời)",
]

_LUC_THU_DEEP_MEANING = {
    "Thanh Long": "Cát thần chủ hỷ sự, tin vui, tài lộc chính đáng, quý nhân nâng đỡ, trang nhã",
    "Chu Tước": "Chủ văn thư, lời nói, tin tức, truyền thông; nếu khắc/động dễ sinh khẩu thiệt, tranh cãi hoặc nóng sốt/viêm nhiễm",
    "Câu Trần": "Chủ điền thổ, nhà cửa, đất đai, bất động sản, vùng núi/nông thôn; nếu kỵ thì chủ trì trệ, chậm chạp, vướng bận",
    "Đằng Xà": "Chủ sự lo âu, nhạy cảm, giấc mơ, dây dưa quấn quýt, biến ảo bất ngờ hoặc đường sá quanh co",
    "Bạch Hổ": "Chủ uy quyền, quyết đoán, kim loại, đường lớn; nếu lâm Quan Quỷ/Kỵ Thần chủ bệnh cấp tính, máu huyết, va chạm",
    "Huyền Vũ": "Chủ mưu lược ngầm, chuyện thầm kín, ẩm ướt/nước; nếu lâm Kỵ Thần/Tuần Không cần đề phòng thất thoát hoặc hiểu lầm",
}

_DOOR_HANH_MAP = {
    "Hưu": "Thủy", "Sinh": "Thổ", "Thương": "Mộc", "Đỗ": "Mộc",
    "Cảnh": "Hỏa", "Tử": "Thổ", "Kinh": "Kim", "Khai": "Kim",
}

_STAR_HANH_MAP = {
    "Bồng": "Thủy", "Nhuế": "Thổ", "Xung": "Mộc", "Phụ": "Mộc",
    "Cầm": "Thổ", "Tâm": "Kim", "Trụ": "Kim", "Nhậm": "Thổ", "Anh": "Hỏa",
}

_DIA_CHI_12 = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


def _calc_12_truong_sinh(hanh: str, target_chi: str) -> str:
    start_chi = _TRUONG_SINH_START.get(hanh, "Dần")
    if start_chi not in _DIA_CHI_12 or target_chi not in _DIA_CHI_12:
        return "Bình hòa"
    idx_start = _DIA_CHI_12.index(start_chi)
    idx_target = _DIA_CHI_12.index(target_chi)
    step = (idx_target - idx_start) % 12
    return _TRUONG_SINH_12_NAMES[step]


def _calc_season_vuong_suy(hanh_target: str, hanh_month: str) -> str:
    if not hanh_target or not hanh_month:
        return "Bình khí"
    if hanh_target == hanh_month:
        return "VƯỢNG (Đắc lệnh tháng — năng lượng cực mạnh)"
    if _SINH_ELEMENT_MAP.get(hanh_month) == hanh_target:
        return "TƯỚNG (Được Nguyệt Lệnh tương sinh — rất có lực)"
    if _SINH_ELEMENT_MAP.get(hanh_target) == hanh_month:
        return "HƯU (Sinh xuất cho tháng — hơi hao sức)"
    if _KHAC_ELEMENT_MAP.get(hanh_target) == hanh_month:
        return "TÙ (Khắc tháng nhưng tháng đang vượng — bị kìm hãm)"
    if _KHAC_ELEMENT_MAP.get(hanh_month) == hanh_target:
        return "TỬ/TUYỆT DƯỚI NGUYỆT LỆNH (Bị Nguyệt Lệnh chế khắc — cần Nhật Thần hoặc Nguyên Thần cứu ứng)"
    return "Bình khí"


def compute_deep_interacting_factors_a_to_z(
    univ_mat: Dict[str, Any],
    chart_data: Dict[str, Any] = None,
    luc_hao_data: Dict[str, Any] = None,
    mai_hoa_data: Dict[str, Any] = None,
    omni_data: Dict[str, Any] = None,
    dung_than: str = "Bản Thân",
    question: str = "",
) -> Dict[str, Any]:
    """
    V117.0: Phân tích toàn diện 24 Yếu Tố Tác Động Sâu & Ẩn Ngầm trên cả 4 hệ thống
    (Lục Hào Kinh Dịch · Mai Hoa Dịch Số · Kỳ Môn Độn Giáp · Thiết Bản & Tử Vi Thiên Kỷ)
    để cung cấp cho AI Cao Cấp Nhất (Gemini Pro) và hiển thị trực tiếp các bước phân tích A→Z.
    """
    import re
    chart_data = chart_data or {}
    luc_hao_data = luc_hao_data or {}
    mai_hoa_data = mai_hoa_data or {}
    omni_data = omni_data or {}
    univ_mat = univ_mat or {}

    can_y = str(chart_data.get("can_nam", "Bính"))
    chi_y = str(chart_data.get("chi_nam", "Ngọ"))
    can_m = str(chart_data.get("can_thang", "Mậu"))
    chi_m = str(chart_data.get("chi_thang", "Tuất"))
    can_n = str(chart_data.get("can_ngay", "Bính"))
    chi_n = str(chart_data.get("chi_ngay", "Thìn"))
    can_g = str(chart_data.get("can_gio", "Bính"))
    chi_g = str(chart_data.get("chi_gio", "Thìn"))

    nh_m = _CHI_HANH_MAP.get(chi_m, "Thổ")
    nh_n = _CHI_HANH_MAP.get(chi_n, "Thổ")
    kv_list = univ_mat.get("kv_list") or []
    dong_list = univ_mat.get("dong_list") or []

    full_chu = str(univ_mat.get("full_chu", "Quẻ Chủ"))
    full_ho = str(univ_mat.get("full_ho", "Quẻ Hỗ"))
    full_bien = str(univ_mat.get("full_bien", "Quẻ Biến"))
    up_chu = str(univ_mat.get("up_chu", "Càn"))
    lo_chu = str(univ_mat.get("lo_chu", "Khôn"))
    up_ho = str(univ_mat.get("up_ho", "Càn"))
    lo_ho = str(univ_mat.get("lo_ho", "Khôn"))
    up_bien = str(univ_mat.get("up_bien", "Càn"))
    lo_bien = str(univ_mat.get("lo_bien", "Khôn"))

    the_idx = int(univ_mat.get("the_idx", 3))
    the_chi = str(univ_mat.get("the_chi", "Thìn"))
    the_nh = str(univ_mat.get("the_nh", "Thổ"))
    ung_idx = int(univ_mat.get("ung_idx", 6))
    ung_chi = str(univ_mat.get("ung_chi", "Tuất"))
    ung_nh = str(univ_mat.get("ung_nh", "Thổ"))
    dt_idx = int(univ_mat.get("dt_idx", 3))
    dt_chi = str(univ_mat.get("dt_chi", "Thìn"))
    dt_nh = str(univ_mat.get("dt_nh", "Thổ"))

    lh_ban = (luc_hao_data.get("ban") or luc_hao_data.get("ban_que") or {}) if isinstance(luc_hao_data, dict) else {}
    lh_bien = (luc_hao_data.get("bien") or luc_hao_data.get("bien_que") or {}) if isinstance(luc_hao_data, dict) else {}
    haos = lh_ban.get("haos") or lh_ban.get("details") or luc_hao_data.get("haos") or []
    bien_haos = lh_bien.get("haos") or lh_bien.get("details") or []

    # -------------------------------------------------------------------------
    # I. BÓC TÁCH SÂU LỤC HÀO KINH DỊCH (10 TẦNG TÁC ĐỘNG NGẦM)
    # -------------------------------------------------------------------------
    # 1. Đặc tính Quẻ Chủ & Quẻ Biến (Lục Xung, Lục Hợp, Du Hồn, Quy Hồn)
    hex_special_traits = []
    if full_chu in _LUC_XUNG_HEXAGRAMS:
        hex_special_traits.append(f"Quẻ Chủ <b>{full_chu}</b> là <b>Quẻ Lục Xung</b> (6 hào nội ngoại lục xung: sự việc biến chuyển nhanh, nếu hỏi bệnh mới/việc xấu thì nhanh tan, hỏi hợp tác lâu dài thì dễ va chạm)")
    elif full_chu in _LUC_HOP_HEXAGRAMS:
        hex_special_traits.append(f"Quẻ Chủ <b>{full_chu}</b> là <b>Quẻ Lục Hợp</b> (6 hào nội ngoại lục hợp: gắn kết bền chặt, tình cảm/gia đạo hòa hợp, nhưng nếu hỏi bệnh cũ/vướng mắc thì dễ dây dưa)")
    if full_chu in _DU_HON_HEXAGRAMS:
        hex_special_traits.append(f"Quẻ Chủ <b>{full_chu}</b> thuộc thế <b>Du Hồn</b> (chủ sự dịch chuyển, đi xa, biến đổi không gian hoặc tâm tư còn phân vân)")
    elif full_chu in _QUY_HON_HEXAGRAMS:
        hex_special_traits.append(f"Quẻ Chủ <b>{full_chu}</b> thuộc thế <b>Quy Hồn</b> (chủ sự thu liễm về gốc, ở trong nhà, ổn định nội tại, giữ vững căn cơ)")
    if full_bien in _LUC_XUNG_HEXAGRAMS and full_bien != full_chu:
        hex_special_traits.append(f"Quẻ Biến <b>{full_bien}</b> hóa <b>Lục Xung</b> (giai đoạn cuối có sự xung kích giải tỏa hoặc phân tách nhanh)")
    elif full_bien in _LUC_HOP_HEXAGRAMS and full_bien != full_chu:
        hex_special_traits.append(f"Quẻ Biến <b>{full_bien}</b> hóa <b>Lục Hợp</b> (kết cục cuối cùng gắn kết, thành tựu bền vững)")
    hex_trait_str = "; ".join(hex_special_traits) if hex_special_traits else f"Quẻ Chủ <b>{full_chu}</b> chuyển biến sang <b>{full_bien}</b> theo trật tự ổn định"

    # 2. Vượng/Suy theo Nguyệt Lệnh, Nhật Thần & 12 Trường Sinh + Nhập Mộ của Dụng Thần & Hào Thế
    dt_season_state = _calc_season_vuong_suy(dt_nh, nh_m)
    the_season_state = _calc_season_vuong_suy(the_nh, nh_m)
    dt_ts_ngay = _calc_12_truong_sinh(dt_nh, chi_n)
    the_ts_ngay = _calc_12_truong_sinh(the_nh, chi_n)
    dt_mo_kho = _MO_KHO_BY_HANH.get(dt_nh, "Thìn")
    is_dt_nhap_mo = (chi_n == dt_mo_kho) or (chi_m == dt_mo_kho) or any(
        1 <= d <= len(bien_haos) and isinstance(bien_haos[d - 1], dict) and str(bien_haos[d - 1].get("chi", "")).split()[-1] == dt_mo_kho
        for d in dong_list if d == dt_idx
    )
    mo_kho_note = (
        f"⚠️ <b>Tác động Nhập Mộ (Mộ Khố {dt_mo_kho}):</b> Dụng Thần ({dt_chi}-{dt_nh}) đang gặp Mộ khố tại <b>{dt_mo_kho}</b> (chủ sự cất giấu kín đáo, thu liễm vào kho, hoặc năng lượng đang bị khóa tạm thời chờ ngày Xung Mộ <b>{_XUNG_CHI_MAP.get(dt_mo_kho, 'Tuất')}</b> mới bung ra)"
        if is_dt_nhap_mo else
        f"Dụng Thần ({dt_chi}-{dt_nh}) <b>không bị Nhập Mộ</b> (Mộ khố của {dt_nh} là {dt_mo_kho}), khí lực lưu thông tự nhiên"
    )

    # 3. Quét 6 Hào tìm: Lục Thú, Nguyên Thần, Kỵ Thần, Cừu Thần, Ám Động, Nguyệt Phá, Hóa Tiến/Thoái/Hồi Đầu
    ng_nh = _DUOC_SINH_BY_MAP.get(dt_nh, "Thổ")
    ky_nh = next((k for k, v in _KHAC_ELEMENT_MAP.items() if v == dt_nh), "Hỏa")
    cuu_nh = _SINH_ELEMENT_MAP.get(dt_nh, "Thủy")

    nguyen_than_list = []
    ky_than_list = []
    am_dong_list = []
    nguyet_pha_list = []
    dong_hoa_details = []
    dt_luc_thu = "Thanh Long"
    the_luc_thu = "Chu Tước"
    all_active_chis = {chi_m, chi_n}

    for ix, h in enumerate(haos, 1):
        if not isinstance(h, dict):
            continue
        lt = str(h.get("luc_than") or "")
        ch = str(h.get("chi") or h.get("can_chi") or "").split()[-1]
        nh = str(h.get("ngu_hanh") or h.get("hanh") or _CHI_HANH_MAP.get(ch, ""))
        lthu = str(h.get("luc_thu") or "")
        is_d = (ix in dong_list) or bool(h.get("dong") or h.get("is_dong"))
        is_kv = ch in kv_list
        if ch:
            all_active_chis.add(ch)
        if ix == dt_idx and lthu:
            dt_luc_thu = lthu
        if ix == the_idx and lthu:
            the_luc_thu = lthu

        # Nguyên Thần & Kỵ Thần
        if nh == ng_nh:
            nguyen_than_list.append(f"Hào {ix} {lt} ({ch}-{nh}){' [ĐỘNG]' if is_d else ''}{' [Tuần Không]' if is_kv else ''}")
        elif nh == ky_nh:
            ky_than_list.append(f"Hào {ix} {lt} ({ch}-{nh}){' [ĐỘNG]' if is_d else ''}{' [Tuần Không]' if is_kv else ''}")

        # Nguyệt Phá (Bị Chi Tháng lục xung)
        if _XUNG_CHI_MAP.get(chi_m) == ch:
            nguyet_pha_list.append(f"Hào {ix} {lt} ({ch}-{nh}) bị Nguyệt Lệnh ({chi_m}) xung ➔ <b>Nguyệt Phá</b>")

        # Ám Động (Hào tĩnh, có khí dưới Nguyệt Lệnh, bị Chi Ngày lục xung)
        if not is_d and _XUNG_CHI_MAP.get(chi_n) == ch:
            is_vuong_tuong = (nh == nh_m) or (_SINH_ELEMENT_MAP.get(nh_m) == nh) or (nh == nh_n)
            if is_vuong_tuong and not is_kv:
                am_dong_list.append(f"Hào {ix} {lt} ({ch}-{nh}) được Nhật Thần ({chi_n}) xung khi đang hữu khí ➔ <b>ÁM ĐỘNG (Tác động ngầm cực mạnh)</b>")
            else:
                am_dong_list.append(f"Hào {ix} {lt} ({ch}-{nh}) bị Nhật Thần ({chi_n}) xung ➔ <b>Nhật Phá / Xung Không</b>")

        # Chi tiết Hào Động & Hào Biến (Hồi đầu sinh/khắc, Hóa Tiến/Thoái, Hóa Không, Hóa Mộ)
        if is_d:
            b_ch, b_nh, b_lt = "", "", ""
            if 1 <= ix <= len(bien_haos) and isinstance(bien_haos[ix - 1], dict):
                bh = bien_haos[ix - 1]
                b_ch = str(bh.get("chi") or bh.get("can_chi") or "").split()[-1]
                b_nh = str(bh.get("ngu_hanh") or bh.get("hanh") or _CHI_HANH_MAP.get(b_ch, ""))
                b_lt = str(bh.get("luc_than") or "")
                if b_ch:
                    all_active_chis.add(b_ch)
            hoa_tags = []
            if (ch, b_ch) in _TIEN_THAN_PAIRS:
                hoa_tags.append("<b>HÓA TIẾN THẦN</b> (Khí lực tiến lên gấp bội)")
            elif (ch, b_ch) in _THOAI_THAN_PAIRS:
                hoa_tags.append("<b>HÓA THOÁI THẦN</b> (Hiện tại đang phát tác nhưng tương lai sẽ lui dần/giảm nhiệt)")
            if _SINH_ELEMENT_MAP.get(b_nh) == nh:
                hoa_tags.append("<b>HỒI ĐẦU SINH</b> (Hào biến quay lại sinh hào gốc — nguồn lực tự tiếp sức)")
            elif _KHAC_ELEMENT_MAP.get(b_nh) == nh:
                hoa_tags.append("<b>HỒI ĐẦU KHẮC</b> (Hào biến quay lại chế khắc hào gốc — tự triệt tiêu hoặc đổi hướng)")
            if b_ch in kv_list:
                hoa_tags.append("<b>HÓA KHÔNG VONG</b> (Chuyển hóa vào Tuần Không)")
            if b_ch == _MO_KHO_BY_HANH.get(nh, ""):
                hoa_tags.append(f"<b>HÓA NHẬP MỘ ({b_ch})</b>")
            if _HOP_CHI_MAP.get(ch) == b_ch:
                hoa_tags.append("<b>ĐỘNG HÓA LỤC HỢP</b> (Gắn kết chặt chẽ)")
            elif _XUNG_CHI_MAP.get(ch) == b_ch:
                hoa_tags.append("<b>PHẢN NGÂM HÀO (Động hóa Lục Xung)</b> (Biến động lật ngược/lặp đi lặp lại)")
            hv_info = LUC_HAO_6_VI_TUONG_PHAP.get(ix, {})
            dong_hoa_details.append(
                f"<b>Hào {ix} ({hv_info.get('ten_hao', f'Hào {ix}')}) — {lt} ({ch}-{nh}, Lục Thú: {lthu})</b> phát động biến thành "
                f"<b>{b_lt} ({b_ch}-{b_nh})</b>"
                + (f" ➔ {', '.join(hoa_tags)}" if hoa_tags else " (Biến hóa thuận chiều)")
                + f" [<i>Tượng hào vị: Địa lý={hv_info.get('dia_ly','')}; Nhân sự={hv_info.get('nhan_su','')}; Cơ thể={hv_info.get('co_the','')}</i>]"
            )

    # 4. Kiểm tra Tam Hợp Cục trên quẻ
    tam_hop_found = []
    for cuc_set, cuc_hanh, cuc_desc in _TAM_HOP_CUCS:
        if cuc_set.issubset(all_active_chis):
            rel_cuc_dt = (
                f"sinh trợ trực tiếp Dụng Thần ({dt_nh})" if _SINH_ELEMENT_MAP.get(cuc_hanh) == dt_nh
                else (f"đồng hành Tỷ Hòa với Dụng Thần ({dt_nh})" if cuc_hanh == dt_nh
                      else (f"khắc chế Dụng Thần ({dt_nh})" if _KHAC_ELEMENT_MAP.get(cuc_hanh) == dt_nh else f"tiết khí/tương tác với Dụng Thần ({dt_nh})"))
            )
            tam_hop_found.append(f"🌟 <b>Đắc {cuc_desc}</b> — Cục {cuc_hanh} {rel_cuc_dt}")

    # 5. Tương quan Thế – Ứng chuyên sâu
    if _SINH_ELEMENT_MAP.get(ung_nh) == the_nh:
        the_ung_rel = f"<b>Ứng sinh Thế ({ung_nh} sinh {the_nh})</b> — Khách thể/Môi trường/Đối phương đem lại lợi ích cho bản thân bạn (Đại Cát)"
    elif _SINH_ELEMENT_MAP.get(the_nh) == ung_nh:
        the_ung_rel = f"<b>Thế sinh Ứng ({the_nh} sinh {ung_nh})</b> — Bạn phải chủ động bỏ công sức, tâm huyết hoặc chi phí cho đối phương/sự việc"
    elif _KHAC_ELEMENT_MAP.get(the_nh) == ung_nh:
        the_ung_rel = f"<b>Thế khắc Ứng ({the_nh} khắc {ung_nh})</b> — Bạn nắm quyền chủ động, kiểm soát và làm chủ được hoàn cảnh"
    elif _KHAC_ELEMENT_MAP.get(ung_nh) == the_nh:
        the_ung_rel = f"<b>Ứng khắc Thế ({ung_nh} khắc {the_nh})</b> — Hoàn cảnh khách quan hoặc đối phương đang tạo áp lực/lực cản lên bạn"
    else:
        the_ung_rel = f"<b>Thế – Ứng Tỷ Hòa ({the_nh} đồng hành {ung_nh})</b> — Hai bên tương đồng, dễ tìm được tiếng nói chung"
    if _HOP_CHI_MAP.get(the_chi) == ung_chi:
        the_ung_rel += f" + <b>Thế Ứng Lục Hợp ({the_chi}–{ung_chi})</b> (Gắn kết hòa hợp)"
    elif _XUNG_CHI_MAP.get(the_chi) == ung_chi:
        the_ung_rel += f" + <b>Thế Ứng Lục Xung ({the_chi}–{ung_chi})</b> (Đang có khoảng cách hoặc xung đột quan điểm)"

    dt_lthu_desc = _LUC_THU_DEEP_MEANING.get(dt_luc_thu, "Chủ khí vận biến chuyển")
    the_lthu_desc = _LUC_THU_DEEP_MEANING.get(the_luc_thu, "Chủ tâm thái hiện tại")
    dt_vi_info = LUC_HAO_6_VI_TUONG_PHAP.get(dt_idx, {})

    # -------------------------------------------------------------------------
    # II. BÓC TÁCH SÂU MAI HOA DỊCH SỐ (ĐẢNG THỂ/DỤNG QUẺ HỖ & ĐẮC THỜI MÙA)
    # -------------------------------------------------------------------------
    hanh_the = str(univ_mat.get("hanh_the", "Thổ"))
    hanh_dung = str(univ_mat.get("hanh_dung", "Thủy"))
    hanh_ho_up = str(univ_mat.get("hanh_ho_up", "Mộc"))
    hanh_ho_lo = str(univ_mat.get("hanh_ho_lo", "Thổ"))
    hanh_bien_dung = str(univ_mat.get("hanh_bien_dung", "Kim"))
    the_quai = str(univ_mat.get("the_quai", up_chu))
    dung_quai = str(univ_mat.get("dung_quai", lo_chu))
    bien_dung_quai = str(univ_mat.get("bien_dung_quai", lo_bien))

    # Đếm Đảng Thể vs Đảng Dụng trên Quẻ Hỗ (up_ho, lo_ho)
    dang_the_parts = []
    dang_dung_parts = []
    for _h_lbl, _q_h, _nh_h in [("Thượng Hỗ", up_ho, hanh_ho_up), ("Hạ Hỗ", lo_ho, hanh_ho_lo)]:
        if _nh_h == hanh_the or _SINH_ELEMENT_MAP.get(_nh_h) == hanh_the:
            dang_the_parts.append(f"{_h_lbl} <b>{_q_h} ({_nh_h})</b> sinh/trợ Quẻ Thể ({hanh_the})")
        else:
            dang_dung_parts.append(f"{_h_lbl} <b>{_q_h} ({_nh_h})</b> khắc/hao Quẻ Thể ({hanh_the})")
    if len(dang_the_parts) == 2:
        dang_ho_verdict = f"<b>Đảng Thể Cực Vượng (Cả 2 quái của Quẻ Hỗ `{full_ho}` đều trợ lực cho Quẻ Thể):</b> {'; '.join(dang_the_parts)} ➔ Nội tình bên trong cực kỳ thuận lợi, có nội lực và quý nhân hậu thuẫn ngầm!"
    elif len(dang_the_parts) == 1:
        dang_ho_verdict = f"<b>Quẻ Hỗ `{full_ho}` Cân Bằng (1 trợ Thể – 1 hao/khắc Thể):</b> {dang_the_parts[0]}; nhưng {dang_dung_parts[0]} ➔ Quá trình trung gian có cả cơ hội lẫn thử thách đan xen."
    else:
        dang_ho_verdict = f"<b>Đảng Dụng Chiếm Ưu Ở Quẻ Hỗ `{full_ho}`:</b> {'; '.join(dang_dung_parts)} ➔ Diễn biến nội tình trung gian đòi hỏi phải nỗ lực vượt qua lực cản nội tại."

    mh_the_season = _calc_season_vuong_suy(hanh_the, nh_m)
    mh_dung_season = _calc_season_vuong_suy(hanh_dung, nh_m)

    # -------------------------------------------------------------------------
    # III. BÓC TÁCH SÂU KỲ MÔN ĐỘN GIÁP (CUNG CHỦ-KHÁCH, MÔN BỨC, 81 CÁCH CỤC)
    # -------------------------------------------------------------------------
    target_cung = int(univ_mat.get("target_cung", 8)) if str(univ_mat.get("target_cung", 8)).isdigit() else 8
    huong_cung = str(univ_mat.get("huong_cung", "Đông Bắc"))
    quai_cung = str(univ_mat.get("quai_cung", "Cấn"))
    sao_name = str(univ_mat.get("sao_name", "Thiên Tâm"))
    cua_name = str(univ_mat.get("cua_name", "Khai Môn"))
    than_name = str(univ_mat.get("than_name", "Trực Phù"))
    is_duong_don = bool(chart_data.get("is_duong_don", False))

    # 1. Nội Bàn vs Ngoại Bàn
    noi_ban_cungs = {1, 8, 3, 4} if is_duong_don else {9, 2, 7, 6}
    is_noi_ban = target_cung in noi_ban_cungs
    noi_ngoai_ban_str = (
        f"<b>Nội Bàn (Cung {target_cung} thuộc Nội Bàn của {'Dương Độn' if is_duong_don else 'Âm Độn'}):</b> Sự việc/đối tượng gắn với không gian <b>bên trong nhà, gần gũi, nội bộ gia đình/cơ quan và tốc độ ứng nghiệm nhanh</b>"
        if is_noi_ban else
        f"<b>Ngoại Bàn (Cung {target_cung} thuộc Ngoại Bàn của {'Dương Độn' if is_duong_don else 'Âm Độn'}):</b> Sự việc/đối tượng liên quan tới <b>không gian bên ngoài xã hội, khoảng cách xa hoặc cần thêm thời gian chuẩn bị</b>"
    )

    # 2. Quan hệ Môn – Cung (Môn Nghĩa, Môn Hòa, Môn Chế, Môn Bức)
    _, _, hanh_cung_dt = _CUNG_HUONG_MAP.get(target_cung, ("Cấn", "Đông Bắc", "Thổ"))
    hanh_cua_dt = next((v for k, v in _DOOR_HANH_MAP.items() if k in cua_name), "Kim")
    hanh_sao_dt = next((v for k, v in _STAR_HANH_MAP.items() if k in sao_name), "Kim")
    if _KHAC_ELEMENT_MAP.get(hanh_cua_dt) == hanh_cung_dt:
        mon_cung_state = f"⚠️ <b>MÔN BỨC (Cửa {cua_name} [{hanh_cua_dt}] khắc Cung {target_cung} [{hanh_cung_dt}]):</b> Cửa bức bách cung vị — làm giảm lực cát hoặc gây áp lực cưỡng ép, cần hành sự mềm mỏng"
    elif _KHAC_ELEMENT_MAP.get(hanh_cung_dt) == hanh_cua_dt:
        mon_cung_state = f"⚖️ <b>MÔN CHẾ (Cung {target_cung} [{hanh_cung_dt}] chế khắc Cửa {cua_name} [{hanh_cua_dt}]):</b> Cung vị kiểm soát được Cửa (nếu là Hung Môn thì cái xấu bị khống chế)"
    elif _SINH_ELEMENT_MAP.get(hanh_cung_dt) == hanh_cua_dt:
        mon_cung_state = f"✅ <b>MÔN NGHĨA (Cung {target_cung} [{hanh_cung_dt}] sinh Cửa {cua_name} [{hanh_cua_dt}]):</b> Hoàn cảnh địa lợi nuôi dưỡng nhân sự (Cát)"
    elif _SINH_ELEMENT_MAP.get(hanh_cua_dt) == hanh_cung_dt:
        mon_cung_state = f"✅ <b>MÔN HÒA (Cửa {cua_name} [{hanh_cua_dt}] sinh Cung {target_cung} [{hanh_cung_dt}]):</b> Nhân hòa tương hợp với địa lợi (Đại Cát)"
    else:
        mon_cung_state = f"✅ <b>Môn – Cung Tỷ Hòa ({hanh_cua_dt} đồng hành {hanh_cung_dt}):</b> Khí lực thông suốt"

    # 3. Tương quan Cung Can Ngày (Chủ thể) ↔ Cung Can Giờ (Sự việc) & Cách Cục Thiên+Địa Can
    ctb = chart_data.get("can_thien_ban") or {}
    cdb = chart_data.get("dia_can") or chart_data.get("dia_ban") or {}
    cung_can_ngay = target_cung
    cung_can_gio = target_cung
    for _ck, _cv in ctb.items():
        if str(_cv).strip() == can_n:
            cung_can_ngay = int(_ck) if str(_ck).isdigit() else target_cung
        if str(_cv).strip() == can_g:
            cung_can_gio = int(_ck) if str(_ck).isdigit() else target_cung
    _, huong_cn, hanh_cung_cn = _CUNG_HUONG_MAP.get(cung_can_ngay, ("Khôn", "Tây Nam", "Thổ"))
    _, huong_cg, hanh_cung_cg = _CUNG_HUONG_MAP.get(cung_can_gio, ("Cấn", "Đông Bắc", "Thổ"))
    if cung_can_ngay == cung_can_gio:
        chu_khach_km_str = f"<b>Can Ngày ({can_n}) và Can Giờ ({can_g}) ĐỒNG CUNG tại Cung {cung_can_ngay} ({huong_cn}):</b> Bản thân người hỏi và sự việc đang gắn chặt làm một, trực tiếp đối diện và quyết định ngay tại chỗ"
    elif _SINH_ELEMENT_MAP.get(hanh_cung_cg) == hanh_cung_cn:
        chu_khach_km_str = f"<b>Cung Sự Việc (Can Giờ {can_g} tại Cung {cung_can_gio} [{hanh_cung_cg}]) tương sinh Cung Bản Thân (Can Ngày {can_n} tại Cung {cung_can_ngay} [{hanh_cung_cn}]):</b> Sự việc mang lại lợi ích thuận lợi cho bạn"
    elif _KHAC_ELEMENT_MAP.get(hanh_cung_cg) == hanh_cung_cn:
        chu_khach_km_str = f"<b>Cung Sự Việc (Can Giờ {can_g} tại Cung {cung_can_gio} [{hanh_cung_cg}]) khắc Cung Bản Thân (Can Ngày {can_n} tại Cung {cung_can_ngay} [{hanh_cung_cn}]):</b> Sự việc đang tạo áp lực trực tiếp lên bạn, cần dùng Thông Quan hóa giải"
    elif _KHAC_ELEMENT_MAP.get(hanh_cung_cn) == hanh_cung_cg:
        chu_khach_km_str = f"<b>Cung Bản Thân (Can Ngày {can_n} tại Cung {cung_can_ngay} [{hanh_cung_cn}]) khắc Cung Sự Việc (Can Giờ {can_g} tại Cung {cung_can_gio} [{hanh_cung_cg}]):</b> Bạn hoàn toàn làm chủ và kiểm soát được sự việc"
    else:
        chu_khach_km_str = f"<b>Cung Bản Thân (Can Ngày {can_n} tại Cung {cung_can_ngay}) & Cung Sự Việc (Can Giờ {can_g} tại Cung {cung_can_gio}) tương thông ({hanh_cung_cn} ↔ {hanh_cung_cg})</b>"

    can_thien_dt = str(ctb.get(target_cung) or ctb.get(str(target_cung)) or can_n).strip()
    can_dia_dt = str(cdb.get(target_cung) or cdb.get(str(target_cung)) or can_m).strip()
    cach_cuc_81_str = f"Thiên Bàn Can <b>{can_thien_dt}</b> + Địa Bàn Can <b>{can_dia_dt}</b>"
    try:
        from luc_hao_ky_mon_rules import THAP_CAN_KHAC_UNG
        _cc_val = THAP_CAN_KHAC_UNG.get((can_thien_dt, can_dia_dt)) or THAP_CAN_KHAC_UNG.get(f"{can_thien_dt}+{can_dia_dt}")
        if _cc_val:
            cach_cuc_81_str += f" — <b>{_cc_val}</b>"
    except Exception:
        pass

    # Kiểm tra Ngũ Bất Ngộ Thời & Dịch Mã / Tuần Không Cung
    _NGU_BAT_NGO = {("Giáp", "Canh"), ("Ất", "Tân"), ("Bính", "Nhâm"), ("Đinh", "Quý"), ("Mậu", "Giáp"), ("Kỷ", "Ất"), ("Canh", "Bính"), ("Tân", "Đinh"), ("Nhâm", "Mậu"), ("Quý", "Kỷ")}
    is_ngu_bat_ngo = (can_n, can_g) in _NGU_BAT_NGO
    dich_ma_cung = chart_data.get("dich_ma")
    kv_cung_list = chart_data.get("khong_vong") or []
    km_special_flags = []
    if is_ngu_bat_ngo:
        km_special_flags.append("⚠️ <b>Phạm Ngũ Bất Ngộ Thời</b> (Can Giờ khắc Can Ngày đồng âm dương: cần hết sức bình tĩnh, tránh nóng vội)")
    if str(dich_ma_cung) == str(target_cung):
        km_special_flags.append("🐎 <b>Đắc Sao Dịch Mã (Mã Tinh) tại Cung</b> (Sự việc chuyển động rất nhanh, có tính dịch chuyển/thay đổi tốc độ cao)")
    if target_cung in kv_cung_list or str(target_cung) in [str(x) for x in kv_cung_list]:
        km_special_flags.append("💀 <b>Cung Dụng Thần lâm Tuần Không trên bàn Kỳ Môn</b> (Chứa yếu tố ẩn tàng, giảm một nửa thực lực hiện tại hoặc chờ Xuất Không)")
    if univ_mat.get("is_km_phuc_ngam"):
        km_special_flags.append("🔒 <b>Cục diện Phục Ngâm</b> (Sao & Cửa nằm tại bản cung: mọi việc đang giậm chân tại chỗ hoặc cất giữ cố định)")
    km_special_flags_str = " | ".join(km_special_flags) if km_special_flags else "Bàn Kỳ Môn không phạm Ngũ Bất Ngộ Thời, khí cục vận chuyển thông suốt"

    # -------------------------------------------------------------------------
    # IV. TỔNG HỢP BẢN PHÂN TÍCH A→Z TỪNG BƯỚC (HTML & TEXT CHO AI PRO)
    # -------------------------------------------------------------------------
    dong_hoa_html = "<br>".join(f"&nbsp;&nbsp;&nbsp;&nbsp;▸ {d}" for d in dong_hoa_details) if dong_hoa_details else "&nbsp;&nbsp;&nbsp;&nbsp;▸ Quẻ Tĩnh (6 hào an tĩnh, lấy Hào Thế, Hào Dụng Thần và Nhật/Nguyệt làm trọng tâm)."
    am_dong_np_html = ""
    if am_dong_list or nguyet_pha_list or tam_hop_found:
        _extra_lh = tam_hop_found + am_dong_list + nguyet_pha_list
        am_dong_np_html = f"<br>&nbsp;&nbsp;• <b>Yếu tố tác động ngầm (Tam Hợp / Ám Động / Nguyệt Phá):</b> {' | '.join(_extra_lh)}."

    nm_line_html = f"<br>&nbsp;&nbsp;• <b>Khớp Niên Mệnh Đích Danh (Mảnh ghép 2):</b> {univ_mat.get('nien_menh_summary')}" if univ_mat.get("nien_menh_summary") else ""

    deep_a_to_z_html = (
        f'<div style="margin-top:10px;padding:12px 14px;background:rgba(15,23,42,0.92);border-radius:10px;border:1px solid rgba(251,191,36,0.45);font-size:0.93em;color:#f1f5f9;line-height:1.58;">'
        f'<div style="font-weight:900;color:#fde047;font-size:1.0em;margin-bottom:8px;border-bottom:1px solid rgba(251,191,36,0.25);padding-bottom:5px;">'
        f'🔬 BÓC TÁCH SÂU TỪ A ĐẾN Z MỌI YẾU TỐ TÁC ĐỘNG TRÊN QUẺ (LỤC HÀO · MAI HOA · KỲ MÔN · THIẾT BẢN & TỬ VI THIÊN KỶ)'
        f'</div>'
        f'<b>1️⃣ Bóc tách Lục Hào Kinh Dịch từ A đến Z (10 Tầng Tác Động):</b><br>'
        f'&nbsp;&nbsp;• <b>Đặc tính Quẻ & Thế – Ứng:</b> {hex_trait_str}. Trục <b>Hào Thế (Hào {the_idx} {the_chi}-{the_nh}, Lục Thú: {the_luc_thu}) ↔ Hào Ứng (Hào {ung_idx} {ung_chi}-{ung_nh})</b>: {the_ung_rel}.<br>'
        f'&nbsp;&nbsp;• <b>Dụng Thần, Hào Vị & Lục Thú:</b> Dụng Thần <b>{dung_than} tại Hào {dt_idx} ({dt_chi}-{dt_nh})</b> ({dt_vi_info.get("ten_hao", f"Hào {dt_idx}")}: <i>{dt_vi_info.get("dia_ly", "")} / {dt_vi_info.get("nhan_su", "")}</i>) lâm Lục Thú <b>{dt_luc_thu}</b> (<i>{dt_lthu_desc}</i>).<br>'
        f'&nbsp;&nbsp;• <b>Nguyệt Lệnh ({chi_m}-{nh_m}), Nhật Thần ({chi_n}-{nh_n}), 12 Trường Sinh & Nhập Mộ:</b> Dụng Thần đạt trạng thái <b>{dt_season_state}</b>, trên Ngày {chi_n} lâm cung <b>{dt_ts_ngay}</b> (Hào Thế lâm <b>{the_ts_ngay}</b>). {mo_kho_note}.<br>'
        f'&nbsp;&nbsp;• <b>Lực lượng Nguyên Thần ({ng_nh}) vs Kỵ Thần ({ky_nh}) & Nguồn Tiền (Thê Tài):</b> Nguyên Thần sinh trợ: <b>{", ".join(nguyen_than_list) or "Ẩn phục"}</b> | Kỵ Thần khắc chế: <b>{", ".join(ky_than_list) or "Không có"}</b> | Nguồn lực Thê Tài: <b>{univ_mat.get("the_tai_status_str", "")}</b>.<br>'
        f'&nbsp;&nbsp;• <b>Phân tích Hào Động & Hào Biến (Tách Hiện Trạng vs Tiên Lượng):</b><br>{dong_hoa_html}'
        f'{am_dong_np_html}<br>'
        f'<b>2️⃣ Bóc tách Mai Hoa Dịch Số từ A đến Z (Tam Quái, Đảng Thể/Dụng & Vạn Vật Loại Tượng):</b><br>'
        f'&nbsp;&nbsp;• <b>Trục Tam Quái:</b> Quẻ Chủ <b>{full_chu}</b> (Thượng {up_chu} · Hạ {lo_chu}) ➔ Quẻ Hỗ <b>{full_ho}</b> (Thượng Hỗ {up_ho} · Hạ Hỗ {lo_ho}) ➔ Quẻ Biến <b>{full_bien}</b> (Thượng Biến {up_bien} · Hạ Biến {lo_bien}).<br>'
        f'&nbsp;&nbsp;• <b>Tương quan Thể – Dụng & Thời Lệnh:</b> Quẻ Thể <b>{the_quai} ({hanh_the} — {mh_the_season})</b> ↔ Quẻ Dụng <b>{dung_quai} ({hanh_dung} — {mh_dung_season})</b> đạt thế <b>{univ_mat.get("rel_chu_tag","")}</b> ({univ_mat.get("rel_chu_desc","")}); biến sang Quẻ Biến Dụng <b>{bien_dung_quai} ({hanh_bien_dung})</b> đạt thế <b>{univ_mat.get("rel_bien_tag","")}</b> ({univ_mat.get("rel_bien_desc","")}).<br>'
        f'&nbsp;&nbsp;• <b>Tác động ngầm của Quẻ Hỗ (Đảng Thể vs Đảng Dụng):</b> {dang_ho_verdict}<br>'
        f'<b>3️⃣ Bóc tách Kỳ Môn Độn Giáp từ A đến Z (Cung Chủ–Khách, Nội/Ngoại Bàn, Môn Bức & 81 Cách Cục):</b><br>'
        f'&nbsp;&nbsp;• <b>Không gian Nội/Ngoại Bàn & Cung Chủ – Khách:</b> {noi_ngoai_ban_str}. {chu_khach_km_str}.<br>'
        f'&nbsp;&nbsp;• <b>Tinh – Môn – Thần & Trạng thái Môn–Cung tại Cung {target_cung} ({quai_cung} — {huong_cung}):</b> Hội <b>Sao {sao_name}</b> ({univ_mat.get("sao_cat_lbl","")}: {univ_mat.get("sao_meaning","")}) · <b>Cửa {cua_name}</b> ({univ_mat.get("cua_cat_lbl","")}: {univ_mat.get("cua_meaning","")}) · <b>Thần {than_name}</b>. Trạng thái Môn–Cung: {mon_cung_state}.<br>'
        f'&nbsp;&nbsp;• <b>Cách Cục Lưu Bá Ôn & Cục Diện Đặc Biệt:</b> {cach_cuc_81_str}. {km_special_flags_str}.{nm_line_html}<br>'
        f'<b>4️⃣ Bóc tách Thiết Bản Thần Toán, Hoàng Cực Kinh Thế & Pháp Quyết Hóa Giải Thông Quan:</b><br>'
        f'&nbsp;&nbsp;• <b>Thiết Bản Khấu Đinh Điều Văn:</b> {univ_mat.get("thiet_ban_luan_giai", "")}<br>'
        f'&nbsp;&nbsp;• <b>Pháp Quyết Hóa Giải Thông Quan (Mảnh ghép 3):</b> Dụng Thần Thông Quan hành <b style="color:#fde047;">{(univ_mat.get("thong_quan_remedy") or {}).get("hanh_thong_quan", "Thổ")}</b> | Tam Cát Môn hiện tại: <b style="color:#4ade80;">{(univ_mat.get("thong_quan_remedy") or {}).get("km_cat_phuong", "")}</b>.'
        f'</div>'
    )

    deep_a_to_z_prompt_text = (
        f"=== HỒ SƠ 24 YẾU TỐ TÁC ĐỘNG SÂU & ẨN NGẦM TRÊN QUẺ (V117.0 — BẮT BUỘC PHÂN TÍCH ĐẦY ĐỦ) ===\n"
        f"1. [LỤC HÀO CHUYÊN SÂU]:\n"
        f"   - Đặc tính Quẻ: {re.sub(r'<[^>]+>', '', hex_trait_str)}\n"
        f"   - Tương quan Thế (Hào {the_idx} {the_chi}-{the_nh}, {the_luc_thu}) ↔ Ứng (Hào {ung_idx} {ung_chi}-{ung_nh}): {re.sub(r'<[^>]+>', '', the_ung_rel)}\n"
        f"   - Dụng Thần [{dung_than}] tại Hào {dt_idx} ({dt_chi}-{dt_nh}, Lục Thú: {dt_luc_thu} [{dt_lthu_desc}]): {dt_season_state} | Vòng 12 Trường Sinh ngày {chi_n}: {dt_ts_ngay} | {re.sub(r'<[^>]+>', '', mo_kho_note)}\n"
        f"   - Nguyên Thần ({ng_nh}): {', '.join(nguyen_than_list) or 'Ẩn phục'} | Kỵ Thần ({ky_nh}): {', '.join(ky_than_list) or 'Không có'}\n"
        f"   - Chi tiết Động/Biến (Hồi đầu sinh/khắc, Hóa Tiến/Thoái): {'; '.join(re.sub(r'<[^>]+>', '', x) for x in dong_hoa_details) or 'Quẻ Tĩnh'}\n"
        f"   - Tam Hợp Cục / Ám Động / Nguyệt Phá: {'; '.join(re.sub(r'<[^>]+>', '', x) for x in (tam_hop_found + am_dong_list + nguyet_pha_list)) or 'Không phạm'}\n"
        f"2. [MAI HOA CHUYÊN SÂU]:\n"
        f"   - Quẻ Thể {the_quai} ({hanh_the}: {mh_the_season}) ↔ Quẻ Dụng {dung_quai} ({hanh_dung}: {mh_dung_season})\n"
        f"   - Đảng Thể vs Đảng Dụng trên Quẻ Hỗ ({full_ho}): {re.sub(r'<[^>]+>', '', dang_ho_verdict)}\n"
        f"3. [KỲ MÔN CHUYÊN SÂU]:\n"
        f"   - Nội/Ngoại Bàn: {re.sub(r'<[^>]+>', '', noi_ngoai_ban_str)}\n"
        f"   - Tương quan Cung Can Ngày ({can_n}) ↔ Cung Can Giờ ({can_g}): {re.sub(r'<[^>]+>', '', chu_khach_km_str)}\n"
        f"   - Trạng thái Môn-Cung: {re.sub(r'<[^>]+>', '', mon_cung_state)} | Cách Cục Lưu Bá Ôn: {re.sub(r'<[^>]+>', '', cach_cuc_81_str)} | Cục diện: {re.sub(r'<[^>]+>', '', km_special_flags_str)}\n"
    )

    return {
        "hex_trait_str": hex_trait_str,
        "the_ung_rel": the_ung_rel,
        "dt_season_state": dt_season_state,
        "dt_ts_ngay": dt_ts_ngay,
        "mo_kho_note": mo_kho_note,
        "nguyen_than_list": nguyen_than_list,
        "ky_than_list": ky_than_list,
        "am_dong_list": am_dong_list,
        "nguyet_pha_list": nguyet_pha_list,
        "tam_hop_found": tam_hop_found,
        "dong_hoa_details": dong_hoa_details,
        "dang_ho_verdict": dang_ho_verdict,
        "noi_ngoai_ban_str": noi_ngoai_ban_str,
        "mon_cung_state": mon_cung_state,
        "chu_khach_km_str": chu_khach_km_str,
        "cach_cuc_81_str": cach_cuc_81_str,
        "km_special_flags_str": km_special_flags_str,
        "deep_a_to_z_html": deep_a_to_z_html,
        "deep_a_to_z_prompt_text": deep_a_to_z_prompt_text,
    }



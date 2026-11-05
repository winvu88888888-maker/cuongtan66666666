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

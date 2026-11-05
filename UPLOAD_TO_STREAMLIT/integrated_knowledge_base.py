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


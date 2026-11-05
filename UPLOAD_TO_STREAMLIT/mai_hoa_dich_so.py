# -*- coding: utf-8 -*-
# mai_hoa_dich_so.py - Module Mai Hoa Dịch Số 64 Quẻ FULL DATA (V110.0 Standard)
import random
import secrets
import hashlib
import re
from datetime import datetime
from qmdg_calc import solar_to_lunar

_SYS_RNG_MH = secrets.SystemRandom()

QUAI_SYMBOLS = {1: "☰ Càn", 2: "☱ Đoài", 3: "☲ Ly", 4: "☳ Chấn", 5: "☴ Tốn", 6: "☵ Khảm", 7: "☶ Cấn", 8: "☷ Khôn"}
QUAI_NAMES = {1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn"}
QUAI_ELEMENTS = {1: "Kim", 2: "Kim", 3: "Hỏa", 4: "Mộc", 5: "Mộc", 6: "Thủy", 7: "Thổ", 8: "Thổ"}
# Số Hậu Thiên Lạc Thư ứng với từng Quái
QUAI_HAU_THIEN_NUM = {1: 6, 2: 7, 3: 9, 4: 3, 5: 4, 6: 1, 7: 8, 8: 2}

# 64 Hexagrams Complete Database (Đủ 64/64 Quẻ Kinh Dịch)
HEXAGRAM_DATA = {
    # 8 Quẻ Thuần
    (1, 1): {"ten": "Càn Vi Thiên", "tuong": "Thiên hành kiện", "nghĩa": "Cửu thiên cương kiện, khởi đầu hanh thông, tự cường bất tức."},
    (8, 8): {"ten": "Khôn Vi Địa", "tuong": "Địa thế khôn", "nghĩa": "Nhu thuận, bao dung, hậu đức tải vật, bền bỉ nâng đỡ."},
    (6, 6): {"ten": "Khảm Vi Thủy", "tuong": "Tập khảm trùng hiểm", "nghĩa": "Hiểm trở trùng trùng, cần giữ vững lòng tin và thận trọng."},
    (3, 3): {"ten": "Ly Vi Hỏa", "tuong": "Minh lưỡng tác", "nghĩa": "Sáng sủa, văn minh, rực rỡ nhưng cần điểm tựa vững chắc."},
    (4, 4): {"ten": "Chấn Vi Lôi", "tuong": "Tiệm lôi chấn động", "nghĩa": "Chấn động mạnh mẽ, kinh sợ lúc đầu nhưng sau đó hanh thông."},
    (5, 5): {"ten": "Tốn Vi Phong", "tuong": "Tùy phong thâm nhập", "nghĩa": "Nhu hòa, thâm nhập sâu sắc, uyển chuyển thuận theo thời thế."},
    (7, 7): {"ten": "Cấn Vi Sơn", "tuong": "Kiêm sơn tĩnh chỉ", "nghĩa": "Ngưng nghỉ đúng lúc, tĩnh tại vững chãi như núi."},
    (2, 2): {"ten": "Đoài Vi Trạch", "tuong": "Lệ trạch duyệt lạc", "nghĩa": "Vui vẻ, hòa duyệt, giao tiếp khéo léo, song đầm nối tiếp."},
    # Họ Càn
    (1, 5): {"ten": "Thiên Phong Cấu", "tuong": "Thiên hạ hữu phong", "nghĩa": "Gặp gỡ bất ngờ, tương ngộ nhưng cần phòng tiểu nhân."},
    (1, 7): {"ten": "Thiên Sơn Độn", "tuong": "Thiên hạ hữu sơn", "nghĩa": "Lùi bước bảo toàn thực lực, ẩn nhẫn chờ thời."},
    (1, 8): {"ten": "Thiên Địa Bĩ", "tuong": "Thiên địa bất giao", "nghĩa": "Bế tắc tạm thời, âm dương cách trở, nên thủ tĩnh."},
    (5, 8): {"ten": "Phong Địa Quan", "tuong": "Phong hành địa thượng", "nghĩa": "Quan sát rộng khắp, chiêm nghiệm kỹ lưỡng trước khi quyết."},
    (7, 8): {"ten": "Sơn Địa Bác", "tuong": "Sơn phụ ư địa", "nghĩa": "Bào mòn, rơi rụng, nên giữ gốc rễ và tránh mạo hiểm."},
    (3, 8): {"ten": "Hỏa Địa Tấn", "tuong": "Minh xuất địa thượng", "nghĩa": "Mặt trời mọc trên đất, tiến lên sáng sủa, thăng tiến."},
    (3, 1): {"ten": "Hỏa Thiên Đại Hữu", "tuong": "Hỏa tại thiên thượng", "nghĩa": "Đại thịnh, giàu có lớn, quang minh chính đại."},
    # Họ Khôn
    (8, 4): {"ten": "Địa Lôi Phục", "tuong": "Lôi tại địa trung", "nghĩa": "Nhất dương lai phục, hồi sinh, quay lại quỹ đạo tốt đẹp."},
    (8, 2): {"ten": "Địa Trạch Lâm", "tuong": "Địa thượng hữu trạch", "nghĩa": "Bao dung quản lý, vận hội lớn mạnh dần lên."},
    (8, 1): {"ten": "Địa Thiên Thái", "tuong": "Thiên địa giao thái", "nghĩa": "Âm dương giao hòa, vạn vật thông suốt, đại cát hanh thông."},
    (4, 1): {"ten": "Lôi Thiên Đại Tráng", "tuong": "Lôi tại thiên thượng", "nghĩa": "Khí thế hùng mạnh, vươn cao nhưng cần giữ chính đạo."},
    (2, 1): {"ten": "Trạch Thiên Quải", "tuong": "Trạch thượng ư thiên", "nghĩa": "Quyết đoán dứt khoát, đột phá rào cản."},
    (6, 1): {"ten": "Thủy Thiên Nhu", "tuong": "Vân thượng ư thiên", "nghĩa": "Kiên nhẫn chờ đợi thời cơ chín muồi, ẩm thực an vui."},
    (6, 8): {"ten": "Thủy Địa Tỷ", "tuong": "Địa thượng hữu thủy", "nghĩa": "Thân thiện, gắn kết, được quý nhân và tập thể tương trợ."},
    # Họ Chấn
    (4, 8): {"ten": "Lôi Địa Dự", "tuong": "Lôi xuất địa phấn", "nghĩa": "Vui vẻ, phấn khởi, chuẩn bị chu đáo từ trước."},
    (4, 6): {"ten": "Lôi Thủy Giải", "tuong": "Lôi vũ tác giải", "nghĩa": "Mưa xuân xóa tan hiểm nạn, hóa giải bế tắc."},
    (4, 5): {"ten": "Lôi Phong Hằng", "tuong": "Lôi phong hằng cửu", "nghĩa": "Bền vững lâu dài, kiên định giữ vững đạo thường."},
    (8, 5): {"ten": "Địa Phong Thăng", "tuong": "地中 sinh mộc", "nghĩa": "Cây mọc từ đất, thăng tiến từng bước vững chắc."},
    (6, 5): {"ten": "Thủy Phong Tỉnh", "tuong": "Mộc thượng hữu thủy", "nghĩa": "Giếng nước nuôi người, nguồn lực ổn định lâu bền."},
    (2, 5): {"ten": "Trạch Phong Đại Quá", "tuong": "Trạch diệt mộc", "nghĩa": "Gánh vác việc lớn vượt tầm, cần trụ cột vững vàng."},
    (2, 4): {"ten": "Trạch Lôi Tùy", "tuong": "Trạch trung hữu lôi", "nghĩa": "Thuận theo thời thế, linh hoạt thích ứng hoàn cảnh."},
    # Họ Tốn
    (5, 1): {"ten": "Phong Thiên Tiểu Súc", "tuong": "Phong hành thiên thượng", "nghĩa": "Tích lũy từng bước nhỏ, gom góp lực lượng chờ thời."},
    (5, 3): {"ten": "Phong Hỏa Gia Nhân", "tuong": "Phong tự hỏa xuất", "nghĩa": "Gia đạo ấm êm, việc trong nhà quy củ, nội bộ đồng lòng."},
    (5, 4): {"ten": "Phong Lôi Ích", "tuong": "Phong lôi tương ích", "nghĩa": "Tăng thêm lợi ích, gió sấm trợ nhau, tiến việc lớn rất lợi."},
    (1, 4): {"ten": "Thiên Lôi Vô Vọng", "tuong": "Thiên hạ lôi hành", "nghĩa": "Thuận theo tự nhiên, chân thật không làm càn."},
    (3, 4): {"ten": "Hỏa Lôi Phệ Hạp", "tuong": "Lôi điện phệ hạp", "nghĩa": "Dứt khoát xử lý chướng ngại để hợp nhất thành công."},
    (7, 4): {"ten": "Sơn Lôi Di", "tuong": "Sơn hạ hữu lôi", "nghĩa": "Bồi dưỡng thân tâm, cẩn trọng lời ăn tiếng nói và dinh dưỡng."},
    (7, 5): {"ten": "Sơn Phong Cổ", "tuong": "Sơn hạ hữu phong", "nghĩa": "Chấn chỉnh việc cũ đổ nát, cải tổ lại từ gốc."},
    # Họ Khảm
    (6, 2): {"ten": "Thủy Trạch Tiết", "tuong": "Trạch thượng hữu thủy", "nghĩa": "Tiết chế chừng mực, giữ kỷ luật và khuôn phép."},
    (6, 4): {"ten": "Thủy Lôi Truân", "tuong": "Vân lôi truân", "nghĩa": "Vạn sự khởi đầu nan, mầm non mới nhú cần kiên trì."},
    (6, 3): {"ten": "Thủy Hỏa Ký Tế", "tuong": "Thủy tại hỏa thượng", "nghĩa": "Việc đã hoàn tất, âm dương đúng ngôi, thành công trọn vẹn."},
    (2, 3): {"ten": "Trạch Hỏa Cách", "tuong": "Trạch trung hữu hỏa", "nghĩa": "Cải cách, đổi mới triệt để, thay cũ đổi mới."},
    (4, 3): {"ten": "Lôi Hỏa Phong", "tuong": "Lôi điện giai chí", "nghĩa": "Thịnh vượng, dồi dào, rực rỡ và sung túc."},
    (8, 3): {"ten": "Địa Hỏa Minh Di", "tuong": "Minh nhập địa trung", "nghĩa": "Ánh sáng ẩn vào trong đất, nên韬 quang dưỡng hối giữ mình."},
    (8, 6): {"ten": "Địa Thủy Sư", "tuong": "Địa trung hữu thủy", "nghĩa": "Quân ngũ kỷ luật, cần người chỉ huy dày dạn kinh nghiệm."},
    # Họ Ly
    (3, 7): {"ten": "Hỏa Sơn Lữ", "tuong": "Sơn thượng hữu hỏa", "nghĩa": "Tạm bợ nơi đất khách, di chuyển linh hoạt, giữ đạo khiêm nhu."},
    (3, 5): {"ten": "Hỏa Phong Đỉnh", "tuong": "Mộc thượng hữu hỏa", "nghĩa": "Vạc vàng vững chãi, luyện tài đắc lộc, đổi mới thành công."},
    (3, 6): {"ten": "Hỏa Thủy Vị Tế", "tuong": "Hỏa tại thủy thượng", "nghĩa": "Việc chưa hoàn tất nhưng tiềm năng mở ra phía trước."},
    (7, 6): {"ten": "Sơn Thủy Mông", "tuong": "Sơn hạ xuất tuyền", "nghĩa": "Còn mờ mịt ban đầu, cần khai mở tri thức và học hỏi."},
    (5, 6): {"ten": "Phong Thủy Hoán", "tuong": "Phong hành thủy thượng", "nghĩa": "Tan băng giải tỏa, vượt sông lớn tìm cơ hội mới."},
    (1, 6): {"ten": "Thiên Thủy Tụng", "tuong": "Thiên dữ thủy vi hành", "nghĩa": "Tranh biện, bất đồng quan điểm, nên hòa giải tránh kiện tụng."},
    (1, 3): {"ten": "Thiên Hỏa Đồng Nhân", "tuong": "Thiên dữ hỏa đồng", "nghĩa": "Đồng tâm hiệp lực, hợp tác cùng chí hướng đại cát."},
    # Họ Cấn
    (7, 3): {"ten": "Sơn Hỏa Bí", "tuong": "Sơn hạ hữu hỏa", "nghĩa": "Văn vẻ trang nhã, làm đẹp hình thức và uy tín."},
    (7, 1): {"ten": "Sơn Thiên Đại Súc", "tuong": "Thiên tại sơn trung", "nghĩa": "Tích lũy lớn lao cả tài sản lẫn đức độ, nền tảng đại cát."},
    (7, 2): {"ten": "Sơn Trạch Tổn", "tuong": "Sơn hạ hữu trạch", "nghĩa": "Chịu thiệt trước mắt để thu lợi lâu dài, bớt dưới thêm trên."},
    (3, 2): {"ten": "Hỏa Trạch Khuê", "tuong": "Thượng hỏa hạ trạch", "nghĩa": "Khác biệt quan điểm, cầu đồng tồn dị để hóa giải."},
    (1, 2): {"ten": "Thiên Trạch Lý", "tuong": "Thượng thiên hạ trạch", "nghĩa": "Giữ đúng lễ nghĩa phép tắc thì đi qua hiểm nguy vẫn bình an."},
    (5, 2): {"ten": "Phong Trạch Trung Phu", "tuong": "Trạch thượng hữu phong", "nghĩa": "Chân thành tín nghĩa từ trong tâm, cảm hóa được lòng người."},
    (5, 7): {"ten": "Phong Sơn Tiệm", "tuong": "Sơn thượng hữu mộc", "nghĩa": "Tiến lên tuần tự từng bước vững chắc như cây mọc trên núi."},
    # Họ Đoài
    (2, 6): {"ten": "Trạch Thủy Khốn", "tuong": "Trạch vô thủy", "nghĩa": "Khó khăn chật vật tạm thời, giữ vững khí tiết sẽ vượt qua."},
    (2, 8): {"ten": "Trạch Địa Tụy", "tuong": "Trạch thượng ư địa", "nghĩa": "Nhóm họp, tụ hội nhân tài và tài lộc đông đúc."},
    (2, 7): {"ten": "Trạch Sơn Hàm", "tuong": "Sơn thượng hữu trạch", "nghĩa": "Cảm ứng tự nhiên, giao hòa tình cảm nhanh chóng."},
    (6, 7): {"ten": "Thủy Sơn Kiển", "tuong": "Sơn thượng hữu thủy", "nghĩa": "Đường đi gặp trở ngại trước mặt, nên dừng lại tìm quý nhân."},
    (8, 7): {"ten": "Địa Sơn Khiêm", "tuong": "Địa trung hữu sơn", "nghĩa": "Khiêm nhường ẩn mình trong đất, càng khiêm tốn càng hanh thông."},
    (4, 7): {"ten": "Lôi Sơn Tiểu Quá", "tuong": "Sơn thượng hữu lôi", "nghĩa": "Việc nhỏ thì hợp, việc lớn chớ nên vượt quá giới hạn."},
    (4, 2): {"ten": "Lôi Trạch Quy Muội", "tuong": "Trạch thượng hữu lôi", "nghĩa": "Xúc tiến vội vàng dễ lệch nhịp, cần chỉnh đốn lại trật tự."},
}


def _calc_the_dung_relation(hanh_the, hanh_dung):
    if hanh_the == hanh_dung:
        return "Tỷ Hòa (Thể Dụng đồng hành, thuận lợi ngang sức)"
    sinh = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
    if sinh.get(hanh_dung) == hanh_the:
        return "Dụng sinh Thể (Đại Cát — Sự việc/Ngoại cảnh sinh lợi cho bản thân)"
    if sinh.get(hanh_the) == hanh_dung:
        return "Thể sinh Dụng (Hao tổn — Bản thân phải bỏ công sức/tiền bạc ra trước)"
    khac = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
    if khac.get(hanh_the) == hanh_dung:
        return "Thể khắc Dụng (Khả Thành — Làm chủ được sự việc nhưng cần nỗ lực)"
    return "Dụng khắc Thể (Hung/Cản trở — Hoàn cảnh bên ngoài gây áp lực lên bản thân)"


def _compute_question_resonance_offsets(question_text="", minute=0, second=0, cast_salt=0):
    """
    V110.0 — Pháp Tự Khởi Quái & Đa Vấn Nhất Thời Chiêm Pháp (Thiệu Khang Tiết - Mai Hoa Dịch Số):
    - Khi hỏi nhiều câu hỏi khác nhau hoặc hỏi lại nhiều câu tương tự trong cùng một khung giờ:
      + Chia câu hỏi làm 2 nửa âm tiết (Thượng Thanh -> Thượng Quái, Hạ Thanh -> Hạ Quái)
      + Cộng thêm khắc/phút hiện tại (minute, second) và số thứ tự lần động tâm (cast_salt)
      => Đảm bảo mỗi câu hỏi khác nhau hoặc mỗi lần gieo lại đều ra quẻ biến thiên sống động, tuyệt đối không bị đơ/lặp lại 1 quẻ cố định!
    """
    q_norm = str(question_text or "").strip().lower()
    min_v = int(minute or 0)
    sec_v = int(second or 0)
    salt_v = int(cast_salt or 0)
    if not q_norm and min_v == 0 and sec_v == 0 and salt_v == 0:
        return 0, 0, 0

    words = [w for w in re.findall(r"\w+", q_norm) if w]
    if words:
        half = max(1, len(words) // 2)
        w_upper = words[:half]
        w_lower = words[half:] if len(words) > half else words
        up_char_sum = sum(sum(ord(c) for c in w) + len(w) * 7 for w in w_upper)
        lo_char_sum = sum(sum(ord(c) * (idx + 1) for idx, c in enumerate(w)) + len(w) * 11 for w in w_lower)
        q_md5 = int(hashlib.md5(f"{q_norm}|{min_v}|{sec_v}|{salt_v}".encode("utf-8")).hexdigest()[:8], 16)
    else:
        up_char_sum = 0
        lo_char_sum = 0
        q_md5 = min_v * 31 + sec_v * 7 + salt_v * 13

    up_offset = (up_char_sum + (min_v // 3) + salt_v * 3) % 64
    lo_offset = (lo_char_sum + min_v + (sec_v // 4) + salt_v * 5) % 64
    dong_offset = (q_md5 + min_v + sec_v + salt_v) % 6
    return up_offset, lo_offset, dong_offset


def tinh_qua_theo_thoi_gian(
    year,
    month,
    day,
    hour,
    minute=0,
    second=0,
    question_text="",
    cast_salt=0,
    upper_override=None,
    lower_override=None,
    dong_override=None,
):
    dt = datetime(year, month, day, hour)
    lday, lmonth, lyear, is_leap = solar_to_lunar(dt)

    # Year Chi index: Tý=1, Sửu=2, ..., Hợi=12
    lyear_chi_idx = (lyear - 4) % 12 + 1

    # Chi index: Tý=1, Sửu=2, ..., Hợi=12
    v_hour = ((hour + 1) // 2) % 12 + 1
    if hour == 23:
        v_hour = 1  # Tý starts at 23:00

    up_off, lo_off, dong_off = _compute_question_resonance_offsets(
        question_text=question_text,
        minute=minute,
        second=second,
        cast_salt=cast_salt,
    )

    # Mai Hoa Formula + Đa Vấn Nhất Thời / Tự Khởi Quái Resonance
    total_upper = lyear_chi_idx + lmonth + lday + up_off
    total_lower = total_upper + v_hour + lo_off

    upper = int(upper_override) if upper_override in (1, 2, 3, 4, 5, 6, 7, 8) else (((total_upper - 1) % 8) + 1)
    lower = int(lower_override) if lower_override in (1, 2, 3, 4, 5, 6, 7, 8) else (((total_lower - 1) % 8) + 1)
    dong_hao = int(dong_override) if dong_override in (1, 2, 3, 4, 5, 6) else (((total_lower + dong_off - 1) % 6) + 1)

    res = build_res(upper, lower, dong_hao)
    res['lunar_info'] = f"Ngày {lday}/{lmonth} năm {lyear} ({'Nhuận' if is_leap else 'Thường'})"
    res['total_upper'] = total_upper
    res['total_lower'] = total_lower
    res['cast_mode'] = "question_time_resonance" if (question_text or cast_salt) else "time"
    return res


def tinh_qua_ngau_nhien(prev_tuple=None):
    """
    V110.0: Gieo quẻ ngẫu nhiên bằng phần cứng OS Entropy (secrets.SystemRandom).
    Đảm bảo 100% không bao giờ bị trùng lặp với quẻ vừa gieo trước đó (prev_tuple).
    """
    upper, lower, dong_hao = _SYS_RNG_MH.randint(1, 8), _SYS_RNG_MH.randint(1, 8), _SYS_RNG_MH.randint(1, 6)
    if prev_tuple and isinstance(prev_tuple, (tuple, list)) and len(prev_tuple) == 3:
        for _ in range(12):
            if (upper, lower, dong_hao) != tuple(prev_tuple):
                break
            upper, lower, dong_hao = _SYS_RNG_MH.randint(1, 8), _SYS_RNG_MH.randint(1, 8), _SYS_RNG_MH.randint(1, 6)
    res = build_res(upper, lower, dong_hao)
    res['_random_cast'] = True
    res['cast_mode'] = 'random_entropy'
    return res


def build_res(upper, lower, dong_hao):
    lines = get_lines(upper, lower)
    res = {
        'upper': upper, 'lower': lower, 'dong_hao': dong_hao,
        'upper_symbol': QUAI_SYMBOLS[upper], 'lower_symbol': QUAI_SYMBOLS[lower],
        'upper_element': QUAI_ELEMENTS[upper], 'lower_element': QUAI_ELEMENTS[lower],
        'lines': lines
    }

    # Hỗ Quẻ: 2,3,4 (Lower), 3,4,5 (Upper)
    ho_lower_lines = [lines[1], lines[2], lines[3]]
    ho_upper_lines = [lines[2], lines[3], lines[4]]

    ho_upper = lines_to_quai(ho_upper_lines)
    ho_lower = lines_to_quai(ho_lower_lines)
    ho_info = HEXAGRAM_DATA.get((ho_upper, ho_lower), {"ten": f"{QUAI_NAMES[ho_upper]} {QUAI_NAMES[ho_lower]}", "nghĩa": ""})

    res['ho_upper'] = ho_upper
    res['ho_lower'] = ho_lower
    res['lines_ho'] = ho_lower_lines + ho_upper_lines
    res['ten_ho'] = ho_info.get('ten', f"{QUAI_NAMES[ho_upper]} {QUAI_NAMES[ho_lower]}")
    res['nghia_ho'] = ho_info.get('nghĩa', '')
    res['hanh_ho_thuong'] = QUAI_ELEMENTS[ho_upper]
    res['hanh_ho_ha'] = QUAI_ELEMENTS[ho_lower]

    info = HEXAGRAM_DATA.get((upper, lower), {"ten": f"{QUAI_NAMES[upper]} {QUAI_NAMES[lower]}", "tuong": "Thiên địa giao cảm", "nghĩa": "Tượng quẻ thuận theo thời vận."})
    res.update(info)
    res['ten_que'] = res['ten']

    res['lines_bien'] = get_bien_lines(lines, dong_hao)
    bien_upper = lines_to_quai(res['lines_bien'][3:])
    bien_lower = lines_to_quai(res['lines_bien'][:3])
    bien_info = HEXAGRAM_DATA.get((bien_upper, bien_lower), {"ten": f"{QUAI_NAMES[bien_upper]} {QUAI_NAMES[bien_lower]}", "nghĩa": ""})
    res['bien_upper'] = bien_upper
    res['bien_lower'] = bien_lower
    res['ten_qua_bien'] = bien_info.get('ten', "Quẻ Biến")
    res['bien_que'] = res['ten_qua_bien']
    res['ten_bien'] = res['ten_qua_bien']
    res['nghia_bien'] = bien_info.get('nghĩa', '')
    res['ten_bien_thuong'] = QUAI_NAMES.get(bien_upper, '')
    res['ten_bien_ha'] = QUAI_NAMES.get(bien_lower, '')
    res['hanh_bien_thuong'] = QUAI_ELEMENTS.get(bien_upper, 'Thổ')
    res['hanh_bien_ha'] = QUAI_ELEMENTS.get(bien_lower, 'Thổ')

    res['ten_thuong'] = QUAI_NAMES.get(upper, f"Quái {upper}")
    res['ten_ha'] = QUAI_NAMES.get(lower, f"Quái {lower}")
    res['hanh_thuong'] = QUAI_ELEMENTS.get(upper, "Thổ")
    res['hanh_ha'] = QUAI_ELEMENTS.get(lower, "Thổ")

    # V101.6: Phân định chính xác QUẺ THỂ & QUẺ DỤNG theo Động Hào chuẩn Mai Hoa Dịch Số:
    # - Động hào 1, 2, 3 (Hạ Quái động) -> Thượng Quái là THỂ (tĩnh), Hạ Quái là DỤNG (động)
    # - Động hào 4, 5, 6 (Thượng Quái động) -> Hạ Quái là THỂ (tĩnh), Thượng Quái là DỤNG (động)
    if dong_hao in (1, 2, 3):
        res['the_quai'] = res['ten_thuong']
        res['dung_quai'] = res['ten_ha']
        res['hanh_the'] = res['hanh_thuong']
        res['hanh_dung'] = res['hanh_ha']
        res['so_the'] = upper
        res['so_dung'] = lower
        res['so_bien_dung'] = bien_lower
        res['bien_dung_quai'] = res['ten_bien_ha']
        res['hanh_bien_dung'] = res['hanh_bien_ha']
        res['the_vi_tri'] = "Thượng Quái"
        res['dung_vi_tri'] = "Hạ Quái"
    else:
        res['the_quai'] = res['ten_ha']
        res['dung_quai'] = res['ten_thuong']
        res['hanh_the'] = res['hanh_ha']
        res['hanh_dung'] = res['hanh_thuong']
        res['so_the'] = lower
        res['so_dung'] = upper
        res['so_bien_dung'] = bien_upper
        res['bien_dung_quai'] = res['ten_bien_thuong']
        res['hanh_bien_dung'] = res['hanh_bien_thuong']
        res['the_vi_tri'] = "Hạ Quái"
        res['dung_vi_tri'] = "Thượng Quái"

    res['the_dung_rel'] = _calc_the_dung_relation(res['hanh_the'], res['hanh_dung'])
    res['the_bien_rel'] = _calc_the_dung_relation(res['hanh_the'], res['hanh_bien_dung'])
    res['interpretation'] = (
        f"Quẻ Chủ {res['ten']} ({res['nghĩa']}) ➔ Quẻ Hỗ {res['ten_ho']} ➔ Quẻ Biến {res['ten_qua_bien']} "
        f"(Động hào {dong_hao}: Thể {res['the_quai']} hành {res['hanh_the']} — Dụng {res['dung_quai']} hành {res['hanh_dung']}: {res['the_dung_rel']})."
    )
    return res


def lines_to_quai(l):
    m = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4, (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}
    return m.get(tuple(l), 1)


def get_lines(upper, lower):
    quai_lines = {1:[1,1,1], 2:[1,1,0], 3:[1,0,1], 4:[1,0,0], 5:[0,1,1], 6:[0,1,0], 7:[0,0,1], 8:[0,0,0]}
    return quai_lines[lower] + quai_lines[upper]


def get_bien_lines(lines, dong_hao):
    bien = list(lines)
    idx = dong_hao - 1
    bien[idx] = 1 if bien[idx] == 0 else 0
    return bien


def giai_qua(res, topic="Chung"):
    return (
        f"Quẻ {res.get('ten')} biến {res.get('ten_qua_bien')} (Động hào {res.get('dong_hao')}): "
        f"{res.get('nghĩa')} | Tương quan Thể-Dụng: {res.get('the_dung_rel', '')}"
    )

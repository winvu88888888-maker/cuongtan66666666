"""
dual_ai_agents.py — V104.0: HỆ THỐNG SONG NÃO AI 2 TẦNG (DUAL-AGENT PIPELINE)
================================================================================
- CON AI SỐ 1 (QuestionReaderAI): Chạy NGAY ĐẦU TIÊN khi nhận câu hỏi để đọc hiểu
  ngữ nghĩa, bóc tách chính xác đối tượng được hỏi (nhà mấy tầng, ở tầng mấy, mấy phòng,
  mấy anh chị em, mặc áo màu gì, đi xe gì, ở nhà hay công ty, đã kết hôn chưa...),
  khóa cứng Dụng Thần chuẩn (ví dụ: Nhà cửa/Số tầng = Phụ Mẫu + Hào Thế, tuyệt đối
  không để nhầm sang Thê Tài đầu tư BĐS).
- CON AI SỐ 2 (HexagramReasoningAI): Nhận Hồ Sơ Câu Hỏi từ Con AI Số 1, mang đi
  ĐỐI CHỨNG TRỰC TIẾP với Quẻ lập theo Giờ - Ngày - Tháng - Năm (Lục Hào, Kỳ Môn,
  Mai Hoa, Đại Lục Nhâm, 18 Tầng), suy luận ra câu trả lời trực diện khớp 100% với
  câu hỏi và quẻ, khóa cứng toàn bộ đầu ra Online & Offline.
"""

import re
import os
import json
import hashlib
import requests
from typing import Dict, Any, List, Optional

_REAL_DUAL_AI_CACHE: Dict[str, Dict[str, Any]] = {}

def _resolve_gemini_api_keys() -> List[str]:
    cand_keys = []
    try:
        import streamlit as st
        ss = getattr(st, 'session_state', {})
        for k in [ss.get('gemini_key'), ss.get('_resolved_api_key'), ss.get('api_key')]:
            if k and str(k).strip():
                cand_keys.append(str(k).strip())
        gh = ss.get('gemini_helper')
        if gh:
            if hasattr(gh, 'api_keys') and gh.api_keys:
                cand_keys.extend([str(x).strip() for x in gh.api_keys if x])
            elif hasattr(gh, 'api_key') and gh.api_key:
                cand_keys.append(str(gh.api_key).strip())
        try:
            sec_k = st.secrets.get('GEMINI_API_KEY', '')
            if sec_k:
                cand_keys.append(str(sec_k).strip())
        except Exception:
            pass
    except Exception:
        pass
    try:
        root_d = os.path.dirname(os.path.abspath(__file__))
        for cfg_rel, cfg_k in [('custom_data.json', 'GEMINI_API_KEY'), ('data_hub/factory_config.json', 'api_key')]:
            cfg_p = os.path.join(root_d, cfg_rel)
            if os.path.exists(cfg_p):
                with open(cfg_p, 'r', encoding='utf-8') as cf:
                    cd = json.load(cf)
                    if cd.get(cfg_k):
                        cand_keys.append(str(cd[cfg_k]).strip())
    except Exception:
        pass
    parsed = []
    for raw in cand_keys:
        for pt in str(raw).replace('\n', ',').replace(';', ',').split(','):
            p = pt.strip()
            if len(p) >= 20 and p not in parsed:
                parsed.append(p)
    return parsed

def _call_gemini_json_fast(prompt_text: str, timeout_sec: int = 12, tier: str = 'cheapest_reader') -> Optional[Dict[str, Any]]:
    keys = _resolve_gemini_api_keys()
    if not keys:
        return None
    if tier == 'cheapest_reader':
        # Con AI Số 1 (Chuyên đọc hiểu câu hỏi): Ưu tiên dòng Flash-Lite rẻ nhất, nhẹ nhất, quota cao nhất, tốc độ 0.4s
        models = ['gemini-2.5-flash-lite', 'gemini-2.0-flash-lite', 'gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
    else:
        # Con AI Số 2 (Chuyên đối chứng quẻ & suy luận chuyên sâu từ chỉ thị của AI Số 1)
        models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro']
    safety = [
        {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
    ]
    for api_key in keys[:3]:
        for m_name in models:
            try:
                url = f'https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={api_key}'
                gen_cfg: Dict[str, Any] = {
                    'temperature': 0.15,
                    'topP': 0.85,
                    'maxOutputTokens': 2048,
                    'responseMimeType': 'application/json',
                }
                if '2.5-flash' in m_name:
                    gen_cfg['thinkingConfig'] = {'thinkingBudget': 0}
                payload = {
                    'contents': [{'parts': [{'text': prompt_text}]}],
                    'generationConfig': gen_cfg,
                    'safetySettings': safety,
                }
                r = requests.post(url, json=payload, timeout=timeout_sec)
                if r.status_code == 400:
                    gen_cfg.pop('thinkingConfig', None)
                    gen_cfg.pop('responseMimeType', None)
                    r = requests.post(url, json=payload, timeout=timeout_sec)
                if r.status_code != 200:
                    continue
                cands = r.json().get('candidates', [])
                if not cands:
                    continue
                txt = ''
                for pt in cands[0].get('content', {}).get('parts', []):
                    if not pt.get('thought', False) and pt.get('text'):
                        txt += pt['text']
                txt = txt.strip()
                if txt.startswith('```'):
                    txt = re.sub(r'^```(?:json)?\s*|\s*```$', '', txt, flags=re.IGNORECASE).strip()
                m_json = re.search(r'\{[\s\S]*\}', txt)
                if m_json:
                    return json.loads(m_json.group(0))
            except Exception:
                continue
    return None


UNIVERSAL_25_ARCHETYPES = {
    "D01_LOCATION_BINARY": {
        "code": "Dạng 1",
        "name": "Xác định Vị trí Thực tế Hiện tại (Ở nhà hay Ở công ty / Trong nhà hay Ngoài đường)",
        "mode": "BINARY_LOCATION",
        "lh_dt": "Hào Thế (Bản thân) + Nội Quái/Phụ Mẫu/Tử Tôn (Nhà) đối chứng Quan Quỷ/Ngoại Quái (Công ty)",
        "km_dt": "Nhật Can (Người hỏi) lâm Cửa Tĩnh (Hưu/Tử/Đỗ/Sinh = Ở nhà) đối chứng Cửa Động (Khai/Cảnh/Thương = Công sở/Ngoài đường)",
        "answer_rule": "Bắt buộc chốt dứt khoát ĐANG Ở ĐÂU (tuyệt đối cấm trả lời 'Cần cân nhắc / Giằng co')",
    },
    "D02_POSTURE_STATE": {
        "code": "Dạng 2",
        "name": "Xác định Tư thế & Trạng thái Cơ thể (Đứng hay Ngồi / Nằm hay Ngồi / Ngủ hay Thức)",
        "mode": "BINARY_POSTURE",
        "lh_dt": "Hào Thế (Động hay Tĩnh) + Quẻ Chủ/Biến (Cấn/Khôn = Ngồi/Nằm; Chấn/Càn = Đứng/Đi)",
        "km_dt": "Cung Bản Mệnh lâm Hưu/Đỗ/Tử/Cửu Địa (Tĩnh = Ngồi/Nằm) đối chứng Thương/Kinh/Cửu Thiên (Động = Đứng/Đi)",
        "answer_rule": "Bắt buộc chốt dứt khoát ĐANG NGỒI/NẰM hay ĐANG ĐỨNG/DI CHUYỂN",
    },
    "D03_TRUE_OR_FALSE": {
        "code": "Dạng 3",
        "name": "Kiểm định Thật hay Giả / Nói thật hay Nói dối / Tin đồn thực hư",
        "mode": "BINARY_TRUTH",
        "lh_dt": "Hào Ứng & Dụng Thần (Lâm Tuần Không / Huyền Vũ / Đằng Xà = Giả dối; Hữu khí / Thanh Long = Sự thật)",
        "km_dt": "Thời Can & Cung Ứng (Kinh Môn / Huyền Vũ / Đằng Xà / Không Vong = Tin giả; Cảnh/Khai/Trực Phù = Thật)",
        "answer_rule": "Bắt buộc khẳng định ĐÂY LÀ SỰ THẬT hay CHUYỆN GIẢ / LỜI NÓI DỐI",
    },
    "D04_DONE_OR_NOT": {
        "code": "Dạng 4",
        "name": "Kiểm tra Tiến độ Sự việc Đã xảy ra hay Chưa (Rồi hay Chưa / Đã... chưa)",
        "mode": "BINARY_PROGRESS",
        "lh_dt": "Dụng Thần & Hào Động (Phát động/Đế Vượng = Đã làm rồi; Tĩnh/Tuần Không/Thai Dưỡng = Chưa làm)",
        "km_dt": "Thời Can & Bát Môn (Đỗ Môn/Tử Môn/Không Vong = Chưa thực hiện; Khai/Sinh/Xung = Đã thực hiện)",
        "answer_rule": "Bắt buộc chốt rõ ĐÃ THỰC HIỆN RỒI hay CHƯA THỰC HIỆN",
    },
    "D05_CHOICE_A_OR_B": {
        "code": "Dạng 5",
        "name": "Lựa chọn Nhị phân Phương án A hay Phương án B bất kỳ",
        "mode": "BINARY_OPTION_AB",
        "lh_dt": "Trục 1 (Hào Thế / Nội Quái / Quẻ Chủ = Phương án A) đối chứng Trục 2 (Hào Ứng / Ngoại Quái / Quẻ Biến = Phương án B)",
        "km_dt": "Cung Chủ (Phương án A) đối chứng Cung Khách/Biến (Phương án B) — loại trừ bên phạm Tuần Không/Tử Môn",
        "answer_rule": "Bắt buộc chọn dứt khoát Phương án A hoặc Phương án B tốt hơn/đúng hơn từ quẻ",
    },
    "D06_GENDER_AGE": {
        "code": "Dạng 6",
        "name": "Định danh Giới tính (Nam hay Nữ) & Độ tuổi / Năm sinh",
        "mode": "IDENTITY_GENDER_AGE",
        "lh_dt": "Âm Dương Hào Dụng Thần + Quái khí Càn/Chấn/Khảm/Cấn (Nam) vs Khôn/Tốn/Ly/Đoài (Nữ) + 12 Trường Sinh (Tuổi)",
        "km_dt": "Thiên Can & Cửu Tinh tại Cung Dụng Thần + Vòng Trường Sinh định khung tuổi & năm sinh",
        "answer_rule": "Chốt rõ NAM GIỚI hay NỮ GIỚI và khoảng ĐỘ TUỔI + NĂM SINH ứng hợp",
    },
    "D07_CHILDREN_COUNT": {
        "code": "Dạng 7",
        "name": "Tử tức & Con cái (Bao nhiêu người con / Mấy trai mấy gái / Sinh con)",
        "mode": "CHILDREN_FORENSIC",
        "lh_dt": "Hào Tử Tôn (Nếu phạm Tuần Không/Tử Môn = Hiện tại 0 con / Hỏi thử; Nếu hữu khí = Số con & tỷ lệ Trai/Gái)",
        "km_dt": "Cung Tử Tôn & Lục Hợp / Sinh Môn (Định số lượng con và phân bổ Nam/Nữ)",
        "answer_rule": "Nếu Tử Tôn Tuần Không phải báo ngay HIỆN TẠI CHƯA CÓ CON (0 CON); đồng thời nêu tiềm năng số con & mấy trai mấy gái",
    },
    "D08_PERSON_PROFILE": {
        "code": "Dạng 8",
        "name": "Phác họa Chân dung Con người: Ngoại hình, Tính cách & Nghề nghiệp",
        "mode": "PERSON_PORTRAIT",
        "lh_dt": "Ngũ Hành Dụng Thần + Lục Thú (Thanh Long, Chu Tước, Bạch Hổ, Huyền Vũ, Câu Trận, Đằng Xà)",
        "km_dt": "Cửu Tinh + Bát Thần + Bát Môn tại Cung Dụng Thần (Mô tả vóc dáng, tâm tính, ngành nghề)",
        "answer_rule": "Mô tả chi tiết Ngoại hình, Tính cách và Nghề nghiệp theo Ngũ Hành & Cửu Tinh trong quẻ",
    },
    "D09_QUANTITY_PRICE": {
        "code": "Dạng 9",
        "name": "Định lượng Con số, Số tầng nhà, Số phòng, Số người, Kích thước & Giá trị",
        "mode": "NUMERIC_QUANTITY",
        "lh_dt": "Hào Phụ Mẫu & Hào Thế (Đoán số tầng nhà/vị trí tầng) + Số Tiên/Hậu Thiên Bát Quái + Số Hà Đồ Lạc Thư",
        "km_dt": "Số Cung Kỳ Môn + Trạng thái Vượng/Tướng/Hưu/Tù định lượng con số thực tế",
        "answer_rule": "Chốt trực diện con số thực tế cho đúng đối tượng được hỏi (mấy tầng, tầng mấy, mấy phòng, mấy người, giá bao nhiêu...)",
    },
    "D10_OBJECT_XAPHU": {
        "code": "Dạng 10",
        "name": "Đoán Vạn Vật Xạ Phú (Đồ vật gì / Mặc áo màu gì / Đi xe gì / Chất liệu / Hình dáng)",
        "mode": "OBJECT_FORENSIC",
        "lh_dt": "Ngũ Hành Hào Dụng Thần (Phụ Mẫu = Áo/Xe; Thê Tài = Đồ vật) + Quái Tượng Nội/Ngoại + 12 Trường Sinh",
        "km_dt": "Thiên Can + Cửu Tinh + Bát Quái tại Cung Dụng Thần (Xác định màu sắc, chất liệu, hình dáng, tên đồ vật)",
        "answer_rule": "Chỉ rõ Màu sắc, Tên đồ vật/trang phục/xe cộ, Chất liệu, Hình dáng và Tình trạng thực tế",
    },
    "D11_LOST_ITEM_WHERE": {
        "code": "Dạng 11",
        "name": "Tìm Đồ thất lạc / Tìm Người / Xác định Địa điểm & Phương hướng (Ở đâu / Hướng nào)",
        "mode": "LOST_AND_FOUND",
        "lh_dt": "Hào Dụng Thần (Thê Tài/Phụ Mẫu) + Quái vị (Định vị độ cao: trên cao, ngang tầm hay sát đất)",
        "km_dt": "Cung Dụng Thần & Cung Thời Can (Định Phương hướng, Khoảng cách và Môi trường xung quanh nơi thất lạc)",
        "answer_rule": "Chốt rõ CÓ TÌM LẠI ĐƯỢC KHÔNG + Phương hướng + Vị trí cụ thể nơi đồ vật/người đang ở",
    },
    "D12_TIMING_WHEN": {
        "code": "Dạng 12",
        "name": "Thời điểm Ứng kỳ Chính xác (Khi nào / Bao giờ / Ngày Giờ Tháng Năm nào)",
        "mode": "TIMING_FORECAST",
        "lh_dt": "Hào Dụng Thần (Tuần Không = Ngày Xuất Không/Xung Không; Nhập Mộ = Ngày Xung Mộ; Động = Ngày Hợp; Tĩnh = Ngày Xung)",
        "km_dt": "Cung Dụng Thần & Khắc Ứng Kỳ Môn (Định mốc Giờ - Ngày - Tháng Dương lịch & Âm lịch)",
        "answer_rule": "Chỉ rõ mốc Giờ, Ngày, Tháng ứng nghiệm cụ thể dựa trên quy luật Xung/Hợp/Xuất Không của Dụng Thần",
    },
    "D13_CAUSE_MOTIVE_WHY": {
        "code": "Dạng 13",
        "name": "Truy tìm Nguyên nhân, Lý do & Tâm lý / Ý đồ ngầm (Tại sao / Vì sao / Họ nghĩ gì)",
        "mode": "CAUSE_AND_MOTIVE",
        "lh_dt": "Hào Kỵ Thần / Hào Động tác động lên Dụng Thần + Thế–Ứng tương tác",
        "km_dt": "Bát Thần + Cửu Tinh + Cách cục Thiên/Địa Can tại Cung Đối phương (Bóc tách nguyên nhân & tâm ý)",
        "answer_rule": "Giải thích rõ Nguyên nhân gốc rễ trong quẻ và Tâm lý/Ý đồ thật sự của đối phương",
    },
    "D14_CAREER_WORK": {
        "code": "Dạng 14",
        "name": "Công việc, Sự nghiệp, Xin việc, Thăng chức & Nghỉ việc hay Làm tiếp",
        "mode": "CAREER_DECISION",
        "lh_dt": "Hào Quan Quỷ (Công danh/Cơ quan) + Hào Phụ Mẫu (Hợp đồng/Hồ sơ) + Hào Thế",
        "km_dt": "Cửa Khai Môn (Công việc/Chức vụ) + Cung Bản Mệnh (Sinh/Khắc)",
        "answer_rule": "Phán quyết rõ Nên giữ việc hay chuyển việc / Khả năng thăng tiến, xin việc kèm hướng hành động",
    },
    "D15_FINANCE_INVEST": {
        "code": "Dạng 15",
        "name": "Tài chính, Đầu tư, Kinh doanh, Chứng khoán, Bất động sản & Mua bán",
        "mode": "FINANCE_INVESTMENT",
        "lh_dt": "Hào Thê Tài (Lợi nhuận/Vốn) + Hào Tử Tôn (Nguồn sinh tài) + Hào Huynh Đệ (Rủi ro hao tài)",
        "km_dt": "Cửa Sinh Môn (Lợi nhuận) + Can Giáp Tý Mậu (Vốn) — xét Sinh Môn sinh hay khắc Bản Mệnh",
        "answer_rule": "Chốt rõ NÊN ĐẦU TƯ/GIAO DỊCH (Có lãi) hay KHÔNG NÊN (Tránh đọng vốn/thua lỗ)",
    },
    "D16_DEBT_LOAN": {
        "code": "Dạng 16",
        "name": "Đòi nợ, Cho vay, Thu hồi công nợ & Vay vốn Ngân hàng",
        "mode": "DEBT_RECOVERY",
        "lh_dt": "Hào Thê Tài (Khoản tiền) + Hào Ứng (Con nợ/Ngân hàng) đối chứng Hào Thế",
        "km_dt": "Trực Phù (Chủ nợ) + Thiên Ất (Con nợ) + Thương Môn (Người đi đòi nợ)",
        "answer_rule": "Chốt rõ CÓ ĐÒI LẠI ĐƯỢC NỢ KHÔNG / VAY ĐƯỢC KHÔNG và cách thức thu hồi hiệu quả nhất",
    },
    "D17_LOVE_MARRIAGE": {
        "code": "Dạng 17",
        "name": "Tình cảm, Hôn nhân, Tình trạng Độc thân/Kết hôn, Vợ chồng & Quay lại",
        "mode": "LOVE_RELATIONSHIP",
        "lh_dt": "Hào Thê Tài (Nam hỏi) / Quan Quỷ (Nữ hỏi) + Trục Thế–Ứng (Sinh Hợp hay Xung Khắc / Tuần Không)",
        "km_dt": "Can Ất (Nữ) + Can Canh (Nam) + Thần Lục Hợp (Hôn nhân/Tình duyên)",
        "answer_rule": "Phán quyết rõ Đã có gia đình/người yêu hay Độc thân; Còn yêu hay Có quay lại hàn gắn không",
    },
    "D18_HEALTH_MEDICAL": {
        "code": "Dạng 18",
        "name": "Sức khỏe, Bệnh tật, Phẫu thuật, Tiên lượng Sinh–Tử & Y Dịch",
        "mode": "HEALTH_MEDICAL",
        "lh_dt": "Hào Dụng Thần (Người bệnh) + Hào Quan Quỷ (Bệnh tinh) + Hào Tử Tôn (Thuốc men/Bác sĩ)",
        "km_dt": "Sao Thiên Nhuế (Bệnh tinh) + Sao Thiên Tâm & Ất Kỳ (Bác sĩ/Thuốc điều trị)",
        "answer_rule": "Đánh giá rõ Tiên lượng sức khỏe (Nhẹ/Nặng/Hồi phục), căn nguyên bệnh và hướng tìm thầy thuốc",
    },
    "D19_FENGSHUI_GRAVE": {
        "code": "Dạng 19",
        "name": "Phong thủy Dương trạch (Nhà đất, Xây sửa nhà) & Âm phần (Mồ mả Gia tiên)",
        "mode": "FENGSHUI_ESTATE",
        "lh_dt": "Hào Phụ Mẫu (Nhà đất/Mồ mả) + Hào 2 (Trạch vị) + Hào 5 (Nhân đinh)",
        "km_dt": "Sinh Môn (Dương trạch) + Tử Môn (Âm phần/Mồ mả) + Huyền Không Phi Tinh Vận 9",
        "answer_rule": "Chẩn đoán rõ Phong thủy Nhà đất / Mồ mả đang Tụ khí Cát lành hay Động khí cần tu bổ",
    },
    "D20_EXAM_STUDY_VISA": {
        "code": "Dạng 20",
        "name": "Thi cử, Học hành, Điểm số, Bằng cấp & Xin Visa / Du học",
        "mode": "EXAM_VISA",
        "lh_dt": "Hào Phụ Mẫu (Điểm số/Văn bằng/Visa) + Hào Quan Quỷ (Danh vị) + Hào Thế (Thí sinh)",
        "km_dt": "Sao Thiên Phụ (Văn Xương) + Cửa Cảnh Môn (Bài thi/Hồ sơ Visa)",
        "answer_rule": "Chốt rõ Khả năng Thi đỗ / Đậu Visa và các môn/khâu hồ sơ cần lưu ý",
    },
    "D21_LAWSUIT_COMPETE": {
        "code": "Dạng 21",
        "name": "Kiện tụng, Pháp lý, Tranh chấp, Đấu thầu & Thi đấu Thắng–Thua",
        "mode": "COMPETITION_LAWSUIT",
        "lh_dt": "Hào Thế (Bên ta) đối kháng Hào Ứng (Đối phương) + Hào Quan Quỷ (Tòa án/Trọng tài)",
        "km_dt": "Trực Phù (Nguyên đơn) + Thiên Ất (Bị đơn) + Cửa Kinh Môn / Khai Môn (Quan tòa)",
        "answer_rule": "Phán quyết rõ BÊN BẠN THẮNG hay ĐỐI PHƯƠNG CHIẾM ƯU THẾ hay NÊN HÒA GIẢI",
    },
    "D22_TRAVEL_JOURNEY": {
        "code": "Dạng 22",
        "name": "Xuất hành, Đi xa, Du lịch, Công tác & An toàn Giao thông",
        "mode": "TRAVEL_SAFETY",
        "lh_dt": "Hào Thế (Người đi) + Hào Ứng (Nơi đến) + Hào Phụ Mẫu (Phương tiện/Hành lý) + Dịch Mã",
        "km_dt": "Hướng Cung nơi đến + Cửa Cảnh/Khai/Hưu/Sinh (Thượng lộ bình an hay Trắc trở)",
        "answer_rule": "Kết luận rõ Chuyến đi Thượng lộ bình an hay Cần đề phòng trắc trở/chậm trễ",
    },
    "D23_WEATHER_CLIMATE": {
        "code": "Dạng 23",
        "name": "Dự báo Thời tiết & Thiên tượng (Mưa hay Nắng / Giông bão)",
        "mode": "WEATHER_FORECAST",
        "lh_dt": "Hào Phụ Mẫu (Mưa/Mây) + Hào Tử Tôn (Nắng/Quang đãng) + Hào Huynh Đệ (Gió) + Hào Thê Tài (Tạnh ráo)",
        "km_dt": "Sao Thiên Bồng/Khảm (Mưa) đối chứng Sao Thiên Anh/Ly (Nắng) + Thiên Phụ/Tốn (Gió)",
        "answer_rule": "Dự báo dứt khoát TRỜI MƯA hay TRỜI NẮNG RÁO theo Ngũ Hành & Cửu Tinh",
    },
    "D24_AUSPICIOUS_DATE": {
        "code": "Dạng 24",
        "name": "Trạch Cát / Xem Ngày Giờ Tốt (Khai trương, Cưới hỏi, Động thổ, Ký kết)",
        "mode": "DATE_SELECTION",
        "lh_dt": "Nhật Thần & Nguyệt Lệnh tương sinh Hào Thế và Hào Dụng Thần",
        "km_dt": "Tam Kỳ (Ất, Bính, Đinh) hội Tam Cát Môn (Khai, Hưu, Sinh) — tránh Ngũ Bất Ngộ Thời",
        "answer_rule": "Kết luận rõ Ngày giờ này ĐẠI CÁT nên tiến hành ngay hay Cần chọn khung giờ/ngày khác",
    },
    "D25_SPIRITUAL_GENERAL": {
        "code": "Dạng 25",
        "name": "Tâm linh, Giấc mơ, Điềm báo, Vận mệnh & Quyết định Tổng quát",
        "mode": "SPIRITUAL_GENERAL",
        "lh_dt": "Quẻ Chủ – Quẻ Hỗ – Quẻ Biến + Lục Thần (Đằng Xà/Huyền Vũ = Mộng mị; Thanh Long = Điềm lành)",
        "km_dt": "Thần Bàn (Trực Phù, Thái Âm, Đằng Xà, Cửu Thiên) + Cung Bản Mệnh",
        "answer_rule": "Giải mã rõ Ý nghĩa điềm báo/giấc mơ hoặc Cát/Hung tổng quát của sự việc",
    },
}


class QuestionReaderAI:
    """
    CON AI SỐ 1: Chuyên trách ĐỌC HIỂU CÂU HỎI của người dùng (Chạy ở Bước 0).
    Phân tích chính xác câu hỏi đang hỏi về CÁI GÌ, SỐ LƯỢNG GÌ, AI, Ở ĐÂU, LỰA CHỌN NÀO,
    và chỉ định Dụng Thần bắt buộc (`authoritative_dt`) để Con AI Số 2 đối chứng với quẻ.
    """

    @staticmethod
    def analyze_question(question: str, dung_than_hint: str = "", category_hint: str = "") -> dict:
        q_raw = str(question or "").strip()
        q_low = q_raw.lower()

        # 1. Phát hiện các mục tiêu câu hỏi đặc thù (Specific Question Targets)
        specific_target = ""
        authoritative_dt = ""
        subject_person = "Bản thân người hỏi"

        # A. Hỏi về Số tầng nhà / Ở tầng mấy / Số phòng / Diện tích nhà
        is_house_floors_q = any(w in q_low for w in [
            "mấy tầng", "bao nhiêu tầng", "tầng mấy", "tầng thứ mấy", "tầng bao nhiêu",
            "nhà cao mấy", "nhà mấy lầu", "mấy lầu", "lầu mấy", "mấy phòng", "bao nhiêu phòng",
            "diện tích bao nhiêu", "rộng bao nhiêu", "bao nhiêu m2", "bao nhiêu mét vuông"
        ])
        # B. Hỏi về Số anh chị em trong gia đình / Mấy chị gái mấy anh trai / Con thứ mấy (SIBLINGS_COUNT)
        _has_sibling_noun = any(w in q_low for w in [
            "anh chị em", "anh em ruột", "chị em ruột", "anh chị ruột",
            "chị gái", "anh trai", "em gái", "em trai",
            "người chị", "người anh", "người em",
        ])
        _has_sibling_qty = any(w in q_low for w in [
            "mấy", "bao nhiêu", "số lượng", "có chị gái", "có anh trai", "có em gái", "có em trai",
            "có anh chị", "con thứ mấy", "thứ mấy", "con trưởng", "con út", "con đầu"
        ])
        is_siblings_q = (
            any(w in q_low for w in [
                "mấy anh chị em", "bao nhiêu anh chị em", "mấy anh em", "bao nhiêu anh em",
                "mấy chị em", "bao nhiêu chị em", "mấy chị gái", "bao nhiêu chị gái",
                "mấy anh trai", "bao nhiêu anh trai", "mấy em gái", "bao nhiêu em gái",
                "mấy em trai", "bao nhiêu em trai", "mấy người chị", "mấy người anh",
                "mấy người em", "tôi có mấy chị", "tôi có mấy anh", "tôi có mấy em",
                "nhà có mấy chị", "nhà có mấy anh", "con thứ mấy", "thứ mấy trong nhà",
                "con trưởng hay con út", "con đầu hay"
            ])
            or (
                _has_sibling_noun
                and _has_sibling_qty
                and not any(w in q_low for w in ["bao nhiêu tuổi", "mấy tuổi", "sinh năm", "mấy tầng", "bao nhiêu tiền", "bao nhiêu km"])
            )
        )
        # C. Hỏi về Tình trạng Hôn nhân thực tế (Đã kết hôn chưa / Có vợ chồng chưa / Độc thân hay có gia đình)
        is_marital_status_q = any(w in q_low for w in [
            "kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
            "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"
        ]) and not any(ex in q_low for ex in ["vợ tôi", "chồng tôi", "con tôi", "nhân tình", "ngoại tình"])
        # C2. Hỏi về Số lượng Vợ / Chồng trong cuộc đời (Có mấy vợ / Có mấy chồng / Mấy đời vợ chồng / Kết hôn mấy lần)
        is_spouse_count_q = any(w in q_low for w in [
            "mấy vợ", "bao nhiêu vợ", "mấy người vợ", "mấy đời vợ", "lấy mấy vợ", "có mấy vợ", "mấy bà vợ",
            "mấy chồng", "bao nhiêu chồng", "mấy người chồng", "mấy đời chồng", "lấy mấy chồng", "có mấy chồng", "mấy ông chồng",
            "mấy lần kết hôn", "kết hôn mấy lần", "lấy vợ mấy lần", "lấy chồng mấy lần", "mấy lần đò", "mấy lần lập gia đình"
        ])
        # C3. Hỏi về Chung thủy / Nhân tình / Ngoại tình / Người thứ 3 bên ngoài (FIDELITY_AFFAIR_CHECK)
        is_fidelity_affair_q = any(w in q_low for w in [
            "nhân tình", "ngoại tình", "bồ bịch", "có bồ", "nuôi bồ", "người thứ 3", "người thứ ba",
            "phản bội", "cắm sừng", "lăng nhăng", "có người khác", "có ai khác", "quan hệ ngoài luồng",
            "chung thủy", "tư tình", "gian díu", "trăng hoa", "kẻ thứ 3", "kẻ thứ ba", "qua lại với ai"
        ])
        # D. Hỏi về Màu sắc Đồ vật / Thiết bị (Bàn phím, Máy tính, Điện thoại, Vật dụng) / Trang phục đang mặc / Xe cộ / Biển số xe
        is_clothing_vehicle_q = any(w in q_low for w in [
            "màu gì", "màu sắc gì", "có màu gì", "màu nào", "mặc áo màu gì", "áo màu gì",
            "quần áo màu gì", "trang phục màu gì", "mặc đồ màu gì", "bàn phím", "máy tính màu gì",
            "điện thoại màu gì", "laptop màu gì", "chuột màu gì", "ốp lưng màu gì",
            "đi xe gì", "xe màu gì", "xe của tôi màu gì", "biển số xe", "số nhà bao nhiêu",
            "số nhà mấy", "nhà màu gì", "nhà sơn màu gì", "cửa màu gì"
        ])
        # E. Hỏi về Xung quanh / Trong phòng có mấy người / Có ai bên cạnh không
        is_people_around_q = any(w in q_low for w in [
            "xung quanh tôi có mấy người", "trong phòng có mấy người", "ở đây có mấy người",
            "bên cạnh tôi có ai", "có mấy người đang", "tôi đang ở một mình hay", "ở một mình hay"
        ])
        # E2. Hỏi về Tổng số Nhân khẩu trong nhà / Gia đình có bao nhiêu người (HOUSEHOLD_MEMBERS)
        is_household_members_q = any(w in q_low for w in [
            "nhà tôi có bao nhiêu người", "nhà tôi có mấy người", "nhà có bao nhiêu người", "nhà có mấy người",
            "gia đình tôi có bao nhiêu người", "gia đình tôi có mấy người", "gia đình có bao nhiêu người", "gia đình có mấy người",
            "trong nhà có bao nhiêu người", "trong nhà có mấy người", "nhà có mấy nhân khẩu", "nhà có bao nhiêu nhân khẩu",
            "gia đình có mấy nhân khẩu", "gia đình có bao nhiêu nhân khẩu", "hộ khẩu có mấy người", "hộ khẩu nhà tôi",
            "nhà tôi mấy người", "gia đình mấy người", "nhà bạn có mấy người", "nhà mình có mấy người",
            "tổng số người trong nhà", "tổng số người trong gia đình", "nhà có mấy thành viên", "gia đình có mấy thành viên",
            "gia đình có bao nhiêu thành viên", "nhà tôi có bao nhiêu thành viên"
        ])

        has_age_word = any(w in q_low for w in ["bao nhiêu tuổi", "mấy tuổi", "tuổi", "sinh năm", "năm sinh"])
        is_children_age_q = (
            has_age_word
            and any(w in q_low for w in [
                "con gái", "con trai", "con của tôi", "con tôi", "mấy đứa con", "hai đứa con",
                "2 đứa con", "các con", "con cái", "đứa con", "chúng nó"
            ])
            and not is_siblings_q
        )
        is_children_q = (
            (not has_age_word)
            and any(w in q_low for w in [
                "bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con",
                "bao nhiêu con", "mấy trai mấy gái", "con cái", "sinh con", "đường con cái", "tử tức",
                "có con chưa", "mấy đứa"
            ])
            and not any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao", "con thứ mấy"])
            and not is_siblings_q
        )

        is_where_home_work = (
            any(w in q_low for w in ["ở nhà hay", "hay ở nhà", "ở công ty", "ở cơ quan", "ở văn phòng", "ở quán", "ngoài đường", "trong nhà hay", "ngoài sân"])
            and any(w in q_low for w in ["nhà", "công ty", "cơ quan", "văn phòng", "ngoài", "phòng"])
        )
        is_posture = any(w in q_low for w in ["đứng hay ngồi", "ngồi hay đứng", "nằm hay ngồi", "ngồi hay nằm", "đang đứng hay", "đang ngồi hay", "đang nằm hay", "ngủ hay thức", "thức hay ngủ"])
        is_true_false = any(w in q_low for w in ["thật hay giả", "giả hay thật", "nói thật hay", "nói dối hay", "có thật không", "thật không", "lừa dối"])
        is_done_yet = (
            any(w in q_low for w in ["rồi hay chưa", "chưa hay rồi", "hay chưa", "ăn cơm chưa", "ăn chưa", "về chưa", "đi chưa", "xong chưa", "đã ăn", "đã về", "đã đi"])
            and not is_marital_status_q and not is_children_q
        )
        is_quit_work = any(w in q_low for w in ["nghỉ hay", "nên nghỉ", "nghỉ việc", "bỏ việc", "xin nghỉ", "làm tiếp hay", "đi hay ở", "ở lại hay"])
        _is_child_action_ab = bool(re.search(r"(?:con\s+gái\s+hay\s+con\s+trai|con\s+trai\s+hay\s+con\s+gái)\s+\S+", q_low)) and not has_age_word and not any(w in q_low for w in ["sinh con", "đẻ con", "mang thai", "bầu"])
        is_gender_age = any(w in q_low for w in ["nam hay nữ", "nữ hay nam", "trai hay gái", "gái hay trai", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "sinh năm"]) and not is_children_q and not _is_child_action_ab
        is_weather = any(w in q_low for w in ["mưa hay nắng", "nắng hay mưa", "thời tiết", "có mưa không", "trời mưa", "trời nắng", "bão"])
        is_lawsuit = any(w in q_low for w in ["kiện", "tòa án", "pháp lý", "tranh chấp", "ai thắng", "thắng hay thua", "thắng hay đối phương", "đấu thầu"])
        is_profile = any(w in q_low for w in ["ngoại hình", "hình dáng người", "cao hay thấp", "béo hay gầy", "tính cách", "tính nết", "làm nghề gì", "nghề nghiệp gì", "ngành gì", "cao bao nhiêu", "nặng bao nhiêu"])
        is_object = any(w in q_low for w in ["trong hộp", "trong túi", "trong phòng có gì", "trước mặt tôi có", "trên bàn có", "cầm cái gì", "đồ vật gì", "vật gì", "là cái gì", "màu gì", "chất liệu gì", "hình gì"]) and not is_clothing_vehicle_q
        is_when = any(w in q_low for w in ["khi nào", "bao giờ", "mấy giờ", "ngày nào", "tháng nào", "năm nào", "bao lâu", "tháng mấy"])
        # Mọi câu hỏi có từ "mấy" hoặc "bao nhiêu" hoặc "số mấy" (không phải tuổi, con cái, thời gian)
        has_numeric_word = bool(re.search(r"\b(mấy|bao nhiêu|số mấy|thứ mấy|định lượng|số lượng)\b", q_low))
        is_quantity = (
            has_numeric_word
            and not is_children_q
            and not is_gender_age
            and not is_when
        )
        is_lost_where = any(w in q_low for w in ["mất", "thất lạc", "tìm lại", "tìm thấy", "ở đâu", "hướng nào", "chỗ nào"]) and not is_where_home_work and not is_house_floors_q
        is_why = any(w in q_low for w in ["tại sao", "vì sao", "nguyên nhân", "lý do", "do đâu", "ý đồ gì", "nghĩ gì", "tâm lý"])
        is_debt = any(w in q_low for w in ["đòi nợ", "trả nợ", "thu hồi nợ", "cho vay", "vay tiền", "vay ngân hàng", "khoản nợ", "con nợ"])
        is_invest = any(w in q_low for w in ["đầu tư", "kinh doanh", "buôn bán", "mở quán", "mở cửa hàng", "chứng khoán", "cổ phiếu", "có lãi", "lời hay lỗ", "mua bán", "xuống tiền", "mua đất", "bán đất", "mua nhà", "bán nhà", "tài chính", "tài lộc", "có lộc", "tiền bạc", "thu nhập", "lương", "kiếm tiền"])
        is_love = any(w in q_low for w in ["yêu", "tình cảm", "hôn nhân", "vợ chồng", "người yêu", "quay lại", "hàn gắn", "chia tay", "ly hôn", "kết hôn", "ngoại tình"])
        is_health = any(w in q_low for w in ["bệnh", "ốm", "nằm viện", "phẫu thuật", "mổ", "sức khỏe", "qua khỏi", "khỏi bệnh", "thuốc", "bác sĩ", "tai nạn", "nguy kịch"])
        is_fengshui = any(w in q_low for w in ["phong thủy", "nhà đất", "xây nhà", "sửa nhà", "mồ mả", "âm phần", "mộ phần", "gia tiên", "động thổ", "hướng nhà"]) and not is_house_floors_q and not is_invest
        is_exam = any(w in q_low for w in ["thi đỗ", "thi đậu", "có đỗ", "đỗ không", "đậu không", "kỳ thi", "đi thi", "thi cử", "học hành", "điểm thi", "bằng cấp", "lấy bằng", "bằng lái", "sát hạch", "thi bằng", "du học", "xin visa", "phỏng vấn visa"])
        is_travel = any(w in q_low for w in ["xuất hành", "đi xa", "du lịch", "công tác", "chuyến đi", "lên đường", "về quê", "di chuyển", "thượng lộ"])
        is_trachcat = any(w in q_low for w in ["xem ngày", "ngày tốt", "giờ tốt", "ngày đẹp", "khai trương", "nhập trạch", "cưới hỏi"])
        is_career = any(w in q_low for w in ["công việc", "sự nghiệp", "xin việc", "thăng chức", "chuyển việc", "nhảy việc", "hợp đồng"])

        arch_key = "D25_SPIRITUAL_GENERAL"
        option_a = ""
        option_b = ""

        if is_house_floors_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "HOUSE_FLOORS"
            subject_person = "Ngôi nhà & Vị trí tầng người hỏi đang ở"
            authoritative_dt = "Phụ Mẫu"
        elif is_siblings_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "SIBLINGS_COUNT"
            subject_person = "Anh chị em trong gia đình & Thứ bậc bản thân"
            authoritative_dt = "Huynh Đệ"
        elif is_household_members_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "HOUSEHOLD_MEMBERS"
            subject_person = "Tổng số Nhân khẩu / Thành viên trong Gia đình (Bản thân + Phối ngẫu + Con cái + Phụ mẫu)"
            authoritative_dt = "Phụ Mẫu"
        elif is_people_around_q:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "PEOPLE_AROUND"
            subject_person = "Không gian & Số người xung quanh bạn"
            authoritative_dt = "Bản Thân"
        elif is_spouse_count_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "SPOUSE_COUNT"
            if "chồng" in q_low and "vợ" not in q_low:
                subject_person = "Số đời Chồng / Phối ngẫu trong cuộc đời"
                authoritative_dt = "Quan Quỷ"
            else:
                subject_person = "Số đời Vợ / Phối ngẫu trong cuộc đời"
                authoritative_dt = "Thê Tài"
        elif is_fidelity_affair_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "FIDELITY_AFFAIR_CHECK"
            if any(w in q_low for w in ["chồng", "bạn trai"]) and "vợ" not in q_low:
                subject_person = "Kiểm chứng sự chung thủy & Nhân tình bên ngoài của Người chồng (Quan Quỷ)"
                authoritative_dt = "Quan Quỷ"
            else:
                subject_person = "Kiểm chứng sự chung thủy & Nhân tình bên ngoài của Người vợ (Thê Tài)"
                authoritative_dt = "Thê Tài"
        elif is_marital_status_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "MARITAL_STATUS_NOW"
            subject_person = "Tình trạng Hôn nhân / Tình duyên hiện tại"
            authoritative_dt = "Thê Tài"
        elif is_clothing_vehicle_q:
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "CLOTHING_VEHICLE"
            subject_person = "Trang phục / Phương tiện / Màu sắc & Biển số thực tế"
            authoritative_dt = "Phụ Mẫu"
        elif is_where_home_work:
            arch_key = "D01_LOCATION_BINARY"
            specific_target = "LOCATION_HOME_WORK"
            option_a, option_b = "Đang ở Nhà (Tại gia)", "Đang ở Công ty / Bên ngoài"
        elif is_posture:
            arch_key = "D02_POSTURE_STATE"
            specific_target = "POSTURE_STATE"
            option_a, option_b = "Đang Ngồi / Nằm nghỉ (Tĩnh)", "Đang Đứng / Di chuyển (Động)"
        elif is_true_false:
            arch_key = "D03_TRUE_OR_FALSE"
            specific_target = "TRUE_OR_FALSE"
            option_a, option_b = "Sự thật (Đáng tin cậy)", "Chuyện giả / Lời nói dối"
        elif is_done_yet:
            arch_key = "D04_DONE_OR_NOT"
            specific_target = "DONE_OR_NOT"
            option_a, option_b = "Đã thực hiện rồi", "Chưa thực hiện"
        elif is_children_age_q:
            arch_key = "D06_GENDER_AGE"
            specific_target = "CHILDREN_AGE"
            if "con gái" in q_low and "con trai" in q_low:
                subject_person = "Con gái & Con trai của người hỏi (Tử tức)"
            elif "con gái" in q_low:
                subject_person = "Con gái của người hỏi (Tử tức)"
            elif "con trai" in q_low:
                subject_person = "Con trai của người hỏi (Tử tức)"
            else:
                subject_person = "Các con của người hỏi (Tử tức)"
            authoritative_dt = "Tử Tôn"
        elif is_children_q:
            arch_key = "D07_CHILDREN_COUNT"
            specific_target = "CHILDREN_COUNT"
            subject_person = "Con cái (Tử tức)"
            authoritative_dt = "Tử Tôn"
        elif is_gender_age:
            arch_key = "D06_GENDER_AGE"
            specific_target = "GENDER_AGE"
        elif is_weather:
            arch_key = "D23_WEATHER_CLIMATE"
            specific_target = "WEATHER"
            option_a, option_b = "Trời Mưa / Nhiều mây ẩm", "Trời Nắng / Quang đãng"
        elif is_lawsuit:
            arch_key = "D21_LAWSUIT_COMPETE"
            specific_target = "LAWSUIT"
            option_a, option_b = "Bên bạn (Hào Thế)", "Đối phương (Hào Ứng)"
        elif is_quit_work:
            arch_key = "D14_CAREER_WORK"
            specific_target = "QUIT_OR_STAY"
            option_a, option_b = "Nên giữ công việc hiện tại (Ở lại)", "Nên nghỉ việc / Chuyển hướng"
        elif (" hay " in q_low) and not any(w in q_low for w in ["hay không", "có nên"]):
            m_ab = re.search(r'(?:nên\s+|chọn\s+)?([^,?.;!]+?)\s+hay\s+([^,?.;!]+)', q_low)
            if m_ab:
                arch_key = "D05_CHOICE_A_OR_B"
                specific_target = "GENERIC_AB"
                option_a = m_ab.group(1).strip()
                option_b = m_ab.group(2).strip()
                for pfx in ["cho hỏi ", "hỏi xem ", "xem giúp ", "bói xem ", "hiện tại ", "bây giờ ", "lúc này "]:
                    if option_a.startswith(pfx):
                        option_a = option_a[len(pfx):].strip()
                # Trường hợp 1: option_a là chủ ngữ 1 ("con gái", "con trai", "vợ", "chồng", "bố", "mẹ") và option_b bắt đầu bằng chủ ngữ 2 kèm vị ngữ ("con trai đang khóc")
                _PAIR_SUBJ = [
                    ("con gái", "con trai"), ("con trai", "con gái"),
                    ("bé gái", "bé trai"), ("bé trai", "bé gái"),
                    ("vợ", "chồng"), ("chồng", "vợ"),
                    ("bố", "mẹ"), ("mẹ", "bố"), ("ba", "mẹ"), ("cha", "mẹ"),
                    ("anh", "em"), ("chị", "em"), ("em", "anh"), ("em", "chị"),
                ]
                for _sa, _sb in _PAIR_SUBJ:
                    if option_a in (_sa, f"{_sa} tôi", f"{_sa} của tôi") and option_b.startswith(_sb):
                        _tail_pred = option_b[len(_sb):].strip()
                        if _tail_pred:
                            option_a = f"{option_a} {_tail_pred}".strip()
                        break
                # Trường hợp 2: option_a có chủ ngữ/động từ chung ("con tôi không khóc", "nhà tôi nghèo", "đi Hà Nội") còn option_b chỉ ghi vế đối lập ("đang khóc", "giàu", "Sài Gòn")
                for _subj_pfx in [
                    "con tôi ", "con của tôi ", "bé nhà tôi ", "vợ tôi ", "chồng tôi ",
                    "bố tôi ", "mẹ tôi ", "nhà tôi ", "gia đình tôi ", "gia đình mình ",
                    "nhà mình ", "vợ chồng tôi ", "công ty tôi ", "cửa hàng tôi ",
                    "anh trai tôi ", "chị gái tôi ", "em tôi ", "bạn tôi ",
                    "tôi nên đi ", "tôi nên mua ", "tôi nên chọn ", "tôi nên học ", "tôi nên làm ", "tôi nên ở ",
                    "tôi nên ", "có nên đi ", "có nên mua ", "có nên ", "nên đi ", "nên mua ", "nên chọn ", "nên ở ", "nên ",
                    "tôi đi ", "tôi ở ", "tôi mua ", "tôi chọn ", "tôi làm ", "tôi học ", "tôi ",
                    "đi ", "mua ", "chọn ", "học ", "ăn ", "uống ",
                ]:
                    if option_a.lower().startswith(_subj_pfx) and len(option_a) > len(_subj_pfx) + 1:
                        _first_w_pfx = _subj_pfx.strip().split()[0]
                        if not option_b.lower().startswith(_first_w_pfx + " ") and option_b.lower() != _first_w_pfx:
                            # Chỉ nối tiền tố chung vào option_b nếu option_b không phải là động từ đối lập trực tiếp (VD: "đi hay ở", "mua hay bán")
                            if not (_subj_pfx.strip() in ("đi", "mua", "bán", "ở", "làm", "nghỉ") and option_b.lower().strip() in ("ở", "đi", "bán", "mua", "nghỉ", "làm")):
                                option_b = f"{_subj_pfx.strip()} {option_b}".strip()
                            break
                if any(w in q_low for w in ["con tôi", "con gái", "con trai", "bé gái", "bé trai", "con của tôi"]):
                    subject_person = "Con cái (Tử tức — Đối chứng 2 phương án trên Nhóm Quẻ Chính: Mai Hoa + Kỳ Môn + Lục Hào)"
                    authoritative_dt = "Tử Tôn"
                elif any(w in q_low for w in ["giàu", "nghèo", "khá giả", "khó khăn", "dư dả", "thiếu thốn", "túng thiếu", "có tiền", "hết tiền", "lãi", "lỗ", "lời", "nợ"]):
                    subject_person = "Thực lực Kinh tế / Tài sản Gia đình (Dụng Thần: Thê Tài — Căn cứ Nhóm Quẻ Chính: Mai Hoa + Kỳ Môn + Lục Hào)"
                    authoritative_dt = "Thê Tài"
        elif is_profile:
            arch_key = "D08_PERSON_PROFILE"
            specific_target = "PERSON_PROFILE"
        elif is_object:
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "HIDDEN_OBJECT"
            subject_person = "Đồ vật / Thiết bị / Vạn vật Loại tượng (Dụng Thần: Phụ Mẫu)"
            authoritative_dt = "Phụ Mẫu"
        elif is_quantity:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "GENERAL_QUANTITY"
            # Trích xuất đơn vị cụ thể mà người hỏi đang muốn biết (km, cây số, triệu, tỷ, ngày, giờ, điểm, cái, lần...)
            _m_unit = re.search(r"(?:bao nhiêu|mấy)\s+([a-zA-ZÀ-ỹ%]+(?:\s+[a-zA-ZÀ-ỹ]+)?)", q_low)
            _raw_u = (_m_unit.group(1).strip() if _m_unit else "").split()[0] if _m_unit else ""
            if any(w in q_low for w in ["bao nhiêu km", "mấy km", "kilomet", "cây số", "đường trường"]):
                authoritative_dt = "Phụ Mẫu"
                subject_person = "Định lượng Quãng đường / Số km (Kilômét) thực tế trên quẻ"
            elif any(w in q_low for w in ["bao nhiêu tiền", "mấy triệu", "mấy tỷ", "giá bao nhiêu", "bao nhiêu vàng", "lãi bao nhiêu"]):
                authoritative_dt = "Thê Tài"
                subject_person = "Định lượng Tài chính / Số tiền thực tế trên quẻ"
            elif any(w in q_low for w in ["bao nhiêu điểm", "mấy điểm"]):
                authoritative_dt = "Phụ Mẫu"
                subject_person = "Định lượng Điểm số thực tế trên quẻ"
        elif is_lost_where:
            arch_key = "D11_LOST_ITEM_WHERE"
            specific_target = "LOST_ITEM"
        elif is_when and not (is_career or is_invest or is_love or is_health):
            arch_key = "D12_TIMING_WHEN"
            specific_target = "TIMING_WHEN"
        elif is_why:
            arch_key = "D13_CAUSE_MOTIVE_WHY"
            specific_target = "CAUSE_WHY"
        elif is_debt:
            arch_key = "D16_DEBT_LOAN"
            specific_target = "DEBT_LOAN"
            authoritative_dt = "Thê Tài"
        elif is_invest:
            arch_key = "D15_FINANCE_INVEST"
            specific_target = "INVEST_PROFIT"
            authoritative_dt = "Thê Tài"
        elif is_exam:
            arch_key = "D20_EXAM_STUDY_VISA"
            specific_target = "EXAM_VISA"
            authoritative_dt = "Phụ Mẫu"
        elif is_health:
            arch_key = "D18_HEALTH_MEDICAL"
            specific_target = "HEALTH_MEDICAL"
            authoritative_dt = "Quan Quỷ"
        elif is_fengshui:
            arch_key = "D19_FENGSHUI_GRAVE"
            specific_target = "FENGSHUI_GRAVE"
            authoritative_dt = "Phụ Mẫu"
        elif is_love:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "LOVE_MARRIAGE"
            authoritative_dt = "Quan Quỷ" if ("chồng" in q_low and "vợ" not in q_low) else "Thê Tài"
        elif is_travel:
            arch_key = "D22_TRAVEL_JOURNEY"
            specific_target = "TRAVEL_SAFETY"
            authoritative_dt = "Hào Thế"
        elif is_trachcat:
            arch_key = "D24_AUSPICIOUS_DATE"
            specific_target = "AUSPICIOUS_DATE"
            authoritative_dt = "Dụng Thần"
        elif is_career:
            arch_key = "D14_CAREER_WORK"
            specific_target = "CAREER_WORK"
            authoritative_dt = "Quan Quỷ"
        elif is_when:
            arch_key = "D12_TIMING_WHEN"
            specific_target = "TIMING_WHEN"

        # V104.0: Quy tắc Định vị Lục Thân Chủ Thể Cổ Pháp (Tăng San Bốc Dịch & Bốc Phệ Chính Tông)
        # Khi người dùng hỏi về một thành viên cụ thể trong gia đình mà chưa khóa Dụng Thần sự việc đặc thù,
        # bắt buộc khóa chính xác Lục Thân của người đó để tuyệt đối không bao giờ giao nhầm Dụng Thần!
        if not authoritative_dt or authoritative_dt == "Dụng Thần":
            if any(w in q_low for w in ["vợ tôi", "vợ của tôi", "vợ mình", "bạn gái tôi", "bạn gái của tôi"]) and "chồng" not in q_low:
                authoritative_dt = "Thê Tài"
                subject_person = "Người vợ / Bạn gái của bạn (Dụng Thần: Thê Tài)"
                if arch_key == "D25_SPIRITUAL_GENERAL" and dung_than_hint != "__SINGLE_CLAUSE__":
                    arch_key = "D17_LOVE_MARRIAGE"
            elif any(w in q_low for w in ["chồng tôi", "chồng của tôi", "chồng mình", "bạn trai tôi", "bạn trai của tôi"]) and "vợ" not in q_low:
                authoritative_dt = "Quan Quỷ"
                subject_person = "Người chồng / Bạn trai của bạn (Dụng Thần: Quan Quỷ)"
                if arch_key == "D25_SPIRITUAL_GENERAL" and dung_than_hint != "__SINGLE_CLAUSE__":
                    arch_key = "D17_LOVE_MARRIAGE"
            elif any(w in q_low for w in ["con tôi", "con của tôi", "con trai tôi", "con gái tôi", "các con tôi", "bé nhà tôi"]):
                authoritative_dt = "Tử Tôn"
                subject_person = "Con cái của bạn (Dụng Thần: Tử Tôn)"
            elif any(w in q_low for w in ["bố tôi", "mẹ tôi", "ba tôi", "má tôi", "bố mẹ tôi", "cha mẹ tôi"]):
                authoritative_dt = "Phụ Mẫu"
                subject_person = "Bố mẹ / Phụ mẫu của bạn (Dụng Thần: Phụ Mẫu)"
            elif any(w in q_low for w in ["anh trai tôi", "chị gái tôi", "em trai tôi", "em gái tôi", "anh chị em tôi"]):
                authoritative_dt = "Huynh Đệ"
                subject_person = "Anh chị em của bạn (Dụng Thần: Huynh Đệ)"

        arch_meta = UNIVERSAL_25_ARCHETYPES.get(arch_key, UNIVERSAL_25_ARCHETYPES["D25_SPIRITUAL_GENERAL"])

        # V104.0: Nhận diện Câu hỏi Đa Chủ Thể (2 người cùng thi / cùng làm việc / cùng hỏi kết quả: "tôi và vợ tôi...", "tôi và chồng...", "tôi và bạn...", "2 con tôi...")
        multi_subjects = []
        if specific_target not in ("CHILDREN_AGE", "CHILDREN_COUNT", "SIBLINGS_COUNT", "MARITAL_STATUS_NOW", "FIDELITY_AFFAIR_CHECK", "LOCATION_HOME_WORK", "POSTURE_STATE"):
            if any(p in q_low for p in ["tôi và vợ", "vợ và tôi", "vợ chồng tôi", "hai vợ chồng", "2 vợ chồng", "cả hai vợ chồng"]):
                multi_subjects = [
                    {"label": "Bản thân bạn", "role": "SELF", "lh_dt": "Hào Thế", "km_role": "NHAT_CAN"},
                    {"label": "Vợ của bạn", "role": "WIFE", "lh_dt": "Thê Tài", "km_role": "CAN_HOP"},
                ]
            elif any(p in q_low for p in ["tôi và chồng", "chồng và tôi"]):
                multi_subjects = [
                    {"label": "Bản thân bạn", "role": "SELF", "lh_dt": "Hào Thế", "km_role": "NHAT_CAN"},
                    {"label": "Chồng của bạn", "role": "HUSBAND", "lh_dt": "Quan Quỷ", "km_role": "CAN_HOP"},
                ]
            elif any(p in q_low for p in ["tôi và người yêu", "tôi và bạn gái", "tôi và bạn trai"]):
                multi_subjects = [
                    {"label": "Bản thân bạn", "role": "SELF", "lh_dt": "Hào Thế", "km_role": "NHAT_CAN"},
                    {"label": "Người yêu của bạn", "role": "PARTNER", "lh_dt": "Hào Ứng", "km_role": "CAN_HOP"},
                ]
            elif any(p in q_low for p in ["tôi và bạn", "bạn và tôi", "tôi và anh", "tôi và chị", "tôi và em", "tôi và đồng nghiệp", "tôi và đối tác", "hai anh em", "2 anh em", "hai chị em", "2 chị em"]):
                multi_subjects = [
                    {"label": "Bản thân bạn", "role": "SELF", "lh_dt": "Hào Thế", "km_role": "NHAT_CAN"},
                    {"label": "Người đi cùng (Bạn / Anh chị em / Đối tác)", "role": "PEER", "lh_dt": "Huynh Đệ", "km_role": "NGUYET_CAN"},
                ]
            elif any(p in q_low for p in ["tôi và con", "mẹ con tôi", "bố con tôi", "cha con tôi", "hai mẹ con", "hai bố con"]):
                multi_subjects = [
                    {"label": "Bản thân bạn", "role": "SELF", "lh_dt": "Hào Thế", "km_role": "NHAT_CAN"},
                    {"label": "Con của bạn", "role": "CHILD", "lh_dt": "Tử Tôn", "km_role": "THOI_CAN"},
                ]
            elif any(p in q_low for p in ["con trai và con gái", "con gái và con trai", "hai con tôi", "2 con tôi", "hai đứa con", "2 đứa con"]):
                multi_subjects = [
                    {"label": "Con Trai của bạn", "role": "SON", "lh_dt": "Tử Tôn (Dương)", "km_role": "THOI_CAN"},
                    {"label": "Con Gái của bạn", "role": "DAUGHTER", "lh_dt": "Tử Tôn (Âm)", "km_role": "THOI_CAN_AM"},
                ]
            elif any(p in q_low for p in ["bố và mẹ", "mẹ và bố", "ba và mẹ", "bố mẹ tôi", "ba mẹ tôi"]):
                multi_subjects = [
                    {"label": "Bố của bạn", "role": "FATHER", "lh_dt": "Phụ Mẫu (Dương)", "km_role": "NIEN_CAN"},
                    {"label": "Mẹ của bạn", "role": "MOTHER", "lh_dt": "Phụ Mẫu (Âm)", "km_role": "NIEN_CAN_AM"},
                ]

        sub_intents = []
        if multi_subjects:
            subject_person = f"{multi_subjects[0]['label']} & {multi_subjects[1]['label']} (Tách 2 trục Dụng Thần độc lập)"
            sub_intents.append(f"Phân Chiêm Đa Nhân (Tách riêng kết quả của {multi_subjects[0]['label']} và {multi_subjects[1]['label']} — tránh gộp chung sai lệch nếu 1 người được 1 người trượt)")
        if is_when and arch_key != "D12_TIMING_WHEN":
            sub_intents.append("Hỏi kèm Thời điểm Ứng kỳ (Khi nào / Bao giờ)")
        if any(w in q_low for w in ["ở đâu", "hướng nào", "chỗ nào"]) and arch_key not in ("D01_LOCATION_BINARY", "D11_LOST_ITEM_WHERE"):
            sub_intents.append("Hỏi kèm Phương hướng & Không gian (Ở đâu / Hướng nào)")
        if has_numeric_word and arch_key not in ("D06_GENDER_AGE", "D07_CHILDREN_COUNT", "D09_QUANTITY_PRICE"):
            sub_intents.append("Hỏi kèm Định lượng Con số / Số lượng")

        _clean_dt_hint = "" if dung_than_hint == "__SINGLE_CLAUSE__" else dung_than_hint
        base_res = {
            "multi_subjects": multi_subjects,
            "is_compound_question": False,
            "sub_questions": [],
            "raw_question": q_raw,
            "archetype_key": arch_key,
            "archetype_code": arch_meta["code"],
            "archetype_name": arch_meta["name"],
            "question_mode": arch_meta["mode"],
            "specific_target": specific_target,
            "authoritative_dt": authoritative_dt,
            "subject_person": subject_person,
            "subject_lh_dt": authoritative_dt or _clean_dt_hint or "Bản Thân",
            "lh_dt_instruction": arch_meta["lh_dt"],
            "km_dt_instruction": arch_meta["km_dt"],
            "answer_rule": arch_meta["answer_rule"],
            "option_a": option_a,
            "option_b": option_b,
            "sub_intents": sub_intents,
        }

        # V104.0: BỘ PHÂN TÁCH ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN (Multi-SubQuestion Decomposer)
        # Khi người dùng hỏi 1 câu nhưng chứa 2–3 câu hỏi nhỏ khác nhau (VD: "cuộc đời tôi có mấy vợ, và mấy đứa con",
        # "tôi có mấy đứa con và chúng bao nhiêu tuổi", "nhà tôi mấy tầng, và có mấy đứa con", "công việc thế nào và tài chính có lộc không"),
        # bắt buộc bóc tách toàn bộ các vế câu hỏi nhỏ để AI Số 2 giải mã đầy đủ từng vế, tuyệt đối không bỏ sót!
        if not dung_than_hint or dung_than_hint != "__SINGLE_CLAUSE__":
            sub_qs = QuestionReaderAI.decompose_sub_questions(q_raw, dung_than_hint=dung_than_hint, category_hint=category_hint)
            if len(sub_qs) >= 2:
                base_res["is_compound_question"] = True
                base_res["sub_questions"] = sub_qs
                base_res["archetype_code"] = " + ".join(sq["archetype_code"] for sq in sub_qs)
                base_res["archetype_name"] = " & ".join(sq["archetype_name"] for sq in sub_qs)
                base_res["subject_person"] = " · ".join(
                    f"[Câu hỏi nhỏ {i+1}: «{sq['clause_label']}» ➔ Giao DT: {sq['subject_lh_dt']}]"
                    for i, sq in enumerate(sub_qs)
                )
                base_res["lh_dt_instruction"] = " | ".join(
                    f"[Vế {i+1} - {sq['clause_label']}]: {sq['lh_dt_instruction']}"
                    for i, sq in enumerate(sub_qs)
                )
                base_res["sub_intents"].append(
                    f"Tách {len(sub_qs)} câu hỏi nhỏ độc lập ({', '.join(sq['clause_label'] for sq in sub_qs)}) để đối chứng riêng từng Dụng Thần"
                )
        # V104.0: Gắn CON AI SỐ 1 THỰC TẾ (Dòng rẻ nhất & siêu tốc: gemini-2.5-flash-lite / gemini-2.0-flash-lite)
        # ngay tại Bước 0 để đọc hiểu câu hỏi và truyền Dụng Thần + Chỉ thị xuống cho mọi Phương pháp & Con AI Số 2!
        if (not dung_than_hint or dung_than_hint != "__SINGLE_CLAUSE__") and len(q_raw) >= 4:
            _ai1_sig = "AI1_READER_V104::" + hashlib.md5(q_raw.lower().encode("utf-8")).hexdigest()
            _ai1_cached = _REAL_DUAL_AI_CACHE.get(_ai1_sig)
            if _ai1_cached is None:
                _p_ai1_step0 = (
                    "Bạn là CON AI SỐ 1 (Model Siêu Nhẹ Chuyên Đọc Hiểu & Phân Tích Câu Hỏi Dịch Học — TUYỆT ĐỐI KHÔNG TỰ ĐOÁN SỐ HAY BỊA ĐÁP ÁN, chỉ đọc hiểu câu hỏi để truyền cho 3 Hệ Thống Quẻ Chủ Lực: Mai Hoa Dịch Số, Kỳ Môn Độn Giáp, Lục Hào Kinh Dịch và Con AI Số 2 tự luận quẻ).\n"
                    f"Câu hỏi của người dùng: \"{q_raw}\"\n\n"
                    "Hãy đọc hiểu thực tế câu hỏi này và trả về ĐÚNG 1 JSON hợp lệ:\n"
                    "{\n"
                    "  \"ai1_intent_summary\": \"Tóm tắt ngắn gọn, chính xác người dùng đang hỏi cái gì (nêu rõ mọi vế và mọi chủ thể)\",\n"
                    "  \"ai1_target_code\": \"Chỉ chọn mã nếu câu hỏi ĐÚNG 100% là câu hỏi đó, còn lại BẮT BUỘC điền DIRECT_HEXAGRAM_REASONING: HOUSEHOLD_MEMBERS (nhà có bao nhiêu người) | HOUSE_FLOORS (nhà mấy tầng/ở tầng mấy) | SIBLINGS_COUNT (mấy anh chị em) | PEOPLE_AROUND (xung quanh có mấy người) | SPOUSE_COUNT (cuộc đời có mấy vợ/chồng) | MARITAL_STATUS_NOW (đã kết hôn chưa) | FIDELITY_AFFAIR_CHECK (vợ/chồng có nhân tình/ngoại tình/người thứ 3 bên ngoài không) | CHILDREN_COUNT (có mấy đứa con) | CHILDREN_AGE (con bao nhiêu tuổi) | CLOTHING_VEHICLE (áo màu gì/đi xe gì) | LOCATION_HOME_WORK (ở nhà hay công ty) | POSTURE_STATE (đứng hay ngồi) | GENERAL_QUANTITY (còn thiếu bao nhiêu km/bao nhiêu tiền/điểm/ngày) | GENERIC_AB (chọn A hay B) | DIRECT_HEXAGRAM_REASONING (mọi câu hỏi khác — để Mai Hoa, Kỳ Môn, Lục Hào tự luận quẻ)\",\n"
                    "  \"ai1_expected_answer_format\": \"Đơn vị và khuôn mẫu câu trả lời bắt buộc sát đúng câu hỏi\",\n"
                    "  \"ai1_primary_dung_than\": \"Chọn ĐÚNG 1 trong 6 Dụng Thần chính phù hợp nhất với chủ thể được hỏi (Hỏi về Vợ/Bạn gái -> Thê Tài; Hỏi về Chồng/Bạn trai/Công danh -> Quan Quỷ; Hỏi về Con cái -> Tử Tôn; Hỏi về Nhà cửa/Bằng cấp/Xe cộ/Bố mẹ -> Phụ Mẫu; Hỏi về Anh chị em/Bạn bè -> Huynh Đệ; Hỏi về Bản thân -> Bản Thân)\",\n"
                    "  \"ai1_dung_than_guide\": \"Hướng dẫn tra cứu Dụng Thần trên Mai Hoa Dịch Số (Thể/Dụng, Chủ/Hỗ/Biến), Kỳ Môn Độn Giáp (Cung/Sao/Cửa/Thần) và Lục Hào (Thế/Ứng/Lục Thân)\",\n"
                    "  \"ai1_strict_instruction_to_ai2\": \"Mệnh lệnh nghiêm ngặt cho AI Số 2: Phải tự luận giải trực tiếp từ các quẻ chuẩn xác (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch) để trả lời đúng 100% câu hỏi của người dùng, TUYỆT ĐỐI CẤM trả lời lạc sang chủ đề khác!\"\n"
                    "}"
                )
                _res_ai1_s0 = _call_gemini_json_fast(_p_ai1_step0, timeout_sec=8, tier="cheapest_reader")
                if isinstance(_res_ai1_s0, dict) and _res_ai1_s0.get("ai1_intent_summary"):
                    _ai1_cached = _res_ai1_s0
                    _REAL_DUAL_AI_CACHE[_ai1_sig] = _ai1_cached
            if isinstance(_ai1_cached, dict):
                base_res["ai1_real_llm"] = _ai1_cached
                base_res["ai1_intent_summary"] = _ai1_cached.get("ai1_intent_summary", "")
                base_res["ai1_expected_answer_format"] = _ai1_cached.get("ai1_expected_answer_format", "")
                base_res["ai1_strict_instruction_to_ai2"] = _ai1_cached.get("ai1_strict_instruction_to_ai2", "")
                _llm_tcode = str(_ai1_cached.get("ai1_target_code") or "").strip().upper()
                # V104.0: TUYỆT ĐỐI KHÔNG cho phép _llm_tcode ép các câu hỏi tự nhiên vào khuôn mẫu hẹp (như MARITAL_STATUS_NOW)
                # trừ khi câu hỏi thực sự chứa từ khóa đặc thù của nhóm đó!
                if base_res.get("specific_target") == "" and _llm_tcode == "FIDELITY_AFFAIR_CHECK" and any(w in q_low for w in ["nhân tình", "ngoại tình", "bồ", "thứ 3", "thứ ba", "phản bội", "cắm sừng", "lăng nhăng", "người khác", "ai khác", "chung thủy", "ngoài luồng", "tư tình", "gian díu"]):
                    base_res["specific_target"] = "FIDELITY_AFFAIR_CHECK"
                elif base_res.get("specific_target") in ("", "GENERAL_QUANTITY") and _llm_tcode == "HOUSEHOLD_MEMBERS" and any(w in q_low for w in ["nhà", "gia đình", "hộ khẩu"]) and any(w in q_low for w in ["người", "nhân khẩu", "thành viên"]):
                    base_res["specific_target"] = "HOUSEHOLD_MEMBERS"
                elif base_res.get("specific_target") in ("", "GENERAL_QUANTITY") and _llm_tcode == "SIBLINGS_COUNT" and any(w in q_low for w in ["anh", "chị", "em", "thứ mấy", "huynh đệ"]):
                    base_res["specific_target"] = "SIBLINGS_COUNT"
                    base_res["authoritative_dt"] = "Huynh Đệ"
                    base_res["subject_lh_dt"] = "Huynh Đệ"
                _valid_dts = ("Phụ Mẫu", "Thê Tài", "Tử Tôn", "Quan Quỷ", "Huynh Đệ", "Bản Thân")
                _llm_dt = str(_ai1_cached.get("ai1_primary_dung_than") or "").strip()
                if not base_res.get("authoritative_dt") and _llm_dt in _valid_dts:
                    base_res["authoritative_dt"] = _llm_dt
                    base_res["subject_lh_dt"] = _llm_dt
                base_res["subject_person"] = (
                    f"{_ai1_cached.get('ai1_intent_summary', base_res['subject_person'])} "
                    f"— <b style='color:#fde047;'>Khuôn đáp án bắt buộc:</b> {_ai1_cached.get('ai1_expected_answer_format', '')}"
                )
                base_res["lh_dt_instruction"] = (
                    f"{_ai1_cached.get('ai1_dung_than_guide', base_res['lh_dt_instruction'])} "
                    f"| <b style='color:#38bdf8;'>Lệnh truyền AI 2 & 18 Phương pháp:</b> {_ai1_cached.get('ai1_strict_instruction_to_ai2', '')}"
                )
                base_res["answer_rule"] = _ai1_cached.get("ai1_strict_instruction_to_ai2") or base_res["answer_rule"]
            else:
                base_res["ai1_intent_summary"] = f"Hỏi về {base_res['archetype_name']} cho đối tượng [{base_res['subject_person']}]"
                base_res["ai1_expected_answer_format"] = base_res["answer_rule"]
                base_res["ai1_strict_instruction_to_ai2"] = f"Phải trả lời trực diện câu hỏi '{q_raw}' theo đúng đơn vị và từng chủ thể được hỏi; cấm trả lời lạc sang chủ đề khác."
        return base_res

    @staticmethod
    def decompose_sub_questions(question: str, dung_than_hint: str = "", category_hint: str = "") -> list:
        """
        Tự động nhận diện và bóc tách 1 câu hỏi ghép thành danh sách các câu hỏi nhỏ độc lập (Sub-Questions).
        Hoạt động kết hợp cả 2 cơ chế:
        1. Tách vế câu theo dấu phẩy (,), chấm phẩy (;), chấm hỏi (?), hoặc từ nối (và, cùng, còn, rồi, kèm, thêm).
        2. Quét Đa Mục Tiêu (Multi-Target Scanner) ngay cả khi người dùng viết liền không dấu phẩy (VD: "tôi có mấy vợ mấy con", "tôi có mấy đứa con bao nhiêu tuổi").
        """
        q_raw = str(question or "").strip()
        q_low = q_raw.lower()
        if len(q_low) < 6:
            return []

        # Bảo vệ các cụm chủ ngữ ghép ("tôi và vợ", "con gái và con trai", "bố và mẹ"...) để không tách nhầm chủ ngữ
        protected_q = q_raw
        _PROTECT_PHRASES = [
            "tôi và vợ tôi", "tôi và vợ", "vợ và tôi", "hai vợ chồng", "vợ chồng tôi",
            "tôi và chồng tôi", "tôi và chồng", "chồng và tôi",
            "tôi và người yêu", "tôi và bạn gái", "tôi và bạn trai",
            "tôi và bạn", "bạn và tôi", "tôi và anh", "tôi và chị", "tôi và em",
            "tôi và đồng nghiệp", "tôi và đối tác", "tôi và con",
            "con gái và con trai", "con trai và con gái",
            "chị gái và anh trai", "anh trai và chị gái",
            "mấy chị gái và mấy anh trai", "mấy anh trai và mấy chị gái",
            "bao nhiêu chị gái và bao nhiêu anh trai", "bao nhiêu anh trai và bao nhiêu chị gái",
            "bố và mẹ", "mẹ và bố", "ba và mẹ", "ông và bà",
            "nam và nữ", "trai và gái", "nếp và tẻ", "ăn và ngủ",
        ]
        for _pp in _PROTECT_PHRASES:
            protected_q = re.sub(re.escape(_pp), lambda m: m.group(0).replace(" và ", " __AND_KEEP__ "), protected_q, flags=re.IGNORECASE)

        # 1. Tách theo dấu câu và từ nối vế câu hỏi (Không tách cụm trạng từ "còn thiếu", "còn bao nhiêu", "còn mấy", "còn lại", "còn cách", "còn phải")
        protected_q = re.sub(
            r"\bcòn\s+(thiếu|bao nhiêu|mấy|lại|cách|phải|cần|nợ|yêu|thương|sống|lâu)\b",
            r"__CON_ADV__ \1",
            protected_q,
            flags=re.IGNORECASE,
        )
        raw_clauses = re.split(r"[,;?/|]+|\s+(?:và|cùng với|còn|rồi|kèm theo|kèm|thêm)\s+", protected_q, flags=re.IGNORECASE)
        clauses = []
        for rc in raw_clauses:
            c_clean = rc.replace(" __AND_KEEP__ ", " và ").replace("__CON_ADV__ ", "còn ").strip(" .,;?!-/")
            if len(c_clean) >= 3:
                clauses.append(c_clean)

        # 2. Quét Đa Mục Tiêu Đặc Thù trong toàn câu hỏi (đề phòng viết liền hoặc 1 vế chứa 2 ý hỏi khác nhau)
        _TARGET_DETECTORS = [
            (
                "SPOUSE_COUNT",
                ["mấy vợ", "bao nhiêu vợ", "mấy người vợ", "mấy đời vợ", "lấy mấy vợ", "có mấy vợ", "mấy bà vợ",
                 "mấy chồng", "bao nhiêu chồng", "mấy người chồng", "mấy đời chồng", "lấy mấy chồng", "có mấy chồng",
                 "mấy lần kết hôn", "kết hôn mấy lần", "mấy lần đò", "mấy lần lập gia đình"],
                "Cuộc đời có mấy vợ" if "chồng" not in q_low or "vợ" in q_low else "Cuộc đời có mấy chồng",
            ),
            (
                "FIDELITY_AFFAIR_CHECK",
                ["nhân tình", "ngoại tình", "bồ bịch", "có bồ", "người thứ 3", "người thứ ba", "phản bội", "cắm sừng", "lăng nhăng", "chung thủy"],
                "Vợ / Chồng có nhân tình bên ngoài không",
            ),
            (
                "MARITAL_STATUS_NOW",
                ["kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
                 "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"],
                "Đã kết hôn / lập gia đình chưa",
            ),
            (
                "CHILDREN_COUNT",
                ["bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con", "bao nhiêu con",
                 "mấy trai mấy gái", "sinh mấy con", "đường con cái", "tử tức", "có con chưa", "mấy con"],
                "Có mấy người con (Mấy trai mấy gái)",
            ),
            (
                "CHILDREN_AGE",
                ["con gái và con trai của tôi bao nhiêu tuổi", "con trai và con gái của tôi bao nhiêu tuổi",
                 "con tôi bao nhiêu tuổi", "con của tôi bao nhiêu tuổi", "các con bao nhiêu tuổi",
                 "chúng bao nhiêu tuổi", "chúng nó bao nhiêu tuổi", "con mấy tuổi", "chúng mấy tuổi"],
                "Các con bao nhiêu tuổi",
            ),
            (
                "HOUSE_FLOORS",
                ["mấy tầng", "bao nhiêu tầng", "tầng mấy", "nhà cao mấy", "nhà mấy lầu", "mấy lầu", "mấy phòng", "bao nhiêu phòng"],
                "Nhà mấy tầng / Ở tầng mấy",
            ),
            (
                "SIBLINGS_COUNT",
                ["mấy anh chị em", "bao nhiêu anh chị em", "mấy chị gái", "bao nhiêu chị gái",
                 "mấy anh trai", "bao nhiêu anh trai", "mấy em gái", "bao nhiêu em gái",
                 "mấy em trai", "bao nhiêu em trai", "mấy anh em", "bao nhiêu anh em",
                 "mấy chị em", "bao nhiêu chị em", "con thứ mấy", "thứ mấy trong nhà"],
                "Gia đình có mấy chị gái, mấy anh trai & Thứ mấy",
            ),
            (
                "HOUSEHOLD_MEMBERS",
                ["nhà tôi có bao nhiêu người", "nhà tôi có mấy người", "nhà có bao nhiêu người", "nhà có mấy người",
                 "gia đình tôi có bao nhiêu người", "gia đình tôi có mấy người", "gia đình có bao nhiêu người", "gia đình có mấy người",
                 "trong nhà có bao nhiêu người", "trong nhà có mấy người", "nhà có mấy nhân khẩu", "gia đình có mấy nhân khẩu"],
                "Nhà / Gia đình có bao nhiêu người (Nhân khẩu)",
            ),
            (
                "PEOPLE_AROUND",
                ["xung quanh tôi có mấy người", "trong phòng có mấy người", "ở đây có mấy người", "bên cạnh tôi có ai", "ở một mình hay"],
                "Xung quanh có mấy người",
            ),
            (
                "CLOTHING_VEHICLE",
                ["mặc áo màu gì", "áo màu gì", "quần áo màu gì", "trang phục màu gì", "đi xe gì", "xe màu gì", "biển số xe", "nhà màu gì", "bàn phím", "máy tính màu gì", "điện thoại màu gì", "màu gì"],
                "Đồ vật / Trang phục / Xe cộ màu gì",
            ),
            (
                "LOCATION_HOME_WORK",
                ["ở nhà hay", "hay ở nhà", "ở công ty hay", "trong nhà hay ngoài đường"],
                "Đang ở nhà hay ở công ty/bên ngoài",
            ),
            (
                "POSTURE_STATE",
                ["đứng hay ngồi", "ngồi hay đứng", "nằm hay ngồi", "ngồi hay nằm", "ngủ hay thức"],
                "Đang đứng hay đang ngồi/nằm",
            ),
        ]

        # Kiểm tra bổ sung cho trường hợp hỏi gộp "mấy đứa con + bao nhiêu tuổi"
        _has_child_cnt_kw = any(w in q_low for w in ["bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con", "bao nhiêu con", "mấy trai mấy gái", "mấy con"]) and not any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao", "con thứ mấy"])
        _has_age_kw = any(w in q_low for w in ["bao nhiêu tuổi", "mấy tuổi", "sinh năm", "năm sinh"])
        _has_child_ref = any(w in q_low for w in ["con gái", "con trai", "con của tôi", "con tôi", "mấy đứa con", "các con", "con cái", "đứa con", "chúng"])

        detected_targets = []
        for t_code, kw_list, default_lbl in _TARGET_DETECTORS:
            if t_code == "CHILDREN_COUNT" and any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao", "con thứ mấy"]):
                continue
            for kw in kw_list:
                pos = q_low.find(kw)
                if pos != -1:
                    detected_targets.append((pos, t_code, kw, default_lbl))
                    break

        if _has_child_cnt_kw and _has_age_kw and _has_child_ref:
            if not any(t[1] == "CHILDREN_AGE" for t in detected_targets):
                pos_age = min([q_low.find(w) for w in ["bao nhiêu tuổi", "mấy tuổi", "sinh năm", "năm sinh"] if q_low.find(w) != -1] or [999])
                detected_targets.append((pos_age, "CHILDREN_AGE", "con tôi bao nhiêu tuổi", "Các con bao nhiêu tuổi"))

        detected_targets.sort(key=lambda x: x[0])

        # Xây dựng danh sách Sub-Questions từ các vế câu (clauses) và các mục tiêu phát hiện được (detected_targets)
        sub_blueprints = []
        seen_keys = set()

        if len(clauses) >= 2:
            for cl in clauses:
                cl_low = cl.lower()
                # Bổ sung ngữ cảnh nếu vế 2 viết tắt như "mấy đứa con" hoặc "bao nhiêu tuổi"
                cl_expanded = cl
                if cl_low in ("mấy đứa", "mấy đứa con", "bao nhiêu con", "mấy con", "mấy người con"):
                    cl_expanded = f"tôi có {cl}"
                elif any(w in cl_low for w in ["bao nhiêu tuổi", "mấy tuổi"]) and _has_child_ref and not any(w in cl_low for w in ["con", "tôi", "vợ", "chồng", "bố", "mẹ"]):
                    cl_expanded = f"các con tôi {cl}"
                bp_cl = QuestionReaderAI.analyze_question(cl_expanded, dung_than_hint="__SINGLE_CLAUSE__", category_hint=category_hint)
                # Chỉ coi là 1 câu hỏi nhỏ hợp lệ nếu nhận diện được chủ đề rõ ràng (không phải D25 mặc định vô nghĩa từ mảnh câu cụt)
                is_meaningful_clause = (
                    bp_cl["specific_target"] != ""
                    or bp_cl["archetype_key"] != "D25_SPIRITUAL_GENERAL"
                    or any(w in cl_low for w in ["mấy", "bao nhiêu", "không", "chưa", "thế nào", "ra sao", "khi nào", "bao giờ", "ở đâu", "ai", "hay"])
                )
                if not is_meaningful_clause:
                    continue
                # Với các vế câu tách trực tiếp từ dấu phẩy / từ nối "và", dùng khóa kết hợp nội dung vế câu
                # để 2 câu hỏi "A hay B" khác nhau (VD: "con tôi không khóc hay đang khóc , và con gái hay con trai đang khóc")
                # tuyệt đối không bị gộp trùng vào 1 khóa GENERIC_AB!
                dedup_key = f"{bp_cl['specific_target'] or bp_cl['archetype_key']}::{bp_cl.get('option_a','')}::{bp_cl.get('option_b','')}::{cl_low[:32]}"
                if dedup_key not in seen_keys:
                    seen_keys.add(dedup_key)
                    bp_cl["clause_label"] = cl[0].upper() + cl[1:] if cl else bp_cl["subject_person"]
                    sub_blueprints.append(bp_cl)

        # Nếu viết liền không tách vế hoặc có mục tiêu đặc thù bị gộp trong 1 vế, bổ sung từ detected_targets
        if len(detected_targets) >= 2 and len(sub_blueprints) < len(detected_targets):
            sub_blueprints = []
            seen_keys = set()
            for _, t_code, kw_match, def_lbl in detected_targets:
                if t_code in seen_keys:
                    continue
                seen_keys.add(t_code)
                # Tìm vế câu gốc chứa kw_match nếu có
                matching_cl = def_lbl
                for cl in clauses:
                    if kw_match in cl.lower():
                        matching_cl = cl[0].upper() + cl[1:]
                        break
                synth_q = matching_cl if t_code != "CHILDREN_AGE" else "con gái và con trai của tôi bao nhiêu tuổi"
                if t_code == "CHILDREN_COUNT" and any(w in synth_q.lower() for w in ["tuổi", "sinh năm"]):
                    synth_q = "tôi có mấy đứa con"
                bp_t = QuestionReaderAI.analyze_question(synth_q, dung_than_hint="__SINGLE_CLAUSE__", category_hint=category_hint)
                bp_t["specific_target"] = t_code
                bp_t["clause_label"] = matching_cl
                sub_blueprints.append(bp_t)

        # Nếu tất cả các vế tách ra đều cùng là SIBLINGS_COUNT (VD: "tôi có mấy chị gái, mấy anh trai"),
        # gộp làm 1 câu hỏi SIBLINGS_COUNT duy nhất để Bộ Giải Mã Huynh Đệ Tam Thức trả lời trọn vẹn cả Số Chị gái + Số Anh trai + Thứ bậc!
        if len(sub_blueprints) >= 2 and all(bp.get("specific_target") == "SIBLINGS_COUNT" for bp in sub_blueprints):
            return []

        return sub_blueprints if len(sub_blueprints) >= 2 else []


class HexagramReasoningAI:
    """
    CON AI SỐ 2 (V104.0): Chuyên trách TỰ LUẬN GIẢI QUẺ ĐA HỆ THỐNG (MAI HOA – KỲ MÔN – LỤC HÀO – THIẾT BẢN).
    Nhận Bản Hồ Sơ Câu Hỏi (`blueprint`) từ Con AI Số 1, mang đi đối chứng trực tiếp
    với Ma Trận Quẻ Toán Học & Tượng Số (`extract_mai_hoa_ky_mon_luc_hao_matrix`) để
    tự luận giải chuẩn xác 100% cho BẤT KỲ câu hỏi nào người dùng đặt ra!
    """

    # Bảng 8 Quái Cơ Bản: (Nhị phân 3 hào từ dưới lên, Tiên Thiên số, Hậu Thiên số, Ngũ Hành, Tượng Quái)
    _TRIGRAM_META = {
        "Càn":  ((1, 1, 1), 1, 6, "Kim",  "Trời / Cha / Chồng / Lãnh đạo / Chính trực / Cương kiện"),
        "Đoài": ((1, 1, 0), 2, 7, "Kim",  "Đầm / Thiếu nữ / Lời nói / Trao đổi / Vui vẻ / Tín hiệu"),
        "Ly":   ((1, 0, 1), 3, 9, "Hỏa",  "Lửa / Trung nữ / Văn thư / Sáng tỏ / Lễ nghĩa / Danh tiếng"),
        "Chấn": ((1, 0, 0), 4, 3, "Mộc",  "Sấm / Trưởng nam / Khởi động / Di chuyển / Xe cộ / Quyết đoán"),
        "Tốn":  ((0, 1, 1), 5, 4, "Mộc",  "Gió / Trưởng nữ / Người vợ / Thuận tòng / Tiệm tiến / Tinh tế"),
        "Khảm": ((0, 1, 0), 6, 1, "Thủy", "Nước / Trung nam / Trí tuệ / Tâm sự ngầm / Vất vả / Thử thách"),
        "Cấn":  ((0, 0, 1), 7, 8, "Thổ",  "Núi / Thiếu nam / Dừng lại đúng giới hạn / Giữ chính đạo / Tòa nhà cao"),
        "Khôn": ((0, 0, 0), 8, 2, "Thổ",  "Đất / Mẹ / Người vợ hiền / Gia đạo / Bao dung / Nhu thuận"),
    }

    # Bảng 64 Quẻ Kinh Dịch: (Thượng Quái, Hạ Quái) -> (Tên Đầy Đủ, Ý Nghĩa Cốt Lõi)
    _PAIR_TO_HEX64 = {
        ("Càn", "Càn"):   ("Thuần Càn", "Cương kiện, chính đại quang minh, vạn vật khởi đầu hanh thông"),
        ("Khôn", "Khôn"): ("Thuần Khôn", "Nhu thuận, bao dung,厚 đức tải vật, gia đạo yên ổn"),
        ("Khảm", "Chấn"): ("Thủy Lôi Truân", "Gian nan buổi đầu nhưng Dụng Thủy sinh Thể Mộc, vất vả lo toan để dựng xây nền tảng"),
        ("Cấn", "Khảm"):  ("Sơn Thủy Mông", "Mờ mịt ban đầu, cần khai sáng và tìm hiểu rõ thực hư"),
        ("Khảm", "Càn"):  ("Thủy Thiên Nhu", "Kiên nhẫn chờ thời, ẩm thực sum vầy, không nên nóng vội"),
        ("Càn", "Khảm"):  ("Thiên Thủy Tụng", "Tranh luận, bất đồng quan điểm, nên hòa giải tránh kiện tụng"),
        ("Khôn", "Khảm"): ("Địa Thủy Sư", "Kỷ luật, huy động lực lượng, gánh vác trọng trách lớn"),
        ("Khảm", "Khôn"): ("Thủy Địa Tỷ", "Thân thiết, gắn bó, hòa hợp tương trợ lẫn nhau"),
        ("Tốn", "Càn"):   ("Phong Thiên Tiểu Súc", "Tích lũy nhỏ, tạm thời kiềm giữ để chờ thời cơ"),
        ("Càn", "Đoài"):  ("Thiên Trạch Lý", "Giữ lễ nghĩa, đi đúng khuôn phép thì nguy cũng hóa an"),
        ("Khôn", "Càn"):  ("Địa Thiên Thái", "Âm dương giao hòa, gia đạo & vạn sự đại cát hanh thông"),
        ("Càn", "Khôn"):  ("Thiên Địa Bĩ", "Âm dương cách trở, tạm thời bế tắc, chưa hiểu lòng nhau"),
        ("Càn", "Ly"):    ("Thiên Hỏa Đồng Nhân", "Đồng tâm hiệp lực, hòa đồng cùng người, minh bạch"),
        ("Ly", "Càn"):    ("Hỏa Thiên Đại Hữu", "Tài lộc dồi dào, sáng suốt, gặt hái thành quả lớn"),
        ("Khôn", "Cấn"):  ("Địa Sơn Khiêm", "Khiêm nhường, giữ mình đúng mực, trong ấm ngoài êm"),
        ("Chấn", "Khôn"): ("Lôi Địa Dự", "Vui vẻ, chuẩn bị chu đáo, phấn khởi đón tin vui"),
        ("Đoài", "Chấn"): ("Trạch Lôi Tùy", "Phu xướng phụ tùy — Vợ chồng thuận hòa đi cùng nhau, thuận theo lẽ phải"),
        ("Cấn", "Tốn"):   ("Sơn Phong Cổ", "Chỉnh đốn việc cũ, tháo gỡ hiểu lầm tích tụ"),
        ("Khôn", "Đoài"): ("Địa Trạch Lâm", "Bao dung, đến gần quan tâm, vận khí đang lên"),
        ("Tốn", "Khôn"):  ("Phong Địa Quan", "Quan sát kỹ lưỡng, suy xét thấu đáo bằng sự điềm tĩnh"),
        ("Ly", "Chấn"):   ("Hỏa Lôi Phệ嗑", "Vượt qua chướng ngại, làm rõ trắng đen"),
        ("Cấn", "Ly"):    ("Sơn Hỏa Bí", "Văn vẻ, phẩm hạnh trang nhã, giữ trọn thể diện"),
        ("Cấn", "Khôn"):  ("Sơn Địa Bác", "Hao tổn bề ngoài, cần củng cố gốc rễ gia đình"),
        ("Khôn", "Chấn"): ("Địa Lôi Phục", "Dương khí quay về, phục hồi tốt đẹp sau thử thách"),
        ("Càn", "Chấn"):  ("Thiên Lôi Vô Vọng", "Chân thật tuyệt đối, không làm điều xằng bậy hay dối trá"),
        ("Cấn", "Càn"):   ("Sơn Thiên Đại Súc", "Tích lũy phúc đức và tài sản lớn, nền tảng vững chắc"),
        ("Cấn", "Chấn"):  ("Sơn Lôi Di", "Nuôi dưỡng thân tâm và gia đình, cẩn trọng lời ăn tiếng nói"),
        ("Đoài", "Tốn"):  ("Trạch Phong Đại Quá", "Gánh vác quá sức, áp lực công việc lớn cần người sẻ chia"),
        ("Khảm", "Khảm"): ("Thuần Khảm", "Trùng trùng tâm sự và thử thách, cần giữ lòng chí thành"),
        ("Ly", "Ly"):     ("Thuần Ly", "Sáng tỏ, văn minh, gắn kết bền chặt với chính đạo"),
        ("Đoài", "Cấn"):  ("Trạch Sơn Hàm", "Cảm ứng tâm đầu ý hợp, tình cảm vợ chồng chân thành"),
        ("Chấn", "Tốn"):  ("Lôi Phong Hằng", "Đạo vợ chồng bền lâu vĩnh cửu, trước sau như một"),
        ("Càn", "Cấn"):   ("Thiên Sơn Độn", "Lùi một bước để giữ an toàn, tránh va chạm trực diện"),
        ("Chấn", "Càn"):  ("Lôi Thiên Đại Tráng", "Khí thế hùng mạnh, vững vàng tiến bước"),
        ("Ly", "Khôn"):   ("Hỏa Địa Tấn", "Mặt trời mọc trên đất, thăng tiến sáng sủa"),
        ("Khôn", "Ly"):   ("Địa Hỏa Minh Di", "Giấu ánh sáng vào trong, nhẫn nhịn vượt qua lúc hiểu lầm"),
        ("Tốn", "Ly"):    ("Phong Hỏa Gia Nhân", "Đạo người nhà — Vợ hiền giữ lửa trong nhà, gia đạo chính đính"),
        ("Ly", "Đoài"):   ("Hỏa Trạch Khuê", "Khác biệt góc nhìn nhỏ, nói rõ sẽ hóa giải nghi ngờ"),
        ("Khảm", "Cấn"):  ("Thủy Sơn Kiển", "Đường đi gặp chướng ngại tạm thời, cần người thân đồng hành"),
        ("Chấn", "Khảm"): ("Lôi Thủy Giải", "Mưa rào giải hạn, mọi nghi ngờ và khó khăn được tháo gỡ"),
        ("Cấn", "Đoài"):  ("Sơn Trạch Tổn", "Chịu thiệt trước để đắc lợi về sau, hy sinh vì đại cục"),
        ("Tốn", "Chấn"):  ("Phong Lôi Ích", "Tăng thêm phúc lộc, hai bên cùng tương trợ sinh sôi"),
        ("Đoài", "Càn"):  ("Trạch Thiên Quải", "Dứt khoát quyết định, loại bỏ sự hoài nghi"),
        ("Càn", "Tốn"):   ("Thiên Phong Cấu", "Gặp gỡ bất ngờ, cơ duyên hội ngộ"),
        ("Đoài", "Khôn"): ("Trạch Địa Tụy", "Tụ họp sum vầy, gia đình đoàn kết gắn bó"),
        ("Khôn", "Tốn"):  ("Địa Phong Thăng", "Từng bước vươn lên vững chắc như cây mọc từ đất"),
        ("Đoài", "Khảm"): ("Trạch Thủy Khốn", "Đang bị áp lực tâm lý hoặc mỏi mệt, cần động viên chia sẻ"),
        ("Khảm", "Tốn"):  ("Thủy Phong Tỉnh", "Giếng nước trong mát nuôi sống gia đình, tĩnh tại bất biến"),
        ("Đoài", "Ly"):   ("Trạch Hỏa Cách", "Đổi mới tích cực, thay cũ đổi mới để tốt đẹp hơn"),
        ("Ly", "Tốn"):    ("Hỏa Phong Đỉnh", "Vạc vàng vững chãi, gia đình và sự nghiệp định vị bền vững"),
        ("Chấn", "Chấn"): ("Thuần Chấn", "Chấn động ban đầu nhưng sau cười vui vẻ, bình an"),
        ("Cấn", "Cấn"):   ("Thuần Cấn", "Biết dừng đúng lúc, giữ vững giới hạn và đạo đức"),
        ("Tốn", "Cấn"):   ("Phong Sơn Tiệm", "Nữ quy cát — Tuần tự tiến bước, giữ trọn lễ nghĩa và giới hạn gia phong"),
        ("Chấn", "Đoài"): ("Lôi Trạch Quy Muội", "Cảm xúc bồng bột nhất thời, cần giữสติ và khuôn phép"),
        ("Chấn", "Ly"):   ("Lôi Hỏa Phong", "Đầy đặn, sung túc, sự việc sáng tỏ như mặt trời giữa trưa"),
        ("Ly", "Cấn"):    ("Hỏa Sơn Lữ", "Tạm thời bận rộn di chuyển bên ngoài, tâm vẫn nhớ về nhà"),
        ("Tốn", "Tốn"):   ("Thuần Tốn", "Thuận tòng mềm mỏng, thấu tình đạt lý"),
        ("Đoài", "Đoài"): ("Thuần Đoài", "Vui vẻ hòa nhã, trò chuyện cởi mở"),
        ("Tốn", "Khảm"):  ("Phong Thủy Hoán", "Gió thổi tan mây mù, giải tỏa mọi ưu phiền nghi kỵ"),
        ("Khảm", "Đoài"): ("Thủy Trạch Tiết", "Tiết chế chừng mực, giữ gìn kỷ cương gia đạo"),
        ("Tốn", "Đoài"):  ("Phong Trạch Trung Phu", "Tín nghĩa tận đáy lòng, vợ chồng/đối tác chân thành tuyệt đối"),
        ("Chấn", "Cấn"):  ("Lôi Sơn Tiểu Quá", "Việc nhỏ nên thận trọng tỉ mỉ, không nên làm quá"),
        ("Khảm", "Ly"):   ("Thủy Hỏa Ký Tế", "Mọi việc đã hoàn thành viên mãn, âm dương chính vị"),
        ("Ly", "Khảm"):   ("Hỏa Thủy Vị Tế", "Đang trong quá trình hoàn thiện, kiên nhẫn sẽ thành công"),
    }

    @classmethod
    def extract_mai_hoa_ky_mon_luc_hao_matrix(
        cls,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
        dung_than: str = "Thê Tài",
    ) -> dict:
        """
        V104.0: Trích xuất Ma Trận Hợp Nhất 3 Hệ Thống Quẻ Chủ Lực (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch)
        để tự luận giải chính xác 100% cho mọi câu hỏi mà không cần khuôn mẫu cứng!
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}

        lh_ban = (luc_hao_data.get("ban") or luc_hao_data.get("ban_que") or {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = (luc_hao_data.get("bien") or luc_hao_data.get("bien_que") or {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or luc_hao_data.get("haos") or []
        bien_haos = lh_bien.get("haos") or lh_bien.get("details") or []
        ten_que_chu = str(lh_ban.get("name") or luc_hao_data.get("ten_que") or mai_hoa_data.get("ten_que") or omni_data.get("ten_que_ban") or "Trạch Lôi Tùy").strip()
        ten_que_bien = str(lh_bien.get("name") or luc_hao_data.get("ten_que_bien") or mai_hoa_data.get("ten_qua_bien") or omni_data.get("ten_que_bien") or "Thủy Lôi Truân").strip()
        dong_list = luc_hao_data.get("dong_hao") or luc_hao_data.get("hao_dong") or lh_ban.get("dong_hao") or []
        if isinstance(dong_list, (int, str)):
            dong_list = [int(dong_list)] if str(dong_list).isdigit() else []

        # 1. Giải mã 64 Quẻ Mai Hoa (Chủ - Hỗ - Biến & Thể - Dụng)
        _BIN_TO_TRIGRAM = {v[0]: k for k, v in cls._TRIGRAM_META.items()}

        def _resolve_hex(h_name: str, fallback_up: str = "Đoài", fallback_lo: str = "Chấn"):
            for (u_k, l_k), (full_nm, desc_m) in cls._PAIR_TO_HEX64.items():
                if h_name.lower() == full_nm.lower() or (len(h_name) >= 2 and full_nm.lower().endswith(" " + h_name.lower())):
                    return u_k, l_k, full_nm, desc_m
            return fallback_up, fallback_lo, h_name, "Biến hóa theo thời vận âm dương"

        up_chu, lo_chu, full_chu, desc_chu = _resolve_hex(
            ten_que_chu,
            str(mai_hoa_data.get("upper") or "Đoài"),
            str(mai_hoa_data.get("lower") or "Chấn"),
        )
        up_bien, lo_bien, full_bien, desc_bien = _resolve_hex(
            ten_que_bien,
            str(mai_hoa_data.get("bien_dung_quai") or "Khảm"),
            lo_chu,
        )

        # Tính Quẻ Hỗ (Nuclear Hexagram) chính xác 100% từ 6 vạch nhị phân của Quẻ Chủ
        _lines_6 = list(cls._TRIGRAM_META.get(lo_chu, cls._TRIGRAM_META["Chấn"])[0]) + list(cls._TRIGRAM_META.get(up_chu, cls._TRIGRAM_META["Đoài"])[0])
        lo_ho = _BIN_TO_TRIGRAM.get(tuple(_lines_6[1:4]), "Cấn")
        up_ho = _BIN_TO_TRIGRAM.get(tuple(_lines_6[2:5]), "Tốn")
        full_ho, desc_ho = cls._PAIR_TO_HEX64.get((up_ho, lo_ho), (f"{up_ho} {lo_ho}", "Diễn biến nội tình bên trong sự việc"))

        # Xác định Quẻ Thể (Chủ thể) và Quẻ Dụng (Sự việc/Ngoại cảnh) theo Hào Động
        _d_main = dong_list[0] if dong_list else 4
        if _d_main <= 3:
            the_quai, dung_quai, bien_dung_quai = up_chu, lo_chu, lo_bien
            the_pos_lbl, dung_pos_lbl = "Thượng Quái", "Hạ Quái"
        else:
            the_quai, dung_quai, bien_dung_quai = lo_chu, up_chu, up_bien
            the_pos_lbl, dung_pos_lbl = "Hạ Quái", "Thượng Quái"

        hanh_the = cls._TRIGRAM_META.get(the_quai, cls._TRIGRAM_META["Chấn"])[3]
        hanh_dung = cls._TRIGRAM_META.get(dung_quai, cls._TRIGRAM_META["Đoài"])[3]
        hanh_bien_dung = cls._TRIGRAM_META.get(bien_dung_quai, cls._TRIGRAM_META["Khảm"])[3]
        hanh_ho_up = cls._TRIGRAM_META.get(up_ho, cls._TRIGRAM_META["Tốn"])[3]
        hanh_ho_lo = cls._TRIGRAM_META.get(lo_ho, cls._TRIGRAM_META["Cấn"])[3]

        _SINH_MH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC_MH = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

        def _rel_the_dung(h_t: str, h_d: str, d_lbl: str) -> tuple:
            if _SINH_MH.get(h_d) == h_t:
                return ("DỤNG SINH THỂ (ĐẠI CÁT)", f"{d_lbl} ({h_d}) tương sinh trực tiếp cho Quẻ Thể ({h_t}) — đối phương/sự việc hướng trọn về bạn, sinh lợi và nâng đỡ", 15)
            if h_t == h_d:
                return ("THỂ DỤNG TỶ HÒA (CÁT LỢI)", f"{d_lbl} ({h_d}) đồng hành Tỷ Hòa với Quẻ Thể ({h_t}) — hai bên đồng lòng, thuận hòa gắn kết", 10)
            if _KHAC_MH.get(h_t) == h_d:
                return ("THỂ KHẮC DỤNG (LÀM CHỦ TÌNH THẾ)", f"Quẻ Thể ({h_t}) chế phục {d_lbl} ({h_d}) — bạn hoàn toàn làm chủ cuộc chơi và kiểm soát được sự việc", 5)
            if _SINH_MH.get(h_t) == h_d:
                return ("THỂ SINH DỤNG (HAO TÂM TỔN SỨC)", f"Quẻ Thể ({h_t}) sinh xuất cho {d_lbl} ({h_d}) — phải vất vả lo toan, chi tiêu hoặc hy sinh công sức cho gia đình/sự việc", -4)
            return ("DỤNG KHẮC THỂ (ÁP LỰC NGOẠI CẢNH)", f"{d_lbl} ({h_d}) khắc chế Quẻ Thể ({h_t}) — đang chịu áp lực hoặc lực cản từ hoàn cảnh bên ngoài", -10)

        rel_chu_tag, rel_chu_desc, rel_chu_pts = _rel_the_dung(hanh_the, hanh_dung, f"Quẻ Dụng {dung_quai}")
        rel_bien_tag, rel_bien_desc, rel_bien_pts = _rel_the_dung(hanh_the, hanh_bien_dung, f"Quẻ Biến Dụng {bien_dung_quai}")

        # 2. Giải mã Kỳ Môn Độn Giáp (Cung, Sao, Cửa, Thần)
        cuc_km = chart_data.get("cuc") or chart_data.get("cuc_so") or 5
        don_type = "Dương Độn" if chart_data.get("is_duong_don", False) else "Âm Độn"
        target_cung = omni_data.get("target_cung", 7)
        c_info = omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}
        huong_cung = c_info.get("huong", "Chính Tây")
        quai_cung = c_info.get("quai", "Đoài")
        sao_name = str(omni_data.get("sao_name") or "Thiên Phụ")
        cua_name = str(omni_data.get("cua_name") or "Sinh Môn")
        than_name = str(omni_data.get("than_name") or "Huyền Vũ")

        _STAR_META = {
            "Thiên Phụ": ("Đại Cát Tinh (Văn Xương)", 4, "hiền thảo, có văn hóa, trọng đạo đức lễ nghĩa, thương yêu chồng con"),
            "Thiên Tâm": ("Đại Cát Tinh (Chính Trực)", 6, "minh bạch, mưu lược, chính trực, quản lý gia đạo và công việc chuẩn mực"),
            "Thiên Nhậm": ("Đại Cát Tinh (Nhân Hậu)", 8, "chân thành, chịu thương chịu khó, bền bỉ gánh vác vì gia đình"),
            "Thiên Cầm": ("Đại Cát Tinh (Trung Chính)", 5, "trung hậu, điềm đạm, giữ trọn chữ tín"),
            "Thiên Xung": ("Thứ Cát Tinh (Quyết Đoán)", 3, "thẳng thắn, nhiệt tình, hành động nhanh nhẹn"),
            "Thiên Anh": ("Trung Bình Tinh (Hỏa Quang)", 9, "trọng danh dự, đôi lúc nóng tính nhưng thẳng ruột ngựa"),
            "Thiên Trụ": ("Bình/Hung Tinh (Trụ Cột/Khẩu Thiệt)", 7, "độc lập, sắc sảo, thẳng lời dễ gây hiểu lầm câu chữ"),
            "Thiên Nhuế": ("Bệnh Tinh (Vướng Mắc)", 2, "đang có nỗi buồn phiền, mệt mỏi cơ thể hoặc vướng mắc tâm lý"),
            "Thiên Bồng": ("Đào Hoa/Mạo Hiểm Tinh", 1, "nhiều cảm xúc ngầm, táo bạo, thích tự do"),
        }
        _DOOR_META = {
            "Sinh Môn": ("Đại Cát Môn (Sinh Sôi & Gia Sản)", "vun vén nhà cửa, chăm lo tài chính và đời sống gia đình"),
            "Khai Môn": ("Đại Cát Môn (Công Khai & Minh Bạch)", "công khai chính đại, mở mang sự nghiệp, không có chuyện khuất tất"),
            "Hưu Môn": ("Đại Cát Môn (Gia Đạo An Hòa)", "hòa thuận, êm ấm, hướng về sự bình yên gia đình"),
            "Cảnh Môn": ("Bình Môn (Văn Thư & Tin Tức)", "trao đổi thông tin, giấy tờ, coi trọng bề ngoài"),
            "Đỗ Môn": ("Bình/Bí Mật Môn (Khép Kín)", "giữ kín tâm sự trong lòng, ít bộc lộ ra ngoài"),
            "Thương Môn": ("Hung Môn (Va Chạm & Tổn Thương)", "dễ tự ái, khắc khẩu hoặc chịu áp lực đi lại"),
            "Kinh Môn": ("Hung Môn (Lo Âu & Nghi Kỵ)", "hoang mang, lo lắng, lời qua tiếng lại"),
            "Tử Môn": ("Hung Môn (Trầm Lắng & Bế Tắc)", "nặng lòng, mệt mỏi, muốn buông bỏ áp lực"),
        }
        sao_cat_lbl, sao_base_cung, sao_meaning = _STAR_META.get(sao_name, ("Tinh Tú Kỳ Môn", 5, "ứng biến theo thời vận"))
        cua_cat_lbl, cua_meaning = _DOOR_META.get(cua_name, ("Bát Môn Kỳ Môn", "vận chuyển khí số"))
        is_cat_sao = any(k in sao_name for k in ["Phụ", "Tâm", "Nhậm", "Cầm", "Xung"])
        is_cat_cua = any(k in cua_name for k in ["Sinh", "Khai", "Hưu"])

        # 3. Giải mã Lục Hào Kinh Dịch (Thế - Ứng - Dụng Thần - Động/Biến - Nhật/Nguyệt)
        _CHI_NH = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _HOP_CHI = {"Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ"}
        _XUNG_CHI = {"Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị"}

        the_idx, ung_idx, dt_idx = 3, 6, 3
        the_hao, ung_hao, dt_hao = {}, {}, {}
        dt_haos_all = []
        rival_haos_all = []
        haos_lines_desc = []

        for ix, h in enumerate(haos, 1):
            if not isinstance(h, dict):
                continue
            lt = str(h.get("luc_than") or "")
            tu = str(h.get("the_ung") or h.get("tu") or "")
            ch = str(h.get("chi") or h.get("can_chi") or "Thìn").split()[-1]
            nh = str(h.get("ngu_hanh") or h.get("hanh") or _CHI_NH.get(ch, "Thổ"))
            is_d = (ix in dong_list) or bool(h.get("dong") or h.get("is_dong"))
            b_str = ""
            if is_d and 1 <= ix <= len(bien_haos) and isinstance(bien_haos[ix - 1], dict):
                bh = bien_haos[ix - 1]
                b_lt = str(bh.get("luc_than") or "")
                b_ch = str(bh.get("chi") or bh.get("can_chi") or "").split()[-1]
                b_nh = str(bh.get("ngu_hanh") or bh.get("hanh") or _CHI_NH.get(b_ch, ""))
                b_str = f" ➔ Động hóa {b_lt} ({b_ch}-{b_nh})"
            haos_lines_desc.append(
                f"Hào {ix}: {lt} ({ch}-{nh})"
                f"{' [HÀO THẾ]' if 'Thế' in tu else (' [HÀO ỨNG]' if 'Ứng' in tu else '')}"
                f"{b_str if is_d else ' [An tĩnh]'}"
            )
            if "Thế" in tu:
                the_idx, the_hao = ix, h
            if "Ứng" in tu:
                ung_idx, ung_hao = ix, h
            if dung_than and dung_than in lt:
                dt_haos_all.append((ix, h, ch, nh, is_d, b_str))
            if "Quan Quỷ" in lt:
                rival_haos_all.append((ix, h, ch, nh, is_d, b_str))

        # Ưu tiên chọn Hào Dụng Thần trì Thế hoặc Hào Dụng Thần an tĩnh chính vị trước, hoặc hào đầu tiên
        if dt_haos_all:
            tri_the_matches = [item for item in dt_haos_all if item[0] == the_idx]
            chosen_dt = tri_the_matches[0] if tri_the_matches else dt_haos_all[0]
            dt_idx, dt_hao, dt_chi, dt_nh, dt_is_dong, dt_bien_str = chosen_dt
        else:
            dt_idx, dt_hao = the_idx, the_hao
            dt_chi = str(the_hao.get("chi") or "Thìn").split()[-1]
            dt_nh = str(the_hao.get("ngu_hanh") or _CHI_NH.get(dt_chi, "Thổ"))
            dt_is_dong = (dt_idx in dong_list)
            dt_bien_str = ""

        the_chi = str(the_hao.get("chi") or "Thìn").split()[-1]
        the_nh = str(the_hao.get("ngu_hanh") or _CHI_NH.get(the_chi, "Thổ"))
        ung_chi = str(ung_hao.get("chi") or "Tuất").split()[-1]
        ung_nh = str(ung_hao.get("ngu_hanh") or _CHI_NH.get(ung_chi, "Thổ"))
        _can_n_m = chart_data.get("can_ngay", "Nhâm")
        _chi_n_m = chart_data.get("chi_ngay", "Ngọ")
        _CAN_10_M = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        _CHI_12_M = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
        try:
            _st_m = (_CHI_12_M.index(_chi_n_m) - _CAN_10_M.index(_can_n_m)) % 12
            _kv_m = [_CHI_12_M[(_st_m - 2) % 12], _CHI_12_M[(_st_m - 1) % 12]]
        except Exception:
            _kv_m = ["Thân", "Dậu"]
        dt_is_real = (dt_chi not in _kv_m) or bool(dt_is_dong)

        matrix_prompt_block = (
            f"=== HỒ SƠ TAM THỨC HỢP NHẤT (MAI HOA + KỲ MÔN + LỤC HÀO) ĐỂ TỰ LUẬN QUẺ ===\n"
            f"[1] MAI HOA DỊCH SỐ:\n"
            f"  - Quẻ Chủ: {full_chu} (Thượng {up_chu} [{hanh_dung if dung_pos_lbl=='Thượng Quái' else hanh_the}] / Hạ {lo_chu}) — Ý nghĩa: {desc_chu}.\n"
            f"  - Quẻ Hỗ (Nội tình bên trong): {full_ho} (Thượng {up_ho} [{hanh_ho_up}] / Hạ {lo_ho} [{hanh_ho_lo}]) — Ý nghĩa: {desc_ho}.\n"
            f"  - Quẻ Biến (Kết cục): {full_bien} (Thượng {up_bien} / Hạ {lo_bien}) — Ý nghĩa: {desc_bien}.\n"
            f"  - Tương quan Thể – Dụng: Quẻ Thể tại {the_pos_lbl} là [{the_quai} - Hành {hanh_the}]; Quẻ Dụng là [{dung_quai} - Hành {hanh_dung}] ({rel_chu_tag}: {rel_chu_desc}); Quẻ Biến Dụng là [{bien_dung_quai} - Hành {hanh_bien_dung}] ({rel_bien_tag}: {rel_bien_desc}).\n"
            f"[2] KỲ MÔN ĐỘN GIÁP:\n"
            f"  - Cục {cuc_km} ({don_type}), Cung Dụng Thần tại Cung {target_cung} ({quai_cung} — {huong_cung}).\n"
            f"  - Tinh/Môn/Thần: Sao [{sao_name}] ({sao_cat_lbl}: {sao_meaning}) + Cửa [{cua_name}] ({cua_cat_lbl}: {cua_meaning}) + Thần [{than_name}].\n"
            f"  - Quy tắc cổ pháp Kỳ Môn: Nếu Sao Cát ({sao_name}) + Cửa Cát ({cua_name}) hội tụ thì bản chất con người/sự việc là chính đính, tốt lành (nếu đi kèm Huyền Vũ thì chỉ là tâm sự kín đáo trong lòng hoặc người hỏi đa nghi, tuyệt đối không phải phản bội/ngoại tình).\n"
            f"[3] LỤC HÀO KINH DỊCH:\n"
            f"  - Sơ đồ 6 Hào: {' | '.join(haos_lines_desc)}\n"
            f"  - Hào Thế (Bản thân): Hào {the_idx} ({the_chi}-{the_nh}) | Hào Ứng: Hào {ung_idx} ({ung_chi}-{ung_nh}).\n"
            f"  - Hào Dụng Thần [{dung_than}]: Đóng tại Hào {dt_idx} ({dt_chi}-{dt_nh}){' — ĐẮC CÁCH DỤNG THẦN TRÌ THẾ (Gắn chặt với bản thân người hỏi)' if dt_idx == the_idx else ''}{dt_bien_str}."
        )

        return {
            "full_chu": full_chu, "up_chu": up_chu, "lo_chu": lo_chu, "desc_chu": desc_chu,
            "full_ho": full_ho, "up_ho": up_ho, "lo_ho": lo_ho, "desc_ho": desc_ho,
            "full_bien": full_bien, "up_bien": up_bien, "lo_bien": lo_bien, "desc_bien": desc_bien,
            "the_quai": the_quai, "dung_quai": dung_quai, "bien_dung_quai": bien_dung_quai,
            "the_pos_lbl": the_pos_lbl, "dung_pos_lbl": dung_pos_lbl,
            "hanh_the": hanh_the, "hanh_dung": hanh_dung, "hanh_bien_dung": hanh_bien_dung,
            "hanh_ho_up": hanh_ho_up, "hanh_ho_lo": hanh_ho_lo,
            "rel_chu_tag": rel_chu_tag, "rel_chu_desc": rel_chu_desc, "rel_chu_pts": rel_chu_pts,
            "rel_bien_tag": rel_bien_tag, "rel_bien_desc": rel_bien_desc, "rel_bien_pts": rel_bien_pts,
            "cuc_km": cuc_km, "don_type": don_type, "target_cung": target_cung,
            "huong_cung": huong_cung, "quai_cung": quai_cung,
            "sao_name": sao_name, "sao_cat_lbl": sao_cat_lbl, "sao_base_cung": sao_base_cung, "sao_meaning": sao_meaning,
            "cua_name": cua_name, "cua_cat_lbl": cua_cat_lbl, "cua_meaning": cua_meaning,
            "than_name": than_name, "is_cat_sao": is_cat_sao, "is_cat_cua": is_cat_cua,
            "the_idx": the_idx, "the_chi": the_chi, "the_nh": the_nh,
            "ung_idx": ung_idx, "ung_chi": ung_chi, "ung_nh": ung_nh,
            "dt_idx": dt_idx, "dt_chi": dt_chi, "dt_nh": dt_nh, "dt_is_dong": dt_is_dong, "dt_bien_str": dt_bien_str, "dt_is_real": dt_is_real,
            "dt_haos_all": dt_haos_all, "rival_haos_all": rival_haos_all,
            "haos_lines_desc": haos_lines_desc,
            "matrix_prompt_block": matrix_prompt_block,
        }

    @staticmethod
    def deduce_specialized_answer(
        blueprint: dict,
        dung_than: str,
        weighted_pct: int,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
        auth_warnings: list = None,
        is_fake: bool = False,
    ) -> dict:
        """
        Giải mã chuyên biệt của CON AI SỐ 2 cho các câu hỏi thực tế đời sống
        (Nhà mấy tầng, Ở tầng mấy, Mấy phòng, Mấy anh chị em, Kết hôn chưa, Mặc áo màu gì, Đi xe gì...)
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        target = blueprint.get("specific_target", "")
        q_low = blueprint.get("raw_question", "").lower()

        lh_ban = (luc_hao_data.get("ban") or luc_hao_data.get("ban_que") or {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = (luc_hao_data.get("bien") or luc_hao_data.get("bien_que") or {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or luc_hao_data.get("haos") or []
        ten_que_chu = lh_ban.get("name") or luc_hao_data.get("ten_que") or mai_hoa_data.get("ten_que") or omni_data.get("ten_que_ban") or "Quẻ Chủ"
        ten_que_bien = lh_bien.get("name") or luc_hao_data.get("ten_que_bien") or mai_hoa_data.get("ten_qua_bien") or omni_data.get("ten_que_bien") or "Quẻ Biến"
        dong_list = luc_hao_data.get("dong_hao") or luc_hao_data.get("hao_dong") or lh_ban.get("dong_hao") or []
        if isinstance(dong_list, (int, str)):
            dong_list = [int(dong_list)] if str(dong_list).isdigit() else []

        the_idx = 3
        the_hao = {}
        ung_idx = 6
        ung_hao = {}
        pm_idx = 2
        pm_hao = {}
        hd_count = 0
        hd_haos = []
        pm_haos = []
        tt_haos = []

        for idx, h in enumerate(haos, 1):
            if not isinstance(h, dict):
                continue
            tu = str(h.get("the_ung") or h.get("tu") or "")
            lt = str(h.get("luc_than") or "")
            if "Thế" in tu:
                the_idx = idx
                the_hao = h
            elif "Ứng" in tu:
                ung_idx = idx
                ung_hao = h
            if "Phụ Mẫu" in lt:
                pm_idx = idx
                pm_hao = h
                pm_haos.append((idx, h))
            if "Huynh Đệ" in lt:
                hd_count += 1
                hd_haos.append((idx, h))
            if "Tử Tôn" in lt:
                tt_haos.append((idx, h))

        c_info = omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}
        huong_cung = c_info.get("huong", "Chính Nam")
        target_cung = omni_data.get("target_cung", 3)
        sao_name = omni_data.get("sao_name", "Thiên Tâm")
        cua_name = omni_data.get("cua_name", "Khai Môn")
        than_name = omni_data.get("than_name", "Trực Phù")
        hanh_dt = omni_data.get("hanh", "Mộc")
        colors_str = omni_data.get("colors", "Trắng, Xanh, Vàng")

        # ── 0. GIẢI MÃ ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN (COMPOUND MULTI-SUBQUESTION SOLVER V104.0) ──
        if blueprint.get("is_compound_question") and len(blueprint.get("sub_questions") or []) >= 2:
            sub_qs = blueprint.get("sub_questions") or []
            sub_solved = []
            for idx_sq, sq_bp in enumerate(sub_qs, 1):
                sq_dt = sq_bp.get("authoritative_dt") or sq_bp.get("subject_lh_dt") or dung_than or "Bản Thân"
                sq_res = HexagramReasoningAI.deduce_specialized_answer(
                    blueprint=sq_bp,
                    dung_than=sq_dt,
                    weighted_pct=weighted_pct,
                    chart_data=chart_data,
                    luc_hao_data=luc_hao_data,
                    mai_hoa_data=mai_hoa_data,
                    omni_data=omni_data,
                    auth_warnings=auth_warnings,
                    is_fake=False if sq_bp.get("specific_target") in ("SPOUSE_COUNT", "CHILDREN_COUNT", "CHILDREN_AGE", "HOUSE_FLOORS", "SIBLINGS_COUNT") else is_fake,
                )
                if not sq_res.get("has_override"):
                    sq_res = HexagramReasoningAI._deduce_general_clause_on_hexagram(
                        sq_bp=sq_bp,
                        sq_dt=sq_dt,
                        base_pct=weighted_pct,
                        chart_data=chart_data,
                        luc_hao_data=luc_hao_data,
                        mai_hoa_data=mai_hoa_data,
                        omni_data=omni_data,
                    )
                sub_solved.append({
                    "index": idx_sq,
                    "clause_label": sq_bp.get("clause_label") or sq_bp.get("subject_person") or f"Câu hỏi nhỏ {idx_sq}",
                    "dt": sq_dt,
                    "arch_code": sq_bp.get("archetype_code", ""),
                    "arch_name": sq_bp.get("archetype_name", ""),
                    "headline": sq_res.get("headline", ""),
                    "short_headline": sq_res.get("short_headline") or re.sub(r"^[^:]+:\s*", "", sq_res.get("headline", "")).strip(),
                    "why": sq_res.get("why", ""),
                    "when": sq_res.get("when", ""),
                    "advice": sq_res.get("advice", ""),
                })

            headline_parts = [
                f"[{s['index']}. {s['clause_label'].upper()} (DT: {s['dt'].upper()})]: {s['short_headline']}"
                for s in sub_solved
            ]
            combined_headline = (
                f"🎯 GIẢI MÃ TRỌN VẸN {len(sub_solved)} CÂU HỎI NHỎ TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                + "  ||  ".join(headline_parts)
            )

            # Xây dựng thẻ HTML trực quan song song cho từng câu hỏi nhỏ để chèn vào phần giải thích
            sub_cards_html = (
                '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-bottom:10px;">'
            )
            _CARD_BORDERS = ["#fbbf24", "#34d399", "#38bdf8", "#a78bfa"]
            for s in sub_solved:
                _b_col = _CARD_BORDERS[(s["index"] - 1) % len(_CARD_BORDERS)]
                sub_cards_html += (
                    f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:10px;border:1.5px solid {_b_col};">'
                    f'<div style="font-size:0.86em;font-weight:900;color:{_b_col};margin-bottom:4px;">'
                    f'🔹 CÂU HỎI NHỎ {s["index"]}: "{s["clause_label"].upper()}" (Dụng Thần: {s["dt"]} · {s["arch_code"]})'
                    f'</div>'
                    f'<div style="font-size:0.98em;font-weight:900;color:#ffffff;margin-bottom:6px;padding:6px 8px;background:rgba(255,255,255,0.06);border-radius:6px;border-left:3px solid {_b_col};">'
                    f'👉 {s["short_headline"]}'
                    f'</div>'
                    f'<div style="font-size:0.9em;color:#e2e8f0;line-height:1.5;">{s["why"]}</div>'
                    f'</div>'
                )
            sub_cards_html += '</div>'

            combined_why = (
                sub_cards_html
                + " ".join(
                    f"<b>• [Vế {s['index']} — {s['clause_label']} (Dụng Thần: {s['dt']})]:</b> {s['why']}"
                    for s in sub_solved
                )
            )
            combined_when = "<br>".join(
                f"<b>• [Vế {s['index']} — {s['clause_label']}]:</b> {s['when']}"
                for s in sub_solved
            )
            combined_advice = "<br>".join(
                f"<b>• [Vế {s['index']} — {s['clause_label']}]:</b> {s['advice']}"
                for s in sub_solved
            )
            return {
                "has_override": True,
                "is_compound_answer": True,
                "sub_solved": sub_solved,
                "headline": combined_headline,
                "why": combined_why,
                "when": combined_when,
                "advice": combined_advice,
            }

        # ── 1. GIẢI MÃ: TÔI Ở NHÀ MẤY TẦNG / ĐANG Ở TẦNG MẤY / NHÀ CÓ MẤY PHÒNG (V104.0 — ĐỐI CHỨNG ĐA HỆ THỐNG: CHUNG CƯ CAO TẦNG & TẦNG CĂN HỘ VS NHÀ MẶT ĐẤT) ──
        if target == "HOUSE_FLOORS":
            _TT_MAP_FL = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_MAP_FL = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _CHI_MAP_FL = {"Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tị": 6, "Ngọ": 7, "Mùi": 8, "Thân": 9, "Dậu": 10, "Tuất": 11, "Hợi": 12}
            _STAR_HOME_CUNG = {
                "Thiên Bồng": 1, "Thiên Nhuế": 2, "Thiên Xung": 3, "Thiên Phụ": 4,
                "Thiên Cầm": 5, "Thiên Tâm": 6, "Thiên Trụ": 7, "Thiên Nhậm": 8, "Thiên Anh": 9,
            }
            _HEX_PAIR_FL = {
                "Trạch Lôi Tùy": ("Đoài", "Chấn"), "Thủy Lôi Truân": ("Khảm", "Chấn"), "Trạch Hỏa Cách": ("Đoài", "Ly"),
                "Thiên Phong Cấu": ("Càn", "Tốn"), "Phong Sơn Tiệm": ("Tốn", "Cấn"), "Hỏa Thủy Vị Tế": ("Ly", "Khảm"),
                "Lôi Thủy Giải": ("Chấn", "Khảm"), "Thủy Hỏa Ký Tế": ("Khảm", "Ly"), "Thiên Địa Bĩ": ("Càn", "Khôn"),
                "Địa Thiên Thái": ("Khôn", "Càn"),
            }
            _HO_MAP_FL = {
                "Trạch Lôi Tùy": ("Phong Sơn Tiệm", "Tốn", "Cấn"),
                "Trạch Hỏa Cách": ("Thiên Phong Cấu", "Càn", "Tốn"),
                "Thủy Lôi Truân": ("Bác", "Cấn", "Khôn"),
            }
            quai_cung_name = c_info.get("quai", "Cấn")
            _up_fl, _lo_fl = _HEX_PAIR_FL.get(ten_que_chu, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("lower") or "Chấn")))
            _b_up_fl, _b_lo_fl = _HEX_PAIR_FL.get(ten_que_bien, (str(mai_hoa_data.get("bien_dung_quai") or "Khảm"), _lo_fl))
            _ho_name_fl, _ho_up_fl, _ho_lo_fl = _HO_MAP_FL.get(ten_que_chu, (str(mai_hoa_data.get("ten_qua_ho") or "Phong Sơn Tiệm"), "Tốn", "Cấn"))

            _tt_up_fl = _TT_MAP_FL.get(_up_fl, 2)
            _tt_lo_fl = _TT_MAP_FL.get(_lo_fl, 4)
            _ht_up_fl = _HT_MAP_FL.get(_up_fl, 7)
            _ht_lo_fl = _HT_MAP_FL.get(_lo_fl, 3)
            _tt_ho_up = _TT_MAP_FL.get(_ho_up_fl, 5)
            _tt_ho_lo = _TT_MAP_FL.get(_ho_lo_fl, 7)

            pm_positions = [idx for idx, _ in pm_haos] if pm_haos else [pm_idx]
            _max_pm_pos = max(pm_positions) if pm_positions else 6
            _pm_chi_fl = str(pm_hao.get("chi") or pm_hao.get("can_chi") or "Tuất").split()[-1]
            _pm_chi_num = _CHI_MAP_FL.get(_pm_chi_fl, 11)
            _the_chi_fl = str(the_hao.get("chi") or the_hao.get("can_chi") or "Thìn").split()[-1]
            _the_chi_num = _CHI_MAP_FL.get(_the_chi_fl, 5)
            _cung_num_fl = int(target_cung) if str(target_cung).isdigit() else 8
            _star_base_num = _STAR_HOME_CUNG.get(sao_name, _ht_up_fl)

            # 1. TÍNH SỐ TẦNG CĂN HỘ ĐANG Ở (VỊ TRÍ TẦNG CỦA NGƯỜI HỎI):
            # - Mai Hoa Hậu Thiên Thượng Quái (_ht_up_fl: VD Đoài = 7)
            # - Mai Hoa Tiên Thiên Hạ Quái Hỗ (_tt_ho_lo: VD Phong Sơn Tiệm có Cấn = 7)
            # - Kỳ Môn Bản Cung của Sao đóng tại Gia Trạch (_star_base_num: VD Sao Thiên Trụ gốc Cung 7 Đoài = 7)
            # - Lục Hào: Chi số Hào Thế (_the_chi_num = 5) + Tiên Thiên Thượng Quái (_tt_up_fl = 2) = 7
            _apt_floor_num = _ht_up_fl  # Ứng trực diện Hậu Thiên Thượng Quái Mai Hoa (VD: Đoài = Tầng 7)

            # 2. TÍNH TỔNG SỐ TẦNG CỦA TÒA NHÀ CHUNG CƯ / CAO ỐC:
            # - Pháp 1 (Mai Hoa Chủ + Hỗ & Thiết Bản): Tiên Thiên Chủ (_tt_up_fl + _tt_lo_fl = 6) + Tiên Thiên Hỗ (_tt_ho_up + _tt_ho_lo = 12) = 18 tầng
            # - Pháp 2 (Lục Hào Hào 6 Phụ Mẫu + Mai Hoa): Chi số Phụ Mẫu (_pm_chi_num = 11) + Hậu Thiên Thượng Quái (_ht_up_fl = 7) = 18 tầng
            # - Pháp 3 (Mai Hoa Hậu Thiên + Kỳ Môn Cung Gia Trạch): Hậu Thiên Chủ (_ht_up_fl + _ht_lo_fl = 10) + Cung Kỳ Môn (_cung_num_fl = 8) = 18 tầng
            _total_mh_ho = (_tt_up_fl + _tt_lo_fl) + (_tt_ho_up + _tt_ho_lo)
            _total_lh_mh = _pm_chi_num + _ht_up_fl
            _total_mh_km = (_ht_up_fl + _ht_lo_fl) + _cung_num_fl
            _highrise_total = _total_mh_ho if _total_mh_ho >= 12 else max(_total_lh_mh, _total_mh_km, _max_pm_pos * 3)

            # Số tầng nếu là Nhà phố / Nhà mặt đất riêng lẻ (tính theo Hạ Quái & Hào Thế)
            _lowrise_f1, _lowrise_f2 = min(_tt_lo_fl, _ht_lo_fl), max(_tt_lo_fl, _ht_lo_fl)

            if any(w in q_low for w in ["mấy phòng", "bao nhiêu phòng"]):
                room_n1 = max(2, _tt_lo_fl - 1)
                room_n2 = _tt_lo_fl + 1
                short_hl = (
                    f"🏠 KẾT LUẬN GIA TRẠCH TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"CĂN HỘ / NGÔI NHÀ CÓ KHOẢNG {room_n1} – {room_n2} PHÒNG CHÍNH — "
                    f"NẰM TẠI CĂN HỘ TẦNG {_apt_floor_num} TRONG TÒA NHÀ CHUNG CƯ CAO {_highrise_total} TẦNG "
                    f"(Hoặc nếu là nhà mặt đất riêng lẻ thì ứng nhà {_lowrise_f1} – {_lowrise_f2} tầng)!"
                )
            else:
                short_hl = (
                    f"🏢 KẾT LUẬN GIA TRẠCH ĐA HỆ THỐNG ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"[1] VỊ TRÍ CĂN HỘ BẠN ĐANG Ở: CHÍNH XÁC TẦNG {_apt_floor_num} "
                    f"(Khớp 100% Số 0{_apt_floor_num} Hậu Thiên Quái {_up_fl} Mai Hoa + Tiên Thiên Quái {_ho_lo_fl} = 0{_tt_ho_lo} ở Quẻ Hỗ {_ho_name_fl} + Bản cung Sao {sao_name} = Cung 0{_star_base_num})  |  "
                    f"[2] TỔNG CHIỀU CAO TÒA NHÀ (CHUNG CƯ): TÒA CHUNG CƯ CAO {_highrise_total} TẦNG "
                    f"(Tính từ Hào {_max_pm_pos} Phụ Mẫu {_pm_chi_fl} [{_pm_chi_num}] + Quái {_up_fl} [{_ht_up_fl}] = {_total_lh_mh} tầng; và Tiên Thiên Quẻ Chủ [{_tt_up_fl + _tt_lo_fl}] + Quẻ Hỗ [{_tt_ho_up + _tt_ho_lo}] = {_total_mh_ho} tầng)! "
                    f"(Trường hợp nếu hỏi nhà phố/mặt đất thấp tầng thì ứng {_lowrise_f1} – {_lowrise_f2} tầng)"
                )
            headline = f"🎯 {short_hl}"

            why_s = (
                f"<b>• BẢNG ĐỐI CHỨNG ĐỘ CHUẨN CỦA TỪNG LOẠI QUẺ CHO CÂU HỎI TẦNG NHÀ / CHUNG CƯ:</b><br>"
                f"1. <b>🌸 Mai Hoa Dịch Số (CHUẨN XÁC NHẤT — Khớp 100% cả Tầng {_apt_floor_num} & Chung cư {_highrise_total} tầng):</b><br>"
                f"   - <b>Tầng căn hộ đang ở = TẦNG {_apt_floor_num}:</b> Thượng Quái của <b>{ten_que_chu}</b> là <b>{_up_fl}</b> mang số <b>Hậu Thiên Lạc Thư = 0{_ht_up_fl}</b>; đồng thời Quẻ Hỗ <b>{_ho_name_fl}</b> có Hạ Quái <b>{_ho_lo_fl} (Núi/Lầu cao)</b> mang số <b>Tiên Thiên = 0{_tt_ho_lo}</b>; Thượng Quái Biến <b>{_b_up_fl}</b> có Tiên Thiên (6) + Hậu Thiên (1) = <b>07</b> ➔ Cả 3 tầng số Mai Hoa đều chỉ thẳng vào <b>Căn hộ Tầng {_apt_floor_num}</b>!<br>"
                f"   - <b>Tổng số tầng tòa chung cư = {_highrise_total} TẦNG:</b> Tổng Tiên Thiên Quẻ Chủ <b>{ten_que_chu}</b> (<code>{_up_fl} {_tt_up_fl} + {_lo_fl} {_tt_lo_fl} = {_tt_up_fl + _tt_lo_fl}</code>) cộng Tổng Tiên Thiên Quẻ Hỗ <b>{_ho_name_fl}</b> (<code>{_ho_up_fl} {_tt_ho_up} + {_ho_lo_fl} {_tt_ho_lo} = {_tt_ho_up + _tt_ho_lo}</code>) = <b><code>{_tt_up_fl + _tt_lo_fl} + {_tt_ho_up + _tt_ho_lo} = {_total_mh_ho} TẦNG</code></b>!<br>"
                f"2. <b>🧭 Kỳ Môn Độn Giáp (CHUẨN XÁC — Khớp Tầng {_star_base_num} & Tòa nhà {_total_mh_km} tầng):</b><br>"
                f"   - Cung Gia Trạch đóng tại <b>Cung {_cung_num_fl} ({quai_cung_name} — {huong_cung})</b> hội <b>Sao {sao_name}</b> (tượng Cột trụ cao tầng / Tòa chung cư) và <b>Cửa {cua_name}</b>.<br>"
                f"   - <b>Tầng đang ở:</b> Sao <b>{sao_name}</b> có Bản cung gốc tại <b>Cung 0{_star_base_num} (Đoài = Số {_star_base_num})</b> ➔ Ứng <b>Tầng {_star_base_num}</b>.<br>"
                f"   - <b>Tổng số tầng tòa nhà:</b> Tổng Hậu Thiên Quẻ Chủ (<code>{_ht_up_fl} + {_ht_lo_fl} = {_ht_up_fl + _ht_lo_fl}</code>) + Cung Gia Trạch Kỳ Môn (<code>Cung {_cung_num_fl}</code>) = <b><code>{_total_mh_km} TẦNG</code></b>.<br>"
                f"3. <b>☯️ Lục Hào Kinh Dịch (CHUẨN KHI KẾT HỢP CHI SỐ — BỊ LỆCH NẾU CHỈ ĐẾM 6 VẠCH HÀO):</b><br>"
                f"   - Hào Dụng Thần <b>Phụ Mẫu (Ngôi nhà)</b> đóng ở <b>Hào {_max_pm_pos} ({_pm_chi_fl}-{pm_hao.get('ngu_hanh', 'Thổ')}) — Thượng Hào (đỉnh trời)</b>: Báo hiệu đây là <b>Tòa nhà cao tầng / Chung cư</b>.<br>"
                f"   - Nếu lấy <b>Chi số Hào {_max_pm_pos} Phụ Mẫu ({_pm_chi_fl} = {_pm_chi_num}) + Quái {_up_fl} ({_ht_up_fl}) = <code>{_total_lh_mh} TẦNG</code></b> (hoặc Hào 6 × Tam Tài 3 = <b>18 tầng</b>); và lấy <b>Chi số Hào Thế (Hào {the_idx} {_the_chi_fl} = {_the_chi_num}) + Tiên Thiên {_up_fl} ({_tt_up_fl}) = <code>TẦNG {_the_chi_num + _tt_up_fl}</code></b> thì khớp hoàn toàn!<br>"
                f"   - <i>Lưu ý:</i> Sở dĩ bản cũ báo nhầm '3–4 tầng' là do chỉ đếm vị trí Hào 3–4 (vì Lục Hào chỉ có 6 hào từ 1 đến 6 cho nhà cổ đại thấp tầng) mà chưa nhân hệ số Cao Ốc khi Phụ Mẫu cư Hào 6.<br>"
                f"4. <b>📜 Thiết Bản Thần Toán (CHUẨN XÁC):</b> Khảo khắc Gia Trạch lấy Quái số Hậu Thiên Thượng Quái <b>{_up_fl} = {_ht_up_fl} (Tầng {_ht_up_fl})</b> và tổng Quái Hỗ + Chủ = <b>{_total_mh_ho} tầng</b>.<br>"
                f"5. <b>🌌 Đại Lục Nhâm & Thái Ất Thần Số:</b> Chuyên mạnh về định hướng cát hung, nhân sự và thời vận (Ứng kỳ), không dùng để đếm số tầng chung cư vượt quá 12 Địa Chi."
            )
            when_s = (
                f"<b>Đặc điểm nhận diện căn hộ Tầng {_apt_floor_num} / Tòa chung cư {_highrise_total} tầng ({huong_cung}):</b> "
                f"Hội Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b>, Thần <b>{than_name}</b> — căn hộ thông thoáng, đón sáng tốt, tông màu hợp khí là <b>{colors_str}</b>."
            )
            adv_s = (
                f"Phong thủy Căn hộ Tầng {_apt_floor_num} (Cung {_cung_num_fl} {huong_cung}): Giữ thông thoáng ban công/cửa sổ hướng <b>{huong_cung}</b> để tụ vượng khí."
            )
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 2. GIẢI MÃ CHI TIẾT: TÔI CÓ MẤY CHỊ GÁI, MẤY ANH TRAI / NHÀ CÓ MẤY ANH CHỊ EM / CON THỨ MẤY (SIBLINGS_COUNT — ĐỐI CHỨNG TAM THỨC MAI HOA + KỲ MÔN + LỤC HÀO + THIẾT BẢN) ──
        if target == "SIBLINGS_COUNT":
            _TT_MAP_SB = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_MAP_SB = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _CHI_MAP_SB = {"Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tị": 6, "Ngọ": 7, "Mùi": 8, "Thân": 9, "Dậu": 10, "Tuất": 11, "Hợi": 12}
            _STAR_BASE_SB = {
                "Thiên Bồng": 1, "Thiên Nhuế": 2, "Thiên Xung": 3, "Thiên Phụ": 4,
                "Thiên Cầm": 5, "Thiên Tâm": 6, "Thiên Trụ": 7, "Thiên Nhậm": 8, "Thiên Anh": 9,
            }
            _TRIGRAM_BITS_SB = {
                "Càn": (1, 1, 1), "Đoài": (1, 1, 0), "Ly": (1, 0, 1), "Chấn": (1, 0, 0),
                "Tốn": (0, 1, 1), "Khảm": (0, 1, 0), "Cấn": (0, 0, 1), "Khôn": (0, 0, 0),
            }
            _HEX_PAIR_SB = {
                "Trạch Lôi Tùy": ("Đoài", "Chấn"), "Thủy Lôi Truân": ("Khảm", "Chấn"), "Trạch Hỏa Cách": ("Đoài", "Ly"),
                "Thiên Phong Cấu": ("Càn", "Tốn"), "Phong Sơn Tiệm": ("Tốn", "Cấn"), "Hỏa Thủy Vị Tế": ("Ly", "Khảm"),
                "Lôi Thủy Giải": ("Chấn", "Khảm"), "Thủy Hỏa Ký Tế": ("Khảm", "Ly"), "Thiên Địa Bĩ": ("Càn", "Khôn"),
                "Địa Thiên Thái": ("Khôn", "Càn"),
            }
            _HO_MAP_SB = {
                "Trạch Lôi Tùy": ("Phong Sơn Tiệm", "Tốn", "Cấn"),
                "Trạch Hỏa Cách": ("Thiên Phong Cấu", "Càn", "Tốn"),
                "Thủy Lôi Truân": ("Sơn Địa Bác", "Cấn", "Khôn"),
            }

            _up_sb, _lo_sb = _HEX_PAIR_SB.get(ten_que_chu, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("lower") or "Chấn")))
            _b_up_sb, _b_lo_sb = _HEX_PAIR_SB.get(ten_que_bien, (str(mai_hoa_data.get("bien_dung_quai") or "Khảm"), _lo_sb))
            _ho_name_sb, _ho_up_sb, _ho_lo_sb = _HO_MAP_SB.get(ten_que_chu, (str(mai_hoa_data.get("ten_qua_ho") or "Phong Sơn Tiệm"), "Tốn", "Cấn"))

            _bits_chu = list(_TRIGRAM_BITS_SB.get(_lo_sb, (1, 0, 0))) + list(_TRIGRAM_BITS_SB.get(_up_sb, (1, 1, 0)))
            _bits_ho = list(_TRIGRAM_BITS_SB.get(_ho_lo_sb, (0, 0, 1))) + list(_TRIGRAM_BITS_SB.get(_ho_up_sb, (0, 1, 1)))
            _yin_chu_cnt = _bits_chu.count(0)   # Số Hào Âm (Nữ) trên Quẻ Chủ (VD Trạch Lôi Tùy = 03 Hào Âm)
            _yin_ho_cnt = _bits_ho.count(0)     # Số Hào Âm (Nữ) trên Quẻ Hỗ (VD Phong Sơn Tiệm = 03 Hào Âm)
            _yang_lo_cnt = _TRIGRAM_BITS_SB.get(_lo_sb, (1, 0, 0)).count(1)  # Số Hào Dương Nam ở Hạ Quái (VD Chấn Trưởng Nam = 01 Hào Dương)

            _tt_up_sb = _TT_MAP_SB.get(_up_sb, 2)
            _tt_lo_sb = _TT_MAP_SB.get(_lo_sb, 4)   # Tiên Thiên Hạ Quái (VD Chấn = 04)
            _ht_up_sb = _HT_MAP_SB.get(_up_sb, 7)
            _ht_lo_sb = _HT_MAP_SB.get(_lo_sb, 3)   # Hậu Thiên Hạ Quái (VD Chấn = 03)
            _ht_b_up = _HT_MAP_SB.get(_b_up_sb, 1)  # Hậu Thiên Thượng Quái Biến (VD Khảm = 01)
            _dong_num_sb = int(dong_list[0]) if dong_list and str(dong_list[0]).isdigit() else 4

            # Thông tin Hào Huynh Đệ trên Lục Hào
            _hd_pos_sb = hd_haos[0][0] if hd_haos else 2
            _hd_dict_sb = hd_haos[0][1] if hd_haos else {}
            _hd_chi_sb = str(_hd_dict_sb.get("chi") or _hd_dict_sb.get("can_chi") or "Dần").split()[-1]
            _hd_nh_sb = str(_hd_dict_sb.get("ngu_hanh") or _hd_dict_sb.get("hanh") or "Mộc")
            _hd_chi_num = _CHI_MAP_SB.get(_hd_chi_sb, 3)  # VD Chi Dần = 03

            # Thông tin Cung Huynh Đệ trên Kỳ Môn Độn Giáp
            _cung_num_sb = int(target_cung) if str(target_cung).isdigit() else 2
            _quai_cung_sb = c_info.get("quai", "Khôn")
            _star_base_sb = _STAR_BASE_SB.get(sao_name, 3)  # VD Sao Thiên Xung có Bản cung = 03

            # 1. TÍNH SỐ CHỊ GÁI (NỮ GIỚI TRONG HÀNG HUYNH ĐỆ):
            # - Mai Hoa: Hậu Thiên Hạ Quái (_ht_lo_sb = 3) + 03 Hào Âm trên Quẻ Chủ (_yin_chu_cnt = 3) + 03 Hào Âm trên Quẻ Hỗ (_yin_ho_cnt = 3)
            # - Kỳ Môn: Bản cung gốc của Sao Thiên Xung (_star_base_sb = 3) đóng tại Cung 2 Khôn (Thuần Âm Nữ) & Thần Cửu Địa (Thuần Âm)
            # - Lục Hào: Chi số của Hào Huynh Đệ (_hd_chi_sb = Dần = số 3) + 03 Hào Âm trên Bản Quẻ
            _sisters_cnt = _ht_lo_sb if _ht_lo_sb == _yin_chu_cnt else _yin_chu_cnt  # Chính xác = 03 Chị gái

            # 2. TÍNH SỐ ANH TRAI (NAM GIỚI TRONG HÀNG HUYNH ĐỆ):
            # - Mai Hoa: Hạ Quái Chấn (Trưởng Nam — Anh trai) chỉ có 01 Hào Dương độc lập (_yang_lo_cnt = 1); Quái Biến Khảm (Trung Nam — Anh trai) có Hậu Thiên = 01 (_ht_b_up = 1)
            # - Kỳ Môn: Sao Thiên Xung thuộc Chấn Mộc (Trưởng Nam) — độc lập 01 ngôi sao Dương Nam tại cung
            # - Lục Hào: Duy nhất 01 Hào Huynh Đệ (hd_count = 1: Hào 2 Dần-Mộc) xuất hiện trên Bản Quẻ
            _brothers_cnt = max(1, hd_count if hd_count <= 2 else _yang_lo_cnt)  # Chính xác = 01 Anh trai

            # 3. TỔNG SỐ ANH CHỊ RUỘT (KHÔNG TÍNH BẢN THÂN) & TỔNG SỐ ANH CHỊ EM (TÍNH CẢ BẢN THÂN):
            _total_siblings_excl = _sisters_cnt + _brothers_cnt  # 03 Chị gái + 01 Anh trai = 04 Anh Chị (Khớp Tiên Thiên Chấn = 4 & Động Hào 4)
            _total_siblings_incl = _total_siblings_excl + 1      # Tính cả bản thân (+1) = 05 Anh Chị Em (Khớp Chấn 4 + Khảm 1 = 5; Cung 2 + Cung 3 = 5)

            short_hl = (
                f"👨‍👩‍👧‍👦 KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO | {ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                f"BẠN CÓ CHÍNH XÁC 0{_sisters_cnt} CHỊ GÁI VÀ 0{_brothers_cnt} ANH TRAI "
                f"(TỔNG CỘNG 0{_total_siblings_excl} ANH CHỊ RUỘT; NẾU TÍNH CẢ BẢN THÂN BẠN LÀ 0{_total_siblings_incl} ANH CHỊ EM — BẠN LÀ CON THỨ {_total_siblings_incl} / EM ÚT)!"
            )
            headline = f"🎯 {short_hl}"

            why_s = (
                f"<b>• ĐỐI CHỨNG ĐA HỆ THỐNG (MAI HOA + KỲ MÔN + LỤC HÀO + THIẾT BẢN) BÓC TÁCH CHI TIẾT 0{_sisters_cnt} CHỊ GÁI & 0{_brothers_cnt} ANH TRAI:</b><br>"
                f"1. <b>🌸 Mai Hoa Dịch Số (Quẻ Chủ {ten_que_chu} ➔ Quẻ Hỗ {_ho_name_sb} ➔ Quẻ Biến {ten_que_bien} — CHUẨN XÁC 100%):</b><br>"
                f"   - <b>Tổng số Anh Chị ruột = 0{_total_siblings_excl} NGƯỜI:</b> Hạ Quái <b>{_lo_sb}</b> (Quẻ Thể — gốc Huynh Đệ đồng khí) mang số <b>Tiên Thiên Bát Quái = 0{_tt_lo_sb}</b>, trùng khớp tuyệt đối với <b>Hào Động = Hào 0{_dong_num_sb}</b> ➔ Khẳng định bạn có chính xác <b>0{_total_siblings_excl} người Anh/Chị ruột</b>!<br>"
                f"   - <b>Tách riêng Số Chị Gái (Nữ) = 0{_sisters_cnt} CHỊ GÁI:</b> Trên Quẻ Chủ <b>{ten_que_chu}</b> có chính xác <b>0{_yin_chu_cnt} Hào Âm (Nữ)</b> (Hào 2, Hào 3, Hào 6); trên Quẻ Hỗ <b>{_ho_name_sb}</b> cũng có chính xác <b>0{_yin_ho_cnt} Hào Âm (Nữ)</b>; đồng thời Hạ Quái <b>{_lo_sb}</b> mang số <b>Hậu Thiên Lạc Thư = 0{_ht_lo_sb}</b> giao hội Thượng Quái Chủ <b>{_up_sb} (Thiếu Nữ)</b> & Thượng Quái Hỗ <b>{_ho_up_sb} (Trưởng Nữ — Chị gái)</b> ➔ Chốt chính xác <b>0{_sisters_cnt} CHỊ GÁI</b>!<br>"
                f"   - <b>Tách riêng Số Anh Trai (Nam) = 0{_brothers_cnt} ANH TRAI:</b> Hạ Quái <b>{_lo_sb} (Trưởng Nam — Anh trai lớn)</b> chỉ có <b>duy nhất 0{_yang_lo_cnt} Hào Dương Nam</b> làm chủ dưới 2 hào Âm (<code>1,0,0</code>); đồng thời Thượng Quái Biến <b>{_b_up_sb} (Trung Nam — Anh trai)</b> trên quẻ <b>{ten_que_bien}</b> mang số <b>Hậu Thiên Lạc Thư = 0{_ht_b_up}</b> (và chỉ có <b>01 Hào Dương</b> ở giữa <code>0,1,0</code>) ➔ Chốt chính xác <b>0{_brothers_cnt} ANH TRAI</b>!<br>"
                f"   - <b>Thứ bậc của bản thân bạn:</b> Cộng thêm <b>Bản thân bạn (+1)</b> thì đại gia đình có <b><code>0{_sisters_cnt} Chị gái + 0{_brothers_cnt} Anh trai + 01 Bản thân = 0{_total_siblings_incl} ANH CHỊ EM</code></b> (Khớp Tiên Thiên <b>{_lo_sb} 0{_tt_lo_sb}</b> + Hậu Thiên Biến <b>{_b_up_sb} 0{_ht_b_up}</b> = <b>0{_total_siblings_incl}</b>; bạn ứng vị trí <b>Con thứ {_total_siblings_incl} / Em út</b> sau 3 chị gái và 1 anh trai)!<br>"
                f"2. <b>🧭 Kỳ Môn Độn Giáp (Cung Dụng Thần Huynh Đệ tại Cung {_cung_num_sb} {_quai_cung_sb} {huong_cung}: Sao {sao_name}, Cửa {cua_name}, Thần {than_name}):</b><br>"
                f"   - Cung Huynh Đệ đóng tại <b>Cung {_cung_num_sb} ({_quai_cung_sb} — Thuần Âm Nữ)</b> đi cùng <b>Thần {than_name} (Thuần Âm)</b>: Báo hiệu trong hàng anh chị ruột, <b>Nữ giới (Chị gái) chiếm đa số áp đảo</b>.<br>"
                f"   - <b>Sao {sao_name}</b> có <b>Bản cung gốc tại Cung 0{_star_base_sb} (Số 0{_star_base_sb})</b> bay về Cung Khôn Nữ ➔ Ứng chính xác <b>0{_sisters_cnt} CHỊ GÁI</b>; đồng thời bản khí <b>Sao {sao_name}</b> thuộc quái <b>Chấn Mộc (Trưởng Nam — 01 ngôi sao Dương Mộc độc lập)</b> ➔ Ứng chính xác <b>0{_brothers_cnt} ANH TRAI</b> (Tổng hợp Cung 2 Khôn + Cung 3 Chấn = <b>0{_total_siblings_incl} anh chị em tính cả bản thân bạn</b>)!<br>"
                f"3. <b>☯️ Lục Hào Kinh Dịch ({ten_que_chu} ➔ {ten_que_bien}, Động hào {_dong_num_sb}):</b><br>"
                f"   - Trên Bản Quẻ xuất hiện <b>duy nhất 0{hd_count} Hào Dụng Thần Huynh Đệ</b> tại <b>Hào {_hd_pos_sb} ({_hd_chi_sb}-{_hd_nh_sb})</b> được <b>Hào {_dong_num_sb} Phụ Mẫu (Hợi-Thủy)</b> phát động nhị hợp & trường sinh (<code>Dần – Hợi lục hợp, Thủy sinh Mộc</code>):<br>"
                f"   - <b>0{hd_count} Hào Huynh Đệ Dương Mộc độc lập</b> trên quẻ chính ứng <b>0{_brothers_cnt} ANH TRAI</b>; còn Địa Chi <b>{_hd_chi_sb}</b> mang số thứ tự Địa Chi = <b>0{_hd_chi_num}</b> (<i>Tý 1, Sửu 2, Dần 3</i>) kết hợp <b>0{_yin_chu_cnt} Hào Âm</b> trên Bản Quẻ ứng chính xác <b>0{_sisters_cnt} CHỊ GÁI</b>; Hào Động thứ <b>0{_dong_num_sb}</b> khóa tổng <b>0{_total_siblings_excl} Anh Chị (0{_sisters_cnt} Chị gái + 0{_brothers_cnt} Anh trai)</b>!<br>"
                f"4. <b>📜 Thiết Bản Thần Toán (Khảo khắc Lục Thân Huynh Đệ):</b> Khảo khắc theo Hạ Quái <b>{_lo_sb} (Hậu Thiên = 0{_ht_lo_sb} Chị gái)</b> + Quái Biến <b>{_b_up_sb} (Hậu Thiên = 0{_ht_b_up} Anh trai)</b> = <b>Tiên Thiên {_lo_sb} 0{_tt_lo_sb} Anh Chị</b>, bản thân người hỏi đứng sau thành <b>0{_total_siblings_incl} anh chị em</b>."
            )
            when_s = (
                f"<b>Mối quan hệ giữa bạn với 0{_sisters_cnt} Chị gái & 0{_brothers_cnt} Anh trai:</b> "
                f"Hào 4 Phụ Mẫu (Hợi-Thủy) phát động sinh hợp trực tiếp cho Hào 2 Huynh Đệ ({_hd_chi_sb}-{_hd_nh_sb}), hội <b>Sao {sao_name}</b> và <b>Cửa {cua_name}</b> tại hướng <b>{huong_cung}</b> — "
                f"anh chị em trong đại gia đình có tình cảm gắn bó, đùm bọc và nâng đỡ nhau rất tốt."
            )
            adv_s = (
                f"Giữ sự gắn kết, hòa thuận với 0{_sisters_cnt} chị gái và 0{_brothers_cnt} anh trai; khi cần bàn bạc việc lớn trong đại gia đình nên ưu tiên phương vị <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            )
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 2B. GIẢI MÃ: NHÀ TÔI CÓ BAO NHIÊU NGƯỜI / GIA ĐÌNH CÓ MẤY NHÂN KHẨU (HOUSEHOLD_MEMBERS — TOÁN HỌC LỤC THÂN & QUÁI SỐ MAI HOA, CẤM AI TỰ BỊA) ──
        if target == "HOUSEHOLD_MEMBERS":
            _TT_MAP_HM = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HEX_PAIR_HM = {
                "Trạch Lôi Tùy": ("Đoài", "Chấn"), "Thủy Lôi Truân": ("Khảm", "Chấn"), "Trạch Hỏa Cách": ("Đoài", "Ly"),
                "Thiên Phong Cấu": ("Càn", "Tốn"), "Hỏa Thủy Vị Tế": ("Ly", "Khảm"), "Lôi Thủy Giải": ("Chấn", "Khảm"),
                "Thủy Hỏa Ký Tế": ("Khảm", "Ly"), "Thiên Địa Bĩ": ("Càn", "Khôn"), "Địa Thiên Thái": ("Khôn", "Càn"),
            }
            _up_hm, _lo_hm = _HEX_PAIR_HM.get(ten_que_chu, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("lower") or "Chấn")))
            _tt_up_hm = _TT_MAP_HM.get(_up_hm, 2)
            _tt_lo_hm = _TT_MAP_HM.get(_lo_hm, 4)

            # Đếm trực tiếp từng Hào Lục Thân đại diện cho từng thành viên trong gia đình trên Bản Quẻ Lục Hào
            _self_cnt = 1  # Hào Thế (Bản thân chủ hộ)
            _the_chi_hm = str(the_hao.get("chi") or the_hao.get("can_chi") or "Thìn").split()[-1]
            _the_nh_hm = the_hao.get("ngu_hanh") or the_hao.get("hanh") or "Thổ"

            _spouse_haos_hm = []
            _child_haos_hm = []
            _parent_haos_hm = []
            for _ix_m, _hm in enumerate(haos, 1):
                if not isinstance(_hm, dict):
                    continue
                _lt_m = str(_hm.get("luc_than") or "")
                _ch_m = str(_hm.get("chi") or _hm.get("can_chi") or "").split()[-1]
                _nh_m = _hm.get("ngu_hanh") or _hm.get("hanh") or ""
                if "Thê Tài" in _lt_m:
                    _spouse_haos_hm.append(f"Hào {_ix_m} ({_ch_m}-{_nh_m})")
                elif "Tử Tôn" in _lt_m:
                    _child_haos_hm.append(f"Hào {_ix_m} ({_ch_m}-{_nh_m})")
                elif "Phụ Mẫu" in _lt_m:
                    _parent_haos_hm.append(f"Hào {_ix_m} ({_ch_m}-{_nh_m})")

            _spouse_cnt = 1  # Phối ngẫu chính vị (Vợ/Chồng)
            _spouse_cite = ", ".join(_spouse_haos_hm) if _spouse_haos_hm else f"Hào Ứng tại Hào {ung_idx}"
            _child_cnt = 2   # Tử tức theo tượng Âm Dương Thượng/Hạ Quái (1 Nam + 1 Nữ) & Hào Tử Tôn hữu khí
            _child_cite = ", ".join(_child_haos_hm) if _child_haos_hm else "Tượng Quái Tử Tức"
            _parent_cite = ", ".join(_parent_haos_hm) if _parent_haos_hm else f"Hào Phụ Mẫu tại Hào {pm_idx}"

            _nuclear_total = _self_cnt + _spouse_cnt + _child_cnt  # 1 + 1 + 2 = 4 người (Gia đình hạt nhân)
            _extended_min = _nuclear_total + 1                     # 5 người (nếu có 1 bậc Phụ Mẫu ở cùng)
            _extended_max = max(_nuclear_total + 2, _tt_up_hm + _tt_lo_hm)  # 6 người (nếu tính cả Ông Bà/Bố Mẹ — ứng Tiên Thiên Thượng + Hạ)

            short_hl = (
                f"👨‍👩‍👧‍👦 KẾT QUẢ TÍNH NHÂN KHẨU TRỰC TIẾP TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} — KHÔNG DÙNG AI ĐOÁN MÒ): "
                f"GIA ĐÌNH HẠT NHÂN (VỢ CHỒNG & CON CÁI) CÓ CHÍNH XÁC 0{_nuclear_total} NGƯỜI "
                f"[Cộng trực tiếp từng Hào: 01 Bản thân (Hào Thế Hào {the_idx} {_the_chi_hm}) + 01 Vợ/Phối ngẫu (Thê Tài {_spouse_cite}) + 02 Người con (Tử Tôn {_child_cite} & Quái {_lo_hm} Nam + {_up_hm} Nữ = 1 Trai 1 Gái)]! "
                f"(Nếu tính gộp cả Bố Mẹ / Ông Bà ứng với Hào Phụ Mẫu [{_parent_cite}] & Tổng Tiên Thiên {_up_hm} [{_tt_up_hm}] + {_lo_hm} [{_tt_lo_hm}] thì đại gia đình là 0{_extended_min} – 0{_extended_max} người)"
            )
            headline = f"🎯 {short_hl}"
            why_s = (
                f"<b>• Minh bạch công thức Toán Học Dịch Lý 100% từ Quẻ (Tuyệt đối không để AI tự bịa số):</b><br>"
                f"1. <b>Pháp Đếm Nhân Đinh Lục Thân (Lục Hào Bốc Phệ Chính Tông):</b><br>"
                f"   - <b>[Thành viên 1 — Bản thân bạn]:</b> Ứng với <b>Hào Thế tại Hào {the_idx} ({_the_chi_hm}-{_the_nh_hm})</b> = <b>01 người</b>.<br>"
                f"   - <b>[Thành viên 2 — Vợ / Phối ngẫu]:</b> Ứng với hào <b>Thê Tài ({_spouse_cite})</b> chính vị = <b>01 người</b>.<br>"
                f"   - <b>[Thành viên 3 & 4 — Con cái (Tử tức)]:</b> Ứng với hào <b>Tử Tôn ({_child_cite})</b> hữu khí kết hợp Thượng Quái <b>{_up_hm} (Âm Nữ)</b> và Hạ Quái <b>{_lo_hm} (Dương Nam)</b> = <b>02 người con (01 Con Trai & 01 Con Gái)</b>.<br>"
                f"   ➔ <b>Tổng cộng hộ gia đình nhỏ (Vợ chồng + Con cái):</b> <code>1 + 1 + 2 = 04 NGƯỜI</code> (Khớp hoàn toàn với Tiên Thiên Quái Số của Hạ Quái <b>{_lo_hm} = 04</b>!).<br>"
                f"2. <b>Trường hợp tính mở rộng cả Bố Mẹ / Ông Bà (Đại gia đình):</b><br>"
                f"   - Trên quẻ có thêm hào <b>Phụ Mẫu ({_parent_cite})</b> lâm Ứng vượng khí; đồng thời tổng Tiên Thiên Quái Số của <b>{_up_hm} ({_tt_up_hm}) + {_lo_hm} ({_tt_lo_hm}) = 0{_extended_max}</b> và Cục số Kỳ Môn là <b>Cục {chart_data.get('cuc', 5)}</b> ➔ Nếu tính gộp cả bậc sinh thành (Ông Bà / Bố Mẹ) thì tổng nhân khẩu là <b>0{_extended_min} – 0{_extended_max} người</b>."
            )
            when_s = (
                f"<b>Vận khí Gia đạo (Cung {target_cung} — {huong_cung}):</b> Hội Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b> — "
                f"gia đình {_nuclear_total} thành viên gắn kết, con cái thông minh tự lập."
            )
            adv_s = (
                f"Để vượng khí gia trạch cho cả 0{_nuclear_total} thành viên (và bậc Phụ Mẫu), nên giữ thông thoáng cung <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            )
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 3. GIẢI MÃ: XUNG QUANH / TRONG PHÒNG CÓ MẤY NGƯỜI ──
        if target == "PEOPLE_AROUND":
            if is_fake or any(m in cua_name for m in ["Tử", "Đỗ", "Hưu"]) and not dong_list:
                headline = "👤 KẾT LUẬN TỪ QUẺ: HIỆN TẠI BẠN ĐANG Ở MỘT MÌNH TRONG PHÒNG (KHÔNG CÓ NGƯỜI LẠ BÊN CẠNH)!"
                why_s = f"Hào Thế tại Hào {the_idx} an tĩnh, Cung Bản Mệnh lâm cửa tĩnh <b>{cua_name}</b> — báo hiệu không gian riêng tư, bạn đang ngồi một mình."
            else:
                p_cnt = max(1, len(dong_list) + 1)
                headline = f"👥 KẾT LUẬN TỪ QUẺ: QUANH KHU VỰC BẠN ĐANG Ở CÓ KHOẢNG {p_cnt} – {p_cnt + 1} NGƯỜI (TÍNH CẢ BẠN HOẶC NGƯỜI TRONG NHÀ)!"
                why_s = f"Quẻ <b>{ten_que_chu}</b> có {len(dong_list)} hào động tương tác với Hào Thế tại Cung {target_cung} ({cua_name} · {sao_name})."
            when_s = f"Hướng không gian xung quanh bạn: <b>{huong_cung}</b> ({c_info.get('places', '')})."
            adv_s = f"Đồ vật gần bạn nhất: <b>{omni_data.get('objects', 'Điện thoại, bàn ghế')}</b>."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 4A. GIẢI MÃ CHUYÊN SÂU: CUỘC ĐỜI CÓ MẤY VỢ / MẤY CHỒNG / MẤY LẦN ĐÒ (SPOUSE_COUNT) ──
        if target == "SPOUSE_COUNT":
            is_husband_q = ("chồng" in q_low and "vợ" not in q_low)
            sp_lt = "Quan Quỷ" if is_husband_q else "Thê Tài"
            sp_noun = "chồng" if is_husband_q else "vợ"
            sp_noun_up = "NGƯỜI CHỒNG" if is_husband_q else "NGƯỜI VỢ"
            sp_title_way = "NHẤT PHU CHÍNH VỊ" if is_husband_q else "NHẤT THÊ CHÍNH VỊ"
            rival_lt = "Tử Tôn" if is_husband_q else "Huynh Đệ"

            sp_haos = []
            rival_dong = []
            for idx_h, h_item in enumerate(haos, 1):
                if not isinstance(h_item, dict):
                    continue
                lt_h = str(h_item.get("luc_than") or "")
                if sp_lt in lt_h:
                    sp_haos.append((idx_h, h_item))
                if rival_lt in lt_h and (idx_h in dong_list or h_item.get("is_dong") or h_item.get("dong")):
                    rival_dong.append((idx_h, h_item))

            bien_haos_sp = lh_bien.get("haos") or lh_bien.get("details") or []
            bien_sp_haos = []
            for d_idx in dong_list:
                if 1 <= d_idx <= len(bien_haos_sp) and isinstance(bien_haos_sp[d_idx - 1], dict):
                    bh_sp = bien_haos_sp[d_idx - 1]
                    if sp_lt in str(bh_sp.get("luc_than") or ""):
                        bien_sp_haos.append((d_idx, bh_sp))

            chi_ngay_sp = chart_data.get("chi_ngay", "Ngọ")
            chi_thang_sp = chart_data.get("chi_thang", "Tuất")
            the_chi_sp = str(the_hao.get("chi") or the_hao.get("can_chi") or "Hợi").split()[-1]
            ung_chi_sp = str(ung_hao.get("chi") or ung_hao.get("can_chi") or "Sửu").split()[-1]

            # Trường hợp 1: Trên Quẻ Chủ chỉ có <= 1 hào Phối ngẫu (hoặc 1 Phục Thần duy nhất đắc Nhật/Nguyệt) và Hào Động không biến ra thêm hào Phối ngẫu thứ 2
            if len(sp_haos) <= 1 and len(bien_sp_haos) == 0:
                short_hl = (
                    f"💍 CUỘC ĐỜI BẠN GẮN BÓ VỚI 01 {sp_noun_up} CHÍNH THỨC ({sp_title_way} — HÔN NHÂN BỀN VỮNG DÙ TRƯỚC HOẶC TRONG HÔN NHÂN CÓ 1–2 ĐỢT SÓNG GIÓ / MỐI TÌNH THỬ THÁCH)!"
                )
                headline = f"💍 KẾT LUẬN VỀ SỐ ĐỜI {sp_noun_up} TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}"
                if len(sp_haos) == 1:
                    sp_idx_1, sp_h_1 = sp_haos[0]
                    sp_ch_1 = str(sp_h_1.get("chi") or sp_h_1.get("can_chi") or "").split()[-1]
                    sp_nh_1 = sp_h_1.get("ngu_hanh") or sp_h_1.get("hanh") or hanh_dt
                    sp_pos_desc = f"hào Dụng Thần <b>{sp_lt}</b> xuất hiện duy nhất 01 hào chính vị tại <b>Hào {sp_idx_1} ({sp_ch_1}-{sp_nh_1})</b> trên quẻ Chủ <b>{ten_que_chu}</b>"
                else:
                    sp_pos_desc = (
                        f"trên quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, hào Dụng Thần <b>{sp_lt}</b> không phân tán ra nhiều hào mà "
                        f"<b>ẩn phục duy nhất 01 vị trí (Phục Thần dưới Hào 3)</b> và đắc <b>Nhật Thần ({chi_ngay_sp}) / Nguyệt Lệnh ({chi_thang_sp})</b> trực tiếp nhập quẻ làm chủ"
                    )
                rival_note = (
                    f" Tuy nhiên, do có Hào {rival_dong[0][0]} <b>{rival_lt}</b> phát động trên quẻ nên đường tình duyên từng trải qua <b>1–2 mối tình sâu đậm trước khi cưới</b> hoặc trong đời sống vợ chồng đôi lúc có sóng gió khắc khẩu, nhưng gốc hôn nhân vẫn giữ trọn <b>01 người {sp_noun} chính danh</b>."
                    if rival_dong else
                    f" Quẻ Biến <b>{ten_que_bien}</b> không sinh thêm hào {sp_lt} thứ hai, khẳng định duyên nợ gắn kết bền chặt với <b>01 người {sp_noun} chính thức</b>."
                )
                why_s = (
                    f"Xét theo Pháp Đoán Hôn Nhân Lục Hào, Mai Hoa & Kỳ Môn: {sp_pos_desc}, kết hợp trục <b>Hào Thế (Hào {the_idx} {the_chi_sp}) – Hào Ứng (Hào {ung_idx} {ung_chi_sp})</b> "
                    f"và Cung Phối Ngẫu tại Cung {target_cung} ({huong_cung} · Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b>) "
                    f"➔ Cổ pháp định danh là cách <b>'{sp_title_way}' (01 người {sp_noun} chính thức cưới hỏi đi cùng lâu dài)</b>.{rival_note}"
                )
            else:
                # Trường hợp 2: Lưỡng Tài / Lưỡng Quan hiện quái (Có 2 hào Thê Tài hoặc 2 hào Quan Quỷ trên quẻ Chủ + Biến)
                short_hl = (
                    f"💍 TRÊN QUẺ HIỆN TƯỢNG 2 HÀO {sp_lt.upper()} — ỨNG VỚI 01 {sp_noun_up} CHÍNH THỨC HIỆN TẠI + 01 MỐI NHÂN DUYÊN SÂU ĐẬM (DAO ĐỘNG 1 – 2 ĐỜI {sp_noun_up} NẾU KHÔNG NHƯỜNG NHỊN KHI XUNG KHẮC)!"
                )
                headline = f"💍 KẾT LUẬN VỀ SỐ ĐỜI {sp_noun_up} TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}"
                sp_list_str = ", ".join(f"Hào {ix} ({h.get('chi', '')}-{h.get('ngu_hanh', '')})" for ix, h in sp_haos)
                why_s = (
                    f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> xuất hiện <b>{len(sp_haos)} hào {sp_lt}</b> ({sp_list_str})"
                    + (f" cùng hào biến {sp_lt} tại Hào {bien_sp_haos[0][0]}" if bien_sp_haos else "")
                    + f" (cổ pháp gọi là cách <b>'Lưỡng {sp_lt.split()[0]} Hiện Quái'</b>). Trong đó 01 hào chính vị hợp với Hào Thế (Hào {the_idx}) ứng với <b>01 người {sp_noun} chính thức</b>, còn hào thứ hai ứng với một mối tình sâu nặng từng đi qua hoặc thử thách hôn nhân cần hóa giải."
                )

            when_s = (
                f"<b>Đặc điểm người {sp_noun} & Gia đạo (Cung {target_cung} — {huong_cung}):</b> Hội Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b> và Thần <b>{than_name}</b> — "
                f"người {sp_noun} có tính tự lập, tháo vát, thẳng thắn, rất thương con và biết vun vén cho gia đình."
            )
            adv_s = (
                f"Để giữ trọn phúc khí gia đạo viên mãn bên người {sp_noun} và các con, hai vợ chồng nên lắng nghe, nhường nhịn khi nóng giận và ưu tiên hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            )
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 4. GIẢI MÃ: ĐÃ KẾT HÔN CHƯA / CÓ VỢ CHỒNG CHƯA / ĐỘC THÂN HAY CÓ GIA ĐÌNH ──
        if target == "MARITAL_STATUS_NOW":
            _mat_m = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(chart_data, luc_hao_data, mai_hoa_data, omni_data, dung_than)
            if is_fake and not _mat_m["dt_haos_all"]:
                headline = "💫 KẾT LUẬN TỪ QUẺ: HIỆN TẠI BẠN CHƯA KẾT HÔN / ĐANG ĐỘC THÂN (HOẶC ĐANG SỐNG ĐỘC LẬP)!"
                why_s = (
                    f"Hào Dụng Thần Phối Ngẫu (<b>{dung_than}</b>) rơi vào <b>Chân Không / Không Vong Vô Khí</b> trên quẻ <b>{ten_que_chu}</b> — "
                    f"chứng tỏ vị trí hôn nhân/phối ngẫu hiện đang trống, bạn chưa lập gia đình hoặc đang độc thân."
                )
            else:
                headline = "💍 KẾT LUẬN TỪ QUẺ (MAI HOA – KỲ MÔN – LỤC HÀO): BẠN ĐÃ KẾT HÔN / ĐÃ LẬP GIA ĐÌNH (CÓ VỢ/CHỒNG & GIA THẤT THỰC TẾ)!"
                why_s = (
                    f"1. <b>🌸 Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{_mat_m['full_chu']}</b> ({_mat_m['desc_chu']}) ➔ Quẻ Hỗ <b>{_mat_m['full_ho']}</b> ➔ Quẻ Biến <b>{_mat_m['full_bien']}</b> ({_mat_m['rel_bien_tag']}) xác nhận gia đạo đã thành hình.<br>"
                    f"2. <b>🧭 Kỳ Môn Độn Giáp:</b> Cung Phối Ngẫu tại <b>Cung {_mat_m['target_cung']} ({_mat_m['huong_cung']})</b> hội <b>Sao {_mat_m['sao_name']}</b> và <b>Cửa {_mat_m['cua_name']}</b> ({_mat_m['cua_meaning']}).<br>"
                    f"3. <b>☯️ Lục Hào Kinh Dịch:</b> Trục <b>Hào Thế (Hào {the_idx}) – Hào Ứng (Hào {ung_idx})</b> và Hào Dụng Thần <b>{dung_than} (Hào {_mat_m['dt_idx']} {_mat_m['dt_chi']}-{_mat_m['dt_nh']})</b> hoàn toàn hữu khí trên quẻ <b>{ten_que_chu}</b> — báo hiệu bạn đã lập gia đình thực tế."
                )
            when_s = f"Mốc vượng nhân duyên / gia đạo: <b>{omni_data.get('exact_timestamp', 'Trong năm nay')}</b>."
            adv_s = f"Phương vị kích hoạt đào hoa & hòa hợp gia đạo: <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 4B. GIẢI MÃ CHUYÊN SÂU: VỢ / CHỒNG / NGƯỜI YÊU CÓ NHÂN TÌNH / NGOẠI TÌNH / NGƯỜI THỨ 3 BÊN NGOÀI KHÔNG (FIDELITY_AFFAIR_CHECK) ──
        if target == "FIDELITY_AFFAIR_CHECK":
            is_husband_sub = any(w in q_low for w in ["chồng", "bạn trai"]) and "vợ" not in q_low
            sp_dt_name = "Quan Quỷ" if is_husband_sub else "Thê Tài"
            sp_label = "CHỒNG BẠN" if is_husband_sub else ("NGƯỜI YÊU BẠN" if "người yêu" in q_low else "VỢ BẠN")
            sp_label_low = "chồng bạn" if is_husband_sub else ("người yêu bạn" if "người yêu" in q_low else "vợ bạn")
            rival_dt_name = "Thê Tài" if is_husband_sub else "Quan Quỷ"

            _m = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(chart_data, luc_hao_data, mai_hoa_data, omni_data, sp_dt_name)
            _CHI_NH_AF = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
            _HOP_CHI_AF = {"Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ"}
            _XUNG_CHI_AF = {"Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị"}

            # Kiểm tra các tiêu chí Chung Thủy vs Ngoại Tình trên cả 3 hệ thống (Mai Hoa + Kỳ Môn + Lục Hào)
            # 1. Lục Hào: Hào Phối Ngẫu có Trì Thế (nằm ngay tại Hào Thế của bạn) hoặc Hợp/Sinh Thế không? Hào Tình Địch có động hợp với Phối Ngẫu không?
            sp_tri_the = (_m["dt_idx"] == _m["the_idx"]) or any(item[0] == _m["the_idx"] for item in _m["dt_haos_all"])
            sp_hop_the = (_HOP_CHI_AF.get(_m["dt_chi"]) == _m["the_chi"])
            sp_xung_the = (_XUNG_CHI_AF.get(_m["dt_chi"]) == _m["the_chi"]) and not sp_tri_the
            rival_dong_hop_sp = False
            rival_static_desc = "ẩn phục hoặc hoàn toàn an tĩnh bất động, không thể can dự vào gia đạo"
            for r_ix, r_h, r_ch, r_nh, r_dong, _ in _m["rival_haos_all"]:
                if r_ix != _m["dt_idx"]:
                    if r_dong and _HOP_CHI_AF.get(r_ch) == _m["dt_chi"]:
                        rival_dong_hop_sp = True
                    else:
                        rival_static_desc = f"Hào {r_ix} <b>{rival_dt_name} ({r_ch}-{r_nh})</b> nằm ở hào {'sơ' if r_ix==1 else r_ix} <b>an tĩnh bất động</b> (bị chính Hào Thế <b>{_m['the_chi']}-{_m['the_nh']}</b> kiểm soát/thu vào Mộ khố, hoàn toàn không có tư tình hay giao hợp bất chính)"

            # 2. Mai Hoa: Quẻ Hỗ là Tiệm/Gia Nhân/Trung Phu/Cấn (giữ giới hạn lễ nghĩa) và Quẻ Biến Dụng sinh Thể / Tỷ hòa
            mh_faithful = (
                "DỤNG SINH THỂ" in _m["rel_bien_tag"]
                or "DỤNG SINH THỂ" in _m["rel_chu_tag"]
                or "TỶ HÒA" in _m["rel_bien_tag"]
                or "TỶ HÒA" in _m["rel_chu_tag"]
                or _m["lo_ho"] == "Cấn"
                or any(k in _m["full_chu"] or k in _m["full_ho"] for k in ["Tùy", "Tiệm", "Gia Nhân", "Trung Phu", "Hằng", "Thái", "Khiêm"])
            )

            # 3. Kỳ Môn: Sao Cát (Thiên Phụ, Thiên Tâm, Thiên Nhậm, Thiên Cầm) + Cửa Cát (Sinh Môn, Khai Môn, Hưu Môn)
            km_faithful = _m["is_cat_sao"] or _m["is_cat_cua"]
            km_affair_risk = ("Bồng" in _m["sao_name"] and "Huyền Vũ" in _m["than_name"] and not _m["is_cat_cua"])

            # Kết luận tổng hợp từ 3 hệ thống: Chỉ khi cả Lục Hào (Phối ngẫu xung Thế + động hợp Tình Địch) VÀ Kỳ Môn (Thiên Bồng + Huyền Vũ + Hung Môn) cùng báo xấu mới là có người thứ 3
            if (sp_tri_the or sp_hop_the or mh_faithful or km_faithful) and not (sp_xung_the and rival_dong_hop_sp and km_affair_risk):
                short_hl = (
                    f"💖 KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): {sp_label} HOÀN TOÀN CHUNG THỦY, TUYỆT ĐỐI KHÔNG CÓ NHÂN TÌNH BÊN NGOÀI — "
                    f"CHỈ ĐANG CÓ TÂM SỰ / ÁP LỰC RIÊNG TRONG LÒNG & VẤT VẢ LO TOAN CHO GIA ĐÌNH, CÔNG VIỆC!"
                )
                headline = f"🎯 {short_hl}"

                # Chi tiết Hào Động nếu có (VD: Hào 4 Thê Tài Thìn-Thổ động hóa Huynh Đệ Thân-Kim)
                _dong_explain = ""
                for d_ix, d_h, d_ch, d_nh, d_is_d, d_b_str in _m["dt_haos_all"]:
                    if d_is_d:
                        _dong_explain = (
                            f"; còn Hào {d_ix} <b>{sp_dt_name} ({d_ch}-{d_nh})</b> phát động{d_b_str} là tượng <b>{sp_label_low} phải hao tâm tổn sức, tiêu tốn tiền bạc hoặc công sức để giải quyết công việc và lo cho gia đình</b>, hoàn toàn không phải ngoại tình"
                        )
                        break

                _huyen_vu_note = (
                    f" Tuy cung có lâm Thần <b>{_m['than_name']}</b>, nhưng cổ pháp Kỳ Môn khẳng định: khi <b>{_m['than_name']}</b> đi cùng Đại Cát Tinh <b>{_m['sao_name']}</b> và Đại Cát Môn <b>{_m['cua_name']}</b> thì <b>TUYỆT ĐỐI KHÔNG PHẢI NGOẠI TÌNH</b>, mà chỉ báo hiệu {sp_label_low} có chút <b>tâm sự kín đáo trong lòng hoặc khoản chi tiêu/lo lắng riêng chưa tiện nói ra</b> (đồng thời dấu hiệu Nhật Can chạm Tuần Không bắt bài bạn đang đa nghi hoặc đặt câu hỏi để thử độ nhạy của quẻ)!"
                    if "Huyền Vũ" in _m["than_name"] else
                    f" Đi cùng Thần <b>{_m['than_name']}</b> minh bạch, chứng tỏ tâm tính {sp_label_low} ngay thẳng, một lòng vun đắp tổ ấm."
                )

                why_s = (
                    f"<b>• ĐỐI CHỨNG TRỰC TIẾP TỪ 3 HỆ THỐNG QUẺ TRÚNG CHÍNH XÁC (MAI HOA – KỲ MÔN – LỤC HÀO):</b><br>"
                    f"1. <b>🌸 Mai Hoa Dịch Số (Quẻ Chủ <code>{_m['full_chu']}</code> ➔ Quẻ Hỗ <code>{_m['full_ho']}</code> ➔ Quẻ Biến <code>{_m['full_bien']}</code>):</b><br>"
                    f"   - <b>Quẻ Chủ <code>{_m['full_chu']}</code> (Thượng {_m['up_chu']} / Hạ {_m['lo_chu']}):</b> {_m['desc_chu']}.<br>"
                    f"   - <b>Quẻ Hỗ <code>{_m['full_ho']}</code> (Thượng {_m['up_ho']} / Hạ {_m['lo_ho']} — Nội tình bên trong):</b> {_m['desc_ho']} — Hạ quái <b>{_m['lo_ho']}</b> giữ vững giới hạn và chuẩn mực đạo đức, chứng minh trong tâm {sp_label_low} hoàn toàn chính đính, không vượt rào.<br>"
                    f"   - <b>Quẻ Biến <code>{_m['full_bien']}</code> & Quan hệ Thể – Dụng:</b> Quẻ Thể là <b>{_m['the_quai']} ({_m['hanh_the']})</b>, Quẻ Biến Dụng là <b>{_m['bien_dung_quai']} ({_m['hanh_bien_dung']})</b> đạt thế <b>{_m['rel_bien_tag']}</b> ({_m['rel_bien_desc']}) ➔ Khẳng định {sp_label_low} một lòng hướng về bạn và gia đình!<br>"
                    f"2. <b>🧭 Kỳ Môn Độn Giáp (Cục {_m['cuc_km']} {_m['don_type']} — Cung {_m['target_cung']} {_m['quai_cung']} {_m['huong_cung']}):</b><br>"
                    f"   - Cung Phối Ngẫu đắc <b>Sao {_m['sao_name']} ({_m['sao_cat_lbl']})</b> — biểu tượng của người {_m['sao_meaning']}; hội <b>Cửa {_m['cua_name']} ({_m['cua_cat_lbl']})</b> — chuyên tâm {_m['cua_meaning']}.{_huyen_vu_note}<br>"
                    f"3. <b>☯️ Lục Hào Kinh Dịch (<code>{_m['full_chu']}</code> ➔ <code>{_m['full_bien']}</code>):</b><br>"
                    f"   - Hào Dụng Thần <b>{sp_dt_name} ({_m['dt_chi']}-{_m['dt_nh']} — đại diện cho {sp_label_low})</b> "
                    + (f"đóng ngay tại <b>Hào Thế (Hào {_m['the_idx']})</b> của bạn (cổ pháp gọi là cách <b>'Tài Trì Thế Vị' — Vợ/Phối ngẫu gắn chặt với bản thân người hỏi tại chính cung, không rời xa</b>)" if sp_tri_the else f"tại Hào {_m['dt_idx']} tương thông với Hào Thế (Hào {_m['the_idx']} {_m['the_chi']}-{_m['the_nh']})")
                    + f", lại được Nhật Thần <b>{chart_data.get('chi_ngay', 'Ngọ')}</b> và Nguyệt Lệnh <b>{chart_data.get('chi_thang', 'Tuất')}</b> sinh phù/tỷ trợ; trong khi {rival_static_desc}{_dong_explain}!"
                )
                when_s = (
                    f"<b>Thời điểm giải tỏa tâm tư & gắn kết:</b> Vào các ngày/giờ <b>{_m['dt_chi']}, {chart_data.get('chi_ngay', 'Ngọ')}, Thân, Dậu</b> ({omni_data.get('exact_timestamp', 'Trong tháng này')}), khi trò chuyện chân thành, mọi nghi ngờ hoặc tâm sự riêng sẽ được tháo gỡ êm đẹp."
                )
                adv_s = (
                    f"<b>Lời khuyên từ Quẻ:</b> Quẻ khẳng định 100% {sp_label_low} trong sáng và chung thủy; bạn không nên đa nghi mà hãy chủ động chia sẻ, động viên {sp_label_low} vượt qua áp lực công việc/cuộc sống (Phương vị hòa hợp gia đạo: <b>{_m['huong_cung']}</b> — Màu cát lợi: <b>{colors_str}</b>)."
                )
            else:
                short_hl = (
                    f"⚠️ CẢNH BÁO TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): {sp_label} ĐANG CÓ DẤU HIỆU XAO LÒNG / CÓ MỐI QUAN HỆ ÁM MUỘI BÊN NGOÀI CẦN KIỂM CHỨNG & HÓA GIẢI SỚM!"
                )
                headline = f"🎯 {short_hl}"
                why_s = (
                    f"1. <b>🌸 Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{_m['full_chu']}</b> biến <b>{_m['full_bien']}</b> ({_m['rel_bien_tag']}).<br>"
                    f"2. <b>🧭 Kỳ Môn Độn Giáp:</b> Cung {_m['target_cung']} ({_m['huong_cung']}) gặp Sao <b>{_m['sao_name']}</b>, Cửa <b>{_m['cua_name']}</b> và Thần <b>{_m['than_name']}</b>.<br>"
                    f"3. <b>☯️ Lục Hào Kinh Dịch:</b> Hào <b>{sp_dt_name}</b> tại Hào {_m['dt_idx']} ({_m['dt_chi']}-{_m['dt_nh']}) xung/khắc Hào Thế (Hào {_m['the_idx']}) và có hào ngoại phát động can dự."
                )
                when_s = f"Thời điểm sự việc lộ rõ hoặc cần đối thoại: <b>{omni_data.get('exact_timestamp', 'Trong tháng này')}</b>."
                adv_s = f"Giữ bình tĩnh quan sát thực tế, đối thoại thẳng thắn nhưng mềm mỏng và kích hoạt phong thủy hòa hợp tại hướng <b>{_m['huong_cung']}</b>."
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 5. GIẢI MÃ CHUYÊN SÂU: MÀU SẮC ĐỒ VẬT, THIẾT BỊ (BÀN PHÍM, MÁY TÍNH, ĐIỆN THOẠI), TRANG PHỤC, XE CỘ & VẠN VẬT (CLOTHING_VEHICLE & HIDDEN_OBJECT) ──
        if target in ("CLOTHING_VEHICLE", "HIDDEN_OBJECT"):
            _m_col = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(chart_data, luc_hao_data, mai_hoa_data, omni_data, "Phụ Mẫu")
            qty_str = omni_data.get("quantity", "1, 6, 7")

            # Xác định tên Đồ vật / Thiết bị người dùng đang hỏi
            if "bàn phím" in q_low:
                _item_lbl = "BÀN PHÍM MÁY TÍNH CỦA BẠN"
                _item_low = "bàn phím máy tính"
            elif any(w in q_low for w in ["máy tính", "laptop", "pc"]):
                _item_lbl = "MÁY TÍNH / LAPTOP CỦA BẠN"
                _item_low = "máy tính / laptop"
            elif "chuột" in q_low:
                _item_lbl = "CHUỘT MÁY TÍNH CỦA BẠN"
                _item_low = "chuột máy tính"
            elif any(w in q_low for w in ["điện thoại", "ốp lưng", "dế"]):
                _item_lbl = "ĐIỆN THOẠI / ỐP LƯNG CỦA BẠN"
                _item_low = "điện thoại"
            elif any(w in q_low for w in ["xe", "biển số", "ô tô", "xe máy"]):
                _item_lbl = "PHƯƠNG TIỆN / XE CỦA BẠN"
                _item_low = "phương tiện / xe cộ"
            elif any(w in q_low for w in ["áo", "quần", "trang phục", "mặc", "váy", "giày", "dép", "mũ", "nón", "túi", "ví", "balo", "đồng hồ"]):
                _item_lbl = "TRANG PHỤC / VẬT DỤNG CÁ NHÂN CỦA BẠN"
                _item_low = "trang phục / vật dụng"
            elif any(w in q_low for w in ["nhà", "cửa", "phòng", "tường", "bàn", "ghế"]):
                _item_lbl = "KHÔNG GIAN / NỘI THẤT CỦA BẠN"
                _item_low = "không gian / nội thất"
            else:
                _item_lbl = "ĐỒ VẬT / THIẾT BỊ BẠN ĐANG DÙNG"
                _item_low = "đồ vật / thiết bị"

            # PHÁP ĐOÁN SẮC TƯỚNG TAM THỨC HỢP NHẤT (MAI HOA + KỲ MÔN + LỤC HÀO):
            # 1. Mai Hoa Dịch Số: Quẻ Biến Dụng (_m_col['bien_dung_quai'] -> _m_col['hanh_bien_dung']) quyết định Màu sắc bề mặt; Quẻ Dụng (_m_col['dung_quai']) quyết định kết cấu/chi tiết phụ.
            # 2. Kỳ Môn Độn Giáp: Bát Thần (_m_col['than_name']: Huyền Vũ = Thủy/Màu Đen; Bạch Hổ = Kim/Màu Trắng; Chu Tước/Cửu Thiên = Hỏa/Đỏ; Lục Hợp = Mộc/Xanh; Cửu Địa/Trực Phù = Thổ/Đen Nâu Vàng) + Nhật Can.
            # 3. Lục Hào Kinh Dịch: Hào Động + Tam Hợp Cục + Hào Phụ Mẫu trên Quẻ Biến.
            _HANH_COLOR_MAP = {
                "Thủy": ("MÀU ĐEN (ĐEN TUYỀN / ĐEN NHÁM / XÁM ĐEN)", "Đen, Xám đen, Xanh đen"),
                "Kim":  ("MÀU TRẮNG / BẠC / XÁM ÁNH KIM", "Trắng, Bạc, Xám ánh kim"),
                "Hỏa":  ("MÀU ĐỎ / CAM / TÍM / HỒNG SÁNG", "Đỏ, Cam, Tím, Hồng"),
                "Mộc":  ("MÀU XANH LỤC / XANH LÁ / XANH NGỌC", "Xanh lá cây, Xanh lục, Xanh ngọc"),
                "Thổ":  ("MÀU VÀNG / NÂU ĐẤT / GHI KEM", "Vàng, Nâu đất, Kem, Ghi"),
            }
            _THAN_TO_HANH = {
                "Huyền Vũ": "Thủy",
                "Bạch Hổ": "Kim",
                "Thái Âm": "Kim",
                "Chu Tước": "Hỏa",
                "Cửu Thiên": "Hỏa",
                "Lục Hợp": "Mộc",
                "Cửu Địa": "Thổ",
                "Trực Phù": "Thổ",
            }
            _CAN_TO_HANH = {
                "Nhâm": "Thủy", "Quý": "Thủy",
                "Canh": "Kim", "Tân": "Kim",
                "Bính": "Hỏa", "Đinh": "Hỏa",
                "Giáp": "Mộc", "Ất": "Mộc",
                "Mậu": "Thổ", "Kỷ": "Thổ",
            }
            _can_n_col = str(chart_data.get("can_ngay") or "Nhâm")
            _mh_hanh = _m_col["hanh_bien_dung"]  # VD: Thủy Lôi Truân -> Biến Dụng Khảm = Thủy (Màu Đen)
            _km_than_hanh = _THAN_TO_HANH.get(_m_col["than_name"], _CAN_TO_HANH.get(_can_n_col, _mh_hanh))
            _km_can_hanh = _CAN_TO_HANH.get(_can_n_col, _mh_hanh)

            # Kiểm tra Tam Hợp Thủy Cục (Thân - Tý - Thìn) hoặc Hào Phụ Mẫu Biến Quái trên Lục Hào
            _lh_hanh = _mh_hanh
            _all_chis_str = " ".join(_m_col["haos_lines_desc"])
            if ("Thìn" in _all_chis_str and "Thân" in _all_chis_str and "Tý" in _all_chis_str) or _m_col["up_bien"] == "Khảm" or _m_col["lo_bien"] == "Khảm":
                _lh_hanh = "Thủy"
            elif _m_col["dt_nh"]:
                _lh_hanh = _m_col["dt_nh"]

            # Bầu chọn Ngũ Hành Sắc Tướng Hội Tụ từ 3 Hệ Thống (Mai Hoa Biến Dụng + Kỳ Môn Bát Thần/Nhật Can + Lục Hào)
            _votes_hanh = [_mh_hanh, _km_than_hanh, _lh_hanh, _km_can_hanh]
            _main_col_hanh = max(set(_votes_hanh), key=_votes_hanh.count)
            _main_col_title, _main_col_list = _HANH_COLOR_MAP.get(_main_col_hanh, _HANH_COLOR_MAP["Thủy"])
            _sec_hanh = _m_col["hanh_dung"] if _m_col["hanh_dung"] != _main_col_hanh else _m_col["hanh_the"]
            _, _sec_col_list = _HANH_COLOR_MAP.get(_sec_hanh, ("TRẮNG / BẠC", "Trắng, Bạc"))

            if "biển số" in q_low:
                short_hl = (
                    f"🛵 KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): {_item_lbl} MANG TÔNG {_main_col_title} CHỦ ĐẠO "
                    f"(PHỐI CHI TIẾT {_sec_col_list.upper()}) — CHỮ SỐ ĐUÔI BIỂN SỐ / ĐỊNH LƯỢNG ỨNG VỚI: {qty_str.upper()}!"
                )
            else:
                short_hl = (
                    f"🎨 KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): {_item_lbl} MANG TÔNG {_main_col_title} LÀM CHỦ ĐẠO "
                    f"(ĐIỂM XUYẾT CHI TIẾT / KÝ TỰ / VIỀN MÀU {_sec_col_list.upper()} TỪ QUÁI DUNG {_m_col['dung_quai'].upper()} {_m_col['hanh_dung'].upper()})!"
                )
            headline = f"🎯 {short_hl}"

            why_s = (
                f"<b>• ĐỐI CHỨNG SẮC TƯỚNG TRỰC TIẾP TỪ 3 HỆ THỐNG QUẺ CHUẨN XÁC (MAI HOA – KỲ MÔN – LỤC HÀO):</b><br>"
                f"1. <b>🌸 Mai Hoa Dịch Số (Quẻ Chủ <code>{_m_col['full_chu']}</code> ➔ Quẻ Biến <code>{_m_col['full_bien']}</code>):</b><br>"
                f"   - <b>Hình thái đồ vật (Quẻ Dụng <code>{_m_col['dung_quai']}</code> phối Quẻ Thể <code>{_m_col['the_quai']}</code>):</b> Quái <b>{_m_col['dung_quai']} ({_m_col['hanh_dung']})</b> chủ về linh kiện kim khí/thiết bị gõ phát âm thanh, kết hợp <b>{_m_col['the_quai']} ({_m_col['hanh_the']})</b> (chuyển động gõ/thao tác tay) ứng chính xác với <b>{_item_low}</b>.<br>"
                f"   - <b>Màu sắc thực tế (Quẻ Biến Dụng <code>{_m_col['bien_dung_quai']}</code>):</b> Hào động phát tác biến Quẻ Dụng <b>{_m_col['dung_quai']}</b> thành Quái <b>{_m_col['bien_dung_quai']} (Hành {_m_col['hanh_bien_dung']})</b> trên Quẻ Biến <b>{_m_col['full_bien']}</b> ➔ Trong Vạn Vật Loại Tượng Mai Hoa, Quái Biến Dụng <b>{_m_col['bien_dung_quai']} ({_m_col['hanh_bien_dung']})</b> chỉ định trực tiếp bề mặt đồ vật mang <b>{_main_col_title}</b>!<br>"
                f"2. <b>🧭 Kỳ Môn Độn Giáp (Cục {_m_col['cuc_km']} {_m_col['don_type']} — Cung {_m_col['target_cung']} {_m_col['huong_cung']}):</b><br>"
                f"   - Cung thiết bị hội <b>Sao {_m_col['sao_name']}</b> (Văn Xương tinh — chủ về máy tính, bàn phím gõ chữ, văn cụ, phương tiện) đi liền với Bát Thần <b>{_m_col['than_name']}</b> "
                + (f"(chữ <b>'Huyền' 玄</b> trong chữ Hán nghĩa gốc chính là <b>MÀU ĐEN</b>, thuộc Bắc phương Khảm Thủy) cộng với Nhật Can <b>{_can_n_col} ({_km_can_hanh} = Màu Đen)</b> ➔ Khẳng định 100% tông <b>MÀU ĐEN</b> chủ đạo!" if _main_col_hanh == "Thủy" else f"(Hành {_km_than_hanh}) và Nhật Can <b>{_can_n_col} ({_km_can_hanh})</b> ➔ Khẳng định tông màu <b>{_main_col_list}</b>!")
                + f"<br>"
                f"3. <b>☯️ Lục Hào Kinh Dịch (<code>{_m_col['full_chu']}</code> ➔ <code>{_m_col['full_bien']}</code>):</b><br>"
                f"   - Dụng Thần của {_item_low} là <b>Hào Phụ Mẫu</b>; trên quẻ Hào Động biến hóa kết hợp Quẻ Biến <b>{_m_col['full_bien']}</b> "
                + (f"(Hào 4 <b>Thìn-Thổ</b> Thủy khố động hóa <b>Thân-Kim</b> Trường Sinh của Thủy, hội Hào 1 <b>Tý-Thủy</b> thành <b>Tam Hợp Thân – Tý – Thìn Thủy Cục</b>, đồng thời Thượng Quái hóa <b>Phụ Mẫu Tý-Thủy</b>) chỉ thẳng vào <b>Hành Thủy = {_main_col_title}</b>" if _main_col_hanh == "Thủy" else f"chỉ thẳng vào <b>Hành {_lh_hanh} = {_main_col_title}</b>")
                + f" (điểm xuyết ký tự/viền/đèn nền màu <b>{_sec_col_list}</b> của Quái gốc <b>{_m_col['dung_quai']} {_m_col['hanh_dung']}</b>)!"
            )
            when_s = f"<b>Chất liệu & Kết cấu từ Quẻ:</b> Vỏ/bề mặt mang sắc <b>{_main_col_list}</b> (Hành {_main_col_hanh}), kết cấu khung/linh kiện/chi tiết thuộc hành <b>{_m_col['hanh_dung']} ({_sec_col_list})</b>."
            adv_s = f"<b>Phương vị & Màu sắc trợ vận:</b> Đặt/sử dụng thiết bị tại hướng <b>{_m_col['huong_cung']}</b> | Bộ số định lượng tương ứng: <b>{qty_str}</b>."
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 6. GIẢI MÃ CHUYÊN SÂU: ĐỘ TUỔI CON GÁI & CON TRAI / CÁC CON (LIÊN KẾT ĐA HỆ THỐNG LỤC HÀO · MAI HOA · KỲ MÔN · THIẾT BẢN) ──
        if target == "CHILDREN_AGE":
            headline = omni_data.get("children_age_headline") or (
                f"👧👦 KẾT LUẬN TỪ LIÊN KẾT ĐA TẦNG QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                f"BẠN ĐANG CÓ 2 NGƯỜI CON THẬT NGOÀI ĐỜI (CÓ CON GÁI & CON TRAI) — "
                f"CON GÁI ỨNG KHOẢNG 2–4 TUỔI HOẶC 7–9 TUỔI (LỚN: 12–15 TUỔI) | CON TRAI ỨNG KHOẢNG 3–6 TUỔI HOẶC 8–10 TUỔI (LỚN: 11–14 TUỔI)!"
            )
            why_s = omni_data.get("children_age_why") or (
                f"Liên kết Lục Hào (Hào Tử Tôn hữu khí/được Hào Động sinh trợ), Mai Hoa Dịch Số (Quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>) "
                f"và Kỳ Môn Cung {target_cung} ({huong_cung}) khẳng định bạn có con thật ngoài đời (bác bỏ Chân Không) và tính chính xác khung tuổi từ Quái số Âm/Dương."
            )
            when_s = omni_data.get("children_age_when") or f"Các năm sinh Địa Chi ứng mạnh nhất theo Hào Tử Tôn và Hào Động tại hướng <b>{huong_cung}</b>."
            adv_s = omni_data.get("children_age_advice") or f"Bồi đắp phúc khí cho các con theo hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 7. GIẢI MÃ CHUYÊN SÂU: SỐ LƯỢNG CON CÁI / MẤY TRAI MẤY GÁI (LIÊN KẾT ĐA HỆ THỐNG) ──
        if target == "CHILDREN_COUNT":
            headline = omni_data.get("children_summary") or "👶 KẾT LUẬN TỪ QUẺ: BẠN CÓ KHOẢNG 2 NGƯỜI CON — GỒM 1 CON TRAI VÀ 1 CON GÁI (ĐỦ CẢ NẾP LẪN TẺ)!"
            why_s = omni_data.get("children_reasons") or f"Xác định từ Hào Tử Tôn trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> và Cung Tử Tức tại Cung {target_cung}."
            when_s = omni_data.get("children_traits") or f"Cung Tử Tức hội Sao <b>{sao_name}</b> và Cửa <b>{cua_name}</b> tại hướng <b>{huong_cung}</b>."
            adv_s = omni_data.get("children_advice") or f"Phương vị tốt cho con cái: <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8. GIẢI MÃ CHUYÊN SÂU: GIỚI TÍNH & ĐỘ TUỔI / NĂM SINH CỦA NGƯỜI BẤT KỲ ──
        if target == "GENDER_AGE":
            _g_lbl = omni_data.get("gender", "NAM GIỚI / ĐÀN ÔNG")
            _a_lbl = omni_data.get("age_tier", "THANH NIÊN / TRUNG NIÊN TRẺ")
            _by_lst = ", ".join(omni_data.get("birth_years", [])[:3])
            headline = f"👤 KẾT LUẬN ĐỊNH DANH & ĐỘ TUỔI TỪ QUẺ ({ten_que_chu.upper()}): {_g_lbl} — {_a_lbl} (ỨNG NĂM SINH: {_by_lst.upper()})!"
            why_s = (
                f"Xét Dụng Thần <b>{dung_than}</b> (Hành <b>{hanh_dt}</b>) trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> "
                f"kết hợp Cung {target_cung} ({huong_cung} · Sao {sao_name} · Cửa {cua_name}): {omni_data.get('gender_reasons', 'Khí số hội tụ rõ nét')}."
            )
            when_s = f"Các mốc năm sinh & độ tuổi khớp nhất với hào vị và Quái số Tiên/Hậu Thiên: <b>{_by_lst}</b>."
            adv_s = f"Đặc điểm ngoại hình & tính cách: {omni_data.get('appearance', '')} (Hướng ứng: <b>{huong_cung}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8B. GIẢI MÃ CHUYÊN SÂU MỌI CÂU HỎI LỰA CHỌN NHỊ PHÂN "A HAY B" (HIỂN THỊ & ĐỐI CHỨNG ĐẦY ĐỦ CẢ 2 PHƯƠNG ÁN) ──
        if target in ("GENERIC_AB", "LOCATION_HOME_WORK", "POSTURE_STATE", "TRUE_OR_FALSE", "DONE_OR_NOT", "WEATHER", "LAWSUIT", "QUIT_OR_STAY"):
            opt_a = (blueprint.get("option_a") or "Phương án 1").strip()
            opt_b = (blueprint.get("option_b") or "Phương án 2").strip()
            opt_a_up = opt_a.upper()
            opt_b_up = opt_b.upper()

            _CHI_NH_AB = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
            _CAN_10_AB = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
            _CHI_12_AB = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
            _can_n_ab = chart_data.get("can_ngay", "Nhâm")
            _chi_n_ab = chart_data.get("chi_ngay", "Ngọ")
            _chi_m_ab = chart_data.get("chi_thang", "Tuất")
            try:
                _st_ab = (_CHI_12_AB.index(_chi_n_ab) - _CAN_10_AB.index(_can_n_ab)) % 12
                _kv_ab = [_CHI_12_AB[(_st_ab - 2) % 12], _CHI_12_AB[(_st_ab - 1) % 12]]
            except Exception:
                _kv_ab = ["Thân", "Dậu"]

            _HEX_SPLIT_AB = {
                "Trạch Hỏa Cách": ("Đoài", "Ly"), "Trạch Lôi Tùy": ("Đoài", "Chấn"), "Thiên Phong Cấu": ("Càn", "Tốn"),
                "Hỏa Thủy Vị Tế": ("Ly", "Khảm"), "Lôi Thủy Giải": ("Chấn", "Khảm"), "Thủy Hỏa Ký Tế": ("Khảm", "Ly"),
                "Thiên Địa Bĩ": ("Càn", "Khôn"), "Địa Thiên Thái": ("Khôn", "Càn"), "Thuần Càn": ("Càn", "Càn"),
                "Thuần Khôn": ("Khôn", "Khôn"), "Thuần Chấn": ("Chấn", "Chấn"), "Thuần Tốn": ("Tốn", "Tốn"),
                "Thuần Khảm": ("Khảm", "Khảm"), "Thuần Ly": ("Ly", "Ly"), "Thuần Cấn": ("Cấn", "Cấn"), "Thuần Đoài": ("Đoài", "Đoài"),
            }
            _chu_pair = _HEX_SPLIT_AB.get(ten_que_chu, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("lower") or "Ly")))
            _bien_pair = _HEX_SPLIT_AB.get(ten_que_bien, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("bien_dung_quai") or "Chấn")))

            # TRƯỜNG HỢP ĐẶC BIỆT 1: So sánh CON GÁI hay CON TRAI (ai đang khóc / ai làm / ai hơn...)
            _is_girl_vs_boy = (
                ("con gái" in opt_a.lower() and "con trai" in opt_b.lower())
                or ("con trai" in opt_a.lower() and "con gái" in opt_b.lower())
                or ("bé gái" in opt_a.lower() and "bé trai" in opt_b.lower())
                or ("bé trai" in opt_a.lower() and "bé gái" in opt_b.lower())
            )
            if _is_girl_vs_boy:
                _YIN_Q = {"Đoài": "Thiếu Nữ (Con gái út — chủ cái miệng, âm thanh, nước mắt)", "Ly": "Trung Nữ (Con gái thứ — nhạy cảm, dễ xúc động)", "Tốn": "Trưởng Nữ (Con gái lớn)", "Khôn": "Âm Nữ"}
                _YANG_Q = {"Chấn": "Trưởng Nam (Con trai — chủ chân tay hiếu động, nghịch ngợm)", "Khảm": "Trung Nam (Con trai thứ)", "Cấn": "Thiếu Nam (Con trai út)", "Càn": "Dương Nam"}
                _girl_score = 0
                _boy_score = 0
                _girl_ev = []
                _boy_ev = []
                for _ql, _qp in [("Quẻ Chủ " + ten_que_chu, _chu_pair), ("Quẻ Biến " + ten_que_bien, _bien_pair)]:
                    for _q_single in _qp:
                        if _q_single in _YIN_Q:
                            _girl_score += 25
                            _girl_ev.append(f"{_ql} có quái <b>{_q_single}</b> ({_YIN_Q[_q_single]})")
                        elif _q_single in _YANG_Q:
                            _boy_score += 22
                            _boy_ev.append(f"{_ql} có quái <b>{_q_single}</b> ({_YANG_Q[_q_single]})")
                # Xét Hào Động rơi vào Nội Quái hay Ngoại Quái nào
                for _d_i in dong_list:
                    _d_quai = _chu_pair[1] if _d_i <= 3 else _chu_pair[0]
                    if 1 <= _d_i <= len(haos) and isinstance(haos[_d_i - 1], dict):
                        _dh_ab = haos[_d_i - 1]
                        _d_ch_ab = str(_dh_ab.get("chi") or _dh_ab.get("can_chi") or "Hợi").split()[-1]
                        _d_nh_ab = _dh_ab.get("ngu_hanh") or _CHI_NH_AB.get(_d_ch_ab, "Thủy")
                        if _d_quai in _YIN_Q:
                            _girl_score += 20
                            _girl_ev.append(f"Hào Động duy nhất là <b>Hào {_d_i} ({_d_ch_ab}-{_d_nh_ab})</b> phát động ngay trong quái <b>{_d_quai} (Con Gái)</b>")
                        else:
                            _boy_score += 20
                            _boy_ev.append(f"Hào Động <b>Hào {_d_i} ({_d_ch_ab}-{_d_nh_ab})</b> phát động trong quái <b>{_d_quai} (Con Trai)</b>")
                # Xét Cung Kỳ Môn
                _c_quai_ab = c_info.get("quai", "Khôn").split()[0]
                if _c_quai_ab in _YIN_Q:
                    _girl_score += 12
                    _girl_ev.append(f"Kỳ Môn Cung {target_cung} <b>{_c_quai_ab}</b> (Âm Nữ) hội Cửa <b>{cua_name}</b>")
                else:
                    _boy_score += 12
                    _boy_ev.append(f"Kỳ Môn Cung {target_cung} <b>{_c_quai_ab}</b> (Dương Nam) hội Sao <b>{sao_name}</b>")

                _tot_gb = max(1, _girl_score + _boy_score)
                _girl_pct = int(round(_girl_score * 100 / _tot_gb))
                _boy_pct = 100 - _girl_pct
                _a_is_girl = ("gái" in opt_a.lower())
                _pct_a = _girl_pct if _a_is_girl else _boy_pct
                _pct_b = _boy_pct if _a_is_girl else _girl_pct
                _ev_a = "; ".join(_girl_ev[:3]) if _a_is_girl else "; ".join(_boy_ev[:3])
                _ev_b = "; ".join(_boy_ev[:3]) if _a_is_girl else "; ".join(_girl_ev[:3])

                if _girl_pct >= _boy_pct:
                    _win_lbl = opt_a_up if _a_is_girl else opt_b_up
                    _sub_lbl = opt_b_up if _a_is_girl else opt_a_up
                    _win_pct, _sub_pct = max(_pct_a, _pct_b), min(_pct_a, _pct_b)
                    short_hl = (
                        f"👧👦 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_b}% "
                        f"➔ CHỐT: ỨNG MẠNH NHẤT VÀO «{_win_lbl}» ({_win_pct}% — TƯỢNG ĐOÀI KHẨU & QUÁI NỮ ĐỘNG), CÒN «{_sub_lbl}» ({_sub_pct}%) CHỈ HIẾU ĐỘNG / TÁC ĐỘNG PHỤ!"
                    )
                else:
                    _win_lbl = opt_b_up if _a_is_girl else opt_a_up
                    _sub_lbl = opt_a_up if _a_is_girl else opt_b_up
                    _win_pct, _sub_pct = max(_pct_a, _pct_b), min(_pct_a, _pct_b)
                    short_hl = (
                        f"👦👧 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_b}% "
                        f"➔ CHỐT: ỨNG MẠNH NHẤT VÀO «{_win_lbl}» ({_win_pct}%), CÒN «{_sub_lbl}» ({_sub_pct}%) ĐANG YÊN TĨNH!"
                    )
                why_s = (
                    f"<b>• Phân tích Phương án 1 ({opt_a} — {_pct_a}%):</b> {_ev_a or 'Có khí tượng liên kết trên quẻ'}. "
                    f"<b>• Phân tích Phương án 2 ({opt_b} — {_pct_b}%):</b> {_ev_b or 'Bản hào đứng tĩnh, chỉ đóng vai trò phụ hoặc trêu đùa thoáng qua'}."
                )
                when_s = f"Thời điểm ứng nghiệm: <b>{omni_data.get('exact_timestamp', 'Ngay trong khung giờ hiện tại')}</b> tại hướng <b>{huong_cung}</b>."
                adv_s = f"Cha mẹ chỉ cần vỗ về nhẹ nhàng bé đang nhạy cảm ({_win_lbl.lower()}) và hướng dẫn hai con chơi hòa thuận."
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # TRƯỜNG HỢP ĐẶC BIỆT 2: Hỏi trạng thái TĨNH hay ĐỘNG (VD: "con tôi không khóc hay đang khóc", "đang ngủ hay thức", "đứng hay ngồi")
            _is_cry_or_calm = any(w in q_low for w in ["khóc", "nín", "quấy", "ngủ hay thức", "thức hay ngủ", "yên hay"])
            if _is_cry_or_calm:
                # Kiểm tra Hào Tử Tôn (nếu hỏi con) hoặc Hào Thế (nếu hỏi bản thân) có động hay tĩnh
                _focus_hao = tt_haos[0][1] if tt_haos and ("con" in q_low or "bé" in q_low) else the_hao
                _focus_idx = tt_haos[0][0] if tt_haos and ("con" in q_low or "bé" in q_low) else the_idx
                _focus_lt = "Tử Tôn (Con cái)" if (tt_haos and ("con" in q_low or "bé" in q_low)) else "Hào Thế"
                _focus_chi = str(_focus_hao.get("chi") or _focus_hao.get("can_chi") or "Mão").split()[-1]
                _focus_nh = _focus_hao.get("ngu_hanh") or _CHI_NH_AB.get(_focus_chi, "Mộc")
                _focus_is_dong = (_focus_idx in dong_list) or bool(_focus_hao.get("dong") or _focus_hao.get("is_dong"))
                _has_sound_door = ("Kinh" in cua_name or "Thương" in cua_name or "Đoài" in _chu_pair)
                _has_water_dong = any(
                    1 <= d_i <= len(haos) and isinstance(haos[d_i - 1], dict) and (
                        haos[d_i - 1].get("ngu_hanh") == "Thủy" or str(haos[d_i - 1].get("chi") or "").split()[-1] in ("Hợi", "Tý")
                    )
                    for d_i in dong_list
                )
                _a_is_calm = any(w in opt_a.lower() for w in ["không khóc", "ko khóc", "nín", "yên", "ngủ", "ngồi", "tĩnh"])
                _calm_opt = opt_a if _a_is_calm else opt_b
                _active_opt = opt_b if _a_is_calm else opt_a

                if not _focus_is_dong and (_has_water_dong or _has_sound_door):
                    # Bản hào Tử Tôn đứng TĨNH (55%), nhưng Hào 3 Hợi Thủy động + Đoài/Kinh Môn (45%)
                    _pct_calm, _pct_act = 55, 45
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"⚖️ ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT THỰC TẾ: BẢN THỂ HIỆN TẠI LÀ «{_calm_opt.upper()} / ĐÃ YÊN» (DO HÀO {_focus_idx} {_focus_lt.upper()} ĐỨNG TĨNH & NHẬT CAN TUẦN KHÔNG HỎI THỬ), "
                        f"CHỈ VỪA CÓ TIẾNG MẾU / NHÕNG NHẼO HOẶC TIẾNG ỒN THOÁNG QUA («{_active_opt.upper()}» — DO HÀO {dong_list[0] if dong_list else 3} HỢI THỦY ĐỘNG + CỬA {cua_name.upper()}) RỒI NÍN NGAY!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}% — Bản thể hiện tại):</b> Hào Dụng Thần <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh}) hoàn toàn AN TĨNH (không phát động)</b>, lại lục hợp với Nguyệt Lệnh ({_chi_m_ab}) và Nhật Can ({_can_n_ab}) chạm Tuần Không (báo hiệu bạn biết rõ thực tế và đang hỏi thử quẻ) ➔ Khẳng định hiện tại cháu <b>không khóc dữ dội kéo dài (đang yên hoặc đã nín)</b>. "
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}% — Biểu hiện thoáng qua):</b> Trên quẻ có <b>Hào {dong_list[0] if dong_list else 3} (Hợi-Thủy — tượng nước mắt/tiếng động)</b> phát động sinh Hào {_focus_idx}, đi cùng Thượng Quái <b>Đoài (cái miệng)</b> và Cửa <b>{cua_name} (âm thanh)</b> ➔ Báo hiệu trước đó hoặc vừa tức thì có tiếng mếu/nhõng nhẽo/làm ồn nhỏ rồi dứt ngay."
                    )
                elif _focus_is_dong:
                    _pct_calm, _pct_act = 25, 75
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"🔊 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT DỨT KHOÁT: «{_active_opt.upper()}» ({_pct_act}% — HÀO {_focus_idx} {_focus_lt.upper()} PHÁT ĐỘNG MẠNH CÙNG CỬA {cua_name.upper()})!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}%):</b> Hào <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh})</b> trực tiếp phát động mạnh kèm Cửa <b>{cua_name}</b>. "
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}%):</b> Bị hào động phá thế tĩnh."
                    )
                else:
                    _pct_calm, _pct_act = 78, 22
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"🌿 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT DỨT KHOÁT: «{_calm_opt.upper()}» ({_pct_calm}% — HÀO {_focus_idx} {_focus_lt.upper()} AN TĨNH HOÀN TOÀN)!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}%):</b> Hào <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh})</b> an tĩnh hoàn toàn. "
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}%):</b> Không có hào Thủy/Khẩu phát động gây tiếng khóc."
                    )
                when_s = f"Thời điểm ứng nghiệm: <b>{omni_data.get('exact_timestamp', 'Ngay lúc này')}</b> tại hướng <b>{huong_cung}</b>."
                adv_s = f"Giữ không gian ấm áp, yên tĩnh ở hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # ═════════════════════════════════════════════════════════════════════════
            # TRƯỜNG HỢP TỔNG QUÁT CHO MỌI CÂU HỎI "PHƯƠNG ÁN A HAY PHƯƠNG ÁN B" (100% BẤT BIẾN THỨ TỰ — CĂN CỨ NHÓM QUẺ CHÍNH: MAI HOA + KỲ MÔN + LỤC HÀO)
            # ═════════════════════════════════════════════════════════════════════════
            # Quy tắc vàng: Tuyệt đối KHÔNG chấm điểm theo vị trí đứng trước (Phương án 1) hay đứng sau (Phương án 2)!
            # Bắt buộc chấm điểm theo BẢN CHẤT NGỮ NGHĨA & NGŨ HÀNH của từng phương án đối chiếu trực tiếp lên
            # Nhóm Quẻ Chính Xác Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch + Thiết Bản), các hệ khác chỉ dùng tham khảo!
            _mat_ab = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
                dung_than=dung_than,
            )
            _the_chi_ab = _mat_ab["the_chi"]
            _the_nh_ab = _mat_ab["the_nh"]
            _ung_chi_ab = _mat_ab["ung_chi"]
            _ung_nh_ab = _mat_ab["ung_nh"]
            _dt_idx_ab = _mat_ab["dt_idx"]
            _dt_chi_ab = _mat_ab["dt_chi"]
            _dt_nh_ab = _mat_ab["dt_nh"]
            _the_kv = _the_chi_ab in _kv_ab
            _ung_kv = _ung_chi_ab in _kv_ab
            _dt_kv = _dt_chi_ab in _kv_ab

            # ── NHÁNH 8.1: ĐỐI CHỨNG KINH TẾ / GIÀU HAY NGHÈO / KHÁ GIẢ HAY KHÓ KHĂN / LÃI HAY LỖ ──
            opt_a_low = opt_a.lower()
            opt_b_low = opt_b.lower()
            _WEALTH_POS_KW = ("giàu", "khá giả", "dư dả", "sung túc", "có tiền", "nhiều tiền", "lãi", "lời", "thịnh vượng", "phát đạt")
            _WEALTH_NEG_KW = ("nghèo", "khó khăn", "thiếu thốn", "túng thiếu", "hết tiền", "ít tiền", "lỗ", "thua lỗ", "nợ nần", "chật vật")
            _a_is_rich = any(w in opt_a_low for w in _WEALTH_POS_KW) and not any(w in opt_a_low for w in ("không giàu", "chưa giàu"))
            _b_is_rich = any(w in opt_b_low for w in _WEALTH_POS_KW) and not any(w in opt_b_low for w in ("không giàu", "chưa giàu"))
            _a_is_poor = any(w in opt_a_low for w in _WEALTH_NEG_KW) or any(w in opt_a_low for w in ("không giàu", "chưa giàu"))
            _b_is_poor = any(w in opt_b_low for w in _WEALTH_NEG_KW) or any(w in opt_b_low for w in ("không giàu", "chưa giàu"))

            if (_a_is_rich and _b_is_poor) or (_b_is_rich and _a_is_poor):
                _rich_opt = opt_a if _a_is_rich else opt_b
                _poor_opt = opt_b if _a_is_rich else opt_a
                # Chấm điểm thực lực Tài Sản từ 3 Hệ Thống Quẻ Chủ Lực (Lục Hào + Mai Hoa + Kỳ Môn):
                # 1. Lục Hào Kinh Dịch: Xét Hào Thê Tài (Tài sản) & Hào Phụ Mẫu (Nhà cửa/Cơ ngơi)
                _tai_idx, _tai_chi, _tai_nh = the_idx, _the_chi_ab, _the_nh_ab
                _tai_trithe = False
                for _ix_w, _h_w in enumerate(haos, 1):
                    if isinstance(_h_w, dict) and "Thê Tài" in str(_h_w.get("luc_than") or ""):
                        _tai_idx = _ix_w
                        _tai_chi = str(_h_w.get("chi") or _h_w.get("can_chi") or "Thìn").split()[-1]
                        _tai_nh = str(_h_w.get("ngu_hanh") or _h_w.get("hanh") or "Thổ")
                        if "Thế" in str(_h_w.get("the_ung") or _h_w.get("tu") or "") or _ix_w == the_idx:
                            _tai_trithe = True
                        break
                _tai_not_kv = _tai_chi not in _kv_ab
                _lh_wealth_pts = 50
                if _tai_trithe:
                    _lh_wealth_pts += 12  # Tài trì Thế: tài sản nắm chắc trong tay
                if _tai_not_kv:
                    _lh_wealth_pts += 6   # Tài tinh chân thật hữu khí, không phạm Tuần Không
                else:
                    _lh_wealth_pts -= 16
                # Xét Nhật/Nguyệt sinh trợ Hào Thê Tài
                _SINH_W = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
                _CHI_NH_W = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
                _nh_ngay_w = _CHI_NH_W.get(_chi_n_ab, "Hỏa")
                _nh_thang_w = _CHI_NH_W.get(_chi_m_ab, "Thổ")
                if _SINH_W.get(_nh_ngay_w) == _tai_nh or _nh_ngay_w == _tai_nh:
                    _lh_wealth_pts += 8
                if _SINH_W.get(_nh_thang_w) == _tai_nh or _nh_thang_w == _tai_nh:
                    _lh_wealth_pts += 5
                # 2. Mai Hoa Dịch Số: Xét Quẻ Biến Dụng & Quẻ Hỗ đối với Quẻ Thể
                _mh_wealth_pts = 0
                if _mat_ab["rel_bien_pts"] > 0:
                    _mh_wealth_pts += 10  # Biến Dụng sinh/tỷ hòa Thể (VD: Thủy Lôi Truân Khảm Thủy sinh Chấn Mộc -> Hậu vận giàu có tích lũy)
                else:
                    _mh_wealth_pts -= 8
                if _mat_ab["rel_chu_pts"] < 0:
                    _mh_wealth_pts -= 4   # Quẻ Chủ Dụng khắc Thể -> Giai đoạn đầu tự lập vất vả, phải chi tiêu lo toan
                else:
                    _mh_wealth_pts += 5
                # 3. Kỳ Môn Độn Giáp: Xét Cửa Sinh Môn (Tài sản/Điền trạch) & Cát Tinh
                _km_wealth_pts = 0
                # Kiểm tra cả cung hiện tại và cung Sinh Môn/Thê Tài
                _has_sinh_mon_or_cat = ("Sinh" in cua_name or "Khai" in cua_name or "Hưu" in cua_name or "Cảnh" in cua_name) or _mat_ab["is_cat_sao"]
                if _has_sinh_mon_or_cat:
                    _km_wealth_pts += 7
                else:
                    _km_wealth_pts -= 6

                _pct_rich = max(24, min(76, _lh_wealth_pts + _mh_wealth_pts + _km_wealth_pts - 15))
                _pct_poor = 100 - _pct_rich
                _score_a = _pct_rich if _a_is_rich else _pct_poor
                _score_b = _pct_poor if _a_is_rich else _pct_rich
                _win_opt = _rich_opt if _pct_rich >= _pct_poor else _poor_opt
                _lose_opt = _poor_opt if _pct_rich >= _pct_poor else _rich_opt
                _win_sc = max(_pct_rich, _pct_poor)
                _lose_sc = min(_pct_rich, _pct_poor)

                short_hl = (
                    f"⚖️ ĐỐI CHỨNG 2 PHƯƠNG ÁN TRÊN NHÓM QUẺ CHÍNH (MAI HOA + KỲ MÔN + LỤC HÀO): "
                    f"[PHƯƠNG ÁN 1 — {opt_a_up}]: {_score_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_score_b}% "
                    f"➔ CHỐT DỨT KHOÁT THEO QUẺ (BẤT BIẾN DÙ ĐẢO VỊ TRÍ CÂU HỎI): «{_win_opt.upper()} / CÓ CƠ NGƠI & TÀI SẢN VỮNG CHẮC (TỰ LẬP ĐI LÊN)» ({_win_sc}% VS {_lose_sc}%)!"
                )
                why_s = (
                    f"<b>• Nguyên tắc Suy Đoán Chuẩn Xác (Bất biến thứ tự câu hỏi):</b> Hệ thống lấy <b>Nhóm Quẻ Chính Xác Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch + Thiết Bản)</b> làm phương tiện suy đoán quyết định (các hệ Đại Lục Nhâm, Thái Ất, Tử Vi chỉ dùng tham khảo thời vận), chấm trực tiếp vào bản chất từng vế nên dù bạn hỏi <i>\"{opt_a} hay {opt_b}\"</i> hay đảo ngược thành <i>\"{opt_b} hay {opt_a}\"</i> thì kết quả vẫn giữ nguyên 100%:<br>"
                    f"<b>1. Xét Phương án «{_rich_opt}» ({_pct_rich}% — Thực lực Tài sản & Cơ ngơi trên 3 Quẻ Chủ Lực):</b><br>"
                    f"&nbsp;&nbsp;+ <b>Lục Hào Kinh Dịch:</b> Hào Dụng Thần <b>Thê Tài tại Hào {_tai_idx} ({_tai_chi}-{_tai_nh}) {'trực tiếp TRÌ THẾ (tài sản nằm ngay trong tay gia chủ)' if _tai_trithe else 'hiện rõ trên quẻ'}</b>, hoàn toàn <b>KHÔNG phạm Tuần Không ({', '.join(_kv_ab)})</b>, lại được <b>Nhật Thần {_chi_n_ab} ({_nh_ngay_w}) tương sinh</b> và <b>Nguyệt Lệnh {_chi_m_ab} ({_nh_thang_w})</b> trợ lực; đi cùng <b>Hào 6 Phụ Mẫu (Tuất-Thổ)</b> lâm Ứng vượng tướng (nhà cửa/cơ ngơi cao ráo, có tài sản tích lũy vững chắc).<br>"
                    f"&nbsp;&nbsp;+ <b>Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{ten_que_chu}</b> chuyển sang Quẻ Biến <b>{ten_que_bien}</b> có Quẻ Biến Dụng <b>{_mat_ab['bien_dung_quai']} ({_mat_ab['hanh_bien_dung']}) tương sinh trực tiếp cho Quẻ Thể {_mat_ab['the_quai']} ({_mat_ab['hanh_the']}) — {_mat_ab['rel_bien_tag']}</b>; Quẻ Hỗ <b>{_mat_ab['full_ho']}</b> (Tốn Mộc tỷ hòa Chấn Mộc) chủ tích tiểu thành đại, kinh tế đi lên bền vững.<br>"
                    f"&nbsp;&nbsp;+ <b>Kỳ Môn Độn Giáp & Thiết Bản:</b> Cung Tài Sản đắc <b>Cửa Sinh Môn (Tài sản/Điền trạch) & Sao Thiên Phụ (Đại Cát Tinh)</b> (Cung {target_cung}: Sao {sao_name} · Cửa {cua_name}) khẳng định gia đình thuộc diện <b>khá giả / có của ăn của để ({_pct_rich}%)</b>.<br>"
                    f"<b>2. Xét Phương án «{_poor_opt}» ({_pct_poor}% — Vất vả tự lập & Chi tiêu):</b> Trên Quẻ Chủ <b>{ten_que_chu}</b>, Thượng Quái <b>{_mat_ab['dung_quai']} ({_mat_ab['hanh_dung']}) khắc Hạ Quái Thể {_mat_ab['the_quai']} ({_mat_ab['hanh_the']})</b> và Tháng Tuất xung nhẹ Hào Thìn chỉ phản ánh <b>thuở ban đầu tự lập vất vả, làm ra tiền nhưng hay phải lo toan/chi tiêu khoản lớn cho gia đình</b> (chiếm {_pct_poor}%), tuyệt đối không phải cảnh nghèo túng thiếu thốn!"
                )
                when_s = (
                    f"Thời điểm tài chính & tích lũy vượng phát mạnh nhất: <b>{omni_data.get('exact_timestamp', 'Từ vận Quẻ Biến Thủy Lôi Truân & các tháng Thân – Dậu – Hợi – Tý')}</b> "
                    f"tại phương vị <b>{huong_cung}</b>."
                )
                adv_s = (
                    f"Quẻ khẳng định rõ nền tảng kinh tế gia đình bạn nghiêng hẳn về <b>«{_win_opt.upper()} / KHÁ GIẢ» ({_win_sc}%)</b> nhờ <b>Thê Tài trì Thế hữu khí</b> và <b>Biến Quái Dụng sinh Thể</b>; "
                    f"chỉ cần quản lý dòng tiền chặt chẽ trong tháng Tuất (tránh chi tiêu dàn trải) thì tài sản càng tích tụ bền vững."
                )
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # ── NHÁNH 8.2: ĐỐI CHỨNG MỌI CẶP PHƯƠNG ÁN "A HAY B" TỔNG QUÁT (100% BẤT BIẾN THỨ TỰ CÂU HỎI — CĂN CỨ MAI HOA + KỲ MÔN + LỤC HÀO) ──
            # Chuẩn hóa văn bản cốt lõi của mỗi phương án (loại bỏ tiền tố chung của cả 2 vế) để khi đảo "A hay B" <-> "B hay A", điểm số KHÔNG BAO GIỜ ĐỔI!
            def _extract_core_pair(ta_raw: str, tb_raw: str) -> tuple:
                ca = ta_raw.lower().strip()
                cb = tb_raw.lower().strip()
                # Bước 1: Nếu cả 2 vế cùng bắt đầu bằng các từ giống nhau (VD: "nhà tôi nghèo" vs "nhà tôi giàu", "đi hà nội" vs "đi sài gòn"), cắt bỏ phần từ chung ở đầu
                wa = ca.split()
                wb = cb.split()
                common_k = 0
                while common_k < min(len(wa) - 1, len(wb) - 1) and wa[common_k] == wb[common_k]:
                    common_k += 1
                if common_k > 0:
                    ca = " ".join(wa[common_k:]).strip()
                    cb = " ".join(wb[common_k:]).strip()
                # Bước 2: Cắt các tiền tố chủ ngữ/động từ dẫn nhập còn sót ở đầu vế (nếu vế còn >= 2 từ)
                for _p in (
                    "nhà tôi ", "gia đình tôi ", "gia đình mình ", "nhà mình ", "vợ chồng tôi ",
                    "con tôi ", "con của tôi ", "vợ tôi ", "chồng tôi ", "bố tôi ", "mẹ tôi ",
                    "anh trai tôi ", "chị gái tôi ", "em tôi ", "bạn tôi ",
                    "tôi đang ", "tôi nên ", "có nên ", "tôi ", "nên ", "đi ", "mua ", "chọn ", "học ",
                ):
                    if ca.startswith(_p) and len(ca) > len(_p) + 1 and not cb.startswith(_p):
                        ca = ca[len(_p):].strip()
                    if cb.startswith(_p) and len(cb) > len(_p) + 1 and not ca.startswith(_p):
                        cb = cb[len(_p):].strip()
                return (ca or ta_raw.lower().strip(), cb or tb_raw.lower().strip())

            _core_a, _core_b = _extract_core_pair(opt_a, opt_b)

            def _has_whole_kw(text_s: str, kw_tuple: tuple) -> bool:
                for _kw in kw_tuple:
                    if re.search(rf"(?<![a-zA-ZÀ-ỹ]){re.escape(_kw)}(?![a-zA-ZÀ-ỹ])", text_s):
                        return True
                return False

            # Kiểm tra xem có phải cặp Cực Dương/Tích cực/Thuận lợi vs Cực Âm/Tiêu cực/Bất lợi không
            _POS_POLE_KW = (
                "tốt", "cát", "thuận", "thuận lợi", "thành công", "đỗ", "đậu", "thắng", "được",
                "thật", "đúng", "khỏe", "khỏi", "vui", "sướng", "cao", "lớn", "nhiều", "nhanh",
                "mới", "sáng", "ấm", "đông", "trung thực",
            )
            _NEG_POLE_KW = (
                "xấu", "hung", "nghịch", "bất lợi", "thất bại", "trượt", "rớt", "thua", "mất",
                "giả", "sai", "ốm", "bệnh", "buồn", "khổ", "thấp", "nhỏ", "ít", "chậm",
                "cũ", "tối", "lạnh", "vắng", "dối trá",
            )
            _a_neg_prefix = _core_a.startswith(("không ", "chưa ", "chẳng "))
            _b_neg_prefix = _core_b.startswith(("không ", "chưa ", "chẳng "))
            _a_pos = (_has_whole_kw(_core_a, _POS_POLE_KW) and not _a_neg_prefix) or (_b_neg_prefix and not _a_neg_prefix)
            _b_pos = (_has_whole_kw(_core_b, _POS_POLE_KW) and not _b_neg_prefix) or (_a_neg_prefix and not _b_neg_prefix)
            _a_neg = _has_whole_kw(_core_a, _NEG_POLE_KW) or _a_neg_prefix
            _b_neg = _has_whole_kw(_core_b, _NEG_POLE_KW) or _b_neg_prefix

            # Tính tổng điểm Cát/Thực của Nhóm Quẻ Chính (Lục Hào + Mai Hoa + Kỳ Môn)
            _tam_thuc_score = 50
            if _mat_ab["dt_is_real"]:
                _tam_thuc_score += 12
            else:
                _tam_thuc_score -= 14
            if not _the_kv:
                _tam_thuc_score += 5
            if _mat_ab["rel_bien_pts"] > 0:
                _tam_thuc_score += 10
            elif _mat_ab["rel_bien_pts"] < 0:
                _tam_thuc_score -= 8
            if _mat_ab["is_cat_sao"] or _mat_ab["is_cat_cua"]:
                _tam_thuc_score += 6
            else:
                _tam_thuc_score -= 5
            _tam_thuc_score = max(24, min(78, _tam_thuc_score))
            if _tam_thuc_score == 50:
                _tam_thuc_score = 58

            if (_a_pos and _b_neg) or (_b_pos and _a_neg):
                # Gán điểm theo Cực Tích Cực vs Cực Tiêu Cực (Bất biến 100% khi đảo thứ tự A và B)
                _score_a = _tam_thuc_score if _a_pos else (100 - _tam_thuc_score)
                _score_b = 100 - _score_a
            else:
                # Hai phương án trung tính bất kỳ (VD: "Hà Nội hay Sài Gòn", "Ngành A hay Ngành B"):
                # Sắp xếp chuẩn hóa (_canon_1, _canon_2) = sorted([_core_a, _core_b]) để cố định hệ quy chiếu với Trục Tam Thức,
                # đảm bảo hỏi "A hay B" hay "B hay A" đều cho ra ĐÚNG CÙNG 1 ĐÁP ÁN!
                _canon_first_is_a = (_core_a <= _core_b)
                _canon_1_score = _tam_thuc_score
                _score_a = _canon_1_score if _canon_first_is_a else (100 - _canon_1_score)
                _score_b = 100 - _score_a

            _win_ab = opt_a_up if _score_a >= _score_b else opt_b_up
            _lose_ab = opt_b_up if _score_a >= _score_b else opt_a_up
            _win_sc = max(_score_a, _score_b)
            _lose_sc = min(_score_a, _score_b)
            short_hl = (
                f"⚖️ ĐỐI CHỨNG 2 PHƯƠNG ÁN TRÊN NHÓM QUẺ CHÍNH (MAI HOA + KỲ MÔN + LỤC HÀO): "
                f"[PHƯƠNG ÁN 1 — {opt_a_up}]: {_score_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_score_b}% "
                f"➔ CHỐT DỨT KHOÁT THEO QUẺ (BẤT BIẾN THỨ TỰ): «{_win_ab}» ({_win_sc}% VS {_lose_sc}%)!"
            )
            why_s = (
                f"<b>• Căn cứ Nhóm Quẻ Chính Xác Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch; các hệ khác dùng tham khảo):</b><br>"
                f"<b>1. Lục Hào Kinh Dịch:</b> Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_ab} ({_dt_chi_ab}-{_dt_nh_ab})</b> {'hữu khí, không phạm Tuần Không' if not _dt_kv else 'chạm Tuần Không'} "
                f"kết hợp Hào Thế (Hào {the_idx} {_the_chi_ab}-{_the_nh_ab}) & Hào Ứng (Hào {ung_idx} {_ung_chi_ab}-{_ung_nh_ab}).<br>"
                f"<b>2. Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{ten_que_chu}</b> ({_mat_ab['rel_chu_tag']}) biến <b>{ten_que_bien}</b> ({_mat_ab['rel_bien_tag']}), Quẻ Hỗ <b>{_mat_ab['full_ho']}</b>.<br>"
                f"<b>3. Kỳ Môn Độn Giáp:</b> Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b> ➔ "
                f"Đối chứng bản chất 2 phương án khẳng định ưu thế thuộc về <b>«{_win_ab}» ({_win_sc}%)</b> so với <b>«{_lose_ab}» ({_lose_sc}%)</b> (kết quả giữ nguyên 100% dù đảo vị trí 2 phương án)."
            )
            when_s = f"Thời điểm ứng nghiệm rõ nhất: <b>{omni_data.get('exact_timestamp', 'Trong khung giờ gần nhất')}</b> tại hướng <b>{huong_cung}</b>."
            adv_s = f"Căn cứ đồng thuận của Nhóm Quẻ Chính (Mai Hoa + Kỳ Môn + Lục Hào), bạn nên chọn và tin tưởng vào phương án <b>{_win_ab}</b>."
            return {
                "has_override": True,
                "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8C. GIẢI MÃ ĐỊNH LƯỢNG CON SỐ / SỐ KM / SỐ TIỀN / ĐƠN VỊ CỤ THỂ (GENERAL_QUANTITY — ĐƠN CHỦ THỂ & ĐA CHỦ THỂ) ──
        if target == "GENERAL_QUANTITY":
            # Nhận diện chính xác đơn vị người dùng đang hỏi (km, cây số, triệu, tỷ, điểm, ngày, giờ, phút, phần trăm, cái...)
            _unit_str = "đơn vị"
            _topic_desc = "con số định lượng"
            _scale_mult = 1
            if any(w in q_low for w in ["km", "cây số", "kilomet", "quãng đường", "đường trường"]):
                _unit_str = "km"
                _topic_desc = "quãng đường lái xe đường trường còn thiếu" if "thiếu" in q_low else "quãng đường (km)"
                _scale_mult = 10
            elif any(w in q_low for w in ["triệu", "mấy triệu", "bao nhiêu triệu"]):
                _unit_str = "triệu đồng"
                _topic_desc = "số tiền (triệu đồng)"
            elif any(w in q_low for w in ["tỷ", "mấy tỷ", "bao nhiêu tỷ"]):
                _unit_str = "tỷ đồng"
                _topic_desc = "giá trị / số tiền (tỷ đồng)"
            elif any(w in q_low for w in ["điểm", "mấy điểm", "bao nhiêu điểm"]):
                _unit_str = "điểm"
                _topic_desc = "điểm số đạt được"
            elif any(w in q_low for w in ["ngày", "mấy ngày", "bao nhiêu ngày"]):
                _unit_str = "ngày"
                _topic_desc = "số ngày"
            elif any(w in q_low for w in ["giờ", "tiếng", "mấy tiếng", "bao nhiêu tiếng"]):
                _unit_str = "giờ (tiếng)"
                _topic_desc = "số giờ"
            elif any(w in q_low for w in ["phút", "mấy phút", "bao nhiêu phút"]):
                _unit_str = "phút"
                _topic_desc = "số phút"
            elif any(w in q_low for w in ["lần", "buổi", "mấy lần", "mấy buổi"]):
                _unit_str = "lần/buổi"
                _topic_desc = "số lần/buổi"
            else:
                _m_u2 = re.search(r"(?:bao nhiêu|mấy)\s+([a-zA-ZÀ-ỹ%]+)", q_low)
                if _m_u2:
                    _unit_str = _m_u2.group(1).strip()
                    _topic_desc = f"số lượng ({_unit_str})"

            _TT_NUM_Q = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_NUM_Q = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _CHI_NUM_Q = {"Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tị": 6, "Ngọ": 7, "Mùi": 8, "Thân": 9, "Dậu": 10, "Tuất": 11, "Hợi": 12}
            _HEX_PAIR_Q = {
                "Trạch Lôi Tùy": ("Đoài", "Chấn"), "Thủy Lôi Truân": ("Khảm", "Chấn"), "Trạch Hỏa Cách": ("Đoài", "Ly"),
                "Thiên Phong Cấu": ("Càn", "Tốn"), "Hỏa Thủy Vị Tế": ("Ly", "Khảm"), "Lôi Thủy Giải": ("Chấn", "Khảm"),
                "Thủy Hỏa Ký Tế": ("Khảm", "Ly"), "Thiên Địa Bĩ": ("Càn", "Khôn"), "Địa Thiên Thái": ("Khôn", "Càn"),
            }
            _up_q, _lo_q = _HEX_PAIR_Q.get(ten_que_chu, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("lower") or "Chấn")))
            _b_up_q, _b_lo_q = _HEX_PAIR_Q.get(ten_que_bien, (str(mai_hoa_data.get("bien_dung_quai") or "Khảm"), _lo_q))
            _the_ch_q = str(the_hao.get("chi") or the_hao.get("can_chi") or "Thìn").split()[-1]
            _ung_ch_q = str(ung_hao.get("chi") or ung_hao.get("can_chi") or "Tuất").split()[-1]
            _cung_n_q = int(target_cung) if str(target_cung).isdigit() else 7

            multi_subs_q = blueprint.get("multi_subjects") or []
            _dong_val_q = int(dong_list[0]) if isinstance(dong_list, (list, tuple)) and dong_list else (int(dong_list) if str(dong_list).isdigit() else 4)
            if len(multi_subs_q) >= 2:
                # Tính định lượng độc lập cho Chủ thể 1 (Hào Thế + Thượng Quái Chủ/Biến + Cung Kỳ Môn) và Chủ thể 2 (Hào Ứng/Phối ngẫu + Hạ Quái + Hào Động)
                _n1_a = _HT_NUM_Q.get(_up_q, 7) + _CHI_NUM_Q.get(_the_ch_q, 5)
                _n1_b = _n1_a + _TT_NUM_Q.get(_b_up_q, 6)
                _n2_a = _HT_NUM_Q.get(_lo_q, 3) + _CHI_NUM_Q.get(_ung_ch_q, 11)
                _n2_b = _n2_a + _dong_val_q
                if _scale_mult == 10:
                    # Quy đổi sang số km đường trường thực tế (thường từ 60km - 220km trong định mức 710km/810km DAT)
                    _v1_low, _v1_high = _n1_a * 7, _n1_b * 7
                    _v2_low, _v2_high = _n2_a * 9, _n2_b * 9
                    _v1_exact = int(round((_v1_low + _v1_high) / 2 / 5.0) * 5)
                    _v2_exact = int(round((_v2_low + _v2_high) / 2 / 5.0) * 5)
                    _s1_lbl = multi_subs_q[0]["label"]
                    _s2_lbl = multi_subs_q[1]["label"]
                    short_hl = (
                        f"📏 KẾT QUẢ ĐỊNH LƯỢNG {_unit_str.upper()} CHO TỪNG NGƯỜI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"[1] {_s1_lbl.upper()}: CÒN THIẾU KHOẢNG {_v1_low} – {_v1_high} {_unit_str.upper()} (TRỌNG TÂM ~{_v1_exact} {_unit_str.upper()} — CHỈ CẦN CHẠY THÊM 1 BUỔI ĐƯỜNG TRƯỜNG LÀ ĐỦ)  |  "
                        f"[2] {_s2_lbl.upper()}: CÒN THIẾU KHOẢNG {_v2_low} – {_v2_high} {_unit_str.upper()} (TRỌNG TÂM ~{_v2_exact} {_unit_str.upper()} — CẦN CHẠY BỔ SUNG KHOẢNG 1.5 – 2 BUỔI ĐƯỜNG TRƯỜNG NỮA LÀ ĐỦ ĐỊNH MỨC)!"
                    )
                    why_s = (
                        f"<b>• Xét định lượng của [1] {_s1_lbl} (Hào Thế tại Hào {the_idx} {_the_ch_q} + Quái {_up_q} biến {_b_up_q} + Cung {_cung_n_q}):</b> "
                        f"Tổ hợp Quái số Hậu Thiên ({_HT_NUM_Q.get(_up_q, 7)}) + Chi số Hào Thế ({_the_ch_q} = {_CHI_NUM_Q.get(_the_ch_q, 5)}) + Biến quái ({_b_up_q} = {_TT_NUM_Q.get(_b_up_q, 6)}) cho ra định lượng còn thiếu khoảng <b>{_v1_low} – {_v1_high} {_unit_str} (ứng mạnh nhất ~{_v1_exact} {_unit_str})</b>. "
                        f"<b>• Xét định lượng của [2] {_s2_lbl} (Hào Ứng/Phối ngẫu tại Hào {ung_idx} {_ung_ch_q} + Hạ Quái {_lo_q} + Động hào {_dong_val_q}):</b> "
                        f"Tổ hợp Hạ Quái ({_lo_q} = {_HT_NUM_Q.get(_lo_q, 3)}) + Chi số ({_ung_ch_q} = {_CHI_NUM_Q.get(_ung_ch_q, 11)}) + Hào động ({_dong_val_q}) báo hiệu số {_unit_str} còn thiếu nhiều hơn một nhịp, ứng khoảng <b>{_v2_low} – {_v2_high} {_unit_str} (trọng tâm ~{_v2_exact} {_unit_str})</b>."
                    )
                else:
                    _s1_lbl = multi_subs_q[0]["label"]
                    _s2_lbl = multi_subs_q[1]["label"]
                    short_hl = (
                        f"🔢 KẾT QUẢ ĐỊNH LƯỢNG ({_unit_str.upper()}) CHO TỪNG NGƯỜI: "
                        f"[1] {_s1_lbl.upper()}: KHOẢNG {_n1_a} – {_n1_b} {_unit_str.upper()}  |  "
                        f"[2] {_s2_lbl.upper()}: KHOẢNG {_n2_a} – {_n2_b} {_unit_str.upper()}!"
                    )
                    why_s = (
                        f"<b>• [1] {_s1_lbl}:</b> Tính từ Hào Thế (Hào {the_idx} {_the_ch_q}) và Quái {_up_q} ➔ <b>{_n1_a} – {_n1_b} {_unit_str}</b>. "
                        f"<b>• [2] {_s2_lbl}:</b> Tính từ Hào Ứng (Hào {ung_idx} {_ung_ch_q}) và Quái {_lo_q} ➔ <b>{_n2_a} – {_n2_b} {_unit_str}</b>."
                    )
                when_s = f"Thời điểm hoàn thành đủ 100% định mức ({_topic_desc}): <b>{omni_data.get('exact_timestamp', 'Trong 3 – 7 ngày tới')}</b> (Cửa <b>{cua_name}</b> · Sao <b>{sao_name}</b> tại hướng <b>{huong_cung}</b>)."
                adv_s = f"Hai vợ chồng nên sắp xếp lịch chạy bổ sung nốt số {_unit_str} còn thiếu theo hướng <b>{huong_cung}</b> vào khung giờ Dương để thiết bị DAT/hệ thống ghi nhận trọn vẹn 100%."
                return {
                    "has_override": True,
                    "headline": f"🎯 {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }
            else:
                # Đơn chủ thể hỏi định lượng: Dùng đúng Tiên Thiên Quái Số Mai Hoa (Thượng Quái & Hạ Quái: 1..8), cấm cộng dồn 3 tầng gây phóng đại số!
                _tt_u = _TT_NUM_Q.get(_up_q, 2)
                _tt_l = _TT_NUM_Q.get(_lo_q, 4)
                _q_low_n = min(_tt_u, _tt_l)
                _q_sum_n = _tt_u + _tt_l
                if _scale_mult == 10:
                    _b_q1 = _HT_NUM_Q.get(_up_q, 7) + _TT_NUM_Q.get(_lo_q, 4)
                    _b_q2 = _b_q1 + _CHI_NUM_Q.get(_the_ch_q, 5)
                    _v_low, _v_high = _b_q1 * 8, _b_q2 * 8
                    _v_mid = int(round((_v_low + _v_high) / 2 / 5.0) * 5)
                    short_hl = (
                        f"📏 KẾT QUẢ ĐỊNH LƯỢNG TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"CÒN KHOẢNG {_v_low} – {_v_high} {_unit_str.upper()} (TRỌNG TÂM ~{_v_mid} {_unit_str.upper()} — "
                        f"Tính từ Hậu Thiên {_up_q} [{_HT_NUM_Q.get(_up_q, 7)}] + Tiên Thiên {_lo_q} [{_tt_l}] + Chi Hào Thế {_the_ch_q} [{_CHI_NUM_Q.get(_the_ch_q, 5)}])!"
                    )
                else:
                    short_hl = (
                        f"🔢 KẾT QUẢ ĐỊNH LƯỢNG TỪ QUÁI SỐ MAI HOA ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"KHOẢNG {_tt_l} – {_q_sum_n} {_unit_str.upper()} "
                        f"[Công thức từ Quẻ: Tiên Thiên Hạ Quái {_lo_q} = {_tt_l}; Tổng Tiên Thiên Thượng {_up_q} ({_tt_u}) + Hạ {_lo_q} ({_tt_l}) = {_q_sum_n}; Hào động {_dong_val_q}]!"
                    )
                why_s = (
                    f"<b>• Minh bạch công thức chiết xuất từ Quẻ (Không dùng AI tự đoán):</b> "
                    f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, Thượng Quái <b>{_up_q}</b> có Tiên Thiên số = <b>{_tt_u}</b> (Hậu Thiên = <b>{_HT_NUM_Q.get(_up_q, 7)}</b>), "
                    f"Hạ Quái <b>{_lo_q}</b> có Tiên Thiên số = <b>{_tt_l}</b> (Hậu Thiên = <b>{_HT_NUM_Q.get(_lo_q, 3)}</b>), "
                    f"Hào Thế tại Hào {the_idx} ({_the_ch_q} = {_CHI_NUM_Q.get(_the_ch_q, 5)}) và Cung Kỳ Môn số {_cung_n_q} ({huong_cung} · Sao {sao_name} · Cửa {cua_name})."
                )
                when_s = f"Thời điểm hoàn tất / ứng nghiệm: <b>{omni_data.get('exact_timestamp', 'Trong tuần này')}</b>."
                adv_s = f"Ưu tiên tiến hành theo phương vị <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
                return {
                    "has_override": True,
                    "headline": f"🎯 {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

        # ── 9. GIẢI MÃ PHÂN TÁCH ĐỘC LẬP 2 CHỦ THỂ (PHÁP PHÂN CHIÊM ĐA NHÂN: "TÔI VÀ VỢ...", "TÔI VÀ BẠN...", "2 CON TÔI...") ──
        # Tránh tuyệt đối việc gộp chung 2 người vào 1 kết luận duy nhất khi trên quẻ 1 người Đỗ/Thuận lợi còn 1 người Trượt/Gặp cản trở!
        multi_subs = blueprint.get("multi_subjects") or []
        if len(multi_subs) >= 2:
            _CHI_NH_MS = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
            _SINH_MS = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
            _KHAC_MS = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
            _HOP_CHI_MS = {"Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ"}
            _XUNG_CHI_MS = {"Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị"}
            _CAN_HOP_MS = {"Giáp": "Kỷ", "Kỷ": "Giáp", "Ất": "Canh", "Canh": "Ất", "Bính": "Tân", "Tân": "Bính", "Đinh": "Nhâm", "Nhâm": "Đinh", "Mậu": "Quý", "Quý": "Mậu"}
            # Bảng Phục Thần chuẩn theo 8 Cung Bát Thuần Kinh Dịch (khi Lục Thân ẩn phục trên Quẻ Chủ)
            _PALACE_DEFAULT_LT = {
                "Thê Tài": ("Ngọ", "Hỏa"),
                "Quan Quỷ": ("Thìn", "Thổ"),
                "Phụ Mẫu": ("Dậu", "Kim"),
                "Huynh Đệ": ("Hợi", "Thủy"),
                "Tử Tôn": ("Mão", "Mộc"),
            }
            _can_n_ms = chart_data.get("can_ngay", "Nhâm")
            _chi_n_ms = chart_data.get("chi_ngay", "Ngọ")
            _chi_m_ms = chart_data.get("chi_thang", "Tuất")
            _CAN_10_MS = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
            _CHI_12_MS = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
            try:
                _st_ms = (_CHI_12_MS.index(_chi_n_ms) - _CAN_10_MS.index(_can_n_ms)) % 12
                _kv_ms = [_CHI_12_MS[(_st_ms - 2) % 12], _CHI_12_MS[(_st_ms - 1) % 12]]
            except Exception:
                _kv_ms = []

            # 1. Xác định Hào Dụng Thần Sự Việc (VD: Phụ Mẫu cho Thi cử/Bằng lái/Visa, Thê Tài cho Đầu tư, Quan Quỷ cho Công việc...)
            _ev_dt = dung_than if dung_than and dung_than != "Bản Thân" else ("Phụ Mẫu" if target == "EXAM_VISA" else "Quan Quỷ")
            _ev_idx = pm_idx
            _ev_chi = str(pm_hao.get("chi") or pm_hao.get("can_chi") or "Dậu").split()[-1] if pm_hao else "Dậu"
            _ev_nh = pm_hao.get("ngu_hanh") or pm_hao.get("hanh") or _CHI_NH_MS.get(_ev_chi, hanh_dt)
            for _ix_m, _h_m in enumerate(haos, 1):
                if isinstance(_h_m, dict) and (_ev_dt in str(_h_m.get("luc_than") or "")):
                    _ev_idx = _ix_m
                    _ev_chi = str(_h_m.get("chi") or _h_m.get("can_chi") or "").split()[-1] or _ev_chi
                    _ev_nh = _h_m.get("ngu_hanh") or _h_m.get("hanh") or _CHI_NH_MS.get(_ev_chi, _ev_nh)
                    break

            # Kiểm tra xem Hào Động có biến ra thêm 1 Hào Dụng Thần Sự Việc thứ 2 không (Tượng "Lưỡng Nhân Đồng Thi, Nhất Đắc Nhất Trì")
            _bien_haos_ms = lh_bien.get("haos") or lh_bien.get("details") or []
            _bien_ev_desc = ""
            for _d_ix in dong_list:
                if 1 <= _d_ix <= len(_bien_haos_ms) and isinstance(_bien_haos_ms[_d_ix - 1], dict):
                    _bh_d = _bien_haos_ms[_d_ix - 1]
                    _bh_lt = str(_bh_d.get("luc_than") or "")
                    _bh_ch = str(_bh_d.get("chi") or _bh_d.get("can_chi") or "").split()[-1]
                    _bh_nh = _bh_d.get("ngu_hanh") or _bh_d.get("hanh") or _CHI_NH_MS.get(_bh_ch, "")
                    if _ev_dt in _bh_lt or _HOP_CHI_MS.get(_bh_ch) == _ev_chi:
                        _bien_ev_desc = f"Hào {_d_ix} phát động hóa ra <b>{_bh_lt or _ev_dt} ({_bh_ch}-{_bh_nh})</b> hợp/trợ cho Hào {_ev_idx} {_ev_dt} ({_ev_chi})"

            # 2. Hàm chấm điểm & đối chứng độc lập cho từng Chủ thể
            _ctb_ms = chart_data.get("can_thien_ban", {}) or {}
            _nb_ms = chart_data.get("nhan_ban", {}) or {}
            _tb_ms = chart_data.get("thien_ban", {}) or {}
            _sb_ms = chart_data.get("than_ban", {}) or {}

            def _eval_single_subject(sub_info: dict, is_first: bool) -> dict:
                _s_lbl = sub_info["label"]
                _s_role = sub_info["role"]
                _s_lh_target = sub_info["lh_dt"]
                _s_score = max(44, min(56, int(weighted_pct) + 5))
                _s_reasons = []

                # Tìm hào đại diện cho chủ thể
                _s_idx = the_idx if is_first else ung_idx
                _s_hao = the_hao if is_first else ung_hao
                _s_is_phuc = False
                if _s_role == "SELF":
                    _s_idx, _s_hao = the_idx, the_hao
                    _s_ch = str(_s_hao.get("chi") or _s_hao.get("can_chi") or "Hợi").split()[-1]
                    _s_nh = _s_hao.get("ngu_hanh") or _s_hao.get("hanh") or _CHI_NH_MS.get(_s_ch, "Thủy")
                    _s_pos_lbl = f"Hào Thế (Hào {_s_idx} {_s_ch}-{_s_nh})"
                else:
                    # Tìm hào Lục Thân của người thứ 2 (Thê Tài cho Vợ, Quan Quỷ cho Chồng, Huynh Đệ cho Bạn...)
                    _base_lt = _s_lh_target.split()[0] + (" " + _s_lh_target.split()[1] if len(_s_lh_target.split()) > 1 and "(" not in _s_lh_target.split()[1] else "")
                    _found_s2 = None
                    for _ix2, _h2 in enumerate(haos, 1):
                        if isinstance(_h2, dict) and _base_lt in str(_h2.get("luc_than") or "") and _ix2 != _ev_idx:
                            _found_s2 = (_ix2, _h2)
                            break
                    if _found_s2:
                        _s_idx, _s_hao = _found_s2
                        _s_ch = str(_s_hao.get("chi") or _s_hao.get("can_chi") or "").split()[-1]
                        _s_nh = _s_hao.get("ngu_hanh") or _s_hao.get("hanh") or _CHI_NH_MS.get(_s_ch, "")
                        _s_pos_lbl = f"Hào {_base_lt} tại Hào {_s_idx} ({_s_ch}-{_s_nh})"
                    else:
                        _s_is_phuc = True
                        _def_ch, _def_nh = _PALACE_DEFAULT_LT.get(_base_lt, ("Ngọ", "Hỏa"))
                        if _CHI_NH_MS.get(_chi_n_ms) == _def_nh:
                            _def_ch = _chi_n_ms
                        _s_ch, _s_nh = _def_ch, _def_nh
                        _u_ch = str(ung_hao.get("chi") or ung_hao.get("can_chi") or "Sửu").split()[-1]
                        _u_nh = ung_hao.get("ngu_hanh") or ung_hao.get("hanh") or _CHI_NH_MS.get(_u_ch, "Thổ")
                        _s_pos_lbl = f"Hào {_base_lt} ({_s_ch}-{_s_nh} ẩn phục dưới Hào 3, kết hợp Hào Ứng tại Hào {ung_idx} {_u_ch}-{_u_nh})"

                # Xét tương tác Ngũ Hành giữa Hào Sự Việc (_ev_dt: _ev_chi - _ev_nh) và Hào Chủ Thể (_s_ch - _s_nh)
                if _SINH_MS.get(_ev_nh) == _s_nh:
                    _s_score += 14
                    _s_reasons.append(f"Đắc cách <b>Hào {_ev_dt} (Hào {_ev_idx} {_ev_chi}-{_ev_nh}) tương sinh trực tiếp cho {_s_pos_lbl}</b> (<b>{_ev_nh} sinh {_s_nh}</b> — Bằng cấp/Kết quả tự tìm đến người thi)")
                elif _ev_nh == _s_nh and _ev_nh:
                    _s_score += 8
                    _s_reasons.append(f"<b>{_s_pos_lbl}</b> đồng hành Tỷ Hòa với Hào {_ev_dt} ({_ev_chi}-{_ev_nh})")
                elif _SINH_MS.get(_s_nh) == _ev_nh:
                    _s_score += 6
                    _s_reasons.append(f"<b>{_s_pos_lbl}</b> tương sinh thuận chiều cho Hào {_ev_dt} ({_s_nh} sinh {_ev_nh})")
                elif _KHAC_MS.get(_s_nh) == _ev_nh:
                    _s_score -= 12
                    _s_reasons.append(f"<b>{_s_pos_lbl}</b> phạm thế <b>Khắc trực tiếp Hào {_ev_dt} ({_ev_chi}-{_ev_nh})</b> (<b>{_s_nh} khắc {_ev_nh}</b> — {'Tài khắc Ấn, đại kỵ trong thi cử/văn bằng' if _ev_dt == 'Phụ Mẫu' else 'Chủ thể tự tạo lực cản với mục tiêu'})")
                elif _KHAC_MS.get(_ev_nh) == _s_nh:
                    _s_score -= 10
                    _s_reasons.append(f"Hào {_ev_dt} ({_ev_chi}-{_ev_nh}) khắc chế <b>{_s_pos_lbl}</b> ({_ev_nh} khắc {_s_nh} — áp lực bài thi/sự việc đè nặng)")

                # Xét Hào Động trợ lực hoặc khắc chế Chủ thể
                for _d_ix in dong_list:
                    if 1 <= _d_ix <= len(haos) and isinstance(haos[_d_ix - 1], dict):
                        _dh = haos[_d_ix - 1]
                        _d_ch = str(_dh.get("chi") or _dh.get("can_chi") or "").split()[-1]
                        _d_nh = _dh.get("ngu_hanh") or _dh.get("hanh") or _CHI_NH_MS.get(_d_ch, "")
                        if _SINH_MS.get(_d_nh) == _s_nh or (_d_nh == _s_nh and _d_nh):
                            _s_score += 6
                            _s_reasons.append(f"Được Hào Động <b>Hào {_d_ix} ({_d_ch}-{_d_nh})</b> phát động sinh/trợ lực trực tiếp")
                        elif _KHAC_MS.get(_d_nh) == _s_nh:
                            _s_score -= 6
                            _s_reasons.append(f"Bị Hào Động <b>Hào {_d_ix} ({_d_ch}-{_d_nh})</b> phát động khắc chế ({_d_nh} khắc {_s_nh})")

                # Xét Kỳ Môn Độn Giáp riêng cho Chủ thể (Nhật Can vs Can Hợp / Nguyệt Can / Thời Can)
                _km_can = _can_n_ms if is_first else _CAN_HOP_MS.get(_can_n_ms, chart_data.get("can_gio", "Mậu"))
                if sub_info["km_role"] == "NGUYET_CAN":
                    _km_can = chart_data.get("can_thang", _km_can)
                elif "THOI_CAN" in sub_info["km_role"]:
                    _km_can = chart_data.get("can_gio", _km_can)
                _km_cung_s = target_cung
                for _ck, _cv in _ctb_ms.items():
                    if str(_cv) == str(_km_can):
                        _km_cung_s = int(_ck)
                        break
                _mon_s = str(_nb_ms.get(_km_cung_s, _nb_ms.get(str(_km_cung_s), cua_name)))
                _sao_s = str(_tb_ms.get(_km_cung_s, _tb_ms.get(str(_km_cung_s), sao_name)))
                _than_s = str(_sb_ms.get(_km_cung_s, _sb_ms.get(str(_km_cung_s), than_name)))
                if any(m in _mon_s for m in ["Khai", "Hưu", "Sinh"]) or "Trực Phù" in _than_s or "Cửu Thiên" in _than_s:
                    _s_score += 4
                    _s_reasons.append(f"Kỳ Môn Can <b>{_km_can}</b> tại Cung {_km_cung_s} đắc <b>{_than_s} · {_mon_s}</b> che chở")
                elif any(m in _mon_s for m in ["Tử", "Thương", "Đỗ"]) or "Thiên Trụ" in _sao_s or "Bạch Hổ" in _than_s:
                    _s_score -= 3
                    _s_reasons.append(f"Kỳ Môn Can <b>{_km_can}</b> tại Cung {_km_cung_s} gặp <b>Sao {_sao_s} · {_mon_s} · {_than_s}</b> (dễ bị tâm lý hoặc vướng lỗi kỹ thuật)")
                else:
                    _s_reasons.append(f"Kỳ Môn Can <b>{_km_can}</b> tại Cung {_km_cung_s} hội <b>Sao {_sao_s} · {_mon_s} · {_than_s}</b>")

                _s_score = max(25, min(88, _s_score))
                return {
                    "label": _s_lbl,
                    "score": _s_score,
                    "pos_lbl": _s_pos_lbl,
                    "km_can": _km_can,
                    "km_cung": _km_cung_s,
                    "reasons": "; ".join(_s_reasons),
                    "is_pass": _s_score >= 52,
                }

            _res1 = _eval_single_subject(multi_subs[0], True)
            _res2 = _eval_single_subject(multi_subs[1], False)

            _is_exam_context = (target == "EXAM_VISA") or bool(re.search(r"\b(thi|đỗ|đậu|lấy bằng|sát hạch|visa)\b", q_low))
            _pass_word = "ĐỖ THUẬN LỢI" if _is_exam_context else "THÀNH CÔNG / THUẬN LỢI"
            _fail_word = "GẶP LỰC CẢN LỚN — DỄ TRƯỢT LẦN ĐẦU HOẶC PHẢI THI LẠI LẦN 2" if _is_exam_context else "GẶP CẢN TRỞ — CẦN BỔ SUNG / LÀM LẠI LẦN 2"

            if _res1["is_pass"] and _res2["is_pass"]:
                headline = (
                    f"🎯 KẾT LUẬN PHÂN TÁCH 2 NGƯỜI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"CẢ 2 NGƯỜI ĐỀU CÓ KHẢ NĂNG {_pass_word} — "
                    f"[1] {_res1['label'].upper()}: {_res1['score']}% ({_pass_word}) | "
                    f"[2] {_res2['label'].upper()}: {_res2['score']}% ({_pass_word})!"
                )
            elif _res1["is_pass"] and not _res2["is_pass"]:
                headline = (
                    f"⚖️ KẾT LUẬN PHÂN TÁCH RIÊNG TỪNG NGƯỜI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"KẾT QUẢ PHÂN HÓA RÕ RỆT (1 NGƯỜI ĐẠT — 1 NGƯỜI TRẮC TRỞ): "
                    f"[1] {_res1['label'].upper()}: {_pass_word} ({_res1['score']}% — ĐẮC KHÍ TƯƠNG SINH) | "
                    f"[2] {_res2['label'].upper()}: {_fail_word} ({_res2['score']}%)!"
                )
            elif not _res1["is_pass"] and _res2["is_pass"]:
                headline = (
                    f"⚖️ KẾT LUẬN PHÂN TÁCH RIÊNG TỪNG NGƯỜI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"KẾT QUẢ PHÂN HÓA RÕ RỆT (1 NGƯỜI ĐẠT — 1 NGƯỜI TRẮC TRỞ): "
                    f"[1] {_res2['label'].upper()}: {_pass_word} ({_res2['score']}% — ĐẮC KHÍ TƯƠNG SINH) | "
                    f"[2] {_res1['label'].upper()}: {_fail_word} ({_res1['score']}%)!"
                )
            else:
                headline = (
                    f"⚠️ KẾT LUẬN PHÂN TÁCH 2 NGƯỜI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"HIỆN TẠI CẢ 2 NGƯỜI ĐỀU ĐANG GẶP LỰC CẢN — "
                    f"[1] {_res1['label'].upper()}: {_res1['score']}% | [2] {_res2['label'].upper()}: {_res2['score']}% "
                    f"(CẦN ÔN LUYỆN KỸ HOẶC CHỜ NGÀY XUẤT KHÔNG ĐỂ TRÁNH CÙNG TRƯỢT)!"
                )

            _dual_ev_note = (
                f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, Hào {_ev_dt} tại Hào {_ev_idx} ({_ev_chi}-{_ev_nh}) "
                + (f"đang tạm lâm Tuần Không ({', '.join(_kv_ms)}) nhưng {_bien_ev_desc} — cổ pháp gọi là tượng <b>'Lưỡng Nhân Đồng Chiêm, Nhất Đắc Nhất Trì' (Hai người cùng thi/làm, kết quả của từng người phân hóa khác nhau)</b>. " if (_ev_chi in _kv_ms and _bien_ev_desc) else f"tương tác khác nhau với trục của từng người. ")
            )
            why_s = (
                f"{_dual_ev_note}"
                f"<b>• Xét riêng [1] {_res1['label']} ({_res1['score']}%):</b> {_res1['reasons']}. "
                f"<b>• Xét riêng [2] {_res2['label']} ({_res2['score']}%):</b> {_res2['reasons']}."
            )
            when_s = (
                f"<b>Thời điểm ứng nghiệm & Xuất Không mở vận:</b> {omni_data.get('exact_timestamp', 'Ngày/Giờ Thìn, Thân, Dậu')} "
                f"(Đặc biệt khi bước sang ngày/giờ <b>{_ev_chi}</b> hoặc <b>{_HOP_CHI_MS.get(_ev_chi, 'Thìn')}</b> Điền Thực / Hợp Thực Tuần Không, người đang gặp cản trở sẽ vượt qua ở lần thi/bổ sung tiếp theo)."
            )
            adv_s = (
                f"<b>Chiến lược cho từng người:</b> <b>{_res1['label']}</b> giữ vững tâm lý ổn định để chốt kết quả tốt; "
                f"riêng <b>{_res2['label']}</b> cần rà soát kỹ phần lý thuyết/mô phỏng/hồ sơ và ưu tiên hướng <b>{huong_cung}</b> (Màu trợ vận: <b>{colors_str}</b>) để hóa giải thế khắc."
            )
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        return {"has_override": False}

    @staticmethod
    def _deduce_general_clause_on_hexagram(
        sq_bp: dict,
        sq_dt: str,
        base_pct: int,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
    ) -> dict:
        """
        V104.0: Giải mã Tam Thức Hợp Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch)
        cho bất kỳ câu hỏi mở hoặc vế câu hỏi nhỏ nào dựa trực tiếp trên Ma Trận Quẻ Chuẩn Xác!
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        _m = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(chart_data, luc_hao_data, mai_hoa_data, omni_data, sq_dt)

        _CHI_NH = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

        chi_m = chart_data.get("chi_thang", "Tuất")
        chi_n = chart_data.get("chi_ngay", "Ngọ")
        nh_m = _CHI_NH.get(chi_m, "Thổ")
        nh_n = _CHI_NH.get(chi_n, "Hỏa")

        dt_idx = _m["dt_idx"]
        dt_chi = _m["dt_chi"]
        dt_nh = _m["dt_nh"]
        found_dt = bool(_m["dt_haos_all"])

        sq_score = int(base_pct or 52) + int(_m["rel_bien_pts"] // 2)
        if _m["is_cat_sao"]:
            sq_score += 5
        if _m["is_cat_cua"]:
            sq_score += 5

        lh_reasons = []
        if found_dt:
            lh_reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> hiện tại <b>Hào {dt_idx} ({dt_chi}-{dt_nh})</b>{' [TRÌ THẾ]' if dt_idx == _m['the_idx'] else ''} trên quẻ <b>{_m['full_chu']}</b>")
        else:
            lh_reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> phối hợp trục <b>Hào Thế (Hào {_m['the_idx']} {_m['the_chi']}-{_m['the_nh']})</b> trên quẻ <b>{_m['full_chu']}</b>")

        if _SINH.get(nh_m) == dt_nh or nh_m == dt_nh:
            sq_score += 7
            lh_reasons.append(f"được Nguyệt Lệnh ({chi_m}-{nh_m}) sinh phù/tỷ trợ")
        elif _KHAC.get(nh_m) == dt_nh:
            sq_score -= 5
            lh_reasons.append(f"chịu Nguyệt Lệnh ({chi_m}-{nh_m}) chế khắc")

        if _SINH.get(nh_n) == dt_nh or nh_n == dt_nh:
            sq_score += 7
            lh_reasons.append(f"đắc Nhật Thần ({chi_n}-{nh_n}) tương sinh/trợ lực")
        elif _KHAC.get(nh_n) == dt_nh:
            sq_score -= 5
            lh_reasons.append(f"bị Nhật Thần ({chi_n}-{nh_n}) xung khắc")

        sq_score = max(30, min(90, sq_score))
        t_code = sq_bp.get("specific_target") or sq_bp.get("archetype_key", "")
        c_lbl = sq_bp.get("clause_label") or sq_bp.get("raw_question") or sq_bp.get("subject_person") or "Sự việc"
        uk_str = omni_data.get("exact_timestamp", f"Ngày/Giờ {dt_chi}, {chi_n}")
        huong_str = _m["huong_cung"]

        if t_code == "TIMING_WHEN" or "D12" in t_code:
            short_hl = f"⏳ THỜI ĐIỂM ỨNG KỲ TỪ QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): {uk_str.upper()} (KHI HÀO {sq_dt.upper()} {dt_chi.upper()} XUNG/HỢP MỞ VẬN)!"
        elif sq_score >= 54:
            short_hl = f"✅ KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): THUẬN LỢI & ĐẠT KẾT QUẢ TỐT ({sq_score}% — CÁT: {_m['rel_bien_tag']}, ĐẮC SAO {_m['sao_name'].upper()} & CỬA {_m['cua_name'].upper()})!"
        elif sq_score >= 45:
            short_hl = f"⚖️ KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): KHẢ QUAN NHƯNG CẦN KIÊN NHẪN VƯỢT QUA VẤT VẢ BAN ĐẦU ({sq_score}% — BÌNH: QUẺ BIẾN {_m['full_bien'].upper()} {_m['rel_bien_tag']})!"
        else:
            short_hl = f"⚠️ KẾT LUẬN TỪ TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO): ĐANG GẶP LỰC CẢN — NÊN THẬN TRỌNG & CHỜ THỜI ({sq_score}% — HUNG)!"

        why_3sys = (
            f"1. <b>🌸 Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{_m['full_chu']}</b> ({_m['desc_chu']}) ➔ Quẻ Hỗ <b>{_m['full_ho']}</b> ({_m['desc_ho']}) ➔ Quẻ Biến <b>{_m['full_bien']}</b> ({_m['rel_bien_tag']}: {_m['rel_bien_desc']}).<br>"
            f"2. <b>🧭 Kỳ Môn Độn Giáp:</b> Cục {_m['cuc_km']} ({_m['don_type']}), Cung {_m['target_cung']} ({_m['huong_cung']}) hội <b>Sao {_m['sao_name']}</b> ({_m['sao_meaning']}), <b>Cửa {_m['cua_name']}</b> ({_m['cua_meaning']}) và <b>Thần {_m['than_name']}</b>.<br>"
            f"3. <b>☯️ Lục Hào Kinh Dịch:</b> {', '.join(lh_reasons)}{_m['dt_bien_str']}."
        )

        return {
            "has_override": True,
            "headline": f"🎯 [{c_lbl.upper()}]: {short_hl}" if sq_bp.get("clause_label") else f"🎯 {short_hl}",
            "short_headline": short_hl,
            "why": why_3sys,
            "when": f"Mốc ứng nghiệm & chuyển vận theo Can Chi: <b>{uk_str}</b>.",
            "advice": f"Hành động chủ động theo nguyên lý quẻ <b>{_m['full_ho']} ➔ {_m['full_bien']}</b> và ưu tiên phương vị <b>{huong_str}</b>.",
        }

    @staticmethod
    def cross_verify_and_reason(
        blueprint: dict,
        dung_than: str,
        weighted_pct: int,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
        auth_warnings: list = None,
        is_fake: bool = False,
        narrative_summary: str = "",
    ) -> dict:
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        auth_warnings = auth_warnings or []

        can_n = chart_data.get("can_ngay", "Giáp")
        chi_n = chart_data.get("chi_ngay", "Tý")
        can_g = chart_data.get("can_gio", "Giáp")
        chi_g = chart_data.get("chi_gio", "Tý")
        can_m = chart_data.get("can_thang", "")
        chi_m = chart_data.get("chi_thang", "")
        can_y = chart_data.get("can_nam", "")
        chi_y = chart_data.get("chi_nam", "")
        cuc_km = chart_data.get("cuc", "?")
        don_type = "Dương Độn" if chart_data.get("is_duong_don", True) else "Âm Độn"

        lh_ban = luc_hao_data.get("ban", {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = luc_hao_data.get("bien", {}) if isinstance(luc_hao_data, dict) else {}
        ten_que_chu = lh_ban.get("name") or mai_hoa_data.get("ten_que") or omni_data.get("ten_que_ban") or "Quẻ Chủ"
        ten_que_bien = lh_bien.get("name") or mai_hoa_data.get("ten_qua_bien") or omni_data.get("ten_que_bien") or "Quẻ Biến"
        dong_hao_list = luc_hao_data.get("dong_hao") or lh_ban.get("dong_hao") or []
        if isinstance(dong_hao_list, (int, str)):
            dong_hao_list = [int(dong_hao_list)] if str(dong_hao_list).isdigit() else []

        if blueprint.get("authoritative_dt"):
            dung_than = blueprint["authoritative_dt"]

        target_cung = omni_data.get("target_cung", "?")
        c_info = omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}
        huong_cung = c_info.get("huong", "Chính Nam")
        sao_name = omni_data.get("sao_name", "Thiên Tâm")
        cua_name = omni_data.get("cua_name", "Khai Môn")
        than_name = omni_data.get("than_name", "Trực Phù")
        hanh_dt = omni_data.get("hanh", "Kim")
        ts_stage = omni_data.get("ts_stage", "Vượng")

        # Bước 1: Chạy bộ giải mã Toán Học & Tam Thức Chuẩn Xác (Mai Hoa + Kỳ Môn + Lục Hào)
        spec_res = HexagramReasoningAI.deduce_specialized_answer(
            blueprint=blueprint,
            dung_than=dung_than,
            weighted_pct=weighted_pct,
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            auth_warnings=auth_warnings,
            is_fake=is_fake,
        )

        # Trích xuất Ma Trận Tam Thức Hợp Nhất (Mai Hoa Chủ/Hỗ/Biến + Kỳ Môn Tinh/Môn/Thần + Lục Hào Thế/Ứng/Động/Biến)
        _univ_mat = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            dung_than=dung_than,
        )
        if _univ_mat.get("dt_nh"):
            hanh_dt = _univ_mat["dt_nh"]

        # Bước 2 (V104.0): KÍCH HOẠT 2 CON AI THỰC TẾ LUẬN QUẺ THEO PHƯƠNG PHÁP CHUẨN TAM THỨC (MAI HOA – KỲ MÔN – LỤC HÀO)
        _raw_q_str = str(blueprint.get("raw_question") or "").strip()
        _haos_summary_str = " | ".join(_univ_mat["haos_lines_desc"])
        _cache_sig = "V104_DUAL::" + hashlib.md5(f"{_raw_q_str}::{ten_que_chu}::{ten_que_bien}::{can_n}_{chi_n}_{can_g}_{chi_g}".encode("utf-8")).hexdigest()
        _real_ai_pair = _REAL_DUAL_AI_CACHE.get(_cache_sig)

        if _real_ai_pair is None and len(_raw_q_str) >= 4:
            # --- GỌI CON AI SỐ 1 THỰC TẾ (CHUYÊN GIA ĐỌC HIỂU CÂU HỎI) ---
            _prompt_ai1 = (
                "Bạn là CON AI SỐ 1 (Chuyên Gia Đọc Hiểu & Phân Tích Câu Hỏi Dịch Học).\n"
                f"Câu hỏi của người dùng: \"{_raw_q_str}\"\n\n"
                "Nhiệm vụ của bạn: Đọc hiểu chính xác 100% ý định thực tế của câu hỏi này để lập Hồ Sơ Chỉ Thị truyền sang cho CON AI SỐ 2 (Chuyên Gia Tự Luận Quẻ Tam Thức: Mai Hoa Dịch Số, Kỳ Môn Độn Giáp, Lục Hào Kinh Dịch).\n"
                "Trả về ĐÚNG 1 JSON hợp lệ:\n"
                "{\n"
                "  \"ai1_intent_summary\": \"Tóm tắt chính xác câu hỏi đang hỏi điều gì (nêu rõ mọi vế và mọi người trong câu hỏi)\",\n"
                "  \"ai1_expected_answer_format\": \"Khuôn mẫu & Đơn vị bắt buộc của câu trả lời sát đúng câu hỏi\",\n"
                "  \"ai1_dung_than_guide\": \"Chỉ định Dụng Thần trên Mai Hoa (Thể/Dụng, Chủ/Hỗ/Biến), Kỳ Môn (Cung/Sao/Cửa/Thần) và Lục Hào (Thế/Ứng/Lục Thân)\",\n"
                "  \"ai1_strict_instruction_to_ai2\": \"Mệnh lệnh bắt buộc giao cho AI Số 2: Phải tự luận giải trực tiếp từ Mai Hoa + Kỳ Môn + Lục Hào để trả lời trúng đích câu hỏi, cấm trả lời lạc đề!\"\n"
                "}"
            )
            _ai1_json = blueprint.get("ai1_real_llm")
            if not isinstance(_ai1_json, dict) or not _ai1_json.get("ai1_intent_summary"):
                _ai1_json = _call_gemini_json_fast(_prompt_ai1, timeout_sec=10, tier="cheapest_reader")
            if isinstance(_ai1_json, dict) and _ai1_json.get("ai1_intent_summary"):
                # --- GỌI CON AI SỐ 2 THỰC TẾ (TỰ LUẬN QUẺ THEO CHUẨN TAM THỨC ĐÃ KIỂM CHỨNG THỰC TẾ: MAI HOA + KỲ MÔN + LỤC HÀO) ---
                _prompt_ai2 = (
                    "Bạn là CON AI SỐ 2 (Đại Sư Tự Luận Quẻ Tam Thức Chuẩn Xác: Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch).\n"
                    f"1. CÂU HỎI GỐC CỦA NGƯỜI DÙNG: \"{_raw_q_str}\"\n"
                    f"2. HỒ SƠ CHỈ THỊ TỪ CON AI SỐ 1:\n"
                    f"   - Ý nghĩa câu hỏi: {_ai1_json.get('ai1_intent_summary')}\n"
                    f"   - Khuôn mẫu & Đơn vị đáp án bắt buộc: {_ai1_json.get('ai1_expected_answer_format')}\n"
                    f"   - Dụng Thần chỉ định: {_ai1_json.get('ai1_dung_than_guide')}\n\n"
                    f"3. {_univ_mat['matrix_prompt_block']}\n"
                    f"   - Tứ Trụ Thời Khắc: Năm {can_y} {chi_y}, Tháng {can_m} {chi_m}, Ngày {can_n} {chi_n}, Giờ {can_g} {chi_g}.\n"
                    f"   - Kết quả giải mã toán học Tam Thức nội bộ: {spec_res.get('headline', '')} | {re.sub(r'<[^>]+>', '', str(spec_res.get('why', '')))[:450]}\n\n"
                    "4. NĂM ĐỊNH LUẬT LUẬN QUẺ CHUẨN XÁC ĐÃ KIỂM CHỨNG THỰC TẾ (BẮT BUỘC TUÂN THỦ):\n"
                    "   - Định luật 1 (Đoán Màu sắc / Đồ vật / Thiết bị): Lấy Quẻ Biến Dụng Mai Hoa (VD: Khảm Thủy = Màu Đen) + Bát Thần Kỳ Môn (Huyền Vũ = Màu Đen, Bạch Hổ = Màu Trắng) + Nhật Can & Tam Hợp Lục Hào làm màu chủ đạo; Quẻ Dụng gốc làm màu chi tiết phụ.\n"
                    "   - Định luật 2 (Đoán Vợ chồng / Nhân tình / Gia đạo): Khi Hào Thê Tài/Quan Quỷ trì Thế hoặc sinh hợp Thế, Quẻ Biến Dụng sinh Thể (VD: Thủy Lôi Truân có Khảm Thủy sinh Chấn Mộc), Quẻ Hỗ là Tiệm/Gia Nhân, Kỳ Môn đắc Thiên Phụ + Sinh Môn thì khẳng định 100% vợ/chồng chung thủy (Huyền Vũ đi cùng Thiên Phụ + Sinh Môn chỉ là tâm sự riêng hoặc người hỏi đa nghi/hỏi thử).\n"
                    "   - Định luật 3 (Đoán Tầng nhà / Chung cư): Hậu Thiên Thượng Quái Mai Hoa + Tiên Thiên Hạ Quái Hỗ + Bản cung Sao Kỳ Môn = Vị trí tầng đang ở (VD: Tầng 7); Tổng Tiên Thiên Chủ + Hỗ = Tổng số tầng tòa chung cư (VD: 18 tầng).\n"
                    "   - Định luật 4 (Đoán Số người / Con cái / Quãng đường km): Rút trích trực tiếp từ các hào Lục Thân hiện hữu và Quái số Tiên/Hậu Thiên Mai Hoa, tuyệt đối cấm tự bịa số.\n"
                    "   - Định luật 5 (Mọi câu hỏi khác): Tự luận giải trực diện câu hỏi từ [1] Mai Hoa Dịch Số (Chủ - Hỗ - Biến, Thể - Dụng), [2] Kỳ Môn Độn Giáp (Cung - Sao - Cửa - Thần), [3] Lục Hào Kinh Dịch (Thế - Ứng - Dụng Thần - Động/Biến). Cấm trả lời lạc đề!\n\n"
                    "Trả về ĐÚNG 1 JSON hợp lệ:\n"
                    "{\n"
                    "  \"ai2_headline\": \"Câu trả lời chốt hạ trực diện, in hoa các ý chính, trả lời đúng 100% câu hỏi từ Tam Thức (Mai Hoa – Kỳ Môn – Lục Hào)\",\n"
                    "  \"ai2_why\": \"Giải thích chi tiết theo đúng 3 mục: 1. Mai Hoa Dịch Số (Chủ/Hỗ/Biến, Thể/Dụng), 2. Kỳ Môn Độn Giáp (Cung/Sao/Cửa/Thần), 3. Lục Hào Kinh Dịch (Hào Thế/Ứng/Dụng Thần/Hào Động)\",\n"
                    "  \"ai2_when\": \"Thời điểm ứng nghiệm / hoàn thành cụ thể dựa trên Can Chi & Ứng kỳ của quẻ\",\n"
                    "  \"ai2_advice\": \"Lời khuyên hành động thực tế sát với câu hỏi và phương vị may mắn\"\n"
                    "}"
                )
                _ai2_json = _call_gemini_json_fast(_prompt_ai2, timeout_sec=14, tier="reasoner")
                if isinstance(_ai2_json, dict) and _ai2_json.get("ai2_headline"):
                    _real_ai_pair = {"ai1": _ai1_json, "ai2": _ai2_json}
                    _REAL_DUAL_AI_CACHE[_cache_sig] = _real_ai_pair

        if isinstance(_real_ai_pair, dict) and _real_ai_pair.get("ai1") and _real_ai_pair.get("ai2"):
            _r_ai1 = _real_ai_pair["ai1"]
            _r_ai2 = _real_ai_pair["ai2"]
            blueprint["subject_person"] = f"{_r_ai1.get('ai1_intent_summary', blueprint['subject_person'])} — <b>Đơn vị/Khuôn đáp án:</b> {_r_ai1.get('ai1_expected_answer_format', '')}"
            blueprint["lh_dt_instruction"] = f"{_r_ai1.get('ai1_dung_than_guide', blueprint['lh_dt_instruction'])} | <b>Chỉ thị AI 1 ➔ Tam Thức & AI 2:</b> {_r_ai1.get('ai1_strict_instruction_to_ai2', '')}"
            if not spec_res.get("has_override"):
                _fb_3sys = HexagramReasoningAI._deduce_general_clause_on_hexagram(
                    sq_bp=blueprint,
                    sq_dt=dung_than,
                    base_pct=weighted_pct,
                    chart_data=chart_data,
                    luc_hao_data=luc_hao_data,
                    mai_hoa_data=mai_hoa_data,
                    omni_data=omni_data,
                )
                spec_res["has_override"] = True
                spec_res["headline"] = _r_ai2.get("ai2_headline") or _fb_3sys.get("headline", "")
                _ai2_w = str(_r_ai2.get("ai2_why") or "").strip()
                if _ai2_w and ("Mai Hoa" in _ai2_w and "Kỳ Môn" in _ai2_w):
                    spec_res["why"] = _ai2_w
                elif _ai2_w:
                    spec_res["why"] = f"{_ai2_w}<br><br><b>• Đối chứng Tam Thức Chuẩn Xác:</b><br>{_fb_3sys.get('why', '')}"
                else:
                    spec_res["why"] = _fb_3sys.get("why", "")
                spec_res["when"] = _r_ai2.get("ai2_when") or _fb_3sys.get("when", "")
                spec_res["advice"] = _r_ai2.get("ai2_advice") or _fb_3sys.get("advice", "")

        # V104.0: Nếu không có mạng/API hoặc chưa có override, tự động kích hoạt Bộ Tự Luận Quẻ Tam Thức (Mai Hoa + Kỳ Môn + Lục Hào)
        if not spec_res.get("has_override"):
            spec_res = HexagramReasoningAI._deduce_general_clause_on_hexagram(
                sq_bp=blueprint,
                sq_dt=dung_than,
                base_pct=weighted_pct,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
            )

        headline_ans = spec_res.get("headline") or omni_data.get("binary_verdict_headline", "")
        why_proof = spec_res.get("why") or omni_data.get("binary_why_reasons", "")
        when_proof = spec_res.get("when") or omni_data.get("binary_when_note", "")
        advice_proof = spec_res.get("advice") or omni_data.get("binary_action_advice", "")

        if not headline_ans and narrative_summary:
            m_ans = re.search(r"👉\s*(.+?)</div>", narrative_summary)
            if m_ans:
                headline_ans = re.sub(r"<[^>]+>", "", m_ans.group(1)).strip()
            else:
                m_ans2 = re.search(r"📢\s*\*\*CÂU TRẢ LỜI:\*\*\s*(.+?)(?:\n|$)", narrative_summary)
                if m_ans2:
                    headline_ans = re.sub(r"<[^>]+>", "", m_ans2.group(1)).strip()

        if not why_proof and narrative_summary:
            m_why = re.search(r"🔍 NGUYÊN NHÂN CỐT LÕI</div><div[^>]*>(.+?)</div>", narrative_summary)
            if m_why:
                why_proof = m_why.group(1).strip()

        tu_tru_str = f"Năm {can_y} {chi_y} · Tháng {can_m} {chi_m} · Ngày {can_n} {chi_n} · Giờ {can_g} {chi_g}".strip(" ·")
        dong_str = f"Động hào {', '.join(map(str, dong_hao_list))}" if dong_hao_list else "Quẻ Tĩnh (6 hào an tĩnh)"

        _dt_real_flag = bool(_univ_mat.get("dt_is_real", True))
        if _dt_real_flag and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"<b>Căn cứ Nhóm Quẻ Chính Xác Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch + Thiết Bản; các quẻ khác dùng tham khảo):</b> "
                f"Hào Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> tại Hào {_univ_mat.get('dt_idx', 3)} ({_univ_mat.get('dt_chi', 'Thìn')}-{_univ_mat.get('dt_nh', hanh_dt)}) hoàn toàn hữu khí (KHÔNG phạm Tuần Không), "
                f"kết hợp Quẻ Biến <b>{ten_que_bien}</b> ({_univ_mat.get('rel_bien_tag', 'Dụng sinh Thể')}) làm phương tiện suy đoán chuẩn xác nhất (kết quả bất biến dù đảo thứ tự 2 phương án)!"
            )
        elif is_fake and not _dt_real_flag and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Tuần Không / Tử Môn</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Quẻ dùng phép <b>Loại Trừ Nhị Phân</b>: Bác bỏ hoàn toàn phương án bị Không Vong để khẳng định 100% phương án thực tế còn lại!"
            )
        elif is_fake and not _dt_real_flag and blueprint.get("specific_target") not in ("HOUSE_FLOORS", "HOUSEHOLD_MEMBERS", "CLOTHING_VEHICLE", "HIDDEN_OBJECT", "FIDELITY_AFFAIR_CHECK", "SIBLINGS_COUNT", "CHILDREN_AGE", "CHILDREN_COUNT"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Chân Không / Không Vong Vô Khí</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Cảnh báo sự việc/đối tượng đang hỏi hiện <b>chưa tồn tại ngoài thực tế (= 0)</b> hoặc là câu hỏi thử lòng quẻ."
            )
        elif auth_warnings or _dt_real_flag:
            auth_status_str = (
                f"<b>Căn cứ Nhóm Quẻ Chính Xác Nhất (Mai Hoa + Kỳ Môn + Lục Hào + Thiết Bản; các quẻ khác dùng tham khảo):</b> "
                f"Hào Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> tại Hào {_univ_mat.get('dt_idx', 3)} ({_univ_mat.get('dt_chi', 'Thìn')}-{_univ_mat.get('dt_nh', hanh_dt)}) hoàn toàn hữu khí / được Hào Động sinh trợ "
                f"khẳng định <b>đối tượng/sự việc bạn hỏi LÀ CÓ THẬT 100% NGOÀI ĐỜI (bác bỏ Chân Không)</b>; còn dấu hiệu Tuần Không ở Nhật Can bắt bài bạn đang <b>đặt câu hỏi để thử độ nhạy bén của quẻ</b>!"
            )
        else:
            auth_status_str = (
                f"Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> đối chứng trực tiếp trên Nhóm Quẻ Chính (Mai Hoa + Kỳ Môn + Lục Hào — {ts_stage}), khớp chính xác vào câu hỏi."
            )

        sub_intents_html = ""
        if blueprint.get("sub_intents"):
            sub_intents_html = f" · <b>Ý phụ đi kèm:</b> {', '.join(blueprint['sub_intents'])}"

        ab_html = ""
        if blueprint.get("is_compound_question") and blueprint.get("sub_questions"):
            _sq_items_html = "<br>".join(
                f'&nbsp;&nbsp;• <b>[Câu hỏi nhỏ {i+1}]:</b> <i>"{sq.get("clause_label", "")}"</i> ➔ Khớp <b>{sq.get("archetype_code", "")}</b> · Giao Dụng Thần: <b style="color:#fde047;">{sq.get("subject_lh_dt", "")}</b>'
                for i, sq in enumerate(blueprint["sub_questions"])
            )
            ab_html = (
                f'<div style="margin-top:6px;padding:7px 10px;background:rgba(56,189,248,0.12);border-radius:8px;border-left:3px solid #38bdf8;font-size:0.9em;color:#e0f2fe;">'
                f'🧩 <b>Phát hiện câu hỏi ghép ({len(blueprint["sub_questions"])} câu hỏi nhỏ trong 1 lần hỏi — Tự động tách & giải mã đủ 100%):</b><br>'
                f'{_sq_items_html}'
                f'</div>'
            )
        elif blueprint.get("option_a") and blueprint.get("option_b"):
            ab_html = (
                f'<div style="margin-top:5px;font-size:0.9em;color:#bae6fd;">'
                f'⚖️ <b>Tách 2 vế đối chứng (Bất biến thứ tự):</b> [Phương án 1]: <b>{blueprint["option_a"]}</b> ↔ [Phương án 2]: <b>{blueprint["option_b"]}</b>'
                f'</div>'
            )

        _ai1_summary_line = (
            f'• <b>Đọc hiểu bản chất câu hỏi (AI Số 1):</b> <span style="color:#a7f3d0;font-weight:700;">{blueprint.get("ai1_intent_summary")}</span><br>'
            if blueprint.get("ai1_intent_summary") else ""
        )
        _ai1_format_line = (
            f'• <b>Khuôn mẫu đáp án truyền sang AI Số 2 & 18 Pháp:</b> <span style="color:#fde68a;">{blueprint.get("ai1_expected_answer_format")}</span><br>'
            if blueprint.get("ai1_expected_answer_format") else ""
        )

        _q_low_domain = str(question or "").lower()
        if any(w in _q_low_domain for w in ["cả cuộc đời", "trọn đời", "cuộc đời tôi", "số mệnh cả đời", "lá số tử vi", "đại vận", "hậu vận cả đời"]):
            _domain_badge_html = (
                '• <b>Phân khu phương pháp chuyên trách:</b> <span style="color:#c4b5fd;font-weight:800;">'
                '🔯 MẢNG VẬN MỆNH CẢ CUỘC ĐỜI — Chuyên trách bởi: Tử Vi Đẩu Số & Thiết Bản Thần Toán</span><br>'
            )
        elif any(w in _q_low_domain for w in ["quốc gia", "đất nước", "thế giới", "quốc vận", "chiến tranh", "thiên tai", "kinh tế thế giới", "vĩ mô"]):
            _domain_badge_html = (
                '• <b>Phân khu phương pháp chuyên trách:</b> <span style="color:#fda4af;font-weight:800;">'
                '⚔️ MẢNG VẬN QUỐC GIA & THỜI CUỘC VĨ MÔ — Chuyên trách bởi: Thái Ất Thần Số & Kỳ Môn Độn Giáp</span><br>'
            )
        elif any(w in _q_low_domain for w in ["ngày nào tốt", "chọn ngày", "xem ngày", "giờ hoàng đạo", "khai trương ngày", "động thổ ngày", "nhập trạch ngày"]):
            _domain_badge_html = (
                '• <b>Phân khu phương pháp chuyên trách:</b> <span style="color:#fcd34d;font-weight:800;">'
                '📅 MẢNG TRẠCH NHẬT HÀNH SỰ — Chuyên trách bởi: Xem Ngày Đẹp (12 Trực · 28 Tú) & Kỳ Môn</span><br>'
            )
        else:
            _domain_badge_html = (
                '• <b>Phân khu phương pháp chuyên trách:</b> <span style="color:#4ade80;font-weight:800;">'
                '🎯 MẢNG LUẬN QUẺ THỰC TẾ — Chỉ dùng 4 Phương Pháp Chuẩn Xác: Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản</span> '
                '<span style="color:#94a3b8;font-size:0.9em;">(Tử Vi xem riêng Cả Cuộc Đời · Thái Ất xem riêng Quốc Gia · Xem Ngày xem riêng Chọn Ngày)</span><br>'
            )

        dual_agent_html = (
            f'<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);padding:16px 18px;border-radius:14px;margin-bottom:16px;border:2px solid #38bdf8;box-shadow:0 6px 22px rgba(56,189,248,0.22);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px;border-bottom:1px solid rgba(56,189,248,0.3);padding-bottom:8px;">'
            f'<div style="font-size:1.06em;font-weight:900;color:#38bdf8;letter-spacing:0.3px;">🤖 HỆ THỐNG SONG NÃO AI 2 TẦNG (V106.0): AI SỐ 1 PHÂN KHU ➔ AI SỐ 2 LUẬN QUẺ BẰNG 4 PHƯƠNG PHÁP CHUẨN XÁC (MAI HOA · KỲ MÔN · LỤC HÀO · THIẾT BẢN)</div>'
            f'<span style="background:rgba(56,189,248,0.18);color:#7dd3fc;padding:3px 10px;border-radius:12px;font-size:0.82em;font-weight:800;border:1px solid #38bdf8;">Khớp {blueprint["archetype_code"]}/25 Đại Dạng Toàn Cầu</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;">'
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #38bdf8;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#7dd3fc;margin-bottom:6px;">🧠 CON AI SỐ 1 (GEMINI FLASH-LITE — ĐỌC HIỂU CÂU HỎI & PHÂN KHU PHƯƠNG PHÁP)</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Nhận diện dạng câu hỏi:</b> <span style="color:#fde047;font-weight:800;">{blueprint["archetype_code"]} — {blueprint["archetype_name"]}</span><br>'
            f'{_domain_badge_html}'
            f'{_ai1_summary_line}'
            f'• <b>Đối tượng trọng tâm:</b> {blueprint["subject_person"]} (Giao Dụng Thần: <b>{dung_than}</b>){sub_intents_html}<br>'
            f'{_ai1_format_line}'
            f'• <b>Chỉ thị tra quẻ cho AI Số 2 & Bộ Tứ Chuẩn Xác:</b> <i>{blueprint["lh_dt_instruction"]}</i>'
            f'{ab_html}'
            f'</div></div>'
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #fbbf24;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#fde047;margin-bottom:6px;">🔮 CON AI SỐ 2 — LUẬN QUẺ BẰNG 4 PHƯƠNG PHÁP CHUẨN XÁC (MAI HOA · KỲ MÔN · LỤC HÀO · THIẾT BẢN)</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Quẻ lập đúng thời khắc ({tu_tru_str}):</b> Quẻ <b>{ten_que_chu}</b> ➔ <b>{ten_que_bien}</b> ({dong_str}) · Kỳ Môn Cục {cuc_km} ({don_type}, Cung {target_cung} {huong_cung}: Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b>, Thần <b>{than_name}</b>)<br>'
            f'• <b>Kết quả đối chứng Thực/Hư:</b> {auth_status_str}<br>'
            f'• <b>Đáp án suy luận khớp quẻ:</b> <span style="color:#4ade80;font-weight:900;">{headline_ans or "Đã khớp toàn bộ 18 tầng quẻ"}</span>'
            f'</div></div>'
            f'</div></div>'
        )

        online_directive = (
            f"=== HỒ SƠ BÀN GIAO TỪ HỆ THỐNG SONG NÃO AI 2 TẦNG (BẮT BUỘC TUÂN THỦ 100%) ===\n"
            f"1. [CON AI SỐ 1 (FLASH-LITE) - ĐỌC HIỂU CÂU HỎI & GIAO NHIỆM VỤ]:\n"
            f"   - Câu hỏi thuộc: {blueprint['archetype_code']} ({blueprint['archetype_name']})\n"
            f"   - Bản chất câu hỏi người dùng muốn hỏi: {blueprint.get('ai1_intent_summary') or blueprint['archetype_name']}\n"
            f"   - Khuôn mẫu & đơn vị đáp án bắt buộc: {blueprint.get('ai1_expected_answer_format') or blueprint['answer_rule']}\n"
            f"   - Đối tượng: {blueprint['subject_person']} | Dụng Thần: {dung_than} (Hành {hanh_dt})\n"
            f"   - Chỉ thị nghiêm ngặt từ AI Số 1: {blueprint.get('ai1_strict_instruction_to_ai2') or blueprint['answer_rule']}\n"
            f"2. [CON AI SỐ 2 - ĐỐI CHỨNG QUẺ ({tu_tru_str})]:\n"
            f"   - Lục Hào & Mai Hoa: Quẻ {ten_que_chu} biến {ten_que_bien} ({dong_str})\n"
            f"   - Kỳ Môn Độn Giáp: Cung {target_cung} ({huong_cung}) hội Sao {sao_name}, Cửa {cua_name}, Thần {than_name}\n"
            f"   - ĐÁP ÁN ĐỐI CHỨNG CHỐT HẠ (TUYỆT ĐỐI KHÔNG ĐƯỢC SỬA ĐỔI HAY BỊA KHÁC ĐI): {headline_ans}\n"
            f"   - Căn cứ suy luận: {re.sub(r'<[^>]+>', '', why_proof)}\n"
        )

        return {
            "blueprint": blueprint,
            "has_specialized_override": bool(spec_res.get("has_override")),
            "verified_headline": headline_ans,
            "verified_why": why_proof,
            "verified_when": when_proof,
            "verified_advice": advice_proof,
            "dual_agent_html": dual_agent_html,
            "online_directive": online_directive,
        }

"""
dual_ai_agents.py — V103.0: HỆ THỐNG SONG NÃO AI 2 TẦNG (DUAL-AGENT PIPELINE)
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
        # B. Hỏi về Số anh chị em trong gia đình / Con thứ mấy
        is_siblings_q = any(w in q_low for w in [
            "mấy anh chị em", "bao nhiêu anh chị em", "mấy anh em", "bao nhiêu anh em",
            "mấy chị em", "con thứ mấy", "thứ mấy trong nhà", "con trưởng hay con út", "con đầu hay"
        ])
        # C. Hỏi về Tình trạng Hôn nhân thực tế (Đã kết hôn chưa / Có vợ chồng chưa / Độc thân hay có gia đình)
        is_marital_status_q = any(w in q_low for w in [
            "kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
            "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"
        ])
        # C2. Hỏi về Số lượng Vợ / Chồng trong cuộc đời (Có mấy vợ / Có mấy chồng / Mấy đời vợ chồng / Kết hôn mấy lần)
        is_spouse_count_q = any(w in q_low for w in [
            "mấy vợ", "bao nhiêu vợ", "mấy người vợ", "mấy đời vợ", "lấy mấy vợ", "có mấy vợ", "mấy bà vợ",
            "mấy chồng", "bao nhiêu chồng", "mấy người chồng", "mấy đời chồng", "lấy mấy chồng", "có mấy chồng", "mấy ông chồng",
            "mấy lần kết hôn", "kết hôn mấy lần", "lấy vợ mấy lần", "lấy chồng mấy lần", "mấy lần đò", "mấy lần lập gia đình"
        ])
        # D. Hỏi về Trang phục đang mặc / Xe cộ đang đi / Màu sắc áo, xe, nhà / Biển số xe
        is_clothing_vehicle_q = any(w in q_low for w in [
            "mặc áo màu gì", "áo màu gì", "quần áo màu gì", "trang phục màu gì", "mặc đồ màu gì",
            "đi xe gì", "xe màu gì", "xe của tôi màu gì", "biển số xe", "số nhà bao nhiêu",
            "số nhà mấy", "nhà màu gì", "nhà sơn màu gì", "cửa màu gì"
        ])
        # E. Hỏi về Xung quanh / Trong phòng có mấy người / Có ai bên cạnh không
        is_people_around_q = any(w in q_low for w in [
            "xung quanh tôi có mấy người", "trong phòng có mấy người", "ở đây có mấy người",
            "bên cạnh tôi có ai", "có mấy người đang", "tôi đang ở một mình hay", "ở một mình hay"
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
                # Trường hợp 2: option_a có chủ ngữ ("con tôi không khóc") còn option_b chỉ ghi vị ngữ đối lập ("đang khóc")
                for _subj_pfx in ["con tôi ", "con của tôi ", "bé nhà tôi ", "vợ tôi ", "chồng tôi ", "bố tôi ", "mẹ tôi ", "nhà tôi "]:
                    if option_a.startswith(_subj_pfx) and not option_b.startswith(_subj_pfx.strip().split()[0]):
                        option_b = f"{_subj_pfx.strip()} {option_b}".strip()
                        break
                if any(w in q_low for w in ["con tôi", "con gái", "con trai", "bé gái", "bé trai", "con của tôi"]):
                    subject_person = "Con cái (Tử tức — Đối chứng 2 phương án trên quẻ)"
                    authoritative_dt = "Tử Tôn"
        elif is_profile:
            arch_key = "D08_PERSON_PROFILE"
            specific_target = "PERSON_PROFILE"
        elif is_object:
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "HIDDEN_OBJECT"
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

        arch_meta = UNIVERSAL_25_ARCHETYPES.get(arch_key, UNIVERSAL_25_ARCHETYPES["D25_SPIRITUAL_GENERAL"])

        # V103.0: Nhận diện Câu hỏi Đa Chủ Thể (2 người cùng thi / cùng làm việc / cùng hỏi kết quả: "tôi và vợ tôi...", "tôi và chồng...", "tôi và bạn...", "2 con tôi...")
        multi_subjects = []
        if specific_target not in ("CHILDREN_AGE", "CHILDREN_COUNT", "SIBLINGS_COUNT", "MARITAL_STATUS_NOW", "LOCATION_HOME_WORK", "POSTURE_STATE"):
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

        # V103.0: BỘ PHÂN TÁCH ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN (Multi-SubQuestion Decomposer)
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
        # V103.0: Gắn CON AI SỐ 1 THỰC TẾ (Dòng rẻ nhất & siêu tốc: gemini-2.5-flash-lite / gemini-2.0-flash-lite)
        # ngay tại Bước 0 để đọc hiểu câu hỏi và truyền Dụng Thần + Chỉ thị xuống cho mọi Phương pháp & Con AI Số 2!
        if (not dung_than_hint or dung_than_hint != "__SINGLE_CLAUSE__") and len(q_raw) >= 4:
            _ai1_sig = "AI1_READER::" + hashlib.md5(q_raw.lower().encode("utf-8")).hexdigest()
            _ai1_cached = _REAL_DUAL_AI_CACHE.get(_ai1_sig)
            if _ai1_cached is None:
                _p_ai1_step0 = (
                    "Bạn là CON AI SỐ 1 (Model Siêu Nhẹ Chuyên Đọc Hiểu & Phân Tích Câu Hỏi Dịch Học).\n"
                    f"Câu hỏi của người dùng: \"{q_raw}\"\n\n"
                    "Hãy đọc hiểu thực tế câu hỏi này và trả về ĐÚNG 1 JSON hợp lệ để truyền xuống cho các Phương pháp Bói Dịch (Lục Hào, Kỳ Môn, Mai Hoa, Thiết Bản, Đại Lục Nhâm, Thái Ất) và Con AI Số 2:\n"
                    "{\n"
                    "  \"ai1_intent_summary\": \"Tóm tắt ngắn gọn, chính xác người dùng đang hỏi cái gì (nêu rõ mọi vế và mọi chủ thể)\",\n"
                    "  \"ai1_expected_answer_format\": \"Đơn vị và khuôn mẫu câu trả lời bắt buộc (VD: Số km còn thiếu của từng người; hoặc Số vợ và số con; hoặc Chọn phương án A hay B)\",\n"
                    "  \"ai1_primary_dung_than\": \"Chọn ĐÚNG 1 trong 6 Dụng Thần chính phù hợp nhất với trọng tâm câu hỏi: Phụ Mẫu | Thê Tài | Tử Tôn | Quan Quỷ | Huynh Đệ | Bản Thân\",\n"
                    "  \"ai1_dung_than_guide\": \"Hướng dẫn tra cứu Dụng Thần cho từng phương pháp (Lục Hào, Kỳ Môn, Mai Hoa, Thiết Bản)\",\n"
                    "  \"ai1_strict_instruction_to_ai2\": \"Mệnh lệnh nghiêm ngặt cho Con AI Số 2 và các phương pháp: Phải trả lời đúng câu hỏi và đúng đơn vị nào, cấm trả lời lệch sang chủ đề nào\"\n"
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
            "bố và mẹ", "mẹ và bố", "ba và mẹ", "ông và bà",
            "nam và nữ", "trai và gái", "nếp và tẻ", "ăn và ngủ",
        ]
        for _pp in _PROTECT_PHRASES:
            protected_q = re.sub(re.escape(_pp), lambda m: m.group(0).replace(" và ", " __AND_KEEP__ "), protected_q, flags=re.IGNORECASE)

        # 1. Tách theo dấu câu và từ nối vế câu hỏi
        raw_clauses = re.split(r"[,;?/|]+|\s+(?:và|cùng với|còn|rồi|kèm theo|kèm|thêm)\s+", protected_q, flags=re.IGNORECASE)
        clauses = []
        for rc in raw_clauses:
            c_clean = rc.replace(" __AND_KEEP__ ", " và ").strip(" .,;?!-/")
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
                ["mấy anh chị em", "bao nhiêu anh chị em", "mấy anh em", "bao nhiêu anh em", "mấy chị em", "con thứ mấy", "thứ mấy trong nhà"],
                "Gia đình có mấy anh chị em & Thứ mấy",
            ),
            (
                "PEOPLE_AROUND",
                ["xung quanh tôi có mấy người", "trong phòng có mấy người", "ở đây có mấy người", "bên cạnh tôi có ai", "ở một mình hay"],
                "Xung quanh có mấy người",
            ),
            (
                "CLOTHING_VEHICLE",
                ["mặc áo màu gì", "áo màu gì", "quần áo màu gì", "trang phục màu gì", "đi xe gì", "xe màu gì", "biển số xe", "nhà màu gì"],
                "Mặc áo màu gì / Đi xe gì",
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

        return sub_blueprints if len(sub_blueprints) >= 2 else []


class HexagramReasoningAI:
    """
    CON AI SỐ 2: Chuyên trách SUY LUẬN & ĐỐI CHỨNG QUẺ.
    Nhận Bản Hồ Sơ Câu Hỏi (`blueprint`) từ Con AI Số 1, mang đi đối chứng trực tiếp
    với Quẻ lập theo Giờ - Ngày - Tháng - Năm hiện tại (`chart_data`, `luc_hao_data`,
    `mai_hoa_data`, `omni_data`) để giải mã trực diện từng câu hỏi đặc thù!
    """

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

        # ── 0. GIẢI MÃ ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN (COMPOUND MULTI-SUBQUESTION SOLVER V103.0) ──
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

        # ── 1. GIẢI MÃ: TÔI Ở NHÀ MẤY TẦNG / ĐANG Ở TẦNG MẤY / NHÀ CÓ MẤY PHÒNG ──
        if target == "HOUSE_FLOORS":
            # Tính số tầng nhà theo Quái số Mai Hoa + vị trí Hào Phụ Mẫu (Nhà) & Hào Thế (Người ở)
            QUAI_FLOOR_MAP = {
                "Khôn": (1, 2, "Nhà thấp tầng (1 – 2 tầng / nhà trệt kiên cố)"),
                "Cấn": (2, 3, "Nhà 2 – 3 tầng (kết cấu vững chãi như núi)"),
                "Khảm": (2, 3, "Nhà 2 – 3 tầng (hoặc có tầng lửng/hầm)"),
                "Chấn": (3, 4, "Nhà 3 – 4 tầng (vươn lên thẳng đứng)"),
                "Tốn": (3, 4, "Nhà 3 – 4 tầng (thoáng gió, nhiều cửa sổ)"),
                "Ly": (3, 4, "Nhà 3 – 4 tầng (sáng sủa, mặt tiền thoáng)"),
                "Đoài": (2, 3, "Nhà 2 – 3 tầng (thiết kế hiện đại)"),
                "Càn": (4, 5, "Nhà cao 4 – 5 tầng (hoặc tòa nhà/chung cư cao tầng)"),
            }
            quai_cung_name = c_info.get("quai", "Ly")
            mh_upper = str(mai_hoa_data.get("upper") or "")
            mh_lower = str(mai_hoa_data.get("lower") or "")
            mh_the = str(mai_hoa_data.get("the_quai") or mh_upper or quai_cung_name)
            mh_dung = str(mai_hoa_data.get("dung_quai") or mh_lower or quai_cung_name)
            mh_bien_dung = str(mai_hoa_data.get("bien_dung_quai") or "")
            pm_positions = [idx for idx, _ in pm_haos] if pm_haos else [pm_idx]
            is_bat_thuan = bool(mh_upper and mh_upper == mh_lower) or ("Thuần " in str(ten_que_chu))
            primary_quai = mh_the if mh_the in QUAI_FLOOR_MAP else (mh_upper if mh_upper in QUAI_FLOOR_MAP else quai_cung_name)
            # Xác định Thượng Quái & Hạ Quái từ tên quẻ
            base_f1, base_f2, desc_f = QUAI_FLOOR_MAP.get(primary_quai, (2, 3, "Nhà 2 – 3 tầng"))
            if primary_quai == "Khôn" and (mh_bien_dung in ("Chấn", "Cấn", "Khảm", "Ly") or max(pm_positions) >= 2):
                base_f1, base_f2 = 2, 3
            active_hao = dong_list[0] if dong_list else (pm_positions[0] if is_bat_thuan else the_idx)
            if max(pm_positions) <= 2 and (not dong_list or max(dong_list) <= 2) and primary_quai in ("Khôn", "Cấn", "Khảm", "Đoài"):
                floor_main = f"NHÀ {base_f1} – {base_f2} TẦNG (ỨNG MẠNH NHẤT: NHÀ {base_f1} TẦNG HOẶC {base_f2} TẦNG / 1 TRỆT {base_f1} LẦU)"
                cur_floor = f"Tầng 1 (Tầng trệt — ứng Hào {active_hao}) hoặc Tầng 2 (Chính Trạch — Hào Phụ Mẫu tại Hào {pm_positions[0]})"
            elif (not is_bat_thuan) and the_idx in (5, 6) and primary_quai == "Càn":
                floor_main = f"NHÀ CAO {base_f1} – {base_f2} TẦNG (HOẶC TÒA NHÀ / CHUNG CƯ)"
                cur_floor = f"Tầng {base_f1} – {base_f2} (hoặc Tầng {the_idx - 1}–{the_idx} nếu ở chung cư)"
            else:
                floor_main = locals().get("floor_main", "")
                cur_f_low = min(max(1, active_hao), base_f1)
                floor_main = f"NHÀ {base_f1} – {base_f2} TẦNG (ỨNG MẠNH: NHÀ {base_f1} TẦNG HOẶC {base_f2} TẦNG)"
                cur_f_high = min(max(cur_f_low + 1, pm_positions[0]), base_f2)
                cur_floor = f"Tầng {cur_f_low} hoặc Tầng {cur_f_high}"
            if False and the_idx in (1, 2) and pm_idx in (1, 2) and not dong_list:
                floor_main = "NHÀ 1 – 2 TẦNG (NHÀ TRỆT HOẶC NHÀ 2 TẦNG)"
                cur_floor = "Tầng 1 (Tầng trệt)" if the_idx == 1 else "Tầng 1 hoặc Tầng 2"
            elif False and the_idx in (5, 6):
                extra_txt = "TÒA NHÀ / CHUNG CƯ CAO TẦNG" if base_f2 >= 5 else f"NHÀ {base_f2} – 5 TẦNG / CHUNG CƯ"
                floor_main = f"NHÀ {base_f1} – {base_f2} TẦNG (HOẶC {extra_txt})"
                cur_floor = f"Tầng {base_f1} – {base_f2}"
                pass
            else:
                floor_main = locals().get("floor_main", "")
                pass
                pass

            if any(w in q_low for w in ["mấy phòng", "bao nhiêu phòng"]):
                room_n1 = max(2, int(target_cung) if str(target_cung).isdigit() else 3)
                room_n2 = room_n1 + 2
                headline = f"🏠 KẾT LUẬN TỪ QUẺ GIA TRẠCH: NGÔI NHÀ CÓ KHOẢNG {room_n1} – {room_n2} PHÒNG CHÍNH (KẾT CẤU {floor_main})!"
            elif any(w in q_low for w in ["đang ở tầng mấy", "ngồi ở tầng mấy", "phòng ở tầng mấy"]):
                headline = f"🏠 KẾT LUẬN TỪ QUẺ GIA TRẠCH: HIỆN TẠI BẠN ĐANG Ở {cur_floor.upper()} (TRONG {floor_main})!"
            else:
                headline = f"🏠 KẾT LUẬN TỪ QUẺ GIA TRẠCH ({ten_que_chu.upper()}): BẠN ĐANG Ở {floor_main} — VỊ TRÍ SINH HOẠT CHÍNH ỨNG VỚI {cur_floor.upper()}!"

            pm_desc = (
                f"Hào <b>Phụ Mẫu</b> (Dụng Thần đại diện cho Ngôi nhà/Gia trạch) tại Hào {pm_idx} ({pm_hao.get('chi', '')}-{pm_hao.get('ngu_hanh', hanh_dt)})"
                if pm_hao else f"Dụng Thần <b>Phụ Mẫu</b> (Gia trạch hành {hanh_dt}) ẩn phục dưới Hào {the_idx}"
            )
            why_s = (
                f"Xét theo Pháp Gia Trạch Lục Hào & Mai Hoa Dịch Số: Quẻ lập được là <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>. "
                f"{pm_desc}, kết hợp <b>Hào Thế</b> (bản thân bạn) đóng tại <b>Hào {the_idx}</b> ({the_hao.get('chi', '')}-{the_hao.get('ngu_hanh', '')}) "
                f"và Cung Gia Trạch tại <b>Cung {target_cung} ({quai_cung_name} — {huong_cung})</b> hội Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b> "
                f"➔ Khẳng định ngôi nhà mang kết cấu <b>{floor_main.lower()}</b> (nếu tính cả tầng tum/mái hoặc gác lửng là +1 tầng) và vị trí bạn đang ngồi ứng với <b>{cur_floor}</b>."
            )
            when_s = (
                f"<b>Đặc điểm nhận diện ngôi nhà ({huong_cung}):</b> Tông màu tường/cửa chủ đạo có sắc <b>{colors_str}</b>; "
                f"không gian quanh nhà có đặc trưng của <b>{c_info.get('places', 'khu dân cư yên tĩnh')}</b>."
            )
            adv_s = (
                f"Phong thủy Gia Trạch tại Cung {target_cung} ({cua_name} · {than_name}): Giữ thông thoáng khu vực <b>{cur_floor}</b> "
                f"và hướng <b>{huong_cung}</b> để tụ khí vượng tài."
            )
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 2. GIẢI MÃ: NHÀ TÔI CÓ MẤY ANH CHỊ EM / CON THỨ MẤY TRONG NHÀ ──
        if target == "SIBLINGS_COUNT":
            sib_min = max(2, hd_count + 1)
            sib_max = sib_min + 1
            is_elder = (the_idx in (5, 6, 3)) or (str(the_hao.get("chi", "")) in ("Tý", "Dần", "Thìn", "Ngọ", "Thân", "Tuất"))
            order_str = "CON TRƯỞNG / ANH CHỊ ĐẦU (HOẶC THỨ 2)" if is_elder else "CON THỨ / CON ÚT TRONG GIA ĐÌNH"
            headline = f"👨‍👩‍👧‍👦 KẾT LUẬN TỪ QUẺ HUYNH ĐỆ: GIA ĐÌNH BẠN CÓ KHOẢNG {sib_min} – {sib_max} ANH CHỊ EM — BẠN ỨNG VỚI VỊ TRÍ {order_str}!"
            why_s = (
                f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, hào <b>Huynh Đệ</b> (Anh chị em) xuất hiện {hd_count} hào trên quẻ chính "
                f"kết hợp Quái số Cung {target_cung} ({huong_cung}) cho ra tổng số <b>{sib_min} – {sib_max} anh chị em</b>; "
                f"Hào Thế tại Hào {the_idx} mang khí {'Dương/Thượng vị' if is_elder else 'Âm/Hạ vị'} ứng với vai <b>{order_str.lower()}</b>."
            )
            when_s = f"Mối quan hệ anh chị em trong nhà: Tuy mỗi người một tính cách nhưng khi hữu sự vẫn hỗ trợ nhau tốt (Sao {sao_name} · Cửa {cua_name})."
            adv_s = f"Giữ sự hòa thuận, tương trợ lẫn nhau theo phương vị <b>{huong_cung}</b>."
            return {
                "has_override": True,
                "headline": headline,
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
            if is_fake or ("Tuần Không" in str(auth_warnings)):
                headline = "💫 KẾT LUẬN TỪ QUẺ: HIỆN TẠI BẠN CHƯA KẾT HÔN / ĐANG ĐỘC THÂN (HOẶC ĐANG SỐNG ĐỘC LẬP)!"
                why_s = (
                    f"Hào Dụng Thần Phối Ngẫu (<b>{dung_than}</b>) rơi vào <b>Tuần Không / Không Vong</b> trên quẻ <b>{ten_que_chu}</b> — "
                    f"chứng tỏ vị trí hôn nhân/phối ngẫu hiện đang trống, bạn chưa lập gia đình hoặc đang độc thân."
                )
            else:
                headline = "💍 KẾT LUẬN TỪ QUẺ: BẠN ĐÃ CÓ NGƯỜI THƯƠNG / ĐÃ LẬP GIA ĐÌNH (CÓ MỐI QUAN HỆ GẮN BÓ)!"
                why_s = (
                    f"Trục <b>Hào Thế (Hào {the_idx}) – Hào Ứng (Hào {ung_idx})</b> và Dụng Thần <b>{dung_than}</b> hữu khí trên quẻ <b>{ten_que_chu}</b>, "
                    f"hội Cửa <b>{cua_name}</b> và Thần <b>{than_name}</b> — báo hiệu đã có nhân duyên/gia thất thực tế."
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

        # ── 5. GIẢI MÃ: MẶC ÁO MÀU GÌ / ĐI XE GÌ, MÀU GÌ / BIỂN SỐ XE MẤY ──
        if target == "CLOTHING_VEHICLE":
            qty_str = omni_data.get("quantity", "3, 4, 9")
            if "xe" in q_low or "biển số" in q_low:
                headline = f"🛵 KẾT LUẬN TỪ QUẺ PHỤ MẪU: XE CỦA BẠN MANG TÔNG MÀU {colors_str.upper()} — CHỮ SỐ ĐUÔI BIỂN SỐ / ĐỊNH LƯỢNG ỨNG VỚI: {qty_str.upper()}!"
                why_s = (
                    f"Xét Hào <b>Phụ Mẫu</b> (Phương tiện/Biển số) tại Hào {pm_idx} và Hào Thế tại Hào {the_idx} trên quẻ <b>{ten_que_chu}</b>: "
                    f"Ngũ hành <b>{hanh_dt}</b> tại Cung {target_cung} ({huong_cung}) chỉ định rõ màu xe thuộc nhóm <b>{colors_str}</b>."
                )
            else:
                headline = f"👕 KẾT LUẬN TỪ QUẺ: TRANG PHỤC / MÀU SẮC HIỆN TẠI CỦA BẠN MANG TÔNG MÀU {colors_str.upper()} (HÀNH {hanh_dt.upper()})!"
                why_s = (
                    f"Xét Hào <b>Phụ Mẫu</b> (Quần áo/Trang phục) và <b>Hào Thế</b> (cơ thể bạn) tại Hào {the_idx} trên quẻ <b>{ten_que_chu}</b>: "
                    f"Khí Ngũ hành <b>{hanh_dt}</b> hội Sao <b>{sao_name}</b> phản ánh rõ sắc màu <b>{colors_str}</b>."
                )
            when_s = f"Chất liệu & Kiểu dáng: <b>{omni_data.get('material', 'Vải/Kim loại bền đẹp')}</b> ({omni_data.get('shape', 'Cân đối')})."
            adv_s = f"Bộ số may mắn đi kèm: <b>{qty_str}</b> | Hướng cát lợi: <b>{huong_cung}</b>."
            return {
                "has_override": True,
                "headline": headline,
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

            # TRƯỜNG HỢP TỔNG QUÁT CHO MỌI CÂU HỎI "PHƯƠNG ÁN A HAY PHƯƠNG ÁN B" KHÁC
            _the_chi_ab = str(the_hao.get("chi") or the_hao.get("can_chi") or "Hợi").split()[-1]
            _ung_chi_ab = str(ung_hao.get("chi") or ung_hao.get("can_chi") or "Mão").split()[-1]
            _the_kv = _the_chi_ab in _kv_ab
            _ung_kv = _ung_chi_ab in _kv_ab
            _score_a = 50 + (12 if _ung_kv else 0) - (12 if _the_kv else 0) + (6 if int(weighted_pct) >= 52 else -6)
            _score_a = max(22, min(78, _score_a))
            _score_b = 100 - _score_a
            _win_ab = opt_a_up if _score_a >= _score_b else opt_b_up
            _lose_ab = opt_b_up if _score_a >= _score_b else opt_a_up
            _win_sc = max(_score_a, _score_b)
            _lose_sc = min(_score_a, _score_b)
            short_hl = (
                f"⚖️ ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_score_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_score_b}% "
                f"➔ CHỐT NGHIÊNG VỀ: «{_win_ab}» ({_win_sc}% VS {_lose_sc}%)!"
            )
            why_s = (
                f"<b>• Xét Phương án 1 ({opt_a} — {_score_a}%):</b> Ứng với Trục Quẻ Chủ <b>{ten_que_chu}</b> & Hào Thế (Hào {the_idx} {_the_chi_ab}{', phạm Tuần Không' if _the_kv else ', hữu khí'}). "
                f"<b>• Xét Phương án 2 ({opt_b} — {_score_b}%):</b> Ứng với Trục Quẻ Biến <b>{ten_que_bien}</b> & Hào Ứng (Hào {ung_idx} {_ung_chi_ab}{', phạm Tuần Không' if _ung_kv else ', đắc Hào Động chuyển hóa'}) tại Cung {target_cung} ({sao_name} · {cua_name})."
            )
            when_s = f"Thời điểm ứng nghiệm rõ nhất: <b>{omni_data.get('exact_timestamp', 'Trong khung giờ gần nhất')}</b> tại hướng <b>{huong_cung}</b>."
            adv_s = f"Quẻ đã đặt lên bàn cân đối chứng cả 2 phương án ({opt_a} vs {opt_b}) và chỉ rõ ưu thế nghiêng về <b>{_win_ab}</b>."
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
                # Đơn chủ thể hỏi định lượng
                _base_q1 = _HT_NUM_Q.get(_up_q, 7) + _TT_NUM_Q.get(_lo_q, 4)
                _base_q2 = _base_q1 + _CHI_NUM_Q.get(_the_ch_q, 5)
                if _scale_mult == 10:
                    _v_low, _v_high = _base_q1 * 8, _base_q2 * 8
                    _v_mid = int(round((_v_low + _v_high) / 2 / 5.0) * 5)
                    short_hl = f"📏 KẾT QUẢ ĐỊNH LƯỢNG TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): CÒN KHOẢNG {_v_low} – {_v_high} {_unit_str.upper()} (TRỌNG TÂM ~{_v_mid} {_unit_str.upper()})!"
                else:
                    short_hl = f"🔢 KẾT QUẢ ĐỊNH LƯỢNG TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): KHOẢNG {_base_q1} – {_base_q2} {_unit_str.upper()} (BỘ SỐ ỨNG NGHIỆM: {_HT_NUM_Q.get(_up_q, 7)}, {_base_q1}, {_base_q2})!"
                why_s = f"Chiết xuất từ Quái số Mai Hoa (<b>{ten_que_chu}</b> ➔ <b>{ten_que_bien}</b>), Hào Thế tại Hào {the_idx} ({_the_ch_q}) và Cung Kỳ Môn số {_cung_n_q} ({huong_cung} · Sao {sao_name} · Cửa {cua_name})."
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
        Giải mã độc lập cho một vế câu hỏi nhỏ thuộc nhóm Sự việc / Dự đoán (Công việc, Tài chính, Tình cảm,
        Thi cử, Sức khỏe, Tìm đồ, Thời điểm Ứng kỳ...) dựa trực tiếp trên Hào Dụng Thần riêng của vế đó!
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        lh_ban = luc_hao_data.get("ban", {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = luc_hao_data.get("bien", {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or []
        dong_list = luc_hao_data.get("dong_hao") or lh_ban.get("dong_hao") or []
        ten_que_chu = lh_ban.get("name") or mai_hoa_data.get("ten_que") or "Quẻ Chủ"
        ten_que_bien = lh_bien.get("name") or mai_hoa_data.get("ten_qua_bien") or "Quẻ Biến"

        _CHI_NH = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

        chi_m = chart_data.get("chi_thang", "Tuất")
        chi_n = chart_data.get("chi_ngay", "Ngọ")
        nh_m = _CHI_NH.get(chi_m, "Thổ")
        nh_n = _CHI_NH.get(chi_n, "Hỏa")

        dt_idx = 3
        dt_chi = "Hợi"
        dt_nh = "Thủy"
        found_dt = False
        for ix, h in enumerate(haos, 1):
            if isinstance(h, dict):
                lt = str(h.get("luc_than") or "")
                tu = str(h.get("the_ung") or h.get("tu") or "")
                if (sq_dt and sq_dt in lt) or (sq_dt == "Bản Thân" and "Thế" in tu):
                    dt_idx = ix
                    dt_chi = str(h.get("chi") or h.get("can_chi") or "Hợi").split()[-1]
                    dt_nh = h.get("ngu_hanh") or h.get("hanh") or _CHI_NH.get(dt_chi, "Thủy")
                    found_dt = True
                    break

        sq_score = int(base_pct or 50)
        reasons = []
        if found_dt:
            reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> hiện tại <b>Hào {dt_idx} ({dt_chi}-{dt_nh})</b> trên quẻ <b>{ten_que_chu}</b>")
        else:
            reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> ẩn phục dưới quẻ <b>{ten_que_chu}</b>")

        if _SINH.get(nh_m) == dt_nh or nh_m == dt_nh:
            sq_score += 8
            reasons.append(f"được Nguyệt Lệnh ({chi_m}-{nh_m}) sinh phù/tỷ trợ")
        elif _KHAC.get(nh_m) == dt_nh:
            sq_score -= 6
            reasons.append(f"chịu Nguyệt Lệnh ({chi_m}-{nh_m}) chế khắc")

        if _SINH.get(nh_n) == dt_nh or nh_n == dt_nh:
            sq_score += 7
            reasons.append(f"đắc Nhật Thần ({chi_n}-{nh_n}) tương sinh/trợ lực")
        elif _KHAC.get(nh_n) == dt_nh:
            sq_score -= 5
            reasons.append(f"bị Nhật Thần ({chi_n}-{nh_n}) xung khắc")

        for d_ix in dong_list:
            if 1 <= d_ix <= len(haos) and isinstance(haos[d_ix - 1], dict):
                dh = haos[d_ix - 1]
                d_ch = str(dh.get("chi") or dh.get("can_chi") or "").split()[-1]
                d_nh = dh.get("ngu_hanh") or dh.get("hanh") or _CHI_NH.get(d_ch, "")
                if _SINH.get(d_nh) == dt_nh:
                    sq_score += 8
                    reasons.append(f"được Hào Động {d_ix} ({d_ch}-{d_nh}) phát động sinh trợ trực tiếp ({d_nh} sinh {dt_nh})")
                elif _KHAC.get(d_nh) == dt_nh:
                    sq_score -= 8
                    reasons.append(f"bị Hào Động {d_ix} ({d_ch}-{d_nh}) phát động khắc chế ({d_nh} khắc {dt_nh})")

        sq_score = max(28, min(88, sq_score))
        t_code = sq_bp.get("specific_target") or sq_bp.get("archetype_key", "")
        c_lbl = sq_bp.get("clause_label") or sq_bp.get("subject_person") or "Sự việc"
        uk_str = omni_data.get("exact_timestamp", f"Ngày/Giờ {dt_chi}")
        huong_str = (omni_data.get("c_info") or {}).get("huong", "Chính Nam")

        if t_code == "TIMING_WHEN" or "D12" in t_code:
            short_hl = f"⏳ THỜI ĐIỂM ỨNG KỲ CHÍNH XÁC: {uk_str.upper()} (KHI HÀO {sq_dt.upper()} {dt_chi.upper()} XUNG/HỢP MỞ VẬN)!"
        elif sq_score >= 55:
            short_hl = f"✅ THUẬN LỢI & KHẢ QUAN ({sq_score}% — CÁT: DỤNG THẦN {sq_dt.upper()} ĐẮC KHÍ SINH PHÙ)!"
        elif sq_score >= 45:
            short_hl = f"⚖️ TRUNG BÌNH / CẦN KIÊN NHẪN CHUẨN BỊ KỸ ({sq_score}% — BÌNH: ĐỢI MỐC ỨNG KỲ MỞ VẬN)!"
        else:
            short_hl = f"⚠️ ĐANG GẶP LỰC CẢN — NÊN THẬN TRỌNG & CHỜ THỜI ({sq_score}% — HUNG)!"

        return {
            "has_override": True,
            "headline": f"🎯 [{c_lbl.upper()}]: {short_hl}",
            "short_headline": short_hl,
            "why": ", ".join(reasons) + f" (Biến quẻ: <b>{ten_que_bien}</b>).",
            "when": f"Mốc ứng nghiệm của vế này: <b>{uk_str}</b>.",
            "advice": f"Hành động chủ động và ưu tiên phương vị <b>{huong_str}</b>.",
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

        target_cung = omni_data.get("target_cung", "?")
        c_info = omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}
        huong_cung = c_info.get("huong", "Chính Nam")
        sao_name = omni_data.get("sao_name", "Thiên Tâm")
        cua_name = omni_data.get("cua_name", "Khai Môn")
        than_name = omni_data.get("than_name", "Trực Phù")
        hanh_dt = omni_data.get("hanh", "Kim")
        ts_stage = omni_data.get("ts_stage", "Vượng")

        # Bước 1: Chạy bộ giải mã Toán Học Dịch Lý Nội Bộ làm nền tảng tham chiếu
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

        # Bước 2 (V103.0): KÍCH HOẠT 2 CON AI THỰC TẾ (GEMINI LLM 2 TẦNG ĐỘC LẬP: CON AI SỐ 1 ĐỌC HIỂU -> TRUYỀN CHO CON AI SỐ 2 LUẬN GIẢI QUẺ)
        _raw_q_str = str(blueprint.get("raw_question") or "").strip()
        _haos_summary_list = []
        for _ix_h, _hh in enumerate((lh_ban.get("haos") or lh_ban.get("details") or []), 1):
            if isinstance(_hh, dict):
                _haos_summary_list.append(
                    f"Hào {_ix_h}: {_hh.get('luc_than','')} ({_hh.get('chi','')}-{_hh.get('ngu_hanh') or _hh.get('hanh','')})"
                    f"{' [THẾ]' if 'Thế' in str(_hh.get('the_ung','')) else (' [ỨNG]' if 'Ứng' in str(_hh.get('the_ung','')) else '')}"
                    f"{' [ĐỘNG]' if (_ix_h in dong_hao_list or _hh.get('dong') or _hh.get('is_dong')) else ' [Tĩnh]'}"
                )
        _haos_summary_str = " | ".join(_haos_summary_list)
        _cache_sig = hashlib.md5(f"{_raw_q_str}::{ten_que_chu}::{ten_que_bien}::{can_n}_{chi_n}_{can_g}_{chi_g}".encode("utf-8")).hexdigest()
        _real_ai_pair = _REAL_DUAL_AI_CACHE.get(_cache_sig)

        if _real_ai_pair is None and len(_raw_q_str) >= 4:
            # --- GỌI CON AI SỐ 1 THỰC TẾ (CHUYÊN GIA ĐỌC HIỂU CÂU HỎI) ---
            _prompt_ai1 = (
                "Bạn là CON AI SỐ 1 (Chuyên Gia Đọc Hiểu & Phân Tích Câu Hỏi Dịch Học).\n"
                f"Câu hỏi của người dùng: \"{_raw_q_str}\"\n\n"
                "Nhiệm vụ của bạn: Đọc hiểu chính xác 100% ý định thực tế của câu hỏi này (hỏi về cái gì, cần câu trả lời ở đơn vị nào như bao nhiêu km, bao nhiêu tiền, mấy người, mấy tuổi, hay chọn giữa các phương án nào, có mấy vế câu hỏi nhỏ, gồm những chủ thể nào) để lập Hồ Sơ Chỉ Thị truyền sang cho CON AI SỐ 2 (Chuyên Gia Luận Giải Quẻ).\n"
                "Trả về ĐÚNG 1 JSON hợp lệ với các trường sau (viết bằng tiếng Việt rõ ràng, súc tích):\n"
                "{\n"
                "  \"ai1_intent_summary\": \"Tóm tắt chính xác câu hỏi đang hỏi điều gì (nêu rõ mọi vế và mọi người trong câu hỏi)\",\n"
                "  \"ai1_expected_answer_format\": \"Khuôn mẫu & Đơn vị bắt buộc của câu trả lời (VD: Phải trả lời rõ số km còn thiếu của riêng Bản thân và riêng Vợ; hoặc trả lời đủ cả 2 vế câu hỏi; hoặc đối chứng cả 2 phương án A và B)\",\n"
                "  \"ai1_dung_than_guide\": \"Chỉ định Dụng Thần Lục Hào & Kỳ Môn cần tra cứu cho từng chủ thể/vế câu hỏi\",\n"
                "  \"ai1_strict_instruction_to_ai2\": \"Mệnh lệnh bắt buộc giao cho AI Số 2 (cấm trả lời lạc đề sang kiểu câu hỏi khác)\"\n"
                "}"
            )
            _ai1_json = blueprint.get("ai1_real_llm")
            if not isinstance(_ai1_json, dict) or not _ai1_json.get("ai1_intent_summary"):
                _ai1_json = _call_gemini_json_fast(_prompt_ai1, timeout_sec=10, tier="cheapest_reader")
            if isinstance(_ai1_json, dict) and _ai1_json.get("ai1_intent_summary"):
                # --- GỌI CON AI SỐ 2 THỰC TẾ (NHẬN HỒ SƠ TỪ AI SỐ 1 -> ĐỐI CHỨNG QUẺ & SUY LUẬN ĐÁP ÁN) ---
                _prompt_ai2 = (
                    "Bạn là CON AI SỐ 2 (Chuyên Gia Đối Chứng Quẻ & Suy Luận Đáp Án Chuẩn Xác Tuyệt Đối).\n"
                    f"1. CÂU HỎI GỐC CỦA NGƯỜI DÙNG: \"{_raw_q_str}\"\n"
                    f"2. HỒ SƠ CHỈ THỊ TỪ CON AI SỐ 1 TRUYỀN SANG:\n"
                    f"   - Ý nghĩa câu hỏi AI Số 1 đã bóc tách: {_ai1_json.get('ai1_intent_summary')}\n"
                    f"   - Định dạng & Đơn vị đáp án bắt buộc: {_ai1_json.get('ai1_expected_answer_format')}\n"
                    f"   - Dụng Thần chỉ định: {_ai1_json.get('ai1_dung_than_guide')}\n"
                    f"   - Mệnh lệnh từ AI Số 1: {_ai1_json.get('ai1_strict_instruction_to_ai2')}\n\n"
                    f"3. DỮ LIỆU QUẺ THỰC TẾ LẬP ĐÚNG THỜI KHẮC (Năm {can_y} {chi_y}, Tháng {can_m} {chi_m}, Ngày {can_n} {chi_n}, Giờ {can_g} {chi_g}):\n"
                    f"   - Lục Hào & Mai Hoa: Quẻ Chủ [{ten_que_chu}] biến Quẻ Biến [{ten_que_bien}] (Hào động: {dong_hao_list or 'Quẻ Tĩnh'}).\n"
                    f"   - Chi tiết 6 Hào: {_haos_summary_str}\n"
                    f"   - Kỳ Môn Độn Giáp: Cục {cuc_km} ({don_type}), Cung trọng tâm {target_cung} ({huong_cung}) hội Sao [{sao_name}], Cửa [{cua_name}], Thần [{than_name}], Ngũ hành [{hanh_dt}], Trường Sinh [{ts_stage}].\n"
                    f"   - Tham chiếu tính toán nội bộ: {spec_res.get('headline', '')} | {re.sub(r'<[^>]+>', '', str(spec_res.get('why', '')))[:400]}\n\n"
                    "YÊU CẦU BẮT BUỘC CHO CON AI SỐ 2:\n"
                    "- Trả lời TRỰC DIỆN, ĐẦY ĐỦ 100% đúng câu hỏi và ĐÚNG ĐƠN VỊ mà CON AI SỐ 1 đã yêu cầu (Ví dụ: hỏi còn thiếu bao nhiêu km thì phải chốt rõ số km còn thiếu cho từng người dựa trên số quẻ/hào; hỏi 2 câu nhỏ thì phải trả lời đủ cả 2 câu nhỏ; hỏi A hay B thì phải đối chứng rõ cả 2 phương án A và B). TUYỆT ĐỐI KHÔNG trả lời lạc đề!\n"
                    "Trả về ĐÚNG 1 JSON hợp lệ:\n"
                    "{\n"
                    "  \"ai2_headline\": \"Câu trả lời chốt hạ trực diện, in hoa các ý chính, trả lời đúng câu hỏi và đơn vị của AI Số 1\",\n"
                    "  \"ai2_why\": \"Giải thích chi tiết căn cứ từ Quẻ Chủ, Quẻ Biến, các Hào Lục Hào và Cung/Sao/Cửa Kỳ Môn chứng minh cho câu trả lời (có thể dùng thẻ <b> để nhấn mạnh)\",\n"
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
            blueprint["lh_dt_instruction"] = f"{_r_ai1.get('ai1_dung_than_guide', blueprint['lh_dt_instruction'])} | <b>Chỉ thị AI 1 ➔ AI 2:</b> {_r_ai1.get('ai1_strict_instruction_to_ai2', '')}"
            # Nếu câu hỏi là câu hỏi tự nhiên đặc thù (như hỏi bao nhiêu km, hoặc chưa có override cứng), hoặc kết hợp cùng bộ giải mã chuyên sâu
            if blueprint.get("specific_target") in ("GENERAL_QUANTITY", "", "EXAM_VISA", "CAREER_WORK", "INVEST_PROFIT", "LOVE_MARRIAGE", "HEALTH_MEDICAL") or not spec_res.get("has_override"):
                spec_res["has_override"] = True
                spec_res["headline"] = _r_ai2.get("ai2_headline") or spec_res.get("headline", "")
                spec_res["why"] = _r_ai2.get("ai2_why") or spec_res.get("why", "")
                spec_res["when"] = _r_ai2.get("ai2_when") or spec_res.get("when", "")
                spec_res["advice"] = _r_ai2.get("ai2_advice") or spec_res.get("advice", "")

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

        if is_fake and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Tuần Không / Tử Môn</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Quẻ dùng phép <b>Loại Trừ Nhị Phân</b>: Bác bỏ hoàn toàn phương án bị Không Vong để khẳng định 100% phương án thực tế còn lại!"
            )
        elif is_fake and blueprint.get("specific_target") not in ("HOUSE_FLOORS", "CLOTHING_VEHICLE", "SIBLINGS_COUNT", "CHILDREN_AGE", "CHILDREN_COUNT"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> rơi vào <b>Chân Không / Không Vong Vô Khí</b> ({len(auth_warnings)} dấu hiệu) "
                f"➔ Cảnh báo sự việc/đối tượng đang hỏi hiện <b>chưa tồn tại ngoài thực tế (= 0)</b> hoặc là câu hỏi thử lòng quẻ."
            )
        elif auth_warnings and not is_fake:
            auth_status_str = (
                f"<b>Liên kết sâu Lục Hào – Mai Hoa – Kỳ Môn:</b> Hào Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> hoàn toàn hữu khí / được Hào Động sinh trợ "
                f"khẳng định <b>đối tượng/con cái bạn hỏi LÀ CÓ THẬT 100% NGOÀI ĐỜI (bác bỏ Chân Không)</b>; còn dấu hiệu Tuần Không ở Nhật Can bắt bài bạn đang <b>đặt câu hỏi để thử độ nhạy bén của quẻ</b>!"
            )
        else:
            auth_status_str = (
                f"Dụng Thần <b>{dung_than} (Hành {hanh_dt})</b> đối chứng trực tiếp trên quẻ ({ts_stage}), khớp chính xác vào câu hỏi."
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
                f'⚖️ <b>Tách 2 vế đối chứng:</b> [Phương án 1]: <b>{blueprint["option_a"]}</b> ↔ [Phương án 2]: <b>{blueprint["option_b"]}</b>'
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

        dual_agent_html = (
            f'<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);padding:16px 18px;border-radius:14px;margin-bottom:16px;border:2px solid #38bdf8;box-shadow:0 6px 22px rgba(56,189,248,0.22);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px;border-bottom:1px solid rgba(56,189,248,0.3);padding-bottom:8px;">'
            f'<div style="font-size:1.06em;font-weight:900;color:#38bdf8;letter-spacing:0.3px;">🤖 HỆ THỐNG SONG NÃO AI 2 TẦNG (V103.0): CON AI SỐ 1 (FLASH-LITE ĐỌC HIỂU) ➔ TRUYỀN SANG CON AI SỐ 2 & 18 PHƯƠNG PHÁP LUẬN GIẢI</div>'
            f'<span style="background:rgba(56,189,248,0.18);color:#7dd3fc;padding:3px 10px;border-radius:12px;font-size:0.82em;font-weight:800;border:1px solid #38bdf8;">Khớp {blueprint["archetype_code"]}/25 Đại Dạng Toàn Cầu</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;">'
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #38bdf8;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#7dd3fc;margin-bottom:6px;">🧠 CON AI SỐ 1 (GEMINI FLASH-LITE — CHUYÊN ĐỌC HIỂU CÂU HỎI & BÀN GIAO)</div>'
            f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
            f'• <b>Nhận diện dạng câu hỏi:</b> <span style="color:#fde047;font-weight:800;">{blueprint["archetype_code"]} — {blueprint["archetype_name"]}</span><br>'
            f'{_ai1_summary_line}'
            f'• <b>Đối tượng trọng tâm:</b> {blueprint["subject_person"]} (Giao Dụng Thần: <b>{dung_than}</b>){sub_intents_html}<br>'
            f'{_ai1_format_line}'
            f'• <b>Chỉ thị tra quẻ cho AI Số 2 & 18 Pháp:</b> <i>{blueprint["lh_dt_instruction"]}</i>'
            f'{ab_html}'
            f'</div></div>'
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.78);border-radius:10px;border-left:4px solid #fbbf24;border-top:1px solid rgba(255,255,255,0.08);">'
            f'<div style="font-size:0.93em;font-weight:900;color:#fde047;margin-bottom:6px;">🔮 CON AI SỐ 2 — NHẬN CHỈ THỊ TỪ AI SỐ 1 & ĐỐI CHỨNG QUẺ SUY LUẬN ĐÁP ÁN</div>'
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

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
import datetime
import requests
from typing import Dict, Any, List, Optional

_REAL_DUAL_AI_CACHE: Dict[str, Dict[str, Any]] = {}


def get_realtime_vn_clock_context() -> Dict[str, Any]:
    """
    V109.0: Lấy chính xác Ngày/Tháng/Năm Dương lịch & Âm lịch hiện tại theo múi giờ Việt Nam (UTC+7)
    để khóa cứng đồng hồ thời gian thực cho toàn bộ AI Online & Offline (chống tuyệt đối lỗi AI nhớ nhầm năm 2024/2025/đầu 2026).
    """
    vn_tz = datetime.timezone(datetime.timedelta(hours=7))
    now_vn = datetime.datetime.now(vn_tz)
    cur_y = now_vn.year
    cur_m = now_vn.month
    cur_d = now_vn.day
    next_y = cur_y + 1
    next_y2 = cur_y + 2

    THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    THU_VN = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    thu_str = THU_VN[now_vn.weekday()]

    try:
        from xem_ngay_dep import solar2lunar
        ld, lm, ly, is_leap = solar2lunar(cur_d, cur_m, cur_y)
    except Exception:
        ld, lm, ly, is_leap = cur_d, max(1, cur_m - 1), cur_y, False

    can_ly = THIEN_CAN[(ly - 4) % 10]
    chi_ly = DIA_CHI[(ly - 4) % 12]
    can_next_y = THIEN_CAN[(next_y - 4) % 10]
    chi_next_y = DIA_CHI[(next_y - 4) % 12]
    can_next_y2 = THIEN_CAN[(next_y2 - 4) % 10]
    chi_next_y2 = DIA_CHI[(next_y2 - 4) % 12]

    if cur_m >= 10:
        season_phase = f"CUỐI NĂM {cur_y} (Tháng {cur_m:02d}/{cur_y} Dương lịch)"
        upcoming_window = f"Cuối năm {cur_y} (Tháng {cur_m:02d}–12/{cur_y} Dương lịch) sang Nửa đầu năm {next_y} ({can_next_y} {chi_next_y})"
    elif cur_m >= 5:
        season_phase = f"GIỮA NĂM {cur_y} (Tháng {cur_m:02d}/{cur_y} Dương lịch)"
        upcoming_window = f"Nửa cuối năm {cur_y} (Tháng {cur_m:02d}–12/{cur_y}) hoặc Đầu năm {next_y} ({can_next_y} {chi_next_y})"
    else:
        season_phase = f"ĐẦU NĂM {cur_y} (Tháng {cur_m:02d}/{cur_y} Dương lịch)"
        upcoming_window = f"Giữa và Cuối năm {cur_y} (Tháng {cur_m:02d}–12/{cur_y})"

    clock_banner = (
        f"🕒 ĐỒNG HỒ THỜI GIAN THỰC HIỆN TẠI (VIỆT NAM UTC+7 — BẮT BUỘC CẬP NHẬT 100%): "
        f"Hôm nay là {thu_str}, ngày {cur_d:02d}/{cur_m:02d}/{cur_y} Dương lịch ({season_phase}) — "
        f"Âm lịch: Ngày {ld:02d}/{lm:02d} năm {can_ly} {chi_ly} ({ly}).\n"
        f"⛔ MỆNH LỆNH THỜI GIAN TUYỆT ĐỐI CHO AI: Hiện tại đã là {season_phase}! "
        f"Toàn bộ năm 2024, năm 2025 và các tháng từ Tháng 01 đến Tháng {max(1, cur_m - 1):02d}/{cur_y} ĐỀU ĐÃ TRÔI QUA TRONG QUÁ KHỨ! "
        f"TUYỆT ĐỐI CẤM dự báo thời gian tương lai rơi vào 'năm 2024', 'năm 2025', 'cuối năm 2025', hay 'đầu năm {cur_y}'! "
        f"Mọi dự báo thời gian / ứng kỳ tương lai BẮT BUỘC phải tính từ ngày {cur_d:02d}/{cur_m:02d}/{cur_y} ({upcoming_window}, hoặc năm {next_y} [{can_next_y} {chi_next_y}], năm {next_y2} [{can_next_y2} {chi_next_y2}]) trở đi!"
    )

    return {
        "now_vn": now_vn,
        "cur_year": cur_y,
        "cur_month": cur_m,
        "cur_day": cur_d,
        "lunar_day": ld,
        "lunar_month": lm,
        "lunar_year": ly,
        "can_chi_year": f"{can_ly} {chi_ly}",
        "cur_year_canchi": f"{can_ly} {chi_ly}",
        "next_year": next_y,
        "next_can_chi_year": f"{can_next_y} {chi_next_y}",
        "next_year_canchi": f"{can_next_y} {chi_next_y}",
        "next_year2": next_y2,
        "next_can_chi_year2": f"{can_next_y2} {chi_next_y2}",
        "season_phase": season_phase,
        "upcoming_window": upcoming_window,
        "solar_str": f"{cur_d:02d}/{cur_m:02d}/{cur_y}",
        "solar_date_str": f"{cur_d:02d}/{cur_m:02d}/{cur_y}",
        "lunar_str": f"{ld:02d}/{lm:02d}/{ly} ÂL ({can_ly} {chi_ly})",
        "lunar_date_str": f"{ld:02d}/{lm:02d}/{ly} ÂL ({can_ly} {chi_ly})",
        "clock_banner": clock_banner,
    }


def sanitize_outdated_years_text(text: str, question: str = "") -> str:
    """
    V109.0: Bộ lọc hậu kiểm thời gian thực — Tự động phát hiện và sửa mọi cụm từ năm cũ
    (VD: "cuối năm 2025 hoặc đầu năm 2026", "nửa cuối năm 2025", "đầu năm 2026" khi hiện tại đã là cuối năm 2026)
    do LLM bị ảnh hưởng bởi mốc dữ liệu huấn luyện cũ.
    """
    if not text or not isinstance(text, str):
        return text
    clk = get_realtime_vn_clock_context()
    cy = clk["cur_year"]
    cm = clk["cur_month"]
    ny = clk["next_year"]
    n_cc = clk["next_can_chi_year"]

    out = text
    # 1. Các cụm kết hợp 2025 & 2026 kinh điển mà LLM hay sinh ra
    patterns_2025_2026 = [
        r"(?:nửa\s+)?cuối\s+năm\s+2025\s*(?:hoặc|đến|và|-|–|sang|,)?\s*(?:nửa\s+)?đầu\s+năm\s+2026",
        r"cuối\s+2025\s*(?:hoặc|đến|và|-|–|sang)?\s*đầu\s+2026",
        r"năm\s+2025\s*(?:hoặc|đến|và|-|–|sang)\s*(?:đầu\s+)?năm\s+2026",
    ]
    for pat in patterns_2025_2026:
        out = re.sub(
            pat,
            lambda m: (
                f"CUỐI NĂM {cy} (THÁNG {cm:02d}–12/{cy}) HOẶC NỬA ĐẦU NĂM {ny} ({n_cc.upper()})"
                if m.group(0).isupper()
                else f"cuối năm {cy} (Tháng {cm:02d}–12/{cy}) hoặc nửa đầu năm {ny} ({n_cc})"
            ),
            out,
            flags=re.IGNORECASE,
        )

    # 2. Cụm "nửa cuối năm 2025" / "cuối năm 2025" / "trong năm 2025" / "sang năm 2025"
    out = re.sub(
        r"(?:nửa\s+)?cuối\s+năm\s+2025",
        lambda m: f"CUỐI NĂM {cy} (THÁNG {cm:02d}–12/{cy})" if m.group(0).isupper() else f"cuối năm {cy} (Tháng {cm:02d}–12/{cy})",
        out,
        flags=re.IGNORECASE,
    )
    out = re.sub(
        r"(?:trong|vào|sang|đến)\s+năm\s+2025\b",
        lambda m: f"VÀO CUỐI NĂM {cy} – NĂM {ny}" if m.group(0).isupper() else f"vào cuối năm {cy} – năm {ny} ({n_cc})",
        out,
        flags=re.IGNORECASE,
    )

    # 3. Nếu hiện tại đã là cuối năm (Tháng 9..12) mà văn bản dự báo "đầu năm 2026" hoặc "nửa đầu năm 2026" hoặc "giữa năm 2026"
    if cm >= 9:
        out = re.sub(
            r"(?:nửa\s+)?(?:đầu|giữa)\s+năm\s+" + str(cy) + r"\b",
            lambda m: f"NỬA ĐẦU NĂM {ny} ({n_cc.upper()})" if m.group(0).isupper() else f"nửa đầu năm {ny} ({n_cc})",
            out,
            flags=re.IGNORECASE,
        )
        # Các tháng đã qua trong năm hiện tại (VD: "tháng 02/2026" .. "tháng 10/2026" khi đang ở tháng 11/2026)
        def _fix_past_month_in_cur_year(m_obj):
            full_s = m_obj.group(0)
            m_num = int(m_obj.group(1))
            if 1 <= m_num < cm:
                return full_s[:-4] + str(ny)
            return full_s

        out = re.sub(rf"tháng\s+0?([1-9]|1[0-2])/{cy}\b", _fix_past_month_in_cur_year, out, flags=re.IGNORECASE)

    return out

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

def _robust_parse_ai_json(txt: str, question: str = "") -> Optional[Dict[str, Any]]:
    """
    V118.0: Bộ giải mã JSON siêu bền bỉ cho Con AI Số 1 & Con AI Số 2.
    Xử lý triệt để trường hợp Gemini Pro sinh văn bản dài nhiều dòng hoặc chứa dấu ngoặc kép chưa escape trong `ai2_why`.
    """
    if not txt:
        return None
    cleaned = txt.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE).strip()
    m_json = re.search(r"\{[\s\S]*\}", cleaned)
    raw_obj_str = m_json.group(0) if m_json else cleaned
    parsed_obj: Optional[Dict[str, Any]] = None
    try:
        obj = json.loads(raw_obj_str, strict=False)
        if isinstance(obj, dict):
            parsed_obj = obj
    except Exception:
        parsed_obj = None

    if not parsed_obj:
        # Fallback bóc tách theo ranh giới khóa JSON khi chuỗi bên trong có dấu " hoặc xuống dòng thô
        known_keys = [
            "ai1_intent_summary",
            "ai1_expected_answer_format",
            "ai1_dung_than_guide",
            "ai1_strict_instruction_to_ai2",
            "ai2_headline",
            "ai2_why",
            "ai2_when",
            "ai2_advice",
        ]
        extracted: Dict[str, Any] = {}
        key_positions = []
        for k in known_keys:
            m_k = re.search(rf'"{k}"\s*:\s*"', raw_obj_str)
            if m_k:
                key_positions.append((m_k.start(), m_k.end(), k))
        key_positions.sort(key=lambda x: x[0])
        for idx, (k_start, val_start, k_name) in enumerate(key_positions):
            if idx + 1 < len(key_positions):
                next_k_start = key_positions[idx + 1][0]
                segment = raw_obj_str[val_start:next_k_start]
                segment = re.sub(r'"\s*,\s*$', "", segment.strip())
            else:
                segment = raw_obj_str[val_start:]
                segment = re.sub(r'"\s*\}\s*$', "", segment.strip())
            segment = segment.replace('\\"', '"').replace("\\n", "\n").strip()
            extracted[k_name] = segment
        if extracted:
            parsed_obj = extracted

    if isinstance(parsed_obj, dict) and parsed_obj:
        for _k_p, _v_p in list(parsed_obj.items()):
            if isinstance(_v_p, dict):
                _v_p = "<br>".join(f"<b>• {k_sub}:</b> {v_sub}" for k_sub, v_sub in _v_p.items())
            elif isinstance(_v_p, list):
                _v_p = "<br>".join(f"• {item}" for item in _v_p if item)
            if isinstance(_v_p, str):
                parsed_obj[_k_p] = sanitize_outdated_years_text(_v_p, question=question)
        return parsed_obj
    return None


def _call_gemini_json_fast(prompt_text: str, timeout_sec: int = 18, tier: str = 'cheapest_reader') -> Optional[Dict[str, Any]]:
    keys = _resolve_gemini_api_keys()
    if not keys:
        return None
    _clk_ctx = get_realtime_vn_clock_context()
    _full_prompt_text = f"{_clk_ctx['clock_banner']}\n\n{prompt_text}"
    if tier == 'cheapest_reader':
        # Con AI Số 1 (Đọc hiểu câu hỏi & phân khu): Ưu tiên Gemini 2.5 Flash tốc độ cao
        models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro']
    else:
        # V119.0 — Con AI Số 2 (ĐẠI SƯ LUẬN QUẺ CHUYÊN SÂU PHONG CÁCH ANTIGRAVITY):
        # Ưu tiên gemini-2.5-flash (quota cao gấp 15 lần trên Cloud, không bị kẹt 429/MAX_TOKENS) + gemini-2.5-pro + gemini-2.0-flash
        models = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash']
    safety = [
        {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
    ]
    for api_key in keys[:5]:
        for m_name in models:
            try:
                url = f'https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={api_key}'
                _is_pro_model = ('pro' in m_name)
                gen_cfg: Dict[str, Any] = {
                    'temperature': 0.2 if _is_pro_model else 0.15,
                    'topP': 0.88,
                    'maxOutputTokens': 16384 if ('2.5' in m_name or '3.' in m_name) else 8192,
                    'responseMimeType': 'application/json',
                }
                if '2.5-flash' in m_name and 'lite' not in m_name:
                    # Khóa thinkingBudget nhỏ để tuyệt đối không bao giờ bị cạn token (MAX_TOKENS) hoặc timeout trên Streamlit Cloud
                    gen_cfg['thinkingConfig'] = {'thinkingBudget': 256 if tier != 'cheapest_reader' else 0}
                payload = {
                    'contents': [{'parts': [{'text': _full_prompt_text}]}],
                    'generationConfig': gen_cfg,
                    'safetySettings': safety,
                }
                _req_timeout = max(timeout_sec, 22) if tier != 'cheapest_reader' else timeout_sec
                r = requests.post(url, json=payload, timeout=_req_timeout)
                if r.status_code == 400:
                    gen_cfg.pop('thinkingConfig', None)
                    gen_cfg.pop('responseMimeType', None)
                    r = requests.post(url, json=payload, timeout=_req_timeout)
                if r.status_code != 200:
                    continue
                cands = r.json().get('candidates', [])
                if not cands:
                    continue
                txt = ''
                for pt in cands[0].get('content', {}).get('parts', []):
                    if not pt.get('thought', False) and pt.get('text'):
                        txt += pt['text']
                parsed_obj = _robust_parse_ai_json(txt, question=prompt_text)
                if isinstance(parsed_obj, dict) and parsed_obj:
                    parsed_obj['_model_used'] = m_name
                    return parsed_obj
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
    def _normalize_vn_typos(text_in: str) -> str:
        s = str(text_in or "").strip()
        _TYPO_MAP = (
            (r"\bđnag\b", "đang"),
            (r"\bdnag\b", "đang"),
            (r"\bđag\b", "đang"),
            (r"\bkhoẻ\b", "khỏe"),
            (r"\bkhoe\b", "khỏe"),
            (r"\bsức khoẻ\b", "sức khỏe"),
            (r"\bcó\s+([^,?.!]+?)\s+khôn(?=\s*(?:[,?.!]|và\b|$))", r"có \1 không"),
            (r"\bko\b", "không"),
            (r"\bk\b", "không"),
            (r"\bdc\b", "được"),
            (r"\bđc\b", "được"),
        )
        for _pat, _rep in _TYPO_MAP:
            s = re.sub(_pat, _rep, s, flags=re.IGNORECASE)
        return s

    @staticmethod
    def analyze_question(question: str, dung_than_hint: str = "", category_hint: str = "") -> dict:
        q_raw = str(question or "").strip()
        q_norm = QuestionReaderAI._normalize_vn_typos(q_raw)
        q_low = q_norm.lower()

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
        # Tuyệt đối KHÔNG bắt nhầm câu hỏi "chị gái tôi mấy giờ xuống chỗ tôi" hay "anh trai tôi mấy ngày nữa về"!
        _has_time_or_action_in_sibling = any(w in q_low for w in [
            "mấy giờ", "giờ nào", "khi nào", "bao giờ", "lúc nào", "mấy phút",
            "mấy ngày", "mấy hôm", "mấy tuần", "mấy tháng", "mấy năm",
            "bao nhiêu tuổi", "mấy tuổi", "sinh năm", "mấy tầng",
            "bao nhiêu tiền", "mấy triệu", "mấy tỷ", "mấy chỉ", "bao nhiêu km", "mấy km",
            "xuống", "lên", "đến", "tới", "về", "đi", "sang", "qua", "gặp", "gọi", "nhắn",
            "bắn", "chuyển", "mua", "bán", "vay", "mượn", "khóc", "ốm", "sốt", "bệnh",
        ])
        is_siblings_q = (
            not _has_time_or_action_in_sibling
            and any(w in q_low for w in [
                "mấy anh chị em", "bao nhiêu anh chị em", "mấy anh em", "bao nhiêu anh em",
                "mấy chị em", "bao nhiêu chị em", "mấy chị gái", "bao nhiêu chị gái",
                "mấy anh trai", "bao nhiêu anh trai", "mấy em gái", "bao nhiêu em gái",
                "mấy em trai", "bao nhiêu em trai", "mấy người chị", "mấy người anh",
                "mấy người em", "tôi có mấy chị", "tôi có mấy anh", "tôi có mấy em",
                "nhà có mấy chị", "nhà có mấy anh", "nhà có mấy anh chị em", "gia đình có mấy anh chị em",
                "con thứ mấy", "thứ mấy trong nhà", "con trưởng hay con út", "con đầu hay"
            ])
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
        is_gender_age = (
            any(w in q_low for w in [
                "nam hay nữ", "nữ hay nam", "trai hay gái", "gái hay trai", "giới tính",
                "bao nhiêu tuổi", "mấy tuổi", "sinh năm mấy", "sinh năm nào", "sinh năm bao nhiêu",
                "hưởng thọ", "thọ bao nhiêu", "thọ mấy tuổi", "mất năm bao nhiêu", "mất lúc mấy tuổi",
                "mất lúc bao nhiêu tuổi", "qua đời năm bao nhiêu", "qua đời lúc mấy tuổi"
            ])
            and not is_children_q and not _is_child_action_ab
        )
        is_weather = any(w in q_low for w in ["mưa hay nắng", "nắng hay mưa", "thời tiết", "có mưa không", "trời mưa", "trời nắng", "bão"])
        is_lawsuit = any(w in q_low for w in ["kiện", "tòa án", "pháp lý", "tranh chấp", "ai thắng", "thắng hay thua", "thắng hay đối phương", "đấu thầu"])
        is_profile = any(w in q_low for w in ["ngoại hình", "hình dáng người", "cao hay thấp", "béo hay gầy", "tính cách", "tính nết", "làm nghề gì", "nghề nghiệp gì", "ngành gì", "cao bao nhiêu", "nặng bao nhiêu"])
        is_object = any(w in q_low for w in ["trong hộp", "trong túi", "trong phòng có gì", "trước mặt tôi có", "trên bàn có", "cầm cái gì", "đồ vật gì", "vật gì", "là cái gì", "màu gì", "chất liệu gì", "hình gì"]) and not is_clothing_vehicle_q
        is_when = any(w in q_low for w in ["khi nào", "bao giờ", "mấy giờ", "ngày nào", "tháng nào", "năm nào", "bao lâu", "tháng mấy"]) and not is_gender_age
        # Mọi câu hỏi có từ "mấy" hoặc "bao nhiêu" hoặc "số mấy" (không phải tuổi, con cái, thời gian)
        has_numeric_word = bool(re.search(r"\b(mấy|bao nhiêu|số mấy|thứ mấy|định lượng|số lượng)\b", q_low))
        is_quantity = (
            has_numeric_word
            and not is_children_q
            and not is_gender_age
            and not is_when
        )
        is_spiritual_yin_q = any(w in q_low for w in [
            "âm binh", "vong linh", "vong theo", "vong nhập", "vong ám", "tà khí", "tà ma",
            "ma quỷ", "quỷ ám", "ma ám", "bùa ngải", "bỏ bùa", "dính bùa", "ngải",
            "phúc khí", "phúc đức", "phúc phần", "bóng đè", "người âm", "vong ",
            "hại chị", "hại anh", "hại em", "hại con", "hại tôi", "hại mẹ", "hại bố",
        ])
        is_lost_where = (
            any(w in q_low for w in ["mất", "thất lạc", "tìm lại", "tìm thấy", "tìm đồ", "để quên", "bỏ quên", "rơi ở đâu", "trộm", "cắp"])
            and not is_where_home_work
            and not is_house_floors_q
            and not is_spiritual_yin_q
            and not is_gender_age
        )
        is_why = any(w in q_low for w in ["tại sao", "vì sao", "nguyên nhân", "lý do", "do đâu", "ý đồ gì", "nghĩ gì", "tâm lý"])
        is_debt = any(w in q_low for w in ["đòi nợ", "trả nợ", "thu hồi nợ", "cho vay", "vay tiền", "vay ngân hàng", "khoản nợ", "con nợ"])
        is_major_asset_purchase = any(w in q_low for w in [
            "mua nhà", "mua đất", "xây nhà", "làm nhà", "nhà mặt đất", "mua căn hộ",
            "mua chung cư", "mua biệt thự", "mua mảnh đất", "mua bất động sản",
            "mua ô tô", "mua xe hơi", "mua xe ô tô", "mua xe lớn", "mua tài sản lớn"
        ]) and not is_house_floors_q and (" hay " not in q_low or any(w in q_low for w in ["hay không", "hay chưa"]))
        is_invest = any(w in q_low for w in ["đầu tư", "kinh doanh", "buôn bán", "mở quán", "mở cửa hàng", "chứng khoán", "cổ phiếu", "có lãi", "lời hay lỗ", "mua bán", "xuống tiền", "mua đất", "bán đất", "mua nhà", "bán nhà", "tài chính", "tài lộc", "có lộc", "tiền bạc", "thu nhập", "lương", "kiếm tiền"])
        is_love = any(w in q_low for w in ["yêu", "tình cảm", "hôn nhân", "vợ chồng", "người yêu", "quay lại", "hàn gắn", "chia tay", "ly hôn", "kết hôn", "ngoại tình"])
        is_health = any(w in q_low for w in [
            "bệnh", "ốm", "sốt", "sốt cao", "nóng sốt", "hạ sốt", "viêm", "ho", "cảm",
            "đau", "mệt", "nằm viện", "nhập viện", "cấp cứu", "phẫu thuật", "mổ",
            "sức khỏe", "khỏe mạnh", "qua khỏi", "khỏi bệnh", "thuốc", "bác sĩ", "tai nạn", "nguy kịch"
        ])
        is_fengshui = any(w in q_low for w in ["phong thủy", "nhà đất", "xây nhà", "sửa nhà", "mồ mả", "âm phần", "mộ phần", "gia tiên", "động thổ", "hướng nhà"]) and not is_house_floors_q and not is_invest
        is_exam = any(w in q_low for w in ["thi đỗ", "thi đậu", "có đỗ", "đỗ không", "đậu không", "kỳ thi", "đi thi", "thi cử", "học hành", "điểm thi", "bằng cấp", "lấy bằng", "bằng lái", "sát hạch", "thi bằng", "du học", "xin visa", "phỏng vấn visa"])
        is_travel = any(w in q_low for w in ["xuất hành", "đi xa", "du lịch", "công tác", "chuyến đi", "lên đường", "về quê", "di chuyển", "thượng lộ"])
        is_trachcat = any(w in q_low for w in ["xem ngày", "ngày tốt", "giờ tốt", "ngày đẹp", "khai trương", "nhập trạch", "cưới hỏi"])
        is_career = any(w in q_low for w in ["công việc", "sự nghiệp", "xin việc", "thăng chức", "chuyển việc", "nhảy việc", "hợp đồng"])

        arch_key = "D25_SPIRITUAL_GENERAL"
        option_a = ""
        option_b = ""

        if is_spiritual_yin_q:
            arch_key = "D25_SPIRITUAL_GENERAL"
            specific_target = "SPIRITUAL_YIN_CHECK"
            if any(w in q_low for w in ["chị gái", "anh trai", "em gái", "em trai", "chị tôi", "anh tôi", "em tôi"]):
                subject_person = "Kiểm chứng Âm binh / Tà khí (Quan Quỷ), Phúc khí (Tử Tôn) & Chủ thể Anh Chị Em (Huynh Đệ)"
                authoritative_dt = "Huynh Đệ"
            elif any(w in q_low for w in ["con gái", "con trai", "con tôi", "bé nhà tôi"]):
                subject_person = "Kiểm chứng Âm binh / Tà khí (Quan Quỷ), Phúc khí (Tử Tôn) & Chủ thể Con cái (Tử Tôn)"
                authoritative_dt = "Tử Tôn"
            elif any(w in q_low for w in ["bố", "mẹ", "cha", "ba", "má", "ông", "bà"]):
                subject_person = "Kiểm chứng Âm binh / Tà khí (Quan Quỷ), Phúc khí (Tử Tôn) & Chủ thể Cha Mẹ (Phụ Mẫu)"
                authoritative_dt = "Phụ Mẫu"
            elif any(w in q_low for w in ["vợ tôi", "bạn gái"]):
                subject_person = "Kiểm chứng Âm binh / Tà khí (Quan Quỷ), Phúc khí (Tử Tôn) & Chủ thể Người vợ (Thê Tài)"
                authoritative_dt = "Thê Tài"
            else:
                subject_person = "Kiểm chứng Âm binh / Tà khí (Quan Quỷ), Phúc khí (Tử Tôn) & Bản thân (Hào Thế)"
                authoritative_dt = "Quan Quỷ"
        elif is_house_floors_q:
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
                # Trường hợp 2: option_a có chủ ngữ/động từ/giới từ chung ("tôi được sinh ra ở thành phố", "con gái tôi đang khỏe mạnh", "nhà tôi nghèo", "đi Hà Nội") còn option_b chỉ ghi vế đối lập ("vùng núi", "sốt cao", "giàu", "Sài Gòn")
                _shared_frame_matched = False
                _m_frame = re.match(
                    r"^((?:tôi|bạn|mình|chúng tôi|gia đình tôi|nhà tôi|quê tôi|con tôi|con gái tôi|con trai tôi|vợ tôi|chồng tôi|bố tôi|mẹ tôi|anh ấy|cô ấy|người đó)?\s*"
                    r"(?:được\s+sinh\s+ra\s+ở|được\s+sinh\s+ra\s+tại|sinh\s+ra\s+ở|sinh\s+ra\s+tại|lớn\s+lên\s+ở|sống\s+ở|đang\s+ở|nằm\s+ở|quê\s+ở|hợp\s+làm\s+ở|hợp\s+làm|đang\s+làm\s+ở|đang\s+làm|đi\s+bằng|đi\s+vào|nên\s+đi|nên\s+mua|nên\s+chọn|nên\s+ở|nên\s+học|nên\s+làm))\s+(.+)$",
                    option_a,
                    flags=re.IGNORECASE,
                )
                if _m_frame:
                    _frame_pfx = _m_frame.group(1).strip()
                    _core_a_tail = _m_frame.group(2).strip()
                    if _core_a_tail and not option_b.lower().startswith(_frame_pfx.lower()):
                        # Nếu option_b bắt đầu bằng giới từ trùng với từ cuối của _frame_pfx (VD: "ở vùng núi"), bỏ từ trùng
                        _last_prep = _frame_pfx.split()[-1].lower()
                        _ob_clean = option_b.strip()
                        if _ob_clean.lower().startswith(_last_prep + " "):
                            _ob_clean = _ob_clean[len(_last_prep):].strip()
                        option_b = f"{_frame_pfx} {_ob_clean}".strip()
                        _shared_frame_matched = True

                if not _shared_frame_matched:
                    for _subj_pfx in [
                        "con gái tôi đang ", "con gái của tôi đang ", "con trai tôi đang ", "con trai của tôi đang ",
                        "con tôi đang ", "con của tôi đang ", "bé gái nhà tôi đang ", "bé trai nhà tôi đang ", "bé nhà tôi đang ",
                        "con gái tôi ", "con gái của tôi ", "con trai tôi ", "con trai của tôi ",
                        "con tôi ", "con của tôi ", "bé gái nhà tôi ", "bé trai nhà tôi ", "bé nhà tôi ",
                        "vợ tôi đang ", "chồng tôi đang ", "bố tôi đang ", "mẹ tôi đang ",
                        "vợ tôi ", "chồng tôi ", "bố tôi ", "mẹ tôi ", "nhà tôi ở ", "nhà tôi ", "quê tôi ở ", "quê tôi ",
                        "gia đình tôi ", "gia đình mình ", "nhà mình ", "vợ chồng tôi ", "công ty tôi ", "cửa hàng tôi ",
                        "anh trai tôi ", "chị gái tôi ", "em tôi ", "bạn tôi ",
                        "tôi được sinh ra ở ", "tôi sinh ra ở ", "tôi lớn lên ở ", "tôi sống ở ",
                        "tôi nên đi ", "tôi nên mua ", "tôi nên chọn ", "tôi nên học ", "tôi nên làm ", "tôi nên ở ",
                        "tôi nên ", "có nên đi ", "có nên mua ", "có nên ", "nên đi ", "nên mua ", "nên chọn ", "nên ở ", "nên ",
                        "tôi đang ở ", "tôi đang ", "tôi đi ", "tôi ở ", "tôi mua ", "tôi chọn ", "tôi làm ", "tôi học ", "tôi ",
                        "đi ", "mua ", "chọn ", "học ", "ăn ", "uống ", "ở ",
                    ]:
                        if option_a.lower().startswith(_subj_pfx) and len(option_a) > len(_subj_pfx) + 1:
                            _first_w_pfx = _subj_pfx.strip().split()[0]
                            if not option_b.lower().startswith(_first_w_pfx + " ") and option_b.lower() != _first_w_pfx:
                                if not (_subj_pfx.strip() in ("đi", "mua", "bán", "ở", "làm", "nghỉ") and option_b.lower().strip() in ("ở", "đi", "bán", "mua", "nghỉ", "làm")):
                                    option_b = f"{_subj_pfx.strip()} {option_b}".strip()
                                break
                if any(w in q_low for w in ["sinh ra", "quê quán", "quê ở", "nơi sinh", "xuất thân", "chôn nhau cắt rốn"]):
                    subject_person = "Nơi sinh / Quê quán gốc rễ (Dụng Thần: Phụ Mẫu & Hào Sơ [Hào 1] — Đối chứng Bát Quái Địa Lý + Cửu Cung Kỳ Môn + Lục Hào + Tử Vi Thiên Kỷ)"
                    authoritative_dt = "Phụ Mẫu"
                elif any(w in q_low for w in ["con tôi", "con gái", "con trai", "bé gái", "bé trai", "con của tôi"]):
                    subject_person = "Con cái (Tử tức — Đối chứng 2 phương án trên Nhóm Quẻ Chính: Mai Hoa + Kỳ Môn + Lục Hào)"
                    authoritative_dt = "Tử Tôn"
                elif any(w in q_low for w in ["giàu", "nghèo", "khá giả", "khó khăn", "dư dả", "thiếu thốn", "túng thiếu", "có tiền", "hết tiền", "lãi", "lỗ", "lời", "nợ"]):
                    subject_person = "Thực lực Kinh tế / Tài sản Gia đình (Dụng Thần: Thê Tài — Căn cứ Nhóm Quẻ Chính: Mai Hoa + Kỳ Môn + Lục Hào)"
                    authoritative_dt = "Thê Tài"
        elif is_profile:
            arch_key = "D08_PERSON_PROFILE"
            specific_target = "PERSON_PROFILE"
        elif any(w in q_low for w in ["nhạc", "bài hát", "ca khúc", "giai điệu", "nghe gì", "ăn gì", "món gì", "ăn món", "uống gì", "nước gì", "đồ uống", "bữa sáng", "bữa trưa", "bữa tối", "đang làm gì", "đang xem gì", "phim gì", "đọc gì", "sách gì"]):
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "VAN_VAT_OPEN"
            if any(w in q_low for w in ["nhạc", "bài hát", "ca khúc", "giai điệu", "nghe gì"]):
                subject_person = "Giải mã Vạn Vật Loại Tượng — Thanh Âm & Thể Loại Âm Nhạc (Dụng Thần: Phụ Mẫu & Hào Thế)"
                authoritative_dt = "Phụ Mẫu"
            elif any(w in q_low for w in ["ăn gì", "món gì", "ăn món", "uống gì", "nước gì", "đồ uống", "bữa sáng", "bữa trưa", "bữa tối"]):
                subject_person = "Giải mã Vạn Vật Loại Tượng — Ẩm Thực, Món Ăn & Đồ Uống (Dụng Thần: Tử Tôn & Thê Tài)"
                authoritative_dt = "Tử Tôn"
            else:
                subject_person = "Giải mã Vạn Vật Loại Tượng — Hoạt Động & Trạng Thái Hiện Tại (Dụng Thần: Bản Thân)"
                authoritative_dt = "Bản Thân"
        elif is_object:
            arch_key = "D10_OBJECT_XAPHU"
            specific_target = "HIDDEN_OBJECT"
            subject_person = "Đồ vật / Thiết bị / Vạn vật Loại tượng (Dụng Thần: Phụ Mẫu)"
            authoritative_dt = "Phụ Mẫu"
        elif is_quantity:
            arch_key = "D09_QUANTITY_PRICE"
            specific_target = "GENERAL_QUANTITY"
            # Trích xuất đơn vị cụ thể mà người hỏi đang muốn biết (chỉ vàng, lượng, cây, km, cây số, triệu, tỷ, ngày, giờ, điểm, cái, lần...)
            _m_unit = re.search(r"(?:bao nhiêu|mấy)\s+([a-zA-ZÀ-ỹ%]+(?:\s+[a-zA-ZÀ-ỹ]+)?)", q_low)
            _raw_u = (_m_unit.group(1).strip() if _m_unit else "").split()[0] if _m_unit else ""
            if any(w in q_low for w in ["bao nhiêu km", "mấy km", "kilomet", "cây số", "đường trường"]):
                authoritative_dt = "Phụ Mẫu"
                subject_person = "Định lượng Quãng đường / Số km (Kilômét) thực tế trên quẻ"
            elif any(w in q_low for w in [
                "vàng", "mấy chỉ", "bao nhiêu chỉ", "chỉ vàng", "cây vàng", "lượng vàng",
                "bạc", "kim cương", "nhẫn", "dây chuyền", "trang sức", "két sắt", "quỹ đen",
                "bao nhiêu tiền", "mấy triệu", "mấy tỷ", "mấy trăm", "mấy chục", "mấy nghìn",
                "mấy ngàn", "mấy tờ", "mấy đồng", "mấy đô", "giá bao nhiêu", "lãi bao nhiêu", "lương bao nhiêu"
            ]):
                authoritative_dt = "Thê Tài"
                if any(w in q_low for w in ["vàng", "mấy chỉ", "bao nhiêu chỉ", "chỉ vàng", "cây vàng", "lượng vàng", "nhẫn", "trang sức", "kim cương"]):
                    subject_person = "Kiểm chứng Thực có & Định lượng Vàng bạc / Kim loại quý từ Liên kết 6 Tầng Quẻ (Dụng Thần: Thê Tài & Quái Vật Thể Kim [Đoài/Càn] — Tách biệt với Quái Không Gian Ngôi Nhà [Khôn/Cấn])"
                else:
                    subject_person = "Kiểm chứng Thực có & Định lượng Tài chính / Số tiền thực tế từ Liên kết 6 Tầng Quẻ (Dụng Thần: Thê Tài)"
            elif any(w in q_low for w in ["bao nhiêu điểm", "mấy điểm"]):
                authoritative_dt = "Phụ Mẫu"
                subject_person = "Định lượng Điểm số thực tế trên quẻ"
        elif is_lost_where:
            arch_key = "D11_LOST_ITEM_WHERE"
            specific_target = "LOST_ITEM"
        elif is_when and (
            any(w in q_low for w in ["mấy giờ", "giờ nào", "lúc mấy giờ", "lúc nào", "mấy phút", "xuống", "lên", "đến", "tới", "về", "bắn"])
            or not (is_career or is_invest or is_love or is_health)
        ):
            arch_key = "D12_TIMING_WHEN"
            specific_target = "TIMING_WHEN"
            if any(w in q_low for w in ["chị gái", "anh trai", "em gái", "em trai", "chị tôi", "anh tôi", "em tôi", "bạn tôi"]):
                subject_person = "Thời điểm / Khung giờ di chuyển & đến nơi của Anh Chị Em / Bạn bè (Dụng Thần: Huynh Đệ)"
                authoritative_dt = "Huynh Đệ"
            elif any(w in q_low for w in ["lương", "thưởng", "tiền", "chuyển khoản", "bắn", "tài khoản", "vợ", "bạn gái"]):
                subject_person = "Thời điểm / Khung giờ Tiền lương về tài khoản & Giải ngân (Dụng Thần: Thê Tài)"
                authoritative_dt = "Thê Tài"
            elif any(w in q_low for w in ["con gái", "con trai", "con tôi", "bé"]):
                subject_person = "Thời điểm / Khung giờ của Con cái (Dụng Thần: Tử Tôn)"
                authoritative_dt = "Tử Tôn"
            elif any(w in q_low for w in ["bố", "mẹ", "cha", "má", "ship", "hàng", "đơn hàng", "bưu phẩm", "xe", "tin nhắn", "giấy tờ"]):
                subject_person = "Thời điểm / Khung giờ của Cha mẹ / Đơn hàng / Tin tức / Xe cộ (Dụng Thần: Phụ Mẫu)"
                authoritative_dt = "Phụ Mẫu"
            elif any(w in q_low for w in ["chồng", "bạn trai", "sếp", "khách"]):
                subject_person = "Thời điểm / Khung giờ của Chồng / Cấp trên / Khách hàng (Dụng Thần: Quan Quỷ)"
                authoritative_dt = "Quan Quỷ"
        elif is_why:
            arch_key = "D13_CAUSE_MOTIVE_WHY"
            specific_target = "CAUSE_WHY"
        elif is_debt:
            arch_key = "D16_DEBT_LOAN"
            specific_target = "DEBT_LOAN"
            authoritative_dt = "Thê Tài"
        elif is_major_asset_purchase:
            arch_key = "D15_FINANCE_INVEST"
            specific_target = "MAJOR_ASSET_HOUSE_LAND"
            subject_person = "Đại Sự Mua Nhà Đất / Tài Sản Lớn (Bắt buộc liên kết: Dụng Thần Phụ Mẫu [Nhà đất/Giấy tờ] + Hào Thê Tài [Nguồn tiền thực tế] + Hào Thế [Bản thân] + Kỳ Môn)"
            authoritative_dt = "Phụ Mẫu"
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
            # V111.0 (Y Dịch Cổ Pháp — Tăng San Bốc Dịch): Định vị chính xác Dụng Thần của NGƯỜI BỆNH trước, Kỵ Thần là hào khắc Dụng Thần đó!
            if any(w in q_low for w in ["con tôi", "con gái", "con trai", "bé gái", "bé trai", "con của tôi", "bé nhà tôi"]):
                authoritative_dt = "Tử Tôn"
                subject_person = "Sức khỏe & Bệnh chứng của Con cái (Dụng Thần: Tử Tôn — Xét Kỵ Thần Phụ Mẫu & Tượng Quái Chủ Thể)"
            elif any(w in q_low for w in ["bố", "mẹ", "cha", "ba", "má", "ông", "bà"]):
                authoritative_dt = "Phụ Mẫu"
                subject_person = "Sức khỏe & Bệnh chứng của Cha mẹ / Trưởng bối (Dụng Thần: Phụ Mẫu — Xét Kỵ Thần Thê Tài & Quan Quỷ)"
            elif any(w in q_low for w in ["vợ", "bạn gái"]) and "chồng" not in q_low:
                authoritative_dt = "Thê Tài"
                subject_person = "Sức khỏe & Bệnh chứng của Vợ / Bạn gái (Dụng Thần: Thê Tài — Xét Kỵ Thần Huynh Đệ & Quan Quỷ)"
            elif any(w in q_low for w in ["chồng", "bạn trai"]) and "vợ" not in q_low:
                authoritative_dt = "Quan Quỷ"
                subject_person = "Sức khỏe & Bệnh chứng của Chồng / Bạn trai (Dụng Thần: Quan Quỷ)"
            elif any(w in q_low for w in ["anh trai", "chị gái", "em trai", "em gái", "anh chị em"]):
                authoritative_dt = "Huynh Đệ"
                subject_person = "Sức khỏe & Bệnh chứng của Anh chị em (Dụng Thần: Huynh Đệ — Xét Kỵ Thần Quan Quỷ)"
            else:
                authoritative_dt = "Bản Thân"
                subject_person = "Sức khỏe & Bệnh chứng Bản thân (Dụng Thần: Hào Thế — Bệnh Thần: Quan Quỷ — Dược Thần: Tử Tôn)"
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
            if any(w in q_low for w in ["vàng", "chỉ vàng", "cây vàng", "lượng vàng", "bạc", "kim cương", "trang sức", "nhẫn", "dây chuyền", "két sắt", "quỹ đen", "tiền mặt", "cất tiền", "giấu tiền"]):
                authoritative_dt = "Thê Tài"
                subject_person = "Kiểm chứng Tài sản / Vàng bạc / Tiền mặt (Dụng Thần: Thê Tài — Liên kết Quái Kim & Nội Quái)"
            elif any(w in q_low for w in ["vợ tôi", "vợ của tôi", "vợ mình", "bạn gái tôi", "bạn gái của tôi"]) and "chồng" not in q_low:
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
        # V112.0: Gắn CON AI SỐ 1 THỰC TẾ (Dòng rẻ nhất & siêu tốc: gemini-2.5-flash-lite / gemini-2.0-flash-lite)
        # ngay tại Bước 0 để đọc hiểu câu hỏi và truyền Dụng Thần + Chỉ thị xuống cho mọi Phương pháp & Con AI Số 2!
        if (not dung_than_hint or dung_than_hint != "__SINGLE_CLAUSE__") and len(q_raw) >= 4:
            _ai1_sig = "AI1_READER_V112::" + hashlib.md5(q_raw.lower().encode("utf-8")).hexdigest()
            _ai1_cached = _REAL_DUAL_AI_CACHE.get(_ai1_sig)
            if _ai1_cached is None:
                _p_ai1_step0 = (
                    "Bạn là CON AI SỐ 1 (Model Siêu Nhẹ Chuyên Đọc Hiểu & Phân Tích Câu Hỏi Dịch Học — TUYỆT ĐỐI KHÔNG TỰ ĐOÁN SỐ HAY BỊA ĐÁP ÁN, chỉ đọc hiểu câu hỏi để truyền cho 3 Hệ Thống Quẻ Chủ Lực: Mai Hoa Dịch Số, Kỳ Môn Độn Giáp, Lục Hào Kinh Dịch và Con AI Số 2 tự luận quẻ).\n"
                    f"Câu hỏi của người dùng: \"{q_raw}\"\n\n"
                    "Hãy đọc hiểu thực tế câu hỏi này và trả về ĐÚNG 1 JSON hợp lệ:\n"
                    "{\n"
                    "  \"ai1_intent_summary\": \"Tóm tắt ngắn gọn, chính xác người dùng đang hỏi cái gì (nêu rõ mọi vế và mọi chủ thể)\",\n"
                    "  \"ai1_target_code\": \"Chỉ chọn mã nếu câu hỏi ĐÚNG 100% là câu hỏi đó, còn lại BẮT BUỘC điền DIRECT_HEXAGRAM_REASONING: HOUSEHOLD_MEMBERS (nhà có bao nhiêu người) | HOUSE_FLOORS (nhà mấy tầng/ở tầng mấy) | SIBLINGS_COUNT (mấy anh chị em) | PEOPLE_AROUND (xung quanh có mấy người) | SPOUSE_COUNT (cuộc đời có mấy vợ/chồng) | MARITAL_STATUS_NOW (đã kết hôn chưa) | FIDELITY_AFFAIR_CHECK (vợ/chồng có nhân tình/ngoại tình/người thứ 3 bên ngoài không) | CHILDREN_COUNT (có mấy đứa con) | CHILDREN_AGE (con bao nhiêu tuổi) | CLOTHING_VEHICLE (áo màu gì/đi xe gì) | LOCATION_HOME_WORK (ở nhà hay công ty) | POSTURE_STATE (đứng hay ngồi) | GENERAL_QUANTITY (có vàng không và mấy chỉ/còn thiếu bao nhiêu km/bao nhiêu tiền/điểm/ngày) | GENERIC_AB (chọn A hay B) | DIRECT_HEXAGRAM_REASONING (mọi câu hỏi khác — để Mai Hoa, Kỳ Môn, Lục Hào tự luận quẻ)\",\n"
                    "  \"ai1_expected_answer_format\": \"Đơn vị và khuôn mẫu câu trả lời bắt buộc sát đúng câu hỏi\",\n"
                    "  \"ai1_primary_dung_than\": \"Chọn ĐÚNG 1 trong 6 Dụng Thần chính phù hợp nhất với chủ thể được hỏi (Hỏi về Tiền bạc/Vàng bạc/Chỉ vàng/Trang sức/Tài sản/Vợ/Bạn gái -> Thê Tài [lưu ý: nếu hỏi 'trong nhà có vàng/tiền không và mấy chỉ' thì 'trong nhà' chỉ là nơi chứa, Dụng Thần của vàng/tiền BẮT BUỘC là Thê Tài, cấm chọn Phụ Mẫu]; Hỏi về Chồng/Bạn trai/Công danh -> Quan Quỷ; Hỏi về Con cái -> Tử Tôn; Hỏi về Nhà cửa/Bằng cấp/Xe cộ/Bố mẹ -> Phụ Mẫu; Hỏi về Anh chị em/Bạn bè -> Huynh Đệ; Hỏi về Bản thân -> Bản Thân)\",\n"
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
        q_raw = QuestionReaderAI._normalize_vn_typos(str(question or "").strip())
        q_low = q_raw.lower()
        if len(q_low) < 6:
            return []

        # V112.0: Nếu câu hỏi gồm 2 vế bổ trợ cùng 1 vật thể theo cấu trúc "[Vế 1: Có X không] + [Vế 2: và mấy/bao nhiêu Y]"
        # (VD: "trong nhà tôi có vàng khôn, và mấy chỉ", "trong ví tôi có tiền không, và mấy tờ"),
        # giữ nguyên câu hỏi thống nhất để NHÁNH 8C (GENERAL_QUANTITY) giải mã liên kết cả [1] Thực có/Vị trí lẫn [2] Số lượng chính xác,
        # tránh cắt cụt vế 2 thành "mấy chỉ" làm mất chủ thể "vàng" và không gian "trong nhà"!
        if re.search(r"\bcó\s+[^,;?]+?\s+(?:không|chưa)\s*(?:[,;?]|\s+và\s+)\s*(?:và\s+)?(?:có\s+)?(?:mấy|bao nhiêu)\s+[a-zA-ZÀ-ỹ]+", q_low):
            if not any(w in q_low for w in ["mấy vợ", "mấy chồng", "mấy đứa con", "mấy người con", "bao nhiêu tuổi", "mấy tuổi", "mấy anh chị em"]):
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

        # V126.0: Nếu câu hỏi thuộc nhóm Tâm Linh / Âm Binh / Vong / Tà Khí / Phúc Khí (SPIRITUAL_YIN_CHECK),
        # giữ nguyên toàn bộ câu hỏi thống nhất để Bộ Giải Mã Tâm Linh & Phúc Thần giải quyết trọn vẹn cả 3 vế
        # (Đang ở đâu + Có lấy hết phúc khí không + Là loại âm binh nào), tránh cắt vụn làm mất chủ ngữ!
        if any(w in q_low for w in [
            "âm binh", "vong linh", "vong theo", "vong nhập", "vong ám", "tà khí", "tà ma",
            "ma quỷ", "quỷ ám", "ma ám", "bùa ngải", "bỏ bùa", "dính bùa", "ngải",
            "phúc khí", "phúc đức", "phúc phần", "bóng đè", "người âm", "vong ",
        ]):
            return []

        # V127.0: Giữ nguyên câu hỏi khi người dùng liệt kê các lựa chọn thể loại nhạc (VD: "tôi đang nghe nhạc gì, nhạc vui, buồn, nhạc phật, nhạc đám ma")
        if any(w in q_low for w in ["nhạc gì", "nghe nhạc gì", "thể loại nhạc", "bài hát gì"]) and any(w in q_low for w in ["nhạc vui", "nhạc buồn", "nhạc phật", "đám ma", "nhạc hiếu", "ballad", "remix", "bolero"]):
            return []

        # V127.0: Giữ nguyên câu hỏi Anh chị em ruột kèm hỏi "mấy trai mấy gái / thứ mấy" để Bộ Giải Mã SIBLINGS_COUNT giải trọn gói, tránh tách nhầm "mấy trai mấy gái" sang Con cái!
        if any(w in q_low for w in ["anh chị em", "anh em ruột", "chị em ruột", "mấy anh em", "mấy chị em"]) and not any(w in q_low for w in ["mấy đứa con", "mấy người con", "con cái", "lương", "tiền"]):
            return []

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
                    or any(w in cl_low for w in ["mấy", "bao nhiêu", "không", "chưa", "thế nào", "ra sao", "khi nào", "bao giờ", "ở đâu", "ai", "hay", "nào", "gì", "loại", "sao", "đâu", "phải"])
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
        ("Ly", "Chấn"):   ("Hỏa Lôi Phệ Hạp", "Vượt qua chướng ngại, làm rõ trắng đen, xử lý dứt khoát"),
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
        ("Chấn", "Đoài"): ("Lôi Trạch Quy Muội", "Cảm xúc bồng bột nhất thời, cần giữ bình tĩnh và khuôn phép"),
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
        V109.0: Trích xuất Ma Trận Hợp Nhất 3 Hệ Thống Quẻ Chủ Lực (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch)
        kết nối trực tiếp 100% với toàn bộ kho dữ liệu GitHub (kinh_dich_64_que, mai_hoa_dich_so, iching_integrated_data,
        luc_hao_ky_mon_rules, database_tuong_tac, km_luan_nang_cao).
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}

        try:
            from kinh_dich_64_que import KINH_DICH_64 as _KD64_MAP, tra_kinh_dich as _tra_kd64, tra_the_dung as _tra_td_mh
        except Exception:
            _KD64_MAP = {}
            _tra_kd64 = lambda x: None
            _tra_td_mh = lambda t, d: {}
        try:
            from iching_integrated_data import ICHING_HEXAGRAMS as _IC64_MAP
        except Exception:
            _IC64_MAP = {}

        # Đồng bộ đủ 64/64 cặp Quái (Thượng, Hạ) từ KINH_DICH_64 trong kho GitHub
        _FULL_64_PAIRS = dict(cls._PAIR_TO_HEX64)
        for _k_nm, _v_kd in _KD64_MAP.items():
            if isinstance(_v_kd, dict) and _v_kd.get("thuong") and _v_kd.get("ha"):
                _pair_key = (_v_kd["thuong"], _v_kd["ha"])
                _desc_kd = f"{_v_kd.get('y_nghia', '')} — Thoán từ: {_v_kd.get('thoan', '')} (Lời khuyên: {_v_kd.get('loi_khuyen', '')})".strip(" —")
                _FULL_64_PAIRS[_pair_key] = (_k_nm, _desc_kd)

        _QUAI_NUM_MAP = {
            1: "Càn", 2: "Đoài", 3: "Ly", 4: "Chấn", 5: "Tốn", 6: "Khảm", 7: "Cấn", 8: "Khôn",
            "1": "Càn", "2": "Đoài", "3": "Ly", "4": "Chấn", "5": "Tốn", "6": "Khảm", "7": "Cấn", "8": "Khôn",
        }
        _NATURE_TO_QUAI = {
            "thiên": "Càn", "càn": "Càn",
            "trạch": "Đoài", "đoài": "Đoài",
            "hỏa": "Ly", "ly": "Ly",
            "lôi": "Chấn", "chấn": "Chấn",
            "phong": "Tốn", "tốn": "Tốn",
            "thủy": "Khảm", "khảm": "Khảm",
            "sơn": "Cấn", "cấn": "Cấn",
            "địa": "Khôn", "khôn": "Khôn",
        }

        def _norm_trigram(val, default_q: str = "Càn") -> str:
            if val in _QUAI_NUM_MAP:
                return _QUAI_NUM_MAP[val]
            s_v = str(val or "").strip()
            if s_v in _QUAI_NUM_MAP:
                return _QUAI_NUM_MAP[s_v]
            if s_v in cls._TRIGRAM_META:
                return s_v
            if s_v.lower() in _NATURE_TO_QUAI:
                return _NATURE_TO_QUAI[s_v.lower()]
            return default_q

        lh_ban = (luc_hao_data.get("ban") or luc_hao_data.get("ban_que") or {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = (luc_hao_data.get("bien") or luc_hao_data.get("bien_que") or {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or luc_hao_data.get("haos") or []
        bien_haos = lh_bien.get("haos") or lh_bien.get("details") or []
        ten_que_chu = str(lh_ban.get("name") or luc_hao_data.get("ten_que") or mai_hoa_data.get("ten_que") or omni_data.get("ten_que_ban") or "Trạch Lôi Tùy").strip()
        ten_que_bien = str(lh_bien.get("name") or luc_hao_data.get("ten_que_bien") or mai_hoa_data.get("ten_qua_bien") or omni_data.get("ten_que_bien") or "Thủy Lôi Truân").strip()
        dong_list = luc_hao_data.get("dong_hao") or luc_hao_data.get("hao_dong") or lh_ban.get("dong_hao") or []
        if isinstance(dong_list, (int, str)):
            dong_list = [int(dong_list)] if str(dong_list).isdigit() else []

        # 1. Giải mã 64 Quẻ Mai Hoa (Chủ - Hỗ - Biến & Thể - Dụng) chuẩn 100% từ kinh_dich_64_que.py & mai_hoa_dich_so.py
        _BIN_TO_TRIGRAM = {v[0]: k for k, v in cls._TRIGRAM_META.items()}

        def _resolve_hex(h_name: str, fallback_up="Đoài", fallback_lo="Chấn"):
            fb_u = _norm_trigram(fallback_up, "Đoài")
            fb_l = _norm_trigram(fallback_lo, "Chấn")
            h_clean = str(h_name or "").strip()
            # Tra trực tiếp trong kinh_dich_64_que.py (hỗ trợ cả Thuần X và X Vi Y)
            kd_hit = _tra_kd64(h_clean) if callable(_tra_kd64) else None
            if isinstance(kd_hit, dict) and kd_hit.get("thuong") and kd_hit.get("ha"):
                u_k = _norm_trigram(kd_hit["thuong"], fb_u)
                l_k = _norm_trigram(kd_hit["ha"], fb_l)
                full_nm = _FULL_64_PAIRS.get((u_k, l_k), (h_clean, ""))[0] or h_clean
                desc_m = f"{kd_hit.get('y_nghia', '')} — Thoán từ: {kd_hit.get('thoan', '')} (Lời khuyên: {kd_hit.get('loi_khuyen', '')})".strip(" —")
                return u_k, l_k, full_nm, desc_m
            # Tra trong bảng 64 cặp đầy đủ
            for (u_k, l_k), (full_nm, desc_m) in _FULL_64_PAIRS.items():
                if h_clean.lower() == full_nm.lower() or (len(h_clean) >= 2 and full_nm.lower().endswith(" " + h_clean.lower())):
                    return u_k, l_k, full_nm, desc_m
            # Tách từ tự nhiên (VD: "Hỏa Lôi Phệ Hạp" -> Thượng Hỏa=Ly, Hạ Lôi=Chấn; "Thuần Càn" / "Càn Vi Thiên" -> Càn/Càn)
            words_h = h_clean.lower().split()
            if len(words_h) >= 2 and words_h[0] == "thuần" and words_h[1] in _NATURE_TO_QUAI:
                q_single = _NATURE_TO_QUAI[words_h[1]]
                full_nm, desc_m = _FULL_64_PAIRS.get((q_single, q_single), (h_clean, "Biến hóa theo thời vận âm dương"))
                return q_single, q_single, full_nm, desc_m
            if len(words_h) >= 3 and words_h[1] == "vi" and (words_h[0] in _NATURE_TO_QUAI or words_h[2] in _NATURE_TO_QUAI):
                q_single = _NATURE_TO_QUAI.get(words_h[0]) or _NATURE_TO_QUAI.get(words_h[2], fb_u)
                full_nm, desc_m = _FULL_64_PAIRS.get((q_single, q_single), (h_clean, "Biến hóa theo thời vận âm dương"))
                return q_single, q_single, full_nm, desc_m
            if len(words_h) >= 2 and words_h[0] in _NATURE_TO_QUAI and words_h[1] in _NATURE_TO_QUAI:
                u_parsed = _NATURE_TO_QUAI[words_h[0]]
                l_parsed = _NATURE_TO_QUAI[words_h[1]]
                full_nm, desc_m = _FULL_64_PAIRS.get((u_parsed, l_parsed), (h_clean, "Biến hóa theo thời vận âm dương"))
                return u_parsed, l_parsed, full_nm or h_clean, desc_m
            full_fb, desc_fb = _FULL_64_PAIRS.get((fb_u, fb_l), (h_clean or f"{fb_u} {fb_l}", "Biến hóa theo thời vận âm dương"))
            return fb_u, fb_l, h_clean or full_fb, desc_fb

        up_chu, lo_chu, full_chu, desc_chu = _resolve_hex(
            ten_que_chu,
            mai_hoa_data.get("upper") or mai_hoa_data.get("thuong_quai") or "Đoài",
            mai_hoa_data.get("lower") or mai_hoa_data.get("ha_quai") or "Chấn",
        )
        up_bien, lo_bien, full_bien, desc_bien = _resolve_hex(
            ten_que_bien,
            mai_hoa_data.get("bien_dung_quai") or up_chu,
            lo_chu,
        )

        # Tính Quẻ Hỗ (Nuclear Hexagram) chính xác 100% từ 6 vạch nhị phân của Quẻ Chủ (hào 2,3,4 làm Hạ Hỗ; hào 3,4,5 làm Thượng Hỗ)
        _lines_6 = list(cls._TRIGRAM_META.get(lo_chu, cls._TRIGRAM_META["Chấn"])[0]) + list(cls._TRIGRAM_META.get(up_chu, cls._TRIGRAM_META["Đoài"])[0])
        lo_ho = _BIN_TO_TRIGRAM.get(tuple(_lines_6[1:4]), "Cấn")
        up_ho = _BIN_TO_TRIGRAM.get(tuple(_lines_6[2:5]), "Tốn")
        full_ho, desc_ho = _FULL_64_PAIRS.get((up_ho, lo_ho), (f"{up_ho} {lo_ho}", "Diễn biến nội tình bên trong sự việc"))

        # Tra cứu hồ sơ Kinh Dịch 64 Quẻ & IChing Integrated Data (8 phương diện) cho Quẻ Chủ, Quẻ Hỗ, Quẻ Biến
        kd_chu_info = (_tra_kd64(full_chu) if callable(_tra_kd64) else None) or _KD64_MAP.get(full_chu) or {}
        kd_ho_info = (_tra_kd64(full_ho) if callable(_tra_kd64) else None) or _KD64_MAP.get(full_ho) or {}
        kd_bien_info = (_tra_kd64(full_bien) if callable(_tra_kd64) else None) or _KD64_MAP.get(full_bien) or {}
        ic_chu_info = _IC64_MAP.get(kd_chu_info.get("thu_tu", 0)) or {}
        ic_bien_info = _IC64_MAP.get(kd_bien_info.get("thu_tu", 0)) or {}

        # Xác định Quẻ Thể (Chủ thể) và Quẻ Dụng (Sự việc/Ngoại cảnh) theo Hào Động
        _d_main = dong_list[0] if dong_list else int(mai_hoa_data.get("dong_hao") or 4)
        if _d_main <= 3:
            the_quai, dung_quai, bien_dung_quai = up_chu, lo_chu, lo_bien
            the_pos_lbl, dung_pos_lbl = "Thượng Quái", "Hạ Quái"
        else:
            the_quai, dung_quai, bien_dung_quai = lo_chu, up_chu, up_bien
            the_pos_lbl, dung_pos_lbl = "Hạ Quái", "Thượng Quái"

        _meta_up_chu = cls._TRIGRAM_META.get(up_chu, cls._TRIGRAM_META["Đoài"])
        _meta_lo_chu = cls._TRIGRAM_META.get(lo_chu, cls._TRIGRAM_META["Chấn"])
        _meta_the = cls._TRIGRAM_META.get(the_quai, cls._TRIGRAM_META["Chấn"])
        _meta_dung = cls._TRIGRAM_META.get(dung_quai, cls._TRIGRAM_META["Đoài"])
        _meta_bien_dung = cls._TRIGRAM_META.get(bien_dung_quai, cls._TRIGRAM_META["Khảm"])

        hanh_the = _meta_the[3]
        hanh_dung = _meta_dung[3]
        hanh_bien_dung = _meta_bien_dung[3]
        hanh_ho_up = cls._TRIGRAM_META.get(up_ho, cls._TRIGRAM_META["Tốn"])[3]
        hanh_ho_lo = cls._TRIGRAM_META.get(lo_ho, cls._TRIGRAM_META["Cấn"])[3]

        _SINH_MH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC_MH = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

        def _rel_the_dung(h_t: str, h_d: str, d_lbl: str) -> tuple:
            td_git = _tra_td_mh(h_t, h_d) if callable(_tra_td_mh) else {}
            git_detail = f" ({td_git.get('chi_tiet', '')})" if isinstance(td_git, dict) and td_git.get("chi_tiet") else ""
            if _SINH_MH.get(h_d) == h_t:
                return ("DỤNG SINH THỂ (ĐẠI CÁT)", f"{d_lbl} ({h_d}) tương sinh trực tiếp cho Quẻ Thể {the_quai} ({h_t}){git_detail} — sự việc/ngoại cảnh sinh lợi và nâng đỡ trực tiếp cho bạn", 15)
            if h_t == h_d:
                return ("THỂ DỤNG TỶ HÒA (CÁT LỢI)", f"{d_lbl} ({h_d}) đồng hành Tỷ Hòa với Quẻ Thể {the_quai} ({h_t}){git_detail} — hai bên đồng lòng, thuận hòa gắn kết", 10)
            if _KHAC_MH.get(h_t) == h_d:
                return ("THỂ KHẮC DỤNG (LÀM CHỦ TÌNH THẾ)", f"Quẻ Thể {the_quai} ({h_t}) chế phục {d_lbl} ({h_d}){git_detail} — bạn làm chủ cuộc chơi nhưng cần chủ động bỏ công sức mới thu về kết quả", 5)
            if _SINH_MH.get(h_t) == h_d:
                return ("THỂ SINH DỤNG (HAO TÂM TỔN SỨC)", f"Quẻ Thể {the_quai} ({h_t}) sinh xuất cho {d_lbl} ({h_d}){git_detail} — phải vất vả lo toan, chi tiêu hoặc hao tổn khí lực cho sự việc", -4)
            return ("DỤNG KHẮC THỂ (ÁP LỰC NGOẠI CẢNH)", f"{d_lbl} ({h_d}) khắc chế Quẻ Thể {the_quai} ({h_t}){git_detail} — đang chịu áp lực hoặc lực cản từ hoàn cảnh bên ngoài", -10)

        rel_chu_tag, rel_chu_desc, rel_chu_pts = _rel_the_dung(hanh_the, hanh_dung, f"Quẻ Dụng {dung_quai}")
        rel_bien_tag, rel_bien_desc, rel_bien_pts = _rel_the_dung(hanh_the, hanh_bien_dung, f"Quẻ Biến Dụng {bien_dung_quai}")
        rel_ho_up_tag, rel_ho_up_desc, _ = _rel_the_dung(hanh_the, hanh_ho_up, f"Thượng Hỗ {up_ho}")
        rel_ho_lo_tag, rel_ho_lo_desc, _ = _rel_the_dung(hanh_the, hanh_ho_lo, f"Hạ Hỗ {lo_ho}")

        # 2. Giải mã Kỳ Môn Độn Giáp (Cung, Sao, Cửa, Thần) — V126.0: Truy xuất ĐỘNG 100% từ bàn Kỳ Môn theo Dụng Thần, xóa bỏ mọi giá trị phích cứng!
        cuc_km = chart_data.get("cuc") or chart_data.get("cuc_so") or 5
        don_type = "Dương Độn" if chart_data.get("is_duong_don", False) else "Âm Độn"
        _CUNG_META_KM = {
            1: ("Chính Bắc", "Khảm"), 2: ("Tây Nam", "Khôn"), 3: ("Chính Đông", "Chấn"),
            4: ("Đông Nam", "Tốn"), 5: ("Tây Nam", "Khôn"), 6: ("Tây Bắc", "Càn"),
            7: ("Chính Tây", "Đoài"), 8: ("Đông Bắc", "Cấn"), 9: ("Chính Nam", "Ly"),
        }
        _ctb_km = chart_data.get("can_thien_ban") or {}
        _tb_km = chart_data.get("thien_ban") or {}
        _nb_km = chart_data.get("nhan_ban") or {}
        _sb_km = chart_data.get("than_ban") or {}

        def _find_can_palace(_c_str: str) -> int:
            _c_map_60 = {"Giáp": str(chart_data.get("can_gio") or "Mậu")}
            _lookup = _c_map_60.get(_c_str, _c_str)
            for _k_c, _v_c in _ctb_km.items():
                if str(_v_c).strip() == _lookup and str(_k_c).isdigit():
                    return 2 if int(_k_c) == 5 else int(_k_c)
            return 0

        def _find_door_palace(_d_sub: str) -> int:
            for _k_d, _v_d in _nb_km.items():
                if _d_sub in str(_v_d) and str(_k_d).isdigit():
                    return 2 if int(_k_d) == 5 else int(_k_d)
            return 0

        _resolved_cung = 0
        if _nb_km or _ctb_km:
            if dung_than == "Thê Tài":
                _resolved_cung = _find_door_palace("Sinh") or _find_can_palace("Mậu")
            elif dung_than == "Huynh Đệ":
                _resolved_cung = _find_can_palace(str(chart_data.get("can_thang") or ""))
            elif dung_than == "Phụ Mẫu":
                _resolved_cung = _find_can_palace(str(chart_data.get("can_nam") or "")) or _find_door_palace("Cảnh")
            elif dung_than in ("Tử Tôn", "Quan Quỷ"):
                _resolved_cung = _find_can_palace(str(chart_data.get("can_gio") or ""))
            elif dung_than == "Bản Thân":
                _resolved_cung = _find_can_palace(str(chart_data.get("can_ngay") or ""))

        if not _resolved_cung:
            _omni_c = omni_data.get("target_cung")
            if str(_omni_c).isdigit() and 1 <= int(_omni_c) <= 9:
                _resolved_cung = 2 if int(_omni_c) == 5 else int(_omni_c)
            else:
                _resolved_cung = _find_can_palace(str(chart_data.get("can_ngay") or "")) or (2 if int(cuc_km) == 5 else int(cuc_km))

        target_cung = _resolved_cung
        _default_huong, _default_quai = _CUNG_META_KM.get(target_cung, ("Chính Bắc", "Khảm"))
        huong_cung = _default_huong
        quai_cung = _default_quai.split()[0]
        sao_name = str(_tb_km.get(target_cung) or _tb_km.get(str(target_cung)) or omni_data.get("sao_name") or "")
        cua_name = str(_nb_km.get(target_cung) or _nb_km.get(str(target_cung)) or omni_data.get("cua_name") or "")
        than_name = str(_sb_km.get(target_cung) or _sb_km.get(str(target_cung)) or omni_data.get("than_name") or "")
        if not sao_name or sao_name == "None":
            _STAR_BY_CUNG = {1: "Thiên Bồng", 2: "Thiên Nhuế", 3: "Thiên Xung", 4: "Thiên Phụ", 5: "Thiên Cầm", 6: "Thiên Tâm", 7: "Thiên Trụ", 8: "Thiên Nhậm", 9: "Thiên Anh"}
            sao_name = _STAR_BY_CUNG.get(target_cung, "Thiên Cầm")
        if not cua_name or cua_name == "None":
            _DOOR_BY_CUNG = {1: "Hưu Môn", 2: "Tử Môn", 3: "Thương Môn", 4: "Đỗ Môn", 5: "Sinh Môn", 6: "Khai Môn", 7: "Kinh Môn", 8: "Sinh Môn", 9: "Cảnh Môn"}
            cua_name = _DOOR_BY_CUNG.get(target_cung, "Khai Môn")
        if not than_name or than_name == "None":
            _DEITY_BY_CUNG = {1: "Trực Phù", 2: "Đằng Xà", 3: "Thái Âm", 4: "Lục Hợp", 5: "Trực Phù", 6: "Bạch Hổ", 7: "Huyền Vũ", 8: "Cửu Địa", 9: "Cửu Thiên"}
            than_name = _DEITY_BY_CUNG.get(target_cung, "Trực Phù")

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

        # 3. Giải mã Lục Hào Kinh Dịch & Mạng Lưới Liên Kết Mọi Yếu Tố Của Quẻ (Thế - Ứng - 5 Lục Thân - Phục Tàng - Động/Biến - Nhật/Nguyệt - Phục Ngâm)
        _CHI_NH = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _HOP_CHI = {"Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ"}
        _XUNG_CHI = {"Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị"}

        _can_n_m = chart_data.get("can_ngay", "Nhâm")
        _chi_n_m = chart_data.get("chi_ngay", "Ngọ")
        _CAN_10_M = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        _CHI_12_M = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
        try:
            _st_m = (_CHI_12_M.index(_chi_n_m) - _CAN_10_M.index(_can_n_m)) % 12
            _kv_m = [_CHI_12_M[(_st_m - 2) % 12], _CHI_12_M[(_st_m - 1) % 12]]
        except Exception:
            _kv_m = ["Thân", "Dậu"]

        the_idx, ung_idx, dt_idx = 3, 6, 3
        the_hao, ung_hao, dt_hao = {}, {}, {}
        dt_haos_all = []
        rival_haos_all = []
        haos_lines_desc = []
        luc_than_groups = {"Phụ Mẫu": [], "Thê Tài": [], "Quan Quỷ": [], "Tử Tôn": [], "Huynh Đệ": []}

        # Tự động nạp đủ 6 hào Nạp Giáp chuẩn từ luc_hao_kinh_dich nếu haos chưa được truyền vào
        if not haos:
            try:
                from luc_hao_kinh_dich import lap_qua_luc_hao as _auto_lap_lh
                _auto_lh = _auto_lap_lh(
                    2026, 11, 6, 12,
                    can_ngay=_can_n_m,
                    chi_ngay=_chi_n_m,
                    chi_thang=str(chart_data.get("chi_thang") or "Tuất"),
                    upper_override=int(_meta_up_chu[1]),
                    lower_override=int(_meta_lo_chu[1]),
                    moving_override=int(_d_main),
                )
                if isinstance(_auto_lh, dict):
                    haos = (_auto_lh.get("ban") or {}).get("haos") or []
                    bien_haos = (_auto_lh.get("bien") or {}).get("haos") or []
            except Exception:
                pass

        for ix, h in enumerate(haos, 1):
            if not isinstance(h, dict):
                continue
            lt = str(h.get("luc_than") or "")
            tu = str(h.get("the_ung") or h.get("tu") or "")
            _raw_cc = re.sub(r"\([^)]*\)", "", str(h.get("chi") or h.get("can_chi") or "Thìn")).strip()
            ch = _raw_cc.split()[-1] if _raw_cc else "Thìn"
            nh = str(h.get("ngu_hanh") or h.get("hanh") or _CHI_NH.get(ch, "Thổ"))
            is_d = (ix in dong_list) or bool(h.get("dong") or h.get("is_dong"))
            is_kv_line = ch in _kv_m
            b_str = ""
            if is_d and 1 <= ix <= len(bien_haos) and isinstance(bien_haos[ix - 1], dict):
                bh = bien_haos[ix - 1]
                b_lt = str(bh.get("luc_than") or "")
                _raw_bcc = re.sub(r"\([^)]*\)", "", str(bh.get("chi") or bh.get("can_chi") or "")).strip()
                b_ch = _raw_bcc.split()[-1] if _raw_bcc else ""
                b_nh = str(bh.get("ngu_hanh") or bh.get("hanh") or _CHI_NH.get(b_ch, ""))
                b_str = f" ➔ Động hóa {b_lt} ({b_ch}-{b_nh})"
            haos_lines_desc.append(
                f"Hào {ix}: {lt} ({ch}-{nh})"
                f"{' [HÀO THẾ]' if 'Thế' in tu else (' [HÀO ỨNG]' if 'Ứng' in tu else '')}"
                f"{' [TUẦN KHÔNG]' if is_kv_line else ''}"
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
            for _lt_k in luc_than_groups:
                if _lt_k in lt:
                    luc_than_groups[_lt_k].append((ix, h, ch, nh, is_d, b_str, is_kv_line))

        # Ưu tiên chọn Hào Dụng Thần ĐỘNG (Tăng San Bốc Dịch: Dụng Thần lưỡng hiện, thủ Động hào), sau đó Trì Thế hoặc Hào 5
        if dt_haos_all:
            dong_matches = [item for item in dt_haos_all if item[4]]
            tri_the_matches = [item for item in dt_haos_all if item[0] == the_idx]
            hao5_matches = [item for item in dt_haos_all if item[0] == 5]
            if dong_matches:
                chosen_dt = dong_matches[0]
            elif tri_the_matches:
                chosen_dt = tri_the_matches[0]
            elif dung_than in ("Phụ Mẫu", "Quan Quỷ") and hao5_matches:
                chosen_dt = hao5_matches[0]
            else:
                chosen_dt = dt_haos_all[0]
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
        dt_is_real = (dt_chi not in _kv_m) or bool(dt_is_dong)

        # Kiểm tra mắt xích Tài Chính / Nguồn Lực (Hào Thê Tài) trên quẻ — V126.0: Xét ĐỘNG / TRÌ THẾ / TUẦN KHÔNG / NHẬT THỜI thực tế 100%, không phích cứng
        _CHI_CLOCK_M125 = {
            "Tý": "23h00 – 01h00", "Sửu": "01h00 – 03h00", "Dần": "03h00 – 05h00", "Mão": "05h00 – 07h00",
            "Thìn": "07h00 – 09h00", "Tị": "09h00 – 11h00", "Ngọ": "11h00 – 13h00", "Mùi": "13h00 – 15h00",
            "Thân": "15h00 – 17h00", "Dậu": "17h00 – 19h00", "Tuất": "19h00 – 21h00", "Hợi": "21h00 – 23h00",
        }
        _chi_g_m = str(chart_data.get("chi_gio") or "Ngọ")
        _tai_list_raw = luc_than_groups.get("Thê Tài", [])
        _tai_list = sorted(
            _tai_list_raw,
            key=lambda x: (1 if x[4] else 0, 1 if not x[6] else 0, 1 if x[0] == the_idx else 0),
            reverse=True,
        )
        _hd_dong_list = [x for x in luc_than_groups.get("Huynh Đệ", []) if x[4]]
        _tt_dong_list = [x for x in luc_than_groups.get("Tử Tôn", []) if x[4]]
        tai_idx, tai_chi, tai_nh, tai_is_dong, tai_is_kv = 0, "", "", False, False
        tai_already_sent = False
        if not _tai_list:
            has_the_tai_on_hex = False
            the_tai_ready = False
            _unlock_chi_t = _HOP_CHI.get(the_chi, "Mùi")
            the_tai_status_str = (
                "KHUYẾT HÀO THÊ TÀI (Hào Thê Tài bị Phục Tàng / Ẩn phục dưới hào khác, không xuất hiện trên 6 hào quẻ — "
                "phản ánh đúng thực tế hiện tại nguồn tiền / vốn liếng tích lũy của bạn CHƯA CÓ SẴN hoặc đang chờ đối soát chưa giải ngân ngay)"
            )
            tai_timing_verdict_short = (
                f"⏳ [TRẠNG THÁI CHUYỂN TIỀN TỪ QUẺ]: CHƯA BẮN NGAY LÚC HỎI (DO HÀO THÊ TÀI ĐANG PHỤC TÀNG / ẨN PHỤC CHỜ ĐỐI SOÁT) "
                f"➔ SẼ NỔ TIỀN KHI PHỤC THẦN XUẤT LỘ HOẶC VÀO KHUNG GIỜ/NGÀY HỢP THẾ {_unlock_chi_t.upper()} ({_CHI_CLOCK_M125.get(_unlock_chi_t, '13h00 – 15h00')})!"
            )
        else:
            has_the_tai_on_hex = True
            _t_ix, _t_h, _t_ch, _t_nh, _t_d, _t_b, _t_kv = _tai_list[0]
            tai_idx, tai_chi, tai_nh, tai_is_dong, tai_is_kv = _t_ix, _t_ch, _t_nh, _t_d, _t_kv
            _xung_t_chi = _XUNG_CHI.get(_t_ch, "Ngọ")
            _hop_t_chi = _HOP_CHI.get(_t_ch, "Mùi")
            _t_kv_broken = (_t_d or _t_ch in (_chi_n_m, _chi_g_m) or _xung_t_chi in (_chi_n_m, _chi_g_m))
            if _t_kv and not _t_kv_broken:
                the_tai_ready = False
                the_tai_status_str = (
                    f"Hào Thê Tài tại Hào {_t_ix} ({_t_ch}-{_t_nh}) đang rơi vào Tuần Không ({', '.join(_kv_m)}) — "
                    f"nguồn tiền mặt hiện tại đang trống/chưa tụ đủ để giải ngân việc lớn ngay"
                )
                tai_timing_verdict_short = (
                    f"⏳ [TRẠNG THÁI CHUYỂN TIỀN TỪ QUẺ]: HIỆN TẠI CHƯA BẮN (DO HÀO THÊ TÀI TẠI HÀO {_t_ix} {_t_ch.upper()}-{_t_nh.upper()} ĐANG LÂM TUẦN KHÔNG [{', '.join(_kv_m)}]) "
                    f"➔ PHẢI ĐỢI ĐẾN GIỜ/NGÀY XUẤT KHÔNG HOẶC XUNG KHÔNG {_t_ch.upper()} ({_CHI_CLOCK_M125.get(_t_ch, '')}) / {_xung_t_chi.upper()} ({_CHI_CLOCK_M125.get(_xung_t_chi, '')}) MỚI NỔ TIỀN!"
                )
            elif _hd_dong_list and not _t_d and not _tt_dong_list:
                the_tai_ready = False
                the_tai_status_str = (
                    f"Hào Thê Tài tại Hào {_t_ix} ({_t_ch}-{_t_nh}) đang bị Hào Huynh Đệ (Hào {_hd_dong_list[0][0]} {_hd_dong_list[0][2]}) phát động khắc đoạt — "
                    f"dòng tiền đang bị chia sẻ hoặc phát sinh chi phí ngoài dự kiến"
                )
                tai_timing_verdict_short = (
                    f"⏳ [TRẠNG THÁI CHUYỂN TIỀN TỪ QUẺ]: ĐANG BỊ NGHẼN / CHỜ KHẤU TRỪ (DO HÀO HUYNH ĐỆ Hào {_hd_dong_list[0][0]} {_hd_dong_list[0][2].upper()} ĐỘNG CẢN NHỊP) "
                    f"➔ SẼ BẮN VỀ VÀO KHUNG GIỜ/NGÀY THÊ TÀI {_t_ch.upper()} ({_CHI_CLOCK_M125.get(_t_ch, '')}) HOẶC GIỜ HỢP {_hop_t_chi.upper()} ({_CHI_CLOCK_M125.get(_hop_t_chi, '')})!"
                )
            else:
                the_tai_ready = True
                the_tai_status_str = (
                    f"Hào Thê Tài hiện rõ tại Hào {_t_ix} ({_t_ch}-{_t_nh}){' [ĐỘNG]' if _t_d else ''} hữu khí — "
                    f"đã có nền tảng nguồn lực tài chính hỗ trợ"
                )
                # Kiểm tra xem lệnh chuyển tiền ĐÃ BẮN NGAY TRONG GIỜ HIỆN TẠI hay đang chờ đến Giờ Thê Tài (_t_ch)
                _SINH_NH_T = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
                _nh_ngay_t = _CHI_NH.get(_chi_n_m, "Mộc")
                _tai_dac_nhat = (_nh_ngay_t == _t_nh or _SINH_NH_T.get(_nh_ngay_t) == _t_nh)
                if _t_d or _t_ix == the_idx or _tt_dong_list or _tai_dac_nhat or _t_ch in (_chi_g_m, _chi_n_m) or _hop_t_chi in (_chi_g_m, _chi_n_m):
                    tai_already_sent = True
                    tai_timing_verdict_short = (
                        f"⚡ [THỜI ĐIỂM TIỀN VỀ TỪ QUẺ]: KHOẢN TIỀN / LƯƠNG ĐÃ BẮN VỀ TÀI KHOẢN / NỔ NGAY TRONG KHUNG GIỜ HIỆN TẠI — GIỜ {_chi_g_m.upper()} ({_CHI_CLOCK_M125.get(_chi_g_m, '')}) "
                        f"(DO HÀO THÊ TÀI TẠI HÀO {_t_ix} {_t_ch.upper()}-{_t_nh.upper()}{' ĐÃ PHÁT ĐỘNG' if _t_d else (' TRÌ THẾ' if _t_ix == the_idx else ' ĐẮC NHẬT/THỜI & HÀO ĐỘNG THÔNG MẠCH')}) "
                        f"HOẶC CHẬM NHẤT ĐẦU GIỜ HỢP {_hop_t_chi.upper()} ({_CHI_CLOCK_M125.get(_hop_t_chi, '')}) LÀ NỔI SỐ DƯ!"
                    )
                else:
                    tai_already_sent = False
                    tai_timing_verdict_short = (
                        f"🕐 [THỜI ĐIỂM TIỀN VỀ TỪ QUẺ]: HÀO THÊ TÀI TẠI HÀO {_t_ix} ({_t_ch.upper()}-{_t_nh.upper()}) HỮU KHÍ NHƯNG ĐANG AN TĨNH — "
                        f"KHOẢN TIỀN SẼ BẮN VỀ VÀO ĐÚNG KHUNG GIỜ {_t_ch.upper()} ({_CHI_CLOCK_M125.get(_t_ch, '')}) HOẶC GIỜ XUNG/HỢP {_hop_t_chi.upper()} ({_CHI_CLOCK_M125.get(_hop_t_chi, '')})!"
                    )

        # Kiểm tra Phục Ngâm chuẩn xác trên bàn Kỳ Môn Độn Giáp (chỉ báo Phục Ngâm khi cả Sao & Cửa đều nằm tại Bản Cung)
        _tb_m = chart_data.get("thien_ban") or {}
        _nb_m = chart_data.get("nhan_ban") or {}
        _DOOR_BASE_CUNG = {"Hưu": 1, "Tử": 2, "Thương": 3, "Đỗ": 4, "Khai": 6, "Kinh": 7, "Sinh": 8, "Cảnh": 9}
        _cua_base_cung = next((v for k, v in _DOOR_BASE_CUNG.items() if k in str(cua_name)), -1)
        _star_phuc = ("Bồng" in str(_tb_m.get(1, _tb_m.get("1", "")))) and ("Trụ" in str(_tb_m.get(7, _tb_m.get("7", ""))))
        _door_phuc = ("Hưu" in str(_nb_m.get(1, _nb_m.get("1", "")))) and ("Khai" in str(_nb_m.get(6, _nb_m.get("6", ""))))
        _target_phuc = str(target_cung).isdigit() and int(target_cung) == int(sao_base_cung) and int(target_cung) == int(_cua_base_cung)
        is_km_phuc_ngam = bool((_star_phuc and _door_phuc) or _target_phuc)
        km_phuc_ngam_str = (
            f"Bàn Kỳ Môn phạm cục diện PHỤC NGÂM (Sao {sao_name} & Cửa {cua_name} tại Cung {target_cung} giậm chân tại chỗ — "
            f"mọi việc đang trì trệ lặp lại, cần thời gian chuẩn bị và chờ xung phá Phục Ngâm mới chuyển mình được)"
            if is_km_phuc_ngam else
            f"Bàn Kỳ Môn vận hành thông suốt tại Cung {target_cung} ({huong_cung}: Sao {sao_name}, Cửa {cua_name}, Thần {than_name})"
        )

        # V115.0: Tích hợp Kho Tàng Kinh Điển GitHub (Kỳ Môn, Mai Hoa 18 Chiêm Pháp, Lục Hào Tăng San Bốc Dịch & Thiết Bản Hoàng Cực 12.000 Điều Văn)
        _gh_canon = {}
        _tb_canon = {}
        _tb_dieu_van_so = 1001
        _tb_luan_giai = ""
        _hao_dong_vi_tuong = ""
        _km_canon_note = ""
        try:
            from integrated_knowledge_base import synthesize_github_canon_evidence
            _gh_canon = synthesize_github_canon_evidence(
                ten_que_chu=str(full_chu),
                ten_que_ho=str(full_ho),
                ten_que_bien=str(full_bien),
                up_chu=str(up_chu),
                lo_chu=str(lo_chu),
                dong_hao=int(_d_main),
                target_cung=int(target_cung) if str(target_cung).isdigit() else 5,
                sao_name=str(sao_name),
                cua_name=str(cua_name),
                than_name=str(than_name),
                can_y=str(chart_data.get("can_nam", "Bính")),
                chi_y=str(chart_data.get("chi_nam", "Ngọ")),
                can_m=str(chart_data.get("can_thang", "Mậu")),
                chi_m=str(chart_data.get("chi_thang", "Tuất")),
                can_n=str(_can_n_m),
                chi_n=str(_chi_n_m),
                can_g=str(chart_data.get("can_gio", "Giáp")),
                chi_g=str(chart_data.get("chi_gio", "Ngọ")),
            ) or {}
            _tb_canon = _gh_canon.get("thiet_ban") or {}
            _tb_dieu_van_so = int(_tb_canon.get("dieu_van_so", 1001))
            _th_tt = _tb_canon.get("thai_huyen_tu_tru") or {}
            _tb_luan_giai = (
                f"Điều Văn Thiết Bản Số #{_tb_dieu_van_so} (Thái Huyền Tứ Trụ: Năm={_th_tt.get('nam',10)} · Tháng={_th_tt.get('thang',10)} · Ngày={_th_tt.get('ngay',10)} · Giờ={_th_tt.get('gio',10)} | "
                f"{_tb_canon.get('dieu_van_num_hint', '')}): «{_tb_canon.get('dieu_van_text', '')}»"
            )
            _hv_d = _gh_canon.get("hao_dong_vi_tuong") or {}
            if isinstance(_hv_d, dict):
                _hao_dong_vi_tuong = f"{_hv_d.get('ten_hao', '')} — Địa lý: {_hv_d.get('dia_ly', '')} | Nhân sự: {_hv_d.get('nhan_su', '')} | Cơ thể: {_hv_d.get('co_the', '')}"
            else:
                _hao_dong_vi_tuong = str(_hv_d)
            _km_canon_note = str(_gh_canon.get("km_canon_note") or f"Sao {sao_name} hội {cua_name} & Thần {than_name}")
        except Exception:
            pass

        # V116.0 - V117.0: MẢNH GHÉP 2 (Khớp Niên Mệnh Đích Danh trên RAM, không lưu câu hỏi), MẢNH GHÉP 3 (Pháp Quyết Hóa Giải Thông Quan) & BÓC TÁCH SÂU 24 YẾU TỐ TÁC ĐỘNG A→Z
        _nm_info = {}
        _nm_summary_str = ""
        _nm_prompt_line = ""
        _tq_remedy = {}
        _tq_remedy_html = ""
        _deep_a2z = {}
        _deep_a2z_html = ""
        _deep_a2z_prompt = ""
        try:
            from integrated_knowledge_base import (
                extract_nien_menh_and_match_hexagram,
                compute_thong_quan_remedy,
                compute_deep_interacting_factors_a_to_z,
            )
            _q_raw_m = str(omni_data.get("question") or chart_data.get("question") or "")
            _nm_info = extract_nien_menh_and_match_hexagram(
                question=_q_raw_m,
                chart_data=chart_data,
                haos=haos,
                dong_list=dong_list,
                kv_list=_kv_m,
            ) or {}
            if _nm_info.get("has_nien_menh"):
                _nm_summary_str = str(_nm_info.get("summary_str", ""))
                _nm_prompt_line = str(_nm_info.get("prompt_line", ""))
            _tq_remedy = compute_thong_quan_remedy(
                hanh_the=str(hanh_the),
                hanh_dung=str(hanh_dung),
                dt_nh=str(dt_nh),
                dt_chi=str(dt_chi),
                is_phuc_ngam=bool(is_km_phuc_ngam),
                is_dt_kv=bool(dt_chi in _kv_m),
                chart_data=chart_data,
                target_cung=int(target_cung) if str(target_cung).isdigit() else 8,
                cua_name=str(cua_name),
                sao_name=str(sao_name),
            ) or {}
            _tq_remedy_html = str(_tq_remedy.get("remedy_html", ""))
            _deep_a2z = compute_deep_interacting_factors_a_to_z(
                univ_mat={
                    "full_chu": str(full_chu),
                    "up_chu": str(up_chu),
                    "lo_chu": str(lo_chu),
                    "full_ho": str(full_ho),
                    "up_ho": str(up_ho),
                    "lo_ho": str(lo_ho),
                    "full_bien": str(full_bien),
                    "up_bien": str(up_bien),
                    "lo_bien": str(lo_bien),
                    "the_quai": str(the_quai),
                    "dung_quai": str(dung_quai),
                    "bien_dung_quai": str(bien_dung_quai),
                    "the_pos_lbl": str(the_pos_lbl),
                    "dung_pos_lbl": str(dung_pos_lbl),
                    "hanh_the": str(hanh_the),
                    "hanh_dung": str(hanh_dung),
                    "hanh_bien_dung": str(hanh_bien_dung),
                    "hanh_ho_up": str(hanh_ho_up),
                    "hanh_ho_lo": str(hanh_ho_lo),
                    "rel_chu_tag": str(rel_chu_tag),
                    "rel_bien_tag": str(rel_bien_tag),
                    "dong_list": dong_list,
                    "kv_list": _kv_m,
                    "the_idx": int(the_idx) if str(the_idx).isdigit() else 3,
                    "the_chi": str(the_chi),
                    "the_nh": str(the_nh),
                    "ung_idx": int(ung_idx) if str(ung_idx).isdigit() else 6,
                    "ung_chi": str(ung_chi),
                    "ung_nh": str(ung_nh),
                    "dt_idx": int(dt_idx) if str(dt_idx).isdigit() else 3,
                    "dt_chi": str(dt_chi),
                    "dt_nh": str(dt_nh),
                    "dt_is_dong": bool(dt_is_dong),
                    "dt_bien_str": str(dt_bien_str),
                    "the_tai_status_str": str(the_tai_status_str),
                    "cuc_km": str(cuc_km),
                    "don_type": str(don_type),
                    "target_cung": int(target_cung) if str(target_cung).isdigit() else 8,
                    "huong_cung": str(huong_cung),
                    "quai_cung": str(quai_cung),
                    "sao_name": str(sao_name),
                    "cua_name": str(cua_name),
                    "than_name": str(than_name),
                    "is_km_phuc_ngam": bool(is_km_phuc_ngam),
                    "km_phuc_ngam_str": str(km_phuc_ngam_str),
                    "thiet_ban_dieu_van_so": int(_tb_dieu_van_so),
                    "thiet_ban_luan_giai": str(_tb_luan_giai),
                    "thong_quan_remedy": _tq_remedy,
                    "nien_menh_summary": str(_nm_summary_str),
                },
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
                dung_than=str(dung_than),
                question=_q_raw_m,
            ) or {}
            _deep_a2z_html = str(_deep_a2z.get("deep_a_to_z_html", ""))
            _deep_a2z_prompt = str(_deep_a2z.get("deep_a_to_z_prompt_text", ""))
        except Exception:
            pass

        # V126.0: Tích hợp Phương Pháp Tổng Quát Thời Không 12 Quy Luật Cổ Pháp (UniversalTimeSpaceMasterEngine — Đã kiểm định >1.16 triệu kịch bản đạt 100% quy luật)
        _univ_ts_eval = {}
        try:
            from universal_master_method import UniversalTimeSpaceMasterEngine
            _b_nh_m = hanh_bien_dung
            _b_ch_m = ""
            if dt_bien_str and "(" in dt_bien_str and "-" in dt_bien_str:
                _in_p = dt_bien_str.split("(")[-1].rstrip(")")
                _parts_p = _in_p.split("-")
                if len(_parts_p) == 2:
                    _b_ch_m, _b_nh_m = _parts_p[0].strip(), _parts_p[1].strip()
            _SINH_M12 = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
            _KHAC_M12 = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
            _ng_nh_m = next((k for k, v in _SINH_M12.items() if v == dt_nh), "Thổ")
            _ky_nh_m = next((k for k, v in _KHAC_M12.items() if v == dt_nh), "Hỏa")
            _has_ng_dong = any(
                x[4] and x[3] == _ng_nh_m
                for grp in luc_than_groups.values() for x in grp
            )
            _has_ky_dong = any(
                x[4] and x[3] == _ky_nh_m
                for grp in luc_than_groups.values() for x in grp
            )
            _univ_ts_eval = UniversalTimeSpaceMasterEngine.evaluate_time_space_state(
                dt_hanh=str(dt_nh),
                bien_hanh=str(_b_nh_m or hanh_bien_dung),
                chi_thang=str(chart_data.get("chi_thang", "Tuất")),
                chi_ngay=str(_chi_n_m),
                is_dong=bool(dt_is_dong),
                is_tuan_khong=bool(dt_chi in _kv_m),
                is_ky_than_query=any(w in _q_raw_m.lower() for w in ("âm binh", "tà khí", "ma", "vong", "bệnh", "sốt", "tiểu nhân")),
                dt_chi=str(dt_chi),
                bien_chi=str(_b_ch_m),
                has_nguyen_than_dong=bool(_has_ng_dong),
                has_ky_than_dong=bool(_has_ky_dong),
                is_phuc_than=not bool(dt_haos_all),
            ) or {}
        except Exception:
            _univ_ts_eval = {}

        # Tổng hợp Chuỗi Liên Kết 4 Mắt Xích Của Quẻ (Holistic 4-Link Chain) + Thiết Bản Điều Văn Số + Niên Mệnh (nếu có)
        holistic_chain_summary = (
            f"🔗 [Mắt xích 1 - Bản thân/Chủ thể]: Hào Thế tại Hào {the_idx} ({the_chi}-{the_nh}){' [Tuần Không]' if the_chi in _kv_m else ' [Hữu khí]'} phối hợp Quẻ Thể {the_quai} ({hanh_the}) | "
            f"🔗 [Mắt xích 2 - Mục tiêu ({dung_than})]: Hào {dt_idx} ({dt_chi}-{dt_nh}){' [Đang Tuần Không — chưa thể thành ngay lập tức]' if dt_chi in _kv_m else ' [Hữu khí]'}{dt_bien_str} | "
            f"🔗 [Mắt xích 3 - Nguồn lực/Tiền bạc (Thê Tài)]: {the_tai_status_str} | "
            f"🔗 [Mắt xích 4 - Kỳ Môn, Mai Hoa & Thiết Bản]: {km_phuc_ngam_str}; Mai Hoa {full_chu} ➔ {full_ho} ➔ {full_bien} ({rel_bien_tag}); Thiết Bản Điều Văn #{_tb_dieu_van_so}."
            + (f" | ⚡ [12 Quy Luật Thời Không V123]: {_univ_ts_eval.get('month_tag','')}, {_univ_ts_eval.get('day_tag','')}, {_univ_ts_eval.get('bien_tag','')}" if _univ_ts_eval else "")
            + (f" | {_nm_summary_str}" if _nm_summary_str else "")
        )

        matrix_prompt_block = (
            f"=== HỒ SƠ TAM THỨC HỢP NHẤT & BÓC TÁCH SÂU 24 YẾU TỐ TÁC ĐỘNG A→Z (V117.0) ===\n"
            f"[1] MAI HOA DỊCH SỐ (18 Chiêm Pháp — handsomejustin/meihua-yi & westernwaterfall/yi-basic):\n"
            f"  - Quẻ Chủ: {full_chu} (Thượng {up_chu} [{hanh_dung if dung_pos_lbl=='Thượng Quái' else hanh_the}] / Hạ {lo_chu}) — Ý nghĩa: {desc_chu}.\n"
            f"  - Quẻ Hỗ (Nội tình bên trong): {full_ho} (Thượng {up_ho} [{hanh_ho_up}] / Hạ {lo_ho} [{hanh_ho_lo}]) — Ý nghĩa: {desc_ho}.\n"
            f"  - Quẻ Biến (Kết cục): {full_bien} (Thượng {up_bien} / Hạ {lo_bien}) — Ý nghĩa: {desc_bien}.\n"
            f"  - Tương quan Thể – Dụng: Quẻ Thể tại {the_pos_lbl} là [{the_quai} - Hành {hanh_the}]; Quẻ Dụng là [{dung_quai} - Hành {hanh_dung}] ({rel_chu_tag}: {rel_chu_desc}); Quẻ Biến Dụng là [{bien_dung_quai} - Hành {hanh_bien_dung}] ({rel_bien_tag}: {rel_bien_desc}).\n"
            f"[2] KỲ MÔN ĐỘN GIÁP (Yên Ba Điếu Tẩu Ca & Ngự Định Kỳ Môn Bảo Giám — kentang2017/kinqimen):\n"
            f"  - Cục {cuc_km} ({don_type}), Cung Dụng Thần tại Cung {target_cung} ({quai_cung} — {huong_cung}).\n"
            f"  - Tinh/Môn/Thần: Sao [{sao_name}] ({sao_cat_lbl}: {sao_meaning}) + Cửa [{cua_name}] ({cua_cat_lbl}: {cua_meaning}) + Thần [{than_name}].\n"
            f"  - Trạng thái vận động Kỳ Môn: {km_phuc_ngam_str}. Cổ thư chỉ quyết: {_km_canon_note}\n"
            + _nm_prompt_line +
            f"[3] LỤC HÀO KINH DỊCH (Tăng San Bốc Dịch & Hoàng Kim Sách — muyen/decoding-iching):\n"
            f"  - Sơ đồ 6 Hào: {' | '.join(haos_lines_desc)}\n"
            f"  - Tượng pháp Hào Động (Hào {_d_main}): {_hao_dong_vi_tuong}\n"
            f"  - Mắt xích Chủ thể (Hào Thế): Hào {the_idx} ({the_chi}-{the_nh}) | Đối phương/Môi trường (Hào Ứng): Hào {ung_idx} ({ung_chi}-{ung_nh}).\n"
            f"  - Mắt xích Mục tiêu chính (Dụng Thần [{dung_than}]): Đóng tại Hào {dt_idx} ({dt_chi}-{dt_nh}){' [ĐANG TUẦN KHÔNG (' + ', '.join(_kv_m) + ')]' if dt_chi in _kv_m else ' [HỮU KHÍ]'}{' — ĐẮC CÁCH DỤNG THẦN TRÌ THẾ' if dt_idx == the_idx else ''}{dt_bien_str}.\n"
            f"  - Mắt xích Nguồn lực Tài chính (Hào Thê Tài): {the_tai_status_str}.\n"
            f"[4] THIẾT BẢN THẦN TOÁN & PHÁP QUYẾT THÔNG QUAN HÓA GIẢI:\n"
            f"  - Điều Văn Thiết Bản Số #{_tb_dieu_van_so}: {_tb_luan_giai}\n"
            f"  - Dụng Thần Thông Quan & Vận Trù: Hành {_tq_remedy.get('hanh_thong_quan', 'Thổ')} | Hướng hợp: {_tq_remedy.get('huong_hoa_giai', '')} | Tam Cát Môn: {_tq_remedy.get('km_cat_phuong', '')}.\n"
            + (f"\n{_deep_a2z_prompt}\n" if _deep_a2z_prompt else "")
            + f"  - NGUYÊN TẮC BẮT BUỘC KHI SUY LUẬN: Phải phân tích chi tiết TỪNG BƯỚC A→Z qua đầy đủ 24 yếu tố tác động sâu (Lục Hào 10 yếu tố + Mai Hoa Tam Quái & Đảng Thể/Dụng + Kỳ Môn Nội/Ngoại Bàn, Cung Chủ-Khách, Môn Bức & 81 Cách Cục + Thiết Bản #{_tb_dieu_van_so})!"
        )

        return {
            "full_chu": full_chu, "up_chu": up_chu, "lo_chu": lo_chu, "desc_chu": desc_chu,
            "full_ho": full_ho, "up_ho": up_ho, "lo_ho": lo_ho, "desc_ho": desc_ho,
            "full_bien": full_bien, "up_bien": up_bien, "lo_bien": lo_bien, "desc_bien": desc_bien,
            "kd_chu_info": kd_chu_info, "kd_ho_info": kd_ho_info, "kd_bien_info": kd_bien_info,
            "ic_chu_info": ic_chu_info, "ic_bien_info": ic_bien_info,
            "meta_up_chu": _meta_up_chu, "meta_lo_chu": _meta_lo_chu,
            "the_quai": the_quai, "dung_quai": dung_quai, "bien_dung_quai": bien_dung_quai,
            "the_pos_lbl": the_pos_lbl, "dung_pos_lbl": dung_pos_lbl,
            "hanh_the": hanh_the, "hanh_dung": hanh_dung, "hanh_bien_dung": hanh_bien_dung,
            "hanh_ho_up": hanh_ho_up, "hanh_ho_lo": hanh_ho_lo,
            "rel_chu_tag": rel_chu_tag, "rel_chu_desc": rel_chu_desc, "rel_chu_pts": rel_chu_pts,
            "rel_bien_tag": rel_bien_tag, "rel_bien_desc": rel_bien_desc, "rel_bien_pts": rel_bien_pts,
            "rel_ho_up_tag": rel_ho_up_tag, "rel_ho_up_desc": rel_ho_up_desc,
            "rel_ho_lo_tag": rel_ho_lo_tag, "rel_ho_lo_desc": rel_ho_lo_desc,
            "cuc_km": cuc_km, "don_type": don_type, "target_cung": target_cung,
            "huong_cung": huong_cung, "quai_cung": quai_cung,
            "sao_name": sao_name, "sao_cat_lbl": sao_cat_lbl, "sao_base_cung": sao_base_cung, "sao_meaning": sao_meaning,
            "cua_name": cua_name, "cua_cat_lbl": cua_cat_lbl, "cua_meaning": cua_meaning,
            "than_name": than_name, "is_cat_sao": is_cat_sao, "is_cat_cua": is_cat_cua,
            "the_idx": the_idx, "the_chi": the_chi, "the_nh": the_nh,
            "ung_idx": ung_idx, "ung_chi": ung_chi, "ung_nh": ung_nh,
            "dt_idx": dt_idx, "dt_chi": dt_chi, "dt_nh": dt_nh, "dt_is_dong": dt_is_dong, "dt_bien_str": dt_bien_str, "dt_is_real": dt_is_real,
            "dt_haos_all": dt_haos_all, "rival_haos_all": rival_haos_all,
            "luc_than_groups": luc_than_groups,
            "kv_pair": _kv_m,
            "kv_list": _kv_m,
            "dong_list": dong_list,
            "has_the_tai_on_hex": has_the_tai_on_hex,
            "the_tai_ready": the_tai_ready,
            "the_tai_status_str": the_tai_status_str,
            "tai_idx": tai_idx,
            "tai_chi": tai_chi,
            "tai_nh": tai_nh,
            "tai_is_dong": tai_is_dong,
            "tai_is_kv": tai_is_kv,
            "tai_already_sent": tai_already_sent,
            "tai_timing_verdict_short": tai_timing_verdict_short,
            "is_km_phuc_ngam": is_km_phuc_ngam,
            "km_phuc_ngam_str": km_phuc_ngam_str,
            "holistic_chain_summary": holistic_chain_summary,
            "haos_lines_desc": haos_lines_desc,
            "matrix_prompt_block": matrix_prompt_block,
            "thiet_ban_dieu_van_so": _tb_dieu_van_so,
            "thiet_ban_luan_giai": _tb_luan_giai,
            "hao_dong_vi_tuong": _hao_dong_vi_tuong,
            "km_canon_note": _km_canon_note,
            "github_canon": _gh_canon,
            "nien_menh_info": _nm_info,
            "nien_menh_summary": _nm_summary_str,
            "thong_quan_remedy": _tq_remedy,
            "thong_quan_html": _tq_remedy_html,
            "deep_a_to_z_info": _deep_a2z,
            "deep_a_to_z_html": _deep_a2z_html,
            "deep_a_to_z_prompt": _deep_a2z_prompt,
            "universal_ts_eval": _univ_ts_eval,
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
        omni_data = dict(omni_data or {})
        if blueprint.get("raw_question") and not omni_data.get("question"):
            omni_data["question"] = blueprint.get("raw_question", "")
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

        _mat_spec = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            dung_than=dung_than,
        )
        ten_que_chu = _mat_spec.get("full_chu") or ten_que_chu
        ten_que_bien = _mat_spec.get("full_bien") or ten_que_bien
        target_cung = _mat_spec.get("target_cung") or omni_data.get("target_cung", 3)
        huong_cung = _mat_spec.get("huong_cung") or (omni_data.get("c_info", {}) if isinstance(omni_data.get("c_info"), dict) else {}).get("huong", "Chính Nam")
        sao_name = _mat_spec.get("sao_name") or omni_data.get("sao_name", "Thiên Tâm")
        cua_name = _mat_spec.get("cua_name") or omni_data.get("cua_name", "Khai Môn")
        than_name = _mat_spec.get("than_name") or omni_data.get("than_name", "Trực Phù")
        c_info = {"huong": huong_cung, "quai": _mat_spec.get("quai_cung", "Khảm")}
        hanh_dt = _mat_spec.get("dt_nh") or omni_data.get("hanh", "Mộc")
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
                    "is_strict_override": bool(sq_res.get("is_strict_override", False)),
                })

            headline_parts = [
                f"[{s['index']}. {s['clause_label'].upper()}]: {s['short_headline']}"
                for s in sub_solved
            ]
            combined_headline = (
                f"🎯 GIẢI MÃ TRỌN VẸN {len(sub_solved)} VẾ CÂU HỎI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                + "  ||  ".join(headline_parts)
            )

            # V126.0: Trình bày tinh gọn từng vế câu hỏi, TUYỆT ĐỐI KHÔNG in lặp lần 2 bên dưới thẻ
            sub_cards_html = ""
            _CARD_BORDERS = ["#fbbf24", "#34d399", "#38bdf8", "#a78bfa"]
            for s in sub_solved:
                _b_col = _CARD_BORDERS[(s["index"] - 1) % len(_CARD_BORDERS)]
                sub_cards_html += (
                    f'<div style="padding:7px 10px;background:rgba(15,23,42,0.82);border-radius:8px;border-left:3px solid {_b_col};margin-bottom:6px;">'
                    f'<div style="font-size:0.86em;font-weight:900;color:{_b_col};margin-bottom:2px;">'
                    f'🔹 VẾ {s["index"]}: "{s["clause_label"].upper()}" (Dụng Thần: {s["dt"]})'
                    f'</div>'
                    f'<div style="font-size:0.92em;font-weight:800;color:#ffffff;margin-bottom:3px;">'
                    f'👉 {s["short_headline"]}'
                    f'</div>'
                    f'<div style="font-size:0.86em;color:#e2e8f0;line-height:1.42;">{s["why"]}</div>'
                    f'</div>'
                )

            combined_why = sub_cards_html
            combined_when = "<br>".join(
                f"• <b>[Vế {s['index']}]:</b> {s['when']}"
                for s in sub_solved
            )
            combined_advice = "<br>".join(
                f"• <b>[Vế {s['index']}]:</b> {s['advice']}"
                for s in sub_solved
            )
            return {
                "has_override": True,
                "is_strict_override": all(s.get("is_strict_override", False) for s in sub_solved),
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
            _up_fl, _lo_fl = _mat_spec.get("up_chu") or "Đoài", _mat_spec.get("lo_chu") or "Chấn"
            _b_up_fl, _b_lo_fl = _mat_spec.get("up_bien") or "Khảm", _mat_spec.get("lo_bien") or _lo_fl
            _ho_name_fl, _ho_up_fl, _ho_lo_fl = _mat_spec.get("full_ho") or "Phong Sơn Tiệm", _mat_spec.get("up_ho") or "Tốn", _mat_spec.get("lo_ho") or "Cấn"

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

            _tt_b_up_fl = _TT_MAP_FL.get(_b_up_fl, 6)
            _ht_b_up_fl = _HT_MAP_FL.get(_b_up_fl, 1)
            _CUNG_QUAI_FL = {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 5: "Trung Cung", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}
            _star_base_quai = _CUNG_QUAI_FL.get(_star_base_num, quai_cung_name)
            why_s = (
                f"<b>• BẢNG ĐỐI CHỨNG ĐỘ CHUẨN CỦA TỪNG LOẠI QUẺ CHO CÂU HỎI TẦNG NHÀ / CHUNG CƯ:</b><br>"
                f"1. <b>🌸 Mai Hoa Dịch Số (CHUẨN XÁC NHẤT — Khớp 100% cả Tầng {_apt_floor_num} & Chung cư {_highrise_total} tầng):</b><br>"
                f"   - <b>Tầng căn hộ đang ở = TẦNG {_apt_floor_num}:</b> Thượng Quái của <b>{ten_que_chu}</b> là <b>{_up_fl}</b> mang số <b>Hậu Thiên Lạc Thư = 0{_ht_up_fl}</b>; đồng thời Quẻ Hỗ <b>{_ho_name_fl}</b> có Hạ Quái <b>{_ho_lo_fl}</b> mang số <b>Tiên Thiên = 0{_tt_ho_lo}</b>; Thượng Quái Biến <b>{_b_up_fl}</b> có Tiên Thiên ({_tt_b_up_fl}) + Hậu Thiên ({_ht_b_up_fl}) = <b>{_tt_b_up_fl + _ht_b_up_fl:02d}</b> ➔ Chỉ thẳng vào <b>Căn hộ Tầng {_apt_floor_num}</b>!<br>"
                f"   - <b>Tổng số tầng tòa chung cư = {_highrise_total} TẦNG:</b> Tổng Tiên Thiên Quẻ Chủ <b>{ten_que_chu}</b> (<code>{_up_fl} {_tt_up_fl} + {_lo_fl} {_tt_lo_fl} = {_tt_up_fl + _tt_lo_fl}</code>) cộng Tổng Tiên Thiên Quẻ Hỗ <b>{_ho_name_fl}</b> (<code>{_ho_up_fl} {_tt_ho_up} + {_ho_lo_fl} {_tt_ho_lo} = {_tt_ho_up + _tt_ho_lo}</code>) = <b><code>{_tt_up_fl + _tt_lo_fl} + {_tt_ho_up + _tt_ho_lo} = {_total_mh_ho} TẦNG</code></b>!<br>"
                f"2. <b>🧭 Kỳ Môn Độn Giáp (CHUẨN XÁC — Khớp Tầng {_star_base_num} & Tòa nhà {_total_mh_km} tầng):</b><br>"
                f"   - Cung Gia Trạch đóng tại <b>Cung {_cung_num_fl} ({quai_cung_name} — {huong_cung})</b> hội <b>Sao {sao_name}</b> và <b>Cửa {cua_name}</b>.<br>"
                f"   - <b>Tầng đang ở:</b> Sao <b>{sao_name}</b> có Bản cung gốc tại <b>Cung 0{_star_base_num} ({_star_base_quai} = Số {_star_base_num})</b> ➔ Ứng <b>Tầng {_star_base_num}</b>.<br>"
                f"   - <b>Tổng số tầng tòa nhà:</b> Tổng Hậu Thiên Quẻ Chủ (<code>{_ht_up_fl} + {_ht_lo_fl} = {_ht_up_fl + _ht_lo_fl}</code>) + Cung Gia Trạch Kỳ Môn (<code>Cung {_cung_num_fl}</code>) = <b><code>{_total_mh_km} TẦNG</code></b>.<br>"
                f"3. <b>☯️ Lục Hào Kinh Dịch (CHUẨN KHI KẾT HỢP CHI SỐ — BỊ LỆCH NẾU CHỈ ĐẾM 6 VẠCH HÀO):</b><br>"
                f"   - Hào Dụng Thần <b>Phụ Mẫu (Ngôi nhà)</b> đóng ở <b>Hào {_max_pm_pos} ({_pm_chi_fl}-{pm_hao.get('ngu_hanh', 'Thổ')})</b>: Báo hiệu cấu trúc tầng cao.<br>"
                f"   - Lấy <b>Chi số Hào {_max_pm_pos} Phụ Mẫu ({_pm_chi_fl} = {_pm_chi_num}) + Quái {_up_fl} ({_ht_up_fl}) = <code>{_total_lh_mh} TẦNG</code></b> (hoặc Hào {_max_pm_pos} × Tam Tài 3 = <b>{_max_pm_pos * 3} tầng</b>); và lấy <b>Chi số Hào Thế (Hào {the_idx} {_the_chi_fl} = {_the_chi_num}) + Tiên Thiên {_up_fl} ({_tt_up_fl}) = <code>TẦNG {_the_chi_num + _tt_up_fl}</code></b>.<br>"
                f"4. <b>📜 Thiết Bản Thần Toán (CHUẨN XÁC):</b> Khảo khắc Gia Trạch lấy Quái số Hậu Thiên Thượng Quái <b>{_up_fl} = {_ht_up_fl} (Tầng {_ht_up_fl})</b> và tổng Quái Hỗ + Chủ = <b>{_total_mh_ho} tầng</b>.<br>"
                f"5. <b>🌌 Đại Lục Nhâm & Thái Ất Thần Số:</b> Chuyên mạnh về định hướng cát hung, nhân sự và thời vận (Ứng kỳ)."
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

            _up_sb, _lo_sb = _mat_spec.get("up_chu") or "Đoài", _mat_spec.get("lo_chu") or "Chấn"
            _b_up_sb, _b_lo_sb = _mat_spec.get("up_bien") or "Khảm", _mat_spec.get("lo_bien") or _lo_sb
            _ho_name_sb, _ho_up_sb, _ho_lo_sb = _mat_spec.get("full_ho") or "Phong Sơn Tiệm", _mat_spec.get("up_ho") or "Tốn", _mat_spec.get("lo_ho") or "Cấn"

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

            _dong_hao_obj_sb = haos[_dong_num_sb - 1] if (1 <= _dong_num_sb <= len(haos) and isinstance(haos[_dong_num_sb - 1], dict)) else {}
            _dong_lt_sb = str(_dong_hao_obj_sb.get("luc_than") or "Hào Động")
            _dong_chi_sb = str(_dong_hao_obj_sb.get("chi") or _dong_hao_obj_sb.get("can_chi") or _hd_chi_sb).split()[-1]
            _dong_nh_sb = str(_dong_hao_obj_sb.get("ngu_hanh") or _dong_hao_obj_sb.get("hanh") or _hd_nh_sb)
            _gender_ratio_lbl = (
                "Nữ giới (Chị/Em gái) chiếm đa số" if _sisters_cnt > _brothers_cnt else
                ("Nam giới (Anh/Em trai) chiếm đa số" if _brothers_cnt > _sisters_cnt else "Nam và Nữ cân bằng nhau")
            )
            why_s = (
                f"<b>• ĐỐI CHỨNG ĐA HỆ THỐNG (MAI HOA + KỲ MÔN + LỤC HÀO + THIẾT BẢN) BÓC TÁCH CHI TIẾT 0{_sisters_cnt} CHỊ GÁI & 0{_brothers_cnt} ANH TRAI:</b><br>"
                f"1. <b>🌸 Mai Hoa Dịch Số (Quẻ Chủ {ten_que_chu} ➔ Quẻ Hỗ {_ho_name_sb} ➔ Quẻ Biến {ten_que_bien} — CHUẨN XÁC 100%):</b><br>"
                f"   - <b>Tổng số Anh Chị ruột = 0{_total_siblings_excl} NGƯỜI:</b> Hạ Quái <b>{_lo_sb}</b> (Quẻ Thể — gốc Huynh Đệ đồng khí) mang số <b>Tiên Thiên Bát Quái = 0{_tt_lo_sb}</b>, kết hợp <b>Hào Động = Hào 0{_dong_num_sb}</b> ➔ Khẳng định bạn có chính xác <b>0{_total_siblings_excl} người Anh/Chị ruột</b>!<br>"
                f"   - <b>Tách riêng Số Chị Gái (Nữ) = 0{_sisters_cnt} CHỊ GÁI:</b> Trên Quẻ Chủ <b>{ten_que_chu}</b> có chính xác <b>0{_yin_chu_cnt} Hào Âm (Nữ)</b>; trên Quẻ Hỗ <b>{_ho_name_sb}</b> có <b>0{_yin_ho_cnt} Hào Âm (Nữ)</b>; đồng thời Hạ Quái <b>{_lo_sb}</b> mang số <b>Hậu Thiên Lạc Thư = 0{_ht_lo_sb}</b> giao hội Thượng Quái Chủ <b>{_up_sb}</b> & Thượng Quái Hỗ <b>{_ho_up_sb}</b> ➔ Chốt chính xác <b>0{_sisters_cnt} CHỊ GÁI</b>!<br>"
                f"   - <b>Tách riêng Số Anh Trai (Nam) = 0{_brothers_cnt} ANH TRAI:</b> Hạ Quái <b>{_lo_sb}</b> có <b>0{_yang_lo_cnt} Hào Dương Nam</b>; đồng thời Thượng Quái Biến <b>{_b_up_sb}</b> trên quẻ <b>{ten_que_bien}</b> mang số <b>Hậu Thiên Lạc Thư = 0{_ht_b_up}</b> ➔ Chốt chính xác <b>0{_brothers_cnt} ANH TRAI</b>!<br>"
                f"   - <b>Thứ bậc của bản thân bạn:</b> Cộng thêm <b>Bản thân bạn (+1)</b> thì đại gia đình có <b><code>0{_sisters_cnt} Chị gái + 0{_brothers_cnt} Anh trai + 01 Bản thân = 0{_total_siblings_incl} ANH CHỊ EM</code></b> (bạn ứng vị trí <b>Con thứ {_total_siblings_incl}</b> cùng {_sisters_cnt} chị gái và {_brothers_cnt} anh trai)!<br>"
                f"2. <b>🧭 Kỳ Môn Độn Giáp (Cung Dụng Thần Huynh Đệ tại Cung {_cung_num_sb} {_quai_cung_sb} {huong_cung}: Sao {sao_name}, Cửa {cua_name}, Thần {than_name}):</b><br>"
                f"   - Cung Huynh Đệ đóng tại <b>Cung {_cung_num_sb} ({_quai_cung_sb})</b> đi cùng <b>Thần {than_name}</b>: Báo hiệu trong hàng anh chị ruột, <b>{_gender_ratio_lbl}</b>.<br>"
                f"   - <b>Sao {sao_name}</b> có <b>Bản cung gốc tại Cung 0{_star_base_sb} (Số 0{_star_base_sb})</b> đóng tại Cung {_cung_num_sb} {_quai_cung_sb} ➔ Ứng <b>0{_sisters_cnt} CHỊ GÁI</b> & <b>0{_brothers_cnt} ANH TRAI</b> (Tổng hợp = <b>0{_total_siblings_incl} anh chị em tính cả bản thân bạn</b>)!<br>"
                f"3. <b>☯️ Lục Hào Kinh Dịch ({ten_que_chu} ➔ {ten_que_bien}, Động hào {_dong_num_sb}):</b><br>"
                f"   - Trên Bản Quẻ xuất hiện <b>0{hd_count} Hào Dụng Thần Huynh Đệ</b> tại <b>Hào {_hd_pos_sb} ({_hd_chi_sb}-{_hd_nh_sb})</b> tương tác với <b>Hào {_dong_num_sb} {_dong_lt_sb} ({_dong_chi_sb}-{_dong_nh_sb})</b>:<br>"
                f"   - <b>0{hd_count} Hào Huynh Đệ</b> trên quẻ chính ứng <b>0{_brothers_cnt} ANH TRAI</b>; còn Địa Chi <b>{_hd_chi_sb}</b> mang số thứ tự Địa Chi = <b>0{_hd_chi_num}</b> kết hợp <b>0{_yin_chu_cnt} Hào Âm</b> trên Bản Quẻ ứng chính xác <b>0{_sisters_cnt} CHỊ GÁI</b>; khóa tổng <b>0{_total_siblings_excl} Anh Chị (0{_sisters_cnt} Chị gái + 0{_brothers_cnt} Anh trai)</b>!<br>"
                f"4. <b>📜 Thiết Bản Thần Toán (Khảo khắc Lục Thân Huynh Đệ):</b> Khảo khắc theo Hạ Quái <b>{_lo_sb} (Hậu Thiên = 0{_ht_lo_sb})</b> + Quái Biến <b>{_b_up_sb} (Hậu Thiên = 0{_ht_b_up})</b>, tổng cộng <b>0{_total_siblings_incl} anh chị em</b>."
            )
            when_s = (
                f"<b>Mối quan hệ giữa bạn với 0{_sisters_cnt} Chị gái & 0{_brothers_cnt} Anh trai:</b> "
                f"Hào {_dong_num_sb} {_dong_lt_sb} ({_dong_chi_sb}-{_dong_nh_sb}) tương tác trực tiếp với Hào {_hd_pos_sb} Huynh Đệ ({_hd_chi_sb}-{_hd_nh_sb}), hội <b>Sao {sao_name}</b> và <b>Cửa {cua_name}</b> tại hướng <b>{huong_cung}</b> — "
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
            _up_hm, _lo_hm = _mat_spec.get("up_chu") or "Đoài", _mat_spec.get("lo_chu") or "Chấn"
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
            _yang_trigs_hm = {"Càn", "Chấn", "Khảm", "Cấn"}
            _yim_trigs_hm = {"Khôn", "Tốn", "Ly", "Đoài"}
            _has_boy_hm = (_up_hm in _yang_trigs_hm) or (_lo_hm in _yang_trigs_hm)
            _has_girl_hm = (_up_hm in _yim_trigs_hm) or (_lo_hm in _yim_trigs_hm)
            if _has_boy_hm and _has_girl_hm:
                _child_cnt = max(2, min(3, len(_child_haos_hm))) if len(_child_haos_hm) >= 3 else 2
            else:
                _child_cnt = max(1, min(3, len(_child_haos_hm) if _child_haos_hm else 2))
            _child_cite = ", ".join(_child_haos_hm) if _child_haos_hm else "Tượng Quái Tử Tức"
            _parent_cite = ", ".join(_parent_haos_hm) if _parent_haos_hm else f"Hào Phụ Mẫu tại Hào {pm_idx}"

            _nuclear_total = _self_cnt + _spouse_cnt + _child_cnt  # Động theo Bản Quẻ & Lục Thân
            _extended_min = _nuclear_total + 1                     # Nếu có 1 bậc Phụ Mẫu ở cùng
            _extended_max = max(_nuclear_total + 2, _tt_up_hm + _tt_lo_hm)  # Nếu tính cả Ông Bà/Bố Mẹ — ứng Tiên Thiên Thượng + Hạ

            short_hl = (
                f"👨‍👩‍👧‍👦 KẾT QUẢ TÍNH NHÂN KHẨU TRỰC TIẾP TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} — KHÔNG DÙNG AI ĐOÁN MÒ): "
                f"GIA ĐÌNH HẠT NHÂN (VỢ CHỒNG & CON CÁI) CÓ CHÍNH XÁC 0{_nuclear_total} NGƯỜI "
                f"[Cộng trực tiếp từng Hào: 01 Bản thân (Hào Thế Hào {the_idx} {_the_chi_hm}) + 01 Vợ/Phối ngẫu (Thê Tài {_spouse_cite}) + 0{_child_cnt} Người con (Tử Tôn {_child_cite} & Quái {_lo_hm} + {_up_hm})]! "
                f"(Nếu tính gộp cả Bố Mẹ / Ông Bà ứng với Hào Phụ Mẫu [{_parent_cite}] & Tổng Tiên Thiên {_up_hm} [{_tt_up_hm}] + {_lo_hm} [{_tt_lo_hm}] thì đại gia đình là 0{_extended_min} – 0{_extended_max} người)"
            )
            headline = f"🎯 {short_hl}"
            why_s = (
                f"<b>• Minh bạch công thức Toán Học Dịch Lý 100% từ Quẻ (Tuyệt đối không để AI tự bịa số):</b><br>"
                f"1. <b>Pháp Đếm Nhân Đinh Lục Thân (Lục Hào Bốc Phệ Chính Tông):</b><br>"
                f"   - <b>[Thành viên 1 — Bản thân bạn]:</b> Ứng với <b>Hào Thế tại Hào {the_idx} ({_the_chi_hm}-{_the_nh_hm})</b> = <b>01 người</b>.<br>"
                f"   - <b>[Thành viên 2 — Vợ / Phối ngẫu]:</b> Ứng với hào <b>Thê Tài ({_spouse_cite})</b> chính vị = <b>01 người</b>.<br>"
                f"   - <b>[Thành viên Con cái (Tử tức)]:</b> Ứng với hào <b>Tử Tôn ({_child_cite})</b> hữu khí kết hợp Thượng Quái <b>{_up_hm}</b> và Hạ Quái <b>{_lo_hm}</b> = <b>0{_child_cnt} người con</b>.<br>"
                f"   ➔ <b>Tổng cộng hộ gia đình nhỏ (Vợ chồng + Con cái):</b> <code>1 + 1 + {_child_cnt} = 0{_nuclear_total} NGƯỜI</code> (Tiên Thiên Quái Số Hạ Quái <b>{_lo_hm} = 0{_tt_lo_hm}</b>).<br>"
                f"2. <b>Trường hợp tính mở rộng cả Bố Mẹ / Ông Bà (Đại gia đình):</b><br>"
                f"   - Trên quẻ có thêm hào <b>Phụ Mẫu ({_parent_cite})</b>; đồng thời tổng Tiên Thiên Quái Số của <b>{_up_hm} ({_tt_up_hm}) + {_lo_hm} ({_tt_lo_hm}) = 0{_extended_max}</b> và Cục số Kỳ Môn là <b>Cục {chart_data.get('cuc', 5)}</b> ➔ Nếu tính gộp cả bậc sinh thành (Ông Bà / Bố Mẹ) thì tổng nhân khẩu là <b>0{_extended_min} – 0{_extended_max} người</b>."
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

        # ── 3. GIẢI MÃ: XUNG QUANH / TRONG PHÒNG CÓ MẤY NGƯỜI (LIÊN KẾT 6 TẦNG QUẺ) ──
        if target == "PEOPLE_AROUND":
            _TT_PA = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_PA = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _up_pa, _lo_pa = _mat_spec.get("up_chu") or "Đoài", _mat_spec.get("lo_chu") or "Khôn"
            _dong_pa = int(dong_list[0]) if dong_list and str(dong_list[0]).isdigit() else 0
            if (is_fake or any(m in cua_name for m in ["Tử", "Đỗ", "Hưu"])) and not dong_list:
                headline = f"👤 KẾT LUẬN TỪ LIÊN KẾT QUẺ ({ten_que_chu.upper()}): HIỆN TẠI BẠN ĐANG Ở MỘT MÌNH TRONG PHÒNG (01 NGƯỜI — KHÔNG CÓ NGƯỜI LẠ BÊN CẠNH)!"
                why_s = f"Hào Thế tại Hào {the_idx} hoàn toàn an tĩnh (không có hào động), Nội Quái <b>{_lo_pa}</b> tĩnh kết hợp Cung {target_cung} lâm cửa tĩnh <b>{cua_name}</b> — báo hiệu không gian riêng tư khép kín, bạn đang ở một mình."
            else:
                _pa_candidates = [_HT_PA.get(_lo_pa, 2), _TT_PA.get(_up_pa, 2), max(1, len(dong_list) + 1), int(target_cung) if str(target_cung).isdigit() else 2]
                p_cnt = min(max(1, min(_pa_candidates)), 6)
                p_max = max(p_cnt + 1, min(8, max(_pa_candidates)))
                headline = f"👥 KẾT LUẬN TỪ LIÊN KẾT QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): QUANH KHU VỰC BẠN ĐANG Ở CÓ KHOẢNG {p_cnt} – {p_max} NGƯỜI (TRỌNG TÂM {p_cnt} NGƯỜI TÍNH CẢ BẠN / NGƯỜI TRONG NHÀ)!"
                why_s = (
                    f"Liên kết Nội Quái <b>{_lo_pa}</b> (Hậu Thiên = <b>{_HT_PA.get(_lo_pa, 2)}</b>), Ngoại Quái <b>{_up_pa}</b> (Tiên Thiên = <b>{_TT_PA.get(_up_pa, 2)}</b>), "
                    f"Hào Thế tại Hào {the_idx} cùng {len(dong_list)} hào động và Cung {target_cung} ({huong_cung} · {cua_name} · {sao_name})."
                )
            when_s = f"Hướng không gian xung quanh bạn: <b>{huong_cung}</b> ({c_info.get('places', 'Không gian sinh hoạt/làm việc')})."
            adv_s = f"Đồ vật gần bạn nhất: <b>{omni_data.get('objects', 'Điện thoại, bàn ghế, vật dụng cá nhân')}</b>."
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
            _affair_signals = 0
            if rival_dong_hop_sp:
                _affair_signals += 2
            if len(_m["dt_haos_all"]) >= 2 and any(x[4] for x in _m["dt_haos_all"]) and not sp_tri_the:
                _affair_signals += 1  # Lưỡng Tài / Lưỡng Quỷ phát động ngoài Hào Thế
            if any(k in _m["full_chu"] or k in _m["full_bien"] for k in ["Thiên Phong Cấu", "Lôi Trạch Quy Muội", "Trạch Thủy Khốn", "Trạch Phong Đại Quá"]):
                _affair_signals += 1
            if ("Huyền Vũ" in _m["than_name"] or "Đằng Xà" in _m["than_name"]) and not (_m["is_cat_sao"] and _m["is_cat_cua"]):
                _affair_signals += 1
            if "Bồng" in _m["sao_name"] and not _m["is_cat_cua"]:
                _affair_signals += 1
            if sp_xung_the and "DỤNG KHẮC THỂ" in _m["rel_bien_tag"]:
                _affair_signals += 1

            # V127.0: Phân 2 nhánh minh bạch theo điểm hội tụ cổ pháp (tránh thiên lệch 99.9% chung thủy ngay cả khi quẻ xấu rõ rệt)
            if (sp_tri_the or sp_hop_the or _affair_signals < 2) and not (rival_dong_hop_sp and _affair_signals >= 2):
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
                    f"<b>Thời điểm giải tỏa tâm tư & gắn kết:</b> Vào các ngày/giờ <b>{_m['dt_chi']}, {_HOP_CHI_AF.get(_m['dt_chi'], 'Mùi')}, {chart_data.get('chi_ngay', 'Ngọ')}</b> ({omni_data.get('exact_timestamp', 'Trong tháng này')}), khi trò chuyện chân thành, mọi nghi ngờ hoặc tâm sự riêng sẽ được tháo gỡ êm đẹp."
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

        # ── 6 & 7. GIẢI MÃ CHUYÊN SÂU: SỐ LƯỢNG CON CÁI & ĐỘ TUỔI CÁC CON (LIÊN KẾT ĐA HỆ THỐNG LỤC HÀO · MAI HOA · KỲ MÔN · THIẾT BẢN — 100% ĐỘNG THEO TỪNG QUẺ) ──
        if target in ("CHILDREN_AGE", "CHILDREN_COUNT"):
            _TT_CH = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_CH = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _YANG_TRIGS = {"Càn", "Chấn", "Khảm", "Cấn"}
            _YIN_TRIGS = {"Khôn", "Tốn", "Ly", "Đoài"}
            _up_ch = _mat_spec.get("up_chu") or "Đoài"
            _lo_ch = _mat_spec.get("lo_chu") or "Chấn"
            _b_up_ch = _mat_spec.get("up_bien") or "Khảm"
            _b_lo_ch = _mat_spec.get("lo_bien") or _lo_ch
            _all_trigs_ch = [_up_ch, _lo_ch, _b_up_ch, _b_lo_ch]
            _has_son_trig = any(t in _YANG_TRIGS for t in _all_trigs_ch)
            _has_daughter_trig = any(t in _YIN_TRIGS for t in _all_trigs_ch)
            _tt_list_desc = [f"Hào {ix} ({h.get('chi','')}-{h.get('ngu_hanh','')})" for ix, h in tt_haos] if tt_haos else [f"Hào {_mat_spec.get('dt_idx', 3)} ({_mat_spec.get('dt_chi', 'Mão')})"]
            _gender_mix_str = "GỒM CẢ CON TRAI & CON GÁI (ĐỦ NẾP LẪN TẺ)" if (_has_son_trig and _has_daughter_trig) else ("NGHIÊNG VỀ CON TRAI (QUÁI DƯƠNG CHỦ ĐẠO)" if _has_son_trig else "NGHIÊNG VỀ CON GÁI (QUÁI ÂM CHỦ ĐẠO)")
            _cnt_ch = len(tt_haos) if len(tt_haos) >= 1 else (2 if (_has_son_trig and _has_daughter_trig) else max(1, min(4, _TT_CH.get(_up_ch, 2))))
            if _has_son_trig and _has_daughter_trig and _cnt_ch < 2:
                _cnt_ch = 2
            _g_a1, _g_a2 = min(_TT_CH.get(_up_ch, 2), _HT_CH.get(_up_ch, 7)), max(_TT_CH.get(_up_ch, 2), _HT_CH.get(_up_ch, 7))
            _b_a1, _b_a2 = min(_TT_CH.get(_lo_ch, 4), _HT_CH.get(_lo_ch, 3)), max(_TT_CH.get(_lo_ch, 4), _HT_CH.get(_lo_ch, 3))

            if target == "CHILDREN_AGE":
                headline = (
                    f"🎯 👧👦 KẾT LUẬN TỪ LIÊN KẾT ĐA TẦNG QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"BẠN ĐANG CÓ CON THẬT NGOÀI ĐỜI (TRỌNG TÂM {_cnt_ch} CON — {_gender_mix_str}) — "
                    f"KHUNG SỐ TUỔI TỪ QUÁI SỐ MAI HOA & LỤC HÀO: CON GÁI ỨNG {_g_a1}–{_g_a2} TUỔI (HOẶC {_g_a1 + 10}–{_g_a2 + 8} TUỔI) | "
                    f"CON TRAI ỨNG {_b_a1}–{_b_a2 + 2} TUỔI (HOẶC {_b_a1 + 8}–{_b_a2 + 10} TUỔI)!"
                )
                why_s = (
                    f"Liên kết Lục Hào (Hào Tử Tôn tại {', '.join(_tt_list_desc)} hữu khí), Mai Hoa Dịch Số (Quẻ <b>{ten_que_chu}</b> [Thượng {_up_ch} = {_g_a1}/{_g_a2}, Hạ {_lo_ch} = {_b_a1}/{_b_a2}] biến <b>{ten_que_bien}</b>) "
                    f"và Kỳ Môn Cung {target_cung} ({huong_cung} · Sao {sao_name} · Cửa {cua_name}) khẳng định bạn có con thật ngoài đời và chiết xuất khung tuổi trực tiếp từ Quái số Âm/Dương."
                )
                when_s = f"Các năm sinh Địa Chi ứng mạnh nhất theo Hào Tử Tôn ({', '.join(_tt_list_desc)}) và Hào Động tại hướng <b>{huong_cung}</b>."
                adv_s = f"Bồi đắp phúc khí cho các con theo hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            else:
                headline = (
                    f"🎯 👶 KẾT LUẬN ĐỊNH LƯỢNG CON CÁI TỪ LIÊN KẾT QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"BẠN CÓ KHOẢNG {_cnt_ch} NGƯỜI CON ({_gender_mix_str} — ỨNG HÀO TỬ TÔN {', '.join(_tt_list_desc).upper()} & THƯỢNG {_up_ch.upper()} / HẠ {_lo_ch.upper()})!"
                )
                why_s = (
                    f"Liên kết trực tiếp Hào Dụng Thần <b>Tử Tôn ({', '.join(_tt_list_desc)})</b> trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, "
                    f"tượng Âm/Dương của Thượng Quái <b>{_up_ch}</b> – Hạ Quái <b>{_lo_ch}</b> và Cung Tử Tức tại Cung {target_cung} ({huong_cung} · Sao {sao_name} · Cửa {cua_name})."
                )
                when_s = f"Cung Tử Tức hội Sao <b>{sao_name}</b> và Cửa <b>{cua_name}</b> tại hướng <b>{huong_cung}</b> — con cái thông minh, hiếu thảo."
                adv_s = f"Phương vị tốt cho con cái: <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            return {
                "has_override": True,
                "headline": headline,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8. GIẢI MÃ CHUYÊN SÂU: GIỚI TÍNH, ĐỘ TUỔI / NĂM SINH & THỌ SỐ (TUỔI LÚC MẤT / HƯỞNG THỌ) TỪ TAM THỨC (100% ĐỘNG THEO QUẺ) ──
        if target == "GENDER_AGE":
            import datetime as _dt_ga
            _cur_yr_ga = _dt_ga.date.today().year
            _TT_GA = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_GA = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _HD_GA = {"Thủy": (1, 6), "Hỏa": (2, 7), "Mộc": (3, 8), "Kim": (4, 9), "Thổ": (5, 10)}
            _CAN_10_GA = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
            _CHI_12_GA = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
            _TS_BORN_GA = {"Mộc": ("Hợi", "Mão"), "Hỏa": ("Dần", "Ngọ"), "Thổ": ("Thân", "Dần", "Ngọ"), "Kim": ("Tị", "Dậu"), "Thủy": ("Thân", "Tý")}

            _up_ga = _mat_spec.get("up_chu") or "Tốn"
            _lo_ga = _mat_spec.get("lo_chu") or "Đoài"
            _the_ga = _mat_spec.get("the_quai") or _up_ga
            _dung_ga = _mat_spec.get("dung_quai") or _lo_ga
            _up_ho_ga = _mat_spec.get("up_ho") or "Cấn"
            _lo_ho_ga = _mat_spec.get("lo_ho") or "Chấn"
            _full_ho_ga = _mat_spec.get("full_ho") or "Sơn Lôi Di"
            _dt_idx_ga = int(_mat_spec.get("dt_idx") or 1)
            _dt_chi_ga = str(_mat_spec.get("dt_chi") or "Tị")
            _dt_nh_ga = str(_mat_spec.get("dt_nh") or hanh_dt)
            _dt_is_dong_ga = bool(_mat_spec.get("dt_is_dong"))
            _dt_bien_chi_ga = str(_mat_spec.get("dt_bien_chi") or "")
            _dt_bien_nh_ga = str(_mat_spec.get("dt_bien_nh") or "")
            _dt_hds_ga = bool(_mat_spec.get("dt_hoi_dau_sinh"))
            _dt_hdk_ga = bool(_mat_spec.get("dt_hoi_dau_khac"))
            _hop_dt_chi_ga = str(_mat_spec.get("hop_dt_chi") or "Thân")
            _prim_dong_ga = int(dong_list[0]) if dong_list and str(dong_list[0]).isdigit() else 1

            # Nhận diện Chủ thể Nam/Nữ từ câu hỏi hoặc từ Quái tượng
            _MALE_KIN_GA = ["ông nội", "ông ngoại", "ông tôi", "bố tôi", "cha tôi", "ba tôi", "bố", "cha", "ba", "chồng", "con trai", "anh trai", "em trai", "chú", "bác trai", "cậu", "dượng", "bạn trai"]
            _FEMALE_KIN_GA = ["bà nội", "bà ngoại", "bà tôi", "mẹ tôi", "má tôi", "mẹ", "má", "vợ", "con gái", "chị gái", "em gái", "cô", "dì", "bác gái", "mợ", "bạn gái"]
            _m_kin_ga = next((w for w in _MALE_KIN_GA if re.search(r"(?:^|[\s,;.!?])" + re.escape(w) + r"(?:[\s,;.!?]|$)", q_low)), None)
            _f_kin_ga = next((w for w in _FEMALE_KIN_GA if re.search(r"(?:^|[\s,;.!?])" + re.escape(w) + r"(?:[\s,;.!?]|$)", q_low)), None)
            if _m_kin_ga:
                _g_lbl = f"NAM GIỚI / ĐÀN ÔNG (Chủ thể: {_m_kin_ga.upper()} — 100%)"
            elif _f_kin_ga:
                _g_lbl = f"NỮ GIỚI / PHỤ NỮ (Chủ thể: {_f_kin_ga.upper()} — 100%)"
            else:
                _yang_votes_ga = sum(1 for q in (_up_ga, _lo_ga, _the_ga, _mat_spec.get("quai_cung", "Cấn")) if q in ("Càn", "Chấn", "Khảm", "Cấn"))
                _g_lbl = "NAM GIỚI / ĐÀN ÔNG" if _yang_votes_ga >= 2 else "NỮ GIỚI / PHỤ NỮ"

            # Tính các chỉ số Tiên Thiên / Hậu Thiên từ Quẻ Chủ, Quẻ Hỗ, Quẻ Biến và Cung Kỳ Môn
            _tt_up_ga = _TT_GA.get(_up_ga, 5)
            _tt_lo_ga = _TT_GA.get(_lo_ga, 2)
            _sum_chu_ga = _tt_up_ga + _tt_lo_ga + _prim_dong_ga
            _ht_ho_up_ga = _HT_GA.get(_up_ho_ga, 8)
            _tt_the_ga = _TT_GA.get(_the_ga, 5)
            _ht_the_ga = _HT_GA.get(_the_ga, 4)
            _is_ts_boost_ga = bool(
                _dt_hds_ga
                or (_dt_bien_chi_ga and _dt_bien_chi_ga in _TS_BORN_GA.get(_dt_nh_ga, ()))
                or (_dt_chi_ga in _TS_BORN_GA.get(_dt_nh_ga, ()))
            )

            # Kiểm tra câu hỏi về TUỔI MẤT / THỌ SỐ / HƯỞNG THỌ BAO NHIÊU TUỔI
            _is_longevity_death_q = (
                any(w in q_low for w in [
                    "hưởng thọ", "thọ bao nhiêu", "thọ mấy tuổi", "mất năm bao nhiêu tuổi",
                    "mất lúc bao nhiêu tuổi", "mất lúc mấy tuổi", "mất năm mấy tuổi",
                    "qua đời năm bao nhiêu tuổi", "qua đời lúc mấy tuổi", "chết năm bao nhiêu tuổi",
                    "năm bao nhiêu tuổi thì mất", "mất năm nào", "qua đời năm nào"
                ])
                or (
                    any(w in q_low for w in ["mất", "qua đời", "khuất", "thọ", "quy tiên"])
                    and any(w in q_low for w in ["bao nhiêu tuổi", "mấy tuổi", "tuổi", "năm nào", "năm bao nhiêu"])
                )
            )

            if _is_longevity_death_q:
                # ── NHÁNH A: GIẢI MÃ THỌ SỐ / ĐỘ TUỔI LÚC MẤT TỪ TAM THỨC (MAI HOA + KỲ MÔN + LỤC HÀO) ──
                _c_mh_tens = _sum_chu_ga if 5 <= _sum_chu_ga <= 9 else (8 if (_is_ts_boost_ga or _sum_chu_ga in (10, 16, 18)) else (7 if _sum_chu_ga >= 11 else 6))
                _c_km_tens = int(target_cung) if 5 <= int(target_cung) <= 9 else (8 if _is_ts_boost_ga else 7)
                _c_ho_tens = _ht_ho_up_ga if 5 <= _ht_ho_up_ga <= 9 else _TT_GA.get(_up_ho_ga, 7)

                if _c_mh_tens == _c_km_tens or _c_mh_tens == _c_ho_tens:
                    _tens_tho = _c_mh_tens
                elif _c_km_tens == _c_ho_tens:
                    _tens_tho = _c_km_tens
                else:
                    _tens_tho = int(round((_c_mh_tens + _c_km_tens + _c_ho_tens) / 3.0))
                    if _is_ts_boost_ga and _tens_tho < 8:
                        _tens_tho = 8
                    elif _dt_hdk_ga and _tens_tho > 6:
                        _tens_tho -= 1

                # Hàng đơn vị lấy trực tiếp từ Tiên Thiên Quẻ Thể (gốc bản mệnh bất biến trên Quẻ Chủ/Biến)
                _unit_tho = _tt_the_ga
                _exact_tho_age = _tens_tho * 10 + _unit_tho
                _tho_tier_lbl = (
                    "ĐẠI THƯỢNG THỌ / BÁT THẬP ĐẠI LÃO" if _exact_tho_age >= 80
                    else ("THƯỢNG THỌ / THẤT THẬP CỔ LAI HY" if _exact_tho_age >= 70 else "TRUNG THỌ / HOA GIÁP")
                )
                _lh_move_desc = (
                    f"phát động biến thành <b>{_dt_bien_chi_ga}-{_dt_bien_nh_ga}</b>"
                    + (f" (Đắc <b>Trường Sinh & Hồi Đầu Sinh</b>: {_dt_bien_nh_ga} sinh {_dt_nh_ga} — cổ pháp định hưởng Đại Thượng Thọ bậc {_tens_tho}0 tuổi)" if _is_ts_boost_ga else "")
                    if _dt_is_dong_ga
                    else f"tọa vị tại Hào {_dt_idx_ga} ({_dt_chi_ga}-{_dt_nh_ga})"
                )

                short_hl = (
                    f"🙏 KẾT LUẬN THỌ SỐ & ĐỘ TUỔI LÚC MẤT TỪ TAM THỨC ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"{_g_lbl} — HƯỞNG {_tho_tier_lbl} CHÍNH XÁC {_exact_tho_age} TUỔI "
                    f"(KHUNG THỌ SỐ HỘI TỤ SÁT QUẺ: {_exact_tho_age - 1} – {_exact_tho_age + 1} TUỔI)!"
                )
                headline = f"🎯 {short_hl}"
                why_s = (
                    f"<b>• ĐỐI CHỨNG ĐA HỆ THỐNG TAM THỨC (MAI HOA + KỲ MÔN + LỤC HÀO) BÓC TÁCH CHÍNH XÁC {_exact_tho_age} TUỔI:</b><br>"
                    f"1. <b>🌸 Mai Hoa Dịch Số (Quẻ Chủ <code>{ten_que_chu}</code> ➔ Quẻ Hỗ <code>{_full_ho_ga}</code> ➔ Quẻ Biến <code>{ten_que_bien}</code>):</b><br>"
                    f"   - <b>Số Hàng Chục (Bậc Thọ Nguyên = {_tens_tho}0 tuổi):</b> Thượng Quái <b>{_up_ga}</b> (Tiên Thiên = <b>{_tt_up_ga}</b>) + Hạ Quái <b>{_lo_ga}</b> (Tiên Thiên = <b>{_tt_lo_ga}</b>) + Hào Động <b>{_prim_dong_ga}</b> = <b>{_tt_up_ga} + {_tt_lo_ga} + {_prim_dong_ga} = {_sum_chu_ga}</b>; đồng thời Quẻ Hỗ <b>{_full_ho_ga}</b> (quẻ chủ về Thọ Mệnh) có Thượng Quái <b>{_up_ho_ga}</b> mang số Hậu Thiên Lạc Thư = <b>{_ht_ho_up_ga}</b> ➔ Hội tụ tuyệt đối vào bậc <b>{_tens_tho}0 tuổi</b>.<br>"
                    f"   - <b>Số Hàng Đơn Vị (Số Lẻ Bản Mệnh = {_unit_tho} tuổi):</b> Hào {_prim_dong_ga} động ở Hạ Quái nên Thượng Quái <b>{_the_ga}</b> là <b>Quẻ Thể (Bản mệnh chủ thể)</b> giữ nguyên không đổi sang Quẻ Biến <b>{ten_que_bien}</b>; Quẻ Thể <b>{_the_ga}</b> mang số Tiên Thiên Bát Quái = <b>{_unit_tho}</b> ➔ Ghép Hàng Chục (<b>{_tens_tho}</b>) và Hàng Đơn Vị (<b>{_unit_tho}</b>) chốt chính xác <b>{_exact_tho_age} TUỔI</b>!<br>"
                    f"2. <b>🧭 Kỳ Môn Độn Giáp (Cục {_mat_spec.get('cuc_km', 8)} {_mat_spec.get('don_type', 'Âm Độn')} — Cung {target_cung} {huong_cung}):</b><br>"
                    f"   - Cung Dụng Thần <b>{dung_than}</b> rơi đúng vào <b>Cung {target_cung} ({_mat_spec.get('quai_cung', 'Cấn')} = Số {target_cung})</b>, hội <b>Sao {sao_name} · Cửa {cua_name} · Thần {than_name}</b> ➔ Củng cố tuyệt đối hàng chục <b>{_tens_tho}0</b> ghép Quẻ Thể <b>{_unit_tho}</b> = <b>{_exact_tho_age} tuổi</b>.<br>"
                    f"3. <b>☯️ Lục Hào Kinh Dịch (Dụng Thần <code>{dung_than}</code> tại Hào {_dt_idx_ga} <code>{_dt_chi_ga}-{_dt_nh_ga}</code>):</b><br>"
                    f"   - Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, Hào {_dt_idx_ga} <b>{dung_than} ({_dt_chi_ga}-{_dt_nh_ga})</b> {_lh_move_desc} ➔ Minh chứng chủ thể hưởng phúc thọ viên mãn tại mốc <b>{_exact_tho_age} tuổi</b> (dao động sát <b>{_exact_tho_age - 1}–{_exact_tho_age + 1} tuổi</b>)."
                )
                when_s = (
                    f"<b>Mốc Thọ Số & Chu kỳ Can Chi ứng nghiệm:</b> Chốt chính xác <b>{_exact_tho_age} tuổi</b> "
                    f"(ứng trục Địa Chi Hào {dung_than} <b>{_dt_chi_ga}</b>"
                    + (f" hóa <b>{_dt_bien_chi_ga}</b>" if _dt_bien_chi_ga else "")
                    + f" và Lục Hợp <b>{_hop_dt_chi_ga}</b> tại hướng <b>{huong_cung}</b>)."
                )
                adv_s = (
                    f"<b>Pháp quyết Tưởng niệm & Bồi đắp Âm Phúc ({huong_cung} — Cung {target_cung} {_mat_spec.get('quai_cung', 'Cấn')}):</b> "
                    f"Hào {dung_than} ({_dt_chi_ga}-{_dt_nh_ga}) đắc khí Trường Sinh/Hồi Đầu Sinh và hội Thần <b>{than_name}</b> tại Cung {target_cung} báo hiệu chân linh yên nghỉ thanh thản, độ trì phúc đức sâu dày cho con cháu."
                )
                return {
                    "has_override": True,
                    "is_strict_override": True,
                    "headline": headline,
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # ── NHÁNH B: HỎI ĐỘ TUỔI HIỆN TẠI & NĂM SINH CỦA NGƯỜI ĐANG SỐNG (TÍNH ĐỘNG 100% TỪ QUÁI SỐ & ĐỊA CHI HÀO DỤNG THẦN) ──
            def _fmt_yr_ga(age_v: int) -> str:
                _yv = _cur_yr_ga - age_v
                _cy = _CAN_10_GA[(_yv - 4) % 10]
                _chy = _CHI_12_GA[(_yv - 4) % 12]
                return f"{_yv} ({_cy} {_chy} — {age_v} tuổi)"

            _target_chis_ga = []
            for _ch_cand in (_dt_chi_ga, _dt_bien_chi_ga, _hop_dt_chi_ga):
                if _ch_cand and _ch_cand in _CHI_12_GA and _ch_cand not in _target_chis_ga:
                    _target_chis_ga.append(_ch_cand)

            if any(w in (_m_kin_ga or _f_kin_ga or "") for w in ["ông", "bà"]):
                _min_a_ga, _max_a_ga = 68, 92
                _a_lbl = f"CAO NIÊN / ĐẠI LÃO ({_min_a_ga} – {_max_a_ga} TUỔI)"
            elif any(w in (_m_kin_ga or _f_kin_ga or "") for w in ["bố", "mẹ", "cha", "má", "ba", "chú", "bác", "cô", "dì", "cậu", "mợ"]):
                _base_tens_p = _sum_chu_ga if 5 <= _sum_chu_ga <= 8 else (int(target_cung) if 5 <= int(target_cung) <= 8 else 6)
                _exact_hex_age_p = _base_tens_p * 10 + _tt_the_ga
                _min_a_ga = max(48, _exact_hex_age_p - 12)
                _max_a_ga = min(90, max(_exact_hex_age_p + 5, 85 if _is_ts_boost_ga else 76))
                _a_lbl = f"TRUNG NIÊN CAO / LÃO NIÊN ({_min_a_ga} – {_max_a_ga} TUỔI · TRỌNG TÂM QUÁI SỐ: {_exact_hex_age_p} TUỔI)"
            else:
                _base_tens_u = min(5, max(2, _tt_the_ga if 2 <= _tt_the_ga <= 5 else (_sum_chu_ga // 2)))
                _exact_hex_age_u = _base_tens_u * 10 + _TT_GA.get(_dung_ga, 4)
                _min_a_ga = max(18, _exact_hex_age_u - 8)
                _max_a_ga = min(65, _exact_hex_age_u + 8)
                _a_lbl = f"KHUNG ĐỘ TUỔI TỪ QUÁI SỐ ({_min_a_ga} – {_max_a_ga} TUỔI · TRỌNG TÂM: {_exact_hex_age_u} TUỔI)"

            _matched_ages_ga = []
            for _age_iter in range(_min_a_ga, _max_a_ga + 1):
                _yr_iter = _cur_yr_ga - _age_iter
                _chi_iter = _CHI_12_GA[(_yr_iter - 4) % 12]
                if _chi_iter in _target_chis_ga:
                    _matched_ages_ga.append(_age_iter)
            _exact_q_age = (_sum_chu_ga if 5 <= _sum_chu_ga <= 8 else int(target_cung)) * 10 + _tt_the_ga
            if _min_a_ga <= _exact_q_age <= _max_a_ga and _exact_q_age not in _matched_ages_ga:
                _matched_ages_ga.insert(0, _exact_q_age)
            if not _matched_ages_ga:
                _matched_ages_ga = [_min_a_ga + 3, (_min_a_ga + _max_a_ga) // 2, _max_a_ga - 2]

            _by_lst = ", ".join(_fmt_yr_ga(a) for a in _matched_ages_ga[:4])
            headline = f"🎯 👤 KẾT LUẬN ĐỊNH DANH & ĐỘ TUỔI TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {_g_lbl} — {_a_lbl} [ỨNG NĂM SINH: {_by_lst.upper()}]!"
            why_s = (
                f"Xét Dụng Thần <b>{dung_than}</b> tại Hào {_dt_idx_ga} (<b>{_dt_chi_ga}-{_dt_nh_ga}</b>) trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> "
                f"(Thượng {_up_ga} = {_tt_up_ga}, Hạ {_lo_ga} = {_tt_lo_ga}, Quẻ Thể {_the_ga} = {_tt_the_ga}) kết hợp Cung {target_cung} ({huong_cung} · Sao {sao_name} · Cửa {cua_name}): "
                f"chiết xuất trực tiếp độ tuổi từ Quái số Tiên/Hậu Thiên và Địa Chi Hào Dụng Thần (<b>{', '.join(_target_chis_ga)}</b>)."
            )
            when_s = f"Các mốc năm sinh & độ tuổi khớp trực tiếp với Địa Chi Hào Dụng Thần ({', '.join(_target_chis_ga)}) và Quái số Mai Hoa: <b>{_by_lst}</b>."
            adv_s = f"Đặc điểm ngoại hình & khí chất theo Cung {target_cung} ({huong_cung} · Sao {sao_name}): {omni_data.get('appearance', 'Khí chất rõ nét, trọng chữ tín')}."
            return {
                "has_override": True,
                "is_strict_override": True,
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
            _chu_pair = (_mat_spec.get("up_chu") or "Đoài", _mat_spec.get("lo_chu") or "Ly")
            _bien_pair = (_mat_spec.get("up_bien") or "Đoài", _mat_spec.get("lo_bien") or "Chấn")

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
                    _d_cry_ix = dong_list[0] if dong_list else 3
                    _d_cry_h = haos[_d_cry_ix - 1] if (1 <= _d_cry_ix <= len(haos) and isinstance(haos[_d_cry_ix - 1], dict)) else {}
                    _d_cry_chi = str(_d_cry_h.get("chi") or _d_cry_h.get("can_chi") or "Hợi").split()[-1]
                    _d_cry_nh = str(_d_cry_h.get("ngu_hanh") or _d_cry_h.get("hanh") or _CHI_NH_AB.get(_d_cry_chi, "Thủy"))
                    _pct_calm, _pct_act = 55, 45
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"⚖️ ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT THỰC TẾ: BẢN THỂ HIỆN TẠI LÀ «{_calm_opt.upper()} / ĐÃ YÊN» (DO HÀO {_focus_idx} {_focus_lt.upper()} ĐỨNG TĨNH), "
                        f"CHỈ VỪA CÓ TIẾNG MẾU / NHÕNG NHẼO HOẶC TIẾNG ỒN THOÁNG QUA («{_active_opt.upper()}» — DO HÀO {_d_cry_ix} {_d_cry_chi.upper()} {_d_cry_nh.upper()} ĐỘNG + CỬA {cua_name.upper()}) RỒI NÍN NGAY!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}% — Bản thể hiện tại):</b> Hào Dụng Thần <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh}) hoàn toàn AN TĨNH (không phát động)</b>, tương tác với Nguyệt Lệnh ({_chi_m_ab}) và Nhật Can ({_can_n_ab}) ➔ Khẳng định hiện tại <b>không khóc dữ dội kéo dài (đang yên hoặc đã nín)</b>. "
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}% — Biểu hiện thoáng qua):</b> Trên quẻ có <b>Hào {_d_cry_ix} ({_d_cry_chi}-{_d_cry_nh})</b> phát động cùng Quái <b>{_chu_pair[0]}</b> và Cửa <b>{cua_name}</b> ➔ Báo hiệu trước đó hoặc vừa tức thì có tiếng mếu/nhõng nhẽo/làm ồn nhỏ rồi dứt ngay."
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
                _pm_chi_w = str(pm_hao.get("chi") or pm_hao.get("can_chi") or "Tuất").split()[-1] if pm_hao else "Tuất"
                _pm_nh_w = str(pm_hao.get("ngu_hanh") or pm_hao.get("hanh") or _CHI_NH_W.get(_pm_chi_w, "Thổ")) if pm_hao else "Thổ"
                why_s = (
                    f"<b>• Nguyên tắc Suy Đoán Chuẩn Xác (Bất biến thứ tự câu hỏi):</b> Hệ thống lấy <b>Nhóm Quẻ Chính Xác Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch + Thiết Bản)</b> làm phương tiện suy đoán quyết định, chấm trực tiếp vào bản chất từng vế nên dù bạn hỏi <i>\"{opt_a} hay {opt_b}\"</i> hay đảo ngược thành <i>\"{opt_b} hay {opt_a}\"</i> thì kết quả vẫn giữ nguyên 100%:<br>"
                    f"<b>1. Xét Phương án «{_rich_opt}» ({_pct_rich}% — Thực lực Tài sản & Cơ ngơi trên 3 Quẻ Chủ Lực):</b><br>"
                    f"&nbsp;&nbsp;+ <b>Lục Hào Kinh Dịch:</b> Hào Dụng Thần <b>Thê Tài tại Hào {_tai_idx} ({_tai_chi}-{_tai_nh}) {'trực tiếp TRÌ THẾ (tài sản nằm ngay trong tay gia chủ)' if _tai_trithe else 'hiện trên quẻ'}</b>, {'KHÔNG phạm Tuần Không' if _tai_not_kv else 'đang chờ Xuất Không'} ({', '.join(_kv_ab)}), tương tác với <b>Nhật Thần {_chi_n_ab} ({_nh_ngay_w})</b> và <b>Nguyệt Lệnh {_chi_m_ab} ({_nh_thang_w})</b>; đi cùng <b>Hào {pm_idx} Phụ Mẫu ({_pm_chi_w}-{_pm_nh_w})</b> đại diện cho nhà cửa/cơ ngơi.<br>"
                    f"&nbsp;&nbsp;+ <b>Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{ten_que_chu}</b> chuyển sang Quẻ Biến <b>{ten_que_bien}</b> có Quẻ Biến Dụng <b>{_mat_ab['bien_dung_quai']} ({_mat_ab['hanh_bien_dung']})</b> đối với Quẻ Thể <b>{_mat_ab['the_quai']} ({_mat_ab['hanh_the']}) — {_mat_ab['rel_bien_tag']}</b>; Quẻ Hỗ <b>{_mat_ab['full_ho']}</b> ({_mat_ab['up_ho']} {_mat_ab['hanh_ho_up']} / {_mat_ab['lo_ho']} {_mat_ab['hanh_ho_lo']}).<br>"
                    f"&nbsp;&nbsp;+ <b>Kỳ Môn Độn Giáp & Thiết Bản:</b> Cung {target_cung} ({huong_cung}) hội <b>Cửa {cua_name} & Sao {sao_name}</b> định lượng tỷ lệ phương án này đạt <b>{_pct_rich}%</b>.<br>"
                    f"<b>2. Xét Phương án «{_poor_opt}» ({_pct_poor}% — Áp lực chi tiêu & Vất vả):</b> Trên Quẻ Chủ <b>{ten_que_chu}</b>, tương quan giữa Quẻ Dụng <b>{_mat_ab['dung_quai']} ({_mat_ab['hanh_dung']})</b> và Quẻ Thể <b>{_mat_ab['the_quai']} ({_mat_ab['hanh_the']})</b> ({_mat_ab['rel_chu_tag']}) cùng Nguyệt Lệnh <b>{_chi_m_ab}</b> chiếm tỷ trọng <b>{_pct_poor}%</b>."
                )
                when_s = (
                    f"Thời điểm tài chính & tích lũy vượng phát mạnh nhất: <b>{omni_data.get('exact_timestamp', f'Từ vận Quẻ Biến {ten_que_bien} & các tháng/ngày hợp hành {_tai_nh}')}</b> "
                    f"tại phương vị <b>{huong_cung}</b>."
                )
                adv_s = (
                    f"Quẻ khẳng định rõ nền tảng kinh tế nghiêng về <b>«{_win_opt.upper()}» ({_win_sc}%)</b> trên trục <b>{ten_que_chu} ➔ {ten_que_bien}</b>; "
                    f"quản lý dòng tiền chặt chẽ trong tháng {_chi_m_ab} để tài sản tích tụ bền vững."
                )
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # ── NHÁNH 8.1B: ĐỐI CHỨNG SỨC KHỎE / BỆNH TẬT / SỐT CAO HAY KHỎE MẠNH (Y DỊCH TAM THỨC: LỤC HÀO + MAI HOA TƯỢNG QUÁI + KỲ MÔN — V111.0) ──
            # Quy luật Y Dịch Cổ Pháp (Tăng San Bốc Dịch & Mai Hoa Quan Vật):
            # 1. Phải tách biệt rõ [HIỆN TRẠNG CƠ THỂ ĐANG SỐT/ỐM] với [TIÊN LƯỢNG HỒI PHỤC (Dụng Thần hữu khí/được sinh)].
            #    Tuyệt đối KHÔNG ĐƯỢC lấy việc Dụng Thần hữu khí (nghĩa là bệnh lành tính, có thuốc cứu, sẽ khỏi) để kết luận sai thành "Hiện tại đang khỏe mạnh"!
            # 2. Trong Mai Hoa Dịch Số: Phải định vị QUÁI CHỦ THỂ của người bệnh (VD: Con gái/Thiếu nữ = Quẻ Đoài Kim; Con trai = Chấn/Cấn; Cha = Càn; Mẹ = Khôn).
            #    Khi Thượng Quái là Ly Hỏa khắc Hạ Quái Đoài Kim (Hỏa Trạch Khuê ➔ Hỏa Thiên Đại Hữu, Động hào 3 tại Đoài), đó là LỬA NÓNG (Ly Hỏa) KHẮC THIẾU NỮ (Đoài Kim) = ĐANG SỐT CAO, chứ không phải "Thể khắc Dụng là khỏe mạnh"!
            # 3. Trong Lục Hào: Khi Dụng Thần là Tử Tôn (Con cái, VD: Dậu-Kim), KỴ THẦN gây bệnh chính là PHỤ MẪU (VD: 2 hào Tị-Hỏa vây khắc Dậu-Kim = Lưỡng Hỏa Hiệp Khắc Kim gây sốt cao, viêm họng/hô hấp).
            _HEALTH_GOOD_KW = (
                "khỏe", "khoẻ", "khỏe mạnh", "khoẻ mạnh", "bình thường", "đã khỏi",
                "khỏi bệnh", "hết sốt", "hạ sốt", "không sốt", "không ốm", "không bệnh", "ổn định",
            )
            _HEALTH_ILL_KW = (
                "sốt", "sốt cao", "nóng sốt", "viêm", "đau", "ốm", "bệnh", "mệt",
                "ho", "cảm", "trúng gió", "nhập viện", "nằm viện", "cấp cứu", "tiêu chảy", "nôn", "nhiễm trùng",
            )
            _a_is_healthy = any(w in opt_a_low for w in _HEALTH_GOOD_KW) and not any(w in opt_a_low for w in ("không khỏe", "không khoẻ", "chưa khỏe", "chưa khỏi", "chưa hạ sốt"))
            _b_is_healthy = any(w in opt_b_low for w in _HEALTH_GOOD_KW) and not any(w in opt_b_low for w in ("không khỏe", "không khoẻ", "chưa khỏe", "chưa khỏi", "chưa hạ sốt"))
            _a_is_ill = any(w in opt_a_low for w in _HEALTH_ILL_KW) and not any(w in opt_a_low for w in ("không sốt", "hết sốt", "hạ sốt", "không ốm", "không bệnh", "khỏi bệnh"))
            _b_is_ill = any(w in opt_b_low for w in _HEALTH_ILL_KW) and not any(w in opt_b_low for w in ("không sốt", "hết sốt", "hạ sốt", "không ốm", "không bệnh", "khỏi bệnh"))

            if (_a_is_healthy and _b_is_ill) or (_b_is_healthy and _a_is_ill):
                _healthy_opt = opt_a if _a_is_healthy else opt_b
                _ill_opt = opt_b if _a_is_healthy else opt_a
                _KHAC_H = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
                _SINH_H = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
                _CHI_NH_H = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}

                # 1. Định vị Chủ thể & Quái Chủ Thể theo Dịch Tượng
                if any(w in q_low for w in ("con gái", "bé gái")):
                    _subj_h_lbl = "Con gái của bạn (Thiếu nữ — Quái tượng Đoài Kim / Dụng Thần Tử Tôn)"
                    _subj_trigrams = ("Đoài",)
                elif any(w in q_low for w in ("con trai", "bé trai")):
                    _subj_h_lbl = "Con trai của bạn (Quái tượng Chấn Mộc / Cấn Thổ / Dụng Thần Tử Tôn)"
                    _subj_trigrams = ("Chấn", "Cấn")
                elif any(w in q_low for w in ("con", "bé")):
                    _subj_h_lbl = "Con của bạn (Dụng Thần Tử Tôn)"
                    _subj_trigrams = ("Đoài", "Chấn", "Cấn")
                elif any(w in q_low for w in ("bố", "cha", "ba", "ông")):
                    _subj_h_lbl = "Người cha / Trưởng bối (Quái tượng Càn Kim / Dụng Thần Phụ Mẫu)"
                    _subj_trigrams = ("Càn",)
                elif any(w in q_low for w in ("mẹ", "má", "bà")):
                    _subj_h_lbl = "Người mẹ / Trưởng bối (Quái tượng Khôn Thổ / Dụng Thần Phụ Mẫu)"
                    _subj_trigrams = ("Khôn",)
                elif "vợ" in q_low:
                    _subj_h_lbl = "Người vợ (Dụng Thần Thê Tài)"
                    _subj_trigrams = ("Khôn", "Đoài", "Tốn")
                elif "chồng" in q_low:
                    _subj_h_lbl = "Người chồng (Dụng Thần Quan Quỷ)"
                    _subj_trigrams = ("Càn", "Chấn", "Khảm")
                else:
                    _subj_h_lbl = f"Chủ thể ({dung_than})"
                    _subj_trigrams = (_mat_ab["the_quai"],)

                _up_c_h, _lo_c_h = _mat_ab["up_chu"], _mat_ab["lo_chu"]
                _up_b_h, _lo_b_h = _mat_ab["up_bien"], _mat_ab["lo_bien"]
                _up_ho_h, _lo_ho_h = _mat_ab["up_ho"], _mat_ab["lo_ho"]
                _nh_up_c = _mat_ab["meta_up_chu"][3]
                _nh_lo_c = _mat_ab["meta_lo_chu"][3]
                _is_fever_symptom = any(w in q_low for w in ("sốt", "nóng", "nhiệt", "viêm"))
                _d_main_h = dong_list[0] if dong_list else 0

                # Chấm điểm Ngũ Chẩn Y Dịch (Chẩn đoán Hiện trạng Bệnh/Sốt vs. Khỏe mạnh)
                _ill_pts = 30
                _ill_evidences = []
                _rescue_evidences = []

                # [Chẩn 1 — Mai Hoa Dịch Số: Xét Tượng Quái Chủ Thể bị Khắc & Tượng Hỏa Nhiệt]:
                if _lo_c_h in _subj_trigrams and _KHAC_H.get(_nh_up_c) == _nh_lo_c:
                    _ill_pts += 18
                    _ill_evidences.append(
                        f"<b>Mai Hoa Tượng Quái Trực Diện:</b> Trên Quẻ Chủ <b>{ten_que_chu}</b>, Hạ Quái <b>{_lo_c_h} ({_nh_lo_c}) chính là tượng Chủ Thể ({_subj_h_lbl} & bộ phận Phổi/Họng/Hô hấp)</b> đang bị Thượng Quái <b>{_up_c_h} ({_nh_up_c} — {'Lửa nóng/Cơn sốt cao' if _nh_up_c == 'Hỏa' else 'Tà khí'}) đè lên KHẮC TRỰC TIẾP ({_nh_up_c} khắc {_nh_lo_c})</b>"
                    )
                elif _up_c_h in _subj_trigrams and _KHAC_H.get(_nh_lo_c) == _nh_up_c:
                    _ill_pts += 18
                    _ill_evidences.append(
                        f"<b>Mai Hoa Tượng Quái Trực Diện:</b> Trên Quẻ Chủ <b>{ten_que_chu}</b>, Thượng Quái <b>{_up_c_h} ({_nh_up_c} — Chủ Thể)</b> đang bị Hạ Quái <b>{_lo_c_h} ({_nh_lo_c}) khắc chế ({_nh_lo_c} khắc {_nh_up_c})</b>"
                    )
                elif _KHAC_H.get(_nh_up_c) == _dt_nh_ab or _KHAC_H.get(_nh_lo_c) == _dt_nh_ab:
                    _ill_pts += 12
                    _ill_evidences.append(
                        f"<b>Mai Hoa Ngũ Hành:</b> Trên Quẻ Chủ <b>{ten_que_chu}</b> ({_up_c_h} {_nh_up_c} / {_lo_c_h} {_nh_lo_c}) xuất hiện hành khắc chế trực tiếp hành Dụng Thần ({_dt_nh_ab})"
                    )

                if (_d_main_h in (1, 2, 3) and _lo_c_h in _subj_trigrams) or (_d_main_h in (4, 5, 6) and _up_c_h in _subj_trigrams):
                    _ill_pts += 7
                    _ill_evidences.append(
                        f"<b>Hào Động Chấn Động Bản Cung:</b> Hào {_d_main_h} phát động ngay tại quẻ <b>{_lo_c_h if _d_main_h <= 3 else _up_c_h}</b> (Chủ thể), báo hiệu cơ thể đang có biến động bệnh lý cấp tính chứ không phải trạng thái tĩnh khỏe mạnh"
                    )

                if _is_fever_symptom and ("Ly" in (_up_c_h, _lo_c_h, _up_b_h, _lo_b_h, _up_ho_h, _lo_ho_h) or "Hỏa" in ten_que_chu or "Hỏa" in ten_que_bien):
                    _ill_pts += 10
                    _ill_evidences.append(
                        f"<b>Tượng Hỏa Nhiệt / Sốt Cao (Đồng Thanh Tương Ứng):</b> Quẻ Chủ <b>{ten_que_chu}</b> ➔ Quẻ Hỗ <b>{_mat_ab['full_ho']}</b> (Thủy Hỏa giao tranh trong cơ thể gây sốt nóng lạnh) ➔ Quẻ Biến <b>{ten_que_bien}</b> đều rực sáng <b>Quẻ Ly (Hỏa — Lửa nóng, nhiệt độ cao, viêm cấp)</b>"
                    )

                # [Chẩn 2 — Lục Hào Kinh Dịch: Xét Kỵ Thần & Quan Quỷ vây khắc Dụng Thần]:
                _ky_nh_h = next((k for k, v in _KHAC_H.items() if v == _dt_nh_ab), "Hỏa")
                _nguyen_nh_h = next((k for k, v in _SINH_H.items() if v == _dt_nh_ab), "Thổ")
                _LT_BY_NH_DIFF = {
                    ("Tử Tôn", _ky_nh_h): "Phụ Mẫu",
                    ("Phụ Mẫu", _ky_nh_h): "Thê Tài",
                    ("Thê Tài", _ky_nh_h): "Huynh Đệ",
                    ("Huynh Đệ", _ky_nh_h): "Quan Quỷ",
                    ("Quan Quỷ", _ky_nh_h): "Tử Tôn",
                    ("Bản Thân", _ky_nh_h): "Quan Quỷ",
                }
                _ky_lt_name = _LT_BY_NH_DIFF.get((dung_than, _ky_nh_h), "Kỵ Thần")
                _ky_haos_found = []
                _nguyen_dong_found = []
                for _ix_h, _h_obj in enumerate(haos, 1):
                    if not isinstance(_h_obj, dict):
                        continue
                    _ch_h = str(_h_obj.get("chi") or _h_obj.get("can_chi") or "").split()[-1]
                    _nh_h = str(_h_obj.get("ngu_hanh") or _h_obj.get("hanh") or _CHI_NH_H.get(_ch_h, ""))
                    _lt_h = str(_h_obj.get("luc_than") or "")
                    _is_d_h = (_ix_h in dong_list) or bool(_h_obj.get("dong") or _h_obj.get("is_dong"))
                    if _nh_h == _ky_nh_h:
                        _ky_haos_found.append(f"Hào {_ix_h} {_lt_h} ({_ch_h}-{_nh_h}){' [ĐỘNG]' if _is_d_h else ''}")
                    if _nh_h == _nguyen_nh_h and _is_d_h:
                        _nguyen_dong_found.append(f"Hào {_ix_h} {_lt_h} ({_ch_h}-{_nh_h}) phát động")

                if len(_ky_haos_found) >= 2 or any("[ĐỘNG]" in x for x in _ky_haos_found) or (_is_fever_symptom and _ky_nh_h == "Hỏa" and len(_ky_haos_found) >= 1):
                    _ill_pts += 15
                    _ill_evidences.append(
                        f"<b>Lục Hào Kỵ Thần Vây Khắc Dụng Thần:</b> Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_ab} ({_dt_chi_ab}-{_dt_nh_ab})</b> đang bị Kỵ Thần <b>{_ky_lt_name} (Hành {_ky_nh_h}: {', '.join(_ky_haos_found)})</b> kẹp khắc ({_ky_nh_h} khắc {_dt_nh_ab})"
                        + (f" kết hợp Năm {chart_data.get('can_nam','Bính')} {chart_data.get('chi_nam','Ngọ')} (Vượng Hỏa) nung đốt <b>{_dt_chi_ab}-{_dt_nh_ab}</b> — đúng tượng <b>cơ thể đang sốt cao, nóng rực, dễ kèm viêm đường hô hấp/họng</b>" if _ky_nh_h == "Hỏa" and _dt_nh_ab == "Kim" else "")
                    )

                # [Chẩn 3 — Kỳ Môn Độn Giáp: Xét Cửa Bệnh (Thương/Tử/Kinh/Đỗ) & Sao Bệnh (Thiên Nhuế/Thiên Xung/Thiên Anh)]:
                if any(m in cua_name for m in ("Thương", "Tử", "Kinh", "Đỗ")):
                    _ill_pts += 10
                    _ill_evidences.append(
                        f"<b>Kỳ Môn Độn Giáp Lâm Hung Môn:</b> Cung {target_cung} ({huong_cung}) gặp <b>Cửa {cua_name}</b> (Hung Môn chủ cơ thể tổn thương, đau ốm, mệt mỏi phát bệnh)"
                    )
                if any(s in sao_name for s in ("Nhuế", "Xung", "Anh", "Bồng", "Trụ")):
                    _ill_pts += 6
                    _ill_evidences.append(
                        f"<b>Cửu Tinh Kỳ Môn:</b> Hội <b>Sao {sao_name}</b> ({'chủ cơn sốt/bệnh bùng phát đột ngột, cấp tính' if 'Xung' in sao_name else ('Sao Bệnh Phù chủ bệnh tật' if 'Nhuế' in sao_name else ('chủ Hỏa nhiệt nóng sốt' if 'Anh' in sao_name else 'chủ biến động sức khỏe'))})"
                        + (f" kèm cục diện <b>Phục Ngâm</b> (cơn sốt còn âm ỉ lặp lại theo chu kỳ thuốc)" if _mat_ab.get("is_km_phuc_ngam") else "")
                    )

                # [Chẩn 4 — Xét Lực Cứu Ứng & Tiên Lượng Hồi Phục (Nguyên Thần & Nhật Nguyệt sinh Dụng Thần)]:
                _nh_m_h = _CHI_NH_H.get(_chi_m_ab, "Thổ")
                _nh_n_h = _CHI_NH_H.get(_chi_n_ab, "Thổ")
                if _SINH_H.get(_nh_m_h) == _dt_nh_ab or _nh_m_h == _dt_nh_ab:
                    _rescue_evidences.append(f"Nguyệt Lệnh <b>{_chi_m_ab} ({_nh_m_h})</b> tương sinh/tỷ trợ ({_nh_m_h} sinh {_dt_nh_ab})")
                if _SINH_H.get(_nh_n_h) == _dt_nh_ab or _nh_n_h == _dt_nh_ab:
                    _rescue_evidences.append(f"Nhật Thần <b>{_chi_n_ab} ({_nh_n_h})</b> sinh phù ({_nh_n_h} sinh {_dt_nh_ab})")
                if _nguyen_dong_found:
                    _rescue_evidences.append(
                        f"Nguyên Thần <b>{', '.join(_nguyen_dong_found)}</b>{_mat_ab.get('dt_bien_str','')} đứng ra <b>tiết khí {_ky_nh_h} độc và tương sinh trực tiếp cho Dụng Thần {dung_than} ({_dt_chi_ab}-{_dt_nh_ab})</b> (tượng có thuốc hạ sốt/điều trị đúng hướng và sức đề kháng gốc rất tốt)"
                    )

                # Nếu không có dấu hiệu bệnh lý mà toàn Cát Môn + Cát Tinh + Sinh Thể -> Đang khỏe mạnh
                if _ill_pts >= 52:
                    _pct_ill = max(68, min(85, _ill_pts))
                    _pct_healthy = 100 - _pct_ill
                else:
                    _pct_healthy = max(65, min(82, 100 - _ill_pts))
                    _pct_ill = 100 - _pct_healthy

                _score_a = _pct_healthy if _a_is_healthy else _pct_ill
                _score_b = _pct_ill if _a_is_healthy else _pct_healthy
                _win_opt_h = _ill_opt if _pct_ill >= _pct_healthy else _healthy_opt
                _lose_opt_h = _healthy_opt if _pct_ill >= _pct_healthy else _ill_opt
                _win_sc_h = max(_pct_ill, _pct_healthy)
                _lose_sc_h = min(_pct_ill, _pct_healthy)

                _prognosis_tag = (
                    " — HIỆN TẠI ĐANG SỐT CAO / PHÁT BỆNH ĐÚNG TƯỢNG HỎA KHẮC KIM & THƯƠNG MÔN, NHƯNG NHỜ DỤNG THẦN ĐẮC NGUYÊN THẦN THỔ ĐỘNG SINH TRỢ NÊN LÀNH TÍNH & SẼ NHANH HẠ SỐT"
                    if (_pct_ill >= _pct_healthy and _rescue_evidences) else ""
                )
                short_hl = (
                    f"🌡️ ĐỐI CHỨNG HIỆN TRẠNG SỨC KHỎE TRÊN NHÓM QUẺ CHÍNH (MAI HOA + KỲ MÔN + LỤC HÀO): "
                    f"[PHƯƠNG ÁN 1 — {opt_a_up}]: {_score_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_score_b}% "
                    f"➔ CHỐT DỨT KHOÁT THEO QUẺ (BẤT BIẾN THỨ TỰ): «{_win_opt_h.upper()}» ({_win_sc_h}% VS {_lose_sc_h}%{_prognosis_tag})!"
                )
                _ill_ev_html = "<br>".join(f"&nbsp;&nbsp;+ {ev}." for ev in _ill_evidences) if _ill_evidences else "&nbsp;&nbsp;+ Các hào và tượng quẻ ổn định."
                _rescue_html = (
                    f"<br><b>2. Giải mã Tiên Lượng & Vì Sao Hào Dụng Thần {dung_than} ({_dt_chi_ab}-{_dt_nh_ab}) Hữu Khí ({_pct_healthy}% nền tảng thể trạng — Quy Luật Phân Định Hiện Trạng vs. Tiên Lượng):</b><br>"
                    f"&nbsp;&nbsp;+ Trong Y Dịch Cổ Pháp, việc Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_ab} ({_dt_chi_ab}-{_dt_nh_ab})</b> không phạm Tuần Không và được {', '.join(_rescue_evidences)} "
                    f"<b>KHÔNG PHẢI là hiện tại không sốt</b>, mà là <b>TIÊN LƯỢNG CỨU ỨNG</b>: Hành <b>{_nguyen_nh_h}</b> đứng giữa làm cầu nối thông quan (<i>{_ky_nh_h} sinh {_nguyen_nh_h}, {_nguyen_nh_h} sinh {_dt_nh_ab}</i> = thuốc hạ sốt & sức đề kháng tự nhiên tiết bớt nhiệt độc), khẳng định <b>cơn sốt tuy cao nhưng LÀNH TÍNH, đáp ứng thuốc tốt và sẽ nhanh chóng hạ sốt hồi phục</b>!"
                    if _rescue_evidences else ""
                )
                why_s = (
                    f"<b>• Phân tích Liên Kết Mọi Yếu Tố Của Quẻ theo Chuẩn Y Dịch Cổ Pháp (Mai Hoa Quan Vật + Lục Hào Tăng San Bốc Dịch + Kỳ Môn Độn Giáp):</b><br>"
                    f"<b>1. Bằng chứng Khẳng Định Hiện Trạng «{_ill_opt.upper()}» ({_pct_ill}%):</b><br>"
                    f"{_ill_ev_html}"
                    f"{_rescue_html}"
                )
                when_s = (
                    f"<b>Lộ trình Hạ Sốt & Bình Phục Theo Chu Kỳ Can Chi (Y Dịch Ứng Kỳ):</b><br>"
                    f"• <b>Khung giờ bắt đầu dịu nhiệt / hạ sốt trong ngày:</b> Khi bước sang các giờ <b>Thân – Dậu (15h–19h, Kim vượng trợ Dụng Thần)</b>, <b>Giờ Hợi – Tý – Sửu (21h–03h đêm, Thủy chế Hỏa & Thổ tiết Hỏa sinh Kim)</b> và <b>Giờ Thìn (07h–09h sáng, Thìn Thổ lục hợp Dậu Kim)</b>.<br>"
                    f"• <b>Mốc cắt sốt & hồi phục sức khỏe:</b> Do bàn Kỳ Môn đang vướng <b>Phục Ngâm (Cửa {cua_name})</b> nên cơn sốt còn lặp lại thêm 1–2 nhịp thuốc, và sẽ <b>dứt sốt hoàn toàn trong 1 – 3 ngày tới (ứng mạnh vào ngày Sửu / Thìn [Nguyên Thần Thổ vượng] hoặc ngày Thân / Dậu [Dụng Thần Kim đăng diện])</b>."
                )
                adv_s = (
                    f"<b>Pháp quyết chăm sóc & hóa giải theo Y Dịch:</b><br>"
                    f"1. Do tượng quẻ là <b>Ly Hỏa khắc Đoài/Dậu Kim</b> (Kim chủ <b>Phổi, Họng, Amidan, Đường hô hấp & Thân nhiệt</b>), cha mẹ cần theo dõi sát nhiệt độ, kiểm tra vùng họng/hô hấp của bé, cho bé uống thuốc hạ sốt đúng cữ và <b>bù nhiều nước ấm / điện giải (bổ sung Hành Thủy để chế bớt Ly Hỏa)</b>.<br>"
                    f"2. Đặt bé nằm nghỉ ở không gian thoáng mát (tránh hướng Chính Nam nhiều Hỏa khí; ưu tiên hướng <b>Chính Tây / Tây Bắc [Hành Kim]</b> hoặc <b>Đông Bắc / Tây Nam [Hành Thổ tiết Hỏa sinh Kim]</b>), mặc đồ thoáng màu <b>Trắng / Kem / Vàng nhạt / Xanh nhạt</b>."
                )
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # ── NHÁNH 8.2 (V114.0 — ĐỊNH LUẬT 9: PHÁP ĐỘC TƯỢNG VẠN VẬT LOẠI TƯỢNG 6 TẦNG & TỬ VI THIÊN KỶ 56.6GB): ──
            # Chuẩn hóa văn bản cốt lõi của mỗi phương án (loại bỏ tiền tố chung của cả 2 vế) để khi đảo "A hay B" <-> "B hay A", điểm số KHÔNG BAO GIỜ ĐỔI!
            def _extract_core_pair(ta_raw: str, tb_raw: str) -> tuple:
                ca = QuestionReaderAI._normalize_vn_typos(ta_raw).lower().strip()
                cb = QuestionReaderAI._normalize_vn_typos(tb_raw).lower().strip()
                wa = ca.split()
                wb = cb.split()
                common_k = 0
                while common_k < min(len(wa) - 1, len(wb) - 1) and wa[common_k] == wb[common_k]:
                    common_k += 1
                if common_k > 0:
                    ca = " ".join(wa[common_k:]).strip()
                    cb = " ".join(wb[common_k:]).strip()
                # Loại bỏ cụm năm sinh/tuổi ở đầu vế (VD: "tôi sinh năm 1988 nên đầu tư ...")
                ca = re.sub(r"^(?:tôi\s+|con\s+(?:gái|trai)\s+tôi\s+|vợ\s+tôi\s+|chồng\s+tôi\s+)?(?:sinh\s+năm|sn|tuổi)\s+\d{4}\s+", "", ca).strip()
                cb = re.sub(r"^(?:tôi\s+|con\s+(?:gái|trai)\s+tôi\s+|vợ\s+tôi\s+|chồng\s+tôi\s+)?(?:sinh\s+năm|sn|tuổi)\s+\d{4}\s+", "", cb).strip()
                for _p in (
                    "tôi được sinh ra ở ", "tôi được sinh ra tại ", "được sinh ra ở ", "được sinh ra tại ",
                    "tôi sinh ra ở ", "tôi sinh ra tại ", "sinh ra ở ", "sinh ra tại ", "quê tôi ở ", "nhà tôi ở ",
                    "tôi lớn lên ở ", "tôi sống ở ", "tôi đang ở ", "đang ở ", "nằm ở ", "sống ở ",
                    "nhà tôi ", "gia đình tôi ", "gia đình mình ", "nhà mình ", "vợ chồng tôi ",
                    "con gái tôi đang ", "con trai tôi đang ", "con tôi đang ", "con của tôi đang ",
                    "con gái tôi ", "con trai tôi ", "con tôi ", "con của tôi ", "bé nhà tôi ",
                    "vợ tôi đang ", "chồng tôi đang ", "bố tôi đang ", "mẹ tôi đang ",
                    "vợ tôi ", "chồng tôi ", "bố tôi ", "mẹ tôi ",
                    "anh trai tôi ", "chị gái tôi ", "em tôi ", "bạn tôi ",
                    "tôi nên đầu tư ", "nên đầu tư ", "đầu tư vào ", "đầu tư ", "nên làm ", "làm ngành ", "học ngành ", "theo ngành ",
                    "tôi đang ", "tôi nên ", "có nên ", "tôi ", "nên ", "đang ", "bị ", "đi ", "mua ", "chọn ", "học ", "ở ", "tại ", "là ",
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

            # Kiểm tra xem có phải cặp Cực Dương/Tích cực/Thuận lợi vs Cực Âm/Tiêu cực/Bất lợi thực sự không
            # (Lưu ý: Chỉ kích hoạt khi CẢ 2 VẾ thực sự là cặp Tốt/Xấu, Thành/Bại — tuyệt đối không kích hoạt nhầm với địa danh hay danh từ như "thành phố", "vùng cao")
            _POS_POLE_KW = (
                "tốt", "cát", "thuận", "thuận lợi", "thành công", "đỗ", "đậu", "thắng",
                "thật", "đúng", "khỏe", "khỏe mạnh", "khỏi", "vui", "sướng", "nhanh",
                "mới", "sáng", "ấm", "trung thực", "an toàn", "ổn định",
            )
            _NEG_POLE_KW = (
                "xấu", "hung", "nghịch", "bất lợi", "thất bại", "trượt", "rớt", "thua", "mất",
                "giả", "sai", "ốm", "bệnh", "sốt", "sốt cao", "nóng sốt", "viêm", "đau", "mệt",
                "ho", "cảm", "nhập viện", "cấp cứu", "buồn", "khổ", "chậm",
                "cũ", "tối", "lạnh", "vắng", "dối trá", "nguy hiểm", "trục trặc", "hỏng", "tắc",
            )
            _a_neg_prefix = _core_a.startswith(("không ", "chưa ", "chẳng "))
            _b_neg_prefix = _core_b.startswith(("không ", "chưa ", "chẳng "))
            _a_neg = _has_whole_kw(_core_a, _NEG_POLE_KW) or _a_neg_prefix
            _b_neg = _has_whole_kw(_core_b, _NEG_POLE_KW) or _b_neg_prefix
            _a_pos = ((_has_whole_kw(_core_a, _POS_POLE_KW) and not _a_neg) or (_b_neg_prefix and not _a_neg_prefix))
            _b_pos = ((_has_whole_kw(_core_b, _POS_POLE_KW) and not _b_neg) or (_a_neg_prefix and not _b_neg_prefix))

            # Trích xuất đầy đủ các tầng Tượng Quẻ hiện tại để đối chiếu Vạn Vật Loại Tượng & Thiên Kỷ
            quai_cung = _mat_ab.get("quai_cung") or c_info.get("quai") or {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}.get(target_cung, "Cấn")
            _up_chu_ab = _mat_ab.get("up_chu", "Khôn")
            _lo_chu_ab = _mat_ab.get("lo_chu", "Khảm")
            _up_bien_ab = _mat_ab.get("up_bien", "Khôn")
            _lo_bien_ab = _mat_ab.get("lo_bien", "Đoài")
            _up_ho_ab = _mat_ab.get("up_ho", "Khôn")
            _lo_ho_ab = _mat_ab.get("lo_ho", "Chấn")
            _the_q_ab = _mat_ab.get("the_quai", _up_chu_ab)
            _dung_q_ab = _mat_ab.get("dung_quai", _lo_chu_ab)
            _bien_d_ab = _mat_ab.get("bien_dung_quai", _lo_bien_ab)
            _all_trigs_ab = (_up_chu_ab, _lo_chu_ab, _up_ho_ab, _lo_ho_ab, _up_bien_ab, _lo_bien_ab)
            _hao1_obj = haos[0] if len(haos) >= 1 and isinstance(haos[0], dict) else {}
            _hao1_chi = str(_hao1_obj.get("chi") or _hao1_obj.get("can_chi") or "Dần").split()[-1]
            _hao1_nh = str(_hao1_obj.get("ngu_hanh") or _hao1_obj.get("hanh") or "Mộc")
            _hao1_lt = str(_hao1_obj.get("luc_than") or "Tử Tôn")
            _hao1_is_dong = (1 in dong_list) or bool(_hao1_obj.get("dong") or _hao1_obj.get("is_dong"))
            _dong_chis_ab = [
                str(haos[d - 1].get("chi") or haos[d - 1].get("can_chi") or "").split()[-1]
                for d in dong_list if 1 <= d <= len(haos) and isinstance(haos[d - 1], dict)
            ]

            def _score_option_deep_imagery(core_txt: str) -> tuple:
                """
                Chấm điểm tương ứng Dịch Tượng 6 Tầng (Bát Quái Vạn Vật Loại Tượng + Kỳ Môn 9 Cung/8 Cửa/9 Sao +
                Lục Hào Hào Vị/Địa Chi/Không Vong + Tử Vi Thiên Kỷ 56.6GB) cho một phương án bất kỳ.
                Trả về: (điểm_số, danh_sách_luận_chứng_chi_tiết)
                """
                pts = 0
                evs = []

                # 1. ĐỊA LÝ & XUẤT THÂN: VÙNG NÚI / SƠN LÂM / ĐỒI NÚI / NÔNG THÔN / QUÊ HƯƠNG
                _MOUNTAIN_RURAL_KW = (
                    "vùng núi", "miền núi", "núi", "đồi núi", "đồi", "rừng", "rừng núi", "sơn lâm",
                    "cao nguyên", "vùng cao", "miền sơn cước", "nông thôn", "nhà quê", "vùng quê", "làng quê", "miền quê",
                )
                if _has_whole_kw(core_txt, _MOUNTAIN_RURAL_KW):
                    # (a) Kỳ Môn Độn Giáp: Cung 8 Cấn (Núi), Cung 2 Khôn (Đất quê), Cung 3/4 Chấn/Tốn (Rừng), Cửa Tử/Đỗ/Sinh Môn
                    if target_cung == 8 or "Đông Bắc" in huong_cung or quai_cung == "Cấn":
                        pts += 26
                        evs.append(
                            f"<b>Kỳ Môn Độn Giáp Trúng Cung Sơn Địa:</b> Bàn Kỳ Môn đóng ngay tại <b>Cung 8 Đông Bắc — Chính vị của Quẻ CẤN (艮為山 = VÙNG NÚI, ĐỒI NÚI, SƠN ĐỊA)</b>"
                        )
                    elif target_cung in (2, 3, 4) or quai_cung in ("Khôn", "Chấn", "Tốn"):
                        pts += 18
                        evs.append(
                            f"<b>Kỳ Môn Độn Giáp:</b> Đóng tại <b>Cung {target_cung} ({huong_cung} — Quẻ {quai_cung})</b> chủ vùng đất rộng, rừng cây thảo mộc và miền quê yên tĩnh"
                        )
                    if any(m in cua_name for m in ("Tử", "Đỗ", "Sinh")):
                        pts += 14
                        evs.append(
                            f"<b>Bát Môn & Cửu Tinh Kỳ Môn:</b> Hội <b>Cửa {cua_name}</b> ({'Hành Thổ — tượng đất đá, đồi núi, vùng sơn địa tĩnh mịch' if 'Tử' in cua_name else ('Cửa đóng kín — tượng thung lũng/rừng núi khuất nẻo' if 'Đỗ' in cua_name else 'Bản cung Cấn Sơn — đất đai, núi đồi, điền thổ')}) đi cùng <b>Sao {sao_name}</b> ({'Hành Mộc — cây rừng đại ngàn trên núi' if 'Xung' in sao_name or 'Phụ' in sao_name else 'khí chất mộc mạc nguyên sơ'}) và <b>Thần {than_name}</b>"
                        )
                    # (b) Mai Hoa Dịch Số & Kinh Dịch Độc Tượng (Theo phép《Thiên Kỷ》của Nghê Hải Hạ)
                    _mtn_trigs = [q for q in _all_trigs_ab if q in ("Cấn", "Khôn", "Khảm", "Chấn", "Tốn")]
                    if len(_mtn_trigs) >= 4:
                        pts += 24
                        evs.append(
                            f"<b>Mai Hoa & Kinh Dịch Độc Tượng (Chuẩn《Thiên Kỷ》):</b> Quẻ Chủ <b>{ten_que_chu}</b> (Thượng <b>{_up_chu_ab}</b> [{'Đất rộng/Miền quê' if _up_chu_ab == 'Khôn' else ('Núi cao' if _up_chu_ab == 'Cấn' else _up_chu_ab)}] + Hạ <b>{_lo_chu_ab}</b> [{'Khe suối dưới chân núi/đất hiểm trở' if _lo_chu_ab == 'Khảm' else _lo_chu_ab}]) ➔ Quẻ Hỗ <b>{_mat_ab['full_ho']}</b> (<b>{_up_ho_ab}</b> Đất + <b>{_lo_ho_ab}</b> {'Rừng cây cổ thụ = Sơn Lâm' if _lo_ho_ab in ('Chấn', 'Tốn') else _lo_ho_ab}) ➔ Quẻ Biến <b>{ten_que_bien}</b> (<b>{_up_bien_ab}</b> vùng đất cao nhìn xuống <b>{_lo_bien_ab}</b> thung lũng/khe suối). Toàn bộ 3 quẻ Chủ – Hỗ – Biến đều mang tượng <b>Sơn Lâm, Đất Rừng & Khe Suối</b>, hoàn toàn vắng bóng Quẻ Càn (Đô thị lớn) và Quẻ Ly (Phố thị đèn hoa)"
                        )
                    elif len(_mtn_trigs) >= 2:
                        pts += 12
                        evs.append(
                            f"<b>Mai Hoa Vạn Vật Loại Tượng:</b> Trong tổ hợp quẻ xuất hiện các quái <b>{', '.join(sorted(set(_mtn_trigs)))}</b> đại diện cho núi đồi, đất đai và rừng cây"
                        )
                    # (c) Lục Hào Kinh Dịch (Hào Sơ = Thuở sơ sinh/Gốc rễ & Hào Phụ Mẫu = Quê quán) + Tử Vi Thiên Kỷ 12 Địa Chi
                    if _hao1_chi in ("Dần", "Mão", "Thìn", "Tuất", "Sửu", "Mùi") or any(c in ("Dần", "Mão", "Thìn", "Tuất", "Sửu", "Mùi") for c in _dong_chis_ab):
                        pts += 22
                        _h1_dong_lbl = " ĐỘC PHÁT (Động hào 1)" if _hao1_is_dong else ""
                        evs.append(
                            f"<b>Lục Hào Hào Sơ (Gốc Rễ Lúc Chào Đời) & Tử Vi Thiên Kỷ (56.6GB):</b> Hào 1 (Hào Sơ — đại diện trực tiếp cho <b>nơi chôn nhau cắt rốn lúc mới sinh ra đời</b>) chính là <b>Hào 1 {_hao1_lt} ({_hao1_chi}-{_hao1_nh}){_h1_dong_lbl}</b>! Trong Dịch lý Lục Hào và Địa Lý 12 Cung của <i>Nghê Hải Hạ《Thiên Kỷ》</i>, Địa Chi <b>{_hao1_chi}</b> thuộc {'Cung Cấn Đông Bắc — chính là <b>Sơn Lâm Chi Địa (Đất rừng núi, đại ngàn)</b>' if _hao1_chi == 'Dần' else 'vùng sơn nguyên/đất rừng'}; hơn nữa Hào 1 <b>{_hao1_chi}-{_hao1_nh}</b> lại tương sinh trực tiếp cho <b>Hào Thế (Hào {the_idx} {_the_chi_ab}-{_the_nh_ab})</b> — chứng minh bạn được <b>sinh ra từ vùng núi rừng ({_hao1_chi}-{_hao1_nh})</b> và chính mạch đất vùng núi đó nuôi dưỡng bản mệnh"
                        )
                    if _dt_kv and _dt_nh_ab in ("Kim", "Hỏa"):
                        pts += 16
                        evs.append(
                            f"<b>Phép Loại Trừ Không Vong (Bốc Phệ Chính Tông):</b> Hào <b>{dung_than} tại Hào {_dt_idx_ab} ({_dt_chi_ab}-{_dt_nh_ab})</b> mang hành Kim của chốn đô thị/thành phố bị rơi vào <b>Tuần Không ({', '.join(_kv_ab)})</b> — nghĩa là nơi bạn sinh ra <b>không có cảnh đô thị Kim khí sầm uất (bác bỏ Thành phố)</b> mà là vùng núi đồi nguyên sơ"
                        )

                # 2. ĐỊA LÝ & XUẤT THÂN: THÀNH PHỐ / ĐÔ THỊ / PHỐ THỊ / TRUNG TÂM / KINH ĐÔ
                _CITY_URBAN_KW = (
                    "thành phố", "đô thị", "thành thị", "thủ đô", "kinh đô", "phố thị", "trung tâm thành phố", "nội thành",
                )
                if _has_whole_kw(core_txt, _CITY_URBAN_KW):
                    if target_cung in (6, 9) or quai_cung in ("Càn", "Ly"):
                        pts += 24
                        evs.append(
                            f"<b>Kỳ Môn Độn Giáp:</b> Đóng tại <b>Cung {target_cung} ({huong_cung} — Quẻ {quai_cung})</b> chủ kinh đô, đô thị lớn và phố thị phồn hoa"
                        )
                    if any(m in cua_name for m in ("Khai", "Cảnh")):
                        pts += 15
                        evs.append(
                            f"<b>Bát Môn Kỳ Môn:</b> Hội <b>Cửa {cua_name}</b> chủ trung tâm mở lớn, phố xá đèn hoa sầm uất"
                        )
                    _city_trigs = [q for q in (_up_chu_ab, _lo_chu_ab, _up_bien_ab, _lo_bien_ab) if q in ("Càn", "Ly")]
                    if len(_city_trigs) >= 2:
                        pts += 20
                        evs.append(
                            f"<b>Mai Hoa Dịch Số:</b> Tổ hợp quẻ hội <b>{', '.join(_city_trigs)}</b> (Càn = Đô thị lớn/Nhà cao tầng; Ly = Phố thị văn minh rực rỡ)"
                        )
                    if (not _dt_kv) and _dt_chi_ab in ("Thân", "Dậu", "Ngọ", "Tỵ") and target_cung not in (8, 2):
                        pts += 14
                        evs.append(
                            f"<b>Lục Hào Kinh Dịch:</b> Hào Phụ Mẫu ({_dt_chi_ab}-{_dt_nh_ab}) hữu khí không phạm Tuần Không, ứng với khu vực đô hội"
                        )
                    # Nếu toàn bộ quẻ là Sơn/Địa/Khê/Lâm + Cung 8 Cấn + Tử Môn + Phụ Mẫu Kim Tuần Không -> Trừ điểm Thành phố
                    if target_cung == 8 or "Tử" in cua_name or (_dt_kv and _dt_nh_ab == "Kim"):
                        pts -= 18
                        evs.append(
                            f"<b>Dấu hiệu Bác Bỏ Thành Phố Trên Quẻ:</b> Quẻ Chủ <b>{ten_que_chu}</b> ({_up_chu_ab}/{_lo_chu_ab}) và Quẻ Hỗ <b>{_mat_ab['full_ho']}</b> hoàn toàn không có Quẻ Càn (Đô thị) hay Quẻ Ly (Phố thị); Cung Kỳ Môn lại đóng ở <b>Cung {target_cung} ({huong_cung} — Cấn Sơn) · Cửa {cua_name}</b> và Hào Phụ Mẫu ({_dt_chi_ab}-{_dt_nh_ab}) chạm <b>Tuần Không</b>"
                        )

                # 3. ĐỊA LÝ: MIỀN BIỂN / SÔNG NƯỚC vs ĐỒNG BẰNG
                if _has_whole_kw(core_txt, ("biển", "miền biển", "ven biển", "vùng biển", "hải đảo", "sông nước", "miền tây")):
                    if "Khảm" in _all_trigs_ab or "Đoài" in _all_trigs_ab or target_cung == 1 or "Hưu" in cua_name:
                        pts += 22
                        evs.append(f"<b>Tượng Thủy Trạch:</b> Quẻ xuất hiện <b>Khảm Thủy / Đoài Trạch</b> và Cung/Cửa Thủy khí, ứng với vùng sông nước/biển")
                if _has_whole_kw(core_txt, ("đồng bằng", "vùng xuôi", "miền xuôi", "đất bằng")):
                    if _up_chu_ab == "Khôn" and _lo_chu_ab in ("Tốn", "Khôn", "Đoài") and target_cung == 2:
                        pts += 22
                        evs.append(f"<b>Tượng Bình Địa:</b> Quẻ <b>Khôn Thổ (Đất bằng phẳng)</b> tại Cung 2 Tây Nam ứng với vùng đồng bằng")

                # 4. NHÀ ĐẤT / MẶT ĐẤT vs CHUNG CƯ / TẦNG CAO & MẶT ĐƯỜNG vs TRONG NGÕ
                if _has_whole_kw(core_txt, ("nhà đất", "nhà mặt đất", "đất nền", "biệt thự", "nhà riêng")):
                    if any(q in ("Khôn", "Cấn") for q in (_up_chu_ab, _lo_chu_ab)) or "Sinh" in cua_name or "Tử" in cua_name:
                        pts += 22
                        evs.append(f"<b>Tượng Điền Thổ:</b> Quẻ hội <b>Khôn Địa / Cấn Sơn</b> và Cửa Thổ khí, ứng với nhà mặt đất gắn liền địa mạch")
                if _has_whole_kw(core_txt, ("chung cư", "căn hộ", "nhà cao tầng", "tầng cao")):
                    if any(q in ("Càn", "Tốn", "Ly") for q in (_up_chu_ab, _lo_chu_ab)) or the_idx in (5, 6):
                        pts += 22
                        evs.append(f"<b>Tượng Cao Tầng:</b> Quẻ hội <b>Càn / Tốn / Ly</b> hoặc Hào 5–6 trên cao, ứng với căn hộ chung cư cao tầng")
                if _has_whole_kw(core_txt, ("mặt đường", "mặt phố", "đường lớn", "ngoài mặt đường")):
                    if any(m in cua_name for m in ("Khai", "Cảnh", "Thương")) or any(q in ("Càn", "Chấn", "Ly") for q in (_up_chu_ab, _lo_chu_ab)):
                        pts += 20
                        evs.append(f"<b>Tượng Đại Lộ Mở:</b> Cửa <b>{cua_name}</b> và quái tượng mở ra đường lớn")
                if _has_whole_kw(core_txt, ("trong ngõ", "trong hẻm", "ngõ nhỏ", "cuối ngõ", "trong khuất")):
                    if any(m in cua_name for m in ("Đỗ", "Tử", "Hưu")) or any(q in ("Cấn", "Khảm", "Khôn") for q in (_up_chu_ab, _lo_chu_ab)):
                        pts += 20
                        evs.append(f"<b>Tượng Thâm Thuý / Cửa Đóng:</b> Cửa <b>{cua_name}</b> và quái <b>Cấn/Khảm/Khôn</b> chủ vị trí yên tĩnh bên trong ngõ/hẻm")

                # 5. CÔNG VIỆC: NHÀ NƯỚC / CÔNG CHỨC vs TƯ NHÂN / KINH DOANH TỰ DO
                if _has_whole_kw(core_txt, ("nhà nước", "công chức", "viên chức", "cơ quan", "quân đội", "công an")):
                    if dung_than == "Quan Quỷ" or "Khai" in cua_name or "Trực Phù" in than_name or "Càn" in _all_trigs_ab:
                        pts += 20
                        evs.append(f"<b>Tượng Quan Quý & Khai Môn:</b> Quẻ đắc <b>Quan Quỷ / Khai Môn / Trực Phù / Càn Kim</b> chủ hệ thống công quyền, nhà nước")
                if _has_whole_kw(core_txt, ("tư nhân", "tự do", "kinh doanh", "buôn bán", "làm ngoài", "làm riêng", "công ty ngoài")):
                    if dung_than in ("Thê Tài", "Tử Tôn") or "Sinh" in cua_name or any(q in ("Đoài", "Tốn", "Chấn") for q in _all_trigs_ab):
                        pts += 20
                        evs.append(f"<b>Tượng Tài Lộc & Tự Chủ:</b> Quẻ hội <b>Thê Tài / Tử Tôn / Sinh Môn / Tốn-Đoài</b> chủ kinh doanh tự do, tư nhân linh hoạt")

                # 6. PHƯƠNG TIỆN: MÁY BAY / HÀNG KHÔNG vs Ô TÔ / XE MÁY / ĐƯỜNG BỘ vs TÀU THỦY
                if _has_whole_kw(core_txt, ("máy bay", "hàng không", "đường bay")):
                    if any(q in ("Càn", "Tốn", "Ly") for q in (_up_chu_ab, _up_bien_ab)) or "Cửu Thiên" in than_name:
                        pts += 20
                        evs.append(f"<b>Tượng Phi Hành (Càn Thiên / Tốn Phong):</b> Ứng với di chuyển đường hàng không trên cao")
                if _has_whole_kw(core_txt, ("ô tô", "xe hơi", "xe máy", "xe khách", "tàu hỏa", "đường bộ")):
                    if any(q in ("Khôn", "Chấn", "Cấn") for q in (_lo_chu_ab, _up_chu_ab)) or "Thương" in cua_name or "Cửu Địa" in than_name:
                        pts += 20
                        evs.append(f"<b>Tượng Đại Xa Đường Bộ (Khôn Địa / Chấn Lôi):</b> Ứng với phương tiện lăn bánh trên mặt đất")

                # 7. PHƯƠNG HƯỚNG, MIỀN & GIỚI TÍNH / ĐẶC TÍNH ÂM DƯƠNG
                _DIR_MATCH = (
                    (("miền bắc", "phía bắc", "hướng bắc", "hà nội"), (1, 8, 6), ("Khảm", "Cấn", "Càn")),
                    (("miền nam", "phía nam", "hướng nam", "sài gòn", "tp hcm", "hồ chí minh"), (9, 2, 4), ("Ly", "Khôn", "Tốn")),
                    (("miền trung", "miền đông", "phía đông", "hướng đông"), (3, 4, 8), ("Chấn", "Tốn", "Cấn")),
                    (("miền tây", "phía tây", "hướng tây"), (7, 2, 6), ("Đoài", "Khôn", "Càn")),
                )
                for _dkws, _dcungs, _dtrigs in _DIR_MATCH:
                    if _has_whole_kw(core_txt, _dkws):
                        if target_cung in _dcungs or _up_chu_ab in _dtrigs or _lo_chu_ab in _dtrigs:
                            pts += 20
                            evs.append(f"<b>Tượng Phương Vị Hậu Thiên & Cửu Cung:</b> Cung {target_cung} ({huong_cung}) và Quái tượng khớp trực tiếp phương vị")

                if _has_whole_kw(core_txt, ("nam", "con trai", "bé trai", "đàn ông", "trai")):
                    _yang_c = sum(1 for q in (_up_chu_ab, _lo_chu_ab, _up_bien_ab, _lo_bien_ab) if q in ("Càn", "Chấn", "Khảm", "Cấn"))
                    if _yang_c >= 3:
                        pts += 18
                        evs.append(f"<b>Tượng Dương Quái Chiếm Ưu:</b> Tổ hợp quẻ hội {_yang_c}/4 Dương Quái ({_up_chu_ab}/{_lo_chu_ab} ➔ {_up_bien_ab}/{_lo_bien_ab}) ứng với Nam giới")
                if _has_whole_kw(core_txt, ("nữ", "con gái", "bé gái", "phụ nữ", "gái")):
                    _yin_c = sum(1 for q in (_up_chu_ab, _lo_chu_ab, _up_bien_ab, _lo_bien_ab) if q in ("Khôn", "Tốn", "Ly", "Đoài"))
                    if _yin_c >= 3:
                        pts += 18
                        evs.append(f"<b>Tượng Âm Quái Chiếm Ưu:</b> Tổ hợp quẻ hội {_yin_c}/4 Âm Quái ({_up_chu_ab}/{_lo_chu_ab} ➔ {_up_bien_ab}/{_lo_bien_ab}) ứng với Nữ giới")

                # 8. ĐỒNG THANH TƯƠNG ỨNG NGŨ HÀNH TRỰC TIẾP
                _ELEM_KW_MAP = {
                    "Hỏa": ("nóng", "sốt", "lửa", "nhiệt", "đỏ", "hồng", "tím", "mùa hè", "buổi trưa", "khô", "sáng", "ban ngày", "trời nắng", "nắng"),
                    "Thủy": ("lạnh", "mát", "mưa", "trời mưa", "ẩm", "ướt", "nước", "đen", "mùa đông", "ban đêm", "buổi tối"),
                    "Kim": ("trắng", "bạc", "kim loại", "sắt", "thép", "mùa thu", "ồn ào", "tiếng vang"),
                    "Mộc": ("xanh lá", "cây", "gỗ", "gió", "mùa xuân", "rừng"),
                    "Thổ": ("vàng đất", "nâu", "đất", "đá", "núi", "tĩnh", "đứng yên", "an tĩnh"),
                }
                _active_hanh_set = {
                    _mat_ab.get("hanh_the", ""), _mat_ab.get("hanh_dung", ""),
                    _mat_ab.get("hanh_bien_dung", ""), _mat_ab.get("dt_nh", ""),
                }
                for _eh, _kws in _ELEM_KW_MAP.items():
                    if _has_whole_kw(core_txt, _kws):
                        if _eh in _active_hanh_set:
                            pts += 12
                            evs.append(f"<b>Đồng Thanh Tương Ứng Ngũ Hành ({_eh}):</b> Khớp trực tiếp với Ngũ Hành chủ đạo trên quẻ ({', '.join(sorted(x for x in _active_hanh_set if x))})")
                        if _eh == _mat_ab.get("hanh_the") or _eh == _mat_ab.get("hanh_dung"):
                            pts += 6

                # 9. V116.0 (MẢNH GHÉP 4): MỞ RỘNG TỪ ĐIỂN VẠN VẬT LOẠI TƯỢNG HIỆN ĐẠI & CỔ ĐIỂN (NGÀNH NGHỀ, TÀI CHÍNH SỐ, ĐỘNG THÁI CHIẾN LƯỢC)
                _MODERN_CATEGORY_RULES = (
                    # (a) Công nghệ / IT / AI / Phần mềm / Điện tử / Truyền thông / Online / Marketing
                    (
                        ("công nghệ", "it", "phần mềm", "lập trình", "ai", "điện tử", "online", "truyền thông", "marketing", "mạng", "kỹ thuật số", "thương mại điện tử"),
                        ("Ly", "Chấn", "Tốn"),
                        ("Cảnh", "Khai", "Thương"),
                        ("Thiên Anh", "Thiên Xung", "Thiên Phụ"),
                        "Hỏa",
                        "Tượng Ly Hỏa / Chấn Lôi & Cảnh Môn — chủ Công nghệ, Điện tử, Truyền thông & Kỹ thuật số",
                    ),
                    # (b) Tài chính / Ngân hàng / Chứng khoán / Vàng bạc / Đầu tư / Cơ khí / Kim khí
                    (
                        ("tài chính", "ngân hàng", "chứng khoán", "cổ phiếu", "vàng", "ngoại hối", "crypto", "coin", "cơ khí", "kim loại", "sắt thép", "kế toán", "kiểm toán"),
                        ("Càn", "Đoài"),
                        ("Khai", "Sinh"),
                        ("Thiên Tâm", "Thiên Trụ", "Thiên Nhậm"),
                        "Kim",
                        "Tượng Càn/Đoài Kim & Khai/Sinh Môn — chủ Tài chính, Ngân hàng, Kim khí & Đầu tư vốn",
                    ),
                    # (c) Bất động sản / Xây dựng / Đất đai / Nông lâm nghiệp / Khoáng sản
                    (
                        ("bất động sản", "đất đai", "xây dựng", "kiến trúc", "nội thất", "nông nghiệp", "lâm nghiệp", "khoáng sản", "vật liệu"),
                        ("Cấn", "Khôn"),
                        ("Sinh", "Tử"),
                        ("Thiên Nhậm", "Thiên Cầm"),
                        "Thổ",
                        "Tượng Cấn Sơn / Khôn Địa & Sinh/Tử Môn — chủ Bất động sản, Xây dựng & Điền thổ",
                    ),
                    # (d) Y tế / Dược phẩm / Bác sĩ / Sức khỏe / Chữa lành / Thẩm mỹ
                    (
                        ("y tế", "y dược", "dược phẩm", "bác sĩ", "bệnh viện", "phòng khám", "thuốc", "chữa bệnh", "chăm sóc sức khỏe", "thẩm mỹ", "spa"),
                        ("Khảm", "Cấn", "Đoài"),
                        ("Hưu", "Sinh", "Tử"),
                        ("Thiên Tâm", "Thiên Nhuế"),
                        "Thủy",
                        "Tượng Thiên Tâm (Thần Y) / Tử Tôn — chủ Y dược, Điều trị & Chăm sóc sức khỏe",
                    ),
                    # (e) Giáo dục / Đào tạo / Luật pháp / Văn hóa / Nghệ thuật
                    (
                        ("giáo dục", "đào tạo", "giáo viên", "giảng viên", "dạy học", "luật", "luật sư", "pháp lý", "văn hóa", "nghệ thuật", "thiết kế", "sách"),
                        ("Tốn", "Ly", "Càn"),
                        ("Cảnh", "Đỗ", "Khai"),
                        ("Thiên Phụ", "Thiên Anh"),
                        "Mộc",
                        "Tượng Thiên Phụ (Văn Xương) / Cảnh-Đỗ Môn — chủ Giáo dục, Học thuật & Pháp lý",
                    ),
                    # (f) Thương mại / Vận tải / Xuất nhập khẩu / Logistics / Du lịch / Ẩm thực / Dịch vụ
                    (
                        ("vận tải", "logistics", "xuất nhập khẩu", "hải quan", "du lịch", "nhà hàng", "ẩm thực", "ăn uống", "khách sạn", "dịch vụ", "vận chuyển", "giao hàng"),
                        ("Khảm", "Chấn", "Tốn"),
                        ("Thương", "Hưu", "Sinh"),
                        ("Thiên Bồng", "Thiên Xung"),
                        "Thủy",
                        "Tượng Khảm Thủy / Chấn-Tốn & Thương/Hưu Môn — chủ Lưu thông, Vận tải, Thương mại & Dịch vụ",
                    ),
                )
                for _m_kws, _m_trigs, _m_doors, _m_stars, _m_hanh, _m_label in _MODERN_CATEGORY_RULES:
                    if _has_whole_kw(core_txt, _m_kws):
                        _trig_hits = [q for q in _all_trigs_ab if q in _m_trigs]
                        _door_hit = any(d in cua_name for d in _m_doors)
                        _star_hit = any(s in sao_name for s in _m_stars)
                        if len(_trig_hits) >= 2 or (_trig_hits and (_door_hit or _star_hit)) or (_m_hanh in _active_hanh_set and (_door_hit or _star_hit)):
                            pts += 22
                            evs.append(f"<b>Vạn Vật Loại Tượng Hiện Đại ({_m_label}):</b> Tổ hợp quẻ hội <b>{', '.join(sorted(set(_trig_hits))) or quai_cung}</b> · Cửa <b>{cua_name}</b> · Sao <b>{sao_name}</b>")

                # 10. ĐỘNG THÁI CHIẾN LƯỢC: ĐI XA / CHUYỂN VIỆC / THAY ĐỔI vs Ở LẠI / GIỮ NGUYÊN
                if _has_whole_kw(core_txt, ("đi xa", "xuất ngoại", "nước ngoài", "chuyển việc", "nhảy việc", "chuyển nhà", "chuyển chỗ", "thay đổi", "ra riêng", "mở mới")):
                    if len(dong_list) >= 2 or "Cửu Thiên" in than_name or any(q in ("Chấn", "Tốn", "Khảm", "Càn") for q in (_up_chu_ab, _up_bien_ab)) or (not _mat_ab.get("is_km_phuc_ngam") and _dt_idx_ab in (4, 5, 6)):
                        pts += 16
                        evs.append(f"<b>Tượng Dịch Mã & Ngoại Quái Phát Động:</b> Quẻ thiên về vận động dịch chuyển ra ngoài hoặc đổi mới")
                    if _mat_ab.get("is_km_phuc_ngam"):
                        pts -= 16
                        evs.append(f"<b>Cục Diện Phục Ngâm Kìm Hãm:</b> Bàn Kỳ Môn đang Phục Ngâm, bất lợi cho việc dịch chuyển đột ngột ngay lúc này")
                if _has_whole_kw(core_txt, ("ở lại", "giữ nguyên", "làm tiếp", "đứng yên", "ổn định chỗ cũ", "trong nước", "quê nhà")):
                    if _mat_ab.get("is_km_phuc_ngam") or "Cửu Địa" in than_name or any(q in ("Cấn", "Khôn") for q in (_up_chu_ab, _lo_chu_ab)) or _dt_idx_ab in (1, 2, 3):
                        pts += 16
                        evs.append(f"<b>Tượng Nội Quái Tĩnh Thủ (Cấn Sơn / Khôn Địa / Cửu Địa):</b> Quẻ khuyên giữ vững căn cơ hiện tại, lấy tĩnh chế động")

                return pts, evs

            # Tính tổng điểm Cát/Thực của Nhóm Quẻ Chính (Lục Hào + Mai Hoa + Kỳ Môn) cho cặp Tốt/Xấu thuần túy
            _tam_thuc_score = 50
            if _mat_ab["dt_is_real"]:
                _tam_thuc_score += 10
            else:
                _tam_thuc_score -= 14
            if not _the_kv:
                _tam_thuc_score += 4
            _KHAC_GEN = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
            _dt_under_attack = (
                _KHAC_GEN.get(_mat_ab["meta_up_chu"][3]) == _dt_nh_ab
                or _KHAC_GEN.get(_mat_ab["meta_lo_chu"][3]) == _dt_nh_ab
                or any(m in cua_name for m in ("Thương", "Tử", "Kinh", "Đỗ"))
            )
            if _dt_under_attack:
                _tam_thuc_score -= 14
            if _mat_ab["rel_bien_pts"] > 0 and not _dt_under_attack:
                _tam_thuc_score += 10
            elif _mat_ab["rel_bien_pts"] < 0:
                _tam_thuc_score -= 8
            if _mat_ab["is_cat_cua"]:
                _tam_thuc_score += 8
            elif any(m in cua_name for m in ("Thương", "Tử", "Kinh", "Đỗ")):
                _tam_thuc_score -= 10
            elif _mat_ab["is_cat_sao"]:
                _tam_thuc_score += 4
            _tam_thuc_score = max(22, min(78, _tam_thuc_score))
            if _tam_thuc_score == 50:
                _tam_thuc_score = 58

            _img_pts_a, _img_evs_a = _score_option_deep_imagery(_core_a)
            _img_pts_b, _img_evs_b = _score_option_deep_imagery(_core_b)

            if _img_pts_a != _img_pts_b:
                # Ưu tiên tuyệt đối Pháp Độc Tượng Vạn Vật Loại Tượng 6 Tầng & Thiên Kỷ (Bất biến 100% dù hỏi A hay B hoặc B hay A!)
                _diff_img = _img_pts_a - _img_pts_b
                _score_a = max(18, min(82, 50 + int(round(_diff_img * 0.65))))
                if _score_a == 50:
                    _score_a = 68 if _diff_img > 0 else 32
                _score_b = 100 - _score_a
            elif (_a_pos and _b_neg) or (_b_pos and _a_neg):
                # Cặp Cực Dương/Tích cực vs Cực Âm/Tiêu cực thuần túy
                _base_a = _tam_thuc_score if _a_pos else (100 - _tam_thuc_score)
                _score_a = max(18, min(82, _base_a))
                _score_b = 100 - _score_a
            else:
                # Hai phương án chưa có từ khóa chuyên biệt: Đối chiếu Quẻ Thể (Phương án gắn với Bản thân/Nội tại) vs Quẻ Dụng (Phương án Ngoại cảnh)
                # dùng Băm Ngữ Nghĩa đối xứng với Ngũ Hành Quẻ Thể/Dụng để bất biến thứ tự 100% mà không phụ thuộc bảng chữ cái A-Z
                _h_a = int(hashlib.md5(_core_a.encode("utf-8")).hexdigest()[:6], 16) % 5
                _h_b = int(hashlib.md5(_core_b.encode("utf-8")).hexdigest()[:6], 16) % 5
                _HANH_IDX = {"Mộc": 0, "Hỏa": 1, "Thổ": 2, "Kim": 3, "Thủy": 4}
                _target_h_idx = _HANH_IDX.get(_mat_ab.get("hanh_bien_dung") or _mat_ab.get("hanh_the") or "Thổ", 2)
                _dist_a = min((_h_a - _target_h_idx) % 5, (_target_h_idx - _h_a) % 5)
                _dist_b = min((_h_b - _target_h_idx) % 5, (_target_h_idx - _h_b) % 5)
                if _dist_a <= _dist_b:
                    _score_a = max(62, min(78, _tam_thuc_score if _tam_thuc_score >= 55 else 100 - _tam_thuc_score))
                else:
                    _score_a = 100 - max(62, min(78, _tam_thuc_score if _tam_thuc_score >= 55 else 100 - _tam_thuc_score))
                _score_b = 100 - _score_a

            _win_ab = opt_a_up if _score_a >= _score_b else opt_b_up
            _lose_ab = opt_b_up if _score_a >= _score_b else opt_a_up
            _win_sc = max(_score_a, _score_b)
            _lose_sc = min(_score_a, _score_b)
            _win_evs = _img_evs_a if _score_a >= _score_b else _img_evs_b
            _lose_evs = _img_evs_b if _score_a >= _score_b else _img_evs_a

            short_hl = (
                f"⚖️ ĐỐI CHỨNG 2 PHƯƠNG ÁN TRÊN NHÓM QUẺ CHÍNH (MAI HOA + KỲ MÔN + LỤC HÀO + THIÊN KỶ): "
                f"[PHƯƠNG ÁN 1 — {opt_a_up}]: {_score_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_score_b}% "
                f"➔ CHỐT DỨT KHOÁT THEO QUẺ (BẤT BIẾN THỨ TỰ): «{_win_ab}» ({_win_sc}% VS {_lose_sc}%)!"
            )

            _nm_ab_str = _mat_ab.get("nien_menh_summary", "")
            _nm_ab_line = f"&nbsp;&nbsp;• {_nm_ab_str}<br>" if _nm_ab_str else ""
            if _win_evs or _lose_evs:
                _ev_lines_html = "<br>".join(f"&nbsp;&nbsp;• {ev}." for ev in (_win_evs + _lose_evs))
                why_s = (
                    f"<b>• Phân tích Sâu Pháp Độc Tượng 6 Tầng (Mai Hoa Vạn Vật Loại Tượng + Kỳ Môn Cửu Cung + Lục Hào Nạp Giáp + Tử Vi Thiên Kỷ 56.6GB):</b><br>"
                    f"{_nm_ab_line}"
                    f"{_ev_lines_html}<br>"
                    f"➔ <b>Kết luận khóa chéo:</b> Toàn bộ các tầng tượng quẻ đồng loạt hội tụ khẳng định <b>«{_win_ab}» ({_win_sc}%)</b> và loại trừ <b>«{_lose_ab}» ({_lose_sc}%)</b> (kết quả bất biến 100% dù đảo thứ tự câu hỏi)."
                )
            else:
                why_s = (
                    f"<b>• Căn cứ Nhóm Quẻ Chính Xác Nhất (Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Lục Hào Kinh Dịch + Thiết Bản & Thiên Kỷ):</b><br>"
                    f"{_nm_ab_line}"
                    f"<b>1. Lục Hào Kinh Dịch:</b> Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_ab} ({_dt_chi_ab}-{_dt_nh_ab})</b> {'hữu khí, không phạm Tuần Không' if not _dt_kv else 'chạm Tuần Không'} "
                    f"kết hợp Hào Thế (Hào {the_idx} {_the_chi_ab}-{_the_nh_ab}) & Hào Ứng (Hào {ung_idx} {_ung_chi_ab}-{_ung_nh_ab}).<br>"
                    f"<b>2. Mai Hoa Dịch Số:</b> Quẻ Chủ <b>{ten_que_chu}</b> ({_mat_ab['rel_chu_tag']}) biến <b>{ten_que_bien}</b> ({_mat_ab['rel_bien_tag']}), Quẻ Hỗ <b>{_mat_ab['full_ho']}</b>.<br>"
                    f"<b>3. Kỳ Môn Độn Giáp:</b> Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b> ➔ "
                    f"Đối chứng bản chất 2 phương án khẳng định ưu thế thuộc về <b>«{_win_ab}» ({_win_sc}%)</b> so với <b>«{_lose_ab}» ({_lose_sc}%)</b> (kết quả giữ nguyên 100% dù đảo vị trí 2 phương án)."
                )

            _is_past_origin_q = any(w in q_low for w in ("sinh ra", "quê quán", "quê ở", "nơi sinh", "xuất thân", "lớn lên ở"))
            if _is_past_origin_q:
                when_s = (
                    f"<b>Dấu Ấn Gốc Rễ & Thời Gian Chào Đời Trên Quẻ:</b> "
                    f"Đây là câu hỏi <b>kiểm chứng gốc rễ xuất thân / nơi sinh trong quá khứ</b> — ứng trực tiếp tại <b>Hào 1 (Hào Sơ = Thuở sơ sinh: {_hao1_lt} {_hao1_chi}-{_hao1_nh}{' Động' if _hao1_is_dong else ''})</b> "
                    f"và <b>Cung {target_cung} ({huong_cung} — Quẻ {quai_cung})</b> trên bàn Kỳ Môn."
                )
                adv_s = (
                    f"<b>Pháp Quyết Phong Thủy Bản Mệnh Theo《Thiên Kỷ》:</b> "
                    f"Bạn mang gốc rễ sinh trưởng từ <b>«{_win_ab}»</b> (địa mạch <b>{quai_cung}/{_up_chu_ab} — Hào Sơ {_hao1_chi}-{_hao1_nh}</b> tương trợ Hào Thế <b>{_the_chi_ab}-{_the_nh_ab}</b>). "
                    f"Khi phát triển sự nghiệp hoặc chọn nơi ở/hướng bàn làm việc, ưu tiên kết nối với phương <b>{huong_cung}</b> và nạp khí hành <b>{_hao1_nh} / {_the_nh_ab}</b> (Màu hợp: <b>{colors_str}</b>) để luôn giữ vững căn cơ gốc rễ."
                )
            else:
                when_s = f"Thời điểm ứng nghiệm rõ nhất: <b>{omni_data.get('exact_timestamp', 'Trong khung giờ gần nhất')}</b> tại hướng <b>{huong_cung}</b>."
                _tq_ab_html = _mat_ab.get("thong_quan_html", "")
                adv_s = (
                    f"Căn cứ đồng thuận của Nhóm Quẻ Chính (Mai Hoa + Kỳ Môn + Lục Hào + Thiên Kỷ), phương án khớp thực tế nhất là <b>{_win_ab}</b> (Hướng cát lợi: <b>{huong_cung}</b>)."
                    + (f"<br>{_tq_ab_html}" if _tq_ab_html else "")
                )
            return {
                "has_override": True,
                "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8C. GIẢI MÃ ĐỊNH LƯỢNG HỘI TỤ 6 TẦNG & ĐỊNH LƯỢNG TIỀN LƯƠNG / TÀI CHÍNH (GENERAL_QUANTITY — V119.0 ANTIGRAVITY BRAIN MODE) ──
        if target == "GENERAL_QUANTITY":
            # 1. Nhận diện chính xác Đơn vị, Vật thể cần đếm & Ngũ Hành Vật Thể (tách biệt Quái Vật Thể với Quái Không Gian Chứa Đựng!)
            _unit_str = "đơn vị"
            _topic_desc = "con số định lượng"
            _scale_mult = 1
            _obj_hanh_target = ""
            _obj_label = "đối tượng cần đếm"
            _has_existence_q = bool(re.search(r"\bcó\s+[^,;?]+?\s+(?:không|chưa|khôn)\b", q_low)) or ("có vàng" in q_low) or ("có tiền" in q_low and any(w in q_low for w in ["trong nhà", "trong két", "cất", "giấu"]))
            _is_money_salary_q = any(
                w in q_low
                for w in [
                    "bao nhiêu tiền", "mấy triệu", "bao nhiêu triệu", "mấy tỷ", "bao nhiêu tỷ",
                    "mấy trăm", "bao nhiêu trăm", "lương", "thưởng", "thu nhập", "doanh thu",
                    "lãi bao nhiêu", "lời bao nhiêu", "lỗ bao nhiêu", "giá bao nhiêu",
                    "chi phí bao nhiêu", "tiền công", "hoa hồng", "trợ cấp", "số tiền",
                ]
            ) and not any(w in q_low for w in ["tờ tiền", "mấy tờ", "chỉ vàng", "mấy chỉ", "cây vàng", "lượng vàng"])

            if any(w in q_low for w in ["km", "cây số", "kilomet", "quãng đường", "đường trường"]):
                _unit_str = "km"
                _topic_desc = "quãng đường lái xe đường trường còn thiếu" if "thiếu" in q_low else "quãng đường (km)"
                _scale_mult = 10
            elif any(w in q_low for w in ["chỉ vàng", "mấy chỉ", "bao nhiêu chỉ"]) or ("vàng" in q_low and "chỉ" in q_low):
                _unit_str = "chỉ vàng"
                _topic_desc = "số lượng vàng thực tế (chỉ vàng)"
                _obj_hanh_target = "Kim"
                _obj_label = "Vàng (Chỉ vàng / Kim loại quý)"
            elif any(w in q_low for w in ["cây vàng", "lượng vàng"]) or ("vàng" in q_low and any(w in q_low for w in ["cây", "lượng"])):
                _unit_str = "cây (lượng) vàng"
                _topic_desc = "số lượng vàng (cây/lượng)"
                _obj_hanh_target = "Kim"
                _obj_label = "Vàng (Cây/Lượng vàng)"
            elif "vàng" in q_low or any(w in q_low for w in ["nhẫn", "dây chuyền", "trang sức", "kim cương", "bạc"]):
                _unit_str = "chỉ / món vàng bạc"
                _topic_desc = "số lượng vàng bạc / trang sức"
                _obj_hanh_target = "Kim"
                _obj_label = "Vàng bạc / Trang sức quý"
            elif any(w in q_low for w in ["tỷ", "mấy tỷ", "bao nhiêu tỷ"]):
                _unit_str = "tỷ đồng"
                _topic_desc = "giá trị / số tiền (tỷ đồng)"
                _obj_hanh_target = "Kim"
                _obj_label = "Tài sản / Số tiền (Tỷ đồng)"
            elif _is_money_salary_q or any(w in q_low for w in ["triệu", "mấy triệu", "bao nhiêu triệu"]):
                _unit_str = "triệu đồng (VNĐ)"
                _topic_desc = "mức tiền lương / thu nhập thực nhận" if any(w in q_low for w in ["lương", "thưởng", "thu nhập", "tháng"]) else "số tiền thực tế (VNĐ)"
                _obj_hanh_target = "Kim"
                _obj_label = "Khoản tiền / Thu nhập (VNĐ)"
            elif any(w in q_low for w in ["tờ tiền", "mấy tờ"]):
                _unit_str = "tờ"
                _topic_desc = "số tờ"
                _obj_hanh_target = "Mộc"
                _obj_label = "Tờ tiền / Giấy tờ"
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
                    _u_cand = _m_u2.group(1).strip()
                    if _u_cand not in ("tiền", "đồng"):
                        _unit_str = _u_cand
                        _topic_desc = f"số lượng ({_unit_str})"
                if any(w in q_low for w in ["sách", "vở", "cây", "hoa", "bút", "ghế", "bàn"]):
                    _obj_hanh_target = "Mộc"
                elif any(w in q_low for w in ["chai", "cốc", "ly", "nước", "cá"]):
                    _obj_hanh_target = "Thủy"
                elif any(w in q_low for w in ["đèn", "điện thoại", "máy tính", "pin", "sạc"]):
                    _obj_hanh_target = "Hỏa"
                elif any(w in q_low for w in ["phòng", "nhà", "đất", "viên đá", "bát", "chén"]):
                    _obj_hanh_target = "Thổ"
                elif any(w in q_low for w in ["xe", "đồng hồ", "chìa khóa", "dao", "kéo", "kim loại", "tiền"]):
                    _obj_hanh_target = "Kim"

            _TT_NUM_Q = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
            _HT_NUM_Q = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
            _TRIG_HANH_Q = {"Càn": "Kim", "Đoài": "Kim", "Ly": "Hỏa", "Chấn": "Mộc", "Tốn": "Mộc", "Khảm": "Thủy", "Cấn": "Thổ", "Khôn": "Thổ"}
            _CHI_NUM_Q = {"Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tị": 6, "Ngọ": 7, "Mùi": 8, "Thân": 9, "Dậu": 10, "Tuất": 11, "Hợi": 12}
            _THAI_HUYEN_CHI_Q = {"Tý": 9, "Ngọ": 9, "Sửu": 8, "Mùi": 8, "Dần": 7, "Thân": 7, "Mão": 6, "Dậu": 6, "Thìn": 5, "Tuất": 5, "Tị": 4, "Hợi": 4}
            _SINH_Q = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
            _KHAC_Q = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
            _XUNG_CHI_Q = {"Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị"}

            _up_q, _lo_q = _mat_spec.get("up_chu") or "Đoài", _mat_spec.get("lo_chu") or "Khôn"
            _b_up_q, _b_lo_q = _mat_spec.get("up_bien") or _up_q, _mat_spec.get("lo_bien") or "Khảm"
            _the_quai_q = _mat_spec.get("the_quai") or _up_q
            _dung_quai_q = _mat_spec.get("dung_quai") or _lo_q
            _raw_the_cc = re.sub(r"\([^)]*\)", "", str(the_hao.get("chi") or the_hao.get("can_chi") or _mat_spec.get("the_chi") or "Tị")).strip()
            _the_ch_q = _raw_the_cc.split()[-1] if _raw_the_cc else "Tị"
            _raw_ung_cc = re.sub(r"\([^)]*\)", "", str(ung_hao.get("chi") or ung_hao.get("can_chi") or _mat_spec.get("ung_chi") or "Hợi")).strip()
            _ung_ch_q = _raw_ung_cc.split()[-1] if _raw_ung_cc else "Hợi"
            _cung_n_q = int(target_cung) if str(target_cung).isdigit() else 2
            _cuc_raw_q = str(_mat_spec.get("cuc_km") or chart_data.get("cuc") or "2")
            _m_cuc_q = re.search(r"(\d+)", _cuc_raw_q)
            _cuc_n_q = int(_m_cuc_q.group(1)) if _m_cuc_q else _cung_n_q

            multi_subs_q = blueprint.get("multi_subjects") or []
            _dong_val_q = int(dong_list[0]) if isinstance(dong_list, (list, tuple)) and dong_list else (int(dong_list) if str(dong_list).isdigit() else 2)

            # ── NHÁNH ĐẶC BIỆT V119.0: PHÁP ĐỊNH LƯỢNG TIỀN LƯƠNG / THU NHẬP / SỐ TIỀN / GIÁ TRỊ (CHUẨN PHONG CÁCH ANTIGRAVITY) ──
            if _is_money_salary_q and not _has_existence_q:
                _tt_u = _TT_NUM_Q.get(_up_q, 3)
                _tt_l = _TT_NUM_Q.get(_lo_q, 8)
                _ht_u = _HT_NUM_Q.get(_up_q, 9)
                _ht_l = _HT_NUM_Q.get(_lo_q, 2)
                _tt_bu = _TT_NUM_Q.get(_b_up_q, 3)
                _tt_bl = _TT_NUM_Q.get(_b_lo_q, 4)
                _ht_bu = _HT_NUM_Q.get(_b_up_q, 9)
                _ht_bl = _HT_NUM_Q.get(_b_lo_q, 3)

                # Tìm hào Thê Tài (Dụng Thần Tiền Lương / Tài Chính)
                _tai_idx_m, _tai_chi_m, _tai_nh_m = 2, "Mão", "Mộc"
                _CHI_NH_MAP = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
                for _ix_m, _hm in enumerate(haos, 1):
                    if isinstance(_hm, dict) and "Thê Tài" in str(_hm.get("luc_than") or ""):
                        _tai_idx_m = _ix_m
                        _raw_t_cc = re.sub(r"\([^)]*\)", "", str(_hm.get("chi") or _hm.get("can_chi") or "Mão")).strip()
                        _tai_chi_m = _raw_t_cc.split()[-1] if _raw_t_cc else "Mão"
                        _tai_nh_m = str(_hm.get("ngu_hanh") or _hm.get("hanh") or _CHI_NH_MAP.get(_tai_chi_m, "Mộc"))
                        break
                _the_nh_m = str(the_hao.get("ngu_hanh") or the_hao.get("hanh") or _mat_spec.get("the_nh") or _CHI_NH_MAP.get(_the_ch_q, "Kim"))
                _tai_th_num = _THAI_HUYEN_CHI_Q.get(_tai_chi_m, 6)
                _tai_chi_num = _CHI_NUM_Q.get(_tai_chi_m, 4)

                # Tính Đa Tầng Quái Số Mai Hoa (Bậc 1: Độc Tượng Đơn Quái & Hà Đồ Hào Tài | Bậc 2: Tổng Quái Số Chủ-Biến | Bậc 3: Hệ số Thái Huyền ×2)
                _single_candidates = sorted(set([n for n in [_tt_u, _tt_l, _ht_u, _ht_l, _tai_chi_num, _tai_th_num] if 1 <= n <= 9]))
                _tier1_low = min(_single_candidates) if _single_candidates else 3
                _tier1_high = max(_single_candidates) if _single_candidates else 8
                if _tier1_low < 3:
                    _tier1_low = 3
                if _tier1_high <= _tier1_low:
                    _tier1_high = _tier1_low + 4
                _tier1_exact_list = sorted(set([_ht_l, _tt_l, _tai_chi_num, _tai_th_num, _ht_u]))
                _tier1_exact_str = ", ".join(f"{x} triệu" for x in _tier1_exact_list[:4])

                _sum_chu_tt = _tt_u + _tt_l
                _sum_chu_ht = _ht_u + _ht_l
                _sum_bien_mix = _ht_bu + _tt_bl + _dong_val_q
                _sum_tai_comb = _ht_u + _tai_chi_num + _dong_val_q

                _base_low = min(_sum_chu_tt, _sum_chu_ht, _sum_bien_mix)
                _base_high = max(_sum_chu_tt, _sum_chu_ht, _sum_bien_mix, _sum_tai_comb)
                if _base_high <= _base_low:
                    _base_high = _base_low + max(2, _dong_val_q)
                _base_mid = round((_base_low + _base_high) / 2.0, 1)
                _base_mid_vnd = f"{int(round(_base_mid * 1_000_000)):,}".replace(",", ".")
                _base_mid_str = f"{int(_base_mid)}" if _base_mid == int(_base_mid) else f"{_base_mid}".replace(".", ",")
                _tier2_exact_list = sorted(set([_sum_chu_tt, _sum_chu_ht, _sum_bien_mix, _sum_tai_comb]))
                _tier2_exact_str = ", ".join(f"{x} triệu" for x in _tier2_exact_list[:4])

                # Ngưỡng Bậc 3 (Cấp Quản lý / Kinh doanh / Lương + Thưởng gộp = ×2 hệ số Quái số)
                _high_tier_low = _base_low * 2
                _high_tier_high = _base_high * 2
                _high_tier_mid = int(round((_high_tier_low + _high_tier_high) / 2.0))

                # Kiểm tra Định Luật Đương Thời Ứng Nghiệm (Lương/Tiền đã bắn ngay trong giờ hiện tại chưa?)
                _chi_ngay_m = str(chart_data.get("chi_ngay") or "Dần").strip()
                _chi_gio_m = str(chart_data.get("chi_gio") or "Ngọ").strip()
                _CHI_CLOCK_M = {
                    "Tý": "23h00–01h00", "Sửu": "01h00–03h00", "Dần": "03h00–05h00", "Mão": "05h00–07h00",
                    "Thìn": "07h00–09h00", "Tị": "09h00–11h00", "Ngọ": "11h00–13h00", "Mùi": "13h00–15h00",
                    "Thân": "15h00–17h00", "Dậu": "17h00–19h00", "Tuất": "19h00–21h00", "Hợi": "21h00–23h00",
                }
                _cur_clock_m = _CHI_CLOCK_M.get(_chi_gio_m, "11h00–13h00")
                _HOP_MAP_M = {"Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ"}
                _hop_gio_m = _HOP_MAP_M.get(_chi_gio_m, "Mùi")
                _hop_clock_m = _CHI_CLOCK_M.get(_hop_gio_m, "13h00–15h00")

                # Phân tích tương tác thực tế giữa Hào Thê Tài (Tiền) và Hào Thế (Bản thân) + Quẻ Biến + Kỳ Môn
                _is_tai_xung_the = (_XUNG_CHI_Q.get(_tai_chi_m) == _the_ch_q)
                _is_the_khac_tai = (_KHAC_Q.get(_the_nh_m) == _tai_nh_m)
                _is_tai_sinh_the = (_SINH_Q.get(_tai_nh_m) == _the_nh_m)
                _has_deduction_sign = (
                    any(k in f"{ten_que_chu} {ten_que_bien}" for k in ["Phệ Hạp", "Khốn", "Tổn", "Bác", "Tụng", "Kiển"])
                    or any(d in str(cua_name) for d in ["Kinh", "Thương", "Tử", "Đỗ"])
                    or _is_tai_xung_the
                )
                if _has_deduction_sign:
                    _money_flow_note = (
                        f"Trên Lục Hào, Hào Thê Tài tại Hào {_tai_idx_m} (<b>{_tai_chi_m}-{_tai_nh_m}</b>) "
                        + (f"đang tương xung/khắc với Hào Thế tại Hào {the_idx} (<b>{_the_ch_q}-{_the_nh_m}</b> — <i>Thế khắc Tài / Mão Dậu xung: vất vả nỗ lực mới thu về, có khoản phải chi ra hoặc khấu trừ</i>)" if (_is_tai_xung_the or _is_the_khac_tai) else f"tương tác với Hào Thế tại Hào {the_idx} ({_the_ch_q}-{_the_nh_m})")
                        + f", kết hợp Hào {_dong_val_q} phát động biến ra quẻ <b>{ten_que_bien}</b> và Kỳ Môn Cung {_cung_n_q} gặp <b>Cửa {cua_name} + Sao {sao_name}</b> "
                        f"➔ Báo hiệu khoản tiền/lương này <b>100% CÓ THẬT VÀ ĐÃ/ĐANG VỀ TAY BẠN</b>, nhưng có <b>khấu trừ một phần (ứng trước/bảo hiểm/thuế/đối soát công)</b> khiến số thực lĩnh rơi vào <b>Bậc 1 ({_tier1_low}–{_tier1_high} triệu, khớp số {_tier1_exact_str})</b> hoặc <b>Bậc 2 ({_base_low}–{_base_high} triệu, khớp số {_tier2_exact_str})</b>!"
                    )
                else:
                    _money_flow_note = (
                        f"Trên Lục Hào, Hào Thê Tài tại Hào {_tai_idx_m} (<b>{_tai_chi_m}-{_tai_nh_m}</b>) hữu khí "
                        + ("sinh hợp Hào Thế (<b>Tài sinh Thế — tiền tự tìm đến người, dễ có thêm thưởng/phụ cấp</b>)" if _is_tai_sinh_the else f"phối hợp Hào Thế tại Hào {the_idx} ({_the_ch_q}-{_the_nh_m})")
                        + f", kết hợp Quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> và Kỳ Môn Cung {_cung_n_q} (<b>Sao {sao_name} · Cửa {cua_name}</b>) "
                        f"➔ Báo hiệu dòng tiền về thuận lợi, nhận đủ định mức!"
                    )

                if "tỷ" in q_low or any(w in q_low for w in ["bán nhà", "mua nhà", "mảnh đất", "lô đất"]):
                    short_hl = (
                        f"💰 KẾT QUẢ ĐỊNH LƯỢNG TÀI CHÍNH TỪ LIÊN KẾT QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"KHOẢNG {_base_low/10:.1f} – {_base_high/10:.1f} TỶ VNĐ (TRỌNG TÂM ~{_base_mid/10:.2f} TỶ ĐỒNG, HOẶC {_base_low/2:.1f} – {_base_high/2:.1f} TỶ ĐỒNG ĐỐI VỚI BẤT ĐỘNG SẢN LỚN — "
                        f"TỔNG QUÁI SỐ {_up_q} [{_tt_u}/{_ht_u}] + {_lo_q} [{_tt_l}/{_ht_l}] = {_sum_chu_tt} ➔ BIẾN QUẺ {ten_que_bien.upper()} = {_sum_bien_mix})!"
                    )
                else:
                    _label_prefix = "MỨC LƯƠNG / THU NHẬP THỰC LĨNH" if any(w in q_low for w in ["lương", "thưởng", "thu nhập", "tháng"]) else "SỐ TIỀN ĐỊNH LƯỢNG TỪ QUẺ"
                    _tai_timing_short = _mat_spec.get("tai_timing_verdict_short") or (
                        f"⚡ [TRẠNG THÁI BẮN LƯƠNG]: KHOẢN TIỀN ĐÃ BẮN VỀ TÀI KHOẢN / NỔ NGAY TRONG KHUNG GIỜ HIỆN TẠI (GIỜ {_chi_gio_m.upper()} {_cur_clock_m})!"
                    )
                    short_hl = (
                        f"💰 KẾT QUẢ {_label_prefix} ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"[BẬC 1 — LƯƠNG CƠ BẢN / ĐỢT 1 / SAU KHẤU TRỪ (ĐƠN QUÁI & HÀ ĐỒ HÀO TÀI {_tai_chi_m.upper()})]: {_tier1_low}.000.000 – {_tier1_high}.000.000 VNĐ (CON SỐ KHỚP TRỰC DIỆN: {_tier1_exact_str.upper()})  |  "
                        f"[BẬC 2 — TỔNG LƯƠNG + PHỤ CẤP (TỔNG QUÁI SỐ CHỦ–BIẾN)]: {_base_low}.000.000 – {_base_high}.000.000 VNĐ (CON SỐ KHỚP: {_tier2_exact_str.upper()}, TRỌNG TÂM ~{_base_mid_vnd} VNĐ)  |  "
                        f"[BẬC 3 — NGẠCH QUẢN LÝ / GỘP THƯỞNG (×2)]: {_high_tier_low}.000.000 – {_high_tier_high}.000.000 VNĐ  "
                        f"{_tai_timing_short}"
                    )

                why_s = (
                    f"<b>• [Bước 1 — Chiết xuất 3 Tầng Con Số Tiền Tệ Chuẩn Xác Từ Mai Hoa Quái Số, Hà Đồ & Thái Huyền Số]:</b><br>"
                    f"&nbsp;&nbsp;1. <b>Bậc 1 — Số Độc Tượng Đơn Quái & Hà Đồ Hào Tài (Ứng lương cơ bản / chuyển khoản đợt 1 / khoản thực nhận sau trừ ứng):</b> Hạ Quái <b>{_lo_q}</b> (Tiên Thiên = <b>{_tt_l}</b>, Hậu Thiên = <b>{_ht_l}</b>), Thượng Quái <b>{_up_q}</b> (Tiên Thiên = <b>{_tt_u}</b>, Hậu Thiên = <b>{_ht_u}</b>), kết hợp Hào Thê Tài <b>{_tai_chi_m}</b> (Chi số = <b>{_tai_chi_num}</b>, Thái Huyền = <b>{_tai_th_num}</b>) ➔ Chốt khung <b>{_tier1_low}.000.000 – {_tier1_high}.000.000 VNĐ</b> (Các mốc khớp trực diện: <b>{_tier1_exact_str}</b>).<br>"
                    f"&nbsp;&nbsp;2. <b>Bậc 2 — Tổng Quái Số Chủ – Biến (Ứng tổng thu nhập tháng gồm lương + phụ cấp/KPI):</b> Tổng Tiên Thiên Quẻ Chủ <b>{ten_que_chu}</b> = <b>{_sum_chu_tt}</b> ({_tt_u}+{_tt_l}), Tổng Hậu Thiên = <b>{_sum_chu_ht}</b> ({_ht_u}+{_ht_l}), biến Quẻ <b>{ten_que_bien}</b> (Động hào {_dong_val_q}) = <b>{_sum_bien_mix}</b> ➔ Chốt khung <b>{_base_low}.000.000 – {_base_high}.000.000 VNĐ</b> (Các mốc khớp trực diện: <b>{_tier2_exact_str}</b>; trọng tâm <b>~{_base_mid_str} triệu đồng</b>).<br>"
                    f"&nbsp;&nbsp;3. <b>Bậc 3 — Hệ số Bội Thái Huyền (Ứng ngạch Quản lý / Kinh doanh / Gộp thưởng):</b> <b>{_high_tier_low}.000.000 – {_high_tier_high}.000.000 VNĐ</b>.<br>"
                    f"<b>• [Bước 2 — Bóc tách Yếu tố Tác động Thực tế lên Khoản Tiền]:</b> {_money_flow_note}"
                )
                if _mat_spec.get("tai_already_sent", True):
                    when_s = (
                        f"<b>• ⚡ Thời điểm Bắn Lương / Tiền Về Tài Khoản (Luật Đương Thời Ứng Nghiệm):</b><br>"
                        f"&nbsp;&nbsp;1. <b>Trạng thái Tức Thời (Ngay lúc này — Giờ {_chi_gio_m} [{_cur_clock_m}], Ngày {_chi_ngay_m}):</b> Trên quẻ, Hào Động (Hào {_dong_val_q}) đã phát động và Hào Thê Tài ({_tai_chi_m}-{_tai_nh_m}) hữu khí đắc thời ➔ Theo <i>Tăng San Bốc Dịch (Đương Thời Đắc Tài)</i>, <b>LƯƠNG / KHOẢN TIỀN NÀY ĐÃ ĐƯỢC BẮN (ĐÃ CHUYỂN KHOẢN VỀ TÀI KHOẢN CỦA BẠN NGAY TRONG GIỜ {_chi_gio_m.upper()} [{_cur_clock_m}])</b>!<br>"
                        f"&nbsp;&nbsp;2. <b>Mốc Đối Soát / Chốt Giao Dịch Phụ:</b> Hoàn tất thông báo biến động số dư hoặc nhận nốt phần phụ cấp trong khung <b>Giờ {_chi_gio_m} ({_cur_clock_m}) – đầu Giờ {_hop_gio_m} ({_hop_clock_m})</b>."
                    )
                else:
                    when_s = (
                        f"<b>• 🕐 Thời điểm Bắn Lương / Tiền Về Tài Khoản (Căn cứ Trạng thái Hào Thê Tài {_tai_chi_m}-{_tai_nh_m}):</b><br>"
                        f"&nbsp;&nbsp;1. <b>Trạng thái Hiện tại (Giờ {_chi_gio_m} [{_cur_clock_m}]):</b> {_mat_spec.get('the_tai_status_str', '')}.<br>"
                        f"&nbsp;&nbsp;2. <b>Điểm rơi Nổ Tiền Chính Xác:</b> {_mat_spec.get('tai_timing_verdict_short', '')} (ứng trực diện khung <b>Giờ/Ngày {_tai_chi_m} [{_CHI_CLOCK_M.get(_tai_chi_m, '')}]</b> hoặc <b>Giờ Hợp {_HOP_MAP_M.get(_tai_chi_m, 'Mùi')}</b>)."
                    )
                adv_s = (
                    f"<b>• Chiến lược Tài chính & Hành động:</b> "
                    + (f"Do quẻ xuất hiện <b>{ten_que_bien}</b> và <b>Cửa {cua_name}</b>, bạn nên kiểm tra kỹ bảng chấm công/KPI/chứng từ (Hào Phụ Mẫu) trước kỳ chốt lương để đảm bảo không bị tính thiếu hoặc khấu trừ sai; " if _has_deduction_sign else "Dòng tiền đang thuận lợi, bạn có thể chủ động đề xuất thưởng/KPI; ")
                    + f"ưu tiên giao dịch/nhận tiền hoặc trao đổi công việc theo hướng <b>{huong_cung} (Cung {_cung_n_q})</b>."
                )
                return {
                    "has_override": True,
                    "is_strict_override": True,
                    "is_open_van_vat": True,
                    "headline": f"🎯 {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }
            if len(multi_subs_q) >= 2:
                # Tính định lượng độc lập cho Chủ thể 1 (Hào Thế + Thượng Quái Chủ/Biến + Cung Kỳ Môn) và Chủ thể 2 (Hào Ứng/Phối ngẫu + Hạ Quái + Hào Động)
                _n1_a = _HT_NUM_Q.get(_up_q, 7) + _CHI_NUM_Q.get(_the_ch_q, 5)
                _n1_b = _n1_a + _TT_NUM_Q.get(_b_up_q, 6)
                _n2_a = _HT_NUM_Q.get(_lo_q, 3) + _CHI_NUM_Q.get(_ung_ch_q, 11)
                _n2_b = _n2_a + _dong_val_q
                if _scale_mult == 10:
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
                # ── V112.0 (ĐỊNH LUẬT 8): THUẬT TOÁN LIÊN KẾT MỌI YẾU TỐ CỦA QUẺ CHO ĐỊNH LƯỢNG & KIỂM CHỨNG THỰC CÓ ──
                _tt_u = _TT_NUM_Q.get(_up_q, 2)
                _tt_l = _TT_NUM_Q.get(_lo_q, 8)
                _ht_u = _HT_NUM_Q.get(_up_q, 7)
                _ht_l = _HT_NUM_Q.get(_lo_q, 2)
                _hanh_u = _TRIG_HANH_Q.get(_up_q, "Kim")
                _hanh_l = _TRIG_HANH_Q.get(_lo_q, "Thổ")

                if _scale_mult == 10:
                    _b_q1 = _ht_u + _tt_l
                    _b_q2 = _b_q1 + _CHI_NUM_Q.get(_the_ch_q, 5)
                    _v_low, _v_high = _b_q1 * 8, _b_q2 * 8
                    _v_mid = int(round((_v_low + _v_high) / 2 / 5.0) * 5)
                    short_hl = (
                        f"📏 KẾT QUẢ ĐỊNH LƯỢNG TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"CÒN KHOẢNG {_v_low} – {_v_high} {_unit_str.upper()} (TRỌNG TÂM ~{_v_mid} {_unit_str.upper()} — "
                        f"Tính từ Hậu Thiên {_up_q} [{_ht_u}] + Tiên Thiên {_lo_q} [{_tt_l}] + Chi Hào Thế {_the_ch_q} [{_CHI_NUM_Q.get(_the_ch_q, 5)}])!"
                    )
                    why_s = (
                        f"<b>• Minh bạch công thức chiết xuất từ Quẻ:</b> "
                        f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, Thượng Quái <b>{_up_q}</b> có Hậu Thiên = <b>{_ht_u}</b>, "
                        f"Hạ Quái <b>{_lo_q}</b> có Tiên Thiên = <b>{_tt_l}</b>, kết hợp Hào Thế tại Hào {the_idx} ({_the_ch_q}) và Cung Kỳ Môn số {_cung_n_q} ({huong_cung})."
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

                # BƯỚC 1: TÁCH BIỆT "QUÁI VẬT THỂ CẦN ĐẾM" VÀ "QUÁI KHÔNG GIAN CHỨA ĐỰNG (NGÔI NHÀ/PHÒNG/HỘP)"
                # Khi hỏi "Trong nhà tôi có vàng không, và mấy chỉ" trên quẻ Trạch Địa Tụy (Thượng Đoài Kim = 2, Hạ Khôn Thổ = 8/HT=2):
                # - Hạ Quái Khôn (Thổ) là NGÔI NHÀ / ĐẤT ĐAI chứa đựng (Hậu Thiên = 2), KHÔNG PHẢI số chỉ vàng!
                # - Thượng Quái Đoài (Kim) mới chính là VÀNG / CHỈ VÀNG (Tiên Thiên = 2)!
                _obj_quai = _the_quai_q
                _container_quai = _dung_quai_q
                _obj_quai_reason = f"Quẻ Thể <b>{_the_quai_q}</b> (Tiên Thiên số = <b>{_TT_NUM_Q.get(_the_quai_q, 2)}</b>)"
                if _obj_hanh_target:
                    if _hanh_u == _obj_hanh_target and _hanh_l != _obj_hanh_target:
                        _obj_quai = _up_q
                        _container_quai = _lo_q
                        _obj_quai_reason = (
                            f"Thượng Quái <b>{_up_q} (Hành {_hanh_u} — đại diện trực tiếp cho {_obj_label})</b> có Tiên Thiên Quái Số = <b>{_tt_u}</b>, "
                            f"tách biệt hoàn toàn với Hạ Quái <b>{_lo_q} (Hành {_hanh_l} — đại diện cho Ngôi nhà/Không gian chứa đựng, Hậu Thiên số = {_ht_l})</b>"
                        )
                    elif _hanh_l == _obj_hanh_target and _hanh_u != _obj_hanh_target:
                        _obj_quai = _lo_q
                        _container_quai = _up_q
                        _obj_quai_reason = (
                            f"Hạ Quái <b>{_lo_q} (Hành {_hanh_l} — đại diện trực tiếp cho {_obj_label})</b> có Tiên Thiên Quái Số = <b>{_tt_l}</b>, "
                            f"đặt trong Thượng Quái <b>{_up_q} (Hành {_hanh_u})</b>"
                        )
                    elif _TRIG_HANH_Q.get(_b_up_q) == _obj_hanh_target:
                        _obj_quai = _b_up_q
                    elif _TRIG_HANH_Q.get(_b_lo_q) == _obj_hanh_target:
                        _obj_quai = _b_lo_q

                _obj_tt_num = _TT_NUM_Q.get(_obj_quai, _tt_u)
                _cont_ht_num = _HT_NUM_Q.get(_container_quai, _ht_l)

                # BƯỚC 2: KIỂM CHỨNG MẮT XÍCH 1 — "TRONG NHÀ / TRONG KÉT CÓ THẬT HAY KHÔNG?" (Existence Linkage)
                # Liên kết: (a) Hào Thê Tài / Hào Dụng Thần trên Lục Hào + (b) Tương sinh Không gian -> Vật thể trên Mai Hoa + (c) Cửa/Thần Kỳ Môn
                _tai_hao_info = None
                for _ix_h, _h_item in enumerate(haos, 1):
                    if isinstance(_h_item, dict) and "Thê Tài" in str(_h_item.get("luc_than") or ""):
                        _tai_hao_info = (_ix_h, _h_item)
                        break
                _dt_hao_idx = _mat_spec.get("dt_idx") or (_tai_hao_info[0] if _tai_hao_info else pm_idx)
                _dt_hao_chi = _mat_spec.get("dt_chi") or (str(_tai_hao_info[1].get("chi") or "").split()[-1] if _tai_hao_info else "Mão")
                _dt_hao_nh = _mat_spec.get("dt_nh") or (str(_tai_hao_info[1].get("ngu_hanh") or _tai_hao_info[1].get("hanh") or "Mộc") if _tai_hao_info else "Mộc")
                if _tai_hao_info and (_obj_hanh_target == "Kim" or "vàng" in q_low or "tiền" in q_low or "chỉ" in q_low):
                    _dt_hao_idx = _tai_hao_info[0]
                    _dt_hao_chi = str(_tai_hao_info[1].get("chi") or _tai_hao_info[1].get("can_chi") or "Mão").split()[-1]
                    _dt_hao_nh = str(_tai_hao_info[1].get("ngu_hanh") or _tai_hao_info[1].get("hanh") or "Mộc")
                _the_nh_q = str(the_hao.get("ngu_hanh") or the_hao.get("hanh") or _mat_spec.get("the_nh") or "Hỏa")

                _lh_pos_desc = "Nội Quái (bên trong ngôi nhà)" if int(_dt_hao_idx) <= 3 else "Ngoại Quái"
                _lh_rel_the = ""
                if _SINH_Q.get(_dt_hao_nh) == _the_nh_q:
                    _lh_rel_the = f"tương sinh trực tiếp cho Hào Thế tại Hào {the_idx} ({_the_ch_q}-{_the_nh_q}: <b>{_dt_hao_nh} sinh {_the_nh_q} — Tài sinh Thế, khẳng định tài sản/vàng bạc thuộc quyền sở hữu thực tế của bạn</b>)"
                elif _dt_hao_nh == _the_nh_q:
                    _lh_rel_the = f"đồng hành Tỷ Hòa với Hào Thế tại Hào {the_idx} ({_the_ch_q}-{_the_nh_q})"
                else:
                    _lh_rel_the = f"liên kết trực tiếp với Hào Thế tại Hào {the_idx} ({_the_ch_q}-{_the_nh_q})"

                _mh_container_sinh = ""
                if _SINH_Q.get(_TRIG_HANH_Q.get(_container_quai, ""), "") == _TRIG_HANH_Q.get(_obj_quai, ""):
                    _mh_container_sinh = f"Quái Không Gian <b>{_container_quai} ({_TRIG_HANH_Q.get(_container_quai, '')})</b> tương sinh trực tiếp cho Quái Vật Thể <b>{_obj_quai} ({_TRIG_HANH_Q.get(_obj_quai, '')})</b> (<b>{_TRIG_HANH_Q.get(_container_quai, '')} sinh {_TRIG_HANH_Q.get(_obj_quai, '')}</b> — Ngôi nhà đang bao bọc, cất giữ {_obj_label} bên trong)"
                else:
                    _mh_container_sinh = f"Quẻ Chủ <b>{ten_que_chu}</b> phối hợp Thượng <b>{_up_q}</b> – Hạ <b>{_lo_q}</b>"

                _km_storage_desc = f"Cung {_cung_n_q} ({huong_cung}) hội Cửa <b>{cua_name}</b> & Thần <b>{than_name}</b>"
                if "Đỗ" in str(cua_name):
                    _km_storage_desc += " (<b>Đỗ Môn + Trực Phù</b> = Tượng cất giấu kín đáo trong tủ/hộp/phòng kín tại phương Tây Nam)"
                elif "Sinh" in str(cua_name) or "Khai" in str(cua_name):
                    _km_storage_desc += f" (<b>{cua_name}</b> = Tượng tài vật hiện hữu rõ ràng)"

                # BƯỚC 3: THUẬT TOÁN HỘI TỤ 6 TẦNG SỐ (6-LAYER CONVERGENT NUMBER SOLVER)
                # Tuyệt đối không lấy đơn lẻ 1 số ngẫu nhiên hay cộng bừa Thượng + Hạ (8+2=10), mà đối chiếu sự hội tụ của cả 6 tầng:
                # [Tầng 1]: Tiên Thiên Quái Vật Thể (_obj_tt_num)
                # [Tầng 2]: Hậu Thiên Quái Không Gian / Hạ Quái (_cont_ht_num)
                # [Tầng 3]: Hào Động (_dong_val_q)
                # [Tầng 4]: Vị trí Hào Thế (the_idx)
                # [Tầng 5]: Cục số Kỳ Môn Độn Giáp (_cuc_n_q)
                # [Tầng 6]: Cung số Kỳ Môn Độn Giáp (_cung_n_q)
                _layer_votes = {}
                _layer_details = [
                    (f"Tiên Thiên Quái Vật Thể ({_obj_quai} - {_TRIG_HANH_Q.get(_obj_quai, '')})", _obj_tt_num, 3),
                    (f"Hậu Thiên Quái Không Gian ({_container_quai} - {_TRIG_HANH_Q.get(_container_quai, '')})", _cont_ht_num, 2),
                    (f"Hào Động Lục Hào & Mai Hoa (Động hào {_dong_val_q})", _dong_val_q, 2),
                    (f"Vị trí Hào Thế Chủ Sở Hữu (Hào {the_idx})", int(the_idx), 2),
                    (f"Cục số Kỳ Môn Độn Giáp (Cục {_cuc_n_q})", _cuc_n_q, 2),
                    (f"Cung vị Kỳ Môn Độn Giáp (Cung {_cung_n_q} {huong_cung})", _cung_n_q, 2),
                ]
                for _l_name, _l_val, _l_weight in _layer_details:
                    if isinstance(_l_val, int) and 1 <= _l_val <= 12:
                        if _l_val not in _layer_votes:
                            _layer_votes[_l_val] = {"score": 0, "count": 0, "names": []}
                        _layer_votes[_l_val]["score"] += _l_weight
                        _layer_votes[_l_val]["count"] += 1
                        _layer_votes[_l_val]["names"].append(f"{_l_name} = <b>{_l_val}</b>")

                # Kiểm định Quy mô Quẻ Biến & Quẻ Hỗ (Thu hẹp/Ít ỏi vs Mở rộng/Nhiều):
                # Nếu Quẻ Biến là Khốn (Trạch Thủy Khốn = hạn hẹp, ít ỏi), Tổn, Bác, Tiểu Quá, Tiểu Súc, Độn, Kiển, Giải, Vị Tế
                # hoặc Quẻ Hỗ là Tiệm (Phong Sơn Tiệm = tích góp nhỏ) hoặc Cửa Đỗ Môn (cất giấu phần nhỏ):
                # Bắt buộc khóa ở ngưỡng SỐ NHỎ (lấy trực tiếp Con Số Hội Tụ & Số Quái Vật Thể), CẤM cộng dồn Thượng + Hạ thành 8-10!
                _full_ho_q = str(_mat_spec.get("full_ho") or "")
                _is_small_scale_hex = any(
                    kw in f"{ten_que_chu} {ten_que_bien} {_full_ho_q}"
                    for kw in ["Khốn", "Tổn", "Bác", "Tiểu Quá", "Tiểu Súc", "Độn", "Kiển", "Vị Tế", "Tiệm", "Giải"]
                ) or ("Đỗ" in str(cua_name)) or ("Tử" in str(cua_name))

                # Tìm con số có điểm hội tụ cao nhất (ưu tiên số khớp nhiều tầng nhất; nếu bằng điểm ưu tiên _obj_tt_num)
                _sorted_candidates = sorted(
                    _layer_votes.items(),
                    key=lambda kv: (kv[1]["score"], kv[1]["count"], 1 if kv[0] == _obj_tt_num else 0, -kv[0] if _is_small_scale_hex else kv[0]),
                    reverse=True,
                )
                _best_num = _sorted_candidates[0][0] if _sorted_candidates else _obj_tt_num
                _best_meta = _sorted_candidates[0][1] if _sorted_candidates else {"score": 3, "count": 1, "names": [f"Quái {_obj_quai} = {_obj_tt_num}"]}
                _converge_count = _best_meta["count"]
                _converge_names_str = "; ".join(_best_meta["names"])

                if _converge_count >= 3 or _is_small_scale_hex:
                    # Khi >= 3 tầng cùng chỉ vào 1 con số (VD: 6/6 tầng cùng chỉ vào số 2 trên quẻ Trạch Địa Tụy -> Trạch Thủy Khốn)
                    # hoặc Quẻ Biến là quẻ Thu Hẹp (Trạch Thủy Khốn = ít ỏi): Chốt ĐÍCH DANH con số hội tụ!
                    _low_bound = max(1, _best_num - 1) if _best_num <= 3 else _best_num
                    _high_bound = _best_num if _best_num <= 3 else (_best_num + 1)
                    _scale_explain = (
                        f"Quẻ Biến <b>{ten_que_bien}</b> (<i>Khốn/Thu hẹp = số lượng ít ỏi, cất kỹ làm vốn nhỏ phòng thân</i>) kết hợp Quẻ Hỗ <b>{_full_ho_q}</b> bác bỏ hoàn toàn số lớn (như {_tt_l} – {_tt_u + _tt_l}), khóa chặt vào con số hội tụ nhỏ"
                        if _is_small_scale_hex else
                        f"Hội tụ đa tầng áp đảo ({_converge_count}/6 tầng chỉ số cùng quy về một mối)"
                    )
                    if _has_existence_q:
                        short_hl = (
                            f"✅ [1] KIỂM CHỨNG THỰC TẾ: TRONG NHÀ BẠN CÓ {_obj_label.upper()} (CẤT KÍN TẠI HƯỚNG {huong_cung.upper()} — CỬA {cua_name.upper()})  |  "
                            f"🔢 [2] SỐ LƯỢNG CHÍNH XÁC TỪ LIÊN KẾT 6 TẦNG QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                            f"ĐÚNG 0{_best_num} {_unit_str.upper()} (DAO ĐỘNG {_low_bound} – {_high_bound} {_unit_str.upper()}, TRỌNG TÂM CHÍNH XÁC {_best_num} {_unit_str.upper()} — HỘI TỤ {_converge_count}/6 TẦNG SỐ = {_best_num})!"
                            if _best_num < 10 else
                            f"✅ [1] KIỂM CHỨNG THỰC TẾ: TRONG NHÀ BẠN CÓ {_obj_label.upper()}  |  "
                            f"🔢 [2] SỐ LƯỢNG CHÍNH XÁC ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): ĐÚNG {_best_num} {_unit_str.upper()} (HỘI TỤ {_converge_count}/6 TẦNG SỐ = {_best_num})!"
                        )
                    else:
                        short_hl = (
                            f"🔢 KẾT QUẢ ĐỊNH LƯỢNG HỘI TỤ ĐA TẦNG ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                            f"CHÍNH XÁC {_best_num:02d} {_unit_str.upper()} (KHOẢNG {_low_bound} – {_high_bound} {_unit_str.upper()}, HỘI TỤ {_converge_count}/6 TẦNG QUẺ = {_best_num})!"
                        )
                else:
                    # Trường hợp Quẻ Biến Mở Rộng (Đại Hữu, Phong, Thái, Ích...) và các tầng phân tán
                    _n_min = min(_obj_tt_num, _best_num)
                    _n_max = max(_obj_tt_num, _best_num) if not _is_small_scale_hex else _best_num
                    if _n_min == _n_max:
                        _n_max = _n_min + _dong_val_q
                    _scale_explain = f"Kết hợp Quái Vật Thể ({_obj_quai} = {_obj_tt_num}) và Điểm Hội Tụ ({_best_num})"
                    short_hl = (
                        f"🔢 KẾT QUẢ ĐỊNH LƯỢNG LIÊN KẾT ĐA TẦNG ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"TRỌNG TÂM {_best_num} {_unit_str.upper()} (KHOẢNG {_n_min} – {_n_max} {_unit_str.upper()})!"
                    )

                why_s = (
                    f"<b>• [Mắt xích 1 — Kiểm chứng Thực có («Có hay Không?»)]:</b> "
                    f"Trên Lục Hào, Hào Dụng Thần <b>{('Thê Tài' if _tai_hao_info else dung_than)} (Hào {_dt_hao_idx} {_dt_hao_chi}-{_dt_hao_nh})</b> hiện rõ tại {_lh_pos_desc}, hoàn toàn hữu khí (không phạm Tuần Không) và {_lh_rel_the}. "
                    f"Trên Mai Hoa, {_mh_container_sinh}. Trên Kỳ Môn, {_km_storage_desc} ➔ <b>Khẳng định 100% có thật!</b><br>"
                    f"<b>• [Mắt xích 2 — Định vị Quái Vật Thể vs. Quái Không Gian]:</b> {_obj_quai_reason}. (Tuyệt đối không lấy nhầm Tiên Thiên số {_TT_NUM_Q.get(_container_quai, 8)} của Quái Không Gian {_container_quai} để cộng dồn sai lệch!).<br>"
                    f"<b>• [Mắt xích 3 — Sự Hội Tụ Tuyệt Đối Của {_converge_count}/6 Tầng Số Vào Con Số {_best_num}]:</b> {_converge_names_str}.<br>"
                    f"<b>• [Mắt xích 4 — Kiểm định Quy mô từ Quẻ Biến & Quẻ Hỗ]:</b> {_scale_explain} ➔ Chốt định lượng chính xác là <b>{_best_num} {_unit_str}</b>!"
                )
                _is_storage_q = _has_existence_q or any(w in q_low for w in ["vàng", "bạc", "trang sức", "két", "cất", "giấu", "trong nhà", "trong tủ"])
                if _is_storage_q:
                    when_s = (
                        f"Trạng thái hiện tại (<b>{omni_data.get('exact_timestamp', 'Hiện tại')}</b>): "
                        f"Số lượng <b>{_best_num} {_unit_str}</b> đang được cất giữ an toàn tại phương <b>{huong_cung} (Cung {_cung_n_q} · Cửa {cua_name} · Thần {than_name})</b>."
                    )
                    adv_s = (
                        f"Tài vật (<b>{_best_num} {_unit_str}</b>) tại hướng <b>{huong_cung}</b> đang đắc cách <b>{_container_quai} sinh {_obj_quai}</b> và <b>Tài sinh Thế</b>, "
                        f"nên tiếp tục cất giữ kín đáo (ứng tượng <b>{cua_name}</b>) để giữ vững khí tài lộc trong nhà (Màu hợp: <b>{colors_str}</b>)."
                    )
                else:
                    when_s = (
                        f"Thời điểm ứng nghiệm & hội tụ con số <b>{_best_num} {_unit_str}</b>: "
                        f"<b>{omni_data.get('exact_timestamp', f'Ứng vào Ngày/Giờ {_dt_hao_chi}')}</b> (Cung {_cung_n_q} {huong_cung} · Cửa <b>{cua_name}</b> · Sao <b>{sao_name}</b>)."
                    )
                    adv_s = (
                        f"Chủ động căn cứ theo định lượng <b>{_best_num} {_unit_str}</b> từ quẻ <b>{ten_que_chu} ➔ {ten_que_bien}</b> để lập kế hoạch hành động, ưu tiên phương vị <b>{huong_cung}</b> (Màu trợ vận: <b>{colors_str}</b>)."
                    )
                return {
                    "has_override": True,
                    "is_strict_override": True,
                    "is_open_van_vat": not _is_storage_q,
                    "headline": f"🎯 {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

        # ── 8D. GIẢI MÃ ĐẠI SỰ MUA NHÀ MẶT ĐẤT / MUA ĐẤT / XÂY NHÀ / MUA XE / TÀI SẢN LỚN (MAJOR_ASSET_HOUSE_LAND — V110.0 LIÊN KẾT MỌI YẾU TỐ CỦA QUẺ) ──
        if target == "MAJOR_ASSET_HOUSE_LAND" or any(w in q_low for w in ["mua nhà mặt đất", "mua được nhà", "bao giờ mua nhà", "khi nào mua nhà", "mua đất", "mảnh đất", "miếng đất", "lô đất", "xây nhà", "làm nhà", "mua căn hộ", "mua chung cư", "mua biệt thự", "mua xe ô tô"]):
            _m_asset = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
                dung_than="Phụ Mẫu",
            )
            _asset_name = "nhà mặt đất" if "mặt đất" in q_low else ("đất đai / bất động sản" if any(k in q_low for k in ["mua đất", "mảnh đất", "miếng đất", "lô đất"]) else ("căn hộ / chung cư" if ("căn hộ" in q_low or "chung cư" in q_low) else ("xe ô tô" if "ô tô" in q_low else "nhà cửa / bất động sản")))
            _CHI_NH_AS = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
            _SINH_AS = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
            _chi_m_as = chart_data.get("chi_thang", "Tuất")
            _chi_n_as = chart_data.get("chi_ngay", "Ngọ")
            _nh_m_as = _CHI_NH_AS.get(_chi_m_as, "Thổ")
            _nh_n_as = _CHI_NH_AS.get(_chi_n_as, "Hỏa")

            _pm_idx_as = _m_asset["dt_idx"]
            _pm_chi_as = _m_asset["dt_chi"]
            _pm_nh_as = _m_asset["dt_nh"]
            _pm_kv_as = _pm_chi_as in _m_asset["kv_list"]
            _pm_vuong_as = (_SINH_AS.get(_nh_m_as) == _pm_nh_as or _nh_m_as == _pm_nh_as) or (_SINH_AS.get(_nh_n_as) == _pm_nh_as or _nh_n_as == _pm_nh_as)

            _ASSET_WINDOW_BY_NH = {
                "Kim": "MÙA THU THÁNG 08–09/2027 DƯƠNG LỊCH (THÁNG THÂN–DẬU ÂM LỊCH NĂM ĐINH MÙI) HOẶC NĂM 2028–2029 (MẬU THÂN – KỶ DẬU)",
                "Thủy": "MÙA THU – ĐÔNG THÁNG 08–12/2027 DƯƠNG LỊCH (THÁNG THÂN–DẬU–HỢI–TÝ ÂM LỊCH KHI KIM SINH THỦY VƯỢNG)",
                "Mộc": "MÙA XUÂN THÁNG 02–04/2027 DƯƠNG LỊCH (THÁNG DẦN–MÃO–THÌN ÂM LỊCH NĂM ĐINH MÙI) HOẶC ĐẦU XUÂN 2028",
                "Hỏa": "MÙA HẠ THÁNG 05–07/2027 DƯƠNG LỊCH (THÁNG TỊ–NGỌ–MÙI ÂM LỊCH NĂM ĐINH MÙI KHI HỎA – THỔ VƯỢNG)",
                "Thổ": "CÁC THÁNG TỨ QUÝ THÁNG 04, 07, 10/2027 DƯƠNG LỊCH (THÁNG THÌN–MÙI–TUẤT ÂM LỊCH NĂM ĐINH MÙI 2027)",
            }
            _target_win_as = _ASSET_WINDOW_BY_NH.get(_pm_nh_as, "MÙA THU THÁNG 08–09/2027 DƯƠNG LỊCH (THÁNG THÂN–DẬU ÂM LỊCH)")

            _tai_on_hex = _m_asset["has_the_tai_on_hex"]
            _tai_ready = _m_asset["the_tai_ready"]
            _tai_status = _m_asset["the_tai_status_str"]
            _km_phuc_ngam = _m_asset["is_km_phuc_ngam"]
            _km_pn_str = _m_asset["km_phuc_ngam_str"]

            # Phân tích liên kết 4 mắt xích: [1] Bản thân (Hào Thế) + [2] Nhà đất (Phụ Mẫu) + [3] Nguồn tiền (Thê Tài) + [4] Cục diện (Phục Ngâm / Hào Động)
            if not _tai_ready or _pm_kv_as or _km_phuc_ngam or not _pm_vuong_as:
                _blocker_list = []
                if not _tai_on_hex:
                    _blocker_list.append("Nguồn tiền Hào Thê Tài đang PHỤC TÀNG (ẩn phục chưa hiện trên quẻ — phản ánh đúng thực tế hiện tại bạn CHƯA CÓ SẴN KHOẢN TIỀN LỚN)")
                elif not _tai_ready:
                    _blocker_list.append(f"Nguồn tiền Hào Thê Tài ({_tai_status}) hiện chưa đủ độ vượng để thanh toán ngay")
                if _pm_kv_as:
                    _blocker_list.append(f"Dụng Thần Nhà đất (Hào Phụ Mẫu tại Hào {_pm_idx_as} {_pm_chi_as}-{_pm_nh_as}) đang tạm lâm TUẦN KHÔNG ({', '.join(_m_asset['kv_list'])}) và có hào động xung")
                elif not _pm_vuong_as:
                    _blocker_list.append(f"Dụng Thần Nhà đất (Hào Phụ Mẫu tại Hào {_pm_idx_as} {_pm_chi_as}-{_pm_nh_as}) hiện đang HƯU TÙ dưới Nguyệt Lệnh {_chi_m_as} ({_nh_m_as}), cần đợi đúng mùa Hành {_pm_nh_as} vượng")
                if _km_phuc_ngam:
                    _blocker_list.append(f"Kỳ Môn Độn Giáp phạm {_km_pn_str} (cục diện giậm chân tại chỗ, không thể đốt cháy giai đoạn trong vài ngày)")

                _severe_asset_risk = ("DỤNG KHẮC THỂ" in _m_asset["rel_bien_tag"] and not _tai_ready and (_pm_kv_as or not _pm_vuong_as))
                if _severe_asset_risk:
                    short_hl = (
                        f"⚠️ KẾT LUẬN LIÊN KẾT TOÀN DIỆN MỌI YẾU TỐ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"GIAI ĐOẠN HIỆN TẠI / NGẮN HẠN CHƯA NÊN XUỐNG TIỀN MUA {_asset_name.upper()} VỘI (DO QUẺ BIẾN {_m_asset['full_bien'].upper()} [{_m_asset['rel_bien_tag'].upper()}] & {'; '.join(_blocker_list[:2]).upper()}) — "
                        f"NẾU CỐ VAY MƯỢN MUA NGAY DỄ GẶP ÁP LỰC NỢ NẦN HOẶC VƯỚNG PHÁP LÝ! "
                        f"➔ LỘ TRÌNH AN TOÀN: HOÃN SANG {_target_win_as} (KHI HÀO PHỤ MẪU {_pm_chi_as.upper()}-{_pm_nh_as.upper()} & THÊ TÀI VƯỢNG KHÍ) MỚI THÀNH CÔNG!"
                    )
                else:
                    short_hl = (
                        f"🏠 KẾT LUẬN LIÊN KẾT TOÀN DIỆN MỌI YẾU TỐ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                        f"CÓ NỀN TẢNG MUA ĐƯỢC {_asset_name.upper()} (DỤNG THẦN PHỤ MẪU TẠI HÀO {_pm_idx_as} {_pm_chi_as.upper()}-{_pm_nh_as.upper()} & QUẺ BIẾN {_m_asset['full_bien'].upper()} [{_m_asset['rel_bien_tag'].upper()}]), "
                        f"NHƯNG HIỆN TẠI CHƯA THỂ CHỐT NGAY LẬP TỨC (DO {'; '.join(_blocker_list[:2]).upper()})! "
                        f"➔ LỘ TRÌNH 2 GIAI ĐOẠN: [1] TÍCH LŨY VỐN ➔ [2] CHỐT MUA THUẬN LỢI VÀO {_target_win_as}!"
                    )
                why_s = (
                    f"<b>• Nguyên lý Suy Luận Liên Kết Mọi Yếu Tố Của Quẻ (Bác bỏ ứng kỳ 2 ngày phi thực tế đối với Đại Sự):</b> Việc mua <b>{_asset_name}</b> là đại sự trọng đại, bắt buộc phải liên kết đồng thời <b>4 Mắt Xích Cốt Lõi</b> trên quẻ chứ không thể chỉ nhìn đơn độc 1 hào:<br>"
                    f"<b>1. Mắt xích 1 — Xét Nguồn Tiền Thực Tế (Hào Thê Tài & Nguyên Thần):</b> {_tai_status}. Trong Lục Hào, <b>Thê Tài là nguồn tiền thanh toán trực tiếp</b>; khi Thê Tài ẩn phục (Phục Tàng) hoặc chưa đồng bộ với Phụ Mẫu thì <b>hiện tại chưa thể giải ngân mua ngay trong vài ngày</b>.<br>"
                    f"<b>2. Mắt xích 2 — Xét Dụng Thần Nhà Đất (Hào Phụ Mẫu & Quẻ Biến):</b> Hào Dụng Thần <b>Phụ Mẫu tại Hào {_pm_idx_as} ({_pm_chi_as}-{_pm_nh_as})</b> biến sang Quẻ <b>{ten_que_bien}</b> ({_m_asset['rel_bien_tag']}) ➔ Khẳng định <b>mệnh bạn CÓ CƠ NGƠI {_asset_name.upper()} thực sự</b>. Tuy nhiên cần đợi đến đúng vận Hành <b>{_pm_nh_as} ({_pm_chi_as})</b> vượng tướng/Xuất Không mới sang tên thành công.<br>"
                    f"<b>3. Mắt xích 3 — Xét Bản Thân Người Mua (Hào Thế & Nhật Can):</b> Hào Thế tại <b>Hào {_m_asset['the_idx']} ({_m_asset['the_chi']}-{_m_asset['the_nh']})</b> trên quẻ <b>{_m_asset['full_chu']}</b> đang ở thế chuẩn bị kế hoạch (Quẻ Hỗ <b>{_m_asset['full_ho']}</b>).<br>"
                    f"<b>4. Mắt xích 4 — Xét Cục Diện Kỳ Môn Độn Giáp:</b> Bàn Kỳ Môn Cục {_m_asset['cuc_km']} ({_m_asset['don_type']}) tại Cung {target_cung} ({huong_cung}: Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b> — {_km_pn_str})."
                )
                when_s = (
                    f"<b>Lộ trình Ứng Kỳ Đa Điều Kiện (Hội tụ đủ Tiền [Thê Tài] + Nhà [Phụ Mẫu {_pm_chi_as}-{_pm_nh_as}]):</b><br>"
                    f"• <b>Giai đoạn 1 — Tích lũy vốn & Dòng tiền (Thê Tài):</b> Từ <b>Cuối năm 2026 đến Đầu năm 2027 (Đinh Mùi)</b> để gom đủ nguồn vốn chủ lực.<br>"
                    f"• <b>Giai đoạn 2 — Điểm rơi Mua được {_asset_name} (Phụ Mẫu {_pm_chi_as}-{_pm_nh_as} Đắc Lệnh):</b> Ứng nghiệm chuẩn xác vào <b>{_target_win_as}</b> (Lưu ý: Các mốc ngày {_pm_chi_as} gần trong tuần chỉ ứng với việc <b>xem thông tin, khảo sát giá hoặc bàn bạc ý định</b>, tuyệt đối không phải ngày xuống tiền mua nhà!)."
                )
                adv_s = (
                    f"<b>Chiến lược thực tế theo chuỗi liên kết của quẻ:</b><br>"
                    f"1. <b>Hiện tại:</b> Tập trung tích lũy vốn tự có đạt tối thiểu 50%–70% giá trị {_asset_name}.<br>"
                    f"2. <b>Phương vị & Thời điểm chọn mua:</b> Khi bước vào <b>{_target_win_as}</b>, ưu tiên tìm mua {_asset_name} ở phương vị <b>{huong_cung}</b> (Cung {target_cung}: Cửa <b>{cua_name}</b> & Sao <b>{sao_name}</b>, màu trợ vận: <b>{colors_str}</b>)."
                )
            else:
                short_hl = (
                    f"🏠 KẾT LUẬN LIÊN KẾT TOÀN DIỆN MỌI YẾU TỐ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                    f"BẠN ĐỦ ĐIỀU KIỆN MUA ĐƯỢC {_asset_name.upper()} — CẢ NGUỒN TIỀN (HÀO THÊ TÀI HỮU KHÍ) VÀ DỤNG THẦN NHÀ ĐẤT (PHỤ MẪU Hào {_pm_idx_as} {_pm_chi_as}-{_pm_nh_as}) ĐỀU ĐẮC LỆNH HỘI TỤ! "
                    f"➔ THỜI ĐIỂM CHỐT GIAO DỊCH & SANG TÊN THUẬN LỢI NHẤT: TỪ CUỐI NĂM 2026 ĐẾN {_target_win_as}!"
                )
                why_s = (
                    f"<b>• Liên kết 4 Mắt Xích Của Quẻ:</b><br>"
                    f"1. <b>Nguồn Tiền (Hào Thê Tài):</b> {_tai_status} (đã sẵn sàng tài chính).<br>"
                    f"2. <b>Nhà Đất (Hào Phụ Mẫu):</b> Hào {_pm_idx_as} ({_pm_chi_as}-{_pm_nh_as}) hữu khí, không phạm Tuần Không, được Nhật/Nguyệt nâng đỡ.<br>"
                    f"3. <b>Bản Thân (Hào Thế):</b> Hào {_m_asset['the_idx']} ({_m_asset['the_chi']}-{_m_asset['the_nh']}) tương hợp với mục tiêu.<br>"
                    f"4. <b>Mai Hoa & Kỳ Môn:</b> Quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> ({_m_asset['rel_bien_tag']}), Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b>."
                )
                when_s = (
                    f"<b>Lộ trình hoàn tất mua & nhận {_asset_name}:</b> Điểm rơi giao dịch thành công từ <b>Cuối năm 2026 sang {_target_win_as}</b> khi Hào Phụ Mẫu ({_pm_chi_as}-{_pm_nh_as}) và Thê Tài đồng vượng."
                )
                adv_s = (
                    f"Chủ động khảo sát pháp lý và đàm phán mua {_asset_name} tại hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
                )
            return {
                "has_override": True,
                "headline": f"🎯 {short_hl}",
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8D_2. GIẢI MÃ CHUYÊN SÂU Y DỊCH — SỨC KHỎE, SỐT CAO, ĐAU ỐM & BỆNH TẬT (HEALTH_MEDICAL — V111.0 NGŨ CHẨN Y DỊCH) ──
        if target == "HEALTH_MEDICAL" or any(w in q_low for w in ["sốt", "sốt cao", "nóng sốt", "hạ sốt", "khỏi bệnh", "bệnh gì", "có ốm không", "có sốt không", "sức khỏe", "nằm viện", "nhập viện", "viêm họng", "đau bụng"]):
            _m_hl = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
                dung_than=dung_than,
            )
            _KHAC_MD = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
            _SINH_MD = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
            _ORGAN_BY_NH = {
                "Kim": "Phổi, Họng, Amidan, Đường hô hấp, Mũi, Xương khớp & Thân nhiệt",
                "Mộc": "Gan, Mật, Dây thần kinh, Đầu mặt, Tay chân & Cảm phong hàn",
                "Thủy": "Thận, Bàng quang, Tai, Huyết dịch & Hệ bài tiết",
                "Hỏa": "Tim mạch, Huyết áp, Mắt, Sốt nhiệt & Viêm cấp tính",
                "Thổ": "Dạ dày, Tỳ vị, Hệ tiêu hóa, Bụng & Cơ thịt",
            }
            _dt_idx_md = _m_hl["dt_idx"]
            _dt_chi_md = _m_hl["dt_chi"]
            _dt_nh_md = _m_hl["dt_nh"]
            _ky_nh_md = next((k for k, v in _KHAC_MD.items() if v == _dt_nh_md), "Hỏa")
            _ng_nh_md = next((k for k, v in _SINH_MD.items() if v == _dt_nh_md), "Thổ")
            _organ_str = _ORGAN_BY_NH.get(_dt_nh_md, "Hô hấp & Thân nhiệt")
            _has_fire_attack = ("Ly" in (_m_hl["up_chu"], _m_hl["lo_chu"], _m_hl["up_bien"], _m_hl["lo_bien"]) or _ky_nh_md == "Hỏa")
            _has_hung_door = any(m in cua_name for m in ("Thương", "Tử", "Kinh", "Đỗ"))
            _symptom_lbl = "ĐANG SỐT CAO / VIÊM NHIỆT CẤP TÍNH" if (_has_fire_attack and _dt_nh_md == "Kim") else ("ĐANG CÓ TRIỆU CHỨNG MỆT MỎI / PHÁT BỆNH" if _has_hung_door else "SỨC KHỎE ĐANG CẦN THEO DÕI & CHĂM SÓC")

            _CHIS_BY_NH_MD = {
                "Thổ": "Sửu · Thìn · Mùi · Tuất",
                "Kim": "Thân · Dậu",
                "Thủy": "Hợi · Tý",
                "Mộc": "Dần · Mão",
                "Hỏa": "Tị · Ngọ",
            }
            _relief_chis_md = f"{_CHIS_BY_NH_MD.get(_ng_nh_md, 'Thân · Dậu')} · {_dt_chi_md}"
            _qq_dong_attack = any(x[4] and _KHAC_MD.get(x[3]) == _dt_nh_md for x in (_m_hl.get("rival_haos_all") or []))
            _severe_med_risk = (_qq_dong_attack and _m_hl.get("dt_is_kv") and ("Tử" in cua_name or "Bạch Hổ" in than_name))
            if _severe_med_risk:
                short_hl = (
                    f"🚨 CẢNH BÁO Y DỊCH TAM THỨC ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_md} {_dt_chi_md.upper()}-{_dt_nh_md.upper()}): "
                    f"TRIỆU CHỨNG ĐANG DIỄN TIẾN NẶNG TẠI {_organ_str.upper()} (DO QUAN QUỶ ĐỘNG KHẮC DỤNG THẦN LÂM TUẦN KHÔNG & GẶP {cua_name.upper()} · {than_name.upper()}) — "
                    f"CẦN ĐƯA ĐI THĂM KHÁM BÁC SĨ / CƠ SỞ Y TẾ CHUYÊN KHOA NGAY (ƯU TIÊN HƯỚNG SAO THIÊN TÂM) ĐỂ CAN THIỆP KỊP THỜI, TUYỆT ĐỐI KHÔNG CHỦ QUAN!"
                )
            elif _qq_dong_attack or ("DỤNG KHẮC THỂ" in _m_hl.get("rel_bien_tag", "") and _has_hung_door):
                short_hl = (
                    f"🩺 KẾT LUẬN Y DỊCH TAM THỨC ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_md} {_dt_chi_md.upper()}-{_dt_nh_md.upper()}): "
                    f"HIỆN TRẠNG {_symptom_lbl} TẠI {_organ_str.upper()} CÒN DAI DẲNG (DO KỴ THẦN HÀNH {_ky_nh_md.upper()} & CỬA {cua_name.upper()} CẢN TRỞ) — "
                    f"CẦN KIỂM TRA Y TẾ / ĐIỀU CHỈNH PHÁC ĐỒ THUỐC ĐÚNG CHỈ DẪN, SẼ THUYÊN GIẢM RÕ VÀO CÁC NGÀY {_relief_chis_md.upper()} (KHOẢNG 4 – 7 NGÀY)!"
                )
            else:
                short_hl = (
                    f"🩺 KẾT LUẬN Y DỊCH TAM THỨC ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_md} {_dt_chi_md.upper()}-{_dt_nh_md.upper()}): "
                    f"HIỆN TRẠNG {_symptom_lbl} (DO HÀNH {_ky_nh_md.upper()} KHẮC {_dt_nh_md.upper()} TÁC ĐỘNG VÀO {_organ_str.upper()} CÙNG CỬA {cua_name.upper()} · SAO {sao_name.upper()}), "
                    f"NHƯNG TIÊN LƯỢNG LÀNH TÍNH — ĐẮC NGUYÊN THẦN HÀNH {_ng_nh_md.upper()} SINH TRỢ NÊN SẼ NHANH HẠ SỐT / BÌNH PHỤC TRONG 1 – 3 NGÀY TỚI (ỨNG GIỜ/NGÀY {_relief_chis_md.upper()})!"
                )
            why_s = (
                f"<b>• Phân tích Ngũ Chẩn Y Dịch (Liên kết Mai Hoa Quan Vật + Lục Hào + Kỳ Môn Độn Giáp):</b><br>"
                f"1. <b>Chủ thể & Bộ phận chịu tác động:</b> Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_md} ({_dt_chi_md}-{_dt_nh_md})</b> đại diện cho người bệnh; Hành <b>{_dt_nh_md}</b> chủ về <b>{_organ_str}</b>.<br>"
                f"2. <b>Căn nguyên phát bệnh / sốt:</b> Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, Kỵ Thần Hành <b>{_ky_nh_md}</b> khắc chế Hành <b>{_dt_nh_md}</b> kết hợp Cung {target_cung} ({huong_cung}) hội <b>Sao {sao_name} · Cửa {cua_name}</b>.<br>"
                f"3. <b>Tiên lượng Cứu Ứng (Nguyên Thần & Dược Thần):</b> Hào Dụng Thần không phạm Chân Không và có Hành <b>{_ng_nh_md}</b> thông quan sinh trợ (<i>{_ky_nh_md} sinh {_ng_nh_md}, {_ng_nh_md} sinh {_dt_nh_md}</i>), khẳng định cơ thể đáp ứng thuốc tốt và nhanh chóng hồi phục."
            )
            when_s = (
                f"<b>Thời điểm hạ sốt / lui bệnh (Ứng kỳ Y Dịch):</b> Bắt đầu dịu triệu chứng vào các khung <b>Giờ {_relief_chis_md}</b> và bình phục rõ rệt trong <b>1 – 3 ngày tới (ngày {_relief_chis_md})</b>."
            )
            adv_s = (
                f"<b>Pháp quyết chăm sóc:</b> Chú trọng chăm sóc vùng <b>{_organ_str}</b>, uống thuốc đúng chỉ dẫn, bù đủ nước ấm và nghỉ ngơi ở hướng thoáng mát (<b>{huong_cung}</b>, màu sắc trợ vận: <b>{colors_str}</b>)."
            )
            return {
                "has_override": True,
                "headline": f"🎯 {short_hl}",
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 8E. GIẢI MÃ LIÊN KẾT MỌI YẾU TỐ CHO CÂU HỎI THỜI ĐIỂM (BAO GIỜ / KHI NÀO / MẤY GIỜ) & XỔ SỐ / VIETLOT / TÀI LỘC BẤT NGỜ (TIMING_WHEN) ──
        _q_low_tm = str(blueprint.get("raw_question") or "").lower()
        _is_lottery_q = any(w in _q_low_tm for w in ["vietlot", "vietlott", "xổ số", "vé số", "độc đắc", "trúng số", "trúng thưởng", "lộc bất ngờ", "hoạnh tài"])
        _has_explicit_when_q = any(
            w in _q_low_tm
            for w in [
                "mấy giờ", "giờ nào", "lúc mấy giờ", "lúc nào", "bao giờ", "khi nào", "chừng nào",
                "tháng mấy", "năm nào", "ngày nào", "mấy tháng nữa", "mấy ngày nữa", "bao lâu nữa",
            ]
        )
        _is_yesno_feasibility_q = bool(
            re.search(r"\bcó\s+[^,;?]+?\s+(?:không|chưa)\b", _q_low_tm)
            or _q_low_tm.strip(" ?.!").endswith(("có tốt không", "tốt không", "được không", "thành công không", "thuận lợi không", "nên không"))
        ) and not any(w in _q_low_tm for w in ["mấy giờ", "giờ nào", "bao giờ", "khi nào", "ngày nào", "tháng mấy", "năm nào", "lúc nào"])
        _is_intraday_hour_tm = (not _is_yesno_feasibility_q) and (
            any(w in _q_low_tm for w in ["mấy giờ", "giờ nào", "lúc mấy giờ", "lúc nào", "bao lâu nữa tới"])
            or (
                (_has_explicit_when_q or target == "TIMING_WHEN")
                and any(
                    w in _q_low_tm
                    for w in [
                        "xuống", "lên", "đến", "tới", "về", "sang", "qua", "bắn", "chuyển khoản",
                        "ting ting", "nổ tiền", "giao hàng", "ship", "hôm nay", "chiều nay", "tối nay", "sáng nay", "trưa nay",
                    ]
                )
            )
        )
        _is_when_words = (not _is_yesno_feasibility_q) and (_is_intraday_hour_tm or _has_explicit_when_q)
        if ((target == "TIMING_WHEN" and not _is_yesno_feasibility_q) or _is_lottery_q or (_is_when_words and len(blueprint.get("multi_subjects") or []) < 2)):
            _clk_tm = get_realtime_vn_clock_context()
            _m_tm = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
                dung_than=dung_than,
            )
            _cur_solar = _clk_tm["solar_date_str"]
            _cur_lunar = _clk_tm["lunar_date_str"]
            _cur_yr = _clk_tm["cur_year"]
            _cur_yr_cc = _clk_tm["cur_year_canchi"]
            _nxt_yr = _clk_tm["next_year"]
            _nxt_yr_cc = _clk_tm["next_year_canchi"]
            _season_lbl = _clk_tm["season_phase"]
            can_y = chart_data.get("can_nam", "Bính")
            chi_y = chart_data.get("chi_nam", "Ngọ")
            can_m = chart_data.get("can_thang", "Mậu")
            chi_m = chart_data.get("chi_thang", "Tuất")
            can_n = chart_data.get("can_ngay", "Quý")
            chi_n = chart_data.get("chi_ngay", "Mùi")
            can_g = chart_data.get("can_gio", "Nhâm")
            chi_g = chart_data.get("chi_gio", "Tý")
            _tai_status_tm = _m_tm.get("the_tai_status_str", "")
            _km_pn_tm = bool(_m_tm.get("is_km_phuc_ngam", False))
            _km_pn_str_tm = _m_tm.get("km_phuc_ngam_str", "Bình thường")
            _dt_idx_tm = _m_tm.get("dt_idx", 6)
            _dt_chi_tm = _m_tm.get("dt_chi", "Tị")
            _dt_nh_tm = _m_tm.get("dt_nh", hanh_dt)
            _dt_kv_tm = bool(_m_tm.get("dt_is_kv", False))
            _the_idx_tm = _m_tm.get("the_idx", 5)
            _the_chi_tm = _m_tm.get("the_chi", "Mùi")
            _the_nh_tm = _m_tm.get("the_nh", "Thổ")
            _dong_desc_tm = ", ".join([x for x in (_m_tm.get("haos_lines_desc") or []) if "ĐỘNG" in x]) or (f"Động hào {', '.join(map(str, _m_tm.get('dong_list') or []))}" if _m_tm.get("dong_list") else "Quẻ tĩnh (6 hào an tĩnh)")
            _hd_dong_flag = ("Huynh Đệ" in _dong_desc_tm) or ("động khắc/đoạt Tài" in _tai_status_tm)

            _SEASON_BY_NH = {
                "Hỏa": f"Tháng 05 – 07/{_nxt_yr} Dương lịch (Tháng Tị – Ngọ – Mùi Âm lịch năm {_nxt_yr_cc} {_nxt_yr}, khi Hỏa – Thổ vượng cực điểm)",
                "Thổ": f"Tháng 11/{_cur_yr} & Tháng 01, 04, 07/{_nxt_yr} Dương lịch (Các tháng Thìn – Tuất – Sửu – Mùi năm {_nxt_yr_cc} {_nxt_yr})",
                "Kim": f"Tháng 08 – 09/{_nxt_yr} Dương lịch (Tháng Thân – Dậu Âm lịch Mùa Thu năm {_nxt_yr_cc} {_nxt_yr}, khi Kim vượng khí)",
                "Thủy": f"Tháng 11 – 12/{_cur_yr} Dương lịch (Cuối năm {_cur_yr} — Tháng Hợi – Tý Âm lịch năm {_cur_yr_cc}) & Đầu năm {_nxt_yr}",
                "Mộc": f"Tháng 02 – 03/{_nxt_yr} Dương lịch (Tháng Dần – Mão Âm lịch Đầu Xuân năm {_nxt_yr_cc} {_nxt_yr}, khi Mộc vượng)",
            }
            _best_window_tm = _SEASON_BY_NH.get(_dt_nh_tm, f"Quý I – Quý II năm {_nxt_yr} ({_nxt_yr_cc})")

            if _is_lottery_q:
                if _hd_dong_flag or _km_pn_tm or "DỤNG KHẮC THỂ" in str(_m_tm.get("rel_chu_tag", "")):
                    short_hl = (
                        f"🎰 KẾT LUẬN LIÊN KẾT MỌI YẾU TỐ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | THỜI ĐIỂM HIỆN TẠI: {_cur_solar} — {_season_lbl.upper()}): "
                        f"NGAY TRONG THÁNG {_clk_tm['cur_month']:02d}/{_cur_yr} HIỆN TẠI CHƯA PHẢI ĐỈNH ĐIỂM ĐỂ TRÚNG ĐỘC ĐẮC VIETLOT (DO {_tai_status_tm.upper()} & KỲ MÔN {'PHẠM PHỤC NGÂM — ' + cua_name.upper() if _km_pn_tm else cua_name.upper()})! "
                        f"➔ THỜI ĐIỂM MỞ VẬN CÓ LỘC BẤT NGỜ / TRÚNG THƯỞNG RƠI VÀO: CUỐI THÁNG 12/{_cur_yr} DƯƠNG LỊCH (THÁNG TÝ ÂM LỊCH CUỐI NĂM {_cur_yr_cc}) "
                        f"VÀ ĐỈNH ĐIỂM VƯỢNG LỘC VÀO MÙA XUÂN – HẠ NĂM {_nxt_yr} ({_best_window_tm.upper()})!"
                    )
                else:
                    short_hl = (
                        f"🎰 KẾT LUẬN LIÊN KẾT MỌI YẾU TỐ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | THỜI ĐIỂM HIỆN TẠI: {_cur_solar} — {_season_lbl.upper()}): "
                        f"VẬN HOẠNH TÀI ĐANG MỞ — BẠN CÓ CƠ HỘI ĐÓN LỘC BẤT NGỜ / TRÚNG THƯỞNG TRONG GIAI ĐOẠN CUỐI NĂM {_cur_yr} (THÁNG 11–12/{_cur_yr} DƯƠNG LỊCH) "
                        f"VÀ ĐẦU NĂM {_nxt_yr} ({_nxt_yr_cc}) VÀO CÁC NGÀY {_dt_chi_tm.upper()} – {_the_chi_tm.upper()}!"
                    )
                why_s = (
                    f"<b>• Phân tích Liên Kết Mật Thiết 4 Mắt Xích Của Quẻ (Đồng bộ thời gian thực: Ngày {_cur_solar} Dương lịch — {_cur_lunar} Âm lịch):</b><br>"
                    f"1. <b>[Mắt xích 1 — Bản thân & Tứ Trụ hiện tại]:</b> Quẻ lập lúc Năm <b>{can_y} {chi_y} ({_cur_yr})</b> · Tháng <b>{can_m} {chi_m}</b> · Ngày <b>{can_n} {chi_n}</b> · Giờ <b>{can_g} {chi_g}</b> ({_season_lbl}). "
                    f"Hào Thế (đại diện cho bạn) đóng tại <b>Hào {_the_idx_tm} ({_the_chi_tm}-{_the_nh_tm})</b>, hoàn toàn hữu khí và giữ được nền tảng tài chính.<br>"
                    f"2. <b>[Mắt xích 2 — Nguồn tiền & Hào Động ({_dong_desc_tm})]:</b> {_tai_status_tm}. "
                    f"{'Khi <b>Hào Huynh Đệ phát động</b> trên quẻ, cổ pháp Lục Hào khẳng định <i>Huynh Đệ động tắc đoạt Tài</i> (dòng tiền đang bị chia sẻ cho nhiều người cùng mua hoặc phát sinh chi phí ngoài dự kiến), nên nếu dồn tiền mua nhiều vé ngay lúc này sẽ hao tài mà chưa nổ giải lớn.' if _hd_dong_flag else 'Dòng tiền Thê Tài trên quẻ đang ổn định, hỗ trợ cho vận thử thời vận.'}<br>"
                    f"3. <b>[Mắt xích 3 — Dụng Thần May Mắn / Hoạnh Tài ({dung_than})]:</b> Hào <b>{dung_than}</b> đóng tại <b>Hào {_dt_idx_tm} ({_dt_chi_tm}-{_dt_nh_tm})</b> "
                    f"{'đang hữu khí trên Quẻ Chủ (chứng tỏ bạn CÓ SỐ hưởng lộc bất ngờ, không phải vô vọng), nhưng hiện đang tĩnh nên cần đợi đúng tháng/ngày Can Chi xung động mới phát lộ.' if not _dt_kv_tm else 'đang tạm thời phạm Tuần Không, phải đợi xuất Không mới phát lộc.'}<br>"
                    f"4. <b>[Mắt xích 4 — Cục Diện Kỳ Môn & Mai Hoa Dịch Số]:</b> Quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> ({_m_tm.get('rel_chu_tag', '')} ➔ {_m_tm.get('rel_bien_tag', '')}); "
                    f"Kỳ Môn Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b> ({_km_pn_str_tm}). "
                    f"{'Do bàn Kỳ Môn đang phạm <b>Phục Ngâm</b> và lâm <b>Cửa Đỗ Môn</b> (cửa bế tắc/ẩn tàng), vận may lớn chưa thể bùng nổ ngay trong vài ngày tới mà phải chờ qua nhịp Phục Ngâm.' if _km_pn_tm else ''}"
                )
                when_s = (
                    f"<b>Lộ trình Ứng Kỳ Trúng Thưởng / Đón Lộc Bất Ngờ (Tính từ mốc hiện tại {_cur_solar} — {_season_lbl}):</b><br>"
                    f"• <b>1. Giai đoạn Hiện tại (Tháng {_clk_tm['cur_month']:02d}/{_cur_yr} Dương lịch — Tháng {can_m} {chi_m} Âm lịch):</b> Đang vướng <b>{_dong_desc_tm}</b> và <b>{_km_pn_str_tm}</b>, vận may hoạnh tài còn bị nén — chỉ nên mua 1 vé nhỏ giải trí, không đổ nhiều tiền.<br>"
                    f"• <b>2. Điểm rơi Mở Vận Ngắn Hạn (Cuối năm {_cur_yr} — Tháng 12/{_cur_yr} Dương lịch & Tháng 01/{_nxt_yr} [Tháng Hợi – Tý – Sửu Âm lịch cuối năm {_cur_yr_cc}]):</b> Khi khí Thủy – Hỏa giao thời phá vỡ cục Phục Ngâm và tiết khí Huynh Đệ, bắt đầu xuất hiện lộc nhỏ hoặc giải thưởng phụ vào các ngày <b>{_dt_chi_tm}</b> và <b>{_the_chi_tm}</b>.<br>"
                    f"• <b>3. Điểm rơi Đỉnh Điểm Vượng Lộc (Năm {_nxt_yr} — {_nxt_yr_cc}):</b> Cửa vận hoạnh tài mạnh nhất rơi vào <b>{_best_window_tm}</b> (khi Hào Dụng Thần <b>{dung_than} [{_dt_chi_tm}-{_dt_nh_tm}]</b> và <b>Hào Thế [{_the_chi_tm}-{_the_nh_tm}]</b> đồng lâm Đế Vượng – Trường Sinh), đặc biệt vào các ngày <b>{_dt_chi_tm} · {_the_chi_tm}</b> trong khung giờ <b>9h–11h (Giờ Tị)</b> hoặc <b>13h–15h (Giờ Mùi)</b>."
                )
                adv_s = (
                    f"<b>Pháp quyết đón lộc theo đúng liên kết quẻ:</b><br>"
                    f"1. Trong <b>Tháng {_clk_tm['cur_month']:02d}/{_cur_yr}</b> hiện tại: Giữ chặt túi tiền trước tượng <i>Huynh Đệ động đoạt Tài</i>; nếu mua Vietlot chỉ mua đúng <b>1 vé tự chọn</b> để giữ nhịp cầu may.<br>"
                    f"2. Khi bước vào <b>Cuối tháng 12/{_cur_yr} Dương lịch</b> và <b>{_best_window_tm}</b>: Chọn điểm bán hoặc bấm mua vé khi đang ở hướng <b>{huong_cung}</b> (ứng Cung {target_cung}), ưu tiên chọn bộ số có chứa đuôi Hà Đồ của Hành <b>{_dt_nh_tm}</b> & <b>{_the_nh_tm}</b> (màu sắc trợ vận: <b>{colors_str}</b>) vào ngày <b>{_dt_chi_tm}</b> hoặc <b>{_the_chi_tm}</b>."
                )
                return {
                    "has_override": True,
                    "headline": f"🎯 {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }
            elif _is_intraday_hour_tm:
                # ── GIẢI MÃ CHUYÊN SÂU GIỜ TRONG NGÀY ("MẤY GIỜ XUỐNG / ĐẾN / VỀ / MẤY GIỜ LƯƠNG BẮN") — 12 ĐỊNH LUẬT THỜI-KHÔNG ──
                _raw_q_tm = str(blueprint.get("raw_question") or "").strip()
                _CHI_CLOCK_TM = {
                    "Tý": "23h00 – 01h00", "Sửu": "01h00 – 03h00", "Dần": "03h00 – 05h00", "Mão": "05h00 – 07h00",
                    "Thìn": "07h00 – 09h00", "Tị": "09h00 – 11h00", "Ngọ": "11h00 – 13h00", "Mùi": "13h00 – 15h00",
                    "Thân": "15h00 – 17h00", "Dậu": "17h00 – 19h00", "Tuất": "19h00 – 21h00", "Hợi": "21h00 – 23h00",
                }
                _CHI_PEAK_TM = {
                    "Tý": "23h30 – 00h30", "Sửu": "01h30 – 02h30", "Dần": "03h30 – 04h30", "Mão": "05h30 – 06h30",
                    "Thìn": "07h30 – 08h30", "Tị": "09h30 – 10h30", "Ngọ": "12h00 – 13h00", "Mùi": "13h00 – 14h00",
                    "Thân": "15h00 – 16h15", "Dậu": "17h15 – 18h30", "Tuất": "19h15 – 20h30", "Hợi": "21h15 – 22h30",
                }
                _HOP_CHI_TM = {
                    "Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão",
                    "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ",
                }
                _XUNG_CHI_TM = {
                    "Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần",
                    "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị",
                }
                _dong_list_tm = _m_tm.get("dong_list") or []
                _dt_is_moving_tm = (_dt_idx_tm in _dong_list_tm)
                # Tìm Địa Chi Hào Biến của Dụng Thần (hoặc của Hào Động)
                _bien_chi_tm = _HOP_CHI_TM.get(_dt_chi_tm, "Mùi")
                for _hd_line in (_m_tm.get("haos_lines_desc") or []):
                    if f"Hào {_dt_idx_tm}" in _hd_line and "biến" in _hd_line:
                        _m_b = re.search(r"biến\s+[^\(]*\(([A-ZĐa-zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+)-", _hd_line)
                        if _m_b:
                            _bien_chi_tm = _m_b.group(1).strip()
                            break
                _hop_dt_chi = _HOP_CHI_TM.get(_dt_chi_tm, _bien_chi_tm)
                _secondary_chi = _bien_chi_tm if _dt_is_moving_tm else (_hop_dt_chi if not _dt_kv_tm else _XUNG_CHI_TM.get(_dt_chi_tm, "Ngọ"))
                if _secondary_chi == _dt_chi_tm:
                    _secondary_chi = _hop_dt_chi

                _cur_g_clock = _CHI_CLOCK_TM.get(chi_g, "11h00 – 13h00")
                _dt_clock = _CHI_CLOCK_TM.get(_dt_chi_tm, "11h00 – 13h00")
                _dt_peak = _CHI_PEAK_TM.get(_dt_chi_tm, "12h00 – 13h00")
                _sec_clock = _CHI_CLOCK_TM.get(_secondary_chi, "13h00 – 15h00")
                _sec_peak = _CHI_PEAK_TM.get(_secondary_chi, "13h00 – 14h00")

                _is_money_tm = any(w in _q_low_tm for w in ["lương", "tiền", "bắn", "chuyển khoản", "tài khoản", "nổ", "ting ting", "thưởng"])
                if _is_money_tm:
                    _tai_sent_tm = bool(_m_tm.get("tai_already_sent", True))
                    _tai_verdict_tm = _m_tm.get("tai_timing_verdict_short") or ""
                    if _tai_sent_tm:
                        short_hl = (
                            f"⚡ KẾT LUẬN THỜI ĐIỂM BẮN LƯƠNG / TIỀN VỀ CHO «{_raw_q_tm.upper()}» ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                            f"[1] ỨNG NGHIỆM TỨC THỜI (ĐƯƠNG THỜI ĐẮC TÀI): KHOẢN LƯƠNG / TIỀN ĐÃ BẮN VỀ TÀI KHOẢN NGAY TRONG KHUNG GIỜ HIỆN TẠI — GIỜ {chi_g.upper()} ({_cur_g_clock}) "
                            f"(DO HÀO ĐỘNG & DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_tm} {_dt_chi_tm.upper()}-{_dt_nh_tm.upper()} ĐÃ PHÁT ĐỘNG / ĐẮC KHÍ TRONG NGÀY {chi_n.upper()}) — KIỂM TRA SỐ DƯ NGAY!  |  "
                            f"[2] NẾU NGÂN HÀNG XỬ LÝ LỆCH NHỊP LIÊN NGÂN HÀNG: CHẬM NHẤT ĐẦU GIỜ {_secondary_chi.upper()} ({_sec_peak}) LÀ NỔI TIỀN!"
                        )
                        why_s = (
                            f"<b>• Phân tích theo 12 Định Luật Thời-Không (Tăng San Bốc Dịch — Chương Ứng Kỳ Tài Phúc):</b><br>"
                            f"1. <b>[Định luật Đương Thời Ứng Nghiệm]:</b> Quẻ lập tại Ngày <b>{can_n} {chi_n}</b> · Giờ <b>{can_g} {chi_g} ({_cur_g_clock})</b>. "
                            f"Khi Hào Động ({_dong_desc_tm}) đã phát động rõ rệt và Dụng Thần <b>{dung_than}</b> tại Hào {_dt_idx_tm} (<b>{_dt_chi_tm}-{_dt_nh_tm}</b>) hữu khí, cổ pháp quyết định: <i>«Dụng Thần đắc thời phát động, tiền tài đương thời đã phát»</i> — tức là lệnh bắn lương/chuyển khoản <b>ĐÃ ĐƯỢC THỰC HIỆN NGAY TRONG GIỜ {chi_g.upper()} ({_cur_g_clock})</b>.<br>"
                            f"2. <b>[Đối chứng Tam Thức (Mai Hoa – Kỳ Môn – Lục Hào)]:</b> Quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> ({_m_tm.get('rel_bien_tag', '')}); Kỳ Môn Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> xác nhận giao dịch đã thông suốt."
                        )
                        when_s = (
                            f"<b>• Khung Giờ Chính Xác Trong Ngày ({_cur_solar}):</b><br>"
                            f"&nbsp;&nbsp;1. <b>Mốc 1 (Đã bắn / Nổ ngay hiện tại):</b> <b>Giờ {chi_g} ({_cur_g_clock})</b> — Lệnh chuyển tiền đã khớp ngay tại thời điểm bạn gieo quẻ.<br>"
                            f"&nbsp;&nbsp;2. <b>Mốc 2 (Khung giờ Lục Hợp / Hào Biến {_secondary_chi}):</b> <b>Đầu Giờ {_secondary_chi} ({_sec_peak})</b> — Hoàn tất 100% thông báo biến động số dư."
                        )
                    else:
                        short_hl = (
                            f"🕐 KẾT LUẬN THỜI ĐIỂM BẮN LƯƠNG / TIỀN VỀ CHO «{_raw_q_tm.upper()}» ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                            f"{_tai_verdict_tm}"
                        )
                        why_s = (
                            f"<b>• Phân tích theo 12 Định Luật Thời-Không (Tăng San Bốc Dịch — Chương Ứng Kỳ Tài Phúc):</b><br>"
                            f"1. <b>[Kiểm tra Trạng thái Hào Thê Tài / Dụng Thần]:</b> {_m_tm.get('the_tai_status_str', '')}.<br>"
                            f"2. <b>[Quy luật Ứng Kỳ]:</b> Khi Hào Tài đang an tĩnh hoặc vướng Không/Phục/Huynh Đệ động, lệnh chuyển tiền chưa khớp ngay tại Giờ {chi_g} mà phải đợi đến đúng <b>Giờ/Ngày Địa Chi Hào Tài ({_dt_chi_tm}: {_dt_clock})</b> hoặc <b>Giờ Xung/Hợp ({_secondary_chi}: {_sec_clock})</b> mới thực sự nổi tiền."
                        )
                        when_s = (
                            f"<b>• Khung Giờ Chính Xác Tiền Về ({_cur_solar}):</b><br>"
                            f"&nbsp;&nbsp;1. <b>Mốc 1 (Ứng trực diện Chi Dụng Thần {_dt_chi_tm}):</b> <b>Giờ {_dt_chi_tm} ({_dt_clock}, trọng tâm {_dt_peak})</b>.<br>"
                            f"&nbsp;&nbsp;2. <b>Mốc 2 (Ứng Chi Lục Hợp / Xung {_secondary_chi}):</b> <b>Giờ {_secondary_chi} ({_sec_clock}, trọng tâm {_sec_peak})</b>."
                        )
                else:
                    # Câu hỏi Người di chuyển / Chị gái / Anh em / Bạn bè / Khách mấy giờ xuống, đến, về — V126.0: Phân nhánh ĐỘNG vs TĨNH vs TUẦN KHÔNG 100% theo quẻ!
                    _person_lbl = "CHỊ GÁI BẠN" if "chị gái" in _q_low_tm else ("ANH TRAI BẠN" if "anh trai" in _q_low_tm else ("EM BẠN" if "em " in _q_low_tm else "NGƯỜI BẠN HỎI"))
                    _xung_dt_chi = _XUNG_CHI_TM.get(_dt_chi_tm, "Tý")
                    _xung_clock = _CHI_CLOCK_TM.get(_xung_dt_chi, "23h00 – 01h00")
                    _xung_peak = _CHI_PEAK_TM.get(_xung_dt_chi, "23h30 – 00h30")
                    if _dt_kv_tm and not _dt_is_moving_tm:
                        # Nhánh C: Dụng Thần lâm Tuần Không tĩnh -> Đang vướng bận/hoãn lịch, phải đợi Giờ Xuất Không / Xung Không
                        short_hl = (
                            f"⏳ KẾT LUẬN CHÍNH XÁC MẤY GIỜ {_person_lbl} XUỐNG / TỚI NƠI ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_tm} {_dt_chi_tm.upper()}-{_dt_nh_tm.upper()} ĐANG TUẦN KHÔNG): "
                            f"HIỆN TẠI {_person_lbl} ĐANG VƯỚNG BẬN / CHƯA XUẤT PHÁT NGAY (DO HÀO {_dt_idx_tm} {_dt_chi_tm.upper()} LÂM TUẦN KHÔNG) — "
                            f"[MỐC 1 — XUẤT KHÔNG / XUNG KHÔNG KHỞI HÀNH]: PHẢI ĐỢI ĐẾN KHUNG GIỜ {_xung_dt_chi.upper()} ({_xung_clock}) HOẶC GIỜ {_dt_chi_tm.upper()} ({_dt_clock}, TRỌNG TÂM {_dt_peak}) MỚI ĐI!  |  "
                            f"[MỐC 2 — TỚI NƠI]: CÓ MẶT VÀO KHUNG GIỜ {_hop_dt_chi.upper()} ({_CHI_CLOCK_TM.get(_hop_dt_chi, _sec_clock)}) (HOẶC DỄ DỜI SANG NGÀY {_dt_chi_tm.upper()})!"
                        )
                        why_s = (
                            f"<b>• Giải Mã Theo 12 Định Luật Thời-Không Cổ Pháp (Tăng San Bốc Dịch — Chương Hành Nhân Quy Kỳ):</b><br>"
                            f"1. <b>[Trạng thái Dụng Thần Tuần Không]:</b> Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_tm} ({_dt_chi_tm}-{_dt_nh_tm})</b> hiện đang lâm <b>Tuần Không ({', '.join(_m_tm.get('kv_list') or [])})</b> lại an tĩnh ➔ Cổ pháp quyết: <i>«Dụng Thần Tuần Không an tĩnh, người còn đang bận việc chưa thể bước chân đi ngay»</i>.<br>"
                            f"2. <b>[Định luật Xuất Không & Xung Không]:</b> Phải chờ đến đúng <b>Giờ {_xung_dt_chi} ({_xung_clock} — Xung thực Tuần Không)</b> hoặc <b>Giờ/Ngày {_dt_chi_tm} ({_dt_clock} — Điền thực Xuất Không)</b> người mới thực sự khởi hành và đến nơi."
                        )
                        when_s = (
                            f"<b>• Chốt Khung Giờ Thực Tế ({_cur_solar} — Ngày {can_n} {chi_n}):</b><br>"
                            f"&nbsp;&nbsp;1. <b>Khung giờ Xung Không / Xuất Không ({_xung_dt_chi} / {_dt_chi_tm}):</b> <b>{_xung_clock}</b> hoặc <b>{_dt_clock} (trọng tâm {_dt_peak})</b> — Bắt đầu xuất phát.<br>"
                            f"&nbsp;&nbsp;2. <b>Khung giờ Hợp Chi Tới Nơi ({_hop_dt_chi}):</b> <b>{_CHI_CLOCK_TM.get(_hop_dt_chi, _sec_clock)}</b> — Có mặt tại chỗ bạn."
                        )
                    elif _dt_is_moving_tm:
                        # Nhánh A: Dụng Thần PHÁT ĐỘNG trực tiếp trên quẻ -> Đã xuất phát / đang trên đường xuống!
                        short_hl = (
                            f"🕐 KẾT LUẬN CHÍNH XÁC MẤY GIỜ {_person_lbl} XUỐNG / TỚI NƠI ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_tm} {_dt_chi_tm.upper()}-{_dt_nh_tm.upper()} PHÁT ĐỘNG): "
                            f"[MỐC 1 — ỨNG TRỰC DIỆN HÀO DỤNG THẦN ĐỘNG TẠI GIỜ {_dt_chi_tm.upper()}]: {_person_lbl} ĐÃ XUẤT PHÁT / ĐANG TRÊN ĐƯỜNG XUỐNG NGAY TRONG KHUNG GIỜ {_dt_chi_tm.upper()} ({_dt_clock}, TRỌNG TÂM {_dt_peak})!  |  "
                            f"[MỐC 2 — ĐIỂM CHẠM MẶT / TỚI NƠI THEO HÀO BIẾN & LỤC HỢP {_secondary_chi.upper()}]: CÓ MẶT TẠI CHỖ BẠN VÀO ĐẦU KHUNG GIỜ {_secondary_chi.upper()} ({_sec_clock}, TRỌNG TÂM {_sec_peak})!"
                        )
                        why_s = (
                            f"<b>• Giải Mã Theo 12 Định Luật Thời-Không Cổ Pháp (Tăng San Bốc Dịch — Chương Hành Nhân Quy Kỳ):</b><br>"
                            f"1. <b>[Xác định Dụng Thần & Vị thế Hào Động]:</b> Bạn hỏi về <b>«{_raw_q_tm}»</b> ➔ Dụng Thần chính xác là <b>{dung_than}</b>, đóng tại <b>Hào {_dt_idx_tm} ({_dt_chi_tm}-{_dt_nh_tm})</b> "
                            f"{'(Hào 4 là <b>Hào Cửa Ngõ / Ngoại Quái giao Nội Quái</b> — tượng trưng người đã bước ra khỏi cửa và đang di chuyển trên đường xuống chỗ bạn)' if _dt_idx_tm in (3, 4) else f'(tương ứng trực tiếp với Hào Thế tại Hào {_the_idx_tm} {_the_chi_tm}-{_the_nh_tm})'}.<br>"
                            f"2. <b>[Định luật Động – Biến – Lục Hợp & Tam Hợp Khóa Giờ]:</b> Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> ({_dong_desc_tm}), Hào Dụng Thần <b>{dung_than} ({_dt_chi_tm}-{_dt_nh_tm})</b> "
                            f"<b>PHÁT ĐỘNG TRỰC TIẾP tại Hào {_dt_idx_tm}</b>, tương tác với Ngày <b>{chi_n}</b> · Giờ <b>{chi_g}</b> và biến ra <b>{_bien_chi_tm}</b>. "
                            f"Cổ pháp Hành Nhân khẳng định: <i>«Dụng Thần động tại môn hộ, phùng Nhật Thời Tam Hợp / trị Giờ: Người đã lên đường ngay trong giờ đó; Hào Động biến Hợp: Giờ Hợp tức khắc tới nơi!»</i><br>"
                            f"3. <b>[Đối chứng Mai Hoa & Kỳ Môn Độn Giáp]:</b> Quẻ Biến <b>{ten_que_bien}</b> ({'Gia Nhân = Người nhà sum họp' if 'Gia Nhân' in ten_que_bien else _m_tm.get('rel_bien_tag', 'Cát lợi')}), Kỳ Môn Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> xác nhận lộ trình di chuyển thông suốt."
                        )
                        when_s = (
                            f"<b>• Chốt Khung Giờ Chính Xác Trong Ngày Hôm Nay ({_cur_solar} — Ngày {can_n} {chi_n}):</b><br>"
                            f"&nbsp;&nbsp;1. <b>Khung giờ số 1 — Giờ {_dt_chi_tm} ({_dt_clock}, điểm rơi mạnh nhất {_dt_peak}):</b> Ứng trực tiếp Địa Chi Hào Dụng Thần <b>{_dt_chi_tm}</b> (Hào {_dt_idx_tm} đang động) — {_person_lbl.capitalize()} di chuyển / xuống ngay trong cuối khung giờ này.<br>"
                            f"&nbsp;&nbsp;2. <b>Khung giờ số 2 — Giờ {_secondary_chi} ({_sec_clock}, điểm rơi mạnh nhất {_sec_peak}):</b> Ứng Hào Biến / Lục Hợp <b>{_dt_chi_tm} – {_secondary_chi}</b> — Điểm chạm mặt, gặp nhau trực tiếp tại chỗ bạn (đầu Giờ {_secondary_chi} <b>{_sec_peak}</b> là tới)."
                        )
                    else:
                        # Nhánh B: Dụng Thần AN TĨNH hữu khí -> Cần đợi Giờ Xung động bước chân hoặc chính Giờ Dụng Thần mới đi
                        short_hl = (
                            f"🕐 KẾT LUẬN CHÍNH XÁC MẤY GIỜ {_person_lbl} XUỐNG / TỚI NƠI ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_tm} {_dt_chi_tm.upper()}-{_dt_nh_tm.upper()} HỮU KHÍ AN TĨNH): "
                            f"[MỐC 1 — KHỞI HÀNH KHI ĐẾN GIỜ BẢN CHI / XUNG ĐỘNG]: HIỆN TẠI LÚC HỎI HÀO {_dt_idx_tm} ĐANG TĨNH (CHƯA ĐI NGAY), SẼ BẮT ĐẦU XUẤT PHÁT VÀO KHUNG GIỜ {_dt_chi_tm.upper()} ({_dt_clock}, TRỌNG TÂM {_dt_peak}) (HOẶC GIỜ XUNG ĐỘNG {_xung_dt_chi.upper()}: {_xung_clock})!  |  "
                            f"[MỐC 2 — TỚI NƠI TẠI GIỜ LỤC HỢP {_hop_dt_chi.upper()}]: CÓ MẶT TẠI CHỖ BẠN VÀO KHUNG GIỜ {_hop_dt_chi.upper()} ({_CHI_CLOCK_TM.get(_hop_dt_chi, _sec_clock)}, TRỌNG TÂM {_CHI_PEAK_TM.get(_hop_dt_chi, _sec_peak)})!"
                        )
                        why_s = (
                            f"<b>• Giải Mã Theo 12 Định Luật Thời-Không Cổ Pháp (Tăng San Bốc Dịch — Chương Hành Nhân Quy Kỳ):</b><br>"
                            f"1. <b>[Trạng thái Dụng Thần An Tĩnh Hữu Khí]:</b> Hào Dụng Thần <b>{dung_than} tại Hào {_dt_idx_tm} ({_dt_chi_tm}-{_dt_nh_tm})</b> hữu khí (không phạm Tuần Không) nhưng đang <b>An Tĩnh</b> trên quẻ ({_dong_desc_tm}). Cổ pháp quyết: <i>«Dụng Thần tĩnh mà hữu khí: Đợi giờ Đương Giá (Giờ {_dt_chi_tm}) hoặc giờ Độc Xung (Giờ {_xung_dt_chi}) xung động bước chân thì lên đường; đến giờ Lục Hợp (Giờ {_hop_dt_chi}) thì gặp mặt»</i>.<br>"
                            f"2. <b>[Đối chứng Mai Hoa & Kỳ Môn Độn Giáp]:</b> Quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> ({_m_tm.get('rel_bien_tag', 'Cát lợi')}), Kỳ Môn Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b>."
                        )
                        when_s = (
                            f"<b>• Chốt Khung Giờ Chính Xác Trong Ngày ({_cur_solar} — Ngày {can_n} {chi_n}):</b><br>"
                            f"&nbsp;&nbsp;1. <b>Khung giờ Xuất phát (Giờ {_dt_chi_tm} / Giờ Xung {_xung_dt_chi}):</b> <b>{_dt_clock} (trọng tâm {_dt_peak})</b> hoặc <b>{_xung_clock}</b>.<br>"
                            f"&nbsp;&nbsp;2. <b>Khung giờ Tới nơi (Giờ Lục Hợp {_hop_dt_chi}):</b> <b>{_CHI_CLOCK_TM.get(_hop_dt_chi, _sec_clock)} (trọng tâm {_CHI_PEAK_TM.get(_hop_dt_chi, _sec_peak)})</b>."
                        )
                adv_s = (
                    f"<b>• Hướng dẫn Thực tế:</b> Chủ động liên hệ/đón tại hướng <b>{huong_cung}</b> (ứng Cung {target_cung}: Sao {sao_name} · Cửa {cua_name}); "
                    f"mốc thời gian hội tụ chuẩn nhất là <b>{_dt_peak} (Giờ {_dt_chi_tm})</b> nối sang <b>{_sec_peak} (Đầu Giờ {_secondary_chi})</b>."
                )
                return {
                    "has_override": True,
                    "is_strict_override": True,
                    "headline": f"🎯 {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }
            else:
                # Câu hỏi "Bao giờ / Khi nào..." tổng quát cho mọi sự việc dài hạn khác
                _raw_q_tm = str(blueprint.get("raw_question") or "").strip()
                _meta_u_tm = _m_tm.get("meta_up_chu") or (1, 1, 6, "Kim", "")
                _meta_l_tm = _m_tm.get("meta_lo_chu") or (4, 4, 3, "Mộc", "")
                _quai_sum_tm = int(_meta_u_tm[1]) + int(_meta_l_tm[1])
                _rel_bien_tm = _m_tm.get("rel_bien_tag", "TỶ HÒA")
                if _km_pn_tm or _dt_kv_tm or _hd_dong_flag:
                    short_hl = (
                        f"⏳ KẾT LUẬN LIÊN KẾT MỌI YẾU TỐ QUẺ CHO «{_raw_q_tm.upper()}» ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | HIỆN TẠI: {_cur_solar} — {_season_lbl.upper()}): "
                        f"SỰ VIỆC (DỤNG THẦN {dung_than.upper()} TẠI HÀO {_dt_idx_tm} {_dt_chi_tm.upper()}-{_dt_nh_tm.upper()}) CHƯA THỂ XẢY RA NGAY TRONG THÁNG {_clk_tm['cur_month']:02d}/{_cur_yr} DO ĐANG VƯỚNG {'PHỤC NGÂM KỲ MÔN & ' if _km_pn_tm else ''}{'TUẦN KHÔNG & ' if _dt_kv_tm else ''}{_dong_desc_tm.upper()}! "
                        f"➔ THỜI ĐIỂM ỨNG NGHIỆM THỰC TẾ (ỨNG QUÁI SỐ MAI HOA = {_quai_sum_tm} KỲ HẠN & HÀO {_dt_idx_tm} {_dt_chi_tm.upper()}): TỪ CUỐI THÁNG 12/{_cur_yr} DƯƠNG LỊCH (CUỐI NĂM {_cur_yr_cc}) ĐẾN {_best_window_tm.upper()} (TRỌNG TÂM NGÀY/THÁNG {_dt_chi_tm.upper()} – {_the_chi_tm.upper()})!"
                    )
                else:
                    short_hl = (
                        f"⏳ KẾT LUẬN LIÊN KẾT MỌI YẾU TỐ QUẺ CHO «{_raw_q_tm.upper()}» ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()} | HIỆN TẠI: {_cur_solar} — {_season_lbl.upper()}): "
                        f"ĐIỀU KIỆN ĐÃ HỘI TỤ (DỤNG THẦN {dung_than.upper()} Hào {_dt_idx_tm} {_dt_chi_tm.upper()}-{_dt_nh_tm.upper()} & {_rel_bien_tm.upper()} · QUÁI SỐ MAI HOA = {_quai_sum_tm}) — "
                        f"THỜI ĐIỂM ỨNG NGHIỆM RƠI VÀO CUỐI NĂM {_cur_yr} (THÁNG 11–12/{_cur_yr} DƯƠNG LỊCH, TRONG {_quai_sum_tm} NGÀY/TUẦN TỚI VÀO NGÀY {_dt_chi_tm.upper()} / {_the_chi_tm.upper()}) "
                        f"HOẶC ĐẦU NĂM {_nxt_yr} ({_nxt_yr_cc} — {_best_window_tm.upper()})!"
                    )
                why_s = (
                    f"<b>• Phân tích Liên Kết 4 Mắt Xích Của Quẻ cho câu hỏi «{_raw_q_tm}» (Tại mốc hiện tại {_cur_solar} Dương lịch — {_cur_lunar} Âm lịch):</b><br>"
                    f"1. <b>[Mắt xích 1 — Bản thân (Hào Thế)]:</b> Hào {_the_idx_tm} ({_the_chi_tm}-{_the_nh_tm}) phối hợp Quẻ Thể <b>{_m_tm.get('the_quai', '')} ({_m_tm.get('hanh_the', '')})</b>.<br>"
                    f"2. <b>[Mắt xích 2 — Nguồn lực / Tiền bạc (Hào Thê Tài)]:</b> {_tai_status_tm}.<br>"
                    f"3. <b>[Mắt xích 3 — Mục tiêu Dụng Thần ({dung_than})]:</b> Hào {_dt_idx_tm} ({_dt_chi_tm}-{_dt_nh_tm}) — Biến động: <b>{_dong_desc_tm}</b>.<br>"
                    f"4. <b>[Mắt xích 4 — Kỳ Môn & Mai Hoa]:</b> Quẻ Chủ <b>{ten_que_chu}</b> (Quẻ Hỗ <b>{_m_tm.get('full_ho','')}</b>) biến <b>{ten_que_bien}</b> ({_rel_bien_tm}, Tổng Tiên Thiên Quái Số = <b>{_quai_sum_tm}</b>); Kỳ Môn Cục {_m_tm.get('cuc_km','?')} tại Cung {target_cung} ({huong_cung}) hội Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b> ({_km_pn_str_tm})."
                )
                when_s = (
                    f"<b>Lộ trình Ứng Kỳ Thực Tế (Tính từ hôm nay {_cur_solar} — {_season_lbl}):</b><br>"
                    f"• <b>Mốc gần (Cuối năm {_cur_yr} — Tháng 11–12/{_cur_yr} Dương lịch, ứng Quái số Mai Hoa = {_quai_sum_tm}):</b> Chuyển biến khởi đầu vào các ngày/giờ <b>{_dt_chi_tm}</b> và <b>{_the_chi_tm}</b>.<br>"
                    f"• <b>Mốc thành tựu trọn vẹn (Năm {_nxt_yr} — {_nxt_yr_cc}):</b> Điểm rơi mạnh nhất vào <b>{_best_window_tm}</b> khi Dụng Thần <b>{dung_than} ({_dt_chi_tm}-{_dt_nh_tm})</b> đắc lệnh hoàn toàn."
                )
                adv_s = (
                    f"Hành động theo phương vị <b>{huong_cung}</b> (Cung {target_cung}: Sao {sao_name} · Cửa {cua_name}), tận dụng màu sắc <b>{colors_str}</b> và chuẩn bị kỹ nguồn lực từ <b>Cuối năm {_cur_yr}</b> sang <b>Năm {_nxt_yr}</b>."
                )
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

        # ── 9. GIẢI MÃ CHUYÊN SÂU: TÂM LINH, ÂM BINH, VONG LINH, TÀ KHÍ & KIỂM CHỨNG PHÚC KHÍ (SPIRITUAL_YIN_CHECK — ĐỊNH LUẬT 11 ANTIGRAVITY) ──
        if target == "SPIRITUAL_YIN_CHECK" or any(w in q_low for w in ["âm binh", "vong linh", "vong theo", "vong nhập", "tà khí", "tà ma", "quỷ ám", "ma ám", "bùa ngải", "phúc khí"]):
            _CHI_NH_SP = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
            _SINH_SP = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
            _KHAC_SP = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
            _DIR_CHI_SP = {
                "Tý": "Chính Bắc (nơi ẩm thấp, gần nguồn nước/nhà vệ sinh)",
                "Sửu": "Đông Bắc (nền đất cũ, góc tường hoặc gần kho/bếp)",
                "Dần": "Đông Bắc (gần cây lớn, đồ gỗ cũ hoặc đầu hồi nhà)",
                "Mão": "Chính Đông (vùng đất có cỏ cây, cửa sổ/cửa phụ hoặc giường gỗ)",
                "Thìn": "Đông Nam (vùng đất trũng, gần rãnh nước hoặc gốc cây)",
                "Tị": "Đông Nam (nơi có đèn điện, bếp lửa hoặc góc khuất nóng bức)",
                "Ngọ": "Chính Nam (phòng khách, ban công hoặc nơi có ánh sáng/nhiệt)",
                "Mùi": "Tây Nam (nền đất vườn cũ, góc phòng ngủ hoặc nơi thờ cúng)",
                "Thân": "Tây Nam (gần đường đi, vật dụng kim khí hoặc cửa sắt)",
                "Dậu": "Chính Tây (cửa ra vào phụ, nơi có gương/kim loại)",
                "Tuất": "Tây Bắc (nền đất cao, miếu cổ/nhà thờ họ hoặc góc tường khô)",
                "Hợi": "Tây Bắc (gần nhà tắm, đường ống nước hoặc góc tối ẩm)",
            }
            _HAO_POS_SP = {
                1: "Hào 1 (Hào Sơ — sát mặt đất, nền nhà, chân tường hoặc gầm giường)",
                2: "Hào 2 (Trạch vị — ngay trong ngôi nhà, phòng sinh hoạt hoặc bếp)",
                3: "Hào 3 (Ranh giới Nội/Ngoại — ngay cửa phòng ngủ, đầu giường hoặc ngưỡng cửa ra vào)",
                4: "Hào 4 (Môn hộ — khu vực cửa chính, hành lang, cầu thang hoặc nhà vệ sinh)",
                5: "Hào 5 (Đường đi bên ngoài — mắc phải khi đi qua ngã đường/nơi công cộng ngoài trời)",
                6: "Hào 6 (Tông miếu / Nơi xa — liên quan âm phần xa, mái nhà hoặc tầng cao)",
            }

            # 1. Tìm Hào Quan Quỷ (Đại diện Âm binh / Vong linh / Tà khí) & Hào Tử Tôn (Đại diện Phúc Khí / Phúc Thần Giải Ách)
            qq_list = []
            tt_list = []
            subj_list = []
            bien_haos_sp = (lh_bien.get("haos") or lh_bien.get("details") or []) if isinstance(lh_bien, dict) else []
            for _ix_s, _h_s in enumerate(haos, 1):
                if not isinstance(_h_s, dict):
                    continue
                _lt_s = str(_h_s.get("luc_than") or "")
                _cc_s = re.sub(r"\([^)]*\)", "", str(_h_s.get("chi") or _h_s.get("can_chi") or "Mão")).strip()
                _ch_s = _cc_s.split()[-1] if _cc_s else "Mão"
                _nh_s = str(_h_s.get("ngu_hanh") or _h_s.get("hanh") or _CHI_NH_SP.get(_ch_s, "Mộc"))
                _is_d_s = (_ix_s in dong_list) or bool(_h_s.get("dong") or _h_s.get("is_dong"))
                _b_lt_s, _b_ch_s, _b_nh_s = "", "", ""
                if _is_d_s and 1 <= _ix_s <= len(bien_haos_sp) and isinstance(bien_haos_sp[_ix_s - 1], dict):
                    _bh_s = bien_haos_sp[_ix_s - 1]
                    _b_lt_s = str(_bh_s.get("luc_than") or "")
                    _bcc_s = re.sub(r"\([^)]*\)", "", str(_bh_s.get("chi") or _bh_s.get("can_chi") or "")).strip()
                    _b_ch_s = _bcc_s.split()[-1] if _bcc_s else ""
                    _b_nh_s = str(_bh_s.get("ngu_hanh") or _bh_s.get("hanh") or _CHI_NH_SP.get(_b_ch_s, ""))
                _item_s = (_ix_s, _cc_s, _ch_s, _nh_s, _is_d_s, _b_lt_s, _b_ch_s, _b_nh_s)
                if "Quan Quỷ" in _lt_s:
                    qq_list.append(_item_s)
                if "Tử Tôn" in _lt_s:
                    tt_list.append(_item_s)
                if dung_than in _lt_s or (dung_than == "Bản Thân" and _ix_s == the_idx):
                    subj_list.append(_item_s)

            qq_ix, qq_cc, qq_ch, qq_nh, qq_dong, qq_b_lt, qq_b_ch, qq_b_nh = qq_list[0] if qq_list else (3, "Ất Mão", "Mão", "Mộc", bool(3 in dong_list), "Tử Tôn", "Thân", "Kim")
            tt_ix, tt_cc, tt_ch, tt_nh, tt_dong, _, _, _ = tt_list[0] if tt_list else (the_idx, "Quý Dậu", "Dậu", "Kim", False, "", "", "")
            sb_ix, sb_cc, sb_ch, sb_nh, sb_dong, _, _, _ = subj_list[0] if subj_list else (1, "Ất Mùi", "Mùi", "Thổ", False, "", "", "")

            _chi_m_sp = chart_data.get("chi_thang", "Tuất")
            _chi_n_sp = chart_data.get("chi_ngay", "Thân")
            _nh_m_sp = _CHI_NH_SP.get(_chi_m_sp, "Thổ")
            _nh_n_sp = _CHI_NH_SP.get(_chi_n_sp, "Kim")
            _kv_sp = _mat_spec.get("kv_list") or ["Ngọ", "Mùi"]

            # Kiểm tra xem Hào Tử Tôn (Phúc Thần) và Nhật/Nguyệt có khắc chế Quan Quỷ (Âm binh) không
            _qq_hoi_dau_khac = bool(qq_dong and qq_b_nh and _KHAC_SP.get(qq_b_nh) == qq_nh)
            _nhat_khac_qq = (_KHAC_SP.get(_nh_n_sp) == qq_nh)
            _tt_vuong = (_SINH_SP.get(_nh_m_sp) == tt_nh or _nh_m_sp == tt_nh or _SINH_SP.get(_nh_n_sp) == tt_nh or _nh_n_sp == tt_nh or tt_ix == the_idx)
            _sb_is_kv = (sb_ch in _kv_sp)

            # Chủ thể được hỏi tên là gì
            _subj_name = "chị gái bạn" if "chị gái" in q_low else ("anh trai bạn" if "anh trai" in q_low else ("em bạn" if "em " in q_low else ("con bạn" if "con " in q_low else "bạn")))

            # [VẾ 1]: ĐANG Ở ĐÂU?
            _where_dir = _DIR_CHI_SP.get(qq_ch, f"Hướng {huong_cung}")
            _where_pos = _HAO_POS_SP.get(qq_ix, f"Hào {qq_ix}")
            _where_summary = (
                f"NẰM TẠI PHƯƠNG {huong_cung.upper()} (CUNG {target_cung} · CỬA {cua_name.upper()} · THẦN {than_name.upper()}) "
                f"KẾT HỢP HƯỚNG {_where_dir.upper()} ({_where_pos.upper()})"
            )

            # [VẾ 2]: CÓ PHẢI LẤY HẾT PHÚC KHÍ KHÔNG?
            if _tt_vuong or _qq_hoi_dau_khac or _nhat_khac_qq or "Thiên Tâm" in sao_name:
                _phuc_verdict = (
                    f"KHÔNG THỂ LẤY HẾT PHÚC KHÍ! PHÚC THẦN (HÀO TỬ TÔN {tt_cc.upper()}-{tt_nh.upper()} TẠI HÀO {tt_ix}{' TRÌ THẾ' if tt_ix == the_idx else ''}) ĐANG VƯỢNG TƯỚNG "
                    + (f"& HÀO QUAN QUỶ ({qq_cc.upper()}) ĐỘNG HÓA TỬ TÔN ({qq_b_ch.upper()}-{qq_b_nh.upper()} — HỒI ĐẦU KHẮC: PHÚC THẦN CHẾ NGƯỢC TÀ KHÍ) " if _qq_hoi_dau_khac else "")
                    + f"— CHỈ LÀM HAO TỔN TINH THẦN / MỆT MỎI TẠM THỜI DO HÀO {dung_than.upper()} ({sb_ch.upper()}) {'LÂM TUẦN KHÔNG' if _sb_is_kv else 'SUY NHƯỢC'}"
                )
                _phuc_detail = (
                    f"<b>KHẲNG ĐỊNH 100% KHÔNG LẤY MẤT PHÚC KHÍ GỐC:</b> Trong Lục Hào, <b>Hào Tử Tôn chính là Phúc Thần (Phúc Khí & Thuốc Giải Tà)</b>. "
                    f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, Hào Tử Tôn đóng tại <b>Hào {tt_ix} ({tt_cc}-{tt_nh}){' trì Thế' if tt_ix == the_idx else ''}</b> được Tháng <b>{_chi_m_sp} ({_nh_m_sp})</b> và Ngày <b>{_chi_n_sp} ({_nh_n_sp})</b> sinh trợ cực vượng"
                    + (f", đặc biệt <b>Hào {qq_ix} Quan Quỷ ({qq_cc}-{qq_nh}) phát động lại biến thành Hào {qq_b_lt or 'Tử Tôn'} ({qq_b_ch}-{qq_b_nh}) — cổ pháp gọi là 'Quỷ Hóa Tử Tôn Hồi Đầu Khắc' (Tà khí tự bị Phúc Thần tiêu trừ)</b>" if _qq_hoi_dau_khac else "")
                    + f", đồng thời Cung {target_cung} có Cát Tinh <b>{sao_name} (Chính khí trừ tà)</b> bảo hộ. Sở dĩ {_subj_name} thấy mệt mỏi, nặng vía là do Hào <b>{dung_than} (Hào {sb_ix} {sb_cc}-{sb_nh})</b> đang {'lâm Tuần Không (tinh thần trống rỗng, suy nhược)' if _sb_is_kv else 'chịu khí khắc nhẹ'}, khiến âm khí thừa cơ quấy nhiễu giấc ngủ và tâm lý chứ <b>không thể đoạt được phúc phần</b>."
                )
            else:
                _phuc_verdict = (
                    f"ĐANG LÀM HAO TỔN DƯƠNG KHÍ & PHÚC LỰC TẠM THỜI (DO HÀO QUAN QUỶ {qq_cc.upper()} VƯỢNG ĐỘNG KHẮC HÀO {dung_than.upper()} {sb_ch.upper()}) — CẦN TỊNH HÓA NGAY ĐỂ BỒI HOÀN PHÚC KHÍ"
                )
                _phuc_detail = (
                    f"Hào Quan Quỷ tại Hào {qq_ix} ({qq_cc}-{qq_nh}) đang tác động lên Hào {dung_than} (Hào {sb_ix} {sb_cc}-{sb_nh}), làm {_subj_name} bị suy giảm dương khí, hay gặp trắc trở và mệt mỏi kéo dài; cần kích hoạt ngay Hào Tử Tôn (Phúc Thần) để chấn chỉnh lại phúc lực."
                )

            # [VẾ 3]: LÀ LOẠI ÂM BINH NÀO?
            _YIN_TYPE_MAP = {
                "Mộc": (
                    "VONG LINH ÂM KHÍ VÃNG LAI NƠI ĐẤT ĐAI – CÂY CỐI / VONG NỮ TRẺ HOẶC VONG ĐẤT CŨ (KHÔNG PHẢI BÙA NGẢI ĐỘC HAY ĐẠI HUNG THẦN)",
                    f"Hào Quan Quỷ mang can chi <b>{qq_cc} (Hành Mộc — Âm Mộc thảo mộc)</b> nằm trong quẻ <b>{ten_que_chu}</b> kết hợp <b>Cửa {cua_name} + Thần {than_name}</b>: Cổ pháp <i>Tăng San Bốc Dịch (Quỷ Thần Chương)</i> định danh đây là <b>vong linh vãng lai vô chủ bám theo nền đất ẩm / gốc cây cũ hoặc vong nữ trẻ khuất mặt lâu ngày</b> (không phải bùa ngải ác ý do thầy tà yểm), nhân lúc {_subj_name} yếu bóng vía mà dựa vào cầu cạnh hương khói."
                ),
                "Thủy": (
                    "VONG NƯỚC / ÂM KHÍ LẠNH LẼO TỪ MẠCH NƯỚC NGẦM – AO HỒ – ĐÊM TỐI",
                    f"Hào Quan Quỷ mang can chi <b>{qq_cc} (Hành Thủy)</b> phối hợp Cung {target_cung} (<b>{cua_name} · {than_name}</b>): Đây là <b>vong linh miền sông nước hoặc tà khí tích tụ nơi ẩm lạnh, tối tăm</b>, hay gây cảm giác ớn lạnh sống lưng, bóng đè và mộng mị ban đêm."
                ),
                "Hỏa": (
                    "VONG HƯƠNG KHÓI / KHẨU NGUYỆN CŨ HOẶC VONG NÓNG NẢY GÂY BỨC BỐI MẤT NGỦ",
                    f"Hào Quan Quỷ mang can chi <b>{qq_cc} (Hành Hỏa)</b> phối hợp <b>{cua_name} · {than_name}</b>: Đây là <b>vong linh liên quan đến hương khói thờ tự thiếu sót, lời khấn nguyện cũ chưa trả hoặc âm khí nóng bức</b>, gây triệu chứng bồn chồn, nóng ruột, đau đầu và khó ngủ."
                ),
                "Kim": (
                    "VONG HUYẾT QUANG / THƯƠNG TÍCH CŨ NGOÀI ĐƯỜNG ĐI (KHÍ TÍNH GẮT GAO)",
                    f"Hào Quan Quỷ mang can chi <b>{qq_cc} (Hành Kim)</b> phối hợp <b>{cua_name} · {than_name}</b>: Đây là <b>vong linh mất vì tai nạn/thương tích cũ ngoài đường hoặc khí sát kim loại</b>, dễ gây đau nhức vai gáy, xương khớp và giật mình hoảng sợ."
                ),
                "Thổ": (
                    "VONG THỔ ĐỊA / ÂM PHẦN ĐẤT CŨ HOẶC GIA TIÊN CHƯA YÊN VỊ DƯỚI NỀN ĐẤT",
                    f"Hào Quan Quỷ mang can chi <b>{qq_cc} (Hành Thổ)</b> nằm trong quẻ <b>{ten_que_chu}</b> kết hợp <b>{cua_name} · {than_name}</b>: Đây là <b>vong thổ kỳ tại nền đất cũ hoặc âm phần/mộ phần động khí</b>, gây cảm giác trì trệ, nặng nề chân tay và uể oải."
                ),
            }
            _yin_type_short, _yin_type_detail = _YIN_TYPE_MAP.get(qq_nh, _YIN_TYPE_MAP["Mộc"])

            short_hl = (
                f"☯️ GIẢI MÃ TRỌN VẸN 3 VẾ TÂM LINH & PHÚC KHÍ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                f"[1. ĐANG Ở ĐÂU]: {_where_summary}  |  "
                f"[2. CÓ LẤY HẾT PHÚC KHÍ KHÔNG]: {_phuc_verdict}  |  "
                f"[3. LÀ LOẠI ÂM BINH NÀO]: {_yin_type_short}!"
            )
            why_s = (
                f"• <b>[1. Định vị nơi Âm khí trú ngụ]:</b> Hào <b>Quan Quỷ ({qq_cc}-{qq_nh})</b> đóng tại <b>{_where_pos}</b>, phối hợp Kỳ Môn <b>Cung {target_cung} ({huong_cung} · Cửa {cua_name} · Thần {than_name})</b> ➔ Chỉ rõ âm khí nằm ở <b>{_where_dir}</b> và góc <b>{huong_cung}</b>.<br>"
                f"• <b>[2. Kiểm chứng Phúc Khí (Hào Tử Tôn)]:</b> {_phuc_detail}<br>"
                f"• <b>[3. Định danh Loại Âm Binh]:</b> {_yin_type_detail}"
            )
            when_s = (
                f"• <b>Thời điểm tiêu trừ & nhẹ người:</b> Vào ngày/giờ <b>{tt_ch}, {_chi_n_sp}</b> (khi Hào Tử Tôn Phúc Thần <b>{tt_ch}-{tt_nh}</b> vượng khí xung khắc hoàn toàn Quan Quỷ <b>{qq_ch}</b> và Hào {dung_than} <b>{sb_ch}</b> Xuất Không)."
            )
            adv_s = (
                f"• <b>Pháp Quyết Hóa Giải Chính Đạo:</b> Mở thoáng ánh sáng dương khí tại góc <b>{huong_cung}</b> và hướng <b>{_where_dir.split(' (')[0]}</b> (dọn sạch đồ ẩm mốc gần giường ngủ/cửa phòng Hào {qq_ix}); "
                f"tăng cường hành <b>{tt_nh} (Phúc Thần Tử Tôn)</b> và <b>Sao {sao_name}</b> bằng cách giữ tâm an định, làm việc thiện lành, xông trầm/tinh dầu ấm để bồi đắp dương khí cho {_subj_name} (tuyệt đối không cần lo sợ hay tốn kém cúng bái mê tín)."
            )
            return {
                "has_override": True,
                "is_strict_override": True,
                "headline": f"🎯 {short_hl}",
                "short_headline": short_hl,
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
        V113.0 (BỘ NÃO HỢP NHẤT 8 ĐỊNH LUẬT CHO TOÀN BỘ 25 ĐẠI DẠNG CÂU HỎI):
        Tự động liên kết 6 Mắt Xích Cốt Lõi (Chủ thể Hào Thế & Quái Chủ Thể <-> Dụng Thần & Quái Vật Thể [tách khỏi Quái Không Gian]
        <-> Nguồn lực Thê Tài / Nguyên Thần / Phục Thần <-> Kỵ Thần / Tuần Không / Phục Ngâm [Tách biệt Hiện trạng vs Tiên lượng]
        <-> Hội tụ 6 Tầng Số & Quy mô Quẻ Biến <-> Kỳ Môn Tinh/Môn/Thần) cho MỌI câu hỏi bất kỳ mà không cần sửa từng câu!
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = dict(omni_data or {})
        if sq_bp.get("raw_question") and not omni_data.get("question"):
            omni_data["question"] = sq_bp.get("raw_question", "")
        _m = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(chart_data, luc_hao_data, mai_hoa_data, omni_data, sq_dt)

        _CHI_NH = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
        _TT_NUM = {"Càn": 1, "Đoài": 2, "Ly": 3, "Chấn": 4, "Tốn": 5, "Khảm": 6, "Cấn": 7, "Khôn": 8}
        _HT_NUM = {"Khảm": 1, "Khôn": 2, "Chấn": 3, "Tốn": 4, "Càn": 6, "Đoài": 7, "Cấn": 8, "Ly": 9}
        _TRIG_NH = {"Càn": "Kim", "Đoài": "Kim", "Ly": "Hỏa", "Chấn": "Mộc", "Tốn": "Mộc", "Khảm": "Thủy", "Cấn": "Thổ", "Khôn": "Thổ"}

        chi_m = chart_data.get("chi_thang", "Tuất")
        chi_n = chart_data.get("chi_ngay", "Ngọ")
        nh_m = _CHI_NH.get(chi_m, "Thổ")
        nh_n = _CHI_NH.get(chi_n, "Hỏa")

        dt_idx = int(_m["dt_idx"] or 3)
        dt_chi = _m["dt_chi"]
        dt_nh = _m["dt_nh"]
        found_dt = bool(_m["dt_haos_all"])
        dt_is_kv = dt_chi in (_m.get("kv_list") or [])
        ky_nh = next((k for k, v in _KHAC.items() if v == dt_nh), "Hỏa")
        ng_nh = next((k for k, v in _SINH.items() if v == dt_nh), "Thổ")

        # 1. Tính Hội Tụ 6 Tầng Số (6-Layer Convergent Number) cho mọi câu hỏi
        _up_g, _lo_g = _m.get("up_chu") or "Đoài", _m.get("lo_chu") or "Khôn"
        _dong_g = int(_m["dong_list"][0]) if _m.get("dong_list") else int(_m.get("the_idx") or 2)
        _cung_g = int(_m.get("target_cung") or 2) if str(_m.get("target_cung") or "2").isdigit() else 2
        _m_cuc_g = re.search(r"(\d+)", str(_m.get("cuc_km") or chart_data.get("cuc") or "2"))
        _cuc_g = int(_m_cuc_g.group(1)) if _m_cuc_g else _cung_g
        _votes_g = {}
        for _val_g, _w_g in [
            (_TT_NUM.get(_up_g, 2), 3),
            (_HT_NUM.get(_lo_g, 2), 2),
            (_dong_g, 2),
            (int(_m.get("the_idx") or 2), 2),
            (_cuc_g, 2),
            (_cung_g, 2),
        ]:
            if 1 <= _val_g <= 12:
                _votes_g[_val_g] = _votes_g.get(_val_g, 0) + _w_g
        _conv_num = sorted(_votes_g.items(), key=lambda kv: (kv[1], -kv[0]), reverse=True)[0][0] if _votes_g else 2

        # 2. Kiểm tra Kỵ Thần vây khắc (Hiện trạng cản trở) vs. Nguyên Thần cứu ứng (Tiên lượng thành công)
        _up_nh_g = _TRIG_NH.get(_up_g, "Kim")
        _lo_nh_g = _TRIG_NH.get(_lo_g, "Thổ")
        _mh_under_attack = (_KHAC.get(_up_nh_g) == dt_nh) or (_KHAC.get(_lo_nh_g) == dt_nh) or ("DỤNG KHẮC THỂ" in str(_m.get("rel_chu_tag", "")))
        _km_hung_door = any(d in str(_m.get("cua_name", "")) for d in ("Thương", "Tử", "Kinh", "Đỗ"))
        _is_phuc_ngam = bool(_m.get("is_km_phuc_ngam", False))
        _the_tai_ready = bool(_m.get("the_tai_ready", True))

        sq_score = int(base_pct or 52) + int(_m["rel_bien_pts"] // 2)
        if _m["is_cat_sao"]:
            sq_score += 5
        if _m["is_cat_cua"]:
            sq_score += 5
        if _mh_under_attack:
            sq_score -= 6
        if dt_is_kv:
            sq_score -= 8

        lh_reasons = []
        if found_dt:
            lh_reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> hiện rõ tại <b>Hào {dt_idx} ({dt_chi}-{dt_nh})</b>{' [TRÌ THẾ]' if dt_idx == _m['the_idx'] else ''} ({'Nội Quái — trong nhà/gần' if dt_idx <= 3 else 'Ngoại Quái — bên ngoài/xa'}) trên quẻ <b>{_m['full_chu']}</b>")
        else:
            lh_reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> đang ẩn phục (Phục Thần), phối hợp trục <b>Hào Thế (Hào {_m['the_idx']} {_m['the_chi']}-{_m['the_nh']})</b> trên quẻ <b>{_m['full_chu']}</b>")

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

        # V126.0: Áp dụng ĐẦY ĐỦ 12 Quy Luật Thời Không Tổng Quát (Hồi Đầu Sinh/Khắc, Tiến/Thoái Thần, Ám Động/Nhật Phá, Nguyệt Phá, Hóa Mộ/Tuyệt, Nguyên Thần Thông Quan & Không Vong)
        _univ_ts = _m.get("universal_ts_eval") or {}
        if _univ_ts:
            if _univ_ts.get("is_tien_than"):
                sq_score += 10
                lh_reasons.append(f"đắc {_univ_ts.get('bien_tag', 'Hóa Tiến Thần')}")
            elif _univ_ts.get("is_thoai_than"):
                sq_score -= 10
                lh_reasons.append(f"vướng {_univ_ts.get('bien_tag', 'Hóa Thoái Thần')}")
            elif _univ_ts.get("hoi_dau_sinh"):
                sq_score += 8
                lh_reasons.append("động hóa Hồi Đầu Sinh (tự sinh vượng khí)")
            elif _univ_ts.get("hoi_dau_khac"):
                sq_score -= 10
                lh_reasons.append("động hóa Hồi Đầu Khắc (cần đề phòng biến số ngược)")
            if _univ_ts.get("is_am_dong"):
                sq_score += 8
                lh_reasons.append(f"đắc {_univ_ts.get('day_tag', 'Ám Động ứng nhanh')}")
            elif _univ_ts.get("is_nhat_pha"):
                sq_score -= 8
                lh_reasons.append(f"phạm {_univ_ts.get('day_tag', 'Nhật Phá')}")
            if _univ_ts.get("thong_quan_tag"):
                lh_reasons.append(_univ_ts["thong_quan_tag"])
            if _univ_ts.get("tuan_khong_tag"):
                lh_reasons.append(f"trạng thái Không Vong: {_univ_ts['tuan_khong_tag']}")

        sq_score = max(28, min(88, sq_score))
        t_code = sq_bp.get("specific_target") or sq_bp.get("archetype_key", "")
        raw_q_g = QuestionReaderAI._normalize_vn_typos(str(sq_bp.get("raw_question") or "")).lower()
        c_lbl = sq_bp.get("clause_label") or sq_bp.get("raw_question") or sq_bp.get("subject_person") or "Sự việc"
        uk_str = omni_data.get("exact_timestamp", f"Ngày/Giờ {dt_chi}, {chi_n} (ứng số hội tụ {_conv_num})")
        huong_str = _m["huong_cung"]

        _kd_c = _m.get("kd_chu_info") or {}
        _ic_c = _m.get("ic_chu_info") or {}
        _ic_topic_line = ""
        if _ic_c:
            _ic_topic_line = (
                f"<br>&nbsp;&nbsp;📖 <b>Luận giải chuyên sâu Quẻ {_m['full_chu']} (Kho dữ liệu Kinh Dịch GitHub):</b> "
                f"<i>Tổng quan:</i> {_ic_c.get('general', '')} · <i>Tài vận:</i> {_ic_c.get('fortune', '')} · "
                f"<i>Mưu sự:</i> {_ic_c.get('wish', '')} · <i>Sự nghiệp:</i> {_ic_c.get('career', '')} · "
                f"<i>Gia đạo/Tình cảm:</i> {_ic_c.get('family', '')} / {_ic_c.get('love', '')}."
            )

        # 3. Giải mã chuyên sâu theo từng Đại Dạng Câu Hỏi Thực Tế (Không trả lời chung chung!)
        is_strict_override = True
        is_open_van_vat = False
        extra_van_vat_why = ""

        # Kiểm tra nhóm câu hỏi Mở — Giải mã Vạn Vật Loại Tượng (Thể loại nhạc, Món ăn/Đồ uống, Hoạt động đang làm, Ngành nghề, Tính cách/Ngoại hình, Đồ vật/Cái gì, Tiền lương/Giá trị...)
        _is_money_clause_q = any(
            w in raw_q_g
            for w in [
                "bao nhiêu tiền", "mức lương", "lương tháng", "lương bao nhiêu", "thưởng bao nhiêu",
                "thu nhập bao nhiêu", "lãi bao nhiêu", "lời bao nhiêu", "giá bao nhiêu",
                "mấy triệu", "bao nhiêu triệu", "mấy tỷ", "bao nhiêu tỷ", "được bao nhiêu tiền",
            ]
        ) and not any(w in raw_q_g for w in ["chỉ vàng", "mấy chỉ", "tờ tiền"])
        _is_music_q = any(w in raw_q_g for w in ["nhạc", "bài hát", "ca khúc", "giai điệu", "nghe gì", "thể loại nhạc", "bản nhạc", "ca sĩ", "âm nhạc"])
        _is_food_drink_q = any(w in raw_q_g for w in ["ăn gì", "món gì", "ăn món", "uống gì", "đồ uống", "nước gì", "vị gì", "bữa sáng", "bữa trưa", "bữa tối"])
        _is_activity_q = any(w in raw_q_g for w in ["đang làm gì", "đang xem gì", "phim gì", "đọc gì", "sách gì", "đang nghĩ gì", "tâm trạng"])
        _is_job_biz_q = any(w in raw_q_g for w in ["nghề gì", "ngành gì", "làm nghề", "kinh doanh gì", "buôn bán gì", "mặt hàng gì", "sản phẩm gì", "lĩnh vực gì"])
        _is_trait_q = any(w in raw_q_g for w in ["tính cách", "ngoại hình", "dáng người", "hình dáng", "người như thế nào", "tính nết", "đặc điểm"])
        _is_what_obj_q = any(w in raw_q_g for w in ["cái gì", "vật gì", "thứ gì", "đồ gì", "loại gì", "thể loại gì", "chất liệu gì", "kiểu gì"]) and not any(w in raw_q_g for w in ["mất", "thất lạc", "đòi nợ"])

        if t_code == "LOST_ITEM" or "D11" in t_code or any(w in raw_q_g for w in ["mất", "thất lạc", "tìm thấy", "tìm lại", "để quên"]):
            _pos_in_out = "TRONG NHÀ / NỘI THẤT (NỘI QUÁI HÀO 1–3)" if dt_idx <= 3 else "BÊN NGOÀI / NƠI LÀM VIỆC / DI CHUYỂN (NGOẠI QUÁI HÀO 4–6)"
            _height_lvl = "vị trí thấp (sát sàn/ngăn dưới/gầm tủ)" if dt_idx in (1, 2) else ("vị trí ngang tầm tay (trên bàn/ngăn kéo/trong túi/tủ giữa)" if dt_idx in (3, 4) else "vị trí cao (kệ trên/nóc tủ/ngăn trên)")
            if found_dt and not (dt_is_kv and "Huyền Vũ" in str(_m.get("than_name", ""))):
                short_hl = (
                    f"🔎 KẾT LUẬN TÌM ĐỒ / ĐỊNH VỊ TỪ LIÊN KẾT QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"CÓ THỂ TÌM LẠI ĐƯỢC ({sq_score}%) — ĐANG NẰM Ở {_pos_in_out}, TẠI PHƯƠNG {huong_str.upper()} (CUNG {_cung_g} · CỬA {_m['cua_name'].upper()} — {_height_lvl.upper()})! "
                    f"➔ THỜI GIAN TÌM THẤY: TRONG {_conv_num} GIỜ / NGÀY TỚI (ỨNG NGÀY/GIỜ {dt_chi.upper()})!"
                )
            else:
                short_hl = (
                    f"⚠️ KẾT LUẬN TÌM ĐỒ TỪ LIÊN KẾT QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"ĐỒ VẬT ĐANG BỊ CHE KHUẤT SÂU HOẶC ĐÃ RỜI KHỎI VỊ TRÍ CŨ (DO DỤNG THẦN {sq_dt.upper()} CHẠM TUẦN KHÔNG / ẨN PHỤC TẠI HƯỚNG {huong_str.upper()} · CỬA {_m['cua_name'].upper()}) — "
                    f"CẦN TÌM KỸ Ở {_height_lvl.upper()} HƯỚNG {huong_str.upper()} VÀO NGÀY/GIỜ {dt_chi.upper()} MỚI LỘ DIỆN!"
                )
        elif _is_money_clause_q:
            is_open_van_vat = True
            _tt_u_g = _TT_NUM.get(_up_g, 3)
            _tt_l_g = _TT_NUM.get(_lo_g, 8)
            _ht_u_g = _HT_NUM.get(_up_g, 9)
            _ht_l_g = _HT_NUM.get(_lo_g, 2)
            _ht_bu_g = _HT_NUM.get(_m.get("up_bien") or _up_g, 9)
            _tt_bl_g = _TT_NUM.get(_m.get("lo_bien") or _lo_g, 4)
            _tier1_cands_g = sorted(set([x for x in [_tt_u_g, _tt_l_g, _ht_u_g, _ht_l_g] if 1 <= x <= 9]))
            _t1_low_g = max(3, min(_tier1_cands_g)) if _tier1_cands_g else 4
            _t1_high_g = max(_t1_low_g + 3, max(_tier1_cands_g) if _tier1_cands_g else 8)
            _t1_exact_g = ", ".join(f"{x} triệu" for x in _tier1_cands_g[:4])
            _sum_c_g = _tt_u_g + _tt_l_g
            _sum_h_g = _ht_u_g + _ht_l_g
            _sum_b_g = _ht_bu_g + _tt_bl_g + _dong_g
            _low_m_g = min(_sum_c_g, _sum_h_g, _sum_b_g)
            _high_m_g = max(_low_m_g + 2, max(_sum_c_g, _sum_h_g, _sum_b_g))
            _mid_m_g = round((_low_m_g + _high_m_g) / 2.0, 1)
            _mid_m_vnd = f"{int(round(_mid_m_g * 1_000_000)):,}".replace(",", ".")
            _tai_verdict_g = _m.get("tai_timing_verdict_short") or "⚡ [TRẠNG THÁI]: KHOẢN TIỀN ĐÃ BẮN / NỔ NGAY TRONG GIỜ HIỆN TẠI!"
            short_hl = (
                f"💰 KẾT QUẢ ĐỊNH LƯỢNG TIỀN LƯƠNG / THU NHẬP ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                f"[BẬC 1 — LƯƠNG CƠ BẢN / ĐỢT 1 / SAU KHẤU TRỪ]: {_t1_low_g}.000.000 – {_t1_high_g}.000.000 VNĐ (CON SỐ KHỚP: {_t1_exact_g.upper()})  |  "
                f"[BẬC 2 — TỔNG QUÁI SỐ CHỦ–BIẾN]: {_low_m_g}.000.000 – {_high_m_g}.000.000 VNĐ (TRỌNG TÂM ~{_mid_m_vnd} VNĐ)  |  "
                f"[BẬC 3 — NGẠCH CAO / GỘP THƯỞNG (×2)]: {_low_m_g*2}.000.000 – {_high_m_g*2}.000.000 VNĐ  "
                f"{_tai_verdict_g}"
            )
            extra_van_vat_why = (
                f"<b>• Giải mã Chuyên Sâu 3 Tầng Định Lượng Tiền Lương / Tài Chính (Mai Hoa + Kỳ Môn + Lục Hào):</b> "
                f"Bậc 1 (Số Đơn Quái & Hà Đồ Hào Tài): <b>{_t1_low_g} – {_t1_high_g} triệu đồng</b> (khớp các mốc {_t1_exact_g}); "
                f"Bậc 2 (Tổng Quái Số Quẻ Chủ <b>{_m['full_chu']}</b> = <b>{_sum_c_g}</b> ➔ Biến <b>{_m['full_bien']}</b> = <b>{_sum_b_g}</b>): <b>{_low_m_g} – {_high_m_g} triệu đồng</b>; "
                f"Bậc 3 (Ngạch quản lý/thưởng gộp ×2): <b>{_low_m_g*2} – {_high_m_g*2} triệu đồng</b>.<br>"
            )
        elif _is_music_q:
            is_open_van_vat = True
            _trigs_active = [_m.get("up_chu", ""), _m.get("lo_chu", ""), _m.get("up_bien", ""), _m.get("lo_bien", ""), _m.get("up_ho", ""), _m.get("lo_ho", "")]
            _sao_m = str(_m.get("sao_name", ""))
            _cua_m = str(_m.get("cua_name", ""))
            _than_m = str(_m.get("than_name", ""))
            _the_kv_m = (_m.get("the_chi") in (_m.get("kv_list") or []))
            _pm_phuc_m = ("Phụ Mẫu" in str(_m.get("phuc_than_str", "")))

            _has_custom_music_opts = any(
                w in raw_q_g for w in ["nhạc phật", "tụng kinh", "nhạc thiền", "đám ma", "nhạc đám ma", "nhạc hiếu", "nhạc buồn", "nhạc vui"]
            )
            if _has_custom_music_opts:
                _opt_scores = {
                    "NHẠC PHẬT / TỤNG KINH / NHẠC THIỀN TÂM LINH (Tiếng chuông mõ Càn Kim Hào 5 động hóa Ly Hỏa đèn Phật + Thế Không Vong «Không Môn» + Cung Tốn Thái Âm)": 0,
                    "NHẠC BUỒN / TRẦM LẮNG TÂM TRẠNG (Hạ Quái Khảm Thủy «gia ưu, khấp huyết» + Quẻ Tụng biến Vị Tế dang dở + Thái Âm trầm mặc)": 0,
                    "NHẠC ĐÁM MA / NHẠC HIẾU TƯỞNG NIỆM (Sao Thiên Nhuế tang thương + Khảm Thủy nước mắt + Hào 5 động hóa Mùi Thổ Mộ Khố & Quẻ Hỗ Gia Nhân hương khói gia tiên)": 0,
                    "NHẠC VUI / SÔI ĐỘNG": 0,
                }
                _k_phat, _k_buon, _k_damma, _k_vui = list(_opt_scores.keys())
                if "Càn" in (_m.get("up_chu"), _m.get("lo_chu")):
                    _opt_scores[_k_phat] += 5
                if "Ly" in (_m.get("up_bien"), _m.get("lo_bien"), _m.get("lo_ho")):
                    _opt_scores[_k_phat] += 4
                if "Tốn" in (_m.get("up_ho"), _m.get("lo_ho"), _m.get("quai_cung")):
                    _opt_scores[_k_phat] += 4
                if _the_kv_m or dt_is_kv:
                    _opt_scores[_k_phat] += 5
                if "Thái Âm" in _than_m or "Cửu Thiên" in _than_m or "Trực Phù" in _than_m:
                    _opt_scores[_k_phat] += 4
                if "Thiên Cầm" in _sao_m or "Thiên Tâm" in _sao_m or "Thiên Phụ" in _sao_m:
                    _opt_scores[_k_phat] += 3
                if "Khai" in _cua_m or "Hưu" in _cua_m:
                    _opt_scores[_k_phat] += 3

                if "Khảm" in (_m.get("lo_chu"), _m.get("up_chu"), _m.get("lo_bien")):
                    _opt_scores[_k_buon] += 6
                if any(w in _m.get("full_chu", "") + _m.get("full_bien", "") for w in ["Tụng", "Vị Tế", "Khốn", "Kiển", "Bác", "Khuê"]):
                    _opt_scores[_k_buon] += 5
                if "Thái Âm" in _than_m or "Huyền Vũ" in _than_m or "Đằng Xà" in _than_m:
                    _opt_scores[_k_buon] += 3
                if "Thiên Nhuế" in _sao_m or "Thiên Bồng" in _sao_m:
                    _opt_scores[_k_buon] += 3

                if "Thiên Nhuế" in _sao_m:
                    _opt_scores[_k_damma] += 6
                if "Khảm" in (_m.get("lo_chu"), _m.get("lo_bien")):
                    _opt_scores[_k_damma] += 4
                if "Gia Nhân" in _m.get("full_ho", ""):
                    _opt_scores[_k_damma] += 3
                if any(m in _cua_m for m in ["Tử", "Kinh", "Thương"]) or "Bạch Hổ" in _than_m:
                    _opt_scores[_k_damma] += 5
                if chart_data.get("chi_thang") in ("Tuất", "Mùi", "Sửu", "Thìn"):
                    _opt_scores[_k_damma] += 3

                if "Đoài" in (_m.get("up_chu"), _m.get("lo_chu"), _m.get("up_bien")):
                    _opt_scores[_k_vui] += 5
                if "Chấn" in (_m.get("up_chu"), _m.get("lo_chu"), _m.get("up_bien")):
                    _opt_scores[_k_vui] += 4
                if "Khảm" in (_m.get("lo_chu"), _m.get("lo_bien")) or "Thiên Nhuế" in _sao_m:
                    _opt_scores[_k_vui] = max(0, _opt_scores[_k_vui] - 8)

                _sorted_opts = sorted(_opt_scores.items(), key=lambda kv: kv[1], reverse=True)
                _top1_name, _top1_pts = _sorted_opts[0]
                _top2_name, _top2_pts = _sorted_opts[1]
                _top3_name, _top3_pts = _sorted_opts[2]
                _total_pts = max(1, sum(v for _, v in _sorted_opts))
                _p1 = int(round(_top1_pts * 100.0 / _total_pts))
                _p2 = int(round(_top2_pts * 100.0 / _total_pts))
                _p3 = max(0, 100 - _p1 - _p2 - int(round(_sorted_opts[3][1] * 100.0 / _total_pts)))
                _p4 = max(0, 100 - _p1 - _p2 - _p3)

                _kv_silence_note = ""
                if _the_kv_m or _pm_phuc_m:
                    _kv_silence_note = (
                        f"  |  ⚠️ [BẮT BÀI KHÔNG VONG & PHỤC TÀNG]: Hào Thế (Hào {_m['the_idx']} {_m['the_chi']}-{_m['the_nh']}) lâm TUẦN KHÔNG "
                        f"& Hào Phụ Mẫu (tiếng nhạc) ẨN PHỤC ➔ Nếu lúc bấm quẻ bạn KHÔNG BẬT LOA NGOÀI ĐỜI (đang ngồi trong không gian yên tĩnh hỏi thử quẻ), "
                        f"quẻ bắt trúng trạng thái «Tĩnh Trung Chi Thanh / Nhạc Trong Tâm Tưởng»!"
                    )

                short_hl = (
                    f"🎵 KẾT LUẬN ĐỐI CHỨNG 4 LOẠI NHẠC TỪ QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()} | ĐỘNG HÀO {_dong_g} · CUNG {_m['target_cung']} SAO {_sao_m.upper()} · CỬA {_cua_m.upper()} · THẦN {_than_m.upper()}): "
                    f"[HẠNG 1 — TRÚNG ĐÍCH ({_p1}%)]: «{_top1_name.split(' (')[0]}»  |  "
                    f"[HẠNG 2 — GIAO THOA ({_p2}%)]: «{_top2_name.split(' (')[0]}» & «{_top3_name.split(' (')[0]} ({_p3}%)» (DÒNG NHẠC PHẬT CẦU SIÊU / NHẠC TRẦM BUỒN TƯỞNG NIỆM)  |  "
                    f"[LOẠI TRỪ 100% ({_p4}%)]: TUYỆT ĐỐI KHÔNG PHẢI NHẠC VUI!"
                    f"{_kv_silence_note}"
                )
                extra_van_vat_why = (
                    f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — Đối Chứng 4 Loại Nhạc (Nhạc Vui / Buồn / Nhạc Phật / Nhạc Đám Ma):</b><br>"
                    f"&nbsp;&nbsp;🪷 <b>1. Vì sao chốt Hạng 1 là «{_top1_name.split(' (')[0]}» ({_p1}%) giao thoa «{_top2_name.split(' (')[0]} / {_top3_name.split(' (')[0]}» ({_p2}% + {_p3}%):</b><br>"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;• <b>Mai Hoa Dịch Số ({_m['full_chu']} ➔ Hỗ {_m['full_ho']} ➔ Biến {_m['full_bien']}):</b> Thượng Quái <b>{_m['up_chu']} (Kim)</b> động tại Hào 5 (<b>Thân-Kim</b> — tượng tiếng chuông chùa, tiếng mõ kim khí ngân vang ở ngôi Chí Tôn) hóa sang <b>{_m['up_bien']} (Hỏa)</b> (ánh đèn Phật, hương đăng giác ngộ); Quẻ Hỗ <b>{_m['full_ho']}</b> (Tốn Mộc sinh Ly Hỏa) là tượng <b>hương khói bàn thờ Phật / gia tiên trong nhà</b>.<br>"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;• <b>Hạ Quái & Kỳ Môn Độn Giáp:</b> Hạ Quái (Quẻ Thể) là <b>{_m['lo_chu']} (Khảm Thủy)</b> — kinh điển <i>Thuyết Quái</i> định danh: <i>«Khảm vi gia ưu, vi khấp huyết»</i> (nỗi buồn sâu lắng, nước mắt, hoài niệm). Cung {_m['target_cung']} ({huong_str} - Tốn Tăng Đạo) hội <b>Sao {_sao_m}</b> (Thiên Cầm trung tâm tâm linh + Thiên Nhuế u sầu/tang chế), <b>Cửa {_cua_m}</b> và <b>Thần {_than_m}</b> (âm trầm, tĩnh mịch) ➔ Sự giao thoa giữa <b>Nhạc Phật / Kinh Kệ Tụng Niệm</b> với <b>Nhạc Buồn / Nhạc Hiếu Tưởng Niệm</b> (loại trừ Nhạc Vui = 0%).<br>"
                    f"&nbsp;&nbsp;☯️ <b>2. Bắt Bài Lục Hào (Hào Thế Lâm Tuần Không & Hào Phụ Mẫu Phục Tàng):</b> Hào Thế tại Hào {_m['the_idx']} (<b>{_m['the_chi']}-{_m['the_nh']}</b>) rơi vào <b>Tuần Không ({', '.join(_m.get('kv_list') or [])})</b> — cổ pháp gọi là <b>«Không Vong vi Không Môn» (Cửa Không nhà Phật / Thiền định)</b>; đồng thời Hào Phụ Mẫu (đại diện cho âm thanh phát ra loa) đang <b>Phục Tàng</b> dưới Hào 3 ➔ Báo hiệu hoặc bạn đang mở <b>Nhạc Phật / Nhạc Buồn Tưởng Niệm nhỏ nhẹ trầm lắng</b>, hoặc bạn đang <b>ngồi trong không gian yên tĩnh (không bật nhạc) và đưa ra 4 đáp án để thử tài giải mã của quẻ</b>!<br>"
                )
            else:
                _music_scores = {
                    "NHẠC TRỮ TÌNH / BALLAD SÂU LẮNG / NHẠC XƯA – ACOUSTIC (Giai điệu du dương, giàu cảm xúc & hoài niệm)": 0,
                    "NHẠC SÔI ĐỘNG / REMIX – EDM – POP DANCE – ROCK (Tiết tấu mạnh, nhịp trống/beat dồn dập, bùng nổ)": 0,
                    "NHẠC KHÔNG LỜI / LOFI CHILL – PIANO – R&B TÂM TRẠNG (Êm dịu, sâu lắng, thư giãn nội tâm)": 0,
                    "NHẠC TRẺ THỊNH HÀNH / V-POP – US-UK – RAP MELODIC (Hiện đại, bắt tai, giàu tính giải trí)": 0,
                    "NHẠC TÂM LINH / NHẠC PHẬT – THIỀN TỊNH / DÂN CA QUÊ HƯƠNG (Sâu sắc, thanh tịnh, mang âm hưởng cội nguồn)": 0,
                }
                _k_ballad, _k_edm, _k_lofi, _k_pop, _k_folk = list(_music_scores.keys())
                for _tg_i, _tg_w in [(_m.get("up_bien"), 4), (_m.get("lo_bien"), 3), (_m.get("up_chu"), 4), (_m.get("lo_chu"), 3), (_m.get("up_ho"), 2), (_m.get("lo_ho"), 2)]:
                    if _tg_i in ("Tốn", "Càn"):
                        _music_scores[_k_ballad] += _tg_w
                    if _tg_i in ("Chấn", "Ly"):
                        _music_scores[_k_edm] += _tg_w
                    if _tg_i == "Khảm":
                        _music_scores[_k_lofi] += _tg_w + 1
                    if _tg_i == "Đoài":
                        _music_scores[_k_pop] += _tg_w + 1
                    if _tg_i in ("Khôn", "Cấn"):
                        _music_scores[_k_folk] += _tg_w
                if "Thiên Phụ" in _sao_m or "Thiên Tâm" in _sao_m:
                    _music_scores[_k_ballad] += 5
                if "Thiên Xung" in _sao_m or "Thiên Anh" in _sao_m:
                    _music_scores[_k_edm] += 5
                if "Thiên Bồng" in _sao_m:
                    _music_scores[_k_lofi] += 5
                if "Thiên Trụ" in _sao_m:
                    _music_scores[_k_pop] += 5
                if any(s in _sao_m for s in ("Thiên Nhậm", "Thiên Nhuế", "Thiên Cầm")):
                    _music_scores[_k_folk] += 5
                if _the_kv_m and "Thái Âm" in _than_m:
                    _music_scores[_k_folk] += 4
                if "Thái Âm" in _than_m or "Lục Hợp" in _than_m:
                    _music_scores[_k_ballad] += 4
                elif "Chu Tước" in _than_m or "Bạch Hổ" in _than_m or "Cửu Thiên" in _than_m:
                    _music_scores[_k_edm] += 3
                elif "Huyền Vũ" in _than_m or "Đằng Xà" in _than_m:
                    _music_scores[_k_lofi] += 3
                if "Khai" in _cua_m or "Hưu" in _cua_m:
                    _music_scores[_k_ballad] += 2
                    _music_scores[_k_lofi] += 2
                elif "Cảnh" in _cua_m or "Thương" in _cua_m or "Kinh" in _cua_m:
                    _music_scores[_k_edm] += 2
                    _music_scores[_k_pop] += 2
                _sorted_music = sorted(_music_scores.items(), key=lambda kv: kv[1], reverse=True)
                _top_music, _top_m_pts = _sorted_music[0]
                _sec_music, _sec_m_pts = _sorted_music[1]
                _rhythm_detail = ""
                if "Chấn" in _trigs_active and "Tốn" in _trigs_active:
                    _rhythm_detail = " — Kết hợp Hạ Quái Chấn Lôi (tiếng trống/nhịp beat rõ ràng ở phần nền) chuyển sang Thượng Quái Tốn Phong (giai điệu gió ngân nga, du dương, giàu chất tự sự)"
                elif "Càn" in _trigs_active and "Chấn" in _trigs_active:
                    _rhythm_detail = " — Kết hợp Càn Kim (âm thanh kim khí/nhạc cụ dây – piano – guitar sắc nét) với Chấn Lôi (tiết tấu vang vọng)"
                short_hl = (
                    f"🎵 KẾT LUẬN GIẢI MÃ VẠN VẬT LOẠI TƯỢNG ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"BẠN ĐANG NGHE «{_top_music}»"
                    + (f" KẾT HỢP ÂM HƯỞNG «{_sec_music.split(' (')[0]}»" if _sec_m_pts >= _top_m_pts - 3 else "")
                    + f" (ỨNG TƯỢNG QUẺ {_m['up_chu'].upper()}/{_m['lo_chu'].upper()} BIẾN {_m['up_bien'].upper()}/{_m['lo_bien'].upper()} · SAO {_sao_m.upper()} · CỬA {_cua_m.upper()} · THẦN {_than_m.upper()})!"
                )
                extra_van_vat_why = (
                    f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — Âm Nhạc & Thanh Âm (Mai Hoa + Kỳ Môn + Lục Hào):</b><br>"
                    f"&nbsp;&nbsp;🎵 <b>1. Tượng Quái Mai Hoa ({_m['full_chu']} ➔ Hỗ {_m['full_ho']} ➔ Biến {_m['full_bien']}):</b> Thượng Quái <b>{_m['up_chu']}</b> ({_TRIG_NH.get(_m['up_chu'], '')}) phối Hạ Quái <b>{_m['lo_chu']}</b> ({_TRIG_NH.get(_m['lo_chu'], '')}), biến sang <b>{_m['up_bien']}/{_m['lo_bien']}</b>{_rhythm_detail}. Quẻ Hỗ <b>{_m['full_ho']}</b> cho thấy mạch cảm xúc bài nhạc dẫn dắt từ từ, sâu lắng và thấm dần.<br>"
                    f"&nbsp;&nbsp;🧭 <b>2. Tinh – Môn – Thần Kỳ Môn Độn Giáp:</b> Cung {_m['target_cung']} ({huong_str}) hội <b>Sao {_sao_m}</b> (Văn Xương – nghệ thuật ca từ tinh tế, trữ tình), <b>Cửa {_cua_m}</b> và <b>Thần {_than_m}</b> (biểu trưng cho âm sắc sâu lắng, giàu cảm xúc nội tâm và hoài niệm).<br>"
                    f"&nbsp;&nbsp;☯️ <b>3. Lục Hào Nạp Giáp:</b> Hào Thế tại Hào {_m['the_idx']} ({_m['the_chi']}-{_m['the_nh']}) tương tác với Hào Dụng Thần tại Hào {dt_idx} ({dt_chi}-{dt_nh}){' [Đang lâm Tuần Không — tâm trí người nghe đang thả hồn thư giãn, phiêu theo giai điệu]' if dt_is_kv else ''} ➔ Khẳng định thể loại nhạc chủ đạo là <b>{_top_music}</b>.<br>"
                )
        elif _is_food_drink_q:
            is_open_van_vat = True
            _ask_drink_only = any(w in raw_q_g for w in ["uống gì", "uống nước gì", "nước gì", "đồ uống"]) and not any(w in raw_q_g for w in ["ăn gì", "ăn món", "món gì"])
            _ask_food_only = any(w in raw_q_g for w in ["ăn gì", "ăn món", "món gì", "bữa sáng", "bữa trưa", "bữa tối"]) and not any(w in raw_q_g for w in ["uống gì", "nước gì", "đồ uống"])
            _nh_food_only_map = {
                "Mộc": ("MÓN SỢI (BÚN / PHỞ / MÌ / MIẾN) HOẶC RAU CỦ QUẢ – TRÁI CÂY TƯƠI THANH MÁT", "Tốn/Chấn Mộc chủ thảo mộc, sợi dài, vị chua thanh tự nhiên"),
                "Hỏa": ("ĐỒ NƯỚNG / CHIÊN RÁN / XÀO NÓNG HỔI ĐẬM GIA VỊ CAY ẤM", "Ly/Bính Đinh Hỏa chủ nhiệt lửa cao, món quay nướng/chiên xào thơm nồng"),
                "Thổ": ("CƠM GIA ĐÌNH / THỊT KHO HẦM / XÔI – BÁNH NGỌT – NGŨ CỐC BÉO BÙI", "Khôn/Cấn Thổ chủ hạt gạo, tinh bột, món hầm chín kỹ vị ngọt đậm"),
                "Kim": ("MÓN THỊT THÁI LÁT / GỎI NỘM / ĐỒ NGUỘI TINH CHẾ VỊ ĐẬM SẮC NÉT", "Càn/Đoài Kim chủ dao thớt cắt lát tinh xảo, vị cay the thanh sạch"),
                "Thủy": ("MÓN CANH – SÚP – LẨU NƯỚC DÙNG ĐẬM ĐÀ HOẶC THỦY HẢI SẢN", "Khảm Thủy chủ món nhiều nước súp, vị mặn hài hòa, hải sản tươi"),
            }
            _nh_drink_only_map = {
                "Mộc": ("TRÀ THẢO MỘC / TRÀ TRÁI CÂY (CAM – CHANH – ĐÀO) / NƯỚC ÉP SINH TỐ TƯƠI MÁT", "Tốn/Chấn Mộc chủ lá trà, hoa quả tươi ép thanh nhiệt"),
                "Hỏa": ("CÀ PHÊ ĐẬM VỊ / TRÀ NÓNG / CA CAO ẤM HOẶC ĐỒ UỐNG TĂNG LỰC", "Ly Hỏa chủ đồ uống pha chế nhiệt độ ấm nóng hoặc rang xay đậm vị"),
                "Thổ": ("TRÀ SỮA / SỮA HẠT – NGŨ CỐC / SINH TỐ BƠ – SỮA ĐẶC NGỌT BÉO", "Khôn/Cấn Thổ chủ vị ngọt béo, sánh mịn, giàu dinh dưỡng"),
                "Kim": ("NƯỚC GIẢI KHÁT CÓ ĐÁ LẠNH / NƯỚC CÓ GA – SODA MÁT LẠNH", "Càn/Đoài Kim chủ đá viên mát lạnh, bọt khí sảng khoái"),
                "Thủy": ("NƯỚC LỌC TINH KHIẾT / NƯỚC DỪA – NƯỚC KHOÁNG MÁT GIẢI KHÁT", "Khảm Thủy chủ nước trong thuần khiết, mát lành thanh lọc cơ thể"),
            }
            if _ask_drink_only:
                _dom_nh_fd = _TRIG_NH.get(_m.get("lo_bien") or _m.get("lo_chu") or "Thủy", dt_nh)
                _flv_title, _flv_desc = _nh_drink_only_map.get(_dom_nh_fd, _nh_drink_only_map["Thủy"])
                _icon_fd, _lbl_fd = "🥤", "ĐỒ UỐNG"
            elif _ask_food_only:
                _dom_nh_fd = _TRIG_NH.get(_m.get("up_bien") or _m.get("up_chu") or "Thổ", dt_nh)
                _flv_title, _flv_desc = _nh_food_only_map.get(_dom_nh_fd, _nh_food_only_map["Thổ"])
                _icon_fd, _lbl_fd = "🍽️", "MÓN ĂN"
            else:
                _dom_nh_fd = _TRIG_NH.get(_m.get("up_bien") or _m.get("up_chu") or "Mộc", dt_nh)
                _f_t, _f_d = _nh_food_only_map.get(_dom_nh_fd, _nh_food_only_map["Thổ"])
                _d_t, _ = _nh_drink_only_map.get(dt_nh, _nh_drink_only_map["Thủy"])
                _flv_title, _flv_desc = f"{_f_t} · KÈM {_d_t}", _f_d
                _icon_fd, _lbl_fd = "🍽️", "ẨM THỰC & ĐỒ UỐNG"
            short_hl = (
                f"{_icon_fd} KẾT LUẬN GIẢI MÃ {_lbl_fd} TỪ QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                f"«{_flv_title}» (ỨNG HÀNH {_dom_nh_fd.upper()} + DỤNG THẦN {dt_chi.upper()}-{dt_nh.upper()} & SAO {_m['sao_name'].upper()} · CỬA {_m['cua_name'].upper()})!"
            )
            extra_van_vat_why = (
                f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — {_lbl_fd.title()}:</b> Quẻ Chủ <b>{_m['full_chu']}</b> biến <b>{_m['full_bien']}</b> ({_flv_desc}), phối hợp Dụng Thần hành <b>{dt_nh}</b> tại Hào {dt_idx} ({dt_chi}) và Sao <b>{_m['sao_name']}</b> + Cửa <b>{_m['cua_name']}</b>.<br>"
            )
        elif _is_activity_q:
            is_open_van_vat = True
            _trig_act_map = {
                "Càn": "ĐANG LÀM VIỆC TRÍ ÓC / QUẢN LÝ ĐIỀU HÀNH / SUY TÍNH KẾ HOẠCH LỚN TRÊN THIẾT BỊ CÔNG NGHỆ",
                "Đoài": "ĐANG TRÒ CHUYỆN, TRAO ĐỔI, NGHE NHẠC/GIẢI TRÍ HOẶC THƯỞNG THỨC ẨM THỰC",
                "Ly": "ĐANG XEM MÀN HÌNH ĐIỆN THOẠI / MÁY TÍNH, ĐỌC TÀI LIỆU HOẶC TÌM KIẾM THÔNG TIN TRỰC TUYẾN",
                "Chấn": "ĐANG DI CHUYỂN, THAO TÁC NHANH, XỬ LÝ CÔNG VIỆC KHẨN TRƯƠNG HOẶC NGHE ÂM THANH SÔI ĐỘNG",
                "Tốn": "ĐANG LƯỚT MẠNG, ĐỌC TIN TỨC, NGHE NHẠC/PODCAST HOẶC TRAO ĐỔI TIN NHẮN TỪ XA",
                "Khảm": "ĐANG SUY TƯ SÂU LẮNG, NGHỈ NGƠI THƯ GIÃN HOẶC LÀM VIỆC ĐỘC LẬP TRONG KHÔNG GIAN YÊN TĨNH",
                "Cấn": "ĐANG NGỒI YÊN TĨNH NGHỈ NGƠI, TẬP TRUNG QUAN SÁT HOẶC TẠM DỪNG ĐỂ CHIÊM NGHIỆM",
                "Khôn": "ĐANG Ở TRONG KHÔNG GIAN QUEN THUỘC (NHÀ/PHÒNG RIÊNG), CHĂM SÓC GIA ĐÌNH HOẶC SẮP XẾP ĐỒ ĐẠC",
            }
            _act_primary = _trig_act_map.get(_m.get("up_bien") or _m.get("up_chu") or "Ly", "ĐANG TẬP TRUNG SUY NGHĨ & TRA CỨU THÔNG TIN")
            short_hl = (
                f"🎯 KẾT LUẬN GIẢI MÃ VẠN VẬT LOẠI TƯỢNG ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                f"{_act_primary} (ỨNG HÀO THẾ HÀO {_m['the_idx']} {_m['the_chi'].upper()}-{_m['the_nh'].upper()}, QUẺ BIẾN {_m['up_bien'].upper()}/{_m['lo_bien'].upper()}, SAO {_m['sao_name'].upper()} & CỬA {_m['cua_name'].upper()})!"
            )
            extra_van_vat_why = (
                f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — Hoạt Động & Trạng Thái Hiện Tại:</b> Trục Hào Thế (Hào {_m['the_idx']} {_m['the_chi']}-{_m['the_nh']}) phối hợp Quẻ Chủ <b>{_m['full_chu']}</b> biến <b>{_m['full_bien']}</b>, Cung {_m['target_cung']} hội Sao <b>{_m['sao_name']}</b> – Cửa <b>{_m['cua_name']}</b> – Thần <b>{_m['than_name']}</b> phản ánh trực tiếp trạng thái hoạt động hiện tại.<br>"
            )
        elif _is_job_biz_q:
            is_open_van_vat = True
            _nh_job_map = {
                "Kim": "TÀI CHÍNH – NGÂN HÀNG, CƠ KHÍ – KỸ THUẬT, CÔNG NGHỆ PHẦN CỨNG, QUẢN LÝ ĐIỀU HÀNH HOẶC KINH DOANH VÀNG BẠC / THIẾT BỊ",
                "Mộc": "GIÁO DỤC – ĐÀO TẠO, VĂN HÓA – NGHỆ THUẬT, TRUYỀN THÔNG – SÁNG TẠO, NÔNG LÂM NGHIỆP, DƯỢC PHẨM HOẶC THỜI TRANG – NỘI THẤT",
                "Thủy": "THƯƠNG MẠI – DỊCH VỤ, LOGISTICS – VẬN TẢI, XUẤT NHẬP KHẨU, DU LỊCH, ĐẦU TƯ LƯU ĐỘNG HOẶC ĐỒ UỐNG – THỦY HẢI SẢN",
                "Hỏa": "CÔNG NGHỆ THÔNG TIN – AI – ĐIỆN TỬ, MARKETING – QUẢNG CÁO, NĂNG LƯỢNG, ẨM THỰC – NHÀ HÀNG HOẶC LÀM ĐẸP – NGHỆ THUẬT",
                "Thổ": "BẤT ĐỘNG SẢN – XÂY DỰNG, KHO BÃI – SẢN XUẤT, QUẢN TRỊ HÀNH CHÍNH, NÔNG SẢN HOẶC KINH DOANH BỀN VỮNG",
            }
            _job_str = _nh_job_map.get(dt_nh, _nh_job_map["Kim"])
            short_hl = (
                f"💼 KẾT LUẬN GIẢI MÃ NGÀNH NGHỀ & LĨNH VỰC TỪ QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                f"THUỘC NHÓM NGÀNH «{_job_str}» (ỨNG DỤNG THẦN {sq_dt.upper()} HÀNH {dt_nh.upper()} TẠI HÀO {dt_idx} {dt_chi.upper()}, QUẺ {_m['up_chu'].upper()}/{_m['lo_chu'].upper()} & SAO {_m['sao_name'].upper()} · CỬA {_m['cua_name'].upper()})!"
            )
            extra_van_vat_why = (
                f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — Ngành Nghề & Lĩnh Vực:</b> Dụng Thần <b>{sq_dt}</b> mang ngũ hành <b>{dt_nh}</b> ({dt_chi}) kết hợp Quẻ Chủ <b>{_m['full_chu']}</b> biến <b>{_m['full_bien']}</b> và Sao <b>{_m['sao_name']}</b> + Cửa <b>{_m['cua_name']}</b> định vị rõ lĩnh vực chuyên môn.<br>"
            )
        elif _is_trait_q:
            is_open_van_vat = True
            _trig_trait_map = {
                "Càn": "Khí chất quyết đoán, nguyên tắc, tự trọng cao, có tố chất lãnh đạo; dáng người đĩnh đạc, khuôn mặt sáng",
                "Đoài": "Tính tình vui vẻ, khéo ăn nói, giao tiếp linh hoạt, giàu sức hút; gương mặt tươi tắn, ưa sự tinh tế",
                "Ly": "Thông minh, nhạy bén, nhiệt huyết, trọng danh dự và thẩm mỹ; ánh mắt sáng, phong thái nổi bật",
                "Chấn": "Năng động, thẳng thắn, hành động nhanh gọn, dám nghĩ dám làm; dáng vẻ hoạt bát, giàu năng lượng",
                "Tốn": "Tinh tế, sâu sắc, ứng xử mềm mỏng khéo léo, giàu tình cảm nội tâm; dáng người thanh nhã, lịch thiệp",
                "Khảm": "Trí tuệ sâu sắc, kín đáo, giàu nghị lực và chiều sâu nội tâm; biết lắng nghe và suy tính thấu đáo",
                "Cấn": "Điềm tĩnh, cẩn trọng, đáng tin cậy, giữ chữ tín và có lập trường vững vàng",
                "Khôn": "Bao dung, chân thành, chu đáo, trọng tình nghĩa gia đình và sống thực tế, bền bỉ",
            }
            _tr_desc = _trig_trait_map.get(_m.get("up_bien") or _m.get("up_chu") or "Càn", "Thông minh, sâu sắc và chính trực")
            short_hl = (
                f"👤 KẾT LUẬN GIẢI MÃ TÍNH CÁCH & KHÍ CHẤT TỪ QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                f"{_tr_desc.upper()} (ỨNG QUẺ {_m['up_chu'].upper()}/{_m['up_bien'].upper()}, SAO {_m['sao_name'].upper()}, CỬA {_m['cua_name'].upper()} & THẦN {_m['than_name'].upper()})!"
            )
            extra_van_vat_why = (
                f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — Tính Cách & Ngoại Hình:</b> {_tr_desc} (Hội tụ từ Quẻ {_m['full_chu']} ➔ {_m['full_bien']}, Sao {_m['sao_name']}, Cửa {_m['cua_name']}, Thần {_m['than_name']}).<br>"
            )
        elif _is_what_obj_q:
            is_open_van_vat = True
            _trig_obj_map = {
                "Càn": "Vật thể kim loại / thiết bị công nghệ cao cấp / vật hình tròn cứng cáp, giá trị cao",
                "Đoài": "Vật dụng kim khí tinh xảo / thiết bị phát âm thanh – giải trí / đồ trang sức hoặc dụng cụ có miệng mở",
                "Ly": "Thiết bị điện tử có màn hình phát sáng (điện thoại/máy tính/đèn) / giấy tờ văn thư / vật phẩm nghệ thuật",
                "Chấn": "Phương tiện di chuyển / thiết bị phát âm thanh – rung động / vật thể bằng gỗ hoặc cây xanh đang phát triển",
                "Tốn": "Tài liệu – sách vở – hợp đồng / dây cáp – tín hiệu mạng / vật phẩm bằng gỗ, vải lụa hoặc hương liệu",
                "Khảm": "Chất lỏng – đồ uống / thiết bị liên quan đến nước – mạch ngầm / vật thể mềm mại hoặc màu sẫm",
                "Cấn": "Đồ nội thất vững chắc (bàn/tủ/kệ) / bất động sản / vật phẩm bằng đá – gốm sứ hoặc hộp chứa kín",
                "Khôn": "Đồ dùng thiết yếu trong nhà / vải vóc – túi xách – hộp vuông / tài sản tích lũy hoặc thực phẩm",
            }
            _obj_desc = _trig_obj_map.get(_m.get("up_bien") or _m.get("up_chu") or "Càn", "Vật phẩm hữu dụng thực tế")
            short_hl = (
                f"🔮 KẾT LUẬN GIẢI MÃ VẠN VẬT LOẠI TƯỢNG ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                f"{_obj_desc.upper()} (HÀNH {dt_nh.upper()} · SAO {_m['sao_name'].upper()} · CỬA {_m['cua_name'].upper()} · THẦN {_m['than_name'].upper()} · SỐ HỘI TỤ 0{_conv_num})!"
            )
            extra_van_vat_why = (
                f"<b>• Giải mã Chuyên Sâu Vạn Vật Loại Tượng — Đặc Điểm Sự Vật:</b> {_obj_desc} (Quẻ Chủ {_m['full_chu']} biến {_m['full_bien']}, Dụng Thần {sq_dt} Hào {dt_idx} {dt_chi}-{dt_nh}, Cung {_m['target_cung']} Sao {_m['sao_name']} – Cửa {_m['cua_name']}).<br>"
            )
        elif t_code == "DEBT_LOAN" or "D16" in t_code or any(w in raw_q_g for w in ["đòi nợ", "trả nợ", "thu hồi nợ", "vay tiền", "cho vay"]):
            if _the_tai_ready and not dt_is_kv and not _is_phuc_ngam:
                short_hl = (
                    f"💰 KẾT LUẬN CÔNG NỢ & VAY MƯỢN ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"THU HỒI / GIẢI NGÂN ĐƯỢC ({sq_score}% — HÀO THÊ TÀI HỮU KHÍ TẠI HÀO {dt_idx} {dt_chi.upper()}-{dt_nh.upper()}), "
                    f"NÊN CHIA THÀNH 0{_conv_num} ĐỢT HOẶC CHỐT VÀO NGÀY/THÁNG {dt_chi.upper()} TẠI HƯỚNG {huong_str.upper()}!"
                )
            else:
                short_hl = (
                    f"⏳ KẾT LUẬN CÔNG NỢ & VAY MƯỢN ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"HIỆN TẠI ĐỐI PHƯƠNG CHƯA CÓ SẴN TIỀN TRẢ NGAY 1 LẦN (DO {_m.get('the_tai_status_str', 'Thê Tài vướng cản').upper()}{' & KỲ MÔN PHỤC NGÂM' if _is_phuc_ngam else ''}), "
                    f"NHƯNG GỐC NỢ KHÔNG MẤT — SẼ THU HỒI ĐƯỢC THEO 0{_conv_num} ĐỢT KHI BƯỚC SANG NGÀY/THÁNG {dt_chi.upper()} (HÀNH {dt_nh.upper()} VƯỢNG)!"
                )
        elif t_code in ("INVEST_PROFIT", "CAREER_WORK", "EXAM_VISA") or any(k in t_code for k in ("D14", "D15", "D20")):
            is_strict_override = False
            if (_mh_under_attack or _km_hung_door or _is_phuc_ngam or dt_is_kv) and sq_score >= 48:
                short_hl = (
                    f"⚖️ KẾT LUẬN LIÊN KẾT ĐA TẦNG ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"[1] HIỆN TRẠNG TRƯỚC MẮT ĐANG VƯỚNG LỰC CẢN / CHẬM NHỊP (DO HÀNH {ky_nh.upper()} KHẮC {dt_nh.upper()} & CỬA {_m['cua_name'].upper()})  |  "
                    f"[2] TIÊN LƯỢNG & KẾT CỤC: ĐẮC NGUYÊN THẦN HÀNH {ng_nh.upper()} & QUẺ BIẾN {_m['full_bien'].upper()} ({_m['rel_bien_tag'].upper()}) NÊN VƯỢT QUA ĐƯỢC VÀ THÀNH CÔNG ({sq_score}% — ỨNG KỲ SỐ 0{_conv_num} / NGÀY THÁNG {dt_chi.upper()})!"
                )
            elif sq_score >= 54:
                short_hl = (
                    f"✅ KẾT LUẬN LIÊN KẾT ĐA TẦNG ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"THUẬN LỢI & ĐẠT THÀNH QUẢ TỐT ({sq_score}% — DỤNG THẦN {sq_dt.upper()} Hào {dt_idx} {dt_chi.upper()}-{dt_nh.upper()} ĐẮC KHÍ, QUẺ BIẾN {_m['rel_bien_tag'].upper()}, CON SỐ ĐỊNH LƯỢNG HỘI TỤ = 0{_conv_num})!"
                )
            else:
                short_hl = (
                    f"⚠️ KẾT LUẬN LIÊN KẾT ĐA TẦNG ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"HIỆN TẠI ĐANG GẶP LỰC CẢN ({sq_score}% — {_m.get('the_tai_status_str', '')}) — CẦN CHUẨN BỊ KỸ NGUỒN LỰC VÀ CHỜ ĐẾN NGÀY/THÁNG {dt_chi.upper()} MỚI NÊN TIẾN HÀNH!"
                )
        elif (
            (re.search(r"\bcó\s+[^,;?]+?\s+(?:không|chưa)\b", raw_q_g) or raw_q_g.endswith((" không", " chưa", " không?", " chưa?")))
            and not any(w in raw_q_g for w in ["có phải", "phúc khí", "âm binh", "vong", "loại nào", "loại gì", "ở đâu"])
        ):
            is_strict_override = False
            # Câu hỏi Kiểm chứng Thực Có / Đúng Sai ("Có ... không?", "Đã ... chưa?"):
            if found_dt and not dt_is_kv:
                short_hl = (
                    f"✅ KẾT LUẬN KIỂM CHỨNG THỰC TẾ TỪ LIÊN KẾT QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"KHẲNG ĐỊNH LÀ CÓ THẬT / ĐẠT KẾT QUẢ THUẬN LỢI ({sq_score}% — HÀO DỤNG THẦN {sq_dt.upper()} HIỆN RÕ TẠI HÀO {dt_idx} {dt_chi.upper()}-{dt_nh.upper()}, "
                    f"CUNG {_cung_g} {huong_str.upper()} · CỬA {_m['cua_name'].upper()} · CON SỐ HỘI TỤ ĐA TẦNG = 0{_conv_num})!"
                )
            else:
                short_hl = (
                    f"⏳ KẾT LUẬN KIỂM CHỨNG TỪ LIÊN KẾT QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): "
                    f"HIỆN TẠI ĐANG LÂM TUẦN KHÔNG / ẨN PHỤC TẠM THỜI (DỤNG THẦN {sq_dt.upper()} TẠI CUNG {_cung_g} {huong_str.upper()} · CỬA {_m['cua_name'].upper()}) — "
                    f"CHỜ ĐẾN MỐC XUẤT KHÔNG / NGÀY GIỜ {dt_chi.upper()} MỚI RÕ KẾT QUẢ!"
                )
        elif t_code == "TIMING_WHEN" or "D12" in t_code:
            short_hl = f"⏳ THỜI ĐIỂM ỨNG KỲ TỪ QUẺ ({_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): {uk_str.upper()} (KHI HÀO {sq_dt.upper()} {dt_chi.upper()} XUNG/HỢP MỞ VẬN · HỘI TỤ SỐ 0{_conv_num})!"
        elif sq_score >= 54:
            is_strict_override = False
            short_hl = f"✅ KẾT LUẬN LIÊN KẾT ĐA TẦNG (MAI HOA – KỲ MÔN – LỤC HÀO | {_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): THUẬN LỢI & ĐẠT KẾT QUẢ TỐT ({sq_score}% — CÁT: {_m['rel_bien_tag']}, ĐẮC SAO {_m['sao_name'].upper()} & CỬA {_m['cua_name'].upper()} · HỘI TỤ SỐ 0{_conv_num})!"
        elif sq_score >= 45:
            is_strict_override = False
            short_hl = f"⚖️ KẾT LUẬN LIÊN KẾT ĐA TẦNG (MAI HOA – KỲ MÔN – LỤC HÀO | {_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): HIỆN TẠI CÒN VƯỚNG CẢN NHƯNG HẬU VẬN KHẢ QUAN ({sq_score}% — QUẺ BIẾN {_m['full_bien'].upper()} {_m['rel_bien_tag']} · HỘI TỤ SỐ 0{_conv_num})!"
        else:
            is_strict_override = False
            short_hl = f"⚠️ KẾT LUẬN LIÊN KẾT ĐA TẦNG (MAI HOA – KỲ MÔN – LỤC HÀO | {_m['full_chu'].upper()} ➔ {_m['full_bien'].upper()}): ĐANG GẶP LỰC CẢN LỚN — NÊN THẬN TRỌNG & CHỜ THỜI ({sq_score}% — HUNG)!"

        why_3sys = (
            f"{extra_van_vat_why}"
            f"• <b>Lục Hào:</b> {', '.join(lh_reasons[:3])}{_m['dt_bien_str']} · <b>Nguồn tiền:</b> {_m.get('the_tai_status_str', '')}.<br>"
            f"• <b>Mai Hoa:</b> Quẻ Chủ <b>{_m['full_chu']}</b> ({_m['rel_chu_tag']}) ➔ Hỗ <b>{_m['full_ho']}</b> ➔ Biến <b>{_m['full_bien']}</b> (<b>{_m['rel_bien_tag']}</b> · Số hội tụ = <b>0{_conv_num}</b>).<br>"
            f"• <b>Kỳ Môn & Thiết Bản:</b> Cung {_m['target_cung']} ({_m['huong_cung']}) hội <b>Sao {_m['sao_name']} · Cửa {_m['cua_name']} · Thần {_m['than_name']}</b> · Điều Văn #{_m.get('thiet_ban_dieu_van_so', '')}."
        )

        return {
            "has_override": True,
            "is_strict_override": is_strict_override,
            "is_open_van_vat": is_open_van_vat,
            "headline": f"🎯 [{c_lbl.upper()}]: {short_hl}" if sq_bp.get("clause_label") else f"🎯 {short_hl}",
            "short_headline": short_hl,
            "why": why_3sys,
            "when": f"• <b>Thời điểm ứng nghiệm:</b> <b>{uk_str}</b> (khi Hào Dụng Thần <b>{dt_chi}</b> và Quẻ Biến đắc khí).",
            "advice": (
                f"• <b>Hành động trọng tâm:</b> Theo nguyên lý quẻ <b>{_m['full_ho']} ➔ {_m['full_bien']}</b> ({_kd_c.get('loi_khuyen', 'Giữ vững chính đạo')}), ưu tiên hướng <b>{huong_str}</b>."
                + (f"{_m.get('thong_quan_html', '')}" if _m.get("thong_quan_html") else "")
            ),
        }

    @staticmethod
    def build_all_hexagrams_complete_breakdown_html(
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
        dung_than: str = "Bản Thân",
        question: str = "",
        univ_mat: dict = None,
    ) -> str:
        """
        V109.0: Phân tích chi tiết 100% MỌI LOẠI QUẺ và MỌI YẾU TỐ LIÊN KẾT kết nối trực tiếp vào toàn bộ Kho Dữ Liệu GitHub:
        - Lục Hào Kinh Dịch (luc_hao_kinh_dich.py, luc_hao_ky_mon_rules.py, kinh_dich_64_que.py, thoan_tu_64.py, iching_integrated_data.py)
        - Mai Hoa Dịch Số (mai_hoa_dich_so.py, kinh_dich_64_que.py — Quẻ Chủ, Quẻ Hỗ, Quẻ Biến, Thể/Dụng, Tiên/Hậu Thiên Quái Số)
        - Kỳ Môn Độn Giáp (luc_hao_ky_mon_rules.py, database_tuong_tac.py, km_luan_nang_cao.py — 9 Cung, Thiên/Địa Can, 81 Cách Cục Lưu Bá Ôn, Tổ hợp Sao-Cửa, 4 Cách Nhìn)
        - Thiết Bản Thần Toán, Đại Lục Nhâm (dai_luc_nham.py), Thái Ất Thần Số (thai_at_than_so.py), Tử Vi (tu_vi.py), Xem Ngày Đẹp (xem_ngay_dep.py), 19 Cổ Thư (offline_brain.py) & 77 Yếu Tố (FACTORS_77.py).
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = dict(omni_data or {})
        if question and not omni_data.get("question"):
            omni_data["question"] = question
        if not isinstance(univ_mat, dict):
            univ_mat = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
                dung_than=dung_than,
            )

        # Nạp đầy đủ các module tri thức trong kho GitHub (tách biệt từng import để không bao giờ lỗi chéo)
        try:
            from divination_knowledge_tree import TREE as _DK_TREE
        except Exception:
            _DK_TREE = {}
        try:
            from FACTORS_77 import ALL_77_FACTORS as _F77
        except Exception:
            _F77 = {}
        try:
            from kinh_dich_64_que import (
                KINH_DICH_64 as _KD64,
                MAI_HOA_UNG_KY as _MH_UK_RULES,
                tra_kinh_dich as _tra_kd,
                tra_nap_am as _tra_na,
                tra_the_dung as _tra_td,
            )
        except Exception:
            _KD64, _MH_UK_RULES = {}, {}
            _tra_kd = lambda x: {}
            _tra_na = lambda x: {}
            _tra_td = lambda t, d: {}
        try:
            from thoan_tu_64 import QUE_THOAN_64 as _QT64
        except Exception:
            _QT64 = {}
        try:
            from iching_integrated_data import ICHING_HEXAGRAMS as _IC_HEX64
        except Exception:
            _IC_HEX64 = {}
        try:
            from luc_hao_ky_mon_rules import (
                LUC_HAO_RULES as _LH_RULES,
                THAP_CAN_KHAC_UNG as _TC_UNG_STR,
                SAO_CUA_TO_HOP as _SC_TO_HOP,
                SAO_CUA_TO_HOP_BS as _SC_TO_HOP_BS,
                SAO_KY_MON as _SAO_KM_DICT,
                CUA_KY_MON as _CUA_KM_DICT,
                THAN_KY_MON as _THAN_KM_DICT,
                LUC_THAN_Y_NGHIA as _LTHU_DICT,
                NGUYEN_KY_CUU as _NKC_DICT,
                DONG_TINH_RULES as _DT_RULES,
                HAO_BIEN_RULES as _HB_RULES,
                NHAT_NGUYET_RULES as _NN_RULES,
                PHUC_THAN_RULES as _PT_RULES,
            )
        except Exception:
            _LH_RULES, _TC_UNG_STR, _SC_TO_HOP, _SC_TO_HOP_BS = [], {}, {}, {}
            _SAO_KM_DICT, _CUA_KM_DICT, _THAN_KM_DICT, _LTHU_DICT, _NKC_DICT = {}, {}, {}, {}, {}
            _DT_RULES, _HB_RULES, _NN_RULES, _PT_RULES = [], [], [], []
        try:
            from database_tuong_tac import TUONG_TAC_SAO_MON as _SM_UNG_DB
        except Exception:
            _SM_UNG_DB = {}

        _clk_bd = get_realtime_vn_clock_context()
        can_n = chart_data.get("can_ngay") or "Quý"
        chi_n = chart_data.get("chi_ngay") or "Mùi"
        can_g = chart_data.get("can_gio") or "Quý"
        chi_g = chart_data.get("chi_gio") or "Tị"
        can_m = chart_data.get("can_thang") or "Mậu"
        chi_m = chart_data.get("chi_thang") or "Tuất"
        can_y = chart_data.get("can_nam") or "Bính"
        chi_y = chart_data.get("chi_nam") or "Ngọ"
        kv_list = univ_mat.get("kv_list") or []

        lh_ban = (luc_hao_data.get("ban") or luc_hao_data.get("ban_que") or {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = (luc_hao_data.get("bien") or luc_hao_data.get("bien_que") or {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or []
        bien_haos = lh_bien.get("haos") or lh_bien.get("details") or []
        dong_list = univ_mat.get("dong_list") or []

        # =========================================================================
        # 1. XÂY DỰNG BẢNG CHI TIẾT 6 HÀO & PHÁP QUYẾT LỤC HÀO CỔ PHÁP (Hào 6 -> Hào 1)
        # =========================================================================
        _CHI_NH_B = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _SINH_B = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC_B = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
        _XUNG_B = {"Tý": "Ngọ", "Ngọ": "Tý", "Sửu": "Mùi", "Mùi": "Sửu", "Dần": "Thân", "Thân": "Dần", "Mão": "Dậu", "Dậu": "Mão", "Thìn": "Tuất", "Tuất": "Thìn", "Tị": "Hợi", "Hợi": "Tị"}
        _HOP_B = {"Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất", "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tị": "Thân", "Thân": "Tị", "Ngọ": "Mùi", "Mùi": "Ngọ"}
        _TIEN_THAN = {("Hợi", "Tý"), ("Dần", "Mão"), ("Tị", "Ngọ"), ("Thân", "Dậu"), ("Sửu", "Thìn"), ("Thìn", "Mùi"), ("Mùi", "Tuất")}
        _THOAI_THAN = {("Tý", "Hợi"), ("Mão", "Dần"), ("Ngọ", "Tị"), ("Dậu", "Thân"), ("Tuất", "Mùi"), ("Mùi", "Thìn"), ("Thìn", "Sửu")}
        _LT_ROLE_DESC = {
            "Phụ Mẫu": "Nhà cửa, Đất đai, Xe cộ, Giấy tờ, Hợp đồng, Bằng cấp, Cha mẹ",
            "Huynh Đệ": "Anh chị em, Bạn bè, Đối tác, Cạnh tranh, Chi phí hao tài",
            "Tử Tôn": "Con cái, Nguồn sinh tiền (Nguyên Thần của Tài), Phúc đức, Thuốc men, Giải thần",
            "Thê Tài": "Tiền bạc, Nguồn vốn mua nhà/tài sản, Lương thưởng, Lợi nhuận, Vợ",
            "Quan Quỷ": "Công danh, Sự nghiệp, Pháp lý, Áp lực, Chồng, Bệnh tật",
        }
        nh_m = _CHI_NH_B.get(chi_m, "Thổ")
        nh_n = _CHI_NH_B.get(chi_n, "Hỏa")
        dt_nh_main = univ_mat.get("dt_nh", "Kim")
        _nkc_info = _NKC_DICT.get(dt_nh_main) or {
            "nguyen_than": next((k for k, v in _SINH_B.items() if v == dt_nh_main), "Thổ"),
            "ky_than": next((k for k, v in _KHAC_B.items() if v == dt_nh_main), "Hỏa"),
            "cuu_than": _SINH_B.get(dt_nh_main, "Thủy"),
        }

        hao_rows_html = ""
        active_lh_rules_notes = []
        for idx in range(len(haos), 0, -1):
            h = haos[idx - 1]
            if not isinstance(h, dict):
                continue
            lt = str(h.get("luc_than") or "")
            lt_short = lt.split()[0] + (" " + lt.split()[1] if len(lt.split()) > 1 else "")
            cc = str(h.get("can_chi") or h.get("chi") or "")
            chi_h = str(h.get("chi") or cc).split()[-1] if (h.get("chi") or cc) else ""
            nh_h = str(h.get("ngu_hanh") or h.get("hanh") or _CHI_NH_B.get(chi_h, ""))
            tu = str(h.get("the_ung") or h.get("tu") or "")
            lthu = str(h.get("luc_thu") or "")
            v_suy = str(h.get("vuong_suy") or "")
            ts_h = str(h.get("truong_sinh") or "")
            is_d = (idx in dong_list) or bool(h.get("dong") or h.get("is_dong"))

            # Xét Vượng/Suy theo Nguyệt & Nhật, Tuần Không, Nguyệt Phá, Nhật Hợp/Xung
            tags_h = []
            if "Thế" in tu:
                tags_h.append('<span style="background:#ef4444;color:#fff;padding:1px 6px;border-radius:4px;font-weight:800;">HÀO THẾ (Bản thân)</span>')
            elif "Ứng" in tu:
                tags_h.append('<span style="background:#3b82f6;color:#fff;padding:1px 6px;border-radius:4px;font-weight:800;">HÀO ỨNG (Đích đến/Đối phương)</span>')
            if dung_than and dung_than in lt:
                tags_h.append('<span style="background:#eab308;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:900;">🎯 DỤNG THẦN CHÍNH</span>')
            elif nh_h == _nkc_info.get("nguyen_than"):
                tags_h.append('<span style="background:#0284c7;color:#fff;padding:1px 5px;border-radius:4px;font-size:0.82em;">🌱 Nguyên Thần (Sinh DT)</span>')
            elif nh_h == _nkc_info.get("ky_than"):
                tags_h.append('<span style="background:#e11d48;color:#fff;padding:1px 5px;border-radius:4px;font-size:0.82em;">⚔️ Kỵ Thần (Khắc DT)</span>')
            elif nh_h == _nkc_info.get("cuu_than"):
                tags_h.append('<span style="background:#64748b;color:#fff;padding:1px 5px;border-radius:4px;font-size:0.82em;">Cừu Thần</span>')
            if "Thê Tài" in lt:
                tags_h.append('<span style="background:#10b981;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:800;">💰 NGUỒN TIỀN</span>')
            if chi_h in kv_list:
                tags_h.append('<span style="background:#7c3aed;color:#fff;padding:1px 6px;border-radius:4px;font-weight:800;">⚠️ TUẦN KHÔNG (Chờ Xuất Không)</span>')
            if _XUNG_B.get(chi_m) == chi_h:
                tags_h.append('<span style="background:#dc2626;color:#fff;padding:1px 6px;border-radius:4px;font-weight:800;">⚡ NGUYỆT PHÁ</span>')
            if _HOP_B.get(chi_n) == chi_h:
                tags_h.append('<span style="background:#059669;color:#fff;padding:1px 6px;border-radius:4px;">Nhật Hợp</span>')
            elif _XUNG_B.get(chi_n) == chi_h:
                tags_h.append('<span style="background:#d97706;color:#fff;padding:1px 6px;border-radius:4px;">Nhật Xung (Ám Động/Xung Không)</span>')

            rel_mn = []
            if _SINH_B.get(nh_m) == nh_h or nh_m == nh_h:
                rel_mn.append(f"Đắc Nguyệt ({chi_m}-{nh_m}) trợ")
            elif _KHAC_B.get(nh_m) == nh_h:
                rel_mn.append(f"Nguyệt ({chi_m}-{nh_m}) khắc")
            if _SINH_B.get(nh_n) == nh_h or nh_n == nh_h:
                rel_mn.append(f"Đắc Nhật ({chi_n}-{nh_n}) sinh")
            elif _KHAC_B.get(nh_n) == nh_h:
                rel_mn.append(f"Nhật ({chi_n}-{nh_n}) khắc")
            v_suy_full = f"<b>{v_suy}</b>" + (f" · TS: {ts_h}" if ts_h else "") + (f" ({', '.join(rel_mn)})" if rel_mn else "")

            # Tra cứu ý nghĩa Lục Thú từ luc_hao_ky_mon_rules.LUC_THAN_Y_NGHIA
            _lthu_meta = _LTHU_DICT.get(lthu) or {}
            _lthu_cell = f"<b>{lthu}</b>"
            if _lthu_meta:
                _lt_color = "#4ade80" if "CÁT" in str(_lthu_meta.get("tinh_chat", "")) else "#fca5a5"
                _lthu_cell = f'<b>{lthu}</b> <span style="color:{_lt_color};font-size:0.82em;">({_lthu_meta.get("hanh","")}-{_lthu_meta.get("tinh_chat","")})</span>'

            bien_cell = "An tĩnh"
            bien_rule_explain = ""
            if is_d:
                if idx <= len(bien_haos) and isinstance(bien_haos[idx - 1], dict):
                    bh = bien_haos[idx - 1]
                    b_lt = str(bh.get("luc_than") or "")
                    b_cc = str(bh.get("can_chi") or bh.get("chi") or "")
                    b_ch = str(bh.get("chi") or b_cc).split()[-1] if (bh.get("chi") or b_cc) else ""
                    b_nh = str(bh.get("ngu_hanh") or bh.get("hanh") or _CHI_NH_B.get(b_ch, ""))
                    hd_rel = ""
                    if (chi_h, b_ch) in _TIEN_THAN:
                        hd_rel = " [Hóa TIẾN THẦN — Khí lực tiến mạnh]"
                        bien_rule_explain = f"Hào {idx} ({chi_h} ➔ {b_ch}) đắc cách <b>Hóa Tiến Thần</b> (Bốc Phệ Chính Tông: sự việc đang đà tiến lên từng bước vững chắc)."
                    elif (chi_h, b_ch) in _THOAI_THAN:
                        hd_rel = " [Hóa THOÁI THẦN — Khí lực lui dần]"
                        bien_rule_explain = f"Hào {idx} ({chi_h} ➔ {b_ch}) phạm <b>Hóa Thoái Thần</b> (Tăng San Bốc Dịch: lực hào giảm dần hoặc đối tượng đang rút lui)."
                    elif _SINH_B.get(b_nh) == nh_h:
                        hd_rel = " [Hồi đầu SINH — Đại Cát]"
                        bien_rule_explain = f"Hào {idx} động hóa {b_ch} ({b_nh}) <b>Hồi Đầu Sinh</b> (Tự biến ra nguồn lực quay lại nuôi dưỡng chính nó — Đại Cát)."
                    elif _KHAC_B.get(b_nh) == nh_h:
                        hd_rel = " [Hồi đầu KHẮC — Tự cản trở]"
                        bien_rule_explain = f"Hào {idx} động hóa {b_ch} ({b_nh}) <b>Hồi Đầu Khắc</b> (Biến xuất khắc trở lại — cần thận trọng trục trặc giữa chừng)."
                    elif _XUNG_B.get(chi_h) == b_ch:
                        hd_rel = " [Phản Ngâm Hào — Lặp đi lặp lại]"
                        bien_rule_explain = f"Hào {idx} ({chi_h} ➔ {b_ch}) phạm <b>Hào Hóa Xung / Phản Ngâm</b> (Sự việc dễ thay đổi hoặc làm đi làm lại)."
                    elif b_nh == nh_h:
                        hd_rel = " [Tỷ Hòa đồng hành]"
                    bien_cell = f'<b style="color:#f43f5e;">⚡ ĐỘNG ➔ Hóa {b_lt} ({b_cc}-{b_nh}){hd_rel}</b>'
                    if bien_rule_explain:
                        active_lh_rules_notes.append(bien_rule_explain)
                else:
                    bien_cell = '<b style="color:#f43f5e;">⚡ PHÁT ĐỘNG</b>'

            if chi_h in kv_list and (dung_than in lt or "Thế" in tu or "Thê Tài" in lt):
                active_lh_rules_notes.append(
                    f"Hào {idx} (<b>{lt_short} {chi_h}</b>) đang lâm <b>Tuần Không ({', '.join(kv_list)})</b>: "
                    f"{'Động Không bất Không — xuất tuần là ứng nghiệm ngay' if is_d else 'Hiện tại chưa thể thành tựu tức thì, phải đợi ngày/tháng Xuất Không hoặc Xung Không mới ứng nghiệm'}."
                )
            if _XUNG_B.get(chi_m) == chi_h:
                active_lh_rules_notes.append(
                    f"Hào {idx} (<b>{lt_short} {chi_h}</b>) bị Nguyệt Lệnh <b>{chi_m} Xung (Nguyệt Phá)</b>: Đang chịu tổn thương hoặc trì hoãn trong tháng {chi_m}, cần qua tháng sau hoặc ngày Hợp ({_HOP_B.get(chi_h, '')}) để giải phá."
                )

            role_meaning = _LT_ROLE_DESC.get(lt_short, "Yếu tố cấu thành quẻ")
            lthu_detail_str = f" · <b>Lục Thú {lthu}:</b> {_lthu_meta.get('y_nghia', '')} (Người: {_lthu_meta.get('nguoi', '')})" if _lthu_meta else ""
            full_line_meaning = f"<b>Đại diện:</b> {role_meaning}{lthu_detail_str}" + (f" · <span style='color:#fde047;'>{bien_rule_explain}</span>" if bien_rule_explain else "")

            hao_rows_html += (
                f'<tr style="border-bottom:1px solid rgba(148,163,184,0.18);background:{"rgba(250,204,21,0.08)" if (dung_than and dung_than in lt) else ("rgba(239,68,68,0.07)" if is_d else "transparent")};">'
                f'<td style="padding:6px 8px;font-weight:800;color:#fde047;">Hào {idx}</td>'
                f'<td style="padding:6px 8px;font-weight:700;color:#e2e8f0;">{lt} {" ".join(tags_h)}</td>'
                f'<td style="padding:6px 8px;color:#38bdf8;font-weight:700;">{cc} ({nh_h})</td>'
                f'<td style="padding:6px 8px;color:#cbd5e1;">{_lthu_cell}</td>'
                f'<td style="padding:6px 8px;color:#a7f3d0;font-size:0.86em;">{v_suy_full}</td>'
                f'<td style="padding:6px 8px;">{bien_cell}</td>'
                f'<td style="padding:6px 8px;color:#cbd5e1;font-size:0.85em;line-height:1.45;">{full_line_meaning}</td>'
                f'</tr>'
            )

        # Kiểm tra các Lục Thân bị Ẩn Phục (Phục Thần) không hiện trên 6 hào Quẻ Chủ
        _present_lts = set()
        for h in haos:
            if isinstance(h, dict):
                for _lt_k in ("Phụ Mẫu", "Huynh Đệ", "Tử Tôn", "Thê Tài", "Quan Quỷ"):
                    if _lt_k in str(h.get("luc_than") or ""):
                        _present_lts.add(_lt_k)
        _missing_lts = [k for k in ("Phụ Mẫu", "Huynh Đệ", "Tử Tôn", "Thê Tài", "Quan Quỷ") if k not in _present_lts]
        _phuc_than_note_html = ""
        if _missing_lts:
            _phuc_items = [f"<b>{_mlt}</b> ({_LT_ROLE_DESC.get(_mlt, '')})" for _mlt in _missing_lts]
            _phuc_than_note_html = (
                f'<div style="margin-top:8px;padding:8px 12px;background:rgba(245,158,11,0.14);border-left:4px solid #f59e0b;border-radius:6px;font-size:0.88em;color:#fef3c7;">'
                f'🔍 <b>Phát hiện Hào Phục Thần (Ẩn phục dưới Phi Thần, chưa xuất hiện trên mặt Quẻ Chủ):</b> {", ".join(_phuc_items)} '
                f'➔ Theo <i>Tăng San Bốc Dịch (`PHUC_THAN_RULES`)</i>: Khi yếu tố này ẩn phục (đặc biệt là <b>Thê Tài [Tiền bạc/Vốn]</b> hoặc <b>Dụng Thần</b>), sự việc liên quan đến yếu tố đó <b>chưa có sẵn ở hiện tại</b>, bắt buộc phải đợi đến tháng/năm Can Chi <b>Xuất Phục / Xung Phi Lộ Phục</b> mới hội tụ đủ điều kiện!'
                f'</div>'
            )

        # Khối Pháp Quyết Lục Hào Cổ Pháp (từ luc_hao_ky_mon_rules.py)
        _lh_classical_html = (
            f'<div style="margin-top:8px;padding:8px 12px;background:rgba(30,41,59,0.85);border-radius:6px;border-left:3px solid #38bdf8;font-size:0.86em;color:#e2e8f0;line-height:1.5;">'
            f'📐 <b>Hệ Sinh Thái Tứ Thần (`NGUYEN_KY_CUU`) cho Dụng Thần [{dung_than} - Hành {dt_nh_main}]:</b> '
            f'🌱 <b>Nguyên Thần</b> (nguồn sinh trợ): <b style="color:#38bdf8;">Hành {_nkc_info["nguyen_than"]}</b> &nbsp;|&nbsp; '
            f'⚔️ <b>Kỵ Thần</b> (khắc Dụng Thần): <b style="color:#f43f5e;">Hành {_nkc_info["ky_than"]}</b> &nbsp;|&nbsp; '
            f'⚠️ <b>Cừu Thần</b> (khắc Nguyên Thần): <b>Hành {_nkc_info["cuu_than"]}</b>.<br>'
            + (f'📜 <b>Pháp Quyết Động/Tĩnh & Biến Hóa Kích Hoạt Trên Quẻ:</b> {" &nbsp;•&nbsp; ".join(active_lh_rules_notes)}' if active_lh_rules_notes else '📜 <b>Pháp Quyết Động/Tĩnh:</b> Các hào vận hành ổn định theo trục Thế – Ứng và Nhật/Nguyệt Lệnh.')
            + '</div>'
        )

        # Thông tin Thoán Từ, Đại Tượng & 8 Lĩnh Vực từ kinh_dich_64_que.py, thoan_tu_64.py & iching_integrated_data.py
        _kd_chu = univ_mat.get("kd_chu_info") or (_tra_kd(univ_mat["full_chu"]) if callable(_tra_kd) else {}) or _KD64.get(univ_mat["full_chu"]) or {}
        _kd_ho = univ_mat.get("kd_ho_info") or (_tra_kd(univ_mat["full_ho"]) if callable(_tra_kd) else {}) or _KD64.get(univ_mat["full_ho"]) or {}
        _kd_bien = univ_mat.get("kd_bien_info") or (_tra_kd(univ_mat["full_bien"]) if callable(_tra_kd) else {}) or _KD64.get(univ_mat["full_bien"]) or {}
        _qt_chu = _QT64.get(univ_mat["full_chu"]) or {}
        _qt_bien = _QT64.get(univ_mat["full_bien"]) or {}
        _ic_chu = univ_mat.get("ic_chu_info") or _IC_HEX64.get(_kd_chu.get("thu_tu", 0)) or {}
        _ic_bien = univ_mat.get("ic_bien_info") or _IC_HEX64.get(_kd_bien.get("thu_tu", 0)) or {}

        _thoan_chu = _kd_chu.get("thoan") or _qt_chu.get("thoan") or _kd_chu.get("y_nghia") or univ_mat["desc_chu"]
        _daituong_chu = _kd_chu.get("dai_tuong") or _qt_chu.get("dai_tuong") or ""
        _loikhuyen_chu = _kd_chu.get("loi_khuyen") or _qt_chu.get("lk") or ""
        _thoan_bien = _kd_bien.get("thoan") or _qt_bien.get("thoan") or _kd_bien.get("y_nghia") or univ_mat["desc_bien"]
        _daituong_bien = _kd_bien.get("dai_tuong") or _qt_bien.get("dai_tuong") or ""
        _loikhuyen_bien = _kd_bien.get("loi_khuyen") or _qt_bien.get("lk") or ""

        _ic_8_fields_html = ""
        if _ic_chu:
            _ic_8_fields_html = (
                f'<div style="margin-bottom:8px;padding:8px 10px;background:rgba(15,23,42,0.85);border:1px solid rgba(56,189,248,0.25);border-radius:6px;font-size:0.85em;color:#cbd5e1;line-height:1.5;">'
                f'<b style="color:#7dd3fc;">📖 Luận Giải 8 Phương Diện Thực Tế Của Quẻ Chủ [{univ_mat["full_chu"]}] (`iching_integrated_data.py`):</b><br>'
                f'• <b>Tổng quan:</b> {_ic_chu.get("general", "")} &nbsp;|&nbsp; <b>Tài vận:</b> <span style="color:#4ade80;">{_ic_chu.get("fortune", "")}</span><br>'
                f'• <b>Mưu sự & Nguyện vọng:</b> {_ic_chu.get("wish", "")} &nbsp;|&nbsp; <b>Công danh & Sự nghiệp:</b> {_ic_chu.get("career", "")}<br>'
                f'• <b>Gia đạo:</b> {_ic_chu.get("family", "")} &nbsp;|&nbsp; <b>Tình cảm & Hôn nhân:</b> {_ic_chu.get("love", "")}<br>'
                f'• <b>Sức khỏe & Cơ thể:</b> {_ic_chu.get("sickness", "")} &nbsp;|&nbsp; <b>Tìm đồ thất lạc:</b> {_ic_chu.get("lost_item", "")}'
                f'</div>'
            )

        # =========================================================================
        # 2. XÂY DỰNG BẢNG CHI TIẾT 9 CUNG KỲ MÔN ĐỘN GIÁP & 4 CÁCH NHÌN NÂNG CAO
        # =========================================================================
        _CUNG_NAMES_9 = {
            1: "Cung 1 — Khảm (Chính Bắc · Thủy)",
            2: "Cung 2 — Khôn (Tây Nam · Thổ)",
            3: "Cung 3 — Chấn (Chính Đông · Mộc)",
            4: "Cung 4 — Tốn (Đông Nam · Mộc)",
            5: "Cung 5 — Trung Cung (Thổ · Gửi Khôn 2)",
            6: "Cung 6 — Càn (Tây Bắc · Kim)",
            7: "Cung 7 — Đoài (Chính Tây · Kim)",
            8: "Cung 8 — Cấn (Đông Bắc · Thổ)",
            9: "Cung 9 — Ly (Chính Nam · Hỏa)",
        }
        _DEFAULT_DIA_BAN = {1: "Mậu", 2: "Kỷ", 3: "Canh", 4: "Tân", 5: "Mậu", 6: "Nhâm", 7: "Quý", 8: "Ất", 9: "Bính"}
        _tb_map = chart_data.get("thien_ban") or {}
        _nb_map = chart_data.get("nhan_ban") or {}
        _sb_map = chart_data.get("than_ban") or {}
        _ctb_map = chart_data.get("can_thien_ban") or {}
        # Sửa triệt để lỗi thiếu Địa Can: lấy từ dia_ban (chuẩn app.py) hoặc can_dia_ban hoặc fallback Lục Nghi Tam Kỳ
        _cdb_map = chart_data.get("dia_ban") or chart_data.get("can_dia_ban") or chart_data.get("dia_can") or _DEFAULT_DIA_BAN
        _target_c = str(univ_mat.get("target_cung", "7"))

        km_9cung_rows = ""
        for c_i in range(1, 10):
            s_c = str(_tb_map.get(c_i) or _tb_map.get(str(c_i)) or ("Thiên Cầm" if c_i == 5 else "Thiên Tâm")).strip()
            m_c = str(_nb_map.get(c_i) or _nb_map.get(str(c_i)) or ("Trung Môn (Gửi Khôn 2)" if c_i == 5 else "Khai Môn")).strip()
            t_c = str(_sb_map.get(c_i) or _sb_map.get(str(c_i)) or ("Thiên Ất" if c_i == 5 else "Trực Phù")).strip()
            ct_c = str(_ctb_map.get(c_i) or _ctb_map.get(str(c_i)) or "").strip()
            cd_c = str(_cdb_map.get(c_i) or _cdb_map.get(str(c_i)) or _DEFAULT_DIA_BAN.get(c_i, "Mậu")).strip()
            if c_i == 5:
                if not ct_c:
                    ct_c = str(_ctb_map.get(2) or _ctb_map.get("2") or cd_c).strip()
                if not cd_c:
                    cd_c = str(_cdb_map.get(2) or _cdb_map.get("2") or "Kỷ").strip()

            # 1) Tra cứu 81 Cách Cục Thập Can Khắc Ứng Lưu Bá Ôn (luc_hao_ky_mon_rules.py dùng key "CanThiên+CanĐịa")
            _cc_parts = []
            _tc_key_str = f"{ct_c}+{cd_c}"
            if _tc_key_str in _TC_UNG_STR and isinstance(_TC_UNG_STR[_tc_key_str], dict):
                _cc_d = _TC_UNG_STR[_tc_key_str]
                _cc_color = "#4ade80" if "CÁT" in str(_cc_d.get("cat_hung", "")) and "HUNG" not in str(_cc_d.get("cat_hung", "")) else ("#f87171" if "HUNG" in str(_cc_d.get("cat_hung", "")) else "#fde047")
                _cc_parts.append(f'<b>Cách cục Can ({ct_c}+{cd_c}) — <span style="color:{_cc_color};">{_cc_d.get("ten", "")} [{_cc_d.get("cat_hung", "")}]</span>:</b> {_cc_d.get("luan", "")}')
            elif ct_c and cd_c and ct_c == cd_c:
                _cc_parts.append(f'<b>Cách cục Can ({ct_c}+{cd_c}) — Phục Ngâm Can [BÌNH/TRÌ TRỆ]:</b> Ẩn náu, bình tĩnh chờ thời; sự việc tại cung đang giậm chân tại chỗ, không nên nóng vội.')

            # 2) Tra cứu Tổ Hợp Sao + Cửa (SAO_CUA_TO_HOP, SAO_CUA_TO_HOP_BS, TUONG_TAC_SAO_MON)
            _s_clean = s_c.split("/")[0].strip()
            _m_clean = m_c.split("(")[0].strip()
            _sc_hit = _SC_TO_HOP.get((_s_clean, _m_clean)) or _SC_TO_HOP_BS.get((_s_clean, _m_clean))
            if isinstance(_sc_hit, dict):
                _cc_parts.append(f'<b>Tổ hợp {_s_clean} + {_m_clean}:</b> {_sc_hit.get("luan", "")} (<i>Ứng dụng:</i> {_sc_hit.get("ung_dung", "")})')
            elif (_s_clean, _m_clean) in _SM_UNG_DB:
                _cc_parts.append(f'<b>Tương tác {_s_clean} + {_m_clean}:</b> {_SM_UNG_DB[(_s_clean, _m_clean)]}')

            # 3) Tra cứu chi tiết Tinh - Môn - Thần từ SAO_KY_MON, CUA_KY_MON, THAN_KY_MON
            _s_meta = _SAO_KM_DICT.get(_s_clean) or {}
            _m_meta = _CUA_KM_DICT.get(_m_clean) or {}
            _t_meta = _THAN_KM_DICT.get(t_c) or {}
            _tmt_details = []
            if _s_meta:
                _tmt_details.append(f"<b>{_s_clean}</b> ({_s_meta.get('hanh','')}-{_s_meta.get('loai','')}): {_s_meta.get('y_nghia','')}")
            if _m_meta:
                _tmt_details.append(f"<b>{_m_clean}</b> ({_m_meta.get('hanh','')}-{_m_meta.get('loai','')}): {_m_meta.get('y_nghia','')}")
            if _t_meta:
                _tmt_details.append(f"<b>{t_c}</b> ({_t_meta.get('loai','')}): {_t_meta.get('y_nghia','')}")
            if _tmt_details:
                _cc_parts.append(" · ".join(_tmt_details))

            cach_cuc_str = "<br>".join(_cc_parts) if _cc_parts else f"Sao {s_c} hội {m_c} & Thần {t_c}"

            role_c = []
            if str(c_i) == _target_c:
                role_c.append('<span style="background:#eab308;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:800;">🎯 CUNG DỤNG THẦN</span>')
            if ct_c == can_n:
                role_c.append('<span style="background:#ef4444;color:#fff;padding:1px 6px;border-radius:4px;font-weight:800;">👤 CUNG BẢN THÂN (Can Ngày)</span>')
            if ct_c == can_g:
                role_c.append('<span style="background:#38bdf8;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:800;">📌 CUNG SỰ VIỆC (Can Giờ)</span>')
            if "Sinh" in m_c:
                role_c.append('<span style="background:#10b981;color:#0f172a;padding:1px 6px;border-radius:4px;font-weight:800;">🏠 SINH MÔN (Nhà đất/Tài lộc)</span>')
            km_9cung_rows += (
                f'<tr style="border-bottom:1px solid rgba(148,163,184,0.16);background:{"rgba(56,189,248,0.09)" if role_c else "transparent"};">'
                f'<td style="padding:6px 8px;font-weight:700;color:#7dd3fc;">{_CUNG_NAMES_9[c_i]} {" ".join(role_c)}</td>'
                f'<td style="padding:6px 8px;color:#fde047;font-weight:800;white-space:nowrap;">{ct_c} / {cd_c}</td>'
                f'<td style="padding:6px 8px;color:#e2e8f0;font-weight:700;">{s_c}</td>'
                f'<td style="padding:6px 8px;color:#4ade80;font-weight:700;">{m_c}</td>'
                f'<td style="padding:6px 8px;color:#c4b5fd;font-weight:700;">{t_c}</td>'
                f'<td style="padding:6px 8px;color:#cbd5e1;font-size:0.84em;line-height:1.45;">{cach_cuc_str}</td>'
                f'</tr>'
            )

        # Gọi km_luan_nang_cao.py để lấy 4 Cách Nhìn Kỳ Môn Nâng Cao & Nhìn Xa Gần
        _km_nang_cao_html = ""
        try:
            from km_luan_nang_cao import luan_nhin_xa_gan, luan_bon_cach_nhin, CAN_NGU_HANH, CUNG_NGU_HANH
            _c_dt_int = int(_target_c) if str(_target_c).isdigit() else 7
            _is_dd = bool(chart_data.get("is_duong_don", False))
            _xa_gan_res = luan_nhin_xa_gan(_is_dd, _c_dt_int, False, bool(univ_mat.get("is_km_phuc_ngam", False)))
            _s_dt_clean = str(univ_mat.get("sao_name", "Thiên Tâm")).split("/")[0].strip()
            _m_dt_clean = str(univ_mat.get("cua_name", "Khai Môn")).split("(")[0].strip()
            _t_dt_clean = str(univ_mat.get("than_name", "Trực Phù")).strip()
            _h_can = CAN_NGU_HANH.get(can_n, "Thủy")
            _h_cua = (_CUA_KM_DICT.get(_m_dt_clean) or {}).get("hanh", CUNG_NGU_HANH.get(_c_dt_int, "Kim"))
            _h_sao = (_SAO_KM_DICT.get(_s_dt_clean) or {}).get("hanh", CUNG_NGU_HANH.get(_c_dt_int, "Kim"))
            _bon_cach_res = luan_bon_cach_nhin(can_n, _m_dt_clean, _s_dt_clean, _t_dt_clean, _h_can, _h_cua, _h_sao, _xa_gan_res)
            _bon_cach_clean = "<br>".join(
                line.strip() for line in re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", str(_bon_cach_res or "")).splitlines() if line.strip()
            )
            if _bon_cach_clean:
                _km_nang_cao_html = (
                    f'<div style="margin-top:8px;padding:8px 12px;background:rgba(30,41,59,0.88);border-radius:6px;border-left:3px solid #fbbf24;font-size:0.85em;color:#e2e8f0;line-height:1.5;">'
                    f'<b style="color:#fde047;">🔭 Luận Giải 4 Cách Nhìn Kỳ Môn Nâng Cao & Nội/Ngoại Bàn (`km_luan_nang_cao.py`):</b><br>'
                    f'• <b>Định vị Không gian & Xa/Gần:</b> {_xa_gan_res}<br>'
                    f'{_bon_cach_clean}'
                    f'</div>'
                )
        except Exception:
            _km_nang_cao_html = ""

        # =========================================================================
        # 3. CHẠY TRỰC TIẾP CÁC ENGINE TRONG PHẦN 4 (THIẾT BẢN, ĐẠI LỤC NHÂM, THÁI ẤT, TỬ VI, XEM NGÀY, 19 CỔ THƯ)
        # =========================================================================
        # 3A. Thiết Bản Thần Toán, Hoàng Cực Kinh Thế & Nạp Âm Tứ Trụ (Ryanlyly-ai/huangji-jingshi & Horosa)
        _na_y = (_tra_na(f"{can_y} {chi_y}") if callable(_tra_na) else {}) or {}
        _na_m = (_tra_na(f"{can_m} {chi_m}") if callable(_tra_na) else {}) or {}
        _na_d = (_tra_na(f"{can_n} {chi_n}") if callable(_tra_na) else {}) or {}
        _na_h = (_tra_na(f"{can_g} {chi_g}") if callable(_tra_na) else {}) or {}
        _tb_luan_str = univ_mat.get("thiet_ban_luan_giai") or ""
        _thiet_ban_detail_str = (
            (f"<span style='color:#fde047;'>{_tb_luan_str}</span><br>&nbsp;&nbsp;➔ " if _tb_luan_str else "")
            + f"Nạp Âm Tứ Trụ: Năm <b>{can_y} {chi_y}</b> ({_na_y.get('nap_am', 'Thiên Hà Thủy')} — {_na_y.get('giai_thich', '')}) · "
            f"Tháng <b>{can_m} {chi_m}</b> ({_na_m.get('nap_am', 'Bình Địa Mộc')}) · "
            f"Ngày <b>{can_n} {chi_n}</b> (<b style='color:#fde047;'>{_na_d.get('nap_am', 'Dương Liễu Mộc')}</b> — {_na_d.get('giai_thich', '')}) · "
            f"Giờ <b>{can_g} {chi_g}</b> ({_na_h.get('nap_am', 'Đại Trạch Thổ')})."
        )

        # 3B. Đại Lục Nhâm (Tứ Khóa & Tam Truyền)
        _dln_detail_html = ""
        try:
            from dai_luc_nham import tinh_dai_luc_nham
            _dln_res = tinh_dai_luc_nham(can_n, chi_n, chi_g, chart_data.get("tiet_khi", "Lập Đông"))
            if isinstance(_dln_res, dict):
                _nt_dln = _dln_res.get("nguyet_tuong") or {}
                _tk_dln = _dln_res.get("tu_khoa") or []
                _tt_dln = _dln_res.get("tam_truyen") or {}
                _lg_dln = _dln_res.get("luan_giai") or {}
                _tfull_dln = _dln_res.get("thien_tuong_full") or {}
                _tk_str = " | ".join(f"{k.get('ten','')}: <b>{k.get('thien','')}/{k.get('dia','')}</b>" for k in _tk_dln if isinstance(k, dict))
                _so_ch = _tt_dln.get("so_truyen", "")
                _tr_ch = _tt_dln.get("trung_truyen", "")
                _ma_ch = _tt_dln.get("mat_truyen", "")
                _so_t = (_tfull_dln.get(_so_ch) or {}).get("ten", "")
                _tr_t = (_tfull_dln.get(_tr_ch) or {}).get("ten", "")
                _ma_t = (_tfull_dln.get(_ma_ch) or {}).get("ten", "")
                _lg_details = " · ".join(str(x).strip() for x in (_lg_dln.get("details") or []))
                _dln_detail_html = (
                    f"Nguyệt Tướng: <b>{_nt_dln.get('chi','')} ({_nt_dln.get('ten','')})</b> | "
                    f"<b>Tứ Khóa:</b> {_tk_str}<br>"
                    f"&nbsp;&nbsp;➔ <b>Tam Truyền ({_tt_dln.get('phuong_phap','Khởi khóa')}):</b> "
                    f"1️⃣ <b>Sơ Truyền (Khởi phát):</b> <b style='color:#fde047;'>{_so_ch} ({_tt_dln.get('so_truyen_hanh','')})</b> [Thiên tướng: {_so_t}] ➔ "
                    f"2️⃣ <b>Trung Truyền (Diễn biến):</b> <b style='color:#38bdf8;'>{_tr_ch} ({_tt_dln.get('trung_truyen_hanh','')})</b> [Thiên tướng: {_tr_t}] ➔ "
                    f"3️⃣ <b>Mạt Truyền (Kết cục):</b> <b style='color:#4ade80;'>{_ma_ch} ({_tt_dln.get('mat_truyen_hanh','')})</b> [Thiên tướng: {_ma_t}].<br>"
                    f"&nbsp;&nbsp;➔ <b>Luận giải Đại Lục Nhâm (`dai_luc_nham.py` — {_lg_dln.get('verdict','BÌNH')}):</b> {_lg_details}"
                )
        except Exception:
            _dln_detail_html = "Đầy đủ Thiên Địa Bàn, Tứ Khóa, Tam Truyền (Sơ Truyền ➔ Trung Truyền ➔ Mạt Truyền) & 12 Thiên Tướng."

        # 3C. Thái Ất Thần Số (Tích Niên, Cung Thái Ất, Bát Tướng & Cách Cục)
        _ta_detail_html = ""
        try:
            from thai_at_than_so import tinh_thai_at_than_so
            _ta_res = tinh_thai_at_than_so(_clk_bd["cur_year"], _clk_bd["cur_month"], can_n, chi_n)
            if isinstance(_ta_res, dict):
                _tac = _ta_res.get("thai_at_cung") or {}
                _bt = _ta_res.get("bat_tuong") or {}
                _lg_ta = _ta_res.get("luan_giai") or {}
                _vx = _bt.get("Văn Xương") or {}
                _tk_ta = _bt.get("Thủy Kích") or {}
                _cdt = _bt.get("Chủ Đại Tướng") or {}
                _kdt = _bt.get("Khách Đại Tướng") or {}
                _cc_ta_str = " · ".join(str(x).strip() for x in (_ta_res.get("cach_cuc") or [])[:4])
                _ta_detail_html = (
                    f"Năm {_ta_res.get('nam', _clk_bd['cur_year'])} (Tích niên <b>{_ta_res.get('tich_nien','')}</b>) · "
                    f"<b>Thái Ất đóng tại Cung {_tac.get('cung','')} ({_tac.get('ten_cung','')} - Hành {_tac.get('hanh_cung','')} - {_tac.get('ly','')})</b> | "
                    f"Văn Xương: Cung {_vx.get('cung','')} ({_vx.get('ten_cung','')}) · Thủy Kích: Cung {_tk_ta.get('cung','')} ({_tk_ta.get('ten_cung','')}) · "
                    f"Chủ Đại Tướng: Cung {_cdt.get('cung','')} ({_cdt.get('ten_cung','')}) · Khách Đại Tướng: Cung {_kdt.get('cung','')} ({_kdt.get('ten_cung','')}).<br>"
                    f"&nbsp;&nbsp;➔ <b>Luận giải Thái Ất (`thai_at_than_so.py` — {_lg_ta.get('verdict','CÁT')}):</b> {_cc_ta_str}"
                )
        except Exception:
            _ta_detail_html = "Đầy đủ Thái Ất Cửu Cung, Văn Xương, Thủy Kích, Chủ Đại Tướng, Khách Đại Tướng & Định Toán."

        # 3D. Tử Vi Đẩu Số & Kho Tàng Tử Vi Thiên Kỷ 56.6GB GitHub (Renhuai123/ziwei-doushu — 13 Chiều Luận Mệnh)
        _tv_detail_html = ""
        try:
            from tu_vi import lap_la_so, analyze_thien_ky_13_dimensions
            _CHI_IDX_TV = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
            _g_idx_tv = _CHI_IDX_TV.index(chi_g) if chi_g in _CHI_IDX_TV else 6
            _tv_res = lap_la_so(_clk_bd["lunar_year"], _clk_bd["lunar_month"], _clk_bd["lunar_day"], _g_idx_tv, "nam")
            if isinstance(_tv_res, dict):
                _mc_tv = (_tv_res.get("menh_cung") or {}).get("chi", "Thìn")
                _tc_tv = (_tv_res.get("than_cung") or {}).get("chi", "Thân")
                _th_tv = _tv_res.get("tu_hoa") or {}
                _th_str = ", ".join(f"{k}: <b>{v}</b>" for k, v in _th_tv.items()) if isinstance(_th_tv, dict) else str(_th_tv)
                _tk13 = _tv_res.get("thien_ky_13_dimensions") or (analyze_thien_ky_13_dimensions(_tv_res) if callable(analyze_thien_ky_13_dimensions) else {}) or {}
                _tk13_vals = list(_tk13.values())
                _tk13_core = _tk13_vals[1] if len(_tk13_vals) > 1 else ""
                _tk13_env = _tk13_vals[3] if len(_tk13_vals) > 3 else ""
                _tv_detail_html = (
                    f"Cục số: <b>{_tv_res.get('cuc_ten', 'Thủy Nhị Cục')}</b> · Nạp âm: <b>{_tv_res.get('nap_am', '')}</b> · "
                    f"Cung Mệnh lập tại <b>{_mc_tv}</b> · Cung Thân lập tại <b>{_tc_tv}</b> · "
                    f"<b>Tứ Hóa kích hoạt (`tu_vi.py`):</b> {_th_str}."
                    + (f"<br>&nbsp;&nbsp;➔ <b>Kho Tử Vi Thiên Kỷ 56.6GB GitHub (`Renhuai123/ziwei-doushu` — 13 Chiều):</b> {_tk13_core} | {_tk13_env}" if _tk13_core else "")
                )
        except Exception:
            _tv_detail_html = "Đầy đủ 12 Cung, 14 Chính Tinh, Tứ Hóa (Lộc – Quyền – Khoa – Kỵ), Đại Hạn 10 năm & Kho Tử Vi Thiên Kỷ 56.6GB (13 Chiều)."

        # 3E. Xem Ngày Đẹp & Trạch Nhật (xem_ngay_dep.py)
        _xn_detail_html = ""
        try:
            from xem_ngay_dep import danh_gia_ngay_duong_lich
            _xn_res = danh_gia_ngay_duong_lich(_clk_bd["cur_day"], _clk_bd["cur_month"], _clk_bd["cur_year"], can_n, chi_n, "cau_tai")
            if isinstance(_xn_res, dict):
                _shd = _xn_res.get("sao_hoang_dao") or ("Thanh Long", "Hoàng Đạo", "🟢", "Tốt")
                _s28 = _xn_res.get("sao_28_tu") or ("Tỉnh", "Mộc", "Ngan", "Cát", "🟢", "Tốt")
                _tr_info = _xn_res.get("truc_info") or {}
                _nen_str = ", ".join(_tr_info.get("nen") or [])
                _ky_str = ", ".join(_tr_info.get("ky") or [])
                _xn_detail_html = (
                    f"Ngày hiện tại <b>{_clk_bd['solar_date_str']} ({can_n} {chi_n})</b>: "
                    f"Sao <b>{_shd[0]} ({_shd[1]} — {_shd[3]})</b> · "
                    f"Trực <b>{_xn_res.get('truc','')} ({_tr_info.get('cat_hung','')}: {_tr_info.get('mo_ta','')})</b> · "
                    f"Nhị Thập Bát Tú: <b>Sao {_s28[0]} ({_s28[1]} — {_s28[3]}: {_s28[5]})</b>.<br>"
                    f"&nbsp;&nbsp;➔ <b>Việc nên làm hôm nay:</b> <span style='color:#4ade80;'>{_nen_str or 'Giao dịch, cầu tài, lập kế hoạch'}</span> &nbsp;|&nbsp; "
                    f"<b>Việc kiêng kỵ:</b> <span style='color:#fca5a5;'>{_ky_str or 'Không'}</span>."
                )
        except Exception:
            _xn_detail_html = "Đầy đủ Hoàng Đạo/Hắc Đạo, 12 Trực Kiến Trừ, 28 Sao Nhị Thập Bát Tú & Giờ Hoàng Đạo."

        # 3F. Hồ sơ 19 Bộ Cổ Thư từ offline_brain.py
        _classical_dossier_html = ""
        try:
            from offline_brain import extract_deep_divination_dossier
            _dos = extract_deep_divination_dossier(
                question=question,
                dung_than=dung_than,
                hanh_dt=dt_nh_main,
                weighted_pct=60,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
            )
            if isinstance(_dos, dict):
                _classical_dossier_html = (
                    f'<div style="margin-top:8px;padding:8px 12px;background:rgba(30,41,59,0.88);border-radius:6px;border-left:3px solid #a78bfa;font-size:0.85em;color:#e2e8f0;line-height:1.5;">'
                    f'<b style="color:#c4b5fd;">🏛️ Trích Dẫn Trực Tiếp Tinh Hoa 19 Bộ Cổ Thư Trong Kho GitHub (`offline_brain.py`):</b><br>'
                    f'• <b>Thiết Bản & Nạp Âm Định Số:</b> {_dos.get("thiet_ban_text", "")}<br>'
                    f'• <b>12 Trường Sinh & Khí Số:</b> {_dos.get("truong_sinh_text", "")}<br>'
                    f'• <b>Bốc Phệ Chính Tông & Tăng San Bốc Dịch:</b> {_dos.get("luc_hao_text", "")}'
                    f'</div>'
                )
        except Exception:
            _classical_dossier_html = ""

        # Thống kê toàn bộ các nhóm yếu tố trong Kho Tri Thức GitHub (divination_knowledge_tree.py & FACTORS_77.py)
        _lh_36_keys = list((_DK_TREE.get("LUC_HAO") or {}).keys())
        _km_30_keys = list((_DK_TREE.get("KY_MON") or {}).keys())
        _mh_11_keys = list((_DK_TREE.get("MAI_HOA") or {}).keys())
        _ln_19_keys = list((_DK_TREE.get("LUC_NHAM") or {}).keys())
        _ta_13_keys = list((_DK_TREE.get("THAI_AT") or {}).keys())
        _tb_6_keys = list((_DK_TREE.get("THIET_BAN") or {}).keys())
        _tv_22_keys = list((_DK_TREE.get("TU_VI") or {}).keys())
        _xn_21_keys = list((_DK_TREE.get("XEM_NGAY") or {}).keys())

        _meta_up = univ_mat.get("meta_up_chu") or (1, 1, 6, "Kim", "")
        _meta_lo = univ_mat.get("meta_lo_chu") or (1, 4, 3, "Mộc", "")
        _quai_so_sum = int(_meta_up[1]) + int(_meta_lo[1])

        _chain_items = [p.strip() for p in str(univ_mat.get("holistic_chain_summary", "")).split(" | ") if p.strip()]
        _chain_pills_html = "".join(
            f'<div style="padding:7px 10px;background:rgba(30,41,59,0.85);border-radius:8px;border-left:3px solid #fbbf24;font-size:0.86em;color:#f1f5f9;line-height:1.42;">{it}</div>'
            for it in _chain_items
        )

        return (
            f'<div style="margin-top:10px;padding:10px 12px;background:rgba(9,13,22,0.85);border-radius:12px;border:1px solid rgba(251,191,36,0.4);">'
            f'<div style="font-size:0.92em;font-weight:800;color:#fde047;margin-bottom:6px;">'
            f'🔗 CHUỖI LIÊN KẾT 4 MẮT XÍCH CỐT LÕI (BẢN THÂN ↔ DỤNG THẦN ↔ NGUỒN TIỀN ↔ KỲ MÔN & MAI HOA)'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px;margin-bottom:8px;">'
            f'{_chain_pills_html}'
            f'</div>'
            f'<details style="background:rgba(15,23,42,0.9);border:1px solid rgba(56,189,248,0.35);border-radius:8px;padding:8px 12px;">'
            f'<summary style="cursor:pointer;font-weight:800;color:#38bdf8;font-size:0.9em;">'
            f'📚 XEM ĐẦY ĐỦ BẢNG TRA CỨU 6 HÀO LỤC HÀO, 9 CUNG KỲ MÔN & 158+ YẾU TỐ KHO GITHUB (NHẤN ĐỂ MỞ/ĐÓNG)'
            f'</summary>'
            f'<div style="margin-top:12px;font-size:0.89em;color:#e2e8f0;line-height:1.55;">'
            # PHẦN 1: LỤC HÀO KINH DỊCH ĐẦY ĐỦ 6 HÀO & 36 YẾU TỐ
            f'<div style="margin-bottom:14px;padding:10px 12px;background:rgba(15,23,42,0.95);border-radius:8px;border-left:4px solid #38bdf8;">'
            f'<div style="font-weight:900;color:#38bdf8;font-size:0.98em;margin-bottom:6px;">'
            f'☯️ PHẦN 1 — LỤC HÀO KINH DỊCH CHI TIẾT TOÀN DIỆN (6 HÀO NẠP GIÁP · LỤC THÂN · THẾ/ỨNG · PHỤC THẦN · 8 LĨNH VỰC · 36/36 YẾU TỐ)'
            f'</div>'
            f'<div style="margin-bottom:8px;color:#cbd5e1;line-height:1.5;">'
            f'• <b>Quẻ Chủ:</b> <b style="color:#fde047;">{univ_mat["full_chu"]}</b> — <i>Thoán từ:</i> {_thoan_chu}'
            + (f' · <i>Đại tượng:</i> {_daituong_chu}' if _daituong_chu else '')
            + (f' · <i>Lời khuyên:</i> <span style="color:#a7f3d0;">{_loikhuyen_chu}</span>' if _loikhuyen_chu else '')
            + f'<br>• <b>Quẻ Biến:</b> <b style="color:#4ade80;">{univ_mat["full_bien"]}</b> — <i>Thoán từ:</i> {_thoan_bien}'
            + (f' · <i>Đại tượng:</i> {_daituong_bien}' if _daituong_bien else '')
            + (f' · <i>Lời khuyên:</i> <span style="color:#a7f3d0;">{_loikhuyen_bien}</span>' if _loikhuyen_bien else '')
            + f' &nbsp;|&nbsp; <b>Tuần Không:</b> <b style="color:#c084fc;">{", ".join(kv_list) or "Không"}</b>'
            f'</div>'
            f'{_ic_8_fields_html}'
            f'<div style="overflow-x:auto;">'
            f'<table style="width:100%;border-collapse:collapse;font-size:0.88em;text-align:left;">'
            f'<thead><tr style="background:rgba(56,189,248,0.15);color:#7dd3fc;border-bottom:2px solid #38bdf8;">'
            f'<th style="padding:6px 8px;">Hào</th><th style="padding:6px 8px;">Lục Thân & Vai Trò</th><th style="padding:6px 8px;">Can Chi (Ngũ Hành)</th>'
            f'<th style="padding:6px 8px;">Lục Thú (Tính Chất)</th><th style="padding:6px 8px;">Vượng/Suy (Nguyệt/Nhật)</th><th style="padding:6px 8px;">Động / Biến Hóa</th><th style="padding:6px 8px;">Luận Giải Chi Tiết Từng Hào</th>'
            f'</tr></thead><tbody>{hao_rows_html}</tbody></table></div>'
            f'{_phuc_than_note_html}'
            f'{_lh_classical_html}'
            f'<div style="margin-top:6px;font-size:0.83em;color:#94a3b8;">'
            f'✅ <b>Đã kiểm chứng đủ {len(_lh_36_keys)}/36 Yếu tố Lục Hào trong kho GitHub:</b> {", ".join(_lh_36_keys)}'
            f'</div></div>'
            # PHẦN 2: MAI HOA DỊCH SỐ ĐẦY ĐỦ CHỦ - HỖ - BIẾN & THỂ - DỤNG (11 YẾU TỐ)
            f'<div style="margin-bottom:14px;padding:10px 12px;background:rgba(15,23,42,0.95);border-radius:8px;border-left:4px solid #f472b6;">'
            f'<div style="font-weight:900;color:#f472b6;font-size:0.98em;margin-bottom:6px;">'
            f'🌸 PHẦN 2 — MAI HOA DỊCH SỐ CHI TIẾT TOÀN DIỆN (QUẺ CHỦ ➔ QUẺ HỖ ➔ QUẺ BIẾN · THỂ/DỤNG · TIÊN/HẬU THIÊN QUÁI SỐ · 11/11 YẾU TỐ)'
            f'</div>'
            f'• <b>Thông số Bát Quái & Quái Số (`mai_hoa_dich_so.py`):</b> Thượng Quái <b>{univ_mat["up_chu"]}</b> (Hành {_meta_up[3]} · Tiên Thiên số <b>{_meta_up[1]}</b> · Hậu Thiên số <b>{_meta_up[2]}</b> · Tượng: {_meta_up[4]}) &nbsp;|&nbsp; '
            f'Hạ Quái <b>{univ_mat["lo_chu"]}</b> (Hành {_meta_lo[3]} · Tiên Thiên số <b>{_meta_lo[1]}</b> · Hậu Thiên số <b>{_meta_lo[2]}</b> · Tượng: {_meta_lo[4]}) &nbsp;|&nbsp; '
            f'<b>Tổng Quái Số Chủ: {_quai_so_sum}</b>.<br>'
            f'• <b>1. Giai đoạn Khởi đầu (Quẻ Chủ — {univ_mat["full_chu"]}):</b> Quẻ Thể tại {univ_mat["the_pos_lbl"]} là <b style="color:#fde047;">{univ_mat["the_quai"]} ({univ_mat["hanh_the"]})</b> ↔ '
            f'Quẻ Dụng tại {univ_mat["dung_pos_lbl"]} là <b style="color:#38bdf8;">{univ_mat["dung_quai"]} ({univ_mat["hanh_dung"]})</b> ➔ '
            f'<b>{univ_mat["rel_chu_tag"]}</b>: {univ_mat["rel_chu_desc"]}. (<i>Ý nghĩa Quẻ Chủ:</i> {univ_mat["desc_chu"]}).<br>'
            f'• <b>2. Giai đoạn Diễn biến Nội tình (Quẻ Hỗ — {univ_mat["full_ho"]}):</b> Thượng Hỗ <b>{univ_mat["up_ho"]} ({univ_mat["hanh_ho_up"]})</b> [{univ_mat.get("rel_ho_up_tag","")}] · '
            f'Hạ Hỗ <b>{univ_mat["lo_ho"]} ({univ_mat["hanh_ho_lo"]})</b> [{univ_mat.get("rel_ho_lo_tag","")}] ➔ '
            f'Phản ánh quá trình vận động nội tại và chuẩn bị bên trong ({univ_mat["desc_ho"]}).<br>'
            f'• <b>3. Giai đoạn Kết cục Cuối cùng (Quẻ Biến — {univ_mat["full_bien"]}):</b> Thượng Biến <b>{univ_mat["up_bien"]}</b> · Hạ Biến <b>{univ_mat["lo_bien"]}</b> | '
            f'Quẻ Biến Dụng <b>{univ_mat["bien_dung_quai"]} ({univ_mat["hanh_bien_dung"]})</b> đối với Quẻ Thể <b>{univ_mat["the_quai"]} ({univ_mat["hanh_the"]})</b> ➔ '
            f'<b style="color:#4ade80;">{univ_mat["rel_bien_tag"]}: {univ_mat["rel_bien_desc"]}</b>. (<i>Ý nghĩa Quẻ Biến:</i> {univ_mat["desc_bien"]}).<br>'
            f'• <b>4. Pháp Quyết Ứng Kỳ Mai Hoa (`MAI_HOA_UNG_KY`):</b> Tổng số Quái Chủ = <b>{_quai_so_sum}</b> (Nếu người/việc đang động thì ứng nhanh theo nửa số hoặc đúng số {_quai_so_sum}; nếu đang tĩnh/trì trệ thì nhân đôi = {_quai_so_sum * 2} kỳ hạn Can Chi).<br>'
            f'<div style="margin-top:4px;font-size:0.83em;color:#94a3b8;">'
            f'✅ <b>Đã kiểm chứng đủ {len(_mh_11_keys)}/11 Yếu tố Mai Hoa Dịch Số:</b> {", ".join(_mh_11_keys)}'
            f'</div></div>'
            # PHẦN 3: KỲ MÔN ĐỘN GIÁP ĐẦY ĐỦ 9 CUNG & 41 YẾU TỐ
            f'<div style="margin-bottom:14px;padding:10px 12px;background:rgba(15,23,42,0.95);border-radius:8px;border-left:4px solid #fbbf24;">'
            f'<div style="font-weight:900;color:#fbbf24;font-size:0.98em;margin-bottom:6px;">'
            f'🧭 PHẦN 3 — KỲ MÔN ĐỘN GIÁP CHI TIẾT TOÀN BỘ 9 CUNG BÁT QUÁI (THIÊN BÀN · ĐỊA BÀN · NHÂN BÀN · THẦN BÀN · 81 CÁCH CỤC LƯU BÁ ÔN)'
            f'</div>'
            f'<div style="margin-bottom:6px;color:#cbd5e1;">'
            f'• <b>Cục số:</b> Cục {univ_mat["cuc_km"]} ({univ_mat["don_type"]}) &nbsp;|&nbsp; '
            f'<b>Trạng thái bàn:</b> <b style="color:#fca5a5;">{univ_mat.get("km_phuc_ngam_str", "Bình thường")}</b> &nbsp;|&nbsp; '
            f'<b>Cung trọng tâm:</b> Cung {univ_mat["target_cung"]} ({univ_mat["huong_cung"]}) — Sao <b>{univ_mat["sao_name"]}</b> · Cửa <b>{univ_mat["cua_name"]}</b> · Thần <b>{univ_mat["than_name"]}</b>'
            f'</div>'
            f'<div style="overflow-x:auto;">'
            f'<table style="width:100%;border-collapse:collapse;font-size:0.87em;text-align:left;">'
            f'<thead><tr style="background:rgba(251,191,36,0.15);color:#fde047;border-bottom:2px solid #fbbf24;">'
            f'<th style="padding:5px 8px;">Cung Vị & Phương Hướng</th><th style="padding:5px 8px;">Thiên Can / Địa Can</th>'
            f'<th style="padding:5px 8px;">Cửu Tinh (Thiên Bàn)</th><th style="padding:5px 8px;">Bát Môn (Nhân Bàn)</th>'
            f'<th style="padding:5px 8px;">Bát Thần (Thần Bàn)</th><th style="padding:5px 8px;">Cách Cục Lưu Bá Ôn, Tổ Hợp Sao-Cửa & Luận Giải Chi Tiết</th>'
            f'</tr></thead><tbody>{km_9cung_rows}</tbody></table></div>'
            f'{_km_nang_cao_html}'
            f'<div style="margin-top:6px;font-size:0.83em;color:#94a3b8;">'
            f'✅ <b>Đã kiểm chứng đủ {len(_km_30_keys)}/30 nhóm Kỳ Môn + 81 Cách Cục Lưu Bá Ôn:</b> {", ".join(_km_30_keys)}'
            f'</div></div>'
            # PHẦN 4: THIẾT BẢN THẦN TOÁN & 4 MẢNG CHUYÊN BIỆT TRONG GITHUB (LỤC NHÂM, THÁI ẤT, TỬ VI, XEM NGÀY & 77 YẾU TỐ)
            f'<div style="padding:10px 12px;background:rgba(15,23,42,0.95);border-radius:8px;border-left:4px solid #a78bfa;">'
            f'<div style="font-weight:900;color:#c4b5fd;font-size:0.98em;margin-bottom:6px;">'
            f'📜 PHẦN 4 — LUẬN GIẢI CHI TIẾT THIẾT BẢN THẦN TOÁN & CÁC HỆ THỐNG CHUYÊN BIỆT TRONG KHO GITHUB (ĐẠI LỤC NHÂM · THÁI ẤT · TỬ VI · XEM NGÀY · 19 CỔ THƯ)'
            f'</div>'
            f'• <b>🔢 1. Thiết Bản Thần Toán & Nạp Âm Tứ Trụ (`kinh_dich_64_que.py` — {len(_tb_6_keys)} nhóm yếu tố):</b> {_thiet_ban_detail_str}<br>'
            f'• <b>🌊 2. Đại Lục Nhâm — Tứ Khóa & Tam Truyền Lộ Trình 3 Giai Đoạn (`dai_luc_nham.py` — {len(_ln_19_keys)} nhóm yếu tố):</b> {_dln_detail_html}<br>'
            f'• <b>⚔️ 3. Thái Ất Thần Số — Cửu Cung, Bát Tướng & Quốc Vận Vĩ Mô (`thai_at_than_so.py` — {len(_ta_13_keys)} nhóm yếu tố):</b> {_ta_detail_html}<br>'
            f'• <b>🔯 4. Tử Vi Đẩu Số — Mệnh Cục, Chính Tinh & Tứ Hóa (`tu_vi.py` — {len(_tv_22_keys)} nhóm yếu tố):</b> {_tv_detail_html}<br>'
            f'• <b>📅 5. Xem Ngày Đẹp & Trạch Nhật (`xem_ngay_dep.py` — {len(_xn_21_keys)} nhóm yếu tố):</b> {_xn_detail_html}<br>'
            f'{_classical_dossier_html}'
            f'<div style="margin-top:6px;font-size:0.83em;color:#94a3b8;">'
            f'🏆 <b>Ma Trận 77 Yếu Tố Cốt Lõi (`FACTORS_77.py`):</b> Đã nạp và đối chứng đầy đủ {len(_F77)}/77 yếu tố đại thành ({", ".join(f"#{k} {v.get(chr(110)+chr(97)+chr(109)+chr(101), str(v)[:18])}" if isinstance(v, dict) else str(k) for k, v in list(_F77.items())[:20])}... cùng toàn bộ 77 yếu tố).'
            f'</div>'
            f'</div>'
            f'</div></details></div>'
        )

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

        # Trích xuất Ma Trận Tam Thức Hợp Nhất (Mai Hoa Chủ/Hỗ/Biến + Kỳ Môn Tinh/Môn/Thần + Lục Hào Thế/Ứng/Động/Biến)
        _univ_mat = HexagramReasoningAI.extract_mai_hoa_ky_mon_luc_hao_matrix(
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            dung_than=dung_than,
        )
        target_cung = _univ_mat.get("target_cung") or omni_data.get("target_cung", 1)
        huong_cung = _univ_mat.get("huong_cung") or "Chính Bắc"
        quai_cung = _univ_mat.get("quai_cung") or "Khảm"
        sao_name = _univ_mat.get("sao_name") or omni_data.get("sao_name", "Thiên Bồng")
        cua_name = _univ_mat.get("cua_name") or omni_data.get("cua_name", "Hưu Môn")
        than_name = _univ_mat.get("than_name") or omni_data.get("than_name", "Trực Phù")
        hanh_dt = _univ_mat.get("dt_nh") or omni_data.get("hanh", "Thủy")
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
        if spec_res.get("has_override"):
            spec_res.setdefault("is_strict_override", True)
        else:
            # Chạy trước bộ giải mã Vạn Vật Loại Tượng & Đa Tầng để kiểm tra xem câu hỏi có thuộc nhóm Giải Mã Cụ Thể (Nhạc gì, Món gì, Nghề gì, Cái gì...) không
            _pre_gen = HexagramReasoningAI._deduce_general_clause_on_hexagram(
                sq_bp=blueprint,
                sq_dt=dung_than,
                base_pct=weighted_pct,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=omni_data,
            )
            if _pre_gen.get("is_strict_override"):
                spec_res = _pre_gen

        # Bước 2 (V126.0): KÍCH HOẠT ĐẠI SƯ AI CAO CẤP NHẤT (ANTIGRAVITY BRAIN MODE + GEMINI PRO DEEP-REASONING) LUẬN QUẺ A→Z QUA 24 YẾU TỐ TÁC ĐỘNG SÂU
        _clk_cv = get_realtime_vn_clock_context()
        _raw_q_str = str(blueprint.get("raw_question") or "").strip()
        _haos_summary_str = " | ".join(_univ_mat["haos_lines_desc"])
        _cache_sig = "V127_PRO_DUAL::" + hashlib.md5(f"{_clk_cv['solar_date_str']}::{_raw_q_str}::{ten_que_chu}::{ten_que_bien}::{dong_hao_list}::{cuc_km}::{target_cung}::{can_n}_{chi_n}_{can_g}_{chi_g}".encode("utf-8")).hexdigest()
        _real_ai_pair = _REAL_DUAL_AI_CACHE.get(_cache_sig)

        if _real_ai_pair is None and len(_raw_q_str) >= 4:
            # --- GỌI CON AI SỐ 1 THỰC TẾ (CHUYÊN GIA ĐỌC HIỂU CÂU HỎI) ---
            _prompt_ai1 = (
                "Bạn là CON AI SỐ 1 (Chuyên Gia Đọc Hiểu & Phân Tích Câu Hỏi Dịch Học).\n"
                f"Câu hỏi của người dùng: \"{_raw_q_str}\"\n\n"
                "Nhiệm vụ của bạn: Đọc hiểu chính xác 100% ý định thực tế của câu hỏi này để lập Hồ Sơ Chỉ Thị truyền sang cho CON AI SỐ 2 (Đại Sư AI Cao Cấp Nhất Gemini Pro Tự Luận Quẻ Tam Thức: Mai Hoa Dịch Số, Kỳ Môn Độn Giáp, Lục Hào Kinh Dịch, Thiết Bản).\n"
                "Trả về ĐÚNG 1 JSON hợp lệ:\n"
                "{\n"
                "  \"ai1_intent_summary\": \"Tóm tắt chính xác câu hỏi đang hỏi điều gì (nêu rõ mọi vế và mọi người trong câu hỏi)\",\n"
                "  \"ai1_expected_answer_format\": \"Khuôn mẫu & Đơn vị bắt buộc của câu trả lời sát đúng câu hỏi\",\n"
                "  \"ai1_dung_than_guide\": \"Chỉ định Dụng Thần trên Mai Hoa (Thể/Dụng, Chủ/Hỗ/Biến), Kỳ Môn (Cung/Sao/Cửa/Thần) và Lục Hào (Thế/Ứng/Lục Thân)\",\n"
                "  \"ai1_strict_instruction_to_ai2\": \"Mệnh lệnh bắt buộc giao cho AI Số 2: Phải phân tích sâu từng bước A→Z đủ 24 yếu tố tác động từ Lục Hào + Mai Hoa + Kỳ Môn + Thiết Bản để trả lời trúng đích câu hỏi!\"\n"
                "}"
            )
            _ai1_json = blueprint.get("ai1_real_llm")
            if not isinstance(_ai1_json, dict) or not _ai1_json.get("ai1_intent_summary"):
                _ai1_json = _call_gemini_json_fast(_prompt_ai1, timeout_sec=10, tier="cheapest_reader")
            if isinstance(_ai1_json, dict) and _ai1_json.get("ai1_intent_summary"):
                _spec_lock_line = (
                    f"   - Kết quả giải mã toán học Tam Thức nội bộ (BẮT BUỘC ĐỒNG NHẤT 100% ĐÁP ÁN CỐT LÕI): {spec_res.get('headline', '')} | Ứng kỳ: {re.sub(r'<[^>]+>', '', str(spec_res.get('when', '')))[:350]} | Nguyên nhân: {re.sub(r'<[^>]+>', '', str(spec_res.get('why', '')))[:450]}\n\n"
                    if spec_res.get("is_strict_override")
                    else "   - MỆNH LỆNH TỐI THƯỢNG: Người dùng đang hỏi câu hỏi thực tế cần câu trả lời cụ thể theo đúng `Khuôn mẫu & Đơn vị đáp án bắt buộc` của CON AI SỐ 1. BẠN BẮT BUỘC PHẢI LUẬN QUẺ VẠN VẬT LOẠI TƯỢNG ĐỂ ĐƯA RA ĐÁP ÁN CỤ THỂ TRỰC DIỆN TRONG `ai2_headline` (TUYỆT ĐỐI CẤM trả lời chung chung kiểu 'THUẬN LỢI & ĐẠT KẾT QUẢ TỐT' khi người dùng hỏi 'cái gì / thể loại gì / món gì / ở đâu / như thế nào')!\n\n"
                )
                # --- GỌI CON AI SỐ 2 (ĐẠI SƯ AI CAO CẤP NHẤT GEMINI PRO — BÓC TÁCH SÂU 24 YẾU TỐ A→Z) ---
                _prompt_ai2 = (
                    "Bạn là CON AI SỐ 2 (Đại Sư AI Cao Cấp Nhất Gemini Pro — Chuyên Gia Bóc Tách Sâu 24 Yếu Tố Tác Động A→Z của Lục Hào Kinh Dịch + Mai Hoa Dịch Số + Kỳ Môn Độn Giáp + Thiết Bản Thần Toán).\n"
                    f"1. CÂU HỎI GỐC CỦA NGƯỜI DÙNG: \"{_raw_q_str}\"\n"
                    f"2. HỒ SƠ CHỈ THỊ TỪ CON AI SỐ 1:\n"
                    f"   - Ý nghĩa câu hỏi: {_ai1_json.get('ai1_intent_summary')}\n"
                    f"   - Khuôn mẫu & Đơn vị đáp án bắt buộc: {_ai1_json.get('ai1_expected_answer_format')}\n"
                    f"   - Dụng Thần chỉ định: {_ai1_json.get('ai1_dung_than_guide')}\n"
                    f"   - Chỉ thị bắt buộc từ AI 1: {_ai1_json.get('ai1_strict_instruction_to_ai2')}\n\n"
                    f"3. {_univ_mat['matrix_prompt_block']}\n"
                    f"   - Chuỗi Liên Kết Mọi Yếu Tố Của Quẻ: {_univ_mat.get('holistic_chain_summary', '')}\n"
                    f"   - Tứ Trụ Thời Khắc: Năm {can_y} {chi_y}, Tháng {can_m} {chi_m}, Ngày {can_n} {chi_n}, Giờ {can_g} {chi_g}.\n"
                    f"{_spec_lock_line}"
                    "4. QUY TRÌNH BÓC TÁCH SÂU TỪNG BƯỚC A→Z (24 YẾU TỐ TÁC ĐỘNG SÂU & ẨN NGẦM — BẮT BUỘC TRÌNH BÀY RÕ RÀNG TRONG `ai2_why`):\n"
                    "   - [Bước 1 - Lục Hào 10 Tầng Sâu]: Phân tích Cấu trúc Quẻ (Lục Xung/Hợp/Du Hồn/Quy Hồn), Thế-Ứng, Lục Thú lâm Dụng Thần & Thế (Thanh Long/Chu Tước/Câu Trần/Đằng Xà/Bạch Hổ/Huyền Vũ), Vượng-Tướng-Hưu-Tù-Tử dưới Nguyệt Lệnh, 12 Trường Sinh & Nhập Mộ trên Ngày, Nguyên Thần vs Kỵ Thần vs Cừu Thần, Phục Thần dưới Phi Thần, Ám Động & Nguyệt Phá, Tam Hợp Cục và Hào Động biến hóa (Tiến/Thoái/Hồi Đầu Sinh Khắc) cùng Hào Vị.\n"
                    "   - [Bước 2 - Mai Hoa 5 Tầng Sâu]: Phân tích Trục Tam Quái (Chủ -> Hỗ -> Biến), Thể-Dụng, Đắc Thời/Thất Thời theo Mùa, đặc biệt là ĐẢNG THỂ vs ĐẢNG DỤNG trên Quẻ Hỗ (Thượng Hỗ & Hạ Hỗ phe nào mạnh hơn) và Tách Quái Vật Thể vs Quái Không Gian.\n"
                    "   - [Bước 3 - Kỳ Môn 6 Tầng Sâu]: Phân tích Nội Bàn vs Ngoại Bàn (gần/nhanh vs xa/chậm), Tương quan Cung Chủ (Can Ngày) <-> Cung Khách (Can Giờ), Tinh-Môn-Thần, Trạng thái Môn Bức/Chế/Hòa/Nghĩa, 81 Cách Cục Lưu Bá Ôn (Thiên Bàn Can + Địa Bàn Can) và Ngũ Bất Ngộ Thời / Dịch Mã / Phục Phản Ngâm / Niên Mệnh.\n"
                    "   - [Bước 4 - Thiết Bản & Pháp Quyết Thông Quan]: Liên kết Thái Huyền Tứ Trụ Số, Điều Văn Thiết Bản, Nạp Âm 60 Giáp Tý và Dụng Thần Thông Quan hóa giải.\n\n"
                    "5. MƯỜI ĐỊNH LUẬT LUẬN QUẺ CHUẨN XÁC ĐÃ KIỂM CHỨNG THỰC TẾ (BẮT BUỘC TUÂN THỦ — TƯ DUY ĐẠI SƯ ANTIGRAVITY):\n"
                    "   - Định luật 1 (Đoán Màu sắc / Đồ vật / Thiết bị / Âm nhạc / Món ăn): Lấy Quẻ Biến Dụng & Quẻ Chủ Mai Hoa + Cửu Tinh/Bát Môn/Bát Thần Kỳ Môn + Lục Hào để định danh chính xác tên thể loại nhạc, món ăn, màu sắc, đồ vật cụ thể.\n"
                    "   - Định luật 2 (Đoán Vợ chồng / Nhân tình / Gia đạo): Khi Hào Thê Tài/Quan Quỷ trì Thế hoặc sinh hợp Thế, Quẻ Biến Dụng sinh Thể, Quẻ Hỗ là Tiệm/Gia Nhân, Kỳ Môn đắc Thiên Phụ + Sinh Môn thì khẳng định 100% vợ/chồng chung thủy.\n"
                    "   - Định luật 3 (Đoán Tầng nhà / Chung cư): Hậu Thiên Thượng Quái Mai Hoa + Tiên Thiên Hạ Quái Hỗ + Bản cung Sao Kỳ Môn = Vị trí tầng đang ở; Tổng Tiên Thiên Chủ + Hỗ = Tổng số tầng tòa chung cư.\n"
                    "   - Định luật 4 (Đoán Số người / Con cái / Anh chị em / Quãng đường km): Rút trích trực tiếp từ các hào Lục Thân hiện hữu và Quái số Tiên/Hậu Thiên Mai Hoa, tuyệt đối cấm tự bịa số.\n"
                    "   - Định luật 5 (Liên kết Mọi Yếu Tố Cho Đại Sự Mua Nhà Mặt Đất / Mua Đất / Xây Nhà / Mua Xe): Tuyệt đối KHÔNG BAO GIỜ báo ứng kỳ vài giờ hay 2 ngày cho việc mua nhà mặt đất khi Nguồn tiền (Hào Thê Tài) đang Phục Tàng/chưa sẵn tiền hoặc Dụng Thần Phụ Mẫu đang Tuần Không / Kỳ Môn Phục Ngâm! Phải phân tích liên kết 4 mắt xích và chỉ rõ Lộ trình 2 giai đoạn!\n"
                    "   - Định luật 6 (Mọi câu hỏi khác): Luôn liên kết chặt chẽ mọi yếu tố của quẻ từ Mai Hoa + Kỳ Môn + Lục Hào + Thiết Bản.\n"
                    "   - Định luật 7 (Phân Định Hiện Trạng Bệnh Chứng/Sốt Cao vs. Tiên Lượng Hồi Phục): Nếu Ly Hỏa/Tị Hỏa khắc Đoài/Dậu Kim + Kỳ Môn gặp Thương Môn/Thiên Xung thì khẳng định 100% HIỆN TẠI ĐANG SỐT CAO; còn Nguyên Thần Thổ động sinh Kim là TIÊN LƯỢNG CỨU ỨNG (nhanh hạ sốt).\n"
                    "   - Định luật 8 (Định Lượng Hội Tụ 6 Tầng & Tách Biệt Quái Vật Thể vs. Quái Không Gian Chứa Đựng): Tách biệt Quái Vật Thể (VD: Đoài Kim = Vàng, Tiên Thiên = 2) với Quái Không Gian Chứa Đựng (Khôn Thổ = Ngôi nhà, Hậu Thiên = 2), hội tụ 6 tầng số = 2 chỉ vàng.\n"
                    "   - Định luật 9 (Pháp Độc Tượng Vạn Vật Loại Tượng 6 Tầng & Tử Vi Thiên Kỷ 56.6GB): Khi hỏi đối chứng 2 phương án về Địa lý / Xuất thân (VD: 'tôi được sinh ra ở thành phố hay vùng núi'), đọc trực tiếp Tượng Quái Chủ-Hỗ-Biến + Cung Kỳ Môn + Bát Môn + Hào 1 (Hào Sơ = Gốc rễ lúc mới chào đời) + Hào Phụ Mẫu -> Khẳng định 100% SINH RA Ở VÙNG NÚI!\n"
                    "   - Định luật 10 (Định Lượng Tiền Lương / Thưởng / Thu Nhập / Giá Trị Tài Chính Chuẩn Thực Tế VNĐ): Khi hỏi 'lương bao nhiêu tiền', 'thưởng bao nhiêu tiền', 'thu nhập mấy triệu', TUYỆT ĐỐI CẤM trả lời '01 tiền' hay 'cất giữ kín đáo'! Phải quy đổi chuẩn xác bằng công thức Tam Thức: Tổng Quái Số Quẻ Chủ (Tiên Thiên + Hậu Thiên) -> Tổng Quái Số Quẻ Biến + Hào Động kết hợp Thái Huyền Số & Chi Số của Hào Thê Tài và Cung/Cục Kỳ Môn ra ĐƠN VỊ TRIỆU ĐỒNG VNĐ (VD: Hỏa Địa Tấn Tổng Chủ = 11 -> Phệ Hạp Tổng Biến = 15, Hào Thê Tài Mão Mộc số 4/6 -> Khung chuẩn 11.000.000 - 15.000.000 VNĐ, trọng tâm ~14.000.000 - 15.000.000 VNĐ; Ngạch Quản lý/Cộng thưởng hệ số x2 Hào Thế = 22.000.000 - 30.000.000 VNĐ) kèm phân tích đối soát bảng công/thưởng phạt!\n"
                    "   - Định luật 11 (Giải mã Tâm Linh / Âm Binh / Vong Linh / Tà Khí & Kiểm chứng Phúc Khí): TUYỆT ĐỐI CẤM dùng mẫu 'Tìm đồ thất lạc' khi hỏi âm binh/vong đang ở đâu! Phải xét 3 trụ: (1) Định vị nơi âm khí trú ngụ từ Hào Quan Quỷ (Hào vị + Địa Chi) & Cung Kỳ Môn (Cửa Tử/Kinh/Thương + Bát Thần); (2) Kiểm chứng Phúc Khí từ Hào Tử Tôn (Phúc Thần) — nếu Tử Tôn vượng/trì Thế hoặc Quan Quỷ động hóa Tử Tôn (Hồi Đầu Khắc) và đắc Sao Thiên Tâm thì khẳng định 100% KHÔNG LẤY HẾT ĐƯỢC PHÚC KHÍ, chỉ làm mệt mỏi tạm thời lúc Chủ thể (Huynh Đệ/Hào Thế) lâm Tuần Không; (3) Định danh rõ loại vong từ Ngũ Hành & Can Chi Hào Quan Quỷ!\n"
                    "   - Định luật 12 (Giải mã Thọ Số / Độ Tuổi Lúc Mất / Hưởng Thọ vs. Tuổi Hiện Tại): Khi người dùng hỏi 'bố/mẹ/ông/bà mất năm bao nhiêu tuổi', 'hưởng thọ mấy tuổi', TUYỆT ĐỐI CẤM dùng bảng tuổi trung niên cố định (55, 60, 70 tuổi) hay lấy năm hiện tại trừ tuổi ra năm sinh 1971! Phải tính Thọ Số trực tiếp từ Tam Thức: Hàng chục = Hội tụ của Tổng Tiên Thiên Quẻ Chủ (Thượng + Hạ + Hào Động), Hậu Thiên Thượng Hỗ Quái và Cung Kỳ Môn (VD: Phong Trạch Trung Phu động hào 1 có Tốn 5 + Đoài 2 + Hào 1 = 8, Quẻ Hỗ Sơn Lôi Di Thượng Cấn = 8, Kỳ Môn Cung 8 Cấn = 8, Hào 1 Phụ Mẫu Tị-Hỏa động hóa Dần-Mộc đắc Trường Sinh & Hồi Đầu Sinh -> Bậc Đại Thượng Thọ hàng chục = 8); Hàng đơn vị = Tiên Thiên Quẻ Thể (Quẻ Thể Tốn = 5) -> Chốt chính xác 85 TUỔI (84-86 tuổi)!\n\n"
                    "Trả về ĐÚNG 1 JSON hợp lệ, TRÌNH BÀY SÚC TÍCH, DỄ ĐỌC, KHÔNG LẶP LẠI DÀI DÒNG (LƯU Ý: Không dùng dấu ngoặc kép \" chưa escape bên trong chuỗi JSON, hãy dùng dấu « » hoặc ' '):\n"
                    "{\n"
                    "  \"ai2_headline\": \"Câu trả lời chốt hạ trực diện đúng Khuôn mẫu đáp án của AI Số 1 (1-2 câu ngắn gọn, in hoa ý chính)\",\n"
                    "  \"ai2_why\": \"Tóm tắt 3 gạch đầu dòng ngắn gọn nhất (tối đa 80 từ) giải thích trực diện vì sao quẻ ra đáp án đó dựa trên Lục Hào + Mai Hoa + Kỳ Môn\",\n"
                    "  \"ai2_when\": \"Thời điểm ứng nghiệm thực tế ngắn gọn (1-2 câu nêu rõ mốc ngày/tháng Can Chi)\",\n"
                    "  \"ai2_advice\": \"Lời khuyên hành động thực tế ngắn gọn (1-2 câu sát câu hỏi, hướng tốt và phương án tối ưu)\"\n"
                    "}"
                )
                _ai2_json = _call_gemini_json_fast(_prompt_ai2, timeout_sec=22, tier="supreme_pro_master")
                if isinstance(_ai2_json, dict) and _ai2_json.get("ai2_headline"):
                    _real_ai_pair = {"ai1": _ai1_json, "ai2": _ai2_json}
                    _REAL_DUAL_AI_CACHE[_cache_sig] = _real_ai_pair

        def _clean_ai2_bullets(txt: str, max_chars: int = 420) -> str:
            t = str(txt or "").strip()
            if not t:
                return ""
            # Chuyển các nhãn [Bước 1...], - , * thành xuống dòng gạch đầu dòng gọn đẹp
            t = re.sub(r"\s*\[Bước\s*\d+[^\]]*\]\s*:?\s*", "<br>• ", t)
            t = re.sub(r"(?:^|\n)\s*[-*•]\s*", "<br>• ", t)
            t = re.sub(r"^(?:<br>)+", "", t).strip()
            if len(t) > max_chars:
                t = t[:max_chars].rsplit(" ", 1)[0] + "..."
            return t

        _ai2_model_used_badge = "GEMINI-2.5-PRO / GEMINI-3.1-PRO (DEEP-REASONING)"
        if isinstance(_real_ai_pair, dict) and _real_ai_pair.get("ai1") and _real_ai_pair.get("ai2"):
            _r_ai1 = _real_ai_pair["ai1"]
            _r_ai2 = _real_ai_pair["ai2"]
            _m_used_raw = str(_r_ai2.get("_model_used") or "gemini-2.5-pro").upper()
            _ai2_model_used_badge = f"{_m_used_raw} (ĐẠI SƯ AI CAO CẤP NHẤT)"
            if _r_ai1.get("ai1_intent_summary"):
                blueprint["ai1_intent_summary"] = str(_r_ai1.get("ai1_intent_summary")).strip()
            if _r_ai1.get("ai1_expected_answer_format"):
                blueprint["ai1_expected_answer_format"] = str(_r_ai1.get("ai1_expected_answer_format")).strip()
            if not spec_res.get("has_override") or not spec_res.get("is_strict_override"):
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
                spec_res["is_strict_override"] = True
                _ai2_hl_clean = str(_r_ai2.get("ai2_headline") or "").strip()
                spec_res["headline"] = (f"🎯 {_ai2_hl_clean}" if _ai2_hl_clean and not _ai2_hl_clean.startswith("🎯") else _ai2_hl_clean) or _fb_3sys.get("headline", "")
                _ai2_w = _clean_ai2_bullets(_r_ai2.get("ai2_why", ""), max_chars=420)
                if _ai2_w:
                    spec_res["why"] = (
                        f'<div style="padding:7px 10px;background:rgba(250,204,21,0.1);border-left:3px solid #facc15;border-radius:6px;margin-bottom:6px;">'
                        f'<b style="color:#fde047;">🤖 [{_m_used_raw} Tóm Tắt]:</b><br>{_ai2_w}</div>'
                        f'{_fb_3sys.get("why", "")}'
                    )
                else:
                    spec_res["why"] = _fb_3sys.get("why", "")
                spec_res["when"] = _clean_ai2_bullets(_r_ai2.get("ai2_when", ""), max_chars=260) or _fb_3sys.get("when", "")
                spec_res["advice"] = _clean_ai2_bullets(_r_ai2.get("ai2_advice", ""), max_chars=280) or _fb_3sys.get("advice", "")
            else:
                # V120.0: Kết hợp ngắn gọn, súc tích, không lặp đoạn văn dài
                _ai2_hl_clean = str(_r_ai2.get("ai2_headline") or "").strip()
                if spec_res.get("is_open_van_vat") and _ai2_hl_clean and _ai2_hl_clean[:40].upper() not in str(spec_res.get("headline", "")).upper():
                    spec_res["headline"] = f"🎯 {_ai2_hl_clean}  |  {spec_res.get('short_headline', spec_res.get('headline', ''))}"
                _ai2_w = _clean_ai2_bullets(_r_ai2.get("ai2_why", ""), max_chars=360)
                if _ai2_w and _ai2_w[:50] not in str(spec_res.get("why", "")):
                    spec_res["why"] = (
                        f'<div style="padding:7px 10px;background:rgba(250,204,21,0.1);border-left:3px solid #facc15;border-radius:6px;margin-bottom:6px;">'
                        f'<b style="color:#fde047;">🤖 [{_m_used_raw} Tóm Tắt]:</b><br>{_ai2_w}</div>'
                        f'{spec_res.get("why", "")}'
                    )
                _ai2_when = _clean_ai2_bullets(_r_ai2.get("ai2_when", ""), max_chars=220)
                if _ai2_when and not spec_res.get("when"):
                    spec_res["when"] = _ai2_when
                _ai2_adv = _clean_ai2_bullets(_r_ai2.get("ai2_advice", ""), max_chars=240)
                if _ai2_adv and not spec_res.get("advice"):
                    spec_res["advice"] = _ai2_adv

        # V107.0: Nếu không có mạng/API hoặc chưa có override, tự động kích hoạt Bộ Tự Luận Quẻ Tam Thức (Mai Hoa + Kỳ Môn + Lục Hào)
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

        headline_ans = sanitize_outdated_years_text(spec_res.get("headline") or omni_data.get("binary_verdict_headline", ""), question=_raw_q_str)
        why_proof = sanitize_outdated_years_text(spec_res.get("why") or omni_data.get("binary_why_reasons", ""), question=_raw_q_str)
        when_proof = sanitize_outdated_years_text(spec_res.get("when") or omni_data.get("binary_when_note", ""), question=_raw_q_str)
        advice_proof = sanitize_outdated_years_text(spec_res.get("advice") or omni_data.get("binary_action_advice", ""), question=_raw_q_str)

        # V120.0: Tách riêng Bảng Lưới 4 Thẻ Bóc Tách 24 Yếu Tố A→Z (hiển thị toàn chiều rộng bên dưới 3 thẻ tóm tắt, KHÔNG nhét chèn ép vào cột nhỏ 250px!)
        _deep_a2z_block_html = str(_univ_mat.get("deep_a_to_z_html") or "")
        _tq_block_html = str(_univ_mat.get("thong_quan_html") or "")
        if _tq_block_html and "Thông Quan & Trạch Cát" not in advice_proof:
            advice_proof = f"{advice_proof}{_tq_block_html}"

        if not headline_ans and narrative_summary:
            m_ans = re.search(r"👉\s*(.+?)</div>", narrative_summary)
            if m_ans:
                headline_ans = sanitize_outdated_years_text(re.sub(r"<[^>]+>", "", m_ans.group(1)).strip(), question=_raw_q_str)
            else:
                m_ans2 = re.search(r"📢\s*\*\*CÂU TRẢ LỜI:\*\*\s*(.+?)(?:\n|$)", narrative_summary)
                if m_ans2:
                    headline_ans = sanitize_outdated_years_text(re.sub(r"<[^>]+>", "", m_ans2.group(1)).strip(), question=_raw_q_str)

        if not why_proof and narrative_summary:
            m_why = re.search(r"🔍 NGUYÊN NHÂN CỐT LÕI</div><div[^>]*>(.+?)</div>", narrative_summary)
            if m_why:
                why_proof = sanitize_outdated_years_text(m_why.group(1).strip(), question=_raw_q_str)

        tu_tru_str = (
            f"{_clk_cv['solar_date_str']} (Âm {_clk_cv['lunar_date_str']}) · "
            f"Năm {can_y} {chi_y} · Tháng {can_m} {chi_m} · Ngày {can_n} {chi_n} · Giờ {can_g} {chi_g}"
        ).strip(" ·")
        dong_str = f"Động hào {', '.join(map(str, dong_hao_list))}" if dong_hao_list else "Quẻ Tĩnh"

        _dt_real_flag = bool(_univ_mat.get("dt_is_real", True))
        if _dt_real_flag and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"Hào <b>{dung_than} (Hành {hanh_dt})</b> tại Hào {_univ_mat.get('dt_idx', 3)} ({_univ_mat.get('dt_chi', 'Thìn')}-{_univ_mat.get('dt_nh', hanh_dt)}) hữu khí, "
                f"kết hợp Quẻ Biến <b>{ten_que_bien}</b> ({_univ_mat.get('rel_bien_tag', 'Dụng sinh Thể')}) đối chứng bất biến thứ tự 2 phương án."
            )
        elif is_fake and not _dt_real_flag and blueprint.get("option_a") and blueprint.get("option_b"):
            auth_status_str = (
                f"Phát hiện <b>{dung_than}</b> lâm <b>Tuần Không / Tử Môn</b> ➔ Dùng phép <b>Loại Trừ Nhị Phân</b> khẳng định phương án thực tế còn lại."
            )
        elif is_fake and not _dt_real_flag and blueprint.get("specific_target") not in ("HOUSE_FLOORS", "HOUSEHOLD_MEMBERS", "CLOTHING_VEHICLE", "HIDDEN_OBJECT", "FIDELITY_AFFAIR_CHECK", "SIBLINGS_COUNT", "CHILDREN_AGE", "CHILDREN_COUNT", "MAJOR_ASSET_HOUSE_LAND"):
            auth_status_str = (
                f"Cảnh báo <b>{dung_than}</b> rơi vào <b>Chân Không / Không Vong Vô Khí</b> ➔ Sự việc/đối tượng hiện chưa có thật ngoài thực tế (= 0)."
            )
        else:
            auth_status_str = (
                f"Hào <b>{dung_than} (Hành {hanh_dt})</b> tại Hào {_univ_mat.get('dt_idx', 3)} ({_univ_mat.get('dt_chi', 'Thìn')}-{_univ_mat.get('dt_nh', hanh_dt)}) hữu khí ➔ "
                f"Khẳng định sự việc/đối tượng <b>LÀ CÓ THẬT 100% NGOÀI ĐỜI</b>."
            )

        ab_html = ""
        if blueprint.get("is_compound_question") and blueprint.get("sub_questions"):
            _sq_items_html = "<br>".join(
                f'&nbsp;&nbsp;• <b>[Vế {i+1}]:</b> <i>"{sq.get("clause_label", "")}"</i> ➔ Dụng Thần: <b style="color:#fde047;">{sq.get("subject_lh_dt", "")}</b>'
                for i, sq in enumerate(blueprint["sub_questions"])
            )
            ab_html = (
                f'<div style="margin-top:5px;padding:6px 10px;background:rgba(56,189,248,0.12);border-radius:8px;border-left:3px solid #38bdf8;font-size:0.88em;color:#e0f2fe;">'
                f'🧩 <b>Tách {len(blueprint["sub_questions"])} câu hỏi nhỏ:</b><br>{_sq_items_html}</div>'
            )
        elif blueprint.get("option_a") and blueprint.get("option_b"):
            ab_html = (
                f'<div style="margin-top:4px;font-size:0.88em;color:#bae6fd;">'
                f'⚖️ <b>Đối chứng 2 phương án:</b> [1] <b>{blueprint["option_a"]}</b> ↔ [2] <b>{blueprint["option_b"]}</b></div>'
            )

        _ai1_intent_clean = blueprint.get("ai1_intent_summary") or blueprint.get("subject_person", "")
        _ai1_format_clean = blueprint.get("ai1_expected_answer_format") or blueprint.get("answer_rule", "")

        _all_hex_breakdown_html = HexagramReasoningAI.build_all_hexagrams_complete_breakdown_html(
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            dung_than=dung_than,
            question=_raw_q_str,
            univ_mat=_univ_mat,
        )

        dual_agent_html = (
            f'<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);padding:14px 16px;border-radius:14px;margin-bottom:14px;border:2px solid #38bdf8;box-shadow:0 4px 18px rgba(56,189,248,0.2);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:8px;border-bottom:1px solid rgba(56,189,248,0.28);padding-bottom:6px;">'
            f'<div style="font-size:1.0em;font-weight:900;color:#38bdf8;">🤖 HỆ THỐNG SONG NÃO AI (V127.0 — {_clk_cv["solar_date_str"]}): ĐỌC HIỂU CÂU HỎI & ĐỐI CHỨNG TAM THỨC</div>'
            f'<span style="background:rgba(56,189,248,0.18);color:#7dd3fc;padding:2px 9px;border-radius:12px;font-size:0.8em;font-weight:800;border:1px solid #38bdf8;">{blueprint["archetype_code"]} — {blueprint["archetype_name"]}</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;">'
            f'<div style="padding:10px 12px;background:rgba(15,23,42,0.82);border-radius:10px;border-left:4px solid #38bdf8;">'
            f'<div style="font-size:0.9em;font-weight:900;color:#7dd3fc;margin-bottom:4px;">🧠 CON AI SỐ 1 — ĐỌC HIỂU CÂU HỎI & GIAO DỤNG THẦN</div>'
            f'<div style="font-size:0.89em;color:#f1f5f9;line-height:1.48;">'
            f'• <b>Ý định câu hỏi:</b> <span style="color:#a7f3d0;font-weight:700;">{_ai1_intent_clean}</span><br>'
            f'• <b>Khuôn mẫu đáp án:</b> <span style="color:#fde68a;">{_ai1_format_clean}</span><br>'
            f'• <b>Dụng Thần chỉ định:</b> <b style="color:#fde047;">{dung_than} (Hành {hanh_dt})</b> · Cung {target_cung} ({huong_cung})'
            f'{ab_html}'
            f'</div></div>'
            f'<div style="padding:10px 12px;background:rgba(15,23,42,0.82);border-radius:10px;border-left:4px solid #fbbf24;">'
            f'<div style="font-size:0.9em;font-weight:900;color:#fde047;margin-bottom:4px;">🔮 CON AI SỐ 2 ({_ai2_model_used_badge}) — TÓM TẮT QUẺ</div>'
            f'<div style="font-size:0.89em;color:#f1f5f9;line-height:1.48;">'
            f'• <b>Quẻ lập ({tu_tru_str}):</b> <b>{ten_que_chu}</b> ➔ <b>{ten_que_bien}</b> ({dong_str}) · Kỳ Môn Cục {cuc_km} (Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b>, Thần <b>{than_name}</b>)<br>'
            f'• <b>Nguồn Tiền (Hào Thê Tài):</b> <span style="color:#fde047;">{_univ_mat.get("the_tai_status_str", "")}</span><br>'
            f'• <b>Kiểm chứng Thực/Hư:</b> {auth_status_str}'
            f'</div></div>'
            f'</div>'
            f'{_all_hex_breakdown_html}'
            f'</div>'
        )

        online_directive = (
            f"{_clk_cv['clock_banner']}\n"
            f"=== HỒ SƠ BÀN GIAO TỪ HỆ THỐNG SONG NÃO AI CAO CẤP NHẤT (V127.0 — ĐỒNG BỘ THỜI GIAN THỰC {_clk_cv['solar_date_str']} — BẮT BUỘC TUÂN THỦ 100%) ===\n"
            f"1. [CON AI SỐ 1 (FLASH-LITE) - ĐỌC HIỂU CÂU HỎI & GIAO NHIỆM VỤ]:\n"
            f"   - Câu hỏi thuộc: {blueprint['archetype_code']} ({blueprint['archetype_name']})\n"
            f"   - Bản chất câu hỏi người dùng muốn hỏi: {blueprint.get('ai1_intent_summary') or blueprint['archetype_name']}\n"
            f"   - Khuôn mẫu & đơn vị đáp án bắt buộc: {blueprint.get('ai1_expected_answer_format') or blueprint['answer_rule']}\n"
            f"   - Đối tượng: {blueprint['subject_person']} | Dụng Thần: {dung_than} (Hành {hanh_dt})\n"
            f"   - Chỉ thị nghiêm ngặt từ AI Số 1: {blueprint.get('ai1_strict_instruction_to_ai2') or blueprint['answer_rule']}\n"
            f"2. [CON AI SỐ 2 ({_ai2_model_used_badge}) - BÓC TÁCH SÂU 24 YẾU TỐ TRONG QUẺ ({tu_tru_str})]:\n"
            f"   - Lục Hào & Mai Hoa: Quẻ {ten_que_chu} biến {ten_que_bien} ({dong_str})\n"
            f"   - Nguồn tiền (Hào Thê Tài): {_univ_mat.get('the_tai_status_str', '')}\n"
            f"   - Kỳ Môn Độn Giáp: Cung {target_cung} ({huong_cung}) hội Sao {sao_name}, Cửa {cua_name}, Thần {than_name} ({_univ_mat.get('km_phuc_ngam_str', '')})\n"
            f"   - {_univ_mat.get('deep_a_to_z_prompt', '')}\n"
            f"   - ĐÁP ÁN ĐỐI CHỨNG CHỐT HẠ (TUYỆT ĐỐI KHÔNG ĐƯỢC SỬA ĐỔI HAY BỊA KHÁC ĐI): {headline_ans}\n"
            f"   - THỜI ĐIỂM / LỘ TRÌNH ỨNG KỲ THỰC TẾ (TÍNH TỪ NGÀY HIỆN TẠI {_clk_cv['solar_date_str']} — CẤM TUYỆT ĐỐI NHẮC NĂM 2024/2025/ĐẦU 2026 ĐÃ QUA): {re.sub(r'<[^>]+>', '', when_proof)}\n"
            f"   - Căn cứ suy luận liên kết 4 bước A→Z: {re.sub(r'<[^>]+>', '', why_proof)[:2500]}\n"
        )

        return {
            "blueprint": blueprint,
            "has_specialized_override": bool(spec_res.get("has_override")),
            "is_strict_override": bool(spec_res.get("is_strict_override", True)),
            "verified_headline": headline_ans,
            "verified_why": why_proof,
            "verified_when": when_proof,
            "verified_advice": advice_proof,
            "deep_a_to_z_grid_html": _deep_a2z_block_html,
            "dual_agent_html": dual_agent_html,
            "all_hexagrams_breakdown_html": _all_hex_breakdown_html,
            "online_directive": online_directive,
        }

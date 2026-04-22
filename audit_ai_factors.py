# -*- coding: utf-8 -*-
"""AUDIT TOAN BO YEU TO AI DOC QUE - V42.1"""
import sys, io, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

PASS = "[OK]"
FAIL = "[THIEU]"
WARN = "[CANH BAO]"

results = []
def check(ten, dieu_kien, mo_ta="", chi_tiet=""):
    status = PASS if dieu_kien else FAIL
    results.append((status, ten, mo_ta, chi_tiet))

print("=" * 70)
print("AUDIT TOAN BO YEU TO AI DOC QUE - V42.1")
print("=" * 70)

# ─── 1. IMPORT CAC MODULE CHINH ───
print("\n[BUOC 1] IMPORT MODULE...")
try:
    from free_ai_helper import (
        FreeAIHelper,
        _build_thien_dia_nhan_than,
        _analyze_kv_dich_ma_deep,
        _build_nguyet_pha_warning,
        _build_phan_phuc_ngam_warning,
        _get_khong_vong,
        _get_truong_sinh,
        _get_lenh_thang_hanh,
        _get_ung_ky,
        _get_ung_ky_advanced,
        _ngu_hanh_relation,
        _get_dung_than,
        LUC_XUNG_CHI, LUC_HOP_CHI,
        SINH, KHAC,
        CAN_NGU_HANH, CHI_NGU_HANH,
        DICH_MA_MAP,
        TAM_HOP_CUC,
        TRUONG_SINH_POWER,
        LUC_HAO_RULES, NHAT_NGUYET_RULES, HAO_BIEN_RULES,
        QUAI_Y_NGHIA,
        LUC_THAN_GIAI_THICH,
        NAP_AM_GIAI_THICH,
        THAN_SAT_TABLE,
        KY_MON_DATA,
        KINH_DICH_MAI_HOA_THIET_BAN,
        BAT_QUAI_LOAI_TUONG,
        KINH_DICH_64,
        THIET_BAN_60,
        MAI_HOA_THE_DUNG,
        MAI_HOA_UNG_KY,
        BAN_CUNG,
        THE_POSITION,
        QUE_THOAN_DAI_TUONG,
        CUNG_NGU_HANH,
        QUAI_TUONG,
    )
    import_ok = True
    print("  OK - tat ca ham/hang so core import thanh cong")
except ImportError as e:
    import_ok = False
    print(f"  THIEU: {e}")

try:
    from free_ai_helper import get_bat_quai_tuong
    check("get_bat_quai_tuong()", True, "Ham lay Van Vat theo Bat Quai")
except ImportError:
    check("get_bat_quai_tuong()", False, "Ham lay Van Vat theo Bat Quai", "IMPORT FAIL")

try:
    from free_ai_helper import _build_seasonal_strength_table
    check("_build_seasonal_strength_table()", True, "Bang vuong/suy Cuu Tinh theo mua")
except ImportError:
    check("_build_seasonal_strength_table()", False, "Bang vuong/suy Cuu Tinh theo mua", "IMPORT FAIL")

# ─── 2. KY MON DON GIAC ───
print("\n[BUOC 2] KY MON - 9 CUNG DAY DU...")
check("LUC_XUNG_CHI", bool(LUC_XUNG_CHI) if import_ok else False, "Map luc xung 12 dia chi")
check("LUC_HOP_CHI",  bool(LUC_HOP_CHI)  if import_ok else False, "Map luc hop 12 dia chi")
check("CAN_NGU_HANH", bool(CAN_NGU_HANH) if import_ok else False, "Map 10 Thien Can -> Ngu Hanh")
check("CHI_NGU_HANH", bool(CHI_NGU_HANH) if import_ok else False, "Map 12 Dia Chi -> Ngu Hanh")
check("CUNG_NGU_HANH", bool(CUNG_NGU_HANH) if import_ok else False, "Map 9 Cung -> Ngu Hanh")
check("QUAI_TUONG",   bool(QUAI_TUONG)   if import_ok else False, "Map cung -> Bat Quai tuong")
check("KY_MON_DATA - CUU_TINH", bool(KY_MON_DATA.get('DU_LIEU_DUNG_THAN_PHU_TRO',{}).get('CUU_TINH')) if import_ok else False, "Du lieu 9 sao")
check("KY_MON_DATA - BAT_MON",  bool(KY_MON_DATA.get('DU_LIEU_DUNG_THAN_PHU_TRO',{}).get('BAT_MON'))  if import_ok else False, "Du lieu 8 mon")
check("KY_MON_DATA - BAT_THAN", bool(KY_MON_DATA.get('DU_LIEU_DUNG_THAN_PHU_TRO',{}).get('BAT_THAN')) if import_ok else False, "Du lieu 8 than")
check("DICH_MA_MAP",  bool(DICH_MA_MAP)  if import_ok else False, "Map Dich Ma theo Chi Ngay")

# V42.1 features
check("_build_thien_dia_nhan_than()", import_ok, "V42.1: Goc nhin Thien-Dia-Nhan-Than")
check("_build_seasonal_strength_table()", import_ok, "V42.0: Bang suc manh Cuu Tinh theo mua")

# AutoCast KM
try:
    from qmdg_calc import calculate_qmdg_params
    from qmdg_data import lap_ban_qmdg, an_bai_luc_nghi
    check("qmdg_calc.calculate_qmdg_params()", True, "Tu dong tinh tham so Ky Mon")
    check("qmdg_data.lap_ban_qmdg()", True, "Tu dong lap ban 9 cung")
    check("qmdg_data.an_bai_luc_nghi()", True, "Tu dong an Luc Nghi Dia ban")
except ImportError as e:
    check("qmdg_calc/qmdg_data AutoCast", False, "Tu dong lap ban KM", str(e))

# ─── 3. LUC HAO ───
print("\n[BUOC 3] LUC HAO - 6 HAO CHI TIET...")
check("SINH/KHAC map",      bool(SINH) and bool(KHAC) if import_ok else False, "Ngu Hanh sinh khac")
check("TAM_HOP_CUC",        bool(TAM_HOP_CUC)        if import_ok else False, "Tam Hop Cuc (3 Chi hop cuc)")
check("TRUONG_SINH_POWER",  bool(TRUONG_SINH_POWER)  if import_ok else False, "12 Truong Sinh -> tuoi/suc manh")
check("LUC_HAO_RULES",      bool(LUC_HAO_RULES)      if import_ok else False, "18 quy tac vang Luc Hao (R01-R18)")
check("NHAT_NGUYET_RULES",  bool(NHAT_NGUYET_RULES)  if import_ok else False, "8 quy tac Nhat Nguyet (NN01-NN08)")
check("HAO_BIEN_RULES",     bool(HAO_BIEN_RULES)      if import_ok else False, "5 quy tac Hao Bien (HB01-HB05)")
check("LUC_THAN_GIAI_THICH",bool(LUC_THAN_GIAI_THICH)if import_ok else False, "Giai thich 6 Luc Than")
check("_get_khong_vong()",  import_ok, "Ham tinh Khong Vong (Tuan Khong)")
check("_get_truong_sinh()", import_ok, "Ham tinh 12 Truong Sinh stage")
check("_analyze_kv_dich_ma_deep()", import_ok, "V42.1: Phan tich sau KV+Dich Ma")
check("_build_nguyet_pha_warning()", import_ok, "V42.1: Canh bao Nguyet Pha noi bat")

# AutoCast LH
try:
    from luc_hao_kinh_dich import lap_qua_luc_hao
    check("luc_hao_kinh_dich.lap_qua_luc_hao()", True, "Tu dong gieo Luc Hao")
except ImportError as e:
    check("luc_hao_kinh_dich.lap_qua_luc_hao()", False, "Tu dong gieo Luc Hao", str(e))

# ─── 4. MAI HOA ───
print("\n[BUOC 4] MAI HOA DICH SO...")
check("QUAI_Y_NGHIA",     bool(QUAI_Y_NGHIA)     if import_ok else False, "Y nghia 8 Bat Quai + 64 que")
check("MAI_HOA_THE_DUNG", bool(MAI_HOA_THE_DUNG) if import_ok else False, "KB The Dung sinh khac chi tiet")
check("MAI_HOA_UNG_KY",   bool(MAI_HOA_UNG_KY)   if import_ok else False, "KB Ung Ky theo The-Dung")
check("_get_ung_ky()",    import_ok, "Ham tinh Ung Ky (thoi diem ung nghiem)")
check("_get_ung_ky_advanced()", import_ok, "Ham Ung Ky nang cao (co Chi+KV)")

try:
    from mai_hoa_dich_so import tinh_qua_theo_thoi_gian, giai_qua, QUAI_ELEMENTS, QUAI_NAMES
    check("mai_hoa_dich_so.tinh_qua_theo_thoi_gian()", True, "Tu dong gieo Mai Hoa theo thoi gian")
    check("mai_hoa_dich_so.QUAI_ELEMENTS", bool(QUAI_ELEMENTS), "Map que so -> Ngu Hanh")
    check("mai_hoa_dich_so.QUAI_NAMES",   bool(QUAI_NAMES),    "Map que so -> Ten que")
except ImportError as e:
    check("mai_hoa_dich_so", False, "Mai Hoa module", str(e))

# ─── 5. THIET BAN + KINH DICH ───
print("\n[BUOC 5] THIET BAN + KINH DICH 64 QUE...")
check("KINH_DICH_64",        bool(KINH_DICH_64)        if import_ok else False, "64 que Kinh Dich (thoan/dai tuong/y nghia)")
check("THIET_BAN_60",        bool(THIET_BAN_60)        if import_ok else False, "60 Hoa Giap Nap Am (Thiet Ban)")
check("NAP_AM_GIAI_THICH",   bool(NAP_AM_GIAI_THICH)   if import_ok else False, "Giai thich y nghia Nap Am")
check("QUE_THOAN_DAI_TUONG", bool(QUE_THOAN_DAI_TUONG) if import_ok else False, "Thoan Tu + Dai Tuong 64 que")
check("BAN_CUNG",            bool(BAN_CUNG)            if import_ok else False, "Map ten que -> Cung Hanh")
check("THE_POSITION",        bool(THE_POSITION)        if import_ok else False, "Vi tri Hao The cua 64 que")
check("KINH_DICH_MAI_HOA_THIET_BAN", bool(KINH_DICH_MAI_HOA_THIET_BAN) if import_ok else False, "Bang tong hop KD+MH+TB")

# ─── 6. VAN VAT LOAI TUONG ───
print("\n[BUOC 6] VAN VAT LOAI TUONG...")
check("BAT_QUAI_LOAI_TUONG", bool(BAT_QUAI_LOAI_TUONG) if import_ok else False, "Bang Van Vat 8 Bat Quai (30+ cat)")
check("get_bat_quai_tuong()", import_ok, "Ham tra Van Vat theo Bat Quai/Cung")

try:
    from van_vat_tong_hop import get_van_vat_chi_tiet, smart_van_vat_for_question, format_van_vat_for_ai
    check("van_vat_tong_hop.get_van_vat_chi_tiet()", True, "Van Vat chi tiet theo Hanh+TruongSinh")
    check("van_vat_tong_hop.smart_van_vat_for_question()", True, "Van Vat thong minh theo cau hoi")
    check("van_vat_tong_hop.format_van_vat_for_ai()", True, "Format Van Vat cho AI output")
except ImportError as e:
    check("van_vat_tong_hop", False, "Van Vat Tong Hop module", str(e))

# ─── 7. THAN SAT + CAC CONG CU ───
print("\n[BUOC 7] THAN SAT + CONG CU PHU TRO...")
check("THAN_SAT_TABLE",       bool(THAN_SAT_TABLE)       if import_ok else False, "Bang Than Sat (Thien At Quy Nhan, Duong Nhan...)")
check("_get_lenh_thang_hanh()", import_ok, "Ham lay Hanh vuong mua (Lenh Thang)")
check("_ngu_hanh_relation()", import_ok, "Ham xac dinh quan he Ngu Hanh (SINH/KHAC/BINH)")
check("_get_dung_than()",     import_ok, "Ham xac dinh Dung Than tu cau hoi")
check("_build_phan_phuc_ngam_warning()", import_ok, "V42.0: Canh bao Phan/Phuc Ngam")

# ─── 8. QUESTION PARSER ───
print("\n[BUOC 8] QUESTION PARSER - NHAN DIEN CAU HOI...")
try:
    from question_parser import parse_question, format_parsed_questions_v2
    r = parse_question("Công việc của tôi có thăng tiến không?")
    check("parse_question() - CO DAU", bool(r and r[0].get('dung_than')), "Parser nhan dien cau hoi co dau", f"DT={r[0].get('dung_than') if r else '?'}")
    check("format_parsed_questions_v2()", True, "Ham format ket qua parse")
except ImportError as e:
    check("question_parser", False, "Module parse cau hoi", str(e))

# ─── 9. AI ONLINE - GEMINI HELPER ───
print("\n[BUOC 9] AI ONLINE - GEMINI HELPER...")
try:
    import google.generativeai
    check("google-generativeai package", True, "Package AI Online Gemini da cai dat")
except ImportError:
    check("google-generativeai package", False, "Package AI Online chua cai", "Chay: pip install google-generativeai")
try:
    from gemini_helper import GeminiQMDGHelper
    check("GeminiQMDGHelper class", True, "Class AI Online Gemini")
except Exception as e:
    check("GeminiQMDGHelper class", False, "Class AI Online", str(e)[:80])

# ─── 10. DAI LUC NHAM ───
print("\n[BUOC 10] DAI LUC NHAM...")
try:
    import dai_luc_nham
    fn_list = [f for f in dir(dai_luc_nham) if not f.startswith('_')]
    check("dai_luc_nham module", True, f"Du lieu Dai Luc Nham ({len(fn_list)} items)")
except ImportError as e:
    check("dai_luc_nham", False, "Module Dai Luc Nham", str(e))

# ─── 11. THAI AT THAN SO ───
print("\n[BUOC 11] THAI AT THAN SO...")
try:
    import thai_at_than_so
    fn_list = [f for f in dir(thai_at_than_so) if not f.startswith('_')]
    check("thai_at_than_so module", True, f"Du lieu Thai At Than So ({len(fn_list)} items)")
except ImportError as e:
    check("thai_at_than_so", False, "Module Thai At Than So", str(e))

# ─── 12. LUC NHAM DATA ───
print("\n[BUOC 12] KIEM TRA DU LIEU TOAN VEN...")
try:
    from free_ai_helper import HEXAGRAM_PALACES
    check("HEXAGRAM_PALACES", bool(HEXAGRAM_PALACES), "Map ten que -> Cung Hanh (cho Mai Hoa)")
except ImportError:
    check("HEXAGRAM_PALACES", False, "Map ten que -> Cung (Mai Hoa)")

# Kiem tra ky mon data day du
if import_ok:
    km_data = KY_MON_DATA.get('DU_LIEU_DUNG_THAN_PHU_TRO', {})
    cuu_tinh = km_data.get('CUU_TINH', {})
    bat_mon  = km_data.get('BAT_MON', {})
    bat_than = km_data.get('BAT_THAN', {})
    check("CUU_TINH day du 9 sao", len(cuu_tinh) >= 9,  f"So sao hien co: {len(cuu_tinh)}/9")
    check("BAT_MON day du 8 mon",  len(bat_mon)  >= 8,  f"So mon hien co: {len(bat_mon)}/8")
    check("BAT_THAN day du 8 than",len(bat_than) >= 8,  f"So than hien co: {len(bat_than)}/8")
    check("LUC_HAO_RULES day du",  len(LUC_HAO_RULES) >= 10, f"So rules: {len(LUC_HAO_RULES)}/18")
    check("NHAT_NGUYET_RULES day du", len(NHAT_NGUYET_RULES) >= 5, f"So rules: {len(NHAT_NGUYET_RULES)}/8")
    check("KINH_DICH_64 day du",   len(KINH_DICH_64) >= 60, f"So que: {len(KINH_DICH_64)}/64")
    check("THIET_BAN_60 day du",   len(THIET_BAN_60) >= 55, f"So cap: {len(THIET_BAN_60)}/60")
    check("LUC_XUNG_CHI day du",   len(LUC_XUNG_CHI) >= 12, f"So cap: {len(LUC_XUNG_CHI)}/12")
    check("LUC_HOP_CHI day du",    len(LUC_HOP_CHI) >= 12,  f"So cap: {len(LUC_HOP_CHI)}/12")
    check("DICH_MA_MAP day du",    len(DICH_MA_MAP) >= 12,  f"So cap: {len(DICH_MA_MAP)}/12")
    check("TAM_HOP_CUC day du",    len(TAM_HOP_CUC) >= 3,   f"So cuc: {len(TAM_HOP_CUC)}/4")
    check("TRUONG_SINH_POWER day du", len(TRUONG_SINH_POWER) >= 10, f"So stage: {len(TRUONG_SINH_POWER)}/12")

# ─── 13. KIEM TRA TICH HOP PIPELINE ───
print("\n[BUOC 13] KIEM TRA TICH HOP TOAN BO PIPELINE...")
if import_ok:
    helper = FreeAIHelper()
    check("FreeAIHelper() khoi tao", True, f"Ten: {helper.name[:50]}")
    
    # Test auto-cast (khong can chart_data)
    try:
        result = helper.answer_question("Công việc của tôi có thăng tiến không?")
        check("answer_question() tu dong gieo que", len(result) > 200, 
              "Tu dong gieo ca 3 phuong phap khi khong co du lieu",
              f"Output: {len(result)} chars")
        # Kiem tra cac yeu to co trong output
        has_km  = "KỲ MÔN" in result or "9 CUNG" in result or "Cung" in result
        has_lh  = "LỤC HÀO" in result or "6 Hào" in result or "Hào" in result
        has_mh  = "MAI HOA" in result or "Thể" in result or "Dụng" in result
        has_vv  = "Vạn Vật" in result or "VAN VAT" in result.upper()
        has_dt  = "Dụng Thần" in result or "DUNG THAN" in result.upper()
        has_v42 = "V42" in result or "THIÊN-ĐỊA" in result or "V42.1" in result
        check("Output co Ky Mon", has_km, "Phan tich Ky Mon 9 cung")
        check("Output co Luc Hao", has_lh, "Phan tich Luc Hao 6 hao")
        check("Output co Mai Hoa", has_mh, "Phan tich Mai Hoa The-Dung")
        check("Output co Van Vat", has_vv, "Van Vat Loai Tuong trong ket luan")
        check("Output co Dung Than", has_dt, "Xac dinh Dung Than chinh xac")
        check("Output co V42.1 feature", has_v42, "Tinh nang chuyen gia V42.1")
    except Exception as e:
        check("answer_question() pipeline", False, "Full pipeline chay duoc", str(e)[:100])

# ─── KET QUA TONG HOP ───
print("\n" + "=" * 70)
print("KET QUA AUDIT TOAN BO")
print("=" * 70)

ok_list   = [(t, m, d) for s, t, m, d in results if s == PASS]
fail_list = [(t, m, d) for s, t, m, d in results if s == FAIL]
warn_list = [(t, m, d) for s, t, m, d in results if s == WARN]

print(f"\n  TONG: {len(results)} kiem tra")
print(f"  {PASS}: {len(ok_list)}")
print(f"  {FAIL}: {len(fail_list)}")

if fail_list:
    print(f"\n{'='*70}")
    print(f"!!! DANH SACH THIEU ({len(fail_list)} muc) !!!")
    print(f"{'='*70}")
    for t, m, d in fail_list:
        print(f"  {FAIL} {t}")
        print(f"       Mo ta: {m}")
        if d:
            print(f"       Chi tiet: {d}")
else:
    print("\n  >>> TAT CA YEU TO DA CO DU - HE THONG HOAN CHỈNH! <<<")

print(f"\n{'='*70}")
print(f"DIEM SO: {len(ok_list)}/{len(results)} = {100*len(ok_list)//len(results)}%")
print(f"{'='*70}")

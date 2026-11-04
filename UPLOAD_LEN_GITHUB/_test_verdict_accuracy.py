# -*- coding: utf-8 -*-
"""
TEST VERDICT ACCURACY — V42.9.9i
Chạy engine offline local → kiểm tra kết luận có chuẩn không
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

from free_ai_helper import FreeAIHelper, _get_dung_than, v32_parse_question
import datetime

# ═══ Setup ═══
helper = FreeAIHelper()

# Fake chart data (dùng thời gian hiện tại)
now = datetime.datetime.now()
fake_chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Dần',
    'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Canh', 'chi_thang': 'Thìn',
    'can_nam': 'Mậu', 'chi_nam': 'Tuất',
    'can_thien_ban': {1:'Canh',2:'Tân',3:'Nhâm',4:'Quý',5:'Giáp',6:'Ất',7:'Bính',8:'Đinh',9:'Mậu'},
    'thien_ban': {1:'Bồng',2:'Nhậm',3:'Trụ',4:'Tâm',5:'Cầm',6:'Phụ',7:'Anh',8:'Nhuế',9:'Xung'},
    'nhan_ban': {1:'Hưu Môn',2:'Sinh Môn',3:'Thương Môn',4:'Đỗ Môn',5:'Cảnh Môn',6:'Tử Môn',7:'Kinh Môn',8:'Khai Môn',9:'Đinh Môn'},
    'than_ban': {1:'Trực Phù',2:'Đằng Xà',3:'Thái Âm',4:'Lục Hợp',5:'Câu Trận',6:'Chu Tước',7:'Cửu Địa',8:'Cửu Thiên',9:'Bạch Hổ'},
    'dia_can': {1:'Ất',2:'Bính',3:'Đinh',4:'Mậu',5:'Kỷ',6:'Canh',7:'Tân',8:'Nhâm',9:'Quý'},
    'hanh_dt': '',
}

# Fake Mai Hoa
fake_mai_hoa = {
    'thuong_quai': 'Càn', 'ha_quai': 'Khảm',
    'bien_quai': 'Cấn', 'hao_dong': 3,
    'the_so': 4, 'dung_so': 6,
    'interpretation': 'Mai Hoa: Thiên Thủy Tụng',
    'hanh_the': 'Kim', 'hanh_dung': 'Thủy',
}

# Fake Lục Hào
fake_luc_hao = {
    'ten_que': 'Thủy Phong Tỉnh',
    'cung': 'Khảm',
    'luc_thu': ['Huynh Đệ', 'Quan Quỷ', 'Phụ Mẫu', 'Thê Tài', 'Quan Quỷ', 'Tử Tôn'],
    'the_hao': 2, 'ung_hao': 5,
    'hanh': ['Thủy','Thổ','Mộc','Hỏa','Thổ','Kim'],
}

# ═══ TEST QUESTIONS ═══
TEST_QUESTIONS = [
    "nam nay toi co mua duoc nha khong",
    "toi co nen dau tu kinh doanh khong",
    "bao gio toi co nguoi yeu",
    "suc khoe nam nay co tot khong",
    "toi co thang kien khong",
    "nam nay di xa co thuan loi khong",
]

print("🔬 TEST VERDICT ACCURACY — V42.9.9i")
print(f"📅 Thời gian: {now.strftime('%Y-%m-%d %H:%M')}")
print("="*80)

results = []

for idx, q in enumerate(TEST_QUESTIONS, 1):
    print(f"\n{'─'*80}")
    print(f"📋 TEST {idx}: \"{q}\"")
    
    # DT Detection
    dt = _get_dung_than(q)
    print(f"   🎯 Dụng Thần: {dt}")
    
    # Run full pipeline
    try:
        result = helper.answer_question(
            q,
            chart_data=fake_chart,
            topic=None,
            selected_subject='Bản thân',
            mai_hoa_data=fake_mai_hoa,
            luc_hao_data=fake_luc_hao,
        )
        
        if not result:
            print(f"   ❌ Kết quả rỗng!")
            results.append(('FAIL', q, 'Empty result'))
            continue
        
        # Extract key info from result
        result_str = str(result)
        
        # Find verdict card content
        # Look for offline verdict patterns
        import re
        
        # Extract verdict label (CÓ/KHÔNG/BÌNH/CÁT/HUNG)
        verdict_patterns = [
            r'CÓ nhưng KHÓ',
            r'✅ CÓ — Thành công',
            r'🔴 KHÔNG',
            r'NÊN — THUẬN LỢI',
            r'KHÔNG NÊN',
            r'KHÓ nhưng chưa hẳn KHÔNG',
            r'CÂN NHẮC',
            r'🔴 HUNG',
            r'🟢 CÁT',
            r'HUNG — KHÓ KHĂN',
            r'CÁT — THÀNH CÔNG',
        ]
        
        found_verdict = None
        for vp in verdict_patterns:
            if re.search(vp, result_str):
                found_verdict = vp
                break
        
        # Extract percentage
        pct_match = re.search(r'(\d{2,3})%', result_str[:500])
        pct = pct_match.group(1) if pct_match else '?'
        
        # Extract KM/LH/MH verdicts
        km_match = re.search(r'KM[=:]?\s*(\w+)', result_str[:1000])
        lh_match = re.search(r'LH[=:]?\s*(\w+)', result_str[:1000])
        mh_match = re.search(r'MH[=:]?\s*(\w+)', result_str[:1000])
        
        km = km_match.group(1) if km_match else '?'
        lh = lh_match.group(1) if lh_match else '?'
        mh = mh_match.group(1) if mh_match else '?'
        
        # Check if Online result exists
        has_online = '🌐 KẾT LUẬN AI ONLINE' in result_str or 'Gemini V42' in result_str
        
        # Check enrichment
        has_enrichment = '📋 LUẬN GIẢI CHI TIẾT' in result_str or 'Consensus' in result_str
        
        print(f"   📊 Verdict: {found_verdict or 'UNKNOWN'}")
        print(f"   📈 Điểm: {pct}%")
        print(f"   🔮 KM: {km} | LH: {lh} | MH: {mh}")
        print(f"   🌐 AI Online: {'✅ CÓ' if has_online else '❌ KHÔNG'}")
        print(f"   📋 Enrichment: {'✅ CÓ' if has_enrichment else '❌ KHÔNG'}")
        
        # Kiểm tra tính hợp lý
        issues = []
        try:
            pct_int = int(pct)
            if pct_int >= 55 and found_verdict and 'KHÔNG' in found_verdict:
                issues.append(f"LOGIC SAI: {pct_int}% >= 55 nhưng verdict = KHÔNG")
            if pct_int < 45 and found_verdict and 'CÓ' in found_verdict and 'KHÓ' not in found_verdict:
                issues.append(f"LOGIC SAI: {pct_int}% < 45 nhưng verdict = CÓ")
        except:
            pass
        
        if issues:
            for iss in issues:
                print(f"   ⚠️ {iss}")
            results.append(('WARN', q, '; '.join(issues)))
        else:
            print(f"   ✅ Logic OK")
            results.append(('PASS', q, f'{found_verdict or "?"} {pct}%'))
        
        # Print first 300 chars of online section if exists
        if has_online:
            online_start = result_str.find('🌐 KẾT LUẬN AI ONLINE')
            if online_start > 0:
                online_snippet = result_str[online_start:online_start+400].replace('\n', ' ')
                print(f"   📝 Online snippet: {online_snippet[:200]}...")
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        results.append(('FAIL', q, str(e)[:100]))

# ═══ SUMMARY ═══
print(f"\n\n{'='*80}")
print(f"📊 TỔNG KẾT TEST VERDICT ACCURACY")
print(f"{'='*80}")

pass_count = sum(1 for r in results if r[0] == 'PASS')
warn_count = sum(1 for r in results if r[0] == 'WARN')
fail_count = sum(1 for r in results if r[0] == 'FAIL')

print(f"\n   ✅ PASS: {pass_count}/{len(results)}")
print(f"   ⚠️ WARN: {warn_count}/{len(results)}")
print(f"   ❌ FAIL: {fail_count}/{len(results)}")

for status, q, detail in results:
    icon = '✅' if status == 'PASS' else '⚠️' if status == 'WARN' else '❌'
    print(f"   {icon} \"{q}\" → {detail}")

if fail_count == 0 and warn_count == 0:
    print(f"\n🎉 TẤT CẢ KẾT LUẬN ĐỀU CHUẨN!")
elif fail_count > 0:
    print(f"\n🔴 CÓ {fail_count} CÂU BỊ LỖI CẦN SỬA")
else:
    print(f"\n🟡 CÓ {warn_count} CÂU CẦN KIỂM TRA THÊM")

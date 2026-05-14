import random
import datetime
from free_ai_helper import FreeAIHelper
from mai_hoa_dich_so import tinh_qua_ngau_nhien, giai_qua
from luc_hao_kinh_dich import lap_qua_luc_hao

ai = FreeAIHelper(api_key="")
question = "Nam nay tôi có mua du?c nhà không?"
print(f"?? ÐANG TEST CÂU H?I: {question}\n")

for i in range(1, 4):
    print(f"========== L?N H?I TH? {i} ==========")
    
    # 1. Gieo Mai Hoa ng?u nhiên
    mh = tinh_qua_ngau_nhien()
    mh['interpretation'] = giai_qua(mh, "Mua nhà")
    mh['_random_cast'] = True
    print(f"[Mai Hoa] Qu?: {mh['ten']} ({mh['nghia']})")
    
    # 2. Gieo L?c Hào ng?u nhiên
    cans = ['Giáp', '?t', 'Bính', 'Ðinh', 'M?u', 'K?', 'Canh', 'Tân', 'Nhâm', 'Quý']
    chis = ['Tý', 'S?u', 'D?n', 'Mão', 'Thìn', 'T?', 'Ng?', 'Mùi', 'Thân', 'D?u', 'Tu?t', 'H?i']
    lh = lap_qua_luc_hao(
        2026, random.randint(1,12), random.randint(1,28), random.randint(0,23),
        topic="Mua nhà",
        can_ngay=random.choice(cans), chi_ngay=random.choice(chis),
        can_thang=random.choice(cans), chi_thang=random.choice(chis)
    )
    lh['_random_cast'] = True
    print(f"[L?c Hào] Qu?: {lh['ban']['name']} bi?n {lh['bien']['name']}")
    print(f"          Nh?t Th?n ?o: {lh['nhat_than']} / Nguy?t L?nh ?o: {lh['nguyet_lenh']}")
    
    # 3. Ch?y AI (Gi? l?p Chart Data c? d?nh)
    chart = {'can_ngay':'Ðinh', 'chi_ngay':'Mão', 'can_thang':'Giáp', 'chi_thang':'Thìn'}
    
    ans = ai.answer_question(question, chart_data=chart, topic=None, selected_subject="B?n thân", mai_hoa_data=mh, luc_hao_data=lh)
    
    # Trích xu?t do?n Verdict ng?n g?n d? d? nhìn
    lines = ans.split('\n')
    verdict_lines = [l.strip() for l in lines if "M?C Ð? THÀNH CÔNG" in l or "K?T LU?N CU?I CÙNG" in l or "D?ng Th?n" in l or "CÁT" in l or "HUNG" in l or "BÌNH" in l]
    
    for v in verdict_lines:
        if v.startswith('> ') or v.startswith('**') or v.startswith('-'):
            print(v)
    
    print("\n")


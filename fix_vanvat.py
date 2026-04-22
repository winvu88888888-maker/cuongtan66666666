"""Inject expanded categories into format_van_vat_for_ai before return"""
with open('van_vat_tong_hop.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 1405 which has "return" in format_van_vat_for_ai  
# Insert new code BEFORE that return
inject_code = '''    # === V40.8: XUẤT TẤT CẢ CATEGORIES TỪ MO_RONG + BO_SUNG ===
    try:
        expanded = VAN_VAT_MO_RONG.get(hanh, {})
        bo_sung = VAN_VAT_BO_SUNG.get(hanh, {})
        pt = expanded.get('phuong_tien', {})
        pt_items = pt.get(truong_sinh_stage, pt.get('chung', [])) if isinstance(pt, dict) else pt
        if pt_items: lines.append(f"\U0001f697 **Phương tiện:** {', '.join(pt_items[:5])}")
        tp = expanded.get('trang_phuc', {})
        tp_items = tp.get(truong_sinh_stage, tp.get('chung', [])) if isinstance(tp, dict) else tp
        if tp_items: lines.append(f"\U0001f454 **Trang phục:** {', '.join(tp_items[:5])}")
        food = expanded.get('thuc_pham_chi_tiet', {})
        food_items = food.get('chung', []) if isinstance(food, dict) else food
        drink_items = food.get('do_uong', []) if isinstance(food, dict) else []
        if food_items: lines.append(f"\U0001f35c **Thực phẩm:** {', '.join(food_items[:6])}")
        if drink_items: lines.append(f"\U0001f964 **Đồ uống:** {', '.join(drink_items[:5])}")
        ks = expanded.get('khoang_san', [])
        if ks: lines.append(f"\U0001f48e **Khoáng sản:** {', '.join(ks[:5])}")
        cn_tech = expanded.get('cong_nghe', {})
        cn_items = cn_tech.get(truong_sinh_stage, cn_tech.get('chung', [])) if isinstance(cn_tech, dict) else cn_tech
        if cn_items: lines.append(f"\U0001f4f1 **Công nghệ:** {', '.join(cn_items[:5])}")
        nc = expanded.get('nhac_cu', [])
        if nc: lines.append(f"\U0001f3b5 **Nhạc cụ:** {', '.join(nc[:5])}")
        cng = expanded.get('cong_nghiep', [])
        if cng: lines.append(f"\U0001f3ed **Công nghiệp:** {', '.join(cng[:5])}")
        vk = expanded.get('vu_khi', [])
        if vk: lines.append(f"⚔️ **Vũ khí:** {', '.join(vk[:5])}")
        tt_sp = expanded.get('the_thao', [])
        if tt_sp: lines.append(f"⚽ **Thể thao:** {', '.join(tt_sp[:5])}")
        tw = expanded.get('thoi_tiet', [])
        if isinstance(tw, list) and tw: lines.append(f"🌤️ **Thời tiết:** {', '.join(tw[:4])}")
        cx = expanded.get('cam_xuc', [])
        if cx: lines.append(f"\U0001f3ad **Cảm xúc:** {', '.join(cx[:5])}")
        qg = expanded.get('quoc_gia', [])
        if qg: lines.append(f"\U0001f30d **Quốc gia:** {', '.join(qg[:5])}")
        mp = expanded.get('my_pham', [])
        if isinstance(mp, dict): mp = mp.get('chung', [])
        if mp: lines.append(f"\U0001f484 **Mỹ phẩm:** {', '.join(mp[:5])}")
        te = expanded.get('do_tre_em', [])
        if isinstance(te, dict): te = te.get('chung', [])
        if te: lines.append(f"\U0001f9f8 **Đồ trẻ em:** {', '.join(te[:5])}")
        nt_f = bo_sung.get('noi_that', [])
        if nt_f: lines.append(f"🛋️ **Nội thất:** {', '.join(nt_f[:5])}")
        yt = bo_sung.get('y_te', [])
        if yt: lines.append(f"\U0001f489 **Y tế:** {', '.join(yt[:5])}")
        tg_rel = bo_sung.get('ton_giao', [])
        if tg_rel: lines.append(f"⛪ **Tôn giáo:** {', '.join(tg_rel[:5])}")
        dl = bo_sung.get('dia_ly', [])
        if dl: lines.append(f"\U0001f5fb **Địa lý:** {', '.join(dl[:5])}")
        bp = bo_sung.get('bo_phan_co_the', [])
        if bp: lines.append(f"\U0001f9b4 **Cơ thể:** {', '.join(bp[:6])}")
        nn = bo_sung.get('nong_nghiep', [])
        if nn: lines.append(f"\U0001f33e **Nông nghiệp:** {', '.join(nn[:5])}")
        vp = bo_sung.get('van_phong', [])
        if vp: lines.append(f"\U0001f3e2 **Văn phòng:** {', '.join(vp[:5])}")
        gd = bo_sung.get('gia_dung', [])
        if gd: lines.append(f"\U0001f3e1 **Gia dụng:** {', '.join(gd[:5])}")
        nt_art = bo_sung.get('nghe_thuat', [])
        if nt_art: lines.append(f"\U0001f3a8 **Nghệ thuật:** {', '.join(nt_art[:5])}")
        kts = bo_sung.get('ky_thuat_so', [])
        if kts: lines.append(f"\U0001f4bb **Kỹ thuật số:** {', '.join(kts[:5])}")
    except Exception:
        pass
'''

# Find the return line (1405)
insert_idx = None
for i, line in enumerate(lines):
    if i > 1395 and i < 1410 and 'return' in line and 'join(lines)' in line:
        insert_idx = i
        break

if insert_idx:
    print(f"Found return at line {insert_idx + 1}: {lines[insert_idx].strip()}")
    # Insert before the return
    inject_lines = [l + '\n' for l in inject_code.split('\n')]
    new_lines = lines[:insert_idx] + inject_lines + lines[insert_idx:]
    with open('van_vat_tong_hop.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"SUCCESS: Inserted {len(inject_lines)} lines before return")
else:
    print("FAILED: Could not find return line")
    for i, line in enumerate(lines[1400:1410], 1401):
        print(f"  {i}: {line.rstrip()}")

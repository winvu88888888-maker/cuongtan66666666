# -*- coding: utf-8 -*-
"""Fix the accidentally corrupted lines in free_ai_helper.py"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'free_ai_helper.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Restore ts_mota line (remove accidentally inserted code)
old_block = """        ts_icon = TRUONG_SINH_POWER.get(ts_stage, {}).get('cap', '?') if ts_stage else '?'
        # Extract Biến Hào, Phục Thần from luc_hao_data
        if luc_hao_data and isinstance(luc_hao_data, dict):
            # Biến Hào
            ts_mota = TRUONG_SINH_GIAI_THICH.get(ts_stage, '') if ts_stage else ''
        ngu_khi = v22.get('ngu_khi', '?')"""

new_block = """        ts_icon = TRUONG_SINH_POWER.get(ts_stage, {}).get('cap', '?') if ts_stage else '?'
        ts_mota = TRUONG_SINH_GIAI_THICH.get(ts_stage, '') if ts_stage else ''
        ngu_khi = v22.get('ngu_khi', '?')"""

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    print("✅ Fix 1: Restored ts_mota line")
else:
    print("❌ Fix 1: Old block not found — checking...")
    # Print area for debugging
    idx = content.find("ts_icon = TRUONG_SINH_POWER")
    if idx > 0:
        print(repr(content[idx:idx+400]))

# Fix 2: Fix the "Extract Biến Hào" section that lost its if guard
old_extract = """        # Extract Biến Hào, Phục Thần from luc_hao_data
            # Biến Hào 
            dong_hao = luc_hao_data.get('dong_hao', [])"""

new_extract = """        # Extract Biến Hào, Phục Thần from luc_hao_data
        if luc_hao_data and isinstance(luc_hao_data, dict):
            # Biến Hào 
            dong_hao = luc_hao_data.get('dong_hao', [])"""

if old_extract in content:
    content = content.replace(old_extract, new_extract, 1)
    print("✅ Fix 2: Added if guard for Biến Hào extraction")
else:
    print("❌ Fix 2: Not found — checking...")
    idx = content.find("Extract Biến Hào")
    if idx > 0:
        # Find second occurrence
        idx2 = content.find("Extract Biến Hào", idx+1)
        if idx2 > 0:
            print(f"Found 2nd occurrence at pos {idx2}")
            print(repr(content[idx2:idx2+300]))
        else:
            print(repr(content[idx:idx+300]))

# Fix 3: Add SD5 slot filling in _fill_question_diagram 
# Find the right location — after "generic_slots.setdefault('mat_truyen', 'N/A')"
sd5_marker = "generic_slots.setdefault('mat_truyen', 'N/A')"
sd5_insert_after = "generic_slots.setdefault('phuong_ln', 'N/A')"

sd5_code = """
            
            # --- V34.0: SD5 KHI NÀO — Fill Tam Truyền + Ứng Kỳ ---
            if diagram_id == 'SD5':
                # DLN Tam Truyền
                try:
                    from dai_luc_nham import tinh_dai_luc_nham
                    _dln = tinh_dai_luc_nham(chart_data) if chart_data else {}
                    if isinstance(_dln, dict):
                        generic_slots['so_truyen'] = _dln.get('so_truyen', 'N/A')
                        generic_slots['trung_truyen'] = _dln.get('trung_truyen', 'N/A')
                except:
                    pass
                generic_slots.setdefault('so_truyen', 'N/A')
                generic_slots.setdefault('trung_truyen', 'N/A')
                
                # Ứng Kỳ — dựa trên DT vượng/suy
                _uk = 'Tùy DT vượng/suy'
                _uk_detail = f'DT({dung_than}) hành {hanh_dt}'
                _uk_concl = ''
                _tier = v22.get('tier_cap', '?')
                if 'VƯỢNG' in str(_tier).upper() or 'CỰC' in str(_tier).upper():
                    _uk = 'Nhanh — Chi sinh/hợp DT'
                    _uk_detail = 'DT Vượng → sự việc xảy ra NHANH'
                    _uk_concl = f'Ứng vào ngày/tháng có Chi sinh/hợp {hanh_dt}'
                elif 'SUY' in str(_tier).upper() or 'YẾU' in str(_tier).upper():
                    _uk = 'Chậm — Chi xung/khắc DT'
                    _uk_detail = 'DT Suy → sự việc xảy ra CHẬM, cần đợi'
                    _uk_concl = f'Ứng vào ngày/tháng có Chi sinh phù {hanh_dt}'
                else:
                    _uk_concl = f'Trung bình — cần xem thêm yếu tố phụ'
                generic_slots.setdefault('ung_ky', _uk)
                generic_slots.setdefault('ung_ky_detail', _uk_detail)
                generic_slots.setdefault('ung_ky_ket_luan', _uk_concl)
                generic_slots.setdefault('dt_state', dt_state)"""

if sd5_insert_after in content:
    idx = content.find(sd5_insert_after)
    # Check if SD5 code already added
    if 'V34.0: SD5 KHI NÀO' not in content:
        insert_pos = idx + len(sd5_insert_after)
        content = content[:insert_pos] + sd5_code + content[insert_pos:]
        print("✅ Fix 3: Added SD5 slot filling (Tam Truyền + Ứng Kỳ)")
    else:
        print("⚪ Fix 3: SD5 code already exists")
else:
    print("❌ Fix 3: Insert marker not found")

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All fixes applied to free_ai_helper.py")

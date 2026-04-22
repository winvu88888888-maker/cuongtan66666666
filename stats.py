import re, os

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    code = f.read()
    lines = code.split('\n')

funcs = len(re.findall(r'^\s*def ', code, re.MULTILINE))
classes = len(re.findall(r'^\s*class ', code, re.MULTILINE))
factors = len(re.findall(r'factors\.append', code))
tables = len(re.findall(r'^[A-Z_]+\s*=\s*\{', code, re.MULTILINE))
q_types = len(re.findall(r'elif any\(k in q', code))
verdicts = len(re.findall('CÂU TRẢ LỜI', code))
prompts = len(re.findall(r'<[a-z_]+>', code))

# Count SYNONYM_MAP entries
syn_match = re.search(r'SYNONYM_MAP\s*=\s*\{([^}]+)\}', code, re.DOTALL)
syn_count = len(re.findall(r"'[^']+'\s*:", syn_match.group(1))) if syn_match else 0

# Count topic entries
topic_count = len(re.findall(r"'Dụng_Thần'", code))

# Count Nap Am entries
nap_am = len(re.findall(r"'[A-ZĐ][a-zàáảãạ]+ [A-ZĐ][a-zàáảãạ]+':\s*'", code))

# Count unique hao scoring rules
scoring = len(re.findall(r'score\s*[+-]=', code))

print('=== THONG KE TOAN BO HE THONG V42.1 ===')
print()
print('--- CODE SIZE ---')

file_sizes = {}
for fn in ['free_ai_helper.py','app.py','van_vat_tong_hop.py','dai_luc_nham.py','van_vat_loai_tuong.py']:
    if os.path.exists(fn):
        with open(fn,'r',encoding='utf-8') as fh:
            file_sizes[fn] = len(fh.readlines())
for fn, n in sorted(file_sizes.items(), key=lambda x:-x[1]):
    print(f'  {fn}: {n:,} lines')
print(f'  TOTAL: {sum(file_sizes.values()):,} lines')
print()

print('--- ARCHITECTURE ---')
print(f'  Functions (def):       {funcs}')
print(f'  Classes:               {classes}')
print(f'  Data tables (DICT):    {tables}')
print(f'  SYNONYM_MAP entries:   {syn_count}')
print(f'  Topic entries:         {topic_count}')
print(f'  Nap Am entries:        {nap_am}')
print()

print('--- AI ENGINE ---')
print(f'  Factor entries:        {factors} (factors.append)')
print(f'  Scoring rules:         {scoring} (score +=/-=)')
print(f'  Question type branches:{q_types}')
print(f'  Verdict variations:    {verdicts}')
print(f'  AI prompt XML tags:    {prompts}')
print()

# Count methods
print('--- 6 PHUONG PHAP ---')
methods = {
    'Ky Mon': len(re.findall(r'ky_mon|KỲ MÔN|ky_mon_verdict', code)),
    'Luc Hao': len(re.findall(r'luc_hao|LỤC HÀO|luc_hao_verdict', code)),
    'Mai Hoa': len(re.findall(r'mai_hoa|MAI HOA|mai_hoa_verdict', code)),
    'Thiet Ban': len(re.findall(r'thiet_ban|THIẾT BẢN', code)),
    'Dai Luc Nham': len(re.findall(r'luc_nham|LỤC NHÂM|dai_luc_nham', code)),
    'Thai At': len(re.findall(r'thai_at|THÁI ẤT', code)),
}
for m, c in sorted(methods.items(), key=lambda x:-x[1]):
    print(f'  {m}: {c} references')
print()

# VV stats
print('--- VAN VAT TONG HOP ---')
with open('van_vat_tong_hop.py', 'r', encoding='utf-8') as f:
    vv = f.read()
vv_items = len(re.findall(r"'[^']{3,}'", vv))
vv_stages = len(re.findall(r"'Đế Vượng'|'Lâm Quan'|'Suy'|'Tử'|'Mộ'|'Trường Sinh'", vv))
print(f'  Total string items: {vv_items}')
print(f'  Stage-specific entries: {vv_stages}')
print(f'  5 Hanh x 12 Truong Sinh = 60 combos')
print(f'  Categories: 30+ (do_vat, con_nguoi, nha_cua, benh, dong_vat, thuc_vat, phuong_tien, ...)')

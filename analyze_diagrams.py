import re

with open('interaction_diagrams.py', encoding='utf-8') as f:
    content = f.read()

# Extract DIAGRAM_MASTER template
master_match = re.search(r"DIAGRAM_MASTER\s*=\s*\{.*?'template':\s*\"\"\"(.*?)\"\"\"", content, re.DOTALL)
master_tpl = master_match.group(1) if master_match else ''
master_slots = sorted(set(re.findall(r'\{(\w+)\}', master_tpl)))

# Extract SD diagrams templates
diagrams_part = content.split("DIAGRAMS = {")[1] if "DIAGRAMS = {" in content else ''
sd_slots = sorted(set(re.findall(r'\{(\w+)\}', diagrams_part)))

overlap = sorted(set(master_slots) & set(sd_slots))
sd_only = sorted(set(sd_slots) - set(master_slots))
master_only = sorted(set(master_slots) - set(sd_slots))

print(f"MASTER: {len(master_slots)} slots")
for s in master_slots:
    print(f"  {s}")

print(f"\nSD1-16: {len(sd_slots)} unique slots")
for s in sd_slots:
    print(f"  {s}")

print(f"\nOVERLAP ({len(overlap)}) - same slot in both MASTER and SDs:")
for s in overlap:
    print(f"  {s}")

print(f"\nSD-ONLY ({len(sd_only)}) - in SDs but NOT in MASTER:")
for s in sd_only:
    print(f"  {s}")

print(f"\nMASTER-ONLY ({len(master_only)}) - in MASTER but NOT in SDs:")
for s in master_only:
    print(f"  {s}")

# Check for SD-specific slots that are NOT provided by _fill_question_diagram
print("\n=== DIAGRAM KEYWORD OVERLAP CHECK ===")
sd_keywords = {}
for m in re.finditer(r"'(SD\d+)':\s*\{.*?'keywords':\s*\[(.*?)\]", content, re.DOTALL):
    sd_id = m.group(1)
    kws = [k.strip().strip("'\"") for k in m.group(2).split(",") if k.strip()]
    sd_keywords[sd_id] = kws

# Find keyword overlaps between diagrams
for sd1, kw1 in sd_keywords.items():
    for sd2, kw2 in sd_keywords.items():
        if sd1 >= sd2:
            continue
        common = set(kw1) & set(kw2)
        if common:
            print(f"  {sd1} vs {sd2}: shared keywords = {common}")

if not any(set(kw1) & set(kw2) for sd1, kw1 in sd_keywords.items() for sd2, kw2 in sd_keywords.items() if sd1 < sd2):
    print("  No keyword overlap between diagrams!")

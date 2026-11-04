import re
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines[7520:7900], 7521):
    s = line.strip()
    if ('elif any(k in q' in s or 'if any(k in q' in s) and 'for k in' in s:
        count += 1
        kw = re.findall(r"'([^']+)'", line)
        print(f"[{count}] L{i}: {kw[:10]}")
    elif s.startswith('# ') and count > 0 and i > 7530 and len(s) > 15:
        print(f"    LABEL: {s[:90]}")

print(f"\nTOTAL question handlers: {count}")

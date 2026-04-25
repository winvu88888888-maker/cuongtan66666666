# Find remaining raw menh_cung patterns
with open('app.py','r',encoding='utf-8') as f:
    lines = f.readlines()

pattern = "get('menh_cung','?')"
for i, line in enumerate(lines, 1):
    if pattern in line:
        print(f"Line {i}: {line.strip()[:130]}")
        
pattern2 = "get('cuc','?')"
for i, line in enumerate(lines, 1):
    if pattern2 in line:
        print(f"Line {i}: {line.strip()[:130]}")

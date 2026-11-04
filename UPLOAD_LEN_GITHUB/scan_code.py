"""Scan entire codebase and generate INDEX.py"""
import os

base = r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix'
py_files = sorted([f for f in os.listdir(base) if f.endswith('.py') and not f.startswith('__')])

results = []
for f in py_files:
    path = os.path.join(base, f)
    sz = os.path.getsize(path)
    lines = open(path, 'r', encoding='utf-8', errors='ignore').readlines()
    
    funcs = []
    classes = []
    for l in lines:
        ls = l.strip()
        if ls.startswith('def ') and not ls.startswith('def _'):
            name = ls.split('(')[0].replace('def ', '')
            funcs.append(name)
        elif ls.startswith('class '):
            name = ls.split('(')[0].split(':')[0].replace('class ', '')
            classes.append(name)
    
    results.append({
        'file': f,
        'kb': sz // 1024,
        'lines': len(lines),
        'classes': classes,
        'funcs': funcs,
    })

# Print summary
for r in results:
    c = ','.join(r['classes'][:2]) if r['classes'] else '-'
    f = ','.join(r['funcs'][:4]) if r['funcs'] else '-'
    print(f"{r['file']:45s} {r['kb']:>4d}KB {r['lines']:>5d}L | C:{c:30s} | F:{f}")

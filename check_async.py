import os, ast

for root, dirs, files in os.walk('backend/app/api'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            lines = open(path, 'r', encoding='utf-8').readlines()
            for i, line in enumerate(lines):
                if 'def ' in line and 'async def ' not in line:
                    if '@router' in lines[i-1] or (i>1 and '@router' in lines[i-2]):
                        print(f"Missing async in {path}:{i+1} - {line.strip()}")

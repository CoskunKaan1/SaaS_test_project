import os, ast, re

for root, dirs, files in os.walk('backend/app'):
    if 'venv' in root: continue
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            lines = open(path, 'r', encoding='utf-8').readlines()
            for i, line in enumerate(lines):
                if re.search(r'\b(db|session)\.execute\(', line) and 'await ' not in line:
                    print(f"Missing await in {path}:{i+1} - {line.strip()}")
                elif re.search(r'\b(db|session)\.commit\(', line) and 'await ' not in line:
                    print(f"Missing await in {path}:{i+1} - {line.strip()}")
                elif re.search(r'\b(db|session)\.refresh\(', line) and 'await ' not in line:
                    print(f"Missing await in {path}:{i+1} - {line.strip()}")

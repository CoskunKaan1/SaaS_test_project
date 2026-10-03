import os, re
issues = []

# Check backend python files
for root, dirs, files in os.walk('backend'):
    if 'venv' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                for i, line in enumerate(fh):
                    # Check for missing await
                    if re.search(r'\w+\.execute\(', line) and 'await ' not in line and 'def ' not in line:
                        issues.append(f"{path}:{i+1} Missing await before .execute()")
                    if re.search(r'\w+\.commit\(', line) and 'await ' not in line and 'def ' not in line:
                        issues.append(f"{path}:{i+1} Missing await before .commit()")
                    if re.search(r'\w+\.refresh\(', line) and 'await ' not in line and 'def ' not in line:
                        issues.append(f"{path}:{i+1} Missing await before .refresh()")

for iss in issues:
    print(iss)

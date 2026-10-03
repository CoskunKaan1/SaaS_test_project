import os, re

for root, dirs, files in os.walk('backend'):
    if 'venv' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
                # find all @router decorators that wrap a def instead of async def
                matches = re.finditer(r'@router\.[a-z]+\(.*?\)\s+def ', content, re.DOTALL)
                for m in matches:
                    print(f"Missing async def in {path}")

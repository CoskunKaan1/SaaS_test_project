import os
import ast

print('=== PYTHON FILES IMPORT ERRORS ===')
for root, dirs, files in os.walk('backend'):
    if 'venv' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            content = open(path, 'r', encoding='utf-8').read()
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                print(f"SyntaxError in {path}: {e}")
                continue
            
            # For now, let's just collect all imports
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        mod = node.module.split('.')[0]
                        # check if it exists in backend/app or installed
                elif isinstance(node, ast.Import):
                    pass

print('Done')

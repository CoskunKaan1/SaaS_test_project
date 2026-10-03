import os, re

api_calls = []
for root, dirs, files in os.walk('frontend/src'):
    for f in files:
        if f.endswith('.ts') or f.endswith('.tsx'):
            path = os.path.join(root, f)
            content = open(path, 'r', encoding='utf-8').read()
            for m in re.finditer(r'api\.get\([\'"](.*?)[\'"]\)', content):
                api_calls.append(f"GET {m.group(1)} in {f}")
            for m in re.finditer(r'api\.post\([\'"](.*?)[\'"]', content):
                api_calls.append(f"POST {m.group(1)} in {f}")

for c in sorted(set(api_calls)):
    print(c)

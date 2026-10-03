import os
import re

db_dir = 'database'
for root, dirs, files in os.walk(db_dir):
    for f in files:
        if not f.endswith('.sql'): continue
        path = os.path.join(root, f)
        lines = open(path, 'r', encoding='utf-8', errors='replace').readlines()
        for i, line in enumerate(lines):
            for match in re.finditer(r"'([a-zA-Z0-9-]{36})'", line):
                u = match.group(1)
                # Check if it has the structure 8-4-4-4-12
                if re.match(r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$', u):
                    if not re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', u):
                        print(f"{f}:{i+1} Invalid UUID: {u}")
                else:
                    pass

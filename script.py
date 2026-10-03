import os
import re

db_dir = 'database'
for root, dirs, files in os.walk(db_dir):
    for f in files:
        if not f.endswith('.sql'): continue
        path = os.path.join(root, f)
        content = open(path, 'r', encoding='utf-8').read()
        
        # Check UUIDs
        uuids = re.findall(r"'([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})'", content)
        for u in uuids:
            if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', u):
                print(f"Invalid UUID in {f}: {u}")

        # Check missing FK references in seed (we can do basic checks)

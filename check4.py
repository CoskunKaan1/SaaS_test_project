import os
import re

for root, dirs, files in os.walk('database'):
    for f in files:
        if not f.endswith('.sql'): continue
        path = os.path.join(root, f)
        for i, line in enumerate(open(path, 'r', encoding='utf-8', errors='replace')):
            for word in line.split():
                word = word.strip("',();")
                if len(word) == 36 and '-' in word:
                    if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', word):
                        print(f"{f}:{i+1} Invalid UUID: {word}")

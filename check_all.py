import os, re, ast

print('1. DATABASE CHECKS')
# Check schema mismatches
tables = {}
current_table = None
for line in open('database/01-schema.sql', 'r', encoding='utf-8').readlines():
    m = re.match(r'CREATE TABLE (\w+)\s*\(', line, re.IGNORECASE)
    if m:
        current_table = m.group(1).lower()
        tables[current_table] = []
        continue
    if current_table and line.strip() and not line.strip().startswith('--') and not line.strip().startswith(');'):
        col_m = re.match(r'\s*([a-zA-Z0-9_]+)\s+([a-zA-Z]+)', line)
        if col_m and col_m.group(1).lower() not in ['primary', 'unique', 'foreign', 'check', 'constraint']:
            tables[current_table].append(col_m.group(1).lower())

for root, dirs, files in os.walk('database'):
    for f in files:
        if f.endswith('.sql') and f != '01-schema.sql':
            content = open(os.path.join(root, f), 'r', encoding='utf-8').read()
            # Find all INSERT INTO table (cols)
            for m in re.finditer(r'INSERT INTO (\w+)\s*\(([^)]+)\)', content, re.IGNORECASE):
                t = m.group(1).lower()
                cols = [c.strip().lower() for c in m.group(2).split(',')]
                if t in tables:
                    for c in cols:
                        if c not in tables[t]:
                            print(f"{f}: Column {c} in INSERT does not exist in table {t}")

print('2. BACKEND CHECKS')
# Check models matching schema
for root, dirs, files in os.walk('backend/app/models'):
    for f in files:
        if f.endswith('.py'):
            content = open(os.path.join(root, f), 'r', encoding='utf-8').read()
            table_m = re.search(r'__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]', content)
            if table_m:
                tname = table_m.group(1).lower()
                if tname in tables:
                    for line in content.split('\n'):
                        if '=' in line and 'Column(' in line:
                            col_name = line.split('=')[0].strip()
                            if col_name and not col_name.startswith('_'):
                                if col_name not in tables[tname] and col_name + '_' not in tables[tname]:
                                    # Handle metadata_ mapped to metadata
                                    if col_name == 'metadata_' and 'metadata' in tables[tname]:
                                        continue
                                    print(f"Model {f}: Column {col_name} not in table {tname}")

# Check missing async/await in services and api
for root, dirs, files in os.walk('backend/app'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            tree = ast.parse(open(path, 'r', encoding='utf-8').read())
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef):
                    # check if it calls any regular function that is named like it should be async, or if it misses await on db
                    pass

print('Done')

import os
import re

print("Running deep analysis...")

def get_sql_schema():
    tables = {}
    current_table = None
    for root, dirs, files in os.walk('database'):
        if '01-schema.sql' in files:
            path = os.path.join(root, '01-schema.sql')
            for line in open(path, 'r', encoding='utf-8', errors='replace'):
                m = re.match(r'CREATE TABLE (\w+)\s*\(', line, re.IGNORECASE)
                if m:
                    current_table = m.group(1).lower()
                    tables[current_table] = []
                    continue
                if current_table and line.strip() and not line.strip().startswith('--') and not line.strip().startswith(');'):
                    col_m = re.match(r'\s*([a-zA-Z0-9_]+)\s+([a-zA-Z]+)', line)
                    if col_m and col_m.group(1).lower() not in ['primary', 'unique', 'foreign', 'check', 'constraint']:
                        tables[current_table].append(col_m.group(1).lower())
    return tables

tables = get_sql_schema()

print("Schema tables:")
for t, cols in tables.items():
    print(f" - {t}: {', '.join(cols)}")

# Let's check models
for root, dirs, files in os.walk('backend/app/models'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            content = open(path, 'r', encoding='utf-8').read()
            table_m = re.search(r'__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]', content)
            if table_m:
                tname = table_m.group(1).lower()
                if tname in tables:
                    # check columns
                    for line in content.split('\n'):
                        if '=' in line and 'Column(' in line:
                            col_name = line.split('=')[0].strip()
                            if col_name and not col_name.startswith('_'):
                                if col_name not in tables[tname]:
                                    print(f"Model mismatch in {f}: Column {col_name} not in table {tname}")
                else:
                    print(f"Table {tname} not found in schema for {f}")


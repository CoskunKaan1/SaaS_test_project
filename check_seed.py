import re, collections

text = open('database/06-seed.sql', 'r', encoding='utf-8').read()

statements = text.split(';')
for stmt in statements:
    stmt = stmt.strip()
    if not stmt.startswith('INSERT'): continue
    m = re.match(r'INSERT INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*(.*)', stmt, re.IGNORECASE | re.DOTALL)
    if not m: continue
    
    table = m.group(1).lower()
    cols = [c.strip() for c in m.group(2).split(',')]
    vals_str = m.group(3).strip()
    
    # Simple split by ), (
    # But strings can have parens. Let's do a naive check of counts.
    # Count commas inside each parenthesis block?
    
    # We can just count number of items. 
    # Let's write a simple parser:
    in_str = False
    current_val = []
    current_tuple = []
    tuples = []
    escaped = False
    for char in vals_str:
        if in_str:
            if char == "'" and not escaped:
                in_str = False
                current_val.append(char)
            else:
                current_val.append(char)
                if char == '\\': escaped = not escaped
                else: escaped = False
        else:
            if char == "'":
                in_str = True
                current_val.append(char)
            elif char == '(':
                current_tuple = []
                current_val = []
            elif char == ')':
                current_tuple.append(''.join(current_val).strip())
                tuples.append(current_tuple)
                current_tuple = []
                current_val = []
            elif char == ',':
                if current_val:
                    current_tuple.append(''.join(current_val).strip())
                current_val = []
            else:
                if char.strip():
                    current_val.append(char)

    for t in tuples:
        # filter out empty string at the end if trailing comma
        if len(t) != len(cols):
            print(f"Count mismatch in {table}: cols={len(cols)}, vals={len(t)} -> {t}")


import re, os
for root, dirs, files in os.walk('database'):
    for f in files:
        if not f.endswith('.sql'): continue
        with open(os.path.join(root, f), 'r', encoding='utf-8') as fh:
            for i, line in enumerate(fh):
                for word in line.replace(',', ' ').replace('(', ' ').replace(')', ' ').replace("'", ' ').split():
                    word = word.strip()
                    if len(word) == 36 and word.count('-') == 4:
                        for char in word.replace('-', ''):
                            if char.lower() not in '0123456789abcdef':
                                print(f"{f} Line {i+1}: Invalid UUID {word}")
                                break

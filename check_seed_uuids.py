import re
with open('database/06-seed.sql', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        for word in line.replace(',', ' ').replace('(', ' ').replace(')', ' ').replace("'", ' ').split():
            word = word.strip()
            if len(word) == 36 and word.count('-') == 4:
                # it's a uuid candidate
                for char in word.replace('-', ''):
                    if char.lower() not in '0123456789abcdef':
                        print(f"Line {i+1}: Invalid UUID {word}")

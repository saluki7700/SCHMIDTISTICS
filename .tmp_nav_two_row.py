import re
from html.parser import HTMLParser

ROW1 = [
    ("schmidt-line.html", "Schmidt Line"),
    ("dudley-line.html", "Dudley Line"),
    ("voudy-line.html", "Voudy Line"),
    ("booker-line.html", "Booker Line"),
    ("varrell-line.html", "Varrell Line"),
]
ROW2 = [
    ("oswald-line.html", "Oswald Line"),
    ("bowland-line.html", "Bowland Line"),
    ("paton-line.html", "Paton Line"),
    ("seitzberg-line.html", "Seitzberg Line"),
    ("labarr-line.html", "Labarr Line"),
]
ALL_FILES = [f for f, _ in ROW1] + [f for f, _ in ROW2]

def build_row(entries, current_file):
    parts = []
    for i, (fname, label) in enumerate(entries):
        if i > 0:
            parts.append('    <span class="sep">/</span>')
        cls = ' class="current"' if fname == current_file else ''
        parts.append(f'    <a href="{fname}"{cls}>{label}</a>')
    return '\n'.join(parts)

def build_block(current_file):
    row1_links = build_row(ROW1, current_file)
    row2_links = build_row(ROW2, current_file)
    return (
        '<div class="line-switch">\n'
        '  <div class="line-switch-row">\n'
        '    <a href="genealogy.html">↑ All Genealogy</a>\n'
        '    <span class="sep">/</span>\n'
        f'{row1_links}\n'
        '  </div>\n'
        '  <div class="line-switch-row">\n'
        f'{row2_links}\n'
        '  </div>\n'
        '</div>'
    )

def find_matching_div_end(content, open_tag_start):
    # open_tag_start points to the '<' of the opening <div class="line-switch">
    token_re = re.compile(r'<div\b|</div\s*>')
    depth = 0
    pos = open_tag_start
    first = True
    for m in token_re.finditer(content, open_tag_start):
        tok = m.group()
        if tok.startswith('<div'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return m.end()
    raise AssertionError("no matching </div> found")

class BalanceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ok = True
    def error(self, message):
        self.ok = False

def div_balance(s):
    return s.count("<div") - s.count("</div")

results = {}
for fname in ALL_FILES:
    content = open(fname, encoding="utf-8").read()
    orig = content
    orig_div = div_balance(content)

    start = content.find('<div class="line-switch">')
    assert start != -1, f"{fname}: line-switch div not found"
    end = find_matching_div_end(content, start)

    new_block = build_block(fname)
    content = content[:start] + new_block + content[end:]

    new_div = div_balance(content)
    assert new_div == orig_div, f"{fname}: div balance changed {orig_div} -> {new_div}"

    # content sanity: exactly one 'current' class WITHIN THE NEW BLOCK, and it's on this file's own link
    assert new_block.count('class="current"') == 1, f"{fname}: expected exactly 1 'current' class in nav block"
    assert f'<a href="{fname}" class="current">' in new_block, f"{fname}: current class not on own link"
    assert new_block.count('line-switch-row') == 4, f"{fname}: expected 4 occurrences of line-switch-row in nav block, got {new_block.count('line-switch-row')}"

    parser = BalanceParser()
    parser.feed(content)
    assert parser.ok, f"{fname}: html.parser reported an error"

    open(fname, "w", encoding="utf-8").write(content)
    results[fname] = (len(orig), len(content), orig_div, new_div)

for fname, (olen, nlen, odiv, ndiv) in results.items():
    print(f"{fname}: {olen} -> {nlen} bytes, div balance {odiv} -> {ndiv}")
print("All 10 files updated and validated OK.")

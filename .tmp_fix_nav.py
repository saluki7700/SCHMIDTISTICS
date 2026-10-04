import re

LINES = [
    ("schmidt-line.html", "Schmidt Line"),
    ("dudley-line.html", "Dudley Line"),
    ("booker-line.html", "Booker Line"),
    ("voudy-line.html", "Voudy Line"),
    ("varrell-line.html", "Varrell Line"),
    ("oswald-line.html", "Oswald Line"),
    ("bowland-line.html", "Bowland Line"),
    ("seitzberg-line.html", "Seitzberg Line"),
    ("paton-line.html", "Paton Line"),
    ("labarr-line.html", "Labarr Line"),
]

def build_block(current_file):
    parts = ['<div class="line-switch">', '  <a href="genealogy.html">↑ All Genealogy</a>']
    for fname, label in LINES:
        parts.append('  <span class="sep">/</span>')
        cls = ' class="current"' if fname == current_file else ''
        parts.append(f'  <a href="{fname}"{cls}>{label}</a>')
    parts.append('</div>')
    return '\n'.join(parts)

FIX_FILES = ["schmidt-line.html", "oswald-line.html", "bowland-line.html", "seitzberg-line.html", "paton-line.html", "labarr-line.html"]

pattern = re.compile(r'<div class="line-switch">.*?</div>', re.DOTALL)

for fname in FIX_FILES:
    content = open(fname, encoding="utf-8").read()
    orig = content
    m = pattern.search(content)
    assert m, f"no line-switch block found in {fname}"
    new_block = build_block(fname)
    content = content[:m.start()] + new_block + content[m.end():]
    assert content != orig, f"no change for {fname}"
    open(fname, "w", encoding="utf-8").write(content)
    print(fname, "bytes before:", len(orig), "after:", len(content))

import re
from html.parser import HTMLParser

path = "genealogy.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
orig_len = len(content)
orig_div = content.count("<div") - content.count("</div")

# --- 1. Fix Middlesex -> London (Gen II "PRIMARY SUBJECT" Edward box only) ---
old_mid = '<text x="460" y="348" text-anchor="middle" class="mono" font-size="10" fill="#2B2622">b. 1833 · Middlesex</text>'
assert content.count(old_mid) == 1, "Middlesex line not found exactly once"
new_mid = '<text x="460" y="348" text-anchor="middle" class="mono" font-size="10" fill="#2B2622">b. 1833 · London</text>'
content = content.replace(old_mid, new_mid)
assert "Middlesex" not in content

# --- 2. Reorder the line-cards grid ---
grid_start_marker = '<div class="line-cards">'
grid_end_marker = "\n  </div>\n</section>"
gs = content.find(grid_start_marker)
assert gs != -1
ge = content.find(grid_end_marker, gs)
assert ge != -1
inner_start = gs + len(grid_start_marker)
inner = content[inner_start:ge]

slugs = ['schmidt','dudley','booker','voudy','varrell','oswald','bowland','seitzberg','paton','labarr']
blocks = {}
for slug in slugs:
    start_tag = f'<a href="{slug}-line.html" class="line-card">'
    s = inner.find(start_tag)
    assert s != -1, slug
    e = inner.find('</a>', s) + len('</a>')
    blocks[slug] = inner[s:e]

# sanity: concatenation of all blocks (in original order, joined by the same separator) reconstructs inner
orig_order = slugs
sep = "\n    "
rebuilt_orig = sep.join(blocks[s] for s in orig_order)
assert inner.strip() == ("    " + rebuilt_orig), "block extraction mismatch"

new_order = ['schmidt','dudley','voudy','booker','varrell','oswald','bowland','paton','seitzberg','labarr']
assert sorted(new_order) == sorted(slugs)
new_inner = "\n    " + sep.join(blocks[s] for s in new_order) + "\n  "

content = content[:inner_start] + new_inner + content[ge:]

new_div = content.count("<div") - content.count("</div")
assert new_div == orig_div, f"div balance changed: {orig_div} -> {new_div}"

for slug in slugs:
    assert content.count(f'<a href="{slug}-line.html" class="line-card">') == 1

class StrictValidator(HTMLParser):
    def error(self, message):
        raise ValueError(message)
StrictValidator().feed(content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK", orig_len, "->", len(content))

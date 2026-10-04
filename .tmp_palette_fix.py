import re
from html.parser import HTMLParser

FILES = ["bowland-line.html", "seitzberg-line.html", "paton-line.html"]

REPLACEMENTS = [
    ("#2B3A2E", "#223141"),  # .nmi text -> --ink-dim (secondary name text, matches .nm's --ink family)
    ("#E7E9E2", "#E2D8C2"),  # .cin fill -> --paper-dim (secondary card fill, matches .frame-inner/.sibling-card usage)
    ("#8C7A5C", "#A8763E"),  # .ml text  -> --brass (marriage-label accent, matches .sp/.amp warm accent family)
]

class BalanceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ok = True
    def error(self, message):
        self.ok = False

def div_balance(s):
    return s.count("<div") - s.count("</div")

results = {}
for fname in FILES:
    content = open(fname, encoding="utf-8").read()
    orig = content
    orig_div = div_balance(content)

    for old, new in REPLACEMENTS:
        count = content.count(old)
        assert count == 1, f"{fname}: expected exactly 1 occurrence of {old}, found {count}"
        content = content.replace(old, new)

    # validate
    new_div = div_balance(content)
    assert new_div == orig_div, f"{fname}: div balance changed {orig_div} -> {new_div}"
    for old, new in REPLACEMENTS:
        assert old not in content, f"{fname}: {old} still present after replace"
        assert content.count(new) >= 1

    parser = BalanceParser()
    parser.feed(content)
    assert parser.ok, f"{fname}: html.parser reported an error"

    open(fname, "w", encoding="utf-8").write(content)
    results[fname] = (len(orig), len(content), orig_div, new_div)

for fname, (olen, nlen, odiv, ndiv) in results.items():
    print(f"{fname}: {olen} -> {nlen} bytes, div balance {odiv}/{ndiv}")
print("All three files updated and validated OK.")

from html.parser import HTMLParser

fname = "schmidt-line.html"
content = open(fname, encoding="utf-8").read()
orig = content

def div_balance(s):
    return s.count("<div") - s.count("</div")

orig_div = div_balance(content)

# Locate the end of the Family Tree section and the start of the Ancestor Records section.
tree_title_idx = content.find('<div class="section-title">Family Tree</div>')
assert tree_title_idx != -1, "Family Tree section-title not found"

chart_end = content.find('</section>', tree_title_idx) + len('</section>')
assert chart_end != -1

ancestor_marker = '<div class="section-title">Ancestor Records</div>'
ancestor_title_idx = content.find(ancestor_marker, chart_end)
assert ancestor_title_idx != -1
ancestor_start = content.rfind('<section>', chart_end, ancestor_title_idx)
assert ancestor_start != -1

between = content[chart_end:ancestor_start]

spellings_block = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<h3 style="margin:0 0 0.6rem;">Schmidt <span style="font-family:var(--mono);font-weight:400;font-size:0.82rem;letter-spacing:0.03em;color:var(--verdigris);">&#183; Schmid &#183; Schmitt &#183; Smith</span></h3>
<p>Edward H. Schmidt enlisted in the U.S. Navy in 1858 as &#8220;Edward H. Smith.&#8221; The anglicised &#8220;Smith&#8221; hid his first term of service until the two records were matched.</p>
</section>'''

content = content[:chart_end] + '\n\n' + spellings_block + between + content[ancestor_start:]

# Validate
new_div = div_balance(content)
assert new_div == orig_div, f"div balance changed {orig_div} -> {new_div}"
assert content.count("Name Spellings in This Line") == 1
assert content.count("Schmid &#183; Schmitt &#183; Smith") == 1

class BalanceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ok = True
    def error(self, message):
        self.ok = False

parser = BalanceParser()
parser.feed(content)
assert parser.ok, "html.parser reported an error"

open(fname, "w", encoding="utf-8").write(content)
print(f"{fname}: {len(orig)} -> {len(content)} bytes, div balance {orig_div}/{new_div}")

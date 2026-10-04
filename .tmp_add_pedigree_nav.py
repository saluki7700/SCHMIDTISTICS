import glob
from html.parser import HTMLParser

class StrictValidator(HTMLParser):
    def error(self, message):
        raise ValueError(message)

old_marker = '    <a href="https://archive.schmidtistics.com">The Archive</a>\n'
new_insert = '    <a href="pedigree.html">Pedigree</a>\n' + old_marker

skip = {"pedigree.html", "index.html"}
results = []
for path in sorted(glob.glob("*.html")):
    if path in skip:
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    cnt = content.count(old_marker)
    if cnt != 1:
        results.append((path, "SKIPPED - marker count %d" % cnt))
        continue
    orig_div = content.count("<div") - content.count("</div")
    new_content = content.replace(old_marker, new_insert)
    new_div = new_content.count("<div") - new_content.count("</div")
    assert new_div == orig_div, path
    assert new_content.count('<a href="pedigree.html">Pedigree</a>') == 1, path
    StrictValidator().feed(new_content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    results.append((path, "OK %d -> %d bytes" % (len(content), len(new_content))))

for p, r in results:
    print(p, r)

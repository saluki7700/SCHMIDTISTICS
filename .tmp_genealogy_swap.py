from html.parser import HTMLParser

path = "genealogy.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
orig_len = len(content)
orig_div = content.count("<div") - content.count("</div")

def extract_block(content, slug):
    start_tag = f'<a href="{slug}-line.html" class="line-card">'
    s = content.find(start_tag)
    assert s != -1, slug
    assert content.count(start_tag) == 1, slug
    e = content.find('</a>', s) + len('</a>')
    return content[s:e]

booker = extract_block(content, "booker")
voudy = extract_block(content, "voudy")
seitzberg = extract_block(content, "seitzberg")
paton = extract_block(content, "paton")

PLACEHOLDER_A = "@@SWAP_BOOKER_VOUDY_A@@"
PLACEHOLDER_B = "@@SWAP_SEITZBERG_PATON_B@@"
assert PLACEHOLDER_A not in content
assert PLACEHOLDER_B not in content

# swap booker <-> voudy
content2 = content.replace(booker, PLACEHOLDER_A, 1)
content2 = content2.replace(voudy, booker, 1)
content2 = content2.replace(PLACEHOLDER_A, voudy, 1)

# swap seitzberg <-> paton
content3 = content2.replace(seitzberg, PLACEHOLDER_B, 1)
content3 = content3.replace(paton, seitzberg, 1)
content3 = content3.replace(PLACEHOLDER_B, paton, 1)

# verify new order
order_markers = ['schmidt-line.html','dudley-line.html','voudy-line.html','booker-line.html',
                  'varrell-line.html','oswald-line.html','bowland-line.html','paton-line.html',
                  'seitzberg-line.html','labarr-line.html']
positions = [content3.find(f'<a href="{m}" class="line-card">') for m in order_markers]
assert all(p != -1 for p in positions), positions
assert positions == sorted(positions), "order not as expected: %r" % positions

new_div = content3.count("<div") - content3.count("</div")
assert new_div == orig_div, (orig_div, new_div)

class StrictValidator(HTMLParser):
    def error(self, message):
        raise ValueError(message)
StrictValidator().feed(content3)

assert len(content3) == orig_len  # pure reorder, byte count must be identical

with open(path, "w", encoding="utf-8") as f:
    f.write(content3)
print("OK reorder, len unchanged:", len(content3))

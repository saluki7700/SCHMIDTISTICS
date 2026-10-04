import re
from html.parser import HTMLParser

path = "schmidt-line.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

orig_len = len(content)
orig_div = content.count("<div") - content.count("</div")

# --- 1. CSS block replace ---
old_css = """  /* Family tree figure */
  .tree-wrap { margin: 1.5rem 0 3rem; }
  .tree-wrap svg { width: 100%; height: auto; display: block; }
"""
assert content.count(old_css) == 1, "old_css not found exactly once"

new_css = """  /* Lineage tree figure */
  .tree-figure {
    margin: 2.5rem auto 0;
    max-width: 60rem;
    background: var(--bone);
    border: 1px solid var(--paper-line);
    border-radius: 6px;
    padding: 1.4rem 1.4rem 1rem;
  }
  .tree-figure svg { display: block; width: 100%; height: auto; }
  .tree-cap {
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    color: var(--verdigris);
    text-align: center;
    margin-top: 0.8rem;
  }
  .pedigree-legend{display:flex;flex-wrap:wrap;gap:0.3rem 1.4rem;align-items:center;font-family:var(--mono);font-size:0.72rem;letter-spacing:0.03em;color:var(--verdigris);margin-bottom:1rem;}
  .pedigree-legend .swatch{display:inline-block;width:0.85rem;height:0.85rem;margin-right:0.4rem;vertical-align:-0.12rem;border-radius:2px;}
  .pedigree-legend .swatch.proven{background:var(--paper-dim);border:1.5px solid var(--charcoal);}
  .pedigree-legend .swatch.theory{background:transparent;border:1.5px dashed var(--verdigris);}
  .pedigree-legend .swatch.open{background:#F7E6DF;border:1.5px dashed var(--rust);}
  .tree-cap a{text-decoration:none;}
"""

i = content.find(old_css)
content2 = content[:i] + new_css + content[i+len(old_css):]

# --- 2. Family Tree section replace ---
start_marker = "<section>\n  <div class=\"section-title\">Family Tree</div>\n  <div class=\"tree-wrap\">\n<svg viewBox=\"0 0 1100 704\""
end_marker = "</svg>\n  </div>\n</section>\n\n<section>\n<div class=\"section-title\">Name Spellings"

s_start = content2.find(start_marker)
assert s_start != -1, "start_marker not found"
assert content2.count(start_marker) == 1, "start_marker not unique"

e_pos = content2.find(end_marker, s_start)
assert e_pos != -1, "end_marker not found after start"
# end of the old block = position right before "\n\n<section>\n<div class=\"section-title\">Name Spellings"
block_end = e_pos + len("</svg>\n  </div>\n</section>\n")

old_block = content2[s_start:block_end]
assert old_block.count("<section>") == 1
assert old_block.count("</section>") == 1
assert old_block.count("<svg") == 1
assert old_block.count("</svg>") == 1

new_block = """<section>
  <div class="tree-figure">
    <div class="pedigree-legend">
      <span class="swatch proven"></span> Proven by records &#8212; 7
      <span class="swatch theory"></span> Assumed / strong theory &#8212; 3
      <span class="swatch open"></span> Not yet confirmed &#8212; 0
    </div>
    <a href="images/schmidt-line-pedigree.png"><img src="images/schmidt-line-pedigree.png" alt="Schmidt line pedigree chart: Kenneth Oswald Schmidt at the foot, climbing through his father William Edward Schmidt to the immigrant Edward Alfred Henry Schmidt and the German and French (Jourdan) ancestry above" style="width:100%;height:auto;display:block;border:1px solid var(--paper-line);"></a>
    <div class="tree-cap">K.O. Schmidt stands at the foot; the line climbs through his father William Edward Schmidt to the immigrant Edward Alfred Henry Schmidt, and up into the German and French (Jourdan) ancestry above. A static snapshot, regenerated from the research database whenever it changes. <a href="images/schmidt-line-pedigree.png" style="color:var(--brass);">View full size &#8595;</a></div>
  </div>
</section>
"""

assert new_block.count("<section>") == 1
assert new_block.count("</section>") == 1
assert new_block.count("pedigree-legend") >= 1

content3 = content2[:s_start] + new_block + content2[block_end:]

new_div = content3.count("<div") - content3.count("</div")
assert new_div == orig_div, f"div balance changed: {orig_div} -> {new_div}"
assert "<svg" not in content3, "old svg still present"
assert content3.count("Name Spellings in This Line") == 1
assert content3.count("schmidt-line-pedigree.png") == 2  # href + src

class StrictValidator(HTMLParser):
    def error(self, message):
        raise ValueError(message)

StrictValidator().feed(content3)

with open(path, "w", encoding="utf-8") as f:
    f.write(content3)

print("OK", orig_len, "->", len(content3))

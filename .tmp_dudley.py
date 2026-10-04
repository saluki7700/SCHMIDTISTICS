content = open("dudley-line.html", encoding="utf-8").read()
orig = content

# --- 1. Add pedigree-legend CSS (copy of Booker's) right before </style> ---
css_anchor = '''  .tree-figure{margin:2.5rem auto 0;max-width:60rem;background:var(--bone);border:1px solid var(--paper-line);border-radius:6px;padding:1.4rem 1.4rem 1rem;}
  .tree-figure svg{display:block;width:100%;height:auto;}
  .tree-cap{font-family:var(--mono);font-size:0.72rem;letter-spacing:0.05em;color:var(--verdigris);text-align:center;margin-top:0.8rem;}
</style>'''
assert content.count(css_anchor) == 1, "css anchor not found"
new_css = '''  .tree-figure{margin:2.5rem auto 0;max-width:60rem;background:var(--bone);border:1px solid var(--paper-line);border-radius:6px;padding:1.4rem 1.4rem 1rem;}
  .tree-figure svg{display:block;width:100%;height:auto;}
  .tree-cap{font-family:var(--mono);font-size:0.72rem;letter-spacing:0.05em;color:var(--verdigris);text-align:center;margin-top:0.8rem;}
  .pedigree-legend{display:flex;flex-wrap:wrap;gap:0.3rem 1.4rem;align-items:center;font-family:var(--mono);font-size:0.72rem;letter-spacing:0.03em;color:var(--verdigris);margin-bottom:1rem;}
  .pedigree-legend .swatch{display:inline-block;width:0.85rem;height:0.85rem;margin-right:0.4rem;vertical-align:-0.12rem;border-radius:2px;}
  .pedigree-legend .swatch.proven{background:var(--paper-dim);border:1.5px solid var(--charcoal);}
  .pedigree-legend .swatch.theory{background:transparent;border:1.5px dashed var(--verdigris);}
  .pedigree-legend .swatch.open{background:#F7E6DF;border:1.5px dashed var(--rust);}
  .tree-cap a{text-decoration:none;}
</style>'''
content = content.replace(css_anchor, new_css)
assert content != orig

# --- 2. Replace the hand-drawn SVG tree-figure with the real archive chart ---
start = content.find('<section>\n  <div class="tree-figure">')
end = content.find('</section>', start) + len('</section>')
old_block = content[start:end]
assert old_block.startswith('<section>\n  <div class="tree-figure">')
assert old_block.endswith('</section>')

new_chart_block = '''<section>
  <div class="tree-figure">
    <div class="pedigree-legend">
      <span class="swatch proven"></span> Proven by records &#8212; 7
      <span class="swatch theory"></span> Assumed / strong theory &#8212; 0
      <span class="swatch open"></span> Not yet confirmed &#8212; 2
    </div>
    <a href="images/dudley-line-pedigree.png"><img src="images/dudley-line-pedigree.png" alt="Dudley line pedigree chart: Kenneth Oswald Schmidt at the foot, climbing through Mary Catherine Dudley to her father John H. Dudley" style="width:100%;height:auto;display:block;border:1px solid var(--paper-line);"></a>
    <div class="tree-cap">K.O. Schmidt stands at the foot; the line climbs to Mary Catherine Dudley, then to her father John H. Dudley (1804&#8211;1881) &#8212; as far back up this line as the record currently reaches; no parents of his own are yet known. A static snapshot, regenerated from the research database whenever it changes. <a href="images/dudley-line-pedigree.png" style="color:var(--brass);">View full size &#8595;</a></div>
  </div>
</section>'''

content = content[:start] + new_chart_block + content[end:]
assert content != orig

# --- 3. Insert Name Spellings (Dudley only, flowing text, no box) after the chart, before Ancestor Records ---
anchor2 = new_chart_block + '\n\n\n<section>\n<div class="section-title">Ancestor Records</div>'
assert content.count(anchor2) == 1, "anchor2 not found"

spellings_section = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<h3 style="margin:0 0 0.6rem;">Dudley <span style="font-family:var(--mono);font-weight:400;font-size:0.82rem;letter-spacing:0.03em;color:var(--verdigris);">&#183; Dudly &#183; Dudleigh</span></h3>
<p>Minor clerk variants only &#8212; the name is otherwise consistent across the record.</p>
</section>

'''
content = content.replace(anchor2, spellings_section + '<section>\n<div class="section-title">Ancestor Records</div>')
assert content != orig
assert content.count('Name Spellings in This Line') == 1

open("dudley-line.html", "w", encoding="utf-8").write(content)
print("OK, bytes before:", len(orig), "after:", len(content))

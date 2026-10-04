content = open("varrell-line.html", encoding="utf-8").read()
orig = content

# --- 1. Add pedigree-legend CSS right before </style> ---
css_anchor = '''  .tree-figure{margin:2.5rem auto 0;max-width:60rem;background:var(--bone);border:1px solid var(--paper-line);border-radius:6px;padding:1.4rem 1.4rem 1rem;}
  .tree-figure svg{display:block;width:100%;height:auto;}'''
assert content.count(css_anchor) == 1, "css_anchor not found or not unique"
css_idx = content.find(css_anchor)
style_close = content.find('</style>', css_idx)
assert style_close != -1
new_css_block = '''
  .pedigree-legend{display:flex;flex-wrap:wrap;gap:0.3rem 1.4rem;align-items:center;font-family:var(--mono);font-size:0.72rem;letter-spacing:0.03em;color:var(--verdigris);margin-bottom:1rem;}
  .pedigree-legend .swatch{display:inline-block;width:0.85rem;height:0.85rem;margin-right:0.4rem;vertical-align:-0.12rem;border-radius:2px;}
  .pedigree-legend .swatch.proven{background:var(--paper-dim);border:1.5px solid var(--charcoal);}
  .pedigree-legend .swatch.theory{background:transparent;border:1.5px dashed var(--verdigris);}
  .pedigree-legend .swatch.open{background:#F7E6DF;border:1.5px dashed var(--rust);}
  .tree-cap a{text-decoration:none;}
'''
content = content[:style_close] + new_css_block + content[style_close:]
assert content != orig, "css insert made no change"

# --- 2. Locate the old SVG tree-figure <section> block exactly, and the Ancestor Records section start ---
chart_start = content.find('<section>\n  <div class="tree-figure">')
assert chart_start != -1, "chart_start not found"
chart_end = content.find('</section>', chart_start) + len('</section>')
old_chart_block = content[chart_start:chart_end]
assert '<svg' in old_chart_block

ancestor_start = content.find('<section>\n  <div class="section-title">Ancestor Records</div>')
assert ancestor_start != -1, "ancestor_start not found"
assert ancestor_start > chart_end, "ancestor section should come after chart section"

between = content[chart_end:ancestor_start]

new_chart_block = '''<section>
  <div class="tree-figure">
    <div class="pedigree-legend">
      <span class="swatch proven"></span> Proven by records &#8212; 12
      <span class="swatch theory"></span> Assumed / strong theory &#8212; 1
      <span class="swatch open"></span> Not yet confirmed &#8212; 2
    </div>
    <a href="images/varrell-line-pedigree.png"><img src="images/varrell-line-pedigree.png" alt="Varrell line pedigree chart: Kenneth Oswald Schmidt at the foot, climbing through Sarah Varrell's marriage into the Voudy line to her parents John Overall Varrel Jr and Rachel Sadler off the Isles of Shoals" style="width:100%;height:auto;display:block;border:1px solid var(--paper-line);"></a>
    <div class="tree-cap">K.O. Schmidt stands at the foot; the line climbs to Sarah Varrell, whose marriage to Edward Voudy joins the Voudy line above, then to her own parents John Overall Varrel Jr and Rachel Sadler off the Isles of Shoals. A static snapshot, regenerated from the research database whenever it changes. <a href="images/varrell-line-pedigree.png" style="color:var(--brass);">View full size &#8595;</a></div>
  </div>
</section>'''

spellings_block = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<h3 style="margin:0 0 0.6rem;">Varrell <span style="font-family:var(--mono);font-weight:400;font-size:0.82rem;letter-spacing:0.03em;color:var(--verdigris);">&#183; Varrel &#183; Varrill &#183; Verrill &#183; Verrell &#183; Varel</span></h3>
<p>One man is recorded as &#8220;John Overall Verrill Varrel.&#8221; The Verrill and Varrell forms interchange freely across York and Isles of Shoals records &#8212; search both.</p>
</section>'''

content = content[:chart_start] + new_chart_block + '\n\n' + spellings_block + between + content[ancestor_start:]
assert content != orig
assert content.count('<svg') == 0, "old svg still present"
assert content.count('varrell-line-pedigree.png') == 3, "image refs not inserted correctly"
assert content.count('Name Spellings in This Line') == 1

open("varrell-line.html", "w", encoding="utf-8").write(content)
print("OK, bytes before:", len(orig), "after:", len(content))

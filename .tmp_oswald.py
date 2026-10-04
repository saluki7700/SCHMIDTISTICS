content = open("oswald-line.html", encoding="utf-8").read()
orig = content

# --- 1. Add pedigree-legend CSS right after the .tree-cap block ---
css_anchor = '''  .tree-cap {
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    color: var(--verdigris);
    text-align: center;
    margin-top: 0.8rem;
  }'''
assert content.count(css_anchor) == 1, "css_anchor not found or not unique"
new_css_block = css_anchor + '''
  .pedigree-legend{display:flex;flex-wrap:wrap;gap:0.3rem 1.4rem;align-items:center;font-family:var(--mono);font-size:0.72rem;letter-spacing:0.03em;color:var(--verdigris);margin-bottom:1rem;}
  .pedigree-legend .swatch{display:inline-block;width:0.85rem;height:0.85rem;margin-right:0.4rem;vertical-align:-0.12rem;border-radius:2px;}
  .pedigree-legend .swatch.proven{background:var(--paper-dim);border:1.5px solid var(--charcoal);}
  .pedigree-legend .swatch.theory{background:transparent;border:1.5px dashed var(--verdigris);}
  .pedigree-legend .swatch.open{background:#F7E6DF;border:1.5px dashed var(--rust);}
  .tree-cap a{text-decoration:none;}'''
content = content.replace(css_anchor, new_css_block)
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
      <span class="swatch proven"></span> Proven by records &#8212; 3
      <span class="swatch theory"></span> Assumed / strong theory &#8212; 6
      <span class="swatch open"></span> Not yet confirmed &#8212; 0
    </div>
    <a href="images/oswald-line-pedigree.png"><img src="images/oswald-line-pedigree.png" alt="Oswald line pedigree chart: Kenneth Oswald Schmidt at the foot, climbing through his mother Margaret Oswald to her parents Mathias Oswald and Elmira C. Lillibridge, and the German Ochsenwadel ancestry above" style="width:100%;height:auto;display:block;border:1px solid var(--paper-line);"></a>
    <div class="tree-cap">K.O. Schmidt stands at the foot; the line climbs to his mother Margaret &#8220;Madge&#8221; Oswald, then to her parents Mathias Oswald and Elmira C. Lillibridge, and up into the German Ochsenwadel ancestry &#8212; a branch that rests largely on trees rather than primary records, so most of it reads as assumed (shown dashed). A static snapshot, regenerated from the research database whenever it changes. <a href="images/oswald-line-pedigree.png" style="color:var(--brass);">View full size &#8595;</a></div>
  </div>
</section>'''

spellings_block = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<h3 style="margin:0 0 0.6rem;">Oswald <span style="font-family:var(--mono);font-weight:400;font-size:0.82rem;letter-spacing:0.03em;color:var(--verdigris);">&#183; Ochsenwadel &#183; Oxenwald</span></h3>
<p>The German &#8220;Ochsenwadel&#8221; was Americanized to &#8220;Oswald&#8221; within a generation of arrival &#8212; the line runs Samuel Friedrich Ochsenwadel &#8594; Mathias Oswald. This branch rests on trees, not records currently held in the archive.</p>
</section>'''

content = content[:chart_start] + new_chart_block + '\n\n' + spellings_block + between + content[ancestor_start:]
assert content != orig
assert content.count('<svg') == 0, "old svg still present"
assert content.count('oswald-line-pedigree.png') == 3, "image refs not inserted correctly"
assert content.count('Name Spellings in This Line') == 1

open("oswald-line.html", "w", encoding="utf-8").write(content)
print("OK, bytes before:", len(orig), "after:", len(content))

import re

path = "booker-line.html"
content = open(path, encoding="utf-8").read()
orig = content

# --- 1. Replace the old hand-drawn SVG tree-figure section with the real archive pedigree chart ---
start = content.find('<section>\n  <div class="tree-figure">')
end = content.find('</section>', start) + len('</section>')
old_block = content[start:end]
assert old_block.startswith('<section>\n  <div class="tree-figure">')
assert old_block.endswith('</section>')

new_chart_block = '''<section>
  <div class="tree-figure">
    <div class="pedigree-legend">
      <span class="swatch proven"></span> Proven by records &#8212; 9
      <span class="swatch theory"></span> Assumed / strong theory &#8212; 0
      <span class="swatch open"></span> Not yet confirmed &#8212; 4
    </div>
    <a href="images/booker-line-pedigree.png"><img src="images/booker-line-pedigree.png" alt="Booker line pedigree chart: Kenneth Oswald Schmidt at the foot, climbing through Dorcas Booker to William Booker and Dorcas Moore" style="width:100%;height:auto;display:block;border:1px solid var(--paper-line);"></a>
    <div class="tree-cap">K.O. Schmidt stands at the foot; the line climbs to Dorcas Booker &#8212; whose own place in the family is not yet confirmed (shown in red) &#8212; with the Booker, Moore, and Ellingwood ancestry above. A static snapshot, regenerated from the research database whenever it changes. <a href="images/booker-line-pedigree.png" style="color:var(--brass);">View full size &#8595;</a></div>
  </div>
</section>'''

content = content[:start] + new_chart_block + content[end:]
assert content != orig, "chart block replacement made no change"

# --- 2. Insert a Name Spellings section (Booker only) right after the chart section ---
anchor = new_chart_block + '\n\n\n<section>\n<div class="section-title">Ancestor Records</div>'
assert content.count(anchor) == 1, "anchor for spellings insert not found uniquely"

spellings_section = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<div class="sibling-card" style="max-width:62ch;">
<div class="name">Booker <span style="font-weight:400;color:var(--verdigris);font-size:0.85rem;">&#183; Bowker &#183; Bocker &#183; Bucker</span></div>
<p style="margin:0.6rem 0 0;">Largely stable as a surname, with an occasional &#8220;Bowker&#8221; turning up in deed and probate indexes. Two further spellings matter less as family variants than as search traps: the printed federal <em>Census of Pensioners</em> of 1841 (Maine, p.&#160;4, York County) sets the name as &#8220;Bocker&#8221; &#8212; one o, then a c &#8212; which is why a surname search for &#8220;Booker&#8221; misses that page; and the printed <em>Boston Births 1700&#8211;1800</em> (24th Report of the Boston Record Commissioners, 1894, p.&#160;154) records &#8220;Mary daughter of William and Mary Bucker, 24 January 1722,&#8221; indexed by the volume&#8217;s own compilers as &#8220;Bucker.&#8221; Neither is a spelling the family itself used &#8212; but the second is consequential: a search of that 397-page volume for &#8220;Booker&#8221; returns zero hits, while &#8220;Bucker&#8221; returns the family. A Booker search of that particular book is a false negative, not an absence of record.</p>
</div>
</section>

'''

content = content.replace(anchor, spellings_section + anchor)
assert content != orig
assert content.count('Name Spellings in This Line') == 1

# --- 3. Add CSS for the legend swatches ---
css_anchor = '.tree-cap{font-family:var(--mono);font-size:0.72rem;letter-spacing:0.05em;color:var(--verdigris);text-align:center;margin-top:0.8rem;}'
assert content.count(css_anchor) == 1
new_css = css_anchor + '''
  .pedigree-legend{display:flex;flex-wrap:wrap;gap:0.3rem 1.4rem;align-items:center;font-family:var(--mono);font-size:0.72rem;letter-spacing:0.03em;color:var(--verdigris);margin-bottom:1rem;}
  .pedigree-legend .swatch{display:inline-block;width:0.85rem;height:0.85rem;margin-right:0.4rem;vertical-align:-0.12rem;border-radius:2px;}
  .pedigree-legend .swatch.proven{background:var(--paper-dim);border:1.5px solid var(--charcoal);}
  .pedigree-legend .swatch.theory{background:transparent;border:1.5px dashed var(--verdigris);}
  .pedigree-legend .swatch.open{background:#F7E6DF;border:1.5px dashed var(--rust);}
  .tree-cap a{text-decoration:none;}'''
content = content.replace(css_anchor, new_css)
assert content != orig

open(path, "w", encoding="utf-8").write(content)
print("OK, bytes before:", len(orig), "after:", len(content))

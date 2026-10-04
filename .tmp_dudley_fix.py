content = open("dudley-line.html", encoding="utf-8").read()
orig = content

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
</section>

'''

anchor = '''<section>
<div class="section-title">Name Spellings in This Line</div>'''
assert content.count(anchor) == 1, "anchor not found"

content = content.replace(anchor, new_chart_block + anchor)
assert content != orig, "no change made"
assert content.count('dudley-line-pedigree.png') == 3, "img not inserted correctly"
assert content.count('Name Spellings in This Line') == 1

open("dudley-line.html", "w", encoding="utf-8").write(content)
print("OK, bytes before:", len(orig), "after:", len(content))

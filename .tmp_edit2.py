content = open("booker-line.html", encoding="utf-8").read()
orig = content

# --- 1. Name Spellings: strip the boxed card, let it flow as plain text ---
old_spellings = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<div class="sibling-card" style="max-width:62ch;">
<div class="name">Booker <span style="font-weight:400;color:var(--verdigris);font-size:0.85rem;">&#183; Bowker &#183; Bocker &#183; Bucker</span></div>
<p style="margin:0.6rem 0 0;">Largely stable as a surname, with an occasional &#8220;Bowker&#8221; turning up in deed and probate indexes. Two further spellings matter less as family variants than as search traps: the printed federal <em>Census of Pensioners</em> of 1841 (Maine, p.&#160;4, York County) sets the name as &#8220;Bocker&#8221; &#8212; one o, then a c &#8212; which is why a surname search for &#8220;Booker&#8221; misses that page; and the printed <em>Boston Births 1700&#8211;1800</em> (24th Report of the Boston Record Commissioners, 1894, p.&#160;154) records &#8220;Mary daughter of William and Mary Bucker, 24 January 1722,&#8221; indexed by the volume&#8217;s own compilers as &#8220;Bucker.&#8221; Neither is a spelling the family itself used &#8212; but the second is consequential: a search of that 397-page volume for &#8220;Booker&#8221; returns zero hits, while &#8220;Bucker&#8221; returns the family. A Booker search of that particular book is a false negative, not an absence of record.</p>
</div>
</section>'''
assert content.count(old_spellings) == 1, "old spellings block not found"

new_spellings = '''<section>
<div class="section-title">Name Spellings in This Line</div>
<h3 style="margin:0 0 0.6rem;">Booker <span style="font-family:var(--mono);font-weight:400;font-size:0.82rem;letter-spacing:0.03em;color:var(--verdigris);">&#183; Bowker &#183; Bocker &#183; Bucker</span></h3>
<p>Largely stable as a surname, with an occasional &#8220;Bowker&#8221; turning up in deed and probate indexes. Two further spellings matter less as family variants than as search traps: the printed federal <em>Census of Pensioners</em> of 1841 (Maine, p.&#160;4, York County) sets the name as &#8220;Bocker&#8221; &#8212; one o, then a c &#8212; which is why a surname search for &#8220;Booker&#8221; misses that page; and the printed <em>Boston Births 1700&#8211;1800</em> (24th Report of the Boston Record Commissioners, 1894, p.&#160;154) records &#8220;Mary daughter of William and Mary Bucker, 24 January 1722,&#8221; indexed by the volume&#8217;s own compilers as &#8220;Bucker.&#8221; Neither is a spelling the family itself used &#8212; but the second is consequential: a search of that 397-page volume for &#8220;Booker&#8221; returns zero hits, while &#8220;Bucker&#8221; returns the family. A Booker search of that particular book is a false negative, not an absence of record.</p>
</section>'''
content = content.replace(old_spellings, new_spellings)
assert content != orig

# --- 2. Remove the DAR application document placeholder ---
old_frame = '''<div class="frame">
<div class="frame-inner">Document placeholder &#8212; DAR application No. 150069</div>
</div>
'''
# allow for literal em dash char instead of entity, try both
if old_frame not in content:
    old_frame = '''<div class="frame">
<div class="frame-inner">Document placeholder — DAR application No. 150069</div>
</div>
'''
assert content.count(old_frame) == 1, "DAR frame block not found"
content = content.replace(old_frame, '')
assert content != orig

# --- 3. Add Aaron Booker's siblings sibling-grid to rec-001 ---
anchor = '''<p>Confirmed through the 1850 census and a DAR application (Beatrice Wayland Smith/English,
National No. 150069), which traces the Booker line back to Aaron Booker's Revolutionary War
service. This is the earliest confirmed ancestor on Mary's side of the family.</p>
'''
assert content.count(anchor) == 1, "anchor paragraph not found"

siblings_grid = anchor + '''<div class="ships-label">Aaron's Siblings &#8212; Children of William Booker &amp; Dorcas Moore</div>
<div class="sibling-grid">
<div class="sibling-card"><div class="name">Dorcas Booker</div><div class="meta">b. 1741</div></div>
<div class="sibling-card"><div class="name">Abigail Booker</div><div class="meta">b. 1742</div></div>
<div class="sibling-card"><div class="name">William Booker</div><div class="meta">b. 1744</div></div>
<div class="sibling-card"><div class="name">Mercy Booker</div><div class="meta">b. 1745</div></div>
<div class="sibling-card"><div class="name">Mary Booker</div><div class="meta">b. 1747</div></div>
<div class="sibling-card"><div class="name">Lois Booker</div><div class="meta">b. 1750</div></div>
<div class="sibling-card"><div class="name">Olive Booker</div><div class="meta">b. 1752</div></div>
<div class="sibling-card"><div class="name">Nehemiah Booker</div><div class="meta">b. 1755</div></div>
</div>
<p style="margin-top:0.8rem;">Named in the family pedigree database alongside Aaron; none of the eight has yet been individually source-verified beyond this listing. The eldest, another Dorcas Booker, is an aunt of our own Dorcas Booker (below) &#8212; not to be confused with her. Dorcas's own siblings, if any, are not yet on file.</p>
'''
content = content.replace(anchor, siblings_grid)
assert content != orig
assert content.count("Aaron's Siblings") == 1

# --- 4. Light accuracy fix: the Open Questions item about "eight siblings... none built into this page yet" is now stale ---
old_oq = '''<span class="label">One More Generation on File</span>
<p>The database already carries Aaron Booker's own parents &#8212; William Booker (1717&#8211;1763) and Dorcas Moore (1720&#8211;1760), both tier "confirmed" &#8212; plus a list of eight siblings for Aaron himself. None of that is built into this page yet.</p>'''
assert content.count(old_oq) == 1
new_oq = '''<span class="label">One More Generation on File</span>
<p>The database already carries Aaron Booker's own parents &#8212; William Booker (1717&#8211;1763) and Dorcas Moore (1720&#8211;1760), both tier "confirmed." Aaron's eight siblings are now listed above; William and Dorcas Moore themselves don't yet have their own page.</p>'''
content = content.replace(old_oq, new_oq)
assert content != orig

open("booker-line.html", "w", encoding="utf-8").write(content)
print("OK, bytes before:", len(orig), "after:", len(content))

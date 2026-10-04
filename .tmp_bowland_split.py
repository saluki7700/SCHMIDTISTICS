from html.parser import HTMLParser

fname = "bowland-line.html"
content = open(fname, encoding="utf-8").read()
orig = content

old_viewbox = 'viewBox="0 0 940 436"'
new_viewbox = 'viewBox="0 0 1180 436"'
assert content.count(old_viewbox) == 1
content = content.replace(old_viewbox, new_viewbox)

old_block = (
    '<rect class="cin" x="520" y="180" width="360" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="207">William A. Bowland <tspan class="amp">&#38;</tspan> Mary F. Porter</text>'
    '<text class="mt" x="538" y="229">1853&#8211;1911 &#183; 1860&#8211;1926 &#183; TIFFIN, OH</text>'
    '<path class="mr" d="M700.0 330 L700.0 244"/>'
    '<rect class="cin" x="520" y="30" width="360" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="57">Ephraim W. Boland <tspan class="amp">&#38;</tspan> Elizabeth Soaper</text>'
    '<text class="mt" x="538" y="79">SENECA COUNTY, OHIO</text>'
    '<path class="mr" d="M700.0 180 L700.0 94"/>'
)
assert content.count(old_block) == 1, "old_block not found exactly once"

new_block = (
    '<rect class="cin" x="520" y="180" width="300" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="203">William A. Bowland</text>'
    '<text class="mt" x="538" y="225">1853&#8211;1911</text>'
    '<rect class="cin" x="860" y="180" width="300" height="64" rx="6"/>'
    '<text class="nmi" x="878" y="203">Mary F. Porter</text>'
    '<text class="mt" x="878" y="225">1860&#8211;1926</text>'
    '<path class="sp" d="M820 212 L860 212"/>'
    '<text class="ml" x="840" y="204" text-anchor="middle">m.</text>'
    '<text class="mt" x="840" y="264" text-anchor="middle">TIFFIN, OH</text>'
    '<path class="mr" d="M600 330 L600 272"/>'
    '<rect class="cin" x="520" y="30" width="300" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="53">Ephraim W. Boland</text>'
    '<rect class="cin" x="860" y="30" width="300" height="64" rx="6"/>'
    '<text class="nmi" x="878" y="53">Elizabeth Soaper</text>'
    '<path class="sp" d="M820 62 L860 62"/>'
    '<text class="ml" x="840" y="54" text-anchor="middle">m.</text>'
    '<text class="mt" x="840" y="114" text-anchor="middle">SENECA COUNTY, OHIO</text>'
    '<path class="mr" d="M600 180 L600 122"/>'
)
content = content.replace(old_block, new_block)

old_footnote = '<text class="fnt" x="470" y="426" text-anchor="middle">The Bowland line joins through Kenneth&#8217;s wife, Nellie.</text>'
new_footnote = '<text class="fnt" x="590" y="426" text-anchor="middle">The Bowland line joins through Kenneth&#8217;s wife, Nellie.</text>'
assert content.count(old_footnote) == 1
content = content.replace(old_footnote, new_footnote)

# validation
assert "&amp;</tspan> Mary F. Porter" not in content
assert "William A. Bowland <tspan" not in content
assert content.count("William A. Bowland") == 1
assert content.count("Mary F. Porter") == 1
assert content.count("Ephraim W. Boland") == 1
assert content.count("Elizabeth Soaper") == 1
assert content.count('viewBox="0 0 1180 436"') == 1

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
print(f"{fname}: {len(orig)} -> {len(content)} bytes")

from html.parser import HTMLParser

fname = "seitzberg-line.html"
content = open(fname, encoding="utf-8").read()
orig = content

old_viewbox = 'viewBox="0 0 940 348"'
new_viewbox = 'viewBox="0 0 1180 348"'
assert content.count(old_viewbox) == 1
content = content.replace(old_viewbox, new_viewbox)

old_label = '<text class="fnt" x="700" y="32" text-anchor="middle">&#8593; Seitzberg line to Hamburg</text>'
new_label = '<text class="fnt" x="840" y="32" text-anchor="middle">&#8593; Seitzberg line to Hamburg</text>'
assert content.count(old_label) == 1
content = content.replace(old_label, new_label)

old_block = (
    '<rect class="cin" x="520" y="40" width="360" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="67">Floyd H. Seitzberg <tspan class="amp">&#38;</tspan> Elnora Englemann</text>'
    '<text class="mt" x="538" y="89">1898&#8211;1967 &#183; 1896&#8211;1990 &#183; ILLINOIS</text>'
    '<rect class="cin" x="520" y="220" width="360" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="247">Marylyn J. Seitzberg</text>'
    '<text class="mt" x="538" y="269">1926&#8211;2011 &#183; SAVANNA, IL</text>'
    '<path class="mr" d="M700 104 L700 220"/>'
)
assert content.count(old_block) == 1, "old_block not found exactly once"

new_block = (
    '<rect class="cin" x="520" y="40" width="300" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="63">Floyd H. Seitzberg</text>'
    '<text class="mt" x="538" y="85">1898&#8211;1967</text>'
    '<rect class="cin" x="860" y="40" width="300" height="64" rx="6"/>'
    '<text class="nmi" x="878" y="63">Elnora Englemann</text>'
    '<text class="mt" x="878" y="85">1896&#8211;1990</text>'
    '<path class="sp" d="M820 72 L860 72"/>'
    '<text class="ml" x="840" y="64" text-anchor="middle">m.</text>'
    '<text class="mt" x="840" y="118" text-anchor="middle">ILLINOIS</text>'
    '<rect class="cin" x="520" y="220" width="360" height="64" rx="6"/>'
    '<text class="nmi" x="538" y="247">Marylyn J. Seitzberg</text>'
    '<text class="mt" x="538" y="269">1926&#8211;2011 &#183; SAVANNA, IL</text>'
    '<path class="mr" d="M600 220 L600 126"/>'
)
content = content.replace(old_block, new_block)

# validation
assert "Floyd H. Seitzberg <tspan" not in content
assert content.count("Floyd H. Seitzberg") >= 1
assert content.count("Elnora Englemann") >= 1
assert content.count('viewBox="0 0 1180 348"') == 1

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

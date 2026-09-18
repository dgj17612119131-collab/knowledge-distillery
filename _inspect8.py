# -*- coding: utf-8 -*-
"""Full dump of mao pano + disc, and fp card 10 fbox area."""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def match_div_end(content, open_end):
    depth = 1
    i = open_end
    n = len(content)
    while i < n and depth > 0:
        nxt = content.find("<", i)
        if nxt == -1:
            break
        if content.startswith("<div", nxt):
            depth += 1
            i = nxt + 4
        elif content.startswith("</div>", nxt):
            depth -= 1
            if depth == 0:
                return content[open_end:nxt], nxt + 6
            i = nxt + 6
        else:
            i = nxt + 1
    return content[open_end:], n

def extract_div(doc, cls):
    m = re.search(r'<div class="%s">' % cls, doc)
    if not m:
        return ""
    inner, _ = match_div_end(doc, m.end())
    return inner

doc = open('mao.html', encoding='utf-8').read()
print('[mao disc full]')
print(extract_div(doc, 'disc'))
print()
pano = extract_div(doc, 'pano')
print('[mao pano] non-pl text check')
# show all h2/p outside pc
for m in re.finditer(r'<h2[^>]*>(.*?)</h2>|<p[^>]*>(.*?)</p>', pano, re.S):
    print('PARA:', repr(m.group(0)[:200]))
print('pc count:', pano.count('class="pc"'))
print('pl links:', pano.count('class="pl"'))
print('[mao pano tail]')
print(pano[-700:])

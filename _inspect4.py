# -*- coding: utf-8 -*-
"""Dump mao.html mx-sec and idx-sec content."""
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

with open('mao.html', encoding='utf-8') as f:
    doc = f.read()

mx = extract_div(doc, 'mx-sec')
print('[mx-sec] len', len(mx))
print(mx[:2500])
print()
print('...TAIL...')
print(mx[-1200:])
print()
idx = extract_div(doc, 'idx-sec')
print('[idx-sec] len', len(idx))
print(idx[:2000])
print()
print('...TAIL...')
print(idx[-800:])

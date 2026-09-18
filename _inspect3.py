# -*- coding: utf-8 -*-
"""Dump book-level sections of mao.html and fp.html for overview rendering."""
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

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 70)
    print('FILE', fn)
    for cls in ['hero', 'ov', 'tens-sec', 'pano', 'disc', 'mx-sec', 'idx-sec', 'frow', 'fb']:
        inner = extract_div(doc, cls)
        print('-' * 40)
        print(f'[{cls}] len={len(inner)}')
        print(inner[:1800])

# -*- coding: utf-8 -*-
"""Inspect structure of mao.html and fp.html."""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        html = f.read()
    out = []
    out.append('=' * 60)
    out.append(fn + ' len=' + str(len(html)))
    cards = re.findall(r'<div class="card" id="card-(\d+)"', html)
    out.append('card ids: ' + str(cards))
    m = re.search(r'<div class="card" id="card-1".*?(?=<div class="card" id="card-2")', html, re.S)
    if m:
        out.append(m.group(0)[:5000])
    else:
        out.append('NO CARD-1 MATCH')
    # book header area before first card
    idx = html.find('<div class="card"')
    out.append('--- HEAD BEFORE FIRST CARD ---')
    out.append(html[max(0, idx-3000):idx])
    print('\n'.join(out))

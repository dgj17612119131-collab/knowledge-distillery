# -*- coding: utf-8 -*-
"""Inspect mao.html / fp.html: separators, overview sections, section types, block types."""
import re, sys, io, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 70)
    print(fn, 'len', len(doc))
    print('card markers:', re.findall(r'<!-- CARD (\d+) -->', doc))
    print('card ids:', re.findall(r'<div class="card" id="card-(\d+)"', doc))
    # overview containers
    for cls in ['hero', 'ov', 'tens-sec', 'pano', 'disc', 'solv', 'search']:
        print(f'container div.{cls}:', doc.count(f'class="{cls}"'))
    # section titles
    sts = re.findall(r'<div class="st">(.*?)</div>', doc)
    print('section titles:', collections.Counter(sts))
    # block classes inside cards
    block_cls = re.findall(r'<div class="([a-z0-9-]+)">', doc)
    print('div classes:', collections.Counter(block_cls))
    ul_cls = re.findall(r'<ul class="([a-z0-9-]+)">', doc)
    print('ul classes:', collections.Counter(ul_cls))
    print('h3 count:', doc.count('<h3'), ' h4 count:', doc.count('<h4'), ' table count:', doc.count('<table'))
    print('img count:', doc.count('<img'), ' svg count:', doc.count('<svg'))
    print('href values:', collections.Counter(re.findall(r'href="([^"]+)"', doc)).most_common(12))

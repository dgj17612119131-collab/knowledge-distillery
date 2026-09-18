# -*- coding: utf-8 -*-
"""Check whether '<!--' comments appear inside card bodies."""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 60)
    print(fn)
    # positions of card starts and next-card markers
    card_starts = [m.start() for m in re.finditer(r'<div class="card" id="card-', doc)]
    comment_positions = [m.start() for m in re.finditer(r'<!--', doc)]
    for cs in card_starts:
        inside = [cp - cs for cp in comment_positions if cs < cp < cs + 60000]
        # determine the card's end: next card start or end of cards section
        nxt = [x for x in card_starts if x > cs]
        end = nxt[0] if nxt else len(doc)
        inside = [cp - cs for cp in comment_positions if cs < cp < end]
        print(f'  card at {cs}: comments inside card region: {inside}')

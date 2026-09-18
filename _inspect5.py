# -*- coding: utf-8 -*-
"""Check what follows the last card in mao.html / fp.html."""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 60)
    print(fn)
    # find last </div></div> closing of card N, show 1200 chars after
    last_card_start = doc.rfind('<div class="card"')
    last_card_end = doc.rfind('</div>', last_card_start)
    # better: find '<!--' after last card start
    m = re.search(r'<!--', doc[last_card_start:])
    print('first comment after last card start:', repr(m.group(0)) if m else None)
    tail = doc[last_card_end - 400: last_card_end + 900]
    print(tail)

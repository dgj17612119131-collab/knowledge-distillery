# -*- coding: utf-8 -*-
"""Find exact end of last card and what follows immediately."""
import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 60)
    print(fn)
    last_card_start = doc.rfind('<div class="card"')
    # find all '<!--' positions after last card start
    comments = [m.start() for m in re.finditer(r'<!--', doc[last_card_start:])]
    print('comment offsets after last card start:', comments)
    # locate the end of last card: sequence "</div>\n</div>" after last section end
    # heuristic: find the last '<!-- CARD' marker and take 600 chars from there
    mk = doc.rfind('<!-- CARD')
    print('last CARD marker at', mk)
    print(repr(doc[mk:mk+600]))

# -*- coding: utf-8 -*-
"""Scan children of container blocks (fbox/deep/cases/bnd/flow/sg/ot) in mao.html & fp.html."""
import re, sys, io, collections

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

CONTAINERS = ['fbox', 'deep', 'cases', 'bnd', 'flow', 'sg', 'ot', 'cr']

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 60)
    print(fn)
    child_types = collections.Counter()
    # iterate over all container openings in doc order
    pattern = re.compile(r'<div class="(%s)">' % '|'.join(CONTAINERS))
    for m in pattern.finditer(doc):
        cls = m.group(1)
        inner, _ = match_div_end(doc, m.end())
        # classify direct children
        for cm in re.finditer(r'<(div|p|h4|h3|ul|a|span|b|strong|br)[^>]*>', inner):
            tag = cm.group(1)
            # only count tags that start a child (rough: ignore known nested like div class=fs2 handled)
            child_types[(cls, tag)] += 1
    for (cls, tag), cnt in sorted(child_types.items()):
        print(f'  {cls}: {tag} x{cnt}')

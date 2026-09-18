# -*- coding: utf-8 -*-
"""扫描每个容器的直接子元素（标签+class），找出转换器未处理的类型。"""
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

CONTAINERS = ['fbox', 'deep', 'cases', 'bnd', 'flow', 'sg', 'ot', 'cr', 's']

for fn in ['mao.html', 'fp.html']:
    with open(fn, encoding='utf-8') as f:
        doc = f.read()
    print('=' * 60)
    print(fn)
    combo = collections.Counter()
    pattern = re.compile(r'<div class="(%s)">' % '|'.join(CONTAINERS))
    for m in pattern.finditer(doc):
        cls = m.group(1)
        inner, _ = match_div_end(doc, m.end())
        # find direct children: walk tokens at depth 1
        depth = 1
        i = 0
        n = len(inner)
        while i < n:
            nxt = inner.find("<", i)
            if nxt == -1:
                break
            if inner.startswith("<!--", nxt):
                i = nxt + 4
                continue
            if inner.startswith("</div>", nxt):
                depth -= 1
                i = nxt + 6
                continue
            mm = re.match(r'<(\w+)([^>]*)>', inner[nxt:])
            if mm:
                tag = mm.group(1)
                attrs = mm.group(2)
                if depth == 1:
                    cm = re.search(r'class="([^"]*)"', attrs)
                    combo[(cls, tag, cm.group(1) if cm else '')] += 1
                if tag == 'div' and not attrs.rstrip().endswith('/'):
                    depth += 1
                i = nxt + mm.end()
            else:
                i = nxt + 1
    for (cls, tag, c), cnt in sorted(combo.items()):
        print(f'  {cls}: <{tag} class="{c}"> x{cnt}')

# Checks that every local link, image, script and frame on the given pages points at a file that exists.
# python linkcheck.py <site-root> <page> [<page> ...]
import re, os, sys
root = sys.argv[1]
bad = 0
for page in sys.argv[2:]:
    s = open(os.path.join(root, page), encoding='utf8').read()
    base = os.path.dirname(page)
    refs = set(re.findall(r'(?:href|src|data-src|data-href|poster)="([^"#?]+)', s))
    for r in sorted(refs):
        if re.match(r'^(https?:|mailto:|tel:|data:|//|javascript:)', r) or '${' in r or "'" in r or '+' in r:
            continue
        t = os.path.normpath(os.path.join(root, r.lstrip('/')) if r.startswith('/') else os.path.join(root, base, r))
        if os.path.isdir(t):
            t = os.path.join(t, 'index.html')
        if not os.path.exists(t):
            bad += 1
            print('MISSING', page, '->', r)
print('checked', len(sys.argv) - 2, 'pages,', bad, 'missing')

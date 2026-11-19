# one-off: converts build_index.py from "standalone /worlds/ page" to "site front door at /"
L = open('_src/build_index.py', encoding='utf8').read().split('\n')
s = '\n'.join(L)


def rep(a, b):
    global s
    assert s.count(a) == 1, (a, s.count(a))
    s = s.replace(a, b)


rep("s = open('index.html', encoding='utf8').read()\na = s.index('<style>')\nb = s.index('<script>')\njs = s[b:]",
    "js = '<script>\\n' + open('_src/index.js', encoding='utf8').read() + '</script>\\n'\n"
    "below = open('_src/below.html', encoding='utf8').read()")
rep("css = open('_src/index.css', encoding='utf8').read()",
    "css = open('_src/index.css', encoding='utf8').read() + open('_src/below.css', encoding='utf8').read()")
rep('<header class="bar"><a class="logo" href="./">',
    '<div class="door" id="door">\n<header class="bar"><a class="logo" href="/">')
rep('<a class="opt far" href="/home.html#proof">Proof</a><a class="opt far" href="/home.html#pricing">Pricing</a><a class="opt" href="/home.html#about">Meet Bryan</a>',
    '<a class="opt far" href="#how">How it works</a><a class="opt far" href="#proof">Proof</a><a class="opt far" href="/home.html#pricing">Pricing</a><a class="opt" href="#bryan">Meet Bryan</a>')
rep('<iframe src="%s" scrolling', '<iframe src="/worlds/%s" scrolling')
i = s.index('<div class="more"><p>You do the work')
j = s.index('<noscript>')
s = s[:i] + '</div>\n' + s[j:]
rep(".row,.foot{display:none}.more{display:block}",
    ".door{display:none}.nolist a{display:block;padding:10px 20px;color:#FF6A2A}")
rep('<div class="more">\'\'\'', '<div class="nolist">\'\'\'')
k = s.index("open('index.html', 'w'")
s = s[:k] + ("open('../index.html', 'w', encoding='utf8', newline='\\n').write("
             "head + css + '</style>\\n' + h + js + below + '</body></html>\\n')\n"
             "print('ok', len(head + css + h + js + below))\n")
rep('<meta name="robots" content="noindex">\n<title>',
    '<meta name="robots" content="noindex">\n<link rel="canonical" href="https://perseidechocreations.com/">\n<title>')
open('_src/build_index.py', 'w', encoding='utf8', newline='\n').write(s)
print('patched')

#!/bin/bash
# verify-build.sh — build + verify the dashboard before pushing.
# Run from ~/workspace/projects/buddy-tree after every build.py change.
set -e
cd "$(dirname "$0")"

echo "== build =="
python3 build.py

echo "== extract main script block (last <script>..</script>) =="
python3 - <<'PYEOF'
import re, sys
html = open('index.html', encoding='utf-8').read()
m = re.search(r'<style>(.*?)</style>', html, re.S)
if not m:
    sys.exit("no <style> block found")
start = html.rfind('<script>')
if start < 0:
    sys.exit("no <script> block found")
start += len('<script>')
end = html.rfind('</script>')
if end <= start:
    sys.exit("no closing </script> found")
open('/tmp/verify-main.js', 'w', encoding='utf-8').write(html[start:end])
print("main script bytes:", end - start)
PYEOF

echo "== node syntax check (full main script) =="
node --check /tmp/verify-main.js && echo "JS syntax OK"

echo "== literal-newline-in-JS-string scan =="
python3 - <<'PYEOF'
import re
js = open('/tmp/verify-main.js', encoding='utf-8').read()
# A real newline inside a single/double-quoted JS string is a syntax error.
# Walk the source tracking string state (rough but effective).
bad = 0
i, n = 0, len(js)
while i < n:
    c = js[i]
    if c in "'\"":
        q = c
        i += 1
        while i < n:
            d = js[i]
            if d == '\\':
                i += 2
                continue
            if d == '\n':
                bad += 1
                print("literal newline in string near:", repr(js[max(0,i-60):i+10][:70]))
                break
            if d == q:
                break
            i += 1
    elif c == '/' and i + 1 < n and js[i+1] == '/':
        while i < n and js[i] != '\n':
            i += 1
        continue
    elif c == '/' and i + 1 < n and js[i+1] == '*':
        i += 2
        while i + 1 < n and not (js[i] == '*' and js[i+1] == '/'):
            i += 1
        i += 2
        continue
    elif c == '/':
        # Could be a regex literal (/.../flags) or division. Try regex skip:
        # advance past \x escapes and [...] classes to an unescaped / on this line.
        j = i + 1
        in_class = False
        ok = False
        while j < n and js[j] != '\n':
            d = js[j]
            if d == '\\':
                j += 2
                continue
            if d == '[':
                in_class = True
            elif d == ']':
                in_class = False
            elif d == '/' and not in_class:
                ok = True
                break
            j += 1
        if ok:
            j += 1
            while j < n and js[j].isalpha():
                j += 1  # flags
            i = j
            continue
        # not a regex — division; just step over
        i += 1
        continue
    elif c == '`':
        # template literal: newlines are legal; skip to closing backtick
        i += 1
        while i < n:
            d = js[i]
            if d == '\\':
                i += 2
                continue
            if d == '`':
                break
            i += 1
    # NB: backslash is only an escape INSIDE strings; outside, just step over it
    i += 1
print("bad strings:", bad)
raise SystemExit(1 if bad else 0)
PYEOF
echo "no broken strings"

echo "== ALL CHECKS PASSED =="

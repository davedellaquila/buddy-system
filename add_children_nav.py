#!/usr/bin/env python3
"""Add a children nav row to every buddy homepage, next to the parent crumb.

Dave 2026-10-15: "all of the web pages should list their children along with
their parent. i may want to jump to one of the children."

- Children computed with the multi-parent model (parents[] + legacy parent).
- Inserts <nav data-buddy-kids> right after the existing <nav data-buddy-crumb>.
- Idempotent: replaces the kids nav if already present.
- Same styling language as the parent crumb; absolute URLs like the crumb.
"""
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://davedellaquila.github.io/buddy-system/'
CRUMB_STYLE = ("padding:14px 20px 0;font-family:-apple-system,BlinkMacSystemFont,"
               "'Segoe UI',sans-serif;font-size:14px;line-height:1.4;")
KIDS_STYLE = ("padding:6px 20px 0;font-family:-apple-system,BlinkMacSystemFont,"
              "'Segoe UI',sans-serif;font-size:14px;line-height:1.9;")
LINK_STYLE = "color:inherit;text-decoration:none;margin-right:14px;white-space:nowrap;"


def eff_parents(b, by_id):
    ps = list(b.get('parents') or [])
    if b.get('parent') and b['parent'] not in ps:
        ps.append(b['parent'])
    return [p for p in ps if p in by_id]


def family_nav_html(b, by_id, kids):
    parts = []
    parents = eff_parents(b, by_id)
    if parents:
        links = ' · '.join(
            '<a href="%s%s/" style="color:inherit;opacity:.65;text-decoration:none;">← %s</a>'
            % (BASE, p, html.escape(by_id[p].get('name', p)))
            for p in parents)
        parts.append('<nav data-buddy-crumb style="%s">%s</nav>' % (CRUMB_STYLE, links))
    elif b['id'] != 'astro':
        parts.append('<nav data-buddy-crumb style="%s">'
                     '<a href="%sastro/" style="color:inherit;opacity:.65;text-decoration:none;">← Astro</a>'
                     '</nav>' % (CRUMB_STYLE, BASE))
    if kids:
        links = []
        for k in kids:
            kid_url = BASE + k['id'] + '/'
            hp = k.get('homepage')
            if hp and hp.startswith('http'):
                kid_url = hp
            label = '%s %s' % (k.get('icon', ''), k.get('name', k['id']))
            links.append(
                '<a href="%s" style="%s">%s</a>' % (
                    html.escape(kid_url, quote=True), LINK_STYLE,
                    html.escape(label)))
        parts.append(
            '<nav data-buddy-kids style="%s">'
            '<span style="opacity:.65;">Children:</span> %s</nav>'
            % (KIDS_STYLE, ' '.join(links)))
    return '\n'.join(parts)


def main():
    d = json.load(open(os.path.join(HERE, 'buddies.json')))
    buddies = d['buddies'] if isinstance(d, dict) else d
    by_id = {b['id']: b for b in buddies}

    kids_of = {}
    for b in buddies:
        for p in eff_parents(b, by_id):
            kids_of.setdefault(p, []).append(b)
    for k in kids_of:
        kids_of[k].sort(key=lambda x: x.get('name', ''))

    updated = 0
    for b in buddies:
        bid = b['id']
        idx = os.path.join(HERE, bid, 'index.html')
        if not os.path.exists(idx):
            continue
        kids = kids_of.get(bid, [])
        with open(idx) as f:
            content = f.read()

        nav_html = family_nav_html(b, by_id, kids)

        # Remove any existing crumb/kids nav (idempotent re-run)
        content = re.sub(r'<nav data-buddy-crumb[^>]*>.*?</nav>\n?', '', content,
                         flags=re.S)
        content = re.sub(r'<nav data-buddy-kids[^>]*>.*?</nav>\n?', '', content,
                         flags=re.S)

        # Insert after <body>
        if nav_html:
            m2 = re.search(r'<body[^>]*>', content)
            if m2:
                content = (content[:m2.end()] + '\n' + nav_html +
                           content[m2.end():])
                updated += 1

        with open(idx, 'w') as f:
            f.write(content)

    print(f'Updated {updated} homepages with family nav')


if __name__ == '__main__':
    main()

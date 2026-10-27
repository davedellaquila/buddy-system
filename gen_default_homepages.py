#!/usr/bin/env python3
"""Default Homepage v3 — "The Dossier".

Redesign of the default buddy homepage (Dave's mission, 2026-10-14):
instead of a pretty-but-thin template, the default page walks the object's
entire data chain and shows everything the system knows about it.

Usage: python3 gen_default_homepages.py <buddy-id> [<buddy-id> ...]
Writes <bid>/index.html (v3). Old page is backed up to the archive folder.

Data chain per buddy:
  registry (buddies.json) -> computed tree (parent chain, siblings, children,
    reverse links) -> plans.json -> docs[] -> repo (ingest.md, pinned.json) ->
    memory/people|groups -> side thread (chat) -> brain-dump box

v3.1 (2026-10-20, Dave): --about writes <bid>/about.html — the default page
served as the buddy's About page, linked from its custom homepage. Every
default/About page also carries the COMPLETE registry record and EVERY
buddy-specific markdown file from the buddy's own git repo (local clone
under ~/workspace/projects/<repo>), rendered in full.

v3.2 (2026-10-20): repo contents are NOT baked into the public page after
all — the section lists the files and embeds the live, token-gated Repo
files reader (gen_basic's FILES_* widget, shipped on template homepages
the same day), so private repo markdown is read from GitHub on Dave's
devices and never published raw.
"""
import json, os, re, sys, html, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

# --- Reuse the v2 brain-dump box (token flow, ingest.md write path) ---------
def _extract_consts():
    src = open(os.path.join(HERE, 'gen_basic_homepages.py')).read()
    out = {}
    for name in ['DUMPBOX_CSS', 'DUMPBOX_HTML', 'DUMPBOX_JS', 'ATTN_JS', 'FILES_CSS', 'FILES_HTML', 'FILES_JS']:
        m = re.search(r'^' + name + r' = """(.*?)"""\s*$', src, re.S | re.M)
        if not m:
            raise RuntimeError('could not extract ' + name)
        out[name] = m.group(1)
    return out
_C = _extract_consts()

def esc(s):
    return html.escape(str(s), quote=True)

# --- Markdown from the buddy's own repo (v3.1; live reader since v3.2) -------
_REPO_ORDER = ['KNOWLEDGE.md', 'CONFIG.md', 'STUDY.md', 'SOUL.md', 'DECISIONS.md',
               'ACCOMPLISHMENTS.md', 'README.md']

def repo_clone_dir(b):
    """Local clone of the buddy's own git repo, if one exists here."""
    cands = []
    if b.get('repo'):
        cands.append(os.path.expanduser('~/workspace/projects/' + b['repo']))
    cands.append(os.path.expanduser('~/workspace/projects/' + b['id']))
    for c in cands:
        if os.path.isdir(c) and glob.glob(os.path.join(c, '*.md')):
            return c
    return None

def _md_files_in(root, sub=''):
    d = os.path.join(root, sub) if sub else root
    out = []
    for f in sorted(glob.glob(os.path.join(d, '*.md'))):
        rel = os.path.join(sub, os.path.basename(f)) if sub else os.path.basename(f)
        out.append((rel, f))
    return out

def repo_markdown_section(b):
    """The buddy's repo markdown, on the page (Dave 2026-10-20): a baked
    inventory of what the local clone holds, plus the live Repo files reader
    (the same widget the template homepages use) which loads the actual
    files from GitHub with Dave's token — always current, never published
    raw to this public page."""
    files = []
    clone = repo_clone_dir(b)
    if clone:
        root_files = _md_files_in(clone)
        root_files.sort(key=lambda rf: (_REPO_ORDER.index(rf[0]) if rf[0] in _REPO_ORDER else 99, rf[0]))
        files = root_files + _md_files_in(clone, 'docs')
    tree_files = _md_files_in(os.path.join(HERE, b['id'])) + _md_files_in(os.path.join(HERE, b['id']), 'docs')
    parts = []
    if files:
        items = []
        for rel, path in files:
            try:
                n = len(open(path, encoding='utf-8', errors='replace').read())
            except Exception:
                n = 0
            items.append('<li><code>%s</code> <span class="muted">%s chars</span></li>' % (esc(rel), format(n, ',')))
        parts.append('<p class="muted">In the local clone of davedellaquila/%s — the reader below '
                     'loads the live files from the repo itself:</p><ul class="mdinv">%s</ul>'
                     % (esc(b.get('repo') or b['id']), ''.join(items)))
    if tree_files:
        items = ''.join('<li><code>%s</code></li>' % esc(rel) for rel, _ in tree_files)
        parts.append('<p class="muted">Also kept in the dashboard folder %s/:</p>'
                     '<ul class="mdinv">%s</ul>' % (esc(b['id']), items))
    if not files and not tree_files:
        parts.append('<p class="empty">No local clone of this buddy\'s repo is kept here yet — '
                     'the reader below still loads the live files from GitHub once a token '
                     'is connected.</p>')
    parts.append(_C['FILES_HTML'].replace('__BID__', esc(b['id'])).replace('__BNAME__', esc(b.get('name', b['id']))))
    return section('From the repo — markdown files (%d)' % len(files), ''.join(parts))

# --- Complete registry record (v3.1) -----------------------------------------
_RECORD_ORDER = ['id', 'name', 'icon', 'tagline', 'type', 'kind', 'status', 'statusClass',
                 'parent', 'parents', 'mission', 'brief', 'persona', 'voice', 'repo',
                 'homepage', 'homepageSource', 'chat', 'docs', 'attention', 'links',
                 'aka', 'tags', 'photos', 'alt_personas', 'setup_pending']

def _rec_val(v):
    if v is None or v == '' or v == [] or v == {}:
        return '<span class="unset">— not set —</span>'
    if isinstance(v, bool):
        return 'yes' if v else 'no'
    if isinstance(v, (int, float)):
        return esc(v)
    if isinstance(v, str):
        if v.startswith('http://') or v.startswith('https://'):
            return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(v), esc(v))
        return esc(v)
    if isinstance(v, list):
        items = []
        for it in v:
            if isinstance(it, dict):
                label = it.get('label') or it.get('text') or it.get('title') or it.get('name') or ''
                url = it.get('url') or ''
                if url:
                    items.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(url), esc(label or url)))
                elif label:
                    items.append(esc(label))
                else:
                    items.append('<code>%s</code>' % esc(json.dumps(it, ensure_ascii=False)))
            else:
                items.append(esc(it))
        return '<br>'.join(items) if items else '<span class="unset">— not set —</span>'
    return '<pre class="recjson">%s</pre>' % esc(json.dumps(v, indent=1, ensure_ascii=False))

def record_section(b):
    keys = [k for k in _RECORD_ORDER if k in b] + sorted(k for k in b if k not in _RECORD_ORDER)
    rows = ''.join('<div class="fact"><dt>%s</dt><dd>%s</dd></div>' % (esc(k), _rec_val(b.get(k))) for k in keys)
    return section('Complete registry record (%d fields)' % len(keys),
                   '<dl class="facts">' + rows + '</dl>')


def load():
    d = json.load(open(os.path.join(HERE, 'buddies.json')))
    buddies = {b['id']: b for b in d['buddies']}
    plans = json.load(open(os.path.join(HERE, 'plans.json')))['plans']
    return buddies, plans

def parent_chain(buddies, b):
    chain = []
    seen = set()
    cur = b
    while cur.get('parent') and cur['parent'] not in seen:
        seen.add(cur['parent'])
        p = buddies.get(cur['parent'])
        if not p:
            break
        chain.append(p)
        cur = p
    return chain

# Multi-parent helpers (Dave 2026-10-15)
BASE_URL = 'https://davedellaquila.github.io/buddy-system/'

def eff_parents(buddies, b):
    ps = list(b.get('parents') or [])
    if b.get('parent') and b['parent'] not in ps:
        ps.append(b['parent'])
    return [p for p in ps if p in buddies]

def family_nav(buddies, b):
    """Parent crumb + children nav HTML for the top of a buddy homepage."""
    bid = b['id']
    parts = []
    parents = eff_parents(buddies, b)
    if parents:
        links = ' · '.join(
            '<a href="%s%s/" style="color:var(--muted);text-decoration:none;">← %s</a>'
            % (BASE_URL, p, esc(buddies[p].get('name', p)))
            for p in parents)
        parts.append('<nav data-buddy-crumb style="margin-bottom:14px;font-size:14px;">%s</nav>' % links)
    elif bid != 'astro':
        parts.append('<nav data-buddy-crumb style="margin-bottom:14px;font-size:14px;">'
                     '<a href="%sastro/" style="color:var(--muted);text-decoration:none;">← Astro</a></nav>' % BASE_URL)
    kids = sorted(
        (x for x in buddies.values() if bid in eff_parents(buddies, x)),
        key=lambda x: x.get('name', ''))
    if kids:
        links = ' '.join(
            '<a href="%s%s/" style="margin-right:14px;white-space:nowrap;">%s %s</a>'
            % (BASE_URL, k['id'], esc(k.get('icon', '')), esc(k.get('name', k['id'])))
            for k in kids)
        parts.append('<nav data-buddy-kids style="margin-bottom:18px;font-size:14px;line-height:1.9;">'
                     '<span style="color:var(--muted);">Children:</span> %s</nav>' % links)
    return ''.join(parts)

def memory_files(b):
    """Memory pages whose filename matches the buddy id or name slug."""
    hits = []
    bid = b['id']
    slug = re.sub(r'[^a-z0-9]+', '-', b.get('name', '').lower()).strip('-')
    for pat in [os.path.expanduser('~/memory/people/*.md'),
                os.path.expanduser('~/memory/groups/*.md')]:
        for f in glob.glob(pat):
            base = os.path.basename(f)[:-3].lower()
            if base == bid.lower() or base == slug or bid.lower() in base or base in bid.lower():
                hits.append(f)
    return hits

def buddy_link(buddies, bid):
    b = buddies.get(bid)
    if not b:
        return esc(bid)
    hp = b.get('homepage') or (bid + '/')
    return '<a href="../%s">%s %s</a>' % (esc(hp), esc(b.get('icon', '')), esc(b.get('name', bid)))

def section(kicker, inner):
    if not inner:
        return ''
    return '<section class="card"><h2 class="kicker">%s</h2>%s</section>' % (esc(kicker), inner)

def build_page(buddies, plans, b, about=False):
    bid = b['id']
    name = b.get('name', bid)
    icon = b.get('icon', '🤖')
    chain = parent_chain(buddies, b)
    kids = sorted([x for x in buddies.values() if bid in eff_parents(buddies, x)],
                  key=lambda x: x.get('name', ''))
    sibs = sorted([x for x in buddies.values()
                   if x['id'] != bid and
                   set(eff_parents(buddies, x)) & set(eff_parents(buddies, b))],
                  key=lambda x: x.get('name', ''))
    fwd_links = [l for l in (b.get('links') or [])]
    rev_links = sorted([x['id'] for x in buddies.values()
                        if bid in (x.get('links') or [])])
    bplans = [p for p in plans if bid in (p.get('buddies') or [])]
    attn = [a if isinstance(a, dict) else {'text': str(a)} for a in (b.get('attention') or [])]
    docs = [d if isinstance(d, dict) else {'url': str(d), 'label': str(d)} for d in (b.get('docs') or [])]
    photos = [p for p in (b.get('photos') or [])]
    mem = memory_files(b)
    pinned = []
    ppath = os.path.join(HERE, bid, 'pinned.json')
    if os.path.exists(ppath):
        try:
            pinned = json.load(open(ppath))
            if isinstance(pinned, dict):
                pinned = pinned.get('pins') or pinned.get('items') or []
        except Exception:
            pinned = []

    # stat strip
    stats = []
    if attn: stats.append('<span class="stat"><b>%d</b> need attention</span>' % len(attn))
    if kids: stats.append('<span class="stat"><b>%d</b> sub-buddies</span>' % len(kids))
    if bplans: stats.append('<span class="stat"><b>%d</b> plans</span>' % len(bplans))
    if docs: stats.append('<span class="stat"><b>%d</b> documents</span>' % len(docs))
    if photos: stats.append('<span class="stat"><b>%d</b> photos</span>' % len(photos))
    if pinned: stats.append('<span class="stat"><b>%d</b> pinned</span>' % len(pinned))
    if b.get('status'):
        stats.insert(0, '<span class="status %s">%s</span>' % (esc(b.get('statusClass', '')), esc(b['status'])))

    # About
    about = ''
    if b.get('mission'):
        about += '<p class="mission">%s</p>' % esc(b['mission'])
    if b.get('brief'):
        about += '<p class="brief">%s</p>' % esc(b['brief'])
    if b.get('persona'):
        about += '<p class="persona">🎭 Persona: %s</p>' % esc(b['persona'])
    if b.get('voice'):
        about += '<p class="persona">🔊 Voice: %s</p>' % esc(b['voice'])
    about_sec = section('About', about)

    # Fact sheet — the raw data chain
    facts = []
    def fact(label, val):
        if val is None or val == '' or val == []:
            return
        facts.append('<div class="fact"><dt>%s</dt><dd>%s</dd></div>' % (esc(label), val))
    fact('Buddy ID', '<code>%s</code>' % esc(bid))
    fact('Kind', esc(b.get('kind', '')))
    if chain:
        crumbs = ' › '.join(buddy_link(buddies, p['id']) for p in reversed(chain))
        fact('Parent chain', crumbs)
    else:
        fact('Parent chain', '— top level —')
    if b.get('repo'):
        fact('Repository', '<a href="https://github.com/davedellaquila/%s" target="_blank" rel="noopener">davedellaquila/%s</a>' % (esc(b['repo']), esc(b['repo'])))
    if b.get('chat'):
        fact('Side thread', '<a href="https://muse.ai/chat/%s" target="_blank" rel="noopener">open thread</a>' % esc(b['chat']))
    if b.get('homepage'):
        fact('Homepage URL', '<code>%s</code>' % esc(b['homepage']))
    if b.get('homepageSource'):
        fact('Homepage source', esc(b['homepageSource']))
    if b.get('tags'):
        fact('Tags', esc(', '.join(b['tags'])))
    if b.get('aka'):
        fact('A.K.A.', esc(b['aka']))
    if b.get('alt_personas'):
        fact('Alt personas', esc(', '.join(b['alt_personas'])))
    if b.get('setup_pending'):
        fact('Setup', '⏳ pending')
    fact_sec = section('Fact sheet — the data chain', '<dl class="facts">' + ''.join(facts) + '</dl>' if facts else '<p class="empty">No registry facts beyond the header.</p>')

    # Attention
    attn_html = ''
    for a in attn:
        txt = esc(a.get('text', ''))
        if a.get('url'):
            txt = '<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (esc(a['url']), txt)
        date = '<div class="adate">%s</div>' % esc(a['date']) if a.get('date') else ''
        attn_html += '<div class="aitem"><span class="adot">●</span><div><div>%s</div>%s</div></div>' % (txt, date)
    attn_sec = section('Needs attention (%d)' % len(attn),
                       '<div class="attn">' + attn_html + '</div>' if attn_html
                       else '<p class="empty">Nothing needs attention right now.</p>')

    # Plans
    plans_html = ''
    for p in bplans:
        doc = ''
        if p.get('docs') and p['docs'][0].get('url'):
            doc = '<a class="pdoc" href="%s" target="_blank" rel="noopener">%s →</a>' % (esc(p['docs'][0]['url']), esc(p['docs'][0].get('label', 'Open doc')))
        plans_html += ('<div class="plan"><div class="picon">%s</div><div><div class="pname">%s%s</div>'
                       '<p class="pdesc">%s</p>%s</div></div>') % (
            esc(p.get('icon', '💼')), esc(p.get('name', 'Untitled')),
            '<span class="pill">%s</span>' % esc(p['status']) if p.get('status') else '',
            esc(p.get('desc', '')), doc)
    plans_sec = section('Plans (%d)' % len(bplans), plans_html)

    # Documents
    docs_html = ''.join(
        '<div class="docrow"><a href="%s" target="_blank" rel="noopener">%s</a></div>' % (esc(d.get('url', '#')), esc(d.get('label', d.get('url', 'Document'))))
        for d in docs)
    docs_sec = section('Documents (%d)' % len(docs), docs_html)

    # Sub-buddies
    kids_html = ''.join(
        '<a class="kid" href="../%s"><span class="kidicon">%s</span><span class="kidname">%s</span></a>' % (
            esc(k.get('homepage') or (k['id'] + '/')), esc(k.get('icon', '')), esc(k.get('name', k['id'])))
        for k in kids)
    kids_sec = section('Sub-buddies (%d)' % len(kids), '<div class="kids">' + kids_html + '</div>' if kids_html else '<p class="empty">No sub-buddies.</p>')

    # Connections
    conn = ''
    for p in eff_parents(buddies, b):
        conn += '<div class="connrow"><span class="connlabel">Parent</span>%s</div>' % buddy_link(buddies, p)
    if sibs:
        conn += '<div class="connrow"><span class="connlabel">Siblings</span>%s</div>' % ', '.join(buddy_link(buddies, s['id']) for s in sibs)
    if fwd_links:
        conn += '<div class="connrow"><span class="connlabel">Linked to</span>%s</div>' % ', '.join(buddy_link(buddies, l) for l in fwd_links)
    if rev_links:
        conn += '<div class="connrow"><span class="connlabel">Linked from</span>%s</div>' % ', '.join(buddy_link(buddies, l) for l in rev_links)
    conn_sec = section('Connections', conn if conn else '<p class="empty">No connections recorded.</p>')

    # Repository & memory
    rm = ''
    if b.get('repo'):
        rm += ('<div class="connrow"><span class="connlabel">Repo</span>'
               '<a href="https://github.com/davedellaquila/%s" target="_blank" rel="noopener">davedellaquila/%s</a>'
               ' <span class="muted">— brain dumps land in docs/ingest.md</span></div>') % (esc(b['repo']), esc(b['repo']))
    if pinned:
        items = ''.join('<div class="pinrow">📌 <b>%s</b><div class="muted">%s</div></div>' % (
            esc(p.get('title', '')), esc(p.get('detail', ''))) for p in pinned if isinstance(p, dict))
        rm += '<div class="connrow"><span class="connlabel">Pinned (%d)</span><div>%s</div></div>' % (len(pinned), items)
    if mem:
        rm += '<div class="connrow"><span class="connlabel">Memory</span>%s</div>' % ', '.join(
            '<code>%s</code>' % esc(os.path.basename(f)) for f in mem)
    rm_sec = section('Repository & memory', rm if rm else '<p class="empty">Nothing recorded.</p>')

    record_sec = record_section(b)
    repo_sec = repo_markdown_section(b)
    aboutnav = ''
    if about:
        aboutnav = ('<div class="aboutnav"><a href="./">\u2190 %s %s — homepage</a>'
                    '<span class="muted">This About page is the full record: every registry '
                    'field and every markdown file in the buddy\'s repo.</span></div>') % (esc(icon), esc(name))

    dumpbox = _C['DUMPBOX_HTML'].replace('__BID__', esc(bid)).replace('__BNAME__', esc(name))

    page = PAGE
    for k, v in {
        'title': esc(('About ' + name) if about else name), 'icon': esc(icon), 'name': esc(name),
        'family_nav': family_nav(buddies, b),
        'tagline': '<p class="tagline">%s</p>' % esc(b['tagline']) if b.get('tagline') else '',
        'stats': '<div class="stats">' + ''.join(stats) + '</div>' if stats else '',
        'about_sec': about_sec, 'fact_sec': fact_sec, 'attn_sec': attn_sec,
        'plans_sec': plans_sec, 'docs_sec': docs_sec, 'kids_sec': kids_sec,
        'conn_sec': conn_sec, 'rm_sec': rm_sec, 'record_sec': record_sec,
        'repo_sec': repo_sec, 'aboutnav': aboutnav,
        'files_css': _C['FILES_CSS'], 'files_js': _C['FILES_JS'],
        'dumpbox_css': _C['DUMPBOX_CSS'], 'dumpbox_html': dumpbox,
        'dumpbox_js': _C['DUMPBOX_JS'], 'attn_js': _C['ATTN_JS'],
        'date': TODAY, 'bid': esc(bid),
    }.items():
        page = page.replace('{' + k + '}', v)
    # Tip jar (Dave's standing rule, 2026-10-24; generator wiring 2026-10-27):
    # every generated page carries the canonical snippet, read live from
    # docs/tipjar-snippet.html so the fleet never drifts from the canonical copy.
    if 'class="tipjar"' not in page:
        try:
            _tipjar = open(os.path.join(HERE, 'docs', 'tipjar-snippet.html'), encoding='utf-8').read().strip('\n')
            page = page.replace('</body>', _tipjar + '\n</body>')
        except OSError:
            pass
    return page

PAGE = '<!-- DEFAULT-HOMEPAGE v3 — "The Dossier" -->\n<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex, nofollow">\n<meta name="color-scheme" content="dark light">\n<title>{title} — Buddy Dossier</title>\n<style>\n:root{color-scheme:dark light;--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#58a6ff;--amber:#f0b429;--amber-bd:#7d5e00}\n@media (prefers-color-scheme:light){:root{--bg:#ffffff;--card:#f6f8fa;--border:#d0d7de;--text:#1f2328;--muted:#57606a;--accent:#0969da}}\nbody{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;margin:0;line-height:1.6}\n.wrap{max-width:860px;margin:0 auto;padding:40px 22px 60px}\nheader.hero{display:flex;gap:18px;align-items:center;margin-bottom:8px}\n.heroicon{width:72px;height:72px;flex:none;border-radius:20px;background:var(--card);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:38px}\nh1{margin:0;font-size:30px;letter-spacing:-.02em}\n.tagline{color:var(--muted);margin:6px 0 0;font-size:15px}\n.stats{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 28px}\n.stat{font-size:12.5px;color:var(--muted);background:var(--card);border:1px solid var(--border);border-radius:999px;padding:4px 12px}\n.stat b{color:var(--text)}\n.status{font-size:12.5px;font-weight:700;border-radius:999px;padding:4px 12px;background:var(--card);border:1px solid var(--border)}\n.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 22px;margin-bottom:20px}\n.kicker{margin:0 0 10px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}\n.mission{font-size:16px;margin:0 0 10px}\n.brief{color:var(--muted);font-size:14px}\n.persona{font-size:14px;margin:8px 0 0}\n.facts{margin:0;display:grid;gap:2px}\n.fact{display:grid;grid-template-columns:150px 1fr;gap:12px;padding:7px 0;border-top:1px solid var(--border);font-size:14px}\n.fact:first-child{border-top:0}\n.fact dt{color:var(--muted);font-weight:600}\n.fact dd{margin:0;overflow-wrap:break-word}\ncode{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:1px 6px;font-size:13px}\na{color:var(--accent);text-decoration:none}\na:hover{text-decoration:underline}\n.aitem{display:flex;gap:10px;padding:10px 0;font-size:14px}\n.aitem+.aitem{border-top:1px solid var(--border)}\n.adot{color:var(--amber);font-size:11px;line-height:2;flex:none}\n.adate{color:var(--muted);font-size:12px;margin-top:2px}\n.plan{display:flex;gap:12px;padding:12px 0}\n.plan+.plan{border-top:1px solid var(--border)}\n.picon{font-size:24px;flex:none}\n.pname{font-weight:650;font-size:15px}\n.pill{display:inline-block;font-size:11px;font-weight:700;background:var(--bg);border:1px solid var(--border);color:var(--accent);border-radius:999px;padding:2px 10px;margin-left:8px}\n.pdesc{margin:6px 0 0;color:var(--muted);font-size:13.5px}\n.pdoc{display:inline-block;margin-top:6px;font-size:13px}\n.docrow{padding:8px 0;font-size:14.5px}\n.docrow+.docrow{border-top:1px solid var(--border)}\n.kids{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}\n.kid{display:flex;align-items:center;gap:10px;background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:10px 12px;color:var(--text)}\n.kid:hover{text-decoration:none;border-color:var(--accent)}\n.kidicon{font-size:22px}\n.kidname{font-size:14px;font-weight:600}\n.connrow{display:flex;gap:12px;padding:8px 0;font-size:14px;align-items:baseline}\n.connrow+.connrow{border-top:1px solid var(--border)}\n.connlabel{flex:none;width:110px;color:var(--muted);font-weight:600;font-size:13px}\n.pinrow{padding:6px 0;font-size:14px}\n.muted{color:var(--muted);font-size:13px}\n.empty{color:var(--muted);font-style:italic;margin:4px 0}\nfooter{margin-top:36px;padding-top:18px;border-top:1px solid var(--border);color:var(--muted);font-size:12.5px;text-align:center}\n.aboutnav{display:flex;gap:14px;flex-wrap:wrap;align-items:baseline;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px 16px;margin-bottom:22px;font-size:14px}.unset{color:var(--muted);font-style:italic}.recjson{margin:0;font-size:12px;white-space:pre-wrap;overflow-wrap:break-word}.mdfile{border-top:1px solid var(--border);padding:14px 0}.mdfile-head{display:flex;gap:12px;align-items:baseline;margin-bottom:8px}details.mdfile summary{cursor:pointer;font-size:14px}.md-body{font-size:14.5px}.md-body h1{font-size:21px;margin:14px 0 8px}.md-body h2{font-size:18px;margin:14px 0 6px}.md-body h3{font-size:15.5px;margin:12px 0 4px}.md-body p{margin:8px 0}.md-body ul,.md-body ol{margin:8px 0 8px 22px}.md-body li{margin:3px 0}.md-body pre{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 12px;overflow-x:auto;font-size:12.5px}.md-body table{border-collapse:collapse;margin:10px 0;font-size:13.5px}.md-body th,.md-body td{border:1px solid var(--border);padding:5px 9px;text-align:left}.md-body blockquote{border-left:3px solid var(--border);margin:10px 0;padding:2px 14px;color:var(--muted)}.mdfallback{white-space:pre-wrap;font-size:12.5px}.mdinv{margin:6px 0 12px 20px;font-size:14px}.mdinv li{margin:3px 0}.repo-files h2{font-size:17px;margin:0 0 4px;color:var(--text)}.attn-btn{background:var(--bg);color:var(--text);border:1px solid var(--border);border-radius:8px;padding:6px 14px;font-size:13px;font-weight:600;cursor:pointer}.attn-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}.attn-actions{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}.attn-status{font-size:13px;color:var(--muted);margin-top:8px}\n{dumpbox_css}\n{files_css}\n@media (max-width:640px){.fact{grid-template-columns:1fr;gap:2px}.connlabel{width:88px}.wrap{padding:28px 16px 48px}h1{font-size:24px}}\n</style>\n</head>\n<body>\n<div class="wrap">\n{aboutnav}\n<header class="hero">\n<div class="heroicon">{icon}</div>\n<div><h1>{name}</h1>{tagline}</div>\n</header>\n{family_nav}\n{stats}\n{about_sec}\n{fact_sec}\n{record_sec}\n{attn_sec}\n{plans_sec}\n{docs_sec}\n{kids_sec}\n{conn_sec}\n{rm_sec}\n{repo_sec}\n{dumpbox_html}\n<footer>Default Homepage v3 — "The Dossier" · Generated {date} · Part of the Buddy System &middot; <a href="https://davedellaquila.github.io/buddy-system/">Buddy System dashboard</a><br>\n<span class="muted">Archived PDF snapshots live in the buddy-system archive folder.</span></footer>\n</div>\n{dumpbox_js}\n{files_js}\n{attn_js}\n</body>\n</html>\n'


def main():
    about = '--about' in sys.argv[1:]
    targets = [a for a in sys.argv[1:] if a != '--about']
    if not targets:
        print("usage: gen_default_homepages.py [--about] <buddy-id> [...]")
        sys.exit(1)
    buddies, plans = load()
    for bid in targets:
        b = buddies.get(bid)
        if not b:
            print("unknown buddy:", bid)
            continue
        page = build_page(buddies, plans, b, about=about)
        outdir = os.path.join(HERE, bid)
        os.makedirs(outdir, exist_ok=True)
        if about:
            out = os.path.join(outdir, 'about.html')
            open(out, 'w').write(page)
            print("wrote", out, len(page), "bytes")
            continue
        idx = os.path.join(outdir, 'index.html')
        if os.path.exists(idx):
            bak = os.path.join(outdir, 'index.html.v2-bak')
            if not os.path.exists(bak):
                os.rename(idx, bak)
                print("backed up v2 ->", bak)
        open(idx, 'w').write(page)
        print("wrote", idx, len(page), "bytes")

if __name__ == '__main__':
    main()

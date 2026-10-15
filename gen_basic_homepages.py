#!/usr/bin/env python3
"""Generate basic homepages for buddies, and refresh template-driven ones.

CRITICAL: every buddy website must support dark mode. This template does via
prefers-color-scheme — do not ship light-only pages. See AGENTS.md and
docs/standing-orders.md.

Template-driven pages carry the <!-- BUDDY-BASIC-TEMPLATE --> marker (v1 pages
are detected by their "Part of the Buddy System" footer signature). Pages
WITHOUT the marker are thread-owned custom designs and are NEVER overwritten
here — the daily rebuild relies on this distinction.
"""
import json
import os
import html
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# Optional: --only <buddy-id> regenerates a single page (used to test
# template changes on one buddy before the daily rebuild rolls them out).
only_bid = None
if '--only' in sys.argv:
    idx = sys.argv.index('--only')
    if idx + 1 < len(sys.argv):
        only_bid = sys.argv[idx + 1]

with open('buddies.json') as f:
    d = json.load(f)

by_id = {b['id']: b for b in d['buddies']}

# ---------------------------------------------------------------------------
# Dump box: self-contained brain-dump snippet (HTML+CSS+JS).
# Same GitHub write path as the dashboard's ingest panel: reads the shared
# GitHub token from the dashboard origin's localStorage (key 'buddyTree.v3',
# field 'ghToken'), resolves the buddy's repo from ../buddies.json, and appends
# a timestamped entry to docs/ingest.md via the GitHub contents API.
# __BID__ / __BNAME__ are substituted per buddy at generation time.
# ---------------------------------------------------------------------------
DUMPBOX_CSS = """
.dumpbox {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 22px;
  margin-bottom: 32px;
}
.dumpbox h2 { margin: 0 0 6px; font-size: 20px; }
.dumpbox-sub { color: var(--muted); font-size: 14px; margin-bottom: 14px; }
.dumpbox textarea {
  width: 100%; min-height: 96px; resize: vertical;
  background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 12px; font-size: 14px; color: var(--text); font-family: inherit;
}
.dumpbox textarea:focus { outline: none; border-color: var(--accent); }
.dumpbox textarea:disabled { opacity: .55; }
.dumpbox-row { display: flex; align-items: center; gap: 12px; margin-top: 10px; flex-wrap: wrap; }
.dumpbox-btn {
  background: var(--accent); color: #fff; border: none; border-radius: 8px;
  padding: 9px 22px; font-size: 14px; font-weight: 600; cursor: pointer;
}
.dumpbox-btn:disabled { opacity: .45; cursor: default; }
.dumpbox-status { font-size: 13px; color: var(--muted); }
.dumpbox-token {
  background: var(--bg); border: 1px dashed var(--border); border-radius: 8px;
  padding: 12px 14px; margin-bottom: 12px; font-size: 14px;
}
.dumpbox-token p { margin-bottom: 8px; }
.dumpbox-tokenrow { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.dumpbox-tokenrow input {
  flex: 1; min-width: 170px; background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; padding: 7px 10px; font-size: 13px; color: var(--text);
}
.dumpbox-tokenrow button {
  background: transparent; color: var(--accent); border: 1px solid var(--accent);
  border-radius: 8px; padding: 7px 14px; font-size: 13px; font-weight: 600; cursor: pointer;
}
.dumpbox-tokenrow a { color: var(--accent); font-size: 13px; }
"""

DUMPBOX_HTML = """
<section class="dumpbox" data-buddy-id="__BID__">
<h2>🧠 Brain dump</h2>
<p class="dumpbox-sub">Dump what's on your mind about __BNAME__ — raw and unfiltered. Each dump lands in the buddy's repo (docs/ingest.md) as a timestamped entry.</p>
<div class="dumpbox-token" hidden>
<p>🔒 Connect GitHub to unlock dumping. Paste a token once — it stays on this device only.</p>
<div class="dumpbox-tokenrow">
<input type="password" placeholder="GitHub token (repo scope)" aria-label="GitHub token">
<button type="button">Save token</button>
<a href="https://github.com/settings/tokens" target="_blank" rel="noopener">Get a token</a>
</div>
</div>
<textarea rows="4" placeholder="Dump what's on your mind about __BNAME__…"></textarea>
<div class="dumpbox-row">
<button type="button" class="dumpbox-btn">Dump it</button>
<span class="dumpbox-status" role="status"></span>
</div>
</section>
"""

DUMPBOX_JS = """
<script>
(function(){
  var box = document.querySelector('.dumpbox');
  if (!box || box.dataset.dumpInit) return;
  box.dataset.dumpInit = '1';
  var bid = box.getAttribute('data-buddy-id') || (function(){
    var p = location.pathname.replace(/\\/+$/, '');
    return p.substring(p.lastIndexOf('/') + 1);
  })();
  var ta = box.querySelector('textarea'),
      btn = box.querySelector('.dumpbox-btn'),
      st = box.querySelector('.dumpbox-status'),
      tokWrap = box.querySelector('.dumpbox-token');
  function lsGet(){ try { return JSON.parse(localStorage.getItem('buddyTree.v3') || '{}'); } catch(e){ return {}; } }
  function lsSet(patch){ try { var s = lsGet(); for (var k in patch) s[k] = patch[k]; localStorage.setItem('buddyTree.v3', JSON.stringify(s)); } catch(e){} }
  function token(){ return lsGet().ghToken || ''; }
  function b64encode(str){
    var bytes = new TextEncoder().encode(str), bin = '';
    bytes.forEach(function(b){ bin += String.fromCharCode(b); });
    return btoa(bin);
  }
  async function ghApi(path, method, body){
    var t = token();
    if (!t) throw new Error('Add a GitHub token first.');
    var r = await fetch('https://api.github.com' + path, {
      method: method || 'GET',
      headers: {'Authorization': 'Bearer ' + t, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'},
      body: body ? JSON.stringify(body) : undefined
    });
    if (!r.ok) throw new Error('GitHub ' + r.status);
    return r.status === 204 ? null : await r.json();
  }
  async function ghGetFile(repo, path){
    try {
      var j = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path);
      if (j && j.content) return {
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\\n/g, '')), function(c){ return c.charCodeAt(0); })),
        sha: j.sha
      };
    } catch(e){}
    return null;
  }
  var repo = null, repoName = bid;
  async function resolveRepo(){
    try {
      var r = await fetch('../buddies.json', {cache: 'no-store'});
      var d = await r.json();
      var buds = d.buddies || [];
      for (var i = 0; i < buds.length; i++) {
        if (buds[i].id === bid && buds[i].repo) { repo = buds[i].repo; repoName = buds[i].name || bid; break; }
      }
    } catch(e){}
  }
  function refreshUI(){
    var has = !!token();
    tokWrap.hidden = has;
    var ok = has && !!repo;
    ta.disabled = !ok;
    btn.disabled = !ok;
    if (!has) { st.textContent = ''; }
    else if (!repo) { st.textContent = 'No repo linked for this buddy yet.'; }
  }
  var tokInput = tokWrap.querySelector('input'),
      tokSave = tokWrap.querySelector('button');
  tokSave.addEventListener('click', function(){
    var v = tokInput.value.trim();
    if (!v) return;
    lsSet({ghToken: v});
    tokInput.value = '';
    refreshUI();
    st.textContent = 'Token saved on this device.';
  });
  async function dump(){
    var text = ta.value.trim();
    if (!text) return;
    if (!token()) { refreshUI(); return; }
    if (!repo) { st.textContent = 'No repo linked for this buddy yet.'; return; }
    st.textContent = 'Dumping…';
    btn.disabled = true;
    try {
      var stamp = new Date().toLocaleString();
      var NL = String.fromCharCode(10);
      var entry = '## ' + stamp + NL + NL + text + NL + NL;
      var cur = await ghGetFile(repo, 'docs/ingest.md');
      var base = cur ? cur.text : '# Ingest log — ' + repoName + NL + NL;
      var body = {message: 'Ingest dump for ' + bid, content: b64encode(base + entry)};
      if (cur && cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md', 'PUT', body);
      ta.value = '';
      st.textContent = '✓ Dumped to ' + repo + '/docs/ingest.md';
    } catch(err){ st.textContent = 'Save failed: ' + (err.message || err); }
    btn.disabled = false;
  }
  btn.addEventListener('click', dump);
  ta.addEventListener('keydown', function(ev){
    if ((ev.metaKey || ev.ctrlKey) && ev.key === 'Enter') { ev.preventDefault(); dump(); }
  });
  resolveRepo().then(refreshUI);
})();
</script>
"""

# ---------------------------------------------------------------------------
# Attention actions: per-tile follow-up buttons ("Done", "Need more info").
# Same GitHub write path as the dump box: the shared token from localStorage
# ('buddyTree.v3' / 'ghToken') appends a timestamped entry to the buddy's
# docs/ingest.md, which the buddy triages — "Done" asks the buddy to clear
# the item from buddies.json; "Need more info" asks it to follow up.
# The tile resolves locally immediately (persisted in localStorage) so Dave
# sees it handled even before the next rebuild.
# ---------------------------------------------------------------------------
ATTN_JS = """
<script>
(function(){
  var tiles = document.querySelectorAll('.attn[data-attn-id]');
  if (!tiles.length) return;
  var dumpbox = document.querySelector('.dumpbox');
  var bid = (dumpbox && dumpbox.getAttribute('data-buddy-id')) || (function(){
    var p = location.pathname.replace(/\\/+$/, '');
    return p.substring(p.lastIndexOf('/') + 1);
  })();
  function lsGet(){ try { return JSON.parse(localStorage.getItem('buddyTree.v3') || '{}'); } catch(e){ return {}; } }
  function lsSet(patch){ try { var s = lsGet(); for (var k in patch) s[k] = patch[k]; localStorage.setItem('buddyTree.v3', JSON.stringify(s)); } catch(e){} }
  function token(){ return lsGet().ghToken || ''; }
  function b64encode(str){
    var bytes = new TextEncoder().encode(str), bin = '';
    bytes.forEach(function(b){ bin += String.fromCharCode(b); });
    return btoa(bin);
  }
  async function ghApi(path, method, body){
    var t = token();
    if (!t) throw new Error('Add a GitHub token first.');
    var r = await fetch('https://api.github.com' + path, {
      method: method || 'GET',
      headers: {'Authorization': 'Bearer ' + t, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'},
      body: body ? JSON.stringify(body) : undefined
    });
    if (!r.ok) throw new Error('GitHub ' + r.status);
    return r.status === 204 ? null : await r.json();
  }
  async function ghGetFile(repo, path){
    try {
      var j = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path);
      if (j && j.content) return {
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\\n/g, '')), function(c){ return c.charCodeAt(0); })),
        sha: j.sha
      };
    } catch(e){}
    return null;
  }
  var repo = null, buddyName = bid;
  async function resolveBuddy(){
    try {
      var r = await fetch('../buddies.json', {cache: 'no-store'});
      var d = await r.json();
      var buds = d.buddies || [];
      for (var i = 0; i < buds.length; i++) {
        if (buds[i].id === bid) {
          if (buds[i].repo) repo = buds[i].repo;
          if (buds[i].name) buddyName = buds[i].name;
          break;
        }
      }
    } catch(e){}
  }
  function rkey(aid, text){ return bid + '|' + (aid || ('text:' + text.slice(0, 60))); }
  function isResolved(aid, text){ var m = lsGet().attnDone || {}; return !!m[rkey(aid, text)]; }
  function setResolved(aid, text){ var s = lsGet(); var m = s.attnDone || {}; m[rkey(aid, text)] = 1; s.attnDone = m; lsSet(s); }
  function paintResolved(tile, msg){
    tile.classList.add('resolved');
    var st = tile.querySelector('.attn-status');
    if (st) st.textContent = msg;
  }
  async function sendAction(tile, entry, okMsg){
    var st = tile.querySelector('.attn-status');
    var btns = tile.querySelectorAll('.attn-btn');
    if (!token()) { st.textContent = 'Add a GitHub token in the Brain dump section above to enable actions.'; return false; }
    if (!repo) { st.textContent = 'No repo linked for this buddy yet.'; return false; }
    btns.forEach(function(b){ b.disabled = true; });
    st.textContent = 'Working…';
    try {
      var NL = String.fromCharCode(10);
      var stamp = new Date().toLocaleString();
      var cur = await ghGetFile(repo, 'docs/ingest.md');
      var base = cur ? cur.text : '# Ingest log — ' + buddyName + NL + NL;
      var body = {message: 'Attention action for ' + bid, content: b64encode(base + '## ' + stamp + NL + NL + entry + NL + NL)};
      if (cur && cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md', 'PUT', body);
      st.textContent = okMsg;
      return true;
    } catch(err){
      st.textContent = 'Save failed: ' + (err.message || err);
      btns.forEach(function(b){ b.disabled = false; });
      return false;
    }
  }
  tiles.forEach(function(tile){
    var aid = tile.getAttribute('data-attn-id') || '';
    var textEl = tile.querySelector('.attn-text');
    var text = textEl ? textEl.textContent.trim() : '';
    if (isResolved(aid, text)) { paintResolved(tile, 'Marked done'); return; }
    tile.addEventListener('click', function(ev){
      var btn = ev.target.closest ? ev.target.closest('.attn-btn') : null;
      if (!btn || btn.disabled) return;
      var act = btn.getAttribute('data-act');
      var idBit = aid ? ' (attention id: ' + aid + ')' : '';
      if (act === 'done') {
        sendAction(tile,
          'DONE — Dave marked this done on the homepage: "' + text + '"' + idBit + '. Please remove it from the attention list in buddies.json.',
          'Marked done — the buddy will clear it.').then(function(ok){ if (ok) { setResolved(aid, text); paintResolved(tile, 'Marked done — the buddy will clear it.'); } });
      } else if (act === 'info') {
        sendAction(tile,
          'FOLLOW-UP — Dave needs more info on: "' + text + '"' + idBit + '. Please follow up with him.',
          'Sent — ' + buddyName + ' will follow up.');
      }
    });
  });
  resolveBuddy();
})();
</script>
"""

TEMPLATE = """<!-- BUDDY-BASIC-TEMPLATE v2 -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}</title>
<style>
:root {{
  --bg: #ffffff;
  --text: #1a1a1a;
  --muted: #666;
  --card: #f5f5f5;
  --border: #e0e0e0;
  --accent: #0066cc;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #1a1a1a;
    --text: #e0e0e0;
    --muted: #999;
    --card: #2a2a2a;
    --border: #3a3a3a;
    --accent: #4da6ff;
  }}
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  padding: 40px 20px;
  max-width: 800px;
  margin: 0 auto;
}}
.header {{ text-align: center; margin-bottom: 40px; }}
.topbar {{
  position: sticky; top: 0; z-index: 50;
  display: flex; align-items: center; gap: 10px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  padding: 10px 2px; margin-bottom: 24px;
  font-size: 17px; font-weight: 700;
}}
.topbar-icon {{ font-size: 22px; line-height: 1; }}
.icon {{ font-size: 64px; margin-bottom: 16px; }}
h1 {{ font-size: 32px; margin-bottom: 8px; }}
.tagline {{ color: var(--muted); font-size: 18px; }}
.mission {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
  font-size: 17px;
}}
h2 {{ font-size: 22px; margin: 32px 0 16px; }}
.attn {{
  background: var(--card);
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 16px 20px;
  margin-bottom: 12px;
}}
.attn-date {{ color: var(--muted); font-size: 14px; margin-top: 8px; }}
.attn-actions {{ display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }}
.attn-btn {{
  border: 1px solid var(--border); background: var(--bg); color: var(--text);
  border-radius: 8px; padding: 7px 14px; font-size: 13px; font-weight: 600; cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}}
.attn-btn:hover {{ border-color: var(--accent); }}
.attn-btn.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
.attn-btn:disabled {{ opacity: .45; cursor: default; }}
.attn-status {{ font-size: 13px; color: var(--muted); margin-top: 8px; min-height: 18px; }}
.attn.resolved {{ opacity: .6; }}
.attn.resolved .attn-actions {{ display: none; }}
.children {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.child {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 20px;
  text-decoration: none;
  color: var(--text);
}}
.child:hover {{ border-color: var(--accent); }}
.footer {{
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 14px;
  text-align: center;
}}
.empty {{ color: var(--muted); font-style: italic; }}
{dumpbox_css}
</style>
</head>
<body>
<div class="topbar"><span class="topbar-icon">{icon}</span><span class="topbar-name">{name}</span></div>
<div class="header">
<div class="icon">{icon}</div>
<h1>{name}</h1>
<div class="tagline">{tagline}</div>
</div>

<div class="mission">{mission}</div>

{dumpbox_html}

{attention_section}

{children_section}

<div class="footer">
Generated {date} · Part of the Buddy System
</div>
{dumpbox_js}
{attn_js}
</body>
</html>
"""

from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')


def is_template_page(idxpath):
    """True if the existing page was generated from the basic template."""
    try:
        with open(idxpath) as f:
            content = f.read()
    except OSError:
        return False
    return ('BUDDY-BASIC-TEMPLATE' in content) or ('Part of the Buddy System' in content)


generated = []
for b in d['buddies']:
    bid = b['id']
    if only_bid and bid != only_bid:
        continue
    dirpath = os.path.join(HERE, bid)
    idxpath = os.path.join(dirpath, 'index.html')
    has_page = os.path.exists(idxpath)

    if b.get('homepage') and has_page and not is_template_page(idxpath):
        continue  # Thread-owned custom design — never overwrite

    name = html.escape(b.get('name', bid))
    icon = b.get('icon', '🤖')
    tagline = html.escape(b.get('tagline', ''))
    mission = html.escape(b.get('mission', 'No mission yet.'))

    # Attention items
    attn_items = b.get('attention', [])
    if attn_items:
        attn_html = '<h2>Needs Attention</h2>\n'
        for a in attn_items[:10]:
            text = html.escape(a.get('text', str(a)) if isinstance(a, dict) else str(a))
            date = html.escape(a.get('date', '') if isinstance(a, dict) else '')
            aid = html.escape(a.get('id', '') if isinstance(a, dict) else '', quote=True)
            attn_html += f'<div class="attn" data-attn-id="{aid}"><div class="attn-text">{text}</div>'
            if date:
                attn_html += f'<div class="attn-date">{date}</div>'
            attn_html += ('<div class="attn-actions">'
                          '<button type="button" class="attn-btn primary" data-act="done">✓ Done</button>'
                          '<button type="button" class="attn-btn" data-act="info">Need more info</button>'
                          '</div><div class="attn-status" role="status"></div></div>\n')
        attention_section = attn_html
    else:
        attention_section = '<h2>Needs Attention</h2>\n<p class="empty">Nothing needs attention right now.</p>'

    # Children
    children = [by_id[cid] for cid in b.get('children', []) if cid in by_id]
    # Also find buddies with this as parent
    kids = [x for x in d['buddies'] if x.get('parent') == bid]
    all_kids = {c['id']: c for c in children + kids}.values()
    if all_kids:
        kids_html = '<h2>Sub-buddies</h2>\n<div class="children">\n'
        for k in sorted(all_kids, key=lambda x: x.get('name', '')):
            kname = html.escape(k.get('name', k['id']))
            kicon = k.get('icon', '🤖')
            kids_html += f'<a class="child" href="../{k["id"]}/">{kicon} {kname}</a>\n'
        kids_html += '</div>'
        children_section = kids_html
    else:
        children_section = ''

    dumpbox_html = DUMPBOX_HTML.replace('__BID__', bid).replace('__BNAME__', name)

    page = TEMPLATE.format(
        name=name,
        icon=icon,
        tagline=tagline,
        mission=mission,
        attention_section=attention_section,
        children_section=children_section,
        date=today,
        dumpbox_css=DUMPBOX_CSS,
        dumpbox_html=dumpbox_html,
        dumpbox_js=DUMPBOX_JS,
        attn_js=ATTN_JS,
    )

    # Write to <bid>/index.html
    os.makedirs(dirpath, exist_ok=True)
    with open(idxpath, 'w') as f:
        f.write(page)

    # Update buddies.json
    b['homepage'] = f'{bid}/'
    generated.append(bid)
    print(f"Generated {bid}/index.html")

with open('buddies.json', 'w') as f:
    # Match the file's existing format exactly (indent=1, literal UTF-8)
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.write('\n')

print(f"\nDone: {len(generated)} pages generated")

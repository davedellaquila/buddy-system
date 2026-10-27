#!/usr/bin/env python3
"""Generate basic homepages for buddies, and refresh template-driven ones.

CRITICAL: every buddy website must support dark mode. This template does via
prefers-color-scheme — do not ship light-only pages. See AGENTS.md and
docs/standing-orders.md.

Template-driven pages carry the <!-- BUDDY-BASIC-TEMPLATE --> marker (v1 pages
are detected by their "Part of the Buddy System" footer signature). Pages
WITHOUT the marker are thread-owned custom designs and are NEVER overwritten
here — the daily rebuild relies on this distinction. DEFAULT-HOMEPAGE v3
"Dossier" pages are also never regenerated here: they are a newer default
treatment, not basic-template pages, despite the shared footer signature.
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
# Family nav: parent crumb + children links (Dave 2026-10-15).
# Multi-parent aware: shows all parents, lists children under each parent.
BASE_URL = 'https://davedellaquila.github.io/buddy-system/'
CRUMB_STYLE = ("padding:14px 20px 0;font-family:-apple-system,BlinkMacSystemFont,"
               "'Segoe UI',sans-serif;font-size:14px;line-height:1.4;")
KIDS_STYLE = ("padding:6px 20px 0;font-family:-apple-system,BlinkMacSystemFont,"
              "'Segoe UI',sans-serif;font-size:14px;line-height:1.9;")

def eff_parents(b):
    ps = list(b.get('parents') or [])
    if b.get('parent') and b['parent'] not in ps:
        ps.append(b['parent'])
    return [p for p in ps if p in by_id]

def family_nav(b):
    """Parent crumb + children nav HTML for the top of a buddy homepage."""
    bid = b['id']
    parts = []
    parents = eff_parents(b)
    if parents:
        links = ' · '.join(
            '<a href="%s%s/" style="color:inherit;opacity:.65;text-decoration:none;">← %s</a>'
            % (BASE_URL, p, html.escape(by_id[p].get('name', p)))
            for p in parents)
        parts.append('<nav data-buddy-crumb style="%s">%s</nav>' % (CRUMB_STYLE, links))
    elif bid != 'astro':
        # Top-level buddies link to Astro (root)
        parts.append('<nav data-buddy-crumb style="%s">'
                     '<a href="%sastro/" style="color:inherit;opacity:.65;text-decoration:none;">← Astro</a>'
                     '</nav>' % (CRUMB_STYLE, BASE_URL))
    kids = sorted(
        (x for x in d['buddies'] if bid in eff_parents(x)),
        key=lambda x: x.get('name', ''))
    if kids:
        links = ' '.join(
            '<a href="%s%s/" style="color:inherit;text-decoration:none;margin-right:14px;white-space:nowrap;">%s %s</a>'
            % (BASE_URL, k['id'], k.get('icon', ''),
               html.escape(k.get('name', k['id'])))
            for k in kids)
        parts.append('<nav data-buddy-kids style="%s">'
                     '<span style="opacity:.65;">Children:</span> %s</nav>'
                     % (KIDS_STYLE, links))
    return '\n'.join(parts)

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
.dumpbox-btn.saved { background: var(--ok); }
.dumpbox-status { font-size: 13px; color: var(--muted); }
.dumpbox-status.flash { color: var(--ok); font-weight: 700; }
.dumpbox-hint { font-size: 12px; color: var(--muted); margin-top: 8px; }
.dumpbox-token {
  /* Jonny, 2026-10-19 (Dave's ask): amber, not zebra. A solid amber frame +
     a soft amber wash says "one small step needs you" — zebra striping is
     hazard tape, it signals danger and fights every calm surface around it.
     Dashed grey read as placeholder; solid amber reads as deliberate. */
  background: rgba(245, 158, 11, .09);
  background: color-mix(in srgb, #f59e0b 9%, var(--bg));
  border: 2px solid #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, .16);
  box-shadow: 0 0 0 3px color-mix(in srgb, #f59e0b 16%, transparent);
  border-radius: 8px;
  padding: 12px 14px; margin-bottom: 12px; font-size: 14px;
}
.dumpbox-token p { margin-bottom: 8px; font-weight: 700; color: #cf222e; }
@media (prefers-color-scheme: dark) { .dumpbox-token p { color: #ff7b72; } }
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
<p class="dumpbox-sub">Dump what's on your mind about <span data-buddy-name>__BNAME__</span> — raw and unfiltered. Each dump lands in the buddy's repo (docs/ingest.md) as a timestamped entry — or saves on this device until a repo is linked and a token is connected.</p>
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
<p class="dumpbox-hint">Enter dumps it &middot; Shift+Enter for a new line</p>
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
  /* Local fallback (Dave 2026-10-15, widened 2026-10-16): dumping always works,
     even with no GitHub token AND no repo linked — entries are saved in this
     device's localStorage until the GitHub write path can take them. The backlog
     flushes into the repo on the next successful GitHub dump (once a repo is
     linked and a token is present). */
  function localKey(){ return 'buddyTree.ingest.' + bid; }
  function localBacklog(){
    try { var a = JSON.parse(localStorage.getItem(localKey()) || '[]'); return Array.isArray(a) ? a : []; }
    catch(e){ return []; }
  }
  function localSave(entry){
    var a = localBacklog(); a.push(entry);
    try { localStorage.setItem(localKey(), JSON.stringify(a)); } catch(e){}
  }
  function localClear(){ try { localStorage.removeItem(localKey()); } catch(e){} }
  function refreshUI(){
    var has = !!token();
    tokWrap.hidden = has;
    /* The box always works: no token and/or no repo just means local saves. */
    ta.disabled = false;
    btn.disabled = false;
    var n = localBacklog().length;
    if (!repo) {
      st.textContent = n
        ? n + ' local ' + (n === 1 ? 'dump' : 'dumps') + ' saved on this device — will sync when a repo is linked.'
        : 'No repo linked yet — dumps save on this device and will sync when one is linked.';
      return;
    }
    st.textContent = has
      ? (n ? n + ' local ' + (n === 1 ? 'dump' : 'dumps') + ' will sync on next dump.' : '')
      : 'No GitHub token — dumps save on this device for now.';
  }
  var tokInput = tokWrap.querySelector('input'),
      tokSave = tokWrap.querySelector('button');
  /* Visual save confirmation (Dave 2026-10-16): the button flashes green
     with a ✓ for ~2s on every successful save, so the save is unmissable. */
  function flashSaved(){
    var label = btn.textContent;
    btn.classList.add('saved');
    btn.textContent = '✓ Saved';
    st.classList.add('flash');
    setTimeout(function(){
      btn.classList.remove('saved');
      if (btn.textContent === '✓ Saved') btn.textContent = label;
      st.classList.remove('flash');
    }, 1800);
  }
  /* Dave 2026-10-18: verify the token against GitHub when pasted, so a
     bad token is caught here instead of surfacing as a mysterious 404 on
     the next dump. The token is kept either way; dumps queue locally until
     a working token is in place. */
  tokSave.addEventListener('click', async function(){
    var v = tokInput.value.trim();
    if (!v) return;
    lsSet({ghToken: v});
    tokInput.value = '';
    st.textContent = 'Checking token…';
    try {
      await ghApi('/user');
      refreshUI();
      st.textContent = '✓ Token verified — dumps will sync to GitHub.';
    } catch(e) {
      refreshUI();
      st.textContent = '⚠ GitHub rejected that token (' + ((e && e.message) || e) + ') — dumps stay on this device until a working token is added.';
    }
  });
  async function dump(){
    var text = ta.value.trim();
    if (!text) return;
    var stamp = new Date().toLocaleString();
    var NL = String.fromCharCode(10);
    if (!repo) {
      /* No repo linked yet — save on this device; syncs once one is linked. */
      localSave({t: stamp, text: text});
      ta.value = '';
      refreshUI();
      st.textContent = '✓ Saved on this device — will sync to the repo once one is linked.';
      flashSaved();
      return;
    }
    if (!token()) {
      /* Temporary workaround: no token → save on this device. */
      localSave({t: stamp, text: text});
      ta.value = '';
      st.textContent = '✓ Saved on this device — add a GitHub token to sync it to the repo.';
      flashSaved();
      return;
    }
    st.textContent = 'Dumping…';
    btn.disabled = true;
    try {
      /* Flush any locally-saved backlog first, then the new entry. */
      var backlog = localBacklog();
      var parts = backlog.map(function(b){ return '## ' + b.t + NL + NL + b.text + NL + NL; });
      parts.push('## ' + stamp + NL + NL + text + NL + NL);
      var cur = await ghGetFile(repo, 'docs/ingest.md');
      var base = cur ? cur.text : '# Ingest log — ' + repoName + NL + NL;
      var body = {message: 'Ingest dump for ' + bid, content: b64encode(base + parts.join(''))};
      if (cur && cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md', 'PUT', body);
      localClear();
      ta.value = '';
      st.textContent = '✓ Dumped to ' + repo + '/docs/ingest.md' + (backlog.length ? ' (' + backlog.length + ' local synced)' : '');
      flashSaved();
    } catch(err){
      /* Dave 2026-10-18: a failed GitHub write must never drop the dump.
         Keep it on this device and say so plainly, with the backlog count —
         it syncs on the next successful dump. */
      try { localSave({t: stamp, text: text}); } catch(e2){}
      ta.value = '';
      refreshUI();
      var why = (err && err.message) || String(err);
      var nq = 0; try { nq = localBacklog().length; } catch(e2){}
      var tail = nq > 1 ? ' (' + nq + ' on this device waiting to sync)' : '';
      st.textContent = (/404/.test(why)
        ? '⚠ Saved on this device — GitHub said 404 (usually a wrong/expired token, or no access to this private repo). Fix the token, then dump again to sync.'
        : '⚠ Saved on this device — GitHub said: ' + why + '. It will sync on your next successful dump.') + tail;
    }
    btn.disabled = false;
  }
  btn.addEventListener('click', dump);
  ta.addEventListener('keydown', function(ev){
    /* Dave 2026-10-16: plain Return dumps, like the button. Shift+Return for a newline. */
    if (ev.key === 'Enter' && !ev.shiftKey && !ev.altKey) { ev.preventDefault(); dump(); }
  });
  resolveRepo().then(refreshUI);
})();
</script>
"""

# ---------------------------------------------------------------------------
# Name sync: every page re-reads the registry on load so a global rename in
# the dashboard info panel shows up here without a rebuild (Dave 2026-10-16).
# Elements carrying data-buddy-name are patched; baked-in names are the
# offline fallback if the fetch fails.
# ---------------------------------------------------------------------------
FILES_CSS = """
/* ---- Repo files (Dave 2026-10-20): view + edit the buddy's repo markdown ---- */
.repo-files { margin-top: 8px; }
.rf-sub { color: var(--muted); font-size: 14px; margin-bottom: 12px; }
.rf-locked { background: var(--card); border: 1px dashed var(--border); border-radius: 8px; padding: 14px 16px; color: var(--muted); font-size: 14px; }
.rf-list { display: flex; flex-direction: column; gap: 8px; }
.rf-file { display: flex; align-items: center; gap: 10px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; cursor: pointer; text-align: left; width: 100%; color: var(--text); font: inherit; -webkit-tap-highlight-color: transparent; }
.rf-file:hover { border-color: var(--accent); }
.rf-file .rf-name { font-weight: 600; font-size: 15px; }
.rf-file .rf-dir { color: var(--muted); font-size: 13px; margin-left: auto; word-break: break-all; text-align: right; }
.rf-view, .rf-editor { margin-top: 14px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
.rf-viewhead { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.rf-path { font-weight: 700; font-size: 14px; margin-right: auto; word-break: break-all; }
.rf-body { font-size: 15px; }
.rf-body h2 { font-size: 21px; margin: 16px 0 8px; }
.rf-body h3 { font-size: 18px; margin: 14px 0 6px; }
.rf-body h4 { font-size: 16px; margin: 12px 0 6px; }
.rf-body p { margin: 6px 0; }
.rf-body ul { margin: 6px 0 6px 20px; }
.rf-body blockquote { border-left: 3px solid var(--border); padding-left: 12px; color: var(--muted); margin: 8px 0; }
.rf-body code { background: var(--bg); border: 1px solid var(--border); border-radius: 4px; padding: 0 4px; font-size: 13px; }
.rf-body pre { background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 12px; overflow-x: auto; margin: 8px 0; }
.rf-body pre code { border: none; padding: 0; background: none; }
.rf-body a { color: var(--accent); }
.rf-body hr { border: none; border-top: 1px solid var(--border); margin: 14px 0; }
.rf-ta { width: 100%; box-sizing: border-box; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 8px; padding: 12px; font-family: ui-monospace, Menlo, monospace; font-size: 13px; line-height: 1.55; }
/* ---- Accordion files (Dave 2026-10-21): the list of markdown files;
   clicking a file name opens its contents inline right below that name.
   Every file toggles independently — several can be open at once — and
   Edit lives inside the opened panel. ---- */
.rf-files-wrap { display: flex; flex-direction: column; gap: 8px; }
.rf-fileitem { display: flex; flex-direction: column; }
.rf-file .rf-chev { color: var(--muted); font-size: 13px; flex: none; }
.rf-panel { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-top: 8px; }
.rf-panel .rf-viewhead { margin-bottom: 8px; }
.rf-loading { color: var(--muted); font-size: 14px; }
.rf-panel .rf-editor { margin-top: 4px; }
.rf-panel .rf-fstatus { margin-top: 8px; }
"""

FILES_HTML = """
<section class="repo-files" data-buddy-id="__BID__">
<h2>📄 Repo files</h2>
<p class="rf-sub">The markdown files in <span data-buddy-name>__BNAME__</span>'s repo. Tap a file name and its contents open right below it — open as many as you like at once. Edit inside an opened file and the save goes straight back to GitHub. The repo is private, so nothing here — not even the file names — is shown until GitHub is connected on this device.</p>
<div class="rf-locked" hidden>🔒 Connect GitHub in the 🧠 Brain dump box above to view and edit files — the repos are private, so a token is needed to read them. Then reload this page.</div>
<div class="rf-main" hidden>
<div class="rf-list rf-files-wrap"></div>
<div class="rf-status attn-status" role="status"></div>
</div>
</section>
"""

FILES_JS = """
<script>
(function(){
  var sec = document.querySelector('.repo-files');
  if (!sec || sec.dataset.rfInit) return;
  sec.dataset.rfInit = '1';
  var bid = sec.getAttribute('data-buddy-id') || (function(){
    var p = location.pathname.replace(/\\/+$/, '');
    return p.substring(p.lastIndexOf('/') + 1);
  })();
  function lsGet(){ try { return JSON.parse(localStorage.getItem('buddyTree.v3') || '{}'); } catch(e){ return {}; } }
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
  var repo = null;
  async function resolveRepo(){
    try {
      var r = await fetch('../buddies.json', {cache: 'no-store'});
      var d = await r.json();
      var buds = d.buddies || [];
      for (var i = 0; i < buds.length; i++) {
        if (buds[i].id === bid && buds[i].repo) { repo = buds[i].repo; break; }
      }
    } catch(e){}
  }
  function esc(s){ return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function inline(s){
    s = esc(s);
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*])\\*([^*\\n]+)\\*/g, '$1<em>$2</em>');
    s = s.replace(/\\[([^\\]]+)\\]\\((https?:[^)\\s]+)\\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return s;
  }
  function mdRender(src){
    var lines = src.split('\\n'), out = [], inList = false, inCode = false, codeBuf = [];
    function closeList(){ if (inList) { out.push('</ul>'); inList = false; } }
    for (var i = 0; i < lines.length; i++){
      var ln = lines[i], m;
      if (/^```/.test(ln)) {
        if (inCode) { out.push('<pre><code>' + esc(codeBuf.join('\\n')) + '</code></pre>'); codeBuf = []; inCode = false; }
        else { closeList(); inCode = true; }
        continue;
      }
      if (inCode) { codeBuf.push(ln); continue; }
      if ((m = ln.match(/^(#{1,4})\\s+(.*)/))) {
        closeList();
        var lv = Math.min(m[1].length + 1, 4);
        out.push('<h' + lv + '>' + inline(m[2]) + '</h' + lv + '>');
        continue;
      }
      if (/^\\s*(-{3,}|\\*{3,})\\s*$/.test(ln)) { closeList(); out.push('<hr>'); continue; }
      if ((m = ln.match(/^\\s*[-*]\\s+(.*)/)) || (m = ln.match(/^\\s*\\d+[.)]\\s+(.*)/))) {
        if (!inList) { out.push('<ul>'); inList = true; }
        out.push('<li>' + inline(m[1]) + '</li>');
        continue;
      }
      if ((m = ln.match(/^>\\s?(.*)/))) { closeList(); out.push('<blockquote>' + inline(m[1]) + '</blockquote>'); continue; }
      if (!ln.trim()) { closeList(); continue; }
      closeList();
      out.push('<p>' + inline(ln) + '</p>');
    }
    closeList();
    if (inCode) out.push('<pre><code>' + esc(codeBuf.join('\\n')) + '</code></pre>');
    return out.join('\\n');
  }
  var locked = sec.querySelector('.rf-locked'), main = sec.querySelector('.rf-main'),
      list = sec.querySelector('.rf-list'), st = sec.querySelector('.rf-status');
  /* Accordion files (Dave 2026-10-21): a list of file names; clicking a
     name toggles that file's contents open inline right below the name.
     Toggles are independent — several files can be open at once. Contents
     load lazily on first open and are cached in the item's own state;
     Edit/Save lives inside the opened panel. */
  function buildFileSection(f){
    var wrap = document.createElement('div');
    wrap.className = 'rf-fileitem';
    var head = document.createElement('button');
    head.type = 'button';
    head.className = 'rf-file';
    head.setAttribute('aria-expanded', 'false');
    var nm = document.createElement('span');
    nm.className = 'rf-name';
    nm.textContent = '📄 ' + f.name;
    var dir = document.createElement('span');
    dir.className = 'rf-dir';
    dir.textContent = f.path;
    var chev = document.createElement('span');
    chev.className = 'rf-chev';
    chev.textContent = '▸';
    head.appendChild(nm);
    head.appendChild(dir);
    head.appendChild(chev);
    var panel = document.createElement('div');
    panel.className = 'rf-panel';
    panel.hidden = true;
    var phead = document.createElement('div');
    phead.className = 'rf-viewhead';
    var ppath = document.createElement('span');
    ppath.className = 'rf-path';
    ppath.textContent = f.path;
    var editBtn = document.createElement('button');
    editBtn.type = 'button';
    editBtn.className = 'attn-btn rf-edit';
    editBtn.textContent = 'Edit';
    editBtn.disabled = true;
    phead.appendChild(ppath);
    phead.appendChild(editBtn);
    var bodyEl = document.createElement('div');
    bodyEl.className = 'rf-body';
    bodyEl.innerHTML = '<p class="rf-loading">Loading ' + esc(f.path) + '…</p>';
    var editor = document.createElement('div');
    editor.className = 'rf-editor';
    editor.hidden = true;
    var ta = document.createElement('textarea');
    ta.className = 'rf-ta';
    ta.rows = 18;
    ta.spellcheck = false;
    ta.setAttribute('aria-label', 'Markdown source for ' + f.path);
    var actions = document.createElement('div');
    actions.className = 'attn-actions';
    var saveBtn = document.createElement('button');
    saveBtn.type = 'button';
    saveBtn.className = 'attn-btn primary rf-save';
    saveBtn.textContent = 'Save to GitHub';
    var cancelBtn = document.createElement('button');
    cancelBtn.type = 'button';
    cancelBtn.className = 'attn-btn rf-cancel';
    cancelBtn.textContent = 'Cancel';
    actions.appendChild(saveBtn);
    actions.appendChild(cancelBtn);
    editor.appendChild(ta);
    editor.appendChild(actions);
    var fst = document.createElement('div');
    fst.className = 'rf-fstatus attn-status';
    fst.setAttribute('role', 'status');
    panel.appendChild(phead);
    panel.appendChild(bodyEl);
    panel.appendChild(editor);
    panel.appendChild(fst);
    wrap.appendChild(head);
    wrap.appendChild(panel);
    var cur = null, loaded = false;
    function loadOnce(){
      if (loaded) return;
      loaded = true;
      ghGetFile(repo, f.path).then(function(got){
        if (!got) { loaded = false; bodyEl.innerHTML = '<p class="rf-loading">⚠ Could not load ' + esc(f.path) + ' — close and open it again to retry.</p>'; return; }
        cur = {path: f.path, sha: got.sha, text: got.text};
        bodyEl.innerHTML = mdRender(got.text);
        editBtn.disabled = false;
      });
    }
    head.addEventListener('click', function(){
      var open = panel.hidden;
      panel.hidden = !open;
      head.setAttribute('aria-expanded', open ? 'true' : 'false');
      chev.textContent = open ? '▾' : '▸';
      if (open) loadOnce();
    });
    editBtn.addEventListener('click', function(){
      if (!cur) return;
      ta.value = cur.text;
      bodyEl.hidden = true;
      editor.hidden = false;
      ta.focus();
    });
    cancelBtn.addEventListener('click', function(){
      editor.hidden = true;
      bodyEl.hidden = false;
    });
    saveBtn.addEventListener('click', async function(){
      if (!cur) return;
      saveBtn.disabled = true;
      fst.textContent = 'Saving…';
      try {
        var payload = {message: 'Edit ' + cur.path + ' from the homepage', content: b64encode(ta.value), sha: cur.sha};
        var j = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + cur.path, 'PUT', payload);
        if (j && j.content && j.content.sha) cur.sha = j.content.sha;
        cur.text = ta.value;
        editor.hidden = true;
        bodyEl.hidden = false;
        bodyEl.innerHTML = mdRender(cur.text);
        fst.textContent = '✓ Saved to GitHub (' + repo + '/' + cur.path + ').';
      } catch(err){
        var why = (err && err.message) || String(err);
        fst.textContent = /409|422/.test(why)
          ? '⚠ GitHub said the file changed since you loaded it (' + why + ') — reload this page and try again.'
          : '⚠ Save failed (' + why + ') — your edit is still in the editor.';
      }
      saveBtn.disabled = false;
    });
    return wrap;
  }
  async function init(){
    await resolveRepo();
    if (!repo) {
      locked.hidden = false;
      locked.textContent = 'No repo is linked for this buddy yet, so there are no repo files to show.';
      return;
    }
    if (!token()) { locked.hidden = false; return; }
    main.hidden = false;
    st.textContent = 'Loading files…';
    var files = [];
    async function grab(dir){
      try {
        var j = await ghApi('/repos/davedellaquila/' + repo + (dir ? '/contents/' + dir : '/contents'));
        if (Array.isArray(j)) j.forEach(function(e){
          if (e.type === 'file' && /\\.md$/i.test(e.name)) files.push({name: e.name, path: e.path});
        });
      } catch(e){}
    }
    await grab('');
    await grab('docs');
    files.sort(function(a, b){ return a.path < b.path ? -1 : 1; });
    if (!files.length) { st.textContent = 'No markdown files found in the repo yet.'; return; }
    st.textContent = '';
    files.forEach(function(f){
      list.appendChild(buildFileSection(f));
    });
  }
  init();
})();
</script>
"""

NAMESYNC_JS = """
<script>
(function(){
  var parts = location.pathname.split('/');
  var bid = '';
  for (var i = parts.length - 1; i >= 0; i--) { if (parts[i]) { bid = parts[i]; break; } }
  function applyName(name){
    if (!name) return;
    var els = document.querySelectorAll('[data-buddy-name]');
    for (var k = 0; k < els.length; k++) els[k].textContent = name;
    var ta = document.querySelector('.dumpbox textarea');
    if (ta) ta.setAttribute('placeholder', "Dump what's on your mind about " + name + "…");
  }
  /* Pending renames (Dave 2026-10-18): when the dashboard has no GitHub token,
     a rename queues in localStorage instead of reaching the registry. The
     dashboard and homepages share an origin, so the homepage reads that queue
     here — a pending rename supersedes the registry name, which is why a freshly
     renamed buddy kept showing its old name after refresh. */
  function pendingName(){
    try {
      var s = JSON.parse(localStorage.getItem('buddyTree.v3') || '{}');
      if (s && s.pendingRenames && s.pendingRenames[bid]) return s.pendingRenames[bid];
    } catch(e){}
    return null;
  }
  var pn = pendingName();
  if (pn) applyName(pn);
  try {
    fetch('../buddies.json', {cache: 'no-store'}).then(function(r){ return r.json(); }).then(function(d){
      var buds = (d && d.buddies) || [];
      for (var j = 0; j < buds.length; j++) {
        if (buds[j].id === bid && buds[j].name) { applyName(pendingName() || buds[j].name); break; }
      }
    }).catch(function(){});
  } catch(e){}
  /* Live rename (Dave 2026-10-16): the dashboard broadcasts renames via
     localStorage, so an open page updates its name without a refresh.
     Same browser only — other devices pick it up on their next load. */
  window.addEventListener('storage', function(e){
    if (e.key !== 'buddyTree.rename' || !e.newValue) return;
    try {
      var d = JSON.parse(e.newValue);
      if (d && d.id === bid && d.name) applyName(d.name);
    } catch(err){}
  });
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
  function isResolved(aid, text){
    var s = lsGet();
    var m = s.attnDone || {};
    if (m[rkey(aid, text)]) return true;
    /* Also honor the dashboard's own done map (the same store's 'seen',
       keyed by bare attention id) so an item cleared in the dashboard
       stays cleared here — one done state across surfaces. */
    if (aid && s.seen && s.seen[aid]) return true;
    return false;
  }
  function setResolved(aid, text){ var s = lsGet(); var m = s.attnDone || {}; m[rkey(aid, text)] = 1; s.attnDone = m; lsSet(s); }
  /* Las Vegas mode (Dave 2026-10-20): marking done feels like a win — the
     button spins once and confetti bursts from it. DOM + WAAPI only;
     skipped under prefers-reduced-motion; only ever called on a real tap. */
  function celebrate(el, fallbackEl){
    if (!el || !el.getBoundingClientRect) return;
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    try { el.animate([{transform:'rotate(0deg)'},{transform:'rotate(360deg)'}], {duration:450, easing:'cubic-bezier(.2,.7,.3,1.2)'}); } catch(e){}
    var r = el.getBoundingClientRect();
    /* A hidden element's rect is all zeros — bursting from it put the
       confetti in the viewport's upper-left corner (Dave, 2026-10-21). Fall
       back to the tile's rect; never burst from a zero rect at all. */
    if ((!r.width || !r.height) && fallbackEl && fallbackEl.getBoundingClientRect) r = fallbackEl.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var cx = r.left + r.width/2, cy = r.top + r.height/2;
    var colors = ['#f0b429','#3fb950','#f778ba','#58a6ff','#ff7b72','#d2a8ff'];
    for (var i = 0; i < 26; i++){
      var s = document.createElement('span');
      var sz = 5 + Math.random()*6;
      s.style.cssText = 'position:fixed;left:'+cx+'px;top:'+cy+'px;width:'+sz+'px;height:'+(sz*0.6)+'px;background:'+colors[i%colors.length]+';z-index:99999;pointer-events:none;border-radius:2px;';
      document.body.appendChild(s);
      var ang = Math.random()*Math.PI*2, v = 60 + Math.random()*130;
      var dx = Math.cos(ang)*v, dy = Math.sin(ang)*v - 90;
      var anim = s.animate([
        {transform:'translate(-50%,-50%) rotate(0deg)', opacity:1},
        {transform:'translate(calc(-50% + '+dx+'px), calc(-50% + '+(dy+170)+'px)) rotate('+(Math.random()*540-270)+'deg)', opacity:0}
      ], {duration: 750 + Math.random()*450, easing:'cubic-bezier(.15,.6,.4,1)'});
      (function(node, a){ if (a) a.onfinish = function(){ node.remove(); }; else setTimeout(function(){ node.remove(); }, 1300); })(s, anim);
    }
  }
  function paintResolved(tile, msg, immediate){
    var st = tile.querySelector('.attn-status');
    if (st) st.textContent = msg;
    /* Dave 2026-10-20: the check belongs to the RESULT of the tap, never the
       label beforehand — an upfront check reads as "already done." The Done
       button renders plain "Done"; the check appears only once clicked. */
    var db = tile.querySelector('[data-act="done"]');
    if (db) db.textContent = '✓ Done';
    if (immediate) { tile.classList.add('resolved'); return; }
    /* Fresh tap (Dave, 2026-10-21): the check + status land while the button
       is still visible, and celebrate() fires against the live button; the
       resolved class (dim + hide actions) arrives a beat later so the result
       registers first. Applying it instantly hid the button before the check
       could be seen — and zeroed the rect celebrate() measures, which sent
       the confetti to the viewport's upper-left corner. */
    setTimeout(function(){ tile.classList.add('resolved'); }, 1100);
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
    if (isResolved(aid, text)) { paintResolved(tile, 'Marked done', true); return; }
    tile.addEventListener('click', function(ev){
      var btn = ev.target.closest ? ev.target.closest('.attn-btn') : null;
      if (!btn || btn.disabled) return;
      var act = btn.getAttribute('data-act');
      var idBit = aid ? ' (attention id: ' + aid + ')' : '';
      if (act === 'done') {
        sendAction(tile,
          'DONE — Dave marked this done on the homepage: "' + text + '"' + idBit + '. Please remove it from the attention list in buddies.json.',
          'Marked done — the buddy will clear it.').then(function(ok){ if (ok) { setResolved(aid, text); paintResolved(tile, 'Marked done — the buddy will clear it.'); celebrate(btn, tile); } });
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
<meta name="robots" content="noindex, nofollow">
<title data-buddy-name>{name}</title>
<style>
:root {{
  --bg: #ffffff;
  --text: #1a1a1a;
  --muted: #666;
  --card: #f5f5f5;
  --border: #e0e0e0;
  --accent: #0066cc;
  --ok: #1b7a2e;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #1a1a1a;
    --text: #e0e0e0;
    --muted: #999;
    --card: #2a2a2a;
    --border: #3a3a3a;
    --accent: #4da6ff;
    --ok: #5fd08a;
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
.topbar-refresh {{
  margin-left: auto; background: none; border: 1px solid transparent; border-radius: 8px;
  color: var(--muted); font-size: 16px; cursor: pointer; padding: 4px 10px; line-height: 1;
}}
.topbar-refresh:hover {{ color: var(--text); border-color: var(--border); }}
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
.attn-link {{ margin-top: 8px; }}
.attn-link a {{ color: var(--accent); font-weight: 600; text-decoration: none; }}
.attn-link a:hover {{ text-decoration: underline; }}
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
/* ---- skills (Dave 2026-10-16) ---- */
.skills {{ display: flex; flex-direction: column; gap: 10px; margin-top: 4px; }}
.skill {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px; }}
.skill-name {{ font-weight: 700; font-size: 15px; }}
.skill-evidence {{ color: var(--muted); font-size: 13px; margin-top: 4px; line-height: 1.45; }}
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
/* Dave 2026-10-16: photo gallery — baked in at generation time from the buddy's repo photos/ */
.gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-bottom: 8px; }}
.gallery a {{ display: block; border-radius: 12px; overflow: hidden; border: 1px solid var(--border); background: var(--card); }}
.gallery img {{ width: 100%; height: 160px; object-fit: cover; display: block; transition: transform .25s ease; }}
.gallery a:hover img {{ transform: scale(1.04); }}
.lightbox {{ position: fixed; inset: 0; z-index: 1000; display: flex; align-items: center; justify-content: center; }}
.lightbox[hidden] {{ display: none; }}
.lightbox-bg {{ position: absolute; inset: 0; background: rgba(0,0,0,.88); }}
.lightbox-img {{ position: relative; max-width: 92vw; max-height: 88vh; border-radius: 12px; box-shadow: 0 24px 64px rgba(0,0,0,.5); }}
.lightbox-x {{ position: absolute; top: 16px; right: 20px; background: rgba(255,255,255,.12); color: #fff; border: none; border-radius: 50%; width: 44px; height: 44px; font-size: 26px; cursor: pointer; line-height: 1; }}
{dumpbox_css}
{files_css}
</style>
</head>
<body>
{family_nav}
<div class="topbar"><span class="topbar-icon">{icon}</span><span class="topbar-name" data-buddy-name>{name}</span><button class="topbar-refresh" title="Reload this page (bypasses cache)" onclick="location.href=location.pathname+'?v='+Date.now()">&#8635;</button></div>
<div class="header">
<div class="icon">{icon}</div>
<h1 data-buddy-name>{name}</h1>
<div class="tagline">{tagline}</div>
</div>

<div class="mission">{mission}</div>

{gallery_section}

{dumpbox_html}

{attention_section}

{skills_section}

{children_section}

{repo_files_section}

<div class="footer">
Generated {date} · Part of the Buddy System<br>
<a href="about.html">About · the full record →</a>
</div>
{dumpbox_js}
{attn_js}
{files_js}
{namesync_js}
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
    # The CUSTOM HOMEPAGE marker always wins (Dave 2026-10-15): thread-owned
    # custom designs are never overwritten, even if they kept a v1-style
    # "Part of the Buddy System" footer (this misclassified Finance Buddy's
    # custom page and it got clobbered on regen — restored from git).
    if 'CUSTOM HOMEPAGE' in content:
        return False
    # DEFAULT-HOMEPAGE v3 "Dossier" pages are a newer default treatment, not
    # basic-template pages — never regenerate them with the basic template
    # even though their footer carries the "Part of the Buddy System"
    # signature (misclassification caught in the 2026-10-20 daily rebuild;
    # the 9 affected pages were restored before commit).
    if 'DEFAULT-HOMEPAGE' in content:
        return False
    return ('BUDDY-BASIC-TEMPLATE' in content) or ('Part of the Buddy System' in content)



# Photo cache so we don't hammer the GitHub API
_photo_cache = {}
def get_buddy_photos(b):
    """Return list of photo URLs for a buddy: registry seeds + repo photos/ folder."""
    bid = b['id']
    if bid in _photo_cache:
        return _photo_cache[bid]
    urls = list(b.get('photos') or [])
    seen = set(urls)
    # Dave 2026-10-16: prefer the PUBLIC buddy-system/photos/<id>/ copies — the
    # buddy repo is often private, and its API download_urls carry expiring
    # ?token= params that 404 for page viewers. Public raw URLs just work.
    try:
        import subprocess, json as _json
        out = subprocess.run(['gh', 'api', f'repos/davedellaquila/buddy-system/contents/photos/{bid}'],
                             capture_output=True, text=True, timeout=15)
        if out.returncode == 0:
            files = _json.loads(out.stdout)
            for fl in files if isinstance(files, list) else []:
                if fl.get('type') == 'file':
                    # Build a clean public raw URL (no token params)
                    u = f"https://raw.githubusercontent.com/davedellaquila/buddy-system/master/photos/{bid}/{fl.get('name')}"
                    if u not in seen:
                        urls.append(u); seen.add(u)
    except Exception:
        pass
    # Fall back to the buddy's own repo photos/ (may be private — URLs can 404)
    repo = b.get('repo')
    if repo:
        try:
            import subprocess, json as _json
            out = subprocess.run(['gh', 'api', f'repos/davedellaquila/{repo}/contents/photos'],
                                 capture_output=True, text=True, timeout=15)
            if out.returncode == 0:
                files = _json.loads(out.stdout)
                for fl in files if isinstance(files, list) else []:
                    if fl.get('type') == 'file':
                        u = fl.get('download_url', '').split('?')[0]
                        if u and u not in seen:
                            urls.append(u); seen.add(u)
        except Exception:
            pass
    _photo_cache[bid] = urls
    return urls

def ensure_thumb(local_path):
    """Create a 480px thumbnail for a local photo if missing. Returns thumb path or None."""
    import os as _os
    d, f = _os.path.split(local_path)
    tdir = _os.path.join(d, 'thumbs')
    tpath = _os.path.join(tdir, f)
    if _os.path.exists(tpath):
        return tpath
    try:
        from PIL import Image
        _os.makedirs(tdir, exist_ok=True)
        img = Image.open(local_path)
        img.thumbnail((480, 480), Image.LANCZOS)
        img.save(tpath, 'JPEG', quality=82, optimize=True)
        return tpath
    except Exception:
        return None

def build_gallery(b):
    """Build the gallery HTML section, or '' if no photos.
    Dave 2026-10-16: thumbnails in the grid (fast), full image in the lightbox on tap."""
    urls = get_buddy_photos(b)
    if not urls:
        return ''
    import html as _html, os as _os
    name = _html.escape(b.get('name', b['id']))
    base_dir = _os.path.dirname(_os.path.abspath(__file__))
    prefix = 'https://raw.githubusercontent.com/davedellaquila/buddy-system/master/'
    items = []
    for u in urls:
        thumb_u = u
        if u.startswith(prefix):
            rel = u[len(prefix):]
            local = _os.path.join(base_dir, rel)
            tpath = ensure_thumb(local)
            if tpath:
                trel = _os.path.relpath(tpath, base_dir)
                thumb_u = prefix + trel
        items.append(
            '<a href="' + _html.escape(u) + '" class="g-item" data-full="' + _html.escape(u) + '">'
            '<img src="' + _html.escape(thumb_u) + '" alt="' + name + ' photo" loading="lazy"></a>')
    items_html = chr(10).join(items)
    return (
        '<h2>Photos</h2>' + chr(10)
        + '<div class="gallery">' + chr(10) + items_html + chr(10) + '</div>' + chr(10)
        + '<div class="lightbox" hidden>' + chr(10)
        + '  <div class="lightbox-bg"></div>' + chr(10)
        + '  <img class="lightbox-img" alt="">' + chr(10)
        + '  <button class="lightbox-x" aria-label="Close">&times;</button>' + chr(10)
        + '</div>' + chr(10)
        + '<script>' + chr(10)
        + '(function(){' + chr(10)
        + "  var items = document.querySelectorAll('.g-item');" + chr(10)
        + "  var lb = document.querySelector('.lightbox');" + chr(10)
        + '  if (!lb) return;' + chr(10)
        + "  var img = lb.querySelector('.lightbox-img');" + chr(10)
        + '  items.forEach(function(a){' + chr(10)
        + '    a.addEventListener("click", function(e){' + chr(10)
        + '      e.preventDefault();' + chr(10)
        + '      img.src = a.getAttribute("data-full");' + chr(10)
        + '      lb.hidden = false;' + chr(10)
        + "      document.body.style.overflow = 'hidden';" + chr(10)
        + '    });' + chr(10)
        + '  });' + chr(10)
        + '  function close(){ lb.hidden = true; img.src=""; document.body.style.overflow=""; }' + chr(10)
        + '  lb.querySelector(".lightbox-bg").addEventListener("click", close);' + chr(10)
        + '  lb.querySelector(".lightbox-x").addEventListener("click", close);' + chr(10)
        + '  document.addEventListener("keydown", function(e){ if(e.key==="Escape" && !lb.hidden) close(); });' + chr(10)
        + '})();' + chr(10)
        + '</scr' + 'ipt>'
    )

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
            url = html.escape(a.get('url', '') if isinstance(a, dict) else '', quote=True)
            attn_html += f'<div class="attn" data-attn-id="{aid}"><div class="attn-text">{text}</div>'
            if url:
                attn_html += f'<div class="attn-link"><a href="{url}" target="_blank" rel="noopener">Open →</a></div>'
            if date:
                attn_html += f'<div class="attn-date">{date}</div>'
            attn_html += ('<div class="attn-actions">'
                          '<button type="button" class="attn-btn primary" data-act="done">Done</button>'
                          '<button type="button" class="attn-btn" data-act="info">Need more info</button>'
                          '</div><div class="attn-status" role="status"></div></div>\n')
        attention_section = attn_html
    else:
        attention_section = '<h2>Needs Attention</h2>\n<p class="empty">Nothing needs attention right now.</p>'

    # Skills — rendered when the buddy has a skills[] list (Dave 2026-10-16)
    skills_items = b.get('skills', [])
    if skills_items:
        skills_html = '<h2>Skills</h2>\n<div class="skills">\n'
        for s in skills_items:
            sname = html.escape(s.get('name', '') if isinstance(s, dict) else str(s))
            sev = html.escape(s.get('evidence', '') if isinstance(s, dict) else '')
            skills_html += f'<div class="skill"><div class="skill-name">{sname}</div>'
            if sev:
                skills_html += f'<div class="skill-evidence">{sev}</div>'
            skills_html += '</div>\n'
        skills_html += '</div>\n'
        skills_section = skills_html
    else:
        skills_section = ''

    # Children — multi-parent aware (Dave 2026-10-15)
    children = [by_id[cid] for cid in b.get('children', []) if cid in by_id]
    # Also find buddies with this as parent (parents[] or legacy parent)
    kids = [x for x in d['buddies'] if bid in eff_parents(x)]
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
    repo_files_html = FILES_HTML.replace('__BID__', bid).replace('__BNAME__', name)

    gallery_section = build_gallery(b)

    page = TEMPLATE.format(
        name=name,
        icon=icon,
        tagline=tagline,
        mission=mission,
        family_nav=family_nav(b),
        attention_section=attention_section,
        skills_section=skills_section,
        children_section=children_section,
        date=today,
        gallery_section=gallery_section,
        dumpbox_css=DUMPBOX_CSS,
        dumpbox_html=dumpbox_html,
        dumpbox_js=DUMPBOX_JS,
        attn_js=ATTN_JS,
        files_css=FILES_CSS,
        repo_files_section=repo_files_html,
        files_js=FILES_JS,
        namesync_js=NAMESYNC_JS,
    )

    # Tip jar (Dave's standing rule, 2026-10-24; generator wiring 2026-10-27):
    # every generated page carries the canonical snippet, read live from
    # docs/tipjar-snippet.html so the fleet never drifts from the canonical copy.
    if 'class="tipjar"' not in page:
        try:
            with open(os.path.join(HERE, 'docs', 'tipjar-snippet.html'), encoding='utf-8') as _tf:
                page = page.replace('</body>', _tf.read().strip('\n') + '\n</body>')
        except OSError:
            pass

    # Write to <bid>/index.html
    os.makedirs(dirpath, exist_ok=True)
    with open(idxpath, 'w') as f:
        f.write(page)

    # Update buddies.json
    b['homepage'] = f'{bid}/'
    generated.append(bid)
    print(f"Generated {bid}/index.html")

with open('buddies.json', 'w') as f:
    # Match the file's existing format exactly (indent=2, literal UTF-8)
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f"\nDone: {len(generated)} pages generated")

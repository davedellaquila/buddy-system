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
import re
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def _tipjar_parts():
    """Canonical Tip Jar (docs/tipjar-snippet.html): returns (style_block, anchor)
    for the HEADER placement (Dave 2026-10-28) — a compact bug in the page's
    header row, superseding the retired floating pill. ('', '') if unreadable."""
    try:
        txt = open(os.path.join(HERE, 'docs', 'tipjar-snippet.html'), encoding='utf-8').read()
    except OSError:
        return '', ''
    txt = re.sub(r'<!--.*?-->', '', txt, flags=re.S)  # strip comments first: the
    # usage prose itself mentions <style>/<a> and must not poison extraction
    m = re.search(r'<style>.*?</style>', txt, re.S)
    style = m.group(0) if m else ''
    anchor = ''
    for line in txt.splitlines():
        if 'class="header-tip"' in line and line.strip().startswith('<a '):
            anchor = line.strip()
            break
    return style, anchor

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
.dumpbox-addimg {
  background: transparent; color: var(--text); border: 1px solid var(--border);
  border-radius: 8px; padding: 8px 16px; font-size: 14px; font-weight: 600; cursor: pointer;
}
.dumpbox-addimg:hover { border-color: var(--accent); color: var(--accent); }
.dumpbox-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.dumpbox-chips:empty { display: none; }
.dumpbox-chip {
  display: inline-flex; align-items: center; gap: 7px; background: var(--card);
  border: 1px solid var(--border); border-radius: 8px; padding: 4px 6px 4px 4px;
  font-size: 12px; max-width: 100%;
}
.dumpbox-chip img { width: 32px; height: 32px; object-fit: cover; border-radius: 5px; }
.dumpbox-chip .dc-name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 140px; }
.dumpbox-chip .dc-x { background: none; border: 0; color: var(--muted); cursor: pointer; font-size: 14px; line-height: 1; padding: 4px; }
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
<div class="dumpbox-chips"></div>
<button type="button" class="dumpbox-btn">Dump it</button>
<button type="button" class="dumpbox-addimg">\U0001f5bc\ufe0f Add image</button>
<span class="dumpbox-status" role="status"></span>
</div>
<p class="dumpbox-hint">Enter dumps it &middot; Shift+Enter for a new line &middot; Images shrink to 1600px wide before upload \u2014 the original stays in your library</p>
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
      tokWrap = box.querySelector('.dumpbox-token'),
      chipsBox = box.querySelector('.dumpbox-chips'),
      addBtn = box.querySelector('.dumpbox-addimg');
  /* Image attachments (Dave 2026-11-08): picked photos shrink on the device
     first (<=1600px JPEG; the original stays in the Photos library), then
     ride the dump into the buddy's repo under docs/ingest-files/<ts>/ and
     are listed with links in the ingest entry \u2014 the same mechanics as the
     dashboard's Universal Dump files. */
  var dumpFiles = [];
  function lsGet(){ try { return JSON.parse(localStorage.getItem('buddyTree.v3') || '{}'); } catch(e){ return {}; } }
  function lsSet(patch){ try { var s = lsGet(); for (var k in patch) s[k] = patch[k]; localStorage.setItem('buddyTree.v3', JSON.stringify(s)); } catch(e){} }
  function token(){ return lsGet().ghToken || ''; }
  function b64OfBlob(blob){
    return new Promise(function(res, rej){
      var fr = new FileReader();
      fr.onload = function(){ res(String(fr.result).split(',')[1]); };
      fr.onerror = rej;
      fr.readAsDataURL(blob);
    });
  }
  function loadHeic(){
    return new Promise(function(res, rej){
      if (window.heic2any) return res();
      var sc = document.createElement('script');
      sc.src = 'https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js';
      sc.onload = res; sc.onerror = rej;
      document.head.appendChild(sc);
    });
  }
  var DUMP_FILE_MAX = 1024 * 1024;
  function fmtSize(n){ return n >= 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB'; }
  async function shrinkImage(file){
    var blob = file;
    if (/\\\\.hei[cf]$/i.test(file.name || '') || file.type === 'image/heic' || file.type === 'image/heif') {
      await loadHeic();
      blob = await window.heic2any({blob: file, toType: 'image/jpeg', quality: 0.92});
    }
    var bmp = await createImageBitmap(blob);
    var scale = Math.min(1, 1600 / Math.max(bmp.width, bmp.height));
    var out = blob, outName = file.name || 'image.jpg';
    if (scale < 1 || !/jpe?g$/i.test(blob.type || '')) {
      var c = document.createElement('canvas');
      c.width = Math.max(1, Math.round(bmp.width * scale));
      c.height = Math.max(1, Math.round(bmp.height * scale));
      c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height);
      var jb = await new Promise(function(res){ c.toBlob(res, 'image/jpeg', 0.85); });
      if (jb) { out = jb; outName = outName.replace(/\\\\.[^.]+$/, '') + '.jpg'; }
    }
    if (bmp.close) bmp.close();
    return { name: outName, type: 'image/jpeg', b64: await b64OfBlob(out), size: out.size };
  }
  async function prepareImages(fileList, notes){
    var list = Array.prototype.slice.call(fileList || []).filter(function(f){ return f.type.indexOf('image/') === 0 || /\\\\.hei[cf]$/i.test(f.name || ''); });
    var out = [];
    for (var i = 0; i < list.length; i++) {
      var f = list[i];
      try {
        var rec = await shrinkImage(f);
        if (rec.size > DUMP_FILE_MAX) { notes.push('\u201c' + rec.name + '\u201d is still ' + fmtSize(rec.size) + ' after shrinking \u2014 over the 1 MB upload limit, so it was not attached.'); continue; }
        out.push(rec);
      } catch(e) { notes.push('\u201c' + (f.name || 'image') + '\u201d could not be prepared \u2014 not attached.'); }
    }
    return out;
  }
  function fileSlug(name){ return String(name || 'file').replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^-+|-+$/g, '') || 'file'; }
  function folderOf(t){
    var d = new Date(t), z = function(n){ return String(n).padStart(2, '0'); };
    return d.getFullYear() + z(d.getMonth() + 1) + z(d.getDate()) + '-' + z(d.getHours()) + z(d.getMinutes()) + z(d.getSeconds());
  }
  function entryBody(text, paths){
    var NL = String.fromCharCode(10);
    var body = text || '';
    if (paths && paths.length) {
      if (body) body += NL + NL;
      body += 'Files:' + paths.map(function(pp){ return NL + '- [' + pp.split('/').pop() + '](https://github.com/davedellaquila/' + repo + '/blob/master/' + pp + ')'; }).join('');
    }
    return body;
  }
  async function uploadFiles(files, whenMs){
    var paths = [];
    if (!files || !files.length) return paths;
    var folder = 'docs/ingest-files/' + folderOf(whenMs) + '/';
    for (var i = 0; i < files.length; i++) {
      var path = folder + fileSlug(files[i].name);
      await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path, 'PUT',
        {message: 'Dump image for ' + bid, content: files[i].b64});
      paths.push(path);
    }
    return paths;
  }
  function escChip(t){
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function renderChips(){
    if (!chipsBox) return;
    chipsBox.innerHTML = dumpFiles.map(function(f, i){
      return '<span class="dumpbox-chip"><img alt="" src="data:' + (f.type || 'image/jpeg') + ';base64,' + f.b64 + '"><span class="dc-name">' + escChip(f.name) + '</span><button type="button" class="dc-x" data-dc-x="' + i + '" aria-label="Remove ' + escChip(f.name) + '">\u00d7</button></span>';
    }).join('');
  }
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
    try { localStorage.setItem(localKey(), JSON.stringify(a)); } catch(e){
      /* Oversize local state (queued photos can exceed the storage quota):
         keep the text, drop the image bytes, and SAY so on the status line -
         a queued dump must never vanish silently. */
      try {
        var lite = {t: entry.t, text: entry.text};
        if (entry.files && entry.files.length) lite.filesDropped = entry.files.length;
        var a2 = localBacklog(); a2.push(lite);
        localStorage.setItem(localKey(), JSON.stringify(a2));
        st.textContent = '\u26a0\ufe0f Saved on this device, but the image was too large for this device\u2019s storage \u2014 the text is queued and will sync; re-attach the image after connecting GitHub.';
      } catch(e2){}
    }
  }
  function localClear(){ try { localStorage.removeItem(localKey()); } catch(e){} }
  /* Split a local backlog entry into (text, file paths) ready for the ingest
     body: its own already-uploaded paths (first sync attempt), plus a note
     for any image that could not be kept on this device. */
  function splitEntry(b){
    var body = b.text || '';
    if (b.filesDropped) {
      var NL = String.fromCharCode(10);
      body += (body ? NL + NL : '') + '_(' + b.filesDropped + ' image' + (b.filesDropped === 1 ? '' : 's') + ' could not be kept on the device while queued \u2014 re-attach from the Photos library.)_';
    }
    return body;
  }
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
    var files = dumpFiles.slice();
    if (!text && !files.length) return;
    var stamp = new Date().toLocaleString();
    var whenMs = Date.now();
    var NL = String.fromCharCode(10);
    function clearBox(){
      ta.value = '';
      dumpFiles = [];
      renderChips();
    }
    if (!repo) {
      /* No repo linked yet — save on this device; syncs once one is linked. */
      localSave({t: stamp, text: text, files: files, when: whenMs});
      clearBox();
      refreshUI();
      if (!/too large/.test(st.textContent)) st.textContent = '\u2713 Saved on this device — will sync to the repo once one is linked.';
      flashSaved();
      return;
    }
    if (!token()) {
      /* Temporary workaround: no token → save on this device. */
      localSave({t: stamp, text: text, files: files, when: whenMs});
      clearBox();
      if (!/too large/.test(st.textContent)) st.textContent = '\u2713 Saved on this device — add a GitHub token to sync it to the repo.';
      flashSaved();
      return;
    }
    st.textContent = 'Dumping\u2026';
    btn.disabled = true;
    try {
      /* This dump's own paths, then the backlog with each entry's uploads. */
      var myPaths = await uploadFiles(files, whenMs);
      var backlog = localBacklog();
      var parts = [];
      for (var bi = 0; bi < backlog.length; bi++) {
        var b = backlog[bi];
        var bPaths = b.paths ? b.paths.slice() : await uploadFiles(b.files || [], b.when || whenMs);
        b.paths = bPaths;
        try { localStorage.setItem(localKey(), JSON.stringify(backlog)); } catch(e){}
        parts.push('## ' + b.t + NL + NL + entryBody(splitEntry(b), bPaths) + NL + NL);
      }
      parts.push('## ' + stamp + NL + NL + entryBody(text, myPaths) + NL + NL);
      var cur = await ghGetFile(repo, 'docs/ingest.md');
      var base = cur ? cur.text : '# Ingest log \u2014 ' + repoName + NL + NL;
      var body = {message: 'Ingest dump for ' + bid, content: b64encode(base + parts.join(''))};
      if (cur && cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md', 'PUT', body);
      localClear();
      clearBox();
      st.textContent = '\u2713 Dumped to ' + repo + '/docs/ingest.md' + (backlog.length ? ' (' + backlog.length + ' local synced)' : '');
      flashSaved();
    } catch(err){
      /* Dave 2026-10-18: a failed GitHub write must never drop the dump.
         Keep it on this device and say so plainly, with the backlog count —
         it syncs on the next successful dump. */
      try { localSave({t: stamp, text: text, files: files, when: whenMs}); } catch(e2){}
      clearBox();
      refreshUI();
      var why = (err && err.message) || String(err);
      var nq = 0; try { nq = localBacklog().length; } catch(e2){}
      var tail = nq > 1 ? ' (' + nq + ' on this device waiting to sync)' : '';
      st.textContent = (/404/.test(why)
        ? '\u26a0 Saved on this device — GitHub said 404 (usually a wrong/expired token, or no access to this private repo). Fix the token, then dump again to sync.'
        : '\u26a0 Saved on this device — GitHub said: ' + why + '. It will sync on your next successful dump.') + tail;
    }
    btn.disabled = false;
  }
  btn.addEventListener('click', dump);
  ta.addEventListener('keydown', function(ev){
    /* Dave 2026-10-16: plain Return dumps, like the button. Shift+Return for a newline. */
    if (ev.key === 'Enter' && !ev.shiftKey && !ev.altKey) { ev.preventDefault(); dump(); }
  });
  if (addBtn) addBtn.addEventListener('click', function(){
    var inp = document.createElement('input');
    inp.type = 'file'; inp.accept = 'image/*,.heic,.heif'; inp.multiple = true;
    inp.addEventListener('change', async function(){
      if (!inp.files || !inp.files.length) return;
      st.textContent = 'Preparing image\u2026';
      var notes = [];
      var recs = await prepareImages(inp.files, notes);
      dumpFiles = dumpFiles.concat(recs);
      renderChips();
      st.textContent = notes.join(' ') || (recs.length ? recs.length + ' image' + (recs.length === 1 ? '' : 's') + ' attached — they ride your next dump.' : '');
      if (recs.length && !ta.value.trim()) dump();
    });
    inp.click();
  });
  if (chipsBox) chipsBox.addEventListener('click', function(ev){
    var x = ev.target.closest('[data-dc-x]');
    if (!x) return;
    dumpFiles.splice(parseInt(x.getAttribute('data-dc-x'), 10), 1);
    renderChips();
  });
  resolveRepo().then(refreshUI);
})();
</script>
"""


# --- Baked repo files (Dave 2026-11-19) ------------------------------------
# The Repo files reader used to fetch contents from GitHub at view time
# with Dave's token; on a device without the token the section sat dead
# and clicking a file did nothing. The generator already reads every file
# from the local clone, so contents are now baked into the page at
# generation time: the accordion opens in place — no token, no sign-in,
# no fetch. A file that cannot be read or rendered gets a panel that
# says why instead of a dead row. Keep in step with the baked builder
# in gen_default_homepages.py.
try:
    import markdown as _markdown
except Exception:
    _markdown = None

_RF_ORDER = ['KNOWLEDGE.md', 'CONFIG.md', 'STUDY.md', 'SOUL.md', 'DECISIONS.md',
             'ACCOMPLISHMENTS.md', 'README.md']

def _rf_clone_dir(b):
    repo = (b.get('repo') or '').replace('https://github.com/davedellaquila/', '').strip('/') or b['id']
    cands = [os.path.expanduser('~/workspace/projects/' + repo),
             os.path.expanduser('~/workspace/projects/' + b['id'])]
    for c in cands:
        if os.path.isdir(c) and any(f.endswith('.md') for f in os.listdir(c)):
            return c
    return None

def _rf_md_files(clone):
    out = []
    for sub in ('', 'docs'):
        d = os.path.join(clone, sub) if sub else clone
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith('.md') and os.path.isfile(os.path.join(d, f)):
                rel = (sub + '/' + f) if sub else f
                out.append((rel, os.path.join(d, f)))
    def _key(item):
        rel = item[0]
        if '/' not in rel and rel in _RF_ORDER:
            return (0, _RF_ORDER.index(rel), rel)
        return (1, 0, rel)
    out.sort(key=_key)
    return out

def _rf_render(path):
    src = open(path, encoding='utf-8', errors='replace').read()
    if _markdown is not None:
        return _markdown.markdown(src, extensions=['tables', 'fenced_code', 'sane_lists'])
    return '<pre class="mdfallback">' + html.escape(src) + '</pre>'

def baked_repo_files_html(b):
    clone = _rf_clone_dir(b)
    if not clone:
        return ('<div class="rf-locked">No local copy of this buddy&#8217;s repo was '
                'available when this page was generated, so there are no files '
                'to bake in yet.</div>')
    if b.get('private_files'):
        # Privacy pull-back (Dave 2026-11-19, Hiking Buddy first): buddies
        # flagged private_files list file NAMES only on their public pages —
        # no baked contents, no reader panels.
        rows = []
        for rel, path in _rf_md_files(clone):
            nm = rel.split('/')[-1]
            dl = rel.rsplit('/', 1)[0] if '/' in rel else 'repo root'
            rows.append('<div class="rf-fileitem"><div class="rf-file">'
                        '<span class="rf-name">' + html.escape(nm) + '</span>'
                        '<span class="rf-dir">' + html.escape(dl) + '</span></div></div>')
        if not rows:
            return ('<div class="rf-locked">This buddy&#8217;s repo held no markdown '
                    'files when this page was generated.</div>')
        return ('<p class="rf-loading">File contents are not published on this '
                'public page.</p>' + ''.join(rows))
    items = []
    for rel, path in _rf_md_files(clone):
        name = rel.split('/')[-1]
        dlabel = rel.rsplit('/', 1)[0] if '/' in rel else 'repo root'
        try:
            panel = '<div class="rf-body">' + _rf_render(path) + '</div>'
        except Exception as e:
            panel = ('<p class="rf-loading">This file could not be baked in when '
                     'the page was generated: ' + html.escape(str(e)) + '</p>')
        items.append(
            '<div class="rf-fileitem">'
            '<button type="button" class="rf-file" aria-expanded="false">'
            '<span class="rf-chev">\u25b8</span>'
            '<span class="rf-name">' + html.escape(name) + '</span>'
            '<span class="rf-dir">' + html.escape(dlabel) + '</span></button>'
            '<div class="rf-panel" hidden>' + panel + '</div></div>')
    if not items:
        return ('<div class="rf-locked">This buddy&#8217;s repo held no markdown '
                'files when this page was generated.</div>')
    return ''.join(items)

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
.rf-body table { border-collapse: collapse; margin: 10px 0; font-size: 13.5px; }
.rf-body th, .rf-body td { border: 1px solid var(--border); padding: 5px 9px; text-align: left; }
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
<p class="rf-sub">The markdown files in <span data-buddy-name>__BNAME__</span>'s repo, baked into this page when it was generated — tap a file name and its contents open right below it; open as many as you like at once. No sign-in and no fetching: the words are right here. To change a file, edit it in the repo — the page picks it up next time it is generated.</p>
<div class="rf-main">
<div class="rf-list rf-files-wrap">__RFFILES__</div>
</div>
</section>
"""
FILES_JS = """
<script>
(function(){
  var sec = document.querySelector('.repo-files');
  if (!sec || sec.dataset.rfInit) return;
  sec.dataset.rfInit = '1';
  sec.querySelectorAll('.rf-fileitem > .rf-file').forEach(function(btn){
    btn.addEventListener('click', function(){
      var item = btn.parentElement;
      var panel = item ? item.querySelector('.rf-panel') : null;
      if (!panel) return;
      var open = panel.hidden;
      panel.hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var ch = btn.querySelector('.rf-chev');
      if (ch) ch.textContent = open ? '▾' : '▸';
    });
  });
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
  /* Disposition state (Dave 2026-11-20): every attention item carries Done /
     Need more info / Later / Drop it, in place. 'done' keeps its Nov 19
     device-local record (attnDone + the dashboard's 'seen' map); 'later' and
     'dropped' live in attnState, keyed the same way, so a tap on any surface
     promotes into the matching registry stamp at dashboard boot. */
  function localState(aid, text){
    var s = lsGet();
    var st = (s.attnState || {})[rkey(aid, text)];
    if (st && st.kind) return st.kind;
    var m = s.attnDone || {};
    if (m[rkey(aid, text)]) return 'done';
    /* Also honor the dashboard's own done map (the same store's 'seen',
       keyed by bare attention id) so an item cleared in the dashboard
       stays cleared here — one done state across surfaces. */
    if (aid && s.seen && s.seen[aid]) return 'done';
    return null;
  }
  function setLocalState(aid, text, kind, date){
    var s = lsGet(); var m = s.attnDone || {}; var st = s.attnState || {}; var k = rkey(aid, text);
    if (kind === 'done') { m[k] = 1; delete st[k]; }
    else { st[k] = {kind: kind, date: date}; delete m[k]; if (aid && s.seen) delete s.seen[aid]; }
    s.attnDone = m; s.attnState = st; lsSet(s);
  }
  function unsetLocalState(aid, text){
    var s = lsGet(); var m = s.attnDone || {}; var st = s.attnState || {}; var k = rkey(aid, text);
    delete m[k]; delete st[k]; s.attnDone = m; s.attnState = st;
    if (aid && s.seen) delete s.seen[aid]; lsSet(s);
  }
  /* Free-text notes (Dave 2026-11-20 amendment): the fifth action. A note
     lives on the device in attnNotes (same store, same keying as the
     dispositions, so the dashboard shows it too), renders on the card with
     its date, and is delivered to the owning buddy as a NOTE entry in
     docs/ingest.md through the same token-gated path as Need more info.
     A registry entry may also carry note {text, date}; the generator bakes
     it as data-note attrs and the tile paints it when no local note exists. */
  function localNote(aid, text){ var s = lsGet(); return (s.attnNotes || {})[rkey(aid, text)] || null; }
  function setLocalNote(aid, text, noteText, date){ var s = lsGet(); var n = s.attnNotes || {}; n[rkey(aid, text)] = {text: noteText, date: date}; s.attnNotes = n; lsSet(s); }
  function paintNote(tile, note){
    var el = tile.querySelector('.attn-note');
    if (!note) { if (el) el.remove(); return; }
    if (!el) {
      el = document.createElement('div'); el.className = 'attn-note';
      var st = tile.querySelector('.attn-status');
      if (st && st.parentNode) st.parentNode.insertBefore(el, st.nextSibling); else tile.appendChild(el);
    }
    el.textContent = '\u270e ' + note.text + (note.date ? ' \u00b7 ' + note.date : '');
  }
  async function sendNote(aid, text, noteText, msgEl){
    if (!token()) { msgEl.textContent = 'Note saved on this device and shown here \u2014 connect GitHub (Brain dump box above) to send it to ' + buddyName + '.'; return; }
    if (!repo) { msgEl.textContent = 'Note saved on this device and shown here \u2014 no repo linked for this buddy yet, so it could not be sent.'; return; }
    msgEl.textContent = 'Sending\u2026';
    try {
      var NL = String.fromCharCode(10);
      var stamp = new Date().toLocaleString();
      var cur = await ghGetFile(repo, 'docs/ingest.md');
      var base = cur ? cur.text : '# Ingest log \u2014 ' + buddyName + NL + NL;
      var idBit = aid ? ' (attention id: ' + aid + ')' : '';
      var entry = 'NOTE \u2014 Dave\u2019s note on: "' + text + '"' + idBit + ':' + NL + NL + noteText;
      var body = {message: 'Attention note for ' + bid, content: b64encode(base + '## ' + stamp + NL + NL + entry + NL + NL)};
      if (cur && cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md', 'PUT', body);
      msgEl.textContent = 'Note saved \u2014 sent to ' + buddyName + ' and shown on this card.';
    } catch(err){ msgEl.textContent = 'Note saved on this device and shown here \u2014 sending failed (' + (err.message || err) + '), so ' + buddyName + ' has not seen it yet.'; }
  }
  function openNoteEditor(tile, aid, text){
    var existing = tile.querySelector('.attn-note-edit');
    if (existing) { var ta0 = existing.querySelector('textarea'); if (ta0) ta0.focus(); return; }
    var wrap = document.createElement('div'); wrap.className = 'attn-note-edit';
    var ta = document.createElement('textarea'); ta.placeholder = 'Type your note\u2026'; ta.setAttribute('aria-label', 'Note for this item');
    var cur = localNote(aid, text); if (cur) ta.value = cur.text;
    var btns = document.createElement('div'); btns.className = 'attn-note-btns';
    var save = document.createElement('button'); save.type = 'button'; save.className = 'attn-btn primary'; save.setAttribute('data-note-act', 'save'); save.textContent = 'Save note';
    var cancel = document.createElement('button'); cancel.type = 'button'; cancel.className = 'attn-btn'; cancel.setAttribute('data-note-act', 'cancel'); cancel.textContent = 'Cancel';
    var msg = document.createElement('div'); msg.className = 'attn-note-msg'; msg.setAttribute('role', 'status');
    btns.appendChild(save); btns.appendChild(cancel); wrap.appendChild(ta); wrap.appendChild(btns); wrap.appendChild(msg);
    var acts = tile.querySelector('.attn-actions');
    if (acts && acts.parentNode) acts.parentNode.insertBefore(wrap, acts.nextSibling); else tile.appendChild(wrap);
    ta.focus();
  }
  function stateMsg(kind, date){
    if (kind === 'later') return 'Later \u00b7 ' + date;
    if (kind === 'dropped') return 'Dropped by Dave \u00b7 ' + date;
    return '\u2713 Done \u00b7 ' + date;
  }
  function todayStr(){ var d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  /* Registry clearance (Dave 2026-11-19): Done used to leave a note in
     the buddy's ingest asking an agent to hand-edit buddies.json later,
     so a fixed blocker (Emile's DocuSign, resolved Oct 21) kept
     presenting as open. The tap now writes the item's cleared stamp
     into buddies.json itself when a token is on this device. The
     device-local attnDone mark remains the instant/offline record,
     and the dashboard promotes local marks into the registry at boot. */
  async function regWrite(aid, text, kind, obj){
    try {
      var cur = await ghGetFile('buddy-system', 'buddies.json');
      if (!cur) return false;
      var d = JSON.parse(cur.text);
      var buds = d.buddies || [], bb = null;
      for (var i = 0; i < buds.length; i++) if (buds[i].id === bid) { bb = buds[i]; break; }
      if (!bb) return false;
      var list = bb.attention || [], hit = null, hitIdx = -1;
      for (var j = 0; j < list.length; j++) {
        var e = list[j];
        if (aid && e && typeof e === 'object' && e.id === aid) { hit = e; break; }
        if (!aid && typeof e === 'string' && e.slice(0, 60) === text.slice(0, 60)) { hitIdx = j; break; }
        if (!aid && e && typeof e === 'object' && (e.text || '').slice(0, 60) === text.slice(0, 60)) { hit = e; break; }
      }
      /* Dispositions are mutually exclusive stamps on the entry — setting one
         clears the others; an Undo removes all three (Dave 2026-11-20). */
      var ATTN_FIELD = {done: 'cleared', later: 'later', dropped: 'dropped'};
      if (hit) {
        ['cleared', 'later', 'dropped'].forEach(function(f){ delete hit[f]; });
        if (obj && kind) hit[ATTN_FIELD[kind]] = obj;
      }
      else if (hitIdx >= 0 && obj && kind) { var nb = {text: bb.attention[hitIdx]}; nb[ATTN_FIELD[kind]] = obj; bb.attention[hitIdx] = nb; }
      else return false;
      var body = {message: (obj && kind ? 'Disposition ' + kind + ' for attention ' : 'Reopen attention ') + (aid || 'item') + ' for ' + bid + ' (homepage)', content: b64encode(JSON.stringify(d, null, 1))};
      if (cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/buddy-system/contents/buddies.json', 'PUT', body);
      return true;
    } catch(e){ return false; }
  }
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
    var stEl = tile.querySelector('.attn-status');
    if (stEl && !tile.querySelector('[data-act="undo"]')) {
      var ub = document.createElement('button');
      ub.type = 'button'; ub.className = 'attn-btn attn-undo'; ub.setAttribute('data-act', 'undo'); ub.textContent = 'Undo';
      stEl.parentNode.insertBefore(ub, stEl.nextSibling);
    }
    /* The resolved class hides .attn-actions; the note button moves beside
       Undo so a dispositioned item can still be noted (Dave 2026-11-20). */
    var nb2 = tile.querySelector('[data-act="note"]');
    var ub2 = tile.querySelector('[data-act="undo"]');
    if (nb2 && ub2 && nb2.parentNode !== ub2.parentNode) ub2.parentNode.insertBefore(nb2, ub2.nextSibling);
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
  function paintOpen(tile){
    tile.classList.remove('resolved');
    tile.removeAttribute('data-cleared');
    tile.removeAttribute('data-later');
    tile.removeAttribute('data-dropped');
    var st = tile.querySelector('.attn-status');
    if (st) st.textContent = '';
    var db = tile.querySelector('[data-act="done"]');
    if (db) db.textContent = 'Done';
    var ub = tile.querySelector('[data-act="undo"]');
    if (ub) ub.remove();
    var acts2 = tile.querySelector('.attn-actions');
    var nb3 = tile.querySelector('[data-act="note"]');
    if (acts2 && nb3 && nb3.parentNode !== acts2) acts2.appendChild(nb3);
  }
  tiles.forEach(function(tile){
    var aid = tile.getAttribute('data-attn-id') || '';
    var textEl = tile.querySelector('.attn-text');
    var text = textEl ? textEl.textContent.trim() : '';
    var bakedKind = tile.getAttribute('data-cleared') ? 'done' : (tile.getAttribute('data-later') ? 'later' : (tile.getAttribute('data-dropped') ? 'dropped' : null));
    var bakedDate = tile.getAttribute('data-cleared') || tile.getAttribute('data-later') || tile.getAttribute('data-dropped') || '';
    var lk = bakedKind || localState(aid, text);
    if (lk) paintResolved(tile, bakedKind ? stateMsg(lk, bakedDate) : (lk === 'done' ? 'Marked done' : (lk === 'later' ? 'Marked later — on this device' : 'Dropped — on this device')), true);
    var bakedNote = tile.getAttribute('data-note') ? {text: tile.getAttribute('data-note'), date: tile.getAttribute('data-note-date') || ''} : null;
    var ln = localNote(aid, text);
    if (ln) paintNote(tile, ln); else if (bakedNote) paintNote(tile, bakedNote);
    tile.addEventListener('click', function(ev){
      var nb = ev.target.closest ? ev.target.closest('[data-note-act]') : null;
      if (nb) {
        var wrap = nb.closest('.attn-note-edit');
        var msg = wrap ? wrap.querySelector('.attn-note-msg') : null;
        if (nb.getAttribute('data-note-act') === 'cancel') { if (wrap) wrap.remove(); return; }
        var ta = wrap ? wrap.querySelector('textarea') : null;
        var val = ta ? ta.value.trim() : '';
        if (!val) { if (msg) msg.textContent = 'Write a note first, or Cancel.'; return; }
        var ndate = todayStr();
        setLocalNote(aid, text, val, ndate);
        paintNote(tile, {text: val, date: ndate});
        if (msg) sendNote(aid, text, val, msg);
        return;
      }
      var btn = ev.target.closest ? ev.target.closest('.attn-btn') : null;
      if (!btn || btn.disabled) return;
      var act = btn.getAttribute('data-act');
      var idBit = aid ? ' (attention id: ' + aid + ')' : '';
      if (act === 'done') {
        var cobj = {date: todayStr(), by: 'Dave'};
        setLocalState(aid, text, 'done', cobj.date);
        paintResolved(tile, stateMsg('done', cobj.date));
        celebrate(btn, tile);
        if (token()) {
          regWrite(aid, text, 'done', cobj).then(function(ok){
            var st = tile.querySelector('.attn-status');
            if (st) st.textContent = ok ? '\u2713 Done \u2014 recorded in the registry, so it stays done on every surface.' : 'Marked done on this device \u2014 the registry could not be updated just now, so other surfaces may still show it open.';
          });
        } else {
          var st2 = tile.querySelector('.attn-status');
          if (st2) st2.textContent = 'Marked done on this device \u2014 connect GitHub (Brain dump box above) to record it in the registry for good.';
        }
      } else if (act === 'later' || act === 'drop') {
        var kind = act === 'later' ? 'later' : 'dropped';
        var dobj = {date: todayStr(), by: 'Dave'};
        setLocalState(aid, text, kind, dobj.date);
        paintResolved(tile, stateMsg(kind, dobj.date));
        if (token()) {
          regWrite(aid, text, kind, dobj).then(function(ok){
            var st = tile.querySelector('.attn-status');
            if (st) st.textContent = ok ? stateMsg(kind, dobj.date) + ' \u2014 recorded in the registry.' : 'Marked on this device \u2014 the registry could not be updated just now, so other surfaces may still show it open.';
          });
        } else {
          var st2 = tile.querySelector('.attn-status');
          if (st2) st2.textContent = 'Marked on this device \u2014 connect GitHub (Brain dump box above) to record it in the registry for good.';
        }
      } else if (act === 'undo') {
        unsetLocalState(aid, text);
        paintOpen(tile);
        var st3 = tile.querySelector('.attn-status');
        if (st3) st3.textContent = 'Reopened \u2014 it needs attention again.';
        if (token()) regWrite(aid, text, null, null);
      } else if (act === 'note') {
        openNoteEditor(tile, aid, text);
      } else if (act === 'info') {
        sendAction(tile,
          'FOLLOW-UP \u2014 Dave needs more info on: \"' + text + '\"' + idBit + '. Please follow up with him.',
          'Sent \u2014 ' + buddyName + ' will follow up.');
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
  display: flex; flex-wrap: wrap; align-items: center; gap: 10px;
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
.bs-dash-link {{ font-size: 13px; font-weight: 600; color: var(--accent); text-decoration: none; white-space: nowrap; margin-left: 10px; }}
.bs-dash-link:hover {{ text-decoration: underline; }}
.topbar .header-tip {{ margin-left: auto; flex: none; }}
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
.attn-undo {{ margin-top: 8px; }}
.attn-note {{ font-size: 13px; color: var(--text); margin-top: 8px; background: var(--card); border-left: 3px solid var(--accent); padding: 6px 10px; border-radius: 0 6px 6px 0; white-space: pre-wrap; }}
.attn-note-edit {{ margin-top: 10px; }}
.attn-note-edit textarea {{ width: 100%; box-sizing: border-box; border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px; font: inherit; font-size: 14px; background: var(--bg); color: var(--text); min-height: 56px; }}
.attn-note-btns {{ display: flex; gap: 8px; margin-top: 8px; }}
.attn-note-msg {{ font-size: 12.5px; color: var(--muted); margin-top: 6px; }}
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
<div class="topbar"><span class="topbar-icon">{icon}</span><span class="topbar-name" data-buddy-name>{name}</span><button class="topbar-refresh" title="Reload this page (bypasses cache)" onclick="location.href=location.pathname+'?v='+Date.now()">&#8635;</button><a class="bs-dash-link" href="https://davedellaquila.github.io/buddy-system/">Buddy System dashboard</a></div>
<div class="header">
<div class="icon">{icon}</div>
<h1 data-buddy-name>{name}</h1>
<div class="tagline">{tagline}</div>
</div>

<div class="mission">{mission}</div>

{gallery_section}

{role_audio_section}
{dumpbox_html}

{attention_section}

{skills_section}

{children_section}

{docs_section}

{files_section}

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
    pubnames = set()
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
                    pubnames.add(fl.get('name'))
                    if u not in seen:
                        urls.append(u); seen.add(u)
    except Exception:
        pass
    # Fall back to the buddy's own repo photos/ (may be private — URLs can 404).
    # A file already vendored into the public buddy-system tree supersedes
    # its private-repo twin (Dave's MGA photo, 2026-11-05: the private raw
    # URL 404s for every viewer, so the fallback copy must not reappear
    # alongside the public one on regeneration).
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
                        if fl.get('name') in pubnames:
                            continue
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

# --- Managed Files section (Dave's homepage standard, 2026-11-18) ---------
# Every homepage lists the files its buddy manages: registry-registered
# records first (they can live outside the repo -- goal files and records a
# buddy or Astro registers in the buddies.json `files` list), then the
# documents in the buddy's own repo, inventoried from the local clone's
# tracked files. The section always renders; a buddy with nothing yet gets
# "No files yet." Keep in step with gen_default_homepages.py.
_MF_DOC_EXTS = ('.md', '.txt', '.pdf', '.csv')
_MF_REPO_ORDER = ['KNOWLEDGE.md', 'CONFIG.md', 'STUDY.md', 'SOUL.md', 'DECISIONS.md',
                  'ACCOMPLISHMENTS.md', 'README.md']
_MF_TRACKED = {}

def _mf_tracked(root):
    if root in _MF_TRACKED:
        return _MF_TRACKED[root]
    tracked, branch = [], 'master'
    try:
        tracked = subprocess.run(['git', '-C', root, 'ls-files'],
                                 capture_output=True, text=True, timeout=30).stdout.splitlines()
        # Blob links must name the REMOTE's default branch -- a local clone
        # can sit on a differently-named working branch (emil-estate's clone
        # is on `main` while the repo's default is `master`, and its clone
        # has no origin/HEAD symref at all). Resolution: the origin/HEAD
        # target when the clone records one, else master when the remote
        # has it, else main, else the local HEAD branch.
        rbranches = set()
        for line in subprocess.run(['git', '-C', root, 'branch', '-r'],
                                   capture_output=True, text=True, timeout=10).stdout.splitlines():
            line = line.strip()
            if ' -> ' in line:
                rbranches.add('HEAD:' + line.split(' -> ')[1].strip().replace('origin/', '', 1))
            elif line.startswith('origin/'):
                rbranches.add(line[len('origin/'):])
        head_target = next((x[5:] for x in rbranches if x.startswith('HEAD:')), None)
        if head_target:
            branch = head_target
        elif 'master' in rbranches:
            branch = 'master'
        elif 'main' in rbranches:
            branch = 'main'
        else:
            branch = subprocess.run(['git', '-C', root, 'rev-parse', '--abbrev-ref', 'HEAD'],
                                    capture_output=True, text=True, timeout=10).stdout.strip() or 'master'
    except Exception:
        pass
    _MF_TRACKED[root] = (tracked, branch)
    return tracked, branch

def _mf_repo_docs(b, exclude_urls=frozenset()):
    """(rows, total): rows are (relpath, blob url) for tracked document files
    in the buddy's repo -- root level plus docs/ and files/ only, so records
    and docs surface while code and build plumbing never do."""
    repo = (b.get('repo') or '').replace('https://github.com/davedellaquila/', '').strip('/') or b['id']
    if repo == 'buddy-system':
        root, prefix = HERE, b['id'] + '/'
    else:
        root = os.path.expanduser('~/workspace/projects/' + repo)
        prefix = ''
        if not os.path.isdir(os.path.join(root, '.git')):
            return [], 0
    tracked, branch = _mf_tracked(root)
    rows = []
    for rel in tracked:
        rel = rel.strip()
        if prefix:
            if not rel.startswith(prefix):
                continue
            r = rel[len(prefix):]
        else:
            r = rel
        if os.path.splitext(r)[1].lower() not in _MF_DOC_EXTS:
            continue
        parts = r.split('/')
        if len(parts) > 1 and parts[0] not in ('docs', 'files'):
            continue
        if any(p in ('node_modules', 'vendor', '__pycache__') for p in parts[:-1]):
            continue
        url = 'https://github.com/davedellaquila/' + repo + '/blob/' + branch + '/' + rel
        if url in exclude_urls:
            continue  # already listed as a registered file with a human title
        rows.append((r, url))
    def _key(row):
        base = row[0].split('/')[-1]
        if '/' not in row[0] and base in _MF_REPO_ORDER:
            return (0, _MF_REPO_ORDER.index(base), row[0])
        return (1, 0, row[0])
    rows.sort(key=_key)
    return rows[:50], len(rows)

def managed_files_section(b):
    reg = [x for x in (b.get('files') or [])
           if isinstance(x, dict) and x.get('title') and (x.get('url') or x.get('path'))]
    repo_rows, repo_total = _mf_repo_docs(
        b, exclude_urls=frozenset(x['url'] for x in reg if x.get('url')))
    if not reg and not repo_rows:
        return '<h2>\U0001F4C1 Files</h2>\n<p style="color:var(--muted)">No files yet.</p>'
    out = ['<h2>\U0001F4C1 Files</h2>']
    both = bool(reg) and bool(repo_rows)
    grp = ('<div style="font-size:13px;color:var(--muted);text-transform:uppercase;'
           'letter-spacing:.06em;margin:12px 0 4px">%s</div>')
    if reg:
        if both:
            out.append(grp % 'Registered files')
        out.append('<div class="docs">')
        for x in reg:
            if x.get('url'):
                row = ('<p style="margin:6px 0"><a href="' + html.escape(x['url'], quote=True)
                       + '">' + html.escape(x['title']) + '</a>')
            else:
                row = '<p style="margin:6px 0">' + html.escape(x['title'])
            for sub in (x.get('note'), x.get('path')):
                if sub:
                    row += ('<br><span style="color:var(--muted);font-size:14px">'
                            + html.escape(sub) + '</span>')
            out.append(row + '</p>')
        out.append('</div>')
    if repo_rows:
        if both:
            out.append(grp % 'In the repo')
        out.append('<div class="docs">')
        for r, url in repo_rows:
            nm = r.split('/')[-1]
            dr = r.rsplit('/', 1)[0] if '/' in r else ''
            row = ('<p style="margin:6px 0"><a href="' + html.escape(url, quote=True)
                   + '">' + html.escape(nm) + '</a>')
            if dr:
                row += (' <span style="color:var(--muted);font-size:14px">'
                        + html.escape(dr) + '/</span>')
            out.append(row + '</p>')
        if repo_total > len(repo_rows):
            out.append('<p style="margin:6px 0;color:var(--muted);font-size:14px">'
                       + '\u2026and %d more in the repo \u2014 the Repo files section below lists everything.</p>'
                       % (repo_total - len(repo_rows)))
        out.append('</div>')
    return '\n'.join(out)

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
            stamp = None
            if isinstance(a, dict):
                if a.get('cleared'): stamp = ('done', a['cleared'])
                elif a.get('later'): stamp = ('later', a['later'])
                elif a.get('dropped'): stamp = ('dropped', a['dropped'])
            note = a.get('note') if isinstance(a, dict) else None
            note_attrs = ''
            if isinstance(note, dict) and note.get('text'):
                note_attrs = ' data-note="%s" data-note-date="%s"' % (html.escape(str(note['text']), quote=True), html.escape(str(note.get('date', '')), quote=True))
            sdate = html.escape(str(stamp[1].get('date', '')), quote=True) if stamp else ''
            sattr = {'done': 'data-cleared', 'later': 'data-later', 'dropped': 'data-dropped'}
            attn_html += f'<div class="attn{" resolved" if stamp else ""}" data-attn-id="{aid}"{(" " + sattr[stamp[0]] + "=\"" + sdate + "\"") if stamp else ""}{note_attrs}><div class="attn-text">{text}</div>'
            if url:
                attn_html += f'<div class="attn-link"><a href="{url}" target="_blank" rel="noopener">Open →</a></div>'
            if date:
                attn_html += f'<div class="attn-date">{date}</div>'
            stamp_note = {'done': f'✓ Done · {sdate}', 'later': f'Later · {sdate}', 'dropped': f'Dropped by Dave · {sdate}'}
            attn_html += ('<div class="attn-actions">'
                          '<button type="button" class="attn-btn primary" data-act="done">Done</button>'
                          '<button type="button" class="attn-btn" data-act="info">Need more info</button>'
                          '<button type="button" class="attn-btn" data-act="later">Later</button>'
                          '<button type="button" class="attn-btn" data-act="drop">Drop it</button>'
                          '<button type="button" class="attn-btn" data-act="note">\u270e Add a note\u2026</button>'
                          '</div><div class="attn-status" role="status">'
                          + (stamp_note[stamp[0]] if stamp else '')
                          + '</div>'
                          + ('<button type="button" class="attn-btn attn-undo" data-act="undo">Undo</button>' if stamp else '')
                          + '</div>\n')
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

    # Role audio (Dave's standing rule, 2026-10-24): when the buddy's
    # role-intro.mp3 is hosted next to this page, emit the "Hear my role"
    # control. The generator owns this block — a hand-inserted copy on
    # garden-buddy was wiped by the 2026-10-28 regen because the generator
    # didn't emit it. Voice display name only when the registry voice id
    # ends in a plain readable name (e.g. avocado_v2:marisol → Marisol).
    role_audio_section = ''
    if os.path.exists(os.path.join(HERE, bid, 'role-intro.mp3')):
        voice_disp = ''
        vsuffix = (b.get('voice') or '').rsplit(':', 1)[-1]
        if vsuffix.isalpha() and vsuffix.islower():
            voice_disp = ' (' + vsuffix.capitalize() + ')'
        role_audio_section = (
            '<div style="margin:16px 0 4px">\n'
            '<div style="font-size:13px;opacity:.75;margin-bottom:6px">🔊 <b>Hear my role</b>'
            ' — the first paragraph of my job req\'s Role summary, in my own voice'
            + voice_disp + '</div>\n'
            '<audio controls preload="none" src="role-intro.mp3" style="width:min(420px,100%)"></audio>\n'
            '</div>\n'
        )

    dumpbox_html = DUMPBOX_HTML.replace('__BID__', bid).replace('__BNAME__', name)
    repo_files_html = FILES_HTML.replace('__BID__', bid).replace('__BNAME__', name).replace('__RFFILES__', baked_repo_files_html(b))

    # Documents -- the registry docs list (label/url, optional note),
    # rendered on the standalone homepage so a buddy's reports are
    # findable where Dave looks for them (Developer Buddy, 2026-11-15:
    # the ML500 tire report sat in the registry with no surface on the
    # basic homepage -- the template never rendered docs at all).
    docs_items = [x for x in (b.get('docs') or [])
                  if isinstance(x, dict) and x.get('label') and x.get('url')]
    if docs_items:
        docs_html = '<h2>\U0001F4DA Documents</h2>\n<div class="docs">\n'
        for x in docs_items:
            docs_html += ('<p style="margin:6px 0"><a href="'
                          + html.escape(x['url'], quote=True) + '">'
                          + html.escape(x['label']) + '</a>')
            if x.get('note'):
                docs_html += ('<br><span style="color:var(--muted);font-size:14px">'
                              + html.escape(x['note']) + '</span>')
            docs_html += '</p>\n'
        docs_html += '</div>'
        docs_section = docs_html
    else:
        docs_section = ''

    files_section = managed_files_section(b)

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
        role_audio_section=role_audio_section,
        dumpbox_css=DUMPBOX_CSS,
        dumpbox_html=dumpbox_html,
        dumpbox_js=DUMPBOX_JS,
        attn_js=ATTN_JS,
        files_css=FILES_CSS,
        docs_section=docs_section,
        files_section=files_section,
        repo_files_section=repo_files_html,
        files_js=FILES_JS,
        namesync_js=NAMESYNC_JS,
    )

    # Tip jar (Dave's standing rule, 2026-10-24; HEADER placement 2026-10-28):
    # the jar is a compact bug in the sticky topbar now (Developer Buddy's
    # homepage is the reference implementation), no longer a floating pill
    # injected before </body>. Canonical copy: docs/tipjar-snippet.html,
    # read live so the fleet never drifts — <style> into <head>, anchor into
    # the topbar after the dashboard link. Regeneration drops the old pill
    # automatically (the template never contained it; it was injected).
    if 'class="header-tip"' not in page:
        _tstyle, _tanchor = _tipjar_parts()
        if _tstyle and '</head>' in page:
            page = page.replace('</head>', _tstyle + '\n</head>', 1)
        if _tanchor and 'Buddy System dashboard</a></div>' in page:
            page = page.replace('Buddy System dashboard</a></div>',
                                'Buddy System dashboard</a>' + _tanchor + '</div>', 1)

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

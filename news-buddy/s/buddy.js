
/* Attention action buttons — writes to the buddy repo's docs/ingest.md via the shared GitHub token (same pattern as the brain-dump box). Reference: gen_basic_homepages.py ATTN_JS. */
(function(){
  var tiles = document.querySelectorAll('.attn[data-attn-id]');
  if (!tiles.length) return;
  var dumpbox = document.querySelector('.dumpbox');
  var bid = (dumpbox && dumpbox.getAttribute('data-buddy-id')) || (function(){
    var p = location.pathname.replace(/\/+$/, '');
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
      var j = await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md');
      if (j && j.content) return {
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\n/g, '')), function(c){ return c.charCodeAt(0); })),
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
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\n/g, '')), function(c){ return c.charCodeAt(0); })),
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

;

/* NBVoice: the read-aloud voice picker. First Listen click opens the picker.
   The free set is 10 voices re-dealt at random on every page load (so non-tippers
   get variety); the rest unlock with a tip. Choice saved in localStorage.
   embedList() renders the same picker UI inline (used by the settings dialog). */
window.NBVoice = (function(){
  var KEY = 'newsBuddyVoiceURI';
  var TIP_URL = 'https://ko-fi.com/davedellaquila';
  var FREE_N = 10;
  var voices = [], loaded = false, waiters = [];
  var freeVoices = [], lockedVoices = [];
  var supported = ('speechSynthesis' in window);
  function savedURI(){ try { return localStorage.getItem(KEY) || ''; } catch(e){ return ''; } }
  function shuffled(){
    var a = voices.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function deal(){
    var all = shuffled();
    var cur = savedURI(), sv = null, i;
    for (i = 0; i < all.length; i++) if (all[i].voiceURI === cur) { sv = all.splice(i, 1)[0]; break; }
    freeVoices = all.slice(0, FREE_N);
    if (sv) freeVoices.unshift(sv);
    lockedVoices = all.slice(FREE_N);
  }
  function grab(){
    if (!supported) return;
    try {
      var v = window.speechSynthesis.getVoices();
      if (v && v.length && !loaded) {
        loaded = true; voices = v; deal();
        waiters.forEach(function(w){ try { w(); } catch(e){} }); waiters = [];
      }
    } catch(e){}
  }
  if (supported) {
    grab();
    window.speechSynthesis.onvoiceschanged = grab;
    setTimeout(grab, 1500);
  }
  function ready(fn){
    if (!supported) { fn([]); return; }
    if (loaded) fn(voices); else waiters.push(function(){ fn(voices); });
  }
  function pick(){
    var uri = savedURI();
    if (!uri) return null;
    for (var i = 0; i < voices.length; i++) if (voices[i].voiceURI === uri) return voices[i];
    return null;
  }
  function preview(v){
    if (!supported) return;
    try {
      window.speechSynthesis.cancel();
      var nm = String(v.name).split('(')[0].trim();
      var u = new SpeechSynthesisUtterance("Hi, I'm " + nm + ". This is how I'll read you the morning news.");
      u.voice = v;
      window.speechSynthesis.speak(u);
    } catch(e){}
  }
  function closePicker(){
    var ov = document.getElementById('vpOverlay');
    if (ov && ov.parentNode) ov.parentNode.removeChild(ov);
    try { window.speechSynthesis.cancel(); } catch(e){}
  }
  function row(v, isCurrent, locked){
    var r = document.createElement('div');
    r.className = 'vp-row' + (isCurrent ? ' current' : '') + (locked ? ' locked' : '');
    r.dataset.vuri = v.voiceURI;
    if (locked) {
      var lk = document.createElement('div'); lk.className = 'vp-check'; lk.textContent = '🔒';
      var nm = document.createElement('div'); nm.className = 'nm';
      var b = document.createElement('b'); b.textContent = String(v.name).split('(')[0].trim();
      var s = document.createElement('span'); s.textContent = (v.lang || '') + ' · unlock with a tip';
      nm.appendChild(b); nm.appendChild(s);
      r.appendChild(lk); r.appendChild(nm);
    } else {
      var pv = document.createElement('button');
      pv.className = 'vp-prev'; pv.textContent = '▶'; pv.title = 'Preview this voice'; pv.setAttribute('aria-label', 'Preview ' + v.name);
      pv.addEventListener('click', function(ev){ ev.stopPropagation(); preview(v); });
      var nm2 = document.createElement('div'); nm2.className = 'nm';
      var b2 = document.createElement('b'); b2.textContent = String(v.name).split('(')[0].trim();
      var s2 = document.createElement('span'); s2.textContent = (v.lang || '') + (v.default ? ' · device default' : '');
      nm2.appendChild(b2); nm2.appendChild(s2);
      var ck = document.createElement('div'); ck.className = 'vp-check'; ck.textContent = isCurrent ? '✓' : '';
      r.appendChild(pv); r.appendChild(nm2); r.appendChild(ck);
    }
    return r;
  }
  function refreshChecks(list, curURI){
    list.querySelectorAll('.vp-row').forEach(function(r){
      if (r.classList.contains('locked')) return;
      var on = r.dataset.vuri === curURI;
      r.classList.toggle('current', on);
      var ck = r.querySelector('.vp-check');
      if (ck) ck.textContent = on ? '✓' : '';
    });
  }
  /* Render the picker list UI into any container. onPick(v) fires on selection. */
  function embedList(container, onPick){
    ready(function(){
      while (container.firstChild) container.removeChild(container.firstChild);
      var cur = savedURI();
      var sub = document.createElement('div'); sub.className = 'vp-sub';
      sub.textContent = freeVoices.length ? 'Tap ▶ to preview a voice — tap the row to choose it' : 'No voices found on this device yet';
      container.appendChild(sub);
      var list = document.createElement('div'); list.className = 'vp-list';
      freeVoices.forEach(function(v){
        var r = row(v, v.voiceURI === cur, false);
        r.addEventListener('click', function(){
          try { localStorage.setItem(KEY, v.voiceURI); } catch(e){}
          refreshChecks(list, v.voiceURI);
          if (onPick) onPick(v);
        });
        list.appendChild(r);
      });
      if (lockedVoices.length) {
        var sub2 = document.createElement('div'); sub2.className = 'vp-sub';
        sub2.textContent = '🔒 ' + lockedVoices.length + ' more voices';
        list.appendChild(sub2);
        lockedVoices.forEach(function(v){ list.appendChild(row(v, false, true)); });
      }
      container.appendChild(list);
      var tip = document.createElement('div'); tip.className = 'vp-tip';
      tip.innerHTML = 'Enjoying the paper? <a href="' + TIP_URL + '" target="_blank" rel="noopener">Tip the jar</a> to unlock every voice.';
      container.appendChild(tip);
    });
  }
  function openPicker(onDone){
    ready(function(){
      closePicker();
      var ov = document.createElement('div');
      ov.className = 'vp-overlay'; ov.id = 'vpOverlay';
      ov.addEventListener('click', function(ev){ if (ev.target === ov) closePicker(); });
      var card = document.createElement('div');
      card.className = 'vp-card'; card.setAttribute('role','dialog'); card.setAttribute('aria-label','Choose a reading voice');
      var head = document.createElement('div'); head.className = 'vp-head';
      var h = document.createElement('h3'); h.textContent = '🎙 Choose your newsreader';
      var x = document.createElement('button'); x.className = 'vp-close'; x.textContent = '✕'; x.setAttribute('aria-label','Close');
      x.addEventListener('click', closePicker);
      head.appendChild(h); head.appendChild(x); card.appendChild(head);
      var wrap = document.createElement('div');
      card.appendChild(wrap);
      ov.appendChild(card);
      document.body.appendChild(ov);
      embedList(wrap, function(){ closePicker(); if (onDone) onDone(); });
    });
  }
  function ensure(fn){
    if (!supported) { if (fn) fn(); return; }
    ready(function(){
      if (savedURI() && pick()) { if (fn) fn(); }
      else openPicker(fn);
    });
  }
  return {pick: pick, chosen: function(){ return !!savedURI(); }, openPicker: openPicker, ensure: ensure, embedList: embedList, supported: supported};
})();

;

/* Read-aloud: whole edition + per-story, via the device's speech engine (no network, no tokens). Buttons are injected so the daily refresh never has to rebuild them. */
(function(){
  if (!('speechSynthesis' in window)) return;
  var synth = window.speechSynthesis;
  var editionBtn = null, queue = [], qIndex = 0, editionMode = false, currentBtn = null;

  function storyText(article){
    var h3 = article.querySelector('h3'), head = '';
    if (h3) {
      var c = h3.cloneNode(true);
      c.querySelectorAll('.thin,.story-listen,.story-vote,.story-controls').forEach(function(s){ s.remove(); });
      head = c.textContent.trim().replace(/\s+/g, ' ');
    }
    var dek = article.querySelector('.dek');
    var body = dek ? dek.textContent.trim().replace(/\s+/g, ' ') : '';
    return (head + '. ' + body).trim();
  }
  function chunkText(text){
    var sentences = text.match(/[^.!?]+[.!?]+/g) || [text];
    var chunks = [], cur = '';
    sentences.forEach(function(s){
      if (cur && (cur + s).length > 220) { chunks.push(cur.trim()); cur = s; }
      else cur += s;
    });
    if (cur.trim()) chunks.push(cur.trim());
    return chunks;
  }
  function speak(text, onend){
    var chunks = chunkText(text), i = 0;
    (function next(){
      if (i >= chunks.length) { if (onend) onend(); return; }
      var u = new SpeechSynthesisUtterance(chunks[i++]);
      u.onend = next; u.onerror = next;
      try { var pv = (window.NBVoice && NBVoice.pick()); if (pv) u.voice = pv; } catch(e){}
      synth.speak(u);
    })();
  }
  function paintOff(){
    document.querySelectorAll('article.story.reading').forEach(function(a){ a.classList.remove('reading'); });
    document.querySelectorAll('.story-listen.playing').forEach(function(b){ b.classList.remove('playing'); b.textContent = '\uD83D\uDD0A'; });
    if (editionBtn) { editionBtn.classList.remove('playing'); editionBtn.textContent = '\uD83D\uDD0A Listen to this edition'; }
    currentBtn = null;
  }
  function stopAll(){ synth.cancel(); queue = []; qIndex = 0; editionMode = false; paintOff(); }
  function playQueue(){
    if (qIndex >= queue.length) { stopAll(); return; }
    var item = queue[qIndex++];
    document.querySelectorAll('article.story.reading').forEach(function(a){ a.classList.remove('reading'); });
    if (item.article) item.article.classList.add('reading');
    if (item.btn) { document.querySelectorAll('.story-listen.playing').forEach(function(b){ b.classList.remove('playing'); b.textContent = '\uD83D\uDD0A'; }); item.btn.classList.add('playing'); item.btn.textContent = '\u23F9'; }
    speak(item.text, playQueue);
  }
  function storyControls(h3){
    var c = h3.querySelector('.story-controls');
    if (!c) { c = document.createElement('span'); c.className = 'story-controls'; h3.appendChild(c); }
    return c;
  }
  function playStory(article, btn){
    if (currentBtn === btn) { stopAll(); return; }
    window.NBVoice.ensure(function(){
    stopAll();
    var text = storyText(article);
    if (!text) return;
    currentBtn = btn;
    article.classList.add('reading');
    btn.classList.add('playing'); btn.textContent = '\u23F9';
    speak(text, stopAll);
    });
  }
  function playEdition(){
    if (editionMode) { stopAll(); return; }
    window.NBVoice.ensure(function(){
    stopAll();
    editionMode = true;
    if (editionBtn) { editionBtn.classList.add('playing'); editionBtn.textContent = '\u23F9 Stop'; }
    queue = [];
    document.querySelectorAll('section').forEach(function(sec){
      var h2 = sec.querySelector('.sec-head h2');
      if (!h2) return;
      var articles = sec.querySelectorAll('article.story');
      if (!articles.length) return;
      queue.push({text: h2.textContent.trim() + '.', article: null, btn: null});
      articles.forEach(function(a){
        queue.push({text: storyText(a), article: a, btn: a.querySelector('.story-listen')});
      });
    });
    playQueue();
    });
  }
  var dateline = document.querySelector('.dateline');
  if (dateline) {
    editionBtn = document.createElement('button');
    editionBtn.type = 'button';
    editionBtn.className = 'listen-edition';
    editionBtn.textContent = '\uD83D\uDD0A Listen to this edition';
    editionBtn.setAttribute('aria-label', 'Read the whole edition aloud');
    editionBtn.addEventListener('click', playEdition);
    dateline.appendChild(editionBtn);
    var vb = document.createElement('button');
    vb.type = 'button';
    vb.className = 'voice-change';
    vb.textContent = '\uD83C\uDFA4';
    vb.title = 'Change reading voice';
    vb.setAttribute('aria-label', 'Change reading voice');
    vb.addEventListener('click', function(){ if (window.NBVoice) NBVoice.openPicker(); });
    dateline.appendChild(vb);
  }
  document.querySelectorAll('article.story h3').forEach(function(h3){
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'story-listen';
    b.textContent = '\uD83D\uDD0A';
    b.title = 'Read this story aloud';
    b.setAttribute('aria-label', 'Read this story aloud');
    b.addEventListener('click', function(ev){
      ev.preventDefault(); ev.stopPropagation();
      var article = h3.closest('article');
      if (article) playStory(article, b);
    });
    storyControls(h3).appendChild(b);
  });
  window.addEventListener('pagehide', function(){ try { synth.cancel(); } catch(e){} });
})();

;

/* Story votes: thumbs up/down per article. Instant state in localStorage; durable log appended to the repo's docs/story-votes.md (same GitHub token as the brain-dump box). */
(function(){
  var box = document.querySelector('.dumpbox');
  var bid = (box && box.getAttribute('data-buddy-id')) || 'news-buddy';
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
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\n/g, '')), function(c){ return c.charCodeAt(0); })),
        sha: j.sha
      };
    } catch(e){}
    return null;
  }
  var repo = null;
  fetch('../buddies.json', {cache: 'no-store'}).then(function(r){ return r.json(); }).then(function(d){
    var buds = d.buddies || [];
    for (var i = 0; i < buds.length; i++) if (buds[i].id === bid && buds[i].repo) { repo = buds[i].repo; break; }
  }).catch(function(){});
  function vkey(article){
    var dc = article.getAttribute('data-canonical');
    if (dc) return 'vote|' + dc;
    var a = article.querySelector('h3 a');
    var url = a ? a.getAttribute('href') : '';
    if (url) return 'vote|' + url;
    var h3 = article.querySelector('h3');
    return 'vote|text:' + (h3 ? h3.textContent.trim().slice(0, 60) : '');
  }
  function getVote(k){ var m = lsGet().storyVotes || {}; return m[k] || 0; }
  function setVote(k, v){ var s = lsGet(); var m = s.storyVotes || {}; if (v) m[k] = v; else delete m[k]; s.storyVotes = m; lsSet(s); }
  function meta(article){
    var h3 = article.querySelector('h3'), head = '';
    if (h3) { var c = h3.cloneNode(true); c.querySelectorAll('.thin,.story-listen,.story-vote,.story-controls').forEach(function(s){ s.remove(); }); head = c.textContent.trim().replace(/\s+/g, ' '); }
    var dc = article.getAttribute('data-canonical');
    var a = article.querySelector('h3 a');
    var sec = article.closest('section');
    var h2 = sec ? sec.querySelector('.sec-head h2') : null;
    return {headline: head, url: dc || (a ? a.getAttribute('href') : ''), section: h2 ? h2.textContent.trim() : ''};
  }
  async function logVote(action, m){
    if (!token() || !repo) return;
    try {
      var NL = String.fromCharCode(10);
      var stamp = new Date().toLocaleString();
      var cur = await ghGetFile(repo, 'docs/story-votes.md');
      var base = cur ? cur.text : '# Story votes \u2014 News Buddy' + NL + NL + 'Dave\u2019s thumbs up/down on newspaper stories. +1 = more like this, -1 = less like this.' + NL + NL;
      var line = '## ' + stamp + NL + action + ' | ' + m.section + ' | "' + m.headline.replace(/"/g, "'") + '"' + (m.url ? ' | ' + m.url : '') + NL + NL;
      var body = {message: 'Story vote for ' + bid, content: b64encode(base + line)};
      if (cur && cur.sha) body.sha = cur.sha;
      await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/story-votes.md', 'PUT', body);
    } catch(e){}
  }
  function paint(article){
    var v = getVote(vkey(article));
    var up = article.querySelector('.story-vote.up'), dn = article.querySelector('.story-vote.dn');
    if (up) up.classList.toggle('on-up', v === 1);
    if (dn) dn.classList.toggle('on-down', v === -1);
  }
  document.querySelectorAll('article.story h3').forEach(function(h3){
    var article = h3.closest('article');
    if (!article) return;
    function mk(cls, label, emoji, val){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'story-vote ' + cls; b.textContent = emoji;
      b.title = label; b.setAttribute('aria-label', label);
      b.addEventListener('click', function(ev){
        ev.preventDefault(); ev.stopPropagation();
        var k = vkey(article), cur = getVote(k);
        var next = (cur === val) ? 0 : val;
        setVote(k, next);
        paint(article);
        var m = meta(article);
        logVote(next === 1 ? 'UPVOTE +1' : next === -1 ? 'DOWNVOTE -1' : 'UNVOTE', m);
      });
      return b;
    }
    var vc = h3.querySelector('.story-controls');
    if (!vc) { vc = document.createElement('span'); vc.className = 'story-controls'; h3.appendChild(vc); }
    vc.appendChild(mk('up', 'More like this', '\uD83D\uDC4D', 1));
    vc.appendChild(mk('dn', 'Less like this', '\uD83D\uDC4E', -1));
    paint(article);
  });
})();

;

/* Settings dialog: topic pills (Money-Buddy-style multi-select), thumbnail toggle, embedded voice picker. Homepage only. */
(function(){
  var dateline = document.querySelector('.dateline');
  if (!dateline) return;
  var TOPICS = [
    ['top-stories','Top Stories'],['ai-technology','AI & Technology'],
    ['markets','Markets'],['product-design','Product Design'],
    ['engineering','Engineering'],['motorsport','Motorsport'],
    ['live-music','Live Music'],['amador-county','Amador County']
  ];
  function jget(k, d){ try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch(e){ return d; } }
  function jset(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} }
  function sectionSlug(sec){
    var a = sec.querySelector('.sec-head h2 a');
    if (!a) return '';
    var m = /sections\/(.+)\.html/.exec(a.getAttribute('href') || '');
    return m ? m[1] : '';
  }
  function applyTopics(){
    var on = jget('newsBuddyTopics', null);
    document.querySelectorAll('section').forEach(function(sec){
      var slug = sectionSlug(sec);
      if (!slug) return;
      sec.style.display = (on && on.indexOf(slug) === -1) ? 'none' : '';
    });
  }
  function applyThumbs(){
    document.body.classList.toggle('no-thumbs', !jget('newsBuddyThumbs', true));
  }
  applyTopics(); applyThumbs();

  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'voice-change';
  btn.textContent = '⚙ Settings'; btn.title = 'Newspaper settings';
  btn.setAttribute('aria-label', 'Open newspaper settings');
  btn.addEventListener('click', openSettings);
  dateline.appendChild(btn);

  function closeSettings(){
    var ov = document.getElementById('setOverlay');
    if (ov && ov.parentNode) ov.parentNode.removeChild(ov);
    try { window.speechSynthesis.cancel(); } catch(e){}
  }
  function openSettings(){
    closeSettings();
    var ov = document.createElement('div');
    ov.className = 'vp-overlay'; ov.id = 'setOverlay';
    ov.addEventListener('click', function(ev){ if (ev.target === ov) closeSettings(); });
    var card = document.createElement('div');
    card.className = 'vp-card'; card.setAttribute('role','dialog'); card.setAttribute('aria-label','Newspaper settings');
    var head = document.createElement('div'); head.className = 'vp-head';
    var h = document.createElement('h3'); h.textContent = '⚙ Newspaper settings';
    var x = document.createElement('button'); x.className = 'vp-close'; x.textContent = '✕'; x.setAttribute('aria-label','Close');
    x.addEventListener('click', closeSettings);
    head.appendChild(h); head.appendChild(x); card.appendChild(head);

    var ts = document.createElement('div'); ts.className = 'set-sec';
    var th = document.createElement('h4'); th.textContent = 'Topics'; ts.appendChild(th);
    var pills = document.createElement('div'); pills.className = 'tpills';
    var cur = jget('newsBuddyTopics', null);
    TOPICS.forEach(function(t){
      var slug = t[0], name = t[1];
      var p = document.createElement('button');
      p.type = 'button'; p.className = 'tpill'; p.textContent = name;
      p.setAttribute('aria-pressed', (!cur || cur.indexOf(slug) !== -1) ? 'true' : 'false');
      p.addEventListener('click', function(){
        var now = jget('newsBuddyTopics', null);
        var list = now ? now.slice() : TOPICS.map(function(x){ return x[0]; });
        var ix = list.indexOf(slug);
        if (ix === -1) list.push(slug); else list.splice(ix, 1);
        jset('newsBuddyTopics', list);
        p.setAttribute('aria-pressed', ix === -1 ? 'true' : 'false');
        applyTopics();
      });
      pills.appendChild(p);
    });
    ts.appendChild(pills); card.appendChild(ts);

    var hs = document.createElement('div'); hs.className = 'set-sec';
    var hh = document.createElement('h4'); hh.textContent = 'Article images'; hs.appendChild(hh);
    var row = document.createElement('label'); row.className = 'set-row';
    var lab = document.createElement('span');
    lab.innerHTML = 'Show thumbnails<small>Pull the article\u2019s image into the card when one is available.</small>';
    var cb = document.createElement('input'); cb.type = 'checkbox';
    cb.checked = !!jget('newsBuddyThumbs', true);
    cb.addEventListener('change', function(){ jset('newsBuddyThumbs', cb.checked); applyThumbs(); });
    row.appendChild(lab); row.appendChild(cb); hs.appendChild(row); card.appendChild(hs);

    var vs = document.createElement('div'); vs.className = 'set-sec set-voice';
    var vh = document.createElement('h4'); vh.textContent = 'Reading voice'; vs.appendChild(vh);
    var vl = document.createElement('div'); vs.appendChild(vl); card.appendChild(vs);
    ov.appendChild(card);
    document.body.appendChild(ov);
    if (window.NBVoice) NBVoice.embedList(vl);
  }
})();

;

/* Per-section refresh: sends a fresh-batch request to the newsroom via docs/ingest.md. */
(function(){
  var heads = document.querySelectorAll('.sec-head');
  if (!heads.length) return;
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
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\n/g, '')), function(c){ return c.charCodeAt(0); })),
        sha: j.sha
      };
    } catch(e){}
    return null;
  }
  var box = document.querySelector('.dumpbox');
  var bid = (box && box.getAttribute('data-buddy-id')) || 'news-buddy';
  var repo = null;
  fetch('../buddies.json', {cache: 'no-store'}).then(function(r){ return r.json(); }).then(function(d){
    var buds = d.buddies || [];
    for (var i = 0; i < buds.length; i++) if (buds[i].id === bid && buds[i].repo) { repo = buds[i].repo; break; }
  }).catch(function(){});
  heads.forEach(function(head){
    var h2 = head.querySelector('h2'); if (!h2) return;
    var a = h2.querySelector('a'); if (!a) return;
    var name = h2.textContent.trim();
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'sec-refresh'; b.textContent = '↻';
    b.title = 'Get a fresh batch of ' + name + ' stories';
    b.setAttribute('aria-label', 'Refresh ' + name + ' stories');
    b.addEventListener('click', async function(){
      if (!token() || !repo) { b.title = 'Add a GitHub token in the brain-dump box first'; return; }
      b.disabled = true; b.textContent = '…';
      try {
        var NL = String.fromCharCode(10);
        var stamp = new Date().toLocaleString();
        var cur = await ghGetFile(repo, 'docs/ingest.md');
        var base = cur ? cur.text : '# News Buddy ingest' + NL + NL;
        var line = '## ' + stamp + NL + 'SECTION-REFRESH-REQUEST | ' + name + NL +
          'Dave tapped refresh on the ' + name + ' section — research a fresh batch of stories for this section.' + NL + NL;
        var body = {message: 'Section refresh request: ' + name, content: b64encode(base + line)};
        if (cur && cur.sha) body.sha = cur.sha;
        await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/ingest.md', 'PUT', body);
        b.textContent = '✓';
        setTimeout(function(){ b.textContent = '↻'; }, 2500);
      } catch(e){ b.textContent = '↻'; }
      b.disabled = false;
    });
    head.appendChild(b);
  });
})();

;

/* Suggestions box (section pages): like the brain dump, but writes to
   docs/suggestions.md \u2014 a separate box for readers' suggestions, not Dave's notes.
   No-token behavior: queue in a localStorage outbox, auto-flush when a token appears. */
(function(){
  var box = document.querySelector('.suggestbox');
  if (!box || box.dataset.sugInit) return;
  box.dataset.sugInit = '1';
  var bid = box.getAttribute('data-buddy-id') || 'news-buddy';
  var ta = box.querySelector('textarea'),
      btn = box.querySelector('.sug-btn'),
      st = box.querySelector('.sug-status');
  var OUTBOX = 'nb_sug_outbox_v1';
  function lsGet(){ try { return JSON.parse(localStorage.getItem('buddyTree.v3') || '{}'); } catch(e){ return {}; } }
  function token(){ return lsGet().ghToken || ''; }
  function getOutbox(){ try { var a = JSON.parse(localStorage.getItem(OUTBOX) || '[]'); return Array.isArray(a) ? a : []; } catch(e){ return []; } }
  function setOutbox(a){ try { localStorage.setItem(OUTBOX, JSON.stringify(a)); } catch(e){} }
  function b64encode(str){
    var bytes = new TextEncoder().encode(str), bin = '';
    bytes.forEach(function(b){ bin += String.fromCharCode(b); });
    return btoa(bin);
  }
  async function ghApi(path, method, body){
    var t = token();
    if (!t) throw new Error('no-token');
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
        text: new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\n/g, '')), function(c){ return c.charCodeAt(0); })),
        sha: j.sha
      };
    } catch(e){}
    return null;
  }
  var repo = null;
  fetch('../buddies.json', {cache: 'no-store'}).then(function(r){ return r.json(); }).then(function(d){
    var buds = d.buddies || [];
    for (var i = 0; i < buds.length; i++) if (buds[i].id === bid && buds[i].repo) { repo = buds[i].repo; break; }
    flushOutbox(true);
  }).catch(function(){});
  async function sendItem(item){
    var NL = String.fromCharCode(10);
    var cur = await ghGetFile(repo, 'docs/suggestions.md');
    var base = cur ? cur.text : '# Suggestions \u2014 News Buddy' + NL + NL +
      'Reader suggestions from the newspaper\u2019s section pages. Separate from Dave\u2019s brain dump (docs/ingest.md).' + NL + NL;
    var line = '## ' + item.stamp + NL + 'Page: ' + item.page + NL + NL + item.text + NL + NL;
    var body = {message: 'Reader suggestion for ' + bid, content: b64encode(base + line)};
    if (cur && cur.sha) body.sha = cur.sha;
    await ghApi('/repos/davedellaquila/' + repo + '/contents/docs/suggestions.md', 'PUT', body);
  }
  async function flushOutbox(quiet){
    var q = getOutbox();
    if (!q.length || !token() || !repo) return 0;
    var sent = 0;
    for (var i = 0; i < q.length; i++){
      try { await sendItem(q[i]); sent++; }
      catch(e){ break; }
    }
    if (sent) setOutbox(q.slice(sent));
    if (sent && !quiet) st.textContent = 'Sent ' + sent + ' saved suggestion' + (sent > 1 ? 's' : '') + ' to the newsroom.';
    return sent;
  }
  btn.addEventListener('click', async function(){
    var text = ta.value.trim();
    if (!text) { st.textContent = 'Write something first.'; return; }
    var item = {text: text, page: document.title || '', section: bid,
                stamp: new Date().toLocaleString()};
    if (!token() || !repo){
      var q = getOutbox(); q.push(item); setOutbox(q); ta.value = '';
      var n = q.length;
      st.textContent = 'Saved on this device (' + n + ' queued) \u2014 it\u2019ll be delivered to the newsroom inbox automatically once this device is connected. Nothing is lost.';
      return;
    }
    st.textContent = 'Sending\u2026'; btn.disabled = true;
    try {
      var sent = await flushOutbox(true);
      await sendItem(item);
      ta.value = '';
      var extra = sent ? ' (plus ' + sent + ' saved earlier)' : '';
      st.textContent = 'Thanks \u2014 suggestion sent to the newsroom.' + extra;
    } catch(e){ st.textContent = 'Couldn\u2019t send. Try again in a bit.'; }
    btn.disabled = false;
  });
  if (!token()){
    var pending = getOutbox().length;
    st.textContent = pending
      ? pending + ' suggestion' + (pending > 1 ? 's' : '') + ' saved on this device \u2014 ' + (pending > 1 ? 'they' : 'it') + '\u2019ll send automatically once the newsroom inbox is connected.'
      : 'No account needed \u2014 suggestions are delivered to the newsroom inbox.';
  }
})();

;
/* Card navigation: clicking a story card (outside links/buttons) opens its article detail page. */
(function(){
  document.querySelectorAll('article.story[data-article]').forEach(function(a){
    a.classList.add('clickable');
    a.addEventListener('click', function(ev){
      if (ev.target.closest('a,button')) return;
      window.location.href = a.getAttribute('data-article');
    });
  });
})();

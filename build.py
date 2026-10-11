#!/usr/bin/env python3
"""Build the Project Buddy dashboard (index.html) from buddies.json + the view fragments.

Usage: python3 build.py   (from this repo root)
Reads:  buddies.json, buddy-tree.html (style + the three view fragments)
Writes: index.html, version.txt
"""
import json
import os
import re
from datetime import datetime
BUILD_NUM = datetime.now().strftime('%Y%m%d.%H%M')

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT_ORDER = [
    "project-buddy",
    "personal-buddy", "family-buddy", "property-buddy", "finance-buddy", "work-buddy",
    "car-buddy", "mga-buddy", "ml500-buddy", "tv-buddy", "news-buddy", "wisdom-buddy", "birthday-buddy",
    "job-buddy", "reminder-buddy", "housing-buddy", "zen-buddy", "school-buddy",
    "document-buddy", "dream-buddy", "tech-buddy", "feedback-buddy",
    "scaffold-buddy", "buddy-suite",
]

NEW_CSS = """
/* ---- theme variables ---- */
:root{
  --bg:#0d1117; --panel:#161b22; --hover:#1c2128; --active:#1f6feb33;
  --wash:#1f6feb22; --wash2:#1c2b4a;
  --border:#30363d; --border2:#21262d;
  --text:#e6edf3; --text2:#c9d1d9; --muted:#8b949e; --faint:#6e7681;
  --accent:#1f6feb; --accent-hi:#58a6ff; --on-accent:#ffffff;
  --ghost:rgba(31,111,235,.12);
  --amber:#f0b429; --amber-bd:#7d5e00; --amber-bg:#3d2e00; --amber-bg2:#4d3a00;
  --amber-hi:#f0b429; --amber-tx:#f0b429; --amber-tx2:#e8c547;
  --grn-bg:#0f2c1a; --grn-bd:#1f6f43; --grn-tx:#3fb950; --grn-solid:#3fb950;
  --danger:#f85149;
  --shadow:rgba(0,0,0,.5); --shadow-soft:rgba(0,0,0,.3);
  --scrim:rgba(0,0,0,.6);
}
html.light{
  --bg:#ffffff; --panel:#f6f8fa; --hover:#eaeef2; --active:#ddf4ff;
  --wash:#ddf4ff; --wash2:#e8f0fe;
  --border:#d0d7de; --border2:#e5e8eb;
  --text:#1f2328; --text2:#424a53; --muted:#57606a; --faint:#6e7781;
  --accent:#0969da; --accent-hi:#0969da; --on-accent:#ffffff;
  --ghost:rgba(9,105,218,.08);
  --amber:#9a6700; --amber-bd:#d4a017; --amber-bg:#fff8c5; --amber-bg2:#ffef9e;
  --amber-hi:#9a6700; --amber-tx:#7d5e00; --amber-tx2:#9a6700;
  --grn-bg:#dafbe1; --grn-bd:#4ac26b; --grn-tx:#1a7f37; --grn-solid:#1a7f37;
  --danger:#cf222e;
  --shadow:rgba(31,35,40,.18); --shadow-soft:rgba(31,35,40,.08);
  --scrim:rgba(31,35,40,.5);
}
body{background:var(--bg);color:var(--text)}
.theme-pick{display:flex;margin:12px 10px 0;border:1px solid var(--border);border-radius:8px;overflow:hidden}
.theme-pick button{flex:1;background:none;border:none;color:var(--muted);font-size:11.5px;padding:6px 0;cursor:pointer;font:inherit}
.theme-pick button+button{border-left:1px solid var(--border)}
.theme-pick button.sel{background:var(--active);color:var(--text);font-weight:600}
.theme-pick button:hover:not(.sel){color:var(--text)}
/* ---- app shell ---- */
body{padding:0}
.app{display:flex;min-height:100vh;align-items:stretch}
#sidebar{width:308px;flex:0 0 308px;background:var(--bg);border-right:1px solid var(--border2);
  padding:0 14px 32px;position:sticky;top:0;height:100vh;overflow-y:auto;overflow-x:hidden;overflow-wrap:break-word;
  z-index:40;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
#main{flex:1;min-width:0;min-height:0;padding:36px 32px 80px;position:relative;z-index:1}
/* Desktop/tablet: lock the shell to the viewport so homepage wheel/trackpad
   never scrolls the document (and the sticky sidebar) on first paint. Each
   pane is its own scrollport; phone drawer layout keeps document scroll. */
@media (min-width:640px){
  html,body{height:100%;overflow:hidden}
  .app{height:100vh;height:100dvh;max-height:100vh;max-height:100dvh;min-height:0;overflow:hidden}
  #sidebar{position:relative;top:auto;height:auto;align-self:stretch;max-height:none;
    overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
  #main{align-self:stretch;height:auto;min-height:0;overflow-y:auto;overflow-x:hidden;
    overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
  #main.homepage-mode{display:flex;flex-direction:column;overflow:hidden;padding:0}
  #main.homepage-mode #view-project.active{flex:1 1 auto;min-height:0!important;height:auto;max-height:none}
  #homepage-wrap{flex:1 1 auto;min-height:0;height:auto;overflow:hidden}
  #homepage-frame{flex:1 1 auto;min-height:0;height:100%;width:100%}
  /* Tree fills the main pane — drop the old 100vh + negative-margin bleed */
  #main:has(#view-tree.active){padding:0;overflow:hidden}
  #view-tree.view.active{margin:0!important;height:100%!important;max-height:100%;box-sizing:border-box}
  /* Standalone buddy pages scroll the document again */
  body.standalone{height:auto;overflow:auto}
  body.standalone .app{height:auto;max-height:none;min-height:100vh;overflow:visible}
  body.standalone #main{overflow:visible;height:auto}
}
.brand{padding:22px 8px 14px;background:var(--bg)}
/* Brand chrome (eyebrow/title/subtitle + gear/close) pins at top; Views scroll under */
.sb-brand-sticky{
  position:sticky;top:0;z-index:7;background:var(--bg);
  margin:0 -14px;padding:0 14px;
  border-bottom:1px solid var(--border)}
.sb-brand-sticky #sb-tools{position:absolute;top:8px;right:8px;z-index:10}
/* Search stacks under brand sticky block; --sb-brand-h set from measured brand height */
.sb-search-sticky{
  position:sticky;top:var(--sb-brand-h,96px);z-index:6;background:var(--bg);
  margin:0 -14px;padding:10px 14px 10px;
  border-bottom:1px solid var(--border);
  box-shadow:0 8px 14px -10px rgba(0,0,0,.55)}
.sb-search-sticky #buddy-search{
  width:100%;box-sizing:border-box;background:var(--bg);border:1px solid var(--border);
  color:var(--text);border-radius:8px;padding:7px 10px;font-size:13px}
.brand .eyebrow{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
.brand h1{font-size:22px;margin:4px 0 0}
#brand-name{outline:none;border-bottom:2px dashed transparent;cursor:text;display:inline-block;min-width:60px}
#brand-name:hover{border-bottom-color:var(--border)}
#brand-name:focus{border-bottom-color:var(--accent)}
.brand .bcount{font-size:12.5px;color:var(--muted);margin-top:4px}
.nav-sec{margin-top:18px}
.nav-sec>h3{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);
  margin:0 8px 8px;display:flex;align-items:center;gap:8px}
#attn-pill{background:var(--accent);color:var(--on-accent);font-size:11px;font-weight:700;border-radius:999px;
  padding:1px 8px;letter-spacing:0;text-transform:none}
#attn-pill.zero{background:var(--border2);color:var(--muted)}
.navbtn{display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:none;border:0;
  color:var(--text);font:inherit;font-size:14px;padding:8px 10px;border-radius:8px;cursor:pointer}
.navbtn:hover{background:var(--hover)}
.navbtn.sel{background:var(--active);box-shadow:inset 2px 0 0 var(--accent)}
.navbtn .nic{width:20px;text-align:center;color:var(--muted)}
/* Views always stack vertically (desktop + iPad); phone keeps the same */
#view-nav{display:flex;flex-direction:column;gap:2px}
#view-nav .navbtn{flex:none;width:100%}
.brow{display:flex;align-items:center;gap:8px;width:100%;text-align:left;background:none;border:0;
  color:var(--text);font:inherit;font-size:13.5px;padding:6px 10px 6px 8px;border-radius:8px;cursor:pointer}
.brow:hover{background:var(--hover)}
.brow:hover .binfo{opacity:0.7 !important}
.brow.sel{background:var(--active);box-shadow:inset 2px 0 0 var(--accent)}
.bdot{width:8px;height:8px;border-radius:50%;background:var(--accent);flex:0 0 8px;visibility:hidden}
.brow.has-unseen .bdot{visibility:visible}
.bname{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bkind{font-size:10px;color:var(--faint);letter-spacing:.5px;text-transform:uppercase}
.bicon{width:20px;flex:0 0 20px;text-align:center;font-size:15px}
.brow.dragging{opacity:.35}
.brow.drop-target{background:var(--active);box-shadow:inset 0 0 0 2px var(--accent)}
.bp-icon{font-size:38px;line-height:1}
.toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%);background:var(--panel);
  border:1px solid var(--accent);color:var(--text);padding:10px 20px;border-radius:999px;
  font-size:14px;z-index:99;box-shadow:0 4px 24px var(--shadow);white-space:nowrap;
  max-width:92vw;overflow:hidden;text-overflow:ellipsis}
.treewrap{position:relative;display:flex;gap:10px;align-items:flex-start}
/* Beat .view.active{display:block} so the tree fills the viewport and #treezoom
   alone scrolls in both axes (fixes iOS axis-lock from nested X/Y scrollers). */
#view-tree.view.active{display:flex !important;flex-direction:column;
  margin:-36px -32px -80px;height:100vh;height:100dvh;overflow:hidden;min-height:0}
#view-tree #zoomwrap{flex:1;min-height:0;min-width:0;align-items:stretch;display:flex;flex-direction:column}
/* Single 2D scrollport: both axes together (no nested .chart / #view-tree scroll) */
#treezoom{flex:1;min-width:0;min-height:0;overflow:auto;overscroll-behavior:contain;
  border:1px solid var(--border);border-left:none;border-right:none;cursor:grab;border-radius:0;background:var(--bg);
  -webkit-overflow-scrolling:touch}
#treezoom.panning{cursor:grabbing}
/* JS pan owns gestures on the tree canvas so touch can move X+Y at once */
#treezoom{touch-action:none}
#view-projects,#view-manifest{touch-action:pan-x pan-y}
#treezoom.panning,#treezoom.panning *{user-select:none!important;-webkit-user-select:none!important}
#treezoom,#treezoom *{user-select:none;-webkit-user-select:none}
/* Slim vertical zoom — right edge of the tree; no panel chrome; large◼ · slider · small▪ · fit */
#zoombar{position:fixed;top:50%;right:10px;left:auto;transform:translateY(-50%);z-index:5;
  display:flex;flex-direction:column;align-items:center;gap:6px;width:auto;height:auto;
  padding:0;margin:0;background:none;border:none;border-radius:0;box-shadow:none;
  -webkit-tap-highlight-color:transparent}
#zoombar .z-out,#zoombar .z-in{flex:0 0 auto;line-height:1;color:var(--faint);user-select:none;pointer-events:none;
  text-shadow:0 0 4px var(--bg),0 0 8px var(--bg)}
#zoombar .z-out{font-size:8px}   /* zoom out (bottom) */
#zoombar .z-in{font-size:13px}   /* zoom in (top) */
#zoomrange{flex:0 0 auto;width:22px;height:112px;margin:0;padding:0;
  writing-mode:vertical-lr;direction:rtl;/* high value at top, next to large mark */
  -webkit-appearance:slider-vertical;appearance:slider-vertical;
  accent-color:var(--accent);cursor:ns-resize;touch-action:none;background:transparent;opacity:.9}
#zoomfit{flex:0 0 auto;background:none;border:none;border-radius:6px;color:var(--faint);
  font-size:12px;width:22px;height:22px;padding:0;cursor:pointer;line-height:1;
  text-shadow:0 0 4px var(--bg),0 0 8px var(--bg)}
#zoomfit:hover{color:var(--text);background:transparent}
/* Fixed to viewport at sidebar edge so vertical #sidebar scroll doesn't move it.
   MUST be a DOM sibling of #sidebar (not a child): overflow on #sidebar clips
   hit-testing/paint for fixed descendants, which made the gripper invisible. */
#sb-resize{position:fixed;top:0;left:calc(var(--sbw, 308px) - 7px);z-index:50;
  display:flex;align-items:center;justify-content:center;width:14px;height:100vh;height:100dvh;cursor:ew-resize;
  background:transparent;-webkit-tap-highlight-color:transparent}
/* Vertical sheet-handle pill (reference rotated 90°) — thin, fully rounded, flat gray */
#sb-resize::after{content:'';width:5px;height:48px;border-radius:999px;background:var(--muted);
  border:none;box-shadow:none}
#sb-resize:hover::after{background:var(--text2)}
#sb-resize:hover{background:transparent}
body.sb-closed #sb-resize{display:none}
/* Phone drawer: stay fixed (sibling of #sidebar); show only while drawer is open */
@media (max-width:639px){
  #sb-resize{display:none;left:calc(var(--sbw, 308px) - 14px);width:28px;z-index:96}
  #sidebar.open ~ #sb-resize{display:flex}
  #sb-resize::after{width:5px;height:56px}
}
/* Sidebar scroll-to-top — Muse-ish frosted chip, pinned to bottom of left panel */
#sb-to-top{position:fixed;bottom:16px;left:calc(var(--sbw, 308px) / 2 - 22px);z-index:48;
  width:44px;height:44px;border-radius:12px;padding:0;
  display:flex;align-items:center;justify-content:center;
  background:color-mix(in srgb, var(--panel) 78%, transparent);border:1px solid var(--border);
  color:var(--muted);cursor:pointer;
  box-shadow:0 2px 14px var(--shadow);
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);
  opacity:0;pointer-events:none;transform:translateY(6px);
  transition:opacity .18s ease,transform .18s ease,color .15s,border-color .15s;
  -webkit-tap-highlight-color:transparent}
#sb-to-top.show{opacity:1;pointer-events:auto;transform:none}
#sb-to-top:hover{color:var(--accent);border-color:var(--accent)}
#sb-to-top:active{transform:scale(.96)}
#sb-to-top svg{display:block}
body.sb-closed #sb-to-top,
body.standalone #sb-to-top{opacity:0!important;pointer-events:none!important}
@media (max-width:639px){
  #sb-to-top{bottom:20px;z-index:101;left:calc(var(--sbw, 308px) / 2 - 22px)}
  /* Only while the drawer is open — sibling selector */
  #sb-to-top{opacity:0;pointer-events:none}
  #sidebar.open ~ #sb-to-top.show{opacity:1;pointer-events:auto}
}
.bp-topnav{display:flex;gap:4px;align-items:center;margin-bottom:6px;flex-wrap:wrap}
.bp-topnav .sep{color:var(--faint);margin:0 2px}
/* Takeover back bar: hidden everywhere except the portrait-phone takeover (see below) */
.bp-takeover-back{display:none;align-items:center;gap:4px;position:sticky;top:0;z-index:20;
  width:calc(100% + 36px);margin:0 -18px 4px;padding:14px 18px;min-height:52px;
  background:var(--bg);border:none;border-bottom:1px solid var(--border);
  color:var(--accent);font-size:17px;font-weight:600;text-align:left;cursor:pointer;
  -webkit-tap-highlight-color:transparent}
.bp-takeover-back:active{opacity:.6}
/* Phone drawer above an open detail sheet (swipe-from-panel / menu) */
@media (max-width:639px){
  #sidebar.open{z-index:100}
  #sb-scrim.show{z-index:99}
}
@keyframes takeoverIn{from{transform:translateX(60px);opacity:.4}to{transform:none;opacity:1}}
#journal-bar{display:none;margin:0 0 12px;background:var(--wash);border:1px solid var(--accent);border-radius:10px;padding:9px 13px;font-size:13px}
#journal-bar.show{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
#journal-bar ul{margin:8px 0 4px;padding-left:18px;display:none}
#journal-bar.open ul{display:block}
#journal-bar li{margin:3px 0;color:var(--text2)}
.jchg{color:var(--muted);font-size:12px;margin:0 8px}
.cl-day{font-size:20px;font-weight:700;color:var(--text);margin:28px 0 12px}
.cl-day:first-child{margin-top:0}
.cl-group{display:flex;flex-direction:column;gap:4px}
.cl-row{display:flex;gap:14px;align-items:flex-start;padding:12px 8px;border-radius:12px}
.cl-row[data-buddy]{cursor:pointer}
.cl-row[data-buddy]:hover{background:var(--hover)}
.cl-row:hover{background:var(--ghost)}
.cl-ic{font-size:18px;line-height:1;flex:0 0 auto;width:44px;height:44px;border-radius:12px;background:var(--wash2);display:flex;align-items:center;justify-content:center}
.cl-body{flex:1;min-width:0;padding-top:2px}
.cl-title{font-size:15px;font-weight:600;color:var(--text);line-height:1.3}
.cl-desc{font-size:13.5px;color:var(--muted);margin-top:3px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cl-time{font-size:12px;color:var(--faint);margin-top:4px;white-space:nowrap}
#journal-bar .jtime{color:var(--faint);font-size:11px;margin-left:6px}
.pdrop{border:2px dashed var(--border);border-radius:12px;padding:20px;text-align:center;color:var(--muted);font-size:13px;margin-top:10px;cursor:pointer}
.pdrop.over{border-color:var(--accent);background:var(--wash);color:var(--text)}
.pstrip:empty{display:none}
.ghtoken{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;align-items:center}
#token-banner{display:none;border:2px solid var(--amber-bd);background:var(--amber-bg);border-radius:12px;padding:14px 16px;margin-bottom:18px}
#token-banner.show{display:block}
#token-banner h4{margin:0 0 6px;font-size:14px;color:var(--text)}
#token-banner p{margin:0 0 10px;font-size:13px;color:var(--amber-tx)}
#token-banner .ghtoken{margin-top:0}
.locked{opacity:.45;pointer-events:none}
textarea[disabled]{opacity:.5;cursor:not-allowed}
.tokenwarn{background:var(--amber-bg2);border:2px solid var(--amber-bd);color:var(--amber);border-radius:10px;padding:14px 16px;font-size:14px;margin-top:8px;line-height:1.6}
.tokenwarn a{color:var(--amber-hi);font-weight:bold}
.tokenwarn b{color:var(--amber-tx2)}
#token-pill{position:fixed;top:12px;right:12px;z-index:1000;display:flex;align-items:center;gap:6px;
  padding:8px 14px;border-radius:20px;font-size:13px;font-weight:600;cursor:pointer;border:2px solid;transition:all .2s}
#token-pill.need{background:var(--amber-bg2);border-color:var(--amber-bd);color:var(--amber-hi)}
#token-pill.ok{background:var(--grn-bg);border-color:var(--grn-bd);color:var(--grn-tx)}
#token-pill:hover{transform:scale(1.05)}
#token-pop{position:fixed;top:52px;right:12px;z-index:1001;background:var(--panel);border:1px solid var(--border);border-radius:12px;
  padding:16px;width:300px;display:none;box-shadow:0 8px 24px var(--shadow)}
#token-pop.show{display:block}
#token-pop h4{margin:0 0 8px;font-size:14px}
#token-pop p{margin:0 0 10px;font-size:12px;color:var(--muted);line-height:1.5}
#token-pop input{width:100%;box-sizing:border-box;background:var(--bg);border:1px solid var(--border);color:var(--text);
  border-radius:8px;padding:8px 10px;font-size:13px;margin-bottom:10px}
#token-pop .saved-check{display:none;color:var(--grn-tx);font-size:14px;font-weight:600;margin-top:8px}
#token-pop .saved-check.show{display:block}
/* Reopen right detail panel when closed — left chevron (expand toward content) */
#panel-open{position:fixed;top:12px;right:12px;z-index:85;width:44px;height:44px;border-radius:12px;
  background:var(--panel);border:1px solid var(--border);color:var(--muted);cursor:pointer;
  display:flex;align-items:center;justify-content:center;padding:0;
  box-shadow:0 2px 14px var(--shadow);-webkit-tap-highlight-color:transparent;transition:border-color .15s,color .15s,transform .15s}
#panel-open:hover{color:var(--accent);border-color:var(--accent);transform:scale(1.05)}
#panel-open:active{transform:scale(.96)}
#panel-open svg{display:block}
body:has(#view-buddy.active) #panel-open,
body.standalone #panel-open{display:none}
body:has(#token-pill) #panel-open{right:148px}
.ctog{display:none;width:18px;height:18px;flex:0 0 18px;align-items:center;justify-content:center;
  background:none;border:none;color:var(--muted);cursor:pointer;font-size:10px;padding:0;margin-right:2px}
.brow:hover .ctog.has-kids{display:inline-flex}
.ctog.has-kids.collapsed{transform:rotate(-90deg)}
#field-settings{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2000;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;width:340px;max-height:80vh;
  box-shadow:0 12px 40px var(--scrim);display:none;overflow:hidden}
#field-settings.show{display:flex;flex-direction:column}
#field-settings .fset-head{padding:20px 20px 0;cursor:move;user-select:none;-webkit-user-select:none;flex:0 0 auto}
#field-settings .fset-head h3{margin:0 0 12px;font-size:14px}
#field-settings .fset-body{padding:0 20px 16px;overflow-y:auto;flex:1 1 auto;min-height:0}
#field-settings .fset-sec{margin:0}
#field-settings .fset-sec-h{position:sticky;top:0;z-index:3;margin:0;padding:12px 0 8px;font-size:13px;
  letter-spacing:.02em;background:var(--panel);border-bottom:1px solid var(--border);color:var(--text)}
#field-settings .fset-sec + .fset-sec .fset-sec-h{margin-top:8px}
#field-settings .fset-sec .fineprint{margin:10px 0 12px}
#field-settings .fset-footer{padding:12px 20px;border-top:1px solid var(--border);display:flex;gap:8px;justify-content:space-between;align-items:center;background:var(--panel);flex:0 0 auto}
#field-settings .fset-resize{position:absolute;right:3px;bottom:3px;width:14px;height:14px;cursor:nwse-resize;opacity:.55;
  background:linear-gradient(135deg,transparent 55%,var(--muted) 55%);border-radius:0 0 8px 0}
#field-settings .fset-resize:hover{opacity:1}
#field-settings .fset-close-x{position:absolute;top:12px;right:12px;width:30px;height:30px;border-radius:50%;
  border:1px solid var(--border);background:linear-gradient(135deg,var(--panel),var(--wash));color:var(--muted);cursor:pointer;
  display:flex;align-items:center;justify-content:center;font-size:14px;line-height:1;padding:0;
  box-shadow:0 2px 8px rgba(0,0,0,.08);transition:all .15s ease}
#field-settings .fset-close-x:hover{color:#fff;background:linear-gradient(135deg,#e0533d,#c23e2a);border-color:#c23e2a;box-shadow:0 2px 12px rgba(224,83,61,.3);transform:scale(1.05)}
.fset-row{display:flex;align-items:center;gap:8px;padding:8px;border:1px solid var(--border2);border-radius:8px;margin-bottom:6px;background:var(--bg);cursor:grab}
.fset-row .fh{touch-action:none;cursor:grab;padding:4px 8px;font-size:18px;min-width:44px;min-height:44px;display:flex;align-items:center;justify-content:center;color:var(--muted)}
.fset-row .fl{flex:1;font-size:13px}
/* Settings list DnD feedback: dim source, dashed insert line, elevated ghost */
.fset-row.dragging{opacity:.32;border-style:dashed;background:var(--wash)}
.fset-insert{height:0;margin:-1px 2px 5px;border:0;border-top:2px dashed var(--accent);
  box-shadow:0 0 0 1px color-mix(in srgb, var(--accent) 35%, transparent);pointer-events:none}
#fset-ghost{position:fixed;z-index:4000;pointer-events:none;margin:0;opacity:.95;
  box-shadow:0 12px 32px rgba(0,0,0,.55);border-color:var(--accent);transform:scale(1.03);
  background:var(--panel)}
/* Circle-check settings toggles (checkmark.circle.fill style) */
.fset-check{display:flex;align-items:center;gap:12px;margin-top:8px;padding:11px 12px;font-size:13.5px;
  cursor:pointer;border:1px solid var(--border2);border-radius:10px;background:var(--bg);user-select:none;-webkit-user-select:none}
.fset-check:hover{border-color:var(--border);background:var(--hover)}
.fset-check:has(input:checked){border-color:color-mix(in srgb, var(--accent) 45%, var(--border));background:var(--wash)}
#field-settings input[type=checkbox]{
  -webkit-appearance:none;appearance:none;width:28px;height:28px;margin:0;flex:0 0 28px;
  border:2px solid var(--border);border-radius:50%;background:var(--panel);cursor:pointer;
  position:relative;transition:background .15s ease,border-color .15s ease,box-shadow .15s ease,transform .12s ease}
#field-settings input[type=checkbox]:hover{border-color:var(--accent);background:var(--ghost)}
#field-settings input[type=checkbox]:checked{background:var(--accent);border-color:var(--accent)}
#field-settings input[type=checkbox]:checked::after{
  content:'';position:absolute;left:9px;top:4px;width:6px;height:12px;
  border:solid var(--on-accent);border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
#field-settings input[type=checkbox]:focus-visible{outline:none;box-shadow:0 0 0 3px var(--ghost)}
#field-settings input[type=checkbox]:active{transform:scale(.92)}
.fset-row input[type=checkbox]{margin-left:2px}
.bp-close-x{position:static;flex:0 0 auto;width:44px;height:44px;margin-left:auto;
  background:none;border:1px solid transparent;border-radius:10px;color:var(--muted);
  cursor:pointer;display:none;align-items:center;justify-content:center;padding:0;
  -webkit-tap-highlight-color:transparent}
.bp-close-x:hover{color:var(--text);border-color:var(--border);background:var(--ghost)}
.bp-close-x:active{opacity:.7}
.bp-close-x svg{display:block}
#view-buddy.panel .bp-close-x,#view-buddy.sheet .bp-close-x{display:flex}
/* Portrait takeover uses the sticky back bar; keep collapse chevron for panel / landscape sheet */
@media (max-width:639px) and (orientation:portrait){
  #view-buddy.sheet .bp-close-x{display:none}
}
#buddy-home{position:relative}
#bp-resize{position:absolute;top:0;left:0;z-index:60;display:flex;align-items:center;justify-content:center;width:14px;height:100vh;cursor:ew-resize;
  background:transparent;-webkit-tap-highlight-color:transparent}
/* Same vertical pill language as #sb-resize */
#bp-resize::after{content:'';width:5px;height:48px;border-radius:999px;background:var(--muted);
  border:none;box-shadow:none}
#bp-resize:hover::after{background:var(--text2)}
#bp-resize:hover{background:transparent}
#view-buddy.active:not(.panel):not(.sheet) #bp-resize{display:none}
.pupload{height:150px;min-width:120px;border-radius:10px;border:1px dashed var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:var(--bg);flex:0 0 auto}
.pupload .pbar{width:80px;height:6px;background:var(--border2);border-radius:3px;overflow:hidden}
.pupload .pbar > div{height:100%;background:var(--accent);border-radius:3px;transition:width .2s}
.pupload .plabel{font-size:11px;color:var(--muted)}
.dumps-head{cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px;margin:12px 0 0}
.dumps-head h4{margin:0;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--muted)}
.dumps-head .darrow{font-size:25px;color:var(--muted);transition:transform .15s;display:inline-block;line-height:1;position:relative;top:-2px}
.bp-sec > h3{cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px}
.bp-sec > h3 .secgrip{cursor:grab;color:var(--faint);font-size:14px;line-height:1;padding:2px 4px;border-radius:4px}
.bp-sec > h3 .secgrip:hover{color:var(--muted);background:var(--ghost)}
.bp-sec > h3 .secgrip:active{cursor:grabbing}
.bp-sec.sec-dragging{opacity:0.4}
.bp-sec > h3 .secarrow{font-size:25px;color:var(--muted);transition:transform .15s;display:inline-block;line-height:1}
.bp-sec.collapsed > *:not(h3){display:none}
.bp-sec .secarrow{transform:rotate(90deg)}
.bp-sec.collapsed .secarrow{transform:rotate(0deg)}
.dumps .darrow{transform:rotate(90deg)}
.dumps.collapsed .darrow{transform:rotate(0deg)}
.dump-actions{position:absolute;top:10px;right:12px;display:flex;gap:8px;align-items:center}
.dump-act{background:none;border:none;cursor:pointer;opacity:.55;padding:3px;line-height:1;color:var(--muted);display:inline-flex;align-items:center}
.dump-act:hover{opacity:1;color:var(--text)}
.dump-act[data-dump-del]{color:#e0533d}
.dump-act[data-dump-del]:hover{color:#ff6b5b}
.dump-act svg{width:14px;height:14px;display:block}
body.no-write .pdel,body.no-write [data-dump-del],body.no-write [data-dump-edit]{display:none!important}
.dumps-body .attn-body{padding-right:64px}
.dumps.collapsed .dumps-body{display:none}
/* Sidebar top-right tools: gear + collapse chevron (44px targets, 8px gap — HIG touch spacing) */
#sb-tools{position:absolute;top:8px;right:8px;z-index:10;display:flex;align-items:center;gap:8px}
#sb-tools button{width:44px;height:44px;background:none;border:none;border-radius:10px;color:var(--muted);
  cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;-webkit-tap-highlight-color:transparent}
#sb-tools button:hover{background:var(--hover);color:var(--text)}
#sb-tools button svg{display:block}
#sb-gear{color:red}
#sb-gear:hover{color:red;background:var(--hover)}
#sb-close{color:var(--faint)}
#sb-close:hover{color:var(--muted)}
#sidebar .brand{padding-right:112px}
/* Collapsed sidebar (iPad/desktop): hide panel, show right-chevron to reopen */
body.sb-closed #sidebar{display:none}
body.sb-closed #menu-btn{display:flex;align-items:center;justify-content:center;position:fixed;top:12px;left:12px;z-index:90;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;color:var(--text);
  width:48px;height:48px;cursor:pointer;box-shadow:0 2px 12px var(--shadow)}
#menu-btn svg{display:block}
#plans-sec.collapsed #plan-nav{display:none}
#plans-sec #plans-arrow{transform:rotate(90deg);display:inline-block}
#plans-sec.collapsed #plans-arrow{transform:rotate(0deg)}

#avatar-picker{position:fixed;z-index:2000;background:var(--panel);border:1px solid var(--border);border-radius:12px;
  padding:16px;width:280px;display:none;box-shadow:0 12px 40px var(--scrim)}
#avatar-picker.show{display:block}
#avatar-picker h4{margin:0 0 10px;font-size:13px}
#avatar-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin-bottom:10px}
#avatar-grid button{background:none;border:1px solid transparent;border-radius:8px;font-size:20px;padding:6px;cursor:pointer}
#avatar-grid button:hover{border-color:var(--accent);background:var(--hover)}
#avatar-picker input{width:100%;box-sizing:border-box;background:var(--bg);border:1px solid var(--border);color:var(--text);
  border-radius:8px;padding:8px;font-size:14px;text-align:center}
.info-tip{position:relative;display:inline-block;margin-left:6px;cursor:help;color:var(--muted);font-size:12px}
.info-tip:hover{color:var(--text)}
.info-tip::after{content:attr(data-tip);text-transform:none;position:absolute;bottom:125%;left:-8px;transform:none;
  background:var(--panel);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:8px;font-size:12px;
  line-height:1.5;width:220px;white-space:normal;z-index:100;opacity:0;pointer-events:none;transition:opacity .15s}
.info-tip:hover::after{opacity:1}
.ghtoken input{flex:1;min-width:180px;background:var(--bg);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:7px 10px;font-size:13px}
.linkbtn{background:none;border:none;color:var(--accent);cursor:pointer;font-size:13px;padding:2px 4px}
.linkbtn:hover{text-decoration:underline}
.bp-topnav{margin-bottom:6px}
.bp-footer{margin:26px 0 6px;display:flex;flex-direction:column;align-items:center;gap:10px}
.bp-footer #bp-open-tab{display:inline-flex;align-items:center;justify-content:center;
  background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:999px;
  padding:8px 16px;font-size:13px;font-weight:600;text-decoration:none;
  box-shadow:0 2px 10px var(--shadow)}
.bp-footer #bp-open-tab:hover{border-color:var(--accent);color:var(--accent)}
.bp-build{margin:0;font-size:11px;color:var(--faint);text-align:center}
.pstrip{display:flex;gap:10px;overflow-x:auto;padding:2px 2px 6px}
.pstrip a{flex:0 0 auto}
/* ---- standalone buddy mode ---- */
body.standalone #sidebar{display:none}
body.standalone .app{display:block}
body.standalone #main{max-width:880px;margin:0 auto;padding:28px 24px 80px}
.sa-bar{display:none;align-items:center;gap:10px;margin-bottom:18px;padding:10px 14px;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;font-size:13px;color:var(--muted)}
body.standalone .sa-bar{display:flex}
.sa-bar .linkbtn{font-size:13px}

/* ============ RESPONSIVE ============ */
#menu-btn{display:none}
/* ---- Small: <640px (iPhone) ---- */
@media (max-width:639px){
  /* Phone drawer: document scrolls; undo desktop viewport lock */
  html,body{height:auto;overflow-x:clip;overflow-y:auto}
  .app{display:block;height:auto;max-height:none;min-height:0;overflow:visible}
  /* Prevent iOS auto-zoom on input focus */
  input, textarea, select{font-size:16px !important}
  #menu-btn{display:flex;align-items:center;justify-content:center;position:fixed;top:12px;left:12px;z-index:90;
    background:var(--panel);border:1px solid var(--border);border-radius:12px;color:var(--text);
    width:48px;height:48px;cursor:pointer;box-shadow:0 2px 12px var(--shadow)}
  /* Sidebar drawer with scrim */
  #sidebar{position:fixed;left:0;top:0;bottom:0;z-index:95;height:100vh;height:100dvh;
    transform:translateX(-105%);transition:transform .28s cubic-bezier(.32,.72,.35,1);width:min(85vw,340px);flex:none;
    overflow-y:auto;overflow-x:hidden}
  #sidebar.open{transform:none;box-shadow:12px 0 40px rgba(0,0,0,.35)}
  /* Sidebar resize: sibling of #sidebar; visibility gated by #sidebar.open ~ #sb-resize above */
  #sb-resize{touch-action:none}
  #main{overflow:visible;height:auto;min-height:0}
  #sb-scrim{display:none;position:fixed;inset:0;z-index:94;background:rgba(0,0,0,.45);opacity:0;transition:opacity .25s}
  #sb-scrim.show{display:block;opacity:1}
  #main{padding:72px 12px 60px}
  /* Tree keeps the org chart on phones — pan with a finger, zoom with the floating slider */
  .standalones .grid{display:block}
  /* Vertical zoom on the right — fat hit areas (≈44px), no filled panel */
  #zoombar{right:4px;z-index:30;padding:8px 4px;gap:4px}
  #zoomrange{width:44px;height:140px}
  #zoomfit{width:44px;height:44px;font-size:14px;display:flex;align-items:center;justify-content:center}
  #zoombar .z-out,#zoombar .z-in{padding:4px 0}
  /* Chunkier tree nodes for touch */
  #treezoom .node{padding:15px 14px;min-height:60px}
  /* Bottom sheet panel — taller, grabbable */
  #view-buddy.sheet{position:fixed;left:0;right:0;bottom:0;top:6%;z-index:96;
    background:var(--bg);border-top:1px solid var(--border);border-radius:20px 20px 0 0;
    overflow-y:auto;overflow-x:hidden;padding:8px 18px 60px;box-shadow:0 -12px 40px rgba(0,0,0,.35);
    -webkit-overflow-scrolling:touch}
  #view-buddy.sheet::before{content:'';display:block;width:48px;height:5px;border-radius:3px;
    background:var(--border);margin:4px auto 14px;flex:none}
  /* Plans: single column cards */
  .plan-grid{display:block;max-width:none}
  .plan-card{margin-bottom:12px}
  /* Projects outline: larger touch targets */
  .proj-row{padding:14px 12px;min-height:52px;border-radius:12px}
  .proj-row .pname{font-size:15px}
  /* Changelog entries */
  .cl-entry{padding:14px 12px}
  /* View nav: vertical list with larger touch targets */
  #view-nav{display:flex;flex-direction:column;gap:2px;overflow:visible;padding:0}
  #view-nav .navbtn{flex:none;width:100%;padding:10px 12px;font-size:15px;border-radius:12px;min-height:44px}
  /* Buddy list in sidebar */
  #buddy-nav .brow{min-height:52px;padding:10px 12px;border-radius:12px;font-size:15px}
  /* Search: full width, proper size */
  .sb-search-sticky{padding:10px 14px 12px}
  .sb-search-sticky #buddy-search,#buddy-search{font-size:16px;padding:12px 14px;border-radius:12px;width:100%}
  /* Settings gear: ensure reachable */
  #settings-btn{width:48px;height:48px;font-size:20px}
  /* Homepage iframe: fill safely */
  #view-project.active{min-height:calc(100dvh - 140px)}
  #homepage-frame{min-height:60vh}
  /* Detail panel content */
  .bp-wrap{padding:4px 2px}
  .bp-name{font-size:22px}
  /* Ensure buttons are tappable */
  button{cursor:pointer;-webkit-tap-highlight-color:transparent}
  .icon-btn,button.icon{width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center}
}
/* ---- Portrait phones: full-screen takeover instead of bottom sheet (Dave, 2026-10-10).
   iOS-style push navigation — one thing on screen at a time, no sidebar/panel crowding.
   Landscape phones are >=640px wide so they keep the bottom sheet above. */
@media (max-width:639px) and (orientation:portrait){
  #view-buddy.sheet{top:0;border-radius:0;border-top:none;padding:0 18px 60px;z-index:97;
    animation:takeoverIn .28s cubic-bezier(.32,.72,.35,1)}
  #view-buddy.sheet::before{display:none}
  #view-buddy.sheet #bp-resize{display:none}
  #view-buddy.sheet .bp-takeover-back{display:flex}
  #view-buddy.sheet .bp-sticky-head{top:53px}
}
/* ---- Medium: 640-1100px (iPad) ---- */
@media (min-width:640px) and (max-width:1100px){
  /* Keep a real left sidebar — do not stack above main (iPad portrait is ~744–834px).
     Scroll isolation comes from the ≥640px viewport-locked shell above. */
  .app{display:flex;flex-direction:row;align-items:stretch}
  #sidebar{width:250px;flex:0 0 250px;position:relative;top:auto;height:auto;align-self:stretch;
    max-height:none;border-right:1px solid var(--border2);border-bottom:0;overflow-y:auto;overflow-x:hidden;
    z-index:40;background:var(--bg);overscroll-behavior:contain}
  #main{flex:1;min-width:0;min-height:0;padding:28px 22px 64px;position:relative;z-index:1}
  #main.homepage-mode{padding:0}
  .node{width:172px}
  #view-buddy.panel{position:fixed;top:0;right:0;bottom:0;width:min(380px,calc(100vw - 250px));z-index:30;
    background:var(--bg);border-left:1px solid var(--border);overflow-y:auto;overflow-x:hidden;
    padding:20px 18px 48px;box-shadow:-8px 0 32px var(--shadow);overscroll-behavior:contain}
}
/* ---- Large: >1100px (desktop) ---- */
@media (min-width:1101px){
  #view-buddy.panel{position:fixed;top:0;right:0;bottom:0;width:400px;z-index:60;
    background:var(--bg);border-left:1px solid var(--border);overflow-y:auto;overflow-x:hidden;
    padding:24px 20px 48px;box-shadow:-8px 0 32px var(--shadow);overscroll-behavior:contain}
}
#view-buddy.panel.active,#view-buddy.sheet.active{display:block}
#main .view{display:none}
#main .view.active{display:block}
#main #view-project.active{display:flex;flex-direction:column;min-height:calc(100vh - 116px)}
#bp-close{display:none}
#view-buddy.panel #bp-close,#view-buddy.sheet #bp-close{display:inline-block}
/* ---------- Project view: stat tiles + buddy homepage embed ---------- */
#project-tiles{display:flex;gap:14px;margin:2px auto 20px;max-width:860px;flex-wrap:wrap}
#project-status-tiles{display:flex;gap:14px;margin:2px auto 20px;max-width:860px;flex-wrap:wrap}
#project-status-tiles .ptile{flex:1 1 180px;max-width:calc(25% - 11px)}
.ptile{flex:1 1 170px;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px 18px 12px;position:relative;overflow:hidden;cursor:pointer;transition:transform .15s ease,box-shadow .15s ease}
.ptile:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.12)}
.ptile::before{content:'';position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--tint)}
/* ---- Business Plans cards ---- */
.plan-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;max-width:860px;margin:0 auto}
.plan-card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px 20px;transition:transform .15s ease,box-shadow .15s ease}
.plan-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.12)}
.plan-card-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.plan-card-icon{font-size:24px}
.plan-card-name{font-size:16px;font-weight:700}
.plan-card-desc{font-size:13.5px;color:var(--muted);line-height:1.5;margin-bottom:12px}
.plan-card-link{display:inline-block;margin:4px 8px 0 0;font-size:13px;color:var(--accent);text-decoration:none}
.plan-card-link:hover{text-decoration:underline}
.ptile-label{font-size:11px;letter-spacing:.14em;font-weight:700;color:var(--muted)}
.ptile-num{font-size:42px;font-weight:800;color:var(--tint);line-height:1.25}
.ptile-sub{font-size:13px;color:var(--muted)}
.ptile[data-tile]{cursor:pointer}
.ptile.sel{box-shadow:inset 0 0 0 2px var(--tint)}
/* Phone tiles AFTER base .ptile so cascade wins (beat inline gap/display too) */
@media (max-width:639px){
  #project-tiles,#changelog-tiles,#plans-tiles,#manifest-tiles,#project-status-tiles{
    display:grid !important;grid-template-columns:1fr 1fr !important;
    gap:6px !important;max-width:none !important;width:100% !important;
    margin:0 0 12px !important;box-sizing:border-box;flex-wrap:unset !important}
  #project-tiles .ptile,#changelog-tiles .ptile,#plans-tiles .ptile,#manifest-tiles .ptile,
  #project-status-tiles .ptile{flex:none !important;max-width:none !important;min-width:0 !important}
  .ptile{padding:6px 8px 5px !important;border-radius:10px !important}
  .ptile::before{width:3px}
  .ptile-label{font-size:9px !important;letter-spacing:.08em;line-height:1.15}
  .ptile-num{font-size:18px !important;line-height:1.05 !important;margin:1px 0}
  .ptile-sub{font-size:10px !important;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
}
/* Landscape phones are often >639px wide — key off short height instead */
@media (orientation:landscape) and (max-height:520px){
  #project-tiles,#changelog-tiles,#plans-tiles,#manifest-tiles,#project-status-tiles{
    display:grid !important;grid-template-columns:repeat(auto-fit,minmax(96px,1fr)) !important;
    gap:6px !important;max-width:none !important;width:100% !important;
    margin:0 0 10px !important;box-sizing:border-box;flex-wrap:unset !important}
  #project-tiles .ptile,#changelog-tiles .ptile,#plans-tiles .ptile,#manifest-tiles .ptile,
  #project-status-tiles .ptile{flex:none !important;max-width:none !important;min-width:0 !important}
  .ptile{padding:5px 7px 4px !important;border-radius:10px !important}
  .ptile::before{width:3px}
  .ptile-label{font-size:9px !important;letter-spacing:.08em;line-height:1.15}
  .ptile-num{font-size:16px !important;line-height:1.05 !important;margin:1px 0}
  .ptile-sub{font-size:10px !important;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
}
#main.homepage-mode{padding:0}
/* Phone / short layouts still size the project view to the viewport; desktop
   homepage fill is handled by the ≥640px locked-shell rules above. */
#main.homepage-mode #view-project.active{min-height:100vh}
#homepage-wrap{flex:1;display:flex;flex-direction:column;min-height:0;margin:0;position:relative}
#homepage-frame{flex:1;width:100%;min-height:0;border:0;border-radius:0;background:#fff;display:block}
@media (max-width:639px){
  #main #view-project.active{min-height:calc(100vh - 88px)}
  #main.homepage-mode{padding:0}
  #main.homepage-mode #view-project.active{min-height:100vh}
}

.pstrip img{height:150px;border-radius:10px;border:1px solid var(--border);display:block}
.pstrip img:hover{border-color:var(--accent)}
.pwrap{position:relative;flex:0 0 auto}
.pdel{position:absolute;top:6px;right:6px;width:24px;height:24px;border-radius:50%;background:var(--scrim);
  color:#e0533d;border:none;cursor:pointer;display:none;align-items:center;justify-content:center;line-height:1}
.pwrap:hover .pdel{display:flex}
.pdel:hover{background:var(--danger);color:#fff}
.pdel svg{width:13px;height:13px;display:block}
.node.drop-target{outline:2px solid var(--accent);outline-offset:3px}
.proj-row.drop-target{background:var(--active);box-shadow:inset 0 0 0 2px var(--accent)}
#view-projects .proj-row[data-buddy]{cursor:pointer}
/* ---- buddy homepage ---- */
.bp-wrap{max-width:880px;margin:0 auto;padding:6px 4px}
.bp-crumb{font-size:12.5px;color:var(--muted);margin-bottom:10px}
.bp-crumb .reposlug{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:600}
.bp-crumb b{color:var(--text);font-weight:600}
.bp-top{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
/* Compact sticky identity bar — one row; nav / crumb / tagline scroll away */
.bp-sticky-head{position:sticky;top:0;z-index:6;background:var(--bg);
  padding:6px 0;margin:0 0 2px;border-bottom:1px solid var(--border)}
.bp-sticky-head .bp-top{gap:8px;flex-wrap:nowrap;min-width:0;align-items:center}
.bp-sticky-head .bp-icon{font-size:20px;line-height:1;flex:0 0 auto}
.bp-sticky-head .bp-name{font-size:16px;font-weight:700;margin:0;padding:0;min-width:0;
  flex:1 1 auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  border-bottom-width:1px}
.bp-sticky-head .status{flex:0 1 auto;max-width:36%;overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap;font-size:11px;padding:2px 8px;line-height:1.25}
.bp-name{font-size:32px;font-weight:700;margin:0;outline:none;border-bottom:2px dashed transparent;
  padding-bottom:2px;min-width:120px}
.bp-name:hover{border-bottom-color:var(--border)}
.bp-name:focus{border-bottom-color:var(--accent);background:var(--wash2)}
.bp-tagline{color:var(--muted);font-size:15px;margin:4px 0 8px}
.bp-sec{margin-top:30px}
.bp-sec>h3{font-size:13px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin:0 0 12px}
.bp-sec[data-field="attention"]>h3{color:var(--amber)}
.bp-mission{font-size:15.5px;line-height:1.7;background:var(--panel);border:1px solid var(--border);
  border-radius:12px;padding:16px 18px;margin:0}
.art-row{display:flex;align-items:center;gap:14px;padding:11px 14px;border:1px solid var(--border2);
  border-radius:12px;margin-bottom:10px;text-decoration:none;color:inherit;background:var(--bg)}
.art-row:hover{border-color:var(--accent);background:var(--hover)}
.art-ic{width:38px;height:38px;border-radius:10px;background:var(--panel);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;flex:0 0 38px;color:var(--muted)}
.art-label{font-weight:650;font-size:14.5px}
.art-sub{font-size:12.5px;color:var(--muted);margin-top:2px}
.art-go{margin-left:auto;color:var(--faint);font-size:18px}
.attn{position:relative;background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:13px 15px;
  margin-bottom:10px;display:flex;gap:12px;align-items:flex-start}
.attn.unseen{border-color:var(--accent);background:var(--wash)}
.attn .adot{width:9px;height:9px;border-radius:50%;background:var(--accent);margin-top:6px;flex:0 0 9px;visibility:hidden}
.attn.unseen .adot{visibility:visible}
.attn-body{flex:1;min-width:0}
.attn-text{font-size:14.5px;line-height:1.5}
.attn-date{font-size:12px;color:var(--muted);margin-top:5px}
.seenbtn{flex:0 0 auto;background:var(--border2);border:1px solid var(--border);color:var(--text);font:inherit;
  font-size:12.5px;padding:6px 12px;border-radius:999px;cursor:pointer}
.seenbtn:hover{border-color:var(--accent)}
.attn.seen{opacity:.55}
.attn.seen .adot{visibility:visible;background:var(--grn-solid);width:18px;height:18px;flex:0 0 18px;
  display:flex;align-items:center;justify-content:center;color:var(--on-accent);font-size:11px;font-weight:700}
.attn.seen .adot::after{content:'\\2713'}
.attn.seen .seenbtn{visibility:hidden}
.attn-all{margin-top:6px}
/* Standing orders — broadcast to every buddy detail (agents + Dave) */
.standing-order{margin:10px 0 4px;padding:10px 12px;border-radius:10px;border:1px solid var(--amber-bd);
  background:var(--amber-bg);font-size:13.5px;line-height:1.45;color:var(--amber-tx)}
.standing-order.critical{border-color:var(--amber-bd)}
.standing-order b{color:var(--amber-hi)}
.standing-order a{color:var(--accent-hi)}
.standing-order .so-date{display:block;margin-top:4px;font-size:11px;color:var(--muted)}
.notes{width:100%;min-height:120px;background:var(--bg);border:1px solid var(--border);border-radius:12px;
  color:var(--text);font:inherit;font-size:14.5px;line-height:1.6;padding:13px 15px;resize:vertical}
.notes:focus{outline:none;border-color:var(--accent)}
.fineprint{font-size:12.5px;color:var(--faint);margin-top:8px;line-height:1.5}
.bp-empty{color:var(--muted);font-size:14px}
.proj-row[data-plan]{cursor:pointer}
.proj-row[data-plan]:hover{background:var(--hover)}
.bp-tree-wrap{border:1px solid var(--border2);border-radius:12px;background:var(--bg);overflow:auto;position:relative;height:420px;cursor:grab}
.bp-tree-wrap.panning{cursor:grabbing}
.bp-mini-zoom{position:absolute;top:8px;right:8px;z-index:5;display:flex;gap:4px}
.bp-mini-zoom button{background:color-mix(in srgb, var(--panel) 94%, transparent);border:1px solid var(--border);color:var(--text);border-radius:8px;width:28px;height:28px;font-size:14px;cursor:pointer}
.bp-mini-zoom button:hover{border-color:var(--accent)}
.linkbtn{background:none;border:0;color:var(--accent);font:inherit;font-size:12.5px;cursor:pointer;padding:0}
.linkbtn:hover{text-decoration:underline}
.node{position:relative;}
/* Fix: flex-centered org tree overflows to negative x-coords on narrow screens, which widens the
   layout viewport and pushes position:fixed UI (zoombar) partly off-screen. max-content + auto
   margins keeps the centered look when it fits, and overflows only rightward (scrollable) when not. */
.tree{justify-content:flex-start;width:max-content;margin:0 auto}
/* ---- tree node drag-to-reparent (pointer-based; mouse + touch) ---- */
#treezoom .node[data-buddy]:not(.root){touch-action:none;cursor:grab}
#treezoom .node[data-buddy]:not(.root):active{cursor:grabbing}
#treezoom .node.drag-src{opacity:.35}
#treezoom .node.drop-invalid{outline:2px dashed #e0533d;outline-offset:3px}
.node-drag-ghost{position:fixed;left:0;top:0;z-index:9999;pointer-events:none;width:196px;opacity:.94;
  transform:translate(-50%,-118%) rotate(-2deg);
  background:#161b22;border:1px solid #58a6ff;border-top:3px solid #58a6ff;
  border-radius:10px;padding:12px 12px 13px;box-shadow:0 12px 32px rgba(0,0,0,.55);
  color:#e6edf3;font-size:15px}
.node-drag-ghost .name{font-weight:700;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
body.node-dragging,body.node-dragging *{cursor:grabbing !important}
/* Chunkier drag/drop affordances on touch devices */
@media (pointer:coarse){
  .node-drag-ghost{width:240px;font-size:17px;padding:16px 16px 17px}
  .node-drag-ghost .name{font-size:17px}
  .node.drop-target{outline-width:3px;outline-offset:5px}
  #treezoom .node.drop-invalid{outline-offset:5px}
}
"""

ICON_DOC = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
            ' stroke-width="1.5"><path d="M4 1.5h5.5L12.5 4.5v10h-8.5z"/>'
            '<path d="M9.5 1.5v3h3M6 8.5h4M6 11h4"/></svg>')
ICON_REPO = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
             ' stroke-width="1.5"><rect x="2" y="2" width="12" height="12" rx="2"/>'
             '<path d="M5.5 5.5l-2 2 2 2M10.5 5.5l2 2-2 2"/></svg>')
ICON_LINK = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor"'
             ' stroke-width="1.5"><path d="M6.5 9.5l3-3M7.5 5.5l1.5-1.5a2.5 2.5 0 013.5 3.5L11 9"/>'
             '<path d="M8.5 10.5L7 12a2.5 2.5 0 01-3.5-3.5L5 7"/></svg>')
ICON_TRASH = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
             ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/>'
             '<path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
             '<path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>'
             '<line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>')
ICON_EDIT = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
            ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M17 3a2.83 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build():
    data = json.load(open(f"{HERE}/buddies.json"))
    buddies = data["buddies"]
    frag = open(f"{HERE}/buddy-tree.html").read()

    style = frag.split("<style>", 1)[1].split("</style>", 1)[0]
    vt = frag.split('<div id="view-tree"', 1)[1].split('<div id="view-projects"', 1)[0]
    vp = frag.split('<div id="view-projects"', 1)[1].split('<div id="view-manifest"', 1)[0]
    vm = frag.split('<div id="view-manifest"', 1)[1].split('<footer class="legend">', 1)[0]
    vt = '<div id="view-tree"' + vt.replace('class="view active"', 'class="view"', 1)
    vp = '<div id="view-projects"' + vp
    vm = '<div id="view-manifest"' + vm

    buddies_js = json.dumps(buddies)
    order_js = json.dumps(ROOT_ORDER)
    plans = json.load(open(f"{HERE}/plans.json"))["plans"]
    plans_js = json.dumps(plans)
    n_buddies = len(buddies)

    plan_rows = "".join(
        f'<div class="plan-card" data-plan="{p["id"]}" data-status="{esc(p["status"])}">'
        f'<div class="plan-card-head"><span class="plan-card-icon">{esc(p["icon"])}</span>'
        f'<span class="plan-card-name">{esc(p["name"])}</span>'
        f'<span class="status {p["statusClass"]}" style="margin-left:auto">{esc(p["status"])}</span></div>'
        f'<div class="plan-card-desc">{esc(p["desc"][:200])}{"…" if len(p["desc"]) > 200 else ""}</div>'
        + ("".join(
            f'<a class="plan-card-link" href="{esc(d["url"])}" target="_blank" rel="noopener">📄 {esc(d["label"])}</a>'
            for d in p.get("docs", [])
        ))
        + '</div>'
        for p in plans
    )
    status_tints = {'Live': '#2f9e44', 'Active': '#1f6feb', 'Mission review': '#a371f7',
                    'Exploring': '#d97a1f', 'Planned': '#8b949e', 'Draft': '#8b949e'}
    status_order = ['Live', 'Active', 'Mission review', 'Exploring', 'Planned', 'Draft']
    status_counts = {}
    for p in plans:
        status_counts[p["status"]] = status_counts.get(p["status"], 0) + 1
    plan_tiles = "".join(
        f'<div class="ptile" data-tile="{esc(s)}" style="--tint:{status_tints.get(s, "#8b949e")};flex:1 1 140px">'
        f'<div class="ptile-label">{esc(s.upper())}</div>'
        f'<div class="ptile-num">{status_counts[s]}</div>'
        f'<div class="ptile-sub">business plans</div></div>'
        for s in status_order if s in status_counts
    )
    vpl = ('<div id="view-plans" class="view"><section class="projects-view" style="margin-top:24px">'
           f'<div id="plans-tiles" style="display:flex;gap:14px;margin:2px auto 20px;max-width:860px;flex-wrap:wrap">{plan_tiles}</div>'
           '<h2>Business Plans</h2>'
           '<p class="sub">BRDs and business plans \u2014 real-world ventures, separate from the buddy-app '
           'software projects. Plans link to the buddies that build them.</p>'
           f'<div class="plan-grid">{plan_rows}</div></section></div>')

    js = """const BUDDIES = BUDDIES_JSON;
const ROOT_ORDER = ORDER_JSON;
const byId = Object.fromEntries(BUDDIES.map(b => [b.id, b]));
(function applyIconOverrides(){ try { const o = JSON.parse(localStorage.getItem('buddyState') || '{}').iconOverrides || {}; Object.entries(o).forEach(([id, ic]) => { if (byId[id]) byId[id].icon = ic; }); } catch(e){} })();
const PLANS = PLANS_JSON;
const planById = Object.fromEntries(PLANS.map(p => [p.id, p]));
/* Durable broadcast memos — shown on every buddy detail. Source: docs/standing-orders.md */
const STANDING_ORDERS = [
  {id:'dark-mode-2026-10-11', date:'2026-10-11', critical:true,
   text:'CRITICAL — Dark mode for every buddy website. Prefer prefers-color-scheme (or equivalent). Dave is outdoors and needs readable UIs now: update light-only homepages immediately.',
   href:'docs/standing-orders.md'}
];
function standingOrdersHtml(){
  if (!STANDING_ORDERS || !STANDING_ORDERS.length) return '';
  return STANDING_ORDERS.map(o => {
    const link = o.href ? ' <a href="'+o.href+'" target="_blank" rel="noopener">Standing orders</a> · <a href="AGENTS.md" target="_blank" rel="noopener">AGENTS.md</a>' : '';
    return '<div class="standing-order'+(o.critical?' critical':'')+'" data-order="'+o.id+'"><b>'+(o.critical?'Critical memo':'Memo')+'</b> — '+escHtml(o.text)+link+'<span class="so-date">'+escHtml(o.date||'')+'</span></div>';
  }).join('');
}
const kidsOf = {};
function effParent(b){ if (S.parents && b.id in S.parents) return S.parents[b.id]; return b.parent; }
function buildKids(){
  for (const k in kidsOf) delete kidsOf[k];
  BUDDIES.forEach(b => { const p = effParent(b) || '__root'; (kidsOf[p] = kidsOf[p] || []).push(b); });
}
const LS_KEY = 'buddyTree.v3';
const SB_DEFAULT_W = 308;
let S = {seen:{}, notes:{}, names:{}, parents:{}, zoom:100, sel:'view:tree', view:'tree'};
try { Object.assign(S, JSON.parse(localStorage.getItem(LS_KEY) || '{}')); } catch(e) {}
S.parents = S.parents || {};
S.zoom = S.zoom || 100;
initTheme();
buildKids();
function save(){ localStorage.setItem(LS_KEY, JSON.stringify(S)); }
function applyTheme(){
  const t = S.theme || 'system';
  let light = false;
  if (t === 'light') light = true;
  else if (t === 'dark') light = false;
  else if (window.matchMedia) light = window.matchMedia('(prefers-color-scheme: light)').matches;
  document.documentElement.classList.toggle('light', light);
  document.querySelectorAll('[data-theme-pick]').forEach(b => b.classList.toggle('sel', b.dataset.themePick === t));
}
function setTheme(t){
  if (['light', 'dark', 'system'].indexOf(t) < 0) return;
  S.theme = t; save(); applyTheme();
}
function wireThemePicks(root){
  (root || document).querySelectorAll('[data-theme-pick]').forEach(b => {
    if (!b.dataset.tinit) { b.dataset.tinit = '1'; b.addEventListener('click', () => setTheme(b.dataset.themePick)); }
  });
  applyTheme();
}
function initTheme(){
  wireThemePicks(document);
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => {
      if ((S.theme || 'system') === 'system') applyTheme();
    });
  }
}
function dispName(b){
  // If the user overrode the name, use it exactly as provided (even if it contains "Buddy").
  // The hideBuddyWord setting only applies to original registry names.
  if (S.names[b.id]) return S.names[b.id];
  let n = b.name;
  if (S.hideBuddyWord) n = n.replace(/\s+Buddy$/i, '');
  return n;
}
function getHomepage(b){ return (S.homepages && S.homepages[b.id]) || b.homepage || ''; }
function homepageUrl(b){
  const hp = getHomepage(b);
  if (!hp) return '';
  // If it's already a full URL, use as-is. Otherwise resolve against the site origin.
  if (/^https?:\/\//i.test(hp)) return hp;
  const base = window.location.origin + window.location.pathname.replace(/\/[^/]*$/, '/');
  return base + hp.replace(/^\//, '');
}
function unseenItems(b){ return (b.attention || []).filter(a => !S.seen[a.id]); }
function descUnseen(id){
  let n = 0;
  (function walk(x){ const b = byId[x]; if(!b) return; n += unseenItems(b).length;
    (kidsOf[x] || []).forEach(c => walk(c.id)); })(id);
  return n;
}
function totalUnseen(){ return ROOT_ORDER.reduce((n,id) => n + (byId[id] && byId[id].parent === null ? descUnseen(id) : 0), 0); }
function crumb(id){
  const chain = []; let b = byId[id];
  while (b) { chain.unshift(b); const p = effParent(b); b = p ? byId[p] : null; }
  return chain.map((c,i) => i < chain.length-1
    ? '<a href="#" data-goto="'+c.id+'" style="color:var(--muted)">'+escHtml(dispName(c))+'</a>'
    : '<b class="reposlug" title="'+escHtml(c.repo ? 'GitHub repo: davedellaquila/'+c.repo : 'No repo linked')+'">'+escHtml(c.repo || 'no repo linked')+'</b>').join(' <span style="color:var(--faint)">/</span> ');
}
function escHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
// Converts URLs in already-escaped HTML text into clickable links
function linkify(escaped){
  return escaped.replace(/(https?:\/\/[^\s<>"']+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
}
const VIEW_DEFS = [
  ['tree','Tree','▦'],
  ['projects','Projects','☰'],
  ['plans','Business Plans','💼'],
  ['manifest','Manifest','✓'],
  ['project','Project Homepage','🏠'],
  ['changelog','Changelog','🕘'],
];
const VIEW_TIPS = {
  tree: 'Tree view — visual hierarchy of all buddies. Click a node to open its details. Drag the background to pan, scroll to zoom. Drag a node onto another node to reparent it.',
  projects: 'Projects list — every buddy in hierarchy order with status. Click a tile to filter by attention status. Click the chevron to expand/collapse sections.',
  plans: 'Business Plans — real-world ventures as cards. Click a status tile to filter. Each card links to its mission statement and related buddies.',
  manifest: 'New-Project Manifest — the checklist every new buddy gets. Click AUTOMATIC or PLANNED tiles to filter the steps.',
  project: 'Project Homepage — loads the selected buddy homepage full-bleed in the main view. Clicking a buddy with a homepage swaps it; clicking one without keeps the current page.',
  changelog: 'Changelog — history of everything that changed. Click a tile to filter by change type. Click a row to open the changed buddy.',
};
function getViewOrder(){
  const ids = VIEW_DEFS.map(v => v[0]);
  if (!Array.isArray(S.viewOrder)) S.viewOrder = ids.slice();
  const clean = S.viewOrder.filter(id => ids.indexOf(id) >= 0);
  ids.forEach(id => { if (clean.indexOf(id) < 0) clean.push(id); });
  S.viewOrder = clean;
  return clean;
}
// The views-list selection changes ONLY on view interaction (view-menu clicks,
// number-key shortcuts, initial load). Buddy/plan selection never touches it.
if (!S.view || VIEW_DEFS.every(v => v[0] !== S.view)) S.view = (typeof S.sel === 'string' && S.sel.indexOf('view:') === 0) ? S.sel.slice(5) : 'tree';
function projectId(){
  const id = S.projectId;
  return (id && byId[id]) ? id : 'project-buddy';
}
function selectProject(id){
  if (!byId[id]) return;
  S.projectId = id; save();
  show('view:project');
}
function selectBuddy(id){
  if (!byId[id]) return;
  const b = byId[id];
  // Select the buddy and update the main view, WITHOUT opening the right-side panel.
  // But if the panel is already open, refresh it to show the newly selected buddy.
  const vb = document.getElementById('view-buddy');
  const panelOpen = vb && vb.classList.contains('active');
  if (S.view === 'project') {
    S.projectId = id; save();
    renderProjectView();
    renderNav();
  } else {
    const inView = (S.sel || '').startsWith('view:');
    S.projectId = id; save();
    if (inView) {
      // Update selection highlight without opening the panel
      renderNav();
    } else {
      show('buddy:' + id);
    }
  }
  // If the detail panel is open, update it to the new buddy
  if (panelOpen) renderBuddy(id);
}
function openBuddy(id){
  if (!byId[id]) return;
  selectBuddy(id);
  // Now open the right-side detail panel
  const inView = (S.sel || '').startsWith('view:');
  const b = byId[id];
  if (S.view === 'project' || inView) {
    const vb = document.getElementById('view-buddy');
    vb.classList.add('active');
    vb.classList.toggle('panel', window.innerWidth >= 640);
    vb.classList.toggle('sheet', window.innerWidth < 640);
    renderBuddy(id);
    renderNav();
  }
}
function shortVal(v){
  if (v == null || v === '') return '(empty)';
  const s = String(v);
  return escHtml(s.length > 90 ? s.slice(0, 90) + '…' : s);
}
const CHANGE_ICONS = {
  notes: '✏️',
  photos: '🖼️',
  move: '↔️',
  rename: '🏷️',
  brand: '🏷️',
};
function changeDiff(c){
  let b = c.before, a = c.after;
  if (c.type === 'move') {
    b = b ? (((byId[b] || {}).name) || b) : '(top level)';
    a = a ? (((byId[a] || {}).name) || a) : '(top level)';
  }
  if (b == null && a == null) return '';
  return shortVal(b) + ' → ' + shortVal(a);
}
function changeOldNew(c){
  const d = changeDiff(c);
  return d ? ' <span class="jchg">' + d + '</span>' : '';
}
function dayLabel(d){
  const day = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const diff = Math.round((today - day) / 86400000);
  if (diff === 0) return 'Today';
  if (diff === 1) return 'Yesterday';
  return d.toLocaleDateString([], {month: 'long', day: 'numeric'});
}
function renderChangelog(){
  const el = document.getElementById('view-changelog');
  if (!el) return;
  // Change-type summary tiles
  const TYPE_META = {notes:['NOTE EDITS','#1f6feb'], photos:['PHOTOS','#8250df'], move:['MOVES','#d97a1f'], rename:['RENAMES','#2f9e44'], brand:['BRAND','#cf222e']};
  const typeCounts = {};
  (S.journal || []).forEach(c => { const t = (c && c.type) || 'other'; typeCounts[t] = (typeCounts[t] || 0) + 1; });
  const typeOrder = Object.keys(TYPE_META).filter(t => typeCounts[t]).concat(Object.keys(typeCounts).filter(t => !TYPE_META[t]));
  const typeTiles = typeOrder.map(t => {
    const m = TYPE_META[t] || [t.toUpperCase(), '#57606a'];
    return tileHtml(m[0], typeCounts[t], m[1], 'changes logged', t, clFilter === t);
  }).join('');
  let h = '<section class="changelog" style="margin:24px auto 0;max-width:860px">'
    + (typeTiles ? '<div id="changelog-tiles" style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">' + typeTiles + '</div>' : '')
    + '<h2>Changelog</h2>'
    + '<p class="sub">Every change made in this dashboard, newest first.</p>';
  const js = (S.journal || []).slice().reverse().filter(c => !clFilter || (c && c.type) === clFilter);
  if (!js.length) { el.innerHTML = h + '<p class="fineprint">' + (clFilter ? 'No changes of this type yet.' : 'No changes yet.') + '</p></section>'; return; }
  const groups = [];
  js.forEach(c => {
    const d = new Date(c.t);
    const key = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
    let g = null;
    for (let i = 0; i < groups.length; i++) { if (groups[i].key === key) { g = groups[i]; break; } }
    if (!g) { g = {key: key, date: d, items: []}; groups.push(g); }
    g.items.push(c);
  });
  h += groups.map(g => {
    const rows = g.items.map(c => {
      const d = new Date(c.t);
      const ic = CHANGE_ICONS[c.type] || '•';
      const diff = changeDiff(c);
      return '<div class="cl-row"' + (c.buddy ? ' data-buddy="' + escHtml(c.buddy) + '"' : '') + '>'
        + '<span class="cl-ic" aria-hidden="true">' + ic + '</span>'
        + '<div class="cl-body">'
        + '<div class="cl-title">' + escHtml(c.desc) + '</div>'
        + (diff ? '<div class="cl-desc">' + diff + '</div>' : '')
        + '<div class="cl-time" title="' + escHtml(d.toLocaleString()) + '">'
        + escHtml(d.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'})) + '</div>'
        + '</div>'
        + '</div>';
    }).join('');
    return '<h3 class="cl-day">' + escHtml(dayLabel(g.date)) + '</h3>'
      + '<div class="cl-group">' + rows + '</div>';
  }).join('');
  el.innerHTML = h + '</section>';
}
function renderNav(){
  const views = getViewOrder().map(id => VIEW_DEFS.find(v => v[0] === id)).filter(Boolean);
  document.getElementById('view-nav').innerHTML = views.map(([v,l,ic]) =>
    '<button class="navbtn'+(S.view===v?' sel':'')+'" data-view="'+v+'" title="'+(VIEW_TIPS[v]||l)+'"><span class="nic">'+ic+'</span>'+l+'</button>').join('');
  const q = (document.getElementById('buddy-search').value || '').toLowerCase().trim();
  const words = q.split(/\s+/).filter(Boolean);
  let h = '';
  function matches(b){
    if (!words.length) return true;
    const hay = (dispName(b) + ' ' + (b.name || '') + ' ' + (b.tagline || '')).toLowerCase();
    return words.every(w => hay.includes(w));
  }
  function row(id, depth){
    const b = byId[id]; if(!b) return;
    if (words.length && !matches(b)) { (kidsOf[id] || []).forEach(c => row(c.id, depth+1)); return; }
    const un = descUnseen(id);
    const kind = b.kind === 'root' ? 'root' : (b.parent === 'project-buddy' ? 'direct' : b.kind);
    h += '<button class="brow'+((S.projectId===id || S.sel==='buddy:'+id)?' sel':'')+(un?' has-unseen':'')+'" data-buddy="'+id+'"'
      + ' draggable="'+(id==='project-buddy'?'false':'true')+'"'
      + ' style="padding-left:'+(8+depth*16)+'px" title="'+escHtml(b.tagline||'')+'">'
      + '<span class="bdot"></span><span class="bicon">'+escHtml(b.icon||'')+'</span><span class="bname">'+escHtml(dispName(b))+'</span>'
      + '<span class="bkind">'+kind+'</span>'
      + '<span class="binfo" data-buddy-info="'+id+'" title="Open '+escHtml(dispName(b))+' details" style="margin-left:auto;padding:2px 6px;opacity:0;transition:opacity 0.15s;cursor:pointer" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0">\u24d8</span></button>';
    (kidsOf[id] || []).forEach(c => row(c.id, depth+1));
  }
  ROOT_ORDER.filter(id => { const b = byId[id]; const p = b ? effParent(b) : null; return p === null; })
    .forEach(id => row(id, 0));
  document.getElementById('buddy-nav').innerHTML = h;
  if (Object.keys(S.parents).length) {
    document.getElementById('buddy-nav').insertAdjacentHTML('beforeend',
      '<div style="padding:10px 10px 0"><button class="linkbtn" id="reset-parents">Reset moved buddies</button></div>'
      + '<div class="fineprint" style="padding:2px 10px 0">Hierarchy moves save on this device.</div>');
  }
  const t = totalUnseen();
  const pill = document.getElementById('attn-pill');
  pill.textContent = t; pill.classList.toggle('zero', t === 0);
  document.getElementById('plan-nav').innerHTML = PLANS.map(p =>
    '<button class="brow'+(S.sel==='plan:'+p.id?' sel':'')+'" data-plan="'+p.id+'" style="padding-left:8px">'
    + '<span class="bicon">'+escHtml(p.icon||'')+'</span><span class="bname">'+escHtml(p.name)+'</span></button>').join('');
}
function artRow(icon, label, sub, url){
  return '<a class="art-row" href="'+url+'" target="_blank" rel="noopener">'
    + '<span class="art-ic">'+icon+'</span>'
    + '<span><span class="art-label">'+escHtml(label)+'</span><div class="art-sub">'+escHtml(sub)+'</div></span>'
    + '<span class="art-go">→</span></a>';
}
function closeDetail(){
  const vb = document.getElementById('view-buddy');
  if (vb) vb.classList.remove('active', 'panel', 'sheet');
  // Restore the middle canvas when nothing else is active (e.g. landed on #/buddy:…)
  const anyMain = document.querySelector('#main .view.active:not(#view-buddy)');
  if (!anyMain) {
    const v = S.view || 'tree';
    const ev = document.getElementById('view-' + v) || document.getElementById('view-tree');
    if (ev) {
      ev.classList.add('active');
      if (!S.sel || S.sel.startsWith('buddy:') || S.sel.startsWith('plan:')) {
        S.sel = 'view:' + (ev.id && ev.id.indexOf('view-') === 0 ? ev.id.slice(5) : v);
        save();
        try { if (typeof location !== 'undefined') location.hash = hashFor(S.sel); } catch (e) {}
      }
    }
  }
  try {
    const main = document.getElementById('main');
    if (main) {
      if (!main.hasAttribute('tabindex')) main.setAttribute('tabindex', '-1');
      main.focus({ preventScroll: true });
    }
  } catch (e) {}
}
const FIELD_DEFS = [
  {id:'ingest', label:'Ingest'},
  {id:'attention', label:'Needs your attention'},
  {id:'mission', label:'About'},
  {id:'homepage', label:'Homepage URL'},
  {id:'photos', label:'Photos'},
  {id:'tree', label:'The Buddy Tree'},
  {id:'artifacts', label:'Artifacts'},
  {id:'plans', label:'Business plans'},
  {id:'notes', label:'Notes'},
  {id:'shared', label:'Shared notes'},
];
function getFieldOrder(){
  if (!S.fieldOrder || !Array.isArray(S.fieldOrder)) S.fieldOrder = FIELD_DEFS.map(f => f.id);
  // Add any new fields that weren't in the saved order
  const ids = FIELD_DEFS.map(f => f.id);
  ids.forEach(id => { if (!S.fieldOrder.includes(id)) S.fieldOrder.push(id); });
  // Remove any stale IDs no longer in FIELD_DEFS
  S.fieldOrder = S.fieldOrder.filter(id => ids.includes(id));
  return S.fieldOrder;
}
function applySectionCollapse(bid){
  const home = document.getElementById('buddy-home');
  if (!home) return;
  if (!S.secCollapsed || typeof S.secCollapsed !== 'object') S.secCollapsed = {};
  if (!S.secCollapsed[bid] || typeof S.secCollapsed[bid] !== 'object') S.secCollapsed[bid] = {};
  home.querySelectorAll('.bp-sec[data-field] > h3').forEach(h3 => {
    if (h3.querySelector('.secarrow')) return;
    const sec = h3.parentElement;
    const fid = sec.dataset.field;
    const arrow = document.createElement('span');
    arrow.className = 'secarrow';
    arrow.textContent = '\u203a';
    h3.insertBefore(arrow, h3.firstChild);
    if (S.secCollapsed[bid][fid]) sec.classList.add('collapsed');
    h3.addEventListener('click', e => {
      if (e.target.closest('.info-tip')) return;
      sec.classList.toggle('collapsed');
      S.secCollapsed[bid][fid] = sec.classList.contains('collapsed');
      save();
    });
  });
}
function applyFieldOrder(){
  const home = document.getElementById('buddy-home');
  if (!home) return;
  // Keep sections inside .bp-wrap (before footer/build) so .bp-sticky-head can stick
  const wrap = home.querySelector('.bp-wrap') || home;
  const build = wrap.querySelector('.bp-footer') || wrap.querySelector('.bp-build');
  const order = getFieldOrder();
  const sections = {};
  home.querySelectorAll('.bp-sec[data-field]').forEach(el => { sections[el.dataset.field] = el; });
  // Remove all and re-append in order
  Object.values(sections).forEach(el => el.remove());
  const place = el => { if (build) wrap.insertBefore(el, build); else wrap.appendChild(el); };
  order.forEach(fid => {
    const el = sections[fid];
    if (!el) return;
    if (S.fieldHidden && S.fieldHidden[fid]) el.style.display = 'none';
    else el.style.display = '';
    place(el);
  });
  // Append any sections not in order (safety)
  Object.entries(sections).forEach(([fid, el]) => {
    if (!order.includes(fid) && !el.parentNode) place(el);
  });
}
function isFieldVisible(fid){
  if (!S.fieldHidden) S.fieldHidden = {};
  return !S.fieldHidden[fid];
}
const SETTING_DEFS = [
  {id:'hideBuddyWord', label:'Hide the word “Buddy” in names', type:'bool', def:false},
  {id:'autoOpenPanel', label:'Always open detail panel on buddy click', type:'bool', def:false, tip:'When off (default), the panel auto-opens in every view EXCEPT Project Homepage — there, use the \u24d8 icon. When on, the panel opens on every click in every view.'},
];
function getSetting(id){
  const def = SETTING_DEFS.find(s => s.id === id);
  if (S[id] === undefined) return def ? !!def.def : undefined;
  return S[id];
}
function snapshotSettable(){
  return {
    hideBuddyWord: !!S.hideBuddyWord,
    autoOpenPanel: !!S.autoOpenPanel,
    fieldOrder: getFieldOrder().slice(),
    fieldHidden: Object.assign({}, S.fieldHidden || {}),
    viewOrder: getViewOrder().slice(),
    sbWidth: S.sbWidth || SB_DEFAULT_W,
    panelWidth: S.panelWidth || SB_DEFAULT_W,
  };
}
function resetToFactory(){
  const f = S.factory || {};
  S.hideBuddyWord = !!f.hideBuddyWord;
  S.autoOpenPanel = !!f.autoOpenPanel;
  if (Array.isArray(f.fieldOrder) && f.fieldOrder.length) S.fieldOrder = f.fieldOrder.slice();
  if (f.fieldHidden && typeof f.fieldHidden === 'object') S.fieldHidden = Object.assign({}, f.fieldHidden);
  if (Array.isArray(f.viewOrder) && f.viewOrder.length) S.viewOrder = f.viewOrder.slice();
  S.sbWidth = f.sbWidth || SB_DEFAULT_W; S.panelWidth = f.panelWidth || SB_DEFAULT_W;
  save();
}
function updateFactory(){
  S.factory = snapshotSettable();
  save();
}
function renderSettingChecks(){
  const sdiv = document.getElementById('fset-settings');
  if (!sdiv) return;
  sdiv.innerHTML = '<div style="margin-bottom:12px"><div style="font-size:13px;margin-bottom:6px">Theme</div>'
    + '<div class="theme-pick" role="group" aria-label="Theme" style="margin:0"><button data-theme-pick="light" title="Light theme">Light</button><button data-theme-pick="dark" title="Dark theme">Dark</button><button data-theme-pick="system" title="Follow system theme">System</button></div></div>'
    + SETTING_DEFS.map(s => {
    const val = getSetting(s.id);
    if (s.type === 'bool') return '<label class="fset-check"><input type="checkbox" data-setting="' + s.id + '"' + (val ? ' checked' : '') + '> <span>' + s.label + '</span></label>';
    return '';
  }).join('');
  wireThemePicks(sdiv);
  sdiv.querySelectorAll('[data-setting]').forEach(cb => {
    cb.addEventListener('change', () => {
      S[cb.dataset.setting] = cb.checked; save();
      show(S.sel, false);
    });
  });
}
function initFsetChrome(m){
  function applyGeom(){
    const g = S.fsetGeom || {};
    if (g.w) m.style.width = g.w + 'px';
    if (g.h) { m.style.height = g.h + 'px'; m.style.maxHeight = 'none'; }
    if (g.x !== undefined && g.y !== undefined) {
      m.style.left = g.x + 'px'; m.style.top = g.y + 'px'; m.style.transform = 'none';
    }
  }
  applyGeom();
  m._applyGeom = applyGeom;
  const head = m.querySelector('#fset-drag'), rz = m.querySelector('#fset-resize');
  head.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    e.preventDefault();
    const r = m.getBoundingClientRect();
    m.style.left = r.left + 'px'; m.style.top = r.top + 'px'; m.style.transform = 'none';
    const ox = e.clientX - r.left, oy = e.clientY - r.top;
    const mv = ev => {
      m.style.left = Math.max(0, Math.min(window.innerWidth - 120, ev.clientX - ox)) + 'px';
      m.style.top = Math.max(0, Math.min(window.innerHeight - 80, ev.clientY - oy)) + 'px';
    };
    const up = () => {
      window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up);
      const rr = m.getBoundingClientRect();
      S.fsetGeom = Object.assign(S.fsetGeom || {}, {x: Math.round(rr.left), y: Math.round(rr.top)});
      save();
    };
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  });
  rz.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    e.preventDefault(); e.stopPropagation();
    const r = m.getBoundingClientRect(), sx = e.clientX, sy = e.clientY;
    const mv = ev => {
      m.style.width = Math.max(300, Math.min(window.innerWidth - 40, r.width + ev.clientX - sx)) + 'px';
      m.style.height = Math.max(220, Math.min(window.innerHeight - 40, r.height + ev.clientY - sy)) + 'px';
      m.style.maxHeight = 'none';
    };
    const up = () => {
      window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up);
      const rr = m.getBoundingClientRect();
      S.fsetGeom = Object.assign(S.fsetGeom || {}, {w: Math.round(rr.width), h: Math.round(rr.height)});
      save();
    };
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  });
}
function openFieldSettings(){
  let m = document.getElementById('field-settings');
  if (!m) {
    m = document.createElement('div'); m.id = 'field-settings';
    m.innerHTML = '<button class="fset-close-x" id="fset-x" title="Close">\u2715</button>'
      + '<div class="fset-head" id="fset-drag"><h3>Settings</h3></div>'
      + '<div class="fset-body">'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Preferences</h3><div id="fset-settings"></div></section>'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Buddy fields</h3><p class="fineprint">Drag to reorder. Uncheck to hide.</p><div id="fset-list"></div></section>'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Main views</h3><p class="fineprint">Drag to reorder. Number keys 1–9 follow this order.</p><div id="vset-list"></div></section>'
      + '</div>'
      + '<div class="fset-footer">'
      + '<div style="display:flex;gap:8px"><button class="linkbtn" id="fset-reset" title="Restore all settings to factory defaults">Reset to Factory Defaults</button>'
      + '<button class="linkbtn" id="fset-update" title="Save current settings as the new factory defaults">Update Factory Defaults</button></div>'
      + '<button class="linkbtn" id="fset-close">Done</button></div>'
      + '<div class="fset-resize" id="fset-resize" title="Drag to resize"></div>';
    document.body.appendChild(m);
    initFsetChrome(m);
    m.querySelector('#fset-close').addEventListener('click', () => m.classList.remove('show'));
    m.querySelector('#fset-x').addEventListener('click', () => m.classList.remove('show'));
    renderSettingChecks();
    m.querySelector('#fset-reset').addEventListener('click', () => {
      if (!confirm('Reset all settings to factory defaults?')) return;
      resetToFactory(); renderSettingChecks(); openFieldSettings();
      applySbWidth(); applyPanelWidth();
      show(S.sel, false);
    });
    m.querySelector('#fset-update').addEventListener('click', () => {
      if (!confirm('Save current settings as the new factory defaults?')) return;
      updateFactory(); toast('Factory defaults updated.');
    });
  }
  const list = document.getElementById('fset-list');
  list.innerHTML = getFieldOrder().map(fid => {
    const def = FIELD_DEFS.find(f => f.id === fid);
    if (!def) return '';
    const vis = isFieldVisible(fid);
    return '<div class="fset-row" draggable="true" data-fid="' + fid + '">'
      + '<span class="fh">\u2630</span><span class="fl">' + def.label + '</span>'
      + '<input type="checkbox" ' + (vis ? 'checked' : '') + ' data-vis="' + fid + '" title="Show/hide"></div>';
  }).join('');
  function clearFsetDnD(listEl){
    if (listEl) {
      listEl.querySelectorAll('.fset-row').forEach(r => r.classList.remove('dragging'));
      listEl.querySelectorAll('.fset-insert').forEach(n => n.remove());
    }
    const g = document.getElementById('fset-ghost');
    if (g) g.remove();
  }
  function moveFsetGhost(row, clientX, clientY){
    let g = document.getElementById('fset-ghost');
    if (!g) {
      g = row.cloneNode(true);
      g.id = 'fset-ghost';
      g.classList.remove('dragging');
      g.querySelectorAll('input').forEach(i => { i.disabled = true; });
      g.style.width = row.getBoundingClientRect().width + 'px';
      document.body.appendChild(g);
    }
    g.style.left = Math.max(8, clientX - 28) + 'px';
    g.style.top = Math.max(8, clientY - 22) + 'px';
  }
  function placeFsetInsert(listEl, clientY, dragEl){
    listEl.querySelectorAll('.fset-insert').forEach(n => n.remove());
    const rows = [...listEl.querySelectorAll('.fset-row')].filter(r => r !== dragEl);
    let before = null;
    for (const r of rows) {
      const rect = r.getBoundingClientRect();
      if (clientY < rect.top + rect.height / 2) { before = r; break; }
    }
    const marker = document.createElement('div');
    marker.className = 'fset-insert';
    if (before) listEl.insertBefore(marker, before);
    else listEl.appendChild(marker);
    return before;
  }
  function insertBeforeFromMarker(listEl, dragEl){
    const insert = listEl.querySelector('.fset-insert');
    let before = insert ? insert.nextElementSibling : null;
    while (before && (before === dragEl || !before.classList || !before.classList.contains('fset-row'))) {
      before = before.nextElementSibling;
    }
    return before;
  }
  function reorderBefore(order, fromId, beforeId){
    const from = order.indexOf(fromId);
    if (from < 0) return order;
    const next = order.slice();
    const [moved] = next.splice(from, 1);
    if (!beforeId) next.push(moved);
    else {
      const to = next.indexOf(beforeId);
      if (to < 0) next.push(moved);
      else next.splice(to, 0, moved);
    }
    return next;
  }
  // HTML5 + touch reorder with ghost preview and dashed insert line
  function bindFsetListDnD(listEl, getId, applyOrder){
    let dragEl = null;
    const finish = () => {
      if (!dragEl) return;
      const before = insertBeforeFromMarker(listEl, dragEl);
      const fromId = getId(dragEl);
      const beforeId = before ? getId(before) : null;
      clearFsetDnD(listEl);
      if (fromId && beforeId !== fromId) applyOrder(fromId, beforeId);
      dragEl = null;
    };
    listEl.querySelectorAll('.fset-row').forEach(row => {
      row.addEventListener('dragstart', e => {
        dragEl = row;
        row.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        try { e.dataTransfer.setData('text/plain', getId(row)); } catch (err) {}
        const ghost = row.cloneNode(true);
        ghost.style.cssText = 'position:absolute;top:-9999px;left:0;width:' + row.offsetWidth + 'px;opacity:.95;box-shadow:0 12px 32px rgba(0,0,0,.55);border-color:var(--accent);background:var(--panel)';
        document.body.appendChild(ghost);
        try { e.dataTransfer.setDragImage(ghost, 28, 22); } catch (err) {}
        setTimeout(() => ghost.remove(), 0);
      });
      row.addEventListener('dragend', () => { clearFsetDnD(listEl); dragEl = null; });
      row.addEventListener('dragover', e => {
        e.preventDefault(); e.dataTransfer.dropEffect = 'move';
        if (dragEl) placeFsetInsert(listEl, e.clientY, dragEl);
      });
      row.addEventListener('drop', e => { e.preventDefault(); finish(); });
      const handle = row.querySelector('.fh');
      if (!handle) return;
      handle.style.touchAction = 'none';
      handle.addEventListener('touchstart', e => {
        const t = e.touches[0];
        dragEl = row;
        row.classList.add('dragging');
        moveFsetGhost(row, t.clientX, t.clientY);
        placeFsetInsert(listEl, t.clientY, dragEl);
        e.preventDefault();
      }, {passive: false});
      handle.addEventListener('touchmove', e => {
        if (!dragEl) return;
        e.preventDefault();
        const t = e.touches[0];
        moveFsetGhost(dragEl, t.clientX, t.clientY);
        placeFsetInsert(listEl, t.clientY, dragEl);
      }, {passive: false});
      handle.addEventListener('touchend', () => finish());
      handle.addEventListener('touchcancel', () => { clearFsetDnD(listEl); dragEl = null; });
    });
    listEl.addEventListener('dragover', e => {
      e.preventDefault();
      if (dragEl) placeFsetInsert(listEl, e.clientY, dragEl);
    });
    listEl.addEventListener('drop', e => { e.preventDefault(); finish(); });
  }
  bindFsetListDnD(list, r => r.dataset.fid, (fromId, beforeId) => {
    S.fieldOrder = reorderBefore(getFieldOrder(), fromId, beforeId);
    save();
    openFieldSettings();
    const vb2 = document.getElementById('view-buddy');
    if (vb2 && vb2.classList.contains('active') && S.projectId && byId[S.projectId]) {
      renderBuddy(S.projectId);
    }
  });
  list.querySelectorAll('[data-vis]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (!S.fieldHidden) S.fieldHidden = {};
      S.fieldHidden[cb.dataset.vis] = !cb.checked;
      save();
      const vb = document.getElementById('view-buddy');
      if (vb && vb.classList.contains('active') && S.projectId && byId[S.projectId]) {
        renderBuddy(S.projectId);
      }
    });
  });
  const vlist = document.getElementById('vset-list');
  if (vlist) {
    vlist.innerHTML = getViewOrder().map(vid => {
      const def = VIEW_DEFS.find(v => v[0] === vid);
      if (!def) return '';
      return '<div class="fset-row" draggable="true" data-vid="' + vid + '">'
        + '<span class="fh">☰</span><span class="fl">' + def[1] + '</span></div>';
    }).join('');
    bindFsetListDnD(vlist, r => r.dataset.vid, (fromId, beforeId) => {
      S.viewOrder = reorderBefore(getViewOrder(), fromId, beforeId);
      save();
      renderNav();
      openFieldSettings();
    });
  }
  m.classList.add('show');
  if (m._applyGeom) m._applyGeom();
}
function applyPanelWidth(){
  const vb = document.getElementById('view-buddy');
  if (vb && S.panelWidth) vb.style.width = Math.min(S.panelWidth, 560) + 'px';
}
function applySbWidth(){
  const sb = document.getElementById('sidebar');
  if (sb) { const w = sbClampW(S.sbWidth || SB_DEFAULT_W); sb.style.width = w + 'px'; sb.style.flex = '0 0 ' + w + 'px'; document.documentElement.style.setProperty('--sbw', w + 'px'); }
}
/* Sidebar width clamp: desktop max 560, but never wider than 92% of the viewport (drawer on phones) */
function sbClampW(w){ return Math.min(Math.min(560, Math.floor(window.innerWidth * 0.92)), Math.max(200, w)); }
function initPanelResize(){
  const vb = document.getElementById('view-buddy');
  if (!vb || vb.dataset.rsz) return;
  vb.dataset.rsz = '1';
  const h = document.getElementById('bp-resize');
  if (!h) return;
  let sx = null, sw = 0;
  h.addEventListener('pointerdown', e => {
    sx = e.clientX; sw = vb.getBoundingClientRect().width;
    h.setPointerCapture(e.pointerId); e.preventDefault();
  });
  h.addEventListener('pointermove', e => {
    if (sx === null) return;
    const w = Math.min(560, Math.max(320, sw + (sx - e.clientX)));
    vb.style.width = w + 'px';
  });
  h.addEventListener('pointerup', e => {
    if (sx === null) return;
    S.panelWidth = Math.round(vb.getBoundingClientRect().width);
    save(); sx = null;
  });
}
function tileHtml(label, num, tint, sub, fkey, sel, tip){
  return '<div class="ptile' + (sel ? ' sel' : '') + '"' + (fkey ? ' data-tile="' + fkey + '"' : '') + (tip ? ' title="' + escHtml(tip) + '"' : '') + ' style="--tint:' + tint + ';flex:1">'
    + '<div class="ptile-label">' + escHtml(label) + '</div>'
    + '<div class="ptile-num">' + escHtml(String(num)) + '</div>'
    + '<div class="ptile-sub">' + escHtml(sub) + '</div></div>';
}
let projFilter = null, clFilter = null, planFilter = null, manifestFilter = null, statusFilter = null;
function applyManifestFilter(){
  document.querySelectorAll('#view-manifest .proj-row').forEach(r => {
    const isAuto = !!r.querySelector('.st-auto');
    const show = !manifestFilter || (manifestFilter === 'auto' ? isAuto : !isAuto);
    r.style.display = show ? '' : 'none';
  });
  document.querySelectorAll('#manifest-tiles .ptile').forEach(t => {
    t.classList.toggle('sel', t.dataset.tile === manifestFilter);
  });
}
function applyPlanFilter(){
  document.querySelectorAll('#view-plans .plan-card[data-status]').forEach(r => {
    r.style.display = (!planFilter || r.dataset.status === planFilter) ? '' : 'none';
  });
  document.querySelectorAll('#plans-tiles .ptile').forEach(t => {
    t.classList.toggle('sel', t.dataset.tile === planFilter);
  });
}
function buddyHomepageHtml(b){
  const kids = (b.children || []).map(cid => byId[cid]).filter(Boolean);
  const arts = b.artifacts || [];
  const plans = (typeof PLANS !== 'undefined' && PLANS[b.id]) || [];
  const attnItems = (b.attention || []).filter(a => !S.seen[b.id + ':' + (a.id || a.text)]);
  let h = '<div style="max-width:800px;margin:0 auto;padding:40px 24px;font-family:inherit">';
  // Header
  h += '<div style="text-align:center;margin-bottom:36px">';
  h += '<div style="font-size:64px;margin-bottom:12px">' + (b.icon || '🤖') + '</div>';
  h += '<h1 style="font-size:32px;margin:0 0 8px">' + escHtml(dispName(b)) + '</h1>';
  if (b.tagline) h += '<p style="color:var(--muted);font-size:16px;margin:0">' + escHtml(b.tagline) + '</p>';
  h += '</div>';
  // Mission
  if (b.mission) {
    h += '<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px">';
    h += '<h3 style="margin:0 0 12px;font-size:14px;text-transform:uppercase;letter-spacing:0.5px;color:var(--muted)">About</h3>';
    h += '<p style="margin:0;line-height:1.6">' + escHtml(b.mission) + '</p></div>';
  }
  // Attention
  if (attnItems.length) {
    h += '<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px">';
    h += '<h3 style="margin:0 0 12px;font-size:14px;text-transform:uppercase;letter-spacing:0.5px;color:var(--muted)">Needs attention (' + attnItems.length + ')</h3>';
    attnItems.slice(0, 5).forEach(a => {
      h += '<div style="padding:8px 0;border-bottom:1px solid var(--border)"><span style="color:#f0a35e">●</span> ' + escHtml(a.text || a) + '</div>';
    });
    h += '</div>';
  }
  // Children
  if (kids.length) {
    h += '<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px">';
    h += '<h3 style="margin:0 0 12px;font-size:14px;text-transform:uppercase;letter-spacing:0.5px;color:var(--muted)">Sub-buddies (' + kids.length + ')</h3>';
    h += '<div style="display:flex;flex-wrap:wrap;gap:8px">';
    kids.forEach(k => {
      h += '<span style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:14px">' + (k.icon || '🤖') + ' ' + escHtml(dispName(k)) + '</span>';
    });
    h += '</div></div>';
  }
  // Artifacts
  if (arts.length) {
    h += '<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px">';
    h += '<h3 style="margin:0 0 12px;font-size:14px;text-transform:uppercase;letter-spacing:0.5px;color:var(--muted)">Artifacts (' + arts.length + ')</h3>';
    arts.slice(0, 6).forEach(a => {
      h += '<div style="padding:6px 0"><a href="' + escHtml(a.url || '#') + '" target="_blank" style="color:var(--accent);text-decoration:none">' + escHtml(a.title || a.name || 'Artifact') + '</a></div>';
    });
    h += '</div>';
  }
  h += '<p style="text-align:center;color:var(--muted);font-size:12px;margin-top:32px">Auto-generated homepage — set a custom URL in the Homepage URL field to override.</p>';
  h += '</div>';
  return h;
}
function renderProjectView(){
  const pv = document.getElementById('view-project');
  if (!pv) return;
  const b = byId[projectId()] || {};
  pv.innerHTML = '';
  const hp = getHomepage(b);
  document.getElementById('main').classList.add('homepage-mode');
  const bar2 = document.getElementById('journal-bar');
  if (bar2) bar2.classList.remove('show');
  const wrap = document.createElement('div');
  wrap.id = 'homepage-wrap';
  if (hp) {
    // Custom homepage URL: load in iframe ("Open in a new tab" lives in the right detail panel footer)
    const frame = document.createElement('iframe');
    frame.id = 'homepage-frame';
    frame.src = hp;
    frame.title = b.name + ' homepage';
    frame.addEventListener('load', () => {
      try {
        frame.contentWindow.addEventListener('keydown', e => {
          if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) {
            document.dispatchEvent(new KeyboardEvent('keydown', {key: e.key, bubbles: true, cancelable: true}));
            e.preventDefault();
          }
        });
      } catch (err) {}
    });
    wrap.appendChild(frame);
  } else {
    // No custom URL: auto-generate homepage
    const content = document.createElement('div');
    content.id = 'homepage-frame';
    content.style.cssText = 'width:100%;height:100%;overflow:auto;background:var(--bg)';
    content.innerHTML = buddyHomepageHtml(b);
    wrap.appendChild(content);
  }
  pv.appendChild(wrap);
}
function renderBuddy(id){
  const b = byId[id]; if(!b) return;
  const items = (b.attention || []).slice().sort((x,y) => (S.seen[x.id]?1:0) - (S.seen[y.id]?1:0));
  let arts = '';
  if (b.brief) arts += artRow(ICON_DOC, 'Mission statement', 'The canonical mission & intent — Google Doc', b.brief);
  if (b.homepageSource) arts += artRow(ICON_LINK, 'Homepage', 'Buddy homepage — opens on Muse', b.homepageSource);
  if (b.repo) arts += artRow(ICON_REPO, 'GitHub Repo', 'davedellaquila/'+b.repo+' (private)', 'https://github.com/davedellaquila/'+b.repo);
  (b.docs || []).forEach(d => { arts += artRow(ICON_LINK, d.label, 'Related document — Google Doc', d.url); });
  if (!arts) arts = '<p class="bp-empty">No artifacts yet — the drill adds the mission statement and repo here when they exist.</p>';
  let photos = '';
  const seedStrip = (b.photos || []).map(u => '<a href="'+escHtml(u)+'" target="_blank" rel="noopener"><img src="'+escHtml(u)+'" loading="lazy" alt=""></a>').join('');
  photos = '<div class="bp-sec" data-field="photos"><h3 id="photos-h3">Photos</h3><div class="prow"><div class="pstrip" id="pstrip">' + seedStrip + '</div>'
    + '<div class="pdrop" id="pdrop">Drop photos here or click to choose<br><span style="font-size:12px">JPEG, PNG, GIF, WebP, HEIC \\u2014 all supported</span></div></div>'
    + '<p class="fineprint" id="pstat"></p></div>';
  const linkedPlans = PLANS.filter(p => (p.buddies || []).includes(id));
  let planSec = '';
  if (linkedPlans.length) {
    planSec = '<div class="bp-sec" data-field="plans"><h3>Business plans</h3>' + linkedPlans.map(p =>
      '<a class="art-row" href="#" data-plan="'+p.id+'">'
      + '<span class="art-ic">'+escHtml(p.icon||'💼')+'</span>'
      + '<span><span class="art-label">'+escHtml(p.name)+'</span><div class="art-sub">BRD / business plan · '+escHtml(p.status)+'</div></span>'
      + '<span class="art-go">→</span></a>').join('') + '</div>';
  }
  let attn = '';
  let unseenCount = 0;
  if (!items.length) attn = '';
  else {
    attn = items.map(a => {
      const seen = !!S.seen[a.id];
      return '<div class="attn'+(seen?' seen':' unseen')+'" data-attn="'+a.id+'"><span class="adot"></span>'
        + '<div class="attn-body"><div class="attn-text">'+escHtml(a.text)+'</div>'
        + '<div class="attn-date">Asked '+a.date+'</div></div>'
        + '<button class="seenbtn" data-seen="'+a.id+'">Mark seen</button></div>';
    }).join('');
    const un = items.filter(a => !S.seen[a.id]).length;
    unseenCount = un;
    if (un > 1) attn += '<div class="attn-all"><button class="seenbtn" data-seen-all="'+id+'">Mark all seen</button></div>';
  }
  document.getElementById('buddy-home').innerHTML =
    '<div class="bp-wrap">'
    + '<button class="bp-takeover-back" id="bp-takeover-back" type="button" title="Close detail \u2014 back to main view" aria-label="Close detail \u2014 back to main view">\u2039 Main</button>'
    + '<div id="token-banner"><h4>\U0001f511 Connect GitHub to unlock this buddy</h4>'
    + '<p>Photos, shared notes, and ingest save to the buddy\u2019s repo. Paste a token once \u2014 it stays on this device.</p>'
    + '<div class="ghtoken"><input type="password" id="ghtok2" placeholder="GitHub token (repo scope)" aria-label="GitHub token">'
    + '<button class="linkbtn" id="ghtok2-save">Save token</button>'
    + '<a href="https://github.com/settings/tokens" target="_blank" rel="noopener" class="linkbtn" style="text-decoration:none" title="Open GitHub token settings in a new tab">Get a token</a></div></div>'
    + '<div class="sa-bar"><span>\U0001f516 Standalone view</span><button class="linkbtn" id="sa-full">Open full dashboard \u2192</button></div>'
    + '<div class="bp-topnav"><button class="linkbtn" data-navbtn="back">\u2190 Back</button>'
    + '<button class="linkbtn" data-navbtn="prev">\u2039 Prev</button><button class="linkbtn" data-navbtn="next">Next \u203a</button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" data-view="tree">All buddies</button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" id="bp-close" type="button" title="Collapse buddy details" aria-label="Collapse buddy details">\u203a Close</button><span class="sep">\u00b7</span><button class="linkbtn" id="bp-desktop">\U0001f4be Save to desktop</button></div>'
    + '<div class="bp-crumb">'+crumb(id)+'</div>'
    + '<p class="bp-tagline">'+escHtml(b.tagline||'')+'</p>'
    + '<div class="bp-sticky-head"><div class="bp-top">'
    + '<span class="bp-icon" id="bp-icon" title="Click to change avatar" style="cursor:pointer">'+escHtml(b.icon||'')+'</span>'
    + '<h2 class="bp-name" id="bp-name" contenteditable="true" spellcheck="false" data-buddy="'+id+'">'+escHtml(dispName(b))+'</h2>'
    + '<span class="status '+b.statusClass+'">'+escHtml(b.status)+'</span>'
    + '<button class="bp-close-x" id="bp-close-x" type="button" title="Collapse buddy details" aria-label="Collapse buddy details"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button></div></div>'
    + standingOrdersHtml()
    + '<div class="bp-sec" data-field="ingest"><h3>Ingest<span class="info-tip" data-tip="Brain-dump anything about this buddy \u2014 raw and unfiltered. Each dump lands in the buddy\u2019s repo (docs/ingest.md) as a timestamped entry.">\u24d8</span></h3>'
    + '<textarea class="notes" id="bp-ingest" placeholder="Dump what\u2019s in your head about '+escHtml(dispName(b))+'\u2026"></textarea>'
    + '<div style="margin-top:8px"><span class="fineprint" id="ingest-status"></span></div>'
    + '<div id="ingest-feed" style="margin-top:8px"></div></div>'
    + '<div class="bp-sec" data-field="mission"><h3>About<span class="info-tip" data-tip="The mission statement\\u2019s executive summary \\u2014 tweak it through the buddy\\u2019s chat thread and it updates everywhere.">\\u24d8</span></h3><p class="bp-mission">'+escHtml(b.mission)+'</p></div>'
    + '<div class="bp-sec" data-field="homepage"><h3>Homepage URL</h3>'
    + '<div style="display:flex;align-items:center;gap:8px">'
    + '<input type="url" id="bp-homepage-url" value="'+escHtml(homepageUrl(b))+'" placeholder="Paste homepage URL here…" style="flex:1;min-width:0;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:13px;color:var(--text)" title="The full URL for this buddy\u2019s homepage. Paste a URL and click away to save.">'
    + '<button class="linkbtn" id="bp-homepage-copy" title="Copy homepage URL to clipboard" style="flex-shrink:0">Copy</button>'
    + '</div></div>'
    + (unseenCount > 0 ? '<div class="bp-sec" data-field="attention"><h3>Needs your attention</h3>'+attn+'</div>' : '')
    + photos
    + (id === 'project-buddy'
        ? '<div class="bp-sec" data-field="tree"><h3>The Buddy Tree</h3><div class="bp-tree-wrap"></div>'
          + '<p class="fineprint"><button class="linkbtn" data-view="tree">Open the tree as its own view \\u2192</button></p></div>'
        : '')
    + '<div class="bp-sec" data-field="artifacts"><h3>Artifacts</h3>'+arts+'</div>'
    + planSec
    + '<div class="bp-sec" data-field="notes"><h3>Notes<span class="info-tip" data-tip="Saved on this device. (For your eyes only)">\u24d8</span></h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this buddy\u2026 (For your eyes only)">'+escHtml(S.notes[id]||'')+'</textarea>'
    + '</div>'
    + '<div class="bp-sec" data-field="shared"><h3>Shared notes<span class="info-tip" data-tip="Anybody with repo access can see this note. Saved to the buddy\u2019s repo (docs/notes.md).">\u24d8</span></h3>'
    + '<textarea class="notes" id="bp-shared-notes" placeholder="Anybody with repo access can see this note."></textarea>'
    + '<p class="fineprint" id="shared-status"></p></div>'
    + '<div class="bp-footer">'
    + (getHomepage(b)
        ? '<a class="linkbtn" id="bp-open-tab" href="'+escHtml(b.homepageSource || getHomepage(b))+'" target="_blank" rel="noopener" title="Open this buddy\u2019s homepage in a new tab">Open in a new tab</a>'
        : '')
    + '<div class="bp-build">Build __BUILD__</div></div>'
    + '</div>';
  const nm = document.getElementById('bp-name');
  nm.addEventListener('keydown', e => { if (e.key === 'Enter'){ e.preventDefault(); nm.blur(); } });
  nm.addEventListener('blur', () => {
    const v = nm.textContent.trim();
    const before = S.names[id] != null ? S.names[id] : null;
    const beforeLabel = dispName(b);
    if (v && v !== beforeLabel) S.names[id] = v; else delete S.names[id];
    const after = S.names[id] != null ? S.names[id] : null;
    if (before !== after) logChange('rename', id, 'Renamed \u201c' + beforeLabel + '\u201d \u2192 \u201c' + dispName(byId[id]) + '\u201d', before, after);
    save(); renderNav();
    // Immediately reflect the new name in the current view
    if (S.view === 'project' && S.projectId === id) renderProjectView();
    else if (S.view === 'projects') renderProjects();
    // Update the panel itself to show the new name (in case hideBuddyWord applies)
    renderBuddy(id);
  });
  // Homepage URL field: editable text input, saves to S.homepages override
  const hpu = document.getElementById('bp-homepage-url');
  if (hpu) {
    hpu.addEventListener('keydown', e => { if (e.key === 'Enter'){ e.preventDefault(); hpu.blur(); } });
    const saveHomepageUrl = () => {
      const v = hpu.value.trim();
      if (!S.homepages || typeof S.homepages !== 'object') S.homepages = {};
      const before = getHomepage(b);
      // Don't save if the value matches the current resolved URL (no change)
      // or if it's empty (clear the override)
      const currentResolved = homepageUrl(b);
      if (!v || v === currentResolved || v === b.homepage) {
        delete S.homepages[id];
      } else {
        S.homepages[id] = v;
      }
      const after = getHomepage(b);
      if (before !== after) logChange('homepage', id, 'Homepage URL \u2192 ' + (after || '(cleared)'), before || null, after || null);
      save();
      // If the Project Homepage view is showing this buddy, reload it with the new URL
      if (S.sel === 'view:project' && S.projectId === id) {
        renderProjectView();
      }
    };
    hpu.addEventListener('blur', saveHomepageUrl);
    // Update immediately on paste (don't wait for blur)
    hpu.addEventListener('paste', () => { setTimeout(saveHomepageUrl, 0); });
    // Prevent the global click handler from re-opening the buddy when clicking the input
    hpu.addEventListener('click', e => e.stopPropagation());
  }
  const hpc = document.getElementById('bp-homepage-copy');
  if (hpc) {
    hpc.addEventListener('click', e => {
      e.stopPropagation();
      const url = (document.getElementById('bp-homepage-url') || {}).value || getHomepage(b);
      if (!url) return;
      const done = () => { hpc.textContent = 'Copied!'; setTimeout(() => { hpc.textContent = 'Copy'; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done).catch(() => {});
      } else {
        const ta = document.createElement('textarea'); ta.value = url; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (err) {}
        ta.remove();
      }
    });
  }
  const nt = document.getElementById('bp-notes');
  let t = null, notesBefore = null;
  nt.addEventListener('focus', () => { notesBefore = nt.value; });
  nt.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { S.notes[id] = nt.value; save(); }, 400); });
  nt.addEventListener('blur', () => {
    if (notesBefore !== null && notesBefore !== nt.value) logChange('notes', id, 'Edited notes for \u201c' + dispName(byId[id]) + '\u201d', notesBefore, nt.value);
    notesBefore = null;
  });
  (function initIngestAuto(bid){
    const ta = document.getElementById('bp-ingest'), st = document.getElementById('ingest-status');
    if (!ta || ta.dataset.auto) return;
    ta.dataset.auto = '1';
    let t = null, lastDumped = '';
    ta.addEventListener('input', () => {
      clearTimeout(t);
      const txt = ta.value.trim();
      if (!txt || txt === lastDumped) { if (st && !txt) st.textContent = ''; return; }
      if (st) st.textContent = 'waiting\u2026';
      t = setTimeout(async () => {
        const cur = ta.value.trim();
        if (!cur || cur === lastDumped) return;
        if (st) st.textContent = 'dumping\u2026';
        const dumped = cur;
        await dumpIngest(bid, false);
        lastDumped = dumped;
        if (st) st.textContent = 'dumped \u2713 — see Dumps below';
      }, 2000);
    });
    ta.addEventListener('keydown', async e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        clearTimeout(t);
        const cur = ta.value.trim();
        if (!cur || cur === lastDumped) return;
        if (st) st.textContent = 'dumping\u2026';
        const dumped = cur;
        await dumpIngest(bid, false);
        lastDumped = dumped;
        if (st) st.textContent = 'dumped \u2713 — see Dumps below';
      }
    });
  })(id);
  loadPhotos(id);
  initPhotoDrop(id);
  initPanelResize(); applyPanelWidth();
  refreshTokenUI(id);
  applyFieldOrder();
  applySectionCollapse(id);
  renderJournal();
  if (id === 'project-buddy') {
    const tw = document.querySelector('#buddy-home .bp-tree-wrap');
    const srcEl = document.getElementById('view-tree');
    if (tw && srcEl) {
      tw.innerHTML = '<div class="bp-mini-zoom"><button id="bp-mz-out" title="Zoom out">\u2212</button><button id="bp-mz-in" title="Zoom in">+</button></div><div class="bp-mini-chart"></div>';
      const mc = tw.querySelector('.bp-mini-chart');
      mc.innerHTML = srcEl.innerHTML;
      const zb = mc.querySelector('#zoombar'); if (zb) zb.remove();
      const zw = mc.querySelector('#zoomwrap'); if (zw) { zw.style.display = 'block'; }
      const tz = mc.querySelector('#treezoom'); if (tz) { tz.style.overflow = 'visible'; tz.style.height = 'auto'; tz.removeAttribute('id'); }
      let mz = 80;
      const applyMz = () => { const ch = mc.querySelector('.chart'); if (ch) ch.style.zoom = mz + '%'; };
      applyMz();
      document.getElementById('bp-mz-in').addEventListener('click', e => { e.stopPropagation(); mz = Math.min(150, mz + 10); applyMz(); });
      document.getElementById('bp-mz-out').addEventListener('click', e => { e.stopPropagation(); mz = Math.max(20, mz - 10); applyMz(); });
      attachPan(tw);
    }
  }
}
function toast(msg){
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const t = document.createElement('div');
  t.className = 'toast'; t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => { if (t.parentNode) t.remove(); }, 3400);
}
function setIcon(emoji){
  if (!emoji) return;
  const svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>"+emoji+"</text></svg>";
  let l = document.querySelector("link[rel='icon']");
  if (!l) { l = document.createElement('link'); l.rel = 'icon'; document.head.appendChild(l); }
  l.type = 'image/svg+xml';
  l.href = 'data:image/svg+xml,' + encodeURIComponent(svg);
  try {
    const c = document.createElement('canvas'); c.width = c.height = 180;
    const x = c.getContext('2d');
    x.fillStyle = (getComputedStyle(document.documentElement).getPropertyValue('--bg') || '#0d1117').trim() || '#0d1117'; x.fillRect(0, 0, 180, 180);
    x.font = '135px serif'; x.textAlign = 'center'; x.textBaseline = 'middle';
    x.fillText(emoji, 90, 96);
    let a = document.querySelector("link[rel='apple-touch-icon']");
    if (!a) { a = document.createElement('link'); a.rel = 'apple-touch-icon'; document.head.appendChild(a); }
    a.href = c.toDataURL('image/png');
  } catch (e) {}
}
function isDesc(id, anc){
  let p = byId[id] ? effParent(byId[id]) : null;
  while (p) { if (p === anc) return true; p = byId[p] ? effParent(byId[p]) : null; }
  return false;
}
function moveBuddy(src, target){
  if (!src || !target || src === target) return;
  const b = byId[src]; if (!b || !byId[target]) return;
  if (isDesc(target, src)) { toast('Can\u2019t move ' + dispName(b) + ' under ' + dispName(byId[target]) + ' \u2014 that would create a loop.'); return; }
  const beforeParent = effParent(b);
  if (target === b.parent) delete S.parents[src]; else S.parents[src] = target;
  logChange('move', src, 'Moved \u201c' + dispName(byId[src]) + '\u201d under \u201c' + dispName(byId[target]) + '\u201d', beforeParent, target);
  save(); buildKids(); renderNav(); refreshViews();
  if (S.sel === 'buddy:' + src || S.sel === 'buddy:' + target || S.sel === 'buddy:project-buddy') renderBuddy(S.sel.slice(6));
  toast(dispName(b) + ' moved under ' + dispName(byId[target]) + '.');
}
const FAMKINDS = ['personal', 'family', 'property', 'finance', 'work'];
function nodeTag(b, depth){
  if (depth === 1) {
    if (b.kind === 'work') return 'direct child';
    if (b.kind === 'meta') return 'meta';
    if (b.kind === 'standalone') return 'direct';
    return 'family';
  }
  return depth === 2 ? 'child' : 'grandchild';
}
function iconName(b){ return escHtml((b.icon ? b.icon + ' ' : '') + dispName(b)); }
function gridKids(b){
  const kids = kidsOf[b.id] || [];
  if (!kids.length) return '';
  return '<ul class="subkids">' + kids.map(c =>
    '<li><div class="node ' + c.kind + '" data-buddy="' + c.id + '"><div class="name">' + iconName(c) + '</div>'
    + '<div class="desc">' + escHtml(c.tagline || '') + '</div><div class="tag">' + nodeTag(c, 2) + '</div>'
    + gridKids(c) + '</div></li>').join('') + '</ul>';
}
function orgNode(b, depth){
  const kids = kidsOf[b.id] || [];
  const kc = kids.length ? '<span class="kcount">' + kids.length + '</span>' : '';
  let s = '<li><div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + '<div class="name">' + iconName(b) + kc + '</div>'
    + '<div class="desc">' + escHtml(b.tagline || '') + '</div>'
    + '<div class="tag">' + nodeTag(b, depth) + '</div></div>';
  if (kids.length) s += '<ul>' + kids.map(c => orgNode(c, depth + 1)).join('') + '</ul>';
  return s + '</li>';
}
function renderOrgTree(){
  const root = byId['project-buddy'];
  const kids = kidsOf['project-buddy'] || [];
  const fam = kids.filter(b => FAMKINDS.includes(b.kind));
  const rest = kids.filter(b => !FAMKINDS.includes(b.kind));
  let s = '<div class="chart"><div style="text-align:center"><div class="node root" data-buddy="project-buddy">'
    + '<div class="name">' + iconName(root) + '</div>'
    + '<div class="desc">' + escHtml(root.tagline || '') + '</div></div></div>'
    + '<div class="root-stub"></div><div class="tree"><ul>'
    + fam.map(b => orgNode(b, 1)).join('') + '</ul></div></div>';
  if (rest.length) {
    s += '<section class="standalones"><h2>Orphaned buddies</h2>'
      + '<p class="sub">No meaningful parent yet &mdash; drag one onto a buddy in the tree to give it a home, or drop it here to detach.</p>'
      + '<div class="grid">'
      + rest.map(b => '<div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + '<div class="name">' + iconName(b) + '</div>'
        + '<div class="desc">' + escHtml(b.tagline || '') + '</div><div class="tag">' + nodeTag(b, 1) + '</div>'
        + gridKids(b) + '</div>').join('')
      + '</div></section>';
  }
  const orphans = (kidsOf['__root'] || []).filter(b => b.id !== 'project-buddy');
  if (orphans.length) {
    s += '<section class="standalones"><h2>Orphaned buddies</h2>'
      + '<p class="sub">No parent yet &mdash; drag one onto a buddy in the tree to give it a home.</p>'
      + '<div class="grid">'
      + orphans.map(b => '<div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + '<div class="name">' + iconName(b) + '</div>'
        + '<div class="desc">' + escHtml(b.tagline || '') + '</div></div>').join('')
      + '</div></section>';
  }
  document.getElementById('treezoom').innerHTML = s;
}
function renderProjects(){
  if (!S.projCollapsed || typeof S.projCollapsed !== 'object') S.projCollapsed = {};
  let unseen = 0, fresh = 0, cleared = 0;
  const weekAgo = Date.now() - 7 * 864e5;
  const statusCounts = {};
  Object.values(byId).forEach(b => {
    const st = b.status || 'Unknown';
    statusCounts[st] = (statusCounts[st] || 0) + 1;
    (b.attention || []).forEach(a => {
      if (S.seen[a.id]) cleared++; else unseen++;
      const t = Date.parse(a.date || '');
      if (t && t >= weekAgo) fresh++;
    });
  });
  // Status tint colors (match the pills)
  const statusTints = {'Active':'#1f6feb','Live · M2 shipped':'#2f9e44','Live · pre-alpha':'#2f9e44','New':'#d97a1f','Mission review':'#a371f7','PRD review':'#a371f7','Pilot':'#1f6feb','Spec review':'#a371f7'};
  const statusOrder = Object.keys(statusCounts).sort();
  let s = '<section class="projects-view" style="margin-top:24px">'
    + '<div id="project-tiles">'
    + tileHtml('TO REVIEW', unseen, '#d43d2a', 'Needs your attention', 'unseen', projFilter === 'unseen')
    + tileHtml('NEW', fresh, '#d97a1f', 'Added in the last 7 days', 'fresh', projFilter === 'fresh')
    + tileHtml('CLEARED', cleared, '#2f9e44', 'Reviewed & cleared', 'cleared', projFilter === 'cleared')
    + '</div>'
    + '<div id="project-status-tiles" style="margin-top:12px">'
    + statusOrder.map(st => tileHtml(st.toUpperCase(), statusCounts[st], statusTints[st] || '#8b949e', st + ' projects', 'status:' + st, statusFilter === st, 'Click to filter by ' + st + ' status. Click again to clear.')).join('')
    + '</div>'
    + '<h2>Projects by Buddy</h2>'
    + '<p class="sub">Every buddy, in hierarchy order, with its current status.</p><div class="proj-list">';
  // When a tile filter is active, show matching buddies plus their ancestors
  let showIds = null;
  if (projFilter) {
    const matches = b => (b.attention || []).some(a => {
      const seen = !!S.seen[a.id];
      if (projFilter === 'unseen') return !seen;
      if (projFilter === 'cleared') return seen;
      const t = Date.parse(a.date || '');
      return t && t >= weekAgo;
    });
    showIds = {};
    Object.values(byId).forEach(b => {
      if (!matches(b)) return;
      let x = b;
      while (x) { showIds[x.id] = true; const p = effParent(x); x = p ? byId[p] : null; }
    });
  } else if (statusFilter) {
    showIds = {};
    Object.values(byId).forEach(b => {
      if ((b.status || 'Unknown') !== statusFilter) return;
      let x = b;
      while (x) { showIds[x.id] = true; const p = effParent(x); x = p ? byId[p] : null; }
    });
  }
  (function walk(id, depth){
    const b = byId[id]; if (!b) return;
    if (showIds && !showIds[id]) return;
    const kids = kidsOf[id] || [];
    const hasKids = kids.length > 0;
    const collapsed = (projFilter || statusFilter) ? false : !!S.projCollapsed[id];
    s += '<div class="proj-row d' + Math.min(depth, 3) + '" data-buddy="' + b.id + '">'
      + (hasKids ? '<span class="parrow ' + (collapsed ? '' : 'expanded') + '" data-proj-toggle="' + b.id + '">\u203a</span>' : '')
      + (depth ? '<span class="dot">\u2514</span>' : '')
      + '<span class="pname">' + iconName(b) + '</span>'
      + '<span class="pdesc">' + escHtml(b.tagline || '') + '</span>'
      + '<span class="status ' + b.statusClass + '">' + escHtml(b.status) + '</span>'
      + '<button class="proj-info" data-proj-info="' + b.id + '" title="Open ' + escHtml(dispName(b)) + ' details (right panel)" style="background:none;border:none;cursor:pointer;font-size:16px;padding:4px 8px;opacity:0.6" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.6">\u24d8</button></div>';
    if (!collapsed) kids.forEach(c => walk(c.id, depth + 1));
  })('project-buddy', 0);
  s += '</div></section>';
  const vp = document.getElementById('view-projects');
  vp.innerHTML = s;
}
let treeHTML0 = null, projHTML0 = null;
function refreshViews(){
  const tz = document.getElementById('treezoom'), vp = document.getElementById('view-projects');
  if (treeHTML0 === null) { treeHTML0 = tz.innerHTML; projHTML0 = vp.innerHTML; }
  if (Object.keys(S.parents).length) { renderOrgTree(); } else { tz.innerHTML = treeHTML0; }
  renderProjects();
}
function applyZoom(){
  const tz = document.getElementById('treezoom');
  if (tz) tz.style.zoom = (S.zoom || 100) + '%';
  const r = document.getElementById('zoomrange'), v = document.getElementById('zoomval');
  if (r) r.value = S.zoom || 100;
  if (v) v.textContent = (S.zoom || 100) + '%';
}
function zoomToFit(){
  const tz = document.getElementById('treezoom');
  const chart = tz ? tz.querySelector('.chart') : null;
  if (!tz || !chart) return;
  const z = (S.zoom || 100) / 100;
  const natW = chart.scrollWidth / z, natH = chart.scrollHeight / z;
  const vw = tz.clientWidth, vh = tz.clientHeight;
  if (!natW || !natH || !vw || !vh) return;
  const fit = Math.min(vw / natW, vh / natH) * 100;
  S.zoom = Math.min(160, Math.max(50, Math.round(fit / 5) * 5));
  save(); applyZoom();
  toast('Zoomed to fit (' + S.zoom + '%).');
}
(function initZoom(){
  const vt = document.getElementById('view-tree');
  vt.insertAdjacentHTML('afterbegin',
    '<div class="treewrap" id="zoomwrap"><div class="zoombar" id="zoombar" title="Zoom — pinch with two fingers, or Shift+scroll">'
    + '<span class="z-in" aria-hidden="true">\u25fc</span>'
    + '<input type="range" id="zoomrange" min="50" max="160" step="5" value="100" aria-label="Zoom in to zoom out" orient="vertical">'
    + '<span class="z-out" aria-hidden="true">\u25aa</span>'
    + '<button type="button" id="zoomfit" title="Zoom to fit" aria-label="Zoom to fit">\u26f6</button></div><div id="treezoom"></div></div>');
  const tw = document.getElementById('zoomwrap'), tz = document.getElementById('treezoom');
  Array.from(vt.childNodes).forEach(n => { if (n !== tw) tz.appendChild(n); });
  document.getElementById('zoomrange').addEventListener('input', e => {
    S.zoom = parseInt(e.target.value, 10) || 100; save(); applyZoom();
  });
  document.getElementById('zoomfit').addEventListener('click', zoomToFit);
  applyZoom();
})();
(function initBrand(){
  const bn = document.getElementById('brand-name');
  const name = S.appName || 'Buddies';
  bn.textContent = name;
  document.title = name;
  bn.setAttribute('contenteditable', 'true');
  bn.setAttribute('spellcheck', 'false');
  bn.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); bn.blur(); } });
  bn.addEventListener('blur', () => {
    const v = bn.textContent.trim();
    const before = S.appName || null;
    if (v && v !== 'Buddies') S.appName = v; else delete S.appName;
    const after = S.appName || null;
    if (before !== after) logChange('brand', null, 'Renamed app \u201c' + (before || 'Buddies') + '\u201d \u2192 \u201c' + (after || 'Buddies') + '\u201d', before, after);
    applyBrand();
    save();
  });
})();
function attachPan(el){
  if (!el || el.dataset.panAttached) return;
  el.dataset.panAttached = '1';
  // #treezoom is the sole 2D scrollport (both axes). Do not pan nested .chart —
  // overflow-x-only on .chart caused Safari/iOS to lock the first gesture axis.
  function scroller(){ return el; }
  const isTree = el.id === 'treezoom';
  let pan = null, swallow = false;
  /* Tree: track touch pointers for one-finger pan vs two-finger pinch zoom */
  const pts = new Map();
  let pinch = null;
  function pinchDist(){
    const v = [...pts.values()];
    if (v.length < 2) return 0;
    return Math.hypot(v[0].x - v[1].x, v[0].y - v[1].y) || 1;
  }
  function startPan(x, y, pid){
    const sc = scroller();
    pan = { x: x, y: y, sl: sc.scrollLeft, st: sc.scrollTop, moved: false, id: pid };
  }
  function movePan(x, y, pid){
    if (!pan || (pid !== undefined && pid !== pan.id)) return;
    const dx = x - pan.x, dy = y - pan.y;
    if (!pan.moved && Math.abs(dx) + Math.abs(dy) < 5) return;
    if (!pan.moved) {
      // Dragging started — capture pointer so pan continues outside the element
      try { if (pid !== undefined && pid !== 'mouse') el.setPointerCapture(pid); } catch (err) {}
    }
    pan.moved = true;
    const sc = scroller();
    sc.classList.add('panning');
    el.classList.add('panning');
    // Apply both axes every move — free diagonal pan (no axis lock)
    sc.scrollLeft = pan.sl - dx;
    sc.scrollTop = pan.st - dy;
  }
  function endPan(pid){
    if (!pan) return;
    if (pid !== undefined && pid !== pan.id) return;
    try { if (el.releasePointerCapture && pan.id !== undefined && pan.id !== 'mouse') el.releasePointerCapture(pan.id); } catch (err) {}
    const sc = scroller();
    sc.classList.remove('panning');
    el.classList.remove('panning');
    if (pan.moved) { swallow = true; setTimeout(() => { swallow = false; }, 80); }
    pan = null;
  }
  function beginPinch(){
    if (pan) endPan(pan.id);
    const d0 = pinchDist();
    if (d0 < 8) return;
    pinch = { d0: d0, z0: S.zoom || 100 };
    el.dataset.pinching = '1';
    el.classList.add('panning');
    swallow = true;
  }
  function movePinch(){
    if (!pinch || pts.size < 2) return;
    const d = pinchDist();
    const next = Math.min(160, Math.max(50, Math.round((pinch.z0 * (d / pinch.d0)) / 5) * 5));
    if (next !== (S.zoom || 100)) { S.zoom = next; applyZoom(); }
  }
  function endPinchFinger(pid){
    pts.delete(pid);
    if (pts.size < 2 && pinch) {
      pinch = null;
      delete el.dataset.pinching;
      el.classList.remove('panning');
      save();
      setTimeout(() => { swallow = false; }, 80);
    }
  }
  // Pointer Events — mouse + touch/pen on the tree (touch-action:none) for free 2D pan
  el.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    if (!isTree && e.pointerType !== 'mouse') return; // projects/manifest keep native touch scroll
    // Tree pinch: track all non-mouse pointers (including on nodes) so 2-finger zoom works
    if (isTree && e.pointerType !== 'mouse') {
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pts.size >= 2) { beginPinch(); e.preventDefault(); return; }
    }
    if (pinch) return;
    // Presses on tree nodes are reserved for node drag-to-reparent (or click); background pans.
    if (e.target.closest && (e.target.closest('#treezoom .node[data-buddy]') || e.target.closest('input,textarea,button'))) return;
    startPan(e.clientX, e.clientY, e.pointerId);
    // Don't set pointer capture here — it interferes with click events on tree nodes.
    // Capture is set in movePan once dragging actually starts.
  });
  el.addEventListener('pointermove', e => {
    if (isTree && pts.has(e.pointerId)) {
      pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pinch) { movePinch(); e.preventDefault(); return; }
    }
    if (pinch) return;
    if (!pan || e.pointerId !== pan.id) return;
    movePan(e.clientX, e.clientY, e.pointerId);
    if (pan && pan.moved) e.preventDefault();
  }, { passive: false });
  el.addEventListener('pointerup', e => {
    if (isTree) endPinchFinger(e.pointerId);
    endPan(e.pointerId);
  });
  el.addEventListener('pointercancel', e => {
    if (isTree) endPinchFinger(e.pointerId);
    endPan(e.pointerId);
  });
  // Mouse Events fallback (older Safari)
  el.addEventListener('mousedown', e => {
    if (pan || pinch) return;
    if (e.button !== 0) return;
    if (e.target.closest && (e.target.closest('#treezoom .node[data-buddy]') || e.target.closest('input,textarea,button'))) return;
    startPan(e.clientX, e.clientY, 'mouse');
    e.preventDefault();
  });
  window.addEventListener('mousemove', e => { if (pan && pan.id === 'mouse') movePan(e.clientX, e.clientY, 'mouse'); });
  window.addEventListener('mouseup', e => { if (pan && pan.id === 'mouse') endPan('mouse'); });
  el.addEventListener('click', e => {
    if (swallow) { e.preventDefault(); e.stopPropagation(); }
  }, true);
}
function initPan(){
  attachPan(document.getElementById('treezoom'));
  attachPan(document.getElementById('view-projects'));
  attachPan(document.getElementById('view-manifest'));
}
initPan();
/* ---------- tree node drag-to-reparent (pointer events: mouse + touch) ----------
   Whole-tile drag: press a node and move >6px to drag it; a simple tap still
   opens the buddy detail panel. Works with mouse and touch (HTML5 DnD never
   fires on touch, which is why the old gripper handles could not work there).
   Dragging a node reparents it; dragging empty background pans the chart. */
let nodeDragEndAt = 0; // timestamp of last node-drag gesture; used to swallow the follow-up click
(function initNodeDrag(){
  const tz = document.getElementById('treezoom');
  if (!tz) return;
  const THRESH = 6; // px of movement before a press becomes a drag (less = click)
  let cand = null;  // {id, x0, y0, pid} — pressed on a node, drag not yet started
  let drag = null;  // {id, pid, ghost, target} — active drag

  function treeNodeFrom(el){
    return (el && el.closest) ? el.closest('#treezoom .node[data-buddy]') : null;
  }
  var TOUCH_SLOP = 16; // px of extra hit area around each node during a touch drag
  function nodeAt(x, y, touch){
    if (!touch) return treeNodeFrom(document.elementFromPoint(x, y));
    // Touch: finger covers the exact point, so test inflated rects and take the smallest match.
    var nodes = tz.querySelectorAll('.node[data-buddy]'), best = null, bestArea = Infinity;
    for (var i = 0; i < nodes.length; i++){
      var r = nodes[i].getBoundingClientRect();
      if (x >= r.left - TOUCH_SLOP && x <= r.right + TOUCH_SLOP && y >= r.top - TOUCH_SLOP && y <= r.bottom + TOUCH_SLOP){
        var area = r.width * r.height;
        if (area < bestArea){ bestArea = area; best = nodes[i]; }
      }
    }
    return best;
  }
  function clearHl(){
    tz.querySelectorAll('.node.drop-target,.node.drop-invalid').forEach(function(x){ x.classList.remove('drop-target', 'drop-invalid'); });
  }
  function moveGhost(x, y){
    if (drag && drag.ghost) { drag.ghost.style.left = x + 'px'; drag.ghost.style.top = y + 'px'; }
  }
  function updateTarget(x, y){
    clearHl();
    drag.target = null;
    const n = nodeAt(x, y, drag.touch);
    if (!n) return;
    const tid = n.dataset.buddy;
    if (!tid || tid === drag.id) return; // self: no highlight, no drop
    if (tid === 'project-buddy' || !isDesc(tid, drag.id)) {
      n.classList.add('drop-target'); drag.target = tid; // valid (root included)
    } else {
      n.classList.add('drop-invalid'); // dropping here would create a cycle
    }
  }
  function cleanup(){
    clearHl();
    tz.querySelectorAll('.node.drag-src').forEach(function(x){ x.classList.remove('drag-src'); });
    if (drag && drag.ghost && drag.ghost.parentNode) drag.ghost.parentNode.removeChild(drag.ghost);
    document.body.classList.remove('node-dragging');
    drag = null; cand = null;
  }
  function beginDrag(x, y){
    const c = cand, id = c.id;
    const src = tz.querySelector('.node[data-buddy="' + id + '"]');
    const ghost = document.createElement('div');
    ghost.className = 'node-drag-ghost';
    let label = id;
    if (src) {
      const nm = src.querySelector('.name');
      label = (nm ? nm.textContent : src.textContent) || id;
    }
    const nmDiv = document.createElement('div');
    nmDiv.className = 'name';
    nmDiv.textContent = label.trim().slice(0, 60);
    ghost.appendChild(nmDiv);
    document.body.appendChild(ghost);
    drag = { id: id, pid: c.pid, ghost: ghost, target: null, touch: !!c.touch };
    cand = null;
    if (src) src.classList.add('drag-src');
    document.body.classList.add('node-dragging');
    moveGhost(x, y);
    updateTarget(x, y);
  }
  tz.addEventListener('pointerdown', function(e){
    if (e.button !== undefined && e.button !== 0) return;
    if (e.isPrimary === false) return;
    const n = treeNodeFrom(e.target);
    if (!n) return;
    const id = n.dataset.buddy;
    if (!id || id === 'project-buddy') return; // root can't be reparented
    cand = { id: id, x0: e.clientX, y0: e.clientY, pid: e.pointerId, touch: e.pointerType === 'touch' };
  });
  window.addEventListener('pointermove', function(e){
    // Two-finger pinch owns the gesture — abort any node drag candidate
    if (tz.dataset.pinching) { if (drag || cand) cleanup(); return; }
    if (drag) {
      if (e.pointerId !== drag.pid) return;
      moveGhost(e.clientX, e.clientY);
      updateTarget(e.clientX, e.clientY);
      return;
    }
    if (cand && e.pointerId === cand.pid) {
      const dx = e.clientX - cand.x0, dy = e.clientY - cand.y0;
      if (dx * dx + dy * dy > THRESH * THRESH) beginDrag(e.clientX, e.clientY);
    }
  }, { passive: true });
  function finish(e, cancelled){
    if (drag && e.pointerId === drag.pid) {
      const src = drag.id, tid = drag.target;
      cleanup();
      nodeDragEndAt = Date.now(); // swallow the click that follows a drag gesture
      if (!cancelled && tid) moveBuddy(src, tid);
      return;
    }
    if (cand && e.pointerId === cand.pid) cand = null;
  }
  window.addEventListener('pointerup', function(e){ finish(e, false); });
  window.addEventListener('pointercancel', function(e){ finish(e, true); });
})();
(function initTreeDrop(){
  function target(e){
    return (e.target && e.target.closest) ? e.target.closest('#treezoom .node[data-buddy], #view-projects .proj-row[data-buddy]') : null;
  }
  function clearHl(){ document.querySelectorAll('.node.drop-target,.proj-row.drop-target').forEach(x => x.classList.remove('drop-target')); }
  document.addEventListener('dragover', e => {
    const n = target(e);
    if (!dragId) return;
    if (n && n.dataset.buddy === dragId) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    document.querySelectorAll('.node.drop-target,.proj-row.drop-target').forEach(x => { if (x !== n) x.classList.remove('drop-target'); });
    if (n) n.classList.add('drop-target');
  });
  document.addEventListener('drop', e => {
    const n = target(e);
    if (!dragId) return;
    e.preventDefault();
    const src = dragId;
    dragId = null; clearHl();
    if (n) {
      moveBuddy(src, n.dataset.buddy);
    } else {
      // Dropped on blank background: detach (no parent)
      const b = byId[src];
      if (b) {
        const beforeParent = effParent(b);
        if (b.parent) { /* has real parent in data */ }
        delete S.parents[src];
        // Set explicit orphan: parent = null override
        S.parents[src] = null;
        logChange('move', src, 'Detached \u201c' + dispName(b) + '\u201d (now orphaned)', beforeParent, null);
        save(); buildKids(); renderNav(); refreshViews();
        toast(dispName(b) + ' detached \u2014 now an orphan.');
      }
    }
  });
  document.addEventListener('dragend', () => { dragId = null; clearHl(); });
})();
document.getElementById('view-tree').addEventListener('wheel', e => {
  if (!e.shiftKey) return;
  e.preventDefault();
  S.zoom = Math.min(160, Math.max(50, (S.zoom || 100) + (e.deltaY > 0 ? -5 : 5)));
  save(); applyZoom();
}, { passive: false });
let dragId = null;
(function initDrag(){
  const nav = document.getElementById('buddy-nav');
  nav.addEventListener('dragstart', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || r.dataset.buddy === 'project-buddy') { e.preventDefault(); return; }
    dragId = r.dataset.buddy;
    e.dataTransfer.effectAllowed = 'move';
    try { e.dataTransfer.setData('text/plain', dragId); } catch (_e) {}
    r.classList.add('dragging');
  });
  nav.addEventListener('dragend', () => {
    dragId = null;
    nav.querySelectorAll('.dragging,.drop-target').forEach(x => x.classList.remove('dragging', 'drop-target'));
  });
  nav.addEventListener('dragover', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || !dragId || r.dataset.buddy === dragId) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    nav.querySelectorAll('.drop-target').forEach(x => { if (x !== r) x.classList.remove('drop-target'); });
    r.classList.add('drop-target');
  });
  nav.addEventListener('drop', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || !dragId) return;
    e.preventDefault();
    const src = dragId, target = r.dataset.buddy;
    dragId = null;
    nav.querySelectorAll('.drop-target').forEach(x => x.classList.remove('drop-target'));
    moveBuddy(src, target);
  });
})();
function renderPlan(id){
  const p = planById[id]; if(!p) return;
  let docs = '';
  (p.docs || []).forEach(d => { docs += artRow(ICON_LINK, d.label, 'Related document', d.url); });
  if (!docs) docs = '<p class="bp-empty">No BRD or plan doc yet.</p>';
  const rel = (p.buddies || []).map(bid => byId[bid]).filter(Boolean);
  let buds = '';
  if (!rel.length) buds = '<p class="bp-empty">No buddy linked yet.</p>';
  else buds = rel.map(b => '<a class="art-row" href="#" data-buddy="'+b.id+'">'
    + '<span class="art-ic">'+escHtml(b.icon||'')+'</span>'
    + '<span><span class="art-label">'+escHtml(dispName(b))+'</span><div class="art-sub">'+escHtml(b.tagline||'')+'</div></span>'
    + '<span class="art-go">→</span></a>').join('');
  document.getElementById('buddy-home').innerHTML =
    '<div class="bp-wrap">'
    + '<div class="bp-crumb"><button class="linkbtn" data-view="plans">Business Plans</button> <span style="color:var(--faint)">/</span> <b>'+escHtml(p.name)+'</b></div>'
    + '<div class="bp-sticky-head"><div class="bp-top"><span class="bp-icon">'+escHtml(p.icon||'')+'</span>'
    + '<h2 class="bp-name">'+escHtml(p.name)+'</h2>'
    + '<span class="status '+p.statusClass+'">'+escHtml(p.status)+'</span></div></div>'
    + '<div class="bp-sec"><h3>What it is</h3><p class="bp-mission">'+escHtml(p.desc)+'</p></div>'
    + '<div class="bp-sec"><h3>Documents</h3>'+docs+'</div>'
    + '<div class="bp-sec"><h3>Related buddies</h3>'+buds+'</div>'
    + '<div class="bp-sec"><h3>Notes<span class="info-tip" data-tip="Saved on this device. (For your eyes only)">\\u24d8</span></h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this plan\\u2026 (For your eyes only)">'+escHtml(S.notes[id]||'')+'</textarea>'
    + '<p class="fineprint">Saved on this device. (For your eyes only)</p></div>'
    + '<div class="bp-sec"><h3>Shared notes<span class="info-tip" data-tip="Visible to everyone with access to this project.">\\u24d8</span></h3><textarea class="notes" id="bp-shared" placeholder="Shared notes\\u2026 (visible to everyone with access)">'+escHtml((S.planShared||{})[id]||'')+'</textarea>'
    + '<p class="fineprint">Shared \u2014 visible to everyone with access.</p></div>'
    + '<div class="bp-build">Build __BUILD__</div>'
    + '</div>';
  const nt = document.getElementById('bp-notes');
  let t = null;
  nt.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { S.notes[id] = nt.value; save(); }, 400); });
  const sht = document.getElementById('bp-shared');
  let st2 = null;
  if (sht) sht.addEventListener('input', () => { clearTimeout(st2); st2 = setTimeout(() => { if (!S.planShared) S.planShared = {}; S.planShared[id] = sht.value; save(); }, 400); });
}
const navHist = [];
function locHash(){ try { return (typeof location !== 'undefined' && location.hash) || ''; } catch (e) { return ''; } }
function isStandalone(){ return /(^|\/)standalone$/.test(locHash().replace(/^#\//, '')); }
function hashFor(sel){ return '#/' + sel + (isStandalone() ? '/standalone' : ''); }
document.addEventListener('keydown', e => {
  // Cmd+, (Mac) or Ctrl+, toggles Settings
  if ((e.metaKey || e.ctrlKey) && e.key === ',') {
    e.preventDefault();
    const m = document.getElementById('field-settings');
    if (m && m.classList.contains('show')) {
      m.classList.remove('show');
    } else {
      openFieldSettings();
    }
    return;
  }
  // Escape closes settings or detail panel
  if (e.key === 'Escape') {
    const m = document.getElementById('field-settings');
    if (m && m.classList.contains('show')) {
      m.classList.remove('show');
      e.preventDefault();
      return;
    }
    const vb = document.getElementById('view-buddy');
    if (vb && vb.classList.contains('active')) {
      // Don't close if user is editing text — check both event target and focused element
      const ae = document.activeElement;
      const inField = (e.target && e.target.closest && e.target.closest('input,textarea,select,[contenteditable="true"],[contenteditable=""]'))
        || (ae && ae.closest && ae.closest('input,textarea,select,[contenteditable="true"],[contenteditable=""]'));
      if (inField) {
        // Blur the field instead of closing the panel
        if (ae && ae.blur) ae.blur();
        e.preventDefault();
        return;
      }
      closeDetail();
      e.preventDefault();
      return;
    }
  }
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.target && e.target.closest && e.target.closest('input,textarea,[contenteditable]')) return;
  if (e.key >= '1' && e.key <= '9') {
    const idx = parseInt(e.key, 10) - 1;
    const btns = Array.from(document.querySelectorAll('#sidebar .navbtn[data-view]'));
    const btn = btns[idx];
    if (btn && btn.dataset.view) { show('view:' + btn.dataset.view); e.preventDefault(); }
  }
  // I or Return toggles the right-side detail panel for the selected buddy
  if (e.key === 'i' || e.key === 'I' || e.key === 'Enter') {
    const vb = document.getElementById('view-buddy');
    if (vb && vb.classList.contains('active')) {
      closeDetail();
    } else if (S.projectId && byId[S.projectId]) {
      openBuddy(S.projectId);
    }
    e.preventDefault();
  }
});
function show(sel, push){
  if (push !== false && S.sel && sel !== S.sel) { navHist.push(S.sel); if (navHist.length > 60) navHist.shift(); }
  S.sel = sel;
  if (sel.indexOf('view:') === 0) S.view = sel.slice(5);
  save();
  const h = hashFor(sel);
  try { if (typeof location !== 'undefined' && location.hash !== h) location.hash = h; } catch (e) {}
  document.body.classList.toggle('standalone', isStandalone());
  const vb = document.getElementById('view-buddy');
  const asOverlay = sel.startsWith('buddy:') && !isStandalone();
  if (asOverlay) {
    vb.classList.add('active');
    vb.classList.toggle('panel', window.innerWidth >= 640);
    vb.classList.toggle('sheet', window.innerWidth < 640);
    renderBuddy(sel.slice(6));
  } else {
    // View-menu clicks switch the center view but never dismiss the buddy
    // detail panel: its visibility is controlled only by buddy selection.
    const overlayOpen = vb.classList.contains('panel') || vb.classList.contains('sheet');
    document.getElementById('main').classList.remove('homepage-mode');
    document.querySelectorAll('#main .view').forEach(v => {
      if (v === vb && overlayOpen) return;
      v.classList.remove('active', 'panel', 'sheet');
    });
    if (sel === 'view:project') {
      const pv = document.getElementById('view-project');
      if (pv) { pv.classList.add('active'); renderProjectView(); }
    } else if (sel.startsWith('view:')) {
      const ev = document.getElementById('view-' + sel.slice(5));
      if (ev) ev.classList.add('active');
      if (sel === 'view:changelog') renderChangelog();
    } else if (sel.startsWith('plan:')) {
      closeDetail();
      vb.style.width = '';
      vb.classList.add('active');
      renderPlan(sel.slice(5));
    } else {
      vb.style.width = '';
      vb.classList.add('active');
      renderBuddy(sel.slice(6));
    }
  }
  renderNav();
  document.getElementById('main').scrollTop = 0;
  window.scrollTo(0,0);
  setIcon(sel.startsWith('plan:') ? ((planById[sel.slice(5)] || {}).icon)
    : sel === 'view:project' ? ((byId[projectId()] || {}).icon)
    : sel.startsWith('buddy:') ? ((byId[sel.slice(6)] || {}).icon) : byId['project-buddy'].icon);
}
/* ---------- keyboard nav ---------- */
document.addEventListener('keydown', e => {
  if (e.target && e.target.id === 'buddy-search' && (e.key === 'ArrowDown' || e.key === 'Tab')) {
    const first = document.querySelector('#buddy-nav [data-buddy]');
    if (first) {
      e.preventDefault(); e.target.blur();
      const bid = first.dataset.buddy;
      const wantPanel = S.autoOpenPanel || S.view !== 'project';
      if (wantPanel) openBuddy(bid);
      else selectBuddy(bid);
    }
    return;
  }
  if (e.target && e.target.matches && e.target.matches('input, textarea, [contenteditable="true"]')) return;
  if (e.key === 'Escape') { closeDetail(); return; }
  if (e.key === '/' && !e.target.matches('input, textarea, [contenteditable="true"]')) { e.preventDefault(); const bs = document.getElementById('buddy-search'); if (bs) bs.focus(); return; }
  if (e.key === '+' || e.key === '=') { S.zoom = Math.min(160, (S.zoom || 100) + 5); save(); applyZoom(); return; }
  if (e.key === '-' || e.key === '_') { S.zoom = Math.max(50, (S.zoom || 100) - 5); save(); applyZoom(); return; }
  if (e.key === '0') { zoomToFit(); return; }
  if (/^[1-9]$/.test(e.key)) {
    const vbtns = Array.from(document.querySelectorAll('#view-nav .navbtn[data-view]'));
    const vi = parseInt(e.key, 10) - 1;
    if (vi < vbtns.length) { e.preventDefault(); show('view:' + vbtns[vi].dataset.view); }
    return;
  }
  if (!['ArrowDown','ArrowUp','ArrowLeft','ArrowRight'].includes(e.key)) return;
  const rows = Array.from(document.querySelectorAll('#buddy-nav [data-buddy]'));
  const total = rows.length;
  if (!total) return;
  e.preventDefault();
  let pos = -1;
  const pid = S.projectId || '';
  if (pid) pos = rows.findIndex(r => r.dataset.buddy === pid);
  if (e.key === 'ArrowDown') pos = (pos + 1 + total) % total;
  else if (e.key === 'ArrowUp') pos = (pos - 1 + total) % total;
  else if (e.key === 'ArrowLeft') pos = 0;
  else if (e.key === 'ArrowRight') pos = total - 1;
  if (pos >= 0 && pos < rows.length) {
    const bid = rows[pos].dataset.buddy;
    const wantPanel = S.autoOpenPanel || S.view !== 'project';
    if (wantPanel) openBuddy(bid);
    else selectBuddy(bid);
  }
});
/* ---------- sidebar resize ---------- */
(function initSbResize(){
  const sb = document.getElementById('sidebar');
  applySbWidth();
  const h = document.getElementById('sb-resize');
  let sx = null, sw = 0;
  h.addEventListener('pointerdown', e => { sx = e.clientX; sw = sb.getBoundingClientRect().width; h.setPointerCapture(e.pointerId); e.preventDefault(); });
  h.addEventListener('pointermove', e => {
    if (sx === null) return;
    const w = sbClampW(sw + e.clientX - sx);
    sb.style.width = w + 'px'; sb.style.flex = '0 0 ' + w + 'px';
    document.documentElement.style.setProperty('--sbw', w + 'px');
  });
  const done = () => {
    if (sx === null) return; sx = null;
    S.sbWidth = Math.round(sb.getBoundingClientRect().width); save();
    applySbWidth();
  };
  h.addEventListener('pointerup', done);
  h.addEventListener('pointercancel', done);
  h.addEventListener('dblclick', () => {
    S.sbWidth = SB_DEFAULT_W; save(); applySbWidth();
  });
  window.addEventListener('resize', () => applySbWidth()); /* re-clamp drawer on rotate/resize */
})();
/* ---------- prev/next/back ---------- */
function goBack(){ const p = navHist.pop(); show(p || 'view:tree', false); }
function stepBuddy(d){
  const ids = BUDDIES.map(b => b.id);
  let i = S.sel.startsWith('buddy:') ? ids.indexOf(S.sel.slice(6)) : (d > 0 ? -1 : 0);
  i = (i + d + ids.length) % ids.length;
  show('buddy:' + ids[i]);
}
/* ---------- change journal ---------- */
if (!Array.isArray(S.journal)) S.journal = [];
function logChange(type, buddyId, desc, before, after){
  S.journal.push({t: Date.now(), type, buddy: buddyId, desc, before: before == null ? null : before, after: after == null ? null : after});
  save(); renderJournal();
}
function renderJournal(){
  const bar = document.getElementById('journal-bar'); if (!bar) return;
  if (!Array.isArray(S.journal)) S.journal = [];
  const unseen = S.journal.filter(c => !c.seen);
  if (!unseen.length) { bar.classList.remove('show'); bar.innerHTML = ''; return; }
  const n = S.journal.length;
  const items = unseen.map(c => '<li>' + escHtml(c.desc) + changeOldNew(c)
    + '<span class="jtime">' + escHtml(new Date(c.t).toLocaleString()) + '</span></li>').join('');
  bar.innerHTML = '<button class="linkbtn" id="j-revert">Revert (' + n + ')</button>'
    + '<button class="linkbtn" id="j-toggle">What changed?</button>'
    + '<ul>' + items + '</ul>'
    + '<button class="linkbtn" id="j-dismiss" style="margin-left:auto">Dismiss</button>';
  bar.classList.add('show');
  document.getElementById('j-toggle').addEventListener('click', () => {
    const isOpen = bar.classList.toggle('open');
    if (isOpen) markJournalSeen();
    else renderJournal();
  });
  document.getElementById('j-dismiss').addEventListener('click', () => { markJournalSeen(); renderJournal(); });
  document.getElementById('j-revert').addEventListener('click', () => { revertJournal(); });
}
function markJournalSeen(){ (S.journal || []).forEach(c => { c.seen = true; }); save(); }
function applyBrand(){
  const bn = document.getElementById('brand-name'); const name = S.appName || 'Buddies';
  if (bn && document.activeElement !== bn) bn.textContent = name;
  document.title = name;
}
function revertJournal(){
  const js = S.journal.slice().reverse(), n = js.length;
  js.forEach(c => {
    if (c.type === 'rename') { if (c.before == null) delete S.names[c.buddy]; else S.names[c.buddy] = c.before; }
    else if (c.type === 'brand') { if (c.before == null) delete S.appName; else S.appName = c.before; applyBrand(); }
    else if (c.type === 'notes') { S.notes[c.buddy] = c.before || ''; }
    else if (c.type === 'move') { const reg = (byId[c.buddy] || {}).parent; if (c.before === reg) delete S.parents[c.buddy]; else S.parents[c.buddy] = c.before; }
  });
  S.journal = []; save(); buildKids(); renderNav(); refreshViews();
  if (S.sel.startsWith('buddy:')) renderBuddy(S.sel.slice(6));
  renderJournal();
  toast('Reverted ' + n + ' change' + (n === 1 ? '' : 's') + '.');
}
function buddyStandaloneUrl(id){
  return 'https://davedellaquila.github.io/buddy-system/#/buddy:' + id + '/standalone';
}
function saveToDesktop(id){
  const b = byId[id]; if (!b) return;
  const url = buddyStandaloneUrl(id);
  const isMac = /mac/i.test(navigator.platform || '') || /mac/i.test(navigator.userAgent || '');
  let filename, content, type;
  if (isMac) {
    filename = b.name + '.webloc';
    content = '<?xml version="1.0" encoding="UTF-8"?>' + String.fromCharCode(10)
      + '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">' + String.fromCharCode(10)
      + '<plist version="1.0"><dict><key>URL</key><string>' + url + '</string></dict></plist>';
    type = 'application/xml';
  } else {
    filename = b.name + '.url';
    content = '[InternetShortcut]' + String.fromCharCode(13,10) + 'URL=' + url + String.fromCharCode(13,10);
    type = 'text/plain';
  }
  const blob = new Blob([content], {type: type});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = filename;
  document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 800);
  toast('Saved ' + filename + ' ' + String.fromCharCode(8212) + ' move it to your desktop.');
}
/* ---------- ingest ---------- */
async function dumpIngest(id, keepText){
  const ta = document.getElementById('bp-ingest'), st = document.getElementById('ingest-status');
  const text = ta.value.trim();
  if (!text) return;
  const b = byId[id];
  const stamp = new Date().toLocaleString();
  const entry = '## ' + stamp + String.fromCharCode(10,10) + text + String.fromCharCode(10,10);
  if (!ghToken() || !b.repo) { if (st) st.innerHTML = 'Add a GitHub token to unlock ingest. <a href="https://github.com/settings/tokens" target="_blank" rel="noopener">Get one here</a>.'; return; }
  if (st) st.textContent = 'Dumping\u2026';
  try {
    const cur = await ghGetFile(b.repo, 'docs/ingest.md') || '# Ingest log \u2014 ' + b.name + String.fromCharCode(10,10);
    await ghPutFile(b.repo, 'docs/ingest.md', b64encode(cur + entry), 'Ingest dump for ' + id);
    // Paint BEFORE clearing the textarea so a UI error can't look like a silent no-op
    prependDumpEntry(id, {stamp: stamp, body: text});
    if (!keepText) ta.value = '';
    if (st) st.textContent = 'Dumped — see Dumps below.';
  } catch (err) { if (st) st.textContent = 'Save failed: ' + (err.message || err); }
}
function dumpKey(e){ return (e.stamp || '') + '\0' + (e.body || ''); }
function revealIngestSection(id){
  if (S.fieldHidden && S.fieldHidden.ingest) {
    S.fieldHidden.ingest = false;
    applyFieldOrder();
  }
  const sec = document.querySelector('#buddy-home .bp-sec[data-field="ingest"]');
  if (!sec) return;
  sec.style.display = '';
  sec.classList.remove('collapsed');
  if (!S.secCollapsed || typeof S.secCollapsed !== 'object') S.secCollapsed = {};
  if (!S.secCollapsed[id] || typeof S.secCollapsed[id] !== 'object') S.secCollapsed[id] = {};
  S.secCollapsed[id].ingest = false;
}
function paintIngestFeed(id, entries){
  const feed = document.getElementById('ingest-feed'); if (!feed) return;
  feed._entries = entries.slice();
  if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
  // Default expanded so new dumps are visible without an extra click
  const dCollapsed = S.dumpsCollapsed[id] === true;
  const body = entries.length
    ? ('<div style="height:8px"></div>' + entries.map(function(e, i){
        return '<div class="attn"><div class="dump-actions"><button class="dump-act" data-dump-edit="' + i + '" title="Edit this dump">' + ICON_EDIT + '</button><button class="dump-act" data-dump-del="' + i + '" title="Delete this dump">' + ICON_TRASH + '</button></div><div class="attn-body"><div class="attn-text">' + linkify(escHtml(e.body.slice(0, 300))) + (e.body.length > 300 ? '\u2026' : '') + '</div><div class="attn-date">' + escHtml(e.stamp) + '</div></div></div>';
      }).join(''))
    : '<p class="fineprint" style="margin:10px 0 4px">No dumps yet — type above and press Enter (or wait 2s) to save one here.</p>';
  // Always show the Dumps chrome so the section is never "missing"
  feed.innerHTML = '<div class="dumps' + (dCollapsed ? ' collapsed' : '') + '">'
    + '<div class="dumps-head" id="dumps-toggle"><span class="darrow">\u203a</span><h4>Dumps (' + entries.length + ')</h4></div>'
    + '<div class="dumps-body">' + body + '</div></div>';
  var dt = document.getElementById('dumps-toggle');
  if (dt) dt.addEventListener('click', function(){
    var d = feed.querySelector('.dumps');
    d.classList.toggle('collapsed');
    if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
    S.dumpsCollapsed[id] = d.classList.contains('collapsed');
    save();
  });
  wireDumpButtons(feed, id);
}
function prependDumpEntry(id, e){
  const feed = document.getElementById('ingest-feed'); if (!feed) return;
  if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
  S.dumpsCollapsed[id] = false;
  revealIngestSection(id);
  const entries = (feed._entries || []).slice();
  // Avoid duplicate optimistic rows if a refresh already included this dump
  if (!entries.some(function(x){ return dumpKey(x) === dumpKey(e); })) entries.unshift(e);
  feed._gen = (feed._gen || 0) + 1; // invalidate in-flight GitHub fetches
  try {
    paintIngestFeed(id, entries);
  } catch (err) {
    // Last-resort visible fallback so a paint bug never hides a successful dump
    feed.innerHTML = '<div class="dumps"><div class="dumps-head"><h4>Dumps (' + entries.length + ')</h4></div>'
      + '<div class="dumps-body"><div class="attn"><div class="attn-body"><div class="attn-text">'
      + escHtml((e && e.body) || '') + '</div><div class="attn-date">' + escHtml((e && e.stamp) || '')
      + '</div></div></div></div></div>';
    feed._entries = entries;
  }
  save();
  const first = feed.querySelector('.dumps-body .attn');
  if (first && first.scrollIntoView) first.scrollIntoView({block: 'nearest', behavior: 'smooth'});
}
function parseIngest(md){
  return md.split(/^## /m).slice(1).map(p => {
    const nl = p.indexOf(String.fromCharCode(10));
    return {stamp: p.slice(0, nl).trim(), body: p.slice(nl).trim()};
  }).reverse();
}
async function renderIngestFeed(id){
  const feed = document.getElementById('ingest-feed'); if (!feed) return;
  const b = byId[id];
  const gen = (feed._gen = (feed._gen || 0) + 1);
  const prior = (feed._entries || []).slice();
  let entries = [];
  if (ghToken() && b.repo) {
    const md = await ghGetFile(b.repo, 'docs/ingest.md');
    if (feed._gen !== gen) return; // newer paint won the race
    if (md) entries = parseIngest(md);
  } else {
    try { entries = (JSON.parse(localStorage.getItem('ingest:' + id) || '[]')).map(e => ({stamp: new Date(e.t).toLocaleString(), body: e.text})).reverse(); } catch (e) {}
  }
  if (feed._gen !== gen) return;
  // Keep optimistic dumps that GitHub has not returned yet (API lag after push)
  if (prior.length) {
    const seen = {};
    entries.forEach(function(e){ seen[dumpKey(e)] = true; });
    const extras = prior.filter(function(e){ return !seen[dumpKey(e)]; });
    if (extras.length) entries = extras.concat(entries);
  }
  paintIngestFeed(id, entries);
}
function wireDumpButtons(feed, id){
  feed.querySelectorAll('[data-dump-del]').forEach(function(btn){
    // Avoid double-wiring
    if (btn.dataset.wired) return; btn.dataset.wired = '1';
    btn.addEventListener('click', function(ev){
      ev.stopPropagation();
      if (!confirm('Delete this dump?')) return;
      deleteDump(id, parseInt(btn.getAttribute('data-dump-del'), 10));
    });
  });
  feed.querySelectorAll('[data-dump-edit]').forEach(function(btn){
    if (btn.dataset.wired) return; btn.dataset.wired = '1';
    btn.addEventListener('click', function(ev){
      ev.stopPropagation();
      editDump(id, parseInt(btn.getAttribute('data-dump-edit'), 10), btn);
    });
  });
}

async function deleteDump(id, idx){
  const b = byId[id];
  try {
    if (ghToken() && b.repo) {
      const md = await ghGetFile(b.repo, 'docs/ingest.md');
      if (!md) throw new Error('No ingest file.');
      const parts = md.split(/^## /m);
      const head = parts[0];
      const secs = parts.slice(1);
      const target = secs.length - 1 - idx;
      if (target < 0 || target >= secs.length) throw new Error('Dump not found.');
      secs.splice(target, 1);
      await ghPutFile(b.repo, 'docs/ingest.md', b64encode(head + secs.map(function(s){ return '## ' + s; }).join('')), 'Delete ingest dump for ' + id);
    } else {
      const key = 'ingest:' + id;
      let arr = [];
      try { arr = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
      const target = arr.length - 1 - idx;
      if (target < 0 || target >= arr.length) throw new Error('Dump not found.');
      arr.splice(target, 1);
      localStorage.setItem(key, JSON.stringify(arr));
    }
    toast('Dump deleted.');
  } catch (err) { toast('Delete failed: ' + (err.message || err)); return; }
  renderIngestFeed(id);
}

async function saveDumpBody(id, idx, newBody){
  const b = byId[id];
  if (ghToken() && b.repo) {
    const md = await ghGetFile(b.repo, 'docs/ingest.md');
    if (!md) throw new Error('No ingest file.');
    const parts = md.split(/^## /m);
    const head = parts[0];
    const secs = parts.slice(1);
    const target = secs.length - 1 - idx;
    if (target < 0 || target >= secs.length) throw new Error('Dump not found.');
    const s = secs[target];
    var LF = String.fromCharCode(10);
    const nl = s.indexOf(LF);
    const stamp = (nl >= 0 ? s.slice(0, nl) : s).trim();
    secs[target] = stamp + LF + LF + newBody + LF + LF;
    await ghPutFile(b.repo, 'docs/ingest.md', b64encode(head + secs.map(function(x){ return '## ' + x; }).join('')), 'Edit ingest dump for ' + id);
  } else {
    const key = 'ingest:' + id;
    let arr = [];
    try { arr = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
    const target = arr.length - 1 - idx;
    if (target < 0 || target >= arr.length) throw new Error('Dump not found.');
    arr[target].text = newBody;
    localStorage.setItem(key, JSON.stringify(arr));
  }
}

function editDump(id, idx, btn){
  const feed = document.getElementById('ingest-feed');
  const entries = (feed && feed._entries) || [];
  const e = entries[idx];
  if (!e) return;
  const tile = btn.closest('.attn');
  if (!tile) return;
  const textDiv = tile.querySelector('.attn-text');
  const acts = tile.querySelector('.dump-actions');
  if (acts) acts.style.display = 'none';
  textDiv.innerHTML = '<textarea class="notes" style="min-height:90px">' + escHtml(e.body) + '</textarea>'
    + '<div class="fineprint" data-dump-status style="margin-top:4px;min-height:16px"></div>';
  const ta = textDiv.querySelector('textarea');
  const st = textDiv.querySelector('[data-dump-status]');
  ta.focus();
  ta.selectionStart = ta.selectionEnd = ta.value.length;
  let t = null;
  ta.addEventListener('input', function(){
    clearTimeout(t);
    if (st) st.textContent = 'Saving…';
    t = setTimeout(function(){
      const v = ta.value.trim();
      if (!v) { if (st) st.textContent = 'Dump text is empty — kept the last saved version.'; return; }
      saveDumpBody(id, idx, v).then(function(){
        entries[idx].body = v;
        if (st) st.textContent = 'Saved ✓';
      }).catch(function(err){
        if (st) st.textContent = 'Save failed: ' + (err.message || err);
      });
    }, 900);
  });
  ta.addEventListener('keydown', function(ev){
    if (ev.key === 'Escape') { ev.stopPropagation(); renderIngestFeed(id); }
  });
}
/* ---------- GitHub repo write-back (photos + shared notes) ---------- */
function ghToken(){ return S.ghToken || ''; }
async function ghApi(path, method, body){
  const t = ghToken(); if (!t) throw new Error('Add a GitHub token first.');
  const r = await fetch('https://api.github.com' + path, {
    method: method || 'GET',
    headers: {'Authorization': 'Bearer ' + t, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'},
    body: body ? JSON.stringify(body) : undefined
  });
  if (!r.ok) throw new Error('GitHub ' + r.status);
  return r.status === 204 ? null : await r.json();
}
async function ghPutFile(repo, path, b64, msg){
  let sha;
  try { const ex = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path); sha = ex.sha; } catch (e) {}
  const body = {message: msg, content: b64}; if (sha) body.sha = sha;
  await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path, 'PUT', body);
}
async function ghDeleteFile(repo, path, msg){
  const t = ghToken(); if (!t) throw new Error('Add a GitHub token first.');
  // Get SHA first
  const r = await fetch('https://api.github.com/repos/davedellaquila/' + repo + '/contents/' + path, {
    headers: {Authorization: 'token ' + t, Accept: 'application/vnd.github.v3+json'}
  });
  if (!r.ok) throw new Error('File not found');
  const j = await r.json();
  const d = await fetch('https://api.github.com/repos/davedellaquila/' + repo + '/contents/' + path, {
    method: 'DELETE',
    headers: {Authorization: 'token ' + t, Accept: 'application/vnd.github.v3+json', 'Content-Type': 'application/json'},
    body: JSON.stringify({message: msg || 'Delete ' + path, sha: j.sha})
  });
  if (!d.ok) throw new Error('Delete failed: ' + d.status);
}
async function ghGetFile(repo, path){
  try {
    const j = await ghApi('/repos/davedellaquila/' + repo + '/contents/' + path);
    if (j && j.content) return new TextDecoder().decode(Uint8Array.from(atob(j.content.replace(/\\n/g, '')), c => c.charCodeAt(0)));
  } catch (e) {}
  return null;
}
function b64encode(str){ const bytes = new TextEncoder().encode(str); let bin = ''; bytes.forEach(b => { bin += String.fromCharCode(b); }); return btoa(bin); }
function blobToB64(blob){ return new Promise((res, rej) => { const fr = new FileReader(); fr.onload = () => res(String(fr.result).split(',')[1]); fr.onerror = rej; fr.readAsDataURL(blob); }); }
function loadHeicLib(){
  return new Promise((res, rej) => {
    if (window.heic2any) return res();
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js';
    s.onload = res; s.onerror = () => rej(new Error('HEIC converter failed to load'));
    document.head.appendChild(s);
  });
}
/* ---------- photos ---------- */
async function loadPhotos(id){
  const strip = document.getElementById('pstrip'); if (!strip) return;
  const b = byId[id];
  const seeds = (b.photos || []).map(u => ({src: u, href: u}));
  let repo = [];
  const headers = {};
  if (ghToken()) headers['Authorization'] = 'token ' + ghToken();
  const reposToCheck = [];
  if (b.repo) reposToCheck.push({repo: b.repo, path: 'photos'});
  reposToCheck.push({repo: 'buddy-system', path: 'photos/' + id});
  for (const rc of reposToCheck) {
    try {
      const r = await fetch('https://api.github.com/repos/davedellaquila/' + rc.repo + '/contents/' + rc.path, {headers});
      if (r.ok) {
        const j = await r.json();
        const files = (Array.isArray(j) ? j : []).filter(f => f.type === 'file')
          .map(f => ({src: f.download_url, href: f.download_url, path: f.path, repo: rc.repo}));
        for (const f of files) { if (!repo.some(x => x.src === f.src)) repo.push(f); }
      }
    } catch (e) {}
  }
  const all = seeds.concat(repo.filter(x => !seeds.some(s => s.src === x.src)));
  const ph3 = document.getElementById('photos-h3');
  if (ph3) ph3.textContent = 'Photos (' + all.length + ')';
  strip.innerHTML = all.map(p => {
    const del = p.path ? '<button class="pdel" data-del="' + escHtml(p.path) + '" data-repo="' + escHtml(p.repo || 'buddy-system') + '" title="Delete photo">' + ICON_TRASH + '</button>' : '';
    return '<div class="pwrap"><a href="' + escHtml(p.href) + '" target="_blank" rel="noopener"><img src="' + escHtml(p.src) + '" loading="lazy" alt=""></a>' + del + '</div>';
  }).join('');
  const st = document.getElementById('pstat');
  if (st) st.textContent = all.length
    ? all.length + ' photo' + (all.length === 1 ? '' : 's') + ' \u2014 stored in the buddy-system repo under photos/' + id + '/'
    : 'No photos yet \u2014 drop some below. They land in the buddy-system repo under photos/' + id + '/';
}
async function handlePhotoFiles(id, files){
  const st = document.getElementById('pstat');
  const strip = document.getElementById('pstrip');
  const dropz = document.getElementById('pdrop');
  const list = Array.from(files || []).filter(f => /^image\//.test(f.type) || /\.hei[cf]$/i.test(f.name));
  if (!list.length) { toast('No image files in that drop.'); return; }
  if (!ghToken()) { toast('Add your GitHub token first — click the token pill (top right).'); document.getElementById('token-pop').classList.add('show'); return; }
  let progTile = null, progBar = null, progLabel = null;
  if (strip) {
    progTile = document.createElement('div');
    progTile.className = 'pupload';
    progTile.innerHTML = '<div class="pbar"><div style="width:0%"></div></div><div class="plabel">Uploading</div>';
    strip.appendChild(progTile);
    progBar = progTile.querySelector('.pbar > div');
    progLabel = progTile.querySelector('.plabel');
  }
  const updateProg = function(done, total) {
    const pct = total ? Math.round(done / total * 100) : 0;
    if (progBar) progBar.style.width = pct + '%';
    if (progLabel) progLabel.textContent = done + '/' + total;
    if (st) st.textContent = 'Uploaded ' + done + '/' + total + '...';
    if (dropz) dropz.style.background = 'linear-gradient(to right, rgba(26,127,55,.45) ' + pct + '%, transparent ' + pct + '%)';
  };
  updateProg(0, list.length);
  let n = 0;
  for (const f of list) {
    try {
      let blob = f, ext = (f.name.split('.').pop() || 'jpg').toLowerCase();
      if (/\.hei[cf]$/i.test(f.name) || f.type === 'image/heic' || f.type === 'image/heif') {
        if (st) st.textContent = 'Converting HEIC\u2026';
        await loadHeicLib();
        blob = await window.heic2any({blob: f, toType: 'image/jpeg', quality: 0.92});
        ext = 'jpg';
      }
      if (!/^(jpg|jpeg|png|gif|webp)$/.test(ext)) ext = 'jpg';
      const b64 = await blobToB64(blob);
      const safe = (f.name.replace(/\.[^.]+$/, '').replace(/[^\w\-]+/g, '_').slice(0, 40) || 'photo');
      const upRepo = (byId[id] && byId[id].repo) ? byId[id].repo : 'buddy-system';
      const upPath = (byId[id] && byId[id].repo) ? 'photos/' + Date.now() + '-' + safe + '.' + ext : 'photos/' + id + '/' + Date.now() + '-' + safe + '.' + ext;
      await ghPutFile(upRepo, upPath, b64, 'Add photo for ' + id);
      n++;
      updateProg(n, list.length);
    } catch (err) { toast('Photo failed: ' + (err.message || err)); }
  }
  if (progTile) progTile.remove();
  const dz = document.getElementById('pdrop'); if (dz) dz.style.background = '';
  if (st) st.textContent = 'Uploaded ' + n + ' photo' + (n === 1 ? '' : 's') + '. Refreshing\u2026';
  setTimeout(() => loadPhotos(id), 2000);
}
function renderTokenRow(id){
  const st = document.getElementById('pstat'); if (!st || document.getElementById('ghtok')) return;
  const d = document.createElement('div'); d.className = 'ghtoken';
  d.innerHTML = '<input type="password" id="ghtok" placeholder="GitHub token (repo scope) \u2014 stored on this device only" aria-label="GitHub token">'
    + '<div style="margin-top:8px;display:flex;gap:8px"><button class="linkbtn" id="ghtok-save">Save token</button>'
    + '<a href="https://github.com/settings/tokens" target="_blank" rel="noopener" class="linkbtn" style="text-decoration:none" title="Open GitHub token settings in a new tab">Get a token</a></div>';
  st.after(d);
  document.getElementById('ghtok-save').addEventListener('click', () => {
    const v = document.getElementById('ghtok').value.trim();
    if (v) { S.ghToken = v; save(); d.remove(); toast('Token saved on this device.'); loadSharedNotes(id); }
  });
}
function initPhotoDrop(id){
  const z = document.getElementById('pdrop'); if (!z) return;
  ['dragenter', 'dragover'].forEach(ev => z.addEventListener(ev, e => { e.preventDefault(); z.classList.add('over'); }));
  ['dragleave', 'drop'].forEach(ev => z.addEventListener(ev, e => { e.preventDefault(); z.classList.remove('over'); }));
  z.addEventListener('drop', e => handlePhotoFiles(id, e.dataTransfer.files));
  z.addEventListener('click', () => {
    const inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'image/*,.heic,.heif'; inp.multiple = true;
    inp.addEventListener('change', () => handlePhotoFiles(id, inp.files));
    inp.click();
  });
  if (!ghToken()) { const tp = document.getElementById('token-pop'); if (tp) tp.classList.add('show'); }
}
/* ---------- shared notes ---------- */
function updateTokenPill(){
  const has = !!ghToken();
  const pill = document.getElementById('token-pill');
  if (!pill) return;
  pill.className = has ? 'ok' : 'need';
  document.getElementById('token-pill-icon').textContent = has ? '\u2713' : '\U0001f511';
  document.getElementById('token-pill-text').textContent = has ? 'GitHub' : 'Token needed';
}
function initTokenPill(){
  const pill = document.getElementById('token-pill'), pop = document.getElementById('token-pop');
  if (!pill || !pop) return;
  pill.addEventListener('click', e => { e.stopPropagation(); pop.classList.toggle('show'); });
  document.addEventListener('click', e => { if (!e.target.closest('#token-pop') && !e.target.closest('#token-pill')) pop.classList.remove('show'); });
  document.getElementById('ghtok-global-save').addEventListener('click', () => {
    const v = document.getElementById('ghtok-global').value.trim();
    if (!v) return;
    S.ghToken = v; save();
    const mm = S.sel.match(/^buddy:(.+)$/); refreshTokenUI(mm ? mm[1] : null);
    const chk = document.getElementById('token-saved-check'); chk.classList.add('show');
    setTimeout(() => { chk.classList.remove('show'); pop.classList.remove('show'); }, 1800);
    toast('\u2713 Token saved on this device.');
  });
  document.getElementById('ghtok-global-clear').addEventListener('click', () => {
    S.ghToken = ''; save();
    const m3 = S.sel.match(/^buddy:(.+)$/); refreshTokenUI(m3 ? m3[1] : null);
    document.getElementById('ghtok-global').value = '';
    toast('Token removed.');
  });
  updateTokenPill();
}
function centerOnBuddy(id){
  const tz = document.getElementById('treezoom');
  const node = tz ? tz.querySelector('.node[data-buddy="' + id + '"]') : null;
  if (!tz || !node) return;
  const nr = node.getBoundingClientRect(), tr = tz.getBoundingClientRect();
  tz.scrollLeft += (nr.left + nr.width / 2) - (tr.left + tr.width / 2);
  tz.scrollTop += (nr.top + nr.height / 2) - (tr.top + tr.height / 2);
}
function firstSearchMatch(){
  const q = (document.getElementById('buddy-search').value || '').toLowerCase().trim();
  const words = q.split(/\s+/).filter(Boolean);
  if (!words.length) return null;
  for (const b of BUDDIES) {
    const hay = (dispName(b) + ' ' + (b.name || '') + ' ' + (b.tagline || '')).toLowerCase();
    if (words.every(w => hay.includes(w))) return b.id;
  }
  return null;
}
const AVATAR_CHOICES = ['\U0001f4cb','\U0001f3e0','\U0001f4bc','\U0001f680','\U0001f4a1','\U0001f3af','\U0001f3ae','\U0001f3b5','\U0001f4f7','\U0001f697','\U0001f3e1','\U0001f9f3','\U0001f4dA','\U0001f4dd','\U0001f6e0','\U0001f9ed','\U0001f464','\U0001f465','\U0001f43e','\U0001f431','\U0001f33a','\U00002600','\U0001f319','\U0001f4ab'];
function openAvatarPicker(bid, anchorEl){
  let pk = document.getElementById('avatar-picker');
  if (!pk) {
    pk = document.createElement('div'); pk.id = 'avatar-picker';
    pk.innerHTML = '<h4>Choose avatar</h4><div id="avatar-grid"></div>'
      + '<input id="avatar-custom" placeholder="Or paste any emoji" maxlength="8">';
    document.body.appendChild(pk);
  }
  const grid = document.getElementById('avatar-grid');
  grid.innerHTML = AVATAR_CHOICES.map(e => '<button data-emoji="' + e + '">' + e + '</button>').join('');
  grid.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => { setBuddyIcon(bid, btn.dataset.emoji); pk.classList.remove('show'); });
  });
  const inp = document.getElementById('avatar-custom');
  inp.value = '';
  inp.onchange = () => { const v = inp.value.trim(); if (v) { setBuddyIcon(bid, v); pk.classList.remove('show'); } };
  const r = anchorEl.getBoundingClientRect();
  pk.style.left = Math.min(window.innerWidth - 300, r.left) + 'px';
  pk.style.top = (r.bottom + 8) + 'px';
  pk.classList.add('show');
  const close = e => { if (!pk.contains(e.target) && e.target !== anchorEl) { pk.classList.remove('show'); document.removeEventListener('click', close); } };
  setTimeout(() => document.addEventListener('click', close), 10);
}
function setBuddyIcon(bid, emoji){
  const b = byId[bid]; if (!b) return;
  b.icon = emoji;
  // Persist to buddies.json via journal? For now, device-local + mark dirty
  if (!S.iconOverrides) S.iconOverrides = {};
  S.iconOverrides[bid] = emoji; save();
  const el = document.getElementById('bp-icon'); if (el) el.textContent = emoji;
  renderNav(); refreshViews();
  toast('Avatar updated.');
}
function initPlansToggle(){
  const t = document.getElementById('plans-toggle');
  const sec = document.getElementById('plans-sec');
  if (!t || !sec || t.dataset.init) return;
  t.dataset.init = '1';
  if (S.plansCollapsed) sec.classList.add('collapsed');
  t.addEventListener('click', () => {
    sec.classList.toggle('collapsed');
    S.plansCollapsed = sec.classList.contains('collapsed');
    save();
  });
}
/* Keep --sb-brand-h in sync so .sb-search-sticky stacks under the brand chrome. */
function syncSbBrandStickyHeight(){
  const sb = document.getElementById('sidebar');
  const brand = document.querySelector('.sb-brand-sticky');
  if (!sb || !brand) return;
  const h = Math.ceil(brand.getBoundingClientRect().height);
  if (h > 0) sb.style.setProperty('--sb-brand-h', h + 'px');
}
function initSbBrandSticky(){
  syncSbBrandStickyHeight();
  const brand = document.querySelector('.sb-brand-sticky');
  if (brand && typeof ResizeObserver !== 'undefined') {
    new ResizeObserver(() => syncSbBrandStickyHeight()).observe(brand);
  }
  window.addEventListener('resize', syncSbBrandStickyHeight);
}
function initGear(){
  const g = document.getElementById('sb-gear');
  if (g && !g.dataset.init) { g.dataset.init = '1'; g.addEventListener('click', () => openFieldSettings()); }
}
/* Floating control at the bottom of the left sidebar — jump back to brand/search. */
function initSbToTop(){
  const sb = document.getElementById('sidebar');
  const btn = document.getElementById('sb-to-top');
  if (!sb || !btn || btn.dataset.init) return;
  btn.dataset.init = '1';
  const THRESH = 100;
  function sync(){
    const useful = sb.scrollTop > THRESH && isSidebarOpen() && !document.body.classList.contains('standalone');
    btn.classList.toggle('show', !!useful);
  }
  sb.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  btn.addEventListener('click', e => {
    e.preventDefault();
    try { sb.scrollTo({ top: 0, behavior: 'smooth' }); }
    catch (err) { sb.scrollTop = 0; }
  });
  // Re-sync when drawer opens/closes (class toggles don't fire scroll)
  const mo = typeof MutationObserver !== 'undefined'
    ? new MutationObserver(sync) : null;
  if (mo) {
    mo.observe(sb, { attributes: true, attributeFilter: ['class'] });
    mo.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }
  sync();
}
function isDrawerNav(){ return window.matchMedia('(max-width:639px)').matches; }
function isSidebarOpen(){
  const sb = document.getElementById('sidebar');
  if (!sb) return false;
  if (isDrawerNav()) return sb.classList.contains('open');
  return !document.body.classList.contains('sb-closed');
}
function setSidebarOpen(open){
  const sb = document.getElementById('sidebar');
  const sc = document.getElementById('sb-scrim');
  if (!sb) return;
  if (isDrawerNav()) {
    document.body.classList.remove('sb-closed');
    sb.classList.toggle('open', !!open);
    if (sc) sc.classList.toggle('show', !!open);
  } else {
    document.body.classList.toggle('sb-closed', !open);
    sb.classList.remove('open');
    if (sc) sc.classList.remove('show');
  }
}
/* Left-edge swipe opens the mobile drawer (restored — was dropped in a later merge).
   Rightward swipe that begins within EDGE_PX of the left screen edge. */
function initEdgeSwipeOpen(){
  const EDGE_PX = 20;
  const MIN_DX = 56;
  const DOMINATE = 1.25;
  let track = null;
  function touchById(list, id){
    if (!list) return null;
    for (let i = 0; i < list.length; i++) if (list[i].identifier === id) return list[i];
    return null;
  }
  function onStart(e){
    if (!isDrawerNav() || isSidebarOpen()) { track = null; return; }
    if (document.body.classList.contains('standalone')) { track = null; return; }
    const t = e.changedTouches && e.changedTouches[0];
    if (!t || t.clientX > EDGE_PX) { track = null; return; }
    track = { id: t.identifier, x0: t.clientX, y0: t.clientY };
  }
  function onMove(e){
    if (!track) return;
    const t = touchById(e.touches, track.id) || touchById(e.changedTouches, track.id);
    if (!t) return;
    const dx = t.clientX - track.x0, dy = t.clientY - track.y0;
    if (Math.abs(dy) > 28 && Math.abs(dy) > Math.abs(dx)) track = null;
  }
  function onEnd(e){
    if (!track) return;
    const t = touchById(e.changedTouches, track.id);
    const x0 = track.x0, y0 = track.y0;
    track = null;
    if (!t || !isDrawerNav() || isSidebarOpen()) return;
    if (document.body.classList.contains('standalone')) return;
    const dx = t.clientX - x0, dy = t.clientY - y0;
    if (dx >= MIN_DX && Math.abs(dx) > Math.abs(dy) * DOMINATE) setSidebarOpen(true);
  }
  document.addEventListener('touchstart', onStart, { passive: true, capture: true });
  document.addEventListener('touchmove', onMove, { passive: true, capture: true });
  document.addEventListener('touchend', onEnd, { passive: true, capture: true });
  document.addEventListener('touchcancel', () => { track = null; }, { passive: true, capture: true });
}
/* Paired horizontal swipes (dominant over vertical so scroll still works):
   • Detail open  → swipe right on the panel/sheet → open left sidebar
   • Detail closed → swipe left on the middle canvas → openBuddy (same as ⓘ)
   • Detail open  → swipe left is ignored
   Tree canvas (#treezoom) is excluded from swipe-left (keeps free 2D pan); a
   right-edge strip (24px) still allows swipe-left to open detail over the tree. */
function initPanelSwipeGestures(){
  const MIN_DX = 56;
  const DOMINATE = 1.25;
  const RIGHT_EDGE = 24;
  let track = null; // {id,x0,y0,mode:'openLeft'|'openRight'}
  function detailOpen(){
    const vb = document.getElementById('view-buddy');
    return !!(vb && vb.classList.contains('active') && (vb.classList.contains('panel') || vb.classList.contains('sheet')));
  }
  function touchById(list, id){
    if (!list) return null;
    for (let i = 0; i < list.length; i++) if (list[i].identifier === id) return list[i];
    return null;
  }
  function blockedEl(el){
    return !!(el && el.closest && el.closest('input,textarea,select,[contenteditable="true"],#bp-resize,#sb-resize,#panel-open,#menu-btn'));
  }
  function onStart(e){
    track = null;
    if (document.body.classList.contains('standalone')) return;
    const t = e.changedTouches && e.changedTouches[0];
    if (!t) return;
    const el = document.elementFromPoint(t.clientX, t.clientY);
    if (!el || blockedEl(el)) return;
    const vb = document.getElementById('view-buddy');
    const main = document.getElementById('main');
    if (detailOpen()) {
      // Swipe-right on the open detail surface → open left. Swipe-left ignored.
      if (isSidebarOpen()) return;
      if (!vb.contains(el)) return;
      track = { id: t.identifier, x0: t.clientX, y0: t.clientY, mode: 'openLeft' };
      return;
    }
    // Detail closed: swipe-left on middle canvas → open right panel
    if (!main || !main.contains(el)) return;
    if (el.closest && el.closest('#view-buddy')) return;
    const onTree = !!(el.closest && el.closest('#treezoom'));
    const nearRightEdge = t.clientX >= (window.innerWidth - RIGHT_EDGE);
    if (onTree && !nearRightEdge) return; // don't fight tree pan
    track = { id: t.identifier, x0: t.clientX, y0: t.clientY, mode: 'openRight' };
  }
  function onMove(e){
    if (!track) return;
    const t = touchById(e.touches, track.id) || touchById(e.changedTouches, track.id);
    if (!t) return;
    const dx = t.clientX - track.x0, dy = t.clientY - track.y0;
    if (Math.abs(dy) > 28 && Math.abs(dy) > Math.abs(dx)) track = null;
  }
  function onEnd(e){
    if (!track) return;
    const mode = track.mode;
    const t = touchById(e.changedTouches, track.id);
    const x0 = track.x0, y0 = track.y0;
    track = null;
    if (!t || document.body.classList.contains('standalone')) return;
    const dx = t.clientX - x0, dy = t.clientY - y0;
    if (Math.abs(dx) < MIN_DX || Math.abs(dx) <= Math.abs(dy) * DOMINATE) return;
    if (mode === 'openLeft') {
      if (!detailOpen() || isSidebarOpen()) return;
      if (dx > 0) setSidebarOpen(true);
      return;
    }
    if (mode === 'openRight') {
      if (detailOpen()) return; // already open → no-op
      if (dx >= 0) return; // need leftward
      const id = (S.projectId && byId[S.projectId]) ? S.projectId : 'project-buddy';
      openBuddy(id);
    }
  }
  document.addEventListener('touchstart', onStart, { passive: true, capture: true });
  document.addEventListener('touchmove', onMove, { passive: true, capture: true });
  document.addEventListener('touchend', onEnd, { passive: true, capture: true });
  document.addEventListener('touchcancel', () => { track = null; }, { passive: true, capture: true });
}
// Checks for a newer deployed version; shows an update banner if the server
// has a newer build than the one currently loaded (helps Safari web apps
// and other containers without a hard-refresh shortcut).
function initVersionCheck(){
  const myBuild = '__BUILD__';
  async function check(){
    try {
      const r = await fetch('version.txt?_=' + Date.now(), {cache: 'no-store'});
      if (!r.ok) return;
      const serverBuild = (await r.text()).trim();
      // Don't show the banner for 10 min after "Update now" was clicked (gives Pages time to deploy)
      try {
        const clicked = parseInt(sessionStorage.getItem('updateClicked') || '0', 10);
        if (clicked && Date.now() - clicked < 10 * 60 * 1000) return;
      } catch (e) {}
      if (serverBuild && serverBuild !== myBuild && !document.getElementById('update-banner')) {
        const b = document.createElement('div');
        b.id = 'update-banner';
        b.innerHTML = '<span>A newer version of Buddies is available (' + escHtml(serverBuild) + ').</span> '
          + '<button id="update-now" style="margin-left:12px;padding:6px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:#fff;font-weight:600;cursor:pointer">Update now</button>'
          + '<button id="update-dismiss" aria-label="Dismiss" style="margin-left:8px;padding:6px 10px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text);font-size:16px;cursor:pointer;line-height:1">\u00d7</button>';
        b.style.cssText = 'position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:9999;background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:12px 18px;box-shadow:0 8px 32px rgba(0,0,0,.3);display:flex;align-items:center;font-size:14px';
        document.body.appendChild(b);
        document.getElementById('update-now').addEventListener('click', () => {
          b.remove();
          try { sessionStorage.setItem('updateClicked', String(Date.now())); } catch (e) {}
          location.href = location.pathname + '?v=' + Date.now() + location.hash;
        });
        document.getElementById('update-dismiss').addEventListener('click', () => {
          b.remove();
        });
      }
    } catch (e) {}
  }
  check();
  setInterval(check, 5 * 60 * 1000);
}
function initSearch(){
  const bs = document.getElementById('buddy-search');
  if (bs && !bs.dataset.init) {
    bs.dataset.init = '1';
    bs.addEventListener('input', () => {
      renderNav();
      if (S.sel === 'view:tree') { const m = firstSearchMatch(); if (m) centerOnBuddy(m); }
    });
  }
}
function refreshTokenUI(id){
  updateTokenPill();
  updateTokenGating(id);
  if (id && S.sel === 'buddy:' + id) {
    loadSharedNotes(id);
    renderIngestFeed(id);
    const pz = document.getElementById('pstat');
    if (pz && ghToken()) pz.textContent = 'Ready — drop photos to publish to the repo.';
  }
}
function updateTokenGating(id){
  const has = !!ghToken();
  document.body.classList.toggle('no-write', !has);
  const banner = document.getElementById('token-banner');
  if (banner) banner.classList.toggle('show', !has);
  const sn = document.getElementById('bp-shared-notes');
  if (sn) {
    sn.disabled = !has;
    sn.placeholder = has ? 'Shared notes\u2026' : 'Add a GitHub token above to unlock shared notes.';
    const oldW = document.getElementById('shared-token-warn'); if (oldW) oldW.remove();
    if (!has) {
      sn.value = '';
      const w = document.createElement('div');
      w.id = 'shared-token-warn'; w.className = 'tokenwarn';
      w.innerHTML = '⚠️ <b>Shared notes are off — you gotta go get the token, bro.</b><br>Nothing you type here will save until then. <a href="https://github.com/settings/tokens/new" target="_blank" rel="noopener">Get a GitHub token</a> (classic token, <b>repo</b> scope), then paste it above — it never leaves this device.';
      if (sn.parentNode) sn.parentNode.insertBefore(w, sn.nextSibling);
    }
  }
  const ig = document.getElementById('bp-ingest');
  if (ig) { ig.disabled = !has; ig.placeholder = has ? ig.placeholder : 'Add a GitHub token above to unlock ingest.'; }

  const pz = document.getElementById('pdrop');
  if (pz) pz.classList.toggle('locked', !has);
}
async function loadSharedNotes(id){
  const ta = document.getElementById('bp-shared-notes'), st = document.getElementById('shared-status');
  if (!ta) return;
  const b = byId[id];
  if (!ghToken() || !b.repo) { if (st) st.textContent = ghToken() ? 'No repo linked for shared notes.' : 'Locked \u2014 add a GitHub token above.'; return; }
  if (st) st.textContent = 'Loading\u2026';
  const txt = await ghGetFile(b.repo, 'docs/notes.md');
  ta.value = txt || '';
  if (st) st.textContent = txt == null ? 'No shared notes yet.' : 'Synced from ' + b.repo + '/docs/notes.md';
  let t = null;
  ta.addEventListener('input', () => {
    clearTimeout(t);
    if (st) st.textContent = 'Saving\u2026';
    t = setTimeout(async () => {
      try { await ghPutFile(b.repo, 'docs/notes.md', b64encode(ta.value), 'Update shared notes'); if (st) st.textContent = 'Saved to ' + b.repo + '/docs/notes.md'; }
      catch (err) { if (st) st.textContent = 'Save failed: ' + (err.message || err); }
    }, 900);
  });
}
document.addEventListener('click', e => {
  if (nodeDragEndAt && Date.now() - nodeDragEndAt < 400) return; // swallow the click that follows a node-drag gesture
  if (e.target.closest && e.target.closest('#bp-icon')) { const m = S.sel.match(/^buddy:(.+)$/); if (m) openAvatarPicker(m[1], e.target.closest('#bp-icon')); return; }
  if (e.target.closest && (e.target.closest('#bp-close') || e.target.closest('#bp-close-x') || e.target.closest('#bp-takeover-back'))) { closeDetail(); return; }
  if (e.target.closest && e.target.closest('#panel-open')) {
    const id = (S.projectId && byId[S.projectId]) ? S.projectId : 'project-buddy';
    openBuddy(id);
    return;
  }
  if (e.target.closest && e.target.closest('#sb-close')) { setSidebarOpen(false); return; }
  if (e.target.closest && e.target.closest('#menu-btn')) { setSidebarOpen(!isSidebarOpen()); return; }
  if (e.target.closest && e.target.closest('#sb-scrim')) { setSidebarOpen(false); return; }
  if (e.target.closest && e.target.closest('#ghtok2-save')) {
    const v = document.getElementById('ghtok2').value.trim();
    if (!v) return;
    S.ghToken = v; save();
    const m2 = S.sel.match(/^buddy:(.+)$/); refreshTokenUI(m2 ? m2[1] : null);
    toast('Token saved on this device.');
    return;
  }
  if (e.target.closest && e.target.closest('#bp-desktop')) { const m = S.sel.match(/^buddy:(.+)$/); if (m) saveToDesktop(m[1]); return; }
  if (e.target.closest && e.target.closest('#sa-full')) { try { location.hash = '#/' + S.sel; } catch (e) {} document.body.classList.remove('standalone'); return; }
  const pd = e.target.closest('[data-del]');
  if (pd) {
    e.preventDefault(); e.stopPropagation();
    const path = pd.dataset.del;
    const repo = pd.dataset.repo || 'buddy-system';
    const mm = S.sel.match(/^buddy:(.+)$/);
    const bid = mm ? mm[1] : null;
    if (!confirm('Delete this photo?')) return;
    const wrap = pd.closest('.pwrap');
    ghDeleteFile(repo, path, 'Delete photo for ' + (bid || 'buddy'))
      .then(() => {
        toast('Photo deleted.');
        if (wrap) wrap.remove();
      })
      .catch(err => {
        if (/not found/i.test(err.message || '')) {
          toast('Photo deleted.');
          if (wrap) wrap.remove();
        } else {
          toast('Delete failed: ' + (err.message || err));
        }
      });
    return;
  }
  const vb = e.target.closest('[data-view]');
  if (vb) { show('view:' + vb.dataset.view); if (window.innerWidth < 640) { const sbo=document.getElementById('sidebar'); if(sbo) sbo.classList.remove('open'); const sco=document.getElementById('sb-scrim'); if(sco) sco.classList.remove('show'); } return; }
  const pb = e.target.closest('[data-plan]');
  if (pb) { e.preventDefault(); show('plan:' + pb.dataset.plan); return; }
  const sb2 = document.getElementById('sidebar');
  if (sb2) sb2.classList.remove('open');
  const projTile = e.target.closest('#project-tiles [data-tile]');
  if (projTile) {
    projFilter = projFilter === projTile.dataset.tile ? null : projTile.dataset.tile;
    renderProjects(); return;
  }
  const statusTile = e.target.closest('#project-status-tiles [data-tile]');
  if (statusTile) {
    const st = statusTile.dataset.tile.replace(/^status:/, '');
    statusFilter = statusFilter === st ? null : st;
    // Clear the attention filter when using status filter (mutually exclusive)
    if (statusFilter) projFilter = null;
    renderProjects(); return;
  }
  const clTile = e.target.closest('#changelog-tiles [data-tile]');
  if (clTile) {
    clFilter = clFilter === clTile.dataset.tile ? null : clTile.dataset.tile;
    renderChangelog(); return;
  }
  const planTile = e.target.closest('#plans-tiles [data-tile]');
  if (planTile) {
    planFilter = planFilter === planTile.dataset.tile ? null : planTile.dataset.tile;
    applyPlanFilter(); return;
  }
  const manTile = e.target.closest('#manifest-tiles [data-tile]');
  if (manTile) {
    manifestFilter = manifestFilter === manTile.dataset.tile ? null : manTile.dataset.tile;
    applyManifestFilter(); return;
  }
  const buddyInfo = e.target.closest('[data-buddy-info]');
  if (buddyInfo) {
    e.stopPropagation(); e.preventDefault();
    const bid = buddyInfo.dataset.buddyInfo;
    const vb = document.getElementById('view-buddy');
    // Toggle: if panel is open for this buddy, close it; otherwise open it
    if (vb && vb.classList.contains('active') && S.projectId === bid) {
      closeDetail();
    } else {
      openBuddy(bid);
    }
    return;
  }
  const projInfo = e.target.closest('[data-proj-info]');
  if (projInfo) {
    e.stopPropagation();
    const bid = projInfo.dataset.projInfo;
    const vb = document.getElementById('view-buddy');
    // Toggle: if panel is open for this buddy, close it; otherwise open it
    if (vb && vb.classList.contains('active') && S.projectId === bid) {
      closeDetail();
    } else {
      openBuddy(bid);
    }
    return;
  }
  const projRow = e.target.closest('#view-projects .proj-row[data-buddy]');
  if (projRow) {
    // Whole row toggles expand/collapse (if it has children)
    const pt = projRow.querySelector('[data-proj-toggle]');
    if (pt) {
      const bid = pt.dataset.projToggle;
      if (!S.projCollapsed || typeof S.projCollapsed !== 'object') S.projCollapsed = {};
      S.projCollapsed[bid] = !S.projCollapsed[bid];
      save(); renderProjects();
    }
    // View-aware panel behavior: Projects list is not the homepage view, so rows
    // open the panel by default (consistent with sidebar clicks in other views).
    const wantPanel = S.autoOpenPanel || S.view !== 'project';
    if (wantPanel) openBuddy(projRow.dataset.buddy);
    else selectBuddy(projRow.dataset.buddy);
    return;
  }
  const bb = e.target.closest('[data-buddy]');
  // Don't re-open the buddy when clicking an editable field (e.g. the name)
  // Panel behavior is view-aware: in Project Homepage view, clicking selects only
  // (use the ⓘ icon for the panel). In other views, clicking opens the panel.
  // The autoOpenPanel setting overrides to always open.
  if (bb && !e.target.closest('[contenteditable="true"]')) {
    const wantPanel = S.autoOpenPanel || S.view !== 'project';
    if (wantPanel) openBuddy(bb.dataset.buddy);
    else selectBuddy(bb.dataset.buddy);
    // On iPhone, close the drawer after picking a buddy
    if (window.innerWidth < 640) { const sbo=document.getElementById('sidebar'); if(sbo) sbo.classList.remove('open'); const sco=document.getElementById('sb-scrim'); if(sco) sco.classList.remove('show'); }
    return;
  }
  const sb = e.target.closest('[data-seen]');
  if (sb) { S.seen[sb.dataset.seen] = Date.now(); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const sa = e.target.closest('[data-seen-all]');
  if (sa) { (byId[sa.dataset.seenAll].attention || []).forEach(a => S.seen[a.id] = Date.now()); save(); renderBuddy(S.sel.slice(6)); renderNav(); return; }
  const gt = e.target.closest('[data-goto]');
  if (gt) { e.preventDefault(); show('buddy:' + gt.dataset.goto); return; }
  const nb = e.target.closest('[data-navbtn]');
  if (nb) { const k = nb.dataset.navbtn; if (k === 'back') goBack(); else stepBuddy(k === 'next' ? 1 : -1); return; }
  const rp = e.target.closest('#reset-parents');
  if (rp) { S.parents = {}; save(); buildKids(); renderNav(); refreshViews();
    if (S.sel.startsWith('buddy:')) renderBuddy(S.sel.slice(6));
    toast('Hierarchy reset to the registry.'); return; }
});
refreshViews();
(function initRoute(){
  const m = locHash().match(/^#\/(buddy:[^\/]+|view:[^\/]+|plan:[^\/]+)(\/standalone)?$/);
  if (m) { document.body.classList.toggle('standalone', !!m[2]); show(m[1], false); }
  else show(S.sel || 'view:tree');
  window.addEventListener('hashchange', () => {
    const mm = locHash().match(/^#\/(buddy:[^\/]+|view:[^\/]+|plan:[^\/]+)(\/standalone)?$/);
    if (!mm) return;
    document.body.classList.toggle('standalone', !!mm[2]);
    if (mm[1] !== S.sel) show(mm[1], false);
  });
})();
renderJournal();
initTokenPill();
updateTokenGating();
initSearch();
initGear();
initSbToTop();
initEdgeSwipeOpen();
initPanelSwipeGestures();
initVersionCheck();
initPlansToggle();
initSbBrandSticky();
"""
    js = js.replace("BUDDIES_JSON", buddies_js).replace("ORDER_JSON", order_js).replace("PLANS_JSON", plans_js)
    js = js.replace("ICON_DOC", "'" + ICON_DOC.replace("'", "\\'") + "'")
    js = js.replace("ICON_REPO", "'" + ICON_REPO.replace("'", "\\'") + "'")
    js = js.replace("ICON_LINK", "'" + ICON_LINK.replace("'", "\\'") + "'")
    js = js.replace("ICON_TRASH", "'" + ICON_TRASH.replace("'", "\\'") + "'")
    js = js.replace("ICON_EDIT", "'" + ICON_EDIT.replace("'", "\\'") + "'")

    out = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>try{var _t=(JSON.parse(localStorage.getItem('buddyTree.v3')||'{}').theme)||'system';if(_t==='light'||(_t!=='dark'&&window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches))document.documentElement.classList.add('light');}catch(e){}</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="application-name" content="Buddies">
<meta name="apple-mobile-web-app-title" content="Buddies">
<title>Buddies</title>
<style>
""" + style + NEW_CSS + """
</style>
</head>
<body>
<div class="app">
<button id="menu-btn" title="Expand sidebar" aria-label="Expand sidebar"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
<button type="button" id="panel-open" title="Expand buddy details" aria-label="Expand buddy details">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
</button>
<div id="sb-scrim"></div>
<aside id="sidebar">
  <div class="sb-brand-sticky">
    <div id="sb-tools"><button id="sb-gear" title="Settings (⌘,)" aria-label="Settings"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></button><button id="sb-close" title="Collapse sidebar" aria-label="Collapse sidebar"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg></button></div>
    <div class="brand"><div class="eyebrow">Project Buddy &middot; macro view</div><h1 id="brand-name" title="Click to rename">Buddies</h1><div class="bcount">NBUD buddies &middot; one family</div></div>
  </div>
  <div class="nav-sec"><h3>Views</h3><div id="view-nav"></div></div>
  <div class="sb-search-sticky">
    <input type="search" id="buddy-search" placeholder="Search buddies\u2026" aria-label="Search buddies"
      title="Search all buddies by name or tagline. Filters the sidebar list as you type. Press / anywhere to jump here. Arrow keys navigate results.">
  </div>
  <div class="nav-sec">
  <h3>Buddies <span id="attn-pill" class="zero">0</span></h3><div id="buddy-nav"></div></div>
  <div class="nav-sec" id="plans-sec"><h3 style="cursor:pointer" id="plans-toggle"><span id="plans-arrow">\u203a</span> Business Plans</h3><div id="plan-nav"></div></div>
</aside>
<div id="sb-resize" title="Drag left or right to resize the sidebar. Double-click to reset to default width."></div>
<button type="button" id="sb-to-top" title="Scroll sidebar to top" aria-label="Scroll sidebar to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M6 11l6-6 6 6"/></svg>
</button>
<main id="main">
<div id="journal-bar"></div>
""" + vt + vp + vpl + vm + """
<section id="view-buddy" class="view"><div id="bp-resize" title="Drag left or right to resize the buddy detail panel. Double-click to reset to default width."></div><div id="buddy-home"></div></section>
<section id="view-project" class="view"></section>
<section id="view-changelog" class="view"></section>
</main>
</div>
<script>
""" + js + """
</script>
</body>
</html>
"""
    out = out.replace("NBUD", str(n_buddies))
    out = out.replace("__BUILD__", BUILD_NUM)
    open(f"{HERE}/index.html", "w").write(out)
    open(f"{HERE}/version.txt", "w").write(BUILD_NUM)
    print("wrote index.html", len(out), "bytes")


if __name__ == "__main__":
    build()

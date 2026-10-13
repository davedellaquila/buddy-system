#!/usr/bin/env python3
"""Build the Project Buddy dashboard (index.html) from buddies.json + the view fragments.

Usage: build.py   (run from ~/workspace/projects/buddy-tree)
Reads:  buddies.json, buddy-tree.html (style + the three view fragments)
Writes: index.html
"""
import json
import re
from datetime import datetime
BUILD_NUM = datetime.now().strftime('%Y%m%d.%H%M')

HERE = "/home/hatch/workspace/projects/buddy-tree"

ROOT_ORDER = [
    "astro",
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
  --canvas:color-mix(in srgb, var(--bg) 97.5%, black); /* whisper-dark chart canvas (Jonny, 2026-10-11) */
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
  --canvas:color-mix(in srgb, var(--bg) 97%, black); /* whisper-dark chart canvas (Jonny, 2026-10-11) */
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
#sidebar{width:308px;flex:0 0 308px;background:var(--bg);border-right:1px solid var(--border2);container-type:inline-size;
  padding:0 14px 32px;position:sticky;top:0;height:100vh;overflow-y:auto;overflow-x:hidden;overflow-wrap:break-word;
  z-index:40}
#main{flex:1;min-width:0;padding:36px 32px 80px;position:relative;z-index:1}
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
  color:var(--text);border-radius:8px;padding:7px 30px 7px 10px;font-size:13px}
.sb-search-wrap{position:relative;display:flex;align-items:center}
#buddy-search-clear{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:none;background:transparent;color:var(--muted);font-size:18px;line-height:1;cursor:pointer;padding:4px 8px;border-radius:6px}
/* Autocomplete dropdown for buddy search (Dave 2026-10-12) */
#buddy-ac{position:absolute;top:100%;left:0;right:0;z-index:5000;background:var(--panel);border:1px solid var(--border);border-radius:12px;margin-top:6px;box-shadow:0 12px 32px var(--shadow);overflow:hidden;max-height:320px;overflow-y:auto}
#buddy-ac[hidden]{display:none}
.bac-row{display:flex;align-items:center;gap:10px;width:100%;padding:10px 14px;border:none;background:none;color:var(--text);cursor:pointer;text-align:left;font-size:14px}
.bac-row:hover,.bac-row.hot{background:var(--active)}
.bac-row .bicon{font-size:18px;flex-shrink:0}
.bac-row .bname{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bac-row .bctx{font-size:11px;color:var(--muted);margin-left:auto;flex-shrink:0}
.bac-empty{padding:14px;font-size:13px;color:var(--muted);text-align:center}
#buddy-search-clear:hover{color:var(--text);background:rgba(127,127,127,.18)}
.brand .eyebrow{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);white-space:nowrap;padding-right:96px;overflow:hidden;text-overflow:ellipsis}
.brand h1{font-size:22px;margin:4px 0 0}
#brand-name{outline:none;border-bottom:2px dashed transparent;cursor:text;display:inline-block;min-width:60px}
#brand-name:hover{border-bottom-color:var(--border)}
#brand-name:focus{border-bottom-color:var(--accent)}
.brand .bcount{font-size:12.5px;color:var(--muted);margin-top:4px;white-space:nowrap}
.nav-sec{margin-top:18px}
.nav-sec>h3{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);
  margin:0 8px 8px;display:flex;align-items:center;gap:8px}
#attn-pill{background:var(--accent);color:var(--on-accent);font-size:11px;font-weight:700;border-radius:999px;
  padding:1px 8px;letter-spacing:0;text-transform:none}
#attn-pill.zero{background:var(--border2);color:var(--muted)}
.attn-count{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:0;text-transform:none}
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
.bname.pname{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;text-overflow:ellipsis}
.bkind{font-size:10px;color:var(--faint);letter-spacing:.5px;text-transform:uppercase}
.bicon{width:20px;flex:0 0 20px;text-align:center;font-size:15px}
.brow.dragging{opacity:.35}
.brow.drop-target{background:var(--active);box-shadow:inset 0 0 0 2px var(--accent)}
.bp-icon{font-size:38px;line-height:1;position:relative;overflow:hidden;display:inline-flex;align-items:center;justify-content:center}
.bp-avatarimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bp-avaemoji{position:relative}
.toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%);background:var(--panel);
  border:1px solid var(--accent);color:var(--text);padding:10px 20px;border-radius:999px;
  font-size:14px;z-index:99;box-shadow:0 4px 24px var(--shadow);white-space:nowrap;
  max-width:92vw;overflow:hidden;text-overflow:ellipsis}
.treewrap{position:relative;display:flex;gap:10px;align-items:flex-start}
/* Beat .view.active{display:block} so the tree fills the viewport and #treezoom
   alone scrolls in both axes (fixes iOS axis-lock from nested X/Y scrollers). */
#quick-answers{display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--panel);border:1px solid var(--border);border-radius:12px;margin:0 0 16px;overflow:hidden}
.qa-label{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);flex:none}
.qa-links{display:flex;gap:8px;overflow-x:auto;flex:1;padding-bottom:2px;scrollbar-width:thin}
.qa-links::-webkit-scrollbar{height:6px}
.qa-link{display:flex;align-items:center;gap:8px;background:var(--bg);border:1px solid var(--border);border-radius:999px;padding:6px 14px;font-size:13px;color:var(--text);cursor:pointer;max-width:280px}
.qa-link:hover{border-color:var(--accent)}
.qa-icon{font-size:16px}
.qa-text{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.qa-chip{display:flex;align-items:center;gap:0;background:var(--bg);border:1px solid var(--border);border-radius:999px;overflow:hidden}
.qa-chip .qa-link{border:none;background:none;border-radius:0}
.qa-done{flex:none;width:44px;height:44px;border:none;background:none;color:var(--muted);font-size:16px;cursor:pointer;touch-action:manipulation;display:flex;align-items:center;justify-content:center;border-left:1px solid var(--border)}
.qa-done:hover{color:var(--grn-solid)}
.node{position:relative}
.collapse-pill{position:absolute;bottom:8px;right:8px;min-width:44px;height:28px;border-radius:999px;border:1px solid var(--border);background:var(--panel);color:var(--muted);font-size:13px;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:4px;padding:0 10px;z-index:2}
.collapse-pill:hover{border-color:var(--accent);color:var(--accent)}
#view-tree.view.active{display:flex !important;flex-direction:column;
  margin:-36px -32px -80px;height:100vh;height:100dvh;overflow:hidden;min-height:0}
#view-tree #zoomwrap{flex:1;min-height:0;min-width:0;align-items:stretch;display:flex;flex-direction:column}
/* Two stacked panes (buddy tree on top, orphaned buddies below) with a draggable
   splitter; each pane is its own 2D scrollport with its own zoom control. */
#treezoom{flex:1;min-width:0;min-height:0;display:flex;flex-direction:column;overflow:hidden;
  border:1px solid var(--border);border-left:none;border-right:none;border-radius:0;background:var(--canvas)}
.treepane{position:relative;min-height:60px;min-width:0;display:flex;flex-direction:column;flex:1 1 0}
/* UI chrome above the chart scroll pane (Quick answers + Atlas lens picker).
   Sits outside #treezoom-main so the zoom control never scales it. */
.tree-chrome{flex:0 0 auto;min-width:0}
.treescroll{flex:1;min-width:0;min-height:0;overflow:auto;overscroll-behavior:contain;cursor:grab;
  -webkit-overflow-scrolling:touch}
.treescroll.panning{cursor:grabbing}
/* JS pan owns gestures on the tree canvas so touch can move X+Y at once */
.treescroll{touch-action:none}
#view-projects,#view-manifest{touch-action:pan-x pan-y}
.treescroll.panning,.treescroll.panning *{user-select:none!important;-webkit-user-select:none!important}
/* Center the composition when it fits inside the pane (Jony: no dead field below at fit zoom).
   margin:auto on the flex child centers only when there's extra space — overflowing content
   still scrolls normally from the top. */
.treescroll.fit-centered{display:flex}
.treescroll.fit-centered .chart,.treescroll.fit-centered .standalones{margin:auto}
/* ============ Atlas lens picker (Jonny's verdict) ============ */
.lens-picker-wrap{position:relative;display:inline-block;margin:0 0 12px 12px;z-index:60}
.lens-pill{display:flex;align-items:center;gap:8px;min-height:44px;padding:10px 16px;
  background:var(--panel);border:1px solid var(--border);border-radius:999px;
  color:var(--text);font-size:14px;font-weight:600;cursor:pointer;
  box-shadow:0 2px 8px var(--shadow);-webkit-tap-highlight-color:transparent}
.lens-pill:hover{border-color:var(--accent)}
.lens-pill-icon{color:var(--accent)}
.lens-pill-chev{color:var(--muted);font-size:12px}
.lens-dropdown{position:absolute;top:calc(100% + 8px);left:0;z-index:61;
  display:grid;grid-template-columns:repeat(2,minmax(220px,1fr));gap:8px;
  background:var(--panel);border:1px solid var(--border);border-radius:16px;
  padding:12px;box-shadow:0 12px 40px var(--shadow);min-width:480px;
  animation:lensIn .18s ease-out}
@keyframes lensIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.lens-dropdown[hidden]{display:none}
.lens-close{position:absolute;top:8px;right:8px;width:32px;height:32px;border-radius:50%;
  border:1px solid var(--border);background:var(--bg);color:var(--muted);font-size:16px;
  line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;
  -webkit-tap-highlight-color:transparent;z-index:2}
.lens-close:hover{color:var(--text);border-color:var(--accent)}
.lens-card{display:flex;flex-direction:column;align-items:flex-start;gap:4px;
  padding:12px;border:1px solid var(--border);border-radius:12px;background:var(--bg);
  cursor:pointer;text-align:left;min-height:44px;-webkit-tap-highlight-color:transparent}
.lens-card:hover{border-color:var(--accent)}
.lens-card.sel{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.lens-thumb{color:var(--muted);display:block;margin-bottom:2px}
.lens-card.sel .lens-thumb{color:var(--accent)}
.lens-name{font-size:14px;font-weight:700;color:var(--text)}
.lens-blurb{font-size:12px;color:var(--muted);line-height:1.35}
.lens-scrim{position:fixed;inset:0;z-index:59;background:transparent}
/* Phone: bottom sheet */
@media (max-width:639px){
  .lens-dropdown{position:fixed;left:12px;right:12px;bottom:12px;top:auto;min-width:0;
    grid-template-columns:1fr 1fr;border-radius:20px;padding:16px 12px calc(16px + env(safe-area-inset-bottom));
    animation:lensSheetIn .25s cubic-bezier(.32,.72,.35,1)}
  .lens-dropdown::before{content:'';display:block;width:36px;height:4px;border-radius:2px;
    background:var(--border);margin:0 auto 12px;grid-column:1/-1}
  @keyframes lensSheetIn{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
  .lens-scrim{background:rgba(0,0,0,.35)}
}
/* ============ Atlas chart types ============ */
.chart-ledger .ledger{max-width:720px;margin:0 auto;padding:8px 0}
.ledger-row{display:flex;align-items:baseline;gap:10px;padding:7px 12px;border-radius:8px;cursor:pointer}
.ledger-row:hover{background:var(--wash)}
.ledger-name{font-weight:600;font-size:15px;white-space:nowrap}
.ledger-desc{color:var(--muted);font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* Ledger drag grippers — Jonny's quiet 2x3 dot-grid language; the gripper is the drag handle */
.ledger-grip{flex:0 0 auto;width:22px;height:22px;align-self:center;cursor:grab;touch-action:none;opacity:.5;border-radius:6px;
  background-image:radial-gradient(circle,var(--gripdot,color-mix(in srgb,var(--muted) 42%,var(--border))) 1.5px,transparent 1.6px);
  background-size:7px 7px;background-position:center;background-repeat:no-repeat}
.ledger-row:hover .ledger-grip{opacity:.95}
.ledger-grip:active{cursor:grabbing}
.ledger-chev{flex:0 0 auto;width:22px;height:22px;border:0;background:none;color:var(--muted);font-size:16px;cursor:pointer;border-radius:6px;align-self:center;padding:0;line-height:1}
.ledger-chev:hover{background:var(--wash);color:var(--text)}
.ledger-chev i{display:inline-block;transition:transform .15s;font-style:normal;line-height:1}
.ledger-chev:not(.collapsed) i{transform:rotate(90deg)}
.ledger-chev-sp{flex:0 0 auto;width:22px;align-self:center}
.ledger-row.drag-armed{outline:2px solid var(--accent);outline-offset:2px}
.ledger-row.drag-src{opacity:.4}
.ledger-row.drop-target{background:var(--active);box-shadow:inset 0 0 0 2px var(--accent)}
.ledger-row.drop-invalid{box-shadow:inset 0 0 0 2px #e0533d}
.chart-lineage .lineage{overflow-x:auto;padding:16px 8px}
.hgen{display:flex;align-items:center;gap:0}
.hchildren{display:flex;flex-direction:column;gap:12px;margin-left:0;padding-left:28px;position:relative}
.hchildren::before{content:'';position:absolute;left:14px;top:12px;bottom:12px;width:1px;background:var(--border)}
.hgen .node{flex:none}
.chart-colonnade .colonnade{display:flex;overflow-x:auto;min-height:420px;border:1px solid var(--border);border-radius:12px;background:var(--panel)}
.mcol{flex:0 0 240px;border-right:1px solid var(--border);overflow-y:auto;max-height:70vh}
.mcol-head{padding:12px 14px;font-weight:700;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--panel)}
.mcol-row{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;cursor:pointer;border-bottom:1px solid var(--wash)}
.mcol-row:hover{background:var(--wash)}
.mcol-arrow{color:var(--muted)}
.chart-terrain .terrain{display:flex;flex-direction:column;min-height:60vh;border-radius:12px;overflow:hidden;border:1px solid var(--border)}
.tm-tile{display:flex;flex-direction:column;min-width:0;min-height:0;border:1px solid var(--border);background:var(--panel);overflow:hidden}
.tm-branch{padding:0}
.tm-label{padding:8px 10px;font-weight:700;font-size:13px;background:var(--wash);cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tm-kids{display:flex;flex-direction:column;flex:1;min-height:0}
.tm-leaf{align-items:center;justify-content:center;cursor:pointer;padding:8px}
.tm-leaf:hover{background:var(--wash)}
.tm-name{font-size:12px;font-weight:600;text-align:center;overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical}
.chart-halo .halo-wrap{position:relative;max-width:640px;margin:0 auto}
.chart-halo #halo-svg{width:100%;height:auto;display:block}
.halo-arc{fill:var(--panel);stroke:var(--border);stroke-width:1;cursor:pointer}
.halo-arc:hover{fill:var(--wash)}
.halo-center{fill:var(--accent);opacity:.9;cursor:pointer}
.halo-label{font-size:11px;fill:var(--text);pointer-events:none;font-family:-apple-system,sans-serif}
.halo-center-label{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-weight:700;font-size:15px;pointer-events:none;text-align:center;max-width:140px;color:#fff}
.chart-constellation .constellation-wrap{position:relative;min-height:60vh}
.chart-constellation #constellation-canvas{display:block;cursor:pointer}
/* Chart transition — Kin's curve */
.chart{transition:opacity .28s cubic-bezier(.32,.72,.35,1)}
.chart.chart-switching{opacity:0}
/* Flash highlight for "All buddies" navigation — brief accent glow that fades */
.proj-row.flash-highlight{outline:2px solid var(--accent);outline-offset:2px;border-radius:8px;
  animation:flashFade 2.5s ease-out forwards}
@keyframes flashFade{0%{background:color-mix(in srgb,var(--accent) 18%,transparent)}100%{background:transparent}}
#treezoom,#treezoom *{user-select:none;-webkit-user-select:none}
/* Draggable splitter between the two tree panes */
#tree-split{flex:0 0 12px;cursor:row-resize;display:flex;align-items:center;justify-content:center;
  background:var(--bg);border-top:1px solid var(--border);border-bottom:1px solid var(--border);
  touch-action:none;z-index:4}
#tree-split .split-grip{width:52px;height:4px;border-radius:2px;background:var(--border2)}
#tree-split:hover .split-grip,#tree-split:active .split-grip{background:var(--accent)}
/* Slim vertical zoom — right edge of each pane; no panel chrome; large◼ · slider · small▪ · fit */
.zoombar{position:absolute;top:50%;right:10px;transform:translateY(-50%);z-index:5;
  display:flex;flex-direction:column;align-items:center;gap:6px;width:auto;height:auto;
  padding:0;margin:0;background:none;border:none;border-radius:0;box-shadow:none;
  -webkit-tap-highlight-color:transparent}
.zoombar .z-out,.zoombar .z-in{flex:0 0 auto;line-height:1;color:var(--faint);user-select:none;pointer-events:none;
  text-shadow:0 0 4px var(--bg),0 0 8px var(--bg)}
.zoombar .z-out{font-size:8px}   /* zoom out (bottom) */
.zoombar .z-in{font-size:13px}   /* zoom in (top) */
input[type=range].zrange{flex:0 0 auto;width:22px;height:112px;margin:0;padding:0;
  writing-mode:vertical-lr;direction:rtl;/* high value at top, next to large mark */
  -webkit-appearance:none;appearance:none;
  background:transparent;cursor:ns-resize;touch-action:none;opacity:1}
/* High-contrast thumb: solid accent puck with a background-colored ring + halo so it pops on any tile */
input[type=range].zrange::-webkit-slider-runnable-track{width:5px;background:var(--faint);border-radius:3px}
input[type=range].zrange::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:20px;height:20px;margin-left:-8px;
  border-radius:50%;background:var(--accent);border:2px solid var(--bg);
  box-shadow:0 0 0 1.5px var(--accent-hi),0 1px 5px rgba(0,0,0,.5);cursor:ns-resize}
input[type=range].zrange::-moz-range-track{width:5px;background:var(--faint);border-radius:3px}
input[type=range].zrange::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:var(--accent);
  border:2px solid var(--bg);box-shadow:0 0 0 1.5px var(--accent-hi),0 1px 5px rgba(0,0,0,.5);cursor:ns-resize}
.zfit{flex:0 0 auto;background:none;border:none;border-radius:6px;color:var(--faint);
  font-size:12px;width:22px;height:22px;padding:0;cursor:pointer;line-height:1;
  text-shadow:0 0 4px var(--bg),0 0 8px var(--bg)}
.zfit:hover{color:var(--text);background:transparent}
/* Fixed to viewport at sidebar edge so vertical #sidebar scroll doesn't move it.
   MUST be a DOM sibling of #sidebar (not a child): overflow on #sidebar clips
   hit-testing/paint for fixed descendants, which made the gripper invisible. */
#sb-resize{position:fixed;top:0;left:calc(var(--sbw, 308px) - 14px);z-index:50;
  display:flex;align-items:center;justify-content:center;width:28px;height:100vh;height:100dvh;cursor:ew-resize;
  background:transparent;-webkit-tap-highlight-color:transparent;touch-action:none;user-select:none}
/* 2x5 dot-grid gripper (Jonny's pick, 2026-10-11): honest affordance, no hover required */
#sb-resize::after{content:'';width:14px;height:35px;transform:translateX(-9px);
  background-image:radial-gradient(circle,var(--gripdot,color-mix(in srgb,var(--muted) 34%,var(--border))) 1.6px,transparent 1.7px);
  background-size:7px 7px;background-position:center;background-repeat:repeat}
#sb-resize:hover::after{--gripdot:var(--text2)}
#sb-resize:active::after{--gripdot:var(--accent)}
#sb-resize:hover{background:transparent}
body.sb-closed #sb-resize{display:none}
/* Phone drawer: stay fixed (sibling of #sidebar); show only while drawer is open */
@media (max-width:639px){
  #sb-resize{display:none;left:calc(var(--sbw, 308px) - 14px);width:28px;z-index:96}
  #sidebar.open ~ #sb-resize{display:flex}
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
/* Buddy-panel scroll-to-top — same chip, centered at the bottom of the info panel */
#bp-to-top{position:fixed;bottom:16px;z-index:48;
  width:44px;height:44px;border-radius:12px;padding:0;
  display:flex;align-items:center;justify-content:center;
  background:color-mix(in srgb, var(--panel) 78%, transparent);border:1px solid var(--border);
  color:var(--muted);cursor:pointer;
  box-shadow:0 2px 14px var(--shadow);
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);
  opacity:0;pointer-events:none;transform:translateY(6px);
  transition:opacity .18s ease,transform .18s ease,color .15s,border-color .15s;
  -webkit-tap-highlight-color:transparent}
#bp-to-top.show{opacity:1;pointer-events:auto;transform:none}
/* Floating + button — iOS frosted-glass translucency (Jonny-approved look, Dave 2026-10-13) */
#new-buddy-fab{position:fixed;right:20px;bottom:20px;z-index:9000;width:56px;height:56px;border-radius:50%;
  background:rgba(50,50,52,.55);color:#fff;border:.5px solid rgba(255,255,255,.25);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  -webkit-backdrop-filter:blur(20px) saturate(180%);backdrop-filter:blur(20px) saturate(180%);
  box-shadow:0 4px 16px rgba(0,0,0,.25);-webkit-tap-highlight-color:transparent}
html.light #new-buddy-fab{background:rgba(255,255,255,.55);color:#1c1c1e;border-color:rgba(0,0,0,.08)}
/* Hide the FAB while Settings is open — it overlapped the Done button */
body:has(#field-settings.show) #new-buddy-fab{display:none}
#new-buddy-fab:active{transform:scale(.94)}
/* New-buddy request bottom sheet */
#newbuddy-sheet{position:fixed;inset:0;z-index:10000;display:flex;align-items:flex-end;justify-content:center}
#newbuddy-sheet .nb-backdrop{position:absolute;inset:0;background:rgba(0,0,0,.5);opacity:0;transition:opacity .25s}
#newbuddy-sheet .nb-sheet{position:relative;background:var(--panel);border-radius:20px 20px 0 0;padding:12px 22px 0;margin:0 16px;width:100%;max-width:560px;box-sizing:border-box;height:auto;max-height:88vh;display:flex;flex-direction:column;min-width:0;
  box-shadow:0 -8px 40px rgba(0,0,0,.4);transform:translateY(100%);transition:transform .3s cubic-bezier(.32,.72,.35,1)}
#newbuddy-sheet .nb-body{overflow-y:auto;padding-bottom:16px;min-width:0}
#newbuddy-sheet .nb-body > *{min-width:0;max-width:100%}
#newbuddy-sheet .nb-actions{position:sticky;bottom:0;background:var(--panel);padding:14px 0 26px;border-top:1px solid var(--border2);display:flex;gap:10px;justify-content:flex-end;margin:0 -22px;padding-left:22px;padding-right:22px}
#newbuddy-sheet .nb-actions button{font-size:14px;font-weight:600;padding:10px 22px;border-radius:20px;cursor:pointer;border:1px solid var(--border)}
#newbuddy-sheet .nb-actions .ab-cancel{background:none;color:var(--text)}
#newbuddy-sheet .nb-actions .ab-create{background:var(--accent);border-color:var(--accent);color:#fff}
#newbuddy-sheet .nb-actions .ab-create:disabled{opacity:.4;cursor:default}
#newbuddy-sheet.open .nb-backdrop{opacity:1}
#newbuddy-sheet.open .nb-sheet{transform:translateY(0)}
#newbuddy-sheet .nb-grab{width:44px;height:5px;border-radius:3px;background:var(--border);margin:0 auto 14px}
#newbuddy-sheet h2{margin:0 0 4px;font-size:19px}
#newbuddy-sheet label{display:block;font-size:12px;color:var(--muted);margin:14px 0 8px;text-transform:uppercase;letter-spacing:.8px}
#newbuddy-sheet input[type=text],#newbuddy-sheet textarea{width:100%;box-sizing:border-box;font-size:16px;padding:10px 12px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-family:inherit}
#newbuddy-sheet textarea{resize:vertical;min-height:76px}
#newbuddy-sheet .nb-personas{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-height:220px;overflow-y:auto;padding:2px;scrollbar-width:thin;scrollbar-color:var(--border) transparent}
#newbuddy-sheet .nb-personas::-webkit-scrollbar{width:6px}
#newbuddy-sheet .nb-personas::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
#newbuddy-sheet .nb-personas::-webkit-scrollbar-track{background:transparent}
#newbuddy-sheet .nb-personas button{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 6px;border-radius:12px;border:1px solid var(--border);background:var(--bg);color:var(--text);cursor:pointer;font-size:12px}
#newbuddy-sheet .nb-personas button.sel{border-color:var(--accent);background:var(--wash)}
#newbuddy-sheet .nb-p-emoji{font-size:24px}
#newbuddy-sheet .nb-p-name{text-align:center;line-height:1.25}
/* ---- Persona picker (info panel) — Kin language, phone-first, dark-mode safe ---- */
.bp-persona-cur{padding:2px 0}
.bp-persona-name{font-size:15px;font-weight:700;color:var(--text)}
.bp-persona-blurb{font-size:13px;color:var(--muted);margin-top:2px;line-height:1.4}
#persona-picker{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:16px}
#persona-picker .pp-backdrop{position:absolute;inset:0;background:var(--scrim)}
#persona-picker .pp-sheet{position:relative;width:100%;max-width:560px;max-height:82vh;display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--border);border-radius:16px;box-shadow:0 12px 40px var(--shadow);overflow:hidden}
#persona-picker .pp-head{padding:16px 16px 0}
#persona-picker .pp-head h2{margin:0 0 2px;font-size:17px}
#persona-picker #pp-filter{padding:10px 12px;font-size:16px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-family:inherit;box-sizing:border-box}
#persona-picker .pp-grid{flex:1;min-height:0;overflow-y:auto;display:grid;grid-template-columns:repeat(2,1fr);gap:8px;padding:12px 16px;scrollbar-width:thin;scrollbar-color:var(--border) transparent}
#persona-picker .pp-card{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:10px 12px;border-radius:12px;border:1px solid var(--border);background:var(--bg);color:var(--text);cursor:pointer;text-align:left;min-height:44px;-webkit-tap-highlight-color:transparent}
#persona-picker .pp-card:hover{border-color:var(--accent)}
#persona-picker .pp-play{display:inline-block;margin-left:6px;font-size:12px;color:var(--accent);cursor:pointer;padding:2px 6px;border-radius:6px;vertical-align:middle}
#persona-picker .pp-play:hover{background:var(--active)}
#persona-picker .pp-card.sel{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent);background:var(--active)}
#persona-picker .pp-name{font-size:13px;font-weight:700}
#persona-picker .pp-quote{font-size:12.5px;color:var(--muted);font-style:italic;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis}#persona-picker .pp-blurb{font-size:12px;color:var(--muted);line-height:1.35;opacity:.85}
#persona-picker .pp-actions{display:flex;gap:8px;flex-wrap:wrap;padding:12px 16px 16px;border-top:1px solid var(--border)}
@media (max-width:639px){
  #persona-picker{align-items:flex-end;padding:0}
  #persona-picker .pp-sheet{max-width:none;border-radius:16px 16px 0 0;max-height:88vh}
  #persona-picker .pp-grid{grid-template-columns:1fr}
}
#newbuddy-sheet .nb-place{display:flex;background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:3px;gap:3px}
#newbuddy-sheet .nb-place button{flex:1;border:none;background:none;color:var(--muted);font-size:13px;font-weight:600;padding:8px 4px;border-radius:9px;cursor:pointer}
#newbuddy-sheet .nb-place button.sel{background:var(--panel);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.2)}
#bp-to-top:hover{color:var(--accent);border-color:var(--accent)}
#bp-to-top:active{transform:scale(.96)}
#bp-to-top svg{display:block}
body.standalone #bp-to-top{opacity:0!important;pointer-events:none!important}
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
/* Changelog / Release Notes: never scroll horizontally — wrap long words */
#view-changelog .changelog,#view-releases .changelog{overflow-x:hidden;overflow-wrap:break-word;word-break:break-word}
#view-changelog .changelog a,#view-releases .changelog a{overflow-wrap:break-word;word-break:break-all}
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
/* Reopen right detail panel when closed (Muse-ish fixed chrome) */
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
.ctog{display:none;width:22px;height:22px;flex:0 0 22px;align-items:center;justify-content:center;
  background:none;border:none;color:var(--muted);cursor:pointer;font-size:14px;padding:0;margin-right:2px;border-radius:6px}
.ctog.has-kids{display:inline-flex}
.ctog.has-kids:hover{background:var(--hover);color:var(--text)}
.ctog .chev{display:inline-block;transition:transform .15s;font-style:normal;line-height:1}
.ctog.has-kids:not(.collapsed) .chev{transform:rotate(90deg)}
#field-settings{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2000;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;width:340px;max-height:80vh;
  box-shadow:0 12px 40px var(--scrim);display:none;overflow:hidden;container-type:inline-size}
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
#field-settings .fset-resize{position:absolute;right:3px;bottom:3px;width:14px;height:14px;cursor:nwse-resize;opacity:.55;touch-action:none;
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
.fset-choice{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:8px;padding:11px 12px;font-size:13.5px;
  border:1px solid var(--border2);border-radius:10px;background:var(--bg)}
.fset-choice select{background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:8px;
  padding:6px 10px;font-size:13px;font-family:inherit}
/* Attention-effect live preview (Advanced settings): a mini attention header running the selected fx */
.attnfx-preview{margin:10px 2px 4px;padding:12px;border:1px dashed var(--border);border-radius:10px;background:var(--panel)}
.attnfx-preview .bp-sec{margin:0}
.attnfx-preview .bp-sec>h3{margin:0}
.attnfx-preview .fineprint{margin:8px 0 0}
/* Narrow settings sheet: stack labels above controls instead of scrunching them */
@container (max-width:440px){
  #field-settings .fset-choice{flex-wrap:wrap}
  #field-settings .fset-choice>span:first-child{flex:1 1 100%}
}
/* Wide settings sheet: Main views + Buddy fields side by side, each scrolling on its own */
@container (min-width:640px){
  #field-settings .fset-cols{display:flex;gap:16px;align-items:stretch}
  #field-settings .fset-cols>.fset-sec{flex:1 1 0;min-width:0}
  #field-settings .fset-cols #vset-list,#field-settings .fset-cols #fset-list{max-height:340px;overflow-y:auto}
}
/* Narrow sidebar: drop the kind column so buddy names get full room */
@container (max-width:290px){
  #sidebar .bkind{display:none}
}
/* Sidebar section drag-to-reorder */
#sidebar .nav-sec>h3{cursor:grab!important}
#sidebar .nav-sec.sec-dragging{opacity:.35}
#sidebar .nav-sec.sec-drop-before{box-shadow:0 -2px 0 var(--accent)}
#sidebar .nav-sec.sec-drop-after{box-shadow:0 2px 0 var(--accent)}
#field-settings input[type=checkbox],
.fset-check input[type=checkbox]{
  -webkit-appearance:none;appearance:none;width:28px;height:28px;margin:0;flex:0 0 28px;
  border:2px solid var(--border);border-radius:50%;background:var(--panel);cursor:pointer;
  position:relative;transition:background .15s ease,border-color .15s ease,box-shadow .15s ease,transform .12s ease}
#field-settings input[type=checkbox]:hover,
.fset-check input[type=checkbox]:hover{border-color:var(--accent);background:var(--ghost)}
#field-settings input[type=checkbox]:checked,
.fset-check input[type=checkbox]:checked{background:var(--accent);border-color:var(--accent)}
#field-settings input[type=checkbox]:checked::after,
.fset-check input[type=checkbox]:checked::after{
  content:'';position:absolute;left:9px;top:4px;width:6px;height:12px;
  border:solid var(--on-accent);border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
#field-settings input[type=checkbox]:focus-visible,
.fset-check input[type=checkbox]:focus-visible{outline:none;box-shadow:0 0 0 3px var(--ghost)}
#field-settings input[type=checkbox]:active,
.fset-check input[type=checkbox]:active{transform:scale(.92)}
.fset-row input[type=checkbox]{margin-left:2px}
.bp-close-x{position:static;flex:0 0 auto;width:44px;height:44px;margin-left:auto;
  background:none;border:1px solid transparent;border-radius:10px;color:var(--muted);font-size:22px;
  cursor:pointer;display:none;align-items:center;justify-content:center;padding:0;
  -webkit-tap-highlight-color:transparent}
.bp-close-x:hover{color:var(--text);border-color:var(--border);background:var(--ghost)}
.bp-close-x:active{opacity:.7}
/* Open panel: the close button floats at the exact screen position of the
   #panel-open expand button, styled as the same control */
#view-buddy.panel .bp-close-x,#view-buddy.sheet .bp-close-x{display:flex;position:fixed;top:12px;right:12px;z-index:65;margin:0;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;box-shadow:0 2px 14px var(--shadow)}
#view-buddy.panel .bp-close-x:hover,#view-buddy.sheet .bp-close-x:hover{color:var(--accent);border-color:var(--accent)}
#view-buddy.panel .bp-close-x:active,#view-buddy.sheet .bp-close-x:active{transform:scale(.96)}
body:has(#token-pill) #view-buddy.panel .bp-close-x,
body:has(#token-pill) #view-buddy.sheet .bp-close-x{right:148px}
/* Keep header content clear of the floating close button */
#view-buddy.panel .bp-sticky-head,#view-buddy.sheet .bp-sticky-head{padding-right:52px}
/* Portrait takeover uses the sticky back bar; keep close button for panel / landscape sheet */
@media (max-width:639px) and (orientation:portrait){
  #view-buddy.sheet .bp-close-x{display:none}
  #view-buddy.sheet .bp-sticky-head{padding-right:0}
}
#buddy-home{position:relative}
#bp-resize{position:fixed;top:0;bottom:0;right:calc(var(--bpw, 380px) - 14px);z-index:60;display:flex;align-items:center;justify-content:center;width:28px;cursor:ew-resize;
  background:transparent;-webkit-tap-highlight-color:transparent;touch-action:none;user-select:none}
/* Same dot-grid gripper language as #sb-resize */
#bp-resize::after{content:'';width:14px;height:35px;
  background-image:radial-gradient(circle,var(--gripdot,color-mix(in srgb,var(--muted) 34%,var(--border))) 1.6px,transparent 1.7px);
  background-size:7px 7px;background-position:center;background-repeat:repeat}
#bp-resize:hover::after{--gripdot:var(--text2)}
#bp-resize:active::after{--gripdot:var(--accent)}
#bp-resize:hover{background:transparent}
#view-buddy.active:not(.panel):not(.sheet) #bp-resize{display:none}
#view-buddy.sheet.active #bp-resize{display:none}
.pupload{height:150px;min-width:120px;border-radius:10px;border:1px dashed var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:var(--bg);flex:0 0 auto}
.pupload .pbar{width:80px;height:6px;background:var(--border2);border-radius:3px;overflow:hidden}
.pupload .pbar > div{height:100%;background:var(--accent);border-radius:3px;transition:width .2s}
.pupload .plabel{font-size:11px;color:var(--muted)}
.dumps-head{cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px;margin:12px 0 0}
.dumps-head h4{margin:0;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:var(--muted)}
.dumps-head .darrow{font-size:25px;color:var(--muted);transition:transform .15s;display:inline-block;line-height:1;position:relative;top:-2px}
.bp-sec > h3{cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px}
.bp-sec > h3 .secgrip{cursor:grab;color:var(--faint);font-size:14px;line-height:1;padding:2px 4px;border-radius:4px;
  margin-left:auto;touch-action:none}
.bp-sec > h3 .secgrip:hover{color:var(--muted);background:var(--ghost)}
.bp-sec > h3 .secgrip:active{cursor:grabbing}
.bp-sec.sec-dragging{opacity:0.4}
.bp-sec > h3 .secarrow{font-size:25px;color:var(--muted);transition:transform .15s;display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:50%;background:var(--ghost);line-height:1;flex:0 0 auto}
.bp-sec.collapsed > *:not(h3){display:none !important} /* !important beats inline display styles (e.g. homepage URL row) */
.bp-sec .secarrow{transform:rotate(90deg)}
.bp-sec.collapsed .secarrow{transform:rotate(0deg)}
.dumps .darrow{transform:rotate(90deg)}
.dumps.collapsed .darrow{transform:rotate(0deg)}
.dump-actions{position:absolute;top:10px;right:12px;display:flex;gap:8px;align-items:center}
.dump-act{background:none;border:none;cursor:pointer;opacity:.35;padding:3px;line-height:1;color:var(--muted);display:inline-flex;align-items:center}
.dump-act:hover{opacity:1;color:var(--text)}
.dump-act:active{opacity:1}
.dump-act[data-dump-del]{color:#e0533d}
.dump-act[data-dump-del]:hover{color:#ff6b5b}
.dump-act svg{width:14px;height:14px;display:block}
body.no-write .pdel,body.no-write [data-dump-del],body.no-write [data-dump-edit]{display:none!important}
.dumps-body .attn-body{padding-right:64px}
.dumps-body .attn{overflow:hidden;transition:max-height .3s ease,opacity .25s ease,margin .3s ease,padding .3s ease,border-width .3s ease}
.dumps-body .attn.dump-removing{max-height:0!important;opacity:0;margin-bottom:0!important;padding-top:0!important;padding-bottom:0!important;border-top-width:0;border-bottom-width:0}
.toast.undo-toast{display:flex;align-items:center;gap:14px;padding:8px 8px 8px 20px;white-space:normal}
.undo-btn{background:var(--accent);border:none;color:#fff;font:inherit;font-size:14px;font-weight:600;border-radius:999px;padding:8px 18px;cursor:pointer;flex:0 0 auto}
.undo-btn:active{transform:scale(.96)}
.dumps.collapsed .dumps-body{display:none}
/* Sidebar top-right tools: gear + close (44px targets, 8px gap — HIG touch spacing) */
#sb-tools{position:absolute;top:8px;right:8px;z-index:10;display:flex;align-items:center;gap:8px}
#sb-tools button{width:44px;height:44px;background:none;border:none;border-radius:10px;color:var(--muted);
  cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;-webkit-tap-highlight-color:transparent}
#sb-tools button:hover{background:var(--hover);color:var(--text)}
#sb-tools button svg{display:block}
#sb-gear{color:red}
#sb-gear:hover{color:red;background:var(--hover)}
#sb-close{color:var(--faint)}
#sb-close:hover{color:var(--muted)}
#sb-close .xmark-x{stroke:var(--bg)}
#sidebar .brand{padding-right:112px}
/* Collapsed sidebar (iPad/desktop): hide panel, show hamburger to reopen */
body.sb-closed #sidebar{display:none}
body.sb-closed #menu-btn{display:flex;align-items:center;justify-content:center;position:fixed;top:12px;left:12px;z-index:90;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:27px;
  width:48px;height:48px;cursor:pointer;box-shadow:0 2px 12px var(--shadow)}
#plans-sec.collapsed #plan-nav{display:none}
#plans-sec #plans-arrow{transform:rotate(90deg);display:inline-block}
#plans-sec.collapsed #plans-arrow{transform:rotate(0deg)}
/* Collapsible sidebar sections (Views, Buddies) — same pattern as Business Plans */
.nav-sec.collapsed > div:last-child{display:none}
.nav-sec .nav-arrow{transform:rotate(90deg);display:inline-block}
.nav-sec.collapsed .nav-arrow{transform:rotate(0deg)}

#avatar-picker{position:fixed;z-index:2000;background:var(--panel);border:1px solid var(--border);border-radius:12px;
  padding:16px;width:320px;max-height:70vh;overflow-y:auto;display:none;box-shadow:0 12px 40px var(--scrim)}
#avatar-picker.show{display:block}
#avatar-picker h4{margin:0 0 10px;font-size:13px}
.av-cat{font-size:11px;color:var(--muted);margin:10px 0 4px;text-transform:uppercase;letter-spacing:.06em}
.av-cat:first-of-type{margin-top:0}
#avatar-grid{margin-bottom:10px}
.av-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:4px}
.av-grid button{background:none;border:1px solid transparent;border-radius:8px;font-size:20px;padding:6px;cursor:pointer}
.av-grid button:hover{border-color:var(--accent);background:var(--hover)}
#avatar-picker input{width:100%;box-sizing:border-box;background:var(--bg);border:1px solid var(--border);color:var(--text);
  border-radius:8px;padding:8px;font-size:14px;text-align:center}
.info-tip{position:relative;display:inline-block;margin-left:6px;cursor:help;color:var(--muted);font-size:15px;line-height:1}
.info-tip:hover{color:var(--text)}
/* Tooltips are JS popovers (see tipPop code) — hover on mouse, tap-to-pin with × on touch */
.tip-pop{position:fixed;z-index:1000;max-width:240px;background:var(--panel);border:1px solid var(--border);
  color:var(--text);padding:10px 12px;border-radius:10px;font-size:12.5px;line-height:1.5;text-transform:none;
  box-shadow:0 8px 28px rgba(0,0,0,.28);white-space:normal}
.tip-pop.pinned{padding-right:30px}
.tip-pop .tip-x{position:absolute;top:4px;right:6px;background:none;border:none;color:var(--muted);
  font-size:17px;line-height:1;padding:4px 6px;cursor:pointer;border-radius:6px}
.tip-pop .tip-x:hover{color:var(--text);background:var(--ghost)}
.ghtoken input{flex:1;min-width:180px;background:var(--bg);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:7px 10px;font-size:13px}
.linkbtn{background:none;border:none;color:var(--accent);cursor:pointer;font-size:13px;padding:2px 4px}
.linkbtn:hover{text-decoration:underline}
.bp-topnav{margin-bottom:6px}
.bp-build{margin:26px 0 6px;font-size:11px;color:var(--faint);text-align:center;cursor:pointer}
.status.st-dormant{background:rgba(139,148,158,.15);color:var(--muted);border:1px solid var(--border)}
.brow.dormant{opacity:.5}.brow.dormant .bname{font-style:italic}
.bp-build:hover{color:var(--accent);text-decoration:underline}
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
  .app{display:block}
  /* Prevent iOS auto-zoom on input focus */
  input, textarea, select{font-size:16px !important}
  #menu-btn{display:flex;align-items:center;justify-content:center;position:fixed;top:12px;left:12px;z-index:90;
    background:var(--panel);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:27px;
    width:48px;height:48px;cursor:pointer;box-shadow:0 2px 12px var(--shadow)}
  /* Sidebar drawer with scrim.
     pointer-events:none while closed so the off-screen drawer never steals the
     left-edge swipe / tree pan hit target (transform alone is not enough on iOS). */
  #sidebar{position:fixed;left:0;top:0;bottom:0;z-index:95;height:100vh;height:100dvh;
    transform:translateX(-105%);transition:transform .28s cubic-bezier(.32,.72,.35,1);width:100vw;max-width:100vw;flex:none;
    pointer-events:none}
  #sidebar.open{transform:none;box-shadow:12px 0 40px rgba(0,0,0,.35);pointer-events:auto}
  /* Sidebar resize: sibling of #sidebar; visibility gated by #sidebar.open ~ #sb-resize above */
  #sb-resize{touch-action:none}
  html,body{overflow-x:clip}
  #sb-scrim{display:none;position:fixed;inset:0;z-index:94;background:rgba(0,0,0,.45);opacity:0;transition:opacity .25s}
  #sb-scrim.show{display:block;opacity:1}
  #main{padding:72px 12px 60px}
  /* Tree keeps the org chart on phones — pan with a finger, zoom with the floating slider */
  .standalones .grid{display:block}
  /* Vertical zoom on the right — fat hit areas (≈44px), no filled panel */
  .zoombar{right:4px;z-index:30;padding:8px 4px;gap:4px}
  input[type=range].zrange{width:44px;height:140px}
  .zfit{width:44px;height:44px;font-size:14px;display:flex;align-items:center;justify-content:center}
  .zoombar .z-out,.zoombar .z-in{padding:4px 0}
  /* Chunkier tree nodes for touch */
  #treezoom .node{padding:15px 14px;min-height:60px}
  /* Buddy panel — full screen on phone */
  #view-buddy.sheet{position:fixed;left:0;right:0;bottom:0;top:0;z-index:96;
    background:var(--bg);border-top:1px solid var(--border);border-radius:0;
    overflow-y:auto;overflow-x:hidden;padding:8px 18px calc(60px + env(safe-area-inset-bottom));box-shadow:0 -12px 40px rgba(0,0,0,.35);
    -webkit-overflow-scrolling:touch}
  #view-buddy.sheet::before{display:none}
  /* Plans: single column cards */
  .plan-grid{display:block;max-width:none}
  .plan-card{margin-bottom:12px}
  /* Projects / Manifest / SME rows: card stack — title (+ status), then full-width description */
  .proj-row{
    display:flex !important;flex-direction:column !important;flex-wrap:nowrap !important;
    align-items:stretch !important;gap:6px;
    background:var(--panel);border:1px solid var(--border);border-bottom:1px solid var(--border);
    border-radius:12px;margin:0 0 8px;padding:12px 14px;min-height:52px}
  .proj-row .pname{font-size:16px}
  .proj-row .pdesc{font-size:15.5px;line-height:1.45}
  .proj-row .dot{display:none}
  .proj-row-head{display:flex;align-items:center;gap:8px;width:100%;min-width:0}
  .proj-row-head .parrow{flex:0 0 auto;margin-top:0}
  .proj-row-head .pname{flex:1 1 auto;min-width:0;white-space:normal;line-height:1.3}
  .proj-row-head .status{flex:0 0 auto;margin-left:auto}
  .proj-row-head .proj-info{flex:0 0 auto;padding:4px !important;opacity:.75}
  .proj-row > .pdesc,.proj-row .pdesc{
    display:block;order:unset;flex:none !important;width:100% !important;max-width:none !important}
  /* Static rows without .proj-row-head (Manifest): CSS grid stack */
  .proj-row:not(:has(.proj-row-head)){
    display:grid !important;grid-template-columns:1fr auto;grid-template-areas:"title status" "desc desc";
    gap:6px 10px;align-items:start}
  .proj-row:not(:has(.proj-row-head)) .pname{grid-area:title;white-space:normal;line-height:1.3;min-width:0}
  .proj-row:not(:has(.proj-row-head)) .status{grid-area:status;justify-self:end}
  .proj-row:not(:has(.proj-row-head)) .pdesc{grid-area:desc}
  .proj-row:not(:has(.proj-row-head)) .parrow{display:none}
  .proj-row.d0,.proj-row.d1,.proj-row.d2,.proj-row.d3{padding-left:14px}
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
  /* Keep a real left sidebar — do not stack above main (iPad portrait is ~744–834px). */
  .app{display:flex;flex-direction:row;align-items:stretch}
  #sidebar{width:250px;flex:0 0 250px;position:sticky;top:0;height:100vh;height:100dvh;
    max-height:none;border-right:1px solid var(--border2);border-bottom:0;overflow-y:auto;overflow-x:hidden;
    z-index:40;background:var(--bg)}
  #main{flex:1;min-width:0;padding:28px 22px 64px;position:relative;z-index:1}
  #main.homepage-mode{padding:0}
  .node{width:max-content;min-width:180px;max-width:320px}
  #view-buddy.panel{position:fixed;top:0;right:0;bottom:0;width:min(380px,calc(100vw - 250px));z-index:30;
    background:var(--bg);border-left:1px solid var(--border);overflow-y:auto;overflow-x:hidden;
    padding:20px 18px 48px;box-shadow:-8px 0 32px var(--shadow)}
}
/* ---- Large: >1100px (desktop) ---- */
@media (min-width:1101px){
  #view-buddy.panel{position:fixed;top:0;right:0;bottom:0;width:400px;z-index:60;
    background:var(--bg);border-left:1px solid var(--border);overflow-y:auto;overflow-x:hidden;
    padding:24px 20px 48px;box-shadow:-8px 0 32px var(--shadow)}
}
#view-buddy.panel.active,#view-buddy.sheet.active{display:block}
#main .view{display:none}
#main .view.active{display:block}
#main #view-project.active{display:flex;flex-direction:column;min-height:calc(100vh - 116px)}
#bp-close{display:none}
#view-buddy.panel #bp-close,#view-buddy.sheet #bp-close{display:inline-block}
/* ---------- Project view: stat tiles + buddy homepage embed ---------- */
#project-tiles{display:flex;gap:14px;margin:2px auto 20px;max-width:860px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:thin}
#project-status-tiles{display:flex;gap:14px;margin:2px auto 20px;max-width:860px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:thin}
#project-status-tiles .ptile{flex:0 0 auto}
.ptile{flex:0 0 auto;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:12px 14px;position:relative;overflow:hidden;cursor:pointer;transition:transform .15s ease,box-shadow .15s ease}
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
.ptile-label{font-size:11px;letter-spacing:.14em;font-weight:700;color:var(--muted);white-space:nowrap}
.ptile-num{font-size:42px;font-weight:800;color:var(--tint);line-height:1.25}
.ptile-sub{font-size:13px;color:var(--muted)}
.ptile[data-tile]{cursor:pointer}
.ptile.sel{box-shadow:inset 0 0 0 2px var(--tint)}
/* Phone tiles AFTER base .ptile so cascade wins (beat inline gap/display too) */
@media (max-width:639px){
  #project-tiles,#changelog-tiles,#plans-tiles,#manifest-tiles,#project-status-tiles{
    display:flex !important;flex-wrap:nowrap !important;overflow-x:auto !important;
    gap:8px !important;max-width:none !important;width:100% !important;
    margin:0 0 12px !important;box-sizing:border-box;scrollbar-width:thin}
  #project-tiles .ptile,#changelog-tiles .ptile,#plans-tiles .ptile,#manifest-tiles .ptile,
  #project-status-tiles .ptile{flex:0 0 auto !important;max-width:none !important;min-width:0 !important}
  .ptile{padding:6px 8px 5px !important;border-radius:10px !important}
  .ptile::before{width:3px}
  .ptile-label{font-size:9px !important;letter-spacing:.08em;line-height:1.15}
  .ptile-num{font-size:18px !important;line-height:1.05 !important;margin:1px 0}
  .ptile-sub{font-size:10px !important;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
}
/* Landscape phones are often >639px wide — key off short height instead */
@media (orientation:landscape) and (max-height:520px){
  #project-tiles,#changelog-tiles,#plans-tiles,#manifest-tiles,#project-status-tiles{
    display:flex !important;flex-wrap:nowrap !important;overflow-x:auto !important;
    gap:8px !important;max-width:none !important;width:100% !important;
    margin:0 0 10px !important;box-sizing:border-box;scrollbar-width:thin}
  #project-tiles .ptile,#changelog-tiles .ptile,#plans-tiles .ptile,#manifest-tiles .ptile,
  #project-status-tiles .ptile{flex:0 0 auto !important;max-width:none !important;min-width:0 !important}
  .ptile{padding:5px 7px 4px !important;border-radius:10px !important}
  .ptile::before{width:3px}
  .ptile-label{font-size:9px !important;letter-spacing:.08em;line-height:1.15}
  .ptile-num{font-size:16px !important;line-height:1.05 !important;margin:1px 0}
  .ptile-sub{font-size:10px !important;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
}
#main.homepage-mode{padding:0}
#main.homepage-mode #view-project.active{min-height:100vh}
#homepage-wrap{flex:1;display:flex;flex-direction:column;min-height:0;margin:0;position:relative}
#homepage-open{display:none}
#homepage-open:hover{border-color:var(--accent);color:var(--accent)}
#homepage-frame{flex:1;width:100%;min-height:0;border:0;border-radius:0;background:#fff;display:block}
@media (max-width:760px){#main #view-project.active{min-height:calc(100vh - 88px)}
#main.homepage-mode{padding:0}
#main.homepage-mode #view-project.active{min-height:100vh}}

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
.proj-search-sticky{position:sticky;top:0;z-index:5;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--border);
  transition:margin .28s ease,top .28s ease,border-radius .28s ease,box-shadow .28s ease,background .28s ease,border-color .28s ease}
@media (max-width:640px){
  /* Stuck mode: compress into a floating pill between the panel buttons */
  .proj-search-sticky.is-stuck{top:12px;margin:0 68px 0 64px;padding:6px 8px;
    border:1px solid var(--border);border-radius:14px;
    background:color-mix(in srgb,var(--bg) 88%,transparent);
    -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);
    box-shadow:0 6px 20px var(--shadow);border-bottom:1px solid var(--border)}
}
.proj-controls{display:flex;gap:8px;align-items:center}
.proj-controls #proj-search{width:100%;box-sizing:border-box;background:var(--bg);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:7px 30px 7px 10px;font-size:13px}
.proj-controls #proj-search-clear{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:none;background:transparent;color:var(--muted);font-size:18px;line-height:1;cursor:pointer;padding:4px 8px;border-radius:6px}
.proj-controls #proj-search-clear:hover{color:var(--text);background:rgba(127,127,127,.18)}
.proj-mode-toggle{display:flex;border:1px solid var(--border);border-radius:8px;overflow:hidden;flex-shrink:0}
.proj-mode-toggle button{border:none;background:transparent;color:var(--muted);padding:7px 12px;font-size:13px;cursor:pointer}
.proj-mode-toggle button.sel{background:var(--active);color:var(--text)}
.proj-mode-toggle button+button{border-left:1px solid var(--border)}
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
.bp-aka{color:var(--muted);font-size:13px;font-style:italic;margin-left:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:60%}
.aka-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 10px;font-size:13px;background:var(--wash2);border:1px solid var(--border);border-radius:999px;color:var(--text)}
/* Section poof-away (Dave 2026-10-12): when the last item in a section is
   completed, the section dims, then poofs — sections below scooch up. */
.bp-sec.poof-dim{
  transition: opacity .3s ease;
  opacity: .35;
}
.bp-sec.poof-gone{
  transition: opacity .25s ease, transform .25s ease, max-height .45s ease, margin .45s ease, padding .45s ease;
  opacity: 0 !important;
  transform: scale(.96);
  max-height: 0 !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  overflow: hidden;
}
.bp-sec{margin-top:30px}
.bp-sec>h3{font-size:13px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin:0 0 12px}
.bp-sec>h3 .bp-add{float:right;font-size:12px;letter-spacing:0;text-transform:none;font-weight:600;color:var(--accent);background:none;border:1px solid var(--accent);border-radius:20px;padding:2px 10px;cursor:pointer}
.art-row.sib-compact{padding:6px 10px}.art-row.sib-compact .art-ic{font-size:18px}
.bp-sec>h3 .bp-circle-add{float:right;font-size:18px;line-height:1;color:var(--accent);background:none;border:none;cursor:pointer;min-width:44px;min-height:44px;display:inline-flex;align-items:center;justify-content:center}
.bp-sec>h3 .bp-add:active{transform:scale(.96)}
.bp-sec[data-field="attention"]>h3{color:var(--amber)}
/* Add-buddy dialog */
#addbuddy-modal{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center}
#addbuddy-modal .ab-backdrop{position:absolute;inset:0;background:rgba(0,0,0,.5)}
#addbuddy-modal .ab-box{position:relative;background:var(--panel);border-radius:14px;padding:22px;width:min(92vw,380px);box-shadow:0 12px 40px rgba(0,0,0,.35)}
#addbuddy-modal .ab-box h2{margin:0 0 4px;font-size:17px;overflow-wrap:break-word}
#addbuddy-modal .ab-sub{color:var(--muted);font-size:13px;margin:0 0 16px}
#addbuddy-modal label{display:block;font-size:12px;color:var(--muted);margin:12px 0 6px;text-transform:uppercase;letter-spacing:.8px}
#addbuddy-modal input[type=text]{width:100%;box-sizing:border-box;font-size:16px;padding:10px 12px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text)}
#addbuddy-modal .ab-icons{display:grid;grid-template-columns:repeat(8,1fr);gap:6px}
#addbuddy-modal .ab-icons button{font-size:22px;padding:6px 0;background:var(--bg);border:1px solid var(--border);border-radius:10px;cursor:pointer}
#addbuddy-modal .ab-icons button.sel{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
#addbuddy-modal .ab-kinds{display:flex;gap:8px;flex-wrap:wrap}
#addbuddy-modal .ab-kinds button{font-size:13px;padding:8px 12px;border-radius:20px;border:1px solid var(--border);background:var(--bg);color:var(--text);cursor:pointer}
#addbuddy-modal .ab-kinds button.sel{border-color:var(--accent);color:var(--accent);font-weight:700}
#addbuddy-modal .ab-actions{display:flex;gap:10px;margin-top:20px}
#addbuddy-modal .ab-actions button{flex:1;font-size:15px;font-weight:600;padding:12px;border-radius:12px;border:none;cursor:pointer}
#addbuddy-modal .ab-cancel{background:var(--bg);color:var(--text);border:1px solid var(--border)}
#addbuddy-modal .ab-create{background:var(--accent);color:#fff}
#addbuddy-modal .ab-create:disabled{opacity:.45}
#addbuddy-modal .ab-err{color:#e5484d;font-size:13px;margin-top:10px;min-height:18px}
/* What's-new modal (from the update banner) */
#whatsnew-modal{position:fixed;inset:0;z-index:10000}
.cl-type-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(72px,1fr));gap:8px;margin:0 0 12px}
.cl-type-stat{display:block;width:100%;box-sizing:border-box;font:inherit;appearance:none;-webkit-appearance:none;
  text-align:center;border:1px solid;border-radius:10px;padding:8px 6px;min-width:0;cursor:pointer;background:var(--panel)}
.cl-type-stat .value{font-size:20px;font-weight:800;letter-spacing:-.3px;line-height:1.1}
.cl-type-stat .label{font-size:11px;font-weight:700;margin-top:3px;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cl-type-stat.cl-type-added{color:#2f9e44;border-color:#2f9e44;background:rgba(47,158,68,.08)}
.cl-type-stat.cl-type-changed{color:#1f6feb;border-color:#1f6feb;background:rgba(31,111,235,.08)}
.cl-type-stat.cl-type-fixed{color:#d43d2a;border-color:#d43d2a;background:rgba(212,61,42,.08)}
.cl-type-stat[aria-pressed="true"]{box-shadow:inset 0 0 0 2px currentColor}
.wn-backdrop{position:absolute;inset:0;background:var(--scrim)}
.wn-box{position:absolute;top:8%;left:50%;transform:translateX(-50%);width:min(560px,calc(100vw - 32px));max-height:80vh;
  display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--border);border-radius:14px;
  box-shadow:0 16px 48px rgba(0,0,0,.4)}
.wn-head{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--border)}
.wn-head h3{margin:0;font-size:16px}
.wn-x{background:none;border:none;color:var(--text);font-size:22px;cursor:pointer;line-height:1;padding:4px}
.wn-body{padding:6px 18px 18px;overflow-y:auto;overflow-x:hidden;overflow-wrap:break-word;word-break:break-word}
.wn-body a{overflow-wrap:break-word;word-break:break-all}
.wn-body h4{margin:16px 0 6px;font-size:14.5px}
.wn-body h5{margin:12px 0 4px;font-size:13px;color:var(--muted)}
.wn-body ul{margin:4px 0 8px;padding-left:20px;font-size:13.5px;line-height:1.55}
.bp-sec[data-field="attention"].attn-high>h3{color:var(--danger)}
/* Attention-getting header effects (style chosen in Settings → Attention header effect) */
@keyframes attn-pulse{0%,100%{opacity:1}50%{opacity:.4}}
@keyframes attn-glow{0%,100%{text-shadow:0 0 0 rgba(0,0,0,0)}50%{text-shadow:0 0 14px var(--amber)}}
@keyframes attn-glow-red{0%,100%{text-shadow:0 0 0 rgba(0,0,0,0)}50%{text-shadow:0 0 14px var(--danger)}}
@keyframes attn-shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-3px)}75%{transform:translateX(3px)}}
@keyframes attn-blink{0%,100%{opacity:1}50%{opacity:.2}}
@keyframes attn-wiggle{0%,100%{transform:rotate(0deg)}20%{transform:rotate(-2.5deg)}40%{transform:rotate(2.5deg)}60%{transform:rotate(-1.5deg)}80%{transform:rotate(1.5deg)}}
@keyframes attn-bounce{0%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}55%{transform:translateY(0)}70%{transform:translateY(-2px)}}
@keyframes attn-swing{0%,100%{transform:rotate(0deg)}25%{transform:rotate(1.1deg)}75%{transform:rotate(-1.1deg)}}
.bp-sec[data-field="attention"].fx-pulse>h3{animation:attn-pulse 1.6s ease-in-out infinite}
.bp-sec[data-field="attention"].fx-glow>h3{animation:attn-glow 1.8s ease-in-out infinite}
.bp-sec[data-field="attention"].fx-glow.attn-high>h3{animation-name:attn-glow-red}
.bp-sec[data-field="attention"].fx-shake>h3{animation:attn-shake 1.2s ease-in-out infinite}
.bp-sec[data-field="attention"].fx-blink>h3{animation:attn-blink 1.1s steps(2,jump-none) infinite}
.bp-sec[data-field="attention"].fx-wiggle>h3{animation:attn-wiggle 1.6s ease-in-out infinite}
.bp-sec[data-field="attention"].fx-bounce>h3{animation:attn-bounce 1.8s ease-in-out infinite}
.bp-sec[data-field="attention"].fx-swing>h3{transform-origin:top center;animation:attn-swing 3s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.bp-sec[data-field="attention"]>h3{animation:none!important}}
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
.attn-text a{color:inherit;text-decoration:none}
.attn-text a:hover{text-decoration:underline}
.attn-open{font-size:11px;color:var(--accent)}
.attn-date{font-size:12px;color:var(--muted);margin-top:5px}
.seenbtn{flex:0 0 auto;background:var(--border2);border:1px solid var(--border);color:var(--text);
  width:44px;height:44px;border-radius:50%;font-size:18px;line-height:1;padding:0;cursor:pointer;touch-action:manipulation;
  display:flex;align-items:center;justify-content:center}
.seenbtn:hover{border-color:var(--accent);color:var(--accent)}
.attn-all .seenbtn{width:auto;height:auto;border-radius:999px;font-size:12.5px;padding:6px 12px}
.attn.seen{opacity:.55}
.attn.seen .adot{visibility:visible;background:var(--grn-solid);width:18px;height:18px;flex:0 0 18px;
  display:flex;align-items:center;justify-content:center;color:var(--on-accent);font-size:11px;font-weight:700}
.attn.seen .adot::after{content:'\\2713'}
.seenbtn.done{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.seenbtn.done:hover{color:var(--on-accent);border-color:var(--accent)}
.attn-all{margin-top:6px}
/* Standing orders — broadcast to every buddy detail (agents + Dave) */
.standing-order{margin:10px 0 4px;padding:10px 12px;border-radius:10px;border:1px solid var(--amber-bd);
  background:var(--amber-bg);font-size:13.5px;line-height:1.45;color:var(--amber-tx)}
.standing-order.critical{border-color:var(--amber-bd)}
.standing-order b{color:var(--amber-hi)}
.standing-order a{color:var(--accent-hi)}
.standing-order .so-date{display:block;margin-top:4px;font-size:11px;color:var(--muted)}
.standing-order{position:relative}
.so-close{position:absolute;top:4px;right:6px;background:none;border:none;color:var(--amber-hi);
  font-size:17px;line-height:1;padding:5px 7px;cursor:pointer;opacity:.6}
.so-close:hover{opacity:1}
.notes{width:100%;min-height:120px;background:var(--bg);border:1px solid var(--border);border-radius:12px;
  color:var(--text);font:inherit;font-size:14.5px;line-height:1.6;padding:13px 15px;resize:vertical}
.notes:focus{outline:none;border-color:var(--accent)}
/* Gentle pulse on the dump field's placeholder — bright to dim, bright to dim */
@keyframes placeholder-pulse{0%,100%{opacity:1}50%{opacity:.35}}
#bp-ingest::placeholder{animation:placeholder-pulse 3.2s ease-in-out infinite}
#bp-ingest::-webkit-input-placeholder{animation:placeholder-pulse 3.2s ease-in-out infinite}
.dump-pending-badge{display:inline-block;font-size:10px;font-weight:600;color:#9a6a00;background:#fff3cd;border:1px solid #e6c200;border-radius:4px;padding:1px 6px;margin-left:8px;vertical-align:middle}
#ingest-status.dumped-ok{color:var(--grn-tx)}
/* ---------- Secret nerd settings (tap build number 5x to unlock) ---------- */
#nerd-modal{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center}
#nerd-modal .nd-backdrop{position:absolute;inset:0;background:rgba(0,0,0,.5)}
#nerd-modal .nd-box{position:relative;background:var(--panel);border-radius:14px;padding:22px;width:min(92vw,360px);box-shadow:0 12px 40px rgba(0,0,0,.35)}
#nerd-modal .nd-box h2{margin:0 0 4px;font-size:17px}
#nerd-modal .nd-sub{color:var(--muted);font-size:13px;margin:0 0 8px}
#nerd-modal .nd-row{margin:16px 0}
#nerd-modal .nd-row label{display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px}
#nerd-modal .nd-row label b{font-variant-numeric:tabular-nums}
#nerd-modal input[type=range]{width:100%;accent-color:var(--accent)}
#nerd-modal .nd-actions{display:flex;gap:10px;margin-top:18px}
#nerd-modal .nd-actions button{flex:1;font-size:14px;font-weight:600;padding:10px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text);cursor:pointer}
#nerd-modal .nd-close{background:var(--accent)!important;color:#fff!important;border:none!important}
.fineprint{font-size:12.5px;color:var(--faint);margin-top:8px;line-height:1.5}
.bp-empty{color:var(--muted);font-size:14px}
/* Parent one-liner link — name + kind, no tile */
.bp-parent-link{display:inline-block;font-size:15px;font-weight:600;color:var(--accent);cursor:pointer;text-decoration:none;padding:6px 0}
.bp-parent-link:hover{text-decoration:underline}
.bp-parent-kind{font-weight:400;color:var(--muted);font-size:13px}
.proj-row[data-plan]{cursor:pointer}
.proj-row[data-plan]:hover{background:var(--hover)}
.bp-tree-wrap{border:1px solid var(--border2);border-radius:12px;background:var(--bg);overflow:auto;position:relative;height:420px;cursor:grab}
.bp-tree-wrap.panning{cursor:grabbing}
.bp-mini-zoom{position:absolute;top:8px;right:8px;z-index:5;display:flex;gap:4px}
.bp-mini-zoom button{background:color-mix(in srgb, var(--panel) 94%, transparent);border:1px solid var(--border);color:var(--text);border-radius:8px;width:28px;height:28px;font-size:14px;cursor:pointer}
.bp-mini-zoom button:hover{border-color:var(--accent)}
.linkbtn{background:none;border:0;color:var(--accent);font:inherit;font-size:12.5px;cursor:pointer;padding:0}
.linkbtn:hover{text-decoration:underline}
.node{position:relative;width:max-content;min-width:180px;max-width:320px;flex-shrink:0}
#treezoom .node .name{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#treezoom .node .desc{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
/* Fix: flex-centered org tree overflows to negative x-coords on narrow screens, which widens the
   layout viewport and pushes position:fixed UI (zoombar) partly off-screen. max-content + auto
   margins keeps the centered look when it fits, and overflows only rightward (scrollable) when not. */
.tree{justify-content:flex-start;width:max-content;margin:0 auto}
/* ---- tree node drag-to-reparent (pointer-based; mouse + touch) ---- */
#treezoom .node[data-buddy]:not(.root){touch-action:none;cursor:grab}
#treezoom .node[data-buddy]:not(.root):active{cursor:grabbing}
#treezoom .node.drag-src{opacity:.35}
#treezoom .node.drag-armed{box-shadow:0 0 0 2px var(--accent),0 8px 24px rgba(0,0,0,.4)}
#treezoom .node.drop-invalid{outline:2px dashed #e0533d;outline-offset:3px}
.node-drag-ghost{position:fixed;left:0;top:0;z-index:9999;pointer-events:none;width:284px;opacity:.94;
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
    # Voice catalog (voice-catalog.json) -> baked into the dashboard.
    # EXTENSIBLE: to add voices, edit voice-catalog.json (id, name, desc,
    # gender, accent, tone) and rebuild. Future: user voice sharing/exchange
    # builds on this file format (pinned 2026-10-12).
    _voices = json.load(open(f"{HERE}/voice-catalog.json", encoding="utf-8"))
    voices_js = json.dumps(_voices)
    # Persona roster (~/workspace/persona-roster.md) -> baked into the dashboard
    # so the info-panel persona picker offers the full 116-entry list.
    import re as _re
    _roster = []
    for _line in open(f"{HERE}/../../persona-roster.md", encoding="utf-8"):
        _m = _re.match(r'\d+\.\s+\*\*(.+?)\*\*\s+[—–-]\s+(.*)', _line.strip())
        if _m:
            _name = _m.group(1).strip()
            _rest = _m.group(2).strip()
            # Extract the quoted voice sample (Dave's one-liner) from the front
            _qm = _re.match(r'"([^"]+)"\s*(.*)', _rest)
            if _qm:
                _quote, _blurb = _qm.group(1).strip(), _qm.group(2).strip()
            else:
                _quote, _blurb = "", _rest
            _roster.append({"name": _name, "quote": _quote, "blurb": _blurb})
    roster_js = json.dumps(_roster)
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
const PERSONA_ROSTER = PERSONA_ROSTER_JSON;
const VOICE_CATALOG = [{"id": "avocado_v2:MAI_01", "name": "Aria", "desc": "Feminine, American, Friendly, Warm"}, {"id": "avocado_v2:MAI_03", "name": "Helio", "desc": "Masculine, American, Gentle, Reassuring"}, {"id": "avocado_v2:Karen", "name": "Regal Icicle", "desc": "Feminine, American, Sharp, Menacing"}, {"id": "avocado_v2:nova", "name": "Deadpan Gumball", "desc": "Feminine, American, Friendly, Sarcastic"}, {"id": "avocado_v2:vincent", "name": "Gruff Brick", "desc": "Masculine, American, Direct, Blunt"}, {"id": "avocado_v2:bud", "name": "Neighborly Syrup", "desc": "Masculine, Southern American, Deep, Slow"}, {"id": "avocado_v2:isabella", "name": "Soothing Ribbon", "desc": "Feminine, British, Soothing, Polished"}, {"id": "avocado_v2:magnus", "name": "Boomy Mountain", "desc": "Masculine, British, Deep, Regal"}, {"id": "avocado_v2:paloma", "name": "Lilting Swing", "desc": "Feminine, British, Friendly, Light"}, {"id": "avocado_v2:ronan", "name": "Fluid Hammock", "desc": "Masculine, American, Friendly, Casual"}, {"id": "avocado_v2:lumi", "name": "Bubbly Pompom", "desc": "Feminine, Finnish, Bubbly, Energetic"}, {"id": "avocado_v2:rumi", "name": "Cheeky Bubble", "desc": "Feminine, American, Bubbly, Sarcastic"}, {"id": "avocado_v2:mudiwa", "name": "Dramatic Canyon", "desc": "Masculine, Zimbabwean, Deep, Dramatic"}, {"id": "avocado_v2:myrtle", "name": "Homespun Basket", "desc": "Feminine, American, Reedy, Kindly"}, {"id": "avocado_v2:hubert", "name": "Loud Gravel", "desc": "Masculine, New York, Loud, Raspy"}, {"id": "avocado_v2:conor", "name": "Polished Coin", "desc": "Masculine, Irish, Relaxed, Professional"}, {"id": "avocado_v2:miles", "name": "Satiny Moon", "desc": "Masculine, American, Deep, Soothing"}, {"id": "avocado_v2:briggs", "name": "Husky Campfire", "desc": "Masculine, Southern American, Husky, Warm"}, {"id": "avocado_v2:chip", "name": "Warm Pebble", "desc": "Masculine, American, Warm, Professional"}, {"id": "avocado_v2:lady_macbeth", "name": "Coppery Crown", "desc": "Feminine, Scottish, Commanding, Regal"}, {"id": "avocado_v2:melody", "name": "Dynamic Sparkler", "desc": "Feminine, American, Confident, Dynamic"}, {"id": "avocado_v2:marisol", "name": "Zippy Cork", "desc": "Feminine, American, Zippy, Warm"}, {"id": "avocado_v2:atlas", "name": "Burnished Trophy", "desc": "Masculine, Australian, Deep, Dramatic"}, {"id": "avocado_v2:casper", "name": "Confident Trumpet", "desc": "Masculine, American, Confident, Storyteller"}, {"id": "avocado_v2:ElvenWizard", "name": "Ethereal Star", "desc": "Neutral, American, Otherworldly, Mysterious"}, {"id": "avocado_v2:TruthTeller", "name": "Wise Lighthouse", "desc": "Masculine, American, Calm, Wise"}, {"id": "avocado_v2:Vanessa", "name": "Cheerful Sunflower", "desc": "Feminine, American, Bright, Friendly"}, {"id": "avocado_v2:Lily", "name": "Mellow Saxophone", "desc": "Feminine, American, Smooth, Smoky"}, {"id": "avocado_v2:Twenty", "name": "Bold Flag", "desc": "Masculine, American, Heroic, Bold"}, {"id": "avocado_v2:Caitlin", "name": "Heroic Bugle", "desc": "Feminine, American, Heroic, Confident"}]; // 116-entry persona list, baked at build time
const byId = Object.fromEntries(BUDDIES.map(b => [b.id, b]));
const ROOT_ID = 'astro'; // chief of staff sits at the root of the tree
BUDDIES.forEach(b => { (b.links || []).forEach(lid => { const t = byId[lid]; if (t && lid !== b.id) { (t.linkedBy = t.linkedBy || []).push(b.id); } }); });
function buddyImageUrl(b, prefix){ if(!b) return null; if(b.image) return b.image; return (prefix || '') + 'avatars/' + b.id + '.jpg'; }
function buddyDisplayIcon(b){ try { if (window.S && S.iconOverrides && S.iconOverrides[b.id]) return S.iconOverrides[b.id]; } catch(e){} return b.icon || ''; }
function setBuddyFavicon(icon, imageUrl){
  function apply(url){
    let l = document.querySelector('link[rel="icon"]');
    if(!l){ l = document.createElement('link'); l.rel = 'icon'; document.head.appendChild(l); }
    l.type = 'image/png'; l.href = url;
    let t = document.querySelector('link[rel="apple-touch-icon"]');
    if(!t){ t = document.createElement('link'); t.rel = 'apple-touch-icon'; document.head.appendChild(t); }
    t.href = url;
  }
  function fromEmoji(e){
    try{
      const c = document.createElement('canvas'); c.width = c.height = 64;
      const x = c.getContext('2d');
      x.font = '48px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif';
      x.textAlign = 'center'; x.textBaseline = 'middle';
      x.fillText(e || '?', 32, 36);
      apply(c.toDataURL('image/png'));
    }catch(err){}
  }
  if(imageUrl){
    const img = new Image();
    img.onload = function(){
      try{
        const c = document.createElement('canvas'); c.width = c.height = 64;
        const x = c.getContext('2d');
        const s = Math.min(img.width, img.height);
        x.drawImage(img, (img.width - s)/2, (img.height - s)/2, s, s, 0, 0, 64, 64);
        apply(c.toDataURL('image/png'));
      }catch(err){ fromEmoji(icon); }
    };
    img.onerror = function(){ fromEmoji(icon); };
    img.src = imageUrl;
  } else fromEmoji(icon);
}
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
  const dismissed = S.dismissedOrders || [];
  return STANDING_ORDERS.filter(o => dismissed.indexOf(o.id) < 0).map(o => {
    const link = o.href ? ' <a href="'+o.href+'" target="_blank" rel="noopener">Standing orders</a> · <a href="AGENTS.md" target="_blank" rel="noopener">AGENTS.md</a>' : '';
    return '<div class="standing-order'+(o.critical?' critical':'')+'" data-order="'+o.id+'"><button type="button" class="so-close" data-close-order="'+o.id+'" aria-label="Dismiss memo" title="Dismiss memo">\u00d7</button><b>'+(o.critical?'Critical memo':'Memo')+'</b> — '+escHtml(o.text)+link+'<span class="so-date">'+escHtml(o.date||'')+'</span></div>';
  }).join('');
}
const kidsOf = {};
function effParent(b){ if (S.parents && b.id in S.parents) return S.parents[b.id]; return b.parent; }
function isDormant(bid){ return !!(S.dormant && S.dormant[bid]); }
function setDormant(bid, val){
  if (!S.dormant || typeof S.dormant !== 'object') S.dormant = {};
  if (val) S.dormant[bid] = true; else delete S.dormant[bid];
  save(); renderBuddy(bid); renderNav(); refreshViews();
}
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
S.zoomOrph = S.zoomOrph || 100;
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
function effAka(b){
  if (S.aka && Array.isArray(S.aka[b.id])) return S.aka[b.id];
  return b.aka || [];
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
function unseenItems(b){ if (isDormant(b.id)) return []; return (b.attention || []).filter(a => !S.seen[a.id]); }
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
    : '<b title="'+escHtml(c.repo ? 'GitHub repo: davedellaquila/'+c.repo : 'No repo linked')+'">'+escHtml(dispName(c))+'</b>').join(' <span style="color:var(--faint)">/</span> ');
}
function escHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
// Converts URLs in already-escaped HTML text into clickable links
function linkify(escaped){
  return escaped.replace(/(https?:\/\/[^\s<>"']+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
}
const VIEW_DEFS = [
  ['tree','Atlas','▦'],
  ['projects','Projects','☰'],
  ['plans','Business Plans','💼'],
  ['manifest','Manifest','✓'],
  ['project','Homepage','🏠'],
  ['changelog','Change Log','🕘'],
  ['releases','Release Notes','🎁'],
];
const VIEW_TIPS = {
  tree: 'Atlas — seven lenses on your buddy hierarchy. Tap the pill to switch views. Click a node to open its details. Drag the background to pan, scroll to zoom. Drag a node onto another node to reparent it.',
  projects: 'Projects list — every buddy in hierarchy order with status. Click a tile to filter by attention status. Click the chevron to expand/collapse sections.',
  plans: 'Business Plans — real-world ventures as cards. Click a status tile to filter. Each card links to its mission statement and related buddies.',
  manifest: 'New-Project Manifest — the checklist every new buddy gets. Click AUTOMATIC or PLANNED tiles to filter the steps.',
  project: 'Homepage — loads the selected buddy homepage full-bleed in the main view. Clicking a buddy with a homepage swaps it; clicking one without keeps the current page.',
  changelog: 'Change Log — history of everything that changed. Click a tile to filter by change type. Click a row to open the changed buddy.',
  releases: 'Release Notes — what shipped, newest first. New since you last looked on top, earlier history below.',
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
  return (id && byId[id]) ? id : ROOT_ID;
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
    + '<h2>Change Log</h2>'
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
  const views = getViewOrder().map(id => VIEW_DEFS.find(v => v[0] === id)).filter(Boolean).filter(([v]) => isViewVisible(v));
  document.getElementById('view-nav').innerHTML = views.map(([v,l,ic]) =>
    '<button class="navbtn'+(S.view===v?' sel':'')+'" data-view="'+v+'" title="'+(VIEW_TIPS[v]||l)+'"><span class="nic">'+ic+'</span>'+l+'</button>').join('');
  const q = (document.getElementById('buddy-search').value || '').toLowerCase().trim();
  const words = q.split(/\s+/).filter(Boolean);
  let h = '';
  function matches(b){
    if (!words.length) return true;
    const hay = (dispName(b) + ' ' + (b.name || '') + ' ' + (b.tagline || '') + ' ' + effAka(b).join(' ')).toLowerCase();
    return words.every(w => hay.includes(w));
  }
  function row(id, depth){
    const b = byId[id]; if(!b) return;
    if (!S.navCollapsed || typeof S.navCollapsed !== 'object') S.navCollapsed = {};
    if (words.length && !matches(b)) { (kidsOf[id] || []).forEach(c => row(c.id, depth+1)); return; }
    const un = descUnseen(id);
    const kind = b.kind === 'root' ? 'root' : (b.parent === ROOT_ID ? 'direct' : b.kind);
    const kids = kidsOf[id] || [];
    const hasKids = kids.length > 0;
    const collapsed = hasKids && !words.length && !!S.navCollapsed[id];
    h += '<button class="brow'+((S.projectId===id || S.sel==='buddy:'+id)?' sel':'')+(un?' has-unseen':'')+(isDormant(id)?' dormant':'')+'" data-buddy="'+id+'"'
      + ' draggable="'+(id===ROOT_ID?'false':'true')+'"'
      + ' style="padding-left:'+(8+depth*16)+'px" title="'+escHtml(b.tagline||'')+'">'
      + (hasKids ? '<span class="ctog has-kids'+(collapsed?' collapsed':'')+'" data-ctog="'+id+'" title="'+(collapsed?'Expand':'Collapse')+' \u2014 Shift+click applies to the whole subtree"><i class="chev">\u203a</i></span>' : '')
      + '<span class="bdot"></span><span class="bicon">'+escHtml(b.icon||'')+'</span><span class="bname">'+escHtml(dispName(b))+'</span>'
      + '<span class="bkind">'+kind+'</span>'
      + '<span class="binfo" data-buddy-info="'+id+'" title="Open '+escHtml(dispName(b))+' details" style="margin-left:auto;padding:2px 6px;opacity:0;transition:opacity 0.15s;cursor:pointer" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0">\u24d8</span></button>';
    if (!collapsed) kids.forEach(c => row(c.id, depth+1));
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
    '<button class="brow prow'+(S.sel==='plan:'+p.id?' sel':'')+'" data-plan="'+p.id+'" style="padding-left:8px">'
    + '<span class="bicon">'+escHtml(p.icon||'')+'</span><span class="bname pname">'+escHtml(p.name)+'</span></button>').join('');
  watchScrollPos('sidebar', document.getElementById('sidebar'));
  restoreScrollPos('sidebar', document.getElementById('sidebar'));
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
  {id:'ingest', label:'Dump box'},
  {id:'attention', label:'Needs your attention'},
  {id:'reports', label:'Direct reports'},
  {id:'siblings', label:'Peers'},
  {id:'parent', label:'Parent'},
  {id:'links', label:'Linked buddies'},
  {id:'photos', label:'Photos'},
  {id:'tree', label:'The Buddy Tree'},
  {id:'artifacts', label:'Artifacts'},
  {id:'plans', label:'Business plans'},
  {id:'notes', label:'Private notes'},
  {id:'shared', label:'Shared notes'},
  {id:'mission', label:'About'},
  {id:'aka', label:'A.K.A.'},
  {id:'persona', label:'Persona'},
  {id:'homepage', label:'Homepage URL'},
];
function getFieldOrder(){
  if (!S.fieldOrder || !Array.isArray(S.fieldOrder)) S.fieldOrder = FIELD_DEFS.map(f => f.id);
  // One-time migration (2026-10-12): About moved to bottom, notes fields right above it;
  // parent/siblings/links added to the orderable fields.
  // Reset stored order if it matches a previous default so the new layout applies.
  const oldDefaults = [
    ['ingest','attention','mission','aka','reports','homepage','photos','tree','artifacts','plans','notes','shared'],
    ['ingest','attention','aka','reports','homepage','photos','tree','artifacts','plans','notes','shared','mission'],
    ['ingest','attention','aka','reports','siblings','parent','links','homepage','photos','tree','artifacts','plans','notes','shared','mission'],
  ];
  if (oldDefaults.some(d => JSON.stringify(S.fieldOrder) === JSON.stringify(d))) S.fieldOrder = FIELD_DEFS.map(f => f.id);
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
  // Collapse state is global per section (not per buddy): collapsing Artifacts
  // on one buddy keeps it collapsed everywhere.
  home.querySelectorAll('.bp-sec[data-field] > h3').forEach(h3 => {
    if (h3.querySelector('.secarrow')) return;
    const sec = h3.parentElement;
    const fid = sec.dataset.field;
    const arrow = document.createElement('span');
    arrow.className = 'secarrow';
    arrow.textContent = '\u203a';
    h3.insertBefore(arrow, h3.firstChild);
    const grip = document.createElement('span');
    grip.className = 'secgrip';
    grip.textContent = '\u22ee\u22ee';
    grip.title = 'Drag to reorder sections';
    h3.appendChild(grip);
    if (S.secCollapsed[fid]) sec.classList.add('collapsed');
    h3.title = 'Click to collapse/expand — Shift+click applies to all sections';
    h3.addEventListener('click', e => {
      if (e.target.closest('.info-tip')) return;
      if (e.target.closest('.secgrip')) return; // grip drags; never toggles collapse
      const willCollapse = !sec.classList.contains('collapsed');
      if (e.shiftKey) {
        // Shift-click: apply to all sections
        home.querySelectorAll('.bp-sec[data-field]').forEach(s2 => {
          s2.classList.toggle('collapsed', willCollapse);
          S.secCollapsed[s2.dataset.field] = willCollapse;
        });
      } else {
        sec.classList.toggle('collapsed');
        S.secCollapsed[fid] = sec.classList.contains('collapsed');
      }
      save();
    });
  });
}
/* ---------- direct section reorder: drag the ⋮⋮ grip on a section title ----------
   Pointer-based (mouse + touch). Live-reorders .bp-sec elements inside .bp-wrap;
   on release the DOM order is persisted to S.fieldOrder. The grip uses pointer
   capture so the follow-up click lands on the grip, which never toggles collapse. */
const secDrag = { cand: null, drag: null };
function applySectionDrag(){
  const home = document.getElementById('buddy-home');
  if (!home) return;
  home.querySelectorAll('.bp-sec[data-field] > h3 .secgrip').forEach(grip => {
    if (grip.dataset.sdrag) return;
    grip.dataset.sdrag = '1';
    grip.addEventListener('pointerdown', e => {
      if (e.button !== undefined && e.button !== 0) return;
      if (e.isPrimary === false) return;
      e.preventDefault(); e.stopPropagation();
      secDrag.cand = { grip: grip, sec: grip.closest('.bp-sec'), y0: e.clientY, pid: e.pointerId };
    });
  });
}
(function initSectionDrag(){
  function secsOf(sec){
    const home = document.getElementById('buddy-home');
    if (!home) return [];
    return Array.from(home.querySelectorAll('.bp-sec[data-field]')).filter(s => s !== sec);
  }
  window.addEventListener('pointermove', e => {
    if (secDrag.drag) {
      if (e.pointerId !== secDrag.drag.pid) return;
      const d = secDrag.drag;
      const wrap = d.sec.parentElement;
      if (!wrap) return;
      const build = wrap.querySelector(':scope > .bp-build');
      let target = null;
      for (const s of secsOf(d.sec)) {
        const r = s.getBoundingClientRect();
        if (e.clientY < r.top + r.height / 2) { target = s; break; }
      }
      if (target) wrap.insertBefore(d.sec, target);
      else if (build) wrap.insertBefore(d.sec, build);
      else wrap.appendChild(d.sec);
      e.preventDefault();
      return;
    }
    const c = secDrag.cand;
    if (c && e.pointerId === c.pid) {
      if (Math.abs(e.clientY - c.y0) > 6) {
        secDrag.drag = c; secDrag.cand = null;
        c.sec.classList.add('sec-dragging');
        try { c.grip.setPointerCapture(c.pid); } catch (err) {}
      }
    }
  }, { passive: false });
  function end(e){
    const d = secDrag.drag;
    if (d && e.pointerId === d.pid) {
      d.sec.classList.remove('sec-dragging');
      const wrap = d.sec.parentElement;
      if (wrap) {
        const order = Array.from(wrap.querySelectorAll(':scope > .bp-sec[data-field]')).map(s => s.dataset.field);
        const cur = getFieldOrder();
        const seen = new Set(order);
        S.fieldOrder = order.concat(cur.filter(id => !seen.has(id)));
        save();
      }
      secDrag.drag = null;
      return;
    }
    const c = secDrag.cand;
    if (c && e.pointerId === c.pid) secDrag.cand = null;
  }
  window.addEventListener('pointerup', end);
  window.addEventListener('pointercancel', end);
})();
function applyFieldOrder(){
  const home = document.getElementById('buddy-home');
  if (!home) return;
  // Keep sections inside .bp-wrap (before .bp-build) so .bp-sticky-head can stick
  const wrap = home.querySelector('.bp-wrap') || home;
  const build = wrap.querySelector('.bp-build');
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
function isViewVisible(vid){
  if (!S.viewHidden) S.viewHidden = {};
  return !S.viewHidden[vid];
}
const SETTING_DEFS = [
  {id:'hideBuddyWord', label:'Hide the word “Buddy” in names', type:'bool', def:false},
  {id:'autoOpenPanel', label:'Always open detail panel on buddy click', type:'bool', def:false, tip:'When off (default), the panel auto-opens in every view EXCEPT Homepage — there, use the \u24d8 icon. When on, the panel opens on every click in every view.'},
  {id:'attnEffect', label:'Attention header effect', type:'choice', options:['pulse','glow','shake','blink','wiggle','bounce','swing','none'], def:'pulse', advanced:true, tip:'How the \u201cNeeds your attention\u201d section header grabs your eye when items are waiting.'},
  {id:'nbSheetWidth', label:'New buddy sheet width', type:'number', def:560, min:320, max:900, advanced:true, tip:'Fixed width of the New Buddy bottom sheet, in pixels. Height follows the content; drag the grab handle to resize vertically.', unit:'px'},
  {id:'shiftLeftAction', label:'Shift+← action', type:'choice', options:['promote','go to parent','nothing'], def:'promote', advanced:true, tip:'What Shift+Left arrow does for the selected buddy. Promote moves it up one level; Go to parent just navigates there.'},
  {id:'fontScale', label:'Text size', type:'slider', def:100, min:80, max:130, step:5, advanced:true, tip:'Scales text and UI throughout the app — like the text-size slider on iPhone and Watch.', unit:'%'},
];
function getSetting(id){
  const def = SETTING_DEFS.find(s => s.id === id);
  if (S[id] === undefined) return def ? def.def : undefined;
  return S[id];
}
function applyFontScale(){
  const v = getSetting('fontScale');
  const scale = (typeof v === 'number' && !isNaN(v) ? v : 100) / 100;
  document.body.style.zoom = scale === 1 ? '' : String(scale);
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
    + SETTING_DEFS.filter(s => !s.advanced).map(s => {
    const val = getSetting(s.id);
    if (s.type === 'bool') return '<label class="fset-check"><input type="checkbox" data-setting="' + s.id + '"' + (val ? ' checked' : '') + '> <span>' + s.label + '</span></label>';
    if (s.type === 'choice') return '<label class="fset-choice"><span>' + s.label + (s.tip ? ' <span class="info-tip" data-tip="' + escHtml(s.tip) + '">\\u24d8</span>' : '') + '</span><select data-setting="' + s.id + '">'
      + s.options.map(o => '<option value="' + o + '"' + (val === o ? ' selected' : '') + '>' + o.charAt(0).toUpperCase() + o.slice(1) + '</option>').join('') + '</select></label>';
    return '';
  }).join('');
  wireThemePicks(sdiv);
  sdiv.querySelectorAll('[data-setting]').forEach(el => {
    el.addEventListener('change', () => {
      S[el.dataset.setting] = (el.type === 'checkbox') ? el.checked : el.value; save();
      show(S.sel, false);
    });
  });
  // Advanced settings
  const adv = document.getElementById('fset-advanced');
  if (adv) {
    adv.innerHTML = SETTING_DEFS.filter(s => s.advanced).map(s => {
      const val = getSetting(s.id);
      if (s.type === 'number') return '<label class="fset-choice"><span>' + s.label + (s.tip ? ' <span class="info-tip" data-tip="' + escHtml(s.tip) + '">\\u24d8</span>' : '') + '</span><span style="display:flex;align-items:center;gap:6px;white-space:nowrap"><input type="number" data-setting="' + s.id + '" value="' + val + '"' + (s.min !== undefined ? ' min="' + s.min + '"' : '') + (s.max !== undefined ? ' max="' + s.max + '"' : '') + ' style="width:90px">' + (s.unit ? '<span class="fineprint">' + escHtml(s.unit) + '</span>' : '') + '</span></label>';
      if (s.type === 'choice') {
        const rowHtml = '<label class="fset-choice"><span>' + s.label + (s.tip ? ' <span class="info-tip" data-tip="' + escHtml(s.tip) + '">\\u24d8</span>' : '') + '</span><select data-setting="' + s.id + '">'
          + s.options.map(o => '<option value="' + o + '"' + (val === o ? ' selected' : '') + '>' + o.charAt(0).toUpperCase() + o.slice(1) + '</option>').join('') + '</select></label>';
        if (s.id === 'attnEffect') return rowHtml + '<div class="attnfx-preview"><div class="bp-sec fx-' + val + '" data-field="attention" id="attnfx-demo"><h3>Needs your attention <span class="attn-count">(3)</span></h3></div><p class="fineprint">Live preview \\u2014 this is what the header will do.</p></div>';
        return rowHtml;
      }
      if (s.type === 'slider') return '<label class="fset-choice"><span>' + s.label + (s.tip ? ' <span class="info-tip" data-tip="' + escHtml(s.tip) + '">\\u24d8</span>' : '') + '</span><span style="display:flex;align-items:center;gap:8px;white-space:nowrap;min-width:180px;flex:1"><span class="fineprint" style="font-size:11px">A</span><input type="range" data-setting="' + s.id + '" value="' + val + '"' + (s.min !== undefined ? ' min="' + s.min + '"' : '') + (s.max !== undefined ? ' max="' + s.max + '"' : '') + (s.step !== undefined ? ' step="' + s.step + '"' : '') + ' style="flex:1;accent-color:var(--accent)"><span class="fineprint" style="font-size:15px">A</span><span class="fineprint" data-scale-val="' + s.id + '" style="min-width:42px;text-align:right">' + val + (s.unit || '') + '</span></span></label>';
      return '';
    }).join('');
    adv.querySelectorAll('[data-setting]').forEach(el => {
      const onSliderInput = () => {
        const def = SETTING_DEFS.find(s => s.id === el.dataset.setting);
        let v = parseInt(el.value, 10);
        if (isNaN(v)) v = def ? def.def : 100;
        if (def && def.min !== undefined) v = Math.max(def.min, v);
        if (def && def.max !== undefined) v = Math.min(def.max, v);
        S[el.dataset.setting] = v;
        const valEl = adv.querySelector('[data-scale-val="' + el.dataset.setting + '"]');
        if (valEl) valEl.textContent = v + (def && def.unit ? def.unit : '');
        applyFontScale();
      };
      if (el.type === 'range') {
        el.addEventListener('input', onSliderInput);
        el.addEventListener('change', () => { save(); });
        return;
      }
      el.addEventListener('change', () => {
        const def = SETTING_DEFS.find(s => s.id === el.dataset.setting);
        if (el.type === 'number') {
          let v = parseInt(el.value, 10);
          if (isNaN(v)) v = def ? def.def : 0;
          if (def && def.min !== undefined) v = Math.max(def.min, v);
          if (def && def.max !== undefined) v = Math.min(def.max, v);
          el.value = v;
          S[el.dataset.setting] = v; save();
        } else {
          S[el.dataset.setting] = el.value; save();
          if (el.dataset.setting === 'attnEffect') {
            const demo = document.getElementById('attnfx-demo');
            if (demo) demo.className = 'bp-sec fx-' + el.value;
          }
        }
      });
    });
  }
}
// ---- Develop tab: new-user simulation and pre-launch tools ----
let devBackup = null; // {buddies, byId, S} stashed while simulating a new user
function renderDevelopSection(){
  const dev = document.getElementById('fset-develop');
  if (!dev) return;
  const simulating = !!devBackup;
  const buildNum = '__BUILD__';
  dev.innerHTML = ''
    + '<label class="fset-check"><input type="checkbox" id="dev-empty-toggle"' + (simulating ? ' checked' : '') + '> <span><strong>Simulate new user</strong> — empty data file, as if opening the shared link fresh</span></label>'
    + '<div class="fineprint" style="margin:8px 0 12px">Build <span style="font-family:monospace">' + escHtml(String(buildNum)) + '</span> · ' + BUDDIES.length + ' buddies in this file</div>'
    + '<div style="display:flex;gap:10px;flex-wrap:wrap">'
    + '<button class="linkbtn" id="dev-clear-local" type="button">Clear this device\u2019s local data</button>'
    + '</div>'
    + '<p class="fineprint" style="margin-top:10px">Simulation never touches your real data — it stashes everything in memory and restores it when you toggle off. Reloading the page also exits simulation.</p>';
  dev.querySelector('#dev-empty-toggle').addEventListener('change', e => {
    setSimulateEmpty(e.target.checked);
    renderDevelopSection();
  });
  dev.querySelector('#dev-clear-local').addEventListener('click', () => {
    if (!confirm('Clear ALL local data on this device (settings, seen items, overrides)? The buddy file itself is untouched.')) return;
    try { localStorage.removeItem(LS_KEY); } catch (e) {}
    toast('Local data cleared — reloading.');
    setTimeout(() => location.reload(), 800);
  });
}
function setSimulateEmpty(on){
  if (on && !devBackup) {
    devBackup = {
      buddies: BUDDIES.slice(),
      byId: Object.assign({}, byId),
      S: JSON.parse(JSON.stringify(S)),
      sel: S.sel, view: S.view
    };
    BUDDIES.length = 0;
    for (const k in byId) delete byId[k];
    const fresh = {seen:{}, notes:{}, names:{}, parents:{}, zoom:100, zoomOrph:100, sel:'view:tree', view:'tree', theme:S.theme};
    for (const k in S) delete S[k];
    Object.assign(S, fresh);
    buildKids(); renderNav(); refreshViews(); applyFontScale();
    showBanner('dev-sim', '\\u{1F6A7} SIMULATING NEW USER — empty data file. <button class="linkbtn" id="dev-sim-exit" style="color:#fff;text-decoration:underline">Exit simulation</button>', true);
    const exit = document.getElementById('dev-sim-exit');
    if (exit) exit.addEventListener('click', () => { setSimulateEmpty(false); const t = document.querySelector('#dev-empty-toggle'); if (t) t.checked = false; });
    toast('New-user simulation on — your data is stashed safely.');
  } else if (!on && devBackup) {
    const b = devBackup; devBackup = null;
    b.buddies.forEach(x => BUDDIES.push(x));
    Object.assign(byId, b.byId);
    for (const k in S) delete S[k];
    Object.assign(S, b.S);
    hideBanner('dev-sim');
    buildKids(); renderNav(); refreshViews(); applyFontScale(); applyTheme();
    S.sel = b.sel; S.view = b.view;
    show(S.view, false);
    toast('Simulation off — your data is back.');
  }
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
  rz.addEventListener('pointerdown', e => {
    if (e.button !== undefined && e.button !== 0) return;
    if (e.isPrimary === false) return;
    e.preventDefault(); e.stopPropagation();
    try { rz.setPointerCapture(e.pointerId); } catch (err) {}
    const r = m.getBoundingClientRect(), sx = e.clientX, sy = e.clientY, pid = e.pointerId;
    const mv = ev => {
      if (ev.pointerId !== pid) return;
      m.style.width = Math.max(300, Math.min(window.innerWidth - 40, r.width + ev.clientX - sx)) + 'px';
      m.style.height = Math.max(220, Math.min(window.innerHeight - 40, r.height + ev.clientY - sy)) + 'px';
      m.style.maxHeight = 'none';
    };
    const up = ev => {
      if (ev.pointerId !== pid) return;
      rz.removeEventListener('pointermove', mv); rz.removeEventListener('pointerup', up); rz.removeEventListener('pointercancel', up);
      const rr = m.getBoundingClientRect();
      S.fsetGeom = Object.assign(S.fsetGeom || {}, {w: Math.round(rr.width), h: Math.round(rr.height)});
      save();
    };
    rz.addEventListener('pointermove', mv); rz.addEventListener('pointerup', up); rz.addEventListener('pointercancel', up);
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
      + '<div class="fset-cols">'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Main views</h3><p class="fineprint">Drag to reorder. Number keys 1–9 follow this order.</p><div id="vset-list"></div></section>'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Buddy fields</h3><p class="fineprint">Drag to reorder. Uncheck to hide.</p><div id="fset-list"></div></section>'
      + '</div>'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Advanced</h3><div id="fset-advanced"></div></section>'
      + '<section class="fset-sec"><h3 class="fset-sec-h">Develop</h3><p class="fineprint">Tools for preparing the app for new users. Nothing here affects your real data.</p><div id="fset-develop"></div></section>'
      + '</div>'
      + '<div class="fset-footer">'
      + '<div style="display:flex;gap:12px"><button class="linkbtn" id="fset-reset" title="Restore all settings to factory defaults">Reset defaults</button>'
      + '<button class="linkbtn" id="fset-update" title="Save current settings as the new factory defaults">Save as defaults</button></div>'
      + '<button id="fset-close" style="font-size:14px;font-weight:600;padding:8px 24px;border:none;border-radius:20px;background:var(--accent);color:#fff;cursor:pointer">Done</button></div>'
      + '<div class="fset-resize" id="fset-resize" title="Drag to resize"></div>';
    document.body.appendChild(m);
    initFsetChrome(m);
    m.querySelector('#fset-close').addEventListener('click', () => m.classList.remove('show'));
    m.querySelector('#fset-x').addEventListener('click', () => m.classList.remove('show'));
    renderSettingChecks();
    renderDevelopSection();
    m.querySelector('#fset-reset').addEventListener('click', () => {
      if (!confirm('Reset all settings to factory defaults?')) return;
      resetToFactory(); renderSettingChecks(); openFieldSettings();
      applySbWidth(); applyPanelWidth(); applyFontScale();
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
      + '<input type="checkbox" ' + (vis ? 'checked' : '') + ' data-vis="' + fid + '" title="Show/hide">'
      + '<span class="fl">' + def.label + '</span>'
      + '<span class="fh" style="margin-left:auto">\u22ee\u22ee</span></div>';
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
    // Auto-scroll the nearest scrollable ancestor while a drag hovers near its top/bottom edge.
    let scrollRaf = null, lastClientY = null;
    const stopAutoScroll = () => { if (scrollRaf) cancelAnimationFrame(scrollRaf); scrollRaf = null; lastClientY = null; };
    const scrollAncestor = () => {
      let sc = listEl.parentElement;
      while (sc && sc !== document.body && sc.scrollHeight <= sc.clientHeight + 1) sc = sc.parentElement;
      return (sc && sc !== document.body) ? sc : null;
    };
    const autoScrollStep = () => {
      scrollRaf = null;
      if (lastClientY == null || !dragEl) return;
      const sc = scrollAncestor();
      if (!sc) return;
      const rect = sc.getBoundingClientRect(), EDGE = 48;
      let dir = 0;
      if (lastClientY < rect.top + EDGE && sc.scrollTop > 0) dir = -1;
      else if (lastClientY > rect.bottom - EDGE && sc.scrollTop < sc.scrollHeight - sc.clientHeight) dir = 1;
      if (!dir) return;
      sc.scrollBy(0, dir * 10);
      scrollRaf = requestAnimationFrame(autoScrollStep);
    };
    const autoScrollTick = (clientY) => {
      lastClientY = clientY;
      if (!scrollRaf) scrollRaf = requestAnimationFrame(autoScrollStep);
    };
    const finish = () => {
      stopAutoScroll();
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
      row.addEventListener('dragend', () => { stopAutoScroll(); clearFsetDnD(listEl); dragEl = null; });
      row.addEventListener('dragover', e => {
        e.preventDefault(); e.dataTransfer.dropEffect = 'move';
        if (dragEl) { placeFsetInsert(listEl, e.clientY, dragEl); autoScrollTick(e.clientY); }
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
        autoScrollTick(t.clientY);
      }, {passive: false});
      handle.addEventListener('touchend', () => finish());
      handle.addEventListener('touchcancel', () => { stopAutoScroll(); clearFsetDnD(listEl); dragEl = null; });
    });
    listEl.addEventListener('dragover', e => {
      e.preventDefault();
      if (dragEl) { placeFsetInsert(listEl, e.clientY, dragEl); autoScrollTick(e.clientY); }
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
      const vvis = isViewVisible(vid);
      return '<div class="fset-row" draggable="true" data-vid="' + vid + '">'
        + '<input type="checkbox" ' + (vvis ? 'checked' : '') + ' data-vvis="' + vid + '" title="Show/hide">'
        + '<span class="fl">' + def[1] + '</span>'
        + '<span class="fh" style="margin-left:auto">\u22ee\u22ee</span></div>';
    }).join('');
    bindFsetListDnD(vlist, r => r.dataset.vid, (fromId, beforeId) => {
      S.viewOrder = reorderBefore(getViewOrder(), fromId, beforeId);
      save();
      renderNav();
      openFieldSettings();
    });
    vlist.querySelectorAll('[data-vvis]').forEach(cb => {
      cb.addEventListener('change', () => {
        if (!S.viewHidden) S.viewHidden = {};
        S.viewHidden[cb.dataset.vvis] = !cb.checked;
        save();
        renderNav();
      });
    });
  }
  m.classList.add('show');
  if (m._applyGeom) m._applyGeom();
}
function applyPanelWidth(){
  const vb = document.getElementById('view-buddy');
  if (vb && S.panelWidth) {
    const w = Math.min(S.panelWidth, 560);
    vb.style.width = w + 'px';
    document.documentElement.style.setProperty('--bpw', w + 'px');
  }
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
  let sx = null, sw = 0, sdrag = false, snapped = false;
  const SNAP_SHUT = 220; /* drag narrower than this → snap the panel closed */
  h.addEventListener('pointerdown', e => {
    sx = e.clientX; sw = vb.getBoundingClientRect().width; sdrag = false; snapped = false;
  });
  h.addEventListener('pointermove', e => {
    if (sx === null || snapped) return;
    if (!sdrag) {
      if (Math.abs(e.clientX - sx) < 6) return; /* tap slop: don't resize on a plain tap */
      sdrag = true;
      try { h.setPointerCapture(e.pointerId); } catch (err) {}
      e.preventDefault();
    }
    const raw = sw + (sx - e.clientX);
    if (raw < SNAP_SHUT) {
      /* Pushed through the threshold — snap shut instead of stopping at min width */
      snapped = true;
      sx = null;
      closeDetail();
      return;
    }
    const w = Math.min(560, Math.max(320, raw));
    vb.style.width = w + 'px';
    document.documentElement.style.setProperty('--bpw', w + 'px');
  });
  h.addEventListener('pointerup', e => {
    if (sx === null) return;
    sx = null;
    if (!sdrag || snapped) return;
    S.panelWidth = Math.round(vb.getBoundingClientRect().width);
    save();
  });
  h.addEventListener('dblclick', () => closeDetail());
}
function tileHtml(label, num, tint, sub, fkey, sel, tip){
  return '<div class="ptile' + (sel ? ' sel' : '') + '"' + (fkey ? ' data-tile="' + fkey + '"' : '') + (tip ? ' title="' + escHtml(tip) + '"' : '') + ' style="--tint:' + tint + ';flex:0 0 auto">'
    + '<div class="ptile-label">' + escHtml(label) + '</div>'
    + '<div class="ptile-num">' + escHtml(String(num)) + '</div>'
    + '<div class="ptile-sub">' + escHtml(sub) + '</div></div>';
}
let projFilter = null, clFilter = null, planFilter = null, manifestFilter = null, statusFilter = null, projSearch = '', projViewMode = 'hier', projStickObs = null;
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
  const allPlans = (typeof PLANS !== 'undefined' && PLANS) || [];
  const plans = allPlans.filter(p => (p.buddies || []).includes(b.id));
  const attnItems = (b.attention || []).filter(a => !S.seen[b.id + ':' + (a.id || a.text)]);
  let stats = '';
  if (attnItems.length) stats += '<span class="hp-stat"><b>' + attnItems.length + '</b> need attention</span>';
  if (kids.length) stats += '<span class="hp-stat"><b>' + kids.length + '</b> sub-buddies</span>';
  if (plans.length) stats += '<span class="hp-stat"><b>' + plans.length + '</b> plans</span>';
  if (arts.length) stats += '<span class="hp-stat"><b>' + arts.length + '</b> artifacts</span>';
  let h = '<style>'
    + '.hp{max-width:1080px;margin:0 auto;padding:36px 28px 56px;color:var(--text);font-family:inherit}'
    + '.hp-grid{display:grid;gap:22px;grid-template-columns:minmax(0,1fr) 340px;grid-template-areas:"head head" "main rail" "dump dump"}'
    + '.hp-head{grid-area:head;display:flex;align-items:center;gap:20px;min-width:0}'
    + '.hp-icon{width:78px;height:78px;flex:none;border-radius:24px;background:var(--panel);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:42px;box-shadow:var(--shadow-soft)}'
    + '.hp-headtxt{min-width:0}'
    + '.hp-name{margin:0;font-size:30px;letter-spacing:-0.02em;line-height:1.15;overflow-wrap:break-word}'
    + '.hp-tagline{margin:8px 0 0;color:var(--muted);font-size:15px;line-height:1.55;max-width:660px}'
    + '.hp-stats{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}'
    + '.hp-stat{font-size:12.5px;color:var(--muted);background:var(--panel);border:1px solid var(--border);border-radius:999px;padding:4px 12px;white-space:nowrap}'
    + '.hp-stat b{color:var(--text)}'
    + '.hp-main{grid-area:main;min-width:0;display:flex;flex-direction:column;gap:22px}'
    + '.hp-rail{grid-area:rail;min-width:0;display:flex;flex-direction:column;gap:22px}'
    + '.hp-card{background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:20px 22px;min-width:0}'
    + '.hp-kicker{margin:0 0 6px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:var(--muted)}'
    + '.hp-mission{margin:8px 0 0;font-size:15px;line-height:1.7;overflow-wrap:break-word}'
    + '.hp-attn{border-color:var(--amber-bd)}'
    + '.hp-attn .hp-kicker{color:var(--amber-tx)}'
    + '.hp-aitem{display:flex;gap:10px;padding:10px 0;font-size:14px;line-height:1.5}'
    + '.hp-aitem + .hp-aitem{border-top:1px solid var(--border)}'
    + '.hp-adot{color:var(--amber);flex:none;font-size:11px;line-height:2}'
    + '.hp-atext{min-width:0;overflow-wrap:break-word}'
    + '.hp-adate{color:var(--faint);font-size:12px;margin-top:3px}'
    + '.hp-more{font-size:12.5px;color:var(--muted);margin:10px 0 0}'
    + '.hp-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}'
    + '.hp-chip{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:8px 12px;font-size:13.5px;white-space:nowrap}'
    + '.hp-plan{display:flex;gap:12px;padding:14px 0;min-width:0}'
    + '.hp-plan + .hp-plan{border-top:1px solid var(--border)}'
    + '.hp-picon{font-size:26px;flex:none;line-height:1.2}'
    + '.hp-pbody{min-width:0}'
    + '.hp-pname{font-weight:650;font-size:15px;overflow-wrap:break-word}'
    + '.hp-pill{display:inline-block;vertical-align:1px;font-size:11px;font-weight:700;background:var(--wash);color:var(--accent-hi);border-radius:999px;padding:3px 10px;margin-left:8px;white-space:nowrap}'
    + '.hp-pdesc{margin:6px 0 0;color:var(--muted);font-size:13.5px;line-height:1.55;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:break-word}'
    + '.hp-pdoc{display:inline-block;margin-top:8px;font-size:13px;color:var(--accent);text-decoration:none}'
    + '.hp-pdoc:hover{text-decoration:underline}'
    + '.hp-art{display:flex;align-items:center;gap:10px;padding:10px 0;font-size:14.5px;min-width:0}'
    + '.hp-art + .hp-art{border-top:1px solid var(--border)}'
    + '.hp-art a{color:var(--accent);text-decoration:none;overflow-wrap:break-word;min-width:0}'
    + '.hp-art a:hover{text-decoration:underline}'
    + '.hp-go{margin-left:auto;color:var(--faint);flex:none}'
    + '.hp-dumpsec{grid-area:dump}'
    + '.hp-dump textarea{display:block;width:100%;box-sizing:border-box;min-height:92px;background:var(--bg);border:1px solid var(--border);border-radius:10px;color:var(--text);padding:12px 14px;font:inherit;font-size:14px;line-height:1.55;resize:vertical;margin-top:10px}'
    + '.hp-dump textarea:focus{outline:none;border-color:var(--accent)}'
    + '.hp-dump-row{display:flex;align-items:center;gap:14px;margin-top:12px;flex-wrap:wrap}'
    + '.hp-dump-btn{background:var(--accent);color:var(--on-accent);border:0;border-radius:10px;padding:10px 22px;font:inherit;font-size:14px;font-weight:650;cursor:pointer}'
    + '.hp-dump-btn:hover{filter:brightness(1.08)}'
    + '.hp-dump-status{font-size:13px;color:var(--muted)}'
    + '.hp-dump-status a{color:var(--accent)}'
    + '.hp-note{text-align:center;color:var(--muted);font-size:12px;margin:34px 0 0}'
    + '.hp-locked{margin-top:10px;background:var(--bg);border:1px dashed var(--border);border-radius:10px;padding:14px 16px}'
    + '@media (max-width:960px){'
    + '.hp-grid{grid-template-columns:minmax(0,1fr);grid-template-areas:"head" "rail" "main" "dump"}'
    + '.hp{padding:26px 16px 44px}'
    + '.hp-icon{width:62px;height:62px;font-size:34px;border-radius:18px}'
    + '.hp-name{font-size:24px}'
    + '.hp-card{padding:16px 18px}'
    + '}'
    + '</style>';
  h += '<div class="hp"><div class="hp-grid">';
  // header
  h += '<header class="hp-head"><div class="hp-icon">' + escHtml(b.icon || '🤖') + '</div><div class="hp-headtxt">';
  h += '<h1 class="hp-name">' + escHtml(dispName(b)) + '</h1>';
  if (b.tagline) h += '<p class="hp-tagline">' + escHtml(b.tagline) + '</p>';
  let statHtml = stats;
  if (b.status) statHtml = '<span class="status ' + escHtml(b.statusClass || '') + '">' + escHtml(b.status) + '</span>' + statHtml;
  + (isDormant(id) ? '<span class=\"status st-dormant\">💤 Dormant</span>' : '')
  if (statHtml) h += '<div class="hp-stats">' + statHtml + '</div>';
  h += '</div></header>';
  // main column
  h += '<div class="hp-main">';
  if (b.mission) {
    h += '<section class="hp-card"><h3 class="hp-kicker">About</h3><p class="hp-mission">' + escHtml(b.mission) + '</p></section>';
  }
  if (plans.length) {
    h += '<section class="hp-card"><h3 class="hp-kicker">Plans (' + plans.length + ')</h3>';
    plans.forEach(p => {
      h += '<div class="hp-plan"><div class="hp-picon">' + escHtml(p.icon || '💼') + '</div><div class="hp-pbody">';
      h += '<div class="hp-pname">' + escHtml(p.name || 'Untitled plan');
      if (p.status) h += '<span class="hp-pill">' + escHtml(p.status) + '</span>';
      h += '</div>';
      if (p.desc) h += '<p class="hp-pdesc">' + escHtml(p.desc) + '</p>';
      if (p.docs && p.docs[0] && p.docs[0].url) h += '<a class="hp-pdoc" href="' + escHtml(p.docs[0].url) + '" target="_blank" rel="noopener">' + escHtml(p.docs[0].label || 'Open doc') + ' →</a>';
      h += '</div></div>';
    });
    h += '</section>';
  }
  if (arts.length) {
    h += '<section class="hp-card"><h3 class="hp-kicker">Artifacts (' + arts.length + ')</h3>';
    arts.slice(0, 6).forEach(a => {
      h += '<div class="hp-art"><a href="' + escHtml(a.url || '#') + '" target="_blank" rel="noopener">' + escHtml(a.title || a.name || 'Artifact') + '</a><span class="hp-go">→</span></div>';
    });
    if (arts.length > 6) h += '<p class="hp-more">+' + (arts.length - 6) + ' more</p>';
    h += '</section>';
  }
  h += '</div>';
  // rail
  h += '<aside class="hp-rail">';
  if (attnItems.length) {
    h += '<section class="hp-card hp-attn"><h3 class="hp-kicker">Needs attention (' + attnItems.length + ')</h3>';
    attnItems.slice(0, 5).forEach(a => {
      h += '<div class="hp-aitem"><span class="hp-adot">●</span><div class="hp-atext">';
      if (a.url) h += '<a href="' + escHtml(a.url) + '" target="_blank" rel="noopener" style="color:inherit">' + escHtml(a.text || a) + ' ↗</a>';
      else h += escHtml(a.text || a);
      if (a.date) h += '<div class="hp-adate">Asked ' + escHtml(a.date) + '</div>';
      h += '</div></div>';
    });
    if (attnItems.length > 5) h += '<p class="hp-more">+' + (attnItems.length - 5) + ' more</p>';
    h += '</section>';
  }
  if (kids.length) {
    h += '<section class="hp-card"><h3 class="hp-kicker">Sub-buddies (' + kids.length + ')</h3><div class="hp-chips">';
    kids.forEach(k => {
      h += '<span class="hp-chip">' + escHtml(k.icon || '🤖') + ' ' + escHtml(dispName(k)) + '</span>';
    });
    h += '</div></section>';
  }
  h += '</aside>';
  // brain dump (full width, two-state: functional when a token is present)
  h += homepageDumpSectionHtml(b);
  h += '</div>';
  h += '<p class="hp-note">Auto-generated homepage — set a custom URL in the Homepage URL field to override.</p>';
  h += '</div>';
  return h;
}
function homepageDumpSectionHtml(b){
  let inner;
  if (!b.repo) {
    inner = '<p class="hp-dump-status" style="margin:10px 0 0">No repo linked for this buddy yet — dumps are disabled.</p>';
  } else if (!ghToken()) {
    inner = '<div class="hp-locked"><p class="hp-dump-status" style="margin:0 0 12px">🔒 Connect GitHub to unlock dumping. The token stays on this device only.</p>'
      + '<button type="button" class="hp-dump-btn" data-hp-connect>Connect GitHub to enable</button></div>';
  } else {
    inner = '<textarea data-hp-dump placeholder="Dump a thought, link, or half-formed idea — it lands in this buddy\\u2019s docs/ingest.md" aria-label="Brain dump"></textarea>'
      + '<div class="hp-dump-row"><button type="button" class="hp-dump-btn" data-hp-dump-btn>Dump it</button><span class="hp-dump-status" data-hp-dump-status></span></div>'
      + '<div data-hp-dump-feed style="margin-top:12px"></div>';
  }
  return '<section class="hp-card hp-dumpsec" data-hp-dumpsec><div class="hp-dump"><h3 class="hp-kicker">🧠 Brain dump</h3>' + inner + '</div></section>';
}
function lsToken(){
  try { return JSON.parse(localStorage.getItem(LS_KEY) || '{}').ghToken || ''; }
  catch (e) { return ''; }
}
function openTokenPopover(){
  const pop = document.getElementById('token-pop');
  if (pop) {
    pop.classList.add('show');
    const inp = document.getElementById('ghtok-global');
    if (inp) inp.focus();
  }
}
function refreshHomepageDumpbox(){
  const sec = document.querySelector('[data-hp-dumpsec]');
  if (!sec) return;
  const b = byId[projectId()] || {};
  const tmp = document.createElement('div');
  tmp.innerHTML = homepageDumpSectionHtml(b);
  const fresh = tmp.firstChild;
  sec.replaceWith(fresh);
  initHomepageDumpbox(fresh, b);
}
async function homepageDumpSubmit(root, id){
  const ta = root.querySelector('[data-hp-dump]');
  const st = root.querySelector('[data-hp-dump-status]');
  const b = byId[id];
  if (!ta || !b) return;
  const text = ta.value.trim();
  if (!text) return;
  // Re-check the token fresh from storage — it may have been added in another tab.
  if (!ghToken()) {
    const freshTok = lsToken();
    if (freshTok) { S.ghToken = freshTok; }
    else {
      if (st) st.innerHTML = 'Add a GitHub token to unlock ingest. <a href="https://github.com/settings/tokens" target="_blank" rel="noopener">Get one here</a>.';
      refreshHomepageDumpbox();
      return;
    }
  }
  const stamp = new Date().toLocaleString();
  const entry = '## ' + stamp + String.fromCharCode(10,10) + text + String.fromCharCode(10,10);
  if (!b.repo) { if (st) st.textContent = 'No repo linked for this buddy yet.'; return; }
  if (st) st.textContent = 'Dumping…';
  try {
    const cur = await ghGetFile(b.repo, 'docs/ingest.md') || '# Ingest log — ' + b.name + String.fromCharCode(10,10);
    await ghPutFile(b.repo, 'docs/ingest.md', b64encode(cur + entry), 'Ingest dump for ' + id);
    ta.value = '';
    if (st) st.textContent = 'Dumped to ' + b.repo + '/docs/ingest.md';
  } catch (err) { if (st) st.textContent = 'Save failed: ' + (err.message || err); }
}
function initHomepageDumpbox(root, b){
  if (!root || !b) return;
  const dumpBtn = root.querySelector('[data-hp-dump-btn]');
  if (dumpBtn && !dumpBtn._hpWired) {
    dumpBtn._hpWired = true;
    dumpBtn.addEventListener('click', function(){ homepageDumpSubmit(root, b.id); });
  }
  // Enter dumps, Shift+Enter for newline (Dave 2026-10-12)
  const ta = root.querySelector('[data-hp-dump]');
  if (ta && !ta._hpEnterWired) {
    ta._hpEnterWired = true;
    ta.addEventListener('keydown', function(e){
      if (e.key === 'Enter' && !e.shiftKey && !e.metaKey && !e.ctrlKey && !e.altKey) {
        e.preventDefault();
        homepageDumpSubmit(root, b.id);
      }
    });
  }
  const connectBtn = root.querySelector('[data-hp-connect]');
  if (connectBtn && !connectBtn._hpWired) {
    connectBtn._hpWired = true;
    connectBtn.addEventListener('click', function(){ openTokenPopover(); });
  }
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
    // Custom homepage URL: load in iframe (the "open in a new tab" link lives below the frame)
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
        // Same-origin homepage: bind pull-to-refresh inside the iframe so the
        // gesture works while a buddy homepage is showing (cross-origin fails
        // silently and keeps parent-only behavior).
        if (window.__bindPullToRefresh && frame.contentDocument) window.__bindPullToRefresh(frame.contentDocument);
        if (window.__bindEdgeSwipes && frame.contentDocument){ try { window.__bindEdgeSwipes(frame.contentDocument, frame, b.id); } catch (err2) {} }
      } catch (err) {}
    });
    wrap.appendChild(frame);
    const open = document.createElement('a');
    open.id = 'homepage-open';
    open.href = b.homepageSource || hp;
    open.target = '_blank';
    open.rel = 'noopener';
    open.textContent = 'Open in a new tab';
    wrap.appendChild(open);
  } else {
    // No custom URL: auto-generate homepage
    const open = document.createElement('span');
    open.id = 'homepage-open';
    open.style.cssText = 'cursor:default;opacity:0.6';
    open.textContent = 'Auto-generated homepage';
    wrap.appendChild(open);
    const content = document.createElement('div');
    content.id = 'homepage-frame';
    content.style.cssText = 'width:100%;height:100%;overflow:auto;background:var(--bg)';
    content.innerHTML = buddyHomepageHtml(b);
    initHomepageDumpbox(content, b);
    wrap.appendChild(content);
  }
  pv.appendChild(wrap);
}
/* ---- Persona picker (info panel) ---- */
function personaBlurb(name){
  const e = (typeof PERSONA_ROSTER !== 'undefined' ? PERSONA_ROSTER : []).find(x => x.name === name);
  return e ? e.blurb : '';
}
function personaQuote(name){
  const e = (typeof PERSONA_ROSTER !== 'undefined' ? PERSONA_ROSTER : []).find(x => x.name === name);
  return e ? (e.quote || '') : '';
}
function personaSecHtml(b){
  const p = b.persona || '';
  const pq = p ? personaQuote(p) : '';
  const cur = p
    ? '<div class="bp-persona-cur"><div class="bp-persona-name">' + escHtml(p) + '</div>'
      + (pq ? '<div class="bp-persona-quote" style="font-style:italic;color:var(--muted);margin:6px 0;font-size:13px">\u201c' + escHtml(pq) + '\u201d</div>' : '')
      + (personaBlurb(p) ? '<div class="bp-persona-blurb">' + escHtml(personaBlurb(p)) + '</div>' : '')
      + (pq ? '<button class="linkbtn" id="bp-persona-play" type="button" style="margin-top:8px">\u25b6\ufe0e Hear it</button>' : '')
      + '</div>'
    : '<p class="bp-empty">No persona set — this buddy speaks in its default voice.</p>';
  const headerName = p ? ': ' + escHtml(p) : '';
  return '<div class="bp-sec" data-field="persona"><h3>Persona' + headerName + '<span class="info-tip" data-tip="The voice this buddy speaks in. Pick the one that makes you grin \\u2014 it shapes how its messages and notifications sound.">\\u24d8</span></h3>'
    + cur
    + '<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">'
    + '<button class="linkbtn" id="bp-persona-change" type="button">Change persona</button>'
    + '<button class="linkbtn" id="bp-persona-surprise" type="button" title="Pick a random persona from the roster">\\uD83C\\uDFB2 Surprise me</button>'
    + '</div><p class="fineprint" id="bp-persona-status"></p></div>';
}
/* ---- Voice picker (info panel) ---- */
function voiceName(id){
  const e = (typeof VOICE_CATALOG !== 'undefined' ? VOICE_CATALOG : []).find(x => x.id === id);
  return e ? e.name : '';
}
function voiceDesc(id){
  const e = (typeof VOICE_CATALOG !== 'undefined' ? VOICE_CATALOG : []).find(x => x.id === id);
  return e ? e.desc : '';
}
function voiceSecHtml(b){
  const v = b.voice || '';
  const vn = v ? voiceName(v) : '';
  const cur = v && vn
    ? '<div class="bp-persona-cur"><div class="bp-persona-name">' + escHtml(vn) + '</div>'
      + (voiceDesc(v) ? '<div class="bp-persona-blurb">' + escHtml(voiceDesc(v)) + '</div>' : '') + '</div>'
    : '<p class="bp-empty">Default voice — this buddy has no specific voice assigned.</p>';
  const notesOn = !!b.voiceNotes;
  return '<div class="bp-sec" data-field="voice"><h3>Voice<span class="info-tip" data-tip="The spoken voice for this buddy\\u2019s voice notes. Pick one, then enable voice notes below to hear it in threads.">\\u24d8</span></h3>'
    + cur
    + '<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;align-items:center">'
    + '<button class="linkbtn" id="bp-voice-change" type="button">Change voice</button>'
    + (v ? '<button class="linkbtn" id="bp-voice-preview" type="button" title="Hear a sample of this voice">\u25b6\ufe0e Preview</button>' : '')
    + '<label style="display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text);cursor:pointer">'
    + '<input type="checkbox" id="bp-voice-notes" ' + (notesOn ? 'checked' : '') + ' style="width:18px;height:18px;accent-color:var(--accent)">'
    + 'Voice notes in threads</label>'
    + '</div><p class="fineprint" id="bp-voice-status"></p>'
    + '<p class="fineprint" style="margin-top:6px">Voice notes are off by default to save tokens. Enable per buddy.</p></div>';
}
function openPersonaPicker(id){
  const b = byId[id]; if (!b) return;
  const cur = b.persona || '';
  const roster = (typeof PERSONA_ROSTER !== 'undefined' ? PERSONA_ROSTER : []);
  const m = document.createElement('div');
  m.id = 'persona-picker';
  m.innerHTML = '<div class="pp-backdrop"></div><div class="pp-sheet" role="dialog" aria-label="Choose a persona">'
    + '<div class="pp-head"><h2>Persona</h2><p class="fineprint">Pick the voice that makes you grin.</p></div>'
    + '<div style="display:flex;align-items:center;gap:8px;margin:12px 16px 0"><input type="search" id="pp-filter" placeholder="Filter the 116 personas…" aria-label="Filter personas" autocomplete="off" style="flex:1;margin:0;width:auto">'
    + '<span id="pp-count" class="fineprint" style="font-size:12px;color:var(--muted);white-space:nowrap"></span></div>'
    + '<div class="pp-grid" id="pp-grid"></div>'
    + '<div class="pp-actions"><button class="linkbtn" id="pp-none" type="button">No persona (default voice)</button>'
    + '<button class="linkbtn" id="pp-surprise" type="button">\\uD83C\\uDFB2 Surprise me</button>'
    + '<button class="linkbtn" id="pp-cancel" type="button">Cancel</button></div></div>';
  document.body.appendChild(m);
  const grid = m.querySelector('#pp-grid');
  const filter = m.querySelector('#pp-filter');
  const close = () => m.remove();
  function renderGrid(){
    const q = filter.value.trim().toLowerCase();
    const list = roster.filter(p => !q || p.name.toLowerCase().indexOf(q) >= 0 || p.blurb.toLowerCase().indexOf(q) >= 0 || (p.quote && p.quote.toLowerCase().indexOf(q) >= 0));
    const countEl = m.querySelector('#pp-count');
    if (countEl) countEl.textContent = list.length + ' of ' + roster.length;
    grid.innerHTML = list.map(p =>
      '<button type="button" class="pp-card' + (p.name === cur ? ' sel' : '') + '" data-persona="' + escHtml(p.name) + '">'
      + '<span class="pp-name">' + escHtml(p.name) + '</span>'
      + (p.quote ? '<span class="pp-quote">\u201c' + escHtml(p.quote) + '\u201d</span>' : '')
      + '<span class="pp-blurb">' + escHtml(p.blurb) + '</span></button>').join('')
      || '<p class="bp-empty">No personas match that filter.</p>';
    grid.querySelectorAll('.pp-card').forEach(c => c.addEventListener('click', () => {
      const name = c.getAttribute('data-persona'); close(); setBuddyPersona(id, name);
    }));
  }
  filter.addEventListener('input', renderGrid);
  renderGrid();
  m.querySelector('.pp-backdrop').addEventListener('click', close);
  m.querySelector('#pp-cancel').addEventListener('click', close);
  m.querySelector('#pp-none').addEventListener('click', () => { close(); setBuddyPersona(id, ''); });
  m.querySelector('#pp-surprise').addEventListener('click', () => {
    if (!roster.length) return;
    close(); setBuddyPersona(id, roster[Math.floor(Math.random() * roster.length)].name);
  });
  m.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  filter.focus();
}
function openVoicePicker(id){
  const b = byId[id]; if (!b) return;
  const cur = b.voice || '';
  const catalog = (typeof VOICE_CATALOG !== 'undefined' ? VOICE_CATALOG : []);
  const m = document.createElement('div');
  m.id = 'persona-picker';
  m.innerHTML = '<div class="pp-backdrop"></div><div class="pp-sheet" role="dialog" aria-label="Choose a voice">'
    + '<div class="pp-head"><h2>Voice</h2><p class="fineprint">Pick the spoken voice for this buddy\\u2019s voice notes.</p></div>'
    + '<div style="display:flex;align-items:center;gap:8px;margin:12px 16px 0"><input type="search" id="pp-filter" placeholder="Filter the ' + catalog.length + ' voices…" aria-label="Filter voices" autocomplete="off" style="flex:1;margin:0;width:auto">'
    + '<span id="pp-count" class="fineprint" style="font-size:12px;color:var(--muted);white-space:nowrap"></span></div>'
    + '<div class="pp-grid" id="pp-grid"></div>'
    + '<div class="pp-actions"><button class="linkbtn" id="pp-none" type="button">Default voice</button>'
    + '<button class="linkbtn" id="pp-cancel" type="button">Cancel</button></div></div>';
  document.body.appendChild(m);
  const grid = m.querySelector('#pp-grid');
  const filter = m.querySelector('#pp-filter');
  const close = () => m.remove();
  function renderGrid(){
    const q = filter.value.trim().toLowerCase();
    const list = catalog.filter(v => !q || v.name.toLowerCase().indexOf(q) >= 0 || v.desc.toLowerCase().indexOf(q) >= 0 || v.accent.toLowerCase().indexOf(q) >= 0 || v.tone.toLowerCase().indexOf(q) >= 0);
    const countEl = m.querySelector('#pp-count');
    if (countEl) countEl.textContent = list.length + ' of ' + catalog.length;
    // Voices with audio samples (Dave 2026-10-12) — baked list of the 30 sampled voices
    const sampledVoices = {'avocado_v2:MAI_01':1,'avocado_v2:MAI_03':1,'avocado_v2:Karen':1,'avocado_v2:nova':1,'avocado_v2:bud':1,'avocado_v2:isabella':1,'avocado_v2:rumi':1,'avocado_v2:mudiwa':1,'avocado_v2:myrtle':1,'avocado_v2:hubert':1,'avocado_v2:conor':1,'avocado_v2:miles':1,'avocado_v2:briggs':1,'avocado_v2:chip':1,'avocado_v2:lady_macbeth':1,'avocado_v2:melody':1,'avocado_v2:marisol':1,'avocado_v2:atlas':1,'avocado_v2:casper':1,'avocado_v2:ElvenWizard':1,'avocado_v2:TruthTeller':1,'avocado_v2:Vanessa':1,'avocado_v2:Lily':1,'avocado_v2:Twenty':1,'avocado_v2:Caitlin':1,'avocado_v2:paloma':1,'avocado_v2:ronan':1,'avocado_v2:lumi':1,'avocado_v2:magnus':1,'avocado_v2:vincent':1};
    let curAudio = null;
    grid.innerHTML = list.map(v =>
      '<button type="button" class="pp-card' + (v.id === cur ? ' sel' : '') + '" data-voice="' + escHtml(v.id) + '">'
      + '<span class="pp-name">' + escHtml(v.name)
      + (sampledVoices[v.id] ? ' <span class="pp-play" data-play="' + escHtml(v.id) + '" title="Hear this voice" role="button" tabindex="0">\u25b6\ufe0e</span>' : '')
      + '</span>'
      + '<span class="pp-blurb">' + escHtml(v.desc) + (v.accent ? ' · ' + escHtml(v.accent) : '') + '</span></button>').join('')
      || '<p class="bp-empty">No voices match that filter.</p>';
    // Play buttons: stop propagation so tapping play doesn't select the voice
    grid.querySelectorAll('[data-play]').forEach(pb => {
      const playIt = (ev) => {
        ev.stopPropagation(); ev.preventDefault();
        if (curAudio){ curAudio.pause(); curAudio = null; }
        const vid = pb.getAttribute('data-play');
        const fname = vid.replace(/:/g, '_').replace(/\//g, '_') + '.mp3';
        curAudio = new Audio('voices/samples/' + fname);
        pb.textContent = '\u23f8\ufe0e';
        curAudio.onended = () => { pb.textContent = '\u25b6\ufe0e'; curAudio = null; };
        curAudio.play().catch(() => { pb.textContent = '\u25b6\ufe0e'; toast('Could not play the preview.'); });
      };
      pb.addEventListener('click', playIt);
      pb.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') playIt(ev); });
    });
    grid.querySelectorAll('.pp-card').forEach(c => c.addEventListener('click', () => {
      if (curAudio){ curAudio.pause(); curAudio = null; }
      const vid = c.getAttribute('data-voice'); close(); setBuddyVoice(id, vid);
    }));
  }
  filter.addEventListener('input', renderGrid);
  renderGrid();
  m.querySelector('.pp-backdrop').addEventListener('click', close);
  m.querySelector('#pp-cancel').addEventListener('click', close);
  m.querySelector('#pp-none').addEventListener('click', () => { close(); setBuddyVoice(id, ''); });
  m.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  filter.focus();
}
async function setBuddyVoice(id, voiceId){
  const st = document.getElementById('bp-voice-status');
  try {
    if (!ghToken()) throw new Error('Add a GitHub token first (gear menu \u2192 GitHub token) so the dashboard can save.');
    if (st) st.textContent = 'Saving…';
    const raw = await ghGetFile('buddy-system', 'buddies.json');
    if (!raw) throw new Error('Could not read buddies.json from GitHub.');
    const data = JSON.parse(raw);
    const arr = data.buddies || data;
    const e = arr.find(x => x.id === id);
    if (!e) throw new Error('Buddy not found in the registry.');
    if (voiceId) e.voice = voiceId; else delete e.voice;
    await ghPutFile('buddy-system', 'buddies.json', b64encode(JSON.stringify(data, null, 1)), 'Set voice for ' + id + ' (dashboard info panel)');
    const b = byId[id];
    if (b) { if (voiceId) b.voice = voiceId; else delete b.voice; }
    save(); renderBuddy(id);
    const vn = voiceName(voiceId);
    toast(voiceId ? 'Voice set to ' + vn + '.' : 'Voice cleared — back to default.');
  } catch (err) {
    if (st) st.textContent = '';
    toast('Could not save voice: ' + (err.message || err));
  }
}
async function setBuddyVoiceNotes(id, enabled){
  const st = document.getElementById('bp-voice-status');
  try {
    if (!ghToken()) throw new Error('Add a GitHub token first (gear menu \u2192 GitHub token) so the dashboard can save.');
    if (st) st.textContent = 'Saving…';
    const raw = await ghGetFile('buddy-system', 'buddies.json');
    if (!raw) throw new Error('Could not read buddies.json from GitHub.');
    const data = JSON.parse(raw);
    const arr = data.buddies || data;
    const e = arr.find(x => x.id === id);
    if (!e) throw new Error('Buddy not found in the registry.');
    if (enabled) e.voiceNotes = true; else delete e.voiceNotes;
    await ghPutFile('buddy-system', 'buddies.json', b64encode(JSON.stringify(data, null, 1)), (enabled ? 'Enable' : 'Disable') + ' voice notes for ' + id + ' (dashboard info panel)');
    const b = byId[id];
    if (b) { if (enabled) b.voiceNotes = true; else delete b.voiceNotes; }
    save();
    if (st) st.textContent = '';
    toast(enabled ? 'Voice notes enabled for this buddy.' : 'Voice notes disabled.');
  } catch (err) {
    if (st) st.textContent = '';
    toast('Could not save: ' + (err.message || err));
    // Revert the checkbox on failure
    const cb = document.getElementById('bp-voice-notes');
    if (cb) cb.checked = !enabled;
  }
}
async function setBuddyPersona(id, name){
  const st = document.getElementById('bp-persona-status');
  try {
    if (!ghToken()) throw new Error('Add a GitHub token first (gear menu \\u2192 GitHub token) so the dashboard can save.');
    if (st) st.textContent = 'Saving…';
    const raw = await ghGetFile('buddy-system', 'buddies.json');
    if (!raw) throw new Error('Could not read buddies.json from GitHub.');
    const data = JSON.parse(raw);
    const arr = data.buddies || data;
    const e = arr.find(x => x.id === id);
    if (!e) throw new Error('Buddy not found in the registry.');
    if (name) e.persona = name; else delete e.persona;
    await ghPutFile('buddy-system', 'buddies.json', b64encode(JSON.stringify(data, null, 1)), 'Set persona for ' + id + ' (dashboard info panel)');
    const b = byId[id];
    if (b) { if (name) b.persona = name; else delete b.persona; }
    save(); renderBuddy(id);
    toast(name ? 'Persona set to ' + name + '.' : 'Persona cleared — back to the default voice.');
  } catch (err) {
    if (st) st.textContent = '';
    toast('Could not save persona: ' + (err.message || err));
  }
}
function renderBuddy(id){
  const b = byId[id]; if(!b) return;
  try{ setBuddyFavicon(buddyDisplayIcon(b), buddyImageUrl(b)); }catch(e){}
  const items = (b.attention || []).filter(a => !S.seen[a.id]);
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
  let reportsSec = '';
  (function(){
    const kids = (kidsOf[id] || []).filter(k => k && k.id !== id);
    const addBtn = '<button class="bp-circle-add" data-addbuddy="child" data-for="'+escHtml(id)+'" title="Add a child buddy below this one" aria-label="Add a child buddy">⊕</button>';
    const rows = kids.map(k =>
      '<a class="art-row" data-buddy="'+escHtml(k.id)+'">'
      + '<span class="art-ic">'+escHtml(k.icon || '')+'</span>'
      + '<span><span class="art-label">'+escHtml(dispName(k))+'</span><div class="art-sub">'+escHtml((k.tagline || k.mission || '').slice(0, 90))+'</div></span>'
      + '<span class="art-go" data-homepage="'+escHtml(k.id)+'" title="Open homepage">\\u2192</span></a>').join('');
    reportsSec = '<div class="bp-sec" data-field="reports"><h3>Children' + (kids.length ? ' <span class="attn-count">('+kids.length+')</span>' : '') + addBtn + '</h3>' + (rows || '<p class="bp-empty">No children yet.</p>') + '</div>';
  })();
  let parSec = '';
  (function(){
    const par = effParent(b);
    const addParentBtn = '<button class="bp-add" data-addbuddy="parent" data-for="'+escHtml(id)+'" title="Add a parent/manager above this buddy">＋ ↑ Parent</button>';
    const addSibBtn = '<button class="bp-add" data-addbuddy="sibling" data-for="'+escHtml(id)+'">+ Peer</button>';
    if (!par) {
      parSec = '<div class="bp-sec" data-field="parent"><h3>Parent'+addParentBtn+'<button class="bp-add" data-changeparent="'+escHtml(id)+'" title="Set this buddy\u2019s parent">Set parent</button></h3><p class="bp-empty">Top-level buddy — no parent.</p></div>';
      return;
    }
    const pb = byId[par];
    if (!pb) return;
    parSec = '<div class="bp-sec" data-field="parent"><h3>Parent<button class="bp-add" data-changeparent="'+escHtml(id)+'" title="Change this buddy\u2019s parent">Change</button></h3>'
      + '<a class="bp-parent-link" data-buddy="'+escHtml(par)+'" title="Open '+escHtml(dispName(pb))+'">'
      + escHtml(dispName(pb)) + '<span class="bp-parent-kind"> (' + escHtml(pb.kind || 'buddy') + ')</span></a></div>';
  })();
  let sibSec = '';
  (function(){
    const par = effParent(b);
    if (!par) return;
    const sibs = (kidsOf[par] || []).filter(k => k && k.id !== id && k.id !== par);
    if (!sibs.length) return;
    const SHOW_SIBS = 5;
    const sibRows = sibs.slice(0, SHOW_SIBS).map(k =>
      '<a class="art-row sib-compact" data-buddy="'+escHtml(k.id)+'">'
      + '<span class="art-ic">'+escHtml(k.icon || '')+'</span>'
      + '<span class="art-label">'+escHtml(dispName(k))+'</span></a>').join('');
    const sibMore = sibs.length > SHOW_SIBS
      ? '<button class="linkbtn" id="sib-showall" style="margin-top:6px">Show all '+sibs.length+' peers</button><div id="sib-rest" hidden>' + sibs.slice(SHOW_SIBS).map(k =>
        '<a class="art-row sib-compact" data-buddy="'+escHtml(k.id)+'">'
        + '<span class="art-ic">'+escHtml(k.icon || '')+'</span>'
        + '<span class="art-label">'+escHtml(dispName(k))+'</span></a>').join('') + '</div>' : '';
    sibSec = '<div class="bp-sec" data-field="siblings"><h3>Peers <span class="attn-count">('+sibs.length+')</span></h3>' + sibRows + sibMore + '</div>';
  })();
  let linkSec = '';
  (function(){
    const out = (b.links || []).filter(lid => lid !== id);
    const inc = (b.linkedBy || []).filter(lid => lid !== id && out.indexOf(lid) < 0);
    const all = out.concat(inc);
    if (!all.length) return;
    function prettyId(s){ return s.replace(/-buddy$/, "'s Buddy").replace(/(^|-)([a-z])/g, function(m, p, c){ return (p === '-' ? ' ' : '') + c.toUpperCase(); }); }
    linkSec = '<div class="bp-sec" data-field="links"><h3>Linked buddies</h3>' + all.map(lid => {
      const lb = byId[lid];
      if (lb) return '<a class="art-row" data-buddy="' + escHtml(lid) + '">'
        + '<span class="art-ic">' + escHtml(lb.icon || '') + '</span>'
        + '<span><span class="art-label">' + escHtml(dispName(lb)) + '</span><div class="art-sub">' + escHtml((lb.mission || '').slice(0, 90)) + '</div></span>'
        + '<span class="art-go" data-homepage="' + escHtml(lid) + '" title="Open homepage">\u2192</span></a>';
      return '<div class="art-row" style="opacity:.55">'
        + '<span class="art-ic">\u23f3</span>'
        + '<span><span class="art-label">' + escHtml(prettyId(lid)) + '</span><div class="art-sub">Buddy being set up</div></span></div>';
    }).join('') + '</div>';
  })();
  let attn = '';
  const fmtSeenTime = ts => {
    try {
      const d = new Date(ts), now = new Date();
      const time = d.toLocaleTimeString([], {hour:'numeric', minute:'2-digit'});
      const sameDay = d.toDateString() === now.toDateString();
      if (sameDay) return time;
      return d.toLocaleDateString([], {month:'short', day:'numeric'}) + ', ' + time;
    } catch (e) { return ''; }
  };
  let unseenCount = 0;
  if (!items.length) attn = '';
  else {
    attn = items.map(a => {
      const txt = escHtml(a.text || '');
      const body = a.url
        ? '<div class="attn-text"><a href="'+escHtml(a.url)+'" target="_blank" rel="noopener">'+txt+' <span class="attn-open">\u2197</span></a></div>'
        : '<div class="attn-text">'+txt+'</div>';
      return '<div class="attn unseen" data-attn="'+a.id+'"><span class="adot"></span>'
        + '<div class="attn-body">'+body
        + (a.date ? '<div class="attn-date">Asked '+escHtml(a.date)+'</div>' : '')+'</div>'
        + '<button class="seenbtn" data-done="'+a.id+'" title="Mark done" aria-label="Mark done" role="checkbox" aria-checked="false">\u25cb</button></div>';
    }).join('');
    unseenCount = items.length;
    if (items.length > 1) attn += '<div class="attn-all"><button class="seenbtn" data-done-all="'+id+'">Mark all done</button></div>';
  }
  document.getElementById('buddy-home').innerHTML =
    '<div class="bp-wrap">'
    + '<button class="bp-takeover-back" id="bp-takeover-back" type="button" title="Close detail \u2014 back to main view" aria-label="Close detail \u2014 back to main view">\u2039 Main</button>'

    + '<div class="sa-bar"><span>\U0001f516 Standalone view</span><button class="linkbtn" id="sa-full">Open full dashboard \u2192</button></div>'
    + '<div class="bp-sticky-head">'
    + '<div class="bp-topnav"><button class="linkbtn" data-navbtn="back">\u2190 Back</button>'
    + '<button class="linkbtn" data-navbtn="prev">\u2039 Prev</button><button class="linkbtn" data-navbtn="next">Next \u203a</button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" data-view="projects" id="bp-allbuddies">All buddies</button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" id="bp-settings">Settings</button>'
    + '<span class=\"sep\">\\u00b7</span><button class=\"linkbtn\" id=\"bp-dormant\" title=\"Mark dormant / wake up\"></button>'
    + '<span class="sep">\u00b7</span><button class="linkbtn" id="bp-desktop">\U0001f4be Save to desktop</button></div>'
    + '<div class="bp-top">'
    + '<span class="bp-icon" id="bp-icon" title="Click to change avatar" style="cursor:pointer">'+'<img class="bp-avatarimg" src="'+escHtml(buddyImageUrl(b))+'" alt="" onerror="this.remove()">'+'<span class="bp-avaemoji">'+escHtml(buddyDisplayIcon(b))+'</span></span>'
    + '<h2 class="bp-name" id="bp-name" contenteditable="true" spellcheck="false" data-buddy="'+id+'">'+escHtml(dispName(b))+'</h2>'
    + '<span class="status '+b.statusClass+'">'+escHtml(b.status)+'</span>'
    + (function(){ const ak = effAka(b); return ak.length ? '<span class="bp-aka" title="Also known as">aka '+escHtml(ak.join(', '))+'</span>' : ''; })()
    + '<button class="bp-close-x" id="bp-close-x" type="button" title="Close detail \u2014 back to main view" aria-label="Close detail \u2014 back to main view">\u203a</button></div>'
    + '</div>'
    + '<div class="bp-crumb">'+crumb(id)+'</div>'
    + '<p class="bp-tagline">'+escHtml(b.tagline||'')+'</p>'
    + '<div id="token-warn-slot"></div>'
    + standingOrdersHtml()
    + '<div class="bp-sec" data-field="ingest"><h3>Dump box<span class="info-tip" data-tip="Brain-dump anything about this buddy \u2014 raw and unfiltered. Each dump lands in the buddy\u2019s repo (docs/ingest.md) as a timestamped entry.">\u24d8</span></h3>'
    + '<textarea class="notes" id="bp-ingest" placeholder="Dump what\u2019s in your head about '+escHtml(dispName(b))+'\u2026"></textarea>'
    + '<div style="margin-top:8px"><span class="fineprint" id="ingest-status"></span></div>'
    + '<div id="ingest-feed" style="margin-top:8px"></div></div>'
    + '<div class="bp-sec" data-field="mission"><h3>About<span class="info-tip" data-tip="The mission statement\\u2019s executive summary \\u2014 tweak it through the buddy\\u2019s chat thread and it updates everywhere.">\\u24d8</span></h3><p class="bp-mission">'+escHtml(b.mission)+'</p></div>'
    + '<div class="bp-sec" data-field="aka"><h3>A.K.A.<span class="info-tip" data-tip="Other names for this buddy \\u2014 nicknames, aliases, what people actually call them. Searchable.">\\u24d8</span></h3>'
    + '<div id="bp-aka-list" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px"></div>'
    + '<div style="display:flex;gap:8px"><input type="text" id="bp-aka-input" placeholder="Add a nickname…" aria-label="Add a nickname" style="flex:1;min-width:0;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:13px;color:var(--text)">'
    + '<button class="linkbtn" id="bp-aka-add" type="button">Add</button></div></div>'
    + personaSecHtml(b)
    + voiceSecHtml(b)
    + reportsSec
    + parSec
    + sibSec
    + linkSec
    + '<div class="bp-sec" data-field="homepage"><h3>Homepage URL</h3>'
    + '<div style="display:flex;align-items:center;gap:8px">'
    + '<input type="url" id="bp-homepage-url" value="'+escHtml(homepageUrl(b))+'" placeholder="Paste homepage URL here…" style="flex:1;min-width:0;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:13px;color:var(--text)" title="The full URL for this buddy\u2019s homepage. Paste a URL and click away to save.">'
    + '<button class="linkbtn" id="bp-homepage-copy" title="Copy homepage URL to clipboard" style="flex-shrink:0">Copy</button>'
    + '<button class="linkbtn" id="bp-homepage-open" title="Open homepage in a new tab" style="flex-shrink:0">Open</button>'
    + '</div></div>'
    + (unseenCount > 0 ? (function(){ const fx = getSetting('attnEffect') || 'none'; const high = items.some(a => !S.seen[a.id] && a.priority === 'high'); return '<div class="bp-sec fx-'+fx+(high?' attn-high':'')+'" data-field="attention"><h3>Needs your attention <span class="attn-count">('+unseenCount+')</span></h3>'+attn+'</div>'; })() : '')
    + photos
    + (id === ROOT_ID
        ? '<div class="bp-sec" data-field="tree"><h3>The Buddy Tree</h3><div class="bp-tree-wrap"></div>'
          + '<p class="fineprint"><button class="linkbtn" data-view="tree">Open the tree as its own view \\u2192</button></p></div>'
        : '')
    + '<div class="bp-sec" data-field="artifacts"><h3>Artifacts</h3>'+arts+'</div>'
    + planSec
    + '<div class="bp-sec" data-field="notes"><h3>Private notes<span class="info-tip" data-tip="Saved on this device. (For your eyes only)">\u24d8</span></h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this buddy\u2026 (For your eyes only)">'+escHtml(S.notes[id]||'')+'</textarea>'
    + '</div>'
    + '<div class="bp-sec" data-field="shared"><h3>Shared notes<span class="info-tip" data-tip="Anybody with repo access can see this note. Saved to the buddy\u2019s repo (docs/notes.md).">\u24d8</span></h3>'
    + '<textarea class="notes" id="bp-shared-notes" placeholder="Anybody with repo access can see this note."></textarea>'
    + '<p class="fineprint" id="shared-status"></p></div>'
    + '<div class="bp-build">Build __BUILD__</div>'
    + '</div>';
  // Update every visible label for a buddy after a rename/re-icon, across all
  // Atlas lenses. A rename changes no structure, so labels are patched in place
  // to preserve the user's pan/zoom/scroll.
  window.refreshBuddyLabels = function(id){
    const b = byId[id]; if (!b) return;
    const label = iconName(b);
    const q = '#treezoom [data-buddy="' + id + '"]';
    // Org + Lineage tiles (and orphan grid)
    document.querySelectorAll('#treezoom .node[data-buddy="' + id + '"] .name').forEach(function(el){
      const kc = el.querySelector('.kcount');
      el.innerHTML = label + (kc ? kc.outerHTML : '');
    });
    // Ledger rows
    document.querySelectorAll('#treezoom .ledger-row[data-buddy="' + id + '"] .ledger-name').forEach(function(el){
      el.innerHTML = label;
    });
    // Colonnade rows (first span holds the name)
    document.querySelectorAll('#treezoom .mcol-row[data-buddy="' + id + '"] > span:first-child').forEach(function(el){
      el.innerHTML = label;
    });
    // Terrain tiles (leaf + branch labels)
    document.querySelectorAll('#treezoom .tm-tile[data-buddy="' + id + '"] .tm-name, #treezoom .tm-label[data-buddy="' + id + '"]').forEach(function(el){
      el.innerHTML = label;
    });
    // Halo SVG labels + center label
    document.querySelectorAll('#halo-svg text.halo-label[data-buddy="' + id + '"]').forEach(function(el){
      el.textContent = (b.icon ? b.icon + ' ' : '') + dispName(b);
    });
    document.querySelectorAll('.halo-center-label[data-buddy="' + id + '"]').forEach(function(el){
      el.innerHTML = label;
    });
    // Constellation is canvas-drawn: re-init picks up the new label
    if (typeof getChartType === 'function' && getChartType() === 'constellation'
        && typeof initConstellation === 'function') initConstellation();
  };
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
    // Immediately reflect the new name in every visible chart (all Atlas lenses)
    refreshBuddyLabels(id);
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
      // If the Homepage view is showing this buddy, reload it with the new URL
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
  /* Persona picker — persisted to buddies.json via the GitHub token route */
  (function initPersona(){
    const changeBtn = document.getElementById('bp-persona-change');
    const surpriseBtn = document.getElementById('bp-persona-surprise');
    if (!changeBtn || !surpriseBtn) return;
    changeBtn.addEventListener('click', e => { e.stopPropagation(); openPersonaPicker(id); });
    surpriseBtn.addEventListener('click', e => {
      e.stopPropagation();
      const roster = (typeof PERSONA_ROSTER !== 'undefined' ? PERSONA_ROSTER : []);
      if (!roster.length) { toast('Persona roster is empty.'); return; }
      setBuddyPersona(id, roster[Math.floor(Math.random() * roster.length)].name);
    });
    const playBtn = document.getElementById('bp-persona-play');
    if (playBtn) playBtn.addEventListener('click', e => {
      e.stopPropagation();
      const b = byId[id];
      const pname = b && b.persona ? b.persona : '';
      if (!pname) { toast('No persona selected.'); return; }
      // Filename: sanitized persona name
      const fname = pname.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '.mp3';
      const audio = new Audio('personas/samples/' + fname);
      audio.play().catch(() => toast('Could not play the sample.'));
    });
  })();
  /* Voice picker + voice notes toggle — persisted to buddies.json via GitHub */
  (function initVoice(){
    const changeBtn = document.getElementById('bp-voice-change');
    const notesCb = document.getElementById('bp-voice-notes');
    if (changeBtn) changeBtn.addEventListener('click', e => { e.stopPropagation(); openVoicePicker(id); });
    const previewBtn = document.getElementById('bp-voice-preview');
    if (previewBtn) previewBtn.addEventListener('click', e => {
      e.stopPropagation();
      const voiceId = (byId[id] && byId[id].voice) || '';
      if (!voiceId) { toast('No voice selected.'); return; }
      const fname = voiceId.replace(/:/g, '_').replace(/\//g, '_') + '.mp3';
      const audio = new Audio('voices/samples/' + fname);
      audio.play().catch(() => toast('Could not play the preview.'));
    });
    if (notesCb) notesCb.addEventListener('change', e => {
      e.stopPropagation();
      setBuddyVoiceNotes(id, notesCb.checked);
    });
  })();
  /* A.K.A. editor — device-local alias list, searchable */
  (function initAka(){
    const list = document.getElementById('bp-aka-list');
    const input = document.getElementById('bp-aka-input');
    const addBtn = document.getElementById('bp-aka-add');
    if (!list || !input || !addBtn) return;
    function cur(){ return effAka(b).slice(); }
    function persist(arr){
      if (!S.aka || typeof S.aka !== 'object') S.aka = {};
      const baked = b.aka || [];
      if (JSON.stringify(arr) === JSON.stringify(baked)) delete S.aka[id];
      else S.aka[id] = arr;
      save();
    }
    function render(){
      const arr = cur();
      list.innerHTML = arr.length
        ? arr.map((a, i) => '<span class="aka-pill">'
          + escHtml(a)
          + '<button type="button" class="linkbtn" data-aka-del="' + i + '" aria-label="Remove nickname" style="padding:0 2px">×</button></span>').join('')
        : '<span class="fineprint">No nicknames yet.</span>';
    }
    list.addEventListener('click', e => {
      const del = e.target.closest('[data-aka-del]');
      if (!del) return;
      e.stopPropagation();
      const arr = cur();
      const removed = arr.splice(+del.dataset.akaDel, 1)[0];
      persist(arr); render();
      logChange('rename', id, 'Removed nickname "' + removed + '"', removed, null);
      renderNav();
    });
    function add(){
      const v = input.value.trim();
      if (!v) return;
      const arr = cur();
      if (arr.some(a => a.toLowerCase() === v.toLowerCase())) { input.value = ''; return; }
      arr.push(v);
      persist(arr); render();
      input.value = '';
      logChange('rename', id, 'Added nickname "' + v + '"', null, v);
      renderNav();
    }
    addBtn.addEventListener('click', e => { e.stopPropagation(); add(); });
    input.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); add(); } });
    input.addEventListener('click', e => e.stopPropagation());
    render();
  })();
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
  const hpo = document.getElementById('bp-homepage-open');
  if (hpo) {
    hpo.addEventListener('click', e => {
      e.stopPropagation();
      const url = (document.getElementById('bp-homepage-url') || {}).value || getHomepage(b);
      if (url) window.open(url, '_blank', 'noopener');
    });
  }
  const dbtn = document.getElementById('bp-dormant');
  if (dbtn) {
    const dor = isDormant(id);
    dbtn.textContent = dor ? '\u23f0 Wake' : '💤 Mark dormant';
    dbtn.addEventListener('click', e => {
      e.stopPropagation();
      setDormant(id, !isDormant(id));
      toast(isDormant(id) ? 'Marked dormant.' : 'Welcomed back.');
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
      if (!txt || txt === lastDumped) { if (st && !txt) { st.textContent = ''; st.classList.remove('dumped-ok'); } return; }
      if (st) { st.textContent = 'waiting\u2026'; st.classList.remove('dumped-ok'); }
      t = setTimeout(async () => {
        const cur = ta.value.trim();
        if (!cur || cur === lastDumped) return;
        if (st) { st.textContent = 'dumping\u2026'; st.classList.remove('dumped-ok'); }
        await dumpIngest(bid, false);
        lastDumped = ta.value.trim();
        if (st && lastDumped) { st.textContent = 'dumped \u2713'; st.classList.add('dumped-ok'); }
      }, 2000);
    });
    ta.addEventListener('keydown', async e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        clearTimeout(t);
        const cur = ta.value.trim();
        if (!cur || cur === lastDumped) return;
        if (st) { st.textContent = 'dumping\u2026'; st.classList.remove('dumped-ok'); }
        await dumpIngest(bid, false);
        lastDumped = '';
        if (st) { st.textContent = 'dumped \u2713'; st.classList.add('dumped-ok'); }
      }
    });
  })(id);
  loadPhotos(id);
  initPhotoDrop(id);
  initPanelResize(); applyPanelWidth();
  refreshTokenUI(id);
  applyFieldOrder();
  applySectionCollapse(id);
  applySectionDrag();
  renderJournal();
  if (id === ROOT_ID) {
    const tw = document.querySelector('#buddy-home .bp-tree-wrap');
    const srcEl = document.getElementById('view-tree');
    if (tw && srcEl) {
      tw.innerHTML = '<div class="bp-mini-zoom"><button id="bp-mz-out" title="Zoom out">\u2212</button><button id="bp-mz-in" title="Zoom in">+</button></div><div class="bp-mini-chart"></div>';
      const mc = tw.querySelector('.bp-mini-chart');
      mc.innerHTML = srcEl.innerHTML;
      mc.querySelectorAll('.zoombar,#tree-split').forEach(x => x.remove());
      const zw = mc.querySelector('#zoomwrap'); if (zw) { zw.style.display = 'block'; }
      const tz = mc.querySelector('#treezoom'); if (tz) { tz.style.overflow = 'visible'; tz.style.height = 'auto'; tz.style.display = 'block'; tz.removeAttribute('id'); }
      mc.querySelectorAll('.treescroll').forEach(x => { x.style.overflow = 'visible'; x.style.height = 'auto'; });
      mc.querySelectorAll('.treepane').forEach(x => { x.style.display = 'block'; });
      let mz = 80;
      const applyMz = () => { const ch = mc.querySelector('.chart'); if (ch) ch.style.zoom = mz + '%'; };
      applyMz();
      document.getElementById('bp-mz-in').addEventListener('click', e => { e.stopPropagation(); mz = Math.min(150, mz + 10); applyMz(); });
      document.getElementById('bp-mz-out').addEventListener('click', e => { e.stopPropagation(); mz = Math.max(20, mz - 10); applyMz(); });
      attachPan(tw);
    }
  }
  // Panel always opens at the top
  (function(){
    const vb = document.getElementById('view-buddy');
    if (vb) vb.scrollTop = 0;
  })();
}
function toast(msg){
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const t = document.createElement('div');
  t.className = 'toast'; t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => { if (t.parentNode) t.remove(); }, 3400);
}
// Jonny's done interaction (2026-10-12): tap circle -> accent fill + white check
// (200ms) -> tile glides out -> "Marked done. Undo." 6s toast. Undo restores.
function toastWithUndo(msg, onUndo){
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = '<span>' + escHtml(msg) + '</span> <button style="margin-left:10px;background:none;border:none;color:var(--accent);font-weight:700;cursor:pointer;font-size:14px;padding:4px 8px">Undo</button>';
  document.body.appendChild(t);
  const btn = t.querySelector('button');
  const kill = setTimeout(() => { if (t.parentNode) t.remove(); }, 6000);
  btn.addEventListener('click', () => { clearTimeout(kill); t.remove(); onUndo(); });
}
// Poof a panel section away when its last item is completed (Dave 2026-10-12).
// Phase 1: text dims. Phase 2: fade + slight shrink + height collapse (sections below scooch up).
// Then callback runs (typically the re-render).
function poofSection(field, callback){
  const sec = document.querySelector('.bp-sec[data-field="' + field + '"]');
  if (!sec){ callback(); return; }
  // Lock the current height so the collapse animates smoothly
  sec.style.maxHeight = sec.offsetHeight + 'px';
  sec.classList.add('poof-dim');
  setTimeout(() => {
    sec.classList.remove('poof-dim');
    sec.classList.add('poof-gone');
    setTimeout(callback, 550);
  }, 320);
}
function markAttentionDone(attnId, btnEl){
  // Step 1: fill the circle with accent + white check (~200ms)
  if (btnEl) {
    btnEl.style.transition = 'background .2s, color .2s, border-color .2s';
    btnEl.style.background = 'var(--accent)';
    btnEl.style.borderColor = 'var(--accent)';
    btnEl.style.color = '#fff';
    btnEl.textContent = '\u2713';
    btnEl.setAttribute('aria-checked', 'true');
  }
  setTimeout(() => {
    // Step 2: record the done timestamp (answers Dave's question: yes, we record when)
    const doneAt = Date.now();
    S.seen[attnId] = doneAt;
    save();
    // Step 3: glide the tile out, then rerender — poof the whole section if it was the last item
    const buddyId = S.sel.slice(6);
    const remaining = (byId[buddyId].attention || []).filter(a => !S.seen[a.id]);
    const tile = btnEl ? btnEl.closest('.attn') : null;
    const rerender = () => { renderBuddy(buddyId); renderNav(); updateAppBadge(); };
    if (tile) {
      tile.style.transition = 'opacity .25s, transform .25s';
      tile.style.opacity = '0';
      tile.style.transform = 'translateX(24px)';
      setTimeout(() => {
        if (remaining.length === 0) {
          // Last item: let the tile finish, then poof the section away
          poofSection('attention', rerender);
        } else {
          rerender();
        }
      }, 250);
    } else {
      if (remaining.length === 0) poofSection('attention', rerender);
      else rerender();
    }
    // Step 4: 6-second Undo toast
    toastWithUndo('Marked done.', () => {
      delete S.seen[attnId];
      save();
      renderBuddy(S.sel.slice(6)); renderNav(); updateAppBadge();
    });
  }, 200);
}
function markAllAttentionDone(buddyId){
  const ids = (byId[buddyId].attention || []).map(a => a.id);
  const doneAt = Date.now();
  ids.forEach(id => S.seen[id] = doneAt);
  save();
  const rerender = () => { renderBuddy(S.sel.slice(6)); renderNav(); updateAppBadge(); };
  poofSection('attention', rerender);
  toastWithUndo('Marked all done.', () => {
    ids.forEach(id => delete S.seen[id]);
    save();
    renderBuddy(S.sel.slice(6)); renderNav(); updateAppBadge();
  });
}
// Persistent top banner (e.g. dev-mode simulation). Sticky, high-contrast, dismissible via hideBanner.
function showBanner(id, html, sticky){
  hideBanner(id);
  const b = document.createElement('div');
  b.className = 'app-banner'; b.dataset.banner = id;
  b.innerHTML = html;
  b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:9999;background:#b3541e;color:#fff;'
    + 'font-size:13px;font-weight:600;text-align:center;padding:8px 12px;box-shadow:0 2px 8px rgba(0,0,0,.3)';
  document.body.appendChild(b);
  document.body.style.paddingTop = b.offsetHeight + 'px';
}
function hideBanner(id){
  document.querySelectorAll('.app-banner' + (id ? '[data-banner="' + id + '"]' : '')).forEach(b => b.remove());
  if (!document.querySelector('.app-banner')) document.body.style.paddingTop = '';
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
let pendingMoveUndo = null; // {src, beforeParent, timer} — one pending move undo at a time
function clearPendingMoveUndo(){
  if (pendingMoveUndo) { clearTimeout(pendingMoveUndo.timer); pendingMoveUndo = null; }
  hideUndoToast();
}
function applyParentOverride(src, parentId){
  const b = byId[src]; if (!b) return;
  if (parentId === b.parent) delete S.parents[src]; else S.parents[src] = parentId;
}
function undoMove(src, beforeParent){
  const b = byId[src]; if (!b) return;
  const wasParent = effParent(b);
  applyParentOverride(src, beforeParent);
  const dest = beforeParent ? byId[beforeParent] : null;
  logChange('move', src, 'Undid move of \u201c' + dispName(b) + '\u201d', wasParent, beforeParent);
  save(); buildKids(); renderNav(); refreshViews();
  if (S.sel === 'buddy:' + src || S.sel === 'buddy:' + ROOT_ID) renderBuddy(S.sel.slice(6));
  toast(dispName(b) + (dest ? ' moved back under ' + dispName(dest) + '.' : ' restored as an orphan.'));
}
function offerMoveUndo(src, beforeParent, msg){
  clearPendingMoveUndo();
  const data = {src: src, beforeParent: beforeParent, timer: null};
  data.timer = setTimeout(function(){ pendingMoveUndo = null; hideUndoToast(); }, 6000);
  pendingMoveUndo = data;
  undoToast(msg, function(){
    if (pendingMoveUndo === data) { clearTimeout(data.timer); pendingMoveUndo = null; }
    undoMove(src, beforeParent);
  });
}
function moveBuddy(src, target){
  if (!src || !target || src === target) return;
  const b = byId[src]; if (!b || !byId[target]) return;
  if (isDesc(target, src)) { toast('Can\u2019t move ' + dispName(b) + ' under ' + dispName(byId[target]) + ' \u2014 that would create a loop.'); return; }
  const beforeParent = effParent(b);
  applyParentOverride(src, target);
  logChange('move', src, 'Moved \u201c' + dispName(byId[src]) + '\u201d under \u201c' + dispName(byId[target]) + '\u201d', beforeParent, target);
  save(); buildKids(); renderNav(); refreshViews();
  if (S.sel === 'buddy:' + src || S.sel === 'buddy:' + target || S.sel === 'buddy:' + ROOT_ID) renderBuddy(S.sel.slice(6));
  offerMoveUndo(src, beforeParent, dispName(b) + ' moved under ' + dispName(byId[target]) + '.');
}
/* FAMKINDS retired 2026-10-11: the org chart now shows every direct report of the
   root side by side; only truly parentless buddies go to the orphan section. */
function nodeTag(b, depth){
  if (depth === 1) {
    if (b.kind === 'work') return 'direct report';
    if (b.kind === 'meta') return 'meta';
    if (b.kind === 'standalone') return 'direct';
    return b.kind || 'family';
  }
  return '';
}
function iconName(b){ return escHtml((b.icon ? b.icon + ' ' : '') + dispName(b)); }
function gridKids(b){
  const kids = visibleKids(b.id);
  if (!kids.length) return '';
  return '<ul class="subkids">' + kids.map(c =>
    '<li><div class="node ' + c.kind + '" data-buddy="' + c.id + '"><div class="name">' + iconName(c) + '</div>'
    + '<div class="desc">' + escHtml(c.tagline || '') + '</div><div class="tag">' + nodeTag(c, 2) + '</div>'
    + gridKids(c) + '</div></li>').join('') + '</ul>';
}
function orgNode(b, depth){
  const kids = visibleKids(b.id);
  const kc = kids.length ? '<span class="kcount">' + kids.length + '</span>' : '';
  const collapsed = kids.length && S.collapsedNodes && S.collapsedNodes[b.id];
  const pill = kids.length ? '<button class="collapse-pill" data-collapse="' + b.id + '" title="' + (collapsed ? 'Expand' : 'Collapse') + ' children">'
    + (collapsed ? '\u203a' : '\u2304') + ' ' + kids.length + '</button>' : '';
  let s = '<li><div class="node ' + b.kind + (collapsed ? ' collapsed' : '') + '" data-buddy="' + b.id + '">' + '<div class="name">' + iconName(b) + kc + '</div>'
    + '<div class="desc">' + escHtml(b.tagline || '') + '</div>'
    + '<div class="tag">' + nodeTag(b, depth) + '</div>' + pill + '</div>';
  if (kids.length && !collapsed) s += '<ul>' + kids.map(c => orgNode(c, depth + 1)).join('') + '</ul>';
  return s + '</li>';
}
function clampTreeSplit(s){
  s = parseFloat(s);
  if (!isFinite(s)) s = 0.72;
  return Math.min(0.9, Math.max(0.45, s));
}
/* ---------- persistent scroll positions ---------- */
function getScrollPos(){ if (!S.scrollPos || typeof S.scrollPos !== 'object') S.scrollPos = {}; return S.scrollPos; }
function saveScrollPos(key, el){ if (el) getScrollPos()[key] = {l: Math.round(el.scrollLeft), t: Math.round(el.scrollTop)}; }
function restoreScrollPos(key, el){
  if (!el) return;
  const p = getScrollPos()[key];
  if (p) { try { el.scrollLeft = p.l || 0; el.scrollTop = p.t || 0; } catch (e) {} }
}
function watchScrollPos(key, el){
  if (!el) return;
  el.dataset.wspKey = key; /* key may change (e.g. per-buddy panel); listener attaches once */
  if (el.dataset.wsp) return;
  el.dataset.wsp = '1';
  let t = null;
  el.addEventListener('scroll', () => {
    clearTimeout(t);
    t = setTimeout(() => { saveScrollPos(el.dataset.wspKey, el); save(); }, 300);
  }, {passive: true});
}
function applyTreeSplit(){
  const orphPane = document.getElementById('treepane-orph');
  const mainPane = document.getElementById('treepane-main');
  const split = document.getElementById('tree-split');
  const orphScroll = document.getElementById('treezoom-orph');
  if (!orphPane || !mainPane || !split || !orphScroll) return;
  const hasOrph = orphScroll.innerHTML.trim().length > 0;
  split.style.display = ''; orphPane.style.display = '';
  if (!hasOrph) {
    /* No orphans: keep a slim drop strip so buddies can always be detached here */
    mainPane.style.flex = '1 1 0'; orphPane.style.flex = '0 0 auto'; return;
  }
  const s = clampTreeSplit(S.treeSplit);
  mainPane.style.flex = s + ' ' + s + ' 0';
  orphPane.style.flex = (1 - s) + ' ' + (1 - s) + ' 0';
}
function initTreeSplit(){
  const sp = document.getElementById('tree-split');
  if (!sp || sp.dataset.splitInit) return;
  sp.dataset.splitInit = '1';
  let sd = null;
  sp.addEventListener('pointerdown', e => {
    if (e.button !== undefined && e.button !== 0) return;
    if (e.isPrimary === false) return;
    sd = { y0: e.clientY, s0: clampTreeSplit(S.treeSplit), pid: e.pointerId };
    try { sp.setPointerCapture(e.pointerId); } catch (err) {}
    e.preventDefault();
  });
  sp.addEventListener('pointermove', e => {
    if (!sd || e.pointerId !== sd.pid) return;
    const tz = document.getElementById('treezoom');
    const h = tz ? tz.getBoundingClientRect().height : 0;
    if (!h) return;
    S.treeSplit = clampTreeSplit(sd.s0 + (e.clientY - sd.y0) / h);
    applyTreeSplit();
  });
  const end = e => { if (sd && (e.pointerId === undefined || e.pointerId === sd.pid)) { sd = null; save(); } };
  sp.addEventListener('pointerup', end);
  sp.addEventListener('pointercancel', end);
}
// All unseen attention items across every buddy — drives Quick Answers and the home-screen icon badge.
function pendingAttentionItems(){
  const items = [];
  (BUDDIES || []).forEach(b => {
    (b.attention || []).forEach(a => {
      const key = b.id + ':' + (a.id || a.text);
      if (!S.seen[key]) items.push({b, a, key});
    });
  });
  return items;
}
// Home-screen icon badge (Badging API: iOS 16.4+ installed web apps, Chromium).
// No permission needed, no service worker — reflects the count while the app is open.
function updateAppBadge(){
  try {
    if (!('setAppBadge' in navigator)) return;
    const n = pendingAttentionItems().length;
    if (n > 0) navigator.setAppBadge(n);
    else if ('clearAppBadge' in navigator) navigator.clearAppBadge();
  } catch (e) {}
}
function quickAnswersHtml(){
  const items = pendingAttentionItems();
  if (!items.length) return '';
  const links = items.slice(0, 12).map(({b, a, key}) =>
    '<span class="qa-chip"><button class="qa-link" data-qa-buddy="'+b.id+'" title="'+escHtml(a.text || '')+'">'
    + '<span class="qa-icon">'+escHtml(buddyDisplayIcon(b))+'</span>'
    + '<span class="qa-text">'+escHtml((a.text || '').slice(0, 60))+'</span></button>'
    + '<button class="qa-done" data-qa-done="'+key+'" title="Mark done">\u2713</button></span>'
  ).join('');
  return '<div id="quick-answers"><div class="qa-label">Quick answers</div><div class="qa-links">'+links+'</div></div>';
}
function getSearchWords(){
  const el = document.getElementById('buddy-search');
  const q = (el ? el.value : '' || '').toLowerCase().trim();
  return q.split(/\s+/).filter(Boolean);
}
function buddyMatchesSearch(b, words){
  if (!words.length) return true;
  const hay = (dispName(b) + ' ' + (b.name || '') + ' ' + (b.tagline || '') + ' ' + effAka(b).join(' ')).toLowerCase();
  return words.every(w => hay.includes(w));
}
// Returns Set of visible buddy IDs under the current search filter, or null if no filter.
// Visible = matching buddies + their ancestors (for hierarchy context) + their descendants.
function getVisibleBuddyIds(){
  const words = getSearchWords();
  if (!words.length) return null;
  const visible = new Set();
  // Mark matching buddies and their descendants
  function mark(id){
    const b = byId[id];
    if (!b) return false;
    const selfMatch = buddyMatchesSearch(b, words);
    let childMatch = false;
    (kidsOf[id] || []).forEach(k => { if (mark(k.id)) childMatch = true; });
    if (selfMatch || childMatch){
      visible.add(id);
      // Add all descendants of a matching buddy
      if (selfMatch){
        (function addDesc(pid){
          (kidsOf[pid] || []).forEach(k => { visible.add(k.id); addDesc(k.id); });
        })(id);
      }
      return true;
    }
    return false;
  }
  ROOT_ORDER.forEach(id => mark(id));
  // Add ancestors of visible buddies for hierarchy context
  const toAdd = [];
  visible.forEach(id => {
    let p = byId[id] ? effParent(byId[id]) : null;
    while (p && !visible.has(p.id)){
      toAdd.push(p.id);
      p = effParent(p);
    }
  });
  toAdd.forEach(id => visible.add(id));
  return visible;
}
// Filtered children accessor — respects the search filter for Atlas lenses
function visibleKids(id){
  const kids = kidsOf[id] || [];
  const vis = getVisibleBuddyIds();
  if (!vis) return kids;
  return kids.filter(k => vis.has(k.id));
}
function renderOrgTree(){
  const root = byId[ROOT_ID];
  const chartType = getChartType();
  // The org chart shows the real hierarchy: every direct report of the root,
  // side by side. Only truly parentless buddies land in the orphan section.
  // Respects the buddy-list search filter (Dave's request 2026-10-12).
  const kids = visibleKids(ROOT_ID);
  let chartHtml;
  if (chartType === 'org') {
    // No root tile — the top level is the staff itself, side by side.
    // (Astro is still the data-model parent; use Change-parent to go top-level.)
    chartHtml = '<div class="chart"><div class="tree tree-no-root"><ul>'
      + kids.map(b => orgNode(b, 1)).join('') + '</ul></div></div>';
  } else {
    chartHtml = '<div class="chart chart-' + chartType + '">' + renderChartMain(chartType, root, kids) + '</div>';
  }
  let orphHtml = '';
  const visOrph = getVisibleBuddyIds();
  const orphans = (kidsOf['__root'] || []).filter(b => b.id !== ROOT_ID && (!visOrph || visOrph.has(b.id)));
  if (orphans.length) {
    orphHtml += '<section class="standalones"><h2>Orphaned buddies</h2>'
      + '<p class="sub">No parent yet &mdash; drag one onto a buddy in the tree to give it a home, or drop it here to detach.</p>'
      + '<div class="grid">'
      + orphans.map(b => '<div class="node ' + b.kind + '" data-buddy="' + b.id + '">' + '<div class="name">' + iconName(b) + '</div>'
        + '<div class="desc">' + escHtml(b.tagline || '') + '</div><div class="tag">' + nodeTag(b, 1) + '</div>'
        + gridKids(b) + '</div>').join('')
      + '</div></section>';
  } else {
    orphHtml += '<section class="standalones empty"><h2>Orphaned buddies</h2>'
      + '<p class="sub">None right now &mdash; drag a buddy here to detach it.</p></section>';
  }
  // UI chrome (Quick answers + lens picker) lives outside the zoomed scroll pane
  // so the zoom control only scales the chart itself.
  document.getElementById('tree-chrome-main').innerHTML = quickAnswersHtml() + chartSwitcherHtml();
  document.getElementById('treezoom-main').innerHTML = chartHtml;
  document.getElementById('treezoom-orph').innerHTML = orphHtml;
  applyTreeSplit();
  updateZoomMin();
  restoreScrollPos('tree:main', document.getElementById('treezoom-main'));
  restoreScrollPos('tree:orph', document.getElementById('treezoom-orph'));
  if (chartType === 'constellation') initConstellation();
  if (chartType === 'halo') initHalo();
}
/* ============ Atlas chart types ============
   Seven visualizations of the same hierarchy. chartType persists in S.
   Each renderer returns the main-pane HTML; the orphan section is shared. */
const CHART_TYPES = [
  {id:'org', label:'Org chart'},
  {id:'lineage', label:'Lineage'},
  {id:'ledger', label:'Ledger'},
  {id:'colonnade', label:'Colonnade'},
  {id:'terrain', label:'Terrain'},
  {id:'halo', label:'Halo'},
  {id:'constellation', label:'Constellation'},
];
function getChartType(){ return S.chartType || 'org'; }
function setChartType(t){ S.chartType = t; save(); renderOrgTree(); }
function closeLensPicker(){
  const dd = document.getElementById('lens-dropdown');
  const scrim = document.getElementById('lens-scrim');
  const pill = document.getElementById('lens-pill');
  if (dd) dd.hidden = true;
  if (scrim) scrim.hidden = true;
  if (pill) pill.setAttribute('aria-expanded', 'false');
}
// Atlas lens picker — Jonny's verdict: one quiet pill, tap to see seven pictures.
// Thumbnails are stylized inline SVGs (icons with ambition, not live renders).
const CHART_BLURBS = {
  org: 'The classic. Top-down tree.',
  halo: 'Radial sunburst — generations as rings.',
  constellation: 'Force-directed — relationships as gravity.',
  terrain: 'Treemap — the family as landscape.',
  lineage: 'Horizontal org chart — time flows left to right.',
  colonnade: 'Miller columns — one level at a time.',
  ledger: 'The indented list, perfected.',
};
function chartThumbSvg(id){
  const s = 'width="64" height="40" viewBox="0 0 64 40" fill="none" stroke="currentColor" stroke-width="1.5"';
  switch(id){
    case 'org': return '<svg ' + s + '><circle cx="32" cy="8" r="4"/><circle cx="16" cy="28" r="4"/><circle cx="48" cy="28" r="4"/><path d="M32 12v6m0 0l-14 6m14-6l14 6"/></svg>';
    case 'halo': return '<svg ' + s + '><circle cx="32" cy="20" r="4"/><circle cx="32" cy="20" r="10"/><circle cx="32" cy="20" r="16"/></svg>';
    case 'constellation': return '<svg ' + s + '><circle cx="14" cy="12" r="3"/><circle cx="34" cy="8" r="3"/><circle cx="50" cy="20" r="3"/><circle cx="28" cy="28" r="3"/><circle cx="46" cy="32" r="3"/><path d="M14 12l20-4m0 0l16 12m-36 8l14-16m18 4l-2 12"/></svg>';
    case 'terrain': return '<svg ' + s + '><rect x="6" y="6" width="52" height="28"/><path d="M6 20h30m-12-14v28m32-28v28m-20-14h20"/></svg>';
    case 'lineage': return '<svg ' + s + '><circle cx="10" cy="20" r="4"/><circle cx="30" cy="12" r="4"/><circle cx="30" cy="28" r="4"/><circle cx="52" cy="20" r="4"/><path d="M14 20h8m0 0l4-6m-4 6l4 6m4-14h12m-12 16h12"/></svg>';
    case 'colonnade': return '<svg ' + s + '><rect x="8" y="6" width="12" height="28"/><rect x="26" y="6" width="12" height="28"/><rect x="44" y="6" width="12" height="28"/></svg>';
    case 'ledger': return '<svg ' + s + '><path d="M8 10h24m-24 8h16m0 8h24m-24 8h12"/></svg>';
    default: return '';
  }
}
function chartSwitcherHtml(){
  const cur = getChartType();
  const curDef = CHART_TYPES.find(c => c.id === cur) || CHART_TYPES[0];
  return '<div class="lens-picker-wrap">'
    + '<button class="lens-pill" id="lens-pill" aria-haspopup="true" aria-expanded="false">'
    + '<span class="lens-pill-icon">◉</span><span>' + curDef.label + '</span><span class="lens-pill-chev">▾</span>'
    + '</button>'
    + '<div class="lens-dropdown" id="lens-dropdown" hidden>'
    + '<button class="lens-close" id="lens-close" aria-label="Close chart picker">&times;</button>'
    + CHART_TYPES.map(c => '<button class="lens-card' + (c.id === cur ? ' sel' : '') + '" data-chart="' + c.id + '">'
      + '<span class="lens-thumb">' + chartThumbSvg(c.id) + '</span>'
      + '<span class="lens-name">' + c.label + (c.id === cur ? ' ✓' : '') + '</span>'
      + '<span class="lens-blurb">' + CHART_BLURBS[c.id] + '</span>'
      + '</button>').join('')
    + '</div></div>'
    + '<div class="lens-scrim" id="lens-scrim" hidden></div>';
}
function renderChartMain(type, root, kids){
  switch(type){
    case 'ledger': return ledgerHtml(root);
    case 'lineage': return lineageHtml(root, kids);
    case 'colonnade': return colonnadeHtml(root);
    case 'terrain': return terrainHtml(root);
    case 'halo': return haloHtml(root);
    case 'constellation': return constellationHtml(root);
    default: return '';
  }
}
/* Ledger — indented list, the hierarchy as a perfected outline */
function ledgerHtml(root){
  function row(b, depth){
    const kids = visibleKids(b.id);
    const collapsed = kids.length && S.collapsedNodes && S.collapsedNodes[b.id];
    const chev = kids.length
      ? '<button class="ledger-chev' + (collapsed ? ' collapsed' : '') + '" data-collapse="' + b.id + '" title="' + (collapsed ? 'Expand' : 'Collapse') + '"><i>\u203a</i></button>'
      : '<span class="ledger-chev-sp"></span>';
    const grip = b.id === ROOT_ID ? '' : '<span class="ledger-grip" data-ledger-grip="' + b.id + '" title="Drag to reparent ' + escHtml(dispName(b)) + '"></span>';
    let s = '<div class="ledger-row" data-buddy="' + b.id + '" style="padding-left:' + (depth * 24 + 12) + 'px">'
      + chev
      + grip
      + '<span class="ledger-name">' + iconName(b) + '</span>'
      + (b.tagline ? '<span class="ledger-desc">' + escHtml(b.tagline) + '</span>' : '')
      + '</div>';
    if (!collapsed) kids.forEach(k => { s += row(k, depth + 1); });
    return s;
  }
  return '<div class="ledger">' + row(root, 0) + '</div>';
}
/* Lineage — horizontal org chart. Root on the left, generations flow right. */
function lineageHtml(root, kids){
  function hNode(b){
    const ch = visibleKids(b.id);
    return '<div class="hgen">'
      + '<div class="node" data-buddy="' + b.id + '"><div class="name">' + iconName(b) + '</div>'
      + '<div class="desc">' + escHtml(b.tagline || '') + '</div></div>'
      + (ch.length ? '<div class="hchildren">' + ch.map(hNode).join('') + '</div>' : '')
      + '</div>';
  }
  return '<div class="lineage"><div class="hgen hroot">'
    + '<div class="node root" data-buddy="' + root.id + '"><div class="name">' + iconName(root) + '</div>'
    + '<div class="desc">' + escHtml(root.tagline || '') + '</div></div>'
    + '<div class="hchildren">' + kids.map(hNode).join('') + '</div>'
    + '</div></div>';
}
/* Colonnade — Miller columns. Each generation is a column; tap to drill. */
function colonnadeHtml(root){
  const colStack = S.colonnadePath || [ROOT_ID];
  // Validate path still exists
  const valid = colStack.filter(id => byId[id]);
  if (!valid.length) valid.push(ROOT_ID);
  let cols = '';
  valid.forEach((id, i) => {
    const b = byId[id];
    const kids = visibleKids(id);
    const isLast = i === valid.length - 1;
    cols += '<div class="mcol' + (isLast ? ' mcol-active' : '') + '">'
      + '<div class="mcol-head">' + iconName(b) + '</div>'
      + kids.map(k => '<div class="mcol-row" data-buddy="' + k.id + '" data-col="' + i + '">'
        + '<span>' + iconName(k) + '</span><span class="mcol-arrow">›</span></div>').join('')
      + '</div>';
  });
  return '<div class="colonnade">' + cols + '</div>';
}
/* Terrain — treemap. Tile area scales with subtree size. */
function terrainHtml(root){
  function size(b){
    let n = 1;
    visibleKids(b.id).forEach(k => { n += size(k); });
    return n;
  }
  function tile(b){
    const kids = visibleKids(b.id);
    const s = size(b);
    if (!kids.length) {
      return '<div class="tm-tile tm-leaf" data-buddy="' + b.id + '" style="flex:' + s + '">'
        + '<span class="tm-name">' + iconName(b) + '</span></div>';
    }
    return '<div class="tm-tile tm-branch" style="flex:' + s + '">'
      + '<div class="tm-label" data-buddy="' + b.id + '">' + iconName(b) + '</div>'
      + '<div class="tm-kids">' + kids.map(tile).join('') + '</div></div>';
  }
  return '<div class="terrain">' + tile(root) + '</div>';
}
/* Halo — radial sunburst. The selected buddy is the sun; generations orbit. */
function haloHtml(root){
  const centerId = S.haloCenter || ROOT_ID;
  const center = byId[centerId] || root;
  return '<div class="halo-wrap">'
    + '<svg id="halo-svg" viewBox="0 0 600 600" data-center="' + center.id + '"></svg>'
    + '<div class="halo-center-label" data-buddy="' + center.id + '">' + iconName(center) + '</div>'
    + '</div>';
}
function initHalo(){
  const svg = document.getElementById('halo-svg');
  if (!svg) return;
  const centerId = svg.dataset.center;
  const center = byId[centerId];
  if (!center) return;
  const NS = 'http://www.w3.org/2000/svg';
  const cx = 300, cy = 300;
  svg.innerHTML = '';
  // Rings: center, children, grandchildren
  function ring(b, r0, r1, a0, a1, depth){
    if (depth > 2) return;
    const kids = visibleKids(b.id);
    if (!kids.length) return;
    const span = (a1 - a0) / kids.length;
    kids.forEach((k, i) => {
      const sa = a0 + i * span, ea = a0 + (i + 1) * span;
      const path = document.createElementNS(NS, 'path');
      const x0 = cx + r0 * Math.cos(sa), y0 = cy + r0 * Math.sin(sa);
      const x1 = cx + r1 * Math.cos(sa), y1 = cy + r1 * Math.sin(sa);
      const x2 = cx + r1 * Math.cos(ea), y2 = cy + r1 * Math.sin(ea);
      const x3 = cx + r0 * Math.cos(ea), y3 = cy + r0 * Math.sin(ea);
      const large = (ea - sa) > Math.PI ? 1 : 0;
      path.setAttribute('d', 'M' + x0 + ',' + y0 + ' L' + x1 + ',' + y1
        + ' A' + r1 + ',' + r1 + ' 0 ' + large + ' 1 ' + x2 + ',' + y2
        + ' L' + x3 + ',' + y3
        + ' A' + r0 + ',' + r0 + ' 0 ' + large + ' 0 ' + x0 + ',' + y0 + ' Z');
      path.setAttribute('class', 'halo-arc');
      path.dataset.buddy = k.id;
      // Label
      const mid = (sa + ea) / 2, lr = (r0 + r1) / 2;
      const tx = cx + lr * Math.cos(mid), ty = cy + lr * Math.sin(mid);
      const text = document.createElementNS(NS, 'text');
      text.setAttribute('x', tx); text.setAttribute('y', ty);
      text.setAttribute('class', 'halo-label');
      text.setAttribute('text-anchor', 'middle');
      text.textContent = (k.icon ? k.icon + ' ' : '') + dispName(k);
      text.dataset.buddy = k.id;
      svg.appendChild(path); svg.appendChild(text);
      ring(k, r1 + 8, r1 + 68, sa, ea, depth + 1);
    });
  }
  // Center circle
  const c = document.createElementNS(NS, 'circle');
  c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', 70);
  c.setAttribute('class', 'halo-center');
  c.dataset.buddy = center.id;
  svg.appendChild(c);
  ring(center, 78, 148, 0, Math.PI * 2, 0);
}
/* Constellation — force-directed star map. Relationships as gravity. */
function constellationHtml(root){
  return '<div class="constellation-wrap"><canvas id="constellation-canvas"></canvas></div>';
}
function initConstellation(){
  const canvas = document.getElementById('constellation-canvas');
  if (!canvas) return;
  const wrap = canvas.parentElement;
  const W = wrap.clientWidth || 800, H = Math.max(500, wrap.clientHeight || 600);
  canvas.width = W * 2; canvas.height = H * 2;
  canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(2, 2);
  // Build node list (cap at 120 for perf)
  const nodes = [], edges = [], seen = {};
  function walk(b, depth){
    if (seen[b.id] || nodes.length >= 120) return;
    seen[b.id] = true;
    nodes.push({id: b.id, b: b, x: W/2 + (Math.random()-0.5)*W*0.6, y: H/2 + (Math.random()-0.5)*H*0.6,
      vx: 0, vy: 0, r: depth === 0 ? 14 : Math.max(6, 10 - depth)});
    if (depth < 4) visibleKids(b.id).forEach(k => {
      if (!seen[k.id] && nodes.length < 120) edges.push([b.id, k.id]);
      walk(k, depth + 1);
    });
  }
  walk(byId[ROOT_ID], 0);
  const byNodeId = {};
  nodes.forEach(n => { byNodeId[n.id] = n; });
  // Physics loop
  let ticks = 0;
  function tick(){
    if (ticks++ > 300) return;
    // Repulsion
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        let dx = a.x - b.x, dy = a.y - b.y;
        let d2 = dx*dx + dy*dy;
        if (d2 < 1) d2 = 1;
        if (d2 > 40000) continue;
        const f = 3200 / d2;
        const d = Math.sqrt(d2);
        dx /= d; dy /= d;
        a.vx += dx * f; a.vy += dy * f;
        b.vx -= dx * f; b.vy -= dy * f;
      }
    }
    // Springs
    edges.forEach(([id1, id2]) => {
      const a = byNodeId[id1], b = byNodeId[id2];
      if (!a || !b) return;
      const dx = b.x - a.x, dy = b.y - a.y;
      const d = Math.sqrt(dx*dx + dy*dy) || 1;
      const f = (d - 90) * 0.02;
      a.vx += dx / d * f; a.vy += dy / d * f;
      b.vx -= dx / d * f; b.vy -= dy / d * f;
    });
    // Gravity to center + damping
    nodes.forEach(n => {
      n.vx += (W/2 - n.x) * 0.002; n.vy += (H/2 - n.y) * 0.002;
      n.vx *= 0.85; n.vy *= 0.85;
      n.x += n.vx; n.y += n.vy;
      n.x = Math.max(30, Math.min(W - 30, n.x));
      n.y = Math.max(30, Math.min(H - 30, n.y));
    });
    draw();
    requestAnimationFrame(tick);
  }
  function draw(){
    ctx.clearRect(0, 0, W, H);
    const isLight = document.documentElement.classList.contains('light');
    // Edges
    ctx.strokeStyle = isLight ? 'rgba(31,35,40,.14)' : 'rgba(255,255,255,.12)';
    ctx.lineWidth = 1;
    edges.forEach(([id1, id2]) => {
      const a = byNodeId[id1], b = byNodeId[id2];
      if (!a || !b) return;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    });
    // Nodes
    nodes.forEach(n => {
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = n.id === ROOT_ID ? '#f0a35e' : (isLight ? '#fff' : '#161b22');
      ctx.fill();
      ctx.strokeStyle = isLight ? '#d0d7de' : '#30363d';
      ctx.stroke();
      // Label
      ctx.fillStyle = isLight ? '#1f2328' : '#e6edf3';
      ctx.font = '11px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      const label = (n.b.icon ? n.b.icon + ' ' : '') + dispName(n.b);
      ctx.fillText(label.length > 18 ? label.slice(0, 17) + '…' : label, n.x, n.y + n.r + 13);
    });
  }
  // Click to open buddy
  canvas.addEventListener('click', e => {
    const r = canvas.getBoundingClientRect();
    const mx = e.clientX - r.left, my = e.clientY - r.top;
    for (const n of nodes) {
      const d = Math.hypot(n.x - mx, n.y - my);
      if (d < n.r + 8) { show('buddy:' + n.id); break; }
    }
  });
  tick();
}
/* Release Notes view — same format as the What's New update modal:
   "new since you last looked" on top, earlier history below. */
function renderReleases(){
  const el = document.getElementById('view-releases');
  if (!el) return;
  el.innerHTML = '<section class="changelog" style="margin:24px auto 0;max-width:860px">'
    + '<h2>Release Notes</h2>'
    + '<p class="sub">What shipped, newest first.</p>'
    + '<div id="releases-body"><p class="fineprint">Loading…</p></div></section>';
  const body = el.querySelector('#releases-body');
  fetch('https://raw.githubusercontent.com/davedellaquila/buddy-system/master/CHANGELOG.md?_=' + Date.now(), {cache: 'no-store'})
    .then(r => { if (!r.ok) throw new Error('fetch failed'); return r.text(); })
    .then(md => {
      const sp = whatsnewSplit(md);
      let html = '';
      if (sp.hasNew) {
        html += '<h4 style="margin-top:0">New since you last looked</h4>' + releaseNotesToHtml(sp.newMd);
      } else {
        html += '<p class="fineprint" style="margin-top:0">You’re up to date — nothing new since you last looked.</p>';
      }
      if (sp.oldMd.trim()) {
        html += '<div style="display:flex;align-items:baseline;gap:16px;margin-top:12px;flex-wrap:wrap">'
          + '<details style="flex:1;min-width:0"><summary class="fineprint" style="cursor:pointer">Earlier history</summary>'
          + releaseNotesToHtml(sp.oldMd) + '</details>'
          + '<p class="fineprint" style="margin:0;white-space:nowrap"><a href="https://github.com/davedellaquila/buddy-system/blob/master/CHANGELOG.md" target="_blank" rel="noopener">Earlier changes on GitHub</a></p>'
          + '</div>';
      } else {
        html += '<p class="fineprint"><a href="https://github.com/davedellaquila/buddy-system/blob/master/CHANGELOG.md" target="_blank" rel="noopener">Earlier changes on GitHub</a></p>';
      }
      body.innerHTML = html;
      whatsnewMarkSeen(md);
    })
    .catch(() => { body.innerHTML = '<p class="fineprint">Couldn’t load the release notes. <a href="https://github.com/davedellaquila/buddy-system/blob/master/CHANGELOG.md" target="_blank" rel="noopener">View on GitHub</a>.</p>'; });
}
// Briefly highlight a project row after "All buddies" navigation — shows you where you came from.
let pendingHighlight = null;
function highlightProjectRow(id){
  requestAnimationFrame(() => {
    const row = document.querySelector('#view-projects .proj-row[data-buddy="' + id + '"]');
    if (!row) return;
    row.scrollIntoView({block:'center', behavior:'smooth'});
    row.classList.add('flash-highlight');
    setTimeout(() => row.classList.remove('flash-highlight'), 2500);
  });
}
function renderProjects(){
  if (!S.projCollapsed || typeof S.projCollapsed !== 'object') S.projCollapsed = {};
  const weekAgo = Date.now() - 7 * 864e5;
  // Compute the exact set of buddy IDs a filter shows (matching buddies +
  // their ancestors, for hierarchy context). Tile counts use this so the
  // number on the tile always matches the filtered row count.
  function idsForFilter(kind, val){
    const ids = {};
    const addWithAncestors = b => {
      let x = b;
      while (x) { ids[x.id] = true; const p = effParent(x); x = p ? byId[p] : null; }
    };
    if (kind === 'attention') {
      const matches = b => (b.attention || []).some(a => {
        const seen = !!S.seen[a.id];
        if (val === 'unseen') return !seen;
        if (val === 'cleared') return seen;
        const t = Date.parse(a.date || '');
        return t && t >= weekAgo;
      });
      Object.values(byId).forEach(b => { if (matches(b)) addWithAncestors(b); });
    } else if (kind === 'status') {
      Object.values(byId).forEach(b => { if ((b.status || 'Unknown') === val) addWithAncestors(b); });
    }
    return ids;
  }
  const unseenIds = idsForFilter('attention', 'unseen');
  const freshIds = idsForFilter('attention', 'fresh');
  const clearedIds = idsForFilter('attention', 'cleared');
  const statusCounts = {};
  const statusIds = {};
  Object.values(byId).forEach(b => {
    const st = b.status || 'Unknown';
    (statusIds[st] = statusIds[st] || {});
    let x = b;
    while (x) { statusIds[st][x.id] = true; const p = effParent(x); x = p ? byId[p] : null; }
  });
  Object.keys(statusIds).forEach(st => statusCounts[st] = Object.keys(statusIds[st]).length);
  // Status tint colors (match the pills)
  const statusTints = {'Active':'#1f6feb','Live · M2 shipped':'#2f9e44','Live · pre-alpha':'#2f9e44','New':'#d97a1f','Mission review':'#a371f7','PRD review':'#a371f7','Pilot':'#1f6feb','Spec review':'#a371f7'};
  const statusOrder = Object.keys(statusCounts).sort();
  // Visible sum for the TO REVIEW tile (Jonny: one tile language)
  const revBits = [];
  if (statusCounts['Mission review']) revBits.push(statusCounts['Mission review'] + ' mission');
  if (statusCounts['PRD review']) revBits.push(statusCounts['PRD review'] + ' PRD');
  if (statusCounts['Spec review']) revBits.push(statusCounts['Spec review'] + ' spec');
  const revSub = revBits.length ? revBits.join(' \u00b7 ') : 'Needs your attention';
  let s = '<section class="projects-view" style="margin-top:24px">'
    + '<div id="project-tiles">'
    + tileHtml('TO REVIEW', Object.keys(unseenIds).length, '#a371f7', revSub, 'unseen', projFilter === 'unseen')
    + tileHtml('FRESH', Object.keys(freshIds).length, '#d97a1f', 'Added in the last 7 days', 'fresh', projFilter === 'fresh')
    + tileHtml('CLEARED', Object.keys(clearedIds).length, '#2f9e44', 'Reviewed & cleared', 'cleared', projFilter === 'cleared')
    + '</div>'
    + '<div id="project-status-tiles" style="margin-top:12px">'
    + statusOrder.map(st => tileHtml(st.replace(/^Live · /i, '').toUpperCase(), statusCounts[st], statusTints[st] || '#8b949e', '', 'status:' + st, statusFilter === st, 'Click to filter by ' + st + ' status. Click again to clear.')).join('')
    + '</div>'
    + '<h2>Projects by Buddy</h2>'
    + '<div class="proj-search-sentinel" aria-hidden="true"></div>'
    + '<div class="proj-search-sticky"><div class="proj-controls">'
    + '<div class="sb-search-wrap" style="flex:1;min-width:0">'
    + '<input type="search" id="proj-search" placeholder="Search projects\u2026" aria-label="Search projects" value="'+escHtml(projSearch)+'">'
    + '<button type="button" id="proj-search-clear" aria-label="Clear search" title="Clear search"'+(projSearch?'':' hidden')+'>\u00d7</button>'
    + '</div>'
    + '<div class="proj-mode-toggle" role="group" aria-label="List layout">'
    + '<button type="button" data-proj-mode="hier" class="'+(projViewMode==='hier'?'sel':'')+'" title="Hierarchical listing">\u2630</button>'
    + '<button type="button" data-proj-mode="alpha" class="'+(projViewMode==='alpha'?'sel':'')+'" title="Alphabetical listing">A\u2013Z</button>'
    + '</div></div></div>'
    + '<p class="sub">'+(projViewMode==='alpha'?'Every buddy, A to Z, with its current status.':'Every buddy, in hierarchy order, with its current status.')+'</p><div class="proj-list">';
  // When a tile filter is active, show matching buddies plus their ancestors.
  // Uses idsForFilter so the row count always matches the tile count.
  let showIds = null;
  if (projFilter) {
    showIds = idsForFilter('attention', projFilter);
  } else if (statusFilter) {
    showIds = idsForFilter('status', statusFilter);
  }
  // Text search: match name or tagline, show matches plus their ancestors
  if (projSearch) {
    const q = projSearch.toLowerCase();
    const sm = {};
    Object.values(byId).forEach(b => {
      const hay = ((b.name || '') + ' ' + (b.tagline || '')).toLowerCase();
      if (!hay.includes(q)) return;
      let x = b;
      while (x) { sm[x.id] = true; const p = effParent(x); x = p ? byId[p] : null; }
    });
    showIds = showIds ? Object.keys(showIds).filter(id => sm[id]).reduce((o, id) => (o[id] = true, o), {}) : sm;
  }
  const projRowHtml = b => '<div class="proj-row" data-buddy="' + b.id + '">'
      + '<div class="proj-row-head">'
      + '<span class="pname">' + iconName(b) + '</span>'
      + '<span class="status ' + b.statusClass + '">' + escHtml(b.status) + '</span>'
      + '<button class="proj-info" data-proj-info="' + b.id + '" title="Open ' + escHtml(dispName(b)) + ' details (right panel)" style="background:none;border:none;cursor:pointer;font-size:16px;padding:4px 8px;opacity:0.6" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.6">\u24d8</button>'
      + '</div>'
      + '<span class="pdesc">' + escHtml(b.tagline || '') + '</span></div>';
  if (projViewMode === 'alpha') {
    // Flat A-Z listing; search/tile filters narrow the set
    Object.values(byId)
      .filter(b => !showIds || showIds[b.id])
      .sort((a, b) => dispName(a).toLowerCase().localeCompare(dispName(b).toLowerCase()))
      .forEach(b => { s += projRowHtml(b); });
  } else {
    (function walk(id, depth){
      const b = byId[id]; if (!b) return;
      if (showIds && !showIds[id]) return;
      const kids = visibleKids(id);
      const hasKids = kids.length > 0;
      const collapsed = (projFilter || statusFilter) ? false : !!S.projCollapsed[id];
      s += '<div class="proj-row d' + Math.min(depth, 3) + '" data-buddy="' + b.id + '">'
        + '<div class="proj-row-head">'
        + (hasKids ? '<span class="parrow ' + (collapsed ? '' : 'expanded') + '" data-proj-toggle="' + b.id + '">\u203a</span>' : '')
        + '<span class="pname">' + iconName(b) + '</span>'
        + '<span class="status ' + b.statusClass + '">' + escHtml(b.status) + '</span>'
        + '<button class="proj-info" data-proj-info="' + b.id + '" title="Open ' + escHtml(dispName(b)) + ' details (right panel)" style="background:none;border:none;cursor:pointer;font-size:16px;padding:4px 8px;opacity:0.6" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.6">\u24d8</button>'
        + '</div>'
        + '<span class="pdesc">' + escHtml(b.tagline || '') + '</span></div>';
      if (!collapsed) kids.forEach(c => walk(c.id, depth + 1));
    })(ROOT_ID, 0);
  }
  s += '</div></section>';
  const vp = document.getElementById('view-projects');
  vp.innerHTML = s;
  // Stuck-state detection for the search pill: sentinel scrolls away -> pill is stuck
  try {
    if (projStickObs) projStickObs.disconnect();
    const sent = vp.querySelector('.proj-search-sentinel');
    const pill = vp.querySelector('.proj-search-sticky');
    if (sent && pill && 'IntersectionObserver' in window) {
      projStickObs = new IntersectionObserver(en => {
        pill.classList.toggle('is-stuck', !en[0].isIntersecting);
      }, {threshold: 0});
      projStickObs.observe(sent);
    }
  } catch (err) {}
}
function refreshViews(){
  // Always re-render the tree from current data. Restoring a cached copy left
  // renamed / re-iconed tiles stale, and broke "reset tree" after reparenting.
  renderOrgTree();
  renderProjects();
}
function applyZoom(){
  const m = document.getElementById('treezoom-main');
  const o = document.getElementById('treezoom-orph');
  if (m) m.style.zoom = (S.zoom || 100) + '%';
  if (o) o.style.zoom = (S.zoomOrph || 100) + '%';
  const r1 = document.getElementById('zoomrange-main');
  const r2 = document.getElementById('zoomrange-orph');
  if (r1) r1.value = S.zoom || 100;
  if (r2) r2.value = S.zoomOrph || 100;
  requestAnimationFrame(centerIfFits);
}
function centerIfFits(){
  [['treezoom-main'],['treezoom-orph']].forEach(([paneId]) => {
    const sc = document.getElementById(paneId);
    if (!sc) return;
    const content = sc.querySelector('.chart') || sc.querySelector('.standalones');
    if (!content) return;
    const fits = content.scrollHeight <= sc.clientHeight + 1 && content.scrollWidth <= sc.clientWidth + 1;
    sc.classList.toggle('fit-centered', fits);
  });
}
function fitZoomFor(paneId){
  const sc = document.getElementById(paneId);
  const content = sc ? (sc.querySelector('.chart') || sc.querySelector('.standalones')) : null;
  if (!sc || !content) return 25;
  const z = 1; // measure at natural size
  const natW = content.scrollWidth, natH = content.scrollHeight;
  const vw = sc.clientWidth, vh = sc.clientHeight;
  if (!natW || !natH || !vw || !vh) return 25;
  return Math.max(5, Math.min(100, Math.floor(Math.min(vw / natW, vh / natH) * 100 / 5) * 5));
}
function updateZoomMin(){
  [['treezoom-main','zoomrange-main','zoom'],['treezoom-orph','zoomrange-orph','zoomOrph']].forEach(([pane, range, key]) => {
    const r = document.getElementById(range);
    if (!r) return;
    const fit = fitZoomFor(pane);
    r.min = fit;
    if ((S[key] || 100) < fit) { S[key] = fit; }
  });
  save(); applyZoom();
}
function zoomToFit(paneId, zoomKey){
  const sc = document.getElementById(paneId);
  const content = sc ? (sc.querySelector('.chart') || sc.querySelector('.standalones')) : null;
  if (!sc || !content) return;
  const z = (S[zoomKey] || 100) / 100;
  const natW = content.scrollWidth / z, natH = content.scrollHeight / z;
  const vw = sc.clientWidth, vh = sc.clientHeight;
  if (!natW || !natH || !vw || !vh) return;
  const fit = Math.min(vw / natW, vh / natH) * 100;
  S[zoomKey] = Math.min(160, Math.max(5, Math.round(fit / 5) * 5));
  save(); applyZoom();
  toast('Zoomed to fit (' + S[zoomKey] + '%).');
}
(function initZoom(){
  const vt = document.getElementById('view-tree');
  function zoombarHTML(sfx, label){
    return '<div class="zoombar" id="zoombar-' + sfx + '" title="Zoom — pinch with two fingers, or Shift+scroll">'
      + '<span class="z-in" aria-hidden="true">\u25fc</span>'
      + '<input type="range" class="zrange" id="zoomrange-' + sfx + '" min="5" max="160" step="5" value="100" aria-label="' + label + '" orient="vertical">'
      + '<span class="z-out" aria-hidden="true">\u25aa</span>'
      + '<button type="button" class="zfit" id="zoomfit-' + sfx + '" title="Zoom to fit" aria-label="Zoom to fit">\u26f6</button></div>';
  }
  vt.insertAdjacentHTML('afterbegin',
    '<div class="treewrap" id="zoomwrap"><div id="treezoom">'
    + '<div class="treepane" id="treepane-main">' + zoombarHTML('main', 'Buddy tree zoom')
    + '<div class="tree-chrome" id="tree-chrome-main"></div>'
    + '<div class="treescroll" id="treezoom-main" data-zoomkey="zoom" data-treepane="1"></div></div>'
    + '<div id="tree-split" title="Drag to resize the tree and orphan panes"><div class="split-grip"></div></div>'
    + '<div class="treepane" id="treepane-orph">' + zoombarHTML('orph', 'Orphaned buddies zoom')
    + '<div class="treescroll" id="treezoom-orph" data-zoomkey="zoomOrph" data-treepane="1"></div></div>'
    + '</div></div>');
  const tw = document.getElementById('zoomwrap');
  const main = document.getElementById('treezoom-main');
  Array.from(vt.childNodes).forEach(n => { if (n !== tw) main.appendChild(n); });
  watchScrollPos('tree:main', document.getElementById('treezoom-main'));
  watchScrollPos('tree:orph', document.getElementById('treezoom-orph'));
  document.getElementById('zoomrange-main').addEventListener('input', e => {
    S.zoom = parseInt(e.target.value, 10) || 100; save(); applyZoom();
  });
  document.getElementById('zoomfit-main').addEventListener('click', () => zoomToFit('treezoom-main', 'zoom'));
  document.getElementById('zoomrange-orph').addEventListener('input', e => {
    S.zoomOrph = parseInt(e.target.value, 10) || 100; save(); applyZoom();
  });
  document.getElementById('zoomfit-orph').addEventListener('click', () => zoomToFit('treezoom-orph', 'zoomOrph'));
  initTreeSplit();
  applyZoom();
  applyTreeSplit();
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
  // Each .treescroll pane is its own 2D scrollport (both axes). Do not pan nested
  // .chart — overflow-x-only on .chart caused Safari/iOS to lock the first gesture axis.
  function scroller(){ return el; }
  const isTree = el.id === 'treezoom' || el.dataset.treepane === '1';
  const zoomKey = el.dataset.zoomkey || 'zoom';
  function pinchHost(){ return (el.closest && el.closest('#treezoom')) || el; }
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
    // Apply both axes every move — free diagonal pan (no axis lock).
    // Scale the finger delta by 1/zoom: scroll offsets live in the zoomed
    // coordinate space, so without this a 50% zoom pans at 2:1 (geared down).
    // Then apply the nerd-setting pan gearing multiplier (default 1x).
    const zf = (S[zoomKey] || 100) / 100;
    const gear = parseFloat(S.panGearing) || 1;
    sc.scrollLeft = pan.sl - dx / zf * gear;
    sc.scrollTop = pan.st - dy / zf * gear;
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
    pinch = { d0: d0, z0: S[zoomKey] || 100 };
    pinchHost().dataset.pinching = '1';
    el.classList.add('panning');
    swallow = true;
  }
  function movePinch(){
    if (!pinch || pts.size < 2) return;
    const d = pinchDist();
    const next = Math.min(160, Math.max(25, Math.round((pinch.z0 * (d / pinch.d0)) / 5) * 5));
    if (next !== (S[zoomKey] || 100)) { S[zoomKey] = next; applyZoom(); }
  }
  function endPinchFinger(pid){
    pts.delete(pid);
    if (pts.size < 2 && pinch) {
      pinch = null;
      delete pinchHost().dataset.pinching;
      el.classList.remove('panning');
      save();
      setTimeout(() => { swallow = false; }, 80);
    }
  }
  // Pointer Events — mouse + touch/pen on the tree (touch-action:none) for free 2D pan
  el.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    if (!isTree && e.pointerType !== 'mouse') return; // projects/manifest keep native touch scroll
    // Left-edge strip is owned by initEdgeSwipeOpen (open drawer) — don't start a pan.
    if (isTree && e.pointerType !== 'mouse' && typeof isDrawerNav === 'function' && isDrawerNav()
        && typeof isSidebarOpen === 'function' && !isSidebarOpen() && e.clientX <= 24) return;
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
  attachPan(document.getElementById('treezoom-main'));
  attachPan(document.getElementById('treezoom-orph'));
  attachPan(document.getElementById('view-projects'));
  attachPan(document.getElementById('view-manifest'));
}
initPan();
/* ---------- tree node drag-to-reparent (pointer events: mouse + touch) ----------
   Press-and-hold a node (~400ms) to arm it, then move >6px to drag it; a
   simple tap still opens the buddy detail panel. Works with mouse and touch
   (HTML5 DnD never fires on touch, which is why the old gripper handles could
   not work there). Dragging a node reparents it; dragging empty background
   pans the chart. */
let nodeDragEndAt = 0; // timestamp of last node-drag gesture; used to swallow the follow-up click
(function initNodeDrag(){
  const tz = document.getElementById('treezoom');
  if (!tz) return;
  const THRESH = 6; // px of movement before an armed press becomes a drag (less = click)
  const HOLD_MS = 400; // press-and-hold delay: a node must be held this long before it can be dragged
  let cand = null;  // {id, x0, y0, pid, touch, armed, timer} — pressed on a node, drag not yet armed/started
  let drag = null;  // {id, pid, ghost, target} — active drag

  function treeNodeFrom(el){
    return (el && el.closest) ? el.closest('#treezoom .node[data-buddy], #treezoom .ledger-row[data-buddy]') : null;
  }
  function dragSrcEl(id){
    return tz.querySelector('.node[data-buddy="' + id + '"], .ledger-row[data-buddy="' + id + '"]');
  }
  var TOUCH_SLOP = 16; // px of extra hit area around each node during a touch drag
  function nodeAt(x, y, touch){
    if (!touch) return treeNodeFrom(document.elementFromPoint(x, y));
    // Touch: finger covers the exact point, so test inflated rects and take the smallest match.
    var nodes = tz.querySelectorAll('.node[data-buddy], .ledger-row[data-buddy]'), best = null, bestArea = Infinity;
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
    tz.querySelectorAll('.node.drop-target,.node.drop-invalid,.ledger-row.drop-target,.ledger-row.drop-invalid').forEach(function(x){ x.classList.remove('drop-target', 'drop-invalid'); });
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
    if (tid === ROOT_ID || !isDesc(tid, drag.id)) {
      n.classList.add('drop-target'); drag.target = tid; // valid (root included)
    } else {
      n.classList.add('drop-invalid'); // dropping here would create a cycle
    }
  }
  function cleanup(){
    clearHl();
    tz.querySelectorAll('.node.drag-src,.node.drag-armed,.ledger-row.drag-src,.ledger-row.drag-armed').forEach(function(x){ x.classList.remove('drag-src', 'drag-armed'); });
    if (drag && drag.ghost && drag.ghost.parentNode) drag.ghost.parentNode.removeChild(drag.ghost);
    document.body.classList.remove('node-dragging');
    if (cand && cand.timer) clearTimeout(cand.timer);
    drag = null; cand = null;
  }
  function beginDrag(x, y){
    const c = cand, id = c.id;
    const src = dragSrcEl(id);
    const ghost = document.createElement('div');
    ghost.className = 'node-drag-ghost';
    let label = id;
    if (src) {
      const nm = src.querySelector('.name, .ledger-name');
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
    if (!id || id === ROOT_ID) return; // root can't be reparented
    const isLedger = n.classList.contains('ledger-row');
    const onGrip = e.target.closest && e.target.closest('[data-ledger-grip]');
    // Ledger rows drag only from their gripper; the row itself stays tappable.
    if (isLedger && !onGrip) return;
    if (cand && cand.timer) clearTimeout(cand.timer);
    cand = { id: id, x0: e.clientX, y0: e.clientY, pid: e.pointerId, touch: e.pointerType === 'touch', armed: false, timer: null };
    if (isLedger) {
      // The gripper is an explicit drag affordance — arm immediately, no hold.
      cand.armed = true;
      n.classList.add('drag-armed');
    } else {
      // Press-and-hold: the node becomes draggable only after HOLD_MS. A quick
      // tap (down+up before the timer) never enters drag mode — it opens the panel.
      cand.timer = setTimeout(function(){
        if (!cand || drag) return;
        cand.armed = true;
        const src = dragSrcEl(cand.id);
        if (src) src.classList.add('drag-armed');
      }, HOLD_MS);
    }
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
      if (cand.armed && dx * dx + dy * dy > THRESH * THRESH) beginDrag(e.clientX, e.clientY);
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
    if (cand && e.pointerId === cand.pid) {
      if (cand.timer) clearTimeout(cand.timer);
      const src = dragSrcEl(cand.id);
      if (src) src.classList.remove('drag-armed');
      cand = null;
    }
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
        // Set explicit orphan: parent = null override
        S.parents[src] = null;
        logChange('move', src, 'Detached \u201c' + dispName(b) + '\u201d (now orphaned)', beforeParent, null);
        save(); buildKids(); renderNav(); refreshViews();
        if (S.sel === 'buddy:' + src || S.sel === 'buddy:' + ROOT_ID) renderBuddy(S.sel.slice(6));
        offerMoveUndo(src, beforeParent, dispName(b) + ' detached \u2014 now an orphan.');
      }
    }
  });
  document.addEventListener('dragend', () => { dragId = null; clearHl(); });
})();
document.addEventListener('click', e => {
  const qd = e.target.closest('[data-qa-done]');
  if (qd) {
    e.stopImmediatePropagation();
    S.seen[qd.dataset.qaDone] = Date.now();
    save(); renderOrgTree(); renderNav(); updateAppBadge();
    return;
  }
  const cp = e.target.closest('[data-collapse]');
  if (cp) {
    e.stopImmediatePropagation();
    const bid = cp.dataset.collapse;
    if (!S.collapsedNodes || typeof S.collapsedNodes !== 'object') S.collapsedNodes = {};
    S.collapsedNodes[bid] = !S.collapsedNodes[bid];
    save(); renderOrgTree();
    return;
  }
  const qa = e.target.closest('[data-qa-buddy]');
  if (qa) { openBuddy(qa.dataset.qaBuddy); return; }
});
document.getElementById('view-tree').addEventListener('wheel', e => {
  if (!e.shiftKey) return;
  e.preventDefault();
  const pane = e.target && e.target.closest ? e.target.closest('.treescroll') : null;
  const key = (pane && pane.dataset.zoomkey) || 'zoom';
  S[key] = Math.min(160, Math.max(25, (S[key] || 100) + (e.deltaY > 0 ? -5 : 5)));
  save(); applyZoom();
}, { passive: false });
let dragId = null;
(function initDrag(){
  const nav = document.getElementById('buddy-nav');
  nav.addEventListener('dragstart', e => {
    const r = e.target.closest('[data-buddy]');
    if (!r || r.dataset.buddy === ROOT_ID) { e.preventDefault(); return; }
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
    + '<div class="bp-sec"><h3>Private notes<span class="info-tip" data-tip="Saved on this device. (For your eyes only)">\\u24d8</span></h3><textarea class="notes" id="bp-notes" placeholder="Scratch pad for this plan\\u2026 (For your eyes only)">'+escHtml(S.notes[id]||'')+'</textarea>'
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
  // Shift+Arrow: create buddy relative to the selected one (Left = configurable)
  if (e.shiftKey && ['ArrowUp','ArrowDown','ArrowRight','ArrowLeft'].includes(e.key)) {
    if (S.projectId && byId[S.projectId]) {
      if (e.key === 'ArrowLeft') {
        const act = (typeof getSetting === 'function') ? getSetting('shiftLeftAction') : 'promote';
        if (act === 'promote') promoteBuddy(S.projectId);
        else if (act === 'go to parent') { const p = effParent(byId[S.projectId]); if (p && byId[p]) openBuddy(p); }
        // 'nothing' → do nothing
      } else {
        const mode = e.key === 'ArrowUp' ? 'parent' : e.key === 'ArrowDown' ? 'child' : 'sibling';
        openAddBuddyDialog(mode, S.projectId);
      }
      e.preventDefault();
    }
    return;
  }
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
      if (sel === 'view:releases') renderReleases();
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
    : sel.startsWith('buddy:') ? ((byId[sel.slice(6)] || {}).icon) : byId[ROOT_ID].icon);
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
  if (e.key === '-' || e.key === '_') { S.zoom = Math.max(5, (S.zoom || 100) - 5); save(); applyZoom(); return; }
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
  applyFontScale();
  updateAppBadge();
  const h = document.getElementById('sb-resize');
  let sx = null, sw = 0, sdrag = false, snapped = false;
  const SNAP_SHUT = 140; /* drag narrower than this → snap the sidebar closed */
  h.addEventListener('pointerdown', e => { sx = e.clientX; sw = sb.getBoundingClientRect().width; sdrag = false; snapped = false; });
  h.addEventListener('pointermove', e => {
    if (sx === null || snapped) return;
    if (!sdrag) {
      if (Math.abs(e.clientX - sx) < 6) return; /* tap slop: don't resize on a plain tap */
      sdrag = true;
      try { h.setPointerCapture(e.pointerId); } catch (err) {}
      e.preventDefault();
    }
    const raw = sw + e.clientX - sx;
    if (raw < SNAP_SHUT) {
      /* Pushed through the threshold — snap shut instead of stopping at min width */
      snapped = true;
      setSidebarOpen(false);
      sx = null;
      return;
    }
    const w = sbClampW(raw);
    sb.style.width = w + 'px'; sb.style.flex = '0 0 ' + w + 'px';
    document.documentElement.style.setProperty('--sbw', w + 'px');
  });
  const done = () => {
    if (sx === null) return; sx = null;
    if (!sdrag || snapped) return;
    S.sbWidth = Math.round(sb.getBoundingClientRect().width); save();
    applySbWidth();
  };
  h.addEventListener('pointerup', done);
  h.addEventListener('pointercancel', done);
  h.addEventListener('dblclick', () => {
    setSidebarOpen(false);
  });
  window.addEventListener('resize', () => { applySbWidth(); centerIfFits(); }); /* re-clamp drawer on rotate/resize */
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
  bar.innerHTML = '<button class="linkbtn" id="j-toggle">What changed?</button>'
    + '<button class="linkbtn" id="j-revert">Revert (' + n + ')</button>'
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
// Pending dump queue (Dave 2026-10-12): when the GitHub write fails (no token,
// bad token, offline), dumps land in localStorage instead of vanishing. They show
// in the feed with a "pending sync" badge and flush to the repo on the next
// successful write or page load with a valid token.
function getPendingDumps(){
  try { return JSON.parse(localStorage.getItem('pendingDumps') || '[]'); }
  catch(e){ return []; }
}
function savePendingDumps(q){
  try { localStorage.setItem('pendingDumps', JSON.stringify(q)); } catch(e){}
}
function queuePendingDump(id, stamp, text){
  const q = getPendingDumps();
  q.push({buddyId: id, stamp: stamp, body: text, queuedAt: Date.now()});
  savePendingDumps(q);
}
async function flushPendingDumps(){
  const q = getPendingDumps();
  if (!q.length || !ghToken()) return;
  const remaining = [];
  for (const p of q){
    const b = byId[p.buddyId];
    if (!b || !b.repo){ remaining.push(p); continue; }
    try {
      const entry = '## ' + p.stamp + String.fromCharCode(10,10) + p.body + String.fromCharCode(10,10);
      const cur = await ghGetFile(b.repo, 'docs/ingest.md') || '# Ingest log \u2014 ' + b.name + String.fromCharCode(10,10);
      await ghPutFile(b.repo, 'docs/ingest.md', b64encode(cur + entry), 'Ingest dump for ' + p.buddyId);
    } catch(err){ remaining.push(p); }
  }
  savePendingDumps(remaining);
  if (remaining.length < q.length) {
    // Some flushed — refresh the feed if we're looking at a buddy
    const m = (S.sel || '').match(/^buddy:(.+)/);
    if (m) renderIngestFeed(m[1]);
  }
}
async function dumpIngest(id, keepText){
  const ta = document.getElementById('bp-ingest'), st = document.getElementById('ingest-status');
  const text = ta.value.trim();
  if (!text) return;
  const b = byId[id];
  const stamp = new Date().toLocaleString();
  const entry = '## ' + stamp + String.fromCharCode(10,10) + text + String.fromCharCode(10,10);
  const fallBackToQueue = (why) => {
    queuePendingDump(id, stamp, text);
    if (!keepText) ta.value = '';
    if (st) st.innerHTML = 'Saved on this device — will sync to GitHub when a token is available. <a href="https://github.com/settings/tokens" target="_blank" rel="noopener">Get a token</a>';
    prependDumpEntry(id, {stamp: stamp, body: text, pending: true});
  };
  if (!ghToken() || !b.repo) { fallBackToQueue('no-token'); return; }
  if (st) st.textContent = 'Dumping\u2026';
  try {
    const cur = await ghGetFile(b.repo, 'docs/ingest.md') || '# Ingest log \u2014 ' + b.name + String.fromCharCode(10,10);
    await ghPutFile(b.repo, 'docs/ingest.md', b64encode(cur + entry), 'Ingest dump for ' + id);
    if (!keepText) ta.value = '';
    if (st) st.textContent = 'Dumped to ' + b.repo + '/docs/ingest.md';
    // Flush any queued dumps now that we know the token works
    flushPendingDumps();
    // Optimistically show the new dump — GitHub API may return stale data right after push
    prependDumpEntry(id, {stamp: stamp, body: text});
  } catch (err) { fallBackToQueue(err.message || err); }
}
function prependDumpEntry(id, e){
  const feed = document.getElementById('ingest-feed'); if (!feed) return;
  // If feed is empty ("No dumps yet"), build the full structure with the new entry
  if (!feed.querySelector('.dumps')) {
    if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
    S.dumpsCollapsed[id] = false;
    feed.innerHTML = '<div class="dumps">'
      + '<div class="dumps-head" id="dumps-toggle"><span class="darrow">\u203a</span><h4>Dumps (1)</h4></div>'
      + '<div class="dumps-body"><div style="height:8px"></div>'
      + '<div class="attn"><div class="dump-actions"><button class="dump-act" data-dump-edit="0" title="Edit this dump">' + ICON_EDIT + '</button><button class="dump-act" data-dump-del="0" title="Delete this dump">' + ICON_TRASH + '</button></div><div class="attn-body"><div class="attn-text">' + linkify(escHtml(e.body.slice(0, 300))) + (e.body.length > 300 ? '\u2026' : '') + (e.pending ? '<span class="dump-pending-badge">pending sync</span>' : '') + '</div><div class="attn-date">' + escHtml(e.stamp) + '</div></div></div>'
      + '</div></div>';
    feed._entries = [e];
    // Wire up the toggle
    var dt = document.getElementById('dumps-toggle');
    if (dt) dt.addEventListener('click', function(){
      var d = feed.querySelector('.dumps');
      d.classList.toggle('collapsed');
      if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
      S.dumpsCollapsed[id] = d.classList.contains('collapsed');
      save();
    });
    // Wire up delete/edit for the new entry
    wireDumpButtons(feed, id);
    save();
    return;
  }
  const body = feed.querySelector('.dumps-body');
  if (!body) return;
  const div = document.createElement('div');
  div.className = 'attn';
  div.innerHTML = '<div class="dump-actions"><button class="dump-act" data-dump-edit="0" title="Edit this dump">' + ICON_EDIT + '</button><button class="dump-act" data-dump-del="0" title="Delete this dump">' + ICON_TRASH + '</button></div><div class="attn-body"><div class="attn-text">' + linkify(escHtml(e.body.slice(0, 300))) + (e.body.length > 300 ? '\u2026' : '') + '' + (e.pending ? '<span class="dump-pending-badge">pending sync</span>' : '') + '</div><div class="attn-date">' + escHtml(e.stamp) + '</div></div>';
  body.insertBefore(div, body.firstChild);
  // Update count and entries cache
  const head = feed.querySelector('.dumps-head h4');
  const entries = feed._entries || [];
  entries.unshift(e);
  feed._entries = entries;
  if (head) head.textContent = 'Dumps (' + entries.length + ')';
  // Re-index all edit/delete buttons (the unshift moved every entry down one)
  // and wire the new buttons — without this, edit taps on fresh dumps do nothing
  // and taps on older dumps hit the wrong entry.
  body.querySelectorAll('.attn').forEach(function(tile, i){
    const eb = tile.querySelector('[data-dump-edit]'); if (eb) eb.setAttribute('data-dump-edit', i);
    const db = tile.querySelector('[data-dump-del]'); if (db) db.setAttribute('data-dump-del', i);
  });
  wireDumpButtons(feed, id);
  // Expand if collapsed so the new dump is visible
  const dumps = feed.querySelector('.dumps');
  if (dumps && dumps.classList.contains('collapsed')) {
    dumps.classList.remove('collapsed');
    if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
    S.dumpsCollapsed[id] = false; save();
  }
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
  let entries = [];
  if (ghToken() && b.repo) {
    const md = await ghGetFile(b.repo, 'docs/ingest.md');
    if (md) entries = parseIngest(md);
  } else {
    try { entries = (JSON.parse(localStorage.getItem('ingest:' + id) || '[]')).map(e => ({stamp: new Date(e.t).toLocaleString(), body: e.text})).reverse(); } catch (e) {}
  }
  // Merge pending (not-yet-synced) dumps at the top, newest first
  const pending = getPendingDumps().filter(p => p.buddyId === id).reverse();
  pending.forEach(p => entries.unshift({stamp: p.stamp, body: p.body, pending: true}));
  if (!entries.length) { feed.innerHTML = '<p class="fineprint">No dumps yet.</p>'; return; }
  if (!S.dumpsCollapsed || typeof S.dumpsCollapsed !== 'object') S.dumpsCollapsed = {};
  const dCollapsed = S.dumpsCollapsed[id] !== false;
  feed.innerHTML = '<div class="dumps' + (dCollapsed ? ' collapsed' : '') + '">'
    + '<div class="dumps-head" id="dumps-toggle"><span class="darrow">\u203a</span><h4>Dumps (' + entries.length + ')</h4></div>'
    + '<div class="dumps-body"><div style="height:8px"></div>'
    + entries.map(function(e, i){ return '<div class="attn"><div class="dump-actions"><button class="dump-act" data-dump-edit="' + i + '" title="Edit this dump">' + ICON_EDIT + '</button><button class="dump-act" data-dump-del="' + i + '" title="Delete this dump">' + ICON_TRASH + '</button></div><div class="attn-body"><div class="attn-text">' + linkify(escHtml(e.body.slice(0, 300))) + (e.body.length > 300 ? '\u2026' : '') + (e.pending ? '<span class="dump-pending-badge">pending sync</span>' : '') + '</div><div class="attn-date">' + escHtml(e.stamp) + '</div></div></div>'; }).join('')
    + '</div></div>';
  feed._entries = entries;
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
function wireDumpButtons(feed, id){
  feed.querySelectorAll('[data-dump-del]').forEach(function(btn){
    // Avoid double-wiring
    if (btn.dataset.wired) return; btn.dataset.wired = '1';
    btn.addEventListener('click', function(ev){
      ev.stopPropagation();
      deleteDumpWithUndo(id, parseInt(btn.getAttribute('data-dump-del'), 10), btn);
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

let pendingDumpDelete = null; // single pending delete: {id, op, timer}
function undoToast(msg, onUndo){
  document.querySelectorAll('.toast').forEach(function(t){ t.remove(); });
  const t = document.createElement('div');
  t.className = 'toast undo-toast'; t.id = 'undo-toast';
  const span = document.createElement('span'); span.textContent = msg;
  const btn = document.createElement('button'); btn.className = 'undo-btn'; btn.textContent = 'Undo';
  btn.addEventListener('click', function(ev){ ev.stopPropagation(); hideUndoToast(); onUndo(); });
  t.appendChild(span); t.appendChild(btn);
  document.body.appendChild(t);
}
function hideUndoToast(){
  const t = document.getElementById('undo-toast');
  if (t && t.parentNode) t.parentNode.removeChild(t);
}
// Compute the post-delete stored state WITHOUT writing it. The destructive
// write waits out the undo window (Jonny: forgiveness, not friction).
async function computeDumpDelete(id, idx){
  const b = byId[id];
  if (ghToken() && b.repo) {
    const md = await ghGetFile(b.repo, 'docs/ingest.md');
    if (!md) throw new Error('No ingest file.');
    const parts = md.split(/^## /m);
    const head = parts[0];
    const secs = parts.slice(1);
    const target = secs.length - 1 - idx;
    if (target < 0 || target >= secs.length) throw new Error('Dump not found.');
    secs.splice(target, 1);
    return {kind:'gh', repo:b.repo, path:'docs/ingest.md',
      content: b64encode(head + secs.map(function(x){ return '## ' + x; }).join('')),
      msg:'Delete ingest dump for ' + id};
  }
  const key = 'ingest:' + id;
  let arr = [];
  try { arr = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
  const target = arr.length - 1 - idx;
  if (target < 0 || target >= arr.length) throw new Error('Dump not found.');
  arr.splice(target, 1);
  return {kind:'ls', key:key, content: JSON.stringify(arr)};
}
async function commitDumpDelete(pd){
  if (!pd) return;
  if (pendingDumpDelete === pd) { clearTimeout(pd.timer); pendingDumpDelete = null; }
  hideUndoToast();
  try {
    if (pd.op.kind === 'gh') await ghPutFile(pd.op.repo, pd.op.path, pd.op.content, pd.op.msg);
    else localStorage.setItem(pd.op.key, pd.op.content);
  } catch (err) { toast('Delete failed: ' + (err.message || err)); }
  renderIngestFeed(pd.id);
}
// Poof the dump list away when the last dump is deleted (Dave 2026-10-12).
// The section minimizes to just its add controls (the textarea) — the list
// poofs, but the ability to add dumps never disappears. Inheritable pattern:
// any section's item list can poof while its input controls stay.
function poofDumpList(id){
  const feed = document.getElementById('ingest-feed');
  if (!feed) return;
  const dumps = feed.querySelector('.dumps');
  if (!dumps) return;
  dumps.style.maxHeight = dumps.offsetHeight + 'px';
  dumps.style.overflow = 'hidden';
  dumps.style.transition = 'opacity .3s ease, transform .3s ease, max-height .45s ease .1s, margin .45s ease .1s';
  requestAnimationFrame(() => {
    dumps.style.opacity = '0';
    dumps.style.transform = 'scale(.97)';
    setTimeout(() => {
      dumps.style.maxHeight = '0';
      dumps.style.margin = '0';
      setTimeout(() => {
        if (dumps.parentNode) dumps.parentNode.removeChild(dumps);
        feed._entries = [];
      }, 500);
    }, 300);
  });
}
async function deleteDumpWithUndo(id, idx, btn){
  const feed = document.getElementById('ingest-feed');
  // One pending delete at a time: commit any earlier one first, then
  // re-resolve this entry's index in the freshly rendered feed.
  if (pendingDumpDelete) {
    const prevEntry = (feed && feed._entries) ? feed._entries[idx] : null;
    await commitDumpDelete(pendingDumpDelete);
    if (prevEntry) {
      const fresh = (document.getElementById('ingest-feed') || {})._entries || [];
      idx = fresh.findIndex(function(e){ return e.stamp === prevEntry.stamp && e.body === prevEntry.body; });
      if (idx < 0) { toast('Dump already gone.'); return; }
    }
  }
  let op;
  try { op = await computeDumpDelete(id, idx); }
  catch (err) { toast('Delete failed: ' + (err.message || err)); return; }
  // Collapse the card out with motion. Nothing is written until the undo window closes.
  const card = btn ? btn.closest('.attn') : null;
  if (card) {
    card.style.maxHeight = card.scrollHeight + 'px';
    void card.offsetHeight;
    card.classList.add('dump-removing');
    setTimeout(function(){
      if (card.parentNode) card.parentNode.removeChild(card);
      // Update count and entries cache immediately (Dave 2026-10-12)
      if (feed && feed._entries) {
        feed._entries.splice(idx, 1);
        const head = feed.querySelector('.dumps-head h4');
        if (head) head.textContent = 'Dumps (' + feed._entries.length + ')';
        // Last dump gone: poof the list, keep the add controls (minimized section)
        if (feed._entries.length === 0) poofDumpList(id);
      }
    }, 340);
  }
  const pd = {id:id, op:op, timer:null};
  pd.timer = setTimeout(function(){ commitDumpDelete(pd); }, 6000);
  pendingDumpDelete = pd;
  undoToast('Dump deleted.', function(){
    if (pendingDumpDelete === pd) { clearTimeout(pd.timer); pendingDumpDelete = null; }
    renderIngestFeed(id);
    toast('Dump restored.');
  });
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
    + '<div style="display:flex;align-items:center;gap:10px;margin-top:6px"><div class="fineprint" data-dump-status style="flex:1;min-height:16px"></div><button class="dump-act" data-dump-done style="font-size:13px;font-weight:600;padding:6px 14px;border:1px solid var(--border);border-radius:20px;background:var(--bg)">Done</button></div>';
  const ta = textDiv.querySelector('textarea');
  const st = textDiv.querySelector('[data-dump-status]');
  ta.focus();
  ta.selectionStart = ta.selectionEnd = ta.value.length;
  textDiv.querySelector('[data-dump-done]').addEventListener('click', function(ev){
    ev.stopPropagation();
    clearTimeout(t);
    // Flush any pending autosave before leaving edit mode
    const v = ta.value.trim();
    const done = function(){ renderIngestFeed(id); };
    if (v && v !== e.body) { saveDumpBody(id, idx, v).then(done, done); }
    else done();
  });
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
/* ---------- Add child / sibling buddy from the info panel ---------- */
const ADD_ICONS = ['🤖','👤','👥','🏠','📍','🚗','🐾','💼','🎯','📚','🎨','🎵','⚽','🌲','☕','💡','🔧','📷','✈️','🎬','🏥','💰','🛒','📱'];
const ADD_KINDS = [['assistant','Assistant'],['family','Person'],['place','Place'],['project','Project'],['standalone','Other']];
function slugifyBuddy(name){
  return name.toLowerCase().trim().replace(/['']/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,40) || 'buddy';
}
function openAddBuddyDialog(mode, forId){
  const ref = byId[forId]; if (!ref) return;
  const parentId = mode === 'child' ? forId : mode === 'parent' ? effParent(ref) : effParent(ref);
  const parentName = parentId && byId[parentId] ? dispName(byId[parentId]) : 'top level';
  const title = mode === 'child' ? 'Add a direct report' : mode === 'parent' ? 'Add a parent' : 'Add a peer';
  const sub = mode === 'child'
    ? 'New buddy under <b>' + escHtml(dispName(ref)) + '</b> — a direct report, subordinate, device, or activity.'
    : mode === 'parent'
    ? 'New buddy above <b>' + escHtml(dispName(ref)) + '</b> — a manager or parent. ' + escHtml(dispName(ref)) + ' becomes its direct report' + (parentId ? ' (under ' + escHtml(parentName) + ')' : ' at top level') + '.'
    : 'New buddy alongside <b>' + escHtml(dispName(ref)) + '</b> (under ' + escHtml(parentName) + ')';
  closeAddBuddyDialog();
  const m = document.createElement('div');
  m.id = 'addbuddy-modal';
  m.innerHTML = '<div class="ab-backdrop"></div><div class="ab-box" role="dialog" aria-label="Add buddy">'
    + '<h2>' + title + '</h2>'
    + '<p class="ab-sub">' + sub + '</p>'
    + '<label>Name</label><input type="text" id="ab-name" placeholder="Buddy name" autocomplete="off">'
    + '<label>Icon</label><div class="ab-icons">' + ADD_ICONS.map((ic,i) => '<button data-ic="'+escHtml(ic)+'" class="'+(i===0?'sel':'')+'">'+escHtml(ic)+'</button>').join('') + '</div>'
    + '<label>Type</label><div class="ab-kinds">' + ADD_KINDS.map((k,i) => '<button data-kind="'+k[0]+'" class="'+(i===0?'sel':'')+'">'+k[1]+'</button>').join('') + '</div>'
    + '<div class="ab-err" id="ab-err"></div>'
    + '<div class="ab-actions"><button class="ab-cancel" id="ab-cancel">Cancel</button><button class="ab-create" id="ab-create" disabled>Create</button></div></div>';
  document.body.appendChild(m);
  const nameInput = m.querySelector('#ab-name');
  const createBtn = m.querySelector('#ab-create');
  const errEl = m.querySelector('#ab-err');
  let icon = ADD_ICONS[0], kind = ADD_KINDS[0][0];
  m.querySelector('.ab-backdrop').addEventListener('click', closeAddBuddyDialog);
  m.querySelector('#ab-cancel').addEventListener('click', closeAddBuddyDialog);
  m.querySelectorAll('.ab-icons button').forEach(b => b.addEventListener('click', () => {
    m.querySelectorAll('.ab-icons button').forEach(x => x.classList.remove('sel'));
    b.classList.add('sel'); icon = b.dataset.ic;
  }));
  m.querySelectorAll('.ab-kinds button').forEach(b => b.addEventListener('click', () => {
    m.querySelectorAll('.ab-kinds button').forEach(x => x.classList.remove('sel'));
    b.classList.add('sel'); kind = b.dataset.kind;
  }));
  nameInput.addEventListener('input', () => { createBtn.disabled = !nameInput.value.trim(); errEl.textContent = ''; });
  nameInput.addEventListener('keydown', e => { if (e.key === 'Enter' && !createBtn.disabled) createBtn.click(); if (e.key === 'Escape') closeAddBuddyDialog(); });
  createBtn.addEventListener('click', () => createBuddyFromDialog(nameInput.value.trim(), icon, kind, parentId, errEl, createBtn, mode, forId));
  setTimeout(() => nameInput.focus(), 50);
}
function closeAddBuddyDialog(){
  const m = document.getElementById('addbuddy-modal');
  if (m) m.remove();
}
/* New-buddy request sheet (FAB) — bottom sheet with name, persona picker, purpose */
const REQUEST_PERSONAS = [
  ['Hawaiian bruddah', '🤙'], ['Japanese zen master', '🧘'], ['Valley girl', '💅'],
  ['Bruno Tonioli', '💃'], ['Hans, German master tech', '🔧'], ['Film noir detective', '🕵️'],
  ['Southern grandmother', '👵'], ['Drill sergeant', '🎖️'], ['Deadpan British butler', '🤵'],
  ['Pirate captain', '🏴‍☠️'], ['French existentialist', '🚬'], ['Auctioneer', '🔨'],
  ['Cowboy ranch hand', '🤠'], ['Rastafarian elder', '🦁'], ['Dr. Evil', '😈'],
  ['Shakespearean actor', '🎭'], ['Mafia consigliere', '🤌'], ['Italian nonna', '🍝'],
  ['Surfer dude', '🏄'], ['Mad scientist', '🧪'], ['BBC documentarian', '🎥'],
  ['Game show host', '🎤'], ['Sommelier', '🍷'], ['Viking warrior', '⚔️'],
];
function openNewBuddyRequest(){
  closeAddBuddyDialog();
  const m = document.createElement('div');
  m.id = 'newbuddy-sheet';
  m.innerHTML = '<div class="nb-backdrop"></div><div class="nb-sheet" role="dialog" aria-label="Request a new buddy">'
    + '<div class="nb-grab"></div>'
    + '<h2>New buddy</h2>'
    + '<div class="nb-body">'
    + '<p class="ab-sub">Tell Astro what you want — they\u2019ll run the full onboarding (repo, mission doc, side chat, homepage).</p>'
    + '<label>Name</label><input type="text" id="nb-name" placeholder="e.g. Car Buddy" autocomplete="off">'
    + '<label>Place in tree</label><div class="nb-place" role="tablist" aria-label="Where in the tree">'
    + '<button type="button" data-place="child" class="sel" role="tab" aria-selected="true">Direct report</button>'
    + '<button type="button" data-place="sibling" role="tab" aria-selected="false">Peer</button>'
    + '<button type="button" data-place="parent" role="tab" aria-selected="false">Parent</button></div>'
    + '<div id="nb-place-pick" style="margin-top:8px"><select id="nb-ref" style="width:100%;box-sizing:border-box;font-size:15px;padding:10px 12px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text)">'
    + '<option value="">— Top level —</option>'
    + BUDDIES.filter(x => x && x.id).sort((a,b) => dispName(a).localeCompare(dispName(b))).map(x => '<option value="' + escHtml(x.id) + '">' + escHtml((x.icon || '') + ' ' + dispName(x)) + '</option>').join('')
    + '</select><p class="fineprint" id="nb-place-hint" style="margin-top:6px">As a child of the selected buddy (or top level).</p></div>'
    + '<label>Persona</label><p class="fineprint" style="margin:-4px 0 8px">Pick the voice that makes you grin.</p>'
    + '<div class="nb-personas">' + REQUEST_PERSONAS.map((p,i) =>
        '<button type="button" data-persona="' + escHtml(p[0]) + '">'
        + '<span class="nb-p-emoji">' + p[1] + '</span><span class="nb-p-name">' + escHtml(p[0]) + '</span></button>').join('') + '</div>'
    + '<label>What should it do?</label><textarea id="nb-purpose" rows="3" placeholder="e.g. Track my car maintenance, remind me about oil changes, and help me plan the restoration."></textarea>'
    + '<div class="ab-err" id="nb-err"></div>'
    + '</div>'
    + '<div class="nb-actions"><button class="ab-cancel" id="nb-cancel">Cancel</button><button class="ab-create" id="nb-create" disabled>Start the setup</button></div></div>';
  document.body.appendChild(m);
  const sheet = m.querySelector('.nb-sheet');
  // Fixed width from Advanced settings
  try {
    const w = (typeof getSetting === 'function') ? getSetting('nbSheetWidth') : 560;
    if (w) sheet.style.maxWidth = w + 'px';
  } catch (e) {}
  const nameInput = m.querySelector('#nb-name');
  const purposeInput = m.querySelector('#nb-purpose');
  const createBtn = m.querySelector('#nb-create');
  const errEl = m.querySelector('#nb-err');
  let persona = null, placeMode = 'child';
  const refSel = m.querySelector('#nb-ref'), placeHint = m.querySelector('#nb-place-hint');
  const updateHint = () => {
    const ref = refSel.value ? byId[refSel.value] : null;
    const rn = ref ? dispName(ref) : 'top level';
    placeHint.textContent = placeMode === 'child'
      ? (ref ? 'As a direct report of ' + rn + '.' : 'At top level (no parent).')
      : placeMode === 'sibling'
      ? (ref ? 'Alongside ' + rn + ' (same parent).' : 'Pick a buddy to sit alongside.')
      : (ref ? 'As the parent of ' + rn + ' — ' + rn + ' becomes its direct report.' : 'Pick a buddy to become a direct report of the new buddy.');
  };
  m.querySelectorAll('.nb-place button').forEach(b => b.addEventListener('click', () => {
    m.querySelectorAll('.nb-place button').forEach(x => { x.classList.remove('sel'); x.setAttribute('aria-selected', 'false'); });
    b.classList.add('sel'); b.setAttribute('aria-selected', 'true');
    placeMode = b.dataset.place; updateHint();
  }));
  refSel.addEventListener('change', updateHint); updateHint();
  const close = () => m.remove();
  m.querySelector('.nb-backdrop').addEventListener('click', close);
  m.querySelector('#nb-cancel').addEventListener('click', close);
  m.querySelectorAll('.nb-personas button').forEach(b => b.addEventListener('click', () => {
    m.querySelectorAll('.nb-personas button').forEach(x => x.classList.remove('sel'));
    b.classList.add('sel'); persona = b.dataset.persona;
    validate();
  }));
  const validate = () => { createBtn.disabled = !(nameInput.value.trim() && persona); errEl.textContent = ''; };
  nameInput.addEventListener('input', validate);
  purposeInput.addEventListener('input', validate);
  createBtn.addEventListener('click', async () => {
    errEl.textContent = '';
    createBtn.disabled = true;
    createBtn.textContent = 'Starting…';
    try {
      if (!ghToken()) throw new Error('Add a GitHub token first (gear menu → GitHub token) so the dashboard can save.');
      const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const req = {
        name: nameInput.value.trim(),
        persona: persona,
        purpose: purposeInput.value.trim(),
        place_mode: placeMode,
        ref_buddy: refSel.value || null,
        requested_at: new Date().toISOString(),
        requested_from: 'dashboard-fab',
      };
      const path = 'docs/inbox/new-buddy-' + stamp + '.json';
      await ghPutFile('buddy-system', path, b64encode(JSON.stringify(req, null, 2)), 'New buddy request: ' + req.name);
      close();
      toast('Request sent — Astro will pick it up shortly.');
    } catch (e) {
      errEl.textContent = e.message || String(e);
      createBtn.disabled = false;
      createBtn.textContent = 'Start the setup';
    }
  });
  requestAnimationFrame(() => m.classList.add('open'));
  setTimeout(() => nameInput.focus(), 300);
  // Drag the grab handle to resize sheet height
  const grab = m.querySelector('.nb-grab');
  grab.style.cursor = 'ns-resize';
  grab.style.touchAction = 'none';
  grab.addEventListener('pointerdown', e => {
    e.preventDefault();
    const startY = e.clientY;
    const startH = sheet.getBoundingClientRect().height;
    const mv = ev => {
      const dh = startY - ev.clientY;
      const nh = Math.min(window.innerHeight * 0.94, Math.max(280, startH + dh));
      sheet.style.height = nh + 'px';
      sheet.style.maxHeight = 'none';
    };
    const up = () => {
      window.removeEventListener('pointermove', mv);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', mv);
    window.addEventListener('pointerup', up);
  });
}
function initNewBuddyFab(){
  const fab = document.getElementById('new-buddy-fab');
  if (!fab || fab.dataset.init) return;
  fab.dataset.init = '1';
  fab.addEventListener('click', e => { e.stopPropagation(); openNewBuddyRequest(); });
}
async function createBuddyFromDialog(name, icon, kind, parentId, errEl, createBtn, mode, forId){
  errEl.textContent = '';
  createBtn.disabled = true;
  createBtn.textContent = 'Creating…';
  try {
    if (!ghToken()) throw new Error('Add a GitHub token first (gear menu → GitHub token) so the dashboard can save.');
    let base = slugifyBuddy(name), nid = base, n = 2;
    while (byId[nid]) { nid = base + '-' + (n++); }
    const today = new Date().toISOString().slice(0,10);
    const entry = {
      id: nid, name: name, icon: icon, kind: kind,
      parent: parentId || null,
      mission: '', tagline: 'New buddy — setup pending',
      status: 'new', statusClass: 'new',
      brief: '', docs: [], repo: '', homepage: '', photos: [],
      setup_pending: true,
      attention: [{id: 'setup-' + nid, date: today, text: 'New buddy added from the dashboard — run the full onboarding (mission doc, repo, side chat, homepage).'}]
    };
    // Fetch latest buddies.json from GitHub, append, write back
    const raw = await ghGetFile('buddy-system', 'buddies.json');
    if (!raw) throw new Error('Could not read buddies.json from GitHub.');
    const data = JSON.parse(raw);
    const arr = data.buddies || data;
    if (arr.some(x => x.id === nid)) throw new Error('A buddy with that id already exists — try a different name.');
    arr.push(entry);
    // Parent mode: reparent the reference buddy under the new parent
    let reparented = null;
    if (mode === 'parent' && forId) {
      reparented = arr.find(x => x.id === forId);
      if (reparented) reparented.parent = nid;
    }
    await ghPutFile('buddy-system', 'buddies.json', b64encode(JSON.stringify(data, null, 1)), 'Add buddy ' + nid + ' (from dashboard info panel)');
    // Optimistic local update
    (BUDDIES).push(entry);
    byId[nid] = entry;
    const p = parentId || '__root';
    (kidsOf[p] = kidsOf[p] || []).push(entry);
    if (mode === 'parent' && forId && byId[forId]) {
      const oldP = effParent(byId[forId]) || '__root';
      byId[forId].parent = nid;
      const sibs = kidsOf[oldP] || [];
      const ix = sibs.indexOf(byId[forId]);
      if (ix >= 0) sibs.splice(ix, 1);
      (kidsOf[nid] = kidsOf[nid] || []).push(byId[forId]);
    }
    closeAddBuddyDialog();
    save(); renderNav(); refreshViews();
    if (S.projectId) renderBuddy(S.projectId);
    toast('Buddy created — Astro will run the full onboarding.');
  } catch (e) {
    errEl.textContent = e.message || String(e);
    createBtn.disabled = false;
    createBtn.textContent = 'Create';
  }
}
// Promote a buddy one level up (Shift+Left). Reparents to grandparent via GitHub.
async function promoteBuddy(id){
  const b = byId[id]; if (!b) return;
  const par = effParent(b);
  if (!par) { toast('Already top-level — nothing to promote to.'); return; }
  const grand = effParent(byId[par]);
  if (!ghToken()) { toast('Add a GitHub token first (gear menu) so the dashboard can save.'); return; }
  try {
    const raw = await ghGetFile('buddy-system', 'buddies.json');
    if (!raw) throw new Error('Could not read buddies.json');
    const data = JSON.parse(raw);
    const arr = data.buddies || data;
    const rec = arr.find(x => x.id === id);
    if (!rec) throw new Error('Buddy not found on GitHub');
    rec.parent = grand || null;
    await ghPutFile('buddy-system', 'buddies.json', b64encode(JSON.stringify(data, null, 1)), 'Promote ' + id + ' one level (Shift+Left)');
    // Optimistic local update
    b.parent = grand || null;
    const oldKids = kidsOf[par] || [];
    const ix = oldKids.indexOf(b);
    if (ix >= 0) oldKids.splice(ix, 1);
    const gp = grand || '__root';
    (kidsOf[gp] = kidsOf[gp] || []).push(b);
    save(); renderNav(); refreshViews();
    if (S.projectId) renderBuddy(S.projectId);
    toast('Promoted — now under ' + (grand && byId[grand] ? dispName(byId[grand]) : 'top level') + '.');
  } catch (err) {
    toast('Promote failed: ' + (err.message || err));
  }
}
// Delegated clicks for the + Child / + Sibling buttons in the info panel
document.addEventListener('click', e => {
  const btn = e.target.closest('[data-addbuddy]');
  if (!btn) return;
  e.preventDefault(); e.stopPropagation();
  openAddBuddyDialog(btn.dataset.addbuddy, btn.dataset.for);
});
// Change-parent picker: select a new parent for a buddy (excludes self + descendants to prevent cycles)
document.addEventListener('click', e => {
  if (e.target.closest('#sib-showall')) {
    document.getElementById('sib-rest').hidden = false;
    e.target.closest('#sib-showall').remove();
    return;
  }
  const btn = e.target.closest('[data-changeparent]');
  if (!btn) return;
  e.preventDefault(); e.stopPropagation();
  openChangeParentDialog(btn.dataset.changeparent);
});
function descendantsOf(bid){
  const out = new Set(); const stack = [bid];
  while (stack.length){ const cur = stack.pop();
    (kidsOf[cur] || []).forEach(k => { if (k && k.id && !out.has(k.id)){ out.add(k.id); stack.push(k.id); } });
  }
  return out;
}
function openChangeParentDialog(bid){
  const b = byId[bid]; if (!b) return;
  const bad = descendantsOf(bid); bad.add(bid);
  const opts = BUDDIES.filter(x => x && x.id && !bad.has(x.id))
    .sort((a,c) => dispName(a).localeCompare(dispName(c)));
  const cur = effParent(b);
  const m = document.createElement('div'); m.id = 'addbuddy-modal';
  const optHtml = x => '<option value="' + escHtml(x.id) + '"' + (x.id === cur ? ' selected' : '') + '>' + escHtml((x.icon || '') + ' ' + dispName(x)) + '</option>';
  const hiddenCount = BUDDIES.length - opts.length;
  m.innerHTML = '<div class="ab-backdrop"></div><div class="ab-box" role="dialog" aria-modal="true" aria-label="Change parent">'
    + '<h2>Change parent</h2><p class="ab-sub">Pick a new parent for ' + escHtml(dispName(b)) + '.</p>'
    + '<label for="cp-filter">Filter</label>'
    + '<input type="text" id="cp-filter" placeholder="Type to filter…" autocomplete="off" style="margin-bottom:10px">'
    + '<label for="cp-select">Parent</label>'
    + '<select id="cp-select" size="8" style="width:100%;box-sizing:border-box;font-size:15px;padding:10px 12px;border-radius:10px;border:1px solid var(--border);background:var(--bg);color:var(--text)">'
    + '<option value="">No parent (top level)</option>'
    + '<option value="" disabled>──────────</option>'
    + opts.map(optHtml).join('')
    + '</select>'
    + (hiddenCount > 0 ? '<p class="fineprint" style="margin-top:6px">' + hiddenCount + ' hidden — a buddy can\u2019t be its own ancestor.</p>' : '')
    + '<div style="display:flex;gap:10px;justify-content:flex-end;margin-top:18px">'
    + '<button class="linkbtn" id="cp-cancel" type="button">Cancel</button>'
    + '<button class="linkbtn" id="cp-save" type="button" style="font-weight:600">Save</button>'
    + '</div></div>';
  document.body.appendChild(m);
  const close = () => m.remove();
  const sel = m.querySelector('#cp-select'), filt = m.querySelector('#cp-filter');
  filt.addEventListener('input', () => {
    const q = filt.value.trim().toLowerCase();
    sel.querySelectorAll('option').forEach(o => {
      if (o.disabled || !o.value) return; // keep "No parent" and separators visible
      o.hidden = q && !o.textContent.toLowerCase().includes(q);
    });
    // Don't steal selection on every keystroke — only auto-select on Enter
  });
  filt.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      const q = filt.value.trim().toLowerCase();
      if (q) {
        const matches = [...sel.options].filter(o => !o.hidden && !o.disabled && o.value && o.textContent.toLowerCase().includes(q));
        if (matches.length === 1) sel.value = matches[0].value;
      }
      m.querySelector('#cp-save').click();
    }
  });
  const doSave = () => {
    const v = sel.value || null;
    const beforeParent = effParent(b);
    applyParentOverride(bid, v); save(); buildKids(); renderNav(); refreshViews();
    if (S.sel === 'buddy:' + bid) renderBuddy(bid);
    close();
    offerMoveUndo(bid, beforeParent, 'Parent updated.');
  };
  m.querySelector('.ab-backdrop').addEventListener('click', close);
  m.querySelector('#cp-cancel').addEventListener('click', close);
  m.querySelector('#cp-save').addEventListener('click', doSave);
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
  if (ph3) {
    // Update the label without disturbing the collapse arrow / drag grip
    let label = ph3.querySelector('.ph-label');
    if (!label) {
      label = document.createElement('span');
      label.className = 'ph-label';
      Array.from(ph3.childNodes).forEach(n => { if (n.nodeType === 3) n.remove(); });
      const arrow = ph3.querySelector('.secarrow');
      if (arrow && arrow.after) arrow.after(label); else ph3.prepend(label);
    }
    label.textContent = 'Photos (' + all.length + ')';
  }
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
  const sc = (node.closest && node.closest('.treescroll')) || tz;
  const nr = node.getBoundingClientRect(), tr = sc.getBoundingClientRect();
  sc.scrollLeft += (nr.left + nr.width / 2) - (tr.left + tr.width / 2);
  sc.scrollTop += (nr.top + nr.height / 2) - (tr.top + tr.height / 2);
}
function firstSearchMatch(){
  const q = (document.getElementById('buddy-search').value || '').toLowerCase().trim();
  const words = q.split(/\s+/).filter(Boolean);
  if (!words.length) return null;
  for (const b of BUDDIES) {
    const hay = (dispName(b) + ' ' + (b.name || '') + ' ' + (b.tagline || '') + ' ' + effAka(b).join(' ')).toLowerCase();
    if (words.every(w => hay.includes(w))) return b.id;
  }
  return null;
}
const AVATAR_CATS = [
 {name:'Smileys', emojis:'😀 😃 😄 😁 😆 😅 😂 🤣 😊 😇 🙂 🙃 😉 😌 😍 🥰 😘 😎 🤩 🥳 😏 🤔 😴 🤯 😱'.split(' ')},
 {name:'Gestures', emojis:'👋 🤚 🖐 ✋ 🖖 👌 🤌 ✌️ 🤞 🤟 🤘 🤙 👈 👉 👆 👇 ☝️ 👍 👎 ✊ 👊 🤛 🤜 👏 🙌 💪 🤲 🤝 🙏'.split(' ')},
 {name:'Animals', emojis:'🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐨 🐯 🦁 🐮 🐷 🐸 🐵 🐔 🐧 🐦 🦄 🐝 🦋 🐢 🐙 🦑 🐠 🐟 🐬 🦈'.split(' ')},
 {name:'Food', emojis:'🍎 🍐 🍊 🍋 🍌 🍉 🍇 🍓 🫐 🍒 🍑 🍍 🥑 🍆 🌶 🥕 🌽 🍄 🥜 🍞 🥐 🧀 🥚 🍳 🥞 🍕 🍔 🍟 🌮 🍣 🍩 🍪 🎂 🍫 ☕ 🍺 🍷'.split(' ')},
 {name:'Activities', emojis:'⚽ 🏀 🏈 ⚾ 🎾 🏐 🎱 🏓 🏸 🥊 🎽 🛹 🎿 ⛷ 🏂 🏋️ 🤸 🏄 🏊 🚴 🧗 🎣 ⛳ 🎯 🎮 🎲 🧩 🎭 🎨 🎬 🎤 🎧 🎷 🎺 🎸 🎹 🥁'.split(' ')},
 {name:'Travel', emojis:'🚗 🚕 🚙 🚌 🏎 🚓 🚑 🚒 🚚 🚜 🛴 🚲 🛵 🏍 ✈️ 🚀 🛸 🚁 ⛵ 🚤 🛳 ⚓ 🗺 🗽 🗼 🏰 🎡 🎢 ⛲ 🏖 🏝 ⛰ 🏔 🗻 🏕 ⛺ 🌋'.split(' ')},
 {name:'Objects', emojis:'💡 🔦 🕯 🧯 💸 💵 💰 💳 💎 ⚖️ 🧰 🔧 🔨 ⚙️ 🧲 💣 🔪 🛡 🔮 📿 🧿 🔭 🔬 💊 🩺 🏷 🔖 🚩 📚 📖 ✏️ 📝 📎 🖇 📐 ✂️'.split(' ')},
 {name:'Symbols', emojis:'❤️ 🧡 💛 💚 💙 💜 🖤 🤍 💔 💕 💖 ☮️ ✝️ ☪️ 🕉 ☸️ ✡️ ☯️ 🛐 ⚛️ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒ ♓ 🆔 ✅ ❌ ❓ ❗ ➕ ➖ 💯 🔱'.split(' ')}
];
function openAvatarPicker(bid, anchorEl){
  let pk = document.getElementById('avatar-picker');
  if(!pk){
    pk = document.createElement('div'); pk.id = 'avatar-picker';
    pk.innerHTML = '<h4>Choose avatar</h4><div id="avatar-grid"></div>'
      + '<input id="avatar-custom" placeholder="Or paste any emoji" maxlength="8">'
      + '<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap">'
      + '<button class="linkbtn" id="avatar-upload">Upload image</button>'
      + '<button class="linkbtn" id="avatar-remove">Remove image</button></div>'
      + '<p class="fineprint" style="margin:8px 0 0">Uploaded images live in the dashboard repo (avatars/) and appear on the card, homepage, and favicon.</p>';
    document.body.appendChild(pk);
    document.getElementById('avatar-upload').addEventListener('click', () => {
      const cur = document.getElementById('avatar-picker').dataset.bid;
      uploadBuddyImage(cur);
    });
    document.getElementById('avatar-remove').addEventListener('click', async () => {
      const cur = document.getElementById('avatar-picker').dataset.bid;
      if(!ghToken()){ openTokenPopover(); toast('Add a GitHub token first.'); return; }
      try{ await ghDeleteFile('buddy-system', 'avatars/' + cur + '.jpg', 'Remove avatar for ' + cur); toast('Avatar image removed.'); }
      catch(e){ toast('No custom image to remove.'); }
      closeAvatarPicker(); if(cur) renderBuddy(cur);
    });
  }
  pk.dataset.bid = bid;
  const grid = document.getElementById('avatar-grid');
  grid.innerHTML = AVATAR_CATS.map(cat =>
    '<div class="av-cat">' + cat.name + '</div><div class="av-grid">' +
    cat.emojis.map(e => '<button data-emoji="' + e + '">' + e + '</button>').join('') + '</div>'
  ).join('');
  grid.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => { setBuddyIcon(bid, btn.dataset.emoji); closeAvatarPicker(); });
  });
  const inp = document.getElementById('avatar-custom');
  inp.value = '';
  inp.onchange = () => { const v = inp.value.trim(); if(v){ setBuddyIcon(bid, v); closeAvatarPicker(); } };
  const r = anchorEl.getBoundingClientRect();
  pk.style.left = Math.min(window.innerWidth - 340, r.left) + 'px';
  pk.style.top = (r.bottom + 8) + 'px';
  // Detach any stale close listener from a previous open (it would instantly
  // close the picker on this tap: the tap target is inside #bp-icon but is
  // the inner span/img, not the anchor element itself).
  if (pk._closeListener) { document.removeEventListener('click', pk._closeListener); pk._closeListener = null; }
  pk.classList.add('show');
  const close = e => { if(!pk.contains(e.target) && !anchorEl.contains(e.target)){ closeAvatarPicker(); } };
  pk._closeListener = close;
  setTimeout(() => document.addEventListener('click', close), 10);
}
function closeAvatarPicker(){
  const pk = document.getElementById('avatar-picker');
  if (!pk) return;
  pk.classList.remove('show');
  if (pk._closeListener) { document.removeEventListener('click', pk._closeListener); pk._closeListener = null; }
}
function fileToDataUrl(f){ return new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(r.result); r.onerror = rej; r.readAsDataURL(f); }); }
function downscaleToJpeg(dataUrl, maxSize){
  return new Promise((res, rej) => {
    const img = new Image();
    img.onload = () => {
      const s = Math.min(1, maxSize / Math.max(img.width, img.height));
      const c = document.createElement('canvas');
      c.width = Math.max(1, Math.round(img.width * s)); c.height = Math.max(1, Math.round(img.height * s));
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      res(c.toDataURL('image/jpeg', 0.85));
    };
    img.onerror = rej; img.src = dataUrl;
  });
}
async function uploadBuddyImage(bid){
  if(!bid) return;
  if(!ghToken()){ openTokenPopover(); toast('Add a GitHub token first.'); return; }
  const inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'image/*';
  inp.onchange = async () => {
    const f = inp.files && inp.files[0]; if(!f) return;
    const pk = document.getElementById('avatar-picker'); if(pk) pk.classList.remove('show');
    toast('Uploading avatar…');
    try{
      const jpg = await downscaleToJpeg(await fileToDataUrl(f), 512);
      await ghPutFile('buddy-system', 'avatars/' + bid + '.jpg', jpg.split(',')[1], 'Avatar image for ' + bid);
      toast('Avatar image saved.');
      renderBuddy(bid);
    }catch(err){ toast('Upload failed: ' + (err && err.message || err)); }
  };
  inp.click();
}
function setBuddyIcon(bid, emoji){
  const b = byId[bid]; if (!b) return;
  b.icon = emoji;
  // Persist to buddies.json via journal? For now, device-local + mark dirty
  if (!S.iconOverrides) S.iconOverrides = {};
  S.iconOverrides[bid] = emoji; save();
  const eel = document.querySelector('#bp-icon .bp-avaemoji'); if (eel) eel.textContent = emoji;
  else { const el = document.getElementById('bp-icon'); if (el) el.textContent = emoji; }
  try{ setBuddyFavicon(emoji, buddyImageUrl(b)); }catch(e){}
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
/* Collapsible sidebar sections: Views and Buddies headers toggle like Business Plans */
function initNavSecToggles(){
  [['views-toggle', 'views-sec', 'viewsCollapsed'],
   ['buddies-toggle', 'buddies-sec', 'buddiesCollapsed']].forEach(([tid, sid, key]) => {
    const t = document.getElementById(tid);
    const sec = document.getElementById(sid);
    if (!t || !sec || t.dataset.init) return;
    t.dataset.init = '1';
    if (S[key]) sec.classList.add('collapsed');
    t.addEventListener('click', () => {
      sec.classList.toggle('collapsed');
      S[key] = sec.classList.contains('collapsed');
      save();
    });
  });
}
/* Drag-to-reorder for the sidebar sections (Buddies / Business Plans / Views).
   Drag by the section header; order persists on this device (S.navSecOrder). */
function applyNavSecOrder(){
  const order = S.navSecOrder;
  if (!order || !order.length) return;
  const sb = document.getElementById('sidebar');
  if (!sb) return;
  order.forEach(id => { const s = document.getElementById(id); if (s) sb.appendChild(s); });
}
function saveNavSecOrder(){
  S.navSecOrder = [...document.querySelectorAll('#sidebar .nav-sec')].map(s => s.id);
  save();
}
function initNavSecDnD(){
  const sb = document.getElementById('sidebar');
  if (!sb || sb.dataset.secdnd) return;
  sb.dataset.secdnd = '1';
  let dragId = null;
  const clearHints = () => sb.querySelectorAll('.nav-sec').forEach(s => s.classList.remove('sec-drop-before', 'sec-drop-after'));
  sb.querySelectorAll('.nav-sec > h3').forEach(h => {
    h.draggable = true;
    h.addEventListener('dragstart', e => {
      dragId = h.parentElement.id;
      e.dataTransfer.effectAllowed = 'move';
      try { e.dataTransfer.setData('text/plain', dragId); } catch (err) {}
      h.parentElement.classList.add('sec-dragging');
    });
    h.addEventListener('dragend', () => {
      const p = h.parentElement;
      if (p) p.classList.remove('sec-dragging');
      clearHints();
      dragId = null;
    });
  });
  sb.querySelectorAll('.nav-sec').forEach(sec => {
    sec.addEventListener('dragover', e => {
      if (!dragId || sec.id === dragId) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      const r = sec.getBoundingClientRect();
      const before = (e.clientY - r.top) < r.height / 2;
      sec.classList.toggle('sec-drop-before', before);
      sec.classList.toggle('sec-drop-after', !before);
    });
    sec.addEventListener('dragleave', () => sec.classList.remove('sec-drop-before', 'sec-drop-after'));
    sec.addEventListener('drop', e => {
      if (!dragId || sec.id === dragId) return;
      e.preventDefault();
      const r = sec.getBoundingClientRect();
      const before = (e.clientY - r.top) < r.height / 2;
      const dragged = document.getElementById(dragId);
      if (dragged) {
        sec.parentElement.insertBefore(dragged, before ? sec : sec.nextSibling);
        saveNavSecOrder();
        toast('Sidebar order saved.');
      }
      clearHints();
    });
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
    e.stopPropagation(); // keep document click from stripping #sidebar.open
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
function initBpToTop(){
  const vb = document.getElementById('view-buddy');
  const btn = document.getElementById('bp-to-top');
  if (!vb || !btn || btn.dataset.init) return;
  btn.dataset.init = '1';
  const THRESH = 100;
  function panelOpen(){
    return vb.classList.contains('active') && (vb.classList.contains('panel') || vb.classList.contains('sheet'));
  }
  function sync(){
    const useful = vb.scrollTop > THRESH && panelOpen() && !document.body.classList.contains('standalone');
    btn.classList.toggle('show', !!useful);
    // Center horizontally in the panel: panel is fixed to the right edge
    if (useful) btn.style.right = Math.max(8, vb.offsetWidth / 2 - 22) + 'px';
  }
  vb.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  btn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    try { vb.scrollTo({ top: 0, behavior: 'smooth' }); }
    catch (err) { vb.scrollTop = 0; }
  });
  const mo = typeof MutationObserver !== 'undefined'
    ? new MutationObserver(sync) : null;
  if (mo) {
    mo.observe(vb, { attributes: true, attributeFilter: ['class'] });
    mo.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }
  sync();
}
function initNerdSettings(){
  // Secret unlock: tap the build number 5 times within 2.5s (Android dev-options style)
  let taps = [], unlocked = !!(S.nerdUnlocked);
  document.addEventListener('click', function(e){
    const el = e.target.closest ? e.target.closest('.bp-build') : null;
    if (!el) return;
    if (S.nerdUnlocked) { openNerdSettings(); return; }
    const now = Date.now();
    taps = taps.filter(t => now - t < 2500);
    taps.push(now);
    if (taps.length >= 5) {
      taps = [];
      S.nerdUnlocked = true; save();
      toast('🤓 Nerd settings unlocked');
      openNerdSettings();
    } else if (taps.length >= 3) {
      toast((5 - taps.length) + ' more taps for nerd settings…');
    }
  });
}
function openNerdSettings(){
  closeNerdSettings();
  const gear = parseFloat(S.panGearing) || 1;
  const m = document.createElement('div');
  m.id = 'nerd-modal';
  m.innerHTML = '<div class="nd-backdrop"></div><div class="nd-box" role="dialog" aria-label="Nerd settings">'
    + '<h2>🤓 Nerd settings</h2>'
    + '<p class="nd-sub">Secret knobs. You didn\u2019t find this. It found you.</p>'
    + '<div class="nd-row"><label>Tree pan gearing <b id="nd-gear-val">' + gear.toFixed(2) + '\u00d7</b></label>'
    + '<input type="range" id="nd-gear" min="0.25" max="3" step="0.25" value="' + gear + '">'
    + '<p class="fineprint" style="margin:8px 0 0">1\u00d7 = finger tracks content exactly. Higher = faster pan, lower = finer control.</p></div>'
    + '<div class="nd-actions"><button id="nd-reset">Reset</button><button class="nd-close" id="nd-done">Done</button></div></div>';
  document.body.appendChild(m);
  const slider = m.querySelector('#nd-gear');
  const val = m.querySelector('#nd-gear-val');
  slider.addEventListener('input', function(){
    const v = parseFloat(slider.value) || 1;
    val.textContent = v.toFixed(2) + '\u00d7';
    S.panGearing = v; save();
  });
  m.querySelector('#nd-reset').addEventListener('click', function(){
    slider.value = 1; slider.dispatchEvent(new Event('input'));
  });
  m.querySelector('.nd-backdrop').addEventListener('click', closeNerdSettings);
  m.querySelector('#nd-done').addEventListener('click', closeNerdSettings);
}
function closeNerdSettings(){
  const m = document.getElementById('nerd-modal');
  if (m) m.remove();
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
/* Left-edge swipe opens the mobile drawer.
   Rightward swipe that begins within EDGE_PX of the left screen edge.
   Tree pan yields this strip; a short click-swallow window prevents the
   document click handler from immediately stripping #sidebar.open. */
let edgeOpenAt = 0;
function initEdgeSwipeOpen(){
  const EDGE_PX = 24;
  const MIN_DX = 56;
  const DOMINATE = 1.25;
  let track = null;
  function touchById(list, id){
    if (!list) return null;
    for (let i = 0; i < list.length; i++) if (list[i].identifier === id) return list[i];
    return null;
  }
  function onStart(e){
    if (isSidebarOpen()) { track = null; return; }
    if (document.body.classList.contains('standalone')) { track = null; return; }
    const t = e.changedTouches && e.changedTouches[0];
    if (!t || t.clientX > EDGE_PX) { track = null; return; }
    // Don't steal the hamburger / chrome taps in the top-left
    const el = document.elementFromPoint(t.clientX, t.clientY);
    if (el && el.closest && el.closest('#menu-btn,#sb-to-top,#sb-resize')) { track = null; return; }
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
    if (!t || isSidebarOpen()) return;
    if (document.body.classList.contains('standalone')) return;
    const dx = t.clientX - x0, dy = t.clientY - y0;
    if (dx >= MIN_DX && Math.abs(dx) > Math.abs(dy) * DOMINATE) {
      setSidebarOpen(true);
      edgeOpenAt = Date.now();
    }
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
    // Left-edge strip is owned by initEdgeSwipeOpen (open drawer)
    if (t.clientX <= 24) return;
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
      const id = (S.projectId && byId[S.projectId]) ? S.projectId : ROOT_ID;
      openBuddy(id);
    }
  }
  document.addEventListener('touchstart', onStart, { passive: true, capture: true });
  document.addEventListener('touchmove', onMove, { passive: true, capture: true });
  document.addEventListener('touchend', onEnd, { passive: true, capture: true });
  document.addEventListener('touchcancel', () => { track = null; }, { passive: true, capture: true });
}

/* Edge swipes inside same-origin homepage iframes.
   Touch events inside the iframe never reach the parent document, so the
   parent binds this recognizer on the iframe's document (via the frame load
   hook — same pattern as pull-to-refresh). Coordinates are translated to
   screen space with the frame's bounding rect at touchstart.
   - swipe right from the left  24px edge -> open left drawer (mobile)
   - swipe left  from the right 24px edge -> open this buddy's right panel
   Actions run in the parent window, so all state stays in one place. */
function bindIframeEdgeSwipes(iframeDoc, frameEl, buddyId){
  if (!iframeDoc || iframeDoc.__edgeSwipesBound) return;
  iframeDoc.__edgeSwipesBound = true;
  const LEFT_EDGE = 24, RIGHT_EDGE = 24, MIN_DX = 56, DOMINATE = 1.25;
  let track = null;
  function screenX(t){
    try { return frameEl.getBoundingClientRect().left + t.clientX; }
    catch (e) { return t.clientX; }
  }
  function touchById(list, id){
    if (!list) return null;
    for (let i = 0; i < list.length; i++) if (list[i].identifier === id) return list[i];
    return null;
  }
  function detailOpen(){
    const vb = document.getElementById('view-buddy');
    return !!(vb && vb.classList.contains('active') && (vb.classList.contains('panel') || vb.classList.contains('sheet')));
  }
  function onStart(e){
    track = null;
    if (document.body.classList.contains('standalone')) return;
    const t = e.changedTouches && e.changedTouches[0];
    if (!t) return;
    const sx = screenX(t);
    const fromLeft = sx <= LEFT_EDGE, fromRight = sx >= (window.innerWidth - RIGHT_EDGE);
    if (!fromLeft && !fromRight) return;
    const el = iframeDoc.elementFromPoint(t.clientX, t.clientY);
    if (el && el.closest && el.closest('input,textarea,select,[contenteditable="true"],button,a')) return;
    track = { id: t.identifier, x0: sx, y0: t.clientY, mode: fromLeft ? 'drawer' : 'panel' };
  }
  function onMove(e){
    if (!track) return;
    const t = touchById(e.touches, track.id) || touchById(e.changedTouches, track.id);
    if (!t) return;
    const dx = screenX(t) - track.x0, dy = t.clientY - track.y0;
    if (Math.abs(dy) > 28 && Math.abs(dy) > Math.abs(dx)) track = null;
  }
  function onEnd(e){
    if (!track) return;
    const mode = track.mode;
    const t = touchById(e.changedTouches, track.id);
    const x0 = track.x0, y0 = track.y0;
    track = null;
    if (!t || document.body.classList.contains('standalone')) return;
    const dx = screenX(t) - x0, dy = t.clientY - y0;
    if (Math.abs(dx) < MIN_DX || Math.abs(dx) <= Math.abs(dy) * DOMINATE) return;
    if (mode === 'drawer'){
      if (dx > 0 && isDrawerNav() && !isSidebarOpen()){ setSidebarOpen(true); edgeOpenAt = Date.now(); }
      return;
    }
    if (dx < 0 && !detailOpen()) openBuddy(buddyId || ROOT_ID);
  }
  iframeDoc.addEventListener('touchstart', onStart, { passive: true, capture: true });
  iframeDoc.addEventListener('touchmove', onMove, { passive: true, capture: true });
  iframeDoc.addEventListener('touchend', onEnd, { passive: true, capture: true });
  iframeDoc.addEventListener('touchcancel', function(){ track = null; }, { passive: true, capture: true });
}
window.__bindEdgeSwipes = bindIframeEdgeSwipes;

// Checks for a newer deployed version; shows an update banner if the server
// has a newer build than the one currently loaded (helps Safari web apps
// and other containers without a hard-refresh shortcut).
// Returns 'new' | 'current' | 'suppressed' | 'error' so manual triggers
// (e.g. pull-to-refresh) can report the outcome.
/* Renders the newest CHANGELOG.md sections as HTML for the What's-new modal */
function changelogMdToHtml(md, bare){
  const lines = String(md || '').split('\\n');
  let html = '', sections = 0, inList = false, curType = '';
  const typeCounts = {};
  const closeList = () => { if (inList) { html += '</ul>'; inList = false; } };
  const typeSlug = t => t.toLowerCase().replace(/[^a-z]+/g, '');
  for (const raw of lines) {
    const line = raw.replace(/\s+$/, '');
    if (/^## /.test(line)) {
      sections++;
      if (!bare && sections > 3) break;
      closeList();
      html += '<h4>' + escHtml(line.slice(3)) + '</h4>';
    } else if (/^### /.test(line)) {
      closeList();
      curType = line.slice(4).trim();
      html += '<h5 data-cl-type-head="' + escHtml(typeSlug(curType)) + '">' + escHtml(curType) + '</h5>';
    } else if (/^- /.test(line)) {
      if (!inList) { html += '<ul>'; inList = true; }
      const slug = typeSlug(curType || 'other');
      typeCounts[slug] = (typeCounts[slug] || 0) + 1;
      html += '<li data-cl-type="' + escHtml(slug) + '">' + escHtml(line.slice(2)).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>') + '</li>';
    } else if (line.trim() === '') {
      closeList();
    }
  }
  closeList();
  if (!html) html = '<p class="fineprint">No changelog entries found.</p>';
  // Type stats (like Money Buddy): clickable counts that filter the list
  const typeLabels = { added: 'Added', changed: 'Changed', fixed: 'Fixed' };
  const order = ['added', 'changed', 'fixed'];
  const shown = order.filter(t => typeCounts[t] > 0);
  let stats = '';
  if (shown.length) {
    stats = '<div class="cl-type-stats" role="group" aria-label="Change type counts">'
      + shown.map(t => '<button type="button" class="cl-type-stat cl-type-' + t + '" data-cl-type="' + t + '" aria-pressed="false"'
        + ' title="Filter to ' + typeLabels[t] + ' (click again to clear)">'
        + '<div class="value">' + typeCounts[t] + '</div><div class="label">' + typeLabels[t] + '</div></button>').join('')
      + '</div>';
  }
  html = stats + html;
  if (!bare) html += '<p class="fineprint"><a href="https://github.com/davedellaquila/buddy-system/blob/master/CHANGELOG.md" target="_blank" rel="noopener">Full changelog on GitHub</a></p>';
  return html;
}
/* Release Notes: render each change as a Change Log row, grouped by date
   with day headers — matching the Change Log view format exactly. */
function releaseNotesToHtml(md){
  const NL = String.fromCharCode(10);
  const lines = String(md || '').split(NL);
  const TYPE_ICON = { added: '+', changed: '~', fixed: '✓' };
  const groups = [];
  let curGroup = null, curType = '';
  function newGroup(dateStr, release){
    curGroup = { dateStr: dateStr, release: release, items: [] };
    groups.push(curGroup);
  }
  for (const raw of lines) {
    const line = raw.replace(/\s+$/, '');
    let m;
    if ((m = line.match(/^## (\d{4}-\d{2}-\d{2})\s*(?:\(([^)]*)\))?/))) {
      newGroup(m[1], (m[2] || '').trim());
      curType = '';
    } else if ((m = line.match(/^### (.+)/))) {
      curType = m[1].trim();
    } else if ((m = line.match(/^- (.+)/)) && curGroup) {
      const text = m[1].trim();
      const t = (curType || 'other').toLowerCase();
      let title = text, desc = '';
      const bm = text.match(/^\*\*([^*]+)\*\*:?\s*(.*)$/);
      if (bm) { title = bm[1].trim(); desc = bm[2].trim(); }
      else if (text.length > 80) { title = text.slice(0, 80).trim() + '…'; desc = text; }
      curGroup.items.push({
        icon: TYPE_ICON[t] || '•',
        title: title, desc: desc, type: curType || 'Update',
      });
    }
  }
  if (!groups.length) return '<p class="fineprint">No release notes found.</p>';
  return groups.map(g => {
    let dLabel = g.dateStr;
    try {
      const dp = g.dateStr.split('-');
      const d = new Date(+dp[0], +dp[1] - 1, +dp[2]);
      dLabel = dayLabel(d);
    } catch (e) {}
    const rows = g.items.map(it =>
      '<div class="cl-row">'
      + '<span class="cl-ic" aria-hidden="true">' + escHtml(it.icon) + '</span>'
      + '<div class="cl-body">'
      + '<div class="cl-title">' + escHtml(it.title).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>') + '</div>'
      + (it.desc ? '<div class="cl-desc">' + escHtml(it.desc).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>') + '</div>' : '')
      + '<div class="cl-time">' + escHtml(g.release ? g.release + ' · ' : '') + escHtml(it.type) + '</div>'
      + '</div></div>'
    ).join('');
    return '<h3 class="cl-day">' + escHtml(dLabel) + '</h3>'
      + '<div class="cl-group">' + rows + '</div>';
  }).join('');
}
function wireChangelogTypeFilter(root){
  if (!root) return;
  root.querySelectorAll('.cl-type-stat').forEach(btn => {
    btn.addEventListener('click', () => {
      const active = btn.getAttribute('aria-pressed') === 'true';
      root.querySelectorAll('.cl-type-stat').forEach(b => b.setAttribute('aria-pressed', 'false'));
      const slug = active ? '' : btn.dataset.clType;
      if (!active) btn.setAttribute('aria-pressed', 'true');
      root.querySelectorAll('li[data-cl-type]').forEach(li => {
        li.hidden = !!(slug && li.dataset.clType !== slug);
      });
      // Hide empty type headings and version sections when filtering
      root.querySelectorAll('h5[data-cl-type-head]').forEach(h => {
        const ul = h.nextElementSibling;
        const anyVisible = ul && ul.tagName === 'UL' && [...ul.children].some(li => !li.hidden);
        h.hidden = !!(slug && !anyVisible);
        if (ul && ul.tagName === 'UL') ul.hidden = !!(slug && !anyVisible);
      });
    });
  });
}
function whatsnewSeenKey(){ try { return localStorage.getItem('whatsnewSeen'); } catch (e) { return null; } }
function whatsnewHash(s){
  let h = 5381;
  s = String(s || '');
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36);
}
function whatsnewMarkSeen(md){
  try {
    // Seen key = newest header + hash of its section content, so new bullets
    // added under an existing header are still detected as new next time.
    const lines = String(md || '').split(String.fromCharCode(10));
    let header = '', section = [];
    for (const line of lines) {
      if (/^## /.test(line)) { if (header) break; header = line; continue; }
      if (header) section.push(line);
    }
    if (header) localStorage.setItem('whatsnewSeen', header + '|' + whatsnewHash(section.join(String.fromCharCode(10))));
  } catch (e) {}
}
function whatsnewSplit(md){
  const seen = whatsnewSeenKey();
  const NL = String.fromCharCode(10);
  const lines = String(md || '').split(NL);
  // Split into sections: [{header, body[]}]
  const sections = [];
  let cur = null;
  for (const line of lines) {
    if (/^## /.test(line)) { cur = {header: line, body: []}; sections.push(cur); }
    else if (cur) cur.body.push(line);
    else { cur = {header: '', body: [line]}; sections.push(cur); }
  }
  // Parse seen key: "header|hash" (new) or bare "header" (legacy).
  let seenHeader = '', seenHash = '';
  if (seen) {
    const pipe = seen.lastIndexOf('|');
    if (pipe > 0 && /^## /.test(seen.slice(0, pipe))) { seenHeader = seen.slice(0, pipe); seenHash = seen.slice(pipe + 1); }
    else seenHeader = seen;
  }
  const newLines = [], oldLines = [];
  let foundSeen = false;
  for (const s of sections) {
    if (s.header && seenHeader && s.header === seenHeader) {
      foundSeen = true;
      // Same header but content changed (new bullets added under it) → still new.
      // Legacy keys (no hash) can't prove what was seen, so show the section once.
      const curHash = whatsnewHash(s.body.join(NL));
      if (!seenHash || curHash !== seenHash) {
        newLines.push(s.header, ...s.body);
      } else {
        oldLines.push(s.header, ...s.body);
      }
      // Everything after the seen section is old.
      const idx = sections.indexOf(s);
      for (let i = idx + 1; i < sections.length; i++) oldLines.push(sections[i].header, ...sections[i].body);
      break;
    }
    if (!foundSeen) newLines.push(s.header, ...s.body);
    else oldLines.push(s.header, ...s.body);
  }
  if (seen && !foundSeen) {
    // Seen header gone (or legacy mismatch): fall back to newest 3 sections as new.
    let count = 0;
    newLines.length = 0; oldLines.length = 0;
    for (const s of sections) {
      if (s.header && /^## /.test(s.header)) count++;
      (count <= 3 ? newLines : oldLines).push(s.header, ...s.body);
    }
  }
  return { newMd: newLines.join(NL), oldMd: oldLines.join(NL), hasNew: newLines.some(l => /^- /.test(l)) };
}
function openWhatsNew(){
  let m = document.getElementById('whatsnew-modal');
  if (m) m.remove();
  m = document.createElement('div');
  m.id = 'whatsnew-modal';
  m.innerHTML = '<div class="wn-backdrop"></div><div class="wn-box" role="dialog" aria-label="What\u2019s new">'
    + '<div class="wn-head"><h3>What\u2019s new</h3><button class="wn-x" aria-label="Close">\u00d7</button></div>'
    + '<div class="wn-body"><p class="fineprint">Loading\u2026</p></div></div>';
  document.body.appendChild(m);
  const close = () => m.remove();
  m.querySelector('.wn-x').addEventListener('click', close);
  m.querySelector('.wn-backdrop').addEventListener('click', close);
  m.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  const body = m.querySelector('.wn-body');
  const head = m.querySelector('.wn-head');
  // Update button (only shows if a newer build is actually available)
  const updBtn = document.createElement('button');
  updBtn.textContent = 'Update';
  updBtn.style.cssText = 'margin-left:auto;margin-right:8px;padding:6px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:#fff;font-weight:600;cursor:pointer;display:none';
  updBtn.addEventListener('click', () => {
    try { sessionStorage.setItem('updateClicked', String(Date.now())); } catch (e) {}
    location.href = location.pathname + '?v=' + Date.now() + location.hash;
  });
  head.insertBefore(updBtn, head.querySelector('.wn-x'));
  fetch('version.txt?_=' + Date.now(), {cache: 'no-store'})
    .then(r => r.ok ? r.text() : '')
    .then(t => {
      const serverBuild = t.trim();
      if (serverBuild && serverBuild !== '__BUILD__') {
        updBtn.style.display = '';
        updBtn.title = 'Update to build ' + serverBuild;
      }
      // Show build numbers at the top of the sheet (Dave's request 2026-10-12)
      const myBuild = '__BUILD__';
      let buildLine = '<p class="fineprint" style="margin-top:0">You\u2019re on build ' + escHtml(myBuild) + '.';
      if (serverBuild && serverBuild !== '__BUILD__' && isNewerBuild(serverBuild, myBuild)) {
        buildLine += ' Build ' + escHtml(serverBuild) + ' is available.';
      }
      buildLine += '</p>';
      body.insertAdjacentHTML('afterbegin', buildLine);
    })
    .catch(() => {});
  fetch('https://raw.githubusercontent.com/davedellaquila/buddy-system/master/CHANGELOG.md?_' + Date.now(), {cache: 'no-store'})
    .then(r => { if (!r.ok) throw new Error('fetch failed'); return r.text(); })
    .then(md => {
      const sp = whatsnewSplit(md);
      let html = '';
      if (sp.hasNew) {
        html += '<h4 style="margin-top:0">New since you last looked</h4>' + changelogMdToHtml(sp.newMd, true);
      } else {
        html += '<p class="fineprint" style="margin-top:0">You\u2019re up to date \u2014 nothing new since you last looked.</p>';
      }
      if (sp.oldMd.trim()) {
        html += '<details style="margin-top:12px"><summary class="fineprint" style="cursor:pointer">Earlier history</summary>'
          + changelogMdToHtml(sp.oldMd, true) + '</details>';
      }
      html += '<p class="fineprint"><a href="https://github.com/davedellaquila/buddy-system/blob/master/CHANGELOG.md" target="_blank" rel="noopener">Full changelog on GitHub</a></p>';
      body.innerHTML = html;
      wireChangelogTypeFilter(body);
      // Mark seen only AFTER the split + render, so the "new" section is
      // computed against the previous visit — not the one that just happened.
      whatsnewMarkSeen(md);
    })
    .catch(() => { body.innerHTML = '<p class="fineprint">Couldn\u2019t load the changelog. <a href="https://github.com/davedellaquila/buddy-system/blob/master/CHANGELOG.md" target="_blank" rel="noopener">View it on GitHub</a>.</p>'; });
  const x = m.querySelector('.wn-x');
  if (x) x.focus();
}
function isNewerBuild(server, mine){
  // Compare build numbers like 20261012.1028 — lexicographic works for zero-padded format
  try {
    return String(server).trim() > String(mine).trim();
  } catch (e) { return false; }
}
function initVersionCheck(){
  const myBuild = '__BUILD__';
  function showUpdateBanner(serverBuild){
    if (document.getElementById('update-banner')) return;
    const b = document.createElement('div');
    b.id = 'update-banner';
    b.innerHTML = '<span>You\u2019re on build ' + escHtml(myBuild) + '. Build ' + escHtml(serverBuild) + ' is available.</span> '
      + '<button id="update-whatsnew" style="margin-left:12px;background:none;border:none;color:var(--accent);font-size:14px;cursor:pointer;text-decoration:underline;padding:6px 4px">What\u2019s new</button>'
      + '<button id="update-now" style="margin-left:12px;padding:6px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:#fff;font-weight:600;cursor:pointer">Update now</button>'
      + '<button id="update-dismiss" aria-label="Dismiss" style="margin-left:8px;padding:6px 10px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text);font-size:16px;cursor:pointer;line-height:1">×</button>';
    b.style.cssText = 'position:fixed;top:16px;left:50%;transform:translateX(-50%);z-index:9999;background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:12px 18px;box-shadow:0 8px 32px rgba(0,0,0,.3);display:flex;align-items:center;font-size:14px';
    document.body.appendChild(b);
    document.getElementById('update-whatsnew').addEventListener('click', () => { openWhatsNew(); });
    document.getElementById('update-now').addEventListener('click', () => {
      b.remove();
      try { sessionStorage.setItem('updateClicked', String(Date.now())); } catch (e) {}
      location.href = location.pathname + '?v=' + Date.now() + location.hash;
    });
    document.getElementById('update-dismiss').addEventListener('click', () => {
      b.remove();
    });
  }
  async function checkForUpdate(){
    try {
      const r = await fetch('version.txt?_=' + Date.now(), {cache: 'no-store'});
      if (!r.ok) return 'error';
      const serverBuild = (await r.text()).trim();
      // Don't show the banner for 10 min after "Update now" was clicked (gives Pages time to deploy)
      try {
        const clicked = parseInt(sessionStorage.getItem('updateClicked') || '0', 10);
        if (clicked && Date.now() - clicked < 10 * 60 * 1000) return 'suppressed';
      } catch (e) {}
      if (serverBuild && isNewerBuild(serverBuild, myBuild)) {
        showUpdateBanner(serverBuild);
        return 'new';
      }
      return 'current';
    } catch (e) { return 'error'; }
  }
  window.__buddyUpdateCheck = checkForUpdate;
  checkForUpdate();
  setInterval(checkForUpdate, 5 * 60 * 1000);
}
// Pull-down at the top of any scrollable view triggers a manual update check.
function initPullToRefresh(){
  const THRESHOLD = 70;
  const PILL_DELAY = 350;
  let pill = null, pillVisible = false, pillTimer = null;
  function scrollableAncestor(el, doc){
    const d = doc || document;
    while (el && el !== d.body && el !== d.documentElement) {
      if (el.scrollHeight > el.clientHeight + 4) return el;
      el = el.parentElement;
    }
    const de = d.documentElement;
    if (de.scrollHeight > de.clientHeight + 4) return de;
    return d.body;
  }
  function ensurePill(){
    if (pill) return pill;
    pill = document.createElement('div');
    pill.setAttribute('aria-live', 'polite');
    pill.style.cssText = 'position:fixed;top:10px;left:50%;transform:translateX(-50%) translateY(-8px);z-index:10000;background:var(--panel);border:1px solid var(--border);border-radius:999px;padding:8px 16px;font-size:13px;color:var(--text);opacity:0;transition:opacity .18s,transform .18s;pointer-events:none;box-shadow:0 4px 16px rgba(0,0,0,.18);white-space:nowrap';
    document.body.appendChild(pill);
    return pill;
  }
  function showPill(text){
    const p = ensurePill();
    p.textContent = text;
    p.style.opacity = '1';
    p.style.transform = 'translateX(-50%) translateY(0)';
    pillVisible = true;
  }
  function hidePill(){
    if (!pill) return;
    pill.style.opacity = '0';
    pill.style.transform = 'translateX(-50%) translateY(-8px)';
    pillVisible = false;
  }
  function toast(text, ms){
    showPill(text);
    setTimeout(hidePill, ms || 2200);
  }
  // Bind the pull gesture on a document. The dashboard binds its own document;
  // the homepage iframe's document is bound on load (same-origin homepages),
  // so pull-to-refresh works while a buddy homepage is showing. The pill and
  // the update check always live in the parent window.
  function bindDoc(doc){
    if (!doc || doc.__ptrBound) return;
    doc.__ptrBound = true;
    let track = null;
    doc.addEventListener('touchstart', function(e){
      if (e.touches.length !== 1) { track = null; return; }
      const t = e.touches[0];
      const sc = scrollableAncestor(e.target, doc);
      track = (sc && sc.scrollTop <= 0) ? { y0: t.clientY, x0: t.clientX } : null;
    }, {passive: true});
    doc.addEventListener('touchmove', function(e){
      if (!track) return;
      const t = e.touches[0];
      const dy = t.clientY - track.y0, dx = t.clientX - track.x0;
      if (Math.abs(dx) > Math.abs(dy) * 1.4) { track = null; hidePill(); if (pillTimer) { clearTimeout(pillTimer); pillTimer = null; } return; }
      if (dy > 24 && !pillTimer && !pillVisible) {
        pillTimer = setTimeout(function(){
          pillTimer = null;
          if (!track) return;
          showPill(dy > THRESHOLD ? 'Release to check for updates' : 'Keep pulling to check for updates');
        }, PILL_DELAY);
      } else if (dy > THRESHOLD && pillVisible) {
        showPill('Release to check for updates');
      } else if (dy <= 24 && pillVisible) {
        hidePill();
      } else if (dy <= 24 && pillTimer) {
        clearTimeout(pillTimer); pillTimer = null;
      }
    }, {passive: true});
    function onEnd(){
      if (pillTimer) { clearTimeout(pillTimer); pillTimer = null; }
      if (!track) return;
      const engaged = pillVisible;
      track = null;
      hidePill();
      if (!engaged) return;
      const run = window.__buddyUpdateCheck;
      if (!run) return;
      showPill('Checking for updates…');
      run().then(function(status){
        if (status === 'new') { hidePill(); }
        else if (status === 'current' || status === 'suppressed') toast('You are up to date');
        else toast('Could not check — are you offline?');
      });
    }
    doc.addEventListener('touchend', onEnd, {passive: true});
    doc.addEventListener('touchcancel', function(){ track = null; hidePill(); }, {passive: true});
  }
  bindDoc(document);
  window.__bindPullToRefresh = bindDoc;
}
function initSearch(){
  const bs = document.getElementById('buddy-search');
  const cb = document.getElementById('buddy-search-clear');
  if (cb && !cb.dataset.init) {
    cb.dataset.init = '1';
    const sync = () => { cb.hidden = !bs.value; };
    bs.addEventListener('input', sync); sync();
    cb.addEventListener('click', () => {
      bs.value = '';
      bs.dispatchEvent(new Event('input', {bubbles: true}));
      sync(); bs.focus();
      // Clearing the filter restores the full Atlas view
      if (S.view === 'tree' || S.sel === 'view:tree') renderOrgTree();
    });
  }
  if (bs && !bs.dataset.init) {
    bs.dataset.init = '1';
    // Autocomplete dropdown (Dave 2026-10-12) — matches narrow as you type
    const wrap = bs.closest('.sb-search-sticky') || bs.parentElement;
    if (wrap && getComputedStyle(wrap).position === 'static') wrap.style.position = 'relative';
    let ac = document.getElementById('buddy-ac');
    if (!ac && wrap) {
      ac = document.createElement('div');
      ac.id = 'buddy-ac'; ac.hidden = true;
      ac.setAttribute('role', 'listbox');
      wrap.appendChild(ac);
    }
    let acHot = -1;
    const acClose = () => { if (ac){ ac.hidden = true; } acHot = -1; };
    const acMatches = (q) => {
      const words = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
      if (!words.length) return [];
      return BUDDIES.filter(b => {
        if (b.id === ROOT_ID) return false;
        const hay = (dispName(b) + ' ' + (b.name || '') + ' ' + (b.tagline || '') + ' ' + effAka(b).join(' ')).toLowerCase();
        return words.every(w => hay.includes(w));
      }).slice(0, 8);
    };
    const acParentName = (b) => {
      const p = b.parent ? byId[b.parent] : null;
      return p ? dispName(p) : '';
    };
    const acRender = () => {
      if (!ac) return;
      const q = bs.value.trim();
      if (!q){ acClose(); return; }
      const ms = acMatches(q);
      acHot = ms.length ? 0 : -1;
      ac.innerHTML = ms.length
        ? ms.map((b, i) => '<button type="button" class="bac-row' + (i === acHot ? ' hot' : '') + '" role="option" data-buddy="' + b.id + '">'
          + '<span class="bicon">' + escHtml(b.icon || '') + '</span>'
          + '<span class="bname">' + escHtml(dispName(b)) + '</span>'
          + (acParentName(b) ? '<span class="bctx">' + escHtml(acParentName(b)) + '</span>' : '')
          + '</button>').join('')
        : '<div class="bac-empty">No buddies match.</div>';
      ac.hidden = false;
      ac.querySelectorAll('.bac-row').forEach(row => {
        row.addEventListener('click', () => {
          const bid = row.dataset.buddy;
          acClose(); bs.value = ''; bs.dispatchEvent(new Event('input', {bubbles: true}));
          selectBuddy(bid);
        });
      });
    };
    const acMove = (dir) => {
      if (!ac || ac.hidden) return;
      const rows = ac.querySelectorAll('.bac-row');
      if (!rows.length) return;
      acHot = (acHot + dir + rows.length) % rows.length;
      rows.forEach((r, i) => r.classList.toggle('hot', i === acHot));
      rows[acHot].scrollIntoView({block: 'nearest'});
    };
    bs.addEventListener('input', () => {
      renderNav();
      acRender();
      // Atlas view follows the buddy-list filter (Dave's request 2026-10-12)
      if (S.view === 'tree' || S.sel === 'view:tree') renderOrgTree();
      if (S.sel === 'view:tree') { const m = firstSearchMatch(); if (m) centerOnBuddy(m); }
    });
    bs.addEventListener('keydown', (e) => {
      if (!ac || ac.hidden) return;
      if (e.key === 'ArrowDown'){ e.preventDefault(); acMove(1); }
      else if (e.key === 'ArrowUp'){ e.preventDefault(); acMove(-1); }
      else if (e.key === 'Enter' && acHot >= 0){
        e.preventDefault();
        const rows = ac.querySelectorAll('.bac-row');
        if (rows[acHot]) rows[acHot].click();
      }
      else if (e.key === 'Escape'){ acClose(); }
    });
    document.addEventListener('click', (e) => {
      if (ac && !ac.hidden && !ac.contains(e.target) && e.target !== bs) acClose();
    });
  }
}
function refreshTokenUI(id){
  updateTokenPill();
  updateTokenGating(id);
  refreshHomepageDumpbox();
  // renderBuddy(id) means the panel is showing this buddy — load its feed
  // regardless of S.sel (which stays 'view:xxx' when the panel opens from a view).
  if (id) {
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
/* ---------- info-tip popovers: hover preview on mouse, tap-to-pin with × on touch ----------
   (Pure-CSS :hover tooltips stick open on touch screens with no way to dismiss.) */
let tipPop = null;
function tipPopClose(){ if (tipPop) { tipPop.remove(); tipPop = null; } }
function tipPopShow(icon, pinned){
  tipPopClose();
  if (typeof escHtml !== 'function') return;
  const pop = document.createElement('div');
  pop.className = 'tip-pop' + (pinned ? ' pinned' : '');
  pop.innerHTML = (pinned ? '<button type="button" class="tip-x" aria-label="Close tooltip">\u00d7</button>' : '')
    + '<div class="tip-text">' + escHtml(icon.getAttribute('data-tip') || '') + '</div>';
  pop._icon = icon;
  document.body.appendChild(pop);
  const r = icon.getBoundingClientRect();
  pop.style.left = Math.max(8, Math.min(window.innerWidth - pop.offsetWidth - 8, r.left - 10)) + 'px';
  let top = r.bottom + 8;
  if (top + pop.offsetHeight > window.innerHeight - 8) top = Math.max(8, r.top - pop.offsetHeight - 8);
  pop.style.top = top + 'px';
  tipPop = pop;
  if (pinned) pop.querySelector('.tip-x').addEventListener('click', e => { e.stopPropagation(); tipPopClose(); });
}
document.addEventListener('pointerover', e => {
  if (e.pointerType === 'touch') return; // touch uses tap-to-pin
  const icon = e.target && e.target.closest ? e.target.closest('.info-tip') : null;
  if (!icon || (tipPop && tipPop._icon === icon)) return;
  tipPopShow(icon, false);
});
document.addEventListener('pointerout', e => {
  const icon = e.target && e.target.closest ? e.target.closest('.info-tip') : null;
  if (!icon || !tipPop || tipPop._icon !== icon || tipPop.classList.contains('pinned')) return;
  tipPopClose();
});
document.addEventListener('click', e => {
  const icon = e.target && e.target.closest ? e.target.closest('.info-tip') : null;
  if (tipPop && tipPop.classList.contains('pinned') && !icon && !(e.target.closest && e.target.closest('.tip-pop'))) {
    tipPopClose(); return;
  }
  if (icon) {
    if (tipPop && tipPop._icon === icon && tipPop.classList.contains('pinned')) tipPopClose();
    else tipPopShow(icon, true);
  }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') tipPopClose(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLensPicker(); });
document.addEventListener('input', e => {
  if (e.target && e.target.id === 'proj-search') {
    projSearch = e.target.value;
    const pos = e.target.selectionStart;
    renderProjects();
    const ni = document.getElementById('proj-search');
    if (ni) { ni.focus(); try { ni.setSelectionRange(pos, pos); } catch (err) {} }
  }
});
document.addEventListener('click', e => {
  if (nodeDragEndAt && Date.now() - nodeDragEndAt < 400) return; // swallow the click that follows a node-drag gesture
  if (edgeOpenAt && Date.now() - edgeOpenAt < 400) return; // swallow the click that follows an edge-swipe open
  const bpb = e.target.closest && e.target.closest('.bp-build');
  if (bpb) { openWhatsNew(); return; }
  if (e.target.closest && e.target.closest('#bp-icon')) { const m = S.sel.match(/^buddy:(.+)$/); if (m) openAvatarPicker(m[1], e.target.closest('#bp-icon')); return; }
  const co = e.target.closest && e.target.closest('[data-close-order]');
  if (co) {
    const oid = co.getAttribute('data-close-order');
    S.dismissedOrders = S.dismissedOrders || [];
    if (S.dismissedOrders.indexOf(oid) < 0) S.dismissedOrders.push(oid);
    save();
    const card = co.closest('.standing-order'); if (card) card.remove();
    return;
  }
  if (e.target.closest && (e.target.closest('#bp-close-x') || e.target.closest('#bp-takeover-back'))) { closeDetail(); return; }
  if (e.target.closest && e.target.closest('#panel-open')) {
    const id = (S.projectId && byId[S.projectId]) ? S.projectId : ROOT_ID;
    openBuddy(id);
    return;
  }
  if (e.target.closest && e.target.closest('#sb-close')) { setSidebarOpen(false); return; }
  if (e.target.closest && e.target.closest('#menu-btn')) {
    // State-dependent per Dave's rule: with the right (detail) panel open, the
    // floating › closes it (same screen position as the drawer's open chevron).
    const _vb = document.getElementById('view-buddy');
    if (_vb && _vb.classList.contains('active') && (_vb.classList.contains('panel') || _vb.classList.contains('sheet'))) { closeDetail(); return; }
    setSidebarOpen(!isSidebarOpen()); return;
  }
  if (e.target.closest && e.target.closest('#sb-scrim')) { setSidebarOpen(false); return; }
  if (e.target.closest && e.target.closest('#bp-desktop')) { const m = S.sel.match(/^buddy:(.+)$/); if (m) saveToDesktop(m[1]); return; }
  if (e.target.closest && e.target.closest('#bp-settings')) { openFieldSettings(); return; }
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
  if (vb) {
    // "All buddies" from the info panel: remember the buddy so the projects
    // view can scroll to and highlight it — you don't lose your place.
    const fromPanel = vb.id === 'bp-allbuddies' || (vb.dataset.view === 'projects' && S.sel && S.sel.startsWith('buddy:'));
    if (fromPanel && S.sel && S.sel.startsWith('buddy:')) pendingHighlight = S.sel.slice(6);
    show('view:' + vb.dataset.view);
    if (window.innerWidth < 640) { const sbo=document.getElementById('sidebar'); if(sbo) sbo.classList.remove('open'); const sco=document.getElementById('sb-scrim'); if(sco) sco.classList.remove('show'); }
    if (pendingHighlight) { const id = pendingHighlight; pendingHighlight = null; highlightProjectRow(id); }
    return;
  }
  // Atlas lens picker: pill toggles, cards switch, scrim/close/Escape dismisses
  const pill = e.target.closest('#lens-pill');
  if (pill) {
    const dd = document.getElementById('lens-dropdown');
    const scrim = document.getElementById('lens-scrim');
    const open = dd.hidden;
    dd.hidden = !open; scrim.hidden = !open;
    pill.setAttribute('aria-expanded', open);
    return;
  }
  const lclose = e.target.closest('#lens-close');
  if (lclose) { closeLensPicker(); return; }
  const lcard = e.target.closest('.lens-card[data-chart]');
  if (lcard) {
    closeLensPicker();
    const chart = document.querySelector('#treezoom-main .chart');
    if (chart) chart.classList.add('chart-switching');
    setTimeout(() => setChartType(lcard.dataset.chart), 140);
    return;
  }
  const lscrim = e.target.closest('#lens-scrim');
  if (lscrim) { closeLensPicker(); return; }
  const pmb = e.target.closest('[data-proj-mode]');
  if (pmb) { projViewMode = pmb.dataset.projMode; renderProjects(); return; }
  if (e.target.closest && e.target.closest('#proj-search-clear')) { projSearch = ''; renderProjects(); const ps = document.getElementById('proj-search'); if (ps) ps.focus(); return; }
  const pb = e.target.closest('[data-plan]');
  if (pb) { e.preventDefault(); show('plan:' + pb.dataset.plan); return; }
  // Don't auto-close the phone drawer for sidebar chrome (#sb-to-top is a sibling of #sidebar)
  if (!(e.target.closest && e.target.closest('#sb-to-top,#sb-resize,#sidebar'))) {
    const sb2 = document.getElementById('sidebar');
    if (sb2) sb2.classList.remove('open');
  }
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
    // The chevron is isolated on the far left: only it toggles expand/collapse.
    const pt = e.target.closest('[data-proj-toggle]');
    if (pt) {
      const bid = pt.dataset.projToggle;
      if (!S.projCollapsed || typeof S.projCollapsed !== 'object') S.projCollapsed = {};
      if (e.shiftKey) {
        // Shift-click: apply to all project sections
        const willCollapse = !S.projCollapsed[bid];
        document.querySelectorAll('#view-projects [data-proj-toggle]').forEach(el => {
          S.projCollapsed[el.dataset.projToggle] = willCollapse;
        });
      } else {
        S.projCollapsed[bid] = !S.projCollapsed[bid];
      }
      save(); renderProjects();
      return;
    }
    // Anywhere else on the row toggles this buddy's info panel.
    const bid = projRow.dataset.buddy;
    const vb = document.getElementById('view-buddy');
    if (vb && vb.classList.contains('active') && S.projectId === bid) closeDetail();
    else openBuddy(bid);
    return;
  }
  const hp = e.target.closest('[data-homepage]');
  if (hp) { e.preventDefault(); selectProject(hp.dataset.homepage); return; }
  const ctog = e.target.closest && e.target.closest('[data-ctog]');
  if (ctog) {
    const cid = ctog.getAttribute('data-ctog');
    if (!S.navCollapsed || typeof S.navCollapsed !== 'object') S.navCollapsed = {};
    const willCollapse = !S.navCollapsed[cid];
    if (e.shiftKey) {
      // Shift+click: apply to the whole subtree, not just this row.
      (function walk(id){
        if (willCollapse) S.navCollapsed[id] = true; else delete S.navCollapsed[id];
        (kidsOf[id] || []).forEach(c => walk(c.id));
      })(cid);
    } else {
      if (willCollapse) S.navCollapsed[cid] = true; else delete S.navCollapsed[cid];
    }
    save(); renderNav();
    return;
  }
  const bb = e.target.closest('[data-buddy]');
  // Don't re-open the buddy when clicking an editable field (e.g. the name)
  // Panel behavior is view-aware: in Homepage view, clicking selects only
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
  const sb = e.target.closest('[data-done]');
  if (sb) { markAttentionDone(sb.dataset.done, sb); return; }
  const sa = e.target.closest('[data-done-all]');
  if (sa) { markAllAttentionDone(sa.dataset.doneAll); return; }
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
// Flush any dumps that were queued while offline or token-less (Dave 2026-10-12)
flushPendingDumps();
initGear();
initSbToTop();
initBpToTop();
initNerdSettings();
initNewBuddyFab();
initEdgeSwipeOpen();
initPanelSwipeGestures();
initVersionCheck();
initPullToRefresh();
initPlansToggle();
initNavSecToggles();
initNavSecDnD();
applyNavSecOrder();
initSbBrandSticky();
"""
    js = js.replace("BUDDIES_JSON", buddies_js).replace("ORDER_JSON", order_js).replace("PLANS_JSON", plans_js).replace("PERSONA_ROSTER_JSON", roster_js)
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
<button id="menu-btn" aria-label="Open sidebar">\u203a</button>
<button type="button" id="panel-open" title="Open buddy details" aria-label="Open buddy details">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 5.5L8 12l6.5 6.5"/></svg>
</button>
<div id="sb-scrim"></div>
<aside id="sidebar">
  <div class="sb-brand-sticky">
    <div id="sb-tools"><button id="sb-gear" title="Settings (⌘,)" aria-label="Settings"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></button><button id="sb-close" title="Collapse sidebar" aria-label="Collapse sidebar"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 5.5L8 12l6.5 6.5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>
    <div class="brand"><div class="eyebrow">Project Buddy</div><h1 id="brand-name" title="Click to rename">Buddies</h1><div class="bcount">NBUD buddies &middot; one family</div></div>
  </div>
  <div class="sb-search-sticky">
    <div class="sb-search-wrap">
    <input type="search" id="buddy-search" placeholder="Search buddies\u2026" aria-label="Search buddies"
      title="Search all buddies by name or tagline. Filters the sidebar list as you type. Press / anywhere to jump here. Arrow keys navigate results.">
    <button type="button" id="buddy-search-clear" aria-label="Clear search" title="Clear search" hidden>×</button>
    </div>
  </div>
  <div class="nav-sec" id="buddies-sec">
  <h3 style="cursor:pointer" id="buddies-toggle"><span class="nav-arrow" id="buddies-arrow">\u203a</span> Buddies <span id="attn-pill" class="zero">0</span></h3><div id="buddy-nav"></div></div>
  <div class="nav-sec" id="plans-sec"><h3 style="cursor:pointer" id="plans-toggle"><span id="plans-arrow">\u203a</span> Business Plans</h3><div id="plan-nav"></div></div>
  <div class="nav-sec" id="views-sec">
  <h3 style="cursor:pointer" id="views-toggle"><span class="nav-arrow" id="views-arrow">\u203a</span> Views</h3><div id="view-nav"></div></div>
</aside>
<div id="sb-resize" title="Drag left or right to resize the sidebar. Double-click to close."></div>
<button type="button" id="sb-to-top" title="Scroll sidebar to top" aria-label="Scroll sidebar to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M6 11l6-6 6 6"/></svg>
</button>
<button type="button" id="bp-to-top" title="Scroll panel to top" aria-label="Scroll panel to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M6 11l6-6 6 6"/></svg>
</button>
<button type="button" id="new-buddy-fab" title="New buddy" aria-label="New buddy">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
</button>
<main id="main">
<div id="journal-bar"></div>
""" + vt + vp + vpl + vm + """
<section id="view-buddy" class="view"><div id="bp-resize" title="Drag left or right to resize the buddy detail panel. Double-click to reset to default width."></div><div id="buddy-home"></div></section>
<section id="view-project" class="view"></section>
<section id="view-changelog" class="view"></section>
<section id="view-releases" class="view"></section>
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

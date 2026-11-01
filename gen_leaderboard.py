#!/usr/bin/env python3
"""Generate astro/leaderboard.html — the fleet homepage leaderboard.

Reads buddies.json (roster, summaries, personas) and astro/homepage-scores.json
(scores awarded by the homepage-audition scoring pass; {} until the pass runs).
Rows sort: scored pages by score descending, then unscored pages A–Z.
Page type (custom vs auto-generated template) is detected from each buddy's
served index.html using the generator's own markers.
"""
import json, os, html, datetime, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Privacy redaction (added 2026-11-01, Dave's strip ruling): scoring notes and
# registry summaries are rendered on this public page, so identifiers must
# never reach the HTML — precise coordinates, emails, phone numbers, and
# house-number street addresses are generalized at render time. The source
# data (homepage-scores.json, buddies.json) is not modified here.
def redact(text):
    if not text:
        return text
    text = re.sub(r"-?\d{1,3}\.\d{4,}\s*,\s*-?\d{1,3}\.\d{4,}", "[coordinates removed]", text)
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email removed]", text)
    text = re.sub(r"\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}", "[phone removed]", text)
    text = re.sub(r"\b\d{3,6}\s+([A-Z][A-Za-z]+ ){1,3}(Dr|Way|Ln|St|Ave|Rd|Ct|Blvd)\b", "[address removed]", text)
    # Lenwood family rent figures (bucket C) where notes quote them
    text = re.sub(r"\$1,000\s*(?:→|->|to)\s*\$2,000(?:/mo)?", "[rent figures removed]", text)
    text = re.sub(r"\$[12],000/mo rent", "rent", text)
    text = re.sub(r"rent \$[12],000", "rent", text)
    return text

def band_for(score):
    if score >= 90: return "Showcase"
    if score >= 75: return "Strong"
    if score >= 60: return "Serviceable"
    if score >= 40: return "Needs work"
    return "Drawing board"

def main():
    buddies = json.load(open(os.path.join(ROOT, "buddies.json")))["buddies"]
    spath = os.path.join(ROOT, "astro", "homepage-scores.json")
    scores = json.load(open(spath)) if os.path.exists(spath) else {}
    names = {b["id"]: b["name"] for b in buddies}

    rows = []
    for b in buddies:
        p = os.path.join(ROOT, b["id"], "index.html")
        ptype = "Custom"
        if os.path.exists(p):
            c = open(p, encoding="utf-8", errors="ignore").read()
            if "BUDDY-BASIC-TEMPLATE" in c or "Part of the Buddy System" in c:
                ptype = "Template"
        else:
            ptype = "Template"
        summary = (b.get("purpose") or b.get("mission") or "").strip()
        if len(summary) > 220:
            summary = summary[:217].rsplit(" ", 1)[0] + "…"
        s = scores.get(b["id"])
        rows.append({
            "id": b["id"], "name": b["name"], "icon": b.get("icon", "•"),
            "persona": b.get("persona", ""), "parent": names.get(b.get("parent", ""), ""),
            "summary": redact(summary), "type": ptype,
            "score": s["score"] if s else None,
            "band": (s.get("band") or band_for(s["score"])) if s else None,
            "sdate": s.get("date", "") if s else "",
            "notes": redact(s.get("notes", "")) if s else "",
        })
    scored = sorted([r for r in rows if r["score"] is not None], key=lambda r: (-r["score"], r["name"]))
    unscored = sorted([r for r in rows if r["score"] is None], key=lambda r: r["name"])
    ordered = scored + unscored
    n_custom = sum(1 for r in rows if r["type"] == "Custom")
    avg = round(sum(r["score"] for r in scored) / len(scored), 1) if scored else None
    today = datetime.date.today().strftime("%B %-d, %Y")

    def esc(x): return html.escape(str(x), quote=True)
    trs = []
    for i, r in enumerate(ordered, 1):
        rank = i if r["score"] is not None else "—"
        if r["score"] is not None:
            badge = f'<span class="score b-{esc(r["band"].replace(" ", "-").lower())}">{r["score"]}<small>{esc(r["band"])}</small></span>'
        else:
            badge = '<span class="score b-none">Not yet scored</span>'
        chip = '<span class="chip custom">Custom page</span>' if r["type"] == "Custom" else '<span class="chip template">Template — audition not yet taken</span>'
        notes = f'<div class="notes">{esc(r["notes"])}</div>' if r["notes"] else ""
        sdate = f' · scored {esc(r["sdate"])}' if r["sdate"] else ""
        trs.append(f'''<div class="row" data-name="{esc(r["name"].lower())}" data-summary="{esc(r["summary"].lower())}" data-type="{r["type"].lower()}" data-scored="{1 if r["score"] is not None else 0}">
  <div class="rank">{rank}</div>
  <div class="who"><a class="bname" href="../{esc(r["id"])}/">{esc(r["icon"])} {esc(r["name"])}</a>
    <div class="meta">{chip}{(" · " + esc(r["persona"])) if r["persona"] else ""}{(" · under " + esc(r["parent"])) if r["parent"] else ""}{sdate}</div>
    <div class="summary">{esc(r["summary"])}</div>{notes}</div>
  <div class="scorebox">{badge}</div>
</div>''')

    tipjar = open(os.path.join(ROOT, "docs", "tipjar-snippet.html"), encoding="utf-8").read()
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>🏆 Homepage Leaderboard — Astro</title>
<style>
:root{{--bg:#f6f8fa;--panel:#ffffff;--ink:#1c2333;--dim:#5a6a85;--line:#d8dee9;--accent:#7c5cd6}}
@media (prefers-color-scheme: dark){{:root{{--bg:#0d1117;--panel:#161b26;--ink:#e6edf7;--dim:#8b98ad;--line:#2a3244;--accent:#a78bfa}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
header{{position:sticky;top:0;z-index:10;background:var(--panel);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:10px;align-items:center}}
header .t{{font-weight:700}} header a{{color:var(--accent);text-decoration:none;font-size:14px}}
main{{max-width:920px;margin:0 auto;padding:18px 14px 40px}}
h1{{font-size:24px;margin:6px 0 4px}} .sub{{color:var(--dim);line-height:1.5;margin:0 0 14px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}}
.stat{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 14px;min-width:110px}}
.stat b{{font-size:20px;display:block}} .stat span{{color:var(--dim);font-size:12px}}
.controls{{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 14px}}
.controls input{{flex:1;min-width:180px;padding:9px 12px;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--ink)}}
.fbtn{{padding:8px 12px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer;font-size:13px}}
.fbtn.on{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.row{{display:flex;gap:12px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0 0 8px;align-items:flex-start}}
.rank{{font-size:18px;font-weight:700;color:var(--dim);min-width:30px;text-align:right;padding-top:2px}}
.who{{flex:1;min-width:0}} .bname{{color:var(--ink);font-weight:700;text-decoration:none;font-size:16px}}
.meta{{color:var(--dim);font-size:12.5px;margin:3px 0}} .summary{{line-height:1.45;font-size:14px}} .notes{{color:var(--dim);font-size:13px;margin-top:4px;font-style:italic}}
.chip{{border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:11.5px}}
.chip.custom{{color:#2ea043}} .chip.template{{color:var(--dim)}}
.score{{display:inline-block;text-align:center;border-radius:10px;padding:6px 10px;font-weight:800;font-size:18px;border:1px solid var(--line);min-width:74px}}
.score small{{display:block;font-size:10.5px;font-weight:600}}
.b-showcase{{background:#f5c54233;border-color:#f5c542}} .b-strong{{background:#2ea04326}} .b-serviceable{{background:#d2992226}}
.b-needs-work{{background:#f778ba26}} .b-drawing-board{{background:#f8514926}} .b-none{{color:var(--dim);font-size:12.5px;font-weight:600}}
footer{{color:var(--dim);font-size:13px;line-height:1.6;margin-top:18px}} footer a{{color:var(--accent)}}
</style>
</head>
<body>
<header><span class="t">🏆 Homepage Leaderboard</span><a href="../astro/">← Astro's homepage</a><a href="https://davedellaquila.github.io/buddy-system/">Buddy System dashboard</a></header>
<main>
<h1>Every buddy homepage, scored and ranked</h1>
<p class="sub">Each page is scored by Astro against the published <a href="https://github.com/davedellaquila/buddy-system/blob/master/docs/homepage-audition.md">homepage audition criteria</a> — 100 points across identity, real current data, working everywhere in dark + light, fleet standards, links, voice, honesty, and staying alive. Dave has the final eye. Pages a buddy never designed (auto-generated template) are marked as such — their audition is still to come.</p>
<div class="stats">
  <div class="stat"><b>{len(rows)}</b><span>pages listed</span></div>
  <div class="stat"><b>{len(scored)}</b><span>scored so far</span></div>
  <div class="stat"><b>{avg if avg is not None else "—"}</b><span>average score</span></div>
  <div class="stat"><b>{n_custom}</b><span>custom-designed pages</span></div>
  <div class="stat"><b>{len(rows) - n_custom}</b><span>template pages</span></div>
</div>
<div class="controls">
  <input id="q" type="search" placeholder="Search a buddy or what it does…" aria-label="Search the leaderboard">
  <button class="fbtn on" data-f="all">All</button>
  <button class="fbtn" data-f="scored">Scored</button>
  <button class="fbtn" data-f="unscored">Not yet scored</button>
  <button class="fbtn" data-f="custom">Custom</button>
  <button class="fbtn" data-f="template">Template</button>
</div>
<div id="board">
{chr(10).join(trs)}
</div>
<footer>Generated {today} from the buddy registry and the audition scorecard. Scores land here as the fleet scoring pass runs; when a buddy revises its page, its new score replaces the old and the climb is visible. Full criteria: <a href="https://github.com/davedellaquila/buddy-system/blob/master/docs/homepage-audition.md">The Homepage Audition — criteria &amp; scorecard</a>.</footer>
{tipjar}
</main>
<script>
const q=document.getElementById('q');let f='all';
function apply(){{const t=q.value.trim().toLowerCase();
document.querySelectorAll('.row').forEach(r=>{{let ok=true;
if(t&&!(r.dataset.name.includes(t)||r.dataset.summary.includes(t)))ok=false;
if(f==='scored'&&r.dataset.scored!=='1')ok=false;
if(f==='unscored'&&r.dataset.scored!=='0')ok=false;
if(f==='custom'&&r.dataset.type!=='custom')ok=false;
if(f==='template'&&r.dataset.type!=='template')ok=false;
r.style.display=ok?'':'none';}});}}
q.addEventListener('input',apply);
document.querySelectorAll('.fbtn').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('on'));b.classList.add('on');f=b.dataset.f;apply();}}));
</script>
</body>
</html>'''
    out = os.path.join(ROOT, "astro", "leaderboard.html")
    open(out, "w", encoding="utf-8").write(page)
    print(f"wrote {out}: {len(rows)} rows ({len(scored)} scored, {n_custom} custom)")

if __name__ == "__main__":
    main()

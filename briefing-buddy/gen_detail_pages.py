#!/usr/bin/env python3
"""Generate the 8 Briefing Buddy section detail pages.

Each page: newsroom aesthetic, dark+light theme toggle, back link to index.html,
and deeper content about its section. Output to the dashboard repo briefing-buddy/.
"""
import os

OUT = os.path.expanduser("~/workspace/projects/buddy-tree/briefing-buddy")

CSS = """  :root{
    --paper:#faf6ee; --card:#fffdf7; --ink:#221b12; --muted:#7d7060;
    --accent:#b45309; --accent-ink:#8a3f06; --accent-soft:#f6e8d2;
    --rule:#e2d7c0; --rule-strong:#221b12;
    --shadow:0 2px 14px rgba(80,55,15,.09);
    --chip:#f1e9d8;
  }
  @media (prefers-color-scheme:dark){
    :root[data-theme="auto"]{
      --paper:#131009; --card:#1e1912; --ink:#f2e9d6; --muted:#a79a82;
      --accent:#f0a83e; --accent-ink:#f5bd67; --accent-soft:#33270f;
      --rule:#38301f; --rule-strong:#f2e9d6;
      --shadow:0 2px 18px rgba(0,0,0,.45);
      --chip:#2b2314;
    }
  }
  :root[data-theme="dark"]{
    --paper:#131009; --card:#1e1912; --ink:#f2e9d6; --muted:#a79a82;
    --accent:#f0a83e; --accent-ink:#f5bd67; --accent-soft:#33270f;
    --rule:#38301f; --rule-strong:#f2e9d6;
    --shadow:0 2px 18px rgba(0,0,0,.45);
    --chip:#2b2314;
  }
  *{box-sizing:border-box}
  body{
    margin:0; background:var(--paper); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.6; -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:880px;margin:0 auto;padding:0 20px 64px}
  .masthead{text-align:center;padding:40px 0 8px}
  .masthead .kicker{
    font-size:11px;letter-spacing:4px;color:var(--muted);
    text-transform:uppercase;margin:0 0 10px;
  }
  .masthead .kicker a{color:var(--accent);text-decoration:none;font-weight:600}
  .masthead .kicker a:hover{text-decoration:underline}
  .masthead h1{
    font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    font-size:clamp(2rem,6vw,3.2rem);font-weight:700;margin:0;line-height:1.05;
  }
  .masthead .tagline{font-size:16px;color:var(--muted);margin:10px 0 0;font-style:italic;font-family:Georgia,serif}
  .dateline{
    display:flex;justify-content:space-between;align-items:center;gap:12px;
    border-top:3px double var(--rule-strong);border-bottom:1px solid var(--rule-strong);
    margin:22px 0 0;padding:9px 2px;font-size:12.5px;color:var(--muted);
    text-transform:uppercase;letter-spacing:1.5px;flex-wrap:wrap;
  }
  .theme-btn{
    border:1px solid var(--rule);background:var(--card);color:var(--ink);
    border-radius:999px;padding:5px 14px;font-size:12px;cursor:pointer;letter-spacing:.5px;
  }
  .theme-btn:hover{border-color:var(--accent)}
  section{margin-top:36px}
  .sec-head{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}
  .sec-head h2{
    font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
    font-size:22px;margin:0;font-weight:700;
  }
  .sec-head .line{flex:1;height:1px;background:var(--rule);align-self:center}
  .lede{color:var(--muted);font-size:15px;margin:0 0 16px;max-width:62ch}
  .card{
    background:var(--card);border:1px solid var(--rule);border-radius:12px;
    box-shadow:var(--shadow);padding:20px 22px;margin-bottom:14px;
  }
  .card h3{margin:0 0 8px;font-size:16px}
  .card p{margin:8px 0;font-size:14.5px;color:var(--muted)}
  .card p strong{color:var(--ink)}
  .card ul{margin:8px 0;padding-left:20px;font-size:14.5px;color:var(--muted)}
  .card li{margin:4px 0}
  .card a{color:var(--accent);font-weight:600}
  .flag{
    display:inline-block;background:var(--accent);color:#fff;
    font-size:10.5px;letter-spacing:1.5px;padding:2px 9px;border-radius:999px;
    vertical-align:2px;margin-right:8px;text-transform:uppercase;
  }
  :root[data-theme="dark"] .flag{color:#1a1206}
  @media (prefers-color-scheme:dark){ :root[data-theme="auto"] .flag{color:#1a1206} }
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  @media (max-width:640px){.grid2{grid-template-columns:1fr}}
  table{width:100%;border-collapse:collapse;font-size:14px;margin:10px 0}
  th{text-align:left;padding:8px 10px;border-bottom:2px solid var(--rule-strong);color:var(--ink)}
  td{padding:8px 10px;border-bottom:1px solid var(--rule);color:var(--muted);vertical-align:top}
  td:first-child{color:var(--ink);font-weight:600;white-space:nowrap}
  footer{margin-top:48px;border-top:3px double var(--rule-strong);padding-top:16px;
    display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
    font-size:13px;color:var(--muted)}
  footer a{color:var(--accent);font-weight:600;text-decoration:none}
  footer a:hover{text-decoration:underline}
  .back{display:inline-block;margin-top:8px;font-size:14px;color:var(--accent);font-weight:600;text-decoration:none}
  .back:hover{text-decoration:underline}"""

JS = """(function(){
  "use strict";
  var root = document.documentElement, btn = document.getElementById("themeBtn");
  function currentTheme(){
    var t = root.getAttribute("data-theme");
    if(t === "light" || t === "dark") return t;
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }
  function paint(){ btn.textContent = currentTheme() === "dark" ? "\\u2600 Theme" : "\\u25D0 Theme"; }
  btn.addEventListener("click", function(){
    root.setAttribute("data-theme", currentTheme() === "dark" ? "light" : "dark");
    try{ localStorage.setItem("bb-theme", root.getAttribute("data-theme")); }catch(e){}
    paint();
  });
  try{
    var saved = localStorage.getItem("bb-theme");
    if(saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  }catch(e){}
  paint();
})();"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Briefing Buddy</title>
<style>
{css}
</style>
</head>
<body>
<div class="wrap">
  <header class="masthead">
    <p class="kicker"><a href="index.html">&larr; Briefing Buddy</a> &middot; Section {num} of 8</p>
    <h1>{h1}</h1>
    <p class="tagline">{tagline}</p>
    <div class="dateline">
      <span>{dateline}</span>
      <button class="theme-btn" id="themeBtn" title="Toggle light / dark">&#x25D0; Theme</button>
    </div>
  </header>
  <main>
{body}
  </main>
  <footer>
    <span><a href="index.html">&larr; Back to Briefing Buddy</a></span>
    <span>Briefing Buddy &middot; a living page</span>
  </footer>
</div>
<script>
{js}
</script>
</body>
</html>
"""

PAGES = [
# ---------------------------------------------------------------- 1. attention
dict(
    slug="attention", num="1", title="Needs your attention",
    h1="Needs your attention",
    tagline="Open items that need Dave's call — decide, delegate, or ask for more.",
    dateline="Briefing Buddy &middot; attention queue",
    body="""    <section>
      <p class="lede">This is the front page of the Briefing Buddy homepage for a reason: everything here is waiting on Dave. Each card is a decision, a review, or a loose end. Tap <strong>&#10003; Done</strong> when it's settled, or <strong>Need more info</strong> and the buddy follows up.</p>
      <div class="sec-head"><h2>How it works</h2><span class="line"></span></div>
      <div class="card">
        <h3>Two buttons, no inbox</h3>
        <p>Every attention card carries <strong>&#10003; Done</strong> and <strong>Need more info</strong>. Tapping either writes a timestamped entry to <code>docs/ingest.md</code> in the buddy's private repo (<a href="https://github.com/davedellaquila/briefing-buddy">davedellaquila/briefing-buddy</a>) via the GitHub API — the same write path as the brain-dump box. Marking something done tells the buddy to clear it from the list; asking for more info asks the buddy to follow up with Dave.</p>
        <p>Done state persists on the device (localStorage), so a card you cleared stays cleared when you come back.</p>
      </div>
      <div class="sec-head"><h2>The current queue</h2><span class="line"></span></div>
      <div class="card">
        <h3><span class="flag">Open</span>Full PRD — not started yet</h3>
        <p>Dave asked for a full PRD after the brief. The brief already queues the spec: user stories per feature, the sections library, per-briefing content mixing, scheduling &amp; send-time rules, the delivery contract with the assistant, and success criteria. One word from Dave and it's drafted.</p>
      </div>
      <div class="card">
        <h3><span class="flag">Resolved</span>The News &#8646; Briefing split is live</h3>
        <p>Settled Oct 11: <strong>Briefing Buddy</strong> assembles and delivers the morning/evening briefings; <strong>News Buddy</strong> is the separate news-sources expert with its own thread and brief. Both have live briefs and private repos.</p>
      </div>
      <div class="card">
        <h3><span class="flag">Open</span>Brief review still pending</h3>
        <p>The <a href="https://docs.google.com/document/d/1s9ghZ-kyp9dag2whTPnk24ULLUJP3JW_0UGtocAynbs/edit">Briefing Buddy brief</a> went up for review Oct 11 — looks good, edits, or hold? The open questions inside (exact section lists, 6 AM / 6 PM still right, who else gets briefings, settings &rarr; job write-back) are what the PRD will settle.</p>
      </div>
      <div class="card">
        <h3><span class="flag">Open</span>Two briefing rules set Oct 11</h3>
        <p><strong>Morning north star:</strong> Dave finishes it in about 10 minutes — digestibility is the design rule. <strong>Evening sports:</strong> 49ers' next-opponent scouting is a standing section — the evening cron definition hasn't been updated to include it yet, so lineups ship without it for now.</p>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 2. editions
dict(
    slug="editions", num="2", title="Today's editions",
    h1="Today&rsquo;s editions",
    tagline="Two editions a day, built by the assistant, delivered to the thread and inbox.",
    dateline="Briefing Buddy &middot; morning 6:00 AM PT &middot; evening 6:00 PM PT",
    body="""    <section>
      <p class="lede">The service the product grows out of. Every day the assistant assembles two briefings from the configured sections plus live data, and delivers each to the Briefings thread — plus a styled HTML email.</p>
      <div class="sec-head"><h2>The Morning Edition</h2><span class="line"></span></div>
      <div class="card">
        <h3>Daily &middot; 6:00 AM PT &middot; 13 sections</h3>
        <p><strong>North-star rule (set Oct 11):</strong> Dave finishes it in about 10 minutes. Digestibility is the design rule — everything in the morning lineup earns its place against that clock.</p>
        <ul>
          <li><strong>High-priority reminders</strong> — from the assistant's registry, leads every briefing</li>
          <li><strong>Calendar</strong> — today's agenda, from Google Calendar</li>
          <li><strong>Weather</strong> — Fiddletown + San Jose conditions, highs and lows</li>
          <li><strong>Sky</strong> — sunrise, moon phase, illumination</li>
          <li><strong>Fire &amp; air</strong> — red-flag warnings, burn-day status, AQI</li>
          <li><strong>Commute</strong> — drive time, only on travel mornings</li>
          <li><strong>Inbox</strong> — what needs action in the last 24 hours</li>
          <li><strong>Markets &amp; tech</strong> — morning headlines, AAPL always included</li>
          <li><strong>Events radar</strong> — live music, motorsport, local happenings</li>
          <li><strong>Prep</strong> — one thing today that needs advance work</li>
          <li><strong>Bills</strong> — overdue + due in 7 days, from the tracker</li>
          <li><strong>Awaiting your reply</strong> — open questions, one line each</li>
          <li><strong>Quick links</strong> — working docs, grouped</li>
        </ul>
        <p>Charts: 60-day Fiddletown sunrise + 7-day weather trend. Audio: the latest briefing MP3, when one exists.</p>
      </div>
      <div class="sec-head"><h2>The Evening Edition</h2><span class="line"></span></div>
      <div class="card">
        <h3>Daily &middot; 6:00 PM PT &middot; 11 sections</h3>
        <p>The wind-down: what happened today, what's on tonight, and the standing dinner question.</p>
        <ul>
          <li><strong>High-priority reminders</strong> — anything still open from the day</li>
          <li><strong>Top stories</strong> — 4&ndash;6 US &amp; world headlines, key fact each</li>
          <li><strong>Markets</strong> — how the day closed: indexes, yields, oil, AAPL</li>
          <li><strong>Tech &amp; AI</strong> — 2&ndash;3 headlines in Dave's lanes</li>
          <li><strong>YouTube picks</strong> — 3&ndash;5 videos, links verified</li>
          <li><strong>Podcast picks</strong> — 2&ndash;3 episodes for the drive</li>
          <li><strong>Sky</strong> — sunset, moon phase</li>
          <li><strong>Night sky</strong> — what's up tonight over Fiddletown</li>
          <li><strong>Awaiting your reply</strong> — open questions, one line each</li>
          <li><strong>Quick links</strong> — working docs, grouped</li>
          <li><strong>The dinner question</strong> — &ldquo;What did you have for lunch and dinner today?&rdquo;</li>
        </ul>
        <p>Charts: market snapshot (Dow / S&amp;P 500 / Nasdaq / AAPL) + 60-day Fiddletown sunset.</p>
      </div>
      <div class="sec-head"><h2>Delivery</h2><span class="line"></span></div>
      <div class="card">
        <p>Both editions land in the <strong>Briefings thread</strong> and go out as <strong>styled HTML email</strong> to dave@dellaquila.com. Morning cron: <code>morning-briefing</code> at 6:00 AM PT. Evening cron: <code>evening-news-briefing</code> at 6:00 PM PT.</p>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 3. live-data
dict(
    slug="live-data", num="3", title="Live briefing data",
    h1="Live briefing data",
    tagline="What the briefings actually carry right now — the snapshot behind the settings.",
    dateline="Briefing Buddy &middot; snapshot refreshes 5:41 AM &amp; PM PT",
    body="""    <section>
      <p class="lede">This is the data the briefings are built from. The homepage snapshot refreshes twice daily — 5:41 AM and 5:41 PM PT, just ahead of each edition — so what you see here is what the next briefing will carry. For the current values, check the homepage tiles.</p>
      <div class="sec-head"><h2>What's in the snapshot</h2><span class="line"></span></div>
      <div class="grid2">
        <div class="card"><h3>Weather &mdash; Fiddletown</h3><p>Current conditions plus today's high/low and tomorrow's outlook. The warm-up watch lives here.</p></div>
        <div class="card"><h3>Sky</h3><p>Sunrise/sunset times, moon phase and illumination. New-moon and full-moon markers included.</p></div>
        <div class="card"><h3>Fire &amp; air</h3><p>NWS alerts (red-flag warnings, etc.) and the current AQI. All-clear reads as good news, not an empty slot.</p></div>
        <div class="card"><h3>AAPL</h3><p>Last close, day change, and the intraday story — Dave's bellwether, always in the briefing.</p></div>
        <div class="card"><h3>Awaiting your reply</h3><p>Open-question count with the high-priority items named. The registry behind the briefings thread.</p></div>
        <div class="card"><h3>Next edition</h3><p>Which briefing ships next, when, and its full section lineup.</p></div>
      </div>
      <div class="sec-head"><h2>Data sources</h2><span class="line"></span></div>
      <div class="card">
        <table>
          <tr><th>Feed</th><th>Source</th></tr>
          <tr><td>Weather</td><td>Open-Meteo &mdash; Fiddletown + San Jose</td></tr>
          <tr><td>Sunrise / sunset</td><td>NOAA solar equation (60-day trends charted)</td></tr>
          <tr><td>Markets</td><td>Yahoo Finance &mdash; Dow, S&amp;P 500, Nasdaq, AAPL</td></tr>
          <tr><td>Alerts</td><td>National Weather Service</td></tr>
          <tr><td>Air quality</td><td>AQI feed, Fiddletown</td></tr>
          <tr><td>Calendar</td><td>Google Calendar</td></tr>
          <tr><td>Inbox</td><td>Gmail &mdash; last 24 hours</td></tr>
          <tr><td>Bills</td><td>The expense tracker</td></tr>
        </table>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 4. designer
dict(
    slug="designer", num="4", title="The briefing designer",
    h1="The briefing designer",
    tagline="The seed of the app — design the briefings, preview the lineup.",
    dateline="Briefing Buddy &middot; the settings surface",
    body="""    <section>
      <p class="lede">This is where Briefing Buddy stops being a service and starts being a product. The designer is the seed of the app: decide how many briefings go out each day, when each lands, and what goes in it — then see the lineup update live.</p>
      <div class="sec-head"><h2>How it works</h2><span class="line"></span></div>
      <div class="card">
        <ul>
          <li><strong>Stepper</strong> &mdash; choose 1 to 4 briefings per day.</li>
          <li><strong>Send-time pickers</strong> &mdash; each edition gets its own time.</li>
          <li><strong>Section checkboxes</strong> &mdash; mix and match from the 20-section library, per edition.</li>
          <li><strong>Live preview</strong> &mdash; the lineup panel updates as you click, sorted by send time.</li>
          <li><strong>Reset</strong> &mdash; one tap restores the current two-edition setup.</li>
        </ul>
      </div>
      <div class="sec-head"><h2>The current setup</h2><span class="line"></span></div>
      <div class="card">
        <p><strong>Morning edition</strong> &mdash; 6:00 AM PT, 13 sections (reminders through quick links). <strong>Evening edition</strong> &mdash; 6:00 PM PT, 11 sections (reminders through the dinner question). This is what the assistant actually delivers today.</p>
      </div>
      <div class="sec-head"><h2>The open question</h2><span class="line"></span></div>
      <div class="card">
        <h3>Settings &rarr; schedule</h3>
        <p>How does a design in the app become the assistant's schedule &mdash; writing back to the jobs safely? That's the product question the PRD has to settle: the designer is the UI, but the write-back path (validation, permissions, rollback) is the real feature. See <a href="on-my-mind.html">On my mind</a>.</p>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 5. library
dict(
    slug="library", num="5", title="Sections library",
    h1="Sections library",
    tagline="Every building block a briefing can be made of — twenty sections, mix and match.",
    dateline="Briefing Buddy &middot; the parts catalog",
    body="""    <section>
      <p class="lede">The full catalog. Check boxes in the designer to build an edition out of these; the two live editions are just two particular mixes. Sections marked <strong>M</strong> ship in the morning, <strong>E</strong> in the evening.</p>
      <div class="sec-head"><h2>Lead &amp; logistics</h2><span class="line"></span></div>
      <div class="card"><ul>
        <li><strong>High-priority reminders</strong> <strong>M E</strong> &mdash; from the assistant's registry; leads every briefing.</li>
        <li><strong>Calendar</strong> <strong>M</strong> &mdash; today's agenda, from Google Calendar.</li>
        <li><strong>Prep</strong> <strong>M</strong> &mdash; one thing today that needs advance work.</li>
        <li><strong>Bills</strong> <strong>M</strong> &mdash; overdue + due in 7 days, from the tracker.</li>
        <li><strong>Commute</strong> <strong>M</strong> &mdash; drive time; only on travel mornings.</li>
      </ul></div>
      <div class="sec-head"><h2>World &amp; markets</h2><span class="line"></span></div>
      <div class="card"><ul>
        <li><strong>Top stories</strong> <strong>E</strong> &mdash; 4&ndash;6 US &amp; world headlines, key fact each.</li>
        <li><strong>Markets</strong> <strong>E</strong> &mdash; how the day closed: indexes, yields, oil, AAPL.</li>
        <li><strong>Markets &amp; tech</strong> <strong>M</strong> &mdash; morning headlines; AAPL always included.</li>
        <li><strong>Tech &amp; AI</strong> <strong>E</strong> &mdash; 2&ndash;3 headlines in Dave's lanes.</li>
      </ul></div>
      <div class="sec-head"><h2>Atmosphere</h2><span class="line"></span></div>
      <div class="card"><ul>
        <li><strong>Weather</strong> <strong>M</strong> &mdash; Fiddletown + San Jose conditions, highs and lows.</li>
        <li><strong>Sky</strong> <strong>M E</strong> &mdash; sunrise/sunset, moon phase, illumination.</li>
        <li><strong>Night sky</strong> <strong>E</strong> &mdash; what's up tonight over Fiddletown.</li>
        <li><strong>Fire &amp; air</strong> <strong>M</strong> &mdash; red-flag warnings, burn-day status, AQI.</li>
      </ul></div>
      <div class="sec-head"><h2>Discovery</h2><span class="line"></span></div>
      <div class="card"><ul>
        <li><strong>Events radar</strong> <strong>M</strong> &mdash; live music, motorsport, local happenings.</li>
        <li><strong>YouTube picks</strong> <strong>E</strong> &mdash; 3&ndash;5 videos, links verified.</li>
        <li><strong>Podcast picks</strong> <strong>E</strong> &mdash; 2&ndash;3 episodes for the drive.</li>
        <li><strong>Sports</strong> &mdash; 49ers' next-opponent scouting; standing evening section (cron update pending).</li>
      </ul></div>
      <div class="sec-head"><h2>Meta</h2><span class="line"></span></div>
      <div class="card"><ul>
        <li><strong>Inbox</strong> <strong>M</strong> &mdash; what needs action in the last 24 hours.</li>
        <li><strong>Awaiting your reply</strong> <strong>M E</strong> &mdash; open questions, one line each.</li>
        <li><strong>Quick links</strong> <strong>M E</strong> &mdash; working docs, grouped.</li>
        <li><strong>The dinner question</strong> <strong>E</strong> &mdash; &ldquo;What did you have for lunch and dinner today?&rdquo;</li>
      </ul></div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 6. topics
dict(
    slug="topics", num="6", title="Topics I watch",
    h1="Topics I watch",
    tagline="The personalization axis — every story is ranked against these.",
    dateline="Briefing Buddy &middot; Dave's lanes",
    body="""    <section>
      <p class="lede">Briefings aren't generic news — they're filtered through what Dave actually cares about. These seven topics are the ranking axis: every candidate story scores against them, and the top scorers make the editions.</p>
      <div class="grid2">
        <div class="card"><h3>&#129302; AI &amp; technology</h3><p>The home lane. Model releases, agent frameworks, Apple intelligence moves, and the infrastructure underneath it all.</p></div>
        <div class="card"><h3>&#128200; Markets &amp; investing</h3><p>Indexes, yields, oil — and AAPL, always. The macro picture with Dave's positions in mind.</p></div>
        <div class="card"><h3>&#9999;&#65039; Product design</h3><p>Interface craft, design systems, the Jony Ive school. What great products feel like, and why.</p></div>
        <div class="card"><h3>&#9881;&#65039; Engineering</h3><p>Systems, tooling, the craft of building. From prototype auto-fetch to homelab infrastructure.</p></div>
        <div class="card"><h3>&#127950; Motorsport</h3><p>F1, endurance racing, the classics in the garage. Sreten's restorations count as motorsport-adjacent.</p></div>
        <div class="card"><h3>&#127926; Live music</h3><p>Shows worth driving for, new releases from the artists that matter, the Amador County scene.</p></div>
        <div class="card"><h3>&#127794; Amador County local</h3><p>Fiddletown and the county: civic news, fire season, neighbors, the stuff that affects home.</p></div>
      </div>
      <div class="sec-head"><h2>How ranking works</h2><span class="line"></span></div>
      <div class="card">
        <p>News Buddy evaluates sources; Briefing Buddy assembles. When the evening edition picks its 4&ndash;6 top stories and 2&ndash;3 tech headlines, these topics are the weights. A story that hits two lanes outranks one that hits none — that's the whole personalization model, and it's why the briefings read like they were edited for one person.</p>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 7. on-my-mind
dict(
    slug="on-my-mind", num="7", title="On my mind",
    h1="On my mind",
    tagline="Open questions from the brief — the ones the PRD will have to settle.",
    dateline="Briefing Buddy &middot; product questions",
    body="""    <section>
      <p class="lede">The product isn't finished being decided. These are the open questions carried over from the brief — each one blocks a piece of the PRD, and each one is Dave's call.</p>
      <div class="card">
        <h3>Exact final section lists</h3>
        <p>What's confirmed vs still fluid? Two rulings already feed this: the morning's 10-minute north-star rule and the evening's new standing sports section (49ers' next-opponent scouting). The library holds 20 sections; the lineups use 13 + 11. Which of the rest earn a slot — and does anything get cut?</p>
      </div>
      <div class="card">
        <h3>Are 6:00 AM / 6:00 PM still the right times?</h3>
        <p>The current daily cadence. Morning at 6:00 AM PT catches Dave before the day starts; evening at 6:00 PM PT lands at wind-down. But cadence is a product decision — should the designer offer different defaults, or is two-a-day the product?</p>
      </div>
      <div class="card">
        <h3>Who else gets briefings?</h3>
        <p>Family, or anyone else? The delivery contract today is one recipient (Dave, thread + email). Multi-recipient briefings change the product: per-person sections, per-person topics, per-person send times. Worth deciding before the PRD, not after.</p>
      </div>
      <div class="card">
        <h3>Settings &rarr; schedule: the write-back path</h3>
        <p>How does a design in the app become the assistant's schedule &mdash; writing back to the jobs safely? The designer is the easy half; the write-back (validation, permissions, rollback, what happens when a cron fails) is the real feature. See also <a href="designer.html">The briefing designer</a>.</p>
      </div>
      <div class="sec-head"><h2>Where these live</h2><span class="line"></span></div>
      <div class="card">
        <p>These questions originated in the <a href="https://docs.google.com/document/d/1s9ghZ-kyp9dag2whTPnk24ULLUJP3JW_0UGtocAynbs/edit">Briefing Buddy brief</a> (review pending). When Dave answers them, they move to the attention queue as resolved &mdash; and the PRD gets written.</p>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
# ---------------------------------------------------------------- 8. brain-dump
dict(
    slug="brain-dump", num="8", title="Brain dump",
    h1="Brain dump",
    tagline="Raw and unfiltered — dump what's on your mind about Briefing Buddy.",
    dateline="Briefing Buddy &middot; the inbox that never sleeps",
    body="""    <section>
      <p class="lede">The fastest way to get an idea out of your head and into the buddy's memory. Type it, hit Dump it (or Cmd/Ctrl+Enter), and it's timestamped into the repo — no formatting, no friction.</p>
      <div class="sec-head"><h2>How it works</h2><span class="line"></span></div>
      <div class="card">
        <ul>
          <li><strong>Write anything</strong> &mdash; a feature idea, a complaint, a question for later, a half-thought.</li>
          <li><strong>Hit Dump it</strong> &mdash; or press Cmd/Ctrl+Enter from the textarea.</li>
          <li><strong>It lands in the repo</strong> &mdash; appended as a timestamped entry to <code>docs/ingest.md</code> in <a href="https://github.com/davedellaquila/briefing-buddy">davedellaquila/briefing-buddy</a>, via the GitHub API.</li>
          <li><strong>The buddy triages it</strong> &mdash; dumps are the inbox the buddy works from; anything actionable becomes an attention item or a task.</li>
        </ul>
      </div>
      <div class="sec-head"><h2>Setup</h2><span class="line"></span></div>
      <div class="card">
        <h3>One-time GitHub token</h3>
        <p>The dump box needs a GitHub token (repo scope) to write to the repo. Paste it once in the box on the homepage &mdash; it's stored in the browser's localStorage on that device only, never sent anywhere except the GitHub API. <a href="https://github.com/settings/tokens">Get a token</a>.</p>
        <p>The token is shared across all buddy homepages on the device (the <code>buddyTree.v3</code> key), so one paste unlocks every dump box and attention action.</p>
      </div>
      <div class="sec-head"><h2>House rule</h2><span class="line"></span></div>
      <div class="card">
        <p>Brain dumps are <strong>write-only from the page</strong> &mdash; you can't edit or delete them from here. They're a log, not a document. If a dump needs retracting, that's a repo edit, and the buddy can do it on request.</p>
      </div>
      <a class="back" href="index.html">&larr; Back to the homepage</a>
    </section>""",
),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    for p in PAGES:
        html = TEMPLATE.format(
            title=p["title"], css=CSS, js=JS,
            num=p["num"], h1=p["h1"], tagline=p["tagline"],
            dateline=p["dateline"], body=p["body"],
        )
        path = os.path.join(OUT, p["slug"] + ".html")
        with open(path, "w") as f:
            f.write(html)
        print(f"wrote {path} ({len(html)} bytes)")

if __name__ == "__main__":
    main()

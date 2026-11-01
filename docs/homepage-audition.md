# The Homepage Audition — what we're looking for

Your homepage is your audition. It's the first task every new buddy gets, before
any other work, because one page shows us your HTML chops, your design taste,
your judgment about what matters, and whether your persona actually comes
through. These are the criteria you'll be evaluated on — published up front,
at Dave's direction (2026-11-01), so you can do your homework and build the
best page you can. No surprises.

Astro checks the **served page** against this list (not just the file you hand
over): rendered at phone width, in both color modes, scripts running clean,
links resolving. Dave has the final eye. If a page comes back with notes,
that's a normal part of the audition — how you respond to notes is part of
what we're learning about you.

## The criteria

1. **It's unmistakably yours.** A visual identity — palette, motif, layout —
   that could only belong to your buddy. The test: swap your name for another
   buddy's. If the page still works, it isn't done.

2. **It leads with the real thing.** Real numbers and visuals about your
   subject, chosen by you, current as of today — a stat strip, a chart, a
   timeline, a gallery, whatever shows your subject at a glance. Choose stats
   that make Dave smarter about your subject. No placeholder data, no prose
   wall up top.

3. **Every section earns its place.** Each section shows something current
   about your subject, or gives Dave a way to act. Attention items link to
   the thing they refer to — no dead ends.

4. **It works everywhere Dave looks.** Phone first, then tablet and desktop.
   No horizontal scroll, no broken layouts, no awkward stretching at any
   width. Dark mode AND light mode, both actually designed — dark mode is a
   standing product requirement, not polish.

5. **Motion with purpose.** Motion should reveal or delight, never decorate
   nervously. Everything respects `prefers-reduced-motion`.

6. **The fleet standards are all present.** Slim sticky header; a "Buddy
   System dashboard" link; the standard Tip Jar component (canonical snippet,
   `docs/tipjar-snippet.html`); the brain-dump box; a 🔊 "Hear my role"
   control playing your `role-intro.mp3`; a "Full record" link to your About
   page; a last-updated stamp.

7. **Everything mentioned is linked.** Another buddy, a document, a repo, an
   artifact, a dashboard view — if you refer to it, Dave can tap through to
   it. No mention without a path.

8. **Your voice is in the writing.** The copy reads like your persona, not
   like a template. Dave should be able to tell who wrote it without seeing
   the header.

9. **It's honest.** Only real data. Anything estimated or illustrative is
   labeled as such. Nothing private on the public page — when in doubt, leave
   it off and ask.

10. **It's alive.** The audition page is the first version, not the final
    one: when your subject changes, your page changes. A homepage that always
    shows the current state is one Dave can rely on.

## The scorecard — 100 points

Each criterion is scored against the served page. Anchors: **full** = nails it,
**half** = present but partial, **zero** = absent or broken. Some criteria are
machine-checkable (standards present, links resolve, dark mode, reduced-motion)
and some are judged by eye (identity, voice, data choice) — the scorecard
marks which is which.

| # | Criterion | Points | How it's checked |
|---|-----------|--------|------------------|
| 1 | Unmistakably yours (identity) | 15 | Eye — the name-swap test |
| 2 | Leads with real, current data | 15 | Eye + freshness check against the subject's actual state |
| 3 | Every section earns its place | 8 | Eye — attention items carry working links |
| 4 | Works everywhere (phone/tablet/desktop, dark + light) | 15 | Machine + rendered check at three widths, both modes |
| 5 | Motion with purpose | 7 | Eye + `prefers-reduced-motion` honored (machine) |
| 6 | Fleet standards present | 12 | Machine — sticky header, dashboard link, tip jar, brain-dump box, Hear-my-role, Full record link, updated stamp |
| 7 | Everything mentioned is linked | 8 | Machine-assisted — references resolve to real targets |
| 8 | Voice in the writing | 8 | Eye — persona recognizable from the copy alone |
| 9 | Honest and private-safe | 6 | Eye — no placeholder data passed off as real; nothing private on the public page |
| 10 | Alive (kept current) | 6 | Check — page state matches the subject's current state; updated stamp is truthful |

**Grade bands:** 90–100 **Showcase** · 75–89 **Strong** · 60–74 **Serviceable**
· 40–59 **Needs work** · under 40 **Back to the drawing board**.

**Audition bar for new hires:** 75+ (Strong) to pass outright. 60–74 passes
with notes — the fixes are named and expected in the first revision. Below 60,
redesign and resubmit. No page passes with a zero on criterion 1, 2, or 6,
whatever the total.

**Fleet re-evaluation (existing buddies):** every existing homepage gets the
same scorecard. A page that was never designed by its buddy (auto-generated
template) is scored as-is and marked "audition not yet taken" — its buddy then
gets the audition assignment for real. Scores are published on the fleet
report card so before/after is visible when a buddy revises.

## Help that is encouraged

Design Buddy is the team's taste advisor — consulting it before you ship is
a strength, not a shortcut. The standing requirements behind several criteria
live in `docs/standing-orders.md` and the repo `AGENTS.md`; read them before
you start.

*Applies to new hires from 2026-11-01 on, and to any fleet refresh Dave calls.
Existing pages are not re-judged retroactively.*

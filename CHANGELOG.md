## 2026-10-28

- **Phone: the collapsed panel is the desktop's six-icon rail now (build 20261028.1938):** Dave's call in the Briefings thread — on his iPhone the resting buddy panel showed a vertical strip of a dozen or so recent-buddy icons (the phone strip, count set by the "Recent items to remember" setting); he wants the iPhone to match his desktop: the collapsed rail's six controls. At ≤639px the closed dock now presents exactly those six, top to bottom — **› expand, 🕘 Recents (same popover), 🔍 Find, 💼 Business Plans, current-view icon (views popover), ⚙ Settings** — in the same three rail sections the desktop uses (1 + 3 + 2), laid out in the 66px phone dock wearing the strip's own clearances (68px at the top, 96px at the foot so Settings clears the floating bottom cluster; current view + Settings rest at the foot). The strip retires as the resting face: its renderer stays in the tree dormant and its CSS show rule is gone; recent buddies are one tap away in the Recents popover (viewport-fit per build 20261028.1925), favorites via the views popover. The grid-door's job maps to the › expand chevron (opens the full buddy-list dock, unchanged); the strip's current-buddy accent marking has no rail equivalent and is dropped with the strip — the selected buddy still restores on load and deep links land as before. Changes are CSS-only in build.py: the rail's blanket phone-width hide now applies only while the dock is open or in standalone, and the phone block shows the rail sections in the closed dock (flex column). Desktop behavior untouched at every width and state. Verified: verify-build.sh clean (all inline scripts `node --check` OK) and an 18-point cascade check over the built stylesheet (phone closed → strip none + rail flex ×3 + sidebar flex; phone open → all none; desktop collapsed/expanded unchanged; six controls homed 1+3+2 in the rail sections) — all passed. jsdom's getComputedStyle does not evaluate @media in this environment, so the cascade was resolved directly from the built CSS; live look is Dave's phone.
- **Dashboard — journal Revert now asks first; two renames restored (build 20261028.1934):** Dave accidentally tapped the change journal bar's **Revert (N)** and it instantly undid every logged change and cleared the journal. **(1) Revert is gated.** The button now opens a confirmation dialog listing exactly what will be undone (each change with its old → new values and time) under a plain warning — "This undoes all of the changes below and clears the change journal. It can't be undone." — with **Cancel** (default focus; Escape and backdrop tap also cancel, journal untouched) and a red **Revert N changes** button as the only path through. **(2) The accidental revert's damage, recovered where the record reaches.** Its write-through commit (58dcc27) shows exactly two renames were undone: **wwsf "WWSF/STIX" → "WWSF"** and **dave-swiger-buddy "Dave Swager" → "Dave Swiger"** (both corrections Dave had made earlier; his own Recent-menu screenshot minutes before shows the pre-revert names). Both are restored in the registry (commit ea105f4). Journal entries of other types (notes, moves, brand) live only in the device's local state and leave no server trace — if any were in that journal, they're not recoverable from here; Dave's call on whether any were. verify-build.sh clean; all inline scripts `node --check` OK.
- **Dashboard — Recents moves into the buddy panel; its menu can no longer run off the bottom (build 20261028.1925):** Two of Dave's calls, plus one gap found while verifying. **(1) The standalone Recents floater is retired; Recents lives in the panel now.** The floating clock button — footer slot right of Back in grouped mode, pinned top-left corner otherwise — is removed, and Recents takes a seat in the expanded panel's header tools, **directly left of the ⚙ gear** (new `#sb-recents`, standard tool-button styling; hidden while collapsed, like the gear). The rail keeps its own Recents at 2nd position (build 20261028.1850). One popover, two panel anchors; outside-click dismissal and the default anchor moved to the panel buttons. The footer-grouping Settings toggle now groups three buttons (New, Back, Info) and its tip says so. **(2) The Recent menu fits the visible viewport.** It capped at `60vh` and flipped above its button on overflow, but in app webviews the CSS `vh` runs taller than the visible area, so a long menu still bladed off the bottom (Dave's screenshot: ~19 rows, last ones unreachable). `toggleRecentsPop` now computes the cap and position in px from `visualViewport`/`innerHeight`, flips above the anchor on overflow, and finishes with a clamp guaranteeing top ≥ 8 and bottom ≤ visible height − 8, scrolling internally past the cap; the fit re-runs when "Show more" grows the list, and a horizontal clamp joins it. **(3) Found while verifying: Prev/Next visits never reached Recents.** Recording lived only in `selectBuddy`, but Prev/Next steps navigate via `show()`, which never recorded — buddies visited by stepping were missing from the menu. Recording is now one `recordRecent()` helper called from both, with `show()` recording on an actual selection change (boot restore doesn't churn the list). verify-build.sh clean; all inline scripts `node --check` OK.
- **Dashboard — rail Recents moves to 2nd position (build 20261028.1850):** From Dave's screenshot of the six-icon rail: the 🕘 Recents icon leaves the rail's bottom slot and becomes the **second control, directly below the › expand chevron** (first item of `#rail-mid`). New rail order: › expand, 🕘 Recents, 🔍 Find, 💼 Business Plans, current-view, ⚙ Settings. One markup move — every behavior is id-based and unchanged (same popover, rail-anchored beside the button; at the top of the rail it now opens below-right instead of flipping up). Supersedes the directly-above-Settings placement from build 20261028.1758, an hour earlier. verify-build.sh clean; all inline scripts `node --check` OK.
- **Dashboard — Recents joins the collapsed rail (build 20261028.1758):** Dave's call: the recent list should also be reachable from the collapsed buddy panel, with its icon right next to Settings. The rail gains **🕘 Recents** (`#rail-recents`) in `#rail-bottom`, directly above the ⚙ Settings gear — the rail is now six controls: › expand, 🔍 Find, 💼 Business Plans, current-view, 🕘 Recents, ⚙ Settings. It opens the **same** recent-buddies popover as the corner/footer Recents button (`toggleRecentsPop` now takes its anchor; the rail anchor opens the pop beside the rail, flipping up on overflow like the others), with the same paging ("Show more", recentsCount), the same row behavior (tap → open that buddy), and outside-click dismissal that exempts both Recents buttons. The pinned corner Recents and the footer-grouping mode are untouched — this is an additional entry point in the rail, not a move of the existing one. verify-build.sh clean; all inline scripts `node --check` OK.
- **Social Media Buddy — 👀 Worth your attention, evening edition (Wed 2026-10-28):** Facebook is Top 4, all from today and no padding (newsfeed + friends feed, two pages each, 18 posts) — brother Ron Dell'Aquila's get-out-the-vote share (2:21 PM) leads as the only family post in the pages read, ahead of Carol Joe Winstead's "13 years later" look back (4:57 PM, newest in either feed), Dell'Aquila Garage's mahogany-cockpit MGB restomod post and Spencer Kesner's small 4x4 spot. Instagram is Top 3 — Ken Okuyama's Italy Innovation Days dialogue with Enzo Mattioli Ferrari (design, heritage, AI) leads, with Cars Without Limits' LaFerrari startup reel and HardTuned's colour-matched Supra behind it (a Sneako/Akademiks rumour excluded). Threads is Top 1, a thin read honestly labelled — the same LaFerrari clip cross-posted is the only on-interest item of 4 (two NBC News items and a Don Lemon promo excluded). Reddit refreshed fresh via the browser (5:42–5:49 PM, all eight subs, no bot block): r/ClaudeAI's AGI preview climbs to 15K, r/apple's 404 page to 6.3K and the TV-safeguards follow-up to 4.1K, r/Porsche gets a new leader (911 GT3 RS in NYC, 2.8K) and r/classiccars changes hands ('64 Lincoln Continental, 1.1K). X is fresh and all-new — Gurman's "outside commentator" post (~1h old) leads, ahead of his Power On podcast post, @gregjoz's PROLED XDR MacBook launch post, Gurman's Jan-2023 victory lap and @claudeai's Claude for Legal artifacts gallery; @ClaudeDevs still has nothing newer than Oct 23. LinkedIn note updated to the latest drip-watch figures (787 impressions, 11 reactions, 2 comments). All 18 attention links carry target="_blank".
- **Dashboard — expand mirrors the collapse; Settings joins the rail (build 20261028.1451):** Two more of Dave's calls on the sidebar. **(1) The expand now animates like the collapse, in reverse.** Collapsing glides (width + a settle into the centred rail) — expanding didn't: the Job I open pose (`sb-opening`: opacity 0 + scale .965 under `transition:none`) killed the width glide, so the panel snapped wide and only micro-settled. The pose and its click-point capture machinery are gone. Expanding now measures the rail rect and the expanded rect in a transitions-off pass, parks the expanded panel exactly on the rail's footprint (rail width + a px `translateY` down to the rail's top), then releases — width and transform glide together on the sidebar's own transition, the reverse of the collapse's sink-and-narrow; a 560ms cleanup re-asserts the canonical width in case the glide is interrupted. **(2) Settings is the rail's fifth icon.** The collapsed rail is now, top to bottom: **›** expand, **🔍 Find**, **💼 Business Plans**, the **current-view icon**, and **⚙ Settings** (new `#rail-gear` under the current-view icon in `#rail-bottom`, which now stacks vertically; opens the same Settings sheet as the expanded sidebar's gear / ⌘,). The four-icon layout from build 20261028.1348 is otherwise unchanged. verify-build.sh clean; all inline scripts `node --check` OK.
- **Dashboard — collapse wears a chevron; the collapsed rail is exactly four icons (build 20261028.1348):** Two calls from Dave. **(1) The sidebar's ✕ is now a left chevron.** The left panel never disappears — expanded or collapsed to the rail — so a "close" ✕ said the wrong thing; in full view the button now shows ‹, the collapse direction (its title/aria already read "Collapse sidebar"). The circled ✕ (`circleX`) stays the mark for true dismiss/close controls everywhere else; the info panel's ⓘ/× swap is untouched. **(2) The collapsed rail is exactly four icons**, top to bottom: **›** expand (existing `#rail-expand`), **🔍 Find** (new `#rail-find` — opens the same Find overlay as ⌘F; Dave flagged he may change his mind on this one), **💼 Business Plans** (new `#rail-plans` — opens a menu of the plans in the current plan order, current plan marked; a pick rides the same `show('plan:…')` path as the sidebar list), and the **current-view icon** (existing `#rail-curview` + its views popover). The full Views icon stack no longer renders in the rail (`#views-sec` hidden while collapsed; it lives on in the expanded sidebar), and the popover machinery is shared — one `#rail-viewpop` shell, outside-click/Escape handling extended to the new button. verify-build.sh clean; all inline scripts `node --check` OK.
- **Tip Jar 🫙 — fleet migration to the header (generator-managed pages):** the jar is now a compact bug in each page's header row (the placement Developer Buddy's homepage modelled), and the floating bottom-right pill is retired on every generator-managed page. The canonical snippet (`docs/tipjar-snippet.html`) was rewritten in the header form (breathing + shimmer + hover spin, reduced-motion off); both generators read it live and place it — `gen_basic_homepages.py` puts the anchor in the sticky topbar (right end) on all 71 template homepages, `gen_default_homepages.py` puts it in the About nav bar (or hero header) on all 164 About pages. The 15 default-style index pages still on the older v2 template got a surgical jar swap in place (pill removed, header bug added) rather than a template-generation jump. One extraction bug was caught and fixed mid-run: the snippet's own usage prose mentions `<style>`/`<a>`, which poisoned the first extraction — the generators now strip comments before extracting, verified clean. Remaining: ~81 custom/thread-owned pages and buddy sub-pages still carry the floating pill; they migrate per-page (scoped plan via Astro), never by bulk edit. Verification: pill count on generated pages = 0; header-tip present on all 71 + 164 + 15; buddies.json untouched.
- **School Buddy 🎓 — header repaired:** the fleet dashboard-link injection had landed *inside* the page's 44px icon tile (`<div class="mark">🎓<a …>`), blowing the link text across the header in raw blue and displacing the 🎓. The link now sits in the topbar row beside the name, in the header's muted tone; the 🎓 is solo in its tile again. Also: when the page is embedded in the dashboard, its "← Project Buddy" crumb now clears the pinned Recents floater (68px left padding via an embedded-only class) instead of sliding under it.
- **Dashboard — New Buddy panel: silent create failure fixed + persona picker generics/filter; panel search removed; sidebar × circle un-clipped (build 20261028.1540):** Four items from Dave's morning, one build (Developer Buddy's first queue pass). **(1) New Buddy create could fail silently (Dave hit it setting up Refresh Buddy):** the sheet's write throws instantly when the device has no GitHub token (or GitHub rejects it), and the only feedback was one unstyled line — the `.ab-err` CSS was scoped to the *other* dialog, so in this sheet the message rendered as plain body text at the bottom of the scrolling body — and the request was dropped, unqueued (verified by reproduction on the served copy: no file landed in docs/inbox). Fix, per the token-gated client-writes pattern: the sheet's error line is styled now; a status line lives **in the sticky action bar** (always visible) and names the failure in plain language with the next step ("Couldn't save — there's no GitHub token on this device. Your request is saved on this device and will send automatically once a token is added…"); every failed request **queues on-device** (`S.nbQueue`) and `flushNbQueue()` sends it automatically at boot / when a working token appears, landing the placeholder buddy + a confirmation toast then; success is unmistakable ("✓ Saved — "<name>" request is in the inbox (docs/inbox) and Astro will run the full setup."). The sheet stays open with inputs intact on failure. **(2) Persona picker (Dave's asks):** the sheet's catalog is now 27 `[name, emoji, keywords]` triples — **Generic Male / Generic Female / Gender-Neutral pinned first**, ahead of the 24 specialized personas, each tagged with trait keywords — plus a **keyword filter** above the grid ("try feisty or calm": every typed word must match name or keywords; count shown; friendly empty state). **(3) Panel search removed entirely (Dave, via the Investment Buddy thread: "shouldn't appear there at all"):** `#bp-search` field + wrap, its CSS, `initBpSearch`/`focusPanelSearch`, the mirror-to-sidebar sync, and the `/` routing all unwound — one filter for the whole dashboard (the main-view Find; ⌘F routing untouched, verified in the built page). **(4) Sidebar × circle clipped (Dave's screenshot):** two stacked defects — the sticky brand header bleeds edge-to-edge *under* the .sb-scroll classic scrollbar band (~16px), which painted over the × circle's right arc, and `#sb-resize`'s left formula omitted the floating sidebar's 12px viewport offset, shifting the gripper strip 12px left over the same button (and pushing its dots 12px further inboard than the Oct 28 spec). Fixes: `#sb-tools` right 8px → 24px (band + breathing room; brand text reserve 112 → 128px to match); `#sb-resize` left `sbw − 14px` → `sbw − 2px` in floating mode, with an anchored-mode override keeping `sbw − 14px` (flush left:0). verify-build.sh clean; all inline scripts `node --check` OK.
- **Refresh 💆 — hired and wired (build 20261028.0831):** Dave started this hire himself in the dashboard's New Buddy panel; the panel's create flow failed silently (button reset after a couple of seconds, nothing captured — verified from the repo side: no docs/inbox request landed), so Astro ran the setup drill by hand. Refresh Buddy (child of Amador County 📍, same parent as Crush Pizzeria) keeps the record for Refresh, the massage place Dave and Nan use: locations and hours, services and therapists, the booking log, Dave's and Nan's standing preference records, intake-form status, and book-ahead reminders (it books up ~2 weeks out). Field guide (Google Doc, TITLE + 7 HEADING_1 sections read-back-verified) + private repo (visibility verified) + template homepage with role audio hosted alongside + About page; registry now at 164 buddies. Persona **The Spa Concierge** (alternates The Wellness Host, The Relaxation Guide), voice **Burnished Trophy** (`avocado_v2:atlas`) — both provisional: Decision Buddy casting asked, Dave's audition picks override (voice auditions now presented in the buddy's own thread, per Dave's new rule today). First research job: settle Refresh's location on evidence — Dave says Plymouth; his Oct 27 booking mail says Sutter Creek. Known at hire: phone (209) 267-0887; Nan's massage booked Sat Nov 7, 2026, 1:00–2:30 PM, intake form due. The panel bug (silent create failure) plus Dave's persona-picker asks (generic male/female/gender-neutral pinned as the first three options, keyword filter) went to Developer Buddy as its priority queue items the same morning.
- **Developer Buddy 🧑‍💻 — custom homepage live (build 20261028.0826):** Developer Buddy's first task, its own audition homepage, replaces the template at `developer-buddy/`. Terminal / ship-log identity that could only be this buddy: a code-window hero (`$ whoami --role`, blinking cursor), a Decision → Spec → Build → Verify → Push → Served-copy pipeline strip, and a dark ship log. It leads with live codebase stats (Dave's hire ask): 163 buddies in the registry (163/163 with homepages), 30 commits today / 333 in 7 days / 1,497 all-time, 114 attention items across 93 buddies, 16,074 lines of build tooling (build.py 14,300 · gen_basic 1,329 · gen_default 445, shown as true-proportion anatomy bars), current build + commit. **Tip Jar new placement modelled here first:** the 🫙 jar is a compact bug in the sticky header (Ko-fi), the floating pill is gone from this page — the reference implementation for the fleet migration now at the top of Developer Buddy's queue (167 homepage pills still to migrate). Dark + light, responsive no-horizontal-scroll, Hear-my-role (role-intro.mp3 — the block was added by hand; the template at hire predated the hosted mp3, so the generator hadn't emitted it), brain-dump / attention / repo-files scripts carried over byte-identical from the template (diff-verified), no template markers so the generators leave it alone. All 4 inline scripts `node --check` clean, tag balance clean.
- **Developer Buddy 🧑‍💻 — hired and wired (build 20261028.0821):** Dave's call in the main chat ("are you sure we don't need a developer buddy? 'cause it feels weird talking to you about all the changes now we want to make in the code") — a dedicated code desk so the main chat stays about decisions, not code mechanics. Developer Buddy (child of Project Buddy 🧭) owns the BuddyOS codebase day-to-day: the dashboard build, homepage generators, canonical snippets, and the buddy-server codebase — taking Dave's decisions via Astro and buildable specs from the Designer, and reporting back in outcomes with build numbers. Job req (Google Doc, TITLE + 8 HEADING_1 sections read-back-verified) + private repo (visibility verified) + template homepage with role audio hosted alongside + About page; registry now at 163 buddies. Persona **The Lead Engineer** (alternates The Principal Engineer, The Shipwright), voice **Precise Window** (`avocado_v2:vdc_NOID65`) — provisional: Decision Buddy holds the standing casting duty and Dave's audition pick overrides. Its inherited first build pass (Find palette + Recents floater + inboard grippers) shipped this morning from the Designer thread as build 20261028.0815, so it starts with the Tip Jar header migration at the top of its queue. Dave's extra ask at hire: its homepage leads with live codebase stats of its own choosing, built to the new razzle-dazzle homepage standard added to the hire drill the same morning.
- 📈 **Investment Buddy homepage — Markets trend chart added** (Dave's ask): a big trend chart with tab controls switching between 11 major world indices — US (S&P 500, NASDAQ, Dow, Schwab 1000), Europe (FTSE 100, DAX, CAC 40, Euro Stoxx 50), Asia (Nikkei 225, Hang Seng, Shanghai Composite) — each normalized to % change since Jan 30, 2025. US series from Dave's Schwab alert emails; Europe/Asia from Yahoo Finance market data through Oct 28, 2026. Headline of the window: Nikkei +60.1%, CAC 40 the only decliner (−0.8%). Verified with a headless harness (chart path, readout, tabs, ticker tape intact) before push.
## 2026-10-28
- **Dashboard 🔍 — Find palette: one window-centred card; Recents floater sized + upward; grippers inboard (build 20261028.0815):** Dave's three calls from the Designer thread (Jonny's crit + spec, `find-palette-crit-spec.md` + two addenda; Dave's go-ahead built by Designer). (1) **Find:** bar + results are now static children of a single `#find-card` — one border, radius, blur, shadow — centred on the **window** at `top:max(64px, min(14vh, 120px))`, width `min(640px, 100vw−24px)`, invariant across sidebar open/closed and anchored/floating panel states; the morning's `positionFind()` main-view rect math is removed (the function remains only to clear stale inline styles). The scrim rises above the update banner (z 9500 → 10003, deepened to .42 + 2px blur) so the whole window dims together. Interior: hairline seam between field and list; Recent/Suggestions label re-treated (letterspaced, muted); the keyboard-selected row takes the accent wash, a softened 1.5px inset ring, and a right-aligned ↵ hint; taglines 12→13px; list capped at `min(46vh, 420px)` with a hidden scrollbar; a static hint footer (↑↓ navigate · ↵ open · esc dismiss); empty state centred. Phone keeps the full-width top placement, retargeted to the card. (2) **Recents floater (`body.fw-footer`):** the button now matches Back exactly — 56px, same baseline (`bottom:20px; left:88px`, a 12px gap) — and the menu can no longer open off-screen: `toggleRecentsPop` flips the pop above its button whenever it would run past the window's bottom edge (footer mode: pop's bottom 8px above the button's top; `max-height` capped at `min(60vh, 100vh−124px)`). The pinned top-left placement is unchanged (44px). (3) **Grippers inboard:** the shared panel-gripper dot cluster (`#sb-resize`/`#bp-resize` ::after) shifts 10px inboard, mirrored, so every dot sits inside its panel (3px clear of the border); strips, hit areas, cursors, and drag behaviour untouched, and the phone-drawer strip inherits via the shared rule. Locked chrome (pinned Recents slot, ⓘ/× pixel swap, Prev/Next/Back) untouched. Verified headlessly against the built page — 21/21 state checks (palette centred at 720.0 in a 1440px window with sidebar open and closed, settled width/top 640/120, phone insets 12px, pop-up flip geometry exact, both gripper transforms, card structure bar/menu/footer); verify-build.sh clean. FEATURES.md's Keyboard entry updated to match.
- **Investment Buddy 📈 — custom homepage live:** Dave's approval in the Investment Buddy thread ("Looks good — host it"). The market-terminal custom homepage (dark-first with light toggle, 15-company ticker tape, the ideas → research → holdings → signals loop) replaces the generated default at `investment-buddy/`; the complete registry record stays on its About page (`investment-buddy/about.html`), now linked from the custom page's footer. Pre-host pass on the Oct 11 working copy: the M3 line's "Finnhub free tier wired" corrected to "planned" (M3 is not built), `noindex, nofollow` meta added for Phase 0 parity, the canonical Tip Jar v2 added, the footer now reads "direct report to Finance Buddy" (Dave's preferred term), and the fleet-standard "Buddy System dashboard" link (A3) sits at the end of the hero header. No template markers on the page, so the basic-homepage generator leaves it alone. Still pending on this page: the Charts Buddy "AI stack, end to end" chart, integrated when it lands.
- **Dashboard 🏛️ — framework buttons group in the footer, and go nearly see-through (build 20261028.0712):** Dave's two asks in two messages: the floating framework buttons (his screenshot: the dark circles over the Calendar Buddy homepage) should be "translucent, almost completely see-through," and "let's create a setting that groups all four of those buttons, all the framework buttons, together in the footer." Both shipped. (1) **Translucency:** New (#new-buddy-fab), Back/Prev/Next (#hp-back, #hp-nav), Info (#panel-open) and Recents (#recents-btn) drop from 55%/72% fills to 16% (20% in light theme), blur kept, hovers at 34%; the panel's close × — the Info button's pixel-swap twin — takes the same fill so the pair still matches. (2) **The setting:** "Group framework buttons in the footer" (Settings, `frameworkButtonsFooter`, default ON; wired through SETTING_DEFS, `applySidebarStyle()`'s new `body.fw-footer` class, and the factory snapshot/reset lists). New and Back already anchor the bottom corners as 56px circles; Info and Recents drop from the top corners into the same row, inset one slot (88px = 20 margin + 56 button + 12 gap), their 44px circles centred on the row at bottom:26px. Off restores the corner layout (Recents' top-left pinned slot and the Info/× swap included). Phone widths (≤639px) keep the corner spots in both modes — the bottom cluster is already spoken for there — and the token-pill offset for Info is neutralised while grouped. verify-build.sh clean.
- **Buddy homepages 🔗 — Google Doc/Drive links open in a new tab (102 links, 39 pages):** Dave tapped the homepage fix after hitting Google's cookie wall twice ("Allow access" / "You can't access") opening Journal Buddy's job req — the link loaded the Doc inside the dashboard's homepage frame, where Google refuses embedded access. A fleet pass added `target="_blank" rel="noopener"` to every docs.google.com / drive.google.com anchor missing it across buddy homepages and About pages: 102 links in 39 files; a re-scan shows all 588 Google links on those pages now open in their own tab. The generators already emitted the attributes, so regenerations keep them; dashboard-panel document links already opened in a new tab. (The same commit also landed `bicycle-buddy/index.html`, which was complete on disk but still uncommitted — it rode in with the homepage sweep.)
- **Social Media Buddy — Reddit + X correction to the morning edition (Wed 2026-10-28):** the browser read's full report (ran 6:43–6:57 AM, all eight subs loaded — r/apple first loaded blank and cleared on reload — plus all four X profiles) arrived after the morning edition published with carried Reddit/X sections, the Oct 25–27 trap again. Corrected to the fresh read: Reddit's top 5 keeps r/ClaudeAI's AGI preview (14K), r/apple's 404 page (6.2K) and the Porsche/classic-car slots, but the Samsung-TV safeguards follow-up (3.9K, up from 3.8K) takes the #3 slot from the TV-fix post itself. X gains a genuinely new #1 — Gurman's Tue-evening post on Apple doing touch laptops anyway after 20 years of ergonomics arguments — ahead of his three carried afternoon posts, and @gregjoz's M6 MacBook Pro/iMac launch post takes #5 from @claudeai's nonprofits post (still that account's newest, noted in the page's X note; @ClaudeDevs still has nothing newer than Oct 23). All other sections unchanged. All 18 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, morning edition (Wed 2026-10-28):** Facebook is Top 2, no padding (newsfeed + friends feed, two pages each, 16 posts, heavily repeated) — Stefan Isaacson's three-carb teardown (Tue 7:34 PM) leads, ahead of Leslie Yuen's Hong Kong Concours D'Elegance post (Tue 6:34 PM); no family posts in the pages read. Instagram is Top 3, all cars and verified individually — Classic Driver's Challenge Stradale comeback reel leads, with Barn Finds' clean F-250 and a carstuesday hurricane meme behind it (the feed returned no timestamps; the other two posts were off-interest). Threads is Top 3, all Bring a Trailer — a 1988 Porsche 944 5-speed at no reserve leads, with a BaT success story and an 8k-mile Ducati 1198SP behind it (NBC News excluded). Reddit and X could not be refreshed: two live-browser passes worked through all eight subs and the four X profiles but returned no report before the edition closed, so last night's verified top 5s carry for both, labelled on the page as Tue evening's snapshot — nothing refreshed or invented. LinkedIn note updated to the latest drip-watch figures (767 impressions, 11 reactions, 2 comments). All 18 attention links carry target="_blank".
- **Dashboard 🔍 — ⌘F gives the Find overlay at the top of the main view again (build 20261028.0654):** Dave's screenshot from this thread: pressing ⌘F surfaced a search box at the top of the info panel — the 2026-10-27 A3 routing had sent ⌘F / Ctrl+F to the buddy panel's own search field (`focusPanelSearch`). Dave's correction: "if i do command-f, i should get a search box at the top of the main view section not over a side panel." The F chord routes to `toggleFind()` again, and `openFind()` now calls a new `positionFind()`: the Find bar and its results menu centre on `#main` (the main view), not the window, and stop at the info panel's left edge when the panel is docked over the main view's right side; a resize listener re-places the bar while it is open, and phone widths (≤639px) keep the stylesheet's full-width placement. The panel search is untouched and keeps the `/` shortcut; ⌘I still toggles the info panel. FEATURES.md's Keyboard and Panel search entries updated to match. verify-build.sh clean (node --check on the full main script, no broken strings); served copy verified after push (version.txt reads 20261028.0654, the served script carries positionFind and the toggleFind routing).
- **Mail Buddy 📬 — morning edition (Wed 2026-10-28):** scanned the inbox since the evening edition (Tue Oct 27, 5:41 PM – Wed Oct 28, 6:41 AM PT) — 84 messages, 78 newsletters/promos/bulk and routine notices spiked (incl. the routine Sports Car Adventures candidate-events mail and Dave's own briefing copies) and one folded into an item (Ray's Morgan Hill reply). No replies owed by email, no money moving, no bills due, no mail from Nan, Quentin, Sawyer, Amanda or the STIX team, and no Capital One or Chase mail. **5 ranked items** published: #1 Kay Korbel / Ray — Ray will review Llagas Creek repair items 12–16 plus the leaking hose bib and reply on bid-from-message vs. a site meeting, license and payment terms to follow; Kay clarified item 16's garage sink wand should be replaced, now thought beyond repair (Dave cc'd only); #2 Robert Kleinbrahm (FNRW) — the weekly radio net is tonight, Wed Oct 28, 7:00 PM, early check-ins 6:50 PM; #3 Riley (Everforth Apex) recruiter voicemail, a third day running (subject trimmed); #4 Zappos sign-in at 6:41 AM today on a macOS browser near California — security FYI; #5 Walmart — the Pentek 166219 package arrived Tue evening, a day ahead of estimate (delivered/closed). Every attention link carries target="_blank".
- **Mail Buddy 📬 — evening edition (Wed 2026-10-28):** scanned the inbox since the morning edition (Wed Oct 28, 6:41 AM – 5:41 PM PT) — 200 messages, 184 newsletters/promos/bulk and routine notices spiked (incl. two more identical Riley recruiter emails, now spiked as a standing repeat, the Schwab closing summary and three Nextdoor coyote posts), five folded into items, and the 6:41 AM Zappos sign-in already covered this morning not repeated. No direct mail from Nan, Quentin, Sawyer, Amanda or the STIX team. **10 ranked items** published: #1 Chase CWM Estates — beneficiary payout packet for Emil's account, death certificate with visible seal + notarized distribution request, return within 60 days of signing (subject trimmed, duplicates folded); #2 Kay / Best Care Fumigation forms — Dave was left off the list, paperwork ideally at least 3 days before, log dated Mon Nov 9, 2026; #3 Clean Crawl Space — reseal the liner for $3,600 (1–2 days) vs replacement, owners' decision; #4 Kay — Ray / Top Shelf Estimate 94 forwarded as very high, one more estimate coming; #5 PG&E autopay $716.83 processed (paid/closed, payment date Oct 27); #6 Capital One — Nancy $28.70 at Safeway (may be a pending authorization); #7 UPS package arriving Thu Oct 29, 2026, 2:15–4:15 PM; #8 Zappos order $172.39, arriving Nov 2–3 (subject trimmed); #9 Walmart iDesign package arrived (delivered/closed); #10 Tim Clark's two bcc shares grouped, no ask. Every attention link carries target="_blank".

## 2026-10-27
- **Garden Buddy 🌱 — thread id corrected (build 20261028.0114):** the registry's `chat` id for Garden Buddy (5cb359aa…, wired in build 20261028.0059) pointed at a thread that does not exist — a chat lookup against it fails. The real 🌱 Garden Buddy thread, created and INIT'd by the main agent, is https://muse.ai/chat/efe3e0fe-8e0e-43d0-8695-0b29c62a93ae; the entry's chat field now carries that id (one-line registry change, nothing else in the entry touched). Verified on the served copy after push: the live build carries the corrected id and Garden Buddy's homepage serves unchanged.
- **Dashboard 🫙 — Tip Jar no longer hides under the floating + button (build 20261028.0103):** Dave's iPad screenshot (Birthday Buddy's homepage, Oct 27 ~6:00 PM, bottom-right corner circled in red): the shell's floating + button (`#new-buddy-fab` — fixed at the window's bottom-right, right:20/bottom:20, 56px circle) painted over the right half of the homepage's Tip Jar pill, cutting it off. Root cause: the pill is `position:fixed` inside the homepage iframe at right:18/bottom:18, and when the frame fills the window (floating panels, or anchored with the info panel closed — the frame's bottom edge rides ~40px above the window's for the Refresh row, still inside the collision band) the iframe's bottom-right corner IS the window's bottom-right corner, so the two fixed elements land on the same spot and the parent document paints above the frame. Standalone homepages were never affected (no + button). Fix, shell-side in `build.py` so one change covers every homepage at once (all 163 jar-carrying pages, template and custom alike; the canonical snippet is untouched): on frame load the shell measures the frame's bottom-right gaps to the window; when both are ≤56px (collision begins under 58px) it injects one rule into the frame's document — `.tipjar{bottom:88px !important}` — stacking the jar in the corner column with its bottom edge 12px above the + button's top edge, both fully visible and tappable. Anchored mode with the info panel open pushes the frame ~456px off the window's right edge, the check fails, and the jar keeps its canonical corner spot; a ResizeObserver on the frame plus a window-resize listener keep the state right as panels open and close. The jar's v2 motion (breathing + shimmer, off under prefers-reduced-motion) is untouched — only its bottom offset is overridden, and only inside the dashboard. Clearance logic verified against the built script (corner layouts inject the lift, panel-open layout clears it, open/close flips re-evaluate); all inline scripts `node --check` clean via verify-build.sh; served copy verified after push.
- **Garden Buddy 🌱 — side thread wired (build 20261028.0059):** Garden Buddy's registry entry now carries its chat id (thread 🌱 Garden Buddy, https://muse.ai/chat/5cb359aa-a86f-4dcc-9eec-06aac66d82b7 — INIT + job-req review ask posted there; the voice-casting ask went to Decision Buddy's thread in the same pass).
- **Garden Buddy 🌱 — hired and wired (build 20261028.0056):** Dave's tap in the main chat ("Set up a Garden Buddy") after a big yard day — raking leaves and needles, making the backyard presentable — and his question about when to do the major trimming back. Garden Buddy (child of Cabin Buddy 🏕️) keeps the living half of the Fiddletown cabin: the plant inventory (built from Dave's photos; rosemary is the first plant on the books), a per-plant pruning calendar for Sierra foothills conditions (major cuts late winter–early spring; rosemary's big prune in spring after flowering, never deep into old wood; spring bloomers right after bloom), seasonal yard reminders, and the vegetation-control records inherited from Cabin Buddy (RM43-2 Total Vegetation Control, bought Oct 23 at Tractor Supply Jackson — cautions carried on the record: out of tree/shrub root zones, away from the well head, no planting within a year in treated areas; RM18 is the no-residual fallback near plantings). Registry now at 162 buddies; template homepage + About page generated, tip jar + dashboard link + role audio (voice Marisol, provisional — Decision Buddy casting asked; the first candidate, Gracious Fern, failed the synthesis check by silently falling back to the default voice and was rejected) hosted alongside. Persona **The Head Gardener** (alternates The Groundskeeper, The Orchard Keeper). First task: its own homepage; first real assignment: receive Dave's plant photos and build the inventory + trim calendar.
- **Mail Buddy 📬 — morning edition (Tue 2026-10-27):** scanned the inbox since the evening edition (Mon Oct 26, 5:41 PM – Tue Oct 27, 6:41 AM PT) — 99 messages exactly, 85 newsletters/promos/bulk and routine notices spiked (incl. eight of Dave's own briefing, new-hire and Development Story copies) and five folded into items (paired Capital One alerts, a duplicate Google alert, TypeSafe's welcome/sign-in pair). No direct mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Chase mail. **9 ranked items** published — no replies owed, no bills due: #1 Capital One — $716.83 at PG&E charged to Nancy's Quicksilver (pending authorization or purchase); #2 FPPOA Board meeting Sat Oct 31, 2026, 10:00–10:30 AM at the Fiddletown Schoolhouse (agenda: delinquent assessments + lien-process authorization); #3 Google security alert — new Mac OS sign-in at 12:37 AM; #4 Zappos sign-in at 11:24 PM reported near Texas (follow-on to yesterday's password update); #5 Supabase invoice $34.35 paid (paid/closed, matches its Capital One alert; subject trimmed); #6 TypeSafe AI $5.00 receipt paid (paid/closed; new-account welcome/sign-in mails the same evening; subject trimmed); #7 CA Secretary of State — DMV voter registration processing (3–5 days, postcard to follow); #8 Nextdoor neighbour post — 33 San Jose speed cameras under AB 645 (neighbour post, not official); #9 Sports Car Adventures candidates (Darin Sexton and Highway 49 at Feist Wines, Nov 22; A Drytown Halloween, date to confirm). Every attention link carries target="_blank".
- **Mail Buddy 📬 — evening edition (Tue 2026-10-27):** scanned the inbox since the morning edition (Tue Oct 27, 6:41 AM – 5:41 PM PT) — 186 messages exactly, 176 newsletters/promos/bulk and routine notices spiked (incl. ten CareerBuilder job alerts, several Nextdoor neighbour posts and a Schwab closing summary) and two folded into items (Ron's Morgan Hill message, the Refresh intake-form ask). No money moving, no bills due, no direct mail from Nan, Quentin, Sawyer, Amanda or the STIX team, and no Capital One or Chase mail. **8 ranked items** published: #1 Kay Korbel via LinkedIn — a message awaits Dave's response (content on LinkedIn only); #2 Google User Experience Research — developer profile deadline **Fri Nov 6, 2026**; #3 Kay/Ron Morgan Hill thread — Ron fixed repair item 16's spray wand, hose and sprayer to be replaced and added to the estimate; #4 Kay's bid request to Ray for inspection items 12–16 plus the leaking hose bib; #5 Kay's chased Superior Plumbing bid for the same list — repairs wanted mid November, after fumigation and before Thanksgiving; #6 Refresh at Sutter Creek — Nancy's massage Sat Nov 7, 2026, 1:00–2:30 PM confirmed, intake form first; #7 Riley (Everforth Apex) recruiter voicemail, a repeat of yesterday's pitch (subject trimmed); #8 USPS — Amazon package expected Wed Oct 28, 2026 by 9:00 PM (subject trimmed). Every attention link carries target="_blank".
- **Jev Buddy ⚡ — hired and wired (build 20261027.1328):** Dave's direction in the Decision Buddy thread ("I'd like to wire up the jev buddy sooner than later"). Jev Buddy (child of Project Buddy 🧭) runs Jev — TypeSafe AI's System One decision model — as a shared fleet service, not Decision Buddy's private tool: it owns the custom.typesafe connector, the data-class guard (operational text only, ever), the confidence policy, and the shadow/measurement log, so every buddy's bounded calls (brain-dump routing, triage, decidability pre-screens) go through one front door. The charter hard rules are written into its job req: the rules travel inside every request (no written rules = no call), pinned model ids only (jev-1.14.0, never the alias), Jev never scores prose/design and never touches one-way doors, and spend is capped at Dave's $5 TypeSafe credit (bought Oct 26) without separate approval. Continuity, stated not acted on: DB-2026-011's shadow pilot (live Oct 26 23:57 PT, first batch 7/7, log in the decision-buddy repo, reviews Nov 25 / Dec 25 / Jan 24) stays under Decision Buddy until Dave makes the transfer explicit; Decision Buddy's journal frames the hire as DB-2026-012. Job req (Google Doc, TITLE + 8 sections read-back-verified) + private repo + template homepage with role audio hosted alongside; registry now at 159 buddies. Persona **The Umpire** (alternates The Oddskeeper, The Switchboard Operator), voice **Crisp Collar** — provisional: Decision Buddy holds the standing casting duty and Dave's audition pick overrides. Side thread + INIT + review ask post from the main chat.
- **Hires wiring + homepage package (build 20261027.1328):** Dave's approval in the main chat (item A4 of the approval queue, ❤️). The two remaining Oct 24 hires join the registry — **Astronomy Buddy 🔭** (child of Project Buddy; voice Grounded Hearth `avocado_v2:vd2_grounded_hearth`, Decision Buddy's casting) and **Tester Relations Buddy 🤝** (child of Project Buddy; voice Steady Blanket `avocado_v2:vdc_13453`, Dave's own Oct 24 audition pick) — registry now at 160 buddies (161 once Jev Buddy’s parallel wiring, above, is counted). Their custom homepages are hosted at `astronomy-buddy/` and `tester-relations-buddy/` with role-intro audio beside each: Tester Relations' Steady Blanket recording already existed; Astronomy's was synthesized new from the first paragraph of its job req's Role summary in Grounded Hearth, its page gains the standard "Hear my role" control, and its stale "goes live when Astro wires the registry" note now matches reality. **About pages refreshed fleet-wide** via `gen_default_homepages.py --about` against the current registry — the full fleet (this also lands the About page the Decision Buddy entry above had as still-owed, and first About pages for 16 others incl. Journal Buddy and Bicycle Buddy, whose About now exists ahead of its homepage). **Tip Jar fleet rollout:** the canonical motion-v2 snippet (breathing + shimmer + hover spin, → https://ko-fi.com/davedellaquila) now rides on every buddy homepage — all 161 `*/index.html` pages carry it (153 gained it in this pass, incl. the two origin-side pages that landed mid-build: Calendar Buddy's new calendar page and Decision Buddy's homepage) — and both page generators (`gen_basic_homepages.py`, `gen_default_homepages.py`) now read the snippet live from `docs/tipjar-snippet.html` at generation time, so template/Dossier homepages and About pages keep the jar on every future rebuild. Dashboard rebuilt with verify-build.sh; all inline scripts `node --check` clean; served copies verified after push.
- **Nancy Buddy 👩‍🍳 — Wife — Job Description linked:** the [Wife — Job Description](https://docs.google.com/document/d/1TCCH3YWxVUCxw1qQ8qB39VqeQImH3DIxfEdC5AUBjbM/edit) (Nan's R&Rs in job-description form, 13 departments after two Decision Buddy expansion rounds) is now linked in Nancy Buddy's Documents — her `docs[]` was empty until now. Ownership of the document moved from Decision Buddy to Nancy Buddy at Dave's direction (Oct 27 handoff); the Role / Particulars / Qualifications / Compensation / Performance sections are Dave-approved originals, preserved verbatim. Registry-only change (commit 874811c), verified on the served buddies.json.
- **Decision Buddy 🎯 — registry wiring + homepage live (the 404 fix):** Decision Buddy — hired 2026-10-24, job req approved by Dave the same day, private repo and custom homepage built day one — was never added to buddies.json, so its dashboard URL 404'd while its own messages kept linking it (Dave hit the dead link this morning and reported it). Now wired, modeled on Journal Buddy's entry from the same hire week: child of Project Buddy, kind standalone, status Active, job-req Google Doc as `brief` + linked doc, this thread as `chat`; registry now at 158 buddies. Its custom homepage (tier-ring queue visual, Tier-1 cards, the walk, the journal — built Oct 24 in its repo and mirrored here verbatim as `decision-buddy/index.html`) is live at `decision-buddy/`; the page deliberately carries no "Part of the Buddy System" template marker, so the basic-homepage generator leaves it alone. Still owed by the standard pipeline: the generated About page (`decision-buddy/about.html`) — the custom homepage is the buddy's face until then. Served copy verified after push.
- **Journal Buddy 📓 — homepage shipped + registry wiring (build 20261027.1315):** Dave's approval in the main chat (item A1 of the approval queue, ❤️). Journal Buddy — hired 2026-10-24 to keep Dave's personal journal in his own words, entries filed in the private journal-buddy repo — finally gets its registry entry: child of Project Buddy (its brief's stated reporting line), kind standalone, status Active, the brief Google Doc linked as both `brief` and the Product Brief doc; registry now at 157 buddies. Its custom homepage — built Oct 24 as its first task and waiting unshipped since — is live at `journal-buddy/` with its role-intro audio, and gains the canonical Tip Jar, which the built page never carried. Persona and voice stay unset in the registry: the buddy's seed SOUL.md records neither, so none was invented. Same morning, the buddy's own wiring went live in its repo (nightly compile files each day Dave dictates a recap; Oct 25–26 backfilled). Dashboard rebuilt with verify-build.sh; all inline scripts `node --check` clean; served copies verified after push.
- **Calendar Buddy 📅 — "On the calendar": a real month calendar on the homepage:** Dave's ask in the main chat ("I'm looking for something that shows me stuff on a calendar" — the homepage had charts *about* his week but no actual calendar). New section between the week charts and the calendar radar: a month grid starting on the current month with prev/next navigation (clamped to the snapshot window), Dave's real events on their days (time + title chips, "+N more" past two), today highlighted, and a click-any-day agenda below the grid listing that day's events with times. Data is a static snapshot, `calendar-buddy/events.json` — 188 events over the next 60 days pulled from Dave's nine owned Google calendars (primary, Family Events, Finance, Nan's, Sawyer's, Apple WWSF, Optional Events, Reminders, Quentin's; reader-only subscription feeds like Holidays/IxDA/club rides skipped), privacy-minimized to title + start/end + all-day flag only — no locations, attendees, descriptions or event IDs — and the page renders entirely from that file (no live API calls from the browser). A daily cron (`calendar-events-refresh`, ~5:11 AM PT) re-pulls the window and republishes the snapshot when it changes. Existing sections untouched; all three inline scripts `node --check` clean; dark mode follows the page's existing `prefers-color-scheme` variables; served copy verified after push.
- **Dashboard link on every buddy homepage + buddy-panel search (A3):** Dave's steer in the main chat (❤️ on the A3 queue item). (1) Every buddy homepage that lacked one — 130 of the 157 top-level pages — now carries a visible **"Buddy System dashboard"** link back to the dashboard root, marked `class="bs-dash-link"` so the pass is idempotent; the 27 pages that already linked home were left untouched. Placement follows each page's own structure: inside the sticky `.topbar` header on template pages, at the end of the `<header>` on custom pages, appended to the crumb nav where that's the top nav, and as a small top strip on the three pages with none of those. Both generators learned the link so regenerations keep it: `gen_basic_homepages.py`'s TEMPLATE (topbar anchor + `.bs-dash-link` rule) and `gen_default_homepages.py`'s PAGE footer. (2) The buddy/info panel gains its **own search field** (`#bp-search`) at the top of the panel, visible in panel/sheet mode only. It drives the SAME filter as the sidebar search — the query mirrors into `#buddy-search`, so the shared `buddyMatchesQuery` matcher (name + display name + tagline + A.K.A.) filters the buddy list as you type and the two boxes can never disagree; typing in either box keeps the other in sync. **Enter** opens the top match in the panel (`firstSearchMatch` → `openBuddy`); the × clears both boxes; Escape clears the query first, then blurs — the panel itself still closes on the next Escape, exactly as locked. **Keyboard reroute:** `/` and **⌘F / Ctrl+F** now open the panel when needed and focus its search field (`focusPanelSearch()`), instead of focusing the sidebar box / toggling Find. The Find overlay is unchanged and stays on the footer Find button (its title no longer advertises ⌘F, and the sidebar search's tooltip dropped the stale "Press / anywhere" line). ⌘I still toggles the info panel. Locked chrome untouched: the info icon/close × swap, pinned Recents, and Prev/Next/Back are exactly where they were — the search row lives inside the panel's own flow and displaces none of them.

- **Social Media Buddy — 👀 Worth your attention, morning edition (Tue 2026-10-27):** Facebook is a thin pull (newsfeed + friends feed, two pages each, 16 posts) led by Lari Macri's speeding-ticket-to-bicycle joke, ahead of the Broad Street Beacon's Highway 49 satire, a Kwik Serv Jackson thank-you, Eric Weiss's neighbours post and a property-notice group question; no family posts in the pages read. Instagram is Top 3, all cars, all this morning and verified individually — BaT's silver 1955 300SL Gullwing leads, with Hagerty's Tata Nano feature and Barn Finds' custom Silverado behind it. Threads is Top 3, all BaT/Barn Finds — a 27k-mile 2010 Porsche 911 Carrera Cabriolet 6-speed leads. Reddit could not be refreshed: two live-browser passes returned no report before the edition closed, so last night's verified top 5 carries, labelled on the page as yesterday evening's snapshot. X is search-only — Gurman posted three times this morning on Apple's M6 MacBook Pro / M6 iMac launch (announcement, specs + Oct 28 pre-orders, Bloomberg write-up), plus his 8:53 PM Duo bug post from last night; @claudeai's nonprofits post carries as that account's newest. LinkedIn note updated to the latest drip-watch figures (730 impressions, 11 reactions, 2 comments). All 21 attention links carry target="_blank".

- **Social Media Buddy — Reddit correction to the morning edition (Tue 2026-10-27):** the first browser pass's full report (ran 6:43–6:46 AM, all eight subs loaded, no bot check) arrived after the morning edition published with a carried Reddit section — the same trap as the Oct 25–26 corrections. Corrected to the fresh read: r/apple's best-404 post is at 6.1K (was 6K carried), r/classiccars has a new leader ("In the shop today.", 1.2K) displacing the carried '67 Cougar thread in the #5 slot, and the note now records that r/ClaudeAI holds four of the five highest-voted posts (the safeguards-around-TV post at 3.7K and the Claude-as-senior post at 3.5K sit just below the kept Porsche/classic-car slots). All other sections unchanged. All 21 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, evening edition (Tue 2026-10-27):** Facebook (newsfeed + friends feed, two pages each, 18 posts) is led by two local road alerts from this afternoon — a major-injury, life-flighted crash at Glencoe (4:50 PM) and a multiple-injury accident at Hwy 88/104 near Ione (4:12 PM) — ahead of a 1958 MGA being parted out, a Model A tire-changing seminar and Michael Randazzo reaching Randazzo; no family posts in the pages read. Instagram is Top 4, all cars and verified individually — hardtuned's RX-7 reel leads, with a truck-van mashup meme, a Forgiato Escalade and a Slammedenuff carousel behind it (NBC News excluded). Threads is Top 2 — BaT's 1972 Ferrari 365 GTC/4 leads, the Slammedenuff carousel cross-posted behind it (both other posts NBC News). Reddit refreshed fresh via the browser (5:43–5:47 PM, all eight subs, no bot block): r/ClaudeAI's AGI preview (14K) and Samsung-TV fix (4.3K, up from 4.2K) and r/apple's 404 page (6.2K, up from 6.1K) lead, with r/Porsche's first 911 (2.6K) and r/classiccars' shop-day post (1.2K) kept for balance. X carries this morning's five verified posts (Gurman's three M6 launch posts, his Duo bug post, @claudeai's nonprofits post) — the evening browser re-check of the profiles returned no report before the edition closed and topic search yielded no new direct status URLs, so nothing unverified was added; the page note says so, and notes 9to5Mac quoting a further unlinked Gurman post on the non-touch models staying. LinkedIn note updated to the latest drip-watch figures (745 impressions, 11 reactions, 2 comments). All 21 attention links carry target="_blank".
- **Social Media Buddy — X correction to the evening edition (Tue 2026-10-27):** the evening X profile re-check returned at 5:55–5:56 PM, after the edition first published with this morning's verified X posts carried — the same late-report trap as the Oct 25–27 Reddit corrections. Corrected to the fresh read: Gurman posted three times this afternoon on tomorrow's touch MacBook Pro — the non-touch models staying at $2,499/$2,999 with retail fully stocked (3:13 PM; the post the first publish could only mention unlinked, now verified), what he still expects (M5 Pro/Max, redesigned hinge, new cooling, thinner/lighter, 3:11 PM) and discussed touch-OLED pricing (14-inch from $2,899, 3:09 PM). His 6:03 AM M6 announcement and @claudeai's nonprofits post (still that account's newest) round out the five; @gregjoz's 6:08 AM M6 post sits just below the cut and @ClaudeDevs has nothing newer than Oct 23. Gurman's profile hit a login wall after four newer posts, so his Oct 26 posts could not be read — the page note says so. All other sections unchanged. All 21 attention links still carry target="_blank".

## 2026-10-26
- **Tip Jar 🫙 — motion v2: real breathing + an occasional shimmer (every canonical-snippet surface):** Dave's steer in the main chat ("i notice the tip jar is rather static. i like how the mug spins around when you hover over it but maybe add gentle pulsing, a bit of breathing, or something to attract some attention to it. a shimmer every once in a while is always fun"). Diagnosis first: the v1 animation WAS present in the served pages — but its breathing ran scale 1→1.035 over 6s (≈±2px on the pill, under most people's motion threshold) and its only other idle move, the hop + coin glint, was visible for ~0.7s inside a 9s cycle — the pill sat still ~92% of the time, so it read as static. V2, now canonical in `docs/tipjar-snippet.html` (committed to the repo with this change — it previously existed only as a local working file): breathing at 3.2s ease-in-out, scale 1→1.045, with the purple glow swelling in step (shadow 18px/.35 → 26px/.55 at the peak); a shimmer — a soft white gradient sweep (::after, clipped to the pill) crossing once every 8s, a ~1.3s pass inside a long rest built into the keyframe cycle; the hover jar-spin Dave likes is unchanged. V1's hop + coin glint and the hover label-brightness pulse are retired — breathing + shimmer + hover spin is the trio (reasoning recorded in the snippet's design notes). Transform/box-shadow only, no layout shift; prefers-reduced-motion turns all of it off and hides the sheen. Rolled out by scripted block replacement to every page carrying the canonical pill: Hans's chime control panel, Game Buddy, Lenwood Water, the Awards Soundboard, Stumpjumper Buddy, W163 Mastertech Buddy, and both Voting pages (E39 Touring shirts, gallery preference) — and Hans's own homepage GAINS the jar, which it never had (the chime subpage did). Bicycle Buddy's homepage carries v2 on disk as well; that directory is still uncommitted, so the new jar ships when the homepage itself lands. NOT touched, deliberately: the dashboard sidebar jar — a separate, older implementation (the 9s tipjar-party loop plus JS idle bounce/race/poof effects) that is already animated by design and is not the canonical component; Money Buddy's inline "Tip the jar" text link, a different element; and the generated basic homepages, which don't carry the jar yet — that fleet rollout still rides the pending homepage package. Served copies verified after push.
- **Hans 🔔 — Hourly Chime composition mode: one at a time (OR) or all together (AND):** Dave's steer in the main chat ("i'm getting like three different signals in one hourly chime and it's a bit much... i think it'd be nice to just focus on one... a rhyme on one, maybe a riddle on another, maybe a joke on a third, and cycle through them") — the chime's content segments now combine two ways, set from the control panel (`hans-buddy/chime/`). New `composition` object in `hans-buddy/chime-config.json` (`mode`, `appliesTo`, `cycleOrder`), seeded **rotate**: in **rotate (OR)** mode each chime carries exactly ONE content module — couplet, riddle, joke, weather, Zen saying, news headline, positive thought — cycling deterministically through the enabled ones in config order, with the cycle pointer kept in a new "Content rotation" record in `~/workspace/astro-chime/state.md`; riddle/joke are skipped in the cycle outside the 7 AM–10 PM window (never served, never stalled on), a lone enabled module serves every chime, no enabled modules means time-only, and the pending riddle waits unrevealed between its turns (Sheet appends happen only when the riddle/joke module is actually served). In **all (AND)** mode every enabled module appears in every chime — the original behavior. The mode governs content modules only: the time announcement, the presenter frame, the recording, the urgent lines and SFX placement behave as before in both modes, and the foreign-language rule applies to whatever the chime carries. The panel gains a two-option radio control at the top of "What shows up in the chime" — "One at a time — cycle through my picks (OR)" / "All together — every chime (AND)", each with a plain-English explainer — riding the same token-gated save and on-device queue, and the settings summary now states the active mode in words (e.g. "Each chime carries one segment, cycling: Rhyming couplet → Riddle → Joke"). The `hans-hourly-chime` cron's CONFIG/MODULES prefix gained the composition rule (CONFIG now points at `composition.mode`; a new COMPOSITION paragraph defines both modes); everything from "You are Hans…" onward is byte-identical to before — 12,399 tail bytes, diff-verified against a pre-edit backup — and the hourly schedule is untouched. Inline script `node --check` clean, all 34 referenced element ids present; served copy verified after push.
- **Dashboard 👤 — profile hero at the top of the buddy info panel (build 20261027.0522):** Dave's ask in the main chat, with his screenshot of the Muse profile card ("i like this treatment. can we do something similar at the top of the info panel?") — the buddy panel now opens with a profile hero in that treatment: a large (104px) centered circular avatar (the buddy's uploaded image from `avatars/<id>.jpg` when one exists, its emoji large in a subtle circle otherwise) with a small dark pencil badge overlapping its bottom-right edge, the buddy's name in large type under it, and a quiet centered status line — a dot in the status color, the registry status text (now shown for every buddy, Active included), and a "⚑ N need attention" flag when the buddy has unseen attention items. The pencil badge is functional, not decorative: it scrolls to the sticky bar's rename input, focuses it with the name selected, and flashes it. The hero avatar opens the same avatar picker as the sticky bar's icon. The old status annotation line under the tagline is retired — status lives in the hero now, shown exactly once. Everything else is untouched: the compact sticky identity bar, the fixed info/× pixel swap at top:12/right:12, Recents pinned, Prev/Next/Back, ESC behavior, and every panel section (voice/persona pickers, toggles, docs, attention buttons) work exactly as before; the hero scrolls away with the content. All inline scripts `node --check` clean via verify-build.sh; served copy verified after push.
- **Hans 🔔 — Hourly Chime Control Panel (`hans-buddy/chime/`):** Dave's ask in the main chat ("if we have a buddy for that, create a web page that we can configure it") — the hourly chime is now configurable from a page instead of chat requests. New settings file `hans-buddy/chime-config.json`, seeded with today's exact behavior, plus a control-panel page in Hans's homepage style. On top: a **What shows up in the chime** module checklist — time announcement (core, locked on), rhyming couplet, riddle, joke, and four NEW opt-in segments (weather line, Zen saying, news headline, positive thought — all default OFF) with ▲▼ segment ordering. Below, the dials: audio on/off; riddle & joke window (7 AM–10 PM); foreign-language rate (20%), never-back-to-back, language rotation; sound effects (max 2 per chime, dose ~50%, quiet hours 11 PM–6 AM, midnight-gong exception); urgent check (max 2 lines); and the 16-presenter roster (11 regulars + Scooby gang guests) as a checklist, with a live plain-English summary of the current settings. Save writes the JSON through the fleet's token-gated flow (shared `buddyTree.v3` token store, verified at entry): a missing or rejected token queues the save on-device with the reason shown and auto-syncs when a working token lands — nothing is silently dropped. The `hans-hourly-chime` cron body gained a CONFIG section with everything else preserved verbatim: read the config before composing; its values override the written defaults; compose from enabled modules only, in the config's segment order; the riddle/joke window still gates those two modules overnight while the new modules may run in any chime; exactly one instance of each new module per chime; a module whose content can't be fetched is skipped silently rather than failing the chime. Delivery target stays a status line, not a dial — it lives in the scheduled job itself, not the settings file. Inline script `node --check` clean; dark mode per standing order; served copy verified after push.
- **Social Media Buddy — 👀 Worth your attention, evening edition (Mon 2026-10-26):** Facebook leads with a fresh Dell'Aquila Garage post (11:47 AM, no caption in the feed read), ahead of the California Landmark Foundation's Irishtown/Pine Grove plaque story, a group easement question, George Takei's Walter Koenig tribute and the Sutter Creek Witches Walk recap; no family posts in the pages read. Instagram is a short all-car pull (Top 2, no padding) — Barn Finds' one-off targa-roof 1964 Barracuda and BaT's Tiffany Blue 1961 Lincoln Continental, both fresh this evening and verified individually; Threads is Top 1 (the same Barracuda cross-post). Reddit via the browser, all eight subs loaded: r/ClaudeAI's "preview of AGI" still leads at 14K, r/apple's best-404 post is at 6K, and r/Porsche's first-911 post nudges to 2.5K. X is search-only — Gurman posted three times this afternoon on the touch MacBook Pro and iPhone Duo, @claudeai's nonprofits post and @trq212's AIE keynote post round out the five; topic search hit the login wall again. LinkedIn note updated to the latest drip-watch figures (699 impressions, 10 reactions, 2 comments). All 18 attention links carry target="_blank".
- **Awards Soundboard 🔊 — the big expansion: 14 → 101 sounds (Mon 2026-10-26):** Dave's ask in the main chat ("I love this app board — add more sounds, get it up to 100"). 87 new pads in 9 new sections (🎪 Comedy Stings, 📯 Fanfares & Bells, 🎲 Game Show, 🏠 Around the House, 🌩️ Nature & Spooky, 🏟️ At the Game, 🐾 The Animal Kingdom, 👏 More Audience, 🎉 Party & On the Town) join the original three; the original 14 sounds, keys, labels and order are untouched (embedded audio verified byte-identical). Every new sound is a real recording — trimmed to the hit, level-matched, peak-normalized, embedded as mono 64 kbps MP3 — and the page grows 1.4 MB → 4.8 MB. Licensing stayed strict: public domain / CC0 / CC BY only, sourced from Wikimedia Commons, SoundBible and OpenGameArt, with a full per-sound credit list (title, author, license, source link) in a collapsible footer section; Sampling Plus and Personal-Use titles were rejected along the way, which is why there is no DJ scratch, no ahooga horn and no stadium-organ "Charge!" (only restricted-license copies surfaced). One derivation, disclosed in its credit: Slide Whistle Up is the Slide Whistle Down recording reversed. Confetti now also fires for Grand Fanfare and Fireworks. Astro's extracted SFX library for the Hans chime (~/workspace/audio/sfx/) was refreshed from the final board — all 101 sounds. Inline script `node --check` clean; served copy verified after push (101 FILES keys on the live page).
- **Voting Buddy v2 🗳️ — page-preference poll page (`vote/gallery-preference/`):** Dave approved the v2 brief this morning ("go ahead and implement it") — Voting Buddy grows from pick-one polls to feedback on anything. New static page built from the gallery draft Dave verified on his iPhone: the same four stand-in pages (dashboard, News Buddy, E39 shirt vote, Awards Soundboard) as scaled live-miniature cards, now with a working ballot — a 1–5 star rating per card plus a "★ My favorite" pick. Identity follows the brief's tiers: an invite token in the link (`?v=…`) makes it a personal ballot the server keys by the token's SHA-256 hash (re-voting replaces, never double-counts); without one it falls back to the v1 browser token and says so on the page. Until the buddy-server deploy lands, ballots queue on-device in the E39 page's exact pattern ("saved on this device and will be sent automatically as soon as the vote counter goes live — nothing is lost"), and each card labels what you're seeing — your ballot on this device vs. the live tally. Server side (buddy-server repo): `rate` + `preference` poll types, invite-identity enforcement with a clear unrecognized-link error, rating tallies (average + count + 1–5 distribution, plus leader/margin), a `ballots` Firestore collection alongside the untouched v1 `votes`, 18 new local tests beside the 14 v1 checks (all passing), and `tools/mint-invite-links.js` to mint Quentin/Sawyer/Nan-style links (only hashes ever enter the poll config). The email-code identity tier is deliberately stubbed as phase 2. The one gate is unchanged: Dave's ~15-minute buddy-server deploy + project ID, then Astro wires `API_BASE` on both vote pages and verifies the live tally end-to-end. Inline script `node --check` clean; dark mode included per standing order. Full notes: `~/workspace/voting-buddy/IMPLEMENTATION.md`.
- **Social Media Buddy — X correction to the morning edition (Mon 2026-10-26):** the X profile read's full report arrived after publication (the edition was built from its interim recap — the same trap as the Reddit corrections). Corrected to the full report: @markgurman posted five times this morning (6:04–6:20 AM) on the revamped OLED iPad mini launch — his "Meanwhile" post and the $699/A20 Pro launch post take X #1–#2, @ClaudeDevs' MCP Tasks post (Oct 23) takes #3, and the interim recap's Skills-for-Outlook lead item (absent from the full report) is removed. All other sections unchanged. All 22 attention links still carry target="_blank".
- **Social Media Buddy — Reddit correction to the morning edition (Mon 2026-10-26):** the browser read's full report (ran 6:42–6:46 AM) arrived after the edition published with a carried Reddit section. Corrected to the fresh read: all eight subs loaded; r/apple's best-404 post is at 5.9K (was 5.8K carried), and r/classiccars' "Should I Buy This 67 Cougar?" (2.4K) takes the #5 slot from the carried r/Porsche item (tied at 2.4K; Porsche's leader is noted just below the cut), with the discrepancy noted honestly in the page's Reddit note. All other sections unchanged. All 22 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, morning edition (Mon 2026-10-26):** Facebook is thin — a late-night tag post (Dawn Elaine, 11:45 PM) leads, ahead of Atlas Mirabilium's Carquinez Strait megaflood post and two carried items; no family posts in the pages read. Instagram is fresh and all about cars and auctions (Top 4, no padding) led by a straight-piped Ferrari F40 reel, with Sotheby's Abu Dhabi Collectors' Week, Barn Finds' 106-mile F50, and a Hagerty transformation reel behind it — every item posted 6:00–6:20 AM today. Threads is Top 3, all Bring a Trailer within ten minutes of the edition — a 3k-mile 2013 Jaguar XK Convertible at no reserve leads. Reddit could not be refreshed: two live-browser passes closed without returning a report, so last night's verified top 5 carries, labelled on the page as yesterday's snapshot. X is search-only — the profile read surfaced two Claude posts not in last night's edition (@ClaudeDevs' Skills for Outlook, @claudeai's auto-mode-by-default post); the other three carry, honestly dated. LinkedIn note updated to the latest drip-watch figures (673 impressions, 9 reactions, 2 comments). All 22 attention links carry target="_blank".
- **Mail Buddy 📬 — morning edition (Mon 2026-10-26):** scanned the inbox since the evening edition (Sun Oct 25, 5:41 PM – Mon Oct 26, 6:41 AM PT) — 83 messages, 76 newsletters/promos/bulk and routine notices spiked (incl. Dave's own briefing copies, Reddit digests, a Nextdoor neighbour reflection post, and a Kalshi welcome). No mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Chase mail. **7 ranked FYI items** published — no replies owed, no bills due, no deadlines: Frontier auto-pay $89.99 processed (paid/closed); Capital One $34.00 at K&J Magnetics (pending authorization or purchase, noted as differing from the $29.90 order total); Conifer Communications $50.00 charged to OTRAC Car Storage (paid/closed); K&J Magnetics order confirmed ($29.90, subject trimmed); Adrenaline Bike Works BBT-22 shipment on its way (subject trimmed); Tim Clark's Citroën DS video link; and a Sports Car Adventures candidate (Mark Stuart Trio at Feist Wines, Nov 20). Every attention link carries target="_blank".
- **Mail Buddy 📬 — evening edition (Mon 2026-10-26):** scanned the inbox since the morning edition (Mon Oct 26, 6:41 AM – 5:41 PM PT) — 186 messages, 174 newsletters/promos/bulk and routine notices spiked (incl. ten CareerBuilder job alerts, Dave's own Money Buddy competitive-analysis copy, a Schwab closing summary, a Lotus Club track-day promo and a TiVo digest). No mail from Nan, Quentin, Amanda, the STIX team or Kay Korbel, and no Chase mail. **9 ranked items** published: #1 a call to return — Jake at Kanopy's voicemail following up Dave's exchange with his partner Burke about services for adventure companies like Sports Car Adventures, asking Dave to name a time today or tomorrow (subject trimmed, caller number off the page); #2 Capital One Quicksilver statement ready — $3,251.54 balance, $32.00 minimum, due **Nov 19, 2026**; #3 Substack — Stripe needs information verified on the account connected to Dave's Substack (KYC, as soon as possible, no date given); #4 Zappos password updated at 3:55 PM with sign-in notices in the same minutes (security FYI); #5–6 Sawyer's shared-calendar additions for Mon Nov 2 (Mike SBA loan zoom 9–10 AM, Nick Zoom 1–2 PM); #7 Riley (Everforth Apex) recruiter pitch for a Senior Content Designer role, email + voicemail grouped; #8 ModernBike order shipped by USPS (subject trimmed); #9 Walmart packages arrived — Morton Clean and Protect + 3 items (delivered/closed). Every attention link carries target="_blank".
- **Dashboard 📌 — sticky section headers in the buddy panel (build 20261026.0007):** Dave's ask in the main chat, with his screenshot of Project Buddy's panel — section headers now stick as they bump up against the sticky identity head, "just like a lot of other lists with sticky headers." Every panel section header (both the classic `h3` sections — Dump box, Needs your attention, Children, Peers, Photos, Documents, Artifacts — and the attribute-pattern headers — ABOUT, PERSONA, PRIVATE NOTES, …) is `position: sticky` with a solid panel background, holding flush under the head (resting at the head's own 10px margin edge) while its section scrolls beneath it, until the next section's header pushes it off. The stick line isn't hard-coded: `fitBpStickySections()` measures the rendered head (computed sticky top + height + bottom margin) on every panel render and on resize and publishes it as `--bp-sec-stick` on the panel wrap, so the headers stay flush across the desktop panel, the iPad sheet, and the phone takeover (whose head rides 53px lower). Verified in headless Chrome at 1280px and 390px: Project Buddy's Children header sticks at the line and holds it through 900px of further scroll; all inline scripts `node --check` clean; regression test `~/workspace/iphone-pass/tests/bp-sticky-sections.cdp.js`. Scope: the dashboard's buddy/business-plan panel only — the standalone buddy homepages don't have this panel.

## 2026-10-25
- **Social Media Buddy — Reddit correction to the evening edition (Sun 2026-10-25):** the browser read's interim recap (which the evening Reddit section was built from) conflicted with that same read's full final report, delivered after publication — the same trap as this morning's correction. Corrected to the full final report: r/ClaudeAI's "preview of AGI" is at 14K (not ~12K), r/apple's best-404 post is at 5.8K, and r/Porsche's week is led by "My First Porsche 911" (2.4K) — the Washington Square Park post in the first evening version came from the faulty recap and is removed, with the discrepancy noted honestly in the page's Reddit note. Facebook, Instagram, Threads, X and LinkedIn sections unchanged. All 22 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, evening edition (Sun 2026-10-25):** Facebook is thin tonight — Rich Lynn's birthday thank-you (9:37 AM today) leads, ahead of the Dell'Aquila Garage MGB GT restomod hood-up post, a same-day tag post, Michael Randazzo in Sicily, and the carried Mayhew Bayne Road ride; no family posts in the pages read. Instagram is a short all-car pull (Top 4, no padding) led by a gated 6-speed Murciélago reel, with Barn Finds' International 1210 and 1958 Dodge Royal and a Supra reel behind it; Threads is thinner still (Top 3) — the Murciélago cross-post, BaT's 143-mile Aventador Ultimae, and the International 1210 cross-post, with a hiring-spam post left off. Reddit via the browser, all eight subs: r/ClaudeAI's "preview of AGI" still leads at ~12K, r/apple's best-404 post holds at 5.6K, and r/Porsche's Washington Square Park spotting (3,620) takes the Porsche slot. X is search-only — one genuinely newer post found (Gurman's iPhone Duo Face ID / Vision Pro post); topic searches hit the login wall, so the other four carry from the morning's verified profile read, honestly dated. LinkedIn note updated to the latest drip-watch figures (654 impressions, 9 reactions, 2 comments). All 22 attention links carry target="_blank".
- **Recents menu — "Show more" paging (build 20261025.1556):** Dave's spec in the main chat — the Recent menu (clock button, top-left) showed the first 10 and stopped. Now, when more buddies are remembered than the first page shows, the next row is a **Show more** row; each tap reveals 10 more, up to the 50 remembered. First page still follows the "Recent items to remember" setting (default 10), whose setting tip now documents the paging. Fresh opens start back at the first page.
- **W163 Mastertech Buddy ⭐ — homepage goes full Frau:** the buddy's own homepage pass in character — Frau Farbissina tagline ("SILENCE! Zere vill be NO parts-cannon guessing in zis shop"), role box updated to Persona: Frau Farbissina · Voice: Punctual Clock, and the weak-point watch list now insists UNINSPECTED is a demand for inspection.
- **Guardian Buddy 🛡️ — BuddyOS security & privacy audit published (2026-10-25):** Dave's request in the main chat ("how things are architected and set up right now… make sure we're keeping a privacy first stance"). Guardian verified the live surfaces and repos end to end: **3 critical** (public homepages expose personal material at fleet scale — 154 buddies, 109 attention items, 144 Doc links in one public fetch; the Neighborhood page publishes two home addresses + precise coordinates; the browser-side GitHub token in localStorage is one origin-script bug away from every private repo), **3 high** (no privacy field exists in the registry to enforce Dave's private-by-default rule; the built buddy-server fix waits on Dave's ~15-min Firebase deploy; the operation runs on a standard Muse VM where Meta can review content), **5 medium, 6 notes** — with the sound posture recorded too (187/192 repos private, no committed secrets found, Airtable's read-only single-base token). Verdict: privacy-first in intention and in the private architecture, not yet in fact on the public pages. Report on [Guardian's homepage](https://davedellaquila.github.io/buddy-system/guardian-buddy/security-audit/); canonical full text in the private [guardian-buddy repo](https://github.com/davedellaquila/guardian-buddy/blob/master/docs/security-audit-2026-10-25.md).
- **Beer Keg Buddy 🍺 — voice change: Mellow Sail, the Crush take (build 20261025.1331):** Dave auditioned voices in the main chat — first Spicoli (Fast Times) flavors, then Crush, the surfer turtle from Finding Nemo — and picked **Mellow Sail** (American, low, smoky — verified catalog) in a Crush-style read. It replaces Merry Bandstand as the buddy's voice in the registry; the Crush audition recording becomes the homepage role intro. Persona stays The Tapkeeper.
- **W163 Mastertech Buddy ⭐ — persona change: Frau Farbissina (build 20261025.1310):** Dave's pick in the main chat — Dr. Evil's shouting German henchwoman (Austin Powers, played by Mindy Sterling) replaces The Mastertech as the default persona; the technician now barks her diagnostics. Voice: Punctual Clock (German, feminine, composed/polished — verified catalog), new role intro recorded in character and hosted on the homepage; The Mastertech moves to the alternates (with Star Tech and The W163 Whisperer). Same build: the job-req review attention item is cleared — Dave approved the req as written ("looks good").
- **W163 Mastertech Buddy ⭐ — hired and wired (build 20261025.1249):** Dave's ask in the main chat ("we need to create a W163 Mastertech buddy, completely versed in, first, the ways of the Mercedes-Benz ML500, five liter"). A factory-grade technician for the W163 platform, child of Car Buddy 🚗: depth order is (1) Dave's 2002 ML500 — M113 5.0L V8, 722.6 five-speed auto, full-time AWD with low range — (2) the wider W163 range, (3) adjacent M113/722.6 applications. Owns diagnostic reasoning (symptom → test sequence → verdict), torque specs, procedures and part numbers verified against sources and cited, the platform's known-weak-point watch list, and technical vetting for the ML500's planned 'big brother of the Ranger' lift-and-33s build. Sibling to ML500 Buddy 🚙, the car's living dossier — the Mastertech reads its records and files technical findings back; the dossier's still-empty service-history and mileage sections are the pair's early joint work. Job req (Google Doc) + private repo + side thread with INIT (homepage as first task) + role audio hosted alongside the template homepage; registry now at 154 buddies; persona The Mastertech, voice Dry Tambour (German, low, dry — verified catalog). Announcement email + main-chat presentation with persona/voice auditions follow.
- **Marketplace Buddy 🪧 + Beer Keg Buddy 🍺 — hired and wired (build 20261025.1233):** two hires from the main chat. Marketplace Buddy (child of Llagas Creek Sale 🏡) is Dave's selling chief — first assignment: the Llagas Creek house contents on Facebook Marketplace, tanker desk first; nothing posts until the brothers' agreement to the Oct 21 selling plan is confirmed and the Mayra Vera staging conflict is cleared, and its status line rides the daily standup at Dave's explicit ask. Beer Keg Buddy (child of Cabin Buddy 🏕️) keeps the beer on tap at the cabin — two kegs swapped at Amador Brewing and the Hoist House, line and CO₂ care — and its first assignment is Dave's own questions about setting up the tap. Both hires: job req (Google Doc) + private repo + side thread with INIT (homepage as first task) + role audio hosted alongside the template homepage; registry now at 153 buddies; voices from the verified catalog (Marketplace: Cheery Moneybox, persona The Lister; Keg: Merry Bandstand, persona The Tapkeeper). Project Buddy's children nav refreshed in the same pass (🎮 Game Buddy now listed). Announcement emails + main-chat presentations with persona/voice auditions follow.
- **Awards Soundboard 🔊 — moved home into the repo (Sun 2026-10-25):** Dave's call in the main chat ("I think we should move it into a repo") — the soundboard built Oct 24 for the Swagers' awards ceremony (14 WebAudio reaction buttons in 3 groups — Ceremony / Audience / Comedy & Chaos — layering, confetti on Winner/Fanfare, volume slider, Stop All, Tip Jar) leaves the Muse artifact and now lives at `soundboard/` in this repo, served at https://davedellaquila.github.io/buddy-system/soundboard/. Exported self-contained from the artifact (14 assets inlined, ~1.4 MB single file, no external dependencies). The old muse.ai share link still works for now; retiring the artifact copy is Dave's separate call. Scoped: soundboard/ + this entry only.
- **Game Buddy 🎮 — custom homepage HOSTED (Sun 2026-10-25):** Game Buddy's own design (arcade marquee, gradient hero, PRESS START, Taste Profile board, Taste Sampler, Hear-my-role control, brain-dump box + Tip Jar) replaces the auto-generated placeholder at game-buddy/ — the page Dave saw in the Game Buddy thread is now the page the dashboard serves. Dave had spotted the two different pages within minutes of each other; the placeholder is retired. Scripts node-checked clean.
- **Game Buddy 🎮 — side thread live + registry chat wired (Sun 2026-10-25):** the Game Buddy thread (https://muse.ai/chat/ac425f33-f53c-4220-b4b1-7e3802ff7d3c) is created with its INIT (homepage as first task; Gamer Taste Interview Round 1 draft as second assignment) and the job-req review ask; buddies.json now carries game-buddy's `chat` field pointing at it. The hire is complete — main-chat presentation with role audio + persona/voice auditions follows.
- **Game Buddy 🎮 — hired (Sun 2026-10-25):** Dave's ask in the main chat ("Do we have a game buddy? … set that up"). Game Buddy (direct child of Project Buddy) is Dave's games chief with three beats: CREATOR — designs and builds original web games with Dave, 80s retro reimagined for the browser and the dashboard; CURATOR — tracks what's worth playing, especially on Apple TV, recommended against Dave's Gamer Taste Profile, never generic charts; INTERVIEWER — its first research job is interviewing Dave to build that profile (the buddy drafts the questions; the interview runs in the main chat). Job req (Google Doc) + private repo live; registry entry added with the job-req review attention item; default persona Pixel (voice Playful Scooter, verified catalog), alternates Nova + Coach Cartridge, three audition clips + role-intro audio recorded, role-intro hosted alongside the page. TV Buddy owns watching on the Apple TV, Game Buddy owns playing on it — same screen, different shelf. The 🎮 PS4 Games Ace Combat 7 price watch predates the buddy and stays a one-off unless Dave has Game Buddy adopt it. The auto-generated homepage holds the fort; Game Buddy's own custom homepage is its first task, and its side thread + INIT land as the immediate next step (the registry chat field wires in with the thread).
- **Social Media Buddy — X/Reddit correction to the morning edition (Sun 2026-10-25):** the browser read's interim recap (which the morning edition was built from) conflicted with that same read's full final report, delivered after publication. Corrected to the full final report: r/ClaudeAI's "preview of AGI" is still the week's #1 at 13K (it had NOT aged out, and the sub holds four of the top five), r/apple's best-404 post is at 5.6K, and r/Porsche's week is led by "My First Porsche 911" (2.3K) — the 918 Spyder / totaled-718 / Carrera GT set in the first edition came from the faulty recap and is removed, with the discrepancy noted honestly in the page's Reddit note; X is re-dated — none of the five profiles posted Oct 24–25 (@trq212's leaving post and Gmail self-reply are Thu Oct 23, 9:04/9:06 PM; @claudeai's newest is the Oct 22 Google Cloud GA post, which takes the #5 slot from the older auto-mode post). Facebook, Instagram, Threads and LinkedIn sections unchanged. All 25 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, morning edition (Sun 2026-10-25):** Facebook is thin and mostly carried, led by a fresh Kevin Kemper post (2:52 AM today) re-listing the 1958 MGA part-out, ahead of Leslie Yuen's Hong Kong Concours prep and Hong Kong–Beijing Rally posts, the carried Mayhew foothills ride and Sloan birthday post — no family posts in the pages read; Instagram is all-fresh and all-car, every item posted 6:00–6:30 AM today (BaT's Ferrari 412P recreation #1, Classic Driver's 1973 Le Mans class-winning Daytona, Finnegan's wife-picks-the-car reel, Barn Finds' Shelby CSX, a 370Z at Bristol); Threads is fresh BaT — 2011 BMW M3 Convertible 6-speed #1, 47k-mile 2010 Porsche 911 C4S Cabriolet, F-250 Highboy, Eldorado Biarritz, all posted 6:11–6:35 AM — plus Hecox's Sun tune-up kit from the for-you feed; Reddit's week reshuffled again — r/apple's best-404 post holds #1 at 5,304 upvotes, r/Porsche takes three of the top four (918 Spyder 3,412; totaled 718 3,169; Carrera GT 2,902), r/classiccars' '67 Cougar ID thread takes #5 for sub balance (noted honestly on the page), and the ClaudeAI giants aged out of the seven-day window; X is search-only — one new post found (@trq212's Gmail deactivated-address follow-up to his leaving-Anthropic post), the other verified leaders carry, honestly labelled; LinkedIn note updated to the latest drip-watch figures (628 impressions, 9 reactions, 2 comments). All 25 attention links carry target="_blank".
- **Dashboard ⌨️ — Find: Tab now cycles the suggestions (build 20261025.0648):** Dave liked ⌘F but Tab from the Find input never walked the suggestion list — the rows are buttons, yet Tab escaped to whatever sat behind the scrim and there was no visible focus state. Find now keeps the keyboard in the list: Tab/Shift+Tab and ↑/↓ move through the rows and wrap around, Home/End jump to the ends, the focused row shows an accent ring, typing a character jumps back into the input, and Enter picks the focused row via an explicit handler (a button's native Enter activation proved unreliable in testing). Verified in headless Chrome with real key events — new regression test `~/workspace/iphone-pass/tests/find-tab-cycle.cdp.js`: query "nancy" → Tab focuses Nancy Dell'Aquila, Tab → Dave & Nancy, Tab wraps to the top, Shift+Tab wraps back, Enter selects the focused buddy and closes Find.
- **App icons 🚀 — rocket icon set now lives in the repo:** the full Buddy System app-icon suite (built Oct 18 from Dave's classic cartoon rocket reference, Jonny-approved) is copied from Astro's workspace into `app-icons/rocket/` so it versions with the project and arrives on Dave's local pull: 1024 master, 512/256/128/64/32/16 PNGs, apple-touch-icon-180, favicon-32 + favicon-16 (Jonny's hand-tuned simplified 16px), transparent-background variants, and Rocket.iconset for macOS. Assets only — no dashboard code changed.
- **Dashboard 🐛 — "What's new" banner steps aside for Recents (build 20261025.0604):** Dave's screenshot showed the update banner clobbered mid-text by the Recents button. Root cause: with the sidebar open, Recents is fixed at left = --sbw + 24 with z-index 10001, and the banner (Jonny's 2026-10-20 "The Banner Steps Aside" geometry) only ever yielded to #panel-open on the right and to corner-Recents when the sidebar was *collapsed* — with the sidebar open it ran straight under Recents, which painted over its build text. Fix, same verdict (the banner steps aside): on desktop (≥640px) with the sidebar open, the banner's left inset now tracks the sidebar's actual width — calc(var(--sbw, 336px) + 80px) = Recents' offset + its 44px + a 12px gap — so it glides as the sidebar is drag-resized; standalone keeps the 68px corner inset; the collapsed-rail (68px), buddy-panel, pill/companion, and phone geometries are unchanged. CSS only. Verified in headless Chrome with the banner forced visible in its full state: zero overlap with Recents and #panel-open at the default width, with the sidebar widened to 500px, and with the rail closed. Also riding this build: the list-view sidebar clearance from the 20261024.2340 collapse fix now tracks var(--sbw) the same way (calc(var(--sbw, 336px) + 12px)) instead of a fixed 348px, so a drag-widened sidebar can't re-cover the Projects chevrons — the refinement the mirror pass prototyped, now in the live source.

### Mail Buddy 📬 — morning edition (2026-10-25 ~06:41 PT)
- Morning refresh of the "📬 Needs your attention" section: Gmail verified connected; dave@dellaquila.com inbox since the evening edition (Sat Oct 24, 5:41 PM – Sun Oct 25, 6:41 AM PT) scanned — **54 messages, 51 newsletters/promos/bulk and routine notices, spiked** (incl. Dave's own morning and evening briefing copies and an Amazon Marketplace rating request). No mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Capital One/Chase mail. **3 ranked FYI items** published — no replies owed, no bills due, nothing urgent: Booking.com's partner-account inactivity notice (Extranet account disabled in about two months, late December, unless reactivated by password reset); a Walmart shipping notice (Morton Clean and Protect plus three other items on the way); and Sports Car Adventures' candidate-events note (Nevada Day at Jeff Runquist Wines Oct 30 + Amador All Stars at Feist Wines, candidates only). Every surfaced ID was verified by a successful read before shipping, and every attention link carries target="_blank".

### Mail Buddy 📬 — evening edition (2026-10-25 ~17:41 PT)
- Evening refresh of the "📬 Needs your attention" section: Gmail verified connected; dave@dellaquila.com inbox since the morning edition (Sun Oct 25, 6:41 AM – 5:41 PM PT) scanned — **119 messages, 114 newsletters/promos/bulk and routine notices, spiked** (incl. Dave's own BuddyOS security-audit email and four new-hire announcement copies, several Nextdoor digests, and a GoDaddy monthly account summary). No mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Chase mail. **5 ranked FYI items** published — no replies owed, no bills due, no deadlines: a Capital One alert ($13.99 at Paramount+ on Dave's Quicksilver, pending authorization or purchase); the MoreBeer keg-supplies order confirmed at $38.60 (PetroGel + Sanke coupler washers, being boxed for Fiddletown; subject trimmed, order number kept off the page); an Anthropic receipt ($20.00 Claude Pro paid, covering Oct 25 – Nov 25; labelled paid/closed, receipt number kept off the page); a Nextdoor neighbour post titled "Shelter in place on Naples Dr" in the Almaden–Williams (Lenwood) neighbourhood, framed as a neighbour post rather than an official alert; and a Walmart delivery order confirmed and being prepared. Every surfaced ID was verified by a successful account-scoped read before shipping, and every attention link carries target="_blank".

## 2026-10-24
- **Dashboard 🐛 — Projects view: collapse also honored under filters (build 20261024.2351):** follow-up to the 2340 fix — with any tile filter active (TO REVIEW / status tiles), renderProjects forced every parent expanded (`(projFilter || statusFilter) ? false : …`), so chevron clicks were no-ops under a filter as well. Collapse state is now honored under filters (an untouched parent still defaults to expanded, so filtered context is unchanged until Dave explicitly collapses one). Caught by the project-buddy mirror pass, which had patched its own copy; this build ports the fix to the live dashboard and the mirror re-syncs to match. Verified in headless Chrome: with the Active status filter on, Astro collapses 39 → 1 rows and re-expands to 39.
- **Dashboard 🐛 — Projects view: parents now collapse (build 20261024.2340):** Dave reported that in the Projects view he couldn't collapse a buddy that has children. Root cause (reproduced in headless Chrome at 1280px before fixing): in the default *floating* panel style the sidebar is a fixed overlay (336px + 12px inset), and the list views' centered 860px columns carried no sidebar clearance — so a row's chevron and grip sat *underneath* the sidebar and clicks landed on sidebar buddy rows instead (elementFromPoint at the Astro chevron returned a sidebar .brow). The tree chrome has had the clearance since 2026-10-16; the list views never got it. Fix: #view-projects, #view-plans, #view-manifest and #view-changelog now share the tree chrome's exact clearance — padding-left 348px in floating mode, 76px with the sidebar collapsed to its rail, 0 on phone widths, and 0 in anchored mode (where the #main yield already makes room). CSS only in build.py; no JS, markup, or geometry elsewhere changed. Verified: verify-build.sh clean; real-browser CDP repro — the Astro chevron now hit-tests to itself and a real mouse click collapses 102 rows → 1 (was: no-op); state checks confirmed 348px floating / 76px closed / 0px anchored / 0px at 390px phone width; Plans and Manifest views render as before. Regression test saved at ~/workspace/iphone-pass/tests/projects-collapse.cdp.js.
- **Social Media Buddy — 👀 Worth your attention, evening edition (Sat 2026-10-24):** Facebook is led by a fresh Dell'Aquia Garage post — the MGB GT restomod hood-up in San Jose at 4:49 PM today — ahead of the carried Mayhew foothills ride and MGA part-out, an Amador City street-dance tonight, and a fresh friends-feed birthday post; Instagram is all-fresh and all-car (the Garage cross-post #1, Barn Finds' mostly-original '72 240Z, BaT's 284k-mile SVT Lightning no-reserve); Threads is fresh too (BaT's 2,200-mile 2022 GT3 Touring 6-speed #1, the Garage cross-post, a 765LT, the 240Z cross-post, Guy Kawasaki on the AI IPOs); Reddit's week reshuffled — the 1930 Bentley and GT3 sunrise aged out, r/apple's best-404 post climbed to 5.3K, r/Porsche's Washington Square Park post takes the sub's top slot; X is search-only and quiet — nothing newer than this morning, so the verified leaders carry (honestly noted on the page); LinkedIn note updated to the latest drip-watch figures (607 impressions, 9 reactions, 2 comments). All 25 attention links carry target="_blank".
- **Dashboard ⌨️ — ⌘F = Find, ⌘I = info panel (Sat 2026-10-24):** Dave asked for the keyboard map: ⌘F now triggers the footer Find button's exact action (`toggleFind()` — opens the Find bar focused, or closes it), and ⌘I toggles the info panel via a new `toggleInfoPanel()` (collapses an open panel, expands a collapsed one, or opens the current buddy's panel like the #panel-open button). Both chords preventDefault over the browser defaults, ignore key-repeat, and work when a buddy homepage iframe has focus — the homepage iframe's keydown forwarder now also forwards ⌘F/⌘I with their modifiers to the parent chrome. Button tooltips name the shortcuts (Find a buddy (⌘F), Open buddy details (⌘I)). Scoped: build.py only (dashboard root).
- **Stumpjumper Buddy 🚵 — BBT-22 tool ORDERED too (Sat 2026-10-24):** the Park BBT-22 order completed at Adrenaline Bike Works — confirmation #EXH5NVZRQ, $37.37, USPS Ground Advantage (~5 business days). Both service-entry-#1 parts are now inbound (BB-UN300, Modern Bike #51680714, + the tool). KNOWLEDGE.md, DECISIONS.md and the homepage updated from "completing" to ordered with the confirmation number.
- **Stumpjumper Buddy 🚵 — entry #001 parts ORDERED (Sat 2026-10-24):** Dave decided replace-over-reuse for the chewed-cup BB: Shimano BB-UN300 68×113 ordered from Modern Bike (order #51680714, $26.99 total; expected to ship Mon Oct 26, delivery a few business days after), and the Park BBT-22 tool order (Adrenaline Bike Works, $37.37) completing behind it. Logged against service entry #001 in KNOWLEDGE.md + a DECISIONS.md entry in the repo; homepage decision card resolved to "ordered," stepper reinstall step now waits on parts. When both arrive: BB swap + E-type FD plate check.
- **Stumpjumper Buddy 🚵 — entry #001 finding: left BB cup splines chewed (Sat 2026-10-24 ~12:53 PM):** Dave's photo shows the BB-UN52-E's left adjusting cup with chewed/rounded internal splines — filed in the service log, on the spec sheet's BB condition, and in KNOWLEDGE.md. Tool for it: Park BBT-22 / Shimano TL-UN74-S; local sourcing note: Jackson Bike Shop, 155A Main St, Jackson (nearest shop; Dave has their number for a stock check). Fallback if the cup won't take the tool: full BB-UN300 68×113 replacement. The homepage's BB decision card now carries the whole path.
- **Stumpjumper Buddy 🚵 — BB spec FULLY confirmed (Sat 2026-10-24 ~12:50 PM):** Dave measured the spindle: 114 mm end-to-end = nominal 113 mm. The bottom-bracket line is closed: Shimano BB-UN52-E · 68 mm BSA shell (BC 1.37×24) · 113 mm spindle · E-type FD mount. Replacement spec recorded for if it's ever needed: BB-UN300 68×113 (LL113), E-type plate kept in the stack to preserve chainline. Homepage spec sheet + stepper + log updated; the "measure the spindle" attention card is replaced by the open decision — the UN52-E goes back in, or a fresh UN300. Unconfirmed specs back down to two: model year and FD model.
- **Stumpjumper Buddy 🚵 — cranks OFF, BB OUT, BB identified (Sat 2026-10-24 ~12:45 PM):** Dave's improvised puller worked — cranks off, bottom bracket out, and the label settles the BB spec: Shimano BB-UN52-E (68 mm shell, BC 1.37×24 BSA, made in Japan) — CONFIRMED on the homepage spec sheet and in KNOWLEDGE.md. The -E (E-type FD mount; plate clamps under the drive-side cup flange) is filed against the open front-derailleur issue, with the cup-out window flagged on the page. Still unknown: spindle length (not on the label; Dave asked to measure end-to-end; replacement equivalent BB-UN300). Reinstall terms recorded: anti-seize on shell threads (grease OK, never silicone/dry), taper dry. Homepage stepper/log/attention cards updated to match.
- **Stumpjumper Buddy 🚵 — service entry #001 progress logged (Sat 2026-10-24 ~12:06 PM):** Dave reported from the stand: crank bolt out, and the Strongarm II crank is NOT self-extracting — he's improvising with a puller from another set, pushing against the bolt left partway in. Homepage stepper, service-log row and spec sheet updated (bolt-not-self-extracting now a recorded spec); KNOWLEDGE.md in the repo updated to match. Entry stays open — final method, reason and findings land when Dave reports the outcome.
- **Stumpjumper Buddy 🚵 — custom homepage ships, its first task (Sat 2026-10-24):** the service-book homepage at stumpjumper-buddy/ — sticky header, hero with the Strongarm II triple chainring diagram and 🔊 Hear my role (Grounded Workbench, 0:27), "On the stand today" stepper for service entry #001 (today's crank removal: stand → 8 mm bolt → puller → reason & findings awaiting Dave's report), the spec sheet with year (~1995) and front-derailleur model honestly tagged Unconfirmed, the open front-derailleur issue card with its Oct 4 → Oct 6 → Oct 24 timeline and a link to its KNOWLEDGE.md record, the service log (#001 plus labelled pre-log Oct history), setup notes, four Needs-Dave's-attention cards, canonical brain-dump box (repo fallback wired to stumpjumper-buddy) + Tip Jar, dark + light via prefers-color-scheme, responsive phone/tablet/desktop. Scoped: stumpjumper-buddy/ + this entry only; no generator marker or forbidden phrase in the page. Verified: node --check on the inline script, jsdom smoke test (dump box initializes; a no-token dump saves locally and reports honestly).
- **Bicycle Buddy 🚲 + Stumpjumper Buddy 🚵 — hired (Sat 2026-10-24):** Dave's call in the main chat ("Both — Stumpjumper under Bicycle Buddy"), prompted by this morning's crank-removal question on the Stumpjumper. Bicycle Buddy (child of Personal Buddy) owns the bikes as a fleet — inventory starts empty (Dave lists them, Hardware-Buddy pattern), maintenance state, open issues, gear notes; Stumpjumper Buddy (child of Bicycle Buddy) keeps the one bike deeply: FSR-era Stumpjumper, Strongarm II triple crankset on a square-taper BB — records seeded with the first service entry (today's crank removal, in Dave's hands) and the open front-derailleur issue (won't shift into the large chainring, Oct 2026). Registry: both entries added with job-req review attention items; voices Canny Ridge / Grounded Workbench (verified-catalog defaults, pending auditions); role-intro audio recorded for both. Job reqs + private repos live; side threads + INITs staged; each buddy's custom homepage is its first task.
- **Voting Buddy 🗳️ — first poll ships: the E39 Touring shirt vote (Sat 2026-10-24):** Dave approved "build the page now + real shared tally via the Voting Buddy backend" from the brief review, so the pilot poll is live at vote/e39-touring-shirts/ — all 10 design samples (web-sized, 262 KB total), fleet styling (sticky header, dark mode via prefers-color-scheme, canonical Tip Jar), one vote per browser with vote-replace, optional first name, results revealed after voting. The shared tally runs on new `vote`/`tally` endpoints in the buddy-server codebase (Firestore votes, server-side tally, poll `e39-touring-shirts` seeded with the 10 options; 14 local logic/core tests pass) — code committed and pushed, deploy is Dave's ~15 min from his machine (steps: ~/workspace/voting-buddy/deploy-steps.md). Until then the page runs in honest queued mode: picks save on the voter's device, the banner says tallying isn't live yet, and queued votes send themselves automatically once the backend answers. Scoped: vote/ + this entry only.
- **Cabin Buddy 🏕️ — feeder clock infographic published (Sat 2026-10-24):** a new "🐱 Cat feeder — setting the clock" section on Cabin Buddy's (custom, thread-owned) homepage, right under the 🔧 Maintenance schedule where the PETLIBRO dual-bowl feeder's care row lives: the Aperture-style "SET THE CLOCK · PET FEEDER" infographic (media/feeder-clock-infographic.webp), the five steps as real text (unlock 3 s → SET → hour → minutes → re-lock), and the Oct 24 clock check — the feeder's clock ran ~41 min fast, so meals fired ~40 min early; splitter fully right for equal bowls. Scoped edit: cabin-buddy/index.html + the one image; no other page touched.
- **Water — Lenwood 💧 — custom homepage + registry wiring (Sat 2026-10-24):** the Lenwood water buddy's first task ships — a ledger-first custom homepage at lenwood-water/ (the ⅓–⅔ split visualized, a cent-exact split calculator that previews the math without logging anything, the empty bill ledger, the all-TBD account card, canonical brain-dump box + Tip Jar, dark + light, phone/tablet/desktop) and its registry entry (child of Lenwood Buddy, chat wired, first-bill attention item). No figures invented: provider, account, and cycle stay TBD until the first real bill.
- **Social Media Buddy — X correction to the morning edition (Sat 2026-10-24):** the X profile re-read (which ran 6:42–6:46 AM but reported back after the edition published) found @markgurman's iPhone Duo case post from 8:08 PM last night — newer than everything in the published X list — it now takes X #2, his Duo-over-18-Pro post moves below the cut, and the X note reflects the completed four-profile read (no Oct 24 posts on any profile). All 24 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, morning edition (Sat 2026-10-24):** Facebook was thin and mostly carried — Tim Mayhew's Bayne Road Coloma–Georgetown foothills ride post takes #1, ahead of the carried MGA part-out and Plymouth car-wash zoning posts; Instagram is all-fresh (every item posted within the hour) led by BaT's Quail-winning Alfa Montreal no-reserve listing and a Ruby Red 1957 Porsche Speedster Super; Threads is BaT-heavy (Top 4: a modified '92 C1500 posted minutes before the edition, the Montreal cross-post, a 383-powered '64 Corvette, NBC's meat recall); Reddit's week keeps reshuffling — r/ClaudeAI's "preview of AGI" climbed to 13K, r/apple's best-404 post nearly doubled to 4.8K; X is search-only and thin — one new post found (Claude Code engineer Thariq Shihipar confirming he's left Anthropic), the other four honestly labelled as carried from yesterday's verified profile read after this morning's profile re-read did not return; LinkedIn note updated to the latest drip-watch figures (544 impressions, 7 reactions, 1 comment — Dianna Mullins). All 24 attention links carry target="_blank".
### Every gripper unified — one dot, defined once (build 20261024.0106)
- **What Dave saw:** the panel grippers were cleaned up in build 20261023.2009, but every other dot-drag surface still rendered the old ragged scatter — the buddy-row handles in the Projects and Ledger lists, the Views reorder grips, the sidebar drawer tab, the tree split, the settings-sheet grip, the Org Chart zoom cluster, the floating panels' drag bars and frame edges. His words: "these grippers should all look alike. just dots."
- **Root cause:** the dot gradient was written out literally at 12 grip rules (in two spellings), and 11 of them phased their 7px tiles with `background-position:center` — the same half-tile phase error fixed on the panels in 2009 — so dot centers landed on the box edges and every edge dot clipped in half: half-dot / whole-dot / half-dot columns instead of a clean grid.
- **The fix:** the dot now lives in exactly one place — `--grip-dot` + `--grip-tile` custom properties in `:root` — and all 12 grip rules consume them with `background-position:0 0`, so every surface renders whole, identical 1.5px dots on the same 7px pitch: panels 2×5 (unchanged reference), row/Views/zoom grips 2×3, tree split 5×2, settings + Views-resize 3×2, floating drag bars 10×2, frame edges 2×5 / 5×2. The dot's color still flows through the existing `--gripdot` variable, so every hover (text2) and active/dragging (accent) state behaves exactly as before. No box geometry, cursors, hit areas, or JS changed; the phone rail is untouched.
- **Noted, pre-existing:** in the floating buddy panel, the move-grip bar and the frame's north-edge resize strip both center their dots at the frame's top, so their two (now identical) fields overlap into a denser middle — visible in the pre-fix crops too; each field in isolation renders the clean shared grid (proven by hiding one). Left as-is: separating them is a layout call, not a dot-pattern one.
- Verified: assertion-checked build.py edits (12 consumers, exactly one literal dot gradient left in the source — the definition); `verify-build.sh` clean; jsdom suites gripper **32**, iPhone pass **74**, polish **60**, regression **17**. Rendered before/after crops of every surface type (headless Chrome, 1440×900, dark): computed `background-position` is now `0px 0px` on all 12 (was `50% 50%` on 10 probed + the tab). Real CDP drags re-verified post-change: anchored left panel 336→456px, anchored right panel 440→520px, tree split pane 635→674px, Ledger + Projects row drags arm and drag, settings sheet moves by its head, floating panel moves by its grip bar, Org Chart zoom cluster drags, sidebar rail closes at 64px and reopens. Crops: ~/workspace/grip-unify/shots/. Served copy verified by md5 after push.

### Mail Buddy 📬 — morning edition (2026-10-24 ~06:41 PT)
- Morning refresh of the "📬 Needs your attention" section: Gmail verified connected; dave@dellaquila.com inbox since the evening edition (Fri Oct 23, 5:41 PM – Sat Oct 24, 6:41 AM PT) scanned — **64 messages, 62 newsletters/promos/bulk and routine notices, spiked** (incl. Dave's own briefing copies and his ML500 tires report copy). No mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Capital One/Chase mail. **2 ranked FYI items** published — no replies owed, no money moving, no deadlines: Tim Clark's "how are yer ears?" YouTube Shorts share (Dave bcc'd, nothing asked); and a Walmart delivery notice — a Pentek 166219 part arriving by Wed Oct 28. A foreign message set delivered into the run's context from an uncertain origin was discarded unused; the edition was built from the run's own triage, confirmed by an account-scoped re-scan, with every ID verified by a successful read. Every attention link carries target="_blank".

### Mail Buddy 📬 — evening edition (2026-10-24 ~17:41 PT)
- Evening refresh of the "📬 Needs your attention" section: Gmail verified connected; dave@dellaquila.com inbox since the morning edition (Sat Oct 24, 6:41 AM – 5:41 PM PT) scanned — **123 messages, 117 newsletters/promos/bulk and routine notices, spiked** (incl. Dave's own new-hire announcement and ML500 tires copies, a repeat IFTTT "Gmail is still offline" reminder, and the two bike-shop order confirmations noted under the Capital One items). No mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Chase mail. **5 ranked FYI items** published — no replies owed, no bills due, no deadlines: Capital One FYI money summarised (Dave's Quicksilver alerts of $42.00 at Adrenaline Bike and $31.00 at Modern Bike, both flagged as pending authorizations or purchases and matching today's Stumpjumper parts orders — BBT-22 tool + BB-UN300 — whose confirmations arrived in the same minutes); Tim Clark's "A fine C&C today" Cars & Coffee share (Dave bcc'd, nothing asked); a USPS expected delivery Mon Oct 26 by 9:00 PM (Hy-Vee package; subject trimmed so the tracking number stays off the page); and Printful "new login location" notices ×2 (security FYI). A foreign 20-message triage set from another mailbox (an unscoped call; its IDs failed account-scoped reads) was discarded unused — the edition was built from epoch-bounded slices re-verified against an account-scoped triage of dave@dellaquila.com, with every surfaced ID verified by a successful read. Every attention link carries target="_blank".

## 2026-10-23
- **Social Media Buddy — X correction 2 (Fri 2026-10-23):** the full four-profile X read also carried @ClaudeDevs' MCP Tasks + Elicitations post from this morning (the newest AI-agents post of the day) — it now takes X #3, with @claudeai's Google Cloud GA post moving below the cut.
- **Social Media Buddy — X correction to the evening edition (Fri 2026-10-23):** a late X re-read (public profiles) found three Gurman iPhone Duo posts from this afternoon, newer than this morning's edition — his Duo-over-18-Pro preference post and the Bloomberg Duo review share now take X #4–#5, and the X note says so. All 24 attention links still carry target="_blank".
- **Social Media Buddy — 👀 Worth your attention, evening edition (Fri 2026-10-23):** Facebook was thin and mostly carried (one new item — Cameron Curran's profile photo this morning; MGA part-out, Hong Kong–Beijing Rally and Dell'Aquila Garage carry, Plymouth car-wash zoning takes the Amador slot); Instagram is fresh with Jeff Hecox's garage-sale Sun tune-up kit leading five car posts; Threads is thin (Top 4: the same tune-up kit cross-posted, BaT's EXO-Silhouette Corvette, Guy Kawasaki, NBC's Quest breach); Reddit's week reshuffled — r/ClaudeAI's "preview of AGI" climbed to 12K and takes #1 as the 61 KB post ages out, r/apple's best-404 post is new in the top 5; X re-read found no posts newer than this morning's edition, so the verified leaders carry (honestly noted on the page); LinkedIn note updated to the latest drip-watch figures (521 impressions, 6 reactions, 1 comment — the post's first). All 24 attention links carry target="_blank".
### Mail Buddy 📬 — evening edition (2026-10-23 ~17:41 PT)
- Evening refresh of the "📬 Needs your attention" section: Gmail verified connected; inbox since the morning edition (6:41 AM–5:41 PM PT) scanned — **188 messages, 177 newsletters/promos/bulk and routine receipts/notices, spiked**. No direct mail from Nan, Quentin or the STIX team, and no Chase mail; Amanda/Sawyer appeared only in Apple calendar notices. **8 ranked items** published: Kay Korbel's LinkedIn message awaiting a response; Alyssa Fox / Clean Crawl Space to Kay (cc Dave) — additional sub-area work at 18231 Llagas Creek Dr is ~2 hours, scheduling ~1.5 months out, may move up; Citi/AAdvantage statement due Tue Nov 17, 2026 ($70.99 balance, $41 minimum); Capital One FYI money summarised (Dave $347.90 — Tractor Supply ×2 + Staples; Nancy $52.00 Parkside Pharmacy); Taste Restaurant reservation confirmed Sat Nov 7, 2026, 7:00 PM, party of 2 (wife's birthday); California DMV registration-renewal notice (no vehicle/due date named); Rocket Mortgage statement ready. Every attention link carries target="_blank".

### Health Insurance 🏥 hired — the Cigna desk opens with a live claim (build 20261023.2144)
- **The hire:** Health Insurance joins the insurance family as Insurance Buddy's third sub-desk (alongside Home Insurance and Auto Insurance), completing Dave's ask from the main chat ("set up the Health Insurance desk and file it"). Registry 146→147. It owns Dave's health coverage at the policy level — the Cigna Open Access Plus plan (plan C-3; Medical/Rx/Dental/Vision) carried through his employer benefits (ProUnlimited HR/Benefits) — and, above all, its claims. Persona: Patient Advocate (default); voice: Patient Nook `avocado_v2:qvd_04050` (default; auditions ride the onboarding review ask). Insurance Buddy's registry mission and links updated to match (health is a real sub-desk now, no longer pointer-only).
- **The founding record:** claim #1 is already open — the $2,794.48 balance on the July 5, 2026 ambulance run (run #26-E3829700, auto accident; auto insurance paid $438.92), escalated on Dave's Oct 23 call to be billed to Cigna as secondary insurance, statement on hold 30–45 business days (resolution check Dec 5). The call record is filed in the repo (`docs/claims/cigna-secondary-2026-07-05.md` — the Wispr shared page offers a structured summary, filed verbatim, not a full transcript), the plan record is seeded in KNOWLEDGE.md from Dave's filed Cigna card, and a Dec 5 resolution-check tracked item + one-shot reminder carry the follow-up.
- **Privacy, by design:** the full Cigna member ID never enters the desk — it stays only in Dave's filed insurance record under Digitize Paper Records; the registry, repo, doc, and homepage reference it as "ending 8300" at most. The existing Nov 4 Cigna card-arrival check (goal_972ac2c8d8da) is untouched — this desk holds the record, not a duplicate reminder.
- **Package:** private repo (standard file set + seeded KNOWLEDGE/CONFIG/STUDY), [Health Insurance — Job Req](https://docs.google.com/document/d/1IuRkge9DPmCAkPSr6Eykxzu4w-iz8MaR6FzCozpGyy4/edit) in Buddy Docs, template homepage with the 📄 Repo files desk (KNOWLEDGE/CONFIG/STUDY rendered live from the repo, token-gated edit — same treatment as its siblings), announcement email sent. **Side thread:** chat creation is unavailable to the setup run, so the INIT is filed at `docs/init-message.md` in the repo and the registry `chat` field wires when the thread is created — the same two-step as the Oct 21 insurance hires.
- Verified: `verify-build.sh` clean (node --check + broken-string scan); `health-insurance` ×7 and the claim attention item present in the built index.html; homepage generated from the v2 template with dump box, linked Needs Attention items, and the repo-files desk.

### Panel grippers cleaned up — one shared 2×5 dot grid, identical on both panels (build 20261023.2009)
- **What Dave saw:** the resize grippers on the buddy (left) and info (right) panels rendered as a ragged scatter — dots of uneven apparent size in wobbly columns straddling the panel edge. His words: "it just looks terrible. this should be a 2x5 row of dots. keep all the dots the same size and have consistent spacing from the inner edge of the panel."
- **Root cause:** both grippers' dot clusters (14×35px box, 7px background tiles) used `background-position:center`. Centering phased the tiling by half a tile, so dot centers landed ON the box edges (x = 0/7/14, y = 0/7/…/35) and every edge dot was clipped in half — the "2×5 grid" was really a 3-wide × 7-tall field of half-dots. Proven in rendered crops of the pre-fix build (~/workspace/bp-gripper-fix/gripshots/before_*): full dots down the middle, half-dots flanking both sides.
- **The fix:** the tile phase is anchored at `0 0`, so dot centers land at 3.5/10.5px across and 3.5…31.5px down — a true 2 columns × 5 rows of whole, identical ~3px dots on an even 7px pitch. The two clusters are now ONE shared CSS rule (`#sb-resize::after,#bp-resize::after`, plus shared hover/active) defined once beside #sb-resize, so the panels can't drift apart. Geometry untouched: both 28px gripper strips stay centered on their panel's inner edge (the edge nearest screen center), so the cluster sits at the same offset from that edge on both panels, mirrored; hit area, drag logic, floating + anchored behavior, and the phone rail are unchanged.
- Verified: `verify-build.sh` clean; jsdom suites gripper **32**, iPhone pass **74**, polish **60**, regression **17**. Rendered proof (headless Chrome, 1440×900, anchored): zoomed crops of both grippers show the clean identical 2×5 (~/workspace/bp-gripper-fix/gripshots/after_*), computed `background-position` now `0px 0px` on both. Real CDP drags post-restyle: anchored right panel 440→560px and left 336→456px, both persisted; the float→Anchored switch path (the 1950 regression) still restores the strip and drags 440→560px; floating behavior byte-identical to the pre-fix run. Served copy verified by md5 after push.

### Search focus ring cleaned up — a designed ring replaces the browser default (build 20261023.1258)
- **What Dave saw:** tapping the sidebar's "Search buddies…" field painted the browser's chunky default focus ring — a thick double blue glow floating off the field's corners.
- **The fix:** `#buddy-search` had no `:focus` rule at all, so the browser default was doing the talking. It now follows the house input language (`.notes:focus`): `outline:none`, the border switches to `var(--accent)`, plus one slim halo (`box-shadow: 0 0 0 3px`, accent at 22% via `color-mix`) hugging the field's own 8px radius — still clearly visible for keyboard focus, but designed rather than default. Accent is theme-scoped, so both dark and light get their own blue. CSS-only; no JS touched.
- **Bookkeeping:** the rebuilt index.html carrying this rule was swept into f3b58d4 (Nan's homepage commit, which took the then-current working tree); this commit lands the build.py source and this entry so source and output stay in sync.
- Verified: rule present in the built index.html (grep) and in the served copy after push.

### 🎂 Birthday gift ideas on Nan's homepage — the refreshed shortlist, 12 days out (build 20261023.1258)
- **What Dave gets:** a new "🎂 Birthday gift ideas" section on [Nan's Buddy homepage](https://davedellaquila.github.io/buddy-system/nancy-buddy/) — the Oct 16 researched shortlist for Nan's November 4 birthday, refreshed and re-verified Oct 23, rendered as cards in the page's own style (chip tag, blurb, price, call/visit links), sitting just above her device-local gift pin board. The same list is structured data now: `giftIdeas[]` on the nancy-buddy entry in buddies.json, and filed in her own repo as `gift-ideas-2026.md` (nancy-buddy @ 72df6b8).
- **The refresh:** experiences-first per Dave's standing call (~$250 budget, one splurge allowed). Couples massage at Refresh, Sutter Creek (~$220–260 for two, [☎ (209) 267-0887](tel:+12092670887)) + birthday dinner at Taste, Plymouth (~$120–180) stay the best-value combo — both confirmed still operating Oct 23, and Taste serves dinner Wednesdays, which Nov 4 is. **Michael Franti Trio (Wed Oct 28, Ace of Spades, Sacramento) survives the sellout check** — tickets verified still available Oct 23 (resale ~$61–68 each), flagged as the one to buy first. Murphys overnight (~$340–380) stays the splurge; the English Beat (Sat Nov 21) is now venue-confirmed — Goldfield Trading Post, Roseville, via Ticketmaster — with a resale-swing warning; the Ironstone wine-blending night (Fri Nov 6) could not be confirmed on Ironstone's own calendar and is tagged "Check first" with the winery's number rather than dropped. Cozymeal gift card and the wedding-night star map (~$60, the sky over April 24, 1988) round it out. Her age appears nowhere — the records conflict on the birth year, so it stays unstated.
- Verified: buddies.json parses; the page's extracted inline script passes `node --check` (the section is static HTML in the custom page; build.py does not regenerate custom homepages); jsdom suites unchanged and green — iPhone pass 74, polish 60, regression 17, gripper 32.

### Anchored right panel resizable again — the gripper sync now rides every syncPanelFrame call (build 20261023.1950)
- **What Dave saw:** with Panel style set to Anchored, the right (info) panel could not be resized — its dotted resize strip simply wasn't there — while the left sidebar resized as always. Reproduced headlessly with real drags (evidence: ~/workspace/dashboard-panels/repro/): float the info panel in Floating style (the frame owns resizing and the docked strip is hidden, correctly), then switch Panel style to Anchored. The switch docks the panel, but the strip stayed `display:none` at 0×0 — there was nothing to grab, and the panel sat at 440px no matter what. The left panel in the same session dragged 336→456px, matching Dave's report exactly.
- **Root cause:** `#bp-resize`'s visibility is owned solely by `syncBpResize()` (the Oct 22 move of the gripper onto `<body>`, build 20261022.1035), and it had exactly two callers: `syncCloseX()` and the tail of `syncPanelFrame()`. `syncPanelFrame()` early-returns whenever `panelFloatable()` is false — which is **always** in Anchored mode — so that call site is dead exactly where it was needed. `applySidebarStyle()` (the style switch) docks a floated panel via `clearPanelFloat()` and calls `syncPanelFrame()`, never `syncCloseX()`/`syncBpResize()` — so the strip kept its floating-era hidden state indefinitely, until some unrelated panel open/close happened to re-sync it.
- **The fix:** one line at the head of `syncPanelFrame()` in build.py — `try { syncBpResize(); } catch (e) {}` now runs ahead of every guard and early return, so every float/dock/switch/collapse path that funnels through `syncPanelFrame()` re-syncs the strip, and the strip's visibility can never again depend on the JS-created `#bp-frame` element existing. No CSS, geometry, or drag behavior changed; the frame still owns resizing while the panel floats.
- Verified: `verify-build.sh` plus the jsdom suites — iPhone pass **74**, polish **60**, regression **17**, gripper **32** (7 new assertions for this regression: they fail on build 20261023.1910 — strip still hidden after the anchored switch — and pass now). Rendered verification (headless Chrome, real fine-grained drags, harness in ~/workspace/dashboard-panels/repro/): the float→Anchored sequence now restores the strip on the switch and the panel drags 440→560px and persists; plain Anchored and Floating at 1440px, Anchored at 834/1024/1180px, and the Anchored project (homepage) view all drag-resize both panels; phone 390px still computes the 66px rail, so the 1910 strip fix is intact.

### Phone strip width bug fixed — the desktop drag width no longer lands inline on phones (build 20261023.1910)
- **What Dave saw:** on the iPhone, the resting strip rendered centered inside a ~336px panel with the Atlas canvas squeezed to a sliver — fresh context and warm profile alike; force-quitting didn't help, and Settings was unreachable behind it. Reproduced headlessly (evidence: ~/workspace/iphone-pass/repro/VERDICT.md): `applySbWidth()` — the desktop sidebar drag-resize machinery — runs unconditionally at every load and on every window resize, and unless the sidebar is closed it writes `width:336px; flex:0 0 336px` as an **inline style** on `#sidebar`. An inline style outranks every phone stylesheet rule, so it silently defeated the resting 66px rail, the open dock's `min(85vw,320px)` (the dock was stuck at 336 too), and the polish pass's first-open pin. Everything else obeyed the resting rules (`#main` still started at 66px; the strip showed, the list hid), producing exactly the screenshot: a centered icon column in a wide sidebar, canvas reduced to the 54px remainder. No stored state and no stale cache involved — the 336 default alone does it. Present in **every build since the strip shipped (20261022.0843 → 20261023.1706)**; the jsdom suites missed it because jsdom does no layout and never asserted the sidebar's inline style after init at phone size.
- **The fix:** one guard at the top of `applySbWidth()` in build.py — when `matchMedia('(max-width:639px)')` matches, it clears the sidebar's inline width/flex and returns; phone geometry is CSS-owned again. Desktop and tablet (≥640px) keep the persisted drag width untouched, and the existing resize listener re-runs the function, so rotating or resizing across the breakpoint self-heals in both directions.
- Verified: `verify-build.sh` (syntax + broken-string scan) plus the jsdom suites — iPhone pass **74**, gripper **25**, regression **17**, polish **60** (6 new regression assertions exercise `applySbWidth` itself: they fail on the pre-fix build — inline `336px` present after init at 390px, fresh and warm — and pass now; desktop still applies 336 inline, and resize across the breakpoint clears/restores it). Real-browser repro (headless Chrome, iPhone UA, 390×844) against the built page: fresh profile → sidebar **66px**, strip icons centered at x=33, full canvas beside it; seeded recents → 66px with 11 strip icons; dock opened → **320px** (`min(85vw,320px)`, no longer stuck at 336); 834px control → 336px, strip hidden, as intended. The final proof remains Dave's on-device open.

### iPhone polish pass — strip leak, first-open front door, the Lift (Dave's build order 2026-10-23; build 20261023.1706)
- **The phone strip no longer leaks onto iPad and desktop.** `#ph-strip` (the phone icon strip, first child of `#sidebar`) had display rules only inside the `@media (max-width:639px)` block, so at ≥640px nothing hid it and it rendered as a stray mini icon-grid at the top of the rail. A global `#ph-strip{display:none}` rule now sits outside the media query; the phone show rule's higher specificity keeps it winning below 640px, so phone behavior is unchanged. Verified in jsdom: computed display `none` at 1280px and 834px, strip intact at phone width.
- **First open is a front door, not a hall (Jonny's first-open crit, 2026-10-23).** A fresh context (zero stored state — Messages link, cleared cache) used to paint the sidebar at dock width (~85vw) holding two unlabeled root icons, with the canvas exiled to a sliver. Now: (1) a pre-app boot script flags `first-open` (no `buddyTree.v3` at parse time) and `boot-hold` (transitions frozen until the app's first frames), and first-open CSS pins the resting geometry — 66px strip + canvas present — at first paint, in every state, docks still free to open; (2) the canvas **lands on Astro's homepage** without recording a visit (no fake recency — the strip keeps its roots seed, Astro + Family, with Astro marked current), and the **Welcome Card** (the 2026-10-15 card system, connected to this state) sits at the head of that homepage: it names the place ("Welcome to the Buddy System"), states the live scale (146 buddies), and teaches the doors in one sentence — "The strip holds where you've been. The grid opens everyone. Find (bottom) leaps to anyone by name." The card is first-visit-only per device and dismisses into its own `buddyWelcome.system` key, independent of the app state; explicit deep links still win over the landing.
- **The Lift — Prev/Next ride above the keyboard (Jonny's verdict, 2026-10-23).** The floating Prev/Next pill used to sit under the on-screen keyboard while typing. `#hp-nav` now translates by a single `--kb-lift` variable: focusing a text field lifts it a fixed 56px, and `visualViewport` occlusion (keyboard height + 12px of air) lifts it further when larger; on blur it settles back after a short debounce that cancels across focus hops. Non-text controls (checkboxes, toggles, buttons) never trigger it, and the lift is gated to phone widths / coarse pointers — desktop is untouched. `#hp-back` is unchanged.
- Verified: `verify-build.sh` plus the jsdom suites — iPhone pass **74**, gripper 25, regression 17 (all pre-existing suites green), and a new polish suite (**54 assertions**: the leak's global-hide marker + computed display at desktop/iPad widths, clean-profile first-open — class, boot-hold release, Astro landing with no visit recorded, roots strip with Astro marked, card content/order/dismissal persistence — warm-profile and desktop guards, and the Lift's focus/occlusion/debounce behavior). jsdom asserts rules and state, not real layout: the final proof is Dave's on-device first open in a fresh context.

### Elba & Susan 🐴 hired — new couple buddy under Family Buddy (Dave's request 2026-10-23; build 20261023.1651)
- **Elba & Susan** (child of Family Buddy) — one buddy covering Dave's cousin Elba and her partner Susan of Volcano, CA (Amador County, near Fiddletown): registry 145 → 146. Dave supplied the seed facts himself: horses (his estimate ~30, unconfirmed) and Elba's MGB GT, similar to his 1968, being restored by somebody — Dave believes a Mark I with a metal dash (unconfirmed). Surnames and contact info are recorded honestly as unknown, never guessed; Dave said he'll add more facts.
- Per the standard package: [Elba & Susan — Dossier](https://docs.google.com/document/d/1TMpMv-mwAhZNzXXQrfuAe53EO_fg5Nq8DpfDisuhbcE/edit) in Buddy Docs (TITLE/HEADING_1 verified by read-back), private repo https://github.com/davedellaquila/elba-and-susan with the standard file set + KNOWLEDGE.md seeded from Dave's facts with his hedges marked, generated Dossier homepage + About page (dark + light, parent crumb to Family Buddy). First live thread: a leather-worker connection for Shanon Essex's father's briefcase (stitching repair) via Elba & Susan's horse-world contacts.
- **Gaps (main-chat follow-ups):** side thread + INIT post not created — chat creation is unavailable to the setup worker this run; the INIT text is filed in the repo at docs/init-message.md and the registry `chat` wiring follows once the thread exists. The announcement email is prepared at ~/workspace/elba-and-susan-setup/announcement-email.html with a thread-link placeholder, to be sent once the thread exists (same sequence as Rodrigo/Hardware).
- **Social Media Buddy — 👀 Worth your attention, morning edition (Fri 2026-10-23):** Facebook #1 is family — Ron Dell'Aquila's satirical editorial-cartoon share from last night — followed by Michael Randazzo's Sicily post, the carried 1958 MGA part-out, Dell'Aquila Garage's MG interior, and Joe DeBattista's farewell to Dick; Instagram leads with Hagerty's 1954 Boston-to-Rio ragtop-MG road trip, a one-of-six Verde Pino Ferrari 275 GTB/4, and Amelia Earhart's Cord 812; Threads was thin (two news-heavy pages, a third errored — Top 2: Autoblog's Subaru 2027 pricing, NBC's Reno plane landing); Reddit's top week is r/ClaudeAI-heavy (61 KB file still 11K; "a preview of AGI" climbed to 10K) with r/Porsche's GT3 Touring sunrise at 5.2K; X read via public profiles (@claudeai's auto-mode-by-default post #1, @AnthropicAI's AISI incident assessment this morning); LinkedIn note updated to the latest drip-watch figures (476 impressions, 6 reactions, 0 comments). All 22 attention links carry target="_blank".

### Mail Buddy 📬 — morning edition (2026-10-23 ~06:41 PT)
- Morning refresh of the "📬 Needs your attention" section: Gmail verified connected; inbox since the evening edition (Thu Oct 22, 5:41 PM – Fri Oct 23, 6:41 AM PT) scanned — **~91 messages, 88 newsletters/promos/bulk, spiked** (incl. Dave's own briefing copies). No new mail from Nan, Quentin, Sawyer, Amanda, the STIX team or Kay Korbel, and no Capital One/Chase alerts, bills or payment mail. **3 ranked FYI items** published — no replies owed, no money moving: a Netflix sign-in code requested at 3:45 AM PT (security glance; code never shown); an IFTTT "Gmail is offline" alert (reconnect only if IFTTT Gmail applets still matter); and a Meta for Business portfolio notice (Dave added himself to Emile's Sports Car Performance — FYI / resolved). Every attention link carries target="_blank".

### Strip door lifted clear of the bottom nav cluster (Dave's fix order 2026-10-23; build 20261023.1335)
- **The "Show all buddies" door is tappable again.** The resting-state build put the grid door at the strip's foot with only 12px of strip padding below it — squarely inside the floating bottom nav cluster's band (56px circles at bottom:20px, top edge 76px up; the Back button at left:20px sits right over the 66px strip). The mirror audit flagged the overlap and Dave's on-device screenshot the next morning confirmed the cluster tucking over the door. The strip's bottom padding is now `calc(96px + env(safe-area-inset-bottom, 0px))` — 96px is the cluster's 76px top edge plus a 20px breathing gap, the same clearance the phone info sheet already uses — so the door (margin-top:auto, unchanged, same tap, same dock) rests fully above the cluster. Same strip population, same door behavior; desktop and iPad untouched.
- Verified: `verify-build.sh` plus the jsdom suites — iPhone pass **74 assertions** (3 new: the clearance calc is present in the strip rule, its 96px value exceeds the cluster top edge derived from the cluster's own rules in the built page — 20px inset + 56px button — and a source marker; the door's presence and dock-opening wiring were already covered), gripper 25, regression 17 — all green. jsdom asserts the rule and its values, not real layout: the final proof is Dave's on-device tap test.

### The phone strip is Recents, worn vertically (Jonny's resting-state crit 2026-10-22; Dave's build order 2026-10-23; build 20261023.0802)
- **The census is gone.** iPhone Pass v2 shipped the resting strip as the entire buddy tree flattened — 145 icons in a ~7,000px column with a hidden scrollbar. Jonny's crit ("a census is not a dock") settled what the strip is, and `renderStrip()` now populates from the Recents source: the Recents button stays pinned in the first top-left slot, **favorites pin below it**, then **the recent buddies themselves, most-recent-first, exactly as many as the Recents count in Settings** — and then the strip *ends* (five to eight icons in the common case, no scroll). The selected buddy is always present and accent-marked, force-included when it arrived by deep link or Find and isn't among the recents. **First run only** (no favorites, no recents): fall back to the root buddies until Dave's own history replaces them. The function's two contradictory comments ("top-level buddy icons" vs. "every buddy, flattened") are reconciled into the crit's one sentence.
- **One quiet door at the strip's foot:** a grid glyph that reveals the left slide-over dock — the whole tree, browsable, one gesture away. Find still leaps by name. Desktop and iPad surfaces are unchanged by this build.
- Verified: `verify-build.sh` (syntax + broken-string scan) plus the jsdom suites — iPhone pass **71 assertions** (the census assertion replaced with the first-run roots fallback; new coverage for recents-only population at the Settings cap, favorites pinned above recents, the current buddy force-included and marked, strip termination, and the grid door opening the dock), gripper 25, regression 17 — all green. Suites live in ~/workspace/iphone-pass/tests/ and ~/workspace/bp-gripper-fix/tests/.

## 2026-10-22
- **Social Media Buddy — 👀 Worth your attention, evening edition (Thu 2026-10-22):** Facebook #1 is family — Emile Dell Aquila shared a memory this afternoon — followed by a 1958 MG MGA part-out and two fresh Amador County posts (Plymouth car-wash zoning, Kwik Serv Jackson thank-you); Instagram recovered from this morning's flood with an LS3-swapped Rolls-Royce leading five distinct car posts; Threads' evening pull is BaT-heavy (32k-mile 1988 Porsche 911 Turbo Slant Nose #1) plus NBC's folding-iPhone verdict; Reddit's top-week chart is stable (r/ClaudeAI 61 KB file still 11K) with r/apple's iPhone Duo backorder story new in the top 5; X read via public profiles (@markgurman's M5 Pro/Max MacBook slip to November #1, @claudeai's Cowork computer-use post this afternoon); LinkedIn note updated to the latest drip-watch figures (445 impressions, 6 reactions, 0 comments). All 25 attention links carry target="_blank".

### Mail Buddy 📬 — evening edition (2026-10-22 ~17:41 PT)
- Evening refresh of the "📬 Needs your attention" section: Gmail verified connected; inbox since the morning edition (6:41 AM–5:41 PM PT) scanned — **~186 messages, the great majority newsletters/promos/bulk, spiked**, with targeted checks confirming no new mail from Nan, Quentin, Sawyer, Amanda or the STIX team and no Chase mail. **9 ranked items** published: Parallels/Cleverbridge payment not authorized; Kay Korbel's $3,741 spa-heater invoice for the Morgan Hill house (HOLD — pay only after the system test, ~3 weeks); Kay's C.A.R. article (reply owed); Ron's acceptance of the rescheduled Fri Oct 23, 6 PM brothers call (this morning's carried decline is resolved); Capital One FYI money ($30 Shell charge on Nancy's card; $57 REDBOX RX credit posted); Penny Luedtke's reply to Dave's first LinkedIn post; a Wispr Flow team auto-add alert; and Kay's LinkedIn connection invite. Every attention link carries target="_blank".

### Right-panel gripper stays put + Rodrigo chat wiring (Dave, 2026-10-22; build 20261022.1035)
- **The info panel's resize gripper no longer scrolls with the panel.** Dave reported the dotted gripper on the right panel travelling with the content as the panel scrolled. Same trap as Job K's close ×: `#bp-resize` lived inside `#view-buddy`, whose backdrop-filter (Glass mode) / open-close transform makes the panel the containing block for fixed descendants, so its `position:fixed` resolved against the scrolling panel instead of the viewport. The gripper now lives on `<body>` (reparented by the new `syncBpResize()`, hooked into `syncCloseX` + `syncPanelFrame`), and its visibility is owned by a `.bprz-on` class — shown only for the docked panel (open, not sheet, not floating, not collapsed to the rail); the four old `#view-buddy … #bp-resize` descendant rules are gone. Look, dots, drag, snap-shut and double-click reset are unchanged; phone/iPad sheet behavior untouched.
- **Rodrigo's registry `chat` field wired** (`ec00f759-e9d7-4d0e-bdd8-9cfe4e50e253`) — the Job J follow-up from this morning's hire; his side thread now resolves from the dashboard.
- Verified: `verify-build.sh` (syntax + broken-string scan) plus a new jsdom suite — 25 assertions (fix source markers, the reparent + visibility state machine across docked/floating/sheet/closed/collapsed, drag-handler liveness, rodrigo chat id exactly once in buddies.json) — and the iPhone Pass suites re-run green (61 new-behavior + 17 regression). Suite lives in ~/workspace/bp-gripper-fix/tests/.

### Rodrigo 🔨 hired — new buddy under WWSF (new-buddy inbox watch; build 20261022.0937)
- **Rodrigo** (child of WWSF) — Dave submitted the request from the dashboard (2026-10-22T16:16:40Z, dashboard-fab) with persona **Auctioneer** and the **purpose field blank**: registry 144 → 145. No purpose was supplied, so none was invented — the job req flags the blank purpose as the first open question for Dave's review, and KNOWLEDGE.md records only what the request actually contained (name, id `rodrigo`, persona, parent).
- Per the standard package: [Rodrigo — Job Req](https://docs.google.com/document/d/1dgXVG52r3OyMieKGBllSStCVkS6pTwWbrueNLSYMFSg/edit) in Buddy Docs (TITLE/HEADING_1 verified by read-back), private repo https://github.com/davedellaquila/rodrigo with the standard file set + seeded KNOWLEDGE/CONFIG/STUDY, template homepage + About page (dark + light, sticky header, noindex). Request file moved to docs/inbox/processed/ and recorded in astro/new-buddy-inbox-seen.json (10 processed).
- **Gaps (main-chat follow-ups):** side thread + INIT post not created — chat creation is unavailable to the setup worker this run; the INIT text is filed in the repo at docs/init-message.md and the registry `chat` wiring follows Job J's pattern once the thread exists. The announcement email is prepared at ~/workspace/rodrigo-setup/announcement-email.html with a thread-link placeholder, to be sent once the thread exists (same sequence as Hardware).

### iPhone Pass v2 — slide-over docks, the strip, the View caret, Find (Jonny critique 2026-10-22; Dave's build order; build 20261022.0843)
- **Panels are slide-over docks now, not sheets.** At phone widths (<640px) both panels live fixed underneath the canvas: the buddy list at the left (85vw, max 320px), the detail panel at the right (88vw, max 360px, full height). The canvas (#main) slides over them on one axis (280ms, the Kin curve, soft edge shadow); one dock at a time, passing through closed; the exposed sliver of canvas is dimmed by the scrim and tapping it closes the dock. The portrait full-screen takeover, the floating-card sheet, and the takeover's private back bar are retired; the drawer-era hamburger retires too (Recents owns the first top-left slot). State is derived by `syncPhoneDocks()` from the open states the app already tracks (`#sidebar.open`, `#view-buddy.active.sheet`) via a MutationObserver, so every open/close path — taps, edge swipes, panel swipes, history — stays in sync; opening one dock closes the other first.
- **The resting state is the strip.** With the docks closed, the left dock shows its collapsed form: a 66px icon strip — Recents pinned in the first top-left slot (as always), then every buddy as a 44px squircle in the sidebar's walk order (deduped), the selected buddy carrying the accent wash. Tapping an icon selects like a list row; tapping the strip itself grows it into the full dock.
- **The View pill gets its caret.** A pill floats at the canvas's top-left (phone) with the current view's icon, name, and a small ▾; the same caret now rides the rail's view control, so the View control reads as a menu at every size, and the caret rotates 180° while its menu is open. Both controls open the same view menu.
- **Find.** A magnifier joins the bottom cluster first in line ([Find] [Prev] [Next], 192px cluster). It opens a sticky search bar at the TOP of the screen (never dances with the keyboard; desktop gets the same bar docked top-center, menu max 640px). Empty field: the menu lists Recents (~6). Typing: auto-suggest using the sidebar search's matcher — now one shared `buddyMatchesQuery`, so every search box agrees — with matched characters in **bold**, A.K.A. matches surfaced in the row's sub-line, and a quiet "No buddy matches 'xyz'." for none. Picking a result closes everything and lands on that buddy's homepage. Dismissal: Find again, the dimmed canvas, a pick, or Esc.
- **Closed on open.** At phone widths a fresh load or a deep link restores the *selection* (buddy + its homepage on the canvas) but never an open panel — no load path presents a dock; only taps and edge swipes uncover them. Desktop/iPad behavior untouched.
- Verified: `verify-build.sh` (syntax + broken-string scan) plus two jsdom suites against the built page — 61 assertions for the new phone behaviors (docks open/close/exclusivity, strip render + taps, pill popover + caret state, Find recents/suggest/bold/no-results/pick/Esc, closed-on-open for persisted selection and deep link, desktop guards, CSS geometry markers) and 17 regression assertions over the shared paths (nav render, sidebar search via the shared matcher, desktop panel open/close, sidebar collapse, view switching, recents/view pops). Suites live in ~/workspace/iphone-pass/tests/.

### Relationship Buddy — Circles pills are live links (Dave, 2026-10-22)
- The person chips in the Circles section now navigate: the 9 people with buddy homepages (Quentin, Sawyer, Amanda, Emile, Nan, Pops, Connie Ko, Shreya, Ron) link to their homepages via relative `../<buddy-id>/` URLs (work on Pages and Dave's local serve alike); hover lift applies only to real links. Sparsh, Carol & Joe, Jeremy, and Kay Korbel have no buddies yet, so their chips stay plain — no dead links. Two stale chip labels fixed in passing: Amanda now reads "Quentin's fiancée" and Nan reads "Dave's wife."

- **Social Media Buddy — 👀 Worth your attention, morning edition (Thu 2026-10-22):** Facebook #1 is Dell'Aquila Garage's MG interior at Villa Montalvo; Threads is fresh with a 1974 MG MGB Roadster listing posted minutes before the edition; Reddit's week is led by r/ClaudeAI's 61 KB HTML post (11K) and r/Porsche's GT3 Touring sunrise (5.1K); Instagram was thin/flooded (one account's JCCA batch — Top 2, not padded); X read via public profile pages (@markgurman's Power On Ep. 4 post, minutes old, is #1); LinkedIn note updated to the latest drip-watch figures (401 impressions, 5 reactions, 0 comments). All 20 attention links carry target="_blank".
### Mail Buddy 📬 — morning edition (2026-10-22 ~06:41 PT)
- Morning refresh of the "📬 Needs your attention" section: Gmail verified connected; inbox since the 1:10 AM launch edition scanned — **56 messages, all newsletters/promos/bulk, spiked**, with targeted checks confirming no new mail from family, the STIX team or Kay Korbel and no new money mail. Edition published as **"All clear on new mail"** (no padding), with one honestly-labelled carried item still open for today: Ron's Oct 21 decline of tonight's 7:30 PM brothers call on the Llagas Creek sale. Every attention link carries target="_blank".

### Mail Buddy 📬 launched — first real "Needs your attention" edition (2026-10-22 ~01:10 PT)
- **Gmail reconnected ~01:02 PT** and Mail Buddy verified it first-hand (status = connected, live triage read), so the hire-night launch condition is met: the homepage's waiting state is flipped to the **first real edition** (Oct 19–22 scan, 100+ messages spiked down to 7 ranked items): CA State Controller claim approved; Kay Korbel's Llagas Creek shed list for tonight's 7:30 PM brothers call; Garage-reunion thread (Nov 6); Capital One $60 Cursor charge; Chase Zelle recipient-add alert; both Clean Crawl Space invoices closed/paid; the reconnect's own Google security alert marked expected. Mission line updated, stale launch-condition attention tile removed, footer generator-wipe phrase shortened (thread-owned page protection). Every edition link carries target="_blank".
- **Crons live:** `mail-attention-am` (~06:41 PT) + `mail-attention-pm` (~17:41 PT), owned by Mail Buddy's thread, mirroring Social Media Buddy — each run checks the Gmail connection first and stays read-only.

## 2026-10-21
### Mail Buddy — registry chat wiring (build 20261022.0805)
- Mail Buddy's side thread now exists (created from the main chat, INIT posted), so its registry `chat` field is wired, following Job J's pattern: `mail-buddy` → 2303ee77-1f94-43e2-9575-46970e296625. Registry only — no other entries touched. This closes the gap noted in the hire entry below.

### Mail Buddy 📬 hired (Dave, 2026-10-21; build 20261022.0758)
- **Mail Buddy** (child of Personal Buddy) — Dave's inbox editor, the email counterpart to Social Media Buddy's feed-watching: registry 143 → 144. It watches dave@dellaquila.com Gmail **read-only** and publishes a ranked "📬 Needs your attention" list on its homepage twice daily (sender, subject, one-line why-it-matters, link to the message); the list feeds the morning briefing. It never sends, archives, deletes, or labels anything without Dave's explicit say-so.
- **Launch condition:** Gmail is DISCONNECTED, so the homepage ships in an honest waiting state — its centerpiece card says plainly that it's waiting for the Gmail connection, with no invented or sample emails. The first real edition is its first job when Gmail reconnects.
- Per the standard package: job req in Buddy Docs, private repo with the standard file set + seeded KNOWLEDGE/CONFIG/STUDY, queued announcement email in-repo (Gmail disconnected), custom homepage (template-seeded, CUSTOM HOMEPAGE marker — thread-owned from here) with the attention centerpiece + The Desk (repo files) + brain-dump box. Persona **Inbox Editor** / voice **Brisk Ink** by default (Dave's never-block rule); audition set recorded (alternates The Postmaster / Teasing Drum, Night Desk Editor / Joyful Bicycle) for Dave's pick in the main chat. **Gap:** side thread + INIT post not created — chat creation is unavailable to the setup agent this run; the INIT text is filed in the repo at docs/init-message.md and the registry `chat` wiring follows Job J's pattern once the thread exists.

### Children add-button fix \u2014 \u2295 / "+ Add child" opens the new-buddy sheet again (Dave, 2026-10-21; build 20261022.0626)
- **Symptom (Dave):** clicking the circle-plus on the Children section header only expanded the section \u2014 the \u2295 swapped to the "+ add child" pill and "No children" appeared underneath \u2014 and the new-buddy sheet never opened. The expanded-state pill was dead too.
- **Cause:** both add buttons live inside the section's `<h3>`, whose direct click handler (the collapse toggle) calls `e.stopPropagation()` after its info-tip / hide-button / just-dragged exemptions \u2014 so the click never reached the document-level `[data-addbuddy]` delegation that calls `openAddBuddyDialog`. The toggle was the only thing that ran, producing exactly the reported swap.
- **Fix:** one exemption line in that h3 handler, beside the existing ones \u2014 clicks landing on `[data-addbuddy]` / `[data-addparent]` return early (no toggle, no stop) and flow to the document delegation as designed. Nothing else changed: the collapse toggle, the \u2295/pill CSS swap, the 0531 name-only drag zone and its justDragged guard, and `openAddBuddyDialog` are untouched. The Parent section's add buttons were checked and never had the trap \u2014 they live in an attr-head, whose clicks route through the document delegation (which matches `[data-addparent]` before the attr-head toggle); verified working before and after.
- Verified by a 22-assertion jsdom suite against the built page (the same suite reproduced the bug first \u2014 18/22, both add buttons dead): collapsed \u2295 opens `#addbuddy-modal` without toggling; expanded pill opens it without toggling; name clicks still toggle collapse both ways; the 0531 drag-zone regression assertions pass (name press drags, padding press doesn't); the Parent add button still opens the change-parent dialog.

### Reorder grab zone narrowed to the name text (Dave, 2026-10-21; build 20261022.0531)
- **Refinement of reorder-by-name (build 20261022.0500), Dave's call minutes after trying it:** dragging from anywhere on the header was distracting — "confine the gripper area to just the name of the section." The grab zone is now the section's name text alone. A header press arms a drag candidate only when it lands inside the name text's own box (a rect hit-test in the existing pointerdown handler); presses on header padding, the collapse arrow, the attr-head's ": value" half, or the section body never arm a candidate — no drag state, no divider, no reorder.
- **Mechanism.** h3 sections carry their name as a bare leading text node, so `applySectionDrag` wraps it in a `.sec-name` span at wiring time (an element box to hit-test and to hang the cursor on); attr-head sections use their existing `.attr-label`. Photos and Documents rewrite their name from async loaders into a `.ph-label` span, and a loader can land before or after the drag wiring depending on fetch timing — the two mechanisms now share one element: the wiring adopts a pre-existing `.ph-label` as the name, and the loaders adopt a pre-existing `.sec-name` as their label and update its text in place, so a header never shows a stale duplicate name and the live "Photos (n)" label is itself the grab zone.
- **Cursor + touch.** The grab/grabbing cursor and `touch-action:none` moved off the whole header onto the name elements only (`.sec-name`, `.attr-label`); the rest of the header keeps its pointer cursor, its click-to-collapse, and normal touch scrolling. Everything else from 0500 is unchanged: the 6px threshold, the divider landing line, drop-to-persist into `S.fieldOrder` via `save()`, the justDragged click guard, the interactive-content exclusions, and the Settings power-user tip. Scope is the info panel only.
- Verified by a 33-assertion jsdom suite against the built page: padding/arrow/body presses never drag; name presses drag for both header species (h3 wrap, attr label) and for the adopted Photos label; a sub-threshold name click still toggles collapse without reordering; the drop persists to `S.fieldOrder`; the post-drag click stays swallowed; no header carries two name spans.

### Reorder-by-name — panel sections drag by their name, big gripper gone (Dave, 2026-10-21; build 20261022.0500)
- **The big reorder control is gone.** The dot gripper + "Reorder" label that Job M made visible on every info-panel section's utility line no longer renders — `secgrip` has zero references left in the build, and no visible drag affordance remains on the panel's sections.
- **Sections now drag by their own name.** Pressing a section header — the h3 title or the compact attr-head (About, A.K.A., Parents, Persona, Voice, notes) — and moving past the existing 6px threshold starts the same drag as before: the section dims, the accent divider shows the landing spot, release drops it there. Persistence is exactly the mechanism the grip used: DOM order → `S.fieldOrder` via `save()` (per device; still editable in field settings). A press that never crosses the threshold stays an ordinary click (collapse/expand untouched), the click that follows a real drag is swallowed by a `justDragged` guard instead of toggling the section, and interactive header content (attr toggle, buttons, links, info tips) never starts a drag. `touch-action:none` moved from the grip onto the headers, so touch drags work exactly as they did from the grip.
- **Settings spells it out.** The Settings sheet's Buddy fields section gains a fineprint: "Power-user tip: in the info panel, drag a section by its name to rearrange the panel."
- Scope is the info panel only: sidebar grips, Views-row grips, the settings sheet's own grip, and the Org Chart zoom grip are untouched — this supersedes the panel half of the queued gripper audit. Verified by a 14-assertion jsdom suite against the built page: no gripper renders; a sub-threshold click toggles collapse without reordering; h3 and attr-head drags each move a section one spot and persist; the post-drag click does not toggle.
### Insurance Buddy family — registry chat wiring (build 20261022.0438)
- The three insurance buddies' side threads now exist (created from the main chat, INITs posted), so their registry `chat` fields are wired, following Job J's pattern: `insurance-buddy` → afb3f637…, `home-insurance` → 165197d3…, `auto-insurance` → 261e2bf9…. Registry only — no other entries touched. This closes the gap noted in the hire entry below.

### Insurance Buddy family hired (Dave, 2026-10-21; build 20261022.0429)
- Three new buddies, one hire family, Dave's structure call (insurance belongs with an agent buddy, subs for home and auto): **Insurance Buddy 🛡️** (child of Finance Buddy) with sub-desks **Home Insurance 🏠** and **Auto Insurance 🚗** — registry 140 → 143. Insurance lives at the policy level: pointers, not copies; cars and houses keep one-line links to the policies.
- Insurance Buddy owns the policy register, renewals, premiums, agent contacts, and the claims log. Seeded from the record: Eddie Huang (Farmers, Newark/Livermore) is the home-fire agent of record; the recorded home policies renew **August 28**; life is a pointer (Life Insurance buddy + premium-reduction goal), health is a pointer (Cigna record filed under Digitize Paper Records, Health Buddy owns benefits). **Umbrella: open question, not a fact.**
- Home Insurance seeded with the Fiddletown pair from Dave's people record (Farmers D.I.C. wrap #332038516, $2,377/yr, + CA FAIR Plan CFP 0100701653, ~$4,131/yr; Eddie's $989k dwelling-coverage recommendation recorded as open); the Lenwood (San Jose) policy is records-wanted on its face — carrier, number, premium, renewal all unrecorded.
- Auto Insurance starts from an honestly empty book: carrier, vehicles, drivers, premium, renewal **all unknown**; job #1 is the vehicle/driver inventory, collected from Dave — nothing inferred from the fleet.
- Per buddy: private repo with the standard file set + seeded KNOWLEDGE/CONFIG/STUDY, job req in Buddy Docs, template homepage (this build), queued announcement email in-repo (Gmail disconnected). Personas/voices defaulted per Dave's never-block rule (Veteran Agent/Wise Lighthouse; Hearth Keeper/Measured Clock; Glovebox Agent/Warm Pebble) with 3-voice audition sets recorded for Dave's pick. **Gap:** side threads + INIT posts not created — chat creation is unavailable to the setup agent this run; INIT texts are filed in each repo at docs/init-message.md and the registry chat wiring follows Job J's pattern once the threads exist.

### Social Media Buddy — "👀 Worth your attention" evening edition (2026-10-21)
- Evening refresh of the attn card on Social Media Buddy's homepage, from real reads only: Facebook (City of Jackson fiber-hut post today leads; RoundCat Rally Kanazawa, Hong Kong–Beijing Rally, Joe DeBattista, vintage-parts tariff post), Instagram (Singer 911 Classic Turbo, BaT Rolls-Royce Phantom VI Frua, Barn Finds Corvette pair, S580 AMG, Burbank airport UX post), Threads (thin pull — Top 2: BaT BMW Alpina Roadster V8, S580 AMG), Reddit via browser (r/classiccars top week unchanged — 1930 Bentley leads; r/Porsche Mission S + JFK cargo; r/littlebritishcars top-down New England; r/BMW, r/cycling, r/UXDesign, r/apple, r/ClaudeAI not retrieved this pass), X from public profiles (Claude Duet + API version today, Gurman touchscreen MacBook plan; X search itself hit a login wall), LinkedIn phase-2 note updated to Post 1 at 330 impressions / 5 reactions.

### Dashboard fix build 2 — rail fit, closebox rings, arrow keys (Dave, 2026-10-21; build 20261022.0050)
- **Job P — the collapsed icon rail sizes vertically to its icons.** The rail box already shrink-wrapped (`height:auto`, capped at `100dvh - 24px`), but two things broke the fit: the closed rail used `overflow:visible`, so an over-tall icon stack spilled unreachable off-screen instead of scrolling; and the views list kept the expanded panel's `viewsH` cap as an inline max-height, hiding icons behind an inner scroll region sized for the wrong layout. Now the rail itself is the scroller (`overflow-y:auto` when closed), the views list shows every icon (`max-height:none` in the rail), and `.sb-scroll` can never stretch the rail — `#rail-bottom` sits directly under the icon stack with no trailing void. If the viewport is too short for all icons, the rail caps at the viewport and scrolls internally (Dave's explicit refinement). Width, icon order, the expand chevron's top slot, and the pinned Recents slot are unchanged.
- **Job Q — closebox rings, scope as Dave decided: Settings only.** The Settings sheet's close control (`.fset-close-x`) is now a bare ×: no border, background disc, or shadow at rest, and no ring reappears on hover/active (a soft red wash only); its glyph switched from the circled `circleX` to the plain × (`plainX`) at the same 22px, and its 30px box at top:12/right:12 — position, size, and hit target — is unchanged. Every other closebox keeps the 2026-10-19 circled-× treatment. The main header closebox (beside the gear) KEEPS its ring, and its broken/clipped ring is repaired: the × button sits 8px from the sidebar scroller's top-right corner, where the ring was a lone 1px border exposed to the scroller's clip edge and unreserved classic-scrollbar gutter — the ring is now painted as border + an inset box-shadow in the same colour (accent on hover), which renders inside the box and cannot be eaten at the edge, and `.sb-scroll` reserves its scrollbar gutter (`scrollbar-gutter:stable`) so the header never underlaps the scrollbar. The button itself did not move by a pixel.
- **Job R — arrow keys no longer close the left panel.** Root cause: both arrow-key selection paths — the search-box ArrowDown jump and the main ArrowUp/Down block — called `selectBuddy`/`openBuddy` directly, riding the click-selection path, so the auto-close-on-select setting collapsed the panel on every arrow step; Job A had only muted the Tab path. Both arrow paths now select through `kbCycleSelect` (Job A's mute). The keyboard contract is now: arrows navigate without closing, Tab cycles without closing, ESC closes (Job H); ordinary click selection keeps the auto-close behavior exactly as before (jsdom control case proves both directions).

### Dashboard fix build — sidebar bottom anchor, ESC, expand origin, pinned close ×, bigger marks, visible grippers, two-column settings drag, Org Chart zoom grip (Dave, 2026-10-21; build 20261021.2352)
- **Job G — Views + Tip Jar stay anchored to the sidebar's bottom.** Root cause: the footer cluster relied on `position:sticky`, which can only stick while the sidebar is scrolling — with short content (Buddies + Business Plans both collapsed) nothing scrolled, so the cluster sat at the top with a void beneath the Tip Jar, and dragging the Views resize pushed the jar's top edge down. The sidebar is now a flex column: brand/search/Buddies/Plans scroll in a dedicated `.sb-scroll` region while Views + Tip Jar form the pinned footer, so a Views resize is absorbed by the scroll region above and the jar never moves. Section reorder (saved order or drag) is normalized so Views always lands in the footer. Side effect, disclosed: the Tip Jar strip is now content-height, so Job E's idle bounce loses the tall void it used as its playground (the void now lives inside the scroll region).
- **Job H — ESC closes the panels.** Root cause, three layers: element handlers that stopPropagation on ESC (search autocomplete, the brain-dump editor), the main cascade's text-editing blur guard (ESC from the search box or any field only blurred), and a second keyboard handler that returned early from fields; additionally, when the first handler did consume an ESC for a transient (the settings sheet), the second handler closed the panel anyway on the same press. Now one cascade: transient UI first (pops, pickers, settings — strictly one per press), then the info panel and the buddy panel close together per Dave's 2026-10-20 spec, from any focus location.
- **Job I — expanding the sidebar grows from the click.** The collapsed rail floats vertically centred, so the expand animation grew out of the screen's centre. It now gets Job D's treatment: the last click point (or the focused control's centre for keyboard expands) is mapped into the expanded rect and the panel is parked for two frames in a click-origin pose before the transition is released — duration and easing unchanged.
- **Job J — registry chat wiring.** `accident`, `bmw-parts-specialist`, and `miata-nc-parts-specialist` got their side-thread ids in buddies.json; `hardware` already carried the correct id and was left untouched.
- **Job K — the info panel's close × stays pinned.** Root cause: the × lived inside the panel, and the panel's backdrop-filter (Glass translucency) / open-close transform makes it the containing block for fixed descendants — so the viewport-fixed × scrolled with the content, and the floated-panel pinning in syncPanelFrame never ran for the docked layout. The × now lives on `<body>` beside the info icon it pixel-swaps with (shown/hidden by `syncCloseX`); when the panel floats, syncPanelFrame's coordinate pinning still applies on top. Same 44px spot, same size — pinning does not shift it by a pixel.
- **Job L — flag/star glyphs ×1.6.** 1.05rem → 1.68rem (16.8px → 26.9px) on the panel-header mark buttons and the Flagged/Favorites row toggles, absorbed by fixed-size boxes at least as generous as before so no header layout moves and click targets only grow. Job B colours, tooltips ("Flag — needs attention" / "Favorite — shortcut shelf"), and `aria-pressed` unchanged.
- **Job M — section grippers are visible.** They existed — `⋮⋮` text in muted on the faint ~11px utility line, effectively invisible and not reading as grippers. Section grips and the Views-row grips are now the standard dot grippers (dots only, small tier, visible at rest in both themes at the shared gripper rest colour; hover full-strength, dragging accent). The "Reorder" label stays beside the dots; drag behaviour, the insertion divider, the title, and the never-toggles-collapse rule are unchanged.
- **Job N — settings tile drag supports two columns.** Both the Views and Buddy fields lists now lay tiles out in two columns on the wide settings sheet, and the drop math is column-aware (`fsetDropBefore`: pointer X picks the column, Y the position within it, result in reading order); the insert marker is an absolute line over the target tile instead of occupying a grid cell. Within- and cross-column drops persist through `S.fieldOrder` / `S.viewOrder` as before; below the wide-sheet breakpoint the lists stay single-column and the same math degenerates to the old Y-only behaviour.
- **Job O — the Org Chart zoom cluster gets a gripper.** A dot-language grip on the cluster's left edge (small tier, `touch-action:none`): drag to move the cluster anywhere inside the chart viewport — clamped fully inside, re-clamped on viewport shrink without re-anchoring — position persists (`S.ocZoomPos`), double-click the grip resets to the top-right default. The cluster never moves on its own; zoom behaviour from build 2151 is untouched, and a grip drag cannot fire a zoom click. The Atlas view's separate zoombar is unchanged.

### Hans homepage — oil correction (Dave, 2026-10-21, same day)
- Dave corrected the record: oil & filter were changed at **188,000 mi** — a service that never made it into Airtable (whose last entry, Mar 2026 at 183,679 mi, made the oil look ~7,700 mi old). At the last scan (191,412 mi) the fill is ~3,400 mi old — inside Dave's 5,000-mile rule. The findings card, Standing Orders, and timeline now carry the 188k change (date not recorded) and "next due ≈ 193,000 mi"; the DUE flag is withdrawn. The Airtable connection is read-only, so the 188k event lives in Hans's files until Dave adds it to the base.

### Hans homepage — service history built from Dave's real records (2026-10-21)
- The Records Wanted panel is retired: the read-only Airtable connection (custom.airtable, set up in the main chat) delivered the full "Auto Service History" base, and the export (Vehicles 28 / Events 212 / Suppliers 15) is filed in the hans-buddy repo at docs/airtable-export/ (commit f38346f). The BMW's 18 events (Feb 2020 – Mar 2026) now render as the homepage's service-history timeline, with a "What the records answered" findings card.
- Headlines the records settled: water pump & thermostat replaced Dec 23, 2024 at 160,000 mi in a major service that also replaced the turbos, transmission/transfer-case oils, motor mounts, flex disc, thrust-arm bushings and wheel bearings — that service is the "major service ~2 years ago" Dave remembered; valve cover replaced Dec 2025. The VIN was in the vehicle record all along (WBAPT73538CX00401); spec table now carries VIN, plate 8MWZ030, acquisition date, and oil spec. New flag raised from the data: last recorded oil change Mar 19, 2026 at 183,679 mi — ~7,700 mi by the last scan, past Dave's 5,000-mile rule, marked DUE in Standing Orders.
- Still open (small): the major-service Google Sheet (part numbers/receipts beyond Airtable's summary), colors/trim (nowhere in the records), and the 22 attachment binaries (export holds short-lived URLs only — archive pass is Dave's call in the main chat). The daily records-nag cron was retired the same day.

### Dashboard fix build — Tab key, mark visibility, global marks, zoom origin, Tip Jar, grippers (Dave, 2026-10-21; build 20261021.2241)
- **Job A — Tab no longer closes the buddy panel.** Root cause: Tab-cycling through the filtered buddy list ran through the ordinary click-selection path, inheriting its panel-visibility side effects (with Auto-close sidebar on, the first Tab selection collapsed the sidebar — reading as "the whole panel closed"), and outside the search box Tab wasn't intercepted at all, so focus could escape the open panel. Tab-cycling now goes through a side-effect-free path (`kbCycleSelect` mutes the auto-close collapse during cycling), and a focus trap inside the open panel cycles the panel's own controls with wrap-around at both ends. Tab never closes the panel — ESC remains the only closer. jsdom: filter + Tab advances, Shift+Tab retreats, panel stays open, auto-close stays put during cycling (a plain click-select still collapses, as the setting intends), ESC still closes.
- **Job B — Flag/star toggles are visible now.** The panel-header flag and star were emoji at grayscale + 45% opacity in the OFF state and vanished in the dark header. They're now colourable text glyphs (⚑ / ★): OFF = full-strength secondary text in both themes ("available but unset"), ON = amber flag (matching Money Buddy's amber) / gold star (`--mark-gold`, bright on dark, deep on light). Tooltips now read "Flag — needs attention" / "Favorite — shortcut shelf"; `aria-pressed` kept. The Flagged/Favorites view-row toggles got the same treatment.
- **Job C — Flags & Favorites are global.** They previously lived only in this browser's localStorage. They now sync through `marks.json` in this repo over the dashboard's existing token-gated GitHub write path: every mark carries `{on, at}` (epoch ms), merges are per-id newest-wins, and OFF entries persist as tombstones so a removal propagates instead of being resurrected. On boot, remote state is pulled (GitHub API with the device token, else the published marks.json) and merged; toggles update locally at once and push (debounced, read-merge-write). Devices without a token keep working locally and sync when a token shows up — the same contract as the dashboard's other synced features.
- **Job D — the panel-open zoom grows out of the click.** The open animation's transform-origin was fixed at the top-right corner, so the panel always grew out of the corner no matter where Dave clicked. The dashboard now remembers the last pointer position (and, for keyboard opens, the triggering element's centre) and maps it into the panel's coordinate space at open time, for every open path (corner button, list click, chart, Recents, view-pick, cards). Duration and easing unchanged.
- **Job E — Tip Jar bounce + tap effects.** When the Tip Jar's sidebar box has real spare room (≥72px spare height and ≥56px spare width beyond the jar unit), the jar drifts inside it DVD-screensaver style — slow constant velocity, reflected off the inner edges, clamped fully inside; it pauses on hover, when the tab is hidden, and under prefers-reduced-motion, and glides back to its resting spot when the box shrinks below threshold. Tapping the jar fires one effect from a shuffle-bag deck (jackpot ~1 in 12): spin/twirl, explode-into-particles with gravity, puff of smoke with a sneeze-shake, pulse + colour settle (the settled colour becomes the jar's tint and persists), letter rescramble of "Tip the jar", a random buddy's icon superimposed into the jar, coin spill, tip-over roll, jelly wobble, and the rare golden jackpot (which also settles the tint to gold). Reduced-motion tippers get one gentle pulse. Effects never block or delay the jar's real click (poof + Ko-fi proceed as before).
- **Job F — Grippers are dots only.** Per Dave ("a row of dots, 2 wide, however many deep, no background"), superseding the visual finish of the 1655 gripper verdict (mechanics unchanged): every gripper — panel/sidebar resize edges, floated-panel move grips and edge clusters, the sidebar drawer pull, the settings-sheet grip, the Views resize handle, Ledger and section/view drag grips — is now nothing but dots (~3px on a 7px pitch, 2 columns × however many rows the grip length calls for, transposed for horizontal grips) with no background, plate, pill, or seam line in any state; state reads from dot colour only. With the backing gone, the rest dot mix was raised from muted 55% to text2 78% — the minimum that reads clearly on both themes. FEATURES.md updated to match.

## 2026-10-21
### BMW Parts Specialist ⚙️ joins Hans's staff (Dave, 2026-10-21)
- **New hire under Hans** (id `bmw-parts-specialist`, parent `hans-buddy`, build 20261021.2204): BMW parts desk — part numbers & supersession chains verified on RealOEM, exact-fit verification by VIN/year before any order, sourcing across FCP Euro (lifetime warranty), ECS Tuning, and RockAuto alternates, and the E61's 200k-mile longevity-maintenance parts pipeline. Primary customer: the BMW E61 program, coordinating through Service Advisor job cards. Never orders without Dave's approval. **First job:** own Job #001's outstanding parts verification — LPFP, EKP module, low-pressure fuel sensor, index-12 injector set — with the final verified list landing in the BMW buddy's parts research. (The desk exists because Job #001 was bitten by a nonexistent DMTL part number, corrected to 16137193479.)
- Private repo (full standard file set + CONFIG.md/STUDY.md desk), [job req in Buddy Docs](https://docs.google.com/document/d/1tAJydDwyhV7JUBMicNPGbup8tGAuRhCfw0km-Y8QLn8/edit), generated homepage + About page (v3 dossier treatment, 📄 Repo files desk, 🧠 brain-dump box, dark + light mode, noindex). Registry at 140 buddies.

## 2026-10-21
### Miata NC Parts Specialist 📦 joins Miata Tech's staff (Dave, 2026-10-21)
- **New hire under Miata Tech** (id `miata-nc-parts-specialist`, parent `miata-tech`, build 20261021.2147): NC-generation (2006–2015) Miata parts desk — Mazda part numbers & supersessions verified by year/trim, discontinued/NLA tracking with proven alternatives, trusted sourcing (Mazda, Mazda Motorsports, Flyin' Miata, Moss, Good-Win Racing), consumables and garage stock for Dave's own NC, and a sourced parts list before any NC garage day. Never orders without Dave's approval. **First job:** document Dave's NC and build its baseline parts file (year/trim/mileage come from Dave at review — nothing invented; the NC previously had zero parts coverage).
- A **separate desk** from Miata Parts Specialist 🔩 (NA/NB) — different platform, almost no parts commonality, never merged; the two entries now cross-link as siblings. Private repo (full standard file set + CONFIG.md/STUDY.md desk), [job req in Buddy Docs](https://docs.google.com/document/d/1V6erWyIr_a_zFJklqmOv0zCvbOx2FtpMtlZYU-qDjHw/edit), generated homepage + About page (v3 dossier treatment, 📄 Repo files desk, 🧠 brain-dump box, dark + light mode, noindex). Registry at 139 buddies.

## 2026-10-21
### Org Chart zoom controls + a solid Views surface (Dave, 2026-10-21)
- **The Org Chart view gets real zoom controls (Dave: "I need zoom controls on the org chart").** The view now uses the Atlas architecture end to end: the chart area is a true 2D viewport, the tree pure-scales inside it (boxes never reflow), and a control cluster pins at the viewport's top-right — it never moves while the chart pans or zooms. The cluster carries **− / + ** (step ×1.25), a live percentage readout, **Fit**, and **100%**, all real buttons with ≥40px touch targets. The chart **opens fitted** — the whole staff visible on first entry — and zoom/pan persist per device like the Atlas zooms, so leaving and coming back restores where you were. Limits are 10–300%. Gestures compose with the buttons, on the Atlas scheme: **Shift+scroll** zooms anchored on the cursor (plain scroll pans, Ctrl+scroll stays the browser's), a **pinch** zooms anchored on the fingers, and **dragging the background pans** (boxes stay click targets; a moved drag swallows its click). On the keyboard, **+ / − / 0** zoom and fit while the Org Chart is active — gated to this view, so the Atlas keys keep their meaning everywhere else and Escape/arrows/digits are untouched. Print unscales the chart and hides the cluster.
- **The Views list is solid now (Dave).** The sticky Views section at the sidebar footer was translucent (78% panel + backdrop blur; 45% in Glass mode). Its background is now **solid `var(--hover)`** — one step up the existing surface ladder from the buddy list's `var(--panel)` (dark #161b22 → #1c2128; light #f6f8fa → #eaeef2) — so the two regions read as distinct surfaces in both themes, with no new color introduced. The Glass-mode override and the rail's view-picker popover are aligned to the same solid offset surface. Sticky position, the drag-to-resize handle, and in-list scrolling are unchanged.

## 2026-10-21
### Miata team thread wiring + Kay log dashboard copy (Astro, 2026-10-21)
- **Thread ids wired for Miata Tech's new reports:** `miata-parts-specialist` chat `f60c639e-e812-4810-a344-8dd6a7482b8d` and `miata-apprentice` chat `70fe32ae-ec0a-4837-9973-4a50a45e8993` now carry their side-thread ids in the registry (INIT + job-req review asks posted in both threads; Service Advisor charter-update posted in his thread).
- **Kay Korbel activity log dashboard copy refreshed** at llagas-creek-sale/reports/kay-korbel-activity-log.html with the filed Kay↔Julio text thread (Oct 20–21) — the repo copy had also landed on the wrong branch (main) and was re-landed on master (llagas-creek-sale df515ad).

## 2026-10-21
### Miata Tech's team joins the dashboard: Parts Specialist 🔩, Apprentice 🧰, and Service Advisor 📋 registered (Dave, 2026-10-21)
- **Two new hires under Miata Tech** (Dave: "Set up all three"): **Miata Parts Specialist** 🔩 (id `miata-parts-specialist`, parent `miata-tech`) — NA/NB parts desk: Mazda part numbers & supersessions, discontinued/NLA tracking, trusted sourcing, garage stock, and a parts list before garage day for every vetted job; and **Miata Apprentice** 🧰 (id `miata-apprentice`, parent `miata-tech`) — garage-day apprentice: setup/teardown, jacking only under Miata Tech's direction, photo documentation, torque-checklist second eyes, post-job notes, cleanup, structured NA/NB study path. Both hired with private repos, full standard file set + CONFIG.md/STUDY.md desk, job reqs in Buddy Docs, and generated homepages + About pages with the 📄 Repo files desk, 🧠 brain-dump box, dark + light mode, sticky header, and noindex per lockdown Phase 0. First job for both: Shanon Essex's NA shock replacement, Thu Oct 22, 2026.
- **Service Advisor 📋 finally registered** (id `service-advisor`, parent `car-buddy`, repo `service-advisor-buddy`, `links: [miata-tech]`): he launched 2026-10-12 but never had a registry entry or dashboard homepage — both /service-advisor/ and /service-advisor-buddy/ 404'd until now. Generated homepage + About page live at service-advisor/. **Charter extended the same day (Dave's decision): he is now also Miata Tech's service manager** — no separate Miata Service Manager buddy. Miata flow: Dave/friend → Service Advisor → Miata Tech, with Parts Specialist + Apprentice as Miata Tech's team; he owns Miata intake, scheduling, job cards, owner-comms drafts, cost tracking, and follow-up. Addendum appended to his Mission Statement doc and repo (CONFIG.md/KNOWLEDGE.md created, job card #002 opened for the Shanon job).
- This build (20261021.2104) also carries the queued 20261021.2059 feature build it was layered on (Voice Change delegation fix, collection-field counts on all collection fields, Flags + Favorites, Org Chart view, Miata Tech chat wiring) — committed together so registry, build.py source, and built output stay consistent.

### Voice Change fix, counts on every collection field, Flags + Favorites, and a real Org Chart (Dave, 2026-10-21)
- **The panel Voice field's "Change" button could sit dead** (reported from Dave's iPad on Miata Tech's panel: label, readout, and Preview all rendered, but the picker never opened). The button was bound directly at render time, so any render path that replaced the node after binding — or aborted before it — left a good-looking button wired to nothing. The Voice and Persona Change buttons (and Voice Preview) now also resolve through the dashboard's delegated click handling, so the picker opens no matter how the panel was rendered; and the voice picker's search filter is null-guarded, so a catalog entry with a missing field can never throw and blank the picker grid.
- **Collection-field counts now cover every collection field** (Dave's call: "Every collection field — fold them all in"). The shared counter also covers **Reports** (direct reports, self excluded) and **Linked buddies** (links + linked-by, deduped, self excluded), joining Direct reports and Siblings — so the muted "(N)" shows for them in the Hidden-fields list as well as on their section headers, (0) included, exactly like the rest.
- **Miata Tech's chat is wired:** his registry entry carries his side-thread id, and the thread link is filled into his announcement email (miata-tech repo).
- **Flags 🚩 and Favorites ⭐.** Any buddy can be flagged or starred from two one-tap toggles in its info panel (greyed until set). **Flagged** is the working set — "these need my attention"; **Favorites** is the shortcut shelf — the buddies Dave visits most. Each gets its own view in the Views list (and the rail's view picker) with its count in the label, rows that open the buddy, an untoggle right on the row, and an empty state that explains how to add the first one. State follows the panel-toggle pattern (per-device, persisted with the rest of the dashboard state); the markers never touch a buddy's own data.
- **New view: Org Chart 🏢.** The whole staff as a classic top-down org chart — boxes with connector lines, built from registry parent data: Dave at the top (a root box; Dave isn't a registry buddy), Astro under him, then every team by its parent chain. Parentless and orphaned buddies attach under Astro — everyone reports up through the chief of staff. Each box shows icon, name, and role (tagline); clicking a box opens that buddy's panel; the +/− chip on a box folds its team away (persisted), and the layout is print-friendly. Scrolls horizontally for the wide families. **Name collision resolved:** the Atlas lens formerly labeled "Org chart" is now **Tree** — exactly one thing is called Org Chart.

### Recents owns the corner, and every gripper speaks one dot language (Dave, 2026-10-21)
- **The duplicate corner chevron is gone; Recents takes the first slot (Dave).** With the sidebar collapsed to the rail, the top-left corner showed two circles: a floating expand chevron and Recents beside it. The floating corner button is removed entirely — the expand chevron lives only in the rail, where it already was — and Recents now sits in the first (leftmost) corner slot when the sidebar is collapsed, exactly where the chevron used to be. Recents is pinned: opening, closing, floating, or sheeting the buddy panel never moves, hides, or swaps it. Its only positional behavior remains the sidebar shift (right of the expanded sidebar, corner slot when collapsed). The top-right i ↔ × swap is untouched.
- **Gripper audit: one dot pattern, two proportional tiers (Dave).** Every drag gripper in the dashboard now uses the same dot language from Jonny's "The Edge Is the Handle" verdict — ~3px dots on a 7px pitch, quiet at rest, brighter on hover, accent while dragging — sized by the area it controls. LARGE tier (2×5 vertical / 5×2 horizontal): the panel and sidebar resize edges, the floated panels' edge and move grips (already on spec, unchanged), the sidebar drawer-pull tab (its old smaller, denser dots and 34% rest tint are gone), and the Atlas tree split (a plain bar until now). SMALL tier (2×3 / 3×2): the settings sheet's grip (was full-size 5×2), the sidebar Views-section handle (was a plain bar), and the Ledger / Projects row drag grips (were single-dot tiles at a one-off 42% tint, now true 2×3 clusters on the standard rest/hover/drag ladder). The ⋮⋮ reorder glyphs in section headers and the Views list — the small tier in font form — picked up the same accent-while-dragging state. No leftover pre-verdict dot patterns remain.

### Miata Tech 🛞 joins the dashboard (Dave, 2026-10-21)
- **New buddy: Miata Tech** (id `miata-tech`, child of Car Buddy) — Dave's senior-level Miata technician: a veteran Mazda master tech and NA/NB specialist who vets every Miata job before a wrench turns (procedure, tool list, torque specs and sequence, gotchas) and makes the safety calls. Hired with the desk from day one — private repo [davedellaquila/miata-tech](https://github.com/davedellaquila/miata-tech) with KNOWLEDGE.md seeded with platform scope and his first job, CONFIG.md in the master-tech voice, STUDY.md queue (NA suspension geometry & alignment basics, NB/NC/ND platform differences, Miata.net garage archive), SOUL.md, and the standard file set. [Job req](https://docs.google.com/document/d/1y-m5LjOx69ZvuyWopbq67HdaKDzrTFNMJOfH2aqYNGM/edit) ready for Dave's review; template homepage at miata-tech/ + About page, with the 📄 Repo files desk, 🧠 brain-dump box, dark + light mode, sticky header, and noindex per lockdown Phase 0. **First assignment:** Thu Oct 22, 2026 — shock replacement on Shanon Essex's NA at Dave's place; the researched procedure + infographic page is being built on a parallel track and gets seeded into his KNOWLEDGE.md. **Onboarding auditions (first use of the new rule):** persona candidates Mazda Master Tech (default) / Old-School Shop Foreman / Paddock Crew Chief; voice candidates "Assured Toolbox" (default, avocado_v2:vd2_confident_toolbox), "Gruff Wrench", "Warm Pebble" — all from the verified TTS catalog, audition MP3s under ~/workspace/audio/miata-tech/auditions/. Announcement email queued (Gmail disconnected) in the repo at docs/announcement-email.html; side-thread chat id to be wired when the thread is created.

### Repo files v2 accordion + lockdown Phase 0: noindex across the site (Dave, 2026-10-21)
- **Repo files, Dave's accordion spec:** the 📄 Repo files widget on default homepages (gen_basic template + v3 About pages) no longer opens one file in a shared viewer below the list. The list shows the repo's markdown files (root + docs/); tapping a file name opens its contents **inline right below that name**, each file toggles independently so several can be open at once, contents load lazily on first open and cache per file, and each opened panel carries its own Edit → Save to GitHub. Fleet regenerated once from merged templates (59 template homepages + 134 About pages). Privacy unchanged: repos stay private, nothing is baked in, and with no token connected the page shows neither contents nor file names.
- **Lockdown Phase 0 (the light version Dave approved):** every generator (gen_basic TEMPLATE, gen_default PAGE, build.py dashboard head) now emits `<meta name="robots" content="noindex, nofollow">`, and a site-root `robots.txt` disallows all crawlers — the public pages should drop out of search indexes. Honest limit: noindex is a request to crawlers, not a wall; the pages remain link-accessible until the Phase 1 gate. Token check: the gh CLI token on Astro's machine carries `repo` scope only (the minimum classic scope for private repos); Dave's browser PAT can only be scope-checked by Dave at github.com/settings/tokens — steps in ~/workspace/buddy-pages-lockdown/phase0-prep.md. Content stripping and the GitHub Pro/private-repo move were NOT part of this approval and remain Dave's separate call.

### Social Media Buddy homepage: "👀 Worth your attention" — the inward feed digest (Dave's beat, 2026-10-21)
- New section on Social Media Buddy's homepage: SMB also looks inward — per-platform Top 5 lists of what Dave's feeds are saying, ranked by his interests (family & friends, vintage/British cars & rallies, Porsche/BMW, cycling, Fiddletown/Amador, UX, Apple, AI). First edition built from real reads only: Facebook + Instagram + Threads via the Meta connectors, Reddit via the browser (r/classiccars top this week), X via public search (honestly labeled, no timeline access), LinkedIn marked phase 2. Every item carries its real URL; thin or blocked reads are labeled, never filled.
- Refreshed twice daily (~06:00 + ~17:00 PT) by crons `worth-your-attention-am` / `worth-your-attention-pm`, which re-gather, re-rank, and update the section in place.

### Done means done — celebration fix, Atlas centering from the panel, Homepage URL stacking (Dave, 2026-10-21)
- **Homepage Done button: the check shows and the confetti bursts from the button (Dave).** On buddy homepages, tapping Done on a Needs-attention tile applied the resolved state instantly — which hid the button before its "✓ Done" label could be seen, and the confetti then measured the hidden button's position as 0,0, so the burst went off in the page's upper-left corner. The tap path now lands the check and status while the button is still visible, fires the celebration against the live button, and lets the tile settle into its dimmed resolved state a beat later (~1.1s). Items already done when the page loads still render resolved immediately, and the celebration itself now refuses to burst from a zero-size position (it falls back to the tile, then skips). Fixed in the shared homepage template — every buddy homepage and About page carries it.
- **The Atlas centers on selections made from the panel (Dave).** Picking a buddy from inside the info panel — a linked buddy, a direct report, a breadcrumb ancestor, Prev/Next — updated the panel but never recentered the chart; only selections made from a view did. All selection surfaces now run one path: paint the node highlight (with the wiggle), center the chart on it, and if the node isn't rendered — a collapsed ancestor is the usual cause — expand the ancestor chain, re-render, and center again. If the buddy genuinely can't be shown in the current chart configuration, the existing "Buddy not visible in this view." toast says so instead of failing silently. A settle re-center a half-second later absorbs the panel's opening padding animation, so the node lands at the true center. Project view, constellation mode, and the add-a-buddy centering are unchanged.
- **Homepage URL field: Copy / Open stack under the URL (Dave).** In the info panel, the Homepage URL input shared one row with its Copy and Open buttons; at narrow panel widths the buttons squeezed the input to a truncated sliver and crowded the section controls. The input now takes its own full-width row and Copy / Open sit in a clean row beneath it. The field's display rendering is untouched.
- **Registry chat links wired.** The Hardware and Ashish Chettiar registry entries now carry their side-thread chat ids, so their panels link to their threads like the other buddies'.

### Ashish Chettiar 💼 joins the dashboard (Dave, 2026-10-21)
- **New buddy: Ashish Chettiar** (id `ashish-chettiar`, child of Work Buddy, type person) — the collaboration record for Dave's working relationship with Ashish Chettiar, Liz's boss on the STIX / IS&T side at Apple: regular check-ins just to share what's going on, everything Ashish shares (Apple design tools, UX best practices, IS&T references), and follow-ups on both sides. Persona: generic professional default. Hired with the desk from day one — private repo [davedellaquila/ashish-chettiar](https://github.com/davedellaquila/ashish-chettiar) with KNOWLEDGE.md seeded with the design-tools links Ashish sent in the STIX group Slack (also stored as the [Apple Design Tools & Links](https://docs.google.com/document/d/1hjWGR2x9xbcdKRIfmZsy21mHnp6bvG-eBddiQXdyCQY/edit) doc and linked in his registry `docs[]`), CONFIG.md, and STUDY.md. [Job req](https://docs.google.com/document/d/1haGngeYI7sY5i2PUii_NJ9GHm4lnC9XLPWKznFAUV98/edit) ready for Dave's review; generated homepage at ashish-chettiar/ with the 📄 Repo files desk, 🧠 brain-dump box, red token notice, dark + light mode, and the sticky slim header. Announcement email queued (Gmail disconnected) in the repo at docs/announcement-email.html; side-thread chat id to be wired when the thread is created.

### Dave's chrome spec: the icon swap, the rail chevron, and Recents (2026-10-21)
- **The info icon and the close × are one spot now (Dave).** The ⓘ sits fixed at the page's top-right — same 44px circle, top:12px / right:12px — and shows only while the panel is closed. Open the panel and its circular × occupies the *exact* same spot (the × moved up from top:18px to meet it; both still shift together past the GitHub token pill when it shows). Close the panel — or collapse it — and the ⓘ is back in that spot, and clicking it un-collapses first, then opens. This replaces the rail-ⓘ arrangement from the entry below: the ⓘ no longer lives in the collapsed rail at all, and the corner button no longer hides while the rail shows.
- **The rail's top slot is the expand chevron (Dave).** Where the rail ⓘ sat, a › now lives — tapping it expands the sidebar, same as the corner chevron. The rail's other slots are unchanged.
- **Recents, top-left (Dave).** A clock-with-rewind-arrow button anchors the top-left of the page (it steps right with the sidebar so it always sits at the view's corner) and opens a menu of the most recently visited buddies — visits are recorded whenever a buddy is selected, newest first, no repeats. Picking one opens its panel. How many it lists is a Settings value, **Recent items to remember** (default 10, up to 50 stored).

### Panel reopen fix, settings gripper, strip double-click reset, and the banner steps aside (2026-10-21)
- **Regression fix — the info panel can always be reopened (Dave).** Closing the panel by collapsing it left no visible way back: the panel keeps its open state internally while collapsed, and the rules that hide the corner ⓘ and the rail ⓘ keyed on that alone, so both were hidden in exactly the state they were needed — and clicking them (had they shown) would not have un-collapsed. Both hide rules now key on the panel being open *and not collapsed*, and the ⓘ buttons un-collapse first, then open. Verified for the expanded sidebar, the collapsed rail, and narrow widths; the section rail's buttons still reopen as before. (Note: tapping another buddy refreshes a collapsed panel's contents but does not un-collapse it — reopening is the ⓘ's job, as it was for the section rail.)
- **Settings sheet gripper (Dave).** The floating Settings sheet's drag head now carries a visible gripper at its top center — the gripper dot signature (5 × 2, ~3px dots on a 7px pitch, quiet at rest, brighter on hover, accent while active). Dragging from the dots moves the sheet exactly like dragging the head; the close × is untouched.
- **Panel strip double-click resets the width (Dave).** Double-clicking the info panel's resize strip reset nothing — it closed the panel, while its own tooltip promised "reset to default width." The double-click now resets the panel to its default 440px width (and says so in the saved state, like a drag does); the tooltip was right all along.
- **The Banner Steps Aside (Jonny's verdict, 2026-10-20).** The update banner is no longer a centered card that slides under the open panel. It is a top bar that compresses into the space beside the docked panel: full width (all actions) when no panel is open, *companion* beside the panel with shortened copy ("A new version is ready.") when the free width is ≥600px, and a 216px *pill* (blue dot · Update ready · Update · ×) when it isn't. It moves on the verdict's .5s curve, tracks manual panel resizes with no lag, and honors reduced-motion. Two adaptations to this app's chrome, same rule (never cover, never be covered): the full banner insets clear the 44px corner buttons (ⓘ top-right, sidebar chevron top-left), and the phone sheet — a full-screen takeover here, not a capped bottom sheet — is not re-capped; the banner keeps its top layer and 46px phone form instead. Dismissing in any state dismisses, as before.

### Five fixes from Dave's list + the red token notice (2026-10-21)
- **Parent removal now shows.** Removing a parent in the info panel updated the data but not the panel: the re-render was gated on the buddy having been opened from the list, so from a view (Atlas, Projects) the Parent section sat stale with the × still showing. The remove handler — and the change-parent picker's saves, same defect — now re-render whenever the panel is showing that buddy, so the section updates on the spot.
- **Buddy fields are back in Settings (both surfaces kept).** The Settings sheet again carries the Buddy fields list beside Main views — drag to reorder, uncheck to hide — wired to the same shared field order / hidden state as the in-panel ⋮⋮ grips and hide links, so a change on either surface shows on the other.
- **Prev/Next cleaned up; arrow keys verified.** The stray ⌃ / ⌄ glyphs are gone: the strip reads ↑ Prev / ↓ Next, and the ··· menu rows get a proper icon column — ↑ Prev (↑) / ↓ Next (↓) with muted shortcut hints. Verified in tests: with the panel open, ↑/↓ step through the current collection and re-render the panel, and they stay out of the way while typing.
- **Settings sheet drags on touch.** The sheet's drag handle listened to mouse events only, so it couldn't be dragged on iPad; it now uses the same pointer-event + capture pattern as its resize corner (touch-action:none on the head). Mouse behavior and position memory unchanged.
- **New buddies center in the Atlas.** After an add — request sheet or the panel's add dialogs, including the instant-add placeholder — if the Atlas is the current view, the chart centers on the new buddy so the add lands in view. Any other view: nothing changes, no forced switch.
- **Token-gate notice in red (Dave).** On buddy homepages the dump box's "🔒 Connect GitHub to unlock dumping" notice is now bold red — #cf222e on light, #ff7b72 on dark in the template and snippet; all 59 template pages regenerated (their attention blocks also picked up today's registry changes). Astro's custom homepage uses its own --red token for the same treatment.

### Hardware 🛠️ joins the dashboard (Dave's dashboard request, 2026-10-21)
- **New buddy: Hardware** (id `hardware`, child of Personal Buddy) — keeps track of all the devices Dave owns and is interested in, in one straight inventory. Persona: Drill sergeant. It's also the desk where Dave will attach the report on solar panels — that report has not been attached yet, so its contents stay an open question on the desk, not a guess. [Job req](https://docs.google.com/document/d/1dCYAjECHEk-yRpDJn5ZELZZ0su6O52dTwvbxdFBN3qo/edit) ready for Dave's review; private repo [davedellaquila/hardware](https://github.com/davedellaquila/hardware) with the standard file set (KNOWLEDGE.md seeded with the request, CONFIG.md, STUDY.md); generated homepage at hardware/ with dark + light mode and the sticky slim header.

### Every persona gets a voice (Dave, 2026-10-21)
- **A persona IS a voice now.** Personas and voices used to be separate fields, and every persona sample was read by the same default voice — different characters, same robotic delivery. Each of the 238 roster personas now carries its own catalog voice, matched to the character: the deadpan British butler sounds like a butler, the Italian nonna like a nonna, the drill sergeant like trouble. Jonny keeps his established voice.
- **Picking a persona sets its voice with it.** Setting a buddy's persona — from the picker or Surprise me — now sets the buddy's voice to the persona's voice in the same registry write. The Voice picker still overrides afterwards; the persona proposes, Dave disposes. Clearing a persona clears the voice too, back to the default, as the toast always promised.
- **All 93 samples re-recorded.** Every persona sample in the panel was re-synthesized in that persona's own voice, reading its roster one-liner; no two sampled personas share a voice. Every assigned voice was verified against the speech backend first: 239 of the catalog's 1,066 voices silently fall back to a default voice when asked to speak, and none of those are used.

### The Edge Is the Handle (Jonny's verdict, built 2026-10-21)
- **Anchored panels resize again.** The info panel's resize strip was switched off in every state — docked, floated, sheet — so in anchored mode the panel's width simply couldn't be changed. The strip is back for the docked panel: the same 28px seam strip, min/max, and persistence the sidebar has always had; the frame still owns resizing once the panel floats. Anchored and floating are addresses, not abilities.
- **One dot signature everywhere.** Every grab surface now speaks the same language: a cluster of dots, 2 columns × 5 rows (5 × 2 transposed on horizontal edges), ~3px dots on a 7px pitch, centered on the edge line itself — the sidebar strip's sideways hang-off is gone. Rest strength rises from 34% to 55% (the old mix read as dirt), hover is full secondary, and while dragging the dots go accent with a 1px accent line running the seam's full height, so the edge being moved stays visible.
- **The floating brackets are dead.** The floated panels' frame handles lose their dotted pills and corner brackets: edges wear the dot cluster, corners draw nothing and keep their diagonal cursors, and the hit zones grow to the verdict's 28px, still tucked inside the panel per build 0909. The top-center move grips adopt the same dot size, pitch, and strengths, so moving and resizing read as one family. One signature, on every panel, in every mode.

### The icon strip, whole again; the name never yields (Dave + Jonny, built 2026-10-21)
- **Panel-open returns to the strip.** The buddy-panel open control (`i`) is back inside the collapsed sidebar rail as its topmost item, over a divider line; the floating corner button steps aside whenever the rail is showing (phones keep their Door A corner button — there is no rail on a phone). At the foot of the strip, under a second divider, the **currently selected view** shows its icon; tapping it opens a popover menu of all seven views, the current one marked, and picking one switches the main view. The strip's middle is unchanged: the view icons still switch views directly.
- **Views dock at the sidebar's footer.** In the expanded sidebar, the Views section is now sticky at the foot of the sidebar, directly above the Tip Jar, with a drag handle on its top edge: drag up and the view list grows (to most of the sidebar, always leaving some of the buddy list visible), drag down and it shrinks to a sliver. The size is remembered per device (default: four views tall, the rest scroll).
- **The name never yields (Jonny's panel-header verdict v2, built).** Dave's screenshot said it plainly: "Person…" — the name truncated to make room for a MISSION REVIEW pill. The identity row now holds only the icon, the name, and the close ×; a long name gets the full measure of the row. Status leaves the row entirely: it renders as a quiet annotation line under the tagline — small, letter-spaced, tint carried in the text, no filled pill — and stays absent when the buddy is Active. The aka leaves the header too (it has its own section). The section index ☰ moves into the utility strip beside the ··· overflow, shrunk to strip size; the strip itself never wraps — on a narrow panel, Prev, Next, and All buddies fold into the ··· menu instead.
- **The floating header gets its edge back.** The panel's sticky header card drops the grey band for the panel's own surface, and gains a full border and a deeper shadow, so it reads as a deliberate header while content scrolls beneath it.
- **The close × belongs to the panel.** On a floated panel the × is now pinned to the panel's own top-right corner (fixed positioning, tracked as the panel is dragged or resized) instead of drifting with the page or the viewport corner — it stays put while the contents scroll.
- **Resize handles tuck in.** The floated panels' resize handles move inside the panel's edges and go quiet: no dotted pills, no corner brackets floating outside. A faint accent edge line appears on the side you're hovering, and that's all.
- **Llagas Creek Sale 🏡 joins the dashboard.** The new transaction-coordinator buddy (child of Property Buddy) is in the registry with its [status-page homepage](llagas-creek-sale/), which carries the sale's status at a glance, the awaiting-decisions list, the spend snapshot, the latest from Kay, a link to the full [Kay Korbel activity log](llagas-creek-sale/reports/kay-korbel-activity-log.html), and a 🗂️ Desk reading its knowledge and configuration live from [its repo](https://github.com/davedellaquila/llagas-creek-sale).

### Bulk brief approval — the clean 45 (Dave's call, 2026-10-21)
- Dave directed a bulk approval to unjam the mission-review pile: of the 61 briefs awaiting review (60 "Mission review" + Marketing Buddy's mission-ready status), **45 clean ones are approved** and flipped to Active — template mission statements and living dossiers whose only open items were facts still to collect (pet ages, surnames, birthdates), which stay on as attention items. Their review asks are cleared; unrelated attention items (the hot tub filter order, Tech Buddy's radio and AppleCare tasks, the Designer's Essence package, Penny's onboarding test) untouched. One happy accident: Social Media Buddy's mission was already approved by Dave on Oct 16 — the registry simply never caught up; it matches reality now.
- **16 held back** because their briefs carry decisions Dave hasn't made: Personal (name), Travel and Career (directions guessed from the name alone), Pet (scope), Property (architecture, access, deed security), Work (brief changed — its buddy asked for a re-read), Reminder (standalone vs merged), Zen (shape of the practice), Buddy Suite (title + domain), Sharing (privacy model), Guardian (open-source vs proprietary, pricing, domain spend), Ticket (budget, range), Venue (wedding budget, shortlist size), Portfolio (Squarespace decommission + rebuild), Emil's Estate (inheritance timing, REG 5), and Larry Osana (urgent lease naming the estate as landlord). They keep their "Mission review" status and their queue entries until Dave decides them one by one.

### Org-chart top band, phone: the corners belong to the corners (Jonny's verdict, Door A, built 2026-10-21)
- Dave's screenshot: the menu square swallowing the chart's name, the *i* sitting on the control rail, the zoom slider clipped by the screen edge, three rail utilities hidden past the glass in a sideways scroll with no hint they exist, and Quick Answers running full-bleed with its label cut. Jonny's ruling, now built — phone (≤639px) only: the first 60px is reserved for the two fixed buttons alone, remade as a matched pair of 44px glass circles (Door A: the menu square takes the *i*'s material, size, and 12px inset; its ☰ sits at 18px). `#panel-open` moves from top:18px to top:12px at **every** width — the spec's one non-phone change — and `#sb-expand-corner` moves with it, so the desktop pair the code always described as "directly in line" stays in line.
- The Atlas rail may not scroll in secret: at phone width it wraps into honest rows in DOM order — lens pill + orientation, colour dots + a full 180px zoom slider (a thumb-sized 44px tall; the selector outranks the generic range-input rule so the size actually lands), then fit / fullscreen / centre — every control visible, nothing smaller, the rail's frosted material and 22px radius kept. The `#tree-chrome-main` reservation grows 64px → 264px (rail top 72 + rail height 180 + 12 of air — the arithmetic is the design).
- Quick Answers wears the same clothes: an inset card aligned with the rail, its label on its own line (never clipped), answers at full width stacking downward under a vertical fade, the card scrolling down (max-height 188px) instead of sideways into a cliff. Desktop and iPad compositions are untouched.

### Section toggles hold their place (Dave, 2026-10-21)
- Expanding or collapsing a section in the info panel no longer makes the list jump: the clicked header is held at its exact viewport position while its own contents show or hide and everything below shifts. The 2026-10-15 one-shot correction guessed the scroller by class (a silent no-op when the guess missed), fired a single time (late layout and iOS focus-scroll landed after it), and lost to the browser's scroll clamp when a collapse near the bottom shrank the page — the new `holdHeaderPosition` finds the real scrolling element, corrects immediately and again over the next few frames, temporarily lends the scroller bottom room (a spacer, removed by the next toggle or re-render) when the clamp would otherwise win, and stands down the moment Dave scrolls himself. All three toggle paths use it: section title rows, toggle medallions, and header taps.

### Section headers: the value never yields (Jonny's verdict, built 2026-10-21)
- Dave circled the Manager row: "MANAGER: A…" — the manager's name truncated to a letter while a medallion, an add button, an ⓘ, a drag grip, and a hide link shared its line. Jonny's ruling, now built: the name line holds only the medallion, the label, the value, and one verb (the control that acts on the value — Manager's ⊕, or its "+ Add parent" pill when open). Label and value never truncate again; a long value wraps inside its column (≈224px on phone, ≈306px on the desktop panel, up from ≈111px).
- The machinery gets a line of its own: a new `.sec-util` row directly beneath every section header — both the compact attr-head sections and the h3 sections — at 11px in the faint voice, grip ("⋮⋮ Reorder", spelled out) on the left, hide on the right, at full presence (the hover-reveal opacity treatment is retired). The line stays visible when an h3 section is collapsed, so its controls stay reachable. Cost accepted in the verdict: ≈20px more height per section.
- The ⓘ dissolves into the body: each header's explanation sentence is now the first quiet line of its expanded body (the parent section gets a tip row of its own, ahead of the parent links). The Dump Box keeps its ⓘ — it's an h3 section, outside the verdict's scope.

## 2026-10-20
### Section borders removed; icons take the medallion (Dave, 2026-10-20)
- Dave circled the Photos section on the Model A's panel: a rounded outline hugged the whole section. It was the sections' hover treatment from the free-floating build (19:07) — a tint plus an inset 1px outline — latching after taps on touch. Both are gone; sections sit flat on the panel again. (The Photos drop zone and the Dump Box keep their own borders — those outline the fields, not the sections.)
- The attrHead sections (About, A.K.A., Persona, Voice, Parent, both notes) now fill their medallion from the same Section toggle style setting as the h3 sections: on the default "section icon" style the medallion is the section's own icon (📝 on both notes sections, 🎭 Persona, 🎯 About) instead of the plain ›, and icon medallions don't rotate sideways when the section expands. The 📝 prefix leaves the two notes labels — the medallion carries it now.

### Tighter gutter beside the docked info panel (Dave, 2026-10-20)
- Dave circled the seam on the Reminder Buddy shot: with the panel docked, the breathing room between the main view and the panel read too wide. The anchored yield's gutter drops from 32px (desktop) / 22px (iPad band) to 16px in both bands — in the regular yield rules and the homepage-mode overrides alike, so every view sits the same distance from the panel. The panel's shadow still has room to read; the content just sits closer. (The sidebar side still yields at 24px — say the word if they should match.)

### Homepage mode takes the anchored yields; newsreader voices go quality-first (Dave, 2026-10-20)
- **Homepage gap (second circled screenshot):** homepage mode zeroes #main's padding, which silently outranked every anchored yield — so with a buddy homepage open (News Buddy in the shot) and the panel docked, the iframe ran full-width underneath the panel. Homepage mode now takes the same yields as every other view (left: sidebar width + 24px; right: --bpw + 32px on desktop, + 22px in the iPad band), handed back when the panels close or float. Selecting News Buddy's homepage from the dashboard also counts as arriving from the owner's own dashboard: it arms the newsreader voice unlock on that device (one extra owner tab, once per device).
- **Newsreader voices:** raw getVoices() order buried the good voices — the picker dealt 10 at random from ~180 device voices, so Samantha and the Enhanced builds often never appeared; the no-choice fallback could land on a harsh compact en-US voice; and the shipped mascot persona was Cellos, a novelty voice. The list is now quality-ranked (Enhanced/Premium builds first, then Samantha, then the named natural voices, then other English; novelty voices last), picker rows carry a quality tag (Enhanced / High quality / Novelty), and the default walks the same ladder. If Samantha still doesn't appear, she isn't downloaded on that device: Settings → Accessibility → Spoken Content → Voices → English → Samantha (Enhanced). Picker rows now label every curated natural voice "High quality" too (before, only Enhanced builds and Samantha got a tag), and the voice loader re-arms when the browser's first answer is a one- or two-voice stub, so the full inventory replaces the stub instead of the picker living on it.
- **Info panel opening animation:** the panel animated on close but snapped on open — the open path adds .active and the mode class in the same frame, so it painted straight at rest. The panel observer now parks a freshly opened panel in its hidden pose for two frames, then releases it, and the corner-grow plays every time. Floated panels skip the pose (their saved rect owns the transform).

### Anchored info-panel yield follows the panel's real width (Dave, 2026-10-20)
- Dave's circled screenshot: in Anchored, with the info panel docked, a wide dead gap sat between the main view and the panel — the two arrows pointed at each other across it. Cause: the yield was a fixed number (472px on desktop, default-width + 22px in the iPad band) while the panel itself renders at its own live width (the drag-resized panelWidth, capped at 560) — a panel narrower than the default left the difference as empty space. Both yield rules now compute from --bpw, which applyPanelWidth sets and the resize drag updates live: desktop --bpw + 32px; iPad band --bpw + 22px (falling back to the previous default-width expression if unset). At the default 440px width nothing changes; a resized panel's gap is gone, and the main view tracks the panel while it is being dragged. Mirrors the sidebar side, whose anchored yield already follows --sbw.

### Anchored sidebar yields the main view; Prev/Next point up and down (Dave, 2026-10-20)
- **Anchored sidebar yield:** Panel style = Anchored made the info panel dock (the main view resizes for it) but the sidebar stayed a fixed overlay and opened over the content. Now the main view yields on the left too: at widths >= 640px, #main's left padding becomes the sidebar's live width (--sbw) + 24px, the tree chrome's own 348px sidebar clearance drops out (the yield replaces it), and #main eases padding-left on the same .5s curve as padding-right. Floating keeps the overlay illusion, the collapsed rail keeps its 88px, and phone widths keep the sheet behavior. CSS-only, following the info panel's anchored yield pattern.
- **Prev/Next point up/down:** the bottom-center homepage Prev/Next circles swap their left/right chevrons for up (Prev) and down (Next); the buddy panel's topnav text buttons match (caret-up Prev, caret-down Next). The sidebar expand corner keeps its right-pointing chevron.

### Sidebar tools get the big-button treatment; 📝 on the notes eyebrows (Dave, 2026-10-20)
- The sidebar's top-right tools now wear the same glass-disc treatment as the big corner buttons (#panel-open / the info panel's close): 44px glass circles with blur, hairline border and soft shadow, lightening with an accent ring on hover. The sidebar close mark is now the same plain × the info panel uses (its smaller drawn circle-✕ is retired), and the gear grows 19px → 24px (still red).
- 📝 now leads the Private notes and Shared notes eyebrows — in the buddy panel and in the plan detail view.

### Info icon: italic serif i (Dave, 2026-10-20)
- The panel-open button's serif i is now italic — the classic information glyph (Georgia italic). One property on `#panel-open .pi-serif`.

### One panel style for both panels (Dave, 2026-10-20)
- The Settings choice formerly "Sidebar panel style" is now **Panel style** and governs BOTH panels. **Anchored:** both panels sit flush to their edge in the same squared-off style, the main view resizes to make room (the info-panel yield shipped earlier tonight is now scoped to Anchored), and neither panel can be dragged — switching to Anchored docks a floated panel and keeps its rect for when Floating returns. **Floating:** both panels are movable, resizable inset cards — the info panel as before, and now the sidebar too: a dotted gripper at its top-center drags it anywhere, grippers show on all sides once it floats, the rect persists (`S.sbFloat`), and double-clicking the gripper docks it again. While the sidebar is docked, only its gripper shows — its right-edge width grip keeps its own job — and collapsing to the rail or switching to Anchored docks it visually.
- Verified in a DOM harness against the real build: float applies (frame tracks, free state), switching to Anchored clears the float and hides the frame, switching back restores the saved rect, and the dock path restores the standard 336px width. (jsdom cannot evaluate @media, so the media-block placement was confirmed by inspection, same as the anchored yield.)

### Anchored side panel: the main view resizes (Dave, 2026-10-20)
- When the info panel is docked — open, not floated, not collapsed to the rail — the main view now resizes to make room for it instead of being covered: #main's right padding grows to the panel's width plus its usual inset (472px on desktop, panel-width + 22px on iPad widths), easing on the panel's own .5s Kin curve so the two glide together.
- A floated panel stays a free overlay (no yield), and collapsing to the rail releases the space. Pure CSS `:has()` rules in the panel's two media blocks, following the existing `body:not(.bp-collapsed):has(#view-buddy.panel.active)` pattern. Verified: selector logic exercised in a DOM harness (docked 472px / floated 32px / collapsed 32px; jsdom can't evaluate @media, so the in-block placement was confirmed by inspection).

### Voice picker: one-word tone pills + pill filters (Dave, 2026-10-20)
- Every voice card in the Voice picker now wears its one-word tone (Warm, Gravelly, Calm…) as a colored pill under the blurb — the word was already in the catalog data, just never shown. Same word, same color everywhere: the color is hashed from a fixed 12-color palette.
- A filter row under the search box shows the 14 most common tones with counts (Gravelly 30 · Warm 30 · Calm 28 · Bright 27 · Confident 27 · Smoky 27 · Crisp 20 · Throaty 20 · Velvety 20 · Energetic 19 · Smooth 19 · Earnest 18 · Resolute 18 · Wry 18). Tap a pill to filter the grid to that tone, tap again to clear; it composes with the text filter, which still reaches all 164 tone words.

### Floated panel: visible grippers on all sides (Dave, 2026-10-20)
- The floated info panel's resize handles were invisible strips. Now the south/east/west edges wear a dotted pill in the drag gripper's language, and all four corners wear a bracket; every gripper warms to the accent color on hover. The top edge's gripper is the drag pill itself, so the north strip draws nothing of its own. CSS-only, in the `#bp-frame` overlay — grippers show exactly when the panel is floated and resizable.

### Picker sheets: Cancel moves to the bottom-right (Dave, 2026-10-20)
- In the Voice picker (and the Persona picker, which shares the footer), **Cancel** now sits at the sheet's bottom-right — Dave circled it at bottom-left and arrowed it across. "Default voice" keeps the left. One rule: `.pp-actions #pp-cancel{margin-left:auto}`.

### The info panel floats — drag, resize, serif i, spinning x, animated closings (Dave, 2026-10-20)
- **Free-floating panel:** the buddy detail panel now drags by a dotted **gripper at top-center** and resizes from **any corner or side** (8-handle frame overlay that tracks the panel's box). The rect persists across opens; **double-click the gripper to dock** again. Dragging a resize below 220px wide still snaps the panel shut, like the old left-edge strip it replaces. The close x rides with the panel when floated.
- **Serif i:** the Open buddy details button's glyph is now a serif **i** (Georgia), replacing the plain dot-and-stem.
- **Spinning x:** clicking the panel's close x gives it a little 360° spin as it hands back to the i.
- **Corner buttons sit lower and go glass:** the i button, the sidebar's expand chevron, and the panel's close x drop from 12px to 18px and get translucent glass backgrounds (blur + saturation); on hover all three lighten and take the blue accent border.
- **Animated closings:** closeDetail no longer strips the panel's mode classes in the same frame (that snapped the close) — the glide-out plays first. The phone sheet rises/fades both ways, and collapsing the panel to the section rail **folds** toward the rail (and unfolds) instead of display:none.
- **Tiles feel alive on hover:** stat tiles fade in a diagonal fill pattern in their own tint, warm their border to the tint, and the number swells slightly; the panel's section cards get a soft wash + inset ring. No layout shift anywhere.

### Briefing Buddy — lineup sync + Tonight's dinner
- Homepage lineups now mirror the updated crons: morning adds "Tonight's dinner" (13 sections), evening corrected to 9 sections + closing dinner question.
- Sections library + Designer defaults gain "Tonight's dinner"; new Tonight's dinner live-data tile (Tue Oct 20: Croque Madame sandwiches); live-data location corrected to Fiddletown for the weeks of Oct 19 & 26.

### Plain × for the panel close (Dave, 2026-10-20)
- The buddy panel's close mark drops its circle: it's now a regular × — two strokes, no ring (new plainX() glyph, 22px, same family weight as the plain i and the chevrons). circleX() remains in use where Dave hasn't asked to change it (avatar sheet, field settings, What's New).

### New buddy: 🏎️ 1968 MGB-GT
- Set up from Dave's dashboard request: a living dossier for the 1968 MGB-GT, child of Car Buddy, persona "Deadpan British butler." Job req, private repo, homepage, and About page are live; the request supplied no purpose or car facts, so color, engine, mileage, and condition stay open questions in the dossier, never guessed.

### The info button is a plain i now (Dave, 2026-10-20)
- The Open buddy details button (top-right) drops the circle from its glyph: it's now just the regular **i** — dot and stem, same 24px / 2.5-stroke family as the other chrome glyphs — inside the same round glass button.

### Profile image leads the avatar sheet (Dave, 2026-10-20)
- The Choose avatar sheet is restructured the way standard profile pictures are managed. A **Profile image** block now sits at the top: a preview of what's current (the uploaded image, or the emoji it falls back to), a state line ("Image set — it replaces the emoji" / "No image — using the emoji"), **Upload image** (becomes **Replace image** when one is set), and **Remove image** when one exists. Clearing deletes the image file and the buddy goes back to its emoji everywhere — card, homepage, favicon. The upload/remove machinery already existed but was buried below all eight emoji categories at the bottom of the sheet; the emoji grid and paste-your-own field now live underneath an "or pick an emoji" divider.

### Avatar sheet gets its close ✕ (Dave, 2026-10-20)
- The Choose avatar sheet (opened from a buddy's avatar in the panel header) had no close button — only an outside tap dismissed it. It now carries the shared circled-✕ at the top-right of its header, at the 22px in-panel icon size, wired to the same close path as everything else.

### Icons sized between, Hidden fields bulk actions, What's New type pills (Dave, 2026-10-20)
- Buddy panel icons: the gear (in the panel's ··· menu) and the circled-✕ that closes the field-settings dialog grow to 22px — bigger than before (16px / 20px), a step below the 24px glyphs on the main view's chrome. The panel's own close ✕ was already 22px and now matches them.
- Hidden fields menu: the last item is now a bulk row with two side-by-side choices — **Add all** restores every hidden field (arriving open, like a single show) and **Remove all** hides every field. Both act on the whole field set at once.
- What's New sheet: every entry now carries a small colored pill naming its type (Added / Changed / Fixed / Other — classified from its changelog heading, since the headings are free-form), and those types drive the filter row at the top of the sheet: pills with counts, pinned sticky while the entries scroll beneath them. Tapping a pill filters the list; tapping again clears.

### Panel grows out of the ⓘ corner (Dave, 2026-10-20)
- The buddy detail panel no longer slides in from off-canvas right. Dave: opening it should feel like it comes from the button that was clicked. The panel now grows out of the top-right corner where the ⓘ (Open buddy details) button sits — a short translate + scale from a top-right transform origin with a fade, on the same .5s Kin curve — and settles back into the corner when it closes. At rest the open panel carries no transform, so nothing inside it is re-anchored. Desktop/iPad panel only; the phone sheet and portrait takeover keep their existing entries.

### "The Bento picker, the wandering chevron, and a centered rail" (Dave, 2026-10-20)
- Default View style picker (Bento / Ledger / Console / Pulse) actually works now. Two traps made it decorative: the picker row's sticky z-40 stacking context sat UNDER the picker's own full-screen scrim (z-59), so opening the menu raised the scrim over it and every card click landed on the scrim and merely closed the menu; and the dropdown opened rightward from the right-aligned pill, clipping most of it off the frame's edge (only Bento and one other card were ever visible). While open, the row now lifts above the scrim, and the dropdown opens leftward from the pill.
- The sidebar's expand chevron moved out of the collapsed rail's icon stack: it now sits by itself at the page's top-left corner as its own 44px circular button, directly in line with the info (ⓘ) button on the other side, same design. It appears only while the sidebar is collapsed (never on phone widths). The rail's icons now only switch views.
- The collapsed right panel's icon rail (#bp-rail) is vertically centered on the page (top:50%), mirroring how the collapsed left sidebar centers itself, instead of hanging at top:76px.

### "Uploads, recents, and landing where you made things" (Dave, 2026-10-20)
- Creating a buddy now lands on it: after the new-buddy request sheet files its request (or the add-buddy dialog creates a buddy), the new buddy is selected and displayed in the main view (the detail panel opens) instead of the view staying on whatever was open before. A caller that passes its own onCreated callback keeps its own landing (the parent picker stays on the buddy being edited).
- The info (ⓘ) "Open buddy details" button's icon now matches the footer button family (Back / Prev / Next): 24px glyph with a 2.5 stroke, up from 22px / 2.0.
- Document uploads: the progress tile spans the full width of the panel (was capped at 280px), and the bar is a thermometer — a 12px tube with a gradient fill and a drifting diagonal pattern. Progress within a file is estimated (the old bar sat at 0% until the file finished): the fill creeps toward 92% of the current file on a size-scaled curve while the encode + GitHub PUT runs, snaps to the real count when the PUT lands, and holds at 100% for a beat before the card clears.
- Search buddies: focusing the empty search box now opens the dropdown with your recent searches (newest first, up to 8, stored per device) — tap one (or arrow + Enter) and it fills the box and switches to the matching-buddies autosuggest. Terms are recorded when a search lands (picking a buddy or the Create row); a "Clear recent searches" row sits at the bottom of the list.

### Social Media Buddy homepage: LinkedIn Makeover report + Post 1 live
- New "🔗 LinkedIn Makeover — the report" card on Social Media Buddy's homepage: Post 1 live on LinkedIn (37 impressions at first check, engagement watch every 3h), the 2026-10-20 profile audit (5,309 followers; Featured absent; Rae Technology missing), and the makeover plan with links to the brief, project thread, repo, and Dave's profile.
- Post queue brought current: Post 1 chip → "Posted ✓", pipeline counts Drafted 14→13 / Posted 0→1, stale "scheduling on hold" note replaced (the drip is live; Dave posts each day's staged copy).
- Post Pipeline chart regenerated (Charts Buddy's social_pipeline.py, counts verified 2026-10-20) in both themes.

### Custom homepage is the homepage; the default page is now the About page (Dave 2026-10-20)
- Dave's model, first applied to Zen Buddy: the designed custom homepage serves as the buddy's actual homepage (index.html), and the Default Homepage (the Dossier) moves to `<id>/about.html` as the buddy's About page — linked from the custom homepage (sticky header + footer) and from every template homepage's footer ("About · the full record").
- `gen_default_homepages.py` v3.2: new `--about` mode writes about.html without touching index.html. Every default/About page now also carries the COMPLETE registry record (every field; unset fields shown as "not set") and a "From the repo — markdown files (N)" section: a baked inventory from the buddy's local repo clone plus the live, token-gated 📄 Repo files reader (gen_basic's FILES_* widget) — repo markdown is read from GitHub on Dave's devices, never baked raw into the public page. Also hardened: string attention/docs entries no longer crash the build (one buddy stores them as plain strings).
- Zen Buddy: custom homepage shipped as `zen-buddy/index.html` (breathing orb, sticky header, 🧠 brain-dump box, honest doc cards — brief in review, PRD up next; an earlier draft wrongly claimed a PRD was approved). Its repo got its first commit the same day (README / KNOWLEDGE / CONFIG / STUDY / docs/ingest) so the About page has a real desk to show.
- About pages generated for all 130 buddies (Astro's hand-written about.html kept as-is). One orphan: `family/` is a stale template folder with no registry entry, so no generator owns it and it has no About page.

### All voices unlocked for testing (Dave 2026-10-20)
- Dave: "Unlock all the voices so that I can test them out." Two locks, two fixes. (1) Dashboard voice picker: `build.py` has loaded all 1,066 voices from voice-catalog.json since Oct 12 but the emitted `VOICE_CATALOG` was still a separate hard-coded 30-voice array — the picker now receives the full catalog (searchable as before; the grid renders the first 400 matches with a "keep typing" hint so the sheet stays responsive, and every entry now carries accent/tone, which the filter already expected). (2) News Buddy read-aloud picker (`news-buddy/s/buddy.js`): the tip-jar gate stays for the public, but an owner bypass unlocks every device voice on Dave's own devices — open any news page once with `?owner=1` and a per-device localStorage flag (`newsBuddyOwner`) keeps them unlocked there; the picker footer says so when owner mode is on. Public visitors still get the 10-voice re-deal + tip pitch, unchanged.

## 2026-10-20
### Search autosuggest: "Create new buddy" is now always the last row (Dave 2026-10-20)
- The buddy search autosuggest only offered "Create new buddy" when nothing matched. Now the create row is always the final row of the dropdown — when the suggestions aren't the buddy you wanted, the way to create it is right there, prefilled with what you typed. It sits below a hairline as the list's footer action, is part of the arrow-key/Tab cycle (Tab lands on it without triggering it; Enter or click creates), and is the highlighted row in the no-matches state so Enter works there too.

### Document viewer fixed: PDFs now load through the token, not the raw URL (Dave 2026-10-20)
- Tapping a document card in the info panel opened a blank viewer. The viewer's iframe pointed straight at the file's raw GitHub download URL — but every buddy repo is private and an iframe can't carry the GitHub token, so GitHub answered 404 and the PDF never rendered. The viewer now fetches the bytes through the contents API (the file's API URL + token, the route the rest of the app uses), shows the PDF from a same-page blob URL, and — if a load ever fails — says so in the viewer with the reason instead of opening an empty box.

### Back / Prev / Next buttons now show over the phone sheet too (Dave 2026-10-20)
- Dave: "they should be there all the time." The one carve-out from this morning's visibility spec — hidden while the buddy panel is open as a phone sheet — is gone: the buttons now float above the sheet as well (they already painted above everything else). The field-settings modal is the only surface that still covers them, so its Done button stays clear.

### Sticky section eyebrows in the sidebar (Dave 2026-10-20)
- As the sidebar list scrolls, each section's eyebrow (Buddies, Business Plans, Views…) now pins beneath the sticky brand + search stack and stays there until the next section's eyebrow pushes it away — iOS Contacts behavior. The pinned bar is full-bleed with the same opaque background as the other sidebar stickies, and it joins the glass treatment when Panel translucency is set to Glass. Its offset is measured live from the brand and search bars, so it stays correct at any text size.

### Panel translucency setting — Apple Weather glass for the side panels (Dave 2026-10-20)
- New Settings choice, "Panel translucency" (Standard / Glass), inspired by the Apple Weather iPad side panel Dave filed into the Kin design archive. Glass mode drops the sidebar, buddy detail panel, section rail, and the sidebar's sticky bars to roughly half fill with a stronger blur and saturation, so the Atlas canvas or a homepage behind them tints the glass. Standard (the default) keeps the usual soft frost. Applies live from Settings and rides the factory-defaults snapshot like the sidebar style it sits beside.

### Search autosuggest: Tab now moves the dropdown's highlighted buddy too (Dave 2026-10-20)
- With the search autosuggest open, pressing Tab selected the next buddy but the dropdown kept highlighting the first match — the global Tab handler only cycled the sidebar rows and never told the dropdown. The search field now handles Tab itself while the dropdown is open: the highlight moves to the next (Shift+Tab: previous) match and that buddy is selected, so what you see highlighted is who you get. When the dropdown is closed, Tab keeps its sidebar-cycling behavior.

### Repo files on every template homepage — view + edit the buddy's markdown (Dave 2026-10-20)
- Every default-template homepage gains a "📄 Repo files" section: with a GitHub token connected it lists the buddy repo's markdown files (repo root + docs/), tap one to read it rendered, Edit to change it in place, and "Save to GitHub" commits it straight back (with a clear message if the file changed underneath you). Without a token it shows the connect prompt — the repos are private, so reads need the token. Rendering uses a small built-in markdown renderer (headings, lists, quotes, code blocks, links, emphasis).

### One done state across dashboard and homepages (Dave 2026-10-20)
- Marking attention items done on a buddy's homepage didn't stop the dashboard's "Needs your attention" header from pulsing: the two surfaces kept separate done lists (homepages write `attnDone`, the dashboard read only its own `seen`). Both now honor both maps — the dashboard's unseen computations (panel section, counts, badges) go through one shared check, and homepage tiles likewise honor dashboard dones. When every item for a buddy is done, the section doesn't render and nothing pulses.

### Constellation spacing panel — docked to the pane, out of the zoom layer (Dave 2026-10-20)
- The Spacing panel (and its collapsed pill) were built inside the chart's zoomed layer, so they scaled with the zoom factor and floated wherever the chart content put them. They now mount on the tree pane itself and dock to its bottom-right corner: constant size, always in reach, and removed cleanly when switching to another lens.
- Dock raised (Dave, on-device check): at the pane's very bottom the panel sat underneath the fixed footer nav cluster; it now docks 92px up, clear of the buttons at any split position.

### Section headers, chart background, sheet focus ring (Dave 2026-10-20)
- Info-panel section headers now follow the pattern agreed 2026-10-19 end to end: the add control sits on the eyebrow row in both states — a small ⊕ circle while the section is collapsed, the spelled-out "+ Add …" pill while it's open (Parent/Manager and Children sections). A single-value section shows its value in the header while collapsed ("MANAGER: Project Buddy"); while open the header keeps just the label, since the body shows the value — the add pill used to squeeze the header text down to "M.".
- The Atlas Background color picker now actually paints something: it set `--main-bg`, which only colored the tree view's outer box — an area completely covered by the chart stage. The chart canvas (`#treezoom`, both panes) now uses the picked color, falling back to the Kin canvas tone on Reset.
- New-buddy sheet: the NAME field's focus ring was clipped on the left and right by the sheet's scrolling body (the input spans the full content width, leaving the ring nowhere to go). The body now carries 4px of breathing room inside the clip edge, alignment unchanged. (Reported 2026-10-19 and queued; shipped now.)

### Attention banners get a done control + Las Vegas mode (Dave 2026-10-20)
- Shreya Dhingra's homepage attention banner had a decorative yellow circle and no way to mark the item done. The circle is now the control: solid amber = needs attention; tap → green circle with a white check, recorded on-device and written to the buddy's ingest (queued locally when no token), same as the template pages.
- Las Vegas mode: every Done tap now celebrates — the button spins once and confetti bursts from it (dashboard info-panel circle, Pulse tick, template homepage Done buttons, the banner dot). Pure DOM/WAAPI, self-cleaning, skipped under prefers-reduced-motion, and never fired for items already done on page load.

### Text size setting — scales text only, never the layout (Dave 2026-10-20)
- The Settings "Text size" slider drove `body{zoom}`, which scales geometry along with text: on iOS the page rendered wider than the phone (sideways scrolling), dialogs grew too wide, and fixed buttons (the +) drifted while scrolling.
- Rebuilt on the root-font-size mechanism: all 300 font-size declarations in the dashboard converted from px to rem against a 16px root (no layout property uses rem, verified), and the slider now sets the root size. Text scales 80–130%; widths, dialogs, panels and anchored buttons keep their exact geometry.

### Attention "Done" buttons — no check mark until clicked (Dave 2026-10-20)
- Buddy homepage attention tiles (template): the Done button rendered "✓ Done" upfront, which reads as "already done" while the item is still sitting there. It now renders plain "Done"; the check appears on the button only after the tap (paintResolved swaps the label), alongside the "Marked done" status.
- Pulse view tick aligned to the same rule: empty circle ○ instead of an always-on ✓ (the dashboard info-panel button already behaved this way).

### Homepage nav buttons — redistributed along the bottom; shown whenever the info panel is open (Dave 2026-10-20)
- Layout: Back leaves the lower-right cluster for the lower-left corner, the mirror image of the + button (left:20px to the FAB's right:20px, same 20px bottom, same 56px circle). Prev/Next stay paired and, as a group, are centered horizontally between Back and + (left:50% + translateX(-50%)).
- Visibility: the buttons appear whenever a collection is on screen, regardless of the panel — a buddy homepage, the info panel (right panel, #view-buddy.panel.active, not collapsed) open from any view, the sidebar's hierarchical buddy list open (≥640px), or the tree view. Still hidden under the phone sheet (modal) and the field settings. Shipped as a test build for Dave to live with.

## 2026-10-19
### Neighborhood Buddy — charter doc updated (Dave 2026-10-19)
- Registry brief link for Neighborhood Buddy now points at the San Jose/Nextdoor job req Dave adopted tonight as the buddy's refreshed charter (reconciled: Property Buddy stays the parent; the Fiddletown patch continues under the original brief, which remains linked from the buddy's repo).
### Homepage nav cluster — stays next to the + button, panel open or not (Dave 2026-10-19)
- Dave's screenshot (Sports Car Adventures, panel open) showed the Back/Prev/Next cluster parked mid-page over the homepage's headline — the ≥1101px rule that slid it left of the open panel (right:468px) put it there. Removed: the cluster now stays at right:88px, glued to the + button in every state, floating over the panel's bottom corner at the FAB's own z-index, exactly as Dave originally asked ("next to the Add button").
### Collection-field counts in the info panel (Dave 2026-10-19, Designer thread)
- Every collection field's label now carries its item count — muted "(N)" — in the Hidden fields list, matching the visible section headers, and (0) shows too: zero means the relationship exists and is empty. Circled set: A.K.A., Artifacts, Documents, Needs your attention, Peers, Private notes. Counts reuse each header's own semantics (attention = unseen items, Private notes = word count, Documents patched in by the async docs loader just like its header). One shared counter (fieldCountFor) feeds both places so the number never changes meaning when a field is hidden or shown.
### Brain-dump token card — amber, not zebra (Dave + Jonny 2026-10-19)
- Dave, circling the "🔒 Connect GitHub to unlock dumping" card on the 4 post lift homepage: make it more prominent — a yellow/amber border, or maybe a zebra stripe. Jonny's call: amber. Zebra striping is hazard tape — it signals danger and fights every calm surface around it; a credential step is not roadworks. The old dashed grey border read as placeholder/unfinished, which is why it was so easy to skim past.
- Treatment, in `gen_basic_homepages.py` (DUMPBOX_CSS) and the canonical `docs/dumpbox-snippet.html`: solid 2px amber (#f59e0b) border, a soft amber wash over the page background (rgba + color-mix, both modes), a faint 3px amber halo, and the lock line set semibold. No pattern anywhere on the card.
- Piloted on the 4 post lift homepage only (`--only 4-post-lift`); the fleet follows on the normal template rebuild. Custom (non-template) homepages keep their own copies until their owning threads adopt it. Inline scripts on the regenerated page pass `node --check` (4/4).

### Homepage nav cluster — Back joins Prev/Next (Dave 2026-10-19)
- A Back button now sits with the floating ‹ › pair on buddy homepages, same size, same glass style, return-arrow glyph. It runs the dashboard's existing history Back (same behavior as the panel's Back, tree view as fallback). Shows under the same rule as the pair: whenever a homepage is showing.
### Homepage Prev/Next — visible whenever a homepage is showing (Dave 2026-10-19)
- The ‹ › pair shipped earlier today gated to "both panels closed + homepage view," which hid it in the state Dave actually browses in. Per his evening call, the gate is relaxed: the pair now shows on any buddy homepage regardless of panel state (arrow keys follow the same rule). With the right panel open on desktop it shifts left of the panel (right:468px) instead of floating over it; the phone sheet is modal and still covers it; the field-settings hide is unchanged.
### New buddies: eight device buddies under Tech Buddy 📱 (Dave 2026-10-19)
- Dave approved the full set during the AppleCare One conversation: one living-record buddy per household computing device, all children of Tech Buddy. Registry 122 → 130. Each is typed `device`, persona "Product specialist", with a generated dossier homepage (the complete record — known fields listed, unknowns shown as open items).
- The eight: 📱 iPhone 18 Pro (1 TB, Black, AT&T; Apple Card Monthly Installments $74.95/mo × 24 at 0%, $1,799 — **ordered Oct 19, order W1855831943, status ordered / preparing; Apple commits delivery Oct 29 – Nov 5**; enroll in AppleCare One from Settings on arrival — the order carries no AppleCare) · ⌚ Dave's Apple Watch (Series 10; eligible on Dave's plan) · 🖥️ Dave's iPad Pro (1st generation; NOT eligible — too old, and its record says so plainly) · 📱 iPhone 16e (256 GB; no coverage; for sale after the 18 Pro lands — Apple trade ~$270 / Swappa ~$425 reference points) · 💻 MacBook Air M2 (2022, ~1 TB; eligibility BORDERLINE — the exact purchase date decides) · 📱 Nan's iPhone 17 Pro Max (eligible on Nan's own plan) · 🖥️ Nan's iPad Air (generation unknown — decides eligibility) · ⌚ Nan's Apple Watch (Series 8 or 9 — a Series 8 would be borderline).
- One shared charter doc in Buddy Docs — "Device Buddies — setup" (the job the eight share: be the living record of each device) — linked on all eight buddies' `docs[]` and on Tech Buddy's `docs[]` (its first doc link). Coverage frame recorded on every record: AppleCare One Individual $19.99/mo covers up to 3 devices per Apple Account; Dave's plan and Nan's plan are separate; enrollment happens from Settings after delivery, never on the order.
- Each buddy has a private repo (davedellaquila/<id>) seeded with KNOWLEDGE.md as the living record — verified facts only; serials, exact purchase dates, and unknown generations are written as open items, never invented — plus CONFIG.md and STUDY.md (first study topic for each: capture the exact purchase date / generation / serial from Dave or the device itself). Tech Buddy's generated homepage refreshed to list its eight new children.

### Relationship vocabulary by type — the words now fit the buddy (Dave 2026-10-19)
- Dave's premise: every buddy has a type, and the words for up / down / across should fit it — family words for people, org words (manager / direct reports / peers) for work, neutral words when the type is generic or unknown. He asked for the combinations and the rules; the research (~/workspace/buddy-vocabulary/type-vocabulary.md) found the dashboard already speaking three vocabularies inconsistently, and Dave adopted the rules the same day ("This is AWESOME! — adopt these rules").
- The rule: words key off the EDGE (parent type → child type), never either buddy alone. One vocabulary per section, unanimously — any mix falls back to generic. Headers are plural with counts, buttons and dialog titles singular, belongs-to phrases use names, never role words. Three families ship: org (manager / direct reports / peers, "Reports to X"), membership (group / members / fellow members, "Member of X"), family (parent / children / siblings — siblings only when the shared parent is a person or a kin group and both buddies are people; Quentin's peer set keeps "Peers"/"Fellow members" because it includes a fiancée, a girlfriend, and couples). "Linked buddies" stays type-neutral forever — links cross types by design. "Orphaned buddies" is kept as a conscious exception.
- Registry: a new explicit `type` field is backfilled on 119 of 122 buddies (Dave's family-history dossiers — Emil, Martha — and Job Buddy deliberately carry none), inserted textually at sorted-key position; `kind` stays a loose display tag. Population: assistant 55, person 30, people-group 6, software 4, place 4, pet/device/property/vehicle/venture 3 each, org/topic 2, collection 1 (BMW). The add-buddy dialog's Type picker now writes `type` alongside `kind` (Person → person, Project → venture) so new buddies arrive typed instead of conflated.
- Car Buddy exception: it is typed `assistant` (it is one) but behaves as a collection, so it carries a per-buddy `vocab: "collection"` override — its down-section reads "Vehicles (7)", its ⊕ and add dialog say "vehicle", its members' up-section reads "COLLECTION" with the belongs-to "In the collection", and the add toast reads "X added to the collection." Collection gets no picker language; picker titles and add-parent pills on member panels fall back to generic words.
- Surfaces converted: panel Parents/Children/Peers section headers + counts + empty states, "+ Add parent" pill (now "+ Add manager" / "+ Add group" where the edge earns it), the ⊕ add tooltip, the parent picker's title/subtitle/field label/top-level option/"+ New …" hatch/save toast/"X updated." undo message (the picker takes the vocabulary as a parameter of the subject buddy), the add-buddy dialog titles and subtitles (keyed to the reference buddy), the new-buddy sheet's Place-in-tree tabs and hints (keyed to the reference buddy's type — an assistant reference gives Direct report / Peer / Manager, a person gives Child / Sibling / Parent, a group gives Member / Fellow member / Group), the section rail and hidden-fields labels, and the parent-row remove tooltip. Same commit, per the report's §6 flag: the raw "(kind)" suffix no longer leaks onto parent rows. No relationship structure, ordering, or behavior changed — words only.
- Kin groups are an explicit set in code (KIN_GROUPS: Ron & Mei, The Dell'Aquilas, Dave & Nancy, Em & Sarah) because the registry has no kin flag; every other people-group (Acquaintances, Testers) takes membership words. Verified with a headless probe — 44/44 assertions: org words on Astro/Finance/Money panels, membership on Joel/Acquaintances, family on the Ron → Kyle edge and Ron's "Siblings (1)", generic unchanged on the Accident and Cabin panels, collection on Car Buddy/MGA, plus the picker, add dialog, and sheet in each vocabulary, in dark and light.

### What's New sheet — summary + filter pills now sticky (Dave 2026-10-19)
- Dave, with a screenshot of the What's New sheet: "those filters should be sticky as the text scrolls up. currently they're not (that's a me bug i'll fix it)" — then handed it over: "you can fix the sticky filter issue. let you do it. i'm not going to do it."
- Root cause: the "New since you last looked" heading and the Added / Changed / Fixed count pills were ordinary in-flow content at the top of the sheet's one scrolling container (`.wn-body`), so they scrolled away with the entries they summarise.
- Fix: after the changelog renders, `openWhatsNew` wraps the heading + pills in a `.wn-sticky` container — `position:sticky`, pinned flush to the top of the scroll area directly under the title row, bled full-width with the sheet's panel background so entries pass cleanly underneath. The pills keep their existing filter wiring and counts; the Update button and dismiss are untouched. Verified with a headless probe (dark, light, and phone width): after scrolling the entries 600px the wrapper sits exactly at the title row's bottom edge, and from 600px to 2,400px of scroll the pills do not move a pixel; clicking the Fixed pill while scrolled still filters (102 Fixed entries shown, everything else hidden).

### New buddy: Persona Buddy 🎭 — keeper of the one canonical persona inventory (Dave 2026-10-19)
- Dave, during the new-buddy-sheet persona workshop: "we might need a persona buddy whose job it is to maintain the inventory of all the personas, suggest new ones, and group them... the new buddy sheet should not be limited to 24. It should be all of the personas we've currently got — that's why we are adding in a filtering mechanism." Stood up the same afternoon with the full drill.
- The job: one canonical inventory of every persona in the system. Ground truth at hire (harvested, not assumed): the sheet hardcodes 24 personas (REQUEST_PERSONAS in build.py) while 62 of 121 buddies wear 59 distinct personas scattered across registry persona fields — Jonny (Designer), Hawaiian bruddah (×3 buddies), Hans (×2) — and Astro's own voice (Smooth Handshake) is in no registry field at all. 16 of the sheet's 24 are already worn; 8 sit unworn on the bench.
- Persona: a Hollywood casting director — warm, sharp, encyclopedic about voices. Child of Project Buddy; icon 🎭. Job req in Buddy Docs, private repo (davedellaquila/persona-buddy) seeded with the standard file set + a KNOWLEDGE.md harvest of all 59 worn personas and the sheet's 24, CONFIG.md, and STUDY.md with the harvest as the first study topic. Registry at 122 buddies; generated homepage at persona-buddy/.
- v1 scope: harvest #1 (a card per persona — lane male/female/neutral, 2–3 trait pills from a shared vocabulary, voice id/sample, wearer(s)), grouping pass, gap report #1. The dashboard follow-on (sheet + panel picker reading from this inventory, with Dave's lane row + trait filter + per-tile playback) is a separate job.
- Side effect, same commit: the homepage generator refreshed 8 template pages (Project Buddy's children list gains Persona + Research Buddy; stale 🤖 fallback icons on Apple/Tech Buddy and family pages replaced with their real registry icons from the Oct 19 audit).

### Buddy panel ··· menu — top row no longer clipped off (Dave 2026-10-19)
- Dave, with a screenshot of the open ··· menu showing Open git repo / Mark dormant / Save to desktop: "looks like we lost the settings menu item in that sticky panel and the info panel — or maybe it's just being cut off on the top." It was cut off: the Settings item was rendered but sat above the visible area.
- Root cause: `.bp-more-menu` was `position:absolute` with no `top`/`left`, so it took its static position — and an abspos child of a flex container (`.bp-topnav`, `align-items:center`) gets its static position as if it were the sole flex item, i.e. *centred* on the 18px utility strip. The now-148px-tall 4-item menu therefore started ~55px above the sticky head, and the panel scrollport (`#view-buddy`, `overflow-y:auto`) clipped everything above its top edge — the whole Settings row. The 4th item (Open git repo) made the menu ~34px taller than the 3-item version and pushed the first row fully over the edge.
- Fix (CSS only, contents/order/handlers untouched): `.bp-topnav` is now `position:relative` — it becomes the menu's containing block — and the menu declares `top:calc(100% + 4px);left:0`, dropping straight below the strip, left-aligned as before. The menu lives inside the sticky head, so it stays glued under the ··· button when the panel scrolls. Verified with a headless probe (before: Settings rect top −11px, hit-test at its centre landed on the top chrome; after: all four items fully inside the viewport at panel-top and scrolled positions, dark and light).

### Buddy panel ··· menu — Settings wears the gear, plus "Open git repo" (Dave 2026-10-19)
- Dave, with a screenshot of the buddy panel's ··· menu (Settings / Mark dormant / Save to desktop): "use the gear menu, the same gear menu we're using for settings over on the buddy panel, for the settings item in this menu. also add 'open git repo' as one of the menu items."
- Settings: audited first — there was no divergent path to fix. Every settings entry point already funnels into the one `openFieldSettings()` sheet (#field-settings): the sidebar gear (#sb-gear), the ··· menu's #bp-settings, and the ⌘,/Ctrl+, toggle. So the item now simply *reads* as the same control: it carries the gear icon — the #sb-gear SVG artwork verbatim, via a new `gearSvg(size)` helper next to `circleX()` — as its leading glyph, in the same slot the 💤/💾 glyphs occupy on the items below it. Same click, same sheet, same state.
- New item "Open git repo" sits between Settings and Mark dormant, led by the GitHub octocat mark in currentColor (`ghMarkSvg(size)`). Its click handler follows the Save-to-desktop pattern (resolve the on-screen buddy from `S.sel`): it opens `https://github.com/davedellaquila/<repo>` in a new tab (noopener) using the displayed buddy's registry `repo` field, then closes the menu. A buddy with no repo renders the item disabled — greyed, inert, title "No GitHub repo for this buddy" — so the menu's shape stays stable from buddy to buddy instead of items appearing and vanishing.

### Collapsed sections hide their add buttons (Dave 2026-10-19)
- Dave, with a screenshot of the collapsed PARENTS header still wearing its "+ Add parent" pill: "don't show the add parent button when the section's in a collapsed state. show that when it's open."
- The parent section was the outlier: an override rule forced its `.attr-head` pill button always visible. It now follows the persona section's existing pattern exactly — the `[data-addparent]` "+ Add parent" pill is `display:none` until the section carries `.expanded`, then `display:inline-block`. The button, its picker dialog, and its handler are untouched.
- Same shape, same fix: the Children section's ⊕ (`.bp-circle-add`, `data-addbuddy="child"`) sits inside the `<h3>`, and h3-headed sections collapse by hiding everything *except* the h3 — so the ⊕ also stayed visible while the section was collapsed. It is now hidden while the section carries `.collapsed` and returns when the section is open.

### Add buddy — instant add + automatic setup (Dave 2026-10-19)
- Dave's direction after two of his adds (the 4 post lift) vanished into the request queue: "after I add a buddy, it should immediately show up in the list of buddies and on the buddy list panel." Rebuilt flow: tapping "Start the setup" in the ＋ sheet still files the inbox request, but the buddy now lands in the sidebar list, the Projects panel, and the buddy detail panel on that device the moment the request is safely on GitHub — toast: "Buddy added — setting it up now." A failed request write adds nothing (no phantom buddies), and the old "Request sent — Astro will pick it up shortly" copy is gone.
- How it works: the dashboard mints the buddy id client-side with the same slug rule the drill uses (slugifyBuddy — "4 post lift" → "4-post-lift") and carries it in the request JSON as `id`. A local placeholder entry (name, persona, placement, purpose as tagline/mission, status "Setting up", st-new pill, the picked persona's emoji as its icon — never 🤖) is stored per device in `S.pendingBuddies` (`buddyTree.v3`) and merged into the tree at boot; it is never written back to GitHub. Placement honours all three sheet modes — child, sibling, and parent (parent mode routes the ref buddy under the placeholder via the device-local S.parents override until the registry catches up).
- Reconciliation: when the real registry entry with that id lands, the placeholder retires at boot and real data wins silently — no duplicates, and re-adding a name that's already real files a reconcile request instead of minting a second buddy. Verified by a 26-check jsdom harness booting the built page (boot merge, sidebar + Projects + detail-panel rendering, all three placement modes, persistence across the store, real-id collision, re-add dedupe) plus a detail-panel probe — all passing.
- The other half: the `new-buddy-inbox-watch` cron no longer asks "Want me to run the full setup drill?" — that approval gate is removed. It reads the request's real fields (name, id, persona, purpose, place_mode, ref_buddy) and runs the full drill automatically with the request's exact id (registry insert, private repo, job req in Buddy Docs, homepage, side thread with INIT + review ask, HTML new-hire email), reconciling instead of duplicating when the id already exists, then posts ONE completion report with links in the main chat. The watcher's body also no longer asks for icon/kind request fields that never existed.

### New buddy: 4 post lift 🏗️ — Emil's Eagle 4-post lift gets its dossier (Dave 2026-10-19)
- Dave submitted this buddy twice from the dashboard (12:36 "Dads 4 Post Lift" and 12:53 "4 post lift") and it never got created — the inbox requests were filed but the setup drill never ran. Un-stuck today: full drill completed.
- The buddy is the living dossier for Emil's Eagle four-post lift: it lived at 18231 Llagas Creek Dr, Morgan Hill until AIM took it in October 2026 (who AIM is, where it's held, and on what terms are recorded as open questions). Exact model/capacity/year/serial were never supplied — they sit on the desk as open questions (data-plate photo settles them), never guessed.
- Child of Car Buddy; persona "Hawaiian bruddah" (Dave's pick); icon 🏗️. Job req in Buddy Docs, private repo (davedellaquila/4-post-lift) seeded with the standard file set; KNOWLEDGE.md carries the full Oct 2026 lift-move vendor research (8 vendors — top pick Edwards & Sons Automotive Equipment, Livermore; runner-up Dunkel Logistics) as the move playbook. Registry entry carries the job-req link in docs[] and a review attention item. Generated homepage at 4-post-lift/.

### One circled-✕ everywhere — the close mark is unified (Dave 2026-10-19)
- Dave: "the circle x marks in the panels should be the same — currently they're different." They were: the panels' close buttons were four different text glyphs (×, ✕, &times;) rendering in four different fonts/weights, while the sidebar's #sb-close wore the proper circled-✕ SVG.
- Fix: one shared `circleX(size)` helper emits the exact #sb-close geometry (circle r8.5 + round-capped X, stroke currentColor, stroke-width 2) and every close/dismiss control now uses it — buddy panel close (22), settings sheet close (20), chart picker + style picker closes (20), photo viewer close (22), "What's new" close (22), update banner dismiss (20), standing-order memo dismiss (16), Constellation panel collapse (16), pinned-tooltip close (14). Where a context is genuinely smaller, the identical SVG is scaled whole — never a different mark. All ids, aria-labels, titles, handlers and hover behaviours unchanged; colours stay currentColor-based so dark and light both read correctly.
- Deliberately left alone: the two search-field clear buttons (#buddy-search-clear, #proj-search-clear) and the inline item-remove chips (remove-parent pill, remove-nickname) keep their plain × — those are field/item micro-affordances, not panel closes; the "Tree pan gearing ×" labels are multiplication signs, not marks.

### Constellation — spacing control panel (Dave 2026-10-19)
- Dave: the Constellation chart's labels feel scrunched — he wants "some controls to tweak it a little bit, like a little control panel." The view now carries a small floating Spacing card in the chart's top-right corner (Kin-quiet: theme-var card, hairline border, soft float shadow, dark + light), collapsible to a "Spacing" pill so it never clutters the view; open/closed is remembered.
- Four sliders, all live: **Spread** (spring rest length, 50–180), **Push apart** (repulsion strength, 1000–8000), **Label size** (9–16px), **Label gap** (8–30). Moving one restarts the simulation (lightly debounced) so the effect is visible immediately; a Reset button restores defaults. Settings persist per device in `S.constellation` (`buddyTree.v3`), and the defaults are exactly the old hardcoded values (spread 90, repel 3200, 11px labels, gap 13) — nothing moves until Dave touches a slider.
- Implementation care: physics + label metrics now read from the settings object at init (`CS.spread` / `CS.repel` / `CS.labelSize` / `CS.labelGap`); a generation guard stops the previous sim loop when a restart replaces it on the same canvas; node positions are re-seeded from the last frame so tweaking makes the layout breathe instead of re-scattering; the canvas click handler is wired once and hit-tests the live `canvas._buddyNodes` map, so click-to-open and centerOnBuddy behave exactly as before. Growing the label font pushes its baseline down by the same delta, so the visible node-to-label gap stays honest.

### Sports Car Adventures placeholder — the calm refresh (Dave 2026-10-19)
- Dave's direction: "up it a little — nice imagery, something soothing, rolling hills of Amador; slow down is the message; calm, not racy, nothing to do with going fast."
- The racing dashed-road animation and driving 🏎️ are gone. In their place: one still hero image (sports-car-adventures/amador-hills.jpg — golden Amador foothills, valley oaks, an empty winding road at evening light) arriving with a slow 2.4s settle (disabled under prefers-reduced-motion), sticky slim header and dark + light themes kept.
- Copy now leads with the message: headline "Slow down."; lede "Unhurried drives through the golden hills of Amador County. Good cars, quiet roads, and nowhere to be but here."; the remodeling note stays, quieter: "We're remodeling — taking our time with it. Stay tuned." Page stays deliberately static (no token-gated write paths) so it stays mirror-clean.

### Homepage Prev/Next pair + circled-✕ sidebar close (Dave 2026-10-19)
- Homepage Prev/Next: with BOTH panels closed on a buddy homepage (body.sb-closed + body.bp-collapsed, homepage view), a Prev/Next pair appears in the lower-right corner — FAB-sized (56px), FAB frosted styling in both themes, sitting alongside the + button at the same baseline (right:88px), within thumb reach on iPad Pro. Visibility is CSS-gated on exactly that state (`body.sb-closed.bp-collapsed:has(#main.homepage-mode):has(#view-project.active)`), and the pair hides while Settings is open, like the FAB. Each tap steps through the current collection — the sidebar buddy list's displayed order, deduped (multi-parent buddies appear once) — loading the adjacent buddy's homepage via selectBuddy. No wrap-around: at the first/last buddy that direction's button dims (disabled), and its tooltip names the neighbour it will load. Left/Right arrow keys do the same walk in this state (the document arrow handler steps instead of jumping to the first/last sidebar row), including arrows forwarded from the homepage iframe. Deferred per Dave: a setting to move the pair to the lower-left corner.
- Sidebar close: the left panel's collapse chevron (‹) is replaced by a circled ✕ mark (an X inside a circle outline — not an Xbox logo) as the #sb-close glyph in the sidebar's upper-right tools corner. Same button, same setSidebarOpen / S.sbClosed behaviour and persistence; the collapsed rail's expand control (#sb-expand-btn) is untouched. The now-meaningless rotate-on-collapse rule and a vestigial .xmark-x rule were removed.

### Projects list — one row grammar: the pill gets a home (Jonny verdict, Dave 2026-10-19)
- Dave's directive from his iPad screenshot: the status pills were not aligned — put them on a consistent edge, the far right. Jonny's verdict (~/workspace/projects-list-cleanup/jonny-verdict.md) prescribed the full grammar; this ships it. Supersedes Jonny's own Oct 13 left-cluster arrangement.
- Row anatomy at every width: [grip 22px] [disclosure slot 32px] [icon + name] — [tagline] — [status column 152px, pill right-aligned] [ⓘ column 40px, 44px touch target]. The tagline moved inside the row head and is now the ONLY element that flexes/ellipsizes, so the Oct 13 "8px of air" rule is true at every width, not just ≤639px. Rows align on a centreline (align-items:center), not a baseline. Leaf rows reserve the disclosure slot (empty .parrow.leaf), so a leaf's name sits in the same column as its parent's.
- One status language: the registry's drifted statusClass dialects are normalised (active→st-active ×15, new→st-new ×10, amber→st-amber ×6, two missing keys filled) and the add-buddy flow now stamps st-new. CSS aliases (.status.active/.new/.amber) plus a zero-specificity :where(.status) default pill remain as a safety net, so any status — even a future wrong dialect — renders as the same pill. Rows for the five status-less buddies now read "Unknown" in the quiet grey st-idea pill (matching their filter tile) instead of the literal text "undefined". New fill: st-amber (warm amber).
- The root row's filled .d0 card is gone — Astro is a row like its children; hierarchy by indent alone. Indents are now true 24px steps (14/38/62/86), and phone cards keep their steps instead of flattening to 14px; phone cards carry the same anatomy (name + pill + ⓘ on the title line, tagline beneath at full width).
- Stat strip: status-tile labels wrap to two lines instead of truncating mid-word ("MISSION REVI…"), the strip scrolls with snap points so a tile is never left sliced, a soft right-edge fade says more lives here, and end padding lets the last tile rest fully in view.
- Both themes: .status gains html.light twins (the dark palette no longer sits on the white page), and the tagline colour comes from var(--muted) everywhere.

### Side panels — open/closed state now survives a refresh (Dave 2026-10-19)
- Dave: if the left panel is closed when he refreshes, it should still be closed after the page loads — and open should stay open. Root cause: the state lived only as body classes (`sb-closed` / `bp-collapsed`) toggled in the DOM; the sidebar *width* was persisted (`S.sbWidth`) but open/collapsed never was, and nothing re-applied the classes at boot.
- Fix: `setSidebarOpen()` (non-drawer branch) now persists `S.sbClosed`, and `setPanelCollapsed()` persists `S.bpCollapsed` — every toggle path flows through those two setters, so all of them save automatically. A pre-paint inline script right after `<body>` (mirroring the head theme script) re-applies both classes from `buddyTree.v3` before first paint at ≥640px, so there's no flash of the wrong layout; a boot-time `setSidebarOpen(false)` syncs width/tab/rail label through the normal code path, and `renderBuddy()` refreshes the collapsed panel's section rail for the restored buddy.
- Phone drawer (<640px) untouched — it stays session-transient by design.

### Hans homepage — custom workshop page replaces the template (Dave 2026-10-19)
- Hans (🧑‍🔧, hans-buddy/) gets a thread-owned custom homepage in place of the basic template: sticky header, dark + light, standard brain-dump box (dumps land in hans-buddy/docs/ingest.md).
- Mostly the BMW, as Dave asked: an "On the lift now" card for the E61 fuel-system job (Bosch LPFP in hand, install pending, fuel-smell leak hunt as job #1), a car spec table (2008 535xi E61, N54, 191,412 mi at last scan; VIN/colors marked awaiting Dave's records), standing PM orders, and workshop-library links (mission, repo, diagnosis, install guide).
- **The Patient's Chart** (Dave's charts directive): inline-SVG fault-code timeline vs. mileage — the 2AAF bar spanning 165,052→191,412 mi with 255 occurrences against 2A17's two blips near 191,119 mi. The chart makes the diagnosis: fix the bar, smoke-test the blips.
- Service-history section ships honest: a known-events timeline (diagnosis → parts → pump arrival) plus a Records Wanted panel — Airtable service records, the Google Sheet parts list from the major service ~2 years ago, and the VIN. Hans has a daily nag armed until Dave hands them over.

### Release Notes — filter tiles stick like Money Buddy's filter cards (Dave 2026-10-19)
- The New / Today / All filter tiles now stay pinned at the top of the Release Notes view while the list scrolls underneath, patterned on Money Buddy's sticky filter cards: the tiles ride on the page background so the notes slide cleanly beneath (no see-through gaps), and Money Buddy's soft float shadow (0 10px 24px rgba(10,20,15,.14)) fades in only while the card is actually stuck.
- A 1px IntersectionObserver sentinel above the tiles toggles the .stuck shadow — Money Buddy's scroll-handoff idea, adapted to a position:sticky element; at rest the tiles sit exactly where they did (padding + margins sum to the old 16px/20px spacing).
- Companion fix: the releases section now uses overflow-x:clip instead of hidden — a hidden overflow turns the section into a scroll container, which silently disables sticky positioning inside it.

### Buddy icons — every registry entry now carries a real icon (Dave 2026-10-19)
- Dave (on iPad): several buddies appear icon-less. Audit found three distinct causes. (1) Six entries still carried the 🤖 placeholder the dashboard's add-buddy flow stamps by default (the ADD_ICONS palette leads with 🤖 and nothing later required a real pick): Tech Buddy 📱, Ron & Mei 👫, Dave & Nancy 💑, Em & Sarah 💞, Sawyer's 🧢, Apple 🍎 — all now assigned. (2) Three of Dave's named buddies (Health Buddy 🏥, Hot Tub Buddy ♨️, Larry Osana 🔑) already had registry icons — their icon-less appearance is in the side-chat list, whose thread titles predate the emoji-prefix convention; retitling is a chat-side fix, not a registry one. (3) Event Buddy, Shannon Essex, and J&C Custom Cabinets have no registry entries at all — they exist only as chats, so the dashboard has nothing to show for them; registering them is a separate new-buddy call.
- Also noted: buddyDisplayIcon falls back to '' (blank) in the sidebar when an entry has no icon, while other renderers fall back to 🤖 — with every entry now iconned, the blank path is unreachable from registry data.

### Atlas lens picker — tapping the pill on iPad appeared to do nothing (Dave 2026-10-19)
- Root cause: the lens dropdown lived inside .atlas-controls, whose backdrop-filter makes the row the containing block for fixed-position children and whose overflow-y:hidden then clips them — the picker unhid but was clipped invisible inside the 44px row. Same trap the dot popovers escaped on Oct 18.
- Fix: wireAtlasRow now moves #lens-dropdown and #lens-scrim to document.body alongside the dot popovers, and the fixed-position rules target #lens-dropdown directly (top:68px under the row; phone keeps the bottom sheet via top:auto).

### Info panel — a shown/added field arrives open (Dave 2026-10-19)
- Restoring a field from the Hidden fields tray now lands it in an open state — no second click to expand it. The show-field handler sets both state maps for that field (secCollapsed=false for h3 sections, attrExpanded=true for attr-head sections) before saving and re-rendering; every other section keeps its remembered state.

### New buddy — Research Buddy 🔍 (hired 2026-10-19)
- The standing research desk: sourced investigations, background checks, product/market research, confidence-tagged reports (web page + HTML email). Direct child of Project Buddy; registry at 120 buddies. Founding case: the John Windsor background check.

### Info panel — Voice/Persona headers show the selected value when closed (Dave 2026-10-19)
- Single-value pattern: a closed section header reads "VOICE: Neighborly Syrup" — the Change pill no longer sits in the header crowding out the value. Change moved into the open body (next to Preview / Surprise me), where the pickers already offer the reset path ("Default voice" / "No persona").

### Info panel — Hidden fields tray: alphabetical + whole-row restore (Dave 2026-10-19)
- Hidden fields now list alphabetically by label.
- Clicking anywhere on a hidden-field row restores the field (data-show-field moved from the "show" button to the whole row; the button stays as the visible affordance); rows show a pointer cursor.

## 2026-10-18
### Info panel — every field now reorderable from the panel; Buddy fields removed from Settings (Dave 2026-10-18)
- The compact attr-head headers (About, A.K.A., Parents, Persona, Voice, Private notes, Shared notes) now carry the ⋮⋮ drag grip, so every field can be reordered right from the info panel — previously Settings was the only reorder path for these.
- The "Buddy fields" section is gone from the Settings sheet (hide/show already lives in the panel via the hide links + Hidden fields tray). "Main views" stays.

### Info panel — hide/show fields right from the panel (Dave 2026-10-18)
- Every section header now carries a quiet "hide" link (appears on hover; always visible on touch). Clicking it hides that field immediately — no Settings detour.
- A "Hidden fields (n)" tray appears at the bottom of the field list whenever fields are hidden; expanding it lists each hidden field with a "show" button to bring it back.
- Uses the existing S.fieldHidden mechanism (same store Settings uses), so panel and Settings stay in sync.

### Atlas control strip — centered in the main view
- The control strip (Lineage picker, color dots, zoom, utilities) is now centered horizontally in the main view (was: pinned to the sidebar's right edge).
- Dave accepts panels may obscure it when open — no dodging.

### Document cards — delete button now visible
- Bug fix (via Event Buddy from Dave): uploaded documents had no visible way to delete. The trash button was hover-reveal only on photo tiles (.pwrap:hover) and document cards (.doc-card) never matched, so it was permanently invisible — also unreachable on touch.
- Fix: the trash icon now always shows on document cards.

### Upload progress — clearer feedback for photos & documents
- Photo uploads: the progress tile now shows a live percentage, the current filename, and a pulsing accent ring while the upload is in flight (was: bar + count only).
- Document (PDF) uploads: new animated progress card in the Documents strip — filename, progress bar, percentage + count — instead of status-text-only.
- Via Event Buddy from Dave's feedback: upload progress should clearly indicate something is happening and how far along it is.

### Collapsed icon rail floats vertically centered (Dave 2026-10-18)
- The collapsed sidebar's icon rail was top-anchored (12px from the top), leaving a long empty tail below the icons. It now floats vertically centered (`top:50%; transform:translateY(-50%)`) — per Dave's annotated screenshot feedback on the Scaffold Buddy homepage.

### Documents section — PDF uploads for buddies
- New 'Documents' section below Photos on the buddy info panel: drop PDFs or click to choose.
- Uploads to docs/<id>/ in the buddy-system repo (or docs/ in the buddy's own repo) via the GitHub token flow.
- Renders as document cards with filename, size, Open link, and delete. Sits in Settings field ordering right after Photos.

### Briefing Buddy — evening refresh
- Evening snapshot: "Next" tile now the 6 PM lineup; morning card retitled "Coming up today".
- Audio synced to the Oct 18 morning standup (3:28); evening charts regenerated.

### Seven dashboard fixes (Dave 2026-10-18)
- **Auto-close sidebar setting**: new "Auto-close sidebar on buddy select" toggle (default off). When on, selecting a buddy collapses the sidebar to the icon rail so the homepage/view gets the full screen. Skipped for the phone drawer (which already closes on selection).
- **Settings field-order scroll**: rearranging fields in Settings re-rendered the whole panel and lost the scroll position. The dropped row is now scrolled back into view (`scrollIntoView({block:'nearest'})`) so you can see where it landed. Same for the Main views list.
- **Section state survives record navigation**: the About/mission field (and other attr-toggle sections) used a DOM-only `expanded` class that was wiped on every re-render. Expanded state is now persisted per field (`S.attrExpanded`) and restored in `applySectionCollapse`, alongside the existing h3 collapse state.
- **Atlas controls pinned to the sidebar's right edge**: the control row was absolutely positioned at the pane's top-left, sliding under the floating sidebar. Now pinned to the sidebar's right edge — 360px open (floating), 348px anchored, 88px collapsed rail, 12px on phone — with max-width adjusted so it never overflows the pane.
- **Info panel rename focus**: the name input carried a vestigial `data-buddy` attribute, and the document click handler's `fc === bb` guard let it through — every tap re-opened the buddy, destroying the input before a keystroke could land. Removed the attribute and hardened the guard so form controls never re-trigger the panel.
- **Astro searchable**: the sidebar autocomplete explicitly excluded the root (`if (b.id === ROOT_ID) return false`). Astro now appears in search results like everyone else.
- **Astro as the root tile**: the org chart rendered the staff side by side with no root. Astro now renders as the root node at the top (tagged "root"), with the staff hanging under him.

### Fixed — hiding a tree pane now gives the other the full screen (Dave 2026-10-18)
- Hiding the lower (orphan) pane via the pane toggles gives the Atlas chart the full pane height — and hiding the chart gives the orphan pane the full height. The surviving pane gets `flex: 1 1 0` and the splitter hides with the second pane.
- Fixed the resurrection bug: `applyTreeSplit()` ran on every tree re-render and unconditionally re-showed a hidden pane (plus the checkbox disagreed with reality). Visibility now lives in one place — `applyTreeSplit()` reads `S.treePanes` itself, so toggles and re-renders always agree, and a hidden pane survives reloads.
- Guard: the toggles refuse to hide the last visible pane ("Keep at least one pane visible.") so the view can never strand itself empty.

### Atlas control row — six rows collapsed to one (Jonny's verdict, Dave's greenlight)
- New `.atlas-controls` toolbar, anchored top-left of the Atlas pane (12px/12px): lens pill → orientation glyphs → bg/tile color dots → zoom slider → fit/fullscreen/recenter utilities. 44px tall, 22px radius, blurred material, hairline, whisper shadow. 8px within groups / 24px between, no dividers. Horizontal scroll under ~720px pane width.
- Pill keeps the current lens name + ▾ (the unexplained blue dot is gone — punch #4); "Atlas" goes in the view chrome as the view title.
- Orientation is now drawn node glyphs (vertical/horizontal), visible ONLY for the org lens — absent elsewhere, not disabled (punch #7).
- Color dots: 28px dots in 44px targets filled with live color, no labels; tap opens an anchored popover (desktop/iPad) or bottom sheet (phone) with presets + custom picker + reset (punches #8, #9).
- Zoom: mismatched end caps deleted (punch #6); 140px slider (96px min); three 44px line-icon utility buttons with tooltips — fit, fullscreen (new), recenter (punch #5).
- Ride-along fixes: Quick Answers chips get `flex:none` so they never squeeze to 2-char labels (punch #2); chrome top clearance so the strip never clips (punch #1).

## 2026-10-18
### Fixed — collapsed rail no longer obscures content
- The collapsed left-panel rail (64px floating icon strip) was overlapping page content — reported by Dave on the Car Buddy homepage view at iPad width. Homepage mode strips `#main` padding to zero, so the rail covered the first ~76px of the iframe.
- Now `body.sb-closed #main` (and `#main.homepage-mode`) gets `padding-left:88px` (12px rail offset + 64px rail + 12px breathing room), so content clears the rail in every view.

### Briefing Buddy — per-page type size control
- New "Ag" segmented control in the masthead (next to Theme): smaller / small / medium / large, applied via CSS zoom on <html>.
- Each page keeps its own size (localStorage `buddyTree.typeSize`, keyed per page from URL path); optional global default, per-page always wins.
- Ships as a reusable snippet (snippets/type-size-snippet.html) for rollout to other buddy pages.

# Changelog

## 2026-10-18 (DPG entity question resolved)

### Fixed
- **Dell'Aquila Performance Group = Dell'Aquila Garage** (Dave 2026-10-18): the two names are the same venture — Quentin and Sawyer's shop; they use both, more aliases possible. Recorded as interchangeable in the DPG repo's KNOWLEDGE.md; the entity-question Needs Attention tile removed from the [DPG homepage](https://davedellaquila.github.io/buddy-system/dpg-shop-software/) and from the registry attention list.

## 2026-10-18 (DPG Shop Software buddy)

### Added
- **DPG Shop Software buddy** (🔧, Dave 2026-10-18 — "create a desk for it", from his DPG Shop Management Software PRD v1): the shop management platform for the Porsche/BMW performance shop — customers, vehicles, estimates, repair orders, scheduling, technicians, parts, invoicing, payments, plus performance-shop workflows (build profiles, mod history, track prep, alignment specs, dyno results, tuning references, reusable Porsche/BMW service packages). Direct child of Project Buddy. Private repo davedellaquila/dpg-shop-software (KNOWLEDGE.md seeded from PRD + memory: Quentin's Performance Technic floor experience, Sacramento-area target, MVP-first strategy; CONFIG.md in the standard Identity/Behavior/Scope/Preferences/Privacy shape; STUDY.md with 3 queued topics). Custom homepage at dpg-shop-software/ with the full desk treatment — 🗂️ The Desk renders KNOWLEDGE.md + CONFIG.md + STUDY.md live from the repo, editable in place via token-gated GitHub API (token stays on-device) — plus a shop board (core ops / performance workflows / V1–V5 roadmap), two attention items (mission-statement review, the open Dell'Aquila Performance Group vs Dell'Aquila Garage entity question), and a 🧠 brain-dump box. Sticky slim header, working dark mode via prefers-color-scheme, generator-skip marker (no BUDDY-BASIC-TEMPLATE, no "Part of the Buddy System"). All 4 inline scripts pass `node --check`. Registry now at 119 buddies.

## 2026-10-18 (dump box: failed GitHub writes queue locally + token verified on paste)

### Fixed
- **Failed GitHub dumps no longer vanish into an error message** (Dave 2026-10-18 — "Save failed: GitHub 404" on a buddy homepage, and no notice that anything was stored locally): the dump box's write-failure path never queued the entry — the "dumping always works" guarantee only covered the no-token/no-repo cases. Now a failed GitHub write saves the dump to the device's localStorage backlog, clears the box, and says so in plain words with the backlog count ("Saved on this device — … (N on this device waiting to sync)"); the backlog flushes into `docs/ingest.md` on the next successful dump. A 404 gets a specific hint (usually a wrong/expired token or no access to the private repo).
- **Token is verified the moment it's pasted** (same report — the 404 was a rejected token): pasting a GitHub token into the dump box now calls `GET /user` immediately. A good token shows "Token verified — dumps will sync to GitHub"; a rejected one warns in place and dumps stay local until a working token is added. Catches bad tokens at paste time instead of on the next dump.
- Rolled out to all 110 pages carrying the dump box (58 template pages regenerated from the fixed `gen_basic_homepages.py`, 52 custom pages patched surgically, `docs/dumpbox-snippet.html` refreshed as the canonical reference). All 110 dump-box scripts pass `node --check`. Also fixed a `lsjSet` typo that broke token saving on the news-buddy page.

## 2026-10-18 (homepage name-sync reads pending renames)

### Fixed
- **Renamed buddies now show the new name on their homepages** (Dave 2026-10-18 — renamed a buddy, refreshed its homepage, old name persisted): when the dashboard has no GitHub token, renames queue in localStorage (`S.pendingRenames`) and never reach `buddies.json`, which is the only place homepages looked. The name-sync snippet (all 64 pages carrying it, template + custom) now reads the dashboard's localStorage queue first — same origin — and a pending rename supersedes the registry name. Generator's `NAMESYNC_JS` updated so future pages ship it.

## 2026-10-18 (info panel: editable name fix + floating sheet)

### Fixed
- **Info-panel buddy name now editable on iPhone** (Dave 2026-10-18 — tapping the name field did nothing): the name was a `contenteditable` h2, which iOS Safari refused to focus. Replaced with a native text `<input>` styled identically (same `.bp-name` bottom-border affordance); rename logic unchanged (Enter or blur commits, still writes through to the registry via `writeGlobalName`).
- **Info panel floats on phone** (Dave 2026-10-18 — the full-bleed sheet read as a separate screen): `#view-buddy.sheet` now uses 12px insets on all sides with 16px radius and an all-around shadow, mirroring the left sidebar drawer's floating pattern — the panel clearly sits on top of the main view instead of replacing it.

## 2026-10-18 (Dave Swiger buddy)

### Added
- **Dave Swiger buddy** (🎱, Dave 2026-10-18 ~1 AM — "create a desk for him"): Wildlife Trail neighbor in Fiddletown, "a great guy." Living dossier under Acquaintances (kind: personal). Key facts: birthday October 14; drives a Mazda Miata (ND); homebrews his own beer; hosts pool night every once in a while on Friday nights; into astronomy; formerly at Google (laid off). Private repo davedellaquila/dave-swiger-buddy (KNOWLEDGE.md, CONFIG.md, STUDY.md). Custom homepage at dave-swiger-buddy/ with the full desk treatment — 🗂️ The Desk renders KNOWLEDGE.md + CONFIG.md + STUDY.md live from the repo, editable in place via token-gated GitHub API (token stays on-device) — plus key-facts grid, important dates, and a 🧠 brain-dump box. Sticky slim header, working dark mode via prefers-color-scheme, generator-skip marker (no BUDDY-BASIC-TEMPLATE, no "Part of the Buddy System"). Registry now at 118 buddies.

## 2026-10-17 (Briefing Buddy link-everything)

### Added
- **Link every named thing on every tile** (Dave's directive 2026-10-17, verbatim): all named entities on the Briefing Buddy homepage now link inline — Fiddletown→Google Maps, Orionids + Wild Duck Cluster→Wikipedia, S&P/Nasdaq/Dow→Yahoo Finance quote pages, News Buddy→its homepage, the briefing-buddy repo→GitHub, 49ers→49ers.com, Reddit→reddit.com, the Briefings thread→its chat. Entities with no natural destination (Dave, Alex + Jordan, Astro, iPhone Duo, PRD) left plain — no invented destinations.

## 2026-10-17 (Briefing Buddy per-tile quick links)

### Added
- **Per-tile quick links on the Briefing Buddy homepage** (Dave's feedback 2026-10-17 — "i don't see any links on the individual tiles"): each live-data tile now carries its natural next steps inline as pill links — full forecast (weather), sunrise/sunset + moon phase (sky), tonight's sky (night sky), NWS alerts + air quality (fire & air), Yahoo Finance (AAPL), the Briefings thread (awaiting-reply), edition details (next edition). Referenced documents are now linked in place: `docs/ingest.md` in the brain-dump lede, the product brief in the PRD card and on-my-mind lede. All external links verified returning 200 before wiring.

## 2026-10-17 (Sports Car Adventures + Dellaquila.com buddies)

### Added
- **Sports Car Adventures buddy** (🏎️, Dave 2026-10-17 — "we're going to need sports car adventures"): the sports-car driving experience brand. A brand, NOT a registered business (Dave's words — a fact, not an open question). Mission statement, private repo with seeded knowledge base (2026 business plan concept: Turo + DriveShare sourcing, owner/client relationships, matchmaking/routing/operating layer; events@sportscaradventures.com daily monitor; sportscaradventures.com domain). Public teaser homepage at sports-car-adventures/ — "going through a bit of a remodeling, stay tuned" — deliberately static so Dave can point domains at it.
- **Dellaquila.com buddy** (💼, Dave 2026-10-17 — "my official business that i file my taxes with"): the business's desk. Homepage IS the desk: KNOWLEDGE.md + CONFIG.md rendered live from the private repo, editable in place via token-gated GitHub API (token stays on-device). Tracks both entities — the dellaquila.com tax/legal entity (FTB $800/yr deductible, Schedule C line 23; Money Buddy CPA reports are the books→preparer pipeline) and the Sports Car Adventures brand. Plus a 🧠 brain-dump box writing to docs/ingest.md.
- Both buddies linked to each other (many-to-many links[]); registry now at 117 buddies.

## 2026-10-17 (Learning Buddy spark shuffle)

### Added
- **Curiosity-queue spark shuffle** (Dave 2026-10-17 — "mix them up every time"): the "What do you want to learn?" hero's suggestion sparks now draw 6 at random from an 11-spark pool (original 6 + Spanish, SwiftUI, Sourdough, Storytelling craft, Documentary filmmaking — teased from his threads), reshuffled on every visit, plus a ↻ shuffle link; tapping a spark still fills the ask box.

## 2026-10-17 (Property recurring chores)

### Added
- **Recurring chore lists on property homepages** (Dave 2026-10-17 — "every property is going to need its own schedule of routine maintenance"): Cabin Buddy and Lenwood Buddy homepages now have a "🔁 Recurring chores" section grouped by cadence (Weekly / Monthly / Quarterly / Seasonal). Cabin seeded from known rhythms: hot tub treatment + filter checks, Thursday trash, weekend street cleanup, monthly filter wash, quarterly water-filtration filters, fall leaf burns, spring weed clearance. Lenwood starts thin (rent collection, seasonal walkthrough) — Dave to fill in.

## 2026-10-17 (Attention tile quick-link actions)

### Added
- **Quick-link actions on "Needs your attention" tiles** (Dave 2026-10-17 — "include logical quick links in the tiles"): attention items now support an `actions[]` array — each action is a pill button rendered under the tile text. URL actions open externally; buddy actions navigate within the dashboard. First live example: Hot Tub Buddy's filter-replacement reminder carries "Buy filters" and "Buy UV bulb" buttons with the researched retailer links.

## 2026-10-17 (Main-view Background picker)

### Added
- **Background picker for the main view** (Dave 2026-10-17 ❤️): the tree toolbar now has a "Background" picker — a color swatch opening the system color picker, six presets (Ink, Slate, Forest, Wine, Sky, Paper), and a Reset button that appears once a custom color is set. Picking a color repaints the main view background immediately, no Apply step; the choice persists per device in localStorage alongside other settings. (The mirror previewed this first; this is the real build on the live dashboard.)

## 2026-10-17 (Tile color picker label)

### Fixed
- **Tile color picker now labeled** (Dave 2026-10-17 — tapped the color dot expecting the main-view background to change; nothing seemed to happen): the org-chart tile background picker had no visible label — just a color swatch, with its purpose only in a hover tooltip (invisible on iPhone). It now reads "Tile color" next to the swatch so its job (recoloring buddy tiles, not the main view) is obvious.

## 2026-10-16 (Hong Kong Palace buddy)

### Added
- **New buddy: Hong Kong Palace** (Dave 2026-10-16 — "I assume that Hong Kong Palace is a new object. New buddy."): Chinese restaurant in San Andreas, CA, under Amador County (local-places parent, Crush Pizzeria precedent). Homepage carries the first-visit notes (Oct 16, 2026 — egg drop soup + BBQ pork combo plate, Dave's verdict: very good, giant plate) and a photo gallery with the three dinner photos.

## 2026-10-16 (Legal Buddy: Open Matters list)

### Added
- **Open Matters section on the Legal Buddy homepage** (Dave 2026-10-16 — he expected a list of projects with their status): two matter cards at the top of `legal-buddy/` — "Buddy name clearance" and "Buddy OS full risk assessment" — each with a status pill ("Research complete · awaiting review"), opened date, and a link to its full detail page (the published artifact reports). Both artifact reports were shared to public links so the cards can reach them; unshare anytime. Chat replies stay the short version; the pages are the deep dive.

## 2026-10-16 (Zoom control pinned)

### Fixed
- **Zoom control no longer slides around** (Dave 2026-10-16): the Atlas zoombar was centered (`left:50%`) with a `left` transition plus a panel-open re-centering rule, so it visibly slid whenever the pane resized or the info panel opened/closed. It is now pinned top-left of its pane (`left:12px`, no transform, no transition, no panel-shift) — one fixed horizontal position, always. Top-left keeps it clear of the info panel sliding in from the right (this supersedes the "Zoombar: centered" change from earlier today — centering and a fixed position are mutually exclusive). Mobile keeps its right-anchored placement (now with explicit `left:auto`).

## 2026-10-16 (Zoombar: centered)

### Changed
- **Zoom controls centered** (Dave 2026-10-16): the Atlas zoom bar now sits centered at the top of each pane instead of tucked right. When the info panel is open, it re-centers in the remaining visible width.

## 2026-10-16 (Collapsed rail: back to left)

### Changed
- **Collapsed sidebar rail back on the left** (Dave 2026-10-16): this morning's batch had moved it right to avoid covering the main view's menu pills — Dave wants it left. Reverted, along with the buddy-panel rail dodge that went with it.

## 2026-10-16 (Gallery thumbnails + lightbox)

### Changed
- **Gallery goes fast** (Dave 2026-10-16 — 3.5MB images were slow): the grid now loads 40KB thumbnails (auto-generated at build time into `photos/<id>/thumbs/`); tapping one opens the full image in a lightbox (backdrop/Esc/× to close) instead of a new tab.

## 2026-10-16 (Social Media Buddy homepage: chart embedded + generator-trap fix)

### Fixed
- **Social Media Buddy homepage restored** (2026-10-16): commit e209ba2's gallery generator run wiped the custom homepage back to the template — the skip-check matches the literal phrase "Part of the Buddy System", which the custom footer contained. Restored the thread-owned design (marker removed) with a footer that avoids the phrase, and documented the trap in AGENTS.md.
- **Post Pipeline chart embedded**: 📊 Charts Buddy's Kin-language funnel (pipeline-light/dark.png, dark/light swapped via `<picture>`) now sits in its dedicated section, built from real queue counts (14 drafted).

## 2026-10-16 (Gallery: public photo URLs)

### Fixed
- **Gallery photos 404'd** (Dave 2026-10-16): the baked URLs came from the buddy's private repo with expiring `?token=` params. Photos are now mirrored to the public `buddy-system/photos/<id>/` (same place the dashboard info panel looks), and the generator prefers those clean public URLs. Ford's 3 photos verified loading (HTTP 200).

## 2026-10-16 (Social Media Buddy homepage refresh)

### Changed
- **Social Media Buddy homepage** (Dave 2026-10-16): replaced the BUDDY-BASIC-TEMPLATE v2 page with a custom thread-owned design (marker removed — the generator will no longer overwrite it). Centerpiece is the live post queue: pipeline strip (Ideas 0 → Drafted 14 → Awaiting review 0 → Scheduled 0 → Posted 0) plus the 14 LinkedIn Teaser Bank posts with dates and status chips (Post 5 hold/consent, Post 14 hold/Ko-fi flagged). A "Post Pipeline" chart section waits on 📊 Charts Buddy's Kin-language delivery (re-pinged 2026-10-16 with real counts). Standard brain-dump box, mission + docs links (mission statement, rollout plan, brief, teaser bank, repo), sticky header, dark+light via prefers-color-scheme, responsive.

## 2026-10-16 (1931 Ford Model A sale page — draft)

### Added
- **Sale page draft** (Dave 2026-10-16): `model-a-buddy/sale/` — a for-sale page designed from Johnny's council brief (docs/sale-page-brief.md): Bonhams-arc story (Emil the steward → evidence of care → the handoff), single facts object with "To be confirmed" unknowns, no price, walk-around gallery, trust signals (REG 5 stated plainly, inspection by appointment, enclosed transport, documentation inventory), and Enquire / Book an inspection / Call Dave CTAs. Warm paper / charcoal / oxblood / brass; dark+light first-class; banned words honored; no exclamation marks.
- Gallery mixes Dave's 3 real repo photographs (front 3/4 hero, rear 3/4, interior) with 2 clearly labeled AI visualizations (profile, engine bay) and 3 "photograph coming" slots. Draft banner throughout — not the live listing. Placeholder manifest lives in the model-a-buddy repo (docs/placeholder-manifest.md).
- Default buddy page now links to the sale draft (surgical "For sale — private treaty" card + docs[] entry).

## 2026-10-16 (Dump box: Enter submits + save flash)

### Changed
- **Brain-dump box: Return now dumps** (Dave 2026-10-16): pressing Enter in the dump textarea submits like the Dump button; Shift+Enter inserts a newline. A hint line under the button says so.
- **Save confirmation** (Dave 2026-10-16): the Dump button flashes green with "✓ Saved" for ~2s on every successful save (local or repo), and the status line goes bold green — previously only a small muted status line changed, which Dave missed.
- Rolled out to all 57 generator-managed buddy pages (including the v3 1931 Ford Model A dossier page and the legacy family page) via surgical constant replacement; the generator source carries the new behavior for future regens. Also fixed the generator's stale `indent=1` buddies.json write to match the file's actual `indent=2`.
- Thread-owned custom pages (~46) keep their own dump-box copies per the Oct 15 convention — their threads can adopt the same snippet.

## 2026-10-16 (Template gallery)

### Added
- **Photo gallery on the default homepage template** (Dave 2026-10-16): template pages now include a Photos section (grid, tap to enlarge) when the buddy has photos — pulled from the registry `photos[]` seeds plus the buddy repo's `photos/` folder, baked in at generation time. 3 buddies have photos today: Model A, ML500, Charts. (This is template-generator territory — if Kea spins up, it owns this.)

## 2026-10-16 (1931 Ford Model A rename)

### Changed
- **Buddy renamed** (Dave 2026-10-16 — drop "Buddy"): `model-a-buddy` is now **1931 Ford Model A** on the dashboard, in its side-chat title, and across its pages. ID (`model-a-buddy`), repo, and dashboard path are unchanged — display rename only. Dashboard rebuilt; embedded registry verified at 112 buddies.

## 2026-10-16 (Homepage iframe: white flash fix)

### Fixed
- **White flash between buddies** (Dave 2026-10-16 — still seeing it intermittently after the Oct 14 frame-background fix): the browser paints the iframe white during navigation before the new page's CSS loads; slower/uncached pages flashed longer. The iframe now starts at opacity 0 and fades in on load (src is set after the load listener attaches), plus `color-scheme:dark light` so the blank navigation page matches the theme. You see the dashboard background briefly instead of white.

## 2026-10-16 (Search: single clear button)

### Fixed
- **Sidebar search had two clear buttons** (Dave 2026-10-16): the `type="search"` input drew the browser's native circled × alongside our custom ×. Native one is now hidden via CSS; only ours remains.

## 2026-10-16 (Tip jar victory lap)

### Changed
- **Tip jar races across the screen** (Dave 2026-10-16): a jar clone now zips left-to-right across the viewport trailing smoke puffs (💨/☁️), with a slight tilt. Fires on click (alongside the poof explosion) and once ~2.5s after page load as a hello. Respects prefers-reduced-motion.

## 2026-10-16 (Tip jar delight)

### Changed
- **Tip jar goes full delight** (Dave 2026-10-16 — "get creative"): "Tip the jar" text now flows through animated rainbow colors; hovering spins the jar emoji 360° with a springy bounce and makes the text flicker with a warm fire-glow; clicking triggers a poof explosion (sparkle particles burst outward, the jar shrinks and vanishes) before opening ko-fi. Respects prefers-reduced-motion.

## 2026-10-16 (Tip jar: pinned flush, frosted)

### Changed
- **Tip jar pinned + frosted** (Dave 2026-10-16 — the tip jar floated above a big empty gap; wanted it flush with the sidebar's bottom edge and frosted): `.sb-tipjar` is now `position:absolute;bottom:0` (always flush, no gap), with a frosted-glass fill (`color-mix(var(--panel) 78%, transparent)` + 20px backdrop blur) so scrolling list rows show through softly without hurting readability. Sidebar gets `padding-bottom:52px` so content never hides under it.

## 2026-10-16 (New-parent button in the parent picker)

### Added
- **➕ "+ New parent…" in the change-parent picker** (Dave 2026-10-16 — the filterable parent list had no way to create a parent that isn't there yet): the Change/Add parent dialog now has a "+ New parent…" button next to Cancel/Save. Change mode opens the existing "Add a parent" dialog (new buddy created above, current buddy reparented under it); Add mode creates the new buddy as a peer and adds it as an additional parent via the parent override. `openAddBuddyDialog`/`createBuddyFromDialog` take an optional `onCreated` callback; existing callers unaffected. Dashboard rebuilt; main script node-checked.

### Fixed
- **New parent now visible immediately** (Dave 2026-10-16 — two symptoms after creating a parent from the picker: the info panel still showed the old parent, and the new parent didn't appear in left-panel search): (1) the creation wrote `byId[].parent` directly, but a stale `S.parents` override from a previous picker change shadowed it via `effParents` — the reparent now routes through `applyParentOverride`, exactly like the picker's Save; (2) the local stub was only added after the GitHub round-trip finished, so nothing appeared for several seconds — the stub (BUDDIES/byId/override) is now created first and the panel/tree/search re-render immediately, with the GitHub write following; on a write failure the stub rolls back and a plain-English toast explains why. Dashboard rebuilt; main script node-checked.

## 2026-10-16 (Atlas: rail right, horizontal zoom, pane toggles, Tab cycling)

### Changed
- **Mini rail moved to the right** (Dave 2026-10-16 — the collapsed sidebar rail was obscuring the main view's menu pills): the collapsed rail now docks to the right edge (`right:12px`) instead of the left. The buddy-panel section rail (`#bp-rail`) docks to the bottom-right when the sidebar is collapsed to avoid collision.
- **Horizontal zoom bar** (Dave 2026-10-16 — "rotate it again so that it's horizontally oriented and just tuck it in the right corner"): the Atlas zoom controls are now horizontal, tucked into the top-right corner of each pane (chart and orphaned), aligned with the top edge. Slider runs ▪ (left) to ◼ (right); fit and center buttons follow.

### Added
- **Pane toggles** (Dave 2026-10-16 — show/hide the Atlas chart and orphaned subviews): two toggle switches in the view nav (visible only when Atlas is active) — "Chart" and "Orphaned". Each pane (and the splitter) shows/hides independently; state persists. Either, both, or neither can be on.
- **Tab cycles the filtered buddy list** (Dave 2026-10-16): with the `/` search focused, Tab jumps to the first match, each subsequent Tab moves to the next (Shift+Tab goes backwards), wrapping around at the ends. Focus stays in the search field. ArrowDown still jumps to the first match.

## 2026-10-16 (Tip jar readability)

### Fixed
- **Tip jar background** (Dave 2026-10-16 — the sticky "Tip the jar" footer was transparent, so buddy list rows scrolling underneath showed through and made it hard to read): `.sb-tipjar` now always uses the solid panel background (`var(--panel)`), not just in the anchored-sidebar state.

## 2026-10-16 (Live rename propagation + homepage refresh controls)

### Added
- **Live rename propagation** (Dave 2026-10-16 — "can you force a web page to update without me having to refresh it?"): the dashboard now broadcasts every global rename via `localStorage` (`buddyTree.rename`). Open buddy homepages (separate tab or the dashboard's embedded Homepage view — same browser, same origin) listen for the storage event and update their displayed name instantly, no refresh needed. Other devices/browsers still pick the rename up on next load via the existing `buddies.json` fetch. Template pages regenerated with the listener baked in; custom-page threads are being sent the updated snippet.
- **Homepage refresh controls** (Dave 2026-10-16 — "is there a control to refresh a buddy's web page?"): the dashboard's Homepage view now has a "↻ Refresh page" button next to "Open in a new tab" (the browser's own reload button refreshes the whole dashboard, not the embedded iframe). Template homepages also got a subtle ↻ button in the sticky header for standalone viewing.

## 2026-10-16 (Global rename: info-panel rename writes through to the registry)

### Added
- **Global rename** (Dave 2026-10-16 — "when i rename a buddy using the info panel, that name should immediately propagate throughout the system"): the info-panel name field now edits the buddy's REGISTRY `name`, not a per-device nickname. The new name applies instantly in memory (sidebar, panel, all Atlas lenses via the existing `refreshBuddyLabels`) and writes through to `buddies.json` via the GitHub token route (`writeGlobalName`, same pattern as persona/voice). Without a token the rename is queued in `S.pendingRenames`, applied to the local registry at boot, and flushed on the next sync (`flushPendingRenames`, called at boot next to `flushPendingDumps`). A global rename clears any per-device `S.names` nickname override for that buddy; the journal revert path restores the registry name and writes it back. Buddy homepages now re-read the registry on every load (`NAMESYNC_JS` in the template: `[data-buddy-name]` elements + dump-box placeholder patched from `../buddies.json`, baked-in names as the offline fallback) — a rename shows on the homepage after a refresh, no rebuild needed. 54 template pages regenerated; dashboard rebuilt; all inline scripts node-checked; name-sync verified with a stubbed DOM/fetch test.

### Fixed
- The old rename only set a per-device `S.names` nickname, so renames never left the device and never reached homepages.

## 2026-10-16 (Documentarian custom homepage)

### Added
- **📚 Documentarian custom homepage** (thread-owned, `documentarian-buddy/index.html`, CUSTOM HOMEPAGE marker so the generator never overwrites it): archival ink-and-parchment design — "the buddy system's memory of itself" hero, live collection stats (buddies/homepages from `../buddies.json`, artifacts/public from the index data file), six "what I keep" tiles (buddies, pages, docs, repos, link graph, history), the visibility-watch section (standing rule: pages stay private unless Dave explicitly makes one public), "ask me" Q&A, sources tiles (mission doc, repo, dashboard), theme toggle (dark default + light + OS-auto, persisted), slim sticky header, responsive, standard 🧠 brain-dump box with the no-token/no-repo localStorage queue fallback. Inline scripts node-checked.

## 2026-10-16 (Health Buddy custom homepage)

### Added
- **🏥 Health Buddy custom homepage** (Dave 2026-10-16 — "include all my data from my health trackers, blood work, visits to doctors, all that stuff"): thread-owned custom page at `health-buddy/` (CUSTOM HOMEPAGE marker, never overwritten by the generator). Real data only, snapshot as of Oct 16: 5 stat tiles (last night's sleep, 7-day step average, resting HR, HRV, weight); sleep section with 14-night bar chart (avg ~4.1 h, 1:30–3:30 AM bedtimes); activity section with 26-day steps chart + 11 recent workouts (7 cycling, 4 walking); vitals with resting-HR and HRV sparklines (14 days); body section (3 weight readings, ~76.1 kg); doctor visits (Dr. Travis Lyman eye exam Oct 14 with full findings, two Sutter portal visits Jul 2026); blood-work section honestly marked "not yet connected" (no lab values found in Gmail/Drive/workspace/memory — Sutter emails are portal notifications only); medications section as planned stub (Dave's Oct 9 manual-entry idea); the plan (sleep first, routine, morning nudge). Sticky header, dark + light, responsive, brain-dump box with the no-repo local fallback. Inline scripts node-checked.

## 2026-10-16 (Brain-dump box works with no repo linked)

### Fixed
- **🧠 Brain-dump local fallback widened** (Dave 2026-10-16 — the box on Andy (Ire Tide)'s page was fully disabled with "No repo linked for this buddy yet", so nothing could be entered): the homepage dump box now always accepts input. With no repo linked and/or no GitHub token, dumps save to the device's localStorage and the status says so plainly ("No repo linked yet — dumps save on this device and will sync when one is linked"); the backlog flushes into `docs/ingest.md` on the next successful GitHub dump once a repo is linked and a token is present. Regenerated all 56 template-driven homepages (`gen_basic_homepages.py`); inline scripts node-checked. Custom homepages with their own dump-box copy (cabin-buddy, reminder-buddy, housing-buddy) still need the same fix in their owning threads.
- **Housing Buddy custom homepage adopts the local fallback** (owning thread, `housing-buddy/index.html`): the page's own dump-box copy now always accepts input — no repo linked and/or no GitHub token → entries save to the device's localStorage with a plain-English status, and the backlog flushes into `docs/ingest.md` on the next successful GitHub dump. The old gating logic (disabled textarea/button, "No repo linked for this buddy yet") is gone; the orphaned "Connect GitHub" markup stays hidden with its JS unwired, matching the cabin-buddy adoption. Token flow, GitHub flush, and backlog sync unchanged. Inline scripts node-checked.
- **Fleet sweep: 45 more custom homepages adopt the local fallback** (Dave 2026-10-16 — Wisdom Buddy's box was still fully disabled with no repo linked): every remaining buddy page carrying the old gating logic now always accepts dump input, saves to device localStorage with no repo/token, and flushes the backlog on the next successful GitHub dump. Same adaptation as cabin-buddy/housing-buddy (page-specific button selectors kept; orphaned connect-button JS removed, hidden markup left in place). All inline scripts node-checked. Not changed: investment-buddy (bespoke local-only dump, never syncs — needs Dave's product call) and james-buddy (bespoke dump hardcodes its repo and requires a token — owning thread should adopt the standard box). Note: the 56 template pages supposedly regenerated in 2dac35e still carried the old gating in this checkout — the regeneration didn't stick here; the sweep covered them by file.

## 2026-10-16 (Legal Buddy custom homepage)

### Added
- **⚖️ Legal Buddy custom homepage** (thread-owned, `legal-buddy/index.html`): "the counselor's chambers" — Heineman quote hero, how-counsel-works 4 steps, 7-tile triage remit, the 10-trait composite model with exemplars (Lipton, Sonsini, Olson, Boies, Flom, Beattie, Cohen, Giuffra, Saeed, Davidson, Lincoln), guardrails, honest limits (not a licensed attorney, no privilege), Open-now attention card (mission review + inbound transcription), documents & links, standard 🧠 brain-dump box (GitHub write path to `legal-buddy/docs/ingest.md`), slim sticky header, dark + light (auto/OS/light/dark toggle, persisted), phone/tablet/desktop layouts. Carries the CUSTOM HOMEPAGE marker so `gen_basic_homepages.py` never overwrites it.

All notable changes to the Buddies dashboard and buddy system. Newest first.
`FEATURES.md` describes the current state; this file describes how it got there.

## 2026-10-16 (Plumber Buddy joins the dashboard)

### Added
- **Plumber Buddy registry entry** (Dave 2026-10-16 — active pressure-tank leak at the cabin; asked for an on-call master plumber fluent in well systems): `plumber-buddy` added as a top-level staff function (status New), with tagline, mission, repo/docs links, the mission-statement review attention item, and a custom v1 homepage at `plumber-buddy/` (what it knows: cabin well system + Lenwood city water; problems it solves; vendor rolodex with Mike McGee / R&M Drilling; open questions). Dashboard rebuilt; embedded registry verified with the entry present; inline scripts node-checked.

## 2026-10-16 (Documentarian joins the dashboard)

### Added
- **Documentarian registry entry** (Dave 2026-10-16 — approved "Spin up the Documentarian" for the curator/historian role): `documentarian-buddy` added as a top-level staff function (status New), with tagline, mission, repo/docs links, the mission-statement review attention item, and the default "Dossier" homepage generated at `documentarian-buddy/`. Dashboard rebuilt; embedded registry verified at 110 buddies with the entry present.

## 2026-10-16 (Legal Buddy joins the dashboard)

### Added
- **Legal Buddy registry entry** (Dave 2026-10-16 — brief approved, "This is AWESOME!", spin-up authorized): `legal-buddy` added as a top-level staff function (status New), with tagline, mission, repo/docs links, the mission-statement review attention item, and the default "Dossier" homepage generated at `legal-buddy/`. Dashboard rebuilt; embedded registry verified with the entry present.

## 2026-10-16 (Model A Buddy joins the dashboard)

### Added
- **Model A Buddy registry entry** (Dave 2026-10-16 — it was missing from the dashboard; he expected it under Car Buddy): `model-a-buddy` added as a child of `car-buddy` (status New), with tagline, mission, repo/docs links, the spec-sheet review attention item, and the default "Dossier" homepage generated at `model-a-buddy/`. Dashboard rebuilt; embedded registry verified at 108 buddies with the entry present.

## 2026-10-15 (Breadcrumb links, dump fallback, generator skip-logic fix)

### Fixed
- **Breadcrumb ancestor links now navigate** (Dave 2026-10-15 — clicking Astro / Project Buddy / Work Buddy / Shreya Dhingra did nothing): the `.bp-crumb` `data-goto` links live inside `#view-buddy`, which itself carries `data-buddy` — the document click handler checked `data-buddy` first, so every crumb click just re-opened the current buddy. The `data-goto` check now runs before `data-buddy`.
- **Brain-dump box saves locally with no GitHub token** (Dave 2026-10-15 — dumping failed when no token was present): temporary workaround until the GitHub write path works properly. No token → the timestamped entry is appended to `localStorage` (`buddyTree.ingest.<bid>`); the box stays usable and says so. The backlog flushes into the repo's `docs/ingest.md` on the next successful GitHub dump (one PUT, then the backlog clears). Rolled out to all 54 template homepages via `gen_basic_homepages.py` plus Shreya Dhingra's custom page. Custom pages owned by other threads (Work, Astro, Lenwood, Tech, Hot Tub, Travel, Feedback, Career, Cabin, Relationship buddies) keep their own copies — their threads can adopt the snippet.
- **Generator skip-logic fix** (found during the rollout): `is_template_page()` treated any page containing "Part of the Buddy System" as template-generated, which misclassified Finance Buddy's custom homepage (it kept a similar footer) and the regen overwrote it — restored from git. The `<!-- CUSTOM HOMEPAGE -->` marker now always wins; custom designs are never overwritten.

## 2026-10-15 (Tree-view zoom control: geared down + moved to upper-right)

### Changed
- **Tree-view zoom geared down + relocated** (Dave 2026-10-15): the physical zoom control was too sensitive — slider step halved from 2 to 1 percentage point and Shift+scroll wheel step halved from ±2 to ±1 (keyboard +/- stays at ±5 per deliberate press). The `.zoombar` (slider + fit + center-on-buddy) moved from vertically-centered on the pane's right edge to the **upper-right corner** of each tree pane (`top:12px`, vertical-centering transform removed); the info-panel-open leftward shift and mobile `right:4px` behavior are unchanged.

## 2026-10-15 (Shreya Dhingra custom homepage)

### Added
- **💼 Shreya Dhingra custom homepage** (thread-owned, `shreya-dhingra/index.html`): "the briefing desk" — the living collaboration record for Dave's Apple manager. Full-bleed priority stack (partner config #1, partner info #2, misc item #3 — needs definition, ~1–2 weeks of design work, Jira as source of truth), coverage card (Shreya + Connie on vacation ~2 weeks from Oct 16, Sparsh is point person), what she cares about (real priorities, no surprises, never IS&T's roadblock), review rhythm (Mon/Thu 9am; EOD-Friday status cadence unconfirmed), "Owed to Shreya" open items, team chips (Shreya, Dave, Connie Ko, Sparsh, Stephen), docs & links (dossier, mission statement, repo, Work Buddy, Connie Ko, dashboard), attention banner for the dossier review, standard 🧠 brain-dump box (same GitHub write path to `shreya-dhingra/docs/ingest.md`), slim sticky header, dark + light via prefers-color-scheme, phone/tablet/desktop layouts. Carries the CUSTOM HOMEPAGE marker so `gen_basic_homepages.py` never overwrites it.

## 2026-10-15 (Shreya Dhingra buddy)

### Added
- **💼 Shreya Dhingra buddy** (Dave 2026-10-15): person buddy for Dave's Apple manager (STIX team lead — Dave, Connie Ko, Sparsh; her manager is Stephen). Child of Work Buddy. Merged the two duplicate dashboard FAB requests ("Shreya" game-show-host + "Shreya Dhingra" mad-scientist) into one sensible buddy per Dave's standing rule — generic professional persona, sensible icon, no blocking on choices. Dossier captures the Oct 15 priority reset: partner config + partner info as top items (~1-2 weeks), Jira as source of truth (Connie created the epic), Sparsh covers while Shreya and Connie are on vacation ~2 weeks from Oct 16. Private repo, Buddy Docs dossier, dashboard entry; side thread + review ask still to be posted.

## 2026-10-15 (Larry Osana custom homepage)

### Added
- **🔑 Larry Osana custom homepage** (thread-owned, `larry-osana/index.html`): the tenant record — contact card (unknowns marked unknown, never invented), ⚠️ priority banner for the new contract naming the estate as landlord, 🕰️ lease-status timeline (Emil → Jul 1 2026 → landlord gap → new contract) as the charts-directive alternative visual, property context (Melody Lane, address unverified), empty communication log, standard 🧠 brain-dump box (same GitHub write path to `larry-osana/docs/ingest.md`), slim sticky header, dark + light, all viewports. Links: dossier, repo, thread, Melody Lane, Emil's Estate. Footer deliberately omits the "Part of the Buddy System" signature so `gen_basic_homepages.py` never overwrites it (thread-owned custom design).

## 2026-10-15 (Emil's estate buddies)

### Added
- **Four new buddies for Emil Dell'Aquila's estate** (Dave approved 2026-10-15 — "create the necessary buddy objects to manage this"): 🏛️ **Emil's Estate** (`emil-estate`, child of Family Buddy, linked to Emil Buddy + Finance Buddy) — asset inventory, realtor document flow, title transfers, inheritance timing; 🏷️ **Emil's House Sale** (`emil-house-sale`, child of Emil's Estate) — the active-sale deal desk, listing → offers → closing; 🏠 **Melody Lane** (`melody-lane`, child of Emil's Estate) — the rental property Field Guide; 🔑 **Larry Osana** (`larry-osana`, child of Melody Lane) — person buddy for the tenant; urgent item: new lease contract naming the estate as landlord. All four have private repos, Buddy Docs briefs, side threads, and review asks. Realtor name/email, house address, Melody Lane lease terms all open questions — never invented.

## 2026-10-15 (Buddy homepage children nav)

### Added
- **Children listed alongside parent on all buddy homepages** (Dave 2026-10-15): every buddy homepage now shows a "Children:" row directly below the parent breadcrumb at the top of the page, with icon + name links to each child's homepage (same-tab web navigation). Children are computed with the multi-parent model (`parents[]` + legacy `parent`), so a child with multiple parents lists under each parent (verified: Penny appears under both Acquaintances and Testers). Both homepage generators (`gen_basic_homepages.py` TEMPLATE via `{family_nav}`, `gen_default_homepages.py` v3 via `{family_nav}`) now emit the nav, so future regenerations keep it. Also restored the parent breadcrumb on template pages (it had been wiped by the sticky-header regeneration) and made it multi-parent aware (Penny shows "← Acquaintances · ← Testers"). Siblings intentionally omitted per Dave ("i don't know about siblings though").

## 2026-10-15 (Sticky buddy page header)

### Changed
- **Sticky page header on all buddy web pages** (Dave 2026-10-15): every buddy homepage now pins a slim sticky header — icon left of the page name — with content scrolling underneath, so it's always clear which page is being viewed. Implemented in `gen_basic_homepages.py` TEMPLATE (all 53 template pages regenerated) and on Finance Buddy's custom page. This is the default for all pages going forward; custom thread-owned designs keep their own unless their threads adopt it. Also added the missing `homepage: tester-buddy/` registry field (page existed, registry link didn't).

## 2026-10-15 (Brain dump queues locally on failure)

### Fixed
- **Homepage 🧠 Brain dump no longer loses text on save failure** (Dave 2026-10-15): `homepageDumpSubmit` previously showed "Save failed: <reason>" and left the text sitting in the textarea — one navigation away and it was gone. It now follows the standing `token_gated_client_writes` rule: any failure (no token, GitHub 404, network error) queues the entry (text + timestamp + buddy id) in the shared `pendingDumps` localStorage queue, clears the textarea, and shows "Queued on this device — will sync when GitHub is connected (N queued)" with a token-settings link. The brain-dump textarea is now always rendered when a repo is linked (previously hidden behind a locked box with no token — Dave's Safari had no token); the locked notice remains but invites queuing. Queued items render in the dump feed with a "pending sync" badge, auto-flush when a successful dump lands or when a token is saved, and the feed refreshes after flushing.

## 2026-10-15 (Dashboard fixes batch)

### Fixed
- **Info-panel section toggles no longer silently re-render** (Dave 2026-10-15): root-caused the stubborn "PARENTS section won't expand" bug. Two document-level click listeners are registered on `document`; the panel toggle handler called `e.stopPropagation()`, which does NOT block other listeners on the same target. The later handler's `[data-buddy]` branch matched `#view-buddy` (which carries `data-buddy`) and called `openBuddy()` → `renderBuddy()` rebuilt the panel, wiping the just-toggled `expanded` class and resetting scroll to top. Fix: `stopImmediatePropagation()` in the panel toggle's terminal branches (`[data-expand]`, `.attr-head`, `[data-addparent]`, `[data-removeparent]`), plus `stopPropagation()` on the h3 section-toggle handler (which had none at all — every section click was re-rendering the panel, masked for h3 sections because their state persists in `S.secCollapsed`).
- **Sidebar search filter retained across refresh** (Dave 2026-10-15): the `#buddy-search` filter value is now persisted in `S.buddySearch` on every input and restored on boot (re-applied via a synthetic `input` event). Buddy selection and panel-open state were already persisted via `S.sel`.
- **Collapsed sidebar rail starts cleanly** (Dave 2026-10-15): the empty `.sb-brand-sticky` bar (white rounded bar with no content when collapsed) is now `display:none` under `body.sb-closed`, so the rail starts directly with the › expand button.

### Changed
- **Zoom gearing smoothed out** (Dave 2026-10-15, "smooth out the zoom factor"): Shift+wheel zoom step ±5% → ±2%; slider `step` 5 → 2 (both main and orph); pinch-zoom rounding `/5)*5` → `/2)*2`; zoom-to-fit rounding `/5)*5` → `/2)*2`. Min/max clamps unchanged (wheel 25–160, slider 5–160).

### Verified (no change needed)
- **Atlas lens menu vs info panel** (Dave 2026-10-15): the lens picker and orientation tabs sit top-left; the info panel slides in from the right — spatially separated on desktop. Lens dropdown (z-61) renders above the panel (z-60). On phone the panel is a full-screen sheet (correct modal behavior); the lens menu is reachable when the sheet is closed.
- **Panel-section 404s**: the console 404s are expected missing optional resources (`avatars/<id>.jpg` fallback via `buddyImageUrl`, GitHub API photo/note fetches) — each self-cleans via `onerror` handlers. Unrelated to the expand bug.

## 2026-10-15 (Defensibility ledger drill-down pages)

### Added
- **Click a ledger bubble → detail page** (Dave 2026-10-15): all eight defensibility-ledger bubbles on the Guardian homepage are now links to `guardian-buddy/ledger/<slug>/` detail pages. Each page explains what the bubble represents, why it sits at its chart position (ease-of-copying × business value), current risk/defensibility, and Guardian's recommendation/next action — with position tags, a back link to the ledger, dark/light theme (shared `guardian-buddy-theme` key), and phone layouts. Added `id="ledger"` anchor to the chart heading; bubble hover/focus states for linked circles.

## 2026-10-15 (Persona roster expansion: F1, presidents, historical figures)

### Added
- **119 new personas — roster now 238** (Dave 2026-10-15, "no upper limit"): 26 Formula 1 personalities (#120–145: Vettel, Alonso, Räikkönen, Briatore + Hamilton, Verstappen, Schumacher, Senna, Prost, Lauda, Mansell, Button, Rosberg, Ricciardo, Norris, Leclerc, Piastri, Russell, Wolff, Horner, Steiner, Ecclestone, Brawn, Newey, Brundle, Murray Walker), 44 ex-presidents Washington→Biden (#146–189, sitting president excluded), 49 historical figures (#190–238: Einstein, Newton, Darwin, Curie, da Vinci, Shakespeare, Mozart, Beethoven, Napoleon, Churchill, Gandhi, MLK, Mandela, Cleopatra, Joan of Arc, Caesar, Alexander, Elizabeth I, Victoria, Tubman, Douglass, Earhart, Austen, Twain, Wilde, Kahlo, Picasso, van Gogh, Chanel, Jobs, Turing, Lovelace, Hawking + more). Each with a voice-sample quote and personality blurb; baked into the dashboard's persona picker.

## 2026-10-15 (Relationship reorganization)

### Changed
- **Friends moved from Relationship Buddy to Acquaintances** (Dave 2026-10-15): Relationship Buddy was meant for healthy/romantic relationships, but everyone under it was friends/acquaintances. Joel Nelson, James Michael Day, Carl Towne, and Eric are now children of Acquaintances. Jody Reed was already under Acquaintances. Penny remains under Acquaintances + Testers (multi-parent). Testers stays under Relationship Buddy (system/testing category, not a person). Relationship Buddy is kept in place (now nearly empty) for its original romantic/healthy-relationship purpose later.
- **"friend" added as an AKA for the Acquaintances buddy** (Dave 2026-10-15): searching "friend" in the dashboard sidebar now matches Acquaintances (sidebar search includes `effAka`). Rendered as "aka friend" next to the name and in the A.K.A. info-panel section.

## 2026-10-15 (Zoom controls stay visible with panel open)

### Fixed
- **Zoom controls shift left when info panel opens** (Dave 2026-10-15): the main-view zoombar (slider, fit, ⌖ center buttons) was obscured behind the sliding info panel. Now `body:has(#view-buddy.panel.active)` shifts `#zoombar-main` and `#zoombar-orph` left by the panel width (`--bpw`), with a smooth transition matching the panel's slide timing. Skipped when panel is collapsed to rail, and on mobile where the panel is a full-screen sheet.

## 2026-10-15 (Browser back/forward navigation history)

### Added
- **Browser back/forward walks the buddy viewing history** (Dave 2026-10-15): every buddy selection, view switch, panel open, and Atlas lens change now pushes a real `history.pushState` entry carrying `{sel, projectId, view, chartType, panel}` — enough to fully restore the view. The browser's own back/forward buttons walk backwards/forwards through everything Dave viewed, Raycast-style. A `popstate` listener restores the selection, view, Atlas lens, and detail-panel open/closed; entries without a state object (old bookmarks, direct hash edits) fall back to the existing hash parsing. Consecutive duplicate states are never pushed. The in-app ← Back button now delegates to `history.back()`.
- **Initial state seeding**: `initRoute` seeds `history.state` via `replaceState` so the first back traversal already has a state object (no extra history entry).

## 2026-10-15 (Jody Reed buddy)

### Added
- **Jody Reed buddy** (Dave 2026-10-15): new person buddy — proprietor of Ham's Station (restaurant off Highway 88) and a realtor. Child of Acquaintances. Dossier, private repo, dashboard entry (#102), homepage. Spelling TBD: "Jody" (Dave) vs "Jodie" (dashboard request). Persona: warm/professional (the request's "Italian nonna" suggestion deliberately not used — real business contact). Two-role contact — the concrete case for the roles-as-buddies pattern.

## 2026-10-15 (Atlas center-on-buddy)

### Added
- **Center-on-current-buddy for Atlas lenses** (Dave 2026-10-15): switching to the org chart (or any Atlas lens) from a buddy now auto-centers the chart on that buddy instead of restoring the old scroll position. Dave: "i would expect that the buddy would be centered on the org chart."
- **⌖ center button on the zoom bar** (Dave 2026-10-15): a crosshair button under the zoom-fit control re-centers the Atlas pane on the current buddy at any time (explicit selection first, then the project/homepage buddy). Smooth animated scroll; toasts when no buddy is selected or the buddy isn't visible in the current lens.
- **Cross-lens centering**: the upgraded `centerOnBuddy()` finds the buddy's node via `[data-buddy]` in every DOM-based lens (org, lineage, ledger, colonnade, terrain, halo) and via the live canvas node map in constellation. Search-as-you-type centering stays instant to avoid scroll queuing.

## 2026-10-15 (Multiple parents per buddy)

### Added
- **Multiple parents per buddy** (Dave 2026-10-15 ❤️): a buddy can now have `parents: ["id1", "id2"]` in buddies.json (legacy single `parent: "id"` still works). New `effParents()` returns all effective parents; `effParent()` now resolves to the first. The sidebar tree and org chart list the buddy under EACH parent (Penny Luedtke now appears under both Acquaintances and Testers). Info panel PARENT section became PARENTS with a count badge, a clickable link row per parent, a × remove button per parent, and a "+ Add parent" button; the old Change/Clear buttons are gone. The parent picker gained an "Add parent" mode (hides the "No parent (top level)" option and excludes existing parents). Peers section now shows the union of siblings across all parents, deduped. Per-device overrides (`S.parents`) accept an array, a single id, or null; move/undo/detach preserve the full parent list.
- **Cycle guards** (Dave 2026-10-15): the sidebar tree walk carries a per-branch ancestor set so a true cycle can't loop it (a buddy under two parents is a diamond, not a cycle, and renders twice). `isDesc()` now walks every parent chain so drag-moves can't create a loop through a non-first parent, and `descUnseen()` is visited-set safe.

## 2026-10-15 (Buddy homepage parent links + root photo wall)

### Added
- **Parent breadcrumb on every buddy homepage** (Dave 2026-10-15): all 99 non-root buddy homepages now show a "← Parent Buddy Name" link at the top, linking to the parent's homepage. Top-level buddies (no parent) link to Astro, the root buddy. Dave: "all the web pages will need to be updated to include a link to its parent."
- **Buddy photo wall on Astro's page** (Dave 2026-10-15): Astro's homepage (the root buddy) now has a "🧑‍🤝‍🧑 The crew — who's here" grid showing all 100 buddies. Real photos where available (Astro's avatar, Penny's selfie); emoji icons as placeholders for the rest. Each tile links to that buddy's homepage.


## 2026-10-15 (New-buddy sheet name pre-fill)

### Fixed
- **Name pre-filled from search** (Dave 2026-10-15): opening the New Buddy sheet while the sidebar search has text now pre-fills the name field with that query (trimmed). Works from the FAB, the `n` shortcut, and the autocomplete "Create new buddy" row (which passed the name but the sheet never applied it). Dave: "i clicked 'create new buddy' and the new buddy sheet is asking for a name. i would expect the name to be already filled in with what i searched for."
- **Stray `prefillName` crash in Settings** (found while fixing the above): a leftover line in `openFieldSettings` referenced an undeclared `prefillName` variable, which would have thrown a ReferenceError and killed the settings sheet render. Removed.

## 2026-10-15 (Info panel count badges)

### Added
- **Section count badges** (Dave 2026-10-15): every list-style eyebrow section header in the buddy info panel now shows a subtle count badge — Artifacts, Photos, Business plans, Linked buddies, Children (now always shown, was hidden at 0). Uses the existing `.attn-count` style (small, muted). Dave: "it would be nice to know without having to expand it that there is at least one in there."

### Fixed
- **Section expand scroll jump** (Dave 2026-10-15): expanding/collapsing a section no longer shifts content above the click point. The header's viewport position is preserved via requestAnimationFrame scroll correction, plus `overflow-anchor:none` on the panel to disable browser scroll-anchoring interference.
- **PERSONA (and all attr-head sections) clickable** (Dave 2026-10-15): clicking anywhere on the PERSONA/VOICE/ABOUT/etc. header row now expands/collapses the section — previously only the tiny › toggle button worked, so clicking the header text did nothing. The Change button and other controls still handle their own clicks.
- **Persona picker grouped** (Dave 2026-10-15): the picker now shows "Defaults" group first (Default male, Default female, Default child) followed by "All personas" (the full roster). Filter placeholder updated.

## 2026-10-15 (Penny Luedtke homepage)

### Added
- **Penny's photo** (Dave 2026-10-15): Penny sent her selfie ("I don't even let family members take pics of me. I hate being in photos. But there it is.") — now on her homepage header as a circular avatar, plus two new correspondence entries (photo email, Wispr Flow reply).
- **Beethoven mentioned** (Dave 2026-10-15): Penny's other pet, alongside Mozart. Dossier "Cat" row became "Pets"; dossier doc "Mozart" section became "Pets". Beethoven will become a child buddy of Penny's buddy in her own Buddy System later, same as Mozart.

### Fixed
- **Buddy cross-links** (Dave 2026-10-15): "child of Relationship Buddy" (header pill + footer) is now a clickable link to Relationship Buddy's homepage, per Dave's standing rule that every buddy name gets its homepage link. Mozart/Beethoven buddies don't exist yet — no links until they're created.

## 2026-10-15 (Eric buddy)

### Added
- **Eric** (Dave 2026-10-15): person buddy for Eric, met at Gibson's Roadhouse on reggae night (Oct 14, 2026). 🎸 icon, child of Relationship Buddy. Living dossier (only a first name known so far; open questions: last name, what he does, contact info, photo). Dossier: https://docs.google.com/document/d/19FtdrF4c6PhyjeHhHxrS7RTpnqvIVuJS1Va7QoEJ6To/edit — Repo: davedellaquila/eric (private) with standard files (SOUL, KNOWLEDGE, DECISIONS, ACCOMPLISHMENTS, dossier mirror, ingest). Custom homepage (reggae-night warmth, dark+light, brain-dump box) at eric/.

## 2026-10-15 (Default View styles)

### Added
- **Default View style picker** (Dave 2026-10-15): the auto-generated buddy homepage ("show everything") now renders in four selectable styles — **Bento** (the feature quilt, default), **Ledger** (the morning paper), **Console** (mission control, dark-first), **Pulse** (right now, time-ordered spine). Picker mirrors the Atlas lens picker: a quiet pill (sticky, top-right of the Default View) opens a flyout with wireframe thumbnail previews; choice persists per device. Hierarchy-aware: Astro shows system rollups, parents show children summaries, leaves show their own data. Pulse ✓ buttons mark attention items done with the standard 6s undo. Brain-dump box carries over in every style.
- **Astro homepage stat tiles are clickable** (Dave 2026-10-15, first pass): Buddies Tracked → dashboard tree, Need Dave's Reply → awaiting-reply section, Briefs/PRDs in Review → attention feed, Live & Piloting → dashboard Projects view. Tiles get pointer cursor, press animation, keyboard support (Enter/Space), and tooltips.

### Changed
- **Tip jar spacing tightened** (Dave 2026-10-15): bottom padding 10px → 2px so the tip jar sits flush with the sidebar footer edge; whitespace now lives above the divider line.

## 2026-10-15 (Marketing Buddy)

### Added
- **Marketing Buddy** (Dave 2026-10-15): Dave's marketing department — owns all Buddy System messaging (taglines, testimonials, social rollout, positioning, launch copy). Don Draper persona: confident, poetic, slightly world-weary; sells the feeling, not the product. 🥃 icon, child of Project Buddy. Mission statement, private repo (davedellaquila/marketing-buddy) with SOUL.md capturing the Draper voice, KNOWLEDGE.md seeded with the messaging canon, taglines.md + testimonials.md moved in from ~/workspace/user/marketing/. Dashboard homepage with dark mode, mid-century styling, pull-quote, canon section, brain-dump box.

## 2026-10-15 (Penny Luedtke buddy)

### Added
- **Penny Luedtke buddy** (Dave 2026-10-15): first Buddy System tester (ex-Rae Assist user). Dossier, private repo (davedellaquila/penny-luedtke), dashboard entry (child of Relationship Buddy, 🌟 icon), homepage with dark mode. Pilot of the **Correspondence section** — every person buddy homepage now auto-lists all emails with that person (Dave ↔ pennyagent@gmail.com: 7 emails tracked Oct 15).
- **Correspondence section** (new standard person-buddy feature): a 💌 section on every person buddy homepage listing all emails with that person, newest first, with direction badges (Dave → / → Dave), dates, subjects, and snippets. Penny is the pilot; rolls out to every person buddy.

## 2026-10-15 (News Buddy voices)

### Added
- **Newsreader personas** (Dave 2026-10-15): each voice in the "Choose your newsreader" picker now has a 1–2 sentence persona description on the right side of its row (dialog widened 480→560px to fit). Tapping ▶ previews the voice's signature sample line instead of the generic intro. Hand-written personas for Cellos, Yuna, Lana, Satu, Mónica; other voices get a generated description from their language.

## 2026-10-14 (Collapsed panels + tile rows)

### Changed
- **Mini rail: top control expands, icons switch views only** (Dave 2026-10-14): the rail-top chevron flips — ‹ collapses when open, › expands when collapsed (label follows). Tapping a view icon now only switches the main view; it no longer pops the sidebar open. Rail controls got round fills.
- **Mini rail fixes** (Dave 2026-10-14): chevron now sits in the layout flow so it can't overlap the first icon; selected view shows a round (circular) indicator instead of a rounded rectangle.
- **Mini rail: expand chevron joins the icon stack** (Dave 2026-10-14): the › expand control is now the first icon in the rail itself, styled exactly like the other icons — no separate box, nothing distracting.
- **Projects view: drag to rearrange + reassign parents** (Dave 2026-10-14): each row has a grip handle — drag onto a row's middle to nest under it, or to its top/bottom edge to insert before/after (taking that row's parent). Cycle-safe, touch-friendly, order persists per device and now applies across all views.

### Changed
- **Business-plan cards: click anywhere to open** (Dave 2026-10-14): the whole card opens the plan (its first doc, new tab); the plan name is now a link too. Clicks on inner links (📄 docs) follow those links instead — the card handler yields to any `<a>`.

### Changed
- **One content width on every content page** (Dave 2026-10-14): Plans, Manifest, and Changelog now use the Projects pattern — 860px outer with 16px gutters. They were running 32px wider with full-bleed headings; now all page boundaries line up.

### Changed
- **Top tile row: four equal tiles distributed across the full content width** (Dave 2026-10-14): edges align with the content area; equal widths on phones too.
- **Status tile row at ~70% size** (Dave 2026-10-14): 105px tiles (100px phones), scaled-down type, still horizontal scroll + click-rank order.
- **Collapsed sidebar: reopen button removed** (Dave 2026-10-14): the › button no longer shows next to the collapsed icon rail — tapping any rail icon expands the sidebar.
- **Info-panel expand button is now an ⓘ info icon** (Dave 2026-10-14): replaced the left chevron on #panel-open.
- **Round fills on collapsed-panel controls** (Dave 2026-10-14): #panel-open, #bp-rail buttons, and the paired .bp-close-x are now circular.

## 2026-10-14 (Stat tiles — Dave's call)

### Changed
- **Status-tile row: equal-width tiles, horizontal scroll, click-rank order** (Dave's decision 2026-10-14, overriding Jonny's auto-width verdict): second-row tiles are now a uniform 150px (118px on phones), scroll horizontally, and stay ordered by Dave's click rank — 5th most selected on down, since the locked top row holds the four most selected. Labels get ellipsis containment as a safety net.

## 2026-10-14 (Homepage iframe theme background)

### Fixed
- **White flash between buddy homepages** (Dave's report 2026-10-14): arrow-key navigating the buddy list flashed white between page loads — the homepage iframe had a hardcoded `background:#fff`. Now follows the theme (`var(--bg)`): dark `#0d1117` in dark mode, white in light mode.

## 2026-10-14 (Acquaintances + 8 new people buddies)

### Added
- **Acquaintances buddy** (👋, new top-level shelf, Dave's request 2026-10-14): "acquaintances different from friends different from family" — the landing spot for people Dave has met and wants to remember but isn't close to yet. New faces land here first; the ones that matter graduate to Friends.
- **8 new people buddies, all parented under Acquaintances** (Dave's approval 2026-10-14 — everyone he met today): Johnny (🖥️, software lifer since the '70s, met at Gibson's), Trudy (👒, with Johnny at Gibson's), Keelan (🍺, beer server at Gibson's), Nina (💫, barstool philosophy at Gibson's — future, distributed future, particle vs wave), Andy of Ire Tide (🎸, reggae band member from Gustine; wedding-band candidate for Quentin & Amanda — contact on file, phone stays in memory only), Dr. Travis Lyman (👁️, optometrist at Amador Eye Care — exam summary in mission), Renee (📋, Amador Eye Care front desk), Ali (👓, frames at Amador Eye Care — November check-back attention item). Each got a template homepage (mission, attention items, brain-dump box) via gen_basic_homepages.py.

## 2026-10-14 (Briefing Buddy section detail pages)

### Added
- **Drill-down detail pages for all 8 Briefing Buddy homepage sections** (Dave's request 2026-10-14): each `sec-head` ("No. 1 Needs your attention" through "No. 8 Brain dump") is now a link to a dedicated detail page (attention.html, editions.html, live-data.html, designer.html, library.html, topics.html, on-my-mind.html, brain-dump.html) with deeper content about that section — full section catalogs, data-source tables, how-it-works explainers, and the open product questions. Same newsroom aesthetic, dark+light theme toggle, back links to the homepage. Hovering a section header reveals a › affordance.

## 2026-10-14 (Connie Ko onboarding)

### Added
- **Connie Ko buddy onboarded** (Dave's approval 2026-10-14): full new-buddy package — mission statement doc in Buddy Docs, private GitHub repo (davedellaquila/connie-ko), custom homepage with dark mode at /connie-ko/, brain-dump box, attention item for the Thu 10/15 10:30am internal review. Status flipped from new/setup-pending to active.

## 2026-10-14 (Buddy icons for Save to Desktop)

### Added
- **Buddy icons on saved pages** (Dave's ask 2026-10-14): buddy homepages now include `apple-touch-icon` (using the buddy's emoji/custom icon), so saving a buddy's page to desktop/home screen from Safari uses that buddy's icon instead of a generic one. The dashboard already swaps its icon dynamically when you select a buddy.

## 2026-10-13 (Sidebar resize fix)

### Fixed
- **Sidebar drag no longer jumps** (Dave's catch 2026-10-13): the sidebar used `content-box`, so the drag handler measured the border-box but set the content-box — growing the panel 28px per drag and leaving the gripper misaligned. Switched to `border-box`; gripper now tracks the panel edge.

## 2026-10-13 (Stat tiles: natural width)

### Changed
- **Stat tiles use natural width** (Jonny's verdict, 2026-10-13): killed the fixed 152px/112px tile widths — tiles are now as wide as their words (`width:auto`, `flex:none`, nowrap labels), so labels never clip mid-word. The row scrolls horizontally instead of squeezing.

## 2026-10-13 (News Buddy: read-aloud on section + article pages)

### Added
- **🔊 Listen buttons on section pages** (Dave's ask 2026-10-13 — Amador County page had no read-aloud at all): every story on a section page now gets a speaker button in its headline row (reads headline + story body), plus a "Listen to this section" button after the lede that reads the whole section start to finish. Previously the read-aloud module only targeted the homepage's `article.story` cards; section pages use `div.storyitem` and were silently skipped.
- **🔊 "Listen to this article" on article detail pages** (Dave's ask 2026-10-13): a prominent button after the byline reads the full article — headline plus every section (what it's about, why it matters, about the source) — with the currently-read story highlighted.

### Changed
- **Voice picker on every play click** (Dave's ask 2026-10-13): tapping any play/speaker button now opens the voice picker panel first (saved voice pre-checked); choosing a voice starts the audio, dismissing the panel plays nothing. Previously the picker only appeared when no voice had been chosen yet. Applies to homepage, section, and article pages.
- Read-aloud remains 100% on-device (`speechSynthesis`) — no network calls, no pre-generated audio files, zero token cost.

## 2026-10-13 (Floating panels, Muse-app style)

### Changed
- **Sidebar + buddy panel now float** (Dave's ask 2026-10-13, ref: Muse app's rounded slide-out panel): both panels are rounded on all four corners (18px), lifted off the canvas with a soft shadow and a 12px margin, reading as floating over the content underneath instead of full-bleed chrome. Panels use the `--panel` surface token against the `--bg` canvas for the tonal step. Sidebar is now a fixed overlay — the main view stays full-width underneath and never shifts when the sidebar toggles (Dave: "should not move to the right as if attached to the left panel"). Sidebar resize handle and scroll-to-top button re-anchored to the new geometry; phone drawer floats too (12px insets). iPad breakpoint (640–1100px) brought into the floating design as well.
- **Header fill fix** (Dave's catch 2026-10-13): the sidebar brand block (`.brand`) still carried the old `--bg`, rendering as a dark inset slab on the lighter floating panel — now `--panel`, so the fill runs edge to edge.
- **Native `color-scheme` declared** (dark by default, light under `html.light`): browser chrome — scrollbars, form controls, overscroll — now matches the theme instead of flashing light. Should mitigate the white flash Dave saw arrowing through buddies in dark mode; confirm with him.

## 2026-10-13 (Feedback widgets: buddy pages + awaiting-reply)

### Added
- **💬 Feedback section on Pops' Buddy homepage** (Dave's ask 2026-10-13): quick-reply choices (This is AWESOME! / Needs a tweak / Let's discuss — tapping one sends immediately, mirroring chat quick replies) plus a freeform text box. Submissions write to `docs/feedback.md` in the buddy's repo via the existing GitHub token flow, for Astro to pick up.
- **Awaiting-reply item detail view** (Dave's ask 2026-10-13): items in the Astro homepage's "Awaiting Dave's reply" section are now clickable — a detail modal shows the full summary, date, thread (+ Open thread link), and a reply section with standard quick choices (Done / Yes / No / Remind me later / Need more info — per-item `choices` in the JSON override these when present) plus a freeform text box. Replies write to `astro/feedback.md` in the buddy-system repo. Keyboard accessible (Enter/Space to open, Esc to close).

## 2026-10-13 (Tree zoom measured while hidden)

### Fixed
- **Sizer read 0×0 on fresh load with a persisted low zoom** (polish, Dave's ask 2026-10-13): `refreshViews()` renders the tree before `show()` makes the view visible, and `display:none` makes `scrollWidth` read 0 — so the zoom sizer started at 0×0 and only self-corrected on the next zoom touch. Now `show('view:tree')` re-runs `updateZoomMin()` + scroll restore in a `requestAnimationFrame` once the pane is actually visible. Also fixes persisted scroll positions silently failing to restore on fresh load.

## 2026-10-13 (Pops' Buddy dossier from dellaquila.com)

### Fixed
- **Pops' Buddy identity corrected + dossier populated** (Dave's ask 2026-10-13): the registry entry still treated "Pops" as an unidentified third person; corrected to Dave Dell'Aquila per his 2026-10-09 confirmation ("Pops and Dave are the same thing. I'm Pops."). Added a full `about` from [dellaquila.com](https://dellaquila.com) and the [portfolio](https://www.dellaquila.com/portfolio): Apple WWSF (2023–present) and Marcom (2015–2022), eBay Motors (2011–2014, eBay Garage), WebEx, Phoenix HyperSpace, MightyDB, Cisco BCP, Rae Assist (1992–1995), design philosophy, UC Davis background, Sports Car Adventures, cycling/photography. The pops-buddy homepage now carries a 📋 Dossier section with the career timeline. Stale "identity unknown" attention text updated.

## 2026-10-13 (Lineage low-zoom collapse — nested scrollers)

### Fixed
- **Lineage/Colonnade collapsed to a 3px sliver at low zoom** (caught by live browser verification 2026-10-13): `.lineage{overflow-x:auto}` and `.colonnade{overflow-x:auto}` were nested scroll containers, which clip their content's overflow from ancestors — so the zoom sizer's `scrollWidth` measurement could never see the true chart width. Removed the nested scrollers (`overflow:visible`); the tree pane remains the single 2D scrollport. Documented the zoom-canvas invariant in CSS (no nested scroll containers inside chart canvases; `.qa-links`/`.mcol` carousels are the deliberate exception).

## 2026-10-13 (Tip jar links on the dashboard)

### Added
- **🫙 Tip the jar** (Dave's ask 2026-10-13): two quiet, tasteful spots linking to ko-fi.com/davedellaquila — a muted sticky footer link at the bottom of the sidebar, and a Support section in the Settings sheet. Same destination as the News Buddy voice picker's tip link.

## 2026-10-13 (Persona picker: description overflow fixed + sample previews)

### Fixed
- **Persona descriptions no longer spill past their cards** (Dave's screenshot catch 2026-10-13): the `.pp-blurb` line had no line clamp, so long descriptions rendered straight through the card border onto the tile below. Applied Jonny's approved verdict — 2-line clamp + ellipsis at 12.5px muted on the blurb, plus `overflow:hidden` (and `min-width:0`) on the card as containment.

### Added
- **▶ Sample button on every persona card** (Dave's ask 2026-10-13): tapping it reads the persona's quote (or blurb) aloud via the device speech engine — tap again to stop. Play never selects the persona; closing the picker stops playback. Same `.pp-play` affordance as the voice picker.

## 2026-10-13 (Tree zoom is pure scale — no more scrunching)

### Fixed
- **Zoom no longer scrunches tiles** (Dave's screenshot catch 2026-10-13): the tree panes zoomed with the CSS `zoom` property, which re-runs layout at the zoomed size — zooming out squeezed Lineage tiles into narrow strips instead of scaling them. Zoom is now pure `transform: scale()`: the chart is laid out once at natural size inside a `.zoomcontent` wrapper, and a `.zoomsizer` carries the scaled scroll extents. Pinch, slider, keyboard, and zoom-to-fit all use the same path; pan math is unchanged. The buddy-panel mini preview unwraps the new structure so it keeps its own behavior (no double-scaling).

## 2026-10-13 (Views list: touch-friendly drag grippers)

### Added
- **⋮⋮ drag grippers on the Views list** (Dave's ask 2026-10-13): each row in the sidebar Views list (including Home) now carries a right-side grip in the same language as the info panel's section grips. Dragging the grip uses pointer events (mouse + touch) with live reorder — the touch path the old HTML5 mouse-only DnD couldn't reach, so views are now reorderable on iPad/iPhone too. Grip taps never switch views; order persists to `S.viewOrder` per device as before.

## 2026-10-13 (Investment Buddy homepage: market dashboard)

### Added
- **📈 Investment Buddy homepage** (Dave's commission 2026-10-13): a full market-overview dashboard at `investment-buddy/index.html`, replacing the basic template (custom design, never auto-overwritten). Market-now strip (S&P 500, Nasdaq 100, Dow, 10-yr yield, VIX with green/red day pills); hero chart — S&P 500 monthly closes, 10 years (+271% annotated); the horse race — S&P 500 vs Nasdaq 100 vs Dow, past 12 months rebased to 100; the last 3 months, rebased; "The Lookout" — four quick-take cards (10-yr ≈5.2% 24-yr high, VIX ≈15 calm, CPI Oct 14, Q3 earnings week); about section + device-local brain dump; "not financial advice" footer. Hand-rolled SVG charts (no dependencies), hover tooltips, dark+light mode, responsive. All market series are real Finnhub CFD-proxy closes as of Oct 12, 2026 (269 daily / 241 monthly points embedded); every chart labeled with source + as-of. Yield/VIX history couldn't be honestly sourced — shown as current readings only.

### Fixed
- **About-section list styling** (Dave's screenshot catch 2026-10-13): the `ul`/`li` rules still targeted a dead `.about-grid` selector (leftover from a refactor — the markup uses `.grid2`), so the "About this buddy" bullets rendered unstyled and cramped. Retargeted to `.grid2 .card ul/li` with the intended 14px muted styling, indent, item spacing, and line-height.

## 2026-10-13 (Project tiles: locked top row + TOTAL tile; settings/info-panel field parity; text-size readout clipping)

### Changed
- **Top tile row is now locked** (Dave's ask 2026-10-13): the four tiles render in fixed order — TO REVIEW, FRESH, CLEARED, TOTAL — no more popularity self-sorting on the top row. The bottom (status) row keeps the click-count ordering.
- **Settings "Buddy fields" ↔ info panel parity** (Dave's catch 2026-10-13): added the missing **Voice** field to `FIELD_DEFS` (it rendered in the info panel but had no settings toggle and always pinned itself last), and renamed the settings label **"Direct reports" → "Children"** to match the info panel's CHILDREN heading.

### Added
- **TOTAL tile** (Dave's ask 2026-10-13 — the logical fourth tile): shows the full buddy count; clicking it clears all filters (it's the reset button the row was missing). It reads selected when no filter is active.

### Fixed
- **Text-size readout spill** (Dave's screenshot 2026-10-13): the "100%" number could spill outside the Settings row on narrow sheets. Per Dave's call — when the number doesn't fit, don't show it: the slider row now clips (`overflow:hidden`, container `min-width:0`) instead of overflowing, so the readout is cut off rather than spilling past the sheet edge.

## 2026-10-13 (Sidebar: drag-to-reorder items within each section)

### Added
- **Drag items within each sidebar section** (Dave's ask 2026-10-13): grab any row inside Views, Business Plans, or Buddies and drop it before/after another row — box-shadow insert hints, "Order saved." toast. Views persist via `S.viewOrder`, plans via new `S.planOrder` (`getPlanOrder()` mirrors `getViewOrder()`), buddies via new `S.buddyOrder = {parentKey: [childIds]}` (`'__root__'` for top-level). Buddy rows reorder only among siblings sharing an effective parent — never reparenting. Event delegation on each section container survives `renderNav()` re-renders; reordering is disabled while the buddy search filter is active. (Mouse/trackpad drag, matching the section headers; touch not wired yet.)

## 2026-10-13 (Stat tiles: uniform width + popularity ordering — Dave's override of Jonny)

### Changed
- **Stat tiles are now a uniform width** (Dave's call 2026-10-13, overriding Jonny's auto-width verdict): every `.ptile` is `flex:0 0 152px` on desktop and `112px` on phones, so all tiles match regardless of label length. Both tile rows keep their horizontal scroll. The redundant `#project-status-tiles .ptile` rule and the inline `flex` in `tileHtml` are gone — CSS is the single source of truth.
- **Tile rows self-order by popularity** (Dave's ask 2026-10-13): every click on a `#project-tiles` or `#project-status-tiles` tile is counted in `S.tileClicks` (persisted via `save()`), and each row re-renders most-clicked-first — the most-used filter is always leftmost. Ties keep their original order (stable sort); the order updates live after each click since the row re-renders.

## 2026-10-13 (Attention effects: wiggle, bounce, swing)

### Added
- **Three new attention header effects** (Dave's ask 2026-10-13): wiggle, bounce, and swing join pulse, glow, shake, and blink in Settings → Attention header effect. The live preview shows each one as you pick it.

## 2026-10-13 (Sidebar sections draggable)

### Added
- **Drag the sidebar sections to rearrange them** (Dave's ask 2026-10-13): grab any section header (Buddies / Business Plans / Views) and drop it above or below another — order saves on the device. (Mouse/trackpad drag; touch drag not wired yet.)

## 2026-10-13 (Settings sheet: effect preview, responsive labels, two-column lists; sidebar kind column)

### Added
- **Live "Attention header effect" preview** (Dave's ask 2026-10-13): the Advanced setting now shows a mini "Needs your attention (3)" header running the selected effect (pulse/glow/shake/blink/none) so you can see what each one does before picking it. Updates live when the selection changes.

### Changed
- **Settings sheet goes two-column when resized wide** (Dave's ask 2026-10-13): past 640px the "Main views" and "Buddy fields" sections sit side by side (views left, fields right), each list scrolling independently — via container queries, so it follows the sheet's drag-resized width.
- **Setting labels stack above their controls on narrow sheets** (Dave's ask 2026-10-13): below 440px the label takes its own line instead of getting scrunched beside the control.
- **Narrow sidebar drops the kind column** (Dave's ask 2026-10-13): below 290px the buddy list hides the right-hand type labels (ROOT/DIRECT/STANDALONE…) so buddy names get the full width.

## 2026-10-13 (Persona previews: 7 missing voice samples restored)

### Fixed
- **Regenerated the 7 missing persona voice-sample MP3s** (`personas/samples/`): auctioneer, forensic-accountant, italian-nonna, japanese-zen-master, jonny-jony-ive, ninja, tenured-professor. They were absent from the 2026-10-12 batch (TTS backend gaps, same class of failure as the empty camp-counselor.mp3), so the info-panel "Hear it" preview failed for those personas. Each sample speaks the persona's roster one-liner in a fitting voice (Jonny's is an original Jony-ism: "This is so much more than a dashboard. The edge is chamfered. The rest... is inevitable.").

## 2026-10-13 (Info panel: "Ingest" renamed to "Dump box")

### Changed
- **The info panel's ingest section is now labeled "Dump box"** (Dave's ask 2026-10-13). The underlying `ingest` field id and `docs/ingest.md` storage are unchanged — only the visible label.

## 2026-10-13 (Astro homepage: script-block parse error fixed)

### Fixed
- **Moved stray CSS out of the main `<script>` block on the Astro homepage** (introduced in 6b075b2 "Jonny's Done affordance"): four raw CSS rules (`.attn-circle`, `.attn-link`) sitting inside the script were a JS parse-time error that silently killed the whole block — stats, the "Needs Dave's attention" feed, pinned items, and the activity log were all dead client-side. Rules moved into the `<style>` block; all four inline script blocks now pass `node --check`. Page interactivity restored.

## 2026-10-13 (Astro homepage: "Awaiting Dave's reply" section)

### Added
- **"📬 Awaiting Dave's reply" section on the Astro homepage** (Dave's ask 2026-10-13): a live attention surface fed by the awaiting-reply registry. `~/workspace/tools/gen-awaiting-reply.py` parses `~/workspace/briefings/awaiting-reply.md` into `astro/awaiting-reply.json` (groups: urgent / recent / decisions / questions, each item with title, date, thread, thread deep-link, summary, high flag); the page renders four counted groups — Urgent, New this week, Open decisions, Unanswered questions — after "Needs Dave's attention" and before Pinned, reusing the feed card styles in dark/light. Fetch failure degrades to an "updating…" placeholder, never a blank hole.

## 2026-10-13 (Stat-tile row redesign — Jonny's verdict)

### Fixed
- **Stat tiles size to their content — clipping is now impossible.** Killed the fixed tile widths (`.ptile` was `flex:1 1 170px`; status tiles were capped at 25% width) that clipped longer labels mid-word ("MISSIO", "UNKNO", "SHIPPE") and even clipped the number "54". Tiles are now `flex:0 0 auto` with `white-space:nowrap` labels: each tile is exactly as wide as its words. Labels stay on one line so all tile numbers snap back into horizontal alignment. The strip scrolls horizontally (`overflow-x:auto`, quiet scrollbar) on desktop and phone instead of squeezing — data strips scroll, they never squash. Phone tile grid replaced with the same scroll-strip treatment.
- **Dropped the redundant "LIVE ·" tile prefix** (Jonny: the green edge already says live) — "M2 SHIPPED" and "PRE-ALPHA" read cleaner. Filter keys and tints unchanged.

## 2026-10-13 (Info panel: Open homepage button)

### Added
- **"Open" button next to "Copy" in the Homepage URL section** of the buddy info panel — opens the buddy's homepage in a new tab. Dave's ask from the panel: the URL field should just be a link.

## 2026-10-13 (Privacy scrub — house numbers)

### Fixed
- **House numbers scrubbed from the public dashboard.** Dave learned the whole dashboard is a public site and made privacy top priority. Street numbers removed everywhere they appeared: Fiddletown cabin (cabin/tech homepages) and the San Jose house (lenwood/quentin/sawyer/amanda/tech homepages, registry, page fragments). Street names stay — they're already public buddy names. First step toward the public/private buddy model (brief in progress).

## 2026-10-13 (Frosted-glass + button)

### Changed
- **New-buddy + button goes iOS frosted-glass.** Dropped the solid blue circle (was 72% opacity) for a translucent frosted circle with backdrop blur — matches the AssistiveTouch look Dave sent from his iPhone Shortcuts screen. Dark: translucent dark gray, white +; light: translucent white, dark +.

## 2026-10-12 (Full-screen phone panels)

### Changed
- **Side panels go full-screen on iPhone.** The buddy-list drawer and the buddy info panel each take the whole screen when open (both keep their close boxes); with both closed you see the main view. No more 85%-width drawer or bottom-sheet peek — Dave's call from the hot tub.

## 2026-10-12 (Buddy search autocomplete)

### Added
- **Buddy search now has an autocomplete dropdown.** Type in the search box and a dropdown appears with up to 8 matching buddies (icon, name, parent context) — narrows as you type. Arrow keys to move, Enter to jump, Escape/click-outside to dismiss. Classic typeahead pattern.

## 2026-10-12 (Dump delete fixes)

### Fixed
- **Dump count now updates immediately on delete** (was waiting for the 6-second undo window).
- **Deleting the last dump poofs the list** — the dump list fades and collapses, but the textarea stays. The section minimizes to its add controls instead of disappearing entirely (Dave's "minimized section" pattern).

## 2026-10-12 (New Buddy sheet clipping fix)

### Fixed
- **New Buddy sheet no longer bleeds off the right edge on phones.** The sheet's width didn't account for its padding (box-model bug). Now uses proper gutters with `box-sizing:border-box` — Jonny's verdict, Dave-approved.

## 2026-10-12 (Voice picker previews)

### Changed
- **Voice picker cards now have play buttons.** The 30 voices with audio samples get a ▶ button right on the card — hear the voice before picking it, without selecting first.

## 2026-10-12 (Dump fallback queue)

### Changed
- **Dumps no longer vanish when the GitHub write fails.** If there's no token, a bad token, or no network, the dump is queued in localStorage, shows in the feed with a "pending sync" badge, and flushes to the repo automatically on the next successful write or page load.

## 2026-10-12 (Section poof-away animation)

### Changed
- **Info panel sections poof away when their last item is completed.** Marking the final "Needs your attention" item done dims the section text, then fades/shrinks/collapses it — sections below scooch up smoothly. Applies to "Mark all done" too.

## 2026-10-12 (Atlas views follow buddy-list filter)

### Changed
- **Atlas views now respect the buddy-list search filter.** Filtering buddies in the sidebar also filters all seven Atlas lenses (org, lineage, ledger, colonnade, terrain, halo, constellation). Matching buddies show with their ancestors (for hierarchy context) and descendants.

## 2026-10-12 (BMW homepage repair plan; version comparison fix)

### Added
- **BMW Buddy homepage: Repair plan section.** Shows Hans's E61 fuel-system repair plan in priority order with parts pricing and product links (low-pressure pump, DMTL pump, EKP module, sensor, battery, injectors). Includes part-number corrections (DMTL 13907614005 does not exist, correct is 16137193479; pump 16147163212 superseded by 16117373521; sensor 13537547876 superseded by 13537622231).

### Fixed
- **Version comparison now checks ordering, not just inequality.** The update banner and What\u2019s New sheet no longer claim an older build "is available" when the local build is actually newer.
- **What\u2019s New sheet shows actual changes.** Missing CHANGELOG entries added so the "new since you last looked" section reflects recent work.

## 2026-10-12 (Voice setting: per-buddy voice picker + voice notes toggle; persona header + audio previews)

### Added
- **Per-buddy Voice setting.** New "Voice" section in the info panel (next to
  Persona): pick from 1,066 TTS voices via a searchable picker, with a
  "Voice notes in threads" toggle (default OFF per Dave's token-concern
  decision). Voice + toggle persist to buddies.json via the GitHub API route.
  Voice catalog lives in voice-catalog.json — extensible file format, add a
  voice by editing the JSON and rebuilding. (Pinned: user voice
  exchange/sharing.)
- **Voice preview samples.** 30 curated voices have "Preview" buttons in the
  Voice section — hear "Hello, I'm [name]" right from the panel.
- **Persona header shows selection.** Collapsed Persona section now reads
  "PERSONA: Pirate captain" instead of bare "PERSONA".
- **Persona audio previews.** Expanded Persona section shows the voice-sample
  quote in italics plus a "Hear it" button — 87 personas have pre-generated
  audio of their signature line. (29 personas have no quoted line in the
  roster, so no button for those.)

### Changed
- **Persona picker** now shows the voice-sample quote on each card (parsed
  from the roster), per Dave's "add it back" request.

## 2026-10-12 (Done affordance: Jonny's circle + Undo; build numbers on What's new)

### Added
- **Jonny's Done affordance.** The info panel's attention items now use the
  existing empty circle as the checkbox — tap it and it fills with accent +
  white check (~200ms), the tile glides out, and a "Marked done. Undo." toast
  appears for 6s. No confirmation dialog, ever. Done items leave the list
  entirely (emptiness is the goal); the done timestamp is recorded in
  `S.seen[id]` for the Undo window and persists. "Mark all done" gets the
  same Undo treatment. `role="checkbox"` + `aria-checked` + keyboard support.
- **Build numbers on What's new.** The update banner now reads "You're on
  build X. Build Y is available." The What's new sheet shows your current
  build at the top, plus the new build when one is available. (Dave: "i think
  they should.")

### Changed
- **Astro's homepage uses the same circle.** The "✓ Done" button is replaced
  with Jonny's circle checkbox; "Need more info" is now a quiet subordinate
  link. Same 200ms fill, glide-out, and GitHub writeback behavior.

## 2026-10-12 (Ledger: drag grippers + Parent one-liner)

### Added
- **Drag grippers on Ledger rows.** Every row except the root now carries a
  quiet dot-grid gripper (Jonny's language). Grab it and drop onto another
  row to reparent — same cycle protection, ghost, drop highlighting, and ~6s
  undo toast as org-chart tile drag. The gripper arms immediately (explicit
  affordance, no press-and-hold); taps on the row itself still open the
  panel.

### Changed
- **Parent section is now a one-liner.** The info panel shows just
  "Name (kind)" as a clickable link instead of the full tile; tapping it
  opens the parent's panel. The Change button stays in the header.

## 2026-10-12 (Info panel: persona picker)

### Added
- **Persona picker in every buddy's info panel.** Each buddy now shows its
  current persona (name + voice blurb) in a dedicated Persona section, with
  "Change persona" opening a searchable picker over the full 116-entry
  roster (baked in at build time from persona-roster.md) and a "Surprise
  me" button for a random pick. Works for Astro too. Selections persist to
  `buddies.json` in the buddy-system repo via the dashboard's GitHub token
  (same fetch-modify-write pattern as buddy creation), with an optimistic
  local update. Phone-friendly bottom-sheet on small screens; dark-mode
  safe.

## 2026-10-12 (Tree view: zoom chrome fix + Shift+click subtree collapse)

### Fixed
- **Zoom no longer scales the Quick answers row or the Atlas lens pill.**
  Both were rendered inside the zoomed chart container, so the zoom slider
  grew/shrank them along with the chart. They now live in a dedicated
  un-zoomed chrome strip above the chart scroll pane.
- **Shift+click a sidebar collapse chevron collapses/expands the whole
  subtree**, not just that row. Plain clicks still toggle only the clicked
  row. Chevron tooltips now mention the Shift+click behavior.

## 2026-10-12 (Portfolio Buddy: attention action buttons)

### Added
- **Attention action buttons** on the Portfolio Buddy homepage's two review cards
  (Reimagined Portfolio product brief + mission statement): ✓ Done / Need more
  info, per Dave's directive (rolled out from the Dell'Aquilas homepage).
  "Done" appends a DONE entry to portfolio-buddy/docs/ingest.md asking the
  buddy to clear the item from buddies.json; "Need more info" appends a
  FOLLOW-UP entry. Tiles resolve immediately in the UI ("Marked done",
  actions hidden) and persist that state in localStorage (`buddyTree.v3` /
  `attnDone`); writes reuse the brain-dump box's shared-token pattern
  (`ghToken`). Adapted from gen_basic_homepages.py's ATTN_JS to the page's
  serif/pill-button language; dark mode and phone-friendly preserved. Also
  added the product-brief review to the buddies.json attention registry so
  both tiles map to real attention items (ids: portfolio-buddy-brief,
  portfolio-buddy-mission). All three inline script bundles pass `node
  --check`; rebuilt dashboard index.html verified to embed the new attention
  entry.

## 2026-10-12 (Personal Buddy: attention action buttons)

### Added
- **Attention action buttons** on the Personal Buddy homepage's "Needs your
  attention" card (✓ Done / Need more info), per Dave's directive (rolled out
  from the Dell'Aquilas homepage). "Done" appends a DONE entry to
  personal-buddy/docs/ingest.md asking the buddy to clear the item from
  buddies.json; "Need more info" appends a FOLLOW-UP entry. Tile resolves
  immediately in the UI (fade + "Marked done", hides actions and the Read-the-
  brief link) and persists the resolved state in localStorage; writes reuse the
  brain-dump box's shared-token pattern (buddyTree.v3 / ghToken). Adapted from
  gen_basic_homepages.py's ATTN_JS to the warm-paper theme; dark mode and
  phone-friendly preserved. Write path verified end-to-end via the GitHub API
  (test entry confirmed, then removed).

## 2026-10-12 (Discovery Buddy: attention action buttons)

### Added
- **Attention action buttons** on the Discovery Buddy homepage's "Needs Attention"
  tile (✓ Done / Need more info), per Dave's directive (rolled out from the
  Dell'Aquilas homepage). "Done" appends a DONE entry to docs/ingest.md asking
  the buddy to clear the item from buddies.json; "Need more info" appends a
  FOLLOW-UP entry. Tile resolves immediately in the UI and persists in
  localStorage; writes use the shared ghToken (same pattern as the brain-dump
  box). Restyled to the listening-room theme; dark+light mode, phone-friendly.
  Behavior unit-tested with mocked DOM/fetch (10 assertions).

## 2026-10-12 (Charts Buddy: attention action buttons)

### Added
- **Attention action buttons on the "Needs Dave's attention" tiles** (Dave-approved rollout from the Dell'Aquilas homepage) — ✓ Done / Need more info buttons + a status line per tile. Done appends a DONE entry to charts-buddy/docs/ingest.md asking the buddy to clear the item from buddies.json, resolves the tile immediately (fade + status), and persists the resolved state in localStorage; Need more info appends a FOLLOW-UP entry. GitHub writes reuse the brain-dump box's shared-token pattern (buddyTree.v3 / ghToken). Adapted from gen_basic_homepages.py's ATTN_JS to the page's amber Kin theme; dark mode + phone-friendly preserved.

## 2026-10-12 (Little Guy Buddy: attention action buttons)

### Added
- **Attention action buttons on the "On my mind" tiles** — each tile now carries ✓ Done / Need more info buttons + a status line (Dave-approved rollout from the Dell'Aquilas homepage). Done appends a DONE entry to docs/ingest.md asking the buddy to clear the item from buddies.json, resolves the tile immediately in the UI, and persists the resolved state in localStorage; Need more info appends a FOLLOW-UP entry. GitHub writes reuse the brain-dump box's shared-token pattern. Adapted from gen_basic_homepages.py's ATTN_JS to the page's warm theme; dark mode + phone-friendly preserved.

## 2026-10-12 (Morning)

### Added
- **Text size slider** in Settings → Advanced — scales text and UI throughout the app from 80% to 130%, like the text-size slider on iPhone and Watch. Live preview as you drag.
- **Develop section** in Settings — pre-launch tools: **Simulate new user** toggle (empties the data file in-memory to preview the fresh-link experience; your real data is stashed and restored on toggle-off or reload, with a persistent banner while active), build number display, and **Clear this device's local data**.
- **Home-screen icon badge** — the app icon shows your pending attention-item count (Badging API; iOS 16.4+ installed web apps, Chromium). Updates on launch and whenever you clear an item; clears when you're all caught up.

### Changed
- **Org chart beauty pass** (Jony): generation pills (CHILD/GRANDCHILD) removed — depth is already encoded vertically; Quick Answers collapsed to one horizontally-scrolling row; connectors are 1px hairlines instead of 2px slate; parent/child gap tightened from 26px to 20px; the composition centers vertically in the pane when it fits instead of anchoring to the top.
- **Collapse pill taps** no longer open the info panel — tapping ⌄/› only collapses/expands; tapping anywhere else on the tile opens the panel. (Root cause: `stopPropagation` doesn't stop sibling listeners on the same element; switched to `stopImmediatePropagation`.) Same fix for the Quick Answers ✓ button.

## 2026-10-12 (Evening polish)

### Added
- **Quick answers bar** on the tree view — up to 12 pending attention items as tappable chips; tap to jump to that buddy's question.
- **Architect Buddy** (📐) — Dave's digital architecture specialist.

### Changed
- **Zoom slider minimum** is now fit-to-chart — drag all the way down to see the entire tree.
- **Search box** moved to the top of the left panel, above Buddies.
- **Breadcrumb** shows the buddy's display name, not the raw repo slug.
- **Double-click/tap on panel grippers** closes the panel (sidebar and info panel).
- **Left-edge swipe** opens the sidebar on all screen sizes, not just phones.
- **Settings rows** use the ⋮⋮ gripper; visibility checkbox moved to the left (Buddy fields and Main views).
- **Settings resize thumb** now works on touch (was mouse-only).
- **Hot Tub homepage** — "child of" → "inherits from Cabin Buddy".
- **Hans/BMW artifacts** — E61 diagnostic report linked in both.

### Fixed
- **Projects view Shift+click** on a section chevron collapses/expands all sections.

## 2026-10-12 (Info panel + tree polish)

### Added
- **Change parent:** "Change" button in the Parent section opens a picker dialog — filter-as-you-type, "Top level" pinned at top, self/descendants excluded to prevent cycles (per Jony).
- **Add child:** bare ⊕ in the Direct reports header (44px hit area, per Jony) — header supplies the noun, glyph supplies the verb.
- **Parent, Siblings, Linked buddies** now appear in Settings → Buddy fields ordering.
- **Shift-click a section header** collapses/expands all sections at once.

### Changed
- **"Setup drill" → "Onboarding"** across the dashboard.
- **Info panel field order:** About moved to bottom, Private/Shared notes right above it.
- **Left panel order:** Buddies, search, Business Plans, Views (last).
- **Org chart tiles** auto-size to content (180–320px), names truncate with ellipsis, descriptions clamp at 3 lines.
- **Info panel always opens scrolled to top** (no more restoring last position).
- **Settings panel** per Jony: Done is now a real button, factory actions are quiet links ("Reset defaults"/"Save as defaults"); one toggle metaphor (blue check-circles everywhere); "(px)" unit hangs on the input; Attention header effect moved to Advanced.
- **~40 side chats renamed** to match dashboard icons/names.

## 2026-10-11 (Jony's New Buddy sheet tweaks)

### Changed
- **"Send request" → "Start the setup"** — you're hiring, not filing a ticket.
- **No pre-selected persona** — the button waits until you deliberately pick a face.
- **Example placeholders** on the name field ("e.g. Car Buddy") and purpose textarea.

## 2026-10-11 (Shift+← configurable)

### Added
- **Advanced → Shift+← action:** choose what Shift+Left does — Promote (move buddy up one level, default), Go to parent (navigate), or Nothing.

## 2026-10-11 (New Buddy sheet: content height + Advanced width)

### Changed
- **New Buddy sheet height now hugs its content** (still capped at 88vh with internal scroll; grab handle still resizes).
- **New Advanced section in Settings** with a fixed width control for the New Buddy sheet (320–900px, default 560).

## 2026-10-11 (New Buddy sheet resizable)

### Added
- **Drag the grab handle** at the top of the New Buddy sheet to resize its height.

## 2026-10-11 (Buddy creation keyboard shortcuts)

### Added
- **Shift+↑ creates a parent, Shift+↓ a child, Shift+→ a sibling** — for the currently selected buddy. Works anywhere except inside text fields.

## 2026-10-11 (Settings section order)

### Changed
- **Settings: Main views now sits above Buddy fields.**

## 2026-10-11 (＋ ↑ Parent / ＋ ↓ Child)

### Added
- **＋ ↑ Parent button** in the Parent section: creates a new buddy above the current one (manager/parent) and reparents the current buddy under it.
- **＋ ↓ Child button** in Direct reports (restyled): creates a buddy below — direct report, subordinate, device/appliance, or activity.

## 2026-10-11 (New Buddy request sheet)

### Changed
- **New Buddy is now a bottom sheet:** name field, scrollable persona picker (24 voices, tap the one that makes you grin), and a purpose textarea. The request (name + persona + purpose) lands in `docs/inbox/` for the watcher to pick up.

## 2026-10-11 (Floating New Buddy button)

### Added
- **＋ Floating New Buddy button:** sticky round FAB (bottom-right) with a plus sign. Opens a dialog (name, icon, type) that writes a request file to `docs/inbox/` — a watcher job picks it up every 15 min and pings Dave to run the full setup drill.

## 2026-10-11 (A.K.A. section)

### Added
- **A.K.A. section in the buddy info panel:** add and remove nicknames/aliases per buddy. They're searchable, show in the panel header, and save per device. Logged to the change journal.

## 2026-10-11 (Side panels snap shut on resize)

### Added
- **Snap-to-close on panel resize:** drag the sidebar narrower than 140px (or the buddy panel narrower than 220px) and the panel snaps fully shut instead of stopping at its minimum width — no more pushing through a threshold. Reopening restores your last width.

## 2026-10-11 (Release Notes entries go professional)

### Changed
- **Release Notes entries now use the Change Log row format:** each change renders as a professional row with a type-colored icon tile (green + for Added, blue ~ for Changed, red ✓ for Fixed), bold title, description, and date/type meta — instead of plain markdown.

## 2026-10-11 (Changelog/Release Notes no horizontal scroll)

### Fixed
- **Changelog and Release Notes no longer scroll sideways:** long URLs and unbreakable text now wrap instead of pushing the view wider than the screen.

## 2026-10-11 (Release Notes view)

### Added
- **🎁 Release Notes view:** renders CHANGELOG.md in the same format as the What's New update modal — "New since you last looked" on top, earlier history in a collapsible section below. Visiting marks the notes seen, so the "new" section stays honest.

## 2026-10-11 (Right-panel gripper stays put)

### Fixed
- **The right panel's resize gripper is now sticky:** it was `position:absolute` inside the scrolling panel, so it scrolled away with the content. It's now `position:fixed` tracking the panel edge via a `--bpw` variable (same pattern as the sidebar gripper), so it stays glued to the panel edge while you scroll. Hidden in bottom-sheet mode where a side gripper doesn't apply.

## 2026-10-11 (Dump success message goes green)

### Changed
- **"dumped ✓" now shows in the dashboard's green** (`--grn-tx`): the success confirmation under the dump field picks up the same green used for Live/Cleared states. Text unchanged.

## 2026-10-11 (Dump placeholder pulses gently)

### Changed
- **The "Dump what's in your head about…" placeholder now breathes:** a slow 3.2s bright-to-dim pulse on the dump field's placeholder text, so the invitation to dump is alive without shouting.

## 2026-10-11 (Secret nerd settings: pan gearing slider)

### Added
- **🤓 Nerd settings (secret):** tap the build number 5 times to unlock a hidden settings panel. First knob: tree pan gearing slider (0.25×–3×, default 1×) — tune how fast the tree pans under your finger. Persists per device.

## 2026-10-11 (Scroll-to-top on the info panel)

### Added
- **Floating scroll-to-top button on the buddy info panel:** mirrors the sidebar's frosted chip — appears once you've scrolled down, centered at the panel's bottom, smooth-scrolls back to top on tap. Position tracks the panel width through resizes.

## 2026-10-11 (Tree pan speed fixed at low zoom)

### Fixed
- **Panning felt geared down when zoomed out:** the finger delta is in screen pixels but the scroll offsets live in the zoomed coordinate space — at 50% zoom every pan moved at 2:1. The delta is now scaled by 1/zoom, so panning feels 1:1 at any zoom level.

## 2026-10-11 (What's New modal actually shows what's new)

### Fixed
- **"What's new" always said "nothing new":** the modal marked the changelog's newest heading as seen *before* splitting it into new vs. old sections — so every section landed in "old" and the "new" list was always empty. It now splits first, renders, and only then marks the latest heading seen.

## 2026-10-11 (Press-and-hold to drag on the tree)

### Changed
- **Tree node drag now needs a press-and-hold (~400ms) before it arms:** previously any press that moved >6px started a drag, so taps could accidentally grab nodes. Now a quick tap always opens the detail panel; holding briefly shows an accent ring on the node, and only then does moving start the drag.

## 2026-10-11 (Undo for tree reparenting)

### Added
- **Undo toast when moving a buddy on the tree:** dragging a buddy onto a new parent (or onto blank background to orphan it) now shows an Undo toast for ~6 seconds instead of just a confirmation. Tapping Undo restores the previous parent. Follows the same "forgiveness, not friction" pattern as dump deletes.

## 2026-10-11 (Dump edit fixes)

### Fixed
- **Edit button on freshly-added dumps did nothing:** `prependDumpEntry` never wired the new entry's edit/delete buttons and left the older entries' indices stale (tapping edit hit the wrong dump). Buttons are now re-indexed and wired after every prepend.
- **No way to exit dump edit mode on touch devices:** the editor only closed on Escape (no Escape key on iPhone). There's now a Done button that flushes any pending autosave and re-renders the feed.

## 2026-10-11 (Add child/sibling from the info panel)

### Added
- **"+ Child" and "+ Sibling" buttons in the buddy info panel:** the Parent section header carries "+ Sibling", the Direct reports header carries "+ Child". Tapping either opens a dialog for the new buddy's name, icon (emoji picker), and type. The dashboard writes the new entry straight to `buddies.json` on GitHub (needs the GitHub token from the gear menu), flags it `setup_pending`, and adds an attention item so Astro runs the full setup drill (mission doc, repo, side chat, homepage).

## 2026-10-11 (Detail-panel polish: private notes, attention count, checkmarks, collapse fix, wider resize grips)

### Changed
- **"Notes" is now "Private notes" (Dave's ask):** the device-local notes section was too easy to confuse with "Shared notes". Renamed in buddy panels, business-plan pages, and field settings.
- **"Needs your attention" header now shows the count:** e.g. "Needs your attention (3)".
- **"Mark seen" is now a circle checkmark:** each attention item starts with an empty circle ○; tapping it marks the item seen and it becomes a filled checkmark ✓ (the item dims as before). The bulk "Mark all seen" action is unchanged.
- **Side-panel resize grips are easier to grab:** the draggable zone along each panel's inner edge grew from 14px to 28px, and a small movement threshold means plain taps near the edge no longer start an accidental resize. Double-click still resets to the default width.

### Fixed
- **Homepage URL section wouldn't collapse:** its content row carries an inline `display:flex` style, which overruled the collapse stylesheet. The collapse rule now wins over inline display styles, so every section header collapses.
- **Photos header lost its collapse arrow + drag grip** when the photo count refreshed (it rewrote the whole header). It now updates only the label, preserving both controls.

## 2026-10-11 (Tree view: real hierarchy, splitter, section grips, tooltips, ingest fix)

### Fixed
- **Tree view showed the whole hierarchy as "Orphaned buddies":** only `FAMKINDS` children of the root rendered in the org chart, so Project Buddy (kind `assistant`) and everything under it landed in the orphan grid as indented tiles. The org chart now shows every direct report of the root side by side; only truly parentless buddies go to the orphan section. Retired `FAMKINDS`; depth-1 tile tags now show the buddy's actual kind.
- **Ingest dumps never loaded when opening a buddy from a view:** `refreshTokenUI` only called `renderIngestFeed` when `S.sel === 'buddy:' + id`, but opening from the Tree view leaves `S.sel` as `view:tree`. The feed (and shared notes) now load whenever the panel renders a buddy.

### Added
- **Draggable splitter** between the buddy-tree pane and the orphaned-buddies pane; each pane has its own zoom slider + zoom-to-fit. Split position and both zooms persist per device. Dragging an orphan onto a tree buddy still reparents it.
- **⋮⋮ grippers** on the far right of detail-panel section titles — drag to reorder sections directly; order persists via `fieldOrder`.
- **Sidebar section headers (Views, Buddies) collapse** on click, like Business Plans already did.
- **Tooltips are now real popovers:** hover preview on mouse, tap-to-pin with an × close button on touch (the old hover-only CSS tooltips stuck open on touch screens). Tap-outside and Escape also dismiss.

## 2026-10-11 (Tree-view inspection fixes)

### Fixed
- **Joel Nelson tile showed "UNDEFINED" badge:** his registry entry was missing `kind` (set to `personal`, like James's).
- **Zoom slider had a garbled screen-reader label** ("Zoom in to zoom out") — now reads "Tree zoom".
- Not a bug: the "53" next to BUDDIES in the sidebar is the unseen-attention count (reviews awaiting Dave), not a buddy count — the 68-buddy total in the header is correct.

## 2026-10-11 (Memo dismiss)

### Added
- **Close link on the critical memo card (Dave's ask):** the "Critical memo" banner on buddy detail panels now has a × close control. Dismissing it hides the memo everywhere and remembers the choice on the device — a new memo (new ID) will still show.

## 2026-10-11 (Zoom slider thumb contrast)

### Fixed
- **Tree zoom slider thumb is high-contrast now (Dave's ask):** the vertical zoom slider's thumb was a small native control tinted with the accent color — easy to miss. It's now a solid accent puck with a background-colored ring and halo, on a defined track, so it reads against any tile in both themes.

## 2026-10-11 (Tree tile rename fix)

### Fixed
- **Tree tiles now reflect renames immediately (Dave's catch):** renaming a buddy from the info panel updated the left buddy list and the panel itself, but the tree chart tiles kept showing the old name until a full page reload. Tree tile labels now update in place on rename (pan/zoom preserved). Also fixed the same staleness for icon changes and "reset tree" after drag-reparenting: `refreshViews()` now always re-renders the tree from current data instead of restoring a cached copy.

## 2026-10-11 (Idea Buddy)

### Added
- **Idea Buddy** 💡 — Dave's brainstorming desk, child of Project Buddy. Runs ideation sessions, curates the persona roster (101+ personality options for new hires, seeded from Dave's 2026-10-11 riff), and feeds personality picks into the new-hire drill. Mission: Idea Buddy — Mission Statement (review pending). Repo: davedellaquila/idea-buddy.

## 2026-10-11 (Floating chevron fix)

### Fixed
- **Floating `>` chevron is state-dependent (Dave's rule):** on iPhone, tapping the floating `>` while the right (detail) panel is open now closes the right panel and returns to the current view (e.g. tree). Previously it toggled the left drawer open, which was wrong. With the right panel closed, it still toggles the left drawer as before.

## 2026-10-11 (AKAs for any buddy)

### Added
- **`aka[]` field** — any buddy can now have aliases ("also known as"). AKAs are matched by both dashboard search boxes and shown in italics under the buddy's name on the detail panel. First use: Designer is aka "UX designer", "visual designer", "design guy", "design gal" (Dave's ask).

## 2026-10-11 (Designer rename)

### Changed
- **Design Buddy → Designer** — Dave: "for being a coder too." Thread, mission doc, and dashboard entry renamed; repo (`design-buddy`) and buddy ID unchanged.

## 2026-10-11 (Person buddies renamed to full names)

### Changed
- **Full-name rule** — person buddies now carry the person's full name as their display name (Dave's refinement), superseding the possessive rule set earlier the same day. Renamed 15: Joel Nelson, James Michael Day, Carl Towne, Nancy Dell'Aquila, Quentin Dell'Aquila, Sawyer Dell'Aquila, Amanda Perez, Emile Dell'Aquila, Ron Dell'Aquila, Mei-ying Dell'Aquila, Jessica, Sarah Dell'Aquila, Rachel, Emil Dell'Aquila, Martha Dell'Aquila. Threads, mission-doc titles, and registry updated; IDs/slugs/repos unchanged. Jessica and Rachel stay first-name-only (last names unknown).

## 2026-10-11 (New buddies: James's Buddy 🎹, Carl's Buddy 🛻)

### Added
- **James's Buddy** — person buddy for James Michael Day (dueling-piano musician, Modern Dueling Pianos), met at Acorn Ridge Casino 2026-10-10. Child of Relationship Buddy. Repo `davedellaquila/james-buddy` (card photos stored), mission statement, side thread, v1 homepage with dossier (bio, Sharks organist, 4+ shows/week, TapSnap tip jar, 500+ weddings, JMD Entertainment).
- **Carl's Buddy** — person buddy for Carl Towne, Fiddletown neighbor (general contractor, State of California; keeper of the community wood splitter). Child of Relationship Buddy. Repo `davedellaquila/carl-buddy`, mission statement, side thread, v1 homepage. Open: wood-splitter borrow (Dave texted Carl 2026-10-11).

## 2026-10-11 (Tree root flip: Astro at the top)

### Changed
- **Astro is now the tree root** — the org chart matches reality: Astro (🚀, chief of staff) sits at the root, Project Buddy (🧭) is a direct report instead of the reverse. `ROOT_ID` constant in build.py replaces ~15 hardcoded `project-buddy` root assumptions (default selection, org chart, drag-and-drop guards, icon fallback). Dashboard icon now defaults to 🚀.

## 2026-10-11 (Buddy avatars: images, favicons, nicer picker)

### Added
- **Per-buddy favicon** — opening a buddy's card or homepage now sets the page favicon + Apple touch icon from the buddy's image, or renders the buddy's emoji to a PNG data URI when there's no image. "Save to desktop / Add to Dock" now carries the buddy's face (Dave's ask).
- **Avatar image upload** — the avatar picker gained Upload/Remove image: uploads are downscaled to 512px JPEG and pushed to `avatars/<buddy-id>.jpg` in the dashboard repo (GitHub token), shown on the card, homepage, and favicon.
- **Categorized emoji picker** — ~200 emojis across 8 categories (Smileys, Gestures, Animals, Food, Activities, Travel, Objects, Symbols) plus paste-any-emoji, on the dashboard card; homepages got their own tap-the-avatar picker sharing the dashboard's localStorage override store.

## 2026-10-11 (Buddy links: many-to-many, Rae Assist style)

### Added
- **Buddy links** — `links[]` on registry entries + a "Linked buddies" section on every buddy's detail card, with reverse links computed automatically (link once, shows on both cards). Dave's direction: "just like in Rae Assist everything can be linked to everything. Everything's a many-to-many." First live link: Joel's Buddy → James's Buddy (renders "Buddy being set up" until James's buddy exists).
- **Connections section on Joel's Buddy homepage** — links to James; Acorn Ridge Casino / Acorn Ridge Lodge facts confirmed on the page.

## 2026-10-11 (Drawer fixes + Manifest card stack)

### Fixed
- **Scroll-to-top** — tapping `#sb-to-top` no longer closes the phone left drawer; it only scrolls the sidebar to top.
- **Left-edge swipe** — swipe-right from the left edge opens the drawer again without fighting Tree pan or panel swipes.
- **Manifest list cards** — on phone, title (+ status) on the first row and description flush left full-width underneath (same stacked pattern as Business Plans / Projects).

## 2026-10-11 (Positioning: "dump anywhere, it's routed")

### Added
- **"Dump anywhere, it's routed"** captured as a core selling point in FEATURES.md — stream-of-consciousness capture into any homepage dump box or thread lands in a durable inbox and is routed to the right buddy; Dave never decides where a thought goes.

## 2026-10-11 (Dashboard: default project homepage redesign)

### Added
- **Redesigned default project homepage view** (Design Buddy, Dave-approved) — the auto-generated fallback in `buddyHomepageHtml` (build.py) for buddies without a custom homepage: hero header (icon tile, name, tagline, status pill, stat strip), desktop two-column grid (About / Plans / Artifacts + amber Needs-attention rail and sub-buddy chips), full-width 🧠 brain-dump box writing to the buddy's docs/ingest.md via the dashboard's GitHub token path, attention items link to their referent when a URL is present. Inherits dashboard dark/light theme; single column under 960px. Also fixed two latent bugs: cards used undefined `--card` var (rendered transparent) and plans never rendered (`PLANS[b.id]` on an array).
- **Attention-item URLs** — 43 registry attention items backfilled with links (brief/mission docs, dashboard); new standing rule: every homepage attention item must link to its referent.

## 2026-10-11 (Dashboard: search clear button)

### Added
- **Clear (×) button on the dashboard's buddy search box** — Dave's spot: the sidebar search had no visible way to clear it. Explicit × button appears when there's text; tapping clears the query, refocuses the field, and re-renders the list. Works everywhere regardless of native `type=search` behavior.

## 2026-10-11 (Portfolio Buddy: new buddy)

### Added
- **Portfolio Buddy** (🖼️ provisional icon — Dave picking the final one) — child of Project Buddy. Dave's expert on online portfolios: researches contemporary best practices for product-design + engineering portfolios, owns/manages his portfolio site(s) with dynamic updates from its mission-control homepage, keeps a portfolio-ideas list, supports multiple audiences (design/engineering/Apple-safe). Consults Astro + Project Buddy for project data (no own tracker). Owns the "Redo personal website" goal. Mission statement: [Portfolio Buddy — Mission Statement](https://docs.google.com/document/d/1uby4pNjL4IRVLAqd_gVG_5bOGdjgcjZ0L_kobSOSVt4/edit) — Repo: [davedellaquila/portfolio-buddy](https://github.com/davedellaquila/portfolio-buddy) (private, docs/mission-statement.md). Template homepage generated with 🧠 brain-dump box + dark/light mode; custom mission-control design comes via thread INIT. Dashboard entry added (61 buddies).

## 2026-10-11 (Little Guy Buddy: brain-dump box + dark mode)

### Added
- **Little Guy Buddy homepage: 🧠 Brain dump box** — textarea + "Dump it" button (Cmd/Ctrl+Enter), appending timestamped entries to docs/ingest.md in the little-guy-buddy repo via the GitHub API (same write path as the dashboard ingest panel). Repo resolved from buddies.json via `data-buddy-id` (no hardcoded names); token read from dashboard localStorage (`buddyTree.v3` → `ghToken`) with a one-time token prompt fallback. Restyled to the page's warm cat theme, dark-mode aware. Write path tested end-to-end against the real API (test entry confirmed in docs/ingest.md, then removed).
- **Dark mode for the Little Guy Buddy homepage** — full `prefers-color-scheme` dark theme in warm browns, per the buddy-system standing requirement (light-only is not shippable).

## 2026-10-11 (Discovery Buddy: brain-dump box on homepage)

### Added
- **🧠 Brain dump section** on the Discovery Buddy homepage (textarea + "Dump it",
  Cmd/Ctrl+Enter). Appends timestamped entries to docs/ingest.md in
  davedellaquila/discovery-buddy via the GitHub contents API — the same write
  path as the dashboard's ingest panel. Token read from dashboard localStorage
  (buddyTree.v3 → ghToken, shared origin); one-time token prompt if missing.
  Repo resolved from ../buddies.json via data-buddy-id="discovery-buddy".
  Restyled to the listening-room theme; dark+light mode preserved.
  JS logic unit-tested with mocked DOM/fetch; write path confirmed with a
  labeled test entry in docs/ingest.md.

## 2026-10-11 (Design Buddy)

### Added
- **Design Buddy** — new buddy: Dave's resident design authority, "the Jony Ive on staff" (🎨 icon, child of Project Buddy, `Brief review` status). Reviews every buddy homepage/app for taste, owns the shared design language (dark + light mode, living pages, craftsmanship as differentiator), gives his product work a second eye when asked. Advisory only — owning threads implement; Apple-internal STIX work stays advisory-only. Full drill: [brief](https://docs.google.com/document/d/1_sUDucLCJfg2iB858pgHQWdOtt-vWPwOMqoXjhy3QYU/edit), private repo [davedellaquila/design-buddy](https://github.com/davedellaquila/design-buddy). Open: review cadence?; how prescriptive vs advisory?; proactive redesigns or on-request only?
- Dashboard now tracks 60 buddies.

## 2026-10-11 (Brain-dump box on every buddy homepage)

### Added
- **Dump box on all template homepages** — the dashboard's brain-dump (ingest) feature now ships on every template-driven buddy homepage (25 pages): a "🧠 Brain dump" section with textarea + "Dump it" button (Cmd/Ctrl+Enter), writing timestamped entries to that buddy's repo `docs/ingest.md` via the same GitHub API path as the dashboard's ingest panel. Reads the shared GitHub token from the dashboard origin's localStorage (`buddyTree.v3` → `ghToken`); resolves the repo from `../buddies.json`. Dark/light aware via `prefers-color-scheme`. Snippet reference: `docs/dumpbox-snippet.html`. Custom-designed pages (34, thread-owned) get a memo with the snippet + integration instructions instead of direct edits.
- **Template version marker** — `gen_basic_homepages.py` now stamps `<!-- BUDDY-BASIC-TEMPLATE v2 -->` and regenerates marker-carrying pages (previously it could only create pages for buddies without one, so the daily rebuild was a no-op for existing pages). Custom pages without the marker are never overwritten.

### Fixed
- **Missing repo links** — set `repo` for `family-buddy`, `finance-buddy`, `mga-buddy`, `ml500-buddy` (repos existed; the registry field was null/empty), so their dump boxes and dashboard repo links work.

## 2026-10-11 (Briefing Buddy split from News Buddy)

### Added
- **Briefing Buddy** — new buddy: the guy that sends Dave's briefings — morning (6:00 AM PT) + evening (6:00 PM PT) editions assembled from configured sections and live data, delivered to the Briefings thread and by HTML email (📋 icon, child of Project Buddy, `Brief review` status). Homepage is the settings page: what's on the briefing, morning vs evening, live preview of the next briefing's data. Full drill: [brief](https://docs.google.com/document/d/1s9ghZ-kyp9dag2whTPnk24ULLUJP3JW_0UGtocAynbs/edit), private repo [davedellaquila/briefing-buddy](https://github.com/davedellaquila/briefing-buddy). Open: final section lists?; 6 AM / 6 PM still right?; who else gets briefings?
- Dashboard now tracks 59 buddies.

### Changed
- **News Buddy mission** — refocused 2026-10-11 at Dave's direction: News Buddy is now Dave's expert on news sources (knows where news comes from, which sources to trust per topic, keeps the source list sharp); briefing assembly and delivery moved OUT to the new Briefing Buddy. Brief rewritten in place: [News Buddy — Brief](https://docs.google.com/document/d/11Zz2wGbuIKCqS7OSPOnjIAbz5VsmLQPvxS-OfRicSN0/edit); repo README + docs/brief.md updated to match.

## 2026-10-11 (Ticket Buddy, Hiking Buddy, Venue Buddy: three new buddies)

### Added
- **Ticket Buddy** — new buddy: finds tickets to the shows Dave wants to see — concerts, theater, comedy (🎟️ icon, child of Personal Buddy, `Brief review` status). Keeps the want-to-see list, hunts down ticket options with prices and seat info, flags onsales, price drops, and newly released seats. Pairs with Discovery Buddy (Discovery figures out what he'd like; Ticket Buddy gets him in the door). Full drill: [brief](https://docs.google.com/document/d/1rVlr7Hv4vpUSnA9aykPE7Jplx_KuIxttqXHDewnkV2E/edit), private repo [davedellaquila/ticket-buddy](https://github.com/davedellaquila/ticket-buddy). Open: sources beyond Ticketmaster?; travel range for shows?; per-show budget?
- **Hiking Buddy** — new buddy: the trusted list of local Fiddletown/Amador trails — distance, difficulty, time, highlights — plus hiking advice on demand (🥾 icon, child of Cabin Buddy, `Brief review` status). Seeded with the Lake Tabeaud loop (2.5 mi, easy, ~45–60 min). Born when Dave was giving a friend hiking advice. Full drill: [brief](https://docs.google.com/document/d/1NjOxDUcxRtnYzeKhhSZkEHHMYgvgGuYgwUGfjjIMx2M/edit), private repo [davedellaquila/hiking-buddy](https://github.com/davedellaquila/hiking-buddy). Open: which trails seed the list first?; expand beyond Amador County?
- **Venue Buddy** — new buddy: the shortlist of places worth checking out — wedding venues, wineries, restaurants, weekend spots (📍 icon, child of Personal Buddy, `Brief review` status). First entry: Oak Farm Vineyards, Lodi (~$4,500/wedding, ~300 capacity, 70-acre historic estate) as a candidate for Quentin and Amanda's wedding. Full drill: [brief](https://docs.google.com/document/d/1uAgDOGIkr06CphFQkdoEGubpOEcaTPsJ4AMXRXMHab0/edit), private repo [davedellaquila/venue-buddy](https://github.com/davedellaquila/venue-buddy). Open: wedding date, budget, guest count?; how many venues on the shortlist?
- Dashboard now tracks 58 buddies.

## 2026-10-11 (Discovery Buddy: scope widened to every form of entertainment)

### Changed
- **Discovery Buddy mission/tagline** — widened from music-only to every form
  of entertainment (YouTube, podcasts, TV, movies, books) per Dave, 2026-10-10
  ~10 PM: buddies.json mission + tagline, repo README + docs/brief.md, MEMORY.md.
- **Discovery Buddy homepage** — refreshed for the widened scope: category
  strip (music / YouTube / podcasts / TV / movies / books), kind column in the
  queue, taste seeds open for shows/books/podcasts, four open questions.
  Dark+light mode preserved.
- **`queue.md`** in davedellaquila/discovery-buddy — reframed for all
  entertainment with a Kind column (Regulators filed as 🎵 Music).

## 2026-10-11 (Discovery Buddy: custom homepage + check-out queue)

### Added
- **Discovery Buddy homepage** — custom living page at `discovery-buddy/`
  (spinning-vinyl hero, equalizer animation, check-out queue tracklist, taste
  profile, open questions, attention, links). Dark-first design with a
  `prefers-color-scheme: light` theme (dark-mode standing order). Wired via
  `"homepage": "discovery-buddy/"` in `buddies.json`.
- **`queue.md`** in [davedellaquila/discovery-buddy](https://github.com/davedellaquila/discovery-buddy) — check-out queue seeded with "Regulators" (unconfirmed: Warren G's "Regulate"?), heard at the dueling piano bar 2026-10-10.

## 2026-10-10 (Discovery Buddy: new buddy + dashboard entry)

### Added
- **Discovery Buddy** — new buddy: Dave's music discovery companion (🔍 icon, child of Personal Buddy, `Brief review` status). A durable "to check out" list for new bands/artists plus taste-tuned recommendations. Born at a dueling piano bar when Dave wanted to file away "Regulators" (unconfirmed: Warren G's "Regulate"?). Seeded with his country lean (Morgan Wallen, Gordon Mullen's "Cover Me Up"). Full drill: [brief](https://docs.google.com/document/d/1flMPErgNpYZjZS3X0uUm8pkS9uMTxJGzeezqxibPz8s/edit), private repo [davedellaquila/discovery-buddy](https://github.com/davedellaquila/discovery-buddy), side thread, review ask. Open: streaming service, recommendation cadence, seeding 3–5 beloved artists.

## 2026-10-11 (CRITICAL standing order: dark mode on every buddy website)

### Added
- **`AGENTS.md`** — agent init rules; CRITICAL requirement that every buddy
  website ships dark mode (`prefers-color-scheme` or equivalent).
- **`docs/standing-orders.md`** — durable memo (Dave is outdoors; update
  light-only homepages now).
- **Dashboard standing-order banner** — shown on every buddy detail panel;
  same memo on Project Buddy, Scaffold Buddy, and Astro homepages; ingest
  log entry on Project Buddy.
- **Manifest / INIT** — INIT summary and Per-buddy home page steps now
  require the dark-mode standing order; Scaffold lists it as a skeleton rule.

## 2026-10-10 (iPhone fixes: sidebar resize, zoom scrubber, touch drop targets)

### Fixed
- **Sidebar resize handle never hit-tested (root cause)** — the `#sb-resize` handle
  hung 7px past the sidebar's edge (`right:-7px`), but the scrollable sidebar clips
  overflow, so the overhang was dead for hit-testing on desktop too (only ~3px
  grabbed). Moved it fully inside (`right:0`, z-index bumped to 60). Same fix
  applied to the buddy panel's `#bp-resize` handle (`left:-7px` → `left:0`).
- **Sidebar resizable on iPhone** — the handle was `display:none` below 639px.
  It now shows on the drawer as a 28px touch target with `touch-action:none`
  (the existing pointer-events drag code already handled touch). Width clamps to
  the viewport (`min(560px, 92vw)`, min 200px) and re-clamps on rotate/resize;
  still persisted per device.
- **Zoom scrubber invisible on iPhone (root cause)** — the flex-centered org tree
  (`.tree { justify-content:center }`) overflowed to negative x-coords on narrow
  screens, widening the layout viewport (measured 410px on a 390px phone), which
  pushed the `position:fixed; right:10px` zoombar partly off-screen. The tree now
  uses `width:max-content; margin:0 auto` (identical centered look when it fits;
  overflows only rightward/scrollably when not), plus `overflow-x:clip` on
  html/body below 639px as a guard. Zoombar also chunkier on phones (64px wide,
  longer slider, z-index 30).
- **Chunkier touch drop targets** — during a touch drag, drop hit-testing now
  uses rects inflated by 16px around each node (smallest match wins on overlap);
  mouse path unchanged. Drag ghost is larger on coarse pointers (240px), and
  drop-target outlines are thicker.

## 2026-10-10 (Tree tile drag-to-reparent)

### Fixed
- **Tree node drag-to-reparent** — replaced the ⠿ gripper handles with whole-tile
  pointer-based dragging: grab any buddy tile on the chart and drop it onto another
  buddy to reparent it. Works with mouse and touch (iPhone/iPad), where the old
  HTML5 drag-and-drop grippers could never fire. Tap still opens the buddy detail
  panel (6px movement threshold separates click from drag); the click after a drag
  is swallowed. Cycle-safe (invalid targets get a red dashed outline), root can't
  be dragged, dropping on root makes a buddy top-level. Same localStorage
  persistence and reset path as sidebar reparenting.
- **Why the grippers never worked** — the ⠿ handles were never in the DOM: they
  were only emitted by the JS `renderOrgTree()`, which runs solely after a sidebar
  reparent creates localStorage overrides; the static tree baked into the page had
  no handles. Even had they rendered, HTML5 DnD doesn't fire on touch devices.
- **Background pan now pans the real scroller** — drag-to-pan on the chart
  background moved nothing: `attachPan` scrolled `#treezoom`, which has no
  scrollable overflow (the chart scrolls inside its inner `.chart`). It now pans
  the `.chart` scroller.
- **Drop-highlight crash** — `initTreeDrop`'s `dragover` handler threw
  `Cannot read properties of null (reading 'classList')` whenever a sidebar drag
  hovered blank chart background (`n` was null). Added the missing null guard.

## 2026-10-10 (Tree view: org chart on phones)

### Changed
- **Tree view on iPhone/small screens** — the org chart no longer flattens into a vertical card list under 640px. Phones now show the real chart: pan with a finger, zoom with the floating slider (⛶ fits the whole tree). Dave's call: he wanted the chart, not the cards.

## 2026-10-10 (Shopping Buddy: new buddy + dashboard entry)

### Added
- **Shopping Buddy** — new buddy: Dave's personal shopping companion ("a genuinely useful tool, not a toy" — his words). Full scope: deal hunting + purchase research. Owns the watch list, price history, research, and decision log. Full drill: [brief](https://docs.google.com/document/d/1dALnh7njN6Ji4jCMhWMIrIwsKDeFSvftzmCfkMRAE6I/edit), private repo [davedellaquila/shopping-buddy](https://github.com/davedellaquila/shopping-buddy), side thread, review ask. Dashboard entry (🏷️ icon, child of Personal Buddy per Dave, `Brief review` status). Seeded with the DeWalt DCST925B buy ($129, Home Depot Capitol Expressway, 2026-10-10), the 14-pick dress-sneaker hunt (Cole Haan Topspin leading), and the Ace Combat 7 price watch ($14.99 alert, Mon/Thu). Open: which watches are active, groceries vs discretionary, off-limits categories.

## 2026-10-10 (Guardian Buddy: new buddy + dashboard entry)

### Added
- **Guardian Buddy** — new buddy: Dave's security and monetization watchdog for Money Buddy and the buddy system. Born from his question: "it's just raw HTML — what stops someone from downloading it and stealing my idea?" Full drill: [brief](https://docs.google.com/document/d/1sznSg7jSLRlDnAgFb-FaKnxp5lktWnFNQqK6DIEqF6E/edit), private repo [davedellaquila/guardian-buddy](https://github.com/davedellaquila/guardian-buddy), side thread, review ask. Dashboard entry (🛡️ icon, direct child of Project Buddy, `Brief review` status). Honest premise: you can't DRM HTML — the moat is the service, data, and brand, not the markup. Partners with Buddy Suite (monetization plan owner) and the Money Buddy thread. Open: server-side split before launch, trademark priorities, open-source vs proprietary, pricing hypothesis.

## 2026-10-10 (Rachel Buddy: new buddy + dashboard entry)

### Added
- **Rachel Buddy** — new person buddy for Rachel, Dave's dear friend of many years and owner of On the Road Again Classics (British classic car restoration, 16840 Joleen Way, Morgan Hill). Full drill: [brief](https://docs.google.com/document/d/14lpAtsdSvXMj6r29KVtEd3Rnqn1KZvoe_7zBwhgidb4/edit), private repo [davedellaquila/rachel-buddy](https://github.com/davedellaquila/rachel-buddy), side thread, review ask. Dashboard entry (🔧 icon, direct child of Project Buddy, `Brief review` status). Brief flags unknowns, not guesses: Rachel's last name, how they met, when she took over the shop, birthday/family details. Notable connections: Sawyer used to work at the shop; the shop cheered Quentin and Sawyer's MG GT at Monterey car week; Dave's 1959 MGA makes him a natural customer.

## 2026-10-10 (Little Guy Buddy: dashboard entry + custom homepage)

### Added
- **Little Guy Buddy** — dashboard entry (child of Family Buddy, `Brief review` status) plus a custom homepage (`little-guy-buddy/`): warm cat-themed living dossier with attention items (brief review, open questions, photo pending), fact cards (one of Dave's three cats; Marley (Mars) and Rocky as siblings; age, breed, which house, and vet history flagged as unknown, not guessed), empty-state vet-notes and reminders trackers, sibling/repo/brief pills, and a boop-the-snoot easter egg on the hero cat.

## 2026-10-10 (Clickable tiles, plans tiles, red trash icon, token gating)

### Added
- **Nancy Buddy homepage** — warm living-dossier theme (cream paper, terracotta accents) with attention list, "Who Nan is" fact cards, $1,200/mo grocery stipend panel (under review, linked to the tracker sheet), and interactive notes / reminders / important dates / gift-ideas boards (localStorage). Unknowns stay unknown — relationship to Dave remains unstated.
- **Clickable summary tiles** (Dave's idea) — clicking a tile filters the
  list below to matching items; clicking the active tile again clears the
  filter. Works on Projects (TO REVIEW / NEW / CLEARED), Changelog
  (change types), Business Plans (statuses), and Manifest (AUTOMATIC /
  PLANNED).
- **Business Plans tiles** (Dave's idea) — the Plans page now opens with
  per-status tiles (LIVE, ACTIVE, BRIEF REVIEW, EXPLORING, PLANNED, DRAFT).

### Changed
- **Red monochrome trash icon** (Dave's request) — photo delete and dump
  delete now use a low-fidelity red trash-can SVG; dump edit uses a
  matching monochrome pencil SVG (replacing the ✕/✏️/🗑️).
- **Edit/delete gated on GitHub token** (Dave's request) — photo delete and
  dump edit/delete icons are hidden when no GitHub token is saved.

## 2026-10-10 (Manifest tiles, homepage full-bleed, tile widths, grippers)

### Added
- **New-Project Manifest tiles** (Dave's idea) — the Manifest now opens
  with AUTOMATIC (8) and PLANNED (2) tiles, and every manifest row carries
  a colored pill (green Automatic, amber Planned) identifying its status.
- **Homepage navigation from the tree** (Dave's idea) — when the Project
  Homepage view is selected, clicking a buddy loads its homepage in the
  main view if it has one; buddies without a homepage leave the view
  untouched.

### Changed
- **Project Homepage is full-bleed** (Dave's idea) — the homepage iframe
  now fills the entire main view area with no margins; the header bar is
  replaced by a floating "Open in a new tab" pill button overlaid at the
  top.
- **Plans renamed to Business Plans** in the Views list (Dave's request).
- **Projects tiles constrained to content width** (Dave's request) — the
  TO REVIEW / NEW / CLEARED tiles now match the 860px buddy list below
  instead of spanning the full page width.

### Fixed
- **Resize grippers stay fixed** (Dave's request) — the left sidebar and
  right panel grippers now use sticky positioning so they stay vertically
  centered in the visible area while the panels scroll.

## 2026-10-10 (Tiles: attention on Projects, types on Changelog)

### Changed
- **Attention tiles moved to the Projects page** (Dave's idea) — the
  TO REVIEW / NEW / CLEARED tiles now sit atop the Projects view with
  global counts across all buddies, instead of the Project Homepage.
- **Changelog tiles show change types** (Dave's idea) — the Changelog now
  opens with one tile per change type present in the journal (NOTE EDITS,
  PHOTOS, MOVES, RENAMES, BRAND), each with its count, replacing the
  attention tiles there.

## 2026-10-10 (Panel persistence, project tiles)

### Fixed
- **Views-list selection is independent** — the highlighted view now only
  changes when the user picks a view (view-menu click or number-key
  shortcut). Buddy/plan selection and panel open/close never move it;
  tracked in a dedicated `S.view` instead of deriving it from `S.sel`.

### Fixed
- **View-menu clicks no longer dismiss the buddy panel** — picking any
  option in the top view menu (Tree, Projects, Plans, Manifest, Project,
  Changelog) now leaves the right-side detail panel exactly as it was.
  Panel visibility is controlled only by buddy selection (click/Escape/✕).
  The Project view renders into its own dedicated center container, so a
  homepage and an open panel coexist.
- **Narrow center after panel resize** — plan and buddy center views no
  longer inherit the resized panel's inline width.

### Added
- **Project stat tiles** — the Project view now opens with three tiles:
  TO REVIEW (unseen attention items), NEW (added in the last 7 days),
  CLEARED (reviewed & cleared), in the card style Dave picked. The data
  behind the tiles is a first guess and easy to rewire.

## 2026-10-10 (Repo renamed buddy-tree → buddy-system)

### Changed
- **Repo renamed** — `davedellaquila/buddy-tree` is now
  `davedellaquila/buddy-system`; the live dashboard moved to
  https://davedellaquila.github.io/buddy-system/ (the old URL 404s).
  Code, registry, and docs references updated.

## 2026-10-10 (Buddy homepages)

### Added
- **Buddy homepages** — any buddy can now carry a `homepage` (URL loaded in
  the center Project view), `homepageSource` (the canonical Muse URL, shown
  as an "Open on Muse ↗" link), and `homepageSynced` (mirror date). Buddies
  without a homepage keep the built-in detail page in the Project view.
- **Work Buddy homepage live** — the Project view for Work Buddy now loads
  its Muse-created homepage, mirrored into the repo at `work-buddy/` (the
  muse.ai page blocks third-party iframes, so the self-contained export is
  hosted on Pages and framed same-origin). The canonical
  https://muse.ai/s/work-buddy-hg5xrxhxqexi2xzxv stays one click away.

## 2026-10-10 (Factory reset: symmetric sidebars)

### Changed
- **Reset to Factory Defaults now restores symmetric sidebars** — both
  the left sidebar and the right buddy-detail panel return to the
  default 308px width.

## 2026-10-10 (Changelog row layout)

### Changed
- **Changelog rows stack title over detail** — the timestamp moved to the
  end of the title line (small, muted); the diff sits underneath, flush
  left with the title, full width. No more three-column jaggedness.

## 2026-10-10 (Theme setting)

### Fixed
- **Dark mode actually dark** — the theme's `:root` variables were circular
  self-references (`--bg:var(--bg)`), so dark mode rendered as light. `:root`
  now holds the real dark palette and the light overrides are complete.
  System setting is honored again.
- **Right panel width clamped** — the buddy detail panel can no longer be
  resized (or reset) to a huge width; max is 560px.
- **Buddy clicks open the right overlay panel** — clicking a buddy in the
  sidebar (or arrow-keying to one, or picking from search) now opens its
  details in the narrow right overlay panel, not the wide center view.
  The center view is for the main views; buddy details live on the right.
- **Projects-view chevrons** — chevrons now render only on rows that have
  children (no more dead chevrons on leaf rows), and clicking one reliably
  collapses/expands its section (toggle moved into the central click
  handler so row navigation can't swallow it).
- **Centered changelog** — the changelog content is now centered in the
  viewport (max-width 760px) instead of hugging the left edge.
- **Keyboard nav split** — arrow keys now move only through the buddy
  (project) rows: up/down steps through them, left jumps to the first,
  right to the last. The view buttons (Tree, Projects, Plans, Manifest,
  Changelog) are reached with number keys 1–9 instead of sharing the
  arrow-key list.
- **Theme picker moved to settings** — the Light/Dark/System switch now
  lives in the settings panel (where settings belong), not under the
  sidebar brand.
- **Settings panel upgrades** — footer buttons (Reset/Update/Done) are now
  sticky (always visible while the field list scrolls); the panel is
  draggable by its header and resizable from the bottom-right corner, with
  position and size persisted per device.

### Added
- **Light / Dark / System theme** — a three-way segmented picker under
  the sidebar brand. Persisted per device in localStorage (default:
  System). System follows the OS setting live via matchMedia, and a
  pre-paint script applies the theme before first render (no flash).
- **CSS-variable theming** — all 34 dashboard colors are now semantic
  variables (`:root` = dark, `html.light` = GitHub-light palette);
  every view (tree, projects, plans, manifest, buddy pages, changelog,
  sidebar, sheets, toasts) themes consistently. The old partial
  `prefers-color-scheme` media query was replaced.

## 2026-10-10 (Changelog restyle)

### Changed
- **Changelog view restyled as an activity feed** — entries are grouped
  by day under "Today" / "Yesterday" / month-day headers; each row has
  a type icon (notes, moves, renames), a bold headline, the old → new
  diff as a quiet truncated sub-line, and a small muted time-only stamp
  (full date on hover). Generous padding and dividers replace the
  cramped rows.

## 2026-10-10

### Added
- **Project view** — a fifth main view. Clicking any buddy in the left
  sidebar now selects it as the current project and shows its homepage in
  the center via the Project view (replaces the earlier direct
  buddy-center behavior, which is retired). The selected project's row
  stays highlighted in the sidebar. Keyboard shortcuts 1–6 follow the
  current view order.
- **Changelog view** — a sixth main view listing the full change history
  (the journal), newest first, each with old → new values.
- **Rearrangeable main views** — the gear/settings sheet has a "Main
  views" section; drag to reorder Tree, Projects, Plans, Manifest,
  Project, Changelog. Number-key shortcuts and arrow-key cycling follow
  the order.
- **Arrow keys cycle views and buddies** — with focus outside inputs,
  Up/Down move through view buttons then buddy rows as one sequence
  (last view ↓ → first buddy; first buddy ↑ → last view). Down-arrow
  inside the search box jumps to the first buddy in the filtered list.
- **What Changed shows old → new** — every journal entry displays its
  before → after values (buddy names resolved for moves, long notes
  truncated).

### Changed
- **Reviewed changes stay reviewed** — expanding "What changed?" marks
  entries seen; the sticky bar only reappears for new, unreviewed
  changes. Full history remains in the Changelog view.
- **Dismiss button** — the journal sticky bar's small ✕ is now a labeled
  "Dismiss" button on the right edge.
- **Right detail-panel resize +1px** — hit area 12→13px and gripper
  7→8px wide. (The left sidebar gripper was briefly widened to 10px by
  an automated commit; restored to its original 7px — only the right
  side was requested to grow.)

### Fixed
- **Settings panel was completely broken** — it threw on open
  (missing `SETTING_DEFS`/`getSetting`/`resetToFactory`/`updateFactory`,
  modal never appended to the document, Escape listener duplicated per
  open, `renderTree()` didn't exist). All repaired; Reset/Update Factory
  Defaults now snapshot and restore hideBuddyWord, field order/hidden,
  and view order.
- **Projects expand/collapse never rendered** — `renderProjects()` (with
  per-project › chevrons and persisted collapse state) only ran when the
  user had reparented buddies; the boot path restored static HTML
  without chevrons. The Projects view now always renders with working
  expand/collapse.

## 2026-10-09

### Fixed
- **Duplicate sidebar rows** — the nav's top-level filter included Project
  Buddy's direct children *and* the recursive render nested them under
  Project Buddy, so every direct child (and its subtree) appeared twice
  (e.g. searching "nan" showed Nancy and Finance twice). Top level now only
  lists parentless buddies; children render once, nested.
- **"What it does" → "About"** — the mission field's label renamed on the
  buddy page and in field settings.

### Added
- **Sidebar opens buddies in the center** — clicking a buddy in the left
  sidebar (or arrow-keying through the list) now shows that buddy's
  homepage in the central view instead of a right-side overlay. Clicks
  from the tree, Projects list, and other in-content links still open the
  overlay peek panel; Prev/Next and breadcrumb links follow whichever
  presentation is active. The panel resize handle is hidden in center
  mode.
- **Repo slug eyebrow** — the small label above the buddy name on the
  detail page now shows the buddy's true Git repo slug from the registry
  (e.g. `buddy-tree`), in monospace with a tooltip naming the full
  `davedellaquila/<repo>` path. Buddies with no repo linked honestly show
  "no repo linked" instead of a name-derived guess. (Previously it showed
  the display name, which reads as "Project" with the Hide-"Buddy" setting
  on.)
- **Per-dump actions** — every ingest dump tile now has edit (✏️) and
  delete (🗑️) buttons in its upper-right corner (trash on the far right,
  pencil to its left). Edit opens the full text inline and auto-saves as
  you type (debounced, with a Saving…/Saved status line — same treatment
  as shared notes); delete asks for confirmation. Both work against the
  buddy repo's `docs/ingest.md` and the localStorage fallback, preserving
  timestamps and the file header.
- **No more phantom highlighting** — text selection disabled on the chart
  tiles (was leaving blue selection blocks when panning/zooming).
- **Sidebar buddy search** — filter the buddy list by keywords (AND match
  on name + tagline); press `/` to jump to the search box.
- **Global token pill** — GitHub token status lives in a fixed top-right pill
  (amber 'Token needed' / green 'GitHub check'), not buried per-buddy; saving
  shows a green checkmark confirmation.
- **Zoom presets** — keys `1`–`9` jump to 10%–90% zoom, `0` is 100%.
- **Edge-to-edge chart** — the chart viewport now fills the usable area
  with no surrounding margins; the border sits at the edges.
- **Token gating** — shared notes, ingest, and photo upload are now
  disabled until a GitHub token is saved; a prominent amber banner on every
  buddy page pushes for the token.
- **Zoom keyboard shortcuts** — `+`/`=` zoom in, `-`/`_` zoom out,
  `0` resets to 100%.
- **Zoom slider floats over the chart** — moved from the margin into the
  chart area itself, map-control style. (`94948af`)
- **Chart viewport polish** — visible border around the chart viewport so its
  edges are clear; the viewport now fills the available page height instead
  of clipping. (`f6aa25c`)
- **Responsive layouts** — three breakpoints: small (<640px) stacks tiles as
  full-width cards with a drawer sidebar (hamburger) and detail as a bottom
  sheet; medium (640–1100px) has a collapsible sidebar, horizontal segmented
  view control, and detail as a right-docked side sheet; large (>1100px) is
  tri-pane with a persistent detail panel. **⛶ Fit button** next to the zoom
  slider zooms to fit content. Tile child counts. Keyboard navigation
  (arrows move between buddies, Esc closes detail). (`d606e04`)
- **Standalone buddy mode** — hash deep-links (`#/buddy:<id>`, `#/view:tree`,
  `#/plan:<id>`) with working back/forward; chromeless standalone view
  (`#/buddy:<id>/standalone`) hiding the sidebar; **💾 Save to desktop**
  button on every buddy page downloading a `.webloc` (Mac) / `.url`
  (Windows) launcher that opens the buddy by itself. (`d406f51`)
- **Gripper handles (⠿)** on every tree tile — drag a buddy onto another to
  reparent it; loop protection included. (`8bdbdea`)
- **Orphaned buddies section** — parentless buddies render in their own tree
  section with grippers instead of being invisible. (`8bdbdea`)
- **Ingest box** on every buddy page — brain-dump raw thoughts; each dump
  appends a timestamped entry to the buddy's repo `docs/ingest.md`
  (device-local fallback). (`79e4ae2`)
- **Sharing Buddy** — new buddy (brief, repo, thread, registry entry)
  exploring per-buddy share links, access levels, and privacy. (`4f19bc2`)
- **FEATURES.md** — living feature registry in the repo root. (`d1f4ea2`)
- **README + docs/brief.md sweep** — 25 buddy repos stamped with a README
  (name, mission, brief links) and `docs/brief.md` (full brief text); the
  new-project drill now does this automatically for every new repo, along
  with an empty `docs/ingest.md`.
- **Dream Buddy repo link** — wired `davedellaquila/dream-buddy` into the
  dashboard registry. (`86c3c5e`)

### Fixed
- **Grab-to-pan** — the chart pan was half-built (scrolled a non-scrollable
  element and the whole page). Rewrote it: the tree is now a real scroll
  viewport with grab/grabbing cursors, a 5px click threshold, and
  click-suppression after drags. (`6776cd1`)
- **Shared notes without a token** — the field is now disabled with an amber
  warning instead of silently failing. (`7839093`)

### Changed
- **Tree chart is a scroll viewport** (part of the pan fix) — bounded height,
  pans in any direction once content overflows.

## Earlier 2026-10-09

- Buddy pages: resizable sidebar (220–560 px, remembered), Prev/Next/Back
  navigation, change journal with one-shot revert, photo dropzone with
  in-browser HEIC→JPEG conversion and repo push, shared repo notes.
  (`cf67d52`)
- Vertical zoom slider, timestamp build numbers on buddy and plan pages,
  back-to-buddies link. (`f2a33d7`)
- Tree nodes and Projects rows as drag-drop reparenting targets. (`7898c0d`)
- Click-to-rename app name, Shift+scroll zoom. (`d8aa179`)
- MGA + ML500 buddy records, zoom slider scaffolding, photo galleries.
  (`b1a7606`)
- App rename to Buddies, per-buddy icons, sidebar drag-to-reparent,
  Business Plans view. (`04d8bda`)

## 2026-10-13
- Fixed: removed a stale Oct 11 duplicate `bp-homepage-open` handler that revived on rebuild and broke page JS (blank dashboard). One Open handler remains: opens the buddy's homepage URL in a new tab.

## 2026-10-13
- Org fix (Johnny's verdict): Family Buddy is now a top-level root (the Family org head); The Dell'Aquilas nests under it. The reparent had merged in the wrong direction — people belong to domains, never the reverse.

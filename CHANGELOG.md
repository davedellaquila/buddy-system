# Changelog

All notable changes to the Buddies dashboard and buddy system. Newest first.
`FEATURES.md` describes the current state; this file describes how it got there.

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

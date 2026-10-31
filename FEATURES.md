# Buddies Dashboard — Feature Registry

Living list of every feature in the dashboard. Update this file when a feature
ships or changes — it's the source of truth for future documentation.

Repo: https://github.com/davedellaquila/buddy-system
Live: https://davedellaquila.github.io/buddy-system/
Build: `build.py` generates `index.html` from `buddies.json` + `plans.json`.

---

## Aliases (AKA)

- **`aka[]`** — every buddy can carry a list of aliases. Both search boxes match them, and they render in italics under the buddy's name on the detail panel. Tell Astro to add/remove AKAs for any buddy.

## Tree chart

- **Classic tree layout** — the canonical design. (A card-based redesign was
  tried and reverted; preserved on branch `card-tree-redesign` for reference.)
- **Split panes** — the tree view is two stacked panes with a draggable
  splitter: the buddy tree on top, orphaned buddies below. Each pane has its
  own zoom slider + zoom-to-fit; split position and both zooms persist per
  device. Dragging an orphan tile onto a tree buddy reparents it.
- **Zoom slider** — compact horizontal control (small▪ · range · large◼ + fit),
  50–160%; Shift+scroll over a pane zooms that pane. Zoom scales only the
  chart — the Quick answers row and the Atlas lens pill stay fixed above it.
- **Shift+scroll zoom** — hold Shift and scroll over a tree pane to zoom it.
- **Grab-to-pan** — click-drag the chart to slide it around; grab/grabbing
  cursors; small movements still count as clicks; the stray click after a
  drag is swallowed so you don't navigate by accident.
- **Drag-to-reparent on tiles** — press-and-hold a tree tile (~400ms, accent
  ring shows when armed), then drag it onto another buddy to reparent it.
  Pointer-based (mouse + touch), so it works on iPhone/iPad where HTML5
  drag-and-drop never fires. A quick tap still opens the buddy's detail panel
  (drag vs. tap distinguished by the hold delay + a 6px movement threshold);
  the stray click after a drag is swallowed. Loop protection:
  can't drop a parent onto its own descendant (invalid targets get a red
  dashed outline). Root can't be dragged; dropping onto root makes a buddy
  top-level. Every move shows an Undo toast (~6s) — tap it to restore the
  previous parent.
- **Ledger drag grippers** — every Ledger row (except the root) has a quiet
  dot-grid gripper (Jonny's language). Grab it and drop onto another row to
  make that buddy the parent. The gripper arms immediately (explicit drag
  affordance, no press-and-hold); same cycle protection, ghost label, drop
  highlighting, and ~6s undo toast as tile drag.
- **Orphaned buddies section** — buddies with no parent render in their own
  pane, instead of being invisible.
- **Drop targets** — tree nodes and Projects rows accept drops from the
  sidebar and from tile drags to assign/change parents.
- **Quick Answers bar** — up to 12 pending attention items as tappable chips
  above the tree; tap to jump to that buddy's question. One horizontally
  scrolling row, so it never crowds the chart.
- **Done affordance (Jonny)** — info-panel attention items use the empty
  circle as the checkbox: tap → accent fill + white check (~200ms) → tile
  glides out → "Marked done. Undo." toast for 6s. Done items leave the list;
  the timestamp is recorded. Same circle on Astro's homepage (replacing the
  "✓ Done" button); "Need more info" stays a quiet link. `role="checkbox"`
  with keyboard support.
- **Voice setting** — per-buddy spoken voice: searchable picker with 1,066
  TTS voices (extensible via voice-catalog.json), "Voice notes in threads"
  toggle defaulting to off (Dave's token-concern call), preview samples for
  30 curated voices. Persists to buddies.json.
- **Persona audio previews** — the Persona panel shows the selected persona's
  voice-sample quote with a "Hear it" button (87 personas have audio); the
  collapsed header reads "PERSONA: [name]".
- **Collapse pills** — parent tiles carry a ⌄/› pill with their descendant
  count; tap to collapse/expand the whole subtree. State persists.
- **Hairline connectors** — 1px tree lines with 8px elbow radius; 20px
  generational gaps. The composition centers vertically in the pane whenever
  it fits, instead of anchoring to the top.

## Appearance

- **Light / Dark / System theme** — segmented picker under the sidebar
  brand; per-device localStorage (default System, follows the OS live).
- **Text size slider** — Settings → Advanced; scales text and UI throughout
  the app from 80% to 130% (default 100%), with live preview as you drag.
  Like the text-size slider on iPhone and Watch.
- **Framework buttons** — the shell buttons (New, Back, Info) wear
  nearly see-through glass (16–20% fills over a blur, both themes; the
  panel's close ×, the Info button's twin, matches). The Settings toggle
  **Group framework buttons in the footer** (default on) seats New and
  Back along the bottom of the screen at the corners. Info is not in
  the group (Dave's ruling, 2026-10-28): it stays in the top-right
  corner at every width and setting, swapping pixel-for-pixel with the
  panel's close ×. On phone widths the buttons keep their corner spots
  either way. (Recents was the fourth button until
  2026-10-28; it lives in the buddy panel now — header tools, left of
  the gear, and 2nd in the collapsed rail — and its menu always fits the
  visible viewport, scrolling internally rather than running off the
  bottom.)
- **Google Doc links open in a new tab** — every docs.google.com /
  drive.google.com link on buddy homepages and About pages carries
  target="_blank": a Doc loaded inside the dashboard's homepage frame
  hits Google's cookie wall and can't open, so Docs always open in their
  own browser tab. (Dashboard-panel document links already did this.)
- **Develop section** — Settings → Develop; pre-launch tools for readying the
  app for new users. **Simulate new user** empties the data file in-memory so
  you can preview the fresh-link experience; real data is stashed and restored
  on toggle-off or page reload, with a persistent banner while active. Also
  shows the build number and offers **Clear this device's local data**.

## Agent standing orders

- **`AGENTS.md`** — critical rules agents read on start (INIT / first
  homepage pass). Currently: every buddy website must ship dark mode.
- **`docs/standing-orders.md`** — durable memo log (newest first).
- **Dashboard broadcast** — each buddy detail panel shows active standing
  orders (amber banner) so existing agents see them when the panel opens;
  also surfaced on Project Buddy / Scaffold / Astro homepages.

## Sidebar

- **Main views** — Tree, Projects, Business Plans, Manifest, Project,
  Changelog; order is user-rearrangeable in settings (gear icon) and is the single source of truth — the sidebar sections and the collapsed rail's current-view popover both render in that order (within their Views / Collections grouping). Number
  keys 1–6 select views in that order; Up/Down arrow through views then
  buddies.
- **Org Chart view zoom** — the Org Chart opens fitted to the whole staff (on a phone-width viewport the fit fills the height instead and the width pans, with a compact title + one-line header that clears the rail cluster; Dave 2026-10-30);
  a cluster that starts at the top-right of the chart viewport zooms −/+
  (×1.25), Fit, and 100% with a live % readout. Its dot gripper drags the
  cluster anywhere inside the viewport (clamped fully inside; position
  persists per device; double-click the grip to reset) — it never moves on
  its own. Shift+scroll and pinch zoom on the pointer, background drags
  pan, + / − / 0 work on the keyboard while the view is active, and
  zoom/pan persist per device (10–300%).
- **Views surface** — the sidebar's Views section (and the rail's
  view-picker popover) sit on solid `--hover`, one surface step off the
  buddy list's `--panel`, in both themes. Views and the Tip Jar form the
  sidebar's pinned footer — anchored to the panel's bottom in every
  collapse state while the sections above scroll in their own region;
  resizing Views is absorbed by that scroll region, never by the Tip Jar. Collections carries the same drag-resize strip above its header (Dave 2026-10-29 — it originally shipped with no handle), its height persisted per device. Both drags start from the section's rendered height, so a stored cap left over from a taller-content era never leaves a dead zone (Dave's dead-grip fix, 2026-10-30). Section headers are tap targets first: on touch devices they are not HTML5-draggable (drag-reorder arms only with a fine pointer), suppress the touch callout/selection, and the resize strips' invisible hit zone reaches only 3px above the strip so it can never sit over a neighboring header (Dave's untappable-Buddies-header fix, 2026-10-30).
  The panel's navigation splits in two (Dave 2026-10-28): **Views**
  (Homepage, Atlas, Org Chart, Projects, Manifest, Change Log, Release
  Notes) and a separate **Collections** section (Favorites, Flagged,
  Business Plans — gathered sets of specific objects, not ways of looking
  at the tree), each collapsible and grip-reorderable within its own group;
  the rail's view popover groups its list under the
  same two headings. Picking a buddy from the Recents popover only selects
  it — an open info panel follows the selection; a closed one stays closed
  until opened. The buddy panel's list is two tabs (Dave 2026-10-28):
  **Buddies** (the hierarchy) and **Recents** — every buddy visit on
  record, most recent first, as flat rows with the tree rows' behavior;
  the visit record keeps the last 200 visits, and the search field filters
  whichever tab is showing.
- **Escape closes the panels** — ESC dismisses transient UI first
  (popovers, menus, the field-settings sheet — one per press), then closes
  the info panel and the buddy panel together, from any focus location,
  including the search box.
- **Collapsed rail fits its icons** — the icon rail's height shrink-wraps
  its contents: exactly five controls, top to bottom — the expand
  chevron, Recents (the same recent-buddies popover the panel header's
  Recents button opens), Settings, Find, then the rail's single divider,
  then the current-view icon (a view picker; its popover's Collections
  group is where Business Plans lives — the rail's own 💼 shortcut was
  retired as redundant, Dave 2026-10-28). (Dave's reorder, 2026-10-28: in the expanded
  panel's header tools the order is Settings, Recents, collapse chevron.)
  Every icon visible, no trailing void below the
  last one. On a viewport too short for the stack, the rail caps at the
  viewport height and scrolls internally. Expanding the rail glides on
  the same width/transform transition as collapsing, in reverse: the
  panel rises and widens out of the rail's footprint.
- **Keyboard selection never closes the panel** — arrow keys and Tab move
  the buddy selection without triggering the sidebar's
  auto-close-on-select; only ESC closes panels. Click selection keeps the
  auto-close behavior.
- **Settings close is a bare ×** — the Settings sheet's close control
  carries no ring or border in any state. The header tools keep their
  circled buttons; the header close ×'s ring is painted as border + inset
  shadow so it always renders complete.
- **Collapsible sections** — Views, Buddies, and Business Plans headers
  collapse their sections on click; state persists per device.
- **Collapsible buddy rows** — buddies with children carry a chevron; click
  toggles just that row, Shift+click collapses/expands the whole subtree.
  State persists per device.
- **Profile hero** — every buddy's info panel opens with a profile
  header in the Muse profile-card treatment: a large centered circular
  avatar (the buddy's uploaded image when it has one, its emoji large
  otherwise) with a pencil badge overlapping its bottom-right edge, the
  buddy's name in large type under it, and a centered status line —
  the registry status with a colored dot, plus a "⚑ N need attention"
  flag when attention items are waiting. The pencil badge scrolls to
  and focuses the panel's rename input; the avatar opens the avatar
  picker. The hero scrolls away with the content; the compact sticky
  identity bar above it is unchanged.
- **Persona picker** — every buddy's info panel shows its current persona
  (name + voice blurb) with "Change persona" (searchable picker over the
  full 116-entry roster) and "🎲 Surprise me" (random pick). Persists to
  `buddies.json` via the GitHub token; works for Astro too.
- **Project view** — shows the current project's homepage full-bleed in the
  main view area (no margins); a floating "Open in a new tab" pill button
  overlays the top. Clicking a sidebar buddy loads its homepage if it has
  one, and leaves the view untouched if it doesn't. Buddies without a
  homepage show a "No homepage for this project" empty state. Picking a
  view-menu option never dismisses the right-side buddy panel.
- **Projects view** — hierarchical outline of every buddy with its status;
  opens with global attention tiles (TO REVIEW / NEW / CLEARED across all
  buddies), constrained to the same 860px width as the list below. The list
  views (Projects, Business Plans, Manifest, Changelog) keep the tree
  chrome's sidebar clearance in floating panel style (348px, 76px when the
  sidebar is collapsed to its rail), so row controls never sit under the
  floating sidebar.
  Clicking a tile filters the list to matching buddies; clicking again
  clears. Clicking a row toggles its section and loads the buddy in the
  right-side panel.
- **Business Plans view** — opens with per-status tiles (LIVE, ACTIVE,
  BRIEF REVIEW, EXPLORING, PLANNED, DRAFT); clicking a tile filters the
  plans below.
- **Changelog view** — opens with per-change-type tiles; clicking a tile
  filters the entries below.
- **Manifest view** — the new-project drill as rows, each badged with a
  colored pill (Automatic / Planned); opens with AUTOMATIC (8) and
  PLANNED (2) summary tiles.
- **Horizontally resizable** — drag the edge, 220–560 px, width remembered
  per device.
- **Grippers are dots only (Dave, 2026-10-21)** — every gripper on the
  dashboard (panel + sidebar resize edges, floated-panel move grips and edge
  clusters, the sidebar drawer pull, the settings-sheet grip, the Views
  resize handle, the Org Chart zoom grip, Ledger and view drag grips) is nothing but dots:
  ~3px dots on a 7px pitch, 2 columns wide by however many rows the grip
  length calls for (transposed for horizontal grips), with NO background,
  plate, or seam in any state — rest, hover, and dragging differ only in dot
  colour (text2 78% mix at rest, full text2 on hover, accent while
  dragging). Hit areas and cursors are unchanged.
- **Drag-to-reparent** — drag any sidebar buddy onto a tree node or
  Projects row to change its parent.
- **App name** — the top-left "Buddies" label is inline-editable,
  device-persisted, and updates the browser title.

## Buddy detail pages

- **Homepage + About page (Dave, 2026-10-20)** — every buddy has two pages:
  its homepage (`<id>/`, the custom design when one exists) and its About
  page (`<id>/about.html`), which is the Default Homepage (the Dossier)
  served as the full record. Homepages link to About (custom pages in their
  header/footer; template pages in the footer). The About page carries
  everything: the complete registry record (every field, unset shown as
  not set) plus a "From the repo" section — an inventory of the buddy's
  repo markdown with the live, token-gated 📄 Repo files reader, so repo
  content is read from GitHub on the device and never published raw.
  Generated by `gen_default_homepages.py --about` (v3.2).
- **Tip Jar on every buddy page (Dave, 2026-10-24; fleet rollout
  2026-10-27)** — every buddy homepage and About page carries the canonical
  Tip Jar pill (motion v2: breathing + shimmer + hover spin), linking
  Dave's Ko-fi (https://ko-fi.com/davedellaquila). The single canonical
  copy lives at `docs/tipjar-snippet.html`; both homepage generators
  (`gen_basic_homepages.py`, `gen_default_homepages.py`) read it live at
  generation time and embed it before `</body>`, so regenerated pages
  keep the jar instead of drifting. Inside the dashboard, the shell keeps
  the pill clear of the floating + button: when a homepage frame reaches
  the window's bottom-right corner, the jar stacks just above the button
  (bottom:88px) instead of sliding under it; standalone pages keep the
  canonical corner position.
- **Hear my role (Dave, 2026-10-24)** — a buddy homepage carries a 🔊
  "Hear my role" audio control: the buddy reads the first paragraph of
  its job req's Role summary aloud in its own voice. The recording
  (`role-intro.mp3`) is hosted beside the homepage and referenced
  relatively.
- **Full-bleed homepage (Dave, 2026-10-30)** — a framed buddy page runs
  the full window width and height: no left clearance for the collapsed
  rail, no bottom band for the footer discs. Every disc floats over the
  page as a bare glass overlay, and only the discs themselves capture
  taps — the page stays scrollable and tappable right up to the left and
  bottom edges. The open panel drawer keeps its own clearances.
- **Navigation** — Back, Prev, Next, and All buddies.
- **Draggable sections** — no visible gripper (Dave, 2026-10-21): drag a
  section by its name text to reorder it directly on the panel — the name
  alone is the grab zone (grab cursor over the name only); pressing
  anywhere else on the header never starts a drag. A plain click still
  collapses/expands, and the Settings sheet's Buddy fields section spells
  the tip out. Order persists per device via `fieldOrder` (also editable
  in field settings).
- **Sticky section headers** — as the buddy panel scrolls, each section
  header sticks just under the sticky identity head and holds there while
  its section scrolls beneath it, until the next section's header pushes
  it off — the classic list behavior. The stick line is measured from the
  rendered head on every render and resize, so it stays flush in the
  desktop panel, the iPad sheet, and the phone takeover layouts.
- **Tooltips** — ⓘ icons show hover popovers on mouse, tap-to-pin popovers
  with an × close button on touch; tap-outside and Escape dismiss.
- **Build numbers** — every buddy and business-plan page shows a timestamp
  build number.
- **Click-to-rename** — buddy names are inline editable.
- **Private notes** — device-local freeform notes (localStorage).
- **Shared notes** — sync to the buddy's repo at `docs/notes.md` via the
  GitHub Contents API (needs a token; falls back to device-local).
- **Ingest box** — brain-dump raw thoughts about the buddy; each dump is
  appended as a timestamped entry to the buddy's repo `docs/ingest.md`.
  On template homepages, the "Connect GitHub" token card inside the brain
  dump wears a solid amber border + amber wash (Jonny, 2026-10-19) so the
  one step that unlocks repo sync can't be skimmed past.
  Raw material for later dossier work. Dumps live in a collapsible
  "Dumps (n)" section (collapsed by default, state remembered per buddy);
  each dump tile has edit (✏️) and delete (🗑️) buttons in its upper-right
  corner.
- **Rail icon family** — the collapsed rail's four slots (expand, Recents,
  current-view, Dump) share one glass disc and one line-icon weight
  everywhere the rail renders, anchored included (Dave, 2026-10-30). The
  discs float bare — no container card, border, or divider in either
  panel style — in one top cluster spaced like the footer cluster (12px).
- **Buddy list scroll memory** — the buddy list keeps its exact scroll
  position when you select a buddy, across list re-renders and across
  closing and reopening the panel/drawer: the list's scroller is
  watched into the persistent scroll-position store, re-renders
  restore the position they started with, and reopening restores the
  stored one (Dave bug fix, 2026-10-30).
- **Universal Dump button** — a 📥 disc on the collapsed rail (below the
  current-view icon, phone and desktop) opens a capture box that routes to
  the TOP LEVEL: entries append to Astro's ingest
  (buddy-system/docs/ingest.md) through the same token-gated write path as
  the homepage dump boxes — no token or a failed write queues the dump on
  the device (buddyTree.dumpQueue) and flushes it on the next successful
  dump or at boot; nothing is ever silently dropped. Shift+Return (or
  ⌘/Ctrl+Return) in the text field submits, exactly like the Dump it
  button; a plain Return just inserts a newline. A dump is optional
  text plus optional files (1 MB per file — the Contents API ceiling,
  enforced at pick time with the reason shown): files upload to
  buddy-system/docs/ingest-files/<one folder per dump>/ and the entry
  lists each with its GitHub link (Dave, 2026-10-30). The card is
  390px wide (was 330px; still capped at the viewport width minus a
  small margin, Dave, 2026-10-30).
- **Dump anywhere, it's routed** — the system's core capture promise: type a
  stream-of-consciousness thought into any buddy's homepage dump box or any
  thread, and it lands in a durable inbox (`docs/ingest.md`) and gets routed
  to the buddy it actually belongs to. Dave never has to decide where a
  thought goes — capture is universal, routing is the staff's job.
- **Add child / sibling from the panel** — the Parent section header has a
  "+ Sibling" button, the Direct reports header has "+ Child". A dialog takes
  the new buddy's name, icon, and type, then writes the entry straight to
  `buddies.json` on GitHub (needs the GitHub token). New buddies are flagged
  `setup_pending` with an attention item so Astro runs the full onboarding.
- **San Jose Gazette Buddy** (2026-10-30) — 🗞️ child of Neighborhood
  Buddy and editor of The San Jose Gazette, Dave's public hyperlocal
  daily for San Jose & the Santa Clara Valley: three editions a day
  plus an hourly safety poll (AlertSCC / city alerts / CHP / VTA / NWS
  Bay Area), sourcing its own public events — a fully separate
  newsroom from its Fiddletown sister paper. Registry-wired with its
  side-thread chat, a provisional voice, the job req doc (also linked
  from Neighborhood Buddy's record), a generated homepage + About
  page, and role audio beside the homepage.
- **Gazette Buddy** (2026-10-30) — 🗞️ child of Neighborhood Buddy and
  editor of The Fiddletown Gazette, Dave's public hyperlocal daily for
  Fiddletown & the Shenandoah Valley: three editions a day plus an hourly
  safety poll with out-of-cycle banners (Safety Wire / Lead / Today in
  the Valley / Week Ahead / Around Town / Community Wire / Weather),
  public sources and events only. Registry-wired with its side-thread
  chat, a provisional voice, the job req doc (also linked from
  Neighborhood Buddy's record), a generated homepage + About page, and
  role audio beside the homepage.
- **Route Buddy** (2026-10-30) — 🗺️ child of Sports Car Adventures, the
  route librarian: the route library (cataloged routes, master GPX,
  14-attribute records, Dave's notes) behind a US-map homepage, and the
  working home of the Milemarker concept. Registry-wired with its
  side-thread chat, a provisional voice, the job req + design brief docs
  (the job req also linked from Sports Car Adventures' record), a
  generated homepage + About page, and role audio beside the homepage.
- **Road Trip Buddy** (2026-10-30) — 🛣️ child of Travel Buddy keeping the
  Road Trip Register: great roads + worthy stops, seeded with the Million
  Dollar Highway + Ouray cluster and Three Rivers/Gateway. Registry-wired
  with its side-thread chat, a provisional voice, the job-req doc (also
  linked from Travel Buddy's record), a generated homepage + About page,
  and its role audio hosted beside the homepage.
- **Parent one-liner** — the Parent section shows just "Name (kind)" as a
  clickable link instead of a tile; tapping it opens the parent's panel. The
  Change button stays in the section header.
- **Buddy links (many-to-many)** — buddies link to each other, Rae Assist
  style: everything can be linked to everything. A `links` array on a
  registry entry names linked buddy ids; the dashboard renders a "Linked
  buddies" section on each buddy's detail card, and reverse links are
  computed automatically — link once, it shows on both cards. Links to
  buddies that don't exist yet render as "Buddy being set up" and light up
  when the buddy is created. Custom homepages carry their own Connections
  section (first live link: Joel's Buddy ↔ James's Buddy).
- **Buddy avatars** — every buddy can have an image, not just an emoji:
  upload from the avatar picker (downscaled, stored in the dashboard repo
  at `avatars/<buddy-id>.jpg`, shown on the card, homepage, and favicon;
  removable). Tapping the avatar on a buddy's card *or* homepage opens a
  categorized emoji picker (~200 emojis across 8 categories, plus
  paste-any-emoji); homepage picks share the dashboard's override store,
  so they stay in sync on the same device.
- **Per-buddy favicon** — opening a buddy's card or homepage sets the
  page's favicon (and Apple touch icon) from the buddy's image, or renders
  the buddy's emoji to a PNG when there's no image. Save the page to the
  desktop or Dock and it carries the buddy's face.
- **Token gating** — photos, shared notes, and ingest are locked until a
  GitHub token is saved; an amber banner at the top of every buddy page
  prompts for it.
- **Photo strip** — photos from `photos/<buddy-id>/` in the dashboard repo;
  drag/drop upload area; HEIC files are converted to JPEG in-browser
  (`heic2any`); uploads push to the repo via the GitHub API.
- **💾 Save to desktop** — downloads a launcher file (`.webloc` on Mac,
  `.url` on Windows) that opens the buddy in standalone mode.

## Standalone mode

- **Hash deep-links** — `#/buddy:<id>`, `#/view:tree`, `#/plan:<id>`;
  back/forward buttons work.
- **Chromeless standalone view** — `#/buddy:<id>/standalone` hides the
  sidebar and shows just the buddy page, with a small "open full
  dashboard" bar. Feels like its own little app.

## Change journal

- Tracks buddy renames, note edits, hierarchy moves, and app-name changes.
- Shows `Revert (N)`, "What changed?", and a labeled Dismiss button;
  persists across reloads via localStorage. Revert asks first: a
  confirmation dialog lists every logged change (old → new, with times)
  and only its red Revert button proceeds — Cancel, Escape, or a
  backdrop tap leaves the journal untouched.
- "What changed?" lists each entry with old → new values; expanding it
  marks entries reviewed so the sticky bar only returns for new changes.
- The **Changelog** main view keeps the full history permanently, opening
  with one summary tile per change type present (note edits, photos,
  moves, renames, brand), each with its count.

## GitHub integration

- Token stored in localStorage (`S.ghToken`); used for photo uploads,
  shared notes, and ingest sync.
- Photo uploads target the public `buddy-tree` repo; shared notes and
  ingest target each buddy's own (usually private) repo.

## Repo automation (project-buddy drill)

- Every new buddy repo is stamped with `README.md` (name, mission,
  brief links) and `docs/brief.md` (full brief text), plus an empty
  `docs/ingest.md` log — committed and pushed automatically.

---

## Responsive design

- **Fit button (⛶)** next to the zoom slider — zooms to fit the chart content.
- **Small (<640px) — iPhone Pass v2 (Jonny critique, 2026-10-22)**: tiles
  stack as full-width cards; the Tree view keeps the org chart (pan with a
  finger, floating zoom slider) instead of a card list. Panels are
  slide-over **docks**: the buddy list lives under the canvas's left edge
  (85vw, max 320px) and the detail panel under its right edge (88vw, max
  360px); the canvas slides over them (280ms), one dock at a time, and the
  exposed dimmed sliver of canvas taps shut. The resting state is the
  **six-icon rail** — the same controls as the desktop's collapsed rail
  (Dave's call, 2026-10-28, superseding the 2026-10-22 recents icon
  strip, whose renderer stays in the tree dormant): › expand (opens the
  full dock — the old grid door's job), 🕘 Recents (the popover),
  ⚙ Settings, 🔍 Find, then a divider, then the current-view icon
  (views popover) alone — in the
  rail's two sections (4 + 1) inside the 66px
  dock, grouped in one cluster and vertically centered, exactly as the
  desktop rail groups them in its floating card (nothing foot-pinned;
  the footer belongs to the bottom glass cluster alone). The dock's
  background is a floating card too - it hugs the cluster (full border,
  rounded, translucent, shadowed) rather than running the view's full
  height. Recent buddies
  live one tap away in the Recents popover; the strip's current-buddy
  accent marking has no rail equivalent. The View control carries a
  **caret (▾)** at every size — it is a menu, and the caret rotates while
  its menu is open. **Find** (center button in the bottom cluster — the cluster's discs are 44px, the same diameter as the rail discs (Dave, 2026-10-30) — Prev / Find / Next, Dave 2026-10-30) opens a
  sticky search bar at the top of the screen: empty it lists Recents,
  typing switches to auto-suggest with the sidebar search's matcher and
  matched characters in bold; picking a result lands on that buddy's
  homepage with the docks closed. A fresh load or deep link at phone
  widths restores the selection but never an open panel (**closed on
  open**). The old drawer, the portrait full-screen takeover, and the
  floating-card sheet are retired. The phone strip element never renders
  at any width now (base hide rule; no show rule remains).
- **First open (fresh context, phone)**: with no stored state on the
  device, the dashboard opens as a front door — the resting geometry is
  invariant at first paint (66px rail + canvas, never dock width), the
  canvas lands on Astro's homepage without recording a visit, and a
  one-time **Welcome Card** (dismissed per device, stored in its own
  `buddyWelcome.system` key) names the place, states the scale, and
  teaches the doors in one sentence. The resting rail is state-free —
  the same six controls regardless of history; no fake recency.
- **The Lift**: while typing on the phone (keyboard open), the Prev/Next
  pill rides above the keyboard via a `--kb-lift` offset driven by focus
  and `visualViewport`, and settles back when the keyboard closes.
- **Disc clearance**: the floating homepage-nav discs (Prev/Find/Next
  centered, Back bottom-left) never cover hosted chrome: when a
  homepage/app is in the frame, the frame wrap reserves the discs' 96px
  footprint at its bottom so the hosted page's own bottom bars reflow
  above the discs, and at sidebar-open widths the sidebar reserves the
  same band at its own bottom (padding on the sidebar itself), so the
  whole column - list, Views, Tip Jar - packs above the Back disc with
  no gap opened mid-column.
- **Medium (640–1100px)**: collapsible sidebar; view nav becomes a horizontal
  segmented control; detail opens as a right-docked side sheet (380px).
- **Large (>1100px)**: tri-pane with persistent detail panel (400px).
- **Keyboard**: arrows move between buddies, Esc closes the detail panel.
  **⌘F / Ctrl+F** opens the Find overlay — one card centred on the window,
  floating in the upper third over a full scrim (bar, results, and a hint
  footer in a single card; placement invariant across sidebar/panel
  states; a bordered circle × at the end of its bar dismisses it — the
  smaller ghost × beside it only clears the typed text); **/** opens the buddy
  panel when needed and focuses its search field; **⌘I** toggles the info
  panel — collapse/expand, or open it when no buddy panel is up. The toggle is exact: collapsed truly hides the panel, and a fast second ⌘I during the fold animation still counts. All work
  even when a buddy homepage iframe has focus (the iframe forwards the
  chords to the parent chrome).
- **Panel search**: the buddy/info panel carries its own search field at
  the top (panel/sheet modes). It mirrors the sidebar search — one shared
  matcher over name + tagline + A.K.A. filters the buddy list as you
  type, the two boxes stay in sync, Enter opens the top match in the
  panel, and Escape clears the query before it ever closes the panel.
  The Find overlay also lives on the footer Find button and on ⌘F / Ctrl+F.
- **Dashboard link on every homepage**: every buddy homepage links back
  to the Buddy System dashboard (`bs-dash-link`, in its sticky header or
  top nav), and both homepage generators emit the link natively.

## Known limitations / follow-ups

- Photo "all image types" claim is aspirational: HEIC is converted and
  JPEG/PNG/GIF/WebP work, but other formats are merely renamed to `.jpg`.
- Shared-note edits, photo uploads, and ingest dumps are not in the
  change journal.
- Back-history is session memory, not persisted across reloads.
- The localStorage GitHub token is convenient but risky; a fine-grained
  token (or backend) is the safer long-term design.
- The dashboard is public and currently contains family dossiers.

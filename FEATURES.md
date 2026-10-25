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
  Changelog; order is user-rearrangeable in settings (gear icon). Number
  keys 1–6 select views in that order; Up/Down arrow through views then
  buddies.
- **Org Chart view zoom** — the Org Chart opens fitted to the whole staff;
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
  resizing Views is absorbed by that scroll region, never by the Tip Jar.
- **Escape closes the panels** — ESC dismisses transient UI first
  (popovers, menus, the field-settings sheet — one per press), then closes
  the info panel and the buddy panel together, from any focus location,
  including the search box.
- **Collapsed rail fits its icons** — the icon rail's height shrink-wraps
  its contents (expand chevron, view icons, current-view button): every
  icon visible, no trailing void below the last one. On a viewport too
  short for the stack, the rail caps at the viewport height and scrolls
  internally.
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
- **Navigation** — Back, Prev, Next, and All buddies.
- **Draggable sections** — no visible gripper (Dave, 2026-10-21): drag a
  section by its name text to reorder it directly on the panel — the name
  alone is the grab zone (grab cursor over the name only); pressing
  anywhere else on the header never starts a drag. A plain click still
  collapses/expands, and the Settings sheet's Buddy fields section spells
  the tip out. Order persists per device via `fieldOrder` (also editable
  in field settings).
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
  persists across reloads via localStorage; reverts all logged changes
  at once.
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
  exposed dimmed sliver of canvas taps shut. The resting state is a 66px
  **icon strip** — Recents worn vertically (Jonny's crit, 2026-10-22): the
  Recents button pinned in the first top-left slot, then any favorites,
  then the recent buddies themselves (as many as the Recents count in
  Settings), the selected buddy always present and accent-marked — and
  then the strip ends; a grid door at its foot opens the full dock (the
  strip's bottom padding holds the door clear of the floating bottom nav
  cluster), and
  first run (no history yet) falls back to the root buddies — plus
  the **View pill** at the canvas's top-left. The View control carries a
  **caret (▾)** at every size — it is a menu, and the caret rotates while
  its menu is open. **Find** (first button in the bottom cluster) opens a
  sticky search bar at the top of the screen: empty it lists Recents,
  typing switches to auto-suggest with the sidebar search's matcher and
  matched characters in bold; picking a result lands on that buddy's
  homepage with the docks closed. A fresh load or deep link at phone
  widths restores the selection but never an open panel (**closed on
  open**). The old drawer, the portrait full-screen takeover, and the
  floating-card sheet are retired. The phone icon strip never renders at
  ≥640px (a global hide rule; its show rule lives only inside the <640px
  query).
- **First open (fresh context, phone)**: with no stored state on the
  device, the dashboard opens as a front door — the resting geometry is
  invariant at first paint (66px strip + canvas, never dock width), the
  canvas lands on Astro's homepage without recording a visit, and a
  one-time **Welcome Card** (dismissed per device, stored in its own
  `buddyWelcome.system` key) names the place, states the scale, and
  teaches the doors in one sentence. The strip seeds from the root
  buddies until real history exists — no fake recency.
- **The Lift**: while typing on the phone (keyboard open), the Prev/Next
  pill rides above the keyboard via a `--kb-lift` offset driven by focus
  and `visualViewport`, and settles back when the keyboard closes.
- **Medium (640–1100px)**: collapsible sidebar; view nav becomes a horizontal
  segmented control; detail opens as a right-docked side sheet (380px).
- **Large (>1100px)**: tri-pane with persistent detail panel (400px).
- **Keyboard**: arrows move between buddies, Esc closes the detail panel.
  **⌘F** toggles Find (the same action as the footer Find button), and
  **⌘I** toggles the info panel — collapse/expand, or open it when no
  buddy panel is up. Both work even when a buddy homepage iframe has
  focus (the iframe forwards the chords to the parent chrome).

## Known limitations / follow-ups

- Photo "all image types" claim is aspirational: HEIC is converted and
  JPEG/PNG/GIF/WebP work, but other formats are merely renamed to `.jpg`.
- Shared-note edits, photo uploads, and ingest dumps are not in the
  change journal.
- Back-history is session memory, not persisted across reloads.
- The localStorage GitHub token is convenient but risky; a fine-grained
  token (or backend) is the safer long-term design.
- The dashboard is public and currently contains family dossiers.

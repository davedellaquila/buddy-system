# Buddies Dashboard — Feature Registry

Living list of every feature in the dashboard. Update this file when a feature
ships or changes — it's the source of truth for future documentation.

Repo: https://github.com/davedellaquila/buddy-system
Live: https://davedellaquila.github.io/buddy-system/
Build: `build.py` generates `index.html` from `buddies.json` + `plans.json`.

---

## Tree chart

- **Classic tree layout** — the canonical design. (A card-based redesign was
  tried and reverted; preserved on branch `card-tree-redesign` for reference.)
- **Zoom slider** — vertical slider beside the chart, 50–160%.
- **Shift+scroll zoom** — hold Shift and scroll over the tree to zoom.
- **Grab-to-pan** — click-drag the chart to slide it around; grab/grabbing
  cursors; small movements still count as clicks; the stray click after a
  drag is swallowed so you don't navigate by accident.
- **Drag-to-reparent on tiles** — grab any tree tile and drag it onto another
  buddy to reparent it. Pointer-based (mouse + touch), so it works on
  iPhone/iPad where HTML5 drag-and-drop never fires. A tap still opens the
  buddy's detail panel (drag vs. click distinguished by a 6px movement
  threshold); the stray click after a drag is swallowed. Loop protection:
  can't drop a parent onto its own descendant (invalid targets get a red
  dashed outline). Root can't be dragged; dropping onto root makes a buddy
  top-level.
- **Orphaned buddies section** — buddies with no parent render in their own
  tree section, instead of being invisible.
- **Drop targets** — tree nodes and Projects rows accept drops from the
  sidebar and from tile drags to assign/change parents.

## Appearance

- **Light / Dark / System theme** — segmented picker under the sidebar
  brand; per-device localStorage (default System, follows the OS live).

## Sidebar

- **Main views** — Tree, Projects, Business Plans, Manifest, Project,
  Changelog; order is user-rearrangeable in settings (gear icon). Number
  keys 1–6 select views in that order; Up/Down arrow through views then
  buddies.
- **Project view** — shows the current project's homepage full-bleed in the
  main view area (no margins); a floating "Open in a new tab" pill button
  overlays the top. Clicking a sidebar buddy loads its homepage if it has
  one, and leaves the view untouched if it doesn't. Buddies without a
  homepage show a "No homepage for this project" empty state. Picking a
  view-menu option never dismisses the right-side buddy panel.
- **Projects view** — hierarchical outline of every buddy with its status;
  opens with global attention tiles (TO REVIEW / NEW / CLEARED across all
  buddies), constrained to the same 860px width as the list below.
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
- **Drag-to-reparent** — drag any sidebar buddy onto a tree node or
  Projects row to change its parent.
- **App name** — the top-left "Buddies" label is inline-editable,
  device-persisted, and updates the browser title.

## Buddy detail pages

- **Navigation** — Back, Prev, Next, and All buddies.
- **Build numbers** — every buddy and business-plan page shows a timestamp
  build number.
- **Click-to-rename** — buddy names are inline editable.
- **Scratch notes** — device-local freeform notes (localStorage).
- **Shared notes** — sync to the buddy's repo at `docs/notes.md` via the
  GitHub Contents API (needs a token; falls back to device-local).
- **Ingest box** — brain-dump raw thoughts about the buddy; each dump is
  appended as a timestamped entry to the buddy's repo `docs/ingest.md`.
  Raw material for later dossier work. Dumps live in a collapsible
  "Dumps (n)" section (collapsed by default, state remembered per buddy);
  each dump tile has edit (✏️) and delete (🗑️) buttons in its upper-right
  corner.
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
- **Small (<640px)**: tiles stack as full-width cards; sidebar becomes a
  drawer (hamburger button); detail opens as a bottom sheet; the Tree view
  keeps the org chart (pan with a finger, floating zoom slider) instead of a
  card list.
- **Medium (640–1100px)**: collapsible sidebar; view nav becomes a horizontal
  segmented control; detail opens as a right-docked side sheet (380px).
- **Large (>1100px)**: tri-pane with persistent detail panel (400px).
- **Keyboard**: arrows move between buddies, Esc closes the detail panel.

## Known limitations / follow-ups

- Photo "all image types" claim is aspirational: HEIC is converted and
  JPEG/PNG/GIF/WebP work, but other formats are merely renamed to `.jpg`.
- Shared-note edits, photo uploads, and ingest dumps are not in the
  change journal.
- Back-history is session memory, not persisted across reloads.
- The localStorage GitHub token is convenient but risky; a fine-grained
  token (or backend) is the safer long-term design.
- The dashboard is public and currently contains family dossiers.

## 2026-10-21
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

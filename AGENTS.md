# Agent standing rules (buddy system)

Read this when you start (INIT / MEMORY / first homepage pass). These override convenience defaults.

## CRITICAL — Dark mode for every buddy website

**Every buddy website / homepage must ship a working dark mode.**

- Prefer `prefers-color-scheme: dark` (or an equivalent explicit theme) so the page is readable outdoors and at night without a flashlight UI.
- Light-only custom dossiers are not done. If your site is light-only or hard-coded to one theme, add dark mode **now**.
- New buddies: include dark mode in the first homepage ship; INIT / MEMORY should call this out when the site is mentioned.
- Canonical memo: [docs/standing-orders.md](docs/standing-orders.md).

Do not treat this as polish-later. It is a standing product requirement.

## Generator skip-check trap (hit 2026-10-16 — Social Media Buddy)
`gen_basic_homepages.py` decides a page is template-managed with
`('BUDDY-BASIC-TEMPLATE' in content) or ('Part of the Buddy System' in content)`.
Removing the marker is NOT enough: any thread-owned custom page whose footer
(or any text) contains the literal phrase "Part of the Buddy System" gets
regenerated and wiped on the next generator run — exactly what happened to the
Social Media Buddy custom homepage in commit e209ba2. Thread-owned pages must
avoid that exact phrase everywhere (footer, comments, JS strings). Case-sensitive
match, so "part of Dave's buddy system" is safe — but simplest is to never use
the phrase at all.

#!/usr/bin/env python3
"""Generate basic homepages for buddies that don't have one yet.

CRITICAL: every buddy website must support dark mode. This template does via
prefers-color-scheme — do not ship light-only pages. See AGENTS.md and
docs/standing-orders.md.
"""
import json
import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

with open('buddies.json') as f:
    d = json.load(f)

by_id = {b['id']: b for b in d['buddies']}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}</title>
<style>
:root {{
  --bg: #ffffff;
  --text: #1a1a1a;
  --muted: #666;
  --card: #f5f5f5;
  --border: #e0e0e0;
  --accent: #0066cc;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #1a1a1a;
    --text: #e0e0e0;
    --muted: #999;
    --card: #2a2a2a;
    --border: #3a3a3a;
    --accent: #4da6ff;
  }}
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  padding: 40px 20px;
  max-width: 800px;
  margin: 0 auto;
}}
.header {{ text-align: center; margin-bottom: 40px; }}
.icon {{ font-size: 64px; margin-bottom: 16px; }}
h1 {{ font-size: 32px; margin-bottom: 8px; }}
.tagline {{ color: var(--muted); font-size: 18px; }}
.mission {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
  font-size: 17px;
}}
h2 {{ font-size: 22px; margin: 32px 0 16px; }}
.attn {{
  background: var(--card);
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 16px 20px;
  margin-bottom: 12px;
}}
.attn-date {{ color: var(--muted); font-size: 14px; margin-top: 8px; }}
.children {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.child {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 20px;
  text-decoration: none;
  color: var(--text);
}}
.child:hover {{ border-color: var(--accent); }}
.footer {{
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  color: var(--muted);
  font-size: 14px;
  text-align: center;
}}
.empty {{ color: var(--muted); font-style: italic; }}
</style>
</head>
<body>
<div class="header">
<div class="icon">{icon}</div>
<h1>{name}</h1>
<div class="tagline">{tagline}</div>
</div>

<div class="mission">{mission}</div>

{attention_section}

{children_section}

<div class="footer">
Generated {date} · Part of the Buddy System
</div>
</body>
</html>
"""

from datetime import datetime
today = datetime.now().strftime('%Y-%m-%d')

generated = []
for b in d['buddies']:
    if b.get('homepage'):
        continue  # Already has one

    bid = b['id']
    name = html.escape(b.get('name', bid))
    icon = b.get('icon', '🤖')
    tagline = html.escape(b.get('tagline', ''))
    mission = html.escape(b.get('mission', 'No mission yet.'))

    # Attention items
    attn_items = b.get('attention', [])
    if attn_items:
        attn_html = '<h2>Needs Attention</h2>\n'
        for a in attn_items[:10]:
            text = html.escape(a.get('text', str(a)) if isinstance(a, dict) else str(a))
            date = html.escape(a.get('date', '') if isinstance(a, dict) else '')
            attn_html += f'<div class="attn"><div>{text}</div>'
            if date:
                attn_html += f'<div class="attn-date">{date}</div>'
            attn_html += '</div>\n'
        attention_section = attn_html
    else:
        attention_section = '<h2>Needs Attention</h2>\n<p class="empty">Nothing needs attention right now.</p>'

    # Children
    children = [by_id[cid] for cid in b.get('children', []) if cid in by_id]
    # Also find buddies with this as parent
    kids = [x for x in d['buddies'] if x.get('parent') == bid]
    all_kids = {c['id']: c for c in children + kids}.values()
    if all_kids:
        kids_html = '<h2>Sub-buddies</h2>\n<div class="children">\n'
        for k in sorted(all_kids, key=lambda x: x.get('name', '')):
            kname = html.escape(k.get('name', k['id']))
            kicon = k.get('icon', '🤖')
            kids_html += f'<a class="child" href="../{k["id"]}/">{kicon} {kname}</a>\n'
        kids_html += '</div>'
        children_section = kids_html
    else:
        children_section = ''

    page = TEMPLATE.format(
        name=name,
        icon=icon,
        tagline=tagline,
        mission=mission,
        attention_section=attention_section,
        children_section=children_section,
        date=today,
    )

    # Write to <bid>/index.html
    dirpath = os.path.join(HERE, bid)
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, 'index.html'), 'w') as f:
        f.write(page)

    # Update buddies.json
    b['homepage'] = f'{bid}/'
    generated.append(bid)
    print(f"Generated {bid}/index.html")

with open('buddies.json', 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')

print(f"\nDone: {len(generated)} pages generated")

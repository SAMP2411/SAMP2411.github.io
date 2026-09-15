from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'

ASSETS = {
    'autonomous-industrial-inspection-robot': 'assets/project/autonomous-industrial-inspection-hd.webp',
    'robot-fleet-observability-platform': 'assets/project/robot-fleet-observability-hd.webp',
    'industrial-robot-operations-intelligence': 'assets/project/industrial-robot-operations-intelligence-hd.jpg',
}

CARD_MARKERS = {
    'autonomous-industrial-inspection-robot': 'project/autonomous-industrial-inspection-robot.html',
    'robot-fleet-observability-platform': 'project/robot-fleet-observability-platform.html',
    'industrial-robot-operations-intelligence': 'project/industrial-robot-operations-intelligence.html',
}


def patch_card(html, slug, asset):
    marker = CARD_MARKERS[slug]
    pos = html.find(marker)
    if pos == -1:
        return html
    start = html.rfind('<div class="tilt-card', 0, pos)
    end = html.find('</div>\n                </div>', pos)
    if start == -1 or end == -1:
        return html
    block = html[start:end + len('</div>\n                </div>')]

    # Replace only the image/header div. Keep the existing badge/icon overlays.
    pattern = re.compile(
        r'<div class="h-28 relative overflow-hidden tilt-inner bg-gray-900"[^>]*>(?P<body>.*?)</div>\n\s*<div class="p-5',
        re.S,
    )
    match = pattern.search(block)
    if not match:
        return html

    body = match.group('body')
    # Remove any previous full-cover img to make the operation idempotent.
    body = re.sub(r'<img[^>]*data-hd-project-image="true"[^>]*>', '', body)
    img = (
        f'<img src="{asset}" data-hd-project-image="true" '
        'class="absolute inset-0 w-full h-full object-cover opacity-100 z-0" '
        'loading="eager" decoding="async" alt="Project visualization">'
    )
    replacement = (
        '<div class="h-28 relative overflow-hidden tilt-inner bg-gray-900">'
        + img + body
        + '</div>\n                    <div class="p-5'
    )
    block2 = pattern.sub(replacement, block, count=1)
    return html[:start] + block2 + html[end + len('</div>\n                </div>'):]


def patch_detail(slug, asset):
    path = ROOT / 'project' / f'{slug}.html'
    if not path.exists():
        return
    text = path.read_text()
    hero_pattern = re.compile(
        r'<div class="project-visual rounded-xl mb-8 relative(?: overflow-hidden)?"[^>]*>(.*?)</div>',
        re.S,
    )
    m = hero_pattern.search(text)
    if not m:
        return
    inner = m.group(1)
    inner = re.sub(r'<img[^>]*data-hd-project-image="true"[^>]*>', '', inner)
    img = (
        f'<img src="../{asset}" data-hd-project-image="true" '
        'class="absolute inset-0 w-full h-full object-cover opacity-100 z-0" '
        'loading="eager" decoding="async" alt="Project visualization">'
    )
    # Keep badge above the image.
    inner = inner.replace('<span ', '<span style="position:relative;z-index:2" ', 1) if '<span ' in inner else inner
    hero = '<div class="project-visual rounded-xl mb-8 relative overflow-hidden">' + img + inner + '</div>'
    text = text[:m.start()] + hero + text[m.end():]
    path.write_text(text)


html = INDEX.read_text()
for slug, asset in ASSETS.items():
    html = patch_card(html, slug, asset)
    patch_detail(slug, asset)
INDEX.write_text(html)
print('Forced real <img> rendering for the three industrial project visuals.')

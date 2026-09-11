from pathlib import Path

ROOT = Path('.')

REPLACEMENTS = {
    'dse-hd.svg': 'dse-photo-hd.webp',
    'competitive-hd.svg': 'competitive-photo-hd.webp',
    'turtlebot3-hd.svg': 'turtlebot3-photo-hd.webp',
    'ur10-hd.svg': 'ur10-photo-hd.webp',
    'iiot-hd.svg': 'iiot-photo-hd.webp',
    'face-hd.svg': 'face-photo-hd.webp',
    'rst-hd.svg': 'rst-photo-hd.webp',
    'so101-hd.svg': 'so101-photo-hd.webp',
    'jj-hd.svg': 'jj-photo-hd.webp',
}

def patch(path: Path):
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.replace('AI VISUAL • VECTOR HD', 'AI VISUAL • HD')
    text = text.replace('AI-GENERATED VISUALIZATION • VECTOR HD', 'AI-GENERATED VISUALIZATION • HD')
    # Keep the photorealistic media fully visible. Only a very light lower gradient remains for contrast.
    text = text.replace('from-black/10 via-transparent to-transparent opacity-10', 'from-black/10 via-transparent to-transparent opacity-5')
    if text != original:
        path.write_text(text, encoding='utf-8')

patch(ROOT / 'index.html')
for path in (ROOT / 'project').glob('*.html'):
    patch(path)
for path in (ROOT / 'experience').glob('*.html'):
    patch(path)

print('Switched portfolio media back to the photorealistic 1600x900 HD assets.')

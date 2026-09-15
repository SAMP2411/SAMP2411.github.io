from pathlib import Path
from PIL import Image

ROOT = Path('.')
ASSET_DIR = ROOT / 'assets' / 'project'

# These are true source-derived HD exports created directly from the original
# 1672x941 generated renders. Do not regenerate them from the old 240x135
# preview images: that produced nominal 1600x900 files with visibly soft detail.
ASSETS = {
    'autonomous-industrial-inspection': ASSET_DIR / 'autonomous-industrial-inspection-original-hd.webp',
    'robot-fleet-observability': ASSET_DIR / 'robot-fleet-observability-original-hd.webp',
    'industrial-robot-operations-intelligence': ASSET_DIR / 'industrial-robot-operations-intelligence-original-hd.webp',
}

for stem, path in ASSETS.items():
    if not path.exists():
        raise FileNotFoundError(f'Missing source-derived HD asset: {path}')
    if path.stat().st_size < 70000:
        raise RuntimeError(f'{path}: unexpectedly small/truncated ({path.stat().st_size} bytes)')
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        if image.size != (1280, 720):
            raise RuntimeError(f'{path}: expected true HD 1280x720, got {image.size}')
    print(f'VALID ORIGINAL HD {path}: 1280x720, {path.stat().st_size} bytes')

REPLACEMENTS = {
    'autonomous-industrial-inspection-hd-v2.webp': 'autonomous-industrial-inspection-original-hd.webp',
    'autonomous-industrial-inspection-hd.webp': 'autonomous-industrial-inspection-original-hd.webp',
    'robot-fleet-observability-hd-v2.webp': 'robot-fleet-observability-original-hd.webp',
    'robot-fleet-observability-hd.webp': 'robot-fleet-observability-original-hd.webp',
    'industrial-robot-operations-intelligence-hd-v2.webp': 'industrial-robot-operations-intelligence-original-hd.webp',
    'industrial-robot-operations-intelligence-hd.jpg': 'industrial-robot-operations-intelligence-original-hd.webp',
    'industrial-robot-operations-intelligence-hd.webp': 'industrial-robot-operations-intelligence-original-hd.webp',
}

for path in [ROOT / 'index.html', *(ROOT / 'project').glob('*.html')]:
    if not path.exists():
        continue
    text = path.read_text()
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text)

print('Source-derived industrial project HD assets verified and applied.')

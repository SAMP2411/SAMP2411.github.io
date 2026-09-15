from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / '.image_chunks'
ASSETS = ROOT / 'assets' / 'project'
ASSETS.mkdir(parents=True, exist_ok=True)

FILES = {
    'autonomous-industrial-inspection-hd': 'autonomous-industrial-inspection-hd.webp',
    'robot-fleet-observability-hd': 'robot-fleet-observability-hd.webp',
    'industrial-robot-operations-intelligence-hd': 'industrial-robot-operations-intelligence-hd.webp',
}

for stem, out_name in FILES.items():
    parts = sorted(CHUNKS.glob(f'{stem}.*.b64part'))
    if not parts:
        raise SystemExit(f'No chunks found for {stem}')
    payload = ''.join(p.read_text().strip() for p in parts)
    raw = base64.b64decode(payload, validate=True)
    if not raw.startswith(b'RIFF') or b'WEBP' not in raw[:16]:
        raise SystemExit(f'{stem}: reconstructed payload is not WebP')
    # Verify RIFF declared length exactly matches reconstructed bytes.
    declared = int.from_bytes(raw[4:8], 'little') + 8
    if declared != len(raw):
        raise SystemExit(f'{stem}: incomplete WebP ({len(raw)} bytes, header expects {declared})')
    (ASSETS / out_name).write_bytes(raw)
    print(f'{out_name}: {len(raw)} bytes')

# The third project previously used a .jpg path. Normalize all three to WebP.
for path in [ROOT / 'index.html', *(ROOT / 'project').glob('*.html')]:
    if not path.exists():
        continue
    text = path.read_text()
    text = text.replace('industrial-robot-operations-intelligence-hd.jpg', 'industrial-robot-operations-intelligence-hd.webp')
    path.write_text(text)

print('HD project images reconstructed successfully.')

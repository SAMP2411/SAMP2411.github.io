from pathlib import Path
from urllib.request import urlretrieve
import cv2
from PIL import Image, ImageFilter

ROOT = Path('.')
SRC_DIR = ROOT / 'assets' / 'project' / 'source'
OUT_DIR = ROOT / 'assets' / 'project'
MODEL_DIR = ROOT / '.cache' / 'superres'
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / 'EDSR_x4.pb'
MODEL_URL = 'https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb'

SOURCES = {
    'autonomous-industrial-inspection': 'autonomous-industrial-inspection.webp',
    'robot-fleet-observability': 'robot-fleet-observability.webp',
    'industrial-robot-operations-intelligence': 'industrial-robot-operations-intelligence.webp',
}

if not MODEL_PATH.exists():
    print('Downloading EDSR x4 super-resolution model...')
    urlretrieve(MODEL_URL, MODEL_PATH)

sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(str(MODEL_PATH))
sr.setModel('edsr', 4)

for stem, source_name in SOURCES.items():
    src = SRC_DIR / source_name
    if not src.exists():
        raise FileNotFoundError(f'Missing industrial project source: {src}')

    img = cv2.imread(str(src), cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f'Could not decode source image: {src}')

    h, w = img.shape[:2]
    print(f'{src}: {w}x{h} -> EDSR x4 -> 1600x900')

    enhanced = sr.upsample(img)
    enhanced = cv2.resize(enhanced, (1600, 900), interpolation=cv2.INTER_LANCZOS4)

    rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    pil = pil.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))

    out = OUT_DIR / f'{stem}-hd.webp'
    pil.save(out, 'WEBP', quality=95, method=6)

    with Image.open(out) as check:
        check.verify()
    with Image.open(out) as check:
        if check.size != (1600, 900):
            raise RuntimeError(f'{out}: wrong dimensions {check.size}')
    if out.stat().st_size < 30000:
        raise RuntimeError(f'{out}: output unexpectedly small/truncated ({out.stat().st_size} bytes)')
    print(f'VALID {out}: 1600x900, {out.stat().st_size} bytes')

for path in [ROOT / 'index.html', *(ROOT / 'project').glob('*.html')]:
    if not path.exists():
        continue
    text = path.read_text()
    text = text.replace(
        'industrial-robot-operations-intelligence-hd.jpg',
        'industrial-robot-operations-intelligence-hd.webp'
    )
    path.write_text(text)

print('Industrial project HD images regenerated and verified.')

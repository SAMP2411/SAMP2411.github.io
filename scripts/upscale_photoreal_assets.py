from pathlib import Path
from urllib.request import urlretrieve
import cv2
from PIL import Image, ImageFilter

ROOT = Path('.')
ASSET_DIR = ROOT / 'assets' / 'ai'
MODEL_DIR = ROOT / '.cache' / 'superres'
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / 'EDSR_x4.pb'
MODEL_URL = 'https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb'

# Preserve the earlier photorealistic compositions, but regenerate them as 1600x900 HD assets.
SOURCES = {
    'dse': 'dse.webp',
    'competitive': 'competitive.webp',
    'turtlebot3': 'turtlebot3.webp',
    'ur10': 'ur10.webp',
    'iiot': 'iiot.webp',
    'face': 'face.webp',
    'rst': 'rst.webp',
    'so101': 'so101.webp',
    'jj': 'jj.webp',
}

if not MODEL_PATH.exists():
    print('Downloading EDSR x4 super-resolution model...')
    urlretrieve(MODEL_URL, MODEL_PATH)

sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(str(MODEL_PATH))
sr.setModel('edsr', 4)

for stem, source_name in SOURCES.items():
    src = ASSET_DIR / source_name
    if not src.exists():
        raise FileNotFoundError(f'Missing source image: {src}')

    img = cv2.imread(str(src), cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f'Could not read source image: {src}')

    h, w = img.shape[:2]
    print(f'{source_name}: {w}x{h} -> EDSR x4 -> 1600x900')
    enhanced = sr.upsample(img)

    # Center-crop to 16:9 before the final resize, preserving composition with minimal distortion.
    eh, ew = enhanced.shape[:2]
    target_ratio = 16 / 9
    ratio = ew / eh
    if ratio > target_ratio:
        new_w = round(eh * target_ratio)
        left = max(0, (ew - new_w) // 2)
        enhanced = enhanced[:, left:left + new_w]
    elif ratio < target_ratio:
        new_h = round(ew / target_ratio)
        top = max(0, (eh - new_h) // 2)
        enhanced = enhanced[top:top + new_h, :]

    enhanced = cv2.resize(enhanced, (1600, 900), interpolation=cv2.INTER_LANCZOS4)
    rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    # Mild sharpening only; avoid halos and the artificial over-sharpened look.
    pil = pil.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))

    out = ASSET_DIR / f'{stem}-photo-hd.webp'
    pil.save(out, 'WEBP', quality=95, method=6)
    print(f'Wrote {out} ({out.stat().st_size // 1024} KiB)')

print('Photorealistic project visuals upgraded to 1600x900 HD.')

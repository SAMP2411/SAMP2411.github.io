from pathlib import Path
import re

AI = {
    'distributed-state-estimation': 'dse.webp',
    'competitive-robotics': 'competitive.webp',
    'turtlebot3-navigation': 'turtlebot3.webp',
    'ur10-manipulator': 'ur10.webp',
    'iiot-anomaly-detector': 'iiot.webp',
    'offline-face-recognition': 'face.webp',
    'rst-hackathon': 'rst.webp',
    'so101-robot-learning': 'so101.webp',
}

BADGE = '<span class="absolute top-2 left-2 z-20 px-2 py-1 text-[9px] font-mono border border-white/20 text-gray-300 bg-black/65">AI VISUAL</span>'

# Homepage cards: replace missing legacy thumbnails and sprite backgrounds.
p = Path('index.html')
text = p.read_text(encoding='utf-8')

for old, new in [('project1.jpg', 'assets/ai/dse.webp'), ('project3.jpg', 'assets/ai/competitive.webp')]:
    text = text.replace(f'src="{old}"', f'src="{new}"')

# Label the two converted legacy images as AI visuals.
for asset in ['assets/ai/dse.webp', 'assets/ai/competitive.webp']:
    needle = f'src="{asset}"'
    pos = text.find(needle)
    if pos >= 0:
        tag_end = text.find('>', pos)
        following = text[tag_end+1:tag_end+1+len(BADGE)+40]
        if 'AI VISUAL' not in following:
            text = text[:tag_end+1] + BADGE + text[tag_end+1:]

positions = {
    '0%': 'turtlebot3.webp',
    '16.6667%': 'ur10.webp',
    '33.3333%': 'iiot.webp',
    '50%': 'face.webp',
    '66.6667%': 'rst.webp',
    '83.3333%': 'so101.webp',
}
for pos, asset in positions.items():
    old = f"background-image:url('assets/portfolio-ai-sprite.svg');background-size:100% 700%;background-position:center {pos};background-repeat:no-repeat"
    new = f"background-image:url('assets/ai/{asset}');background-size:cover;background-position:center;background-repeat:no-repeat"
    text = text.replace(old, new)

p.write_text(text, encoding='utf-8')

# Detail pages.
for slug, asset in AI.items():
    page = Path('project') / f'{slug}.html'
    if not page.exists():
        continue
    t = page.read_text(encoding='utf-8')

    # Replace missing legacy image banners with generated assets.
    t = re.sub(
        r'<div class="project-visual rounded-xl mb-8 relative overflow-hidden"><img src="\.\./project[13]\.jpg"[^>]*><span class="source-badge">PROJECT MEDIA</span></div>',
        f'<div class="project-visual rounded-xl mb-8 relative" style="background-image:url(\'../assets/ai/{asset}\');background-size:cover;background-position:center;background-repeat:no-repeat"><span class="ai-badge">AI-GENERATED VISUALIZATION</span></div>',
        t,
        count=1,
    )

    # Replace generated sprite slice with the project's actual individual image.
    t = re.sub(
        r"background-image:url\('\.\./assets/portfolio-ai-sprite\.svg'\);background-size:100% 700%;background-position:center [^;]+;background-repeat:no-repeat",
        f"background-image:url('../assets/ai/{asset}');background-size:cover;background-position:center;background-repeat:no-repeat",
        t,
        count=1,
    )
    page.write_text(t, encoding='utf-8')

# J&J lives under Experience, not Projects.
jj = Path('experience/jj-medtech-robotics.html')
if jj.exists():
    t = jj.read_text(encoding='utf-8')
    t = re.sub(
        r"background-image:url\('\.\./assets/portfolio-ai-sprite\.svg'\);background-size:100% 700%;background-position:center [^;]+;background-repeat:no-repeat",
        "background-image:url('../assets/ai/jj.webp');background-size:cover;background-position:center;background-repeat:no-repeat",
        t,
        count=1,
    )
    jj.write_text(t, encoding='utf-8')

print('Applied individual AI assets to homepage, project pages, and J&J experience page.')

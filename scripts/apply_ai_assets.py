from pathlib import Path
import html
import re

# Scalable 1600x900 vector artwork: stays crisp on Retina/4K displays.
VISUALS = {
    'distributed-state-estimation': dict(file='dse-hd.svg', title='Distributed State Estimation', subtitle='EMBEDDED LINUX  •  SECURE OTA  •  EDGE INTELLIGENCE', accent='#00f0ff', accent2='#6d5cff', kind='dse'),
    'competitive-robotics': dict(file='competitive-hd.svg', title='Competitive Robotics', subtitle='DESIGN  •  BUILD  •  CONTROL  •  COMPETE', accent='#0aff64', accent2='#00d4ff', kind='competition'),
    'turtlebot3-navigation': dict(file='turtlebot3-hd.svg', title='TurtleBot3 Autonomous Navigation', subtitle='ROS2  •  SLAM  •  AMCL  •  NAV2', accent='#00f0ff', accent2='#2563eb', kind='turtlebot'),
    'ur10-manipulator': dict(file='ur10-hd.svg', title='UR10 Manipulator Control', subtitle='KINEMATICS  •  DLS  •  TRAJECTORY CONTROL', accent='#a855f7', accent2='#00f0ff', kind='ur10'),
    'iiot-anomaly-detector': dict(file='iiot-hd.svg', title='IIoT Anomaly Detector', subtitle='MQTT  •  STREAMING  •  ISOLATION FOREST', accent='#0aff64', accent2='#00f0ff', kind='iiot'),
    'offline-face-recognition': dict(file='face-hd.svg', title='Offline Face Recognition', subtitle='OPENCV  •  INSIGHTFACE  •  ONNX RUNTIME', accent='#38bdf8', accent2='#7000ff', kind='face'),
    'rst-hackathon': dict(file='rst-hd.svg', title='RST Hackathon', subtitle='VISION  •  TRACKING  •  COORDINATE TRANSFORMS', accent='#facc15', accent2='#00f0ff', kind='rst'),
    'so101-robot-learning': dict(file='so101-hd.svg', title='SO-101 Robot Learning', subtitle='ZERO-SHOT  •  FEW-SHOT  •  IN-CONTEXT', accent='#e879f9', accent2='#00f0ff', kind='so101'),
}
JJ = dict(file='jj-hd.svg', title='MedTech Robotics & Controls', subtitle='TROUBLESHOOT  •  VALIDATE  •  RETEST  •  DOCUMENT', accent='#fb7185', accent2='#00f0ff', kind='jj')

BADGE = '<span class="absolute top-2 left-2 z-20 px-2 py-1 text-[9px] font-mono border border-cyan-300/40 text-cyan-100 bg-black/45 backdrop-blur-sm">AI VISUAL • VECTOR HD</span>'


def esc(s):
    return html.escape(s, quote=True)


def panel(x, y, w, h, title, accent, body=''):
    lines = ''
    if body:
        yy = y + 86
        for part in body.split('|'):
            lines += f'<text x="{x+28}" y="{yy}" class="small">{esc(part.strip())}</text>'
            yy += 34
    return f'''<g class="panel"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22"/><path d="M{x+18} {y+52} H{x+w-18}" class="hair"/><text x="{x+28}" y="{y+36}" class="panelTitle" fill="{accent}">{esc(title)}</text>{lines}</g>'''


def subject(kind, a, b):
    if kind == 'turtlebot':
        return f'''<path d="M820 640 C980 600 1050 520 1190 480 S1370 360 1480 340" class="route"/>
        <g transform="translate(760 520)"><ellipse cx="0" cy="86" rx="160" ry="64" fill="#0b111b" stroke="{a}" stroke-width="5"/><rect x="-128" y="0" width="256" height="118" rx="34" fill="#101827" stroke="{a}" stroke-width="4"/><circle cx="-108" cy="90" r="35" fill="#030609" stroke="#64748b" stroke-width="7"/><circle cx="108" cy="90" r="35" fill="#030609" stroke="#64748b" stroke-width="7"/><rect x="-66" y="-40" width="132" height="60" rx="16" fill="#172334" stroke="{b}" stroke-width="4"/><ellipse cx="0" cy="-45" rx="74" ry="24" fill="#09111b" stroke="{a}" stroke-width="4"/><ellipse cx="0" cy="-45" rx="44" ry="9" fill="{a}" opacity=".65"/><path d="M-210 -45 H210 M0 -150 V80" stroke="{a}" opacity=".25"/><circle cx="0" cy="-45" r="145" fill="none" stroke="{a}" opacity=".18" stroke-width="3"/></g>'''
    if kind in ('ur10', 'rst', 'so101', 'jj'):
        extra = ''
        if kind == 'rst':
            extra = f'<path d="M1045 345 Q1235 155 1430 330" class="route"/><circle cx="1422" cy="326" r="24" fill="{a}"/><circle cx="1480" cy="335" r="88" fill="none" stroke="{a}" stroke-width="8"/><circle cx="1480" cy="335" r="50" fill="none" stroke="{a}" stroke-width="3" opacity=".55"/>'
        elif kind == 'so101':
            extra = f'<rect x="1110" y="602" width="70" height="70" rx="8" fill="#ef4444"/><rect x="1210" y="602" width="70" height="70" rx="8" fill="#22c55e"/><rect x="1310" y="602" width="70" height="70" rx="8" fill="#eab308"/><path d="M1120 540 H1385" stroke="{a}" stroke-width="3" opacity=".5"/>'
        elif kind == 'jj':
            extra = f'<circle cx="1240" cy="590" r="95" fill="#10202c" stroke="{a}" stroke-width="4"/><path d="M1185 590 H1295 M1240 535 V645" stroke="{a}" stroke-width="3" opacity=".65"/><circle cx="1240" cy="590" r="45" fill="none" stroke="{b}" stroke-width="3"/>'
        else:
            extra = f'<path d="M1030 570 C1120 500 1210 520 1310 450" class="route"/><rect x="1325" y="430" width="95" height="95" rx="12" fill="#0f1722" stroke="{a}" stroke-width="4"/>'
        return f'''<g class="arm" transform="translate(720 580)"><rect x="-145" y="70" width="310" height="70" rx="20" fill="#0c131d" stroke="{a}" stroke-width="4"/><circle cx="-70" cy="45" r="62" fill="#111b28" stroke="{a}" stroke-width="5"/><path d="M-70 45 L80 -120" stroke="#cbd5e1" stroke-width="62" stroke-linecap="round"/><circle cx="80" cy="-120" r="56" fill="#111b28" stroke="{b}" stroke-width="5"/><path d="M80 -120 L250 -225" stroke="#cbd5e1" stroke-width="56" stroke-linecap="round"/><circle cx="250" cy="-225" r="48" fill="#111b28" stroke="{a}" stroke-width="5"/><path d="M250 -225 L360 -115" stroke="#cbd5e1" stroke-width="45" stroke-linecap="round"/><circle cx="360" cy="-115" r="39" fill="#111b28" stroke="{b}" stroke-width="4"/><path d="M360 -115 L410 -55" stroke="#cbd5e1" stroke-width="32" stroke-linecap="round"/><path d="M394 -44 l-22 58 M426 -44 l22 58" stroke="{a}" stroke-width="12" stroke-linecap="round"/></g>{extra}'''
    if kind == 'face':
        return f'''<g transform="translate(930 470)"><ellipse cx="0" cy="0" rx="180" ry="235" fill="#08131d" stroke="{a}" stroke-width="5"/><path d="M-128 -120 L-70 -165 L0 -185 L72 -160 L130 -112 L145 -20 L120 95 L65 175 L0 210 L-62 178 L-125 95 L-148 -20 Z" fill="none" stroke="{a}" stroke-width="3" opacity=".8"/><g stroke="{b}" opacity=".65"><path d="M-128 -120 L0 210 L130 -112 M-70 -165 L65 175 M72 -160 L-62 178 M-148 -20 H145 M-125 95 H120"/><path d="M-75 -35 Q-38 -55 0 -35 Q38 -55 78 -35 M-50 75 Q0 115 50 75"/></g><circle cx="-52" cy="-32" r="8" fill="{a}"/><circle cx="52" cy="-32" r="8" fill="{a}"/></g><path d="M700 240 h-55 v55 M1160 240 h55 v55 M700 700 h-55 v-55 M1160 700 h55 v-55" stroke="{a}" stroke-width="8" fill="none"/>'''
    if kind == 'iiot':
        return f'''<g transform="translate(680 350)"><path d="M0 240 V80 H110 V140 H200 V40 H310 V240" fill="#0b1420" stroke="{a}" stroke-width="4"/><rect x="52" y="122" width="28" height="118" fill="{b}" opacity=".35"/><rect x="245" y="82" width="28" height="158" fill="{a}" opacity=".45"/><circle cx="365" cy="165" r="75" fill="#071019" stroke="{a}" stroke-width="4"/><circle cx="365" cy="165" r="38" fill="none" stroke="{b}" stroke-width="12" stroke-dasharray="12 10"/></g><path d="M1020 520 C1090 470 1120 560 1190 500 S1315 420 1390 470" fill="none" stroke="{a}" stroke-width="5"/><g fill="{a}"><circle cx="1020" cy="520" r="8"/><circle cx="1190" cy="500" r="8"/><circle cx="1390" cy="470" r="8"/></g>'''
    if kind == 'competition':
        return f'''<g transform="translate(760 530)"><rect x="-210" y="0" width="420" height="150" rx="25" fill="#0d1520" stroke="{a}" stroke-width="5"/><circle cx="-155" cy="145" r="58" fill="#05070a" stroke="#6b7280" stroke-width="9"/><circle cx="155" cy="145" r="58" fill="#05070a" stroke="#6b7280" stroke-width="9"/><rect x="-115" y="-210" width="58" height="220" rx="16" fill="#b8c0cc"/><rect x="-78" y="-205" width="26" height="190" fill="{b}" opacity=".4"/><path d="M-65 -185 L95 -290" stroke="#cbd5e1" stroke-width="50" stroke-linecap="round"/><circle cx="95" cy="-290" r="45" fill="#101923" stroke="{a}" stroke-width="5"/><path d="M95 -290 L205 -185" stroke="#cbd5e1" stroke-width="42" stroke-linecap="round"/><rect x="190" y="-200" width="115" height="85" rx="12" fill="#4c1d95" stroke="{b}" stroke-width="4"/><rect x="-20" y="35" width="110" height="70" rx="12" fill="#111827" stroke="{a}"/><circle cx="10" cy="70" r="15" fill="#22c55e"/><circle cx="55" cy="70" r="15" fill="#2563eb"/></g>'''
    if kind == 'dse':
        nodes = [(710,360),(920,300),(1120,410),(1340,300),(1240,610),(950,620),(760,590)]
        lines=''.join(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for (x1,y1),(x2,y2) in zip(nodes,nodes[1:]+nodes[:1]))
        dots=''.join(f'<g transform="translate({x} {y})"><rect x="-42" y="-30" width="84" height="60" rx="12" fill="#0b1521" stroke="{a}" stroke-width="3"/><circle r="9" fill="{b}"/></g>' for x,y in nodes)
        return f'''<g stroke="{a}" stroke-width="4" opacity=".65">{lines}</g>{dots}<g transform="translate(1000 460)"><circle r="120" fill="#07121c" stroke="{a}" stroke-width="5"/><circle r="86" fill="none" stroke="{b}" stroke-width="3" stroke-dasharray="8 12"/><text x="0" y="-5" text-anchor="middle" class="centerLabel">EDGE</text><text x="0" y="32" text-anchor="middle" class="centerSub">STATE ESTIMATION</text></g>'''
    return ''


def make_svg(cfg):
    a, b = cfg['accent'], cfg['accent2']
    kind = cfg['kind']
    if kind == 'turtlebot':
        cards = panel(1120,105,390,180,'NAVIGATION STACK',a,'SLAM / MAP|AMCL LOCALIZATION|NAV2 PLANNING') + panel(90,585,390,180,'VALIDATION',b,'TF + ODOM CHECKS|GAZEBO / RVIZ|SIM → REAL')
    elif kind == 'ur10':
        cards = panel(1050,100,460,185,'MOTION PIPELINE',a,'FK / IK|DAMPED LEAST SQUARES|JOINT TRAJECTORY') + panel(90,575,410,185,'SIM → HARDWARE',b,'VERIFY JOINT ORDER|CHECK TRAJECTORY|EXECUTE SAFELY')
    elif kind == 'iiot':
        cards = panel(1030,100,480,190,'STREAMING PIPELINE',a,'MQTT TELEMETRY|PYTHON PROCESSING|ISOLATION FOREST') + panel(95,590,430,175,'MONITORING',b,'TEMPERATURE|VIBRATION|CURRENT')
    elif kind == 'face':
        cards = panel(1100,120,410,180,'OFFLINE PIPELINE',a,'DETECT + ALIGN|POSE VALIDATION|EMBED + MATCH') + panel(90,590,440,170,'GUIDED ENROLLMENT',b,'MULTI-POSE CAPTURE|LOCAL ONNX INFERENCE|NO CLOUD API')
    elif kind == 'rst':
        cards = panel(1080,110,430,175,'HACKATHON LOOP',a,'VISION TRACKING|FRAME TRANSFORMS|THROW STRATEGY') + panel(90,590,420,170,'RESULT',b,'~36–40 HOURS|ROBUST SCOPE CONTROL|3RD PLACE')
    elif kind == 'so101':
        cards = panel(1040,105,470,210,'LEARNING CONDITIONS',a,'ZERO-SHOT|FEW-SHOT|IN-CONTEXT') + panel(90,575,430,190,'EVALUATION',b,'COMMON TASK|SUCCESS / FAILURE LOGS|HARDWARE TRANSFER')
    elif kind == 'jj':
        cards = panel(1020,105,490,205,'VALIDATION WORKFLOW',a,'MEASURE RESPONSE|REVIEW PYTHON CONTROL|RETEST AFTER CHANGES') + panel(90,575,445,190,'ENGINEERING OUTPUT',b,'BEFORE / AFTER TIMINGS|CORRECTIVE ACTIONS|DOCUMENTATION')
    elif kind == 'competition':
        cards = panel(1070,105,440,190,'CONTROL STACK',a,'PS4 INPUT|RASPBERRY PI|ARDUINO ACTUATION') + panel(90,590,430,175,'COMPETITION FOCUS',b,'MECHANISM ROUTINES|PID-ORIENTED TUNING|RELIABILITY')
    else:
        cards = panel(1110,100,400,210,'DEPLOYMENT LAYER',a,'YOCTO / BUILDROOT|RAUC A/B OTA|CONTAINERD') + panel(90,590,430,180,'RESILIENCE',b,'RSA-4096 SIGNING|ROLLBACK|QEMU + CI')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">
<title id="title">{esc(cfg['title'])}</title><desc id="desc">AI-generated scalable technical visualization for {esc(cfg['title'])}</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050b"/><stop offset=".55" stop-color="#08111d"/><stop offset="1" stop-color="#03060c"/></linearGradient><radialGradient id="glow"><stop stop-color="{a}" stop-opacity=".22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient><pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="{a}" stroke-opacity=".075"/></pattern><filter id="soft"><feGaussianBlur stdDeviation="18"/></filter></defs>
<style>.title{{font:700 58px system-ui,sans-serif;letter-spacing:-1px;fill:#f8fafc}}.subtitle{{font:600 17px system-ui,sans-serif;letter-spacing:4px;fill:#9ca3af}}.panel rect{{fill:#07111c;fill-opacity:.9;stroke:#334155;stroke-width:1.5}}.panelTitle{{font:700 17px system-ui,sans-serif;letter-spacing:1.4px}}.small{{font:500 15px system-ui,sans-serif;fill:#cbd5e1}}.hair{{stroke:#475569;stroke-width:1}}.route{{fill:none;stroke:{a};stroke-width:6;stroke-linecap:round;stroke-dasharray:16 14;filter:url(#soft)}}.centerLabel{{font:800 24px system-ui,sans-serif;fill:#fff;letter-spacing:2px}}.centerSub{{font:600 13px system-ui,sans-serif;fill:{a};letter-spacing:2px}}</style>
<rect width="1600" height="900" fill="url(#bg)"/><rect width="1600" height="900" fill="url(#grid)"/><ellipse cx="1030" cy="460" rx="560" ry="420" fill="url(#glow)"/><circle cx="1300" cy="130" r="220" fill="{b}" opacity=".06" filter="url(#soft)"/>
<text x="78" y="104" class="title">{esc(cfg['title'])}</text><text x="82" y="142" class="subtitle">{esc(cfg['subtitle'])}</text><rect x="80" y="174" width="120" height="5" rx="3" fill="{a}"/>
{cards}{subject(kind,a,b)}
<text x="82" y="842" class="subtitle" fill="{a}">SAMARTH PATEL  •  ROBOTICS ENGINEERING PORTFOLIO</text><text x="1515" y="842" text-anchor="end" class="small">AI-GENERATED VECTOR VISUALIZATION</text>
</svg>'''


def generate_visuals():
    out = Path('assets/ai')
    out.mkdir(parents=True, exist_ok=True)
    for cfg in list(VISUALS.values()) + [JJ]:
        (out / cfg['file']).write_text(make_svg(cfg), encoding='utf-8')


def patch_card(text, slug, asset):
    marker = f'data-project-detail="project/{slug}.html"'
    m = text.find(marker)
    if m < 0:
        return text
    start = text.rfind('<div class="tilt-card', 0, m)
    next_comment = text.find('<!-- Project', m + len(marker))
    end = next_comment if next_comment >= 0 else text.find('</section>', m)
    if start < 0 or end < 0:
        return text
    block = text[start:end]
    style = f"background-image:url('assets/ai/{asset}');background-size:cover;background-position:center;background-repeat:no-repeat"
    block = re.sub(r'(<div class="h-28 relative overflow-hidden tilt-inner bg-gray-900")(?: style="[^"]*")?>', rf'\1 style="{style}">', block, count=1)
    block = re.sub(r'<img\s+[^>]*>', '', block, count=1)
    first_visual = block.find('class="h-28 relative overflow-hidden tilt-inner bg-gray-900"')
    if first_visual >= 0 and 'AI VISUAL' not in block[first_visual:first_visual+700]:
        gt = block.find('>', first_visual)
        block = block[:gt+1] + BADGE + block[gt+1:]
    block = block.replace('bg-gradient-to-t from-cyber-black via-transparent to-transparent opacity-80', 'bg-gradient-to-t from-black/25 via-transparent to-transparent opacity-30')
    text = text[:start] + block + text[end:]
    return text


def patch_detail(page, asset):
    if not page.exists():
        return
    t = page.read_text(encoding='utf-8')
    replacement = f'''<div class="project-visual rounded-xl mb-8 relative" style="background-image:url('../assets/ai/{asset}');background-size:cover;background-position:center;background-repeat:no-repeat"><span class="ai-badge">AI-GENERATED VISUALIZATION • VECTOR HD</span></div>'''
    t = re.sub(r'<div class="project-visual rounded-xl mb-8 relative(?: overflow-hidden)?"[^>]*>.*?</div>', replacement, t, count=1, flags=re.S)
    page.write_text(t, encoding='utf-8')


def main():
    generate_visuals()
    p = Path('index.html')
    text = p.read_text(encoding='utf-8')
    text = text.replace('opacity-60 group-hover:opacity-40', 'opacity-100 group-hover:opacity-100')
    text = text.replace('bg-gradient-to-t from-cyber-black via-transparent to-transparent opacity-80', 'bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-25')
    for slug, cfg in VISUALS.items():
        text = patch_card(text, slug, cfg['file'])
    p.write_text(text, encoding='utf-8')

    for slug, cfg in VISUALS.items():
        patch_detail(Path('project') / f'{slug}.html', cfg['file'])
    patch_detail(Path('experience/jj-medtech-robotics.html'), JJ['file'])
    print('Generated 1600x900 scalable vector-HD visuals and removed heavy card-image dimming.')

if __name__ == '__main__':
    main()

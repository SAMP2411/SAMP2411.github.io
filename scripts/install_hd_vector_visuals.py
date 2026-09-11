from pathlib import Path
import re

ROOT = Path('.')
ASSET_DIR = ROOT / 'assets' / 'ai'
ASSET_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = {
    'dse': ('DISTRIBUTED STATE ESTIMATION', 'EDGE LINUX • OTA • RESILIENT DEPLOYMENT', '#00f0ff', 'dse'),
    'competitive': ('COMPETITIVE ROBOTICS', 'DESIGN • BUILD • CONTROL • COMPETE', '#0aff64', 'competitive'),
    'turtlebot3': ('TURTLEBOT3 AUTONOMY', 'ROS2 • SLAM • AMCL • NAV2', '#00f0ff', 'turtlebot'),
    'ur10': ('UR10 MANIPULATOR CONTROL', 'KINEMATICS • DLS • TRAJECTORIES', '#a855f7', 'ur10'),
    'iiot': ('IIOT ANOMALY DETECTOR', 'MQTT • ISOLATION FOREST • MONITORING', '#0aff64', 'iiot'),
    'face': ('OFFLINE FACE RECOGNITION', 'OPENCV • INSIGHTFACE • ONNX', '#38bdf8', 'face'),
    'rst': ('RST HACKATHON', 'VISION • TRANSFORMS • ROBOT ACTION', '#facc15', 'rst'),
    'so101': ('SO-101 ROBOT LEARNING', 'ZERO-SHOT • FEW-SHOT • IN-CONTEXT', '#e879f9', 'so101'),
    'jj': ('MEDTECH ROBOTICS VALIDATION', 'PYTHON • TEST • MEASURE • DOCUMENT', '#fb7185', 'jj'),
}

DEFS = '''
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#030712"/><stop offset=".55" stop-color="#071422"/><stop offset="1" stop-color="#020617"/></linearGradient>
  <radialGradient id="halo"><stop stop-color="{accent}" stop-opacity=".32"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#ffffff" stroke-opacity=".045" stroke-width="1"/></pattern>
  <filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
  <style>
    .t{font-family:Arial,Helvetica,sans-serif;fill:#f8fafc} .m{font-family:Arial,Helvetica,sans-serif;fill:#94a3b8}
    .tech{font-family:Arial,Helvetica,sans-serif;fill:{accent};letter-spacing:3px}
    .panel{fill:#07111d;fill-opacity:.86;stroke:{accent};stroke-opacity:.42;stroke-width:2}
    .line{stroke:{accent};stroke-width:5;fill:none;stroke-linecap:round;stroke-linejoin:round}
    .thin{stroke:{accent};stroke-width:2;fill:none;stroke-linecap:round}
  </style>
</defs>'''

def common(title, subtitle, accent, scene):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" role="img" aria-label="{title} AI generated visualization">
{DEFS.format(accent=accent)}
<rect width="1600" height="900" fill="url(#bg)"/><rect width="1600" height="900" fill="url(#grid)"/>
<circle cx="1260" cy="160" r="420" fill="url(#halo)"/><circle cx="300" cy="760" r="300" fill="url(#halo)" opacity=".35"/>
<rect x="54" y="48" width="1492" height="804" rx="28" fill="none" stroke="{accent}" stroke-opacity=".17" stroke-width="2"/>
<text x="92" y="126" class="t" font-size="54" font-weight="700">{title}</text>
<text x="96" y="173" class="tech" font-size="19">{subtitle}</text>
<g opacity=".95">{scene}</g>
<g transform="translate(96 812)"><rect width="275" height="36" rx="18" fill="#000" fill-opacity=".55" stroke="{accent}" stroke-opacity=".35"/><text x="20" y="24" class="tech" font-size="12">AI-GENERATED VISUALIZATION</text></g>
</svg>'''

def scene(kind, c):
    if kind == 'dse':
        nodes = ''.join(f'<circle cx="{x}" cy="{y}" r="17" fill="#081827" stroke="{c}" stroke-width="4" filter="url(#glow)"/>' for x,y in [(300,380),(500,300),(690,430),(920,300),(1120,410)])
        links = '<path d="M300 380L500 300L690 430L920 300L1120 410M500 300L920 300M690 430L1120 410" class="line" opacity=".7"/>'
        return f'''<g>{links}{nodes}<rect x="220" y="520" width="350" height="170" rx="22" class="panel"/><text x="252" y="568" class="t" font-size="24">EDGE NODE</text><text x="252" y="610" class="m" font-size="20">Yocto / Buildroot</text><text x="252" y="644" class="m" font-size="20">containerd • BusyBox</text><text x="252" y="678" class="m" font-size="20">ARM Linux</text><rect x="940" y="520" width="390" height="170" rx="22" class="panel"/><text x="972" y="568" class="t" font-size="24">SIGNED A/B OTA</text><rect x="980" y="602" width="110" height="54" rx="10" fill="{c}" fill-opacity=".22" stroke="{c}"/><rect x="1140" y="602" width="110" height="54" rx="10" fill="#7000ff" fill-opacity=".22" stroke="#a855f7"/><text x="1027" y="637" class="t" font-size="20">A</text><text x="1187" y="637" class="t" font-size="20">B</text><path d="M1095 628H1134" class="thin"/><text x="974" y="684" class="m" font-size="18">RAUC • rollback • CI validation</text></g>'''
    if kind == 'competitive':
        return f'''<g transform="translate(150 238)"><rect x="410" y="360" width="560" height="130" rx="28" fill="#0a111b" stroke="{c}" stroke-width="4"/><circle cx="520" cy="500" r="62" fill="#020617" stroke="#64748b" stroke-width="12"/><circle cx="860" cy="500" r="62" fill="#020617" stroke="#64748b" stroke-width="12"/><rect x="530" y="140" width="70" height="250" rx="24" fill="#1f2937" stroke="#94a3b8" stroke-width="5"/><path d="M565 150L780 65L840 120L640 250" class="line"/><circle cx="565" cy="150" r="28" fill="#111827" stroke="{c}" stroke-width="5"/><circle cx="790" cy="68" r="28" fill="#111827" stroke="{c}" stroke-width="5"/><rect x="828" y="88" width="95" height="95" rx="12" fill="#7c3aed" stroke="#c4b5fd" stroke-width="4"/><rect x="60" y="40" width="290" height="230" rx="22" class="panel"/><text x="92" y="88" class="t" font-size="23">CONTROL STACK</text><text x="92" y="134" class="m" font-size="20">PS4 operator input</text><text x="92" y="172" class="m" font-size="20">Raspberry Pi</text><text x="92" y="210" class="m" font-size="20">Arduino actuation</text><text x="92" y="248" class="m" font-size="20">PID / routines</text><rect x="1040" y="85" width="320" height="220" rx="22" class="panel"/><text x="1075" y="132" class="t" font-size="23">COMPETITION MODE</text><text x="1075" y="178" class="m" font-size="20">Integrate mechanisms</text><text x="1075" y="216" class="m" font-size="20">Repeat task cycles</text><text x="1075" y="254" class="m" font-size="20">Prioritize reliability</text></g>'''
    if kind == 'turtlebot':
        return f'''<g transform="translate(90 230)"><path d="M180 500C330 350 430 540 590 370S850 170 1040 300S1210 450 1390 240" class="line" stroke-dasharray="16 18" opacity=".9"/><g transform="translate(490 370)"><ellipse cx="0" cy="90" rx="120" ry="42" fill="#030712" stroke="{c}" stroke-width="5"/><rect x="-95" y="0" width="190" height="95" rx="28" fill="#101827" stroke="#64748b" stroke-width="4"/><circle cx="-112" cy="72" r="34" fill="#020617" stroke="#94a3b8" stroke-width="7"/><circle cx="112" cy="72" r="34" fill="#020617" stroke="#94a3b8" stroke-width="7"/><rect x="-48" y="-38" width="96" height="44" rx="14" fill="#0f172a" stroke="{c}" stroke-width="4"/><circle cx="0" cy="-18" r="13" fill="{c}" filter="url(#glow)"/><circle cx="0" cy="-18" r="130" fill="none" stroke="{c}" stroke-opacity=".22" stroke-width="2"/><circle cx="0" cy="-18" r="205" fill="none" stroke="{c}" stroke-opacity=".12" stroke-width="2"/></g><rect x="865" y="20" width="450" height="230" rx="22" class="panel"/><text x="900" y="66" class="t" font-size="24">NAVIGATION PIPELINE</text><text x="900" y="111" class="m" font-size="20">SLAM map → AMCL pose</text><text x="900" y="150" class="m" font-size="20">Nav2 planner / controller</text><text x="900" y="189" class="m" font-size="20">TF2 + odometry checks</text><text x="900" y="228" class="m" font-size="20">Simulation → hardware</text><g opacity=".5"><rect x="60" y="30" width="240" height="180" rx="18" fill="#111827" stroke="#64748b"/><rect x="90" y="70" width="55" height="55" fill="#334155"/><rect x="205" y="115" width="65" height="65" fill="#334155"/><path d="M115 175L235 75" class="thin"/></g></g>'''
    if kind == 'ur10':
        return f'''<g transform="translate(120 220)"><rect x="90" y="470" width="650" height="55" rx="18" fill="#111827" stroke="#475569" stroke-width="4"/><g stroke-linecap="round"><path d="M390 450L390 320" stroke="#cbd5e1" stroke-width="54"/><circle cx="390" cy="320" r="43" fill="#1e293b" stroke="{c}" stroke-width="5"/><path d="M390 320L555 185" stroke="#cbd5e1" stroke-width="58"/><circle cx="555" cy="185" r="43" fill="#1e293b" stroke="{c}" stroke-width="5"/><path d="M555 185L760 280" stroke="#cbd5e1" stroke-width="55"/><circle cx="760" cy="280" r="40" fill="#1e293b" stroke="{c}" stroke-width="5"/><path d="M760 280L830 390" stroke="#cbd5e1" stroke-width="42"/></g><path d="M830 390C945 315 1025 255 1125 220" class="line" stroke-dasharray="14 16" opacity=".75"/><circle cx="1125" cy="220" r="13" fill="{c}" filter="url(#glow)"/><rect x="930" y="350" width="440" height="210" rx="22" class="panel"/><text x="966" y="395" class="t" font-size="24">CONTROL WORKFLOW</text><text x="966" y="440" class="m" font-size="20">FK / IK</text><text x="966" y="477" class="m" font-size="20">Damped Least Squares</text><text x="966" y="514" class="m" font-size="20">JointTrajectory messages</text><text x="966" y="551" class="m" font-size="20">Simulation → real UR10</text></g>'''
    if kind == 'iiot':
        bars=''.join(f'<rect x="{x}" y="{590-h}" width="28" height="{h}" rx="5" fill="{c}" opacity="{.35+i*.06}"/>' for i,(x,h) in enumerate([(880,80),(920,120),(960,95),(1000,165),(1040,115),(1080,210),(1120,130),(1160,185)]))
        return f'''<g><g transform="translate(110 280)"><rect x="40" y="180" width="520" height="300" rx="28" fill="#0a111b" stroke="#475569" stroke-width="4"/><circle cx="300" cy="330" r="108" fill="#111827" stroke="{c}" stroke-width="5"/><circle cx="300" cy="330" r="52" fill="#020617" stroke="#94a3b8" stroke-width="7"/><path d="M300 190V125M300 470V535M160 330H95M440 330H505" class="line" opacity=".45"/><text x="90" y="220" class="t" font-size="23">INDUSTRIAL SENSOR STREAM</text><text x="90" y="455" class="m" font-size="18">temperature • vibration • current</text></g><rect x="760" y="230" width="690" height="430" rx="28" class="panel"/><text x="805" y="282" class="t" font-size="26">LIVE ANOMALY MONITOR</text><path d="M820 470C865 455 900 480 940 435S1010 520 1060 390S1130 500 1190 425S1280 455 1380 335" class="line"/><circle cx="1060" cy="390" r="12" fill="#fb7185" filter="url(#glow)"/><circle cx="1380" cy="335" r="12" fill="#fb7185" filter="url(#glow)"/>{bars}<text x="805" y="635" class="m" font-size="20">MQTT → Python → Isolation Forest → Plotly</text></g>'''
    if kind == 'face':
        pts=[(620,290),(560,350),(680,350),(535,430),(705,430),(575,510),(665,510),(620,560),(620,420),(585,400),(655,400)]
        lines=[(0,1),(0,2),(1,3),(2,4),(3,5),(4,6),(5,7),(6,7),(1,8),(2,8),(8,9),(8,10),(9,5),(10,6)]
        mesh=''.join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" class="thin" opacity=".55"/>' for a,b in lines)+''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>' for x,y in pts)
        return f'''<g><rect x="160" y="235" width="930" height="490" rx="34" fill="#07111d" stroke="#475569" stroke-width="4"/><rect x="200" y="275" width="840" height="410" rx="24" fill="#020617" stroke="{c}" stroke-opacity=".45"/><ellipse cx="620" cy="430" rx="145" ry="190" fill="#0f172a" stroke="#64748b" stroke-width="4"/>{mesh}<path d="M455 270h-70v70M785 270h70v70M455 590h-70v-70M785 590h70v-70" class="line"/><rect x="1145" y="290" width="300" height="300" rx="24" class="panel"/><text x="1180" y="338" class="t" font-size="24">LOCAL PIPELINE</text><text x="1180" y="388" class="m" font-size="20">Detect + align</text><text x="1180" y="428" class="m" font-size="20">Pose validation</text><text x="1180" y="468" class="m" font-size="20">Embedding</text><text x="1180" y="508" class="m" font-size="20">Offline matching</text><text x="1180" y="555" class="tech" font-size="16">NO CLOUD API</text></g>'''
    if kind == 'rst':
        return f'''<g transform="translate(95 210)"><rect x="120" y="470" width="460" height="90" rx="22" fill="#0a111b" stroke="#475569" stroke-width="4"/><path d="M300 450L300 345L410 245L530 310" stroke="#cbd5e1" stroke-width="34" fill="none" stroke-linecap="round"/><circle cx="300" cy="345" r="28" fill="#111827" stroke="{c}" stroke-width="4"/><circle cx="410" cy="245" r="28" fill="#111827" stroke="{c}" stroke-width="4"/><circle cx="530" cy="310" r="24" fill="#111827" stroke="{c}" stroke-width="4"/><path d="M555 300Q810 70 1125 245" class="line" stroke-dasharray="14 15"/><circle cx="555" cy="300" r="18" fill="#38bdf8" filter="url(#glow)"/><circle cx="1125" cy="245" r="18" fill="#38bdf8" filter="url(#glow)"/><rect x="1150" y="100" width="210" height="300" rx="22" fill="#07111d" stroke="{c}" stroke-width="4"/><circle cx="1255" cy="250" r="68" fill="none" stroke="{c}" stroke-width="14"/><rect x="675" y="380" width="430" height="190" rx="22" class="panel"/><text x="712" y="425" class="t" font-size="23">PERCEPTION → ACTION</text><text x="712" y="468" class="m" font-size="19">vision tracking</text><text x="712" y="503" class="m" font-size="19">coordinate transforms</text><text x="712" y="538" class="m" font-size="19">robust throw strategy</text></g>'''
    if kind == 'so101':
        return f'''<g transform="translate(90 220)"><rect x="120" y="500" width="650" height="45" rx="14" fill="#111827" stroke="#475569"/><path d="M390 490L390 365L520 270L645 355" stroke="#e2e8f0" stroke-width="34" fill="none" stroke-linecap="round"/><circle cx="390" cy="365" r="27" fill="#111827" stroke="{c}" stroke-width="4"/><circle cx="520" cy="270" r="27" fill="#111827" stroke="{c}" stroke-width="4"/><circle cx="645" cy="355" r="24" fill="#111827" stroke="{c}" stroke-width="4"/><rect x="637" y="380" width="54" height="54" rx="8" fill="#2563eb"/><rect x="250" y="420" width="54" height="54" rx="8" fill="#ef4444"/><rect x="320" y="420" width="54" height="54" rx="8" fill="#22c55e"/><rect x="790" y="65" width="210" height="175" rx="20" class="panel"/><rect x="1015" y="65" width="210" height="175" rx="20" class="panel"/><rect x="1240" y="65" width="210" height="175" rx="20" class="panel"/><text x="825" y="110" class="t" font-size="22">ZERO-SHOT</text><text x="1045" y="110" class="t" font-size="22">FEW-SHOT</text><text x="1270" y="110" class="t" font-size="22">IN-CONTEXT</text><text x="822" y="156" class="m" font-size="17">No demos</text><text x="1045" y="156" class="m" font-size="17">Few examples</text><text x="1270" y="156" class="m" font-size="17">Task context</text><text x="822" y="200" class="tech" font-size="13">COMPARE FAIRLY</text><text x="1045" y="200" class="tech" font-size="13">SAME TASK</text><text x="1270" y="200" class="tech" font-size="13">LOG RESULTS</text></g>'''
    if kind == 'jj':
        return f'''<g transform="translate(110 225)"><rect x="100" y="470" width="610" height="55" rx="16" fill="#111827" stroke="#475569" stroke-width="4"/><path d="M350 450L350 320L490 205L650 290" stroke="#e2e8f0" stroke-width="40" fill="none" stroke-linecap="round"/><circle cx="350" cy="320" r="31" fill="#111827" stroke="{c}" stroke-width="5"/><circle cx="490" cy="205" r="31" fill="#111827" stroke="{c}" stroke-width="5"/><circle cx="650" cy="290" r="28" fill="#111827" stroke="{c}" stroke-width="5"/><rect x="815" y="50" width="520" height="210" rx="22" class="panel"/><text x="852" y="98" class="t" font-size="24">CONTROL VALIDATION</text><path d="M855 210C910 195 945 180 990 202S1060 150 1115 180S1200 125 1290 155" class="line"/><text x="852" y="145" class="m" font-size="18">measure → modify → retest</text><rect x="815" y="300" width="520" height="250" rx="22" class="panel"/><text x="852" y="348" class="t" font-size="24">PYTHON TROUBLESHOOTING</text><text x="852" y="397" class="m" font-size="19">command response timing</text><text x="852" y="436" class="m" font-size="19">iterative code review</text><text x="852" y="475" class="m" font-size="19">before / after validation</text><text x="852" y="514" class="m" font-size="19">engineering documentation</text></g>'''
    return ''

for slug,(title,subtitle,accent,kind) in PROJECTS.items():
    (ASSET_DIR / f'{slug}.svg').write_text(common(title, subtitle, accent, scene(kind, accent)), encoding='utf-8')

index = ROOT / 'index.html'
if index.exists():
    s = index.read_text(encoding='utf-8')
    for slug in PROJECTS:
        s = s.replace(f"assets/ai/{slug}.webp", f"assets/ai/{slug}.svg")
    s = s.replace('opacity-60 group-hover:opacity-40 transition-opacity duration-500', 'opacity-100 group-hover:opacity-95 transition-opacity duration-500')
    a = s.find('<!-- Projects Section -->')
    b = s.find('<!-- Contact Section -->', a)
    if a != -1:
        if b == -1: b = len(s)
        chunk = s[a:b]
        chunk = chunk.replace('opacity-80"></div>', 'opacity-25"></div>')
        chunk = re.sub(r'(text-6xl\s+[^\"]*?/)(50)(\s+group-hover)', r'\g<1>30\g<3>', chunk)
        s = s[:a] + chunk + s[b:]
    index.write_text(s, encoding='utf-8')

for folder in [ROOT/'project', ROOT/'experience']:
    if not folder.exists():
        continue
    for p in folder.glob('*.html'):
        s = p.read_text(encoding='utf-8')
        for slug in PROJECTS:
            s = s.replace(f"../assets/ai/{slug}.webp", f"../assets/ai/{slug}.svg")
        p.write_text(s, encoding='utf-8')

css = ROOT / 'project-detail.css'
if css.exists():
    c = css.read_text(encoding='utf-8')
    c += '''\n.project-visual{height:clamp(280px,52vw,560px);background-size:cover!important;background-position:center!important;background-repeat:no-repeat!important;border:1px solid rgba(0,240,255,.22);box-shadow:0 18px 70px rgba(0,0,0,.45);image-rendering:auto;overflow:hidden}.project-visual:after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.12),transparent 42%);pointer-events:none}.ai-badge{opacity:.88!important;background:rgba(0,0,0,.66)!important;backdrop-filter:blur(6px)}\n'''
    css.write_text(c, encoding='utf-8')

print('HD vector visuals generated and website media treatment updated.')

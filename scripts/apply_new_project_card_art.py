from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "project"
INDEX = ROOT / "index.html"
PROJECT_DIR = ROOT / "project"
ASSET_DIR.mkdir(parents=True, exist_ok=True)


def shell(title, accent, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#050914"/><stop offset=".55" stop-color="#0b1627"/><stop offset="1" stop-color="#09111d"/></linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#182535"/><stop offset="1" stop-color="#05080d"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#132a42" stop-opacity=".94"/><stop offset="1" stop-color="#07121f" stop-opacity=".9"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="{accent}" stop-opacity=".45"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="shadow"><feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#000" flood-opacity=".65"/></filter>
</defs>
<rect width="1600" height="900" fill="url(#bg)"/>
<circle cx="1280" cy="120" r="360" fill="url(#glow)" opacity=".35"/>
<text x="70" y="84" fill="{accent}" font-family="monospace" font-size="18" letter-spacing="4">HD PROJECT ILLUSTRATION</text>
<text x="70" y="132" fill="#e8f5ff" font-family="monospace" font-size="34" font-weight="700">{title}</text>
{body}
</svg>'''


inspection = shell("AUTONOMOUS INDUSTRIAL INSPECTION", "#f59e0b", r'''
<!-- factory depth -->
<rect x="0" y="180" width="1600" height="720" fill="#0a111a"/>
<path d="M0 570 L800 365 L1600 570 L1600 900 L0 900Z" fill="url(#floor)"/>
<g opacity=".7" stroke="#334155" stroke-width="5"><path d="M100 190V650M250 190V610M1430 190V650M1290 190V610"/><path d="M0 250H1600M0 355H1600"/></g>
<!-- pipes and plant -->
<g fill="#263746" stroke="#475569" stroke-width="4"><rect x="80" y="220" width="120" height="350" rx="28"/><rect x="1320" y="210" width="130" height="370" rx="30"/><rect x="1180" y="300" width="260" height="70" rx="32"/></g>
<g stroke="#f59e0b" stroke-width="10" opacity=".6"><path d="M210 320H420V210H610"/><path d="M1180 510H1370V420"/></g>
<!-- glowing patrol route -->
<path d="M520 760 C700 650 820 800 980 665 S1260 715 1370 600" fill="none" stroke="#38bdf8" stroke-width="8" stroke-dasharray="18 16" opacity=".9"/>
<g fill="#0b1220" stroke="#38bdf8" stroke-width="6"><circle cx="590" cy="718" r="18"/><circle cx="835" cy="724" r="18"/><circle cx="1080" cy="640" r="18"/><circle cx="1330" cy="620" r="18"/></g>
<!-- robot -->
<g transform="translate(360 430)" filter="url(#shadow)"><ellipse cx="215" cy="300" rx="230" ry="38" fill="#000" opacity=".5"/><rect x="65" y="170" width="300" height="155" rx="42" fill="#dce7ef" stroke="#7dd3fc" stroke-width="5"/><rect x="100" y="240" width="230" height="70" rx="20" fill="#111827"/><rect x="188" y="25" width="55" height="160" rx="18" fill="#1f2937"/><rect x="135" y="15" width="160" height="58" rx="18" fill="#d8e5ee" stroke="#67e8f9" stroke-width="4"/><circle cx="178" cy="44" r="15" fill="#020617" stroke="#38bdf8" stroke-width="5"/><circle cx="252" cy="44" r="15" fill="#020617" stroke="#38bdf8" stroke-width="5"/><rect x="158" y="-18" width="114" height="28" rx="13" fill="#111827" stroke="#38bdf8" stroke-width="4"/><circle cx="105" cy="325" r="54" fill="#05080d" stroke="#475569" stroke-width="14"/><circle cx="325" cy="325" r="54" fill="#05080d" stroke="#475569" stroke-width="14"/><rect x="130" y="268" width="170" height="9" rx="5" fill="#38bdf8"/></g>
<!-- floating inspection panels -->
<g filter="url(#shadow)" font-family="monospace"><rect x="820" y="205" width="270" height="160" rx="18" fill="url(#glass)" stroke="#fb7185" stroke-width="3"/><text x="850" y="245" fill="#fda4af" font-size="18">THERMAL CHECK</text><rect x="850" y="268" width="90" height="62" rx="10" fill="#7c2d12"/><circle cx="895" cy="299" r="27" fill="#fb923c"/><text x="965" y="307" fill="#fff" font-size="26">42.6°C</text><circle cx="1047" cy="330" r="14" fill="#22c55e"/>
<rect x="1110" y="205" width="320" height="160" rx="18" fill="url(#glass)" stroke="#38bdf8" stroke-width="3"/><text x="1140" y="245" fill="#7dd3fc" font-size="18">VISUAL + ACOUSTIC</text><path d="M1145 300 H1170 L1185 270 L1202 330 L1225 288 L1244 318 L1268 275 L1288 322 L1312 290 L1350 300" fill="none" stroke="#22d3ee" stroke-width="4"/><text x="1140" y="344" fill="#94a3b8" font-size="14">evidence captured • anomaly scored</text>
<rect x="820" y="385" width="610" height="155" rx="18" fill="url(#glass)" stroke="#22c55e" stroke-width="3"/><text x="850" y="425" fill="#86efac" font-size="18">MISSION STATUS</text><text x="850" y="463" fill="#e2e8f0" font-size="16">NAV2 ✓   CAMERA ✓   THERMAL ✓   REPORT ✓</text><text x="850" y="502" fill="#94a3b8" font-size="15">checkpoint evidence → follow-up decision → report</text></g>
''')

fleet = shell("ROBOT FLEET OBSERVABILITY PLATFORM", "#22d3ee", r'''
<!-- command centre -->
<rect x="55" y="175" width="1490" height="650" rx="34" fill="#050b14" stroke="#1e3a5f" stroke-width="4"/>
<rect x="470" y="210" width="1010" height="435" rx="22" fill="#071522" stroke="#22d3ee" stroke-width="3"/>
<!-- top pipeline -->
<g font-family="monospace" font-size="24" font-weight="700"><text x="530" y="262" fill="#67e8f9">FastAPI</text><text x="720" y="262" fill="#64748b">→</text><text x="795" y="262" fill="#38bdf8">InfluxDB</text><text x="1035" y="262" fill="#64748b">→</text><text x="1110" y="262" fill="#fb923c">Grafana</text></g>
<!-- fleet map -->
<rect x="710" y="295" width="455" height="285" rx="18" fill="#0b1b2c" stroke="#1e40af" stroke-width="2"/><g stroke="#164e63" stroke-width="2" opacity=".8"><path d="M750 350H1118M750 405H1118M750 460H1118M750 515H1118M810 320V555M890 320V555M970 320V555M1050 320V555"/></g><path d="M770 505 C835 455 865 470 930 405 S1030 395 1110 340" fill="none" stroke="#38bdf8" stroke-width="5"/>
<g fill="#e2e8f0" stroke="#22d3ee" stroke-width="4"><rect x="792" y="474" width="38" height="26" rx="8"/><rect x="900" y="412" width="38" height="26" rx="8"/><rect x="1015" y="383" width="38" height="26" rx="8"/><rect x="1082" y="330" width="38" height="26" rx="8"/></g><circle cx="947" cy="447" r="19" fill="#ef4444"/><text x="947" y="453" text-anchor="middle" fill="#fff" font-family="monospace" font-size="20">!</text>
<!-- KPI cards -->
<g font-family="monospace"><rect x="500" y="295" width="180" height="120" rx="16" fill="#0b1b2c" stroke="#155e75"/><text x="525" y="330" fill="#94a3b8" font-size="15">ACTIVE</text><text x="525" y="385" fill="#67e8f9" font-size="44">24</text><rect x="500" y="435" width="180" height="145" rx="16" fill="#0b1b2c" stroke="#155e75"/><text x="525" y="470" fill="#94a3b8" font-size="15">UPTIME</text><text x="525" y="520" fill="#86efac" font-size="38">89%</text><path d="M525 550 L548 528 L570 542 L595 510 L620 527 L652 500" fill="none" stroke="#22c55e" stroke-width="4"/>
<rect x="1190" y="295" width="255" height="285" rx="16" fill="#0b1b2c" stroke="#155e75"/><text x="1215" y="330" fill="#94a3b8" font-size="15">ALERTS & EVENTS</text><text x="1215" y="375" fill="#f87171" font-size="15">▲ R-003  low battery</text><text x="1215" y="415" fill="#fbbf24" font-size="15">▲ R-017  waypoint stall</text><text x="1215" y="455" fill="#fbbf24" font-size="15">▲ R-021  obstacle</text><text x="1215" y="510" fill="#94a3b8" font-size="14">tenant-scoped fault history</text></g>
<!-- workstations -->
<g transform="translate(105 250)" filter="url(#shadow)"><rect x="0" y="0" width="310" height="190" rx="18" fill="#0a1725" stroke="#22d3ee" stroke-width="3"/><rect x="22" y="22" width="266" height="110" rx="10" fill="#06111d"/><g stroke="#22d3ee" stroke-width="3" fill="none"><path d="M40 103 L75 77 L110 92 L145 55 L178 75 L215 43 L265 67"/></g><text x="25" y="165" fill="#67e8f9" font-family="monospace" font-size="18">FLEET OPS</text></g>
<!-- warehouse robots -->
<g transform="translate(120 560)" fill="#dce7ef" stroke="#38bdf8" stroke-width="4"><g><rect x="0" y="0" width="115" height="60" rx="20"/><circle cx="25" cy="62" r="20" fill="#05080d"/><circle cx="92" cy="62" r="20" fill="#05080d"/></g><g transform="translate(160 35)"><rect width="115" height="60" rx="20"/><circle cx="25" cy="62" r="20" fill="#05080d"/><circle cx="92" cy="62" r="20" fill="#05080d"/></g></g>
<!-- bottom monitors -->
<g><rect x="470" y="675" width="300" height="105" rx="16" fill="#071522" stroke="#1e40af"/><rect x="790" y="675" width="300" height="105" rx="16" fill="#071522" stroke="#1e40af"/><rect x="1110" y="675" width="300" height="105" rx="16" fill="#071522" stroke="#1e40af"/><path d="M500 740H735" stroke="#22d3ee" stroke-width="4" stroke-dasharray="10 10"/><path d="M820 746 L850 720 L890 735 L925 705 L970 730 L1035 700" fill="none" stroke="#a78bfa" stroke-width="4"/><g fill="#38bdf8"><rect x="1140" y="735" width="24" height="25"/><rect x="1175" y="710" width="24" height="50"/><rect x="1210" y="725" width="24" height="35"/><rect x="1245" y="690" width="24" height="70"/><rect x="1280" y="715" width="24" height="45"/><rect x="1315" y="700" width="24" height="60"/></g></g>
''')

operations = shell("INDUSTRIAL ROBOT OPERATIONS INTELLIGENCE", "#a78bfa", r'''
<!-- split industrial + operations scene -->
<rect x="0" y="180" width="610" height="720" fill="#0b121a"/><rect x="610" y="180" width="990" height="720" fill="#07101d"/>
<!-- factory columns/pipes -->
<g stroke="#475569" stroke-width="8" opacity=".8"><path d="M90 200V720M510 200V720"/><path d="M80 280H540M80 390H540"/></g><g fill="#263746" stroke="#64748b" stroke-width="3"><rect x="100" y="230" width="110" height="330" rx="24"/><rect x="430" y="240" width="100" height="310" rx="24"/></g>
<!-- robot -->
<g transform="translate(160 475)" filter="url(#shadow)"><ellipse cx="160" cy="245" rx="180" ry="30" fill="#000" opacity=".5"/><rect x="35" y="110" width="250" height="120" rx="36" fill="#dbe7ef" stroke="#a78bfa" stroke-width="5"/><rect x="128" y="5" width="45" height="115" rx="14" fill="#1f2937"/><rect x="80" y="0" width="140" height="46" rx="16" fill="#dbe7ef"/><circle cx="120" cy="23" r="13" fill="#020617" stroke="#38bdf8" stroke-width="4"/><circle cx="180" cy="23" r="13" fill="#020617" stroke="#38bdf8" stroke-width="4"/><circle cx="80" cy="228" r="44" fill="#05080d" stroke="#475569" stroke-width="12"/><circle cx="245" cy="228" r="44" fill="#05080d" stroke="#475569" stroke-width="12"/><rect x="92" y="172" width="140" height="8" fill="#38bdf8"/></g>
<!-- thermal evidence panel -->
<g font-family="monospace" filter="url(#shadow)"><rect x="65" y="610" width="480" height="175" rx="20" fill="url(#glass)" stroke="#fb7185" stroke-width="3"/><text x="95" y="650" fill="#fda4af" font-size="18">INSPECTION EVIDENCE</text><rect x="95" y="675" width="120" height="75" rx="10" fill="#7c2d12"/><circle cx="155" cy="713" r="28" fill="#fb923c"/><text x="240" y="702" fill="#e2e8f0" font-size="15">asset P-101</text><text x="240" y="730" fill="#f87171" font-size="15">thermal anomaly</text></g>
<!-- large operations console -->
<g font-family="monospace"><rect x="650" y="215" width="900" height="575" rx="24" fill="#071522" stroke="#a78bfa" stroke-width="3"/><text x="695" y="265" fill="#c4b5fd" font-size="20">OPERATIONS INTELLIGENCE</text>
<!-- plant map --> <rect x="690" y="300" width="420" height="270" rx="16" fill="#0b1b2c" stroke="#4c1d95"/><g stroke="#334155" stroke-width="2"><path d="M730 340H1070M730 390H1070M730 440H1070M730 490H1070M780 320V550M850 320V550M920 320V550M990 320V550"/></g><path d="M735 515 C820 470 810 420 890 400 S995 390 1060 350" fill="none" stroke="#22d3ee" stroke-width="5"/><g fill="#22c55e"><circle cx="800" cy="468" r="14"/><circle cx="890" cy="400" r="14"/></g><circle cx="995" cy="390" r="18" fill="#ef4444"/><text x="995" y="397" fill="#fff" text-anchor="middle" font-size="20">!</text>
<!-- incident timeline --> <rect x="1140" y="300" width="365" height="270" rx="16" fill="#0b1b2c" stroke="#4c1d95"/><text x="1170" y="340" fill="#94a3b8" font-size="15">INCIDENT TIMELINE</text><path d="M1185 390V520" stroke="#64748b" stroke-width="5"/><g><circle cx="1185" cy="400" r="12" fill="#22c55e"/><circle cx="1185" cy="445" r="12" fill="#f59e0b"/><circle cx="1185" cy="490" r="12" fill="#ef4444"/></g><text x="1220" y="405" fill="#cbd5e1" font-size="14">robot event</text><text x="1220" y="450" fill="#cbd5e1" font-size="14">network delay</text><text x="1220" y="495" fill="#cbd5e1" font-size="14">inspection fault</text>
<!-- bottom cards --> <rect x="690" y="600" width="250" height="145" rx="16" fill="#0b1b2c" stroke="#312e81"/><text x="720" y="638" fill="#94a3b8" font-size="15">EVIDENCE</text><text x="720" y="680" fill="#86efac" font-size="15">✓ supporting</text><text x="720" y="710" fill="#fda4af" font-size="15">× contradicting</text><rect x="965" y="600" width="250" height="145" rx="16" fill="#0b1b2c" stroke="#312e81"/><text x="995" y="638" fill="#94a3b8" font-size="15">HYPOTHESES</text><text x="995" y="680" fill="#e2e8f0" font-size="14">confidence + provenance</text><rect x="1240" y="600" width="265" height="145" rx="16" fill="#0b1b2c" stroke="#312e81"/><text x="1270" y="638" fill="#94a3b8" font-size="15">HUMAN REVIEW</text><text x="1270" y="680" fill="#c4b5fd" font-size="14">approve → report</text></g>
''')

assets = {
    "industrial-inspection-system.svg": inspection,
    "fleet-observability-system.svg": fleet,
    "operations-intelligence-system.svg": operations,
}
for name, svg in assets.items():
    (ASSET_DIR / name).write_text(svg, encoding="utf-8")

# Update the badges on the three cards/detail pages while preserving all existing routing.
if INDEX.exists():
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace(">SYSTEM VISUAL<", ">HD ILLUSTRATION<")
    INDEX.write_text(text, encoding="utf-8")

for slug in ("autonomous-industrial-inspection-robot", "robot-fleet-observability-platform", "industrial-robot-operations-intelligence"):
    path = PROJECT_DIR / f"{slug}.html"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace("REPOSITORY-DERIVED SYSTEM VISUALIZATION", "HD PROJECT ILLUSTRATION")
        path.write_text(text, encoding="utf-8")

print("Applied 1600x900 HD project illustrations to the three new industrial project cards and detail heroes.")

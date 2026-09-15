from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
PROJECT_DIR = ROOT / "project"
ASSET_DIR = ROOT / "assets" / "project"

PROJECTS = [
    {
        "title": "Autonomous Industrial Inspection Robot",
        "card": "Autonomous Industrial Inspection",
        "slug": "autonomous-industrial-inspection-robot",
        "repo": "https://github.com/SAMP2411/autonomous-industrial-inspection-robot",
        "accent": "#f59e0b",
        "hover": "yellow-400",
        "icon": "fa-industry",
        "status": "Independent Engineering Project · Public release Sep 2026",
        "stack": "ROS 2 Jazzy · Nav2 · Gazebo Harmonic · C++17 · Python · OpenCV · pluginlib · yaml-cpp",
        "tags": "ROS2 JAZZY • NAV2 • GAZEBO • C++",
        "summary": "Built a deterministic ROS 2 inspection patrol with Nav2 waypoint execution, custom inspection messages, evidence capture, follow-up logic and regression tooling.",
        "challenge": "Industrial patrol automation needs more than successful navigation. Every checkpoint must preserve what was inspected, the evidence that was captured, how an anomaly was classified and what the mission should do next when captures or inspections fail.",
        "implementation": "Implemented ROS 2 Jazzy packages for an industrial inspection mission around a TurtleBot 4 simulation. The repository defines custom InspectionResult and PatrolRoundSummary messages, configuration-driven sites/assets/checkpoints and inspection profiles, a Nav2 waypoint task-executor plugin, and synthetic visual, thermal, acoustic and gauge-style inspection modes. The mission produces raw and annotated evidence together with health score, severity, confidence and diagnostic fields.",
        "architecture": "Site / asset / checkpoint configuration → Gazebo Harmonic + ROS 2 → Nav2 waypoint navigation → inspection-at-waypoint plugin → evidence + InspectionResult messages → mission aggregation → JSON / CSV / Markdown / HTML reports → continue / targeted follow-up / watchlist / safety hold.",
        "validation": "The repository includes clean colcon build/test instructions, a headless smoke test, runtime cleanup and retry wrappers, a full benchmark path and multi-seed regression tooling. Seeded scenarios make failures reproducible; visual verification uses Gazebo and RViz to inspect maps, transforms, plans and robot state.",
        "decisions": "The design favors deterministic, auditable behavior over opaque autonomy. Scenario seeds, evidence paths, severity rules, retry limits and mission decisions are explicit and configurable. The repository also clearly limits the work to simulation and documents the additional safety integration required before physical deployment.",
        "visual": "industrial-inspection-system.svg",
        "visual_kind": "inspection",
    },
    {
        "title": "Robot Fleet Observability Platform",
        "card": "Robot Fleet Observability",
        "slug": "robot-fleet-observability-platform",
        "repo": "https://github.com/SAMP2411/robot-fleet-observability-platform",
        "accent": "#22d3ee",
        "hover": "cyan-300",
        "icon": "fa-chart-line",
        "status": "Independent Engineering Project · Public release Sep 2026",
        "stack": "Python · FastAPI · InfluxDB 2.x · Flux · JWT · Grafana · HTML/CSS/JavaScript · Docker",
        "tags": "FASTAPI • INFLUXDB • JWT • GRAFANA",
        "summary": "Built a tenant-aware AMR monitoring backend with time-series telemetry, fleet KPIs, fault history, secured ingestion and a five-robot simulator.",
        "challenge": "Operations teams need fleet-level visibility rather than separate robot logs. The service therefore has to authenticate operators, isolate tenant data, ingest robot telemetry safely and turn time-series measurements into useful fleet-level health and fault views.",
        "implementation": "Built a FastAPI service with JWT operator authentication and separate API-key protection for telemetry producers. Robot status, battery, odometry, task, uptime and fault measurements are written to InfluxDB 2.x and queried through tenant-scoped Flux expressions. The project includes a browser dashboard, OpenAPI endpoints, an importable Grafana definition and a simulator that continuously publishes five AMRs.",
        "architecture": "AMRs / five-robot simulator → X-API-Key + X-Tenant-ID ingestion → FastAPI → InfluxDB time-series storage → tenant-scoped fleet API → built-in operator dashboard / OpenAPI clients / optional Grafana dashboard.",
        "validation": "The documented end-to-end procedure checks API/database health, authentication, protected fleet queries, HTTP 401 behavior, direct telemetry ingestion and browser-dashboard population. The health endpoint distinguishes a running API from a degraded database connection.",
        "decisions": "The project deliberately keeps user and tenant registration in process memory and calls that out as a development boundary rather than pretending it is production-ready. The documentation identifies the next production steps: persistent identity storage, separate revocable producer credentials, token rotation, rate limiting, audit events and backups.",
        "visual": "fleet-observability-system.svg",
        "visual_kind": "fleet",
    },
    {
        "title": "Industrial Robot Operations Intelligence",
        "card": "Industrial Robot Operations Intelligence",
        "slug": "industrial-robot-operations-intelligence",
        "repo": "https://github.com/SAMP2411/industrial-robot-operations-intelligence",
        "accent": "#a78bfa",
        "hover": "purple-300",
        "icon": "fa-diagram-project",
        "status": "Integration Capstone · Public release Sep 2026",
        "stack": "ROS 2 Jazzy · Nav2 · FastAPI · SQLAlchemy · PostgreSQL · Alembic · Docker Compose · Pytest · Caddy",
        "tags": "ROS2 • FASTAPI • POSTGRES • INCIDENT DIAGNOSTICS",
        "summary": "Integrated autonomous inspection, operator finding workflows and cross-system incident diagnostics into one auditable industrial robotics platform.",
        "challenge": "A robot anomaly rarely lives in one log. Navigation and inspection evidence may need to be reconciled with fleet, WMS/WCS, PLC, network, charger, ticket and maintenance records before an operator can understand impact, recovery and likely causes.",
        "implementation": "Integrated the autonomous inspection stack with a FleetWatch operator workflow and a separate historical incident-intelligence service. FleetWatch imports benchmark reports, campaign state and evidence into persistent site/asset/mission/finding records. The diagnostic service ingests CSV, JSON, JSONL, structured logs, ROS exports and other supported files through preview-before-commit flows, then normalizes events, aligns timelines, maps assets, calculates incident/recovery context, links hypotheses to evidence and generates reviewable reports.",
        "architecture": "Live path: ROS 2 inspection → reports / evidence / campaign state → FleetWatch sync → operator acknowledge / assign / reinspect / resolve / close → follow-up mission queue. Historical path: robot / WMS / WCS / PLC / network / maintenance exports → safe preview + commit → immutable source records → normalization + asset mapping → aligned timeline → incident metrics + evidence-linked hypotheses → human-reviewed reports.",
        "validation": "The repository contains CI workflows plus contract, integration, end-to-end, browser, migration, fault-injection, parser-fuzz, property, performance, PostgreSQL, release and security tests. It also includes backup/restore tooling, migration history and release-gate checks. These are treated as validation surfaces in the portfolio, not as unsupported claims that every environment will pass unchanged.",
        "decisions": "The diagnostic subsystem is intentionally read-only with respect to robots and industrial control systems. Source files retain SHA-256 provenance, ingestion uses a preview-before-commit boundary, hypotheses can carry supporting or contradicting evidence, and human review remains explicit instead of allowing the system to present unverified root-cause claims as facts.",
        "visual": "operations-intelligence-system.svg",
        "visual_kind": "operations",
    },
]


def esc(value):
    return html.escape(str(value), quote=True)


def write_svg(project):
    accent = project["accent"]
    kind = project["visual_kind"]
    if kind == "inspection":
        boxes = [
            (95, 315, 255, 125, "SITE CONFIG", "assets • checkpoints"),
            (420, 315, 255, 125, "ROS 2 + GAZEBO", "TurtleBot 4 simulation"),
            (745, 315, 255, 125, "NAV2 PATROL", "waypoints • recovery"),
            (1070, 315, 255, 125, "INSPECTION", "visual • thermal • gauge"),
            (1395, 315, 115, 125, "REPORT", "evidence"),
        ]
        footer = "SEED → NAVIGATE → INSPECT → PRESERVE EVIDENCE → DECIDE"
    elif kind == "fleet":
        boxes = [
            (90, 315, 250, 125, "5 AMRs", "status • battery • pose"),
            (405, 315, 255, 125, "FASTAPI INGEST", "API key + tenant"),
            (725, 315, 255, 125, "INFLUXDB", "time-series telemetry"),
            (1045, 315, 255, 125, "FLEET API", "JWT • tenant scope"),
            (1365, 315, 145, 125, "OPS UI", "Grafana"),
        ]
        footer = "TELEMETRY → DURABLE TIME SERIES → TENANT-SCOPED OPERATIONS VIEW"
    else:
        boxes = [
            (90, 230, 300, 120, "ROS INSPECTION", "missions • evidence"),
            (490, 230, 300, 120, "FLEETWATCH", "findings • follow-up"),
            (890, 230, 300, 120, "INCIDENT ENGINE", "timeline • recovery"),
            (1290, 230, 220, 120, "REPORTS", "review + export"),
            (90, 535, 300, 120, "ROBOT / WMS / PLC", "network • tickets"),
            (490, 535, 300, 120, "SAFE INGESTION", "preview • provenance"),
            (890, 535, 300, 120, "EVIDENCE", "support • contradict"),
            (1290, 535, 220, 120, "HUMAN REVIEW", "approve claims"),
        ]
        footer = "LIVE ROBOT OPERATIONS + HISTORICAL INCIDENT DIAGNOSTICS"

    elements = []
    for x, y, w, h, title, sub in boxes:
        elements.append(f'''<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#0b1320" stroke="{accent}" stroke-width="2"/><text x="{x+w/2}" y="{y+48}" text-anchor="middle" fill="#ffffff" font-family="monospace" font-size="22" font-weight="700">{esc(title)}</text><text x="{x+w/2}" y="{y+82}" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="15">{esc(sub)}</text></g>''')
    # Connect rows left-to-right without implying control authority beyond the documented data flow.
    if kind != "operations":
        ys = [377] * (len(boxes) - 1)
        for i in range(len(boxes) - 1):
            x1 = boxes[i][0] + boxes[i][2] + 12
            x2 = boxes[i+1][0] - 12
            elements.append(f'<path d="M{x1} {ys[i]} H{x2}" stroke="{accent}" stroke-width="4" opacity=".65" marker-end="url(#arrow)"/>')
    else:
        for row in (boxes[:4], boxes[4:]):
            y = row[0][1] + 60
            for i in range(len(row) - 1):
                x1 = row[i][0] + row[i][2] + 12
                x2 = row[i+1][0] - 12
                elements.append(f'<path d="M{x1} {y} H{x2}" stroke="{accent}" stroke-width="4" opacity=".65" marker-end="url(#arrow)"/>')
        elements.append(f'<path d="M640 365 V520" stroke="{accent}" stroke-width="3" opacity=".35" stroke-dasharray="10 10"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#030712"/><stop offset="1" stop-color="#111827"/></linearGradient><pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" stroke="#334155" stroke-width="1" opacity=".22"/></pattern><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{accent}"/></marker></defs>
<rect width="1600" height="900" fill="url(#bg)"/><rect width="1600" height="900" fill="url(#grid)"/>
<circle cx="1360" cy="120" r="250" fill="{accent}" opacity=".06"/><circle cx="250" cy="820" r="300" fill="{accent}" opacity=".04"/>
<text x="90" y="105" fill="{accent}" font-family="monospace" font-size="22" letter-spacing="4">SYSTEM ARCHITECTURE</text>
<text x="90" y="165" fill="#ffffff" font-family="monospace" font-size="43" font-weight="700">{esc(project['card'])}</text>
{''.join(elements)}
<text x="800" y="805" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="19" letter-spacing="2">{esc(footer)}</text>
<text x="90" y="855" fill="#64748b" font-family="monospace" font-size="14">Repository-derived system visualization • not a hardware photograph</text>
</svg>'''
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    (ASSET_DIR / project["visual"]).write_text(svg, encoding="utf-8")


HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="manifest" href="../site.webmanifest"><meta name="theme-color" content="#02040a"><script src="https://cdn.tailwindcss.com"></script><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"><link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet"><link rel="stylesheet" href="../project-detail.css"><script>tailwind.config={theme:{extend:{colors:{'cyber-blue':'#00f0ff','cyber-purple':'#7000ff','neon-green':'#0aff64'}}}}</script>'''


def detail_page(p):
    a = esc(p["accent"])
    return f'''{HEAD}<title>{esc(p['title'])} | Samarth Patel</title></head><body class="grid-bg min-h-screen"><nav class="sticky top-0 z-50 bg-black/90 backdrop-blur border-b border-cyan-400/20"><div class="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between"><a href="../index.html#projects" class="section-title text-white hover:text-cyan-300"><i class="fas fa-arrow-left mr-2"></i>FEATURED PROTOCOLS</a><a href="../index.html" class="tech text-cyan-300">SP.ROBOTICS</a></div></nav><main class="max-w-6xl mx-auto px-5 py-14 md:py-20"><div class="project-visual rounded-xl mb-8 relative" style="background-image:url('../assets/project/{esc(p['visual'])}');background-size:cover;background-position:center;background-repeat:no-repeat"><span class="source-badge">REPOSITORY-DERIVED SYSTEM VISUALIZATION</span></div><header class="cyber-border rounded-2xl p-7 md:p-12 mb-8 relative overflow-hidden"><div class="absolute inset-0 opacity-10" style="background:radial-gradient(circle at 80% 10%,{a},transparent 42%)"></div><div class="relative"><div class="hero-icon text-5xl mb-6" style="color:{a}"><i class="fas {esc(p['icon'])}"></i></div><p class="tech uppercase tracking-[.22em] text-xs mb-3" style="color:{a}">{esc(p['status'])}</p><h1 class="section-title text-3xl md:text-5xl leading-tight mb-5">{esc(p['title'])}</h1><p class="text-gray-300 text-lg md:text-xl leading-8 max-w-4xl">{esc(p['summary'])}</p><div class="mt-7 inline-block px-4 py-2 rounded border border-white/10 bg-white/5 tech text-sm text-gray-300">{esc(p['stack'])}</div></div></header><div class="grid gap-6"><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{a}"><i class="fas fa-triangle-exclamation mr-3"></i>Engineering Challenge</h2><p class="text-gray-300 leading-8 text-lg">{esc(p['challenge'])}</p></section><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{a}"><i class="fas fa-code mr-3"></i>Implementation</h2><p class="text-gray-300 leading-8 text-lg">{esc(p['implementation'])}</p></section><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{a}"><i class="fas fa-diagram-project mr-3"></i>System Architecture</h2><p class="text-gray-300 leading-8 text-lg">{esc(p['architecture'])}</p></section><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{a}"><i class="fas fa-vial-circle-check mr-3"></i>Validation &amp; Test Strategy</h2><p class="text-gray-300 leading-8 text-lg">{esc(p['validation'])}</p></section><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{a}"><i class="fas fa-scale-balanced mr-3"></i>Engineering Decisions &amp; Boundaries</h2><p class="text-gray-300 leading-8 text-lg">{esc(p['decisions'])}</p></section><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl text-cyan-300 mb-4"><i class="fas fa-link mr-3"></i>Project Access</h2><p class="text-gray-400 mb-5">Public repository with implementation and documentation.</p><a href="{esc(p['repo'])}" target="_blank" class="inline-flex items-center px-5 py-3 border border-cyan-400/40 rounded text-cyan-300 hover:bg-cyan-400 hover:text-black tech"><i class="fab fa-github mr-2"></i>OPEN GITHUB REPOSITORY</a></section></div><div class="mt-10"><a href="../index.html#projects" class="tech text-gray-400 hover:text-cyan-300"><i class="fas fa-arrow-left mr-2"></i>BACK TO PROJECTS</a></div></main></body></html>'''


def card_html(p):
    return f'''<div class="tilt-card group cursor-pointer rounded-xl overflow-hidden border border-white/10 bg-cyber-dark/50 hover:border-{p['hover']}/50 transition-all" onmousemove="tiltCard(event, this)" onmouseleave="resetCard(this)" data-project-detail="project/{esc(p['slug'])}.html" role="link" tabindex="0" onclick="if(!event.target.closest('a')) window.location.href='project/{esc(p['slug'])}.html'" onkeydown="if(event.key==='Enter' || event.key===' ') window.location.href='project/{esc(p['slug'])}.html'">
                    <div class="h-28 relative overflow-hidden tilt-inner bg-gray-900" style="background-image:url('assets/project/{esc(p['visual'])}');background-size:cover;background-position:center;background-repeat:no-repeat"><span class="absolute top-2 left-2 z-20 px-2 py-1 text-[9px] font-mono border border-white/20 text-gray-200 bg-black/45 backdrop-blur-sm">SYSTEM VISUAL</span><div class="absolute inset-0 flex items-center justify-center pointer-events-none"><i class="fas {esc(p['icon'])} text-5xl opacity-20 group-hover:opacity-60 transition-opacity z-10" style="color:{esc(p['accent'])}"></i></div><div class="absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-transparent opacity-5"></div></div>
                    <div class="p-5 relative tilt-inner bg-cyber-black/50 backdrop-blur-sm"><h3 class="text-xl font-bold text-white font-mono mb-2" style="--project-accent:{esc(p['accent'])}">{esc(p['card'])}</h3><p class="font-tech text-xs mb-4" style="color:{esc(p['accent'])}">[ {esc(p['tags'])} ]</p><p class="text-gray-400 text-sm mb-3">{esc(p['summary'])}</p><a href="{esc(p['repo'])}" target="_blank" class="inline-flex items-center text-white hover:text-cyan-300 transition-colors font-mono text-sm"><i class="fab fa-github mr-2"></i> ACCESS REPO <i class="fas fa-arrow-right ml-2 transform group-hover:translate-x-1 transition-transform"></i></a></div>
                </div>'''


def patch_index():
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(r'\s*<!-- NEW INDUSTRIAL PROJECTS START -->.*?<!-- NEW INDUSTRIAL PROJECTS END -->\s*', '\n', text, flags=re.S)

    # Keep the profile aligned with the new work without presenting repository publication as an earlier project date.
    new_about = '<p>My project work spans <span class="text-white">ROS/ROS2 mobile robotics</span>, UR10 manipulation, autonomous industrial inspection, robot fleet observability, computer vision, industrial anomaly detection, industrial incident diagnostics, embedded Linux/OTA deployment and an ongoing SO-101 robot-learning study.</p>'
    text = re.sub(r'<p>My project work spans .*?</p>', new_about, text, count=1, flags=re.S)

    text = text.replace(
        'ROS Noetic, ROS2 Humble, Nav2, TF2, GMapping, Cartographer, AMCL, move_base, DWA, TEB, RRT/BiRRT/PRM, Gazebo and RViz.',
        'ROS Noetic, ROS2 Humble/Jazzy, Nav2, TF2, GMapping, Cartographer, AMCL, move_base, DWA, TEB, RRT/BiRRT/PRM, Gazebo/RViz, Gazebo Harmonic, TurtleBot platforms and waypoint task plugins.'
    )

    text = re.sub(r'\s*<!-- ROBOT OPS SKILLS START -->.*?<!-- ROBOT OPS SKILLS END -->\s*', '\n', text, flags=re.S)
    ops_skills = '''<!-- ROBOT OPS SKILLS START --><div class="p-5 bg-white/5 rounded-xl border border-cyan-400/20"><h3 class="font-mono text-cyan-300 mb-2">ROBOT OPERATIONS & BACKEND</h3><p class="text-gray-400 text-sm leading-6">FastAPI, REST/OpenAPI, InfluxDB 2.x/Flux, JWT, Grafana, SQLite, SQLAlchemy, PostgreSQL, Alembic, Docker Compose, Caddy and Prometheus-style observability.</p></div><div class="p-5 bg-white/5 rounded-xl border border-yellow-400/20"><h3 class="font-mono text-yellow-300 mb-2">VALIDATION & RELIABILITY</h3><p class="text-gray-400 text-sm leading-6">ROS smoke/regression workflows, Pytest, integration and contract testing, fault injection, parser fuzzing, migration checks, evidence provenance and release-gate tooling.</p></div><!-- ROBOT OPS SKILLS END -->'''
    programming_marker = '<div class="p-5 bg-white/5 rounded-xl border border-white/10"><h3 class="font-mono text-white mb-3">PROGRAMMING & ENGINEERING TOOLS</h3>'
    if programming_marker in text:
        text = text.replace(programming_marker, ops_skills + programming_marker, 1)

    sec_start = text.find('<section id="projects"')
    if sec_start < 0:
        raise RuntimeError('Projects section not found')
    sec_end = text.find('</section>', sec_start)
    if sec_end < 0:
        raise RuntimeError('Projects section closing tag not found')
    section = text[sec_start:sec_end]
    closes = list(re.finditer(r'</div>', section))
    if len(closes) < 2:
        raise RuntimeError('Could not identify project grid closing tag')
    insertion_abs = sec_start + closes[-2].start()
    cards = '\n                <!-- NEW INDUSTRIAL PROJECTS START -->\n                ' + '\n\n                '.join(card_html(p) for p in PROJECTS) + '\n                <!-- NEW INDUSTRIAL PROJECTS END -->\n            '
    text = text[:insertion_abs] + cards + text[insertion_abs:]
    INDEX.write_text(text, encoding="utf-8")


def main():
    PROJECT_DIR.mkdir(exist_ok=True)
    for p in PROJECTS:
        write_svg(p)
        (PROJECT_DIR / f"{p['slug']}.html").write_text(detail_page(p), encoding="utf-8")
    patch_index()
    print('Added 3 industrial robotics platform projects, case studies, visuals, and skills updates.')


if __name__ == '__main__':
    main()

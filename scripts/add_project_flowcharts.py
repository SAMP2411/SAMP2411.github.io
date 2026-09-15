from pathlib import Path
import html
import math
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "project"
FLOW_DIR = ROOT / "assets" / "flowcharts"
FLOW_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS = {
    "distributed-state-estimation": ("Distributed State Estimation", "#00f0ff", ["Edge / Substation Device", "Buildroot → Yocto Image", "U-Boot", "A/B Root Filesystem", "containerd Applications", "Signed RAUC OTA", "Boot Validation / Rollback"]),
    "telepresence-robot": ("Telepresence Robot", "#7000ff", ["LiDAR + IMU + Encoders", "ROS Topics + TF", "GMapping", "Saved Occupancy Map", "AMCL Localization", "move_base + DWA", "cmd_vel", "Arduino Motor Control"]),
    "competitive-robotics": ("Competitive Robotics", "#0aff64", ["PS4 Operator Input", "Raspberry Pi Control", "Task / Sequence Logic", "Arduino Actuation", "Motors + Mechanisms", "Feedback + Iteration"]),
    "unmanned-ground-vehicle": ("Unmanned Ground Vehicle", "#ef4444", ["GPS", "IMU", "Sensor Preprocessing", "Kalman Filter", "Position + Heading", "Waypoint Error", "PID Controller", "Drive Commands"]),
    "turtlebot3-navigation": ("TurtleBot3 Autonomous Navigation", "#00f0ff", ["Sensors + Odometry", "TF2 Tree", "SLAM / Saved Map", "AMCL Pose", "Global Planner", "Local Controller + Costmap", "cmd_vel", "TurtleBot3 Base"]),
    "ur10-manipulator": ("UR10 Manipulator Control", "#a855f7", ["Target Pose / Config", "Forward + Inverse Kinematics", "Damped Least Squares", "Joint Ordering", "Trajectory Generation", "JointTrajectory Message", "Simulation Validation", "Hardware Execution"]),
    "iiot-anomaly-detector": ("IIoT Anomaly Detector", "#0aff64", ["Industrial Sensor Stream", "MQTT Publisher", "Broker / Topic", "Python Subscriber", "Preprocessing", "Isolation Forest", "Anomaly Log", "Plotly Dashboard"]),
    "offline-face-recognition": ("Offline Guided Face Recognition", "#38bdf8", ["Camera Frame", "Face Detection", "Alignment + Pose Check", "Embedding Extraction", "Enrollment Store", "Live Embedding", "Similarity Decision", "Identity / Unknown"]),
    "rst-hackathon": ("RST Hackathon", "#facc15", ["Camera Observation", "Target Tracking", "Coordinate Transform", "Throw Strategy", "Robot Command / IK", "Throw Execution", "Observe + Retry"]),
    "so101-robot-learning": ("SO-101 Robot Learning", "#e879f9", ["Task Definition", "Context / Demonstrations", "Zero / Few / In-Context", "Action Generation", "Pick-and-Place", "Trial Logging", "Method Comparison", "Hardware Transfer"]),
    "autonomous-industrial-inspection-robot": ("Autonomous Industrial Inspection", "#f59e0b", ["Site + Asset Config", "Gazebo + ROS 2", "Nav2 Waypoints", "Inspection Plugin", "Visual / Thermal / Acoustic Evidence", "InspectionResult", "Mission Aggregation", "Report + Follow-up Decision"]),
    "robot-fleet-observability-platform": ("Robot Fleet Observability", "#22d3ee", ["AMRs / 5-Robot Simulator", "API Key + Tenant ID", "FastAPI Ingestion", "InfluxDB Time Series", "Tenant-Scoped Fleet API", "JWT Operator Access", "Dashboard / OpenAPI / Grafana", "Fleet KPIs + Alerts"]),
    "industrial-robot-operations-intelligence": ("Industrial Robot Operations Intelligence", "#a78bfa", ["ROS 2 Inspection", "Reports + Evidence", "FleetWatch Sync", "Operator Finding Workflow", "Follow-up Mission Queue", "Robot / WMS / PLC / Network Logs", "Safe Preview + Commit", "Normalize + Asset Mapping", "Aligned Incident Timeline", "Evidence-Linked Hypotheses", "Human-Reviewed Report"]),
}


def esc(v):
    return html.escape(str(v), quote=True)


def split_label(label, max_chars=22):
    words = label.split()
    lines, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if current and len(candidate) > max_chars:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if len(lines) > 2:
        lines = [lines[0], " ".join(lines[1:])]
    return lines[:2]


def flow_svg(title, accent, nodes):
    width, height = 1600, 650
    n = len(nodes)
    if n <= 6:
        rows = [nodes]
    else:
        cut = math.ceil(n / 2)
        rows = [nodes[:cut], nodes[cut:]]

    box_h = 118
    row_y = [225] if len(rows) == 1 else [180, 400]
    boxes = []
    order = 1
    for r, row in enumerate(rows):
        count = len(row)
        gap = 34
        box_w = min(250, int((width - 140 - gap * (count - 1)) / count))
        total = count * box_w + (count - 1) * gap
        start_x = (width - total) // 2
        seq = list(enumerate(row))
        if r == 1:
            seq = list(reversed(seq))
        for visual_i, (logical_i, label) in enumerate(seq):
            x = start_x + visual_i * (box_w + gap)
            y = row_y[r]
            boxes.append((order, x, y, box_w, box_h, label, r, visual_i))
            order += 1

    # Actual visual order is row 1 L→R, then row 2 R→L for a continuous snake.
    boxes_sorted = sorted(boxes, key=lambda b: b[0])
    parts = []
    for idx, x, y, bw, bh, label, r, vi in boxes_sorted:
        lines = split_label(label)
        text_y = y + 55 if len(lines) == 1 else y + 45
        text = "".join(
            f'<text x="{x+bw/2}" y="{text_y+i*27}" text-anchor="middle" fill="#f8fafc" font-family="monospace" font-size="17" font-weight="700">{esc(line)}</text>'
            for i, line in enumerate(lines)
        )
        parts.append(f'''<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="18" fill="#0a1422" stroke="{accent}" stroke-width="2.5"/><circle cx="{x+24}" cy="{y+24}" r="15" fill="{accent}"/><text x="{x+24}" y="{y+30}" text-anchor="middle" fill="#020617" font-family="monospace" font-size="14" font-weight="900">{idx}</text>{text}</g>''')

    for a, b in zip(boxes_sorted, boxes_sorted[1:]):
        _, ax, ay, aw, ah, _, ar, _ = a
        _, bx, by, bw, bh, _, br, _ = b
        if ar == br:
            if bx > ax:
                d = f"M{ax+aw+8} {ay+ah/2} H{bx-8}"
            else:
                d = f"M{ax-8} {ay+ah/2} H{bx+bw+8}"
        else:
            # route cleanly down the right edge before returning across the second row
            xmid = min(width - 55, ax + aw + 22)
            d = f"M{ax+aw/2} {ay+ah+8} V{by-32} H{bx+bw/2} V{by-8}"
        parts.append(f'<path d="{d}" fill="none" stroke="{accent}" stroke-width="4" opacity=".78" marker-end="url(#arrow)"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="650" viewBox="0 0 1600 650">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#020617"/><stop offset=".55" stop-color="#07111f"/><stop offset="1" stop-color="#0b1320"/></linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#334155" stroke-width="1" opacity=".2"/></pattern>
  <radialGradient id="halo"><stop stop-color="{accent}" stop-opacity=".2"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <filter id="shadow"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity=".6"/></filter>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{accent}"/></marker>
</defs>
<rect width="1600" height="650" rx="28" fill="url(#bg)"/><rect width="1600" height="650" rx="28" fill="url(#grid)"/><ellipse cx="800" cy="325" rx="700" ry="350" fill="url(#halo)" opacity=".35"/>
<text x="70" y="67" fill="{accent}" font-family="monospace" font-size="18" letter-spacing="4">SYSTEM FLOW ILLUSTRATION</text>
<text x="70" y="112" fill="#f8fafc" font-family="monospace" font-size="30" font-weight="700">{esc(title)}</text>
<text x="1530" y="69" text-anchor="end" fill="#64748b" font-family="monospace" font-size="14">architecture flow • portfolio illustration</text>
{''.join(parts)}
<text x="800" y="610" text-anchor="middle" fill="#64748b" font-family="monospace" font-size="14">Separate architecture illustration — project hero/media shown independently above</text>
</svg>'''


def section_html(slug, title, accent):
    return f'''<!-- FLOWCHART START --><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{accent}"><i class="fas fa-sitemap mr-3"></i>System Flow Illustration</h2><p class="text-gray-400 mb-5">A separate visual map of the project architecture and data/control flow.</p><div class="overflow-x-auto rounded-xl border border-white/10 bg-black/40 p-3 md:p-5"><img src="../assets/flowcharts/{slug}.svg" alt="{esc(title)} system flowchart illustration" class="block w-full min-w-[820px] h-auto"></div></section><!-- FLOWCHART END -->'''


for slug, (title, accent, nodes) in PROJECTS.items():
    (FLOW_DIR / f"{slug}.svg").write_text(flow_svg(title, accent, nodes), encoding="utf-8")
    page = PROJECT_DIR / f"{slug}.html"
    if not page.exists():
        print(f"WARN: missing detail page for {slug}")
        continue
    text = page.read_text(encoding="utf-8")
    text = re.sub(r'<!-- FLOWCHART START -->.*?<!-- FLOWCHART END -->', '', text, flags=re.S)
    # Insert immediately after the System Architecture section, before Validation.
    marker = '<i class="fas fa-vial-circle-check mr-3"></i>Validation'
    idx = text.find(marker)
    if idx == -1:
        print(f"WARN: validation marker missing for {slug}")
        continue
    section_start = text.rfind('<section', 0, idx)
    if section_start == -1:
        continue
    text = text[:section_start] + section_html(slug, title, accent) + text[section_start:]
    page.write_text(text, encoding="utf-8")

print(f"Generated {len(PROJECTS)} standalone flowchart illustrations and inserted them into project detail pages.")

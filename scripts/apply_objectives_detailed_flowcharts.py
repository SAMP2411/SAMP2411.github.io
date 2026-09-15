from pathlib import Path
import html
import math
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / 'project'
FLOW_DIR = ROOT / 'assets' / 'flowcharts'
INDEX = ROOT / 'index.html'
FLOW_DIR.mkdir(parents=True, exist_ok=True)

DATA = {
'distributed-state-estimation': {
 'title':'Distributed State Estimation','accent':'#00f0ff',
 'objective':'Build a secure, reproducible embedded-Linux edge platform for distributed state-estimation workloads, with maintainable Yocto builds, signed RAUC A/B OTA updates, containerized application deployment and QEMU-based validation on a constrained ARM target.',
 'goals':['Target the ARM Cortex-A7 edge hardware and its memory/resource constraints.','Replace the initial Buildroot baseline with a maintainable Yocto Scarthgap image workflow.','Provide signed, rollback-capable A/B OTA updates through RAUC and U-Boot.','Run state-estimation applications in a lightweight containerd environment and validate releases before deployment.'],
 'nodes':[('Grid / IEC 61850 context','Define substation data and edge-compute role'),('ARM Cortex-A7 target','Constrained RAM/storage target'),('Buildroot baseline','Bring up minimal Linux reference'),('Yocto Scarthgap migration','Create reproducible maintainable image'),('Linux + BusyBox image','Build kernel/rootfs/userspace'),('U-Boot boot flow','Load kernel, DT and boot metadata'),('A/B rootfs layout','Active and standby system slots'),('RAUC signing','Build and cryptographically sign bundle'),('OTA delivery','Transfer update bundle over HTTP'),('Inactive-slot install','Write update without touching active slot'),('Boot validation','Health-check newly booted system'),('Rollback / confirm','Recover on failure or accept update'),('containerd apps','Deploy isolated estimation workloads'),('QEMU + CI/CD','Automate build, boot and release validation')]},
'telepresence-robot': {
 'title':'Telepresence Robot','accent':'#a855f7',
 'objective':'Build a ROS-based telepresence mobile robot that combines mapping, localization and autonomous navigation with onboard sensing and Arduino-based low-level drive control, so remote presence can operate on top of a reliable mobility stack.',
 'goals':['Integrate LiDAR, IMU/odometry and robot frames into a consistent ROS Noetic data model.','Create and save a 2D occupancy map with GMapping, then localize against it using AMCL.','Use move_base and DWA for global/local navigation and obstacle-aware velocity generation.','Bridge high-level cmd_vel commands to the Arduino motor layer and validate the stack in Gazebo/RViz and hardware.'],
 'nodes':[('Chassis + compute','Mechanical platform and onboard computer'),('LiDAR + IMU + odometry','Acquire environment and motion data'),('ROS Noetic bring-up','Launch drivers and robot interfaces'),('Topics + TF','Publish /scan, /imu, /odom and transforms'),('Frame validation','Check map/odom/base/sensor consistency'),('GMapping SLAM','Estimate pose while building occupancy map'),('Map persistence','Save map.yaml and map image'),('AMCL localization','Particle-filter localization in saved map'),('move_base','Coordinate global/local navigation'),('Global planning','Generate collision-aware route to goal'),('DWA + costmaps','Local obstacle avoidance and tracking'),('cmd_vel','Generate linear/angular velocity commands'),('Arduino motor interface','Translate commands to wheel actuation'),('Gazebo/RViz + hardware','Inspect, tune and validate real behavior')]},
'competitive-robotics': {
 'title':'Competitive Robotics / DD Robocon','accent':'#0aff64',
 'objective':'Develop a competition-robot control architecture that translates PS4 operator commands into coordinated mechanism actions through Raspberry Pi supervision, discrete task sequencing, Arduino actuation and iterative PID/control tuning.',
 'goals':['Convert competition rules and scoring tasks into explicit robot behaviors.','Use Raspberry Pi as the high-level coordination layer and Arduino for low-level actuation.','Combine manual PS4 input with repeatable task/sequence logic for mechanisms.','Iteratively tune control, reliability and recovery under competition time and hardware constraints.'],
 'nodes':[('Competition requirements','Break scoring rules into robot functions'),('PS4 operator input','Capture motion and task commands'),('Raspberry Pi supervisor','Manage high-level state and communication'),('Command parsing','Convert operator commands to actions'),('Task state machine','Sequence mechanisms and timed actions'),('Safety / interlocks','Prevent invalid or conflicting actions'),('Arduino controller','Receive low-level actuation targets'),('Motor / servo drive','Generate PWM/direction outputs'),('Mechanisms','Drive, manipulate, grip or launch'),('Feedback sensing','Use available position/IMU/limit feedback'),('PID + tuning','Improve repeatability and stability'),('Iterative test loop','Debug, stress-test and refine for competition')]},
'unmanned-ground-vehicle': {
 'title':'Autonomous Unmanned Ground Vehicle','accent':'#ef4444',
 'objective':'Build a waypoint-navigation ground vehicle that fuses GPS and IMU measurements for state estimation and uses closed-loop PID control to continually reduce position and heading error during autonomous motion.',
 'goals':['Represent the mission as a sequence of geographic waypoints.','Fuse noisy GPS and IMU measurements with a Kalman-filter state estimator.','Convert state estimates into waypoint position/heading errors.','Close the loop with PID-based steering/speed commands through Raspberry Pi and Arduino actuation.'],
 'nodes':[('Mission waypoints','Load geographic navigation targets'),('GPS measurements','Acquire global position'),('IMU measurements','Acquire acceleration / angular rate'),('Preprocessing','Synchronize, filter and normalize sensors'),('Kalman filter','Fuse GPS + IMU uncertainty'),('State estimate','Position, heading and motion estimate'),('Waypoint selection','Choose active navigation target'),('Error computation','Position and heading error to target'),('PID control','Compute steering / speed correction'),('Raspberry Pi supervisor','Mission and safety logic'),('Arduino interface','Translate commands to motor signals'),('Drive actuation','Apply wheel/steering outputs'),('Vehicle motion','Move through environment'),('Feedback loop','New GPS/IMU data closes control loop')]},
'turtlebot3-navigation': {
 'title':'TurtleBot3 Autonomous Navigation','accent':'#00f0ff',
 'objective':'Implement and validate an end-to-end ROS2 autonomous-navigation workflow for TurtleBot3, covering bring-up, TF/odometry integrity, SLAM, AMCL localization, global/local planning, controller tuning, simulation and real-robot execution.',
 'goals':['Validate hardware/simulation bring-up, odometry and the TF2 frame tree before navigation.','Generate, save and reuse maps through the SLAM workflow.','Localize probabilistically with AMCL and route goals through Nav2 planning/control.','Tune costmaps, planners and velocity limits in Gazebo/RViz before simulation-to-real execution.'],
 'nodes':[('Robot bring-up','Launch TurtleBot3 base and sensors'),('LiDAR + odometry','Publish scan and odom inputs'),('TF2 validation','Verify map→odom→base→sensor frames'),('SLAM mapping','Build 2D occupancy representation'),('Map save / reload','Persist map for later navigation'),('AMCL','Estimate robot pose in known map'),('Goal / waypoint input','Define desired navigation target'),('Global costmap','Static map + obstacle context'),('Global planner','Generate start-to-goal path'),('Local costmap','Maintain nearby obstacle model'),('Local controller','Track path and avoid obstacles'),('Velocity limits','Tune min/max linear/angular behavior'),('cmd_vel + base','Execute motion commands'),('Gazebo/RViz→real','Inspect, tune and transfer to hardware')]},
'ur10-manipulator': {
 'title':'UR10 Manipulator Control','accent':'#a855f7',
 'objective':'Develop a manipulator-control workflow for UR10 that converts task-space targets into joint-space trajectories using forward/inverse kinematics, damped least squares, ordered joint conversion and ROS JointTrajectory messaging, with simulation-first validation before hardware.',
 'goals':['Model the UR10 kinematic chain and compute forward/inverse kinematics.','Use damped least squares to improve numerical behavior near singular configurations.','Convert solved joint states into the exact UR10 joint-name/order convention.','Generate ROS-compatible trajectories and validate in MATLAB/Simulink/Simscape and simulation before hardware execution.'],
 'nodes':[('Task / target pose','Specify desired position + orientation'),('UR10 model / URDF','Load kinematic structure and joint limits'),('Forward kinematics','Map joint vector to end-effector pose'),('Pose error','Compare desired and current task pose'),('Jacobian','Relate joint velocity to task-space change'),('Damped least squares','Compute robust incremental IK update'),('IK convergence','Iterate until target / tolerance'),('Joint-name mapping','Map semantic names to UR10 indices'),('Config→joint vector','Produce ordered numeric joint state'),('Trajectory generation','Build smooth time-parameterized motion'),('JointTrajectory message','Populate names, positions and timing'),('MATLAB/Simscape validation','Check model and control behavior'),('Gazebo/RViz validation','Inspect commanded robot motion'),('Hardware execution','Send validated trajectory to real UR10')]},
'iiot-anomaly-detector': {
 'title':'IIoT Anomaly Detector','accent':'#0aff64',
 'objective':'Build a lightweight industrial monitoring pipeline that transports streaming sensor telemetry over MQTT, applies unsupervised anomaly detection with Isolation Forest and visualizes operating behavior for investigation.',
 'goals':['Model an industrial telemetry producer and stream measurements continuously over MQTT.','Parse and transform the incoming measurements into features suitable for unsupervised detection.','Use Isolation Forest to score/flag unusual behavior without requiring labelled fault classes.','Expose sensor trends and anomaly events through a low-latency Plotly-based monitoring view.'],
 'nodes':[('Sensor / IIoT source','Generate industrial telemetry'),('MQTT publisher','Serialize and publish measurements'),('Broker + topics','Route messages to subscribers'),('Python subscriber','Consume streaming payloads'),('Payload validation','Parse fields and reject malformed data'),('Preprocessing','Clean and normalize measurements'),('Feature preparation','Create model input representation'),('Isolation Forest','Estimate anomaly score from structure'),('Decision rule','Convert score to normal/anomaly flag'),('Event logging','Preserve anomaly context'),('Latency monitoring','Track end-to-end processing responsiveness'),('Plotly visualization','Show trends and anomaly markers'),('Operator investigation','Review unusual operating behavior')]},
'offline-face-recognition': {
 'title':'Offline Guided Face Enrollment and Recognition','accent':'#38bdf8',
 'objective':'Build a fully offline guided enrollment and recognition pipeline that rejects weak enrollment samples, extracts face embeddings locally with InsightFace/ONNX Runtime and performs real-time identity matching without cloud dependence.',
 'goals':['Guide enrollment so stored examples have useful pose and image quality.','Perform detection/alignment and embedding extraction locally rather than through a cloud API.','Store identity embeddings and compare live query embeddings against them.','Handle weak/boundary inputs and return an identity or unknown decision in a live OpenCV loop.'],
 'nodes':[('Camera frame','Capture local RGB video'),('Face detection','Locate face region'),('Landmark alignment','Normalize face geometry'),('Pose validation','Check orientation constraints'),('Input-quality checks','Reject weak enrollment frames'),('Guided enrollment','Collect multiple acceptable samples'),('InsightFace model','Extract discriminative face embedding'),('ONNX Runtime','Execute model locally/offline'),('Enrollment store','Persist identity + embeddings'),('Live query embedding','Embed incoming face'),('Similarity comparison','Compare query with stored identities'),('Threshold decision','Best match vs unknown'),('Display / monitoring','Render result and system status')]},
'rst-hackathon': {
 'title':'RST Hackathon Vision-Guided Throwing','accent':'#facc15',
 'objective':'Rapidly integrate computer vision, target tracking, coordinate transformation and robot-action planning into a robust hackathon system capable of converting visual target observations into executable ball-throw actions under strict time constraints.',
 'goals':['Detect and track the relevant target state from camera observations.','Transform observations from camera coordinates into a robot/task coordinate frame.','Choose a practical throw/action strategy that can be implemented and debugged within the hackathon.','Close the loop by observing the outcome and refining the strategy while prioritizing reliability.'],
 'nodes':[('Challenge definition','Understand rules, target and time limits'),('Camera observation','Acquire scene frames'),('Target detection','Identify moving/desired target'),('Target tracking','Estimate target position over time'),('Scene geometry','Relate pixels to spatial position'),('Coordinate transform','Camera frame → robot/task frame'),('Strategy selection','Choose trajectory/timing/speed approach'),('Robot command / IK','Map target action to robot joints'),('Throw execution','Execute arm release motion'),('Outcome observation','Measure hit/miss/landing behavior'),('Retry / refinement','Tune parameters from feedback'),('Robust task completion','Prefer reliable execution under deadline')]},
'so101-robot-learning': {
 'title':'SO-101 Zero/Few/In-Context Robot Learning','accent':'#e879f9',
 'objective':'Design a controlled pick-and-place experiment for the SO-101 arm to compare zero-shot, few-shot and in-context learning strategies using common task definitions, demonstrations, success criteria, trial logging and eventual hardware transfer.',
 'goals':['Define one common pick-and-place task and success criteria for all learning conditions.','Keep observations/action format consistent so zero-shot, few-shot and in-context approaches can be compared fairly.','Log every trial, failure mode and method configuration rather than presenting unverified performance.','Start with lightweight simulation/offline experimentation and transfer only validated behavior toward SO-101 hardware.'],
 'nodes':[('Task + workspace','Define objects, source, target and constraints'),('Success criteria','Specify what counts as task completion'),('SO-101 / lightweight sim','Initialize robot model or hardware interface'),('Observation capture','Collect image/state/gripper context'),('Prompt / instruction','Define common task description'),('Deterministic baseline','Establish non-learning reference'),('Zero-shot branch','Instruction only, no examples'),('Few-shot branch','Condition with a few demonstrations'),('In-context branch','Condition with richer task context'),('Action generation','Produce robot action sequence'),('Safety / format checks','Validate generated action structure'),('Pick-and-place execution','Run trial in controlled environment'),('Trial logging','Record context, actions and failure modes'),('Method comparison','Compare consistency/success qualitatively/quantitatively'),('Prompt refinement','Iterate based on observed failure modes'),('Hardware transfer','Validate selected approach on SO-101')]},
'autonomous-industrial-inspection-robot': {
 'title':'Autonomous Industrial Inspection Robot','accent':'#f59e0b',
 'objective':'Build a deterministic ROS2 industrial inspection workflow that patrols configured industrial assets, executes multimodal inspection-at-waypoint tasks, preserves auditable evidence, aggregates findings and makes explicit follow-up decisions.',
 'goals':['Represent sites, assets, checkpoints and inspection profiles in configuration rather than hard-coded mission logic.','Use Nav2 waypoint execution with a custom inspection task plugin so navigation and inspection remain composable.','Capture visual/thermal/acoustic/gauge-style evidence and publish structured InspectionResult messages.','Aggregate a patrol round into auditable reports and deterministic continue/reinspect/watchlist/safety-hold decisions.'],
 'nodes':[('Site / asset config','Load facility, assets and checkpoint definitions'),('Inspection profiles','Select modes, thresholds and parameters'),('Seeded scenario','Make simulated anomalies reproducible'),('Gazebo Harmonic','Simulate robot, environment and sensors'),('ROS2 bring-up','Launch mission + inspection packages'),('Nav2 waypoint mission','Navigate configured patrol route'),('Waypoint task plugin','Trigger inspection after arrival'),('Evidence capture','Visual / thermal / acoustic / gauge modes'),('Evidence metadata','Timestamp, asset, checkpoint and paths'),('Health / severity logic','Compute score, severity, confidence fields'),('InspectionResult','Publish structured per-checkpoint result'),('PatrolRoundSummary','Aggregate waypoint results'),('Decision logic','Continue / reinspect / watchlist / safety hold'),('Report generation','JSON / CSV / Markdown / HTML outputs'),('Smoke + regression','Headless, retry and multi-seed validation')]},
'robot-fleet-observability-platform': {
 'title':'Robot Fleet Observability Platform','accent':'#22d3ee',
 'objective':'Build a tenant-aware robot fleet observability platform that securely ingests AMR telemetry, stores time-series data in InfluxDB, computes fleet KPIs/fault context and presents operator-facing views through FastAPI, OpenAPI, dashboard and Grafana interfaces.',
 'goals':['Ingest status, battery, odometry, task, uptime and fault telemetry from simulated or real AMRs.','Separate producer authentication from operator JWT access and keep data tenant-scoped.','Use InfluxDB/Flux for time-series persistence, aggregation and fleet-level views.','Expose health, KPIs and fault history through APIs plus operator/dashboard visualization and explicit degraded-health reporting.'],
 'nodes':[('AMRs / simulator','Five-robot simulator or telemetry producers'),('Telemetry payload','Status, battery, pose, task, uptime, faults'),('Producer auth','X-API-Key + X-Tenant-ID'),('FastAPI validation','Validate schema and resolve tenant'),('Ingestion routing','Accept authorized telemetry writes'),('InfluxDB write','Store tagged time-series measurements'),('Retention / series model','Organize measurements for query'),('Flux queries','Filter and aggregate per tenant'),('Fleet KPI service','Compute fleet-level health/context'),('Fault history','Retrieve robot fault/event context'),('JWT operator auth','Authenticate human/API users'),('Tenant-scoped API','Protect fleet/robot/KPI endpoints'),('Dashboard / OpenAPI','Built-in operator and developer interfaces'),('Grafana path','Optional advanced visualization'),('Health endpoint','Report API/DB dependency state')]},
'industrial-robot-operations-intelligence': {
 'title':'Industrial Robot Operations Intelligence','accent':'#a78bfa',
 'objective':'Unify live robot inspection workflows with historical multi-system incident diagnostics into an auditable operations-intelligence platform that preserves evidence provenance, aligns events across systems, supports operator finding lifecycle and keeps hypotheses subject to human review.',
 'goals':['Synchronize live inspection missions, reports and evidence into durable site/asset/mission/finding records.','Support operator acknowledgement, assignment, reinspect, resolve and close actions with traceable state transitions.','Safely ingest heterogeneous historical robot/WMS/WCS/PLC/network/maintenance data through preview-before-commit.','Preserve source provenance, normalize events, align timelines and generate evidence-linked hypotheses that remain human-reviewed rather than autonomous control actions.'],
 'nodes':[('ROS2 inspection missions','Live mission execution and findings'),('Evidence + reports','Images/sensor context and summaries'),('FleetWatch sync','Import mission state into operations DB'),('Durable records','Site / asset / mission / finding entities'),('Operator workflow','Acknowledge / assign / reinspect / resolve / close'),('Follow-up queue','Create targeted repeat-inspection work'),('Historical exports','Robot / WMS / WCS / PLC / network / maintenance'),('Safe preview','Parse and inspect before persistence'),('Commit + provenance','Store source metadata and SHA-256 lineage'),('Normalization','Convert heterogeneous records to event model'),('Asset mapping','Relate events to robots/assets/locations'),('Timeline alignment','Correlate events across clocks/systems'),('Incident metrics','Recovery and operational context'),('Evidence-linked hypotheses','Attach support and contradiction evidence'),('Human review','Validate findings and hypotheses'),('Auditable report','Produce reviewable/exportable diagnostics')]},
}

HERO = {
'autonomous-industrial-inspection-robot': ('assets/project/autonomous-industrial-inspection-hd.webp','../assets/project/autonomous-industrial-inspection-hd.webp'),
'robot-fleet-observability-platform': ('assets/project/robot-fleet-observability-hd.webp','../assets/project/robot-fleet-observability-hd.webp'),
'industrial-robot-operations-intelligence': ('assets/project/industrial-robot-operations-intelligence-hd.jpg','../assets/project/industrial-robot-operations-intelligence-hd.jpg'),
}

def esc(v): return html.escape(str(v), quote=True)

def split_label(text, width=24):
    words=text.split(); lines=[]; cur=''
    for w in words:
        nxt=(cur+' '+w).strip()
        if cur and len(nxt)>width:
            lines.append(cur); cur=w
        else: cur=nxt
    if cur: lines.append(cur)
    return lines[:3]

def svg_for(slug,d):
    nodes=d['nodes']; accent=d['accent']; title=d['title']
    W,H=1600,900; cols=4; rows=math.ceil(len(nodes)/cols)
    top=170; bottom=90; gapx=26; gapy=28; margin=55
    bw=(W-2*margin-gapx*(cols-1))/cols
    bh=min(150,(H-top-bottom-gapy*(rows-1))/rows)
    entries=[]
    for i,(name,detail) in enumerate(nodes):
        r=i//cols; pos=i%cols; c=pos if r%2==0 else cols-1-pos
        x=margin+c*(bw+gapx); y=top+r*(bh+gapy)
        entries.append((i+1,x,y,name,detail,r,c))
    parts=[]
    for idx,x,y,name,detail,r,c in entries:
        title_lines=split_label(name,22); detail_lines=split_label(detail,35)
        ty=y+45
        t=''.join(f'<text x="{x+bw/2:.1f}" y="{ty+j*23:.1f}" text-anchor="middle" fill="#f8fafc" font-family="Rajdhani,Arial,sans-serif" font-size="19" font-weight="700">{esc(line)}</text>' for j,line in enumerate(title_lines))
        dy=y+91
        dt=''.join(f'<text x="{x+bw/2:.1f}" y="{dy+j*19:.1f}" text-anchor="middle" fill="#94a3b8" font-family="Arial,sans-serif" font-size="13">{esc(line)}</text>' for j,line in enumerate(detail_lines))
        parts.append(f'<g filter="url(#shadow)"><rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="18" fill="#071421" stroke="{accent}" stroke-width="2"/><circle cx="{x+25:.1f}" cy="{y+25:.1f}" r="17" fill="{accent}"/><text x="{x+25:.1f}" y="{y+31:.1f}" text-anchor="middle" fill="#020617" font-family="monospace" font-size="14" font-weight="900">{idx}</text>{t}{dt}</g>')
    for a,b in zip(entries,entries[1:]):
        _,ax,ay,_,_,ar,ac=a; _,bx,by,_,_,br,bc=b
        if ar==br:
            if bx>ax: dpath=f'M {ax+bw+5:.1f} {ay+bh/2:.1f} H {bx-5:.1f}'
            else: dpath=f'M {ax-5:.1f} {ay+bh/2:.1f} H {bx+bw+5:.1f}'
        else:
            startx=ax+bw/2; endx=bx+bw/2
            dpath=f'M {startx:.1f} {ay+bh+4:.1f} V {ay+bh+gapy/2:.1f} H {endx:.1f} V {by-5:.1f}'
        parts.append(f'<path d="{dpath}" fill="none" stroke="{accent}" stroke-width="4" opacity=".78" marker-end="url(#arrow)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#020617"/><stop offset=".58" stop-color="#07111f"/><stop offset="1" stop-color="#0b1320"/></linearGradient><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#334155" stroke-width="1" opacity=".18"/></pattern><radialGradient id="halo"><stop stop-color="{accent}" stop-opacity=".20"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><filter id="shadow"><feDropShadow dx="0" dy="9" stdDeviation="9" flood-color="#000" flood-opacity=".6"/></filter><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{accent}"/></marker></defs><rect width="1600" height="900" rx="28" fill="url(#bg)"/><rect width="1600" height="900" rx="28" fill="url(#grid)"/><ellipse cx="800" cy="450" rx="760" ry="430" fill="url(#halo)" opacity=".32"/><text x="65" y="62" fill="{accent}" font-family="monospace" font-size="17" letter-spacing="4">DETAILED SYSTEM / ENGINEERING FLOW</text><text x="65" y="112" fill="#f8fafc" font-family="Orbitron,Arial,sans-serif" font-size="31" font-weight="700">{esc(title)}</text><text x="1535" y="65" text-anchor="end" fill="#64748b" font-family="monospace" font-size="13">code- and project-derived portfolio illustration</text>{''.join(parts)}<text x="800" y="866" text-anchor="middle" fill="#64748b" font-family="monospace" font-size="13">Flowchart is a technical illustration of the implemented/planned engineering pipeline; project media is shown separately.</text></svg>'''

def objective_html(d):
    bullets=''.join(f'<li>{esc(x)}</li>' for x in d['goals'])
    return f'''<!-- OBJECTIVE START --><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{d['accent']}"><i class="fas fa-bullseye mr-3"></i>Objective</h2><p class="text-gray-300 leading-8 text-lg">{esc(d['objective'])}</p><ul class="mt-5 grid md:grid-cols-2 gap-x-8 gap-y-3 text-gray-400 list-disc pl-5">{bullets}</ul></section><!-- OBJECTIVE END -->'''

def flow_html(slug,d):
    return f'''<!-- FLOWCHART START --><section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{d['accent']}"><i class="fas fa-sitemap mr-3"></i>Detailed Engineering Flow</h2><p class="text-gray-400 mb-5">Project-specific architecture and execution flow reconstructed from the implementation, project files and documented engineering workflow.</p><div class="overflow-x-auto rounded-xl border border-white/10 bg-black/40 p-3 md:p-5"><img src="../assets/flowcharts/{slug}-detailed.svg" alt="{esc(d['title'])} detailed engineering flowchart" class="block w-full min-w-[980px] h-auto"></div></section><!-- FLOWCHART END -->'''

def patch_page(slug,d):
    p=PROJECT_DIR/f'{slug}.html'
    if not p.exists():
        print('missing',p); return
    s=p.read_text(encoding='utf-8'); obj=objective_html(d)
    if '<!-- OBJECTIVE START -->' in s:
        s=re.sub(r'<!-- OBJECTIVE START -->.*?<!-- OBJECTIVE END -->',obj,s,flags=re.S)
    else:
        marker='<div class="grid gap-6">'
        if marker in s: s=s.replace(marker,marker+obj,1)
        else: print('no grid marker',slug)
    flow=flow_html(slug,d)
    if '<!-- FLOWCHART START -->' in s:
        s=re.sub(r'<!-- FLOWCHART START -->.*?<!-- FLOWCHART END -->',flow,s,flags=re.S)
    else:
        m=re.search(r'(<section class="glass rounded-xl p-6 md:p-8"><h2[^>]*>.*?System Architecture.*?</section>)',s,re.S)
        if m: s=s[:m.end()]+flow+s[m.end():]
        else: print('no flow insertion marker',slug)
    if slug in HERO:
        _,detail=HERO[slug]
        s=re.sub(r"background-image:url\('\.\./assets/project/[^']+'\)",f"background-image:url('{detail}')",s,count=1)
        s=s.replace('REPOSITORY-DERIVED SYSTEM VISUALIZATION','AI-GENERATED VISUALIZATION • HD')
        s=s.replace('HD PROJECT ILLUSTRATION','AI-GENERATED VISUALIZATION • HD')
    p.write_text(s,encoding='utf-8')

def patch_index():
    s=INDEX.read_text(encoding='utf-8')
    repl={'industrial-inspection-system.svg':'autonomous-industrial-inspection-hd.webp','fleet-observability-system.svg':'robot-fleet-observability-hd.webp','operations-intelligence-system.svg':'industrial-robot-operations-intelligence-hd.jpg'}
    for old,new in repl.items(): s=s.replace(f"assets/project/{old}",f"assets/project/{new}")
    s=s.replace('HD ILLUSTRATION','AI VISUAL • HD')
    INDEX.write_text(s,encoding='utf-8')

for slug,d in DATA.items():
    (FLOW_DIR/f'{slug}-detailed.svg').write_text(svg_for(slug,d),encoding='utf-8')
    patch_page(slug,d)
patch_index()
print(f'Applied objectives + detailed flowcharts to {len(DATA)} project pages and HD heroes to the three industrial projects.')

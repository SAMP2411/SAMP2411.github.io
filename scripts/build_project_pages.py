from pathlib import Path
import html

PROJECTS = [
    {
        'title':'Distributed State Estimation', 'slug':'distributed-state-estimation', 'icon':'fa-network-wired', 'accent':'#00f0ff',
        'status':'TU Dortmund Research Project', 'stack':'Yocto · Buildroot · RAUC · containerd · GitLab CI · QEMU · ARM Linux',
        'summary':'Designed the embedded-Linux deployment layer for a distributed state-estimation research project, focusing on minimal ARM images, secure A/B OTA updates, rollback and repeatable CI builds.',
        'challenge':'The project required an operating-system and deployment approach suitable for resource-constrained edge devices while still supporting reliable application delivery and remote maintenance.',
        'implementation':'Built a minimal Linux image first with Buildroot and later migrated the platform to Yocto Scarthgap. Integrated U-Boot, BusyBox, musl and containerd, and implemented RAUC A/B updates with RSA-4096 signing and rollback logic. QEMU qemuarm was used to validate images and update flows before hardware deployment.',
        'architecture':'Bootloader → A/B root filesystem → minimal userspace → container runtime → management layer → state-estimation application containers. OTA bundles are signed, written to the inactive slot and only promoted after successful boot validation.',
        'validation':'Verified A/B update behavior and rollback in QEMU, measured idle-memory behavior on the minimal image, and moved the build process into GitLab CI to make image generation repeatable.',
        'decisions':'The main trade-off was minimizing RAM and image complexity without removing the mechanisms needed for recoverable updates and containerized application delivery.',
        'repo':'https://gitlab.tu-dortmund.de/ie3/ie3_protection_and_automation/pgwise2526/-/tree/samarth?ref_type=heads'
    },
    {
        'title':'Telepresence Robot', 'slug':'telepresence-robot', 'icon':'fa-robot', 'accent':'#7000ff',
        'status':'Completed Robotics Project', 'stack':'ROS Noetic · GMapping · AMCL · move_base · DWA · Gazebo · RViz · Arduino',
        'summary':'Built a telepresence mobile robot covering mapping, localization, navigation, low-level motion control and a Gazebo digital twin.',
        'challenge':'The project combined mobile-base hardware, sensing and ROS navigation. The main engineering challenge was getting mapping, localization and motion control to behave coherently across simulation and the physical robot.',
        'implementation':'Used LiDAR-based GMapping to create occupancy-grid maps, AMCL for localization and move_base with DWA for local motion planning. Arduino-based motor control handled base actuation while ROS nodes connected perception, localization and navigation. A Gazebo model and RViz were used for debugging and visualization.',
        'architecture':'LiDAR/IMU/encoder data → ROS topics and TF → SLAM or AMCL → global/local navigation stack → velocity command → Arduino motor controller → differential-drive base.',
        'validation':'Tested the navigation workflow in simulation before transferring it to the real platform. Debugging focused on transforms, localization stability, map quality and whether commanded velocities were sufficient for the physical base.',
        'decisions':'Simulation was used as the first integration layer so navigation and frame issues could be isolated before involving hardware limitations such as motor choice and static friction.',
        'repo':'https://github.com/SAMP2411/Telepresence-Robot'
    },
    {
        'title':'Competitive Robotics', 'slug':'competitive-robotics', 'icon':'fa-trophy', 'accent':'#0aff64',
        'status':'Completed Team Robotics Work', 'stack':'Raspberry Pi · Arduino · Embedded C · PID · PS4 Control · Mechanism Automation',
        'summary':'Competition robotics work from DD Robocon involving operator control, embedded actuation, mechanism routines and rapid integration under event constraints.',
        'challenge':'Competition robots require mechanisms, electronics and control logic to work together reliably while the team iterates quickly around changing task strategies.',
        'implementation':'Worked with Raspberry Pi and Arduino-based control, including PS4 controller input, actuation routines and PID-oriented tuning. The work focused on integrating mechanisms into reliable task sequences rather than treating each actuator as an isolated subsystem.',
        'architecture':'Operator input → Raspberry Pi control layer → command logic → Arduino/embedded actuation → motors and mechanisms → task feedback and operator observation.',
        'validation':'Validation was practical and competition-oriented: repeated mechanism execution, tuning response and checking that combined action sequences were robust enough for event use.',
        'decisions':'The emphasis was on reliability and repeatability under time pressure, which is often more valuable in competition robotics than adding complex behavior that cannot be fully validated.',
        'repo':'https://github.com/SAMP2411/Robocon-2k22'
    },
    {
        'title':'Unmanned Ground Vehicle', 'slug':'unmanned-ground-vehicle', 'icon':'fa-car-battery', 'accent':'#ef4444',
        'status':'Completed Autonomous Vehicle Project', 'stack':'Python · Raspberry Pi · GPS · IMU · Kalman Filter · PID · Waypoint Navigation',
        'summary':'Implemented waypoint navigation for an autonomous ground vehicle using GPS/IMU state estimation and PID-based motion control.',
        'challenge':'Raw GPS and inertial measurements are noisy and arrive with different error characteristics, so navigation requires a usable state estimate before the controller can steer toward waypoints.',
        'implementation':'Implemented a Kalman-filter-based GPS/IMU fusion workflow in Python on Raspberry Pi, then used the estimated state for waypoint guidance and PID control. The project connected sensing, estimation and control into one navigation loop.',
        'architecture':'GPS + IMU → preprocessing/state update → Kalman filter → position/heading estimate → waypoint error → PID controller → drive commands.',
        'validation':'Tested waypoint-following behavior and observed position-estimation stability while tuning controller response. Reported project accuracy was typically below roughly 50 cm in the documented setup.',
        'decisions':'A standard Kalman filter was used because it matched the available state-estimation formulation and kept the implementation lightweight enough for the Raspberry Pi platform.',
        'repo':'https://github.com/SAMP2411/Unmanned_Ground_Vehicle'
    },
    {
        'title':'TurtleBot3 Autonomous Navigation', 'slug':'turtlebot3-navigation', 'icon':'fa-route', 'accent':'#00f0ff',
        'status':'Completed Academic Robotics Project', 'stack':'ROS2 · TurtleBot3 · Nav2 · SLAM · AMCL · TF · Gazebo · RViz',
        'summary':'Implemented a ROS2 autonomous-navigation workflow from bring-up and TF validation through mapping, probabilistic localization, planner evaluation and simulation-to-real testing.',
        'challenge':'Navigation failures can originate from perception, transforms, localization, costmaps or motion control, so the system had to be validated layer by layer rather than only checking whether the robot eventually reached a goal.',
        'implementation':'Verified robot bring-up, odometry and the TF tree, created maps using SLAM, saved and reused maps for navigation, localized with AMCL and sent autonomous waypoint goals through Nav2. Planner experiments also compared RRT, BiRRT and PRM approaches in the broader project workflow.',
        'architecture':'Sensors/odometry → TF tree → SLAM map or saved map → AMCL pose estimate → global planner → local controller/costmap → cmd_vel → TurtleBot3 base.',
        'validation':'Used Gazebo and RViz to inspect pose, map, paths, costmaps and sensor behavior before moving to the physical TurtleBot3. A real-world issue near the goal was traced partly to minimum velocity being too low for the loaded platform, and the threshold was increased to overcome static friction.',
        'decisions':'The project emphasized reproducible debugging: first confirm frame and odometry consistency, then localization, then planner/controller behavior, and only then tune hardware-specific motion limits.',
        'repo':''
    },
    {
        'title':'UR10 Manipulator Control', 'slug':'ur10-manipulator', 'icon':'fa-robot', 'accent':'#a855f7',
        'status':'Completed Academic Robotics Project', 'stack':'MATLAB · Simulink · Simscape · ROS · UR10 · FK/IK · Damped Least Squares',
        'summary':'Implemented manipulator kinematics and trajectory-control workflows for a UR10, including deterministic joint conversion utilities, DLS inverse kinematics and simulation-before-hardware validation.',
        'challenge':'Manipulator commands must remain consistent across joint naming, vector ordering, kinematic calculations and ROS trajectory messages. Small indexing or representation errors can produce unsafe or incorrect robot motion.',
        'implementation':'Worked with forward and inverse kinematics and damped least-squares updates. Helper functions mapped joint names to indexes, converted joint configurations into ordered vectors and transformed joint vectors into ROS-compatible trajectory messages. The motion-control workflow was exercised from MATLAB/ROS and visualized in simulation.',
        'architecture':'Target pose/configuration → FK/IK and DLS computation → ordered joint vector → time-parameterized trajectory → JointTrajectory message → simulated UR10 → validated hardware execution.',
        'validation':'Compared commanded motion in simulation before sending trajectories to the real robot. Joint-position and joint-trajectory control approaches were examined, with trajectory control providing smoother time-ordered motion in the project workflow.',
        'decisions':'Simulation-before-hardware and explicit joint-order conversion were treated as safety and reproducibility requirements rather than optional convenience layers.',
        'repo':''
    },
    {
        'title':'IIoT Anomaly Detector', 'slug':'iiot-anomaly-detector', 'icon':'fa-wave-square', 'accent':'#0aff64',
        'status':'Completed Industrial AI Project', 'stack':'Python · MQTT · Isolation Forest · scikit-learn · Plotly · Streaming Telemetry',
        'summary':'Built an edge-to-cloud style monitoring pipeline that streams sensor telemetry over MQTT, applies unsupervised anomaly detection and visualizes operating behavior.',
        'challenge':'Industrial telemetry needs to be processed continuously rather than only in an offline notebook, while anomaly detection must remain lightweight enough for a practical streaming pipeline.',
        'implementation':'Created MQTT publisher/subscriber components for simulated industrial sensor values such as temperature, vibration and current. The subscriber processed incoming data, applied an Isolation Forest model and surfaced anomalous points in a Plotly-based monitoring view.',
        'architecture':'Sensor/data generator → MQTT publisher → broker/topic → Python subscriber → preprocessing → Isolation Forest inference → anomaly log → Plotly dashboard.',
        'validation':'The documented implementation processed more than 5,000 sensor points and reported end-to-end pipeline latency below about 300 ms. Peak-like injected conditions were used to inspect whether the detector reacted as expected.',
        'decisions':'Isolation Forest was chosen because labelled failure data was not available. The project therefore treats model output as anomaly detection, not as a claim of labelled fault-classification accuracy.',
        'repo':'https://github.com/SAMP2411/AI-Based-IIoT-Anomaly-Detector'
    },
    {
        'title':'Offline Guided Face Enrollment and Recognition', 'slug':'offline-face-recognition', 'icon':'fa-user-check', 'accent':'#38bdf8',
        'status':'Completed Computer Vision Project', 'stack':'Python · OpenCV · InsightFace · ONNX Runtime · Offline Inference',
        'summary':'Built a fully local face-recognition workflow with guided multi-pose enrollment, pose-aware sample acceptance and real-time recognition.',
        'challenge':'Recognition quality depends heavily on enrollment quality. Accepting arbitrary frames can create weak identity representations, especially when pose or capture conditions are poor.',
        'implementation':'Used OpenCV for the camera pipeline and InsightFace models through ONNX Runtime for face analysis and representation. Enrollment guides the user through multiple poses and checks whether an input is suitable before accepting it. Recognition runs locally without depending on a cloud service.',
        'architecture':'Camera frame → face detection/analysis → pose and quality checks → embedding extraction → local enrollment store → live embedding → similarity decision → identity/unknown result.',
        'validation':'Tested live camera behavior and boundary cases such as weak inputs and pose inconsistency. The important validation target was not only successful matches, but whether the enrollment pipeline rejected samples that should not be stored.',
        'decisions':'The system was designed around guided enrollment because improving the stored reference data is often more reliable than trying to compensate for poor enrollment only at recognition time.',
        'repo':'https://github.com/SAMP2411/Face-Recognition-System'
    },
    {
        'title':'RST Hackathon — Vision-Guided Robot Arm', 'slug':'rst-hackathon', 'icon':'fa-trophy', 'accent':'#facc15',
        'status':'3rd Place · October 2025', 'stack':'Computer Vision · Tracking · Coordinate Transforms · Robot Manipulation · Rapid Prototyping',
        'summary':'Built a vision-guided robotic ball-throwing solution during a roughly 36–40 hour hackathon, combining perception, coordinate transformation, strategy and robot execution.',
        'challenge':'The system had to convert camera observations into usable robot actions within a very short development window, while still being reliable enough for competition attempts.',
        'implementation':'Integrated visual tracking with coordinate transformation logic and robot-arm action execution. The team developed a ball-throwing strategy and iterated on the full perception-to-action chain rather than optimizing the vision stage in isolation.',
        'architecture':'Camera/scene observation → target tracking/localization → coordinate convention/transform → strategy logic → robot-arm command sequence → throw execution.',
        'validation':'Repeated full task attempts were used to expose failures across perception, transforms and motion. Under time pressure, the team intentionally prioritized the most reliable executable strategy rather than adding higher-risk features that were not sufficiently validated.',
        'decisions':'The strongest engineering decision was scope control: simplify the strategy enough to make the entire system dependable. That trade-off contributed to a third-place finish.',
        'repo':''
    },
    {
        'title':'J&J MedTech Robotics & Controls Investigation', 'slug':'jj-medtech-robotics', 'icon':'fa-stethoscope', 'accent':'#fb7185',
        'status':'Completed Forage Job Simulation', 'stack':'Python · Robotic Control Diagnostics · Performance Testing · Engineering Documentation',
        'summary':'Investigated a simulated surgical-robot control issue by reviewing Python control code, measuring command behavior, iterating on changes and documenting the resulting performance improvement.',
        'challenge':'The simulated support ticket centered on delayed robot response. The task required distinguishing measured behavior from expected timing and identifying changes that could improve responsiveness without treating a single number as the whole problem.',
        'implementation':'Reviewed Python control logic for the simulated RBA-2201 robot and analyzed move_arm, rotate_joint and adjust_grip timings. After modification and retesting, measured times changed from 0.104/0.151/0.063 s to 0.083/0.121/0.041 s respectively.',
        'architecture':'Customer ticket → reproduce/measure command behavior → inspect control code → modify suspected logic → rerun timing tests → compare before/after → document findings and recommendations.',
        'validation':'Used iterative timing measurements rather than assuming a code change was successful. The final work included troubleshooting notes, corrective actions, validation results and a design-improvement proposal.',
        'decisions':'The project is presented explicitly as a Forage virtual job simulation, not employment. Its value is the engineering workflow: measure, diagnose, modify, retest and document.',
        'repo':''
    },
    {
        'title':'SO-101 Robot Learning', 'slug':'so101-robot-learning', 'icon':'fa-grip', 'accent':'#e879f9',
        'status':'In Development', 'stack':'SO-101 · Pick-and-Place · Zero-Shot · Few-Shot · In-Context Learning · Experiment Design',
        'summary':'Developing a controlled SO-101 pick-and-place study comparing zero-shot, few-shot and in-context learning under one common evaluation protocol.',
        'challenge':'The learning methods must be compared fairly: the task definition, observations, actions, reset conditions and evaluation metrics need to stay consistent across zero-shot, few-shot and in-context conditions.',
        'implementation':'The current work focuses on defining a common task interface, demonstration/context representation, trial protocol and machine-readable experiment logs. Because the development machine has 16 GB RAM and a GTX 1050 Ti, the simulation approach is intentionally lightweight rather than depending on Isaac Sim.',
        'architecture':'Task definition → observation/context preparation → learning condition (zero/few-shot/in-context) → action generation → pick-and-place execution → success/failure logging → comparison → eventual hardware transfer.',
        'validation':'Planned evaluation includes task success, completion behavior, failure/intervention type and any trajectory-quality measures that can be supported by the final implementation. No performance metric is claimed yet because the project is still in development.',
        'decisions':'The project deliberately separates planned evaluation from completed results. The strongest method will only be moved to physical SO-101 testing after it is stable in the lightweight experimental setup.',
        'repo':''
    }
]

HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="manifest" href="../site.webmanifest"><meta name="theme-color" content="#02040a"><script src="https://cdn.tailwindcss.com"></script><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"><link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;500;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet"><link rel="stylesheet" href="../project-detail.css"><script>tailwind.config={theme:{extend:{colors:{'cyber-blue':'#00f0ff','cyber-purple':'#7000ff','neon-green':'#0aff64'}}}}</script>'''

def esc(x): return html.escape(x, quote=True)

def page(p):
    repo = f'''<a href="{esc(p['repo'])}" target="_blank" class="inline-flex items-center px-5 py-3 border border-cyan-400/40 rounded text-cyan-300 hover:bg-cyan-400 hover:text-black tech"><i class="fab fa-github mr-2"></i>OPEN PROJECT REPOSITORY</a>''' if p['repo'] else '''<span class="inline-flex items-center px-5 py-3 border border-white/10 rounded text-gray-500 tech"><i class="fas fa-lock mr-2"></i>NO PUBLIC REPOSITORY LINK</span>'''
    blocks = [
      ('Engineering Challenge', p['challenge'], 'fa-triangle-exclamation'),
      ('Implementation', p['implementation'], 'fa-code'),
      ('System Architecture', p['architecture'], 'fa-diagram-project'),
      ('Validation & Debugging', p['validation'], 'fa-vial-circle-check'),
      ('Engineering Decisions', p['decisions'], 'fa-scale-balanced')]
    sections=''.join(f'''<section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl mb-4" style="color:{p['accent']}"><i class="fas {icon} mr-3"></i>{esc(title)}</h2><p class="text-gray-300 leading-8 text-lg">{esc(body)}</p></section>''' for title,body,icon in blocks)
    return HEAD + f'''<title>{esc(p['title'])} | Samarth Patel</title></head><body class="grid-bg min-h-screen"><nav class="sticky top-0 z-50 bg-black/90 backdrop-blur border-b border-cyan-400/20"><div class="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between"><a href="../index.html#projects" class="section-title text-white hover:text-cyan-300"><i class="fas fa-arrow-left mr-2"></i>FEATURED PROTOCOLS</a><a href="../index.html" class="tech text-cyan-300">SP.ROBOTICS</a></div></nav><main class="max-w-6xl mx-auto px-5 py-14 md:py-20"><header class="cyber-border rounded-2xl p-7 md:p-12 mb-8 relative overflow-hidden"><div class="absolute inset-0 opacity-10" style="background:radial-gradient(circle at 80% 10%,{p['accent']},transparent 42%)"></div><div class="relative"><div class="hero-icon text-5xl mb-6" style="color:{p['accent']}"><i class="fas {p['icon']}"></i></div><p class="tech uppercase tracking-[.22em] text-xs mb-3" style="color:{p['accent']}">{esc(p['status'])}</p><h1 class="section-title text-3xl md:text-5xl leading-tight mb-5">{esc(p['title'])}</h1><p class="text-gray-300 text-lg md:text-xl leading-8 max-w-4xl">{esc(p['summary'])}</p><div class="mt-7 inline-block px-4 py-2 rounded border border-white/10 bg-white/5 tech text-sm text-gray-300">{esc(p['stack'])}</div></div></header><div class="grid gap-6">{sections}<section class="glass rounded-xl p-6 md:p-8"><h2 class="section-title text-xl md:text-2xl text-cyan-300 mb-4"><i class="fas fa-link mr-3"></i>Project Access</h2><p class="text-gray-400 mb-5">This page documents the project using verified work and known implementation details. Public repository links are shown only where a valid public source is available.</p>{repo}</section></div><div class="mt-10 flex justify-between items-center"><a href="../index.html#projects" class="tech text-gray-400 hover:text-cyan-300"><i class="fas fa-arrow-left mr-2"></i>BACK TO PROJECTS</a><a href="#top" class="tech text-gray-400 hover:text-cyan-300">TOP <i class="fas fa-arrow-up ml-2"></i></a></div></main></body></html>'''

def compact_and_link_index():
    path=Path('index.html')
    text=path.read_text(encoding='utf-8')
    start=text.find('<section id="projects"')
    if start<0: raise SystemExit('projects section not found')
    end=text.find('</section>', start)
    if end<0: raise SystemExit('projects section end not found')
    end += len('</section>')
    section=text[start:end]
    section=section.replace('h-52 relative overflow-hidden tilt-inner','h-28 relative overflow-hidden tilt-inner')
    section=section.replace('p-8 relative tilt-inner','p-5 relative tilt-inner')
    section=section.replace('text-2xl font-bold text-white font-mono','text-xl font-bold text-white font-mono')
    section=section.replace('text-gray-400 text-sm mb-6','text-gray-400 text-sm mb-3')
    section=section.replace('group cursor-none rounded-xl','group cursor-pointer rounded-xl')
    for p in PROJECTS:
        title=p['title']
        # Older homepage titles use slightly different labels.
        aliases={
          'RST Hackathon — Vision-Guided Robot Arm':'RST Hackathon',
          'J&J MedTech Robotics & Controls Investigation':'J&J MedTech Robotics & Controls',
          'Offline Guided Face Enrollment and Recognition':'Offline Face Recognition',
          'SO-101 Robot Learning':'SO-101 Robot Learning'
        }
        needle=aliases.get(title,title)
        pos=section.find('>'+needle+'<')
        if pos<0:
            print('warning: card title not found:', needle); continue
        card=section.rfind('<div class="tilt-card',0,pos)
        close=section.find('>',card)
        tag=section[card:close+1]
        url=f"project/{p['slug']}.html"
        if 'data-project-detail=' not in tag:
            newtag=tag[:-1]+f' data-project-detail="{url}" role="link" tabindex="0" onclick="if(!event.target.closest(\'a\')) window.location.href=\'{url}\'" onkeydown="if(event.key===\'Enter\' || event.key===\' \') window.location.href=\'{url}\'">'
            section=section[:card]+newtag+section[close+1:]
    text=text[:start]+section+text[end:]
    path.write_text(text,encoding='utf-8')

Path('project').mkdir(exist_ok=True)
for p in PROJECTS:
    Path('project',p['slug']+'.html').write_text(page(p),encoding='utf-8')
compact_and_link_index()
print(f'Generated {len(PROJECTS)} detail pages and patched Featured Protocols cards.')

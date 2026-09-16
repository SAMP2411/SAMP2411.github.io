#!/usr/bin/env python3
"""Build dependency-free, accessible portfolio pages from reviewed project data."""
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/projects.json').read_text())
PROJECTS = {p['slug']: p for p in DATA}
SITE = 'https://samp2411.github.io/'
EMAIL = 'samarthp2411@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/samarth-patel-206451197/'
FEATURED = ['turtlebot3-navigation', 'distributed-state-estimation', 'ur10-manipulator']
DOMAIN_MAP = {'Mobile robotics':'autonomy', 'Embedded systems':'embedded', 'Manipulation':'manipulation', 'Industrial AI':'industrial-ai', 'Computer vision':'perception', 'Robot learning':'manipulation', 'Industrial robotics':'autonomy industrial-ai', 'Industrial software':'industrial-ai'}
DATES = {'distributed-state-estimation':'Oct 2025 – Mar 2026', 'turtlebot3-navigation':'Nov 2024 – Apr 2025', 'ur10-manipulator':'2025', 'telepresence-robot':'Jan – May 2024', 'iiot-anomaly-detector':'Jul – Sep 2024', 'offline-face-recognition':'Nov 2024 – Apr 2025', 'rst-hackathon':'October 2025', 'unmanned-ground-vehicle':'Jan – Mar 2021', 'competitive-robotics':'2020 – 2022'}
EXPERIENCE = [
 ('From Oct 2026', 'Incoming working student', 'B. Braun · AI, Robotics & Industrial System Integration', 'Accepted offer; planned start 1 October 2026 in Melsungen. Role has not started yet.', None),
 ('Apr 2026 – present', 'Software Engineer (Student)', 'GETracing Dortmund e.V.', 'Localization robustness, sensor uncertainty and map consistency. Reproducible ROS debugging through TF analysis, recorded data and systematic fault isolation.', None),
 ('Oct 2025 – Mar 2026', 'Embedded platform & deployment', 'Research project · ie³, TU Dortmund', 'Built the operating-system and remote-update layer for a constrained ARM state-estimation platform: Yocto, RAUC A/B updates, rollback, containerd and repeatable CI builds.', 'project/distributed-state-estimation.html'),
 ('September 2026', 'Robotics & Controls Job Simulation', 'Johnson & Johnson MedTech · Forage', 'Virtual job simulation: reviewed Python control code, investigated command-response delays, iterated on changes, retested and documented the findings. Not employment at Johnson & Johnson.', 'experience/jj-medtech-robotics.html'),
 ('Jan – Jul 2024', 'ML & Data Science Trainee', 'GeeksforGeeks', 'Built Python data workflows, regression and classification experiments, cross-validation and automation tooling.', None),
 ('Oct 2023 – Jan 2024', 'Electronics Production Intern', 'Omsara Industries', 'Assembled and tested 50+ PCBs, debugged electronics and checked I2C/SPI interfaces with laboratory instrumentation.', None),
 ('Jun – Sep 2023', 'Manufacturing Support Intern', 'Ashlesh Bright Bars Pvt. Ltd.', 'Supported calibration, maintenance, process documentation and manufacturing improvement work.', None),
]
DOMAINS = [
 ('01', 'Mobile robotics', 'ROS2 · Nav2 · SLAM · AMCL · TF2', 'Mapping, localization and autonomous waypoint execution, from simulation to physical robot integration.', ['turtlebot3-navigation','telepresence-robot','autonomous-industrial-inspection-robot']),
 ('02', 'Manipulation', 'FK / IK · DLS · Trajectories · ROS', 'Connecting kinematic models, coordinate frames and controller interfaces to deliberate robot motion.', ['ur10-manipulator','rst-hackathon','so101-robot-learning']),
 ('03', 'Embedded & deployment', 'Yocto · Buildroot · RAUC · CI/CD', 'Reproducible Linux platforms, recoverable updates and deployment under real hardware constraints.', ['distributed-state-estimation','competitive-robotics']),
 ('04', 'Perception', 'OpenCV · InsightFace · ONNX · Sensing', 'Camera pipelines, local inference and sensor observations that support reliable downstream decisions.', ['offline-face-recognition','rst-hackathon']),
 ('05', 'Industrial AI & operations', 'MQTT · FastAPI · Telemetry · Diagnostics', 'Anomaly alerts, fleet visibility and evidence-linked incident analysis in documented prototypes.', ['iiot-anomaly-detector','robot-fleet-observability-platform','industrial-robot-operations-intelligence']),
 ('06', 'Control & estimation', 'PID · Kalman filtering · State estimation', 'Reasoning about noisy measurements and connecting state estimates to controllable motion.', ['unmanned-ground-vehicle','ur10-manipulator']),
]

def esc(value):
    return html.escape(str(value), quote=True)

def tags(values):
    return '<ul class="tags" aria-label="Technologies">' + ''.join(f'<li>{esc(v)}</li>' for v in values) + '</ul>'

def dims(path):
    if path.endswith('.svg') and (ROOT/path).exists():
        node = ET.parse(ROOT/path).getroot()
        vb = node.get('viewBox', '').split()
        if len(vb) == 4: return int(float(vb[2])), int(float(vb[3]))
    audit = ROOT/'docs/image-dimensions.json'
    if audit.exists():
        for item in json.loads(audit.read_text()):
            if item['path'] == path and 'width' in item: return item['width'], item['height']
    return {'profile.jpg':(1792,2400),'project2.jpg':(887,592),'project4.jpg':(3000,4000)}.get(path,(1600,1000))

def image(path, alt, prefix='', eager=False, cls=''):
    w,h = dims(path)
    return f'<img src="{prefix}{esc(path)}" alt="{esc(alt)}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async" class="{cls}">'

def section_heading(number, title, detail='', link=''):
    return f'<div class="section-heading"><div><span class="section-number">{number} / ENGINEERING PORTFOLIO</span><h2>{esc(title)}</h2></div>{f"<p>{esc(detail)}</p>" if detail else ""}{link}</div>'

def layout(title, desc, content, path, scene=False, modal=False):
    prefix = '../' if '/' in path else ''
    nav = [('projects.html','Projects'),('experience.html','Experience'),('skills.html','Skills'),('about.html','About')]
    links = ''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if path==url else '')+f'>{label}</a>' for url,label in nav)
    schema = {'@context':'https://schema.org','@type':'Person','name':'Samarth Patel','url':SITE,'sameAs':['https://github.com/SAMP2411',LINKEDIN],'jobTitle':'Robotics Software Engineer','alumniOf':{'@type':'CollegeOrUniversity','name':'SRM Institute of Science and Technology'}}
    dialog = ''
    if modal:
        brief = [{k:p[k] for k in ['slug','title','summary','status','image','tags','contributions']} for p in DATA]
        dialog = '<dialog id="project-dialog" class="dialog" aria-label="Project quick view"><button class="dialog-close" type="button" aria-label="Close project quick view">×</button><div class="dialog-content"></div></dialog><script id="project-data" type="application/json">'+json.dumps(brief).replace('<','\\u003c')+'</script>'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Samarth Patel</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#090f16">
<link rel="canonical" href="{SITE}{'' if path=='index.html' else path}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="manifest" href="{prefix}site.webmanifest">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} | Samarth Patel"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{SITE}{'' if path=='index.html' else path}"><meta property="og:image" content="{SITE}profile.jpg"><meta property="og:image:alt" content="Samarth Patel"><meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{prefix}site.css"><link rel="stylesheet" href="{prefix}refinements.css">{f'<link rel="stylesheet" href="{prefix}scene.css">' if scene else ''}<script src="{prefix}site.js" defer></script>{f'<script src="{prefix}scene.js" defer></script>' if scene else ''}
<script type="application/ld+json">{json.dumps(schema)}</script></head><body>
<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container"><a class="brand" href="{prefix}index.html" aria-label="Samarth Patel home"><span class="brand-mark" aria-hidden="true">SP</span>SAMARTH PATEL</a><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" hidden>Menu</button><nav class="nav-links" id="primary-nav" aria-label="Primary">{links}<a href="{prefix}resume.html" class="button small">Résumé ↗</a><a href="{prefix}index.html#contact">Contact</a></nav></div></header>
<main id="main" class="container">{content}</main>{dialog}
<footer class="site-footer"><div class="container"><span>© 2026 Samarth Patel · Robotics, software & systems.</span><div class="social-links"><a href="https://github.com/SAMP2411">GitHub ↗</a><a href="{LINKEDIN}">LinkedIn ↗</a><a href="mailto:{EMAIL}">Email ↗</a></div></div></footer></body></html>'''

def card(p, prefix='', quick=False):
    slug=p['slug']; href=f'{prefix}project/{slug}.html'
    return f'''<article class="project-card" data-domains="{DOMAIN_MAP[p['domain']]}"><a class="card-visual" href="{href}" tabindex="-1" aria-hidden="true">{image(p['image'], '',prefix)}<span class="image-label">{esc(p.get('image_kind','Illustrative visualization'))}</span></a><div class="card-body"><span class="card-domain">{esc(p['domain'])}</span><h3 class="card-title"><a href="{href}">{esc(p['title'])}</a></h3><p class="card-summary">{esc(p['summary'])}</p>{tags(p['tags'][:4])}<p class="project-status">{esc(p['status'])}</p><div class="card-actions"><a class="text-link" href="{href}">Case study <span aria-hidden="true">↗</span></a>{f'<button type="button" class="button small" data-quick-view="{slug}" hidden>Quick view</button>' if quick else ''}</div></div></article>'''

def experience(limit=None):
    rows=''
    for date,role,company,body,link in EXPERIENCE[:limit]:
        rows+=f'<article class="experience-row"><div class="experience-date">{esc(date)}</div><div class="experience-body"><h3>{esc(role)}</h3><p class="experience-company">{esc(company)}</p><p>{esc(body)}</p>{f"<a class=\"text-link\" href=\"{link}\">Explore the work ↗</a>" if link else ""}</div></article>'
    return '<div class="experience-list">'+rows+'</div>'

def domains():
    return '<div class="domain-grid">'+''.join(f'<article class="domain-card"><span class="eyebrow">{n} / CAPABILITY</span><h3>{title}</h3><p>{stack}</p><p>{body}</p><ul class="evidence-links">'+''.join(f'<li><a href="project/{slug}.html">{esc(PROJECTS[slug]["title"])} ↗</a></li>' for slug in slugs)+'</ul></article>' for n,title,stack,body,slugs in DOMAINS)+'</div>'

def contact():
    return f'<section id="contact" class="section"><div class="contact-panel"><div><span class="eyebrow">LET’S CONNECT</span><h2>Let’s build reliable<br>robotic systems.</h2><p>Robotics software, autonomous systems and the engineering that connects them.</p></div><div><a class="button primary" href="mailto:{EMAIL}">Get in touch ↗</a><p class="contact-email"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></section>'

def write(path, text):
    (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/path).write_text(text+'\n')

def build():
    scene=(ROOT/'assets/robotics-scene.svg').read_text()
    hero=f'''<section class="hero"><div class="hero-copy"><span class="eyebrow">ROBOTICS · SOFTWARE · SYSTEMS</span><h1 class="hero-name">Samarth<br>Patel<span class="name-dot">.</span></h1><p class="hero-role">Robotics Software Engineer</p><p class="hero-summary">Building robotic systems across mobile autonomy, manipulation, perception and embedded deployment. From the algorithm to the robot.</p><div class="hero-actions"><a class="button primary" href="projects.html">Explore projects ↗</a><a class="button" href="resume.html">View résumé</a></div><div class="social-links"><a href="https://github.com/SAMP2411">GitHub ↗</a><a href="{LINKEDIN}">LinkedIn ↗</a><a href="#contact">Contact ↗</a></div><div class="hero-meta"><span>Dortmund, Germany</span><span>M.Sc. Automation & Robotics · TU Dortmund</span></div></div><div class="hero-visual"><figure class="robotics-visual">{scene}<figcaption class="scene-caption"><span>Conceptual robotics workspace</span><button class="scene-toggle" type="button" aria-pressed="false" hidden>Pause motion</button></figcaption></figure></div></section>'''
    snapshot='<div class="snapshot" aria-label="Engineering snapshot">'+''.join(f'<a class="snapshot-item" href="projects.html?domain={d}"><strong>{label}</strong><span>{s}</span></a>' for d,label,s in [('autonomy','Mobile autonomy','ROS2 · SLAM · Nav2'),('manipulation','Manipulation','Kinematics · Trajectories · Control'),('embedded','Embedded platforms','Yocto · RAUC · CI/CD'),('perception','Perception & AI','OpenCV · ONNX · Sensor data')])+'</div>'
    featured='<section id="projects" class="section">'+section_heading('01','Selected engineering work',link='<a class="text-link" href="projects.html">All 13 projects ↗</a>')+'<div class="project-grid">'+''.join(card(PROJECTS[s],quick=True) for s in FEATURED)+'</div><div class="project-extension"><span class="eyebrow">ALSO IN THE WORKSHOP</span><p>From inspection missions to fleet telemetry and incident diagnostics.</p><a href="project/industrial-robot-operations-intelligence.html" class="text-link">Explore the industrial robotics capstone ↗</a></div></section>'
    capability='<section id="skills" class="section">'+section_heading('02','Across the robotics stack','Capabilities linked to the work that demonstrates them. No skill scores. Just engineering evidence.')+domains()+'</section>'
    exp='<section id="experience" class="section">'+section_heading('03','Experience, in context',link='<a class="text-link" href="experience.html">Full experience ↗</a>')+experience(4)+'</section>'
    approach='<section id="approach" class="section">'+section_heading('04','Understand. Integrate. Validate.','A systems-first approach: make behavior observable, isolate the failing layer, and make the next change testable.')+'<div class="approach-grid">'+''.join(f'<article class="approach-item"><span class="eyebrow">0{i}</span><h3>{t}</h3><p>{b}</p></article>' for i,t,b in [(1,'Model the system','Start with frames, interfaces, constraints and failure modes—not only the nominal behavior.'),(2,'Integrate in layers','Verify sensing, transforms, estimation and control before tuning the complete robot.'),(3,'Measure behavior','Use recorded data, simulation, diagnostics and repeatable scenarios to understand the fault.'),(4,'Validate the change','Retest under the same conditions. Document the result and the boundaries of the evidence.')])+'</div></section>'
    write('index.html',layout('Robotics Software Engineer','Samarth Patel — robotics software, mobile autonomy, manipulation and embedded Linux. M.Sc. Automation & Robotics at TU Dortmund.',hero+snapshot+featured+capability+exp+approach+contact(),'index.html',True,True))
    filters='<div class="filters" aria-label="Filter projects">'+''.join(f'<button type="button" class="filter-button" data-filter="{v}" aria-pressed="{"true" if v=="all" else "false"}" disabled>{label}</button>' for v,label in [('all','All projects'),('autonomy','Autonomy'),('manipulation','Manipulation'),('embedded','Embedded'),('perception','Perception'),('industrial-ai','Industrial AI')])+'</div>'
    ordered=FEATURED+[p['slug'] for p in DATA if p['slug'] not in FEATURED]
    body='<header class="page-header"><span class="eyebrow">PROJECT EXPLORER</span><h1>Engineering, with evidence.</h1><p>Explore the systems, the implementation decisions and the debugging behind them. Each case study distinguishes completed work, simulation and ongoing development.</p></header>'+filters+'<p id="project-count" class="result-count" role="status" aria-live="polite">13 projects</p><noscript><p>All projects are shown. Filters and quick views require JavaScript; every case study remains accessible.</p></noscript><div class="project-grid project-index">'+''.join(card(PROJECTS[s],quick=True) for s in ordered)+'</div>'+contact()
    write('projects.html',layout('Projects','Thirteen robotics and embedded software case studies: objectives, architecture, contributions, implementation and validation.',body,'projects.html',modal=True))
    for p in DATA: build_case(p)
    body='<header class="page-header"><span class="eyebrow">EXPERIENCE</span><h1>Software meets<br>physical systems.</h1><p>Research, student engineering, technical training and industrial experience. Roles and simulation exercises are labelled separately.</p></header>'+experience()+contact()
    write('experience.html',layout('Experience','Research, student engineering and industrial experience across robotics, embedded platforms and electronics.',body,'experience.html'))
    body='<header class="page-header"><span class="eyebrow">CAPABILITIES & EVIDENCE</span><h1>A connected engineering stack.</h1><p>Technologies are useful when they solve a system problem. Follow each capability into the projects where I used it.</p></header>'+domains()+'<section class="section prose"><h2>Programming & engineering tools</h2>'+tags(['Python','C++','Embedded C','MATLAB','Bash','Git','Linux','Docker','SolidWorks','Jira','Confluence'])+'<p>My project work spans algorithm implementation, robotics middleware, simulation, hardware integration, deployment and reproducible testing. Individual case studies describe the depth and context of each technology.</p></section>'+contact()
    write('skills.html',layout('Skills','Robotics capabilities connected to project evidence: ROS2, navigation, manipulation, embedded Linux, perception and industrial AI.',body,'skills.html'))
    about='<header class="page-header"><span class="eyebrow">ABOUT</span><h1>Curious about the algorithm.<br>Responsible for the system.</h1></header><div class="about-grid"><div class="prose"><p>I’m Samarth Patel, an M.Sc. Automation & Robotics student at TU Dortmund University. I focus on robotics software: the connections between sensing, estimation, planning, control and the platforms that run them.</p><p>My work ranges from ROS navigation and UR10 kinematics to resource-constrained embedded Linux and recoverable software updates. I enjoy the integration problems that appear between components—and the process of making those problems reproducible.</p><p>I’m based in Dortmund, Germany, with an upcoming working-student role in AI, Robotics & Industrial System Integration at B. Braun in Melsungen, planned for October 2026.</p><h2>Education</h2><h3>M.Sc. Automation & Robotics</h3><p>TU Dortmund University · October 2024 – present</p><p>Coursework includes mobile robots, 3D computer vision, robotic manipulators, control theory and automated driving.</p><h3>B.Tech. Mechatronics Engineering</h3><p>SRM Institute of Science and Technology · 2019 – 2023</p><h2>Languages</h2><p>English (C1), German (A2), Hindi and Gujarati.</p></div><figure>'+image('profile.jpg','Samarth Patel',eager=True,cls='portrait')+'<figcaption class="portrait-caption">Robotics · Software · Systems</figcaption></figure></div>'+contact()
    write('about.html',layout('About','Samarth Patel, M.Sc. Automation & Robotics student at TU Dortmund, focused on robotics software and dependable system integration.',about,'about.html'))
    resume='<header class="page-header"><span class="eyebrow">RÉSUMÉ / WEB EDITION</span><h1>Samarth Patel</h1><p>Robotics Software Engineer · M.Sc. Automation & Robotics<br>Dortmund, Germany · <a href="mailto:'+EMAIL+'">'+EMAIL+'</a></p><p class="print-note">This is the concise web résumé. Use your browser’s Print → Save as PDF for an offline copy.</p></header><section class="prose"><h2>Profile</h2><p>Robotics software and automation engineer with project experience in ROS/ROS2 navigation, manipulation, computer vision and embedded Linux. Systems-first debugging, simulation-to-real integration and recoverable deployment workflows.</p><h2>Core technologies</h2>'+tags(['Python','C++','ROS2','Nav2','SLAM / AMCL','FK / IK','Yocto','Buildroot','RAUC','OpenCV','ONNX','GitLab CI'])+'</section><section class="section"><h2>Experience</h2>'+experience()+'</section><section class="section prose"><h2>Selected projects</h2>'+''.join(f'<h3><a href="project/{s}.html">{esc(PROJECTS[s]["title"])}</a></h3><p>{esc(PROJECTS[s]["summary"])}</p>' for s in FEATURED)+'<h2>Education</h2><p><strong>M.Sc. Automation & Robotics</strong><br>TU Dortmund · October 2024 – present</p><p><strong>B.Tech. Mechatronics Engineering</strong><br>SRM IST · 2019 – 2023</p><h2>Languages</h2><p>English C1 · German A2 · Hindi · Gujarati</p></section>'
    write('resume.html',layout('Résumé','Concise web résumé for Samarth Patel: robotics, embedded Linux, experience, education and selected engineering projects.',resume,'resume.html'))
    build_forage()
    write('404.html',layout('Page not found','Return to Samarth Patel’s robotics portfolio.','<section class="section prose"><span class="eyebrow">404 / ROUTE NOT FOUND</span><h1>This path needs replanning.</h1><p>The page may have moved. Explore the project archive or return to the portfolio.</p><div class="hero-actions"><a class="button primary" href="/index.html">Return home</a><a class="button" href="/projects.html">Explore projects</a></div></section>','404.html'))
    paths=['','projects.html','experience.html','skills.html','about.html','resume.html','experience/jj-medtech-robotics.html']+['project/'+p['slug']+'.html' for p in DATA]
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+SITE+p+'</loc></url>' for p in paths)+'</urlset>')
    write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+SITE+'sitemap.xml')
    print(f'Built {len(paths)+1} pages with 13 project case studies.')

def build_case(p):
    prefix='../'; slug=p['slug']
    sections=[('objective','Objective'),('contribution','My contribution'),('architecture','System architecture'),('implementation','Implementation'),('decisions','Engineering decisions'),('challenges','Challenges & debugging'),('validation','Validation'),('outcome','Outcome & boundaries'),('links','Project sources')]
    hero=f'<header class="case-header"><a class="text-link" href="../projects.html">← All projects</a><span class="eyebrow">{esc(p["domain"])} / {esc(p["status"])}</span><h1>{esc(p["title"])}</h1><p>{esc(p["summary"])}</p><div class="case-meta"><span><strong>Role</strong><br>{esc(p["role"])}</span><span><strong>Timeline</strong><br>{esc(DATES.get(slug,p["timeline"]))}</span></div>{tags(p["tags"])}<div class="hero-actions"><a class="button primary" href="#architecture">Explore architecture ↓</a>'+''.join(f'<a class="button" href="{esc(l["url"])}">{esc(l["label"])} ↗</a>' for l in p['links'])+'</div></header>'
    visual=f'<figure class="case-visual">{image(p["image"],p["title"]+" — "+p.get("image_kind","illustration"),prefix,eager=True)}<figcaption>{esc(p.get("image_kind","Illustrative visualization"))}. Project media and architecture are shown separately; illustrations are not evidence of hardware testing.</figcaption></figure>'
    nav='<nav class="case-nav" aria-label="On this page">'+''.join(f'<a href="#{i}">{label}</a>' for i,label in sections)+'</nav>'
    flow=p['flowchart']['image']
    architecture='<p>'+esc(p['architecture'])+'</p><figure class="flowchart-panel">'+image(flow,p['title']+' explanatory system flowchart',prefix,cls='flowchart-image')+'<figcaption>'+esc(p['flowchart']['caption'])+'</figcaption></figure><a class="text-link" href="../'+flow+'">Open full-size diagram ↗</a><details><summary>Read the architecture as text</summary><ol>'+''.join('<li><strong>'+esc(n['label'])+'</strong> — '+esc(n['detail'])+'</li>' for n in p['flowchart']['nodes'])+'</ol></details>'
    content={'objective':'<p>'+esc(p['objective'])+'</p><ul>'+''.join('<li>'+esc(v)+'</li>' for v in p['goals'])+'</ul>', 'contribution':'<ul>'+''.join('<li>'+esc(v)+'</li>' for v in p['contributions'])+'</ul>', 'architecture':architecture}
    for k in ['implementation','decisions','challenges','validation','outcome']: content[k]='<p>'+esc(p[k])+'</p>'
    content['links']='<p>Implementation notes and available project sources. Public code is linked where available; descriptive diagrams are not independent validation.</p>'+(''.join(f'<p><a href="{esc(l["url"])}">{esc(l["label"])} ↗</a></p>' for l in p['links']) if p['links'] else '<p>No public repository is linked for this project.</p>')
    article='<div class="case-layout">'+nav+'<article class="case-content">'+''.join(f'<section class="case-section" id="{i}"><h2>{label}</h2>{content[i]}</section>' for i,label in sections)+'</article></div>'
    related=sorted([x for x in DATA if x['slug']!=slug],key=lambda x:x['domain']!=p['domain'])[:2]
    related_html='<section class="section"><h2>Related engineering</h2><div class="related-grid">'+''.join(card(x,prefix) for x in related)+'</div></section>'
    write('project/'+slug+'.html',layout(p['title'],p['summary'],hero+visual+article+related_html,'project/'+slug+'.html'))

def build_forage():
    body='<header class="case-header"><a class="text-link" href="../experience.html">← Experience</a><span class="eyebrow">FORAGE / VIRTUAL JOB SIMULATION / SEPTEMBER 2026</span><h1>Robotics & Controls<br>troubleshooting.</h1><p>Johnson & Johnson MedTech job simulation: investigating delayed response in a simulated robotic arm through code review, measurement and iterative testing.</p></header><div class="prose"><section class="case-section"><h2>Context & scope</h2><p>This was an educational virtual job simulation on Forage, not employment at Johnson & Johnson or work on a deployed surgical robot. The exercise followed a customer-reported command-response issue.</p></section><section class="case-section"><h2>My contribution</h2><ul><li>Reviewed the reported delay and inspected Python robotic-control functions.</li><li>Compared command behavior including move_arm, rotate_joint and adjust_grip.</li><li>Iterated on code changes and retested response behavior.</li><li>Documented troubleshooting, corrective actions and recommendations.</li></ul></section><section class="case-section"><h2>Engineering workflow</h2><p>Reproduce the symptom → instrument response times → inspect the control path → modify the cause → repeat the test → document the result.</p></section><section class="case-section"><h2>What I took away</h2><p>A slower command is a symptom, not a diagnosis. Timing evidence helps separate algorithm behavior, software delay and system assumptions before proposing a fix. The exercise reinforced a measured, repeatable troubleshooting process.</p></section><section class="case-section"><h2>Validation boundary</h2><p>Results belong to the supplied simulation exercise. They are not clinical, hardware safety or real-time performance guarantees.</p></section></div>'
    write('experience/jj-medtech-robotics.html',layout('Robotics & Controls Job Simulation','Forage virtual job simulation: Python robot-control debugging, command timing, iterative testing and documentation.',body,'experience/jj-medtech-robotics.html'))

if __name__=='__main__': build()

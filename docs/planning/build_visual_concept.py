"""Render review-only UI compositions; does not build or alter the live website."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, math
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
P=json.loads((ROOT/'data/projects.json').read_text())
featured=['turtlebot3-navigation','distributed-state-estimation','ur10-manipulator']
P.sort(key=lambda p:featured.index(p['slug']) if p['slug'] in featured else 3)
BG='#080f17'; SURFACE='#101c28'; LINE='#26394a'; TEXT='#edf4f7'; MUTED='#a5b6c6'; CYAN='#7ee4eb'; ORANGE='#ecc28b'
F='/usr/share/fonts/truetype/dejavu/'
def font(n,b=False,mono=False):return ImageFont.truetype(F+('DejaVuSansMono' if mono else 'DejaVuSans')+('-Bold' if b else '')+'.ttf',n)
class Canvas:
 def __init__(self,w,h): self.im=Image.new('RGB',(w,h),BG);self.d=ImageDraw.Draw(self.im)
 def text(self,x,y,t,n=14,c=TEXT,b=False,mono=False):self.d.text((x,y),t,font=font(n,b,mono),fill=c)
 def rule(self,x,y,w,c=LINE):self.d.line((x,y,x+w,y),fill=c,width=1)
 def box(self,x,y,w,h,fill=SURFACE,outline=LINE,r=10):self.d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=outline)
 def wrap(self,x,y,t,w,n=14,c=MUTED,b=False,leading=None):
  f=font(n,b);line='';yy=y;step=leading or n+6
  for word in t.split():
   candidate=(line+' '+word).strip()
   if line and self.d.textlength(candidate,font=f)>w:self.text(x,yy,line,n,c,b);yy+=step;line=word
   else:line=candidate
  if line:self.text(x,yy,line,n,c,b);yy+=step
  return yy
 def button(self,x,y,w,t,active=False):self.box(x,y,w,40,CYAN if active else SURFACE,CYAN if active else LINE,6);self.text(x+12,y+12,t,12,BG if active else TEXT,True)
 def image(self,p,x,y,w,h):
  im=ImageOps.exif_transpose(Image.open(ROOT/p)).convert('RGB');im=ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS)
  mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=7,fill=255);self.im.paste(im,(x,y),mask)
 def save(self,name):self.im.save(OUT/name,'WEBP',quality=87,method=6)
short={'offline-face-recognition':'Offline Face Recognition','rst-hackathon':'Vision-Guided Robot Arm','autonomous-industrial-inspection-robot':'Industrial Inspection Robot','industrial-robot-operations-intelligence':'Robot Operations Intelligence'}
scopes={'distributed-state-estimation':'RESEARCH','turtlebot3-navigation':'SIM + HARDWARE','ur10-manipulator':'ACADEMIC','so101-robot-learning':'IN DEVELOPMENT','autonomous-industrial-inspection-robot':'SIMULATION','robot-fleet-observability-platform':'SOFTWARE','industrial-robot-operations-intelligence':'SOFTWARE'}
def card(c,p,x,y,w,h=208):
 c.box(x,y,w,h)
 if p['slug'] in featured:c.rule(x+16,y,56,CYAN)
 c.image(p['image'],x+16,y+18,88,66)
 c.wrap(x+118,y+18,short.get(p['slug'],p['title']),w-134,15,TEXT,True,19)
 c.text(x+16,y+101,scopes.get(p['slug'],'PROJECT'),9,ORANGE,mono=True)
 desc=p['summary'];desc={'distributed-state-estimation':'Embedded Linux, signed updates and recoverable deployment.','turtlebot3-navigation':'Mapping, localization and autonomous waypoint navigation.','ur10-manipulator':'Kinematics, controller integration and trajectory execution.'}.get(p['slug'],desc)
 # Deliberate short display summaries; full detail belongs in the preview.
 brief={'telepresence-robot':'ROS mapping, localization and Arduino drive integration.','competitive-robotics':'Operator controls and embedded robot actuation.','unmanned-ground-vehicle':'GPS/IMU estimation and waypoint control.','iiot-anomaly-detector':'Anomaly prediction from synthetic industrial telemetry.','offline-face-recognition':'Guided enrollment and local face inference.','rst-hackathon':'Camera tracking connected to robot-arm execution.','so101-robot-learning':'A controlled study of robot-learning methods.','autonomous-industrial-inspection-robot':'Inspection patrol simulation and evidence capture.','robot-fleet-observability-platform':'Fleet telemetry and tenant-aware operator views.','industrial-robot-operations-intelligence':'Evidence-linked findings and incident diagnostics.'}
 c.wrap(x+16,y+120,brief.get(p['slug'],desc),w-32,12,MUTED,leading=17)
 c.rule(x+16,y+h-42,w-32);c.text(x+16,y+h-29,'View project',12,CYAN,True);c.text(x+w-32,y+h-30,'→',16,CYAN)
def section(c,y,label,title,w):c.text(32,y,label,10,CYAN,mono=True);c.text(32,y+24,title,28,TEXT,True)

c=Canvas(1440,2120)
c.text(32,16,'VISUAL CONCEPT / 01     •     REVIEW ONLY',10,MUTED,mono=True)
c.text(32,63,'Samarth Patel',20,TEXT,True);c.text(935,70,'Work    Experience    About',13,MUTED);c.button(1190,55,98,'Résumé');c.text(1316,70,'Contact',12,CYAN);c.rule(32,113,1376)
c.text(32,151,'ROBOTICS SOFTWARE / SYSTEMS ENGINEERING',11,CYAN,mono=True)
c.text(32,184,'Samarth Patel',58,TEXT,True)
c.text(32,262,'Robotics software. From algorithm to integration.',23,TEXT)
c.wrap(32,310,'ROS2 navigation, robot manipulation and dependable embedded Linux.',780,17)
c.text(32,353,'M.Sc. Automation & Robotics · TU Dortmund · Dortmund, Germany',13,MUTED)
c.button(32,390,152,'Explore work ↓',True);c.button(196,390,110,'View résumé');c.text(332,403,'Email  /  GitHub  /  LinkedIn',12,MUTED)
# An understated engineering motif, no decorative name box.
for i,(a,b) in enumerate([('01','SENSE'),('02','PLAN'),('03','CONTROL')]):
 y=205+i*65;c.text(1100,y,a,10,CYAN,mono=True);c.text(1140,y-3,b,15,MUTED,mono=True);c.rule(1100,y+35,272)
c.rule(32,470,1376)
section(c,500,'01 / SELECTED & EXPLORATORY WORK','Project portfolio',1376);c.text(1258,532,'13 projects',13,MUTED)
for x,w,t in [(32,55,'All'),(95,103,'Autonomy'),(206,121,'Manipulation'),(335,107,'Embedded'),(450,105,'Vision / AI'),(563,110,'Industrial')]:c.button(x,583,w,t,x==32)
c.button(1155,583,122,'Overview',True);c.button(1285,583,123,'Gallery')
c.text(32,645,'Recommended starting points appear first. Open any project without losing your place.',12,MUTED)
for i,p in enumerate(P):card(c,p,32+(i%4)*348,679+(i//4)*224,332)
section(c,1610,'02 / EXPERIENCE','Engineering in context',1376)
for i,(a,b) in enumerate([('Student engineering','Localization, sensor uncertainty and systematic debugging'),('TU Dortmund research','Embedded platforms and recoverable deployment'),('Industry & training','Electronics, manufacturing and applied machine learning')]):
 y=1680+i*60;c.rule(32,y,1376);c.text(32,y+18,a,15,TEXT,True);c.text(470,y+19,b,14,MUTED);c.text(1378,y+15,'+',20,CYAN)
c.rule(32,1880,1376);c.text(32,1910,'About',23,TEXT,True);c.text(32,1951,'Education, working approach and languages.',14,MUTED)
c.text(850,1910,'Let’s talk robotics.',23,TEXT,True);c.button(850,1950,135,'Get in touch',True);c.text(1010,1963,'Résumé / GitHub / LinkedIn',12,MUTED)
c.text(32,2070,'STRUCTURE APPROVED · VISUAL DIRECTION PROPOSED · EXISTING PROJECT IMAGERY',10,MUTED,mono=True)
c.save('cyber-desktop-concept.webp')

c=Canvas(390,4310)
c.text(20,13,'VISUAL CONCEPT / MOBILE / REVIEW ONLY',9,MUTED,mono=True)
c.text(20,55,'Samarth Patel',18,TEXT,True);c.text(327,59,'Menu',12,MUTED);c.rule(20,96,350)
c.text(20,125,'ROBOTICS SOFTWARE ENGINEER',10,CYAN,mono=True);c.text(20,157,'Samarth Patel',37,TEXT,True)
c.wrap(20,218,'Robotics software. From algorithm to integration.',350,21,TEXT,True,28)
c.wrap(20,292,'ROS2 navigation, robot manipulation and dependable embedded Linux.',350,15)
c.wrap(20,358,'M.Sc. Automation & Robotics · TU Dortmund\nDortmund, Germany',345,12)
c.button(20,415,152,'Explore work ↓',True);c.button(184,415,118,'View résumé');c.text(20,478,'Email  /  GitHub  /  LinkedIn',12,MUTED);c.rule(20,518,350)
c.text(20,545,'01 / WORK',10,CYAN,mono=True);c.text(20,573,'Project portfolio',27,TEXT,True);c.text(20,615,'All 13 projects, in one place.',13,MUTED)
c.button(20,650,108,'Category ▾');c.button(139,650,118,'Overview',True);c.button(268,650,102,'Gallery')
for i,p in enumerate(P):card(c,p,20,712+i*224,350)
c.rule(20,3650,350)
c.text(20,3680,'02 / EXPERIENCE',10,CYAN,mono=True)
c.text(20,3708,'Engineering in context',24,TEXT,True)
for i,(title,desc) in enumerate([('Student engineering','Localization and systematic debugging'),('TU Dortmund research','Embedded platforms and deployment'),('Industry & training','Electronics and applied machine learning')]):
 y=3760+i*90;c.text(20,y,title,16,TEXT,True);c.wrap(20,y+29,desc,350,13);c.rule(20,y+72,350)
c.text(20,4050,'About',22,TEXT,True)
c.wrap(20,4086,'Education, working approach and languages.',350,14)
c.text(20,4150,'Let’s talk robotics.',24,TEXT,True)
c.button(20,4196,135,'Get in touch',True);c.text(175,4210,'Résumé / GitHub',12,MUTED)
c.save('cyber-mobile-concept.webp')
# Detail panel concept, with clear provenance and readable technical narrative.
c=Canvas(1120,990)
c.text(32,18,'VISUAL CONCEPT / PROJECT PREVIEW / REVIEW ONLY',10,MUTED,mono=True)
c.box(24,56,1072,900,BG,LINE,12);c.text(52,83,'← Back to projects',13,CYAN);c.text(1008,83,'Close ×',13,MUTED)
c.text(52,137,'TurtleBot3 Navigation',32,TEXT,True);c.text(52,187,'ACADEMIC PROJECT  /  SIMULATION + HARDWARE',10,ORANGE,mono=True)
c.image(P[0]['image'],52,225,536,302);c.text(52,541,'Illustrative visualization · existing portfolio asset',11,MUTED)
c.text(640,232,'The problem',19,TEXT,True);c.wrap(640,270,'Map an environment, localize the robot and execute waypoint navigation reliably.',404,15)
c.text(640,360,'My contribution',19,TEXT,True);c.wrap(640,398,'ROS2 integration, SLAM and AMCL workflows, Nav2 tuning, and TF/odometry debugging.',404,15)
c.text(52,605,'Engineering evidence',22,TEXT,True)
for i,(a,b) in enumerate([('IMPLEMENTATION','Bring-up → mapping → localization → navigation'),('VALIDATION','Simulation and hardware checks; conditions documented'),('BOUNDARIES','Separate implemented behavior from future work')]):
 y=657+i*62;c.text(52,y,a,10,CYAN,mono=True);c.text(252,y-2,b,14,MUTED);c.rule(52,y+35,992)
c.button(52,864,166,'Full case study →',True);c.button(232,864,130,'Source code ↗');c.text(640,878,'Close returns to your place in the collection.',12,MUTED)
c.save('cyber-preview-concept.webp')
print('Rendered three review-only visual concepts.')

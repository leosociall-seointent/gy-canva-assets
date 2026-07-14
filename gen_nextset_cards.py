#!/usr/bin/env python3
"""
Editable single-card HTML for the July Week-2 "next set" statics (S1-S5).
Text/CSS only -> imports into Canva as native EDITABLE designs (no image garble,
no crop, no collision). data-document-role="page" on the single page div.

    python3 gen_nextset_cards.py   # writes ns_s1..ns_s5.html
"""
LOGO = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/gy-logo.png"

HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box;}
  .page{position:relative;width:1080px;height:1080px;overflow:hidden;padding:60px 64px;
    display:flex;flex-direction:column;background:%(bg)s;
    font-family:'Helvetica Neue',Arial,sans-serif;color:#EEF2FB;}
  .top{display:flex;justify-content:space-between;align-items:center;}
  .logo{height:48px;}
  .pill{border:2px solid %(acc)s;color:%(acc)s;font-weight:800;font-size:20px;
    letter-spacing:2px;padding:11px 26px;border-radius:40px;white-space:nowrap;}
  .h1{font-family:Impact,'Arial Black',sans-serif;color:#fff;letter-spacing:-1px;}
  .sub{color:#B7C0DA;font-weight:600;}
  .foot{display:flex;align-items:center;gap:24px;margin-top:auto;}
  .btn{background:%(acc)s;color:#08122B;font-weight:800;font-size:29px;
    padding:20px 34px;border-radius:14px;white-space:nowrap;}
  .url{color:#EEF2FB;font-size:27px;font-weight:800;}
</style></head><body>"""

def head(bg, acc): return HEAD % {"bg": bg, "acc": acc}
NAVY = "#0E1024"

# ---------- S1: cost of a bad hire ----------
def s1():
    rows = [
        ("Sourcing &amp; screening", "&#8377;1&#8211;2L",
         '<circle cx="20" cy="20" r="12" fill="none" stroke="#47A3FF" stroke-width="3"/><line x1="29" y1="29" x2="38" y2="38" stroke="#47A3FF" stroke-width="3"/>'),
        ("Onboarding &amp; training", "&#8377;1.5&#8211;2.5L",
         '<path d="M8 18 L24 10 L40 18 L24 26 Z" fill="#47A3FF"/><path d="M16 22 v8 a8 4 0 0 0 16 0 v-8" fill="none" stroke="#47A3FF" stroke-width="3"/>'),
        ("Productivity loss", "&#8377;2&#8211;3L",
         '<polyline points="8,12 20,24 28,18 40,32" fill="none" stroke="#47A3FF" stroke-width="3"/><polyline points="40,22 40,32 30,32" fill="none" stroke="#47A3FF" stroke-width="3"/>'),
        ("Exit &amp; re-hire", "&#8377;0.5&#8211;1L",
         '<path d="M26 8 H12 a4 4 0 0 0-4 4 V36 a4 4 0 0 0 4 4 H26" fill="none" stroke="#47A3FF" stroke-width="3"/><polyline points="32,15 41,24 32,33" fill="none" stroke="#47A3FF" stroke-width="3"/><line x1="20" y1="24" x2="41" y2="24" stroke="#47A3FF" stroke-width="3"/>'),
    ]
    r = ""
    for i,(lab,amt,svg) in enumerate(rows):
        border = "" if i==0 else "border-top:1px solid #262a45;"
        r += f'''<div style="display:flex;align-items:center;padding:26px 8px;{border}">
          <div style="width:60px;height:60px;border-radius:50%;border:2px solid #47A3FF;display:flex;align-items:center;justify-content:center;margin-right:26px;">
            <svg width="48" height="48" viewBox="0 0 48 48">{svg}</svg></div>
          <div style="flex:1;font-size:33px;font-weight:800;color:#fff;">{lab}</div>
          <div style="font-size:36px;font-weight:800;color:#47A3FF;font-family:Georgia,serif;">{amt}</div>
        </div>'''
    return head(NAVY,"#47A3FF") + f'''
    <div class="page">
      <div class="top"><img class="logo" src="{LOGO}"><div class="pill">INDUSTRY DATA</div></div>
      <div class="h1" style="font-size:60px;margin-top:40px;line-height:1.02;">THE TRUE COST OF ONE BAD HIRE</div>
      <div class="h1" style="font-size:108px;color:#47A3FF;font-family:Georgia,serif;margin-top:10px;">&#8377;5&#8211;7 LAKH</div>
      <div style="background:#14162E;border-radius:20px;padding:6px 26px;margin-top:34px;">{r}</div>
      <div class="foot"><div class="url" style="margin-left:auto;">groyouth.com</div></div>
    </div></body></html>'''

# ---------- S2: job post -> shortlist in 3 steps ----------
def s2():
    steps = [
        ("1","Post your role","Post your requirements for free in 90 seconds."),
        ("2","AI matches verified talent","Talent Match AI screens &amp; ranks candidates by skills."),
        ("3","Get a ranked shortlist","Receive the top matching candidate shortlist."),
    ]
    s = ""
    for n,t,sub in steps:
        s += f'''<div style="display:flex;align-items:center;background:#14162E;border-radius:18px;padding:30px 34px;margin-bottom:22px;">
          <div style="width:74px;height:74px;border-radius:50%;background:#47A3FF;color:#08122B;font-family:Impact,sans-serif;font-size:44px;display:flex;align-items:center;justify-content:center;margin-right:30px;">{n}</div>
          <div><div style="font-size:37px;font-weight:800;color:#fff;">{t}</div>
          <div style="font-size:25px;font-weight:600;color:#97A1C4;margin-top:6px;">{sub}</div></div>
        </div>'''
    return head(NAVY,"#47A3FF") + f'''
    <div class="page">
      <div class="top"><img class="logo" src="{LOGO}"><div class="pill">FOR EMPLOYERS</div></div>
      <div class="h1" style="font-size:56px;margin-top:44px;">JOB POST &#8594; SHORTLIST IN 3 STEPS</div>
      <div style="margin-top:40px;">{s}</div>
      <div class="foot"><div class="btn">Post a role free &#8594;</div><div class="url">groyouth.com</div></div>
    </div></body></html>'''

# ---------- S3: 5 skills 2026 ----------
def s3():
    skills = [
        ("1","AI literacy","Work with AI tools to build and deliver faster."),
        ("2","Commercial awareness","Understand the business model and how money is made."),
        ("3","Async communication","Write clearly and document well for remote collaboration."),
        ("4","Data translation","Convert raw figures &amp; analytics into business action."),
        ("5","Proactive problem-solving","Present solutions instead of just highlighting problems."),
    ]
    s = ""
    for i,(n,t,sub) in enumerate(skills):
        border = "" if i==0 else "border-top:1px solid #223022;"
        s += f'''<div style="display:flex;align-items:center;padding:22px 6px;{border}">
          <div style="width:56px;height:56px;border-radius:50%;border:2px solid #52D695;color:#52D695;font-family:Impact,sans-serif;font-size:30px;display:flex;align-items:center;justify-content:center;margin-right:26px;flex:0 0 auto;">{n}</div>
          <div><div style="font-size:33px;font-weight:800;color:#fff;">{t}</div>
          <div style="font-size:24px;font-weight:600;color:#97A1C4;margin-top:3px;">{sub}</div></div>
        </div>'''
    return head(NAVY,"#52D695") + f'''
    <div class="page">
      <div class="top"><img class="logo" src="{LOGO}"><div class="pill">CAREER SKILLS</div></div>
      <div class="h1" style="font-size:52px;margin-top:40px;">5 SKILLS THAT GET YOU HIRED IN 2026</div>
      <div class="sub" style="color:#52D695;font-style:italic;font-size:32px;margin-top:8px;">that no degree teaches</div>
      <div style="background:#12181A;border-radius:20px;padding:6px 26px;margin-top:26px;">{s}</div>
      <div class="foot"><div class="url" style="margin-left:auto;">groyouth.com</div></div>
    </div></body></html>'''

# ---------- S4: why the ATS is free (founder quote) ----------
def s4():
    return head("linear-gradient(135deg,#5B3FA6 0%,#2A2350 45%,#0E1024 100%)","#B98CFF") + f'''
    <div class="page">
      <div class="top"><img class="logo" src="{LOGO}"><div class="pill">FOUNDER&#8217;S DESK</div></div>
      <div style="font-family:Georgia,serif;font-size:150px;line-height:0.6;color:#B98CFF;margin-top:40px;">&#8220;</div>
      <div style="font-family:Georgia,serif;font-size:62px;line-height:1.28;color:#fff;font-weight:700;margin-top:10px;width:900px;">
        We made our ATS <span style="color:#B98CFF;">free on purpose.</span> A marketplace only works when <span style="color:#B98CFF;">both sides show up.</span></div>
      <div style="font-size:30px;font-weight:700;color:#C9CFE6;margin-top:40px;">&#8212; Founder&#8217;s Desk, GroYouth</div>
      <div class="foot"><div class="btn">Claim your free ATS &#8594;</div><div class="url">groyouth.com</div></div>
    </div></body></html>'''

# ---------- S5: more than a resume (GY Assist) ----------
def s5():
    chips = ["React.js","Node.js","AWS","Python","System Design","Problem Solving"]
    chip_html = ""
    for c in chips:
        chip_html += f'''<span style="display:inline-flex;align-items:center;gap:8px;border:1.5px solid #52D695;color:#0E1024;background:#EAF9F1;font-size:22px;font-weight:700;padding:9px 15px;border-radius:20px;margin:0 8px 10px 0;">{c} <span style="color:#2BB673;">&#10003;</span></span>'''
    # score ring (SVG, 88%)
    import math
    r=78; circ=2*math.pi*r; fill=circ*0.88
    ring=f'''<svg width="200" height="200" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="{r}" fill="none" stroke="#E4EAF2" stroke-width="18"/>
      <circle cx="100" cy="100" r="{r}" fill="none" stroke="#52D695" stroke-width="18" stroke-linecap="round"
        stroke-dasharray="{fill:.0f} {circ:.0f}" transform="rotate(-90 100 100)"/>
      <text x="100" y="116" text-anchor="middle" font-family="Helvetica,Arial" font-size="52" font-weight="800" fill="#0E1024">88%</text></svg>'''
    return head("radial-gradient(1200px 700px at 78% 40%, #1c2b3a 0%, #0E1024 60%)","#B98CFF") + f'''
    <div class="page">
      <div class="top"><img class="logo" src="{LOGO}"><div class="pill">GY ASSIST</div></div>
      <div style="display:flex;flex:1;align-items:center;gap:36px;margin-top:20px;">
        <div style="flex:0 0 430px;">
          <div class="h1" style="font-size:76px;line-height:1.02;">MORE THAN A R&#201;SUM&#201;</div>
          <div class="sub" style="font-size:29px;margin-top:22px;width:400px;">GY Assist builds your verified, job-ready profile.</div>
        </div>
        <div style="flex:1;background:#fff;border-radius:28px;padding:34px 32px;color:#0E1024;box-shadow:0 30px 80px rgba(0,0,0,0.35);">
          <div style="display:flex;align-items:center;gap:18px;">
            <div style="width:76px;height:76px;border-radius:50%;background:linear-gradient(135deg,#B98CFF,#52D695);color:#fff;font-size:30px;font-weight:800;display:flex;align-items:center;justify-content:center;">AS</div>
            <div><div style="font-size:30px;font-weight:800;">Ananya Sharma</div>
            <div style="font-size:22px;color:#5B6478;">Software Engineer</div></div>
          </div>
          <div style="text-align:center;margin:18px 0;"><div style="font-size:20px;font-weight:700;color:#5B6478;text-align:left;">Score</div>{ring}</div>
          <div style="font-size:20px;font-weight:800;color:#0E1024;margin-bottom:12px;">Verified Skills</div>
          <div>{chip_html}</div>
        </div>
      </div>
      <div class="foot"><div class="btn">Build your profile free &#8594;</div><div class="url">groyouth.com</div></div>
    </div></body></html>'''

CARDS = {"ns_s1_bad_hire.html":s1(),"ns_s2_shortlist.html":s2(),"ns_s3_skills.html":s3(),
         "ns_s4_free_ats.html":s4(),"ns_s5_gyassist.html":s5()}
for fn,html in CARDS.items():
    open(fn,"w").write(html)
    print("wrote",fn,len(html),"bytes")

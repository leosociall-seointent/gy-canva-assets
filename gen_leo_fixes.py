#!/usr/bin/env python3
"""
Leo's round-2 fixes as EDITABLE Canva-import HTML (separate movable logo/text
layers, no baked text). Emits 6 designs:
  partner_v2   — reworded "Our partners take 70% / GroYouth keeps 30%", dominant 70%
  venn         — matching-problem Venn with "THE MATCH" in WHITE (was green/purple)
  poll_speed   — graphical Day-3 poll (stopwatch motif) + options + comment CTA
  poll_2026    — graphical Day-7 poll (target motif) + options + comment CTA
  resume_wrap  — resume make-over image (watermark cleaned) + editable GroYouth logo
  gyassist_wrap— GY Assist founder portrait + editable GroYouth logo
Also preps two hosted images (resume_clean.png, gyassist.png).
"""
import os, html, shutil
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
GY   = "/Users/leo/Claude AI/socialorange/clients/groyouth"
LOGO = BASE + "gy-logo.png"
GREEN, BLUE, VIOLET = "#52D695", "#47A3FF", "#B98CFF"
INKBTN = "#08122B"

def esc(s): return html.escape(str(s), quote=False)

# ---------------------------------------------------------------- image prep
def prep_images():
    # clean the "RESUME MASTERCLASS" watermarks off the resume make-over image
    src = os.path.join(GY, "social_samples/11_resume_mistakes.png")
    im = Image.open(src).convert("RGB"); d = ImageDraw.Draw(im)
    d.rectangle([812,192,1016,238], fill=(6,25,57))     # top-right wordmark
    d.rectangle([6,370,46,724],   fill=(6,23,50))       # left vertical wordmark
    im.save(os.path.join(HERE, "resume_clean.png"))
    # stage the founder portrait for hosting
    shutil.copy(os.path.join(GY,"social_samples/13_gy_assist_founder.png"),
                os.path.join(HERE,"gyassist.png"))
    print("prepped: resume_clean.png, gyassist.png")

# ---------------------------------------------------------------- shared CSS
CSS = """
 *{margin:0;padding:0;box-sizing:border-box}
 .page{position:relative;width:1080px;height:1080px;overflow:hidden;background:#0E1024;
   font-family:'Helvetica Neue',Arial,sans-serif}
 .bg{position:absolute;top:0;left:0;width:1080px;height:1080px;object-fit:cover}
 .grad{position:absolute;inset:0;width:1080px;height:1080px;
   background:radial-gradient(66% 52% at 78% 14%,var(--glow),rgba(9,12,26,0) 60%),
   linear-gradient(180deg,#16193a 0%,#0E1024 62%)}
 .logo{position:absolute;top:56px;left:60px;height:52px}
 .logoback{position:absolute;top:44px;left:44px;width:250px;height:78px;border-radius:16px;
   background:rgba(9,12,26,0.55)}
 .pill{position:absolute;top:62px;right:60px;background:rgba(9,12,26,0.5);border:2px solid var(--accent);
   color:var(--accent);font-weight:700;font-size:22px;letter-spacing:2px;padding:12px 28px;border-radius:40px}
 .accent{position:absolute;left:64px;width:92px;height:10px;background:var(--accent);border-radius:6px}
 .headline{position:absolute;left:60px;width:952px;color:#fff;font-family:Impact,'Arial Black',sans-serif;
   line-height:0.99;letter-spacing:-1px}
 .sub{position:absolute;left:64px;width:900px;color:#EEF2FB;font-size:30px;font-weight:600;line-height:1.3}
 .btn{position:absolute;left:64px;display:flex;align-items:center}
 .btnbox{background:var(--accent);color:#08122B;font-weight:800;font-size:32px;padding:22px 38px;border-radius:14px}
 .url{color:#EEF2FB;font-size:30px;font-weight:700;margin-left:26px}
"""

def frame(accent, glow, inner, label, bg=None):
    base = (f'<img class="bg" src="{bg}"><div class="grad" style="--glow:{glow};background:'
            'linear-gradient(90deg,rgba(9,12,26,.55),rgba(9,12,26,.08) 60%,rgba(9,12,26,0))"></div>'
            if bg else f'<div class="grad" style="--glow:{glow}"></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="page" style="--accent:{accent}" data-document-role="page" data-label="{esc(label)}">'
            f'{base}{inner}</div></body></html>')

GLOW = {GREEN:"rgba(82,214,149,0.20)", BLUE:"rgba(71,163,255,0.20)", VIOLET:"rgba(185,140,255,0.20)"}
def logo_el(): return f'<img class="logo" src="{LOGO}" alt="GroYouth">'
def pill_el(t): return f'<div class="pill">{esc(t)}</div>'

# ---------------------------------------------------------------- PARTNER v2
def partner():
    inner = f"""{logo_el()}{pill_el('PARTNER ECONOMICS')}
 <div class="headline" style="top:196px;font-size:78px">Keep 70%. We run the tech.</div>
 <div class="sub" style="top:300px;color:#97A1C4">A transparent 70:30 split — you keep the bigger share.</div>
 <div style="position:absolute;left:64px;top:372px;width:640px;height:252px;background:{GREEN};border-radius:22px"></div>
 <div style="position:absolute;left:64px;top:372px;width:640px;text-align:center;color:{INKBTN};font-weight:800;font-size:34px;padding-top:44px;letter-spacing:1px">OUR PARTNERS TAKE</div>
 <div style="position:absolute;left:64px;top:372px;width:640px;text-align:center;color:{INKBTN};font-family:Impact,sans-serif;font-size:168px;padding-top:70px">70%</div>
 <div style="position:absolute;left:716px;top:372px;width:300px;height:252px;background:{BLUE};border-radius:22px"></div>
 <div style="position:absolute;left:716px;top:372px;width:300px;text-align:center;color:{INKBTN};font-weight:800;font-size:24px;padding-top:46px">GROYOUTH KEEPS</div>
 <div style="position:absolute;left:716px;top:372px;width:300px;text-align:center;color:{INKBTN};font-family:Impact,sans-serif;font-size:104px;padding-top:96px">30%</div>
 {_cards()}
 <div style="position:absolute;left:64px;top:986px;width:952px;text-align:center;color:#97A1C4;font-size:23px;font-weight:600">You focus on delivery. We bring the tech, mandates &amp; scale.</div>"""
    return frame(BLUE, GLOW[BLUE], inner, "For Agencies · Our Partners Take 70%")

def _cards():
    cards=[("Free enterprise ATS","Run your whole desk on our platform — free.",GREEN),
           ("AI candidate matching","Verified talent matched to your mandates.",BLUE),
           ("Verified job mandates","Real, ready-to-fill roles — not cold leads.",GREEN),
           ("You own the relationship","We power the tech; you keep the client.",BLUE)]
    out=""
    for i,(t,desc,acc) in enumerate(cards):
        x=64 if i%2==0 else 552; y=664+(i//2)*140
        out+=(f'<div style="position:absolute;left:{x}px;top:{y}px;width:464px;height:118px;'
              f'background:#14162E;border:2px solid #20233A;border-radius:14px"></div>'
              f'<div style="position:absolute;left:{x+26}px;top:{y+22}px;width:420px;color:{acc};font-weight:800;font-size:25px">{esc(t)}</div>'
              f'<div style="position:absolute;left:{x+26}px;top:{y+60}px;width:420px;color:#EEF2FB;font-size:21px;font-weight:600">{esc(desc)}</div>')
    return out

# ---------------------------------------------------------------- VENN (white THE MATCH)
def venn():
    svg = f"""<svg width="1080" height="620" style="position:absolute;left:0;top:430px">
   <defs><clipPath id="L"><circle cx="418" cy="310" r="238"/></clipPath></defs>
   <circle cx="418" cy="310" r="238" fill="rgba(185,140,255,0.26)" stroke="{VIOLET}" stroke-width="4"/>
   <circle cx="662" cy="310" r="238" fill="rgba(71,163,255,0.26)" stroke="{BLUE}" stroke-width="4"/>
   <circle cx="662" cy="310" r="238" fill="{GREEN}" fill-opacity="0.92" clip-path="url(#L)"/>
 </svg>"""
    inner = f"""{logo_el()}{pill_el("FOUNDER'S DESK")}
 <div class="accent" style="top:170px"></div>
 <div class="headline" style="top:200px;font-size:82px">India doesn't have a hiring problem. It has a matching problem.</div>
 {svg}
 <div style="position:absolute;left:250px;top:706px;width:220px;text-align:center;color:#fff;font-weight:800;font-size:34px">TALENT<div style="color:#EEF2FB;font-size:22px;font-weight:600;margin-top:6px">millions, job-ready</div></div>
 <div style="position:absolute;left:612px;top:706px;width:240px;text-align:center;color:#fff;font-weight:800;font-size:34px">COMPANIES<div style="color:#EEF2FB;font-size:22px;font-weight:600;margin-top:6px">thousands, hiring</div></div>
 <div style="position:absolute;left:474px;top:706px;width:132px;text-align:center;color:#FFFFFF;font-weight:800;font-size:30px;line-height:1.05">THE<br>MATCH</div>
 <div class="btn" style="bottom:60px"><div class="btnbox">Read the founder's take →</div><div class="url">groyouth.com</div></div>"""
    return frame(VIOLET, GLOW[VIOLET], inner, "Founder's Desk · The Match (white)")

# ---------------------------------------------------------------- POLLS (graphical)
def _stopwatch(cx,cy,accent):
    return f"""<svg width="200" height="200" style="position:absolute;left:{cx}px;top:{cy}px">
      <rect x="86" y="8" width="28" height="20" rx="5" fill="{accent}"/>
      <line x1="100" y1="30" x2="100" y2="46" stroke="{accent}" stroke-width="8"/>
      <circle cx="100" cy="118" r="72" fill="none" stroke="{accent}" stroke-width="9"/>
      <line x1="100" y1="118" x2="100" y2="66" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
      <line x1="100" y1="118" x2="140" y2="132" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
      <circle cx="100" cy="118" r="7" fill="#fff"/></svg>"""
def _target(cx,cy,accent):
    return f"""<svg width="200" height="200" style="position:absolute;left:{cx}px;top:{cy}px">
      <circle cx="100" cy="105" r="76" fill="none" stroke="{accent}" stroke-width="9"/>
      <circle cx="100" cy="105" r="48" fill="none" stroke="#fff" stroke-width="7"/>
      <circle cx="100" cy="105" r="20" fill="{accent}"/>
      <line x1="100" y1="105" x2="176" y2="40" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
      <path d="M176 40 l6 22 l-22 -6 z" fill="#fff"/></svg>"""
def poll(kicker,question,options,footer,accent,icon,label):
    opts=""
    for i,o in enumerate(options):
        y=548+i*112
        opts+=(f'<div style="position:absolute;left:64px;top:{y}px;width:952px;height:92px;background:#14162E;'
               f'border:2px solid #20233A;border-radius:16px"></div>'
               f'<div style="position:absolute;left:96px;top:{y+24}px;width:44px;height:44px;border-radius:12px;'
               f'background:{accent};color:{INKBTN};font-weight:800;font-size:24px;text-align:center;line-height:44px">{chr(65+i)}</div>'
               f'<div style="position:absolute;left:166px;top:{y+26}px;width:820px;color:#fff;font-size:30px;font-weight:700">{esc(o)}</div>')
    inner=f"""{logo_el()}{pill_el(kicker)}{icon}
 <div class="accent" style="top:250px"></div>
 <div class="headline" style="top:280px;left:288px;width:728px;font-size:66px">{esc(question)}</div>
 {opts}
 <div style="position:absolute;left:64px;top:1004px;width:952px;text-align:center;color:{accent};font-weight:800;font-size:27px">{esc(footer)}</div>"""
    return frame(accent, GLOW[accent], inner, label)

# ---------------------------------------------------------------- PHOTO + LOGO wrappers
def photo_wrap(img_url, label, pill=None, accent=VIOLET):
    p = pill_el(pill) if pill else ""
    inner=(f'<img class="bg" src="{img_url}">'
           f'<div class="logoback"></div>{logo_el()}{p}')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="page" style="--accent:{accent}" data-document-role="page" data-label="{esc(label)}">'
            f'{inner}</div></body></html>')

# ---------------------------------------------------------------- build
def build():
    prep_images()
    files={
      "partner_v2.html": partner(),
      "venn.html": venn(),
      "poll_speed_v2.html": poll("INDUSTRY POLL","What kills your hiring speed the most?",
          ["CV overload & manual screening","Candidate ghosting & no-shows",
           "Skills mismatch at final interview","Salary alignment & budget gaps"],
          "Vote below — tell us your #1 in the comments.",VIOLET,_stopwatch(70,232,VIOLET),"Poll · Hiring speed (graphical)"),
      "poll_2026_v2.html": poll("TALENT POLL","Job seekers: what matters most in 2026?",
          ["Base salary / compensation","Flexibility / WFH options",
           "Continuous learning & growth","Bias-free / skills-first hiring"],
          "Cast your vote — then tell us why below.",GREEN,_target(70,244,GREEN),"Poll · What matters 2026 (graphical)"),
      "resume_wrap.html": photo_wrap(BASE+"resume_clean.png","Resume Make-Over + logo",accent=GREEN),
      "gyassist_wrap.html": photo_wrap(BASE+"gyassist.png","GY Assist · Founder + logo","FOUNDER'S DESK",VIOLET),
    }
    for fn,doc in files.items():
        open(os.path.join(HERE,fn),"w").write(doc)
    print("generated:", ", ".join(files))

if __name__=="__main__":
    build()

#!/usr/bin/env python3
"""
GroYouth — Canva import HTML generator.
Emits one 1080x1080 HTML page per social post (data-document-role="page"),
matching the approved Direction-A Branded System. Direction-B posts are
full-bleed wrappers around the already-finished photoreal images.

Import each emitted .html into Canva via import-design-from-url -> native
editable design. Backgrounds/images are served from this same GitHub repo.
"""
import os, html

BASE = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
HERE = os.path.dirname(os.path.abspath(__file__))

GREEN, BLUE, VIOLET = "#52D695", "#47A3FF", "#B98CFF"
BTN_TEXT = "#08122B"           # dark navy — reads on all three accents
LOGO = BASE + "gy-logo.png"

CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  .page { position:relative; width:1080px; height:1080px; overflow:hidden;
          background:#0E1024; font-family:'Helvetica Neue', Arial, sans-serif; }
  .bg { position:absolute; top:0; left:0; width:1080px; height:1080px; object-fit:cover; }
  .scrim { position:absolute; top:0; left:0; width:1080px; height:1080px;
    background:
      linear-gradient(90deg, rgba(9,12,26,0.93) 0%, rgba(9,12,26,0.66) 46%, rgba(9,12,26,0.12) 74%, rgba(9,12,26,0) 100%),
      linear-gradient(0deg, rgba(9,12,26,0.90) 2%, rgba(9,12,26,0) 48%); }
  .logo { position:absolute; top:56px; left:60px; height:54px; }
  .pill { position:absolute; top:62px; right:60px; border:2px solid var(--accent); color:var(--accent);
    font-weight:700; font-size:22px; letter-spacing:2px; padding:12px 28px; border-radius:40px; }
  .accent { position:absolute; left:64px; width:92px; height:10px; background:var(--accent); border-radius:6px; }
  .headline { position:absolute; left:60px; width:930px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; line-height:0.97; letter-spacing:-1px; }
  .subhead { position:absolute; left:64px; width:910px; color:#EEF2FB; font-size:30px; font-weight:600; line-height:1.28; }
  .rows { position:absolute; left:64px; width:900px; }
  .row { display:flex; align-items:center; margin-bottom:16px; }
  .mark { min-width:44px; width:44px; height:44px; border:2px solid var(--accent); color:var(--accent);
    border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:22px; margin-right:22px; }
  .row .label { color:#FFFFFF; font-size:28px; font-weight:600; }
  .cta { position:absolute; left:64px; bottom:70px; display:flex; align-items:center; }
  .btn { background:var(--accent); color:%(btn_text)s; font-weight:800; font-size:32px; padding:24px 40px; border-radius:14px; }
  .url { color:#EEF2FB; font-size:30px; font-weight:700; margin-left:28px; }
  .statflow { position:absolute; left:60px; display:flex; align-items:center; }
  .bignum { font-family:Impact,'Arial Black',sans-serif; color:#FFFFFF; font-size:150px; line-height:1; }
  .arrow { color:var(--accent); font-size:90px; font-weight:800; margin:0 34px; }
  .bigto { font-family:Impact,'Arial Black',sans-serif; color:var(--accent); font-size:150px; line-height:1; }
  .attrib { position:absolute; left:64px; color:var(--accent); font-size:26px; font-weight:700; letter-spacing:1px; }
""" % {"btn_text": BTN_TEXT}

def esc(s): return html.escape(s, quote=False)

def frame(accent, label, bg, inner):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
  <div class="page" style="--accent:{accent}" data-document-role="page" data-label="{esc(label)}">
    <img class="bg" src="{bg}" alt="{esc(label)}">
    <div class="scrim"></div>
    <img class="logo" src="{LOGO}" alt="GroYouth logo">
    <div class="pill">{esc(label.split('·')[0].strip().upper()) if '·' in label else 'GROYOUTH'}</div>
    {inner}
  </div>
</body></html>"""

def cta(btn, url="groyouth.com"):
    return f'<div class="cta"><div class="btn">{esc(btn)}</div><div class="url">{esc(url)}</div></div>'

def flow(headline, subhead, steps, btn, hsize=104, marker="num"):
    rows = ""
    for i, s in enumerate(steps, 1):
        m = str(i) if marker == "num" else "&#10003;"
        rows += f'<div class="row"><div class="mark">{m}</div><div class="label">{esc(s)}</div></div>'
    return (f'<div class="accent" style="top:402px"></div>'
            f'<div class="headline" style="top:428px;font-size:{hsize}px">{esc(headline)}</div>'
            f'<div class="subhead" style="top:672px">{esc(subhead)}</div>'
            f'<div class="rows" style="top:766px">{rows}</div>'
            + cta(btn))

def statflow(headline, num_from, num_to, caption, btn, hsize=92):
    return (f'<div class="accent" style="top:392px"></div>'
            f'<div class="headline" style="top:418px;font-size:{hsize}px">{esc(headline)}</div>'
            f'<div class="statflow" style="top:600px"><div class="bignum">{esc(num_from)}</div>'
            f'<div class="arrow">&rarr;</div><div class="bigto">{esc(num_to)}</div></div>'
            f'<div class="subhead" style="top:800px">{esc(caption)}</div>'
            + cta(btn))

def typographic(headline, attrib, btn, hsize=100):
    return (f'<div class="accent" style="top:392px"></div>'
            f'<div class="headline" style="top:418px;font-size:{hsize}px">{esc(headline)}</div>'
            f'<div class="attrib" style="top:absolute;top:760px">{esc(attrib)}</div>'
            + cta(btn))

# ------------------------------------------------------------------ POSTS
POSTS_A = [
  dict(key="founder", accent=VIOLET, bg=BASE+"bg_founder.png",
       label="Founder's Desk · The Matching Problem",
       inner=typographic(
         "India doesn't have a hiring problem. It has a matching problem.",
         "— FOUNDER'S DESK, GROYOUTH", "See how it works", hsize=88)),
  dict(key="employer", accent=BLUE, bg=BASE+"bg_employer.png",
       label="For Hiring Teams · Talent Match AI",
       inner=statflow("Still screening 300 CVs by hand?",
         "300", "10", "Talent Match AI ranks candidates by real fit — shortlist in minutes.",
         "Book a 15-min demo")),
  dict(key="partner", accent=BLUE, bg=BASE+"bg_partner.png",
       label="For Agencies · The 70:30 Model",
       inner=flow("Keep 70%. We run the tech.",
         "The 70:30 model: you own the relationship, we power the matching.",
         ["You keep the client relationship", "We power sourcing + AI matching",
          "You keep 70% of the fee"], "Partner with us", hsize=100, marker="check")),
  dict(key="campus", accent=GREEN, bg=BASE+"bg_campus.png",
       label="For Universities · GY Campus",
       inner=flow("Turn students into verified, job-ready talent.",
         "GY Campus makes your placement cell measurably stronger.",
         ["Skill-verify every student with GY SAT", "Employers find them directly",
          "Placement reports that impress"], "Partner your campus", hsize=84, marker="check")),
]

# Direction B — finished photoreal, full-bleed wrappers
POSTS_B = [
  ("get_found",   "Get Found · Job Seekers"),
  ("bad_hire",    "Cost of a Bad Hire · Hiring Orgs"),
  ("marketplace", "One Marketplace · Both Sides Win"),
  ("brand",       "Brand POV · Not an Agency"),
  ("campus",      "Campus · Universities"),
]

def build():
    made = []
    for p in POSTS_A:
        out = os.path.join(HERE, f"a_{p['key']}.html")
        with open(out, "w") as f:
            f.write(frame(p["accent"], p["label"], p["bg"], p["inner"]))
        made.append(os.path.basename(out))
    for key, label in POSTS_B:
        inner = ""  # full-bleed: the finished image IS the post, no overlays
        html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0}} .page{{position:relative;width:1080px;height:1080px;overflow:hidden}}
 .bg{{position:absolute;top:0;left:0;width:1080px;height:1080px;object-fit:cover}}
</style></head><body>
 <div class="page" data-document-role="page" data-label="{esc(label)}">
   <img class="bg" src="{BASE}b_{key}.png" alt="{esc(label)}">
 </div></body></html>"""
        out = os.path.join(HERE, f"b_{key}.html")
        with open(out, "w") as f:
            f.write(html_doc)
        made.append(os.path.basename(out))
    print("generated:", ", ".join(made))

if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""
Build the 5 Direction-B posts as EDITABLE Canva templates:
a single pre-darkened photoreal background (bdark_<key>.png) + separate movable
layers for logo / audience pill / headline / subhead / CTA. No baked-in text,
no separate scrim layer -> clean editable structure on import.

    python3 gen_b_editable.py
"""
import os, html

BASE = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = BASE + "gy-logo.png"
GREEN, BLUE, VIOLET = "#52D695", "#47A3FF", "#B98CFF"

CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  .page { position:relative; width:1080px; height:1080px; overflow:hidden;
          background:#0E1024; font-family:'Helvetica Neue', Arial, sans-serif; }
  .bg { position:absolute; top:0; left:0; width:1080px; height:1080px; object-fit:cover; }
  .logo { position:absolute; top:56px; left:60px; height:54px; }
  .pill { position:absolute; top:62px; left:60px; border:2px solid ACCENT; color:ACCENT;
    font-weight:700; font-size:22px; letter-spacing:2px; padding:12px 28px; border-radius:40px; }
  .accent { position:absolute; top:556px; left:64px; width:92px; height:10px; background:ACCENT; border-radius:6px; }
  .headline { position:absolute; top:584px; left:60px; width:840px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:HSIZEpx; line-height:0.98; letter-spacing:-1px; }
  .subhead { position:absolute; top:SUBTOPpx; left:64px; width:780px; color:#EEF2FB;
    font-size:29px; font-weight:600; line-height:1.3; }
  .cta { position:absolute; left:64px; bottom:68px; display:flex; align-items:center; }
  .btn { background:ACCENT; color:#08122B; font-weight:800; font-size:31px; padding:23px 38px; border-radius:14px; }
  .url { color:#EEF2FB; font-size:29px; font-weight:700; margin-left:26px; }
"""

def esc(s): return html.escape(s, quote=True)

def page(key, accent, pill, headline, subhead, cta, hsize=82, subtop=812):
    css = (CSS.replace("ACCENT", accent).replace("HSIZE", str(hsize)).replace("SUBTOP", str(subtop)))
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{css}</style></head>
<body>
  <div class="page" data-document-role="page" data-label="{esc(pill.title())} (Editable Photoreal)">
    <img class="bg" src="{BASE}bdark_{key}.png" alt="{esc(pill)}">
    <img class="logo" src="{LOGO}" alt="GroYouth logo">
    <div class="pill">{esc(pill)}</div>
    <div class="accent"></div>
    <div class="headline">{esc(headline)}</div>
    <div class="subhead">{esc(subhead)}</div>
    <div class="cta"><div class="btn">{esc(cta)}</div><div class="url">groyouth.com</div></div>
  </div>
</body></html>"""

POSTS = [
  dict(key="get_found", accent=GREEN, pill="FOR JOB SEEKERS",
       headline="Stop applying. Start getting found.",
       subhead="Take the free GY SAT once, get a verified skill score, and let companies come to you.",
       cta="Get found free →", hsize=80, subtop=812),
  dict(key="bad_hire", accent=BLUE, pill="FOR HIRING TEAMS",
       headline="One wrong hire costs ₹5–7 lakh.",
       subhead="Talent Match AI ranks candidates by real fit — so the first hire is the right one.",
       cta="See Talent Match AI →", hsize=80, subtop=812),
  dict(key="marketplace", accent=VIOLET, pill="HOW IT WORKS",
       headline="One marketplace. Both sides win.",
       subhead="Talent proves skills on one side, companies post real needs on the other. AI makes the match.",
       cta="See how it works →", hsize=80, subtop=812),
  dict(key="brand", accent=BLUE, pill="WHY GROYOUTH",
       headline="We're not a recruitment agency.",
       subhead="Agencies work one side. We're the marketplace that serves talent and companies at once.",
       cta="See how it works →", hsize=82, subtop=812),
  dict(key="campus", accent=GREEN, pill="FOR UNIVERSITIES",
       headline="Turn students into job-ready talent.",
       subhead="Verified skill scores, direct employer visibility, and placement reports that impress.",
       cta="Partner your campus →", hsize=78, subtop=812),
]

def build():
    made = []
    for p in POSTS:
        out = os.path.join(HERE, f"be_{p['key']}.html")
        with open(out, "w") as f:
            f.write(page(p["key"], p["accent"], p["pill"], p["headline"], p["subhead"], p["cta"], p["hsize"], p["subtop"]))
        made.append(os.path.basename(out))
    print("generated:", ", ".join(made))

if __name__ == "__main__":
    build()

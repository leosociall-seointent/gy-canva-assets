#!/usr/bin/env python3
"""
GroYouth — Set 1 (Jul 10–19) single-post generator.
Emits editable 1080x1080 HTML pages (data-document-role="page") for the
8 single-image posts in calendar Days 1-10: polls, founder/news/community
typographic cards, a data big-stat, and a partner 3-step flow.

Same Branded-System anatomy as build_canva_html.py (separate movable logo /
pill / headline / body layers, no baked-in text). Polls + big-stat use a clean
gradient canvas (bg=None) so all four options stay legible; the rest sit on the
existing branded backgrounds already in this repo.

    python3 gen_set1.py
"""
import os, html

BASE = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
HERE = os.path.dirname(os.path.abspath(__file__))

GREEN, BLUE, VIOLET = "#52D695", "#47A3FF", "#B98CFF"
GLOW = {GREEN: "rgba(82,214,149,0.20)", BLUE: "rgba(71,163,255,0.20)", VIOLET: "rgba(185,140,255,0.20)"}
LOGO = BASE + "gy-logo.png"

CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  .page { position:relative; width:1080px; height:1080px; overflow:hidden;
          background:#0E1024; font-family:'Helvetica Neue', Arial, sans-serif; }
  .bg { position:absolute; top:0; left:0; width:1080px; height:1080px; object-fit:cover; }
  .gradbg { position:absolute; top:0; left:0; width:1080px; height:1080px;
    background: radial-gradient(68% 54% at 76% 15%, var(--glow), rgba(9,12,26,0) 60%),
                linear-gradient(180deg, #16193a 0%, #0E1024 62%); }
  .scrim { position:absolute; top:0; left:0; width:1080px; height:1080px;
    background:
      linear-gradient(90deg, rgba(9,12,26,0.93) 0%, rgba(9,12,26,0.66) 46%, rgba(9,12,26,0.12) 74%, rgba(9,12,26,0) 100%),
      linear-gradient(0deg, rgba(9,12,26,0.90) 2%, rgba(9,12,26,0) 48%); }
  .logo { position:absolute; top:56px; left:60px; height:54px; }
  .pill { position:absolute; top:62px; right:60px; background:rgba(9,12,26,0.45);
    border:2px solid var(--accent); color:var(--accent);
    font-weight:700; font-size:22px; letter-spacing:2px; padding:12px 28px; border-radius:40px; }
  .accent { position:absolute; left:64px; width:92px; height:10px; background:var(--accent); border-radius:6px; }
  .headline { position:absolute; left:60px; width:940px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; line-height:0.99; letter-spacing:-1px; }
  .subhead { position:absolute; left:64px; width:900px; color:#EEF2FB; font-size:31px; font-weight:600; line-height:1.3; }
  .attrib { position:absolute; left:64px; width:900px; color:var(--accent); font-size:27px; font-weight:700; letter-spacing:1px; line-height:1.3; }
  /* flow rows */
  .rows { position:absolute; left:64px; width:920px; }
  .row { display:flex; align-items:center; margin-bottom:18px; }
  .mark { min-width:46px; width:46px; height:46px; border:2px solid var(--accent); color:var(--accent);
    border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:24px; margin-right:22px; }
  .row .label { color:#FFFFFF; font-size:29px; font-weight:600; }
  /* poll options */
  .polls { position:absolute; left:64px; width:952px; }
  .opt { display:flex; align-items:center; background:rgba(255,255,255,0.06);
    border:2px solid rgba(255,255,255,0.16); border-radius:18px; padding:22px 26px; margin-bottom:20px; }
  .optkey { min-width:56px; width:56px; height:56px; border-radius:14px; background:var(--accent); color:#08122B;
    font-weight:800; font-size:27px; display:flex; align-items:center; justify-content:center; margin-right:24px; }
  .optlabel { color:#FFFFFF; font-size:31px; font-weight:700; }
  /* big stat */
  .bignum { position:absolute; left:58px; color:#FFFFFF; font-family:Impact,'Arial Black',sans-serif;
    font-size:280px; line-height:0.86; letter-spacing:-3px; }
  .biglabel { position:absolute; left:64px; width:930px; color:#FFFFFF; font-size:46px; font-weight:800; line-height:1.08; }
  /* cta */
  .cta { position:absolute; left:64px; bottom:70px; display:flex; align-items:center; }
  .btn { background:var(--accent); color:#08122B; font-weight:800; font-size:32px; padding:24px 40px; border-radius:14px; }
  .url { color:#EEF2FB; font-size:30px; font-weight:700; margin-left:28px; }
  .foot { position:absolute; left:64px; bottom:78px; color:#EEF2FB; font-size:30px; font-weight:700; }
  .footaccent { color:var(--accent); }
"""

def esc(s): return html.escape(str(s), quote=False)

def frame(accent, label, inner, bg=None):
    if bg:
        base = f'<img class="bg" src="{bg}" alt="{esc(label)}"><div class="scrim"></div>'
    else:
        base = f'<div class="gradbg" style="--glow:{GLOW[accent]}"></div>'
    pill = label.split('·')[0].strip().upper() if '·' in label else 'GROYOUTH'
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
  <div class="page" style="--accent:{accent}" data-document-role="page" data-label="{esc(label)}">
    {base}
    <img class="logo" src="{LOGO}" alt="GroYouth logo">
    <div class="pill">{esc(pill)}</div>
    {inner}
  </div>
</body></html>"""

def cta(btn, url="groyouth.com"):
    return f'<div class="cta"><div class="btn">{esc(btn)}</div><div class="url">{esc(url)}</div></div>'

def foot(text, accent_tail=""):
    tail = f' <span class="footaccent">{esc(accent_tail)}</span>' if accent_tail else ""
    return f'<div class="foot">{esc(text)}{tail}</div>'

def typographic(headline, attrib, btn, hsize=90, htop=430):
    return (f'<div class="accent" style="top:{htop-26}px"></div>'
            f'<div class="headline" style="top:{htop}px;font-size:{hsize}px">{esc(headline)}</div>'
            f'<div class="attrib" style="top:770px">{esc(attrib)}</div>'
            + cta(btn))

def flow(headline, subhead, steps, btn, hsize=92, htop=404):
    rows = ""
    for s in steps:
        rows += f'<div class="row"><div class="mark">&#10003;</div><div class="label">{esc(s)}</div></div>'
    return (f'<div class="accent" style="top:{htop-26}px"></div>'
            f'<div class="headline" style="top:{htop}px;font-size:{hsize}px">{esc(headline)}</div>'
            f'<div class="subhead" style="top:660px">{esc(subhead)}</div>'
            f'<div class="rows" style="top:762px">{rows}</div>'
            + cta(btn))

def poll(question, options, foot_text, foot_tail, hsize=82, htop=300):
    opts = ""
    for i, o in enumerate(options):
        opts += (f'<div class="opt"><div class="optkey">{chr(65+i)}</div>'
                 f'<div class="optlabel">{esc(o)}</div></div>')
    return (f'<div class="accent" style="top:{htop-26}px"></div>'
            f'<div class="headline" style="top:{htop}px;font-size:{hsize}px">{esc(question)}</div>'
            f'<div class="polls" style="top:512px">{opts}</div>'
            + foot(foot_text, foot_tail))

def bigstat(num, label, caption, btn, numtop=250, numsize=280):
    return (f'<div class="bignum" style="top:{numtop}px;font-size:{numsize}px">{esc(num)}</div>'
            f'<div class="accent" style="top:{numtop+310}px"></div>'
            f'<div class="biglabel" style="top:{numtop+346}px">{esc(label)}</div>'
            f'<div class="subhead" style="top:{numtop+512}px">{esc(caption)}</div>'
            + cta(btn))

# ------------------------------------------------------------------ SET 1 SINGLES
POSTS = [
  # #5 · Day 3 AM · Industry poll (all)
  dict(file="s05_poll_hiring_speed.html", accent=BLUE, bg=None,
       label="Poll · What kills your hiring speed?",
       inner=poll("What kills your hiring speed the most?",
                  ["CV overload — too many to screen", "No-shows & candidate ghosting",
                   "Skill–role mismatch", "Salary expectation gaps"],
                  "Vote + comment your", "#1 →", hsize=80)),
  # #8 · Day 4 PM · Industry news / reactive take (all)
  dict(file="s08_news_ai_recruiters.html", accent=BLUE, bg=BASE+"bg_employer.png",
       label="Industry Take · AI in Hiring",
       inner=typographic("AI won't replace recruiters. Recruiters who use AI will replace those who don't.",
                         "— GROYOUTH ON THE 2026 HIRING SHIFT", "Agree, or not? →", hsize=76, htop=396)),
  # #12 · Day 6 PM · Community weekend note (all)
  dict(file="s12_community_weekend.html", accent=GREEN, bg=BASE+"seeker_bg.png",
       label="Weekend Note · Keep Going",
       inner=typographic("Every ‘you're hired’ started with one more try.",
                         "IF YOU'RE JOB-HUNTING THIS WEEKEND — ONE HONEST APPLICATION BEATS TEN COPY-PASTED ONES.",
                         "Tag someone job-hunting →", hsize=84, htop=404)),
  # #13 · Day 7 AM · Founder's desk (all)
  dict(file="s13_founder_human.html", accent=VIOLET, bg=BASE+"bg_founder.png",
       label="Founder's Desk · The Human Part",
       inner=typographic("Hiring is the most human thing a company does.",
                         "— FOUNDER'S DESK · AI SHOULD MAKE IT MORE HUMAN, NOT LESS",
                         "Your take? →", hsize=84, htop=404)),
  # #14 · Day 7 PM · Talent poll (job seekers)
  dict(file="s14_poll_seekers_2026.html", accent=GREEN, bg=None,
       label="Poll · What matters most in 2026?",
       inner=poll("Job seekers — what matters most in 2026?",
                  ["Salary & benefits", "Growth & learning", "Remote / flexibility", "Skills-first hiring"],
                  "Vote — we'll share the", "results →", hsize=78)),
  # #17 · Day 9 AM · Industry data big-stat (all)
  dict(file="s17_data_job_ready.html", accent=BLUE, bg=None,
       label="Skills-Gap Data · Job-Readiness",
       inner=bigstat("70%", "of Indian employers say candidates aren't job-ready.",
                     "The gap isn't talent — it's proof. Verified skills close it faster than another degree.",
                     "See the skills map →")),
  # #18 · Day 9 PM · Partner (service providers)
  dict(file="s18_partner_dashboard.html", accent=BLUE, bg=BASE+"bg_partner.png",
       label="For Agencies · One Dashboard",
       inner=flow("One dashboard. Every requirement. AI-matched.",
                  "Service providers run every open mandate from a single screen — GroYouth does the matching.",
                  ["Post every client requirement in one place",
                   "AI matches verified talent to each role",
                   "You place faster, with less overhead"],
                  "Join the network", hsize=76, htop=396)),
  # #20 · Day 10 PM · Employer poll (hiring orgs)
  dict(file="s20_poll_time_to_hire.html", accent=BLUE, bg=None,
       label="Poll · How long does hiring take?",
       inner=poll("How long does your hiring take, start to offer?",
                  ["Under 1 week", "2–3 weeks", "About a month", "2 months or more"],
                  "Vote — we'll share the", "benchmark →", hsize=80)),
]

def build():
    made = []
    for p in POSTS:
        out = os.path.join(HERE, p["file"])
        with open(out, "w") as f:
            f.write(frame(p["accent"], p["label"], p["inner"], p["bg"]))
        made.append(p["file"])
    print("generated:", ", ".join(made))

if __name__ == "__main__":
    build()

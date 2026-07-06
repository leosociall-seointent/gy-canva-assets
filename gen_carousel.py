#!/usr/bin/env python3
"""
Build EDITABLE multi-page Instagram carousels for Canva URL-import.

Editable anatomy (separate movable logo + live text layers, NO baked-in text),
extended to N pages by emitting multiple data-document-role="page" divs in one
document. Solid dark slides (no photo dependency) so numbers pop and every layer
stays editable on import.

Two slide kinds:
  * stat pages  — one huge number + label + sub   (post["stats"]  = [(num,label,sub)])
  * point pages — big index + title + sub          (post["points"] = [(title,sub)])
Per-post accent lane: talent/campus = green, employer/partner/industry = blue.

    python3 gen_carousel.py     # builds all Set-1 carousels
"""
import os, html

BASE   = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
HERE   = os.path.dirname(os.path.abspath(__file__))
LOGO   = BASE + "gy-logo.png"
INK    = "#0E1024"
GREEN, BLUE, VIOLET = "#52D695", "#47A3FF", "#B98CFF"

def css(accent):
  return f"""
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  .page {{ position:relative; width:1080px; height:1080px; overflow:hidden;
          background:{INK}; font-family:'Helvetica Neue', Arial, sans-serif; }}
  .logo {{ position:absolute; top:56px; left:60px; height:50px; }}
  .counter {{ position:absolute; top:64px; right:62px; color:#8A93AD;
    font-size:26px; font-weight:800; letter-spacing:3px; }}
  .pill {{ position:absolute; top:62px; right:60px; background:rgba(9,12,26,0.55);
    border:2px solid {accent}; color:{accent}; font-weight:700; font-size:22px;
    letter-spacing:2px; padding:12px 28px; border-radius:40px; }}
  /* cover */
  .cover-title {{ position:absolute; top:392px; left:64px; width:930px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:96px; line-height:0.97; letter-spacing:-1px; }}
  .cover-sub {{ position:absolute; top:724px; left:66px; width:840px; color:#EEF2FB;
    font-size:32px; font-weight:600; line-height:1.3; }}
  .swipe {{ position:absolute; left:66px; bottom:70px; color:{accent};
    font-size:34px; font-weight:800; letter-spacing:1px; }}
  /* stat */
  .snum {{ position:absolute; top:280px; left:60px; width:980px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:210px; line-height:0.88; letter-spacing:-2px; }}
  .saccent {{ position:absolute; top:566px; left:66px; width:110px; height:12px; background:{accent}; border-radius:6px; }}
  .slabel {{ position:absolute; top:606px; left:64px; width:940px; color:#FFFFFF;
    font-size:50px; font-weight:800; line-height:1.06; }}
  .ssub {{ position:absolute; top:812px; left:64px; width:900px; color:#EEF2FB;
    font-size:31px; font-weight:600; line-height:1.32; }}
  /* point */
  .pindex {{ position:absolute; top:244px; left:60px; color:{accent};
    font-family:Impact,'Arial Black',sans-serif; font-size:150px; line-height:1; letter-spacing:-2px; }}
  .ptitle {{ position:absolute; top:452px; left:64px; width:948px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:80px; line-height:0.99; letter-spacing:-1px; }}
  .psub {{ position:absolute; top:702px; left:64px; width:912px; color:#EEF2FB;
    font-size:33px; font-weight:600; line-height:1.32; }}
  /* cta */
  .cta-accent {{ position:absolute; top:388px; left:66px; width:110px; height:12px; background:{accent}; border-radius:6px; }}
  .cta-title {{ position:absolute; top:430px; left:64px; width:940px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:78px; line-height:0.98; letter-spacing:-1px; }}
  .cta-sub {{ position:absolute; top:742px; left:66px; width:880px; color:#EEF2FB;
    font-size:31px; font-weight:600; line-height:1.3; }}
  .cta-row {{ position:absolute; left:64px; bottom:66px; display:flex; align-items:center; }}
  .btn {{ background:{accent}; color:#08122B; font-weight:800; font-size:31px; padding:23px 38px; border-radius:14px; }}
  .url {{ color:#EEF2FB; font-size:29px; font-weight:700; margin-left:26px; }}
"""

def esc(s): return html.escape(str(s), quote=True)
def logo():  return f'<img class="logo" src="{LOGO}" alt="GroYouth logo">'

def cover_page(pill, title, sub, label):
    return f'''  <div class="page" data-document-role="page" data-label="{esc(label)}">
    {logo()}
    <div class="pill">{esc(pill)}</div>
    <div class="cover-title">{esc(title)}</div>
    <div class="cover-sub">{esc(sub)}</div>
    <div class="swipe">Swipe &#8594;</div>
  </div>'''

def stat_page(idx, total, num, label, sub):
    return f'''  <div class="page" data-document-role="page" data-label="Stat {idx} &#8212; {esc(label)}">
    {logo()}
    <div class="counter">{idx:02d} / {total:02d}</div>
    <div class="snum">{esc(num)}</div>
    <div class="saccent"></div>
    <div class="slabel">{esc(label)}</div>
    <div class="ssub">{esc(sub)}</div>
  </div>'''

def point_page(idx, total, title, sub):
    return f'''  <div class="page" data-document-role="page" data-label="Point {idx} &#8212; {esc(title)}">
    {logo()}
    <div class="counter">{idx:02d} / {total:02d}</div>
    <div class="pindex">{idx}</div>
    <div class="ptitle">{esc(title)}</div>
    <div class="psub">{esc(sub)}</div>
  </div>'''

def cta_page(title, sub, btn, label="CTA"):
    return f'''  <div class="page" data-document-role="page" data-label="{esc(label)}">
    {logo()}
    <div class="cta-accent"></div>
    <div class="cta-title">{esc(title)}</div>
    <div class="cta-sub">{esc(sub)}</div>
    <div class="cta-row"><div class="btn">{esc(btn)}</div><div class="url">groyouth.com</div></div>
  </div>'''

def doc(accent, pages):
    return ('<!doctype html>\n<html><head><meta charset="utf-8"><style>' + css(accent) +
            '</style></head>\n<body>\n' + "\n".join(pages) + "\n</body></html>")

def build(post, filename, accent=BLUE):
    items = post.get("stats") or post.get("points")
    is_stats = "stats" in post
    total = len(items)
    pages = [cover_page(post["pill"], post["cover_title"], post["cover_sub"], post.get("cover_label", "Cover"))]
    for i, item in enumerate(items, 1):
        if is_stats:
            num, label, sub = item
            pages.append(stat_page(i, total, num, label, sub))
        else:
            title, sub = item
            pages.append(point_page(i, total, title, sub))
    pages.append(cta_page(post["cta_title"], post["cta_sub"], post["cta_btn"], post.get("cta_label", "CTA")))
    out = os.path.join(HERE, filename)
    with open(out, "w") as f:
        f.write(doc(accent, pages))
    print("generated:", filename, f"({len(pages)} pages)")

# ---- #2 · Day 1 PM · The India hiring gap in 6 numbers (Industry / All) ----
HIRING_GAP = dict(
  pill="THE HIRING GAP",
  cover_title="India's hiring gap, in 6 numbers.",
  cover_sub="Save this — it reframes how you think about hiring in 2026.",
  cover_label="Cover — India hiring gap",
  stats=[
    ("1.5 Cr+", "graduates enter India's workforce every year", "The talent is here. Matching it isn't."),
    ("~50%",    "are rated ‘job-ready’ by employers",   "Half can't easily prove real skills."),
    ("40+",     "days to fill the average open role",            "Slow hiring drains momentum and money."),
    ("1 in 3",  "candidates ghost during hiring",                "No-shows burn recruiter hours every week."),
    ("₹5–7L", "the cost of a single bad hire",          "Wrong-fit hires drain salary, training and time."),
    ("#1",      "reason hires fail: skill–role mismatch",   "Not a people shortage — a matching one."),
  ],
  cta_title="India doesn't have a hiring problem. It has a matching problem.",
  cta_sub="GroYouth is the AI marketplace that matches verified talent to real roles — no agency in the middle.",
  cta_btn="Save + follow →",
  cta_label="CTA — matching problem",
)

# ---- #3 · Day 2 AM · 5 skills that get you hired in 2026 (Talent) ----
SKILLS = dict(
  pill="GET-HIRED SKILLS",
  cover_title="5 skills that get you hired in 2026.",
  cover_sub="No degree teaches these — but every employer screens for them. Swipe.",
  cover_label="Cover — 5 skills",
  points=[
    ("Problem-solving out loud", "Employers hire people who can think through a problem — not just recite the answer."),
    ("Clear written communication", "Most work is async now. The person understood the first time wins."),
    ("Working with AI tools", "Not replacing you — making you 2x. Show you can actually use them."),
    ("Owning an outcome", "‘I got it done’ beats ‘I did my part.’ Accountability is rare and obvious."),
    ("Learning speed", "Skills date fast. How quickly you pick up the next one is the real hire signal."),
  ],
  cta_title="Prove these with a verified GY SAT score.",
  cta_sub="One free 20-minute test turns skills you can't fit on a CV into proof employers can see.",
  cta_btn="Take the free GY SAT →",
  cta_label="CTA — GY SAT",
)

# ---- #9 · Day 5 AM · The true cost of one bad hire (Employer / data) ----
BAD_HIRE = dict(
  pill="COST OF A BAD HIRE",
  cover_title="The real cost of one bad hire.",
  cover_sub="It's not just salary. Here's the full bill — and how AI matching cuts it. Swipe.",
  cover_label="Cover — bad hire cost",
  stats=[
    ("₹5–7L", "the direct cost of one wrong hire", "Salary, onboarding and training you don't get back."),
    ("6 mo",    "before a bad fit is usually replaced", "Half a year of lost output and team drag."),
    ("2x",      "the workload dumped on everyone else", "Good people burn out covering the gap."),
    ("#1",      "cause: hiring on gut, not on fit", "No verified signal of real, role-ready skill."),
  ],
  cta_title="Match on proof, not gut.",
  cta_sub="Talent Match AI ranks candidates by verified fit — so your first hire is the right one.",
  cta_btn="Try Talent Match AI →",
  cta_label="CTA — Talent Match AI",
)

# ---- #15 · Day 8 AM · What your GY SAT score tells employers (Talent) ----
SAT_SCORE = dict(
  pill="YOUR GY SAT SCORE",
  cover_title="What your GY SAT score really tells employers.",
  cover_sub="It's not a grade. It's a hiring signal. Here's what they see. Swipe.",
  cover_label="Cover — SAT score",
  points=[
    ("Verified skill, not claimed skill", "The difference between ‘proficient in Excel’ and proof of it."),
    ("Role readiness at a glance", "Employers see fit for the job — not just a list of subjects."),
    ("How you stack up, fairly", "Same test for everyone. No degree-brand bias."),
    ("A reason to shortlist you", "A strong score is the nudge that turns ‘maybe’ into an interview."),
  ],
  cta_title="Turn your skills into a score employers trust.",
  cta_sub="The GY SAT is free and takes 20 minutes. Do it once, get found for months.",
  cta_btn="Take the free GY SAT →",
  cta_label="CTA — GY SAT",
)

# ---- #16 · Day 8 PM · From job post to shortlist in 3 steps (Employer) ----
POST_SHORTLIST = dict(
  pill="POST → SHORTLIST",
  cover_title="From job post to shortlist in 3 steps.",
  cover_sub="No agency, no CV pile. Here's how Talent Match AI works. Swipe.",
  cover_label="Cover — post to shortlist",
  points=[
    ("Post your role — free", "Describe the job once. It takes about 90 seconds."),
    ("AI matches verified talent", "Candidates ranked by real, tested fit — not keywords."),
    ("Shortlist and reach out", "Skip the 300-CV screen. Start with the best ten."),
  ],
  cta_title="Post a role and see your shortlist.",
  cta_sub="Posting is free. The first matched shortlist lands in minutes.",
  cta_btn="Post a role free →",
  cta_label="CTA — post a role",
)

BUILDS = [
  (HIRING_GAP,     "carousel_hiring_gap.html", BLUE),
  (SKILLS,         "c03_skills.html",          GREEN),
  (BAD_HIRE,       "c09_bad_hire.html",        BLUE),
  (SAT_SCORE,      "c15_sat_score.html",       GREEN),
  (POST_SHORTLIST, "c16_post_shortlist.html",  BLUE),
]

if __name__ == "__main__":
    for post, fn, accent in BUILDS:
        build(post, fn, accent)

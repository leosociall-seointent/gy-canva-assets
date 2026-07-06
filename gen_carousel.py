#!/usr/bin/env python3
"""
Build an EDITABLE multi-page Instagram carousel for Canva URL-import.

Same editable anatomy as gen_b_editable.py (separate movable logo + live text
layers, NO baked-in text), extended to N pages by emitting multiple
data-document-role="page" divs inside one document. Solid dark slides (no photo
dependency) so the numbers pop and every layer stays editable on import.

    python3 gen_carousel.py

Reuse for the other 14 calendar carousels: copy the POST block, swap cover/
stats/cta text, call build(post, "carousel_<slug>.html").
"""
import os, html

BASE   = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
HERE   = os.path.dirname(os.path.abspath(__file__))
LOGO   = BASE + "gy-logo.png"
INK    = "#0E1024"
ACCENT = "#47A3FF"   # all-audience / industry lane = blue

CSS = f"""
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  .page {{ position:relative; width:1080px; height:1080px; overflow:hidden;
          background:{INK}; font-family:'Helvetica Neue', Arial, sans-serif; }}
  .logo {{ position:absolute; top:56px; left:60px; height:50px; }}
  .counter {{ position:absolute; top:64px; right:62px; color:#8A93AD;
    font-size:26px; font-weight:800; letter-spacing:3px; }}
  .pill {{ position:absolute; top:62px; right:60px; background:rgba(9,12,26,0.55);
    border:2px solid {ACCENT}; color:{ACCENT}; font-weight:700; font-size:22px;
    letter-spacing:2px; padding:12px 28px; border-radius:40px; }}
  /* cover */
  .cover-title {{ position:absolute; top:392px; left:64px; width:920px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:98px; line-height:0.96; letter-spacing:-1px; }}
  .cover-sub {{ position:absolute; top:724px; left:66px; width:820px; color:#EEF2FB;
    font-size:32px; font-weight:600; line-height:1.3; }}
  .swipe {{ position:absolute; left:66px; bottom:70px; color:{ACCENT};
    font-size:34px; font-weight:800; letter-spacing:1px; }}
  /* stat */
  .snum {{ position:absolute; top:280px; left:60px; width:980px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:210px; line-height:0.88; letter-spacing:-2px; }}
  .saccent {{ position:absolute; top:566px; left:66px; width:110px; height:12px; background:{ACCENT}; border-radius:6px; }}
  .slabel {{ position:absolute; top:606px; left:64px; width:940px; color:#FFFFFF;
    font-size:50px; font-weight:800; line-height:1.06; }}
  .ssub {{ position:absolute; top:812px; left:64px; width:900px; color:#EEF2FB;
    font-size:31px; font-weight:600; line-height:1.32; }}
  /* cta */
  .cta-accent {{ position:absolute; top:388px; left:66px; width:110px; height:12px; background:{ACCENT}; border-radius:6px; }}
  .cta-title {{ position:absolute; top:430px; left:64px; width:940px; color:#FFFFFF;
    font-family:Impact,'Arial Black',sans-serif; font-size:78px; line-height:0.98; letter-spacing:-1px; }}
  .cta-sub {{ position:absolute; top:742px; left:66px; width:860px; color:#EEF2FB;
    font-size:31px; font-weight:600; line-height:1.3; }}
  .cta-row {{ position:absolute; left:64px; bottom:66px; display:flex; align-items:center; }}
  .btn {{ background:{ACCENT}; color:#08122B; font-weight:800; font-size:31px; padding:23px 38px; border-radius:14px; }}
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

def cta_page(title, sub, btn, label="CTA"):
    return f'''  <div class="page" data-document-role="page" data-label="{esc(label)}">
    {logo()}
    <div class="cta-accent"></div>
    <div class="cta-title">{esc(title)}</div>
    <div class="cta-sub">{esc(sub)}</div>
    <div class="cta-row"><div class="btn">{esc(btn)}</div><div class="url">groyouth.com</div></div>
  </div>'''

def doc(pages):
    return "<!doctype html>\n<html><head><meta charset=\"utf-8\"><style>" + CSS + \
           "</style></head>\n<body>\n" + "\n".join(pages) + "\n</body></html>"

def build(post, filename):
    stats = post["stats"]; total = len(stats)
    pages = [cover_page(post["pill"], post["cover_title"], post["cover_sub"], post.get("cover_label","Cover"))]
    for i,(num,label,sub) in enumerate(stats, 1):
        pages.append(stat_page(i, total, num, label, sub))
    pages.append(cta_page(post["cta_title"], post["cta_sub"], post["cta_btn"], post.get("cta_label","CTA")))
    out = os.path.join(HERE, filename)
    with open(out,"w") as f: f.write(doc(pages))
    print("generated:", filename, f"({len(pages)} pages)")

# ---- Calendar post #2: The India hiring gap in 6 numbers (Industry / All) ----
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

if __name__ == "__main__":
    build(HIRING_GAP, "carousel_hiring_gap.html")

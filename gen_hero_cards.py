#!/usr/bin/env python3
"""Photoreal hero cards (Option A2) — FLUX background + editable text over a scrim.
Cleaner than the graphic cards: big headline + one-line sub + CTA, photo as the star.
LOGO-FREE (kicker + pill only). Renders local flux_*.png; HTML -> square PDF -> Canva.
    python3 gen_hero_cards.py   # writes hero_*.html (needs flux_*.png present)
"""
NAVY="#0E1024"; BLUE="#47A3FF"; GREEN="#52D695"; VIOLET="#B98CFF"; GOLD="#E4B95B"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1080"><style>
  @page{size:1080px 1080px;margin:0;}
  *{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  html,body{width:1080px;height:1080px;}
  .page{position:relative;width:1080px;height:1080px;overflow:hidden;
    font-family:'Helvetica Neue',Arial,sans-serif;color:#EEF2FB;}
  .bg{position:absolute;top:0;left:0;width:1080px;height:1080px;object-fit:cover;}
  .scrim{position:absolute;top:0;left:0;width:1080px;height:1080px;
    background:linear-gradient(to bottom, rgba(6,8,20,.55) 0%, rgba(6,8,20,.05) 20%, rgba(6,8,20,.10) 42%, rgba(6,8,20,.80) 74%, rgba(6,8,20,.94) 100%);}
  .wrap{position:absolute;top:0;left:0;width:1080px;height:1080px;
    padding:60px 64px;display:flex;flex-direction:column;}
  .top{display:flex;justify-content:space-between;align-items:center;}
  .kick{color:%(acc)s;font-weight:800;font-size:22px;letter-spacing:4px;text-transform:uppercase;text-shadow:0 2px 10px rgba(0,0,0,.6);}
  .pill{border:2px solid %(acc)s;color:%(acc)s;font-weight:800;font-size:20px;letter-spacing:2px;
    padding:11px 26px;border-radius:40px;white-space:nowrap;background:rgba(6,8,20,.35);}
  .h1{font-family:Impact,'Arial Black',sans-serif;color:#fff;letter-spacing:-1px;line-height:1.02;
    text-shadow:0 3px 24px rgba(0,0,0,.55);}
  .sub{color:#E6EAF6;font-weight:600;text-shadow:0 2px 14px rgba(0,0,0,.6);}
  .foot{display:flex;align-items:center;gap:24px;margin-top:34px;}
  .btn{background:%(acc)s;color:#08122B;font-weight:800;font-size:29px;padding:20px 34px;border-radius:14px;white-space:nowrap;}
  .url{color:#EEF2FB;font-size:27px;font-weight:800;text-shadow:0 2px 10px rgba(0,0,0,.6);}
</style></head><body>"""

def hero(bgimg, acc, kicker, pill, headline, sub, btn):
    head = HEAD.replace("%(acc)s", acc)
    inner = (f'<div class="top"><div class="kick">{kicker}</div><div class="pill">{pill}</div></div>'
             f'<div style="margin-top:auto;">'
             f'<div class="h1" style="font-size:82px;width:900px;">{headline}</div>'
             f'<div class="sub" style="font-size:34px;margin-top:20px;width:820px;">{sub}</div>'
             f'<div class="foot"><div class="btn">{btn} &#8594;</div><div class="url">groyouth.com</div></div>'
             f'</div>')
    return head + f'<div class="page"><img class="bg" src="{bgimg}"><div class="scrim"></div><div class="wrap">{inner}</div></div></body></html>'

# (filename, flux_bg, accent, kicker, pill, headline, sub, btn)
CARDS = [
 ("hero_12_weekend.html","flux_12_weekend.png",GREEN,"WEEKEND","COMMUNITY",
   "Someone just got found.","You&#8217;re next &#8212; your skills, verified in 20 minutes.","Start free"),
 ("hero_15_sat.html","flux_15_sat.png",GREEN,"GY SAT","TALENT",
   "Your score is proof, not a grade.","Show employers what you can actually do.","Take the test free"),
 ("hero_29_route.html","flux_29_route.png",BLUE,"TALENT ROUTE","EMPLOYER",
   "The best candidate isn&#8217;t job-hunting.","Talent Route surfaces passive, verified talent.","Book a demo"),
 ("hero_32_team.html","flux_32_team.png",BLUE,"VOLUME HIRING","EMPLOYER",
   "Hiring 10+ this quarter?","Let AI build every shortlist in parallel.","Book a demo"),
 ("hero_42_interview.html","flux_42_interview.png",GREEN,"INTERVIEW PREP","TALENT",
   "7 questions every fresher gets.","Walk in with clean answers.","Prep on GroYouth"),
 ("hero_46_post.html","flux_46_post.png",BLUE,"POST A JOB","EMPLOYER",
   "Post a job in 90 seconds.","Title, skills, done &#8212; matches start immediately.","Post free"),
 ("hero_47_matches.html","flux_47_matches.png",GREEN,"REAL MATCHES","COMMUNITY",
   "Real people, real matches.","The point was never the tech &#8212; it&#8217;s who got hired.","Share your story"),
 ("hero_54_hire.html","flux_54_hire.png",BLUE,"TALENT MATCH AI","EMPLOYER",
   "Your next hire is already here.","Verified, ranked, waiting to be matched.","Book a demo"),
]
if __name__ == "__main__":
    for fn,bg,acc,k,p,h,s,b in CARDS:
        open(fn,"w").write(hero(bg,acc,k,p,h,s,b))
    print("wrote %d hero cards" % len(CARDS))

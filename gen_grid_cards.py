#!/usr/bin/env python3
"""
Grid-completion editable cards (Option A) for GroYouth's 60-post July grid.
LOGO-FREE per Leo (7/15): NO logo image is embedded anywhere. Top-left carries a
plain pillar kicker (text), top-right an audience pill. Branding/logo is added in
Canva from the brand kit as a separate editable layer.

Square-canvas fix (proven 14-Jul): .page is a plain 1080x1080 block with a
full-bleed .bg layer -> render to a 1080x1080 PDF via headless Chrome -> Canva
imports it as a native EDITABLE design (text stays extractable).

    python3 gen_grid_cards.py            # writes grid_*.html for every post below
Then render each to pdf/grid_*.pdf with Chrome --print-to-pdf (see render_pdfs.sh).
"""
BASE = "https://raw.githubusercontent.com/leosociall-seointent/gy-canva-assets/main/"
BG_NAVY, BG_VIOLET, BG_RADIAL = BASE+"ns_bg_navy.png", BASE+"ns_bg_violet.png", BASE+"ns_bg_radial.png"

NAVY="#0E1024"; BLUE="#47A3FF"; GREEN="#52D695"; VIOLET="#B98CFF"; GOLD="#E4B95B"; INK="#EEF2FB"
PANEL="#14162E"

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1080"><style>
  @page{size:1080px 1080px;margin:0;}
  *{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  html,body{width:1080px;height:1080px;}
  .page{position:relative;width:1080px;height:1080px;overflow:hidden;
    font-family:'Helvetica Neue',Arial,sans-serif;color:#EEF2FB;}
  .bg{position:absolute;top:0;left:0;width:1080px;height:1080px;object-fit:cover;}
  .wrap{position:absolute;top:0;left:0;width:1080px;height:1080px;
    padding:60px 64px;display:flex;flex-direction:column;}
  .top{display:flex;justify-content:space-between;align-items:center;}
  .kick{color:%(acc)s;font-weight:800;font-size:22px;letter-spacing:4px;text-transform:uppercase;}
  .pill{border:2px solid %(acc)s;color:%(acc)s;font-weight:800;font-size:20px;
    letter-spacing:2px;padding:11px 26px;border-radius:40px;white-space:nowrap;}
  .h1{font-family:Impact,'Arial Black',sans-serif;color:#fff;letter-spacing:-1px;line-height:1.03;}
  .sub{color:#B7C0DA;font-weight:600;}
  .foot{display:flex;align-items:center;gap:24px;margin-top:auto;}
  .btn{background:%(acc)s;color:#08122B;font-weight:800;font-size:29px;
    padding:20px 34px;border-radius:14px;white-space:nowrap;}
  .url{color:#EEF2FB;font-size:27px;font-weight:800;}
</style></head><body>"""

def page(bgimg, acc, kicker, pill, inner):
    head = HEAD % {"acc": acc}
    top = f'<div class="top"><div class="kick">{kicker}</div><div class="pill">{pill}</div></div>'
    return head + f'<div class="page"><img class="bg" src="{bgimg}"><div class="wrap">{top}{inner}</div></div></body></html>'

def foot(btn, acc, url="groyouth.com", right=False):
    b = f'<div class="btn">{btn} &#8594;</div>' if btn else ''
    push = ' style="margin-left:auto;"' if (right or not btn) else ''
    u = f'<div class="url"{push}>{url}</div>'
    return f'<div class="foot">{b}{u}</div>'

# ---------------- layouts ----------------
def L_quote(q_html, attrib, acc):
    return (f'<div style="font-family:Georgia,serif;font-size:150px;line-height:0.6;color:{acc};margin-top:46px;">&#8220;</div>'
            f'<div style="font-family:Georgia,serif;font-size:60px;line-height:1.28;color:#fff;font-weight:700;margin-top:12px;width:920px;">{q_html}</div>'
            f'<div style="font-size:30px;font-weight:700;color:#C9CFE6;margin-top:38px;">&#8212; {attrib}</div>')

def L_poll(headline, options, acc, tag="POLL &#183; VOTE BELOW"):
    chips=""
    letters=["A","B","C","D"]
    for i,o in enumerate(options):
        chips+=(f'<div style="display:flex;align-items:center;gap:20px;background:{PANEL};border:1.5px solid #262a45;'
                f'border-radius:16px;padding:26px 30px;margin-bottom:20px;">'
                f'<div style="width:52px;height:52px;border-radius:50%;border:2px solid {acc};color:{acc};'
                f'font-family:Impact,sans-serif;font-size:28px;display:flex;align-items:center;justify-content:center;flex:0 0 auto;">{letters[i]}</div>'
                f'<div style="font-size:33px;font-weight:800;color:#fff;">{o}</div></div>')
    return (f'<div class="h1" style="font-size:60px;margin-top:44px;width:940px;">{headline}</div>'
            f'<div style="margin-top:38px;">{chips}</div>'
            f'<div class="foot"><div class="pill" style="margin-left:auto;">{tag}</div></div>')

def L_data(headline, bigstat, statlabel, rows, acc, sub=None):
    r=""
    for i,(lab,val) in enumerate(rows):
        border="" if i==0 else "border-top:1px solid #262a45;"
        r+=(f'<div style="display:flex;align-items:center;padding:22px 8px;{border}">'
            f'<div style="flex:1;font-size:30px;font-weight:800;color:#fff;">{lab}</div>'
            f'<div style="font-size:33px;font-weight:800;color:{acc};font-family:Georgia,serif;">{val}</div></div>')
    big=(f'<div class="h1" style="font-size:120px;color:{acc};font-family:Georgia,serif;margin-top:6px;">{bigstat}'
         f'<span style="font-size:34px;font-family:Helvetica;color:#B7C0DA;font-weight:700;margin-left:16px;">{statlabel}</span></div>') if bigstat else ''
    subhtml=f'<div class="sub" style="font-size:30px;margin-top:10px;">{sub}</div>' if sub else ''
    return (f'<div class="h1" style="font-size:56px;margin-top:40px;width:940px;">{headline}</div>{subhtml}{big}'
            f'<div style="background:{PANEL};border-radius:20px;padding:8px 28px;margin-top:26px;">{r}</div>'
            f'<div class="foot"><div class="url" style="margin-left:auto;">groyouth.com</div></div>')

def L_steps(headline, sub, steps, btn, acc):
    s=""
    for n,(t,d) in enumerate(steps,1):
        s+=(f'<div style="display:flex;align-items:center;background:{PANEL};border-radius:18px;padding:26px 32px;margin-bottom:20px;">'
            f'<div style="width:70px;height:70px;border-radius:50%;background:{acc};color:#08122B;font-family:Impact,sans-serif;'
            f'font-size:40px;display:flex;align-items:center;justify-content:center;margin-right:28px;flex:0 0 auto;">{n}</div>'
            f'<div><div style="font-size:35px;font-weight:800;color:#fff;">{t}</div>'
            f'<div style="font-size:24px;font-weight:600;color:#97A1C4;margin-top:5px;">{d}</div></div></div>')
    subhtml=f'<div class="sub" style="font-size:30px;margin-top:12px;">{sub}</div>' if sub else ''
    return (f'<div class="h1" style="font-size:58px;margin-top:42px;width:940px;">{headline}</div>{subhtml}'
            f'<div style="margin-top:32px;">{s}</div>{foot(btn,acc)}')

def L_service(headline, sub, bullets, btn, acc):
    b=""
    for x in bullets:
        b+=(f'<div style="display:flex;align-items:flex-start;gap:18px;margin-bottom:20px;">'
            f'<div style="color:{acc};font-size:32px;font-weight:800;line-height:1;flex:0 0 auto;">&#10003;</div>'
            f'<div style="font-size:32px;font-weight:700;color:#EEF2FB;">{x}</div></div>')
    return (f'<div class="h1" style="font-size:64px;margin-top:44px;width:940px;">{headline}</div>'
            f'<div class="sub" style="font-size:31px;margin-top:16px;width:900px;">{sub}</div>'
            f'<div style="background:{PANEL};border-radius:20px;padding:34px 34px;margin-top:34px;">{b}</div>'
            f'{foot(btn,acc)}')

def L_compare(headline, left_t, left_items, right_t, right_items, btn, acc):
    def col(title,items,color,dim):
        li="".join(f'<div style="font-size:26px;font-weight:600;color:{"#97A1C4" if dim else "#EEF2FB"};margin-bottom:14px;">&#8226; {i}</div>' for i in items)
        return (f'<div style="flex:1;background:{PANEL};border-radius:18px;padding:30px 28px;{"opacity:.75;" if dim else f"border:2px solid {color};"}">'
                f'<div style="font-size:30px;font-weight:800;color:{color};margin-bottom:20px;letter-spacing:1px;">{title}</div>{li}</div>')
    return (f'<div class="h1" style="font-size:58px;margin-top:42px;width:940px;">{headline}</div>'
            f'<div style="display:flex;gap:26px;margin-top:40px;">{col(left_t,left_items,"#8891AE",True)}{col(right_t,right_items,acc,False)}</div>'
            f'{foot(btn,acc)}')

def L_news(tab, acc):
    return (f'<div style="margin-top:60px;background:{PANEL};border-left:8px solid {acc};border-radius:14px;padding:44px 40px;width:940px;min-height:300px;">'
            f'<div style="font-size:22px;font-weight:800;letter-spacing:3px;color:{acc};">THE HEADLINE</div>'
            f'<div style="font-size:44px;font-weight:800;color:#fff;margin-top:18px;line-height:1.2;">[ Drop the week&#8217;s hiring headline here ]</div></div>'
            f'<div style="margin-top:26px;background:{acc};color:#08122B;display:inline-block;padding:16px 30px;border-radius:12px;font-size:28px;font-weight:800;">{tab}</div>'
            f'<div style="font-size:30px;font-weight:600;color:#B7C0DA;margin-top:22px;width:940px;">[ GroYouth&#8217;s one-line take goes here. ]</div>'
            f'<div class="foot"><div class="url" style="margin-left:auto;">groyouth.com</div></div>')

# ---------------- posts ----------------
# each: (filename, bg, accent, kicker, pill, inner)
P=[]
def add(fn,bg,acc,kick,pill,inner): P.append((fn,bg,acc,kick,pill,inner))

# ---- Founder quotes (typographic, violet) ----
add("grid_13_founder_human.html",BG_VIOLET,VIOLET,"FOUNDER'S DESK","FOUNDER",
    L_quote('Hiring is the most human thing a company does. AI should make it <span style="color:%s;">more</span> human, not less.'%VIOLET,"Founder&#8217;s Desk, GroYouth",VIOLET))
add("grid_35_founder_trust.html",BG_VIOLET,VIOLET,"FOUNDER'S DESK","FOUNDER",
    L_quote('A marketplace isn&#8217;t built on features. It&#8217;s built on <span style="color:%s;">trust</span> &#8212; earned twice, on both sides.'%VIOLET,"Founder&#8217;s Desk, GroYouth",VIOLET))
add("grid_44_founder_math.html",BG_VIOLET,VIOLET,"FOUNDER'S DESK","FOUNDER",
    L_quote('The free ATS isn&#8217;t charity. Free tool &#8594; more companies &#8594; more matches &#8594; more talent. The <span style="color:%s;">flywheel</span> starts with zero friction.'%VIOLET,"Founder&#8217;s Desk, GroYouth",VIOLET))
add("grid_53_founder_next.html",BG_VIOLET,VIOLET,"FOUNDER'S DESK","FOUNDER",
    L_quote('Month one was about <span style="color:%s;">showing up.</span> Month two is about <span style="color:%s;">showing proof.</span>'%(VIOLET,VIOLET),"Founder&#8217;s Desk, GroYouth",VIOLET))

# ---- Polls ----
add("grid_28_poll_skills_degrees.html",BG_VIOLET,VIOLET,"FOUNDER'S POLL","VOTE",
    L_poll("Should skills matter more than degrees in hiring?",["Yes","No","Depends on the role"],VIOLET))
add("grid_43_poll_priority.html",BG_NAVY,BLUE,"INDUSTRY POLL","VOTE",
    L_poll("Biggest 2026 hiring priority?",["Speed","Quality of hire","Cost","Culture-fit"],BLUE))
add("grid_48_poll_switch.html",BG_NAVY,BLUE,"EMPLOYER POLL","VOTE",
    L_poll("What would make you switch hiring platforms?",["Speed","Cost","Quality of matches","Support"],BLUE))
add("grid_56_poll_postmore.html",BG_NAVY,GREEN,"COMMUNITY POLL","VOTE",
    L_poll("What should we post more of?",["Job tips","Skill tests","Employer insights","Founder notes"],GREEN))
add("grid_34_poll_skillstest.html",BG_NAVY,GREEN,"TALENT POLL","VOTE",
    L_poll("Would you take a skills test if it got you found by employers?",["Yes","Maybe","No"],GREEN))

# ---- Data / industry ----
add("grid_17_data_jobready.html",BG_NAVY,BLUE,"INDUSTRY DATA","RESEARCH",
    L_data("Candidates aren&#8217;t job-ready, say Indian employers","70%","of employers agree",
      [("Communication gap","#1"),("Practical skills gap","#2"),("Tool/AI fluency gap","#3"),("Role-fit mismatch","#4")],BLUE,
      sub="The gap isn&#8217;t talent &#8212; it&#8217;s proof."))
add("grid_23_data_timetohire.html",BG_NAVY,BLUE,"INDUSTRY DATA","RESEARCH",
    L_data("Time-to-hire by sector &#8212; India 2026",None,None,
      [("IT / Software","28 days"),("BFSI","34 days"),("Healthcare","31 days"),("Retail","19 days"),("Manufacturing","26 days")],BLUE,
      sub="Where does yours sit?"))
add("grid_33_data_migration.html",BG_NAVY,BLUE,"INDUSTRY DATA","RESEARCH",
    L_data("Where India&#8217;s talent is moving &#8212; 2026",None,None,
      [("Tier-2 cities rising","+ demand"),("Remote / hybrid roles","+ share"),("Metro-to-metro churn","steady"),("Return-to-hometown","growing")],BLUE,
      sub="The talent map is being redrawn."))
add("grid_41_data_costperhire.html",BG_NAVY,BLUE,"INDUSTRY DATA","COMPARE",
    L_data("Cost-per-hire &#8212; three ways",None,None,
      [("Recruitment agency","8.33% of CTC"),("Job board spend","per-post + time"),("GroYouth marketplace","lowest, verified")],BLUE,
      sub="Same hire. Very different bill."))
add("grid_50_data_premiumskills.html",BG_NAVY,GREEN,"INDUSTRY DATA","RESEARCH",
    L_data("Skills India will pay a premium for &#8212; H2 2026",None,None,
      [("AI / prompt fluency","premium"),("Data storytelling","premium"),("Commercial judgement","premium"),("Cross-functional comms","premium")],GREEN,
      sub="Not all of them are technical."))
add("grid_55_data_month1.html",BG_NAVY,BLUE,"BUILD IN PUBLIC","TRANSPARENCY",
    L_data("One month of GroYouth, by the numbers",None,None,
      [("Reach","[ real # ]"),("Matches made","[ real # ]"),("Signups","[ real # ]"),("Roles posted","[ real # ]")],BLUE,
      sub="No vanity spin &#8212; overlay the real dashboard numbers in edit."))

# ---- Service / single ----
add("grid_18_partner_dashboard.html",BG_NAVY,GOLD,"FOR AGENCIES","PARTNER",
    L_service("One dashboard. Every requirement. AI-matched.","For sourcing agencies juggling five clients from five inboxes.",
      ["All client requirements in one view","Verified talent, AI-matched to each","Less admin, more placements, no new headcount"],"Join the network",GOLD))
add("grid_24_free_ats.html",BG_NAVY,BLUE,"FREE ATS","EMPLOYER",
    L_service("Post, track, hire &#8212; &#8377;0.","The GY AI ATS is genuinely free. No trial wall, no &#8216;contact sales&#8217;.",
      ["Post roles in 90 seconds","Track every applicant in one pipeline","AI-matched, verified candidates"],"Set it up in 5 min",BLUE))
add("grid_29_talent_route.html",BG_NAVY,BLUE,"TALENT ROUTE","EMPLOYER",
    L_service("The best candidate isn&#8217;t job-hunting.","Talent Route surfaces passive, verified talent that never hits your inbox.",
      ["Reach the 70% who aren&#8217;t applying","Verified, ranked by real fit","Before your competitor does"],"Book a demo",BLUE))
add("grid_32_volume_hiring.html",BG_NAVY,BLUE,"VOLUME HIRING","EMPLOYER",
    L_service("Hiring 10+ this quarter? Let AI build the shortlist.","CV-by-CV doesn&#8217;t scale &#8212; and neither do your recruiters.",
      ["Every shortlist built in parallel","Ranked by fit, not gut-feel","Your team focuses on the interview"],"Book a demo",BLUE))
add("grid_38_partner_scale.html",BG_NAVY,GOLD,"FOR AGENCIES","PARTNER",
    L_service("Scale placements without scaling headcount.","GroYouth&#8217;s matching engine multiplies your team&#8217;s output.",
      ["Same team, more fills","Better margins per placement","The tech cost is on us"],"Join the network",GOLD))
add("grid_46_post_90s.html",BG_NAVY,BLUE,"POST A JOB","EMPLOYER",
    L_service("Post a job in 90 seconds.","Title, skills, done. Matches start immediately &#8212; no endless forms.",
      ["Three fields, not thirty","Free to post","Verified matches within minutes"],"Post free",BLUE))
add("grid_51_partner_7030.html",BG_NAVY,GOLD,"FOR AGENCIES","PARTNER",
    L_service("Why 70:30 beats a fixed placement fee.","A fixed fee caps your upside. 70:30 scales with the volume you place.",
      ["The more you place, the more you keep","No platform to build or maintain","We carry the tech cost"],"Run the numbers",GOLD))
add("grid_54_next_hire.html",BG_NAVY,BLUE,"TALENT MATCH AI","EMPLOYER",
    L_service("Your next hire is already in the marketplace.","Verified, ranked, and waiting to be matched &#8212; stop searching, start matching.",
      ["No three-week CV hunt","Verified candidates only","Ranked by real fit"],"Book a demo",BLUE))
add("grid_58_bundle.html",BG_NAVY,BLUE,"ONE LOGIN","EMPLOYER",
    L_service("Free ATS + AI matching, one login.","The two things every hiring team wants &#8212; behind a single free login.",
      ["A real ATS, not a trial","AI matching built in","No &#8216;contact sales&#8217; wall"],"Start free",BLUE))

# ---- Talent value carousels rendered as single hero cards ----
add("grid_22_redflags.html",BG_NAVY,GREEN,"JOB SAFETY","TALENT",
    L_service("5 red-flag job posts &#8212; and how to spot a real one.","If a &#8216;job&#8217; asks you to pay to apply, it isn&#8217;t a job.",
      ["Upfront &#8216;registration fee&#8217;","Vague JD, no real company","&#8216;Earn &#8377;50k/week from home&#8217;"],"Read the guide",GREEN))
add("grid_31_read_jd.html",BG_NAVY,GREEN,"CAREER TIPS","TALENT",
    L_steps("How to read a JD like a recruiter","Stop applying blind. Decode what they actually test.",
      [("Split must-have vs nice-to-have","The first 3 lines are the real filter."),
       ("Decode the buzzwords","&#8216;Fast-paced&#8217; = priorities shift; ask how."),
       ("Match to proof, not keywords","Map each ask to something you can show.")],"Get matched",GREEN))
add("grid_42_interview_qs.html",BG_NAVY,GREEN,"INTERVIEW PREP","TALENT",
    L_service("7 questions every fresher gets &#8212; clean answers.","Save this before your next interview.",
      ["&#8216;Tell me about yourself&#8217; &#8212; 3-part frame","&#8216;Your weakness&#8217; &#8212; real + fixing it","&#8216;Why hire you&#8217; &#8212; proof, not adjectives"],"Prep on GroYouth",GREEN))
add("grid_15_sat_score.html",BG_NAVY,GREEN,"GY SAT","TALENT",
    L_service("What your GY SAT score tells employers.","It&#8217;s not a grade &#8212; it&#8217;s proof, in the language they hire on.",
      ["Aptitude + role-fit, verified","Skills employers actually trust","One number that opens doors"],"Take the test free",GREEN))

# ---- Comparison ----
add("grid_36_before_after.html",BG_NAVY,BLUE,"BEFORE / AFTER","EMPLOYER",
    L_compare("Hiring without vs with Talent Match AI",
      "BEFORE",["300 CVs by hand","2&#8211;3 weeks to shortlist","Gut-feel guesses","Ghosting + re-posts"],
      "WITH GROYOUTH",["Ranked shortlist in minutes","Verified skills, not claims","Matched on real fit","One clean pipeline"],"Try it free",BLUE))
add("grid_52_li_vs_gy.html",BG_NAVY,GREEN,"GET FOUND","TALENT",
    L_compare("Seen everywhere vs found where it counts",
      "MOST PLATFORMS",["1 of 100M profiles","You chase every post","Seen, rarely matched"],
      "GROYOUTH",["A verified profile","Employers matched to you","Found, not just seen"],"Create your profile",GREEN))

# ---- News frames ----
add("grid_08_news_ai.html",BG_NAVY,BLUE,"INDUSTRY NEWS","OUR TAKE", L_news("OUR TAKE",BLUE))
add("grid_26_news_good.html",BG_NAVY,GREEN,"GOOD NEWS","GOOD SIGN?", L_news("GOOD SIGN?",GREEN))
add("grid_39_news_read.html",BG_NAVY,BLUE,"INDUSTRY NEWS","OUR READ", L_news("OUR READ",BLUE))
add("grid_59_news_monthend.html",BG_NAVY,BLUE,"MONTH-END","OUR TAKE", L_news("OUR TAKE",BLUE))

# ---- Community / testimonial ----
add("grid_12_weekend_win.html",BG_RADIAL,GREEN,"WEEKEND","COMMUNITY",
    L_quote('Someone just got <span style="color:%s;">found.</span> You&#8217;re next.'%GREEN,"A GroYouth match, this week",GREEN))
add("grid_47_real_matches.html",BG_NAVY,GREEN,"REAL MATCHES","COMMUNITY",
    L_service("Real people, real matches.","The point was never the tech &#8212; it&#8217;s who got hired.",
      ["A fresher who got found","An HR who filled a role in days","A campus that placed a batch"],"Share your story",GREEN))

for fn,bg,acc,kick,pill,inner in P:
    open(fn,"w").write(page(bg,acc,kick,pill,inner));
print("wrote %d grid cards"%len(P))
print("\n".join(fn for fn,*_ in P))

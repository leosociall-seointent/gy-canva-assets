import re
# color swaps: dark theme -> light theme
REPS = [
  ('ns_bg_navy.png','ns_bg_light.png'),
  ('ns_bg_violet.png','ns_bg_light.png'),
  ('ns_bg_radial.png','ns_bg_light.png'),
  # base text -> navy ink
  ('color:#EEF2FB','color:#0E1024'), ('color:#fff','color:#0E1024'), ('color:#FFFFFF','color:#0E1024'),
  # dark panels -> white cards
  ('#14162E','#FFFFFF'), ('#12181A','#FFFFFF'), ('background:#08122B','background:#0E1024'),
  # dark borders -> light grey
  ('#262a45','#E3E8F2'), ('#223022','#E3E8F2'),
  # muted subtext -> slate
  ('#B7C0DA','#5B6478'), ('#97A1C4','#5B6478'), ('#C9CFE6','#5B6478'), ('#8891AE','#8A93A8'),
  # deepen accents for contrast on light
  ('#52D695','#12A66B'), ('#47A3FF','#2E7FE0'), ('#B98CFF','#7C4DE0'), ('#E4B95B','#C08A1E'),
]
def to_light(html):
    for a,b in REPS: html=html.replace(a,b)
    # panels that became pure white need a subtle border for definition on a light bg
    html=html.replace('border-radius:20px;padding:8px 28px;','border-radius:20px;padding:8px 28px;border:1px solid #E3E8F2;')
    html=html.replace('border-radius:20px;padding:34px 34px;','border-radius:20px;padding:34px 34px;border:1px solid #E3E8F2;')
    html=html.replace('border-radius:18px;padding:26px 32px;','border-radius:18px;padding:26px 32px;border:1px solid #E3E8F2;')
    html=html.replace('border-radius:16px;padding:26px 30px;','border-radius:16px;padding:26px 30px;border:1px solid #E3E8F2;')
    return html
import sys
for fn in sys.argv[1:]:
    h=open(fn).read()
    out='light_'+fn
    open(out,'w').write(to_light(h)); print('wrote',out)

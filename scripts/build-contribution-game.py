"""Render a self-contained animated contribution arcade from public GitHub data."""
import argparse
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'assets/contributions.json'

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tip = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('data-date') and attrs.get('data-level'):
            self.cells[attrs['id']] = {'date': attrs['data-date'], 'level': int(attrs['data-level']), 'count': None}
        if tag == 'tool-tip':
            self.tip = attrs.get('for')
    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.tip = None
    def handle_data(self, data):
        if self.tip in self.cells and 'contribution' in data:
            first = data.strip().split()[0]
            self.cells[self.tip]['count'] = 0 if first == 'No' else int(first.replace(',', ''))

def read_calendar(html):
    parser = CalendarParser()
    parser.feed(html)
    days = sorted(parser.cells.values(), key=lambda d: d['date'])
    if len(days) < 350 or any(d['count'] is None for d in days):
        raise ValueError('Incomplete GitHub calendar: refusing to replace existing data.')
    for d in days:
        if not 0 <= d['level'] <= 4 or d['count'] < 0:
            raise ValueError('Invalid contribution cell.')
    return days

def render(days, theme):
    bg,panel,text,muted,edge,cyan,purple,green = ('#070C18','#0C1425','#EAF2FF','#8C9FBC','#20334D','#22D3EE','#B09AFF','#34D399') if theme=='dark' else ('#EDF3FC','#F8FAFF','#172B47','#546C89','#CDDCEC','#087D9D','#7951D0','#138467')
    palette = ['#152338','#155366','#148396','#21B6BE','#5DE4CD'] if theme=='dark' else ['#DFE8F4','#B2DEE0','#76C1C6','#389DA8','#147F8C']
    start=date.fromisoformat(days[0]['date'])
    origin=start-timedelta(days=(start.weekday()+1)%7)
    cols=((date.fromisoformat(days[-1]['date'])-origin).days//7)+1
    step=19
    x0=98+(53-cols)*step/2
    y0=207
    total=sum(d['count'] for d in days)
    active=sum(d['count']>0 for d in days)
    best=max(d['count'] for d in days)
    def t(x,y,value,size=12,color=None,extra=''):
        return f'<text x="{x}" y="{y}" fill="{color or text}" font-size="{size}" {extra}>{escape(str(value))}</text>'
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="456" viewBox="0 0 1200 456" role="img" aria-labelledby="title desc">
<title id="title">Contribution Defender — dhuyhoang1406</title><desc id="desc">Animated space arcade using real GitHub contribution cells from {days[0]['date']} to {days[-1]['date']}. {total} contributions, {active} active days. The spaceship and lasers are decorative; the calendar counts remain unchanged.</desc>
<defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{cyan}" stop-opacity=".05"/><stop offset="1" stop-color="{cyan}" stop-opacity=".7"/></linearGradient><pattern id="stars" width="97" height="61" patternUnits="userSpaceOnUse"><circle cx="19" cy="17" r=".8" fill="{muted}" opacity=".3"/><circle cx="69" cy="49" r=".5" fill="{cyan}" opacity=".5"/></pattern></defs>
<style>text{{font-family:Consolas,'Liberation Mono',monospace}}@media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}</style>
<rect x="1" y="1" width="1198" height="454" rx="18" fill="{bg}" stroke="{edge}"/><rect x="2" y="54" width="1196" height="342" rx="16" fill="url(#stars)"/>
<path d="M24 54H1176M24 396H1176" stroke="{edge}"/>
'''
    s+=t(26,34,'CONTRIBUTION DEFENDER',18,cyan,'font-weight="700" letter-spacing="2"')+t(1174,33,'ARCADE / AUTOPILOT',11,purple,'text-anchor="end" letter-spacing="1.5"')
    for x,label,value,col in [(26,'ENERGY / CONTRIBUTIONS',total,cyan),(350,'POWERED DAYS',active,green),(646,'PEAK DAILY ENERGY',best,purple)]:
        s+=t(x,83,label,10,muted,'letter-spacing="1"')+t(x,113,f'{value:,}',26,col,'font-weight="700"')
    s+=t(1174,84,'MISSION WINDOW',10,muted,'text-anchor="end"')+t(1174,109,days[0]['date']+' → '+days[-1]['date'],12,text,'text-anchor="end"')
    s+=f'<rect x="76" y="188" width="1048" height="162" rx="8" fill="{panel}" stroke="{edge}"/>'
    for row,name in [(1,'MON'),(3,'WED'),(5,'FRI')]:s+=t(63,y0+row*step+11,name,9,muted,'text-anchor="end"')
    targets=[]
    month=None
    for d in days:
        dt=date.fromisoformat(d['date'])
        offset=(dt-origin).days
        col,row=divmod(offset,7)
        x,y=x0+col*step,y0+row*step
        if dt.month!=month:
            if dt.day<=7 and col<cols-2:s+=t(x,180,dt.strftime('%b').upper(),9,muted)
            month=dt.month
        s+=f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{palette[d["level"]]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>'
        if d['count']:
            targets.append((x+7,y+7,d['level']))
            if d['level']>=3:s+=f'<circle cx="{x+7}" cy="{y+7}" r="2" fill="{text}" opacity=".65"/>'
    s+=t(98,374,'EACH TILE = ONE DAY  /  BRIGHTER = MORE CONTRIBUTIONS',10,muted)
    s+=t(929,374,'LOW',9,muted)
    for i,c in enumerate(palette):s+=f'<rect x="{958+i*21}" y="363" width="14" height="14" rx="3" fill="{c}"/>'
    s+=t(1099,374,'HIGH',9,muted,'text-anchor="end"')
    # Harvest stops and combat encounters share one timeline in each theme.
    chosen=targets[::max(1,len(targets)//14)][:14]
    if not chosen:chosen=[(x0+7,y0+7,0)]
    encounters=[215,610,1010]
    events=[{'kind':'harvest','x':x,'y':y} for x,y,level in chosen]
    events.extend({'kind':'combat','x':enemy_x-75,'enemy_x':enemy_x,'index':i}
                  for i,enemy_x in enumerate(encounters))
    events.sort(key=lambda e:e['x'])
    duration=24
    n=len(events)+2
    positions=['90 150']
    timestamps=[0]
    for i,event in enumerate(events):
        event['arrive']=(i+1)/n
        event['leave']=(i+1.65)/n
        positions.extend([f'{event["x"]} 150',f'{event["x"]} 150'])
        timestamps.extend([event['arrive'],event['leave']])
    positions.extend(['1110 150','90 150'])
    timestamps.extend([(len(events)+1)/n,1])

    def animate(attr,values,times,discrete=False,tag='animate',extra=''):
        if not (len(values)==len(times) and times[0]==0 and times[-1]==1
                and all(a<b for a,b in zip(times,times[1:]))):
            raise ValueError('Invalid combat animation timeline')
        mode=' calcMode="discrete"' if discrete else ''
        return (f'<{tag} attributeName="{attr}" values="{";".join(map(str,values))}" '
                f'keyTimes="{";".join(f"{v:.7f}" for v in times)}" '
                f'dur="{duration}s" repeatCount="indefinite"{mode} {extra}/>')

    s+=f'<g class="motion"><path d="M80 150H1120" stroke="{cyan}" stroke-opacity=".15" stroke-dasharray="3 8"/>'
    for event in events:
        x=event['x']
        a,b=event['arrive'],event['leave']
        if event['kind']=='harvest':
            y=event['y']
            s+='<g opacity="0">'+animate('opacity',[0,1,0,0],[0,a,b,1],True)
            s+=f'<path d="M{x} 163V{y}" stroke="{cyan}" stroke-width="2"/><path d="M{x-6} 163L{x-12} {y}H{x+12}L{x+6} 163Z" fill="url(#beam)"/><circle cx="{x}" cy="{y}" r="12" fill="none" stroke="{green}"/><path d="M{x-17} {y}h-6M{x+17} {y}h6M{x} {y-17}v-6M{x} {y+17}v6" stroke="{cyan}"/></g>'

    # Ship stops before every enemy; bullets are timed in world coordinates.
    s+='<g id="player-ship" transform="translate(90 150)">'
    s+=animate('transform',positions,timestamps,tag='animateTransform',extra='type="translate"')
    s+=f'''<path d="M-13 -8L-27 -4L-13 0" fill="{purple}" opacity=".7"><animate attributeName="opacity" values=".3;1;.3" dur=".3s" repeatCount="indefinite"/></path>
<path d="M17 0L-13 -11L-8 0L-13 11Z" fill="{text}" stroke="{cyan}" stroke-width="1.5"/><path d="M-5 -4H5V4H-5Z" fill="{cyan}"/></g>'''

    for event in (e for e in events if e['kind']=='combat'):
        index=event['index']+1
        enemy_x=event['enemy_x']
        fire=event['arrive']+.08/n
        hit=event['arrive']+.38/n
        end=min(hit+.55/duration,event['leave']-.015/n)
        if end>=event['leave']:
            raise ValueError('Explosion must finish before the ship leaves')
        s+=f'<g id="virus-{index}" data-hit-time="{hit*duration:.7f}" transform="translate({enemy_x} 150)" fill="{purple}" opacity=".85">'
        s+=animate('opacity',[.85,0,0],[0,hit,1],True)
        s+=f'<path d="M-9 -9h3v3h-3zm15 0h3v3H6zM-12 -3h24v9h-3v3H6V6H-6v3h-3V6h-3z"/><path d="M-6 0h3v3h-3zm9 0h3v3H3z" fill="{bg}"/></g>'
        # Projectile head reaches the exact enemy center at the visibility cutoff.
        s+=f'<g id="bullet-{index}" data-fire-time="{fire*duration:.7f}" data-hit-time="{hit*duration:.7f}" opacity="0">'
        s+=animate('opacity',[0,1,0,0],[0,fire,hit,1],True)
        s+='<g transform="translate(0 150)">'
        s+=animate('transform',[f'{event["x"]+24} 150',f'{event["x"]+24} 150',f'{enemy_x} 150',f'{enemy_x} 150'],[0,fire,hit,1],tag='animateTransform',extra='type="translate"')
        s+=f'<path d="M-16 0H0" stroke="{cyan}" stroke-width="3" stroke-linecap="round"/><circle r="3" fill="{text}"/></g></g>'
        # Impact flash, expanding shock wave and twelve drifting pixel fragments.
        s+=f'<g id="explosion-{index}" transform="translate({enemy_x} 150)" opacity="0">'
        s+=animate('opacity',[0,1,0,0],[0,hit,end,1],True)
        s+=f'<circle r="4" fill="none" stroke="{cyan}" stroke-width="2" opacity="1">'
        s+=animate('r',[4,4,31,31],[0,hit,end,1])
        s+=animate('opacity',[0,1,0,0],[0,hit,end,1])+'</circle>'
        s+=f'<circle r="9" fill="{text}" opacity="0">'+animate('opacity',[0,0,1,0,0],[0,hit,hit+.002,hit+.007,1])+'</circle>'
        for j,(dx,dy) in enumerate([(-31,-22),(-14,-30),(8,-34),(28,-22),(35,-3),(27,20),(10,31),(-13,29),(-33,17),(-38,-3),(1,-20),(4,20)]):
            col=[purple,cyan,green,text][j%4]
            s+=f'<g><rect x="-2" y="-2" width="{4 if j%3 else 5}" height="{4 if j%3 else 5}" fill="{col}"/>'
            s+=animate('transform',['0 0','0 0',f'{dx} {dy}',f'{dx} {dy}'],[0,hit,end,1],tag='animateTransform',extra='type="translate"')
            s+=animate('opacity',[0,1,0,0],[0,hit,end,1])+'</g>'
        s+='</g>'
    s+='</g>'
    s+=t(26,425,'MISSION: HARVEST CONTRIBUTION ENERGY',11,cyan,'letter-spacing="1"')+t(1174,425,'PUBLIC GITHUB DATA / DAILY SYNC',10,muted,'text-anchor="end"')
    s+=t(26,444,'Animated replay · contribution tiles keep their real values',9,muted)+'</svg>'
    return s

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--refresh',action='store_true')
    ap.add_argument('--html',type=Path)
    args=ap.parse_args()
    if args.html:
        days=read_calendar(args.html.read_text())
    elif args.refresh:
        request=urllib.request.Request('https://github.com/users/dhuyhoang1406/contributions',headers={'User-Agent':'dhuyhoang1406-profile'})
        with urllib.request.urlopen(request,timeout=30) as response:days=read_calendar(response.read().decode())
    else:
        days=json.loads(DATA.read_text())
    if args.html or args.refresh:
        DATA.write_text(json.dumps(days,indent=2)+'\n')
    for theme in ['dark','light']:
        (ROOT/f'assets/contribution-defender-{theme}.svg').write_text(render(days,theme))
    print(f'Built Contribution Defender from {len(days)} real calendar days.')

if __name__=='__main__':main()

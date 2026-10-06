from pathlib import Path
from html import escape


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
portrait_template = (OUT/'portrait-trace.svg.inc').read_text()

for mode in ['dark', 'light']:
    bg, panel, card, text, muted, edge, cyan, violet, green = ('#070C18','#0C1425','#111E32','#EAF2FF','#8C9FBC','#20334D','#22D3EE','#B09AFF','#34D399') if mode == 'dark' else ('#EDF3FC','#F8FAFF','#FFFFFF','#172B47','#546C89','#CDDCEC','#087D9D','#7951D0','#138467')
    theme_portrait = (OUT/'portrait-trace-light.svg.inc').read_text() if mode == 'light' else portrait_template
    portrait_ink = '#352657' if mode == 'light' else violet
    portrait_trace = theme_portrait.replace('{cyan}',cyan).replace('{violet}',portrait_ink)
    if mode == 'light':
        portrait_trace = portrait_trace.replace('stroke-width=".68"','stroke-width=".85"').replace('stroke-opacity=".92"','stroke-opacity="1"')
    def start(w,h,title):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Custom developer dashboard for dhuyhoang1406. Decorative animations do not represent live metrics.</desc>
<defs>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{cyan}"/><stop offset="1" stop-color="{violet}"/></linearGradient>
<radialGradient id="halo"><stop stop-color="{cyan}" stop-opacity=".15"/><stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{muted}" stroke-opacity=".07"/></pattern>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{cyan}" stop-opacity="0"/><stop offset="1" stop-color="{cyan}" stop-opacity=".13"/></linearGradient>
<style>text{{font-family:'SFMono-Regular',Consolas,'Liberation Mono',monospace}} .muted{{fill:{muted}}} .fg{{fill:{text}}} @media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}</style>
</defs><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{bg}" stroke="{edge}"/>
'''
    def label(x,y,value,size=13,color=None,extra=''):
        return f'<text x="{x}" y="{y}" fill="{color or text}" font-size="{size}" {extra}>{escape(value)}</text>'
    def box(x,y,w,h):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{panel}" stroke="{edge}"/>'
    def header(x,y,title,w):
        return label(x,y,title,12,cyan,'letter-spacing="1.5"')+f'<path d="M{x} {y+12}H{x+w}" stroke="{edge}"/>'
    s=start(1200,650,'dhuyhoang1406 | Developer command center')
    s+= '<rect x="2" y="48" width="1196" height="550" fill="url(#grid)"/>'
    s+=f'<path d="M18 48H1182" stroke="{edge}"/>'
    for i,col in enumerate(['#FB7185','#FBBF24','#34D399']):
        s+=f'<circle cx="{25+i*20}" cy="25" r="5" fill="{col}"/>'
    s+=label(91,30,'workspace / dhuyhoang1406',12,muted)
    s+=label(1172,30,'PROFILE.SYS   /   v2.0',12,cyan,'text-anchor="end"')
    # Left holographic identity panel.
    s+=box(24,70,340,550)+header(43,96,'01 / IDENTITY.MAP',302)
    # Plotter-style vector portrait. Source PNG is used only by the offline tracer.
    s+=f'''<defs>
<clipPath id="portrait-panel"><rect x="44" y="122" width="300" height="324" rx="6"/></clipPath>
<clipPath id="trace-reveal"><rect x="44" y="122" width="300" height="324"><animate attributeName="height" values="0;324;324;0" keyTimes="0;.22;.95;1" dur="14s" repeatCount="indefinite"/></rect></clipPath>
<clipPath id="trace-band"><rect x="44" y="122" width="300" height="24"><animate attributeName="y" values="440;122;122" keyTimes="0;.85;1" dur="7s" repeatCount="indefinite"/></rect></clipPath>
<filter id="vector-light"><feFlood flood-color="{cyan}"/><feComposite in2="SourceAlpha" operator="in"/></filter>
<g id="vector-portrait" fill="none" stroke-linecap="round">{portrait_trace}</g>
</defs>
<g clip-path="url(#portrait-panel)">
<rect x="44" y="122" width="300" height="324" fill="url(#grid)"/>
<ellipse cx="200" cy="280" rx="158" ry="166" fill="url(#halo)"/>
<path d="M60 183V143H110M281 143H331V183M60 391V429H110M281 429H331V391" fill="none" stroke="{edge}"/>
'''
    for i in range(7):
        y=169+i*36
        s+=f'<path d="M50 {y}h12M325 {y}h12" stroke="{cyan}" stroke-opacity=".35"/>'
        s+=label(338,y+3,format(i,'02X'),7,muted,'text-anchor="end"')
    s+=f'''<g clip-path="url(#trace-reveal)"><use href="#vector-portrait"/></g>
<g class="motion" clip-path="url(#trace-band)" opacity=".8"><use href="#vector-portrait" filter="url(#vector-light)"/><path d="M49 122H319" stroke="{cyan}" stroke-opacity=".35"><animateTransform attributeName="transform" type="translate" values="0 318;0 0;0 0" keyTimes="0;.85;1" dur="7s" repeatCount="indefinite"/></path></g>
<g class="motion"><path d="M319 163v41" stroke="{violet}" stroke-width="2"><animate attributeName="stroke-dasharray" values="2 7;5 4;2 7" dur="3s" repeatCount="indefinite"/></path></g>
<path d="M51 137v-8h16M321 129h16v8M51 427v8h16M321 435h16v-8" fill="none" stroke="{cyan}" stroke-width="1.3"/>
</g>'''
    s+=label(58,151,'VECTOR / 01',8,cyan,'letter-spacing="1"')
    s+=label(328,429,'TRACE.RENDER',8,cyan,'text-anchor="end" letter-spacing="1"')
    s+=label(194,470,'@dhuyhoang1406',18,text,'text-anchor="middle" font-weight="700"')
    s+=label(194,495,'GITHUB / DEVELOPER PROFILE',10,muted,'text-anchor="middle" letter-spacing="1.5"')
    s+=f'<path d="M43 518H345" stroke="{edge}"/>'
    s+=label(43,544,'IDENTITY',11,muted)+label(345,544,'PUBLIC REPOSITORIES',11,green,'text-anchor="end"')
    s+=label(43,573,'PORTFOLIO',11,muted)+label(345,573,'GITHUB PAGES ↗',11,cyan,'text-anchor="end"')
    s+=label(43,599,'EST. 2023',10,muted)+label(345,599,'UTC +07:00',10,muted,'text-anchor="end"')
    # Right terminal.
    s+=box(384,70,792,348)+header(406,96,'02 / TERMINAL.SESSION',748)
    s+=label(1153,96,'bash',11,muted,'text-anchor="end"')
    s+=label(407,139,'❯ whoami',15,green)
    # Character-by-character SVG typing, hold, then reverse-order deletion.
    intro_lines = [
        "Hi, I'm Dang Huy Hoang.",
        'About me',
        'I’m a full-stack developer working primarily with JavaScript',
        'and TypeScript. I build applications with React, Next.js,',
        'NestJS, and .NET 8, with a focus on REST APIs, real-time',
        'features, clean architecture, and automated CI. I’m also',
        'exploring AI-powered applications through personal projects.',
    ]
    intro_x, intro_y, cell, line_height = 407, 161, 9.6, 22
    letters = [(line_no, column, char) for line_no, line in enumerate(intro_lines)
               for column, char in enumerate(line)]
    start_delay, type_step, erase_step, hold = .6, .065, .025, 3.5
    typed_at = start_delay + len(letters)*type_step
    erase_start = typed_at + hold
    erased_at = erase_start + len(letters)*erase_step
    cycle = erased_at + 1.2
    s+='<style>.typing-static{display:none}@media(prefers-reduced-motion:reduce){.typing-animated{display:none}.typing-static{display:inline}}</style>'
    s+='<g class="typing-static">'
    for row,line in enumerate(intro_lines):
        s+=label(intro_x,intro_y+row*line_height,line,16,text if row==0 else (violet if row==1 else cyan))
    s+='</g><g id="typing-intro" class="typing-animated">'
    for index,(row,column,char) in enumerate(letters):
        appear = (start_delay+(index+1)*type_step)/cycle
        disappear = (erase_start+(len(letters)-index)*erase_step)/cycle
        s+=f'<text x="{intro_x+column*cell:.1f}" y="{intro_y+row*line_height}" font-size="16" fill="{text if row==0 else (violet if row==1 else cyan)}" xml:space="preserve" opacity="1">{escape(char)}<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{appear:.8f};{disappear:.8f};1" calcMode="discrete" dur="{cycle:.4f}s" repeatCount="indefinite"/></text>'
    positions=[f'{intro_x} {intro_y-17}']
    caret_times=[0]
    for index,(row,column,char) in enumerate(letters):
        positions.append(f'{intro_x+(column+1)*cell:.1f} {intro_y+row*line_height-17}')
        caret_times.append((start_delay+(index+1)*type_step)/cycle)
    for deletion,(row,column,char) in enumerate(reversed(letters)):
        positions.append(f'{intro_x+column*cell:.1f} {intro_y+row*line_height-17}')
        caret_times.append((erase_start+(deletion+1)*erase_step)/cycle)
    positions.append(positions[0])
    caret_times.append(1)
    s+=f'<g id="typing-caret" transform="translate({intro_x} {intro_y-17})"><animateTransform attributeName="transform" type="translate" values="{";".join(positions)}" keyTimes="{";".join(f"{v:.8f}" for v in caret_times)}" calcMode="discrete" dur="{cycle:.4f}s" repeatCount="indefinite"/><rect width="2" height="20" fill="{cyan}"><animate attributeName="opacity" values="1;0;1" calcMode="discrete" keyTimes="0;.5;1" dur=".9s" repeatCount="indefinite"/></rect></g></g>'
    s+=label(407,316,'❯ cat profile.json',15,green)
    for y,k,v in [(336,'github','github.com/dhuyhoang1406'),(359,'portfolio','dhuyhoang1406.github.io'),(382,'stack','React / NestJS / .NET 8')]:
        s+=label(420,y,k,14,violet)+label(531,y,':',14,muted)+label(552,y,v,14,text)
    s+=label(407,406,'❯ explore ./repositories',14,green)
    s+=f'<rect x="635" y="393" width="8" height="17" fill="{cyan}" class="motion"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>'
    # Core technologies supplied by the profile owner.
    s+=box(384,436,490,184)+header(405,464,'03 / CORE.STACK',448)
    for x,y,name,col in [(405,502,'TypeScript',cyan),(631,502,'JavaScript',violet),(405,541,'C# / .NET 8',green),(631,541,'React / Next.js',cyan),(405,580,'Node.js / NestJS',violet),(631,580,'PostgreSQL',green)]:
        s+=f'<rect x="{x}" y="{y-19}" width="204" height="29" rx="5" fill="{card}" stroke="{edge}"/><circle cx="{x+13}" cy="{y-5}" r="3" fill="{col}"/>'+label(x+26,y,name,13,text)
    s+=box(892,436,284,184)+header(913,464,'04 / BUILD.LOOP',241)
    for i,(name,col) in enumerate([('EXPLORE',cyan),('IMPLEMENT',violet),('ITERATE',green)]):
        y=500+i*39
        s+=f'<circle cx="923" cy="{y-4}" r="9" fill="{card}" stroke="{col}"/>'+label(923,y,str(i+1),10,col,'text-anchor="middle"')+label(945,y,name,12,text,'letter-spacing="1.5"')
        if i<2:s+=f'<path d="M923 {y+6}v18" stroke="{edge}"/>'
    s+=label(26,640,'DH / ENGINEERING WORKSPACE',10,muted,'letter-spacing="1"')+label(1174,640,'TECH STACK / ARCADE BELOW ↓',10,cyan,'text-anchor="end" letter-spacing="1"')
    s+='</svg>'
    (OUT/f'hero-{mode}.svg').write_text(s)
    p=start(1200,70,'Code. Explore. Build.')
    p+=f'<path d="M20 35H385M815 35H1180" stroke="{edge}"/>'
    p+=label(600,41,'CODE. EXPLORE. BUILD.',14,cyan,'text-anchor="middle" letter-spacing="3"')+'</svg>'
    (OUT/f'footer-{mode}.svg').write_text(p)

# The preview is generated by build-readme.py from the final README.

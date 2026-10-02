"""Keep the GitHub README and local preview aligned."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'README.md'
s=p.read_text()
a=s.index('### `01` /')
b=s.index('### `02` / GITHUB TELEMETRY')
def icons(ids,alt):
 return f'''<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i={ids}&amp;theme=light" />
  <img src="https://skillicons.dev/icons?i={ids}&amp;theme=dark" alt="{alt}" />
</picture>'''
groups = [
 ('LANGUAGES', 'js,ts,cs', 'JavaScript · TypeScript · C#'),
 ('FRONTEND', 'react,nextjs,redux,tailwind,html,css', 'React · Next.js · Redux Toolkit · Tailwind CSS · HTML5 · CSS3 · Responsive Design'),
 ('BACKEND', 'nodejs,nestjs,dotnet,prisma', 'Node.js · NestJS · ASP.NET Core (.NET 8) · RESTful APIs · JWT · Socket.IO · Prisma'),
 ('DATA', 'postgres,mysql,redis', 'PostgreSQL · PostGIS · SQL Server · MySQL · Redis · Neo4j'),
 ('ENGINEERING', 'git,github,docker,githubactions,postman,linux', 'Git/GitHub · Docker · Docker Compose · GitHub Actions · CI · Integration Testing · Postman · Linux'),
]
stack = '### `01` / TECH STACK\n\n<div align="center">\n'
for title, ids, technologies in groups:
 stack += f'  <p><b>{title}</b></p>\n' + icons(ids, technologies) + f'\n  <p><sub>{technologies}</sub></p>\n'
stack += '</div>\n\n<br />\n\n'
s=s[:a]+stack+s[b:]
marker='<p align="center"><a href="https://github.com/dhuyhoang1406?tab=overview">'
a=s.index(marker) if marker in s else s.index('### `03` / CONTRIBUTION DEFENDER')
b=s.index('<picture>',s.index('<br />',s.index('contribution-defender-dark.svg',a))) if '### `03` / CONTRIBUTION DEFENDER' in s else s.index('<picture>',a)
arcade='''### `03` / CONTRIBUTION DEFENDER

<p align="center"><b>One day. One energy tile. A year of missions.</b><br />
<sub>A spaceship harvests contribution energy and blasts pixel viruses — on autopilot.</sub></p>

<picture>
  <source media="(prefers-color-scheme: light)" srcset="./assets/contribution-defender-light.svg" />
  <img src="./assets/contribution-defender-dark.svg" width="100%" alt="Contribution Defender: animated spaceship harvesting energy from my GitHub contribution calendar" />
</picture>

<p align="center"><sub>Brighter tiles = more contributions · Animated replay · Calendar updates daily through GitHub Actions</sub></p>

<br />

'''
s=s[:a]+arcade+s[b:]
s=s.replace('<!-- Custom assets: python3 scripts/build-profile.py -->','<!-- Local assets: build-profile.py; contribution arcade: build-contribution-game.py -->')
p.write_text(s)
# Tiny renderer for this README's limited Markdown. Keep the embedded HTML unchanged.
body=re.sub(r'^### `(\d+)` / (.+)$',r'<h2>\1 / \2</h2>',s,flags=re.M)
body=body.replace('./assets/','assets/')
(ROOT/'preview.html').write_text('''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>dhuyhoang1406 · Profile preview</title><style>*{box-sizing:border-box}body{margin:0;background:#060b14;color:#eaf2ff;font:14px system-ui}main{max-width:1248px;margin:32px auto;padding:0 24px}nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;color:#8c9fbc}button{background:#111e32;color:#22d3ee;border:1px solid #20334d;padding:10px 18px;border-radius:8px;cursor:pointer}img{max-width:100%;vertical-align:middle}h2{font:13px monospace;letter-spacing:3px;margin:36px 0 20px;color:#8c9fbc}a{color:#22d3ee;text-decoration:none}sub{color:#8c9fbc}body.light{background:#fff;color:#172b47}body.light h2,body.light sub{color:#546c89}</style><main><nav><span>dhuyhoang1406 / profile preview</span><button id="toggle">Light / Dark</button></nav>'''+body+'''</main><script>document.getElementById('toggle').onclick=()=>{const light=document.body.classList.toggle('light');document.querySelectorAll('picture').forEach(p=>{const img=p.querySelector('img');if(!img.dataset.dark)img.dataset.dark=img.getAttribute('src');const source=p.querySelector('source');const target=light?source.getAttribute('srcset'):img.dataset.dark;p.querySelectorAll('source').forEach(s=>s.media='not all');img.src=target;});}</script></html>''')

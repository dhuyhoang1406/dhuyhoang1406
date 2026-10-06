"""Generate a luminance-preserving stippled bust portrait as SVG paths."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT=Path(__file__).resolve().parents[1]
# Frame the face and shoulders rather than shrinking the entire body.
photo=Image.open(ROOT/'assets/portrait.png').convert('RGBA')
photo=photo.crop((110,28,390,335)).resize((280,307),Image.Resampling.LANCZOS)
alpha=photo.getchannel('A')
# Keep bright skin/shirt bright and glasses/tie/hair dark. The previous version
# reversed this relationship and lost the separation between materials.
gray=ImageOps.grayscale(photo)
gray=ImageEnhance.Contrast(gray).enhance(1.12)
gray=gray.filter(ImageFilter.UnsharpMask(radius=1.0,percent=115,threshold=3))
# A white shirt remains textured rather than becoming a featureless solid slab.
gray=gray.point(lambda v: int(255*(.045+.75*(v/255)**.94)))
stipple=gray.convert('1',dither=Image.Dither.FLOYDSTEINBERG)
bits=stipple.load()
a=alpha.load()
width,height=photo.size
x0,y0=54,130
def trace_strokes(light_theme=False):
 segments=[]
 for y in range(height):
  x=0
  while x<width:
   ink = not bool(bits[x,y]) if light_theme else bool(bits[x,y])
   if a[x,y]<128 or not ink:
    x+=1
    continue
   begin=x
   while x<width and a[x,y]>=128 and (not bool(bits[x,y]) if light_theme else bool(bits[x,y])):
    x+=1
   segments.append(f'M{x0+begin} {y0+y}h{x-begin-.25:.2f}')
 return segments

for light_theme in (False,True):
 segments=trace_strokes(light_theme)
 # Violet light on a dark screen; complementary dark ink on a light screen.
 path=f'<path d="{"".join(segments)}" stroke="{{violet}}" stroke-opacity=".92" stroke-width=".68"/>'
 name='portrait-trace-light.svg.inc' if light_theme else 'portrait-trace.svg.inc'
 (ROOT/'assets'/name).write_text(path+'\n')
 print(f'Built {name}: {len(segments):,} vector strokes.')

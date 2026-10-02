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
segments=[]
for y in range(height):
 x=0
 while x<width:
  if a[x,y]<128 or not bits[x,y]:
   x+=1
   continue
  begin=x
  while x<width and a[x,y]>=128 and bits[x,y]:x+=1
  segments.append(f'M{x0+begin} {y0+y}h{x-begin-.25:.2f}')
# One material-independent violet ink, with luminance encoded by stroke density.
# Hair has sparse highlights; skin midtones; shirt dense lines; tie/glasses voids.
path=f'<path d="{"".join(segments)}" stroke="{{violet}}" stroke-opacity=".92" stroke-width=".68"/>'
(ROOT/'assets/portrait-trace.svg.inc').write_text(path+'\n')
print(f'Built a face-and-shoulders portrait with {len(segments):,} stippled vector strokes.')

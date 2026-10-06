# Profile assets

Put this README, `assets/`, `scripts/`, and `.github/` in the public
`dhuyhoang1406/dhuyhoang1406` profile repository.

Contribution Defender uses the public GitHub calendar. Cell color, daily count,
and summary totals come from real data. The spaceship, enemies and laser effects
are an animated replay rather than a playable game inside the README. Bullets
strike three viruses in sequence; each impact triggers a pixel explosion. All
three viruses respawn together when the 24-second animation starts again.

The workflow runs daily at 07:17 Vietnam time (00:17 UTC). After uploading the
files, open **Actions → Update Contribution Defender → Run workflow** for the
first update. Scheduled workflows run from the default branch. Enable GitHub
Actions if GitHub asks, and allow the workflow to write repository contents.

Regenerate the arcade locally with Python 3, without dependencies:

```sh
python3 scripts/build-contribution-game.py --refresh
```

To use the saved calendar without network access:

```sh
python3 scripts/build-contribution-game.py
```

The parser rejects incomplete calendar responses rather than replacing the
saved data with an empty or invented graph. If GitHub changes its calendar HTML,
the refresh will fail visibly and the previously committed SVGs remain available.

Regenerate the banner, then rebuild the local preview from the README:

```sh
python3 scripts/build-profile.py
python3 scripts/build-readme.py
```

Open `preview.html` in a browser. Its Light / Dark button switches all images.
Tech stack icons are served by [Skill Icons](https://skillicons.dev/).
Stats and streak cards use external services; their availability is separate
from the locally stored banner and contribution arcade.

The identity panel is a vector portrait made from approximately 11,000 short SVG
strokes. The hero contains no embedded photo. `assets/portrait.png` is only the
source for the offline tracer. To retrace a new source image, install Pillow and run:

```sh
python3 scripts/trace-portrait.py
python3 scripts/build-profile.py
```

The traced path templates are stored in `assets/portrait-trace.svg.inc`
and `assets/portrait-trace-light.svg.inc`, so normal
banner regeneration does not need Pillow. The face-and-shoulders crop preserves positive luminance: sparse hair highlights,
mid-density skin strokes, dense white-shirt strokes and dark glasses/tie.
A plotter reveal and luminous scan band
animate the vector strokes inside the SVG.

The terminal introduction types the greeting, About me heading and biography,
pauses, erases in reverse order,
and repeats. Edit `intro_lines` in `scripts/build-profile.py` to change the text,
then regenerate the banner. The cursor follows the characters in the SVG,
and reduced-motion viewers see a static introduction.

The light theme uses complementary dark-ink stippling on white: hair, glasses
and the tie are dense; skin is medium; the white shirt has sparse marks.
The dark theme uses luminous strokes with the original brightness ordering.

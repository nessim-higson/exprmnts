# 002 · Text Nav, Rebuilt

The Firstborn '03 homepage navigation rebuilt in modern vanilla JS — no libraries, one file.
Where the original faked its motion with eased tweens (`textNavAni`/`easeIn`), this rebuild runs a
real physics integrator, so it's the nav as *remembered*, not as shipped. See `../firstborn/` for
the archived original running in Ruffle.

## What's in it
- **109 genuine thumbnails** mined straight out of the archived `portfolio.swf`
  (DefineBits + shared JPEGTables reconstruction — no decompiler needed). NBC Uni, The 4400,
  Madonna, FCUK, Loreal, Yigal… the real 2003–2006 portfolio.
- **The type engine (v3)** — a straight port of the decompiled 2003 ActionScript (see
  `original-as2-disassembly.txt`, extracted with a hand-rolled AS2 bytecode disassembler). The
  original's "physics" is two primitives running at a fixed 60fps:

  ```actionscript
  scaleEase: diff = goal - _xscale;  |diff|>1 ? _xscale += diff/speed : snap   // speed = 3
  easeIn(prop, goal, speed): same, for any property
  ```

  plus structure: **nested scaling containers** (main ⊃ sub ⊃ subsub) on a ×0.75-per-level ladder
  with newcomers at 133 (=1/0.75, so the newest level nets out full-size while ancestors recede as
  one organism); **layout re-chained every frame from live scales** (the column breathes);
  **threshold choreography** (snap makes eased values *arrive*, and arrival triggers the next
  phase — body copy scale-pops 0→100 at speed/2 only after the nav settles); sub-subs fly in from
  x=400; logo 66.5 → 29.7; selected 100 / siblings 75 / leaves 133; selection recolors instantly
  (grey↔dark). All constants verbatim: navSpace=8, mLeading=8, mainOffset=-14, horOffset=22.

  Placement rules from navRun's per-frame section: the stack top tracks the logo's live bottom
  edge and its x eases toward the logo's shrinking right edge (the column rides the logo); main
  items right-align by easing x to −width×scale and chain follow-the-leader with easing (the
  ripple runs down the stack); the child column hangs off the selected ghost's right edge −
  horOffset, tracked every frame; the sub only cascades once the ghost ARRIVES at mainOffset —
  reorganize, then reveal; closing branches scale to 0 and unload (subRetract).
- **Data-driven** — the entire menu is one `TREE` object at the top of the file (labels, copy,
  children, field layouts); the feel lives in a `CFG` block (scales, ratios, stagger, ghost alpha,
  drift). Edit either without touching the engine. Copy transcribed from the 2003 original where
  recoverable; items marked [edit] are stand-ins.
- **The nav drives the field** — each portfolio sort re-homes the tiles and physics carries them
  there: scatter (BY THUMBNAIL), grid (BY CLIENT / BY CHRONOLOGY), clusters (BY PROJECT TYPE),
  bands (BY DELIVERY MEDIA).
- **Spring vs Tween '03 toggle** — A/B the modern spring integrator (velocity, stiffness, damping,
  mouse repulsion) against the archival pure-ease feel. Sliders for stiffness / damping / repel
  radius. Static-by-default: tiles spawn settled; motion is opt-in.

## Notes
- Canvas 2D, DPR-aware; tiles brighten + scale on cursor proximity (as in the original).
- Deterministic seeded PRNG so the scatter is stable.
- `assets/` tile ids are the SWF character ids (`t012.jpg` = character 12).

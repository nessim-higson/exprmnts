# 002 · Text Nav, Rebuilt

The Firstborn '03 homepage navigation rebuilt in modern vanilla JS — no libraries, one file.
Where the original faked its motion with eased tweens (`textNavAni`/`easeIn`), this rebuild runs a
real physics integrator, so it's the nav as *remembered*, not as shipped. See `../firstborn/` for
the archived original running in Ruffle.

## What's in it
- **109 genuine thumbnails** mined straight out of the archived `portfolio.swf`
  (DefineBits + shared JPEGTables reconstruction — no decompiler needed). NBC Uni, The 4400,
  Madonna, FCUK, Loreal, Yigal… the real 2003–2006 portfolio.
- **The type engine (v2)** — rebuilt after driving the original in Ruffle and mapping its grammar:
  one living hierarchy where children splice inline below their parent, later siblings get pushed
  down, the newest level always arrives biggest + brightest, every older generation scales down and
  dims ("type shifts back, new type cascades forward"), selected items ghost (enlarge + fade) as
  their children take focus, leaves zoom in place, and body copy fades in lazily after the nav
  settles. The whole block drifts up-left as depth grows, like a camera pulling back.
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

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

## The recovered content (v4)
- **Every copy block on the 2003 site, decoded from the binary** — I wrote a DefineText/DefineFont
  glyph-table decoder; static Flash text stores glyph indices, the font's code table maps them back
  to characters. 44 blocks: section intros, THE BASICS process steps, case studies (Redken, Madonna,
  Federated, Calvin Klein), the year-by-year HISTORY entries, contact details — all verbatim, all at
  their original stage coordinates (cX/cY from the decompiled `initData`).
- **The founders** — Michael Ferdman & Vas Sloutchevsky, with their real bios, and their silhouettes
  extracted as vectors (DefineShape → SVG converter) from `principalAni`: the pair appears at
  (69,315) scaling to 65 when WHO WE ARE opens, to 100 on PRINCIPALS, and each founder dims the
  other when selected (`addPrincipals` / `scalePrincipals` / `morphPrincipals`, verbatim).
- **HISTORY year-chips** — 1997–2002 chip list with the real annual entries, selected chip red
  (`startTextNav`'s chip behavior, simplified).
- **FIRSTBORN IS 5! runs red** through its whole subtree (`colorSelec`), incl. the GOODIE BAG.
- More mined vectors in `assets/`: sil-pointing, sil-phone, sil-plane (the tiny paper-plane man).

## v5 — the reshuffle + line-accurate everything
- **Sequenced branch switching** (the original's `aniMode` chain, now ported): switching branches
  runs retract → tuck → slide-out → cascade — the open sub column scales to zero, the old ghost
  tucks back into the stack, the new ghost slides out, and only then does the new column cascade.
  Clicking mid-sequence retargets it. This is the "shuffling and reshuffling" of the original.
- **Line-accurate copy**: every copy block renders line-by-line at its decoded x/y/size from the
  binary — the original's two-column layouts (lead-in insets, rags, alignments) reproduce
  automatically.
- **The crowd**: WHO WE ARE shows a group scene composed from the extracted silhouette cast
  (the original's exact crowd arrangement lives partly in DefineMorphShape targets — 3 shapes
  still unparsed; composition approximates the archived scene). PRINCIPALS isolates the pair.
- **Stage furniture**: the scaler box, top hairlines, and left dashes.

## v7 — the real fonts, the real pair
- **The embedded fonts, rebuilt as webfonts** — a SWF-glyph→TTF converter (fontTools) turns the
  binary's own outlines into `fb-nav.ttf` (Helvetica 65 Medium uppercase subset — the nav labels),
  `fb-body.ttf` (Helvetica 65 Medium — all copy; advances derived per-glyph from usage), and
  `fb-roman.ttf` (Helvetica 55 Roman). The letterforms are literally the 2003 cuts.
- **The founders' morph, verbatim** — walking `principalAni`'s timeline frame by frame gave the
  exact choreography: select Michael and he grows to ×1.75 at (50.9,−30.6) while Vas shrinks to
  nothing, and vice versa (frames 1–23 / 47–67). The invented crowd is gone — the ~11-figure group
  scene turns out to be the 2007 site's; the 2003 binary contains only the pair. Correctness > more.
- **HISTORY chips** nudge apart around the selection, per `startTextNav`.

## v6 — true coordinates (no more approximations)
The rebuild now runs entirely on numbers read from the binary:
- **Stage 800×650 @60fps**, showAll-scaled and centered; the nav sprite at its real (105,60).
- **Every menu item is its real `sizer` box** — exact width per item (WHO WE ARE 174.9,
  OUR PORTFOLIO 207.0, ENVISION 122.1…), 20px tall, label at 28px inset at the decoded
  per-symbol offset. The chain math now reproduces the original's spacing to the pixel
  (23px sibling pitch, 28px at the selected — emergent, not tuned).
- **The real vector logotype** (DefineShape 11 → SVG), 389.9×45, in place of HTML text.
- Furniture at stage coordinates (scaler 11,11; hairlines; dashes).

Remaining gaps to full 1:1: the embedded fonts as a webfont (glyph outlines are extractable),
the morph-shape crowd figures, and the content chip/thumb module animations.

## Notes
- Canvas 2D, DPR-aware; tiles brighten + scale on cursor proximity (as in the original).
- Deterministic seeded PRNG so the scatter is stable.
- `assets/` tile ids are the SWF character ids (`t012.jpg` = character 12).

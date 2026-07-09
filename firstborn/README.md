# Firstborn — Flash-era text navigation (archive)

Reference teardown of the homepage navigation from **firstbornmultimedia.com**, the NYC Flash
agency (Zeh Fernando era). Pulled from the Internet Archive Wayback Machine and run in-browser
via a self-hosted [Ruffle](https://ruffle.rs) build so no Flash plug-in is needed.

Lives in the exprmnts playground at `/firstborn/`.

## Files
| File | Source capture | Notes |
|------|----------------|-------|
| `swf/firstborn-2003.swf` | `20030406122526/…/swf/main.swf` | AS2 · `buildMainNav` / `easeIn` |
| `swf/firstborn-2007.swf` | `20070302091151/…/swf/main.swf` | AS2 · fullest text-nav build (828 KB) |
| `swf/firstborn-2010.swf` | `20100103103748/…/main.swf` | AS3 · fb7, elastic/bounce tween engine |
| `swf/firstborn-2004-loader.swf` | `20041014180627/…/swf/base.swf` | preloader only (kept for reference) |
| `swf/portfolio.swf` | `20060526100219/…/swf/portfolio.swf` | "2003 PORTFOLIO BOOK" — the child SWF the 2003 build loads to draw the nav + thumbnail field. **Required** for 2003 to render. |

## Finding — "text nav built on physics"
Decompiled strings show the nav is **text-based and motion-driven**, but the motion is
**eased tweening**, not a spring/mass/drag physics simulation:

- 2003–2007 (AS2): `buildMainNav`, `buildSubNav`, `textNavAni`, `easeIn` — keyframed easing.
- 2010 (fb7, AS3): a `nectere` tween engine with `outElastic` / `outBounce` easing — springy feel,
  scripted underneath. Classes are `Menu` / `MenuItem` / `MenuLine` / `NumberNav` / `ArrowNav`.

No `velocity` / `gravity` / `friction` / constraint code is present in these homepage binaries.
If the physics nav in question was a separate lab/experiment piece, dig it out of the archive
separately.

## What actually renders
- **2003** — renders fully: the text menu (WHO WE ARE / WHAT WE DO / OUR PORTFOLIO / CONTACT US)
  over a loosely scattered field of project thumbnails. The thumbnail field is the "physics" read —
  a drifting particle-like layout, not a grid. This is the one to show.
- **2007 (fb6)** — partial; pulls further child SWFs / server XML that weren't archived.
- **2010 (fb7)** — shell only; its nav data came over Flash Remoting, which is gone.

## Caveat
The archived `.swf` files loaded dynamic content (news, project pages, per-project SWFs) from live
backends that are gone. The 2003 build works because its child `portfolio.swf` bakes the project list
in; the later builds fetch data at runtime, so they show a blank/partial stage.

# exprmnts

A personal playground — inspiration, teardowns, and things I'm playing with. Public, no login.

Deployed as a plain static site on **Cloudflare Pages** (no worker, no gate).

- **Local:** `~/CLAUDE/projects/exprmnts/`
- **Live:** `https://exprmnts.pages.dev`
- **Deploy:** `./deploy.sh` (needs a Cloudflare API token in the env or
  `~/.config/cloudflare/experiments.env`, falling back to `aff.env`)
- Deliberately separate from client work (AFF, Arena).

## Structure
```
index.html    playground index
firstborn/    001 — Firstborn Flash-era text nav, run in-browser via Ruffle
text-nav/     002 — the '03 nav rebuilt in vanilla JS with real spring physics
deploy.sh     Cloudflare Pages deploy (static)
```

Add a new thing: drop it in its own top-level folder and add a row to `index.html`.

## Contents
- **001 · firstborn/** — Firstborn (firstbornmultimedia.com) archived homepage text navigation from
  the Wayback Machine, running via self-hosted Ruffle. See `firstborn/README.md`.
- **002 · text-nav/** — the same nav rebuilt modern: vanilla JS, real spring integrator, 109
  thumbnails mined from `portfolio.swf`, the portfolio sorts re-layout the field, Spring vs
  Tween '03 toggle. See `text-nav/README.md`.

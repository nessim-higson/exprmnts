# exprmnts — STATE
_Last updated: 2026-11-18_

## What
Public personal playground — inspiration, teardowns, tinkering. Deliberately separate from
client work (AFF, Arena). No gate, no login. Each experiment is a top-level folder plus a
row in `index.html`.

## Where
- Local: `~/CLAUDE/projects/exprmnts/` (repo github.com/nessim-higson/exprmnts, branch `main`)
- Hosting: Cloudflare Pages project `exprmnts` → exprmnts.pages.dev; deploy via `./deploy.sh` (wrangler OAuth)
- Public URL: https://lab.iamalwayshungry.com/exprmnts/ — mounted via the gate worker's PUBLIC_ROUTES proxy
- Because of the path mount, ALL internal links must be RELATIVE (`../firstborn/`, never `/firstborn/`)

## Status
LIVE. Contents:
- **001 `firstborn/`** — archived Firstborn Flash text-nav (2003/2007/2010) via self-hosted Ruffle
- **002 `text-nav/`** — the '03 nav rebuilt 1:1 in vanilla JS from the decompiled AS2; 109 mined
  thumbnails; 5 reusable SWF-archaeology Python tools in `text-nav/tools/`
- **`compare/`** — 001 vs 002 side by side, driven in parallel
- **003 `nav-variants/`** — the grammar distilled into a clean engine: A·PAPER / B·SPINE / C·RAIL
- **004 `pretext/`** — canvas typesetting instrument (author poses, engine owns transitions)
- **005 `text-nav-2027/`** — the '03 grammar redesigned for 2027: Roboto Flex variable ladder, springs, the TREE decoded from the swf
- **005·HN `text-nav-2027-helvetica/`** — Swiss paper version in Helvetica Neue, real cuts only (500/400), catalogue numbers, grid on G
- **005·KO `text-nav-2027-knockout/`** — the nav cut out of a thumbnail wall on canvas; weight still from a stroke (the HN study dropped that)
- **`studies/`** — public studies hub = `grep -v localOnly` copy of `prototypes/hub/index.html`;
  also the target of the lab's top-level `/studies` mount, so one refresh updates both paths

## Open threads
- Branch `005-text-nav-2027` (pushed, not merged, not deployed) holds the three 005 studies and the
  hub refresh (+2 rows: Compression, tomato.three). Merge to `main` and `./deploy.sh` to take them live
- The IAAH-specific follow-ons (L Index onward) live in the gated `iaah-living-site`, not here
- Studies hub goes stale vs `prototypes/hub/index.html`; refresh = grep copy + deploy
  (never copy unstripped — localOnly rows are client/confidential)
- pretext v2 candidates: splice, ripple lag on chains, multi-select, undo

## Sessions
- IAAH — Lab · 2026-07-09 · repo created, gate stripped (public by decree), Pages deploy, 001 Firstborn Ruffle
- IAAH — Lab · 2026-07-10 · 002 text-nav v5–v9 (binary-true rebuild), compare view, relative-links fix, lab mount
- IAAH — Lab · 2026-07-10 · 003 nav-variants + 004 pretext (the tool)
- IAAH — Lab · 2026-07-17 · studies hub mounted at /studies + INDEX row; links open in new tabs (last commit dd91866)
- IAAH — Lab · 2026-07-31 · hub refresh into studies/index.html (left uncommitted)
- IAAH — Lab · 2026-11-16/17 · 005 Text Nav 2027, 005 Helvetica (real cuts), 005 Knockout; STATE and hub refresh committed on the branch

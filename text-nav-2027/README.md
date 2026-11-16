# 005 · Text Nav, 2027

The Firstborn 2003 homepage navigation (001 / 002), redesigned as if it shipped in 2027.
It's one HTML file plus `tree.js`, with no build step and no libraries.

## Kept from '03
- **Right-aligned stack, children cascading to the right**: each new column hangs off the edge of the column before it.
- **The ladder**: older levels shrink back together as one unit while the newest level stays full size.
- **Wait for arrival**: the old branch folds away first, then the picked item settles, then its children cascade in, then the copy appears.
- **The portfolio field**: the 109 thumbnails pulled from `portfolio.swf`, which each sort rearranges.
- **The copy**: every word is the decoded 2003 text (`tree.js`, taken from `../text-nav/`).

## New for 2027
- **The ladder also changes the type.** Ancestor columns shrink and also get narrower and lighter (Roboto Flex `wdth` and `wght`). Hovering widens a word.
- **Real springs** with velocity and follow-through. The *Physics* panel has an **Ease · 2003** switch that brings back the original engine (`x += (goal − x) / 3` at 60fps, snapping within a pixel) for a side-by-side feel.
- **A camera that follows the newest column**, so deep paths and phones still work.
- **Deep links** (`#/how-we-do-it/case-studies/madonna`), back and forward buttons, and a breadcrumb path at the bottom left.
- **Keyboard**: arrow keys move around the menu, Enter opens, Esc goes back one level. Reduced-motion settings are respected.
- **The field has depth**: on the index the thumbnails float in grey at different depths and shift slightly with the pointer. Opening the portfolio brings them forward in colour, sorted, and they grow under the cursor.
- Light and dark themes, plus a subtle grain texture.

## Notes
- The sort groups (project type, delivery media) are illustrative. No per-project details survived in the archive, so tiles are dealt into groups the same way the 2003 build did.
- `TN.advance(seconds)` in the console steps the simulation by hand. It's useful when the tab is in the background and the animation is throttled.

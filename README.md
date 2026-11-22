# The World Today — Sunday, 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Alim-14-code/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Alim-14-code/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image that sums up the world's news of Sunday 22 November 2026:
32 stories across 6 regions, every one dated that day.

## What's on the page

- Masthead: 32 stories, 6 regions, all dated Sunday 22 November 2026
- Six-number strip: 0 COP31 deals agreed, 2 US Patriot radars Iran says
  it hit, 16 dead in Manipur, 80 drones downed over Leningrad, 129 bodies
  recovered in Gaza, 5,700 Hong Kong voters
- Coloured region bar with true counts: Europe 9, Africa 7,
  Asia-Pacific 5, Americas 4, Middle East 4, World 3
- Three illustrated heroes: the FBI NCIC breach probe, Iran's Patriot
  radar claim in Bahrain, the burning Russian cargo ship Sparta II
- Ten illustrated secondaries (stories 4–13) in a 5-column picture grid
- World map with numbered pins matching story numbers 1–13
- "Also on Sunday 22 November" — 19 more stories, to 32 in all
- DATE CHECK box written as proof: wire-read cutoff, stories left out as
  other days' news, and items not yet happened at draw time
- Sources footer naming an outlet beside every story

## How it is built

`render.py` (Pillow, run locally) draws `entry.png` — all art is
procedural, drawn in code. `main.py` is a standard-library-only program
that copies `entry.png` into the output directory; it runs the same way
twice, byte for byte.

```text
python3 render.py            # draws entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies it to out/entry.png
```

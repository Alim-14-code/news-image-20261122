# THE WORLD TODAY — Sunday, 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/Alim-14-code/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/Alim-14-code/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page newspaper front page for Sunday 22 November 2026: **36 stories across
5 regions**, drawn as a dense broadsheet — masthead with story and region counts,
giant date line, a six-number strip (0 COP31 deals agreed · 400+ drones fired at
Ukraine · 2 US radars Iran says it hit · 16 Manipur liquor dead · 129 Gaza bodies
recovered · 5,700 Hong Kong voters), a coloured region bar, three illustrated
heroes (COP31 deal close, Ukraine's 400-drone barrage, the burning Sparta II),
ten illustrated secondaries, a "BY THE CLOCK" UTC timeline, a world map with
numbered pins matching every story, an ALSO ON list to 36 stories, and a DATE
CHECK box proving what the wires were read to (08:00 UTC) and what was deliberately
left out (FBI NCIC hack, first reported 20 Nov; Peru quake; Nigeria boat; and more).

## How it works

- `render.py` — the renderer (Pillow). Draws every panel procedurally: conference
  hall, night skyline under drone trails, burning tanker, radar domes, hospital
  ward, ballot box, race car, and the rest. Run it to regenerate `entry.png`
  (1024×1024, byte-identical on repeat runs).
- `main.py` — the entry point. Standard library only: it copies `entry.png` into
  the grader's output directory. It never removes the output directory itself,
  only its contents.
- `entry.png` — the finished front page.

## Run

```sh
python3 render.py   # writes entry.png
python3 main.py     # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

## Sources

BBC, Reuters, CNN, AP, ANI, Al Jazeera, Xinhua, HK Govt, Finland MoD, Ukraine Air
Force. Every story is numbered and sourced on the page; the DATE CHECK box lists
the wire-read cutoff and every story left out on purpose.

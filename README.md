# The World Today — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Alim-14-code/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Alim-14-code/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page newspaper front page for Sunday, 22 November 2026. Every story
on the page was first reported, or had a genuine development, on that day —
the DATE CHECK box at the bottom lists what was deliberately left out and
why (including Russia's 400-drone barrage of 19–20 November: tonight's
barrage was 186, not 400).

## Layout

- Masthead + sub-headline, six-number strip, region bar
- Three illustrated heroes: COP31 deal close in Antalya, Ukraine's
  186-drone night, the tanker Sparta II still burning off Finland
- BY THE CLOCK strip (WIB), ten illustrated secondaries with
  ONGOING / REPORTED / CLAIM / FORECAST tags
- World map with 13 numbered pins, ALSO ON (14–25), DATE CHECK, sources

## How it is built

`render.py` draws the whole page procedurally with Pillow and writes
`entry.png` (1024×1024). `main.py` is the entry program: standard library
only, it copies `entry.png` to the output directory. Run locally:

```sh
python3 render.py   # writes entry.png
python3 main.py     # writes output/entry.png
```

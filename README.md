# The World Today — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Alim-14-code/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Alim-14-code/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the [make.fun news-image bounty for 22 November 2026](https://make.fun/bounty/news-image-20261122) ($100, top 50 share the pot).

One page that sums up Sunday, 22 November 2026: the FBI investigating a
breach of its own crime database, Iran claiming a missile-and-drone strike
on two US Patriot radars in Bahrain, and the sanctioned Russian cargo ship
Sparta II still burning in the Baltic — plus a six-number strip, ten more
stories from the day, and a world map of where it all happened. Every
story was first reported on 22 November 2026.

## How it works

- `render.py` draws the front page with Pillow on the author's machine and
  writes `entry.png` (1024×1024, ~110 KB). It is the artwork program and
  stays in the repo.
- `main.py` is the entry program: standard library only, it copies
  `entry.png` to `MAKEFUN_OUTPUT_DIR` (default `/output`). The grader runs
  with no third-party packages installed, so the entrypoint ships no
  Pillow import at all.
- `entry.png` is the finished front page, byte-identical across runs.

## Verify locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`out/entry.png` is byte-identical to `entry.png` in this repo.

<sub>Entered on [make.fun](https://make.fun/?ref=e6d1qmmj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

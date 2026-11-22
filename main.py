#!/usr/bin/env python3
"""Entrypoint for news-image-20261122 (stdlib only).

Copies the pre-rendered front page (entry.png, drawn by render.py with
Pillow on the author's machine) to the grader's output directory.
No third-party imports, no network, deterministic: the same bytes out
on every run.
"""
import os
import shutil
import sys


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard: refuse to report success if the copy came out short.
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

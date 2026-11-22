#!/usr/bin/env python3
"""Entry point for THE WORLD TODAY — news-image-20261122 (round 3).

Standard-library only. Copies the pre-rendered entry.png (produced by
render.py with Pillow at build time) into the grader's output directory.

Never removes the output directory itself: /output is a bind mount on the
grader, so only its contents are cleared.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    # Clear only the CONTENTS of the output directory, never the dir itself.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

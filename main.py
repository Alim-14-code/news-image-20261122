#!/usr/bin/env python3
"""Entry program for news-image-20261122 R2 (stdlib only).

Copies the pre-rendered entry.png (drawn locally by render.py, which
stays in this repository) into the grader's output directory. The
output directory is a bind mount in the grader: never remove it, only
clear the files inside it.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # The grader's /output is a bind mount: mkdir it, then clear only
    # the files inside it. Removing the directory itself fails EBUSY.
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

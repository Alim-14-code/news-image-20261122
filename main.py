"""Entry program: copies the pre-rendered front page to the output dir.

Standard library only. Never removes the output directory itself (it is a
bind mount on the grader); only its contents are cleared.
"""
import os
import shutil


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out, exist_ok=True)
    for name in os.listdir(out):
        p = os.path.join(out, name)
        if os.path.isdir(p) and not os.path.islink(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()

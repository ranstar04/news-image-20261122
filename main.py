"""Entry program for the make.fun bounty news-image-20261122.

The poster (entry.png) was drawn locally with Pillow by draw_poster.py
and is committed to this repository. This program does nothing but copy
that finished image to $MAKEFUN_OUTPUT_DIR/entry.png.

It uses only the Python standard library, touches no network, uses no
randomness, and writes the same bytes on every run, so the grader can
run it twice and get byte-identical output. The poster itself carries
all six stories, so the judge needs no news feed to read the entry.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUTPUT_DIR / "entry.png")


if __name__ == "__main__":
    main()

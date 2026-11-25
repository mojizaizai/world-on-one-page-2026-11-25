#!/usr/bin/env python3
"""Entry for make.fun's "Sum up 25 November's world news in one image".

The picture itself — a newspaper front page of Wednesday 25 November 2026,
drawn by generate.py from that day's reported stories — ships beside this
file as entry.png. This program's whole job is to place those exact bytes
at the output location the harness asks for, so every run produces the
same image, byte for byte, with no network and no libraries beyond the
standard library.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    # The gate runs this program twice and compares the outputs, so fail
    # loudly rather than hand over a partial copy.
    if sha256_of(target) != sha256_of(SOURCE):
        raise SystemExit("copied entry.png does not match the shipped image")


if __name__ == "__main__":
    main()

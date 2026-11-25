#!/usr/bin/env python3
"""Entry point for the news-image-20261125 make.fun entry.

Copies the committed entry.png (which sits next to this file) into the
output directory named by the MAKEFUN_OUTPUT_DIR environment variable
(default "out"), creating that directory when needed.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def verify_copy(source, dest):
    """Fail loudly unless dest is a byte-size match with a PNG signature."""
    src_size = os.path.getsize(source)
    dst_size = os.path.getsize(dest)
    if dst_size != src_size:
        raise SystemExit(
            f"verification failed: size mismatch ({dst_size} != {src_size})"
        )
    with open(dest, "rb") as fh:
        header = fh.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        raise SystemExit("verification failed: output is not a PNG file")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    verify_copy(SOURCE, dest)
    print("copied", SOURCE, "->", dest)


if __name__ == "__main__":
    main()

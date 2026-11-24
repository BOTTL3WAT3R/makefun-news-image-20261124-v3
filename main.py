#!/usr/bin/env python3
"""make.fun entry: news-image-20261124.

Writes one image that sums up the world's news of Tuesday 24 November
2026 to the output directory as entry.png. The poster is committed in
this repository as poster.png (drawn at build time by
tools/make_poster.py); this program is a standard-library-only copier,
so every run writes exactly the same bytes.

Usage:
    python3 main.py            copy poster.png to <output>/entry.png
    python3 main.py --check    validate the poster and the copy, write nothing

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
"""

import argparse
import binascii
import hashlib
import os
import shutil
import struct
import sys
import tempfile
from pathlib import Path

POSTER_NAME = "poster.png"
ENTRY_NAME = "entry.png"
MAX_BYTES = 1_048_576  # 1 MiB gate
MAX_DIM = 1024  # 1024 x 1024 gate
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def poster_path() -> Path:
    return Path(__file__).resolve().parent / POSTER_NAME


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Read (width, height) from the IHDR chunk of a PNG byte string."""
    if data[:8] != PNG_MAGIC:
        raise ValueError("poster is not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("poster PNG has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate_chunks(data: bytes) -> None:
    """Walk every PNG chunk, verifying each stored CRC, up to IEND.

    The bounty gate only accepts a whole image: every chunk present
    with its checksum correct and the data its header describes.
    """
    pos = 8
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("poster PNG ends inside a chunk header")
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        ctype = data[pos + 4 : pos + 8]
        end = pos + 8 + length
        if end + 4 > len(data):
            raise ValueError(f"poster PNG ends inside chunk {ctype!r}")
        (stored_crc,) = struct.unpack(">I", data[end : end + 4])
        actual_crc = binascii.crc32(data[pos + 4 : end]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise ValueError(f"poster PNG chunk {ctype!r} has a bad CRC")
        pos = end + 4
        if ctype == b"IEND":
            seen_iend = True
            break
    if not seen_iend:
        raise ValueError("poster PNG has no IEND chunk")


def validate_poster(data: bytes) -> tuple[int, int]:
    if len(data) > MAX_BYTES:
        raise ValueError(f"poster is {len(data)} bytes, over the 1 MiB gate")
    width, height = png_dimensions(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"poster is {width}x{height}, over the 1024x1024 gate")
    validate_chunks(data)
    return width, height


def copy_poster(dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / ENTRY_NAME
    shutil.copyfile(poster_path(), dest)
    return dest


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_check() -> int:
    poster = poster_path()
    if not poster.is_file():
        print(f"check FAILED: {POSTER_NAME} missing next to main.py", file=sys.stderr)
        return 1
    data = poster.read_bytes()
    try:
        width, height = validate_poster(data)
    except ValueError as exc:
        print(f"check FAILED: {exc}", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        written = copy_poster(Path(tmp))
        if sha256_of(written) != hashlib.sha256(data).hexdigest():
            print("check FAILED: copied bytes differ from the poster", file=sys.stderr)
            return 1
    print(f"check OK: {POSTER_NAME} is a {width}x{height} PNG of {len(data)} bytes")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the poster and the copy without writing an entry",
    )
    args = parser.parse_args(argv)
    if args.check:
        return run_check()
    dest = copy_poster(output_dir())
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

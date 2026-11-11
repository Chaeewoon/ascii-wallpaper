"""
main.py
Command line entry point.

Usage:
    python main.py <image> [-w WIDTH] [-cr RATIO] [--invert] [-o out.txt]

Needs: pip install pillow
"""

import argparse
import sys

from config import DEFAULT_RAMP, DEFAULT_COLS, DEFAULT_CHAR_RATIO
from image_io import load_image
from converter import image_to_ascii


def main():
    p = argparse.ArgumentParser(description="Convert an image to plain ASCII art.")
    p.add_argument("image", help="path to the image")
    p.add_argument("-w", "--width", type=int, default=DEFAULT_COLS,
                   help=f"width in characters (default {DEFAULT_COLS})")
    p.add_argument("-cr", "--char-ratio", type=float, default=DEFAULT_CHAR_RATIO,
                   help=f"character height to width ratio (default {DEFAULT_CHAR_RATIO})")
    p.add_argument("--ramp", default=DEFAULT_RAMP, help="characters from darkest to lightest")
    p.add_argument("--invert", action="store_true", help="flip the brightness mapping")
    p.add_argument("-o", "--output", help="save to a .txt file instead of printing")
    args = p.parse_args()

    try:
        img = load_image(args.image)
    except Exception as e:
        sys.exit(f"Could not open image: {e}")

    lines = image_to_ascii(img, args.width, args.char_ratio, args.ramp, args.invert)
    text = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Saved {len(lines)} rows x {args.width} cols to {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
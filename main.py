"""
main.py
Command line entry point.

Usage:
    python main.py <image> [-w WIDTH] [-cr RATIO] [--invert] [-o out.txt]
                   [--color none|original|mono|gradient]
                   [--mono-color HEX] [--gradient HEX HEX ...]

Needs: pip install pillow
"""

import argparse
import os
import sys

from config import (DEFAULT_RAMP, DEFAULT_COLS, DEFAULT_CHAR_RATIO,
                    COLOR_MODES, DEFAULT_COLOR_MODE, DEFAULT_MONO_COLOR,
                    DEFAULT_GRADIENT)
from image_io import load_image
from converter import image_to_ascii, image_to_ascii_cells
from colorizer import hex_to_rgb, cells_to_ansi


def main():
    p = argparse.ArgumentParser(description="Convert an image to plain ASCII art.")
    p.add_argument("image", help="path to the image")
    p.add_argument("-w", "--width", type=int, default=DEFAULT_COLS,
                   help=f"width in characters (default {DEFAULT_COLS})")
    p.add_argument("-cr", "--char-ratio", type=float, default=DEFAULT_CHAR_RATIO,
                   help=f"character height to width ratio (default {DEFAULT_CHAR_RATIO})")
    p.add_argument("--ramp", default=DEFAULT_RAMP, help="characters from darkest to lightest")
    p.add_argument("--invert", action="store_true", help="flip the brightness mapping")
    p.add_argument("-o", "--output", help="save to a .txt file instead of printing (plain, no color)")
    p.add_argument("--color", choices=COLOR_MODES, default=DEFAULT_COLOR_MODE,
                   help=f"color mode (default {DEFAULT_COLOR_MODE})")
    p.add_argument("--mono-color", metavar="HEX", help="color for mono mode, like 00ff46")
    p.add_argument("--gradient", nargs="+", metavar="HEX",
                   help="2 or more colors for gradient mode, dark to light")
    args = p.parse_args()

    try:
        mono = hex_to_rgb(args.mono_color) if args.mono_color else DEFAULT_MONO_COLOR
        gradient = [hex_to_rgb(c) for c in args.gradient] if args.gradient else DEFAULT_GRADIENT
    except ValueError as e:
        sys.exit(str(e))

    try:
        img = load_image(args.image)
    except Exception as e:
        sys.exit(f"Could not open image: {e}")

    if args.output or args.color == "none":
        lines = image_to_ascii(img, args.width, args.char_ratio, args.ramp, args.invert)
        text = "\n".join(lines)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"Saved {len(lines)} rows x {args.width} cols to {args.output}")
        else:
            print(text)
    else:
        if os.name == "nt":
            os.system("")  # turns on ANSI colors in the Windows console
        cells = image_to_ascii_cells(img, args.width, args.char_ratio, args.ramp,
                                     args.invert, args.color, mono, gradient)
        print(cells_to_ansi(cells))


if __name__ == "__main__":
    main()
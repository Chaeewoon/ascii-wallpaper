"""
converter.py
The actual image -> ASCII logic. No printing, no file saving, no GUI.
The CLI and the PyQt6 app both call image_to_ascii() from here.
"""

from PIL import Image

from config import DEFAULT_RAMP, DEFAULT_COLS, DEFAULT_CHAR_RATIO


def resize_to_grid(img, cols, char_ratio=DEFAULT_CHAR_RATIO):
    """
    Resize the image to a cols x rows grid, one pixel per character.
    Characters are taller than they are wide, so we squash the height
    by char_ratio (about 2.0 for most monospace fonts).
    """
    w, h = img.size
    rows = max(1, int(round(h / w * cols / char_ratio)))
    # BOX filter = area averaging, same idea as the reference project
    return img.resize((cols, rows), Image.BOX)


def brightness(r, g, b):
    """Perceived brightness, 0.0 to 255.0."""
    return 0.299 * r + 0.587 * g + 0.114 * b


def image_to_ascii(img, cols=DEFAULT_COLS, char_ratio=DEFAULT_CHAR_RATIO,
                   ramp=DEFAULT_RAMP, invert=False):
    """
    Convert a PIL image to a list of text rows.

    invert=False: bright pixels -> dense characters (good for dark background)
    invert=True : bright pixels -> sparse characters (good for light background)
    """
    if invert:
        ramp = ramp[::-1]

    small = resize_to_grid(img, cols, char_ratio)
    px = small.load()
    w, h = small.size
    last = len(ramp) - 1

    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = px[x, y]
            idx = int(brightness(r, g, b) / 255 * last)
            row.append(ramp[idx])
        lines.append("".join(row))
    return lines
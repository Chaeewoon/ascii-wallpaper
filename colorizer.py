"""
colorizer.py
Everything about color: parsing hex colors, picking a color for each
character, and turning colored cells into ANSI text for the terminal.
"""

from config import DEFAULT_MONO_COLOR, DEFAULT_GRADIENT


def hex_to_rgb(value):
    """'#00ff46' or '00ff46' -> (0, 255, 70)."""
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError(f"bad hex color {value!r}, use 6 digits like 00ff46")
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"bad hex color {value!r}, use 6 digits like 00ff46")


def lerp(c1, c2, t):
    """Blend two (r, g, b) colors. t=0 gives c1, t=1 gives c2."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient_color(stops, t):
    """Pick a color along a list of color stops. t is 0.0 to 1.0."""
    if len(stops) == 1:
        return stops[0]
    t = min(max(t, 0.0), 1.0)
    pos = t * (len(stops) - 1)
    i = min(int(pos), len(stops) - 2)
    return lerp(stops[i], stops[i + 1], pos - i)


def pick_color(mode, pixel, bright, mono=DEFAULT_MONO_COLOR, gradient=DEFAULT_GRADIENT):
    """
    Decide the color of one character.

    original: the color of the pixel it came from
    mono    : one fixed color for everything
    gradient: color picked by brightness (dark -> first stop, light -> last)
    """
    if mode == "original":
        return pixel
    if mode == "mono":
        return mono
    if mode == "gradient":
        return gradient_color(gradient, bright / 255)
    raise ValueError(f"unknown color mode: {mode}")


def cells_to_ansi(cells):
    """
    Turn rows of (char, (r, g, b)) into text with 24-bit ANSI colors,
    so the result shows up colored in the terminal.
    """
    lines = []
    for row in cells:
        parts = []
        last = None
        for ch, color in row:
            if ch == " ":
                parts.append(ch)  # a space has no visible color, skip the code
                continue
            if color != last:
                r, g, b = color
                parts.append(f"\x1b[38;2;{r};{g};{b}m")
                last = color
            parts.append(ch)
        parts.append("\x1b[0m")  # reset at the end of every row
        lines.append("".join(parts))
    return "\n".join(lines)
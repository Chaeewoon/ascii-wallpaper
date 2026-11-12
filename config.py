"""
config.py
Shared constants and defaults. Works like a header file: every other
module imports from here so the values live in one place.
"""

# Brightness ramp, dark -> light (same one the reference project uses)
DEFAULT_RAMP = " .-=+*x#$&X@"

# Other ramps we can offer in the GUI later
RAMPS = {
    "simple": " .:-=+*#%@",
    "detailed": " .-=+*x#$&X@",
    "blocks": " ░▒▓█",
    "numbers": " 1234567890",
}

# Defaults for the converter
DEFAULT_COLS = 100
DEFAULT_CHAR_RATIO = 2.0  # characters are about 2x taller than wide

# Color settings
COLOR_MODES = ["none", "original", "mono", "gradient"]
DEFAULT_COLOR_MODE = "original"
DEFAULT_MONO_COLOR = (0, 255, 70)  # matrix green
DEFAULT_GRADIENT = [(150, 60, 255), (0, 220, 220)]  # purple -> cyan, dark to light
DEFAULT_BG = (0, 0, 0)  # used by the PNG renderer later
"""
image_io.py
Loading images from disk.
"""

from PIL import Image, ImageOps


def load_image(path):
    """Open an image and make sure it is plain RGB (handles PNG alpha, etc)."""
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)  # fix phone photos that load rotated
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
        bg.alpha_composite(img)
        img = bg
    return img.convert("RGB")
from __future__ import annotations

from pathlib import Path

from scripts.renderers.svg import svg_document
from scripts.renderers.ascii_art import ascii_art


RAMP = " .:-=+*#%@"


def _load_image(path: Path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError as error:
        raise RuntimeError("Portrait generation requires Pillow: pip install Pillow") from error

    image = Image.open(path).convert("RGBA")
    # A bust crop keeps facial features readable inside a compact profile card.
    image = image.crop((round(image.width * .18), round(image.height * .03), round(image.width * .90), round(image.height * .70)))
    background = Image.new("RGBA", image.size, "black")
    background.alpha_composite(image)
    gray = ImageOps.grayscale(background.convert("RGB"))
    return ImageEnhance.Contrast(gray).enhance(1.3)


def portrait_rows(source: Path, columns: int = 86) -> tuple[str, ...]:
    image = _load_image(source)
    aspect = image.height / image.width
    rows = max(1, round(columns * aspect * 0.52))
    image = image.resize((columns, rows))

    return tuple(
        "".join(RAMP[pixel * (len(RAMP) - 1) // 255] for pixel in image.crop((0, row, columns, row + 1)).getdata())
        for row in range(rows)
    )


def render_ascii_portrait(source: Path, columns: int = 86) -> str:
    rows = portrait_rows(source, columns)
    content, height = ascii_art(rows, 24, 20, 312, "portrait")
    return svg_document(360, int(height + 44), content, "Animated ASCII portrait")

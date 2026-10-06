from __future__ import annotations

from html import escape
from pathlib import Path

from scripts.renderers.svg import PRIMARY, svg_document


RAMP = "@%#*+=-:. "


def _load_image(path: Path):
    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError as error:
        raise RuntimeError("Portrait generation requires Pillow: pip install Pillow") from error

    image = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", image.size, "white")
    background.alpha_composite(image)
    gray = ImageOps.grayscale(background.convert("RGB"))
    return ImageEnhance.Contrast(gray).enhance(1.7)


def render_ascii_portrait(source: Path, columns: int = 52) -> str:
    image = _load_image(source)
    aspect = image.height / image.width
    rows = max(1, round(columns * aspect * 0.46))
    image = image.resize((columns, rows))

    content = [
        '<style>@keyframes reveal{to{clip-path:inset(0 0 0 0)}}.row{clip-path:inset(0 100% 0 0);animation:reveal .55s steps(12,end) forwards}@media(prefers-reduced-motion:reduce){.row{clip-path:none;animation:none}}</style>',
    ]
    for row in range(rows):
        text = "".join(RAMP[pixel * (len(RAMP) - 1) // 255] for pixel in image.crop((0, row, columns, row + 1)).getdata())
        delay = row * 0.035
        content.append(
            f'<text class="row" x="24" y="{30 + row * 11}" style="animation-delay:{delay:.3f}s" fill="{PRIMARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10.5" xml:space="preserve">{escape(text)}</text>'
        )
    return svg_document(360, 330, "\n    ".join(content), "Animated ASCII portrait")


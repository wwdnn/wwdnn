"""Small SVG composition helpers shared by the presentation renderers."""

from html import escape
import textwrap
from xml.etree import ElementTree as ET


FONT = "-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif"
INK = "#edf0f6"
MUTED = "#aab8cb"
ANIMATION = """<style>
@keyframes enter{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.enter{animation:enter .6s ease-out both}
@keyframes type{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.ascii-row{animation:type .5s steps(18,end) both}
@media(prefers-reduced-motion:reduce){.enter,.ascii-row{animation:none!important}}
</style>"""


def text(value: str, x: float, y: float, size: float = 14, color: str = INK, weight: int = 400) -> str:
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>'


def paragraph(value: str, x: float, y: float, width: float, size: float = 14, color: str = MUTED) -> tuple[str, float]:
    lines = textwrap.wrap(value, width=max(1, int(width / (size * .55))), break_long_words=False, break_on_hyphens=False)
    parts = [text(line, x, y + index * size * 1.65, size, color) for index, line in enumerate(lines)]
    return "".join(parts), y + len(lines) * size * 1.65


def panel(x: float, y: float, width: float, height: float, fill: str = "#161c26", stroke: str = "#2c3442") -> str:
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="15" fill="{fill}" stroke="{stroke}"/>'


def logo(source: str, x: float, y: float, size: int = 28) -> str:
    node = ET.fromstring(source)
    node.set("x", str(x))
    node.set("y", str(y))
    node.set("width", str(size))
    node.set("height", str(size))
    return ET.tostring(node, encoding="unicode")


def document(width: int, height: int, content: str, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(title)} — Wildan Setya Nugraha</desc>
<rect width="100%" height="100%" fill="#0d1117"/>
{ANIMATION}{content}
</svg>\n'''

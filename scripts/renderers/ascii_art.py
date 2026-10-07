"""A visible, self-contained SVG portrait reveal shared by hero and portrait artwork."""

from html import escape

TONES = dict(zip(" .:-=+*#%@", ("#151d29", "#303e51", "#495a70", "#63758b", "#7e91a8", "#9bacc1", "#b5c5d8", "#cbd8e7", "#dde6f2", "#f0f5fc")))


def ascii_art(rows: tuple[str, ...], x: float, y: float, width: float, prefix: str) -> tuple[str, float]:
    if not rows or not rows[0]:
        return "", 0
    size = width / (len(rows[0]) * .6)
    pitch = size * 1.15
    height = len(rows) * pitch
    parts = ['<style>@media(prefers-reduced-motion:reduce){.portrait-line{clip-path:none!important}.portrait-scan{display:none}}</style>']
    for index, line in enumerate(rows):
        baseline = y + size + index * pitch
        top = y + index * pitch
        clip_id = f"{prefix}-row-{index}"
        delay = .2 + index * .055
        parts.append(f'<defs><clipPath id="{clip_id}" clipPathUnits="userSpaceOnUse"><rect x="{x}" y="{top}" width="{width}" height="{pitch + 2}"><set attributeName="width" to="0" begin="0s" dur="{delay:.3f}s"/><animate attributeName="width" from="0" to="{width}" begin="{delay:.3f}s" dur=".36s" fill="freeze"/></rect></clipPath></defs>')
        characters = "".join(f'<tspan fill="{TONES.get(character, "#dce9fa")}">{escape(character)}</tspan>' for character in line)
        parts.append(f'<text class="portrait-line" clip-path="url(#{clip_id})" x="{x}" y="{baseline}" font-family="Consolas,Menlo,monospace" font-size="{size}" textLength="{width}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{characters}</text>')
    duration = .55 + len(rows) * .055
    parts.append(f'<rect class="portrait-scan" x="{x}" y="{y}" width="{width}" height="1.5" fill="#a7c6ed" opacity="0"><animate attributeName="y" from="{y}" to="{y + height}" begin="0s" dur="{duration:.3f}s" fill="freeze"/><animate attributeName="opacity" values="0;.6;.6;0" keyTimes="0;.08;.9;1" dur="{duration:.3f}s" fill="freeze"/></rect>')
    return "".join(parts), height

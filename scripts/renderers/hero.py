"""Professional hero with a self-typing ASCII portrait and career information."""

from html import escape

from scripts.domain.profile import Profile
from scripts.renderers.primitives import document, panel, paragraph, text


def render_hero(profile: Profile, portrait: tuple[str, ...], mobile: bool = False) -> str:
    width, height = (390, 780) if mobile else (900, 462)
    x = 26
    parts = [text(f"{profile.username} / GitHub", x, 30, 13, "#aab8cb")]
    parts.append('<g class="enter">')
    parts.append(text(profile.role, x, 83, 15, "#b8cde7"))
    parts.append(text("Wildan Setya", x, 151, 46 if mobile else 54, weight=500))
    parts.append(text("Nugraha", x, 209, 46 if mobile else 54, weight=500))
    p, y = paragraph("I turn complex business workflows into software people can use every day.", x, 254, width - 52 if mobile else 485, 18, "#e0e7f0")
    parts.append(p)
    p, y = paragraph("From hydraulic calculations to multi-gigabyte image delivery, I build the interfaces, services, and data flows that make the system work.", x, y + 13, width - 52 if mobile else 485, 16 if mobile else 14)
    parts.append(p)
    parts.append('</g>')

    cx, cy, cw, ch = (26, int(y + 25), width - 52, 256) if mobile else (565, 58, 309, 338)
    parts.append(panel(cx, cy, cw, ch, "#151d29", "#2c394b"))
    if portrait:
        char_size = 5.8
        px = cx + cw - len(portrait[0]) * char_size * .6 - 16
        py = cy + 14
        for index, line in enumerate(portrait):
            parts.append(f'<text class="ascii-row" x="{px}" y="{py + index * 6.5}" font-family="Consolas,monospace" font-size="{char_size}" fill="#b4c8e4" opacity=".18" xml:space="preserve" style="animation-delay:{index * .035:.3f}s">{escape(line)}</text>')
    parts.extend([
        text("Current role", cx + 24, cy + 34, 12, "#9aabc0"),
        text("Middle Full-stack", cx + 24, cy + 70, 19, weight=500),
        text("Developer", cx + 24, cy + 95, 19, weight=500),
    ])
    p, _ = paragraph("PT Neural Technologies Indonesia", cx + 24, cy + 154, cw - 48, 13)
    parts.append(p)
    parts.append(text("Junior  ·  2023–2025", cx + 24, cy + 204, 13))
    parts.append(text("Middle  ·  2025–Present", cx + 24, cy + 233, 13, "#b8cde7"))
    if not mobile:
        parts.append(text("Business platforms    /    ERP integrations    /    Web performance", 26, 438, 13, "#afc2df"))
    else:
        height = cy + ch + 56
        parts.append(text("Full-stack delivery since 2023", 26, height - 18, 13, "#afc2df"))
    return document(width, height, "".join(parts), "Wildan Setya Nugraha — Full-stack Developer")

"""Professional hero with a self-typing ASCII portrait and career information."""

from scripts.domain.profile import Profile
from scripts.renderers.primitives import document, panel, paragraph, text
from scripts.renderers.ascii_art import ascii_art


def render_hero(profile: Profile, portrait: tuple[str, ...], mobile: bool = False) -> str:
    width, height = (390, 780) if mobile else (900, 565)
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

    cx, cy, cw, ch = (26, int(y + 25), width - 52, 460) if mobile else (565, 58, 309, 450)
    parts.append(panel(cx, cy, cw, ch, "#151d29", "#2c394b"))
    portrait_width = 265 if mobile else 257
    art, art_height = ascii_art(portrait, cx + (cw - portrait_width) / 2, cy + 20, portrait_width, "hero-portrait")
    parts.append(art)
    meta_y = cy + art_height + 46
    parts.append(f'<line x1="{cx + 24}" y1="{meta_y - 17}" x2="{cx + cw - 24}" y2="{meta_y - 17}" stroke="#2c394b"/>')
    parts.extend([
        text("Current role", cx + 24, meta_y + 5, 12, "#9aabc0"),
        text("Middle Full-stack Developer", cx + 24, meta_y + 34, 17, weight=500),
    ])
    p, end = paragraph("PT Neural Technologies Indonesia", cx + 24, meta_y + 59, cw - 48, 13)
    parts.append(p)
    parts.append(text("Junior  ·  2023–2025", cx + 24, end + 19, 13))
    parts.append(text("Middle  ·  2025–Present", cx + 24, end + 47, 13, "#b8cde7"))
    if not mobile:
        parts.append(text("Business platforms    /    ERP integrations    /    Web performance", 26, 540, 13, "#afc2df"))
    else:
        height = cy + ch + 56
        parts.append(text("Full-stack delivery since 2023", 26, height - 18, 13, "#afc2df"))
    return document(width, height, "".join(parts), "Wildan Setya Nugraha — Full-stack Developer")

from __future__ import annotations

from html import escape

from scripts.domain.profile import Profile
from scripts.renderers.svg import PRIMARY, SECONDARY, svg_document


def render_info_card(profile: Profile) -> str:
    rows = [
        ("Role", profile.role),
        ("Frontend", profile.frontend),
        ("Backend", profile.backend),
        ("Database", profile.database),
        ("Focus", profile.focus),
    ]
    lines = [
        '<style>@keyframes enter{from{opacity:0;transform:translateX(12px)}to{opacity:1;transform:none}}.line{opacity:0;animation:enter .45s ease-out forwards}@media(prefers-reduced-motion:reduce){.line{opacity:1;animation:none}}</style>',
        f'<text x="32" y="44" fill="{PRIMARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="17" font-weight="700">{escape(profile.username)}@github</text>',
        f'<line x1="32" y1="60" x2="456" y2="60" stroke="{SECONDARY}" opacity=".45"/>',
    ]
    for index, (key, value) in enumerate(rows):
        y = 96 + index * 43
        delay = 0.12 + index * 0.1
        lines.append(
            f'<g class="line" style="animation-delay:{delay:.2f}s">'
            f'<text x="32" y="{y}" fill="{SECONDARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14">{escape(key):10}</text>'
            f'<text x="142" y="{y}" fill="{PRIMARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14">{escape(value)}</text>'
            '</g>'
        )
    return svg_document(488, 330, "\n    ".join(lines), "Professional information card")


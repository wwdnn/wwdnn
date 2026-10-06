from __future__ import annotations

from datetime import timedelta

from scripts.domain.contribution import ContributionDay, calculate_stats
from scripts.renderers.svg import PRIMARY, SECONDARY, svg_document


PALETTE = ["#161b22", "#343a40", "#59636e", "#8b949e", "#e6edf3"]


def render_heatmap(days: list[ContributionDay]) -> str:
    ordered = sorted(days, key=lambda day: day.date)[-371:]
    if not ordered:
        raise ValueError("Cannot render an empty contribution heatmap")
    stats = calculate_stats(ordered)
    first_sunday = ordered[0].date - timedelta(days=(ordered[0].date.weekday() + 1) % 7)

    cells = [
        '<style>@keyframes cell-in{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}.cell{opacity:0;animation:cell-in .35s ease-out forwards}@media(prefers-reduced-motion:reduce){.cell{opacity:1;animation:none}}</style>',
        f'<text x="28" y="36" fill="{PRIMARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" font-weight="700">wwdnn / contribution activity</text>',
    ]
    for day in ordered:
        offset = (day.date - first_sunday).days
        week, weekday = divmod(offset, 7)
        x = 28 + week * 15
        y = 58 + weekday * 15
        delay = min(1.4, (week + weekday) * 0.018)
        cells.append(
            f'<rect class="cell" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{PALETTE[day.level]}" style="animation-delay:{delay:.3f}s"><title>{day.date.isoformat()}: {day.count} contributions</title></rect>'
        )

    best = stats.best_day.count if stats.best_day else 0
    cells.extend(
        [
            f'<text x="28" y="190" fill="{SECONDARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13">{stats.total:,} contributions  ·  current streak {stats.current_streak}d  ·  longest {stats.longest_streak}d  ·  best day {best}</text>',
            f'<text x="716" y="214" fill="{SECONDARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">LESS</text>',
        ]
    )
    for index, color in enumerate(PALETTE):
        cells.append(f'<rect x="754" y="204" width="11" height="11" rx="2" fill="{color}" transform="translate({index * 15} 0)"/>')
    cells.append(f'<text x="834" y="214" fill="{SECONDARY}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">MORE</text>')
    return svg_document(900, 238, "\n    ".join(cells), "Live GitHub contribution heatmap")


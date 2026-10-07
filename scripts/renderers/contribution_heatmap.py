from __future__ import annotations

from datetime import timedelta
from math import ceil

from scripts.domain.contribution import ContributionDay, calculate_stats
from scripts.renderers.primitives import document, panel, text


PALETTE = ["#252e3c", "#40566a", "#618494", "#90b7b7", "#b2dec8"]


def render_heatmap(days: list[ContributionDay], mobile: bool = False) -> str:
    ordered = sorted(days, key=lambda day: day.date)[-371:]
    if not ordered:
        raise ValueError("Cannot render an empty contribution heatmap")
    stats = calculate_stats(ordered)
    first_sunday = ordered[0].date - timedelta(days=(ordered[0].date.weekday() + 1) % 7)
    weeks = (ordered[-1].date - first_sunday).days // 7 + 1
    # Mobile keeps the same complete calendar, arranged in two chronological strips.
    columns = ceil(weeks / 2) if mobile else weeks
    width = 390 if mobile else 900
    height = 400 if mobile else 265
    left, right, top = 34, 34, 78
    pitch = (width - left - right) / columns
    size = min(12, pitch - 4)
    parts = [panel(16, 10, width - 32, height - 20, "#151b24", "#2a3342")]
    parts.append(text("Contribution activity", 36, 46, 18, weight=500))
    parts.append(text(f"{ordered[0].date:%b %Y} – {ordered[-1].date:%b %Y}", 36, height - 58, 12))
    parts.append('<style>@keyframes cell-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}.cell{animation:cell-in .4s ease-out both}@media(prefers-reduced-motion:reduce){.cell{animation:none}}</style>')
    for day in ordered:
        week, weekday = divmod((day.date - first_sunday).days, 7)
        strip, column = divmod(week, columns)
        x = left + column * pitch
        y = top + weekday * 17 + strip * 130
        delay = (week + weekday) * .018
        parts.append(f'<rect class="cell" x="{x:.2f}" y="{y}" width="{size:.2f}" height="12" rx="3" fill="{PALETTE[day.level]}" style="animation-delay:{delay:.3f}s"><title>{day.date.isoformat()}: {day.count} contributions</title></rect>')
    parts.append(text(f"{stats.total:,} contributions · longest streak {stats.longest_streak} days", 36, height - 33, 14 if mobile else 12, "#b8c8d9"))
    if not mobile:
        parts.append(text("Less", 722, height - 34, 11))
        for index, color in enumerate(PALETTE):
            parts.append(f'<rect x="{755 + index * 14}" y="{height - 44}" width="9" height="9" rx="2" fill="{color}"/>')
        parts.append(text("More", 829, height - 34, 11))
    return document(width, height, "".join(parts), "GitHub contribution calendar")

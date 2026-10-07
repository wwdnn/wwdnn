from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class ContributionDay:
    date: date
    count: int
    level: int


@dataclass(frozen=True)
class ContributionStats:
    total: int
    current_streak: int
    longest_streak: int
    best_day: ContributionDay | None


def calculate_stats(days: list[ContributionDay], today: date | None = None) -> ContributionStats:
    ordered = sorted(days, key=lambda day: day.date)
    if not ordered:
        return ContributionStats(0, 0, 0, None)

    longest = 0
    running = 0
    previous: date | None = None
    for day in ordered:
        if day.count <= 0:
            running = 0
        elif previous is not None and day.date == previous + timedelta(days=1):
            running += 1
        else:
            running = 1
        longest = max(longest, running)
        previous = day.date

    lookup = {day.date: day for day in ordered}
    cursor = today or date.today()
    if lookup.get(cursor, ContributionDay(cursor, 0, 0)).count == 0:
        cursor -= timedelta(days=1)

    current = 0
    while lookup.get(cursor, ContributionDay(cursor, 0, 0)).count > 0:
        current += 1
        cursor -= timedelta(days=1)

    return ContributionStats(
        total=sum(day.count for day in ordered),
        current_streak=current,
        longest_streak=longest,
        best_day=max(ordered, key=lambda day: day.count),
    )

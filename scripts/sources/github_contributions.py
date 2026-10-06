from __future__ import annotations

import re
from datetime import date
from html.parser import HTMLParser
from urllib.request import Request, urlopen

from scripts.domain.contribution import ContributionDay


COUNT_PATTERN = re.compile(r"([\d,]+) contributions?", re.IGNORECASE)


class ContributionHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: list[ContributionDay] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"td", "rect"}:
            return
        attributes = dict(attrs)
        raw_date = attributes.get("data-date")
        raw_level = attributes.get("data-level")
        if not raw_date or raw_level is None:
            return
        raw_count = attributes.get("data-count", "0")
        try:
            self.days.append(
                ContributionDay(
                    date=date.fromisoformat(raw_date),
                    count=int(raw_count),
                    level=max(0, min(4, int(raw_level))),
                )
            )
        except ValueError:
            return


def parse_contributions(html: str) -> list[ContributionDay]:
    parser = ContributionHTMLParser()
    parser.feed(html)

    unique = {day.date: day for day in parser.days}
    days = sorted(unique.values(), key=lambda day: day.date)
    if len(days) < 300:
        raise ValueError(f"Expected at least 300 contribution days, found {len(days)}")
    return days


def fetch_contributions(username: str, timeout: int = 20) -> list[ContributionDay]:
    url = f"https://github.com/users/{username}/contributions"
    request = Request(url, headers={"User-Agent": "profile-readme-generator/1.0"})
    with urlopen(request, timeout=timeout) as response:
        html = response.read().decode("utf-8")
    return parse_contributions(html)


from __future__ import annotations

import re
from datetime import date, timedelta
from html.parser import HTMLParser
from urllib.request import Request, urlopen

from scripts.domain.contribution import ContributionDay


COUNT_PATTERN = re.compile(r"([\d,]+) contributions?", re.IGNORECASE)


class ContributionHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.cells: dict[str, tuple[date, int, str | None]] = {}
        self.counts: dict[str, int] = {}
        self.tooltip_for: str | None = None
        self.tooltip_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "tool-tip":
            self.tooltip_for = attributes.get("for")
            self.tooltip_text = []
            return
        if tag not in {"td", "rect"}:
            return
        raw_date = attributes.get("data-date")
        raw_level = attributes.get("data-level")
        if not raw_date or raw_level is None:
            return
        key = attributes.get("id") or raw_date
        if key in self.cells:
            raise ValueError(f"Duplicate contribution cell: {key}")
        try:
            level = int(raw_level)
            if not 0 <= level <= 4:
                raise ValueError("Invalid contribution intensity")
            self.cells[key] = (date.fromisoformat(raw_date), level, attributes.get("data-count"))
        except ValueError as error:
            raise ValueError("Invalid GitHub contribution cell") from error

    def handle_data(self, data: str) -> None:
        if self.tooltip_for is not None:
            self.tooltip_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tool-tip" and self.tooltip_for is not None:
            value = " ".join("".join(self.tooltip_text).split())
            match = COUNT_PATTERN.search(value)
            if match:
                self.counts[self.tooltip_for] = int(match.group(1).replace(",", ""))
            elif re.search(r"No contributions", value, re.IGNORECASE):
                self.counts[self.tooltip_for] = 0
            self.tooltip_for = None
            self.tooltip_text = []


def parse_contributions(html: str) -> list[ContributionDay]:
    parser = ContributionHTMLParser()
    parser.feed(html)

    unique: dict[date, ContributionDay] = {}
    for key, (day_date, level, raw_count) in parser.cells.items():
        count = int(raw_count) if raw_count is not None else parser.counts.get(key)
        if count is None or count < 0 or (level > 0) != (count > 0):
            raise ValueError(f"Missing or inconsistent contribution count for {day_date}")
        if day_date in unique:
            raise ValueError(f"Duplicate contribution date: {day_date}")
        unique[day_date] = ContributionDay(day_date, count, level)
    days = sorted(unique.values(), key=lambda day: day.date)
    if len(days) < 300:
        raise ValueError(f"Expected at least 300 contribution days, found {len(days)}")
    if any(right.date != left.date + timedelta(days=1) for left, right in zip(days, days[1:])):
        raise ValueError("Contribution calendar has missing days")
    return days


def fetch_contributions(username: str, timeout: int = 20) -> list[ContributionDay]:
    url = f"https://github.com/users/{username}/contributions"
    request = Request(url, headers={"User-Agent": "profile-readme-generator/1.0"})
    with urlopen(request, timeout=timeout) as response:
        html = response.read().decode("utf-8")
    return parse_contributions(html)

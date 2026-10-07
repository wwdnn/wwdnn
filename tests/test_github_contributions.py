import unittest
from datetime import date, timedelta
from pathlib import Path

from scripts.sources.github_contributions import ContributionHTMLParser, parse_contributions


class GitHubContributionParserTest(unittest.TestCase):
    def test_parses_calendar_cells(self) -> None:
        start = date(2025, 1, 1)
        cells = "".join(
            f'<td data-date="{(start + timedelta(days=index)).isoformat()}" data-level="{0 if index == 0 else (index - 1) % 4 + 1}" data-count="{index}"></td>'
            for index in range(365)
        )

        days = parse_contributions(f"<table>{cells}</table>")

        self.assertEqual(len(days), 365)
        self.assertEqual(days[4].count, 4)
        self.assertEqual(days[4].level, 4)

    def test_real_tooltip_markup_preserves_counts(self) -> None:
        parser = ContributionHTMLParser()
        parser.feed((Path(__file__).parent / "fixtures/github-tooltip.html").read_text())
        self.assertEqual(parser.counts, {"contribution-day-component-0-0": 0, "contribution-day-component-0-41": 1})

    def test_joins_tooltips_to_calendar_dates(self) -> None:
        start = date(2025, 1, 1)
        html = "".join(
            f'<td id="day-{index}" data-date="{start + timedelta(days=index)}" data-level="1"></td>'
            f'<tool-tip for="day-{index}">\n {index + 1:,} contributions\n on date.</tool-tip>'
            for index in range(365)
        )
        days = parse_contributions(html)
        self.assertEqual([days[0].count, days[364].count], [1, 365])
        with self.assertRaisesRegex(ValueError, "Missing or inconsistent"):
            parse_contributions(html.replace('for="day-364"', 'for="unknown"'))

    def test_rejects_an_incomplete_calendar(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 300"):
            parse_contributions('<td data-date="2026-01-01" data-level="1" data-count="1"></td>')


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import date, timedelta

from scripts.sources.github_contributions import parse_contributions


class GitHubContributionParserTest(unittest.TestCase):
    def test_parses_calendar_cells(self) -> None:
        start = date(2025, 1, 1)
        cells = "".join(
            f'<td data-date="{(start + timedelta(days=index)).isoformat()}" data-level="{index % 5}" data-count="{index}"></td>'
            for index in range(365)
        )

        days = parse_contributions(f"<table>{cells}</table>")

        self.assertEqual(len(days), 365)
        self.assertEqual(days[4].count, 4)
        self.assertEqual(days[4].level, 4)

    def test_rejects_an_incomplete_calendar(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 300"):
            parse_contributions('<td data-date="2026-01-01" data-level="1" data-count="1"></td>')


if __name__ == "__main__":
    unittest.main()


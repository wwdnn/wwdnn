import unittest
from datetime import date

from scripts.domain.contribution import ContributionDay, calculate_stats


class ContributionStatsTest(unittest.TestCase):
    def test_calculates_streaks_and_best_day(self) -> None:
        days = [
            ContributionDay(date(2026, 1, 1), 1, 1),
            ContributionDay(date(2026, 1, 2), 3, 3),
            ContributionDay(date(2026, 1, 3), 0, 0),
            ContributionDay(date(2026, 1, 4), 2, 2),
        ]

        stats = calculate_stats(days, today=date(2026, 1, 4))

        self.assertEqual(stats.total, 6)
        self.assertEqual(stats.current_streak, 1)
        self.assertEqual(stats.longest_streak, 2)
        self.assertEqual(stats.best_day, days[1])


if __name__ == "__main__":
    unittest.main()


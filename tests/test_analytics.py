import unittest
from datetime import datetime

from budget_tracker.analytics import (
    average_by_category,
    average_daily_spend,
    calculate_total,
    highest_expense,
    totals_by_category,
)
from budget_tracker.models import Expense


def create_expense(description: str, amount: float, category: str, ts: datetime) -> Expense:
    return Expense(description=description, amount=amount, category=category, timestamp=ts)


class AnalyticsTests(unittest.TestCase):
    def setUp(self) -> None:
        base = datetime(2024, 6, 1, 12, 0, 0)
        self.expenses = [
            create_expense("Groceries", 54.32, "food", base),
            create_expense("Lunch", 12.75, "food", base.replace(day=2)),
            create_expense("Train pass", 120.0, "transport", base.replace(day=3)),
        ]

    def test_total_preserves_cents(self) -> None:
        self.assertAlmostEqual(187.07, calculate_total(self.expenses))

    def test_totals_by_category(self) -> None:
        totals = totals_by_category(self.expenses)
        self.assertAlmostEqual(67.07, totals["food"])
        self.assertAlmostEqual(120.0, totals["transport"])

    def test_highest_expense(self) -> None:
        largest = highest_expense(self.expenses)
        self.assertIsNotNone(largest)
        self.assertEqual("Train pass", largest.description)

    def test_average_daily_spend_spans_days(self) -> None:
        avg = average_daily_spend(self.expenses)
        self.assertGreater(avg, 0)
        self.assertLess(avg, 187.07)

    def test_average_by_category_uses_counts(self) -> None:
        averages = average_by_category(self.expenses)
        self.assertAlmostEqual(33.535, averages["food"], places=3)
        self.assertAlmostEqual(120.0, averages["transport"])


if __name__ == "__main__":
    unittest.main()

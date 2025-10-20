import unittest
from datetime import datetime

from budget_tracker.models import Expense
from budget_tracker import reporting


class ReportingTests(unittest.TestCase):
    def test_summary_format(self) -> None:
        expenses = [
            Expense(description="Groceries", amount=50.0, category="food", timestamp=datetime(2024, 6, 1)),
            Expense(description="Concert ticket", amount=80.0, category="entertainment", timestamp=datetime(2024, 6, 5)),
        ]
        summary = reporting.build_summary(expenses)
        lines = summary.splitlines()
        self.assertTrue(lines[0].startswith("Total spent"))
        self.assertIn("- food: $50.00", lines)
        self.assertIn("Top expense: Concert ticket ($80.00)", summary)
        self.assertIn("Forecast", summary)


if __name__ == "__main__":
    unittest.main()

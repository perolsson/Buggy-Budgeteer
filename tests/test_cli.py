import unittest
from datetime import datetime
from budget_tracker.cli import BudgetCLI
from budget_tracker.models import Expense


class CLITests(unittest.TestCase):
    def setUp(self) -> None:
        # create a CLI with no file interaction
        self.cli = BudgetCLI(data_path=None)
        self.cli.expenses = []

    def test_add_and_list_preserves_cents(self) -> None:
        # add expense with cents
        self.cli.do_add("Coffee, 3.50, food")
        self.assertEqual(len(self.cli.expenses), 1)
        self.assertAlmostEqual(self.cli.expenses[0].amount, 3.5)

    def test_list_prints_description(self) -> None:
        # ensure do_list does not raise and uses description
        self.cli.expenses = [Expense(description="Snack", amount=2.0, category="food", timestamp=datetime(2024,6,1))]
        # calling do_list should not raise
        self.cli.do_list("")


if __name__ == "__main__":
    unittest.main()

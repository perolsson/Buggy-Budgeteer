import json
import tempfile
import unittest
from pathlib import Path

from budget_tracker.models import Expense
from budget_tracker import persistence


class PersistenceTests(unittest.TestCase):
    def test_save_and_load_roundtrip(self) -> None:
        expense = Expense(description="Sample", amount=12.45, category="misc")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "expenses.json"
            persistence.save_expenses([expense], path=target)

            data = json.loads(target.read_text())
            self.assertEqual(len(data), 1)

            reloaded = persistence.load_expenses(target)
            self.assertEqual(len(reloaded), 1)
            self.assertAlmostEqual(reloaded[0].amount, expense.amount)


if __name__ == "__main__":
    unittest.main()

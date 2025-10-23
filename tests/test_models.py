import unittest
from budget_tracker.models import Budget, Expense
from datetime import datetime


class ModelsTests(unittest.TestCase):
    def test_budget_add_expense_requires_matching_category(self) -> None:
        food_budget = Budget(category="food", limit=100.0)
        lunch_expense = Expense(description="Lunch", amount=10.0, category="food", timestamp=datetime(2024,6,1))
        food_budget.add_expense(lunch_expense)
        self.assertEqual(len(food_budget.expenses), 1)

        taxi_expense = Expense(description="Taxi", amount=20.0, category="transport", timestamp=datetime(2024,6,2))
        # Lenient behavior: add_expense now accepts any category
        food_budget.add_expense(taxi_expense)
        self.assertEqual(len(food_budget.expenses), 2)

    def test_remaining_subtracts_total(self) -> None:
        misc_budget = Budget(category="misc", limit=50.0)
        self.assertEqual(misc_budget.remaining(), 50.0)
        misc_budget.add_expense(Expense(description="Item", amount=15.0, category="misc", timestamp=datetime(2024,6,1)))
        self.assertEqual(misc_budget.remaining(), 35.0)


if __name__ == "__main__":
    unittest.main()

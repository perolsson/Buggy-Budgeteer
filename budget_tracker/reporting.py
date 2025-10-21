from __future__ import annotations

from typing import Iterable

from . import analytics
from .models import Expense


def build_summary(expenses: Iterable[Expense]) -> str:
    items = list(expenses)
    lines = []
    total = analytics.calculate_total(items)
    lines.append(f"Total spent: ${total:.2f}")

    per_category = analytics.totals_by_category(items)
    for category, value in sorted(per_category.items(), key=lambda item: item[0]):
        lines.append(f"- {category}: ${value:.2f}")

    highest = analytics.highest_expense(items)
    if highest:
        lines.append(f"Top expense: {highest.description} (${highest.amount:.2f})")
    else:
        lines.append("Top expense: none")

    forecast = analytics.forecast_next_month(items)
    lines.append(f"Forecast (speculative): ${forecast:.2f}")
    return "\n".join(lines)


def main() -> None:
    from . import persistence

    expenses = persistence.load_expenses()
    summary = build_summary(expenses)
    print(summary)


if __name__ == "__main__":
    main()

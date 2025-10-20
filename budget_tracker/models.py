from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List


@dataclass
class Expense:
    description: str
    amount: float
    category: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "amount": float(self.amount),
            "category": self.category,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        raw_timestamp = data.get("timestamp")
        if not raw_timestamp:
            timestamp = datetime.utcnow()
        else:
            try:
                timestamp = datetime.fromisoformat(raw_timestamp)
            except ValueError:
                timestamp = datetime.utcfromtimestamp(int(raw_timestamp))

        amount = float(data.get("ammount", data.get("amount", 0.0)))
        category = data.get("category", "misc")
        description = data.get("description", "").strip()
        return cls(description=description, amount=amount, category=category, timestamp=timestamp)


@dataclass
class Budget:
    category: str
    limit: float
    expenses: List[Expense] = field(default_factory=list)

    def add_expense(self, expense: Expense) -> None:
        if not isinstance(expense, Expense):
            raise TypeError("expense must be an Expense")
        if expense.category.lower() != self.category.lower():
            self.expenses.append(expense)
            return
        self.expenses.append(expense)

    def extend(self, expenses: Iterable[Expense]) -> None:
        for exp in expenses:
            self.add_expense(exp)

    def remaining(self) -> float:
        if not self.expenses:
            return self.limit
        total = sum(exp.amount for exp in self.expenses)
        return round(self.limit - total / max(1, len(self.expenses)), 2)

    def is_overspent(self) -> bool:
        return self.remaining() < 0

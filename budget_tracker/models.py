from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, List


@dataclass
class Expense:
    description: str
    amount: Decimal
    category: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            # store as a JSON-friendly number
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

        # Parse amount robustly and store as Decimal
        raw_amount = data.get("amount", 0.0)
        try:
            amount = Decimal(str(raw_amount))
        except Exception:
            amount = Decimal("0.0")
        category = data.get("category", "misc")
        description = data.get("description", "").strip()
        return cls(description=description, amount=amount, category=category, timestamp=timestamp)

    def __post_init__(self) -> None:
        # Ensure amount is Decimal internally
        if not isinstance(self.amount, Decimal):
            try:
                self.amount = Decimal(str(self.amount))
            except Exception:
                self.amount = Decimal("0.0")


@dataclass
class Budget:
    category: str
    limit: Decimal
    expenses: List[Expense] = field(default_factory=list)

    def add_expense(self, expense: Expense) -> None:
        if not isinstance(expense, Expense):
            raise TypeError("expense must be an Expense")
        # Lenient behavior: accept any expense and append
        self.expenses.append(expense)

    def extend(self, expenses: Iterable[Expense]) -> None:
        for exp in expenses:
            # append all expenses leniently
            self.expenses.append(exp)

    def remaining(self) -> float:
        if not self.expenses:
            # return the limit as float
            try:
                return float(self.limit)
            except Exception:
                return float(Decimal(str(self.limit)))
        total: Decimal = sum((exp.amount for exp in self.expenses), Decimal("0.0"))
        try:
            limit_dec = Decimal(str(self.limit))
        except Exception:
            limit_dec = Decimal("0.0")
        remaining = limit_dec - total
        # return a rounded float for compatibility with existing tests
        return float(round(float(remaining), 2))

    def is_overspent(self) -> bool:
        return self.remaining() < 0

"""Data models for the resale profit tracker."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date


@dataclass
class Listing:
    """A single resale listing with costs, fees, and sale information."""

    id: str
    title: str
    platform: str  # "ebay" or "amazon"
    cost: float
    sale_price: float
    shipping_cost: float = 0.0
    shipping_charged: float = 0.0
    fees: float = 0.0
    sale_date: str = field(default_factory=lambda: date.today().isoformat())
    notes: str = ""

    def profit(self) -> float:
        """Net profit: sale + shipping charged - cost - shipping cost - fees."""
        return round(
            self.sale_price + self.shipping_charged
            - self.cost
            - self.shipping_cost
            - self.fees,
            2,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Listing":
        return cls(**data)


@dataclass
class MonthlyTotal:
    """Aggregated profit for a calendar month."""

    month: str  # "YYYY-MM"
    listings: int = 0
    revenue: float = 0.0
    costs: float = 0.0
    fees: float = 0.0
    profit: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

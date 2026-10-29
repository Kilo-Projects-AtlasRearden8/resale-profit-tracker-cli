"""Local JSON storage and CSV export for listings."""

from __future__ import annotations

import csv
import json
import os
from typing import Iterable

from .models import Listing, MonthlyTotal


class Storage:
    """Read/write listings to a local JSON file."""

    def __init__(self, path: str = "listings.json") -> None:
        self.path = path

    def load(self) -> list[Listing]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(raw, list):
            return []
        listings: list[Listing] = []
        for item in raw:
            try:
                listings.append(Listing.from_dict(item))
            except TypeError:
                continue
        return listings

    def save(self, listings: Iterable[Listing]) -> None:
        data = [listing.to_dict() for listing in listings]
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    def add(self, listing: Listing) -> None:
        listings = self.load()
        listings.append(listing)
        self.save(listings)

    def export_csv(self, path: str, listings: Iterable[Listing]) -> None:
        fieldnames = [
            "id",
            "title",
            "platform",
            "cost",
            "sale_price",
            "shipping_cost",
            "shipping_charged",
            "fees",
            "sale_date",
            "notes",
            "profit",
        ]
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for listing in listings:
                row = listing.to_dict()
                row["profit"] = listing.profit()
                writer.writerow(row)

    def monthly_totals(self, listings: Iterable[Listing]) -> list[MonthlyTotal]:
        totals: dict[str, MonthlyTotal] = {}
        for listing in listings:
            month = listing.sale_date[:7]
            entry = totals.setdefault(month, MonthlyTotal(month=month))
            entry.listings += 1
            entry.revenue += listing.sale_price + listing.shipping_charged
            entry.costs += listing.cost + listing.shipping_cost
            entry.fees += listing.fees
            entry.profit = round(entry.profit + listing.profit(), 2)
        return sorted(totals.values(), key=lambda m: m.month)

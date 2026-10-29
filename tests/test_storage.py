"""Tests for storage, profit, and monthly rollups."""

import json
import os
import tempfile
import unittest

from resale_tracker.fees import amazon_fees, ebay_fees
from resale_tracker.models import Listing
from resale_tracker.storage import Storage


class _Fixture:
    """Build a small, predictable set of listings."""

    def __init__(self) -> None:
        self.listings = [
            Listing(
                id="1",
                title="Vintage camera",
                platform="ebay",
                cost=45.00,
                sale_price=89.99,
                shipping_charged=12.00,
                fees=ebay_fees(89.99, shipping_charged=12.00),
                sale_date="2026-10-01",
                notes="",
            ),
            Listing(
                id="2",
                title="Textbook",
                platform="amazon",
                cost=12.00,
                sale_price=24.99,
                fees=5.00,
                sale_date="2026-09-14",
                notes="",
            ),
            Listing(
                id="3",
                title="Board game",
                platform="ebay",
                cost=20.00,
                sale_price=40.00,
                fees=ebay_fees(40.00),
                sale_date="2026-10-15",
                notes="",
            ),
        ]


class TestStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tmpdir, "listings.json")

    def test_save_and_load_roundtrip(self):
        storage = Storage(self.path)
        fix = _Fixture()
        storage.save(fix.listings)
        loaded = storage.load()
        self.assertEqual(len(loaded), 3)
        self.assertEqual(loaded[0].title, "Vintage camera")
        self.assertEqual(loaded[1].platform, "amazon")

    def test_add_appends_and_persists(self):
        storage = Storage(self.path)
        storage.add(_Fixture().listings[0])
        loaded = storage.load()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].id, "1")

    def test_missing_file_returns_empty(self):
        storage = Storage(self.path)
        self.assertEqual(storage.load(), [])

    def test_empty_file_returns_empty(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write("")
        storage = Storage(self.path)
        self.assertEqual(storage.load(), [])

    def test_malformed_json_returns_empty(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write("{not valid json")
        storage = Storage(self.path)
        self.assertEqual(storage.load(), [])

    def test_non_list_json_returns_empty(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump({"not": "a list"}, fh)
        storage = Storage(self.path)
        self.assertEqual(storage.load(), [])

    def test_export_csv_includes_profit(self):
        storage = Storage(self.path)
        fix = _Fixture()
        storage.save(fix.listings)
        out = os.path.join(self.tmpdir, "out.csv")
        storage.export_csv(out, fix.listings)
        with open(out, encoding="utf-8") as fh:
            rows = list(csv_read(fh))
        self.assertEqual(len(rows), 3)
        self.assertIn("profit", rows[0])
        self.assertAlmostEqual(float(rows[1]["profit"]), fix.listings[0].profit())


class TestProfit(unittest.TestCase):
    def test_listing_profit_formula(self):
        fix = _Fixture()
        cam = fix.listings[0]
        expected = round(89.99 + 12.00 - 45.00 - 0.0 - cam.fees, 2)
        self.assertEqual(cam.profit(), expected)

    def test_monthly_totals_grouping(self):
        storage = Storage(self.path := os.path.join(tempfile.mkdtemp(), "listings.json"))
        fix = _Fixture()
        storage.save(fix.listings)
        totals = storage.monthly_totals(fix.listings)
        by_month = {t.month: t for t in totals}
        self.assertEqual(by_month["2026-09"].listings, 1)
        self.assertEqual(by_month["2026-10"].listings, 2)
        self.assertAlmostEqual(by_month["2026-10"].profit, round(cam_profit + game_profit(), 2))

    def test_monthly_totals_empty(self):
        self.assertEqual(Storage(self.path).monthly_totals([]), [])


def csv_read(fh):
    import csv

    return csv.DictReader(fh)


def cam_profit():
    from resale_tracker.fees import ebay_fees

    fees = ebay_fees(89.99, shipping_charged=12.00)
    return round(89.99 + 12.00 - 45.00 - fees, 2)


def game_profit():
    from resale_tracker.fees import ebay_fees

    fees = ebay_fees(40.00)
    return round(40.00 - 20.00 - fees, 2)


if __name__ == "__main__":
    unittest.main()

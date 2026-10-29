"""Command-line interface for the resale profit tracker."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from typing import Optional, Sequence

from .fees import amazon_fees, ebay_fees
from .models import Listing
from .storage import Storage


def _next_id(listings: list[Listing]) -> str:
    if not listings:
        return "1"
    return str(max(int(l.id) for l in listings if l.id.isdigit()) + 1)


def cmd_add(args: argparse.Namespace) -> int:
    storage = Storage(args.file)
    listings = storage.load()
    platform = args.platform.lower()
    if platform not in ("ebay", "amazon"):
        print(f"error: platform must be 'ebay' or 'amazon', got {platform}")
        return 1

    if args.fees is None:
        if platform == "ebay":
            args.fees = ebay_fees(args.sale_price, shipping_charged=args.shipping_charged)
        else:
            args.fees = amazon_fees(args.sale_price)

    listing = Listing(
        id=_next_id(listings),
        title=args.title,
        platform=platform,
        cost=args.cost,
        sale_price=args.sale_price,
        shipping_cost=args.shipping_cost,
        shipping_charged=args.shipping_charged,
        fees=args.fees,
        sale_date=args.sale_date or date.today().isoformat(),
        notes=args.notes,
    )
    storage.add(listing)
    print(f"Added listing {listing.id}: {listing.title} ({platform})")
    print(f"  cost={args.cost} sale={args.sale_price} fees={args.fees} profit={listing.profit()}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    storage = Storage(args.file)
    listings = storage.load()
    if not listings:
        print("No listings found.")
        return 0
    print(f"{'ID':<4} {'Date':<11} {'Platform':<9} {'Cost':<8} {'Sale':<8} {'Fees':<8} {'Profit':<8}  Title")
    print("-" * 70)
    total_profit = 0.0
    for listing in listings:
        print(
            f"{listing.id:<4} {listing.sale_date:<11} {listing.platform:<9} "
            f"{listing.cost:<8.2f} {listing.sale_price:<8.2f} {listing.fees:<8.2f} "
            f"{listing.profit():<8.2f}  {listing.title}"
        )
        total_profit += listing.profit()
    print("-" * 70)
    print(f"{'':<44}Total profit: {total_profit:.2f}")
    return 0


def cmd_profit(args: argparse.Namespace) -> int:
    storage = Storage(args.file)
    listings = storage.load()
    totals = storage.monthly_totals(listings)
    if not totals:
        print("No listings found.")
        return 0
    print(f"{'Month':<8} {'Listings':<10} {'Revenue':<10} {'Costs':<10} {'Fees':<10} {'Profit':<10}")
    print("-" * 60)
    grand_profit = 0.0
    for month in totals:
        print(
            f"{month.month:<8} {month.listings:<10} {month.revenue:<10.2f} "
            f"{month.costs:<10.2f} {month.fees:<10.2f} {month.profit:<10.2f}"
        )
        grand_profit += month.profit
    print("-" * 60)
    print(f"{'':<40}Grand total profit: {grand_profit:.2f}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    storage = Storage(args.file)
    listings = storage.load()
    if args.format == "csv":
        storage.export_csv(args.output, listings)
        print(f"Exported {len(listings)} listings to CSV: {args.output}")
    else:
        data = [l.to_dict() for l in listings]
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        print(f"Exported {len(listings)} listings to JSON: {args.output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resale-tracker",
        description="Local-first profit tracker for eBay/Amazon resellers.",
    )
    parser.add_argument(
        "--file", default="listings.json", help="Local JSON data file (default: listings.json)"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new listing")
    p_add.add_argument("title", help="Item title")
    p_add.add_argument("platform", choices=["ebay", "amazon"], help="Marketplace")
    p_add.add_argument("cost", type=float, help="Your cost for the item")
    p_add.add_argument("sale_price", type=float, help="Sale price")
    p_add.add_argument("--shipping-cost", type=float, default=0.0, help="Your shipping cost")
    p_add.add_argument("--shipping-charged", type=float, default=0.0, help="Shipping charged to buyer")
    p_add.add_argument("--fees", type=float, default=None, help="Override auto-calculated fees")
    p_add.add_argument("--sale-date", default=None, help="Sale date YYYY-MM-DD (default: today)")
    p_add.add_argument("--notes", default="", help="Notes")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all items with profit")
    p_list.set_defaults(func=cmd_list)

    p_profit = sub.add_parser("profit", help="Monthly profit totals")
    p_profit.set_defaults(func=cmd_profit)

    p_export = sub.add_parser("export", help="Export to JSON or CSV")
    p_export.add_argument("format", choices=["json", "csv"], help="Export format")
    p_export.add_argument("output", help="Output file path")
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

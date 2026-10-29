# Resale Profit Tracker CLI

A local-first, no-keys Python command-line tool for eBay/Amazon resellers to log
items, costs, fees, and sales, and compute profit per listing plus monthly
totals, with local JSON and CSV export.

Built and maintained by **Asdale Dynamics, LLC** (Indiana, formed Oct 2026) —
beginner-friendly AI education, books and guides, and practical tools the LLC
can publish or sell. Credit to Asdale Dynamics, LLC.

## What it does

- Log a listing: title, platform (eBay or Amazon), cost, sale price, shipping, fees, sale date, notes
- Auto-calculate platform fees (eBay final value + per-order; Amazon referral + closing + FBA)
- View all listings with per-item profit
- View monthly profit totals and grand totals
- Export data to JSON or CSV
- All data stays local in a JSON file — no accounts, no API keys, no network

## Install

```bash
git clone <this-repo>
cd resale-profit-tracker-cli
pip install -e .
```

Or run without installing:

```bash
python3 -m resale_tracker.cli --help
```

## Usage

Add a listing (fees auto-calculated):

```bash
resale-tracker add "Vintage camera" ebay 45.00 89.99 --shipping-charged 12.00
```

Override the auto-fees:

```bash
resale-tracker add "Textbook" amazon 12.00 24.99 --fees 5.00 --sale-date 2026-10-15
```

List every item with profit:

```bash
resale-tracker list
```

Monthly totals:

```bash
resale-tracker profit
```

Export:

```bash
resale-tracker export csv listings.csv
resale-tracker export json backup.json
```

Specify a different data file with `--file`:

```bash
resale-tracker --file 2026-10.json list
```

## Fee math

Default rates are planning estimates, not platform quotes:

- eBay: 13.25% final value fee on sale price + $0.30 per order + 13.25% on shipping charged
- Amazon: 15% referral fee on sale price + optional closing fee + optional FBA fee

Override rates or pass `--fees` to match your actual invoices.

## Tests

```bash
python3 -m unittest discover tests
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.

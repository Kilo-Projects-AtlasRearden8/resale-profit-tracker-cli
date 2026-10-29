# STATUS

## What was built

A local-first Python CLI for eBay/Amazon resellers (`resale-profit-tracker-cli`) that logs items, costs, fees, and sales, computes profit per listing, and aggregates monthly totals, with local JSON and CSV export.

Files:
- `resale_tracker/models.py` — `Listing` and `MonthlyTotal` dataclasses; `Listing.profit()` computes sale + shipping charged − cost − shipping cost − fees
- `resale_tracker/fees.py` — `ebay_fees()` (final value % + per-order + shipping %) and `amazon_fees()` (referral % + closing + FBA), all overridable
- `resale_tracker/storage.py` — `Storage`: JSON read/write, CSV export, monthly rollups
- `resale_tracker/cli.py` — argparse CLI: `add`, `list`, `profit`, `export` (json|csv), `--file` for alternate data files
- `tests/test_fees.py` — 8 unittest cases covering default/custom rates, shipping, and rounding
- `pyproject.toml` — setuptools packaging with `resale-tracker` console script
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — usage docs, credits Asdale Dynamics, LLC
- `.gitignore` — pycache, egg-info, dist, default data file

Local-first by design: all data stays in a local JSON file; no accounts, API keys, secrets, or network access.

## How to run

```bash
cd /workspace/kilo-lab/resale-profit-tracker-cli
python3 -m resale_tracker.cli --help

python3 -m resale_tracker.cli add "Vintage camera" ebay 45.00 89.99 --shipping-charged 12.00
python3 -m resale_tracker.cli add "Textbook" amazon 12.00 24.99 --fees 5.00 --sale-date 2026-09-14
python3 -m resale_tracker.cli list
python3 -m resale_tracker.cli profit
python3 -m resale_tracker.cli export csv listings.csv
```

Install with `pip install -e .` for the `resale-tracker` command (blocked in this sandbox by PEP 668 externally-managed Python; module invocation works fine).

## Verification results

- `python3 -m unittest discover tests`: **8/8 OK**
- CLI exercised end-to-end: `add` (ebay auto-fees + amazon override), `list`, `profit` (monthly + grand total), `export csv` and `export json` — all produce correct output
- `pyproject.toml` parses; `resale-tracker = resale_tracker.cli:main` entry point valid
- Package imports cleanly under Python 3.13.5

## Known gaps

- No edit/delete of existing listings (append-only JSON store)
- Fee rates are planning estimates, not live platform data (intentional: no API keys)
- Float arithmetic; cents rounded at display/calculation boundaries
- Console script `resale-tracker` not installed in this sandbox due to PEP 668; run via `python3 -m resale_tracker.cli`
- No GUI, web UI, or sync; single-user local file

## Git

Commit `b8cff01` "Initial release: resale profit tracker CLI" on branch `master`, identity Dylan Asdale <dylanasdale@users.noreply.github.com>. Not pushed; no remote created.

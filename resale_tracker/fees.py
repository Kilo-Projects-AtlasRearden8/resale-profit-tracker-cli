"""Fee calculations for eBay and Amazon resale listings.

All rates are defaults and can be overridden per call. These are planning
estimates, not quotes from the platforms. Verify against your own seller
invoices before making business decisions.
"""

from __future__ import annotations


def ebay_fees(
    sale_price: float,
    final_value_rate: float = 0.1325,
    per_order_fee: float = 0.30,
    shipping_charged: float = 0.0,
    shipping_rate: float = 0.1325,
) -> float:
    """Estimate eBay total fees.

    Charges a final value fee on the sale price plus a per-order fee, and a
    final value fee on the shipping amount charged to the buyer.
    """
    sale_fee = round(sale_price * final_value_rate, 2)
    shipping_fee = round(shipping_charged * shipping_rate, 2)
    return round(sale_fee + per_order_fee + shipping_fee, 2)


def amazon_fees(
    sale_price: float,
    referral_rate: float = 0.15,
    closing_fee: float = 0.0,
    fba_fee: float = 0.0,
) -> float:
    """Estimate Amazon total fees.

    Charges a referral fee on the sale price plus an optional per-item closing
    fee (e.g. media) and an optional FBA fulfillment fee.
    """
    referral_fee = round(sale_price * referral_rate, 2)
    return round(referral_fee + closing_fee + fba_fee, 2)

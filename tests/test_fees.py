"""Tests for fee math in resale_tracker.fees."""

import unittest

from resale_tracker.fees import amazon_fees, ebay_fees


class TestEbayFees(unittest.TestCase):
    def test_default_fees(self):
        self.assertEqual(ebay_fees(100.0), 13.25 + 0.30)

    def test_shipping_fee_applies(self):
        self.assertEqual(ebay_fees(100.0, shipping_charged=20.0), 13.25 + 2.65 + 0.30)

    def test_custom_rates(self):
        self.assertEqual(ebay_fees(100.0, final_value_rate=0.10, per_order_fee=0.0), 10.0)

    def test_rounding(self):
        self.assertEqual(ebay_fees(19.99), round(round(19.99 * 0.1325, 2) + 0.30, 2))


class TestAmazonFees(unittest.TestCase):
    def test_default_fees(self):
        self.assertEqual(amazon_fees(100.0), 15.0)

    def test_with_closing_and_fba(self):
        self.assertEqual(amazon_fees(100.0, closing_fee=1.80, fba_fee=5.00), 21.80)

    def test_custom_rate(self):
        self.assertEqual(amazon_fees(200.0, referral_rate=0.10), 20.0)

    def test_rounding(self):
        self.assertEqual(amazon_fees(19.99), round(19.99 * 0.15, 2))


if __name__ == "__main__":
    unittest.main()

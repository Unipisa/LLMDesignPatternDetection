from data.dataset.refactored.ledger_refactored_proxy import *
import unittest

class TestLedgerProxy(unittest.TestCase):
    def test_creation(self):
        proxy = LedgerProxy()
        self.assertIsNone(proxy.db)

    def test_first_call(self):
        proxy = LedgerProxy()
        x = proxy.get_block(10333)
        self.assertIsNotNone(proxy.db)

    def test_correctness(self):
        proxy = LedgerProxy()
        x = proxy.get_block(10333)
        self.assertEqual(x, "transaction_10333")

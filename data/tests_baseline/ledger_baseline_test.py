from data.baseline.ledger_baseline import *
import unittest

class TestLedgerDB(unittest.TestCase,):
    def test_ledger(self):
        ledger = LedgerDB()
        self.assertIsNotNone(ledger.heavy_db)
    def test_get_block(self):
        ledger = LedgerDB()
        self.assertEqual(ledger.get_block(10333), "transaction_10333")

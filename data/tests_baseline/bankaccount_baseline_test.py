import unittest
from data.baseline.bankaccount_baseline import BankAccount, TransactionManager

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account1 = BankAccount(100)
    def test_withdraw(self):
        self.account1.withdraw(50)
        self.assertEqual(str(self.account1), "Balance: 50")
    def test_withdraw_with_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account1.withdraw(150)

    def test_deposit(self):
        self.account1.deposit(50)
        self.assertEqual(str(self.account1), "Balance: 150")

class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        self.manager = TransactionManager()
        self.account1 = BankAccount(100)
        self.account2 = BankAccount(200)
    def test_transfer(self):
        self.manager.transfer(self.account1, self.account2, 50)
        self.assertEqual(str(self.account1), "Balance: 50")
        self.assertEqual(str(self.account2), "Balance: 250")
    def test_tax_payment(self):
        self.manager.tax_payment(self.account2, 20)
        self.assertEqual(str(self.account2), "Balance: 180")
    def test_salary_deposit(self):
        self.manager.salary_deposit(self.account1, 200)
        self.assertEqual(str(self.account1), "Balance: 300")
    def test_transfer_with_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.manager.transfer(self.account1, self.account2, 150)
    def test_tax_payment_with_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.manager.tax_payment(self.account2, 1150)


if __name__ == "__main__":
    unittest.main()


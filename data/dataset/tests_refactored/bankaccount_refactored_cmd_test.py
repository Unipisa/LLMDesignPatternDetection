import unittest
from data.dataset.refactored.bankaccount_refactored_cmd import (BankAccount, Transaction, TransactionManager, Transfer, TaxPayment,
                                                        SalaryDeposit)

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
    def test_add_transaction(self):
        self.manager.add_transaction(Transfer(50, self.account1, self.account2))
        self.assertEqual(len(self.manager.transactions), 1)

    def test_execute_transactions(self):
        self.manager.add_transaction(TaxPayment(20, self.account2))
        self.manager.execute_transactions()
        self.assertEqual(str(self.account2), "Balance: 180")

    def test_undo_transactions(self):
        self.manager.add_transaction(Transfer(50, self.account1, self.account2))
        self.manager.execute_transactions()
        self.manager.undo_transactions()
        self.assertEqual(str(self.account1), "Balance: 100")
        self.assertEqual(str(self.account2), "Balance: 200")

class TestTransactions(unittest.TestCase):
    def test_transfer(self):
        account1 = BankAccount(100)
        account2 = BankAccount(200)
        transaction = Transfer(50, account1, account2)
        transaction.execute()
        self.assertEqual(str(account1), "Balance: 50")
        self.assertEqual(str(account2), "Balance: 250")
    def test_tax_payment(self):
        account = BankAccount(100)
        transaction = TaxPayment(20, account)
        transaction.execute()
        self.assertEqual(str(account), "Balance: 80")
    def test_salary_deposit(self):
        account = BankAccount(100)
        transaction = SalaryDeposit(200, account)
        transaction.execute()
        self.assertEqual(str(account), "Balance: 300")
    def test_salary_undo(self):
        account = BankAccount(100)
        transaction = SalaryDeposit(200, account)
        transaction.execute()
        transaction.undo()
        self.assertEqual(str(account), "Balance: 100")
    def test_transfer_undo(self):
        account1 = BankAccount(100)
        account2 = BankAccount(200)
        transaction = Transfer(50, account1, account2)
        transaction.execute()
        transaction.undo()
        self.assertEqual(str(account1), "Balance: 100")
        self.assertEqual(str(account2), "Balance: 200")
    def test_tax_payment_undo(self):
        account = BankAccount(100)
        transaction = TaxPayment(20, account)
        transaction.execute()
        transaction.undo()
        self.assertEqual(str(account), "Balance: 100")

if __name__ == "__main__":
    unittest.main()
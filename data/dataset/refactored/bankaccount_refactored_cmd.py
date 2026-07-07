from abc import ABC, abstractmethod
from typing import List

# management of bankaccount implemented with command pattern.
# These commands represent various types of transactions: bank transfer, tax payment, salary deposit
# Tries to enhance the power of rollback

# reciver
class BankAccount:
    def __init__(self, balance: int):
        self._balance = balance
    def withdraw(self, amount: int):    # withdraw money from the account
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
    def deposit(self, amount: int):     # deposit money into the account
        self._balance += amount
    def __str__(self):
        return f"Balance: {self._balance}"


# abstarct command
class Transaction(ABC):
    @abstractmethod
    def undo(self):
        pass
    @abstractmethod
    def execute(self):
        pass


# concrete commands
class Transfer(Transaction):
    def __init__(self, amount: int, from_account: BankAccount, to_account: BankAccount):
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
    def execute(self):
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
    def undo(self):
        self.to_account.withdraw(self.amount)
        self.from_account.deposit(self.amount)

class TaxPayment(Transaction):
    def __init__(self, amount: int, account: BankAccount):
        self.amount = amount
        self.account = account
    def execute(self):
        self.account.withdraw(self.amount)
    def undo(self):
        self.account.deposit(self.amount)

class SalaryDeposit(Transaction):
    def __init__(self, amount: int, account: BankAccount):
        self.amount = amount
        self.account = account
    def execute(self):
        self.account.deposit(self.amount)
    def undo(self):
        self.account.withdraw(self.amount)


# invoker
class TransactionManager:
    def __init__(self):
        self.transactions : List[Transaction]= []
        self.completed_transactions = []
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
    def execute_transactions(self):
        for transaction in self.transactions:
            try:
                transaction.execute()
            except Exception as e:
                self.undo_transactions()
                raise e
            self.completed_transactions.append(transaction)
        self.transactions.clear()
    def undo_transactions(self):
        for transaction in reversed(self.completed_transactions):   # LIFO order to undo
            try:
                transaction.undo()
            except Exception:
                raise Exception("Undo failed, inconsistent state")
        self.completed_transactions.clear()


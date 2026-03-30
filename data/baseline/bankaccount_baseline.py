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

class TransactionManager:
    def transfer(self, from_account, to_account, amount):
        from_account.withdraw(amount)
        to_account.deposit(amount)
    def tax_payment(self, account, amount):
        account.withdraw(amount)
    def salary_deposit(self, account, amount):
        account.deposit(amount)
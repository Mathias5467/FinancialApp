from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class Transaction:
    def __init__(self, amount: float, type: TransactionType, date: datetime = None, note: str = "Add note"):
        if not isinstance(type, TransactionType):
            raise ValueError("Type must be a TransactionType Enum")
        self.type = type
        self.amount = amount
        self.note = note
        self.date = date if date else datetime.now()
    
    def __repr__(self):
        return "Transaction {}: {} ({}) on {}".format(self.type.value, self.amount, self.note, self.date.strftime("%Y-%m-%d"))


class FinancialEntity:
    def __init__(self, name: str, image_path: str = None, current_amount: float = 0):
        self.name = name
        self.current_amount = current_amount
        self.image_path = image_path
        self.transactions = []

    def process_income(self, amount: float):
        self.current_amount += amount

    def process_expense(self, amount: float):
        self.current_amount -= amount

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        if transaction.type == TransactionType.INCOME:
            self.process_income(transaction.amount)
        else:
            self.process_expense(transaction.amount)

class Savings(FinancialEntity):
    def __init__(self, name: str, target_amount: float, image_path: str = "icons/money.png", current_amount: float = 0):
        super().__init__(name, image_path, current_amount)
        self.target_amount = target_amount

    def calculate_percent(self):
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_amount / self.target_amount) * 100)
    
class Budget(FinancialEntity):
    def __init__(self, name: str, image_path: str = "icons/money.png", current_amount: float = 0):
        super().__init__(name, image_path, current_amount)

    
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class Transaction:
    def __init__(self, amount: float, type: TransactionType, current_amount: float, date: datetime = None, note: str = "Add note"):
        if not isinstance(type, TransactionType):
            raise ValueError("Type must be a TransactionType Enum")
        self.type = type
        self.amount = amount
        self.note = note
        self.date = date if date else datetime.now()
        self.current_amount = current_amount
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "type": self.type.value,
            "current_amount": self.current_amount,
            "date": self.date.isoformat(),
            "note": self.note
        }


class FinancialEntity:
    def __init__(self, name: str, image_name: str = "money", current_amount: float = 0):
        self.name = name
        self.current_amount = current_amount
        self.image_name = image_name
        self.transactions = []

    @property
    def image_path(self):
        return f"icons/{self.image_name}.png"

    def to_dict(self):
        data = {
            "type": self.__class__.__name__,
            "name": self.name,
            "image_name": self.image_name, # Ukladáme len meno
            "current_amount": self.current_amount,
            "transactions": [t.to_dict() for t in self.transactions]
        }
        if hasattr(self, "target_amount"):
            data["target_amount"] = self.target_amount
        return data

    def process_income(self, amount: float):
        self.current_amount += amount

    def process_expense(self, amount: float):
        self.current_amount -= amount

    def get_current_amount(self):
        return self.current_amount
    
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

    
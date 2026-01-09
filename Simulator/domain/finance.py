# domain/finance.py

class Finance:
    def __init__(self):
        self.revenue = 0.0
        self.expenses = 0.0
        self.losses = 0.0

    def add_revenue(self, amount: float):
        self.revenue += amount

    def add_expense(self, amount: float):
        self.expenses += amount

    def add_loss(self, amount: float):
        self.losses += amount

    def net_profit(self) -> float:
        return self.revenue - self.expenses - self.losses

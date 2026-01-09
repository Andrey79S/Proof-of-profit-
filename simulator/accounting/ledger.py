class Ledger:
    def __init__(self):
        self.revenue = 0.0
        self.expenses = 0.0

        self.ingredients_used = 0.0
        self.energy_used = 0.0

    def add_revenue(self, value: float):
        self.revenue += value

    def add_expense(self, value: float):
        self.expenses += value

    @property
    def profit(self) -> float:
        return self.revenue - self.expenses

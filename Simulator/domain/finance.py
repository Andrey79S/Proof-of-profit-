#domain/finance.py

class Finance:
def init(self):
self.revenue = 0.0
self.expenses = 0.0
self.losses = 0.0

def profit(self) -> float:  
    return self.revenue - self.expenses - self.losses

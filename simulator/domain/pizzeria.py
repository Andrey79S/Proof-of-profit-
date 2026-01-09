class Pizzeria:
    def __init__(self, capacity_per_hour: int, ledger):
        self.capacity_per_hour = capacity_per_hour
        self.ledger = ledger

    def capacity(self, hours: float) -> int:
        return int(self.capacity_per_hour * hours)

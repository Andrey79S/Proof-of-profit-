class Pizzeria:
    def __init__(self, capacity_per_hour: int, reserve, ledger):
        self.capacity_per_hour = capacity_per_hour
        self.reserve = reserve
        self.ledger = ledger

    def production_capacity(self, hours: float) -> int:
        return int(self.capacity_per_hour * hours)

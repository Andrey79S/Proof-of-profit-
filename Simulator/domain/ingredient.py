class Ingredient:
    def __init__(self, name: str, amount: float, unit: str, expires_at: int):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.expires_at = expires_at

    def is_expired(self, now: int) -> bool:
        return now >= self.expires_at

    def consume(self, qty: float):
        if qty > self.amount:
            raise ValueError("Not enough ingredient")
        self.amount -= qty

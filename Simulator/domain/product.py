from dataclasses import dataclass

@dataclass
class Ingredient:
    name: str
    amount_kg: float = 0.0

    def consume(self, qty: float):
        if qty > self.amount_kg:
            raise ValueError(f"Недостаточно {self.name}: нужно {qty}, есть {self.amount_kg}")
        self.amount_kg -= qty

    def add(self, qty: float):
        self.amount_kg += qty

    def __repr__(self):
        return f"Ingredient({self.name}: {self.amount_kg} kg)"

@dataclass
class DoughBatch:
    amount_kg: float
    prepared_at_min: int
    expires_at_min: int

    def consume(self, qty: float):
        if qty > self.amount_kg:
            raise ValueError(f"Недостаточно теста: нужно {qty}, есть {self.amount_kg}")
        self.amount_kg -= qty

    def is_expired(self, now: int) -> bool:
        return now >= self.expires_at_min

    def __repr__(self):
        return f"DoughBatch({self.amount_kg} kg, prepared={self.prepared_at_min}, expires={self.expires_at_min})"

@dataclass
class Pizza:
    recipe: str
    price: float

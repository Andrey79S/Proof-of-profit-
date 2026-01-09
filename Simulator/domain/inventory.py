from typing import Dict, List
from domain.product import DoughBatch

class Inventory:
    def __init__(self):
        self.ingredients: Dict[str, float] = {}
        self.dough_batches: List[DoughBatch] = []

    def add_ingredient(self, name: str, amount: float):
        self.ingredients[name] = self.ingredients.get(name, 0.0) + amount

    def consume_ingredient(self, name: str, amount: float):
        current = self.ingredients.get(name, 0.0)
        if current < amount:
            raise ValueError(f"Недостаточно {name}: {current} < {amount}")
        self.ingredients[name] -= amount
        if self.ingredients[name] == 0:
            del self.ingredients[name]

    def add_dough_batch(self, batch: DoughBatch):
        self.dough_batches.append(batch)

    def consume_dough(self, amount: float, now: int):
        available = [b for b in self.dough_batches if not b.is_expired(now)]
        available.sort(key=lambda b: b.prepared_at_min)

        consumed = 0.0
        for batch in available:
            take = min(amount - consumed, batch.amount_kg)
            batch.amount_kg -= take
            consumed += take
            if batch.amount_kg == 0:
                self.dough_batches.remove(batch)
            if consumed >= amount:
                break
        if consumed < amount:
            raise ValueError("Недостаточно теста")

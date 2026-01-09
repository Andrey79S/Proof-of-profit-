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
        total = 0.0
        to_remove = []
        for i, batch in enumerate(self.dough_batches):
            if batch.is_expired(now):
                to_remove.append(i)
                continue
            take = min(amount - total, batch.amount_kg)
            batch.amount_kg -= take
            total += take
            if batch.amount_kg == 0:
                to_remove.append(i)
            if total >= amount:
                break
        for i in sorted(to_remove, reverse=True):
            del self.dough_batches[i]
        if total < amount:
            raise ValueError("Недостаточно теста")

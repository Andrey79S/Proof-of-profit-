from typing import Dict
from domain.product import Ingredient, DoughBatch

class Inventory:
    def __init__(self):
        self.ingredients: Dict[str, Ingredient] = {}
        self.dough_batches: list[DoughBatch] = []

    def add_ingredient(self, name: str, amount_kg: float):
        if name not in self.ingredients:
            self.ingredients[name] = Ingredient(name)
        self.ingredients[name].add(amount_kg)

    def consume_ingredient(self, name: str, amount_kg: float):
        if name in self.ingredients:
            self.ingredients[name].consume(amount_kg)
        else:
            raise ValueError(f"{name} не в инвентаре")

    def add_dough_batch(self, batch: DoughBatch):
        self.dough_batches.append(batch)

    def consume_dough(self, amount_kg: float, now: int) -> float:
        # Сортируем по сроку годности (FIFO + не истёкшие)
        self.dough_batches = [b for b in self.dough_batches if not b.is_expired(now)]
        self.dough_batches.sort(key=lambda b: b.prepared_at_min)
        consumed = 0.0
        while consumed < amount_kg and self.dough_batches:
            batch = self.dough_batches[0]
            take = min(amount_kg - consumed, batch.amount_kg)
            batch.consume(take)
            consumed += take
            if batch.amount_kg == 0:
                self.dough_batches.pop(0)
        if consumed < amount_kg:
            raise ValueError("Недостаточно теста")
        return consumed

    def check_spoilage(self, now: int) -> float:
        spoiled = [b for b in self.dough_batches if b.is_expired(now)]
        losses = sum(b.amount_kg for b in spoiled)
        self.dough_batches = [b for b in self.dough_batches if not b.is_expired(now)]
        # TODO: Для ингредиентов добавить lifetime из config
        return losses

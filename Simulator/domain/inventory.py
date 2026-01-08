import random
from typing import Dict
from domain.product import Ingredient, DoughBatch

class Inventory:
    def __init__(self):
        self.ingredients: Dict[str, Ingredient] = {}  # основной холодильник
        self.table_ingredients: Dict[str, Ingredient] = {}  # стол-холодильник
        self.dough_batches: list[DoughBatch] = []  # расстоечный холодильник
        self.table_dough: list[DoughBatch] = []  # тесто на столе

    def add_ingredient(self, name: str, amount_kg: float):
        if name not in self.ingredients:
            self.ingredients[name] = Ingredient(name)
        self.ingredients[name].add(amount_kg)

    def consume_ingredient(self, name: str, amount_kg: float):
        # Сначала со стола, потом из холодильника
        if name in self.table_ingredients and self.table_ingredients[name].amount_kg >= amount_kg:
            self.table_ingredients[name].consume(amount_kg)
            return
        if name in self.ingredients:
            self.ingredients[name].consume(amount_kg)
        else:
            raise ValueError(f"Недостаточно {name}")

    def add_dough_batch(self, batch: DoughBatch):
        self.dough_batches.append(batch)

    def consume_dough(self, amount_kg: float, now: int):
        # Со стола + из холодильника (готовое)
        batches = self.table_dough + self.dough_batches
        batches = [b for b in batches if not b.is_expired(now)]
        batches.sort(key=lambda b: b.prepared_at_min)

        consumed = 0.0
        for batch in batches:
            take = min(amount_kg - consumed, batch.amount_kg)
            batch.consume(take)
            consumed += take
            if batch.amount_kg == 0:
                if batch in self.table_dough:
                    self.table_dough.remove(batch)
                if batch in self.dough_batches:
                    self.dough_batches.remove(batch)
            if consumed >= amount_kg:
                break
        if consumed < amount_kg:
            raise ValueError("Недостаточно теста")
        return consumed

    def check_spoilage(self, now: int) -> float:
        spoiled = 0.0
        # Тесто
        self.dough_batches = [b for b in self.dough_batches if not b.is_expired(now)]
        self.table_dough = [b for b in self.table_dough if not b.is_expired(now)]
        # Ингредиенты (простая модель)
        for ing in list(self.table_ingredients.values()):
            if random.random() < 0.05:  # 5% шанс порчи на столе
                loss = ing.amount_kg * 0.2
                ing.consume(loss)
                spoiled += loss
        return spoiled

    def start_shift(self, now: int):
        # Перенос готового теста на стол
        ready = [b for b in self.dough_batches if now - b.prepared_at_min >= 720]
        self.table_dough.extend(ready)
        self.dough_batches = [b for b in self.dough_batches if b not in ready]

        # Перенос ингредиентов на стол
        for name, ing in list(self.ingredients.items()):
            transfer = min(ing.amount_kg * 0.3, 20.0)
            if transfer > 0:
                ing.consume(transfer)
                if name not in self.table_ingredients:
                    self.table_ingredients[name] = Ingredient(name)
                self.table_ingredients[name].add(transfer)

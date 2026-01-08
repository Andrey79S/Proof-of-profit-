from typing import Dict
from domain.product import Ingredient, DoughBatch

class Inventory:
    def __init__(self):
        self.ingredients: Dict[str, Ingredient] = {}  # общий холодильник
        self.table_ingredients: Dict[str, Ingredient] = {}  # стол-холодильник (открытые)
        self.dough_batches: list[DoughBatch] = []  # расстоечный холодильник
        self.table_dough: list[DoughBatch] = []  # тесто на столе

    def add_ingredient(self, name: str, amount_kg: float):
        if name not in self.ingredients:
            self.ingredients[name] = Ingredient(name)
        self.ingredients[name].add(amount_kg)

    def consume_ingredient(self, name: str, amount_kg: float):
        # Сначала берём со стола, если нет — с холодильника
        if name in self.table_ingredients and self.table_ingredients[name].amount_kg >= amount_kg:
            self.table_ingredients[name].consume(amount_kg)
        elif name in self.ingredients:
            self.ingredients[name].consume(amount_kg)
        else:
            raise ValueError(f"{name} не в инвентаре")

    def add_dough_batch(self, batch: DoughBatch):
        self.dough_batches.append(batch)

    def consume_dough(self, amount_kg: float, now: int) -> float:
        # Сначала со стола, потом из холодильника
        batches = self.table_dough + self.dough_batches
        batches = [b for b in batches if not b.is_expired(now)]
        batches.sort(key=lambda b: b.prepared_at_min)

        consumed = 0.0
        i = 0
        while consumed < amount_kg and i < len(batches):
            batch = batches[i]
            take = min(amount_kg - consumed, batch.amount_kg)
            batch.consume(take)
            consumed += take
            if batch.amount_kg == 0:
                batches.pop(i)
            else:
                i += 1
        if consumed < amount_kg:
            raise ValueError("Недостаточно теста")
        # Обновляем списки
        self.table_dough = [b for b in batches if b in self.table_dough]
        self.dough_batches = [b for b in batches if b in self.dough_batches]
        return consumed

    def check_spoilage(self, now: int) -> float:
        # Порча теста
        spoiled_dough = [b for b in self.dough_batches + self.table_dough if b.is_expired(now)]
        losses_dough = sum(b.amount_kg for b in spoiled_dough)
        self.dough_batches = [b for b in self.dough_batches if not b.is_expired(now)]
        self.table_dough = [b for b in self.table_dough if not b.is_expired(now)]

        # Порча ингредиентов (пример: lifetime из equipment)
        losses_ing = 0.0
        for ing in list(self.ingredients.values()) + list(self.table_ingredients.values()):
            # Пока упрощённо — добавь lifetime для каждого
            if random.random() < 0.01:  # 1% шанс порчи в день
                losses_ing += ing.amount_kg * 0.1  # 10% порчи
                ing.amount_kg *= 0.9

        return losses_dough + losses_ing

    def start_shift(self, now: int):
        """Перенос на стол в начале смены"""
        # Перенос теста (если готово после расстойки)
        ready_dough = [b for b in self.dough_batches if now - b.prepared_at_min >= 720]  # 12 часов
        self.table_dough.extend(ready_dough)
        self.dough_batches = [b for b in self.dough_batches if b not in ready_dough]

        # Перенос ингредиентов (пример: 20% от запаса)
        for name, ing in self.ingredients.items():
            transfer = ing.amount_kg * 0.2
            ing.consume(transfer)
            if name not in self.table_ingredients:
                self.table_ingredients[name] = Ingredient(name)
            self.table_ingredients[name].add(transfer)

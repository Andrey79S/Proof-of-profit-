# domain/inventory.py

from collections import defaultdict
from domain.product import DoughBatch

class Ingredient:
    def __init__(self, name: str, amount_kg: float):
        self.name = name
        self.amount_kg = amount_kg

class Inventory:
    """
    Хранение ингредиентов и теста
    """
    def __init__(self):
        # Обычные ингредиенты
        self.ingredients = {}          # name -> Ingredient
        # Ингредиенты на столе (быстрый доступ для сборки)
        self.table_ingredients = {}    # name -> Ingredient

        # Тесто
        self.dough_batches = []        # в холодильнике
        self.table_dough = []          # на столе, готовое для сборки

    # ----------------------------------------
    # Добавление ингредиентов
    # ----------------------------------------
    def add_ingredient(self, name: str, amount_kg: float, to_table: bool = False):
        target = self.table_ingredients if to_table else self.ingredients
        if name in target:
            target[name].amount_kg += amount_kg
        else:
            target[name] = Ingredient(name, amount_kg)

    # ----------------------------------------
    # Списание ингредиентов
    # ----------------------------------------
    def consume_ingredient(self, name: str, amount_kg: float):
        # Сначала со стола
        table = self.table_ingredients.get(name)
        if table:
            if table.amount_kg >= amount_kg:
                table.amount_kg -= amount_kg
                return
            else:
                amount_kg -= table.amount_kg
                table.amount_kg = 0

        # Потом из основного склада
        main = self.ingredients.get(name)
        if main:
            if main.amount_kg >= amount_kg:
                main.amount_kg -= amount_kg
                return
            else:
                main.amount_kg = 0

        # Если не хватило, списываем сколько есть (Pizzeria проверяет can_accept_order перед cook)
    
    # ----------------------------------------
    # Добавление теста
    # ----------------------------------------
    def add_dough_batch(self, batch: DoughBatch, to_table: bool = False):
        if to_table:
            self.table_dough.append(batch)
        else:
            self.dough_batches.append(batch)

    # ----------------------------------------
    # Списание теста
    # ----------------------------------------
    def consume_dough(self, amount_kg: float, now_minute: int):
        # Сначала со стола
        self._consume_from_list(self.table_dough, amount_kg, now_minute)
    
    def _consume_from_list(self, batches: list, amount_kg: float, now_minute: int):
        i = 0
        while amount_kg > 0 and i < len(batches):
            batch = batches[i]
            if batch.is_expired(now_minute):
                i += 1
                continue
            if batch.amount_kg > amount_kg:
                batch.amount_kg -= amount_kg
                return
            else:
                amount_kg -= batch.amount_kg
                batch.amount_kg = 0
                i += 1
        # Очистка пустых партий
        batches[:] = [b for b in batches if b.amount_kg > 0]

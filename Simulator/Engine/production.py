# simulator/engine/production.py

import json
from collections import deque
import math


class Production:
    def __init__(self, config_folder="config"):
        # =========================
        # Загружаем ингредиенты и рецепты
        # =========================
        with open(f"{config_folder}/ingredients.json", encoding="utf-8") as f:
            self.ingredients_data = json.load(f)

        with open(f"{config_folder}/recipes.json", encoding="utf-8") as f:
            self.recipes = json.load(f)

        # =========================
        # Настройки теста
        # =========================
        self.dough_loss_pct = 0.02

        # тесто хранится партиями
        # каждый элемент: {"kg": float, "age": int}
        self.dough_batches = deque()

    # =========================
    # Стоимость ингредиентов
    # =========================
    def ingredient_cost(self, name, kg):
        return self.ingredients_data[name]["price_per_kg"] * kg

    def dough_cost(self, kg):
        cost = 0
        for ing, ratio in self.recipes["dough"].items():
            cost += self.ingredient_cost(ing, kg * ratio)
        return cost

    # =========================
    # Доступное тесто
    # =========================
    def available_dough(self):
        return sum(batch["kg"] for batch in self.dough_batches)

    # =========================
    # Списание теста
    # =========================
    def use_dough(self, kg):
        used = 0
        while kg > 0 and self.dough_batches:
            batch = self.dough_batches[0]
            take = min(batch["kg"], kg)
            batch["kg"] -= take
            kg -= take
            used += take
            if batch["kg"] <= 0:
                self.dough_batches.popleft()
        return used

    # =========================
    # Старение теста + порча
    # =========================
    def age_dough(self):
        spoiled = 0
        fresh = deque()
        for batch in self.dough_batches:
            batch["age"] += 1
            if batch["age"] > 2:
                spoiled += batch["kg"]
            else:
                fresh.append(batch)
        self.dough_batches = fresh
        return spoiled

    # =========================
    # Замес теста
    # =========================
    def mix_dough(self, kg):
        loss = kg * self.dough_loss_pct
        net = kg - loss
        self.dough_batches.append({"kg": net, "age": 0})
        return net, self.dough_cost(kg)

    # =========================
    # Проверка ингредиентов
    # =========================
    def check_ingredients(self, table_stock, recipe, count):
        for ing, kg_per_pizza in recipe.items():
            if ing == "dough":
                continue
            if table_stock.get(ing, 0) < kg_per_pizza * count:
                return False
        return True

    # =========================
    # Списание ингредиентов со стола
    # =========================
    def consume_ingredients(self, table_stock, recipe, count):
        cost = 0
        for ing, kg_per_pizza in recipe.items():
            if ing == "dough":
                continue
            total = kg_per_pizza * count
            table_stock[ing] -= total
            cost += self.ingredient_cost(ing, total)
        return cost

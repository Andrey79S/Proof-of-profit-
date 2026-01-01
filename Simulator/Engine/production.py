import json
import math
from collections import deque


class Production:
    def __init__(self):
        with open("simulator/config/ingredients.json", "r", encoding="utf-8") as f:
            self.ingredients = json.load(f)

        with open("simulator/config/recipes.json", "r", encoding="utf-8") as f:
            self.recipes = json.load(f)

        # =========================
        # НАСТРОЙКИ
        # =========================
        self.dough_fridge_capacity = 20.0  # кг
        self.ingredients_fridge_capacity = 20.0  # кг
        self.table_capacity = 5.0  # кг

        self.min_mix = 15.0
        self.max_mix = 35.0

        self.dough_loss_pct = 0.02
        self.ingredients_loss_pct = 0.01

        # =========================
        # СОСТОЯНИЕ (остатки)
        # =========================

        # тесто хранится партиями (кг, возраст_дней)
        self.dough_batches = deque()

        # холодильник ингредиентов
        self.ingredients_stock = {
            "tomato_sauce": 0.0,
            "mozzarella": 0.0,
            "pepperoni": 0.0
        }

        # стол
        self.table_stock = {
            "tomato_sauce": 0.0,
            "mozzarella": 0.0,
            "pepperoni": 0.0
        }

    # =========================
    # БАЗОВЫЕ ФУНКЦИИ
    # =========================

    def ingredient_cost(self, ingredient, kg):
        return self.ingredients[ingredient]["price_per_kg"] * kg

    # =========================
    # ТЕСТО
    # =========================

    def dough_cost(self, dough_kg):
        cost = 0.0
        for ing, ratio in self.recipes["dough"].items():
            cost += self.ingredient_cost(ing, dough_kg * ratio)
        return cost

    def available_dough(self):
        return sum(batch["kg"] for batch in self.dough_batches)

    def age_dough(self):
        """Увеличиваем возраст теста, списываем просрочку"""
        fresh_batches = deque()
        spoiled = 0.0

        for batch in self.dough_batches:
            batch["age"] += 1
            if batch["age"] > 2:
                spoiled += batch["kg"]
            else:
                fresh_batches.append(batch)

        self.dough_batches = fresh_batches
        return spoiled

    def mix_dough_if_needed(self, required_kg):
        produced = 0.0
        cost = 0.0
        mixes = 0

        while self.available_dough() < required_kg:
            mix_size = min(self.max_mix, self.dough_fridge_capacity - self.available_dough())
            if mix_size < self.min_mix:
                break

            loss = mix_size * self.dough_loss_pct
            net = mix_size - loss

            self.dough_batches.append({
                "kg": net,
                "age": 0
            })

            produced += net
            cost += self.dough_cost(mix_size)
            mixes += 1

        return {
            "mixes": mixes,
            "produced_kg": round(produced, 2),
            "cost": round(cost, 2)
        }

    # =========================
    # ИНГРЕДИЕНТЫ
    # =========================

    def load_ingredients(self, purchases: dict):
        cost = 0.0
        for ing, kg in purchases.items():
            self.ingredients_stock[ing] += kg
            cost += self.ingredient_cost(ing, kg)
        return cost

    def fill_table_from_fridge(self):
        for ing in self.table_stock:
            need = self.table_capacity - self.table_stock[ing]
            take = min(need, self.ingredients_stock[ing])
            self.ingredients_stock[ing] -= take
            self.table_stock[ing] += take

    # =========================
    # ПРОИЗВОДСТВО ПИЦЦЫ
    # =========================

    def produce_pizzas(self, margarita_qty, pepperoni_qty):
        report = {
            "produced": {"margarita": 0, "pepperoni": 0},
            "ingredient_cost": 0.0,
            "dough_used_kg": 0.0
        }

        pizza_queue = (
            ["pizza_margarita"] * margarita_qty +
            ["pizza_pepperoni"] * pepperoni_qty
        )

        for pizza in pizza_queue:
            recipe = self.recipes[pizza]

            # проверка теста
            if self.available_dough() < recipe["dough"]:
                break

            # проверка стола
            for ing, kg in recipe.items():
                if ing == "dough":
                    continue
                if self.table_stock.get(ing, 0) < kg:
                    return report

            # списываем тесто
            need = recipe["dough"]
            while need > 0:
                batch = self.dough_batches[0]
                take = min(batch["kg"], need)
                batch["kg"] -= take
                need -= take
                if batch["kg"] <= 0:
                    self.dough_batches.popleft()

            report["dough_used_kg"] += recipe["dough"]

            # списываем ингредиенты
            for ing, kg in recipe.items():
                if ing == "dough":
                    continue
                loss = kg * self.ingredients_loss_pct
                self.table_stock[ing] -= (kg + loss)
                report["ingredient_cost"] += self.ingredient_cost(ing, kg + loss)

            report["produced"][pizza.replace("pizza_", "")] += 1

        return report

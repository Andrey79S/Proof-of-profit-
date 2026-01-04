import json
from collections import deque

class Production:
    def __init__(self, config_folder="config"):
        with open(f"{config_folder}/ingredients.json", "r", encoding="utf-8") as f:
            self.ingredients = json.load(f)

        with open(f"{config_folder}/recipes.json", "r", encoding="utf-8") as f:
            self.recipes = json.load(f)

        # Настройки
        self.dough_fridge_capacity = 20.0  # кг
        self.table_capacity = 5.0  # кг
        self.min_mix = 15.0
        self.max_mix = 35.0
        self.dough_loss_pct = 0.02
        self.ingredients_loss_pct = 0.01

        # Состояние
        self.dough_batches = deque()  # тесто (kg, age_days)
        self.ingredients_stock = {ing: 0.0 for ing in self.ingredients}
        self.table_stock = {ing: 0.0 for ing in self.ingredients}

    # =========================
    # ТЕСТО
    # =========================
    def dough_cost(self, dough_kg):
        cost = 0.0
        for ing, ratio in self.recipes["dough"].items():
            cost += self.ingredients[ing]["price_per_kg"] * dough_kg * ratio
        return cost

    def available_dough(self):
        return sum(batch["kg"] for batch in self.dough_batches)

    def age_dough(self):
        fresh = deque()
        spoiled = 0.0
        for batch in self.dough_batches:
            batch["age"] += 1
            if batch["age"] > 2:
                spoiled += batch["kg"]
            else:
                fresh.append(batch)
        self.dough_batches = fresh
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
            self.dough_batches.append({"kg": net, "age": 0})
            produced += net
            cost += self.dough_cost(mix_size)
            mixes += 1
        return {"mixes": mixes, "produced_kg": round(produced, 2), "cost": round(cost, 2)}

    # =========================
    # ИНГРЕДИЕНТЫ
    # =========================
    def load_ingredients(self, purchases: dict):
        cost = 0.0
        for ing, kg in purchases.items():
            self.ingredients_stock[ing] += kg
            cost += self.ingredients[ing]["price_per_kg"] * kg
        return round(cost, 2)

    def fill_table_from_fridge(self):
        for ing in self.table_stock:
            need = self.table_capacity - self.table_stock[ing]
            take = min(need, self.ingredients_stock[ing])
            self.ingredients_stock[ing] -= take
            self.table_stock[ing] += take

    # =========================
    # ПРОИЗВОДСТВО ПИЦЦЫ
    # =========================
    def produce_pizza(self, pizza_name):
        recipe = self.recipes[pizza_name]

        # Проверка теста
        if self.available_dough() < recipe["dough"]:
            return False, 0.0

        # Проверка ингредиентов на столе
        for ing, kg in recipe.items():
            if ing == "dough":
                continue
            if self.table_stock.get(ing, 0) < kg:
                return False, 0.0

        # Списание теста
        need = recipe["dough"]
        while need > 0:
            batch = self.dough_batches[0]
            take = min(batch["kg"], need)
            batch["kg"] -= take
            need -= take
            if batch["kg"] <= 0:
                self.dough_batches.popleft()

        dough_used = recipe["dough"]

        # Списание ингредиентов
        ing_cost = 0.0
        for ing, kg in recipe.items():
            if ing == "dough":
                continue
            loss = kg * self.ingredients_loss_pct
            total_kg = kg + loss
            self.table_stock[ing] -= total_kg
            ing_cost += total_kg * self.ingredients[ing]["price_per_kg"]

        return True, round(ing_cost, 2)

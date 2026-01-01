import json
from collections import deque

class Production:
    def __init__(self, config_folder="config"):
        with open(f"{config_folder}/ingredients.json", "r", encoding="utf-8") as f:
            self.ingredients = json.load(f)

        with open(f"{config_folder}/recipes.json", "r", encoding="utf-8") as f:
            self.recipes = json.load(f)

        # параметры
        self.dough_loss_pct = 0.02
        self.ingredients_loss_pct = 0.01
        self.dough_batches = deque()  # тесто (kg, возраст)
        self.ingredients_stock = {k: 0 for k in self.ingredients}
        self.table_stock = {k: 0 for k in self.ingredients}

        self.max_table_load = 5.0  # кг
        self.min_table_pct = 0.3

    # =========================
    # Тесто
    # =========================
    def mix_dough(self, kg):
        loss = kg * self.dough_loss_pct
        net = kg - loss
        self.dough_batches.append({"kg": net, "age": 0})
        return net

    def available_dough(self):
        return sum(batch["kg"] for batch in self.dough_batches)

    def take_dough(self, kg):
        taken = 0
        while kg > 0 and self.dough_batches:
            batch = self.dough_batches[0]
            use = min(batch["kg"], kg)
            batch["kg"] -= use
            kg -= use
            taken += use
            if batch["kg"] <= 0:
                self.dough_batches.popleft()
        return taken

    # =========================
    # Ингредиенты
    # =========================
    def load_ingredients(self, purchases: dict):
        for ing, kg in purchases.items():
            self.ingredients_stock[ing] += kg

    def fill_table_from_fridge(self):
        for ing in self.table_stock:
            need = self.max_table_load - self.table_stock[ing]
            take = min(need, self.ingredients_stock[ing])
            self.ingredients_stock[ing] -= take
            self.table_stock[ing] += take

    # =========================
    # Производство пиццы
    # =========================
    def produce_pizza(self, pizza_name):
        recipe = self.recipes[pizza_name]

        # проверка теста
        dough_needed = recipe["dough"]
        if self.available_dough() < dough_needed:
            return False  # нет теста

        # проверка ингредиентов на столе
        for ing, kg in recipe.items():
            if ing == "dough":
                continue
            if self.table_stock.get(ing, 0) < kg:
                return False  # нет ингредиентов

        # списание теста
        self.take_dough(dough_needed)

        # списание ингредиентов
        for ing, kg in recipe.items():
            if ing == "dough":
                continue
            loss = kg * self.ingredients_loss_pct
            self.table_stock[ing] -= (kg + loss)

        return True

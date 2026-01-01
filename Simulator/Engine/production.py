# simulator/engine/production.py

import json

class Production:
    def __init__(self, config_folder="config"):
        with open(f"{config_folder}/ingredients.json", "r", encoding="utf-8") as f:
            self.ingredients = json.load(f)
        with open(f"{config_folder}/recipes.json", "r", encoding="utf-8") as f:
            self.recipes = json.load(f)
        with open(f"{config_folder}/prices.json", "r", encoding="utf-8") as f:
            self.prices = json.load(f)

    # =========================
    # Стоимость ингредиентов
    # =========================
    def ingredient_cost(self, ingredient, kg):
        return self.ingredients[ingredient]["price"] * kg

    def dough_cost(self, dough_kg):
        cost = 0.0
        for ing, ratio in self.recipes["dough"].items():
            cost += self.ingredient_cost(ing, dough_kg * ratio)
        return cost

    # =========================
    # Стоимость пиццы
    # =========================
    def pizza_cost(self, pizza_name):
        return self.prices[pizza_name]

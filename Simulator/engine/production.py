import json
import os

class Production:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria
        self.recipes = self._load_recipes()

    def _load_recipes(self):
        recipes = {}
        base = "config/recipes"
        for f in os.listdir(base):
            with open(f"{base}/{f}", "r") as file:
                data = json.load(file)
                recipes[f.replace(".json", "")] = data
        return recipes

    def can_cook(self, recipe_name: str) -> bool:
        recipe = self.recipes[recipe_name]
        inv = self.pizzeria.inventory

        for ing, qty in recipe["ingredients"].items():
            if not inv.has(ing, qty):
                return False
        return True

    def cook(self, order):
        recipe = self.recipes[order.recipe]
        inv = self.pizzeria.inventory

        # списываем ингредиенты
        for ing, qty in recipe["ingredients"].items():
            inv.consume(ing, qty)

        order.status = order.status.COOKING
        return recipe["cook_time"], recipe["price"]

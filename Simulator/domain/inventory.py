# domain/inventory.py
from domain.ingredient import Ingredient

class Inventory:
    def __init__(self):
        self.ingredients = {}

    def add_ingredient(self, ingredient: Ingredient):
        self.ingredients[ingredient.name] = ingredient

    def use_ingredient(self, name, amount):
        if name not in self.ingredients:
            raise ValueError(f"{name} нет в инвентаре")
        self.ingredients[name].remove(amount)

    def check_available(self, name, amount):
        return self.ingredients.get(name, Ingredient(name, 0)).quantity_kg >= amount

from domain.recipe import Recipe
from domain.inventory import Inventory

class Kitchen:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory

    def can_cook(self, recipe: Recipe) -> bool:
        for name, qty in recipe.ingredients.items():
            if self.inventory.total(name) < qty:
                return False
        return True

    def cook(self, recipe: Recipe):
        if not self.can_cook(recipe):
            raise ValueError("Cannot cook: insufficient ingredients")
        for name, qty in recipe.ingredients.items():
            self.inventory.consume(name, qty)

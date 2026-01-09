from domain.pizzeria import Pizzeria

class ProductionEngine:
    def __init__(self, pizzeria: Pizzeria):
        self.pizzeria = pizzeria

    def cook(self, recipe: str):
        self.pizzeria.cook(recipe)

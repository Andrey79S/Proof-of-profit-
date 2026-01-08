from domain.pizzeria import Pizzeria

class Procurement:
    def __init__(self, pizzeria: Pizzeria):
        self.pizzeria = pizzeria

    def order_ingredients(self, ingredients: dict[str, float]):
        for name, qty in ingredients.items():
            self.pizzeria.inventory.add_ingredient(name, qty)
        # Добавить расходы: self.pizzeria.expenses += cost

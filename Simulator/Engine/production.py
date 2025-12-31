import json

class Production:
    def __init__(self):
        with open("simulator/config/ingredients.json") as f:
            self.ingredients = json.load(f)
        with open("simulator/config/recipes.json") as f:
            self.recipes = json.load(f)

    def ingredient_cost(self, ingredient, kg):
        return self.ingredients[ingredient]["price_per_kg"] * kg

    def pizza_cost(self, recipe):
        cost = 0
        for ing, kg in recipe.items():
            cost += self.ingredient_cost(ing, kg)
        return cost

    def make_pizzas(self, margarita_qty, pepperoni_qty):
        margarita_cost = self.pizza_cost(self.recipes["pizza_margarita"])
        pepperoni_cost = self.pizza_cost(self.recipes["pizza_pepperoni"])
        return margarita_cost * margarita_qty + pepperoni_cost * pepperoni_qty

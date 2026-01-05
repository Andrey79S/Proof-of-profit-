import json

class Production:
    def __init__(self, equipment, ingredients, recipes):
        self.equipment = equipment
        self.ingredients = ingredients
        self.recipes = recipes
        self.total_dough_kg = 0
        self.energy_used = 0

    def make_dough(self, kg):
        recipe = self.recipes["dough"]
        for ing, amount in recipe.items():
            needed = amount * kg
            if self.ingredients[ing]["stock_kg"] < needed:
                return False
            self.ingredients[ing]["stock_kg"] -= needed
            self.energy_used += self.equipment["dough_mixer"].power_kw * self.equipment["dough_mixer"].time_min / 60
        self.total_dough_kg += kg
        return True

    def can_make_pizza(self, pizza_name, quantity):
        recipe = self.recipes[pizza_name]
        for ing, amount in recipe.items():
            if ing == "dough":
                if self.total_dough_kg < amount * quantity:
                    return False
            else:
                if self.ingredients[ing]["stock_kg"] < amount * quantity:
                    return False
        return True

    def make_pizza(self, pizza_name, quantity):
        if not self.can_make_pizza(pizza_name, quantity):
            return 0
        recipe = self.recipes[pizza_name]
        for ing, amount in recipe.items():
            if ing == "dough":
                self.total_dough_kg -= amount * quantity
            else:
                self.ingredients[ing]["stock_kg"] -= amount * quantity
        # энергия на выпечку
        total_capacity = sum(o.capacity for o in self.equipment.values() if hasattr(o, "capacity"))
        total_bake_time = max(o.bake_time_min for o in self.equipment.values() if hasattr(o, "bake_time_min"))
        self.energy_used += sum(o.power_kw for o in self.equipment.values() if hasattr(o, "power_kw")) * total_bake_time / 60
        return quantity

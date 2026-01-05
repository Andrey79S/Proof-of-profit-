from engine.production import Production
from engine.equipment import DoughMixer, Oven
import json

class Pizzeria:
    def __init__(self, name, equipment_config, ingredients_config, recipes_config):
        self.name = name
        self.total_pizzas = {}
        self.total_orders = 0
        self.total_costs = 0
        self.energy_used = 0

        # загрузка конфигов
        with open(equipment_config, "r", encoding="utf-8") as f:
            eq_data = json.load(f)
        with open(ingredients_config, "r", encoding="utf-8") as f:
            ingredients = json.load(f)
        with open(recipes_config, "r", encoding="utf-8") as f:
            recipes = json.load(f)

        self.equipment = {}
        for key, val in eq_data.items():
            if "bake_time_min" in val:
                self.equipment[key] = Oven(**val)
            else:
                self.equipment[key] = DoughMixer(**val)

        self.production = Production(self.equipment, ingredients, recipes)

    def process_orders(self, orders):
        for pizza_name, quantity in orders.items():
            made = self.production.make_pizza(pizza_name, quantity)
            self.total_pizzas[pizza_name] = self.total_pizzas.get(pizza_name, 0) + made
            self.total_orders += quantity

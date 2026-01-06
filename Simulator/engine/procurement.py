# engine/procurement.py
import random

class Procurement:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def order_ingredients(self, ingredient_list):
        # доставляем через фиксированное время (1 минута в игре)
        for name, qty in ingredient_list.items():
            self.pizzeria.inventory.add(name, qty)

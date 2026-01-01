from engine.production import Production
from datetime import datetime
import random

class Pizzeria:
    def __init__(self, config_folder="config"):
        self.production = Production(config_folder)
        self.total_orders = 0
        self.total_pizzas = {"margarita": 0, "pepperoni": 0}

        # для простоты: минимальные закупки
        self.min_ingredients = {
            "tomato_sauce": 2.0,
            "mozzarella": 2.0,
            "pepperoni": 1.0
        }

    # =========================
    # Сессия: старт дня
    # =========================
    def start_day(self):
        # замес теста 20 кг в день
        self.production.mix_dough(20)

        # закупка ингредиентов при низком уровне
        purchases = {}
        for ing, min_qty in self.min_ingredients.items():
            if self.production.ingredients_stock[ing] < min_qty:
                purchases[ing] = min_qty * 2
        self.production.load_ingredients(purchases)

        # заполнение стола
        self.production.fill_table_from_fridge()

    # =========================
    # Заказы
    # =========================
    def generate_orders(self, orders_per_day):
        orders = []
        for _ in range(orders_per_day):
            pizza_type = random.choice(["pizza_margarita", "pizza_pepperoni"])
            quantity = random.randint(1, 4)
            orders.append({"pizza": pizza_type, "quantity": quantity})
        return orders

    def process_order(self, order):
        produced = 0
        for _ in range(order["quantity"]):
            success = self.production.produce_pizza(order["pizza"])
            if success:
                produced += 1
            else:
                break
        if produced > 0:
            pizza_name = order["pizza"].replace("pizza_", "")
            self.total_pizzas[pizza_name] += produced
            self.total_orders += 1
        return produced

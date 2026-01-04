from engine.production import Production

class Pizzeria:
    def __init__(self, config_folder="config"):
        self.production = Production(config_folder)
        self.total_energy_kwh = 0.0
        self.total_sales = 0.0
        self.total_orders = 0
        self.total_pizzas = {"Margarita": 0, "Pepperoni": 0}

        # Цена продажи пиццы
        self.prices = {"Margarita": 10.0, "Pepperoni": 15.0}

        # Энергия за день (печь + холодильники + стол + тестомес)
        self.daily_energy_kwh = 12 * (8 + 0.5 + 0.25 + 3)  # грубо

    def process_orders_day(self, orders_count):
    import random

    report = {
        "pizzas": {"Margarita": 0, "Pepperoni": 0},
        "ingredient_cost": 0.0,
        "energy_kwh": 0.0
    }

    for _ in range(orders_count):
        pizza_type = random.choice(["Margarita", "Pepperoni"])

        result = self.production.make_pizza(pizza_type)

        if not result["success"]:
            # нет теста или ингредиентов → заказ потерян
            continue

        # статистика
        report["pizzas"][pizza_type] += 1
        report["ingredient_cost"] += result["ingredient_cost"]
        report["energy_kwh"] += result["energy_kwh"]

        self.total_sales += result["price"]
        self.total_orders += 1
        self.total_pizzas[pizza_type] += 1

    return report
        }

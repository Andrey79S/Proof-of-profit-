from engine.production import Production


class Pizzeria:
    def __init__(self, config):
        self.config = config

        # Производственный модуль
        self.production = Production(config)

        # Общая статистика
        self.total_orders = 0
        self.total_sales = 0.0

        self.total_pizzas = {
            "Margarita": 0,
            "Pepperoni": 0
        }

        self.total_ingredient_cost = 0.0
        self.total_energy_kwh = 0.0

    def process_orders_day(self, orders_count):
        """
        Обрабатывает заказы за один день
        """
        import random

        day_report = {
            "pizzas": {
                "Margarita": 0,
                "Pepperoni": 0
            },
            "ingredient_cost": 0.0,
            "energy_kwh": 0.0,
            "revenue": 0.0
        }

        for _ in range(orders_count):
            pizza_type = random.choice(["Margarita", "Pepperoni"])

            result = self.production.make_pizza(pizza_type)

            if not result["success"]:
                continue

            # Дневная статистика
            day_report["pizzas"][pizza_type] += 1
            day_report["ingredient_cost"] += result["ingredient_cost"]
            day_report["energy_kwh"] += result["energy_kwh"]
            day_report["revenue"] += result["price"]

            # Общая статистика
            self.total_orders += 1
            self.total_sales += result["price"]
            self.total_pizzas[pizza_type] += 1
            self.total_ingredient_cost += result["ingredient_cost"]
            self.total_energy_kwh += result["energy_kwh"]

        return day_report

    def summary(self):
        """
        Финальный отчёт по симуляции
        """
        profit = self.total_sales - self.total_ingredient_cost

        return {
            "orders": self.total_orders,
            "pizzas": self.total_pizzas,
            "revenue": round(self.total_sales, 2),
            "ingredient_cost": round(self.total_ingredient_cost, 2),
            "energy_kwh": round(self.total_energy_kwh, 2),
            "profit": round(profit, 2)
            }

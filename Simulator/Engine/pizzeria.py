import json
import os
from engine.production import Production


class Pizzeria:
    def __init__(self, config_folder="config"):
        self.config = self._load_config(config_folder)

        # Производство
        self.production = Production(self.config)

        # Общая статистика
        self.total_orders = 0
        self.total_sales = 0.0

        self.total_pizzas = {
            "Margarita": 0,
            "Pepperoni": 0
        }

        self.total_ingredient_cost = 0.0
        self.total_energy_kwh = 0.0

    def _load_config(self, folder):
        """
        Загружает все JSON-конфиги из папки config
        """
        config = {}
        base_path = os.path.abspath(folder)

        for file_name in os.listdir(base_path):
            if file_name.endswith(".json"):
                key = file_name.replace(".json", "").lower()
                with open(os.path.join(base_path, file_name), "r") as f:
                    config[key] = json.load(f)

        return config

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
        Финальный отчёт
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

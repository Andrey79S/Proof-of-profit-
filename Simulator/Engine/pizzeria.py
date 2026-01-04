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

    def process_orders_day(self, orders_per_day):
        pizzas_made = {"Margarita": 0, "Pepperoni": 0}
        ingredient_cost_total = 0.0
        self.production.fill_table_from_fridge()

        for _ in range(orders_per_day):
            # Случайный заказ 1-4 пиццы
            import random
            qty = random.randint(1, 4)
            for _ in range(qty):
                pizza_name = random.choice(["pizza_margarita", "pizza_pepperoni"])
                success, ing_cost = self.production.produce_pizza(pizza_name)
                if success:
                    pizzas_made[pizza_name.replace("pizza_", "").capitalize()] += 1
                    ingredient_cost_total += ing_cost
                    self.total_sales += self.prices[pizza_name.replace("pizza_", "").capitalize()]
                self.total_orders += 1

        self.total_pizzas["Margarita"] += pizzas_made["Margarita"]
        self.total_pizzas["Pepperoni"] += pizzas_made["Pepperoni"]
        self.total_energy_kwh += self.daily_energy_kwh

        return {
            "ingredient_cost": round(ingredient_cost_total, 2),
            "energy_kwh": round(self.daily_energy_kwh, 2),
            "pizzas": pizzas_made
        }

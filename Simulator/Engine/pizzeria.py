from engine.production import Production
from engine.energy import Energy


class Pizzeria:
    def __init__(self, working_hours=12):
        self.production = Production()
        self.energy = Energy(working_hours)

    def simulate_day(self, margarita_qty, pepperoni_qty, ingredient_purchases):
        day_log = {}

        # 1️⃣ Старение теста
        spoiled_dough = self.production.age_dough()
        day_log["spoiled_dough_kg"] = round(spoiled_dough, 2)

        # 2️⃣ Сколько нужно теста
        dough_needed = (
            self.production.dough_required_for_pizzas(
                margarita_qty, pepperoni_qty
            )
        )

        # 3️⃣ Замес при необходимости
        mixing_report = self.production.mix_dough_if_needed(dough_needed)
        day_log["mixing"] = mixing_report

        # 4️⃣ Закупка ингредиентов
        ingredients_cost = self.production.load_ingredients(
            ingredient_purchases
        )
        day_log["ingredients_purchase_cost"] = round(ingredients_cost, 2)

        # 5️⃣ Наполнение стола
        self.production.fill_table_from_fridge()

        # 6️⃣ Производство пиццы
        production_report = self.production.produce_pizzas(
            margarita_qty, pepperoni_qty
        )
        day_log["production"] = production_report

        # 7️⃣ Энергия
        energy_cost = self.energy.total_energy(
            mixing_report["produced_kg"]
        )

        # 8️⃣ Выручка
        revenue = margarita_qty * 10 + pepperoni_qty * 14

        # 9️⃣ Итоги
        total_cost = (
            mixing_report["cost"]
            + production_report["ingredient_cost"]
            + ingredients_cost
            + energy_cost
        )

        day_log["summary"] = {
            "revenue": round(revenue, 2),
            "total_cost": round(total_cost, 2),
            "energy_cost": round(energy_cost, 2),
            "net_profit": round(revenue - total_cost, 2)
        }

        return day_log

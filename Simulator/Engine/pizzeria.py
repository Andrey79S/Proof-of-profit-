import json
from engine.production import Production
from engine.energy import Energy

class Pizzeria:
    def __init__(self):
        self.production = Production()
        self.energy = Energy(working_hours=12)

    def simulate_day(self, margarita_qty, pepperoni_qty):
        dough_kg = self.production.total_dough_required(
            margarita_qty, pepperoni_qty
        )

        ingredient_cost = self.production.make_pizzas(
            margarita_qty, pepperoni_qty
        )

        energy_cost = self.energy.total_energy(dough_kg)

        revenue = margarita_qty * 10 + pepperoni_qty * 14
        total_cost = ingredient_cost + energy_cost
        profit = revenue - total_cost

        return {
            "pizzas_total": margarita_qty + pepperoni_qty,
            "dough_used_kg": round(dough_kg, 2),
            "ingredient_cost": round(ingredient_cost, 2),
            "energy_cost": round(energy_cost, 2),
            "total_cost": round(total_cost, 2),
            "revenue": revenue,
            "net_profit": round(profit, 2)
        }

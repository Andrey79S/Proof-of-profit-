import json
from engine.production import Production
from engine.energy import Energy

class Pizzeria:
    def __init__(self):
        self.production = Production()
        self.energy = Energy()

    def simulate_day(self, margarita_qty, pepperoni_qty):
        production_cost = self.production.make_pizzas(
            margarita_qty,
            pepperoni_qty
        )

        energy_cost = self.energy.calculate_daily_energy(
            margarita_qty + pepperoni_qty
        )

        revenue = margarita_qty * 10 + pepperoni_qty * 14
        total_cost = production_cost + energy_cost
        profit = revenue - total_cost

        return {
            "revenue": revenue,
            "production_cost": round(production_cost, 2),
            "energy_cost": round(energy_cost, 2),
            "total_cost": round(total_cost, 2),
            "net_profit": round(profit, 2)
        }

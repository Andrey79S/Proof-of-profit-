import json

class Energy:
    def __init__(self):
        with open("simulator/config/equipment.json") as f:
            self.eq = json.load(f)
        with open("simulator/config/prices.json") as f:
            self.prices = json.load(f)

    def calculate_daily_energy(self, total_pizzas):
        oven_time_hours = (total_pizzas * 6) / 60
        oven_energy = oven_time_hours * self.eq["oven"]["power_kw"]
        return oven_energy * self.prices["electricity_per_kwh"]

import json
import math

class Energy:
    def __init__(self, working_hours=12):
        with open("simulator/config/equipment.json") as f:
            self.eq = json.load(f)
        with open("simulator/config/prices.json") as f:
            self.prices = json.load(f)

        self.working_hours = working_hours

    def fridge_energy(self):
        dough_fridge = self.eq["dough_fridge"]["power_kw"] * 24
        ing_fridge = self.eq["ingredients_fridge"]["power_kw"] * 24
        return dough_fridge + ing_fridge

    def oven_energy(self):
        return self.eq["oven"]["power_kw"] * self.working_hours

    def prep_table_energy(self):
        return self.eq["prep_table"]["power_kw"] * self.working_hours

    def mixer_energy(self, dough_kg):
        mixer = self.eq["dough_mixer"]
        min_load = 15
        max_load = 35

        batches = math.ceil(dough_kg / max_load)
        time_hours = batches * (mixer["time_min"] / 60)

        return mixer["power_kw"] * time_hours

    def total_energy(self, dough_kg):
        total_kwh = (
            self.fridge_energy() +
            self.oven_energy() +
            self.prep_table_energy() +
            self.mixer_energy(dough_kg)
        )
class EnergyTracker:
    def __init__(self):
        self.total_energy = 0.0

    def add(self, kwh):
        self.total_energy += kwh

    def reset(self):
        self.total_energy = 0.0

    def report(self):
        return self.total_energy
        
        return total_kwh * self.prices["electricity_per_kwh"]

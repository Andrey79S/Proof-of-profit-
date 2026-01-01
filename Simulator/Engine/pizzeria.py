# simulator/engine/pizzeria.py

import json
from collections import deque
from datetime import datetime
from engine.production import Production


class Fridge:
    def __init__(self, name, max_load, power_kw, spoil_hours):
        self.name = name
        self.max_load = max_load
        self.power_kw = power_kw
        self.spoil_hours = spoil_hours
        self.current_load = 0
        self.items = deque()  # (kg, timestamp)

    def add(self, kg):
        self.items.append((kg, datetime.now()))
        self.current_load += kg

    def remove(self, kg):
        removed = 0
        while kg > 0 and self.items:
            batch, ts = self.items[0]
            take = min(batch, kg)
            batch -= take
            kg -= take
            removed += take
            self.current_load -= take
            if batch <= 0:
                self.items.popleft()
            else:
                self.items[0] = (batch, ts)
        return removed

    def check_spoilage(self):
        now = datetime.now()
        spoiled = 0
        new_items = deque()
        for kg, ts in self.items:
            hours = (now - ts).total_seconds() / 3600
            if hours > self.spoil_hours:
                spoiled += kg
                self.current_load -= kg
            else:
                new_items.append((kg, ts))
        self.items = new_items
        return spoiled


class Table:
    def __init__(self, max_load):
        self.max_load = max_load
        self.current_load = 0.0
        self.stock = {}  # {ingredient: kg}

    def fill(self, ing_name, kg):
        if ing_name not in self.stock:
            self.stock[ing_name] = 0
        space = self.max_load - self.current_load
        to_add = min(space, kg)
        self.stock[ing_name] += to_add
        self.current_load += to_add
        return to_add

    def remove(self, ing_name, kg):
        available = self.stock.get(ing_name, 0)
        take = min(available, kg)
        self.stock[ing_name] -= take
        self.current_load -= take
        return take


class Oven:
    def __init__(self, power_kw, capacity):
        self.power_kw = power_kw
        self.capacity = capacity
        self.on = False

    def energy_per_minute(self):
        return self.power_kw / 60 if self.on else 0


class DoughMixer:
    def __init__(self, min_load, max_load, power_kw, time_min):
        self.min_load = min_load
        self.max_load = max_load
        self.power_kw = power_kw
        self.time_min = time_min

    def mix(self, kg):
        kg = max(self.min_load, min(kg, self.max_load))
        return kg

    def energy_per_mix(self):
        return self.power_kw * (self.time_min / 60)


class Pizzeria:
    def __init__(self, config_folder="config"):
        # Production
        self.production = Production(config_folder)

        # Чтение оборудования
        with open(f"{config_folder}/equipment.json", encoding="utf-8") as f:
            eq = json.load(f)

        self.dough_mixer = DoughMixer(**eq["dough_mixer"])
        self.oven = Oven(eq["oven"]["power_kw"], eq["oven"]["capacity"])
        self.proofing_fridge = Fridge("proofing", eq["proofing_fridge"]["max_load"], eq["proofing_fridge"]["power_kw"], spoil_hours=48)
        self.ingredients_fridge = Fridge("ingredients", eq["ingredient_fridge"]["max_load"], eq["ingredient_fridge"]["power_kw"], spoil_hours=168)
        self.table = Table(eq["table"]["max_load"])

    # =========================
    # Методы для WorkSession
    # =========================
    def fill_table_if_needed(self):
        for ing_name in self.production.ingredients_data.keys():
            needed = self.table.max_load - self.table.current_load
            moved = self.ingredients_fridge.remove(needed)
            self.table.fill(ing_name, moved)

    def return_table_to_fridge(self):
        for ing_name, kg in self.table.stock.items():
            self.ingredients_fridge.add(kg)
        self.table.stock.clear()
        self.table.current_load = 0

    def check_spoilage(self):
        return self.proofing_fridge.check_spoilage() + self.ingredients_fridge.check_spoilage()

    def calculate_energy_per_minute(self):
        total = self.oven.energy_per_minute()
        total += self.proofing_fridge.power_kw / 60
        total += self.ingredients_fridge.power_kw / 60
        return total

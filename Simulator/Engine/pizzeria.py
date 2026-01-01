# simulator/engine/pizzeria.py

from engine.production import DoughMixer
from engine.energy import EnergyTracker
import json
import os
import random
from datetime import datetime, timedelta

class Fridge:
    def __init__(self, name, max_load, min_load_ratio=0.3, spoil_hours=48):
        self.name = name
        self.max_load = max_load
        self.min_load = max_load * min_load_ratio
        self.current_load = 0.0  # кг
        self.spoil_hours = spoil_hours
        self.items = []  # list of tuples (weight, timestamp)

    def add_dough(self, weight):
        timestamp = datetime.now()
        self.items.append((weight, timestamp))
        self.current_load += weight

    def remove_dough(self, weight):
        removed = 0
        while weight > 0 and self.items:
            w, ts = self.items[0]
            if w <= weight:
                weight -= w
                removed += w
                self.items.pop(0)
            else:
                self.items[0] = (w - weight, ts)
                removed += weight
                weight = 0
        self.current_load -= removed
        return removed

    def check_spoilage(self):
        now = datetime.now()
        spoiled = 0
        new_items = []
        for w, ts in self.items:
            if (now - ts).total_seconds() / 3600 > self.spoil_hours:
                spoiled += w
            else:
                new_items.append((w, ts))
        self.items = new_items
        self.current_load -= spoiled
        return spoiled

class Table:
    def __init__(self, max_load, min_load_ratio=0.3):
        self.max_load = max_load
        self.min_load = max_load * min_load_ratio
        self.current_load = 0.0

    def fill(self, amount):
        space = self.max_load - self.current_load
        to_add = min(space, amount)
        self.current_load += to_add
        return to_add

    def empty(self):
        temp = self.current_load
        self.current_load = 0.0
        return temp

class Oven:
    def __init__(self, power_kw=8):
        self.power_kw = power_kw
        self.on = False

    def energy_per_minute(self):
        return self.power_kw / 60 if self.on else 0

class Pizzeria:
    def __init__(self, config_folder="config"):
        # Загружаем конфиги
        self.config_folder = config_folder
        self.load_configs()

        # Энергия
        self.energy_tracker = EnergyTracker()

        # Оборудование
        self.dough_mixer = DoughMixer(self.equipment["dough_mixer"])
        self.oven = Oven(self.equipment["oven"]["power_kw"])
        self.proofing_fridge = Fridge("proofing", max_load=self.equipment["proofing_fridge"]["max_load"], spoil_hours=48)
        self.ingredients_fridge = Fridge("ingredients", max_load=self.equipment["ingredient_fridge"]["max_load"], spoil_hours=168)  # 7 дней
        self.table = Table(max_load=self.equipment["table"]["max_load"])

    def load_configs(self):
        def load_json(file):
            with open(os.path.join(self.config_folder, file), "r") as f:
                return json.load(f)
        self.equipment = load_json("equipment.json")
        self.ingredients = load_json("ingredients.json")
        self.recipes = load_json("recipes.json")
        self.prices = load_json("prices.json")

    # ==================== Методы для WorkSession ====================
    def fill_table_if_needed(self):
        if self.table.current_load < self.table.min_load:
            amount_needed = self.table.max_load - self.table.current_load
            available = self.ingredients_fridge.current_load
            moved = min(amount_needed, available)
            if moved > 0:
                self.ingredients_fridge.remove_dough(moved)
                self.table.fill(moved)
                print(f"🧑‍🍳 Стол наполнен {moved:.2f} кг ингредиентов")

    def load_ready_dough_to_cooking_area(self):
        # Перемещение теста из расстоечного холодильника на стол для печи
        max_cooking = 10  # поддонов
        # поддон = 1 кг
        ready_dough = min(max_cooking - self.table.current_load, self.proofing_fridge.current_load)
        if ready_dough > 0:
            self.proofing_fridge.remove_dough(ready_dough)
            self.table.fill(ready_dough)
            print(f"🍞 {ready_dough} кг теста перемещено на стол для готовки")

    def return_table_to_fridge(self):
        returned = self.table.empty()
        if returned > 0:
            self.ingredients_fridge.add_dough(returned)
            print(f"🔄 Остаток со стола {returned:.2f} кг вернулся в холодильник ингредиентов")

    def calculate_energy_per_minute(self):
        energy = 0
        # Печь
        energy += self.oven.energy_per_minute()
        # Стол (условно)
        energy += self.equipment["table"]["power_kw"] / 60
        # Холодильники 24/7
        energy += self.equipment["proofing_fridge"]["power_kw"] / 60
        energy += self.equipment["ingredient_fridge"]["power_kw"] / 60
        return energy

    def check_spoilage(self):
        # Тесто в расстоечном холодильнике
        spoiled_dough = self.proofing_fridge.check_spoilage()
        if spoiled_dough > 0:
            print(f"⚠️  {spoiled_dough:.2f} кг теста испорчено в расстоечном холодильнике")
        # Ингредиенты
        spoiled_ing = self.ingredients_fridge.check_spoilage()
        if spoiled_ing > 0:
            print(f"⚠️  {spoiled_ing:.2f} кг ингредиентов испорчено в холодильнике")
        return spoiled_dough + spoiled_ing

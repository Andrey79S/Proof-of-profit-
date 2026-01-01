import json
from datetime import datetime
from collections import deque

class Fridge:
    def __init__(self, name, max_load, power_kw, spoil_hours=48):
        self.name = name
        self.max_load = max_load
        self.power_kw = power_kw
        self.current_load = 0.0
        self.items = deque()  # (kg, timestamp)
        self.spoil_hours = spoil_hours

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
            if (now - ts).total_seconds() / 3600 > self.spoil_hours:
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

    def fill(self, kg):
        space = self.max_load - self.current_load
        to_add = min(space, kg)
        self.current_load += to_add
        return to_add

    def empty(self):
        temp = self.current_load
        self.current_load = 0.0
        return temp


class Oven:
    def __init__(self, power_kw, capacity=4):  # capacity = 4 пиццы по умолчанию
        self.power_kw = power_kw
        self.capacity = capacity
        self.on = False

self.oven = Oven(
    power_kw=eq["oven"]["power_kw"],
    capacity=eq["oven"].get("capacity", 4)  # берём из JSON или дефолт 4
)

    def energy_per_minute(self):
        return self.power_kw / 60 if self.on else 0


class DoughMixer:
    def __init__(self, min_load, max_load, power_kw, time_min, **kwargs):
        self.min_load = min_load
        self.max_load = max_load
        self.power_kw = power_kw
        self.time_min = time_min
        # сохраняем все дополнительные поля из JSON, чтобы не было ошибок
        for k, v in kwargs.items():
            setattr(self, k, v)

    def mix(self, kg):
        # ограничиваем по min/max
        kg = max(self.min_load, min(kg, self.max_load))
        return kg

    def energy_per_mix(self):
        return self.power_kw * (self.time_min / 60)


# =========================
# Pizzeria
# =========================
class Pizzeria:
    def __init__(self, config_folder="config"):
        from engine.production import Production
        from engine.energy import EnergyTracker

        self.production = Production(config_folder)
        self.energy = EnergyTracker()

        # Загружаем конфиг оборудования
        with open(f"{config_folder}/equipment.json", "r", encoding="utf-8") as f:
            eq = json.load(f)

        # оборудование
        self.dough_mixer = DoughMixer(**eq["dough_mixer"])
        self.oven = Oven(eq["oven"]["power_kw"], eq["oven"]["capacity"])
        self.proofing_fridge = Fridge(
            "proofing", eq["proofing_fridge"]["max_load"], eq["proofing_fridge"]["power_kw"], spoil_hours=48
        )
        self.ingredients_fridge = Fridge(
            "ingredients", eq["ingredient_fridge"]["max_load"], eq["ingredient_fridge"]["power_kw"], spoil_hours=168
        )
        self.table = Table(eq["table"]["max_load"])

    # =========================
    # Методы для WorkSession
    # =========================
    def fill_table_if_needed(self):
        if self.table.current_load < self.table.max_load * 0.3:
            moved = self.ingredients_fridge.remove(self.table.max_load - self.table.current_load)
            self.table.fill(moved)
            return moved
        return 0

    def load_dough_to_table(self):
        moved = self.proofing_fridge.remove(min(10, self.proofing_fridge.current_load))
        self.table.fill(moved)
        return moved

    def return_table_to_fridge(self):
        kg = self.table.empty()
        self.ingredients_fridge.add(kg)
        return kg

    def check_spoilage(self):
        spoiled_dough = self.proofing_fridge.check_spoilage()
        spoiled_ing = self.ingredients_fridge.check_spoilage()
        return spoiled_dough + spoiled_ing

    def calculate_energy_per_minute(self):
        total = 0
        total += self.oven.energy_per_minute()
        total += self.proofing_fridge.power_kw / 60
        total += self.ingredients_fridge.power_kw / 60
        return total

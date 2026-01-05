import json
from pathlib import Path

class DoughMixer:
    def __init__(self, min_load, max_load, power_kw, time_min):
        self.min_load = min_load
        self.max_load = max_load
        self.power_kw = power_kw
        self.time_min = time_min

    def mix(self, amount):
        # Ограничение по загрузке
        actual = min(max(amount, self.min_load), self.max_load)
        # Возвращаем сколько теста получилось
        return actual

class Oven:
    def __init__(self, power_kw, capacity, bake_time_min):
        self.power_kw = power_kw
        self.capacity = capacity
        self.bake_time_min = bake_time_min

    def bake(self, pizzas):
        # Максимум, что помещается за один раз
        baked = min(pizzas, self.capacity)
        return baked

class ProofingFridge:
    def __init__(self, max_load, power_kw):
        self.max_load = max_load
        self.power_kw = power_kw

class IngredientFridge:
    def __init__(self, max_load, power_kw):
        self.max_load = max_load
        self.power_kw = power_kw

def load_equipment(json_file: str):
    path = Path(json_file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    eq_type = data.get("type")
    if eq_type == "dough_mixer":
        return DoughMixer(**data)
    elif eq_type == "oven":
        return Oven(**data)
    elif eq_type == "proofing_fridge":
        return ProofingFridge(**data)
    elif eq_type == "ingredient_fridge":
        return IngredientFridge(**data)
    else:
        raise ValueError(f"Unknown equipment type: {eq_type}")

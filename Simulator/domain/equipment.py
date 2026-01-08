# domain/equipment.py
import json
from pathlib import Path

class Equipment:
    def __init__(self, name, min_load, max_load, power_kw, cook_time_min=None):
        self.name = name
        self.min_load = min_load
        self.max_load = max_load
        self.power_kw = power_kw
        self.cook_time_min = cook_time_min
        self.current_load = 0

    def can_process(self, amount):
        return self.current_load + amount <= self.max_load

    def process(self, amount):
        self.current_load += amount

class EquipmentFactory:
    @staticmethod
    def create_from_json(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Equipment(
            name=data["name"],
            min_load=data.get("min_load", 0),
            max_load=data.get("max_load", 0),
            power_kw=data.get("power_kw", 0),
            cook_time_min=data.get("cook_time_min", None)
        )

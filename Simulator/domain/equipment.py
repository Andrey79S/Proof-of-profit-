# domain/equipment.py
import json
import os

class Equipment:
    def __init__(self, name, eq_type, capacity, min_load, cook_time_min, power_kw):
        self.name = name
        self.type = eq_type
        self.capacity = capacity
        self.min_load = min_load
        self.cook_time_min = cook_time_min
        self.power_kw = power_kw
        self.busy_until = 0  # время до окончания работы

class EquipmentFactory:
    @staticmethod
    def load_from_file(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Equipment(
                data["name"],
                data["type"],
                data["capacity"],
                data.get("min_load", 1),
                data.get("cook_time_min", 0),
                data.get("power_kw", 0)
            )

    @staticmethod
    def load_all_from_folder(folder_path):
        equipments = []
        for fname in os.listdir(folder_path):
            if fname.endswith(".json"):
                eq = EquipmentFactory.load_from_file(os.path.join(folder_path, fname))
                equipments.append(eq)
        return equipments

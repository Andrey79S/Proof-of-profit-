# domain/equipment.py

import json
import os

class Equipment:
    def __init__(self, name, type_, capacity=None, power_kw=0, min_load=None, max_load=None, cook_time=None):
        self.name = name
        self.type = type_
        self.capacity = capacity
        self.power_kw = power_kw
        self.min_load = min_load
        self.max_load = max_load
        self.cook_time = cook_time

    def __repr__(self):
        return f"<Equipment {self.name} ({self.type})>"

class EquipmentFactory:
    def __init__(self, player_folder: str):
        # folder должен указывать на папку конкретного игрока, например "player_data/player123/equipment"
        self.folder = player_folder

    def load_player_equipment(self):
        equipment_objects = {}
        if not os.path.exists(self.folder):
            return equipment_objects

        for filename in os.listdir(self.folder):
            if filename.endswith(".json"):
                path = os.path.join(self.folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    key = filename.replace(".json", "")
                    eq = Equipment(
                        name=data.get("name", key),
                        type_=data.get("type"),
                        capacity=data.get("capacity"),
                        power_kw=data.get("power_kw", 0),
                        min_load=data.get("min_load"),
                        max_load=data.get("max_load"),
                        cook_time=data.get("cook_time")
                    )
                    equipment_objects[key] = eq
        return equipment_objects

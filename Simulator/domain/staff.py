# domain/staff.py
import json
import os

class Staff:
    def __init__(self, name, role, speed_multiplier, can_use_equipment):
        self.name = name
        self.role = role
        self.speed_multiplier = speed_multiplier
        self.can_use_equipment = can_use_equipment
        self.busy_until = 0

class StaffFactory:
    @staticmethod
    def load_from_file(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Staff(
                data["name"],
                data["role"],
                data.get("speed_multiplier", 1.0),
                data.get("can_use_equipment", [])
            )

    @staticmethod
    def load_all_from_folder(folder_path):
        staff_list = []
        for fname in os.listdir(folder_path):
            if fname.endswith(".json"):
                s = StaffFactory.load_from_file(os.path.join(folder_path, fname))
                staff_list.append(s)
        return staff_list

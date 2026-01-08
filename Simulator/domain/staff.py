import json

class Staff:
    def __init__(self, name, role, skill_level, speed_modifier=1.0):
        self.name = name
        self.role = role           # cook, waiter, etc.
        self.skill_level = skill_level
        self.speed_modifier = speed_modifier

    def __repr__(self):
        return f"<Staff {self.name} ({self.role}) skill={self.skill_level}>"

class StaffFactory:
    @staticmethod
    def create_from_json(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Staff(
            name=data.get("name"),
            role=data.get("role"),
            skill_level=data.get("skill_level", 1),
            speed_modifier=data.get("speed_modifier", 1.0)
        )

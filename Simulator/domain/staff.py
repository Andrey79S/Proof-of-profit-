import json

class Staff:
    def __init__(self, name: str, role: str, speed_multiplier: float = 1.0, salary_per_hour: float = 0.0):
        self.name = name
        self.role = role
        self.speed_multiplier = speed_multiplier
        self.salary_per_hour = salary_per_hour

    def __repr__(self):
        return f"Staff({self.name}, {self.role}, speed={self.speed_multiplier})"

class StaffFactory:
    @staticmethod
    def create_from_json(data: dict):
        return Staff(
            name=data["name"],
            role=data["role"],
            speed_multiplier=data.get("speed_multiplier", 1.0),
            salary_per_hour=data.get("salary_per_hour", 0.0)
        )

class Staff:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.role = data["role"]
        self.salary_per_hour = data.get("salary_per_hour", 0.0)

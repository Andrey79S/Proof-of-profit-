import json

class Equipment:
    def __init__(self, name: str, type: str, capacity: int | float, power_kw: float, cook_time_min: int = None, min_batch: float = 0, max_batch: float = 0):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.power_kw = power_kw
        self.cook_time_min = cook_time_min
        self.min_batch = min_batch
        self.max_batch = max_batch
        self.is_busy = False

    def can_use(self, amount: float = 0):
        if self.type == "mixer" and (amount < self.min_batch or amount > self.max_batch):
            return False
        return not self.is_busy

    def use(self, duration_min: int):
        self.is_busy = True
        # В симуляции tick(duration_min), потом free
        self.is_busy = False  # Пока просто, в scheduler добавить event для free

class EquipmentFactory:
    @staticmethod
    def create_from_json(data: dict):
        return Equipment(
            name=data["name"],
            type=data.get("type", ""),
            capacity=data.get("capacity", 0),
            power_kw=data.get("power_kw", 0.0),
            cook_time_min=data.get("cook_time_min"),
            min_batch=data.get("min_batch_kg", 0),
            max_batch=data.get("max_batch_kg", 0)
    )

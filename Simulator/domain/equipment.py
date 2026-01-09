class Equipment:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.type = data["type"]
        self.power_kw = data.get("power_kw", 0.0)
        self.capacity = data.get("capacity", 0.0)
        self.min_batch = data.get("min_batch_kg", 0.0)
        self.max_batch = data.get("max_batch_kg", 0.0)

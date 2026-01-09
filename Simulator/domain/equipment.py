class Equipment:
    def __init__(self, name: str, type: str, power_kw: float = 0.0, capacity: float = 0.0):
        self.name = name
        self.type = type
        self.power_kw = power_kw
        self.capacity = capacity

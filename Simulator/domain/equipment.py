class Equipment:
    def __init__(self, name, power_kw):
        self.name = name
        self.power_kw = power_kw


class Oven(Equipment):
    def __init__(self, name, power_kw, capacity, cook_time):
        super().__init__(name, power_kw)
        self.capacity = capacity
        self.cook_time = cook_time

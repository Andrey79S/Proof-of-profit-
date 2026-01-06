class Equipment:
    def __init__(self, name, power_kw=0):
        self.name = name
        self.power_kw = power_kw
        self.in_use = False

    def use(self, duration_min):
        self.in_use = True

    def release(self):
        self.in_use = False

class Oven(Equipment):
    def __init__(self, name, power_kw, capacity, bake_time):
        super().__init__(name, power_kw)
        self.capacity = capacity
        self.bake_time = bake_time

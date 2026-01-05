class DoughMixer:
    def __init__(self, min_load, max_load, power_kw, time_min):
        self.min_load = min_load
        self.max_load = max_load
        self.power_kw = power_kw
        self.time_min = time_min

class Oven:
    def __init__(self, power_kw, capacity, bake_time_min):
        self.power_kw = power_kw
        self.capacity = capacity
        self.bake_time_min = bake_time_min

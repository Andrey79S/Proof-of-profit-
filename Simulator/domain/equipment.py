# domain/equipment.py
class Equipment:
    def __init__(self, name, power_kw):
        self.name = name
        self.power_kw = power_kw
        self.busy_until = 0

    def is_free(self, current_time):
        return current_time >= self.busy_until

    def use(self, current_time, duration_min):
        self.busy_until = current_time + duration_min
        return self.power_kw * duration_min / 60  # энергозатраты кВт·ч

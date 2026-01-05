# domain/staff.py
class Staff:
    def __init__(self, name, skill=1.0, speed_factor=1.0):
        self.name = name
        self.skill = skill
        self.speed_factor = speed_factor
        self.busy_until = 0

    def is_free(self, current_time):
        return current_time >= self.busy_until

    def assign(self, current_time, duration_min):
        self.busy_until = current_time + duration_min
        return duration_min

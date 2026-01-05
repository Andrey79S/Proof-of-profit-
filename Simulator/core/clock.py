# core/clock.py
class Clock:
    def __init__(self):
        self.day = 1
        self.minute = 0  # минута в дне
        self.total_minutes = 0

    def advance(self, minutes):
        self.minute += minutes
        self.total_minutes += minutes
        while self.minute >= 1440:  # 24*60 минут в дне
            self.minute -= 1440
            self.day += 1

    def current_time(self):
        h = self.minute // 60
        m = self.minute % 60
        return f"День {self.day}, {h:02d}:{m:02d}"

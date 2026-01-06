# core/clock.py
class Clock:
    def __init__(self):
        self._time = 0  # минуты

    def now(self):
        return self._time

    def tick(self, minutes=1):
        self._time += minutes

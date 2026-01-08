class Clock:
    def __init__(self):
        self._time = 0  # минуты с начала симуляции

    def now(self):
        return self._time

    def tick(self, minutes: int):
        if minutes < 0:
            raise ValueError("Время не может идти назад")
        self._time += minutes

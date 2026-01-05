class Clock:
    def __init__(self):
        self.now = 0  # минуты от старта

    def advance(self, minutes: int):
        self.now += minutes

class Clock:
    def __init__(self):
        self.current_minute = 0

    def tick(self, minutes=1):
        self.current_minute += minutes

    def now(self):
        return self.current_minute

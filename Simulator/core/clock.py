class Clock:
    def __init__(self, initial_minutes: int = 0):
        self.current_minutes = initial_minutes

    def now(self) -> int:
        return self.current_minutes

    def tick(self, minutes: int):
        if minutes < 0:
            raise ValueError("Нельзя двигать время назад")
        self.current_minutes += minutes

    def get_day(self) -> int:
        return self.current_minutes // (24 * 60)

    def get_hour(self) -> int:
        return (self.current_minutes % (24 * 60)) // 60

    def __str__(self):
        d = self.get_day() + 1
        h = self.get_hour()
        m = self.current_minutes % 60
        return f"День {d}, {h:02d}:{m:02d}"

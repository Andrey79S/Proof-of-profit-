class Clock:
    def __init__(self, initial_minutes: int = 0):
        self.current_minutes = initial_minutes

    def now(self) -> int:
        return self.current_minutes

    def tick(self, minutes: int):
        if minutes < 0:
            raise ValueError("Время не может идти назад")
        self.current_minutes += minutes

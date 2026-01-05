# domain/dough.py
class Dough:
    def __init__(self):
        self.total_kg = 0

    def add(self, kg):
        self.total_kg += kg

    def remove(self, kg):
        if kg > self.total_kg:
            raise ValueError("Недостаточно теста")
        self.total_kg -= kg

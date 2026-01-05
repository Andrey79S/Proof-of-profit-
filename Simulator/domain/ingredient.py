# domain/ingredient.py
class Ingredient:
    def __init__(self, name, price_per_kg, quantity_kg=0):
        self.name = name
        self.price_per_kg = price_per_kg
        self.quantity_kg = quantity_kg

    def add(self, kg):
        self.quantity_kg += kg

    def remove(self, kg):
        if kg > self.quantity_kg:
            raise ValueError(f"Недостаточно {self.name}")
        self.quantity_kg -= kg

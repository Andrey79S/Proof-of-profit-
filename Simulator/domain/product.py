class Ingredient:
    def __init__(self, name, amount_kg=0):
        self.name = name
        self.amount_kg = amount_kg

    def consume(self, qty):
        if qty > self.amount_kg:
            raise ValueError(f"Недостаточно {self.name}")
        self.amount_kg -= qty

    def add(self, qty):
        self.amount_kg += qty

    def __repr__(self):
        return f"<Ingredient {self.name} {self.amount_kg}kg>"

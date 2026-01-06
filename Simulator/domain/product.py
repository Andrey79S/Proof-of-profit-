# domain/product.py
class Product:
    def __init__(self, name, quantity_kg):
        self.name = name
        self.quantity = quantity_kg  # кг

    def consume(self, amount):
        if amount > self.quantity:
            raise ValueError(f"Not enough {self.name}")
        self.quantity -= amount

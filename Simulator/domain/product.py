class Product:
    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount  # кг или шт

    def __repr__(self):
        return f"{self.name}: {self.amount:.2f}"

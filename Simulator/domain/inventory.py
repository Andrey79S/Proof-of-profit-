from domain.ingredient import Ingredient

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, ingredient: Ingredient):
        self.items.append(ingredient)

    def cleanup(self, now: int):
        self.items = [i for i in self.items if not i.is_expired(now)]

    def total(self, name: str) -> float:
        return sum(i.amount for i in self.items if i.name == name)

    def consume(self, name: str, qty: float):
        needed = qty
        for i in self.items:
            if i.name == name:
                take = min(i.amount, needed)
                i.amount -= take
                needed -= take
                if needed <= 0:
                    return
        raise ValueError(f"Not enough {name}")

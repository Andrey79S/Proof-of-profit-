class Inventory:
    def __init__(self):
        self.items = {}  # name -> amount

    def add(self, name: str, amount: float):
        self.items[name] = self.items.get(name, 0) + amount

    def has(self, name: str, amount: float) -> bool:
        return self.items.get(name, 0) >= amount

    def consume(self, name: str, amount: float) -> bool:
        if not self.has(name, amount):
            return False
        self.items[name] -= amount
        return True

    def __repr__(self):
        return str(self.items)

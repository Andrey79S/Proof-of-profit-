class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, product):
        if product.name not in self.items:
            self.items[product.name] = 0
        self.items[product.name] += product.quantity

    def consume(self, name, quantity):
        if self.items.get(name, 0) >= quantity:
            self.items[name] -= quantity
            return True
        return False

    def get_quantity(self, name):
        return self.items.get(name, 0)

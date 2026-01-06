# domain/inventory.py
from domain.product import Product

class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        self.products[product.name] = product

    def consume(self, name, amount):
        if name not in self.products:
            raise ValueError(f"{name} not in inventory")
        self.products[name].consume(amount)

# domain/ingredient.py

from domain.product import Product


class Ingredient(Product):
    def __init__(
        self,
        name: str,
        quantity: float,
        created_at: int,
        shelf_life_min: int,
        base_price: float
    ):
        super().__init__(name, quantity, created_at, shelf_life_min)
        self.base_price = base_price

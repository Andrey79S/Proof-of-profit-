# domain/prepared.py

from domain.product import Product


class PreparedPizza(Product):
    def __init__(
        self,
        recipe: str,
        created_at: int,
        shelf_life_min: int = 10
    ):
        super().__init__(f"prepared_{recipe}", 1, created_at, shelf_life_min)
        self.recipe = recipe

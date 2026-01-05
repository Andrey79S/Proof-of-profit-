class Inventory:
    def __init__(self):
        self.ingredients = {
            "flour": 100,
            "water": 50,
            "tomato_sauce": 30,
            "mozzarella": 20,
            "pepperoni": 15
        }

    def has_ingredients(self, recipe: str) -> bool:
        needed = recipes[recipe]
        return all(self.ingredients[i] >= needed[i] for i in needed)

    def consume(self, recipe: str):
        needed = recipes[recipe]
        for i in needed:
            self.ingredients[i] -= needed[i]

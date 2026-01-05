from domain.dough import Dough

class Cooking:
    def __init__(self, dough: Dough):
        self.dough = dough

    def make_pizza(self, recipe: str, amount: float):
        if self.dough.weight >= amount:
            self.dough.use(amount)
            return True
        return False

# engine/cooking.py
class Cooking:
    def __init__(self, production):
        self.production = production

    def prepare_order(self, order):
        cook_time = self.production.cook(order)
        return cook_time

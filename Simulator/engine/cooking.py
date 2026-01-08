from engine.production import ProductionEngine

class Cooking:
    def __init__(self, production: ProductionEngine):
        self.production = production

    def prepare_order(self, order, now: int):
        return self.production.pizzeria.cook(order, now)

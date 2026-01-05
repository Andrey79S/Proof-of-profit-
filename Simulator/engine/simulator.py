from domain.order_pool import OrderPool
from engine.production import Production
from engine.cooking import Cooking

class Simulator:
    def __init__(self, production: Production, cooking: Cooking):
        self.production = production
        self.cooking = cooking
        self.order_pool = OrderPool()

    def add_orders(self, orders):
        for o in orders:
            self.order_pool.add_order(o)

    def run_day(self):
        completed = 0
        for order in self.order_pool.get_pending_orders():
            dough_needed = 0.2  # кг теста на пиццу
            self.production.mix_dough_if_needed(dough_needed)
            if self.cooking.make_pizza(order.recipe, dough_needed):
                completed += 1
                order.status = "done"
        print(f"[Simulator] Пицц выполнено за день: {completed}")
        return completed

from domain.order import Order, OrderStatus

class OrderPool:
    def __init__(self):
        self.pool = []

    def add_order(self, recipe: str, created_at: int, max_wait: int = 60):
        order = Order(recipe, created_at, max_wait)
        self.pool.append(order)
        return order

    def pending_orders(self):
        return [o for o in self.pool if o.status == OrderStatus.PENDING]

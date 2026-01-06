# domain/order_pool.py
class OrderPool:
    def __init__(self):
        self.pool = []

    def add_order(self, order):
        self.pool.append(order)

    def pending_orders(self):
        return [o for o in self.pool if o.status == o.status.PENDING]

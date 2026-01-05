class OrderPool:
    def __init__(self):
        self.orders = []

    def add_orders(self, orders):
        self.orders.extend(orders)

    def get_orders(self, capacity):
        taken = self.orders[:capacity]
        self.orders = self.orders[capacity:]
        return taken

    def remaining_orders(self):
        return len(self.orders)

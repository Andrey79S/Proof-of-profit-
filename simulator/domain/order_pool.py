class OrderPool:
    def __init__(self, initial_orders: int):
        self.orders = initial_orders

    def take(self, amount: int) -> int:
        taken = min(self.orders, amount)
        self.orders -= taken
        return taken

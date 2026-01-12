# domain/orders/pool.py

class OrdersPool:
    def __init__(self, initial_orders: int = 0):
        self.orders = initial_orders

    def add_orders(self, amount: int):
        if amount <= 0:
            return
        self.orders += amount

    def take_orders(self, amount: int) -> int:
        taken = min(self.orders, amount)
        self.orders -= taken
        return taken

    def get_orders_count(self) -> int:
        return self.orders

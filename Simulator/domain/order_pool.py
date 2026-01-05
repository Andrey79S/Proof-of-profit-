class OrderPool:
    def __init__(self):
        self.orders: list[Order] = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_available(self, now: int):
        """Возвращает список заказов, которые ещё можно принять"""
        return [
            order for order in self.orders
            if order.status == OrderStatus.PENDING and not order.is_expired(now)
        ]

    def expire_orders(self, now: int):
        for order in self.orders:
            if order.status == OrderStatus.PENDING and order.is_expired(now):
                order.status = OrderStatus.FAILED

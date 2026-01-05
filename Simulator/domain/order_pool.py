from domain.order import OrderStatus

class OrderPool:
    def __init__(self):
        self.orders = []

    def add(self, order):
        self.orders.append(order)

    def get_available(self, now: int):
        """Только живые, не просроченные заказы"""
        return [
            o for o in self.orders
            if o.status == OrderStatus.PENDING and not o.is_expired(now)
        ]

    def expire_orders(self, now: int):
        """Помечаем просроченные"""
        for o in self.orders:
            if o.status == OrderStatus.PENDING and o.is_expired(now):
                o.status = OrderStatus.FAILED

    def stats(self):
        return {
            "total": len(self.orders),
            "pending": sum(1 for o in self.orders if o.status == OrderStatus.PENDING),
            "done": sum(1 for o in self.orders if o.status == OrderStatus.DONE),
            "failed": sum(1 for o in self.orders if o.status == OrderStatus.FAILED),
        }

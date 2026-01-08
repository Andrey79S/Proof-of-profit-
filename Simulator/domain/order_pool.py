# domain/order_pool.py

from domain.order import Order, OrderStatus

class OrderPool:
    def __init__(self):
        self.pool = []

    def add_order(self, recipe: str, created_at_min: int, max_wait: int = 60):
        """
        Добавляет новый заказ в пул
        :param recipe: название рецепта (например, "margarita")
        :param created_at_min: время создания заказа в минутах от начала симуляции
        :param max_wait: максимальное время ожидания в минутах (по умолчанию 60)
        """
        order = Order(recipe=recipe, created_at=created_at_min, max_wait=max_wait)
        self.pool.append(order)
        return order

    def pending_orders(self):
        return [o for o in self.pool if o.status == OrderStatus.PENDING]

    def get_all_orders(self):
        return self.pool

    def __len__(self):
        return len(self.pool)

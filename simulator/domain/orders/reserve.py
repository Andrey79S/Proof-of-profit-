# domain/orders/reserve.py
from typing import Dict
from domain.orders.conversion import convert_orders_to_pizzas

class OrderReserve:
    """
    Резерв пиццерии:
    - хранит заказы, которые пиццерия может выполнить
    - конвертирует их в пиццы при резервировании
    """

    def __init__(self, base_capacity: int, menu_level: int = 1):
        self.base_capacity = base_capacity
        self.current = 0
        self.orders_detail: Dict[str, int] = {}
        self.menu_level = menu_level

    def reserve_from_pool(self, pool, capacity_limit: int):
        """
        Забираем из пулa до capacity_limit
        """
        taken = pool.take_orders(capacity_limit)
        pizza_orders = convert_orders_to_pizzas(taken, self.menu_level)
        self.add(pizza_orders)
        return taken, pizza_orders

    def add(self, pizza_orders: Dict[str, int]):
        total = sum(pizza_orders.values())
        self.current += total
        for k, v in pizza_orders.items():
            if k not in self.orders_detail:
                self.orders_detail[k] = 0
            self.orders_detail[k] += v

    def consume_for_production(self, amount: int) -> Dict[str, int]:
        if amount > self.current:
            amount = self.current
        self.current -= amount
        result = {}
        for k in self.orders_detail:
            qty = int(self.orders_detail[k] * amount / (self.current + amount))
            result[k] = qty
            self.orders_detail[k] -= qty
        return result

    def get_current(self) -> int:
        return self.current

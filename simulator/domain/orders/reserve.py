# domain/orders/reserve.py
from typing import Dict

class OrderReserve:
    def __init__(self, base_capacity: int):
        self.base_capacity = base_capacity
        self.current = 0
        self.orders_detail: Dict[str, int] = {}  # тип пиццы → кол-во

    def add(self, amount: int, pizza_types: Dict[str, int]):
        self.current += amount
        for k, v in pizza_types.items():
            if k not in self.orders_detail:
                self.orders_detail[k] = 0
            self.orders_detail[k] += v

    def consume(self, amount: int) -> Dict[str, int]:
        if amount > self.current:
            amount = self.current
        self.current -= amount

        # упрощенно: отдаём пропорцию каждого типа
        result = {}
        for k in self.orders_detail:
            qty = int(self.orders_detail[k] * amount / (self.current + amount))
            result[k] = qty
            self.orders_detail[k] -= qty
        return result

    def get_current(self) -> int:
        return self.current

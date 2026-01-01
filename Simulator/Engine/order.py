# simulator/engine/order.py

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict
import itertools


# =========================
# СТАТУСЫ ЗАКАЗА
# =========================

class OrderStatus(Enum):
    PENDING = auto()
    COOKING = auto()
    DONE = auto()
    LOST = auto()


# =========================
# ГЕНЕРАТОР ID
# =========================

_order_id_gen = itertools.count(1)


# =========================
# ORDER
# =========================

@dataclass
class Order:
    pizzas_count: int
    created_minute: int
    expected_time: int  # допустимое ожидание (мин)
    recipe: Dict[str, float]  # ингредиенты на 1 пиццу
    cook_time: int            # время готовки заказа (мин)

    id: int = field(default_factory=lambda: next(_order_id_gen))
    status: OrderStatus = OrderStatus.PENDING

    started_minute: int | None = None
    finished_minute: int | None = None
    reserved_ingredients: Dict[str, float] = field(default_factory=dict)

    # =========================
    # РАСЧЁТЫ
    # =========================

    def total_ingredients(self) -> Dict[str, float]:
        """Сколько ингредиентов нужно на весь заказ"""
        return {
            ing: qty * self.pizzas_count
            for ing, qty in self.recipe.items()
            if ing != "dough"
        }

    def total_dough(self) -> float:
        return self.recipe.get("dough", 0.0) * self.pizzas_count

    def deadline_minute(self) -> int:
        return self.created_minute + self.expected_time

# simulator/engine/order_queue.py

from collections import deque
from typing import List
from engine.order import Order, OrderStatus


class OrderQueue:
    def __init__(self):
        self.pending = deque()   # заказы, ожидающие старта
        self.cooking = deque()   # активные заказы
        self.done: List[Order] = []
        self.lost: List[Order] = []

    # =========================
    # ДОБАВЛЕНИЕ ЗАКАЗА
    # =========================

    def add_order(self, order: Order):
        self.pending.append(order)

    # =========================
    # ПОПЫТКА ЗАПУСКА ЗАКАЗА
    # =========================

    def try_start_order(
        self,
        order: Order,
        current_minute: int,
        available_queue_time: int
    ) -> bool:
        """
        Проверяем:
        - успеваем ли по времени
        - если да → переводим в COOKING
        """

        finish_minute = current_minute + available_queue_time + order.cook_time

        if finish_minute > order.deadline_minute():
            order.status = OrderStatus.LOST
            self.lost.append(order)
            return False

        order.status = OrderStatus.COOKING
        order.started_minute = current_minute
        self.cooking.append(order)
        return True

    # =========================
    # ТИК ВРЕМЕНИ
    # =========================

    def tick(self, current_minute: int):
        """Проверяем завершение готовящихся заказов"""
        still_cooking = deque()

        for order in self.cooking:
            if current_minute >= order.started_minute + order.cook_time:
                order.status = OrderStatus.DONE
                order.finished_minute = current_minute
                self.done.append(order)
            else:
                still_cooking.append(order)

        self.cooking = still_cooking

    # =========================
    # СТАТИСТИКА
    # =========================

    def queue_cook_time(self) -> int:
        """Сколько минут уже занято в печи"""
        return sum(order.cook_time for order in self.cooking)

    def stats(self) -> dict:
        return {
            "pending": len(self.pending),
            "cooking": len(self.cooking),
            "done": len(self.done),
            "lost": len(self.lost)
        }

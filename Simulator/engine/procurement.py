# engine/procurement.py
import random

class Procurement:
    """
    Логика закупки ингредиентов
    """
    def __init__(self, pizzeria, delivery_time_min=1):
        self.pizzeria = pizzeria
        self.delivery_time_min = delivery_time_min
        self.orders = []  # список заказов на поставку

    def order_ingredient(self, name, amount, now):
        """
        Создаём заказ на поставку
        """
        self.orders.append({
            "ingredient": name,
            "amount": amount,
            "arrives_at": now + self.delivery_time_min
        })

    def process_orders(self, now):
        """
        Проверяем, пришли ли поставки
        """
        delivered = []
        for o in self.orders:
            if o["arrives_at"] <= now:
                self.pizzeria.inventory.add_product(o["ingredient"], o["amount"])
                delivered.append(o)
        for o in delivered:
            self.orders.remove(o)

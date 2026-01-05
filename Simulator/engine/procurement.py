from domain.inventory import Inventory

class Procurement:
    def __init__(self, inventory: Inventory, delivery_time: int = 1):
        self.inventory = inventory
        self.delivery_time = delivery_time  # минуты ожидания доставки

    def order_ingredient(self, name: str, amount: float):
        # Для симуляции просто добавляем в инвентарь с задержкой
        print(f"[Procurement] Заказ {amount} кг {name} (доставка {self.delivery_time} мин)")
        self.inventory.add(name, amount)

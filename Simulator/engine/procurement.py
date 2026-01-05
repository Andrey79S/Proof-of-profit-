class Procurement:
    def __init__(self, inventory, scheduler, economy_config):
        self.inventory = inventory
        self.scheduler = scheduler
        self.economy = economy_config

    def order_ingredient(self, ingredient, amount, now):
        delivery_time = 1  # минута, потом можно настраивать
        self.scheduler.schedule(now + delivery_time, lambda: self.inventory.add(ingredient, amount))
        print(f"Заказано {amount} кг {ingredient}, доставка через {delivery_time} мин")

from domain.pizzeria import Pizzeria
from domain.inventory import Inventory
from domain.order_pool import OrderPool
from core.scheduler import Scheduler
from engine.procurement import Procurement
from engine.production import Production

class Simulator:
    def __init__(self, config):
        self.scheduler = Scheduler()
        self.inventory = Inventory(config["ingredients"])
        self.order_pool = OrderPool()
        self.pizzeria = Pizzeria(
            "PoP Pizzeria",
            self.inventory,
            config["equipment"],
            config["staff"],
            self.scheduler
        )
        self.production = Production(self.pizzeria, self.scheduler)
        self.procurement = Procurement(self.inventory, self.scheduler, config["economy"])

    def run_day(self, orders_today, day_number):
        print(f"\n=== День {day_number} ===")
        # Загружаем заказы
        for order_data in orders_today:
            self.order_pool.add_order(order_data)

        # Симулируем по минутам
        day_minutes = 60 * 12  # 12 часов работы
        for _ in range(day_minutes):
            self.scheduler.tick()
            available_orders = self.order_pool.get_available(self.scheduler.now)
            for order in available_orders:
                self.pizzeria.try_accept_order(order)

            self.order_pool.expire_orders(self.scheduler.now)

    def summary(self):
        total_orders = len(self.order_pool.orders)
        done_orders = len([o for o in self.order_pool.orders if o.status == o.status.DONE])
        failed_orders = len([o for o in self.order_pool.orders if o.status == o.status.FAILED])
        print("\n=== Итоги симуляции ===")
        print(f"Всего заказов: {total_orders}")
        print(f"Выполнено: {done_orders}")
        print(f"Просрочено: {failed_orders}")

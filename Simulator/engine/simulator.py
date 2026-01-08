from core.clock import Clock
from core.scheduler import Scheduler
from domain.order import OrderStatus
from engine.procurement import Procurement

class SimulatorEngine:
    def __init__(self, pizzeria, order_pool, clock: Clock, scheduler: Scheduler):
        self.pizzeria = pizzeria
        self.order_pool = order_pool
        self.clock = clock
        self.scheduler = scheduler
        self.procurement = Procurement(pizzeria)

        self.stats = {
            "orders_total": 0,
            "orders_done": 0,
            "orders_failed": 0,
            "losses": 0.0
        }

    def run(self, total_minutes: int):
        print(f"▶ Симуляция: {total_minutes} минут")
        self.scheduler.run_until(self.clock, total_minutes)
        while self.clock.now() < total_minutes:
            self.step()
        self.report()

    def step(self):
        now = self.clock.now()

        # Порча
        losses = self.pizzeria.inventory.check_spoilage(now)
        self.stats["losses"] += losses * 0.5  # Пример стоимости

        # Закупки если мало
        if sum(ing.amount_kg for ing in self.pizzeria.inventory.ingredients.values()) < 20:
            cost_per_kg = 2.0  # пример: соус и сыр по 2$ за кг
            order_qty = {"tomato_sauce": 30, "mozzarella": 30}
            total_cost = sum(order_qty.values()) * cost_per_kg
            self.pizzeria.expenses += total_cost
            self.procurement.order_ingredients(order_qty)
            print(f"Закупка: +{order_qty}, затраты: {total_cost}$")

        # Истёкшие заказы
        for order in self.order_pool.pool:
            if order.status == OrderStatus.PENDING and order.is_expired(now):
                order.status = OrderStatus.FAILED
                self.stats["orders_failed"] += 1

        # Обработка заказа
        pending = self.order_pool.pending_orders()
        if pending:
            order = pending[0]
            if self.pizzeria.can_accept_order(order):
                order.status = OrderStatus.ACCEPTED
                order.accepted_at = now
                self.stats["orders_total"] += 1

                cook_time = self.pizzeria.cook(order, now)
                self.clock.tick(cook_time)

                order.status = OrderStatus.DONE
                order.completed_at = self.clock.now()
                self.stats["orders_done"] += 1
                return

        self.clock.tick(1)  # Шаг

    def report(self):
        print("\n=== ОТЧЁТ ===")
        print(f"Заказы всего: {self.stats['orders_total']}")
        print(f"Обработано: {self.stats['orders_done']}")
        print(f"Провалено: {self.stats['orders_failed']}")
        print(f"Потери от порчи: {self.stats['losses']}$")
        print(f"Энергия: {self.pizzeria.energy_consumed:.2f} кВт·ч")
        print(f"Доход: {self.pizzeria.revenue}$")
        print(f"Расходы: {self.pizzeria.expenses}$")
        print(f"Прибыль: {self.pizzeria.revenue - self.pizzeria.expenses - self.stats['losses']}$")

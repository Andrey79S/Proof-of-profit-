from core.clock import Clock
from core.scheduler import Scheduler 
from domain.order import OrderStatus
from engine.procurement import Procurement

class Clock:
    def __init__(self):
        self._now = 0
    def now(self):
        return self._now
    def tick(self, minutes):
        self._now += minutes

class SimulatorEngine:
    def __init__(self, pizzeria, order_pool, clock: Clock, scheduler: Scheduler):
        self.pizzeria = pizzeria
        self.order_pool = order_pool
        self.clock = clock
        self.scheduler = scheduler 
        self.procurement = Procurement(pizzeria)  # Для закупок

        self.stats = {
            "orders_total": 0,
            "orders_done": 0,
            "orders_failed": 0,
            "losses": 0.0  # Потери от порчи
        }

    def run(self, sessions, hours_per_session):
        total_minutes = sessions * hours_per_session * 60
        print(f"▶ Симуляция: {total_minutes} минут")

        while self.clock.now() < total_minutes:
            self.step()

        self.report()

    def step(self):
        now = self.clock.now()

        # 1. Порча и списание (для теста; добавь для ингредиентов аналогично)
        self._handle_spoilage(now)

        # 2. Закупки, если мало ингредиентов (пример: если <10, заказать)
        if sum(self.pizzeria.state.inventory.ingredients.values()) < 10:
            self.procurement.order_ingredients({"tomato_sauce": 10, "mozzarella": 10})  # Адаптируй

        # 3. Истёкшие заказы
        for order in self.order_pool.pool:
            if order.status == order.status.PENDING and order.is_expired(now):
                order.status = order.status.FAILED
                self.stats["orders_failed"] += 1

        # 4. Берём заказ
        pending = [o for o in self.order_pool.pool if o.status == order.status.PENDING]
        if pending:
            order = pending[0]
            if self.pizzeria.can_accept_order(order):
                order.status = order.status.ACCEPTED
                order.accepted_at = now
                self.stats["orders_total"] += 1

                cook_time = self.pizzeria.cook(order)
                self.clock.tick(cook_time)

                order.status = order.status.DONE
                order.completed_at = self.clock.now()
                self.stats["orders_done"] += 1
                return

        # Если ничего — тик
        self.clock.tick(1)

    def _handle_spoilage(self, now):
        # Списание теста
        spoiled = [b for b in self.pizzeria.state.inventory.dough_batches if b.expires_at_min <= now]
        for b in spoiled:
            self.stats["losses"] += b.amount * 0.5  # Пример: стоимость порчи за единицу
        self.pizzeria.state.inventory.dough_batches = [b for b in self.pizzeria.state.inventory.dough_batches if b.expires_at_min > now]

    def report(self):
        print("\n=== ОТЧЁТ ===")
        print(f"Заказы всего: {self.stats['orders_total']}")
        print(f"Обработано: {self.stats['orders_done']}")
        print(f"Провалено: {self.stats['orders_failed']}")
        print(f"Потери от порчи: {self.stats['losses']}$")
        print(f"Электроэнергия: {self.pizzeria.state.energy.consumed_kwh:.2f} кВт·ч")
        print(f"Продажи: {self.pizzeria.state.finance.revenue}$")
        print(f"Касса (баланс): {self.pizzeria.state.finance.balance}$")
        print(f"Доход (revenue - expenses): {self.pizzeria.state.finance.revenue - self.pizzeria.state.finance.expenses}$")
        print(f"Затраты на стафф: {sum(s['level'] * 10 for s in self.pizzeria.state.staff.staff.values())} $ (пример)")  # Адаптируй
        print(f"Пиццы: {self.pizzeria.state.stats.pizzas_made}")

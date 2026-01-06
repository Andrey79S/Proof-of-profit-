# engine/simulator.py

class SimulatorEngine:
    def __init__(self, pizzeria, order_pool, clock):
        self.pizzeria = pizzeria
        self.order_pool = order_pool
        self.clock = clock

        self.stats = {
            "orders_total": 0,
            "orders_done": 0,
            "orders_failed": 0
        }

    def run(self, sessions: int, hours_per_session: int):
        total_minutes = sessions * hours_per_session * 60

        print(f"▶ Симуляция запущена: {sessions} сессий × {hours_per_session} ч = {total_minutes} минут")

        while self.clock.now() < total_minutes:
            self.step()

        self.report()

    def step(self):
        now = self.clock.now()

        # 1. Проверяем истёкшие заказы
        for order in self.order_pool.pool:
            if order.status == order.status.PENDING and order.is_expired(now):
                order.status = order.status.FAILED
                self.stats["orders_failed"] += 1
                self.stats["orders_total"] += 1

        # 2. Берём первый доступный заказ из пула
        pending_orders = [
            o for o in self.order_pool.pool
            if o.status == o.status.PENDING
        ]

        if not pending_orders:
            # заказов нет — идёт время
            self.clock.tick(1)
            return

        order = pending_orders[0]

        # 3. Проверяем, может ли пиццерия принять заказ
        if not self.pizzeria.can_accept_order(order):
            self.clock.tick(1)
            return

        # 4. Принимаем заказ
        order.status = order.status.ACCEPTED
        order.accepted_at = now

        # 5. Производство (возвращает длительность)
        cook_time = self.pizzeria.production.cook(order)

        # 6. Время идёт
        self.clock.tick(cook_time)

        # 7. Завершаем заказ
        order.status = order.status.DONE
        order.completed_at = self.clock.now()

        self.stats["orders_done"] += 1
        self.stats["orders_total"] += 1

    def report(self):
        print("\n=== ОТЧЁТ СИМУЛЯЦИИ ===")
        print(f"Всего завершённых заказов: {self.stats['orders_total']}")
        print(f"Выполнено успешно:        {self.stats['orders_done']}")
        print(f"Сорвано (время/ресурсы):  {self.stats['orders_failed']}")

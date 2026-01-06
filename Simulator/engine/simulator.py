# engine/simulator.py

class SimulatorEngine:
    def __init__(self, pizzeria, order_pool, clock):
        self.pizzeria = pizzeria
        self.order_pool = order_pool
        self.clock = clock

        self.stats = {
            "orders_total": 0,    # всего завершённых (done + failed)
            "orders_done": 0,
            "orders_failed": 0,
        }

    def run(self, sessions: int, hours_per_session: int):
        total_minutes = sessions * hours_per_session * 60

        print(f"▶ Симуляция запущена: {total_minutes} минут")

        while self.clock.now() < total_minutes:
            self.step()

        self.report()

    def step(self):
        now = self.clock.now()

        # 1. Проверяем истёкшие заказы в пуле
        for order in self.order_pool.pool:
            if order.status.name == "PENDING" and order.is_expired(now):
                order.status = order.status.FAILED
                self.stats["orders_failed"] += 1
                self.stats["orders_total"] += 1

        # 2. Берём первый доступный заказ
        pending_orders = [
            o for o in self.order_pool.pool
            if o.status.name == "PENDING"
        ]

        if pending_orders:
            order = pending_orders[0]

            if self.pizzeria.can_accept_order(order):
                order.status = order.status.ACCEPTED
                order.accepted_at = now

                # 3. Производство (возвращает время готовки)
                cook_time = self.pizzeria.production.cook(order)

                # 4. Время проходит
                self.clock.tick(cook_time)

                order.status = order.status.DONE
                order.completed_at = self.clock.now()

                self.stats["orders_done"] += 1
                self.stats["orders_total"] += 1
                return

        # 5. Если ничего не произошло — время идёт на 1 минуту
        self.clock.tick(1)

    def report(self):
        print("\n=== ОТЧЁТ СИМУЛЯЦИИ ===")
        print(f"Время симуляции: {self.clock.now()} мин")

        for key, value in self.stats.items():
            print(f"{key}: {value}")

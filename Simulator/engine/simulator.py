class Clock:
    def __init__(self):
        self._now = 0
    def now(self):
        return self._now
    def tick(self, minutes):
        self._now += minutes

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

    def run(self, sessions, hours_per_session):
        total_minutes = sessions * hours_per_session * 60
        print(f"▶ Симуляция: {total_minutes} минут")

        while self.clock.now() < total_minutes:
            self.step()

        self.report()

    def step(self):
        now = self.clock.now()

        # 1. истёкшие заказы
        for order in self.order_pool.pool:
            if order.status == order.status.PENDING and order.is_expired(now):
                order.status = order.status.FAILED
                self.stats["orders_failed"] += 1

        # 2. берём заказ
        pending = [
            o for o in self.order_pool.pool
            if o.status == o.status.PENDING
        ]

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

        # если ничего не произошло — время идёт
        self.clock.tick(1)

    def report(self):
        print("\n=== ОТЧЁТ ===")
        for k, v in self.stats.items():
            print(f"{k}: {v}")
        print(f"Электроэнергия использована: {self.pizzeria.electricity_consumed:.2f} кВт·ч")
        print(f"Пицц приготовлено: {self.pizzeria.completed_orders}")

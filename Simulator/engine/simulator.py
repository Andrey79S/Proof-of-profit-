# engine/simulator.py

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

        # Для отслеживания смены
        self.current_day = 0
        self.shift_started = False

    def run(self, total_minutes: int):
        print(f"▶ Симуляция: {total_minutes} минут")
        end_time = self.clock.now() + total_minutes

        while self.clock.now() < end_time:
            self.step()

        self.report()

    def step(self):
        now = self.clock.now()
        current_hour = (now % (24 * 60)) // 60
        current_day = now // (24 * 60)

        # Новый день — сбрасываем смену
        if current_day > self.current_day:
            self.current_day = current_day
            self.shift_started = False
            print(f"\n🌙 Новый день ({current_day + 1}). Ночь — работают только холодильники.")

        # Оффлайн: энергия холодильников круглосуточно
        fridge_power = sum(
            eq.power_kw for eq in self.pizzeria.equipment.values()
            if eq.type in ["fridge", "proofing_fridge", "table_fridge", "ingredient_fridge"]
        )
        self.pizzeria.energy_consumed += fridge_power / 60.0  # за минуту
        self.pizzeria.expenses += (fridge_power / 60.0) * self.pizzeria.economy.get("electricity_price_per_kwh", 0.12)

        # Порча (каждые 60 минут)
        if now % 60 == 0:
            losses = self.pizzeria.inventory.check_spoilage(now)
            self.stats["losses"] += losses * 2.0  # пример стоимости кг

        # Начало смены (10:00)
        if current_hour == 10 and not self.shift_started:
            self.shift_started = True
            self.pizzeria.inventory.start_shift(now)
            print(f"☀ Начало смены в 10:00! Печь включена. Ингредиенты и тесто перенесены на стол.")

        # Конец смены (21:00)
        if current_hour == 21 and self.shift_started:
            self.shift_started = False
            print("🌆 Конец смены в 21:00. Печь выключена.")

        # Автоматический замес теста — только в смену и если мало готового
        if 10 <= current_hour <= 20:  # можно замешивать до 20:00
            ready_dough = sum(
                b.amount_kg for b in (self.pizzeria.inventory.table_dough + self.pizzeria.inventory.dough_batches)
                if (now - b.prepared_at_min) >= 720 and not b.is_expired(now)
            )
            if ready_dough < 30.0:
                success = self.pizzeria.production_engine.make_dough(now=now)
                if success:
                    self.clock.tick(25)  # замес + подготовка

        # Обработка заказов — только в смену
        if 10 <= current_hour < 21:
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

        # Истёкшие заказы
        for order in self.order_pool.pool:
            if order.status == OrderStatus.PENDING and order.is_expired(now):
                order.status = OrderStatus.FAILED
                self.stats["orders_failed"] += 1

        # Закупки (пока простые, потом с задержкой)
        if sum(ing.amount_kg for ing in self.pizzeria.inventory.ingredients.values()) < 100:
            self.procurement.order_ingredients({
                "flour": 100, "water": 60, "salt": 10, "yeast": 5, "olive_oil": 5,
                "tomato_sauce": 50, "mozzarella": 50
            })
            self.pizzeria.expenses += 300  # пример стоимости

        self.clock.tick(1)  # обычный шаг

    def report(self):
        print("\n" + "="*40)
        print("ОТЧЁТ ПО СМЕНЕ / ДНЮ")
        print("="*40)
        print(f"Заказы принято:     {self.stats['orders_total']}")
        print(f"Приготовлено:       {self.stats['orders_done']}")
        print(f"Провалено:          {self.stats['orders_failed']}")
        print(f"Потери от порчи:    {self.stats['losses']:.2f}$")
        print(f"Энергия:            {self.pizzeria.energy_consumed:.2f} кВт·ч")
        print(f"Выручка:            {self.pizzeria.revenue:.2f}$")
        print(f"Расходы:            {self.pizzeria.expenses:.2f}$")
        print(f"Прибыль:            {self.pizzeria.revenue - self.pizzeria.expenses - self.stats['losses']:.2f}$")

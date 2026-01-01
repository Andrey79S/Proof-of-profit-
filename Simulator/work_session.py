# simulator/work_session.py

from enum import Enum, auto
from engine.order import Order, OrderStatus
from engine.order_queue import OrderQueue


# =========================
# СОСТОЯНИЯ СЕССИИ
# =========================

class SessionState(Enum):
    IDLE = auto()
    STARTING = auto()
    ACTIVE = auto()
    STOPPING = auto()
    CLOSED = auto()


# =========================
# WORK SESSION
# =========================

class WorkSession:
    def __init__(self, pizzeria, working_minutes=12 * 60):
        self.pizzeria = pizzeria
        self.state = SessionState.IDLE

        self.current_minute = 0
        self.working_minutes = working_minutes

        self.orders = OrderQueue()

        self.energy = pizzeria.energy

        self.report = {
            "orders_total": 0,
            "orders_done": 0,
            "orders_lost": 0,
            "revenue": 0.0,
            "ingredients_cost": 0.0,
            "energy_kwh": 0.0,
        }

    # =========================
    # УПРАВЛЕНИЕ СЕССИЕЙ
    # =========================

    def start(self):
        if self.state != SessionState.IDLE:
            return

        self.state = SessionState.STARTING
        self._init_session()
        self.state = SessionState.ACTIVE

    def stop(self):
        if self.state != SessionState.ACTIVE:
            return

        self.state = SessionState.STOPPING
        self._close_session()
        self.state = SessionState.CLOSED

    # =========================
    # ИНИЦИАЛИЗАЦИЯ
    # =========================

    def _init_session(self):
        # включаем печь
        self.pizzeria.oven.on = True

        # наполняем стол
        self.pizzeria.fill_table_if_needed()

        # проверка теста → замес при необходимости
        self._ensure_dough_available()

    # =========================
    # ЗАКРЫТИЕ
    # =========================

    def _close_session(self):
        # выключаем печь
        self.pizzeria.oven.on = False

        # остатки со стола → в холодильник
        self.pizzeria.return_table_to_fridge()

        # финальный отчёт
        self.report["orders_done"] = len(self.orders.done)
        self.report["orders_lost"] = len(self.orders.lost)
        self.report["energy_kwh"] = round(self.energy.report(), 3)

    # =========================
    # ДОБАВЛЕНИЕ ЗАКАЗА (ТАП)
    # =========================

    def add_order(self, pizzas_count, recipe, cook_time, expected_time, price):
        if self.state != SessionState.ACTIVE:
            return

        order = Order(
            pizzas_count=pizzas_count,
            created_minute=self.current_minute,
            expected_time=expected_time,
            recipe=recipe,
            cook_time=cook_time
        )

        order.price = price
        self.orders.add_order(order)
        self.report["orders_total"] += 1

    # =========================
    # ОСНОВНОЙ TICK (1 МИНУТА)
    # =========================

    def tick(self):
        if self.state != SessionState.ACTIVE:
            return

        # 1️⃣ энергия за минуту
        self.energy.add(self.pizzeria.calculate_energy_per_minute())

        # 2️⃣ порча
        self.pizzeria.check_spoilage()

        # 3️⃣ обработка очереди заказов
        self._process_orders()

        # 4️⃣ тик готовки
        self.orders.tick(self.current_minute)

        # 5️⃣ замес теста при необходимости
        self._ensure_dough_available()

        # 6️⃣ время
        self.current_minute += 1

        if self.current_minute >= self.working_minutes:
            self.stop()

    # =========================
    # ОБРАБОТКА ЗАКАЗОВ
    # =========================

    def _process_orders(self):
        if not self.orders.pending:
            return

        order = self.orders.pending[0]

        # проверка ингредиентов
        if not self._has_ingredients(order):
            order.status = OrderStatus.LOST
            self.orders.lost.append(order)
            self.orders.pending.popleft()
            return

        # проверка времени
        queue_time = self.orders.queue_cook_time()
        started = self.orders.try_start_order(
            order,
            self.current_minute,
            queue_time
        )

        self.orders.pending.popleft()

        if not started:
            return

        # списываем ингредиенты
        self._consume_ingredients(order)

        # доход
        self.report["revenue"] += order.price

    # =========================
    # ИНГРЕДИЕНТЫ
    # =========================

    def _has_ingredients(self, order: Order) -> bool:
        needed = order.total_ingredients()
        dough_needed = order.total_dough()

        if self.pizzeria.proofing_fridge.current_load < dough_needed:
            return False

        for ing, kg in needed.items():
            if self.pizzeria.table.current_load < kg:
                self.pizzeria.fill_table_if_needed()
                if self.pizzeria.table.current_load < kg:
                    return False

        return True

    def _consume_ingredients(self, order: Order):
        # тесто
        self.pizzeria.proofing_fridge.remove(order.total_dough())

        # ингредиенты
        for ing, kg in order.total_ingredients().items():
            self.pizzeria.table.current_load -= kg
            self.report["ingredients_cost"] += kg  # цена считается отдельно

    # =========================
    # ТЕСТО
    # =========================

    def _ensure_dough_available(self):
        fridge = self.pizzeria.proofing_fridge
        mixer = self.pizzeria.dough_mixer

        if fridge.current_load >= fridge.max_load * 0.3:
            return

        space = fridge.max_load - fridge.current_load
        if space < mixer.min_load:
            return

        mixed = mixer.mix(space)
        fridge.add(mixed)

        self.energy.add(mixer.energy_per_mix())

# game/game_engine.py
import time
from simulation.engine import simulate_time


class GameEngine:
    def __init__(self, pool_manager, player_manager, config):
        self.pool = pool_manager
        self.players = player_manager
        self.config = config

    # ---------- TAP ----------
    def tap(self, user_id: int, taps: int = 1):
        player = self.players.get_or_create(user_id)
        pizzeria = player.pizzeria

        added_orders = taps * pizzeria.tap_power()
        self.pool.add_orders(added_orders)

        return added_orders

    # ---------- RESERVE ----------
    def reserve_work(self, user_id: int):
        player = self.players.get_or_create(user_id)
        pizzeria = player.pizzeria

        # сколько работы пиццерия МОЖЕТ взять
        reserve_capacity = pizzeria.production_capacity(hours=24)

        taken = self.pool.take_orders(reserve_capacity)

        if taken <= 0:
            return {}

        # тут впервые появляются ПИЦЦЫ
        pizza_orders = pizzeria.menu.convert_orders_to_pizzas(taken)
        pizzeria.reserve.add(taken, pizzeria)

        return pizza_orders

    # ---------- OFFLINE CATCH-UP ----------
    def catch_up(self, user_id: int):
        player = self.players.get_or_create(user_id)

        now = time.time()
        delta_seconds = now - player.last_seen
        hours = delta_seconds / 3600

        if hours <= 0:
            return

        simulate_time(player.pizzeria, self.config, hours)

        player.last_seen = now

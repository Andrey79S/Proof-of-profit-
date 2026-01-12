# game/player_manager.py
from domain.pizzeria import Pizzeria
from domain.order_reserve import OrderReserve
from accounting.ledger import Ledger
from config.default import CONFIG
import time


class PlayerState:
    def __init__(self, user_id: int):
        self.user_id = user_id

        self.reserve = OrderReserve(base_capacity=CONFIG["max_reserve"])
        self.ledger = Ledger()

        self.pizzeria = Pizzeria(
            base_capacity_per_hour=CONFIG["base_capacity_per_hour"],
            reserve=self.reserve,
            ledger=self.ledger
        )

        self.last_seen = time.time()


class PlayerManager:
    def __init__(self):
        self.players: dict[int, PlayerState] = {}

    def get_or_create(self, user_id: int) -> PlayerState:
        if user_id not in self.players:
            self.players[user_id] = PlayerState(user_id)
        return self.players[user_id]

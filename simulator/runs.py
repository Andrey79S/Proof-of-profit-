from domain.orders.pool import OrdersPool
from domain.orders.reserve import OrderReserve
from domain.pizzeria.production import Production
from game.tap.tap_system import TapSystem
from game.currencies.energy import Energy
from game.currencies.crystals import Crystals
from engine.game_loop import GameLoop

# --- Инициализация ---
pool = OrdersPool(1000)

class Player:
    def __init__(self, pool):
        self.energy = Energy(max_energy=10)
        self.crystals = Crystals(initial=5)
        self.reserve = OrderReserve(base_capacity=50, menu_level=1)
        self.production = Production(self.reserve, base_capacity=50)
        self.tap_system = TapSystem(self, pool)

players = [Player(pool), Player(pool)]  # несколько игроков

# --- Симуляция тапов ---
players[0].tap_system.do_tap()
players[1].tap_system.do_tap(multiplier=2)

# --- Game Loop ---
game_loop = GameLoop(players, pool, tick_hours=1)

# --- Один тик для проверки ---
game_loop.tick()

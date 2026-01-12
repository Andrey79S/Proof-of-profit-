# game/tap/tap_system.py
from .tap_action import TapAction
from .tap_upgrades import TapUpgrades

class TapSystem:
    """
    Менеджер всех тапов игрока
    """
    def __init__(self, player, pool):
        self.player = player
        self.pool = pool
        self.tap_upgrades = TapUpgrades()

    def do_tap(self, multiplier: int = 1):
        tap = TapAction(self.player, self.pool)
        orders_added = tap.tap(multiplier)
        return orders_added

    def upgrade(self, upgrade_type: str):
        if upgrade_type == "amount":
            self.tap_upgrades.upgrade_amount()
        elif upgrade_type == "quality":
            self.tap_upgrades.upgrade_quality()
        elif upgrade_type == "efficiency":
            self.tap_upgrades.upgrade_efficiency()

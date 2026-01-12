# game/tap/tap_upgrades.py

class TapUpgrades:
    """
    Управляет прокачкой тапов:
    - количество заказов за 1 тап
    - шанс качественного заказа
    - эффективность (меньше энергии на тап)
    """

    def __init__(self):
        self.amount_level = 1      # увеличивает кол-во заказов за тап
        self.quality_level = 1     # влияет на % премиум-пицц
        self.energy_efficiency = 1 # модификатор потребляемой энергии

    def upgrade_amount(self):
        self.amount_level += 1

    def upgrade_quality(self):
        self.quality_level += 1

    def upgrade_efficiency(self):
        self.energy_efficiency += 0.1  # например +10% эффективность

# simulator/engine/energy.py

class EnergyTracker:
    """
    Считает суммарное потребление энергии оборудования.
    Энергия в кВт·ч.
    """

    def __init__(self):
        self.total_energy = 0.0  # суммарная энергия

    def add(self, kwh: float):
        """
        Добавить потребление энергии за один шаг (минуту или цикл).
        """
        self.total_energy += kwh

    def reset(self):
        """Сбросить накопленное потребление энергии"""
        self.total_energy = 0.0

    def report(self) -> float:
        """Вернуть накопленное потребление энергии"""
        return round(self.total_energy, 2)

# game/currencies/crystals.py

class Crystals:
    """
    Премиум-валюта:
    - покупка редких апгрейдов
    - ускорение производства / тапов
    """
    def __init__(self, initial: int = 0):
        self.amount = initial

    def add(self, value: int):
        if value > 0:
            self.amount += value

    def spend(self, value: int) -> bool:
        if value > self.amount:
            return False
        self.amount -= value
        return True

    def get(self) -> int:
        return self.amount

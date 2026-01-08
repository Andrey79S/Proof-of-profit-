from dataclasses import dataclass
from typing import Optional


@dataclass
class DoughBatch:
    """
    Партия теста — полуфабрикат.
    Один batch = несколько заготовок под пиццу.
    """
    amount: int                  # сколько пицц можно сделать
    created_at: int              # timestamp (в минутах симуляции)
    ready_at: int                # когда можно использовать
    expires_at: int              # когда портится

    def is_ready(self, now: int) -> bool:
        return now >= self.ready_at

    def is_expired(self, now: int) -> bool:
        return now >= self.expires_at

    def take(self, qty: int) -> bool:
        """
        Забрать тесто из партии
        """
        if self.amount < qty:
            return False
        self.amount -= qty
        return True

# core/clock.py

class Clock:
    """
    Симуляционные часы.
    Истина времени для всей системы.
    """

    def __init__(self, start_minute: int = 0):
        self._minute = start_minute

    def now(self) -> int:
        """Текущее симуляционное время в минутах"""
        return self._minute

    def tick(self, minutes: int) -> None:
        """
        Продвигает время вперёд.
        """
        if minutes < 0:
            raise ValueError("Clock cannot go backwards")
        self._minute += minutes

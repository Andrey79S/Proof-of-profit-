class OrderReserve:
    def __init__(self, base_capacity: int):
        self.base_capacity = base_capacity
        self.current = 0

    def max_capacity(self, pizzeria) -> int:
        return pizzeria.max_reserve()

    def add(self, amount: int, pizzeria) -> int:
        free_space = self.max_capacity(pizzeria) - self.current
        added = max(0, min(free_space, amount))
        self.current += added
        return added

    def consume(self, amount: int) -> int:
        consumed = min(self.current, amount)
        self.current -= consumed
        return consumed

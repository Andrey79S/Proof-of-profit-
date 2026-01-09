class OrderReserve:
    def __init__(self, max_capacity: int):
        self.max_capacity = max_capacity
        self.current = 0

    def add(self, amount: int) -> int:
        free_space = self.max_capacity - self.current
        added = min(free_space, amount)
        self.current += added
        return added

    def consume(self, amount: int) -> int:
        consumed = min(self.current, amount)
        self.current -= consumed
        return consumed

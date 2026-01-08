from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COOKING = "cooking"
    DONE = "done"
    FAILED = "failed"

class Order:
    _id_counter = 1

    def __init__(self, recipe: str, created_at: int, max_wait: int):
        self.id = Order._id_counter
        Order._id_counter += 1
        self.recipe = recipe
        self.created_at = created_at
        self.max_wait = max_wait
        self.status = OrderStatus.PENDING
        self.accepted_at = None
        self.completed_at = None

    def is_expired(self, now: int) -> bool:
        return now - self.created_at > self.max_wait

    def __repr__(self):
        return f"Order(id={self.id}, recipe='{self.recipe}', status={self.status}, created_at={self.created_at})"

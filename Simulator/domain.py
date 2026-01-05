from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"      # в пуле
    ACCEPTED = "accepted"    # приняла пиццерия
    COOKING = "cooking"      # готовится
    DONE = "done"            # выполнен
    FAILED = "failed"        # сорван (время / нет ресурсов)


class Order:
    _id_counter = 1

    def __init__(self, recipe: str, created_at: int, max_wait: int):
        self.id = Order._id_counter
        Order._id_counter += 1

        self.recipe = recipe              # "margarita", "pepperoni"
        self.created_at = created_at      # минута создания
        self.max_wait = max_wait          # сколько клиент ждёт
        self.status = OrderStatus.PENDING

        self.accepted_at = None
        self.completed_at = None

    def is_expired(self, now: int) -> bool:
        return now - self.created_at > self.max_wait

    def __repr__(self):
        return f"<Order #{self.id} {self.recipe} status={self.status.value}>"

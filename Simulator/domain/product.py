# domain/product.py

class DoughBatch:
    """
    Партия теста
    """
    def __init__(self, amount_kg: float, prepared_at_min: int, expires_at_min: int):
        self.amount_kg = amount_kg
        self.prepared_at_min = prepared_at_min
        self.expires_at_min = expires_at_min

    def is_expired(self, now_minute: int) -> bool:
        return now_minute >= self.expires_at_min

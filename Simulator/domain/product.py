from dataclasses import dataclass

@dataclass
class DoughBatch:
    amount_kg: float
    prepared_at_min: int
    expires_at_min: int

    def is_expired(self, now: int) -> bool:
        return now >= self.expires_at_min

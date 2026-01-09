from dataclasses import dataclass

@dataclass
class Order:
    recipe: str
    created_at: int
    max_wait: int = 60

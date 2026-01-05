# domain/dough.py

from domain.product import Product, ProductState


class Dough(Product):
    def __init__(
        self,
        quantity: float,
        created_at: int,
        proof_time_min: int,
        shelf_life_min: int
    ):
        super().__init__("dough", quantity, created_at, shelf_life_min)
        self.proof_time_min = proof_time_min
        self.state = ProductState.PROOFING

    def update_state(self, now: int):
        if self.state == ProductState.PROOFING:
            if now - self.created_at >= self.proof_time_min:
                self.state = ProductState.READY

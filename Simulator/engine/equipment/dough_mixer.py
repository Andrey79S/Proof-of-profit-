from domain.dough import DoughBatch


class DoughMixer:
    """
    Миксер производит партии теста
    """

    def __init__(
        self,
        mix_time: int = 10,        # минут
        proof_time: int = 60,      # минут
        shelf_life: int = 240      # минут
    ):
        self.mix_time = mix_time
        self.proof_time = proof_time
        self.shelf_life = shelf_life

    def produce(self, now: int, amount: int) -> DoughBatch:
        created_at = now + self.mix_time
        ready_at = created_at + self.proof_time
        expires_at = ready_at + self.shelf_life

        return DoughBatch(
            amount=amount,
            created_at=created_at,
            ready_at=ready_at,
            expires_at=expires_at
        )

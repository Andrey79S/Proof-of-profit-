class SimulatorEngine:
    def __init__(self, pizzeria, order_pool, clock):
        self.pizzeria = pizzeria
        self.order_pool = order_pool
        self.clock = clock

    def run(self, sessions=1, hours_per_session=8):
        print(f"Running simulation: {sessions} sessions of {hours_per_session}h")

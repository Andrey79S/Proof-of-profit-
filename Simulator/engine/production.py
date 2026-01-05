class Production:
    def __init__(self, pizzeria, scheduler):
        self.pizzeria = pizzeria
        self.scheduler = scheduler

    def prepare_dough(self, amount, now):
        mixer = self.pizzeria.equipment["dough_mixer"]
        time = mixer["time_min"]
        self.scheduler.schedule(now + time, lambda: print(f"Готово тесто {amount} кг"))

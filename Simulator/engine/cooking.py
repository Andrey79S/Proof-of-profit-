class Cooking:
    @staticmethod
    def bake(order, pizzeria, scheduler):
        oven = pizzeria.equipment["oven"]
        time = oven["time_min"]
        scheduler.schedule(scheduler.now + time, lambda: pizzeria.finish_order(order))

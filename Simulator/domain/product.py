class Ingredient:
    def __init__(self, name, quantity=0, spoil_time=None):
        self.name = name
        self.quantity = quantity
        self.spoil_time = spoil_time  # минуты до порчи
        self.added_at = 0

    def is_spoiled(self, current_time):
        if self.spoil_time is None:
            return False
        return (current_time - self.added_at) >= self.spoil_time

class Dough(Ingredient):
    pass

class Pizza(Ingredient):
    def __init__(self, recipe, quantity=1):
        super().__init__(name=recipe, quantity=quantity)

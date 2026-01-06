# engine/production.py
from domain.product import Dough, Pizza
from domain.equipment import Oven, DoughMixer, ProofingFridge
from domain.staff import Staff

class Production:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria
        self.dough_mixer = pizzeria.equipment.get_mixer()
        self.proofing_fridge = pizzeria.equipment.get_proofing_fridge()
        self.ovens = pizzeria.equipment.get_ovens()

    def make_dough(self, amount_kg, staff: Staff):
        # проверка на наличие свободного оборудования
        if not self.dough_mixer.is_available():
            return 0

        # тесто замешивается с участием стафа
        time_required = self.dough_mixer.get_mix_time(amount_kg) / staff.speed_multiplier
        self.dough_mixer.use(time_required)
        dough = Dough(amount_kg)
        self.proofing_fridge.store(dough)
        return dough

    def cook(self, pizza_order):
        pizza_name = pizza_order.recipe
        pizza_recipe = self.pizzeria.recipes[pizza_name]

        # проверяем наличие ингредиентов
        if not self.pizzeria.inventory.has_ingredients(pizza_recipe["ingredients"]):
            return 0

        # вычитаем ингредиенты
        self.pizzeria.inventory.consume(pizza_recipe["ingredients"])

        # выбираем свободную печь
        oven = next((o for o in self.ovens if o.is_available()), None)
        if not oven:
            return 0

        cook_time = oven.get_cook_time()
        oven.use(cook_time)
        pizza = Pizza(pizza_name)
        return cook_time

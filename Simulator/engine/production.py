# engine/production.py
from domain.product import Product

class Production:
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def mix_dough(self, amount_kg, now):
        """
        Замес теста. Проверяем оборудование (миксер + расстоечный холодильник)
        """
        mixer = next((e for e in self.pizzeria.equipment if e.type == "mixer"), None)
        fridge = next((e for e in self.pizzeria.equipment if e.type == "dough_fridge"), None)
        if not mixer or not fridge:
            raise ValueError("Нет оборудования для замеса теста")

        # простой расчёт времени: пропорционально количеству
        cook_time = mixer.cook_time_min * (amount_kg / mixer.capacity)
        self.pizzeria.inventory.add_product(Product("dough", amount_kg))

        # оборудование занято до now + cook_time
        mixer.busy_until = now + cook_time
        fridge.busy_until = now + cook_time  # тесто расстаивается в холодильнике
        return cook_time

    def cook(self, order):
        """
        Приготовление пиццы по рецепту
        """
        oven = next((e for e in self.pizzeria.equipment if e.type == "oven"), None)
        if not oven:
            raise ValueError("Нет печи")

        # считаем сколько пицц одновременно можно поставить в печь
        num_pizzas = 1  # на данный момент 1 пицца за раз
        cook_time = oven.cook_time_min

        # списываем ингредиенты
        for ing, amt in order.recipe["ingredients"].items():
            self.pizzeria.inventory.consume(ing, amt)

        # списываем тесто
        self.pizzeria.inventory.consume("dough", order.recipe.get("dough", 0))

        oven.busy_until += cook_time
        return cook_time

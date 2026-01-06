# engine/cooking.py
class Cooking:
    """
    Логика приготовления пиццы с учётом staff и оборудования
    """
    def __init__(self, pizzeria):
        self.pizzeria = pizzeria

    def prepare_pizza(self, order, now):
        """
        Готовим одну пиццу:
        - проверяем staff
        - проверяем оборудование
        - списываем ингредиенты
        - возвращаем время приготовления
        """
        # проверка наличия staff
        staff_member = next((s for s in self.pizzeria.staff if s.role == "cook" and s.is_available(now)), None)
        if not staff_member:
            return None  # пока нет свободного cook

        # проверка ингредиентов
        for ing, amt in order.recipe["ingredients"].items():
            if not self.pizzeria.inventory.has(ing, amt):
                return None  # ингредиентов нет

        if order.recipe.get("dough"):
            if not self.pizzeria.inventory.has("dough", order.recipe["dough"]):
                return None  # теста нет

        # списываем ингредиенты
        for ing, amt in order.recipe["ingredients"].items():
            self.pizzeria.inventory.consume(ing, amt)

        if order.recipe.get("dough"):
            self.pizzeria.inventory.consume("dough", order.recipe["dough"])

        # оборудование
        oven = next((e for e in self.pizzeria.equipment if e.type == "oven"), None)
        if not oven:
            return None

        # учитываем навыки staff, уменьшаем время
        skill_factor = 1 - (staff_member.skill_level * 0.05)  # например 5% ускорение за уровень
        cook_time = max(1, int(oven.cook_time_min * skill_factor))

        # помечаем staff занятым
        staff_member.busy_until = now + cook_time
        oven.busy_until = now + cook_time

        return cook_time

# simulator/work_session.py

import random

class WorkSession:
    """
    Симуляция рабочего дня пиццерии с заказами (тапами).
    """

    def __init__(self, pizzeria, taps: int = 10, duration_minutes: int = 720):
        """
        :param pizzeria: объект Pizzeria
        :param taps: количество тапов (заказов)
        :param duration_minutes: длительность сессии в минутах
        """
        self.pizzeria = pizzeria
        self.duration = duration_minutes
        self.taps = taps
        self.orders_queue = self.generate_orders()

    def generate_orders(self):
        """
        Генерация случайной очереди заказов.
        Каждый заказ содержит 1–4 пиццы.
        """
        orders = []
        pizza_types = ["margarita", "pepperoni"]
        for _ in range(self.taps):
            count = random.randint(1, 4)
            pizzas = [random.choice(pizza_types) for _ in range(count)]
            orders.append({"pizzas": pizzas, "remaining_time": self.calc_prep_time(count)})
        return orders

    @staticmethod
    def calc_prep_time(count):
        """Время приготовления заказа по количеству пицц (в минутах)"""
        if count == 1:
            return 15
        elif count == 2:
            return 25
        elif count == 3:
            return 35
        else:
            return 40

    def run(self):
        """
        Запуск сессии.
        Обрабатывает заказы, замес теста, порчу продуктов, энергию.
        """
        report = {
            "energy_kwh": 0.0,
            "dough_moved_to_table_kg": 0.0,
            "table_returned_to_fridge_kg": 0.0,
            "spoiled_kg": 0.0,
            "completed_orders": 0,
            "failed_orders": 0
        }

        for minute in range(1, self.duration + 1):
            # 1️⃣ Энергия оборудования за минуту
            self.pizzeria.energy.add(self.pizzeria.calculate_energy_per_minute())

            # 2️⃣ Наполнение стола из холодильника при необходимости
            moved = self.pizzeria.fill_table_if_needed()
            report["dough_moved_to_table_kg"] += moved

            # 3️⃣ Замес теста если меньше минимума
            if self.pizzeria.proofing_fridge.current_load < self.pizzeria.dough_mixer.min_load:
                kg_to_mix = self.pizzeria.dough_mixer.mix(20)
                self.pizzeria.proofing_fridge.add(kg_to_mix)

            # 4️⃣ Проверка порчи продуктов каждый час
            if minute % 60 == 0:
                spoiled = self.pizzeria.check_spoilage()
                report["spoiled_kg"] += spoiled

            # 5️⃣ Обработка текущего заказа
            if self.orders_queue:
                order = self.orders_queue[0]
                # Проверяем есть ли тесто и ингредиенты на столе
                can_make = True
                for pizza in order["pizzas"]:
                    recipe = self.pizzeria.production.recipes[f"pizza_{pizza}"]
                    if self.pizzeria.proofing_fridge.current_load < recipe["dough"]:
                        can_make = False
                        break
                    for ing, kg in recipe.items():
                        if ing != "dough" and self.pizzeria.table.current_load < kg:
                            can_make = False
                            break
                if can_make:
                    # Списываем тесто
                    for pizza in order["pizzas"]:
                        recipe = self.pizzeria.production.recipes[f"pizza_{pizza}"]
                        self.pizzeria.proofing_fridge.remove(recipe["dough"])
                        self.pizzeria.table.empty()  # упрощаем списание ингредиентов
                    order["remaining_time"] -= 1
                    if order["remaining_time"] <= 0:
                        report["completed_orders"] += 1
                        self.orders_queue.pop(0)
                else:
                    report["failed_orders"] += 1
                    self.orders_queue.pop(0)

        # 6️⃣ Итоговая энергия
        report["energy_kwh"] = self.pizzeria.energy.report()

        # 7️⃣ Возврат остатков со стола в холодильник
        report["table_returned_to_fridge_kg"] = self.pizzeria.return_table_to_fridge()

        return report

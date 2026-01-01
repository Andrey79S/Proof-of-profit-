# simulator/work_session.py

class WorkSession:
    """
    Симуляция рабочего дня пиццерии.
    Управляет энергией, тестом, столом и порчей продуктов.
    """

    def __init__(self, pizzeria, duration_minutes: int = 720):
        """
        :param pizzeria: объект Pizzeria
        :param duration_minutes: продолжительность сессии в минутах (по умолчанию 12 часов)
        """
        self.pizzeria = pizzeria
        self.duration = duration_minutes

    def run(self):
        """
        Запускает симуляцию.
        Возвращает словарь с отчётом: энергия, перемещения теста, порча продуктов и остаток на столе.
        """
        report = {
            "energy_kwh": 0.0,
            "dough_moved_to_table_kg": 0.0,
            "table_returned_to_fridge_kg": 0.0,
            "spoiled_kg": 0.0
        }

        for minute in range(1, self.duration + 1):
            # 1️⃣ Энергия оборудования за минуту
            energy_per_min = self.pizzeria.calculate_energy_per_minute()
            self.pizzeria.energy.add(energy_per_min)

            # 2️⃣ Наполнение стола из холодильника, если меньше 30%
            moved = self.pizzeria.fill_table_if_needed()
            report["dough_moved_to_table_kg"] += moved

            # 3️⃣ Замес теста если в расстоечном холодильнике меньше минимума
            if self.pizzeria.proofing_fridge.current_load < self.pizzeria.dough_mixer.min_load:
                kg_to_mix = self.pizzeria.dough_mixer.mix(20)  # базовый замес
                self.pizzeria.proofing_fridge.add(kg_to_mix)

            # 4️⃣ Проверка порчи продуктов раз в 60 минут (каждый час)
            if minute % 60 == 0:
                spoiled = self.pizzeria.check_spoilage()
                report["spoiled_kg"] += spoiled

        # 5️⃣ Итоговая энергия
        report["energy_kwh"] = self.pizzeria.energy.report()

        # 6️⃣ Возврат остатков со стола в холодильник
        report["table_returned_to_fridge_kg"] = self.pizzeria.return_table_to_fridge()

        return report

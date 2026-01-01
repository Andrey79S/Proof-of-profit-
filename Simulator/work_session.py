# simulator/work_session.py

from datetime import datetime, timedelta
import random

class WorkSession:
    def __init__(self, pizzeria, duration_minutes=720):
        """
        pizzeria: объект Pizzeria (в нём все холодильники, стол, тестомес, печь)
        duration_minutes: длительность сессии (по умолчанию 12 часов)
        """
        self.pizzeria = pizzeria
        self.duration_minutes = duration_minutes
        self.current_minute = 0
        self.active = False
        self.session_report = {
            "energy_consumed": 0.0,
            "orders_processed": 0,
            "orders_lost": 0,
            "pizzas_baked": 0,
            "ingredient_losses": 0,
            "dough_prepared": 0
        }

    def start(self):
        """Запуск сессии"""
        self.active = True
        print(f"⚡ Сессия начата на {self.duration_minutes} минут")

        # Наполнение стола
        self.pizzeria.fill_table_if_needed()

        # Замес теста при старте сессии
        self._try_dough_mix()

        # Перемещение готового теста в зону готовки
        self.pizzeria.load_ready_dough_to_cooking_area()

    def tick(self):
        """Обновление каждой минуты"""
        if not self.active:
            return

        # Увеличиваем текущую минуту
        self.current_minute += 1

        # Энергия: печь, стол, холодильники
        self.session_report["energy_consumed"] += self.pizzeria.calculate_energy_per_minute()

        # Стол: автозаполнение при достижении минимума
        self.pizzeria.fill_table_if_needed()

        # Тесто: замес при необходимости
        self._try_dough_mix()

        # Перемещение готового теста в зону готовки
        self.pizzeria.load_ready_dough_to_cooking_area()

        # Порча продуктов
        self.pizzeria.check_spoilage()

    def run(self):
        """Полная сессия от старта до конца"""
        self.start()
        while self.current_minute < self.duration_minutes:
            self.tick()
        self.end()
        return self.session_report

    def end(self):
        """Завершение сессии"""
        self.active = False
        # Остатки со стола возвращаются в холодильник
        self.pizzeria.return_table_to_fridge()
        # Финальная проверка порчи продуктов
        self.pizzeria.check_spoilage()
        print(f"✅ Сессия завершена. Энергия потрачена: {self.session_report['energy_consumed']:.2f} кВт·ч")

    def _try_dough_mix(self):
        """
        Проверяем, нужно ли делать замес:
        - есть место в расстоечном холодильнике
        - есть возможность минимального замеса
        - сессия активна
        """
        fridge = self.pizzeria.proofing_fridge
        if not self.active:
            return

        min_load = self.pizzeria.dough_mixer.min_load
        max_load = self.pizzeria.dough_mixer.max_load
        available_space = fridge.max_load - fridge.current_load

        if available_space >= min_load:
            mix_weight = min(max_load, available_space)
            # Производим замес
            prepared_dough = self.pizzeria.dough_mixer.mix(mix_weight)
            fridge.add_dough(prepared_dough)
            self.session_report["dough_prepared"] += prepared_dough
            self.session_report["energy_consumed"] += self.pizzeria.dough_mixer.energy_per_mix()
            print(f"🍞 Замес теста: {prepared_dough} кг → расстоечный холодильник")

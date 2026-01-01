# simulator/run.py

from engine.pizzeria import Pizzeria
from work_session import WorkSession

if __name__ == "__main__":
    print("🎯 Добро пожаловать в симулятор пиццерии PoP!")

    # 1️⃣ Настройка сессии
    taps = int(input("Введите количество тапов (заказов) на сессию: "))
    duration_hours = int(input("Введите длительность сессии (часы): "))
    duration_minutes = duration_hours * 60

    # 2️⃣ Создаём пиццерию
    pizzeria = Pizzeria()

    # 3️⃣ Запуск рабочей сессии
    session = WorkSession(pizzeria, taps=taps, duration_minutes=duration_minutes)
    report = session.run()

    # 4️⃣ Вывод отчёта
    print("\n📊 Итоговый отчёт по сессии:")
    print(f"Энергия потреблена (кВт·ч): {report['energy_kwh']}")
    print(f"Тесто перемещено на стол (кг): {report['dough_moved_to_table_kg']}")
    print(f"Остатки возвращены в холодильник (кг): {report['table_returned_to_fridge_kg']}")
    print(f"Порча продуктов (кг): {report['spoiled_kg']}")
    print(f"Выполненные заказы: {report['completed_orders']}")
    print(f"Пропущенные заказы: {report['failed_orders']}")

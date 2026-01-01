# simulator/run.py

from engine.pizzeria import Pizzeria
from work_session import WorkSession

def main():
    print("🎯 Добро пожаловать в симулятор пиццерии PoP!")

    # 1️⃣ Ввод параметров сессии
    try:
        taps = int(input("Введите количество тапов (заказов) на сессию: "))
        if taps < 1:
            raise ValueError
    except ValueError:
        print("Некорректное значение. Используем 10 тапов по умолчанию.")
        taps = 10

    try:
        duration_hours = int(input("Введите длительность сессии (часы, 1–24): "))
        if duration_hours < 1 or duration_hours > 24:
            raise ValueError
    except ValueError:
        print("Некорректное значение. Используем 12 часов по умолчанию.")
        duration_hours = 12

    duration_minutes = duration_hours * 60

    # 2️⃣ Создаём пиццерию
    pizzeria = Pizzeria()

    # 3️⃣ Создаём и запускаем рабочую сессию
    session = WorkSession(pizzeria, taps=taps, duration_minutes=duration_minutes)
    report = session.run()

    # 4️⃣ Выводим итоговый отчёт
    print("\n📊 Итоговый отчёт по сессии:")
    print(f"Энергия потреблена (кВт·ч): {report['energy_kwh']:.2f}")
    print(f"Тесто перемещено на стол (кг): {report['dough_moved_to_table_kg']:.2f}")
    print(f"Остатки возвращены в холодильник (кг): {report['table_returned_to_fridge_kg']:.2f}")
    print(f"Порча продуктов (кг): {report['spoiled_kg']:.2f}")
    print(f"Выполненные заказы: {report['completed_orders']}")
    print(f"Пропущенные заказы: {report['failed_orders']}")

if __name__ == "__main__":
    main()

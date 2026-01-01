# simulator/run.py

from engine.pizzeria import Pizzeria
from work_session import WorkSession

# =========================
# Ввод количества дней
# =========================
while True:
    try:
        days = int(input("Введите количество дней для симуляции (1-365): "))
        if 1 <= days <= 365:
            break
        else:
            print("Введите число от 1 до 365")
    except ValueError:
        print("Пожалуйста, введите целое число")

# =========================
# ИНИЦИАЛИЗАЦИЯ ПИЦЦЕРИИ
# =========================
pizzeria = Pizzeria(config_folder="config")

# Каждый день = 12 часов = 720 минут
total_minutes = days * 12 * 60
session = WorkSession(pizzeria, working_minutes=total_minutes)

# =========================
# Добавим тестовые заказы для симуляции
# =========================
recipes = pizzeria.production.recipes

# Для примера: на каждый день по 5-10 случайных заказов
import random

for _ in range(days * 5):
    pizza_type = random.choice(["pizza_margarita", "pizza_pepperoni"])
    recipe = recipes[pizza_type]
    pizzas_count = random.randint(1, 4)
    cook_time = 6  # минут на пиццу
    expected_time = 10 + pizzas_count * 5  # минимальное время ожидания
    price = 0
    if pizza_type == "pizza_margarita":
        price = 12 * pizzas_count
    else:
        price = 20 * pizzas_count

    session.add_order(
        pizzas_count=pizzas_count,
        recipe=recipe,
        cook_time=cook_time,
        expected_time=expected_time,
        price=price
    )

# =========================
# ЗАПУСК СИМУЛЯЦИИ
# =========================
print(f"\nСимуляция на {days} дней ({total_minutes} минут) запущена...\n")
while session.state == session.state.ACTIVE:
    session.tick()

# =========================
# ВЫВОД ОТЧЁТА
# =========================
report = session.report
print("=== Отчёт по симуляции ===")
print(f"Всего заказов: {report['orders_total']}")
print(f"Выполнено: {report['orders_done']}")
print(f"Потеряно: {report['orders_lost']}")
print(f"Выручка: ${report['revenue']:.2f}")
print(f"Расход ингредиентов: ${report['ingredients_cost']:.2f}")
print(f"Энергия: {report['energy_kwh']:.2f} kWh")
profit = report['revenue'] - report['ingredients_cost']
print(f"Прибыль: ${profit:.2f}")

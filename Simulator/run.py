# simulator/run.py

import argparse
from engine.pizzeria import Pizzeria
from work_session import WorkSession

# =========================
# ПАРСИНГ АРГУМЕНТОВ
# =========================
parser = argparse.ArgumentParser(description="Simulate a day at the pizzeria.")
parser.add_argument(
    "--minutes",
    type=int,
    default=720,  # 12 часов * 60 минут
    help="Количество минут симуляции (по умолчанию 720 = 12 часов)"
)
args = parser.parse_args()

# =========================
# ИНИЦИАЛИЗАЦИЯ
# =========================
pizzeria = Pizzeria(config_folder="config")
session = WorkSession(pizzeria, working_minutes=args.minutes)
session.start()

# =========================
# ДОБАВЛЕНИЕ ТЕСТОВЫХ ЗАКАЗОВ
# =========================
# Для проверки: можно добавить вручную несколько заказов
# Например, 1-2 пиццы маргарита, 1 пицца пепперони
recipes = pizzeria.production.recipes
session.add_order(
    pizzas_count=2,
    recipe=recipes["pizza_margarita"],
    cook_time=6,
    expected_time=15,
    price=12.0*2
)
session.add_order(
    pizzas_count=1,
    recipe=recipes["pizza_pepperoni"],
    cook_time=6,
    expected_time=15,
    price=20.0
)

# =========================
# ОСНОВНОЙ ЦИКЛ
# =========================
print("Симуляция запущена...")
while session.state == session.state.ACTIVE:
    session.tick()

# =========================
# ОТЧЁТ
# =========================
report = session.report
print("=== Отчёт за день ===")
print(f"Всего заказов: {report['orders_total']}")
print(f"Выполнено: {report['orders_done']}")
print(f"Потеряно: {report['orders_lost']}")
print(f"Выручка: ${report['revenue']:.2f}")
print(f"Расход ингредиентов: ${report['ingredients_cost']:.2f}")
print(f"Энергия: {report['energy_kwh']:.2f} kWh")

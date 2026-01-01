from engine.pizzeria import Pizzeria
from engine.energy import EnergyTracker
from datetime import datetime
import random

# =========================
# Ввод пользователя
# =========================
while True:
    try:
        days = int(input("Введите количество дней для симуляции (1-365): "))
        if 1 <= days <= 365:
            break
        else:
            print("Введите число от 1 до 365")
    except ValueError:
        print("Введите корректное число")

# =========================
# Создание пиццерии
# =========================
pizzeria = Pizzeria(config_folder="config")
energy_tracker = EnergyTracker()

total_sales = {"margarita": 0, "pepperoni": 0}
total_costs = 0.0

# =========================
# Симуляция
# =========================
for day in range(1, days + 1):
    print(f"\n=== День {day} ===")

    # 1️⃣ Проверка порчи продуктов
    spoiled = pizzeria.check_spoilage()
    if spoiled > 0:
        print(f"Продукты испорчены: {spoiled:.2f} кг")

    # 2️⃣ Заполнение стола ингредиентами
    moved = pizzeria.fill_table_if_needed()
    if moved > 0:
        print(f"Заполнено со склада на стол: {moved:.2f} кг")

    # 3️⃣ Замес теста при необходимости
    dough_needed = 10  # пример потребности в кг для дня
    pizzeria.production.mix_dough_if_needed(dough_needed)

    # 4️⃣ Генерация заказов (1 тап = 1 заказ, 1-4 пиццы)
    orders = random.randint(5, 15)  # примерное количество тапов/заказов
    for _ in range(orders):
        qty_margarita = random.randint(0, 4)
        qty_pepperoni = random.randint(0, 4 - qty_margarita)
        report = pizzeria.production.produce_pizzas(qty_margarita, qty_pepperoni)

        # если заказ выполнен
        if sum(report["produced"].values()) > 0:
            total_sales["margarita"] += report["produced"]["margarita"]
            total_sales["pepperoni"] += report["produced"]["pepperoni"]
            total_costs += report["ingredient_cost"]

    # 5️⃣ Энергозатраты
    daily_energy = pizzeria.calculate_energy_per_minute() * 60 * 12  # 12 часов работы
    energy_tracker.add(daily_energy)
    total_costs += daily_energy * 0.1  # цена за 1 kWh

# =========================
# Итоговая статистика
# =========================
total_pizzas = total_sales["margarita"] + total_sales["pepperoni"]
profit = total_pizzas * 10 - total_costs  # 10$ за пиццу по умолчанию

print("\n=== Симуляция завершена ===")
print(f"Всего пицц: {total_pizzas}")
print(f"  Маргарита: {total_sales['margarita']}")
print(f"  Пепперони: {total_sales['pepperoni']}")
print(f"Общие затраты: {total_costs:.2f}$")
print(f"Энергозатраты: {energy_tracker.total_energy:.2f} kWh")
print(f"Прибыль: {profit:.2f}$")

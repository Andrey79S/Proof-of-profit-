# run.py

import random
from domain.pizzeria import Pizzeria
from domain.order_pool import OrderPool
from core.clock import Clock
from core.scheduler import Scheduler
from engine.simulator import SimulatorEngine


def generate_orders_for_day(order_pool: OrderPool, day_start_min: int, working_hours: int, avg_orders_per_hour: float):
    """
    Генерирует заказы на один рабочий день
    """
    total_minutes = working_hours * 60
    total_orders = int(avg_orders_per_hour * working_hours)
    
    recipes = list(pizzeria.recipes.keys())
    if not recipes:
        print("Внимание: нет загруженных рецептов!")
        return

    print(f"   → Генерация ~{total_orders} заказов на день (с {day_start_min // 60:02d}:00 до {(day_start_min + total_minutes) // 60:02d}:00)")

    for _ in range(total_orders):
        # Случайное время появления заказа в течение рабочего дня
        offset_min = random.randint(0, total_minutes - 1)
        created_at = day_start_min + offset_min

        # Случайный рецепт
        recipe = random.choice(recipes)

        # Случайное терпение клиента (30–90 минут)
        max_wait = random.randint(30, 90)

        order_pool.add_order(recipe, created_at_min=created_at, max_wait=max_wait)


# === Основная часть ===

print("🍕 Симулятор пиццерии — Настройка симуляции\n")

try:
    days = int(input("Сколько дней симулировать? (например, 7): "))
    if days < 1:
        raise ValueError
except:
    print("Некорректное значение, устанавливаю 1 день.")
    days = 1

try:
    hours_per_day = int(input("Сколько рабочих часов в день? (например, 8): "))
    if hours_per_day < 1 or hours_per_day > 24:
        raise ValueError
except:
    print("Некорректное значение, устанавливаю 8 часов.")
    hours_per_day = 8

try:
    avg_orders_per_hour = float(input("Среднее количество заказов в час? (например, 5.5): "))
    if avg_orders_per_hour < 0:
        raise ValueError
except:
    print("Некорректное значение, устанавливаю 5 заказов в час.")
    avg_orders_per_hour = 5.0


# Инициализация пиццерии
print("\nЗагрузка пиццерии и конфигов...")
pizzeria = Pizzeria(config_path="config")
pizzeria.add_initial_inventory()

order_pool = OrderPool()
pizzeria.order_pool = order_pool

clock = Clock()
scheduler = Scheduler()
pizzeria.clock = clock  # для can_accept_order и порчи

sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)

total_minutes = days * 24 * 60  # вся симуляция
working_minutes_per_day = hours_per_day * 60

print(f"\nЗапуск симуляции на {days} день(дней), {hours_per_day} ч/день")
print(f"Ожидается ~{avg_orders_per_hour * hours_per_day * days:.0f} заказов всего\n")

current_time = 0  # начало симуляции

for day in range(1, days + 1):
    print(f"\n=== День {day} ===")
    
    # Предполагаем, что работа начинается в 10:00 (можно менять)
    day_start_min = (10 * 60) + (day - 1) * 24 * 60  # 10:00 каждого дня
    
    # Генерируем заказы только на рабочие часы
    generate_orders_for_day(order_pool, day_start_min, hours_per_day, avg_orders_per_hour)
    
    # Симулируем весь день (24 часа), но заказы только в рабочее время
    day_minutes = working_minutes_per_day + 12 * 60  # +12 часов на "ночь" для порчи и т.д.
    sim.run(total_minutes=day_minutes)

# Финальный отчёт после всех дней
print("\n" + "="*50)
print("ФИНАЛЬНЫЙ ОТЧЁТ ЗА ВСЮ СИМУЛЯЦИЮ")
print("="*50)
sim.report()

# Дополнительная статистика
total_revenue = pizzeria.revenue
total_expenses = pizzeria.expenses + sim.stats["losses"]
profit = total_revenue - total_expenses

print(f"\nИтого за {days} день(дней):")
print(f"   Выручка: {total_revenue:.2f}$")
print(f"   Расходы + потери: {total_expenses:.2f}$")
print(f"   Чистая прибыль: {profit:.2f}$")
if days > 0:
    print(f"   Прибыль в день: {profit / days:.2f}$")

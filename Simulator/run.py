# simulator/run.py

import random
from engine.pizzeria import Pizzeria
from engine.energy import EnergyTracker

# ==========================
# Настройка симуляции
# ==========================
while True:
    try:
        days = int(input("Введите количество дней для симуляции (1-365): "))
        if 1 <= days <= 365:
            break
    except:
        pass
    print("Введите число от 1 до 365.")

working_hours = 12  # часы работы пиццерии в день
avg_orders_per_hour = 3  # среднее количество заказов в час

# ==========================
# Инициализация пиццерии
# ==========================
pizzeria = Pizzeria(config_folder="config")
energy_tracker = EnergyTracker()  # рабочие часы будут учитываться в расчётах вручную

# ==========================
# Итоги симуляции
# ==========================
total_orders = 0
produced_pizzas = {"margarita": 0, "pepperoni": 0}
total_cost = 0.0
total_energy_kwh = 0.0

# ==========================
# Симуляция по дням
# ==========================
for day in range(1, days + 1):
    print(f"\n=== День {day} ===")

    # ==========================
    # 1. Запуск сессии: наполняем стол, проверяем тесто
    # ==========================
    pizzeria.fill_table_if_needed()
    
    # Считаем сколько теста нужно для дня
    dough_needed = working_hours * avg_orders_per_hour * 0.2 * 2  # запас для 2 пицц/час
    pizzeria.production.mix_dough_if_needed(dough_needed)
    
    # ==========================
    # 2. Генерация заказов по часам
    # ==========================
    for hour in range(working_hours):
        orders_this_hour = random.randint(max(1, avg_orders_per_hour-1), avg_orders_per_hour+1)
        for _ in range(orders_this_hour):
            total_orders += 1
            pizza_type = random.choice(["margarita", "pepperoni"])
            qty = random.randint(1, 4)

            # Производство пицц (проверяет тесто и ингредиенты)
            report = pizzeria.production.produce_pizzas(
                margarita_qty=qty if pizza_type=="margarita" else 0,
                pepperoni_qty=qty if pizza_type=="pepperoni" else 0
            )

            # Обновляем статистику
            produced_pizzas["margarita"] += report["produced"]["margarita"]
            produced_pizzas["pepperoni"] += report["produced"]["pepperoni"]
            total_cost += report["ingredient_cost"]

    # ==========================
    # 3. Энергозатраты за день
    # ==========================
    dough_used_kg = sum(batch["kg"] for batch in pizzeria.production.dough_batches)
    energy_kwh = (
        pizzeria.oven.power_kw * working_hours +              # печь
        pizzeria.proofing_fridge.power_kw * 24 +              # холодильник теста
        pizzeria.ingredients_fridge.power_kw * 24             # холодильник ингредиентов
    )
    # замес теста
    energy_kwh += (pizzeria.dough_mixer.power_kw * (dough_needed / pizzeria.dough_mixer.max_load) * (pizzeria.dough_mixer.time_min/60))
    
    total_energy_kwh += energy_kwh

    # ==========================
    # 4. Списание просрочки
    # ==========================
    spoiled = pizzeria.check_spoilage()
    if spoiled > 0:
        print(f"Продукты испорчены: {spoiled:.2f} кг")

# ==========================
# Финальный отчет
# ==========================
revenue = produced_pizzas["margarita"]*8 + produced_pizzas["pepperoni"]*10  # примерные цены
profit = revenue - total_cost

print("\n=== Симуляция завершена ===")
print(f"Всего заказов: {total_orders}")
print(f"Всего пицц: {produced_pizzas['margarita'] + produced_pizzas['pepperoni']}")
print(f" - Маргарита: {produced_pizzas['margarita']}")
print(f" - Пепперони: {produced_pizzas['pepperoni']}")
print(f"Общие затраты на ингредиенты: {total_cost:.2f}$")
print(f"Энергозатраты: {total_energy_kwh:.2f} kWh")
print(f"Прибыль: {profit:.2f}$")

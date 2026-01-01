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

# Среднее количество заказов в час
avg_orders_per_hour = 3  
working_hours = 12  # по умолчанию рабочий день 12 часов

# ==========================
# Инициализация пиццерии
# ==========================
pizzeria = Pizzeria(config_folder="config")
energy_tracker = EnergyTracker(working_hours=working_hours)

# ==========================
# Результаты симуляции
# ==========================
total_orders = 0
produced_pizzas = {"margarita": 0, "pepperoni": 0}
total_cost = 0.0
total_energy_kwh = 0.0
profit = 0.0

# ==========================
# Симуляция по дням
# ==========================
for day in range(1, days + 1):
    print(f"\n=== День {day} ===")
    
    # Стартер: заполняем стол из холодильника
    pizzeria.fill_table_if_needed()
    
    # Замес теста, если нужно
    dough_needed = working_hours * avg_orders_per_hour * 0.2  # 200г теста на пиццу
    pizzeria.production.mix_dough_if_needed(dough_needed)
    
    # Генерация заказов по часам
    for hour in range(working_hours):
        orders_this_hour = random.randint(max(1, avg_orders_per_hour-1), avg_orders_per_hour+1)
        for _ in range(orders_this_hour):
            total_orders += 1
            pizza_type = random.choice(["margarita", "pepperoni"])
            qty = random.randint(1, 4)
            
            report = pizzeria.production.produce_pizzas(
                margarita_qty=qty if pizza_type=="margarita" else 0,
                pepperoni_qty=qty if pizza_type=="pepperoni" else 0
            )
            
            # Обновляем статистику
            produced_pizzas["margarita"] += report["produced"]["margarita"]
            produced_pizzas["pepperoni"] += report["produced"]["pepperoni"]
            total_cost += report["ingredient_cost"]
    
    # Энергозатраты за день
    dough_used_kg = sum(batch["kg"] for batch in pizzeria.production.dough_batches)
    energy_kwh = energy_tracker.total_energy + pizzeria.calculate_energy_per_minute() * 60 * working_hours
    total_energy_kwh += energy_kwh
    
    # Списание просрочки
    spoiled = pizzeria.check_spoilage()
    
# ==========================
# Финальный отчет
# ==========================
revenue = produced_pizzas["margarita"]*8 + produced_pizzas["pepperoni"]*10  # Пример цены за пиццу
profit = revenue - total_cost

print("\n=== Симуляция завершена ===")
print(f"Всего заказов: {total_orders}")
print(f"Всего пицц: {produced_pizzas['margarita'] + produced_pizzas['pepperoni']}")
print(f" - Маргарита: {produced_pizzas['margarita']}")
print(f" - Пепперони: {produced_pizzas['pepperoni']}")
print(f"Общие затраты на ингредиенты: {total_cost:.2f}$")
print(f"Энергозатраты: {total_energy_kwh:.2f} kWh")
print(f"Прибыль: {profit:.2f}$")

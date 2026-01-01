from engine.pizzeria import Pizzeria

days = int(input("Введите количество дней для симуляции (1-365): "))
orders_per_day = int(input("Сколько заказов в день: "))

pizzeria = Pizzeria()

for day in range(1, days+1):
    print(f"\n=== День {day} ===")
    pizzeria.start_day()
    orders = pizzeria.generate_orders(orders_per_day)
    for order in orders:
        pizzeria.process_order(order)

print("\n=== Симуляция завершена ===")
print(f"Всего заказов: {pizzeria.total_orders}")
print(f"Всего пицц: {sum(pizzeria.total_pizzas.values())}")
for name, qty in pizzeria.total_pizzas.items():
    print(f" - {name.capitalize()}: {qty}")

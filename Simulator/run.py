from engine.pizzeria import Pizzeria
from engine.order_pool import OrderPool

def main():
    print("=== Симулятор PoP пиццерии ===")
    days = int(input("Введите количество дней для симуляции (1-365): "))
    orders_per_day = int(input("Сколько заказов в день: "))

    order_pool = OrderPool()

    pizzeria = Pizzeria(
        name="PopPizza",
        equipment_config="config/equipment.json",
        ingredients_config="config/ingredients.json",
        recipes_config="config/recipes.json"
    )

    for day in range(1, days+1):
        print(f"\n=== День {day} ===")
        # генерация заказов
        orders = {"Margarita": orders_per_day // 2, "Pepperoni": orders_per_day // 2}
        order_pool.add_orders([orders])

        today_orders = order_pool.get_orders(orders_per_day)
        for order in today_orders:
            pizzeria.process_orders(order)

        print(f"Пицц за день: {pizzeria.total_pizzas}")

    print("\n=== Симуляция завершена ===")
    print(f"Всего заказов: {pizzeria.total_orders}")
    print(f"Всего пицц: {pizzeria.total_pizzas}")
    print(f"Энергозатраты: {pizzeria.production.energy_used:.2f} kWh")

if __name__ == "__main__":
    main()

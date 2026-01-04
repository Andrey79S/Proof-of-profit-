from engine.pizzeria import Pizzeria

def main():
    print("=== Симулятор PoP пиццерии ===")

    # --- ввод параметров ---
    while True:
        try:
            days = int(input("Введите количество дней для симуляции (1-365): "))
            if 1 <= days <= 365:
                break
        except ValueError:
            pass
        print("Ошибка. Введите число от 1 до 365.")

    while True:
        try:
            orders_per_day = int(input("Сколько заказов в день: "))
            if orders_per_day > 0:
                break
        except ValueError:
            pass
        print("Ошибка. Введите положительное число.")

    # --- запуск ---
    pizzeria = Pizzeria(config_folder="config")

    total_ingredient_cost = 0.0
    total_energy_kwh = 0.0

    for day in range(1, days + 1):
        print(f"\n=== День {day} ===")

        # 👉 готовим тесто заранее под ожидаемую нагрузку
        # 1 заказ ~ 2.5 пиццы ~ 0.5 кг теста
        expected_dough = orders_per_day * 0.5
        mix_report = pizzeria.production.mix_dough_if_needed(expected_dough)

        if mix_report["mixes"] > 0:
            print(
                f"Замесов: {mix_report['mixes']}, "
                f"Произведено теста: {mix_report['produced_kg']} кг, "
                f"Стоимость теста: {mix_report['cost']}$"
            )
            total_ingredient_cost += mix_report["cost"]

        # 👉 обрабатываем заказы дня
        day_report = pizzeria.process_orders_day(orders_per_day)

        total_ingredient_cost += day_report["ingredient_cost"]
        total_energy_kwh += day_report["energy_kwh"]

        print(
            f"Пицц за день: "
            f"Margarita={day_report['pizzas']['Margarita']}, "
            f"Pepperoni={day_report['pizzas']['Pepperoni']}"
        )

        # 👉 старение теста (порча)
        spoiled = pizzeria.production.age_dough()
        if spoiled > 0:
            print(f"Испорчено теста: {round(spoiled, 2)} кг")

    # --- итоги ---
    revenue = pizzeria.total_sales
    profit = revenue - total_ingredient_cost

    print("\n=== Симуляция завершена ===")
    print(f"Всего заказов: {pizzeria.total_orders}")
    print(f"Всего пицц: {sum(pizzeria.total_pizzas.values())}")
    print(f" - Margarita: {pizzeria.total_pizzas['Margarita']}")
    print(f" - Pepperoni: {pizzeria.total_pizzas['Pepperoni']}")
    print(f"Выручка: {round(revenue, 2)}$")
    print(f"Затраты на ингредиенты: {round(total_ingredient_cost, 2)}$")
    print(f"Энергозатраты: {round(total_energy_kwh, 2)} kWh")
    print(f"Прибыль (без учета аренды/персонала): {round(profit, 2)}$")


if __name__ == "__main__":
    main()

from domain.inventory import Inventory
from domain.equipment import DoughMixer
from engine.production import Production
from engine.cooking import Cooking
from engine.simulator import Simulator
from domain.order import Order

def main():
    print("=== Симулятор PoP пиццерии ===")
    days = int(input("Введите количество дней для симуляции (1-365): "))
    orders_per_day = int(input("Сколько заказов в день: "))

    # Инициализация
    inventory = Inventory()
    mixer = DoughMixer(min_load=15, max_load=35, power_kw=3, time_min=15)
    production = Production(inventory, mixer)
    cooking = Cooking(production.dough_storage)
    sim = Simulator(production, cooking)

    for day in range(1, days+1):
        print(f"\n=== День {day} ===")
        orders = [Order("Margarita", created_at=0, max_wait=60) for _ in range(orders_per_day//2)]
        orders += [Order("Pepperoni", created_at=0, max_wait=60) for _ in range(orders_per_day//2)]
        sim.add_orders(orders)
        sim.run_day()

if __name__ == "__main__":
    main()

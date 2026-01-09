# run.py

from core.clock import Clock
from core.config_loader import ConfigLoader
from domain.pizzeria import Pizzeria
from app.offline import apply_offline
from app.daily import run_daily
from persistence.state import save_state, load_state

def main():
    print("🍕 Симулятор Proof-of-Profit (MVP) запущен")

    loader = ConfigLoader()
    clock = Clock()

    pizzeria = load_state(loader) or Pizzeria(loader)
    pizzeria.clock = clock

    apply_offline(pizzeria)

    run_daily(pizzeria)

    save_state(pizzeria)

    print(f"\nЗавершено. Прибыль: {pizzeria.finance.net_profit():.2f}$")
    print(f"Состояние сохранено в state.json")

if __name__ == "__main__":
    main()

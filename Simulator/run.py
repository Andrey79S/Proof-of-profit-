# run.py

from core.clock import Clock
from core.config_loader import ConfigLoader
from domain.pizzeria import Pizzeria
from app.offline import apply_offline
from app.daily import run_daily
from persistence.state import save_state, load_state

def main():
    print("🍕 Запуск симулятора пиццерии (Proof-of-Profit MVP)")

    loader = ConfigLoader()
    clock = Clock()

    # Загрузка состояния или новая пиццерия
    pizzeria = load_state(loader) or Pizzeria(loader)
    pizzeria.clock = clock

    # Оффлайн-процессы (с последнего запуска)
    apply_offline(pizzeria)

    # Рабочий день
    run_daily(pizzeria)

    # Сохранение
    save_state(pizzeria)

    print("\nСимуляция завершена. Состояние сохранено в state.json")

if __name__ == "__main__":
    main()

# app/offline.py

from engine.spoilage import apply_spoilage
from engine.energy import calculate_energy

def apply_offline(pizzeria):
    now = pizzeria.clock.now()
    # Пример: 12 часов оффлайн
    delta = 12 * 60
    calculate_energy(pizzeria, delta)
    apply_spoilage(pizzeria, now + delta)
    pizzeria.clock.tick(delta)
    print("Оффлайн-процессы применены (12 часов)")

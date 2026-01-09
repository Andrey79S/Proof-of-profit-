from engine.spoilage import apply_spoilage
from engine.energy import calculate_energy

def apply_offline(pizzeria):
    delta = 12 * 60  # 12 часов оффлайн
    calculate_energy(pizzeria, delta)
    apply_spoilage(pizzeria, pizzeria.clock.now() + delta)
    pizzeria.clock.tick(delta)

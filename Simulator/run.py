from core.clock import Clock
from domain.pizzeria import Pizzeria
from persistence.state import PizzeriaState

clock = Clock()
pizzeria = Pizzeria()
pizzeria.add_initial_inventory()

PizzeriaState.save(pizzeria, clock)

clock.tick(120)

delta = PizzeriaState.load(pizzeria, clock)
print("offline delta:", delta)

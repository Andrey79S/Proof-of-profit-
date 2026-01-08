from engine.simulator import SimulatorEngine
from core.clock import Clock
from core.scheduler import Scheduler

def simulate_day(pizzeria, order_pool, hours: int = 8):
    clock = Clock()
    scheduler = Scheduler()
    sim = SimulatorEngine(pizzeria, order_pool, clock, scheduler)
    sim.run(hours * 60)

from core.clock import Clock
from core.scheduler import Scheduler
from core.event import Event

clock = Clock()
scheduler = Scheduler(clock)

def hello():
    print(f"Привет! Время = {clock.now} мин")

scheduler.schedule(Event(10, hello))
scheduler.schedule(Event(30, hello))

scheduler.run_until(60)

import heapq
from core.clock import Clock
from core.event import Event

class Scheduler:
    def __init__(self):
        self.events = []  # Мин-куча: (time, event)

    def add_event(self, event: Event):
        heapq.heappush(self.events, (event.time, event))

    def run_until(self, clock: Clock, end_time: int):
        while self.events and clock.now() < end_time:
            event_time, event = heapq.heappop(self.events)
            if event_time > clock.now():
                clock.tick(event_time - clock.now())
            event.trigger()

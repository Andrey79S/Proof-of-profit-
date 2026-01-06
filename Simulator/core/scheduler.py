# core/scheduler.py
import heapq

class Scheduler:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        heapq.heappush(self.events, (event.time, event))

    def run_until(self, clock, end_time):
        while self.events and clock.now() < end_time:
            event_time, event = heapq.heappop(self.events)
            if event_time >= clock.now():
                clock.tick(event_time - clock.now())
                event.trigger()

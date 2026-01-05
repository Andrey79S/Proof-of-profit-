# core/scheduler.py
import heapq

class Scheduler:
    def __init__(self):
        self.events = []

    def schedule(self, event):
        heapq.heappush(self.events, (event.time, event))

    def run(self, until_minute):
        while self.events and self.events[0][0] <= until_minute:
            _, event = heapq.heappop(self.events)
            event.execute()

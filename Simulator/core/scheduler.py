import heapq

class Scheduler:
    def __init__(self, clock):
        self.clock = clock
        self.queue = []

    def schedule(self, event):
        heapq.heappush(self.queue, (event.time, event))

    def run_until(self, end_time):
        while self.queue and self.queue[0][0] <= end_time:
            time, event = heapq.heappop(self.queue)
            self.clock.now = time
            event.callback()

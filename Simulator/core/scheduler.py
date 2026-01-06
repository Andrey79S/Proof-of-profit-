class Scheduler:
    def __init__(self):
        self.events = []

    def schedule(self, event):
        self.events.append(event)
        self.events.sort(key=lambda e: e.time)

    def run_pending(self, now):
        to_run = [e for e in self.events if e.time <= now]
        for e in to_run:
            e.run()
            self.events.remove(e)

class Scheduler:
    def __init__(self):
        self.queue = []  # список (time, callback)
        self.now = 0

    def schedule(self, time: int, callback):
        self.queue.append((time, callback))

    def tick(self):
        """Выполнить события на текущую минуту"""
        for event in list(self.queue):
            if event[0] <= self.now:
                event[1]()  # вызываем callback
                self.queue.remove(event)
        self.now += 1

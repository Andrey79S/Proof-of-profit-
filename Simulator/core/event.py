# core/event.py
class Event:
    def __init__(self, time, callback, description=""):
        self.time = time
        self.callback = callback
        self.description = description

    def trigger(self):
        self.callback()

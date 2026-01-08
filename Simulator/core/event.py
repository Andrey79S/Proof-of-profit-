from typing import Callable

class Event:
    def __init__(self, time: int, callback: Callable, description: str = ""):
        self.time = time
        self.callback = callback
        self.description = description

    def trigger(self):
        self.callback()

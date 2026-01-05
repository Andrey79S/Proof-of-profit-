# core/event.py
class Event:
    def __init__(self, time, callback, *args, **kwargs):
        self.time = time
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        self.callback(*self.args, **self.kwargs)

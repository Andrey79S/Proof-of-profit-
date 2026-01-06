class Event:
    def __init__(self, time, callback, *args, **kwargs):
        self.time = time
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.callback(*self.args, **self.kwargs)

class Event:
    def __init__(self, time: int, callback, description=""):
        self.time = time
        self.callback = callback
        self.description = description

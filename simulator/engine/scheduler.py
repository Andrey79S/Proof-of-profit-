# engine/scheduler.py
import threading
import time

class Scheduler:
    """
    Простой планировщик для авто-тиков
    """
    def __init__(self, game_loop, tick_interval_sec: int = 5):
        self.game_loop = game_loop
        self.tick_interval_sec = tick_interval_sec
        self._stop = False

    def start(self):
        def loop():
            while not self._stop:
                self.game_loop.tick()
                time.sleep(self.tick_interval_sec)
        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self._stop = True

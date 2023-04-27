from time import time
class Timer:
    def __init__(self):
        self.clock = 0.0
        self.end_time = 0.0
        self.active = False

    def start(self, end: float):
        self.end_time = end
        self.active = True

    def update(self, dt):
        if self.active:
            self.clock += dt
        if self.clock >= self.end_time:
            self.active = False
            self.reset()

    def reset(self):
        self.clock = 0.0

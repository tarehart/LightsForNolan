class CooldownHelper:
    def __init__(self, cooldown_millis):
        self.cooldown_millis = cooldown_millis
        self.timer = 0

    def update(self, elapsed_millis: int):
        self.timer += elapsed_millis

    def is_ready(self):
        return self.timer >= self.cooldown_millis

    def elapsed_millis(self):
        return self.timer

    def reset(self):
        self.timer = 0

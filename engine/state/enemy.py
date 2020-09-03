import engine.toolkit.dot


class Enemy:

    def __init__(self, state):
        self.state = state
        self.dot = None

    def apply_dot(self, dot):
        self.dot = dot

    def has_dot(self):
        return self.dot is not None and self.dot.duration > 0

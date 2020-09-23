class Enemy:

    def __init__(self, state):
        self.dot_duration = 0.0
        self.state = state
        self.damage_taken = 0.0

    def apply_dot(self, dot):
        self.dot_duration = dot.duration

    def has_dot(self):
        return self.dot_duration > 0

    # TODO add pandemic check
    def extend_dot(self, extend_duration, max_dot_duration):
        self.dot_duration = max_dot_duration if self.dot_duration + extend_duration > max_dot_duration else \
            self.dot_duration + extend_duration

    def take_damage(self, damage):
        self.damage_taken = self.damage_taken + damage

    def decay_dot(self, duration):
        self.dot_duration = self.dot_duration - duration

    @property
    def dot_duration(self):
        return self.dot_duration

    @dot_duration.setter
    def dot_duration(self, value):
        self.dot_duration = value

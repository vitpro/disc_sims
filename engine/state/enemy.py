import engine.toolkit.dot


class Enemy:

    def __init__(self, state):
        self.dot_duration = 0.0
        self.state = state
        self.damage_taken = 0.0

    def apply_dot(self, dot):
        self.dot_duration = dot.duration

    def has_dot(self):
        return self.dot_duration > 0
    
    def extend_dot(self, extend_duration):
        self.dot_duration = self.dot_duration + extend_duration

    def take_damage(self, sp):   # TODO convert sp into actual numbers maybe? idk
        self.damage_taken = self.damage_taken + sp

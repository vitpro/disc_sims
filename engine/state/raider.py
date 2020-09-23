class Raider:

    def __init__(self, state):
        self.state = state
        self.hp = 0.0
        self.atonement_duration = 0.0

    def apply_atonement(self, duration):
        self.atonement_duration = duration

    def get_atonement_duration(self):
        return self.atonement_duration

    @property
    def hp(self):
        return self.hp

    def has_atonement(self):
        return self.atonement_duration > 0

    def __str__(self):
        return '{ ' + str(self.hp) + ' / ' + str(self.atonement_duration) + 'sec } '

    def heal(self, healing):
        self.hp = self.hp + healing
        pass

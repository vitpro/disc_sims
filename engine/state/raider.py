class Raider:

    def __init__(self):
        self.hp = 0.0
        self.atonement_duration = 0.0

    def apply_atonement(self, duration):
        self.atonement_duration = duration

    def get_atonement_duration(self):
        return self.atonement_duration

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp

    def __str__(self):
        return '{ ' + str(self.hp) + ' / ' + str(self.atonement_duration) + 'sec } '

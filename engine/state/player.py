class Player:

    def __init__(self, stats):
        self.vers = stats['VERS']
        self.mastery = stats['MASTERY']
        self.haste = stats['HASTE']
        self.crit = stats['CRIT']

    @property
    def vers(self):
        return self.vers

    @property
    def mastery(self):
        return self.mastery

    @property
    def haste(self):
        return self.haste

    @property
    def crit(self):
        return self.crit

    @vers.setter
    def vers(self, v):
        self.vers = v

    @mastery.setter
    def mastery(self, v):
        self.mastery = v

    @haste.setter
    def haste(self, value):
        self.haste = value

    @crit.setter
    def crit(self, value):
        self.crit = value


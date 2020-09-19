class Player:

    '''
    TODO CERE what's a good way to represent these? would be int stat values that we convert into %, 
    or work with % straight away? (would probably be more precise to do ints and calculate here if we get some procs)
    '''
    def __init__(self, stats):
        self.stats = stats
        self._vers = stats['VERS']
        self._mastery = stats['MASTERY']
        self._haste = stats['HASTE']
        self._crit = stats['CRIT']

    @property
    def vers(self):
        return self._vers

    @property
    def mastery(self):
        return self._mastery

    @property
    def haste(self):
        return self._haste

    @property
    def crit(self):
        return self._crit

    @vers.setter
    def vers(self, v):
        self._vers = v

    @mastery.setter
    def mastery(self, v):
        self._mastery = v

    @haste.setter
    def haste(self, value):
        self._haste = value

    @crit.setter
    def crit(self, value):
        self._crit = value

    ''' TOOD CERE do these stat multipliers'''
    def get_haste_multiplier(self):
        return self.stats['HASTE']   # TODO CERE convert to double, i.e. X units/20% haste returns 1.2

    def get_crit_multiplier(self):
        return self.stats['CRIT']

    def get_mastery_multiplier(self):
        return self.stats['MASTERY']

    def get_vers_multiplier(self):
        return self.stats['VERS']

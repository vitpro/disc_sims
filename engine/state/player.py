class Player:

    '''
    
    mastery point is 35
    disc mastery 26
    haste 33
    crit 35
    vers 40
    leech 21

    '''

    def __init__(self, stats, race):
        self.stats = stats
        self.int = stats['INT']
        self.vers = stats['VERS']
        self.mastery = stats['MASTERY']
        self.haste = stats['HASTE']
        self.crit = stats['CRIT']
        self.leech = stats['LEECH']
        self.int_mod = 1.0
        self.vers_mod = 1.0
        self.mastery_mod = 1.0
        if race == 'GOBLIN' or 'NIGHTELF_NIGHT':
            self.haste_mod = 1.01
        else:
            self.haste_mod= 1.0
        if race == 'BLOODELF' or 'NIGHTELF_DAY':
            self.crit_mod = 1.01
        else:
            self.crit_mod = 1.0

    @int_mod.setter
    def int_mod(self, v):
        self._int_mod = v

    @vers_mod.setter
    def vers_mod(self, v):
        self._vers_mod = v

    @mastery_mod.setter
    def mastery_mod(self, v):
        self._mastery_mod = v

    @haste_mod.setter
    def haste_mod(self, value):
        self._haste_mod = value

    @crit_mod.setter
    def crit_mod(self, value):
        self._haste_mod = value

    @int.setter
    def int(self, v):
        self._int = v

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

    @leech.setter
    def leech(self, value):
        self._leech = value

    def get_sp(self):
        sp = self._int_mod * self._int
        return sp

    def get_haste_multiplier(self):
        base_haste_multiplier = (self._haste / 33) / 100
        if base_haste_multiplier <= 0.25:
            haste_multiplier = self._haste_mod + self._haste_mod * (self._haste / 33) / 100
        elif base_haste_multiplier <= 0.35:
            haste_multiplier = self._haste_mod + self._haste_mod * (25 + (self._haste - 825) * 0.9 / 33) / 100
        elif base_haste_multiplier <= 0.45:
            haste_multiplier = self._haste_mod + self._haste_mod * (34 + (self._haste - 1155) * 0.8 / 33) / 100
        elif base_haste_multiplier <= 0.55:
            haste_multiplier = self._haste_mod + self._haste_mod * (42 + (self._haste - 1485) * 0.7 / 33) / 100
        elif base_haste_multiplier <= 1.50:
            haste_multiplier = self._haste_mod + self._haste_mod * (49 + (self._haste - 1815) * 0.6 / 33) / 100
        else:
            haste_multiplier = self._haste_mod + self._haste_mod * 1.06
        return haste_multiplier

    def get_crit_multiplier(self):
        base_crit_multiplier = (self._crit / 35) / 100
        if base_crit_multiplier <= 0.25:
            crit_multiplier = (0.05 + self._crit_mod) + self._crit_mod * (self._crit / 35) / 100
        elif base_crit_multiplier <= 0.35:
            crit_multiplier = (0.05 + self._crit_mod) + self._crit_mod * (25 + (self._crit - 875) * 0.9 / 35) / 100
        elif base_crit_multiplier <= 0.45:
            crit_multiplier = (0.05 + self._crit_mod) + self._crit_mod * (34 + (self._crit - 1225) * 0.8 / 35) / 100
        elif base_crit_multiplier <= 0.55:
            crit_multiplier = (0.05 + self._crit_mod) + self._crit_mod * (42 + (self._crit - 1575) * 0.7 / 35) / 100
        elif base_crit_multiplier <= 1.50:
            crit_multiplier = (0.05 + self._crit_mod) + self._crit_mod * (49 + (self._crit - 1915) * 0.6 / 35) / 100
        else:
            crit_multiplier = (0.05 + self._crit_mod) + self._crit_mod * 1.06
        return crit_multiplier

    def get_mastery_multiplier(self):
        base_mastery_multiplier = (self._mastery / 35) / 100
        if base_mastery_multiplier <= 0.25:
            mastery_multiplier = (0.108 + self._mastery_mod) + self._mastery_mod * (35 / 26) * (self._mastery / 35) / 100
        elif base_mastery_multiplier <= 0.35:
            mastery_multiplier = (0.108 + self._mastery_mod) + self._mastery_mod * (35 / 26) * (25 + (self._mastery - 875) * 0.9 / 35) / 100
        elif base_mastery_multiplier <= 0.45:
            mastery_multiplier = (0.108 + self._mastery_mod) + self._mastery_mod * (35 / 26) * (34 + (self._mastery - 1225) * 0.8 / 35) / 100
        elif base_mastery_multiplier <= 0.55:
            mastery_multiplier = (0.108 + self._mastery_mod) + self._mastery_mod * (35 / 26) * (42 + (self._mastery - 1575) * 0.7 / 35) / 100
        elif base_mastery_multiplier <= 1.50:
            mastery_multiplier = (0.108 + self._mastery_mod) + self._mastery_mod * (35 / 26) * (49 + (self._mastery - 1915) * 0.6 / 35) / 100
        else:
            mastery_multiplier = (0.108 + self._mastery_mod) + self._mastery_mod * (35 / 26) * 1.06
        return mastery_multiplier

    def get_vers_multiplier(self):
        base_vers_multiplier = (self._vers / 40) / 100
        if base_vers_multiplier <= 0.25:
            vers_multiplier = self._vers_mod + self._vers_mod * (self._vers / 40) / 100
        elif base_vers_multiplier <= 0.40:
            vers_multiplier = self._vers_mod + self._vers_mod * (25 + (self._vers - 1000) * 0.9 / 40) / 100
        elif base_vers_multiplier <= 0.45:
            vers_multiplier = self._vers_mod + self._vers_mod * (34 + (self._vers - 1400) * 0.8 / 40) / 100
        elif base_vers_multiplier <= 0.55:
            vers_multiplier = self._vers_mod + self._vers_mod * (42 + (self._vers - 1800) * 0.7 / 40) / 100
        elif base_vers_multiplier <= 1.50:
            vers_multiplier = self._vers_mod + self._vers_mod * (49 + (self._vers - 2200) * 0.6 / 40) / 100
        else:
            vers_multiplier = self._vers_mod + self._vers_mod * 1.06
        return vers_multiplier

    def get_leech_multiplier(self):
        return (self._leech / 21) / 100
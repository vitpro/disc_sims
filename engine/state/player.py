from disc_sims.settings import SECONDARY_DRS, SECONDARY_SCALING

class Player:

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
        if race == 'TAUREN' or 'DWARF':
            self.crit_dmg_modifier = 2.04
        else:
            self.crit_dmg_modifier = 2.0

    @property
    def int_mod(self):
        return self._int_mod

    @property
    def vers_mod(self):
        return self._vers_mod

    @property
    def mastery_mod(self):
        return self._mastery_mod

    @property
    def haste_mod(self):
        return self._haste_mod

    @property
    def crit_mod(self):
        return self._haste_mod

    @property
    def int(self):
        return self._int

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

    @property
    def leech(self):
        return self._leech


    @int_mod.setter
    def int_mod(self, value):
        self._int_mod += value

    @vers_mod.setter
    def vers_mod(self, value):
        self._vers_mod += value

    @mastery_mod.setter
    def mastery_mod(self, value):
        self._mastery_mod += value

    @haste_mod.setter
    def haste_mod(self, value):
        self._haste_mod += value

    @crit_mod.setter
    def crit_mod(self, value):
        self._haste_mod += value

    @int.setter
    def int(self, value):
        self._int += value

    @vers.setter
    def vers(self, value):
        self._vers += value

    @mastery.setter
    def mastery(self, value):
        self._mastery += value

    @haste.setter
    def haste(self, value):
        self._haste += value

    @crit.setter
    def crit(self, value):
        self._crit += value

    @leech.setter
    def leech(self, value):
        self._leech += value

    def get_sp(self):
        sp = self._int_mod * self._int
        return sp

    def get_crit_dmg_modifier(self):
        return self.crit_dmg_modifier

    def get_haste_multiplier(self):
        haste_from_rating = self.calc_secondary_drs(self._haste, SECONDARY_SCALING('HASTE')) / 100
        haste_multiplier = self._haste_mod + self._haste_mod * haste_from_rating
        return haste_multiplier

    def get_crit_multiplier(self):
        crit_from_rating = self.calc_secondary_drs(self._crit, SECONDARY_SCALING('CRIT')) / 100
        crit_multiplier = 0.05 + self._crit_mod + self._crit_mod * crit_from_rating
        return crit_multiplier

    def get_mastery_multiplier(self):
        # secondary DRs determined based on "mastery points" (equal for every spec)
        mastery_from_rating = self.calc_secondary_drs(self._mastery, SECONDARY_SCALING('MASTERY')) / 100
        # disc base mastery and mastery scaling applied
        mastery_multiplier = 0.108 + self._mastery_mod + self._mastery_mod * (SECONDARY_SCALING('MASTERY') / SECONDARY_SCALING('DISC_MASTERY')) * mastery_from_rating
        return mastery_multiplier

    def get_vers_multiplier(self):
        vers_from_rating = self.calc_secondary_drs(self._vers, SECONDARY_SCALING('VERS')) / 100
        vers_multiplier = self._vers_mod + self._vers_mod * vers_from_rating
        return vers_multiplier

    def get_leech_multiplier(self):
        return (self._leech / 21) / 100

    def calc_secondary_drs(self, rating, coefficient):
        remaining = rating
        stat_percent = 0.0
        for i in SECONDARY_DRS:
            r = min((i[1] - i[0]) * (coefficient / i[2]), remaining)
            stat_percent += r / (coefficient / i[2])
            remaining -= r
            if not remaining:
                break
        return stat_percent
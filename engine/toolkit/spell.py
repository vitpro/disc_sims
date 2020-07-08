
class Spell:

    def __init__(self, spell_name, cast_time, mana_cost, sp):
        self.spell_name = spell_name
        self.cast_time = cast_time
        self.mana_cost = mana_cost
        self.sp = sp

    def get_cast_time(self, haste_value):
        return self.base_cast_time / (1 + haste_value / 100)

    def __str__(self):
        return self.spell_name

from django.db import models
#from django.contrib.postgres.fields import ArrayField


class Spell(models.Model):
    name = models.CharField(max_length=255, unique=True)
    mana_cost = models.DecimalField(max_digits=6, decimal_places=3)
    spell_id = models.IntegerField(default=0, unique=True)

    def get_spell_name(self):
        return self.name

    def get_mana_cost(self):
        return self.mana_cost

    def __eq__(self, other):
        return self.name == other.name and self.spell_id == other.spell_id

    def __str__(self):
        return '%s[%d]' % (self.name, self.spell_id)

    class Meta:
        abstract = True


class Dot(Spell):
    duration = models.IntegerField(default=0)
    initial_hit_sp = models.DecimalField(max_digits=10, decimal_places=2)
    ticks_sp = models.DecimalField(max_digits=10, decimal_places=2)
    # end of duration to indicate it's a dot that benefits from haste, pets have a chance to hit instead
    end_of_duration_tick = models.BooleanField(default=True)

    def get_dot_duration(self):
        return self.duration

    def get_initial_hit_sp(self):
        return self.initial_hit_sp

    def get_ticks_sp(self):
        return self.ticks_sp


class Cast(Spell):
    cast_time = models.DecimalField(max_digits=5, decimal_places=2)
    dps_sp = models.DecimalField(max_digits=10, decimal_places=2)
    healing_sp = models.DecimalField(max_digits=10, decimal_places=2)


class Buff(models.Model):
    name = models.CharField(max_length=255, unique=True)
    buff_id = models.IntegerField(default=0, unique=True)
    # TODO: one to many relation to abstract spell
    # not sure how to implement this best
    # affects_spells = ArrayField(models.IntegerField(default=0), size=10)

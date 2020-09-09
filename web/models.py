from django.db import models
# from django.contrib.postgres.fields import ArrayField
from disc_sims.settings import STAT_NAMES, BUFF_PROCS_FROM


class Spell(models.Model):
    name = models.CharField(max_length=255, unique=True)
    mana_cost = models.DecimalField(max_digits=6, decimal_places=3)
    spell_id = models.IntegerField(default=0, unique=True)
    icon = models.ImageField(upload_to='icons', null=True)

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
    # cast time 0.0 means an instant spell
    cast_time = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    dps_sp = models.DecimalField(max_digits=10, decimal_places=2)
    healing_sp = models.DecimalField(max_digits=10, decimal_places=2)
    applies_atonement = models.BooleanField(default=False)
    atonement_duration = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def get_cast_time(self):
        return self.cast_time

    def get_dps_sp(self):
        return self.dps_sp

    def get_healing_sp(self):
        return self.healing_sp


class Buff(models.Model):
    name = models.CharField(max_length=255, unique=True)
    buff_id = models.IntegerField(default=0, unique=True)

    max_stacks = models.IntegerField(default=1)
    affected_stat = models.CharField(choices=map(lambda t: (t, t), STAT_NAMES), max_length=10, default='')
    duration = models.IntegerField(default=0)

    procs_from = models.CharField(choices=map(lambda t: (t, t), BUFF_PROCS_FROM), max_length=10, null=False)
    rppm = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)

    def __str__(self):
        return '%s[%d]' % (self.name, self.buff_id)

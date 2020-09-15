import uuid
from django.db import models
from django.core.validators import int_list_validator
from disc_sims.settings import STAT_NAMES, BUFF_PROCS_FROM, CASTING_SCHOOLS


class Spell(models.Model):
    spell_id = models.IntegerField(primary_key=True, default=0, unique=True)
    name = models.CharField(max_length=255, unique=True)
    mana_cost = models.DecimalField(max_digits=6, decimal_places=3)
    cooldown = models.DecimalField(max_digits=5, decimal_places=2)

    icon = models.ImageField(upload_to='icons', null=True, blank=True)
    # schools for things like scov checks
    casting_school = models.CharField(choices=map(lambda t: (t, t), CASTING_SCHOOLS), max_length=10, default='')

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
        ordering = ('name',)


class Dot(Spell):
    duration = models.IntegerField(default=0)
    initial_hit_sp = models.DecimalField(max_digits=10, decimal_places=2)
    sp_per_tick = models.DecimalField(max_digits=10, decimal_places=2)
    baseline_tick_time = models.DecimalField(max_digits=4, decimal_places=2)
    # end of duration to indicate it's a dot that benefits from haste, pets have a chance to hit instead
    end_of_duration_tick = models.BooleanField(default=True)

    def get_dot_duration(self):
        return self.duration

    def get_initial_hit_sp(self):
        return self.initial_hit_sp


class Cast(Spell):
    # cast time 0.0 means an instant spell
    cast_time = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    dps_sp = models.DecimalField(max_digits=10, decimal_places=2)
    healing_sp = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_sp = models.DecimalField(max_digits=10, decimal_places=2)
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
    icon = models.ImageField(upload_to='buff_icons', null=True, blank=True)

    # empty if not a blank stat buff
    affects_stat = models.CharField(choices=map(lambda t: (t, t), STAT_NAMES), max_length=10, default='', blank=True)
    # field showing which spell in particular it affects, many spells if null
    affects_spell = models.OneToOneField(Cast, on_delete=models.DO_NOTHING, blank=True, null=True,
                                         related_name='affects_spell')
    # if spell causes a buff - register it here (schism/scov etc)
    caused_by_spell = models.OneToOneField(Cast, on_delete=models.DO_NOTHING, blank=True, null=True,
                                           related_name='caused_by_spell')

    max_stacks = models.IntegerField(default=1)
    max_duration = models.IntegerField(default=0)
    is_permanent = models.BooleanField(default=False)

    # indicator of how this buff in invoked
    procs_from = models.CharField(choices=map(lambda t: (t, t), BUFF_PROCS_FROM), max_length=10, null=False)
    rppm = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True)

    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return '%s[%d]' % (self.name, self.buff_id)

    class Meta:
        ordering = ('name',)


class SimulationReport(models.Model):  # TODO CERE what else do we need in the report?
    report_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    total_gcds = models.IntegerField(default=0)
    total_healing = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)  # in sp?
    total_damage = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)  # in sp?
    # values = [int(x) for x in data.split(',') if x], values = map(int, '0,1,2,3,'.rstrip(',').split(','))
    # ','.join([str(i) for i in list_of_ints])
    raiders_healing_received_list = models.CharField(validators=[int_list_validator, ], max_length=120)

    def __str__(self):
        return 'report #' + str(self.report_id)

    class Meta:
        ordering = ('report_id', )


# 1 report -> N buffs values
class ReportBuffValue(models.Model):
    buff = models.OneToOneField(Buff, on_delete=models.DO_NOTHING, primary_key=True)
    simulation_report = models.ForeignKey(SimulationReport, on_delete=models.CASCADE)
    total_healing_value = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)
    total_damage_value = models.DecimalField(max_digits=32, decimal_places=2, default=0.0)

    def __str__(self):
        return '[%s] -> %s' % (str(self.buff), str(self.simulation_report.report_id))

from engine.state.raider import Raider
from engine.state.enemy import Enemy
from engine.state.player import Player
from web.models import SimulationReport, Buff
from disc_sims.settings import SINS_BUFF_ID, TOF_BUFF_ID, INF, ATONEMENT_TRANSFER_RATE
import uuid
import random
import datetime


class State:

    def __init__(self, scheduler, player_stats, player_talents, player_race, active_buffs, response_lock):
        self.player_talents = player_talents
        self.active_buffs = active_buffs
        self.response_lock = response_lock
        self.scheduler = scheduler
        self.raiders = [Raider(self)] * 20
        self.enemies = [Enemy(self)]
        self.player = Player(player_stats, player_race)

        self.total_mana_spent = 0.0
        self.total_healing_done = 0.0
        self.results = []

        # stores timestamps for rppm procs
        self.proc_data = {}

        #self.init_stats()
        self.init_buffs()

    def get_stats(self):
        with self.response_lock:
            return self.results

    def process_crit(self):
        if random.random() < (self.player.get_crit_modifier() - 1):
            return self.player.crit_dmg_modifier
        else:
            return 1

    def register_healing(self, target, sp, applies_atonement=False, atonement_duration=0.0):
        # TODO log healing
        hps_sp = self.apply_generic_hps_buffs(sp, self.raiders[target].has_atonement()) * self.process_crit() * self.player.get_vers_multiplier()
        self.raiders[target].heal(hps_sp * self.player.get_sp())
        if applies_atonement:
            self.raiders[target].apply_atonement(atonement_duration)

    def register_damage(self, enemy, sp, atonement_trigger=False):
        # TODO log damage
        damage_sp = self.apply_generic_dps_buffs(sp, False) * self.process_crit() * self.player.get_vers_multiplier()
        enemy.take_damage(damage_sp * self.player.get_sp())
        if atonement_trigger:
            # dmg portion that goes into atonement
            dps_atonement_sp = self.apply_generic_dps_buffs(sp, True) * self.process_crit() * self.player.get_vers_multiplier()
            for raider in self.raiders:
                if raider.has_atonement():
                    hps_sp = self.apply_generic_hps_buffs(dps_atonement_sp, raider.has_atonement()) * ATONEMENT_TRANSFER_RATE
                    # TODO log healing done
                    raider.heal(hps_sp * self.player.get_sp())

    # TODO add actual data to the report when ready
    def generate_report(self):
        self.results = []
        SimulationReport(report_id=uuid.uuid4()).save()

    def atonement_count(self):
        return len(list(filter(lambda raider: raider.has_atonement, self.raiders)))

    #def apply_generic_buffs(self, sp, atonement_trigger=False):
    #    buffed_sp = self.process_talents(sp)
    #    buffed_sp = self.process_active_buffs(buffed_sp)
    #    return buffed_sp

    def apply_generic_dps_buffs(self, sp, atonement_trigger=False):
        damage_sp = sp
        if atonement_trigger:
            for buff in self.active_buffs:
                # spell-specific buffs are applied elsewhere
                if buff.affects_atonement and not buff.affects_spell:
                    damage_sp *= buff.multiplier_value
        # apply generic damage buffs for spells/portion of spells that don't do atonement healing
        else:
             for buff in self.active_buffs:
                if buff.affects_generic_damage:
                    damage_sp *= buff.multiplier_value
        return damage_sp

    def apply_generic_hps_buffs(self, sp, has_atonement):
        healing_sp = sp
        for buff in self.active_buffs:
            if buff.affects_generic_healing:
                healing_sp *= buff.multiplier_value
        if has_atonement:   # apply mastery
            healing_sp *= self.player.get_mastery_multiplier()
        return healing_sp

    def process_talents(self, sp):
        processed_sp = sp
        # check for tof, (0th row 2nd column)
        if self.player_talents[0] == 1:
            try:
                tof = Buff.objects.get(buff_id=TOF_BUFF_ID)
                if tof in [buff[0] for buff in self.active_buffs]:
                    processed_sp = processed_sp * tof.multiplier_value
            except Buff.DoesNotExist:   # no twist in the db - log error
                # TODO log error
                pass
        # check for sins (5th row 1st column)
        if self.player_talents[4] == 0:
            try:
                sins = Buff.objects.get(buff_id=SINS_BUFF_ID)
                processed_sp = processed_sp * self.get_sins_value()
                # if talent is selected but buff isn't in the list then we need to add it
                if sins not in [buff[0] for buff in self.active_buffs]:
                    self.active_buffs.append([sins, INF])
            except Buff.DoesNotExist:   # no sins in the db - log error
                # TODO log error
                pass

        return processed_sp

    def get_sins_value(self):
        atonement_count = self.atonement_count()
        if atonement_count > 9:
            return 1.03
        elif atonement_count > 7:
            return 1.04
        elif atonement_count == 7:
            return 1.05
        elif atonement_count > 4:
            return 1.06
        elif atonement_count == 4:
            return 1.07
        elif atonement_count == 3:
            return 1.08
        elif atonement_count == 2:
            return 1.1
        else:
            return 1.12

    # TODO implment this
    def process_specific_buffs(self, next_spell):
        buffed_sp = next_spell.get_healing_sp()
        try:
            specific_buff = Buff.objects.get(affects_spell=next_spell)
            if specific_buff in self.active_buffs:
                buffed_sp *= specific_buff.multiplier_value
        except Buff.DoesNotExist:
            pass
        return buffed_sp
        

    def init_buffs(self):
        for buff in self.active_buffs:
            if buff.affects_stat:
                self.player.stats[buff.affects_stat] = self.player.stats[buff.affects_stat] * buff.multiplier_value


    def register_mana(self, mana_cost):
        # TODO check for mana buffs (rapture legendary, sd, innervate)
        self.total_mana_spent = self.total_mana_spent + mana_cost

    def process_rppm(self, rppm, spell_name):
        try:
            time_since_last_proc = datetime.datetime.now() - self.state.proc_data['%s_time_since_last_proc' % (spell_name)]
            time_since_last_proc_attempt = datetime.datetime.now() - self.state.proc_data['%s_time_since_last_proc_attempt' % (spell_name)]
        except:
                    # TODO time since combat start
            time_since_last_proc = 0.0
            time_since_last_proc_attempt = 0.0
       
        unlucky_streak_prevention = max(1.0, 1.0 + 3.0 * (time_since_last_proc * rppm / 60.0 - 1.5))
        proc_chance = unlucky_streak_prevention * (rppm / 60.0) * min(time_since_last_proc_attempt, 10.0)
        
        roll = random.random() < proc_chance
        if roll:
            self.proc_data['%s_time_since_last_proc' % (spell_name)] = datetime.datetime.now()
        self.state.proc_data['%s_time_since_last_proc_attempt' % (spell_name)] = datetime.datetime.now()
        return roll
              



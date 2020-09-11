from apscheduler.scheduler import Scheduler  # this has to be v2.1.2 !important
from engine.state.state import State
import threading
import time
from disc_sims.settings import EXEC_SPEED_MULTIPLIER, PET_SPELL_ID
from web.models import Dot, Cast, Spell
from django.core.exceptions import ObjectDoesNotExist
import datetime
import random

'''
    spell_sequence format:
        [[ Spell, [ (0 - healing, 1 - harm, 2 - aoe), (int ally_id/enemy_id for 0,1 OR [[ally_ids ... ], [ enemy ids ...]] for aoe) ] ], ... ]
'''


class Engine:
    def __init__(self, spell_sequence=None, player_stats=None, player_talents=None, simulate=False):
        self.error_list = []
        if player_talents is None:
            player_talents = []
        if player_stats is None:
            player_stats = []
        if spell_sequence is None:
            spell_sequence = []
        self.simulate = simulate  # this is for much later when we would want it to generate spell sequence for us
        # get Spell objects from spell ids
        try:
            self.spell_sequence = list(
                map(lambda spell: [Spell.objects.get(spell_id=spell[0]), spell[1]], spell_sequence))
        except ObjectDoesNotExist:
            # TODO add error message to some error list
            self.spell_sequence = []

        self.scheduler = Scheduler()
        self.scheduler.start()
        self.response_lock = threading.Lock()

        self.state = State(self.scheduler, player_stats, player_talents, self.response_lock)

    def run(self):
        self.execute_next_spell()

    def simulate(self):
        # if there are no spells to sim then we return an empty report and display any errors that may have happened
        if not self.spell_sequence:
            return [], self.error_list

        run_thread = threading.Thread(target=self.run)
        run_thread.start()

        # wait for spell queue to finish working, indicated by results list being filled
        while True:
            self.response_lock.aquire()
            if not self.state.get_stats():
                self.response_lock.release()
                time.sleep(5 * EXEC_SPEED_MULTIPLIER)
            else:
                self.response_lock.release()
                break

        if run_thread.is_alive():
            run_thread.join()

        return self.state.get_stats(), self.error_list

    def execute_next_spell(self):
        (next_spell, target_id) = self.spell_sequence.pop(0)  # should be of django spell type

        # update rppm buffs TODO
        # check for buffs TODO

        # que the spell, with timer if needed
        if type(next_spell) is Dot:
            enemy = self.state.enemies[target_id[1]]
            # apply initial hit
            self.state.register_damage(enemy, next_spell.get_initial_hit_sp())  # TODO CERE - fix maths
            # check if dot is in pandemic, if new dot - schedule the ticks
            if enemy.has_dot():
                enemy.extend_dot(next_spell.duration)
            else:  # apply new dot
                enemy.apply_dot(next_spell)
                # schedule ticks
                current_time = datetime.datetime.now()
                # TODO CERE fix dot tickrate maths, use haste etc
                sched_time = datetime.timedelta(milliseconds=(next_spell.baseline_tick_time * 1000
                                                              * EXEC_SPEED_MULTIPLIER)) + current_time
                self.scheduler.add_date_job(self.process_dot_tick, sched_time, args=[next_spell.baseline_tick_time,
                                                                                     next_spell.sp_per_tick,
                                                                                     enemy])
        elif type(next_spell) is Cast:
            # next spell is a cast`

            # check if this is an instant cast or not, schedule if needed for the cast time duration
            if next_spell.cast_time:
                self.execute_spell_now(next_spell, target_id)
            else:
                current_time = datetime.datetime.now()
                # TODO CERE fix dot tickrate maths, use haste etc
                # *1000 because need to convert to milliseconds
                sched_time = datetime.timedelta(milliseconds=(next_spell.cast_time * 1000
                                                              * EXEC_SPEED_MULTIPLIER)) + current_time
                self.scheduler.add_date_job(self.execute_spell_now, sched_time, args=[next_spell, target_id])
        else:
            # some weirdness TODO test this and display error
            print('bp')
            pass

    def execute_spell_now(self, next_spell, target_id):
        # check if it's a dps or healing spell, then check if it's an aoe spell
        is_aoe_spell = target_id[0] == 2
        # check if the spell does any damage
        if target_id[0] == 1 or (is_aoe_spell and len(target_id[1][1]) != 0):
            # cover aoe spell case
            aoe_target_list = target_id[1][1]
            if is_aoe_spell and aoe_target_list:  # will assume first target in the enemy list is the closest one
                main_target = aoe_target_list.pop(0)
                self.state.register_damage(main_target, next_spell.get_dps_sp())  # TODO CERE fix maths
                # atonement only works on 1 target
                for target in aoe_target_list:
                    self.state.register_damage_no_atonement(target, next_spell.get_dps_sp())
            # ST spell case
            else:
                self.state.register_damage(target_id[1], next_spell.get_dps_sp())

        # check if the spell does any healing
        aoe_healing_list = target_id[1][0]
        if target_id[0] == 0 or (is_aoe_spell and aoe_healing_list):
            # check if it does aoe healing
            if is_aoe_spell and aoe_healing_list:
                for target in aoe_healing_list:
                    self.state.register_healing(target, next_spell.get_healing_sp(),
                                                next_spell.applies_atonement,
                                                next_spell.atonement_duration)
            # st spell
            else:
                self.state.register_healing(target_id[1], next_spell.get_healing_sp(),
                                            next_spell.applies_atonement,
                                            next_spell.atonement_duration)

    def process_dot_tick(self, baseline_tick_time, tick_sp, dot, enemy):
        # TODO add potds proc

        self.state.register_damage(enemy, tick_sp)
        dot_tick_time = baseline_tick_time  # TODO CERE fix maths for this dot tick time
        enemy.decay_dot(dot_tick_time)

        # check if the dot has expired and there is no next tick
        if enemy.dot_duration == 0:
            return

        current_time = datetime.datetime.now()
        # check if dot is going to expire soon and we need to process the last tick bit
        if enemy.dot_duration < dot_tick_time:
            # check if it's a bender or shadowfiend and we need to rng last hit
            if dot.spell_id in PET_SPELL_ID:
                chance_to_hit = enemy.dot_duration / dot_tick_time
                if random.random() < chance_to_hit:
                    sched_time = datetime.timedelta(milliseconds=(dot_tick_time * 1000 *
                                                                  EXEC_SPEED_MULTIPLIER)) + current_time
                    self.scheduler.add_date_job(self.process_dot_tick, sched_time,
                                                args=[dot_tick_time, dot.sp_per_tick, dot, enemy])
            else:   # SWP or PTW case
                sched_time = datetime.timedelta(milliseconds=(enemy.dot_duration * 1000 *
                                                              EXEC_SPEED_MULTIPLIER)) + current_time
                sp_dmg_portion = enemy.dot_duration / dot_tick_time
                self.scheduler.add_date_job(self.process_dot_tick, sched_time,
                                            args=[enemy.dot_duration, sp_dmg_portion, dot, enemy])
        else:
            # TODO CERE fix dot tickrate maths, use haste etc
            sched_time = datetime.timedelta(milliseconds=(dot_tick_time * 1000 * EXEC_SPEED_MULTIPLIER)) + current_time
            self.scheduler.add_date_job(self.process_dot_tick, sched_time,
                                        args=[dot_tick_time, dot.sp_per_tick, dot, enemy])

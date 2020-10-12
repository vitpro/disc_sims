from apscheduler.scheduler import Scheduler # this has to be v2.1.2 !important
from engine.state.state import State
import threading
import time
from disc_sims.settings import EXEC_SPEED_MULTIPLIER, PET_SPELL_IDS
from web.models import Dot, Cast, Spell, Buff
from django.core.exceptions import ObjectDoesNotExist
import datetime
import random
import math


'''
    spell_sequence format:
        [[ Spell, [ (0 - healing, 1 - harm, 2 - aoe), (int ally_id/enemy_id for 0,1 OR [[ally_ids ... ], [ enemy ids ...]] for aoe) ] ], ... ]
'''


class Engine:
    def __init__(self, spell_sequence=None, player_stats=None, player_talents=None,
                 active_buffs=None, simulate=False):
        if active_buffs is None:
            active_buffs = []
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

        self.active_buffs = self.init_buffs(active_buffs)

        # TODO check active buffs references - maybe need to pass self and reference via engine.active_buffs?
        self.state = State(self.scheduler, player_stats, player_talents, self.active_buffs, self.response_lock)

    def run(self):
        # TODO implement logic loop
        #while job store is not empty
        self.execute_next_spell()
        # else gen report

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

        # clean up
        # TODO anything else?
        for buff in self.active_buffs:
            if buff.is_blocked:
                buff.is_blocked = False
                buff.save()

        return self.state.get_stats(), self.error_list

    def execute_next_spell(self):
        (next_spell, target_id) = self.spell_sequence.pop(0)  # should be of django spell type

        # update rppm buffs TODO
        # check for buffs TODO

        # que the spell, with timer if needed
        if type(next_spell) is Dot:
            self.state.register_mana(next_spell.get_mana_cost())
            enemy = self.state.enemies[target_id[1]]
            # apply initial hit
            self.state.register_damage(enemy, next_spell.get_initial_hit_sp(), next_spell.atonement_trigger)
            # check if dot is in pandemic, if new dot - schedule the ticks
            if enemy.has_dot():
                # 1.3 = pandemic window
                enemy.extend_dot(next_spell.duration, max_dot_duration=next_spell.duration * 1.3)
            else:  # apply new dot
                enemy.apply_dot(next_spell)
                # schedule ticks
                current_time = datetime.datetime.now()
                haste = self.state.player.get_haste_multiplier()
                dot_tick_time = next_spell.baseline_tick_time / haste
                sched_time = datetime.timedelta(milliseconds=(dot_tick_time * 1000
                                                              * EXEC_SPEED_MULTIPLIER)) + current_time
                self.scheduler.add_date_job(self.process_dot_tick, sched_time, args=[next_spell.baseline_tick_time,
                                                                                     next_spell.sp_per_tick,
                                                                                     enemy, next_spell.atonement_trigger])
        elif type(next_spell) is Cast:
            # next spell is a cast

            # check if this is an instant cast or not, schedule if needed for the cast time duration
            if next_spell.cast_time == 0.0:
                self.execute_spell_now(next_spell, target_id)
            else:
                current_time = datetime.datetime.now()
                haste = self.state.player.get_haste_multiplier()
                cast_time = next_spell.cast_time / haste
                # *1000 because need to convert to milliseconds
                sched_time = datetime.timedelta(milliseconds=(cast_time * 1000
                                                              * EXEC_SPEED_MULTIPLIER)) + current_time
                self.scheduler.add_date_job(self.execute_spell_now, sched_time, args=[next_spell, target_id])
        else:
            # some weirdness TODO test this and display error
            print('bp')
            pass

    def execute_spell_now(self, next_spell, target_id):
        self.state.register_mana(next_spell.get_mana_cost())
        # buff triggers/procs
        for proc in Buff.objects.filter(caused_by_spell=next_spell):
            if proc.rppm:
                if self.state.process_rppm(proc.rppm, proc.name):
                    self.state.active_buffs.append(proc)
            else:
                self.state.active_buffs.append(proc)
        # check if the spell does any damage
        if target_id[0] == 1 or (next_spell.is_aoe and len(target_id[1][1]) != 0):
        # TODO add buff modifiers here
            # cover aoe spell case
            aoe_target_list = target_id[1][1]
            if next_spell.is_aoe and aoe_target_list:
                # check for target cap, distribute damage depending on scaling type
                if next_spell.damage_cap and next_spell.aoe_scaling_type == 'LINEAR':
                    damage_sp = next_spell.get_damage_sp() * next_spell.damage_cap / max(len(aoe_damage_list), next_spell.damage_cap)
                # TODO implement capped SQRT scaling - how does it work?
                elif next_spell.aoe_scaling_type == 'SQRT': 
                    # TODO make an exception for ascended eruption?
                    damage_sp = next_spell.get_damage_sp() / math.sqrt(len(aoe_damage_list))
                else: 
                    damage_sp = next_spell.get_damage_sp()
                # will assume first target in the enemy list is the closest one
                main_target = aoe_target_list.pop(0)
                self.state.register_damage(main_target, next_spell.get_damage_sp(), next_spell.atonement_trigger)
                # atonement only works on 1 target
                for target in aoe_target_list:
                    self.state.register_damage(target, next_spell.get_damage_sp(), False)
            # ST spell case
            else:
                self.state.register_damage(target_id[1], next_spell.get_damage_sp(), next_spell.atonement_trigger)

        # check if the spell does any healing
        aoe_healing_list = target_id[1][0]
        if target_id[0] == 0 or (next_spell.is_aoe and aoe_healing_list):
            # TODO apply spell specific buffs
            healing_sp = next_spell.get_healiing_sp()
            # check if it does aoe healing
            if next.spell.is_aoe and aoe_healing_list:
                # check for target cap, distribute healing depending on scaling type
                if next_spell.healing_cap and next_spell.aoe_scaling_type == 'LINEAR':
                    healing_sp = healing_sp * next_spell.healing_cap / max(len(aoe_healing_list), next_spell.healing_cap)
                # TODO implement capped SQRT scaling
                elif next_spell.aoe_scaling_type == 'SQRT': 
                    healing_sp = healing_sp / math.sqrt(len(aoe_healing_list))
                
                for target in aoe_healing_list:
                    self.state.register_healing(target, healing_sp,
                                                next_spell.applies_atonement,
                                                next_spell.atonement_duration)
            # st spell
            else:
                self.state.register_healing(target_id[1], healing_sp,
                                            next_spell.applies_atonement,
                                            next_spell.atonement_duration)
        # process any additional perks, i.e. mindgames extra value
        if next_spell.bonus_sp:
            self.state.register_healing(0, next_spell.bonus_sp)

    def process_dot_tick(self, baseline_tick_time, tick_sp, dot, enemy, atonement_trigger=False):
        
        self.state.register_damage(enemy, tick_sp, atonement_trigger)
        haste = self.state.player.get_haste_multiplier()
        dot_tick_time = baseline_tick_time / haste
        enemy.decay_dot(dot_tick_time)

        # buff triggers/procs
        # TODO refresh/pandemic buff durations
        for proc in Buff.objects.filter(caused_by_spell=dot):
            if proc.rppm:
                if self.state.process_rppm(proc.rppm, proc.name):
                    self.state.active_buffs.append(proc)
            else:
                self.state.active_buffs.append(proc)



        # check if the dot has expired and there is no next tick
        if enemy.dot_duration == 0:
            return

        current_time = datetime.datetime.now()
        # check if dot is going to expire soon and we need to process the last tick bit
        if enemy.dot_duration < dot_tick_time:
            # check if it's a bender or shadowfiend and we need to rng last hit TODO test if fiend actually works like this
            if dot.spell_id in PET_SPELL_IDS:       # TODO test if fiend actually works like this
                chance_to_hit = enemy.dot_duration / dot_tick_time
                if random.random() < chance_to_hit:
                    sched_time = datetime.timedelta(milliseconds=(dot_tick_time * 1000 *
                                                                  EXEC_SPEED_MULTIPLIER)) + current_time
                    self.scheduler.add_date_job(self.process_dot_tick, sched_time,
                                                args=[dot_tick_time, dot.sp_per_tick, dot, enemy, next_spell.atonement_trigger])
            else:  # SWP or PTW case
                sched_time = datetime.timedelta(milliseconds=(enemy.dot_duration * 1000 *
                                                              EXEC_SPEED_MULTIPLIER)) + current_time
                sp_dmg_portion = dot.sp_per_tick * (enemy.dot_duration / dot_tick_time)
                self.scheduler.add_date_job(self.process_dot_tick, sched_time,
                                            args=[enemy.dot_duration, sp_dmg_portion, dot, enemy, next_spell.atonement_trigger])
        else:
            sched_time = datetime.timedelta(milliseconds=(dot_tick_time * 1000 * EXEC_SPEED_MULTIPLIER)) + current_time
            self.scheduler.add_date_job(self.process_dot_tick, sched_time,
                                        args=[dot_tick_time, dot.sp_per_tick, dot, enemy, next_spell.atonement_trigger])

    def untrack_buff(self, buff_id):
        try:
            _buff = Buff.objects.get(buff_id=buff_id)
            self.active_buffs = [buff for buff in self.active_buffs if not buff[0] == _buff]
        except Buff.DoesNotExist:
            # TODO really bad error happining
            self.error_list.append('...')

    def init_buffs(self, buff_list):
        active_buffs = []
        for buff in buff_list:
            try:
                # schedule buff expiration
                sched_time = datetime.timedelta(milliseconds=buff[1] * 1000 * EXEC_SPEED_MULTIPLIER) + datetime.datetime.now()
                job = self.scheduler.add_date_job(self.untrack_buff, sched_time, args=[buff[0], ])
                active_buffs.append([Buff.objects.get(buff_id=buff[0]), job])
            except Buff.DoesNotExist:
                # TODO error message
                self.error_list.append('some error message, buff %d isn;t in the db etc' % buff[0])
        return active_buffs

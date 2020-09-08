from apscheduler.scheduler import Scheduler  # this has to be v2.1.2 !important
from engine.state.state import State
import threading
import time
from disc_sims.settings import EXEC_SPEED_MULTIPLIER
from web.models import Dot, Cast
import datetime

"""

"""


class Engine:
    def __init__(self, spell_sequence=None, player_stats=None, simulate=False):
        if player_stats is None:
            player_stats = []
        if spell_sequence is None:
            spell_sequence = []
        self.simulate = simulate # this is for much later when we would want it to generate spell sequence for us
        self.spell_sequence = spell_sequence

        self.scheduler = Scheduler()
        self.scheduler.start()

        self.state = State(self.scheduler, player_stats)

    # TODO logic for safe running next spell, need some sort of lock for state resources!!
    def run(self):
        self.execute_next_spell()

    def simulate(self):
        run_thread = threading.Thread(target=self.run)
        run_thread.start()

        # wait for spell queue to finish working, indicated by results list being filled
        while not self.state.get_stats():
            time.sleep(1 * EXEC_SPEED_MULTIPLIER)
        if run_thread.is_alive():
            run_thread.join()

        return self.state.get_stats()

    def execute_next_spell(self):
        (next_spell, target) = self.spell_sequence.pop(0)  # should be of django spell type

        # update rppm buffs TODO
        # check for buffs TODO

        # que the spell, with timer if needed
        if type(next_spell) is Dot:
            # apply initial hit
            self.state.register_damage(target, next_spell.get_initial_hit_sp())  # TODO CERE - fix maths
            # check if dot is in pandemic, if new dot - schedule the ticks
            enemy = self.state.enemies[target[1]]
            if enemy.has_dot():
                enemy.extend_dot(next_spell.duration)
            else:   # apply new dot
                enemy.apply_dot(next_spell)
                # schedule ticks
                current_time = datetime.datetime.now()
                # TODO CERE fix dot tickrate maths, use haste etc
                sched_time = datetime.timedelta(milliseconds=(1500 * EXEC_SPEED_MULTIPLIER)) + current_time
                self.scheduler.add_date_job(self.process_dot_ticks, sched_time, )
        else:
            # next spell is a cast
            pass

    def process_dot_tick(self):
        pass

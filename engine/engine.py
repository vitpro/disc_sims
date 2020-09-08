from apscheduler.scheduler import Scheduler  # this has to be v2.1.2 !important
from engine.state.state import State
import threading
import time
from disc_sims.settings import EXEC_SPEED_MULTIPLIER

"""



state = State
class State:
    [Raider,] //x20
    Timeline (just ms since start, maybe some timeframe blocks?).. with flux can use t.schedule_callback(100, callback),
        and use simulate_timeframe as a repetitive callback that will change the state
    [Enemy,]



def simulate(player, sim details(?)):

    init_state



"""


class Engine:
    def __init__(self, spell_sequence=None, player_stats=None, simulate=False):
        if player_stats is None:
            player_stats = []
        if spell_sequence is None:
            spell_sequence = []
        self.simulate = simulate
        self.spell_sequence = spell_sequence
        self.scheduler = Scheduler()
        self.state = State(self.scheduler, player_stats)

    # TODO logic for safe running next spell
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
        next_spell = self.spell_sequence.pop(0)  # should be of django spell type

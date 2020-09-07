from apscheduler.scheduler import Scheduler  # this has to be v2.1.2 !important
from engine.state.state import State

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
    def __init__(self, spell_sequence=[], player_stats=[], simulate=False):
        self.simulate = simulate
        self.spell_sequence = spell_sequence
        self.scheduler = Scheduler()
        self.state = State(self.scheduler, player_stats)

    def run(self):
        self.execute_next_spell()

    # spell sequence is empty and scheduler has finish its' last task
    def report(self):
        return self.state.get_stats()

    def execute_next_spell(self):
        next_spell = self.spell_sequence.pop(0)  # should be of django spell type


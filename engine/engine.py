#import sched
from apscheduler.scheduler import Scheduler
import time
import datetime
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

    def __init__(self):
        #self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler = Scheduler()

        self.state = State(self.scheduler)
        # e2 = s.enter(seconds_to_exec, priority, callback, (time.time(),)), can access start time later by e2.argument[0]

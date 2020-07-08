from flux import Timeline

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


class State:

    def __init__(self):
        self.timeline = Timeline()

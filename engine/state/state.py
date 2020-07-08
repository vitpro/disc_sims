from engine.state.raider import Raider
from engine.state.enemy import Enemy


class State:

    def __init__(self, timeline, time_chunk):
        self.time_chunk = time_chunk
        self.timeline = timeline
        self.raiders = [Raider()] * 20
        self.bosses = [Enemy(self.timeline)]

        self.total_healing_done = 0.0

    def apply_healing(self, value):
        pass  # TODO: traverse raiders list, check if atonement is active and apply healing

    def decay_atonements(self):
        pass  # TODO: traverse and apply the decay

    def process_dots(self):
        pass  # TODO: process if dots ticked in a given time chunk on any enemies

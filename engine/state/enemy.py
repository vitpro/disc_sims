import engine.toolkit.dot


class Enemy:

    def __init__(self, timeline, state, time_chunk):
        self.time_chunk = time_chunk
        self.state = state
        self.dot_start_time = 0.0
        self.timeline = timeline
        self.dot = None
        self.last_dot_tick = 0.0  # can use this to track if we need to account for a dot tick in a given time chunk
        self.time_chunks_missed = 0

    def apply_dot(self, dot):
        self.dot = dot
        self.dot_start_time = self.timeline.time()
        self.last_dot_tick = self.dot_start_time

    def get_remaining_dot_duration(self):
        if self.dot is not None:
            rem = self.dot.duration - (self.timeline.time() - self.dot_start_time)
            return rem if rem > 0 else 0

    # returns dot sp value for a given tick if it happened in a time chunk, else 0
    # TODO: assuming the interval is short enough that dot doesnt tick twice on 1 target within it, fix?
    # TODO: need to add last time chunk reference point to not miss any ticks, and have a more complex check with
    #  regards to last dot tick and last time chunk POVs
    def has_dot_ticked(self):
        tick_interval = self.dot.get_tick_interval(self.state.player.get_haste())
        if self.time_chunk * (1 + self.time_chunks_missed) > tick_interval:
            self.time_chunks_missed = 0
            self.last_dot_tick = self.timeline.time()
            return self.dot.get_sp()
        else:
            self.time_chunks_missed += 1




from engine.state.raider import Raider
from engine.state.enemy import Enemy


class State:

    def __init__(self, scheduler, player_stats):
        self.scheduler = scheduler
        self.raiders = [Raider()] * 20
        self.enemies = [Enemy(self)]

        self.total_healing_done = 0.0
        self.results = []

    def get_stats(self):
        return self.results

    def register_damage(self, target, sp):
        # TODO log damage
        target

        for raider in self.raiders:
            if raider.has_atonement():
                # TODO log healing done
                raider.heal()   # TODO CERE do maths

    def register_healing(self, target, sp):  # non atonement healing
        pass

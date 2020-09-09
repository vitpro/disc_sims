from engine.state.raider import Raider
from engine.state.enemy import Enemy


class State:

    def __init__(self, scheduler, player_stats, response_lock):
        self.response_lock = response_lock
        self.scheduler = scheduler
        self.raiders = [Raider()] * 20
        self.enemies = [Enemy(self)]

        self.total_healing_done = 0.0
        self.results = []

    def get_stats(self):
        with self.response_lock:
            return self.results

    def register_healing(self, target, sp, applies_atonement=False, atonement_duration=0.0):
        self.raiders[target].heal(sp)
        if applies_atonement:
            self.raiders[target].apply_atonement(atonement_duration)

    def register_damage(self, enemy, sp):
        # log damage
        enemy.take_damage(sp)

        for raider in self.raiders:
            if raider.has_atonement():
                # TODO log healing done
                raider.heal(sp)   # TODO CERE do maths

    def register_damage_no_atonement(self, enemy, sp):
        enemy.take_damage(sp)

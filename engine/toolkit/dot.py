class Dot:

    # TODO: add constructor values and getters/setters for sp, etcetc
    def __int__(self):
        self.duration = 0
        pass

    def get_tick_interval(self, haste):
        return self.duration / self.base_ticks / (1 + haste / 100)

    def get_last_tick(self, haste):
        if haste % 10:
            return self.sp_tick * self.base_ticks * (haste % 10) / 100
        else:
            return 0

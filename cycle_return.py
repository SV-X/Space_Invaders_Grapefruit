class CycleReturn:
    def __init__(self, si_game, group = [(0,0,0)], rate = 1.0, member_index = 0):

        self.si_game = si_game

        self.group = group
        self.rate = rate
        self.delay = 1.0 / self.rate if self.rate != 0 else 1.0
        self.countdown = self.delay
        self.member_index = member_index
        self.member_index %= len(self.group)
        self.member = self.group[self.member_index]

    def tick(self):
        self.countdown -= self.si_game.dt

        if self.countdown <= 0:
            self.countdown = self.delay
            self.member_index += 1
            self.member_index %= len(self.group)
    
    def check_current(self):
        return self.group[self.member_index]

    def update(self):
        self.tick()
        return self.group[self.member_index]
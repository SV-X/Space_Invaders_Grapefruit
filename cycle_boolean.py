class CycleBoolean:
    def __init__(self, si_game, rate = 1.0):

        self.si_game = si_game
        self.rate = rate
        self.delay = 1.0 / self.rate if self.rate != 0 else 1.0
        self.countdown = self.delay

        self.can_act = True

    def tick(self):
        if not self.can_act: self.countdown -= self.si_game.dt
        if self.countdown <= 0:
            self.can_act = True
            self.countdown = self.delay
    
    def act(self):
        self.tick()

        if self.can_act:
            self.can_act = False
            self.countdown = self.delay
            return True
        else:
            return False
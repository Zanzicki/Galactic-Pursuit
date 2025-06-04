class BossStateMachine:
    def __init__(self, boss, player):
        self.boss = boss
        self.player = player
        self.current_state = None

    def change_state(self, new_state):
        if self.current_state:
            self.current_state.exit(self.boss, self.player)
        self.current_state = new_state
        self.current_state.enter(self.boss, self.player)

class TurnOrder:
    def __init__(self, player, enemy):
        self.actors = [player, enemy]
        self.current_turn = 0  # 0 = player, 1 = enemy
        self.turncount = 1

    @property
    def current_turn(self):
        return self._current_turn
    
    @current_turn.setter
    def current_turn(self, value):
        if value < 0 or value >= len(self.actors):
            raise ValueError("Invalid turn index")
        self._current_turn = value
    
    def reset_turn(self):
        self._current_turn = 0
        self.turncount = 0

    def current_actor(self):
        return self.actors[self.current_turn]

    def end_turn(self):
        if self.current_turn == 0:
            self.turncount += 1
        self.current_turn = (self.current_turn + 1) % len(self.actors)

    def is_player_turn(self):
        return self.current_turn == 0
    
    def is_enemy_turn(self):
        return self.current_turn == 1
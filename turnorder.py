class TurnOrder:
    def __init__(self, player, enemy):
        self.actors = [player, enemy]
        self.current_turn = 0  # 0 = player, 1 = enemy

    def current_actor(self):
        return self.actors[self.current_turn]

    def end_turn(self):
        # Switch to the other actor
        self.current_turn = (self.current_turn + 1) % len(self.actors)

    def is_player_turn(self):
        return self.current_turn == 0

    def is_enemy_turn(self):
        return self.current_turn == 1
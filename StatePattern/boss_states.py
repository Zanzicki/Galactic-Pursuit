from StatePattern.State import State

class IdleState(State):
    def enter(self, boss, player):
        print("Boss enters Idle state.")

    def execute(self, boss, player):
        print("Boss is idling.")
        # Example logic: If boss health < 40%, enrage. If player health < 30%, attack. Otherwise, defend.
        boss_health_pct = boss.health / boss._max_health
        player_health_pct = player.health / player._max_health

        if boss_health_pct < 0.4:
            boss.state_machine.change_state(EnrageState())
        elif player_health_pct < 0.3:
            boss.state_machine.change_state(AttackState())
        else:
            boss.state_machine.change_state(DefendState())

    def exit(self, boss, player):
        print("Boss leaves Idle state.")

class AttackState(State):
    def enter(self, boss, player):
        print("Boss prepares to attack!")

    def execute(self, boss, player):
        print("Boss attacks the player!")
        boss.attack(player)
        # After attacking, go idle or enrage if low health
        if boss.health / boss._max_health < 0.4:
            boss.state_machine.change_state(EnrageState())
        else:
            boss.state_machine.change_state(IdleState())

    def exit(self, boss, player):
        print("Boss finishes attack.")

class DefendState(State):
    def enter(self, boss, player):
        print("Boss prepares to defend!")

    def execute(self, boss, player):
        print("Boss defends or heals!")
        boss.defend()  # You must implement this method in your Boss class
        boss.state_machine.change_state(IdleState())

    def exit(self, boss, player):
        print("Boss finishes defending.")

class EnrageState(State):
    def enter(self, boss, player):
        print("Boss is enraged! It will attack harder.")

    def execute(self, boss, player):
        print("Boss performs a powerful attack!")
        boss.enraged_attack(player)  # You must implement this method in your Boss class
        boss.state_machine.change_state(IdleState())

    def exit(self, boss, player):
        print("Boss calms down (leaves Enrage state).")
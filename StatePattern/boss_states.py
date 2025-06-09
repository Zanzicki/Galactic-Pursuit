from StatePattern.State import State

class IdleState(State):
    icon_type = "skill"

    def enter(self, boss, player):
        print("Boss enters Idle state.")

    def execute(self, boss, player):
        print("Boss is idling.")
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
    icon_type = "attack"

    def enter(self, boss, player):
        print("Boss prepares to attack!")

    def execute(self, boss, player):
        print("Boss attacks the player!")
        boss.attack(player)
        # After attacking, go idle or enrage if low health
        if boss.health / boss._max_health < 0.4:
            boss.state_machine.change_state(EnrageState())
        else:
            boss.state_machine.change_state(DefendState())

    def exit(self, boss, player):
        print("Boss finishes attack.")

class DefendState(State):
    icon_type = "defend"

    def enter(self, boss, player):
        print("Boss prepares to defend!")

    def execute(self, boss, player):
        print("Boss grants itself temporary health!")
        boss.defend()  # This should heal the boss
        boss.last_state_was_defend = True  # Set flag
        boss.state_machine.change_state(AttackState())

    def exit(self, boss, player):
        print("Boss finishes defending.")

class EnrageState(State):
    icon_type = "attack"

    def enter(self, boss, player):
        print("Boss is enraged! It will attack harder.")

    def execute(self, boss, player):
        print("Boss performs a powerful attack!")
        boss.enraged_attack(player)  # You must implement this method in your Boss class
        boss.state_machine.change_state(IdleState())

    def exit(self, boss, player):
        print("Boss calms down (leaves Enrage state).")

class DebuffState(State):
    icon_type = "debuff"

    def enter(self, boss, player):
        print("Boss applies a debuff to the player.")

    def execute(self, boss, player):
        print("Boss is applying debuff!")
        boss.apply_debuff(player)  # You must implement this method in your Boss class
        boss.state_machine.change_state(IdleState())

    def exit(self, boss, player):
        print("Boss finishes applying debuff.")
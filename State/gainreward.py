class GainReward:
    def __init__(self):
        pass

    def gain_card_reward(self, player, card):
        player.gain_card(card)
        print(f"{player.name} gains a {card.name} card.")
    
    def gain_artifact_reward(self, player, artifact):
        player.gain_artifact(artifact)
        print(f"{player.name} gains an artifact: {artifact.name}.")

    def gain_gold_reward(self, player, gold_amount):
        player.gain_gold(gold_amount)
        print(f"{player.name} gains {gold_amount} gold.")
    
    def gain_scrap_reward(self, player, scrap_amount):
        player.gain_scrap(scrap_amount)
        print(f"{player.name} gains {scrap_amount} scrap.")
        
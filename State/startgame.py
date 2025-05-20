class NewGame:
    def __init__(self):
        self.database = None  # Should be set to your Database instance

    def create_new_player(self, name):
        player_id = self.database.insert_player(name, 100, 0, 100)
        self.database.fetch_player(player_id)
        print(f"New player created: {name} (ID: {player_id})")
        return player_id

    def continue_game(self, player_id):
        self.database.fetch_player(player_id)
        print(f"Continuing game for player ID: {player_id}")

    def get_player_list(self):
        return self.database.fetch_players()



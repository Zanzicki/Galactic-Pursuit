

class NewGame():
    def __init__(self):
        self.database = None

    def create_new_player(self, name):
        self.database.create_player(name)
    
    def continue_game(self, player_id):
        self.database.load_player(player_id)
        


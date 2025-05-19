

class NewGame():
    def __init__(self):
        self.database = None

    def create_new_player(self, name):
        self.database.create_player(name)

        self.game_world.initialize_player(name)


from Database.database import Database

class SQLRepository:
    def __init__(self, db_name="game_data.db"):
        self.db = Database(db_name)

    # --- Artifact methods ---
    def insert_artifact(self, name, rarity, description, price):
        self.db.insert_artifact(name, rarity, description, price)

    def fetch_artifacts(self):
        return self.db.fetch_artifacts()
    
    def fetch_artifact_by_name(self, name):
        return self.db.fetch_artifact_by_name(name)
    
    def fetch_artifact_by_id(self, artifact_id):
        return self.db.fetch_artifact_by_id(artifact_id)

    def fetch_all_artifacts(self):
        return self.db.fetch_all_artifacts()
    
    def fetch_all_artifact_names(self):
        return self.db.fetch_all_artifact_names()

    # --- Card methods ---
    def insert_card(self, name, value, type, rarity, description, prize):
        self.db.insert_card(name, value, type, rarity, description, prize)

    def fetch_cards(self):
        return self.db.fetch_cards()

    def fetch_all_cards(self):
        return self.db.fetch_all_cards()

    def fetch_basic_cards(self):
        return self.db.fetch_basic_cards()
    
    def fetch_all_card_names(self):
        return self.db.fetch_all_card_names()
    
    def fetch_all_non_basic_cards(self):
        return [card for card in self.db.fetch_all_cards() if not card['Basic']]

    # --- Player methods ---
    def insert_player(self, name, credits, scraps, health, max_health):
        return self.db.insert_player(name, credits, scraps, health, max_health)

    def fetch_players(self):
        return self.db.fetch_players()

    def fetch_player_id(self, name):
        return self.db.fetch_player_id(name)

    def fetch_player(self, player_id):
        return self.db.fetch_player(player_id)

    def update_player_currency(self, player_id, credits=None, scrap=None, health=None, max_health=None):
        self.db.update_player_currency(player_id, credits, scrap, health, max_health)

    # --- Player cards/artifacts ---
    def insert_player_card(self, player_id, card_id):
        self.db.insert_player_card(player_id, card_id)

    def insert_player_artifact(self, player_id, artifact_id):
        self.db.insert_player_artifact(player_id, artifact_id)

    def fetch_player_cards(self, player_id):
        return self.db.fetch_player_cards(player_id)

    def fetch_player_artifacts(self, player_id):
        return self.db.fetch_player_artifacts(player_id)

    # --- Planets ---
    def fetch_planets_for_player(self, player_id):
        return self.db.fetch_planets_for_player(player_id)

    def change_planet_explored(self, player_id, planet_name):
        self.db.change_planet_explored(player_id, planet_name)

    def insert_planet(self, player_id, name, r, g, b, explored, x, y, size):
        self.db.insert_planet(player_id, name, r, g, b, explored, x, y, size)

    # --- Utility ---
    def close(self):
        self.db.close()
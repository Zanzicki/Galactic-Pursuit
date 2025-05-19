import sqlite3

class Database:
    def __init__(self, db_name="game_data.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):

        # Create the artifacts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rarity TEXT NOT NULL,
                prize INTEGER NOT NULL
            )
        ''')

        # Create the cards table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value INTEGER NOT NULL,
                type TEXT NOT NULL,
                rarity TEXT NOT NULL,
                description TEXT NOT NULL,
                prize INTEGER NOT NULL
            )
        ''')

        # Create the players cards table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playercards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                card_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (card_id) REFERENCES cards(id)
            )
        ''')

        # Create the players artifacts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playerartifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                artifact_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
            )
        ''')

        # Create the players table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                scraps INTEGER NOT NULL,
                health INTEGER NOT NULL
            )
        ''')

        # Create planet table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS planets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                explored BOOLEAN NOT NULL,
                position_x INTEGER NOT NULL,
                position_y INTEGER NOT NULL,
            )
        ''')

        self.connection.commit()

    def insert_artifact(self, name, rarity, prize):
        self.cursor.execute('''
            INSERT INTO artifacts (name, rarity, prize)
            VALUES (?, ?, ?)
        ''', (name, rarity, prize))
        self.connection.commit()

    def insert_card(self, name, value, type, rarity, description, prize):
        self.cursor.execute('''
            INSERT INTO cards (name, value, type, rarity, description, prize)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, value, type, rarity, description, prize))
        self.connection.commit()
    
    def insert_player(self, name, credits, scraps, health):
        self.cursor.execute('''
            INSERT INTO players (name, credits, scraps, health)
            VALUES (?, ?, ?, ?)
        ''', (name, credits, scraps, health))
        self.connection.commit()

    def insert_player_card(self, player_id, card_id):
        self.cursor.execute('''
            INSERT INTO playercards (player_id, card_id)
            VALUES (?, ?)
        ''', (player_id, card_id))
        self.connection.commit()

    def insert_player_artifact(self, player_id, artifact_id):
        self.cursor.execute('''
            INSERT INTO playerartifacts (player_id, artifact_id)
            VALUES (?, ?)
        ''', (player_id, artifact_id))
        self.connection.commit()

    def fetch_artifacts(self):
        self.cursor.execute('SELECT * FROM artifacts')
        return self.cursor.fetchall()

    def fetch_cards(self):
        self.cursor.execute('SELECT * FROM cards')
        return self.cursor.fetchall()
    
    def fetch_basic_cards(self):
        self.cursor.execute('SELECT * FROM cards where rarity = "Basic"')
        return self.cursor.fetchall()
    
    def fetch_players(self):
        self.cursor.execute('SELECT * FROM players')
        return self.cursor.fetchall()
    
    def fetch_player_cards(self, player_id):
        self.cursor.execute('SELECT * FROM playercards WHERE player_id = ?', (player_id,))
        return self.cursor.fetchall()
    
    def fetch_player_artifacts(self, player_id):
        self.cursor.execute('SELECT * FROM playerartifacts WHERE player_id = ?', (player_id,))
        return self.cursor.fetchall()
    
    def fetch_planets(self):
        self.cursor.execute('SELECT * FROM planets')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

# Example usage
if __name__ == "__main__":
    db = Database()

    # Insert sample data
    db.insert_artifact("Tooth Necklace", "Rare", 243)
    db.insert_card("Laser Cannon", 1, "Attack", "Basic", "A simple card", 10)
    db.insert_card("Protective Barrier", 1, "Block", "Basic", "A simple card", 10)

    # Fetch and print data
    print("Artifacts:", db.fetch_artifacts())
    print("Cards:", db.fetch_cards())

    db.close()


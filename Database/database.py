import sqlite3

class Database:
    def __init__(self, db_name="game_data.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    # ---------- Table Creation ----------
    def create_tables(self):
        # Artifacts
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rarity TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')

        # Cards
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value INTEGER NOT NULL,
                type TEXT NOT NULL,
                rarity TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        ''')

        # Players
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                scraps INTEGER NOT NULL,
                health INTEGER NOT NULL,
                max_health INTEGER NOT NULL
            )
        ''')

        # Player-Cards
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playercards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                card_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (card_id) REFERENCES cards(id)
            )
        ''')

        # Player-Artifacts
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playerartifacts (
                player_id INTEGER NOT NULL,
                artifact_id INTEGER NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
            )
        ''')

        # Planets
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS planets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                r INTEGER NOT NULL,
                g INTEGER NOT NULL,
                b INTEGER NOT NULL,
                explored BOOLEAN NOT NULL,
                position_x INTEGER NOT NULL,
                position_y INTEGER NOT NULL,
                size INTEGER NOT NULL                            
            )
        ''')

        self.connection.commit()

    # ---------- Artifact Methods ----------
    def insert_artifact(self, name, rarity, description, price):
        self.cursor.execute('''
            INSERT INTO artifacts (name, rarity, description, price)
            VALUES (?, ?, ?, ?)
        ''', (name, rarity, description, price))
        self.connection.commit()

    def fetch_artifacts(self):
        self.cursor.execute('SELECT * FROM artifacts')
        return self.cursor.fetchall()

    def fetch_artifact_by_name(self, name):
        self.cursor.execute('SELECT * FROM artifacts WHERE name = ?', (name,))
        return self.cursor.fetchone() 
    
    def fetch_artifact_by_id(self, artifact_id):
        self.cursor.execute('SELECT * FROM artifacts WHERE id = ?', (artifact_id,))
        return self.cursor.fetchone()

    def fetch_all_artifacts(self):
        self.cursor.execute('SELECT * FROM artifacts')
        return self.cursor.fetchall()

    def fetch_all_artifact_names(self):
        self.cursor.execute('SELECT name FROM artifacts')
        return [row[0] for row in self.cursor.fetchall()]
    
    def fetch_random_artifact(self):
        self.cursor.execute('SELECT * FROM artifacts ORDER BY RANDOM() LIMIT 1')
        return self.cursor.fetchone()

    # ---------- Card Methods ----------
    def insert_card(self, name, value, type, rarity, description, price):
        self.cursor.execute('''
            INSERT INTO cards (name, value, type, rarity, description, price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, value, type, rarity, description, price))
        self.connection.commit()

    def fetch_cards(self):
        self.cursor.execute('SELECT * FROM cards')
        return self.cursor.fetchall()

    def fetch_card_by_id(self, card_id):
        self.cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
        return self.cursor.fetchone()
    
    def fetch_basic_cards(self):
        self.cursor.execute('SELECT * FROM cards WHERE rarity = "Basic"')
        return self.cursor.fetchall()

    def fetch_all_cards(self):
        self.cursor.execute('SELECT * FROM cards')
        return self.cursor.fetchall()

    def fetch_all_card_names(self):
        self.cursor.execute('SELECT name FROM cards')
        return [row[0] for row in self.cursor.fetchall()]
    
    def fetch_all_non_basic_cards(self):
        self.cursor.execute('SELECT * FROM cards WHERE rarity != "Basic"')
        return self.cursor.fetchall()
    
    def fetch_random_card(self):
        self.cursor.execute('SELECT * FROM cards ORDER BY RANDOM() LIMIT 1')
        return self.cursor.fetchone()

    # ---------- Player Methods ----------
    def insert_player(self, name, credits, scraps, health, max_health):
        self.cursor.execute('''
            INSERT INTO players (name, credits, scraps, health, max_health)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, credits, scraps, health, max_health))
        self.connection.commit()
        return self.cursor.lastrowid 

    def fetch_players(self):
        self.cursor.execute('SELECT * FROM players')
        return self.cursor.fetchall()

    def fetch_player_id(self, name):
        self.cursor.execute('SELECT id FROM players WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def fetch_player(self, player_id):
        self.cursor.execute('SELECT * FROM players WHERE id = ?', (player_id,))
        return self.cursor.fetchone()

    def update_player_currency(self, player_id, credits=None, scraps=None, health=None, max_health=None):
        if credits is not None:
            self.cursor.execute('''
                UPDATE players
                SET credits = ?
                WHERE id = ?
            ''', (credits, player_id))
        if scraps is not None:
            self.cursor.execute('''
                UPDATE players
                SET scraps = ?
                WHERE id = ?
            ''', (scraps, player_id))
        if health is not None:
            self.cursor.execute('''
                UPDATE players
                SET health = ?
                WHERE id = ?
            ''', (health, player_id))
        if max_health is not None:
            self.cursor.execute('''
                UPDATE players
                SET max_health = ?
                WHERE id = ?
            ''', (max_health, player_id))
        self.connection.commit()

    # ---------- Player-Card/Artifact Methods ----------
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

    def fetch_player_cards(self, player_id):
        self.cursor.execute('SELECT * FROM playercards WHERE player_id = ?', (player_id,))
        return self.cursor.fetchall()

    def fetch_player_artifacts(self, player_id):
        self.cursor.execute('SELECT * FROM playerartifacts WHERE player_id = ?', (player_id,))
        return self.cursor.fetchall()

    # ---------- Planet Methods ----------
    def fetch_planets_for_player(self, player_id):
        self.cursor.execute('''
            SELECT name, r, g, b, explored, position_x, position_y, size
            FROM planets WHERE player_id = ?
        ''', (player_id,))
        return self.cursor.fetchall()

    def change_planet_explored(self, player_id, planet_name):
        self.cursor.execute('''
            UPDATE planets
            SET explored = True
            WHERE player_id = ? AND name = ?
        ''', (player_id, planet_name))
        if self.cursor.rowcount == 0:
            print(f"[error] No planet found for player {player_id} with name {planet_name}.")
        self.connection.commit()
    
    def insert_planet(self, player_id, name, r, g, b, explored, x, y, size):
        self.cursor.execute('''
            INSERT INTO planets (player_id, name, r, g, b, explored, position_x, position_y, size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_id, name, r, g, b, explored, x, y, size))
        self.connection.commit()

    # ---------- Utility ----------
    def close(self):
        self.connection.close()

# ---------- Sample Usage ----------
if __name__ == "__main__":
    db = Database()

    # Insert sample data
    db.insert_artifact("Double AA Battery", "Common", "Increase energy by 1", 100)
    db.insert_artifact("Motherboard", "Rare", "Increase CPU by 2", 200)
    db.insert_artifact("Old Scart Cable", "Epic", "Increase RAM by 4", 300)
    db.insert_card("Laser Cannon", 10, "Attack", "Basic", "Deal 10 damage", 10)
    db.insert_card("Protective Barrier", 2, "Block", "Basic", "Gain 2 shield", 10)
    db.insert_card("Railgun", 15, "Attack", "Common", "Deal 15 damage", 25)
    db.insert_card("Fusion shield", 5, "Block", "Common", "Gain 5 shield", 25)
    db.insert_card("Exterminator", 20, "Attack", "Rare", "Deal 20 damage", 50)
    db.insert_card("Vortex shield", 10, "Block", "Rare", "Gain 10 shield", 50)

    # Fetch and print data
    print("Artifacts:", db.fetch_artifacts())
    print("Cards:", db.fetch_cards())

    db.close()


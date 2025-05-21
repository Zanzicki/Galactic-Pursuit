from Components.planet import Planet
from gameobject import GameObject
from State.map import Map


class NewGame:
    def __init__(self, game_world):
        self._game_world = game_world
        self.database = None  # Should be set to your Database instance
        
    def create_new_player(self, name):
        self.database.insert_player(name, 100, 0, 100)
        player_id = self.database.fetch_player_id(name)
        print(f"New player created: {name} (ID: {player_id})")

        self._game_world.map.generate_planets()
        planets = self._game_world.map.planets  # Make sure map.planets is populated
        if not planets:
            print("[error] No planets generated.")
            return None
        for planet in planets:
            print(f"Adding planet: {planet}")
            planet_component = planet.get_component("Planet")
            self.database.cursor.execute('''
                INSERT INTO planets (player_id, name, r, g, b, explored, position_x, position_y, size)
                VALUES (?, ?, ?, ?, ?, ?, ?,?, ?)
            ''', (
                player_id,
                planet_component.name,
                planet_component.color[0],
                planet_component.color[1],
                planet_component.color[2],                
                False,
                int(planet_component.position[0]),
                int(planet_component.position[1]),
                planet_component.size
            ))
        self.database.connection.commit()
        return player_id

    def continue_game(self, player_id):
        self.database.fetch_player(player_id)
        print(f"Continuing game for player ID: {player_id}")

        # Load planets for this player
        planet_rows = self.database.fetch_planets_for_player(player_id)
        for row in planet_rows:
            name, r, g, b, explored, x, y, size = row
            planet = GameObject((x, y))
            planet.add_component(Planet(name, size, (r, g, b), (x, y), self._game_world))  # Use correct color/type
            planet.get_component("Planet")._explored = explored
            self._game_world.map.planets.append(planet)
            self._game_world._gameObjects.append(planet)

    def get_player_list(self):
        return self.database.fetch_players()
